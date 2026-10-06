# FLORESTA — Plan de construcción del sitio (20 fases, método RILÁN)

Encargo de Pablo Figueroa (6 oct 2026): rehacer lafloresta.vercel.app con la skill `web-regalo-cold-call`. La v2 "se quedó corta, le falta el alma de la marca". Debe sentirse como un estudio metódico de cómo se construye Floresta, no como una página genérica.

Marca: **Floresta** (firma completa: *Floresta by Almácigos Chiloé*). Florería en Esmeralda 198, Castro, Chiloé. Instagram @florestaenchiloe. Vivero hermano @almacigoschiloe en Pidpid. A cargo: Natalia Torres Manzo (@natiiitm).

## Reglas que no se negocian
1. **Ghostwriter estricto.** Todo texto visible sale de lo que Floresta ya publicó (posts de IG, bio, piezas gráficas) o de un dato verificable (ficha de Google Maps). Cada texto lleva su fuente en `content/copy.md`: [IG-NNN], [BIO], [PIEZA], [DATO], [RESEÑA] o [UI]. Solo correcciones mínimas, documentadas. Promociones vencidas no se publican (Día de la Madre, 21 de septiembre, Día de la Novia): de esas piezas se usan solo los textos permanentes.
2. **Contenido de origen en su idioma; solo se traduce la interfaz.** Español por defecto; inglés solo si el visitante lo elige (`data-l`, `data-alt-en`, `data-aria-en`, `tools/alt-en.json`).
3. **Diseño desde el sistema visual de Floresta**: logotipo serif de alto contraste, títulos manuscritos, sans humanista, campos verde bosque y salvia con grabado botánico en línea, el isotipo del ramo coral y el ramo sostenido por una mano tatuada.
4. **Solo material real** de @florestaenchiloe. Nada de stock ni imágenes generadas.
5. **Aire.** Secciones a sangre de exactamente `100svh` (mín. ~560 px). Parallax con `inset` negativo.
6. **Un solo momento memorable.** El resto es sobrio.
7. **Movimiento** expo-out `cubic-bezier(.16,1,.3,1)`, 200–700 ms. `prefers-reduced-motion` siempre.
8. **CLS < 0,01.** Nunca `pin` de ScrollTrigger con Lenis (sticky + alto `recorrido + 100vh`); `overflow: clip`; fuentes precargadas con `Promise.allSettled` + tope; reglas mínimas de Swiper en el CSS propio; grillas `minmax(0,1fr)`.
9. **Commits como Claude** (`noreply@anthropic.com`).

Assets fuente: `C:\Users\pfigug\Desktop\brgrc\LA_FLORESTA` (01_imagenes, 02_videos, 03_textos, 04_marca, 05_web, 06_herramientas, 99_archivo). En el repo viven en `assets/raw/` (fuera de git).
Rama de trabajo: `dev`. `main` se publica solo en la Fase 20. La v2 queda en `main@9e96ee1` y en `05_web`.
Archivos originales del repo que no se tocan: `imagenes/`, `imagotipo.png`, `isotipo.png`, `logotipo.png`, `agent.js`, `package.json`, `node_modules/`, `.agents/`, `.claude/`.

## Las 20 fases
| # | Fase | Entregable |
|---|------|-----------|
| 01 | Inventario | `assets/raw/`, `content/inventario.md` |
| 02 | Voz de marca | `content/brand-voice.md`: corpus literal con fuente, rasgos, titulares, datos, reseñas de Google |
| 03 | Tipografías | `brand/typography.md`, woff2 autoalojados en `assets/fonts/` |
| 04 | Paleta | `brand/palette.md` (k-means k=7 sobre fotos y piezas), tokens con contraste calculado |
| 05 | Logos | `brand/logo/`: logotipo, isotipo, firma *by Almácigos Chiloé*, claro/oscuro/mono, favicons 16–512, OG 1200×630 |
| 06 | Guion | `content/copy.md` sección por sección con fuente |
| 07 | Medios | Hojas de contacto, WebP 800/1800 + LQIP en `meta.json`, MP4 + WebM + póster |
| 08 | Dirección de arte | `brand/art-direction.md`: ritmo, momento memorable, sistema de movimiento |
| 09 | Base | `src/index.html` + `tools/build.py` → `index.html`; `css/main.css`; `js/main.js`; GSAP/ScrollTrigger/Lenis vendorizados; Swiper diferido |
| 10 | Portada | Video a sangre, logotipo, "Silvestre. Elegante. Es Floresta." |
| 11 | Momento memorable + manifiesto | El isotipo que se dibuja y se abre al taller; "ramos con alma" |
| 12 | Del jardín a la florería | Vivero Almácigos Chiloé en Pidpid → Esmeralda 198 |
| 13 | Ramos (catálogo) | Slider/cards al estilo de las piezas: campo salvia, título manuscrito, precios, carrito WhatsApp |
| 14 | Ocasiones + quien los hace | Celebrar, agradecer, acompañar, despedir; Natalia en primera persona |
| 15 | Reseñas, Debes saber, visítanos, pie | Google 5,0; normas de pedido; mapa; WhatsApp |
| 16 | Micro-interacciones | Menú `role=dialog`, foco atrapado, `inert`, `killTweensOf`, botones magnéticos, Arrastrar |
| 17 | Responsive + accesibilidad | 390/1280/1366/1440/1536/1920 |
| 18 | QA | Playwright 1536×864, CLS con PerformanceObserver, Lighthouse |
| 19 | Auditoría independiente | Dos agentes: voz/datos y código |
| 20 | Publicación + aviso | README, `.nojekyll`, `dev:main`, Vercel, correo |
