"""Converte o .mov do Manim (qtrle/argb) em PNG RGBA por quadro (alfa direto) para o Remotion.

O .mov NÃO é alfa direto (medido): os pixels com α = 0 guardam K (aqui (0, 0, 0): a cena não define background_color) e
o Cairo desenha em pré-multiplicado, então rgb = cor·α + K·(1 − α). O PNG e o navegador esperam alfa direto: gravar o rgb
cru fazia o Remotion multiplicar por α de novo (α²), apagando bordas e translúcidos. Aqui: cor = (rgb − K·(1 − α)) / α.
A CenaMat não tem ImageMobject (essas, sim, já viriam em alfa direto).

O compositor do Remotion 4.0.539 não decodifica qtrle ("Compositor error: Decoder not found" no <OffthreadVideo>),
então a camada Manim entra como sequência de imagens, igual à do Three.js.
Uso (na raiz do repositório): uv run python videos/vid_0030_anel_guardanapo/remotion/manim_png.py [CenaMat]
"""
import sys
import time
from pathlib import Path

import av
import numpy as np
from PIL import Image

AQUI = Path(__file__).resolve().parent
classe = sys.argv[1] if len(sys.argv) > 1 else "CenaMat"
# v5: resolução e pasta de mídia opcionais (master: 1920p30 em media_final)
res = sys.argv[2] if len(sys.argv) > 2 else "960p15"
midia = sys.argv[3] if len(sys.argv) > 3 else "media_preview"
mov = AQUI.parent / midia / "videos" / "cena" / res / f"{classe}.mov"
out = AQUI / "public" / "manim_png"
out.mkdir(parents=True, exist_ok=True)
t0, n = time.time(), 0
with av.open(str(mov)) as c:
    for n, fr in enumerate(c.decode(video=0)):
        # to_image() devolve RGB e perde o alfa: pedir rgba ao decodificador
        q = fr.to_ndarray(format="rgba")
        if n == 0:
            K = np.median(q[q[..., 3] == 0][:, :3], axis=0).astype(np.float32)
        alpha = q[..., 3:4].astype(np.float32) / 255
        cor = (q[..., :3] - K * (1 - alpha)) / np.maximum(alpha, 1 / 255)
        q[..., :3] = np.where(alpha > 0, np.clip(cor + .5, 0, 255), 0).astype(np.uint8)
        Image.fromarray(q, "RGBA").save(out / f"f{n:05d}.png", compress_level=1)
print(f"{n + 1} PNG em {time.time() - t0:.1f} s -> {out}")
