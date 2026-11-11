"""Lote PB2 · QUANDO O LIMITE NÃO EXISTE (v2: alvos 06 e 07; B2-3/B2-4 no layout B com a forma polar G = (sen 2θ, 0)). Da v1: layout A, alvo 04. Campo G = (2xy/(x² + y²), 0) com setas PROPORCIONAIS (nada sobre os eixos).
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
        cmp = campo28(V, F_DIAG, prop=True, rmin=.3, nome="B2 campo das diagonais (proporcional)")
        o = ponto7(V.c2p(0, 0), GEO, 5)
        ativos = []                                   # testes de clareira dos caminhos já desenhados
        st = {"p": None}
        clareira(cmp, lambda: ou(*ativos, (clar28([], [(*st["p"], .15)]) if st["p"] else None)))
        self.play(cresce_campo(cmp, 1.0), FadeIn(o), run_time=1.0)
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
            self.play(UpdateFromAlphaFunc(pt, anda_), run_time=1.6)
            ativos.append(clar28([RET_LBL[i]], [(*PONTOS[i], .15)]))
            st["p"] = None
            s, xy = LBL[i]
            self.play(FadeIn(TP(s, *canto_xy(V, *xy), 36)), run_time=0.5)
        print(f"[G] nas três retas: {[tuple(round(v, 3) for v in F_DIAG(*p)) for p in PONTOS]}")
        nr = legenda("NA RETA y = m x:", 1124, 450, GEO, up=False)
        fm = TC(r"\G = \left(\dfrac{2m}{1+m^2},\ 0\right)", 1120, 530, 48)
        self.gat("numa reta qualquer")
        self.play(FadeIn(nr, shift=0.06 * UP), run_time=0.5)
        self.play(caneta(fm))
        ml = TC(r"m=0 \to 0\quad m=1 \to 1\quad m=-1 \to -1", 1120, 650, 40)
        self.gat("muda a reta")
        self.play(caneta(ml, ritmo=0.5))
        self.ate(0.97)

        ne = VGroup(T("NÃO EXISTE O LIMITE", 1120, 780, 40, cor=BR), T("EM (0, 0)", 1120, 830, 40, cor=BR))
        self.gat("muda o valor")
        self.play(FadeIn(ne, shift=0.08 * UP), run_time=0.6)
        self.ate(0.97)
        cmp.clear_updaters()

        # ── B2-3 · a forma polar: G = (sen 2θ, 0); a ponta varre [−1, 1] (alvo 07; layout B) ──
        self.an("B2-3")
        VE, VD = Vista(480, 540, 140), Vista(1440, 560, 140)
        R, TH0 = .38, PI / 8
        sai = self.snap()
        pE, pD = painel(*PAINEL_E[:2], 700, 560), painel(*PAINEL_D[:2], 700, 560)
        st2 = {"th": TH0}
        Xp = lambda: (R * math.cos(st2["th"]), R * math.sin(st2["th"]))
        c2 = campo28(VE, F_DIAG, -2.25, 2.25, -1.75, 1.75, .5, prop=True, rmin=.3, nome="B2-3 G (painel)")
        clareira(c2, lambda: ou(clar28([], [(0, 0, .6)]), clar28([(Xp()[0] - .3, Xp()[1] + .1, Xp()[0] + .2, Xp()[1] + .5)])))
        from sec_b1 import nomes_b
        nm = nomes_b()
        self.gat("e dá para ver isso")
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        self.play(Create(pE), Create(pD), cresce_campo(c2, 0.9), FadeIn(nm), run_time=1.0)
        pol = TC(r"\dfrac{2\X\Y}{\X^2+\Y^2}=\dfrac{2r^2\cos\theta\,\sen\theta}{r^2}=\sen 2\theta", 960, 195, 38, "c")
        self.gat("em coordenadas polares")
        self.play(caneta(pol, ritmo=0.45))
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
        self.play(Create(circ_), FadeIn(o), FadeIn(Xd, scale=0.5), FadeIn(aX), FadeIn(lX), Create(arco), FadeIn(lth), FadeIn(oD), FadeIn(aT), FadeIn(seg), run_time=0.9)

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
        self.ate(0.97)
        for m in (pLc, lL, dE, lE, al, lX, c2):
            m.clear_updaters()
        self.sai_fim()
