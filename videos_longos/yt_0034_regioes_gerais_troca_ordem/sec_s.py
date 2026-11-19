"""yt_0034 · S · síntese (alvo 25) e o próximo vídeo + CTA (alvo 26).
S1: as duas primeiras miniaturas (o retângulo tracejado com o quarto de disco; a fatia 0 | f | 0) aparecem uma de cada vez à esquerda, onde
as caixas ainda não estão (assim o palco não fica parado enquanto a voz resume); a do retângulo do sino vai para o lado direito e fica (alvo).
S2: o cartão do próximo vídeo entra em "como fica a troca" para ficar ≥ 8 s antes do CTA (em "no próximo vídeo" ficaria só ~7 s)."""
from pecas34 import *


class PS(B34):
    ANTES = "SÍNTESE"

    def corpo(self):
        # ── S1 · síntese (alvo v2_13): três painéis (zero fora, dois saltos, o retângulo), a tese e os três selos ──
        self.an("S1")
        pns = [painel(X0, 160, 520, 380) for X0 in (100, 700, 1300)]
        tts = [leg(t, X, 205, GEO, "center", 26) for t, X in (("ESTENDE POR ZERO", 360), ("NO MÁXIMO DOIS SALTOS", 960), ("A FATIA VIRA RETÂNGULO", 1560))]
        M1 = Lat(170, 490, 170, 105)
        a, b = .3, 1.85
        reg1 = regiao(M1, cX(c_b21, a, b) + cX(d_b21, a, b)[::-1], z=2)
        c1 = curva(M1, cX(c_b21, a, b), AZC, 3)
        d1 = curva(M1, cX(d_b21, a, b), CORAL, 3)
        self.play(Create(pns[0]), FadeIn(reg1), Create(c1), Create(d1), run_time=0.5)
        self.pena(tts[0])
        self.gat("entre duas curvas")
        t1_ = poly_px([M1.px(1.07, c_b21(1.07)), M1.px(1.13, c_b21(1.13)), M1.px(1.13, d_b21(1.13)), M1.px(1.07, d_b21(1.07))], mixh(BG_, E1, .55), z=4)
        t1_.set_stroke(E1, W(2), 1)
        lB1 = TC("B", *M1.px(.65, 1.05), 30, "c")
        self.play(GrowFromEdge(t1_, DOWN), run_time=0.6)
        self.pena(lB1)
        self.gat("estende a função por")
        R1 = curva(M1, [(0, -.1), (2.2, -.1), (2.2, 2.1), (0, 2.1), (0, -.1)], GEO, 2, z=3)
        z1 = TC(r"\Ge{0}", *M1.px(.15, 1.9), 26, "c")
        z2 = TC(r"\Ge{0}", *M1.px(2.05, .2), 26, "c")
        lR1 = TC("R", *M1.px(2.3, 1.85), 26, "l")
        self.play(Create(R1), run_time=0.7)
        self.pena(z1, z2, lR1, lag=0.2)
        self.gat("até um retângulo e")
        realce(self, R1, lR1)                                          # o retângulo que contém a região
        self.gat("a fronteira dessas regiões")
        fr = VGroup(curva(M1, cX(c_b21, a, b), AL, 2.5, z=6), curva(M1, cX(d_b21, a, b), AL, 2.5, z=6),
                    curva(M1, [(a, c_b21(a)), (a, d_b21(a))], AL, 2.5, z=6), curva(M1, [(b, c_b21(b)), (b, d_b21(b))], AL, 2.5, z=6))
        self.play(Create(fr), run_time=0.8)
        self.play(FadeOut(fr), run_time=0.5)
        self.remove(fr)
        self.gat("no máximo dois saltos")
        M2 = Lat(760, 470, 190, 70)
        ff = lambda Y: 1.3 + .35 * math.sin(2.2 * Y)
        e2_ = seta_px(M2.px(-.05, 0), M2.px(2.15, 0), E2, 2.5, 14, z=6)
        q = M2.px(2.15, 0)
        ly2 = TC(r"\Y", q[0] + 20, q[1], 28, "c")
        p2a = curva(M2, [(0, 0), (.5, 0)], CI, 4, z=5)
        p2f = curva(M2, cX(ff, .5, 1.55, 50), CI, 4, z=5)
        p2b = curva(M2, [(1.55, 0), (2.05, 0)], CI, 4, z=5)
        j1 = curva(M2, [(.5, 0), (.5, ff(.5))], AL, 2, dash=(5, 5), z=4)
        j2 = curva(M2, [(1.55, 0), (1.55, ff(1.55))], AL, 2, dash=(5, 5), z=4)
        l0a = TC("0", *M2.px(.25, .45), 26, "c")
        lf2 = TC(r"\f", *M2.px(1.0, ff(1.0) + .6), 28, "c")
        l0b = TC("0", *M2.px(1.8, .45), 26, "c")
        self.play(Create(pns[1]), GrowFromPoint(e2_, M2.P(0, 0)), run_time=0.5)
        self.pena(tts[1], ly2)
        self.play(Create(p2a), run_time=0.3)
        self.play(Create(p2f), Create(j1), run_time=0.5)
        self.play(Create(p2b), Create(j2), run_time=0.3)
        self.pena(l0a, lf2, l0b, lag=0.15)
        self.gat("entra numa curva e")
        tese = L([("a", r"\iint_B\f="), ("io", r"\int_{\Am a}^{\Am b}\!"), ("ii", r"\int_{\Az{c(\X)}}^{\Co{d(\X)}}"), ("r1", r"\f\,\dY\,\dX="),
                  ("jo", r"\int_{\Mg c}^{\Mg d}\!"), ("ji", r"\int_{\Az{a(\Y)}}^{\Co{b(\Y)}}"), ("r2", r"\f\,\dX\,\dY")], 960, 660, 46, "c")
        self.pena(tese, passo=0.06)

        def lims(ch):
            g_ = list(gl(tese, ch))
            a_ = max(g_, key=lambda x: x.height)
            return VGroup(*[x for x in g_ if x is not a_])
        self.gat("os limites de fora")
        acende(self, (lims("io"), E1), (lims("jo"), E2), rt=0.9)
        self.gat("os de dentro dependem")
        acende(self, (lims("ii"), CORAL), (lims("ji"), CORAL), rt=0.9)
        self.gat("só da variável de")
        realce(self, t1_, c1, d1)                                      # a fatia em pé de c(x) a d(x)
        self.gat("quando a ordem muda")
        realce(self, p2a, p2f, p2b)                                    # o perfil da fatia: 0, f, 0
        self.gat("virar um retângulo")
        realce(self, t1_, reg1)
        M3 = Lat(1380, 480, 300, 230)
        a3 = regiao(M3, [(0, 0)] + cX(gs, 0, 1.15) + [(1.15, 0)], mixh(BG_, CI, .18), z=2)
        c3 = curva(M3, cX(gs, 0, 1.15), CI, 3)
        r3 = poly_px([M3.px(0, 0), M3.px(.6, 0), M3.px(.6, gs(.6)), M3.px(0, gs(.6))], mixh(BG_, CI, .35), z=3)
        r3.set_stroke(E2, W(4), 1)
        e3_ = seta_px(M3.px(-.02, 0), M3.px(1.25, 0), E1, 2.5, 14, z=6)
        q = M3.px(1.25, 0)
        lx3 = TC(r"\X", q[0] + 20, q[1], 28, "c")
        self.pena(tts[2], lx3, extra=[FadeIn(pns[2]), FadeIn(a3), FadeIn(c3), FadeIn(e3_)])     # handoff final D9: nasce inteiro
        self.play(GrowFromEdge(r3, DOWN), run_time=0.7)
        self.gat("o fator que faltava")
        realce(self, tese, cor=MEN, f=.35)                             # a tese que a síntese lê
        self.play(r3.animate.set_stroke(width=W(7)), run_time=0.4)
        self.play(r3.animate.set_stroke(width=W(4)), run_time=0.4)
        selos = [("QUARTO DE DISCO:", r"\pi", 100, "deu pi", 40), ("TRAVADA:", r"(1-1/e)/2", 690, "um menos um sobre", 34),
                 ("TROCAR = RELER", None, 1280, "reler a mesma região", 0)]
        for t, tex, X, gg, sz in selos:
            self.gat(gg)
            mol, ck, tt = caixa_ok(X, 860, 540, t)
            self.play(Create(mol), Create(ck), run_time=0.4)
            if tex:
                mt = TC(tex, pxof(tt.get_right())[0] + 16, 856, sz, "l")
                self.pena(tt, mt, lag=0.3)
            else:
                self.pena(tt)
        self.marca("v2_13", agora=True)

        # ── S2 · o próximo vídeo e CTA (alvo 26) ──
        self.an("S2")
        self.secao("NO PRÓXIMO VÍDEO")
        # ── S2 (handoff v3 §6, alvo v3_07): o problema acontecendo — a saída da fatia deitada troca de curva em y = 3 ──
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
        rx_ = curva(V, cX(lambda a: a, 0, 3), CORAL, 4)                 # a reta (saída lá embaixo)
        pl_ = curva(V, cX(pa, 0, 2), AZC, 4)                            # ramo esquerdo da parábola (entrada da deitada)
        pr_ = curva(V, cX(pa, 2, 3), CORAL, 4)                          # ramo direito (a saída depois de y = 3)
        t3 = tick(V, "x", 3, r"\Am{3}")
        t3y, t4y = tick(V, "y", 3, r"\Mg{3}"), tick(V, "y", 4, r"\Mg{4}")
        self.play(FadeIn(reg), Create(rx_), Create(pl_), Create(pr_), Create(t3[0]), Create(t3y[0]), Create(t4y[0]), run_time=1.1)
        self.pena(t3[1], t3y[1], t4y[1], lag=0.1)
        eq_ = mixl([("m", r"\Co{\Y=4\X-\X^2}"), ("t", "E"), ("m", r"\Co{\Y=\X}")], 1120, 260, 34)
        self.pena(*eq_.p, lag=0.15)
        self.gat("em pé é uma")                              # a tira em pé atravessa em 1 s: uma conta só
        xt = ValueTracker(.3)
        self.add(xt)
        tv = always_redraw(lambda: tiraV(V, xt.get_value(), xt.get_value(), pa(xt.get_value()), h=.1))
        self.play(FadeIn(tv), run_time=0.3)
        self.play(xt.animate.set_value(2.6), run_time=1.0)
        self.play(FadeOut(tv), run_time=0.3)
        tv.clear_updaters()
        self.remove(tv, xt)
        um_ = leg("EM PÉ: UMA CONTA", 1120, 340, E1, "left", 28)
        self.pena(um_)
        self.gat("agora deitado")                            # a tira deitada começa embaixo: entra na parábola (azul-claro), sai na reta (coral)
        yt = ValueTracker(1.5)
        self.add(yt)
        sai_ = lambda y: y if y <= 3 else xr(y)
        th = always_redraw(lambda: tiraH(V, yt.get_value(), xl(yt.get_value()), sai_(yt.get_value()), h=.1))
        ph1 = always_redraw(lambda: ponto_px(*V.px(xl(yt.get_value()), yt.get_value()), AZC, 9))
        ph2 = always_redraw(lambda: ponto_px(*V.px(sai_(yt.get_value()), yt.get_value()), CORAL, 9))
        self.play(FadeIn(th), FadeIn(ph1), FadeIn(ph2), run_time=0.4)
        fant = tiraH(V, 1.5, xl(1.5), 1.5, h=.1, alpha=.55 * .35)        # a cópia em y = 1,5 fica apagada, para comparar
        self.gat("mas quando ela")                            # a linha y = 3 (ALERTA) aparece um instante antes da passagem
        l3 = curva(V, [(0, 3), (3.6, 3)], AL, 2, dash=(7, 6), z=5)
        self.add(fant)
        self.play(Create(l3), yt.animate.set_value(2.55), run_time=1.6, rate_func=linear)
        self.play(yt.animate.set_value(3.0), run_time=1.2, rate_func=linear)
        self.gat("a saída troca")
        st_ = leg("A SAÍDA TROCA", *V.px(3.75, 3), AL, "left", 28)
        self.play(yt.animate.set_value(3.5), run_time=1.6, rate_func=linear)
        self.pena(st_)
        for m in (th, ph1, ph2):
            m.clear_updaters()
        self.remove(yt)
        self.gat("lida pelo eixo")                           # glyph map na coluna: y = 4x − x² ⇒ x = 2 ∓ √(4 − y); os rótulos voam para o desenho
        G1 = L([("y", r"\Co{\Y=4\X-\X^2}"), ("im", r"\ \Rightarrow\ "), ("x", r"\X=2\mp\sqrt{4-\Y}")], 1120, 440, 36, caneta=False)
        voos(self, [(eq_.p[0].copy(), parte(G1, sel(G1, "y"), "y = 4x − x²"))], rt=0.8)
        self.gat("vira duas curvas")
        self.pena(parte(G1, sel(G1, ["im", "x"]), "⇒ x = 2 ∓ √(4 − y)"))
        G1._esc = True
        ra = rot(V, r"\Az{\X=2-\sqrt{4-\Y}}", (xl(2.0), 2.0), 14, 0, 26, "l")
        rb = rot(V, r"\Co{\X=2+\sqrt{4-\Y}}", (xr(3.6), 3.6), 20, -6, 28, "l")
        xg = VGroup(*gl(G1, "x"))
        voos(self, [(xg.copy(), ra.f), (xg.copy(), rb.f)], rt=1.0, extra=[FadeIn(ra[0]), FadeIn(rb[0])])
        self.gat("quantas contas aparecem")
        realce(self, th, ph1, ph2)
        self.marca("v3_07a", agora=True)
        # o cartão: entra no gatilho falado e fica ≥ 8 s; os três itens acendem um a um, na voz
        self.gat("no próximo vídeo os")
        col = [*eq_.p, um_, G1]
        pn = painel(1120, 200, 740, 560)
        n1 = leg("NO PRÓXIMO VÍDEO:", 1160, 260, GEO, "left", 30)
        n2 = T("EXERCÍCIOS DO MÓDULO", 1160, 330, 40)
        print(f"[cartao] entra {self.t:.2f}")
        self.play(*[FadeOut(m) for m in col], Create(pn), run_time=0.5)
        self.remove(*col)
        self.pena(n1, n2, lag=0.3)
        self.gat("essa parábola uma")
        i1 = T("1. A PARÁBOLA VIRA DUAS CURVAS", 1160, 435, 32, "left", MEN)
        self.pena(i1, extra=[])
        realce(self, pl_, pr_)
        self.gat("seno de ípsilon sobre")
        i2 = mixl([("t", "2.", MEN), ("m", r"\dfrac{\sen\Y}{\Y}"), ("t", "SÓ SAI TROCANDO", MEN)], 1160, 540, 34)
        self.pena(*i2.p, lag=0.12)
        self.gat("dois cilindros que")
        i3 = T("3. DOIS CILINDROS:", 1160, 640, 32, "left", MEN)
        i3b = T("UM VOLUME SEM π", 1210, 690, 32, "left", MEN)
        self.pena(i3, i3b, lag=0.3)
        self.marca("v3_07", agora=True)
        self.gat("deixa o like")
        print(f"[cartao] sai {self.t:.2f}")
        logo_cta(self)
