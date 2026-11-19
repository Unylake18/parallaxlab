"""yt_0044 final §3: prancha correcoes_final.jpg (antes = still do preview v2 | depois = still da rodada final), um par por quadro afetado pelo F1–F5 (+ quadro 0 do F4)."""
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
ant, dep = U / "renders" / "final" / "antes_v2", U / "renders" / "final" / "qa" / "comparacao_v2" / "stills"
ROT = [("F4", "quadro 0 (canto inteiro)", None), ("F1", "01_H1", "01_H1"), ("F3", "06_E1-4", "06_E1-4"), ("F1", "12_E3-1", "12_E3-1"), ("F1", "13_E3-2", "13_E3-2"),
       ("F1", "14_E3-3", "14_E3-3"), ("F1", "16_E4-1", "16_E4-1"), ("F1", "17_E4-2", "17_E4-2"), ("F1", "19_E5-1", "19_E5-1"), ("F1+F2", "20_E5-2", "20_E5-2"), ("F1+F5", "26_S2", "26_S2")]


def quadro0(p):
    c = av.open(str(p))
    for fr in c.decode(video=0):
        return fr.to_image().convert("RGB").resize((1920, 1080))


W, H = 960, 540
sh = Image.new("RGB", (2 * W, len(ROT) * (H + 30)), (12, 10, 30))
d = ImageDraw.Draw(sh)
for i, (f, nome, k) in enumerate(ROT):
    y = i * (H + 30)
    if k is None:
        a = quadro0(U / "renders" / "v2" / "yt_0044_preview_v2_540p15.mp4")
        b = Image.open(U / "renders" / "final" / "stills" / "00_quadro0_PH.png").convert("RGB")
    else:
        a, b = Image.open(next(ant.glob(f"{k}_*.png"))).convert("RGB"), Image.open(dep / f"{k}.png").convert("RGB")
    d.text((10, y + 8), f"{f} · {nome} · ANTES (v2)", fill=(255, 255, 255))
    d.text((W + 10, y + 8), f"{f} · {nome} · DEPOIS (final)", fill=(255, 255, 255))
    sh.paste(a.resize((W, H)), (0, y + 30)); sh.paste(b.resize((W, H)), (W, y + 30))
(U / "renders" / "final").mkdir(parents=True, exist_ok=True)
sh.save(U / "renders" / "final" / "correcoes_final.jpg", quality=88)
print(sh.size)
