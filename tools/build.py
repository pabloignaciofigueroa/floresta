#!/usr/bin/env python3
"""Arma index.html desde src/index.html.

Reemplaza cada <x-img ...> por un <img> responsivo con srcset, ancho/alto reales,
placeholder borroso (LQIP) y data-alt-en. Falla si falta un texto alternativo en inglés.
Inserta el manifiesto de carga crítica que usa la precarga. Uso: python3 tools/build.py
"""
import json, re, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = json.loads((ROOT / 'assets/img/meta.json').read_text())
SRC = (ROOT / 'src/index.html').read_text()
ALT_EN = json.loads((ROOT / 'tools/alt-en.json').read_text())


def attrs(s):
    kv = {k: (a if a else b) for k, a, b in re.findall(r"([\w-]+)=(?:\"([^\"]*)\"|'([^']*)')", s)}
    bare = re.sub(r"[\w-]+=(?:\"[^\"]*\"|'[^']*')", '', s).split()
    return kv | {k: '' for k in bare}


def repl(m):
    a = attrs(m.group(1))
    i = a['id']
    meta = META[i]
    eager = 'eager' in a
    cls = a.get('class', '')
    sizes = a.get('sizes', '100vw')
    alt = a.get('alt', '')
    extra = a.get('data', '')
    if alt:
        if alt not in ALT_EN:
            raise SystemExit(f'Falta alt en inglés para "{alt}" ({i}) en tools/alt-en.json')
        extra += f' data-alt-en="{html.escape(ALT_EN[alt])}"'
    s, l = meta['src']['800'], meta['src']['1800']
    srcset = f'{s["path"]} {s["w"]}w' + (f', {l["path"]} {l["w"]}w' if l['w'] > s['w'] else '')
    return (
        f'<img class="{cls}" src="{l["path"]}" srcset="{srcset}" sizes="{sizes}" '
        f'width="{meta["w"]}" height="{meta["h"]}" alt="{html.escape(alt)}" '
        + ('fetchpriority="high" ' if eager else 'loading="lazy" ')
        + f'decoding="async" style="background-image:url({meta["lqip"]})" {extra}>'
    )


out = re.sub(r'<x-img\s+([^>]*?)\s*/?>', repl, SRC)


def size(rel):
    return (ROOT / rel).stat().st_size


# Lo que la precarga espera (con su peso real) antes de abrir la portada.
CRITICAL_IMGS = [('hero', 1), ('cont-1', .42), ('cont-2', .18)]
FONTS = ['allura-latin-400-normal', 'catamaran-latin-400-normal', 'catamaran-latin-600-normal', 'catamaran-latin-700-normal']
crit = {
    'fonts': [{'url': f'assets/fonts/{f}.woff2', 'bytes': size(f'assets/fonts/{f}.woff2')} for f in FONTS]
             + [{'url': f'brand/logo/{f}', 'bytes': size(f'brand/logo/{f}')} for f in ('logotipo.svg', 'isotipo.svg')],
    'imgs': [{'frac': fr,
              's': {'url': META[i]['src']['800']['path'], 'bytes': size(META[i]['src']['800']['path'])},
              'l': {'url': META[i]['src']['1800']['path'], 'bytes': size(META[i]['src']['1800']['path'])}} for i, fr in CRITICAL_IMGS],
    'video': None,
}
out = out.replace('<!--CRITICAL-->', '<script type="application/json" id="critical">' + json.dumps(crit, separators=(',', ':')) + '</script>')
(ROOT / 'index.html').write_text(out)
left = re.findall(r'<x-img', out)
print('index.html listo', len(out) // 1024, 'KB · pendientes:', len(left))
