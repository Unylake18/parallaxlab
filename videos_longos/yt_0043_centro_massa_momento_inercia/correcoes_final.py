"""yt_0043 final §7: correcoes_final.jpg — R1–R13 com antes (preview v2) × depois (preview final 540p). Uso: python correcoes_final.py"""
import json
from pathlib import Path
import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
INI = json.loads((U / "renders" / "final" / "lotes_final.json").read_text())["inicio"]
f15 = lambda l: INI[l] / 15
R = [("R1 · B3-4: rótulos s e φ separados", 758.0, ("PB3", 268.5)), ("R2 · B1-2: z = z̄ no plano (menta)", 264.0, ("PB1", 153.8)),
     ("R3 · B4-2: degraus de 4√2−2 = 2(2√2−1)", 890.0, ("PB4", 118.8)), ("R4 · B2-2: G(b)−G(a) explícito", 462.0, ("PB2", 80.5)),
     ("R5 · B1-3b: chips M e M_yz, x̄ = M_yz/M", 345.0, ("PB1", 231.3)), ("R6 · B4-2: chip em s e 2π com ∫dθ", 890.0, ("PB4", 66.5)),
     ("R7 · B4-3: a cadeia com o lado esquerdo certo", 1022.0, ("PB4", 197.5)), ("R8 · B4-3→B4-4: − ⅕z⁵ + ⅓z⁵ à mostra", 1045.0, ("PB4", 212.0)),
     ("R9 · B4-4: lata fica até o triângulo", 1042.0, ("PB4", 226.3)), ("R10 · B3-3: casca desde o início", 625.0, ("PB3", 128.5)),
     ("R11 · B2-2: 1/2 fora da sonda", 478.0, ("PB2", 121.7)), ("R12 · B3-4→B3-5: sem palco vazio", 762.5, ("PB3", 269.7)),
     ("R13 · S1: fórmulas grandes no começo", 1245.0, ("PS", 6.0))]


def quadro(arq, t):
    c = av.open(str(arq)); st = c.streams.video[0]; fps = float(st.average_rate); k = int(round(t * fps))
    for i, fr in enumerate(c.decode(st)):
        if i >= k:
            im = fr.to_image(); c.close(); return im


V2 = U / "renders" / "v2" / "yt_0043_preview_v2_540p15.mp4"
FIN = U / "renders" / "final" / "yt_0043_preview_final_540p15.mp4"
W, H = 640, 360
try:
    F = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
except OSError:
    F = ImageFont.load_default()
P = Image.new("RGB", (2 * W + 30, len(R) * (H + 40) + 20), (22, 18, 34)); d = ImageDraw.Draw(P)
for j, (tit, ta, (l, tl)) in enumerate(R):
    y = 10 + j * (H + 40)
    d.text((10, y), f"{tit}   |   antes: v2 {int(ta // 60)}:{ta % 60:05.2f}   depois: final {l} {tl:.1f} s", font=F, fill=(255, 196, 92))
    P.paste(quadro(V2, ta).resize((W, H)), (10, y + 30)); P.paste(quadro(FIN, f15(l) + tl).resize((W, H)), (W + 20, y + 30))
(U / "renders" / "final").mkdir(exist_ok=True)
P.save(U / "renders" / "final" / "correcoes_final.jpg", quality=86); print("ok", P.size)
