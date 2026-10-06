"""Fase 04: paleta por k-means (k=7) sobre grupos de imágenes de assets/raw."""
import glob, numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def km(files, k=7, n=4000):
    px = []
    for f in files:
        im = Image.open(f).convert('RGBA'); im.thumbnail((200, 200))
        a = np.array(im).reshape(-1, 4); a = a[a[:, 3] > 200][:, :3]
        if len(a): px.append(a[np.random.default_rng(1).choice(len(a), min(n, len(a)), replace=False)])
    X = np.vstack(px); m = KMeans(k, n_init=4, random_state=1).fit(X)
    cnt = np.bincount(m.labels_); o = np.argsort(-cnt)
    return [('#%02x%02x%02x' % tuple(int(v) for v in m.cluster_centers_[i]), round(cnt[i] / len(X) * 100, 1)) for i in o]

P = 'assets/raw/piezas/'
GRUPOS = {
    'verde': [P + '20260504_DX69F30lsj8_2.jpg', P + '20260504_DX69F30lsj8_7.jpg'],
    'salvia': [P + f'20260504_DX69F30lsj8_{i}.jpg' for i in (3, 4, 5, 6)],
    'crema': [P + '20250912_DOgOT_wAJVo_1.jpg', P + '20260801_DberjTWBJ-u_1.jpg'],
    'fotos_2025_26': sorted(glob.glob('assets/raw/fotos/2025*.jpg') + glob.glob('assets/raw/fotos/2026*.jpg'))[::3],
}
if __name__ == '__main__':
    for g, fs in GRUPOS.items(): print(g, km(fs))
