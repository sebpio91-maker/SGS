using System;
using System.IO;
using System.Threading;
using System.Windows.Forms;

namespace PokerGrid
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            EnableDpiAwareness();

            bool created;
            using (var mutex = new Mutex(true, "PokerGrid_SingleInstance_5B1E", out created))
            {
                if (!created)
                {
                    MessageBox.Show("PokerGrid läuft bereits (Symbol im Infobereich der Taskleiste).", "PokerGrid");
                    return;
                }

                Application.EnableVisualStyles();
                Application.SetCompatibleTextRenderingDefault(false);
                string configPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "PokerGrid.ini");
                Application.Run(new TrayApp(configPath));
            }
        }

        /// <summary>
        /// Work in physical pixels on every monitor. Without this, Windows would scale our
        /// coordinates on high-DPI screens and tables would land in the wrong place.
        /// </summary>
        private static void EnableDpiAwareness()
        {
            try
            {
                // DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 (Windows 10 1703+)
                if (NativeMethods.SetProcessDpiAwarenessContext(new IntPtr(-4)))
                    return;
            }
            catch (EntryPointNotFoundException) { }
            NativeMethods.SetProcessDPIAware();
        }
    }
}
