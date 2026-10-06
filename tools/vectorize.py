"""Fase 05: vectoriza logotipo e isotipo desde los PNG originales con potrace (por capas de color)."""
import subprocess, re, numpy as np, os, tempfile
from PIL import Image

def trace(mask, turd=4, alpha=1.0, opt=0.4):
    """mask: bool array (True = tinta). Devuelve (viewBox w,h, lista de 'd')."""
    h, w = mask.shape
    with tempfile.TemporaryDirectory() as t:
        pbm = os.path.join(t, 'm.pbm'); svg = os.path.join(t, 'm.svg')
        Image.fromarray(((~mask) * 255).astype('uint8')).convert('1').save(pbm)
        subprocess.run(['potrace', pbm, '-s', '-o', svg, '-t', str(turd), '-a', str(alpha), '-O', str(opt), '--flat'], check=True)
        s = open(svg).read()
    tr = re.search(r'<g transform="([^"]+)"', s).group(1)
    ds = re.findall(r'<path d="([^"]+)"', s, re.S)
    return w, h, tr, [' '.join(d.split()) for d in ds]

def layer(tr, ds, fill, extra=''):
    return f'<g transform="{tr}" fill="{fill}"{extra}>' + ''.join(f'<path d="{d}"/>' for d in ds) + '</g>'

def logotipo():
    a = np.array(Image.open('assets/raw/logos/logotipo.png').convert('RGBA'))
    m = a[:, :, 3] > 127
    w, h, tr, ds = trace(m)
    return w, h, layer(tr, ds, 'currentColor')

def isotipo():
    a = np.array(Image.open('assets/raw/logos/isotipo.png').convert('RGBA')).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    linea = (al > 140) & (r + g + b < 330)
    coral = (al > 140) & (r > 180) & (r - g > 40)
    hoja = (al > 25) & ~linea & ~coral
    # rellenos bajo la línea: se dilatan un poco para no dejar huecos
    import cv2
    k = np.ones((5, 5), np.uint8)
    coral = cv2.dilate(coral.astype(np.uint8), k).astype(bool)
    hoja = cv2.dilate(hoja.astype(np.uint8), k).astype(bool)
    def limpia(m, minarea=400):
        n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
        keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] >= minarea
        return keep[lab]
    coral, hoja = limpia(coral), limpia(hoja, 2000)
    w, h, tr, dl = trace(linea, turd=6)
    # los rellenos van debajo de la línea: se trazan a 1/4 de resolución
    def small(m):
        return np.array(Image.fromarray(m.astype(np.uint8) * 255).resize((m.shape[1] // 4, m.shape[0] // 4), Image.BILINEAR)) > 127
    _, _, trs, dc = trace(small(coral), turd=6)
    _, _, _, dh = trace(small(hoja), turd=6)
    return w, h, tr, dl, dc, dh, trs

if __name__ == '__main__':
    W, H, g = logotipo()
    open('brand/logo/logotipo.svg', 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Floresta" style="color:#32583c">{g}</svg>')
    w, h, tr, dl, dc, dh, trs = isotipo()
    def iso(linea='#305038', coral='#f8b0a0', hoja='#e4f4e7', hoja_op='.44', cls=''):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Floresta"{cls}>'
                + '<g transform="scale(4)">' + layer(trs, dh, hoja, f' fill-opacity="{hoja_op}"') + layer(trs, dc, coral, ' class="iso-coral"') + '</g>' + layer(tr, dl, linea, ' class="iso-linea"') + '</svg>')
    open('brand/logo/isotipo.svg', 'w').write(iso())
    open('brand/logo/isotipo-claro.svg', 'w').write(iso(linea='#f7f4ed', hoja='#c9d6c4', hoja_op='.25'))
    open('brand/logo/isotipo-mono.svg', 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Floresta">' + layer(tr, dl, 'currentColor') + '</svg>')
    # solo la línea, como trazos para el momento memorable
    open('brand/logo/_isotipo_linea_paths.txt', 'w').write('\n'.join(dl))
    print('ok', W, H, w, h, len(dl), len(dc), len(dh))
