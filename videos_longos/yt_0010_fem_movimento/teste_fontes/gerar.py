from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
R = Path(__file__).resolve().parents[3]; T = Path(__file__).resolve().parent
F = {
 "Space Grotesk Medium": R/"assets/fonts/space_grotesk/SpaceGrotesk-Medium.ttf",
 "Sanomat Regular": T/"Sanomat-Regular.ttf",
 "Sanomat Medium": T/"Sanomat-Medium.ttf",
 "Inter Regular": R/"assets/fonts/inter/Inter-Regular.ttf",
}
W, H = 1920, 1080
im = Image.new("RGB", (W, H), "#050816"); d = ImageDraw.Draw(im)
fnt = lambda p, s: ImageFont.truetype(str(p), s)
d.text((90, 40), "ELETROMAGNETISMO · FEM DE MOVIMENTO E REGRA DO FLUXO MAGNÉTICO", font=fnt(F["Space Grotesk Medium"], 26), fill="#B9C6E0")
d.text((90, 95), "FEM DE MOVIMENTO E REGRA DO FLUXO MAGNÉTICO", font=fnt(F["Space Grotesk Medium"], 62), fill="#35D9FF")
caps = "FEM DE MOVIMENTO E REGRA DO FLUXO MAGNÉTICO"
low = "fem de movimento e regra do fluxo magnético; a força não realiza trabalho"
y = 235
for name, p in F.items():
    d.text((90, y), name, font=fnt(F["Inter Regular"], 22), fill="#8FA3C4")
    d.text((90, y + 34), caps, font=fnt(p, 42), fill="#F5F7FF")
    d.text((90, y + 98), low, font=fnt(p, 42), fill="#F5F7FF")
    y += 205
im.save(T/"comparacao_fontes.png"); print("ok")
