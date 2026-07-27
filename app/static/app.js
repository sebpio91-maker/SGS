(function () {
  const normId = window.NORM_ID;
  const tbody = document.getElementById("pruefpunkte-body");
  const status = document.getElementById("speicherstatus");
  const relevanzOptionenHtml = document.getElementById("relevanz-optionen-template").innerHTML;

  function zeigeStatus(text, klasse) {
    status.textContent = text;
    status.className = klasse || "";
    if (text) {
      setTimeout(() => {
        if (status.textContent === text) status.textContent = "";
      }, 1500);
    }
  }

  function baueZeile(p) {
    const tr = document.createElement("tr");
    tr.dataset.id = p.id;

    const tdKapitel = document.createElement("td");
    const inputKapitel = document.createElement("input");
    inputKapitel.type = "text";
    inputKapitel.value = p.kapitel || "";
    inputKapitel.dataset.field = "kapitel";
    tdKapitel.appendChild(inputKapitel);

    const tdUeberschrift = document.createElement("td");
    const inputUeberschrift = document.createElement("input");
    inputUeberschrift.type = "text";
    inputUeberschrift.value = p.ueberschrift || "";
    inputUeberschrift.dataset.field = "ueberschrift";
    tdUeberschrift.appendChild(inputUeberschrift);

    const tdRelevanz = document.createElement("td");
    const select = document.createElement("select");
    select.dataset.field = "pruefungsrelevant";
    select.innerHTML = relevanzOptionenHtml;
    select.value = p.pruefungsrelevant || "Nein";
    tdRelevanz.appendChild(select);

    const tdInhalt = document.createElement("td");
    const textarea = document.createElement("textarea");
    textarea.value = p.inhalt || "";
    textarea.dataset.field = "inhalt";
    tdInhalt.appendChild(textarea);

    const tdAktionen = document.createElement("td");
    tdAktionen.className = "zeile-aktionen";
    tdAktionen.innerHTML =
      '<button type="button" data-action="hoch" title="Nach oben">↑</button>' +
      '<button type="button" data-action="runter" title="Nach unten">↓</button>' +
      '<button type="button" data-action="loeschen" title="Löschen">🗑</button>';

    tr.append(tdKapitel, tdUeberschrift, tdRelevanz, tdInhalt, tdAktionen);
    return tr;
  }

  async function ladeTabelle() {
    const res = await fetch(`/api/normen/${normId}/pruefpunkte`);
    const daten = await res.json();
    tbody.innerHTML = "";
    daten.forEach((p) => tbody.appendChild(baueZeile(p)));
  }

  async function speichereFeld(id, feld, wert) {
    try {
      const res = await fetch(`/api/pruefpunkte/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ [feld]: wert }),
      });
      if (!res.ok) throw new Error("Serverfehler");
      zeigeStatus("Gespeichert ✓", "ok");
    } catch (e) {
      zeigeStatus("Fehler beim Speichern", "fehler");
    }
  }

  tbody.addEventListener(
    "blur",
    (ev) => {
      const el = ev.target;
      if (!el.dataset || !el.dataset.field) return;
      const tr = el.closest("tr");
      speichereFeld(tr.dataset.id, el.dataset.field, el.value);
    },
    true
  );

  tbody.addEventListener("change", (ev) => {
    const el = ev.target;
    if (el.tagName === "SELECT" && el.dataset.field) {
      const tr = el.closest("tr");
      speichereFeld(tr.dataset.id, el.dataset.field, el.value);
    }
  });

  tbody.addEventListener("click", async (ev) => {
    const btn = ev.target.closest("button[data-action]");
    if (!btn) return;
    const tr = btn.closest("tr");
    const id = tr.dataset.id;
    const aktion = btn.dataset.action;

    if (aktion === "loeschen") {
      if (!confirm("Diese Zeile wirklich löschen?")) return;
      await fetch(`/api/pruefpunkte/${id}`, { method: "DELETE" });
      tr.remove();
    } else if (aktion === "hoch" || aktion === "runter") {
      await fetch(`/api/pruefpunkte/${id}/verschieben`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ richtung: aktion }),
      });
      await ladeTabelle();
    }
  });

  document.getElementById("zeile-hinzufuegen").addEventListener("click", async () => {
    const res = await fetch(`/api/normen/${normId}/pruefpunkte`, { method: "POST" });
    const neu = await res.json();
    tbody.appendChild(baueZeile(neu));
  });

  ladeTabelle();
})();
