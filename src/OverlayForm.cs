using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace PokerGrid
{
    /// <summary>Click-through, always-on-top overlay that shows the slots of the active layout for a few seconds.</summary>
    internal class OverlayForm : Form
    {
        private readonly List<Rectangle> slots;
        private readonly int[] counts;
        private readonly string layoutName;
        private readonly Timer closeTimer;

        public OverlayForm(IList<Rectangle> slots, int[] counts, string layoutName)
        {
            this.slots = new List<Rectangle>(slots);
            this.counts = counts;
            this.layoutName = layoutName;

            FormBorderStyle = FormBorderStyle.None;
            ShowInTaskbar = false;
            TopMost = true;
            StartPosition = FormStartPosition.Manual;
            AutoScaleMode = AutoScaleMode.None;
            BackColor = Color.Magenta;
            TransparencyKey = Color.Magenta;
            Bounds = SystemInformation.VirtualScreen;
            DoubleBuffered = true;

            closeTimer = new Timer();
            closeTimer.Interval = 3000;
            closeTimer.Tick += delegate { Close(); };
            closeTimer.Start();
        }

        protected override bool ShowWithoutActivation
        {
            get { return true; }
        }

        protected override CreateParams CreateParams
        {
            get
            {
                CreateParams cp = base.CreateParams;
                cp.ExStyle |= NativeMethods.WS_EX_TRANSPARENT | NativeMethods.WS_EX_LAYERED
                    | NativeMethods.WS_EX_TOOLWINDOW | NativeMethods.WS_EX_NOACTIVATE;
                return cp;
            }
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            Graphics g = e.Graphics;
            // No anti-aliasing: blended edge pixels would not match the transparency key and show up pink.
            g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.SingleBitPerPixelGridFit;
            Rectangle vs = SystemInformation.VirtualScreen;
            using (var pen = new Pen(Color.Lime, 4))
            using (var font = new Font("Segoe UI", 28, FontStyle.Bold))
            using (var small = new Font("Segoe UI", 12, FontStyle.Bold))
            using (var textBrush = new SolidBrush(Color.Lime))
            using (var shadow = new SolidBrush(Color.Black))
            {
                for (int i = 0; i < slots.Count; i++)
                {
                    Rectangle r = slots[i];
                    r.Offset(-vs.X, -vs.Y);
                    r.Inflate(-2, -2);
                    g.DrawRectangle(pen, r);

                    string label = (i + 1).ToString();
                    if (i < counts.Length && counts[i] > 1)
                        label += " (" + counts[i] + ")";
                    DrawShadowed(g, label, font, textBrush, shadow, r.X + 10, r.Y + 6);
                    if (i == 0)
                        DrawShadowed(g, "Layout: " + layoutName, small, textBrush, shadow, r.X + 12, r.Y + 56);
                }
            }
        }

        private static void DrawShadowed(Graphics g, string text, Font font, Brush brush, Brush shadow, int x, int y)
        {
            g.DrawString(text, font, shadow, x + 2, y + 2);
            g.DrawString(text, font, brush, x, y);
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
                closeTimer.Dispose();
            base.Dispose(disposing);
        }
    }
}
