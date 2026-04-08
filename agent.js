/**
 * ╔══════════════════════════════════════════════════════════╗
 * ║   AGENTE DESCARGADOR DE INSTAGRAM — La Floresta         ║
 * ║   Descarga automáticamente todas las imágenes del perfil ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * USO: node agent.js
 *
 * El agente:
 *  1. Abre Chrome con interfaz visible
 *  2. Navega al perfil de Instagram
 *  3. Hace scroll automático para cargar todas las fotos
 *  4. Descarga todas las imágenes a /images/
 *  5. Actualiza el index.html con las fotos reales
 */

const { chromium } = require('playwright');
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ─── CONFIGURACIÓN ───────────────────────────────────────────
const INSTAGRAM_URL  = 'https://www.instagram.com/florestaenchiloe/';
const OUTPUT_DIR     = path.join(__dirname, 'imagenes');
const MAX_POSTS      = 30;      // cuántas fotos descargar (máx)
const SCROLL_PAUSES  = 8;       // cuántas veces hacer scroll
const HEADLESS       = false;   // false = ves el browser; true = segundo plano
// ─────────────────────────────────────────────────────────────

const log = (msg, icon = '→') => console.log(`\x1b[36m${icon}\x1b[0m  ${msg}`);
const ok  = (msg)              => console.log(`\x1b[32m✓\x1b[0m  ${msg}`);
const err = (msg)              => console.log(`\x1b[31m✗\x1b[0m  ${msg}`);
const sep = ()                 => console.log('\x1b[90m' + '─'.repeat(55) + '\x1b[0m');

// ─── CREAR CARPETA IMAGES ────────────────────────────────────
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  ok(`Carpeta /imagenes/ creada`);
}

// ─── DESCARGAR ARCHIVO ───────────────────────────────────────
function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    if (fs.existsSync(dest)) { resolve(dest); return; }
    const proto = url.startsWith('https') ? https : http;
    const file = fs.createWriteStream(dest);
    proto.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, res => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        file.close();
        fs.unlinkSync(dest);
        downloadFile(res.headers.location, dest).then(resolve).catch(reject);
        return;
      }
      res.pipe(file);
      file.on('finish', () => { file.close(); resolve(dest); });
    }).on('error', e => { fs.unlink(dest, () => {}); reject(e); });
  });
}

// ─── SLEEP ───────────────────────────────────────────────────
const sleep = ms => new Promise(r => setTimeout(r, ms));

// ─── AGENTE PRINCIPAL ────────────────────────────────────────
async function run() {
  sep();
  console.log('\x1b[33m🔥 AGENTE INSTAGRAM — La Floresta\x1b[0m');
  sep();

  const browser = await chromium.launch({
    headless: HEADLESS,
    args: ['--lang=es-ES']
  });

  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    locale: 'es-ES',
    viewport: { width: 1280, height: 900 }
  });

  const page = await context.newPage();

  // ── 1. Navegar al perfil ─────────────────────────────────
  log(`Abriendo perfil: ${INSTAGRAM_URL}`);
  await page.goto(INSTAGRAM_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await sleep(3000);

  // ── 2. Cerrar popup de login si aparece ─────────────────
  try {
    const closeBtn = page.locator('[aria-label="Cerrar"]').first();
    if (await closeBtn.isVisible({ timeout: 4000 })) {
      await closeBtn.click();
      log('Popup de login cerrado');
      await sleep(1000);
    }
  } catch (_) {}

  // También intentar botón "No ahora"
  try {
    const notNow = page.getByText('Ahora no').first();
    if (await notNow.isVisible({ timeout: 3000 })) {
      await notNow.click();
      await sleep(1000);
    }
  } catch (_) {}

  // ── 3. Scroll para cargar más posts ─────────────────────
  log(`Haciendo scroll para cargar fotos (${SCROLL_PAUSES} pasadas)...`);
  for (let i = 0; i < SCROLL_PAUSES; i++) {
    await page.evaluate(() => window.scrollBy(0, 800));
    await sleep(1200);
    process.stdout.write(`\r   Scroll ${i + 1}/${SCROLL_PAUSES}...`);
  }
  console.log('');
  await sleep(2000);

  // ── 4. Extraer URLs de imágenes del grid ────────────────
  log('Extrayendo URLs de imágenes...');

  const imageUrls = await page.evaluate((max) => {
    const results = [];
    const seen = new Set();

    // Selector principal: imágenes en el grid de posts
    const selectors = [
      'article img',
      'div[style*="flex-direction"] img',
      'img[srcset]',
      'img[src*="cdninstagram"]',
      'img[src*="fbcdn"]',
    ];

    for (const sel of selectors) {
      document.querySelectorAll(sel).forEach(img => {
        const src = img.srcset
          ? img.srcset.split(',').map(s => s.trim().split(' ')[0]).sort((a, b) => {
              const wa = parseInt((img.srcset.match(new RegExp(a.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ' (\\d+)w')) || ['', '0'])[1]);
              const wb = parseInt((img.srcset.match(new RegExp(b.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ' (\\d+)w')) || ['', '0'])[1]);
              return wb - wa;
            })[0]
          : img.src;

        if (src && !seen.has(src) && (src.includes('cdninstagram') || src.includes('fbcdn')) && !src.includes('profile') && !src.includes('s150x150') && !src.includes('s320x320')) {
          seen.add(src);
          results.push(src);
        }
        if (results.length >= max) return;
      });
      if (results.length >= max) break;
    }
    return results.slice(0, max);
  }, MAX_POSTS);

  if (imageUrls.length === 0) {
    err('No se encontraron imágenes. Instagram puede requerir login.');
    err('Intenta: 1) Abre el browser que se abre, 2) Inicia sesión manualmente, 3) Vuelve a ejecutar node agent.js');
    await browser.close();
    return [];
  }

  ok(`${imageUrls.length} imágenes encontradas`);
  sep();

  // ── 5. Descargar imágenes ────────────────────────────────
  const downloaded = [];
  for (let i = 0; i < imageUrls.length; i++) {
    const url  = imageUrls[i];
    const hash = crypto.createHash('md5').update(url).digest('hex');
    const name = `${hash}.jpg`;
    const dest = path.join(OUTPUT_DIR, name);

    try {
      await downloadFile(url, dest);
      ok(`[${i + 1}/${imageUrls.length}] ${name}`);
      downloaded.push(name);
    } catch (e) {
      err(`[${i + 1}/${imageUrls.length}] Error: ${e.message}`);
    }
  }

  sep();
  ok(`${downloaded.length} imágenes descargadas en /imagenes/`);

  // ── 6. Actualizar index.html con las imágenes reales ────
  if (downloaded.length > 0) {
    log('Actualizando index.html con fotos reales...');
    updateHTML();
    ok('index.html actualizado ✓');
  }

  await browser.close();
  sep();
  console.log('\x1b[32m🎉 ¡LISTO! Abre index.html en el navegador para ver el resultado.\x1b[0m');
  sep();

  return downloaded;
}

// ─── ACTUALIZAR HTML ─────────────────────────────────────────
function updateHTML() {
  const files = fs.readdirSync(OUTPUT_DIR).filter(f => f.endsWith('.jpg')).sort();
  const htmlPath = path.join(__dirname, 'index.html');
  if (!fs.existsSync(htmlPath)) {
    const basicHtml = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>La Floresta en Chiloé</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f0f0f0; }
    h1 { text-align: center; color: #333; }
    .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; padding: 20px; }
    .gallery img { width: 100%; height: 200px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.3s; }
    .gallery img:hover { transform: scale(1.05); }
  </style>
</head>
<body>
  <h1>La Floresta en Chiloé</h1>
  <div class="gallery">
    <!-- IMAGES -->
  </div>
</body>
</html>`;
    fs.writeFileSync(htmlPath, basicHtml, 'utf8');
  }

  let html = fs.readFileSync(htmlPath, 'utf8');
  const imagesHtml = files.map(file => `<img src="imagenes/${file}" alt="Imagen de La Floresta">`).join('\n    ');
  html = html.replace('<!-- IMAGES -->', imagesHtml);
  fs.writeFileSync(htmlPath, html, 'utf8');
}

// ─── EJECUTAR ────────────────────────────────────────────────
async function start() {
  await run();
  setInterval(async () => {
    try {
      await run();
    } catch (e) {
      err(`Error en ejecución automática: ${e.message}`);
    }
  }, 3600000); // Ejecutar cada hora
}

start().catch(e => {
  err(`Error fatal: ${e.message}`);
  process.exit(1);
});
