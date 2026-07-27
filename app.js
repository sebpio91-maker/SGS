// Seat-Koordinaten (in % des Tisch-Containers) im Uhrzeigersinn.
const SEAT_COORDS = {
  UTG: { top: 15, left: 15 },
  UTG1: { top: 15, left: 50 },
  MP: { top: 15, left: 85 },
  HJ: { top: 50, left: 85 },
  CO: { top: 85, left: 85 },
  BTN: { top: 85, left: 50 },
  SB: { top: 85, left: 15 },
  BB: { top: 50, left: 15 },
};

const SEAT_MARKER = {
  BTN: 'D',
  SB: 'SB',
  BB: 'BB',
};

const CONTINUE_OPENERS = ['EP', 'MP', 'CO', 'BTN'];

let activePositionId = 'BTN';
let activeStack = 100;

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
  activePositionId = posId;
  document.querySelectorAll('.seat').forEach((seat) => {
    const isActive = seat.dataset.position === posId;
    seat.classList.toggle('active', isActive);
    seat.style.setProperty('--seat-accent', RANGE_DATA[seat.dataset.position].accent);
  });
  renderRange(posId);
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
  if (allinCells.size > 0) {
    allinNoteEl.style.display = '';
    allinNoteEl.textContent = `* markiert ${allinCells.size} Hand${allinCells.size === 1 ? '' : 'e'}, die deine Tabelle bei 20BB für BTN als All-in statt Raise kennzeichnet.`;
  } else {
    allinNoteEl.style.display = 'none';
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

renderTable();
renderStackSelector();
selectPosition(activePositionId);
