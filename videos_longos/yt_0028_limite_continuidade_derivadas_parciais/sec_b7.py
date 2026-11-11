"""Lote PB7 · QUATRO NÚMEROS, QUATRO MEDIDAS (v3: alvos 30–36; matriz de movimentos e arestas no papel, cartões C encaixados, B7-4b novo: o atrito viscoso). Da v2: alvos 25–30. B7-1: a matriz de movimentos (cada número é um movimento de aresta; a aresta
se move UMA vez na direção da seta e volta). B7-2: as combinações (rot = soma dos giros, div = soma dos estiramentos, def₁ e def₂; a tesoura).
B7-3: os três cartões e os valores (da v1). B7-4: volta ao gancho, com as setas das quinas (1, 0) e (0, −1) por 2 s. B7-5: o desafio (y, x),
com as setas das quinas (0, 1) e (1, 0) por 2 s; TAMBÉM VALE a 36 px por ≥ 4 s."""
from v28 import *  # noqa: F401,F403
from sec_h import palco_sela

V = Vista(600, 540, 120)
Q12 = quad_pts((0, 0), 1.2)
CART = [(120, "GIRA", VEL, F_GIRO, fl_rot(.6)), (720, "MUDA DE ÁREA", SAI, F_EXPL, fl_escala(1.42, 1.42)), (1320, "DEFORMA", LIMA, F_SELA, fl_escala(1.5, 1 / 1.5))]
# células da matriz de movimentos: (cx, cy, ponta da aresta, ponta da seta, fórmula, legenda, cor, aresta 'h' ou 'v')
CEL = [(540, 370, (1, 0), (1.45, 0), r"\dfrac{\partial\Pp}{\dx}=\Am{1}", "ESTICA A HORIZONTAL", E1, "h"),
       (540, 730, (1, 0), (1, .9), r"\dfrac{\partial\Qq}{\dx}=\Am{2}", "GIRA A HORIZONTAL", E1, "h"),
       (1020, 370, (0, 1), (-.45, 1), r"\dfrac{\partial\Pp}{\dy}=\Mg{-1}", "TOMBA A VERTICAL", E2, "v"),
       (1020, 730, (0, 1), None, r"\dfrac{\partial\Qq}{\dy}=\Mg{0}", "ESTICA A VERTICAL", E2, "v")]


def cartao(i):
    X0, tit, cor, Fv, fl = CART[i]
    v = VB(LAY_C[i], X0 + 240, 540, 56)                # v4: 60 px/u
    p = painel(X0, 250, 480, 460, v=v)
    cmp = campo28(v, Fv, -3, 3, -3, 3, 1.0, rmin=1.2, rmax=3.6, mmax=3.4, nome=f"B7 cartão {tit}")
    return v, p, cmp, Pedaco(v, Q12), fantasma(v, Q12), T(tit, X0 + 240, 830, 34, "center", cor), fl


def parenteses():
    g = VGroup()
    for (x0, xc) in ((390, 340), (1170, 1220)):
        m = VMobject().set_points_as_corners([PX(x0 + (xc - x0) * 2 * t * (1 - t) * 2 / 2, 280 + 640 * t) for t in np.linspace(0, 1, 60)])
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
        zera_chapas()
        zM = zona_px(1200, 180, 1920, 1020, "coluna (B7-1)")
        jn = TC(r"J=\begin{pmatrix}\Am{1} & \Mg{-1}\\ \Am{2} & \Mg{0}\end{pmatrix}", 1290, 420, 52)
        g30 = grade_v(Vista(480, 420, 120), None, "B7-1 matriz (tela cheia, quinas das células nos nós)")
        frases = [("em cima à esquerda", "aqui um"), ("embaixo à esquerda", "dois"), ("em cima à direita", "menos um para a esquerda"), ("embaixo à direita", "zero")]
        primeira = True
        for (cx, cy, a, b, f, l, c, ar), (g1, g2) in zip(CEL, frases):
            v = Vista(cx - 60, cy + 50, 120)
            origem_papel(v, f"B7-1 quina da célula ({cx - 60}, {cy + 50})")
            if primeira:
                tr = vlinha(v, [(1, 0), (1, 1), (0, 1)], GEO, 2, dash=(6, 7)).set_z_index(5)
                eh = vlinha(v, [(0, 0), (1, 0)], E1, 5).set_z_index(6)
                ev = vlinha(v, [(0, 0), (0, 1)], E2, 5).set_z_index(6)
                p0 = ponto7(v.c2p(0, 0), POS, 6, 8)
                # v4 R10 (B6-7 → B7-1): a grade, os parênteses e a 1ª célula entram com o J
                self.play(FadeIn(g30), FadeIn(zM), Create(par), Create(tr), Create(eh), Create(ev), FadeIn(p0), caneta(jn, ritmo=0.4))
                primeira = False
                self.gat(g1)
                b_ = True
            else:
                b_ = False
            tr = vlinha(v, [(1, 0), (1, 1), (0, 1)], GEO, 2, dash=(6, 7)).set_z_index(5)
            eh = vlinha(v, [(0, 0), (1, 0)], E1, 5).set_z_index(6)
            ev = vlinha(v, [(0, 0), (0, 1)], E2, 5).set_z_index(6)
            p0 = ponto7(v.c2p(0, 0), POS, 6, 8)
            if not b_:
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
                lgs = [legenda("1ª COLUNA: MEXE A ARESTA HORIZONTAL", 1294, 560, E1), legenda("2ª COLUNA: MEXE A ARESTA VERTICAL", 1294, 610, E2),
                       legenda("LINHA DE CIMA: EMPURRA PARA O LADO", 1294, 700, GEO), legenda("LINHA DE BAIXO: EMPURRA PARA CIMA", 1294, 750, GEO)]
                self.play(FadeIn(pa), LaggedStart(*[FadeIn(m, shift=0.05 * UP) for m in lgs], lag_ratio=0.2), run_time=0.9)   # final (sync)
            fx = TC(f, cx, cy + 112, 30, "c")
            lx = legenda(l, cx, cy + 172, c, "center", 26)
            self.gat(g2)
            self.play(caneta(fx, ritmo=0.25), FadeIn(lx, shift=0.05 * UP))
        self.ate(0.97)

        # ── B7-2 · as combinações; a tesoura (alvo 26) ──
        self.an("B7-2")
        vq = Vista(360, 780, 150)
        g31 = grade_v(vq, None, "B7-2 combinações (tela cheia, 150 px/u)")
        Sq, k_ = 1.6, .35 * 1.6
        sai = self.snap()
        zQ = zona_px(840, 180, 1920, 1020, "coluna (B7-2)")
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
        self.play(*[FadeOut(m) for m in sai], FadeIn(g31), FadeIn(zQ), Create(tr), Create(eh), Create(ev), FadeIn(p0), run_time=0.5)     # v4 R10
        self.remove(*sai)
        self.play(GrowArrow(sa), GrowArrow(sb), FadeIn(la), FadeIn(lb), FadeIn(hv), run_time=0.7)
        linhas = [(r"\V{\rot}=\text{giro}_{\Am{\text{H}}}+\text{giro}_{\Mg{\text{V}}}=\Am{2}+\Mg{1}=\V{3}", 290, "dão o rotacional"),
                  (r"\D{\dv}=\text{estica}_{\Am{\text{H}}}+\text{estica}_{\Mg{\text{V}}}=\Am{1}+\Mg{0}=\D{1}", 430, "dão o divergente"),
                  (None, 570, None),
                  (r"\Lm{\text{def}_2}=\text{giro}_{\Am{\text{H}}}-\text{giro}_{\Mg{\text{V}}}=\Am{2}-\Mg{1}=\Lm{1}", 710, "essa é a segunda")]
        for s_, y, g in linhas:
            if s_ is None:                     # def₁ em dois tempos (v3)
                ma = TC(r"\Lm{\text{def}_1}=\text{estica}_{\Am{\text{H}}}-\text{estica}_{\Mg{\text{V}}}", 940, y, 38)
                mb = TC(r"=\Am{1}-\Mg{0}=\Lm{1}", 940, y, 38)
                mb.shift(RIGHT * (ma.get_right()[0] + 0.1 - mb.get_left()[0]))
                self.gat("estiramento horizontal menos vertical")
                self.play(caneta(ma, ritmo=0.3))
                self.gat("estica mais numa direção")
                self.play(caneta(mb, ritmo=0.3))
                continue
            m = TC(s_, 940, y, 38)
            self.gat(g)
            self.play(caneta(m, ritmo=0.3))
        tes = leg_mix([r"$\text{def}_2$", ": QUANTO O ÂNGULO RETO FECHA, COMO UMA TESOURA"], 944, 800, LIMA, "left", 26, up=True, gap=4)

        def tesoura(m, al):
            th = 0.15 * al
            eh.set_points_as_corners([vq.c2p(0, 0), vq.c2p(Sq * math.cos(th), Sq * math.sin(th))])
            ev.set_points_as_corners([vq.c2p(0, 0), vq.c2p(Sq * math.sin(th), Sq * math.cos(th))])
        self.gat("como uma tesoura")
        self.play(UpdateFromAlphaFunc(eh, tesoura, rate_func=there_and_back), FadeIn(tes, shift=0.05 * UP), run_time=1.0)   # final (sync)
        self.ate(0.97)

        # ── B7-3 · os três cartões e os valores (alvos 27 e 28) ──
        self.an("B7-3")
        sai = self.snap()
        fr = [TC(r"\V{\rot}:\ \dfrac{\partial \Qq}{\dx}-\dfrac{\partial \Pp}{\dy}", 360, 912, 34, "c"),
              TC(r"\D{\dv}:\ \dfrac{\partial \Pp}{\dx}+\dfrac{\partial \Qq}{\dy}", 960, 912, 34, "c")]
        d1, d2 = linha_partes([r"\dfrac{\partial \Pp}{\dx}-\dfrac{\partial \Qq}{\dy}", r"\Lm{\text{e}}\ \ \dfrac{\partial \Qq}{\dx}+\dfrac{\partial \Pp}{\dy}"], 1560, 912, 32, gap=20)
        zera_chapas()
        cards = [cartao(i) for i in range(3)]
        zC = zona_px(120, 780, 1800, 1020, "títulos C (B7)")
        for v, p, cmp, ped, fan, t, fl in cards:
            clareira(cmp, (lambda ped=ped: clarPoly(ped.poly(), .25)))
        self.gat("quatro números entram")
        self.play(*[FadeOut(m) for m in sai], FadeIn(zC), *[a for v, p, cmp, ped, fan, t, fl in cards for a in (FadeIn(p), cresce_campo(cmp, 0.6), FadeIn(ped), FadeIn(fan), FadeIn(t, shift=0.06 * UP))], run_time=0.6)    # v4 R10
        self.remove(*sai)
        # final §2.6 (M4): os quadradinhos ficam na posição original até a frase de cada um
        self.play(caneta(fr[0], ritmo=0.25), caneta(fr[1], ritmo=0.25), caneta(d1, ritmo=0.25), caneta(d2, ritmo=0.25))
        vals = [TC(r"=2-(-1)=\V{3}", 360, 995, 36, "c"), TC(r"=1+0=\D{1}", 960, 995, 36, "c"), TC(r"=1-0=\Lm{1}\quad =2+(-1)=\Lm{1}", 1560, 995, 34, "c")]
        q4t = T("4 NÚMEROS ENTRAM, 4 MEDIDAS SAEM", 960, 245, 36, "center", BR)
        q4 = VGroup(placa7(q4t, 10, 5), q4t)
        self.gat("quatro medidas saem")
        self.play(*[caneta(m, ritmo=0.25) for m in vals])
        self.gat("e nada se perde no caminho")
        self.play(FadeIn(q4, shift=0.04 * DOWN), run_time=0.5)
        # (v3, holds) "um redemoinho, uma explosão e duas deformações": a moldura de cada cartão acende na sua cor (stroke direto, 0,3 s)
        for i, g in ((0, "um redemoinho"), (1, "uma explosão"), (2, "e duas deformações")):
            self.gat(g)
            self.play(cards[i][1][-1].animate.set_stroke(CART[i][2], 4 / 1.2, 1), run_time=0.3)
        # final §2.6 (M4): cada quadradinho faz a sua transformação UMA vez (≈ 1,0 s), na sua frase, e fica no estado final
        for i, g in ((0, "o redemoinho gira"), (1, "a explosão cresce"), (2, "a deformação estica de um lado")):
            v, p, cmp, ped, fan, t, fl = cards[i]
            self.gat(g)
            self.play(anda(ped, fl, 1.0, 1.0, nome=f"B7 {CART[i][1]} (M4)"))
            print(f"[B7] {CART[i][1]}: área 1,44 → {ped.area():.4f}")
        self.gat("e isso não é só matemática")
        self.play(*[c[1][-1].animate.set_stroke(MOLD_COR, 2 / 1.2, 0.38) for c in cards], run_time=0.3)
        # v3 (alvo 34): o atrito viscoso vem da deformação; o giro rígido não tem atrito
        for i, txt_ in ((2, "ATRITO VISCOSO AQUI"), (0, "SEM ATRITO VISCOSO")):         # v4: acima de cada cartão, 26 px, y = 288
            v, p, cmp, ped, fan, t, fl = cards[i]
            cor = CART[i][2]
            lg = legenda(txt_, CART[i][0] + 240, 288, cor, "center", 26)
            self.gat("o atrito viscoso vem da deformação" if i == 2 else "girando inteiro rígido")
            cmp.clear_updaters()
            clareira(cmp, (lambda ped=ped: clarPoly(ped.poly(), .25)))
            self.play(p[-1].animate.set_stroke(cor, 4 / 1.2, 1), FadeIn(lg, shift=0.04 * DOWN), run_time=0.4)
        self.ate(0.97)

        # ── B7-4 · volta ao gancho (alvo 35) ──
        self.an("B7-4")
        for _, _, c, _, _, _, _ in cards:
            c.clear_updaters()
        s0 = self.snap()
        zera_chapas()
        chA, znA = chapa_px(*LAY_A, nome="A (B7-4)"), zona_px(1080, 180, 1920, 1020, "coluna A (B7-4)")
        gch = palco_sela(nome="B7-4 gancho (x, −y)")
        pg = Pedaco(V, Q12).em(fl_sela, .55)
        fg = fantasma(V, Q12)
        ag = TP(r"\text{ÁREA } 1{,}44 \to 1{,}44", *canto_xy(V, 0, -1), 34, "c")
        st = {"extra": NADA}
        clareira(gch, lambda: ou(clarPoly(pg.poly(), .25), clarPoly(Q12, .15), clar28([(-1.1, -1.25, 1.1, -.75)]), st["extra"]))
        self.play(*[FadeOut(m) for m in s0], run_time=0.5)
        self.remove(*s0)
        self.play(FadeIn(chA), FadeIn(znA), cresce_campo(gch, 0.9), FadeIn(pg), FadeIn(fg), FadeIn(ag), run_time=0.9)
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
