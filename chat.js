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

function defaultTitle(suffix) {
  const stamp = new Date().toLocaleString('de-DE', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
  return suffix ? `Hand vom ${stamp} (${suffix})` : `Hand vom ${stamp}`;
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

async function uploadImage(file, pathPrefix) {
  if (!file) return null;
  if (file.size > MAX_IMAGE_BYTES) {
    alert(`Das Bild "${file.name}" ist größer als 8 MB und wird übersprungen.`);
    return null;
  }
  const path = `${pathPrefix}/${Date.now()}_${file.name}`;
  const storageRef = fb.ref(storage, path);
  await fb.uploadBytes(storageRef, file);
  return fb.getDownloadURL(storageRef);
}

async function uploadImageIfAny(fileInput, pathPrefix) {
  const file = fileInput.files && fileInput.files[0];
  const url = await uploadImage(file, pathPrefix);
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
    const item = document.createElement('div');
    item.className = 'chat-thread-item';

    const openBtn = document.createElement('button');
    openBtn.type = 'button';
    openBtn.className = 'chat-thread-item-open';
    openBtn.innerHTML =
      `<span class="chat-thread-item-title">${escapeHtml(data.title || 'Ohne Titel')}</span>` +
      `<span class="chat-thread-item-meta">von ${escapeHtml(data.author || 'Anonym')} · ${formatTimestamp(data.createdAt)}</span>`;
    openBtn.addEventListener('click', () => openThread(docSnap.id, data.title));

    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.className = 'chat-thread-item-delete';
    deleteBtn.title = 'Thread löschen';
    deleteBtn.textContent = '🗑';
    deleteBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      deleteThread(docSnap.id, data.title);
    });

    item.appendChild(openBtn);
    item.appendChild(deleteBtn);
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
  hideEditTitle();

  if (unsubscribeMessages) unsubscribeMessages();
  const q = fb.query(fb.collection(db, 'threads', id, 'messages'), fb.orderBy('createdAt', 'asc'));
  unsubscribeMessages = fb.onSnapshot(q, renderMessages);
}

function backToList() {
  currentThreadId = null;
  if (unsubscribeMessages) unsubscribeMessages();
  document.getElementById('chatThreadListPane').style.display = '';
  document.getElementById('chatThreadDetailPane').classList.remove('visible');
  hideEditTitle();
}

function showEditTitle() {
  const currentTitle = document.getElementById('chatThreadTitle').textContent;
  document.getElementById('chatEditTitleInput').value = currentTitle;
  document.getElementById('chatEditTitleForm').classList.add('visible');
  document.getElementById('chatEditTitleInput').focus();
}

function hideEditTitle() {
  document.getElementById('chatEditTitleForm').classList.remove('visible');
}

async function saveTitle() {
  const newTitle = document.getElementById('chatEditTitleInput').value.trim();
  if (!newTitle || !currentThreadId) return;
  await fb.updateDoc(fb.doc(db, 'threads', currentThreadId), { title: newTitle });
  document.getElementById('chatThreadTitle').textContent = newTitle;
  hideEditTitle();
}

async function deleteThread(id, title) {
  const ok = confirm(`Thread "${title || 'Ohne Titel'}" wirklich löschen? Das betrifft alle Nachrichten und Bilder darin und kann nicht rückgängig gemacht werden.`);
  if (!ok) return;

  const messagesSnap = await fb.getDocs(fb.collection(db, 'threads', id, 'messages'));
  await Promise.all(messagesSnap.docs.map((d) => fb.deleteDoc(d.ref)));

  try {
    const folderRef = fb.ref(storage, `thread-images/${id}`);
    const listing = await fb.listAll(folderRef);
    await Promise.all(listing.items.map((item) => fb.deleteObject(item)));
  } catch (err) {
    // Bild-Löschung ist best-effort (z.B. falls die Storage-Regeln noch die
    // alte Version ohne "list"/"delete" haben) -- der Thread wird trotzdem
    // gelöscht, es blieben dann höchstens verwaiste Bilddateien liegen.
  }

  await fb.deleteDoc(fb.doc(db, 'threads', id));

  if (currentThreadId === id) backToList();
}

async function createSingleThread(title, text, file, author) {
  const threadRef = await fb.addDoc(fb.collection(db, 'threads'), {
    title,
    author,
    createdAt: fb.serverTimestamp(),
  });

  const imageUrl = await uploadImage(file, `thread-images/${threadRef.id}`);
  if (text || imageUrl) {
    await fb.addDoc(fb.collection(db, 'threads', threadRef.id, 'messages'), {
      author,
      text: text || null,
      imageUrl: imageUrl || null,
      createdAt: fb.serverTimestamp(),
    });
  }

  return threadRef.id;
}

async function createThread() {
  const text = document.getElementById('chatNewText').value.trim();
  const imageInput = document.getElementById('chatNewImage');
  const files = Array.from(imageInput.files || []);
  const author = ensureDisplayName();

  if (!text && files.length === 0) {
    alert('Bitte einen Text eingeben oder mindestens ein Bild auswählen.');
    return;
  }

  document.getElementById('chatNewText').value = '';
  imageInput.value = '';

  if (files.length > 1) {
    for (let i = 0; i < files.length; i++) {
      await createSingleThread(defaultTitle(`${i + 1}/${files.length}`), text, files[i], author);
    }
    backToList();
  } else {
    const title = defaultTitle();
    const threadId = await createSingleThread(title, text, files[0] || null, author);
    openThread(threadId, title);
  }
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
  document.getElementById('chatEditTitleBtn').addEventListener('click', showEditTitle);
  document.getElementById('chatCancelTitleBtn').addEventListener('click', hideEditTitle);
  document.getElementById('chatSaveTitleBtn').addEventListener('click', saveTitle);
  document.getElementById('chatDeleteThreadBtn').addEventListener('click', () => {
    if (!currentThreadId) return;
    deleteThread(currentThreadId, document.getElementById('chatThreadTitle').textContent);
  });

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
    doc: storeMod.doc,
    updateDoc: storeMod.updateDoc,
    deleteDoc: storeMod.deleteDoc,
    getDocs: storeMod.getDocs,
    query: storeMod.query,
    orderBy: storeMod.orderBy,
    onSnapshot: storeMod.onSnapshot,
    serverTimestamp: storeMod.serverTimestamp,
    getStorage: storageMod.getStorage,
    ref: storageMod.ref,
    uploadBytes: storageMod.uploadBytes,
    getDownloadURL: storageMod.getDownloadURL,
    listAll: storageMod.listAll,
    deleteObject: storageMod.deleteObject,
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
