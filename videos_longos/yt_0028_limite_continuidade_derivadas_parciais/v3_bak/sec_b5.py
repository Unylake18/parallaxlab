"""Lote PB5 · O ENGANO (v3: alvos 18–22; chapas A e B, gráficos no papel; B5-5 novo: o erro ÷ passo some × dobra). Da v2: alvos 14–17. B5-1 (layout A): G, as retas dos eixos e ∂G/∂x(0,0) = ∂G/∂y(0,0) = 0⃗; as diagonais acendem.
B5-2 (layout B): a previsão das parciais (um ponto) contra a imagem de verdade (o segmento [−1, 1]); A PREVISÃO ERRA FEIO (ALERTA).
B5-3 (layout B com gráficos, 120 px/u): ∂P/∂x(0, y) = 1 contra ∂/∂x(2xy/(x² + y²))(0, y) = 2/y; classe C¹ e Cʳ.
B5-4 (layout B, 200 px/u): a malhinha em volta de P e a sua imagem pela função original (as linhas voam e curvam); quase um paralelogramo."""
from v28 import *  # noqa: F401,F403
from sec_b1 import nomes_b

V = Vista(600, 540, 120)
DIAGS = [(1, 1), (1.5, 1.5), (2, 2), (-1, -1), (-1.5, -1.5), (-2, -2), (-1, 1), (-1.5, 1.5), (-2, 2), (1, -1), (1.5, -1.5), (2, -2)]


def paineis():
    return painel(*PAINEL_E[:2], 700, 560), painel(*PAINEL_D[:2], 700, 560)


class LoteB5(Base):
    ANTES = "DERIVADA PARCIAL"

    def corpo(self):
        # ── B5-1 · o engano (alvo 14) ──
        self.an("B5-1")
        self.secao("O ENGANO")
        zera_chapas()
        chA, znA = chapa_px(*LAY_A, nome="A (B5-1)"), zona_px(1080, 180, 1920, 1020, "coluna A (B5-1)")
        cmp = campo28(V, F_DIAG, prop=True, rmin=.3, skip=lambda X, Y: abs(X) < .05 or abs(Y) < .05, nome="B5 campo das diagonais")
        P = ponto7(V.c2p(0, 0), POS, 10, 11)
        self.play(FadeIn(chA), FadeIn(znA), cresce_campo(cmp, 1.0), FadeIn(P), run_time=1.0)
        lx = vlinha(V, [(-3.1, 0), (3.1, 0)], E1, 4).set_z_index(6)
        ly = vlinha(V, [(0, -3.1), (0, 3.1)], E2, 4).set_z_index(6)
        d1 = TC(r"\dfrac{\partial\G}{\dx}(0,0)=\vec 0", 1120, 290, 44)
        d2 = TC(r"\dfrac{\partial\G}{\dy}(0,0)=\vec 0", 1120, 410, 44)
        self.gat("pelo eixo horizontal")
        self.play(Create(lx), run_time=0.6)
        self.gat("derivada zero")
        self.play(caneta(d1, ritmo=0.3))
        self.gat("pelo vertical")
        self.play(Create(ly), run_time=0.6)
        self.play(caneta(d2, ritmo=0.3))
        so = legenda("AS PARCIAIS SÓ OLHAM DUAS RETAS", 1124, 505, GEO)
        nc = legenda("E G NEM É CONTÍNUO EM (0, 0)", 1124, 555, BR)
        tr = []
        for X, Y in DIAGS:
            s = next((a for a in cmp if abs(a._xy[0] - X) < 1e-6 and abs(a._xy[1] - Y) < 1e-6), None)
            if s is not None:
                tr.append(Transform(s, seta_prop(V, X, Y, F_DIAG(X, Y), .42, cor=CAMPO2, w=7, head=22)))
        self.gat("as duas existem")
        self.play(FadeIn(so, shift=0.06 * UP), LaggedStart(*tr, lag_ratio=0.08), run_time=1.4)
        self.gat("as duas são zero")
        self.play(FadeIn(nc, shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)

        # ── B5-2 · a previsão contra a imagem (alvo 15) ──
        self.an("B5-2")
        VE, VD = Vista(480, 540, 140), Vista(1440, 560, 140)
        a = .45
        sai = self.snap()
        zera_chapas()
        pE, pD = paineis()
        znB = zona_px(120, 900, 1800, 1020, "linha de baixo B (B5)")
        c2 = campo28(VE, F_DIAG, -2.25, 2.25, -1.75, 1.75, .5, prop=True, rmin=.3, skip=clar28([(-a, -a, a, a)]), nome="B5-2 G (painel)")
        nm = nomes_b()
        fb = TC(r"\dfrac{\partial\G}{\dx}(0,0)=\dfrac{\partial\G}{\dy}(0,0)=\vec 0", 480, 965, 34, "c")
        self.gat("se você confiasse só nelas")
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        self.play(FadeIn(pE), FadeIn(znB), cresce_campo(c2, 0.9), FadeIn(nm[0]), run_time=1.0)
        self.play(caneta(fb, ritmo=0.35))
        mal = VGroup(faixa(VE, [(-a, -a), (a, -a), (a, a), (-a, a)], FAIXA2, 2))
        for c in (-a, 0, a):
            mal.add(vlinha(VE, [(-a, c), (a, c)], E1, 3).set_z_index(3), vlinha(VE, [(c, -a), (c, a)], E2, 3).set_z_index(3))
        P2 = ponto7(VE.c2p(0, 0), POS, 8, 11)
        self.gat("um quadradinho em volta da origem")
        self.play(FadeIn(mal), FadeIn(P2), run_time=0.8)
        anelD, oD = anel7(VD.c2p(0, 0), GEO, 13), ponto7(VD.c2p(0, 0), GEO, 6, 10)
        prv = legenda("PREVISÃO DAS PARCIAIS: UM PONTO", 1440, canto_xy(VD, 0, .75)[1], GEO, "center", 26)
        self.gat("iria parar num ponto só")
        self.play(FadeIn(pD), FadeIn(nm[1]), FadeIn(anelD), FadeIn(oD), FadeIn(prv, shift=0.06 * UP), run_time=0.7)
        seg = vlinha(VD, [(-1, 0), (1, 0)], CAMPO2, 7).set_z_index(5)
        guarda(self, seg, PAINEL_D, "segmento")
        tk = [TC("-1", *canto_xy(VD, -1, -.35), 30, "c"), TC("1", *canto_xy(VD, 1, -.35), 30, "c")]
        img = legenda("IMAGEM DE VERDADE: O SEGMENTO TODO", 1440, canto_xy(VD, 0, -.75)[1], CAMPO2, "center", 26)
        self.gat("mas olha a imagem de verdade")
        self.play(GrowFromCenter(seg), run_time=1.2)
        self.play(caneta(tk[0], ritmo=0.5), caneta(tk[1], ritmo=0.5), FadeIn(img, shift=0.06 * UP))
        ef = legenda("A PREVISÃO ERRA FEIO", 1440, 962, ALERTA, "center", 30)
        self.gat("a previsão errou feio")
        self.play(FadeIn(ef, shift=0.06 * UP), run_time=0.5)
        tr = []
        for X, Y in [(sx * r_, sy * r_) for r_ in (.75, 1.25) for sx in (1, -1) for sy in (1, -1)]:
            s_ = next((q for q in c2 if abs(q._xy[0] - X) < 1e-6 and abs(q._xy[1] - Y) < 1e-6), None)
            if s_ is not None:
                tr.append(Transform(s_, seta_prop(VE, X, Y, F_DIAG(X, Y), .42, cor=CAMPO2, w=7, head=22)))
        self.gat("esconde tudo nas diagonais")
        self.play(LaggedStart(*tr, lag_ratio=0.1), run_time=1.2)
        self.ate(0.97)

        # ── B5-3 · o que faltou: os gráficos (alvo 16) ──
        self.an("B5-3")
        GE, GD = Vista(480, 540, 120), Vista(1440, 540, 120)
        origem_papel(GE, "B5-3 gráfico esquerdo (480, 540)")
        origem_papel(GD, "B5-3 gráfico direito (1440, 540)")
        sai = [m for m in self.snap() if m is not znB]
        zera_chapas()
        nm2 = nomes_b("NO EIXO VERTICAL: SEMPRE 1", "NO EIXO VERTICAL: 2/y, EXPLODE")
        nm2[1].become(legenda("NO EIXO VERTICAL: 2/y, EXPLODE", 1440, 868, GEO, "center", 28, up=False))

        def eixos_(g):
            return VGroup(seta7(g.c2p(-2.65, 0), g.c2p(2.75, 0), GEO, 2, 12), seta7(g.c2p(0, -2.15), g.c2p(0, 2.2), GEO, 2, 12)).set_z_index(2)
        eE, eD = eixos_(GE), eixos_(GD)
        lyE = TC(r"\Y", *canto_xy(GE, 2.75, -.25), 30, "c", caneta=False)
        lyD = TC(r"\Y", *canto_xy(GD, 2.75, -.25), 30, "c", caneta=False)
        self.gat("o que faltou")
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        self.play(Create(eE), Create(eD), FadeIn(lyE), FadeIn(lyD), FadeIn(nm2), run_time=0.8)
        tE = TC(r"\dfrac{\partial \Pp}{\dx}(0,\Y)=\cos 0=1", 480, 195, 32, "c")
        reta = vlinha(GE, [(-2.6, 1), (2.6, 1)], E1, 4).set_z_index(5)
        u1 = TC("1", *canto_xy(GE, -.2, 1.25), 30, "c", caneta=False)
        p1 = ponto7(GE.c2p(0, 1), E1, 7, 9)
        self.gat("no nosso campo a derivada na horizontal")
        self.play(caneta(tE, ritmo=0.4))
        self.play(Create(reta), FadeIn(u1), FadeIn(p1), run_time=1.5)
        tD = TC(r"\dfrac{\partial}{\dx}\!\left(\dfrac{2\X\Y}{\X^2+\Y^2}\right)\!(0,\Y)=\dfrac{2}{\Y}", 1440, 190, 30, "c")
        y0 = 2 / 2.05
        ramos = VGroup(*[vlinha(GD, [(sg * (y0 + (2.6 - y0) * i / 120), 2 / (sg * (y0 + (2.6 - y0) * i / 120))) for i in range(121)][::(-1 if sg < 0 else 1)], E1, 4).set_z_index(5)
                         for sg in (-1, 1)])
        guarda(self, ramos, PAINEL_D, "ramos de 2/y")
        sobe = TC(r"\uparrow\ \infty", *canto_xy(GD, .55, 2.0), 30, "c", caneta=False).set_color(E1)
        desce = TC(r"\downarrow\ -\infty", *canto_xy(GD, -.6, -1.95), 30, "c", caneta=False).set_color(E1)
        self.gat("no encrenqueiro")
        self.play(caneta(tD, ritmo=0.35))
        self.play(Create(ramos[0]), Create(ramos[1]), run_time=1.5)
        self.play(FadeIn(sobe), FadeIn(desce), run_time=0.5)
        p0 = ponto7(GD.c2p(0, 0), POS, 8, 10)
        l0 = TP(r"\text{vale }0\text{ na origem}", *canto_xy(GD, .95, -.45), 30)
        self.gat("na origem vale zero")
        self.play(FadeIn(p0, scale=0.5), FadeIn(l0), run_time=0.6)
        c1 = leg_mix(["CLASSE", r"$\mathrm{C}^{1}$", ": AS PARCIAIS EXISTEM E SÃO CONTÍNUAS"], 960, 958, WHITE_, "center", 34, up=True, bold=True, gap=6)
        self.gat("classe cê um")
        self.play(FadeIn(c1, shift=0.06 * UP), run_time=0.5)
        cr = leg_mix(["CLASSE", r"$\mathrm{C}^{r}$", ": O MESMO ATÉ A ORDEM", r"$r$"], 960, 1012, GEO, "center", 26, up=True, gap=6)
        self.gat("classe cê erre")
        self.play(FadeIn(cr, shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)

        # ── B5-4 · a malhinha e quase um paralelogramo (alvo 17; 200 px/u) ──
        self.an("B5-4")
        VE4, VD4 = Vista(480, 540, 200), Vista(1170, 560, 200)
        a = .5
        sai = [m for m in self.snap() if m is not znB]
        zera_chapas()
        pE4, pD4 = paineis()
        c4 = campo28(VE4, F_AULA, -1.5, 1.5, -1.25, 1.25, .5, rmin=0, mmax=3.5, ctx=True, skip=clar28([(-a, -a, a, a)], [(0, -.75, .05)]), nome="B5-4 campo da aula (200 px/u)")
        nm3 = nomes_b()
        cel = faixa(VE4, [(0, 0), (a, 0), (a, a), (0, a)], FAIXA2, 2)
        hs = [vlinha(VE4, [(-a, c), (a, c)], E1, 3).set_z_index(4) for c in (-a, 0, a)]
        vs = [vlinha(VE4, [(c, -a), (c, a)], E2, 3).set_z_index(4) for c in (-a, 0, a)]
        P4 = ponto7(VE4.c2p(0, 0), POS, 9, 11)
        lab = [TP(r"\Pt", *canto_xy(VE4, -.2, -.75), 30), TP(r"\h", *canto_xy(VE4, a / 2, -.75), 30), TP(r"\k", *canto_xy(VE4, -.75, a / 2), 30)]
        self.gat("e com ela vem a promessa")
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        self.play(FadeIn(pE4), cresce_campo(c4, 0.8), FadeIn(nm3[0]), FadeIn(cel), *[Create(l) for l in hs + vs], FadeIn(P4), *[FadeIn(l) for l in lab], run_time=1.0)
        N = 60
        cela = [F_AULA(a * i / N, 0) for i in range(N + 1)] + [F_AULA(a, a * i / N) for i in range(N + 1)] + \
               [F_AULA(a - a * i / N, a) for i in range(N + 1)] + [F_AULA(0, a - a * i / N) for i in range(N + 1)]
        celD = faixa(VD4, [tuple(p) for p in cela], FAIXA2, 2)
        hD = [vlinha(VD4, [tuple(F_AULA(-a + 2 * a * i / N, c)) for i in range(N + 1)], E1, 3).set_z_index(4) for c in (-a, 0, a)]
        vD = [vlinha(VD4, [tuple(F_AULA(c, -a + 2 * a * i / N)) for i in range(N + 1)], E2, 3).set_z_index(4) for c in (-a, 0, a)]
        pF = ponto7(VD4.c2p(1, 0), CAMPO2, 9, 11)
        lF = TP(r"\F(\Pt)", *canto_xy(VD4, .62, -.25), 30)
        self.gat("manda para a tela da chegada")
        self.play(FadeIn(pD4), FadeIn(nm3[1]), FadeIn(pF, scale=0.5), FadeIn(lF), TransformFromCopy(cel, celD, path_arc=-0.4), run_time=1.0)
        self.gat("as linhas horizontais viram curvas")
        self.play(*[TransformFromCopy(a_, b_, path_arc=-0.4) for a_, b_ in zip(hs, hD)], run_time=1.2)
        self.gat("e as verticais")
        self.play(*[TransformFromCopy(a_, b_, path_arc=-0.4) for a_, b_ in zip(vs, vD)], run_time=1.2)
        for m in hD + vD + [celD]:
            guarda(self, m, PAINEL_D, "malha imagem")          # R6 a partir de quando a malha pousa (o voo do painel esquerdo ao direito é a ação pedida)
        t0, k1, k2 = np.array([1.0, 0]), np.array([a, 2 * a]), np.array([-a, 0])
        par = vlinha(VD4, [tuple(t0), tuple(t0 + k1), tuple(t0 + k1 + k2), tuple(t0 + k2), tuple(t0)], BR, 2, dash=(6, 7)).set_z_index(6)
        s1 = seta7(VD4.c2p(*t0), VD4.c2p(*(t0 + k1)), E1, 7, 20).set_z_index(9)
        s2 = seta7(VD4.c2p(*t0), VD4.c2p(*(t0 + k2)), E2, 7, 20).set_z_index(9)
        guarda(self, s1, PAINEL_D, "h ∂F/∂x")
        l1 = TP(r"\h\,\dfrac{\partial\F}{\dx}", *canto_xy(VD4, 1.95, .95), 30)
        l2 = TP(r"\k\,\dfrac{\partial\F}{\dy}", *canto_xy(VD4, .3, .32), 30)
        qp = legenda("QUASE UM PARALELOGRAMO", 1440, 800, BR, "center", 26)
        err = []
        for c in (-a, 0, a):
            for i in range(N + 1):
                s_ = -a + 2 * a * i / N
                for (x_, y_) in ((s_, c), (c, s_)):
                    lin_ = t0 + x_ * np.array([1, 2]) + y_ * np.array([-1, 0])
                    err.append(np.linalg.norm(np.array(F_AULA(x_, y_)) - lin_))
        print(f"[B5-4] malha ±{a}: maior distância da imagem ao paralelogramo das colunas = {max(err):.3f} u")
        self.gat("quase um paralelogramo")
        self.play(Create(par), GrowArrow(s1), GrowArrow(s2), FadeIn(l1), FadeIn(l2), FadeIn(qp), run_time=1.0)
        ap = TC(r"\F(\Pt+H)\approx\F(\Pt)+\h\,\dfrac{\partial\F}{\dx}+\k\,\dfrac{\partial\F}{\dy}", 960, 975, 38, "c")
        self.gat("escrito")
        self.play(caneta(ap, ritmo=0.45))
        cl = t0 + k1 + k2
        cv = np.array(F_AULA(a, a), float)
        er = seta7(VD4.c2p(*cl), VD4.c2p(*cv), ALERTA, 5, 16).set_z_index(12)
        ler = TP(r"\text{erro}", *canto_xy(VD4, (cl[0] + cv[0]) / 2 - .35, (cl[1] + cv[1]) / 2 + .12), 30)
        print(f"[B5-4] erro no canto da célula (h = k = 0,5): {np.linalg.norm(cv - cl):.3f} u")
        self.gat("com um erro que some")
        self.play(GrowArrow(er), FadeIn(ler), run_time=0.8)
        # ── v3 · B5-5: o erro some (nosso campo) × o erro dobra (encrenqueiro) (alvo 22) ──
        def erro_passo(Fv, J_, a_):
            th = np.linspace(0, 2 * PI, 721)
            v0 = np.array(Fv(0.0, 0.0), float)
            return max(np.linalg.norm(np.array(Fv(a_ * math.cos(t), a_ * math.sin(t)), float) - v0 - J_ @ np.array([a_ * math.cos(t), a_ * math.sin(t)])) / a_ for t in th)
        e_nosso = [erro_passo(F_AULA, JA, a_) for a_ in (.5, .25, .125)]
        e_enc = [erro_passo(F_DIAG, np.zeros((2, 2)), a_) for a_ in (.5, .25, .125)]
        print(f"[B5-5] erro/passo — nosso campo: {[round(x, 3) for x in e_nosso]}; encrenqueiro: {[round(x, 3) for x in e_enc]} (passo 0,5 · 0,25 · 0,125)")
        conteudo = [m for m in self.snap() if m not in (pE4, pD4, znB, nm3[0], nm3[1], ap)]
        nE = leg_mix(["NOSSO CAMPO: CLASSE", r"$\mathrm{C}^{1}$"], 480, 868, GEO, "center", 28, up=True, gap=6)
        self.gat("o nosso campo feito de senos e cossenos")
        self.play(*[FadeOut(m) for m in conteudo], FadeOut(nm3[0]), FadeIn(nE), run_time=0.6)
        self.remove(*conteudo, nm3[0])
        nD = leg_mix(["O ENCRENQUEIRO: NÃO É", r"$\mathrm{C}^{1}$"], 1440, 868, GEO, "center", 28, up=True, gap=6)
        self.gat("o encrenqueiro não")
        self.play(FadeOut(nm3[1]), FadeIn(nD), run_time=0.5)
        self.remove(nm3[1])
        tE = leg_mix(["ERRO", r"$\div$", "PASSO: CAI PELA METADE"], 480, 300, CAMPO2, "center", 28, up=True, gap=6)
        tD = leg_mix(["ERRO", r"$\div$", "PASSO: DOBRA", r"$\to\infty$"], 1440, 300, ALERTA, "center", 28, up=True, gap=6)
        fe = TC(r"\dfrac{\|\text{erro}\|}{\|H\|}\to 0\ \ \text{quando}\ \ H\to \vec 0", 960, 960, 40, "c")
        self.gat("dividindo o erro pelo passo")
        self.play(FadeOut(ap), FadeIn(tE, shift=0.05 * UP), FadeIn(tD, shift=0.05 * UP), run_time=0.5)
        self.remove(ap)
        self.play(caneta(fe, ritmo=0.4))
        VL = Vista(480, 640, 140)
        bL = vlinha(VL, [(-2.1, 0), (2.1, 0)], GEO, 2).set_z_index(4)
        self.gat("quando o passo cai pela metade")
        self.play(Create(bL), run_time=0.4)
        for i_, (a_, rs, r_) in enumerate(((.5, "0{,}33", .33), (.25, "0{,}15", .145), (.125, "0{,}07", .068))):
            X_ = -1.4 + 1.4 * i_
            sa = seta7(VL.c2p(X_, 0), VL.c2p(X_, r_ * 4.2), CAMPO2, 8, 24).set_z_index(9)
            guarda(self, sa, PAINEL_E, "seta erro÷passo")
            lpa = TC(r"\text{passo }" + str(a_).replace(".", "{,}"), *canto_xy(VL, X_, -.4), 28, "c")
            lva = TP(rs, *canto_xy(VL, X_, r_ * 4.2 + .35), 32)
            self.play(GrowArrow(sa), caneta(lpa, ritmo=0.25), FadeIn(lva), run_time=0.6)
        z0 = TC(r"\to 0", 480, 345, 30, "c")
        z0.set_color(CAMPO2)
        self.gat("e vai para zero")
        self.play(caneta(z0, ritmo=0.5))
        VR = Vista(1160, 540, 70)
        self.gat("ela dobra")
        for i_, (a_, r_) in enumerate(((.5, 2), (.25, 4), (.125, 8))):
            Y_ = 2.2 - 2.2 * i_
            sa = seta7(VR.c2p(0, Y_), VR.c2p(r_, Y_), ALERTA, 8, 24).set_z_index(9)
            guarda(self, sa, PAINEL_D, "seta erro÷passo (encrenqueiro)")
            lpa = TC(r"\text{passo }" + str(a_).replace(".", "{,}"), *canto_xy(VR, 1.3, Y_ + .75), 28, "c")
            lva = TP(str(r_), *canto_xy(VR, r_ + .6, Y_), 32)
            self.play(GrowArrow(sa), caneta(lpa, ritmo=0.25), FadeIn(lva), run_time=0.6)
        self.ate(0.97)
        self.sai_fim()
