/*
 LA FLORESTA · Descarga de Instagram desde el navegador (método que SÍ funcionó)
 ===============================================================================
 Instagram bloquea (429) su API a scripts externos, pero la página de perfil, abierta
 con tu sesión, sí recibe todas las publicaciones. Este script "escucha" esas respuestas
 mientras bajas por el perfil y luego empaqueta todo en ZIPs.

 PASOS
 1. Abre https://www.instagram.com/florestaenchiloe/ con tu sesión iniciada.
 2. F12 -> pestaña Consola -> pega TODO este archivo -> Enter.
 3. Baja con la rueda del mouse hasta el final del perfil (o deja que auto-scroll lo haga;
    si la pestaña queda en segundo plano, Chrome lo pausa: mantenla visible).
 4. Cuando la consola diga "FIN", escribe:  floresta.descargar()
    -> floresta_textos.json, floresta_fotos.zip, floresta_videos_1.zip, floresta_videos_2.zip
*/
(() => {
  const media = {};
  const harvest = (o) => {
    if (!o || typeof o !== 'object') return;
    if (o.code && o.taken_at && (o.image_versions2 || o.video_versions || o.carousel_media)) {
      const items = o.carousel_media || [o];
      media[o.code] = {
        code: o.code, taken: o.taken_at, cap: (o.caption && o.caption.text) || '', likes: o.like_count,
        items: items.map(c => ({ img: c.image_versions2?.candidates?.[0]?.url, vid: c.video_versions?.[0]?.url })),
      };
    }
    for (const k in o) if (o[k] && typeof o[k] === 'object') harvest(o[k]);
  };
  const oo = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (m, u) {
    this.addEventListener('load', () => { try { if (/graphql|api\/v1/.test(u)) harvest(JSON.parse(this.responseText)); } catch (e) {} });
    return oo.apply(this, arguments);
  };
  const of = window.fetch;
  window.fetch = async function (...a) {
    const r = await of.apply(this, a);
    try { const u = String(a[0]?.url || a[0]); if (/graphql|api\/v1/.test(u)) r.clone().text().then(t => { try { harvest(JSON.parse(t)); } catch (e) {} }); } catch (e) {}
    return r;
  };

  // auto-scroll
  let last = 0, stall = 0;
  const iv = setInterval(() => {
    window.scrollTo(0, document.body.scrollHeight);
    const n = Object.keys(media).length;
    if (n === last) stall++; else { stall = 0; last = n; console.log('publicaciones:', n); }
    if (stall > 20) { clearInterval(iv); console.log('FIN ->', n, 'publicaciones. Ejecuta floresta.descargar()'); }
  }, 2500);

  // ZIP sin compresión (store) — sin librerías
  const T = new Uint32Array(256);
  for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; T[n] = c >>> 0; }
  const crc = (u8) => { let c = 0xFFFFFFFF; for (let i = 0; i < u8.length; i++) c = T[(c ^ u8[i]) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; };
  const save = (blob, name) => { const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); };
  const zip = async (entries, name) => {
    const parts = [], central = [], enc = new TextEncoder(); let off = 0, i = 0;
    for (const e of entries) {
      let data; try { data = new Uint8Array(await (await fetch(e.url)).arrayBuffer()); } catch (x) { continue; }
      const c32 = crc(data), nm = enc.encode(e.name);
      const h = new DataView(new ArrayBuffer(30)); h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint32(14, c32, true); h.setUint32(18, data.length, true); h.setUint32(22, data.length, true); h.setUint16(26, nm.length, true);
      parts.push(h.buffer, nm, data);
      const c = new DataView(new ArrayBuffer(46)); c.setUint32(0, 0x02014b50, true); c.setUint16(4, 20, true); c.setUint16(6, 20, true); c.setUint32(16, c32, true); c.setUint32(20, data.length, true); c.setUint32(24, data.length, true); c.setUint16(28, nm.length, true); c.setUint32(42, off, true);
      central.push(c.buffer, nm); off += 30 + nm.length + data.length;
      if (++i % 50 === 0) console.log(name, i, '/', entries.length);
    }
    let cs = 0; central.forEach(b => cs += b.byteLength);
    const eo = new DataView(new ArrayBuffer(22)); const n = central.length / 2;
    eo.setUint32(0, 0x06054b50, true); eo.setUint16(8, n, true); eo.setUint16(10, n, true); eo.setUint32(12, cs, true); eo.setUint32(16, off, true);
    save(new Blob([...parts, ...central, eo.buffer], { type: 'application/zip' }), name);
  };

  window.floresta = {
    media,
    async descargar() {
      const posts = Object.values(media).sort((a, b) => b.taken - a.taken);
      const d = t => new Date(t * 1000).toISOString().slice(0, 10).replace(/-/g, '');
      const imgs = [], vids = [], meta = [];
      posts.forEach(p => {
        const m = { code: p.code, url: `https://www.instagram.com/p/${p.code}/`, fecha: new Date(p.taken * 1000).toISOString(), likes: p.likes, caption: p.cap, archivos: [] };
        p.items.forEach((it, k) => {
          const base = `${d(p.taken)}_${p.code}_${k + 1}`;
          if (it.vid) { vids.push({ url: it.vid, name: base + '.mp4' }); m.archivos.push(base + '.mp4'); }
          if (it.img) { const n = (it.vid ? 'portadas/' : '') + base + '.jpg'; imgs.push({ url: it.img, name: n }); m.archivos.push(n); }
        });
        meta.push(m);
      });
      save(new Blob([JSON.stringify({ perfil: 'florestaenchiloe', publicaciones: meta }, null, 1)], { type: 'application/json' }), 'floresta_textos.json');
      await zip(imgs, 'floresta_fotos.zip');
      const mid = Math.ceil(vids.length / 2);
      await zip(vids.slice(0, mid), 'floresta_videos_1.zip');
      await zip(vids.slice(mid), 'floresta_videos_2.zip');
      console.log('Descargas listas.');
    },
  };
  console.log('Floresta: escuchando… baja por el perfil.');
})();
