import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { request } from './api';
import './styles.css';

const statuses = ['OPEN', 'IN_PROGRESS', 'RESOLVED'];
const priorities = ['LOW', 'MEDIUM', 'HIGH', 'URGENT'];
const label = value => value.toLowerCase().replaceAll('_', ' ').replace(/^./, s => s.toUpperCase());
const blank = { subject: '', description: '', requester: '', assignee: 'Unassigned', status: 'OPEN', priority: 'MEDIUM' };

function TicketForm({ ticket, onClose, onSaved }) {
  const [form, setForm] = useState(ticket ? Object.fromEntries(Object.keys(blank).map(k => [k, ticket[k]])) : blank);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const field = e => setForm({ ...form, [e.target.name]: e.target.value });
  async function save(e) {
    e.preventDefault(); setSaving(true); setError('');
    try { await request(ticket ? `/${ticket.id}` : '', { method: ticket ? 'PUT' : 'POST', body: JSON.stringify(form) }); await onSaved(); }
    catch (e) { setError(e.message); } finally { setSaving(false); }
  }
  return <div className="overlay"><section className="dialog" role="dialog" aria-modal="true" aria-labelledby="form-title">
    <div className="dialog-head"><div><small>SUPPORT REQUEST</small><h2 id="form-title">{ticket ? `Edit ticket #${ticket.id}` : 'Open a new ticket'}</h2></div><button onClick={onClose} aria-label="Close form">×</button></div>
    <form onSubmit={save}>
      <label>Subject<input autoFocus name="subject" value={form.subject} onChange={field} required maxLength={180} placeholder="What do you need help with?" /></label>
      <label>Details<textarea name="description" value={form.description} onChange={field} maxLength={10000} placeholder="Describe the issue and any steps you have tried." /></label>
      <div className="form-grid"><label>Requester<input name="requester" value={form.requester} onChange={field} required maxLength={120} placeholder="Name or team" /></label><label>Assigned to<input name="assignee" value={form.assignee} onChange={field} required maxLength={120} /></label>
      <label>Priority<select name="priority" value={form.priority} onChange={field}>{priorities.map(v => <option key={v}>{v}</option>)}</select></label>
      <label>Status<select name="status" value={form.status} onChange={field}>{statuses.map(v => <option key={v} value={v}>{label(v)}</option>)}</select></label></div>
      {error && <p role="alert" className="error">{error}</p>}
      <div className="form-actions"><button type="button" onClick={onClose}>Cancel</button><button className="primary" disabled={saving}>{saving ? 'Saving…' : ticket ? 'Save changes' : 'Create ticket'}</button></div>
    </form>
  </section></div>;
}

function App() {
  const [tickets, setTickets] = useState([]);
  const [filter, setFilter] = useState('ALL');
  const [search, setSearch] = useState('');
  const [editor, setEditor] = useState(undefined);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [busy, setBusy] = useState(null);
  async function load() {
    try { setTickets(await request()); setError(''); }
    catch (e) { setError(e.message); } finally { setLoading(false); }
  }
  useEffect(() => { load(); }, []);
  async function changeStatus(ticket, status) {
    setBusy(ticket.id);
    const data = Object.fromEntries(Object.keys(blank).map(k => [k, ticket[k]]));
    try { await request(`/${ticket.id}`, { method: 'PUT', body: JSON.stringify({ ...data, status }) }); await load(); setNotice(`Ticket #${ticket.id} updated.`); }
    catch (e) { setError(e.message); } finally { setBusy(null); }
  }
  async function remove(ticket) {
    if (!window.confirm(`Delete ticket #${ticket.id}: ${ticket.subject}?`)) return;
    setBusy(ticket.id);
    try { await request(`/${ticket.id}`, { method: 'DELETE' }); await load(); setNotice(`Ticket #${ticket.id} deleted.`); }
    catch (e) { setError(e.message); } finally { setBusy(null); }
  }
  const visible = tickets.filter(t => (filter === 'ALL' || t.status === filter) && `${t.subject} ${t.requester} ${t.assignee} ${t.id}`.toLowerCase().includes(search.toLowerCase()));
  const active = tickets.filter(t => t.status !== 'RESOLVED');
  return <div className="workspace">
    <aside className="rail"><a className="brand" href="/" aria-label="Relaydesk home"><span className="logo">r.</span><span>relaydesk<small>SUPPORT WORKSPACE</small></span></a><div className="rail-label">WORKSPACE</div><button className="nav-active" onClick={() => { setFilter('ALL'); setSearch(''); }}>▤ &nbsp; Ticket inbox <span>{tickets.length}</span></button><div className="rail-note"><span className="signal" /> Support, in good hands.<p>One place to track every request, from the first message to the final fix.</p></div><div className="agent"><span>P</span><div>Pranav<small>Support engineer</small></div></div></aside>
    <main><div className="topline"><span>Workspace <b>/</b> Ticket inbox</span><span className="workspace-badge">RELAYDESK / 01</span></div>
      <header><div><div className="eyebrow">KEEP WORK MOVING</div><h1>A little clarity.<br /><em>A lot less back-and-forth.</em></h1><p>Your team's requests, priorities, and resolutions in one place.</p></div><button className="primary" onClick={() => setEditor(null)}>＋ New ticket</button></header>
      <section className="summary" aria-label="Ticket summary">{[['All requests', tickets.length, 'Every conversation counts'], ['Needs attention', active.length, 'Open or in progress'], ['High priority', active.filter(t => ['HIGH', 'URGENT'].includes(t.priority)).length, 'Keep these moving'], ['Resolved', tickets.filter(t => t.status === 'RESOLVED').length, 'A job well done']].map(([name, value, hint]) => <article key={name}><small>{name}</small><strong>{value}</strong><span>{hint}</span></article>)}</section>
      {error && <div className="error" role="alert">{error} <button onClick={load}>Retry connection</button></div>}
      {notice && <p className="notice" role="status">{notice}</p>}
      <section className="inbox"><div className="inbox-head"><div><h2>Ticket inbox <span>{visible.length}</span></h2><p>Pick up a request. Make someone's day easier.</p></div><input className="search" aria-label="Search tickets" placeholder="Search tickets, people, or ID…" value={search} onChange={e => setSearch(e.target.value)} /></div>
      <div className="tabs" aria-label="Filter by status">{['ALL', ...statuses].map(s => <button key={s} aria-pressed={filter === s} className={filter === s ? 'selected' : ''} onClick={() => setFilter(s)}>{s === 'ALL' ? 'All tickets' : label(s)}</button>)}</div>
      {loading ? <div className="empty" role="status">Loading your inbox…</div> : visible.length === 0 ? <div className="empty"><div className="empty-icon">✉</div><h3>{tickets.length ? 'No tickets match this view' : 'A clear inbox. A fresh start.'}</h3><p>{tickets.length ? 'Try another status or search term.' : 'Create your first ticket to start helping your team.'}</p><button onClick={() => setEditor(null)}>Open a ticket ↗</button></div> : <div className="table-scroll"><table><thead><tr><th>Request</th><th>Requester / owner</th><th>Priority</th><th>Status</th><th>Actions</th></tr></thead><tbody>{visible.map(t => <tr key={t.id}><td><button className="ticket-link" onClick={() => setEditor(t)}><small>RD-{String(t.id).padStart(4, '0')}</small><strong>{t.subject}</strong></button><p className="description">{t.description || 'No additional details'}</p></td><td><div className="person">{t.requester}</div><small className="muted">↳ {t.assignee}</small></td><td><span className={`priority ${t.priority.toLowerCase()}`}><i />{label(t.priority)}</span></td><td><select aria-label={`Status for ticket ${t.id}`} className={`status ${t.status.toLowerCase()}`} disabled={busy === t.id} value={t.status} onChange={e => changeStatus(t, e.target.value)}>{statuses.map(s => <option key={s} value={s}>{label(s)}</option>)}</select></td><td><div className="actions"><button onClick={() => setEditor(t)} disabled={busy === t.id}>Edit</button><button className="delete" onClick={() => remove(t)} disabled={busy === t.id}>Delete</button></div></td></tr>)}</tbody></table></div>}
      </section><footer>RELAYDESK <span>Thoughtful support. Clear outcomes.</span></footer>
    </main>{editor !== undefined && <TicketForm ticket={editor} onClose={() => setEditor(undefined)} onSaved={async () => { setEditor(undefined); await load(); setNotice('Ticket saved.'); }} />}
  </div>;
}
createRoot(document.getElementById('root')).render(<App />);
