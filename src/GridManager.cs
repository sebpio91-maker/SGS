using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;

namespace PokerGrid
{
    internal class ManagedWindow
    {
        public IntPtr Hwnd;
        public SiteProfile Site;
        public int Slot = -1;            // -1 = no slot (waiting or released)
        public bool Released;            // dragged out of the grid by the user
        public double Ratio;             // width / height of the visible window, <= 0 = stretch
        public long Order;               // arrival order, used for fair slot assignment
        public DateTime PlacedAt = DateTime.MinValue;
        public bool Verified = true;     // false until we checked the client did not move it back
        public Rectangle Expected;
    }

    /// <summary>Core logic: detects poker tables and keeps them in the slots of the active layout.</summary>
    internal class GridManager
    {
        private AppConfig cfg;
        private LayoutDef layout;
        private List<Rectangle> slots = new List<Rectangle>();
        private readonly Dictionary<IntPtr, ManagedWindow> managed = new Dictionary<IntPtr, ManagedWindow>();
        private readonly Dictionary<IntPtr, DateTime> pending = new Dictionary<IntPtr, DateTime>();
        private readonly Dictionary<IntPtr, Rectangle> moveStart = new Dictionary<IntPtr, Rectangle>();
        private long orderCounter;

        public bool Paused;
        public bool AutoLayoutEnabled;
        private DateTime shrinkSince = DateTime.MinValue;
        public event EventHandler StateChanged;

        public GridManager(AppConfig config)
        {
            ApplyConfig(config);
        }

        public AppConfig Config { get { return cfg; } }
        public LayoutDef Layout { get { return layout; } }
        public IList<Rectangle> Slots { get { return slots; } }
        public int ManagedCount { get { return managed.Count; } }

        public int[] SlotCounts()
        {
            var counts = new int[slots.Count];
            foreach (ManagedWindow m in managed.Values)
                if (m.Slot >= 0 && m.Slot < counts.Length)
                    counts[m.Slot]++;
            return counts;
        }

        public string DescribeWindow(IntPtr hwnd)
        {
            ManagedWindow m;
            if (!managed.TryGetValue(hwnd, out m))
                return "";
            if (m.Released) return m.Site.Name + " (freigegeben)";
            if (m.Slot < 0) return m.Site.Name + " (wartet)";
            return m.Site.Name + " → Slot " + (m.Slot + 1);
        }

        // ------------------------------------------------------------------ configuration

        public void ApplyConfig(AppConfig config)
        {
            cfg = config;
            layout = cfg.FindLayout(cfg.ActiveLayout) ?? cfg.Layouts[0];
            AutoLayoutEnabled = cfg.AutoLayouts.Count > 0;
            shrinkSince = DateTime.MinValue;
            slots = layout.ComputeSlots();

            // Keep known windows and their slots, just re-link them to the new site profiles.
            foreach (IntPtr h in managed.Keys.ToList())
            {
                ManagedWindow m = managed[h];
                SiteProfile site = cfg.Sites.FirstOrDefault(s => s.Enabled && s.Name == m.Site.Name);
                if (site == null)
                {
                    managed.Remove(h);
                    continue;
                }
                m.Site = site;
                if (site.AspectRatio != 0)
                    m.Ratio = site.AspectRatio;
                if (m.Slot >= slots.Count)
                    m.Slot = -1;
            }
            pending.Clear();
            if (!Paused)
                ArrangeAll();
        }

        public void SetLayout(string name)
        {
            LayoutDef l = cfg.FindLayout(name);
            if (l == null)
                return;
            layout = l;
            cfg.ActiveLayout = l.Name;
            slots = layout.ComputeSlots();
            Compact();
        }

        public string NextLayoutName()
        {
            int idx = cfg.Layouts.IndexOf(layout);
            return cfg.Layouts[(idx + 1) % cfg.Layouts.Count].Name;
        }

        /// <summary>Screen resolution or monitor setup changed.</summary>
        public void RefreshScreens()
        {
            slots = layout.ComputeSlots();
            ArrangeAll();
        }

        // ------------------------------------------------------------------ periodic scan

        public void Tick()
        {
            DateTime now = DateTime.Now;
            bool changed = false;
            bool active = !Paused && cfg.AutoArrange;
            var seen = new HashSet<IntPtr>();

            foreach (WinInfo w in WindowScanner.Scan())
            {
                SiteProfile site = MatchSite(w);
                if (site == null)
                    continue;
                seen.Add(w.Hwnd);

                ManagedWindow m;
                if (managed.TryGetValue(w.Hwnd, out m))
                {
                    m.Site = site;
                    continue;
                }

                DateTime first;
                if (!pending.TryGetValue(w.Hwnd, out first))
                {
                    pending[w.Hwnd] = now;
                    continue;
                }
                if ((now - first).TotalMilliseconds < cfg.NewWindowDelayMs)
                    continue;

                // "auto" ratio can only be measured on a normal (not minimized/maximized) window.
                if (site.AspectRatio == 0 && (w.Minimized || w.Maximized))
                {
                    if (active && cfg.RestoreMinimized)
                        NativeMethods.ShowWindow(w.Hwnd, NativeMethods.SW_SHOWNOACTIVATE);
                    continue;
                }

                pending.Remove(w.Hwnd);
                m = new ManagedWindow();
                m.Hwnd = w.Hwnd;
                m.Site = site;
                m.Order = ++orderCounter;
                m.Ratio = site.AspectRatio != 0 ? site.AspectRatio
                    : (w.Bounds.Height > 0 ? (double)w.Bounds.Width / w.Bounds.Height : -1);
                managed[w.Hwnd] = m;
                changed = true;
            }

            foreach (IntPtr h in managed.Keys.ToList())
                if (!seen.Contains(h))
                {
                    managed.Remove(h);
                    moveStart.Remove(h);
                    changed = true;
                }
            foreach (IntPtr h in pending.Keys.ToList())
                if (!seen.Contains(h))
                    pending.Remove(h);

            if (active && ApplyAutoLayout(now))
                changed = true;

            if (active)
            {
                // New windows and windows waiting for a free slot (Overflow=Wait or layout had no room).
                foreach (ManagedWindow m in managed.Values.Where(x => x.Slot < 0 && !x.Released).OrderBy(x => x.Order).ToList())
                {
                    AssignSlot(m);
                    if (m.Slot >= 0)
                    {
                        Place(m, IsFresh(m));
                        changed = true;
                    }
                }

                // Some clients restore their saved position right after opening a table.
                // Check once shortly after placing and put the window back if that happened.
                foreach (ManagedWindow m in managed.Values)
                {
                    if (m.Verified || (now - m.PlacedAt).TotalMilliseconds < 1200)
                        continue;
                    m.Verified = true;
                    if (m.Slot >= 0 && !NativeMethods.IsIconic(m.Hwnd)
                        && !WindowScanner.IsNear(WindowScanner.GetVisibleBounds(m.Hwnd), m.Expected, 3))
                        Place(m, false);
                }
            }

            if (changed)
                RaiseChanged();
        }

        private SiteProfile MatchSite(WinInfo w)
        {
            foreach (SiteProfile s in cfg.Sites)
                if (s.Matches(w))
                    return s;
            return null;
        }

        /// <summary>
        /// Picks the first layout of AutoLayout that has enough slots for all tables.
        /// Switches to a bigger layout immediately, to a smaller one only after the table
        /// count stayed low for AutoLayoutShrinkDelayMs (tournament table moves close and
        /// open tables in quick succession).
        /// </summary>
        private bool ApplyAutoLayout(DateTime now)
        {
            if (!AutoLayoutEnabled)
                return false;
            int count = managed.Values.Count(x => !x.Released);
            LayoutDef want = null;
            int wantSlots = 0;
            foreach (string name in cfg.AutoLayouts)
            {
                LayoutDef l = cfg.FindLayout(name);
                if (l == null)
                    continue;
                want = l;
                wantSlots = l.ComputeSlots().Count;
                if (wantSlots >= count)
                    break;
            }
            if (want == null || want == layout)
            {
                shrinkSince = DateTime.MinValue;
                return false;
            }
            if (wantSlots < slots.Count)
            {
                if (shrinkSince == DateTime.MinValue)
                    shrinkSince = now;
                if ((now - shrinkSince).TotalMilliseconds < cfg.AutoLayoutShrinkDelayMs)
                    return false;
            }
            shrinkSince = DateTime.MinValue;
            SetLayout(want.Name);
            return true;
        }

        private static bool IsFresh(ManagedWindow m)
        {
            return m.PlacedAt == DateTime.MinValue;
        }

        // ------------------------------------------------------------------ user drag & drop

        public void OnMoveSizeStart(IntPtr hwnd)
        {
            if (managed.ContainsKey(hwnd))
                moveStart[hwnd] = WindowScanner.GetVisibleBounds(hwnd);
        }

        public void OnMoveSizeEnd(IntPtr hwnd)
        {
            ManagedWindow m;
            if (!managed.TryGetValue(hwnd, out m))
                return;

            Rectangle start;
            bool hadStart = moveStart.TryGetValue(hwnd, out start);
            moveStart.Remove(hwnd);
            if (Paused)
                return;

            Rectangle now = WindowScanner.GetVisibleBounds(hwnd);
            bool resized = hadStart && (Math.Abs(start.Width - now.Width) > 2 || Math.Abs(start.Height - now.Height) > 2);

            int target;
            if (resized)
            {
                // Resizing is not a drop: the cursor sits on the border and may point into a neighbour slot.
                target = m.Slot >= 0 ? m.Slot : SlotAt(Center(now));
            }
            else
            {
                target = SlotAt(Cursor.Position);
                if (target < 0)
                    target = SlotAt(Center(now));
            }

            if (target < 0)
            {
                if (cfg.SnapBack && m.Slot >= 0)
                {
                    Place(m, false);
                }
                else
                {
                    m.Slot = -1;
                    m.Released = true;
                }
                RaiseChanged();
                return;
            }

            m.Released = false;
            if (target != m.Slot)
            {
                int old = m.Slot;
                if (cfg.SwapOnDrop && old >= 0)
                {
                    foreach (ManagedWindow other in managed.Values.Where(x => x != m && x.Slot == target).ToList())
                    {
                        other.Slot = old;
                        Place(other, false);
                    }
                }
                m.Slot = target;
            }
            Place(m, false);
            RaiseChanged();
        }

        private int SlotAt(Point p)
        {
            for (int i = 0; i < slots.Count; i++)
                if (slots[i].Contains(p))
                    return i;
            return -1;
        }

        private static Point Center(Rectangle r)
        {
            return new Point(r.X + r.Width / 2, r.Y + r.Height / 2);
        }

        // ------------------------------------------------------------------ commands

        /// <summary>Puts every known table (including released ones) back into its slot.</summary>
        public void ArrangeAll()
        {
            foreach (ManagedWindow m in managed.Values)
            {
                m.Released = false;
                if (m.Slot >= slots.Count)
                    m.Slot = -1;
            }
            foreach (ManagedWindow m in managed.Values.Where(x => x.Slot < 0).OrderBy(x => x.Order).ToList())
                AssignSlot(m);
            foreach (ManagedWindow m in managed.Values)
                Place(m, IsFresh(m));
            RaiseChanged();
        }

        /// <summary>Re-numbers all tables so they fill the slots from the first one without gaps.</summary>
        public void Compact()
        {
            List<ManagedWindow> ordered = managed.Values
                .OrderBy(x => x.Slot < 0 ? int.MaxValue : x.Slot)
                .ThenBy(x => x.Order)
                .ToList();
            foreach (ManagedWindow m in ordered)
            {
                m.Slot = -1;
                m.Released = false;
            }
            foreach (ManagedWindow m in ordered)
                AssignSlot(m);
            foreach (ManagedWindow m in ordered)
                Place(m, IsFresh(m));
            RaiseChanged();
        }

        // ------------------------------------------------------------------ placement

        private void AssignSlot(ManagedWindow m)
        {
            if (slots.Count == 0)
                return;
            int[] counts = SlotCounts();
            for (int i = 0; i < counts.Length; i++)
                if (counts[i] == 0)
                {
                    m.Slot = i;
                    return;
                }
            if (cfg.Overflow == OverflowMode.Stack)
            {
                int best = 0;
                for (int i = 1; i < counts.Length; i++)
                    if (counts[i] < counts[best])
                        best = i;
                m.Slot = best;
            }
        }

        private void Place(ManagedWindow m, bool verifyLater)
        {
            if (m.Slot < 0 || m.Slot >= slots.Count || !NativeMethods.IsWindow(m.Hwnd))
                return;

            if (NativeMethods.IsIconic(m.Hwnd))
            {
                if (!cfg.RestoreMinimized)
                    return;
                NativeMethods.ShowWindow(m.Hwnd, NativeMethods.SW_SHOWNOACTIVATE);
            }
            if (NativeMethods.IsZoomed(m.Hwnd))
                NativeMethods.ShowWindow(m.Hwnd, NativeMethods.SW_SHOWNOACTIVATE);

            Rectangle target = Fit(slots[m.Slot], m.Ratio, layout.Align);
            m.Expected = WindowScanner.SetVisibleBounds(m.Hwnd, target);
            m.PlacedAt = DateTime.Now;
            m.Verified = !verifyLater;
        }

        /// <summary>Largest rectangle with the given aspect ratio that fits into the slot.</summary>
        public static Rectangle Fit(Rectangle slot, double ratio, AlignMode align)
        {
            if (ratio <= 0)
                return slot;
            int w = slot.Width;
            int h = (int)Math.Round(w / ratio);
            if (h > slot.Height)
            {
                h = slot.Height;
                w = (int)Math.Round(h * ratio);
            }
            int x = slot.X, y = slot.Y;
            if (align == AlignMode.Center || align == AlignMode.Top)
                x += (slot.Width - w) / 2;
            if (align == AlignMode.Center || align == AlignMode.Left)
                y += (slot.Height - h) / 2;
            return new Rectangle(x, y, w, h);
        }

        private void RaiseChanged()
        {
            EventHandler handler = StateChanged;
            if (handler != null)
                handler(this, EventArgs.Empty);
        }
    }
}
