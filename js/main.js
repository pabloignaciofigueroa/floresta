/* =========================================================
   FLORESTA — movimiento e interacción
   Curva única: expo.out = cubic-bezier(.16,1,.3,1) · cortinas: power3.inOut
   ========================================================= */
(() => {
  'use strict';

  const root = document.documentElement;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const desktop = window.matchMedia('(min-width: 900px)');
  const fine = window.matchMedia('(hover: hover) and (pointer: fine)');
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* sin almacenamiento */ } }
  };
  let introDone = false;
  const critical = window.__floresta || { done: Promise.resolve(), reached: Promise.resolve() };
  let finishIntro = () => { const l = $('.loader'); if (l) l.remove(); };
  const loaderSafety = setTimeout(() => finishIntro(), 9000);

  /* posición estable del scroll mientras la ventana cambia de tamaño */
  let stableY = window.scrollY, resizing = false, resizeT = 0, resizeFromY = null;
  let anchor = null; /* sección visible y cuánto se había avanzado en ella */
  const takeAnchor = () => {
    const secs = [...document.querySelectorAll('main > section, .foot')];
    const sec = secs.find(x => { const r = x.getBoundingClientRect(); return r.top <= 1 && r.bottom > 1; });
    if (!sec) return null;
    const r = sec.getBoundingClientRect();
    return { sec, ratio: -r.top / Math.max(1, r.height) };
  };
  let anchorRaf = 0, restoring = false;
  window.addEventListener('scroll', () => {
    if (!resizing) stableY = window.scrollY;
    if (!anchorRaf) anchorRaf = requestAnimationFrame(() => { anchorRaf = 0; if (!restoring) anchor = takeAnchor(); });
  }, { passive: true });
  window.addEventListener('resize', () => {
    if (!resizing) { resizing = true; resizeFromY = stableY; }
    clearTimeout(resizeT);
    resizeT = setTimeout(() => { resizing = false; resizeFromY = null; stableY = window.scrollY; }, 1200);
  });

  /* ---------- idioma: español por defecto, inglés solo si se elige ---------- */
  const swapAttr = (attr, key) => {
    $$(`[data-${key}-en]`).forEach(el => {
      if (el.dataset[key + 'Es'] === undefined) el.dataset[key + 'Es'] = el.getAttribute(attr) || '';
      el.setAttribute(attr, root.dataset.lang === 'en' ? el.dataset[key + 'En'] : el.dataset[key + 'Es']);
      /* dentro del contenido en español, lo traducido se marca como inglés */
      if (el.closest('[lang="es"]') && key !== 'meta') { if (root.dataset.lang === 'en') el.setAttribute('lang', 'en'); else if (el.getAttribute('lang') === 'en') el.removeAttribute('lang'); }
    });
  };
  const setLang = (l) => {
    root.dataset.lang = l;
    root.lang = l;
    store.set('floresta-lang', l);
    swapAttr('alt', 'alt');
    swapAttr('aria-label', 'aria');
    swapAttr('content', 'meta');
    document.dispatchEvent(new CustomEvent('floresta:lang'));
  };
  $$('[data-l="en"]').forEach(el => el.setAttribute('lang', 'en'));
  setLang(store.get('floresta-lang') === 'en' ? 'en' : 'es');
  $('[data-lang-toggle]')?.addEventListener('click', () => setLang(root.dataset.lang === 'es' ? 'en' : 'es'));

  /* ---------- scroll suave ---------- */
  let lenis = null;
  const scrollToEl = (el) => {
    if (!el) return;
    if (lenis) lenis.scrollTo(el, { duration: 1.5, force: true, easing: t => 1 - Math.pow(1 - t, 4) });
    else el.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
  };
  const focusTarget = (t) => { if (!t.hasAttribute('tabindex')) t.setAttribute('tabindex', '-1'); t.focus({ preventScroll: true }); };
  $$('a[href^="#"]').forEach(a => {
    if (a.hasAttribute('data-menu-key')) return;
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      if (id.length < 2) { e.preventDefault(); scrollToEl(document.body); return; }
      const t = $(id);
      if (!t) return;
      e.preventDefault();
      if (cartOpen) toggleCart(false);
      scrollToEl(t);
      focusTarget(t);
    });
  });

  /* ---------- diálogos: menú y pedido (foco atrapado + resto inert) ---------- */
  const outside = () => $$('main, .foot, .nav, .skip');
  const trapTab = (box, e) => {
    const f = $$('a, button, input, textarea, select', box).filter(x => x.offsetParent && !x.disabled);
    if (!f.length) return;
    const first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  };

  const menu = $('[data-menu]');
  const openBtn = $('[data-menu-open]');
  let menuOpen = false;
  const toggleMenu = (open, then) => {
    if (open === menuOpen || !menu) return;
    menuOpen = open;
    openBtn.setAttribute('aria-expanded', String(open));
    if (window.gsap) { gsap.killTweensOf(menu); gsap.killTweensOf($$('.menu__w', menu)); }
    outside().forEach(el => { el.inert = open; });
    if (open) {
      menu.hidden = false;
      lenis && lenis.stop();
      if (window.gsap && !reduced) {
        gsap.fromTo(menu, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: .8, ease: 'power3.inOut' });
        gsap.fromTo($$('.menu__w', menu), { yPercent: 110 }, { yPercent: 0, duration: .8, stagger: .05, ease: 'power3.inOut', delay: .3 });
      } else menu.style.clipPath = 'none';
      $('[data-menu-close]').focus();
    } else {
      const done = () => { menu.hidden = true; lenis && introDone && lenis.start(); if (then) then(); else openBtn.focus(); };
      if (window.gsap && !reduced) gsap.to(menu, { clipPath: 'inset(100% 0 0% 0)', duration: .6, ease: 'power3.inOut', onComplete: done });
      else done();
    }
  };
  openBtn?.addEventListener('click', () => toggleMenu(true));
  $('[data-menu-close]')?.addEventListener('click', () => toggleMenu(false));
  $$('[data-menu-key]').forEach(a => {
    const show = () => $$('[data-menu-img]').forEach(i => i.classList.toggle('is-on', i.dataset.menuImg === a.dataset.menuKey));
    a.addEventListener('mouseenter', show);
    a.addEventListener('focus', show);
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const t = $(a.getAttribute('href'));
      toggleMenu(false, () => { scrollToEl(t); focusTarget(t); });
    });
  });

  /* ---------- pedido: carrito que se envía armado por WhatsApp ---------- */
  const cart = $('[data-cart]');
  const cartBtn = $('[data-cart-open]');
  const WA = '56964838490';
  const clp = (n) => '$' + String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  let items = [];
  try { items = JSON.parse(store.get('floresta-pedido') || '[]'); if (!Array.isArray(items)) items = []; } catch (e) { items = []; }
  let cartOpen = false;
  let navHoldUntil = 0; /* tras agregar, la barra con "Pedido" queda a la vista */
  const saveCart = () => store.set('floresta-pedido', JSON.stringify(items));
  const renderCart = () => {
    const n = items.reduce((a, i) => a + i.qty, 0);
    $('[data-cart-count]').textContent = n;
    const list = $('[data-cart-items]');
    list.innerHTML = '';
    items.forEach((it, idx) => {
      const li = document.createElement('li');
      li.className = 'cart__item';
      li.innerHTML = `<span><b></b><small></small></span><span class="cart__qty"><button type="button" data-q="-1"></button><span></span><button type="button" data-q="1"></button></span><span class="t-label"></span>`;
      li.querySelector('b').textContent = it.name;
      li.querySelector('small').textContent = `${it.option} · ${clp(it.price)}`;
      const [minus, plus] = li.querySelectorAll('button');
      const en = root.dataset.lang === 'en';
      minus.textContent = '−'; minus.setAttribute('aria-label', (en ? 'One less: ' : 'Uno menos: ') + it.name);
      plus.textContent = '+'; plus.setAttribute('aria-label', (en ? 'One more: ' : 'Uno más: ') + it.name);
      li.querySelector('.cart__qty > span').textContent = it.qty;
      li.querySelector('.t-label').textContent = clp(it.price * it.qty);
      li.addEventListener('click', (e) => {
        const b = e.target.closest('[data-q]');
        if (!b) return;
        const q = b.dataset.q;
        it.qty += parseInt(q, 10);
        const gone = it.qty <= 0;
        if (gone) items.splice(idx, 1);
        saveCart(); renderCart();
        const rows = $$('[data-cart-items] .cart__item');
        const row = rows[gone ? Math.min(idx, rows.length - 1) : idx];
        const again = row && $(`[data-q="${gone ? '1' : q}"]`, row);
        if (again) again.focus(); else $('.cart__close').focus();
      });
      list.appendChild(li);
    });
    const total = items.reduce((a, i) => a + i.price * i.qty, 0);
    $('[data-cart-empty]').hidden = items.length > 0;
    $('[data-cart-total-row]').hidden = items.length === 0;
    $('[data-cart-total]').textContent = clp(total);
  };
  const toast = (msg) => {
    const t = $('[data-toast]');
    t.textContent = msg; t.classList.add('is-on');
    clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('is-on'), 2400);
  };
  $$('[data-add]').forEach(btn => {
    btn.addEventListener('click', () => {
      const card = btn.closest('[data-product]');
      const opt = $('input:checked', card);
      const it = { name: card.dataset.product, option: opt.value, price: parseInt(opt.dataset.price, 10), qty: 1 };
      const same = items.find(i => i.name === it.name && i.option === it.option);
      if (same) same.qty++; else items.push(it);
      saveCart(); renderCart();
      navHoldUntil = Date.now() + 3500; $('[data-nav]').classList.remove('is-hidden');
      flyToBag(card);
      cartBtn.classList.remove('is-bump'); void cartBtn.offsetWidth; cartBtn.classList.add('is-bump');
      toast((root.dataset.lang === 'en' ? 'Added: ' : 'Agregado: ') + `${it.name} (${it.option})`);
    });
  });
  /* el ramo, en miniatura, viaja hasta "Pedido" */
  const flyToBag = (card) => {
    const img = $('.ramo__img img', card);
    if (!img || !window.gsap || reduced) return;
    const a = img.getBoundingClientRect(), z = cartBtn.getBoundingClientRect();
    const f = img.cloneNode(); f.removeAttribute('srcset'); f.src = img.currentSrc || img.src;
    Object.assign(f.style, { position: 'fixed', left: a.left + 'px', top: a.top + 'px', width: a.width + 'px', height: a.height + 'px', objectFit: 'cover', borderRadius: '24px', zIndex: 140, pointerEvents: 'none' });
    document.body.appendChild(f);
    const s = 56 / a.width;
    gsap.to(f, { x: z.left + z.width / 2 - (a.left + a.width / 2), y: z.top + z.height / 2 - (a.top + a.height / 2), scale: s, borderRadius: '50%', opacity: .2, duration: .9, ease: 'power3.inOut', onComplete: () => f.remove() });
  };
  /* el precio rueda al cambiar de tamaño */
  $$('[data-product]').forEach(card => {
    const out = $('[data-price-out]', card);
    if (!out) return;
    $$('input[type="radio"]', card).forEach(r => r.addEventListener('change', () => {
      const v = clp(parseInt(r.dataset.price, 10));
      if (!window.gsap || reduced) { out.textContent = v; return; }
      gsap.killTweensOf(out);
      gsap.timeline()
        .to(out, { yPercent: -60, opacity: 0, duration: .22, ease: 'power2.in' })
        .call(() => { out.textContent = v; })
        .fromTo(out, { yPercent: 60, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .38, ease: 'power3.out' });
    }));
  });
  const toggleCart = (open) => {
    if (open === cartOpen) return;
    cartOpen = open;
    cartBtn.setAttribute('aria-expanded', String(open));
    outside().forEach(el => { el.inert = open; });
    const panel = $('.cart__panel', cart);
    if (window.gsap) gsap.killTweensOf([panel, $('.cart__scrim', cart)]);
    if (open) {
      renderCart();
      cart.hidden = false;
      lenis && lenis.stop();
      if (window.gsap && !reduced) {
        gsap.fromTo(panel, { xPercent: 100 }, { xPercent: 0, duration: .7, ease: 'power3.inOut' });
        gsap.fromTo($('.cart__scrim', cart), { opacity: 0 }, { opacity: 1, duration: .4 });
      }
      $('.cart__close', cart).focus();
    } else {
      const done = () => { cart.hidden = true; lenis && introDone && lenis.start(); cartBtn.focus(); };
      if (window.gsap && !reduced) {
        gsap.to($('.cart__scrim', cart), { opacity: 0, duration: .35 });
        gsap.to(panel, { xPercent: 100, duration: .5, ease: 'power3.in', onComplete: done });
      } else done();
    }
  };
  cartBtn?.addEventListener('click', () => toggleCart(true));
  $$('[data-cart-close]').forEach(b => b.addEventListener('click', () => toggleCart(false)));
  $('[data-cart-form]')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const f = e.target;
    const lines = [items.length ? 'Hola Floresta, quiero hacer un pedido:' : 'Hola Floresta, quiero cotizar un ramo.'];
    if (items.length) {
      items.forEach(i => lines.push(`· ${i.qty} × ${i.name} (${i.option}) ${clp(i.price * i.qty)}`));
      lines.push(`Total referencial: ${clp(items.reduce((a, i) => a + i.price * i.qty, 0))}`);
    }
    lines.push(`Entrega: ${f.modo.value}`);
    if (f.modo.value === 'Despacho' && f.direccion.value.trim()) lines.push(`Dirección: ${f.direccion.value.trim()}`);
    if (f.fecha.value) { const [y, m, d] = f.fecha.value.split('-'); lines.push(`Fecha: ${d}-${m}-${y}`); }
    if (f.mensaje.value.trim()) lines.push(`Mensaje para la tarjeta: ${f.mensaje.value.trim()}`);
    window.open(`https://wa.me/${WA}?text=${encodeURIComponent(lines.join('\n'))}`, '_blank', 'noopener');
  });
  renderCart();
  document.addEventListener('floresta:lang', renderCart);
  $$('[data-cart-form] input[name="modo"]').forEach(r => r.addEventListener('change', () => { $('[data-addr]').hidden = $('[data-cart-form]').modo.value !== 'Despacho'; }));

  document.addEventListener('keydown', (e) => {
    const box = menuOpen ? menu : cartOpen ? cart : null;
    if (!box) return;
    if (e.key === 'Escape') { menuOpen ? toggleMenu(false) : toggleCart(false); return; }
    if (e.key === 'Tab') trapTab(box, e);
  });

  /* ---------- videos: se cargan al acercarse, se reproducen solo en pantalla ---------- */
  const lazyVideo = (v) => {
    if (v.dataset.loaded) return;
    v.dataset.loaded = '1';
    if (v.dataset.poster) v.poster = v.dataset.poster;
    $$('source[data-src]', v).forEach(s => { s.src = s.dataset.src; });
    v.preload = 'auto';
    v.load();
  };
  let introPlayed = false; /* el video de la portada parte cuando se levanta la precarga */
  const videos = $$('video');
  if ('IntersectionObserver' in window) {
    const near = new IntersectionObserver((en) => en.forEach(e => { if (e.isIntersecting) { lazyVideo(e.target); near.unobserve(e.target); } }), { rootMargin: '900px 0px' });
    const seen = new IntersectionObserver((en) => en.forEach(e => {
      const v = e.target;
      if (e.isIntersecting && !reduced && !v.closest('.ocas__thumb') && (introPlayed || !v.hasAttribute('data-hero-video'))) v.play().catch(() => {});
      else if (!e.isIntersecting) v.pause();
    }), { threshold: .15 });
    videos.forEach(v => { if (v.hasAttribute('data-lazy-video')) near.observe(v); seen.observe(v); });
  } else videos.forEach(lazyVideo);
  if (reduced) videos.forEach(v => { v.removeAttribute('autoplay'); v.pause(); });

  /* ---------- mapa (Leaflet, diferido): el marcador queda anclado a Esmeralda 198 ---------- */
  const mapEl = $('[data-map]');
  const initMap = () => {
    if (!mapEl || mapEl._map || !window.L) return;
    const L = window.L;
    const home = [parseFloat(mapEl.dataset.lat), parseFloat(mapEl.dataset.lng)];
    const zoom = parseInt(mapEl.dataset.zoom || '16', 10);
    const touch = window.matchMedia('(pointer: coarse)').matches;
    const map = L.map(mapEl, { center: home, zoom, minZoom: 9, maxZoom: 18, scrollWheelZoom: false, dragging: !touch, tap: false });
    mapEl._map = map;
    map.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19, subdomains: 'abc',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
    }).addTo(map);
    const pin = L.marker(home, { icon: L.divIcon({ className: 'floresta-pin', html: '<i></i>', iconSize: [22, 22], iconAnchor: [11, 11] }), keyboard: false, title: 'Floresta', alt: 'Floresta' }).addTo(map);
    pin.on('click', () => map.flyTo(home, Math.max(map.getZoom(), 17), { duration: .8 }));
    const Home = L.Control.extend({
      options: { position: 'bottomright' },
      onAdd() {
        const wrap = L.DomUtil.create('div', 'leaflet-control map-home');
        wrap.innerHTML = '<button type="button"><span data-l="es">Volver a la florería</span><span data-l="en">Back to the shop</span></button>';
        L.DomEvent.disableClickPropagation(wrap);
        wrap.querySelector('button').addEventListener('click', () => map.flyTo(home, zoom, { duration: 1 }));
        return wrap;
      }
    });
    map.addControl(new Home());
    const zin = $('.leaflet-control-zoom-in', mapEl), zout = $('.leaflet-control-zoom-out', mapEl);
    const zoomLabels = () => {
      const en = root.dataset.lang === 'en';
      [[zin, en ? 'Zoom in' : 'Acercar'], [zout, en ? 'Zoom out' : 'Alejar']].forEach(([b, t]) => { if (b) { b.setAttribute('aria-label', t); b.title = t; } });
    };
    zoomLabels();
    document.addEventListener('floresta:lang', zoomLabels);
    const hint = $('[data-map-hint]');
    let hintT = 0;
    const showHint = (kind) => { if (!hint) return; hint.dataset.show = kind; hint.classList.add('is-on'); clearTimeout(hintT); hintT = setTimeout(() => hint.classList.remove('is-on'), 1400); };
    mapEl.addEventListener('wheel', () => showHint('wheel'), { passive: true });
    if (touch) {
      mapEl.addEventListener('touchstart', (e) => { if (e.touches.length >= 2) { map.dragging.enable(); hint && hint.classList.remove('is-on'); } else map.dragging.disable(); }, { passive: true });
      mapEl.addEventListener('touchmove', (e) => { if (e.touches.length === 1) showHint('touch'); }, { passive: true });
      mapEl.addEventListener('touchend', (e) => { if (e.touches.length < 2) map.dragging.disable(); }, { passive: true });
    }
    if ('ResizeObserver' in window) new ResizeObserver(() => map.invalidateSize()).observe(mapEl);
  };
  const mapFail = () => {
    mapEl.classList.add('is-failed');
    mapEl.innerHTML = '<a class="u-link t-label" href="https://maps.app.goo.gl/VrV2dyRCbsa9qnkP8" target="_blank" rel="noopener"><span data-l="es">Ver ubicación en Google Maps</span><span data-l="en">See location on Google Maps</span></a>';
  };
  const loadMap = () => {
    if (!mapEl || mapEl.dataset.loading) return;
    mapEl.dataset.loading = '1';
    if (window.L) return initMap();
    const sc = document.createElement('script');
    sc.src = 'vendor/leaflet/leaflet.js';
    sc.onload = () => { try { initMap(); } catch (e) { mapFail(); } };
    sc.onerror = mapFail;
    document.head.appendChild(sc);
  };
  if (mapEl && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((en) => { if (en[0].isIntersecting) { loadMap(); io.disconnect(); } }, { rootMargin: '700px 0px' });
    io.observe(mapEl);
  } else loadMap();

  /* ---------- sliders (Swiper, diferido) ---------- */
  const pad = (n) => String(n).padStart(2, '0');
  const a11yMsgs = () => root.dataset.lang === 'en'
    ? { prevSlideMessage: 'Previous', nextSlideMessage: 'Next', firstSlideMessage: 'First', lastSlideMessage: 'Last', slideLabelMessage: '{{index}} / {{slidesLength}}' }
    : { prevSlideMessage: 'Anterior', nextSlideMessage: 'Siguiente', firstSlideMessage: 'Primero', lastSlideMessage: 'Último', slideLabelMessage: '{{index}} / {{slidesLength}}' };
  let swiperLoading = null;
  const loadSwiper = () => swiperLoading || (swiperLoading = new Promise((res, rej) => {
    if (window.Swiper) return res();
    const sc = document.createElement('script');
    sc.src = 'vendor/swiper/swiper-bundle.min.js'; sc.onload = res; sc.onerror = rej;
    document.head.appendChild(sc);
  }));
  const lazySlider = (el, opts) => {
    if (!el) return;
    const init = () => {
      if (el.swiper || el.dataset.pending) return;
      el.dataset.pending = '1';
      loadSwiper().then(() => {
        const cur = $('[data-count-cur]', el), tot = $('[data-count-tot]', el);
        const total = $$('.swiper-slide', el).length;
        if (tot) tot.textContent = pad(total);
        new Swiper(el, Object.assign({
          slidesPerView: 'auto', spaceBetween: 18, speed: 800, grabCursor: true,
          keyboard: { enabled: true, onlyInViewport: true },
          a11y: Object.assign({ enabled: true }, a11yMsgs()),
          on: {
            slideChange(s) {
              if (!cur) return;
              const n = pad(s.realIndex + 1);
              if (window.gsap && !reduced) gsap.fromTo(cur, { yPercent: 60, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .5, ease: 'power3.inOut', onStart: () => { cur.textContent = n; } });
              else cur.textContent = n;
            }
          }
        }, opts));
      }).catch(() => {}).finally(() => { delete el.dataset.pending; });
    };
    if (!('IntersectionObserver' in window)) return init();
    const io = new IntersectionObserver((en) => { if (en[0].isIntersecting) { io.disconnect(); init(); } }, { rootMargin: '900px 0px' });
    io.observe(el);
  };
  const ramosEl = $('[data-ramos]');
  lazySlider(ramosEl, { spaceBetween: 18, navigation: { prevEl: $('[data-ramos-prev]'), nextEl: $('[data-ramos-next]') }, slidesOffsetAfter: 0 });
  lazySlider($('[data-plants]'), { spaceBetween: 12, freeMode: { enabled: true, momentum: true } });
  document.addEventListener('floresta:lang', () => {
    $$('[data-ramos], [data-plants]').forEach(el => { if (el.swiper) { Object.assign(el.swiper.params.a11y, a11yMsgs()); el.swiper.update(); } });
  });

  /* ---------- ocasiones: la foto de cada fila aparece al pasar ---------- */
  $$('[data-ocas-key]').forEach(row => {
    const v = $('video', row);
    const thumb = $('.ocas__thumb', row);
    let qx = null, qy = null;
    const place = (e) => {
      if (!window.gsap) { thumb.style.translate = `${e.clientX + 24}px ${e.clientY - 120}px`; return; }
      if (!qx) { qx = gsap.quickTo(thumb, 'x', { duration: .55, ease: 'power3.out' }); qy = gsap.quickTo(thumb, 'y', { duration: .55, ease: 'power3.out' }); gsap.set(thumb, { x: e.clientX + 30, y: e.clientY - 140 }); }
      qx(e.clientX + 30); qy(e.clientY - 140);
    };
    const on = (yes, e) => {
      if (!desktop.matches || !fine.matches) return;
      if (yes && e) place(e);
      row.classList.toggle('is-on', yes);
      if (v) { if (yes && !reduced) { lazyVideo(v); v.play().catch(() => {}); } else v.pause(); }
    };
    row.addEventListener('pointerenter', (e) => on(true, e));
    row.addEventListener('pointermove', (e) => { if (row.classList.contains('is-on')) place(e); });
    row.addEventListener('pointerleave', () => on(false));
  });
  desktop.addEventListener('change', () => $$('.ocas__thumb').forEach(t => { t.style.transform = ''; t.style.translate = ''; }));

  /* ---------- etiqueta "Arrastrar" (el cursor nativo sigue visible) ---------- */
  const drag = $('[data-drag]');
  if (drag && fine.matches && !reduced && window.gsap) {
    let dx = 0, dy = 0, tx = 0, ty = 0, raf = 0, shown = false;
    const loop = () => { dx += (tx - dx) * .2; dy += (ty - dy) * .2; drag.style.translate = `${dx}px ${dy}px`; raf = requestAnimationFrame(loop); };
    $$('[data-drag-label]').forEach(zone => {
      zone.addEventListener('pointerenter', (e) => { gsap.killTweensOf(drag); tx = dx = e.clientX; ty = dy = e.clientY; shown = true; cancelAnimationFrame(raf); loop(); gsap.to(drag, { scale: 1, opacity: 1, duration: .5, ease: 'power3.inOut' }); });
      zone.addEventListener('pointermove', (e) => { tx = e.clientX; ty = e.clientY; });
      zone.addEventListener('pointerdown', () => shown && gsap.to(drag, { scale: .82, duration: .3, ease: 'power3.inOut' }));
      zone.addEventListener('pointerup', () => shown && gsap.to(drag, { scale: 1, duration: .4, ease: 'power3.inOut' }));
      zone.addEventListener('pointerleave', () => { shown = false; gsap.to(drag, { scale: 0, opacity: 0, duration: .4, ease: 'power3.inOut', onComplete: () => { if (!shown) cancelAnimationFrame(raf); } }); });
      $$('button, a, label, input', zone).forEach(b => {
        b.addEventListener('pointerenter', () => gsap.to(drag, { scale: 0, opacity: 0, duration: .25 }));
        b.addEventListener('pointerleave', () => shown && gsap.to(drag, { scale: 1, opacity: 1, duration: .4, ease: 'power3.inOut' }));
      });
    });
  }

  /* ---------- botones magnéticos ---------- */
  if (fine.matches && !reduced && window.gsap) {
    $$('[data-magnetic]').forEach(btn => {
      btn.addEventListener('pointermove', (e) => {
        const r = btn.getBoundingClientRect();
        gsap.to(btn, { x: ((e.clientX - r.left) / r.width - .5) * 12, y: ((e.clientY - r.top) / r.height - .5) * 12, duration: .45, ease: 'power3.inOut' });
      });
      btn.addEventListener('pointerleave', () => gsap.to(btn, { x: 0, y: 0, duration: .7, ease: 'power3.inOut' }));
    });
  }

  /* ---------- barra blanca mientras se ve la portada ---------- */
  const heroEl = $('[data-hero]');
  if (heroEl && 'IntersectionObserver' in window) {
    new IntersectionObserver((en) => $('[data-nav]').classList.toggle('on-hero', en[0].isIntersecting), { rootMargin: '-40px 0px -100% 0px' }).observe(heroEl);
  }

  /* ---------- Debes saber: notas que se abren y se cierran ---------- */
  $$('[data-acc] details').forEach(d => {
    const sum = $('summary', d), body = $('.acc', d);
    sum.addEventListener('click', (e) => {
      if (!window.gsap || reduced) return;
      e.preventDefault();
      gsap.killTweensOf(body);
      if (d.open) {
        gsap.to(body, { height: 0, opacity: 0, duration: .45, ease: 'power3.inOut', onComplete: () => { d.open = false; gsap.set(body, { clearProps: 'height,opacity' }); ScrollTrigger.refresh(); } });
      } else {
        d.open = true;
        gsap.fromTo(body, { height: 0, opacity: 0 }, { height: 'auto', opacity: 1, duration: .55, ease: 'power3.inOut', onComplete: () => { gsap.set(body, { clearProps: 'height' }); ScrollTrigger.refresh(); } });
      }
    });
  });

  /* ---------- Esmeralda 198: once ramos, un solo letrero ---------- */
  const esm = $('[data-esm]');
  const frames = esm ? $$('[data-esm-frame] img', esm) : [];
  const curEl = $('[data-esm-cur]');
  if ($('[data-esm-tot]')) $('[data-esm-tot]').textContent = pad(frames.length);
  let esmIdx = 0;
  const showFrame = (i) => {
    i = Math.max(0, Math.min(frames.length - 1, i));
    if (i === esmIdx) return;
    frames[esmIdx].classList.remove('is-on');
    frames[i].classList.add('is-on');
    esmIdx = i;
    if (curEl) curEl.textContent = pad(i + 1);
  };
  const esmBar = $('[data-esm-bar]');

  /* ---------- sin movimiento: todo visible, sin Lenis ---------- */
  if (reduced || !window.gsap || !window.ScrollTrigger) {
    $('.loader')?.remove();
    clearTimeout(loaderSafety);
    root.classList.add('no-motion');
    if (!reduced) { introPlayed = true; $('[data-hero-video]')?.play().catch(() => {}); }
    if (window.gsap && window.ScrollTrigger) { gsap.registerPlugin(ScrollTrigger); navTheme(); }
    return;
  }

  gsap.registerPlugin(ScrollTrigger);
  gsap.defaults({ ease: 'power3.inOut', duration: .8 });

  if (window.Lenis) {
    lenis = new Lenis({ lerp: .1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    lenis.stop();
  }

  /* ---------- división en líneas para revelados con máscara ---------- */
  const splitLines = (el) => {
    const targets = $$(':scope > [data-l]', el).length ? $$(':scope > [data-l]', el) : [el];
    targets.forEach(t => {
      if (!t.dataset.raw) t.dataset.raw = t.innerHTML;
      t.innerHTML = t.dataset.raw;
      if (getComputedStyle(t).display === 'none') return;
      /* se respetan los elementos en línea (p. ej. <em> en script) */
      const walk = [];
      t.childNodes.forEach(n => {
        if (n.nodeType === 3) n.textContent.split(/(\s+)/).forEach(w => { if (w.trim()) walk.push({ text: w, wrap: null }); });
        else if (n.nodeType === 1) n.textContent.split(/\s+/).forEach(w => { if (w) walk.push({ text: w, wrap: n }); });
      });
      const esc = (x) => x.replace(/&/g, '&amp;').replace(/</g, '&lt;');
      const tag = (w) => w.wrap ? `<${w.wrap.tagName.toLowerCase()} class="${w.wrap.className}">${esc(w.text)}</${w.wrap.tagName.toLowerCase()}>` : esc(w.text);
      t.innerHTML = walk.map((w, i) => `<span class="w" data-i="${i}">${tag(w)}</span>`).join(' ');
      const lines = []; let top = null;
      $$('.w', t).forEach(w => {
        const y = w.offsetTop;
        if (top === null || Math.abs(y - top) > 6) { lines.push([]); top = y; }
        lines[lines.length - 1].push(tag(walk[+w.dataset.i]));
      });
      t.innerHTML = lines.map(l => `<span class="line"><span>${l.join(' ')} </span></span>`).join('');
    });
  };
  const revealTweens = [];
  const buildReveals = (rebuild = false) => {
    revealTweens.forEach(t => { t.scrollTrigger && t.scrollTrigger.kill(); t.kill(); });
    revealTweens.length = 0;
    $$('[data-lines]').forEach(el => {
      try { splitLines(el); } catch (e) { return; }
      const inner = $$('.line > span', el).filter(s => s.offsetParent);
      if (!inner.length) return;
      if (rebuild && el.getBoundingClientRect().top < window.innerHeight * .9) return;
      revealTweens.push(gsap.fromTo(inner, { yPercent: 108 }, { yPercent: 0, duration: 1, stagger: .07, ease: 'power3.inOut', scrollTrigger: { trigger: el, start: 'top 90%', once: true } }));
    });
  };

  /* ---------- precarga + entrada de la portada ---------- */
  const loader = $('.loader');
  const fontsReady = document.fonts
    ? Promise.race([Promise.allSettled(['400 1em Allura', '400 1em Catamaran', '600 1em Catamaran', '700 1em Catamaran', '400 1em "Playfair Display"', 'italic 400 1em "Playfair Display"'].map(f => document.fonts.load(f))), new Promise(r => setTimeout(r, 2500))]).catch(() => {})
    : Promise.resolve();
  if (loader) outside().forEach(el => { el.inert = true; });
  gsap.set('[data-hero-fade]', { opacity: 0, y: 18 });
  gsap.set('.hero__logo .logo-mask', { yPercent: 102 });
  gsap.set('[data-hero-motto] span', { opacity: 0, y: 26 });
  gsap.set('[data-hero-media]', { clipPath: 'inset(8% 6% 8% 6% round 40px)' });
  gsap.set('[data-hero-media] img', { scale: 1.22 });

  const prefetchRest = () => {
    const conn = navigator.connection || {};
    if (conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '')) return;
    const imgs = $$('img[loading="lazy"]').filter(i => !i.closest('[data-menu]'));
    const next = () => {
      const img = imgs.shift();
      if (!img) return;
      if (img.complete && img.naturalWidth) return next();
      img.addEventListener('load', next, { once: true });
      img.addEventListener('error', next, { once: true });
      img.loading = 'eager';
    };
    (window.requestIdleCallback || ((fn) => setTimeout(fn, 300)))(() => { next(); next(); });
  };

  /* portada: la precarga sube, el ramo se abre a pantalla completa, el logo emerge */
  finishIntro = () => {
    if (introDone) return;
    introDone = true;
    clearTimeout(loaderSafety);
    buildReveals();
    const tl = gsap.timeline({ defaults: { ease: 'power3.inOut' }, onComplete: () => { loader && loader.remove(); prefetchRest(); gsap.set('[data-hero-media]', { clearProps: 'clipPath' }); } });
    tl.to(loader, { yPercent: -100, duration: .9, ease: 'power4.inOut' })
      .call(() => { if (loader) loader.style.pointerEvents = 'none'; outside().forEach(el => { el.inert = menuOpen || cartOpen; }); lenis && !menuOpen && !cartOpen && lenis.start(); }, null, .7)
      .to('[data-hero-media]', { clipPath: 'inset(0% 0% 0% 0% round 0px)', duration: 1.25 }, .35)
      .to('[data-hero-media] img', { scale: 1.06, duration: 1.6 }, .35)
      .to('.hero__logo .logo-mask', { yPercent: 0, duration: 1.1 }, .85)
      .to('[data-hero-motto] span', { opacity: 1, y: 0, duration: .8, stagger: .12 }, 1.1)
      .to('[data-hero-fade]', { opacity: 1, y: 0, duration: .7 }, 1.35);
    ScrollTrigger.refresh();
  };
  const minShow = new Promise(r => setTimeout(r, Math.max(0, 1200 - performance.now())));
  Promise.all([critical.reached, fontsReady, minShow]).then(() => {
    gsap.timeline({ onComplete: () => finishIntro() })
      .to('.loader__pct', { opacity: 0, y: -8, duration: .3, ease: 'power2.in' })
      .to('.loader__full', { opacity: 1, duration: .5, ease: 'power2.inOut' }, '-=.1')
      .to({}, { duration: .25 });
  }, () => finishIntro());

  /* al bajar: el ramo se queda atrás y el texto se adelanta */
  gsap.timeline({ scrollTrigger: { trigger: '[data-hero]', start: 'top top', end: 'bottom top', scrub: .4 } })
    .to('[data-hero-media]', { yPercent: 22, ease: 'none' }, 0)
    .to('.hero__content', { yPercent: -40, opacity: 0, ease: 'none' }, 0);

  /* ---------- fotos que se descubren (cortina) y masas a distinta velocidad ---------- */
  const fromClip = { left: 'inset(0% 100% 0% 0%)', right: 'inset(0% 0% 0% 100%)', '': 'inset(100% 0% 0% 0%)' };
  $$('[data-reveal]').forEach(fig => {
    const img = $('img, video', fig);
    const dir = fig.dataset.reveal || '';
    gsap.timeline({ scrollTrigger: { trigger: fig, start: 'top 82%', once: true } })
      .fromTo(fig, { clipPath: fromClip[dir] || fromClip[''] }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.1, ease: 'power4.inOut', clearProps: 'clipPath' })
      .fromTo(img || {}, { scale: 1.25 }, { scale: 1, duration: 1.4, ease: 'power3.inOut' }, 0);
  });
  const mmSpeed = gsap.matchMedia();
  mmSpeed.add('(min-width: 900px)', () => {
    $$('[data-speed]').forEach(el => {
      const sp = parseFloat(el.dataset.speed) || 0;
      gsap.fromTo(el, { yPercent: -sp }, { yPercent: sp, ease: 'none', scrollTrigger: { trigger: el.closest('section'), start: 'top bottom', end: 'bottom top', scrub: .6 } });
    });
  });
  $$('[data-parallax-in]').forEach(img => {
    gsap.fromTo(img, { yPercent: -4 }, { yPercent: 4, ease: 'none', scrollTrigger: { trigger: img.closest('section'), start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* ---------- cinta de ramos: corre sola, acelera con el scroll, se calma con el cursor ---------- */
  const track = $('[data-cinta]');
  if (track) {
    const set = $('.cinta__set', track);
    const clone = set.cloneNode(true);
    clone.setAttribute('aria-hidden', 'true');
    $$('img', clone).forEach(i => { i.alt = ''; i.removeAttribute('data-alt-en'); i.loading = 'lazy'; });
    track.appendChild(clone);
    let x = 0, speed = 0.6, target = 0.6, boost = 0, w = set.offsetWidth, visible = false;
    new ResizeObserver(() => { w = set.offsetWidth; }).observe(set);
    new IntersectionObserver((en) => { visible = en[0].isIntersecting; }).observe(track);
    track.addEventListener('pointerenter', () => { target = 0.12; });
    track.addEventListener('pointerleave', () => { target = 0.6; });
    if (lenis) lenis.on('scroll', (e) => { boost = Math.min(6, Math.abs(e.velocity) * .35); });
    gsap.ticker.add((t, dt) => {
      if (!visible) return;
      speed += (target + boost - speed) * .06; boost *= .92;
      x -= speed * dt * .06;
      if (-x >= w) x += w;
      track.style.transform = `translate3d(${x}px,0,0)`;
    });
  }

  /* ---------- ramos: entran como mazo que se reparte ---------- */
  gsap.fromTo('.ramo', { opacity: 0, y: 60, rotate: (i) => [-3, 2, -1.5, 2.5, -2][i % 5] }, { opacity: 1, y: 0, rotate: 0, stagger: .08, duration: .9, ease: 'power3.inOut', scrollTrigger: { trigger: '.ramos__slider', start: 'top 85%', once: true } });

  /* ---------- Esmeralda 198: sticky sin pin; el progreso elige el ramo ---------- */
  if (esm && frames.length) {
    const per = () => window.innerHeight * .55;
    const size = () => { esm.style.height = (frames.length * per() + window.innerHeight) + 'px'; };
    size();
    ScrollTrigger.addEventListener('refreshInit', size);
    ScrollTrigger.create({
      trigger: esm, start: 'top top', end: 'bottom bottom',
      onUpdate: (self) => { showFrame(Math.floor(self.progress * frames.length * .999)); if (esmBar) esmBar.style.transform = `scaleX(${self.progress})`; }
    });
    gsap.fromTo('[data-esm-frame]', { clipPath: 'inset(14% 10% 14% 10% round 40px)' }, { clipPath: 'inset(0% 0% 0% 0% round 0px)', ease: 'power2.inOut', scrollTrigger: { trigger: esm, start: 'top bottom', end: 'top top', scrub: .5 } });
  }

  /* ---------- invierno: la tarjeta se abre a pantalla completa ---------- */
  const inv = $('[data-invierno]');
  if (inv) {
    const mmInv = gsap.matchMedia();
    mmInv.add({ d: '(min-width: 900px)', m: '(max-width: 899px)' }, (ctx) => {
      gsap.timeline({ scrollTrigger: { trigger: inv, start: 'top top', end: 'bottom bottom', scrub: .5 } })
        .fromTo('[data-invierno-card]', { clipPath: ctx.conditions.d ? 'inset(9% 7% 9% 7% round 40px)' : 'inset(6% 4% 6% 4% round 28px)' }, { clipPath: 'inset(0% 0% 0% 0% round 0px)', ease: 'power2.inOut' }, 0)
        .fromTo('.invierno__media img', { scale: 1.16 }, { scale: 1, ease: 'power2.inOut' }, 0);
    });
  }

  /* ---------- detalles que acompañan ---------- */
  gsap.fromTo('.saber details', { opacity: 0, y: 26 }, { opacity: 1, y: 0, stagger: .07, duration: .7, scrollTrigger: { trigger: '.saber__list', start: 'top 85%', once: true } });
  gsap.fromTo('.ocas__row', { opacity: 0, y: 24 }, { opacity: 1, y: 0, stagger: .07, duration: .7, scrollTrigger: { trigger: '.ocas__list', start: 'top 85%', once: true } });
  gsap.fromTo('.resenas__stars i', { scale: 0, rotate: -40 }, { scale: 1, rotate: 0, stagger: .08, duration: .6, ease: 'back.inOut(2)', scrollTrigger: { trigger: '.resenas', start: 'top 75%', once: true } });
  gsap.fromTo('.resena', { opacity: 0, y: 40 }, { opacity: 1, y: 0, stagger: .12, duration: .8, scrollTrigger: { trigger: '.resenas', start: 'top 75%', once: true } });
  gsap.fromTo('.plant', { opacity: 0, x: 60 }, { opacity: 1, x: 0, stagger: .06, duration: .8, scrollTrigger: { trigger: '.jardin__strip', start: 'top 90%', once: true } });

  /* ---------- conservar la posición al cruzar el quiebre móvil/escritorio ---------- */
  desktop.addEventListener('change', () => {
    const a = anchor;
    const target = () => a ? a.sec.getBoundingClientRect().top + window.scrollY + a.ratio * a.sec.offsetHeight : (resizeFromY !== null ? resizeFromY : stableY);
    const go = () => { const y = target(); if (Math.abs(window.scrollY - y) < 40) return; if (lenis) lenis.scrollTo(y, { immediate: true, force: true }); else window.scrollTo(0, y); stableY = y; ScrollTrigger.update(); };
    restoring = true;
    requestAnimationFrame(() => requestAnimationFrame(go)); setTimeout(go, 450); setTimeout(() => { go(); restoring = false; }, 1000);
  });

  /* ---------- navegación: se esconde al bajar, cambia de tono sobre fondos claros ---------- */
  navTheme();
  const nav = $('[data-nav]');
  $$('.nav__pill a').forEach(a => {
    const sec = $(a.getAttribute('href'));
    if (!sec) return;
    ScrollTrigger.create({ trigger: sec, start: 'top 50%', end: 'bottom 50%', onToggle: (s) => a.classList.toggle('is-active', s.isActive) });
  });
  ScrollTrigger.create({
    start: 'top -120',
    onUpdate: (self) => { nav.classList.toggle('is-hidden', self.direction === 1 && !menuOpen && !cartOpen && Date.now() > navHoldUntil); nav.classList.toggle('is-scrolled', self.scroll() > 120); },
    onLeaveBack: () => nav.classList.remove('is-scrolled')
  });
  function navTheme() { /* v4: el tono de la barra lo decide la portada (on-hero) */ }

  /* ---------- re-división de líneas al cambiar idioma o ancho ---------- */
  let rz, lastW = window.innerWidth;
  const rebuild = () => { buildReveals(true); ScrollTrigger.refresh(); };
  document.addEventListener('floresta:lang', () => {
    if (!introDone) return;
    rebuild();
    $$('.line > span').forEach(s => { if (s.getBoundingClientRect().top < window.innerHeight) gsap.set(s, { yPercent: 0 }); });
  });
  window.addEventListener('resize', () => {
    if (Math.abs(window.innerWidth - lastW) < 2) return;
    lastW = window.innerWidth;
    clearTimeout(rz); rz = setTimeout(() => { if (introDone) rebuild(); }, 250);
  });
})();
