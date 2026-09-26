using System;
using System.Drawing;
using System.Globalization;
using System.Text;
using System.Text.RegularExpressions;
using System.Windows.Forms;

namespace PokerGrid
{
    /// <summary>
    /// Lists all visible windows with process, class and title so the user can find out
    /// how to recognise the tables of a poker client, and copies a [Site:...] template.
    /// </summary>
    internal class WindowListForm : Form
    {
        private readonly GridManager manager;
        private readonly ListView list;
        private readonly CheckBox showUntitled;

        public WindowListForm(GridManager manager)
        {
            this.manager = manager;

            Text = "PokerGrid – Fenster-Info";
            Width = 1000;
            Height = 520;
            StartPosition = FormStartPosition.CenterScreen;

            list = new ListView();
            list.Dock = DockStyle.Fill;
            list.View = View.Details;
            list.FullRowSelect = true;
            list.GridLines = true;
            list.HideSelection = false;
            list.Columns.Add("Prozess", 140);
            list.Columns.Add("Klasse", 200);
            list.Columns.Add("Titel", 300);
            list.Columns.Add("Größe", 90);
            list.Columns.Add("Verhältnis", 75);
            list.Columns.Add("Erkannt als", 170);

            var panel = new FlowLayoutPanel();
            panel.Dock = DockStyle.Bottom;
            panel.Height = 40;
            panel.Padding = new Padding(6);

            var refresh = new Button();
            refresh.Text = "Aktualisieren";
            refresh.AutoSize = true;
            refresh.Click += delegate { Reload(); };

            var copyTemplate = new Button();
            copyTemplate.Text = "Als Site-Vorlage kopieren";
            copyTemplate.AutoSize = true;
            copyTemplate.Click += delegate { CopyTemplate(); };

            var copyRows = new Button();
            copyRows.Text = "Zeilen kopieren";
            copyRows.AutoSize = true;
            copyRows.Click += delegate { CopyRows(); };

            showUntitled = new CheckBox();
            showUntitled.Text = "Fenster ohne Titel anzeigen";
            showUntitled.AutoSize = true;
            showUntitled.Padding = new Padding(10, 5, 0, 0);
            showUntitled.CheckedChanged += delegate { Reload(); };

            panel.Controls.Add(refresh);
            panel.Controls.Add(copyTemplate);
            panel.Controls.Add(copyRows);
            panel.Controls.Add(showUntitled);

            var hint = new Label();
            hint.Dock = DockStyle.Top;
            hint.Height = 36;
            hint.Padding = new Padding(6, 4, 6, 0);
            hint.Text = "Öffne einen Pokertisch, klicke auf „Aktualisieren“, wähle die Zeile des Tisches und kopiere die Vorlage " +
                        "in die Konfiguration (Tray-Menü › Konfiguration bearbeiten). Danach „Konfiguration neu laden“.";

            Controls.Add(list);
            Controls.Add(panel);
            Controls.Add(hint);

            Reload();
        }

        private void Reload()
        {
            list.BeginUpdate();
            list.Items.Clear();
            foreach (WinInfo w in WindowScanner.Scan())
            {
                if (!showUntitled.Checked && w.Title.Length == 0)
                    continue;
                string ratio = w.Minimized || w.Bounds.Height == 0 ? "-"
                    : ((double)w.Bounds.Width / w.Bounds.Height).ToString("0.000", CultureInfo.InvariantCulture);
                string size = w.Minimized ? "minimiert" : w.Bounds.Width + "x" + w.Bounds.Height;
                var item = new ListViewItem(new[] { w.Process, w.ClassName, w.Title, size, ratio, manager.DescribeWindow(w.Hwnd) });
                item.Tag = w;
                if (item.SubItems[5].Text.Length > 0)
                    item.BackColor = Color.FromArgb(220, 245, 220);
                list.Items.Add(item);
            }
            list.EndUpdate();
        }

        private void CopyTemplate()
        {
            if (list.SelectedItems.Count == 0)
            {
                MessageBox.Show("Bitte zuerst einen Tisch in der Liste auswählen.", Text);
                return;
            }
            var w = (WinInfo)list.SelectedItems[0].Tag;
            string name = w.Process.EndsWith(".exe", StringComparison.OrdinalIgnoreCase)
                ? w.Process.Substring(0, w.Process.Length - 4) : w.Process;

            var sb = new StringBuilder();
            sb.AppendLine("[Site:" + name + "]");
            sb.AppendLine("Process=" + w.Process);
            sb.AppendLine("Class=^" + Regex.Escape(w.ClassName) + "$");
            sb.AppendLine("; Falls Lobby und Tische dieselbe Klasse haben, über den Titel unterscheiden:");
            sb.AppendLine("TitleRegex=");
            sb.AppendLine("ExcludeTitleRegex=Lobby");
            sb.AppendLine("AspectRatio=auto");
            Clipboard.SetText(sb.ToString());
            MessageBox.Show("Vorlage in die Zwischenablage kopiert:\n\n" + sb, Text);
        }

        private void CopyRows()
        {
            var sb = new StringBuilder();
            foreach (ListViewItem item in list.SelectedItems.Count > 0 ? (System.Collections.IEnumerable)list.SelectedItems : list.Items)
            {
                var cells = new string[item.SubItems.Count];
                for (int i = 0; i < cells.Length; i++)
                    cells[i] = item.SubItems[i].Text;
                sb.AppendLine(string.Join("\t", cells));
            }
            if (sb.Length > 0)
                Clipboard.SetText(sb.ToString());
        }
    }
}
