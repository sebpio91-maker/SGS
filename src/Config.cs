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

    internal enum AlignMode { Center, TopLeft, Top, Left }

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
        public List<SlotSpec> Slots = new List<SlotSpec>();

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

            Rectangle a = MonitorArea(Monitor, UseWorkingArea);
            a.Inflate(-Margin, -Margin);
            int cols = Math.Max(1, Columns), rows = Math.Max(1, Rows);
            int cellW = (a.Width - Gap * (cols - 1)) / cols;
            int cellH = (a.Height - Gap * (rows - 1)) / rows;

            if (ColumnFirst)
            {
                for (int c = 0; c < cols; c++)
                    for (int r = 0; r < rows; r++)
                        result.Add(new Rectangle(a.X + c * (cellW + Gap), a.Y + r * (cellH + Gap), cellW, cellH));
            }
            else
            {
                for (int r = 0; r < rows; r++)
                    for (int c = 0; c < cols; c++)
                        result.Add(new Rectangle(a.X + c * (cellW + Gap), a.Y + r * (cellH + Gap), cellW, cellH));
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
