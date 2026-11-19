"""Lote PT6: T6 — UM ATALHO PARA PLACAS. Placa fina em vista oblíqua (plano xy, eixo z saindo dela); o pedaço em (x, y) com o triângulo
retângulo x, y, r (r = distância ao eixo z) → I_z = Σmx² + Σmy² = I_y + I_x. T6-3 disco no diâmetro: I_x = I_y ⇒ ¼MR² (e o aro: ½MR²), sem integral.
T6-4 Three.js 'esfera' inteira com os três eixos: I_x + I_y + I_z = 2∫r²dm ⇒ I = ⅔∫r²dm; casca ⅔MR²; maciça ⅔·⅗ = ⅖MR²."""
from pecas21 import *  # noqa: F401,F403

O6 = P3(-4.6, -1.55)
EX, EY, EZ = np.array([1.0, 0, 0]), np.array([0.62, 0.40, 0]), np.array([0, 1.0, 0])


def ob(x, y, z=0.0, o=O6):
    return o + x * EX + y * EY + z * EZ


def eixos_ob(o=O6, ax=(-1.4, 3.2), ay=(-1.6, 3.4), az=(0, 3.4), w=3):
    g = VGroup(Arrow(ob(ax[0], 0, 0, o), ob(ax[1], 0, 0, o), buff=0, stroke_width=w, tip_length=0.16).set_color(GEO),
               Arrow(ob(0, ay[0], 0, o), ob(0, ay[1], 0, o), buff=0, stroke_width=w, tip_length=0.16).set_color(GEO),
               Arrow(ob(0, 0, az[0], o), ob(0, 0, az[1], o), buff=0, stroke_width=w, tip_length=0.16).set_color(GEO))
    lab = VGroup(T("x", 42).next_to(g[0].get_end(), DR, buff=0.3), T("y", 42).next_to(g[1].get_end(), UR, buff=0.3),
                 T("z", 42).next_to(g[2].get_end(), LEFT, buff=0.3))
    return g.set_z_index(12), lab


class LoteT6(Lote21):
    def corpo(self):
        self.an("T6-1")
        self.secao("UM ATALHO PARA PLACAS")
        self.guia(['PERGUNTA:', 'HÁ UM ATALHO PARA', 'PLACAS FINAS?'])                                      # v6 G4: a coluna da direita não fica vazia
        cs = [ob(-1.2, -1.3), ob(2.6, -1.3), ob(2.6, 2.7), ob(-1.2, 2.7)]
        placa = Polygon(*cs)
        aco(placa, 2.0)
        placa.set_z_index(4)
        ax, labs = eixos_ob()
        self.play(FadeIn(placa), run_time=0.6)
        self.selo("SÓ PARA PLACAS FINAS", ["PLANAS"])
        self.gat("coloca a placa no plano x y")
        self.play(GrowArrow(ax[0]), GrowArrow(ax[1]), FadeIn(labs[0]), FadeIn(labs[1]), run_time=0.8)
        self.gat("e o eixo z saindo perpendicular")
        self.play(GrowArrow(ax[2]), FadeIn(labs[2]), run_time=0.6)
        X, Y = 1.9, 1.6
        pc = ob(X, Y)
        ped = Polygon(ob(X - 0.15, Y - 0.15), ob(X + 0.15, Y - 0.15), ob(X + 0.15, Y + 0.15), ob(X - 0.15, Y + 0.15)).set_fill(MAS, 0.95).set_stroke(WHITE_, 2).set_z_index(14)
        lmp = T("m", 42).next_to(ped, UR, buff=0.3)
        tri_x = Line(ob(0, 0), ob(X, 0)).set_stroke(GEO, 4).set_z_index(13)
        tri_y = Line(ob(X, 0), pc).set_stroke(GEO, 4).set_z_index(13)
        tri_r = DashedLine(ob(0, 0), pc, dash_length=0.09).set_stroke(WHITE_, 3.5).set_z_index(13)
        lx = T("x", 40).next_to(ob(X * 0.62, 0), DOWN, buff=0.3)
        ly = T("y", 40).next_to(ob(X, Y * 0.5), RIGHT, buff=0.3)
        lr = T("r", 42).next_to(ob(X * 0.45, Y * 0.45), UL, buff=0.3)
        self.vivos = [placa]
        self.play(Indicate(placa, scale_factor=1.05, color=WHITE_), run_time=1.3)                  # v6 parado 12:52
        self.play(Indicate(placa, scale_factor=1.05, color=WHITE_), run_time=1.3)
        self.gat("a distância de um pedaço ao eixo z")
        self.play(FadeIn(ped), FadeIn(lmp), Create(tri_r), FadeIn(lr), run_time=0.8)
        self.gat("por pitágoras")
        self.play(Create(tri_x), Create(tri_y), FadeIn(lx), FadeIn(ly), run_time=0.8)
        A, ia = M("r^2", "=", "x^2", "+", "y^2", size=52)
        self.pilha.poe(A)
        self.monta(A, ia, {0: lr, 2: lx, 4: ly})
        for _ in range(2):
            self.play(Indicate(placa, scale_factor=1.05, color=WHITE_), run_time=1.3)      # v6 parado 12:52
        B, ib = M(r"I_z", "=", r"\sum", "m", "r^2", size=50)
        B2, ib2 = M("=", r"\sum", "m", "x^2", "+", r"\sum", "m", "y^2", size=50)
        self.pilha.poe(B)
        self.pilha.poe(B2)
        self.gat("e a soma de m r ao quadrado se divide em duas")
        self.monta(B, ib, {}, rt=0.7)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.passo(A, B2, (J(ia, 2), J(ib2, 3)), (J(ia, 3), J(ib2, 4)), (J(ia, 4), J(ib2, 7)), rt=1.2, origem=False)
        self.foco = B
        self.ate(0.99)
        # ── T6-2 ──
        self.an("T6-2")
        self.gat("a soma de m vezes y ao quadrado")
        self.play(self.ind(B2, ib2, [5, 6, 7], MAS, 1.12, 0.9), self.ind_copia(ax[0], WHITE_, 1.06, 0.9), self.ind_copia(tri_y, MAS, 1.1, 0.9), run_time=0.9)
        nota = linha_m(T(r"y", 40), txt("= DISTÂNCIA AO EIXO x", 26), buff=0.15)
        self.pilha.poe(nota, dx=0.4)
        self.play(FadeIn(nota), run_time=0.6)
        self.gat("o mesmo para m x ao quadrado")
        self.play(self.ind(B2, ib2, [1, 2, 3], MAS, 1.12, 0.9), self.ind_copia(ax[1], WHITE_, 1.06, 0.9), self.ind_copia(tri_x, MAS, 1.1, 0.9), run_time=0.9)
        C_, ic = M(r"I_z", "=", r"I_x", "+", r"I_y", size=60)
        Cb = caixa_l(C_, MAS)
        self.pilha.poe(Cb)
        self.gat("então o momento de inércia em torno do eixo perpendicular")
        self.cx(Cb[0])
        self.passo(B2, C_, (J(ib2, 0), J(ic, 1)), (J(ib2, 5, 6, 7), J(ic, 2)), (J(ib2, 4), J(ic, 3)), (J(ib2, 1, 2, 3), J(ic, 4)), rt=1.4, origem=False)
        lz0 = T(r"z=0", 42).next_to(ob(-1.0, 2.5), UP, buff=0.1)
        self.gat("onde todo ponto tem z igual a zero")
        self.play(FadeIn(lz0), run_time=0.5)
        self.foco = Cb
        self.ate(0.99)
        # ── T6-3: disco e aro pelo diâmetro ──
        self.an("T6-3")
        self.sem_selo()
        self.pilha.so(Cb)
        OD = P3(-4.4, -0.7)
        RD = 1.75
        disco = Ellipse(width=2 * RD * 1.0, height=2 * RD * 0.42).move_to(OD)
        aco(disco, 2.0)
        disco.set_z_index(4)
        dsh = Ellipse(width=2 * RD, height=2 * RD * 0.42).move_to(OD).set_stroke(width=0).set_fill(MAS, 0.35).set_z_index(5)
        exd = VGroup(Arrow(OD + 2.4 * LEFT, OD + 2.5 * RIGHT, buff=0, stroke_width=3, tip_length=0.16).set_color(GEO),
                     Arrow(OD - 1.35 * np.array([0.95, 0.55, 0]), OD + 1.5 * np.array([0.95, 0.55, 0]), buff=0, stroke_width=3, tip_length=0.16).set_color(GEO),
                     Arrow(OD, OD + 2.8 * UP, buff=0, stroke_width=3, tip_length=0.16).set_color(GEO)).set_z_index(12)
        lxd = VGroup(T("x", 40).next_to(exd[0].get_end(), DOWN, buff=0.08), T("y", 40).next_to(exd[1].get_end(), UR, buff=0.04),
                     T("z", 40).next_to(exd[2].get_end(), LEFT, buff=0.1))
        lRd = T("R", 42).move_to(OD + P3(-RD * 0.94 - 0.3, 0.55))
        self.troca([placa, ax, labs, ped, lmp, tri_x, tri_y, tri_r, lx, ly, lr, lz0], FadeIn(disco), FadeIn(dsh), FadeIn(exd), FadeIn(lxd), FadeIn(lRd), seq=True)
        D1, id1 = M(r"I_x", "=", r"I_y", size=50)
        D1l = linha_m(D1, txt("POR SIMETRIA", 26), buff=0.25)
        self.pilha.poe(D1l)
        self.gat("os eixos x e y no diâmetro são equivalentes")
        self.play(FadeIn(D1l), run_time=0.7)
        D2, id2 = M("2", r"I_x", "=", r"\tfrac{1}{2}", "M", "R^2", size=50)
        self.pilha.poe(D2)
        self.gat("e a soma deles é o do eixo perpendicular")
        self.monta(D2, id2, {}, rt=0.8)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        D3, id3 = M(r"I_{di\hat{a}metro}", "=", r"\tfrac{1}{4}", "M", "R^2", size=54)
        D3b = caixa_l(D3, MAS)
        self.pilha.poe(D3b)
        self.gat("cada um vale um quarto")
        self.cx(D3b[0])
        self.passo(D2, D3, (J(id2, 2), J(id3, 1)), (J(id2, 4), J(id3, 3)), (J(id2, 5), J(id3, 4)), rt=1.2, origem=False)
        self.selo("SEM INTEGRAL", "")
        OA = P3(-1.35, 1.25)
        aro = Ellipse(width=1.5, height=0.63).move_to(OA).set_stroke(MAS, 5).set_z_index(6)
        la = txt("ARO", 24).next_to(aro, DOWN, buff=0.3)
        E_, ie = M(r"\mathrm{aro}:\ ", "M", "R^2", r"\ \to\ ", r"\tfrac{1}{2}", "M", "R^2", size=48)
        self.pilha.poe(E_)
        self.gat("e no aro pelo diâmetro")
        self.monta(E_, ie, {}, rt=0.8)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.reg("t6_3", disco_diam=0.25, aro_diam=0.5)
        self.foco = D3b
        self.ate(0.99)
        # ── T6-4: a esfera com os três eixos (Three.js) ──
        self.an("T6-4")
        self.secao("O ATALHO NA ESFERA")
        self.sem_selo()
        self.pilha.limpa(rt=0.3)
        rot_ = ValueTracker(0.0)
        self.add(rot_)
        cam = cam_e(K=1.85, xc=-3.6, yc=-0.5, az=-58.0, el=18.0)
        f3 = Fundo3D(self, "esfera", lambda t: r4({"cut": 0.0, "sep": 0.0, "hi": -1, "rot": rot_.get_value(), "eixos": 1.0, "cam": cam}), op=0.0)
        self.add(f3)
        velhos = [m for m in self.snap() if m not in (rot_, f3)]
        self.troca(velhos, f3.op.animate.set_value(1.0), seq=True)
        lex = VGroup(T("x", 42).next_to(projeta3d(cam, (1.5, 0, 0)), DR, buff=0.06), T("y", 42).next_to(projeta3d(cam, (0, 1.5, 0)), UR, buff=0.06),
                     T("z", 42).next_to(projeta3d(cam, (0, 0, 1.5)), LEFT, buff=0.12))
        self.reg("al_t64", ex=projeta3d(cam, (1.5, 0, 0)), ey=projeta3d(cam, (0, 1.5, 0)), ez=projeta3d(cam, (0, 0, 1.5)), centro=projeta3d(cam, (0, 0, 0)))
        self.play(FadeIn(lex), run_time=0.5)
        F1, if1 = M(r"I_x+I_y+I_z", "=", r"\int", r"\big[(y^2+z^2)", size=46)
        F1b, if1b = M(r"+(x^2+z^2)+(x^2+y^2)\big]", r"\,dm", size=40)
        self.pilha.poe(F1)
        self.pilha.poe(F1b, dx=0.9)
        self.gat("somando os três momentos de inércia")
        self.monta(F1, if1, {}, rt=0.8)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.monta(F1b, if1b, {}, rt=0.8)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.play(rot_.animate.set_value(0.3), run_time=1.0)
        F2, if2 = M(r"I_x+I_y+I_z", "=", "2", r"\int", "r^2", r"\,dm", size=46)
        self.pilha.poe(F2)
        self.gat("duas vezes r ao quadrado")
        self.passo(F1, F2, (J(if1, 0, 1), J(if2, 0, 1)), (J(if1, 2), J(if2, 3)), rt=1.2, origem=False)
        self.play(FadeOut(F1), FadeOut(F1b), run_time=0.4)
        self.remove(F1, F1b)
        self.pilha.tira(F1, F1b)
        self.pilha._reflow(self.pilha.linhas, 0.5)
        F3, if3 = M("I", "=", r"\tfrac{2}{3}", r"\int", "r^2", r"\,dm", size=50)
        self.pilha.poe(F3)
        self.gat("na esfera os três são iguais")
        self.monta(F3, if3, {}, rt=0.8)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.play(rot_.animate.set_value(0.6), run_time=0.8)
        F4, if4 = M(r"\text{casca}:\ ", "r", "=", "R", r"\ \Rightarrow\ ", "I", "=", r"\tfrac{2}{3}", "M", "R^2", size=46)
        self.pilha.poe(F4)
        self.gat("na casca fina")
        self.monta(F4, if4, {}, rt=0.8)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        F5, if5 = M(r"\text{maci\c{c}a}:\ ", "I", "=", r"\tfrac{2}{3}", r"\cdot", r"\tfrac{3}{5}", "M", "R^2", "=", r"\tfrac{2}{5}", "M", "R^2", size=44)
        F5b = caixa_l(F5, MAS)
        self.pilha.poe(F5b)
        self.gat("na maciça a integral dá três quintos")
        self.cx(F5b[0])
        self.monta(F5, if5, {}, rt=0.8)                                  # v9: idem
        self.play(rot_.animate.set_value(0.9), run_time=0.9)
        self.selo("DUAS CONTAS DIFERENTES", ["O MESMO RESULTADO"])
        self.foco = F5b
        dur_ = max(0.5, self.resta() - 0.8)
        self.play(rot_.animate(rate_func=linear).set_value(0.9 + 0.785 * dur_), run_time=dur_)            # v6: ≈ 45°/s (visível) em torno de um eixo oblíquo
        self.ate(0.99)
        self.play(f3.op.animate.set_value(0.0), FadeOut(lex), run_time=0.4)
