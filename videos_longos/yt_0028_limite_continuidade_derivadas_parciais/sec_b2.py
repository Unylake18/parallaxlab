"""v4: fundo violeta + grade do eixo; 144 px/u. Lote PB2 · QUANDO O LIMITE NÃO EXISTE (v3: chapas A e B encaixadas; B2-4 novo com o campo K = (x²y/(x⁴ + y²), 0), alvo 10. Da v2: alvos 06 e 07; B2-3/B2-4 no layout B com a forma polar G = (sen 2θ, 0)). Da v1: layout A, alvo 04. Campo G = (2xy/(x² + y²), 0) com setas PROPORCIONAIS (nada sobre os eixos).
Três caminhos GEO tracejados, um por vez, cada um com a sua clareira; o ponto laranja anda UMA vez carregando a sua seta (0⃗, (1, 0), (−1, 0))."""
from v28 import *  # noqa: F401,F403

V = Vista(600, 540, 120)
PONTOS = [(1.25, 0.0), (1.1, 1.1), (-1.1, 1.1)]
INICIOS = [(2.8, 0.0), (2.55, 2.55), (-2.55, 2.55)]
SEGS = [((3, 0), (.3, 0)), ((2.7, 2.7), (.22, .22)), ((-2.7, 2.7), (-.22, .22))]
RET_LBL = [(1.0, -.75, 2.0, -.3), (1.3, 1.25, 2.6, 1.75), (-2.6, 1.25, -1.3, 1.75)]
LBL = [(r"\vec 0", (1.5, -.5)), (r"(1,\ 0)", (1.95, 1.5)), (r"(-1,\ 0)", (-1.95, 1.5))]


def seta_g(p):
    g = F_DIAG(*p)
    if math.hypot(*g) < 1e-9:
        return None
    return seta7(V.c2p(p[0] - .1, p[1]), V.c2p(p[0] - .1 + g[0] * .42 * 1.15, p[1]), CAMPO2, 8, 24).set_z_index(9)


class LoteB2(Base):
    ANTES = "CHEGAR PERTO"

    def corpo(self):
        # ── B2-1 ──
        self.an("B2-1")
        self.secao("QUANDO O LIMITE NÃO EXISTE")
        zera_chapas()
        chA, znA = chapa_px(*LAY_A, nome="A (B2)"), zona_px(1080, 180, 1920, 1020, "coluna A (B2)")
        cmp = campo28(V, F_DIAG, prop=True, rmin=.3, nome="B2 campo das diagonais (proporcional)")
        o = ponto7(V.c2p(0, 0), GEO, 5)
        ativos = []                                   # testes de clareira dos caminhos já desenhados
        st = {"p": None}
        clareira(cmp, lambda: ou(*ativos, (clar28([], [(*st["p"], .15)]) if st["p"] else None)))
        self.play(FadeIn(chA), FadeIn(znA), onda(cmp, 1.0), FadeIn(o), run_time=1.0)   # final M1: onda
        fG = TC(r"\G = \left(\dfrac{2\X\Y}{\X^2+\Y^2},\ 0\right)", 1120, 320, 48)
        self.gat("campo encrenqueiro")
        self.play(caneta(fG))
        self.ate(0.97)

        # ── B2-2 · três caminhos ──
        self.an("B2-2")
        frases = ["pelo eixo horizontal", "pela diagonal de subida", "pela outra"]
        for i, fr in enumerate(frases):
            cam = vlinha(V, list(SEGS[i]), GEO, 3, dash=(10, 9))
            a, b = np.array(INICIOS[i]), np.array(PONTOS[i])
            pt = ponto7(V.c2p(*a), POS, 9, 10)
            st["p"] = tuple(a)
            sg = seta_g(tuple(a))
            self.gat(fr)
            ativos.append(clarSeg([SEGS[i]], .2))
            self.play(Create(cam), FadeIn(pt, scale=0.5), *([GrowArrow(sg)] if sg else []), run_time=0.5)

            def anda_(m, al, a=a, b=b, sg=sg):
                p = a + (b - a) * smooth(al)
                st["p"] = (float(p[0]), float(p[1]))
                pt.move_to(V.c2p(*p))
                if sg is not None:
                    sg.become(seta_g(st["p"]))
            self.play(UpdateFromAlphaFunc(pt, anda_), run_time=1.1)       # final (sync)
            ativos.append(clar28([RET_LBL[i]], [(*PONTOS[i], .15)]))
            st["p"] = None
            s, xy = LBL[i]
            self.play(FadeIn(TP(s, *canto_xy(V, *xy), 36)), run_time=0.4)
        print(f"[G] nas três retas: {[tuple(round(v, 3) for v in F_DIAG(*p)) for p in PONTOS]}")
        nr = legenda("NA RETA y = m x:", 1124, 450, GEO, up=False)
        fm = TC(r"\G = \left(\dfrac{2m}{1+m^2},\ 0\right)", 1120, 530, 48)
        self.gat("numa reta qualquer")
        self.play(FadeIn(nr, shift=0.06 * UP), run_time=0.5)
        self.play(caneta(fm, ritmo=0.45))
        ml = TC(r"m=0 \to 0\quad m=1 \to 1\quad m=-1 \to -1", 1120, 650, 40)
        self.gat("três caminhos três resultados diferentes")     # final (sync): os três valores entram na frase dos três resultados
        self.play(caneta(ml, ritmo=0.35))

        ne = VGroup(T("NÃO EXISTE O LIMITE", 1120, 780, 40, cor=BR), T("EM (0, 0)", 1120, 830, 40, cor=BR))
        self.gat("muda o valor")
        self.play(FadeIn(ne, shift=0.08 * UP), run_time=0.6)
        self.ate(0.97)
        cmp.clear_updaters()

        # ── B2-3 · a forma polar: G = (sen 2θ, 0); a ponta varre [−1, 1] (alvo 07; layout B) ──
        self.an("B2-3")
        VE, VD = VB(LAY_BE, 480, 540, 140), VB(LAY_BD, 1440, 560, 140)      # v4: (480, 540) e (1440, 576), 144 px/u
        R, TH0 = .38, PI / 8
        sai = self.snap()
        zera_chapas()
        pE, pD = painel(130, 260, 700, 560, v=VE), painel(1090, 260, 700, 560, v=VD)
        znB = zona_px(120, 900, 1800, 1020, "linha de baixo B (B2)")
        st2 = {"th": TH0}
        Xp = lambda: (R * math.cos(st2["th"]), R * math.sin(st2["th"]))
        c2 = campo28(VE, F_DIAG, -2.25, 2.25, -1.75, 1.75, .5, prop=True, rmin=.3, nome="B2-3 G (painel)")
        clareira(c2, lambda: ou(clar28([], [(0, 0, .6)]), clar28([(Xp()[0] - .3, Xp()[1] + .1, Xp()[0] + .2, Xp()[1] + .5)])))
        from sec_b1 import nomes_b
        nm = nomes_b()
        self.gat("e dá para ver isso")
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        self.play(FadeIn(pE), FadeIn(znB), cresce_campo(c2, 0.9), FadeIn(nm[0]), run_time=1.0)
        pol = TP(r"\dfrac{2\X\Y}{\X^2+\Y^2}=\dfrac{2r^2\cos\theta\,\sen\theta}{r^2}=\sen 2\theta", 960, 128, 34, "c", caneta=True)       # v4: acima da moldura (como a do K)
        self.gat("em coordenadas polares")
        self.play(FadeIn(pol[0]), caneta(pol.f, ritmo=0.45))
        gp = TC(r"\G=(\sen 2\theta,\ 0)", 480, 955, 40, "c")
        self.gat("o seno do dobro do ângulo")
        self.play(caneta(gp, ritmo=0.6))
        circ_ = vcirc(VE, R, POS, 3).set_z_index(6)
        o = ponto7(VE.c2p(0, 0), GEO, 5)
        Xd = ponto7(VE.c2p(*Xp()), POS, 7, 10)

        def sX():
            g = F_DIAG(*Xp())
            p = Xp()
            if abs(g[0]) * .6 * 140 < 4:
                return VMobject()
            return seta7(VE.c2p(*p), VE.c2p(p[0] + g[0] * .6, p[1]), CAMPO2, 6, 18).set_z_index(9)
        aX = sX()
        arco = vlinha(VE, circ_pts(.17, (0, 0), 40, 0, TH0), BR, 2).set_z_index(6)
        lth = TC(r"\theta", *canto_xy(VE, .27, .03), 26, "c", caneta=False)
        lX = segue(TP(r"\Xp", *canto_xy(VE, Xp()[0] - .05, Xp()[1] + .3), 28), lambda: canto_xy(VE, Xp()[0] - .05, Xp()[1] + .3))
        oD = ponto7(VD.c2p(0, 0), GEO, 6)
        ext = {"a": math.sin(2 * TH0), "b": math.sin(2 * TH0)}

        def sT():
            g = F_DIAG(*Xp())
            if abs(g[0]) * 140 < 4:
                return VMobject()
            return seta7(VD.c2p(0, 0), VD.c2p(g[0], 0), CAMPO, 5, 20).set_z_index(9)
        aT = sT()
        seg = vlinha(VD, [(ext["a"], 0), (ext["b"] + 1e-3, 0)], CAMPO2, 6).set_z_index(5)
        guarda(self, seg, PAINEL_D, "segmento")
        guarda(self, aT, PAINEL_D, "seta da ponta")
        self.gat("num círculo minúsculo")
        self.play(FadeIn(pD), FadeIn(nm[1]), Create(circ_), FadeIn(o), FadeIn(Xd, scale=0.5), FadeIn(aX), FadeIn(lX), Create(arco), FadeIn(lth), FadeIn(oD), FadeIn(aT), FadeIn(seg), run_time=0.9)

        def volta_(m, a):
            st2["th"] = TH0 + 2 * PI * a
            g = F_DIAG(*Xp())[0]
            ext["a"], ext["b"] = min(ext["a"], g), max(ext["b"], g)
            Xd.move_to(VE.c2p(*Xp()))
            aX.become(sX())
            aT.become(sT())
            seg.set_points_as_corners([VD.c2p(ext["a"], 0), VD.c2p(ext["b"] + 1e-3, 0)])
        self.play(FadeOut(arco), FadeOut(lth), run_time=0.3)
        self.remove(arco, lth)
        self.gat("a ponta da seta varre o segmento")
        self.play(UpdateFromAlphaFunc(Xd, volta_), run_time=4.0, rate_func=linear)
        ext["a"], ext["b"] = -1.0, 1.0           # o sup exato (sen 2θ = ±1 em θ = ±π/4) entre dois quadros
        seg.set_points_as_corners([VD.c2p(-1, 0), VD.c2p(1, 0)])
        print(f"[G] uma volta em r = {R}: a ponta varreu [{ext['a']:.4f}; {ext['b']:.4f}]")
        tk = [TC("-1", *canto_xy(VD, -1, -.35), 30, "c"), TC("1", *canto_xy(VD, 1, -.35), 30, "c")]
        self.play(caneta(tk[0], ritmo=0.5), caneta(tk[1], ritmo=0.5))
        self.ate(0.97)

        # ── B2-4 · o desafio perdido ──
        self.an("B2-4")
        Lc = ValueTracker(.3)
        EPS = .5
        pLc = ponto7(VD.c2p(.3, 0), CAMPO, 8, 11)
        pLc.add_updater(lambda m: m.move_to(VD.c2p(Lc.get_value(), 0)))
        lL = segue(TP(r"\Lv\,?", *canto_xy(VD, .3, .35), 30), lambda: canto_xy(VD, Lc.get_value(), .35))
        self.gat("escolhe um alvo qualquer")
        self.play(FadeIn(pLc, scale=0.5), FadeIn(lL), run_time=0.6)
        dE = vcirc(VD, EPS, CAMPO2, 3, c=(.3, 0)).set_z_index(6)
        dE.add_updater(lambda m: m.become(vcirc(VD, EPS, CAMPO2, 3, c=(Lc.get_value(), 0)).set_z_index(6)))
        lE = segue(TP(r"\eps=0{,}5", *canto_xy(VD, .45, -.8), 30), lambda: canto_xy(VD, Lc.get_value() + .15, -.8))

        def alertas():
            c = Lc.get_value()
            g = VGroup()
            if c - EPS > -1:
                g.add(vlinha(VD, [(-1, 0), (c - EPS, 0)], ALERTA, 6).set_z_index(5.5))
            if c + EPS < 1:
                g.add(vlinha(VD, [(c + EPS, 0), (1, 0)], ALERTA, 6).set_z_index(5.5))
            return g
        al = alertas()
        al.add_updater(lambda m: m.become(alertas()))
        guarda(self, dE, PAINEL_D, "disco ε")
        self.gat("um épsilon de meio")
        self.play(Create(dE), FadeIn(lE), FadeIn(al), run_time=0.9)
        nl = legenda("A PONTA VARRE DE −1 A 1: NENHUM L SERVE", 1440, 962, BR, "center", 28)
        self.gat("não cabe")
        self.play(FadeIn(nl, shift=0.06 * UP), run_time=0.5)
        self.gat("seja qual for o alvo")
        self.play(Lc.animate.set_value(-.3), run_time=1.3)
        self.play(Lc.animate.set_value(.3), run_time=1.3)
        # ── v3 · "dá para chegar por uma curva": o campo K (alvo 10) ──
        for m in (pLc, lL, dE, lE, al, lX, c2):
            m.clear_updaters()
        Kf = lambda X, Y: (0.0, 0.0) if X ** 4 + Y * Y < 1e-12 else (X * X * Y / (X ** 4 + Y * Y), 0.0)
        K2 = lambda X, Y: (2 * Kf(X, Y)[0], 0.0)            # setas em escala × 2 (|K| ≤ 1/2)
        sai = [m for m in self.snap() if m not in (pE, pD, znB, nm, nm[0], nm[1])]
        kt = TP(r"\textcolor{cc}{\vec K}=\left(\dfrac{\X^2\Y}{\X^4+\Y^2},\ 0\right)", 960, 128, 34, "c", caneta=True)     # v4: acima da moldura
        segs = [((-1.75, -1.75), (1.75, 1.75)), ((-1.75, 1.75), (1.75, -1.75)), ((-2.2, 0), (2.2, 0))]
        ck = campo28(VE, K2, -2.25, 2.25, -1.75, 1.75, .5, prop=True, rmin=.3, ctx=True,
                     skip=ou(clarSeg(segs, .15), lambda X, Y: abs(Y - X * X) < .3 and abs(X) < 1.4, clar28([(-2.3, .75, -1.4, 1.15)])), nome="B2-4 K (contexto, × 2)")
        retas = VGroup(*[vlinha(VE, list(sg), GEO, 2.5, dash=(9, 8)).set_z_index(4) for sg in segs])
        lmx = TP(r"\Y=m\X", *canto_xy(VE, 1.85, 1.45), 30)
        self.gat("e fica um cuidado")
        VK = VD
        base = vlinha(VK, [(-1, 0), (1, 0)], GEO, 2).set_z_index(4)
        o0 = ponto7(VK.c2p(0, 0), GEO, 8, 8)
        tks = [TC("0", *canto_xy(VK, 0, -.38), 30, "c"), TC(r"\tfrac12", *canto_xy(VK, .5, -.42), 30, "c"),
               TC("-1", *canto_xy(VK, -1, -.38), 30, "c"), TC("1", *canto_xy(VK, 1, -.38), 30, "c")]
        self.play(*[FadeOut(m) for m in sai], cresce_campo(ck, 0.8), Create(retas), FadeIn(lmx), FadeIn(base), FadeIn(o0), run_time=0.9)
        self.remove(*sai)
        self.play(*[caneta(t, ritmo=0.4) for t in tks])
        sk = {"X": (1.2, 1.2)}
        Xk = ponto7(VE.c2p(*sk["X"]), POS, 8, 11)

        def setaX():
            k = Kf(*sk["X"])[0]
            if abs(k) * 140 < 4:
                return VMobject()
            return seta7(VE.c2p(*sk["X"]), VE.c2p(sk["X"][0] + k, sk["X"][1]), CAMPO2, 6, 18).set_z_index(12)

        def setaR():
            k = Kf(*sk["X"])[0]
            if abs(k) * 140 < 4:
                return VMobject()
            return seta7(VK.c2p(0, 0), VK.c2p(k, 0), CAMPO2, 7, 22).set_z_index(10)
        aK, aR = setaX(), setaR()
        pR = ponto7(VK.c2p(Kf(*sk["X"])[0], 0), POS, 8, 11)
        lXk = TP(r"\Xp", *canto_xy(VE, sk["X"][0] - .13, sk["X"][1] + .36), 28)
        lXk.add_updater(lambda m: m.move_to(PX(*canto_xy(VE, sk["X"][0] - .13, sk["X"][1] + .36))))      # posição absoluta (o X salta entre as retas)
        lr = legenda("PELAS RETAS: A PONTA VAI PARA ZERO", 1440, canto_xy(VK, 0, 1.25)[1], GEO, "center", 26)
        guarda(self, aR, PAINEL_D, "seta K(X)")

        def anda_k(m, a, ini, fim, curva):
            x = ini + (fim - ini) * smooth(a)
            sk["X"] = (x, curva(x))
            Xk.move_to(VE.c2p(*sk["X"]))
            aK.become(setaX())
            aR.become(setaR())
            pR.move_to(VK.c2p(Kf(*sk["X"])[0], 0))
        self.gat("todas as retas darem o mesmo valor")
        sk["X"] = (-1.2, 1.2)
        Xk.move_to(VE.c2p(*sk["X"]))
        aK.become(setaX())
        aR.become(setaR())
        pR.move_to(VK.c2p(Kf(*sk["X"])[0], 0))
        self.play(FadeIn(Xk, scale=0.5), FadeIn(aK), FadeIn(aR), FadeIn(pR), FadeIn(lXk), run_time=0.9)
        self.play(UpdateFromAlphaFunc(Xk, lambda m, a: anda_k(m, a, -1.2, -.05, lambda x: -x)), run_time=2.0)
        par = vlinha(VE, [(-1.3 + 2.6 * i / 120, (-1.3 + 2.6 * i / 120) ** 2) for i in range(121)], POS, 4).set_z_index(5)
        lpar = TP(r"\Y=\X^2", *canto_xy(VE, -1.85, .95), 30)
        self.gat("chegar por uma curva")
        self.play(Create(par), FadeIn(lpar), run_time=0.8)
        self.gat("olha este campo")
        self.play(FadeIn(kt[0]), caneta(kt.f, ritmo=0.3))
        self.gat("por qualquer reta")
        self.play(UpdateFromAlphaFunc(Xk, lambda m, a: anda_k(m, a, 1.2, .05, lambda x: x)), FadeIn(lr), run_time=2.0)
        print(f"[B2-4] K na reta y = x em x = 0,05: {Kf(.05, .05)[0]:.4f} (→ 0); na parábola: {Kf(.6, .36)[0]:.4f} (= 1/2)")
        lp = legenda("PELA PARÁBOLA: FICA EM 1/2", 1440, canto_xy(VK, 0, .85)[1], POS, "center", 26)
        self.gat("pela parábola")
        self.play(UpdateFromAlphaFunc(Xk, lambda m, a: anda_k(m, a, 1.3, .15, lambda x: x * x)), FadeIn(lp), run_time=2.5)
        fim = legenda("TODA RETA DÁ 0, A CURVA DÁ 1/2: O LIMITE NÃO EXISTE", 960, 962, BR, "center", 30)
        self.gat("também não tem limite")
        self.play(FadeIn(fim, shift=0.05 * UP), run_time=0.5)
        lXk.clear_updaters()
        self.ate(0.97)
        for m in (pLc, lL, dE, lE, al, lX, c2):
            m.clear_updaters()
        self.sai_fim()
