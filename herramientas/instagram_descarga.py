#!/usr/bin/env python3
"""
LA FLORESTA · Descarga completa de Instagram (@florestaenchiloe)
================================================================
Baja TODAS las fotos, videos y textos del perfil y los ordena en:
  fotos/    -> imágenes (incluye cada foto de los carruseles)
  videos/   -> reels y videos (.mp4)
  textos.json -> caption, fecha, likes y archivos de cada publicación

Usa tu sesión de Instagram ya abierta en Chrome/Edge/Firefox (no pide contraseña):
lee las cookies del navegador con browser_cookie3.

Uso (Windows):
  pip install instaloader browser_cookie3 opencv-python numpy
  python instagram_descarga.py                # usa Chrome
  python instagram_descarga.py --navegador edge
  python instagram_descarga.py --y-mejores    # descarga y luego extrae mejores tomas
Si Chrome bloquea sus cookies (Chrome 127+ en Windows), cierra Chrome antes de ejecutar,
o usa el método alternativo: scripts/descargar_desde_chrome.js (se pega en la consola del navegador).
"""
import argparse, json, shutil, subprocess, sys, time
from pathlib import Path

PERFIL = "florestaenchiloe"


def sesion(L, navegador):
    import browser_cookie3
    fn = getattr(browser_cookie3, navegador)
    cj = fn(domain_name="instagram.com")
    n = 0
    for c in cj:
        L.context._session.cookies.set(c.name, c.value, domain=c.domain, path=c.path)
        n += 1
    L.context._session.headers.update({"X-CSRFToken": L.context._session.cookies.get("csrftoken", "")})
    usuario = L.test_login()
    if not usuario:
        sys.exit("No se encontró sesión de Instagram en el navegador. Inicia sesión en instagram.com y reintenta.")
    L.context.username = usuario
    print(f"Sesión OK como @{usuario} ({n} cookies)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--navegador", default="chrome", choices=["chrome", "edge", "firefox", "brave", "opera"])
    ap.add_argument("--salida", default=".")
    ap.add_argument("--y-mejores", action="store_true")
    a = ap.parse_args()

    import instaloader
    base = Path(a.salida).resolve()
    crudo = base / "_instaloader"
    L = instaloader.Instaloader(dirname_pattern=str(crudo), filename_pattern="{date_utc:%Y%m%d}_{shortcode}",
                                download_video_thumbnails=True, save_metadata=False, compress_json=False,
                                post_metadata_txt_pattern="", max_connection_attempts=5)
    sesion(L, a.navegador)
    perfil = instaloader.Profile.from_username(L.context, PERFIL)
    print(f"@{PERFIL}: {perfil.mediacount} publicaciones")

    meta = []
    for i, post in enumerate(perfil.get_posts(), 1):
        for intento in range(3):
            try:
                L.download_post(post, target=PERFIL)
                break
            except instaloader.exceptions.TooManyRequestsException:
                print("Instagram pidió pausa: espero 5 min…"); time.sleep(300)
        meta.append(dict(code=post.shortcode, url=f"https://www.instagram.com/p/{post.shortcode}/",
                         fecha=post.date_utc.isoformat(), likes=post.likes, caption=post.caption or "",
                         tipo=post.typename))
        print(f"[{i}/{perfil.mediacount}] {post.shortcode}", flush=True)
        time.sleep(1.5)  # ritmo amable para no gatillar bloqueos

    (base / "fotos").mkdir(exist_ok=True); (base / "videos").mkdir(exist_ok=True)
    for f in crudo.rglob("*"):
        if f.suffix.lower() == ".mp4":
            shutil.move(str(f), base / "videos" / f.name)
        elif f.suffix.lower() in (".jpg", ".jpeg", ".webp", ".png"):
            shutil.move(str(f), base / "fotos" / f.name)
    json.dump(dict(perfil=PERFIL, publicaciones=meta), open(base / "textos.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    shutil.rmtree(crudo, ignore_errors=True)
    print(f"Listo: {len(list((base/'fotos').iterdir()))} fotos, {len(list((base/'videos').iterdir()))} videos.")

    if a.y_mejores:
        subprocess.run([sys.executable, str(Path(__file__).with_name("mejores_tomas.py")),
                        "--videos", str(base / "videos"), "--fotos", str(base / "fotos"),
                        "--salida", str(base / "mejores")], check=True)


if __name__ == "__main__":
    main()
