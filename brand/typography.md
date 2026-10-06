# Tipografía — Floresta (Fase 03)

Floresta no tiene web propia, así que no hay estilos computados que leer. El sistema se reconstruyó desde sus piezas gráficas (`assets/raw/piezas/`): se recortaron los textos y se compararon renderizados contra candidatas libres de @fontsource. Las láminas están en `brand/_comparaciones/`.

## Lo que usa la marca
| Rol en las piezas | Ejemplo | Fuente original | Equivalente libre elegido |
|---|---|---|---|
| **Logotipo** | FLORESTA (verde, mayúsculas de alto contraste, O inclinada, R con pierna que se enrosca, S de remates en gota, A con una hoja que cruza el travesaño) | Display comercial, probablemente *The Seasons* (no está disponible; Pablo no tiene el archivo) | **No se reemplaza.** El logotipo se vectoriza desde `logotipo.png` (Fase 05), así que el sitio usa los trazos reales |
| **Títulos manuscritos** | "Debes saber…", "Ramos Silvestres", "Rosas Rojas", "También puedes venir directamente" | Script fina y monolineal, con la *r* final que baja en lazo | **Allura** 400 — coincide en la D, la b, la R con bucle y la inclinación. Es la más cercana de 23 candidatas |
| **Texto corrido** | Normas de "Debes saber…", notas bajo cada ramo | Sans humanista angosta, de x alta | **Catamaran** 300/400 — mismo ancho y ritmo; Fira y Open Sans quedan demasiado anchas, Alegreya Sans demasiado caligráfica |
| **Rótulos y bajadas** | "RAMOS SILVESTRES", "Un clásico lleno de significado", "10 Rosas · $39.000" | La misma sans en seminegrita y en mayúsculas espaciadas | **Catamaran** 600/700 |
| **Serif de apoyo** | "CELEBRA CON FLORES DE FLORESTA", "BY ALMÁCIGOS CHILOÉ" (pieza Día de la Novia) | La misma display del logotipo | **Playfair Display** 400/500 e itálica — la de mayor contraste con la pierna de la R curva, la más cercana al logotipo entre 25 serif probadas. Se usa poco: cifras grandes, firma, cita |

## Reglas de uso (tomadas de las piezas)
- El título de cada bloque va **en script**, en el color claro del fondo (salvia sobre verde, verde sobre salvia), centrado o alineado a la izquierda, nunca en mayúsculas.
- Bajo el título, una **bajada en Catamaran seminegrita**, corta.
- Los rótulos de sección van en **mayúsculas espaciadas** (`letter-spacing: .08em`), Catamaran 700, en el tono claro y apagado del fondo.
- Los precios se componen como en el catálogo: `5 Rosas · $21.000`, con punto medio y punto de miles.
- Debajo de cada foto de producto: "* Ramo de referencia", en cuerpo pequeño.
- La script no baja de 32 px (en pantalla pierde los trazos finos) y nunca se usa para texto corrido.

## Escala (fluida, `clamp`)
| Token | Uso | Tamaño |
|---|---|---|
| `--t-script-xl` | Portada, momento memorable | clamp(4rem, 11vw, 11rem) Allura |
| `--t-script-l` | Títulos de sección | clamp(3rem, 6.4vw, 6.5rem) Allura |
| `--t-script-m` | Títulos de producto | clamp(2.4rem, 3.6vw, 3.6rem) Allura |
| `--t-serif-l` | Cifras, citas | clamp(1.8rem, 3.2vw, 3rem) Playfair Display |
| `--t-lead` | Bajadas | clamp(1.15rem, 1.5vw, 1.45rem) Catamaran 600 |
| `--t-body` | Texto | clamp(1.02rem, 1.1vw, 1.15rem) Catamaran 400, interlínea 1.55 |
| `--t-label` | Rótulos | .78rem Catamaran 700, mayúsculas, +.08em |
| `--t-small` | Notas | .82rem Catamaran 400 |

## Archivos autoalojados (`assets/fonts/`, subconjunto latin, cubre á é í ó ú ñ ¿ ¡ … ·)
| Archivo | Peso | Precarga |
|---|---|---|
| `allura-latin-400-normal.woff2` | 26 KB | sí (portada) |
| `catamaran-latin-400-normal.woff2` | 9 KB | sí |
| `catamaran-latin-600-normal.woff2` | 9 KB | sí |
| `catamaran-latin-700-normal.woff2` | 9 KB | sí (rótulos sobre el pliegue) |
| `catamaran-latin-300-normal.woff2` | 9 KB | no |
| `playfair-display-latin-400-normal.woff2` | 22 KB | no |
| `playfair-display-latin-500-normal.woff2` | 23 KB | no |
| `playfair-display-latin-400-italic.woff2` | 22 KB | no |

Licencia: SIL Open Font License 1.1 (las tres familias). Se esperan con `Promise.allSettled` y un tope de 2,5 s: una fuente que falle no bloquea la página.
