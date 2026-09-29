#!/usr/bin/env python3
"""
LA FLORESTA · Extractor de mejores tomas
=========================================
Recorre todos los videos (.mp4) y fotos (.jpg) descargados de Instagram,
revisa cada video CADA 0,5 SEGUNDOS, puntúa cada fotograma y guarda las
mejores tomas (sin duplicados) listas para usar en la web.

Puntaje (0-100) combina:
  - Nitidez      (varianza del Laplaciano; descarta fotogramas movidos)
  - Exposición   (penaliza quemados y subexpuestos)
  - Color        (colorfulness de Hasler-Süsstrunk: las flores deben "vibrar")
  - Contraste    (desviación de luminancia)
  - Texto        (penaliza fotogramas con mucho texto/gráficas sobreimpresas)
Duplicados: hash perceptual (dHash) con distancia de Hamming.

Uso:
  python mejores_tomas.py --videos ./videos --fotos ./fotos --salida ./mejores --por-video 4 --top 120
Requisitos: pip install opencv-python numpy
"""
import argparse, csv, json, os, sys
from pathlib import Path
import cv2
import numpy as np

PASO_SEG = 0.5  # revisar cada 0,5 segundos


def dhash(img, size=8):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.resize(g, (size + 1, size), interpolation=cv2.INTER_AREA)
    diff = g[:, 1:] > g[:, :-1]
    return sum(1 << i for i, v in enumerate(diff.flatten()) if v)


def hamming(a, b):
    return bin(a ^ b).count("1")


def puntuar(img):
    h, w = img.shape[:2]
    escala = 720 / max(h, w)
    if escala < 1:
        img = cv2.resize(img, (int(w * escala), int(h * escala)), interpolation=cv2.INTER_AREA)
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    nitidez = cv2.Laplacian(gris, cv2.CV_64F).var()
    s_nitidez = min(nitidez / 600.0, 1.0)

    media = gris.mean() / 255.0
    quemado = (gris > 250).mean()
    oscuro = (gris < 12).mean()
    s_expo = max(0.0, 1 - abs(media - 0.5) * 1.6 - quemado * 3 - oscuro * 2)

    b, g, r = [c.astype(np.float64) for c in cv2.split(img)]
    rg, yb = np.abs(r - g), np.abs(0.5 * (r + g) - b)
    color = np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2)
    s_color = min(color / 90.0, 1.0)

    s_contraste = min(gris.std() / 64.0, 1.0)

    # Texto sobreimpreso: muchas regiones pequeñas de alto contraste horizontal (MSER aproximado con morfología)
    grad = cv2.morphologyEx(gris, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    _, bw = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1)))
    cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lineas = 0
    for c in cnts:
        x, y, cw, ch = cv2.boundingRect(c)
        if cw > 3 * ch and 6 < ch < 40 and cw > 40:
            region = gris[y:y + ch, x:x + cw]
            if region.std() > 45:
                lineas += 1
    s_texto = max(0.0, 1 - lineas / 12.0)

    total = 100 * (0.34 * s_nitidez + 0.18 * s_expo + 0.26 * s_color + 0.10 * s_contraste + 0.12 * s_texto)
    return round(total, 2), dict(nitidez=round(nitidez, 1), exposicion=round(s_expo, 3),
                                 color=round(color, 1), contraste=round(s_contraste, 3), lineas_texto=lineas)


def fotogramas(ruta):
    # Lectura secuencial (mucho más rápida que saltar con seek): se decodifica
    # solo el fotograma que cae en cada marca de 0,5 s.
    cap = cv2.VideoCapture(str(ruta))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    i, siguiente = 0, 0.0
    while cap.grab():
        t = i / fps
        if t + 1e-6 >= siguiente:
            ok, fr = cap.retrieve()
            if ok:
                yield round(siguiente, 1), fr
            siguiente += PASO_SEG
        i += 1
    cap.release()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--videos", default="videos")
    ap.add_argument("--fotos", default="fotos")
    ap.add_argument("--salida", default="mejores")
    ap.add_argument("--por-video", type=int, default=4, help="máx. tomas por video")
    ap.add_argument("--top", type=int, default=150, help="tamaño de la selección final")
    ap.add_argument("--min", type=float, default=45, help="puntaje mínimo")
    a = ap.parse_args()

    out = Path(a.salida); (out / "tomas_video").mkdir(parents=True, exist_ok=True); (out / "seleccion").mkdir(exist_ok=True)
    candidatos = []

    videos = sorted(Path(a.videos).rglob("*.mp4")) if Path(a.videos).exists() else []
    for i, v in enumerate(videos, 1):
        tomas, revisados = [], 0
        for t, fr in fotogramas(v):
            revisados += 1
            s, det = puntuar(fr)
            tomas.append((s, t, fr, det))
        tomas.sort(key=lambda x: -x[0])
        elegidas, hashes = [], []
        for s, t, fr, det in tomas:
            if s < a.min or len(elegidas) >= a.por_video:
                break
            hsh = dhash(fr)
            if any(hamming(hsh, x) < 12 for x in hashes):
                continue
            hashes.append(hsh)
            nombre = f"{v.stem}_t{t:05.1f}s.jpg"
            cv2.imwrite(str(out / "tomas_video" / nombre), fr, [cv2.IMWRITE_JPEG_QUALITY, 92])
            elegidas.append(nombre)
            candidatos.append(dict(archivo=str(out / "tomas_video" / nombre), origen=v.name, tipo="video",
                                   segundo=t, puntaje=s, hash=hsh, **det))
        print(f"[{i}/{len(videos)}] {v.name}: {revisados} fotogramas revisados (cada {PASO_SEG}s) -> {len(elegidas)} tomas", flush=True)

    fotos = sorted(p for p in Path(a.fotos).rglob("*.jpg")) if Path(a.fotos).exists() else []
    for j, f in enumerate(fotos, 1):
        img = cv2.imread(str(f))
        if img is None:
            continue
        s, det = puntuar(img)
        candidatos.append(dict(archivo=str(f), origen=f.name, tipo="foto", segundo=None, puntaje=s, hash=dhash(img), **det))
        if j % 100 == 0:
            print(f"fotos puntuadas: {j}/{len(fotos)}", flush=True)

    candidatos.sort(key=lambda c: -c["puntaje"])
    finales, hashes = [], []
    for c in candidatos:
        if len(finales) >= a.top:
            break
        if any(hamming(c["hash"], h) < 10 for h in hashes):
            continue
        hashes.append(c["hash"])
        destino = out / "seleccion" / f"{len(finales)+1:03d}_{int(c['puntaje'])}_{Path(c['archivo']).name}"
        img = cv2.imread(c["archivo"]); cv2.imwrite(str(destino), img, [cv2.IMWRITE_JPEG_QUALITY, 92])
        c["seleccion"] = str(destino); finales.append(c)

    with open(out / "ranking.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=[k for k in candidatos[0].keys() if k != "hash"] + ["seleccion"], extrasaction="ignore")
        w.writeheader(); [w.writerow(c) for c in candidatos]
    json.dump([{k: v for k, v in c.items() if k != "hash"} for c in finales], open(out / "seleccion.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nListo: {len(videos)} videos, {len(fotos)} fotos, {len(candidatos)} candidatos -> {len(finales)} mejores en {out/'seleccion'}")


if __name__ == "__main__":
    main()
