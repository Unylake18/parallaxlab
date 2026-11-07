"""yt_0020 — texturas do Three.js, gravadas como data URI em threejs/cena3d/tex20.js (o Chrome não sobe imagem file:// para o WebGL).
- TERRA: mapa equirretangular 1024×512 com contornos grosseiros dos continentes (lon, lat), oceano escuro e terra em verde-terroso
  dessaturado (handoff §2.1: nada de verde #3FE08B nem âmbar na Terra).
- CAPA: capa do livro do T5 (azul-escuro neutro com a logo do Parallax Lab); CONTRA: contracapa lisa.
uso: python gerar_texturas.py"""
import base64
import io
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

U = Path(__file__).resolve().parent
ROOT = U.parents[1]

CONT = {
    "am_sul": [(-80, 10), (-75, 11), (-62, 10), (-50, 0), (-35, -5), (-39, -13), (-41, -22), (-48, -27), (-58, -35), (-65, -41), (-68, -54), (-75, -50),
               (-73, -40), (-71, -30), (-70, -18), (-77, -12), (-81, -5), (-80, 1), (-78, 8)],
    "am_norte": [(-168, 65), (-155, 71), (-120, 70), (-95, 72), (-80, 63), (-65, 60), (-55, 50), (-67, 45), (-76, 35), (-81, 25), (-82, 30), (-90, 29),
                 (-97, 26), (-97, 20), (-90, 16), (-83, 9), (-78, 8), (-85, 12), (-92, 15), (-105, 20), (-112, 30), (-117, 33), (-124, 40), (-125, 48),
                 (-135, 58), (-150, 60), (-165, 60)],
    "groen": [(-55, 60), (-45, 60), (-20, 70), (-20, 80), (-60, 82), (-70, 76), (-55, 68)],
    "africa": [(-17, 21), (-17, 15), (-8, 5), (5, 5), (9, 4), (10, -2), (13, -12), (12, -18), (18, -34), (26, -34), (33, -27), (40, -15), (40, -5),
               (51, 11), (43, 12), (35, 27), (32, 31), (20, 32), (10, 37), (-5, 36), (-10, 30)],
    "eurasia": [(-10, 36), (-9, 43), (-2, 44), (-5, 48), (0, 50), (8, 54), (5, 58), (10, 63), (20, 70), (30, 70), (45, 68), (60, 70), (80, 73), (100, 77),
                (120, 73), (140, 72), (160, 70), (180, 68), (180, 62), (160, 58), (142, 50), (135, 43), (122, 40), (122, 30), (110, 20), (105, 10),
                (100, 13), (98, 8), (92, 20), (80, 15), (77, 8), (72, 20), (66, 25), (57, 25), (52, 12), (43, 12), (35, 28), (36, 36), (28, 37), (26, 40),
                (20, 40), (15, 45), (12, 44), (8, 44), (3, 43), (-1, 37)],
    "australia": [(113, -22), (114, -34), (125, -33), (135, -35), (140, -38), (150, -38), (153, -28), (145, -15), (142, -11), (136, -12), (130, -12), (123, -17)],
}


def terra(W=1024, H=512):
    px = lambda lon, lat: ((lon + 180) / 360 * W, (90 - lat) / 180 * H)
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    for pts in CONT.values():
        d.polygon([px(*p) for p in pts], fill=255)
    d.rectangle([0, px(0, -70)[1], W, H], fill=255)                     # Antártida
    mask = mask.filter(ImageFilter.GaussianBlur(1.6))
    m = np.asarray(mask, float)[..., None] / 255
    y = np.linspace(-1, 1, H)[:, None, None]
    rng = np.random.default_rng(20)
    ruido = np.asarray(Image.fromarray((rng.random((H // 8, W // 8)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), float)[..., None] / 255
    oceano = np.array([0x0E, 0x22, 0x3E], float) * (0.85 + 0.25 * ruido)
    terra_ = (np.array([0x5C, 0x6E, 0x55], float) * (1 - ruido) + np.array([0x74, 0x6C, 0x52], float) * ruido)
    gelo = np.array([0xC9, 0xD3, 0xE0], float)
    polar = np.clip((np.abs(y) - 0.78) / 0.1, 0, 1)
    img = oceano * (1 - m) + terra_ * m
    img = img * (1 - polar * m) + gelo * polar * m
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def capa(W=1024, H=712, logo=True):
    # v7 §2.1: capa azul-royal profundo #17408F com a logo oficial em cores (≥ 60% da largura; textura ≥ 1024 px, sem reamostrar para cima);
    # verso branco-gelo #E8EEF8 com um X fino. Material sem iluminação (MeshBasicMaterial).
    img = Image.new("RGB", (W, H), (0x17, 0x40, 0x8F) if logo else (0xE8, 0xEE, 0xF8))
    d = ImageDraw.Draw(img)
    if logo:
        d.rectangle([18, 18, W - 19, H - 19], outline=(0xBF, 0xD8, 0xFF), width=6)
        lg = Image.open(ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png").convert("RGBA")
        a = np.asarray(lg)[..., 3]
        ys, xs = np.nonzero(a > 8)
        lg = lg.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        k = 0.72 * W / lg.width
        lg = lg.resize((int(lg.width * k), int(lg.height * k)), Image.LANCZOS)
        print("logo na capa: origem", lg.width / k, "px -> ", lg.width, "px (", round(lg.width / W * 100), "% da largura )")
        img.paste(lg, ((W - lg.width) // 2, (H - lg.height) // 2), lg)
    else:
        c = (0x9A, 0xA8, 0xC4)
        d.rectangle([18, 18, W - 19, H - 19], outline=c, width=6)
        d.line([(60, 60), (W - 60, H - 60)], fill=c, width=5)
        d.line([(W - 60, 60), (60, H - 60)], fill=c, width=5)
    return img


def uri(im, fmt="PNG"):
    b = io.BytesIO()
    im.save(b, fmt, quality=88) if fmt == "JPEG" else im.save(b, fmt)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(b.getvalue()).decode()


js = ("// gerado por gerar_texturas.py (não editar)\nwindow.TEX20 = {\n"
      f"  terra: '{uri(terra(), 'JPEG')}',\n  capa: '{uri(capa())}',\n  contra: '{uri(capa(logo=False))}'\n}};\n")
(U / "threejs" / "cena3d" / "tex20.js").write_text(js, encoding="utf-8")
terra().save(U / "renders" / "_terra_textura.png")
capa().save(U / "renders" / "_capa_livro.png")
print("tex20.js", len(js) // 1024, "KB")
