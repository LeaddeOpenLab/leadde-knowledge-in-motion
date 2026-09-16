const app = document.querySelector('#app');
const breadcrumb = document.querySelector('#breadcrumb');
let videos = [];
let activeCourse = null;

const esc = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));

function render() {
  const courses = Object.groupBy(videos, video => video.course);
  breadcrumb.innerHTML = activeCourse
    ? `<button type="button" id="all-videos">All Mathematics Videos</button><span>/</span><span class="current">${esc(activeCourse)}</span>`
    : '<span class="current">Mathematics Videos</span>';
  document.querySelector('#all-videos')?.addEventListener('click', () => { activeCourse = null; render(); });

  if (!activeCourse) {
    app.innerHTML = `<div class="grid">${Object.entries(courses).map(([course, entries], index) => `<button class="card" type="button" data-course="${esc(course)}"><span class="number">${String(index + 1).padStart(2, '0')} / ${entries.length} VIDEOS</span><h2>${esc(course)}</h2><p>Watch the concept collection</p><span class="arrow">↘</span></button>`).join('')}</div>`;
    app.querySelectorAll('[data-course]').forEach(button => button.addEventListener('click', () => { activeCourse = button.dataset.course; render(); }));
    return;
  }

  const selected = videos.filter(video => video.course === activeCourse);
  app.innerHTML = `<div class="video-grid">${selected.map(video => `<article class="video-card"><div class="preview"><video controls preload="metadata" src="${esc(video.video)}"></video></div><div class="video-body"><span class="status">VIDEO READY</span><h2>${esc(video.title)}</h2><a class="cta" href="https://leadde.ai/animation" target="_blank" rel="noreferrer">Create an animation with Leadde →</a></div></article>`).join('')}</div>`;
}

fetch('./data/videos.json').then(response => response.json()).then(data => { videos = data; render(); }).catch(() => { app.innerHTML = '<p class="empty">The video collection could not be loaded.</p>'; });
