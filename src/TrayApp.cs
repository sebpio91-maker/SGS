using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Windows.Forms;
using Microsoft.Win32;

namespace PokerGrid
{
    /// <summary>Hidden window that receives WM_HOTKEY messages.</summary>
    internal class HotkeyWindow : NativeWindow, IDisposable
    {
        private readonly List<int> ids = new List<int>();
        public event Action<int> HotkeyPressed;

        public HotkeyWindow()
        {
            CreateHandle(new CreateParams());
        }

        /// <summary>Registers e.g. "Ctrl+Alt+A". Returns an error text or null.</summary>
        public string Register(int id, string combo)
        {
            if (string.IsNullOrEmpty(combo) || combo.Trim().Length == 0)
                return null;
            uint mods = NativeMethods.MOD_NOREPEAT;
            Keys key = Keys.None;
            foreach (string raw in combo.Split('+'))
            {
                string part = raw.Trim();
                switch (part.ToLowerInvariant())
                {
                    case "ctrl": case "strg": case "control": mods |= NativeMethods.MOD_CONTROL; continue;
                    case "alt": mods |= NativeMethods.MOD_ALT; continue;
                    case "shift": mods |= NativeMethods.MOD_SHIFT; continue;
                    case "win": mods |= NativeMethods.MOD_WIN; continue;
                }
                if (part.Length == 1 && char.IsDigit(part[0]))
                    part = "D" + part;
                try
                {
                    key = (Keys)Enum.Parse(typeof(Keys), part, true);
                }
                catch (ArgumentException)
                {
                    return string.Format("Hotkey '{0}': unbekannte Taste '{1}'", combo, part);
                }
            }
            if (key == Keys.None)
                return string.Format("Hotkey '{0}': keine Taste angegeben", combo);
            if (!NativeMethods.RegisterHotKey(Handle, id, mods, (uint)key))
                return string.Format("Hotkey '{0}' ist bereits von einem anderen Programm belegt", combo);
            ids.Add(id);
            return null;
        }

        public void UnregisterAll()
        {
            foreach (int id in ids)
                NativeMethods.UnregisterHotKey(Handle, id);
            ids.Clear();
        }

        protected override void WndProc(ref Message m)
        {
            if (m.Msg == NativeMethods.WM_HOTKEY && HotkeyPressed != null)
                HotkeyPressed(m.WParam.ToInt32());
            base.WndProc(ref m);
        }

        public void Dispose()
        {
            UnregisterAll();
            DestroyHandle();
        }
    }

    internal class TrayApp : ApplicationContext
    {
        private const int HkArrange = 1, HkCompact = 2, HkPause = 3, HkNextLayout = 4, HkOverlay = 5;

        private readonly string configPath;
        private readonly GridManager manager;
        private readonly NotifyIcon tray;
        private readonly Timer timer;
        private readonly HotkeyWindow hotkeys;
        private readonly Icon iconActive, iconPaused;
        private readonly NativeMethods.WinEventDelegate winEventProc;   // field keeps the delegate alive
        private IntPtr winEventHook;
        private ToolStripMenuItem pauseItem, layoutMenu, autoLayoutItem;
        private OverlayForm overlay;
        private WindowListForm windowList;

        public TrayApp(string configPath)
        {
            this.configPath = configPath;

            AppConfig cfg;
            try
            {
                cfg = AppConfig.Load(configPath);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Konfiguration konnte nicht geladen werden:\n" + ex.Message, "PokerGrid",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                throw;
            }

            iconActive = CreateIcon(Color.FromArgb(46, 160, 67));
            iconPaused = CreateIcon(Color.Gray);

            manager = new GridManager(cfg);
            manager.StateChanged += delegate { UpdateTray(); };
            manager.MoveDenied += OnMoveDenied;

            tray = new NotifyIcon();
            tray.Icon = iconActive;
            tray.ContextMenuStrip = BuildMenu();
            tray.DoubleClick += delegate { ShowOverlay(); };
            tray.Visible = true;

            hotkeys = new HotkeyWindow();
            hotkeys.HotkeyPressed += OnHotkey;

            winEventProc = OnWinEvent;
            winEventHook = NativeMethods.SetWinEventHook(
                NativeMethods.EVENT_SYSTEM_MOVESIZESTART, NativeMethods.EVENT_SYSTEM_MOVESIZEEND,
                IntPtr.Zero, winEventProc, 0, 0,
                NativeMethods.WINEVENT_OUTOFCONTEXT | NativeMethods.WINEVENT_SKIPOWNPROCESS);

            timer = new Timer();
            timer.Tick += delegate { SafeRun(manager.Tick); };

            SystemEvents.DisplaySettingsChanged += OnDisplaySettingsChanged;

            ApplyRuntimeSettings(cfg);
            UpdateTray();
            tray.ShowBalloonTip(3000, "PokerGrid läuft",
                string.Format("Layout '{0}' mit {1} Slots. Rechtsklick auf das Symbol für das Menü.",
                    manager.Layout.Name, manager.Slots.Count), ToolTipIcon.Info);
        }

        // ------------------------------------------------------------------ setup

        private void ApplyRuntimeSettings(AppConfig cfg)
        {
            timer.Stop();
            timer.Interval = cfg.PollIntervalMs;
            timer.Start();

            hotkeys.UnregisterAll();
            var errors = new List<string>(cfg.Warnings);
            AddIfError(errors, hotkeys.Register(HkArrange, cfg.HotkeyArrange));
            AddIfError(errors, hotkeys.Register(HkCompact, cfg.HotkeyCompact));
            AddIfError(errors, hotkeys.Register(HkPause, cfg.HotkeyPause));
            AddIfError(errors, hotkeys.Register(HkNextLayout, cfg.HotkeyNextLayout));
            AddIfError(errors, hotkeys.Register(HkOverlay, cfg.HotkeyOverlay));

            RebuildLayoutMenu();

            if (errors.Count > 0)
                MessageBox.Show("Hinweise zur Konfiguration (" + configPath + "):\n\n" + string.Join("\n", errors),
                    "PokerGrid", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }

        private static void AddIfError(List<string> list, string error)
        {
            if (error != null)
                list.Add(error);
        }

        private ContextMenuStrip BuildMenu()
        {
            var menu = new ContextMenuStrip();
            menu.Items.Add("Jetzt anordnen", null, delegate { SafeRun(manager.ArrangeAll); });
            menu.Items.Add("Lücken schließen", null, delegate { SafeRun(manager.Compact); });
            pauseItem = new ToolStripMenuItem("Pausieren", null, delegate { TogglePause(); });
            menu.Items.Add(pauseItem);
            layoutMenu = new ToolStripMenuItem("Layout");
            menu.Items.Add(layoutMenu);
            menu.Items.Add("Slots anzeigen", null, delegate { ShowOverlay(); });
            menu.Items.Add("Fenster-Info …", null, delegate { ShowWindowList(); });
            menu.Items.Add(new ToolStripSeparator());
            menu.Items.Add("Konfiguration bearbeiten", null, delegate { EditConfig(); });
            menu.Items.Add("Konfiguration neu laden", null, delegate { ReloadConfig(); });
            menu.Items.Add(new ToolStripSeparator());
            menu.Items.Add("Beenden", null, delegate { ExitThread(); });
            return menu;
        }

        private void RebuildLayoutMenu()
        {
            layoutMenu.DropDownItems.Clear();
            if (manager.Config.AutoLayouts.Count > 0)
            {
                autoLayoutItem = new ToolStripMenuItem(
                    "Automatisch nach Tischanzahl (" + string.Join(" → ", manager.Config.AutoLayouts) + ")",
                    null, delegate { ToggleAutoLayout(); });
                layoutMenu.DropDownItems.Add(autoLayoutItem);
                layoutMenu.DropDownItems.Add(new ToolStripSeparator());
            }
            else
            {
                autoLayoutItem = null;
            }
            foreach (LayoutDef l in manager.Config.Layouts)
            {
                string name = l.Name;
                var item = new ToolStripMenuItem(name, null, delegate { SwitchLayout(name); });
                item.Tag = l;
                layoutMenu.DropDownItems.Add(item);
            }
            UpdateLayoutChecks();
        }

        private void UpdateLayoutChecks()
        {
            if (autoLayoutItem != null)
                autoLayoutItem.Checked = manager.AutoLayoutEnabled;
            foreach (ToolStripItem item in layoutMenu.DropDownItems)
            {
                var menuItem = item as ToolStripMenuItem;
                if (menuItem != null && menuItem.Tag is LayoutDef)
                    menuItem.Checked = menuItem.Tag == manager.Layout;
            }
        }

        private void ToggleAutoLayout()
        {
            manager.AutoLayoutEnabled = !manager.AutoLayoutEnabled;
            UpdateTray();
        }

        // ------------------------------------------------------------------ actions

        private void OnHotkey(int id)
        {
            switch (id)
            {
                case HkArrange: SafeRun(manager.ArrangeAll); break;
                case HkCompact: SafeRun(manager.Compact); break;
                case HkPause: TogglePause(); break;
                case HkNextLayout: SwitchLayout(manager.NextLayoutName()); break;
                case HkOverlay: ShowOverlay(); break;
            }
        }

        private void OnWinEvent(IntPtr hook, uint eventType, IntPtr hwnd, int idObject, int idChild, uint thread, uint time)
        {
            if (idObject != 0 || hwnd == IntPtr.Zero)   // 0 = OBJID_WINDOW
                return;
            if (eventType == NativeMethods.EVENT_SYSTEM_MOVESIZESTART)
                SafeRun(delegate { manager.OnMoveSizeStart(hwnd); });
            else if (eventType == NativeMethods.EVENT_SYSTEM_MOVESIZEEND)
                SafeRun(delegate { manager.OnMoveSizeEnd(hwnd); });
        }

        private void OnMoveDenied(string siteName)
        {
            tray.ShowBalloonTip(10000, "PokerGrid braucht Administratorrechte",
                siteName + " läuft als Administrator, deshalb blockiert Windows das Verschieben der Tische. " +
                "PokerGrid beenden und per Rechtsklick › Als Administrator ausführen starten.",
                ToolTipIcon.Warning);
        }

        private void OnDisplaySettingsChanged(object sender, EventArgs e)
        {
            SafeRun(manager.RefreshScreens);
        }

        private void TogglePause()
        {
            manager.Paused = !manager.Paused;
            if (!manager.Paused)
                SafeRun(manager.ArrangeAll);
            UpdateTray();
        }

        /// <summary>Manual switch (menu or hotkey); turns the automatic layout choice off.</summary>
        private void SwitchLayout(string name)
        {
            manager.AutoLayoutEnabled = false;
            SafeRun(delegate
            {
                manager.SetLayout(name);
                AppConfig.SaveActiveLayout(configPath, manager.Layout.Name);
            });
            UpdateTray();
            ShowOverlay();
        }

        private void ShowOverlay()
        {
            if (overlay != null && !overlay.IsDisposed)
                overlay.Close();
            overlay = new OverlayForm(manager.Slots, manager.SlotCounts(), manager.Layout.Name);
            overlay.Show();
        }

        private void ShowWindowList()
        {
            if (windowList == null || windowList.IsDisposed)
                windowList = new WindowListForm(manager);
            windowList.Show();
            windowList.Activate();
        }

        private void EditConfig()
        {
            try
            {
                Process.Start("notepad.exe", "\"" + configPath + "\"");
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "PokerGrid", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void ReloadConfig()
        {
            AppConfig cfg;
            try
            {
                cfg = AppConfig.Load(configPath);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Konfiguration konnte nicht geladen werden, die alte bleibt aktiv:\n" + ex.Message,
                    "PokerGrid", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            SafeRun(delegate { manager.ApplyConfig(cfg); });
            ApplyRuntimeSettings(cfg);
            UpdateTray();
            tray.ShowBalloonTip(2000, "PokerGrid", "Konfiguration neu geladen.", ToolTipIcon.Info);
        }

        private void UpdateTray()
        {
            pauseItem.Checked = manager.Paused;
            UpdateLayoutChecks();
            tray.Icon = manager.Paused ? iconPaused : iconActive;
            string text = string.Format("PokerGrid – {0}{1} – {2} Tische{3}",
                manager.Layout.Name, manager.AutoLayoutEnabled ? " (auto)" : "", manager.ManagedCount, manager.Paused ? " (Pause)" : "");
            tray.Text = text.Length > 63 ? text.Substring(0, 63) : text;
        }

        private void SafeRun(Action action)
        {
            try
            {
                action();
            }
            catch (Exception ex)
            {
                // Never let a single failure (e.g. a window closing mid-move) kill the tray app.
                Debug.WriteLine(ex);
            }
        }

        private static Icon CreateIcon(Color color)
        {
            using (var bmp = new Bitmap(32, 32))
            {
                using (Graphics g = Graphics.FromImage(bmp))
                using (var brush = new SolidBrush(color))
                {
                    g.Clear(Color.Transparent);
                    for (int r = 0; r < 2; r++)
                        for (int c = 0; c < 2; c++)
                            g.FillRectangle(brush, 2 + c * 15, 2 + r * 15, 13, 13);
                }
                IntPtr h = bmp.GetHicon();
                Icon icon = (Icon)Icon.FromHandle(h).Clone();
                NativeMethods.DestroyIcon(h);
                return icon;
            }
        }

        protected override void ExitThreadCore()
        {
            timer.Stop();
            SystemEvents.DisplaySettingsChanged -= OnDisplaySettingsChanged;
            if (winEventHook != IntPtr.Zero)
                NativeMethods.UnhookWinEvent(winEventHook);
            hotkeys.Dispose();
            tray.Visible = false;
            tray.Dispose();
            base.ExitThreadCore();
        }
    }
}
