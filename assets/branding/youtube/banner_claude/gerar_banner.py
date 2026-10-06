"""Banner do canal Parallax Lab no YouTube (2560×1440) — 3 variações, guias de área segura e prévia de recortes.

Uso, na raiz do repositório (precisa só de Pillow e numpy):
    uv run python assets/branding/youtube/banner_claude/gerar_banner.py

Marca: símbolo oficial (master/parallax_lab_icon_transparent.png) e logotipo oficial PARALLAX LAB recortado do
lockup horizontal (overlays/parallax_lab_watermark.png), sem redesenho; só a proporção entre símbolo e logotipo
muda de uma variação para outra. Assinatura em Space Grotesk, linha secundária em Inter. Fundo: o banner 16:9
oficial (social/parallax_lab_banner_16x9.png) com o lockup central apagado e a faixa central escurecida.

Área segura (todas as telas): 1546×423 centrada, de (507, 508) a (2053, 931). Tablet: 1855×423; desktop: 2560×423;
TV: a imagem toda. Todo o conteúdo essencial fica dentro da área segura, com folga; as bordas só têm atmosfera.
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[3]
BR = ROOT / "assets" / "branding"
FONTES = ROOT / "assets" / "fonts"
SG_BOLD = str(FONTES / "space_grotesk" / "SpaceGrotesk-Bold.ttf")
SG_MED = str(FONTES / "space_grotesk" / "SpaceGrotesk-Medium.ttf")
INTER = str(FONTES / "inter" / "Inter-Regular.ttf")
INTER_MED = str(FONTES / "inter" / "Inter-Medium.ttf")

W, H = 2560, 1440
SEGURA = (507, 508, 2053, 931)
TABLET = (352, 508, 2208, 931)
DESKTOP = (0, 508, 2560, 931)
CX, CY = W // 2, (SEGURA[1] + SEGURA[3]) // 2

CYAN, WHITE, CINZA = (0x35, 0xD9, 0xFF), (0xF5, 0xF7, 0xFF), (0xB4, 0xBC, 0xD6)
BRAND = [(0x35, 0xD9, 0xFF), (0x26, 0x7B, 0xFF), (0x74, 0x5C, 0xFF), (0xEA, 0x63, 0xFF)]
HEADLINE = "FÍSICA E MATEMÁTICA POR OUTRA PERSPECTIVA"
LINHA2 = ["Intuição", "Visualização", "Rigor"]


# ── Marca oficial ─────────────────────────────────────────────────────────────
def simbolo(altura):
    im = Image.open(BR / "master" / "parallax_lab_icon_transparent.png").convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    return im.resize((round(im.width * altura / im.height), altura), Image.LANCZOS)


def logotipo(altura):
    """PARALLAX LAB do lockup horizontal oficial (x 673–1935, y 328–419 com alfa > 40), com margem para o brilho."""
    im = Image.open(BR / "overlays" / "parallax_lab_watermark.png").convert("RGBA")
    im = im.crop((655, 312, 1955, 436))
    alvo = altura * im.height / 91                       # altura pedida = altura das letras
    return im.resize((round(im.width * alvo / im.height), round(alvo)), Image.LANCZOS)


# ── Fundo ─────────────────────────────────────────────────────────────────────
def fundo_cosmico():
    img = Image.open(BR / "social" / "parallax_lab_banner_16x9.png").convert("RGB")
    arr = np.asarray(img).astype(np.float32)
    soft = np.asarray(img.filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(12))).astype(np.float32)
    x0, x1, y0, y1 = 495, 1195, 150, 740                     # lockup do banner de origem
    h, w = y1 - y0, x1 - x0
    topo, base, esq, dir_ = soft[y0, x0:x1], soft[y1 - 1, x0:x1], soft[y0:y1, x0], soft[y0:y1, x1 - 1]
    u = np.linspace(0, 1, w)[None, :, None]
    v = np.linspace(0, 1, h)[:, None, None]
    cantos = (1 - v) * ((1 - u) * topo[0] + u * topo[-1]) + v * ((1 - u) * base[0] + u * base[-1])
    bg = (1 - v) * topo[None] + v * base[None] + (1 - u) * esq[:, None] + u * dir_[:, None] - cantos
    jan = lambda n, f: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / f, 0, 1)
    fe = np.outer(jan(h, 40), jan(w, 40))[..., None]
    arr[y0:y1, x0:x1] = arr[y0:y1, x0:x1] * (1 - fe) + bg * fe
    img = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    return estrelas(img, 0.0009, 3)


def fundo_liso():
    """Quase sólido #050816 com brilho ciano/violeta muito leve nas laterais (minimalista)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.zeros((H, W, 3), np.float32) + np.array([5, 8, 22])
    for cx, cy, cor, k in ((-150, 400, (0x26, 0x7B, 0xFF), 0.22), (W + 150, 1050, (0x74, 0x5C, 0xFF), 0.22)):
        d = np.exp(-(((xx - cx) / 900) ** 2 + ((yy - cy) / 650) ** 2))
        base += d[..., None] * np.array(cor) * k
    return estrelas(Image.fromarray(base.clip(0, 255).astype(np.uint8)), 0.0005, 11)


def estrelas(img, dens, seed):
    rng = np.random.default_rng(seed)
    st = np.zeros((H, W), np.float32)
    idx = rng.random(st.shape) < dens
    st[idx] = rng.uniform(40, 200, idx.sum()) ** 1.0
    st = np.asarray(Image.fromarray(st.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32) * 2.2
    a = np.asarray(img).astype(np.float32) + st[..., None] * np.array([0.78, 0.86, 1.0])
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def faixa_calma(img, forca=0.55, rx=1100, ry=330):
    """Escurece suavemente o miolo da área segura para o texto não brigar com a nebulosa."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.exp(-(((xx - CX) / rx) ** 4 + ((yy - CY) / ry) ** 2))
    a = np.asarray(img).astype(np.float32) * (1 - forca * d[..., None])
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


# ── Texto ─────────────────────────────────────────────────────────────────────
def gradiente(w, h, stops):
    seg = np.clip(np.linspace(0, 1, w) * (len(stops) - 1), 0, len(stops) - 1 - 1e-6)
    i = seg.astype(int)
    f = (seg - i)[:, None]
    row = (np.array(stops)[i] * (1 - f) + np.array(stops)[i + 1] * f).astype(np.uint8)
    return Image.fromarray(np.repeat(row[None], h, 0), "RGB")


def texto(t, fonte, size, track=0):
    """Máscara recortada do texto, mais a distância do topo da máscara ao topo das maiúsculas e a altura delas."""
    f = ImageFont.truetype(fonte, size)
    larg = sum(f.getlength(c) + track for c in t) - track
    raw = Image.new("L", (int(larg) + 40, int(size * 1.8)), 0)
    d = ImageDraw.Draw(raw)
    x = 20
    for c in t:
        d.text((x, 20), c, font=f, fill=255)
        x += f.getlength(c) + track
    hb = f.getbbox("H")
    bb = raw.getbbox()
    top = min(bb[1], 20 + hb[1])
    return raw.crop((bb[0], top, bb[2], max(bb[3], 20 + hb[3]))), 20 + hb[1] - top, hb[3] - hb[1]


def pintar(img, mask, cor, x, y_cap, off, brilho=None, raio=14, alfa=0.35):
    """Cola a máscara com o topo das maiúsculas em y_cap; `cor` é RGB ou uma imagem (gradiente)."""
    pos = (int(x), int(y_cap - off))
    cheio = Image.new("L", (W, H), 0)
    cheio.paste(mask, pos)
    out = img.convert("RGBA")
    if brilho:
        halo = cheio.filter(ImageFilter.GaussianBlur(raio)).point(lambda p: int(p * alfa))
        out = Image.composite(Image.new("RGBA", (W, H), brilho + (255,)), out, halo)
    tinta = Image.new("RGBA", (W, H), (cor if isinstance(cor, tuple) else (0, 0, 0)) + (255,))
    if not isinstance(cor, tuple):
        tinta = Image.new("RGBA", (W, H))
        tinta.paste(cor.convert("RGBA"), pos)
    out = Image.composite(tinta, out, cheio)
    return out.convert("RGB"), (pos[0], pos[1], pos[0] + mask.width, pos[1] + mask.height)


def colar_rgba(img, im, x, y, halo=None, raio=30, alfa=0.35):
    out = img.convert("RGBA")
    if halo:
        a = Image.new("L", (W, H), 0)
        a.paste(im.getchannel("A"), (int(x), int(y)))
        h = a.filter(ImageFilter.GaussianBlur(raio)).point(lambda p: int(p * alfa))
        out = Image.composite(Image.new("RGBA", (W, H), halo + (255,)), out, h)
    out.alpha_composite(im, (int(x), int(y)))
    return out.convert("RGB"), (int(x), int(y), int(x) + im.width, int(y) + im.height)


def linha_secundaria(img, size, cx=None, x=None, y_cap=0, cor=CINZA, fonte=INTER):
    """Intuição • Visualização • Rigor: palavras em cinza claro, separadores em ciano."""
    f = ImageFont.truetype(fonte, size)
    sep = "   •   "
    partes = []
    for i, p in enumerate(LINHA2):
        if i:
            partes.append((sep, CYAN))
        partes.append((p, cor))
    total = sum(f.getlength(t) for t, _ in partes)
    x0 = cx - total / 2 if cx is not None else x
    caixas = []
    hb = f.getbbox("H")
    for t, c in partes:
        d_img = Image.new("L", (int(f.getlength(t)) + 10, int(size * 1.6)), 0)
        ImageDraw.Draw(d_img).text((0, 0), t, font=f, fill=255)
        img, cx_ = pintar(img, d_img, c, x0, y_cap, hb[1])
        caixas.append(cx_)
        x0 += f.getlength(t)
    return img, (min(c[0] for c in caixas), y_cap, max(c[2] for c in caixas), y_cap + hb[3] - hb[1])


# ── Variações ─────────────────────────────────────────────────────────────────
def v01_institucional():
    """Lockup horizontal centrado, assinatura em linha única e linha secundária."""
    img = faixa_calma(fundo_cosmico(), 0.6)
    s, lg = simbolo(212), logotipo(80)
    gap = 64
    larg = s.width + gap + lg.width
    x = CX - larg / 2
    topo = SEGURA[1] + 28
    img, b1 = colar_rgba(img, s, x, topo, (70, 110, 255), 40, 0.30)
    img, b2 = colar_rgba(img, lg, x + s.width + gap, topo + s.height / 2 - lg.height / 2, (60, 120, 255), 18, 0.25)
    m, off, cap = texto(HEADLINE, SG_MED, 54, 4)
    y = topo + s.height + 46
    img, b3 = pintar(img, m, CYAN, CX - m.width / 2, y, off, (30, 140, 255), 12, 0.35)
    img, b4 = linha_secundaria(img, 38, cx=CX, y_cap=y + cap + 36)
    return img, [b1, b2, b3, b4]


def v02_cinematografica():
    """Símbolo grande à esquerda, texto à direita em duas linhas."""
    img = faixa_calma(fundo_cosmico(), 0.55, 1150, 360)
    s = simbolo(350)
    xs = SEGURA[0] + 90
    img, b1 = colar_rgba(img, s, xs, CY - s.height / 2, (70, 110, 255), 60, 0.40)
    xt = xs + s.width + 90
    lg = logotipo(68)
    m1, off1, cap1 = texto("FÍSICA E MATEMÁTICA", SG_BOLD, 66, 2)
    m2, off2, cap2 = texto("POR OUTRA PERSPECTIVA", SG_BOLD, 66, 2)
    bloco = lg.height + 44 + cap1 + 28 + cap2 + 44 + 27
    y = CY - bloco / 2
    img, b2 = colar_rgba(img, lg, xt - 18, y - 14, (60, 120, 255), 18, 0.25)
    y += lg.height + 44 - 28
    img, b3 = pintar(img, m1, WHITE, xt, y, off1, (60, 120, 255), 12, 0.25)
    y += cap1 + 28
    img, b4 = pintar(img, m2, gradiente(m2.width, m2.height, BRAND[:3]), xt, y, off2, (60, 110, 255), 14, 0.35)
    y += cap2 + 44
    img, b5 = linha_secundaria(img, 36, x=xt, y_cap=y)
    return img, [b1, b2, b3, b4, b5]


def v03_minimalista():
    """Só tipografia: logotipo grande, filete em gradiente, assinatura espaçada e linha secundária."""
    img = fundo_liso()
    lg = logotipo(104)
    y = SEGURA[1] + 52
    img, b1 = colar_rgba(img, lg, CX - lg.width / 2, y, (60, 120, 255), 26, 0.30)
    y += lg.height + 36
    fil = gradiente(520, 4, BRAND)
    img.paste(fil, (CX - 260, int(y)))
    y += 46
    m, off, cap = texto(HEADLINE, SG_MED, 48, 6)
    img, b2 = pintar(img, m, WHITE, CX - m.width / 2, y, off, (60, 120, 255), 10, 0.25)
    img, b3 = linha_secundaria(img, 36, cx=CX, y_cap=y + cap + 36)
    # filetes de paralaxe nas bordas, fora da área segura
    d = ImageDraw.Draw(img)
    for i, dy in enumerate((-36, 0, 36)):
        a = (90 - 25 * i)
        d.line((140 + 40 * i, CY + dy, 420 + 40 * i, CY + dy), fill=(0x35 * a // 100, 0xD9 * a // 100, 0xFF * a // 100), width=2)
        d.line((W - 420 - 40 * i, CY + dy, W - 140 - 40 * i, CY + dy), fill=(0x74 * a // 100, 0x5C * a // 100, 0xFF * a // 100),
               width=2)
    return img, [b1, b2, b3]


def v04_minimalista_cosmico():
    """Layout da 03 sobre o fundo cósmico do canal: logotipo oficial; assinatura e linha secundária em Space Grotesk."""
    img = faixa_calma(fundo_cosmico(), 0.6, 1150, 330)
    lg = logotipo(104)
    y = SEGURA[1] + 52
    img, b1 = colar_rgba(img, lg, CX - lg.width / 2, y, (60, 120, 255), 26, 0.35)
    y += lg.height + 36
    img.paste(gradiente(520, 4, BRAND), (CX - 260, int(y)))
    y += 46
    m, off, cap = texto(HEADLINE, SG_MED, 48, 6)
    img, b3 = pintar(img, m, WHITE, CX - m.width / 2, y, off, (60, 120, 255), 10, 0.25)
    img, b4 = linha_secundaria(img, 36, cx=CX, y_cap=y + cap + 36, fonte=SG_MED)
    d = ImageDraw.Draw(img)
    for i, dy in enumerate((-36, 0, 36)):
        a = (90 - 25 * i)
        d.line((140 + 40 * i, CY + dy, 420 + 40 * i, CY + dy), fill=(0x35 * a // 100, 0xD9 * a // 100, 0xFF * a // 100), width=2)
        d.line((W - 420 - 40 * i, CY + dy, W - 140 - 40 * i, CY + dy), fill=(0x74 * a // 100, 0x5C * a // 100, 0xFF * a // 100),
               width=2)
    return img, [b1, b3, b4]


VARIACOES = {"banner_01_institucional": v01_institucional, "banner_02_cinematografico": v02_cinematografica,
             "banner_03_minimalista": v03_minimalista, "banner_04_minimalista_cosmico": v04_minimalista_cosmico}


# ── Guias e prévias (só revisão) ──────────────────────────────────────────────
def guia(img):
    out = img.convert("RGBA")
    veu = Image.new("L", (W, H), 150)
    ImageDraw.Draw(veu).rectangle(DESKTOP, fill=70)
    ImageDraw.Draw(veu).rectangle(SEGURA, fill=0)
    out = Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), out, veu)
    d = ImageDraw.Draw(out)
    f = ImageFont.truetype(INTER_MED, 30)
    for box, cor, nome in ((SEGURA, (80, 255, 140), "ÁREA SEGURA 1546×423 (todas as telas)"),
                           (TABLET, (255, 200, 80), "TABLET 1855×423"),
                           (DESKTOP, (255, 120, 120), "DESKTOP 2560×423"),
                           ((0, 0, W - 1, H - 1), (150, 170, 255), "TV 2560×1440")):
        d.rectangle(box, outline=cor, width=4)
        ty = {"Á": box[3] + 10, "T": box[3] - 44}.get(nome[0], box[1] + 10 if box[1] > 0 else 14)
        d.text((box[0] + 14, ty), nome, font=f, fill=cor)
    return out.convert("RGB")


def previa(imgs, destino):
    """Faixa de desktop (2560×423) e recorte do celular (1546×423) de cada variação, lado a lado."""
    dw, mw, m = 1500, 700, 40
    dh, mh = round(423 * dw / 2560), round(423 * mw / 1546)
    f = ImageFont.truetype(INTER_MED, 30)
    folha = Image.new("RGB", (dw + mw + 3 * m, len(imgs) * (dh + 90) + m), (10, 12, 20))
    d = ImageDraw.Draw(folha)
    for i, (nome, im) in enumerate(imgs.items()):
        y = m + i * (dh + 90)
        d.text((m, y), f"{nome}  ·  desktop (2560×423)  |  celular (1546×423)", font=f, fill=(225, 230, 245))
        folha.paste(im.crop(DESKTOP).resize((dw, dh), Image.LANCZOS), (m, y + 44))
        folha.paste(im.crop(SEGURA).resize((mw, mh), Image.LANCZOS), (2 * m + dw, y + 44))
    folha.save(destino)


def main():
    qa, imgs = {}, {}
    folga = 20
    for nome, fn in VARIACOES.items():
        img, caixas = fn()
        assert img.size == (W, H)
        for b in caixas:
            assert (b[0] >= SEGURA[0] + folga and b[1] >= SEGURA[1] + folga and b[2] <= SEGURA[2] - folga
                    and b[3] <= SEGURA[3] - folga), f"{nome}: {b} fora da área segura"
        img.save(AQUI / f"{nome}.png", optimize=True)
        guia(img).save(AQUI / f"{nome}_guia.png", optimize=True)
        imgs[nome] = img
        qa[nome] = {"resolucao": list(img.size), "bytes": (AQUI / f"{nome}.png").stat().st_size,
                    "conteudo": [[int(v) for v in b] for b in caixas], "folga_min_px": folga}
        print(f"{nome}.png: {qa[nome]['bytes'] / 1e6:.2f} MB")
    previa(imgs, AQUI / "previa_recortes.png")
    (AQUI / "qa_banner.json").write_text(json.dumps(qa, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
