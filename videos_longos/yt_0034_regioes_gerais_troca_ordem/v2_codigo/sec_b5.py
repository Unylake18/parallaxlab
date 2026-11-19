"""yt_0034 · B5 · a chapa x² + y² cortada na diagonal: em pé (alvo 18) e deitada + espelho (alvo 19). Glyph maps 10 e 11.
A diagonal troca de papel (e de cor do rótulo) quando a tira troca de direção: saída coral `y = x` em pé, entrada azul-claro `x = y` deitada."""
from pecas34 import *


def glifo_dir(m):
    """último glifo (mais à direita) de um rótulo."""
    return max(m[0], key=lambda x: x.get_center()[0])


class PB5(B34):
    ANTES = "A CHAPA NA DIAGONAL"

    def corpo(self):
        # ── B5-1 · a chapa cortada na diagonal (alvo 18) ──
        self.an("B5-1")
        mapa = img_chapa(arr_dens(64), CH, z=0)
        bd = borda_ch(CH, GEO, 2, z=5)
        sx, sy, lx, ly = eixos_chapa(CH)
        self.play(Create(bd), GrowFromPoint(sx, CH.P(0, 0)), GrowFromPoint(sy, CH.P(0, 0)), run_time=0.6)
        self.pena(lx, ly)
        self.gat("com a chapa de")
        self.play(FadeIn(mapa), run_time=2.0)
        self.gat("xis ao quadrado mais")
        niv = VGroup(*[curva(CH, [(r * math.cos(t), r * math.sin(t)) for t in np.linspace(0, PI / 2, 60) if r * math.cos(t) <= 2 and r * math.sin(t) <= 2],
                             BR, 1.5, dash=(5, 6), alpha=.7, z=4) for r in (1.0, 1.6, 2.2)])
        self.play(LaggedStart(*[Create(c) for c in niv], lag_ratio=0.3), run_time=1.4)
        self.gat("trinta e dois terços")
        self.play(FadeOut(niv), run_time=0.4)
        self.remove(niv)
        ci = mixl([("t", "CHAPA INTEIRA:", GEO), ("m", r"\Ge{\dfrac{32}{3}\ \text{kg}}")], 1120, 200, 30)
        self.pena(*ci.p, lag=0.15)
        self.gat("na diagonal ípsilon")
        dg = curva(CH, [(0, 0), (2, 2)], BR, 4, z=6)
        self.play(Create(dg), run_time=0.9)
        self.gat("triângulo de baixo")
        cima = regiao(CH, [(0, 0), (2, 2), (0, 2)], BG_, .86, z=3)
        cb = curva(CH, [(0, 0), (2, 0), (2, 2), (0, 0)], BR, 3, z=6)
        lBb = TC("B", *CH.px(1.68, .5), 40, "c")
        lfo = leg("FORA", *CH.px(.35, 1.5), GEO, "left", 26)
        self.play(FadeIn(cima), Create(cb), run_time=0.8)
        self.pena(lBb, lfo, lag=0.3)
        self.gat("fatia em pé ela")
        X0 = 1.2
        tv = tiraV(CH, X0, 0, X0, h=.08, alpha=.6)
        pe, ps = pontos_es(CH, (X0, 0), (X0, X0))
        r0 = rot(CH, r"\Az{\Y=0}", (1.3, 0), 0, -30, 28)
        self.play(GrowFromEdge(tv, DOWN), FadeIn(pe, scale=.5), run_time=0.8)
        self.pena(r0)
        self.gat("e sai na diagonal")
        rx = rot(CH, r"\Co{\Y=\X}", (1.45, 1.45), -150, -10, 30)
        self.play(FadeIn(ps, scale=.5), run_time=0.3)
        self.pena(rx)
        self.gat("a integral de dentro")
        L1 = L([("i", r"\int_{\Az{0}}^{\Co{\X}}"), ("f", r"(\X^2+\Y^2)"), ("dy", r"\,\dY")], 1120, 300, 40, caneta=False)
        ii = list(gl(L1, "i"))
        alto = max(ii, key=lambda x: x.height)
        sup = [k for k in sel(L1, "i") if L1[0][k] is not alto and L1[0][k].get_center()[1] > alto.get_center()[1]]
        voos(self, [(VGroup(glifo_dir(rx.f)).copy(), ja_escrita(parte(L1, sup, "x")))], rt=1.0)
        self.pena(parte(L1, [k for k in range(len(L1[0])) if k not in sup], "resto"))
        L1._esc = True
        realce(self, tv, pe, ps)                                       # a fatia em pé que a integral de dentro percorre
        self.gat("dê ípsilon o xis")                           # um ponto percorre a fatia de baixo para cima (a integral de dentro, em y)
        yv = ValueTracker(0.0)
        self.add(yv)
        pv = always_redraw(lambda: ponto_px(*CH.px(X0, yv.get_value()), BR, 6, z=9))
        self.play(FadeIn(pv), run_time=0.2)
        self.play(yv.animate.set_value(X0), run_time=1.6, rate_func=linear)
        self.play(FadeOut(pv), run_time=0.3)
        pv.clear_updaters()
        self.remove(pv, yv)
        self.gat("constante na fatia")
        fx2 = sel(L1, "f")[1:3]                          # ( x ² + y ² ): o x² são os glifos 1 e 2 da peça
        fy2 = sel(L1, "f")[4:6]
        L2a = L([("eq", "="), ("x2", r"\X^2"), ("d", r"\cdot"), ("fx", r"\X")], 1160, 410, 40)
        passo(self, L1, L2a, [(fx2, "x2"), (sup, "fx")], rt=1.2, copia=True, nota="mapa 10a (B5-1: x² é constante na fatia: x²·x)")
        realce(self, tv)                                               # na fatia, o x² não muda
        self.gat("ao cubo sobre três")
        L2 = L([("eq", "="), ("x2", r"\X^2"), ("d", r"\cdot"), ("fx", r"\X"), ("pl", "+"), ("fr", r"\dfrac{\X^3}{3}")], 1160, 410, 40)
        passo(self, L2a, L2, [(k, k) for k in ("eq", "x2", "d", "fx")], rt=0.5, nota="mapa 10b (B5-1: + x³/3)")
        self.gat("somando quatro terços")
        L3 = L([("eq", "="), ("fr", r"\dfrac{4\X^3}{3}")], 1160, 520, 40)
        passo(self, L2, L3, [("eq", "eq"), (["x2", "d", "fx", "pl", "fr"], "fr")], rt=1.3, copia=True, nota="mapa 10c (B5-1: = 4x³/3)")
        self.gat("a de fora de")
        L4a = L([("i", r"\int_0^2"), ("c", r"\dfrac{4}{3}\X^3"), ("dx", r"\,\dX")], 1120, 660, 40, caneta=False)
        voos(self, [(gl(L3, "fr").copy(), ja_escrita(parte(L4a, sel(L4a, "c"), "4/3 x³")))], rt=1.0)
        self.pena(parte(L4a, sel(L4a, ["i", "dx"]), "∫ dx"))
        L4a._esc = True
        L4b = L([("i", r"\int_0^2"), ("c", r"\dfrac{4}{3}\X^3"), ("dx", r"\,\dX"), ("eq", "="), ("m", r"\dfrac{4}{3}\cdot\dfrac{2^4}{4}")], 1120, 660, 40)
        passo(self, L4a, L4b, [(k, k) for k in ("i", "c", "dx")], rt=0.5, nota="mapa 10d (B5-1: = (4/3)·2⁴/4)")
        self.gat("dezesseis terços de")
        L4 = L([("i", r"\int_0^2"), ("c", r"\dfrac{4}{3}\X^3"), ("dx", r"\,\dX"), ("eq", "="), ("m", r"\dfrac{4}{3}\cdot\dfrac{2^4}{4}"), ("e2", "="),
                ("v", r"\dfrac{16}{3}")], 1120, 660, 40)
        passo(self, L4b, L4, [(k, k) for k in ("i", "c", "dx", "eq", "m")], rt=0.5, nota="mapa 10e (B5-1: = 16/3)")
        self.marca("v2_09", agora=True)

        # ── B5-2 · a outra ordem e o espelho (alvo 19) ──
        self.an("B5-2")
        self.secao("A OUTRA ORDEM")
        self.gat("congela o ípsilon")
        Y0 = .8
        th = tiraH(CH, Y0, Y0, 2, h=.08, alpha=.6)
        pe2, ps2 = pontos_es(CH, (Y0, Y0), (2, Y0))
        rxy = rot(CH, r"\Az{\X=\Y}", (Y0, Y0), -120, -30, 30)
        rx2 = rot(CH, r"\Co{\X=2}", (2, Y0), 20, -34, 30, "l")
        col = [ci, L1, L2, L3, L4]
        self.play(*[FadeOut(m) for m in col], FadeOut(r0), FadeOut(rx), FadeOut(lBb), run_time=0.4)          # os rótulos saem antes de a tira girar (sem cruzar traços)
        self.remove(*col, r0, rx)
        self.play(ReplacementTransform(tv, th), ReplacementTransform(pe, pe2), ReplacementTransform(ps, ps2), cima.animate.set_fill(opacity=.55),
                  run_time=1.0)
        self.pena(rxy, rx2, lag=0.2)
        self.play(FadeIn(lBb), run_time=0.3)
        self.gat("entra na diagonal")
        M1 = L([("i", r"\int_{\Az{\Y}}^{\Co{2}}"), ("f", r"(\X^2+\Y^2)"), ("dx", r"\,\dX")], 1120, 250, 36, caneta=False)
        ii = list(gl(M1, "i"))
        alto = max(ii, key=lambda x: x.height)
        sup = [k for k in sel(M1, "i") if M1[0][k] is not alto and M1[0][k].get_center()[1] > alto.get_center()[1]]
        inf = [k for k in sel(M1, "i") if M1[0][k] is not alto and k not in sup]
        voos(self, [(VGroup(glifo_dir(rxy.f)).copy(), ja_escrita(parte(M1, inf, "y"))), (VGroup(glifo_dir(rx2.f)).copy(), ja_escrita(parte(M1, sup, "2")))],
             rt=1.0)
        self.pena(parte(M1, [k for k in range(len(M1[0])) if k not in sup + inf], "resto"))
        M1._esc = True
        self.gat("sai na borda em")
        realce(self, rx2, ps2)                                         # a saída em x = 2
        self.gat("o limite de baixo")
        acende(self, (VGroup(*[M1[0][k] for k in inf]), AZC), rt=1.2)
        self.gat("agora é a diagonal")
        realce(self, dg, rxy, pe2, cor=AZC)                            # a diagonal virou a entrada
        self.gat("dá oito terços")
        M1b = L([("i", r"\int_{\Az{\Y}}^{\Co{2}}"), ("f", r"(\X^2+\Y^2)"), ("dx", r"\,\dX"), ("eq", "="), ("r", r"\dfrac{8}{3}+2\Y^2-\dfrac{4\Y^3}{3}")],
                1120, 250, 36)
        passo(self, M1, M1b, [(k, k) for k in ("i", "f", "dx")], rt=0.5, nota="mapa 11a (B5-2: = 8/3 + 2y² − 4y³/3)")
        self.gat("menos quatro terços de")
        realce(self, th, pe2, ps2)                                     # a fatia deitada que a conta de dentro somou
        self.gat("integrando de zero")
        N0 = L([("i", r"\int_0^2"), ("a", r"\Big("), ("r", r"\dfrac{8}{3}+2\Y^2-\dfrac{4\Y^3}{3}"), ("b", r"\Big)"), ("dy", r"\dY")], 1120, 380, 36, caneta=False)
        voos(self, [(gl(M1b, "r").copy(), ja_escrita(parte(N0, sel(N0, "r"), "parcelas")))], rt=1.0)
        self.pena(parte(N0, sel(N0, ["i", "a", "b", "dy"]), "∫ ( ) dy"))
        N0._esc = True
        self.gat("cada parcela vale")
        N1 = L([("i", r"\int_0^2"), ("a", r"\Big("), ("r", r"\dfrac{8}{3}+2\Y^2-\dfrac{4\Y^3}{3}"), ("b", r"\Big)"), ("dy", r"\dY"), ("eq", "="),
                ("s", r"\dfrac{16}{3}+\dfrac{16}{3}-\dfrac{16}{3}")], 1120, 380, 36)
        passo(self, N0, N1, [(k, k) for k in ("i", "a", "r", "b", "dy")], rt=0.5, nota="mapa 11b (B5-2: = 16/3 + 16/3 − 16/3)")
        self.gat("sobra dezesseis terços")
        N2 = L([("i", r"\int_0^2"), ("a", r"\Big("), ("r", r"\dfrac{8}{3}+2\Y^2-\dfrac{4\Y^3}{3}"), ("b", r"\Big)"), ("dy", r"\dY"), ("eq", "="),
                ("s", r"\dfrac{16}{3}")], 1120, 380, 36)
        passo(self, N1, N2, [(k, k) for k in ("i", "a", "r", "b", "dy", "eq", "s")], rt=1.2, nota="mapa 11c (B5-2: = 16/3, um termo cancela outro)")
        ck = check_px(1790, 380)
        self.play(Create(ck), run_time=0.4)
        self.gat("uma conferência que")
        realce(self, dg, cor=AZC)                                      # a diagonal: o espelho da conferência
        self.gat("trocar xis com")
        fs_ = TC(r"\f(\X,\Y)=\f(\Y,\X)", 1120, 520, 40)
        self.pena(fs_)
        self.gat("um espelho")
        self.play(FadeOut(lfo), run_time=0.3)              # o de cima volta a contar no espelho
        self.remove(lfo)
        tracej = curva(CH, [(0, 0), (0, 2), (2, 2)], GEO, 2, dash=(7, 7), z=6)
        self.play(Create(tracej), run_time=0.7)
        dobra = Polygon(CH.P(0, 0), CH.P(0, 2), CH.P(2, 2)).set_fill(GEO, .18).set_stroke(GEO, W(2), 1)
        sem_ctn(dobra).set_z_index(5)
        seta_ = seta_px(CH.px(.5, 1.5), CH.px(1.45, .62), BR, 3, 18, z=8)
        self.play(FadeOut(rxy), run_time=0.2)              # o rótulo da diagonal sai durante a dobra e volta depois
        self.add(dobra)
        eixo = np.array([1.0, 1.0, 0.0]) / math.sqrt(2)
        self.play(Rotate(dobra, PI, axis=eixo, about_point=CH.P(0, 0)), Create(seta_), run_time=1.4)
        self.play(FadeOut(dobra), FadeIn(rxy), run_time=0.3)
        self.remove(dobra)
        es = leg("ESPELHO NA DIAGONAL", 1120, 600, GEO, "left", 26)
        self.pena(es)
        self.gat("dezesseis terços mais")
        sm = TC(r"\dfrac{16}{3}+\dfrac{16}{3}=\dfrac{32}{3}\ \text{kg}", 1120, 720, 44)
        self.pena(sm)
        self.marca("19", agora=True)
        self.sai_fim(rt=0.25)                         # palco vazio ≤ 0,5 s na virada para o PB6
