// Hand-Chat: Threads pro Hand mit Freunden, inkl. Bild-Upload. Nutzt Firebase
// (Firestore für Threads/Nachrichten, Storage für Bilder, anonyme
// Authentifizierung nur damit die Sicherheitsregeln greifen -- für die
// Nutzer:innen ist davon nichts sichtbar, es gibt keinen Login-Screen).
//
// Die Firebase-SDK-Module werden bewusst NICHT statisch importiert: ein
// statischer `import` von gstatic.com würde bei jedem Laden dieser Datei
// versucht, selbst wenn Firebase noch gar nicht eingerichtet ist -- ohne
// Internetzugriff würde dann das ganze Modul (inkl. des "noch nicht
// eingerichtet"-Hinweises) mit einem Fehler abbrechen. Stattdessen wird das
// SDK per dynamic import() erst geladen, wenn firebase-config.js echte Werte
// enthält.
import { firebaseConfig } from './firebase-config.js';

const FIREBASE_SDK_VERSION = '10.14.1';
const MAX_IMAGE_BYTES = 8 * 1024 * 1024;
const isConfigured = Boolean(firebaseConfig.apiKey) && !firebaseConfig.apiKey.startsWith('DEIN_');

const fb = {}; // wird beim Init mit den benötigten Firebase-SDK-Funktionen befüllt
let db = null;
let storage = null;
let currentThreadId = null;
let unsubscribeMessages = null;

function getDisplayName() {
  return localStorage.getItem('handChatName') || '';
}

function ensureDisplayName() {
  let name = getDisplayName();
  if (!name) {
    name = (prompt('Wie sollen dich deine Freunde im Hand-Chat sehen?', '') || '').trim() || 'Anonym';
    localStorage.setItem('handChatName', name);
  }
  document.getElementById('chatDisplayName').textContent = getDisplayName();
  return getDisplayName();
}

function formatTimestamp(ts) {
  if (!ts || !ts.toDate) return '';
  return ts.toDate().toLocaleString('de-DE', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

async function uploadImageIfAny(fileInput, pathPrefix) {
  const file = fileInput.files && fileInput.files[0];
  if (!file) return null;
  if (file.size > MAX_IMAGE_BYTES) {
    alert('Das Bild ist größer als 8 MB. Bitte ein kleineres Bild wählen.');
    return null;
  }
  const path = `${pathPrefix}/${Date.now()}_${file.name}`;
  const storageRef = fb.ref(storage, path);
  await fb.uploadBytes(storageRef, file);
  const url = await fb.getDownloadURL(storageRef);
  fileInput.value = '';
  return url;
}

function renderThreadList(snapshot) {
  const listEl = document.getElementById('chatThreadList');
  listEl.innerHTML = '';
  if (snapshot.empty) {
    listEl.innerHTML = '<p class="chat-empty">Noch keine Threads – eröffne den ersten oben.</p>';
    return;
  }
  snapshot.forEach((docSnap) => {
    const data = docSnap.data();
    const item = document.createElement('button');
    item.type = 'button';
    item.className = 'chat-thread-item';
    item.innerHTML =
      `<span class="chat-thread-item-title">${escapeHtml(data.title || 'Ohne Titel')}</span>` +
      `<span class="chat-thread-item-meta">von ${escapeHtml(data.author || 'Anonym')} · ${formatTimestamp(data.createdAt)}</span>`;
    item.addEventListener('click', () => openThread(docSnap.id, data.title));
    listEl.appendChild(item);
  });
}

function renderMessages(snapshot) {
  const el = document.getElementById('chatMessages');
  el.innerHTML = '';
  snapshot.forEach((docSnap) => {
    const m = docSnap.data();
    const row = document.createElement('div');
    row.className = 'chat-message';
    let inner = `<div class="chat-message-head"><strong>${escapeHtml(m.author || 'Anonym')}</strong> <span>${formatTimestamp(m.createdAt)}</span></div>`;
    if (m.text) inner += `<p class="chat-message-text">${escapeHtml(m.text)}</p>`;
    if (m.imageUrl) inner += `<img class="chat-message-image" src="${m.imageUrl}" alt="Hochgeladenes Bild">`;
    row.innerHTML = inner;
    el.appendChild(row);
  });
  el.scrollTop = el.scrollHeight;
}

function openThread(id, title) {
  currentThreadId = id;
  document.getElementById('chatThreadTitle').textContent = title || '';
  document.getElementById('chatThreadListPane').style.display = 'none';
  document.getElementById('chatThreadDetailPane').classList.add('visible');

  if (unsubscribeMessages) unsubscribeMessages();
  const q = fb.query(fb.collection(db, 'threads', id, 'messages'), fb.orderBy('createdAt', 'asc'));
  unsubscribeMessages = fb.onSnapshot(q, renderMessages);
}

function backToList() {
  currentThreadId = null;
  if (unsubscribeMessages) unsubscribeMessages();
  document.getElementById('chatThreadListPane').style.display = '';
  document.getElementById('chatThreadDetailPane').classList.remove('visible');
}

async function createThread() {
  const title = document.getElementById('chatNewTitle').value.trim();
  if (!title) {
    alert('Bitte einen Titel für den Thread eingeben.');
    return;
  }
  const text = document.getElementById('chatNewText').value.trim();
  const imageInput = document.getElementById('chatNewImage');
  const author = ensureDisplayName();

  const threadRef = await fb.addDoc(fb.collection(db, 'threads'), {
    title,
    author,
    createdAt: fb.serverTimestamp(),
  });

  const imageUrl = await uploadImageIfAny(imageInput, `thread-images/${threadRef.id}`);
  if (text || imageUrl) {
    await fb.addDoc(fb.collection(db, 'threads', threadRef.id, 'messages'), {
      author,
      text: text || null,
      imageUrl: imageUrl || null,
      createdAt: fb.serverTimestamp(),
    });
  }

  document.getElementById('chatNewTitle').value = '';
  document.getElementById('chatNewText').value = '';
  openThread(threadRef.id, title);
}

async function sendMessage() {
  if (!currentThreadId) return;
  const textEl = document.getElementById('chatMessageText');
  const imageInput = document.getElementById('chatMessageImage');
  const text = textEl.value.trim();
  const author = ensureDisplayName();

  const imageUrl = await uploadImageIfAny(imageInput, `thread-images/${currentThreadId}`);
  if (!text && !imageUrl) return;

  await fb.addDoc(fb.collection(db, 'threads', currentThreadId, 'messages'), {
    author,
    text: text || null,
    imageUrl: imageUrl || null,
    createdAt: fb.serverTimestamp(),
  });
  textEl.value = '';
}

function initChatUi() {
  document.getElementById('chatChangeName').addEventListener('click', () => {
    localStorage.removeItem('handChatName');
    ensureDisplayName();
  });
  document.getElementById('chatCreateThreadBtn').addEventListener('click', createThread);
  document.getElementById('chatSendBtn').addEventListener('click', sendMessage);
  document.getElementById('chatBackToList').addEventListener('click', backToList);

  const q = fb.query(fb.collection(db, 'threads'), fb.orderBy('createdAt', 'desc'));
  fb.onSnapshot(q, renderThreadList);
}

async function loadFirebaseSdk() {
  const base = `https://www.gstatic.com/firebasejs/${FIREBASE_SDK_VERSION}`;
  const [appMod, authMod, storeMod, storageMod] = await Promise.all([
    import(/* webpackIgnore: true */ `${base}/firebase-app.js`),
    import(/* webpackIgnore: true */ `${base}/firebase-auth.js`),
    import(/* webpackIgnore: true */ `${base}/firebase-firestore.js`),
    import(/* webpackIgnore: true */ `${base}/firebase-storage.js`),
  ]);
  Object.assign(fb, {
    initializeApp: appMod.initializeApp,
    getAuth: authMod.getAuth,
    signInAnonymously: authMod.signInAnonymously,
    onAuthStateChanged: authMod.onAuthStateChanged,
    getFirestore: storeMod.getFirestore,
    collection: storeMod.collection,
    addDoc: storeMod.addDoc,
    query: storeMod.query,
    orderBy: storeMod.orderBy,
    onSnapshot: storeMod.onSnapshot,
    serverTimestamp: storeMod.serverTimestamp,
    getStorage: storageMod.getStorage,
    ref: storageMod.ref,
    uploadBytes: storageMod.uploadBytes,
    getDownloadURL: storageMod.getDownloadURL,
  });
}

async function init() {
  const notice = document.getElementById('chatSetupNotice');
  const main = document.getElementById('chatMain');

  if (!isConfigured) {
    notice.style.display = 'block';
    main.style.display = 'none';
    return;
  }

  notice.style.display = 'none';
  main.style.display = '';

  try {
    await loadFirebaseSdk();
  } catch (err) {
    main.innerHTML = `<p class="chat-empty">Firebase-SDK konnte nicht geladen werden (keine Internetverbindung?): ${escapeHtml(err.message)}</p>`;
    return;
  }

  const app = fb.initializeApp(firebaseConfig);
  const auth = fb.getAuth(app);
  db = fb.getFirestore(app);
  storage = fb.getStorage(app);

  fb.onAuthStateChanged(auth, (user) => {
    if (user) {
      ensureDisplayName();
      initChatUi();
    }
  });
  fb.signInAnonymously(auth).catch((err) => {
    main.innerHTML = `<p class="chat-empty">Verbindung zu Firebase fehlgeschlagen: ${escapeHtml(err.message)}. Prüfe firebase-config.js und ob "Anonyme Anmeldung" in der Firebase-Konsole aktiviert ist.</p>`;
  });
}

init();
