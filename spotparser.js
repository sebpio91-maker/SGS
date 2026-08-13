// Freitext-Parser für Spot-Beschreibungen. Läuft komplett lokal, ruft keine
// externe API auf. Erkennt Position(en), Stacktiefe, Hero-Hand und groben
// Spot-Typ aus einem frei getippten Satz. Das Ergebnis ist bewusst nur ein
// Vorschlag -- die UI zeigt es in editierbaren Feldern zur Kontrolle an,
// bevor daraus eine Auswertung gebaut wird.

const POSITION_DEFS = [
  { id: 'UTG1', res: [/utg\s*\+\s*1/i, /utg\s*1\b/i] },
  { id: 'BTN', res: [/\bbtn\b/i, /\bbu\b/i, /\bbutton\b/i] },
  { id: 'SB', res: [/\bsb\b/i, /small\s*blind/i] },
  { id: 'BB', res: [/\bbb\b/i, /big\s*blind/i] },
  { id: 'CO', res: [/\bco\b/i, /cut\s*-?\s*off/i] },
  { id: 'HJ', res: [/\bhj\b/i, /hijack/i] },
  { id: 'MP', res: [/\bmp\b/i, /middle\s*position/i] },
  { id: 'UTG', res: [/\butg\b/i, /under\s*the\s*gun/i] },
];

const OTHER_SPOT_KEYWORDS = [
  { re: /3[\s-]?bet|three[\s-]?bet|dreibet/i, label: '3-Bet-Pot' },
  { re: /squeeze/i, label: 'Squeeze' },
  { re: /4[\s-]?bet|four[\s-]?bet/i, label: '4-Bet-Pot' },
  { re: /rejam|re-jam|shove|all[\s-]?in|jam/i, label: 'Rejam/All-in' },
  { re: /flop|turn|river|board/i, label: 'Postflop' },
];

const OPEN_VERB_RE = /raise|raist|open|erh[oö]ht|er[oö]ffnet/i;
const STACK_RE = /(\d{1,3})\s*(?:bb|big\s*blinds?)\b/i;
const HAND_RE = /\b([AKQJT2-9])([AKQJT2-9])([so])?\b/gi;

function maskSpan(text, start, end) {
  return text.slice(0, start) + ' '.repeat(end - start) + text.slice(end);
}

function nearestStack(n) {
  return STACK_DEPTHS.reduce((best, d) => (Math.abs(d - n) < Math.abs(best - n) ? d : best), STACK_DEPTHS[0]);
}

function scanPositions(text) {
  let working = text;
  const found = [];
  POSITION_DEFS.forEach((def) => {
    def.res.forEach((re) => {
      const flags = re.flags.includes('g') ? re.flags : re.flags + 'g';
      const g = new RegExp(re.source, flags);
      let m;
      while ((m = g.exec(working)) !== null) {
        const start = m.index;
        const end = m.index + m[0].length;
        const overlaps = found.some((p) => !(end <= p.start || start >= p.end));
        if (!overlaps) {
          found.push({ id: def.id, start, end });
          working = maskSpan(working, start, end);
        }
      }
    });
  });
  found.sort((a, b) => a.start - b.start);
  return { positions: found, masked: working };
}

// Parst einen frei getippten Spot-Text. Gibt nie einen Fehler, sondern
// bestmögliche (auch leere/unsichere) Werte zurück -- die Bestätigungs-UI
// fängt Fehlinterpretationen ab.
function parseSpotText(rawText) {
  const original = rawText || '';
  let working = original;

  let stack = null;
  const stackMatch = working.match(STACK_RE);
  if (stackMatch) {
    stack = nearestStack(parseInt(stackMatch[1], 10));
    working = maskSpan(working, stackMatch.index, stackMatch.index + stackMatch[0].length);
  }

  const { positions, masked } = scanPositions(working);

  let hand = null;
  let handNeedsSuffix = false;
  HAND_RE.lastIndex = 0;
  let hm;
  while ((hm = HAND_RE.exec(masked)) !== null) {
    const r1 = hm[1].toUpperCase();
    const r2 = hm[2].toUpperCase();
    const suf = hm[3] ? hm[3].toLowerCase() : '';
    if (r1 === r2 && suf) continue;
    hand = r1 + r2 + suf;
    if (r1 !== r2 && !suf) handNeedsSuffix = true;
    break;
  }

  const lower = original.toLowerCase();
  let scenario = 'rfi';
  let scenarioLabel = '';
  let openerPos = null;

  const otherMatch = OTHER_SPOT_KEYWORDS.find((k) => k.re.test(lower));
  if (otherMatch) {
    scenario = 'other';
    scenarioLabel = otherMatch.label;
  } else if (positions.length >= 2) {
    const heroId = positions[0].id;
    const candidate = positions.find((p) => p.id !== heroId);
    if (candidate && OPEN_VERB_RE.test(lower)) {
      scenario = 'vs_open';
      openerPos = candidate.id;
    }
  }

  return {
    heroPos: positions[0] ? positions[0].id : null,
    openerPos,
    stack,
    hand,
    handNeedsSuffix,
    scenario,
    scenarioLabel,
  };
}

// Rechnet einen Hand-Code ("AKo", "T9s", "77") in {row, col} des 13x13-Grids
// um -- dieselbe Konvention wie handCodeAt() in ranges.js. Gibt null zurück,
// wenn die Notation ungültig oder unvollständig ist (fehlendes s/o).
function handToCell(handStr) {
  if (!handStr) return null;
  const s = handStr.trim().toUpperCase();
  if (s.length < 2) return null;
  const r1 = s[0];
  const r2 = s[1];
  const suf = s[2] ? s[2].toLowerCase() : '';
  const i1 = RANKS.indexOf(r1);
  const i2 = RANKS.indexOf(r2);
  if (i1 === -1 || i2 === -1) return null;
  if (i1 === i2) return { row: i1, col: i1 };
  if (suf !== 's' && suf !== 'o') return null;
  const hi = Math.min(i1, i2);
  const lo = Math.max(i1, i2);
  return suf === 's' ? { row: hi, col: lo } : { row: lo, col: hi };
}

// Ordnet eine Sitzposition der Gruppen-Bezeichnung zu, die CONTINUE_STATS
// verwendet (dort gibt es nur EP/MP/CO/BTN als Eröffner bzw.
// MP/CO/BTN/SB/BB als Continue-Positionen).
function toContinueGroup(posId) {
  if (posId === 'UTG' || posId === 'UTG1') return 'EP';
  return posId;
}
