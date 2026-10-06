"""Recorta el ramo de referencia (mano + ramo sobre salvia) de cada pieza del catálogo de mayo 2026.
Se borra el rótulo '* Ramo de referencia' horneado en la imagen (cv2.inpaint) porque el sitio lo escribe como texto."""
import cv2, numpy as np
P = 'assets/raw/piezas/20260504_DX69F30lsj8_{}.jpg'
CROPS = {'girasoles': (3, 260), 'rosas-rojas': (4, 340), 'rosas-y-girasoles': (5, 300), 'silvestres': (6, 300)}
for name, (n, x0) in CROPS.items():
    im = cv2.imread(P.format(n)); h, w = im.shape[:2]
    bg = np.median(im[1200:1260, 20:120].reshape(-1, 3), 0)
    reg = im[1780:1880, 760:1260].astype(int)
    d = np.abs(reg - bg).sum(2) > 40
    mask = np.zeros(im.shape[:2], np.uint8); mask[1780:1880, 760:1260] = d * 255
    mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))
    im = cv2.inpaint(im, mask, 6, cv2.INPAINT_TELEA)
    crop = im[1130:1920, x0:x0 + 860]
    cv2.imwrite(f'assets/raw/_derivados/ramo-{name}.jpg', crop, [cv2.IMWRITE_JPEG_QUALITY, 93])
    print(name, crop.shape, bg)
