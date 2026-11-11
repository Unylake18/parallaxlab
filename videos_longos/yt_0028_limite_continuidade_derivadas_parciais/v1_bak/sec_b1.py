"""Lote PB1 · CHEGAR PERTO (layout B; alvos 02 e 03). Painéis 700×560, 1 u = 140 px nos dois. Esquerda: campo da aula em contexto e P; direita: origem
comum e F(P) = (1, 0). X sai de (1,4; 0,9) e anda UMA vez por um arco até a borda do disco δ; disco ε = 1 e δ = 0,41; X dá UMA volta no disco δ e a
ponta desenha a curva das pontas F(P + δ(cos θ, sen θ)) (exata); ε = 0,5 ⇒ δ = 0,21 (TransformByGlyphMap); a definição; o atalho por componentes."""
from v28 import *  # noqa: F401,F403

VE, VD = Vista(480, 540, 140), Vista(1250, 560, 140)
ANG = 0.9                                   # ângulo de X no disco δ (sb28)
X_INI = (1.4, 0.9)


def tip_curva(d, n=240):
    th = np.linspace(0, 2 * PI, n + 1)
    a = F_AULA(d * np.cos(th), d * np.sin(th))
    return list(zip(a[0], a[1]))


def nomes_b():
    return VGroup(legenda("ONDE VOCÊ ANDA", 480, 868, GEO, "center", 28), legenda("ONDE A SETA CHEGA", 1440, 868, GEO, "center", 28))


class LoteB1(Base):
    ANTES = None

    def corpo(self):
        # ── B1-1 · duas telas ──
        self.an("B1-1")
        self.secao("CHEGAR PERTO")
        pE, pD = painel(130, 260, 700, 560), painel(1090, 260, 700, 560)
        self.play(Create(pE), Create(pD), run_time=0.8)
        st = {"X": None, "d": None}
        cmp = campo28(VE, F_AULA, -2.25, 2.25, -1.75, 1.75, .5, rmin=0, mmax=3.5, ctx=True, nome="B1 campo da aula (contexto)")

        def teste():
            fs = [clar28([(-.85, -.5, -.45, .15)], [(0, 0, max(st["d"] or 0, .2) + .1)])]
            if st["X"] is not None:
                X0, X1 = st["X"]
                f = F_AULA(X0, X1)
                m = math.hypot(*f)
                L = .84 * .5 * (.4 + .6 * min(1, m / 3.5))
                fs.append(clar28([(X0 - .2, X1 + .2, X0 + .4, X1 + .62)], [(X0, X1, .1)]))
                fs.append(clarSeg([((X0, X1), (X0 + f[0] / m * L, X1 + f[1] / m * L))], .25))
            return ou(*fs)
        clareira(cmp, teste)
        P = ponto7(VE.c2p(0, 0), POS, 9)
        lP = TP(r"\Pt", *canto_xy(VE, -.25, -.3), 36)
        self.gat("na da esquerda está o campo")
        self.play(cresce_campo(cmp, 1.0), FadeIn(P, scale=0.5), FadeIn(lP), run_time=1.0)
        nm = nomes_b()
        self.gat("é ali que você anda")
        self.play(FadeIn(nm[0], shift=0.06 * UP), run_time=0.5)
        org = ponto7(VD.c2p(0, 0), GEO, 6)
        sFP = seta7(VD.c2p(0, 0), VD.c2p(1, 0), CAMPO2, 7, 24).set_z_index(9)
        lFP = TP(r"\F(\Pt)", *canto_xy(VD, .5, -.32), 34)
        self.gat("na da direita")
        self.play(FadeIn(org, scale=0.5), GrowArrow(sFP), FadeIn(lFP), run_time=0.8)
        self.gat("só onde a ponta dela chega")
        self.play(FadeIn(nm[1], shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)

        # ── B1-2 · X chega perto; ε e δ ──
        self.an("B1-2")
        d0 = 0.41
        X_FIM = (d0 * math.cos(ANG), d0 * math.sin(ANG))
        st["X"] = X_INI
        Xd = ponto7(VE.c2p(*X_INI), POS, 6, 10)

        def sX():
            X0, X1 = st["X"]
            f = F_AULA(X0, X1)
            m = math.hypot(*f)
            L = .84 * .5 * (.4 + .6 * min(1, m / 3.5))
            return seta7(VE.c2p(X0, X1), VE.c2p(X0 + f[0] / m * L, X1 + f[1] / m * L), CAMPO2, 7, 22).set_z_index(9)

        def sFX():
            f = F_AULA(*st["X"])
            return seta7(VD.c2p(0, 0), VD.c2p(*f), CAMPO, 6, 22).set_z_index(8)
        aX, aFX = sX(), sFX()
        lX = TP(r"\Xp", *canto_xy(VE, X_INI[0] + .1, X_INI[1] + .42), 32)
        f0 = F_AULA(*X_INI)
        lFX = TP(r"\F(\Xp)", *canto_xy(VD, f0[0] - .15, f0[1] + .38), 34)

        def pos_lX():
            return canto_xy(VE, st["X"][0] + .1, st["X"][1] + .42)

        def pos_lFX():
            f = F_AULA(*st["X"])
            return canto_xy(VD, f[0] - .15, f[1] + .38)

        def liga_X():
            Xd.add_updater(lambda m: m.move_to(VE.c2p(*st["X"])))
            aX.add_updater(lambda m: m.become(sX()))
            aFX.add_updater(lambda m: m.become(sFX()))
            segue(lX, pos_lX)
            segue(lFX, pos_lFX)
        self.gat("repara")
        self.play(FadeIn(Xd, scale=0.5), GrowArrow(aX), GrowArrow(aFX), FadeIn(lX), FadeIn(lFX), run_time=0.8)
        liga_X()
        A, B = np.array(X_INI), np.array(X_FIM)
        C = (A + B) / 2 + 0.35 * np.array([-(B - A)[1], (B - A)[0]]) / np.linalg.norm(B - A) * np.linalg.norm(B - A) * 0.6

        def arco(m, a):
            s = smooth(a)
            p = (1 - s) ** 2 * A + 2 * (1 - s) * s * C + s * s * B
            st["X"] = (float(p[0]), float(p[1]))
        self.gat("conforme você chega perto")
        self.play(UpdateFromAlphaFunc(Xd, arco), run_time=3.2)
        ep_v, d_v = ValueTracker(1.0), ValueTracker(d0)
        cE = vcirc(VD, 1.0, CAMPO2, 3, c=(1, 0)).set_z_index(6)
        cE.add_updater(lambda m: m.become(vcirc(VD, ep_v.get_value(), CAMPO2, 3, c=(1, 0)).set_z_index(6)))
        lE = TP(r"\eps", *canto_xy(VD, 1 + .75 + .22, .75 + .2), 36)
        segue(lE, lambda: canto_xy(VD, 1 + ep_v.get_value() * .75 + .22, ep_v.get_value() * .75 + .2))
        self.gat("um disquinho de raio épsilon")
        self.play(Create(cE), FadeIn(lE), run_time=1.0)
        cD = vcirc(VE, d0, POS, 3).set_z_index(6)
        cD.add_updater(lambda m: m.become(vcirc(VE, d_v.get_value(), POS, 3).set_z_index(6)))
        lD = TP(r"\del", *canto_xy(VE, -d0 - .3, 0), 36)
        segue(lD, lambda: canto_xy(VE, -d_v.get_value() - .3, 0))
        self.gat("um disquinho de raio delta")
        st["d"] = d0
        self.play(Create(cD), FadeIn(lD), run_time=1.0)
        self.ate(0.97)

        # ── B1-3 · ε = 1 ⇒ δ = 0,41; a volta; ε = 0,5 ⇒ δ = 0,21; a definição ──
        self.an("B1-3")
        L1 = TC(r"\eps = 1 \;\Rightarrow\; \del = 0{,}41", 960, 955, 44, "c")
        self.gat("com épsilon igual a um")
        self.play(caneta(L1))
        th = {"a": ANG}
        curva = VMobject().set_stroke(CAMPO2, 2 / 1.2, 0.85).set_fill(opacity=0).set_z_index(5)
        curva._sem_contorno = True

        def volta_(m, a):
            t = ANG + 2 * PI * a
            d = d_v.get_value()
            st["X"] = (d * math.cos(t), d * math.sin(t))
            n = max(2, int(240 * a) + 1)
            tt = np.linspace(ANG, t, n)
            fx, fy = F_AULA(d * np.cos(tt), d * np.sin(tt))
            curva.set_points_as_corners([VD.c2p(x, y) for x, y in zip(fx, fy)])
        self.gat("dá a volta na borda")
        self.add(curva)
        self.play(UpdateFromAlphaFunc(curva, volta_), run_time=3.0, rate_func=linear)
        pts = tip_curva(d0)
        dist = max(math.hypot(x - 1, y) for x, y in pts)
        print(f"[ε-δ] δ = 0,41: maior distância da curva das pontas a F(P) = {dist:.4f} (< ε = 1: {'ok' if dist < 1 else 'FORA'})")
        L2 = TC(r"\eps = 0{,}5 \;\Rightarrow\; \del = 0{,}21", 960, 955, 44, "c")
        L2.move_to(L1.get_center())

        def redesenha(m):
            d = d_v.get_value()
            st["X"] = (d * math.cos(ANG), d * math.sin(ANG))
            st["d"] = d
            m.set_points_as_corners([VD.c2p(x, y) for x, y in tip_curva(d)])
        self.gat("aperta para meio")
        curva.add_updater(redesenha)
        n1 = len(L1[0])
        print(f"[algebra] B1 ε-δ: {n1} → {len(L2[0])} glifos")
        mapa = [([0], [0]), ([1], [1]), ([2], [2, 3, 4]), *[([k], [k + 2]) for k in range(3, n1)]]
        self.play(ep_v.animate.set_value(0.5), d_v.animate.set_value(0.21), tbgm(L1, L2, *mapa, rt=1.5), run_time=1.5)
        limpa_soltos(self)
        curva.clear_updaters()
        dist = max(math.hypot(x - 1, y) for x, y in tip_curva(0.21))
        print(f"[ε-δ] δ = 0,21: maior distância da curva das pontas a F(P) = {dist:.4f} (< ε = 0,5: {'ok' if dist < .5 else 'FORA'})")
        dfn = TC(r"\lim\limits_{\Xp\to\Pt}\F(\Xp)=\Lv \iff \forall\eps>0\ \exists\del>0:\ 0<\|\Xp-\Pt\|<\del \;\Rightarrow\; \|\F(\Xp)-\Lv\|<\eps", 960, 960, 40, "c")
        self.gat("escrito é exatamente essa frase")
        self.play(FadeOut(L2), run_time=0.35)
        self.remove(L2)
        self.play(caneta(dfn, ritmo=0.45))
        self.ate(0.97)

        # ── B1-4 · o atalho por componentes ──
        self.an("B1-4")
        atl = TC(r"\lim\limits_{\Xp\to\Pt}\F(\Xp)=\Lv \iff \lim\limits_{\Xp\to\Pt}\Pp = L_1 \text{ e } \lim\limits_{\Xp\to\Pt}\Qq = L_2", 960, 960, 40, "c")
        self.gat("um atalho")
        self.play(FadeOut(dfn), run_time=0.35)
        self.remove(dfn)
        self.play(caneta(atl, ritmo=0.6))
        self.ate(0.97)
        for m in (Xd, aX, aFX, lX, lFX, cE, cD, lE, lD, cmp):
            m.clear_updaters()
        self.sai_fim()
