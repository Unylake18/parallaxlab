"""Lote PB7 · QUATRO NÚMEROS, QUATRO MEDIDAS (alvos 14–17). B7-1/2 (layout C): GIRA (giro de 0,6 rad), MUDA DE ÁREA (× 1,42), DEFORMA
((x, −y): × 1,5 e ÷ 1,5; em "entre as duas diagonais" o campo troca para (y, x) e o quadradinho vira losango); as fórmulas e, no nosso ponto, os
valores. B7-3 (layout A): o palco do gancho volta com o retângulo final; J = (1 0; 0 −1). B7-4: (y, x), o losango pelo fluxo exato (cosh, senh)
de 0 a 0,55; TAMBÉM VALE: (x² − y², −2xy) por ~3 s. (O B7-5 do handoff foi cortado na v1.2.)"""
from v28 import *  # noqa: F401,F403
from sec_h import palco_sela

V = Vista(600, 540, 120)
Q12 = quad_pts((0, 0), 1.2)
CART = [(140, "GIRA", VEL, F_GIRO, fl_rot(.6)), (720, "MUDA DE ÁREA", SAI, F_EXPL, fl_escala(1.42, 1.42)), (1300, "DEFORMA", LIMA, F_SELA, fl_escala(1.5, 1 / 1.5))]


def cartao(i):
    X0, tit, cor, Fv, fl = CART[i]
    v = Vista(X0 + 240, 480, 56)
    p = painel(X0, 250, 480, 460)
    cmp = campo28(v, Fv, -3.5, 3.5, -3.5, 3.5, .85, rmin=1.2, rmax=3.9, mmax=3.4, nome=f"B7 cartão {tit}")
    ped = Pedaco(v, Q12)
    fan = fantasma(v, Q12)
    t = T(tit, X0 + 240, 760, 34, "center", cor)
    return v, p, cmp, ped, fan, t, fl


class LoteB7(Base):
    ANTES = "A TABELA"

    def corpo(self):
        # ── B7-1 · GIRA e MUDA DE ÁREA ──
        self.an("B7-1")
        self.secao("QUATRO NÚMEROS, QUATRO MEDIDAS")
        fr = [TC(r"\V{\rot}:\ \dfrac{\partial \Qq}{\dx}-\dfrac{\partial \Pp}{\dy}", 380, 845, 36, "c"),
              TC(r"\D{\dv}:\ \dfrac{\partial \Pp}{\dx}+\dfrac{\partial \Qq}{\dy}", 960, 845, 36, "c")]
        d1, d2 = linha_partes([r"\dfrac{\partial \Pp}{\dx}-\dfrac{\partial \Qq}{\dy}", r"\Lm{\text{e}}\ \ \dfrac{\partial \Qq}{\dx}+\dfrac{\partial \Pp}{\dy}"], 1540, 845, 34, gap=22)
        cards = []
        gats = [("o giro vem", "a derivada da componente vertical na horizontal"), ("a mudança de área", "a soma das duas derivadas")]
        for i, (g1, g2) in enumerate(gats):
            v, p, cmp, ped, fan, t, fl = cartao(i)
            clareira(cmp, (lambda ped=ped: clarPoly(ped.poly(), .25)))
            self.gat(g1)
            self.play(Create(p), cresce_campo(cmp, 0.8), FadeIn(ped), FadeIn(fan), FadeIn(t, shift=0.06 * UP), run_time=0.9)
            self.play(anda(ped, fl, 1.0, 2.0, nome=f"B7 {CART[i][1]}"))
            print(f"[B7] {CART[i][1]}: área 1,44 → {ped.area():.4f}")
            self.gat(g2)
            self.play(caneta(fr[i], ritmo=0.6))
            cards.append((v, cmp, ped))
        self.ate(0.97)

        # ── B7-2 · DEFORMA ──
        self.an("B7-2")
        v, p, cmp, ped, fan, t, fl = cartao(2)
        clareira(cmp, lambda: clarPoly(ped.poly(), .25))
        self.gat("as outras duas são a deformação")
        self.play(Create(p), cresce_campo(cmp, 0.8), FadeIn(ped), FadeIn(fan), FadeIn(t, shift=0.06 * UP), run_time=0.9)
        self.play(anda(ped, fl, 1.0, 2.0, nome="B7 DEFORMA (x, −y)"))
        print(f"[B7] DEFORMA: área 1,44 → {ped.area():.4f}")
        self.gat("a primeira é a derivada")
        self.play(caneta(d1, ritmo=0.6))
        self.gat("a segunda é a derivada")
        self.play(caneta(d2, ritmo=0.6))
        nv = mesma_grade(cmp, F_TROCA, 3.4)
        ret = lambda X, Y: fl(X, Y, 1.0)
        los = lambda X, Y: fl_troca(X, Y, .55)
        self.gat("entre as duas diagonais")
        self.play(Transform(cmp, nv), UpdateFromAlphaFunc(ped, lambda m, a: m.forma(lambda X, Y: tuple((1 - smooth(a)) * np.asarray(r) + smooth(a) * np.asarray(l) for r, l in zip(ret(X, Y), los(X, Y))))), run_time=1.8)
        herda(cmp, nv)
        print(f"[B7] DEFORMA → (y, x): losango, área {ped.area():.4f}")
        self.ate(0.97)

        # ── B7-3 · no nosso ponto; o gancho volta ──
        self.an("B7-3")
        vals = [TC(r"=2-(-1)=\V{3}", 380, 940, 38, "c"), TC(r"=1+0=\D{1}", 960, 940, 38, "c"), TC(r"=1-0=\Lm{1}\quad =2+(-1)=\Lm{1}", 1540, 940, 36, "c")]
        for m, g in zip(vals, ("rotacional três", "divergente um", "deformação um e um")):
            self.gat(g)
            self.play(caneta(m, ritmo=0.35))
        q4 = T("4 NÚMEROS ENTRAM, 4 MEDIDAS SAEM", 960, 205, 36, "center", BR)
        self.gat("quatro números entram")
        self.play(FadeIn(q4, shift=0.06 * DOWN), run_time=0.6)
        # o próximo passo entra mais cedo (a fala continua sobre a física; a cena dos cartões acabou)
        self.gat("e isso não é só matemática")
        for c in self.snap():
            c.clear_updaters()
        for _, c, _ in cards:
            c.clear_updaters()
        cmp.clear_updaters()
        s0 = self.snap()
        e = math.exp(.55)
        reta = [(-.6 * e, -.6 / e), (.6 * e, -.6 / e), (.6 * e, .6 / e), (-.6 * e, .6 / e)]
        gch = palco_sela(nome="B7-3 gancho (x, −y)")
        pg = Pedaco(V, Q12).em(fl_sela, .55)
        fg = fantasma(V, Q12)
        ag = TP(r"\text{ÁREA } 1{,}44 \to 1{,}44", *canto_xy(V, 0, -1), 34, "c")
        clareira(gch, lambda: ou(clarPoly(pg.poly(), .25), clarPoly(Q12, .15), clar28([(-1.1, -1.25, 1.1, -.75)])))
        self.play(*[FadeOut(m) for m in s0], run_time=0.5)
        self.remove(*s0)
        self.play(cresce_campo(gch, 0.9), FadeIn(pg), FadeIn(fg), FadeIn(ag), run_time=0.9)
        self.ate(0.97)

        # ── B7-4 · volta ao gancho: a tabela ──
        self.an("B7-4")
        j1 = TC(r"J = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}", 1120, 360, 52)
        self.gat("a tabela é um e zero")
        self.play(caneta(j1, ritmo=0.5))
        rd = TC(r"\rot = \V{0}\qquad \dv = \D{0}", 1120, 520, 48)
        self.gat("rotacional zero")
        self.play(caneta(rd, ritmo=0.5))
        dfm = T("DEFORMAÇÃO: 2 e 0", 1120, 650, 44, cor=LIMA, up=False)
        self.gat("a primeira deformação vale dois")
        self.play(FadeIn(dfm, shift=0.06 * UP), run_time=0.5)
        l1 = legenda("É TUDO DEFORMAÇÃO", 1124, 730, GEO)
        self.gat("é tudo deformação")
        self.play(FadeIn(l1, shift=0.06 * UP), run_time=0.5)
        l2 = legenda("ESTICA NO x · ACHATA NO y", 1124, 780, GEO, up=False)
        self.gat("estica na horizontal")
        self.play(FadeIn(l2, shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)

        # ── B7-5 · o desafio: (y, x) ──
        self.an("B7-5")
        self.secao("O DESAFIO")
        col = [j1, rd, dfm, l1, l2]
        self.play(*[FadeOut(m) for m in col], FadeOut(ag), FadeOut(pg), run_time=0.5)
        self.remove(*col, ag, pg)
        gch.clear_updaters()
        p2 = Pedaco(V, Q12)
        clareira(gch, lambda: ou(clarPoly(p2.poly(), .25), clarPoly(Q12, .15)))
        tr = mesma_grade(gch, F_TROCA, 3)
        fF = TC(r"\F = (\Y,\ \X)", 1120, 300, 48)
        self.gat("um deles é este")
        self.play(Transform(gch, tr), FadeIn(p2), run_time=1.2)
        herda(gch, tr)
        self.play(caneta(fF, ritmo=0.6))
        self.play(anda(p2, fl_troca, .55, 2.5, nome="B7-4 (y, x)"))
        print(f"[B7] (y, x): área 1,44 → {p2.area():.4f}")
        j2 = TC(r"J = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}", 1120, 440, 48)
        rd2 = TC(r"\rot = \V{0}\qquad \dv = \D{0}", 1120, 580, 44)
        self.gat("a tabela dá zero e um")
        self.play(caneta(j2, ritmo=0.5))
        self.play(caneta(rd2, ritmo=0.4))
        d02 = T("DEFORMAÇÃO: 0 e 2", 1120, 700, 44, cor=LIMA, up=False)
        self.gat("agora quem vale dois")
        self.play(FadeIn(d02, shift=0.06 * UP), run_time=0.5)
        g45 = legenda("O MESMO, GIRADO DE 45°", 1124, 770, GEO)
        self.gat("é o mesmo campo de antes")
        self.play(FadeIn(g45, shift=0.06 * UP), run_time=0.5)
        tv = TP(r"\text{TAMBÉM VALE: } (\X^2-\Y^2,\ -2\X\Y)", 1120, 880, 34, "l")
        self.gat("quem achou um de segundo grau")
        self.play(FadeIn(tv), run_time=0.5)
        self.wait(3.0)
        self.play(FadeOut(tv), run_time=0.5)
        self.remove(tv)
        self.ate(0.97)
        gch.clear_updaters()
        self.sai_fim()
