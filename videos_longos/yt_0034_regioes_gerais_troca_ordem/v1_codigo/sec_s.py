"""yt_0034 · S · síntese (alvo 25) e o próximo vídeo + CTA (alvo 26).
S1: as duas primeiras miniaturas (o retângulo tracejado com o quarto de disco; a fatia 0 | f | 0) aparecem uma de cada vez à esquerda, onde
as caixas ainda não estão (assim o palco não fica parado enquanto a voz resume); a do retângulo do sino vai para o lado direito e fica (alvo).
S2: o cartão do próximo vídeo entra em "como fica a troca" para ficar ≥ 8 s antes do CTA (em "no próximo vídeo" ficaria só ~7 s)."""
from pecas34 import *


class PS(B34):
    ANTES = "SÍNTESE"

    def corpo(self):
        # ── S1 · síntese (alvo 25) ──
        self.an("S1")
        Vm = Vw(470, 760, 150)                    # miniaturas da esquerda
        regm = regiao(Vm, cX(c_b21, .3, 1.85) + cX(d_b21, .3, 1.85)[::-1], z=2)
        cm = curva(Vm, cX(c_b21, .3, 1.85), AZC, 3)
        dm = curva(Vm, cX(d_b21, .3, 1.85), CORAL, 3)
        self.play(FadeIn(regm), Create(cm), Create(dm), run_time=0.4)
        self.gat("entre duas curvas")
        tm = tiraV(Vm, 1.1, c_b21(1.1), d_b21(1.1), h=.07)
        self.play(GrowFromEdge(tm, DOWN), run_time=0.6)
        self.gat("estende a função por")
        rq = curva(Vm, [(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)], GEO, 2, dash=(7, 7), z=3)
        z1 = TC(r"\Ge{0}", *Vm.px(1.75, 1.85), 30, "c")
        z2 = TC(r"\Ge{0}", *Vm.px(.2, .15), 30, "c")
        self.play(Create(rq), FadeOut(tm), run_time=0.8)
        self.remove(tm)
        self.pena(z1, z2, lag=0.2)
        self.gat("a fronteira dessas regiões")
        fr = VGroup(curva(Vm, cX(c_b21, .3, 1.85), AL, 2.5, z=6), curva(Vm, cX(d_b21, .3, 1.85), AL, 2.5, z=6),
                    curva(Vm, [(.3, c_b21(.3)), (.3, d_b21(.3))], AL, 2.5, z=6), curva(Vm, [(1.85, c_b21(1.85)), (1.85, d_b21(1.85))], AL, 2.5, z=6))
        self.play(Create(fr), run_time=0.9)
        self.gat("no máximo dois saltos")
        Lv = Lat(330, 760, 260, 70)
        G = lateral(Lv, 2.3, ymax=2.25, zt=(), yt=(), grade=False)
        ff = lambda Y: 1.5 + .35 * math.sin(2.2 * Y)
        ca = curva(Lv, [(0, 0), (.55, 0)], CI, 5, z=6)
        cf = curva(Lv, cX(ff, .55, 1.55, 60), CI, 5, z=6)
        cb = curva(Lv, [(1.55, 0), (2, 0)], CI, 5, z=6)
        j1 = curva(Lv, [(.55, 0), (.55, ff(.55))], AL, 2, dash=(5, 5), z=5)
        j2 = curva(Lv, [(1.55, 0), (1.55, ff(1.55))], AL, 2, dash=(5, 5), z=5)
        sai = [regm, cm, dm, rq, z1, z2, fr]
        self.play(*[FadeOut(m) for m in sai], GrowFromPoint(G["eh"], Lv.P(0, 0)), GrowFromPoint(G["ev"], Lv.P(0, 0)), run_time=0.6)
        self.remove(*sai)
        self.pena(G["lh"], G["lv"])
        self.play(Create(ca), run_time=0.3)
        self.play(Create(cf), Create(j1), run_time=0.6)
        self.play(Create(cb), Create(j2), run_time=0.3)
        self.gat("na prática a fatia")
        mini = [G["eh"], G["ev"], G["lh"], G["lv"], ca, cf, cb, j1, j2]
        self.play(*[FadeOut(m) for m in mini], run_time=0.4)
        self.remove(*mini)
        tese = L([("a", r"\iint_B\f="), ("io", r"\int_{\Am a}^{\Am b}\!"), ("ii", r"\int_{\Az{c(\X)}}^{\Co{d(\X)}}"), ("r1", r"\f\,\dY\,\dX="),
                  ("jo", r"\int_{\Mg c}^{\Mg d}\!"), ("ji", r"\int_{\Az{a(\Y)}}^{\Co{b(\Y)}}"), ("r2", r"\f\,\dX\,\dY")], 960, 290, 46, "c")
        self.pena(tese, passo=0.06)
        self.gat("os limites de fora")
        def lims(ch):
            g_ = list(gl(tese, ch))
            a_ = max(g_, key=lambda x: x.height)
            return VGroup(*[x for x in g_ if x is not a_])
        acende(self, (lims("io"), E1), (lims("jo"), E2), rt=0.9)
        self.gat("os de dentro dependem")
        acende(self, (lims("ii"), CORAL), (lims("ji"), CORAL), rt=0.9)
        self.gat("virar um retângulo")
        LS = Lat(1300, 800, 420, 330)
        Gs = lateral(LS, 1.15, ymax=1.15, zt=(0, 1), yt=(0, 1), hcor=E1, hl=r"\X", vl=r"\f", passo=.25)
        h = gs(.6)
        rs = poly_px([LS.px(0, 0), LS.px(.6, 0), LS.px(.6, h), LS.px(0, h)], mixh(BG_, CI, .3), z=2)
        rs.set_stroke(E2, W(4), 1)
        self.play(FadeIn(Gs["grade"]), GrowFromPoint(Gs["eh"], LS.P(0, 0)), GrowFromPoint(Gs["ev"], LS.P(0, 0)), run_time=0.6)
        self.pena(Gs["lh"], Gs["lv"], Gs["nums"])
        self.play(GrowFromEdge(rs, DOWN), run_time=0.7)
        self.gat("e trazer exatamente o")
        self.play(rs.animate.set_stroke(width=W(7)), run_time=0.4)
        self.play(rs.animate.set_stroke(width=W(4)), run_time=0.4)
        caixas = [("QUARTO DE DISCO: ÁREA", r"\pi", 480, "deu pi"), ("TRAVADA", r"\to\ \dfrac{1-1/e}{2}", 610, "um menos um sobre"),
                  ("TROCAR = RELER A REGIÃO", None, 740, "reler a mesma região")]
        for t, tex, Y, gg in caixas:
            if gg == "deu pi":
                self.gat("foi assim que")
                mols = [moldura(260, Yc - 45, 860, 80, GEO, .45, 2, 12) for _, _, Yc, _ in caixas]
                self.play(LaggedStart(*[Create(m) for m in mols], lag_ratio=0.3), run_time=1.0)
            self.gat(gg)
            ck = check_px(300, Y - 6, MEN, .9)
            tt = T(t, 340, Y + 8, 30)
            self.play(Create(ck), run_time=0.3)
            if tex:
                mt = TC(tex, pxof(tt.get_right())[0] + 16, Y - 2, 40 if tex == r"\pi" else 36, "l")
                self.pena(tt, mt, lag=0.4)
            else:
                self.pena(tt)
        self.marca("25", agora=True)

        # ── S2 · o próximo vídeo e CTA (alvo 26) ──
        self.an("S2")
        self.secao("NO PRÓXIMO VÍDEO")
        V = Vw(200, 920, 150)
        pa = lambda a: 4 * a - a * a
        xl = lambda y: 2 - math.sqrt(4 - y)
        xr = lambda y: 2 + math.sqrt(4 - y)
        self.limpa(rt=0.4)
        g = papel_v(V, (0, 4.2, 0, 4.2))
        self.grade = g
        sx, sy, lx, ly = eixos_v(V, 4.3, 4.4)
        self.play(FadeIn(g), GrowFromPoint(sx, V.P(0, 0)), GrowFromPoint(sy, V.P(0, 0)), run_time=0.5)
        self.pena(lx, ly)
        self.gat("olha a região entre")
        reg = regiao(V, cX(pa, 0, 3) + [(0, 0)])
        rx_ = curva(V, cX(lambda a: a, 0, 3), AZC, 4)              # em pé: a reta é a entrada, a parábola é a saída
        pab = curva(V, cX(pa, 0, 3), CORAL, 4)
        t3 = tick(V, "x", 3, r"\Am{3}")
        self.play(FadeIn(reg), Create(rx_), Create(pab), Create(t3[0]), run_time=1.1)
        self.pena(t3[1])
        eq_ = mixl([("m", r"\Co{\Y=4\X-\X^2}"), ("t", "E"), ("m", r"\Az{\Y=\X}")], 1120, 720, 34)
        self.pena(*eq_.p, lag=0.15)
        self.gat("em pé é uma")
        xt = ValueTracker(.3)
        self.add(xt)
        tv = always_redraw(lambda: tiraV(V, xt.get_value(), xt.get_value(), pa(xt.get_value()), h=.1))
        pv1 = always_redraw(lambda: ponto_px(*V.px(xt.get_value(), xt.get_value()), AZC, 9))
        pv2 = always_redraw(lambda: ponto_px(*V.px(xt.get_value(), pa(xt.get_value())), CORAL, 9))
        self.play(FadeIn(tv), FadeIn(pv1), FadeIn(pv2), run_time=0.4)
        self.play(xt.animate.set_value(2.6), run_time=2.4)
        self.play(FadeOut(tv), FadeOut(pv1), FadeOut(pv2), run_time=0.4)
        for m in (tv, pv1, pv2):
            m.clear_updaters()
        self.remove(tv, pv1, pv2, xt)
        self.gat("para fatiar deitado")                          # a mesma curva troca de cor quando a ordem troca
        rx2 = curva(V, cX(lambda a: a, 0, 3), CORAL, 4)
        pl_ = curva(V, cX(pa, 0, 2), AZC, 4)
        pr_ = curva(V, cX(pa, 2, 3), CORAL, 4)
        eq2 = mixl([("m", r"\Y=4\X-\X^2"), ("t", "E"), ("m", r"\Co{\Y=\X}")], 1120, 720, 34)
        self.play(ReplacementTransform(rx_, rx2), FadeOut(pab), FadeIn(pl_), FadeIn(pr_), *[ReplacementTransform(a, b) for a, b in zip(eq_.p, eq2.p)],
                  run_time=1.0)
        self.remove(pab)
        for m in eq2.p:
            ja_escrita(m)
        t3y, t4y = tick(V, "y", 3, r"\Mg{3}"), tick(V, "y", 4, r"\Mg{4}")
        h3 = curva(V, [(0, 3), (3, 3)], E2, 2, dash=(6, 7), alpha=.7, z=3)
        self.play(Create(t3y[0]), Create(t4y[0]), Create(h3), run_time=0.6)
        self.pena(t3y[1], t4y[1])
        self.gat("vira duas curvas")
        yt = ValueTracker(.6)
        self.add(yt)
        sai_ = lambda y: y if y <= 3 else xr(y)
        th = always_redraw(lambda: tiraH(V, yt.get_value(), xl(yt.get_value()), sai_(yt.get_value()), h=.1))
        ph1 = always_redraw(lambda: ponto_px(*V.px(xl(yt.get_value()), yt.get_value()), AZC, 9))
        ph2 = always_redraw(lambda: ponto_px(*V.px(sai_(yt.get_value()), yt.get_value()), CORAL, 9))
        self.play(FadeIn(th), FadeIn(ph1), FadeIn(ph2), run_time=0.3)
        self.play(yt.animate.set_value(1.5), run_time=1.0)
        ra = rot(V, r"\Az{\X=2-\sqrt{4-\Y}}", (xl(2.4), 2.4), -20, 0, 28, "r")
        rxy = rot(V, r"\Co{\X=\Y}", (2, 2), 40, 20, 28, "l")
        self.pena(ra, rxy, lag=0.3)
        fixa1 = tiraH(V, 1.5, xl(1.5), 1.5, h=.1)
        f1a, f1b = pontos_es(V, (xl(1.5), 1.5), (1.5, 1.5))
        self.add(fixa1, f1a, f1b)
        self.play(yt.animate.set_value(3.5), run_time=1.6)
        rb = rot(V, r"\Co{\X=2+\sqrt{4-\Y}}", (xr(3.2), 3.2), 24, 0, 28, "l")
        self.pena(rb)
        for m in (th, ph1, ph2):
            m.clear_updaters()
        self.gat("como fica a troca")
        pn = painel(1120, 300, 740, 330)
        n1 = leg("NO PRÓXIMO VÍDEO:", 1160, 380, GEO, "left", 30)
        n2 = T("EXERCÍCIOS DO MÓDULO", 1160, 450, 40)
        n3 = T("A PARÁBOLA VIRA", 1160, 540, 40, "left", MEN)
        n4 = T("DUAS CURVAS?", 1160, 595, 40, "left", MEN)
        print(f"[cartao] entra {self.t:.2f}")
        self.play(Create(pn), run_time=0.5)
        self.pena(n1, n2, lag=0.3)
        self.pena(n3, n4, lag=0.3)
        self.marca("26", agora=True)
        self.gat("deixa o like")
        print(f"[cartao] sai {self.t:.2f}")
        logo_cta(self)
