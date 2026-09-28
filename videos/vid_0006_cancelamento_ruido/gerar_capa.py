"""Gera capa_instagram.png do vid_0006 (DA EQUAÇÃO AO FENÔMENO · EP. 02).

Uso, na raiz do repositório:
    uv run python videos/vid_0006_cancelamento_ruido/gerar_capa.py [SAIDA.png]

Mesmo layout das capas do vid_0005/vid_0003: base versionada
videos/vid_0002_integral_substituicao/capa_instagram.png, da qual se apagam título,
linha de série e interior do painel; fundo, símbolo, divisor, borda do painel,
marca e horizonte são preservados. Headline (provisória, ainda em aberto):
“O SOM PODE / CANCELAR O SOM?”. Painel: ruído (ciano) + fone (magenta) → resíduo
branco pequeno, calculados com as mesmas funções da cena, e p₁ + p₂.

Variantes da rodada A/B/C (nenhuma escolhida):
    uv run python videos/vid_0006_cancelamento_ruido/gerar_capa.py videos/vid_0006_cancelamento_ruido/capa_variante_a_som_cancela_som.png a
    … capa_variante_b_onda_cancela_onda.png b · … capa_variante_c_fisica_anc.png c

Fontes: Space Grotesk versionada em assets/fonts/; matemática em MathTex.
"""
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(ROOT))
from template.fonts import SPACE_GROTESK  # noqa: E402
sys.path.insert(0, str(UNIT))
from cena import fone, noise, residual  # noqa: E402  mesmas funções da cena
from cena import text as scene_text  # noqa: E402  (importar antes do tempconfig)

BASE = UNIT.parent / "vid_0002_integral_substituicao" / "capa_instagram.png"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capa_instagram.png"
VARIANTE = sys.argv[2] if len(sys.argv) > 2 else "a"       # a (escolhida) · b · c · ondas (1ª versão) · fone · equacao · fone_rotulos · hero · antes_depois · opostas
TMP_MEDIA = ROOT / "media" / "_capa_vid0006_tmp"   # LaTeX falha em caminhos curtos (~) do Temp
BOLD, MEDIUM = str(SPACE_GROTESK["bold"]), str(SPACE_GROTESK["medium"])
BRAND = [(0x35, 0xD9, 0xFF), (0x26, 0x7B, 0xFF), (0x74, 0x5C, 0xFF), (0xEA, 0x63, 0xFF)]
PALE = [(0xC8, 0xF4, 0xFF), (0xD8, 0xDD, 0xFF), (0xE6, 0xC4, 0xFF)]


def render_rgba(build, height):
    """Renderiza mobjects do Manim em fundo transparente, recortados, com a altura pedida."""
    from manim import Scene, tempconfig

    class Quadro(Scene):
        def construct(self):
            group = build()
            group.scale_to_fit_height(6)
            if group.width > 15:
                group.scale_to_fit_width(15)
            self.add(group)

    with tempconfig({"frame_width": 16, "frame_height": 9, "pixel_width": 3200,
                     "pixel_height": 1800, "transparent": True, "format": "png",
                     "save_last_frame": True, "write_to_movie": False,
                     "media_dir": str(TMP_MEDIA), "verbosity": "WARNING",
                     "disable_caching": True, "output_file": "quadro"}):
        scene = Quadro()
        scene.render()
        image = Image.open(scene.renderer.file_writer.image_file_path).convert("RGBA")
    shutil.rmtree(TMP_MEDIA, ignore_errors=True)
    image = image.crop(image.getchannel("A").getbbox())
    return image.resize((round(image.width * height / image.height), height), Image.LANCZOS)


def tex_mask(content, height):
    """MathTex → máscara L (para receber o gradiente pálido das capas)."""
    from manim import MathTex
    alpha = render_rgba(lambda: MathTex(content, color="#FFFFFF"), height).getchannel("A")
    return alpha.filter(ImageFilter.MaxFilter(3))  # traço do LaTeX é fino para capa


def waves():
    """Assinatura física do vídeo: ruído + contribuição do fone → resíduo pequeno (melhor ajuste)."""
    from manim import VGroup, VMobject

    xs = np.linspace(0, 6, 400)
    wt = 4 * np.pi * xs / 6
    g, wtau = 0.95, 0.03 * np.pi                      # melhor ajuste da cena (resíduo ≈ 0,105A)

    def curve(ys, color, width, opacity=1.0):
        return VMobject().set_points_smoothly(np.column_stack([xs, ys, 0 * xs])).set_stroke(color, width, opacity)

    base = curve(0 * xs, "#267BFF", 5, 0.5)
    return VGroup(base,
                  curve(noise(wt, 0), "#35D9FF", 12),
                  curve(fone(wt, g, wtau, 0), "#EA63FF", 12),
                  curve(residual(wt, g, wtau, 0), "#F5F7FF", 18))


img = Image.open(BASE).convert("RGB")
W, H = img.size
arr = np.asarray(img).astype(np.float32)
# Fundo sem estrelas: mínimo local seguido de suavização.
soft = np.asarray(img.filter(ImageFilter.MinFilter(15)).filter(ImageFilter.GaussianBlur(20))).astype(np.float32)


def erase_vertical(x0, x1, y0, y1, blend=30):
    top, bot = soft[y0, x0:x1], soft[y1, x0:x1]
    t = np.clip((np.arange(y1 - y0) - (y1 - y0 - blend)) / blend, 0, 1)[:, None, None]
    return (x0, y0, (1 - t) * top[None] + t * bot[None])


def erase_bilinear(x0, x1, y0, y1, r=6):
    """Interior do painel: interpolação entre os quatro cantos, fora da fórmula antiga."""
    c = lambda x, y: arr[y - r:y + r, x - r:x + r].reshape(-1, 3).mean(0)
    tl, tr, bl, br = c(x0, y0), c(x1, y0), c(x0, y1), c(x1, y1)
    u = np.linspace(0, 1, x1 - x0)[None, :, None]; v = np.linspace(0, 1, y1 - y0)[:, None, None]
    return (x0, y0, (1 - v) * ((1 - u) * tl + u * tr) + v * ((1 - u) * bl + u * br))


fill = arr.copy()
mask = np.zeros((H, W), np.float32)
for x0, y0, patch in (erase_vertical(64, 1016, 666, 1000),     # título
                      erase_vertical(96, 988, 1052, 1142),    # linha de série
                      erase_bilinear(226, 874, 1194, 1420)):  # interior do painel
    h, w = patch.shape[:2]
    fill[y0:y0 + h, x0:x0 + w] = patch
    mask[y0:y0 + h, x0:x0 + w] = 1
m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(
    ImageFilter.GaussianBlur(8))).astype(np.float32)[..., None] / 255
fill += np.random.default_rng(5).normal(0, 1.6, fill.shape)  # grão similar ao original
img = Image.fromarray((arr * (1 - m) + fill * m).clip(0, 255).astype(np.uint8)).convert("RGBA")
if VARIANTE == "hero":          # painel inteiro some: fundo sem estrelas, borda bem suave
    m2 = np.zeros((H, W), np.float32); m2[1125:1495, 115:965] = 1
    m2 = np.asarray(Image.fromarray((m2 * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(25))).astype(np.float32)[..., None] / 255
    # Fundo sob o painel: interpolação vertical entre faixas de fundo acima e abaixo dele
    # (o `soft` ainda carrega o brilho da borda do painel).
    y0, y1 = 1110, 1510
    under = soft.copy()
    k = np.clip((np.arange(H) - y0) / (y1 - y0), 0, 1)[:, None, None]
    under[:] = (1 - k) * soft[y0][None] + k * soft[y1][None]
    under += np.random.default_rng(6).normal(0, 1.6, soft.shape)
    img = Image.fromarray((np.asarray(img.convert("RGB")).astype(np.float32) * (1 - m2) + under * m2)
                          .clip(0, 255).astype(np.uint8)).convert("RGBA")


def gradient(size, stops):
    w, h = size
    seg = np.clip(np.linspace(0, 1, w) * (len(stops) - 1), 0, len(stops) - 1 - 1e-6)
    i = seg.astype(int); f = (seg - i)[:, None]
    row = (np.array(stops)[i] * (1 - f) + np.array(stops)[i + 1] * f).astype(np.uint8)
    return Image.fromarray(np.repeat(row[None], h, 0), "RGB")


def glow_paste(layer_mask, box, color_img, glow_color, glow_radius, glow_alpha):
    """Aplica texto (máscara L em box) com preenchimento e brilho."""
    global img
    full = Image.new("L", img.size, 0); full.paste(layer_mask, box[:2])
    halo = full.filter(ImageFilter.GaussianBlur(glow_radius)).point(lambda v: int(v * glow_alpha))
    img = Image.composite(Image.new("RGBA", img.size, glow_color + (255,)), img, halo)
    fill_full = Image.new("RGBA", img.size); fill_full.paste(color_img.convert("RGBA"), box[:2])
    img = Image.composite(fill_full, img, full)


def text_mask(text, font, tracking=0):
    widths = [font.getlength(c) + tracking for c in text]
    asc, desc = font.getmetrics()
    mk = Image.new("L", (int(sum(widths) - tracking) + 4, asc + desc + 4), 0)
    d = ImageDraw.Draw(mk); x = 2
    for c, w in zip(text, widths):
        d.text((x, 2), c, font=font, fill=255); x += w
    return mk.crop(mk.getbbox())


def fit(text, path, width, start):
    size = start
    while ImageFont.truetype(path, size).getlength(text) > width:
        size -= 1
    return ImageFont.truetype(path, size)


def place_center(mask_img, cy):
    return ((W - mask_img.width) // 2, int(cy - mask_img.height / 2))


G, WTAU = 0.95, 0.03 * np.pi                          # melhor ajuste da cena (resíduo ≈ 0,105A)
CYAN, MAGENTA, WHITE, BLUE = "#35D9FF", "#EA63FF", "#F5F7FF", "#267BFF"


def curve(x0, x1, y, amp, f, color, width, periods=2):
    """Curva y = amp·f(ωt) em [x0, x1], com as funções da cena (f recebe ωt)."""
    from manim import VMobject
    xs = np.linspace(x0, x1, 300)
    wt = 2 * np.pi * periods * (xs - x0) / (x1 - x0)
    return VMobject().set_points_smoothly(np.column_stack([xs, y + amp * f(wt), 0 * xs])).set_stroke(color, width)


def headphone_icon():
    """Fone de ouvido visto de frente (haste, conchas e almofadas), centrado em x = 0."""
    from manim import PI, Arc, Line, RoundedRectangle, VGroup
    band = Arc(radius=2.3, start_angle=0.15, angle=PI - 0.3).shift([0, 0.2, 0]).set_stroke(BLUE, 16)
    sliders = VGroup(*(Line([s * 2.27, 0.54, 0], [s * 2.3, 0.2, 0]) for s in (-1, 1))).set_stroke(BLUE, 14)
    cups = VGroup(*(RoundedRectangle(width=0.95, height=1.9, corner_radius=0.4).move_to([s * 2.3, -0.7, 0])
                    for s in (-1, 1))).set_stroke(BLUE, 10).set_fill(BLUE, 0.35)
    pads = VGroup(*(RoundedRectangle(width=0.28, height=1.5, corner_radius=0.14).move_to([s * 1.7, -0.7, 0])
                    for s in (-1, 1))).set_stroke(BLUE, 6).set_fill(BLUE, 0.6)
    return VGroup(band, sliders, cups, pads)


def headphone_front(labels=False):
    """Fone visto de frente: ruído grande do lado de fora, só um resíduo mínimo entre as conchas."""
    from manim import PI, Arc, VGroup
    band, sliders, cups, pads = headphone_icon()
    arcs = VGroup(*(Arc(radius=r, start_angle=(PI if s > 0 else 0) - 0.5, angle=1.0, arc_center=[s * 1.6, -0.7, 0])
                    .set_stroke(MAGENTA, 7, 0.9 - 0.25 * k) for s in (-1, 1) for k, r in enumerate((0.35, 0.6))))
    out_l = curve(-6.6, -2.95, -0.7, 0.75, lambda w: noise(w, 0), CYAN, 12)
    out_r = curve(2.95, 6.6, -0.7, 0.75, lambda w: noise(w, 0), CYAN, 12)
    inside = curve(-1.15, 1.15, -0.7, 0.75, lambda w: residual(w, G, WTAU, 0), WHITE, 12, periods=1)
    art = VGroup(out_l, out_r, band, sliders, cups, arcs, pads, inside)
    if labels:                                        # onde está o ruído e o que sobra perto do ouvido
        art.add(*(scene_text("RUÍDO", 40, color=CYAN).move_to([x, -1.95, 0]) for x in (-4.8, 4.8)),
                scene_text("RESÍDUO", 36, color=WHITE).move_to([0, -2.05, 0]))
    return art


def equation_visual():
    """RUÍDO + FONE = RESÍDUO, com as curvas da cena na mesma escala."""
    from manim import Line, VGroup
    amp = 0.8
    parts = VGroup(curve(-6.2, -3.4, 0, amp, lambda w: noise(w, 0), CYAN, 12),
                   curve(-1.4, 1.4, 0, amp, lambda w: fone(w, G, WTAU, 0), MAGENTA, 12),
                   curve(3.4, 6.2, 0, amp, lambda w: residual(w, G, WTAU, 0), WHITE, 14))
    plus = VGroup(Line([-2.7, 0, 0], [-2.1, 0, 0]), Line([-2.4, -0.3, 0], [-2.4, 0.3, 0])).set_stroke(WHITE, 10)
    equal = VGroup(Line([2.1, 0.15, 0], [2.7, 0.15, 0]), Line([2.1, -0.15, 0], [2.7, -0.15, 0])).set_stroke(WHITE, 10)
    labels = VGroup(*(scene_text(name, 40, color=col).move_to([x, -1.45, 0])
                      for name, col, x in (("RUÍDO", CYAN, -4.8), ("FONE", MAGENTA, 0), ("RESÍDUO", WHITE, 4.8))))
    return VGroup(parts, plus, equal, labels)


def before_after():
    """Perto do ouvido: fone desligado (o próprio ruído) → fone ligado (só o resíduo), mesma escala."""
    from manim import Arrow, VGroup
    amp, y = 0.8, -0.6
    off = curve(-5.6, -1.2, y, amp, lambda w: noise(w, 0), CYAN, 12)
    on = curve(1.2, 5.6, y, amp, lambda w: residual(w, G, WTAU, 0), WHITE, 14)
    icons = VGroup(*(headphone_icon().scale(0.35).move_to([x, 1.25, 0]) for x in (-3.4, 3.4)))
    icons[0].set_stroke(opacity=0.4)                  # desligado: ícone apagado (só o traço)
    icons[0][2].set_fill(opacity=0.12); icons[0][3].set_fill(opacity=0.2)
    arrow = Arrow([-0.55, y, 0], [0.55, y, 0], buff=0, color=WHITE, stroke_width=10, tip_length=0.3)
    labels = VGroup(scene_text("FONE DESLIGADO", 36, color=CYAN).move_to([-3.4, -1.9, 0]),
                    scene_text("FONE LIGADO", 36, color=WHITE).move_to([3.4, -1.9, 0]))
    return VGroup(off, on, icons, arrow, labels)


def opposite_into_fone():
    """Ruído e contribuição do fone quase opostos; a soma branca fica pequena; o fone ao lado."""
    from manim import VGroup
    amp = 0.85
    return VGroup(curve(-6.4, 1.0, 0, amp, lambda w: noise(w, 0), CYAN, 12, periods=3),
                  curve(-6.4, 1.0, 0, amp, lambda w: fone(w, G, WTAU, 0), MAGENTA, 12, periods=3),
                  curve(-6.4, 1.0, 0, amp, lambda w: residual(w, G, WTAU, 0), WHITE, 16, periods=3),
                  headphone_icon().scale(0.62).move_to([3.7, 0.2, 0]))


def superposition(x0, x1, y, amp, periods=2, white=16):
    """Ruído (ciano) e fone (magenta) quase opostos no mesmo eixo; a soma branca fica pequena, não nula."""
    from manim import VGroup
    return VGroup(curve(x0, x1, y, amp, lambda w: noise(w, 0), CYAN, 12, periods),
                  curve(x0, x1, y, amp, lambda w: fone(w, G, WTAU, 0), MAGENTA, 12, periods),
                  curve(x0, x1, y, amp, lambda w: residual(w, G, WTAU, 0), WHITE, white, periods))


def fone_applied(cx, cy, k, incoming=1.3, emit=False, res_width=12, res_periods=1):
    """Fone de frente (escala k): ruído ciano chegando pela esquerda (comprimento `incoming`, 0 = sem),
    resíduo branco entre as conchas e, com `emit`, a contribuição magenta saindo do próprio fone."""
    from manim import PI, Arc, VGroup
    icon = headphone_icon().scale(k).move_to([cx, cy, 0])
    cup_l = icon[2][0]
    pad_l, pad_r = icon[3]
    y, amp = cup_l.get_center()[1], 0.62 * k / 0.75
    group = VGroup(icon, curve(pad_l.get_right()[0] + 0.12, pad_r.get_left()[0] - 0.12, y, amp,
                               lambda w: residual(w, G, WTAU, 0), WHITE, res_width, periods=res_periods))
    if incoming:
        group.add(curve(cup_l.get_left()[0] - 0.12 - incoming, cup_l.get_left()[0] - 0.12, y, amp,
                        lambda w: noise(w, 0), CYAN, 12, periods=1))
    if emit:                                          # o fone adiciona uma contribuição (não só bloqueia)
        for center, start in (([pad_l.get_right()[0], y, 0], -0.55), ([pad_r.get_left()[0], y, 0], PI - 0.55)):
            for j, r in enumerate((0.4, 0.72)):
                group.add(Arc(radius=r * k / 0.85, start_angle=start, angle=1.1, arc_center=center)
                          .set_stroke(MAGENTA, 12, 1.0 - 0.25 * j))
    return group


def flow_arrow(x0, x1, y):
    from manim import Arrow
    return Arrow([x0, y, 0], [x1, y, 0], buff=0, color=WHITE, stroke_width=9, tip_length=0.3)


def axis_y(group):
    return group[0][2][0].get_center()[1]              # altura do centro das conchas


def variant_a():
    """Interferência (esquerda) → cancelamento de ruído no fone (direita): ciano + magenta → branco pequeno."""
    from manim import VGroup
    right = fone_applied(3.9, 0.6, 0.85, emit=True, res_width=16, res_periods=1.5)
    y = axis_y(right)
    bottom = y - 1.75                                 # abaixo do vale das ondas
    labels = VGroup(scene_text("INTERFERÊNCIA", 48, color=WHITE).move_to([-4.35, bottom, 0]),
                    scene_text("CANCELAMENTO DE RUÍDO", 48, color=WHITE).move_to([3.45, bottom, 0]))
    return VGroup(superposition(-6.4, -2.3, y, 1.1, white=20), flow_arrow(-2.0, -0.9, y), right, labels)


def variant_b():
    """Ondas em primeiro plano (mesmo eixo); fone pequeno como aplicação à direita."""
    from manim import VGroup
    icon = headphone_icon().scale(0.55).move_to([4.5, 0.35, 0])
    y = icon[2][0].get_center()[1]
    label = scene_text("SUPERPOSIÇÃO", 50, color=WHITE).set_opacity(0.85).move_to([-2.5, y - 1.85, 0])
    return VGroup(superposition(-6.6, 1.6, y, 1.4, periods=3), label, flow_arrow(2.0, 2.9, y), icon)


def variant_c():
    """Transição completa: ciano + magenta → resultante branca pequena → fone."""
    from manim import VGroup
    right = fone_applied(4.35, 0.5, 0.8, incoming=0)
    y = axis_y(right)
    pair = superposition(-6.6, -3.5, y, 1.1)
    pair.remove(pair[2])                              # 1º passo: só as duas contribuições
    result = curve(-2.4, 0.6, y, 1.1, lambda w: residual(w, G, WTAU, 0), WHITE, 16)
    return VGroup(pair, flow_arrow(-3.25, -2.6, y), result, flow_arrow(0.85, 1.5, y), right)


HEADLINES = {"ondas": ("O SOM PODE", "CANCELAR O SOM?"), "fone": ("O SOM PODE", "CANCELAR O SOM?"),
             "equacao": ("COMO O FONE", "REDUZ O RUÍDO?"), "fone_rotulos": ("SOM + SOM", "= SILÊNCIO?"),
             "hero": ("COMO FUNCIONA?", "CANCELAMENTO DE RUÍDO"),
             "antes_depois": ("O QUE O FONE", "FAZ COM O RUÍDO?"),
             "opostas": ("UMA ONDA PODE", "CANCELAR OUTRA?"),
             "a": ("O SOM PODE", "CANCELAR O SOM?"), "b": ("UMA ONDA PODE", "CANCELAR OUTRA?"),
             "c": ("O SOM PODE", "CANCELAR O SOM?")}
HEAD_Y = {"c": (748, 882)}                          # C sobe a headline para caber o subtítulo

# 1. Headline em duas linhas (branco + gradiente da marca), como no EP. 01 da série.
line1, line2 = HEADLINES[VARIANTE]
head = text_mask(line1, fit(line1, BOLD, 870, 170))
y_head, y_subj = HEAD_Y.get(VARIANTE, (772, 920))
glow_paste(head, place_center(head, y_head), Image.new("RGB", head.size, (255, 255, 255)),
           (70, 140, 255), 16, 0.55)
subj = text_mask(line2, fit(line2, BOLD, 870, 130))
glow_paste(subj, place_center(subj, y_subj), gradient(subj.size, BRAND), (110, 90, 255), 14, 0.45)

if VARIANTE == "c":             # subtítulo claramente secundário, uma linha
    sub = text_mask("A FÍSICA POR TRÁS DO CANCELAMENTO DE RUÍDO", fit("A FÍSICA POR TRÁS DO CANCELAMENTO DE RUÍDO",
                                                                      MEDIUM, 800, 34), tracking=2)
    glow_paste(sub, place_center(sub, 968), Image.new("RGB", sub.size, (214, 222, 255)), (60, 120, 255), 5, 0.2)

# 2. Linha de série, no lugar e escala das capas anteriores.
series = text_mask("DA EQUAÇÃO AO FENÔMENO · EP. 02", ImageFont.truetype(MEDIUM, 38), tracking=9)
if series.width > 850:
    series = series.resize((850, round(series.height * 850 / series.width)), Image.LANCZOS)
glow_paste(series, place_center(series, 1097), Image.new("RGB", series.size, (245, 247, 255)),
           (60, 120, 255), 6, 0.32)

# 3. Painel (interior x 226–874, y 1194–1420).
PANEL_CY = 1307


def paste_art(art, x, y):
    global img
    full = Image.new("L", img.size, 0); full.paste(art.getchannel("A"), (x, y))
    halo = full.filter(ImageFilter.GaussianBlur(10)).point(lambda p: int(p * 0.3))
    img = Image.composite(Image.new("RGBA", img.size, (90, 110, 255, 255)), img, halo)
    img.alpha_composite(art, (x, y))


def fit_box(art, max_w, max_h):
    k = min(max_w / art.width, max_h / art.height)
    return art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)


if VARIANTE == "ondas":         # publicada: ondas + p₁ + p₂
    GAP = 36
    art = fit_box(render_rgba(waves, 150), 320, 999)
    formula = tex_mask(r"p_1+p_2", 62)
    assert art.width + GAP + formula.width <= 610, (art.width, formula.width)
    x = (W - art.width - GAP - formula.width) // 2
    paste_art(art, x, PANEL_CY - art.height // 2)
    glow_paste(formula, (x + art.width + GAP, PANEL_CY - formula.height // 2),
               gradient(formula.size, PALE), (150, 110, 255), 10, 0.5)
elif VARIANTE == "hero":        # sem painel: fone grande com rótulos
    art = fit_box(render_rgba(lambda: headphone_front(labels=True), 600), 840, 300)
    paste_art(art, (W - art.width) // 2, 1310 - art.height // 2)
else:                           # conteúdo ocupando o painel
    build = {"fone": headphone_front, "fone_rotulos": lambda: headphone_front(labels=True),
             "equacao": equation_visual, "antes_depois": before_after,
             "opostas": opposite_into_fone, "a": variant_a, "b": variant_b, "c": variant_c}[VARIANTE]
    art = fit_box(render_rgba(build, 400), 600, 205)
    paste_art(art, (W - art.width) // 2, PANEL_CY - art.height // 2)

img.convert("RGB").save(OUT, optimize=True)
print(OUT, img.size)
