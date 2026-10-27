"""Protótipo técnico (NÃO publicável): MF-Tools numa sequência contínua de ~30 s.

Tema: completar o quadrado, y = x² + 6x + 5  ->  y = (x + 3)² - 4.

uv run --frozen --with "MF-Tools[manimce]==1.4.9" python -m manim -r 540,960 --fps 15 \
    experiments/mf_tools_production_test.py MFToolsProductionTest
"""
from manim import *
from MF_Tools import (DN, VT, SurroundingRectangleUnion, TransformByGlyphMap,
                      Vcis, Arc3d, bounding_box, indexx_labels)

from template.config import BACKGROUND_COLOR, PRIMARY_COLOR as CYAN, SECONDARY_COLOR as VIOLET
from template.fonts import screen_text

config.background_color = BACKGROUND_COLOR
ACCENT = "#B79CFF"  # violeta mais claro que o SECONDARY_COLOR, legível sobre o fundo escuro
EQ = min(1.5, 8.0 / MathTex("y=x^2+6x+9-9+5").width)  # a equação mais larga cabe em 8 un.
LEFT_X = -4.0  # todas as equações ancoradas à esquerda, pelo "y"
STEP4_MODE = "fade"  # "morph" | "fade": auto_morph deixa borrão na meia-transição; auto_fade fica limpo


class PopIn(FadeIn):
    """Introducer customizado: glifo entra pequeno e descendo."""

    def __init__(self, mob, **kw):
        kw.setdefault("scale", 0.4)
        kw.setdefault("shift", DOWN * 0.35)
        super().__init__(mob, **kw)


def eq(s, y):
    return MathTex(s).scale(EQ).move_to(UP * y).align_to(RIGHT * LEFT_X, LEFT)


def morph(scene, A, B, *glyph_map, run_time=2.0, **kw):
    """B alinhada à esquerda de A; depois do play a A restaurada sai da cena."""
    B.shift(A[0][0].get_left() - B[0][0].get_left())  # "y" de B exatamente sobre o "y" de A
    scene.play(TransformByGlyphMap(A, B, *glyph_map, **kw), run_time=run_time)
    scene.remove(A)


def swap(scene, old, text, *extra):
    new = screen_text(text, 24, color=GREY_B).move_to(old)
    scene.play(FadeOut(old), FadeIn(new), *extra, run_time=0.5)
    return new


def f(x):
    return (x + 3) ** 2 - 4


class MFToolsProductionTest(Scene):
    def construct(self):
        # NOTA: unbuff=0 porque o apply_unbuff do MF-Tools 1.4.9 usa np.cross em vetores 2D (erro no numpy 2.x)
        # ---- 0-3 s: título ----
        title = screen_text("COMPLETANDO O QUADRADO", 30, color=CYAN).set_width(7.4)
        sub = screen_text("sem esconder os passos", 22, color=GREY_B).next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(sub), title.animate.scale(0.6).move_to(UP * 6.9), run_time=0.8)

        # ---- 3-8 s: introduzir +9 -9 ----
        E1 = eq("y=x^2+6x+5", 2.0)
        cap = screen_text("somamos e subtraímos 9", 24, color=GREY_B).move_to(DOWN * 0.2)
        self.play(FadeIn(E1), run_time=0.7)
        self.wait(0.8)
        self.play(FadeIn(cap), run_time=0.4)
        E2 = eq("y=x^2+6x+9-9+5", 2.0)
        E2[0][8:12].set_color(ACCENT)  # os glifos novos entram coloridos
        morph(
            self, E1, E2,
            *[([i], [i]) for i in range(8)], ([8], [12]),
            ([], [8], {"delay": 0.0}),
            ([], [9, 10], {"delay": 0.6}),
            ([], [11], {"delay": 1.2}),
            default_introducer=PopIn, introduce_individually=True,
            run_time=2.2,
        )
        self.wait(0.6)

        # ---- 8-14 s: agrupar e fatorar ----
        rect = SurroundingRectangleUnion(*[E2[0][i] for i in range(2, 9)], buff=0.2, unbuff=0, color=CYAN, stroke_width=3)
        cap = swap(self, cap, "isto é um quadrado perfeito", Create(rect))
        self.wait(0.6)
        E3 = eq("y=(x+3)^2-9+5", 2.0)
        E3[0][5].set_color(CYAN)
        self.play(FadeOut(rect), run_time=0.3)
        morph(
            self, E2, E3,
            ([0], [0]), ([1], [1]), ([2], [3]),
            ([3], [7], {"path_arc": -PI * 0.8}),
            ([4], [4]), ([5], [5], {"delay": 0.4}),
            ([6, 7, 8], [], {"shift": UP * 0.4}),
            ([], [2], {"delay": 0.3}), ([], [6], {"delay": 0.6}),
            default_introducer=PopIn,
            run_time=2.4,
        )
        self.wait(0.8)

        # ---- 14-19 s: -9 + 5 = -4 ----
        cap = swap(self, cap, "−9 + 5 = −4")
        E4 = eq("y=(x+3)^2-4", 2.0)
        E4[0][9].set_color(CYAN)
        E3[0][5].set_color(WHITE)
        step4 = (dict(auto_morph=True) if STEP4_MODE == "morph" else dict(auto_fade=True))
        morph(self, E3, E4, ([i for i in range(9)], [i for i in range(9)]),
              auto_resolve_kwargs={"path_arc": -PI / 3}, run_time=2.0, **step4)
        E4[0][5].set_color(WHITE)
        self.play(FadeOut(cap), run_time=0.4)
        self.wait(1.4)

        # ---- 19-24 s: parábola, VT / DN ----
        self.play(E4.animate.scale(0.8).move_to(UP * 5.9), run_time=0.7)
        axes = Axes(
            x_range=[-7, 1, 1], y_range=[-5, 6, 1], x_length=7.6, y_length=7.2,
            axis_config={"color": GREY_B, "stroke_width": 2, "include_ticks": False, "include_tip": False},
        ).move_to(DOWN * 0.7)
        curve = axes.plot(f, x_range=[-6, 0], color=CYAN, stroke_width=4)
        vt = VT(0)
        dot = always_redraw(lambda: Dot(axes.c2p(~vt, f(~vt)), color=ACCENT, radius=0.12))
        xl, yl = MathTex("x=").scale(1.3), MathTex("y=").scale(1.3)
        xv, yv = DN(vt, num_decimal_places=2).scale(1.3).set_color(CYAN), DN(lambda: f(~vt), num_decimal_places=2).scale(1.3).set_color(CYAN)
        xl.move_to(LEFT * 2.2 + DOWN * 5.5); yl.next_to(xl, DOWN, buff=0.3, aligned_edge=RIGHT)
        xv.add_updater(lambda m: m.next_to(xl, RIGHT, buff=0.12)); yv.add_updater(lambda m: m.next_to(yl, RIGHT, buff=0.12))
        self.play(Create(axes), run_time=0.7)
        self.play(Create(curve), FadeIn(dot), FadeIn(xl), FadeIn(yl), FadeIn(xv), FadeIn(yv), run_time=1.0)
        self.play(vt @ -3, run_time=2.4, rate_func=smooth)

        # ---- 24-28 s: vértice ----
        self.wait(0.3)
        vtx = MathTex("(-3,\\,-4)").scale(0.9).set_color(ACCENT).next_to(dot, RIGHT, buff=0.35)
        vrect = SurroundingRectangleUnion(*[E4[0][i] for i in (4, 5, 8, 9)], unbuff=0, color=CYAN, stroke_width=3)
        vcap = screen_text("forma de vértice", 28, color=CYAN).move_to(DOWN * 7.2)
        self.play(Create(vrect), FadeIn(vtx), FadeIn(vcap), run_time=0.9)
        self.wait(3.0)

        # ---- 28-31 s: fechamento ----
        final = MathTex("y=(x+3)^2-4").scale(EQ * 1.1)
        self.play(
            *[FadeOut(m) for m in (axes, curve, dot, xl, yl, xv, yv, vtx, vcap, vrect, E4)],
            FadeIn(final), run_time=0.9,
        )
        note = screen_text("vértice em (−3, −4)", 26, color=CYAN).next_to(final, DOWN, buff=0.8)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.7)
        self.wait(2.2)


class MFToolsProductionDebug(Scene):
    """Só utilitários de depuração: show_indices, indexx_labels, bounding_box, retângulo em movimento."""

    def construct(self):
        A, B = MathTex("y=x^2+6x+5").scale(1.4), MathTex("y=(x+3)^2-4").scale(1.4)
        A.move_to(UP * 3.5)
        self.add(A)
        self.play(TransformByGlyphMap(A, B, show_indices=True))  # sem glyph_map => modo índices
        self.clear()
        C = MathTex("y=x^2+6x+9").scale(1.4).move_to(UP * 3)
        labels, box = indexx_labels(C, label_height=0.22), bounding_box(C, include_center=True)
        self.play(FadeIn(C), Create(labels), FadeIn(box))
        self.wait(1)
        # retângulo união seguindo glifos em movimento (always_redraw)
        self.clear()
        D = MathTex("x^2+6x+9").scale(1.4).move_to(LEFT * 1.5)
        rect = always_redraw(lambda: SurroundingRectangleUnion(*D[0][:4], unbuff=0, color=CYAN, stroke_width=3))
        self.add(D, rect)
        self.play(D.animate.shift(RIGHT * 3 + DOWN * 2).scale(1.3), run_time=1.5)
        self.play(D[0][1].animate.shift(UP * 1.2), run_time=1)  # glifo individual saindo do grupo
        self.wait(0.5)


class MFToolsFromCopy(Scene):
    """from_copy: a A original permanece enquanto B é construída a partir de cópias."""

    def construct(self):
        A = MathTex("(x+3)^2").scale(1.5).move_to(UP * 2.5)
        B = MathTex("x^2+6x+9").scale(1.5).move_to(DOWN * 0.5)
        self.add(A)
        self.play(TransformByGlyphMap(
            A, B, ([1], [0]), ([5], [1], {"path_arc": -PI / 2}), ([2], [2]), ([3], [3]), ([3], [6]),
            ([], [4, 5], {"delay": 0.3}), ([0, 4], []),
            from_copy=True, run_time=2.5,
        ))
        self.wait(1)


class MFToolsPureCompare(Scene):
    """Mesma transformação central com TransformMatchingTex puro."""

    def construct(self):
        A = MathTex("x^2", "+", "6x", "+", "9").scale(1.6)
        B = MathTex("(", "x", "+", "3", ")^2").scale(1.6).move_to(A, aligned_edge=LEFT)
        self.play(FadeIn(A))
        self.wait(0.6)
        self.play(TransformMatchingTex(A, B), run_time=2.0)
        self.wait(0.8)


class MFToolsMiscCheck(Scene):
    """Só confirma que Vcis e Arc3d importam/instanciam e renderizam."""

    def construct(self):
        a, b = Vcis(PI / 4) * 2, Vcis(PI / 4 + 1.2, clockwise=True) * 2
        arc = Arc3d(A=a, B=b, center=ORIGIN, radius=2)
        self.add(arc, Dot(a), Dot(b))
        self.wait(0.5)


class MFToolsAutoVariants(Scene):
    """Último passo (-9+5 -> -4): auto_morph vs auto_fade, lado a lado em sequência."""

    def construct(self):
        for kw in (dict(auto_morph=True, auto_resolve_kwargs={"path_arc": -PI / 3}), dict(auto_fade=True)):
            A, B = eq("y=(x+3)^2-9+5", 1.0), eq("y=(x+3)^2-4", 1.0)
            tag = screen_text(" + ".join(kw.keys()).replace("auto_resolve_kwargs", "kwargs"), 22, color=GREY_B).move_to(DOWN * 2)
            self.add(A, tag)
            self.wait(0.5)
            morph(self, A, B, ([i for i in range(9)], [i for i in range(9)]), run_time=2.0, **kw)
            self.wait(0.5)
            self.clear()
