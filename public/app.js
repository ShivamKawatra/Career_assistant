const API = '/api/notes';
let notes = [], activeId = null;

const $ = id => document.getElementById(id);

const notesList    = $('notesList');
const emptyState   = $('emptyState');
const searchInput  = $('searchInput');
const catFilter    = $('categoryFilter');
const editorForm   = $('editorForm');
const noteView     = $('noteView');
const editorActions= $('editorActions');
const editorTitle  = $('editorTitle');
const noteTitle    = $('noteTitle');
const noteContent  = $('noteContent');
const noteCategory = $('noteCategory');
const titleError   = $('titleError');
const contentError = $('contentError');

// ── Auth check ───────────────────────────────────
async function checkAuth() {
  const res = await fetch('/api/me');
  if (!res.ok) { window.location.replace('/login.html'); return false; }
  const user = await res.json();
  $('navUser').textContent = `👤 ${user.name}`;
  $('userGreeting').textContent = `Hello, ${user.name.split(' ')[0]} 👋`;
  return true;
}

async function logout() {
  await fetch('/api/logout', { method: 'POST' });
  window.location.replace('/');
}

// ── Toast ────────────────────────────────────────
function toast(msg, type = 'success') {
  const t = $('toast');
  t.textContent = msg;
  t.className = `toast show${type === 'error' ? ' error' : ''}`;
  setTimeout(() => t.className = 'toast', 2500);
}

function fmtDate(dt) {
  return new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

// ── Load notes ───────────────────────────────────
async function loadNotes() {
  const search = searchInput.value.trim();
  const category = catFilter.value;
  const params = new URLSearchParams();
  if (search) params.set('search', search);
  if (category !== 'All') params.set('category', category);

  const res = await fetch(`${API}?${params}`);
  if (res.status === 401) { window.location.href = '/login.html'; return; }
  notes = await res.json();
  renderList();
  await loadCategories();
}

function renderList() {
  notesList.innerHTML = '';
  if (!notes.length) {
    notesList.appendChild(emptyState);
    emptyState.style.display = 'block';
    $('stats').textContent = '0 notes';
    return;
  }
  emptyState.style.display = 'none';
  $('stats').textContent = `${notes.length} note${notes.length !== 1 ? 's' : ''}`;

  notes.forEach(n => {
    const card = document.createElement('div');
    card.className = `note-card${n.id === activeId ? ' active' : ''}`;
    card.innerHTML = `
      <div class="note-card-title">${escHtml(n.title)}</div>
      <div class="note-card-preview">${escHtml(n.content)}</div>
      <div class="note-card-footer">
        <span class="badge">${escHtml(n.category)}</span>
        <span class="note-date">${fmtDate(n.updated_at)}</span>
      </div>`;
    card.addEventListener('click', () => viewNote(n.id));
    notesList.appendChild(card);
  });
}

async function loadCategories() {
  const res = await fetch('/api/categories');
  const cats = await res.json();
  const current = catFilter.value;
  catFilter.innerHTML = '<option value="All">All</option>';
  cats.forEach(c => {
    const o = document.createElement('option');
    o.value = o.textContent = c;
    catFilter.appendChild(o);
  });
  catFilter.value = current;
}

// ── View note ────────────────────────────────────
async function viewNote(id) {
  activeId = id;
  const res = await fetch(`${API}/${id}`);
  const note = await res.json();

  editorTitle.textContent = 'Viewing Note';
  editorForm.style.display = 'none';
  noteView.style.display = 'flex';
  editorActions.style.display = 'flex';
  $('viewTitle').textContent = note.title;
  $('viewContent').textContent = note.content;
  $('viewCategory').textContent = note.category;
  $('viewDate').textContent = fmtDate(note.updated_at);
  $('saveBtn').style.display = 'none';
  $('deleteBtn').style.display = '';
  $('cancelBtn').style.display = '';
  renderList();
}

// ── New note ─────────────────────────────────────
function newNote() {
  activeId = null;
  editorTitle.textContent = 'New Note';
  noteView.style.display = 'none';
  editorForm.style.display = 'flex';
  editorActions.style.display = 'flex';
  noteTitle.value = ''; noteContent.value = ''; noteCategory.value = 'General';
  titleError.textContent = ''; contentError.textContent = '';
  $('saveBtn').style.display = '';
  $('deleteBtn').style.display = 'none';
  $('cancelBtn').style.display = '';
  noteTitle.focus();
}

// ── Edit note ────────────────────────────────────
async function editNote() {
  const res = await fetch(`${API}/${activeId}`);
  const note = await res.json();
  editorTitle.textContent = 'Edit Note';
  noteView.style.display = 'none';
  editorForm.style.display = 'flex';
  noteTitle.value = note.title;
  noteContent.value = note.content;
  noteCategory.value = note.category;
  titleError.textContent = ''; contentError.textContent = '';
  $('saveBtn').style.display = '';
  $('deleteBtn').style.display = '';
  $('cancelBtn').style.display = '';
  noteTitle.focus();
}

// ── Validate ─────────────────────────────────────
function validate() {
  let valid = true;
  titleError.textContent = ''; contentError.textContent = '';
  if (!noteTitle.value.trim()) { titleError.textContent = 'Title is required.'; valid = false; }
  if (!noteContent.value.trim()) { contentError.textContent = 'Content is required.'; valid = false; }
  return valid;
}

// ── Save note ────────────────────────────────────
async function saveNote() {
  if (!validate()) return;
  const isNew = !activeId;
  const body = { title: noteTitle.value.trim(), content: noteContent.value.trim(), category: noteCategory.value };
  const res = await fetch(activeId ? `${API}/${activeId}` : API, {
    method: activeId ? 'PUT' : 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  if (!res.ok) { toast((await res.json()).error, 'error'); return; }
  const saved = await res.json();
  activeId = saved.id;
  toast(isNew ? 'Note created!' : 'Note updated!');
  await loadNotes();
  viewNote(activeId);
}

// ── Delete note ──────────────────────────────────
async function deleteNote() {
  if (!activeId) return;
  if (!confirm('Delete this note?')) return;
  const res = await fetch(`${API}/${activeId}`, { method: 'DELETE' });
  if (!res.ok) { toast('Failed to delete', 'error'); return; }
  activeId = null;
  resetEditor();
  await loadNotes();
  toast('Note deleted!');
}

function cancelEdit() { activeId ? viewNote(activeId) : resetEditor(); }

function resetEditor() {
  editorTitle.textContent = 'Select or create a note';
  editorForm.style.display = 'none';
  noteView.style.display = 'none';
  editorActions.style.display = 'none';
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function debounce(fn, ms) {
  let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
}

// ── Events ───────────────────────────────────────
$('newNoteBtn').addEventListener('click', newNote);
$('navNewNote').addEventListener('click', e => { e.preventDefault(); newNote(); });

$('logoutBtn').addEventListener('click', logout);
$('saveBtn').addEventListener('click', saveNote);
$('deleteBtn').addEventListener('click', deleteNote);
$('cancelBtn').addEventListener('click', cancelEdit);
$('editBtn').addEventListener('click', editNote);
if ($('profileBtn')) $('profileBtn').addEventListener('click', () => window.location.href = '/profile.html');
searchInput.addEventListener('input', debounce(loadNotes, 300));
catFilter.addEventListener('change', loadNotes);

// ── Init ─────────────────────────────────────────
checkAuth().then(ok => { if (ok) loadNotes(); });
