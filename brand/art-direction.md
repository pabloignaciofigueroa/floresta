# Dirección de arte y movimiento — Floresta (Fase 08)

## La idea
Floresta se reconoce en dos objetos que se repiten en todo su Instagram:
1. **El letrero redondo** de la fachada verde de Esmeralda 198 (instalado en noviembre de 2025, [IG-559]). Aparece detrás de casi todos los ramos desde entonces.
2. **El ramo sostenido en alto por una mano tatuada**, frente a ese letrero o sobre el campo salvia del catálogo.

Y en una gramática gráfica muy clara en sus piezas: **dos campos planos, verde bosque y salvia, que se alternan**; un título manuscrito arriba; una bajada en sans seminegrita; el isotipo del ramo coral sobre una mancha salvia; el ramo abajo, saliendo del borde.

El sitio se construye con esas tres cosas y nada más. No hay "estilo web" agregado: hay campos de color de la marca, su letra, su isotipo y sus fotos.

## Momento memorable (uno solo): "Nunca son idénticas"
En la sección *Esmeralda 198*, once fotos de ramos tomadas frente al letrero (nov 2025 → ago 2026) se alinearon con `tools/align_facade.py`: el letrero quedó exactamente en el mismo lugar y al mismo tamaño en las once. Al hacer scroll, la escena queda fija y **solo cambia el ramo**: el letrero no se mueve, las flores sí. Es la frase de [IG-613] hecha imagen: "las flores son como la naturaleza: nunca son idénticas".
- Técnica: sección de alto `11 × 55vh + 100vh` con un hijo `position: sticky; top: 0; height: 100svh`. Sin `pin`. Las fotos están apiladas; el progreso de ScrollTrigger (`start: 'top top', end: 'bottom bottom'`) decide cuál es visible (corte seco, como stop-motion, con un fundido de 120 ms para no parpadear).
- Contador `Ramo 03 / 11` en Catamaran con cifras tabulares.
- Movimiento reducido: las once fotos en una grilla, sin sticky.

## Ritmo de la página
```
00 PRECARGA     crema · isotipo que se dibuja (stroke) + % real
01 PORTADA      bosque · logotipo a todo el ancho · CÍRCULO (letrero) con video de flores · "Silvestre. Elegante. Es Floresta."
02 MANIFIESTO   crema · "hacemos ramos con alma" · 4 fotos que flotan a distinta velocidad (masas)
03 ESMERALDA 198 bosque · STICKY · el letrero quieto, once ramos ← momento memorable
04 OFICIO       mitad video (Natalia armando) / mitad bosque · "Comienza con una idea"
05 DEL JARDÍN   salvia · video Helleborus en óvalo + galería de plantas con arrastre
06 RAMOS        salvia · slider de 4 ramos como las piezas del catálogo + tarjeta "desde $5.000"
07 DEBES SABER  bosque · isotipo sobre mancha salvia · 5 notas en 2 columnas
08 OCASIONES    crema · lista grande; al pasar el cursor aparece la foto/video de cada ocasión
09 NATALIA      foto a sangre · citas en script y serif
10 INVIERNO     foto a sangre de girasoles · cita de [IG-630]
11 RESEÑAS      crema · 5,0 · dos citas
12 VISÍTANOS    bosque · mapa (Leaflet, diferido) + foto de fachada · horario · WhatsApp
13 PIE          bosque hondo · "Flores lindas, para momentos que importan." · firma
```
Alternancia de campos: bosque → crema → bosque → bosque/video → salvia → salvia → bosque → crema → foto → foto → crema → bosque. Nunca dos campos claros sin una imagen entre ellos.

Todas las secciones miden `100svh` (mín. 560 px), salvo la sticky (recorrido + 100vh) y la de ramos en móvil.

## Reglas de composición
- **Título manuscrito** (Allura) siempre en el color "claro" del campo: salvia sobre bosque, tinta sobre salvia/crema.
- **Rótulo** en Catamaran 700 mayúsculas espaciadas sobre el título, como "RAMOS SILVESTRES" en "Debes saber…".
- El **isotipo** sobre bosque va siempre sobre una mancha salvia (círculo irregular hecho con `border-radius` asimétrico).
- **Línea botánica**: el isotipo en versión línea (`isotipo-mono.svg`) a gran tamaño y 7% de opacidad, saliendo por el borde inferior de los campos verdes, como el grabado del fondo de las piezas.
- **Precios** con punto medio y punto de miles: `10 Rosas · $39.000`. "* Ramo de referencia" bajo cada foto.
- Fotos sin marco ni sombra. Esquinas rectas, salvo el círculo del letrero y el óvalo del vivero.
- Botón principal: píldora coral con texto hondo. Secundario: subrayado que crece.

## Sistema de movimiento
| Token | Valor | Uso |
|---|---|---|
| `--ease` | `cubic-bezier(.16,1,.3,1)` (expo-out) | Todo |
| `--d-fast` | 240 ms | Hover, botones |
| `--d-med` | 520 ms | Revelados de texto |
| `--d-slow` | 700 ms | Cortinas, imágenes |

- Revelado con máscara por línea (`.line > span` sube desde 105%). Padding inferior en `.line` para no cortar descendentes de Allura ni tildes de mayúsculas.
- Imágenes: `clip-path: inset(0 0 100% 0)` → `inset(0)`, con escala 1.08 → 1.
- Parallax: medio con `inset: -8% 0` y `yPercent` ±6.
- Masas (manifiesto): cuatro fotos con `data-speed` 0.7 / 1.15 / 0.85 / 1.3.
- Isotipo de la precarga: los trazos de la capa línea se dibujan con `stroke-dashoffset` (la capa se convierte en contorno con `stroke` + `fill: none`), luego entra el coral.
- Micro: botones magnéticos (máx. 6 px), cursor nativo siempre visible, etiqueta "Arrastrar" que sigue al cursor sobre la galería.
- `prefers-reduced-motion`: sin Lenis, sin parallax, todo visible desde el inicio; el momento memorable pasa a grilla.

## Guías externas aplicadas
- *frontend-design*: una dirección estética comprometida (aquí, la de la marca), tipografía con carácter, nada de plantilla.
- *impeccable* / *taste*: jerarquía de un solo foco por pantalla, ritmo de campos, cero tarjetas con sombra, cero gradientes decorativos, nada de íconos genéricos; los textos no se centran todos.
- La marca manda sobre las reglas genéricas: si las piezas centran el título script, el catálogo lo centra.
