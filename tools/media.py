"""Fase 07 (los videos finales los re-codifica tools/video_tune.sh con presupuesto de peso): imágenes WebP 800/1800 + LQIP (meta.json) y videos MP4 h264 faststart + WebM VP9 + póster.
Fuente: assets/raw (fuera de git). Salida: assets/img, assets/video, assets/img/meta.json."""
import json, os, subprocess, base64, io, glob
from PIL import Image, ImageOps

RAW = 'assets/raw/'
F = RAW + 'fotos/'
D = RAW + '_derivados/'
IMG = {
    # id: (archivo, alt ES, [ancho máximo opcional])
    'manif-1': (F + '20250506_DJSxjSCAghA_1.jpg', 'Ramo de girasoles, iris morados y flores blancas'),
    'manif-2': (F + '20250517_DJvWKLcgAc9_1.jpg', 'Ramo de flores moradas y lilas frente a la florería'),
    'manif-3': (F + '20251004_DPZAK2UAGz6_1.jpg', 'Ramo de tulipanes rojos y fucsia en papel kraft'),
    'manif-4': (F + '20250530_DKQhQDfAplW_1.jpg', 'Ramo de rosas fucsia y girasol'),
    'oc-ramos': (F + '20250528_DKLZLxAgLsj_1.jpg', 'Ramo de gerberas, lirios y alstroemerias'),
    'oc-arreglos': (F + '20250505_DJQPCxFADaH_1.jpg', 'Arreglos florales en cajas sobre el mesón de la florería'),
    'oc-regalos': (F + '20251027_DQUMiXogMXv_1.jpg', 'Ramo de flores amarillas y blancas'),
    'oc-despachos': (F + '20260904_Dc3l9NqFu89_1.jpg', 'Natalia en la puerta de la florería con un ramo de tulipanes'),
    'natalia': (F + '20250717_DMMDzwHgpZN_1.jpg', 'Natalia Torres Manzo sonriendo con un ramo de lirios, rosas y flores amarillas'),
    'natalia-2': (F + '20250512_DJiZA6bgtDm_1.jpg', 'Natalia en la florería con un ramo grande en las manos'),
    'natalia-3': (F + '20260425_DXibfz0FlURhwpiGNOo04otQOUv5SUdHFRYJUQ0_1.jpg', 'Natalia con un ramo de girasoles y rosas'),
    'invierno': (F + '20250514_DJohm66gLB5_1.jpg', 'Ramo de girasoles envuelto en papel kraft frente a la florería'),
    'visita': (F + '20260129_DUF5aOiAH9K_1.jpg', 'Fachada verde de Floresta con su letrero redondo y un ramo rosado'),
    'orquideas': (F + '20260914_DdQEPzjRrsV_1.jpg', 'Natalia con orquídeas en el invernadero del vivero Almácigos Chiloé'),
    'planta-1': (F + '20260319_DWEqkKlEbFl_1.jpg', 'Planta de interior sostenida frente al letrero de Floresta'),
    'planta-2': (F + '20260319_DWEqkKlEbFl_2.jpg', 'Maranta de hojas rojas en macetero frente a la florería'),
    'planta-3': (F + '20260319_DWEqkKlEbFl_3.jpg', 'Planta de hojas verdes en macetero frente a la florería'),
    'planta-4': (F + '20260319_DWEqkKlEbFl_4.jpg', 'Begonia de hojas manchadas frente a la florería'),
    'planta-5': (F + '20260319_DWEqkKlEbFl_5.jpg', 'Pilea de hojas redondas frente al letrero de Floresta'),
    'planta-6': (F + '20260319_DWEqkKlEbFl_6.jpg', 'Potus en macetero frente al letrero de Floresta'),
    'ramo-silvestres': (D + 'ramo-silvestres.jpg', 'Ramo silvestre de flores fucsia, rojas y amarillas sostenido en alto'),
    'ramo-rosas-rojas': (D + 'ramo-rosas-rojas.jpg', 'Ramo de rosas rojas en papel rosado sostenido en alto'),
    'ramo-girasoles': (D + 'ramo-girasoles.jpg', 'Ramo de girasoles en papel kraft sostenido en alto'),
    'ramo-rosas-y-girasoles': (D + 'ramo-rosas-y-girasoles.jpg', 'Ramo de rosas rojas y girasoles sostenido en alto'),
}
for n in range(1, 12):
    IMG[f'fachada-{n:02d}'] = (D + f'fachada-{n:02d}.jpg', f'Ramo {n} de 11 frente al letrero de Floresta, Esmeralda 198')

VID = {
    # id: (archivo, inicio, duración, alt ES)
    'portada': ('20260903_Dc1HniPBpeG_1.mp4', 0.5, 22, 'Mesón cubierto de flores: crisantemos, margaritas y girasoles'),
    'oficio': ('20260331_DWh0WXdgKi1_1.mp4', 6, 28, 'Natalia arma un arreglo de flores blancas sobre el mesón'),
    'jardin': ('20260904_Dc3ZBC4h0XP_1.mp4', 0, 17, 'Helleborus del jardín del vivero, frente al letrero de Floresta'),
    'corona': ('20260715_Da05yhvBxvM_1.mp4', 0, 8.5, 'Corona de flores en pedestal frente a la florería'),
}

os.makedirs('assets/img', exist_ok=True); os.makedirs('assets/video', exist_ok=True)
meta = {}

def lqip(im):
    t = im.copy(); t.thumbnail((24, 24)); b = io.BytesIO(); t.save(b, 'WEBP', quality=40)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()

def save_img(key, im, alt):
    im = ImageOps.exif_transpose(im).convert('RGB'); w, h = im.size
    out = {}
    for W in (800, 1800):
        tw = min(W, w)
        r = im.resize((tw, round(h * tw / w)), Image.LANCZOS) if tw < w else im
        p = f'assets/img/{key}-{W}.webp'
        r.save(p, 'WEBP', quality=78 if W > 800 else 80, method=6)
        out[str(W)] = {'path': p, 'w': tw}
    meta[key] = {'w': w, 'h': h, 'alt': alt, 'lqip': lqip(im), 'src': out}

for key, (path, alt) in IMG.items():
    save_img(key, Image.open(path), alt)

for key, (f, ss, dur, alt) in VID.items():
    src = RAW + 'videos/' + f
    base = f'assets/video/{key}'
    vf = 'scale=720:-2,fps=30' if key != 'portada' else 'scale=720:-2'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(dur), '-i', src, '-an', '-vf', vf,
                    '-c:v', 'libx264', '-profile:v', 'high', '-crf', '25', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', base + '.mp4'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(dur), '-i', src, '-an', '-vf', vf,
                    '-c:v', 'libvpx-vp9', '-crf', '36', '-b:v', '0', '-row-mt', '1', '-deadline', 'good', '-cpu-used', '2', base + '.webm'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss + 0.3), '-i', src, '-frames:v', '1', '-vf', 'scale=720:-2', '/tmp/_poster.png'], check=True)
    save_img(f'poster-{key}', Image.open('/tmp/_poster.png'), alt)
    meta[f'poster-{key}']['video'] = {'mp4': base + '.mp4', 'webm': base + '.webm'}

json.dump(meta, open('assets/img/meta.json', 'w'), ensure_ascii=False, indent=1)
tot = sum(os.path.getsize(p) for p in glob.glob('assets/img/*.webp') + glob.glob('assets/video/*'))
print(len(meta), 'medios ·', round(tot / 1e6, 1), 'MB')
