"""vid_0024 — Desvio para Leste na Queda Livre (Efeito Coriolis)
Série: DA EQUAÇÃO AO FENÔMENO · EP. 01
Formato: curto_vertical (9:16)
Versão: V3 — Derivação Visual Contínua (sem slideshow, continuidade de pensamento,
equações construídas passo a passo, vetores refinados e ritmo didático expandido).
Duração-alvo: ~2:45 a 2:55 (165s a 175s).
"""

import sys
from pathlib import Path
import numpy as np
from manim import *

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from template.config import BACKGROUND_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

config.media_dir = str(UNIT / "media")
config.background_color = BACKGROUND_COLOR

# Gramática semântica de cores oficial Parallax Lab
WHITE_COLOR = "#F5F7FF"
CYAN_COLOR = "#35D9FF"     # Coriolis, leste, desvio lateral, resultado principal
BLUE_COLOR = "#267BFF"     # Velocidade da bola, movimento radial da conta
VIOLET_COLOR = "#745CFF"   # Rotação, omega, omega_T, norte entrando na tela
MAGENTA_COLOR = "#EA63FF"  # Aviso excepcional de desvio exagerado
MUTED_COLOR = "#8492AE"    # Rótulos secundários, eixos neutros, linhas de apoio


def label(text, size=28, color=WHITE_COLOR, x=0, y=0, width=7.4):
    """Texto não-matemático oficial em Space Grotesk Medium."""
    oversample = 2 if size >= 25 else 4
    m = screen_text(text, font_size=size, color=color, oversample=oversample)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m.move_to([x, y, 0])


def formula(*parts, size=38, color=WHITE_COLOR, x=0, y=0, width=7.4):
    """Fórmulas matemáticas em MathTex com escala segura."""
    m = MathTex(*parts, font_size=size, color=color)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m.move_to([x, y, 0])


def setup_header(scene):
    """Cabeçalho oficial vigente: série + ep à esquerda, watermark à direita."""
    header_series = screen_text("DA EQUAÇÃO AO FENÔMENO · EP. 01", font_size=18, color=WHITE_COLOR)
    header_series.set_opacity(0.65).to_corner(UP + LEFT, buff=0.42)
    watermark = ImageMobject(str(WATERMARK_PATH)).set_width(1.75).set_opacity(0.35)
    watermark.to_corner(UP + RIGHT, buff=0.30)
    scene.add(header_series, watermark)
    return header_series, watermark


def build_torre(x_c=-1.6, y_solo=-3.8, y_topo=4.2, w_base=1.1, w_topo=0.45):
    """Torre estilizada, esguia, simétrica e estruturalmente limpa."""
    corpo = Polygon(
        [x_c - w_base / 2, y_solo, 0],
        [x_c + w_base / 2, y_solo, 0],
        [x_c + w_topo / 2, y_topo, 0],
        [x_c - w_topo / 2, y_topo, 0],
        color=WHITE_COLOR, stroke_width=0, fill_color="#0A1124", fill_opacity=0.75
    )
    m_esq = Line([x_c - w_base / 2, y_solo, 0], [x_c - w_topo / 2, y_topo, 0], color=WHITE_COLOR, stroke_width=2.4)
    m_dir = Line([x_c + w_base / 2, y_solo, 0], [x_c + w_topo / 2, y_topo, 0], color=WHITE_COLOR, stroke_width=2.4)

    # Plataforma de lançamento horizontal com cantilever
    x_soltura = x_c + w_topo / 2 + 0.35  # ~ -1.025
    plat = Line([x_c - w_topo / 2 - 0.15, y_topo, 0], [x_soltura + 0.18, y_topo, 0], color=WHITE_COLOR, stroke_width=3.2)
    topo_cap = Line([x_c - w_topo / 2, y_topo + 0.08, 0], [x_soltura + 0.18, y_topo + 0.08, 0], color=CYAN_COLOR, stroke_width=1.5, stroke_opacity=0.6)

    # Sapatas de assentamento na base
    base_esq = Line([x_c - w_base / 2 - 0.15, y_solo, 0], [x_c - w_base / 2 + 0.15, y_solo, 0], color=WHITE_COLOR, stroke_width=3.0)
    base_dir = Line([x_c + w_base / 2 - 0.15, y_solo, 0], [x_c + w_base / 2 + 0.15, y_solo, 0], color=WHITE_COLOR, stroke_width=3.0)

    # Treliças em X regulares
    trelicas = VGroup()
    n_andares = 6
    for i in range(n_andares):
        y1 = y_solo + i * (y_topo - y_solo) / n_andares
        y2 = y_solo + (i + 1) * (y_topo - y_solo) / n_andares
        xa1 = x_c - np.interp(y1, [y_solo, y_topo], [w_base / 2, w_topo / 2])
        xa2 = x_c + np.interp(y1, [y_solo, y_topo], [w_base / 2, w_topo / 2])
        xb1 = x_c - np.interp(y2, [y_solo, y_topo], [w_base / 2, w_topo / 2])
        xb2 = x_c + np.interp(y2, [y_solo, y_topo], [w_base / 2, w_topo / 2])
        trelicas.add(Line([xa1, y1, 0], [xb2, y2, 0], color=WHITE_COLOR, stroke_width=1.1, stroke_opacity=0.30))
        trelicas.add(Line([xa2, y1, 0], [xb1, y2, 0], color=WHITE_COLOR, stroke_width=1.1, stroke_opacity=0.30))
        trelicas.add(Line([xb1, y2, 0], [xb2, y2, 0], color=WHITE_COLOR, stroke_width=1.2, stroke_opacity=0.35))

    torre_grupo = VGroup(corpo, m_esq, m_dir, trelicas, base_esq, base_dir, plat, topo_cap)
    return torre_grupo, x_soltura


def symbol_into_screen(center, radius=0.18, color=VIOLET_COLOR):
    """Símbolo vetorial entrando no plano (Norte / +y)."""
    c = Circle(radius=radius, color=color, stroke_width=2.4)
    d = radius * 0.70
    l1 = Line([-d, -d, 0], [d, d, 0], color=color, stroke_width=2.0)
    l2 = Line([-d, d, 0], [d, -d, 0], color=color, stroke_width=2.0)
    return VGroup(c, l1, l2).move_to(center)


def glowing_ball(point, radius=0.11, color=WHITE_COLOR, glow_color=CYAN_COLOR):
    """Bola estilizada apoiada com brilho volumétrico suave."""
    glow2 = Circle(radius=radius * 2.2, stroke_width=0, fill_color=glow_color, fill_opacity=0.12)
    glow1 = Circle(radius=radius * 1.5, stroke_width=1.5, stroke_color=glow_color, fill_color=glow_color, fill_opacity=0.22)
    core = Dot(radius=radius, color=color)
    return VGroup(glow2, glow1, core).move_to(point)


class QuedaCoriolis024(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        header_series, watermark = setup_header(self)

        # Geometria base do cenário da torre
        y_solo = -3.8
        y_topo = 4.2
        r_bola = 0.11
        chao_linha = Line([-4.2, y_solo, 0], [4.2, y_solo, 0], color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.7)
        torre_mobject, x_solt = build_torre(x_c=-1.6, y_solo=y_solo, y_topo=y_topo)
        y_bola_topo = y_topo + r_bola

        # =========================================================================
        # BLOCO 1 — GANCHO COM COMPOSIÇÃO FORTE (~9.5 s)
        # =========================================================================
        bola_gancho = glowing_ball([x_solt, y_bola_topo, 0])
        linha_vertical_gancho = DashedLine(
            [x_solt, y_bola_topo, 0],
            [x_solt, y_solo, 0],
            color=WHITE_COLOR,
            stroke_opacity=0.45,
            dash_length=0.14,
            dashed_ratio=0.5
        )
        marcador_solo = VGroup(
            Line([x_solt - 0.18, y_solo, 0], [x_solt + 0.18, y_solo, 0], color=WHITE_COLOR, stroke_width=2.5),
            Line([x_solt, y_solo - 0.18, 0], [x_solt, y_solo + 0.18, 0], color=WHITE_COLOR, stroke_width=2.5),
            Dot([x_solt, y_solo, 0], radius=0.05, color=CYAN_COLOR)
        )

        txt_gancho_1 = label("SE EU SOLTAR A BOLA...", size=32, color=WHITE_COLOR, y=5.8)
        p1 = label("ELA CAI EXATAMENTE ", size=32, color=WHITE_COLOR)
        p2 = label("AQUI?", size=32, color=CYAN_COLOR)
        txt_gancho_2 = VGroup(p1, p2).arrange(RIGHT, buff=0.15).move_to([0, 5.2, 0])

        self.play(FadeIn(chao_linha), FadeIn(torre_mobject), FadeIn(bola_gancho), run_time=1.4)
        self.play(Create(linha_vertical_gancho), FadeIn(marcador_solo), FadeIn(txt_gancho_1), run_time=1.6)
        self.play(FadeIn(txt_gancho_2), run_time=1.0)
        # Pulso na bola para instigar expectativa
        self.play(bola_gancho[1].animate.scale(1.3), run_time=0.6, rate_func=rate_functions.wiggle)
        self.wait(4.5)

        self.play(
            FadeOut(txt_gancho_1),
            FadeOut(txt_gancho_2),
            FadeOut(torre_mobject),
            FadeOut(linha_vertical_gancho),
            FadeOut(marcador_solo),
            FadeOut(bola_gancho),
            FadeOut(chao_linha),
            run_time=1.2
        )

        # =========================================================================
        # BLOCO 2 — CASO ESTUDADO: EQUADOR COM TERRA ESTILIZADA (~7.5 s)
        # =========================================================================
        txt_equador_1 = label("VAMOS OLHAR O CASO MAIS LIMPO", size=28, color=WHITE_COLOR, y=5.6)
        txt_equador_2 = label("EQUADOR  ·  50 m  ·  SEM ARRASTO", size=22, color=MUTED_COLOR, y=4.95)

        centro_globo = np.array([0.0, -0.4, 0.0])
        raio_globo = 2.4
        disco_terra = Circle(radius=raio_globo, stroke_width=2.5, stroke_color="#1F3A73", fill_color="#0A132C", fill_opacity=0.95).move_to(centro_globo)
        atmosfera = Circle(radius=raio_globo * 1.05, stroke_width=1.8, stroke_color=BLUE_COLOR, stroke_opacity=0.45).move_to(centro_globo)
        linha_equador = Line(centro_globo + LEFT * raio_globo, centro_globo + RIGHT * raio_globo, color=CYAN_COLOR, stroke_width=3.5)
        lbl_equador = label("EQUADOR", size=18, color=CYAN_COLOR, x=0, y=centro_globo[1] - 0.35)

        # Arco de rotação perfeitamente tangencial (sem vetor torto)
        arco_rot_globo = Arc(radius=1.4, start_angle=-PI/4, angle=PI/2, arc_center=centro_globo, color=VIOLET_COLOR, stroke_width=3.0)
        p_end_rot = arco_rot_globo.point_from_proportion(1.0)
        p_prev_rot = arco_rot_globo.point_from_proportion(0.95)
        tan_dir_rot = (p_end_rot - p_prev_rot) / np.linalg.norm(p_end_rot - p_prev_rot)
        seta_rot_globo = Arrow(
            p_end_rot - tan_dir_rot * 0.28, p_end_rot,
            color=VIOLET_COLOR, buff=0, stroke_width=3.0, max_tip_length_to_length_ratio=0.38
        )
        lbl_omega_globo = formula(r"\vec{\omega}_T", size=32, color=VIOLET_COLOR, x=p_end_rot[0] + 0.45, y=p_end_rot[1] + 0.2)

        ponto_experimento = glowing_ball(centro_globo + RIGHT * 0.0, radius=0.13, color=WHITE_COLOR, glow_color=CYAN_COLOR)

        globo_grupo = VGroup(
            disco_terra, atmosfera, linha_equador, lbl_equador,
            arco_rot_globo, seta_rot_globo, lbl_omega_globo, ponto_experimento
        )

        self.play(FadeIn(txt_equador_1), FadeIn(txt_equador_2), FadeIn(globo_grupo), run_time=1.4)
        self.wait(4.5)

        # Transição limpa que remove completamente a Terra antes do bloco conceitual
        self.play(
            FadeOut(globo_grupo),
            FadeOut(txt_equador_1),
            FadeOut(txt_equador_2),
            run_time=1.2
        )
        self.wait(0.3)

        # =========================================================================
        # BLOCO 3 — O QUE É A ACELERAÇÃO DE CORIOLIS? (~12.5 s)
        # =========================================================================
        txt_bloco3_titulo = label("O QUE É A ACELERAÇÃO DE CORIOLIS?", size=28, color=WHITE_COLOR, y=5.5)
        self.play(FadeIn(txt_bloco3_titulo), run_time=0.8)

        # Equação protagonista com cores semânticas nos termos
        # \vec{a}_C (ciano) = -2 \vec{\omega}_T (violeta) \times \vec{v} (azul)
        eq_protagonista = MathTex(
            r"\vec{a}_C", r"=", r"-2", r"\vec{\omega}_T", r"\times", r"\vec{v}",
            font_size=44, color=WHITE_COLOR
        ).move_to([0, 3.8, 0])
        eq_protagonista[0].set_color(CYAN_COLOR)
        eq_protagonista[3].set_color(VIOLET_COLOR)
        eq_protagonista[5].set_color(BLUE_COLOR)
        box_protagonista = SurroundingRectangle(eq_protagonista, color=CYAN_COLOR, buff=0.25, stroke_width=2.0)

        self.play(Write(eq_protagonista), Create(box_protagonista), run_time=1.6)

        # Rótulos conceituais estruturados com apontadores/destaques
        item_ac = VGroup(formula(r"\vec{a}_C", size=32, color=CYAN_COLOR), label("aceleração aparente de Coriolis", size=22, color=WHITE_COLOR)).arrange(RIGHT, buff=0.3)
        item_w = VGroup(formula(r"\vec{\omega}_T", size=32, color=VIOLET_COLOR), label("velocidade angular da Terra", size=22, color=WHITE_COLOR)).arrange(RIGHT, buff=0.3)
        item_v = VGroup(formula(r"\vec{v}", size=32, color=BLUE_COLOR), label("velocidade do corpo relativa à Terra", size=22, color=WHITE_COLOR)).arrange(RIGHT, buff=0.3)
        tabela_variaveis = VGroup(item_ac, item_w, item_v).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0.2, 0.9, 0])

        frase_conceito = label("Ela surge ao descrever o movimento em um referencial que gira.", size=20, color=MUTED_COLOR, y=-1.5)

        self.play(FadeIn(tabela_variaveis), run_time=1.8)
        self.play(FadeIn(frase_conceito), run_time=1.2)
        self.wait(5.0)

        self.play(
            FadeOut(txt_bloco3_titulo),
            FadeOut(tabela_variaveis),
            FadeOut(frase_conceito),
            FadeOut(box_protagonista),
            run_time=1.0
        )

        # =========================================================================
        # BLOCO 4 — DE ONDE VEM O FATOR 2? (HASTE GIRATÓRIA) (~33 s)
        # =========================================================================
        txt_haste_pergunta = label("POR QUE APARECE O FATOR 2?", size=30, color=WHITE_COLOR, y=5.5)
        # Transforma a protagonista em pergunta
        self.play(
            ReplacementTransform(eq_protagonista, txt_haste_pergunta),
            run_time=1.1
        )

        # --- ESTADO A: ESTABELECIMENTO (~7 s) ---
        pivo_pt = np.array([-1.5, 2.2, 0.0])
        pivo = Dot(pivo_pt, radius=0.09, color=WHITE_COLOR)
        pivo_anel = Circle(radius=0.18, color=WHITE_COLOR, stroke_width=1.5).move_to(pivo_pt)
        haste_linha = Line(pivo_pt, pivo_pt + RIGHT * 3.8, color=WHITE_COLOR, stroke_width=3.0)

        # Rotação angular em torno do pivô (arco perfeitamente tangencial)
        arco_haste_omega = Arc(radius=0.85, start_angle=-PI/12, angle=PI/3, arc_center=pivo_pt, color=VIOLET_COLOR, stroke_width=2.8)
        p_end_ho = arco_haste_omega.point_from_proportion(1.0)
        p_prev_ho = arco_haste_omega.point_from_proportion(0.95)
        tan_ho = (p_end_ho - p_prev_ho) / np.linalg.norm(p_end_ho - p_prev_ho)
        seta_haste_omega = Arrow(p_end_ho - tan_ho * 0.22, p_end_ho, color=VIOLET_COLOR, buff=0, stroke_width=2.8, max_tip_length_to_length_ratio=0.38)
        lbl_haste_omega = formula(r"\omega", size=30, color=VIOLET_COLOR, x=pivo_pt[0] + 0.95, y=pivo_pt[1] + 1.05)

        # Conta e velocidade radial u
        r1 = 1.3
        conta_pt = pivo_pt + RIGHT * r1
        conta = Dot(conta_pt, radius=0.13, color=BLUE_COLOR)
        vetor_u = Arrow(conta_pt, conta_pt + RIGHT * 1.05, color=BLUE_COLOR, buff=0, stroke_width=4.0, max_tip_length_to_length_ratio=0.25)
        lbl_u = formula(r"u", size=30, color=BLUE_COLOR, x=conta_pt[0] + 0.55, y=conta_pt[1] - 0.38)

        # Legendas discretas das variáveis na haste
        def_u = VGroup(formula(r"u", size=26, color=BLUE_COLOR), label(": velocidade radial da conta", size=20, color=WHITE_COLOR)).arrange(RIGHT, buff=0.15)
        def_w = VGroup(formula(r"\omega", size=26, color=VIOLET_COLOR), label(": velocidade angular de rotação", size=20, color=WHITE_COLOR)).arrange(RIGHT, buff=0.15)
        defs_haste = VGroup(def_u, def_w).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0.2, 0.4, 0])

        haste_cenario = VGroup(
            pivo, pivo_anel, haste_linha,
            arco_haste_omega, seta_haste_omega, lbl_haste_omega,
            conta, vetor_u, lbl_u, defs_haste
        )
        self.play(FadeIn(haste_cenario), run_time=1.5)
        self.wait(4.2)

        # --- ESTADO B: PRIMEIRA CONTRIBUIÇÃO (v_t aumenta) (~9 s) ---
        vt1_len = 0.70
        vetor_vt1 = Arrow(conta_pt, conta_pt + UP * vt1_len, color=CYAN_COLOR, buff=0, stroke_width=3.5, max_tip_length_to_length_ratio=0.25)
        lbl_vt1 = formula(r"v_{t1} = \omega r", size=22, color=CYAN_COLOR, x=conta_pt[0] - 0.75, y=conta_pt[1] + 0.5)

        # Fantasma inicial
        ghost_conta = Dot(conta_pt, radius=0.13, color=BLUE_COLOR, fill_opacity=0.28)
        ghost_vt1 = Arrow(conta_pt, conta_pt + UP * vt1_len, color=CYAN_COLOR, buff=0, stroke_width=2.5, stroke_opacity=0.30, max_tip_length_to_length_ratio=0.25)

        # Deslocamento radial dr = u dt
        r2 = 2.6
        novo_conta_pt = pivo_pt + RIGHT * r2
        vt2_len = 1.40
        vetor_vt2 = Arrow(novo_conta_pt, novo_conta_pt + UP * vt2_len, color=CYAN_COLOR, buff=0, stroke_width=3.5, max_tip_length_to_length_ratio=0.25)
        diff_vt = Arrow(novo_conta_pt + UP * vt1_len, novo_conta_pt + UP * vt2_len, color=CYAN_COLOR, buff=0, stroke_width=5.0, max_tip_length_to_length_ratio=0.30)
        lbl_diff_vt = formula(r"\Delta v_t", size=24, color=CYAN_COLOR, x=novo_conta_pt[0] + 0.5, y=novo_conta_pt[1] + 1.1)

        # Derivação da contribuição 1 na tela
        lbl_b_step1 = formula(r"dr = u\,dt \implies dv_t = \omega\,dr = \omega u\,dt", size=26, color=WHITE_COLOR, x=0, y=0.5)
        eq_a1 = formula(r"a_1 = \frac{dv_t}{dt} = \omega u", size=32, color=WHITE_COLOR, x=0, y=-0.3)
        box_a1 = SurroundingRectangle(eq_a1, color=CYAN_COLOR, buff=0.18, stroke_width=1.8)
        desc_a1 = label("efeito 1: velocidade tangencial aumenta com o raio", size=18, color=CYAN_COLOR, x=0, y=-1.35, width=7.6)
        bloco_deriv_b = VGroup(lbl_b_step1, eq_a1, box_a1, desc_a1)

        self.play(Create(vetor_vt1), FadeIn(lbl_vt1), run_time=0.8)
        self.play(
            FadeIn(ghost_conta), FadeIn(ghost_vt1),
            conta.animate.move_to(novo_conta_pt),
            vetor_u.animate.shift(RIGHT * (r2 - r1)),
            lbl_u.animate.shift(RIGHT * (r2 - r1)),
            ReplacementTransform(vetor_vt1, vetor_vt2),
            FadeOut(lbl_vt1),
            FadeOut(defs_haste),
            run_time=1.6
        )
        self.play(Create(diff_vt), FadeIn(lbl_diff_vt), run_time=0.8)
        self.play(FadeIn(bloco_deriv_b), run_time=1.4)
        self.wait(5.2)

        # --- ESTADO C: SEGUNDA CONTRIBUIÇÃO (direção de r gira) (~9 s) ---
        self.play(
            FadeOut(ghost_conta), FadeOut(ghost_vt1),
            FadeOut(vetor_vt2), FadeOut(diff_vt), FadeOut(lbl_diff_vt),
            FadeOut(bloco_deriv_b),
            conta.animate.move_to(pivo_pt + RIGHT * 1.8),
            vetor_u.animate.move_to(pivo_pt + RIGHT * 2.35),
            lbl_u.animate.move_to(pivo_pt + RIGHT * 2.35 + DOWN * 0.38),
            run_time=1.1
        )

        r_mid = 1.8
        pos_c_mid = pivo_pt + RIGHT * r_mid
        ghost_haste_linha = Line(pivo_pt, pivo_pt + RIGHT * 3.8, color=WHITE_COLOR, stroke_width=2.0, stroke_opacity=0.30)
        ghost_u_mid = Arrow(pos_c_mid, pos_c_mid + RIGHT * 1.05, color=BLUE_COLOR, buff=0, stroke_width=3.0, stroke_opacity=0.30, max_tip_length_to_length_ratio=0.25)
        self.add(ghost_haste_linha, ghost_u_mid)

        # Rotação suave da haste por pequeno dtheta
        dtheta = 22 * PI / 180
        arco_dtheta = Arc(radius=1.1, start_angle=0, angle=dtheta, arc_center=pivo_pt, color=VIOLET_COLOR, stroke_width=2.4)
        lbl_dtheta = formula(r"d\theta = \omega\,dt", size=24, color=VIOLET_COLOR, x=pivo_pt[0] + 1.7, y=pivo_pt[1] + 1.0)

        mat_rot = np.array([[np.cos(dtheta), -np.sin(dtheta), 0],
                            [np.sin(dtheta),  np.cos(dtheta), 0],
                            [0,               0,              1]])
        pos_c_rot = pivo_pt + mat_rot @ (RIGHT * r_mid)
        u_rot_end = pos_c_rot + mat_rot @ (RIGHT * 1.05)

        # Vetor transversal conectando a rotação de direção
        delta_u_seta = Arrow(pos_c_rot + RIGHT * 1.05, u_rot_end, color=CYAN_COLOR, buff=0, stroke_width=4.5, max_tip_length_to_length_ratio=0.35)

        # Derivação da contribuição 2 na tela
        lbl_c_step1 = formula(r"d\theta = \omega\,dt \implies |d\vec{v}| \approx u\,d\theta = u\omega\,dt", size=26, color=WHITE_COLOR, x=0, y=0.5)
        eq_a2 = formula(r"a_2 = \frac{|d\vec{v}|}{dt} = \omega u", size=32, color=WHITE_COLOR, x=0, y=-0.3)
        box_a2 = SurroundingRectangle(eq_a2, color=CYAN_COLOR, buff=0.18, stroke_width=1.8)
        desc_a2 = label(r"efeito 2: direção da velocidade radial gira no espaço", size=18, color=CYAN_COLOR, x=0, y=-1.35, width=7.6)
        bloco_deriv_c = VGroup(lbl_c_step1, eq_a2, box_a2, desc_a2)

        self.play(
            Rotate(haste_linha, angle=dtheta, about_point=pivo_pt),
            conta.animate.move_to(pos_c_rot),
            vetor_u.animate.put_start_and_end_on(pos_c_rot, u_rot_end),
            lbl_u.animate.move_to(pos_c_rot + mat_rot @ (RIGHT * 0.55 + DOWN * 0.38)),
            Create(arco_dtheta), FadeIn(lbl_dtheta),
            run_time=1.6
        )
        self.play(Create(delta_u_seta), FadeIn(bloco_deriv_c), run_time=1.4)
        self.wait(5.2)

        # --- ESTADO D: SOMA DAS DUAS CONTRIBUIÇÕES (~8 s) ---
        self.play(
            FadeOut(haste_cenario),
            FadeOut(ghost_haste_linha),
            FadeOut(ghost_u_mid),
            FadeOut(arco_dtheta),
            FadeOut(lbl_dtheta),
            FadeOut(delta_u_seta),
            FadeOut(bloco_deriv_c),
            FadeOut(txt_haste_pergunta),
            run_time=1.0
        )

        txt_soma_titulo = label("DOIS EFEITOS INDEPENDENTES SE SOMAM", size=26, color=WHITE_COLOR, y=5.4)
        eq_soma_expandida = formula(
            r"a_{\text{tang}}", r"=", r"\underbrace{\omega u}_{v_t\ \text{aumenta}}", r"+", r"\underbrace{\omega u}_{\hat{r}\ \text{gira}}",
            size=36, color=WHITE_COLOR, y=2.2
        )
        eq_soma_expandida[2].set_color(CYAN_COLOR)
        eq_soma_expandida[4].set_color(CYAN_COLOR)

        eq_fator_2 = formula(r"a_{\text{tang}} = 2\omega u", size=48, color=WHITE_COLOR, y=0.5)
        eq_fator_2[0][6].set_color(CYAN_COLOR)  # Destaca o '2'
        box_fator_2 = SurroundingRectangle(eq_fator_2, color=CYAN_COLOR, buff=0.28, stroke_width=2.5)
        desc_fator_2 = label("daqui nasce o fator 2 da aceleração transversal!", size=22, color=CYAN_COLOR, y=-0.7)

        self.play(FadeIn(txt_soma_titulo), Write(eq_soma_expandida), run_time=1.5)
        self.wait(2.6)
        self.play(Write(eq_fator_2), Create(box_fator_2), FadeIn(desc_fator_2), run_time=1.6)
        # Brilho de destaque no 2
        self.play(eq_fator_2[0][6].animate.scale(1.25), run_time=0.5, rate_func=rate_functions.wiggle)
        self.wait(5.0)

        # =========================================================================
        # BLOCO 5 — DA HASTE PARA A EQUAÇÃO DE CORIOLIS (~11 s)
        # =========================================================================
        txt_ponte_titulo = label("DO REFERENCIAL INERCIAL AO GIRANTE", size=26, color=WHITE_COLOR, y=5.4)
        self.play(
            ReplacementTransform(txt_soma_titulo, txt_ponte_titulo),
            FadeOut(eq_soma_expandida),
            FadeOut(desc_fator_2),
            FadeOut(box_fator_2),
            eq_fator_2.animate.scale(0.8).move_to([0, 3.4, 0]),
            run_time=1.2
        )

        txt_explic_inercial = label("No referencial inercial: aceleração real de arraste", size=20, color=MUTED_COLOR, y=2.6)
        txt_explic_girante = label("No referencial que gira: surge a força inercial aparente oposta", size=20, color=CYAN_COLOR, y=1.9)

        eq_fc = formula(r"\vec{F}_C = -2m\,\vec{\omega}\times\vec{v}", size=36, color=WHITE_COLOR, y=0.6)
        txt_dividir_m = label(r"dividindo pela massa m:", size=20, color=MUTED_COLOR, y=-0.2)
        eq_ac_geral = formula(r"\vec{a}_C = -2\vec{\omega}\times\vec{v}", size=42, color=WHITE_COLOR, y=-1.1)
        eq_ac_geral[0][:3].set_color(CYAN_COLOR)
        box_ac_geral = SurroundingRectangle(eq_ac_geral, color=CYAN_COLOR, buff=0.25, stroke_width=2.2)

        self.play(FadeIn(txt_explic_inercial), FadeIn(txt_explic_girante), run_time=1.2)
        self.play(Write(eq_fc), FadeIn(txt_dividir_m), run_time=1.3)
        self.play(Write(eq_ac_geral), Create(box_ac_geral), run_time=1.5)
        self.wait(4.8)

        self.play(
            FadeOut(txt_ponte_titulo),
            FadeOut(eq_fator_2),
            FadeOut(txt_explic_inercial),
            FadeOut(txt_explic_girante),
            FadeOut(eq_fc),
            FadeOut(txt_dividir_m),
            FadeOut(eq_ac_geral),
            FadeOut(box_ac_geral),
            run_time=1.0
        )

        # =========================================================================
        # BLOCO 6 — APLICAÇÃO NA TERRA (TORRE E INSTANTE DA SOLTURA) (~15 s)
        # =========================================================================
        # Cenário local com torre e eixos locais bem distribuídos
        bola_topo = glowing_ball([x_solt, y_bola_topo, 0])
        linha_ref_queda = DashedLine(
            [x_solt, y_bola_topo, 0],
            [x_solt, y_solo, 0],
            color=WHITE_COLOR,
            stroke_opacity=0.45,
            dash_length=0.14,
            dashed_ratio=0.5
        )
        marcador_ref_solo = Dot([x_solt, y_solo, 0], radius=0.07, color=WHITE_COLOR)

        # Sistema de eixos locais integrado na lateral direita superior
        eixo_x = Arrow(ORIGIN, RIGHT * 1.1, color=CYAN_COLOR, buff=0, stroke_width=2.5).move_to([2.1, 4.8, 0])
        lbl_eixo_x = formula(r"+x\ \text{leste}", size=19, color=CYAN_COLOR).next_to(eixo_x, DOWN, buff=0.10)

        eixo_z = Arrow(ORIGIN, UP * 1.0, color=WHITE_COLOR, buff=0, stroke_width=2.5).move_to([1.2, 5.2, 0])
        lbl_eixo_z = formula(r"+z\ \text{cima}", size=19, color=WHITE_COLOR).next_to(eixo_z, UP, buff=0.10)

        simbolo_norte = symbol_into_screen([3.1, 5.2, 0], radius=0.16, color=VIOLET_COLOR)
        lbl_norte = formula(r"\vec{\omega}_T\ \otimes", size=21, color=VIOLET_COLOR).next_to(simbolo_norte, RIGHT, buff=0.12)

        eixos_locais = VGroup(eixo_x, lbl_eixo_x, eixo_z, lbl_eixo_z, simbolo_norte, lbl_norte)

        self.play(
            FadeIn(chao_linha),
            FadeIn(torre_mobject),
            FadeIn(bola_topo),
            Create(linha_ref_queda),
            FadeIn(marcador_ref_solo),
            FadeIn(eixos_locais),
            run_time=1.4
        )

        # Na soltura: rotação terrestre e repouso inicial
        txt_soltura_bloco = label("NO INSTANTE DA SOLTURA", size=22, color=MUTED_COLOR, x=1.5, y=3.2)
        eq_rot_terra = formula(r"\vec{\omega}_T = \omega_T\,\hat{y}\ \ (\text{norte})", size=24, color=VIOLET_COLOR, x=1.5, y=2.5)
        eq_v0_bloco = formula(r"\vec{v} = 0", size=32, color=BLUE_COLOR, x=1.5, y=1.7)
        eq_ac_v0 = formula(r"\vec{a}_C = -2\vec{\omega}_T\times\vec{0} = \vec{0}", size=28, color=WHITE_COLOR, x=1.5, y=0.9)
        lbl_sem_ac = label("inicialmente não há desvio!", size=20, color=CYAN_COLOR, x=1.5, y=0.1)

        self.play(FadeIn(txt_soltura_bloco), FadeIn(eq_rot_terra), run_time=1.0)
        self.play(FadeIn(eq_v0_bloco), run_time=0.8)
        self.play(FadeIn(eq_ac_v0), FadeIn(lbl_sem_ac), run_time=1.4)
        self.wait(5.0)

        self.play(
            FadeOut(txt_soltura_bloco),
            FadeOut(eq_v0_bloco),
            FadeOut(eq_ac_v0),
            FadeOut(lbl_sem_ac),
            run_time=0.8
        )

        # =========================================================================
        # BLOCO 7 — A QUEDA COMEÇA: VETORES E SUBSTITUIÇÃO (~18 s)
        # =========================================================================
        # Velocidade cresce na queda
        eq_v_descendo = formula(r"\vec{v} \approx -gt\,\hat{z}", size=28, color=BLUE_COLOR, x=1.5, y=3.2)
        lbl_v_desc = label("velocidade vertical para baixo", size=18, color=BLUE_COLOR, x=1.5, y=2.7)

        # Substituição vetorial passo a passo:
        eq_sub1 = formula(r"\vec{a}_C = -2(\omega_T\hat{y})\times(-gt\hat{z})", size=26, color=WHITE_COLOR, x=1.5, y=1.9)
        regra_cruz = formula(r"\hat{y}\times\hat{z} = \hat{x} \quad (\text{norte}\times\text{cima} = \text{leste})", size=21, color=MUTED_COLOR, x=1.5, y=1.2)
        eq_sub2 = formula(r"\vec{a}_C = 2\omega_T gt\,\hat{x}", size=30, color=CYAN_COLOR, x=1.5, y=0.4)
        lbl_destaque_leste = label("ACELERAÇÃO PARA LESTE (+x)", size=20, color=CYAN_COLOR, x=1.5, y=-0.2)
        eq_ax_result = formula(r"a_x = 2\omega_T gt", size=36, color=CYAN_COLOR, x=1.5, y=-1.0)
        box_ax_result = SurroundingRectangle(eq_ax_result, color=CYAN_COLOR, buff=0.20, stroke_width=2.0)

        self.play(FadeIn(eq_v_descendo), FadeIn(lbl_v_desc), run_time=1.0)
        self.play(FadeIn(eq_sub1), FadeIn(regra_cruz), run_time=1.2)
        self.play(Write(eq_sub2), FadeIn(lbl_destaque_leste), run_time=1.2)
        self.play(Write(eq_ax_result), Create(box_ax_result), run_time=1.2)
        self.wait(2.5)

        # Queda sincronizada com ValueTracker
        aviso_exagero_bloco = label("DESVIO EXAGERADO PARA VISUALIZAÇÃO", size=16, color=MAGENTA_COLOR, x=1.5, y=-2.0)
        self.play(FadeIn(aviso_exagero_bloco), run_time=0.6)

        H_queda = y_bola_topo - y_solo
        B_exag = 2.2  # Desvio amplo e perceptível no quadro vertical

        tau = ValueTracker(0.0)

        vetor_v_dinamico = always_redraw(lambda: Arrow(
            bola_topo.get_center(),
            bola_topo.get_center() + DOWN * (2.1 * tau.get_value()),
            color=BLUE_COLOR, buff=0, stroke_width=3.6, max_tip_length_to_length_ratio=0.24
        ) if tau.get_value() > 0.06 else VGroup())

        vetor_ac_dinamico = always_redraw(lambda: Arrow(
            bola_topo.get_center(),
            bola_topo.get_center() + RIGHT * (1.6 * tau.get_value()),
            color=CYAN_COLOR, buff=0, stroke_width=3.6, max_tip_length_to_length_ratio=0.24
        ) if tau.get_value() > 0.06 else VGroup())

        def get_trajetoria_curva():
            t_v = tau.get_value()
            if t_v < 0.02:
                return VGroup()
            pts = []
            steps = max(5, int(t_v * 48))
            for s in np.linspace(0, t_v, steps):
                zx = x_solt + B_exag * (s ** 3)
                zy = y_bola_topo - H_queda * (s ** 2)
                pts.append([zx, zy, 0])
            c = VMobject(color=CYAN_COLOR, stroke_width=3.0)
            c.set_points_as_corners(pts)
            return c

        trajetoria_dinamica = always_redraw(get_trajetoria_curva)

        bola_topo.add_updater(lambda m: m.move_to([
            x_solt + B_exag * (tau.get_value() ** 3),
            y_bola_topo - H_queda * (tau.get_value() ** 2),
            0
        ]))

        self.add(trajetoria_dinamica, vetor_v_dinamico, vetor_ac_dinamico)

        self.play(tau.animate.set_value(1.0), run_time=5.8, rate_func=linear)
        self.wait(2.4)

        bola_topo.clear_updaters()
        vetor_v_dinamico.clear_updaters()
        vetor_ac_dinamico.clear_updaters()
        trajetoria_dinamica.clear_updaters()

        self.play(
            FadeOut(vetor_v_dinamico),
            FadeOut(vetor_ac_dinamico),
            FadeOut(aviso_exagero_bloco),
            FadeOut(eq_v_descendo),
            FadeOut(lbl_v_desc),
            FadeOut(eq_sub1),
            FadeOut(regra_cruz),
            FadeOut(eq_sub2),
            FadeOut(lbl_destaque_leste),
            FadeOut(eq_rot_terra),
            run_time=1.0
        )

        # =========================================================================
        # BLOCO 8 — INTEGRAR UMA VEZ, INTEGRAR DE NOVO (~18 s)
        # =========================================================================
        # Reorganiza a coluna de derivação algébrica contínua
        # Linha 1: a_x = 2 \omega_T g t
        # Linha 2: v_x = \int a_x dt = \omega_T g t^2
        # Linha 3: x = \int v_x dt = \frac{1}{3} \omega_T g t^3
        self.play(
            eq_ax_result.animate.move_to([1.5, 2.8, 0]),
            box_ax_result.animate.move_to([1.5, 2.8, 0]),
            run_time=0.9
        )

        txt_int1 = formula(r"\Downarrow\ \int dt \quad [v_x(0) = 0]", size=22, color=MUTED_COLOR, x=1.5, y=2.0)
        eq_vx_int = formula(r"v_x(t) = \omega_T gt^2", size=34, color=CYAN_COLOR, x=1.5, y=1.2)
        box_vx = SurroundingRectangle(eq_vx_int, color=CYAN_COLOR, buff=0.18, stroke_width=1.8)

        self.play(FadeIn(txt_int1), Write(eq_vx_int), Create(box_vx), run_time=1.4)
        self.wait(3.0)

        txt_int2 = formula(r"\Downarrow\ \int dt \quad [x(0) = 0]", size=22, color=MUTED_COLOR, x=1.5, y=0.35)
        eq_x_int = formula(r"x(t) = \frac{1}{3}\omega_T gt^3", size=38, color=CYAN_COLOR, x=1.5, y=-0.5)
        box_x_int = SurroundingRectangle(eq_x_int, color=CYAN_COLOR, buff=0.22, stroke_width=2.5)

        self.play(FadeIn(txt_int2), Write(eq_x_int), Create(box_x_int), run_time=1.5)
        self.wait(5.0)

        # Limpa os passos intermediários mantendo a fórmula final de x(t)
        self.play(
            FadeOut(eq_ax_result),
            FadeOut(box_ax_result),
            FadeOut(txt_int1),
            FadeOut(eq_vx_int),
            FadeOut(box_vx),
            FadeOut(txt_int2),
            eq_x_int.animate.move_to([1.5, -1.2, 0]),
            box_x_int.animate.move_to([1.5, -1.2, 0]),
            run_time=1.0
        )

        # =========================================================================
        # BLOCO 9 — O CASO DOS 50 METROS (~13 s)
        # =========================================================================
        # Cota de altura na torre
        cota_h = VGroup(
            Line([-2.3, y_topo, 0], [-2.3, y_solo, 0], color=WHITE_COLOR, stroke_width=1.6),
            Line([-2.45, y_topo, 0], [-2.15, y_topo, 0], color=WHITE_COLOR, stroke_width=1.6),
            Line([-2.45, y_solo, 0], [-2.15, y_solo, 0], color=WHITE_COLOR, stroke_width=1.6),
            formula(r"h = 50\,\mathrm{m}", size=24, color=WHITE_COLOR).move_to([-3.1, (y_topo + y_solo) / 2, 0])
        )

        eq_queda_tempo = formula(r"h = \frac{1}{2}gt^2", size=30, color=WHITE_COLOR, x=1.5, y=2.8)
        eq_tf_formula = formula(r"t_f = \sqrt{\frac{2h}{g}}", size=32, color=WHITE_COLOR, x=1.5, y=1.8)
        eq_tf_valor = formula(r"t_f \approx 3{,}19\,\mathrm{s}", size=36, color=WHITE_COLOR, x=1.5, y=0.8)
        box_tf = SurroundingRectangle(eq_tf_valor, color=WHITE_COLOR, buff=0.18, stroke_width=1.8)

        self.play(FadeIn(cota_h), FadeIn(eq_queda_tempo), run_time=1.1)
        self.play(Write(eq_tf_formula), run_time=1.0)
        self.play(Write(eq_tf_valor), Create(box_tf), run_time=1.3)
        self.wait(5.0)

        # =========================================================================
        # BLOCO 10 — O RESULTADO NUMÉRICO (~12 s)
        # =========================================================================
        # Desvanece tempo e cota para foco total no resultado numérico com máxima respiração
        self.play(
            FadeOut(cota_h),
            FadeOut(eq_queda_tempo),
            FadeOut(eq_tf_formula),
            FadeOut(eq_tf_valor),
            FadeOut(box_tf),
            FadeOut(torre_mobject),
            FadeOut(linha_ref_queda),
            FadeOut(marcador_ref_solo),
            FadeOut(bola_topo),
            FadeOut(trajetoria_dinamica),
            FadeOut(chao_linha),
            FadeOut(eixos_locais),
            eq_x_int.animate.move_to([0, 3.0, 0]),
            box_x_int.animate.move_to([0, 3.0, 0]),
            run_time=1.2
        )

        const_omega = formula(r"\omega_T \approx 7{,}29\times 10^{-5}\,\mathrm{rad/s}", size=24, color=MUTED_COLOR, x=0, y=1.9)
        const_g_tf = formula(r"g \approx 9{,}8\,\mathrm{m/s^2} \quad t_f \approx 3{,}19\,\mathrm{s}", size=24, color=MUTED_COLOR, x=0, y=1.3)
        self.play(FadeIn(const_omega), FadeIn(const_g_tf), run_time=1.3)
        self.wait(2.6)

        # Payoff final do valor
        res_cm = formula(r"x \approx 0{,}77\ \mathrm{cm}", size=56, color=CYAN_COLOR, x=0, y=-0.3)
        box_res_cm = SurroundingRectangle(res_cm, color=CYAN_COLOR, buff=0.30, stroke_width=3.0)
        lbl_leste_payoff = label("PARA LESTE", size=32, color=CYAN_COLOR, x=0, y=-1.5)

        self.play(Write(res_cm), Create(box_res_cm), run_time=1.5)
        self.play(FadeIn(lbl_leste_payoff), run_time=1.2)
        self.wait(5.5)

        self.play(
            FadeOut(eq_x_int),
            FadeOut(box_x_int),
            FadeOut(const_omega),
            FadeOut(const_g_tf),
            FadeOut(res_cm),
            FadeOut(box_res_cm),
            FadeOut(lbl_leste_payoff),
            run_time=1.0
        )

        # =========================================================================
        # BLOCO 11 — ESCALA EXAGERADA VS ESCALA REAL + AMPLIAÇÃO (~15 s)
        # =========================================================================
        exag_tracker = ValueTracker(B_exag)

        def get_curva_escala():
            ex = exag_tracker.get_value()
            pts = [
                [x_solt + ex * (s ** 3), y_bola_topo - H_queda * (s ** 2), 0]
                for s in np.linspace(0, 1.0, 40)
            ]
            c = VMobject(color=CYAN_COLOR, stroke_width=2.5)
            c.set_points_as_corners(pts)
            return c

        curva_estatica = get_curva_escala()
        bola_topo.move_to([x_solt + B_exag, y_solo, 0])

        lbl_aviso_exag = label("DESVIO EXAGERADO PARA VISUALIZAÇÃO", size=18, color=MAGENTA_COLOR, x=1.5, y=3.2)

        self.play(
            FadeIn(chao_linha),
            FadeIn(torre_mobject),
            FadeIn(linha_ref_queda),
            FadeIn(marcador_ref_solo),
            FadeIn(bola_topo),
            FadeIn(curva_estatica),
            FadeIn(eixos_locais),
            FadeIn(lbl_aviso_exag),
            run_time=1.1
        )

        curva_dinamica_escala = always_redraw(get_curva_escala)
        self.remove(curva_estatica)
        self.add(curva_dinamica_escala)

        bola_topo.add_updater(lambda m: m.move_to([
            x_solt + exag_tracker.get_value(),
            y_solo,
            0
        ]))

        # Animação do recuo da trajetória até a escala física real
        lbl_escala_real = label("ESCALA FÍSICA REAL", size=24, color=WHITE_COLOR, x=1.5, y=3.2)
        self.play(
            exag_tracker.animate.set_value(0.015),
            ReplacementTransform(lbl_aviso_exag, lbl_escala_real),
            run_time=3.0,
            rate_func=rate_functions.smooth
        )
        self.wait(2.0)

        bola_topo.clear_updaters()
        curva_dinamica_escala.clear_updaters()

        # Inset científico circular de ampliação
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

        seta_desvio = Arrow(
            [x_abaixo, y_pts_lupa + 0.28, 0],
            [x_impacto, y_pts_lupa + 0.28, 0],
            color=CYAN_COLOR, buff=0, stroke_width=3.5, max_tip_length_to_length_ratio=0.25
        )
        valor_desvio_txt = formula(r"0{,}77\,\mathrm{cm}", size=28, color=CYAN_COLOR, x=centro_lupa[0], y=y_pts_lupa + 0.65)
        titulo_inset = label("AMPLIAÇÃO CIENTÍFICA", size=18, color=WHITE_COLOR, x=centro_lupa[0], y=centro_lupa[1] + 1.25)

        grupo_lupa = VGroup(
            disco_lupa, linha_solo_lupa,
            ponto_abaixo_lupa, lbl_abaixo_lupa,
            ponto_impacto_lupa, lbl_impacto_lupa,
            seta_desvio, valor_desvio_txt,
            titulo_inset
        )

        self.play(FadeIn(grupo_lupa), run_time=1.5)
        self.wait(5.0)

        # =========================================================================
        # BLOCO 12 — FECHAMENTO REFLEXIVO (~10 s)
        # =========================================================================
        self.play(
            FadeOut(grupo_lupa),
            FadeOut(lbl_escala_real),
            eixos_locais.animate.set_opacity(0.06),
            torre_mobject.animate.set_opacity(0.06),
            chao_linha.animate.set_opacity(0.06),
            linha_ref_queda.animate.set_opacity(0.06),
            marcador_ref_solo.animate.set_opacity(0.06),
            bola_topo.animate.set_opacity(0.06),
            curva_dinamica_escala.animate.set_opacity(0.06),
            run_time=1.2
        )

        f1 = label("A OLHO NU,", size=32, color=WHITE_COLOR, y=2.2)
        f2 = label("A QUEDA PARECE VERTICAL.", size=32, color=WHITE_COLOR, y=1.5)
        f3_part1 = label("MAS ELA TERMINA ", size=25, color=WHITE_COLOR)
        f3_part2 = label("ALGUNS MILÍMETROS A LESTE.", size=25, color=CYAN_COLOR)
        f3 = VGroup(f3_part1, f3_part2).arrange(RIGHT, buff=0.12).move_to([0, 0.6, 0])

        sintese_box_txt = formula(r"50\,\mathrm{m}\ \rightarrow\ 0{,}77\,\mathrm{cm\ para\ leste}", size=36, color=CYAN_COLOR, y=-0.8)
        sintese_retangulo = SurroundingRectangle(sintese_box_txt, color=CYAN_COLOR, buff=0.25, stroke_width=2.5)

        self.play(FadeIn(f1), run_time=0.8)
        self.play(FadeIn(f2), run_time=1.0)
        self.play(FadeIn(f3), run_time=1.2)
        self.play(FadeIn(sintese_box_txt), Create(sintese_retangulo), run_time=1.4)
        self.wait(4.8)

        self.play(
            FadeOut(f1),
            FadeOut(f2),
            FadeOut(f3),
            FadeOut(sintese_box_txt),
            FadeOut(sintese_retangulo),
            run_time=1.5
        )
        self.wait(0.5)
