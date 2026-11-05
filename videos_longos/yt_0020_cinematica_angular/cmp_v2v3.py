"""Comparação v2×v3 (QA): quadros nos mesmos instantes, v2 em cima e v3 embaixo → renders/v3/v2xv3/<nome>.png"""
import av
from pathlib import Path
from PIL import Image, ImageDraw
U = Path(__file__).resolve().parent
V = {"v2": U/"renders/preview_yt0020_v2_960x540.mp4", "v3": U/"renders/preview_yt0020_v3_960x540.mp4"}
ITENS = [("H1_helice", 14), ("H3_frase", 37.5), ("A3_conta", 88), ("T1-5_contador", 229.7), ("T2-4_helice", 306.4), ("T2-5_cronometro", 330.4),
 ("T3-1_tmt_cor", 352.1), ("T3-4_inset", 433.8), ("T4-1_disco", 520), ("T4-4_tmt", 624), ("T5-4_tmt", 811), ("T5-5_mao_disco", 837.5),
 ("T5-8_operadores_setas", 938.5), ("E1-1_cota", 966.1), ("E1-6_eixo", 1139.6), ("E2-1_coluna", 1158.5), ("E2-3_algebra", 1218.7),
 ("E3-2_terra", 1378.8), ("PS_helice", 1588.4)]
def quadro(mp4, t):
    c = av.open(str(mp4)); s = c.streams.video[0]
    c.seek(int(t / s.time_base), stream=s)
    for f in c.decode(s):
        if f.time >= t - 1e-3:
            im = f.to_image(); c.close(); return im
    c.close()
for nome, t in ITENS:
    a, b = quadro(V["v2"], t), quadro(V["v3"], t)
    W, H = a.size
    out = Image.new("RGB", (W, 2*H + 4), (255, 0, 255))
    out.paste(a, (0, 0)); out.paste(b, (0, H + 4))
    d = ImageDraw.Draw(out)
    d.rectangle((0, 0, 170, 16), fill=(0,0,0)); d.text((4, 2), f"v2 · {t:.1f} s · {nome}", fill=(255,255,255))
    d.rectangle((0, H+4, 170, H+20), fill=(0,0,0)); d.text((4, H+6), f"v3 · {t:.1f} s", fill=(255,255,255))
    out.save(U/"renders/v3/v2xv3"/f"{nome}.png")
print(len(ITENS), "comparações")
