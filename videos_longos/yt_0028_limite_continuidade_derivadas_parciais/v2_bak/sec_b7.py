"""Lote PB7 · QUATRO NÚMEROS, QUATRO MEDIDAS (v2; alvos 25–30). B7-1: a matriz de movimentos (cada número é um movimento de aresta; a aresta
se move UMA vez na direção da seta e volta). B7-2: as combinações (rot = soma dos giros, div = soma dos estiramentos, def₁ e def₂; a tesoura).
B7-3: os três cartões e os valores (da v1). B7-4: volta ao gancho, com as setas das quinas (1, 0) e (0, −1) por 2 s. B7-5: o desafio (y, x),
com as setas das quinas (0, 1) e (1, 0) por 2 s; TAMBÉM VALE a 36 px por ≥ 4 s."""
from v28 import *  # noqa: F401,F403
from sec_h import palco_sela

V = Vista(600, 540, 120)
Q12 = quad_pts((0, 0), 1.2)
CART = [(140, "GIRA", VEL, F_GIRO, fl_rot(.6)), (720, "MUDA DE ÁREA", SAI, F_EXPL, fl_escala(1.42, 1.42)), (1300, "DEFORMA", LIMA, F_SELA, fl_escala(1.5, 1 / 1.5))]
# células da matriz de movimentos: (cx, cy, ponta da aresta, ponta da seta, fórmula, legenda, cor, aresta 'h' ou 'v')
CEL = [(500, 380, (1, 0), (1.45, 0), r"\dfrac{\partial\Pp}{\dx}=\Am{1}", "ESTICA A HORIZONTAL", E1, "h"),
       (500, 720, (1, 0), (1, .9), r"\dfrac{\partial\Qq}{\dx}=\Am{2}", "GIRA A HORIZONTAL", E1, "h"),
       (940, 380, (0, 1), (-.45, 1), r"\dfrac{\partial\Pp}{\dy}=\Mg{-1}", "TOMBA A VERTICAL", E2, "v"),
       (940, 720, (0, 1), None, r"\dfrac{\partial\Qq}{\dy}=\Mg{0}", "ESTICA A VERTICAL", E2, "v")]


def cartao(i):
    X0, tit, cor, Fv, fl = CART[i]
    v = Vista(X0 + 240, 480, 56)
    p = painel(X0, 250, 480, 460)
    cmp = campo28(v, Fv, -3.5, 3.5, -3.5, 3.5, .85, rmin=1.2, rmax=3.9, mmax=3.4, nome=f"B7 cartão {tit}")
    return v, p, cmp, Pedaco(v, Q12), fantasma(v, Q12), T(tit, X0 + 240, 760, 34, "center", cor), fl


def parenteses():
    g = VGroup()
    for (x0, xc) in ((350, 300), (1090, 1140)):
        m = VMobject().set_points_as_corners([PX(x0 + (xc - x0) * 2 * t * (1 - t) * 2 / 2, 270 + 640 * t) for t in np.linspace(0, 1, 60)])
        m.set_stroke(WHITE_, 4 / 1.2).set_fill(opacity=0)
        m._sem_contorno = True
        g.add(m)
    return g.set_z_index(10)


class LoteB7(Base):
    ANTES = "A TABELA"

    def corpo(self):
        # ── B7-1 · a matriz de movimentos (alvo 25) ──
        self.an("B7-1")
        self.secao("QUATRO NÚMEROS, QUATRO MEDIDAS")
        par = parenteses()
        jn = TC(r"J=\begin{pmatrix}\Am{1} & \Mg{-1}\\ \Am{2} & \Mg{0}\end{pmatrix}", 1250, 420, 52)
        self.gat("lendo cada número da tabela")
        self.play(Create(par), caneta(jn, ritmo=0.4))
        frases = [("em cima à esquerda", "aqui um"), ("embaixo à esquerda", "dois"), ("em cima à direita", "menos um para a esquerda"), ("embaixo à direita", "zero")]
        for (cx, cy, a, b, f, l, c, ar), (g1, g2) in zip(CEL, frases):
            v = Vista(cx - 60, cy + 50, 130)
            tr = vlinha(v, [(1, 0), (1, 1), (0, 1)], GEO, 2, dash=(6, 7)).set_z_index(5)
            eh = vlinha(v, [(0, 0), (1, 0)], E1, 5).set_z_index(6)
            ev = vlinha(v, [(0, 0), (0, 1)], E2, 5).set_z_index(6)
            p0 = ponto7(v.c2p(0, 0), POS, 6, 8)
            self.gat(g1)
            self.play(Create(tr), Create(eh), Create(ev), FadeIn(p0), run_time=0.6)
            if b is not None:
                s_ = seta7(v.c2p(*a), v.c2p(*b), c, 7, 20).set_z_index(9)
                self.play(GrowArrow(s_), run_time=0.5)
                ed = eh if ar == "h" else ev
                A, B = np.array(a, float), np.array(b, float)

                def mexe(m, al, A=A, B=B, v=v, ar=ar):
                    tip = A + (B - A) * al
                    m.set_points_as_corners([v.c2p(0, 0), v.c2p(*tip)])
                self.play(UpdateFromAlphaFunc(ed, mexe, rate_func=there_and_back), run_time=1.6)    # vai UMA vez e volta (0,8 s + 0,8 s)
            else:
                pa = legenda("PARADA", *canto_xy(v, .5, .45), GEO, "center", 26)
                self.play(FadeIn(pa), run_time=0.4)
            fx = TC(f, cx, cy + 112, 30, "c")
            lx = legenda(l, cx, cy + 172, c, "center", 26)
            self.gat(g2)
            self.play(caneta(fx, ritmo=0.35), FadeIn(lx, shift=0.05 * UP))
        lgs = [legenda("1ª COLUNA: MEXE A ARESTA HORIZONTAL", 1254, 560, E1), legenda("2ª COLUNA: MEXE A ARESTA VERTICAL", 1254, 610, E2),
               legenda("LINHA DE CIMA: EMPURRA PARA O LADO", 1254, 700, GEO), legenda("LINHA DE BAIXO: EMPURRA PARA CIMA", 1254, 750, GEO)]
        self.play(LaggedStart(*[FadeIn(m, shift=0.05 * UP) for m in lgs], lag_ratio=0.3), run_time=1.2)
        self.ate(0.97)

        # ── B7-2 · as combinações; a tesoura (alvo 26) ──
        self.an("B7-2")
        vq = Vista(330, 720, 190)
        Sq, k_ = 1.6, .35 * 1.6
        sai = self.snap()
        tr = vlinha(vq, [(Sq, 0), (Sq, Sq), (0, Sq)], GEO, 2, dash=(7, 8)).set_z_index(5)
        eh = vlinha(vq, [(0, 0), (Sq, 0)], E1, 6).set_z_index(6)
        ev = vlinha(vq, [(0, 0), (0, Sq)], E2, 6).set_z_index(6)
        p0 = ponto7(vq.c2p(0, 0), POS, 9, 8)
        sa = seta7(vq.c2p(Sq, 0), vq.c2p(Sq + k_, 2 * k_), E1, 8, 24).set_z_index(9)
        sb = seta7(vq.c2p(0, Sq), vq.c2p(-k_, Sq), E2, 8, 24).set_z_index(9)
        la = TP(r"(\Am1,\Am2)", *canto_xy(vq, Sq + .85, .75), 30)
        lb = TP(r"(\Mg{-1},\Mg0)", *canto_xy(vq, -.05, Sq + .38), 30)
        hv = legenda("H = ARESTA HORIZONTAL · V = ARESTA VERTICAL", 944, 860, GEO, "left", 26)
        self.gat("agora junta")
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        self.play(Create(tr), Create(eh), Create(ev), FadeIn(p0), GrowArrow(sa), GrowArrow(sb), FadeIn(la), FadeIn(lb), FadeIn(hv), run_time=0.9)
        linhas = [(r"\V{\rot}=\text{giro}_{\Am{\text{H}}}+\text{giro}_{\Mg{\text{V}}}=\Am{2}+\Mg{1}=\V{3}", 290, "dão o rotacional"),
                  (r"\D{\dv}=\text{estica}_{\Am{\text{H}}}+\text{estica}_{\Mg{\text{V}}}=\Am{1}+\Mg{0}=\D{1}", 430, "dão o divergente"),
                  (r"\Lm{\text{def}_1}=\text{estica}_{\Am{\text{H}}}-\text{estica}_{\Mg{\text{V}}}=\Am{1}-\Mg{0}=\Lm{1}", 570, "essa é a primeira deformação"),
                  (r"\Lm{\text{def}_2}=\text{giro}_{\Am{\text{H}}}-\text{giro}_{\Mg{\text{V}}}=\Am{2}-\Mg{1}=\Lm{1}", 710, "essa é a segunda")]
        for s_, y, g in linhas:
            m = TC(s_, 940, y, 38)
            self.gat(g)
            self.play(caneta(m, ritmo=0.3))
        tes = leg_mix([r"$\text{def}_2$", ": QUANTO O ÂNGULO RETO FECHA, COMO UMA TESOURA"], 944, 800, LIMA, "left", 26, up=True, gap=4)

        def tesoura(m, al):
            th = 0.15 * al
            eh.set_points_as_corners([vq.c2p(0, 0), vq.c2p(Sq * math.cos(th), Sq * math.sin(th))])
            ev.set_points_as_corners([vq.c2p(0, 0), vq.c2p(Sq * math.sin(th), Sq * math.cos(th))])
        self.gat("como uma tesoura")
        self.play(UpdateFromAlphaFunc(eh, tesoura, rate_func=there_and_back), FadeIn(tes, shift=0.05 * UP), run_time=1.6)
        self.ate(0.97)

        # ── B7-3 · os três cartões e os valores (alvos 27 e 28) ──
        self.an("B7-3")
        sai = self.snap()
        fr = [TC(r"\V{\rot}:\ \dfrac{\partial \Qq}{\dx}-\dfrac{\partial \Pp}{\dy}", 380, 845, 36, "c"),
              TC(r"\D{\dv}:\ \dfrac{\partial \Pp}{\dx}+\dfrac{\partial \Qq}{\dy}", 960, 845, 36, "c")]
        d1, d2 = linha_partes([r"\dfrac{\partial \Pp}{\dx}-\dfrac{\partial \Qq}{\dy}", r"\Lm{\text{e}}\ \ \dfrac{\partial \Qq}{\dx}+\dfrac{\partial \Pp}{\dy}"], 1540, 845, 34, gap=22)
        cards = [cartao(i) for i in range(3)]
        for v, p, cmp, ped, fan, t, fl in cards:
            clareira(cmp, (lambda ped=ped: clarPoly(ped.poly(), .25)))
        self.gat("quatro números entram")
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        self.play(*[a for v, p, cmp, ped, fan, t, fl in cards for a in (Create(p), cresce_campo(cmp, 0.8), FadeIn(ped), FadeIn(fan), FadeIn(t, shift=0.06 * UP))], run_time=0.9)
        self.play(*[anda(ped, fl, 1.0, 2.0, nome=f"B7 {CART[i][1]}") for i, (v, p, cmp, ped, fan, t, fl) in enumerate(cards)])
        for i, c in enumerate(cards):
            print(f"[B7] {CART[i][1]}: área 1,44 → {c[3].area():.4f}")
        self.play(caneta(fr[0], ritmo=0.25), caneta(fr[1], ritmo=0.25), caneta(d1, ritmo=0.25), caneta(d2, ritmo=0.25))
        vals = [TC(r"=2-(-1)=\V{3}", 380, 940, 38, "c"), TC(r"=1+0=\D{1}", 960, 940, 38, "c"), TC(r"=1-0=\Lm{1}\quad =2+(-1)=\Lm{1}", 1540, 940, 36, "c")]
        q4 = T("4 NÚMEROS ENTRAM, 4 MEDIDAS SAEM", 960, 205, 36, "center", BR)
        self.gat("quatro medidas saem")
        self.play(FadeIn(q4, shift=0.06 * DOWN), *[caneta(m, ritmo=0.25) for m in vals])
        # o próximo passo entra mais cedo: a fala continua sobre a física, e a cena dos cartões acabou
        self.gat("e isso não é só matemática")
        for _, _, c, _, _, _, _ in cards:
            c.clear_updaters()
        s0 = self.snap()
        gch = palco_sela(nome="B7-4 gancho (x, −y)")
        pg = Pedaco(V, Q12).em(fl_sela, .55)
        fg = fantasma(V, Q12)
        ag = TP(r"\text{ÁREA } 1{,}44 \to 1{,}44", *canto_xy(V, 0, -1), 34, "c")
        st = {"extra": NADA}
        clareira(gch, lambda: ou(clarPoly(pg.poly(), .25), clarPoly(Q12, .15), clar28([(-1.1, -1.25, 1.1, -.75)]), st["extra"]))
        self.play(*[FadeOut(m) for m in s0], run_time=0.5)
        self.remove(*s0)
        self.play(cresce_campo(gch, 0.9), FadeIn(pg), FadeIn(fg), FadeIn(ag), run_time=0.9)
        self.ate(0.97)

        # ── B7-4 · volta ao gancho (alvo 29) ──
        self.an("B7-4")
        j1 = TC(r"J = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}", 1120, 360, 52)
        self.gat("a tabela é um e zero")
        self.play(caneta(j1, ritmo=0.4))
        qa, qb = np.array([.6, -.6]), np.array([-.6, .6])
        c1 = seta7(V.c2p(*qa), V.c2p(*(qa + [.5, 0])), E1, 8, 26).set_z_index(12)
        c2 = seta7(V.c2p(*qb), V.c2p(*(qb + [0, -.5])), E2, 8, 26).set_z_index(12)
        self.gat("a aresta horizontal estica")
        st["extra"] = clar28([(.55, -.75, 1.15, -.45), (-.75, .05, -.45, .65)])
        self.play(GrowArrow(c1), GrowArrow(c2), run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(c1), FadeOut(c2), run_time=0.4)
        self.remove(c1, c2)
        st["extra"] = NADA
        rd = TC(r"\rot = \V{0}\qquad \dv = \D{0}", 1120, 520, 48)
        self.gat("rotacional zero")
        self.play(caneta(rd, ritmo=0.4))
        dfm = T("DEFORMAÇÃO: 2 e 0", 1120, 650, 44, cor=LIMA, up=False)
        self.gat("a primeira deformação vale dois")
        self.play(FadeIn(dfm, shift=0.06 * UP), run_time=0.5)
        l1 = legenda("É TUDO DEFORMAÇÃO", 1124, 730, GEO)
        l2 = legenda("ESTICA NO x · ACHATA NO y", 1124, 780, GEO, up=False)
        self.gat("é tudo deformação")
        self.play(FadeIn(l1, shift=0.06 * UP), run_time=0.5)
        self.play(FadeIn(l2, shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)

        # ── B7-5 · o desafio: (y, x) (alvo 30) ──
        self.an("B7-5")
        self.secao("O DESAFIO")
        col = [j1, rd, dfm, l1, l2]
        self.play(*[FadeOut(m) for m in col], FadeOut(ag), FadeOut(pg), run_time=0.5)
        self.remove(*col, ag, pg)
        gch.clear_updaters()
        p2 = Pedaco(V, Q12)
        st["extra"] = NADA
        clareira(gch, lambda: ou(clarPoly(p2.poly(), .25), clarPoly(Q12, .15), st["extra"]))
        tr = mesma_grade(gch, F_TROCA, 3)
        fF = TC(r"\F = (\Y,\ \X)", 1120, 300, 48)
        self.gat("um deles é este")
        self.play(Transform(gch, tr), FadeIn(p2), run_time=1.2)
        herda(gch, tr)
        self.play(caneta(fF, ritmo=0.5))
        j2 = TC(r"J = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}", 1120, 440, 48)
        rd2 = TC(r"\rot = \V{0}\qquad \dv = \D{0}", 1120, 580, 44)
        self.gat("que troca as coordenadas")
        self.play(caneta(j2, ritmo=0.35))
        self.play(caneta(rd2, ritmo=0.3))
        c1 = seta7(V.c2p(*qa), V.c2p(*(qa + [0, .5])), E1, 8, 26).set_z_index(12)
        c2 = seta7(V.c2p(*qb), V.c2p(*(qb + [.5, 0])), E2, 8, 26).set_z_index(12)
        self.gat("as duas arestas giram uma contra a outra")
        st["extra"] = clar28([(.45, -.65, .75, -.05), (-.65, .45, -.05, .75)])
        self.play(GrowArrow(c1), GrowArrow(c2), run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(c1), FadeOut(c2), run_time=0.4)
        self.remove(c1, c2)
        st["extra"] = NADA
        d02 = T("DEFORMAÇÃO: 0 e 2", 1120, 700, 44, cor=LIMA, up=False)
        self.gat("a segunda deformação vale dois")
        self.play(FadeIn(d02, shift=0.06 * UP), run_time=0.5)
        self.gat("e o quadradinho vira losango")
        self.add(fantasma(V, Q12))
        self.play(anda(p2, fl_troca, .55, 2.5, nome="B7-5 (y, x)"))
        print(f"[B7] (y, x): área 1,44 → {p2.area():.4f}")
        g45 = legenda("O MESMO, GIRADO DE 45°", 1124, 770, GEO)
        self.gat("é o mesmo campo de antes")
        self.play(FadeIn(g45, shift=0.06 * UP), run_time=0.5)
        tv = TP(r"\text{TAMBÉM VALE: } (\X^2-\Y^2,\ -2\X\Y)", 1120, 880, 36, "l")
        self.gat("quem achou um de segundo grau")
        self.play(FadeIn(tv), run_time=0.5)
        self.wait(4.0)
        self.ate(0.97)
        gch.clear_updaters()
        self.sai_fim()
