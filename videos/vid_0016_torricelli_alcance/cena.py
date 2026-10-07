"""DA EQUAÇÃO AO FENÔMENO — vid_0016 · Torricelli: onde furar para a água chegar mais longe?

RODADA 1 (≈0–10 s): gancho (furos em u = 0,2 e 0,8 chegam ao mesmo ponto) e definição geométrica de H, y e H − y.
Primeiro teste real do arsenal Blender → Manim: o sólido `tanque_torricelli` dá só a geometria; todo texto, cota,
seta e marcador são Manim, posicionados sobre pontos projetados na câmera do Blender (`projecao.json`, gerado por
`projecao.py`). Estado conceitual único: u = y/H (0,2 e 0,8 no gancho; 0,35 na definição).

Preview:  uv run python -m manim -r 540,960 --fps 15 videos/vid_0016_torricelli_alcance/cena.py Vid0016Rodada1
Sequências Blender (preparar antes; res = 1,2 × o quadro, proporção 9:16):
  python experimentos/blender/arsenal/ponte.py tanque_torricelli --res 648x1152 --frames 30 --set altura_furo=<u·2,2> --set enquadramento_fixo=1 --set setas=0 --set estilo_jato=1
"""
from contextlib import contextmanager
import json
from pathlib import Path
import sys
import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experimentos" / "blender" / "arsenal"))
from template.config import BACKGROUND_COLOR, TEXT_COLOR, PRIMARY_COLOR, WATERMARK_PATH
from template.fonts import screen_text
from manim_solido3d import Solido3D

UNIT = Path(__file__).resolve().parent
WHITE, CYAN, VIOLET, MUTED = TEXT_COLOR, PRIMARY_COLOR, "#9C8CFF", "#ADB8D1"
HEADER_Y, TITLE_Y, SUBTITLE_SAFE_Y = 7.4, 6.45, -5.7

# Sólido 3D: a imagem tem proporção 9:16 e S vezes o quadro (o fundo é transparente, o excesso fica fora da tela).
S = 1.2                                   # escala da imagem em relação ao quadro 9×16
CX0, CY0 = 1.3, 0.6                      # centro da imagem em unidades do Manim
ASSET_RES = f"{round(540 * S)}x{round(960 * S)}"
NIVEL = 2.2                               # H do sólido (default da ficha)
PROJ = json.loads((UNIT / "projecao.json").read_text(encoding="utf-8"))


def u_params(u):
    """Estado conceitual único u = y/H → parâmetros do sólido (câmera fixa, sem seta de velocidade ainda, jato em contas: estilo_jato=1)."""
    return {"altura_furo": round(u * NIVEL, 4), "enquadramento_fixo": 1, "setas": 0, "estilo_jato": 1}


def pt(u, chave):
    """Ponto projetado do sólido (normalizado 0–1 na imagem) → coordenadas do Manim."""
    nx, ny = PROJ["u"][str(u)][chave]
    return np.array([(nx - 0.5) * 9 * S + CX0, (ny - 0.5) * 16 * S + CY0, 0.0])


@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def text(content, size=26, color=WHITE, opacity=1, width=8):
    with wide_pango():
        mob = screen_text(content, size, color=color)
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob.set_opacity(opacity)


def mt(*parts, size=44, color=WHITE):
    return MathTex(*parts, font_size=size, color=color)


def dim_arrow(a, b, color, width=3.2):
    return DoubleArrow(a, b, buff=0, stroke_width=width, color=color, tip_length=0.16,
                       max_tip_length_to_length_ratio=0.3).set_z_index(6)


def guide(a, b, color=MUTED, width=2.2, opacity=0.75):
    return DashedLine(a, b, color=color, stroke_width=width, dash_length=0.1, stroke_opacity=opacity).set_z_index(5)


class Vid0016Rodada1(Scene):
    def sold(self, u):
        img = Solido3D("tanque_torricelli", params=u_params(u), frames=30, res=ASSET_RES, render="nunca")
        return img.mobject(cena=self, altura=16 * S, centro=np.array([CX0, CY0, 0.0]), periodo=2.0).set_z_index(1)

    def ring(self, p, color=CYAN, r=0.2):
        return Circle(radius=r, color=color, stroke_width=3.2).move_to(p).set_z_index(7)

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        rng = np.random.default_rng(16)
        self.add(VGroup(*[Dot([rng.uniform(-4.4, 4.4), rng.uniform(-7.2, 7.2), 0], radius=rng.uniform(0.01, 0.025),
                              color=WHITE, fill_opacity=rng.uniform(0.08, 0.2)) for _ in range(46)]).set_z_index(0))
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(wm.to_corner(UP + RIGHT, buff=0.28).set_z_index(9))
        self.add(text("DA EQUAÇÃO AO FENÔMENO", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4).set_z_index(9))

        # ── 0–4 s · GANCHO: dois furos complementares (u = 0,2 e u = 0,8) com o mesmo alcance ────────────────────────
        sa, sb, sd = self.sold(0.2), self.sold(0.8), self.sold(0.35)
        h1, h2 = text("O MAIS BAIXO", 46), text("VAI MAIS LONGE?", 46, CYAN)
        headline = VGroup(h1, h2).arrange(DOWN, buff=0.22).move_to([0, 5.75, 0])
        self.play(FadeIn(sa), FadeIn(headline, shift=UP * 0.15), run_time=0.5)
        ring_a = self.ring(pt(0.2, "furo"))
        self.play(Create(ring_a), run_time=0.3)
        self.play(FadeOut(ring_a), run_time=0.2)
        self.wait(0.3)
        land = pt(0.2, "pouso")                      # o mesmo ponto vale para u = 0,8: x(u) = x(1 − u)
        mark = VGroup(guide(land, land + UP * 2.3, VIOLET, 2.6, 0.9),
                      Circle(radius=0.12, color=WHITE, stroke_width=3.2).move_to(land)).set_z_index(7)
        self.play(Create(mark), run_time=0.4)
        self.wait(0.3)
        self.play(FadeOut(sa), FadeIn(sb), run_time=0.4)
        ring_b = self.ring(pt(0.8, "furo"))
        self.play(Create(ring_b), run_time=0.3)
        self.play(FadeOut(ring_b), run_time=0.2)
        self.play(Indicate(mark[1], color=WHITE, scale_factor=1.7), run_time=0.5)
        self.wait(0.2)

        # ── 4–10 s · DEFINIÇÃO GEOMÉTRICA: H, y e H − y (um tanque, u = 0,35) ───────────────────────────────────────
        sub = text("Nível constante · jato ideal", 28, opacity=0.7).move_to([0, 5.9, 0])
        self.play(FadeOut(headline), FadeOut(mark), FadeOut(sb), FadeIn(sd), FadeIn(sub), run_time=0.5)

        chao_y = pt(0.35, "cota_chao")[1]
        sup_y = pt(0.35, "cota_superficie")[1]
        furo = pt(0.35, "furo")
        parede_x = pt(0.35, "chao_parede")[0]                       # parede direita (onde está o furo)
        esq_x = pt(0.35, "esq_chao")[0]                              # aresta esquerda do tanque
        xA, xB = esq_x - 0.4, esq_x - 2.0                           # coluna de y e H − y · coluna de H

        # 1) plano de impacto (chão): referência comum de H e y
        fim = pt(0.35, "chao_fim")
        piso_e = guide([xB - 0.12, chao_y, 0], [esq_x, chao_y, 0], WHITE)
        piso_d = guide([parede_x, chao_y, 0], [fim[0], chao_y, 0], WHITE)
        tag_chao = text("plano de impacto", 22, WHITE, 0.8).move_to([(esq_x + parede_x) / 2, chao_y - 0.42, 0])
        self.play(Create(piso_e), Create(piso_d), FadeIn(tag_chao), run_time=0.55)
        self.wait(0.15)

        # 2) H: da superfície até o plano de impacto
        sup_e = guide([xB - 0.12, sup_y, 0], [esq_x, sup_y, 0], WHITE)
        seta_H = dim_arrow([xB, chao_y, 0], [xB, sup_y, 0], WHITE)
        lab_H = mt("H", size=46, color=WHITE).move_to([xB, sup_y + 0.45, 0])
        tag_sup = text("superfície", 22, WHITE, 0.8).move_to([parede_x + 1.35, sup_y + 0.42, 0])
        self.play(Create(sup_e), GrowFromCenter(seta_H), FadeIn(lab_H, tag_sup), run_time=0.6)
        self.wait(0.25)

        # 3) y: do plano de impacto até o furo (mesmo chão de H)
        lin_furo = guide([xA - 0.12, furo[1], 0], furo, CYAN, 2.4, 0.8)
        ring_f = self.ring(furo, CYAN, 0.17)
        seta_y = dim_arrow([xA, chao_y, 0], [xA, furo[1], 0], CYAN)
        lab_y = mt("y", size=46, color=CYAN).next_to(seta_y, LEFT, buff=0.16)
        tag_furo = text("furo", 26, CYAN).move_to(furo + np.array([0.95, 0.55, 0]))
        self.play(Create(lin_furo), Create(ring_f), run_time=0.4)
        self.play(GrowFromCenter(seta_y), FadeIn(lab_y, tag_furo), run_time=0.5)
        self.play(FadeOut(ring_f), run_time=0.2)
        self.wait(0.2)

        # 4) H − y: da superfície até o furo (profundidade)
        seta_p = dim_arrow([xA, furo[1], 0], [xA, sup_y, 0], VIOLET)
        lab_p = mt("H", "-", "y", size=38, color=VIOLET).next_to(seta_p, LEFT, buff=0.16)
        self.play(GrowFromCenter(seta_p), FadeIn(lab_p), run_time=0.5)
        self.wait(0.25)

        # 5) a relação entre as três medidas
        rel = mt("H", "=", "y", "+", "(H-y)", size=52)
        rel[0].set_color(WHITE), rel[2].set_color(CYAN), rel[4].set_color(VIOLET)
        rel.move_to([0, -2.6, 0])
        self.play(FadeIn(rel, shift=UP * 0.12), run_time=0.5)
        self.wait(0.8)
