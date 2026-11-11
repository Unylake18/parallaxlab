"""Lote PB6 · A TABELA (v2; alvos 18–24). B6-1: a janela × 10 em volta de P cresce até o palco e as setas são reavaliadas continuamente em
P + (X, Y)/s, s de 1 a 10 (E4); cada seta = a seta do centro + um resto (triângulo em tamanho × 2, no ponto (−1; 1) do palco); tira a seta do centro
(Transform único para o campo residual). B6-2: a matriz simbólica na caneta; os números voam dos valores (1, 2) e (−1, 0) (E3: nada de glyph map de
matriz). B6-3: J·H = h·(1ª coluna) + k·(2ª coluna). B6-4: o quadradinho, as colunas empurram as arestas e o fluxo e^{tJ} do modelo (área × 1,42)."""
from v28 import *  # noqa: F401,F403

V = Vista(600, 540, 120)
S = 1.2
SQ = [(0, 0), (S, 0), (S, S), (0, S)]
MAT = r"J_{\F}(\Pt)=\begin{pmatrix}\dfrac{\partial\Pp}{\dx} & \dfrac{\partial\Pp}{\dy}\\[10pt] \dfrac{\partial\Qq}{\dx} & \dfrac{\partial\Qq}{\dy}\end{pmatrix}"
NUM = r"=\begin{pmatrix}\Am{1} & \Mg{-1}\\ \Am{2} & \Mg{0}\end{pmatrix}"
JN = r"J=\begin{pmatrix}\Am{1} & \Mg{-1}\\ \Am{2} & \Mg{0}\end{pmatrix}"
# NUM: 0 "=", 1 "(", 2 "1", 3 "−", 4 "1", 5 "2", 6 "0", 7 ")"  (conferido no v1 com _dbg.py)


def zoom_lbl():
    return TP(r"\text{ZOOM}\times 10", *canto_xy(V, -2.35, 3.0), 30)


def modelo_lbl():
    t = T("MODELO LINEAR LOCAL", *canto_xy(V, -1.3, 2.92), 26, "left", GEO, bold=False)
    g = VGroup(placa7(t, 8, 4), t)
    g.f = t
    return g


def seta_zoom(X, Y, s):
    mm = 3.5 + (6 - 3.5) * (s - 1) / 9
    return seta_campo(V, X, Y, F_AULA(X / s, Y / s), .42, mm)


class LoteB6(Base):
    ANTES = "O ENGANO"

    def corpo(self):
        # ── B6-1 · a janela × 10 vira o palco (alvos 18, 19, 20) ──
        self.an("B6-1")
        self.secao("A TABELA")
        cmp = campo28(V, F_AULA, rmin=0, mmax=3.5, nome="B6 campo da aula")
        st = {"t": NADA}
        clareira(cmp, lambda: st["t"])
        P = ponto7(V.c2p(0, 0), POS, 8, 11)
        self.gat("pega o campo da aula")
        self.play(cresce_campo(cmp, 1.0), FadeIn(P), run_time=1.0)
        zs = ValueTracker(1.0)
        jan = vlinha(V, [(-.3, -.3), (.3, -.3), (.3, .3), (-.3, .3), (-.3, -.3)], BR, 3).set_z_index(8)
        lz = TP(r"\times 10", *canto_xy(V, .82, .6), 32)
        ch = VGroup(T("CHEGA DEZ VEZES", 1120, 420, 40), T("MAIS PERTO", 1120, 475, 40))
        self.gat("dez vezes mais perto")
        st["t"] = clar28([(-.35, -.35, .35, .35), (.4, .35, 1.25, .85)])
        self.play(Create(jan), FadeIn(lz), FadeIn(ch, shift=0.06 * UP), run_time=0.8)
        lj = legenda("ESSA JANELINHA VIRA O PALCO INTEIRO", 1124, 560, GEO)
        self.gat("essa janelinha vira o palco inteiro")
        self.play(FadeIn(lj, shift=0.06 * UP), FadeOut(lz), run_time=0.5)
        self.remove(lz)
        st["t"] = NADA

        def zoom(m, a):
            s = 1 + 9 * smooth(a)
            zs.set_value(s)
            h = min(3.05, .3 * s)
            jan.set_points_as_corners([V.c2p(*p) for p in ((-h, -h), (h, -h), (h, h), (-h, h), (-h, -h))])
            for a_ in cmp:
                X, Y = a_._xy
                n = seta_zoom(X, Y, s)
                if n is not None:
                    a_.become(n)
                    a_._t, a_._f = n._t, n._f
        self.play(UpdateFromAlphaFunc(jan, zoom), run_time=2.2)
        st["t"] = lambda X, Y: Y > 2.75
        print("[E4] zoom contínuo: setas reavaliadas em P + (X, Y)/s, s de 1 a 10, mmax de 3,5 a 6")
        topo = VGroup(*[a_ for a_ in cmp if a_._xy[1] > 2.75])
        zl = zoom_lbl()
        self.play(FadeOut(jan), some(topo, 0.5), FadeIn(zl), run_time=0.5)
        self.remove(jan)
        # cada seta = a seta do centro + um resto (no ponto (−1; 1) do palco = H = (−0,1; 0,1); tamanho × 2)
        Xs, k2 = np.array([-1.0, 1.0]), 2.0
        FX = np.array(F_AULA(-.1, .1), float)
        A, B, C = Xs, Xs + k2 * np.array([1.0, 0]), Xs + k2 * FX
        print(f"[B6] H = (−0,1; 0,1): F = ({FX[0]:.3f}; {FX[1]:.3f}), resto = ({FX[0] - 1:.3f}; {FX[1]:.3f})")
        tri = VGroup(seta7(V.c2p(*A), V.c2p(*B), GEO, 5, 20), seta7(V.c2p(*B), V.c2p(*C), CAMPO2, 7, 20), seta7(V.c2p(*A), V.c2p(*C), CAMPO, 5, 20),
                     ponto7(V.c2p(*A), POS, 7, 13)).set_z_index(12)
        ltri = VGroup(TP(r"\F(\Pt)", *canto_xy(V, 0, 1.38), 30), TP(r"\text{resto}", *canto_xy(V, 1.25, .62), 30), TP(r"\F(\Xp)", *canto_xy(V, -.35, .5), 30))
        fr = TC(r"\F(\Xp)=\F(\Pt)+\big(\F(\Xp)-\F(\Pt)\big)", 1110, 330, 40)
        lg = VGroup(legenda("QUASE TUDO É A SETA DO CENTRO", 1114, 440, GEO), legenda("TIRANDO ELA, SOBRA SÓ A MUDANÇA", 1114, 490, GEO),
                    legenda("(SETAS DESTA CONTA EM TAMANHO × 2)", 1114, 560, GEO, "left", 26))
        self.gat("cada uma é a seta do centro")
        st["t"] = ou(clar28([(-1.3, .35, 1.35, 1.75)], [(0, 0, .25)]), lambda X, Y: Y > 2.75)
        self.play(FadeOut(ch), FadeOut(lj), run_time=0.3)
        self.remove(ch, lj)
        self.play(GrowArrow(tri[0]), FadeIn(tri[3]), FadeIn(ltri[0]), run_time=0.5)
        self.play(GrowArrow(tri[1]), FadeIn(ltri[1]), GrowArrow(tri[2]), FadeIn(ltri[2]), caneta(fr, ritmo=0.3))
        self.play(FadeIn(lg, shift=0.06 * UP), run_time=0.4)
        r = mesma_grade(cmp, F_RESID, 6)
        for a_, b_ in zip(cmp, r):
            if a_._xy[1] > 2.75 or math.hypot(*a_._xy) < .3:
                b_.set_opacity(0)
        self.gat("tira a seta do centro de todas")
        st["t"] = lambda X, Y: Y > 2.75 or math.hypot(X, Y) < .3
        self.play(FadeOut(tri), FadeOut(ltri), Transform(cmp, r), run_time=1.4)
        self.remove(tri, ltri)
        herda(cmp, r)
        self.ate(0.97)

        # ── B6-2 · a matriz jacobiana (alvo 21) ──
        self.an("B6-2")
        ap = TC(r"\F(\Pt+H)-\F(\Pt)\approx\h\,\dfrac{\partial\F}{\dx}+\k\,\dfrac{\partial\F}{\dy}", 1110, 330, 40)
        lg2 = VGroup(legenda("DE PERTO, SEM A SETA DO CENTRO,", 1114, 450, GEO), legenda("SOBRA UM CAMPO LINEAR", 1114, 495, GEO))
        self.gat("bem de perto essa mudança é escrita")
        self.play(FadeOut(fr), FadeOut(lg), run_time=0.35)
        self.remove(fr, lg)
        self.play(caneta(ap, ritmo=0.35), FadeIn(lg2, shift=0.06 * UP))
        lin = mesma_grade(cmp, F_LIN, 6, ctx=True)
        for a_, b_ in zip(cmp, lin):
            if a_._xy[1] > 2.75 or math.hypot(*a_._xy) < .3:
                b_.set_opacity(0)
        ml = modelo_lbl()
        mat = TC(MAT, 1110, 360, 44)
        self.gat("então coloca as duas lado a lado")
        self.play(FadeOut(ap), FadeOut(lg2), Transform(cmp, lin), FadeIn(ml), run_time=1.0)
        self.remove(ap, lg2)
        herda(cmp, lin)
        self.play(caneta(mat, ritmo=0.3))
        # os valores do B4 (a coluna do palco) voltam como rótulos, e cada número voa para a sua casa
        r1 = TP(r"\dfrac{\partial\F}{\dx}=\Am{(1,\,2)}", *canto_xy(V, 1.8, 2.1), 34)
        r2 = TP(r"\dfrac{\partial\F}{\dy}=\Mg{(-1,\,0)}", *canto_xy(V, -1.9, .5), 34)
        st["t"] = ou(lambda X, Y: Y > 2.75 or math.hypot(X, Y) < .3, clar28([(1.05, 1.6, 2.55, 2.45), (-2.65, .2, -1.15, .8)]))
        self.gat("a derivada na horizontal na primeira")
        self.play(FadeIn(r1[0]), caneta(r1.f, ritmo=0.4))
        self.gat("a derivada na vertical na segunda")
        self.play(FadeIn(r2[0]), caneta(r2.f, ritmo=0.4))
        mj = T("MATRIZ JACOBIANA", 1114, 700, 40)
        mjl = TC(r"\textcolor{cg}{1^{\underline{\text{a}}}\text{ COLUNA: }}\partial\F/\dx\quad\textcolor{cg}{\cdot\ 2^{\underline{\text{a}}}\text{ COLUNA: }}\partial\F/\dy", 1114, 760, 30, "l")
        self.gat("matriz jacobiana")
        self.play(FadeIn(mj, shift=0.06 * UP), run_time=0.5)
        self.play(caneta(mjl, ritmo=0.3))
        num = TC(NUM, 1310, 560, 52, caneta=False)
        g, a1, a2 = num[0], r1.f[0], r2.f[0]
        voos = [TransformFromCopy(a1[-4], g[2], path_arc=-0.6), TransformFromCopy(a1[-2], g[5], path_arc=-0.6),
                TransformFromCopy(VGroup(a2[-5], a2[-4]), VGroup(g[3], g[4]), path_arc=0.6), TransformFromCopy(a2[-2], g[6], path_arc=0.6)]
        self.gat("no nosso ponto")
        self.play(Create(VGroup(g[0], g[1], g[7])), *voos, run_time=1.4)
        self.remove(*[x for x in self.mobjects if x in (g[0], g[1], g[7], g[2], g[3], g[4], g[5], g[6])])
        self.add(num)
        limpa_soltos(self)
        self.play(FadeOut(r1), FadeOut(r2), run_time=0.4)
        self.remove(r1, r2)
        st["t"] = lambda X, Y: Y > 2.75 or math.hypot(X, Y) < .3
        self.ate(0.97)

        # ── B6-3 · J·H = h·(1ª coluna) + k·(2ª coluna) (alvo 22) ──
        self.an("B6-3")
        Xs, c1, c2 = np.array([.9, .6]), np.array([.9, 1.8]), np.array([-.6, 0])
        T1, T2 = Xs + c1, Xs + c1 + c2
        sH = seta7(V.c2p(0, 0), V.c2p(*Xs), POS, 6, 18).set_z_index(12)
        s1 = seta7(V.c2p(*Xs), V.c2p(*T1), E1, 7, 22).set_z_index(12)
        s2 = seta7(V.c2p(*T1), V.c2p(*T2), E2, 7, 22).set_z_index(12)
        sJ = seta7(V.c2p(*Xs), V.c2p(*T2), CAMPO2, 7, 22).set_z_index(12)
        lH = TP(r"\textcolor{cp}{H}", *canto_xy(V, .25, .55), 30)
        l1 = TP(r"\h\,(\Am1,\Am2)", *canto_xy(V, 1.95, 1.7), 30)
        l2 = TP(r"\k\,(\Mg{-1},\Mg0)", *canto_xy(V, 1.5, 2.75), 30)
        lJ = TP(r"J H", *canto_xy(V, .45, 1.95), 30)
        e1 = TC(r"J\begin{pmatrix}\h\\ \k\end{pmatrix}=\h\begin{pmatrix}\Am{1}\\ \Am{2}\end{pmatrix}+\k\begin{pmatrix}\Mg{-1}\\ \Mg{0}\end{pmatrix}", 1110, 330, 44)
        e2 = TC(r"=(\h-\k,\ \ 2\h)", 1180, 470, 44)
        le1 = legenda("PASSO HORIZONTAL × 1ª COLUNA", 1114, 580, E1)
        le2 = legenda("PASSO VERTICAL × 2ª COLUNA", 1114, 630, E2)
        ex = TC(r"\textcolor{cp}{H}=(0{,}9;\ 0{,}6)\ \Rightarrow\ JH=(0{,}3;\ 1{,}8)", 1110, 750, 34)
        segs = [((0, 0), tuple(Xs)), (tuple(Xs), tuple(T1)), (tuple(T1), tuple(T2)), (tuple(Xs), tuple(T2))]
        self.gat("um passo com uma parte horizontal")
        self.play(FadeOut(mat), FadeOut(num), FadeOut(mj), FadeOut(mjl), run_time=0.4)
        self.remove(mat, num, mj, mjl)
        st["t"] = ou(lambda X, Y: Y > 2.75 or math.hypot(X, Y) < .3, clarSeg(segs, .3), clar28([(1.3, 1.4, 2.6, 2.0), (-.6, 1.6, 1.0, 2.3), (.9, 2.5, 2.1, 3.0), (-.05, .35, .5, .75)]))
        self.play(GrowArrow(sH), FadeIn(lH), run_time=0.6)
        self.play(caneta(e1, ritmo=0.35))
        self.gat("vira a parte horizontal vezes a primeira coluna")
        self.play(GrowArrow(s1), FadeIn(l1), FadeIn(le1, shift=0.06 * UP), run_time=0.8)
        self.gat("mais a parte vertical vezes a segunda")
        self.play(GrowArrow(s2), FadeIn(l2), FadeIn(le2, shift=0.06 * UP), run_time=0.8)
        self.gat("a seta do modelo é a soma das duas")
        self.play(GrowArrow(sJ), FadeIn(lJ), caneta(e2, ritmo=0.45))
        self.play(caneta(ex, ritmo=0.3))
        print(f"[B6] J·H com H = (0,9; 0,6): {tuple(np.round(JA @ Xs, 3))}")
        self.ate(0.97)

        # ── B6-4 · o quadradinho; as colunas empurram; o fluxo do modelo (alvos 23 e 24) ──
        self.an("B6-4")
        jn = TC(JN, 1120, 330, 48)
        sai = [sH, s1, s2, sJ, lH, l1, l2, lJ, e1, e2, le1, le2, ex]
        ped = Pedaco(V, SQ)
        P2 = ponto7(V.c2p(0, 0), POS, 10, 12)
        self.gat("agora coloca um quadradinho")
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        base = lambda X, Y: Y > 2.75 or math.hypot(X, Y) < .3
        st["t"] = ou(base, clarPoly(SQ, .25))
        self.play(FadeIn(ped), FadeOut(P), FadeIn(P2), caneta(jn, ritmo=0.4))
        self.remove(P)
        ax = seta7(V.c2p(S, 0), V.c2p(S + .4, .8), E1, 8, 26).set_z_index(12)
        ay = seta7(V.c2p(0, S), V.c2p(-.4, S), E2, 8, 26).set_z_index(12)
        lq1 = legenda("QUINA DA DIREITA: 1ª COLUNA", 1124, 610, E1)
        lq2 = legenda("QUINA DE CIMA: 2ª COLUNA", 1124, 655, E2)
        self.gat("a quina da direita")
        st["t"] = ou(base, clarPoly(SQ, .25), clar28([(S - .05, .05, S + .45, .85)]))
        self.play(GrowArrow(ax), FadeIn(lq1, shift=0.06 * UP), run_time=0.7)
        self.gat("a de cima")
        st["t"] = ou(base, clarPoly(SQ, .25), clar28([(S - .05, .05, S + .45, .85), (-.55, S - .1, -.05, S + .1)]))
        self.play(GrowArrow(ay), FadeIn(lq2, shift=0.06 * UP), run_time=0.7)
        ce = VGroup(T("AS COLUNAS EMPURRAM", 1120, 480, 38), T("AS ARESTAS", 1120, 530, 38))
        self.gat("cada coluna empurra uma aresta")
        self.play(FadeIn(ce, shift=0.06 * UP), run_time=0.6)
        fan = fantasma(V, SQ)
        self.gat("solta o fluido no modelo")
        self.play(FadeOut(ax), FadeOut(ay), FadeOut(ce), FadeOut(lq1), FadeOut(lq2), run_time=0.4)
        self.remove(ax, ay, ce, lq1, lq2)
        self.add(fan)
        lbl = clar28([(1.0, -.95, 2.1, -.55)])
        st["t"] = NADA
        cmp.clear_updaters()
        clareira(cmp, lambda: ou(base, clarPoly(ped.poly(), .25), clarPoly(SQ, .15)))
        a0 = ped.area()
        self.play(anda(ped, fl_J, .35, 2.5, nome="B6 e^{tJ}"))
        print(f"[B6] área {a0:.4f} → {ped.area():.4f} (× {ped.area() / a0:.4f})")
        cmp.clear_updaters()
        clareira(cmp, lambda: ou(base, clarPoly(ped.poly(), .25), clarPoly(SQ, .15), lbl))
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
