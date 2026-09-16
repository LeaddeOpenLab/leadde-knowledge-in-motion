const app = document.querySelector('#app');
const breadcrumb = document.querySelector('#breadcrumb');
let library = [];
let state = { subject: null, course: null };

const esc = value => String(value).replace(/[&<>"']/g, char => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[char]));
const courseLabel = item => item.course || 'Uncategorized';

function renderBreadcrumb() {
  const parts = [['All disciplines', () => state = { subject: null, course: null }]];
  if (state.subject) parts.push([state.subject, () => state = { subject: null, course: null }]);
  if (state.course) parts.push([state.course, null]);
  breadcrumb.innerHTML = parts.map(([name, action], index) => `${index ? '<span>/</span>' : ''}${action ? `<button data-crumb="${index}">${esc(name)}</button>` : `<span class="current">${esc(name)}</span>`}`).join('');
  breadcrumb.querySelectorAll('[data-crumb]').forEach(button => button.onclick = () => { parts[button.dataset.crumb][1](); render(); });
}

function card(name, count, index, detail = 'Explore this collection') {
  return `<button class="card" data-name="${esc(name)}"><span class="number">${String(index + 1).padStart(2, '0')} / ${count} PROMPTS</span><h2>${esc(name)}</h2><p>${esc(detail)}</p><span class="arrow">↘</span></button>`;
}

function render() {
  renderBreadcrumb();
  if (!state.subject) {
    const groups = Object.groupBy(library, item => item.subject);
    app.innerHTML = `<div class="grid">${Object.entries(groups).map(([name, items], index) => card(name, items.length, index)).join('')}</div>`;
    app.querySelectorAll('[data-name]').forEach(button => button.onclick = () => { state.subject = button.dataset.name; render(); });
    return;
  }
  if (!state.course) {
    const groups = Object.groupBy(library.filter(item => item.subject === state.subject), courseLabel);
    app.innerHTML = `<div class="grid">${Object.entries(groups).map(([name, items], index) => card(name, items.length, index, items[0].textbook || '未填写教材')).join('')}</div>`;
    app.querySelectorAll('[data-name]').forEach(button => button.onclick = () => { state.course = button.dataset.name; render(); });
    return;
  }
  const prompts = library.filter(item => item.subject === state.subject && courseLabel(item) === state.course);
  app.innerHTML = `<p class="course-meta">TEXTBOOK · ${esc(prompts[0]?.textbook || 'Not specified')}</p><div class="prompt-grid">${prompts.map(item => `<article class="prompt"><div class="preview">${item.status === 'ready' && item.video ? `<video controls preload="metadata" src="${esc(item.video)}"></video>` : '<span class="generating">VIDEO COMING SOON</span>'}</div><div class="prompt-body"><span class="status">${item.status === 'ready' ? 'VIDEO READY' : 'VIDEO COMING SOON'}</span><h2>${esc(item.title)}</h2><div class="tags">${(item.tags || []).filter(Boolean).map(tag => `<span class="tag">${esc(tag)}</span>`).join('')}</div><div class="prompt-text">${esc(item.prompt)}</div><a class="cta" href="https://leadde.ai" target="_blank" rel="noreferrer">Want a similar video? Create it at leadde.ai →</a></div></article>`).join('')}</div>`;
}

fetch('./data/prompts.json').then(response => response.json()).then(data => { library = data; render(); }).catch(() => { app.innerHTML = '<p class="empty">The resource catalog could not be loaded.</p>'; });
