"""yt_0045 final R6 medido no still 1080p do B4-3: ponta de sentido (laranja) × última seta de F (t = 1,5) e × círculo; seta × círculo."""
import numpy as np
from PIL import Image
from scipy import ndimage
a = np.asarray(Image.open("renders/final/qa/comparacao/stills/09_B4-3_no_raio.png").convert("RGB")).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
verde = (g > 190) & (r < 110) & (b > 120) & (b < 200)
lar = (r > 220) & (g > 140) & (g < 215) & (b < 150)
lima = (r > 170) & (r < 225) & (g > 220) & (b < 140)
y0, y1 = 520, 600
def sub(m, x0, x1):
    z = np.zeros_like(m); z[y0:y1, x0:x1] = m[y0:y1, x0:x1]; return z
# a haste da ponta de sentido (1,55→1,82) corre em cima do segmento laranja (mesma cor); o que se lê como "ponta" é a cabeça: últimos 14,4 px (x 683,6–698)
sen, seta, circ = sub(lar, 684, 700), sub(verde, 640, 680), sub(lima, 704, 740)
xs = np.where(sen.any(0))[0]
out = [f"B4-3 (R6, still nativo 1080p): cabeça da ponta de sentido x {xs.min()}–{xs.max()} px",
       f"  sentido × última seta de F (t = 1,5): {ndimage.distance_transform_edt(~seta)[sen].min():.1f} px",
       f"  sentido × círculo: {ndimage.distance_transform_edt(~circ)[sen].min():.1f} px",
       f"  última seta de F × círculo: {ndimage.distance_transform_edt(~circ)[seta].min():.1f} px"]
open("renders/final/qa/b43_r6.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
