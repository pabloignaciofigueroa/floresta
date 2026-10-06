# Floresta · by Almácigos Chiloé

Sitio de **Floresta**, florería en Esmeralda 198, Castro, Chiloé. Está hecho solo con el material que la marca ya publicó en @florestaenchiloe: sus fotos, sus videos, sus palabras, su logo vectorizado y el sistema de sus piezas gráficas. Se construyó con el método de 20 fases de la skill `web-regalo-cold-call`; la bitácora está en `_plan/`.

**En línea:** https://lafloresta.vercel.app

## Cómo está armado
| Carpeta | Qué hay |
|---|---|
| `src/index.html` | Plantilla. Las imágenes van como `<x-img id=…>` |
| `tools/build.py` | Genera `index.html` con srcset, LQIP, alt en inglés y el manifiesto de la precarga: `python3 tools/build.py` |
| `css/main.css`, `js/main.js` | Estilos y movimiento (GSAP + ScrollTrigger, Lenis; Swiper y Leaflet diferidos, en `vendor/`) |
| `content/` | `brand-voice.md` (voz y datos), `copy.md` (cada texto con su fuente), `inventario.md` |
| `brand/` | `typography.md`, `palette.md`, `art-direction.md`, `logo/` (SVG, favicons, firma) |
| `assets/` | `img/` WebP 800/1800, `video/` MP4 + WebM, `fonts/` woff2 (OFL), `icons/`, `og.jpg` |
| `tools/` | Vectorizado del logo, paleta, alineación del momento memorable, medios, QA y pruebas |
| `assets/raw/` | Material original (fuera de git; vive en el PC en `Desktop\brgrc\LA_FLORESTA`) |

## El momento memorable
En *Esmeralda 198*, once ramos fotografiados frente al letrero redondo de la tienda se alinearon (`tools/align_facade.py`) para que el letrero quede quieto y solo cambie el ramo al hacer scroll: "las flores son como la naturaleza: nunca son idénticas" (IG, 6 jun 2026).

## Pedido
El carrito arma el mensaje y lo abre en WhatsApp (+56 9 6483 8490). No cobra ni guarda datos en un servidor; el pedido se recuerda solo en el navegador de quien lo arma.

## Por confirmar con la florería
- Horario: el sitio dice lunes a sábado de 10:00 a 19:30 (último post con horario general, 22 jun 2026). Algunos posts dicen 10:30.
- Precios: son los del catálogo 2026 (Día de la Madre), publicados como referenciales.
- Horario de despacho AM 10–13 y PM 14–20 (de la pieza "Debes saber…").
- Los "30 años" de la bio de Instagram no se publicaron.

## Pruebas
```
python3 -m http.server 8765 &
python3 tools/qa.py 1536 864        # capturas por sección + CLS
python3 tools/test_interactions.py  # idioma, menú, pedido, movimiento reducido
python3 tools/test_auditoria.py     # verificaciones de la auditoría
```

La versión anterior (v2) queda en el historial: commit `9e96ee1`.
