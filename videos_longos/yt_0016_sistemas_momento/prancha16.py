"""Prancha de conferência dos 16 pontos da tabela 1.1 do handoff v4, nos tempos equivalentes do preview v4."""
import av
from PIL import Image, ImageDraw

PONTOS = [("S1 A1 logo limpo", 25.6), ("S2 T7-3 soma", 176.6), ("S3 T8 setas no balancim", 386.6), ("S4 T8-7→T8-8", 475.5),
          ("S5 T9-2→T9-3", 542.5), ("S6 chip T9", 618.8), ("S7 T10 replay", 705.4), ("S8 T10 texto BODY", 718.7),
          ("S9 E6-3 rebate", 761.9), ("S10 E6-4 0,25 J", 789.0), ("S11 E7 p_x / N / LAGO", 843.5), ("S12 E8 setas e DICA", 937.0),
          ("S13 E9-2→E9-3", 976.3), ("S14 E9-7 DICA", 1061.5), ("S15 S1 INTERNA", 1146.0), ("S16 S2 ideia 3", 1188.0)]
c = av.open("renders/preview_yt0016_v4_960x540.mp4")
alvo = {int(round(t * 15)): (n, t) for n, t in PONTOS}
ims = {}
for i, fr in enumerate(c.decode(video=0)):
    if i in alvo:
        ims[i] = fr.to_image().resize((480, 270))
    if i > max(alvo):
        break
P = Image.new("RGB", (4 * 480, 4 * 290), (15, 15, 15))
d = ImageDraw.Draw(P)
for k, i in enumerate(sorted(ims)):
    x, y = (k % 4) * 480, (k // 4) * 290
    P.paste(ims[i], (x, y + 20))
    n, t = alvo[i]
    d.text((x + 6, y + 4), f"{n}  {int(t // 60)}:{t % 60:04.1f}", fill=(255, 230, 0))
P.save("renders/conferencia_16_pontos_v4.png")
print(len(ims))
