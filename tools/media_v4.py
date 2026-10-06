"""v4: agrega a assets/img/meta.json las fotos de la portada, su continuación y la cinta de ramos (sin re-codificar videos)."""
import json
from PIL import Image
F = 'assets/raw/fotos/'
NEW = {
    'hero': (F + '20260907_DdAPKv2hBR3_1.jpg', 'Ramo de rosas rojas con gypsophila sostenido frente a la florería'),
    'cont-1': (F + '20260617_DZsd-uBBSK0_1.jpg', 'Ramo de crisantemos fucsia, alstroemerias y rosa frente al letrero de Floresta'),
    'cont-2': (F + '20260423_DXeWb3oFuvG_1.jpg', 'Ramo de rosas bicolor, margaritas y dalias frente a la florería'),
    'cinta-1': (F + '20250506_DJSxjSCAghA_1.jpg', 'Ramo de girasoles, iris morados y flores blancas'),
    'cinta-2': (F + '20250517_DJvWKLcgAc9_1.jpg', 'Ramo de flores moradas y lilas frente a la florería'),
    'cinta-3': (F + '20250530_DKQhQDfAplW_1.jpg', 'Ramo de rosas fucsia y girasol'),
    'cinta-4': (F + '20251004_DPZAK2UAGz6_1.jpg', 'Ramo de tulipanes rojos y fucsia en papel kraft'),
    'cinta-5': (F + '20251027_DQUMiXogMXv_1.jpg', 'Ramo de flores amarillas y blancas'),
    'cinta-6': (F + '20250528_DKLZLxAgLsj_1.jpg', 'Ramo de gerberas, lirios y alstroemerias'),
    'cinta-7': (F + '20260904_Dc4DvMFhMoP_1.jpg', 'Ramo de tulipanes blancos y amarillos en arpillera'),
    'cinta-8': (F + '20260908_DdC3QVghbB3_1.jpg', 'Natalia con un ramo gigante de flores de colores'),
}
import os, io, base64
from PIL import ImageOps
meta = json.load(open('assets/img/meta.json'))
def lqip(im):
    t = im.copy(); t.thumbnail((24, 24)); b = io.BytesIO(); t.save(b, 'WEBP', quality=40)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
for key, (path, alt) in NEW.items():
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB'); w, h = im.size; out = {}
    for W in (800, 1800):
        tw = min(W, w); r = im.resize((tw, round(h * tw / w)), Image.LANCZOS) if tw < w else im
        p = f'assets/img/{key}-{W}.webp'; r.save(p, 'WEBP', quality=80, method=6); out[str(W)] = {'path': p, 'w': tw}
    meta[key] = {'w': w, 'h': h, 'alt': alt, 'lqip': lqip(im), 'src': out}
json.dump(meta, open('assets/img/meta.json', 'w'), ensure_ascii=False, indent=1)
print(len(NEW), 'agregadas')
