"""Preview silencioso do vid_0015. Render: LinhasCarga015, 540×960 / 15 fps.

Campo de cada força: produzido pela linha 1 e avaliado na linha 2.
O desenho usa cargas positivas para fixar as orientações; os módulos usam |λ|, |I|.
MF-Tools considerado: matching simples e cancelamentos marcados bastam nesta cena.
"""
import json
from pathlib import Path
import sys

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config import BACKGROUND_COLOR, TEXT_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, WATERMARK_PATH
from template.fonts import screen_text

UNIT = Path(__file__).resolve().parent
E_COLOR = PRIMARY_COLOR
B_COLOR = "#EA63FF"
SURFACE_COLOR = SECONDARY_COLOR
MUTED = "#ADB8D1"


def label(text, size=26, color=TEXT_COLOR, width=7.8):
    mob = screen_text(text, font_size=size, color=color, oversample=2)
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def equation(tex, y=-1.15, size=43, color=TEXT_COLOR):
    mob = MathTex(tex, font_size=size, color=color)
    if mob.width > 7.7:
        mob.scale_to_fit_width(7.7)
    return mob.move_to([0, y, 0])


def arrow(a, b, color, width=5):
    return Arrow(a, b, buff=0, color=color, stroke_width=width,
                 max_tip_length_to_length_ratio=0.22)


def charged_line(x, number):
    wire = Line([x, 0.9, 0], [x, 4.15, 0], color=TEXT_COLOR, stroke_width=3)
    charges = VGroup(*[MathTex("+", font_size=24, color=E_COLOR).move_to([x, y, 0])
                       for y in np.linspace(1.2, 3.85, 6)])
    names = label(f"linha {number}", 20, MUTED).move_to([x, 0.5, 0])
    density = MathTex(r"\lambda", font_size=31, color=E_COLOR).move_to([x-0.43, 2.5, 0])
    speed = arrow([x+0.35, 3.25, 0], [x+0.35, 4.25, 0], E_COLOR)
    speed_label = MathTex("v", font_size=31, color=E_COLOR).move_to([x+0.72, 3.85, 0])
    return VGroup(wire, charges, names, density, speed, speed_label)


class LinhasCarga015(Scene):
    def checkpoint(self, name, hold=3):
        # Timestamps do MP4 para QA localizado; não desenha debug na cena.
        self.qa.append({"estado": name, "tempo_s": round(float(self.time + hold/2), 3)})
        self.wait(hold)

    def title_to(self, text):
        new = label(text, 35).move_to([0, 5.85, 0])
        self.play(Transform(self.title, new), run_time=0.7)

    def note_to(self, text, color=MUTED):
        new = label(text, 24, color).move_to([0, -5.45, 0])
        self.play(Transform(self.note, new), run_time=0.6)

    def replace_eq(self, old, tex, y=-1.15, size=43):
        new = equation(tex, y, size)
        self.play(TransformMatchingTex(old, new), run_time=1)
        return new

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.qa = []
        tag = label("EXERCÍCIO RESOLVIDO  /  015", 19, E_COLOR).move_to([0, 7.05, 0])
        self.title = label("Duas linhas carregadas", 35).move_to([0, 5.85, 0])
        subtitle = label("Infinitas, paralelas, no mesmo sentido", 23, MUTED).move_to([0, 4.95, 0])
        self.note = label("Representação: cargas positivas", 24, MUTED).move_to([0, -5.45, 0])
        watermark = ImageMobject(str(WATERMARK_PATH)).scale_to_fit_width(1.25)
        watermark.move_to([3.2, -6.75, 0]).set_opacity(0.45)
        self.add(tag, watermark)
        left = charged_line(-1.5, 1)
        right = charged_line(1.5, 2)
        separation = DoubleArrow([-1.5, 0, 0], [1.5, 0, 0], buff=0, color=MUTED, stroke_width=2)
        d_label = MathTex("d", font_size=28).move_to([0, -0.35, 0])
        question = label("Qual velocidade iguala os módulos?", 29).move_to([0, -1.5, 0])
        question_eq = equation(r"F_B=F_E\;?", -2.6, 46)
        self.play(FadeIn(self.title, subtitle, self.note), Create(left), Create(right),
                  GrowArrow(separation), FadeIn(d_label), run_time=1.4)
        self.play(FadeIn(question), Write(question_eq), run_time=1)
        self.checkpoint("enunciado_inicial", 4)

        fe = arrow([1.5, 2.8, 0], [3.65, 2.8, 0], E_COLOR)
        fe_label = MathTex("F_E", font_size=31, color=E_COLOR).move_to([2.85, 3.23, 0])
        fb = arrow([1.5, 1.75, 0], [-0.2, 1.75, 0], B_COLOR)
        fb_label = MathTex("F_B", font_size=31, color=B_COLOR).move_to([0.4, 1.3, 0])
        self.title_to("Repulsão elétrica")
        self.play(GrowArrow(fe), FadeIn(fe_label), run_time=0.8)
        self.checkpoint("repulsao_eletrica", 2)
        self.title_to("Atração magnética")
        self.play(GrowArrow(fb), FadeIn(fb_label), run_time=0.8)
        self.checkpoint("atracao_magnetica", 2)
        self.note_to("Campos da linha 1 → forças sobre a linha 2")
        self.checkpoint("forcas_iniciais", 2)

        self.title_to("Primeiro, o campo elétrico")
        self.play(FadeOut(right, fe, fe_label, fb, fb_label, separation, d_label,
                          question, question_eq, subtitle), left.animate.shift(RIGHT*1.5), run_time=1)
        self.note_to("Isolamos a linha 1: ela é a fonte do campo")
        source_label = label("linha 1", 20, MUTED).move_to([0, 0.35, 0])
        self.play(FadeOut(left[2]), FadeIn(source_label), run_time=0.5)
        radius = 1.4
        lateral = Rectangle(width=2*radius, height=3.2, stroke_color=SURFACE_COLOR,
                            fill_color=SURFACE_COLOR, fill_opacity=0.13).move_to([0, 2.5, 0])
        top = Ellipse(width=2*radius, height=0.7, color=SURFACE_COLOR,
                      fill_color=SURFACE_COLOR, fill_opacity=0.17).move_to([0, 4.1, 0])
        bottom = top.copy().move_to([0, 0.9, 0])
        cylinder = VGroup(lateral, top, bottom).set_z_index(-1)
        height_mark = DoubleArrow([-1.75, 0.9, 0], [-1.75, 4.1, 0], buff=0,
                                  color=MUTED, stroke_width=2)
        height_label = MathTex(r"\ell", font_size=30).move_to([-2.1, 2.5, 0])
        radius_mark = DashedLine([0, 2.5, 0], [radius, 2.5, 0], color=MUTED)
        radius_label = MathTex("d", font_size=29).move_to([0.7, 2.23, 0])
        self.play(Create(cylinder), GrowArrow(height_mark), FadeIn(height_label),
                  Create(radius_mark), FadeIn(radius_label), run_time=1.2)
        gauss_caption = label("GAUSS  ·  superfície fechada", 25, SURFACE_COLOR).move_to([0, -0.4, 0])
        self.play(FadeIn(gauss_caption), run_time=0.6)
        self.checkpoint("cilindro_gaussiano", 2)

        radial = VGroup(arrow([radius, 3, 0], [2.65, 3, 0], E_COLOR),
                        arrow([-radius, 3, 0], [-2.65, 3, 0], E_COLOR))
        radial_label = MathTex(r"\vec E\;\text{radial}", font_size=29, color=E_COLOR).move_to([2.35, 3.48, 0])
        side_area = arrow([radius, 1.7, 0], [2.4, 1.7, 0], SURFACE_COLOR)
        side_label = MathTex(r"d\vec A", font_size=27, color=SURFACE_COLOR).move_to([2.75, 1.7, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in radial], lag_ratio=0.2),
                  GrowArrow(side_area), FadeIn(radial_label, side_label), run_time=1)
        g = equation(r"\oint_{\mathcal S}\vec E\cdot d\vec A=\frac{Q_{\rm int}}{\varepsilon_0}")
        self.play(Write(g), run_time=1)
        self.note_to("Na lateral: campo e vetor área paralelos")
        self.checkpoint("campo_radial_lateral", 2)

        # Ambos os vetores E estão no plano de cada tampa; dA é axial, ±y.
        cap_vectors = VGroup()
        for y, sign in ((4.1, 1), (0.9, -1)):
            cap_vectors.add(arrow([0.7, y, 0], [1.6, y, 0], E_COLOR, 4),
                            arrow([0.7, y, 0], [0.7, y+sign*0.65, 0], SURFACE_COLOR, 4))
        cap_labels = VGroup(
            MathTex(r"d\vec A", font_size=24, color=SURFACE_COLOR).move_to([0.1, 4.6, 0]),
            MathTex(r"d\vec A", font_size=24, color=SURFACE_COLOR).move_to([0.1, 0.15, 0]),
            MathTex(r"\vec E", font_size=24, color=E_COLOR).move_to([1.88, 4.1, 0]),
            MathTex(r"\vec E", font_size=24, color=E_COLOR).move_to([1.88, 0.9, 0]))
        cap_zero = VGroup(
            equation(r"\Phi_{\rm tampa\ superior}=0", -2.45, 33),
            equation(r"\Phi_{\rm tampa\ inferior}=0", -3.25, 33),
            equation(r"\vec E\perp d\vec A\quad\text{em cada tampa}", -4.15, 30))
        self.play(*[GrowArrow(a) for a in cap_vectors], FadeIn(cap_labels), Write(cap_zero), run_time=1)
        self.note_to("Cada tampa tem fluxo zero individualmente")
        self.checkpoint("gauss_tampas", 4)
        self.play(FadeOut(cap_zero, cap_vectors, cap_labels), run_time=0.6)
        g = self.replace_eq(g, r"E(d)\,2\pi d\ell=\frac{|\lambda|\ell}{\varepsilon_0}")
        self.note_to("Só a lateral contribui para o fluxo")
        self.checkpoint("gauss_fluxo_lateral", 3)
        g = self.replace_eq(g, r"E(d)=\frac{|\lambda|}{2\pi\varepsilon_0 d}")
        self.checkpoint("campo_E", 3)
        electric_force = equation(r"\frac{F_E}{\ell}=|\lambda|E(d)=\frac{\lambda^2}{2\pi\varepsilon_0 d}", -2.7, 39, E_COLOR)
        self.play(Write(electric_force), run_time=1)
        self.note_to("Campo da linha 1 avaliado na posição da linha 2")
        self.checkpoint("forca_eletrica_por_comprimento", 3)

        # O cilindro se reduz a uma seção. A borda da seção vira a curva amperiana.
        self.title_to("Agora, o campo magnético")
        cut = Ellipse(width=2*radius, height=0.95, color=SURFACE_COLOR,
                      fill_color=SURFACE_COLOR, fill_opacity=0.18).move_to([0, 2.5, 0])
        small_electric = equation(r"\frac{F_E}{\ell}=\frac{\lambda^2}{2\pi\varepsilon_0 d}", -4.25, 33, E_COLOR)
        self.play(Transform(top, cut), bottom.animate.move_to([0, 2.5, 0]),
                  lateral.animate.stretch_to_fit_height(0.01),
                  FadeOut(radial, radial_label, side_area, side_label, height_mark, height_label, g),
                  TransformMatchingTex(electric_force, small_electric), run_time=1.4)
        self.note_to("Cortamos o cilindro perpendicularmente à linha")
        self.checkpoint("corte_gauss_ampere", 2)
        curve = Ellipse(width=2*radius, height=0.95, color=B_COLOR, stroke_width=4).move_to([0, 2.5, 0])
        amp_caption = label("AMPÈRE  ·  curva fechada", 25, B_COLOR).move_to([0, -0.4, 0])
        self.play(FadeOut(bottom, lateral), top.animate.set_fill(opacity=0),
                  Transform(top, curve), Transform(gauss_caption, amp_caption), run_time=1)
        current_label = MathTex("I", font_size=32, color=B_COLOR).move_to([0.72, 3.85, 0])
        self.play(left[4].animate.set_color(B_COLOR),
                  Transform(left[5], current_label), run_time=0.7)
        b_tangent = VGroup(arrow([-0.5, 2.025, 0], [0.55, 2.025, 0], B_COLOR, 4),
                           arrow([0.5, 2.975, 0], [-0.55, 2.975, 0], B_COLOR, 4))
        b_label = label("B azimutal", 23, B_COLOR).move_to([2.45, 2.25, 0])
        self.play(*[GrowArrow(a) for a in b_tangent], FadeIn(b_label), run_time=0.8)
        a = equation(r"\oint_{\mathcal C}\vec B\cdot d\vec\ell=\mu_0 I_{\rm int}")
        self.play(Write(a), run_time=1)
        self.note_to("Circulação do campo B ao longo de uma curva")
        self.checkpoint("ampere_curva_circulacao", 3)

        # Mão direita estilizada: polegar axial + quatro dedos curvados ao redor.
        thumb = arrow([-2.7, 1.95, 0], [-2.7, 3.65, 0], TEXT_COLOR, 6)
        fingers = VGroup(*[ArcBetweenPoints([-2.55, 2.1+i*0.23, 0], [-1.7, 2.1+i*0.23, 0],
                                           angle=-PI*0.85, color=TEXT_COLOR, stroke_width=3)
                          for i in range(4)])
        palm = ArcBetweenPoints([-2.75, 1.95, 0], [-1.7, 1.95, 0], angle=PI*0.45,
                                color=TEXT_COLOR, stroke_width=3)
        hand = VGroup(thumb, fingers, palm)
        rhr = VGroup(label("MÃO DIREITA", 21).move_to([-2.35, 4.3, 0]),
                     label("polegar ↑ I", 20).move_to([-2.3, 1.45, 0]),
                     label("dedos: B", 20, B_COLOR).move_to([-2.3, 1.0, 0]))
        cross = MathTex(r"\otimes", font_size=56, color=B_COLOR).move_to([radius, 2.5, 0])
        cross_label = label("entra na tela", 22, B_COLOR).move_to([2.65, 3.15, 0])
        self.title_to("Regra da mão direita")
        self.play(Create(hand), FadeIn(rhr, cross, cross_label), run_time=1)
        self.note_to("I para cima → B entra na tela à direita da linha 1")
        self.checkpoint("regra_mao_direita", 4)
        self.play(FadeOut(hand, rhr), run_time=0.6)
        a = self.replace_eq(a, r"B(d)\,2\pi d=\mu_0|I|")
        self.checkpoint("ampere_integral", 2)
        a = self.replace_eq(a, r"B(d)=\frac{\mu_0|I|}{2\pi d}")
        self.checkpoint("campo_B", 2)

        self.play(FadeOut(top, b_tangent, b_label, gauss_caption, radius_mark, radius_label, source_label),
                  left.animate.shift(LEFT*1.5), cross.animate.move_to([1.5, 2.5, 0]),
                  cross_label.animate.move_to([2.6, 2.0, 0]), run_time=1)
        # A linha 2 retorna no ponto onde o campo da linha 1 é avaliado.
        right = charged_line(1.5, 2)
        current2 = MathTex("I", font_size=32, color=B_COLOR).move_to([2.22, 3.85, 0])
        right[4].set_color(B_COLOR)
        right[5].become(current2)
        self.play(FadeIn(right), run_time=0.7)
        force_cross = equation(r"\vec F_B=I\vec\ell\times\vec B", -2.25, 39, B_COLOR)
        direction = equation(r"+\hat y\times(-\hat z)=-\hat x", -3.15, 34, B_COLOR)
        self.play(Write(force_cross), Write(direction), GrowArrow(fb), FadeIn(fb_label), run_time=1)
        self.note_to("Na linha 2: força magnética para a linha 1")
        self.checkpoint("produto_vetorial_atracao", 3)
        self.play(FadeOut(force_cross, direction, cross_label), run_time=0.6)
        magnetic_force = equation(r"\frac{F_B}{\ell}=|I|B(d)=\frac{\mu_0 I^2}{2\pi d}", -2.7, 39, B_COLOR)
        self.play(Write(magnetic_force), run_time=1)
        self.checkpoint("forca_magnetica_por_comprimento", 3)
        self.play(FadeOut(a, cross), GrowArrow(fe), FadeIn(fe_label), run_time=0.7)
        self.title_to("As duas forças coexistem")
        self.note_to("Repulsão elétrica e atração magnética: sentidos opostos")
        self.checkpoint("forcas_opostas", 4)

        self.title_to("Igualando os módulos")
        balance = MathTex(r"\frac{\lambda^2}{ {{2\pi}} \varepsilon_0 {{d}} }",
                          "=", r"\frac{\mu_0 I^2}{ {{2\pi}} {{d}} }", font_size=47, color=TEXT_COLOR)
        balance.move_to([0, -1.5, 0])
        # Na hipótese de igualdade, também igualamos os comprimentos das setas.
        # A exploração posterior restaura F_B/F_E = (v/c)², sempre abaixo de 1.
        self.play(FadeOut(magnetic_force, small_electric), Write(balance),
                  fb.animate.put_start_and_end_on([1.5, 1.75, 0], [-0.65, 1.75, 0]), run_time=1)
        self.checkpoint("igualar_modulos", 2)
        cancel = VGroup()
        for tex in (r"2\pi", "d"):
            for part in balance:
                if part.tex_string.strip() != tex:
                    continue
                cancel.add(Line(part.get_corner(DL)+0.08*DL, part.get_corner(UR)+0.08*UR,
                                color=E_COLOR, stroke_width=3))
        assert len(cancel) == 4, "Os dois denominadores devem ter 2π e d marcados."
        self.play(Create(cancel), run_time=0.8)
        self.note_to("Os fatores comuns 2π e d se cancelam")
        self.checkpoint("cancelamento_fatores", 2)
        simple = equation(r"\frac{\lambda^2}{\varepsilon_0}=\mu_0 I^2", -1.5, 48)
        self.play(FadeOut(cancel), TransformMatchingTex(balance, simple), run_time=1)
        self.checkpoint("equilibrio_reduzido", 2)
        simple = self.replace_eq(simple, r"\frac{|I|}{|\lambda|}=\frac{1}{\sqrt{\mu_0\varepsilon_0}}", -1.5, 45)
        c_def = equation(r"c=\frac{1}{\sqrt{\mu_0\varepsilon_0}}", -3.1, 37, E_COLOR)
        self.play(Write(c_def), run_time=0.8)
        simple = self.replace_eq(simple, r"\frac{|I|}{|\lambda|}=c", -1.5, 62)
        result_box = SurroundingRectangle(simple, color=E_COLOR, buff=0.27, corner_radius=0.12)
        self.play(Create(result_box), run_time=0.7)
        self.note_to("Esta é a condição de igualdade dos módulos")
        self.checkpoint("I_sobre_lambda_igual_c", 4)

        self.title_to("Volte ao v do enunciado")
        speed1 = MathTex("v", font_size=32, color=E_COLOR).move_to([-0.78, 3.85, 0])
        speed2 = MathTex("v", font_size=32, color=E_COLOR).move_to([2.22, 3.85, 0])
        self.play(Transform(left[5], speed1), Transform(right[5], speed2),
                  left[4].animate.set_color(E_COLOR), right[4].animate.set_color(E_COLOR),
                  FadeOut(c_def), run_time=0.8)
        self.play(Indicate(left[4:6], color=E_COLOR), Indicate(right[4:6], color=E_COLOR), run_time=1)
        return_text = label("Mas aqui a corrente é produzida justamente\npela própria linha de carga em movimento.",
                            24, TEXT_COLOR).move_to([0, -4.3, 0])
        self.play(FadeIn(return_text), run_time=0.6)
        self.note_to("A corrente vem do movimento da própria carga")
        self.checkpoint("retorno_ao_enunciado", 4)
        relation = equation(r"|I|=|\lambda|v", -3.0, 49, E_COLOR)
        self.play(Write(relation), run_time=1)
        self.checkpoint("corrente_lambda_v", 3)
        self.play(FadeOut(result_box), run_time=0.4)
        simple = self.replace_eq(simple, r"v=c", -1.5, 75)
        v_box = SurroundingRectangle(simple, color=E_COLOR, buff=0.3, corner_radius=0.12)
        self.play(Create(v_box), run_time=0.7)
        self.note_to("A igualdade exigiria a velocidade da luz")
        self.checkpoint("v_igual_c", 4)

        self.title_to("Explore o modelo ideal")
        self.play(FadeOut(simple, v_box, relation, return_text, fe, fe_label, fb, fb_label), run_time=0.8)
        model = label("MODELO IDEAL  ·  linhas infinitas de carga", 23, E_COLOR).move_to([0, 4.95, 0])
        model_note = label("v/c é um parâmetro do modelo", 22, MUTED).move_to([0, -4.65, 0])
        ratio = equation(r"\frac{F_B}{F_E}=\mu_0\varepsilon_0 v^2=\frac{v^2}{c^2}", -0.8, 44)
        self.play(FadeIn(model, model_note), Write(ratio), run_time=1)
        beta = ValueTracker(0.2)
        electric_arrow = arrow([1.5, 2.9, 0], [3.7, 2.9, 0], E_COLOR)
        magnetic_arrow = always_redraw(lambda: arrow([1.5, 1.9, 0],
                                  [1.5-2.2*beta.get_value()**2, 1.9, 0], B_COLOR))
        force_labels = VGroup(MathTex("F_E", font_size=30, color=E_COLOR).move_to([3, 3.3, 0]),
                              MathTex("F_B", font_size=30, color=B_COLOR).move_to([0.5, 1.35, 0]))
        track = Line([-2.8, -2.7, 0], [2.8, -2.7, 0], color=MUTED, stroke_width=3)
        knob = always_redraw(lambda: Dot([-2.8+5.6*beta.get_value(), -2.7, 0], radius=0.1, color=E_COLOR))
        limits = VGroup(MathTex("0", font_size=24).move_to([-2.8, -3.1, 0]),
                        MathTex("1", font_size=24).move_to([2.8, -3.1, 0]))
        limit_mark = Line([2.8, -2.9, 0], [2.8, -2.5, 0], color=B_COLOR, stroke_width=3)
        limit_text = label("limite c", 20, B_COLOR).move_to([2.8, -3.6, 0])
        beta_label = MathTex("v/c=", font_size=34).move_to([-0.7, -1.9, 0])
        beta_number = DecimalNumber(beta.get_value(), num_decimal_places=3, font_size=34, color=E_COLOR).move_to([0.9, -1.9, 0])
        beta_number.add_updater(lambda m: m.set_value(beta.get_value()))
        self.play(GrowArrow(electric_arrow), FadeIn(magnetic_arrow, force_labels, knob,
                  limits, limit_mark, limit_text, beta_label, beta_number), Create(track), run_time=0.8)
        self.note_to("Variamos o modelo; não aceleramos elétrons em um fio real")
        self.checkpoint("modelo_ideal_beta_020", 3)
        for value, name in ((0.6, "modelo_ideal_beta_060"), (0.85, "modelo_ideal_beta_085"),
                            (0.97, "modelo_ideal_beta_097"), (0.995, "modelo_ideal_beta_0995")):
            self.play(beta.animate.set_value(value), run_time=1.4, rate_func=smooth)
            self.checkpoint(name, 2)
        mass_limit = equation(r"\text{partículas massivas:}\quad v<c", -4.65, 33)
        self.play(FadeOut(model_note), FadeIn(mass_limit), run_time=0.8)
        self.note_to("A atração se aproxima da repulsão, mas não a ultrapassa")
        self.checkpoint("limite_particulas_massivas", 3)
        final_ratio = equation(r"\frac{F_B}{F_E}=\frac{v^2}{c^2}<1", -0.8, 51)
        self.play(TransformMatchingTex(ratio, final_ratio), beta.animate.set_value(0.75), run_time=1.4)
        self.title_to("Repulsão líquida")
        net = arrow([1.5, 0.65, 0], [1.5+2.2*(1-0.75**2), 0.65, 0], TEXT_COLOR)
        net_label = label("resultante", 21).move_to([2.4, 0.2, 0])
        net_eq = equation(r"\frac{F_{\text{líquida}}}{\ell}=\frac{\lambda^2}{2\pi\varepsilon_0 d}\left(1-\frac{v^2}{c^2}\right)>0", -3.9, 31)
        self.play(FadeOut(track, knob, limits, limit_mark, limit_text, beta_label, beta_number, mass_limit),
                  GrowArrow(net), FadeIn(net_label), Write(net_eq), run_time=1)
        self.note_to("Para v < c, a repulsão elétrica vence")
        self.checkpoint("comparacao_final_repulsao_liquida", 5)
        UNIT.joinpath("qa_estados.json").write_text(json.dumps({"duracao_cena_s": round(float(self.time), 3),
                  "estados": self.qa}, ensure_ascii=False, indent=2), encoding="utf-8")
