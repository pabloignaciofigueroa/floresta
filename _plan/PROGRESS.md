# Progreso

estado: en curso
fase_actual: 19
inicio_ejecucion: 2026-10-06 11:00
ultima_fase_completada: 18

## Bitácora
- 2026-10-06 11:10 — Carpeta del PC ordenada según la skill (01_imagenes, 02_videos, 03_textos, 04_marca, 05_web, 06_herramientas, 99_archivo). Rama `dev` creada desde main@9e96ee1 (v2 tal cual). Plan creado.
- 11:30 — F01 inventario: 880 fotos, 110 videos, 150 mejores tomas, 11 piezas gráficas, 3 logos y 658 publicaciones en assets/raw (fuera de git). content/inventario.md.
- 11:50 — F02 voz: content/brand-voice.md con manifiesto, rasgos, 33 titulares literales con fuente, textos permanentes del catálogo, "Debes saber…", datos verificables y reseñas de Google (5,0 ★, 6). Por confirmar con la clienta: horario 10:00 o 10:30, y el "30 años" de la bio.
- 12:20 — F03 tipografía: Allura (títulos manuscritos), Catamaran (texto y rótulos), Playfair Display (apoyo); comparadas contra las piezas, láminas en brand/_comparaciones. F04 paleta k-means: bosque #406345, salvia #a3bba9, crema, coral del isotipo; contraste calculado.
- 12:45 — F05 logotipo e isotipo vectorizados desde los PNG (potrace, por capas), firma "by Almácigos Chiloé", vertical, favicons 16–512, OG 1200×630.
- 13:30 — F06 guion content/copy.md (cada texto con fuente). F07: 37 imágenes WebP 800/1800 + LQIP, 4 videos MP4/WebM con presupuesto de peso. Momento memorable armado: once ramos alineados frente al mismo letrero (tools/align_facade.py, plantilla multiescala). Ramos de referencia recortados de las piezas del catálogo. F08 brand/art-direction.md.
- 14:30 — F09–F16 sitio: src/index.html + tools/build.py → index.html; css/main.css; js/main.js; vendor (GSAP 3.15, Lenis 1.3, Swiper 14 diferido, Leaflet 1.9 diferido). Portada con el letrero como ventana al video, manifiesto con masas, Esmeralda 198 (sticky sin pin), oficio, del jardín, ramos (pedido → WhatsApp), debes saber, ocasiones, Natalia, invierno, reseñas de Google, visítanos (mapa), pie. Menú dialog con foco atrapado e inert; pedido como dialog.
- 15:10 — F17 responsive 390/1280/1366/1440/1536/1920 sin desborde. F18 QA: CLS 0,0005–0,0011; pruebas automáticas 19/19 (idioma, menú, pedido, Escape, recordar pedido, movimiento reducido); Lighthouse local sin compresión: Perf 65 · A11y 100 · BP 100 · SEO 100. Corregido: contraste de rótulos sobre salvia, barra oculta tras agregar al pedido, recálculo de estilos de la precarga (4,1 s → 1,3 s), grabados rasterizados, video de portada parte al levantar la precarga.
