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
        L1 = L([("i", r"\int_{\Az{0}}^{\Co{\X}}"), ("f", r"(\X^2+\Y^2)"), ("dy", r"\,\dY"), ("eq", "="), ("pr", r"\Big[\X^2\Y+\dfrac{\Y^3}{3}\Big]_0^{\X}")],
               1120, 300, 36, caneta=False)
        ii = list(gl(L1, "i"))
        alto = max(ii, key=lambda x: x.height)
        sup = [k for k in sel(L1, "i") if L1[0][k] is not alto and L1[0][k].get_center()[1] > alto.get_center()[1]]
        voos(self, [(VGroup(glifo_dir(rx.f)).copy(), ja_escrita(parte(L1, sup, "x")))], rt=1.0)
        self.pena(parte(L1, [k for k in sel(L1, ["i", "f", "dy"]) if k not in sup], "resto"))
        yv = ValueTracker(0.0)                                          # um ponto percorre a fatia de baixo para cima (a integral de dentro, em y)
        self.add(yv)
        pv = always_redraw(lambda: ponto_px(*CH.px(X0, yv.get_value()), BR, 6, z=9))
        self.play(FadeIn(pv), run_time=0.2)
        self.play(yv.animate.set_value(X0), run_time=1.6, rate_func=linear)
        self.play(FadeOut(pv), run_time=0.3)
        pv.clear_updaters()
        self.remove(pv, yv)
        self.gat("a primitiva em ípsilon")
        self.pena(parte(L1, sel(L1, ["eq", "pr"]), "= [x²y + y³/3]₀^x"))
        L1._esc = True
        realce(self, tv, pe, ps)
        self.gat("mais ípsilon ao cubo")
        realce(self, tv, pe, ps, cor=E1)
        self.gat("igual a xis dá")
        realce(self, ps, rx)
        L2 = L([("a", r"=\Big(\X^3+\dfrac{\X^3}{3}\Big)"), ("b", r"-\,0"), ("e", "="), ("r", r"\dfrac{4\X^3}{3}")], 1120, 410, 36)
        self.pena(parte(L2, sel(L2, "a"), "= (x³ + x³/3)"))
        self.gat("em zero zero")
        self.pena(parte(L2, sel(L2, "b"), "− 0"))
        self.gat("somando quatro terços")
        self.pena(parte(L2, sel(L2, ["e", "r"]), "= 4x³/3"))
        L2._esc = True
        self.gat("a de fora")
        L3 = L([("i", r"\int_0^2"), ("c", r"\dfrac{4\X^3}{3}"), ("dx", r"\,\dX"), ("eq", "="), ("pr", r"\dfrac{4}{3}\Big[\dfrac{\X^4}{4}\Big]_0^2")],
               1120, 525, 36, caneta=False)
        voos(self, [(VGroup(*gl(L2, "r")).copy(), parte(L3, sel(L3, "c"), "4x³/3"))], rt=0.9)
        self.pena(parte(L3, sel(L3, ["i", "dx"]), "∫ dx"))
        self.gat("à quarta sobre")
        self.pena(parte(L3, sel(L3, ["eq", "pr"]), "= (4/3)[x⁴/4]₀²"))
        L3._esc = True
        self.gat("em dois xis à")
        L4 = L([("a", r"=\dfrac{4}{3}\Big(\dfrac{16}{4}-0\Big)"), ("e", "="), ("v", r"\dfrac{16}{3}")], 1120, 640, 36)
        self.pena(parte(L4, sel(L4, "a"), "= (4/3)(16/4 − 0)"))
        self.gat("dezesseis terços de quilo")
        self.pena(parte(L4, sel(L4, ["e", "v"]), "= 16/3"))
        L4._esc = True
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
        M1 = L([("i", r"\int_{\Az{\Y}}^{\Co{2}}"), ("f", r"(\X^2+\Y^2)"), ("dx", r"\,\dX"), ("eq", "="), ("pr", r"\Big[\dfrac{\X^3}{3}+\Y^2\X\Big]_{\Y}^{2}")],
               1120, 250, 36, caneta=False)
        ii = list(gl(M1, "i"))
        alto = max(ii, key=lambda x: x.height)
        sup = [k for k in sel(M1, "i") if M1[0][k] is not alto and M1[0][k].get_center()[1] > alto.get_center()[1]]
        inf = [k for k in sel(M1, "i") if M1[0][k] is not alto and k not in sup]
        voos(self, [(VGroup(glifo_dir(rxy.f)).copy(), ja_escrita(parte(M1, inf, "y"))), (VGroup(glifo_dir(rx2.f)).copy(), ja_escrita(parte(M1, sup, "2")))],
             rt=1.0)
        self.pena(parte(M1, [k for k in sel(M1, ["i", "f", "dx"]) if k not in sup + inf], "resto"))
        self.gat("sai na borda em")
        realce(self, rx2, ps2)                                         # a saída em x = 2
        self.gat("o limite de baixo")
        acende(self, (VGroup(*[M1[0][k] for k in inf]), AZC), rt=1.2)
        self.gat("agora é a diagonal")
        realce(self, dg, rxy, pe2, cor=AZC)                            # a diagonal virou a entrada
        self.gat("a primitiva em xis")
        self.pena(parte(M1, sel(M1, ["eq", "pr"]), "= [x³/3 + y²x]_y²"))
        realce(self, th, pe2, ps2)
        M1._esc = True
        self.gat("igual a dois oito")
        M2 = L([("a", r"=\Big(\dfrac{8}{3}+2\Y^2\Big)"), ("b", r"-\Big(\dfrac{\Y^3}{3}+\Y^3\Big)")], 1120, 355, 36)
        self.pena(parte(M2, sel(M2, "a"), "= (8/3 + 2y²)"))
        self.gat("igual a ípsilon ípsilon")
        self.pena(parte(M2, sel(M2, "b"), "− (y³/3 + y³)"))
        M2._esc = True
        realce(self, th, pe2, ps2)
        self.gat("subtraindo oito terços")
        realce(self, th, cor=MEN)
        M3 = L([("eq", "="), ("r", r"\dfrac{8}{3}+2\Y^2-\dfrac{4\Y^3}{3}")], 1120, 460, 36)
        self.pena(M3)
        self.gat("a primitiva disso")
        vivo(self, lambda u: tiraH(CH, 2 * u, 2 * u, max(2 * u + .002, 2.0), h=.08, alpha=.35), dur=5.5)    # palco vivo: a de fora, y de 0 a 2
        N0 = L([("i", r"\int_0^2"), ("a", r"\Big("), ("r", r"\dfrac{8}{3}+2\Y^2-\dfrac{4\Y^3}{3}"), ("b", r"\Big)"), ("dy", r"\dY"), ("eq", "="),
                ("pr", r"\Big[\dfrac{8\Y}{3}+\dfrac{2\Y^3}{3}-\dfrac{\Y^4}{3}\Big]_0^2")], 1120, 570, 34, caneta=False)
        voos(self, [(gl(M3, "r").copy(), ja_escrita(parte(N0, sel(N0, "r"), "parcelas")))], rt=1.0)
        self.pena(parte(N0, sel(N0, ["i", "a", "b", "dy"]), "∫ ( ) dy"))
        self.pena(parte(N0, sel(N0, ["eq", "pr"]), "= [8y/3 + 2y³/3 − y⁴/3]₀²"))
        N0._esc = True
        self.gat("dá dezesseis terços")
        N1 = L([("a", r"=\dfrac{16}{3}+\dfrac{16}{3}-\dfrac{16}{3}"), ("e", "="), ("v", r"\dfrac{16}{3}")], 1120, 680, 36)
        self.pena(parte(N1, sel(N1, "a"), "= 16/3 + 16/3 − 16/3"))
        self.gat("sobra dezesseis terços")
        self.pena(parte(N1, sel(N1, ["e", "v"]), "= 16/3"))
        N1._esc = True
        ck = check_px(1720, 680)
        self.play(Create(ck), run_time=0.4)
        # a escada sobe e sai; o resultado vira chip no topo (a coluna nunca passa de 7 linhas)
        self.gat("uma conferência que")
        chip_ = TC(r"\text{DEITADO: }\dfrac{16}{3}\ \checkmark", 1135, 220, 30, caneta=False)
        mold_ = RoundedRectangle(width=(chip_.width * 120 + 30) / 120, height=(chip_.height * 120 + 20) / 120, corner_radius=10 / 120)
        mold_.move_to(chip_.get_center()).set_stroke(MEN, W(2)).set_fill(opacity=0).set_z_index(24)
        esc = [M1, M2, M3, N0, N1, ck]
        src_ = VGroup(*gl(N1, "v")).copy()
        self.play(*[m.animate.shift(UP * .5).set_opacity(0) for m in esc], run_time=0.35)
        self.remove(*esc)
        voos(self, [(src_, chip_)], rt=0.8, extra=[Create(mold_)])
        realce(self, dg, cor=AZC)                                      # a diagonal: o espelho da conferência
        self.gat("trocar xis com")
        fs_ = TC(r"\f(\X,\Y)=\f(\Y,\X)", 1120, 340, 40)
        self.pena(fs_)
        self.gat("um espelho")
        self.play(FadeOut(lfo), run_time=0.3)              # o de cima volta a contar no espelho
        self.remove(lfo)
        tracej = curva(CH, [(0, 0), (0, 2), (2, 2)], GEO, 2, dash=(7, 7), z=6)
        self.play(Create(tracej), run_time=0.7)
        dobra = Polygon(CH.P(0, 0), CH.P(0, 2), CH.P(2, 2)).set_fill(GEO, .18).set_stroke(GEO, W(2), 1)
        sem_ctn(dobra).set_z_index(5)
        seta_ = seta_px(CH.px(.5, 1.5), CH.px(1.45, .62), BR, 3, 18, z=8)
        bs_ = [m for m in (lBb,) if m in self.mobjects]
        self.play(FadeOut(rxy), *[FadeOut(m) for m in bs_], run_time=0.2)    # os rótulos saem durante a dobra e voltam depois
        self.add(dobra)
        eixo = np.array([1.0, 1.0, 0.0]) / math.sqrt(2)
        self.play(Rotate(dobra, PI, axis=eixo, about_point=CH.P(0, 0)), Create(seta_), run_time=1.4)
        self.play(FadeOut(dobra), FadeIn(rxy), *[FadeIn(m) for m in bs_], run_time=0.3)
        self.remove(dobra)
        es = leg("ESPELHO NA DIAGONAL", 1120, 420, GEO, "left", 26)
        self.pena(es)
        self.gat("pesam igual dezesseis")
        sm = TC(r"\dfrac{16}{3}+\dfrac{16}{3}=\dfrac{32}{3}\ \text{kg}", 1120, 540, 44)
        self.pena(sm)
        self.marca("19", agora=True)
        self.sai_fim(rt=0.25)                         # palco vazio ≤ 0,5 s na virada para o PB6
