"""10 propostas de capa do vid_0015 (EXERCÍCIO RESOLVIDO · EP. 06): duas linhas carregadas em movimento.

Uso, na raiz do repositório:
    uv run python videos/vid_0015_linhas_carga_movimento/gerar_capas.py [PASTA_SAIDA [NUMERO]]

Conceitos e headlines vêm de capas/briefing_capas.json. Mesma base da série (símbolo, divisor, linha de série,
marca PARALLAX LAB e horizonte iguais; compositor do vid_0009 via vid_0014). As artes são desenhadas em Manim,
não geradas por imagem, para a física ficar exata. Paleta da cena: azul = linhas e v; ciano = F_E; magenta = F_B
e I; violeta = c; branco = resultante.

Regras físicas respeitadas em todas as artes: linha 1 acima da linha 2; movimento para a direita; repulsão
elétrica ciano (na linha de baixo aponta para baixo, na de cima para cima); atração magnética magenta (cada
linha puxada para a outra); a cauda de cada seta está sobre a sua linha; F_B sempre menor que F_E; nenhuma capa
afirma cancelamento em v < c; o ponto (1, 1) do gráfico é um círculo aberto.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Circle, DashedLine, Line, MathTex, RoundedRectangle, VGroup, VMobject, config,
)
from PIL import Image, ImageDraw, ImageFilter, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
_spec = importlib.util.spec_from_file_location("capa14", ROOT / "videos" / "vid_0014_momento_inercia_eixos_paralelos" / "gerar_capa.py")
c14 = importlib.util.module_from_spec(_spec)
sys.modules["capa14"] = c14
_spec.loader.exec_module(c14)
g9 = c14.g9
g9.SERIE = "EXERCÍCIO RESOLVIDO · EP. 06"
from template.fonts import screen_text  # noqa: E402  (g9 já pôs a raiz no sys.path)

CYAN, WHITE, MAGENTA, VIOLET, BLUE_L = c14.CYAN, c14.WHITE, c14.MAGENTA, c14.VIOLET, c14.BLUE_L
BLUE, MUTED, NAVY = "#267BFF", "#ADB8D1", "#0A1640"
BLUE_H = "#4E9BFF"                  # azul de headline: mais claro que o das linhas, para ler como miniatura
tx, neon, seta = c14.tx, c14.neon, c14.seta

MOLDURA_ALTA = (100, 1135, 980, 1560)


# ── Peças ───────────────────────────────────────────────────────────────────
def rotulo(s, size=40, color=MUTED):
    """Texto em linguagem natural: Space Grotesk Medium, como nas cenas (nunca MathTex)."""
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        return screen_text(s, size, color=color)
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def etiqueta(s, size=36, color=MUTED):
    """Rótulo pequeno dentro de uma pílula translúcida (MODELO IDEAL, REPULSÃO LÍQUIDA)."""
    t = rotulo(s, size, color)
    pill = RoundedRectangle(corner_radius=0.2, width=t.width + 0.55, height=t.height + 0.34)
    pill.set_stroke(color, 4, 0.85).set_fill(color, 0.08)
    return VGroup(pill, t)


def caixa(mob, cor, pad=0.38):
    """Caixa arredondada translúcida ao redor de uma expressão em destaque."""
    r = RoundedRectangle(corner_radius=0.28, width=mob.width + 2 * pad, height=mob.height + 1.4 * pad)
    r.move_to(mob).set_stroke(cor, 7, 1.0).set_fill(cor, 0.12)
    return VGroup(neon(r, cor, 7)[:2], r, mob)


def duas(W=7.2, gap=2.1, n=7, trail=False):
    """Duas linhas carregadas paralelas (1 em cima, 2 embaixo) com contas positivas.

    Devolve (grupo, y_cima, y_baixo, xs das contas). Com trail=True, cada conta ganha um rastro curto à esquerda
    (movimento para a direita).
    """
    y1, y2 = gap / 2, -gap / 2
    xs = np.linspace(-W / 2 + 0.4, W / 2 - 0.4, n)
    g = VGroup()
    for y in (y1, y2):
        g.add(neon(Line([-W / 2, y, 0], [W / 2, y, 0]), BLUE, 10))
    for y in (y1, y2):
        for x in xs:
            if trail:
                for k, (a, b, op) in enumerate(((0.28, 0.5, 0.75), (0.55, 0.72, 0.45), (0.77, 0.9, 0.22))):
                    g.add(Line([x - b, y, 0], [x - a, y, 0]).set_stroke(BLUE_L, 9 - 2 * k, op))
            c = Circle(radius=0.27).set_stroke(BLUE_L, 6).set_fill(NAVY, 1.0).move_to([x, y, 0])
            g.add(c, Line([x - 0.15, y, 0], [x + 0.15, y, 0]).set_stroke(WHITE, 6),
                  Line([x, y - 0.15, 0], [x, y + 0.15, 0]).set_stroke(WHITE, 6))
    return g, y1, y2, xs


def f_baixo(x, y, comp, cor, w=17, tip=0.42):
    """Seta que parte da linha em (x, y) e aponta para baixo."""
    return seta([x, y, 0], [x, y - comp, 0], cor, w, tip)


def f_cima(x, y, comp, cor, w=17, tip=0.42):
    """Seta que parte da linha em (x, y) e aponta para cima."""
    return seta([x, y, 0], [x, y + comp, 0], cor, w, tip)


def v_dir(x0, x1, y, cor=BLUE_H, w=15):
    return seta([x0, y, 0], [x1, y, 0], cor, w, 0.4)


def rot(s, cor, seta_, size=96, buff=0.3):
    """Rótulo à direita de uma seta vertical, centrado perto da ponta (longe das contas da linha)."""
    ini, fim = seta_.get_start(), seta_.get_end()
    sinal = 1 if fim[1] > ini[1] else -1
    m = tx(s, size, cor)
    return m.move_to([fim[0] + buff + m.width / 2, fim[1] - sinal * 0.18, 0])


def lbl(s, cor, ref, lado=RIGHT, size=96, buff=0.16):
    return tx(s, size, cor).next_to(ref, lado, buff=buff)


def v_label(setas_v, size=88):
    return [tx("v", size, BLUE_H).next_to(a, RIGHT, buff=0.18) for a in setas_v]


def forcas_baixo(y2, xe, xb, fe=1.6, fb=1.0, rotulos=True):
    """Na linha de baixo: F_E (ciano) para baixo em xe e F_B (magenta, menor) para cima em xb, com rótulos."""
    se, sb = f_baixo(xe, y2, fe, CYAN), f_cima(xb, y2, fb, MAGENTA)
    g = VGroup(se, sb)
    if rotulos:
        g.add(rot("F_E", CYAN, se), rot("F_B", MAGENTA, sb))
    return g


# ── Artes (uma por conceito do briefing) ────────────────────────────────────
def arte_1():
    """AS FORÇAS SE CANCELAM? — F_E longa e F_B curta na linha de baixo; ponto de interrogação grande."""
    d, y1, y2, _ = duas(gap=1.7)
    f = forcas_baixo(y2, -1.6, 0.53, fe=1.6, fb=1.0)
    q = tx("?", 280, WHITE).move_to([2.55, y2 - 1.15, 0])
    return VGroup(d, f, q)


def arte_2():
    """QUAL VELOCIDADE? — v igual nas duas linhas, d entre elas, 'v = ?' em caixa ciano."""
    d, y1, y2, _ = duas(gap=1.8)
    a1, a2 = v_dir(-2.4, 0.2, y1 + 0.6), v_dir(-2.4, 0.2, y2 + 0.6)
    vs = v_label([a1, a2])
    dx = 4.1
    dd = VGroup(seta([dx, y1 - 0.15, 0], [dx, y2 + 0.15, 0], WHITE, 6, 0.2),
                seta([dx, y2 + 0.15, 0], [dx, y1 - 0.15, 0], WHITE, 6, 0.2),
                tx("d", 90, WHITE).move_to([dx + 0.45, 0, 0]))
    q = tx(r"v\,=\,?", 200, WHITE)
    q[0][0].set_color(BLUE_H)
    q[0][2].set_color(CYAN)
    return VGroup(VGroup(d, a1, a2, *vs, dd), caixa(q, CYAN)).arrange(DOWN, buff=0.4)


def arte_3():
    """ATRAÇÃO OU REPULSÃO? — em cada linha, F_B (magenta, curta) aponta para a outra e F_E (ciano, longa) para fora."""
    d, y1, y2, _ = duas(gap=2.2)
    xe, xb = -2.67, 0.53
    ge = VGroup(f_baixo(xe, y2, 1.2, CYAN), f_cima(xe, y1, 1.2, CYAN))
    gb = VGroup(f_cima(xb, y2, 0.8, MAGENTA), f_baixo(xb, y1, 0.8, MAGENTA))
    ls = VGroup(rot("F_E", CYAN, ge[0], 90), rot("F_E", CYAN, ge[1], 90),
                rot("F_B", MAGENTA, gb[0], 90), rot("F_B", MAGENTA, gb[1], 90))
    leg = rotulo("duas linhas carregadas", 46, MUTED)
    return VGroup(VGroup(d, ge, gb, ls), leg).arrange(DOWN, buff=0.5)


def arte_4():
    """ELÉTRICA × MAGNÉTICA — 'F_E × F_B' grande; abaixo, as duas linhas com F_E ↓ longa e F_B ↑ curta."""
    comp = MathTex("F_E", r"\times", "F_B", font_size=230, color=WHITE)
    comp[0].set_color(CYAN)
    comp[2].set_color(MAGENTA)
    d, y1, y2, _ = duas(gap=1.5)
    f = forcas_baixo(y2, -1.6, 0.53, fe=1.3, fb=0.85, rotulos=False)
    return VGroup(comp, VGroup(d, f)).arrange(DOWN, buff=0.45)


def arte_5():
    """SÓ NA VELOCIDADE DA LUZ? — 'v = c' em caixa; abaixo, as linhas em movimento; 'cancelamento exato?'."""
    q = tx(r"v\,=\,c", 250, WHITE)
    q[0][0].set_color(BLUE_H)
    q[0][2].set_color(VIOLET)
    box = RoundedRectangle(corner_radius=0.28, width=q.width + 0.9, height=q.height + 0.55).move_to(q)
    box.set_stroke(VIOLET, 7).set_fill(VIOLET, 0.13)
    caixa_q = VGroup(neon(box.copy(), VIOLET, 7)[:2], box, q)
    d, y1, y2, _ = duas(gap=1.5)
    a1, a2 = v_dir(-2.2, 0.4, y1 + 0.58), v_dir(-2.2, 0.4, y2 + 0.58)
    leg = rotulo("cancelamento exato?", 44, MUTED)
    return VGroup(caixa_q, VGroup(d, a1, a2, *v_label([a1, a2], 76)), leg).arrange(DOWN, buff=0.45)


def arte_6():
    """A CORRENTE PODE VENCER? — setas I (magenta) para a direita; F_E ↓ longa e F_B ↑ curta na linha de baixo."""
    d, y1, y2, _ = duas(gap=1.9)
    i1 = seta([-2.4, y1 + 0.6, 0], [0.4, y1 + 0.6, 0], MAGENTA, 15, 0.4)
    i2 = seta([0.0, y2 - 0.6, 0], [2.4, y2 - 0.6, 0], MAGENTA, 15, 0.4)
    li = VGroup(lbl("I", MAGENTA, i1, RIGHT, 84, 0.18), lbl("I", MAGENTA, i2, RIGHT, 84, 0.18))
    f = forcas_baixo(y2, -2.67, -1.6, fe=1.5, fb=0.95)
    return VGroup(d, i1, i2, li, f)


def arte_7():
    """QUASE… MAS NÃO! — F_B quase igual a F_E, mas menor; resultante branca para baixo, em outro ponto; MODELO IDEAL."""
    d, y1, y2, _ = duas(gap=1.9)
    fe, fb = 1.85, 1.3
    f = forcas_baixo(y2, -2.67, -1.6, fe=fe, fb=fb)
    res = f_baixo(1.6, y2, fe - fb, WHITE, 15, 0.28)
    rl = tx(r"F_{\mathrm{liq}}>0", 84, WHITE).move_to([2.25, y2 - 0.8, 0])
    tag = etiqueta("MODELO IDEAL", 40, MUTED)
    return VGroup(VGroup(d, f, res, rl), tag).arrange(DOWN, buff=0.45)


def arte_8():
    """MOVER AS CARGAS MUDA TUDO? — rastros atrás das contas, v azul, F_E ↓ longa e F_B ↑ curta."""
    d, y1, y2, _ = duas(gap=1.9, trail=True)
    a1 = v_dir(-2.4, 0.4, y1 + 0.6)
    a2 = v_dir(0.0, 2.4, y2 - 0.6)
    vs = VGroup(*v_label([a1, a2]))
    f = forcas_baixo(y2, -2.67, -1.6, fe=1.5, fb=0.95)
    return VGroup(d, a1, a2, vs, f)


def arte_9():
    """POR QUE NÃO CANCELA? — 'F_B < F_E' grande; abaixo, linhas com a força líquida branca para baixo."""
    comp = MathTex("F_B", "<", "F_E", font_size=230, color=WHITE)
    comp[0].set_color(MAGENTA)
    comp[2].set_color(CYAN)
    d, y1, y2, _ = duas(gap=1.4)
    net = f_baixo(0.53, y2, 1.1, WHITE, 17, 0.42)
    nl = tx(r"F_{\mathrm{liq}}", 90, WHITE).move_to([1.75, y2 - 0.85, 0])
    tag = etiqueta("REPULSÃO LÍQUIDA", 38, MUTED)
    return VGroup(comp, VGroup(d, net, nl), tag).arrange(DOWN, buff=0.4)


def arte_10():
    """DUAS LINHAS. UM LIMITE. — linhas em movimento e a parábola (v/c)² terminando em círculo aberto em (1, 1)."""
    d, y1, y2, _ = duas(gap=1.0)
    a1, a2 = v_dir(-1.0, 1.2, y1 + 0.55, BLUE_H, 11), v_dir(-1.0, 1.2, y2 - 0.55, BLUE_H, 11)
    topo = VGroup(d, a1, a2)
    w, h = 4.6, 2.8
    gp = lambda u: np.array([w * u, h * u * u, 0.0])
    r = 0.15
    # a curva para antes do círculo aberto (o ponto final fica visivelmente vazio)
    fim = max(u for u in np.linspace(0.8, 1.0, 400) if np.linalg.norm(gp(u) - gp(1.0)) > r + 0.06)
    curva = VMobject().set_points_as_corners([gp(u) for u in np.linspace(0, fim, 160)]).set_stroke(CYAN, 12)
    eixos = VGroup(Line([0, 0, 0], [w + 0.35, 0, 0]).set_stroke(BLUE_L, 6, 0.9),
                   Line([0, 0, 0], [0, h + 0.35, 0]).set_stroke(BLUE_L, 6, 0.9))
    guia = DashedLine(gp(1.0) * [1, 0, 0], gp(1.0) - [0, r, 0], dash_length=0.14).set_stroke(VIOLET, 5, 0.8)
    aberto = Circle(radius=r).set_stroke(VIOLET, 7).set_fill(VIOLET, 0).move_to(gp(1.0))
    cl = tx(r"v=c", 96, VIOLET).next_to(aberto, LEFT, buff=0.3).shift(UP * 0.1)
    xl = tx(r"v/c", 80, WHITE).next_to(eixos[0], DOWN, buff=0.12, aligned_edge=RIGHT)
    graf = VGroup(eixos, curva, guia, aberto, cl, xl)
    tag = etiqueta("MODELO IDEAL", 36, MUTED).next_to(graf, LEFT, buff=0.5).align_to(graf, UP).shift(DOWN * 0.1)
    return VGroup(topo, VGroup(graf, tag)).arrange(DOWN, buff=0.5)


# headline por linhas: [(texto, tipo)], tipo ∈ white | grad | cyan | magenta | violet | blue
HEADLINES = {
    1: [[("AS FORÇAS", "white")], [("SE CANCELAM?", "grad")]],
    2: [[("QUAL", "white")], [("VELOCIDADE?", "grad")]],
    3: [[("ATRAÇÃO", "white")], [("OU", "white")], [("REPULSÃO?", "grad")]],
    4: [[("ELÉTRICA", "cyan")], [("×", "white")], [("MAGNÉTICA", "magenta")]],
    5: [[("SÓ NA", "white")], [("VELOCIDADE", "white")], [("DA LUZ?", "violet")]],
    6: [[("A CORRENTE", "white")], [("PODE", "white")], [("VENCER?", "magenta")]],
    7: [[("QUASE…", "white")], [("MAS NÃO!", "cyan")]],
    8: [[("MOVER", "blue"), (" AS", "white")], [("CARGAS MUDA", "white")], [("TUDO?", "grad")]],
    9: [[("POR QUE", "white")], [("NÃO", "white")], [("CANCELA?", "cyan")]],
    10: [[("DUAS LINHAS.", "white")], [("UM LIMITE.", "violet")]],
}
ARTES = {1: arte_1, 2: arte_2, 3: arte_3, 4: arte_4, 5: arte_5, 6: arte_6, 7: arte_7, 8: arte_8, 9: arte_9,
         10: arte_10}
MOLDURA = {1: True, 2: True, 3: True, 4: False, 5: False, 6: True, 7: True, 8: True, 9: False, 10: False}
SOLIDAS = {"cyan": (53, 217, 255), "magenta": (234, 99, 255), "violet": (156, 140, 255), "blue": (78, 155, 255),
           "white": (255, 255, 255)}


# ── Composição ──────────────────────────────────────────────────────────────
def linha_headline(segs, size):
    """Como g9.headline_line, mas com tamanho dado e cores sólidas além do gradiente da marca."""
    full = "".join(t for t, _ in segs)
    font = ImageFont.truetype(g9.BOLD, size)
    raw = Image.new("L", (int(font.getlength(full)) + 8, sum(font.getmetrics()) + 8), 0)
    ImageDraw.Draw(raw).text((4, 4), full, font=font, fill=255)
    box = raw.getbbox()
    mask = raw.crop(box)
    color = Image.new("RGB", mask.size, (255, 255, 255))
    x = 4
    for t, kind in segs:
        w = font.getlength(t)
        x0, x1 = max(0, int(x - box[0])), min(mask.width, int(x + w - box[0]) + 2)
        if kind == "grad":
            color.paste(g9.gradient((x1 - x0, mask.height), g9.BRAND), (x0, 0))
        elif kind != "white":
            color.paste(Image.new("RGB", (x1 - x0, mask.height), SOLIDAS[kind]), (x0, 0))
        x += w
    tipo = {k for _, k in segs}
    if "grad" in tipo:
        glow = (110, 90, 255)
    elif tipo - {"white"}:
        glow = tuple(int(c * 0.55) for c in SOLIDAS[next(iter(tipo - {"white"}))])
    else:
        glow = (70, 140, 255)
    return mask, color, glow


def montar_headline(n):
    """Tamanho único para todas as linhas: o maior que cabe em 870 px de largura e 340 px de altura."""
    linhas = HEADLINES[n]
    textos = ["".join(t for t, _ in seg) for seg in linhas]
    size = min(g9.fit(t, g9.BOLD, 870, 150).size for t in textos)
    gap = 22
    while True:
        rows = [linha_headline(seg, size) for seg in linhas]
        total = sum(r[0].height for r in rows) + gap * (len(rows) - 1)
        if total <= 300:
            return rows, total, gap
        size -= 3


def compor(n):
    com_moldura = MOLDURA[n]
    velha_moldura, velha_func = g9.MOLDURA, g9.desenhar_moldura
    if com_moldura:
        g9.MOLDURA = MOLDURA_ALTA
    else:
        g9.desenhar_moldura = lambda img, cantos: img            # sem moldura: só o fundo apagado
    try:
        arte = g9.render_rgba(lambda: ARTES[n]().move_to([0, 0, 0]), 520)
        img = g9.base()
    finally:
        g9.MOLDURA, g9.desenhar_moldura = velha_moldura, velha_func
    rows, total, gap = montar_headline(n)
    y = 826 - total / 2
    for mask, color, glow in rows:
        img = g9.glow_paste(img, mask, ((img.width - mask.width) // 2, int(y)), color, glow, 15, 0.5)
        y += mask.height + gap
    serie = g9.text_mask(g9.SERIE, ImageFont.truetype(g9.MEDIUM, 38), tracking=9)
    serie = serie.resize((min(serie.width, 850), round(serie.height * min(serie.width, 850) / serie.width)), Image.LANCZOS)
    img = g9.glow_paste(img, serie, g9.center(img, serie, 1097), Image.new("RGB", serie.size, (245, 247, 255)),
                        (60, 120, 255), 6, 0.32)
    caixa_px = (810, 380) if com_moldura else (900, 420)
    k = min(caixa_px[0] / arte.width, caixa_px[1] / arte.height)
    arte = arte.resize((round(arte.width * k), round(arte.height * k)), Image.LANCZOS)
    x, yy = (img.width - arte.width) // 2, (1347 if com_moldura else 1345) - arte.height // 2
    cheio = Image.new("L", img.size, 0)
    cheio.paste(arte.getchannel("A"), (x, yy))
    halo = cheio.filter(ImageFilter.GaussianBlur(12)).point(lambda p: int(p * 0.35))
    img = Image.composite(Image.new("RGBA", img.size, (90, 110, 255, 255)), img, halo)
    img.alpha_composite(arte, (x, yy))
    return img.convert("RGB")


def grade(pasta, arquivos):
    """Contact sheet 2×5 em miniatura, para avaliar a leitura em tamanho de celular."""
    imgs = [Image.open(p).convert("RGB") for p in arquivos]
    w = 540
    h = round(imgs[0].height * w / imgs[0].width)
    cols, rows = 5, 2
    sheet = Image.new("RGB", (cols * w + (cols + 1) * 10, rows * h + (rows + 1) * 10), (24, 24, 24))
    for i, im in enumerate(imgs):
        sheet.paste(im.resize((w, h), Image.LANCZOS), (10 + (i % cols) * (w + 10), 10 + (i // cols) * (h + 10)))
    alvo = pasta / "grade_2x5.png"
    sheet.save(alvo, optimize=True)
    return alvo


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capas_manim"
    out.mkdir(parents=True, exist_ok=True)
    so = int(sys.argv[2]) if len(sys.argv) > 2 else None
    feitos = []
    for n in ARTES:
        if so and n != so:
            continue
        alvo = out / f"capa_{n:02d}.png"
        compor(n).save(alvo, optimize=True)
        feitos.append(alvo)
        print(alvo)
    if not so:
        print(grade(out, feitos))
