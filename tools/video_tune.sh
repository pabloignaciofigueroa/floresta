#!/bin/sh
# Re-codifica los videos con un presupuesto de peso: portada (crítica) y oficio (mucho detalle).
# uso: sh tools/video_tune.sh  (requiere assets/raw)
set -e
enc() { # id archivo inicio duración ancho crf264 crfvp9
  src="assets/raw/videos/$2"; out="assets/video/$1"
  ffmpeg -v error -y -ss $3 -t $4 -i "$src" -an -vf "scale=$5:-2,fps=24" -c:v libx264 -profile:v high -crf $6 -preset slow -pix_fmt yuv420p -movflags +faststart "$out.mp4"
  ffmpeg -v error -y -ss $3 -t $4 -i "$src" -an -vf "scale=$5:-2,fps=24" -c:v libvpx-vp9 -crf $7 -b:v 0 -row-mt 1 -deadline good -cpu-used 3 "$out.webm"
}
enc portada 20260903_Dc1HniPBpeG_1.mp4 0.5 14 640 29 40
enc oficio 20260331_DWh0WXdgKi1_1.mp4 6 16 540 31 44
enc corona 20260715_Da05yhvBxvM_1.mp4 0 8.5 540 28 40
enc jardin 20260904_Dc3ZBC4h0XP_1.mp4 0 14 640 29 40
ls -la assets/video
