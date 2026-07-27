# Beispiel-/Startdaten, übernommen aus dem Normenauswahl.xlsm ("NORMEN"-Blatt),
# damit die Datenbank direkt mit einem funktionierenden Beispiel (DIN EN 581-1/-2/-3)
# gefüllt ist.

NORMEN_SEED = [
    {
        "kurzbezeichnung": "EN 581-1",
        "vollbezeichnung": "EN 581-1:2017",
        "titel": (
            "Außenmöbel - Sitzmöbel und Tische für den Camping-, Wohn und "
            "Objektbereich - Teil 1: Allgemeine sicherheitstechnische Anforderungen"
        ),
        "status": "aktiv",
        "kategorie": "Möbel",
        "pruefpunkte": [
            {"kapitel": "NV", "ueberschrift": "Nationales Vorwort", "relevanz": "Nein"},
            {"kapitel": "EV", "ueberschrift": "Europäisches Vorwort", "relevanz": "Nein"},
            {
                "kapitel": "1",
                "ueberschrift": "Anwendungsbereich",
                "relevanz": "Indirekt",
                "inhalt": (
                    "Dieser Teil von EN 581 legt allgemeine sicherheitstechnische Anforderungen für "
                    "Außensitzmöbel und Außentische zur Verwendung durch Erwachsene im Camping-, "
                    "Wohn- und Objektbereich fest, ohne Berücksichtigung der Materialien, des "
                    "Designs/der Konstruktion oder der Herstellungsprozesse.\n"
                    "Er gilt nicht für Sitzmöbel für Zuschaueranlagen.\n"
                    "Er enthält keine Anforderungen an die Dauerhaltbarkeit von Polstermaterialien, "
                    "Rollen-, Liege- und Kippmechanismen sowie Mechanismen zur Sitzhöhenverstellung.\n"
                    "Mechanische Sicherheitsanforderungen werden für die Sitzmöbel in EN 581-2 und für "
                    "Tische in EN 581-3 abgedeckt.\n"
                    "Anhang A (informativ) enthält eine schematische Darstellung der Anforderungen und "
                    "Bedingungen bezüglich der Scher- und Quetschstellen.\n"
                    "Anhang B (informativ) enthält eine Begründung für die Verletzungen von Fingern."
                ),
            },
            {"kapitel": "2", "ueberschrift": "Normative Verweisungen", "relevanz": "Indirekt"},
            {"kapitel": "3", "ueberschrift": "Begriffe", "relevanz": "Indirekt"},
            {"kapitel": "4", "ueberschrift": "Prüffinger", "relevanz": "Indirekt"},
            {"kapitel": "5", "ueberschrift": "Sicherheitstechnische Anforderungen", "relevanz": "Ja"},
            {
                "kapitel": "5.1",
                "ueberschrift": "Allgemeines",
                "relevanz": "Ja",
                "inhalt": (
                    "Um Verletzungen zu vermeiden, wenn sich das Produkt in seiner vorgesehenen "
                    "Gebrauchsstellung befindet, müssen alle Kanten und Ecken abgerundet, abgeschrägt "
                    "oder anderweitig geschützt sein. Das gilt für:\n"
                    "— Sitzmöbel: Kanten des Sitzes, der Rückenlehne und Armlehnen und jedes Teils der "
                    "Sitzflächen-Unterseite, bei einem Abstand von weniger als 120 mm von jeder Kante, "
                    "die ein Finger üblicherweise erreichen kann;\n"
                    "— Tische: Tischflächen, jeder Teil der Unterseite der Oberfläche bei einem Abstand "
                    "von weniger als 500 mm von jeder Kante unter dem Tisch, das ein Knie und/oder ein "
                    "Arm üblicherweise erreichen kann.\n"
                    "Alle anderen Teile müssen ohne Grate, scharfe Kanten und scharfe Spitzen sein.\n"
                    "Die einstellbaren und beweglichen Teile müssen so ausgeführt sein, dass jede "
                    "Verletzung und jede unbeabsichtigte Betätigung vermieden werden.\n"
                    "Kein lasttragendes Teil des Möbelstücks darf sich unbeabsichtigt lösen können.\n"
                    "Alle zum leichteren Gleiten mit einem Schmierstoff versehenen Teile müssen so "
                    "ausgeführt sein, dass die Benutzer bei bestimmungsgemäßem Gebrauch vor "
                    "Schmiermittelflecken geschützt sind."
                ),
            },
            {
                "kapitel": "5.2",
                "ueberschrift": "Röhrenförmige Bauteile",
                "relevanz": "Ja",
                "inhalt": (
                    "In den Enden röhrenförmiger Bauteile dürfen keine zugänglichen Löcher sein, die "
                    "einen Durchmesser zwischen 7 mm und 12 mm und eine Tiefe von ≥ 10 mm haben.\n"
                    "Die Unterseiten der röhrenförmigen Beine, die mit dem Fußboden in Kontakt stehen, "
                    "müssen geschlossen oder mit einem Deckel versehen werden, Löcher darin sind "
                    "erlaubt, solange sie nicht zwischen 7 mm und 12 mm groß sind.\n"
                    "Diese Anforderungen müssen mit Hilfe der Prüffinger (Abschnitt 4) beurteilt werden."
                ),
            },
            {"kapitel": "5.3", "ueberschrift": "Scher- und Quetschstellen", "relevanz": "Ja"},
            {
                "kapitel": "5.3.1",
                "ueberschrift": "Scher- und Quetschstellen beim Aufstellen, Einstellen und Zusammenklappen",
                "relevanz": "Ja",
                "inhalt": (
                    "Sofern 5.3.2 oder 5.3.3 nicht zutreffend ist, sind Scher- und Quetschstellen, die "
                    "nur beim Aufstellen, Einstellen oder Zusammenklappen entstehen, zulässig, sofern "
                    "davon ausgegangen werden kann, dass der/die Benutzer/-in seine/ihre Bewegungen "
                    "unter Kontrolle hat und in der Lage ist, die Krafteinwirkung bei Schmerzempfindung "
                    "sofort zu beenden."
                ),
            },
            {
                "kapitel": "5.3.2",
                "ueberschrift": "Scher- und Quetschstellen unter Einwirkung von kraftbetriebenen Vorrichtungen",
                "relevanz": "Ja",
                "inhalt": (
                    "Teile eines Möbels, die durch kraftbetriebene Vorrichtungen, z. B. mechanische "
                    "Federn und Gasfedern, bewegt werden, dürfen keine zugänglichen Scher- und "
                    "Quetschstellen bilden.\n"
                    "Diese Anforderung muss mit Hilfe der Prüffinger (Abschnitt 4) beurteilt werden."
                ),
            },
            {
                "kapitel": "5.3.3",
                "ueberschrift": "Scher- und Quetschstellen bei der Benutzung",
                "relevanz": "Ja",
                "inhalt": (
                    "Es dürfen keine zugänglichen Scher- und Quetschstellen durch Belastungen entstehen, "
                    "die bei bestimmungsgemäßer Benutzung aufgebracht werden. Scher- und Quetschstellen "
                    "sind nicht zulässig, wenn bei üblichen Bewegungen und Tätigkeiten, z. B. beim "
                    "Versuch des Anhebens des Sitzes, um den Stuhl zu verrücken, oder Verstellen der "
                    "Rückenlehne, durch das Körpergewicht des Benutzers eine Verletzungsgefahr entsteht.\n"
                    "Diese Anforderung muss mit Hilfe der Prüffinger (Abschnitt 4) beurteilt werden.\n"
                    "Bei Liegen ist die angewandte Last während des normalen Gebrauchs die Last, die für "
                    "die folgenden mechanischen Prüfungen nach EN 581-2:2015, Tabelle 1, verwendet wurde:\n"
                    "— Prüfung 2: Ergänzende statische Belastungsprüfung an Sitzfläche und Beinauflage;\n"
                    "— Prüfung 3: Dauerhaltbarkeitsprüfung an Sitzfläche und Rückenlehne;\n"
                    "— Prüfung 4: Zusätzliche Dauerhaltbarkeitsprüfung an der Sitzfläche;\n"
                    "— Prüfung 5: Dauerhaltbarkeitsprüfung an der Verstellvorrichtung der Rückenlehne.\n"
                    "Bei anderen Sitzmöbeln ist die angewandte Last während des normalen Gebrauchs die "
                    "Last, die für die folgenden mechanischen Prüfungen nach EN 581-2:2015, Tabelle 2, "
                    "verwendet wurde:\n"
                    "— Prüfung 2: Statische Belastung der Sitzvorderkante;\n"
                    "— Prüfung 3: Kombinierte Dauerhaltbarkeitsprüfung an Sitzfläche und Rückenlehne;\n"
                    "— Prüfung 4: Dauerhaltbarkeitsprüfung von Sitzmöbeln mit einer Mehrpositions-Rückenlehne.\n"
                    "Bei Tischen ist die angewandte Last während des normalen Gebrauchs die Last, die für "
                    "die folgenden mechanischen Prüfungen nach EN 581-3:2007, Tabelle 1, verwendet wurde:\n"
                    "— Prüfung 1: Vertikale statische Belastung der Hauptoberfläche;\n"
                    "— Prüfung 4: Vertikale statische Belastung der Ergänzungsplatte;\n"
                    "— Prüfung 5: Horizontale Dauerhaltbarkeitsprüfung."
                ),
            },
            {"kapitel": "6", "ueberschrift": "Prüfbericht", "relevanz": "Indirekt"},
            {
                "kapitel": "Anhang A",
                "ueberschrift": "(informativ) Schematische Darstellung der Anforderungen und Bedingungen bezüglich Scher- und Quetschstellen",
                "relevanz": "Indirekt",
            },
            {
                "kapitel": "Anhang B",
                "ueberschrift": "(informativ) Begründung für die Verletzungen von Fingern",
                "relevanz": "Nein",
            },
        ],
    },
    {
        "kurzbezeichnung": "EN 581-2",
        "vollbezeichnung": "DIN EN 581-2:2017-01",
        "titel": (
            "Außenmöbel – Sitzmöbel und Tische für den Camping-, Wohn- und Objektbereich – "
            "Teil 2: Mechanische Sicherheitsanforderungen und Prüfverfahren für Sitzmöbel"
        ),
        "status": "aktiv",
        "kategorie": "Möbel",
        "pruefpunkte": [
            {"kapitel": "NV", "ueberschrift": "Nationales Vorwort", "relevanz": "Nein"},
            {"kapitel": "EV", "ueberschrift": "Europäisches Vorwort", "relevanz": "Nein"},
            {
                "kapitel": "1",
                "ueberschrift": "Anwendungsbereich",
                "relevanz": "Indirekt",
                "inhalt": (
                    "Diese Europäische Norm legt die Mindestanforderungen an die Sicherheit, Festigkeit "
                    "und Dauerhaltbarkeit für alle Arten von Außensitzmöbeln für Erwachsene, unabhängig "
                    "von Werkstoffen, Design/Konstruktion oder Herstellungsprozessen, fest.\n"
                    "Sie gilt nicht für öffentlich aufgestellte Straßenmöbel.\n"
                    "Sie gilt nicht für abnehmbare Polster und Bezüge.\n"
                    "Sie enthält keine Anforderungen an die Dauerhaltbarkeit von Rollen/Rädern und an "
                    "Mechanismen zur Höhenverstellung.\n"
                    "Sie enthält keine Anforderungen an die elektrische Sicherheit.\n"
                    "Sie enthält keine Anforderungen an die Alterungsbeständigkeit und Verwitterung "
                    "verursacht durch Licht, Temperatur und Feuchtigkeit.\n"
                    "Die in dieser Norm enthaltenen Prüfanforderungen beruhen auf dem Gebrauch durch "
                    "Personen mit einem Körpergewicht bis zu 110 kg."
                ),
            },
            {"kapitel": "2", "ueberschrift": "Normative Verweisungen", "relevanz": "Indirekt"},
            {"kapitel": "3", "ueberschrift": "Begriffe", "relevanz": "Indirekt"},
            {
                "kapitel": "4",
                "ueberschrift": "Prüfung",
                "relevanz": "Ja",
                "inhalt": "EN 1728 / EN 1022",
            },
            {"kapitel": "5", "ueberschrift": "Prüfeinrichtung", "relevanz": "Ja"},
            {
                "kapitel": "6",
                "ueberschrift": "Anforderungen an die Sicherheit, Festigkeit und Dauerhaltbarkeit bei Liegen",
                "relevanz": "Ja",
            },
            {"kapitel": "6.1", "ueberschrift": "Allgemeines", "relevanz": "Ja"},
            {"kapitel": "6.2", "ueberschrift": "Standsicherheit, Festigkeit und Dauerhaltbarkeit", "relevanz": "Ja"},
            {
                "kapitel": "6.2.1",
                "ueberschrift": "Prüfreihenfolge und Prüfparameter",
                "relevanz": "Ja",
                "inhalt": "Die Liege ist in der in Tabelle 1 angegebenen Reihenfolge zu prüfen.",
            },
            {
                "kapitel": "6.2.2",
                "ueberschrift": "Anforderungen",
                "relevanz": "Ja",
                "inhalt": (
                    "Die Anforderungen an die Sicherheit, Festigkeit und Dauerhaltbarkeit sind "
                    "eingehalten, wenn nach der Prüfung nach Tabelle 1:\n"
                    "a) kein Teil, Bauteil oder Verbindungselement Brüche aufweist;\n"
                    "b) sich kein Verbindungselement gelöst hat, welches festsitzen muss;\n"
                    "c) die Liege ihre Funktion nach Entfernung der Prüflasten erfüllt;\n"
                    "d) das Produkt während der Standsicherheitsprüfungen nicht umkippt."
                ),
            },
            {
                "kapitel": "7",
                "ueberschrift": "Anforderungen an die Sicherheit, Festigkeit und Dauerhaltbarkeit bei anderen Sitzmöbeln",
                "relevanz": "Ja",
            },
            {"kapitel": "7.1", "ueberschrift": "Allgemeines", "relevanz": "Ja"},
            {"kapitel": "7.2", "ueberschrift": "Standsicherheit, Festigkeit und Dauerhaltbarkeit", "relevanz": "Ja"},
            {
                "kapitel": "7.2.1",
                "ueberschrift": "Prüfreihenfolge und Prüfparameter",
                "relevanz": "Ja",
                "inhalt": (
                    "Das Sitzmöbel ist in der in Tabelle 2 angegebenen Reihenfolge auf Festigkeit, "
                    "Dauerhaltbarkeit und Standsicherheit zu prüfen."
                ),
            },
            {
                "kapitel": "7.2.2",
                "ueberschrift": "Anforderungen",
                "relevanz": "Ja",
                "inhalt": (
                    "Die Anforderungen an die Sicherheit, Festigkeit und Dauerhaltbarkeit sind "
                    "eingehalten, wenn nach der Prüfung nach Tabelle 2:\n"
                    "a) kein Teil, Bauteil oder Verbindungselement Brüche aufweist;\n"
                    "b) sich kein Verbindungselement gelöst hat, welches festsitzen muss;\n"
                    "c) das Sitzmöbel seine Funktion nach Entfernung der Prüflasten erfüllt;\n"
                    "d) das Sitzmöbel die sicherheitstechnischen Anforderungen erfüllt;\n"
                    "e) das Produkt während der Standsicherheitsprüfungen nicht umkippt."
                ),
            },
            {"kapitel": "8", "ueberschrift": "Gebrauchsanleitung", "relevanz": "Ja"},
            {
                "kapitel": "8.1",
                "ueberschrift": "Allgemeines",
                "relevanz": "Ja",
                "inhalt": (
                    "Eine Gebrauchsanleitung muss in der(den) Sprache(n) des Landes beigefügt werden, in "
                    "dem das Sitzmöbel verkauft wird. Diese Gebrauchsanleitung muss in Buchstaben von "
                    "mindestens 5 mm Höhe die folgende Überschrift aufweisen: „WICHTIG, FÜR SPÄTERE "
                    "BEZUGNAHME AUFBEWAHREN: SORGFÄLTIG LESEN“, es sei denn, das Produkt ist dauerhaft "
                    "mit den folgenden Angaben gekennzeichnet.\n"
                    "Es müssen mindestens die folgenden Angaben enthalten sein:\n"
                    "a) Name und Anschrift des Herstellers/Lieferanten/Einzelhändlers;\n"
                    "b) Nutzungsbedingungen für das Produkt (Camping-, Wohn- oder Objektbereich).\n"
                    "Falls zutreffend:\n"
                    "c) Aufbauanleitung;\n"
                    "d) Anweisungen zur Pflege und Instandhaltung des Sitzmöbels;\n"
                    "e) sofern das Sitzmöbel mit einer Sitzhöhen-Einstellvorrichtung mit Energiespeicher "
                    "ausgerüstet ist, muss eine zusätzliche Anmerkung vorhanden sein, in der darauf "
                    "hingewiesen wird, dass nur geschultes Personal die Bauteile der "
                    "Sitzhöhen-Einstellvorrichtung mit Energiespeicher austauschen oder reparieren darf."
                ),
            },
            {
                "kapitel": "8.2",
                "ueberschrift": "Kennzeichnung bei Liegen",
                "relevanz": "Ja",
                "inhalt": (
                    "Mit Rädern ausgestattete Liegen, die nicht dazu vorgesehen sind, mit einer darauf "
                    "befindlichen Person angehoben und bewegt zu werden, sind mit dem in Bild 2 "
                    "dargestellten graphischen Symbol dauerhaft zu kennzeichnen. Die kleinste Abmessung "
                    "des graphischen Symbols darf nicht kleiner als 25 mm sein."
                ),
            },
            {"kapitel": "9", "ueberschrift": "Prüfbericht", "relevanz": "Indirekt"},
            {
                "kapitel": "Anhang A",
                "ueberschrift": "(normativ) Prüfungen der Standsicherheit bei Liegen nach vorne und zur Seite",
                "relevanz": "Ja",
            },
            {"kapitel": "A.1", "ueberschrift": "Prüfverfahren", "relevanz": "Ja"},
            {
                "kapitel": "Anhang B",
                "ueberschrift": "(informativ) Kaufinformation (Leitfaden)",
                "relevanz": "Nein",
                "inhalt": (
                    "Um dem Verbraucher vor dem Kauf die Wahl eines Produktes im Hinblick auf die "
                    "vorgesehene Nutzung zu ermöglichen, sollte die Kaufinformation ohne Öffnen der "
                    "Verpackung verfügbar sein. Folgende Angaben sollten enthalten sein:\n"
                    "— Bezeichnung des Produktes;\n"
                    "— Produktmerkmale, z. B. Maße, Angaben zur Aufbewahrung, Pflege, usw.;\n"
                    "— Nutzungsbedingungen für das Produkt (Camping-, Wohn- oder Objektbereich)."
                ),
            },
        ],
    },
    {
        "kurzbezeichnung": "EN 581-3",
        "vollbezeichnung": "EN 581-3:2017",
        "titel": None,
        "status": "aktiv",
        "kategorie": "Möbel",
        "pruefpunkte": [
            {"kapitel": "NV", "ueberschrift": "Nationales Vorwort", "relevanz": "Nein"},
            {"kapitel": "EV", "ueberschrift": "Europäisches Vorwort", "relevanz": "Nein"},
            {
                "kapitel": "1",
                "ueberschrift": "Anwendungsbereich",
                "relevanz": "Indirekt",
                "inhalt": (
                    "Diese Europäische Norm legt die Mindestanforderungen an die Sicherheit, Festigkeit "
                    "und Dauerhaltbarkeit für alle Arten von Außentischen für Erwachsene, unabhängig von "
                    "Werkstoffen, Design/Konstruktion oder Herstellungsprozessen, fest.\n"
                    "Sie gilt nicht für öffentlich aufgestellte Straßenmöbel.\n"
                    "Die Norm enthält mit Ausnahme der Prüfungen der Standsicherheit keine Beurteilung "
                    "der Eignung der in Tischen enthaltenen Aufbewahrungsmöglichkeiten.\n"
                    "Sie enthält keine Anforderungen an die Dauerhaltbarkeit von Rollen/Rädern und an "
                    "Mechanismen zur Höhenverstellung.\n"
                    "Sie enthält keine Anforderungen an die elektrische Sicherheit.\n"
                    "Sie enthält keine Anforderungen an die Alterungsbeständigkeit und an durch Licht, "
                    "Temperatur und Feuchtigkeit verursachte Qualitätsminderungen."
                ),
            },
            {"kapitel": "2", "ueberschrift": "Normative Verweisungen", "relevanz": "Indirekt"},
            {"kapitel": "3", "ueberschrift": "Begriffe", "relevanz": "Indirekt"},
            {
                "kapitel": "4",
                "ueberschrift": "Prüfung",
                "relevanz": "Indirekt",
                "inhalt": "Das Prüfen ist nach EN 1730 durchzuführen.",
            },
            {"kapitel": "5", "ueberschrift": "Anforderungen an die Sicherheit, Festigkeit und Dauerhaltbarkeit", "relevanz": "Ja"},
            {
                "kapitel": "5.1",
                "ueberschrift": "Allgemeines",
                "relevanz": "Ja",
                "inhalt": (
                    "Die Anforderungen nach EN 581-1:2017 müssen vor und nach der Durchführung der "
                    "Prüfungen der Festigkeit, Dauerhaltbarkeit und Standsicherheit erfüllt sein.\n"
                    "Glastischplatten müssen den Anforderungen nach EN 12150-1:2015, Abschnitt 8, "
                    "Prüfung der Bruchstruktur, oder dem Bruchverhalten (β) vom Typ B oder Typ C nach "
                    "EN 12600:2002 entsprechen.\n"
                    "Öffnungen für Sonnenschirme in der Glastischplatte müssen geschützt sein, um einen "
                    "Kontakt zwischen Metall und Glas zu vermeiden."
                ),
            },
            {"kapitel": "5.2", "ueberschrift": "Standsicherheit, Festigkeit und Dauerhaltbarkeit", "relevanz": "Ja"},
            {
                "kapitel": "5.2.1",
                "ueberschrift": "Prüfreihenfolge und Prüfparameter",
                "relevanz": "Ja",
                "inhalt": "Der Tisch ist in der in Tabelle 1 angegebenen Reihenfolge zu prüfen.",
            },
            {
                "kapitel": "5.2.2",
                "ueberschrift": "Anforderungen",
                "relevanz": "Ja",
                "inhalt": (
                    "Die Anforderungen an die Sicherheit, Festigkeit und Dauerhaltbarkeit sind "
                    "eingehalten, wenn nach der Prüfung nach Tabelle 1:\n"
                    "a) kein Teil, Bauteil oder Verbindungselement Brüche aufweist;\n"
                    "b) sich kein bestimmungsgemäß festsitzendes Verbindungselement gelöst hat;\n"
                    "c) der Tisch nach Entfernung der Prüflasten seine Funktionen erfüllt.\n"
                    "Das Produkt darf während der Standsicherheitsprüfungen nicht umkippen."
                ),
            },
            {
                "kapitel": "6",
                "ueberschrift": "Gebrauchsanleitung",
                "relevanz": "Ja",
                "inhalt": (
                    "Eine Gebrauchsanleitung muss in der oder den Sprachen des Landes beigefügt werden, "
                    "in dem die Tische verkauft werden. Diese Gebrauchsanleitung muss in Buchstaben von "
                    "nicht weniger als 5 mm Höhe die folgende Überschrift aufweisen: „WICHTIG, FÜR "
                    "SPÄTERE BEZUGNAHME AUFBEWAHREN: SORGFÄLTIG LESEN“, es sei denn, das Produkt ist "
                    "dauerhaft mit den folgenden Angaben gekennzeichnet.\n"
                    "Es müssen mindestens die folgenden Angaben enthalten sein:\n"
                    "a) Name und Anschrift des Herstellers/Lieferanten/Einzelhändlers;\n"
                    "b) Nutzungsbedingungen für das Produkt (Camping-, Wohn- oder Objektbereich).\n"
                    "Falls zutreffend:\n"
                    "c) Aufbauanweisungen;\n"
                    "d) Anweisungen zur Pflege und Instandhaltung des Tisches;\n"
                    "e) bei Tischen, die über eine Öffnung für einen Sonnenschirm verfügen, die aber "
                    "nicht dazu vorgesehen sind, als alleinige Sonnenschirmhalterung zu dienen, ein "
                    "Warnhinweis, dass ein Sonnenschirm immer mit einem geeigneten Gestell zu verwenden ist."
                ),
            },
            {"kapitel": "7", "ueberschrift": "Prüfbericht", "relevanz": "Indirekt"},
            {
                "kapitel": "Anhang A",
                "ueberschrift": "(informativ) Kaufinformation (Leitfaden)",
                "relevanz": "Nein",
                "inhalt": (
                    "Um dem Verbraucher vor dem Kauf die Wahl eines Produktes im Hinblick auf die "
                    "vorgesehene Nutzung zu ermöglichen, sollte die Kaufinformation ohne Öffnen der "
                    "Verpackung verfügbar sein. Folgende Angaben sollten enthalten sein:\n"
                    "- Bezeichnung des Produktes;\n"
                    "- Produktmerkmale, z. B. Maße, Angaben zur Aufbewahrung, Pflege usw.;\n"
                    "- Nutzungsbedingungen für das Produkt (Camping-, Wohn- oder Objektbereich);\n"
                    "- ein Warnhinweis, falls der Tisch, der ein Loch für einen Sonnenschirm hat, nicht "
                    "dafür vorgesehen ist, einen Sonnenschirm zu halten."
                ),
            },
        ],
    },
]


def seed_if_empty(db):
    from .models import Norm, Pruefpunkt

    if db.query(Norm).count() > 0:
        return

    for norm_data in NORMEN_SEED:
        norm = Norm(
            kurzbezeichnung=norm_data["kurzbezeichnung"],
            vollbezeichnung=norm_data.get("vollbezeichnung"),
            titel=norm_data.get("titel"),
            status=norm_data.get("status", "aktiv"),
            kategorie=norm_data.get("kategorie"),
        )
        db.add(norm)
        db.flush()

        for i, punkt in enumerate(norm_data["pruefpunkte"]):
            db.add(
                Pruefpunkt(
                    norm_id=norm.id,
                    kapitel=punkt.get("kapitel"),
                    ueberschrift=punkt.get("ueberschrift"),
                    pruefungsrelevant=punkt.get("relevanz", "Nein"),
                    inhalt=punkt.get("inhalt"),
                    sortierung=i,
                )
            )
    db.commit()
