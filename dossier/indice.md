# Floresta · Decisiones de diseño del sitio web · dossier v4

Son 19 láminas horizontales de 13 × 8,5 in. Combinan el sistema «dos mitades, dos colores» con los textos del dossier de 19 láminas.

Script: `/tmp/claude-0/dossier-v4/build_v4.py`. Genera:
- `floresta-dossier-diseno.html`: un solo archivo autocontenido, con imágenes y letras en base64; `@page` de 13in × 8.5in, margen 0.
- `floresta-dossier-diseno.pdf`: 19 páginas de 936 × 612 pt, con fondos.
- `pages/p-01.png` … `p-19.png`: 1950 × 1275 px.

## El sistema
- **Proporción estable de 45/55.** Izquierda, 5,85 in: el sitio, en computador y en celular. Derecha, 7,15 in: las decisiones.
- **Dos campos de color plano.** Cada mitad tiene el suyo y la pareja cambia en cada lámina. El script comprueba que ningún color ni ninguna forma se repita entre láminas seguidas, y que ninguna lámina use el mismo color en sus dos mitades.
- **Berenjena como acento.** Aparece en solo cuatro mitades (01, 05 y 15 a la izquierda; 19 a la derecha). Ninguno de los dos verdes es nunca un campo completo.
- **Lado derecho.** Rótulo de capítulo, título en Fraunces y una bajada de una o dos líneas. Debajo, bloques rotulados: TEXTOS, IMÁGENES, COMPOSICIÓN, MOVIMIENTO, INTERACCIÓN, POR QUÉ ASÍ, etc. La disposición de esos bloques cambia de una lámina a la siguiente.
- **Láminas de sección (09 a 17).** Llevan abajo a la izquierda el índice «Lugar en el recorrido», con las 9 partes del sitio y la actual marcada.
- **Tamaños.** Los textos de los bloques van a 9,5 pt, las citas a 10,5 pt, y los rótulos y pies a 7,5–8 pt. El chequeo automático no encuentra nada bajo 7 pt.
- **Frases literales.** Las 26 frases citadas se comprueban al construir contra `floresta_textos.json`, `almacigos_textos.json` y, en el caso de las reseñas de Google, contra el sitio publicado. Si una no coincide, el script se detiene.
- **Palabras vetadas.** El script también falla si aparece cualquiera de estas: github, precarga, carrusel, cursor, navegador, scroll, layout, «se corrigió», «nueva versión», Esmeralda 998, etc.
- **Capturas.** Todas van sin la barra superior del sitio y cortadas entre dos bloques. El mazo de Esmeralda 198 (sin el distintivo «Arrastrar») y el pedido (fecha 14/10/2026, formato es-CL) se recapturaron con `capture_v4.py` en `/tmp/claude-0/dossier-v4/shots/`.
- **Fechas.** Todas las fechas se calculan en hora de Chile (America/Santiago), no en UTC.

### Formas de la izquierda
C centrada · P celular solo · E pegada al borde · A apoyada abajo · R fila de celulares · G grilla de 3 × 3 · D computador y celular desfasados · H dos capturas de computador escalonadas.

### Disposiciones de la derecha
Portada · K carta · M mosaico de fuentes y bloques · Q cita grande y bloques debajo · E muestras de letra · S muestras de color · G bloques en dos columnas · N pasos o lista numerada · I bloques al costado de las fuentes de Instagram con fecha · P lista de precios · T lista y firma.

## Láminas

| # | Lámina | Izq. \| der. | Izq. | Der. | Contenido principal |
|---|---|---|---|---|---|
| 01 | Portada | berenjena \| rosa empolvado | C | Portada | Portada del sitio · logotipo, «Decisiones de diseño del sitio web», «De tu Instagram a tu sitio», «Preparado para Natalia», Esmeralda 198 · Castro, Chiloé · octubre 2026, florestachiloe.vercel.app |
| 02 | Antes de empezar | frambuesa \| blanco rosado | P | K | La carta del v1, firmada «Pablo Figueroa / Director de estudio» |
| 03 | De dónde viene todo | blanco rosado \| lila | E | M | Mosaico de 10 fotos y 4 piezas · 658 publicaciones, 879 fotos y 110 videos (verificados), piezas gráficas, @almacigoschiloe, Google y «La regla» |
| 04 | La voz | lila \| rosa empolvado | A | Q | «Mientras más silvestre… ¡mejor!» en grande · firma, oficio, vocabulario, cierres afectuosos y ocasiones |
| 05 | Las letras | berenjena \| blanco rosado | C | E | Muestras de Fraunces y Figtree y la letra manuscrita del catálogo · la cursiva va en frambuesa en los títulos y en rosa claro en el lema |
| 06 | Los colores | rosa empolvado \| lila | R | S | 3 celulares con filete · los 7 colores con código y 4 fotos de origen con fecha · claros, fuertes, el verde con medida, que se lea |
| 07 | El logo | blanco rosado \| frambuesa | A | G | Variantes en planos de color · trazos, variantes, en miniatura, dónde aparece |
| 08 | El recorrido | lila \| blanco rosado | G | N | Las 9 partes en grilla · 1 Llegar, 2 Elegir, 3 Conocer, 4 Venir, Ritmo |
| 09 | La espera antes de entrar | rosa empolvado \| lila | C | G | Qué se ve, qué se deja listo, tiempos, por qué así |
| 10 | Portada del sitio | frambuesa \| rosa empolvado | D | I | 3 fotos de origen con fecha (dos frente a la fachada, una dentro de la florería) · textos (la cursiva del lema en rosa claro), imágenes, movimiento, por qué así |
| 11 | Manifiesto | blanco rosado \| lila | E | Q | «En Floresta no hacemos “arreglos”, hacemos ramos con alma.» · textos, 4 imágenes, composición, movimiento |
| 12 | Ramos | lila \| rosa empolvado | D | P | Lista de precios del catálogo (4 ramos y «desde $5.000») · textos, interacción, por qué así |
| 13 | Esmeralda 198 | frambuesa \| blanco rosado | H | Q | «…las flores son como la naturaleza: nunca son idénticas.» · la frase de invierno sobre los girasoles, 4 ramos frente al letrero, interacción, por qué aquí |
| 14 | Comienza con una idea | rosa empolvado \| lila | D | I | 4 portadas de video con fecha · textos, composición, por qué aquí |
| 15 | Ocasiones | berenjena \| rosa empolvado | P | N | Las 5 ocasiones literales (25 ago 2026) · la corona, 4 imágenes, interacción, por qué así |
| 16 | Del jardín | lila \| blanco rosado | H | I | 3 fotos del vivero con fecha · textos, imágenes, interacción, por qué aquí |
| 17 | Visítanos | frambuesa \| lila | D | Q | Reseña de Tamara D. en grande · datos, lo que dicen, «Debes saber…», por qué al final |
| 18 | Detalles | rosa empolvado \| blanco rosado | A | G | Pedido, menú, movimiento con calma, celular primero, sin saltos, para todos |
| 19 | Lo que sigue y cierre | lila \| berenjena | P | T | Las 4 propuestas del v1 · Cuando quieras, lo conversamos. / Pablo Figueroa / Director de estudio / pablo@bergerac.cl · +56 9 7589 2096 / Bergerac.cl |

## Secuencias
- **Izquierda**: berenjena, frambuesa, blanco rosado, lila, berenjena, rosa empolvado, blanco rosado, lila, rosa empolvado, frambuesa, blanco rosado, lila, frambuesa, rosa empolvado, berenjena, lila, frambuesa, rosa empolvado, lila.
- **Derecha**: rosa empolvado, blanco rosado, lila, rosa empolvado, blanco rosado, lila, frambuesa, blanco rosado, lila, rosa empolvado, lila, rosa empolvado, blanco rosado, lila, rosa empolvado, blanco rosado, lila, blanco rosado, berenjena.
- **Forma izquierda**: C P E A C R A G C D E D H D P H D A P.
- **Disposición derecha**: Portada K M Q E S G N G I Q P Q I N I Q G T.

## Cambios de texto respecto del v1
- **Dirección y nombres.** La dirección es siempre florestachiloe.vercel.app. «Precarga» pasa a ser «La espera antes de entrar».
- **Sin jerga.** Sin carrusel, cursor ni navegador: «fila de fichas que se arrastra con la mano», «al pasar por encima», «el pequeño ícono que acompaña el nombre del sitio».
- **Sin proceso.** «Se revisó» se reescribió como descripción, por ejemplo «se lee con holgura» o «se ve igual de bien».
- **Cursiva del lema.** La cursiva del lema de la portada va en rosa claro, y la frambuesa marca la palabra que importa en los títulos.
- **Frase de invierno.** Se describe sobre un ramo de girasoles, con una segunda línea más pequeña.
- **Trato de tú.** A Natalia se le habla de tú: «tu historia», «tus clientes», «Tú y un ramo gigante».
- **Frase de Almácigos.** La de Almácigos Chiloé se cita sin el punto final, porque así está escrita en la publicación.
