/* Floresta — interacción y movimiento */
(() => {
'use strict';
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const WA = '56964838490';
const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
const FINE = matchMedia('(hover: hover) and (pointer: fine)').matches;
const DESK = () => innerWidth > 860;
const clp = n => '$' + n.toLocaleString('es-CL');
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const IMG = id => `assets/img/t/${id}.jpg`;

gsap.registerPlugin(ScrollTrigger, Draggable, InertiaPlugin, Flip, SplitText);

/* ---------------- data ---------------- */
const P = [
  ['ramo-rosas-rojas', 'Doce rosas rojas', 'Rosas rojas con gypsophila y helecho.', 32000, 'amor'],
  ['ramo-rosas-bicolor', 'Rojo y crema', 'Rosas rojas y crema en envoltorio negro y rosado.', 45000, 'amor'],
  ['ramo-lilium-rosa', 'Lilium rosa', 'Lilium, rosas, dalias y margaritas.', 26000, 'cumpleanos'],
  ['ramo-tulipanes-blancos', 'Tulipanes en arpillera', 'Tulipanes blancos y amarillos con mini girasoles.', 25000, 'gracias novias'],
  ['ramo-girasoles-mix', 'Sol de Castro', 'Girasol, rosas durazno y crisantemo amarillo.', 24000, 'gracias'],
  ['ramo-pastel', 'Jardín pastel', 'Rosas cappuccino, ranúnculos y margaritas.', 38000, 'novias'],
  ['ramo-rosas-girasol', 'Fucsia y girasol', 'Rosas fucsia, girasol y anémona.', 26000, 'cumpleanos'],
  ['ramo-tropical', 'Mercado', 'Alstroemerias y flores de colores en papel coral.', 22000, 'gracias cumpleanos'],
  ['ramo-rosas-rosadas', 'Rosas rosadas', 'Rosas rosadas con alstroemerias blancas.', 28000, 'amor novias'],
  ['ramo-rosado-suave', 'Rosa suave', 'Alstroemerias, tulipanes y crisantemo rosado.', 24000, 'amor novias'],
  ['ramo-fucsia', 'Fucsia', 'Rosas, gerberas y crisantemos en papel blanco.', 22000, 'cumpleanos'],
  ['ramo-primavera', 'Primavera', 'Alstroemerias, margaritas y rosa lila.', 24000, 'cumpleanos gracias'],
  ['ramo-dalias-rosa', 'Crisantemo lila', 'Crisantemos lila, rosa y lirios blancos.', 20000, 'gracias'],
  ['ramo-girasoles', 'Girasoles del 21', 'Girasoles y alstroemerias en papel de diario.', 26000, 'gracias'],
  ['ramo-durazno', 'Durazno', 'Rosas durazno, claveles y ranúnculos naranjos.', 38000, 'novias'],
  ['ramo-jardin', 'Novia campestre', 'Rosas, hortensia verde y margaritas silvestres.', 42000, 'novias'],
  ['condolencia-blanco', 'Blanco y amarillo', 'Lirios blancos, craspedia y crisantemos amarillos.', 30000, 'condolencias'],
  ['anemonas-blancas', 'Anémonas blancas', 'Anémonas de temporada, sobrias y delicadas.', 28000, 'condolencias'],
  ['planta-pilea', 'Pilea', 'Planta china del dinero, en macetero.', 9900, 'plantas regalos'],
  ['planta-maranta', 'Maranta', 'Hojas con nervaduras rojas, para interior.', 12900, 'plantas'],
  ['planta-philodendron', 'Philodendron', 'Fácil de cuidar, crece con luz indirecta.', 10900, 'plantas'],
  ['regalo-corazon', 'Caja corazón', 'Rosas, peluche, bombones y un vino.', 35000, 'regalos amor'],
  ['regalo-peluche', 'Arreglo con peluche', 'Canasto de flores con peluche y corazón.', 29000, 'regalos cumpleanos'],
  ['ramo-rojo-dorado', 'Color intenso', 'Rosas naranjas, gerbera, anémona y col ornamental.', 30000, 'cumpleanos'],
].map(([id, n, d, p, c]) => ({ id, n, d, p, c: c.split(' ') }));
const byId = Object.fromEntries(P.map(p => [p.id, p]));
const FAV = ['ramo-pastel', 'ramo-rosas-rojas', 'ramo-tulipanes-blancos', 'ramo-lilium-rosa', 'ramo-girasoles-mix', 'ramo-rosas-bicolor', 'ramo-durazno', 'ramo-tropical'];
const DECK = ['ramo-rosas-girasol', 'ramo-jardin', 'ramo-fucsia', 'regalo-corazon', 'ramo-rosado-suave', 'ramo-girasoles', 'planta-maranta', 'ramo-primavera', 'ramo-rosas-rosadas', 'ramo-rojo-dorado'];
const OCC = [
  { k: 'amor', t: 'Amor', d: 'Rosas y ramos para decirlo', img: 'anemonas-rojas' },
  { k: 'cumpleanos', t: 'Cumpleaños', d: 'Color y alegría en un ramo', img: 'ramo-rojo-dorado' },
  { k: 'gracias', t: 'Gracias', d: 'Para quien siempre está', img: 'ramo-girasoles-mix' },
  { k: 'novias', t: 'Novias', d: 'Tonos suaves y silvestres', img: 'ramo-durazno' },
  { k: 'condolencias', t: 'Condolencias', d: 'Blancos y sobrios', img: 'condolencia-blanco' },
  { k: 'plantas', t: 'Plantas', d: 'Para que duren meses', img: 'planta-maranta' },
];
const FIL = [['todos', 'Todos'], ['amor', 'Amor'], ['cumpleanos', 'Cumpleaños'], ['gracias', 'Gracias'], ['novias', 'Novias'], ['condolencias', 'Condolencias'], ['plantas', 'Plantas'], ['regalos', 'Regalos']];
const WALL = ['hero', 'ranunculos', 'ramo-pastel', 'florista-orquideas', 'ramo-rosas-rojas', 'tulipanes-florero', 'anemonas-rojas', 'florista-girasol', 'ramo-girasoles', 'taller-detalles', 'ramo-durazno', 'regalo-corazon', 'florista-ramo', 'anemonas-blancas', 'ramo-lilium-rosa', 'tienda-bicicleta', 'planta-pilea', 'ramo-jardin'];

/* ---------------- render ---------------- */
const tagHTML = p => `<span class="tag"><small>desde</small>${clp(p.p)}</span>`;
$('#hTrack').innerHTML = FAV.map(id => { const p = byId[id]; return `
  <article class="pcard" data-id="${p.id}">
    <img class="pcard__img" src="${IMG(p.id)}" alt="${esc(p.n)}" draggable="false">
    ${tagHTML(p)}
    <div class="pcard__info"><div><h3>${esc(p.n)}</h3><p>${esc(p.d)}</p></div><button class="add" data-add="${p.id}" aria-label="Agregar ${esc(p.n)} al pedido">+</button></div>
  </article>`; }).join('');
$('#hTot').textContent = String(FAV.length).padStart(2, '0');

$('#occList').innerHTML = OCC.map((o, i) => `<li><button class="occ__item" data-filter="${o.k}" data-img="${o.img}">
  <span class="n">0${i + 1}</span><span class="t">${o.t}</span><span class="d">${o.d}</span><img class="mini" src="${IMG(o.img)}" alt="" loading="lazy"></button></li>`).join('');

$('#chips').innerHTML = FIL.map(([k, t]) => `<button class="chip" data-f="${k}" aria-pressed="${k === 'todos'}">${t}</button>`).join('');
$('#pgrid').innerHTML = P.map(p => `
  <article class="gcard" data-id="${p.id}" data-c="${p.c.join(' ')}">
    <div class="gcard__ph"><img src="${IMG(p.id)}" alt="${esc(p.n)}: ${esc(p.d)}" loading="lazy">${tagHTML(p)}<button class="add" data-add="${p.id}" aria-label="Agregar ${esc(p.n)} al pedido">+</button></div>
    <h3>${esc(p.n)}</h3><p>${esc(p.d)}</p>
  </article>`).join('');

const wallHTML = list => list.map(id => `<img src="${IMG(id)}" alt="" loading="lazy" draggable="false">`).join('');
$('#wall1').innerHTML = wallHTML(WALL.slice(0, 9));
$('#wall2').innerHTML = wallHTML(WALL.slice(9));

/* ---------------- smooth scroll ---------------- */
let lenis = null;
if (!REDUCED && window.Lenis) {
  lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 1, smoothWheel: true });
  window.__lenis = lenis;
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add(t => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
  lenis.stop();
}
const scrollToEl = el => { if (!el) return; lenis ? lenis.scrollTo(el, { duration: 1.6 }) : el.scrollIntoView({ behavior: REDUCED ? 'auto' : 'smooth' }); };
let velocity = 0;
if (lenis) lenis.on('scroll', e => { velocity = e.velocity; });

/* ---------------- loader ---------------- */
const seqFrames = [];
const SEQ_N = 110;
function preload(src) { return new Promise(res => { const i = new Image(); i.onload = i.onerror = () => res(i); i.src = src; }); }
(async function boot() {
  const word = $('.loader__word');
  word.innerHTML = [...word.textContent].map(c => `<span>${c}</span>`).join('');
  gsap.from('.loader__word span', { yPercent: 120, opacity: 0, stagger: .05, duration: 1, ease: 'expo.out' });
  const first = ['assets/video/taller.jpg', 'assets/video/desfile.jpg', 'assets/video/amarillas.jpg'];
  for (let i = 1; i <= SEQ_N; i++) first.push(`assets/seq/f${String(i).padStart(3, '0')}.webp`);
  let done = 0; const st = { v: 0 };
  const upd = () => { $('#loadNum').textContent = Math.round(st.v); $('#loadBar').style.transform = `scaleX(${st.v / 100})`; };
  const jobs = first.map((src, i) => preload(src).then(img => { if (i >= 3) seqFrames[i - 3] = img; done++; gsap.to(st, { v: done / first.length * 100, duration: .4, overwrite: true, onUpdate: upd }); }));
  await Promise.race([Promise.all(jobs), new Promise(r => setTimeout(r, 6000))]);
  await new Promise(r => gsap.to(st, { v: 100, duration: .5, onUpdate: upd, onComplete: r }));
  intro();
})();

function intro() {
  const tl = gsap.timeline({ onComplete: () => { document.body.classList.remove('is-loading'); lenis && lenis.start(); ScrollTrigger.refresh(); } });
  tl.to('.loader__word span', { yPercent: -120, opacity: 0, stagger: .03, duration: .6, ease: 'expo.in' })
    .to('#loader', { clipPath: 'inset(0 0 100% 0)', duration: 1.1, ease: 'expo.inOut' }, '-=.2')
    .set('#loader', { display: 'none' })
    .from('.hero__col', { yPercent: i => (i % 2 ? -30 : 30), scale: 1.2, duration: 1.6, ease: 'expo.out', stagger: .08 }, '-=.9')
    .from('#heroTitle .line > *', { yPercent: 110, duration: 1.3, ease: 'expo.out', stagger: .1 }, '-=1.3')
    .from('.hero__kicker, .hero__sub, .hero__row .btn, .nav', { y: 30, opacity: 0, duration: 1, ease: 'expo.out', stagger: .08 }, '-=1');
}
// wrap hero lines so inner can slide
$$('#heroTitle .line').forEach(l => { l.innerHTML = `<span style="display:inline-block">${l.innerHTML}</span>`; });

/* ---------------- nav, progress ---------------- */
const nav = $('#nav');
let lastY = 0;
ScrollTrigger.create({ start: 0, end: 'max', onUpdate: self => {
  const y = self.scroll();
  gsap.set('#progress', { scaleX: self.progress });
  nav.classList.toggle('is-solid', y > innerHeight * .8);
  nav.classList.toggle('is-hidden', y > lastY && y > 300 && !document.body.classList.contains('menu-open'));
  lastY = y;
} });

/* ---------------- hero parallax ---------------- */
if (!REDUCED) {
  $$('.hero__col').forEach(c => gsap.to(c, { yPercent: +c.dataset.speed, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } }));
  gsap.to('.hero__content', { yPercent: -30, opacity: 0, ease: 'none', scrollTrigger: { trigger: '.hero', start: '30% top', end: 'bottom top', scrub: true } });
}

/* ---------------- marquees (velocity reactive) ---------------- */
function marquee(row, base) {
  const track = row.firstElementChild;
  const unit = track.innerHTML;
  while (track.scrollWidth < innerWidth * 2.2) track.innerHTML += unit;
  track.innerHTML += track.innerHTML;
  const dir = +row.dataset.dir || 1;
  let x = 0, skew = 0;
  const setX = gsap.quickSetter(track, 'x', 'px');
  const setSkew = gsap.quickSetter(track, 'skewX', 'deg');
  gsap.ticker.add((t, dt) => {
    const half = track.scrollWidth / 2;
    const v = REDUCED ? 0 : Math.max(-40, Math.min(40, velocity));
    x -= (base + Math.abs(v) * 0.9) * dir * (dt / 16.7) * (v < 0 ? -1 : 1);
    if (x <= -half) x += half; if (x > 0) x -= half;
    setX(x);
    skew += ((REDUCED ? 0 : -v * 0.25) - skew) * 0.1;
    setSkew(skew);
  });
}
$$('.marquee__row').forEach(r => marquee(r, 1.1));
$$('.wall__row').forEach(r => marquee(r, 0.7));

/* ---------------- manifesto word reveal ---------------- */
(function manifesto() {
  const el = $('#manifesto');
  const walk = n => { [...n.childNodes].forEach(c => {
    if (c.nodeType === 3) {
      const f = document.createDocumentFragment();
      c.textContent.split(/(\s+)/).forEach(w => { if (!w) return; if (/^\s+$/.test(w)) f.append(w); else { const s = document.createElement('span'); s.className = 'w'; s.textContent = w; f.append(s); } });
      c.replaceWith(f);
    } }); };
  walk(el);
  const words = $$('.w, .pill', el);
  ScrollTrigger.create({ trigger: el, start: 'top 80%', end: 'bottom 45%', scrub: true, onUpdate: self => {
    const k = Math.round(self.progress * words.length);
    words.forEach((w, i) => { if (w.classList.contains('w')) w.style.color = i < k ? 'var(--ink)' : ''; else w.style.transform = i < k ? 'rotate(-3deg) scale(1)' : 'rotate(-3deg) scale(.4)'; });
  } });
  $$('.pill', el).forEach(p => { p.style.transition = 'transform .6s cubic-bezier(.16,1,.3,1)'; p.style.transform = 'rotate(-3deg) scale(.4)'; });
  gsap.from('.manifesto__sign', { opacity: 0, x: -30, rotate: -8, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: '.manifesto__sign', start: 'top 90%' } });
})();

/* ---------------- hyperframes ---------------- */
(function frames() {
  const cv = $('#seq'); const ctx = cv.getContext('2d');
  const steps = $$('.frames__steps li');
  let cur = -1;
  const draw = i => {
    i = Math.max(0, Math.min(SEQ_N - 1, i)); if (i === cur) return;
    const img = seqFrames[i] || seqFrames.find(Boolean);
    if (!img || !img.naturalWidth) { if (!seqFrames[i]) preload(`assets/seq/f${String(i + 1).padStart(3, '0')}.webp`).then(im => { seqFrames[i] = im; cur = -1; draw(i); }); return; }
    cur = i; ctx.drawImage(img, 0, 0, cv.width, cv.height);
    $('#frameNum').textContent = String(i + 1).padStart(3, '0');
  };
  const wait = setInterval(() => { if (seqFrames[0]) { draw(0); clearInterval(wait); } }, 100);
  ScrollTrigger.create({ trigger: '.frames', start: 'top top', end: 'bottom bottom', scrub: true, onUpdate: self => {
    const p = self.progress;
    draw(Math.round(p * (SEQ_N - 1)));
    gsap.set('#frameBar', { scaleX: p });
    const s = Math.min(steps.length - 1, Math.floor(p * steps.length));
    steps.forEach((li, i) => li.classList.toggle('is-on', i === s));
  } });
  if (!REDUCED) gsap.fromTo('.frames__bgword', { xPercent: -30 }, { xPercent: -70, ease: 'none', scrollTrigger: { trigger: '.frames', start: 'top bottom', end: 'bottom top', scrub: true } });
  gsap.from('.frames__stage', { scale: .7, borderRadius: 200, ease: 'none', scrollTrigger: { trigger: '.frames', start: 'top bottom', end: 'top top', scrub: true } });
})();

/* ---------------- occasions follower ---------------- */
(function occ() {
  const sec = $('#ocasiones'), fol = $('#occFollow'), img = $('img', fol), bg = $('#occBg');
  if (FINE) {
    const xTo = gsap.quickTo(fol, 'x', { duration: .6, ease: 'power3' }), yTo = gsap.quickTo(fol, 'y', { duration: .6, ease: 'power3' });
    const rTo = gsap.quickTo(fol, 'rotation', { duration: .8, ease: 'power3' });
    let px = 0;
    sec.addEventListener('pointermove', e => { const r = sec.getBoundingClientRect(); const x = e.clientX - r.left, y = e.clientY - r.top; xTo(x); yTo(y); rTo(Math.max(-12, Math.min(12, (x - px) * .6))); px = x; });
    $$('.occ__item').forEach(b => {
      b.addEventListener('pointerenter', () => { img.src = IMG(b.dataset.img); bg.style.backgroundImage = `url(assets/img/${b.dataset.img}.jpg)`; gsap.to(fol, { opacity: 1, scale: 1, duration: .5, ease: 'expo.out' }); bg.style.opacity = .55; });
    });
    $('#occList').addEventListener('pointerleave', () => { gsap.to(fol, { opacity: 0, scale: .6, duration: .4 }); bg.style.opacity = 0; });
  }
  gsap.from('.occ__item .t', { yPercent: 100, opacity: 0, duration: 1.2, ease: 'expo.out', stagger: .07, scrollTrigger: { trigger: '#occList', start: 'top 80%' } });
})();

/* ---------------- horizontal shop ---------------- */
let hTween = null;
ScrollTrigger.matchMedia({
  '(min-width: 861px)': () => {
    const track = $('#hTrack');
    const dist = () => track.scrollWidth - (innerWidth - $('.hshop__intro').offsetWidth) + 40;
    hTween = gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: { trigger: '.hshop', pin: '.hshop__pin', start: 'top top', end: () => '+=' + dist(), scrub: 1, invalidateOnRefresh: true,
      onUpdate: self => { $('#hIdx').textContent = String(Math.min(FAV.length, 1 + Math.floor(self.progress * FAV.length))).padStart(2, '0'); } } });
    $$('.pcard').forEach(c => gsap.fromTo(c, { rotate: 4, y: 60 }, { rotate: 0, y: 0, ease: 'none', scrollTrigger: { trigger: c, containerAnimation: hTween, start: 'left right', end: 'left 55%', scrub: true } }));
    return () => { hTween = null; };
  },
});
if (FINE) $$('.pcard, .gcard__ph').forEach(c => {
  const rx = gsap.quickTo(c, 'rotationX', { duration: .6, ease: 'power3' }), ry = gsap.quickTo(c, 'rotationY', { duration: .6, ease: 'power3' });
  gsap.set(c, { transformPerspective: 900 });
  c.addEventListener('pointermove', e => { const r = c.getBoundingClientRect(); ry(((e.clientX - r.left) / r.width - .5) * 12); rx(-((e.clientY - r.top) / r.height - .5) * 12); });
  c.addEventListener('pointerleave', () => { rx(0); ry(0); });
});

/* ---------------- grid filter with Flip ---------------- */
let curF = 'todos';
function setFilter(k) {
  curF = k;
  const cards = $$('.gcard');
  const state = Flip.getState(cards);
  cards.forEach(c => { c.style.display = (k === 'todos' || c.dataset.c.split(' ').includes(k)) ? '' : 'none'; });
  $$('.chip').forEach(b => b.setAttribute('aria-pressed', b.dataset.f === k));
  Flip.from(state, { duration: .8, ease: 'expo.inOut', scale: true, absolute: true, stagger: .02,
    onEnter: els => gsap.fromTo(els, { opacity: 0, scale: .8, y: 40 }, { opacity: 1, scale: 1, y: 0, duration: .8, ease: 'expo.out', stagger: .03 }),
    onLeave: els => gsap.to(els, { opacity: 0, scale: .8, duration: .4 }),
    onComplete: () => ScrollTrigger.refresh() });
}
gsap.utils.toArray('.gcard').forEach((c, i) => gsap.from(c, { y: 80, opacity: 0, duration: 1.1, ease: 'expo.out', delay: (i % 4) * .08, scrollTrigger: { trigger: c, start: 'top 92%' } }));

/* ---------------- swipe deck ---------------- */
let deckIdx = 0, liked = 0;
function buildDeck() {
  const deck = $('#deck');
  deck.innerHTML = `<div class="deck__done"><b>Eso es todo por ahora</b><p>Elegiste ${liked} ${liked === 1 ? 'ramo' : 'ramos'}.</p><button class="btn btn--light" id="deckAgain"><span>Ver de nuevo</span><i class="btn__ico">↺</i></button></div>` +
    DECK.slice().reverse().map(id => { const p = byId[id]; return `<article class="scard" data-id="${id}"><img src="${IMG(id)}" alt="${esc(p.n)}"><span class="stamp stamp--yes">LO QUIERO</span><span class="stamp stamp--no">OTRO</span><div class="scard__info"><h3>${esc(p.n)}</h3><p>desde ${clp(p.p)} · ${esc(p.d)}</p></div></article>`; }).join('');
  deckIdx = 0; layoutDeck();
  $('#deckAgain').onclick = () => { liked = 0; buildDeck(); };
}
function topCard() { const cs = $$('.scard'); return cs[cs.length - 1 - deckIdx]; }
function layoutDeck() {
  const cs = $$('.scard').reverse();
  cs.forEach((c, i) => { const d = i - deckIdx; if (d < 0) return; gsap.to(c, { scale: 1 - Math.min(d, 3) * .05, y: Math.min(d, 3) * 18, rotation: d === 0 ? 0 : (d % 2 ? 3 : -3), duration: .6, ease: 'expo.out' }); });
  $('#swLeft').textContent = DECK.length - deckIdx; $('#swLiked').textContent = liked;
  const t = topCard(); if (!t) return;
  Draggable.create(t, { type: 'x,y', inertia: false, onDrag() { const r = this.x * .07; gsap.set(t, { rotation: r }); $('.stamp--yes', t).style.opacity = Math.max(0, this.x / 120); $('.stamp--no', t).style.opacity = Math.max(0, -this.x / 120); },
    onRelease() { const vx = InertiaPlugin.getVelocity(t, 'x') || 0; if (Math.abs(this.x) > 110 || Math.abs(vx) > 900) fling(this.x + vx * .1 > 0); else gsap.to(t, { x: 0, y: 0, rotation: 0, duration: .9, ease: 'elastic.out(1,.5)', onUpdate() { $$('.stamp', t).forEach(s => s.style.opacity = 0); } }); } });
}
function fling(yes) {
  const t = topCard(); if (!t) return;
  Draggable.get(t)?.kill();
  $(yes ? '.stamp--yes' : '.stamp--no', t).style.opacity = 1;
  gsap.to(t, { x: (yes ? 1 : -1) * innerWidth, y: '+=' + 80, rotation: yes ? 30 : -30, duration: .7, ease: 'power2.in', onComplete: () => { t.style.visibility = 'hidden'; } });
  if (yes) { liked++; add(t.dataset.id, $('img', t)); }
  deckIdx++; setTimeout(layoutDeck, 120);
  if (deckIdx >= DECK.length) setTimeout(() => { const d = $('.deck__done p'); if (d) d.textContent = `Elegiste ${liked} ${liked === 1 ? 'ramo' : 'ramos'}.`; }, 200);
}
buildDeck();
$('#swYes').onclick = () => fling(true);
$('#swNo').onclick = () => fling(false);

/* ---------------- stacked panels ---------------- */
$$('.panel').forEach((p, i, arr) => {
  const shade = document.createElement('div'); shade.className = 'panel__shade'; p.append(shade);
  if (i < arr.length - 1 && !REDUCED) {
    gsap.to(p, { scale: .9, borderRadius: 30, ease: 'none', scrollTrigger: { trigger: arr[i + 1], start: 'top bottom', end: 'top top', scrub: true } });
    gsap.to(shade, { opacity: .55, ease: 'none', scrollTrigger: { trigger: arr[i + 1], start: 'top bottom', end: 'top top', scrub: true } });
  }
  gsap.from($('.panel__img', p), { scale: 1.25, ease: 'none', scrollTrigger: { trigger: p, start: 'top bottom', end: 'top top', scrub: true } });
  gsap.from($$('.panel__in > *', p), { y: 60, opacity: 0, duration: 1.1, ease: 'expo.out', stagger: .08, scrollTrigger: { trigger: p, start: 'top 55%' } });
});

/* ---------------- season slider (drag + inertia) ---------------- */
(function slider() {
  const wrap = $('#slider'), track = $('#sTrack');
  const bounds = () => ({ minX: Math.min(0, wrap.offsetWidth - track.scrollWidth), maxX: 0 });
  const bar = () => { const b = bounds(); const x = gsap.getProperty(track, 'x'); const p = b.minX ? x / b.minX : 1; gsap.set('#sBar', { scaleX: .1 + .9 * p }); };
  const d = Draggable.create(track, { type: 'x', bounds: bounds(), inertia: true, edgeResistance: .85, dragClickables: true, onDrag: bar, onThrowUpdate: bar,
    onPress() { gsap.to($$('.slide', track), { scale: .97, duration: .4 }); }, onRelease() { gsap.to($$('.slide', track), { scale: 1, duration: .6, ease: 'expo.out' }); } })[0];
  addEventListener('resize', () => d.applyBounds(bounds()));
  gsap.from('.slide', { x: 200, opacity: 0, rotation: 6, stagger: .08, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: '#slider', start: 'top 85%' } });
  gsap.fromTo('.season__video', { rotation: -12, yPercent: 20 }, { rotation: 4, yPercent: -10, ease: 'none', scrollTrigger: { trigger: '.season', start: 'top bottom', end: 'bottom top', scrub: true } });
})();

/* ---------------- how ---------------- */
(function how() {
  const path = $('#howPath');
  if (path) { gsap.set(path, { strokeDasharray: 100, strokeDashoffset: 100, attr: { pathLength: 100 } });
    gsap.to(path, { strokeDashoffset: 0, ease: 'none', scrollTrigger: { trigger: '.how__steps', start: 'top 60%', end: 'bottom 60%', scrub: true } }); }
  $$('.how__steps li').forEach(li => ScrollTrigger.create({ trigger: li, start: 'top 62%', end: 'bottom 40%', toggleClass: 'is-lit' }));
  gsap.from('.how__steps li', { x: 60, opacity: 0, duration: 1.1, ease: 'expo.out', stagger: .12, scrollTrigger: { trigger: '.how__steps', start: 'top 80%' } });
})();

/* ---------------- visit parallax + section titles ---------------- */
if (!REDUCED) gsap.fromTo('.visit__bg', { yPercent: -8 }, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: '.visit', start: 'top bottom', end: 'bottom top', scrub: true } });
gsap.from('.visit__card', { y: 100, opacity: 0, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: '.visit', start: 'top 60%' } });
document.fonts && document.fonts.ready.then(() => {
  $$('.grid-sec .big, .swipe .big, .season .big, .how .big, .occ .big, .visit .big').forEach(h => {
    const s = new SplitText(h, { type: 'lines,words', mask: 'lines' });
    gsap.from(s.words, { yPercent: 110, duration: 1.2, ease: 'expo.out', stagger: .04, scrollTrigger: { trigger: h, start: 'top 85%' } });
  });
  ScrollTrigger.refresh();
});

/* ---------------- magnetic buttons ---------------- */
if (FINE) $$('.magnetic').forEach(b => {
  const xT = gsap.quickTo(b, 'x', { duration: .5, ease: 'power3' }), yT = gsap.quickTo(b, 'y', { duration: .5, ease: 'power3' });
  b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); xT((e.clientX - r.left - r.width / 2) * .3); yT((e.clientY - r.top - r.height / 2) * .35); });
  b.addEventListener('pointerleave', () => { xT(0); yT(0); });
});

/* ---------------- physics footer ---------------- */
(function physics() {
  const { Engine, Bodies, Composite, Mouse, MouseConstraint, Body } = Matter;
  const cv = $('#physics'), ctx = cv.getContext('2d'), foot = $('#foot');
  const sprites = Array.from({ length: 10 }, (_, i) => { const im = new Image(); im.src = `assets/petals/p${i}.png`; return im; });
  let engine, bodies = [], walls = [], running = false, W = 0, H = 0, dpr = 1;
  function size() { dpr = Math.min(2, devicePixelRatio || 1); W = foot.clientWidth; H = foot.clientHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
  function makeWalls() {
    if (walls.length) Composite.remove(engine.world, walls);
    const t = 200, floor = H - 70;
    walls = [Bodies.rectangle(W / 2, floor + t / 2, W * 3, t, { isStatic: true }), Bodies.rectangle(-t / 2, H / 2, t, H * 4, { isStatic: true }), Bodies.rectangle(W + t / 2, H / 2, t, H * 4, { isStatic: true })];
    Composite.add(engine.world, walls);
  }
  function drop(n) {
    for (let i = 0; i < n; i++) setTimeout(() => {
      const r = (W < 700 ? 34 : 48) + Math.random() * (W < 700 ? 22 : 40);
      const b = Bodies.circle(W * (.15 + Math.random() * .7), -r - Math.random() * 400, r, { restitution: .45, friction: .08, frictionAir: .012, density: .002 });
      b.sprite = sprites[(bodies.length) % sprites.length]; b.r = r; Body.setAngularVelocity(b, (Math.random() - .5) * .2);
      bodies.push(b); Composite.add(engine.world, b);
    }, i * 90);
  }
  function start() {
    if (running) return; running = true; size();
    engine = Engine.create({ gravity: { y: 1 } }); makeWalls();
    if (FINE) {
      const mouse = Mouse.create(cv); mouse.pixelRatio = 1;
      cv.removeEventListener('wheel', mouse.mousewheel); cv.removeEventListener('mousewheel', mouse.mousewheel); cv.removeEventListener('DOMMouseScroll', mouse.mousewheel);
      Composite.add(engine.world, MouseConstraint.create(engine, { mouse, constraint: { stiffness: .2, render: { visible: false } } }));
    } else {
      cv.addEventListener('click', e => { const r = cv.getBoundingClientRect(); bodies.forEach(b => { const dx = b.position.x - (e.clientX - r.left), dy = b.position.y - (e.clientY - r.top); const d = Math.hypot(dx, dy); if (d < 220) Body.applyForce(b, b.position, { x: dx / d * .06 * b.mass, y: -.12 * b.mass }); }); });
    }
    drop(W < 700 ? 16 : 26);
    gsap.ticker.add(tick);
  }
  function tick(t, dt) {
    Engine.update(engine, Math.min(dt, 32));
    ctx.clearRect(0, 0, W, H);
    for (const b of bodies) {
      ctx.save(); ctx.translate(b.position.x, b.position.y); ctx.rotate(b.angle);
      if (b.sprite.complete && b.sprite.naturalWidth) ctx.drawImage(b.sprite, -b.r, -b.r, b.r * 2, b.r * 2);
      else { ctx.fillStyle = '#E4572E'; ctx.beginPath(); ctx.arc(0, 0, b.r, 0, 7); ctx.fill(); }
      ctx.restore();
    }
  }
  ScrollTrigger.create({ trigger: foot, start: 'top 60%', once: true, onEnter: start });
  addEventListener('resize', () => { if (running) { size(); makeWalls(); } });
})();

/* ---------------- menu ---------------- */
const burger = $('#burger');
function menu(open) {
  document.body.classList.toggle('menu-open', open);
  burger.setAttribute('aria-expanded', open); $('#menu').setAttribute('aria-hidden', !open);
  open ? lenis && lenis.stop() : lenis && lenis.start();
}
burger.onclick = () => menu(!document.body.classList.contains('menu-open'));
$$('.menu__list a').forEach(a => a.addEventListener('pointerenter', () => { const im = $('.menu__bg img'); im.style.opacity = 0; setTimeout(() => { im.src = `assets/img/${a.dataset.img}.jpg`; im.style.opacity = 1; }, 200); }));

/* ---------------- global clicks ---------------- */
document.addEventListener('click', e => {
  const f = e.target.closest('[data-filter]');
  if (f) { e.preventDefault(); menu(false); setFilter(f.dataset.filter); scrollToEl($('#tienda')); return; }
  const c = e.target.closest('.chip'); if (c) { setFilter(c.dataset.f); return; }
  const a = e.target.closest('[data-add]'); if (a) { e.preventDefault(); const card = a.closest('[data-id]'); add(a.dataset.add, card && $('img', card)); return; }
  const w = e.target.closest('[data-wa]'); if (w) { w.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(w.dataset.wa); w.target = '_blank'; w.rel = 'noopener'; return; }
  const h = e.target.closest('a[href^="#"]');
  if (h && h.getAttribute('href').length > 1) { e.preventDefault(); menu(false); scrollToEl($(h.getAttribute('href'))); }
});

/* ---------------- cart ---------------- */
let cart = {};
try { cart = JSON.parse(localStorage.getItem('floresta-cart') || '{}') || {}; } catch (e) { cart = {}; }
Object.keys(cart).forEach(k => { if (!byId[k]) delete cart[k]; });
const save = () => { try { localStorage.setItem('floresta-cart', JSON.stringify(cart)); } catch (e) {} };
function fly(img) {
  if (!img || REDUCED) return;
  const a = img.getBoundingClientRect(), b = $('#cartBtn').getBoundingClientRect();
  const f = document.createElement('div'); f.className = 'flyer'; f.innerHTML = `<img src="${img.src}" alt="">`; document.body.append(f);
  gsap.set(f, { left: a.left + a.width / 2 - 35, top: a.top + a.height / 2 - 44 });
  const tl = gsap.timeline({ onComplete: () => f.remove() });
  tl.to(f, { x: b.left + b.width / 2 - (a.left + a.width / 2), duration: .9, ease: 'power1.inOut' }, 0)
    .to(f, { y: b.top + b.height / 2 - (a.top + a.height / 2), duration: .9, ease: 'back.in(1.6)' }, 0)
    .to(f, { scale: .2, rotation: 25, opacity: .6, duration: .9, ease: 'power2.in' }, 0);
}
function add(id, img) {
  cart[id] = (cart[id] || 0) + 1; save(); sync(); fly(img);
  setTimeout(() => gsap.fromTo('#cartBtn', { scale: 1 }, { scale: 1.15, duration: .25, yoyo: true, repeat: 1, ease: 'power2.out' }), 800);
  toast(`${byId[id].n} está en tu pedido`);
}
function setQ(id, d) { cart[id] = (cart[id] || 0) + d; if (cart[id] <= 0) delete cart[id]; save(); sync(); }
function totals() { let n = 0, t = 0; for (const k in cart) { n += cart[k]; t += cart[k] * byId[k].p; } return { n, t }; }
function message() {
  const { t } = totals(); const mode = $('input[name=mode]:checked').value;
  const L = ['Hola Floresta, quiero hacer un pedido:', ''];
  for (const k in cart) L.push(`• ${cart[k]} × ${byId[k].n} (desde ${clp(byId[k].p)})`);
  L.push('', `Total referencial: ${clp(t)}`);
  const m = $('#msg').value.trim(); if (m) L.push('', `Tarjeta: "${m}"`);
  L.push('', `Entrega: ${mode}`);
  const d = $('#date').value; if (d) { const [y, mo, da] = d.split('-'); L.push(`Fecha: ${da}/${mo}/${y}, ${$('#slot').value}`); }
  if (mode === 'Despacho' && $('#addr').value.trim()) L.push(`Dirección: ${$('#addr').value.trim()}`);
  if ($('#to').value.trim()) L.push(`Recibe: ${$('#to').value.trim()}`);
  if ($('#from').value.trim()) L.push(`Mi nombre: ${$('#from').value.trim()}`);
  return L.join('\n');
}
function sync() {
  const { n, t } = totals();
  $('#cartCount').textContent = n; $('#total').textContent = clp(t); $('#fabTotal').textContent = clp(t);
  $('#itemsN').textContent = n ? `· ${n} ${n === 1 ? 'producto' : 'productos'}` : '';
  $('#fab').classList.toggle('on', n > 0);
  $$('[data-add]').forEach(b => { const on = !!cart[b.dataset.add]; b.classList.toggle('done', on); b.textContent = on ? '✓' : '+'; });
  if (!n) { $('#lines').innerHTML = `<div class="empty"><b>Tu pedido está vacío</b><p>Elige un ramo y aquí escribes la tarjeta y la fecha de entrega.</p><a class="btn btn--coral" href="#ramos" id="goShop"><span>Ver ramos</span><i class="btn__ico">→</i></a></div>`; $('#orderForm').hidden = true; }
  else { $('#orderForm').hidden = false; $('#lines').innerHTML = '<div style="display:grid;gap:14px">' + Object.keys(cart).map(k => { const p = byId[k]; return `<div class="line"><img src="${IMG(p.id)}" alt=""><div><b>${esc(p.n)}</b><small>desde ${clp(p.p)}</small></div><div class="qty"><button data-q="${k}" data-d="-1" aria-label="Quitar uno">−</button><span>${cart[k]}</span><button data-q="${k}" data-d="1" aria-label="Agregar uno">+</button></div></div>`; }).join('') + '</div>'; }
  updateSend();
}
function updateSend() {
  const { n } = totals(); const s = $('#send');
  s.setAttribute('aria-disabled', n ? 'false' : 'true');
  s.href = n ? 'https://wa.me/' + WA + '?text=' + encodeURIComponent(message()) : '#';
  $('#addrF').hidden = $('input[name=mode]:checked').value !== 'Despacho';
}
const drawer = $('#drawer');
drawer.addEventListener('click', e => { const q = e.target.closest('[data-q]'); if (q) setQ(q.dataset.q, +q.dataset.d); if (e.target.closest('#goShop')) closeDr(); });
drawer.addEventListener('input', updateSend); drawer.addEventListener('change', updateSend);
const td = new Date(); $('#date').min = new Date(td - td.getTimezoneOffset() * 6e4).toISOString().slice(0, 10);
let lastFocus = null;
function openDr() { lastFocus = document.activeElement; document.body.classList.add('cart-open'); drawer.setAttribute('aria-hidden', 'false'); $('#cartBtn').setAttribute('aria-expanded', 'true'); lenis && lenis.stop(); setTimeout(() => $('#closeDr').focus(), 60);
  gsap.from('.drawer__body > *', { x: 40, opacity: 0, stagger: .06, duration: .8, ease: 'expo.out', delay: .2 }); }
function closeDr() { document.body.classList.remove('cart-open'); drawer.setAttribute('aria-hidden', 'true'); $('#cartBtn').setAttribute('aria-expanded', 'false'); lenis && lenis.start(); lastFocus && lastFocus.focus && lastFocus.focus(); }
$('#cartBtn').onclick = openDr; $('#fab').onclick = openDr; $('#closeDr').onclick = closeDr; $('#scrim').onclick = closeDr;
addEventListener('keydown', e => { if (e.key === 'Escape') { if (document.body.classList.contains('cart-open')) closeDr(); if (document.body.classList.contains('menu-open')) menu(false); } });
function copy(text, ok) { (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(() => toast(ok)).catch(() => toast('No se pudo copiar. Selecciona el texto y cópialo a mano.')); }
$('#copyPhone').onclick = () => copy('+56 9 6483 8490', 'Número copiado');
$('#copyOrder').onclick = () => { if (!totals().n) { toast('Agrega un ramo primero'); return; } copy(message(), 'Pedido copiado. Pégalo en WhatsApp.'); };
let tt; function toast(m) { const t = $('#toast'); t.textContent = m; t.classList.add('show'); clearTimeout(tt); tt = setTimeout(() => t.classList.remove('show'), 2400); }
sync();

/* keep hero videos playing only when visible */
const io = new IntersectionObserver(es => es.forEach(en => { const v = en.target; en.isIntersecting ? v.play().catch(() => {}) : v.pause(); }), { threshold: .05 });
$$('video').forEach(v => io.observe(v));
addEventListener('load', () => ScrollTrigger.refresh());
})();
