#!/usr/bin/env python3
"""Floresta · Decisiones de diseño del sitio web — dossier v4 (19 láminas).

Sistema «dos mitades, dos colores» con los textos del dossier v1.
Izquierda: el sitio (computador y celular). Derecha: las decisiones, en bloques rotulados.
Salida en /tmp/claude-0/dossier-v4/final/.
"""
import base64, glob, html, io, json, pathlib, re
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageOps

ROOT = pathlib.Path('/home/claude/lafloresta')
OUT = pathlib.Path('/tmp/claude-0/dossier-v4/final')
(OUT / 'pages').mkdir(parents=True, exist_ok=True)
SH = ROOT / 'dossier/shots'
SH2 = pathlib.Path('/tmp/claude-0/dossier-v4/shots')  # recapturas propias (es-CL)
RAW = ROOT / 'assets/raw'

W_, R_, L_, EC = '#fffbfa', '#f6e3ea', '#efe8f6', '#e2efe8'
F_, EU, B_ = '#b8457a', '#67a284', '#2f2238'
DARK = {B_, F_}
CNAME = {W_: 'blanco rosado', R_: 'rosa empolvado', L_: 'lila', F_: 'frambuesa', B_: 'berenjena'}

MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
FL = {p['code']: p for p in json.load(open(RAW / 'textos/floresta_textos.json'))['publicaciones']}
AL = {p['code']: p for p in json.load(open(RAW / 'almacigos/almacigos_textos.json'))['publicaciones']}
SITE = (ROOT / 'index.html').read_text(encoding='utf-8')
E = html.escape
URL = 'florestachiloe.vercel.app'


def _norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def fecha(code):
    """Fecha de publicación en hora de Chile (el JSON trae UTC)."""
    p = FL.get(code) or AL[code]
    dt = datetime.fromisoformat(p['fecha'].replace('Z', '+00:00')).astimezone(ZoneInfo('America/Santiago'))
    return f'{dt.day} {MESES[dt.month - 1]} {dt.year}'


def ig(code):
    return (f'Instagram de Almácigos Chiloé · {fecha(code)}' if code in AL and code not in FL
            else f'Instagram · {fecha(code)}')


CHECKED = []


def lit(code, text):
    """Frase literal: debe estar tal cual en el texto de la publicación (se ignoran saltos de línea)."""
    cap = (FL.get(code) or AL[code])['caption']
    core = text.lstrip('…')
    assert _norm(core) in _norm(cap), f'{code}: «{text}» no está literal'
    CHECKED.append((code, text))
    return E(text)


def lit_google(text):
    assert text in SITE, f'reseña no encontrada en el sitio: {text}'
    CHECKED.append(('Google', text))
    return E(text)


def q(code, text, cls='q'):
    return f'<blockquote class="{cls}"><p>“{lit(code, text)}”</p><cite>{ig(code)}</cite></blockquote>'


def qg(text, who, cls='q'):
    return f'<blockquote class="{cls}"><p>“{lit_google(text)}”</p><cite>{who} · Reseña en Google</cite></blockquote>'


# ---------------------------------------------------------------- imágenes
def b64(path, w=1600, crop=None, q_=84):
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    if crop:
        im = im.crop(crop)
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q_, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def d(name, w=1400, top=110, bottom=None, right=None, left=0):
    """Captura de computador sin la franja de navegación del sitio."""
    src = SH2 / f'{name}.jpg' if (SH2 / f'{name}.jpg').exists() else SH / f'{name}.jpg'
    im = Image.open(src)
    sc = im.width / 2160
    return b64(src, w, crop=(left, round(top * sc), right or im.width, bottom or im.height))


# ventana vertical de cada captura de celular: empieza bajo la barra del sitio y termina entre dos bloques
MWIN = {'m-cont': (130, 1790), 'm-hist': (250, 1650), 'm-ocas': (130, 1710), 'm-alm': (260, 1860),
        'm-visita': (175, 1780), 'm-hero': (170, 1960), 'm-ramos': (270, 1870), 'm-esm': (340, 1470),
        'm-foot': (452, 2052)}
MRIGHT = {'m-hero': 905, 'm-hist': 715}


def m(name, w=600):
    top, bot = MWIN[name]
    return b64(SH / f'{name}.jpg', w, crop=(0, top, MRIGHT.get(name, 975), bot))


def igpath(code, n=1):
    for pat in (f'fotos/*_{code}_{n}.jpg', f'piezas/*_{code}_{n}.jpg', f'fotos/portadas/*_{code}_{n}.jpg', f'almacigos/fotos/*_{code}_{n}.jpg'):
        g = glob.glob(str(RAW / pat))
        if g:
            return g[0]
    raise FileNotFoundError(code)


def igimg(code, n=1, w=420):
    return b64(igpath(code, n), w, q_=80)


def png_tint(rel, color, w=900):
    im = Image.open(ROOT / rel).convert('RGBA')
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    if color:
        solid = Image.new('RGBA', im.size, color); solid.putalpha(im.getchannel('A')); im = solid
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def font(n):
    return 'data:font/woff2;base64,' + base64.b64encode((ROOT / 'assets/fonts' / f'{n}.woff2').read_bytes()).decode()


# ---------------------------------------------------------------- piezas
def fig(src, cap='', style='', cls='', capfirst=False):
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    cls += " capfirst" if capfirst else ""
    return f'<figure class="sf {cls}" style="{style}">{c if capfirst else ""}<img src="{src}" alt="">{"" if capfirst else c}</figure>'


def bk(title, body, cls=''):
    return f'<section class="bk {cls}"><h4>{title}</h4>{body}</section>'


def P(t, cls=''):
    return f'<p class="{cls}">{t}</p>'


def th(code, cap, n=1, cls=''):
    return f'<figure class="th {cls}"><img src="{igimg(code, n)}" alt=""><figcaption>{cap}<br><span>{fecha(code)}</span></figcaption></figure>'


RECORRIDO = ['La espera', 'Portada', 'Manifiesto', 'Ramos', 'Esmeralda 198', 'Comienza con una idea', 'Ocasiones', 'Del jardín', 'Visítanos']


def rec(cur):
    li = ''.join(f'<li class="{"on" if r == cur else ""}">{E(r)}</li>' for r in RECORRIDO)
    return f'<div class="rec"><p class="lab">Lugar en el recorrido</p><ol>{li}</ol></div>'


def head(kick, title, lead=''):
    return f'<p class="kick">{kick}</p><h2>{title}</h2>' + (f'<p class="lead">{lead}</p>' if lead else '')


SHEETS = []


def sheet(n, lcol, rcol, lform, rform, left, right, lab_left='El sitio'):
    lk = 'on-dark' if lcol in DARK else ''
    rk = 'on-dark' if rcol in DARK else ''
    SHEETS.append(dict(n=n, lcol=lcol, rcol=rcol, left=lform, right=rform))
    return f'''
<article class="lam s{n:02d}" style="--l:{lcol};--r:{rcol}">
  <section class="half L {lk}"><p class="lab">{lab_left}</p>{left}</section>
  <section class="half R {rk}">{right}
    <footer class="foot"><span>Floresta · Decisiones de diseño del sitio</span><span class="folio">{n:02d}</span></footer></section>
</article>'''


LOGO_INK = png_tint('dossier/png/logotipo.png', B_)
PAGES = []

# ============================================================ 01 · Portada
PAGES.append(sheet(1, B_, R_, 'C', 'Portada',
  fig(d('d-hero', right=1975, bottom=1340), 'Portada · florestachiloe.vercel.app', 'left:.55in;right:.55in;top:50%;transform:translateY(-50%)'),
  f'''<div class="cover">
      <img class="logo" src="{LOGO_INK}" alt="Floresta">
      <p class="sub">Decisiones de diseño del sitio web</p>
      <h1>De tu Instagram<br><em>a tu sitio</em></h1>
      <p class="for">Preparado para Natalia</p>
      <p class="meta">Esmeralda 198 · Castro, Chiloé · octubre 2026<br><a href="https://{URL}">{URL}</a></p></div>'''))

# ============================================================ 02 · Carta
PAGES.append(sheet(2, F_, W_, 'P', 'K · carta',
  fig(m('m-cont'), 'Tu florería · en el celular', 'left:50%;width:2.3in;top:50%;transform:translate(-50%,-50%)'),
  head('Antes de empezar', 'Un sitio hecho con lo que tú ya dijiste') + '''
    <div class="letter">
      <p>Natalia:</p>
      <p>Este sitio nació de mirar con atención lo que Floresta ya publica. No hay frases inventadas: cada título y cada párrafo sale de tus publicaciones de Instagram, de tus piezas gráficas o de lo que tus clientes escribieron en Google. Lo que hicimos fue ordenarlo, darle aire y ponerlo en movimiento.</p>
      <p>Tampoco hay fotos de banco de imágenes. Todas las fotos y los videos son de Floresta y de Almácigos Chiloé, tal como los publicaste. Los colores y el ramo del logo salen de tus propias piezas, y la letra se eligió para acompañarlas.</p>
      <p>Este documento explica, sección por sección, qué se decidió y por qué. En cada lámina, a la izquierda está la sección tal como se ve en el sitio. A la derecha, de dónde salió cada texto e imagen, qué letra y qué color se usó, cómo se compuso y por qué va en ese lugar del recorrido.</p>
      <p>Es un regalo. Ojalá lo disfrutes tanto como nosotros disfrutamos haciéndolo.</p>
      <p class="sign">Pablo Figueroa<br><span>Director de estudio</span></p>
    </div>'''))

# ============================================================ 03 · De dónde viene todo
n_pub = len(FL); n_fot = len(glob.glob(str(RAW / 'fotos/*.jpg'))); n_vid = len(glob.glob(str(RAW / 'videos/*.mp4')))
assert (n_pub, n_fot, n_vid) == (658, 879, 110)
grid_codes = ['DdAPKv2hBR3', 'DJSxjSCAghA', 'DZsd-uBBSK0', 'DPZAK2UAGz6', 'DKLZLxAgLsj', 'DdC3QVghbB3', 'DKQhQDfAplW', 'DXeWb3oFuvG', 'DQUMiXogMXv', 'Dc4DvMFhMoP']
mosaic = ''.join(f'<img src="{igimg(c, 1, 260)}" alt="">' for c in grid_codes)
piezas = ''.join(f'<img src="{igimg(c, k, 260)}" alt="">' for c, k in [('DX69F30lsj8', 3), ('DX69F30lsj8', 2), ('DX69F30lsj8', 1), ('DdSsnKwgGa6', 1)])
PAGES.append(sheet(3, W_, L_, 'E', 'M · mosaico de fuentes',
  fig(d('d-cinta', top=160, bottom=830, left=70, right=1975), 'Tus ramos, uno detrás de otro · en el computador', 'left:0;width:5.3in;top:3.2in', 'line edge'),
  head('Materia prima', 'De dónde viene todo', 'Antes de diseñar, reunimos todo lo que Floresta ya había publicado y lo ordenamos: ramos, la fachada, el mesón, el vivero, las ocasiones y las piezas gráficas.')
  + f'''<div class="mos"><div><p class="lab">Algunas de tus fotos · Instagram @florestaenchiloe</p><div class="mgrid">{mosaic}</div></div>
       <div><p class="lab">Tus piezas gráficas</p><div class="pgrid">{piezas}</div></div></div>
    <div class="cols2">
      {bk('Instagram @florestaenchiloe', P(f'<b>{n_pub} publicaciones</b>, con sus textos completos, <b>{n_fot} fotos</b> y <b>{n_vid} videos</b>. De ahí salen los títulos, los párrafos y casi todas las imágenes del sitio.'))}
      {bk('Piezas gráficas', P('El catálogo del Día de la Madre 2026, la pieza “Debes saber…” y el Día de las Flores Amarillas. De ahí salen los precios de referencia y las notas prácticas.'))}
      {bk('Instagram @almacigoschiloe', P('De sus publicaciones, el sitio usa <b>6</b>: 3 de fotos, 2 de video y una frase, para presentar a Almácigos Chiloé con su propio material.'))}
      {bk('Google', P('<b>5,0 en 6 reseñas.</b> Dos de ellas se citan en el sitio tal como fueron escritas, con su ortografía.'))}
      {bk('La regla', P('Cada texto del sitio tiene su origen identificado: qué publicación, qué pieza o qué reseña. Lo único escrito para el sitio son las indicaciones de uso: los botones, el formulario del pedido y la ayuda del mapa.'), 'wide')}
    </div>'''))

# ============================================================ 04 · La voz
PAGES.append(sheet(4, L_, R_, 'A', 'Q · cita grande',
  fig(d('d-nati', left=1010, top=290, bottom=1060, right=1800, w=1100), 'Tus palabras, en tu historia · en el computador', 'left:.55in;width:4.75in;bottom:0', capfirst=True),
  head('Sistema · voz', 'Escribir como Floresta', 'El sitio no agrega adjetivos ni promesas: escribe con la voz que Floresta ya construyó, cálida y cercana, y pone cada frase en el lugar justo.')
  + q('DMppRews63d', 'Mientras más silvestre… ¡mejor!', 'big')
  + f'''<div class="cols2">
      {bk('Una firma propia', q('DMIK3D4Apyi', 'Silvestre. Elegante. Es Floresta.') + P('El lema con que firmas tus ramos abre el sitio, sobre las fotos de la portada.'))}
      {bk('El oficio, contado de cerca', q('DaBGf9WByJu', 'Cada ramo que sale de nuestra florería comienza mucho antes de elegir las flores.'))}
      {bk('Un vocabulario propio', P('Silvestre, soñado, ramito, detalles, con cariño. Y el nombre completo cuando corresponde: <b>Floresta by Almácigos Chiloé</b>, que une la florería con el vivero de Pidpid.'))}
      {bk('Cerca, como en el mesón', q('DMMDzwHgpZN', 'Cariños para todos!') + P('Los cierres afectuosos de tus publicaciones se mantienen tal cual, con sus signos.'))}
      {bk('Para todas las ocasiones', P('La misma voz que celebra un cumpleaños acompaña una despedida, con respeto. El sitio mantiene ese tono en cada sección.'), 'wide')}
    </div>'''))

# ============================================================ 05 · Las letras
PAGES.append(sheet(5, B_, W_, 'C', 'E · muestras de letra',
  fig(d('d-resenas'), 'Visítanos · tus reseñas en Fraunces y Figtree', 'left:.55in;right:.55in;top:50%;transform:translateY(-50%)'),
  head('Sistema · tipografía', 'Una letra con curvas de pétalo', 'En tus piezas impresas, los títulos de Floresta van en una letra manuscrita. En el sitio se leen en pantallas pequeñas y mientras la página se mueve, así que los títulos usan una letra elegante y con personalidad, pero que se lee al instante.')
  + f'''<div class="spec">
      <div><p class="sp1">Silvestre. <em>Elegante.</em> Es Floresta.</p><p class="cap">Fraunces · títulos y frases de la marca</p>
      <p class="sp2">De esas que tienen aroma, textura, movimiento y vida.</p><p class="cap">Figtree · bajadas, párrafos y botones</p>
      <p class="sp3">ESMERALDA 198 · CASTRO</p><p class="cap">Figtree en mayúsculas pequeñas y espaciadas · rótulos</p></div>
      <figure class="th spth"><img src="{b64(igpath('DX69F30lsj8', 3), 500, crop=(0, 0, 1440, 560))}" alt=""><figcaption>La letra manuscrita de tu catálogo<br><span>{ig('DX69F30lsj8')}</span></figcaption></figure>
    </div>
    <div class="cols2">
      {bk('Fraunces · títulos', P('Una letra con remates de curvas blandas, casi orgánicas, emparentada con los remates del logotipo FLORESTA. Su cursiva destaca la palabra que importa: en frambuesa en los títulos, y en rosa claro sobre las fotos de la portada, como en el lema: <i>Elegante.</i>'))}
      {bk('Figtree · lectura', P('Una letra sin remates, redonda y cálida, que se lee con comodidad en el celular. Va en las bajadas, los párrafos, los precios y los botones, y en letra liviana bajo cada publicación.'))}
      {bk('Tamaños', P('Pocos tamaños y bien contrastados: el logo, enorme; los títulos, grandes y serenos; los párrafos, cómodos y con espacio entre líneas; los rótulos, pequeños y espaciados.'))}
      {bk('Primero, que se lea', P('Antes de lo bonito, lo útil: un precio, un horario o una dirección se leen sin esfuerzo, incluso con sol sobre la pantalla. Y las letras viajan con el propio sitio, así que el texto nunca cambia de forma mientras se lee.'))}
    </div>'''))

# ============================================================ 06 · Los colores
SW = [('Blanco rosado', W_), ('Rosa empolvado', R_), ('Lila', L_), ('Eucalipto claro', EC), ('Frambuesa', F_), ('Eucalipto', EU), ('Berenjena', B_)]
pal = [('DRFHHhKkdYz', 'Papel rosado'), ('DJvWKLcgAc9', 'Flores moradas'), ('DaGBcNkg4xT', 'Lisianthus'), ('DZsd-uBBSK0', 'La fachada')]
PAGES.append(sheet(6, R_, L_, 'R', 'S · muestras de color',
  '<div class="row4">' + ''.join(fig(m(x, 420), '', cls='st line') for x in ('m-ramos', 'm-alm', 'm-foot')) + '</div><p class="rowcap">Berenjena, eucalipto claro y frambuesa · en el celular</p>',
  head('Sistema · color', 'La paleta está en tus ramos', 'Los colores salen de lo que más se repite en las fotos de Floresta: el papel rosado de los ramos, las flores fucsia y moradas, los lisianthus y el verde de la fachada y de las hojas.')
  + '<div class="sws">' + ''.join(f'<div class="sw"><i style="background:{c}"></i><b>{nm}</b><code>{c}</code></div>' for nm, c in SW) + '</div>'
  + '<p class="lab thl">De estas fotos de tu Instagram salen los colores</p><div class="ths4">' + ''.join(th(c, cap) for c, cap in pal) + '</div>'
  + f'''<div class="cols2">
      {bk('Claros, para respirar', P('Blanco rosado y rosa empolvado son el fondo de la mayoría de las secciones; el lila acompaña las notas prácticas. Dejan que las flores pongan el color.'))}
      {bk('Fuertes, para marcar', P('Dos secciones van en berenjena (los ramos y la historia) y el pie en frambuesa. Así cada cambio de color marca un capítulo y ninguna sección se pierde entre las otras.'))}
      {bk('El verde, con medida', P('El verde de la fachada y de tus piezas aparece en una sola sección grande, Del jardín, y en pequeños detalles. Ocupa menos de un cuarto de la página, para que las flores sean las protagonistas.'))}
      {bk('Contraste', P('Cada combinación de texto y fondo se lee con holgura, incluso con poca vista o con el sol sobre la pantalla.'))}
    </div>'''))

# ============================================================ 07 · El logo
tiles = [(W_, png_tint('dossier/png/isotipo.png', None, 400), 'iso'), (B_, png_tint('dossier/png/isotipo.png', W_, 400), 'iso'),
         (W_, png_tint('dossier/png/logotipo.png', B_, 1000), 'wide'), (R_, png_tint('dossier/png/firma.png', None, 800), 'firma'),
         (W_, png_tint('assets/icons/icon-192.png', None, 192), 'ico')]
PAGES.append(sheet(7, W_, F_, 'A', 'G · logo y bloques',
  fig(d('d-foot', top=200, left=345, right=1815), 'El pie de tu sitio: el logotipo y la firma', 'left:0;right:0;bottom:0', capfirst=True, cls='capin line'),
  head('Sistema · logo', 'El ramo del letrero', 'El logotipo FLORESTA y el ramo del letrero de Esmeralda 198 se redibujaron siguiendo sus trazos originales, para que se vean nítidos a cualquier tamaño, desde el pequeño ícono que acompaña el nombre del sitio hasta un letrero.')
  + '<div class="tiles">' + ''.join(f'<div class="tile {k}" style="background:{c}"><img src="{s}" alt=""></div>' for c, s, k in tiles) + '</div>'
  + f'''<div class="cols2">
      {bk('Trazos respetados', P('Las letras del logotipo conservan sus remates y la A con su curva. El ramo mantiene sus flores coral, sus hojas y el lazo.'))}
      {bk('Variantes', P('El ramo en color y en claro, el logotipo en berenjena y en blanco, y la firma “by Almácigos Chiloé” para el pie.'))}
      {bk('En miniatura', P('El ramo solo, sin fondo, con trazos más firmes para que se reconozca aun muy pequeño, junto al nombre del sitio. Sobre fondo oscuro, las hojas pasan a claro.'))}
      {bk('Dónde aparece', P('El ramo se dibuja en la espera antes de entrar. El logotipo encabeza la portada a gran escala, vive en la barra superior y cierra el pie con la firma completa.'))}
    </div>'''))

# ============================================================ 08 · El recorrido
strip = [('d-loader', 'La espera', {}), ('d-hero', 'Portada', dict(right=1975, bottom=1340)), ('d-cont', 'Manifiesto', {}),
         ('d-ramos', 'Ramos', {}), ('d-esm', 'Esmeralda 198', dict(top=150)), ('d-hist', 'Comienza con una idea', {}),
         ('d-ocas', 'Ocasiones', dict(bottom=910)), ('d-jardin', 'Del jardín', {}), ('d-visita-prod', 'Visítanos', dict(top=165, bottom=770, right=1420))]
PAGES.append(sheet(8, L_, W_, 'G', 'N · pasos numerados',
  '<div class="g9">' + ''.join(f'<figure><img src="{d(s, 520, **kw)}" alt=""><figcaption>{i + 1} · {c}</figcaption></figure>' for i, (s, c, kw) in enumerate(strip)) + '</div><p class="rowcap">El recorrido completo, de arriba hacia abajo · en el computador</p>',
  head('Sistema · recorrido', 'Del ramo a la puerta de la florería', 'El orden de la página no es una lista de servicios: es una visita que empieza con un ramo en la mano y termina en Esmeralda 198.')
  + f'''<div class="steps">
      {bk('<span>1</span>Llegar', P('Tres ramos a pantalla completa y el lema. Luego, el manifiesto con tus propias palabras y una cinta de ramos que no se detiene.'))}
      {bk('<span>2</span>Elegir', P('El catálogo con precios de referencia y la opción de armar el pedido ahí mismo. Lo concreto aparece temprano, para quien ya sabe lo que busca.'))}
      {bk('<span>3</span>Conocer', P('Esmeralda 198 y sus once ramos, tu historia en video, las ocasiones y el vivero de Almácigos Chiloé.'))}
      {bk('<span>4</span>Venir', P('El mapa con el punto exacto, lo que dicen tus clientes y las notas prácticas para pedir. Recién al final, cuando ya se decidió.'))}
    </div>
    {bk('Ritmo', P('Se alternan secciones claras de lectura con dos secciones oscuras y un pie frambuesa, como respirar. Ninguna composición se repite dos veces seguidas: una fila que se desliza, un mazo, videos, franjas, fichas.'), 'solo')}'''))

# ============================================================ 09 · La espera antes de entrar
PAGES.append(sheet(9, R_, L_, 'C', 'G · dos columnas',
  fig(d('d-loader'), 'La espera, mientras el porcentaje avanza', 'left:.55in;right:.55in;top:1.5in', 'line') + rec('La espera'),
  head('01 · La espera antes de entrar', 'Floresta · Esmeralda 198', 'Antes de entrar, el sitio deja listo lo que se ve primero. Mientras tanto se dibuja el ramo del logo y un porcentaje muestra cuánto falta. Debajo, el nombre y la dirección.')
  + f'''<div class="cols2 airy">
      {bk('Qué se ve', P('El ramo se dibuja de abajo hacia arriba, como si creciera desde el lazo, y debajo avanza el porcentaje. Al llegar a cien, la pantalla sube como una cortina y aparece la portada.'))}
      {bk('Qué se deja listo', P('Las letras, las tres fotos de la portada, las fotos del manifiesto, la cinta de ramos y la primera imagen de los cuatro videos de tu historia. Así nada aparece borroso ni a medias.'))}
      {bk('Tiempos', P('El porcentaje tarda al menos un segundo y medio en llegar a cien, aunque la conexión sea rápida. Si la conexión es lenta, a los seis segundos deja de esperar y abre igual. Los videos siguen llegando solos, en el orden de la página, para que ya estén corriendo cuando se llega a ellos.'))}
      {bk('Por qué así', P('Floresta es una marca de fotos y videos. Una espera breve y cuidada vale más que una página que aparece a saltos.'))}
    </div>'''))

# ============================================================ 10 · Portada del sitio
PAGES.append(sheet(10, F_, R_, 'D', 'I · fuentes al costado',
  fig(d('d-hero', right=1975, bottom=1340), 'En el computador', 'left:.55in;width:3.9in;top:1.15in')
  + fig(m('m-hero'), 'En el celular', 'right:.55in;width:1.35in;top:4.05in', 'capr') + rec('Portada'),
  head('02 · Portada', 'Silvestre. Elegante. Es Floresta.', 'Tres ramos a pantalla completa, sostenidos en la mano, se turnan cada pocos segundos: dos frente a la fachada verde y coral, y uno dentro de la florería. Encima, solo el logotipo y el lema, al centro.')
  + f'''<div class="side">
      <div class="thcol"><p class="lab">En tu Instagram</p>{th('DdAPKv2hBR3', 'Rosas rojas')}{th('DdC3QVghbB3', 'Tú y un ramo gigante')}{th('DaGBcNkg4xT', 'Rosas y lisianthus')}</div>
      <div class="blocks">
        {bk('Textos', q('DMIK3D4Apyi', 'Silvestre. Elegante. Es Floresta.') + P('El lema es la única frase de la portada. Su cursiva va en rosa claro, para leerse sobre la foto. No hay botones: “Pedido” está arriba, a mano.'))}
        {bk('Imágenes', P('Las tres fotos son tuyas, del Instagram de Floresta: dos ramos en la mano frente a la fachada verde y coral, y tú con un ramo gigante dentro de la florería.'))}
        {bk('Movimiento', P('Al abrir, la foto se expande desde un marco de esquinas suaves hasta llenar la pantalla y el logotipo emerge desde abajo. Cada ramo cede su lugar al siguiente con una cortina suave; los puntos de abajo se van llenando. En celular se cambia de ramo deslizando el dedo.'))}
        {bk('Por qué así', P('Así es como Floresta muestra sus ramos en Instagram: en la mano, y casi siempre frente a la florería. La primera imagen ya dice qué es y dónde está.'))}
      </div></div>'''))

# ============================================================ 11 · Manifiesto
PAGES.append(sheet(11, W_, L_, 'E', 'Q · cita grande',
  fig(d('d-cont'), 'Manifiesto y cinta de ramos · en el computador', 'left:0;width:5.3in;top:1.55in', 'line edge') + rec('Manifiesto'),
  head('03 · Manifiesto', 'Ramos con alma', 'Una pausa clara después de la portada: tu manifiesto a la izquierda y tus ramos frente al letrero, a la derecha. Debajo, una cinta de ramos que corre sola.')
  + q('DLUq_50AvEX', 'En Floresta no hacemos “arreglos”, hacemos ramos con alma.', 'big')
  + f'''<div class="cols2">
      {bk('Textos', q('DLUq_50AvEX', 'Nuestros diseños tienen un estilo único: más natural, más libre, más sureño.') + q('DMppRews63d', 'Mientras más silvestre… ¡mejor!'))}
      {bk('Imágenes · tu Instagram', '<div class="ths3">' + th('DZsd-uBBSK0', 'Frente al letrero') + th('DXeWb3oFuvG', 'Rosas bicolor') + th('DJSxjSCAghA', 'Girasoles e iris') + '</div>' + P('Y unos tulipanes, del ' + fecha('DPZAK2UAGz6') + '.', 'small'))}
      {bk('Composición', P('La foto grande se sale por el borde derecho, con esquinas suaves y aire respecto de la portada. Una segunda foto se monta sobre ella, más pequeña. Ninguna foto va encerrada en formas: se muestran libres, como en tus publicaciones.'))}
      {bk('Movimiento', P('Las fotos flotan a distinta profundidad al recorrer la página. La cinta de ocho ramos corre sola, se calma al pasar por encima y se inclina levemente al bajar rápido. Al pasar sobre ella aparece “Ver ramos”.'))}
    </div>'''))

# ============================================================ 12 · Ramos
precios = [('Ramos Silvestres', 'Pequeño · Mediano · Grande', '$15.000 · $33.000 · $49.000'),
           ('Rosas Rojas', '5 · 10 · 20 rosas', '$21.000 · $39.000 · $79.000'),
           ('Ramos de Girasoles', '3 · 5 · 10 girasoles', '$14.000 · $22.000 · $40.000'),
           ('Rosas y Girasoles', '5 · 10 · 20 flores', '$21.000 · $39.000 · $79.000'),
           ('En la tienda', 'Opciones listas para llevar', 'desde $5.000')]
PAGES.append(sheet(12, L_, R_, 'D', 'P · lista de precios',
  fig(d('d-ramos'), 'En el computador', 'left:.55in;width:3.9in;top:1.15in')
  + fig(m('m-ramos'), 'En el celular', 'right:.55in;width:1.5in;top:3.75in', 'capr') + rec('Ramos'),
  head('04 · Ramos', 'Regala flores. Flores de verdad.', 'Tu catálogo, con precios de referencia, en una fila de fichas que se arrastra con la mano. Es la primera sección de fondo oscuro, para que el producto resalte.')
  + '<div class="prices"><p class="lab">Precios de referencia</p>' + ''.join(f'<div class="pr"><b>{a}</b><span>{b}</span><span class="v">{c}</span></div>' for a, b, c in precios)
  + f'<p class="psrc">Catálogo Día de la Madre 2026 · {ig("DX69F30lsj8")}. Cada foto lleva “* Ramo de referencia”, como en el catálogo.</p></div>'
  + f'''<div class="cols3">
      {bk('Textos', q('DdSsnKwgGa6', '…regala flores. Flores de verdad.') + q('DdSsnKwgGa6', 'De esas que tienen aroma, textura, movimiento y vida.') + P('Los nombres, las descripciones y las notas de cada ramo vienen del catálogo, al pie de la letra.'))}
      {bk('Interacción', P('Al elegir un tamaño, el precio rueda al nuevo valor. Al tocar “Agregar”, saltan pétalos de colores y el ramo, en miniatura, vuela hasta “Pedido”. Las fichas se inclinan levemente hacia donde se apunta.'))}
      {bk('Por qué así', P('Quien llega buscando un ramo encuentra precio y tamaño sin preguntar. El pedido se arma ahí mismo y se envía por WhatsApp, que es como Floresta ya recibe sus pedidos.'))}
    </div>'''))

# ============================================================ 13 · Esmeralda 198
PAGES.append(sheet(13, F_, W_, 'H', 'Q · cita grande',
  fig(d('d-esm', top=150), 'Esmeralda 198 · el mazo de once ramos', 'left:.55in;width:4.2in;top:1.05in')
  + fig(d('d-invierno'), 'La frase de invierno, sobre tus girasoles', 'right:.55in;width:4.2in;top:3.95in') + rec('Esmeralda 198'),
  head('05 · Esmeralda 198', 'Nunca son idénticas', 'Once ramos fotografiados frente al mismo letrero, en un mazo que se puede tomar y lanzar con la mano. Cierra con la frase de invierno a pantalla completa, sobre un ramo de girasoles y con una segunda línea más pequeña.')
  + q('DZPs-SVtb-s', '…las flores son como la naturaleza: nunca son idénticas.', 'big')
  + f'''<div class="cols2">
      {bk('Textos', q('DZPs-SVtb-s', 'Podemos inspirarnos en un diseño, mantener su esencia y estilo, pero cada ramo será siempre único y especial.') + q('DavQtc1Bg0w', 'Aunque estemos en pleno invierno en Chiloé, para nosotros todos los días son primavera.'))}
      {bk('Imágenes · tu Instagram', '<div class="ths3">' + ''.join(th(c, 'Frente al letrero') for c in ('DRFHHhKkdYz', 'DV8ZZI9gCgv', 'DcBdWxFBuC7')) + '</div>' + P('Once publicaciones distintas, todas frente al letrero de Esmeralda 198, alineadas para que el letrero quede siempre en el mismo lugar.', 'small'))}
      {bk('Interacción', P('El ramo de arriba se arrastra y, si se suelta con fuerza, sale volando y vuelve a entrar por debajo del mazo. Al pasar por encima, los ramos se abren en abanico. “Otro ramo” permite recorrerlos sin arrastrar, y el contador indica en cuál vas.'))}
      {bk('Por qué aquí', P('Es la prueba visual de la frase: el mismo letrero, once ramos distintos. Después del catálogo, muestra que cada ramo es único.'))}
    </div>'''))

# ============================================================ 14 · Comienza con una idea
PAGES.append(sheet(14, R_, L_, 'D', 'I · fuentes al costado',
  fig(d('d-hist'), 'Tus cuatro videos · en el computador', 'left:.55in;width:3.9in;top:1.15in')
  + fig(m('m-hist'), 'En el celular', 'right:.55in;width:1.45in;top:3.85in', 'capr') + rec('Comienza con una idea'),
  head('06 · Comienza con una idea', 'Comienza <em>con una idea</em>', 'La sección de la persona detrás de los ramos, en fondo berenjena: cuatro videos de distintas publicaciones y, debajo, tú, con tus propias palabras.')
  + f'''<div class="side">
      <div class="thcol two"><p class="lab">En tu Instagram</p>{th('DWh0WXdgKi1', 'El mesón')}{th('Dal1L2VhFpw', 'Un ratito en la florería')}{th('DWgtaCRAPFB', 'Ramos listos')}{th('DTonzAXgLkC', 'Matrimonio al aire libre')}</div>
      <div class="blocks">
        {bk('Textos', q('DaBGf9WByJu', 'Cada ramo que sale de nuestra florería comienza mucho antes de elegir las flores. Comienza con una idea, con una historia y con la intención de emocionar a quien lo recibe.') + q('DJiZA6bgtDm', 'Mi destino siempre fueron las plantas y las flores!'))}
        {bk('Composición', P('Cuatro videos verticales a distintas alturas, con mucho aire entre ellos, que flotan a distinta velocidad al bajar. Bajo cada uno, una frase de tus publicaciones, en letra liviana. En celular se recorren deslizando.'))}
        {bk('Por qué aquí', P('Después de ver el producto, la visita conoce a quien lo hace. Son cuatro momentos distintos: el oficio en el mesón, un día en la florería, los ramos listos y un matrimonio en el campo.'))}
      </div></div>'''))

# ============================================================ 15 · Ocasiones
serv = ['Ramos personalizados', 'Arreglos florales para toda ocasión', 'Regalos y detalles', 'Condolencias y coronas', 'Despachos en Castro y alrededores']
PAGES.append(sheet(15, B_, R_, 'P', 'N · lista numerada',
  fig(m('m-ocas'), 'Ocasiones · en el celular', 'left:50%;width:2.2in;top:1.2in;transform:translateX(-50%)') + rec('Ocasiones'),
  head('07 · Ocasiones', 'Para celebrar, agradecer, acompañar o despedir', 'Cinco franjas verticales, una por ocasión. La elegida se abre, corre su video o aparece su foto, y se lee su frase; las demás se angostan.')
  + '<ol class="nl5">' + ''.join(f'<li><span>0{i + 1}</span>{lit("DcfGCrWhf9E", s)}</li>' for i, s in enumerate(serv)) + f'</ol><p class="src acc">Los cinco nombres vienen de una misma publicación · {ig("DcfGCrWhf9E")}</p>'
  + f'''<div class="cols2">
      {bk('Textos', q('Da05yhvBxvM', 'Una corona floral no es solo un gesto; es una forma de acompañar, honrar y expresar lo que muchas veces las palabras no alcanzan a decir.'))}
      {bk('Videos e imágenes · tu Instagram', '<div class="ths3">' + th('DXVVyQqhF3D', 'Hecho a medida') + th('DN1tVVeQADZ', 'Carterita') + th('Da05yhvBxvM', 'Corona') + '</div>' + P('Además, un matrimonio del ' + fecha('DUQUsMqAHoR') + '.', 'small'))}
      {bk('Interacción', P('En computador, la franja se abre al pasar por encima; en celular, al tocarla, y se abre hacia abajo. Solo corre el video de la franja abierta, para que la página se mantenga liviana.'))}
      {bk('Por qué así', P('Floresta hace mucho más que ramos, y cada ocasión tiene su tono. Mostrarlas una a la vez da espacio a cada una, incluida la despedida, con el mismo respeto con que Floresta la nombra.'))}
    </div>'''))

# ============================================================ 16 · Del jardín
PAGES.append(sheet(16, L_, W_, 'H', 'I · fuentes al costado',
  fig(d('d-jardin'), 'Del jardín a la florería', 'left:.55in;width:4.2in;top:1.05in')
  + fig(d('d-alm'), 'El vivero, con su propio Instagram', 'right:.55in;width:4.2in;top:4.0in') + rec('Del jardín'),
  head('08 · Del jardín', 'Del jardín <em>a la florería</em>', 'La única sección de fondo verde. Primero, los Helleborus cosechados en el vivero. Después, Almácigos Chiloé presentado con fotos y videos de su propio Instagram.')
  + f'''<div class="side">
      <div class="thcol"><p class="lab">Almácigos Chiloé</p>{th('DTiL9X9ETwm', 'Dalias')}{th('DQobKvtkX2k', 'Rododendro')}{th('DQFsU65jVtf', 'Rododendro', 2)}</div>
      <div class="blocks">
        {bk('Textos', q('DJ-mvELNwQx', 'Almácigos Chiloé ya no es solo un vivero de plantas… ¡ahora también somos flores, diseño y emociones!') + q('DXK7qcBERv1', 'Hay lugares que invitan a detenerse, respirar y reconectar… este es uno de ellos'))}
        {bk('Imágenes del vivero', P('Las fotos son del Instagram de Almácigos Chiloé. Además, dos videos del vivero: un campo de dalias y un recorrido con los pavos reales.'))}
        {bk('Interacción', P('Las fotos y videos del vivero se deslizan en una fila. Bajo cada uno va la frase con que abre su publicación y un enlace pequeño, “Ver publicación”, que la abre en Instagram. Arriba, “Conocer @almacigoschiloe” lleva al perfil del vivero.'))}
        {bk('Por qué aquí', P('Floresta es “by Almácigos Chiloé”. Esta sección deja que la florería presente al vivero con su propio material, y abre la puerta para conocerlo en Pidpid.'))}
      </div></div>'''))

# ============================================================ 17 · Visítanos
PAGES.append(sheet(17, F_, L_, 'D', 'Q · cita grande',
  fig(d('d-visita-prod', top=165, bottom=770, right=1420), 'Con el mapa real · en el computador', 'left:.55in;width:3.9in;top:1.15in')
  + fig(m('m-visita'), 'En el celular', 'right:.55in;width:1.55in;top:3.55in', 'capr') + rec('Visítanos'),
  head('09 · Visítanos', '¿Buscas flores en Castro? <em>Las encontraste.</em>', 'El cierre práctico: dónde está, cuándo abre y cómo pedir. Debajo, lo que dicen tus clientes y las notas que conviene saber antes de encargar.')
  + qg('Fantásticas, empáticas y amorosas !!! Y las flores bellas !!!', 'Tamara D.', 'big')
  + f'''<div class="cols2">
      {bk('Datos', P('Esmeralda 198, Castro, Chiloé · Lunes a sábado, 10:00 a 19:30 hrs · WhatsApp +56 9 6483 8490. El horario es el que Floresta publica en Instagram.') + P('El mapa queda anclado al punto exacto de la florería, y “Volver a la florería” lo recentra.'))}
      {bk('Lo que dicen', qg('Me encantó el lugar. Hermoso y bien decorado. Los mejores ramos de la ciudad de castro y además en un lugar cómodo y céntrico', 'Ignacio M.') + P('Las reseñas se citan tal como fueron escritas, con su ortografía.', 'small'))}
      {bk('Debes saber…', P(f'Las cinco notas de tu pieza “Debes saber…” ({ig("DX69F30lsj8")}): ramos silvestres, reservas, despacho, horario de despacho y qué incluye cada ramo. Cada nota se abre al tocarla, para no recargar la vista.'))}
      {bk('Por qué al final', P(f'Lo práctico llega cuando la visita ya decidió. El título es la frase con que Floresta invita en Instagram ({fecha("DcfGCrWhf9E")}), y la nota 5,0 de Google habla por sí sola.'))}
    </div>'''))
lit('DcfGCrWhf9E', '¿BUSCAS FLORES EN CASTRO? LAS ENCONTRASTE.')

# ============================================================ 18 · Detalles
PAGES.append(sheet(18, R_, W_, 'A', 'G · dos columnas',
  fig(b64(SH2 / 'd-cart.jpg', 900, crop=(1420, 20, 2160, 1350)), 'El pedido, listo para enviar por WhatsApp', 'left:50%;width:2.6in;bottom:0;transform:translateX(-50%)', capfirst=True),
  head('Detalles en todo el sitio', 'Lo que no se ve, <em>pero se siente</em>', 'Pequeñas decisiones que no se notan una por una, pero que hacen que el sitio se sienta cuidado de principio a fin.')
  + f'''<div class="cols2 airy">
      {bk('Pedido', P('Los ramos elegidos se juntan en “Pedido” y se envían por WhatsApp con el mensaje ya escrito. Con “Retiro en tienda” se pide la fecha; con “Despacho” se suman la dirección y las notas de despacho.'))}
      {bk('Menú', P('En celular, el menú se abre a pantalla completa en rosa empolvado. En computador, una marca de color se desliza hasta la sección en la que se está.'))}
      {bk('Movimiento con calma', P('Todo se mueve rápido, pero arranca y frena con suavidad. Quien tenga activada la opción de “reducir movimiento” en su equipo ve el sitio completo y quieto.'))}
      {bk('Pensado para el celular', P('Cada sección tiene su forma en el celular: filas que se deslizan con el dedo, franjas que se abren hacia abajo y el mapa que se mueve con dos dedos.'))}
      {bk('Sin saltos', P('La página no “brinca” mientras carga ni al bajar, y se ve igual de bien en un computador grande, una tableta o un celular.'))}
      {bk('Para todos', P('Textos que se leen bien, recorrido completo con el teclado y todas las imágenes descritas para quienes usan lectores de pantalla.'))}
    </div>'''))

# ============================================================ 19 · Lo que sigue + cierre
PAGES.append(sheet(19, L_, B_, 'P', 'T · lista y firma',
  fig(m('m-foot'), 'El pie de tu sitio · en el celular', 'left:50%;width:2.3in;top:50%;transform:translate(-50%,-50%)'),
  head('Lo que sigue', 'Hacerlo <em>tuyo</em>', 'Este sitio se hizo solo con lo que ya estaba publicado. Con un par de conversaciones podría ir mucho más lejos:')
  + '''<ul class="next">
      <li>Fotografía propia de los ramos de temporada, del taller y tuya</li>
      <li>Los contenidos que quieras contar, con tu voz</li>
      <li>Una dirección propia terminada en .cl, a nombre de Floresta</li>
      <li>Pedidos y pagos en línea, y despachos más fáciles de coordinar</li></ul>
    <div class="close">
      <p class="invite">Cuando quieras, lo conversamos.</p>
      <p class="who">Pablo Figueroa</p>
      <p class="role">Director de estudio</p>
      <p class="contact"><a href="mailto:pablo@bergerac.cl">pablo@bergerac.cl</a> · <a href="tel:+56975892096">+56 9 7589 2096</a></p>
      <p class="web"><a href="https://bergerac.cl">Bergerac.cl</a></p></div>'''))

CSS = f'''
@font-face{{font-family:"Fraunces";font-weight:100 900;src:url({font("fraunces-latin-full-normal")}) format("woff2")}}
@font-face{{font-family:"Fraunces";font-weight:100 900;font-style:italic;src:url({font("fraunces-latin-full-italic")}) format("woff2")}}
@font-face{{font-family:"Figtree";font-weight:300 900;src:url({font("figtree-latin-wght-normal")}) format("woff2")}}
@page{{size:13in 8.5in;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#ddd}}
body{{font-family:"Figtree",sans-serif;color:{B_};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
h1,h2,blockquote p,.sp1,.who,.invite,.name,.pr b,.nl5 li,.letter .sign,.steps h4 span,.for{{font-family:"Fraunces",serif;font-variation-settings:"SOFT" 100;font-weight:380}}
em,i,blockquote p,.invite,.for{{font-style:italic;font-variation-settings:"SOFT" 100,"WONK" 1}}
em{{font-family:"Fraunces",serif;color:{F_}}}
.on-dark em{{color:{R_}}}
.lam{{width:13in;height:8.5in;position:relative;overflow:hidden;break-after:page;page-break-after:always;margin:0 auto;display:grid;grid-template-columns:5.85in 7.15in}}
.half{{position:relative;height:8.5in;overflow:hidden}}
.L{{background:var(--l);padding:.55in}}
.R{{background:var(--r);padding:.55in .62in .55in .6in;display:flex;flex-direction:column}}
.on-dark{{color:{W_}}}
.lab{{font-size:7.5pt;font-weight:650;letter-spacing:.18em;text-transform:uppercase;color:{F_}}}
.on-dark .lab{{color:{R_}}}
.sf{{position:absolute;margin:0}} .sf img{{display:block;width:100%;height:auto}}
.sf figcaption,.rowcap{{font-size:8pt;letter-spacing:.03em;margin-top:6pt;opacity:.8}}
.sf.capfirst figcaption{{margin:0 0 6pt}}
.capin figcaption{{padding-left:.55in;margin:0 0 6pt}}
.capr figcaption{{text-align:right}}
.edge figcaption{{padding-left:.55in}}
.line img{{outline:1px solid rgba(47,34,56,.16);outline-offset:-1px}}
.kick{{font-size:7.5pt;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:{F_};margin-bottom:.1in}}
.on-dark .kick{{color:{R_}}}
h2{{font-size:25pt;line-height:1.06;letter-spacing:-.01em;margin-bottom:.1in}}
.lead{{font-size:11.5pt;line-height:1.42;max-width:5.9in;opacity:.85;margin-bottom:.2in}}
.foot{{margin-top:auto;padding-top:.12in;display:flex;justify-content:space-between;align-items:baseline;font-size:7.5pt;letter-spacing:.12em;text-transform:uppercase;opacity:.65}}
.folio{{font-family:"Fraunces",serif;font-size:11pt;letter-spacing:0;text-transform:none}}
.cols2{{display:grid;grid-template-columns:1fr 1fr;gap:.17in .32in;align-content:start}}
.cols2.roomy{{gap:.3in .4in;margin-top:.15in}}
.cols3{{display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:.17in .28in}}
.bk h4{{font-size:7.5pt;font-weight:700;letter-spacing:.16em;text-transform:uppercase;padding-bottom:3pt;border-bottom:.6pt solid rgba(47,34,56,.22);margin-bottom:5pt}}
.on-dark .bk h4{{border-color:rgba(255,251,250,.3)}}
.bk p{{font-size:9.5pt;line-height:1.4;margin-bottom:4pt}}
.bk p.small{{font-size:9pt;opacity:.8}}
.bk.wide{{grid-column:1/-1}}
.bk.solo{{margin-top:.2in;max-width:5.9in}}
.q{{margin:0 0 6pt}}
.q p{{font-size:10.5pt;line-height:1.3;margin-bottom:2pt}}
.q cite,.th figcaption span,.src{{display:block;font-style:normal;font-size:7.5pt;font-weight:650;letter-spacing:.1em;text-transform:uppercase;color:{F_}}}
.on-dark .q cite,.on-dark .src{{color:{R_}}}
.big{{margin:0 0 .2in}}
.big p{{font-size:22pt;line-height:1.12;margin-bottom:4pt;max-width:5.9in}}
.big cite{{display:block;font-style:normal;font-size:7.5pt;font-weight:650;letter-spacing:.12em;text-transform:uppercase;color:{F_}}}
.th{{margin:0}} .th img{{display:block;width:100%;aspect-ratio:1;object-fit:cover}}
.th figcaption{{font-size:8pt;line-height:1.25;margin-top:3pt}}
.th figcaption span{{font-size:7.5pt;letter-spacing:.02em;font-weight:650;margin-top:1pt;white-space:nowrap;text-transform:none}}
.ths3{{display:grid;grid-template-columns:repeat(3,1fr);gap:.1in;margin-bottom:4pt}}
.ths3 figcaption{{font-size:8pt}}
.ths4{{display:grid;grid-template-columns:repeat(4,1fr);gap:.12in;margin-bottom:.18in}}
.ths4.tight{{gap:.07in;margin-bottom:4pt}}
.ths4.tight figcaption{{font-size:7.5pt}}
.ths4.tight figcaption span{{font-size:7pt;letter-spacing:0}}
.side{{display:grid;grid-template-columns:1.3in 1fr;gap:.32in;align-items:start}}
.thcol{{display:flex;flex-direction:column;gap:.14in}}
.thcol.two{{display:grid;grid-template-columns:1fr;gap:.1in}}
.thcol.two .th img{{aspect-ratio:4/5}}
.blocks{{display:grid;grid-template-columns:1fr 1fr;gap:.17in .3in;align-content:start}}
.blocks .bk:first-child{{grid-column:1/-1}}
.s14 .side{{grid-template-columns:2.45in 1fr}} .s14 .thcol.two{{grid-template-columns:1fr 1fr;gap:.12in}} .s14 .thcol.two .lab{{grid-column:1/-1}} .thl{{margin-bottom:5pt}} .s14 .blocks{{grid-template-columns:1fr}}
.s16 .th img{{aspect-ratio:4/3}} .s16 .thcol{{gap:.1in}}
.airy .bk p{{font-size:10.5pt;line-height:1.45}} .airy{{gap:.3in .4in!important;margin-top:.1in}}
/* recorrido */
.rec{{position:absolute;left:.55in;right:.55in;bottom:.5in}}
.rec ol{{list-style:none;display:grid;grid-template-columns:repeat(3,auto);justify-content:start;gap:2pt .28in;margin-top:5pt}}
.rec li{{font-size:8pt;font-weight:600;letter-spacing:.06em;opacity:.5}}
.rec li.on{{opacity:1;font-weight:800}}
.rec li.on::before{{content:"● ";color:{F_}}}
.on-dark .rec li.on::before{{color:{R_}}}
/* portada */
.cover{{margin:auto 0}}
.cover .logo{{width:2.4in;display:block;margin-bottom:.32in}}
.cover .sub{{font-size:9.5pt;font-weight:650;letter-spacing:.24em;text-transform:uppercase;margin-bottom:.2in}}
h1{{font-size:50pt;line-height:1.02;letter-spacing:-.01em}}
.cover .for{{font-size:17pt;color:{F_};margin-top:.35in}}
.cover .meta{{font-size:10pt;line-height:1.6;letter-spacing:.04em;margin-top:.14in;opacity:.8}}
/* carta */
.letter p{{font-size:11.5pt;line-height:1.55;margin-bottom:9pt;max-width:5.8in}}
.s02 h2{{margin-bottom:.25in}}
.letter .sign{{font-size:14pt;line-height:1.3;margin-top:.12in}}
.letter .sign span{{font-family:"Figtree",sans-serif;font-size:10pt}}
/* fuentes */
.mos{{display:grid;grid-template-columns:1fr auto;gap:.3in;margin-bottom:.22in}}
.mgrid{{display:grid;grid-template-columns:repeat(5,.6in);gap:4pt;margin-top:5pt}}
.mgrid img{{width:100%;aspect-ratio:1;object-fit:cover;display:block}}
.pgrid{{display:grid;grid-template-columns:repeat(2,.6in);gap:4pt;margin-top:5pt}}
.pgrid img{{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 0;display:block}}
/* letras */
.spec{{display:grid;grid-template-columns:1fr 1.55in;gap:.3in;align-items:start;margin-bottom:.22in;padding:.14in 0;border-top:.6pt solid rgba(47,34,56,.22);border-bottom:.6pt solid rgba(47,34,56,.22)}}
.sp1{{font-size:24pt;line-height:1.08}}
.sp2{{font-size:13pt;font-weight:450;line-height:1.3;margin-top:.12in}}
.sp3{{font-size:8.5pt;font-weight:700;letter-spacing:.22em;margin-top:.12in;color:{F_}}}
.spec .cap{{font-size:7.5pt;font-weight:600;letter-spacing:.12em;text-transform:uppercase;opacity:.7;margin-top:3pt}}
.spth img{{aspect-ratio:auto}}
/* colores */
.sws{{display:grid;grid-template-columns:repeat(7,1fr);gap:.06in;margin-bottom:.2in}}
.sw i{{display:block;height:.75in;box-shadow:inset 0 0 0 1px rgba(47,34,56,.14)}}
.sw b{{display:block;font-weight:650;font-size:8pt;line-height:1.2;margin-top:4pt;min-height:2.4em}}
.sw code{{font-family:"Figtree",sans-serif;font-size:7.5pt;opacity:.75}}
.row4{{position:absolute;left:.55in;right:.55in;top:2.35in;display:grid;grid-template-columns:repeat(3,1fr);gap:.25in;align-items:start}}
.row4 .sf{{position:static}}
.s06 .rowcap{{position:absolute;left:.55in;top:5.25in;width:4.75in}}
.s06 .th img{{aspect-ratio:3/2}}
.s06 .sws{{margin-bottom:.16in}} .s06 .sw i{{height:.6in}} .s06 .ths4{{margin-bottom:.14in}}
/* logo */
.tiles{{display:grid;grid-template-columns:1fr 1fr 2fr;grid-template-rows:.95in .95in;gap:.08in;margin-bottom:.22in}}
.tile{{display:grid;place-items:center;padding:.12in}}
.tile img{{max-width:100%;max-height:.72in;width:auto;height:auto;display:block}}
.tile.wide{{grid-column:3;grid-row:1}} .tile.wide img{{max-height:.36in}}
.tile.firma{{grid-column:3;grid-row:2}} .tile.firma img{{max-height:.6in}}
.tile.ico img{{max-height:.4in}}
.tile.iso:first-child{{grid-row:1/3}}
/* recorrido 3×3 */
.g9{{position:absolute;left:.55in;right:.55in;top:1.25in;display:grid;grid-template-columns:repeat(3,1fr);gap:.2in .16in;align-items:start}}
.g9 figure{{margin:0}} .g9 img{{display:block;width:100%;height:.86in;object-fit:contain;object-position:left top}}
.g9 figcaption{{font-size:8pt;font-weight:600;margin-top:4pt}}
.s08 .rowcap{{position:absolute;left:.55in;bottom:.55in}}
.steps{{display:grid;grid-template-columns:1fr 1fr;gap:.2in .35in}}
.steps h4{{display:flex;align-items:baseline;gap:8pt}}
.steps h4 span{{font-size:20pt;letter-spacing:0;color:{F_};text-transform:none}}
/* precios */
.prices{{margin-bottom:.2in}}
.pr{{display:grid;grid-template-columns:1.75in 1.75in 1fr;align-items:baseline;padding:4pt 0;border-bottom:.6pt solid rgba(47,34,56,.2)}}
.prices .lab{{margin-bottom:4pt}}
.pr b{{font-size:13pt}}
.pr span{{font-size:9.5pt}}
.pr .v{{font-size:10.5pt;font-weight:600;font-variant-numeric:tabular-nums}}
.psrc{{font-size:8pt;margin-top:5pt;opacity:.8}}
/* ocasiones */
.nl5{{list-style:none;margin-bottom:5pt;border-top:.6pt solid rgba(47,34,56,.2)}}
.nl5 li{{display:grid;grid-template-columns:.45in 1fr;font-size:14pt;padding:4pt 0;border-bottom:.6pt solid rgba(47,34,56,.2)}}
.nl5 span{{font-size:10pt;color:{F_};padding-top:3pt}}
.s15 .src{{margin-bottom:.2in}}
/* cierre */
.next{{list-style:none;margin:.05in 0 .35in;max-width:5.6in}}
.next li{{font-size:11.5pt;line-height:1.45;padding:6pt 0;border-bottom:.6pt solid rgba(255,251,250,.25)}}
.close p{{margin:0}}
.invite{{font-size:22pt;margin-bottom:.22in!important}}
.who{{font-size:15pt}}
.role{{font-size:10.5pt;opacity:.85;margin-bottom:.12in!important}}
.contact{{font-size:10.5pt}}
.web{{font-family:"Fraunces",serif;font-size:15pt;letter-spacing:.04em;color:{R_};margin-top:.16in!important}}
@media print{{html,body{{background:none}}}}
'''

DOC = f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Floresta · Decisiones de diseño del sitio web</title><style>{CSS}a{{color:inherit;text-decoration:none}}
</style></head>
<body>{"".join(PAGES)}</body></html>'''
html_out = OUT / 'floresta-dossier-diseno.html'
html_out.write_text(DOC, encoding='utf-8')

# --------------------------------------------------------------- comprobaciones
for a, b in zip(SHEETS, SHEETS[1:]):
    for k in ('lcol', 'rcol', 'left', 'right'):
        assert a[k] != b[k], f'{a["n"]}→{b["n"]} repite {k}'
for s in SHEETS:
    assert s['lcol'] != s['rcol'], s['n']
JERGA = ['github', 'lafloresta', 'precarga', 'carrusel', 'cursor', 'navegador', 'scroll', 'slider', 'hero', 'layout', 'landing',
         'responsive', 'desktop', 'mobile', 'frontend', 'código', 'antes/ahora', 'se corrigió', 'nueva versión', 'Esmeralda 998']
texto = re.sub(r'<[^>]+>', ' ', re.sub(r'<style>.*?</style>', '', re.sub(r'src="[^"]*"', '', DOC), flags=re.S))
for w in JERGA:
    assert w.lower() not in texto.lower(), f'palabra no permitida: {w}'
print('frases literales verificadas:', len(CHECKED))

from playwright.sync_api import sync_playwright
exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe)
    pg = b.new_page(viewport={'width': 1248, 'height': 816}, device_scale_factor=1950 / 1248)
    pg.goto(html_out.as_uri())
    pg.evaluate('document.fonts.ready.then(()=>1)'); pg.wait_for_timeout(800)
    bad = pg.evaluate('''() => {const r=[];
      document.querySelectorAll('.half').forEach((h,i)=>{const H=h.getBoundingClientRect(); const n=Math.floor(i/2)+1;
        h.querySelectorAll('*').forEach(e=>{const q=e.getBoundingClientRect(); if(q.width&&(q.right>H.right+.5||q.bottom>H.bottom+.5||q.left<H.left-.5||q.top<H.top-.5)) r.push(n+':'+e.tagName+'.'+e.className)});
        if(h.scrollHeight>h.clientHeight+1) r.push(n+' desborde vertical');
        const kids=[...h.children];
        for(let a=0;a<kids.length;a++)for(let c=a+1;c<kids.length;c++){const A=kids[a].getBoundingClientRect(),C=kids[c].getBoundingClientRect();
          if(A.width&&C.width&&A.left<C.right-1&&C.left<A.right-1&&A.top<C.bottom-1&&C.top<A.bottom-1) r.push(n+' solape '+kids[a].className+' / '+kids[c].className)}
        const foot=h.querySelector('.foot'); if(foot){const F=foot.getBoundingClientRect(); [...h.children].filter(k=>k!==foot).forEach(k=>{const K=k.getBoundingClientRect(); if(K.bottom>F.top+1) r.push(n+' toca el pie: '+k.className)})}
        h.querySelectorAll('p,li,figcaption,cite,span,b,code,h4').forEach(e=>{const fs=parseFloat(getComputedStyle(e).fontSize); if(e.textContent.trim() && fs<9.3) r.push(n+' letra chica '+fs.toFixed(1)+'px '+e.tagName+'.'+e.className+' «'+e.textContent.trim().slice(0,25)+'»')});
      });return r}''')
    small = [x for x in bad if 'letra chica' in x]
    other = [x for x in bad if 'letra chica' not in x]
    print('problemas:', other)
    print('textos bajo 7pt:', small[:20], len(small))
    for i in range(len(SHEETS)):
        pg.locator('.lam').nth(i).screenshot(path=str(OUT / f'pages/p-{i + 1:02d}.png'))
    pg.pdf(path=str(OUT / 'floresta-dossier-diseno.pdf'), width='13in', height='8.5in', print_background=True,
           margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}, prefer_css_page_size=True)
    b.close()
print('ok', len(SHEETS))
for s in SHEETS:
    print(f"{s['n']:02d} {CNAME[s['lcol']]:15s}| {CNAME[s['rcol']]:15s} {s['left']:3s} {s['right']}")
