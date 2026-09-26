using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Text;

namespace PokerGrid
{
    /// <summary>Snapshot of one top-level window.</summary>
    internal class WinInfo
    {
        public IntPtr Hwnd;
        public string Title;
        public string ClassName;
        public string Process;
        public uint Pid;
        public Rectangle Bounds;   // visible bounds (without invisible Win10 resize borders)
        public bool Minimized;
        public bool Maximized;
    }

    internal static class WindowScanner
    {
        private static Dictionary<uint, string> processCache = new Dictionary<uint, string>();

        /// <summary>Returns all visible, non-cloaked top-level windows.</summary>
        public static List<WinInfo> Scan()
        {
            var result = new List<WinInfo>();
            var usedCache = new Dictionary<uint, string>();

            NativeMethods.EnumWindows(delegate(IntPtr h, IntPtr l)
            {
                if (!NativeMethods.IsWindowVisible(h) || IsCloaked(h))
                    return true;
                WinInfo w = Describe(h, usedCache);
                if (w != null)
                    result.Add(w);
                return true;
            }, IntPtr.Zero);

            // Only keep cache entries for processes that still own windows (PIDs get reused).
            processCache = usedCache;
            return result;
        }

        private static WinInfo Describe(IntPtr h, Dictionary<uint, string> usedCache)
        {
            var w = new WinInfo();
            w.Hwnd = h;

            int len = NativeMethods.GetWindowTextLength(h);
            var sb = new StringBuilder(Math.Max(len + 1, 2));
            NativeMethods.GetWindowText(h, sb, sb.Capacity);
            w.Title = sb.ToString();

            var cls = new StringBuilder(256);
            NativeMethods.GetClassName(h, cls, cls.Capacity);
            w.ClassName = cls.ToString();

            uint pid;
            NativeMethods.GetWindowThreadProcessId(h, out pid);
            w.Pid = pid;
            string name;
            if (!processCache.TryGetValue(pid, out name) && !usedCache.TryGetValue(pid, out name))
                name = GetProcessName(pid);
            usedCache[pid] = name;
            w.Process = name;

            w.Minimized = NativeMethods.IsIconic(h);
            w.Maximized = NativeMethods.IsZoomed(h);
            w.Bounds = GetVisibleBounds(h);
            return w;
        }

        private static string GetProcessName(uint pid)
        {
            try
            {
                using (Process p = Process.GetProcessById((int)pid))
                    return p.ProcessName + ".exe";
            }
            catch
            {
                return "?";
            }
        }

        private static bool IsCloaked(IntPtr h)
        {
            int cloaked;
            try
            {
                if (NativeMethods.DwmGetWindowAttribute(h, NativeMethods.DWMWA_CLOAKED, out cloaked, 4) == 0)
                    return cloaked != 0;
            }
            catch (DllNotFoundException) { }
            return false;
        }

        private static Rectangle ToRectangle(NativeMethods.RECT r)
        {
            return Rectangle.FromLTRB(r.Left, r.Top, r.Right, r.Bottom);
        }

        /// <summary>
        /// The rectangle the user actually sees. On Windows 10, GetWindowRect includes
        /// invisible resize borders (~7px), DWM's extended frame bounds do not.
        /// </summary>
        public static Rectangle GetVisibleBounds(IntPtr h)
        {
            NativeMethods.RECT r;
            try
            {
                if (NativeMethods.DwmGetWindowAttribute(h, NativeMethods.DWMWA_EXTENDED_FRAME_BOUNDS, out r,
                        Marshal.SizeOf(typeof(NativeMethods.RECT))) == 0)
                    return ToRectangle(r);
            }
            catch (DllNotFoundException) { }
            NativeMethods.GetWindowRect(h, out r);
            return ToRectangle(r);
        }

        private const int ERROR_ACCESS_DENIED = 5;

        /// <summary>
        /// Set by SetVisibleBounds when Windows refused the move. That happens when the target
        /// window belongs to a process running as administrator and PokerGrid does not.
        /// </summary>
        public static bool LastMoveDenied;

        /// <summary>Moves/resizes a window so that its visible part matches target. Returns the resulting visible bounds.</summary>
        public static Rectangle SetVisibleBounds(IntPtr h, Rectangle target)
        {
            Rectangle result = Rectangle.Empty;
            LastMoveDenied = false;
            // A second pass handles windows that change their border size after being moved
            // to a monitor with a different DPI.
            for (int pass = 0; pass < 2; pass++)
            {
                NativeMethods.RECT wr;
                NativeMethods.GetWindowRect(h, out wr);
                Rectangle vis = GetVisibleBounds(h);
                int left = Clamp(vis.Left - wr.Left), top = Clamp(vis.Top - wr.Top);
                int right = Clamp(wr.Right - vis.Right), bottom = Clamp(wr.Bottom - vis.Bottom);

                if (!NativeMethods.SetWindowPos(h, IntPtr.Zero,
                        target.X - left, target.Y - top,
                        target.Width + left + right, target.Height + top + bottom,
                        NativeMethods.SWP_NOZORDER | NativeMethods.SWP_NOACTIVATE | NativeMethods.SWP_NOOWNERZORDER)
                    && Marshal.GetLastWin32Error() == ERROR_ACCESS_DENIED)
                {
                    LastMoveDenied = true;
                    return GetVisibleBounds(h);
                }

                result = GetVisibleBounds(h);
                if (IsNear(result, target, 1))
                    break;
            }
            return result;
        }

        private static int Clamp(int border)
        {
            return border < 0 || border > 40 ? 0 : border;
        }

        public static bool IsNear(Rectangle a, Rectangle b, int tolerance)
        {
            return Math.Abs(a.X - b.X) <= tolerance && Math.Abs(a.Y - b.Y) <= tolerance
                && Math.Abs(a.Width - b.Width) <= tolerance && Math.Abs(a.Height - b.Height) <= tolerance;
        }
    }
}
