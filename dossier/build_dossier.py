#!/usr/bin/env python3
"""Dossier de decisiones de diseño — Floresta (para Natalia).

Genera dossier/floresta-dossier-diseno.html: láminas de 13 × 8,5 in para imprimir.
Izquierda: la sección del sitio (computador + celular). Derecha: la disección.
Todo queda embebido (imágenes y letras) para enviarlo como un solo archivo.
Uso: python3 dossier/build_dossier.py
"""
import base64, glob, html, io, json, pathlib
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / 'dossier'
SH = D / 'shots'
FOTOS = ROOT / 'assets/raw/fotos'
PIEZAS = ROOT / 'assets/raw/piezas'
ALM = ROOT / 'assets/raw/almacigos/fotos'

MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
_FL = {p['code']: p['fecha'][:10] for p in json.load(open(ROOT / 'assets/raw/textos/floresta_textos.json'))['publicaciones']}
_AL = {p['code']: p['fecha'][:10] for p in json.load(open(ROOT / 'assets/raw/almacigos/almacigos_textos.json'))['publicaciones']}


def fecha(iso):
    y, m, d = iso.split('-')
    return f'{int(d)} {MESES[int(m) - 1]} {y}'


def ig(code, extra=''):
    return f'Instagram · {fecha(_FL[code])}' + (f' · {extra}' if extra else '')


def iga(code, extra=''):
    return f'Instagram de Almácigos Chiloé · {fecha(_AL[code])}' + (f' · {extra}' if extra else '')


# ---------------------------------------------------------------- imágenes
def b64img(img, w, q=80):
    img = img.convert('RGB')
    if img.width > w:
        img = img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def shot(name, w=1500):
    p = SH / f'{name}.jpg'
    return b64img(Image.open(p), w) if p.exists() else ''


def _find(stem):
    for base in (FOTOS, PIEZAS, ALM):
        p = base / f'{stem}.jpg'
        if p.exists():
            return p
    p = ROOT / stem
    return p if p.exists() else None


def src(stem, w=420):
    """Miniatura del archivo original (sin recortar)."""
    p = _find(stem)
    if not p:
        raise SystemExit(f'falta original: {stem}')
    return b64img(ImageOps.exif_transpose(Image.open(p)), w, 76)


def raw(stem, w=1950):
    return b64img(ImageOps.exif_transpose(Image.open(_find(stem))), w, 82)


def font(name):
    return 'data:font/woff2;base64,' + base64.b64encode((ROOT / 'assets/fonts' / f'{name}.woff2').read_bytes()).decode()


def png_tint(rel, color, w=900):
    im = Image.open(ROOT / rel).convert('RGBA')
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    if color:
        solid = Image.new('RGBA', im.size, color)
        solid.putalpha(im.getchannel('A'))
        im = solid
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


E = html.escape
INK, BASE, FRAMB, ROSA, EUCA = '#2f2238', '#fffbfa', '#b8457a', '#f6e3ea', '#67a284'
ISO = png_tint('dossier/png/isotipo.png', None, 400)
ISO_INK = png_tint('dossier/png/isotipo.png', INK, 400)
MARK = f'<img class="mk" src="{ISO}" alt="">'
FIRMA = 'Silvestre. Elegante. Es Floresta.'
URL = 'pabloignaciofigueroa.github.io/lafloresta'

RECORRIDO = ['Precarga', 'Portada', 'Manifiesto', 'Ramos', 'Esmeralda 198', 'Comienza con una idea',
             'Ocasiones', 'Del jardín', 'Visítanos']
GOOGLE = 'Reseña en Google'
CAT = 'Catálogo Día de la Madre 2026 · pieza gráfica'
SABER = 'Pieza gráfica "Debes saber…" · 2026'


# ---------------------------------------------------------------- piezas de lámina
def quote(text, source):
    return f'<blockquote class="q"><p>{text}</p><cite>{E(source)}</cite></blockquote>'


def thumbs(items, tall=False):
    out = [f'<figure class="th"><img src="{src(stem)}" alt=""><figcaption>{cap}</figcaption></figure>' for stem, cap in items]
    return f'<div class="ths {"tall" if tall else ""}">{"".join(out)}</div>'


def chips(items):
    return '<div class="chips">' + ''.join(
        f'<span class="chip"><i style="background:{hx}"></i><b>{E(n)}</b> {hx.upper()}</span>' for n, hx in items) + '</div>'


def block(title, body, cls=''):
    return f'<section class="bk {cls}"><h4>{title}</h4>{body}</section>'


def recorrido(cur):
    li = ''.join(f'<li class="{"on" if r == cur else ""}">{E(r)}</li>' for r in RECORRIDO)
    return f'<ol class="rec">{li}</ol>'


def pie(n):
    return f'<footer class="pf"><span>Floresta · Decisiones de diseño del sitio</span><span>{FIRMA}</span><span>{n:02d}</span></footer>'


def lamina_seccion(n, nombre, titulo, lead, desk, mob, bloques, nota_izq='', desk2=None):
    left_extra = f'<img class="desk2" src="{shot(desk2)}" alt="">' if desk2 else ''
    if desk2:
        mob = None
    mob_html = f'<img class="mob" src="{shot(mob, 520)}" alt="">' if mob else ''
    return f'''
<article class="lam">
  <div class="L {'two' if desk2 else ''}">
    <p class="lab">Sitio · computador</p>
    <img class="desk" src="{shot(desk)}" alt="">
    {left_extra}
    <div class="Lrow">
      {f'<div class="mobw"><p class="lab">Celular</p>{mob_html}</div>' if mob else ''}
      <div class="Linfo">
        <p class="lab">Lugar en el recorrido</p>
        {recorrido(nombre)}
        {f'<p class="lnote">{nota_izq}</p>' if nota_izq else ''}
      </div>
    </div>
  </div>
  <div class="R">
    <p class="kick">{n:02d} · {E(nombre)}</p>
    <h2>{titulo}</h2>
    <p class="lead">{lead}</p>
    <div class="grid">{''.join(bloques)}</div>
    {pie(n)}
  </div>
</article>'''


def lamina_libre(n, left_html, right_html, left_cls='', right_cls=''):
    return f'''
<article class="lam">
  <div class="L {left_cls}">{left_html}</div>
  <div class="R {right_cls}">{right_html}{pie(n)}</div>
</article>'''


L = []
n = 0


def nx():
    global n
    n += 1
    return n


# ================================================================ 01 · Portada
nx()
L.append(f'''
<article class="lam cover">
  <div class="L full"><img class="bleed" src="{raw('20260907_DdAPKv2hBR3_1')}" alt="" style="object-position:50% 45%"></div>
  <div class="R center">
    <img class="cover-iso" src="{ISO}" alt="">
    <h1>FLORESTA</h1>
    <p class="sub">Decisiones de diseño del sitio web</p>
    <p class="for">Preparado para Natalia</p>
    <p class="meta">Esmeralda 198 · Castro, Chiloé · Octubre 2026</p>
    <p class="coords">{FIRMA}</p>
    <footer class="pf"><span>{URL}</span><span></span><span>01</span></footer>
  </div>
</article>''')

# ================================================================ 02 · Carta
nx()
L.append(lamina_libre(n,
    f'<img class="bleed" src="{raw("20250717_DMMDzwHgpZN_1")}" alt="" style="object-position:50% 30%">',
    f'''<p class="kick">Antes de empezar</p>
    <h2>Un sitio hecho con lo que tú ya dijiste</h2>
    <div class="letter">
      <p>Natalia:</p>
      <p>Este sitio nació de mirar con atención lo que Floresta ya publica. No hay frases inventadas: cada título y cada párrafo sale de tus publicaciones de Instagram, de tus piezas gráficas o de lo que tus clientes escribieron en Google. Lo que hicimos fue ordenarlo, darle aire y ponerlo en movimiento.</p>
      <p>Tampoco hay fotos de banco de imágenes. Todas las fotos y los videos son de Floresta y de Almácigos Chiloé, tal como los publicaste, y la letra, los colores y el ramo del logo se construyeron a partir de tus propias piezas.</p>
      <p>Este documento explica, sección por sección, qué se decidió y por qué. En cada lámina, a la izquierda está la sección tal como se ve en el sitio, en computador y en celular. A la derecha, de dónde salió cada texto e imagen, qué letra y qué color se usó, cómo se compuso y por qué va en ese lugar del recorrido.</p>
      <p>Es un regalo. Ojalá lo disfrutes tanto como nosotros disfrutamos haciéndolo.</p>
      <p class="sign">Pablo Figueroa G.<br>Director de estudio</p>
    </div>''', left_cls='full'))

# ================================================================ 03 · De dónde viene todo
nx()
grid_ig = ''.join(f'<img src="{src(s, 300)}" alt="">' for s in [
    '20260907_DdAPKv2hBR3_1', '20250506_DJSxjSCAghA_1', '20260617_DZsd-uBBSK0_1', '20251004_DPZAK2UAGz6_1', '20250528_DKLZLxAgLsj_1',
    '20260908_DdC3QVghbB3_1', '20250530_DKQhQDfAplW_1', '20260423_DXeWb3oFuvG_1', '20251027_DQUMiXogMXv_1', '20260904_Dc4DvMFhMoP_1',
    '20250517_DJvWKLcgAc9_1', '20250514_DJohm66gLB5_1', '20250717_DMMDzwHgpZN_1', '20260627_DaGBcNkg4xT_1', '20251115_DRFHHhKkdYz_1'])
piezas = ''.join(f'<img src="{src(s, 260)}" alt="">' for s in ['20260504_DX69F30lsj8_3', '20260504_DX69F30lsj8_2', '20260801_DberjTWBJ-u_1', '20260915_DdSsnKwgGa6_1'])
L.append(lamina_libre(n,
    f'''<p class="lab">Instagram @florestaenchiloe · mayo 2025 a septiembre 2026</p>
    <div class="igrid">{grid_ig}</div>
    <p class="lab" style="margin-top:.16in">Piezas gráficas de Floresta</p>
    <div class="dgrid">{piezas}</div>''',
    f'''<p class="kick">Materia prima</p>
    <h2>De dónde viene todo</h2>
    <p class="lead">Antes de diseñar, reunimos todo lo que Floresta ya había publicado y lo ordenamos: ramos, la fachada, el mesón, el vivero, las ocasiones y las piezas gráficas.</p>
    <div class="grid">
      {block('Instagram @florestaenchiloe', '<p><b>658 publicaciones</b>, con sus textos completos, <b>879 fotos</b> y <b>110 videos</b>. De ahí salen los títulos, los párrafos y casi todas las imágenes del sitio.</p>')}
      {block('Piezas gráficas', '<p>El catálogo del Día de la Madre 2026, la pieza "Debes saber…", el Día de la Novia y el Día de las Flores Amarillas. De ahí salen los precios de referencia, las notas prácticas y la letra de la marca.</p>')}
      {block('Instagram @almacigoschiloe', '<p>De sus publicaciones, el sitio usa <b>5</b>: 3 de fotos y 2 de video, para presentar a Almácigos Chiloé con su propio material.</p>')}
      {block('Google', '<p><b>5,0 en 6 reseñas.</b> Dos de ellas se citan en el sitio tal como fueron escritas, con su ortografía.</p>')}
      {block('La regla', '<p>Cada texto del sitio tiene su origen identificado: qué publicación, qué pieza o qué reseña. Lo único escrito para el sitio son las indicaciones de uso: los botones, el formulario del pedido y la ayuda del mapa.</p>', 'wide')}
    </div>'''))

# ================================================================ 04 · La voz
nx()
L.append(lamina_libre(n,
    f'''<p class="lab">Pieza gráfica · Día de la Novia · {E(ig('DberjTWBJ-u'))}</p>
    <img class="piece" src="{src('20260801_DberjTWBJ-u_1', 900)}" alt="" style="object-position:50% 40%">
    <div class="pair"><img src="{src('20250528_DKLZLxAgLsj_1', 600)}" alt=""><img src="{src('20260627_DaGBcNkg4xT_1', 600)}" alt=""></div>''',
    f'''<p class="kick">Sistema · voz</p>
    <h2>Escribir como Floresta</h2>
    <p class="lead">El sitio no agrega adjetivos ni promesas: escribe con la voz que Floresta ya construyó, cálida y cercana, y pone cada frase en el lugar justo.</p>
    <div class="grid">
      {block('Una firma propia', quote('Silvestre. Elegante. Es Floresta.', ig('DMIK3D4Apyi')) + quote('Mientras más silvestre… ¡mejor!', ig('DMppRews63d')))}
      {block('El oficio, contado de cerca', quote('Cada ramo que sale de nuestra florería comienza mucho antes de elegir las flores.', ig('DaBGf9WByJu')))}
      {block('Un vocabulario propio', '<p>Silvestre, soñado, ramito, detalles, con cariño. Y el nombre completo cuando corresponde: <b>Floresta by Almácigos Chiloé</b>, que une la florería con el vivero de Pidpid.</p>')}
      {block('Cerca, como en el mesón', quote('Cariños para todos!', ig('DMMDzwHgpZN')) + '<p>Los cierres afectuosos de las publicaciones se mantienen tal cual, con sus signos.</p>')}
      {block('Para todas las ocasiones', '<p>La misma voz que celebra un cumpleaños acompaña una despedida, con respeto. El sitio respeta ese tono en cada sección.</p>', 'wide')}
    </div>'''))

# ================================================================ 05 · Tipografía
nx()
L.append(lamina_libre(n,
    f'''<p class="lab">Pieza original · {E(CAT)}</p>
    <img class="piece" src="{src('20260504_DX69F30lsj8_3', 900)}" alt="" style="max-height:1.55in;object-fit:cover;object-position:50% 12%">
    <p class="lab" style="margin-top:.18in">Las letras del sitio</p>
    <div class="spec">
      <p class="sp1">Regala flores. <em>Flores de verdad.</em></p><p class="cap">Fraunces · títulos y frases de la marca</p>
      <p class="sp2">De esas que tienen aroma, textura, movimiento y vida.</p><p class="cap">Figtree · bajadas, párrafos y botones</p>
      <p class="sp3">ESMERALDA 198 · CASTRO</p><p class="cap">Figtree en mayúsculas pequeñas y espaciadas · rótulos</p>
    </div>''',
    f'''<p class="kick">Sistema · tipografía</p>
    <h2>Una letra con curvas de pétalo</h2>
    <p class="lead">En sus piezas impresas, los títulos de Floresta van en una letra manuscrita. En la web se leen en pantallas pequeñas y mientras la página se mueve, así que los títulos usan una letra elegante y con personalidad, pero que se lee de una.</p>
    <div class="grid">
      {block('Fraunces · títulos', '<p>Una serif de curvas blandas, casi orgánicas, emparentada con los remates del logotipo FLORESTA. Su cursiva destaca una palabra en color frambuesa, como en el lema: <i>Elegante.</i></p>')}
      {block('Figtree · lectura', '<p>Una letra sin remates, redonda y cálida, que se lee cómoda en celular. Va en las bajadas, los párrafos, los precios y los botones, y en versión liviana bajo cada publicación.</p>')}
      {block('Tamaños', '<p>Pocos tamaños y bien contrastados: el logo, enorme; los títulos, grandes y serenos; los párrafos, cómodos y con espacio entre líneas; los rótulos, pequeños y espaciados.</p>')}
      {block('Primero, que se lea', '<p>Antes de lo bonito, la funcionalidad: un precio, un horario o una dirección se leen sin esfuerzo, incluso con sol sobre la pantalla.</p>')}
      {block('Un detalle', '<p>Las letras viajan con el propio sitio y ya están listas cuando se abre la portada. Así el texto nunca cambia de forma mientras se lee.</p>', 'wide')}
    </div>'''))

# ================================================================ 06 · Paleta
nx()
pal = ''.join(f'<img src="{src(s, 330)}" alt="">' for s in ['20251115_DRFHHhKkdYz_1', '20250517_DJvWKLcgAc9_1', '20260627_DaGBcNkg4xT_1',
                                                            '20250530_DKQhQDfAplW_1', '20260617_DZsd-uBBSK0_1', '20251004_DPZAK2UAGz6_1'])
sw = [('Blanco rosado', '#fffbfa', INK), ('Rosa empolvado', '#f6e3ea', INK), ('Lila', '#efe8f6', INK), ('Eucalipto claro', '#e2efe8', INK),
      ('Frambuesa', '#b8457a', BASE), ('Eucalipto', '#67a284', BASE), ('Berenjena', '#2f2238', BASE)]
swh = ''.join(f'<span style="background:{hx};color:{tc}">{nm}<br>{hx.upper()}</span>' for nm, hx, tc in sw)
L.append(lamina_libre(n,
    f'''<p class="lab">De estas imágenes salen los colores</p><div class="pgrid">{pal}</div>
    <div class="swatches">{swh}</div>''',
    f'''<p class="kick">Sistema · color</p>
    <h2>La paleta está en sus ramos</h2>
    <p class="lead">Los colores salen de lo que más se repite en las fotos de Floresta: el papel rosado de los ramos, las rosas fucsia, los lisianthus morados y el verde de la fachada y de las hojas.</p>
    <div class="grid">
      {block('Claros, para respirar', chips([('Blanco rosado', '#fffbfa'), ('Rosa empolvado', '#f6e3ea'), ('Lila', '#efe8f6')]) + '<p>Son el fondo de la mayoría de las secciones. Dejan que las flores pongan el color.</p>')}
      {block('Fuertes, para marcar', chips([('Berenjena', '#2f2238'), ('Frambuesa', '#b8457a')]) + '<p>Dos secciones van en berenjena (los ramos y la historia) y el pie en frambuesa. Así cada cambio de color marca un capítulo y ninguna sección se pierde entre las otras.</p>')}
      {block('El verde, con medida', chips([('Eucalipto', '#67a284'), ('Eucalipto claro', '#e2efe8')]) + '<p>El verde de la fachada y de sus piezas aparece en una sola sección grande, Del jardín, y en pequeños detalles. Ocupa menos de un cuarto de la página, para que las flores sean las protagonistas.</p>')}
      {block('Legibilidad', '<p>Cada combinación de texto y fondo se revisó para que se lea con holgura, incluso con poca vista o con el sol sobre la pantalla.</p>')}
    </div>'''))

# ================================================================ 07 · Isotipo
nx()
L.append(lamina_libre(n,
    f'''<div class="logos">
      <p class="lab" style="grid-column:1/-1;margin-bottom:4pt">El ramo y el logotipo · variantes de uso</p>
      <div class="lg light"><img src="{ISO}" alt=""></div>
      <div class="lg dark"><img src="{png_tint('dossier/png/isotipo.png', BASE, 400)}" alt=""></div>
      <div class="lg light wide"><img src="{png_tint('dossier/png/logotipo.png', INK, 1200)}" alt=""></div>
      <div class="lg framb"><img src="{png_tint('dossier/png/firma-claro.png', BASE, 900)}" alt=""></div>
      <div class="lg light"><img src="{png_tint('assets/icons/icon-192.png', None, 192)}" alt="" style="width:34%"></div>
    </div>''',
    f'''<p class="kick">Sistema · logo</p>
    <h2>El ramo del letrero</h2>
    <p class="lead">El logotipo FLORESTA y el ramo del letrero de Esmeralda 198 se redibujaron siguiendo sus trazos originales, para que se vean nítidos a cualquier tamaño, desde el ícono de la pestaña del navegador hasta un letrero.</p>
    <div class="grid">
      {block('Trazos respetados', '<p>Las letras del logotipo conservan sus remates y la A con su curva. El ramo mantiene sus flores coral, sus hojas y el lazo.</p>')}
      {block('Variantes', '<p>El ramo en color y en claro, el logotipo en berenjena y en blanco, y la firma "by Almácigos Chiloé" para el pie.</p>')}
      {block('En la pestaña del navegador', '<p>El ramo solo, sin fondo, con trazos más firmes para que se reconozca aun muy pequeño. Cuando el navegador usa fondo oscuro, las hojas pasan a claro.</p>')}
      {block('Dónde aparece', '<p>El ramo se dibuja en la pantalla de carga. El logotipo encabeza la portada a gran escala, vive en la barra superior y cierra el pie con la firma completa.</p>')}
    </div>''', left_cls='full'))

# ================================================================ 08 · Recorrido
nx()
strip = ''.join(f'<figure><img src="{shot(s, 420)}" alt=""><figcaption>{c}</figcaption></figure>' for s, c in [
    ('d-hero', 'Portada'), ('d-cont', 'Manifiesto'), ('d-ramos', 'Ramos'), ('d-esm', 'Esmeralda 198'), ('d-hist', 'Comienza con una idea'),
    ('d-ocas', 'Ocasiones'), ('d-alm', 'Del jardín'), ('d-visita-prod', 'Visítanos'), ('d-foot', 'Pie')])
L.append(lamina_libre(n,
    f'<p class="lab">El recorrido completo, de arriba hacia abajo</p><div class="strip">{strip}</div>',
    f'''<p class="kick">Sistema · recorrido</p>
    <h2>Del ramo a la puerta de la florería</h2>
    <p class="lead">El orden de la página no es una lista de servicios: es una visita que empieza con un ramo en la mano y termina en Esmeralda 198.</p>
    <div class="grid">
      {block('1 · Llegar', '<p>Tres ramos a pantalla completa y el lema. Luego, el manifiesto con sus propias palabras y una cinta de ramos que no se detiene.</p>')}
      {block('2 · Elegir', '<p>El catálogo con precios de referencia y la opción de armar el pedido ahí mismo. Lo concreto aparece temprano, para quien ya sabe lo que busca.</p>')}
      {block('3 · Conocer', '<p>Esmeralda 198 y sus once ramos, la historia de Natalia en video, las ocasiones y el vivero de Almácigos Chiloé.</p>')}
      {block('4 · Venir', '<p>El mapa con el punto exacto, lo que dicen sus clientes y las notas prácticas para pedir. Recién al final, cuando ya se decidió.</p>')}
      {block('Ritmo', '<p>Se alternan secciones claras de lectura con dos secciones oscuras y un pie frambuesa, como respirar. Ninguna composición se repite dos veces seguidas: carrusel, mazo, videos, franjas, fichas.</p>', 'wide')}
    </div>'''))


# ================================================================ secciones
def S(nombre, titulo, lead, desk, mob, bloques, nota='', desk2=None):
    L.append(lamina_seccion(nx(), nombre, titulo, lead, desk, mob, bloques, nota, desk2))


S('Precarga', 'Floresta · Esmeralda 198',
  'Antes de entrar, el sitio deja listo lo que se ve primero. Mientras tanto se dibuja el ramo del logo y un porcentaje muestra cuánto falta. Debajo, el nombre y la dirección.',
  'd-loader', None, [
      block('Qué se ve', '<p>El ramo se dibuja de abajo hacia arriba, como si creciera desde el lazo, y debajo avanza el porcentaje. Al llegar a cien, la pantalla sube como una cortina y aparece la portada.</p>'),
      block('Qué se deja listo', '<p>Las letras, las tres fotos de la portada, las fotos del manifiesto, la cinta de ramos y la primera imagen de cada video. Así nada aparece borroso ni a medio cargar.</p>'),
      block('Tiempos', '<p>Dura casi dos segundos aunque la conexión sea rápida, para que se alcance a ver. Y nunca más de seis, aunque la conexión sea lenta. Los videos siguen llegando solos, en el orden de la página, para que ya estén corriendo cuando se llega a ellos.</p>'),
      block('Por qué', '<p>Floresta es una marca de fotos y videos. Una espera breve y cuidada vale más que una página que aparece a saltos.</p>'),
  ], nota='Captura tomada mientras el porcentaje avanza.')

S('Portada', 'Silvestre. Elegante. Es Floresta.',
  'Tres ramos a pantalla completa, sostenidos frente a la florería, se turnan cada pocos segundos. Encima, solo el logotipo y el lema, al centro.',
  'd-hero', 'm-hero', [
      block('Textos', quote('Silvestre. Elegante. Es Floresta.', ig('DMIK3D4Apyi')) + '<p>El lema es la única frase de la portada. No hay botones: el botón "Pedido" está siempre arriba, a mano.</p>'),
      block('Imágenes', thumbs([('20260907_DdAPKv2hBR3_1', 'Rosas rojas · ' + ig('DdAPKv2hBR3')), ('20260908_DdC3QVghbB3_1', 'Natalia y un ramo gigante · ' + ig('DdC3QVghbB3')), ('20260627_DaGBcNkg4xT_1', 'Rosas y lisianthus · ' + ig('DaGBcNkg4xT'))])),
      block('Movimiento', '<p>Al abrir, la foto se expande desde un marco de esquinas suaves hasta llenar la pantalla y el logotipo sube desde detrás de una línea. Cada ramo cede su lugar al siguiente con una cortina suave; los puntos de abajo se van llenando. En celular se cambia de ramo deslizando el dedo.</p>'),
      block('Por qué así', '<p>Así es como Floresta muestra sus ramos en Instagram: en la mano, frente a la florería. La primera imagen ya dice qué es y dónde está.</p>'),
  ])

S('Manifiesto', 'Ramos con alma',
  'Una pausa clara después de la portada: el manifiesto de Floresta a la izquierda y sus ramos frente al letrero, a la derecha. Debajo, una cinta de ramos que corre sola.',
  'd-cont', 'm-cont', [
      block('Textos', quote('En Floresta no hacemos “arreglos”, hacemos ramos con alma.', ig('DLUq_50AvEX')) + quote('Nuestros diseños tienen un estilo único: más natural, más libre, más sureño.', ig('DLUq_50AvEX')) + quote('Mientras más silvestre… ¡mejor!', ig('DMppRews63d'))),
      block('Imágenes', thumbs([('20260617_DZsd-uBBSK0_1', 'Frente al letrero · ' + ig('DZsd-uBBSK0')), ('20260423_DXeWb3oFuvG_1', 'Rosas bicolor · ' + ig('DXeWb3oFuvG')), ('20250506_DJSxjSCAghA_1', 'Girasoles e iris · ' + ig('DJSxjSCAghA')), ('20251004_DPZAK2UAGz6_1', 'Tulipanes · ' + ig('DPZAK2UAGz6'))])),
      block('Composición', '<p>La foto grande se sale por el borde derecho, con esquinas suaves y aire respecto de la portada. Una segunda foto se monta sobre ella, más pequeña. Ninguna foto va encerrada en formas: se muestran libres, como en sus publicaciones.</p>'),
      block('Movimiento', '<p>Las fotos flotan a distinta profundidad cuando se mueve el cursor. La cinta de ocho ramos corre sola, se calma al pasar el cursor y se inclina levemente al bajar rápido. Al pasar sobre ella aparece "Ver ramos".</p>'),
  ], desk2='d-cinta')

S('Ramos', 'Regala flores. Flores de verdad.',
  'El catálogo de Floresta, con precios de referencia, en un carrusel que se arrastra. Es la única sección de fondo oscuro arriba en la página, para que el producto resalte.',
  'd-ramos', 'm-ramos', [
      block('Textos', quote('…regala flores. Flores de verdad.', ig('DdSsnKwgGa6')) + quote('De esas que tienen aroma, textura, movimiento y vida.', ig('DdSsnKwgGa6')) + '<p>Los nombres, las descripciones y las notas de cada ramo vienen del catálogo, al pie de la letra.</p>'),
      block('Precios de referencia', '<p>Ramos Silvestres $15.000 · $33.000 · $49.000 · Rosas Rojas, 5/10/20: $21.000 · $39.000 · $79.000 · Ramos de Girasoles, 3/5/10: $14.000 · $22.000 · $40.000 · Rosas y Girasoles, 5/10/20: $21.000 · $39.000 · $79.000 · En la tienda, desde $5.000.</p><p class="small">Fuente: ' + E(CAT) + '. Cada foto lleva "* Ramo de referencia", como en el catálogo.</p>'),
      block('Interacción', '<p>Al elegir un tamaño, el precio rueda al nuevo valor. Al tocar "Agregar", saltan pétalos de colores y el ramo, en miniatura, vuela hasta "Pedido". Las fichas se inclinan levemente hacia el cursor.</p>'),
      block('Por qué así', '<p>Quien llega buscando un ramo encuentra precio y tamaño sin preguntar. El pedido se arma ahí mismo y se envía por WhatsApp, que es como Floresta ya recibe sus pedidos.</p>'),
  ])

S('Esmeralda 198', 'Nunca son idénticas',
  'Once ramos fotografiados frente al mismo letrero, en un mazo que se puede tomar y lanzar con la mano. Cierra con la frase de invierno a pantalla completa.',
  'd-esm', 'm-esm', [
      block('Textos', quote('…las flores son como la naturaleza: nunca son idénticas. Podemos inspirarnos en un diseño, mantener su esencia y estilo, pero cada ramo será siempre único y especial.', ig('DZPs-SVtb-s')) + quote('Aunque estemos en pleno invierno en Chiloé, para nosotros todos los días son primavera.', ig('DavQtc1Bg0w'))),
      block('Imágenes', thumbs([('20251115_DRFHHhKkdYz_1', ig('DRFHHhKkdYz')), ('20260316_DV8ZZI9gCgv_1', ig('DV8ZZI9gCgv')), ('20260410_DW9Nix6gSXd_1', ig('DW9Nix6gSXd')), ('20260814_DcBdWxFBuC7_1', ig('DcBdWxFBuC7'))]) + '<p class="small">Once publicaciones distintas, todas frente al letrero de Esmeralda 198, alineadas para que el letrero quede siempre en el mismo lugar.</p>'),
      block('Interacción', '<p>El ramo de arriba se arrastra y, si se suelta con fuerza, sale volando y vuelve a entrar por debajo del mazo. Al pasar el cursor, los ramos se abren en abanico. El botón "Otro ramo" y el contador permiten recorrerlos sin arrastrar.</p>'),
      block('Por qué aquí', '<p>Es la prueba visual de la frase: el mismo letrero, once ramos distintos. Después del catálogo, muestra que cada ramo es único.</p>'),
  ], desk2='d-invierno')

S('Comienza con una idea', 'Comienza con una idea',
  'La sección de la persona detrás de los ramos, en fondo berenjena: cuatro videos de distintas publicaciones y, debajo, Natalia con sus propias palabras.',
  'd-hist', 'm-hist', [
      block('Textos', quote('Cada ramo que sale de nuestra florería comienza mucho antes de elegir las flores. Comienza con una idea, con una historia y con la intención de emocionar a quien lo recibe.', ig('DaBGf9WByJu')) + quote('Mi destino siempre fueron las plantas y las flores!', ig('DJiZA6bgtDm'))),
      block('Videos', thumbs([('assets/img/poster-oficio-800.webp', 'El mesón · ' + ig('DWh0WXdgKi1')), ('assets/img/poster-ratito-800.webp', 'Un ratito en la florería · ' + ig('Dal1L2VhFpw')), ('assets/img/poster-vitrina-800.webp', 'Ramos listos · ' + ig('DWgtaCRAPFB')), ('assets/img/poster-airelibre-800.webp', 'Matrimonio al aire libre · ' + ig('DTonzAXgLkC'))], tall=True)),
      block('Composición', '<p>Cuatro videos verticales a distintas alturas, con mucho aire entre ellos, que flotan a distinta velocidad al bajar. Bajo cada uno, la frase de su publicación en letra liviana. En celular se recorren deslizando.</p>'),
      block('Por qué aquí', '<p>Después de ver el producto, la visita conoce a quien lo hace. Son cuatro momentos distintos: el oficio en el mesón, un día en la florería, los ramos listos y un matrimonio en el campo.</p>'),
  ], desk2='d-nati')

S('Ocasiones', 'Para celebrar, agradecer, acompañar o despedir',
  'Cinco franjas verticales, una por ocasión. La elegida se abre, corre su video y aparece su frase; las demás se angostan.',
  'd-ocas', 'm-ocas', [
      block('Textos', '<p>Los cinco nombres vienen de una misma publicación: Ramos personalizados · Arreglos florales para toda ocasión · Regalos y detalles · Condolencias y coronas · Despachos en Castro y alrededores (' + E(ig('DcfGCrWhf9E')) + ').</p>' + quote('Una corona floral no es solo un gesto; es una forma de acompañar, honrar y expresar lo que muchas veces las palabras no alcanzan a decir.', ig('Da05yhvBxvM'))),
      block('Videos e imágenes', thumbs([('assets/img/poster-medida-800.webp', 'Hecho a medida · ' + ig('DXVVyQqhF3D')), ('assets/img/poster-iglesia-800.webp', 'Matrimonio · ' + ig('DUQUsMqAHoR')), ('assets/img/poster-carterita-800.webp', 'Carterita con flores · ' + ig('DN1tVVeQADZ')), ('assets/img/poster-corona-800.webp', 'Corona · ' + ig('Da05yhvBxvM'))], tall=True)),
      block('Interacción', '<p>En computador, la franja se abre al pasar el cursor; en celular, al tocarla, y se abre hacia abajo. Solo corre el video de la franja abierta, para que la página se mantenga liviana.</p>'),
      block('Por qué así', '<p>Floresta hace mucho más que ramos, y cada ocasión tiene su tono. Mostrarlas una a la vez da espacio a cada una, incluida la despedida, con el mismo respeto con que Floresta la nombra.</p>'),
  ])

S('Del jardín', 'Del jardín a la florería',
  'La única sección de fondo verde. Primero, los Helleborus cosechados en el vivero. Después, Almácigos Chiloé presentado con fotos y videos de su propio Instagram.',
  'd-jardin', None, [
      block('Textos', quote('Almácigos Chiloé ya no es solo un vivero de plantas… ¡ahora también somos flores, diseño y emociones!', ig('DJ-mvELNwQx')) + quote('Hay lugares que invitan a detenerse, respirar y reconectar… este es uno de ellos.', iga('DXK7qcBERv1'))),
      block('Imágenes del vivero', thumbs([('20260115_DTiL9X9ETwm_1', 'Dalias · ' + iga('DTiL9X9ETwm')), ('20251104_DQobKvtkX2k_1', 'Rododendro · ' + iga('DQobKvtkX2k')), ('20251021_DQFsU65jVtf_2', 'Rododendro · ' + iga('DQFsU65jVtf'))]) + '<p class="small">Además, dos videos del vivero: un campo de dalias y un recorrido con los pavos reales.</p>'),
      block('Interacción', '<p>Las fotos y videos del vivero se deslizan en una fila. Bajo cada uno va la frase con que abre su publicación y un botón pequeño, "Ver publicación", que la abre en Instagram. Arriba, "Conocer @almacigoschiloe" lleva al perfil del vivero.</p>'),
      block('Por qué aquí', '<p>Floresta es "by Almácigos Chiloé". Esta sección deja que la florería presente al vivero con su propio material, y abre la puerta para conocerlo en Pidpid.</p>'),
  ], desk2='d-alm')

S('Visítanos', '¿Buscas flores en Castro? Las encontraste.',
  'El cierre práctico: dónde está, cuándo abre y cómo pedir. Debajo, lo que dicen sus clientes y las notas que conviene saber antes de encargar.',
  'd-visita-prod', None, [
      block('Datos', '<p>Esmeralda 198, Castro, Chiloé · Lunes a sábado, 10:00 a 19:30 hrs · WhatsApp +56 9 6483 8490. El horario es el que Floresta publica en Instagram.</p><p>El mapa queda anclado al punto exacto de la florería, y "Volver a la florería" lo recentra.</p>'),
      block('Lo que dicen', quote('Fantásticas, empáticas y amorosas !!! Y las flores bellas !!!', 'Tamara D. · ' + GOOGLE) + quote('Me encantó el lugar. Hermoso y bien decorado. Los mejores ramos de la ciudad de castro y además en un lugar cómodo y céntrico', 'Ignacio M. · ' + GOOGLE)),
      block('Debes saber…', '<p>Las cinco notas de la pieza "Debes saber…": ramos silvestres, reservas, despacho, horario de despacho y qué incluye cada ramo. Se abren de a una, para no recargar la vista.</p><p class="small">Fuente: ' + E(SABER) + '.</p>'),
      block('Por qué al final', '<p>Lo práctico llega cuando la visita ya decidió. El título es la frase con que Floresta invita en Instagram (' + E(ig('DcfGCrWhf9E')) + '), y la nota 5,0 de Google habla por sí sola.</p>'),
  ], desk2='d-resenas', nota='Captura del sitio publicado, con el mapa real.')

# ================================================================ Detalles
nx()
L.append(lamina_libre(n,
    f'''<p class="lab">El pedido, listo para enviar por WhatsApp</p><img class="desk" src="{shot('d-cart')}" alt="" style="width:88%">
    <p class="lab" style="margin-top:.14in">El mismo sitio en celular</p>
    <div class="mrow">{''.join(f'<img src="{shot(s, 360)}" alt="">' for s in ['m-hero', 'm-ramos', 'm-esm', 'm-ocas', 'm-alm'])}</div>''',
    f'''<p class="kick">Detalles en todo el sitio</p>
    <h2>Lo que no se ve, pero se siente</h2>
    <div class="grid">
      {block('Pedido', '<p>Los ramos elegidos se juntan en "Pedido" y se envían por WhatsApp con el mensaje ya escrito. Con "Retiro en tienda" solo se pide la fecha; con "Despacho" aparecen la dirección y las notas de despacho.</p>')}
      {block('Menú', '<p>En celular, el menú se abre a pantalla completa en rosa empolvado. En computador, una píldora de color se desliza hasta la sección en la que se está.</p>')}
      {block('Movimiento con calma', '<p>Todo arranca rápido y frena suave. Quien tenga activada la opción de "reducir movimiento" en su equipo ve el sitio completo y quieto.</p>')}
      {block('Celular primero', '<p>Cada sección tiene su versión para teléfono: carruseles que se deslizan con el dedo, franjas que se abren hacia abajo y el mapa que se mueve con dos dedos.</p>')}
      {block('Sin saltos', '<p>La página no "brinca" mientras carga ni al bajar. Se revisó en computador grande, tablet y celular.</p>')}
      {block('Accesible', '<p>Textos que se leen bien, recorrido completo con el teclado y todas las imágenes descritas para quienes usan lectores de pantalla.</p>')}
    </div>'''))

# ================================================================ Cierre
nx()
L.append(lamina_libre(n,
    f'<img class="bleed" src="{raw("20251115_DRFHHhKkdYz_1")}" alt="" style="object-position:50% 40%">',
    f'''<div class="center close">
      <img class="mk" src="{ISO}" alt="">
      <p class="kick">Lo que sigue</p>
      <h2>Hacerlo tuyo</h2>
      <p class="lead">Este sitio se hizo solo con lo que ya estaba publicado. Con un par de conversaciones podría ir mucho más lejos:</p>
      <ul class="next">
        <li>Fotografía propia de los ramos de temporada, del taller y tuya</li>
        <li>Los contenidos que quieras contar, con tu voz</li>
        <li>Dominio propio .cl y alojamiento a nombre de Floresta</li>
        <li>Pedidos y pagos en línea, y la coordinación de despachos, más simples</li>
      </ul>
      <p class="invite">Cuando quieras, lo conversamos.</p>
      <p class="who">Pablo Figueroa G.</p>
      <p class="role">Director de estudio</p>
      <p class="contact"><a href="mailto:pablo@bergerac.cl">pablo@bergerac.cl</a> · <a href="tel:+56975892096">+56 9 7589 2096</a></p>
      <p class="link"><a href="https://bergerac.cl">Bergerac.cl</a></p>
      <p class="coords">{FIRMA}</p>
    </div>''', left_cls='full'))

# ================================================================ documento
CSS = f'''
@font-face{{font-family:"Fraunces";font-weight:100 900;src:url({font("fraunces-latin-full-normal")}) format("woff2")}}
@font-face{{font-family:"Fraunces";font-weight:100 900;font-style:italic;src:url({font("fraunces-latin-full-italic")}) format("woff2")}}
@font-face{{font-family:"Figtree";font-weight:300 900;src:url({font("figtree-latin-wght-normal")}) format("woff2")}}
@page{{size:13in 8.5in;margin:0}}
:root{{--base:{BASE};--rosa:{ROSA};--lila:#efe8f6;--euca-claro:#e2efe8;--framb:{FRAMB};--euca:{EUCA};--ink:{INK};--ink2:rgba(47,34,56,.68);--line:rgba(47,34,56,.16)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#d9cfd6}}
body{{font-family:"Figtree",system-ui,sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.disp,h1,h2,.sp1,.who{{font-family:"Fraunces",Georgia,serif;font-variation-settings:"SOFT" 100}}
em,i{{font-family:"Fraunces";font-style:italic;font-variation-settings:"SOFT" 100,"WONK" 1}}
.lam{{width:13in;height:8.5in;display:grid;grid-template-columns:6.5in 6.5in;overflow:hidden;margin:0 auto .3in;background:var(--base);page-break-after:always;break-after:page;position:relative}}
@media print{{html,body{{background:none}}.lam{{margin:0}}}}
.L{{background:var(--ink);color:var(--base);padding:.42in .4in .38in;display:flex;flex-direction:column;gap:.12in;overflow:hidden}}
.L.full{{padding:0}}
.bleed{{width:100%;height:100%;object-fit:cover;display:block}}
.R{{position:relative;padding:.5in .55in .7in;display:flex;flex-direction:column;overflow:hidden}}
.lab{{font-size:6.4pt;font-weight:600;letter-spacing:.2em;text-transform:uppercase;opacity:.82}}
.desk,.desk2{{width:100%;display:block;border-radius:6pt}}
.L.two .desk,.L.two .desk2{{width:88%}}
.L.two .Lrow{{margin-top:0}}
.L.two .rec{{columns:3;font-size:5.8pt;line-height:1.7}}
.Lrow{{display:flex;gap:.22in;align-items:flex-start;margin-top:.04in;min-height:0;flex:1}}
.mobw{{display:flex;flex-direction:column;gap:.08in}}
.mob{{width:1.35in;display:block;border-radius:6pt}}
.Linfo{{flex:1;display:flex;flex-direction:column;gap:.08in}}
.rec{{list-style:none;columns:2;column-gap:.14in;font-size:6.6pt;font-weight:600;letter-spacing:.12em;text-transform:uppercase;line-height:1.85}}
.rec li{{opacity:.4;break-inside:avoid}}
.rec li.on{{opacity:1;color:#fff}}
.rec li.on::before{{content:"";display:inline-block;width:5pt;height:5pt;border-radius:50%;background:#f2879f;margin-right:4pt;vertical-align:1pt}}
.lnote{{font-size:7.6pt;font-style:italic;opacity:.75;line-height:1.4;margin-top:.04in;font-family:"Figtree"}}
.kick{{font-size:7pt;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--framb);margin-bottom:.12in}}
h1{{font-weight:400;font-size:58pt;letter-spacing:.06em;line-height:1;color:var(--ink)}}
h2{{font-weight:400;font-size:24pt;line-height:1.08;letter-spacing:-.01em;margin-bottom:.14in;color:var(--ink)}}
.lead{{font-size:11.6pt;font-weight:400;line-height:1.45;margin-bottom:.2in;max-width:5.4in;color:var(--ink2)}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:.18in .3in;align-content:start}}
.bk h4{{font-size:6.8pt;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--ink);padding-bottom:4pt;border-bottom:.5pt solid var(--line);margin-bottom:6pt}}
.bk p{{font-size:8.9pt;line-height:1.48;margin-bottom:5pt}}
.bk p.small{{font-size:7.2pt;color:var(--ink2)}}
.bk.wide{{grid-column:1/-1}}
.q{{margin:0 0 6pt}}
.q p{{font-family:"Fraunces";font-variation-settings:"SOFT" 100;font-size:9.6pt;font-style:italic;line-height:1.36;margin-bottom:1.5pt}}
.q p::before{{content:"“"}}.q p::after{{content:"”"}}
.q cite{{display:block;font-style:normal;font-size:6.2pt;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--framb)}}
.ths{{display:flex;gap:5pt;flex-wrap:wrap;margin-bottom:4pt}}
.th{{width:calc(25% - 4pt);min-width:.62in}}
.th img{{width:100%;height:.95in;object-fit:cover;display:block;border-radius:4pt}}
.ths.tall .th img{{height:1.2in}}
.th figcaption{{font-size:6pt;line-height:1.25;color:var(--ink2);margin-top:2pt}}
.chips{{display:flex;flex-wrap:wrap;gap:4pt 8pt;margin-bottom:4pt}}
.chip{{display:inline-flex;align-items:center;gap:4pt;font-size:6.8pt}}
.chip i{{width:11pt;height:11pt;display:inline-block;border-radius:50%;outline:.5pt solid var(--line)}}
.chip b{{font-weight:700;letter-spacing:.06em;text-transform:uppercase;font-size:6pt}}
.pf{{position:absolute;left:.55in;right:.55in;bottom:.3in;display:flex;justify-content:space-between;font-size:6pt;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--ink2);border-top:.5pt solid var(--line);padding-top:6pt}}
.mk{{width:.42in;display:block}}
/* portada */
.cover .R.center{{justify-content:center;align-items:center;text-align:center;gap:.14in}}
.cover-iso{{width:.8in;margin-bottom:.06in}}
.cover .sub{{font-size:9.6pt;font-weight:600;letter-spacing:.26em;text-transform:uppercase}}
.cover .for{{font-family:"Fraunces";font-variation-settings:"SOFT" 100;font-size:15pt;font-style:italic;margin-top:.22in;color:var(--framb)}}
.cover .meta{{font-size:9pt;color:var(--ink2)}}
.coords{{font-family:"Fraunces";font-variation-settings:"SOFT" 100;font-style:italic;font-size:10pt;color:var(--ink2);margin-top:.26in}}
/* carta */
.letter p{{font-size:10.2pt;line-height:1.56;margin-bottom:8pt;max-width:5.2in}}
.letter .sign{{font-family:"Fraunces";font-style:italic;margin-top:6pt}}
/* fuentes, paleta, logos, recorrido */
.igrid{{display:grid;grid-template-columns:repeat(5,1fr);gap:4pt}}
.igrid img{{width:100%;aspect-ratio:1;object-fit:cover;display:block;border-radius:3pt}}
.dgrid{{display:grid;grid-template-columns:repeat(4,1fr);gap:4pt}}
.dgrid img{{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 0;display:block;border-radius:3pt}}
.piece{{width:100%;display:block;max-height:3.9in;object-fit:cover;border-radius:6pt}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:6pt;margin-top:6pt}}
.pair img{{width:100%;height:2.1in;object-fit:cover;display:block;border-radius:6pt}}
.spec{{background:var(--base);color:var(--ink);padding:.2in .24in;border-radius:6pt}}
.sp1{{font-size:24pt;line-height:1.05}}
.sp1 em{{color:var(--framb)}}
.sp2{{font-size:12.5pt;font-weight:500;line-height:1.35;margin-top:.12in}}
.sp3{{font-size:8pt;font-weight:700;letter-spacing:.22em;margin-top:.14in;color:var(--framb)}}
.spec .cap{{font-size:5.8pt;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--ink2);margin-top:3pt}}
.pgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:4pt}}
.pgrid img{{width:100%;aspect-ratio:1;object-fit:cover;display:block;border-radius:3pt}}
.swatches{{display:grid;grid-template-columns:repeat(4,1fr);gap:4pt;margin-top:.12in}}
.swatches span{{height:.72in;padding:6pt;font-size:6.2pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;display:flex;align-items:flex-end;line-height:1.5;border-radius:4pt}}
.logos{{display:grid;grid-template-columns:1fr 1fr;gap:6pt;padding:.42in .4in;height:100%;align-content:center}}
.lg{{display:grid;place-items:center;height:1.75in;padding:.25in;border-radius:6pt}}
.lg.light{{background:var(--base)}}.lg.dark{{background:#3d2d48}}.lg.framb{{background:var(--framb)}}
.lg.wide{{grid-column:1/-1;height:1.15in}}
.lg img{{max-width:100%;max-height:1.15in;width:auto;height:auto;display:block}}
.lg.wide img{{max-height:.5in}}
.strip{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6pt}}
.strip figure img{{width:100%;aspect-ratio:16/10;object-fit:cover;object-position:50% 0;display:block;border-radius:4pt}}
.strip figcaption{{font-size:5.8pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;margin-top:3pt;opacity:.82}}
.mrow{{display:grid;grid-template-columns:repeat(5,1fr);gap:5pt}}
.mrow img{{width:100%;display:block;border-radius:4pt}}
/* cierre */
.close{{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;height:100%;gap:.1in}}
.close .mk{{margin-bottom:.12in}}
.next{{list-style:none;margin:.04in 0 .2in}}
.next li{{font-size:10.6pt;line-height:1.5;padding:5pt 0;border-bottom:.5pt solid var(--line)}}
.close a{{color:inherit;text-decoration:none}}
.close .invite{{font-family:"Fraunces";font-variation-settings:"SOFT" 100;font-size:13pt;font-style:italic;margin-bottom:.06in}}
.close .who{{font-size:10pt;letter-spacing:.2em;text-transform:uppercase;color:var(--ink)}}
.close .role{{font-size:9.2pt;margin-top:-4pt}}
.close .contact{{font-size:8.4pt;color:var(--ink2)}}
.close .link{{font-family:"Fraunces";font-variation-settings:"SOFT" 100;font-size:14pt;letter-spacing:.2em;text-transform:uppercase;color:var(--framb);margin-top:.12in}}
.close .coords{{margin-top:.12in}}
'''

DOC = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Floresta · Decisiones de diseño del sitio web</title>
<style>{CSS}</style></head>
<body>
{''.join(L)}
</body></html>'''

out = D / 'floresta-dossier-diseno.html'
out.write_text(DOC, encoding='utf-8')
print(out, round(out.stat().st_size / 1e6, 1), 'MB ·', n, 'láminas')
