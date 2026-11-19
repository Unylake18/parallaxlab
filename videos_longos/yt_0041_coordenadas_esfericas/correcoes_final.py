"""yt_0041 final §7/§10: prancha correcoes_final.jpg — R1 (antes: v4 em 9:50; depois: v5 no mesmo gatilho), R2 (tabela de tamanhos), R3 (atrasos de gatilho v4 × v5)."""
import json, re
from pathlib import Path
import av
from PIL import Image, ImageDraw, ImageFont
U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
def quadro(mp4, t):
    c = av.open(str(mp4)); s = c.streams.video[0]
    alvo = int(round(t * float(s.average_rate)))
    for i, fr in enumerate(c.decode(s)):
        if i == alvo:
            im = fr.to_image(); c.close(); return im.resize((960, 540))
    c.close(); return Image.new("RGB", (960, 540))
fala = A["B2-3"]["fala"].split()
al = "mais cosseno de fi vezes o primeiro menor".split()
k = next(i for i in range(len(fala)) if fala[i:i + len(al)] == al)
t_v5 = A["B2-3"]["ini"] + A["B2-3"]["t"][k] + 9.0
antes = quadro(U / "renders" / "v4" / "yt_0041_preview_v4_540p15.mp4", 9 * 60 + 50)
depois = quadro(U / "renders" / "v5" / "yt_0041_preview_v5_540p15.mp4", t_v5)
try:
    F = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22); Fm = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 17)
except OSError:
    F = Fm = ImageFont.load_default()
tab = (U / "qa" / "tamanhos_final.txt").read_text(encoding="utf-8").splitlines()
def lerv4():
    out = []
    for l in (U / "renders" / "v4" / "qa" / "palco_parado_v4.txt").read_text(encoding="utf-8").splitlines():
        if "[gatilho]" in l: out.append(l.strip())
    return out
sy = (U / "qa" / "sync_v5.txt").read_text(encoding="utf-8").splitlines()
resumo = [l for l in sy if l.startswith(("resumo", "  gatilho"))]
P = Image.new("RGB", (1920, 540 + 40 + 560), (18, 14, 34)); d = ImageDraw.Draw(P)
d.text((14, 8), "R1 · ANTES (v4, 9:50): LINHA DE BAIXO sem a matriz", font=F, fill=(255, 196, 92)); P.paste(antes, (0, 40))
d.text((974, 8), f"R1 · DEPOIS (v5, {int(t_v5 // 60)}:{t_v5 % 60:05.2f}): o rótulo some com a matriz e não volta", font=F, fill=(140, 255, 210)); P.paste(depois, (960, 40))
y0 = 590
d.text((14, y0), "R2 · tamanhos reais por bloco (1080p)", font=F, fill=(255, 196, 92))
for i, l in enumerate(tab[:24]):
    d.text((14, y0 + 30 + i * 21), l[:100], font=Fm, fill=(225, 225, 245))
d.text((974, y0), "R3 · atrasos de gatilho: v4 (12 acima de 0,3 s) × v5 (voz real)", font=F, fill=(255, 196, 92))
for i, l in enumerate(lerv4()[:12]):
    d.text((974, y0 + 30 + i * 21), l[:92], font=Fm, fill=(255, 150, 150))
for i, l in enumerate(resumo[:4]):
    d.text((974, y0 + 300 + i * 21), l[:92], font=Fm, fill=(140, 255, 210))
(U / "renders" / "final").mkdir(parents=True, exist_ok=True)
P.save(U / "renders" / "final" / "correcoes_final.jpg", quality=88)
print("ok", t_v5)
