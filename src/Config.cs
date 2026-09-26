using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Windows.Forms;

namespace PokerGrid
{
    internal enum OverflowMode { Stack, Wait }

    internal enum AlignMode { Center, TopLeft, Top, Left, Spread }

    internal class SlotSpec
    {
        public int Monitor = -1;   // -1 = use the layout's monitor
        public string X, Y, W, H;
    }

    internal class LayoutDef
    {
        public string Name;
        public int Monitor = 0;
        public int Columns = 2;
        public int Rows = 2;
        public int Margin = 0;
        public int Gap = 0;
        public bool UseWorkingArea = true;
        public bool ColumnFirst = false;
        public AlignMode Align = AlignMode.Center;
        public int Overlap = 0;   // percent a table may grow taller than its slot
        public bool Dynamic;      // Mode=Dynamic: rows are planned at runtime by BestPlan
        public int MaxColumns = 5;
        public int MaxRows = 4;
        public List<SlotSpec> Slots = new List<SlotSpec>();

        // Current plan of a dynamic layout: tables per row (top to bottom) and row heights.
        public int[] RowCounts;
        public int[] RowHeights;

        /// <summary>
        /// Mode=Dynamic: distributes the tables over 1..MaxRows rows. Rows may hold different
        /// numbers of tables (7 → 3 + 4); rows with fewer tables go on top and get wider
        /// cells and more height. Chooses the plan in which the smallest table is biggest,
        /// then the one with the most total table area, then the one with fewer rows.
        /// </summary>
        public void BestPlan(IList<double> ratios, out int[] bestCounts, out int[] bestHeights)
        {
            Rectangle a = GridArea();
            double grow = 1 + Math.Max(0, Overlap) / 100.0;
            int n = Math.Max(1, ratios.Count);
            double rMin = ratios.Count > 0 ? ratios.Min() : 1.4;
            double rMax = ratios.Count > 0 ? ratios.Max() : 1.4;
            double rMean = ratios.Count > 0 ? ratios.Average() : 1.4;

            bestCounts = null;
            bestHeights = null;
            double bestMin = -1, bestSum = -1;

            for (int rows = 1; rows <= Math.Max(1, MaxRows) && rows <= n; rows++)
            {
                int[] counts = new int[rows];
                for (int i = 0; i < rows; i++)
                    counts[i] = n / rows + (i >= rows - n % rows ? 1 : 0);   // fewer tables on top
                if (counts[rows - 1] > Math.Max(1, MaxColumns))
                    continue;

                double[] cellW = new double[rows];
                double[] need = new double[rows];
                for (int i = 0; i < rows; i++)
                {
                    cellW[i] = (a.Width - Gap * (counts[i] - 1)) / (double)counts[i];
                    need[i] = cellW[i] / rMin;   // row height at which even the tallest table uses the full width
                }
                double[] heights = DistributeHeights(need, a.Height - Gap * (rows - 1));

                double min = double.MaxValue, sum = 0;
                for (int i = 0; i < rows; i++)
                {
                    double maxH = Math.Min(heights[i] * grow, a.Height);
                    min = Math.Min(min, Math.Min(TableArea(cellW[i], maxH, rMin), TableArea(cellW[i], maxH, rMax)));
                    sum += counts[i] * TableArea(cellW[i], maxH, rMean);
                }

                bool better;
                if (bestMin < 0 || min > bestMin * 1.01)
                    better = true;
                else if (min < bestMin * 0.99)
                    better = false;
                else if (sum > bestSum * 1.01)
                    better = true;
                else if (sum < bestSum * 0.99)
                    better = false;
                else
                    better = rows < bestCounts.Length;

                if (better)
                {
                    bestMin = min;
                    bestSum = sum;
                    bestCounts = counts;
                    bestHeights = heights.Select(h => (int)Math.Floor(h)).ToArray();
                }
            }

            if (bestCounts == null)
            {
                // More tables than MaxColumns x MaxRows: full grid, the rest gets stacked.
                int rows = Math.Max(1, MaxRows);
                bestCounts = Enumerable.Repeat(Math.Max(1, MaxColumns), rows).ToArray();
                bestHeights = DistributeHeights(Enumerable.Repeat(1.0, rows).ToArray(), a.Height - Gap * (rows - 1))
                    .Select(h => (int)Math.Floor(h)).ToArray();
            }
        }

        /// <summary>Gives each row the height it needs; spare height is shared, missing height taken proportionally.</summary>
        private static double[] DistributeHeights(double[] need, double available)
        {
            double total = need.Sum();
            var result = new double[need.Length];
            for (int i = 0; i < need.Length; i++)
                result[i] = total <= available
                    ? need[i] + (available - total) / need.Length
                    : need[i] * available / total;
            return result;
        }

        private static double TableArea(double maxW, double maxH, double ratio)
        {
            double w = Math.Min(maxW, maxH * ratio);
            return w * (w / ratio);
        }

        private bool HasRowPlan
        {
            get { return Dynamic && RowCounts != null && Slots.Count == 0; }
        }

        /// <summary>
        /// Where a table with the given aspect ratio goes for slot <paramref name="index"/>:
        /// the largest size that fits the slot's width and its height enlarged by Overlap
        /// percent, positioned according to Align and kept inside the monitor.
        /// Overlap only works vertically: tables side by side would cover each other's seats.
        /// </summary>
        public Rectangle PlaceTable(int index, Rectangle slot, double ratio)
        {
            if (ratio <= 0)
                return slot;

            Rectangle area = Slots.Count > 0
                ? MonitorArea(Slots[index].Monitor >= 0 ? Slots[index].Monitor : Monitor, UseWorkingArea)
                : GridArea();

            double grow = 1 + Math.Max(0, Overlap) / 100.0;
            double maxW = slot.Width;
            double maxH = Math.Min(slot.Height * grow, Math.Max(slot.Height, area.Height));
            int w = (int)Math.Round(Math.Min(maxW, maxH * ratio));
            int h = (int)Math.Round(w / ratio);
            int x, y;

            if (HasRowPlan)
            {
                int row = 0, col = index;
                while (row < RowCounts.Length - 1 && col >= RowCounts[row])
                {
                    col -= RowCounts[row];
                    row++;
                }
                int cols = RowCounts[row];
                x = cols > 1 ? area.X + (int)Math.Round((double)col * (area.Width - w) / (cols - 1))
                             : area.X + (area.Width - w) / 2;
                // First row flush with the top, last row flush with the bottom, others centered in their band.
                if (RowCounts.Length == 1)
                    y = slot.Y + (slot.Height - h) / 2;
                else if (row == 0)
                    y = slot.Y;
                else if (row == RowCounts.Length - 1)
                    y = slot.Bottom - h;
                else
                    y = slot.Y + (slot.Height - h) / 2;
                return new Rectangle(x, Math.Max(area.Y, Math.Min(y, area.Bottom - h)), w, h);
            }

            if (Align == AlignMode.Spread && Slots.Count == 0)
            {
                // Outer tables flush with the screen edges, the others evenly in between,
                // so free space and overlap are shared equally by all rows and columns.
                int cols = Math.Max(1, Columns), rows = Math.Max(1, Rows);
                int col = ColumnFirst ? index / rows : index % cols;
                int row = ColumnFirst ? index % rows : index / cols;
                x = cols > 1 ? area.X + (int)Math.Round((double)col * (area.Width - w) / (cols - 1))
                             : area.X + (area.Width - w) / 2;
                y = rows > 1 ? area.Y + (int)Math.Round((double)row * (area.Height - h) / (rows - 1))
                             : area.Y + (area.Height - h) / 2;
                return new Rectangle(x, y, w, h);
            }

            x = slot.X;
            y = slot.Y;
            if (Align == AlignMode.Center || Align == AlignMode.Top || Align == AlignMode.Spread)
                x += (slot.Width - w) / 2;
            if (Align == AlignMode.Center || Align == AlignMode.Left || Align == AlignMode.Spread)
                y += (slot.Height - h) / 2;
            // A table taller than its slot must not stick out of the screen.
            if (w <= area.Width)
                x = Math.Max(area.X, Math.Min(x, area.Right - w));
            if (h <= area.Height)
                y = Math.Max(area.Y, Math.Min(y, area.Bottom - h));
            return new Rectangle(x, y, w, h);
        }

        private Rectangle GridArea()
        {
            Rectangle a = MonitorArea(Monitor, UseWorkingArea);
            a.Inflate(-Margin, -Margin);
            return a;
        }

        /// <summary>Name for tray and overlay; dynamic layouts also show the current rows, e.g. "Dynamisch (3+4)".</summary>
        public string DisplayName
        {
            get { return HasRowPlan ? string.Format("{0} ({1})", Name, string.Join("+", RowCounts.Select(c => c.ToString()))) : Name; }
        }

        public List<Rectangle> ComputeSlots()
        {
            var result = new List<Rectangle>();

            if (Slots.Count > 0)
            {
                foreach (SlotSpec s in Slots)
                {
                    Rectangle area = MonitorArea(s.Monitor >= 0 ? s.Monitor : Monitor, UseWorkingArea);
                    result.Add(new Rectangle(
                        area.X + Resolve(s.X, area.Width),
                        area.Y + Resolve(s.Y, area.Height),
                        Resolve(s.W, area.Width),
                        Resolve(s.H, area.Height)));
                }
                return result;
            }

            Rectangle a = GridArea();

            if (HasRowPlan)
            {
                int top = a.Y;
                for (int r = 0; r < RowCounts.Length; r++)
                {
                    int cols = RowCounts[r];
                    int cellW = (a.Width - Gap * (cols - 1)) / cols;
                    int rowH = r == RowCounts.Length - 1 ? a.Bottom - top : RowHeights[r];
                    for (int c = 0; c < cols; c++)
                        result.Add(new Rectangle(a.X + c * (cellW + Gap), top, cellW, rowH));
                    top += rowH + Gap;
                }
                return result;
            }

            int gridCols = Math.Max(1, Columns), gridRows = Math.Max(1, Rows);
            int gridCellW = (a.Width - Gap * (gridCols - 1)) / gridCols;
            int gridCellH = (a.Height - Gap * (gridRows - 1)) / gridRows;

            if (ColumnFirst)
            {
                for (int c = 0; c < gridCols; c++)
                    for (int r = 0; r < gridRows; r++)
                        result.Add(new Rectangle(a.X + c * (gridCellW + Gap), a.Y + r * (gridCellH + Gap), gridCellW, gridCellH));
            }
            else
            {
                for (int r = 0; r < gridRows; r++)
                    for (int c = 0; c < gridCols; c++)
                        result.Add(new Rectangle(a.X + c * (gridCellW + Gap), a.Y + r * (gridCellH + Gap), gridCellW, gridCellH));
            }
            return result;
        }

        /// <summary>0 = primary monitor, 1..n = monitors sorted from left to right.</summary>
        public static Rectangle MonitorArea(int index, bool workingArea)
        {
            Screen screen = Screen.PrimaryScreen;
            if (index > 0)
            {
                Screen[] sorted = Screen.AllScreens.OrderBy(s => s.Bounds.X).ThenBy(s => s.Bounds.Y).ToArray();
                if (index <= sorted.Length)
                    screen = sorted[index - 1];
            }
            return workingArea ? screen.WorkingArea : screen.Bounds;
        }

        private static int Resolve(string value, int total)
        {
            string v = value.Trim();
            if (v.EndsWith("%"))
            {
                double pct = AppConfig.ParseDouble(v.Substring(0, v.Length - 1));
                return (int)Math.Round(total * pct / 100.0);
            }
            return (int)Math.Round(AppConfig.ParseDouble(v));
        }
    }

    internal class SiteProfile
    {
        public string Name;
        public bool Enabled = true;
        public List<string> Processes = new List<string>();
        public Regex ClassRegex;
        public Regex TitleRegex;
        public Regex ExcludeTitleRegex;
        public double AspectRatio = 0;   // 0 = auto (take from window), < 0 = stretch to slot
        public int MinWidth = 200;
        public int MinHeight = 150;

        public bool HasCriteria
        {
            get { return Processes.Count > 0 || ClassRegex != null || TitleRegex != null; }
        }

        public bool Matches(WinInfo w)
        {
            if (!Enabled || !HasCriteria)
                return false;
            if (Processes.Count > 0 && !Processes.Contains(NormalizeProcess(w.Process)))
                return false;
            if (ClassRegex != null && !ClassRegex.IsMatch(w.ClassName))
                return false;
            if (TitleRegex != null && !TitleRegex.IsMatch(w.Title))
                return false;
            if (ExcludeTitleRegex != null && ExcludeTitleRegex.IsMatch(w.Title))
                return false;
            // Minimized windows report a tiny rectangle, the size check only applies to normal windows.
            if (!w.Minimized && (w.Bounds.Width < MinWidth || w.Bounds.Height < MinHeight))
                return false;
            return true;
        }

        public static string NormalizeProcess(string name)
        {
            string n = (name ?? "").Trim().ToLowerInvariant();
            return n.EndsWith(".exe") ? n.Substring(0, n.Length - 4) : n;
        }
    }

    internal class AppConfig
    {
        public int PollIntervalMs = 500;
        public int NewWindowDelayMs = 500;
        public bool AutoArrange = true;
        public bool SwapOnDrop = true;
        public bool SnapBack = true;
        public bool RestoreMinimized = true;
        public OverflowMode Overflow = OverflowMode.Stack;
        public string ActiveLayout = "";
        public List<string> AutoLayouts = new List<string>();
        public int AutoLayoutShrinkDelayMs = 5000;

        public string HotkeyArrange = "";
        public string HotkeyCompact = "";
        public string HotkeyPause = "";
        public string HotkeyNextLayout = "";
        public string HotkeyOverlay = "";

        public List<LayoutDef> Layouts = new List<LayoutDef>();
        public List<SiteProfile> Sites = new List<SiteProfile>();
        public List<string> Warnings = new List<string>();

        public LayoutDef FindLayout(string name)
        {
            foreach (LayoutDef l in Layouts)
                if (string.Equals(l.Name, name, StringComparison.OrdinalIgnoreCase))
                    return l;
            return null;
        }

        // ------------------------------------------------------------------ loading

        public static AppConfig Load(string path)
        {
            if (!File.Exists(path))
                File.WriteAllText(path, DefaultConfig.Text, new UTF8Encoding(true));

            var cfg = new AppConfig();
            string section = "";
            LayoutDef layout = null;
            SiteProfile site = null;
            string[] lines = File.ReadAllLines(path);

            for (int i = 0; i < lines.Length; i++)
            {
                string line = lines[i].Trim();
                int lineNo = i + 1;
                if (line.Length == 0 || line.StartsWith(";") || line.StartsWith("#"))
                    continue;

                if (line.StartsWith("[") && line.EndsWith("]"))
                {
                    section = line.Substring(1, line.Length - 2).Trim();
                    layout = null;
                    site = null;
                    if (section.StartsWith("Layout:", StringComparison.OrdinalIgnoreCase))
                    {
                        layout = new LayoutDef();
                        layout.Name = section.Substring(7).Trim();
                        cfg.Layouts.Add(layout);
                    }
                    else if (section.StartsWith("Site:", StringComparison.OrdinalIgnoreCase))
                    {
                        site = new SiteProfile();
                        site.Name = section.Substring(5).Trim();
                        cfg.Sites.Add(site);
                    }
                    else if (!section.Equals("General", StringComparison.OrdinalIgnoreCase))
                    {
                        cfg.Warnings.Add(string.Format("Zeile {0}: unbekannter Abschnitt [{1}]", lineNo, section));
                    }
                    continue;
                }

                int eq = line.IndexOf('=');
                if (eq <= 0)
                {
                    cfg.Warnings.Add(string.Format("Zeile {0}: kein Schlüssel=Wert: {1}", lineNo, line));
                    continue;
                }
                string key = line.Substring(0, eq).Trim();
                string value = line.Substring(eq + 1).Trim();

                try
                {
                    bool known;
                    if (layout != null)
                        known = ApplyLayoutKey(layout, key, value);
                    else if (site != null)
                        known = ApplySiteKey(site, key, value);
                    else if (section.Equals("General", StringComparison.OrdinalIgnoreCase))
                        known = cfg.ApplyGeneralKey(key, value);
                    else
                        known = true;   // already warned about the section
                    if (!known)
                        cfg.Warnings.Add(string.Format("Zeile {0}: unbekannter Schlüssel '{1}' in [{2}]", lineNo, key, section));
                }
                catch (Exception ex)
                {
                    cfg.Warnings.Add(string.Format("Zeile {0}: ungültiger Wert für '{1}': {2}", lineNo, key, ex.Message));
                }
            }

            if (cfg.Layouts.Count == 0)
            {
                cfg.Warnings.Add("Kein [Layout:...] definiert, verwende 2x2.");
                var fallback = new LayoutDef();
                fallback.Name = "2x2";
                cfg.Layouts.Add(fallback);
            }
            if (cfg.FindLayout(cfg.ActiveLayout) == null)
            {
                if (cfg.ActiveLayout.Length > 0)
                    cfg.Warnings.Add(string.Format("ActiveLayout '{0}' nicht gefunden, verwende '{1}'.", cfg.ActiveLayout, cfg.Layouts[0].Name));
                cfg.ActiveLayout = cfg.Layouts[0].Name;
            }
            foreach (string n in cfg.AutoLayouts)
                if (cfg.FindLayout(n) == null)
                    cfg.Warnings.Add(string.Format("AutoLayout: Layout '{0}' nicht gefunden.", n));
            foreach (SiteProfile s in cfg.Sites)
                if (s.Enabled && !s.HasCriteria)
                    cfg.Warnings.Add(string.Format("[Site:{0}] braucht mindestens Process, Class oder TitleRegex und wird ignoriert.", s.Name));
            if (cfg.PollIntervalMs < 100)
                cfg.PollIntervalMs = 100;

            return cfg;
        }

        private bool ApplyGeneralKey(string key, string value)
        {
            switch (key.ToLowerInvariant())
            {
                case "pollintervalms": PollIntervalMs = ParseInt(value); return true;
                case "newwindowdelayms": NewWindowDelayMs = ParseInt(value); return true;
                case "autoarrange": AutoArrange = ParseBool(value); return true;
                case "swapondrop": SwapOnDrop = ParseBool(value); return true;
                case "snapback": SnapBack = ParseBool(value); return true;
                case "restoreminimized": RestoreMinimized = ParseBool(value); return true;
                case "overflow": Overflow = (OverflowMode)ParseEnum(typeof(OverflowMode), value); return true;
                case "activelayout": ActiveLayout = value; return true;
                case "autolayout":
                    AutoLayouts.Clear();
                    foreach (string n in value.Split(','))
                        if (n.Trim().Length > 0)
                            AutoLayouts.Add(n.Trim());
                    return true;
                case "autolayoutshrinkdelayms": AutoLayoutShrinkDelayMs = ParseInt(value); return true;
                case "hotkeyarrange": HotkeyArrange = value; return true;
                case "hotkeycompact": HotkeyCompact = value; return true;
                case "hotkeypause": HotkeyPause = value; return true;
                case "hotkeynextlayout": HotkeyNextLayout = value; return true;
                case "hotkeyoverlay": HotkeyOverlay = value; return true;
            }
            return false;
        }

        private static bool ApplyLayoutKey(LayoutDef l, string key, string value)
        {
            string k = key.ToLowerInvariant();
            switch (k)
            {
                case "monitor": l.Monitor = ParseInt(value); return true;
                case "columns": l.Columns = ParseInt(value); return true;
                case "rows": l.Rows = ParseInt(value); return true;
                case "margin": l.Margin = ParseInt(value); return true;
                case "gap": l.Gap = ParseInt(value); return true;
                case "useworkingarea": l.UseWorkingArea = ParseBool(value); return true;
                case "overlap": l.Overlap = ParseInt(value); return true;
                case "maxcolumns": l.MaxColumns = ParseInt(value); return true;
                case "maxrows": l.MaxRows = ParseInt(value); return true;
                case "mode":
                    l.Dynamic = value.Trim().Equals("Dynamic", StringComparison.OrdinalIgnoreCase);
                    if (!l.Dynamic && !value.Trim().Equals("Grid", StringComparison.OrdinalIgnoreCase))
                        throw new FormatException("erwartet Grid oder Dynamic");
                    return true;
                case "align": l.Align = (AlignMode)ParseEnum(typeof(AlignMode), value); return true;
                case "order":
                    l.ColumnFirst = value.Trim().Equals("ColumnFirst", StringComparison.OrdinalIgnoreCase);
                    if (!l.ColumnFirst && !value.Trim().Equals("RowFirst", StringComparison.OrdinalIgnoreCase))
                        throw new FormatException("erwartet RowFirst oder ColumnFirst");
                    return true;
            }
            if (k.StartsWith("slot"))
            {
                l.Slots.Add(ParseSlot(value));
                return true;
            }
            return false;
        }

        private static bool ApplySiteKey(SiteProfile s, string key, string value)
        {
            switch (key.ToLowerInvariant())
            {
                case "enabled": s.Enabled = ParseBool(value); return true;
                case "process":
                    s.Processes.Clear();
                    foreach (string p in value.Split(','))
                        if (p.Trim().Length > 0)
                            s.Processes.Add(SiteProfile.NormalizeProcess(p));
                    return true;
                case "class": s.ClassRegex = ParseRegex(value); return true;
                case "titleregex": s.TitleRegex = ParseRegex(value); return true;
                case "excludetitleregex": s.ExcludeTitleRegex = ParseRegex(value); return true;
                case "aspectratio": s.AspectRatio = ParseRatio(value); return true;
                case "minwidth": s.MinWidth = ParseInt(value); return true;
                case "minheight": s.MinHeight = ParseInt(value); return true;
            }
            return false;
        }

        // ------------------------------------------------------------------ value parsing

        private static SlotSpec ParseSlot(string value)
        {
            var spec = new SlotSpec();
            string v = value;
            int colon = v.IndexOf(':');
            if (colon >= 0)
            {
                spec.Monitor = ParseInt(v.Substring(0, colon));
                v = v.Substring(colon + 1);
            }
            string[] parts = v.Split(',');
            if (parts.Length != 4)
                throw new FormatException("erwartet [Monitor:]X,Y,Breite,Höhe");
            spec.X = parts[0]; spec.Y = parts[1]; spec.W = parts[2]; spec.H = parts[3];
            // Validate now so errors show up when loading.
            foreach (string p in parts)
                ParseDouble(p.Trim().TrimEnd('%'));
            return spec;
        }

        private static Regex ParseRegex(string value)
        {
            if (value.Length == 0)
                return null;
            return new Regex(value, RegexOptions.IgnoreCase | RegexOptions.CultureInvariant);
        }

        private static double ParseRatio(string value)
        {
            string v = value.Trim().ToLowerInvariant();
            if (v == "auto" || v.Length == 0)
                return 0;
            if (v == "stretch" || v == "none")
                return -1;
            string[] parts = v.Split('x', ':', '/');
            double r = parts.Length == 2 ? ParseDouble(parts[0]) / ParseDouble(parts[1]) : ParseDouble(v);
            if (r <= 0 || double.IsInfinity(r) || double.IsNaN(r))
                throw new FormatException("muss größer als 0 sein");
            return r;
        }

        public static double ParseDouble(string value)
        {
            return double.Parse(value.Trim().Replace(',', '.'), NumberStyles.Float, CultureInfo.InvariantCulture);
        }

        private static int ParseInt(string value)
        {
            return int.Parse(value.Trim(), NumberStyles.Integer, CultureInfo.InvariantCulture);
        }

        private static bool ParseBool(string value)
        {
            switch (value.Trim().ToLowerInvariant())
            {
                case "1": case "true": case "yes": case "ja": case "on": return true;
                case "0": case "false": case "no": case "nein": case "off": return false;
            }
            throw new FormatException("erwartet true oder false");
        }

        private static object ParseEnum(Type t, string value)
        {
            foreach (string name in Enum.GetNames(t))
                if (name.Equals(value.Trim(), StringComparison.OrdinalIgnoreCase))
                    return Enum.Parse(t, name);
            throw new FormatException("erlaubt: " + string.Join(", ", Enum.GetNames(t)));
        }

        // ------------------------------------------------------------------ saving

        /// <summary>Rewrites the ActiveLayout line in [General], keeping comments and everything else intact.</summary>
        public static void SaveActiveLayout(string path, string name)
        {
            var lines = new List<string>(File.ReadAllLines(path));
            int generalIdx = -1;
            string section = "";
            for (int i = 0; i < lines.Count; i++)
            {
                string t = lines[i].Trim();
                if (t.StartsWith("[") && t.EndsWith("]"))
                {
                    section = t.Substring(1, t.Length - 2).Trim();
                    if (section.Equals("General", StringComparison.OrdinalIgnoreCase))
                        generalIdx = i;
                    continue;
                }
                if (section.Equals("General", StringComparison.OrdinalIgnoreCase)
                    && t.StartsWith("ActiveLayout", StringComparison.OrdinalIgnoreCase) && t.Contains("="))
                {
                    lines[i] = "ActiveLayout=" + name;
                    File.WriteAllLines(path, lines, new UTF8Encoding(true));
                    return;
                }
            }
            if (generalIdx < 0)
            {
                lines.Insert(0, "[General]");
                generalIdx = 0;
            }
            lines.Insert(generalIdx + 1, "ActiveLayout=" + name);
            File.WriteAllLines(path, lines, new UTF8Encoding(true));
        }
    }
}
