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
  const critical = window.__floresta || { done: Promise.resolve(), reached: Promise.resolve() };
  let finishIntro = () => { const l = $('.loader'); if (l) l.remove(); };
  const loaderSafety = setTimeout(() => finishIntro(), 9000);

  /* posición estable del scroll mientras la ventana cambia de tamaño */
  let stableY = window.scrollY, resizing = false, resizeT = 0, resizeFromY = null;
  window.addEventListener('scroll', () => { if (!resizing) stableY = window.scrollY; }, { passive: true });
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
  setLang(store.get('floresta-lang') === 'en' ? 'en' : 'es');
  $('[data-lang-toggle]')?.addEventListener('click', () => setLang(root.dataset.lang === 'es' ? 'en' : 'es'));

  /* ---------- scroll suave ---------- */
  let lenis = null;
  const scrollToEl = (el) => {
    if (!el) return;
    if (lenis) lenis.scrollTo(el, { duration: 1.5, easing: t => 1 - Math.pow(1 - t, 4) });
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
  const toggleMenu = (open) => {
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
        gsap.fromTo($$('.menu__w', menu), { yPercent: 110 }, { yPercent: 0, duration: .8, stagger: .05, ease: 'expo.out', delay: .3 });
      } else menu.style.clipPath = 'none';
      $('[data-menu-close]').focus();
    } else {
      const done = () => { menu.hidden = true; lenis && lenis.start(); openBtn.focus(); };
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
      toggleMenu(false);
      setTimeout(() => { scrollToEl(t); focusTarget(t); }, reduced ? 0 : 450);
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
        it.qty += parseInt(b.dataset.q, 10);
        if (it.qty <= 0) items.splice(idx, 1);
        saveCart(); renderCart();
        const again = $$('[data-cart-items] button')[0];
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
      cartBtn.classList.remove('is-bump'); void cartBtn.offsetWidth; cartBtn.classList.add('is-bump');
      toast((root.dataset.lang === 'en' ? 'Added: ' : 'Agregado: ') + `${it.name} (${it.option})`);
    });
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
        gsap.fromTo(panel, { xPercent: 100 }, { xPercent: 0, duration: .7, ease: 'expo.out' });
        gsap.fromTo($('.cart__scrim', cart), { opacity: 0 }, { opacity: 1, duration: .4 });
      }
      $('.cart__close', cart).focus();
    } else {
      const done = () => { cart.hidden = true; lenis && lenis.start(); cartBtn.focus(); };
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
    const lines = ['Hola Floresta, quiero hacer un pedido:'];
    if (items.length) {
      items.forEach(i => lines.push(`· ${i.qty} × ${i.name} (${i.option}) ${clp(i.price * i.qty)}`));
      lines.push(`Total referencial: ${clp(items.reduce((a, i) => a + i.price * i.qty, 0))}`);
    }
    lines.push(`Entrega: ${f.modo.value}`);
    if (f.fecha.value) { const [y, m, d] = f.fecha.value.split('-'); lines.push(`Fecha: ${d}-${m}-${y}`); }
    if (f.mensaje.value.trim()) lines.push(`Mensaje para la tarjeta: ${f.mensaje.value.trim()}`);
    window.open(`https://wa.me/${WA}?text=${encodeURIComponent(lines.join('\n'))}`, '_blank', 'noopener');
  });
  renderCart();
  document.addEventListener('floresta:lang', renderCart);

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
  const videos = $$('video');
  if ('IntersectionObserver' in window) {
    const near = new IntersectionObserver((en) => en.forEach(e => { if (e.isIntersecting) { lazyVideo(e.target); near.unobserve(e.target); } }), { rootMargin: '900px 0px' });
    const seen = new IntersectionObserver((en) => en.forEach(e => {
      const v = e.target;
      if (e.isIntersecting && !reduced && !v.closest('.ocas__thumb')) v.play().catch(() => {});
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
              if (window.gsap && !reduced) gsap.fromTo(cur, { yPercent: 60, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .5, ease: 'expo.out', onStart: () => { cur.textContent = n; } });
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
    const on = (yes) => {
      if (!desktop.matches) return;
      row.classList.toggle('is-on', yes);
      if (v) { if (yes && !reduced) { lazyVideo(v); v.play().catch(() => {}); } else v.pause(); }
    };
    row.addEventListener('pointerenter', () => on(true));
    row.addEventListener('pointerleave', () => on(false));
  });

  /* ---------- etiqueta "Arrastrar" (el cursor nativo sigue visible) ---------- */
  const drag = $('[data-drag]');
  if (drag && fine.matches && !reduced && window.gsap) {
    let dx = 0, dy = 0, tx = 0, ty = 0, raf = 0, shown = false;
    const loop = () => { dx += (tx - dx) * .2; dy += (ty - dy) * .2; drag.style.translate = `${dx}px ${dy}px`; raf = requestAnimationFrame(loop); };
    $$('[data-drag-label]').forEach(zone => {
      zone.addEventListener('pointerenter', (e) => { tx = dx = e.clientX; ty = dy = e.clientY; shown = true; cancelAnimationFrame(raf); loop(); gsap.to(drag, { scale: 1, opacity: 1, duration: .5, ease: 'expo.out' }); });
      zone.addEventListener('pointermove', (e) => { tx = e.clientX; ty = e.clientY; });
      zone.addEventListener('pointerdown', () => shown && gsap.to(drag, { scale: .82, duration: .3, ease: 'expo.out' }));
      zone.addEventListener('pointerup', () => shown && gsap.to(drag, { scale: 1, duration: .4, ease: 'expo.out' }));
      zone.addEventListener('pointerleave', () => { shown = false; gsap.to(drag, { scale: 0, opacity: 0, duration: .4, ease: 'expo.out', onComplete: () => cancelAnimationFrame(raf) }); });
      $$('button, a, label, input', zone).forEach(b => {
        b.addEventListener('pointerenter', () => gsap.to(drag, { scale: 0, opacity: 0, duration: .25 }));
        b.addEventListener('pointerleave', () => shown && gsap.to(drag, { scale: 1, opacity: 1, duration: .4, ease: 'expo.out' }));
      });
    });
  }

  /* ---------- botones magnéticos ---------- */
  if (fine.matches && !reduced && window.gsap) {
    $$('[data-magnetic]').forEach(btn => {
      btn.addEventListener('pointermove', (e) => {
        const r = btn.getBoundingClientRect();
        gsap.to(btn, { x: ((e.clientX - r.left) / r.width - .5) * 12, y: ((e.clientY - r.top) / r.height - .5) * 12, duration: .45, ease: 'expo.out' });
      });
      btn.addEventListener('pointerleave', () => gsap.to(btn, { x: 0, y: 0, duration: .7, ease: 'expo.out' }));
    });
  }

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

  /* ---------- sin movimiento: todo visible, sin Lenis ---------- */
  if (reduced || !window.gsap || !window.ScrollTrigger) {
    $('.loader')?.remove();
    clearTimeout(loaderSafety);
    root.classList.add('no-motion');
    if (window.gsap && window.ScrollTrigger) { gsap.registerPlugin(ScrollTrigger); navTheme(); }
    return;
  }

  gsap.registerPlugin(ScrollTrigger);
  gsap.defaults({ ease: 'expo.out', duration: .9 });

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
      t.innerHTML = lines.map(l => `<span class="line"><span>${l.join(' ')}</span></span>`).join('');
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
      revealTweens.push(gsap.fromTo(inner, { yPercent: 108 }, { yPercent: 0, duration: 1, stagger: .07, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 90%', once: true } }));
    });
  };

  /* ---------- precarga + entrada de la portada ---------- */
  const loader = $('.loader');
  const fontsReady = document.fonts
    ? Promise.race([Promise.allSettled(['400 1em Allura', '400 1em Catamaran', '600 1em Catamaran', '700 1em Catamaran'].map(f => document.fonts.load(f))), new Promise(r => setTimeout(r, 2500))]).catch(() => {})
    : Promise.resolve();
  gsap.set('[data-hero-fade]', { opacity: 0, y: 14 });
  gsap.set('.hero__logo img', { yPercent: 104 });
  gsap.set('[data-hero-motto] span', { opacity: 0, y: 24, filter: 'blur(6px)' });
  gsap.set('[data-hero-sign]', { clipPath: 'circle(0% at 50% 50%)' });

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

  let introDone = false;
  finishIntro = () => {
    if (introDone) return;
    introDone = true;
    clearTimeout(loaderSafety);
    buildReveals();
    const tl = gsap.timeline({ onComplete: () => { loader && loader.remove(); prefetchRest(); } });
    tl.to(loader, { clipPath: 'inset(0 0 100% 0)', duration: 1, ease: 'power3.inOut' })
      .call(() => { if (loader) loader.style.pointerEvents = 'none'; lenis && lenis.start(); }, null, .9)
      .to('[data-hero-sign]', { clipPath: 'circle(50% at 50% 50%)', duration: 1.6, ease: 'expo.out' }, '-=.45')
      .fromTo('.hero__video', { scale: 1.3 }, { scale: 1.04, duration: 2.2, ease: 'expo.out' }, '<')
      .to('.hero__logo img', { yPercent: 0, duration: 1.2, ease: 'expo.out' }, '<.1')
      .to('[data-hero-motto] span', { opacity: 1, y: 0, filter: 'blur(0px)', duration: 1, stagger: .16, ease: 'expo.out' }, '<.25')
      .to('[data-hero-fade]', { opacity: 1, y: 0, duration: .9, stagger: .08, ease: 'expo.out' }, '<.2');
    ScrollTrigger.refresh();
  };
  const minShow = new Promise(r => setTimeout(r, Math.max(0, 1300 - performance.now())));
  Promise.all([critical.reached, fontsReady, minShow]).then(() => {
    gsap.timeline({ onComplete: () => finishIntro() })
      .to('.loader__pct', { opacity: 0, y: -8, duration: .35, ease: 'power2.in' })
      .to('.loader__full', { opacity: 1, duration: .6, ease: 'power2.out' }, '-=.1')
      .to({}, { duration: .3 });
  }, () => finishIntro());

  /* portada: al salir, el letrero se hunde y el texto se va */
  gsap.timeline({ scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } })
    .to('[data-hero-sign]', { yPercent: 14, scale: .92, ease: 'none' }, 0)
    .to('.hero__text', { yPercent: -16, opacity: .2, ease: 'none' }, 0);

  /* ---------- manifiesto: masas a distinta velocidad ---------- */
  $$('.masa').forEach((m, i) => {
    const s = parseFloat(m.dataset.speed || 0);
    gsap.fromTo(m, { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: 1.2, ease: 'expo.out', delay: i * .08, scrollTrigger: { trigger: '.manif', start: 'top 70%', once: true } });
    gsap.fromTo(m, { yPercent: -s }, { yPercent: s, ease: 'none', scrollTrigger: { trigger: '.manif', start: 'top bottom', end: 'bottom top', scrub: .6 } });
  });

  /* ---------- Esmeralda 198: sticky sin pin; el progreso elige el ramo ---------- */
  if (esm && frames.length) {
    const per = () => window.innerHeight * .55;
    const size = () => { esm.style.height = (frames.length * per() + window.innerHeight) + 'px'; };
    size();
    ScrollTrigger.addEventListener('refreshInit', size);
    ScrollTrigger.create({
      trigger: esm, start: 'top top', end: 'bottom bottom',
      onUpdate: (self) => showFrame(Math.floor(self.progress * frames.length * .999))
    });
    gsap.fromTo('[data-esm-frame]', { clipPath: 'inset(12% 12% 12% 12%)' }, { clipPath: 'inset(0% 0% 0% 0%)', ease: 'none', scrollTrigger: { trigger: esm, start: 'top bottom', end: 'top top', scrub: .5 } });
  }

  /* ---------- imágenes con cortina y parallax ---------- */
  $$('[data-clip]').forEach(fig => {
    const img = $('img', fig);
    gsap.timeline({ scrollTrigger: { trigger: fig, start: 'top 85%', once: true } })
      .fromTo(fig, { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: 1.2, ease: 'expo.out' })
      .fromTo(img, { scale: 1.14 }, { scale: 1, duration: 1.7, ease: 'expo.out' }, 0);
  });
  $$('[data-parallax-in]').forEach(img => {
    gsap.fromTo(img, { yPercent: -4 }, { yPercent: 4, ease: 'none', scrollTrigger: { trigger: img.closest('section'), start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  $$('[data-parallax-bg]').forEach(m => {
    gsap.fromTo(m, { yPercent: -6 }, { yPercent: 6, ease: 'none', scrollTrigger: { trigger: m.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  gsap.fromTo('.jardin__oval', { clipPath: 'inset(50% 0 50% 0 round 50%)' }, { clipPath: 'inset(0% 0 0% 0 round 50%)', duration: 1.4, ease: 'expo.out', scrollTrigger: { trigger: '.jardin', start: 'top 70%', once: true } });
  gsap.fromTo('.blob', { scale: .6, rotate: -20, opacity: 0 }, { scale: 1, rotate: 0, opacity: 1, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: '.saber', start: 'top 70%', once: true } });
  gsap.fromTo('.saber__list > div', { opacity: 0, y: 24 }, { opacity: 1, y: 0, stagger: .08, duration: .9, ease: 'expo.out', scrollTrigger: { trigger: '.saber__list', start: 'top 85%', once: true } });
  gsap.fromTo('.ocas__row', { opacity: 0, x: -20 }, { opacity: 1, x: 0, stagger: .07, duration: .9, ease: 'expo.out', scrollTrigger: { trigger: '.ocas__list', start: 'top 85%', once: true } });
  gsap.fromTo('.ramo', { opacity: 0, y: 40 }, { opacity: 1, y: 0, stagger: .08, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.ramos__slider', start: 'top 85%', once: true } });
  gsap.fromTo('.resenas__num', { yPercent: 40, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: '.resenas', start: 'top 70%', once: true } });
  $$('.engrave').forEach(e => gsap.fromTo(e, { yPercent: 6 }, { yPercent: -6, ease: 'none', scrollTrigger: { trigger: e.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } }));

  /* ---------- conservar la posición al cruzar el quiebre móvil/escritorio ---------- */
  desktop.addEventListener('change', () => {
    const y = resizeFromY !== null ? resizeFromY : stableY;
    const go = () => { if (Math.abs(window.scrollY - y) < 40) return; if (lenis) lenis.scrollTo(y, { immediate: true, force: true }); else window.scrollTo(0, y); stableY = y; ScrollTrigger.update(); };
    requestAnimationFrame(() => requestAnimationFrame(go)); setTimeout(go, 450); setTimeout(go, 1000);
  });

  /* ---------- navegación: se esconde al bajar, cambia de tono sobre fondos claros ---------- */
  navTheme();
  const nav = $('[data-nav]');
  ScrollTrigger.create({
    start: 'top -120',
    onUpdate: (self) => { nav.classList.toggle('is-hidden', self.direction === 1 && !menuOpen && !cartOpen); nav.classList.toggle('is-scrolled', self.scroll() > 120); },
    onLeaveBack: () => nav.classList.remove('is-scrolled')
  });
  function navTheme() {
    const nav = $('[data-nav]');
    $$('[data-theme="light"]').forEach(sec => {
      ScrollTrigger.create({ trigger: sec, start: 'top 40px', end: 'bottom 40px', onToggle: (s) => nav.classList.toggle('on-light', s.isActive) });
    });
  }

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
