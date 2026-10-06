"""Momento memorable: alinea los ramos fotografiados frente al letrero redondo de Esmeralda 198.
Busca el letrero (plantilla tools/letrero_template.png, multi-escala) y recorta cada foto para que el letrero
quede en el mismo lugar y al mismo tamaño. Así, al pasar las fotos, el letrero queda quieto y solo cambia el ramo."""
import cv2, numpy as np, json, sys
from PIL import Image, ImageFilter

FOTOS = ['20251115_DRFHHhKkdYz_1', '20251124_DRcUHhlANGE_1', '20260316_DV8ZZI9gCgv_1', '20260410_DW9Nix6gSXd_1',
         '20260423_DXeWb3oFuvG_1', '20260424_DXg7SuzlqaL_1', '20260502_DX10FqpAZAU_1', '20260528_DY4xij0BZcF_1',
         '20260617_DZsd-uBBSK0_1', '20260627_DaGBcNkg4xT_1', '20260814_DcBdWxFBuC7_1']
OW, OH, TX, TY, TW = 800, 1120, 400, 220, 210
T0 = cv2.imread('tools/letrero_template.png', 0)

def busca(g):
    top = g[:int(g.shape[0] * .55)]; best = (-1,)
    for sc in np.linspace(.5, 2.2, 52):
        T = cv2.resize(T0, None, fx=sc, fy=sc)
        if T.shape[0] >= top.shape[0] or T.shape[1] >= top.shape[1]: continue
        _, mv, _, ml = cv2.minMaxLoc(cv2.matchTemplate(top, T, cv2.TM_CCOEFF_NORMED))
        if mv > best[0]: best = (mv, ml[0] + T.shape[1] / 2, ml[1] + T.shape[0] / 2, sc)
    return best

meta = {}
for n, f in enumerate(FOTOS, 1):
    src = f'assets/raw/fotos/{f}.jpg'
    mv, x, y, sc = busca(cv2.imread(src, 0))
    im = Image.open(src).convert('RGB'); k = TW / (243 * sc)
    im2 = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    L, T = round(x * k - TX), round(y * k - TY)
    # relleno: la misma foto ampliada y desenfocada (solo se ve si falta borde)
    fondo = im.resize((OW, OH), Image.LANCZOS).filter(ImageFilter.GaussianBlur(30))
    fondo.paste(im2, (-L, -T))
    out = f'assets/raw/_derivados/fachada-{n:02d}.jpg'; fondo.save(out, quality=92)
    meta[out] = {'fuente': f, 'confianza': round(mv, 3)}
    print(out, f, round(mv, 3))
json.dump(meta, open('assets/raw/_derivados/fachada.json', 'w'), indent=1)
