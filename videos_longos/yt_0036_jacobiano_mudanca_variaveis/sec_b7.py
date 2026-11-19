"""yt_0036 · B7 · pause e tente (sem alvo) — v2 (Q15). Layout C760: o plano x, y em vista(140, 560, 150) em cima à esquerda (o trapézio
1 ≤ x + y ≤ 2 no primeiro quadrante, a borda desenhada uma vez só, sobre a aresta), o enunciado no vão, o plano u, v em vista(400, 980, 105)
embaixo à esquerda (a região nova = a mesma do trapézio do B6, selo por 3 s) e a coluna em x = 760. C17 v2 linha a linha (9 degraus);
M10: as linhas derivadas nascem por glyph map (2 → 4, 6 → 7 → 8, o par sen v / sen v acende e some, 9). Papel: VX em cima e na coluna,
VU no canto de baixo (emenda em L: horizontal em y = 705 até x = 700)."""
from j36 import *

VX, VU = Vw(140, 560, 150), Vw(400, 980, 105)
REG = [(1, 0), (2, 0), (0, 2), (0, 1)]
EMX, EMY = 700, 705                     # a emenda em L do papel (px a 1080p)
CX = 760


def area_ret(v, x0, x1, y0, y1):
    return ((x0 - v.cx) / v.u, (x1 - v.cx) / v.u, (v.cy - y1) / v.uy, (v.cy - y0) / v.uy)


def grade_L(vA, vB, xe=EMX, ye=EMY):
    """vA no quadro todo menos o canto de baixo à esquerda (x < xe, y > ye), que é de vB."""
    g = VGroup(papel(vA, area=area_ret(vA, 0, xe, 0, ye)), papel(vA, area=area_ret(vA, xe, 1920, 0, 1080)),
               papel(vB, area=area_ret(vB, 0, xe, ye, 1080)))
    g.set_z_index(-10)
    for x in g.get_family():
        x._sem_foco = True
    g._emenda = f"L (y = {ye} até x = {xe}; x = {xe} abaixo)"
    return g


def lado_a_lado(sc, A, pecas, pares, nota, gap=30):
    """M10: a linha B nasce À DIREITA de A, na mesma altura, por glyph map de uma cópia de A (A fica)."""
    B = Lp(pecas, dir_(A) + gap, centro(A)[1], A._size)
    B._xy = (esq(B), centro(B)[1])
    estava = A in sc.mobjects
    passo(sc, A, B, pares(B) if callable(pares) else pares, copia=True, rt=1.0, nota=nota)
    if estava and A not in sc.mobjects:
        sc.add(A)
    sc.col.registra(B)
    return B


def g_(m, idx):
    return VGroup(*[m[0][i] for i in idx])


class PB7(J36):
    ANTES = "A CONFERÊNCIA"
    CHIP = False

    def corpo(self):
        self.an("B7")
        self.secao("PAUSE E TENTE")
        self.fundo(VX, rt=0)
        d = monta_plano(VX, None, 2.4, 2.3, -.1, -.1, ticks=[("x", 1, r"\Am{1}"), ("x", 2, r"\Am{2}"), ("y", 1, r"\Mg{1}"), ("y", 2, r"\Mg{2}")])
        reg = poligono(VX, REG, RB, 1.0, GEO, 3, z=1)
        entra_plano(self, d, rt=0.6, extra=[FadeIn(reg[0]), Create(reg[1])], caneta=False)
        col = self.col = Coluna36(self, CX, 200)
        col.GAP36 = 24
        E = Lp([("ii", r"\iint_B"), ("f", r"\dfrac{\Ci{\cos}(\X-\Y)}{\Ci{\sen}(\X+\Y)}"), ("d", r"\,\dX\,\dY")], 0, 660, 40)
        E.shift(RIGHT * (320 - (esq(E) + dir_(E)) / 2) / 120)
        nE, _, dE = nd(E, "f")
        self.gat("pausa o vídeo")
        sl = pausa(CX, 262)
        poe_selo(self, sl)
        self.pena(E)
        self.gat("cosseno de xis menos")
        acende(self, (gl(E, "f"), CI), rt=0.8)
        self.gat("no trapézio entre")
        realca(self, reg[1], cor=GEO, rt=0.6, wpx=5)
        self.gat("pronto")
        corta(self, *sl)

        # C17.1 — u e v voam do enunciado
        self.gat("o livro escolhe")
        L1 = Lp([("u", r"\uu="), ("a", r"\X-\Y"), ("s", r",\qquad\vv="), ("b", r"\X+\Y")], CX, 0, 40)
        col.poe(L1)
        yL1 = centro(L1)[1]
        self.escreve_voos(L1, [(g_(E, nE[4:7]), "a", [(620, centro(g_(E, nE[4:7]))[1]), (620, yL1)]),
                               (g_(E, dE[4:7]), "b", [(640, centro(g_(E, dE[4:7]))[1]), (640, yL1)])])     # sobem pelo vão entre o plano e a coluna
        # C17.2 — a inversa: somando e subtraindo (o 2 atravessa a igualdade por mapa)
        self.gat("somando")
        X2 = Lp([("l", r"\uu+\vv"), ("e", "="), ("r", r"2\X")], CX, 0, 40)
        col.poe(X2)
        X2._xy = (CX, centro(X2)[1])
        self.pena(X2)
        self.gat("então xis é u")
        X2b = lado_a_lado(self, X2, [("i", r"\Rightarrow\ "), ("x", r"\X"), ("e", "="), ("f", r"\dfrac{\uu+\vv}{2}")],
                          lambda B: [(X2._ix["l"], nd(B, "f")[0]), (X2._ix["e"], "e"), ([X2._ix["r"][0]], nd(B, "f")[2]), ([X2._ix["r"][1]], "x")],
                          "M10 C17.2 (o 2 atravessa: x = (u + v)/2)")
        self.gat("subtraindo")
        xl = X2._ix["l"]                                                # u + v
        Y2 = deriva(self, X2, [("l", r"\vv-\uu"), ("e", "="), ("r", r"2\Y")],
                    lambda B: [([xl[0]], [B._ix["l"][2]]), ([xl[1]], [B._ix["l"][1]]), ([xl[2]], [B._ix["l"][0]]), ("e", "e"),
                               ([X2._ix["r"][0]], [B._ix["r"][0]]), ([X2._ix["r"][1]], [B._ix["r"][1]])],
                    col, x=CX, rt=0.9, nota="M10 C17.2 (subtraindo: v − u = 2y)")
        self.gat("então ípsilon é vê")
        Y2b = lado_a_lado(self, Y2, [("i", r"\Rightarrow\ "), ("y", r"\Y"), ("e", "="), ("f", r"\dfrac{\vv-\uu}{2}")],
                          lambda B: [(Y2._ix["l"], nd(B, "f")[0]), (Y2._ix["e"], "e"), ([Y2._ix["r"][0]], nd(B, "f")[2]), ([Y2._ix["r"][1]], "y")],
                          "M10 C17.2 (o 2 atravessa: y = (v − u)/2)")
        # C17.3 — as quatro derivadas
        self.gat("o jacobiano")
        D3 = Lp([("a", r"\dd{\X}{\uu}=\dfrac{1}{2}"), ("b", r"\qquad\dd{\X}{\vv}=\dfrac{1}{2}"), ("c", r"\qquad\dd{\Y}{\uu}=-\dfrac{1}{2}"),
                 ("d", r"\qquad\dd{\Y}{\vv}=\dfrac{1}{2}")], CX, 0, 40)
        col.poe(D3)
        self.pena(D3, passo=0.03)
        # C17.4 — J = (1/2)(1/2) − (1/2)(−1/2) (os valores voam das derivadas) → 1/4 + 1/4 (mapa) → +1/2
        self.gat("um meio vezes um meio")
        J2 = Lp([("J", "J"), ("e", "="), ("a", r"\left(\dfrac{1}{2}\right)"), ("c", r"\left(\dfrac{1}{2}\right)"), ("m", "-"),
                 ("b", r"\left(\dfrac{1}{2}\right)"), ("d", r"\left(-\dfrac{1}{2}\right)")], CX, 0, 40)
        col.poe(J2)
        J2._xy = (CX, centro(J2)[1])
        rhs = lambda k_, n: VGroup(*[D3[0][i] for i in D3._ix[k_][-n:]])
        inner = lambda k_: [J2._ix[k_][i] for i in range(1, len(J2._ix[k_]) - 1)]
        self.pena(parte(J2, J2._ix["J"] + J2._ix["e"] + J2._ix["m"] + [J2._ix[k][0] for k in "acbd"] + [J2._ix[k][-1] for k in "acbd"], "J = ( )( ) − ( )( )"))
        voos(self, [(rhs("a", 3).copy(), parte(J2, inner("a"), "xu")), (rhs("d", 3).copy(), parte(J2, inner("c"), "yv")),
                    (rhs("b", 3).copy(), parte(J2, inner("b"), "xv")), (rhs("c", 4).copy(), parte(J2, inner("d"), "yu"))], rt=0.8)
        self.gat("um quarto mais um quarto")
        a_, c_, b_, d_ = J2._ix["a"], J2._ix["c"], J2._ix["b"], J2._ix["d"]

        def mapa4(B):
            q = B._ix["q"]
            return [("e", "e"), ([a_[1], c_[1]], [q[0]]), ([a_[2], c_[2]], [q[1]]), ([a_[3], c_[3]], [q[2]]), (J2._ix["m"] + [d_[1]], [q[3]]),
                    ([b_[1], d_[2]], [q[4]]), ([b_[2], d_[3]], [q[5]]), ([b_[3], d_[4]], [q[6]])]
        J3 = deriva(self, J2, [("e", "="), ("q", r"\dfrac{1}{4}+\dfrac{1}{4}")], mapa4, col, x=eq_x(J2, "e"), nota="M10 C17.4 (produtos → 1/4 + 1/4; − · − = +)")
        self.gat("mais um meio")
        J3 = cresce(self, J3, [("e2", "="), ("r", r"\Lm{+\dfrac{1}{2}}")], voos=lambda B: [(gl(J3, "q").copy(), "r")], col=col, nota="C17.4 (= +1/2)")

        # C17.5 — as bordas (o plano u, v entra; as linhas que já serviram saem; J fica no topo)
        dU = monta_plano(VU, None, 2.4, 2.35, -2.4, -.15, uv=True)
        self.fundo(g=grade_L(VX, VU), rt=0.4)
        entra_plano(self, dU, rt=0.5)
        self.gat("as bordas viram")
        saem = [L1, X2, X2b, Y2, Y2b, D3]
        dy = centro(J2)[1] - (200 + J2.height * 60)
        self.play(*[FadeOut(m) for m in saem], run_time=0.4)  # final K12: troca de página em dois tempos (sai, depois sobe)
        self.play(*[m.animate.shift(UP * dy / 120) for m in (J2, J3)], run_time=0.6)
        self.remove(*saem)
        col.ls = [J2, J3]
        regU = poly_px([VU.px(*p) for p in [(1, 1), (2, 2), (-2, 2), (-1, 1)]], RB, 1.0, z=1)
        B1 = Lp([("a0", r"\X+\Y=1"), ("b0", r"\ \Rightarrow\ \Vc{\vv=1},\qquad"), ("a1", r"\X+\Y=2"), ("b1", r"\ \Rightarrow\ \Vc{\vv=2}")], CX, 0, 40)
        B2 = Lp([("a2", r"\Y=0"), ("b2", r"\ \Rightarrow\ \Co{\vv=\uu},\qquad"), ("a3", r"\X=0"), ("b3", r"\ \Rightarrow\ \Az{\vv=-\uu}")], CX, 0, 40)
        lados = [((1, 0), (0, 1), (1, 1), (-1, 1), CVV, B1, "vê igual a um"), ((2, 0), (0, 2), (2, 2), (-2, 2), CVV, B1, "vê igual a dois"),
                 ((1, 0), (2, 0), (1, 1), (2, 2), CORAL, B2, "vê igual a u e"), ((0, 1), (0, 2), (-1, 1), (-2, 2), AZC, B2, "vê igual a menos u")]
        Buv = Lp([("B", r"B_{uv}:\ "), ("v1", r"\Vc{1}\le\vv\le\Vc{2}"), ("c", r",\qquad"), ("u1", r"\Az{-\vv}"), ("le", r"\le\uu\le"), ("u2", r"\Co{\vv}")], CX, 0, 40)
        col.poe(B1)
        for m_, r_ in ((B2, B1), (Buv, B2)):                            # as três linhas já têm lugar (a Coluna só conta as que estão na tela)
            m_.shift(PX(CX, pxof(r_.get_bottom())[1] + col.GAP36 + m_.height * 60) - PX(esq(m_), centro(m_)[1]))
            col.registra(m_)
        vb_ = Buv._ix["v1"]
        for k, (p0, p1, q0, q1, cor, Bk, gt) in enumerate(lados):
            self.gat(gt)
            lx_ = lin_px([VX.px(*p0), VX.px(*p1)], cor, 5, z=6)              # sobre a aresta (a mesma do polígono)
            self.play(Create(lx_), run_time=0.25)
            self.pena(parte(Bk, Bk._ix[f"a{k}"], f"borda {k + 1}"), parte(Bk, Bk._ix[f"b{k}"], f"v {k + 1}"), lag=0.1, passo=0.03)
            lu_ = lin_px([VU.px(*q0), VU.px(*q1)], cor, 5, z=6)
            if k == 0:
                self.play(FadeIn(regU), run_time=0.3)
            voos(self, [(lx_.copy(), lu_)], rt=0.5, arco=0.4, livre=(E,))
            if k == 1:                                                    # B_uv vai nascendo: a faixa de v com os lados 1 e 2
                self.pena(parte(Buv, Buv._ix["B"] + vb_[1:-1], "B_uv: ≤ v ≤"), passo=0.03)
                voos(self, [(B1[0][B1._ix["b0"][3]].copy(), parte(Buv, [vb_[0]], "1")), (B1[0][B1._ix["b1"][3]].copy(), parte(Buv, [vb_[-1]], "2"))],
                     rt=0.5, seq=False)
        # a região completa: o resto de B_uv e o selo A MESMA REGIÃO DO TRAPÉZIO (≥ 3 s)
        sl_ = selo("A MESMA REGIÃO DO TRAPÉZIO", 660, 842, GEO, 26)
        self.pena(parte(Buv, Buv._ix["c"] + Buv._ix["u1"] + Buv._ix["le"] + Buv._ix["u2"], "−v ≤ u ≤ v"), sl_[1], passo=0.025, extra=[Create(sl_[0])])
        Buv._esc = True
        t_sl = self.t

        # C17.6 — por dentro: 1/sen v sai, colchete (os limites voam de B_uv; cos e sen do enunciado)
        self.gat("por dentro")
        L6 = Lp([("I", r"\int_{\Az{-\vv}}^{\Co{\vv}}"), ("f", r"\dfrac{\Ci{\cos}\uu}{\Ci{\sen}\vv}"), ("du", r"\,\du")], CX, 0, 40)
        col.poe(L6)
        L6._xy = (CX, centro(L6)[1])
        lo6, hi6 = idx_lims(L6, "I")
        n6, _, d6 = nd(L6, "f")
        self.escreve_voos(L6, [(gl(Buv, "u1"), lo6), (gl(Buv, "u2"), hi6), (g_(E, nE[0:3]), n6[0:3]), (g_(E, dE[0:3]), d6[0:3])])
        self.gat("sai da integral")
        L6 = cresce(self, L6, [("e1", "="), ("k", r"\dfrac{1}{\Ci{\sen}\vv}"), ("lb", r"\Big["), ("F", r"\Ci{\sen}\uu"), ("rb", r"\Big]"),
                               ("sb", r"_{\uu=\Az{-\vv}}^{\uu=\Co{\vv}}")],
                    voos=lambda B: [(g_(L6, d6).copy(), [B._ix["k"][k] for k in range(2, len(B._ix["k"]))]),
                                    (g_(L6, lo6).copy(), lims_sb(B, "sb")[0][-2:]), (g_(L6, hi6).copy(), lims_sb(B, "sb")[1][-1:])],
                    col=col, nota="C17.6 (1/sen v sai; colchete)")
        if self.t - t_sl < 3.0:
            self.wait(3.0 - (self.t - t_sl))
        corta(self, *sl_)                                              # o selo da região ficou ≥ 3 s
        # C17.7 — G(b) − G(a) (mapa da linha de cima) e, ao lado, sen(−v) = −sen v
        self.gat("dá seno de vê menos")
        k6, F6, sb6 = L6._ix["k"], L6._ix["F"], L6._ix["sb"]
        lo_sb, hi_sb = lims_sb(L6, "sb")

        def mapa7(B):
            n_, b_, d_ = nd(B, "d")
            return [("e1", "e"), (F6[0:3], n_[0:3]), (hi_sb[-1:], [n_[3]]), (lo_sb[-2:], n_[9:11]), ([k6[1]], b_), (k6[2:], d_)]
        L7 = deriva(self, L6, [("e", "="), ("d", r"\dfrac{\Ci{\sen}\vv-\Ci{\sen}(-\vv)}{\Ci{\sen}\vv}")], mapa7, col, x=eq_x(L6, "e1"),
                    nota="M10 C17.7 (G(v) − G(−v))")
        self.gat("seno de menos vê é menos")
        nt = Lp([("l", r"\Ci{\sen}(-\vv)"), ("e", "="), ("r", r"-\Ci{\sen}\vv")], dir_(L7) + 48, centro(L7)[1], 40)
        n7_ = nd(L7, "d")[0]                                            # sen v − sen ( − v )
        tem7 = L7 in self.mobjects
        passo(self, L7, nt, [(n7_[5:8], nt._ix["l"][0:3]), (n7_[8:12], nt._ix["l"][3:7])], copia=True, rt=0.8, nota="M10 C17.7 (o sen(−v) sai da linha)")
        if tem7 and L7 not in self.mobjects:
            self.add(L7)
        # C17.8 — (sen v + sen v)/sen v (mapa) = 2 sen v / sen v; o par acende e some; = 2
        self.gat("então fica seno de vê mais")
        self.play(FadeOut(B1), FadeOut(B2), run_time=0.3)                  # as bordas já serviram (B_uv fica): no máximo 7 linhas
        self.remove(B1, B2)
        col.tira(B1, B2)
        n7, b7, d7 = nd(L7, "d")

        def mapa8(B):
            n_, b_, d_ = nd(B, "d")
            return [("e", "e"), (n7[0:4], n_[0:4]), ([n7[4], n7[9]], [n_[4]]), (n7[5:8], n_[5:8]), ([n7[10]], [n_[8]]), (b7, b_), (d7, d_)]
        L8 = deriva(self, L7, [("e", "="), ("d", r"\dfrac{\Ci{\sen}\vv+\Ci{\sen}\vv}{\Ci{\sen}\vv}")], mapa8, col, x=eq_x(L7, "e"),
                    nota="M10 C17.8 (− sen(−v) → + sen v)")
        self.gat("dois seno de vê")
        n8, b8, d8 = nd(L8, "d")
        L8 = cresce(self, L8, [("e2", "="), ("q", r"\dfrac{2\,\Ci{\sen}\vv}{\Ci{\sen}\vv}")],
                    voos=lambda B: [(g_(L8, n8[0:4]).copy(), nd(B, "q")[0][1:5]), (g_(L8, d8).copy(), nd(B, "q")[2])], col=col,
                    nota="C17.8 (sen v + sen v = 2 sen v)")
        self.gat("dividido por seno")
        nq, bq, dq = nd(L8, "q")
        acende(self, (VGroup(g_(L8, nq[1:5]), g_(L8, dq)), LIMA), rt=0.8)
        L8 = cresce(self, L8, [("e3", "="), ("r", "2")], voos=lambda B: [(L8[0][nq[0]].copy(), "r")], col=col, nota="C17.8 (o par some: = 2)")

        # C17.9 — por fora (as linhas 6 e 7 já serviram e saem; a 8 sobe)
        self.gat("por fora")
        # a linha 7 e a nota já serviram e saem; B_uv e a linha 6 sobem para o lugar das bordas e a 8 encosta embaixo da 6 (a 6 fica: a 8 continua dela)
        dyb = centro(Buv)[1] - centro(B1)[1]
        dy8 = pxof(L8.get_top())[1] - (pxof(L6.get_bottom())[1] - dyb + col.GAP36)
        self.play(FadeOut(L7), FadeOut(nt), run_time=0.4)  # final K12: troca de página em dois tempos (sai, depois sobe)
        self.play(Buv.animate.shift(UP * dyb / 120), L6.animate.shift(UP * dyb / 120), L8.animate.shift(UP * dy8 / 120), run_time=0.6)
        self.remove(L7, nt)
        col.ls = [J2, J3, Buv, L6, L8]
        L9 = Lp([("h", r"\Lm{\dfrac{1}{2}}"), ("I", r"\int_{\Vc{1}}^{\Vc{2}}"), ("t", r"2\,\dv")], CX, 0, 40)
        col.poe(L9)
        L9._xy = (CX, centro(L9)[1])
        lo9, hi9 = idx_lims(L9, "I")
        v1 = Buv._ix["v1"]
        self.escreve_voos(L9, [(g_(J3, J3._ix["r"][1:]), "h"), (Buv[0][v1[0]], lo9), (Buv[0][v1[-1]], hi9), (L8[0][L8._ix["r"][0]], [L9._ix["t"][0]])])
        self.gat("a primitiva de dois")
        t9 = L9._ix["t"]
        L9 = cresce(self, L9, [("e", "="), ("h2", r"\Lm{\dfrac{1}{2}}"), ("lb", r"\Big["), ("F", r"2\vv"), ("rb", r"\Big]"), ("sb", r"_{\Vc{1}}^{\Vc{2}}")],
                    voos=lambda B: [(g_(L9, L9._ix["h"]).copy(), "h2"), (L9[0][t9[0]].copy(), [B._ix["F"][0]]), (g_(L9, lo9).copy(), lims_sb(B, "sb")[0]),
                                    (g_(L9, hi9).copy(), lims_sb(B, "sb")[1])], col=col, nota="C17.9 (primitiva [2v])")
        self.gat("quatro menos dois")
        h2, F9 = L9._ix["h2"], L9._ix["F"]
        lo9b, hi9b = lims_sb(L9, "sb")

        def mapa9(B):
            p = B._ix["p"]
            # p: ( 2 · 2 − 2 · 1 )  →  índices 0..8
            return [("e", "e"), (h2, "h3"), ([F9[0]], [p[1], p[5]]), (hi9b, [p[3]]), (lo9b, [p[7]])]
        L9b = deriva(self, L9, [("e", "="), ("h3", r"\Lm{\dfrac{1}{2}}"), ("p", r"(2\cdot\Vc{2}-2\cdot\Vc{1})")], mapa9, col, x=eq_x(L9, "e"),
                     nota="M10 C17.9 (G(2) − G(1))")
        L9b = cresce(self, L9b, [("e2", "="), ("h4", r"\Lm{\dfrac{1}{2}}"), ("c", r"\cdot"), ("s", "2")],
                     voos=lambda B: [(g_(L9b, L9b._ix["h3"]).copy(), "h4"), (g_(L9b, L9b._ix["p"]).copy(), "s")], col=col, nota="C17.9 (= 1/2 · 2)")
        self.gat("um meio vezes dois")
        L9b = cresce(self, L9b, [("e3", "="), ("r", "1")], voos=lambda B: [(VGroup(g_(L9b, L9b._ix["h4"]), g_(L9b, L9b._ix["s"])).copy(), "r")], col=col,
                     nota="C17.9 (= 1)")
        ck = check_px(dir_(L9b) + 30, centro(L9b)[1], MEN)
        self.play(Create(ck), run_time=0.4)
        self.gat("trocaram de papel")
        sl2 = selo("SINAL TROCOU, MÓDULO NÃO", dir_(J3) + 40, centro(J3)[1] + 12, LIMA, 26)
        poe_selo(self, sl2)
        self.marca("B7")
        self.sai_fim()
