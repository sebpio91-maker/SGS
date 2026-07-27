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

let activePositionId = 'BTN';

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
  const { cells, totalCombos } = buildRangeGrid(data.tokens);

  document.getElementById('rangeTitle').textContent = data.title;
  document.getElementById('rangeSubtitle').textContent = data.subtitle;
  document.getElementById('rangeNote').textContent = data.note;
  document.getElementById('rangeCombos').textContent = `${totalCombos} von ${TOTAL_COMBOS} Kombinationen`;
  document.getElementById('rangePercent').textContent = `${((totalCombos / TOTAL_COMBOS) * 100).toFixed(1)} %`;
  document.getElementById('legendSwatch').style.background = data.accent;

  const grid = document.getElementById('rangeGrid');
  grid.innerHTML = '';
  for (let row = 0; row < 13; row++) {
    for (let col = 0; col < 13; col++) {
      const cell = document.createElement('div');
      cell.className = 'grid-cell';
      const label = cellLabel(row, col);
      cell.textContent = label;
      const hand = cells.get(`${row}-${col}`);
      if (hand) {
        cell.classList.add('in-range');
        cell.style.background = data.accent;
      }
      grid.appendChild(cell);
    }
  }
}

function cellLabel(row, col) {
  if (row === col) return RANKS[row] + RANKS[row];
  if (row < col) return RANKS[row] + RANKS[col] + 's';
  return RANKS[col] + RANKS[row] + 'o';
}

renderTable();
selectPosition(activePositionId);
