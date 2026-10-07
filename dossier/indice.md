# Floresta · Dossier de diseño · Propuesta 2 «Dos mitades, dos colores»

Dossier impreso de 18 láminas horizontales de 13 × 8,5 in. Lo arma `/tmp/claude-0/dossier-v3/2/build_final.py`, que genera:
- `floresta-dossier-diseno.html`: un solo archivo autocontenido, con las imágenes y las fuentes en base64, `@page` 13in × 8.5in y margen 0.
- `floresta-dossier-diseno.pdf`: 18 páginas de 936 × 612 pt, generadas con Playwright y `print_background`.
- `pages/p-01.png` … `p-18.png`: 1950 × 1275 px, a 150 ppp.

Narrativa: lo que vimos en tu Instagram (01–06) → el sitio parte por parte (07–17) → cierre (18).

## El sistema
- Cada lámina se parte en dos campos de color plano, exactamente al centro y sin línea divisoria. **Izquierda = el sitio** (capturas reales de florestachiloe.vercel.app). **Derecha = las decisiones** (por qué se ve así y de qué publicación viene).
- Elementos fijos en todas las láminas: rótulo en mayúsculas espaciadas arriba de cada mitad ("EL SITIO" a la izquierda y el capítulo a la derecha), pie bajo cada captura y número de lámina en Fraunces abajo a la derecha.
- Campos posibles: berenjena #2f2238, frambuesa #b8457a, rosa empolvado #f6e3ea, lila #efe8f6, blanco rosado #fffbfa. El eucalipto #67a284 y el eucalipto claro #e2efe8 nunca son campo: solo aparecen dentro de las fotos y en las muestras, para que el verde no pase del ~25 % de una lámina.
- Tipografías: Fraunces para títulos y frases (SOFT 100; la cursiva con WONK 1, en frambuesa sobre fondo claro y en rosa empolvado sobre fondo oscuro) y Figtree para textos.
- A las capturas de computador y de celular se les quita la barra superior del sitio, y cada una termina entre dos bloques, sin cortar texto. Son rectángulos planos, con aire alrededor. Las capturas cuyo fondo es igual al campo llevan un filete de 1 px.
- Las frases de Instagram son literales: el script comprueba cada una contra `floresta_textos.json` y se detiene si alguna no coincide. Las fechas salen del mismo archivo.

## Formas del lado izquierdo (sitio)
C centrada · P celular solo · R fila de celulares · D dos desfasadas (computador arriba, celular abajo) · A apoyada abajo · E pegada al borde exterior.

## Formas del lado derecho (decisiones)
T título grande y una línea · K carta · X cifras · F frase literal en grande · M muestras de color · S muestras tipográficas · O publicación de origen con fecha · N decisiones numeradas · I firma.

## Láminas

| # | Título | Izq. \| der. | Contraste | Izq. | Der. | Contenido |
|---|---|---|---|---|---|---|
| 01 | De tu Instagram a tu sitio | berenjena \| rosa empolvado | fuerte | C | T | Izq.: la portada en el computador. Der.: logotipo, título y una línea con florestachiloe.vercel.app; Esmeralda 198 · Castro, Chiloé · octubre 2026. |
| 02 | Natalia: | frambuesa \| lila | fuerte | P | K | Izq.: tu florería en el celular (inicio del manifiesto). Der.: carta breve, firmada "Pablo". |
| 03 | 658 publicaciones | lila \| berenjena | fuerte | R | X | Izq.: Ramos, Del jardín y Visítanos en el celular. Der.: 658 publicaciones desde mayo de 2019 · 879 fotos · 110 videos (cifras verificadas) y "De ahí sale casi todo tu sitio: tus frases, tus fotos y tus precios." |
| 04 | Lo que vimos en tu Instagram | blanco rosado \| frambuesa | fuerte | D | F | Izq.: la cinta de ramos (computador) y tus videos (celular). Der.: "Silvestre. Elegante. Es Floresta." (Tu firma · Instagram · 15 jul 2025) y tres lecturas numeradas, una de ellas "hacemos ramos con alma" (25 jun 2025). |
| 05 | Paleta | rosa empolvado \| blanco rosado | suave | A | M | Izq.: Esmeralda 198, apoyada abajo y a todo el ancho del campo. Der.: "Tus colores ya estaban en tu florería", los siete colores con nombre y código, la fachada verde y coral, una línea sobre los tonos claros y la berenjena que acompañan para que las flores sean protagonistas, y "¡AMAMOS EL ROSADO!" (Instagram · 14 ago 2026). |
| 06 | Tus letras | berenjena \| lila | fuerte | C | S | Izq.: reseñas y "Debes saber…" en el sitio. Der.: muestras de Fraunces (la cursiva frambuesa marca la palabra que importa en cada título) y de Figtree, con su uso. |
| 07 | El ramo en la mano, frente a la florería | rosa empolvado \| frambuesa | fuerte | P | O | Izq.: la portada en el celular. Der.: foto de DdAPKv2hBR3 y "Hay clásicos que nunca pasan de moda…" (Instagram · 7 sep 2026). |
| 08 | Ramos con alma | blanco rosado \| rosa empolvado | suave | A | F | Izq.: el manifiesto en el computador. Der.: "En Floresta no hacemos “arreglos”, hacemos ramos con alma." (25 jun 2025) y "Mientras más silvestre… ¡mejor!" (28 jul 2025). |
| 09 | Ramos | lila \| berenjena | fuerte | E | O | Izq.: la sección Ramos, pegada al borde. Der.: la pieza Ramos Silvestres del catálogo Día de la Madre 2026 (DX69F30lsj8 · 4 may 2026); Ramo Pequeño $15.000 = Ramos Silvestres $15.000; "regala flores. Flores de verdad." (15 sep 2026). |
| 10 | Nunca son idénticas | frambuesa \| blanco rosado | fuerte | P | F | Izq.: Esmeralda 198 en el celular. Der.: "…las flores son como la naturaleza: nunca son idénticas." (Instagram · 6 jun 2026); los once ramos frente al mismo letrero. |
| 11 | Comienza con una idea | rosa empolvado \| lila | suave | E | N | Izq.: Historia (cuatro videos), pegada al borde derecho. Der.: tres decisiones; frase del 25 jun 2026 y "Un ratito en la florería hoy…" (9 jul 2026). |
| 12 | Mi destino siempre fueron las plantas y las flores | berenjena \| blanco rosado | fuerte | C | O | Izq.: Natalia en el sitio. Der.: foto de DJiZA6bgtDm y la frase (Instagram · 12 may 2025). |
| 13 | Ocasiones | lila \| rosa empolvado | suave | A | N | Izq.: Ocasiones en el celular, apoyada abajo (la captura de computador corta los rótulos de los paneles). Der.: las cinco ocasiones, literales de la lista del 26 ago 2026, y la corona (15 jul 2026). |
| 14 | Del jardín a la florería | blanco rosado \| frambuesa | fuerte | E | T | Izq.: Del jardín, pegada al borde izquierdo. Der.: título y una línea; "¡Ahora somos uno con Floresta!" (Instagram · 23 may 2025). |
| 15 | Visítanos | rosa empolvado \| berenjena | fuerte | D | N | Izq.: Visítanos con el mapa (computador) y en el celular. Der.: "¿Buscas flores en Castro? Las encontraste." (Instagram · 26 ago 2026); dirección y horario, "Debes saber…" (4 may 2026: reservas, despacho y horario de despacho) y 5,0 en Google. |
| 16 | Todos los días son primavera | frambuesa \| lila | fuerte | C | F | Izq.: la frase de invierno en el computador. Der.: "Aunque estemos en pleno invierno en Chiloé, para nosotros todos los días son primavera." (Instagram · 13 jul 2026); la frase ocupa la pantalla sobre un ramo de girasoles. |
| 17 | Del ramo a la puerta de la florería | blanco rosado \| rosa empolvado | suave | R | T | Izq.: seis celulares (Portada, Ramos, Esmeralda 198, Ocasiones, Del jardín, Visítanos). Der.: título, "Así se recorre tu sitio en el celular, de la portada a Visítanos." y florestachiloe.vercel.app. |
| 18 | Cierre | lila \| berenjena | fuerte | A | I | Izq.: el pie del sitio. Der.: Cuando quieras, lo conversamos. / PABLO FIGUEROA G. / Director de estudio / pablo@bergerac.cl · +56 9 7589 2096 / BERGERAC.CL |

## Secuencias
El script lo comprueba: nada se repite entre láminas seguidas, y ninguna lámina usa el mismo color en sus dos mitades.
- **Campo izquierdo**: berenjena → frambuesa → lila → blanco rosado → rosa empolvado → berenjena → rosa empolvado → blanco rosado → lila → frambuesa → rosa empolvado → berenjena → lila → blanco rosado → rosa empolvado → frambuesa → blanco rosado → lila.
- **Campo derecho**: rosa empolvado → lila → berenjena → frambuesa → blanco rosado → lila → frambuesa → rosa empolvado → berenjena → blanco rosado → lila → blanco rosado → rosa empolvado → frambuesa → berenjena → lila → rosa empolvado → berenjena.
- **Forma izquierda**: C P R D A C P A E P E C A E D C R A.
- **Forma derecha**: T K X F M S O F O F N O N T N F T I.
- **Contraste**: fuerte, fuerte, fuerte, fuerte, suave, fuerte, fuerte, suave, fuerte, fuerte, suave, fuerte, suave, fuerte, fuerte, fuerte, suave, fuerte.

## Cifras verificadas (lámina 03)
- 658 publicaciones: entradas de `floresta_textos.json`; la primera es de mayo de 2019 y la última del 15 sep 2026.
- 879 fotos: archivos .jpg en `assets/raw/fotos/` (sin contar las portadas de video). Coincide con las fotos que cita el JSON.
- 110 videos: archivos .mp4 en `assets/raw/videos/`, uno por cada una de las 110 publicaciones con video.
- 5,0 en Google con 6 reseñas (lámina 15) sale del sitio publicado, no del JSON.
