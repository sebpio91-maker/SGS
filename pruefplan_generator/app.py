import tempfile
from pathlib import Path

import streamlit as st

from src import matcher, suggest, excel_export, pdf_export
from src.db import get_connection, init_schema
from src.models import PruefplanErgebnis, PruefplanPosition
from src.pdf_parser import parse_pruefauftrag

st.set_page_config(page_title="Prüfplan-Generator", layout="wide")
st.title("Automatische Prüfplan-Erstellung")

uploaded = st.file_uploader("Prüfauftrag-PDF hochladen", type=["pdf"])

if uploaded is None:
    st.info("Bitte einen Prüfauftrag (PDF) hochladen, um zu starten.")
    st.stop()

_AUSWAHL_PREFIXE = ("mech_", "ps_", "normen_", "eig_", "std_")

cache_key = uploaded.file_id  # jede Interaktion mit dem Uploader bekommt eine neue ID,
# auch bei erneutem Hochladen derselben Datei -- zuverlässiger als name+size als Trigger.
if st.session_state.get("_cache_key") != cache_key:
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(uploaded.getvalue())
        tmp_path = Path(tmp.name)
    st.session_state["artikel"] = parse_pruefauftrag(tmp_path)
    st.session_state["_cache_key"] = cache_key
    tmp_path.unlink(missing_ok=True)
    # Auswahl-Häkchen/Dropdowns aus vorherigem Prüfauftrag nicht ins neue Dokument übernehmen.
    for key in list(st.session_state.keys()):
        if key.startswith(_AUSWAHL_PREFIXE):
            del st.session_state[key]

artikel = st.session_state["artikel"]

st.subheader("Extrahierte Artikeldaten")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**IAN / Charge:** {artikel.ian_charge}")
    st.write(f"**Artikelbezeichnung:** {artikel.artikelbezeichnung}")
    st.write(f"**Artikelkategorie:** {artikel.artikelkategorie}")
    st.write(f"**Warenbereich:** {artikel.warenbereich}")
    st.write(f"**Warengruppe:** {artikel.warengruppe} (Code: {artikel.warengruppe_code})")
with col2:
    st.write(f"**Lieferant:** {artikel.lieferant}")
    st.write(f"**Herkunftsland:** {artikel.herkunftsland}")
    st.write(f"**Produktklassifizierung:** {artikel.produktklassifizierung}")
    st.write(f"**Batterietyp:** {artikel.batterietyp}")
    st.write(f"**Zertifizierungen:** {artikel.zertifizierungen}")
    st.write(f"**Prüfumfang lt. Auftrag:** {', '.join(artikel.pruefumfang) or '-'}")

# Die PSI-Phase (Verpackung/Transportverpackung, On-Site Testing, ...) betrifft
# Produktions-/Versandprüfung, nicht Mechanik/Produktspezifikation -- hier raus.
relevante_pruefumfang_komponenten = {
    phase: komponenten
    for phase, komponenten in artikel.pruefumfang_komponenten.items()
    if "psi" not in phase.lower()
}

if relevante_pruefumfang_komponenten:
    with st.expander("Prüfumfang-Bestandteile je Phase (aus 'bestehend aus ...')", expanded=True):
        for phase, komponenten in relevante_pruefumfang_komponenten.items():
            st.write(f"**{phase}:**")
            for k in komponenten:
                st.write(f"- {k}")

with st.expander("Weitere Details (Material, Farbe, Zielländer, ...)"):
    st.text(f"Qualität / Auslobungen:\n{artikel.qualitaet or '-'}")
    st.text(f"Material:\n{artikel.material or '-'}")
    st.text(f"Materialstärke:\n{artikel.materialstaerke or '-'}")
    st.text(f"Farbe:\n{artikel.farbe or '-'}")
    st.write(f"Zielländer: {', '.join(artikel.laender) or '-'}")

conn = get_connection()
init_schema(conn)

st.subheader("Prüfumfang bestimmen")

kategorie_umfang, kategorie_hinweis = suggest.pruefumfang_nach_artikelkategorie(artikel.artikelkategorie)
artikel_ist_trivial = suggest.ist_trivialer_artikel(artikel.artikelkategorie)
if artikel_ist_trivial:
    st.warning(
        f"{kategorie_hinweis}. Normangaben unten sind Vollprüfungen (100%) — Mechanik-Positionen "
        "sind daher standardmäßig abgewählt, können aber bei Bedarf trotzdem ausgewählt werden."
    )
else:
    st.info(f"{kategorie_hinweis}. Normangaben unten sind Vollprüfungen (100%).")

mechanik_kandidaten = matcher.find_mechanik(conn, artikel.warengruppe_code)
positionen: list[PruefplanPosition] = []

if mechanik_kandidaten:
    st.success(
        f"{len(mechanik_kandidaten)} Regel(n) für Warengruppe {artikel.warengruppe} "
        "in der Mechanik-Datenbank gefunden."
    )
    bewertet = suggest.rank_kandidaten(
        mechanik_kandidaten, "produkt", artikel.artikelbezeichnung, artikel.produktklassifizierung
    )
    max_score = bewertet[0][1] if bewertet else 0.0
    st.caption(
        "Vorschlag basiert auf Textabgleich zwischen Artikelbezeichnung/Produktklassifizierung "
        "und den hinterlegten Produktnamen. Bitte prüfen und ggf. korrigieren."
    )

    ausgewaehlt = []
    for k, score in bewertet:
        default = (score == max_score and score > 0) and not artikel_ist_trivial
        label = f"**{k.produkt}** — {k.norm_ek_ppm or 'keine Norm hinterlegt'} (Score {score:.2f})"
        checked = st.checkbox(label, value=default, key=f"mech_{k.id}")
        if k.norm_ek_ppm:
            st.caption(f"Vollprüfung lt. Norm — {kategorie_hinweis}")
        with st.expander("Details", expanded=False):
            st.write(f"Bemerkungen: {k.bemerkungen or '-'}")
            st.write(f"Anzahl Muster: {k.anzahl_muster or '-'}")
            st.write(f"Kosten VP: {k.kosten_vp if k.kosten_vp is not None else '-'}")
            st.write(f"Trivial: {k.trivial or '-'}")
            st.write(f"KEZ Anforderungen: {k.kez_anforderungen or '-'}")
        if checked:
            ausgewaehlt.append(k)

    for i, k in enumerate(ausgewaehlt):
        setbestandteil = "Hauptprodukt" if i == 0 else f"Teilprodukt {i}"
        umfang_zusatz = f"Vollprüfung; {kategorie_hinweis}"
        bemerkung = f"{k.bemerkungen} — {umfang_zusatz}" if k.bemerkungen else umfang_zusatz
        positionen.append(
            PruefplanPosition(
                setbestandteil=setbestandteil,
                produkt=k.produkt,
                pruefung=k.norm_ek_ppm,
                anzahl=k.anzahl_muster,
                kosten=k.kosten_vp,
                bemerkung=bemerkung,
                quelle="mechanik",
            )
        )
else:
    st.warning(
        "Keine Mechanik-Regel für diese Warengruppe hinterlegt. "
        "Fallback: manuelle Normenauswahl (aktuell nur Möbel/Spielzeug abgedeckt)."
    )

    felder = ["kategorie", "produktart", "zielgruppe", "einsatzort", "bereich", "produkt"]
    labels = ["Kategorie", "Produktart", "Zielgruppe", "Einsatzort", "Bereich", "Produkt"]
    kriterien: dict = {}
    cols = st.columns(len(felder))
    for col, feld, label in zip(cols, felder, labels):
        optionen = matcher.get_normen_optionen(conn, kriterien, feld)
        with col:
            wert = st.selectbox(label, [""] + optionen, key=f"normen_{feld}")
        if wert:
            kriterien[feld] = wert

    eigenschaft_optionen = [
        r[0] for r in conn.execute("SELECT DISTINCT eigenschaft FROM sonderposten ORDER BY eigenschaft").fetchall()
    ]
    eig_cols = st.columns(3)
    eigenschaften = []
    for i, col in enumerate(eig_cols):
        with col:
            e = st.selectbox(f"Eigenschaft {i + 1}", [""] + eigenschaft_optionen, key=f"eig_{i}")
        if e:
            eigenschaften.append(e)

    status, treffer = matcher.find_normen(conn, kriterien)
    if status == "unique":
        t = treffer[0]
        zusatzkosten = matcher.find_zusatzkosten(conn, kriterien, eigenschaften)
        gesamt = (t.preis or 0) + zusatzkosten
        st.success(f"Norm gefunden: {t.normen} — Preis: {gesamt:.2f} EUR (Basis {t.preis} + {zusatzkosten} Zusatz)")
        st.caption(f"Vollprüfung lt. Norm — {kategorie_hinweis}")
        umfang_zusatz = f"Vollprüfung; {kategorie_hinweis}"
        bemerkung = f"{t.bemerkungen} — {umfang_zusatz}" if t.bemerkungen else umfang_zusatz
        positionen.append(
            PruefplanPosition(
                setbestandteil="Hauptprodukt",
                produkt=t.produkt,
                pruefung=t.normen,
                anzahl="",
                kosten=gesamt,
                bemerkung=bemerkung,
                quelle="normenauswahl",
            )
        )
    elif status == "ambiguous":
        st.info(f"Auswahl nicht eindeutig ({len(treffer)} Normen) — bitte weitere Felder eingrenzen.")
    else:
        st.info("Bitte alle relevanten Felder auswählen, um eine passende Norm zu finden.")

with st.expander("Neuen Mechanik-Datensatz für dieses Produkt anlegen"):
    st.caption(
        "Falls kein bestehender Datensatz passt: hier einen neuen anlegen. Er wird dauerhaft "
        "gespeichert und bei künftigen Prüfaufträgen mit dieser Warengruppe vorgeschlagen."
    )
    with st.form("neuer_mechanik_datensatz"):
        neu_produkt = st.text_input(
            "Produkt", value=artikel.produktklassifizierung or artikel.artikelbezeichnung
        )
        neu_norm = st.text_input("Norm / EK / PPM")
        neu_anzahl = st.text_input("Anzahl Muster", value="2")
        neu_kosten = st.number_input("Kosten VP (EUR)", min_value=0.0, step=10.0, value=0.0)
        neu_bemerkung = st.text_area("Bemerkung")
        angelegt = st.form_submit_button("Datensatz anlegen")
        if angelegt:
            if not neu_produkt.strip() or not neu_norm.strip():
                st.error("Bitte mindestens Produkt und Norm angeben.")
            else:
                matcher.add_mechanik_regel(
                    conn,
                    lidl_bereich=artikel.warenbereich,
                    lidl_warengruppe=artikel.warengruppe,
                    warengruppe_code=artikel.warengruppe_code,
                    produkt=neu_produkt.strip(),
                    norm_ek_ppm=neu_norm.strip(),
                    anzahl_muster=neu_anzahl.strip(),
                    kosten_vp=neu_kosten or None,
                    bemerkungen=neu_bemerkung.strip(),
                )
                st.success(f"Datensatz '{neu_produkt}' angelegt.")
                st.rerun()

komponenten_flat = [k for liste in relevante_pruefumfang_komponenten.values() for k in liste]
klassifiziert = {k: matcher.klassifiziere_komponente(k) for k in komponenten_flat}

if any(kat == "sicherheit_norm" for kat in klassifiziert.values()):
    st.subheader("Kennzeichnung, Akku & weitere Standardprüfungen")
    st.caption(
        "Feste Teilprüfungen unter 'Sicherheit & Norm / Sonder- & Funktionsparameter'. "
        "Vorauswahl für Spielzeug/elektrisches Produkt basiert auf einem Textabgleich mit dem "
        "Warenbereich und wurde noch nicht an echten Beispielen geprüft — bitte kontrollieren. "
        "1005_PPM (Lebensmittelkontakt/LFGB) wird nicht automatisch erkannt, das war bislang "
        "manuelle Pflege in der KV-Monitoringliste. Preise sind noch nicht hinterlegt und "
        "müssen aktuell manuell ergänzt werden."
    )
    for pos in matcher.get_standard_pruefpositionen(conn):
        default_checked, begruendung = suggest.bewerte_standardposition(pos.bedingung, artikel)
        label = f"**{pos.code}** — {pos.bezeichnung}"
        checked = st.checkbox(label, value=default_checked, key=f"std_{pos.code}")
        st.caption(begruendung)
        if checked:
            positionen.append(
                PruefplanPosition(
                    setbestandteil="Kennzeichnung/Standard",
                    produkt=pos.bezeichnung,
                    pruefung=pos.code,
                    anzahl="",
                    kosten=pos.kosten,
                    bemerkung="Preis noch nicht hinterlegt" if pos.kosten is None else "",
                    quelle="standard",
                )
            )

st.subheader("Produktspezifikationen")

if any(kat == "produktspezifikation" for kat in klassifiziert.values()):
    st.caption(
        "Im Prüfumfang wurde '(Physikalische-) Produktspezifikationen' erkannt. Vorschlag basiert "
        "auf den Auslobungen im Feld 'Qualität' des Prüfauftrags — bitte prüfen und ggf. ergänzen."
    )
    katalog = matcher.get_produktspezifikation_katalog(conn)
    bewertet = suggest.rank_produktspezifikationen(
        katalog, artikel.qualitaet, artikel.artikelbezeichnung, artikel.produktklassifizierung
    )

    def _render_ps_eintrag(parameter, score, varianten, default_checked):
        label = f"**{parameter}** (Score {score:.2f})"
        checked = st.checkbox(label, value=default_checked, key=f"ps_{parameter}")
        variante = varianten[0]
        if len(varianten) > 1:
            optionen_labels = [
                f"{v.produkt or '-'} / {v.mak_paket or 'Basis'} / "
                f"{v.laufzeit + 'h' if v.laufzeit else '-'} — "
                f"{v.vk_preis if v.vk_preis is not None else (v.gesamtkosten or '-')} EUR"
                for v in varianten
            ]
            idx = st.selectbox(
                "Variante",
                range(len(varianten)),
                format_func=lambda i, opts=optionen_labels: opts[i],
                key=f"ps_variante_{parameter}",
            )
            variante = varianten[idx]
        else:
            st.caption(
                f"Norm: {variante.norm or '-'} — "
                f"Preis: {variante.vk_preis if variante.vk_preis is not None else (variante.gesamtkosten or '-')} EUR"
            )
        if checked:
            positionen.append(
                PruefplanPosition(
                    setbestandteil="Produktspezifikation",
                    produkt=f"{variante.parameter} ({variante.produkt})" if variante.produkt else variante.parameter,
                    pruefung=variante.norm,
                    anzahl=variante.anzahl_proben,
                    kosten=variante.vk_preis if variante.vk_preis is not None else variante.gesamtkosten,
                    bemerkung=variante.bemerkung,
                    quelle="produktspezifikation",
                )
            )

    vorschlaege = [(p, s, v) for p, s, v in bewertet if s > 0]
    weitere = [(p, s, v) for p, s, v in bewertet if s == 0]

    if vorschlaege:
        st.markdown("**Wahrscheinlichste Vorschläge (anhand der Auslobungen im Feld 'Qualität'):**")
        for parameter, score, varianten in vorschlaege:
            _render_ps_eintrag(parameter, score, varianten, default_checked=True)
    else:
        st.caption("Kein Parameter konnte anhand der Auslobungen automatisch zugeordnet werden.")

    with st.expander(f"Weitere Parameter durchsuchen ({len(weitere)})"):
        kategorien_reihenfolge = ["Küche", "Textil", "Outdoor", "Material / Sonstiges", "Sonstige"]
        nach_kategorie: dict = {k: [] for k in kategorien_reihenfolge}
        for parameter, score, varianten in weitere:
            nach_kategorie[suggest.kategorie_fuer_parameter(parameter)].append((parameter, score, varianten))
        for kategorie in kategorien_reihenfolge:
            eintraege = nach_kategorie[kategorie]
            if not eintraege:
                continue
            st.markdown(f"*{kategorie}*")
            for parameter, score, varianten in eintraege:
                _render_ps_eintrag(parameter, score, varianten, default_checked=False)
else:
    st.caption("Im erkannten Prüfumfang wurde keine Produktspezifikations-Anforderung gefunden.")

conn.close()

if positionen:
    st.subheader("Vorschau Prüfplan")
    ergebnis = PruefplanErgebnis(artikel=artikel, positionen=positionen)
    st.table(
        [
            {
                "Setbestandteil": p.setbestandteil,
                "Produkt": p.produkt,
                "Prüfung": p.pruefung,
                "Anzahl": p.anzahl,
                "Kosten": p.kosten,
            }
            for p in positionen
        ]
    )
    st.write(f"**Gesamtkosten:** {ergebnis.gesamtkosten:.2f} EUR")

    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            "Prüfplan als Excel herunterladen",
            data=excel_export.export_bytes(ergebnis),
            file_name=f"Pruefplan_{artikel.ian_charge}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    with col_b:
        st.download_button(
            "Prüfplan als PDF herunterladen",
            data=pdf_export.build_pdf(ergebnis),
            file_name=f"Pruefplan_{artikel.ian_charge}.pdf",
            mime="application/pdf",
        )
else:
    st.info("Noch keine Prüfpositionen ausgewählt.")
