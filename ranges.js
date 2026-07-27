// Rangordnung der Karten, absteigend (Index 0 = höchste Karte)
const RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'];

function rankIndex(ch) {
  return RANKS.indexOf(ch);
}

// Erweitert ein einzelnes Notationstoken (z.B. "77+", "A9s+", "K9s-KQs", "AKo")
// zu einer Liste konkreter Hand-Codes (z.B. "AA", "AKs", "AJo").
function expandToken(rawToken) {
  const token = rawToken.trim();
  if (!token) return [];

  const pairPlusMatch = token.match(/^([AKQJT98765432])\1\+$/);
  if (pairPlusMatch) {
    const r = rankIndex(pairPlusMatch[1]);
    const hands = [];
    for (let i = 0; i <= r; i++) hands.push(RANKS[i] + RANKS[i]);
    return hands;
  }

  const pairRangeMatch = token.match(/^([AKQJT98765432])\1-([AKQJT98765432])\2$/);
  if (pairRangeMatch) {
    const r1 = rankIndex(pairRangeMatch[1]);
    const r2 = rankIndex(pairRangeMatch[2]);
    const lo = Math.min(r1, r2);
    const hi = Math.max(r1, r2);
    const hands = [];
    for (let i = lo; i <= hi; i++) hands.push(RANKS[i] + RANKS[i]);
    return hands;
  }

  const soPlusMatch = token.match(/^([AKQJT98765432])([AKQJT98765432])([so])\+$/);
  if (soPlusMatch) {
    const hi = rankIndex(soPlusMatch[1]);
    const lo = rankIndex(soPlusMatch[2]);
    const suf = soPlusMatch[3];
    const hands = [];
    for (let li = hi + 1; li <= lo; li++) hands.push(RANKS[hi] + RANKS[li] + suf);
    return hands;
  }

  const soRangeMatch = token.match(/^([AKQJT98765432])([AKQJT98765432])([so])-\1([AKQJT98765432])\3$/);
  if (soRangeMatch) {
    const hi = rankIndex(soRangeMatch[1]);
    const lo1 = rankIndex(soRangeMatch[2]);
    const lo2 = rankIndex(soRangeMatch[4]);
    const suf = soRangeMatch[3];
    const loMin = Math.min(lo1, lo2);
    const loMax = Math.max(lo1, lo2);
    const hands = [];
    for (let li = loMin; li <= loMax; li++) hands.push(RANKS[hi] + RANKS[li] + suf);
    return hands;
  }

  const singleMatch = token.match(/^([AKQJT98765432])([AKQJT98765432])?([so])?$/);
  if (singleMatch) {
    return [token];
  }

  console.warn('Konnte Range-Token nicht parsen:', token);
  return [];
}

function parseNotation(tokens) {
  const set = new Set();
  tokens.forEach((tok) => {
    expandToken(tok).forEach((hand) => set.add(hand));
  });
  return set;
}

// Liefert Grid-Position {row, col} und Combo-Anzahl für einen Hand-Code.
function handInfo(hand) {
  if (hand.length === 2 && hand[0] === hand[1]) {
    const i = rankIndex(hand[0]);
    return { row: i, col: i, combos: 6, type: 'pair' };
  }
  const hi = rankIndex(hand[0]);
  const lo = rankIndex(hand[1]);
  const suf = hand[2];
  if (suf === 's') {
    return { row: hi, col: lo, combos: 4, type: 'suited' };
  }
  return { row: lo, col: hi, combos: 12, type: 'offsuit' };
}

function buildRangeGrid(tokens) {
  const hands = parseNotation(tokens);
  const cells = new Map(); // key "row-col" -> hand code
  let totalCombos = 0;
  hands.forEach((hand) => {
    const info = handInfo(hand);
    cells.set(`${info.row}-${info.col}`, hand);
    totalCombos += info.combos;
  });
  return { cells, totalCombos, handCount: hands.size };
}

const TOTAL_COMBOS = 1326;

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

const RANGE_DATA = {
  UTG: {
    title: 'UTG – Open Raise (RFI)',
    subtitle: 'Under the Gun',
    accent: '#e2703a',
    note: 'Sehr tighte Range – noch 7 Gegner müssen handeln, bevor die Runde zurückkommt.',
    tokens: ['66+', 'A9s+', 'KTs+', 'QTs+', 'JTs', 'T9s', 'AJo+', 'KQo'],
  },
  UTG1: {
    title: 'UTG+1 – Open Raise (RFI)',
    subtitle: 'Under the Gun +1',
    accent: '#e2703a',
    note: 'Minimal weiter als UTG, da eine Position weniger hinter dir sitzt.',
    tokens: ['55+', 'A7s+', 'KTs+', 'QTs+', 'JTs', 'T9s', '98s', 'AJo+', 'KQo'],
  },
  MP: {
    title: 'MP – Open Raise (RFI)',
    subtitle: 'Middle Position',
    accent: '#d4922f',
    note: 'Etwas mehr Suited Connectors und Broadways werden spielbar.',
    tokens: ['44+', 'A5s+', 'K9s+', 'Q9s+', 'J9s+', 'T9s', '98s', '87s', 'ATo+', 'KJo+', 'QJo'],
  },
  HJ: {
    title: 'HJ – Open Raise (RFI)',
    subtitle: 'Hijack',
    accent: '#c9a227',
    note: 'Deutlich breitere Range, da nur noch 3 Gegner hinter dir sind.',
    tokens: ['33+', 'A2s+', 'K8s+', 'Q9s+', 'J9s+', 'T8s+', '98s', '87s', '76s', 'ATo+', 'KTo+', 'QJo'],
  },
  CO: {
    title: 'CO – Open Raise (RFI)',
    subtitle: 'Cutoff',
    accent: '#8fae2f',
    note: 'Späte Position – viele Suited-Hände und schwächere Broadways werden profitabel.',
    tokens: ['22+', 'A2s+', 'K5s+', 'Q7s+', 'J7s+', 'T7s+', '96s+', '85s+', '75s+', '64s+', '54s', 'A8o+', 'K9o+', 'QTo+', 'JTo'],
  },
  BTN: {
    title: 'BTN – Open Raise (RFI)',
    subtitle: 'Button',
    accent: '#3f9b5e',
    note: 'Die weiteste Range am Tisch, da du danach immer als Letzter agierst.',
    tokens: ['22+', 'A2s+', 'K2s+', 'Q4s+', 'J6s+', 'T6s+', '95s+', '85s+', '74s+', '64s+', '53s+', '43s', 'A2o+', 'K7o+', 'Q9o+', 'J8o+', 'T8o+'],
  },
  SB: {
    title: 'SB – Open Raise (RFI, Folded to SB)',
    subtitle: 'Small Blind',
    accent: '#3f8fb0',
    note: 'Raise-Strategie gegen den BB, wenn alle vor dir gefoldet haben. Out of Position, daher etwas enger als BTN.',
    tokens: ['22+', 'A2s+', 'K4s+', 'Q6s+', 'J7s+', 'T7s+', '96s+', '86s+', '75s+', '65s', '54s', 'A5o+', 'K9o+', 'QTo+', 'JTo'],
  },
  BB: {
    title: 'BB – Defend vs. BTN-Open (Beispiel)',
    subtitle: 'Big Blind',
    accent: '#7d5fbf',
    note: 'Der BB eröffnet nie selbst (er sitzt im Blind). Gezeigt wird stattdessen eine beispielhafte Continue-Range (Call oder 3-Bet) gegen einen Button-Open.',
    tokens: ['22+', 'A2s+', 'K2s+', 'Q4s+', 'J6s+', 'T6s+', '95s+', '85s+', '74s+', '64s+', '53s+', '43s', '32s', 'A2o+', 'K5o+', 'Q8o+', 'J8o+', 'T8o+', '98o'],
  },
};
