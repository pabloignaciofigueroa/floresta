"""v4.1: portada en 3 ramos, siempre desde el archivo original (sin IA, sin reescalar hacia arriba).
Se codifica al ancho nativo con calidad alta para que no aparezcan bloques de compresión."""
import json, io, base64
from PIL import Image, ImageOps
F = 'assets/raw/fotos/'
NEW = {
    'hero-1': (F + '20260907_DdAPKv2hBR3_1.jpg', 'Ramo de rosas rojas con gypsophila sostenido frente a la florería'),
    'hero-2': (F + '20260908_DdC3QVghbB3_1.jpg', 'Natalia con un ramo gigante de flores de colores'),
    'hero-3': (F + '20260627_DaGBcNkg4xT_1.jpg', 'Ramo de rosas, lisianthus y alstroemerias rosadas frente a la florería'),
}
meta = json.load(open('assets/img/meta.json'))
def lqip(im):
    t = im.copy(); t.thumbnail((24, 24)); b = io.BytesIO(); t.save(b, 'WEBP', quality=40)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
for key, (path, alt) in NEW.items():
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB'); w, h = im.size; out = {}
    for W, q in ((800, 82), (1800, 92)):
        tw = min(W, w); r = im.resize((tw, round(h * tw / w)), Image.LANCZOS) if tw < w else im
        p = f'assets/img/{key}-{W}.webp'; r.save(p, 'WEBP', quality=q, method=6); out[str(W)] = {'path': p, 'w': tw}
    meta[key] = {'w': w, 'h': h, 'alt': alt, 'lqip': lqip(im), 'src': out}
meta.pop('hero', None)
json.dump(meta, open('assets/img/meta.json', 'w'), ensure_ascii=False, indent=1)
print(len(NEW), 'listas')
