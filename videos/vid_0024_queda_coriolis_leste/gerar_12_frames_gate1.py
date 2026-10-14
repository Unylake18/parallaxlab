"""Script auxiliar para gerar os 12 frames do GATE VISUAL 1.
Renderiza snapshots estáticos de alta precisão em 540x960 para inspeção e autocrítica.
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

OUT_DIR = UNIT / "gate1_frames"
os.makedirs(OUT_DIR, exist_ok=True)


class Frame01Gancho(Scene):
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
            Line([x_solt - 0.15, y_solo, 0], [x_solt + 0.15, y_solo, 0], color=WHITE_COLOR, stroke_width=2.5),
            Line([x_solt, y_solo - 0.15, 0], [x_solt, y_solo + 0.15, 0], color=WHITE_COLOR, stroke_width=2.5),
            Dot([x_solt, y_solo, 0], radius=0.04, color=WHITE_COLOR)
        )
        t1 = label("SE EU SOLTAR A BOLA...", size=32, color=WHITE_COLOR, y=5.8)
        p1 = label("ELA CAI EXATAMENTE ", size=32, color=WHITE_COLOR)
        p2 = label("AQUI?", size=32, color=CYAN_COLOR)
        t2 = VGroup(p1, p2).arrange(RIGHT, buff=0.15).move_to([0, 5.2, 0])
        self.add(chao_linha, torre, bola, linha_ref, marcador, t1, t2)


class Frame02Equador(Scene):
    def construct(self):
        setup_header(self)
        t1 = label("CASO MAIS LIMPO: EQUADOR", size=32, color=WHITE_COLOR, y=5.6)
        t2 = label("50 m  ·  SEM ARRASTO", size=24, color=MUTED_COLOR, y=4.95)
        centro = np.array([0.0, -0.2, 0.0])
        raio = 2.3
        disco = Circle(radius=raio, stroke_width=2.5, stroke_color="#1F3A73", fill_color="#0A132C", fill_opacity=0.95).move_to(centro)
        atmo = Circle(radius=raio * 1.05, stroke_width=1.8, stroke_color=BLUE_COLOR, stroke_opacity=0.45).move_to(centro)
        eq_linha = Line(centro + LEFT * raio, centro + RIGHT * raio, color=CYAN_COLOR, stroke_width=3.5)
        elipse = Arc(radius=raio, start_angle=-PI/2, angle=PI, color=WHITE_COLOR, stroke_width=1.0, stroke_opacity=0.25).stretch(0.35, 0).move_to(centro)
        pt = glowing_ball(centro, radius=0.13, color=WHITE_COLOR, glow_color=CYAN_COLOR)
        arco_rot = Arc(radius=1.45, start_angle=-PI/3, angle=2*PI/3, arc_center=centro, color=VIOLET_COLOR, stroke_width=3.0)
        seta_rot = Arrow(arco_rot.point_from_proportion(0.92), arco_rot.point_from_proportion(1.0) + UP*0.12 + LEFT*0.08, color=VIOLET_COLOR, buff=0, stroke_width=3.0, max_tip_length_to_length_ratio=0.35)
        lbl_w = formula(r"\vec{\omega}_T", size=32, color=VIOLET_COLOR, x=1.8, y=1.2)
        self.add(t1, t2, disco, atmo, elipse, eq_linha, pt, arco_rot, seta_rot, lbl_w)


class Frame03HasteInicial(Scene):
    def construct(self):
        setup_header(self)
        tit = label("DE ONDE VEM O 2?", size=34, color=WHITE_COLOR, y=5.6)
        pivo_pt = np.array([-1.2, 0.4, 0.0])
        pivo = Dot(pivo_pt, radius=0.09, color=WHITE_COLOR)
        pivo_anel = Circle(radius=0.18, color=WHITE_COLOR, stroke_width=1.5).move_to(pivo_pt)
        haste = Line(pivo_pt, pivo_pt + RIGHT * 3.6, color=WHITE_COLOR, stroke_width=3.0)
        arco_w = Arc(radius=0.75, start_angle=-PI/12, angle=PI/3, arc_center=pivo_pt, color=VIOLET_COLOR, stroke_width=3.0)
        seta_w = Arrow(arco_w.point_from_proportion(0.92), arco_w.point_from_proportion(1.0) + UP*0.12 + LEFT*0.08, color=VIOLET_COLOR, buff=0, stroke_width=3.0, max_tip_length_to_length_ratio=0.35)
        lbl_w = formula(r"\omega", size=32, color=VIOLET_COLOR, x=pivo_pt[0] + 0.85, y=pivo_pt[1] + 0.95)
        r1 = 1.3
        conta_pt = pivo_pt + RIGHT * r1
        conta = Dot(conta_pt, radius=0.13, color=BLUE_COLOR)
        vetor_u = Arrow(conta_pt, conta_pt + RIGHT * 1.0, color=BLUE_COLOR, buff=0, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        lbl_u = formula(r"u", size=32, color=BLUE_COLOR, x=conta_pt[0] + 0.5, y=conta_pt[1] - 0.38)
        self.add(tit, pivo, pivo_anel, haste, arco_w, seta_w, lbl_w, conta, vetor_u, lbl_u)


class Frame04ContribVt(Scene):
    def construct(self):
        setup_header(self)
        tit = label("DE ONDE VEM O 2?", size=34, color=WHITE_COLOR, y=5.6)
        pivo_pt = np.array([-1.2, 0.4, 0.0])
        pivo = Dot(pivo_pt, radius=0.09, color=WHITE_COLOR)
        pivo_anel = Circle(radius=0.18, color=WHITE_COLOR, stroke_width=1.5).move_to(pivo_pt)
        haste = Line(pivo_pt, pivo_pt + RIGHT * 3.6, color=WHITE_COLOR, stroke_width=3.0)
        r1 = 1.3
        r2 = 2.5
        c1 = pivo_pt + RIGHT * r1
        c2 = pivo_pt + RIGHT * r2
        ghost_c = Dot(c1, radius=0.13, color=BLUE_COLOR, fill_opacity=0.28)
        ghost_vt1 = Arrow(c1, c1 + UP * 0.70, color=CYAN_COLOR, buff=0, stroke_width=2.5, stroke_opacity=0.30, max_tip_length_to_length_ratio=0.25)
        conta = Dot(c2, radius=0.13, color=BLUE_COLOR)
        u2 = Arrow(c2, c2 + RIGHT * 1.0, color=BLUE_COLOR, buff=0, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        vt2 = Arrow(c2, c2 + UP * 1.35, color=CYAN_COLOR, buff=0, stroke_width=3.5, max_tip_length_to_length_ratio=0.25)
        diff_vt = Arrow(c2 + UP * 0.70, c2 + UP * 1.35, color=CYAN_COLOR, buff=0, stroke_width=5.0, max_tip_length_to_length_ratio=0.30)
        lbl_diff = formula(r"\Delta v_t", size=24, color=CYAN_COLOR, x=c2[0] + 0.45, y=c2[1] + 1.05)
        eq1 = formula(r"\underbrace{\omega u}_{v_t\ \text{aumenta}}", size=38, color=WHITE_COLOR, x=0.0, y=-1.8)
        self.add(tit, pivo, pivo_anel, haste, ghost_c, ghost_vt1, conta, u2, vt2, diff_vt, lbl_diff, eq1)


class Frame05ContribRGira(Scene):
    def construct(self):
        setup_header(self)
        tit = label("DE ONDE VEM O 2?", size=34, color=WHITE_COLOR, y=5.6)
        pivo_pt = np.array([-1.2, 0.4, 0.0])
        pivo = Dot(pivo_pt, radius=0.09, color=WHITE_COLOR)
        pivo_anel = Circle(radius=0.18, color=WHITE_COLOR, stroke_width=1.5).move_to(pivo_pt)
        r_mid = 1.7
        ghost_haste = Line(pivo_pt, pivo_pt + RIGHT * 3.6, color=WHITE_COLOR, stroke_width=2.0, stroke_opacity=0.30)
        ghost_c = Dot(pivo_pt + RIGHT * r_mid, radius=0.13, color=BLUE_COLOR, fill_opacity=0.28)
        ghost_u = Arrow(pivo_pt + RIGHT * r_mid, pivo_pt + RIGHT * (r_mid + 1.0), color=BLUE_COLOR, buff=0, stroke_width=3.0, stroke_opacity=0.30, max_tip_length_to_length_ratio=0.25)

        dtheta = 22 * PI / 180
        arco_dth = Arc(radius=1.0, start_angle=0, angle=dtheta, arc_center=pivo_pt, color=VIOLET_COLOR, stroke_width=2.4)
        lbl_dth = formula(r"d\theta = \omega\,dt", size=24, color=VIOLET_COLOR, x=pivo_pt[0] + 1.6, y=pivo_pt[1] + 1.15)
        mat = np.array([[np.cos(dtheta), -np.sin(dtheta), 0],
                        [np.sin(dtheta),  np.cos(dtheta), 0],
                        [0,               0,              1]])
        haste_rot = Line(pivo_pt, pivo_pt + mat @ (RIGHT * 3.6), color=WHITE_COLOR, stroke_width=3.0)
        pos_c_rot = pivo_pt + mat @ (RIGHT * r_mid)
        conta = Dot(pos_c_rot, radius=0.13, color=BLUE_COLOR)
        u_rot_end = pos_c_rot + mat @ (RIGHT * 1.0)
        vetor_u = Arrow(pos_c_rot, u_rot_end, color=BLUE_COLOR, buff=0, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        delta_u = Arrow(pos_c_rot + RIGHT * 1.0, u_rot_end, color=CYAN_COLOR, buff=0, stroke_width=5.0, max_tip_length_to_length_ratio=0.35)
        eq2 = formula(r"\underbrace{\omega u}_{\hat{r}\ \text{gira}}", size=38, color=WHITE_COLOR, x=0.0, y=-1.8)
        self.add(tit, pivo, pivo_anel, ghost_haste, ghost_c, ghost_u, haste_rot, arco_dth, lbl_dth, conta, vetor_u, delta_u, eq2)


class Frame06Soma2wu(Scene):
    def construct(self):
        setup_header(self)
        tit = label("DUAS CONTRIBUIÇÕES CINEMÁTICAS", size=28, color=WHITE_COLOR, y=5.6)
        fator_2 = formula(r"2\omega u", size=50, color=WHITE_COLOR, y=0.4)
        fator_2[0][0].set_color(CYAN_COLOR)
        box = SurroundingRectangle(fator_2, color=CYAN_COLOR, buff=0.28, stroke_width=2.5)
        sub = formula(r"\underbrace{\omega u}_{v_t\ \text{aumenta}} + \underbrace{\omega u}_{\hat{r}\ \text{gira}}", size=34, color=MUTED_COLOR, y=-1.2)
        self.add(tit, fator_2, box, sub)


class Frame07EquacaoCoriolis(Scene):
    def construct(self):
        setup_header(self)
        ref_txt = label("REFERENCIAL GIRANTE", size=24, color=CYAN_COLOR, y=2.8)
        seta = Arrow(ORIGIN, DOWN * 1.5, color=CYAN_COLOR, buff=0, stroke_width=4.0).move_to([0, 1.6, 0])
        eq = formula(r"\vec{a}_C = -2\vec{\omega}\times\vec{v}", size=40, color=WHITE_COLOR, y=-0.6)
        box = SurroundingRectangle(eq, color=CYAN_COLOR, buff=0.22, stroke_width=2.5)
        sub = label("termo aparente no referencial girante", size=22, color=MUTED_COLOR, y=-1.5)
        self.add(ref_txt, seta, eq, box, sub)


class Frame08SolturaV0(Scene):
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

        eixo_x = Arrow(ORIGIN, RIGHT * 1.1, color=CYAN_COLOR, buff=0, stroke_width=2.5).move_to([2.1, 4.6, 0])
        lbl_x = formula(r"+x\ \text{leste}", size=20, color=CYAN_COLOR).next_to(eixo_x, DOWN, buff=0.10)
        eixo_z = Arrow(ORIGIN, UP * 1.0, color=WHITE_COLOR, buff=0, stroke_width=2.5).move_to([1.2, 5.0, 0])
        lbl_z = formula(r"+z\ \text{cima}", size=20, color=WHITE_COLOR).next_to(eixo_z, UP, buff=0.10)
        simb = symbol_into_screen([3.1, 5.0, 0], radius=0.16, color=VIOLET_COLOR)
        lbl_simb = formula(r"\vec{\omega}_T\ \otimes", size=22, color=VIOLET_COLOR).next_to(simb, RIGHT, buff=0.12)
        eixos = VGroup(eixo_x, lbl_x, eixo_z, lbl_z, simb, lbl_simb)

        txt_s = label("NO INSTANTE DA SOLTURA", size=24, color=MUTED_COLOR, x=1.5, y=2.4)
        eq_v0 = formula(r"\vec{v} = 0", size=32, color=BLUE_COLOR, x=1.5, y=1.7)
        eq_ac0 = formula(r"\vec{a}_C = 0", size=36, color=CYAN_COLOR, x=1.5, y=0.9)
        box_ac0 = SurroundingRectangle(eq_ac0, color=CYAN_COLOR, buff=0.20, stroke_width=2.2)

        self.add(chao_linha, torre, bola, linha_ref, marcador, eixos, txt_s, eq_v0, eq_ac0, box_ac0)


class Frame09QuedaVetores(Scene):
    def construct(self):
        setup_header(self)
        y_solo = -3.8
        y_topo = 4.2
        r_bola = 0.11
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.7)
        torre, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        y_bola_topo = y_topo + r_bola
        linha_ref = DashedLine([x_solt, y_bola_topo, 0], [x_solt, y_solo, 0], color=WHITE_COLOR, stroke_opacity=0.45, dash_length=0.14, dashed_ratio=0.5)
        marcador = Dot([x_solt, y_solo, 0], radius=0.07, color=WHITE_COLOR)

        H = y_bola_topo - y_solo
        B = 2.2
        tau_val = 0.70
        zx = x_solt + B * (tau_val ** 3)
        zy = y_bola_topo - H * (tau_val ** 2)

        bola = glowing_ball([zx, zy, 0])
        v_vet = Arrow([zx, zy, 0], [zx, zy - 1.8, 0], color=BLUE_COLOR, buff=0, stroke_width=3.6, max_tip_length_to_length_ratio=0.24)
        ac_vet = Arrow([zx, zy, 0], [zx + 1.3, zy, 0], color=CYAN_COLOR, buff=0, stroke_width=3.6, max_tip_length_to_length_ratio=0.24)

        pts = [[x_solt + B * (s ** 3), y_bola_topo - H * (s ** 2), 0] for s in np.linspace(0, tau_val, 35)]
        curva = VMobject(color=CYAN_COLOR, stroke_width=3.0).set_points_as_corners(pts)

        aviso = label("DESVIO EXAGERADO PARA VISUALIZAÇÃO", size=16, color=MAGENTA_COLOR, x=1.5, y=3.2)
        eq_ax = formula(r"a_x = 2\omega_T gt", size=36, color=CYAN_COLOR, x=1.5, y=0.0)

        self.add(chao_linha, torre, linha_ref, marcador, curva, bola, v_vet, ac_vet, aviso, eq_ax)


class Frame10Integracoes(Scene):
    def construct(self):
        setup_header(self)
        y_solo = -3.8
        y_topo = 4.2
        r_bola = 0.11
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.7)
        torre, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        y_bola_topo = y_topo + r_bola
        linha_ref = DashedLine([x_solt, y_bola_topo, 0], [x_solt, y_solo, 0], color=WHITE_COLOR, stroke_opacity=0.45, dash_length=0.14, dashed_ratio=0.5)
        marcador = Dot([x_solt, y_solo, 0], radius=0.07, color=WHITE_COLOR)

        H = y_bola_topo - y_solo
        B = 2.2
        pts = [[x_solt + B * (s ** 3), y_bola_topo - H * (s ** 2), 0] for s in np.linspace(0, 1.0, 40)]
        curva = VMobject(color=CYAN_COLOR, stroke_width=2.5, stroke_opacity=0.6).set_points_as_corners(pts)
        bola = glowing_ball([x_solt + B, y_solo, 0])

        eq_ax = formula(r"a_x = 2\omega_T gt", size=30, color=MUTED_COLOR, x=1.5, y=1.4)
        eq_vx = formula(r"v_x = \omega_T gt^2", size=32, color=MUTED_COLOR, x=1.5, y=0.6)
        eq_x = formula(r"x = \frac{1}{3}\omega_T gt^3", size=38, color=CYAN_COLOR, x=1.5, y=-0.4)
        box_x = SurroundingRectangle(eq_x, color=CYAN_COLOR, buff=0.22, stroke_width=2.5)

        self.add(chao_linha, torre, linha_ref, marcador, curva, bola, eq_ax, eq_vx, eq_x, box_x)


class Frame11Payoff(Scene):
    def construct(self):
        setup_header(self)
        payoff_h = label("50 m DE QUEDA", size=32, color=WHITE_COLOR, y=1.8)
        payoff_res = formula(r"0{,}77\ \mathrm{cm}", size=64, color=CYAN_COLOR, y=0.5)
        payoff_box = SurroundingRectangle(payoff_res, color=CYAN_COLOR, buff=0.30, stroke_width=3.0)
        payoff_dir = label("PARA LESTE", size=32, color=CYAN_COLOR, y=-0.8)
        self.add(payoff_h, payoff_res, payoff_box, payoff_dir)


class Frame12EscalaRealAmpliacao(Scene):
    def construct(self):
        setup_header(self)
        y_solo = -3.8
        y_topo = 4.2
        r_bola = 0.11
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.7)
        torre, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        y_bola_topo = y_topo + r_bola
        linha_ref = DashedLine([x_solt, y_bola_topo, 0], [x_solt, y_solo, 0], color=WHITE_COLOR, stroke_opacity=0.45, dash_length=0.14, dashed_ratio=0.5)
        marcador = Dot([x_solt, y_solo, 0], radius=0.07, color=WHITE_COLOR)

        H = y_bola_topo - y_solo
        pts_real = [[x_solt + 0.015 * (s ** 3), y_bola_topo - H * (s ** 2), 0] for s in np.linspace(0, 1.0, 40)]
        curva_real = VMobject(color=CYAN_COLOR, stroke_width=2.5).set_points_as_corners(pts_real)
        bola = glowing_ball([x_solt + 0.015, y_solo, 0])

        tit_escala = label("ESCALA FÍSICA REAL", size=26, color=WHITE_COLOR, x=1.5, y=2.5)

        centro_lupa = np.array([1.5, -0.9, 0.0])
        raio_lupa = 1.6
        disco_lupa = Circle(radius=raio_lupa, color=CYAN_COLOR, stroke_width=2.4, fill_color="#091024", fill_opacity=0.96).move_to(centro_lupa)
        linha_solo_lupa = Line(centro_lupa + LEFT * 1.5 + DOWN * 0.45, centro_lupa + RIGHT * 1.5 + DOWN * 0.45, color=MUTED_COLOR, stroke_width=1.5)

        x_abaixo = centro_lupa[0] - 0.80
        x_impacto = centro_lupa[0] + 0.80
        y_pts_lupa = centro_lupa[1] - 0.45

        ponto_abaixo_lupa = Dot([x_abaixo, y_pts_lupa, 0], radius=0.08, color=WHITE_COLOR)
        lbl_abaixo_lupa = label("ponto abaixo", size=15, color=MUTED_COLOR, x=x_abaixo - 0.15, y=y_pts_lupa - 0.38)

        ponto_impacto_lupa = Dot([x_impacto, y_pts_lupa, 0], radius=0.08, color=CYAN_COLOR)
        lbl_impacto_lupa = label("impacto real", size=15, color=CYAN_COLOR, x=x_impacto + 0.15, y=y_pts_lupa - 0.38)

        seta_desvio = Arrow(
            [x_abaixo, y_pts_lupa + 0.28, 0],
            [x_impacto, y_pts_lupa + 0.28, 0],
            color=CYAN_COLOR, buff=0, stroke_width=3.5, max_tip_length_to_length_ratio=0.25
        )
        valor_desvio_txt = formula(r"0{,}77\,\mathrm{cm}", size=28, color=CYAN_COLOR, x=centro_lupa[0], y=y_pts_lupa + 0.65)
        titulo_inset = label("AMPLIAÇÃO", size=20, color=WHITE_COLOR, x=centro_lupa[0], y=centro_lupa[1] + 1.2)

        grupo_lupa = VGroup(
            disco_lupa, linha_solo_lupa,
            ponto_abaixo_lupa, lbl_abaixo_lupa,
            ponto_impacto_lupa, lbl_impacto_lupa,
            seta_desvio, valor_desvio_txt,
            titulo_inset
        )

        self.add(chao_linha, torre, linha_ref, marcador, curva_real, bola, tit_escala, grupo_lupa)


if __name__ == "__main__":
    scenes = [
        ("01_gancho", Frame01Gancho),
        ("02_equador", Frame02Equador),
        ("03_haste_inicial", Frame03HasteInicial),
        ("04_contrib_vt_aumenta", Frame04ContribVt),
        ("05_contrib_r_gira", Frame05ContribRGira),
        ("06_soma_2wu", Frame06Soma2wu),
        ("07_equacao_coriolis", Frame07EquacaoCoriolis),
        ("08_soltura_v0", Frame08SolturaV0),
        ("09_queda_vetores", Frame09QuedaVetores),
        ("10_integracoes", Frame10Integracoes),
        ("11_payoff", Frame11Payoff),
        ("12_escala_real_ampliacao", Frame12EscalaRealAmpliacao),
    ]

    for name, SceneCls in scenes:
        scene = SceneCls()
        scene.render()
        img = scene.camera.get_image()
        out_path = OUT_DIR / f"{name}.png"
        img.save(str(out_path))
        print(f"Frame gerado: {out_path.name}")
