"""vid_0024 — Desvio para Leste na Queda Livre (Efeito Coriolis)
Série: DA EQUAÇÃO AO FENÔMENO · EP. 05
Formato: curto_vertical (9:16)
Versão: V4A — Bloco Fundamental: Do Gancho ao Nascimento de Coriolis
Duração: ~80 a 90 segundos.
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
config.pixel_width = 540
config.pixel_height = 960
config.frame_rate = 15

# Gramática semântica de cores oficial Parallax Lab
WHITE_COLOR = "#F5F7FF"
CYAN_COLOR = "#35D9FF"     # Coriolis, leste, desvio lateral, resultado principal
BLUE_COLOR = "#267BFF"     # Velocidade da bola, movimento radial da conta
VIOLET_COLOR = "#745CFF"   # Rotação, omega, omega_T, norte entrando na tela
MAGENTA_COLOR = "#EA63FF"  # Aviso excepcional de desvio exagerado
MUTED_COLOR = "#8492AE"    # Rótulos secundários, eixos neutros, linhas de apoio


def label(text, size=24, color=WHITE_COLOR, x=0, y=0, width=7.6):
    """Texto não-matemático oficial em Space Grotesk Medium."""
    oversample = 2 if size >= 25 else 4
    m = screen_text(text, font_size=size, color=color, oversample=oversample)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m.move_to([x, y, 0])


def formula(*parts, size=34, color=WHITE_COLOR, x=0, y=0, width=7.6):
    """Fórmulas matemáticas em MathTex com escala segura."""
    m = MathTex(*parts, font_size=size, color=color)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m.move_to([x, y, 0])


def setup_header(scene):
    """Cabeçalho oficial V4: EP. 05 à esquerda, watermark à direita."""
    header_series = screen_text("DA EQUAÇÃO AO FENÔMENO · EP. 05", font_size=18, color=WHITE_COLOR)
    header_series.set_opacity(0.65).to_corner(UP + LEFT, buff=0.42)
    watermark = ImageMobject(str(WATERMARK_PATH)).set_width(1.75).set_opacity(0.35)
    watermark.to_corner(UP + RIGHT, buff=0.30)
    scene.add(header_series, watermark)
    return header_series, watermark


def build_torre(x_c=-1.6, y_solo=-4.0, y_topo=3.6, w_base=1.1, w_topo=0.45):
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

    x_soltura = x_c + w_topo / 2 + 0.35  # ~ -1.025
    plat = Line([x_c - w_topo / 2 - 0.15, y_topo, 0], [x_soltura + 0.18, y_topo, 0], color=WHITE_COLOR, stroke_width=3.2)
    topo_cap = Line([x_c - w_topo / 2, y_topo + 0.08, 0], [x_soltura + 0.18, y_topo + 0.08, 0], color=CYAN_COLOR, stroke_width=1.5, stroke_opacity=0.6)

    base_esq = Line([x_c - w_base / 2 - 0.15, y_solo, 0], [x_c - w_base / 2 + 0.15, y_solo, 0], color=WHITE_COLOR, stroke_width=3.0)
    base_dir = Line([x_c + w_base / 2 - 0.15, y_solo, 0], [x_c + w_base / 2 + 0.15, y_solo, 0], color=WHITE_COLOR, stroke_width=3.0)

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


def build_terra_25d(center=[0, 0.4, 0], radius=2.5):
    """Constrói uma representação 2.5D sofisticada da Terra com eixos, equador e paralelos."""
    cx, cy, _ = center
    
    # 1. Disco base escura com gradiente suave
    disco_base = Circle(radius=radius, color="#223354", fill_color="#080E1C", fill_opacity=0.92, stroke_width=2.5)
    disco_base.move_to(center)
    
    # 2. Eixo polar
    eixo_polar = Line([cx, cy - radius - 0.7, 0], [cx, cy + radius + 0.7, 0], color=MUTED_COLOR, stroke_width=2.2, stroke_opacity=0.7)
    polo_norte = Dot([cx, cy + radius + 0.7, 0], radius=0.06, color=WHITE_COLOR)
    polo_sul = Dot([cx, cy - radius - 0.7, 0], radius=0.06, color=WHITE_COLOR)
    
    # 3. Equador destacado (elipse frontal)
    equador = Ellipse(width=2 * radius, height=2 * radius * 0.44, color=CYAN_COLOR, stroke_width=3.6)
    equador.move_to(center)
    
    # 4. Paralelos (Trópicos e Círculos Polares)
    paralelos = VGroup()
    for dy_factor in [0.45, -0.45, 0.75, -0.75]:
        dy = dy_factor * radius
        r_sub = np.sqrt(max(0.1, radius**2 - dy**2))
        p = Ellipse(width=2 * r_sub, height=2 * r_sub * 0.44, color="#3D527A", stroke_width=1.2, stroke_opacity=0.4)
        p.move_to([cx, cy + dy, 0])
        paralelos.add(p)
        
    # 5. Meridianos frontais elípticos
    meridianos = VGroup()
    for fx in [0.28, 0.58, 0.85]:
        m1 = Ellipse(width=2 * radius * fx, height=2 * radius, color="#48608F", stroke_width=1.1, stroke_opacity=0.35)
        m1.move_to(center)
        meridianos.add(m1)
    
    # 6. Arco de rotação violeta em torno do eixo polar no topo
    y_arco = cy + radius + 0.35
    rx_arco = 0.8
    ry_arco = 0.3
    # Arco cobrindo de -140 deg a 40 deg
    t_vals = np.linspace(-np.pi * 0.75, np.pi * 0.25, 40)
    pts_arco = [[cx + rx_arco * np.cos(t), y_arco + ry_arco * np.sin(t), 0] for t in t_vals]
    arco_linha = VMobject(color=VIOLET_COLOR, stroke_width=3.2)
    arco_linha.set_points_smoothly(pts_arco)
    
    # Seta tangente na ponta do arco
    p_fim = np.array(pts_arco[-1])
    p_ant = np.array(pts_arco[-2])
    tan_dir = normalize(p_fim - p_ant)
    seta_arco = Arrow(p_fim - tan_dir * 0.25, p_fim, buff=0, color=VIOLET_COLOR, stroke_width=3.2, max_tip_length_to_length_ratio=0.38)
    arco_rotacao = VGroup(arco_linha, seta_arco)
    
    # 7. Símbolo omega_T e rótulo
    omega_sym = MathTex(r"\vec\omega_T", color=VIOLET_COLOR, font_size=32).next_to(arco_rotacao, RIGHT, buff=0.18)
    rot_label = screen_text("rotação da Terra", font_size=18, color=VIOLET_COLOR).next_to(omega_sym, DOWN, buff=0.12, aligned_edge=LEFT)
    omega_grupo = VGroup(arco_rotacao, omega_sym, rot_label)
    
    # 8. Ponto do experimento no equador frontal
    ponto_eq = Dot([cx - 0.4, cy - radius * 0.44 * 0.35, 0], radius=0.11, color=CYAN_COLOR)
    halo_eq = Dot([cx - 0.4, cy - radius * 0.44 * 0.35, 0], radius=0.22, color=CYAN_COLOR).set_opacity(0.35)
    ponto_grupo = VGroup(halo_eq, ponto_eq)
    
    terra_completa = VGroup(disco_base, paralelos, meridianos, equador, eixo_polar, polo_norte, polo_sul, ponto_grupo)
    return terra_completa, ponto_grupo, equador, arco_rotacao, omega_sym, rot_label, center


class QuedaCoriolisV4A(Scene):
    def construct(self):
        # Header oficial fixo
        setup_header(self)

        # =====================================================================
        # BLOCO 1: GANCHO FENOMENOLÓGICO (0s ~ 9s)
        # =====================================================================
        torre, x_soltura = build_torre(x_c=-1.6, y_solo=-4.0, y_topo=3.6)
        solo = Line([-4.2, -4.0, 0], [4.2, -4.0, 0], color=WHITE_COLOR, stroke_width=2.5)
        linha_vertical = DashedLine([x_soltura, 3.6, 0], [x_soltura, -4.0, 0], color=MUTED_COLOR, stroke_width=2.0, dash_length=0.15)
        
        # Marcador no solo
        alvo_circ = Circle(radius=0.12, color=WHITE_COLOR, stroke_width=2.0).move_to([x_soltura, -4.0, 0])
        alvo_cross = VGroup(
            Line([x_soltura - 0.18, -4.0, 0], [x_soltura + 0.18, -4.0, 0], color=WHITE_COLOR, stroke_width=1.5),
            Line([x_soltura, -4.0 - 0.18, 0], [x_soltura, -4.0 + 0.18, 0], color=WHITE_COLOR, stroke_width=1.5)
        )
        alvo_grupo = VGroup(alvo_circ, alvo_cross)
        
        # Bola no topo
        bola_topo = Dot([x_soltura, 3.6, 0], radius=0.13, color=WHITE_COLOR)
        halo_topo = Dot([x_soltura, 3.6, 0], radius=0.25, color=CYAN_COLOR).set_opacity(0.4)
        
        # Perguntas de impacto
        t_pergunta1 = label("SE EU SOLTAR A BOLA...", size=26, color=WHITE_COLOR, y=4.5)
        t_pergunta2 = label("ELA CAI EXATAMENTE AQUI?", size=26, color=CYAN_COLOR, y=-4.6)

        self.play(FadeIn(torre), Create(solo), run_time=1.3)
        self.play(Create(linha_vertical), FadeIn(alvo_grupo), FadeIn(halo_topo), FadeIn(bola_topo), run_time=1.1)
        self.play(Write(t_pergunta1), run_time=0.9)
        self.play(Write(t_pergunta2), run_time=0.9)
        self.wait(2.5)

        # Transição para o Bloco 2
        self.play(
            FadeOut(t_pergunta1), FadeOut(t_pergunta2),
            FadeOut(torre), FadeOut(linha_vertical), FadeOut(alvo_grupo), FadeOut(halo_topo), FadeOut(bola_topo), FadeOut(solo),
            run_time=1.2
        )

        # =====================================================================
        # BLOCO 2: TERRA 2.5D NO MANIM (9s ~ 22s)
        # =====================================================================
        terra, ponto_eq_grupo, equador_mobj, arco_rotacao, omega_sym, rot_label, c_terra = build_terra_25d(center=[0, 0.4, 0], radius=2.5)
        selo_terra = label("EQUADOR · 50 m · SEM ARRASTO", size=20, color=MUTED_COLOR, y=4.5)

        self.play(FadeIn(selo_terra), run_time=0.8)
        self.play(FadeIn(terra), FadeIn(arco_rotacao), Write(omega_sym), FadeIn(rot_label), run_time=1.8)
        self.wait(1.0)

        # Rotação suave do ponto no equador
        alpha_tracker = ValueTracker(0)
        
        def update_ponto(mob):
            a = alpha_tracker.get_value()
            rx = 2.5
            ry = 2.5 * 0.44
            cx, cy, _ = c_terra
            # Movimento angular de oeste para leste (na face frontal)
            phi = -0.7 + a * 1.2
            x = cx + rx * np.sin(phi)
            y = cy - ry * np.cos(phi) * 0.45
            mob.move_to([x, y, 0])

        ponto_eq_grupo.add_updater(update_ponto)
        self.play(alpha_tracker.animate.set_value(1.0), run_time=4.0, rate_func=linear)
        ponto_eq_grupo.remove_updater(update_ponto)
        self.wait(1.5)

        # =====================================================================
        # BLOCO 3: DO GLOBO PARA A HASTE — CONTEXTO (22s ~ 31s)
        # =====================================================================
        t_contexto = label("A Terra gira. Descrevemos o movimento em um referencial que gira.", size=21, color=WHITE_COLOR, y=4.5)
        self.play(Transform(selo_terra, t_contexto), run_time=1.2)
        self.wait(1.0)

        # Posição do laboratório da haste (quadrante inferior para dar respiro à álgebra)
        pivo_pt = np.array([-2.0, -1.5, 0])
        theta_0 = 18 * DEGREES
        haste_len = 3.8
        p_ponta = pivo_pt + haste_len * np.array([np.cos(theta_0), np.sin(theta_0), 0])

        # Haste e Pivô
        pivo_base = Dot(pivo_pt, radius=0.18, color=WHITE_COLOR)
        pivo_centro = Dot(pivo_pt, radius=0.08, color="#080E1C")
        pivo_mobj = VGroup(pivo_base, pivo_centro)
        haste_linha = Line(pivo_pt, p_ponta, color=WHITE_COLOR, stroke_width=3.2)

        # Arco omega da haste posicionado à esquerda do pivô para não colidir
        arco_haste_pts = [pivo_pt + 0.95 * np.array([np.cos(t), np.sin(t), 0]) for t in np.linspace(0, theta_0 + 26 * DEGREES, 25)]
        arco_haste_linha = VMobject(color=VIOLET_COLOR, stroke_width=2.6).set_points_smoothly(arco_haste_pts)
        p_fim_h = np.array(arco_haste_pts[-1])
        p_ant_h = np.array(arco_haste_pts[-2])
        tan_h = normalize(p_fim_h - p_ant_h)
        seta_h = Arrow(p_fim_h - tan_h * 0.22, p_fim_h, buff=0, color=VIOLET_COLOR, stroke_width=2.8, max_tip_length_to_length_ratio=0.38)
        arco_haste_grupo = VGroup(arco_haste_linha, seta_h)
        omega_haste_sym = MathTex(r"\omega", color=VIOLET_COLOR, font_size=28).move_to(pivo_pt + np.array([-0.85, 0.55, 0]))
        omega_haste_lbl = screen_text("velocidade angular", font_size=16, color=MUTED_COLOR).next_to(omega_haste_sym, UP, buff=0.08, aligned_edge=LEFT)

        # A Terra se contrai e funde no pivô da haste, enquanto omega_T se torna omega
        self.play(
            terra.animate.scale(0.08).move_to(pivo_pt).set_opacity(0),
            FadeOut(selo_terra),
            Transform(arco_rotacao, arco_haste_grupo),
            Transform(omega_sym, omega_haste_sym),
            Transform(rot_label, omega_haste_lbl),
            FadeIn(pivo_mobj),
            Create(haste_linha),
            run_time=2.2
        )
        self.remove(terra)
        self.wait(1.0)

        # =====================================================================
        # BLOCO 4: HASTE — PRIMEIRA CONTRIBUIÇÃO (a1 = omega * u) (31s ~ 47s)
        # =====================================================================
        # Conta azul na haste
        r0 = 1.3
        p_conta0 = pivo_pt + r0 * np.array([np.cos(theta_0), np.sin(theta_0), 0])
        conta_mobj = Dot(p_conta0, radius=0.13, color=BLUE_COLOR)
        
        # Vetor radial u saindo da conta
        dir_radial = np.array([np.cos(theta_0), np.sin(theta_0), 0])
        dir_tang = np.array([-np.sin(theta_0), np.cos(theta_0), 0])
        seta_u = Arrow(p_conta0, p_conta0 + 0.95 * dir_radial, buff=0, color=BLUE_COLOR, stroke_width=3.2, max_tip_length_to_length_ratio=0.25)
        u_sym = MathTex(r"u", color=BLUE_COLOR, font_size=28).next_to(seta_u, DOWN, buff=0.14)
        u_lbl = screen_text("velocidade radial", font_size=16, color=MUTED_COLOR).next_to(u_sym, DOWN, buff=0.08, aligned_edge=LEFT)
        u_bloco = VGroup(seta_u, u_sym, u_lbl)

        self.play(FadeIn(conta_mobj), FadeIn(u_bloco), run_time=1.2)
        self.wait(1.0)

        # Congelar dois instantes: conta anda dr = u dt
        ghost_conta = Dot(p_conta0, radius=0.13, color=BLUE_COLOR).set_opacity(0.35)
        dr_val = 1.05
        p_conta1 = pivo_pt + (r0 + dr_val) * np.array([np.cos(theta_0), np.sin(theta_0), 0])
        
        seta_dr = Arrow(p_conta0, p_conta1, buff=0, color=WHITE_COLOR, stroke_width=2.0, max_tip_length_to_length_ratio=0.2)
        dr_sym = MathTex(r"dr = u\,dt", font_size=24, color=WHITE_COLOR).next_to(seta_dr, DOWN, buff=0.35)

        # Vetores tangenciais vt = omega * r
        vt0_len = 0.65
        vt1_len = 1.25
        seta_vt0 = Arrow(p_conta0, p_conta0 + vt0_len * dir_tang, buff=0, color=WHITE_COLOR, stroke_width=2.4, stroke_opacity=0.6, max_tip_length_to_length_ratio=0.22)
        lbl_vt0 = MathTex(r"v_t(r)", font_size=22, color=MUTED_COLOR).next_to(seta_vt0, UP + LEFT, buff=0.08)

        seta_vt1 = Arrow(p_conta1, p_conta1 + vt1_len * dir_tang, buff=0, color=WHITE_COLOR, stroke_width=2.8, max_tip_length_to_length_ratio=0.22)
        lbl_vt1 = MathTex(r"v_t(r+dr)", font_size=22, color=WHITE_COLOR).next_to(seta_vt1, UP + LEFT, buff=0.08)

        self.add(ghost_conta)
        self.play(
            conta_mobj.animate.move_to(p_conta1),
            u_bloco.animate.shift(dr_val * dir_radial),
            Create(seta_dr),
            run_time=1.5
        )
        # O u voa da seta para dr = u dt
        self.play(Write(dr_sym), run_time=1.0)
        self.play(Create(seta_vt0), FadeIn(lbl_vt0), Create(seta_vt1), FadeIn(lbl_vt1), run_time=1.4)
        self.wait(1.0)

        # Álgebra do Efeito 1 à direita e acima (espaço protegido)
        x_alg = 2.4
        eq1_1 = MathTex(r"v_t = \omega r", font_size=28, color=WHITE_COLOR).move_to([x_alg, 4.0, 0])
        eq1_2 = MathTex(r"dv_t = \omega\,dr", font_size=28, color=WHITE_COLOR).move_to([x_alg, 3.4, 0])
        eq1_3 = MathTex(r"dv_t = \omega(u\,dt)", font_size=28, color=WHITE_COLOR).move_to([x_alg, 2.8, 0])
        eq1_res = MathTex(r"\boxed{a_1 = \omega u}", font_size=32, color=CYAN_COLOR).move_to([x_alg, 2.0, 0])
        lbl_efeito1 = screen_text("raio aumenta → v_t aumenta", font_size=16, color=MUTED_COLOR).next_to(eq1_res, DOWN, buff=0.15)

        self.play(Write(eq1_1), run_time=0.8)
        self.play(Write(eq1_2), run_time=0.8)
        self.play(TransformMatchingShapes(eq1_2.copy(), eq1_3), run_time=1.0)
        self.play(Write(eq1_res), FadeIn(lbl_efeito1), run_time=1.2)
        self.wait(2.0)

        # =====================================================================
        # BLOCO 5: HASTE — SEGUNDA CONTRIBUIÇÃO (a2 = omega * u) (47s ~ 62s)
        # =====================================================================
        # Mesma cena! Limpar elementos intermediários, guardar eq1_res no topo
        self.play(
            FadeOut(eq1_1), FadeOut(eq1_2), FadeOut(eq1_3), FadeOut(lbl_efeito1),
            FadeOut(seta_vt0), FadeOut(lbl_vt0), FadeOut(seta_vt1), FadeOut(lbl_vt1),
            FadeOut(seta_dr), FadeOut(dr_sym), FadeOut(ghost_conta),
            eq1_res.animate.move_to([x_alg, 4.4, 0]).scale(0.85),
            run_time=1.2
        )

        # Agora mantemos u fixo em módulo e giramos a haste de dtheta = omega dt
        d_theta = 22 * DEGREES
        theta_1 = theta_0 + d_theta
        
        # Ghost do vetor u na orientação antiga
        seta_u_antiga = Arrow(p_conta1, p_conta1 + 0.95 * dir_radial, buff=0, color=BLUE_COLOR, stroke_width=2.0, stroke_opacity=0.35, max_tip_length_to_length_ratio=0.25)
        
        # Nova posição da haste e conta
        dir_radial_novo = np.array([np.cos(theta_1), np.sin(theta_1), 0])
        p_conta_novo = pivo_pt + (r0 + dr_val) * dir_radial_novo
        p_ponta_novo = pivo_pt + haste_len * dir_radial_novo
        
        # Vetor diferença dv unindo as pontas dos dois vetores u (com caudas alinhadas em p_conta_novo)
        seta_u_ref = Arrow(p_conta_novo, p_conta_novo + 0.95 * dir_radial, buff=0, color=MUTED_COLOR, stroke_width=2.0, stroke_opacity=0.45, max_tip_length_to_length_ratio=0.25)
        seta_u_nova = Arrow(p_conta_novo, p_conta_novo + 0.95 * dir_radial_novo, buff=0, color=BLUE_COLOR, stroke_width=3.2, max_tip_length_to_length_ratio=0.25)
        
        ponta_ref = p_conta_novo + 0.95 * dir_radial
        ponta_nova = p_conta_novo + 0.95 * dir_radial_novo
        seta_dv = Arrow(ponta_ref, ponta_nova, buff=0, color=WHITE_COLOR, stroke_width=2.8, max_tip_length_to_length_ratio=0.3)
        lbl_dv = MathTex(r"d\vec v", font_size=22, color=WHITE_COLOR).next_to(seta_dv, UP, buff=0.08)

        # Arco dtheta na haste
        arco_dth_pts = [pivo_pt + 1.8 * np.array([np.cos(t), np.sin(t), 0]) for t in np.linspace(theta_0, theta_1, 20)]
        arco_dth = VMobject(color=VIOLET_COLOR, stroke_width=2.2).set_points_smoothly(arco_dth_pts)
        lbl_dth = MathTex(r"d\theta", font_size=20, color=VIOLET_COLOR).next_to(arco_dth, RIGHT, buff=0.08)

        self.play(
            Rotate(haste_linha, angle=d_theta, about_point=pivo_pt),
            conta_mobj.animate.move_to(p_conta_novo),
            u_bloco.animate.move_to(p_conta_novo + 0.45 * dir_radial_novo),
            Create(arco_dth), Write(lbl_dth),
            run_time=1.5
        )
        self.play(FadeIn(seta_u_ref), Create(seta_dv), Write(lbl_dv), run_time=1.2)
        self.wait(1.0)

        # Álgebra do Efeito 2
        eq2_1 = MathTex(r"|d\vec v| \approx u\,d\theta", font_size=28, color=WHITE_COLOR).move_to([x_alg, 3.5, 0])
        eq2_2 = MathTex(r"d\theta = \omega\,dt", font_size=28, color=VIOLET_COLOR).move_to([x_alg, 2.9, 0])
        eq2_3 = MathTex(r"|d\vec v| = u\omega\,dt", font_size=28, color=WHITE_COLOR).move_to([x_alg, 2.3, 0])
        eq2_res = MathTex(r"\boxed{a_2 = \omega u}", font_size=32, color=CYAN_COLOR).move_to([x_alg, 1.5, 0])
        lbl_efeito2 = screen_text("mesmo u, nova direção", font_size=16, color=MUTED_COLOR).next_to(eq2_res, DOWN, buff=0.15)

        self.play(Write(eq2_1), run_time=0.9)
        self.play(Write(eq2_2), run_time=0.8)
        self.play(TransformMatchingShapes(eq2_2.copy(), eq2_3), run_time=1.0)
        self.play(Write(eq2_res), FadeIn(lbl_efeito2), run_time=1.2)
        self.wait(2.0)

        # =====================================================================
        # BLOCO 6: O FATOR 2 NASCE NA MESMA TELA (62s ~ 71s)
        # =====================================================================
        # Haste e geometria vão para baixa opacidade
        geometria_haste = VGroup(
            haste_linha, pivo_mobj, conta_mobj, u_bloco, seta_u_ref, seta_dv, lbl_dv,
            arco_dth, lbl_dth, arco_rotacao, omega_sym, rot_label
        )

        self.play(
            geometria_haste.animate.set_opacity(0.12),
            FadeOut(eq2_1), FadeOut(eq2_2), FadeOut(eq2_3), FadeOut(lbl_efeito2),
            eq1_res.animate.move_to([0, 2.6, 0]).scale(1.15),
            eq2_res.animate.move_to([0, 1.6, 0]).scale(1.15),
            run_time=1.5
        )

        # As duas equações se fundem em a_perp = a1 + a2 = 2 omega u
        soma_1 = MathTex(r"a_\perp = a_1 + a_2", font_size=34, color=WHITE_COLOR).move_to([0, 0.7, 0])
        soma_2 = MathTex(r"a_\perp = \omega u + \omega u", font_size=34, color=WHITE_COLOR).move_to([0, 0.7, 0])
        soma_res = MathTex(r"\boxed{a_\perp = 2\omega u}", font_size=40, color=CYAN_COLOR).move_to([0, -0.3, 0])
        lbl_fator2 = screen_text("DUAS CONTRIBUIÇÕES IGUAIS", font_size=20, color=CYAN_COLOR).next_to(soma_res, DOWN, buff=0.25)

        self.play(Write(soma_1), run_time=1.0)
        self.play(TransformMatchingShapes(soma_1, soma_2), run_time=1.2)
        self.play(Write(soma_res), FadeIn(lbl_fator2), run_time=1.4)
        self.wait(2.5)

        # =====================================================================
        # BLOCO 7: TROCA DE REFERENCIAL E VETOR DE CORIOLIS (71s ~ 90s)
        # =====================================================================
        # Retirar as fórmulas do centro para abrir espaço para o laboratório
        self.play(
            FadeOut(eq1_res), FadeOut(eq2_res), FadeOut(soma_2),
            FadeOut(lbl_fator2),
            soma_res.animate.move_to([2.3, 4.4, 0]).scale(0.72),
            run_time=1.2
        )

        # Limpar vetores auxiliares de dv e dtheta e labels já entendidos
        self.remove(seta_u_ref, seta_dv, lbl_dv, arco_dth, lbl_dth)

        # Restaurar haste e colocar em rotação (Vista Inercial)
        haste_linha.set_opacity(1.0)
        pivo_mobj.set_opacity(1.0)
        conta_mobj.set_opacity(1.0)
        seta_u.set_opacity(1.0)
        arco_rotacao.set_opacity(1.0)
        omega_sym.set_opacity(1.0)

        lbl_ref = label("vista inercial", size=22, color=MUTED_COLOR, x=0, y=3.2)
        
        # Vetor aceleração tangencial 2 omega u (sentido do movimento)
        dir_tang_atual = np.array([-np.sin(theta_1), np.cos(theta_1), 0])
        seta_2wu = Arrow(p_conta_novo, p_conta_novo + 1.35 * dir_tang_atual, buff=0, color=WHITE_COLOR, stroke_width=3.6, max_tip_length_to_length_ratio=0.25)
        lbl_2wu = MathTex(r"2\omega u", font_size=26, color=WHITE_COLOR).next_to(seta_2wu, UP + LEFT, buff=0.1)

        self.play(FadeIn(lbl_ref), Create(seta_2wu), Write(lbl_2wu), run_time=1.2)
        self.wait(1.5)

        # TRANSIÇÃO DE REFERENCIAL: O mundo gira no sentido contrário (-theta_1)
        # trazendo a haste para a horizontal estática!
        conta_horizontal_pt = pivo_pt + (r0 + dr_val) * np.array([1, 0, 0])

        lbl_ref_girante = label("vista que gira com a haste", size=22, color=CYAN_COLOR, x=0, y=3.2)

        # No referencial que gira, a aceleração aparente INVERTE de sentido: aponta para baixo (-y)
        seta_coriolis = Arrow(conta_horizontal_pt, conta_horizontal_pt + 1.35 * np.array([0, -1, 0]), buff=0, color=CYAN_COLOR, stroke_width=3.8, max_tip_length_to_length_ratio=0.25)
        lbl_coriolis_nome = screen_text("aceleração de Coriolis", font_size=18, color=CYAN_COLOR).next_to(seta_coriolis, DOWN, buff=0.18)
        sym_ac = MathTex(r"\vec a_C", font_size=32, color=CYAN_COLOR).next_to(seta_coriolis, RIGHT, buff=0.14)

        self.play(
            Rotate(haste_linha, angle=-theta_1, about_point=pivo_pt),
            conta_mobj.animate.move_to(conta_horizontal_pt),
            seta_u.animate.move_to(conta_horizontal_pt + 0.47 * np.array([1, 0, 0])),
            FadeOut(u_sym), FadeOut(u_lbl), FadeOut(rot_label),
            FadeOut(seta_2wu), FadeOut(lbl_2wu),
            Transform(lbl_ref, lbl_ref_girante),
            run_time=2.2, rate_func=smooth
        )
        # Seta inverte de sentido e nasce aC
        self.play(Create(seta_coriolis), Write(sym_ac), FadeIn(lbl_coriolis_nome), run_time=1.5)
        self.wait(1.5)

        # Equação de Coriolis Geral com layout espaçado impecável
        eq_coriolis_geral = MathTex(r"\boxed{\vec a_C = -2\vec\omega \times \vec v}", font_size=38, color=CYAN_COLOR).move_to([0, 1.4, 0])
        
        # Callouts anatômicos que explicam cada termo sem colisões
        c_2 = screen_text("2 contribuições", font_size=16, color=WHITE_COLOR).move_to([-1.5, 2.5, 0])
        seta_c2 = Arrow(c_2.get_bottom(), eq_coriolis_geral.get_top() + LEFT * 0.7, buff=0.1, color=WHITE_COLOR, stroke_width=1.5, max_tip_length_to_length_ratio=0.25)

        c_omega = screen_text("rotação", font_size=16, color=VIOLET_COLOR).move_to([1.1, 2.5, 0])
        seta_comega = Arrow(c_omega.get_bottom(), eq_coriolis_geral.get_top() + RIGHT * 0.15, buff=0.1, color=VIOLET_COLOR, stroke_width=1.5, max_tip_length_to_length_ratio=0.25)

        c_sinal = screen_text("sentido oposto", font_size=16, color=MUTED_COLOR).move_to([-1.7, 0.3, 0])
        seta_csinal = Arrow(c_sinal.get_top(), eq_coriolis_geral.get_bottom() + LEFT * 1.3, buff=0.1, color=MUTED_COLOR, stroke_width=1.5, max_tip_length_to_length_ratio=0.25)

        c_v = screen_text("velocidade relativa", font_size=16, color=BLUE_COLOR).move_to([1.4, 0.3, 0])
        seta_cv = Arrow(c_v.get_top(), eq_coriolis_geral.get_bottom() + RIGHT * 1.0, buff=0.1, color=BLUE_COLOR, stroke_width=1.5, max_tip_length_to_length_ratio=0.25)

        self.play(Write(eq_coriolis_geral), run_time=1.5)
        self.play(
            FadeIn(c_2), Create(seta_c2),
            FadeIn(c_sinal), Create(seta_csinal),
            FadeIn(c_omega), Create(seta_comega),
            FadeIn(c_v), Create(seta_cv),
            run_time=1.8
        )
        self.wait(3.5)

