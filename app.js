// Seat-Koordinaten (in % des Tisch-Containers) im Uhrzeigersinn, exakt auf der
// Ellipsen-Kontur des ovalen Tisches (gleicher Radius-Anteil in beiden Achsen,
// wodurch die Punkte automatisch der Ellipse folgen statt einem quadratischen Raster).
const SEAT_COORDS = {
  UTG: { top: 19.6, left: 19.6 },
  UTG1: { top: 7, left: 50 },
  MP: { top: 19.6, left: 80.4 },
  HJ: { top: 50, left: 93 },
  CO: { top: 80.4, left: 80.4 },
  BTN: { top: 93, left: 50 },
  SB: { top: 80.4, left: 19.6 },
  BB: { top: 50, left: 7 },
};

const SEAT_MARKER = {
  BTN: 'D',
  SB: 'SB',
  BB: 'BB',
};

const CONTINUE_OPENERS = ['EP', 'MP', 'CO', 'BTN'];
const OPEN_POSITION_IDS = POSITIONS.filter((p) => RANGE_DATA[p.id].kind === 'open').map((p) => p.id);

let activePositionId = 'BTN';
let activeStack = 100;
let compareMode = false;
let compareAxis = 'position'; // 'position' = gleicher Stack, unterschiedliche Positionen; 'stack' = gleiche Position, unterschiedliche Stacktiefen
let spotMode = false;
let chatMode = false;

function renderTable() {
  const table = document.getElementById('pokerTable');
  POSITIONS.forEach((pos) => {
    const coords = SEAT_COORDS[pos.id];
    const seat = document.createElement('button');
    seat.className = 'seat';
    seat.style.top = coords.top + '%';
    seat.style.left = coords.left + '%';
    seat.dataset.position = pos.id;
    if (SEAT_MARKER[pos.id]) seat.dataset.marker = SEAT_MARKER[pos.id];

    const badge = document.createElement('div');
    badge.className = 'seat-badge';
    badge.textContent = pos.short;
    seat.appendChild(badge);

    const marker = document.createElement('span');
    marker.className = 'seat-marker';
    marker.textContent = SEAT_MARKER[pos.id] || '';
    seat.appendChild(marker);

    seat.addEventListener('click', () => selectPosition(pos.id));
    table.appendChild(seat);
  });
}

function renderStackSelector() {
  const container = document.getElementById('stackSelector');
  STACK_DEPTHS.forEach((depth) => {
    const btn = document.createElement('button');
    btn.className = 'stack-btn';
    btn.textContent = depth + ' BB';
    btn.dataset.stack = depth;
    btn.addEventListener('click', () => {
      activeStack = depth;
      updateStackButtons();
      renderRange(activePositionId);
    });
    container.appendChild(btn);
  });
  updateStackButtons();
}

function updateStackButtons() {
  document.querySelectorAll('.stack-btn').forEach((btn) => {
    btn.classList.toggle('active', Number(btn.dataset.stack) === activeStack);
  });
}

function selectPosition(posId) {
  if (compareMode) setCompareMode(false);
  if (spotMode) setSpotMode(false);
  if (chatMode) setChatMode(false);
  activePositionId = posId;
  updateSeatActiveClasses();
  renderRange(posId);
}

function updateSeatActiveClasses() {
  document.querySelectorAll('.seat').forEach((seat) => {
    const isActive = !compareMode && !spotMode && !chatMode && seat.dataset.position === activePositionId;
    seat.classList.toggle('active', isActive);
    seat.style.setProperty('--seat-accent', RANGE_DATA[seat.dataset.position].accent);
  });
}

// Markiert die aktuell verglichenen Sitze am Tisch farblich (A/B bzw. beide Farben bei
// gleicher Position, unterschiedlichen Stacktiefen).
function updateCompareSeatHighlight() {
  document.querySelectorAll('.seat').forEach((seat) => {
    seat.classList.remove('cmp-a', 'cmp-b', 'cmp-dual');
  });
  if (!compareMode) return;

  const sel = getCompareSelection();
  if (compareAxis === 'stack') {
    const seat = document.querySelector(`.seat[data-position="${sel.posA}"]`);
    if (seat) seat.classList.add('cmp-dual');
  } else {
    const seatA = document.querySelector(`.seat[data-position="${sel.posA}"]`);
    const seatB = document.querySelector(`.seat[data-position="${sel.posB}"]`);
    if (sel.posA === sel.posB) {
      if (seatA) seatA.classList.add('cmp-dual');
    } else {
      if (seatA) seatA.classList.add('cmp-a');
      if (seatB) seatB.classList.add('cmp-b');
    }
  }
}

function renderRange(posId) {
  const data = RANGE_DATA[posId];

  document.getElementById('rangeTitle').textContent = data.title;
  document.getElementById('rangeSubtitle').textContent = data.subtitle;
  document.getElementById('rangeNote').textContent = data.note;
  document.getElementById('legendSwatch').style.background = data.accent;

  const gridEl = document.getElementById('rangeGrid');
  const legendEl = document.getElementById('gridLegend');
  const statsEl = document.getElementById('continueStats');
  const allinNoteEl = document.getElementById('allinNote');

  if (data.kind === 'open') {
    gridEl.style.display = '';
    legendEl.style.display = '';
    statsEl.style.display = 'none';
    renderOpenRaiseGrid(data, posId);
  } else {
    gridEl.style.display = 'none';
    legendEl.style.display = 'none';
    allinNoteEl.style.display = 'none';
    statsEl.style.display = '';
    renderContinueStats(data, posId);
  }
}

function renderOpenRaiseGrid(data, posId) {
  const { cells, totalCombos, allinCells: rawAllin } = buildOpenRaiseGrid(activeStack, data.group);
  // Die "*"-Markierung aus deiner Tabelle bezieht sich speziell auf BTNs Aktion (All-in statt
  // Raise) und ist nur beim Betrachten von BTN selbst aussagekräftig, auch wenn eine so markierte
  // Hand über die verschachtelten Ranges auch bei engeren Positionen enthalten sein kann.
  const allinCells = data.group === 'BTN' ? rawAllin : new Set();

  document.getElementById('rangeCombos').textContent = `${totalCombos} von ${TOTAL_COMBOS} Kombinationen`;
  document.getElementById('rangePercent').textContent = `${((totalCombos / TOTAL_COMBOS) * 100).toFixed(1)} %`;

  const grid = document.getElementById('rangeGrid');
  grid.innerHTML = '';
  for (let row = 0; row < 13; row++) {
    for (let col = 0; col < 13; col++) {
      const cell = document.createElement('div');
      cell.className = 'grid-cell';
      const key = `${row}-${col}`;
      cell.textContent = handCodeAt(row, col);
      if (cells.has(key)) {
        cell.classList.add('in-range');
        cell.style.background = data.accent;
        if (allinCells.has(key)) {
          cell.classList.add('all-in');
          cell.title = 'Laut deiner Tabelle: BTN geht bei 20BB hier All-in statt Raise.';
        }
      }
      grid.appendChild(cell);
    }
  }

  const allinNoteEl = document.getElementById('allinNote');
  const legendAllinEl = document.getElementById('legendAllin');
  if (allinCells.size > 0) {
    allinNoteEl.style.display = '';
    allinNoteEl.textContent = `Goldenes * = ${allinCells.size} Hand${allinCells.size === 1 ? '' : 'e'}, die deine Tabelle bei 20BB für BTN als All-in statt Raise kennzeichnet.`;
    legendAllinEl.style.display = 'flex';
  } else {
    allinNoteEl.style.display = 'none';
    legendAllinEl.style.display = 'none';
  }
}

function renderContinueStats(data, posId) {
  document.getElementById('rangeCombos').textContent = `Stack: ${activeStack} BB`;
  document.getElementById('rangePercent').textContent = '';

  const stats = CONTINUE_STATS[activeStack] || {};
  const statsEl = document.getElementById('continueStats');
  statsEl.innerHTML = '';

  CONTINUE_OPENERS.forEach((opener) => {
    const value = stats[opener] && stats[opener][posId];
    if (value === undefined) return;

    const row = document.createElement('div');
    row.className = 'stat-row';

    const label = document.createElement('span');
    label.className = 'stat-label';
    label.textContent = `vs. ${opener}-Open`;
    row.appendChild(label);

    const barTrack = document.createElement('div');
    barTrack.className = 'stat-bar-track';
    const bar = document.createElement('div');
    bar.className = 'stat-bar';
    bar.style.width = `${(value * 100).toFixed(1)}%`;
    bar.style.background = data.accent;
    barTrack.appendChild(bar);
    row.appendChild(barTrack);

    const pct = document.createElement('span');
    pct.className = 'stat-pct';
    pct.textContent = `${(value * 100).toFixed(1)} %`;
    row.appendChild(pct);

    statsEl.appendChild(row);
  });
}

function fillSelect(select, options, formatLabel) {
  select.innerHTML = '';
  options.forEach((opt) => {
    const el = document.createElement('option');
    el.value = opt;
    el.textContent = formatLabel(opt);
    select.appendChild(el);
  });
}

function setupCompareControls() {
  const sharedStack = document.getElementById('cmpSharedStackSelect');
  const posA = document.getElementById('cmpPosASelect');
  const posB = document.getElementById('cmpPosBSelect');
  const sharedPos = document.getElementById('cmpSharedPosSelect');
  const stackA = document.getElementById('cmpStackASelect');
  const stackB = document.getElementById('cmpStackBSelect');

  fillSelect(sharedStack, STACK_DEPTHS, (d) => d + ' BB');
  fillSelect(posA, OPEN_POSITION_IDS, (id) => POSITIONS.find((p) => p.id === id).label);
  fillSelect(posB, OPEN_POSITION_IDS, (id) => POSITIONS.find((p) => p.id === id).label);
  fillSelect(sharedPos, OPEN_POSITION_IDS, (id) => POSITIONS.find((p) => p.id === id).label);
  fillSelect(stackA, STACK_DEPTHS, (d) => d + ' BB');
  fillSelect(stackB, STACK_DEPTHS, (d) => d + ' BB');

  sharedStack.value = 100;
  posA.value = 'BTN';
  posB.value = 'UTG';
  sharedPos.value = 'BTN';
  stackA.value = 100;
  stackB.value = 20;

  [sharedStack, posA, posB, sharedPos, stackA, stackB].forEach((el) =>
    el.addEventListener('change', () => {
      renderCompare();
      updateCompareSeatHighlight();
    })
  );

  document.querySelectorAll('.cmp-axis-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      compareAxis = btn.dataset.axis;
      updateCompareAxisUI();
      renderCompare();
      updateCompareSeatHighlight();
    });
  });

  document.getElementById('compareToggle').addEventListener('click', () => {
    setCompareMode(!compareMode);
  });

  updateCompareAxisUI();
}

function updateCompareAxisUI() {
  document.querySelectorAll('.cmp-axis-btn').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.axis === compareAxis);
  });
  document.getElementById('pickerPosition').style.display = compareAxis === 'position' ? 'flex' : 'none';
  document.getElementById('pickerStack').style.display = compareAxis === 'stack' ? 'flex' : 'none';
}

// Liest die aktuelle Vergleichs-Auswahl aus, je nach Achse (Position oder Stacktiefe gemeinsam).
function getCompareSelection() {
  if (compareAxis === 'stack') {
    const pos = document.getElementById('cmpSharedPosSelect').value;
    return {
      posA: pos,
      posB: pos,
      stackA: Number(document.getElementById('cmpStackASelect').value),
      stackB: Number(document.getElementById('cmpStackBSelect').value),
    };
  }
  return {
    posA: document.getElementById('cmpPosASelect').value,
    posB: document.getElementById('cmpPosBSelect').value,
    stackA: Number(document.getElementById('cmpSharedStackSelect').value),
    stackB: Number(document.getElementById('cmpSharedStackSelect').value),
  };
}

function anyAltModeActive() {
  return compareMode || spotMode || chatMode;
}

function setCompareMode(on) {
  if (on && spotMode) setSpotMode(false);
  if (on && chatMode) setChatMode(false);
  compareMode = on;
  document.getElementById('singleView').style.display = on ? 'none' : '';
  document.getElementById('compareView').style.display = on ? 'block' : 'none';
  document.getElementById('stackSelector').style.display = anyAltModeActive() ? 'none' : '';
  document.getElementById('compareToggle').textContent = on ? 'Zurück zur Einzelansicht' : 'Ranges vergleichen';
  document.getElementById('compareToggle').classList.toggle('active', on);
  updateSeatActiveClasses();
  if (on) {
    renderCompare();
  }
  updateCompareSeatHighlight();
}

function setSpotMode(on) {
  if (on && compareMode) setCompareMode(false);
  if (on && chatMode) setChatMode(false);
  spotMode = on;
  document.getElementById('singleView').style.display = on ? 'none' : '';
  document.getElementById('spotView').style.display = on ? 'block' : 'none';
  document.getElementById('stackSelector').style.display = anyAltModeActive() ? 'none' : '';
  document.getElementById('spotToggle').textContent = on ? 'Zurück zur Einzelansicht' : 'Spot analysieren';
  document.getElementById('spotToggle').classList.toggle('active', on);
  updateSeatActiveClasses();
}

function setChatMode(on) {
  if (on && compareMode) setCompareMode(false);
  if (on && spotMode) setSpotMode(false);
  chatMode = on;
  document.getElementById('singleView').style.display = on ? 'none' : '';
  document.getElementById('chatView').style.display = on ? 'block' : 'none';
  document.getElementById('stackSelector').style.display = anyAltModeActive() ? 'none' : '';
  document.getElementById('chatToggle').textContent = on ? 'Zurück zur Einzelansicht' : 'Hand-Chat';
  document.getElementById('chatToggle').classList.toggle('active', on);
  updateSeatActiveClasses();
}

function renderCompare() {
  const { posA, posB, stackA, stackB } = getCompareSelection();

  const gridA = buildOpenRaiseGrid(stackA, RANGE_DATA[posA].group);
  const gridB = buildOpenRaiseGrid(stackB, RANGE_DATA[posB].group);

  const grid = document.getElementById('compareGrid');
  grid.innerHTML = '';

  let onlyACombos = 0;
  let onlyBCombos = 0;
  let bothCombos = 0;

  for (let row = 0; row < 13; row++) {
    for (let col = 0; col < 13; col++) {
      const key = `${row}-${col}`;
      const inA = gridA.cells.has(key);
      const inB = gridB.cells.has(key);
      const cell = document.createElement('div');
      cell.className = 'grid-cell';
      cell.textContent = handCodeAt(row, col);

      if (inA || inB) {
        cell.classList.add('in-range');
        const combos = combosAt(row, col);
        if (inA && inB) {
          cell.style.background = 'var(--cmp-both)';
          bothCombos += combos;
        } else if (inA) {
          cell.style.background = 'var(--cmp-a)';
          onlyACombos += combos;
        } else {
          cell.style.background = 'var(--cmp-b)';
          onlyBCombos += combos;
        }
      }
      grid.appendChild(cell);
    }
  }

  const pct = (c) => ((c / TOTAL_COMBOS) * 100).toFixed(1);
  const aLabel = `${POSITIONS.find((p) => p.id === posA).label} @ ${stackA}BB`;
  const bLabel = `${POSITIONS.find((p) => p.id === posB).label} @ ${stackB}BB`;
  document.getElementById('compareStats').innerHTML =
    `<strong>A</strong> = ${aLabel} (${gridA.totalCombos} Kombos, ${pct(gridA.totalCombos)} %) &nbsp;·&nbsp; ` +
    `<strong>B</strong> = ${bLabel} (${gridB.totalCombos} Kombos, ${pct(gridB.totalCombos)} %)<br>` +
    `Nur A: ${onlyACombos} Kombos (${pct(onlyACombos)} %) &nbsp;·&nbsp; ` +
    `Nur B: ${onlyBCombos} Kombos (${pct(onlyBCombos)} %) &nbsp;·&nbsp; ` +
    `Beide: ${bothCombos} Kombos (${pct(bothCombos)} %)`;
}

function setupSpotControls() {
  const stackSel = document.getElementById('spotStack');
  const heroSel = document.getElementById('spotHeroPos');
  const openerSel = document.getElementById('spotOpenerPos');
  const scenarioSel = document.getElementById('spotScenario');

  fillSelect(stackSel, STACK_DEPTHS, (d) => d + ' BB');
  fillSelect(heroSel, POSITIONS.map((p) => p.id), (id) => POSITIONS.find((p) => p.id === id).label);
  fillSelect(openerSel, POSITIONS.map((p) => p.id), (id) => POSITIONS.find((p) => p.id === id).label);
  stackSel.value = 100;
  heroSel.value = 'BTN';
  openerSel.value = 'UTG';

  document.getElementById('spotToggle').addEventListener('click', () => {
    setSpotMode(!spotMode);
  });

  scenarioSel.addEventListener('change', updateSpotOpenerVisibility);
  updateSpotOpenerVisibility();

  document.getElementById('spotAnalyzeBtn').addEventListener('click', () => {
    const text = document.getElementById('spotInput').value;
    const parsed = parseSpotText(text);

    scenarioSel.value = parsed.scenario;
    stackSel.value = parsed.stack || 100;
    if (parsed.heroPos) heroSel.value = parsed.heroPos;
    if (parsed.openerPos) openerSel.value = parsed.openerPos;
    document.getElementById('spotHand').value = parsed.hand || '';
    updateSpotOpenerVisibility();

    document.getElementById('spotParsed').classList.add('visible');
    renderSpotResult(null);
  });

  document.getElementById('spotConfirmBtn').addEventListener('click', () => {
    renderSpotResult({
      scenario: scenarioSel.value,
      stack: Number(stackSel.value),
      heroPos: heroSel.value,
      openerPos: openerSel.value,
      hand: document.getElementById('spotHand').value,
    });
  });
}

function updateSpotOpenerVisibility() {
  const scenario = document.getElementById('spotScenario').value;
  document.getElementById('spotOpenerRow').style.display = scenario === 'vs_open' ? 'flex' : 'none';
}

function renderSpotResult(input) {
  const resultEl = document.getElementById('spotResult');
  if (!input) {
    resultEl.innerHTML = '';
    resultEl.classList.remove('visible');
    return;
  }

  const heroLabel = POSITIONS.find((p) => p.id === input.heroPos).label;
  let html = '';

  if (input.scenario === 'other') {
    html = `<p class="spot-verdict spot-verdict-unknown">Für diesen Spot-Typ liegen in deiner Tabelle keine Daten vor (nur Open-Raise-Ranges und aggregierte Continue-Werte gegen Opens sind hinterlegt). Ich kann dazu keine verlässliche Aussage aus deinen Daten treffen.</p>`;
  } else if (input.scenario === 'rfi') {
    const data = RANGE_DATA[input.heroPos];
    if (data.kind !== 'open') {
      html = `<p class="spot-verdict spot-verdict-unknown">Für ${heroLabel} enthält deine Tabelle keine Hand-für-Hand-Open-Range (nur Continue-Werte gegen andere Positionen). Wähle oben ggf. den Spot-Typ „Gegen einen Open“.</p>`;
    } else {
      const cell = handToCell(input.hand);
      if (!cell) {
        html = `<p class="spot-verdict spot-verdict-unknown">„${escapeHtml(input.hand || '')}“ ist keine gültige Hand-Notation. Bitte im Format AKo, T9s oder 77 angeben.</p>`;
      } else {
        const { cells, totalCombos } = buildOpenRaiseGrid(input.stack, data.group);
        const key = `${cell.row}-${cell.col}`;
        const inRange = cells.has(key);
        const pct = ((totalCombos / TOTAL_COMBOS) * 100).toFixed(1);
        const handLabel = handCodeAt(cell.row, cell.col);
        html =
          `<p class="spot-verdict ${inRange ? 'spot-verdict-yes' : 'spot-verdict-no'}">` +
          `${inRange ? '✅ Raise' : '❌ Fold'} – ${handLabel} ist bei ${heroLabel} (${input.stack} BB) laut deiner Tabelle ` +
          `${inRange ? '' : 'NICHT '}in der Open-Range.</p>` +
          `<p class="spot-detail">${heroLabel} eröffnet bei ${input.stack} BB insgesamt ${totalCombos} von ${TOTAL_COMBOS} Kombinationen (${pct} %).</p>`;
      }
    }
  } else if (input.scenario === 'vs_open') {
    const openerLabel = POSITIONS.find((p) => p.id === input.openerPos).label;
    const openerGroup = toContinueGroup(input.openerPos);
    const heroGroup = toContinueGroup(input.heroPos);
    const stats = CONTINUE_STATS[input.stack] || {};
    const value = stats[openerGroup] && stats[openerGroup][heroGroup];
    if (value === undefined) {
      html = `<p class="spot-verdict spot-verdict-unknown">Für „${openerLabel} eröffnet, ${heroLabel} reagiert“ liegen bei ${input.stack} BB keine Daten in deiner Tabelle vor.</p>`;
    } else {
      const pct = (value * 100).toFixed(1);
      html =
        `<p class="spot-verdict spot-verdict-info">📊 Laut deiner Tabelle spielt ${heroLabel} bei ${input.stack} BB gegen einen ${openerLabel}-Open im Schnitt <strong>${pct} %</strong> der Hände weiter (Call oder 3-Bet zusammen).</p>` +
        `<p class="spot-detail">Deine Tabelle enthält dafür keine Hand-für-Hand-Aufschlüsselung – ob ${escapeHtml(input.hand || 'diese Hand')} konkret dazugehört, ist daraus nicht ablesbar. Nutze die Einzelansicht von ${heroLabel}, um die aggregierten Werte für alle Eröffner zu vergleichen.</p>`;
    }
  }

  resultEl.innerHTML = html;
  resultEl.classList.add('visible');
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

document.getElementById('chatToggle').addEventListener('click', () => {
  setChatMode(!chatMode);
});

renderTable();
renderStackSelector();
setupCompareControls();
setupSpotControls();
selectPosition(activePositionId);
