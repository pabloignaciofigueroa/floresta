"""Fase 05: favicons (16–512, ICO, apple-touch), firma horizontal/vertical y OG 1200x630, rasterizados con Playwright."""
import os, re
from playwright.sync_api import sync_playwright
from PIL import Image
R = os.path.abspath('.')
L = 'brand/logo/'
iso = open(L + 'isotipo.svg').read()
logo = open(L + 'logotipo.svg').read()
logo_inner = re.sub(r'^<svg[^>]*>|</svg>$', '', logo)
FONTS = f"""@font-face{{font-family:Allura;src:url(file://{R}/assets/fonts/allura-latin-400-normal.woff2)}}
@font-face{{font-family:Catamaran;font-weight:700;src:url(file://{R}/assets/fonts/catamaran-latin-700-normal.woff2)}}
@font-face{{font-family:Catamaran;font-weight:600;src:url(file://{R}/assets/fonts/catamaran-latin-600-normal.woff2)}}"""

# Firma: logotipo + "BY ALMÁCIGOS CHILOÉ" (como en la pieza del Día de la Novia), con el texto pasado a trazos vía fontTools
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
def texto_a_path(txt, font, size, tracking=0.0):
    f = TTFont(font); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    s = size / upm; x = 0; ds = []
    for ch in txt:
        gn = cmap[ord(ch)]; pen = SVGPathPen(gs)
        gs[gn].draw(TransformPen(pen, (s, 0, 0, -s, x, 0))); ds.append(pen.getCommands())
        x += gs[gn].width * s + tracking * size
    return ' '.join(ds), x - tracking * size
by_d, by_w = texto_a_path('BY ALMÁCIGOS CHILOÉ', 'assets/fonts/catamaran-latin-600-normal.woff2', 150, 0.22)
W = 4084
firma = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 900" role="img" aria-label="Floresta by Almácigos Chiloé" style="color:#32583c">'
         f'{logo_inner}<path fill="currentColor" transform="translate({(W - by_w) / 2:.1f} 860)" d="{by_d}"/></svg>')
open(L + 'firma.svg', 'w').write(firma)
open(L + 'firma-claro.svg', 'w').write(firma.replace('color:#32583c', 'color:#f7f4ed'))
open(L + 'logotipo-claro.svg', 'w').write(logo.replace('color:#32583c', 'color:#f7f4ed'))

# Vertical: isotipo sobre la firma
iso_inner = re.sub(r'^<svg[^>]*>|</svg>$', '', iso)
vert = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 4300" role="img" aria-label="Floresta by Almácigos Chiloé" style="color:#32583c">'
        f'<g transform="translate({(W - 2342 * 1.05) / 2:.0f} 0) scale(1.05)">{iso_inner}</g>'
        f'<g transform="translate(0 3400)">{logo_inner}<path fill="currentColor" transform="translate({(W - by_w) / 2:.1f} 860)" d="{by_d}"/></g></svg>')
open(L + 'vertical.svg', 'w').write(vert)

# Favicon SVG: isotipo sobre círculo salvia (como la mancha salvia de las piezas)
fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3200 3200"><circle cx="1600" cy="1600" r="1600" fill="#a8baa2"/>'
       f'<g transform="translate({(3200 - 2342 * .9) / 2:.0f} {(3200 - 2961 * .9) / 2:.0f}) scale(.9)">{iso_inner}</g></svg>')
open(L + 'favicon.svg', 'w').write(fav)
os.makedirs('assets/icons', exist_ok=True)
open('assets/icons/favicon.svg', 'w').write(fav)

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg = b.new_page()
    def shot(html, w, h, out, transparent=False):
        pg.set_viewport_size({'width': w, 'height': h})
        open('/tmp/_shot.html', 'w').write(f'<html><style>{FONTS} html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden}}</style><body>{html}</body></html>')
        pg.goto('file:///tmp/_shot.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        pg.screenshot(path=out, omit_background=transparent)
    for s in (16, 32, 48, 180, 192, 512):
        shot(f'<img src="file://{R}/{L}favicon.svg" style="width:{s}px;height:{s}px;display:block">', s, s, f'assets/icons/icon-{s}.png', True)
    Image.open('assets/icons/icon-48.png').save('assets/icons/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
    os.replace('assets/icons/icon-180.png', 'assets/icons/apple-touch-icon.png')
    # PNG de las variantes del logo
    for n, bg in (('firma', '#f7f4ed'), ('vertical', '#f7f4ed'), ('isotipo', '#a8baa2')):
        shot(f'<div style="background:{bg};width:1200px;height:800px;display:grid;place-items:center"><img src="file://{R}/{L}{n}.svg" style="max-width:900px;max-height:640px"></div>', 1200, 800, f'brand/logo/{n}.png')
    # OG 1200x630: campo bosque, isotipo claro, firma clara, lema en script
    og = f'''<div style="width:1200px;height:630px;background:#406345;display:grid;grid-template-columns:420px 1fr;align-items:center;color:#f7f4ed">
      <div style="display:grid;place-items:center;height:100%;background:radial-gradient(circle at 50% 50%,#a8baa2 0 39%,transparent 39.3%)"><img src="file://{R}/{L}isotipo.svg" style="height:430px"></div>
      <div style="padding-right:70px"><img src="file://{R}/{L}firma-claro.svg" style="width:640px;display:block">
      <p style="font:68px/1.05 Allura;color:#c9d6c4;margin:44px 0 0">Silvestre. Elegante.<br>Es Floresta.</p>
      <p style="font:600 22px Catamaran;letter-spacing:.14em;color:#c9d6c4;margin:26px 0 0">ESMERALDA 198 · CASTRO · CHILOÉ</p></div></div>'''
    shot(og, 1200, 630, 'assets/og.png')
    b.close()
Image.open('assets/og.png').convert('RGB').save('assets/og.jpg', quality=88)
os.remove('assets/og.png')
print('ok')
