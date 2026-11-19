"""Demo Three.js + Manim — solenoide (curto vertical, sandbox).

O Manim começa exatamente no último quadro da cena 3D (render do Three.js em frames3d/f0269.png):
a vista frontal tem 16 unidades de altura no plano z = 0, o mesmo sistema de coordenadas do frame 9 × 16.
Daqui em diante é 2D: corte do enrolamento (⊙/⊗), amperiano retangular e B = μ0 n I.
"""
import os
import sys
from pathlib import Path

from manim import *

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from template.config import BACKGROUND_COLOR, TEXT_COLOR  # noqa: E402
from template.fonts import screen_text  # noqa: E402

UNIT = Path(__file__).absolute().parent
config.media_dir = os.environ.get("MEDIA_DIR", str(UNIT / "media"))
config.background_color = BACKGROUND_COLOR
ULTIMO_3D = Path(os.environ.get("ULTIMO_3D", str(UNIT / "frames3d" / "f0269.png")))

# cores das grandezas (padrao_video_longo.md)
MAG, GREEN, GEO, DIM, STEEL = "#EA63FF", "#3FE08B", "#B8C4DA", "#8FA3C4", "#7A8696"
PANEL, BLUE_L = "#0E2A52", "#7FB2FF"

R, LEN, TURNS = 1.5, 6.0, 12
PASSO = LEN / TURNS  # 0,5: espiras por unidade n = 2
Y_DIR = [-LEN / 2 + PASSO * m for m in range(TURNS + 1)]            # x = +R: corrente entra (⊗)
Y_ESQ = [-LEN / 2 + PASSO * (m + .5) for m in range(TURNS)]         # x = -R: corrente sai (⊙)
COR = {r"\vec B": MAG, "B": MAG, r"d\vec\ell": GEO, r"\ell": GEO, r"I_{\text{enc}}": GREEN, "I": GREEN}


def cores(t):
    for parte in t:
        if parte.tex_string in COR:
            parte.set_color(COR[parte.tex_string])
    return t


def sai(p):
    c = Circle(.13, color=GREEN, stroke_width=3).set_fill(BACKGROUND_COLOR, 1).move_to(p)
    return VGroup(c, Dot(p, radius=.045, color=GREEN))


def entra(p):
    c = Circle(.13, color=GREEN, stroke_width=3).set_fill(BACKGROUND_COLOR, 1).move_to(p)
    d = .085
    x = VGroup(Line(p + [-d, -d, 0], p + [d, d, 0]), Line(p + [-d, d, 0], p + [d, -d, 0])).set_stroke(GREEN, 3)
    return VGroup(c, x)


class SolenoideAmpere(Scene):
    def construct(self):
        fundo = ImageMobject(str(ULTIMO_3D)).set_height(config.frame_height)
        fundo.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        self.add(fundo)
        self.wait(.4)

        # 1) o 3D recua e o corte do enrolamento aparece por cima, no mesmo lugar
        titulo = screen_text("LEI DE AMPÈRE", 26, color=DIM).move_to(UP * 7.05)
        sub = screen_text("CAMPO DENTRO DO SOLENOIDE", 34, color=TEXT_COLOR).move_to(UP * 6.45)
        esq = VGroup(*[sai(np.array([-R, y, 0])) for y in Y_ESQ])
        dir_ = VGroup(*[entra(np.array([R, y, 0])) for y in Y_DIR])
        self.play(fundo.animate.set_opacity(.28), FadeIn(titulo, shift=DOWN * .2), FadeIn(sub, shift=DOWN * .2), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(m, scale=.6) for m in [*esq, *dir_]], lag_ratio=.04), run_time=1.4)

        # campo uniforme no interior: colunas de setas iguais
        setas = VGroup(*[Arrow([x, y - .45, 0], [x, y + .45, 0], buff=0, color=MAG, stroke_width=5,
                               max_tip_length_to_length_ratio=.3)
                         for x in (-.9, -.3, .3) for y in (-2.1, -.7, .7, 2.1)])
        rot_b = MathTex(r"\vec B", color=MAG, font_size=44).next_to(setas, LEFT, buff=.25).shift(UP * 2.1 + RIGHT * 0)
        rot_b.move_to([-1.0 + 0, 3.55, 0])
        self.play(LaggedStart(*[GrowArrow(s) for s in setas], lag_ratio=.05), FadeIn(rot_b), run_time=1.3)
        self.wait(.5)

        # 2) amperiano retangular: um lado dentro (comprimento ℓ), o outro fora, onde B ≈ 0
        x0, x1, y0, y1 = .9, 2.5, -1.25, .75
        caminho = [np.array(p) for p in ([x0, y0, 0], [x0, y1, 0], [x1, y1, 0], [x1, y0, 0])]
        amp = DashedVMobject(Polygon(*caminho, color=GEO, stroke_width=4), num_dashes=46)
        sentido = VGroup(*[Arrow(a, b, buff=0, color=GEO, stroke_width=0, max_tip_length_to_length_ratio=1,
                                 tip_length=.22).set_fill(GEO, 1)
                           for a, b in (([x0, -.35, 0], [x0, -.05, 0]), ([x1, -.05, 0], [x1, -.35, 0]))])
        rot_l = MathTex(r"\ell", color=GEO, font_size=46).next_to([x1, -.25, 0], RIGHT, buff=.18)
        dentro = VGroup(*[m for m, y in zip(dir_, Y_DIR) if y0 < y < y1])
        self.play(Create(amp), FadeIn(sentido), run_time=1.4)
        self.play(FadeIn(rot_l), *[m[0].animate.set_fill(GREEN, .35) for m in dentro], run_time=.8)

        # 3) a conta, embaixo
        eq1 = cores(MathTex(r"\oint", r"\vec B", r"\cdot", r"d\vec\ell", "=", r"\mu_0", r"I_{\text{enc}}", font_size=58))
        eq2 = cores(MathTex("B", r"\ell", "=", r"\mu_0", "(", "n", r"\ell", ")", "I", font_size=58))
        eq3 = cores(MathTex("B", "=", r"\mu_0", "n", "I", font_size=72))
        for e in (eq1, eq2, eq3):
            e.move_to(DOWN * 5.0)
        nota = screen_text("só o lado de dentro contribui", 26, color=DIM).move_to(DOWN * 6.1)
        nota2 = screen_text("4 espiras = n·ℓ, com n = 2 por unidade", 26, color=DIM).move_to(DOWN * 6.1)
        self.play(Write(eq1), run_time=1.4)
        self.play(FadeIn(nota, shift=UP * .15), run_time=.6)
        self.wait(1.0)
        self.play(TransformMatchingTex(eq1, eq2), FadeOut(nota), run_time=1.3)
        self.play(FadeIn(nota2, shift=UP * .15), run_time=.6)
        self.wait(1.0)
        # ℓ dos dois lados se cancela: risca, some, e o resto escorrega para B = μ0 n I
        riscos = VGroup(*[Line(p.get_corner(DL), p.get_corner(UR), color=TEXT_COLOR, stroke_width=4)
                          for p in (eq2[1], eq2[6])])
        self.play(Create(riscos), run_time=.7)
        self.play(FadeOut(riscos), FadeOut(eq2[1]), FadeOut(eq2[4]), FadeOut(eq2[6]), FadeOut(eq2[7]), FadeOut(nota2), run_time=.6)
        resto = VGroup(eq2[0], eq2[2], eq2[3], eq2[5], eq2[8])
        self.play(*[ReplacementTransform(a, b) for a, b in zip(resto, eq3)], run_time=1.0)
        caixa = SurroundingRectangle(eq3, buff=.3, corner_radius=.15, color=BLUE_L, stroke_width=2.5).set_fill(PANEL, .7)
        self.play(FadeIn(caixa), eq3.animate.set_z_index(1), run_time=.6)
        self.wait(2.0)
