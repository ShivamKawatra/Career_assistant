const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const initSqlJs = require('sql.js');
const bcrypt = require('bcryptjs');
const session = require('express-session');

const app = express();
const DB_FILE = path.join(__dirname, 'notes.db');
let db;

app.use(cors());
app.use(express.json());
app.use(session({
  secret: 'notesapp_secret_key',
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 7 * 24 * 60 * 60 * 1000 }
}));
// Serve dashboard only when logged in
app.get('/dashboard', (req, res) => {
  if (!req.session.userId) return res.redirect('/login.html');
  res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

app.get('/profile.html', (req, res) => {
  if (!req.session.userId) return res.redirect('/login.html');
  res.sendFile(path.join(__dirname, 'public', 'profile.html'));
});

// Root → landing page (always public)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.use(express.static(path.join(__dirname, 'public')));

async function initDB() {
  const SQL = await initSqlJs();
  db = fs.existsSync(DB_FILE)
    ? new SQL.Database(fs.readFileSync(DB_FILE))
    : new SQL.Database();

  db.run(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
  )`);

  db.run(`CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT DEFAULT 'General',
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(user_id) REFERENCES users(id)
  )`);
  save();
}

function save() { fs.writeFileSync(DB_FILE, Buffer.from(db.export())); }

function all(q, p = []) {
  const s = db.prepare(q); s.bind(p);
  const rows = [];
  while (s.step()) rows.push(s.getAsObject());
  s.free(); return rows;
}
function get(q, p = []) { return all(q, p)[0] || null; }
function run(q, p = []) { db.run(q, p); save(); }

function auth(req, res, next) {
  if (!req.session.userId) return res.status(401).json({ error: 'Unauthorized' });
  next();
}

// ── Auth Routes ──────────────────────────────────────────────

app.post('/api/signup', async (req, res) => {
  const { name, email, password } = req.body;
  if (!name?.trim() || !email?.trim() || !password)
    return res.status(400).json({ error: 'All fields are required' });

  if (get('SELECT id FROM users WHERE email = ?', [email.trim()]))
    return res.status(409).json({ error: 'Email already registered' });

  const hash = await bcrypt.hash(password, 10);
  run('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
    [name.trim(), email.trim().toLowerCase(), hash]);

  const user = get('SELECT id, name, email FROM users WHERE email = ?', [email.trim().toLowerCase()]);
  req.session.userId = user.id;
  req.session.userName = user.name;
  res.status(201).json({ id: user.id, name: user.name, email: user.email });
});

app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email?.trim() || !password)
    return res.status(400).json({ error: 'Email and password are required' });

  const user = get('SELECT * FROM users WHERE email = ?', [email.trim().toLowerCase()]);
  if (!user || !(await bcrypt.compare(password, user.password)))
    return res.status(401).json({ error: 'Invalid email or password' });

  req.session.userId = user.id;
  req.session.userName = user.name;
  res.json({ id: user.id, name: user.name, email: user.email });
});

app.post('/api/logout', (req, res) => {
  req.session.destroy(() => res.json({ message: 'Logged out' }));
});

app.get('/api/me', (req, res) => {
  if (!req.session.userId) return res.status(401).json({ error: 'Not logged in' });
  const user = get('SELECT id, name, email, created_at FROM users WHERE id = ?', [req.session.userId]);
  res.json({ ...user, name: req.session.userName });
});

app.get('/api/me/stats', auth, (req, res) => {
  const total = get('SELECT COUNT(*) as c FROM notes WHERE user_id = ?', [req.session.userId])?.c || 0;
  const cats  = all('SELECT category, COUNT(*) as c FROM notes WHERE user_id = ? GROUP BY category ORDER BY c DESC', [req.session.userId]);
  const recent = all('SELECT title, updated_at FROM notes WHERE user_id = ? ORDER BY updated_at DESC LIMIT 5', [req.session.userId]);
  res.json({ total, categories: cats, recent });
});

// ── Notes Routes (auth protected) ────────────────────────────

app.get('/api/notes', auth, (req, res) => {
  const { search, category } = req.query;
  let q = 'SELECT * FROM notes WHERE user_id = ?';
  const p = [req.session.userId];

  if (search) { q += ' AND (title LIKE ? OR content LIKE ?)'; p.push(`%${search}%`, `%${search}%`); }
  if (category && category !== 'All') { q += ' AND category = ?'; p.push(category); }
  q += ' ORDER BY updated_at DESC';
  res.json(all(q, p));
});

app.get('/api/notes/:id', auth, (req, res) => {
  const note = get('SELECT * FROM notes WHERE id = ? AND user_id = ?', [req.params.id, req.session.userId]);
  if (!note) return res.status(404).json({ error: 'Note not found' });
  res.json(note);
});

app.post('/api/notes', auth, (req, res) => {
  const { title, content, category } = req.body;
  if (!title?.trim() || !content?.trim())
    return res.status(400).json({ error: 'Title and content are required' });

  run('INSERT INTO notes (user_id, title, content, category) VALUES (?, ?, ?, ?)',
    [req.session.userId, title.trim(), content.trim(), category?.trim() || 'General']);

  res.status(201).json(get('SELECT * FROM notes WHERE id = (SELECT MAX(id) FROM notes WHERE user_id = ?)', [req.session.userId]));
});

app.put('/api/notes/:id', auth, (req, res) => {
  const { title, content, category } = req.body;
  if (!title?.trim() || !content?.trim())
    return res.status(400).json({ error: 'Title and content are required' });

  const existing = get('SELECT id FROM notes WHERE id = ? AND user_id = ?', [req.params.id, req.session.userId]);
  if (!existing) return res.status(404).json({ error: 'Note not found' });

  run(`UPDATE notes SET title=?, content=?, category=?, updated_at=datetime('now') WHERE id=? AND user_id=?`,
    [title.trim(), content.trim(), category?.trim() || 'General', req.params.id, req.session.userId]);

  res.json(get('SELECT * FROM notes WHERE id = ?', [req.params.id]));
});

app.delete('/api/notes/:id', auth, (req, res) => {
  const existing = get('SELECT id FROM notes WHERE id = ? AND user_id = ?', [req.params.id, req.session.userId]);
  if (!existing) return res.status(404).json({ error: 'Note not found' });
  run('DELETE FROM notes WHERE id = ? AND user_id = ?', [req.params.id, req.session.userId]);
  res.json({ message: 'Note deleted' });
});

app.get('/api/categories', auth, (req, res) => {
  const rows = all('SELECT DISTINCT category FROM notes WHERE user_id = ? ORDER BY category', [req.session.userId]);
  res.json(rows.map(r => r.category));
});

initDB().then(() => app.listen(3000, () => console.log('Server running at http://localhost:3000')));
