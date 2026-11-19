"""Lote PA: abertura A1 (logo), A2 (título + três ícones: soma de pedaços, haltere com eixo móvel, barra com dois eixos), A3 (uma partícula
girando com v = ωr e ½mv²; ela vira muitas, em círculos de raios diferentes, todas com o mesmo ω, e os círculos viram o disco em pedaços rosa)."""
from pecas21 import *  # noqa: F401,F403

C_A3 = P3(-3.6, -0.45)
W_A3 = 1.1                                          # rad/s na tela (≈ 4° por quadro)


class LoteA(Lote21):
    def corpo(self):
        # ── A1 ──
        self.an("A1")
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        aneis = VGroup(*[Circle(radius=r).move_to(P3(0, 0.9)).set_stroke(VEL, 2.2, opacity=o) for r, o in ((2.1, 0.35), (2.45, 0.2))])
        bv = txt("BEM-VINDOS AO PARALLAX LAB", 30).move_to(P3(0, -1.6))
        self.play(FadeIn(logo, scale=0.94), FadeIn(aneis), FadeIn(bv, shift=0.1 * UP), run_time=0.8)
        self.play(aneis.animate.scale(1.05), run_time=max(0.5, self.resta() - 0.4))
        self.ate(0.99)
        # ── A2 ──
        self.an("A2")
        tt = txt("MOMENTO DE INÉRCIA:", 44, bold=True).move_to(P3(0, 2.7))
        tt2 = txt("POR QUE O MESMO BASTÃO EXIGE O DOBRO DE ENERGIA PARA GIRAR?", 28, bold=True).next_to(tt, DOWN, buff=0.2)
        nv = txt("NESTE VÍDEO:", 28).move_to(P3(-5.4, 0.85))
        ics = VGroup(*[self.item(k) for k in range(3)])
        self.vivos = [ics]
        for k, it in enumerate(ics):
            it.move_to(P3(-4.3 + 4.3 * k, -1.3))
        self.play(FadeOut(logo), FadeOut(aneis), FadeOut(bv), run_time=0.35)
        self.play(FadeIn(tt, shift=0.1 * UP), FadeIn(tt2, shift=0.1 * UP), FadeIn(nv), FadeIn(ics), run_time=0.8)
        ul = VGroup()
        for k, frase in enumerate(("primeiro de onde ele aparece", "depois de que ele depende", "dois atalhos poderosos")):
            self.gat(frase)
            ul.add(Line(ics[k].get_corner(DL) + 0.16 * DOWN, ics[k].get_corner(DR) + 0.16 * DOWN).set_stroke(CYAN, 3.5))
            self.play(Create(ul[-1]), self.ind_copia(ics[k][0], WHITE_, 1.08, 0.6), run_time=0.6)
            ic_ = ics[k][0]                                                  # v6 §5 agenda animada: cada ícone mostra o que a fala promete
            if k == 0:
                self.play(Rotate(ic_[0], angle=2 * PI, about_point=ic_[0].get_center(), rate_func=linear), run_time=2.4)
            else:
                self.play(ic_[1].animate(rate_func=there_and_back).move_to(ic_[2].get_center()), run_time=2.4)
            self.foco = ics[k][0]
        ic0, ic1, ic2 = ics[0][0], ics[1][0], ics[2][0]
        self.play(Rotate(ic0[0], angle=2 * PI, about_point=ic0[0].get_center(), rate_func=linear),
                  ic1[1].animate(rate_func=there_and_back).move_to(ic1[2].get_center()),
                  ic2[1].animate(rate_func=there_and_back).move_to(ic2[2].get_center()), run_time=2.6)       # v9: os três ícones juntos (a agenda não fica parada antes dos exercícios)
        self.gat("três exercícios")
        self.play(*[self.ind_copia(i[1], WHITE_, 1.06, 0.7) for i in ics], run_time=0.7)
        self.ate(0.99)
        # ── A3: uma partícula → a multidão → o disco ──
        self.an("A3")
        self.play(FadeOut(VGroup(tt, tt2, nv, ics, ul)), run_time=0.35)
        t0 = self.clk.get_value()
        n_on = ValueTracker(0.0)                          # 0: uma partícula · 1: a multidão inteira
        dsk = ValueTracker(0.0)                           # 0 → 1: os círculos viram o disco em pedaços
        self.add(n_on, dsk)
        RAIOS = [0.55, 0.95, 1.35, 1.75, 2.15]
        R1 = 1.75

        def cena():
            fi = W_A3 * (self.clk.get_value() - t0)
            g = VGroup()
            k_on = n_on.get_value()
            d_ = dsk.get_value()
            if d_ > 0.01:
                dp = DiscoPedacos(C_A3, 2.35, nr=4, nt=10)
                dp.rotate(fi, about_point=C_A3)
                escala_op(dp, d_)
                g.add(dp)
            for j, r in enumerate(RAIOS):
                prim = (r == R1)
                o = 1.0 if prim else min(1.0, max(0.0, k_on * len(RAIOS) - j))
                if o < 0.02:
                    continue
                o *= (1 - 0.65 * d_)
                g.add(Circle(radius=r).move_to(C_A3).set_stroke(GEO, 1.6, opacity=0.45 * o))
                for q in range(1 if prim and k_on < 0.05 else 6):
                    a = fi + 2 * PI * q / 6 + 0.4 * j
                    p = C_A3 + r * np.array([math.cos(a), math.sin(a), 0])
                    tg = np.array([-math.sin(a), math.cos(a), 0])
                    g.add(Dot(p, radius=0.09, color=MAS).set_opacity(o).set_z_index(9))
                    g.add(seta(p, p + tg * 0.55 * r, VEL, 5, tip=0.16, op=o))
            if d_ < 0.02 and k_on < 0.6:
                a = fi + 0.4 * RAIOS.index(R1)
                p = C_A3 + R1 * np.array([math.cos(a), math.sin(a), 0])
                o1 = 1 - min(1.0, k_on / 0.6)
                g.add(Line(C_A3, p).set_stroke(GEO, 3, opacity=o1).set_z_index(7))
                lr_ = mtex("r", GEO, 42).move_to(C_A3 + 0.5 * R1 * np.array([math.cos(a), math.sin(a), 0]) + 0.3 * np.array([-math.sin(a), math.cos(a), 0]))
                lk_ = mtex(r"\tfrac{1}{2}mv^2", KC, 42).move_to(C_A3 + (R1 + 0.75) * np.array([math.cos(a - 0.35), math.sin(a - 0.35), 0]))
                g.add(lr_.set_opacity(o1), lk_.set_opacity(o1))
            g.add(eixo_cruz(C_A3, 0.18))
            return g
        cv = vivo(cena)
        self.play(FadeIn(cv), run_time=0.6)
        self.reg("a3", w=W_A3, graus_por_quadro=math.degrees(W_A3 / FPS))
        A, ia = M("v", "=", r"\omega", "r", size=52)
        self.pilha.poe(A)
        self.gat("um ponto de um corpo que gira")
        self.play(FadeIn(A), run_time=0.7)
        B, ib = M("K", "=", r"\tfrac{1}{2}", "m", "v^2", size=52)
        self.pilha.poe(B)
        self.gat("uma partícula com velocidade v")
        self.play(FadeIn(B), run_time=0.7)
        self.gat("junta as duas ideias")
        self.play(n_on.animate.set_value(1.0), run_time=2.4)
        self.gat("qual é a energia de toda essa multidão")
        C, ic = M("K", "=", r"\,?", size=56)
        lc = linha_m(C, txt("DO CORPO TODO", 28, bold=True), buff=0.25)
        self.pilha.poe(lc)
        self.play(dsk.animate.set_value(1.0), FadeIn(lc), run_time=1.6)
        self.foco = lc
        self.ate(0.99)

    def icone(self, k):
        if k == 0:
            d = DiscoPedacos(ORIGIN, 0.72, nr=3, nt=8)
            s = seta(P3(0.0, 0.0), P3(0.0, 0.0), VEL)
            return VGroup(d, eixo_cruz(ORIGIN, 0.1))
        if k == 1:
            h = haltere(P3(-0.75, 0), P3(0.75, 0), 0.22)
            e1 = eixo_cruz(P3(0, 0), 0.12)
            e2 = escala_op(eixo_cruz(P3(-0.75, 0), 0.12), 0.45)
            arr = Arrow(P3(-0.1, -0.45), P3(-0.7, -0.45), buff=0, stroke_width=3, tip_length=0.14).set_color(GEO)
            return VGroup(h, e1, e2, arr)
        b = barra_fatias(-0.9, 0, 1.8, 0.24, 10, brilho=False)
        return VGroup(b, eixo_cruz(P3(0, 0), 0.12), eixo_cruz(P3(-0.9, 0), 0.12), cm_pt(P3(0, 0.36), 0.06))

    ROT = (("ENERGIA", "DE UM GIRO"), ("MOMENTO", "DE INÉRCIA"), ("EIXOS", "PARALELOS"))

    def item(self, k):
        ic = self.icone(k)
        ic.scale(min(1.9 / ic.width, 1.45 / ic.height))
        t = VGroup(*[txt(l, 26) for l in self.ROT[k]]).arrange(DOWN, buff=0.18)
        return VGroup(ic, t).arrange(DOWN, buff=0.35)
