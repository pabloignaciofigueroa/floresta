#!/usr/bin/env python3
"""Floresta · dossier de diseño completo · Propuesta 2 «Dos mitades, dos colores» (18 láminas)."""
import base64, glob, io, json, pathlib
from PIL import Image, ImageOps

ROOT = pathlib.Path('/home/claude/lafloresta')
OUT = pathlib.Path(__file__).parent
(OUT / 'pages').mkdir(parents=True, exist_ok=True)
SH = ROOT / 'dossier/shots'
RAW = ROOT / 'assets/raw'

W_, R_, L_, EC = '#fffbfa', '#f6e3ea', '#efe8f6', '#e2efe8'
F_, EU, B_ = '#b8457a', '#67a284', '#2f2238'
DARK = {B_, F_}

MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
POSTS = {p['code']: p for p in json.load(open(RAW / 'textos/floresta_textos.json'))['publicaciones']}
POSTS_ALM = {p['code']: p for p in json.load(open(RAW / 'almacigos/almacigos_textos.json'))['publicaciones']}


def fecha(code):
    p = POSTS.get(code) or POSTS_ALM[code]
    y, m, d = p['fecha'][:10].split('-')
    return f'{int(d)} {MESES[int(m) - 1]} {y}'


def ig(code):
    return f'Instagram · {fecha(code)}'


def lit(code, text):
    """Frase literal: se verifica que esté tal cual en el texto de la publicación."""
    cap = (POSTS.get(code) or POSTS_ALM[code])['caption']
    assert text.replace('…', '…') in cap, f'{code}: «{text}» no está literal'
    return text


def b64(path, w=1600, crop=None, q=86):
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    if crop:
        im = im.crop(crop)
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def d(name, w=1500, top=110, bottom=None, right=None, left=0):
    """Captura de computador sin la franja de navegación del sitio."""
    im = Image.open(SH / f'{name}.jpg')
    sc = im.width / 2160
    return b64(SH / f'{name}.jpg', w, crop=(left, round(top * sc), right or im.width, bottom or im.height))


# ventana vertical (arriba, abajo) de cada captura de celular: empieza bajo la barra del sitio y termina entre dos bloques
MWIN = {'m-cont': (130, 1880), 'm-hist': (150, 1150), 'm-ocas': (130, 1710), 'm-alm': (260, 2000), 'm-visita': (175, 1780),
        'm-hero': (170, 1960), 'm-ramos': (270, 1870), 'm-esm': (340, 1470)}
MRIGHT = {'m-hero': 905}


def m(name, w=640, full=False):
    """Captura de celular sin la barra superior del sitio (y sin el vacío final)."""
    top, bot = MWIN[name]
    return b64(SH / f'{name}.jpg', w, crop=(0, top, MRIGHT.get(name, 975), bot))


def igimg(code, n=1, w=900):
    for pat in (f'fotos/*_{code}_{n}.jpg', f'fotos/portadas/*_{code}_{n}.jpg', f'piezas/*_{code}_{n}.jpg', f'almacigos/fotos/*_{code}_{n}.jpg'):
        g = glob.glob(str(RAW / pat))
        if g:
            return b64(g[0], w)
    raise FileNotFoundError(code)


def png_tint(rel, color, w=900):
    im = Image.open(ROOT / rel).convert('RGBA')
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    solid = Image.new('RGBA', im.size, color); solid.putalpha(im.getchannel('A'))
    buf = io.BytesIO(); solid.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def font(n):
    return 'data:font/woff2;base64,' + base64.b64encode((ROOT / 'assets/fonts' / f'{n}.woff2').read_bytes()).decode()


def fig(cls, src, cap='', capfirst=False):
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    return f'<figure class="{cls}">{c if capfirst else ""}<img src="{src}" alt="">{"" if capfirst else c}</figure>'


SHEETS = []


def sheet(n, left, right, lcol, rcol, rlab, lbody, rbody, foot=''):
    lk = 'on-dark' if lcol in DARK else ''
    rk = 'on-dark' if rcol in DARK else ''
    SHEETS.append(dict(n=n, left=left, right=right, lcol=lcol, rcol=rcol))
    return f'''
<article class="lam s{n:02d}" style="--l:{lcol};--r:{rcol}">
  <section class="half L {lk}"><p class="lab">El sitio</p>{lbody}</section>
  <section class="half R {rk}"><p class="lab">{rlab}</p>{rbody}
    <p class="foot"><span>{foot}</span><span class="folio">{n:02d}</span></p></section>
</article>'''


LOGO_INK = png_tint('dossier/png/logotipo.png', B_)
P = []

# 01 · Portada ---------------------------------------------------------------
P.append(sheet(1, 'C', 'T', B_, R_, 'Para Natalia',
  fig('f01', d('d-hero', right=1975, bottom=1340), 'Portada · florestachiloe.vercel.app'),
  f'''<div class="mid"><img class="logo" src="{LOGO_INK}" alt="Floresta">
      <h1>De tu Instagram<br>a <em>tu sitio</em></h1>
      <p class="line w44 mt">Cómo lo que ya mostrabas cada día se convirtió en florestachiloe.vercel.app.</p></div>''',
  'Esmeralda 198 · Castro, Chiloé · octubre 2026'))

# 02 · Carta -----------------------------------------------------------------
P.append(sheet(2, 'P', 'K', F_, L_, 'Antes de empezar',
  fig('f02', m('m-cont'), 'Tu florería · en el celular'),
  '''<div class="mid carta"><h2>Natalia:</h2>
      <p>Todo lo que necesitábamos para tu sitio ya estaba en tu Instagram. Antes de dibujar nada, leímos tus fotos, tus palabras y tus piezas.</p>
      <p>En estas láminas te mostramos de dónde viene cada parte: qué publicación tuya está detrás de cada color, de cada frase y de cada ramo.</p>
      <p>Es tu Floresta, contada en un solo lugar.</p>
      <p class="firma"><em>Pablo</em></p></div>'''))

# 03 · Cifras ----------------------------------------------------------------
n_pub = len(POSTS)
n_fot = len(glob.glob(str(RAW / 'fotos/*.jpg')))
n_vid = len(glob.glob(str(RAW / 'videos/*.mp4')))
assert (n_pub, n_fot, n_vid) == (658, 879, 110), (n_pub, n_fot, n_vid)
primera = min(p['fecha'] for p in POSTS.values())[:7]
pa, pm = primera.split('-')
MES_L = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
P.append(sheet(3, 'R', 'X', L_, B_, 'Tu Instagram',
  '<div class="row3">' + ''.join(fig('ph', m(x, 560)) for x in ('m-ramos', 'm-alm', 'm-visita')) + '</div><p class="rowcap">Ramos, Del jardín y Visítanos, en el celular</p>',
  f'''<div class="mid">
      <div class="num"><b>{n_pub}</b><span>publicaciones, desde {MES_L[int(pm) - 1]} de {pa}</span></div>
      <div class="num"><b>{n_fot}</b><span>fotos</span></div>
      <div class="num"><b>{n_vid}</b><span>videos</span></div>
      <p class="line w44 mt">Las leímos todas. De ahí sale casi todo tu sitio: tus frases, tus fotos y tus precios.</p></div>''',
  '@florestaenchiloe'))

# 04 · Lo que vimos ----------------------------------------------------------
P.append(sheet(4, 'D', 'F', W_, F_, 'Lo que vimos en tu Instagram',
  fig('f04d', d('d-cinta', top=160, bottom=830, left=70, right=1975), 'Tus ramos, uno detrás de otro · en el computador')
  + fig('f04m', m('m-hist'), 'Tus videos · en el celular'),
  f'''<div class="mid"><blockquote>“{lit('DMIK3D4Apyi', 'Silvestre. Elegante. Es Floresta.').replace('Es Floresta', 'Es&nbsp;Floresta')}”</blockquote>
      <p class="src">Tu firma · {ig('DMIK3D4Apyi')}</p>
      <ol class="nl">
        <li><span>1</span>Muestras tus ramos en la mano, frente a la florería.</li>
        <li><span>2</span>Escribes cálido y breve. Tus frases quedaron tal cual, como “{lit('DLUq_50AvEX', 'hacemos ramos con alma')}” ({fecha('DLUq_50AvEX')}).</li>
        <li><span>3</span>Tu catálogo ya tenía nombres y precios. De ahí nace Ramos.</li>
      </ol></div>'''))

# 05 · Paleta ----------------------------------------------------------------
SW = [('blanco rosado', W_), ('rosa empolvado', R_), ('lila', L_), ('eucalipto claro', EC),
      ('frambuesa', F_), ('eucalipto', EU), ('berenjena', B_)]
P.append(sheet(5, 'A', 'M', R_, W_, 'Paleta',
  fig('f05 line', d('d-esm', top=150, left=40), 'Esmeralda 198 · rosa empolvado, frambuesa, berenjena y la fachada', capfirst=True),
  '<h2 class="h32 mt4">Tus colores ya estaban<br><em>en tu florería</em></h2><div class="sws">'
  + ''.join(f'<div class="sw"><i style="background:{c}"></i><b>{n}</b><code>{c}</code></div>' for n, c in SW)
  + f'''</div><div class="w49 mt4"><p class="body">El verde de tu florería se volvió eucalipto; el coral de sus marcos y tu rosado, frambuesa y rosa empolvado. Los tonos claros y la berenjena los acompañan para que tus flores sean las protagonistas.</p>
      <p class="src acc">“{lit('DcBdWxFBuC7', '¡AMAMOS EL ROSADO!')}” · {ig('DcBdWxFBuC7')}</p></div>'''))

# 06 · Tus letras ------------------------------------------------------------
P.append(sheet(6, 'C', 'S', B_, L_, 'Tus letras',
  fig('f06', d('d-resenas'), 'Visítanos · tus reseñas y tus notas'),
  '''<div class="mid">
      <p class="kick">Fraunces · títulos y frases</p>
      <p class="spec">Silvestre. <em>Elegante.</em><br>Es Floresta.</p>
      <p class="body w46">Una letra con algo de antigua y algo de pincel: elegante sin ser rígida, como tus ramos. La cursiva en frambuesa marca la palabra que importa en cada título.</p>
      <p class="kick mt">Figtree · textos, precios y datos</p>
      <p class="spec2">Esmeralda 198, Castro<br>Lunes a sábado · 10:00 a 19:30 hrs</p>
      <p class="body w46">Clara y tranquila, para que lo práctico se lea sin esfuerzo en el celular.</p></div>'''))

# 07 · El ramo en la mano ----------------------------------------------------
P.append(sheet(7, 'P', 'O', R_, F_, 'La portada',
  fig('f07', m('m-hero'), 'Portada · en el celular'),
  f'''<div class="mid src2">
      {fig('f07i', igimg('DdAPKv2hBR3'))}
      <div><p class="kick">De aquí salió</p>
      <p class="q24">“{lit('DdAPKv2hBR3', 'Hay clásicos que nunca pasan de moda…')}”</p>
      <p class="src">{ig('DdAPKv2hBR3')}</p></div></div>
    <h2 class="h30">El ramo en la mano,<br><em>frente a la florería</em></h2>
    <p class="body w49 mt2">Así muestras tus ramos. Por eso el sitio se abre igual: el ramo a pantalla completa, tu nombre y tu frase.</p>'''))

# 08 · Ramos con alma --------------------------------------------------------
P.append(sheet(8, 'A', 'F', W_, R_, 'Manifiesto',
  fig('f08 line', d('d-cont'), 'Manifiesto · en el computador', capfirst=True),
  f'''<div class="mid"><blockquote class="bq40">“{lit('DLUq_50AvEX', 'En Floresta no hacemos “arreglos”, hacemos ramos con alma.')}”</blockquote>
      <p class="src acc">{ig('DLUq_50AvEX')}</p>
      <p class="q20 mt">“{lit('DMppRews63d', 'Mientras más silvestre… ¡mejor!')}”</p>
      <p class="src acc">{ig('DMppRews63d')}</p>
      <p class="body w46 mt">Tu manifiesto, con tus palabras exactas, es lo primero que se lee después de la portada.</p></div>'''))

# 09 · Ramos -----------------------------------------------------------------
P.append(sheet(9, 'E', 'O', L_, B_, 'Ramos',
  fig('f09', d('d-ramos'), 'Ramos · cada ramo con su nombre, sus tamaños y su precio'),
  f'''<div class="p9">
      {fig('f09i', igimg('DX69F30lsj8', 6, 700))}
      <div><p class="kick">De aquí salió</p>
      <p class="name">Tu catálogo<br><em>Día de la Madre 2026</em></p>
      <p class="src">{ig('DX69F30lsj8')}</p>
      <p class="eq">Ramo Pequeño · $15.000<br><span>en tu catálogo</span></p>
      <p class="eq">Ramos Silvestres · $15.000<br><span>en tu sitio, con la misma foto</span></p></div></div>
    <p class="body w5 mt4">Los nombres, las descripciones, los tamaños y los precios son los tuyos. Y el título de la sección es tu frase: “…{lit('DdSsnKwgGa6', 'regala flores. Flores de verdad.')}”</p>
    <p class="src mt1 rosa">{ig('DdSsnKwgGa6')}</p>'''))

# 10 · Nunca son idénticas ---------------------------------------------------
P.append(sheet(10, 'P', 'F', F_, W_, 'Esmeralda 198',
  fig('f10', m('m-esm'), 'Esmeralda 198 · en el celular'),
  f'''<div class="mid"><blockquote class="bq44">“…{lit('DZPs-SVtb-s', 'las flores son como la naturaleza: nunca son idénticas.')}”</blockquote>
      <p class="src acc">{ig('DZPs-SVtb-s')}</p>
      <p class="body w46 mt">Por eso Esmeralda 198 muestra once ramos distintos, uno detrás de otro, frente al mismo letrero de tu florería.</p></div>'''))

# 11 · Comienza con una idea -------------------------------------------------
P.append(sheet(11, 'E', 'N', R_, L_, 'Historia',
  fig('f11', d('d-hist'), 'Comienza con una idea · tus cuatro videos'),
  f'''<div class="mid"><h2 class="h34">Comienza <em>con una idea</em></h2>
      <ol class="nl ink">
        <li><span>1</span>El título es tu frase: “{lit('DaBGf9WByJu', 'Comienza con una idea, con una historia y con la intención de emocionar a quien lo recibe')}” ({fecha('DaBGf9WByJu')}).</li>
        <li><span>2</span>Los cuatro videos son tuyos y llevan tus propias palabras, como “{lit('Dal1L2VhFpw', 'Un ratito en la florería hoy…')}” ({fecha('Dal1L2VhFpw')}).</li>
        <li><span>3</span>Se ven como los subiste: verticales, uno al lado del otro, como en tu Instagram.</li>
      </ol></div>'''))

# 12 · Mi destino ------------------------------------------------------------
P.append(sheet(12, 'C', 'O', B_, W_, 'Natalia',
  fig('f12', d('d-nati'), 'Tu historia · en el computador'),
  f'''<div class="mid src2 s12g">
      {fig('f12i', igimg('DJiZA6bgtDm'))}
      <div><p class="kick">De aquí salió</p>
      <p class="q24">“{lit('DJiZA6bgtDm', 'Mi destino siempre fueron las plantas y las flores!')}”</p>
      <p class="src acc">{ig('DJiZA6bgtDm')}</p></div></div>
    <p class="body w49 mt4">Tu historia la cuentas tú: con tu foto, tu nombre y tus palabras, tal como las escribiste.</p>'''))

# 13 · Ocasiones -------------------------------------------------------------
serv = ['Ramos personalizados', 'Arreglos florales para toda ocasión', 'Regalos y detalles', 'Condolencias y coronas', 'Despachos en Castro y alrededores']
for s in serv:
    lit('DcfGCrWhf9E', s)
P.append(sheet(13, 'A', 'N', L_, R_, 'Ocasiones',
  fig('f13', m('m-ocas'), 'Ocasiones · en el celular', capfirst=True),
  f'''<div class="mid"><h2 class="h30">Tus cinco ocasiones<br><em>salen de tu lista</em></h2>
      <ol class="nl5">{''.join(f'<li><span>0{i + 1}</span>{s}</li>' for i, s in enumerate(serv))}</ol>
      <p class="src acc mt2">{ig('DcfGCrWhf9E')}</p>
      <p class="body w46 mt">Cada una lleva una foto o un video tuyo. La de condolencias, con tu corona y tus palabras ({fecha('Da05yhvBxvM')}).</p></div>'''))

# 14 · Del jardín ------------------------------------------------------------
P.append(sheet(14, 'E', 'T', W_, F_, 'Almácigos Chiloé',
  fig('f14 line', d('d-jardin'), 'Del jardín a la florería · en el computador'),
  f'''<div class="mid"><h1 class="h52">Del jardín<br><em>a la florería</em></h1>
      <p class="line w46 mt">Floresta y el vivero de Pidpid son una sola casa, y tu sitio también les da lugar a los dos.</p>
      <p class="src mt2">“{lit('DJ-mvELNwQx', '¡Ahora somos uno con Floresta!')}” · {ig('DJ-mvELNwQx')}</p></div>'''))

# 15 · Visítanos -------------------------------------------------------------
P.append(sheet(15, 'D', 'N', R_, B_, 'Visítanos',
  fig('f15d', d('d-visita-prod', w=1400, top=165, bottom=770, right=1420), 'Visítanos · con el mapa para llegar')
  + fig('f15m', m('m-visita'), 'En el celular'),
  f'''<div class="mid"><h2 class="h34">¿Buscas flores en Castro? <em>Las encontraste.</em></h2>
      <p class="src rosa mt1">{ig('DcfGCrWhf9E')}</p>
      <ol class="nl">
        <li><span>1</span>Esmeralda 198, Castro · lunes a sábado, 10:00 a 19:30 hrs, con el mapa y un enlace directo a tu WhatsApp.</li>
        <li><span>2</span>Las notas de tu pieza “Debes saber…” ({fecha('DX69F30lsj8')}): reservas, despacho y horario de despacho.</li>
        <li><span>3</span>5,0 en Google, con tus reseñas reales.</li>
      </ol></div>'''))

# 16 · Primavera -------------------------------------------------------------
P.append(sheet(16, 'C', 'F', F_, L_, 'Invierno',
  fig('f16', d('d-invierno'), 'Tu frase de invierno · en el computador'),
  f'''<div class="mid"><blockquote class="bq40">“{lit('DavQtc1Bg0w', 'Aunque estemos en pleno invierno en Chiloé, para nosotros todos los días son primavera.')}”</blockquote>
      <p class="src acc">{ig('DavQtc1Bg0w')}</p>
      <p class="body w46 mt">Tu frase ocupa la pantalla entera, sobre uno de tus ramos de girasoles.</p></div>'''))

# 17 · Recorrido -------------------------------------------------------------
rec = [('m-hero', 'Portada'), ('m-ramos', 'Ramos'), ('m-esm', 'Esmeralda 198'), ('m-ocas', 'Ocasiones'), ('m-alm', 'Del jardín'), ('m-visita', 'Visítanos')]
P.append(sheet(17, 'R', 'T', W_, R_, 'El recorrido',
  '<div class="row6">' + ''.join(fig('ph', m(x, 420), c) for x, c in rec) + '</div>',
  '''<div class="mid"><h1 class="h52">Del ramo a la puerta <em>de la florería</em></h1>
      <p class="line w46 mt">Así se recorre tu sitio en el celular, de la portada a Visítanos.</p>
      <p class="src acc mt2">florestachiloe.vercel.app</p></div>'''))

# 18 · Cierre ----------------------------------------------------------------
P.append(sheet(18, 'A', 'I', L_, B_, 'Cierre',
  fig('f18', d('d-foot', top=300, left=300, right=1860), 'El pie de tu sitio', capfirst=True),
  '''<div class="mid firma18">
      <p class="cierre">Cuando quieras, lo conversamos.</p>
      <p class="pf">PABLO FIGUEROA G.</p>
      <p class="cargo">Director de estudio</p>
      <p class="cont">pablo@bergerac.cl · +56 9 7589 2096</p>
      <p class="web">BERGERAC.CL</p></div>'''))

CSS = f'''
@font-face{{font-family:"Fraunces";font-weight:100 900;src:url({font("fraunces-latin-full-normal")}) format("woff2")}}
@font-face{{font-family:"Fraunces";font-weight:100 900;font-style:italic;src:url({font("fraunces-latin-full-italic")}) format("woff2")}}
@font-face{{font-family:"Figtree";font-weight:300 900;src:url({font("figtree-latin-wght-normal")}) format("woff2")}}
@page{{size:13in 8.5in;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#ddd}}
body{{font-family:"Figtree",sans-serif;color:{B_};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
h1,h2,em,blockquote,.name,.q24,.q20,.spec,.cierre,.carta h2{{font-family:"Fraunces",serif;font-variation-settings:"SOFT" 100;font-weight:380;letter-spacing:-.01em}}
em,blockquote,.q24,.q20{{font-style:italic;font-variation-settings:"SOFT" 100,"WONK" 1}}
em{{color:{F_}}}
.on-dark em{{color:{R_}}}
.lam{{width:13in;height:8.5in;position:relative;overflow:hidden;break-after:page;page-break-after:always;margin:0 auto;display:grid;grid-template-columns:1fr 1fr}}
.half{{position:relative;height:8.5in;padding:.62in .62in .55in;display:flex;flex-direction:column}}
.L{{background:var(--l)}} .R{{background:var(--r)}}
.on-dark{{color:{W_}}}
figure{{margin:0;position:absolute}} figure img{{display:block;width:100%;height:auto}}
figcaption{{font-size:8.5pt;letter-spacing:.04em;margin-top:9pt;opacity:.75}}
.line img{{outline:1px solid rgba(47,34,56,.16);outline-offset:-1px}}
.lab{{font-size:8.5pt;font-weight:650;letter-spacing:.2em;text-transform:uppercase;color:{F_}}}
.on-dark .lab{{color:{R_}}}
.src{{font-size:9pt;font-weight:600;letter-spacing:.12em;text-transform:uppercase;opacity:.8;margin-top:.14in}}
.acc{{color:{F_};opacity:1}} .on-dark .acc,.rosa{{color:{R_};opacity:1}}
.line{{font-size:13pt;line-height:1.5}}
.body{{font-size:11.5pt;line-height:1.5}}
.kick{{font-size:10pt;opacity:.8;margin-bottom:.1in}}
.foot{{margin-top:auto;display:flex;justify-content:space-between;align-items:baseline;font-size:8.5pt;letter-spacing:.06em;opacity:.7}}
.folio{{font-family:"Fraunces",serif;font-size:11pt;letter-spacing:0}}
.mid{{margin:auto 0}}
.w44{{max-width:4.4in}} .w46{{max-width:4.6in}} .w49{{max-width:4.9in}} .w5{{max-width:5in}}
.mt{{margin-top:.3in}} .mt1{{margin-top:.1in}} .mt2{{margin-top:.2in}} .mt4{{margin-top:.4in}}
h1{{font-size:56pt;line-height:1.02}}
.h52{{font-size:50pt;line-height:1.02}}
.h34{{font-size:34pt;line-height:1.06}} .h32{{font-size:32pt;line-height:1.06}} .h30{{font-size:28pt;line-height:1.08}}
blockquote{{font-size:46pt;line-height:1.04}}
.bq44{{font-size:42pt}} .bq40{{font-size:36pt;line-height:1.08}}
.q24{{font-size:22pt;line-height:1.15}} .q20{{font-size:22pt;line-height:1.15}}
.nl{{list-style:none;margin-top:.45in;display:flex;flex-direction:column;gap:.16in;max-width:4.9in}}
.nl li{{display:grid;grid-template-columns:.36in 1fr;font-size:11.5pt;line-height:1.45}}
.nl span,.nl5 span{{font-family:"Fraunces",serif;font-size:15pt;line-height:1.1;color:{R_}}}
.nl.ink span,.nl5 span{{color:{F_}}}
.nl5{{list-style:none;margin-top:.35in;border-top:1px solid rgba(47,34,56,.18)}}
.nl5 li{{display:grid;grid-template-columns:.5in 1fr;font-family:"Fraunces",serif;font-variation-settings:"SOFT" 100;font-size:16pt;padding:.11in 0;border-bottom:1px solid rgba(47,34,56,.18)}}
.nl5 span{{font-size:11pt;padding-top:4pt}}

/* izquierda */
.f01{{left:.62in;right:.62in;top:50%;transform:translateY(-50%)}}
.f02{{left:50%;top:50%;width:2.2in;transform:translate(-50%,-50%)}}
.row3{{margin:auto 0 0;display:grid;grid-template-columns:repeat(3,1fr);gap:.22in}}
.row3 figure,.row6 figure{{position:static}}
.row3{{align-items:start}}
.rowcap{{font-size:8.5pt;letter-spacing:.04em;margin:9pt 0 auto;opacity:.75}}
.f04d{{left:.62in;right:.62in;top:1.2in}}
.f04m{{right:.62in;bottom:.55in;width:2.3in}} .f04m figcaption{{text-align:right}}
.f05{{left:0;right:0;bottom:0}} .f05 figcaption{{margin:0 0 9pt .62in}}
.f06{{left:.62in;right:.62in;top:50%;transform:translateY(-50%)}}
.f07{{left:50%;bottom:.55in;width:2.15in;transform:translateX(-50%)}}
.f08{{left:0;right:0;bottom:0}} .f08 figcaption{{margin:0 0 9pt .62in}}
.f09{{left:0;width:5.88in;top:2.3in}} .f09 figcaption{{padding-left:.62in}}
.f10{{left:50%;top:50%;width:2.7in;transform:translate(-50%,-50%)}}
.f11{{right:0;width:5.88in;top:1.55in}}
.f12{{left:.62in;right:.62in;top:50%;transform:translateY(-50%)}}
.f13{{left:50%;width:2.5in;bottom:0;transform:translateX(-50%)}} .f13 figcaption{{margin:0 0 9pt}}
.f14{{left:0;width:5.9in;bottom:.55in}} .f14 figcaption{{padding-left:.62in}}
.f15d{{left:.62in;top:1.2in;width:4.4in}}
.f15m{{right:.62in;bottom:.55in;width:1.62in}} .f15m figcaption{{text-align:right}}
.f16{{left:.5in;right:.5in;top:50%;transform:translateY(-50%)}}
.row6{{margin:auto 0;display:grid;grid-template-columns:repeat(3,1.45in);justify-content:space-between;align-items:start;gap:.28in 0}}

.row6 figcaption{{margin-top:6pt}}
.f18{{left:.62in;right:0;bottom:0}} .f18 figcaption{{margin:0 0 9pt}}

/* derecha */
.logo{{width:2.2in;display:block;margin-bottom:.55in}}
.carta h2{{font-size:40pt;margin-bottom:.35in}}
.carta p{{font-size:13pt;line-height:1.55;max-width:4.6in;margin-bottom:.16in}}
.carta .firma{{font-size:22pt;margin-top:.2in}}
.num{{display:grid;grid-template-columns:2.6in 1fr;align-items:baseline;border-bottom:1px solid rgba(255,251,250,.22);padding:.1in 0}}
.num b{{font-family:"Fraunces",serif;font-variation-settings:"SOFT" 100;font-weight:330;font-size:64pt;line-height:1.05;color:{R_}}}
.num span{{font-size:12pt}}
.sws{{display:grid;grid-template-columns:repeat(7,1fr);gap:.07in;margin-top:.45in}}
.sw i{{display:block;height:2.3in;box-shadow:inset 0 0 0 1px rgba(47,34,56,.14)}}
.sw b{{display:block;font-weight:600;font-size:9pt;line-height:1.2;margin-top:8pt;min-height:2.4em}}
.sw code{{font-family:"Figtree",sans-serif;font-size:8.5pt;letter-spacing:.03em;opacity:.7}}
.spec{{font-size:44pt;line-height:1.05;margin-bottom:.2in}}
.spec2{{font-size:20pt;line-height:1.3;font-weight:450;margin-bottom:.16in}}
.src2{{display:grid;grid-template-columns:2.3in 1fr;gap:.35in;align-items:end;margin:auto 0 .45in}}
.src2 figure{{position:static}}
.p9{{display:grid;grid-template-columns:2.35in 1fr;gap:.38in;margin-top:.5in;align-items:end}}
.p9 figure{{position:static}}
.name{{font-size:24pt;line-height:1.1}}
.eq{{font-size:12pt;line-height:1.35;margin-top:.24in}}
.eq span{{font-size:9.5pt;opacity:.7}}
.firma18 p{{margin:0}}
.cierre{{font-size:40pt;line-height:1.08;margin-bottom:.6in!important;max-width:5in}}
.pf{{font-size:12pt;font-weight:700;letter-spacing:.2em}}
.cargo{{font-size:12pt;margin:.06in 0 .3in!important;opacity:.85}}
.cont{{font-size:12pt}}
.web{{font-size:11pt;font-weight:700;letter-spacing:.24em;color:{R_};margin-top:.3in!important}}
@media print{{html,body{{background:none}}}}
'''

DOC = f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Floresta · Dossier de diseño</title><style>{CSS}</style></head>
<body>{"".join(P)}</body></html>'''
html = OUT / 'floresta-dossier-diseno.html'
html.write_text(DOC, encoding='utf-8')

# comprobación de secuencias
for a, b in zip(SHEETS, SHEETS[1:]):
    for k in ('left', 'right', 'lcol', 'rcol'):
        assert a[k] != b[k], f'{a["n"]}→{b["n"]} repite {k}'
for s in SHEETS:
    assert s['lcol'] != s['rcol'], s['n']

from playwright.sync_api import sync_playwright
exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe)
    pg = b.new_page(viewport={'width': 1248, 'height': 816}, device_scale_factor=1950 / 1248)
    pg.goto(html.as_uri())
    pg.evaluate('document.fonts.ready.then(()=>1)'); pg.wait_for_timeout(800)
    bad = pg.evaluate('''() => {const r=[];
      document.querySelectorAll('.half').forEach((h,i)=>{const H=h.getBoundingClientRect(); const n=Math.floor(i/2)+1;
        h.querySelectorAll('*').forEach(e=>{const q=e.getBoundingClientRect(); if(q.width&&(q.right>H.right+.5||q.bottom>H.bottom+.5||q.left<H.left-.5||q.top<H.top-.5)) r.push(n+':'+e.tagName+'.'+e.className)});
        h.querySelectorAll('*').forEach(e=>{if(e.scrollHeight>e.clientHeight+1&&getComputedStyle(e).overflow!=='visible') r.push(n+' scroll '+e.className)});
        const kids=[...h.children];
        for(let a=0;a<kids.length;a++)for(let c=a+1;c<kids.length;c++){const A=kids[a].getBoundingClientRect(),C=kids[c].getBoundingClientRect();
          if(A.width&&C.width&&A.left<C.right-1&&C.left<A.right-1&&A.top<C.bottom-1&&C.top<A.bottom-1) r.push(n+' overlap '+kids[a].className+' / '+kids[c].className)}
        const imgs=[...h.querySelectorAll('img')]; imgs.forEach(im=>{ if(getComputedStyle(im).objectFit!=='cover'){const ra=im.naturalWidth/im.naturalHeight, rb=im.clientWidth/im.clientHeight; if(Math.abs(ra-rb)>0.02) r.push(n+' distorsión '+im.parentElement.className)}});
      });return r}''')
    print('problemas:', bad)
    for i in range(len(SHEETS)):
        pg.locator('.lam').nth(i).screenshot(path=str(OUT / f'pages/p-{i + 1:02d}.png'))
    pg.pdf(path=str(OUT / 'floresta-dossier-diseno.pdf'), width='13in', height='8.5in', print_background=True,
           margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}, prefer_css_page_size=True)
    b.close()
print('ok', len(SHEETS))
