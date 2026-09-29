# Floresta · Castro, Chiloé

Sitio web y tienda de **Floresta**, florería en Esmeralda 198, Castro.
Flores lindas, para momentos que importan.

Sitio estático (HTML + CSS + JS), sin paso de compilación. Se publica tal cual en GitHub Pages, Netlify o cualquier hosting.

## Ver el sitio en tu computador

Abre `index.html` en el navegador. Para que los videos y la secuencia de cuadros carguen bien, mejor servirlo:

```bash
npx serve .
# o
python -m http.server 8000
```

## Publicar con GitHub Pages

Settings → Pages → Source: *Deploy from a branch* → Branch `main`, carpeta `/ (root)`.
Queda en `https://pabloignaciofigueroa.github.io/lafloresta/`.

## Estructura

| Carpeta | Qué hay |
|---|---|
| `index.html` | La página completa |
| `css/styles.css` | Estilos (paleta de la fachada: verde, menta, coral; girasol para temporada) |
| `js/app.js` | Animaciones, tienda, carrito y pedido por WhatsApp |
| `js/vendor/` | GSAP (ScrollTrigger, Draggable, Inertia, Flip, SplitText), Lenis, Matter.js |
| `assets/img/` | Fotos reales de @florestaenchiloe (`t/` = recortes 4:5 para tarjetas) |
| `assets/video/` | Loops de video de la portada y la sección de temporada |
| `assets/seq/` | 110 cuadros del video de la florista armando un arreglo (se reproduce con el scroll) |
| `assets/brand/` | Logotipo e isotipo optimizados para web, favicon |
| `marca/` | Archivos originales de logotipo, isotipo e imagotipo |
| `herramientas/` | Scripts para descargar el Instagram y extraer las mejores tomas de video |
| `docs/` | Ficha del producto y dirección de diseño |
| `archivo/` | Versión anterior del sitio y fotos de WhatsApp |

## Editar lo más común

- **Precios y productos**: `js/app.js`, lista `const P = [ ... ]`. Cada fila es `[imagen, nombre, descripción, precio, categorías]`. Los precios actuales son **de ejemplo**.
- **Ramos destacados (galería horizontal)**: `const FAV` en `js/app.js`.
- **Tarjetas para deslizar**: `const DECK` en `js/app.js`.
- **WhatsApp**: `const WA = '56964838490'` en `js/app.js`.
- **Horario y dirección**: sección `visit` en `index.html`. Verificar el horario antes de publicar.

## Cómo funciona el pedido

El carrito junta productos, mensaje de la tarjeta, fecha, horario, dirección y quién recibe, y abre WhatsApp con el pedido armado para +56 9 6483 8490. No hay pasarela de pago.

## Qué se mueve

Pantalla de carga con el isotipo · portada con tres videos · franjas de texto que reaccionan a la velocidad del scroll · manifiesto que se revela palabra por palabra · secuencia de 110 cuadros controlada por el scroll · lista de ocasiones con imagen que sigue al cursor · galería horizontal fija con tarjetas 3D · filtros animados (Flip) · foto que vuela al carrito · tarjetas para deslizar tipo Tinder · paneles de servicios que se apilan · carrusel con inercia · pie de página con flores con física (Matter.js). Respeta `prefers-reduced-motion`.
