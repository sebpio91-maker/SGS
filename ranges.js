// Rangordnung der Karten, absteigend (Index 0 = höchste Karte)
const RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'];
const TOTAL_COMBOS = 1326;
const POS_ORDER = ['EP', 'MP', 'HJ', 'CO', 'BTN'];
const STACK_DEPTHS = [100, 60, 40, 30, 20];

function rankIndex(ch) {
  return RANKS.indexOf(ch);
}

// Hand-Code (z.B. "AKs", "72o", "77") für eine Grid-Zelle (Zeile/Spalte, je 0-12).
function handCodeAt(row, col) {
  if (row === col) return RANKS[row] + RANKS[row];
  if (row < col) return RANKS[row] + RANKS[col] + 's';
  return RANKS[col] + RANKS[row] + 'o';
}

// Anzahl Kombinationen einer Grid-Zelle: Pair=6, Suited=4, Offsuit=12.
function combosAt(row, col) {
  if (row === col) return 6;
  if (row < col) return 4;
  return 12;
}

// Baut die Open-Raise-Range einer Positionsgruppe (EP/MP/HJ/CO/BTN) bei einer
// bestimmten Stacktiefe aus OPEN_RAISE_GRID (siehe myranges.js, aus der Excel erzeugt).
// Jede Zelle dort trägt den Code der am weitesten links sitzenden Position, die diese
// Hand eröffnet ('0' = niemand). Da Ranges verschachtelt breiter werden (EP ⊆ MP ⊆ HJ ⊆ CO ⊆ BTN),
// ist eine Hand für Zielposition "group" enthalten, wenn ihr Code <= Rang von "group" ist.
function buildOpenRaiseGrid(stack, group) {
  const grid = OPEN_RAISE_GRID[stack];
  const targetRank = POS_ORDER.indexOf(group) + 1;
  const cells = new Map();
  const allinCells = new Set();
  let totalCombos = 0;

  for (let row = 0; row < 13; row++) {
    for (let col = 0; col < 13; col++) {
      const raw = grid[row][col];
      if (raw === '0') continue;
      const allin = raw.endsWith('a');
      const rank = parseInt(raw, 10);
      if (rank <= targetRank) {
        const key = `${row}-${col}`;
        cells.set(key, handCodeAt(row, col));
        totalCombos += combosAt(row, col);
        if (allin) allinCells.add(key);
      }
    }
  }
  return { cells, totalCombos, allinCells };
}

const POSITIONS = [
  { id: 'UTG', label: 'UTG', short: 'UTG' },
  { id: 'UTG1', label: 'UTG+1', short: 'UTG+1' },
  { id: 'MP', label: 'MP', short: 'MP' },
  { id: 'HJ', label: 'HJ', short: 'HJ' },
  { id: 'CO', label: 'CO', short: 'CO' },
  { id: 'BTN', label: 'BTN', short: 'BTN' },
  { id: 'SB', label: 'SB', short: 'SB' },
  { id: 'BB', label: 'BB', short: 'BB' },
];

// Metadaten je Sitz. kind 'open' -> Open-Raise-Grid (aus OPEN_RAISE_GRID, Gruppe "group").
// kind 'continue' -> Continue-Statistik (aus CONTINUE_STATS), da SB/BB nie zuerst eröffnen.
const RANGE_DATA = {
  UTG: {
    kind: 'open',
    group: 'EP',
    title: 'UTG – Open Raise (RFI)',
    subtitle: 'Under the Gun',
    accent: '#e2703a',
    note: 'Aus deiner Tabelle übernommen. Deine Excel unterscheidet nicht zwischen UTG und UTG+1 – beide nutzen die "EP"-Range.',
  },
  UTG1: {
    kind: 'open',
    group: 'EP',
    title: 'UTG+1 – Open Raise (RFI)',
    subtitle: 'Under the Gun +1',
    accent: '#e2703a',
    note: 'Aus deiner Tabelle übernommen. Deine Excel unterscheidet nicht zwischen UTG und UTG+1 – beide nutzen die "EP"-Range.',
  },
  MP: {
    kind: 'open',
    group: 'MP',
    title: 'MP – Open Raise (RFI)',
    subtitle: 'Middle Position',
    accent: '#d4922f',
    note: 'Aus deiner Tabelle übernommen (Blatt "Openraising").',
  },
  HJ: {
    kind: 'open',
    group: 'HJ',
    title: 'HJ – Open Raise (RFI)',
    subtitle: 'Hijack',
    accent: '#c9a227',
    note: 'Aus deiner Tabelle übernommen (Blatt "Openraising").',
  },
  CO: {
    kind: 'open',
    group: 'CO',
    title: 'CO – Open Raise (RFI)',
    subtitle: 'Cutoff',
    accent: '#8fae2f',
    note: 'Aus deiner Tabelle übernommen (Blatt "Openraising").',
  },
  BTN: {
    kind: 'open',
    group: 'BTN',
    title: 'BTN – Open Raise (RFI)',
    subtitle: 'Button',
    accent: '#3f9b5e',
    note: 'Aus deiner Tabelle übernommen (Blatt "Openraising").',
  },
  SB: {
    kind: 'continue',
    title: 'SB – Continue-Range',
    subtitle: 'Small Blind',
    accent: '#3f8fb0',
    note: 'Deine Tabelle enthält für SB kein Hand-für-Hand-Grid, sondern nur die Continue-Quote (Call + 3-Bet zusammen) gegen die jeweilige Eröffner-Position (Blatt "% Ranges" / "Flat & 3-Bet").',
  },
  BB: {
    kind: 'continue',
    title: 'BB – Continue-Range',
    subtitle: 'Big Blind',
    accent: '#7d5fbf',
    note: 'Der BB eröffnet nie selbst. Deine Tabelle enthält für BB kein Hand-für-Hand-Grid, sondern nur die Continue-Quote (Call + 3-Bet zusammen) gegen die jeweilige Eröffner-Position (Blatt "% Ranges" / "Flat & 3-Bet").',
  },
};
