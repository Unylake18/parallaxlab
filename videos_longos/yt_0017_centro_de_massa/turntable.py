"""granada_turntable.png (handoff v3 do lote 1, §6.4): a granada inteira e os três cacos separados, lado a lado, com o volume de cada um.
As duas imagens vêm da sonda do Three.js (exp): node threejs/r3d.js --sonda exp ... --png; os volumes, de threejs/cena3d/granada_medidas.json.
uso: python turntable.py <inteira.png> <cacos.png>"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
F = U.parents[1] / "assets" / "fonts" / "space_grotesk"
med = json.loads((U / "threejs" / "cena3d" / "granada_medidas.json").read_text(encoding="utf-8"))
br = lambda x, n=4: f"{x:.{n}f}".replace(".", ",")
a, b = Image.open(sys.argv[1]).convert("RGB"), Image.open(sys.argv[2]).convert("RGB")
pr = Image.new("RGB", (1920, 720), (5, 8, 22))
pr.paste(a.crop((240, 110, 720, 430)), (0, 150))
pr.paste(b.crop((150, 110, 870, 430)).resize((1440, 640)).crop((0, 80, 1440, 560)), (480, 150))
d = ImageDraw.Draw(pr)
fb, fm, fs = (ImageFont.truetype(str(F / n), s) for n, s in (("SpaceGrotesk-Bold.ttf", 34), ("SpaceGrotesk-Medium.ttf", 26), ("SpaceGrotesk-Medium.ttf", 22)))
d.text((40, 30), "GRANADA DE FRAGMENTAÇÃO · INTEIRA E OS TRÊS CACOS DO PRÓPRIO CORPO", font=fb, fill=(245, 247, 255))
d.text((40, 78), f"volume do corpo (quadratura) = {br(med['vol_corpo'])} · soma dos cacos = {br(med['soma'])} "
       f"({br(100 * med['soma'] / med['vol_corpo'], 2)}%) · unidades do corpo (semieixo menor = 1)", font=fs, fill=(143, 163, 196))
d.text((150, 640), f"INTEIRA · V = {br(med['vol_corpo'], 3)}", font=fm, fill=(245, 247, 255))
for k, (nome, x) in enumerate(zip(("2 kg", "1 kg", "1,5 kg"), (740, 1200, 1650))):
    fr, alvo = med["vol"][k] / med["vol_corpo"], med["frac_alvo"][k]
    d.text((x - 150, 600), f"{nome} · V = {br(med['vol'][k], 3)}", font=fm, fill=(245, 247, 255))
    d.text((x - 150, 640), f"{br(fr)} do volume (alvo {br(alvo)}; {br(100 * (fr / alvo - 1), 2)}%)", font=fs, fill=(184, 196, 218))
pr.save(U / "renders" / "granada_turntable.png")
print("ok")
