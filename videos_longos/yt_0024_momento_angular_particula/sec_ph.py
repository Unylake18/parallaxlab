"""Lote PH: hook H1–H3 e abertura A1–A2 (Three.js 'mesa_furo', câmera C_34 no centro da tela).
H1 órbita de 0,60 m · H2 a puxada em tempo real (o puxador desce 0,30 m) · H3 congela: seta azul da tração para o furo, arco âmbar do giro e a pergunta.
A1/A2: a mesa continua girando, desfocada (profundidade de campo no Three.js), atrás do bem-vindos, do título e de NESTE VÍDEO com três ícones."""
from pecas24 import *  # noqa: F401,F403


def icone_reta(c, s=1.0, cor=GEO):
    return VGroup(Line(c + P3(-0.55 * s, -0.12 * s), c + P3(0.55 * s, -0.12 * s)).set_stroke(cor, 4),
                  Dot(c + P3(0.25 * s, -0.12 * s), radius=0.07 * s, color=MAS), Dot(c + P3(-0.1 * s, 0.32 * s), radius=0.06 * s, color=WHITE_))


def icone_circ(c, s=1.0, cor=GEO):
    return VGroup(Circle(radius=0.42 * s).move_to(c).set_stroke(cor, 4),
                  Arrow(c + P3(0.42 * s, -0.05), c + P3(0.42 * s, 0.25 * s), buff=0, stroke_width=4, tip_length=0.14).set_color(cor),
                  Dot(c, radius=0.05 * s, color=WHITE_))


def icone_espiral(c, s=1.0, cor=GEO):
    pts = [c + s * (0.48 - 0.06 * a) * np.array([math.cos(a), math.sin(a), 0]) for a in np.linspace(0, 6.0, 80)]
    return VGroup(VMobject().set_points_smoothly(pts).set_stroke(cor, 4), Dot(c, radius=0.05 * s, color=WHITE_))


class LotePH(Lote24):
    def cam(self):
        """v2 §2.2 câmera viva: azimute ±3° lento (período 16 s) com amplitude self.der (0..1); as camadas presas à mesa são vivas."""
        c = super().cam()
        c["az"] += 3.0 * float(self.der.get_value()) * math.sin(2 * math.pi * self.clk.get_value() / 16.0)
        return c

    def estado3d(self, _t=0.0):
        e = super().estado3d(_t)
        e["furoLuz"] = round(1.0 + 2.0 * float(self.furo_luz.get_value()), 3)
        return e

    def corpo(self):
        self.der = ValueTracker(1.0)
        self.furo_luz = ValueTracker(0.0)
        self.add(self.der, self.furo_luz)
        self.camA = self.camB = C34H
        self.mov = mov_puxada(self)
        self.zp = zp_puxada(self)
        self.vth = vth_puxada(self)
        self.anda(1.0, tf=0.0)
        f3 = self.mesa()

        # ── H1: órbita de 0,60 m; rótulos FURO e PUXADOR com chamada (saem antes da puxada) ──
        self.an("H1")
        f3.op.set_value(1.0)                      # v5: a abertura não tem transição nenhuma; o 1º quadro já é a mesa
        self.gat("um fio que passa por um furinho")
        # caso 1: o anel do furo acende sozinho; o rótulo fica logo acima dele, dentro da órbita (linha curta que não cruza a órbita)
        c_furo = vivo(lambda: Line(self.tela((0, 0, 0)) + P3(0, 0.10), self.tela((0, 0, 0)) + P3(0, 0.36)).set_stroke(GEO, 2.2))
        l_furo = vivo(lambda: txt("FURO", 28, bold=True, color=GEO).move_to(self.tela((0, 0, 0)) + P3(0, 0.64)))
        self.play(self.furo_luz.animate.set_value(1.0), OpVivo(c_furo), OpVivo(l_furo), run_time=0.6)
        self.gat("desce até a mão de alguém")
        # caso 2: chamada do puxador pelo vão livre entre os cavaletes (rótulo embaixo do T, linha curta vertical)
        c_pux = vivo(lambda: Line(self.tela((0, 0, -0.53)) + P3(0, -0.08), self.tela((0, 0, -0.53)) + P3(0, -0.55)).set_stroke(GEO, 2.2))
        l_pux = vivo(lambda: txt("PUXADOR", 28, bold=True, color=GEO).move_to(self.tela((0, 0, -0.53)) + P3(0, -0.86)))
        self.play(OpVivo(c_pux), OpVivo(l_pux), run_time=0.6)
        self.ate(0.97)
        self.play(OpVivo(c_furo, entra=False), OpVivo(l_furo, entra=False), OpVivo(c_pux, entra=False), OpVivo(l_pux, entra=False),
                  self.furo_luz.animate.set_value(0.0), run_time=0.4)
        self.remove(c_furo, l_furo, c_pux, l_pux)

        # ── H2: a puxada em tempo real (rampa 0,15 s · 0,30 m/s · rampa 0,15 s); seta PUXA na descida ──
        self.an("H2")
        self.gat("puxa o fio")
        self.tp = self.tf() + 0.25
        pp = self.tela((0, 0, -0.52))
        s_pux = vetor_lab(pp + P3(0.75, 0.15), pp + P3(0.75, -0.85), FC)
        l_pux2 = txt("PUXA", 28, bold=True, color=FC).next_to(s_pux, RIGHT, buff=0.18)
        self.play(FadeIn(s_pux), FadeIn(l_pux2), run_time=0.5)
        self.wait(1.2)
        self.play(FadeOut(s_pux), FadeOut(l_pux2), run_time=0.4)
        self.gat("o raio cai pela metade")
        r_esq = VGroup(txt("RAIO", 30, bold=True, color=VETC), T(r"\div\,2", 44, WHITE_)).arrange(RIGHT, buff=0.18).move_to(P3(-4.6, 2.55))
        self.play(FadeIn(r_esq, shift=0.08 * DOWN), run_time=0.5)
        self.gat("quatro voltas")
        v_dir = VGroup(txt("VOLTAS", 30, bold=True, color=VEL), T(r"\times\,4", 44, WHITE_)).arrange(RIGHT, buff=0.18).move_to(P3(4.4, 2.55))
        self.play(FadeIn(v_dir, shift=0.08 * DOWN), run_time=0.5)
        self.ate(0.97)

        # ── H3: congela; seta da tração para o furo; arco do giro; a pergunta (hold de 2 s) ──
        self.an("H3")
        self.anda(0.0)
        self.der.set_value(0.0)
        self.play(FadeOut(r_esq), FadeOut(v_dir), run_time=0.4)
        pd = self.tela_disco()
        po = self.tela((0, 0, 0))
        u = (po - pd) / np.linalg.norm(po - pd)
        s_T = vetor_lab(pd + 0.30 * u, pd + 1.35 * u, FC)
        l_T = T(r"\vec T", 46, FC).move_to(pd + 0.75 * u + 0.45 * np.array([-u[1], u[0], 0]))
        if l_T.get_y() < pd[1]:
            l_T.move_to(pd + 0.75 * u - 0.45 * np.array([-u[1], u[0], 0]))
        self.gat("puxa o disco para o furo")
        self.play(FadeIn(s_T), FadeIn(l_T), run_time=0.6)
        # arco âmbar do sentido do giro (anti-horário visto de cima), em volta do furo, projetado na câmera
        x, y = self.disco()
        th0 = math.atan2(y, x)
        pts = [self.tela((0.42 * math.cos(th0 + a), 0.42 * math.sin(th0 + a), 0.002)) for a in np.linspace(0.35, 1.6, 30)]
        arco = VMobject().set_points_smoothly(pts).set_stroke(ANG, 4).set_z_index(12)
        pa, pb = pts[-2], pts[-1]
        ua = (pb - pa) / np.linalg.norm(pb - pa)
        ponta = Polygon(pb + 0.2 * ua, pb - 0.05 * ua + 0.11 * np.array([-ua[1], ua[0], 0]), pb - 0.05 * ua - 0.11 * np.array([-ua[1], ua[0], 0])) \
            .set_fill(ANG, 1).set_stroke(ANG, 1).set_z_index(12)
        self.gat("nunca empurra para o lado")
        self.play(Create(arco), FadeIn(ponta), run_time=0.7)
        perg = VGroup(txt("O FIO SÓ PUXA PARA O CENTRO.", 34, bold=True),
                      txt("QUEM EMPURRA O DISCO PARA O LADO?", 34, bold=True, color=ANG)).arrange(DOWN, buff=0.16).move_to(P3(0.6, 3.0))
        self.gat("se ninguém empurra")
        self.play(FadeIn(perg[0], shift=0.06 * DOWN), run_time=0.5)
        self.play(FadeIn(perg[1], shift=0.06 * DOWN), run_time=0.5)
        self.ate(0.995)

        # ── A1: logo e bem-vindos; a mesa volta a girar, desfocada ──
        self.an("A1")
        self.anda(1.0)
        logo = self.logo(5.2).move_to(P3(0, 0.75)).set_z_index(30)
        bv = txt("BEM-VINDOS AO PARALLAX LAB", 36, bold=True).move_to(P3(0, -0.85)).set_z_index(30)
        self.play(FadeOut(VGroup(s_T, l_T, arco, ponta, perg)), self.desf_tr.animate.set_value(1.0), f3.op.animate.set_value(0.38), run_time=0.5)
        self.der.set_value(1.0)
        self.play(FadeIn(logo), FadeIn(bv), run_time=0.5)
        tit = txt("MOMENTO ANGULAR DE UMA PARTÍCULA", 46, bold=True).move_to(P3(0, 2.3)).set_z_index(30)
        self.gat("hoje o assunto")                      # v13: "Hoje o assunto é…" fecha o A1 (a fala nova); o título entra nessa frase
        self.play(FadeOut(logo), FadeOut(bv), FadeIn(tit, shift=0.08 * DOWN), run_time=0.6)
        self.ate(0.97)

        # ── A2: NESTE VÍDEO e três ícones que acendem nas palavras ──
        self.an("A2")
        nv =txt("NESTE VÍDEO:", 30, color=GEO).move_to(P3(0, 1.15)).set_z_index(30)
        cs = [P3(-4.2, -0.45), P3(0, -0.45), P3(4.2, -0.45)]
        ics = [icone_reta(cs[0], 1.9, GEO), icone_circ(cs[1], 1.8, GEO), icone_espiral(cs[2], 1.8, GEO)]
        legs = [txt("ATÉ UMA RETA GIRA", 26, bold=True), linha_base([txt("O QUE MUDA", 26, bold=True), T("L", 40, LMAG)], 0.14), txt("DE VOLTA À MESA", 26, bold=True)]
        for ic, lg, c in zip(ics, legs, cs):
            ic.set_z_index(30)
            lg.move_to(c + P3(0, -1.35)).set_z_index(30)
        self.gat("a gente vai ver")
        self.play(FadeIn(nv), run_time=0.4)
        for frase, k in (("em linha reta", 0), ("o que faz esse momento mudar", 1), ("volta para essa mesa", 2)):
            self.gat(frase)
            self.play(FadeIn(ics[k], scale=0.9), FadeIn(legs[k]), run_time=0.6)
        self.ate(0.97)
        self.play(FadeOut(VGroup(tit, nv, *ics, *legs)), self.desf_tr.animate.set_value(0.0), f3.op.animate.set_value(1.0), run_time=0.4)
