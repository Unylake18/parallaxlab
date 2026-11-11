"""Lote PB6 · A TABELA (layout A; alvos 10–13). B6-1: o campo da aula faz zoom × 10 em volta de P (Transform único das setas, avaliadas em
P + (X, Y)/10); B6-2: tira a seta do centro (campo residual R, Transform único). B6-3 em diante: o palco mostra o MODELO LINEAR LOCAL J·(X, Y),
exato, em contexto; as setas ∂F/∂x e ∂F/∂y voam para as colunas de J_F(P); J = (1 −1; 2 0) (TransformByGlyphMap). B6-4: o quadradinho [0; 1,2]²
com a quina em P, as colunas × 0,4 empurram as arestas. B6-5: o quadradinho anda por e^{tJ} (exato para o modelo) de 0 a 0,35: área × 1,42."""
from v28 import *  # noqa: F401,F403

V = Vista(600, 540, 120)
S = 1.2
SQ = [(0, 0), (S, 0), (S, S), (0, S)]
MAT = r"J_{\F}(\Pt)=\begin{pmatrix}\dfrac{\partial\Pp}{\dx} & \dfrac{\partial\Pp}{\dy}\\[10pt] \dfrac{\partial\Qq}{\dx} & \dfrac{\partial\Qq}{\dy}\end{pmatrix}"
NUM = r"=\begin{pmatrix}\Am{1} & \Mg{-1}\\ \Am{2} & \Mg{0}\end{pmatrix}"
JN = r"J=\begin{pmatrix}\Am{1} & \Mg{-1}\\ \Am{2} & \Mg{0}\end{pmatrix}"
# índices dos glifos (conferidos com _dbg.py): MAT 0–6 "J_F(P)=", 7–10 "(", col. 1 = 11–15 e 21–25, col. 2 = 16–20 e 26–30, 31–34 ")";
# NUM 0 "=", 1 "(", col. 1 = 2, 5; col. 2 = 3, 4, 6; 7 ")"; JN 0 "J", 1 "=", 2 "(", col. 1 = 3, 6; col. 2 = 4, 5, 7; 8 ")"
C1, C2 = [*range(11, 16), *range(21, 26)], [*range(16, 21), *range(26, 31)]


def zoom_lbl():
    return TP(r"\text{ZOOM}\times 10", *canto_xy(V, -2.35, 3.0), 30)


def modelo_lbl():
    t = T("MODELO LINEAR LOCAL", *canto_xy(V, -1.3, 2.92), 26, "left", GEO, bold=False)
    g = VGroup(placa7(t, 8, 4), t)
    g.f = t
    return g


class LoteB6(Base):
    ANTES = "O ENGANO"

    def corpo(self):
        # ── B6-1 · zoom × 10; tira a seta do centro ──
        self.an("B6-1")
        self.secao("A TABELA")
        cmp = campo28(V, F_AULA, y1=2.5, rmin=0, mmax=3.5, nome="B6 campo da aula")
        st = {"t": NADA}
        clareira(cmp, lambda: st["t"])
        self.gat("pega o campo da aula")
        self.play(cresce_campo(cmp, 1.0), run_time=1.0)
        z = mesma_grade(cmp, F_ZOOM, 6)
        zl = zoom_lbl()
        self.gat("dez vezes mais perto")
        self.play(Transform(cmp, z), FadeIn(zl), run_time=1.6)
        herda(cmp, z)
        r = mesma_grade(cmp, F_RESID, 6)
        P = ponto7(V.c2p(0, 0), POS, 9, 11)
        self.gat("agora tira a seta do centro")
        self.play(Transform(cmp, r), FadeIn(P, scale=0.5), run_time=1.6)
        herda(cmp, r)
        lg = VGroup(legenda("DE PERTO, SEM A SETA DO CENTRO,", 1114, 450, GEO), legenda("SOBRA UM CAMPO LINEAR", 1114, 495, GEO))
        self.gat("olha que campo arrumadinho")
        self.play(FadeIn(lg, shift=0.06 * UP), run_time=0.6)
        self.ate(0.97)

        # ── B6-2 · a matriz jacobiana ──
        self.an("B6-2")
        ap = TC(r"\F(\Pt+H)-\F(\Pt)\approx\h\,\dfrac{\partial\F}{\dx}+\k\,\dfrac{\partial\F}{\dy}", 1110, 330, 40)
        self.gat("bem de perto essa mudança é escrita")
        self.play(caneta(ap, ritmo=0.55))
        lin = mesma_grade(cmp, F_LIN, 6, ctx=True)
        ml = modelo_lbl()
        self.gat("então coloca as duas lado a lado")
        self.play(FadeOut(ap), FadeOut(lg), Transform(cmp, lin), FadeIn(ml), run_time=1.2)
        self.remove(ap, lg)
        herda(cmp, lin)
        print("[B6] do B6-3 em diante o palco é o modelo linear local J·H = (X − Y, 2X)")
        mat = TC(MAT, 1110, 360, 44)
        g = mat[0]
        col1, col2 = VGroup(*[g[i] for i in C1]), VGroup(*[g[i] for i in C2])
        resto = VGroup(*[g[i] for i in range(len(g)) if i not in C1 and i not in C2])
        sx = seta7(V.c2p(0, 0), V.c2p(.4, .8), E1, 7, 22).set_z_index(12)
        sy = seta7(V.c2p(0, 0), V.c2p(-.4, 0), E2, 7, 22).set_z_index(12)
        self.play(GrowArrow(sx), GrowArrow(sy), run_time=0.6)
        c1c, c2c = col1.copy(), col2.copy()
        mat._esc = True
        resto._caneta, resto._esc, resto._em_caneta, resto._tex = True, False, False, "J_F(P) = ( )"
        self.play(caneta(resto, ritmo=0.6), ReplacementTransform(sx, c1c, path_arc=-0.6), ReplacementTransform(sy, c2c, path_arc=0.6))
        self.remove(c1c, c2c, resto)
        self.add(mat)
        mj = T("MATRIZ JACOBIANA", 1114, 700, 40)
        mjl = leg_mix(["1ª COLUNA:", r"$\partial F/\partial x$", "· 2ª COLUNA:", r"$\partial F/\partial y$"], 1114, 760, GEO, "left", 28, up=False, gap=7)
        self.gat("matriz jacobiana")
        self.play(FadeIn(mj, shift=0.06 * UP), run_time=0.5)
        self.play(FadeIn(mjl, shift=0.06 * UP), run_time=0.5)
        num = TC(NUM, 1310, 560, 52)
        mapa = [([7, 8, 9, 10], [1]), (C1, [2, 5]), (C2, [3, 4, 6]), ([31, 32, 33, 34], [7]), ([6], [0])]
        self.gat("no nosso ponto ela vale")
        self.play(tbgm(mat, num, *mapa, rt=1.6, copia=True))
        limpa_soltos(self)
        self.ate(0.97)

        # ── B6-3 · as colunas empurram as arestas; solta o fluido ──
        self.an("B6-3")
        jn = TC(JN, 1120, 330, 48)
        self.gat("e agora a parte bonita")
        self.play(FadeOut(mat), FadeOut(mj), FadeOut(mjl), tbgm(num, jn, ([0], [1]), ([1], [2]), ([2], [3]), ([5], [6]), ([3], [4]), ([4], [5]), ([6], [7]), ([7], [8]), rt=1.2), run_time=1.2)
        self.remove(mat, mj, mjl)
        limpa_soltos(self)
        ped = Pedaco(V, SQ)
        P2 = ponto7(V.c2p(0, 0), POS, 10, 12)
        self.gat("coloca um quadradinho")
        st["t"] = clarPoly(SQ, .25)
        self.play(FadeIn(ped), FadeOut(P), FadeIn(P2), run_time=0.7)
        self.remove(P)
        ax = seta7(V.c2p(S, 0), V.c2p(S + .4, .8), E1, 8, 26).set_z_index(12)
        ay = seta7(V.c2p(0, S), V.c2p(-.4, S), E2, 8, 26).set_z_index(12)
        lq1 = legenda("QUINA DA DIREITA: 1ª COLUNA", 1124, 610, E1)
        lq2 = legenda("QUINA DE CIMA: 2ª COLUNA", 1124, 655, E2)
        self.gat("a quina da direita")
        st["t"] = ou(clarPoly(SQ, .25), clar28([(S - .05, .05, S + .45, .85)]))
        self.play(GrowArrow(ax), FadeIn(lq1, shift=0.06 * UP), run_time=0.7)
        self.gat("a quina de cima")
        st["t"] = ou(clarPoly(SQ, .25), clar28([(S - .05, .05, S + .45, .85), (-.55, S - .1, -.05, S + .1)]))
        self.play(GrowArrow(ay), FadeIn(lq2, shift=0.06 * UP), run_time=0.7)
        ce = VGroup(T("AS COLUNAS EMPURRAM", 1120, 480, 38), T("AS ARESTAS", 1120, 530, 38))
        self.gat("cada coluna da tabela empurra uma aresta")
        self.play(FadeIn(ce, shift=0.06 * UP), run_time=0.6)
        fan = fantasma(V, SQ)
        self.gat("solta o fluido no modelo")
        self.play(FadeOut(ax), FadeOut(ay), FadeOut(ce), FadeOut(lq1), FadeOut(lq2), run_time=0.4)
        self.remove(ax, ay, ce, lq1, lq2)
        self.add(fan)
        st["t"] = NADA
        lbl = clar28([(1.0, -.95, 2.1, -.55)])
        cmp.clear_updaters()
        clareira(cmp, lambda: ou(clarPoly(ped.poly(), .25), clarPoly(SQ, .15)))
        a0 = ped.area()
        self.play(anda(ped, fl_J, .35, 2.5, nome="B6 e^{tJ}"))
        print(f"[B6] área {a0:.4f} → {ped.area():.4f} (× {ped.area() / a0:.4f}; det e^(0,35 J) = e^(0,35) = {math.exp(.35):.4f})")
        M = expJA(.35)
        print(f"[B6] e^(0,35 J) = [[{M[0, 0]:.4f}, {M[0, 1]:.4f}], [{M[1, 0]:.4f}, {M[1, 1]:.4f}]]")
        cmp.clear_updaters()
        clareira(cmp, lambda: ou(clarPoly(ped.poly(), .25), clarPoly(SQ, .15), lbl))
        ar = TP(r"\text{ÁREA}\times 1{,}42", *canto_xy(V, 1.55, -.75), 32)
        self.play(FadeIn(ar), run_time=0.5)
        gce = T("GIRA · CRESCE · ENTORTA", 1120, 490, 38)
        self.gat("gira cresce e entorta")
        self.play(FadeIn(gce, shift=0.06 * UP), run_time=0.5)
        tm = legenda("TUDO AO MESMO TEMPO", 1124, 550, GEO)
        self.gat("tudo ao mesmo tempo")
        self.play(FadeIn(tm, shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)
        cmp.clear_updaters()
        self.sai_fim()
