"""Script para gerar os 17 frames do GATE 1 para a V3.
Renderiza snapshots estáticos em 540x960 para inspeção e autocrítica (GATE 2)
antes do render do preview completo.
"""

import sys
import os
from pathlib import Path
import numpy as np
from manim import *

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from template.config import BACKGROUND_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text
from videos.vid_0024_queda_coriolis_leste.cena import (
    WHITE_COLOR, CYAN_COLOR, BLUE_COLOR, VIOLET_COLOR, MAGENTA_COLOR, MUTED_COLOR,
    label, formula, setup_header, build_torre, symbol_into_screen, glowing_ball
)

config.pixel_width = 540
config.pixel_height = 960
config.frame_width = 9
config.frame_height = 16
config.background_color = BACKGROUND_COLOR

OUT_DIR = UNIT / "gate1_v3_frames"
os.makedirs(OUT_DIR, exist_ok=True)


class Frame01_PerguntaInicial(Scene):
    def construct(self):
        setup_header(self)
        y_solo = -3.8
        y_topo = 4.2
        r_bola = 0.11
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.7)
        torre, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        y_bola_topo = y_topo + r_bola
        bola = glowing_ball([x_solt, y_bola_topo, 0])
        linha_ref = DashedLine([x_solt, y_bola_topo, 0], [x_solt, y_solo, 0], color=WHITE_COLOR, stroke_opacity=0.45, dash_length=0.14, dashed_ratio=0.5)
        marcador = VGroup(
            Line([x_solt - 0.18, y_solo, 0], [x_solt + 0.18, y_solo, 0], color=WHITE_COLOR, stroke_width=2.5),
            Line([x_solt, y_solo - 0.18, 0], [x_solt, y_solo + 0.18, 0], color=WHITE_COLOR, stroke_width=2.5),
            Dot([x_solt, y_solo, 0], radius=0.05, color=CYAN_COLOR)
        )
        t1 = label("SE EU SOLTAR A BOLA...", size=32, color=WHITE_COLOR, y=5.8)
        p1 = label("ELA CAI EXATAMENTE ", size=32, color=WHITE_COLOR)
        p2 = label("AQUI?", size=32, color=CYAN_COLOR)
        t2 = VGroup(p1, p2).arrange(RIGHT, buff=0.15).move_to([0, 5.2, 0])
        self.add(chao_linha, torre, bola, linha_ref, marcador, t1, t2)


class Frame02_GloboEquador(Scene):
    def construct(self):
        setup_header(self)
        t1 = label("VAMOS OLHAR O CASO MAIS LIMPO", size=28, color=WHITE_COLOR, y=5.6)
        t2 = label("EQUADOR  ·  50 m  ·  SEM ARRASTO", size=22, color=MUTED_COLOR, y=4.95)
        centro_globo = np.array([0.0, -0.4, 0.0])
        raio_globo = 2.4
        disco_terra = Circle(radius=raio_globo, stroke_width=2.5, stroke_color="#1F3A73", fill_color="#0A132C", fill_opacity=0.95).move_to(centro_globo)
        atmosfera = Circle(radius=raio_globo * 1.05, stroke_width=1.8, stroke_color=BLUE_COLOR, stroke_opacity=0.45).move_to(centro_globo)
        linha_equador = Line(centro_globo + LEFT * raio_globo, centro_globo + RIGHT * raio_globo, color=CYAN_COLOR, stroke_width=3.5)
        lbl_equador = label("EQUADOR", size=18, color=CYAN_COLOR, x=0, y=centro_globo[1] - 0.35)
        arco_rot_globo = Arc(radius=1.4, start_angle=-PI/4, angle=PI/2, arc_center=centro_globo, color=VIOLET_COLOR, stroke_width=3.0)
        p_end_rot = arco_rot_globo.point_from_proportion(1.0)
        p_prev_rot = arco_rot_globo.point_from_proportion(0.95)
        tan_dir_rot = (p_end_rot - p_prev_rot) / np.linalg.norm(p_end_rot - p_prev_rot)
        seta_rot_globo = Arrow(p_end_rot - tan_dir_rot * 0.28, p_end_rot, color=VIOLET_COLOR, buff=0, stroke_width=3.0, max_tip_length_to_length_ratio=0.38)
        lbl_omega_globo = formula(r"\vec{\omega}_T", size=32, color=VIOLET_COLOR, x=p_end_rot[0] + 0.45, y=p_end_rot[1] + 0.2)
        ponto_experimento = glowing_ball(centro_globo + RIGHT * 0.0, radius=0.13, color=WHITE_COLOR, glow_color=CYAN_COLOR)
        self.add(t1, t2, disco_terra, atmosfera, linha_equador, lbl_equador, arco_rot_globo, seta_rot_globo, lbl_omega_globo, ponto_experimento)


class Frame03_EquacaoProtagonistaRotulos(Scene):
    def construct(self):
        setup_header(self)
        tit = label("O QUE É A ACELERAÇÃO DE CORIOLIS?", size=28, color=WHITE_COLOR, y=5.5)
        eq_protagonista = MathTex(
            r"\vec{a}_C", r"=", r"-2", r"\vec{\omega}_T", r"\times", r"\vec{v}",
            font_size=44, color=WHITE_COLOR
        ).move_to([0, 3.8, 0])
        eq_protagonista[0].set_color(CYAN_COLOR)
        eq_protagonista[3].set_color(VIOLET_COLOR)
        eq_protagonista[5].set_color(BLUE_COLOR)
        box_protagonista = SurroundingRectangle(eq_protagonista, color=CYAN_COLOR, buff=0.25, stroke_width=2.0)
        item_ac = VGroup(formula(r"\vec{a}_C", size=32, color=CYAN_COLOR), label("aceleração aparente de Coriolis", size=22, color=WHITE_COLOR)).arrange(RIGHT, buff=0.3)
        item_w = VGroup(formula(r"\vec{\omega}_T", size=32, color=VIOLET_COLOR), label("velocidade angular da Terra", size=22, color=WHITE_COLOR)).arrange(RIGHT, buff=0.3)
        item_v = VGroup(formula(r"\vec{v}", size=32, color=BLUE_COLOR), label("velocidade do corpo relativa à Terra", size=22, color=WHITE_COLOR)).arrange(RIGHT, buff=0.3)
        tabela_variaveis = VGroup(item_ac, item_w, item_v).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0.2, 0.9, 0])
        frase = label("Ela surge ao descrever o movimento em um referencial que gira.", size=20, color=MUTED_COLOR, y=-1.5)
        self.add(tit, eq_protagonista, box_protagonista, tabela_variaveis, frase)


class Frame04_HasteEstadoInicial(Scene):
    def construct(self):
        setup_header(self)
        tit = label("POR QUE APARECE O FATOR 2?", size=30, color=WHITE_COLOR, y=5.5)
        pivo_pt = np.array([-1.5, 2.2, 0.0])
        pivo = Dot(pivo_pt, radius=0.09, color=WHITE_COLOR)
        pivo_anel = Circle(radius=0.18, color=WHITE_COLOR, stroke_width=1.5).move_to(pivo_pt)
        haste_linha = Line(pivo_pt, pivo_pt + RIGHT * 3.8, color=WHITE_COLOR, stroke_width=3.0)
        arco_haste_omega = Arc(radius=0.85, start_angle=-PI/12, angle=PI/3, arc_center=pivo_pt, color=VIOLET_COLOR, stroke_width=2.8)
        p_end_ho = arco_haste_omega.point_from_proportion(1.0)
        p_prev_ho = arco_haste_omega.point_from_proportion(0.95)
        tan_ho = (p_end_ho - p_prev_ho) / np.linalg.norm(p_end_ho - p_prev_ho)
        seta_haste_omega = Arrow(p_end_ho - tan_ho * 0.22, p_end_ho, color=VIOLET_COLOR, buff=0, stroke_width=2.8, max_tip_length_to_length_ratio=0.38)
        lbl_haste_omega = formula(r"\omega", size=30, color=VIOLET_COLOR, x=pivo_pt[0] + 0.95, y=pivo_pt[1] + 1.05)
        r1 = 1.3
        conta_pt = pivo_pt + RIGHT * r1
        conta = Dot(conta_pt, radius=0.13, color=BLUE_COLOR)
        vetor_u = Arrow(conta_pt, conta_pt + RIGHT * 1.05, color=BLUE_COLOR, buff=0, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        lbl_u = formula(r"u", size=30, color=BLUE_COLOR, x=conta_pt[0] + 0.55, y=conta_pt[1] - 0.38)
        def_u = VGroup(formula(r"u", size=26, color=BLUE_COLOR), label(": velocidade radial da conta", size=20, color=WHITE_COLOR)).arrange(RIGHT, buff=0.15)
        def_w = VGroup(formula(r"\omega", size=26, color=VIOLET_COLOR), label(": velocidade angular de rotação", size=20, color=WHITE_COLOR)).arrange(RIGHT, buff=0.15)
        defs_haste = VGroup(def_u, def_w).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0.2, 0.4, 0])
        self.add(tit, pivo, pivo_anel, haste_linha, arco_haste_omega, seta_haste_omega, lbl_haste_omega, conta, vetor_u, lbl_u, defs_haste)


class Frame05_PrimeiraContribuicao(Scene):
    def construct(self):
        setup_header(self)
        tit = label("POR QUE APARECE O FATOR 2?", size=30, color=WHITE_COLOR, y=5.5)
        pivo_pt = np.array([-1.5, 2.2, 0.0])
        pivo = Dot(pivo_pt, radius=0.09, color=WHITE_COLOR)
        pivo_anel = Circle(radius=0.18, color=WHITE_COLOR, stroke_width=1.5).move_to(pivo_pt)
        haste_linha = Line(pivo_pt, pivo_pt + RIGHT * 3.8, color=WHITE_COLOR, stroke_width=3.0)
        arco_haste_omega = Arc(radius=0.85, start_angle=-PI/12, angle=PI/3, arc_center=pivo_pt, color=VIOLET_COLOR, stroke_width=2.8)
        p_end_ho = arco_haste_omega.point_from_proportion(1.0)
        p_prev_ho = arco_haste_omega.point_from_proportion(0.95)
        tan_ho = (p_end_ho - p_prev_ho) / np.linalg.norm(p_end_ho - p_prev_ho)
        seta_haste_omega = Arrow(p_end_ho - tan_ho * 0.22, p_end_ho, color=VIOLET_COLOR, buff=0, stroke_width=2.8, max_tip_length_to_length_ratio=0.38)
        lbl_haste_omega = formula(r"\omega", size=30, color=VIOLET_COLOR, x=pivo_pt[0] + 0.95, y=pivo_pt[1] + 1.05)
        r1 = 1.3
        conta_pt = pivo_pt + RIGHT * r1
        ghost_conta = Dot(conta_pt, radius=0.13, color=BLUE_COLOR, fill_opacity=0.28)
        ghost_vt1 = Arrow(conta_pt, conta_pt + UP * 0.70, color=CYAN_COLOR, buff=0, stroke_width=2.5, stroke_opacity=0.30, max_tip_length_to_length_ratio=0.25)
        r2 = 2.6
        novo_conta_pt = pivo_pt + RIGHT * r2
        conta = Dot(novo_conta_pt, radius=0.13, color=BLUE_COLOR)
        vetor_u = Arrow(novo_conta_pt, novo_conta_pt + RIGHT * 1.05, color=BLUE_COLOR, buff=0, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        lbl_u = formula(r"u", size=30, color=BLUE_COLOR, x=novo_conta_pt[0] + 0.55, y=novo_conta_pt[1] - 0.38)
        vetor_vt2 = Arrow(novo_conta_pt, novo_conta_pt + UP * 1.40, color=CYAN_COLOR, buff=0, stroke_width=3.5, max_tip_length_to_length_ratio=0.25)
        diff_vt = Arrow(novo_conta_pt + UP * 0.70, novo_conta_pt + UP * 1.40, color=CYAN_COLOR, buff=0, stroke_width=5.0, max_tip_length_to_length_ratio=0.30)
        lbl_diff_vt = formula(r"\Delta v_t", size=24, color=CYAN_COLOR, x=novo_conta_pt[0] + 0.5, y=novo_conta_pt[1] + 1.1)
        lbl_b_step1 = formula(r"dr = u\,dt \implies dv_t = \omega\,dr = \omega u\,dt", size=26, color=WHITE_COLOR, x=0, y=0.5)
        eq_a1 = formula(r"a_1 = \frac{dv_t}{dt} = \omega u", size=32, color=WHITE_COLOR, x=0, y=-0.3)
        box_a1 = SurroundingRectangle(eq_a1, color=CYAN_COLOR, buff=0.18, stroke_width=1.8)
        desc_a1 = label("efeito 1: velocidade tangencial aumenta com o raio", size=18, color=CYAN_COLOR, x=0, y=-1.35, width=7.6)
        self.add(tit, pivo, pivo_anel, haste_linha, arco_haste_omega, seta_haste_omega, lbl_haste_omega,
                 ghost_conta, ghost_vt1, conta, vetor_u, lbl_u, vetor_vt2, diff_vt, lbl_diff_vt,
                 lbl_b_step1, eq_a1, box_a1, desc_a1)


class Frame06_SegundaContribuicao(Scene):
    def construct(self):
        setup_header(self)
        tit = label("POR QUE APARECE O FATOR 2?", size=30, color=WHITE_COLOR, y=5.5)
        pivo_pt = np.array([-1.5, 2.2, 0.0])
        pivo = Dot(pivo_pt, radius=0.09, color=WHITE_COLOR)
        pivo_anel = Circle(radius=0.18, color=WHITE_COLOR, stroke_width=1.5).move_to(pivo_pt)
        ghost_haste_linha = Line(pivo_pt, pivo_pt + RIGHT * 3.8, color=WHITE_COLOR, stroke_width=2.0, stroke_opacity=0.30)
        ghost_u_mid = Arrow(pivo_pt + RIGHT * 1.8, pivo_pt + RIGHT * 2.85, color=BLUE_COLOR, buff=0, stroke_width=3.0, stroke_opacity=0.30, max_tip_length_to_length_ratio=0.25)
        dtheta = 22 * PI / 180
        arco_dtheta = Arc(radius=1.1, start_angle=0, angle=dtheta, arc_center=pivo_pt, color=VIOLET_COLOR, stroke_width=2.4)
        lbl_dtheta = formula(r"d\theta = \omega\,dt", size=24, color=VIOLET_COLOR, x=pivo_pt[0] + 1.7, y=pivo_pt[1] + 1.0)
        mat_rot = np.array([[np.cos(dtheta), -np.sin(dtheta), 0],
                            [np.sin(dtheta),  np.cos(dtheta), 0],
                            [0,               0,              1]])
        r_mid = 1.8
        pos_c_rot = pivo_pt + mat_rot @ (RIGHT * r_mid)
        u_rot_end = pos_c_rot + mat_rot @ (RIGHT * 1.05)
        haste_linha_rot = Line(pivo_pt, pivo_pt + mat_rot @ (RIGHT * 3.8), color=WHITE_COLOR, stroke_width=3.0)
        conta = Dot(pos_c_rot, radius=0.13, color=BLUE_COLOR)
        vetor_u = Arrow(pos_c_rot, u_rot_end, color=BLUE_COLOR, buff=0, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        delta_u_seta = Arrow(pos_c_rot + RIGHT * 1.05, u_rot_end, color=CYAN_COLOR, buff=0, stroke_width=4.5, max_tip_length_to_length_ratio=0.35)
        lbl_c_step1 = formula(r"d\theta = \omega\,dt \implies |d\vec{v}| \approx u\,d\theta = u\omega\,dt", size=26, color=WHITE_COLOR, x=0, y=0.5)
        eq_a2 = formula(r"a_2 = \frac{|d\vec{v}|}{dt} = \omega u", size=32, color=WHITE_COLOR, x=0, y=-0.3)
        box_a2 = SurroundingRectangle(eq_a2, color=CYAN_COLOR, buff=0.18, stroke_width=1.8)
        desc_a2 = label(r"efeito 2: direção da velocidade radial gira no espaço", size=18, color=CYAN_COLOR, x=0, y=-1.35, width=7.6)
        self.add(tit, pivo, pivo_anel, ghost_haste_linha, ghost_u_mid, haste_linha_rot, arco_dtheta, lbl_dtheta,
                 conta, vetor_u, delta_u_seta, lbl_c_step1, eq_a2, box_a2, desc_a2)


class Frame07_SomaFator2(Scene):
    def construct(self):
        setup_header(self)
        tit = label("DOIS EFEITOS INDEPENDENTES SE SOMAM", size=26, color=WHITE_COLOR, y=5.4)
        eq_soma = formula(
            r"a_{\text{tang}}", r"=", r"\underbrace{\omega u}_{v_t\ \text{aumenta}}", r"+", r"\underbrace{\omega u}_{\hat{r}\ \text{gira}}",
            size=36, color=WHITE_COLOR, y=2.2
        )
        eq_soma[2].set_color(CYAN_COLOR)
        eq_soma[4].set_color(CYAN_COLOR)
        eq_fator_2 = formula(r"a_{\text{tang}} = 2\omega u", size=48, color=WHITE_COLOR, y=0.5)
        eq_fator_2[0][6].set_color(CYAN_COLOR)
        box_fator_2 = SurroundingRectangle(eq_fator_2, color=CYAN_COLOR, buff=0.28, stroke_width=2.5)
        desc_fator_2 = label("daqui nasce o fator 2 da aceleração transversal!", size=22, color=CYAN_COLOR, y=-0.7)
        self.add(tit, eq_soma, eq_fator_2, box_fator_2, desc_fator_2)


class Frame08_TransicaoCoriolis(Scene):
    def construct(self):
        setup_header(self)
        tit = label("DO REFERENCIAL INERCIAL AO GIRANTE", size=26, color=WHITE_COLOR, y=5.4)
        eq_f2 = formula(r"a_{\text{tang}} = 2\omega u", size=36, color=WHITE_COLOR, y=3.4)
        eq_f2[0][6].set_color(CYAN_COLOR)
        t_in = label("No referencial inercial: aceleração real de arraste", size=20, color=MUTED_COLOR, y=2.6)
        t_gi = label("No referencial que gira: surge a força inercial aparente oposta", size=20, color=CYAN_COLOR, y=1.9)
        eq_fc = formula(r"\vec{F}_C = -2m\,\vec{\omega}\times\vec{v}", size=36, color=WHITE_COLOR, y=0.6)
        txt_m = label(r"dividindo pela massa m:", size=20, color=MUTED_COLOR, y=-0.2)
        eq_ac = formula(r"\vec{a}_C = -2\vec{\omega}\times\vec{v}", size=42, color=WHITE_COLOR, y=-1.1)
        eq_ac[0][:3].set_color(CYAN_COLOR)
        box_ac = SurroundingRectangle(eq_ac, color=CYAN_COLOR, buff=0.25, stroke_width=2.2)
        self.add(tit, eq_f2, t_in, t_gi, eq_fc, txt_m, eq_ac, box_ac)


class Frame09_ReferencialLocalTorre(Scene):
    def construct(self):
        setup_header(self)
        y_solo = -3.8
        y_topo = 4.2
        r_bola = 0.11
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.7)
        torre, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        y_bola_topo = y_topo + r_bola
        bola = glowing_ball([x_solt, y_bola_topo, 0])
        linha_ref = DashedLine([x_solt, y_bola_topo, 0], [x_solt, y_solo, 0], color=WHITE_COLOR, stroke_opacity=0.45, dash_length=0.14, dashed_ratio=0.5)
        marcador = Dot([x_solt, y_solo, 0], radius=0.07, color=WHITE_COLOR)
        eixo_x = Arrow(ORIGIN, RIGHT * 1.1, color=CYAN_COLOR, buff=0, stroke_width=2.5).move_to([2.1, 4.8, 0])
        lbl_eixo_x = formula(r"+x\ \text{leste}", size=19, color=CYAN_COLOR).next_to(eixo_x, DOWN, buff=0.10)
        eixo_z = Arrow(ORIGIN, UP * 1.0, color=WHITE_COLOR, buff=0, stroke_width=2.5).move_to([1.2, 5.2, 0])
        lbl_eixo_z = formula(r"+z\ \text{cima}", size=19, color=WHITE_COLOR).next_to(eixo_z, UP, buff=0.10)
        simbolo_norte = symbol_into_screen([3.1, 5.2, 0], radius=0.16, color=VIOLET_COLOR)
        lbl_norte = formula(r"\vec{\omega}_T\ \otimes", size=21, color=VIOLET_COLOR).next_to(simbolo_norte, RIGHT, buff=0.12)
        txt_solt = label("NO INSTANTE DA SOLTURA", size=22, color=MUTED_COLOR, x=1.5, y=3.2)
        eq_rot = formula(r"\vec{\omega}_T = \omega_T\,\hat{y}\ \ (\text{norte})", size=24, color=VIOLET_COLOR, x=1.5, y=2.5)
        self.add(chao_linha, torre, bola, linha_ref, marcador, eixo_x, lbl_eixo_x, eixo_z, lbl_eixo_z, simbolo_norte, lbl_norte, txt_solt, eq_rot)


class Frame10_SolturaV0(Scene):
    def construct(self):
        setup_header(self)
        y_solo = -3.8
        y_topo = 4.2
        r_bola = 0.11
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.7)
        torre, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        bola = glowing_ball([x_solt, y_topo + r_bola, 0])
        linha_ref = DashedLine([x_solt, y_topo + r_bola, 0], [x_solt, y_solo, 0], color=WHITE_COLOR, stroke_opacity=0.45, dash_length=0.14, dashed_ratio=0.5)
        marcador = Dot([x_solt, y_solo, 0], radius=0.07, color=WHITE_COLOR)
        eixo_x = Arrow(ORIGIN, RIGHT * 1.1, color=CYAN_COLOR, buff=0, stroke_width=2.5).move_to([2.1, 4.8, 0])
        lbl_eixo_x = formula(r"+x\ \text{leste}", size=19, color=CYAN_COLOR).next_to(eixo_x, DOWN, buff=0.10)
        eixo_z = Arrow(ORIGIN, UP * 1.0, color=WHITE_COLOR, buff=0, stroke_width=2.5).move_to([1.2, 5.2, 0])
        lbl_eixo_z = formula(r"+z\ \text{cima}", size=19, color=WHITE_COLOR).next_to(eixo_z, UP, buff=0.10)
        simbolo_norte = symbol_into_screen([3.1, 5.2, 0], radius=0.16, color=VIOLET_COLOR)
        lbl_norte = formula(r"\vec{\omega}_T\ \otimes", size=21, color=VIOLET_COLOR).next_to(simbolo_norte, RIGHT, buff=0.12)
        txt_solt = label("NO INSTANTE DA SOLTURA", size=22, color=MUTED_COLOR, x=1.5, y=3.2)
        eq_rot = formula(r"\vec{\omega}_T = \omega_T\,\hat{y}\ \ (\text{norte})", size=24, color=VIOLET_COLOR, x=1.5, y=2.5)
        eq_v0 = formula(r"\vec{v} = 0", size=32, color=BLUE_COLOR, x=1.5, y=1.7)
        eq_ac_v0 = formula(r"\vec{a}_C = -2\vec{\omega}_T\times\vec{0} = \vec{0}", size=28, color=WHITE_COLOR, x=1.5, y=0.9)
        lbl_sem = label("inicialmente não há desvio!", size=20, color=CYAN_COLOR, x=1.5, y=0.1)
        self.add(chao_linha, torre, bola, linha_ref, marcador, eixo_x, lbl_eixo_x, eixo_z, lbl_eixo_z, simbolo_norte, lbl_norte, txt_solt, eq_rot, eq_v0, eq_ac_v0, lbl_sem)


class Frame11_SubstituicaoVetorialQueda(Scene):
    def construct(self):
        setup_header(self)
        y_solo = -3.8
        y_topo = 4.2
        r_bola = 0.11
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.7)
        torre, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        bola = glowing_ball([x_solt, y_topo + r_bola, 0])
        linha_ref = DashedLine([x_solt, y_topo + r_bola, 0], [x_solt, y_solo, 0], color=WHITE_COLOR, stroke_opacity=0.45, dash_length=0.14, dashed_ratio=0.5)
        marcador = Dot([x_solt, y_solo, 0], radius=0.07, color=WHITE_COLOR)
        eixo_x = Arrow(ORIGIN, RIGHT * 1.1, color=CYAN_COLOR, buff=0, stroke_width=2.5).move_to([2.1, 4.8, 0])
        lbl_eixo_x = formula(r"+x\ \text{leste}", size=19, color=CYAN_COLOR).next_to(eixo_x, DOWN, buff=0.10)
        eixo_z = Arrow(ORIGIN, UP * 1.0, color=WHITE_COLOR, buff=0, stroke_width=2.5).move_to([1.2, 5.2, 0])
        lbl_eixo_z = formula(r"+z\ \text{cima}", size=19, color=WHITE_COLOR).next_to(eixo_z, UP, buff=0.10)
        simbolo_norte = symbol_into_screen([3.1, 5.2, 0], radius=0.16, color=VIOLET_COLOR)
        lbl_norte = formula(r"\vec{\omega}_T\ \otimes", size=21, color=VIOLET_COLOR).next_to(simbolo_norte, RIGHT, buff=0.12)
        eq_v_desc = formula(r"\vec{v} \approx -gt\,\hat{z}", size=28, color=BLUE_COLOR, x=1.5, y=3.2)
        lbl_v_desc = label("velocidade vertical para baixo", size=18, color=BLUE_COLOR, x=1.5, y=2.7)
        eq_sub1 = formula(r"\vec{a}_C = -2(\omega_T\hat{y})\times(-gt\hat{z})", size=26, color=WHITE_COLOR, x=1.5, y=1.9)
        regra_cruz = formula(r"\hat{y}\times\hat{z} = \hat{x} \quad (\text{norte}\times\text{cima} = \text{leste})", size=21, color=MUTED_COLOR, x=1.5, y=1.2)
        eq_sub2 = formula(r"\vec{a}_C = 2\omega_T gt\,\hat{x}", size=30, color=CYAN_COLOR, x=1.5, y=0.4)
        lbl_dest = label("ACELERAÇÃO PARA LESTE (+x)", size=20, color=CYAN_COLOR, x=1.5, y=-0.2)
        self.add(chao_linha, torre, bola, linha_ref, marcador, eixo_x, lbl_eixo_x, eixo_z, lbl_eixo_z, simbolo_norte, lbl_norte, eq_v_desc, lbl_v_desc, eq_sub1, regra_cruz, eq_sub2, lbl_dest)


class Frame12_AxResultado(Scene):
    def construct(self):
        setup_header(self)
        y_solo = -3.8
        y_topo = 4.2
        r_bola = 0.11
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.7)
        torre, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        y_bola_topo = y_topo + r_bola
        B_exag = 2.2
        bola = glowing_ball([x_solt + B_exag, y_solo, 0])
        linha_ref = DashedLine([x_solt, y_bola_topo, 0], [x_solt, y_solo, 0], color=WHITE_COLOR, stroke_opacity=0.45, dash_length=0.14, dashed_ratio=0.5)
        marcador = Dot([x_solt, y_solo, 0], radius=0.07, color=WHITE_COLOR)
        # Trajetória curva exagerada
        pts = [[x_solt + B_exag * (s**3), y_bola_topo - (y_bola_topo - y_solo)*(s**2), 0] for s in np.linspace(0, 1.0, 40)]
        curva = VMobject(color=CYAN_COLOR, stroke_width=3.0)
        curva.set_points_as_corners(pts)
        eixo_x = Arrow(ORIGIN, RIGHT * 1.1, color=CYAN_COLOR, buff=0, stroke_width=2.5).move_to([2.1, 4.8, 0])
        lbl_eixo_x = formula(r"+x\ \text{leste}", size=19, color=CYAN_COLOR).next_to(eixo_x, DOWN, buff=0.10)
        eixo_z = Arrow(ORIGIN, UP * 1.0, color=WHITE_COLOR, buff=0, stroke_width=2.5).move_to([1.2, 5.2, 0])
        lbl_eixo_z = formula(r"+z\ \text{cima}", size=19, color=WHITE_COLOR).next_to(eixo_z, UP, buff=0.10)
        simbolo_norte = symbol_into_screen([3.1, 5.2, 0], radius=0.16, color=VIOLET_COLOR)
        lbl_norte = formula(r"\vec{\omega}_T\ \otimes", size=21, color=VIOLET_COLOR).next_to(simbolo_norte, RIGHT, buff=0.12)
        eq_ax = formula(r"a_x = 2\omega_T gt", size=36, color=CYAN_COLOR, x=1.5, y=0.0)
        box_ax = SurroundingRectangle(eq_ax, color=CYAN_COLOR, buff=0.20, stroke_width=2.0)
        self.add(chao_linha, torre, bola, linha_ref, marcador, curva, eixo_x, lbl_eixo_x, eixo_z, lbl_eixo_z, simbolo_norte, lbl_norte, eq_ax, box_ax)


class Frame13_CadeiaIntegracoes(Scene):
    def construct(self):
        setup_header(self)
        y_solo = -3.8
        y_topo = 4.2
        r_bola = 0.11
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.7)
        torre, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        y_bola_topo = y_topo + r_bola
        B_exag = 2.2
        bola = glowing_ball([x_solt + B_exag, y_solo, 0])
        linha_ref = DashedLine([x_solt, y_bola_topo, 0], [x_solt, y_solo, 0], color=WHITE_COLOR, stroke_opacity=0.45, dash_length=0.14, dashed_ratio=0.5)
        marcador = Dot([x_solt, y_solo, 0], radius=0.07, color=WHITE_COLOR)
        pts = [[x_solt + B_exag * (s**3), y_bola_topo - (y_bola_topo - y_solo)*(s**2), 0] for s in np.linspace(0, 1.0, 40)]
        curva = VMobject(color=CYAN_COLOR, stroke_width=3.0)
        curva.set_points_as_corners(pts)
        eixo_x = Arrow(ORIGIN, RIGHT * 1.1, color=CYAN_COLOR, buff=0, stroke_width=2.5).move_to([2.1, 4.8, 0])
        lbl_eixo_x = formula(r"+x\ \text{leste}", size=19, color=CYAN_COLOR).next_to(eixo_x, DOWN, buff=0.10)
        eixo_z = Arrow(ORIGIN, UP * 1.0, color=WHITE_COLOR, buff=0, stroke_width=2.5).move_to([1.2, 5.2, 0])
        lbl_eixo_z = formula(r"+z\ \text{cima}", size=19, color=WHITE_COLOR).next_to(eixo_z, UP, buff=0.10)
        simbolo_norte = symbol_into_screen([3.1, 5.2, 0], radius=0.16, color=VIOLET_COLOR)
        lbl_norte = formula(r"\vec{\omega}_T\ \otimes", size=21, color=VIOLET_COLOR).next_to(simbolo_norte, RIGHT, buff=0.12)
        eq_ax = formula(r"a_x = 2\omega_T gt", size=32, color=CYAN_COLOR, x=1.5, y=2.8)
        box_ax = SurroundingRectangle(eq_ax, color=CYAN_COLOR, buff=0.18, stroke_width=1.6)
        txt_int1 = formula(r"\Downarrow\ \int dt \quad [v_x(0) = 0]", size=22, color=MUTED_COLOR, x=1.5, y=2.0)
        eq_vx = formula(r"v_x(t) = \omega_T gt^2", size=34, color=CYAN_COLOR, x=1.5, y=1.2)
        box_vx = SurroundingRectangle(eq_vx, color=CYAN_COLOR, buff=0.18, stroke_width=1.8)
        txt_int2 = formula(r"\Downarrow\ \int dt \quad [x(0) = 0]", size=22, color=MUTED_COLOR, x=1.5, y=0.35)
        eq_x = formula(r"x(t) = \frac{1}{3}\omega_T gt^3", size=38, color=CYAN_COLOR, x=1.5, y=-0.5)
        box_x = SurroundingRectangle(eq_x, color=CYAN_COLOR, buff=0.22, stroke_width=2.5)
        self.add(chao_linha, torre, bola, linha_ref, marcador, curva, eixo_x, lbl_eixo_x, eixo_z, lbl_eixo_z, simbolo_norte, lbl_norte,
                 eq_ax, box_ax, txt_int1, eq_vx, box_vx, txt_int2, eq_x, box_x)


class Frame14_Bloco50mTempo(Scene):
    def construct(self):
        setup_header(self)
        y_solo = -3.8
        y_topo = 4.2
        r_bola = 0.11
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.7)
        torre, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        y_bola_topo = y_topo + r_bola
        B_exag = 2.2
        bola = glowing_ball([x_solt + B_exag, y_solo, 0])
        linha_ref = DashedLine([x_solt, y_bola_topo, 0], [x_solt, y_solo, 0], color=WHITE_COLOR, stroke_opacity=0.45, dash_length=0.14, dashed_ratio=0.5)
        marcador = Dot([x_solt, y_solo, 0], radius=0.07, color=WHITE_COLOR)
        pts = [[x_solt + B_exag * (s**3), y_bola_topo - (y_bola_topo - y_solo)*(s**2), 0] for s in np.linspace(0, 1.0, 40)]
        curva = VMobject(color=CYAN_COLOR, stroke_width=3.0)
        curva.set_points_as_corners(pts)
        cota_h = VGroup(
            Line([-2.3, y_topo, 0], [-2.3, y_solo, 0], color=WHITE_COLOR, stroke_width=1.6),
            Line([-2.45, y_topo, 0], [-2.15, y_topo, 0], color=WHITE_COLOR, stroke_width=1.6),
            Line([-2.45, y_solo, 0], [-2.15, y_solo, 0], color=WHITE_COLOR, stroke_width=1.6),
            formula(r"h = 50\,\mathrm{m}", size=24, color=WHITE_COLOR).move_to([-3.1, (y_topo + y_solo) / 2, 0])
        )
        eq_tf_formula = formula(r"t_f = \sqrt{\frac{2h}{g}}", size=32, color=WHITE_COLOR, x=1.5, y=1.8)
        eq_tf_valor = formula(r"t_f \approx 3{,}19\,\mathrm{s}", size=36, color=WHITE_COLOR, x=1.5, y=0.8)
        box_tf = SurroundingRectangle(eq_tf_valor, color=WHITE_COLOR, buff=0.18, stroke_width=1.8)
        eq_x = formula(r"x = \frac{1}{3}\omega_T gt^3", size=36, color=CYAN_COLOR, x=1.5, y=-1.2)
        box_x = SurroundingRectangle(eq_x, color=CYAN_COLOR, buff=0.20, stroke_width=2.0)
        self.add(chao_linha, torre, bola, linha_ref, marcador, curva, cota_h, eq_tf_formula, eq_tf_valor, box_tf, eq_x, box_x)


class Frame15_PayoffResultado(Scene):
    def construct(self):
        setup_header(self)
        eq_x = formula(r"x = \frac{1}{3}\omega_T gt^3", size=36, color=WHITE_COLOR, x=0, y=3.0)
        box_x = SurroundingRectangle(eq_x, color=WHITE_COLOR, buff=0.20, stroke_width=1.8)
        const_omega = formula(r"\omega_T \approx 7{,}29\times 10^{-5}\,\mathrm{rad/s}", size=24, color=MUTED_COLOR, x=0, y=1.9)
        const_g_tf = formula(r"g \approx 9{,}8\,\mathrm{m/s^2} \quad t_f \approx 3{,}19\,\mathrm{s}", size=24, color=MUTED_COLOR, x=0, y=1.3)
        res_cm = formula(r"x \approx 0{,}77\ \mathrm{cm}", size=56, color=CYAN_COLOR, x=0, y=-0.3)
        box_res_cm = SurroundingRectangle(res_cm, color=CYAN_COLOR, buff=0.30, stroke_width=3.0)
        lbl_leste_payoff = label("PARA LESTE", size=32, color=CYAN_COLOR, x=0, y=-1.5)
        self.add(eq_x, box_x, const_omega, const_g_tf, res_cm, box_res_cm, lbl_leste_payoff)


class Frame16_EscalaRealAmpliacao(Scene):
    def construct(self):
        setup_header(self)
        y_solo = -3.8
        y_topo = 4.2
        r_bola = 0.11
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.7)
        torre, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        y_bola_topo = y_topo + r_bola
        # Quase perfeitamente vertical na escala real
        bola = glowing_ball([x_solt + 0.015, y_solo, 0])
        linha_ref = DashedLine([x_solt, y_bola_topo, 0], [x_solt, y_solo, 0], color=WHITE_COLOR, stroke_opacity=0.45, dash_length=0.14, dashed_ratio=0.5)
        marcador = Dot([x_solt, y_solo, 0], radius=0.07, color=WHITE_COLOR)
        lbl_escala_real = label("ESCALA FÍSICA REAL", size=24, color=WHITE_COLOR, x=1.5, y=3.2)
        centro_lupa = np.array([1.5, -0.8, 0.0])
        raio_lupa = 1.65
        disco_lupa = Circle(radius=raio_lupa, color=CYAN_COLOR, stroke_width=2.4, fill_color="#091024", fill_opacity=0.96).move_to(centro_lupa)
        linha_solo_lupa = Line(centro_lupa + LEFT * 1.5 + DOWN * 0.45, centro_lupa + RIGHT * 1.5 + DOWN * 0.45, color=MUTED_COLOR, stroke_width=1.5)
        x_abaixo = centro_lupa[0] - 0.85
        x_impacto = centro_lupa[0] + 0.85
        y_pts_lupa = centro_lupa[1] - 0.45
        ponto_abaixo_lupa = Dot([x_abaixo, y_pts_lupa, 0], radius=0.08, color=WHITE_COLOR)
        lbl_abaixo_lupa = label("ponto abaixo", size=15, color=MUTED_COLOR, x=x_abaixo - 0.15, y=y_pts_lupa - 0.38)
        ponto_impacto_lupa = Dot([x_impacto, y_pts_lupa, 0], radius=0.08, color=CYAN_COLOR)
        lbl_impacto_lupa = label("impacto real", size=15, color=CYAN_COLOR, x=x_impacto + 0.15, y=y_pts_lupa - 0.38)
        seta_desvio = Arrow([x_abaixo, y_pts_lupa + 0.28, 0], [x_impacto, y_pts_lupa + 0.28, 0], color=CYAN_COLOR, buff=0, stroke_width=3.5, max_tip_length_to_length_ratio=0.25)
        valor_desvio_txt = formula(r"0{,}77\,\mathrm{cm}", size=28, color=CYAN_COLOR, x=centro_lupa[0], y=y_pts_lupa + 0.65)
        titulo_inset = label("AMPLIAÇÃO CIENTÍFICA", size=18, color=WHITE_COLOR, x=centro_lupa[0], y=centro_lupa[1] + 1.25)
        grupo_lupa = VGroup(disco_lupa, linha_solo_lupa, ponto_abaixo_lupa, lbl_abaixo_lupa, ponto_impacto_lupa, lbl_impacto_lupa, seta_desvio, valor_desvio_txt, titulo_inset)
        self.add(chao_linha, torre, bola, linha_ref, marcador, lbl_escala_real, grupo_lupa)


class Frame17_FechamentoFinal(Scene):
    def construct(self):
        setup_header(self)
        y_solo = -3.8
        y_topo = 4.2
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.06)
        torre, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        torre.set_opacity(0.06)
        f1 = label("A OLHO NU,", size=32, color=WHITE_COLOR, y=2.2)
        f2 = label("A QUEDA PARECE VERTICAL.", size=32, color=WHITE_COLOR, y=1.5)
        f3_part1 = label("MAS ELA TERMINA ", size=25, color=WHITE_COLOR)
        f3_part2 = label("ALGUNS MILÍMETROS A LESTE.", size=25, color=CYAN_COLOR)
        f3 = VGroup(f3_part1, f3_part2).arrange(RIGHT, buff=0.12).move_to([0, 0.6, 0])
        sintese_box_txt = formula(r"50\,\mathrm{m}\ \rightarrow\ 0{,}77\,\mathrm{cm\ para\ leste}", size=36, color=CYAN_COLOR, y=-0.8)
        sintese_retangulo = SurroundingRectangle(sintese_box_txt, color=CYAN_COLOR, buff=0.25, stroke_width=2.5)
        self.add(chao_linha, torre, f1, f2, f3, sintese_box_txt, sintese_retangulo)
