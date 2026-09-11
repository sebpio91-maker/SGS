"""Liest die Stammdaten aus der Anwendung aus.

Ohne Argument gelten die in KV-Monitoring.html eingebauten Startdaten; mit dem
Pfad zu einem JSON-Export der Anwendung wird dieser vorher in den Browser-Speicher
gelegt, sodass die Anwendung ihn wie einen echten Datenbestand lädt - samt aller
Migrationen, die sie beim Start darauf anwendet."""
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright
DATEI = (pathlib.Path(__file__).resolve().parent.parent / "KV-Monitoring.html").as_uri()

JS = r"""() => {
  const blocks = [
    { feld: "normen",      label: "Sicherheit-/Normprüfung" },
    { feld: "ffuNormen",   label: "FFU/Fitting" },
    { feld: "stiwaNormen", label: "NGO / StiWa" }
  ];
  const normById = (id) => data.normen.find(n => n.id === id) || null;

  /* Wie oft eine Norm in Prüfgrundlagen referenziert ist - fürs Aufräumen sichtbar machen. */
  const verwendung = {};
  data.pruefgrundlagen.forEach(e => blocks.forEach(b => (e[b.feld] || []).forEach(r => {
    verwendung[r.normId] = (verwendung[r.normId] || 0) + 1;
  })));

  const normen = data.normen.map(n => ({
    bezeichnung: n.bezeichnung || "",
    titel: n.titel || "",
    typ: normTypLabel(n.typ),
    pruefungsart: n.pruefungsart || "",
    sapCode: n.sapCode || "",
    kosten: (n.kosten === null || n.kosten === undefined || n.kosten === "") ? null : Number(n.kosten),
    kennzeichnung: !!n.kennzeichnung,
    bedienungsanleitung: !!n.bedienungsanleitung,
    lidlBlock: n.lidlSpezifischBlock || "",
    anzahlAnwendungsbereiche: (n.anwendungsbereiche || []).length,
    anwendungsbereiche: (n.anwendungsbereiche || []).map(b => b.name).join(" | "),
    bemerkung: n.bemerkung || "",
    dateiname: n.dateiname || "",
    hochgeladenAm: n.hochgeladenAm || "",
    volltextVorhanden: !!(n.rohtext && String(n.rohtext).trim()),
    verwendungen: verwendung[n.id] || 0,
    id: n.id
  }));

  const bereiche = [];
  data.normen.forEach(n => (n.anwendungsbereiche || []).forEach(b => bereiche.push({
    norm: n.bezeichnung || "", normTitel: n.titel || "",
    pruefungsart: n.pruefungsart || "",
    name: b.name || "", text: b.text || "",
    preis: (b.preis === null || b.preis === undefined || b.preis === "") ? null : Number(b.preis)
  })));

  const grundlagen = [], positionen = [];
  data.pruefgrundlagen.forEach(e => {
    grundlagen.push({
      id: e.id,
      bereich: e.bereich || "",
      warengruppeCode: e.warengruppeCode || "",
      warengruppeName: e.warengruppeName || "",
      produkt: e.produkt || "",
      trivial: !!e.trivial,
      anzahlMuster: (e.anzahlMuster === null || e.anzahlMuster === undefined) ? "" : e.anzahlMuster,
      bearbeitungsdauerTage: (e.bearbeitungsdauerTage === null || e.bearbeitungsdauerTage === undefined || e.bearbeitungsdauerTage === "") ? null : Number(e.bearbeitungsdauerTage),
      kennzeichnung: pruefgrundlageKennzeichnungAktiv(e),
      bedienungsanleitung: pruefgrundlageBedienungsanleitungAktiv(e),
      normenText: normRefListeText(e.normen),
      normenSumme: normenBlockSumme(e.normen),
      normenKommentar: e.normenKommentar || "",
      normenBemerkungen: normRefBemerkungenText(e.normen),
      ffuText: normRefListeText(e.ffuNormen),
      ffuSumme: normenBlockSumme(e.ffuNormen),
      ffuKommentar: e.ffuNormenKommentar || "",
      stiwaText: normRefListeText(e.stiwaNormen),
      stiwaSumme: normenBlockSumme(e.stiwaNormen),
      stiwaKommentar: e.stiwaNormenKommentar || "",
      kostenTp: (e.kostenTp === null || e.kostenTp === undefined || e.kostenTp === "") ? null : Number(e.kostenTp),
      kostenAlt: (e.kostenSicherheitNormAlt === null || e.kostenSicherheitNormAlt === undefined || e.kostenSicherheitNormAlt === "") ? null : Number(e.kostenSicherheitNormAlt)
    });
    blocks.forEach(b => (e[b.feld] || []).forEach(r => {
      const n = normById(r.normId);
      const ab = n && r.anwendungsbereichId ? (n.anwendungsbereiche || []).find(x => x.id === r.anwendungsbereichId) : null;
      positionen.push({
        pgId: e.id,
        bereich: e.bereich || "",
        warengruppeName: e.warengruppeName || "",
        produkt: e.produkt || "",
        block: b.label,
        norm: n ? (n.bezeichnung || "") : "(gelöschte Norm)",
        normTitel: n ? (n.titel || "") : "",
        inAnlehnungAn: !!r.inAnlehnungAn,
        anwendungsbereich: ab ? (ab.name || "") : "",
        pruefungsart: n ? (n.pruefungsart || "") : "",
        sapCode: n ? (n.sapCode || "") : "",
        kosten: (r.kosten === null || r.kosten === undefined || r.kosten === "") ? null : Number(r.kosten),
        kostenWeiteresProdukt: (r.kostenWeiteresProdukt === null || r.kostenWeiteresProdukt === undefined || r.kostenWeiteresProdukt === "") ? null : Number(r.kostenWeiteresProdukt),
        kennzeichnung: normRefKennzeichnungAktiv(r),
        bedienungsanleitung: normRefBedienungsanleitungAktiv(r),
        bemerkung: n ? (n.bemerkung || "") : ""
      });
    }));
  });

  const mak = data.mak.map(m => ({
    id: m.id, sapCode: m.sapCode || "", kategorie: m.kategorie || "", bereich: m.bereich || "",
    parameter: m.parameter || "", anforderung: m.anforderung || "",
    normEu: m.normEu || "", normUs: m.normUs || "", pruefnachweis: m.pruefnachweis || "",
    kosten: (m.kosten === null || m.kosten === undefined || m.kosten === "") ? null : Number(m.kosten),
    kostenWeiteresArtikel: (m.kostenWeiteresArtikel === null || m.kostenWeiteresArtikel === undefined || m.kostenWeiteresArtikel === "") ? null : Number(m.kostenWeiteresArtikel),
    abrechnungsmodus: m.abrechnungsmodus || "",
    bewertungsgrundlageErforderlich: !!m.bewertungsgrundlageErforderlich,
    varianten: (m.varianten || []).map(v => v.name || v).join(" | "),
    bemerkung: m.bemerkung || "",
    schlagworte: (m.schlagworte || []).join(", ")
  }));

  return { normen, bereiche, grundlagen, positionen, mak,
           pruefungsarten: data.pruefungsarten, bereichsliste: data.bereiche };
}"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox"])
        page = await b.new_page()
        page.on("pageerror", lambda e: print("PAGEERROR:", e))
        if len(sys.argv) > 1:
            bestand = json.load(open(sys.argv[1], encoding="utf-8"))
            await page.add_init_script(
                "localStorage.setItem('kv_monitoring_v3', %s);" % json.dumps(json.dumps(bestand)))
            print("Datenbestand:", sys.argv[1])
        await page.goto(DATEI); await page.wait_for_timeout(3000)
        d = await page.evaluate(JS)
        d["stand"] = bestand.get("exportiertAm", "") if len(sys.argv) > 1 else ""
        d["quelle"] = pathlib.Path(sys.argv[1]).name if len(sys.argv) > 1 else "Startdaten aus KV-Monitoring.html"
        json.dump(d, open(pathlib.Path(__file__).parent / "export.json","w",encoding="utf-8"), ensure_ascii=False)
        for k, v in d.items():
            print(k, len(v) if isinstance(v, list) else repr(v))
        await b.close()
asyncio.run(main())
