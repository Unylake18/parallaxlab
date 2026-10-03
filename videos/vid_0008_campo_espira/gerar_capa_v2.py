"""Segunda rodada de capas do vid_0008 (POR TRÁS DA FÓRMULA · EP. 03): 6 versões.

Uso, na raiz do repositório:
    uv run python videos/vid_0008_campo_espira/gerar_capa_v2.py [PASTA_SAIDA [1-6]]

Mesma base e identidade da série (reaproveita gerar_capa.py: base versionada do vid_0002,
headline em Space Grotesk com gradiente, linha de série, painel de vidro, marca e horizonte).
Novidades: espira em neon (traço em gradiente ciano → violeta → magenta com bloom em três
camadas), fórmula com termos em cor (I magenta, R ciano, z azul), cards mais ricos (triângulo,
eixo z e ponto P, gráfico com preenchimento, chips com brilho) e arte um pouco maior dentro do
painel.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(UNIT))
from gerar_capa import (BLUE, BRAND, CYAN, MAGENTA, SERIE, VIOLET, WHITE, MEDIUM, base,  # noqa: E402
                        center, glow_paste, headline_line, render_rgba, text_mask)
from comum import b_loop, mtex, tex  # noqa: E402
from template.fonts import screen_text  # noqa: E402
from PIL import ImageFont  # noqa: E402

GRAD = [CYAN, BLUE, VIOLET, MAGENTA]


# ── Peças de painel (neon) ────────────────────────────────────────────────────
def neon(pts, colors, width, back=1.0):
    """Traço em gradiente com três camadas: aura larga, corpo e núcleo claro."""
    from manim import VGroup, VMobject
    g = VGroup()
    for w, op in ((width * 2.4, 0.22), (width, 0.95), (width * 0.30, 0.95)):
        vm = VMobject().set_points_as_corners(pts)
        vm.set_stroke(color=colors if w != width * 0.30 else "#EFFFFF", width=w, opacity=op * back)
        g.add(vm)
    return g


def formula(size=60):
    return mtex(r"B_z(\vZ)", "=", r"\frac{\mu_0 \vI \vR^2}{2\left(\vR^2+\vZ^2\right)^{3/2}}", size=size)


def espira_neon(rs=1.3, tilt=0.52, com_p=False, com_eixo=False, op=1.0, axis=2.3):
    """Espira pseudo-3D em neon; opcionalmente com o eixo z, o ponto P e a seta do campo."""
    from manim import PI, Arrow, DashedLine, Dot, VGroup
    pt = lambda phi: np.array([rs * tilt * np.sin(phi), rs * np.cos(phi), 0.0])
    trás = neon([pt(p) for p in np.linspace(PI, 2 * PI, 70)], [BLUE, VIOLET, MAGENTA], 22, back=0.9 * op)
    frente = neon([pt(p) for p in np.linspace(0, PI, 70)], [MAGENTA, VIOLET, CYAN], 22, back=op)
    g = VGroup(trás, frente)
    for phi, c in ((0.7, MAGENTA), (1.6, WHITE), (2.5, CYAN)):       # pontos de energia no fio
        g.add(Dot(pt(phi), 0.15, color=c).set_opacity(op))
    if com_eixo or com_p:
        p = np.array([axis, 0, 0])
        g.add(DashedLine([-0.55, 0, 0], p + [0.6, 0, 0], dash_length=0.16).set_stroke(CYAN, 6, 0.65))
        g.add(Arrow(p, p + [0.9, 0, 0], buff=0, stroke_width=24, tip_length=0.42, color=CYAN,
                    max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=60))
        g.add(Dot(p, 0.26, color=CYAN).set_opacity(0.25), Dot(p, 0.16, color=WHITE))
        g.add(tex("P", 80, WHITE).move_to(p + [0, -0.55, 0]), tex("z", 80, BLUE).move_to([axis + 1.35, 0.5, 0]))
    return g


def triangulo_neon():
    """Triângulo R (ciano) – z (azul) – r (violeta), em neon, com os rótulos."""
    from manim import VGroup
    O, T, P = np.array([0, 0, 0.0]), np.array([0, 1.5, 0.0]), np.array([2.3, 0, 0.0])
    g = VGroup(neon([O, T], [CYAN, CYAN], 22), neon([O, P], [BLUE, BLUE], 22), neon([T, P], [VIOLET, MAGENTA], 22))
    g.add(tex("R", 95, CYAN).move_to([-0.48, 0.75, 0]), tex("z", 95, BLUE).move_to([1.15, -0.5, 0]),
          tex("r", 95, VIOLET).move_to([1.5, 1.05, 0]))
    return g


def grafico_neon(w=3.4, h=1.7, zmax=3.4, preenche=True):
    """B_z/B_z(0) contra z/R: curva em gradiente, área sutil sob o pico e o máximo em magenta."""
    from manim import Circle, Dot, Line, Polygon, VGroup
    gp = lambda z: np.array([w * z / zmax, h * float(b_loop(z)), 0.0])
    zs = np.linspace(-zmax, zmax, 260)
    pts = [gp(z) for z in zs]
    g = VGroup()
    if preenche:
        g.add(Polygon(*pts, gp(zmax) * [1, 0, 0], gp(-zmax) * [1, 0, 0]).set_stroke(width=0).set_fill(CYAN, 0.16))
    g.add(Line([-w - 0.15, 0, 0], [w + 0.15, 0, 0]).set_stroke(BLUE, 6, 0.7),
          Line([0, -0.05, 0], [0, h + 0.3, 0]).set_stroke(BLUE, 6, 0.7),
          neon(pts, [BLUE, CYAN, CYAN, BLUE], 20),
          Circle(0.34).move_to(gp(0)).set_stroke(MAGENTA, 6, 0.6), Dot(gp(0), 0.2, color=MAGENTA))
    return g


def chips():
    from manim import RIGHT, RoundedRectangle, VGroup
    itens = VGroup()
    for t, c in (("GEOMETRIA", CYAN), ("SIMETRIA", MAGENTA), ("BIOT-SAVART", VIOLET)):
        tx = screen_text(t, 40).set_color(WHITE)
        halo = RoundedRectangle(width=tx.width + 0.7, height=tx.height + 0.6, corner_radius=0.26
                                ).set_stroke(c, 16, 0.22).set_fill(c, 0)
        bg = RoundedRectangle(width=tx.width + 0.6, height=tx.height + 0.5, corner_radius=0.24
                              ).set_stroke(c, 5, 1.0).set_fill(c, 0.16)
        itens.add(VGroup(halo, bg, tx))
    return itens.arrange(RIGHT, buff=0.3)


def painel(kind):
    from manim import DOWN, LEFT, RIGHT, VGroup
    if kind == "v1":       # fórmula grande + (espira mini | gráfico com pico)
        base_ = VGroup(espira_neon(rs=0.85), grafico_neon(w=2.4, h=0.85)).arrange(RIGHT, buff=1.0, aligned_edge=DOWN)
        return VGroup(formula(76), base_).arrange(DOWN, buff=0.3)
    if kind == "v2":       # triângulo + fórmula, com a espira como aura ao fundo
        fx = VGroup(triangulo_neon(), formula(66)).arrange(RIGHT, buff=0.7)
        fundo = espira_neon(rs=1.9, op=0.38).move_to(fx.get_center())
        return VGroup(fundo, fx)
    if kind == "v3":       # espira + eixo z + P | fórmula
        return VGroup(espira_neon(rs=0.95, com_p=True, axis=1.6), formula(72)).arrange(RIGHT, buff=0.6)
    if kind == "v4":       # fórmula + chips
        return VGroup(formula(80), chips()).arrange(DOWN, buff=0.5)
    if kind == "v5":       # espira | (fórmula sobre gráfico baixo e largo)
        col = VGroup(formula(72), grafico_neon(w=2.9, h=0.85)).arrange(DOWN, buff=0.35)
        return VGroup(espira_neon(rs=1.15), col).arrange(RIGHT, buff=0.7)
    if kind == "v6":       # espira | fórmula | gráfico pequeno
        return VGroup(espira_neon(rs=0.85), formula(66), grafico_neon(w=1.5, h=1.0)).arrange(RIGHT, buff=0.45)
    raise ValueError(kind)


# ── As 6 versões: (headline, painel) ──────────────────────────────────────────
VERSOES = {
    "1": ([([("VOCÊ DECOROU", "white")], 150), ([("ESSA FÓRMULA?", "grad")], 150)], "v1"),
    "2": ([([("ELA NÃO SURGE", "white")], 150), ([("DO NADA", "grad")], 190)], "v2"),
    "3": ([([("DECORAR OU", "white")], 150), ([("CONSTRUIR?", "grad")], 190)], "v3"),
    "4": ([([("3 IDEIAS.", "white")], 150), ([("1 FÓRMULA.", "grad")], 190)], "v4"),
    "5": ([([("A FÓRMULA POR TRÁS", "white")], 124), ([("DO CAMPO", "white")], 118),
           ([("DA ESPIRA", "grad")], 124)], "v5"),
    "6": ([([("ENTENDER,", "white")], 150), ([("NÃO DECORAR", "grad")], 150)], "v6"),
}


def cover(lines, art):
    img = base()
    rows = [headline_line(seg, start) for seg, start in lines]
    gap = 22
    total = sum(r[0].height for r in rows) + gap * (len(rows) - 1)
    assert total <= 344, f"headline alta demais: {total}px"
    y = 832 - total / 2
    for mask, color, glow, _ in rows:
        img = glow_paste(img, mask, ((img.width - mask.width) // 2, int(y)), color, glow, 15, 0.5)
        y += mask.height + gap
    series = text_mask(SERIE, ImageFont.truetype(MEDIUM, 38), tracking=9)
    series = series.resize((min(series.width, 850), round(series.height * min(series.width, 850) / series.width)),
                           Image.LANCZOS)
    img = glow_paste(img, series, center(img, series, 1097), Image.new("RGB", series.size, (245, 247, 255)),
                     (60, 120, 255), 6, 0.32)
    k = min(660 / art.width, 250 / art.height)              # o painel de vidro vai de 725 × 285 px
    art = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)
    x, yy = (img.width - art.width) // 2, 1307 - art.height // 2
    full = Image.new("L", img.size, 0); full.paste(art.getchannel("A"), (x, yy))
    for raio, cor, a in ((26, (234, 99, 255), 0.20), (12, (90, 140, 255), 0.34)):   # bloom em duas camadas
        halo = full.filter(ImageFilter.GaussianBlur(raio)).point(lambda p, a=a: int(p * a))
        img = Image.composite(Image.new("RGBA", img.size, cor + (255,)), img, halo)
    img.alpha_composite(art, (x, yy))
    return img.convert("RGB")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capas_v2"
    so = sys.argv[2] if len(sys.argv) > 2 else None
    out.mkdir(parents=True, exist_ok=True)
    for nome, (lines, kind) in VERSOES.items():
        if so and nome != so:
            continue
        alvo = out / f"capa_v{nome}.png"
        cover(lines, render_rgba(lambda k=kind: painel(k), 420)).save(alvo, optimize=True)
        print(alvo)
