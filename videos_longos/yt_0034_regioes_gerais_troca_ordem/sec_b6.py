"""yt_0034 · B6 · seno de x³ (alvo 20). Glyph map 12. Leitura deitada pelos limites; a curva x = √y é a parábola y = x² e troca de papel
(entrada azul-claro na tira deitada → saída coral na tira em pé). Painel lateral pequeno (≈ 40 % do alvo 16) no canto vazio do palco (em cima,
à esquerda: o canto de baixo à direita é a própria região), com a miniatura do retângulo do sino por 2–3 s."""
from pecas34 import *

par = lambda a: a * a
X0 = .72


class PB6(B34):
    ANTES = "OUTRA INTEGRAL TRAVADA"

    def corpo(self):
        # ── B6-1 (handoff v3 §5, P5/P6): a fórmula nasce na coluna com o palco já armado; os limites voam na ordem da voz; a região é pintada
        #    por tiras em pé, da esquerda para a direita, só depois da curva lida; a conta C7 inteira (u = x³) ──
        self.an("B6-1")
        g = papel_v(TRI, (0, 1.12, 0, 1.12))
        self.grade = g
        sx, sy, lx, ly = eixos_v(TRI, 1.2, 1.2)
        pecasA = [("io", r"\int_{\Mg{0}}^{\Mg{1}}\!"), ("ii", r"\int_{\Az{\sqrt{\Y}}}^{\Co{1}}"), ("s", r"\sen(\X^3)"), ("dx", r"\,\dX"), ("dy", r"\,\dY")]
        A = L(pecasA, 1120, 210, 40)
        for m in (lx, ly):
            ja_escrita(m)
        self.add(g, sx, sy, lx, ly)                                     # palco armado já no quadro 0 (nunca vazio)
        self.pena(parte(A, sel(A, "io"), "∫₀¹"), passo=0.08)
        lo = sorted([x for x in gl(A, "io") if x.height < max(y.height for y in gl(A, "io"))], key=lambda x: x.get_center()[1])
        t0 = TC(r"\Mg{0}", *TRI.px(0, 0), 28, "r").shift(LEFT * 22 / 120 + UP * 28 / 120)      # folga ≥ 12 px dos dois eixos
        t1 = tick(TRI, "y", 1, r"\Mg{1}")
        self.play(Create(t1[0]), run_time=0.2)
        voos(self, [(lo[0], t0), (lo[1], t1[1])], rt=0.8)               # 0 e 1 voam para o eixo y
        self.pena(parte(A, [k for k in range(len(A[0])) if k not in sel(A, "io")], "resto"), passo=0.07)
        A._esc = True
        self.gat("integral de zero a")
        acende(self, (gl(A, "io"), None), rt=0.3)
        realce(self, t0, t1[1], cor=E2)
        self.gat("raiz de ípsilon até")                     # a curva x = √y traçada de baixo para cima; a reta x = 1
        ii = list(gl(A, "ii"))
        alto = max(ii, key=lambda x: x.height)
        inf = VGroup(*[x for x in ii if x is not alto and x.get_center()[1] < alto.get_center()[1]])
        sup = VGroup(*[x for x in ii if x is not alto and x.get_center()[1] > alto.get_center()[1]])
        cv = curva(TRI, cX(par, 0, 1), AZC, 4)
        x1 = curva(TRI, [(1, 0), (1, 1)], CORAL, 4)
        risca_voando(self, [(inf, cv)], rt=1.1)
        rcv = rot(TRI, r"\Az{\X=\sqrt{\Y}}", (.55, .32), -24, -14, 30, "r")
        self.pena(rcv)
        risca_voando(self, [(sup, x1)], rt=0.9)
        rx1 = rot(TRI, r"\Co{\X=1}", (1, .75), 22, 0, 30, "l")
        self.pena(rx1)
        self.gat("de seno de xis")
        acende(self, (gl(A, "s"), None), rt=0.5)
        self.gat("dê xis dê")
        acende(self, (gl(A, "dx", "dy"), None), rt=0.5)
        self.gat("a primitiva de seno")
        realce(self, cv, x1)
        self.gat("também não se escreve")
        spc = mixl([("m", r"\sen(\X^3)"), ("t", "SEM PRIMITIVA EM FÓRMULA", AL)], 1120, 300, 30)
        self.pena(*spc.p, lag=0.12)
        realce(self, t0, t1[0], t1[1], cor=E2)
        self.gat("então o método")
        realce(self, cv, x1)
        self.gat("desenha ípsilon de")
        realce(self, t1[0], sy, cor=E2)
        self.gat("cada fatia deitada")
        th = tiraH(TRI, .5, math.sqrt(.5), 1)
        pe, ps = pontos_es(TRI, (math.sqrt(.5), .5), (1, .5))
        self.play(GrowFromEdge(th, LEFT), FadeIn(pe, scale=.5), FadeIn(ps, scale=.5), run_time=0.8)
        self.gat("entra na curva")
        realce(self, cv, rcv)
        self.gat("e sai em xis")
        realce(self, x1, rx1)
        # "pelo outro eixo": x = √y ⇔ y = x² (o quadrado atravessa) e a curva troca de rótulo e de cor (vira a saída da tira em pé)
        self.gat("pelo outro eixo")
        N0 = L([("l", r"\Az{\X=\sqrt{\Y}}")], 1120, 410, 40, caneta=False)
        voa(self, rcv.f, N0, rt=1.0)
        N1 = L([("l", r"\Az{\X=\sqrt{\Y}}"), ("eq", r"\ \Leftrightarrow\ "), ("r", r"\Co{\Y=\X^2}")], 1120, 410, 40)
        passo(self, N0, N1, [("l", "l")], rt=0.5, nota="mapa 12a (B6-1: x = √y ⇔ y = x², o quadrado atravessa)")
        self.gat("é a parábola")
        cv2 = curva(TRI, cX(par, 0, 1), CORAL, 4)
        rcv2 = rot(TRI, r"\Co{\Y=\X^2}", (.55, .32), -24, -14, 30, "r")
        ja_escrita(rcv2.f)
        x1d = curva(TRI, [(1, 0), (1, 1)], GEO, 2, dash=(6, 7), z=3)
        self.play(ReplacementTransform(cv, cv2), ReplacementTransform(rcv, rcv2), ReplacementTransform(x1, x1d), FadeOut(rx1), FadeOut(th), FadeOut(pe),
                  FadeOut(ps), run_time=1.2)
        self.remove(rx1, th, pe, ps)
        self.play(FadeOut(N1), run_time=0.4)
        self.remove(N1)
        ja_escrita(rcv2.f)
        t1x = tick(TRI, "x", 1, r"\Am{1}")
        self.play(Create(t1x[0]), run_time=0.3)
        self.pena(t1x[1])
        self.gat("a região é o pedaço")
        realce(self, cv2, rcv2)
        # P6: a região é pintada por tiras em pé, da esquerda para a direita (nunca Transform de forma)
        self.gat("embaixo da parábola")
        nt = 40
        tir = [poly_px([TRI.px(k / nt, 0), TRI.px((k + 1) / nt, 0), TRI.px((k + 1) / nt, par((k + 1) / nt)), TRI.px(k / nt, par(k / nt))], RB, z=1)
               for k in range(nt)]
        self.play(LaggedStart(*[GrowFromEdge(t_, DOWN) for t_ in tir], lag_ratio=0.12), run_time=1.6)
        reg = regiao(TRI, [(0, 0)] + cX(par, 0, 1) + [(1, 0)])
        self.add(reg)
        self.remove(*tir)
        self.gat("agora fatia em pé")
        tv = tiraV(TRI, X0, 0, X0 * X0)
        pe2, ps2 = pontos_es(TRI, (X0, 0), (X0, X0 * X0))
        r0 = rot(TRI, r"\Az{\Y=0}", (.8, 0), 0, -30, 28)
        self.play(GrowFromEdge(tv, DOWN), FadeIn(pe2, scale=.5), FadeIn(ps2, scale=.5), run_time=0.8)
        self.pena(r0)
        self.gat("ípsilon de zero até")
        B1 = L([("eq", "="), ("io", r"\int_0^1\!"), ("ii", r"\int_{\Az{0}}^{\Co{\X^2}}"), ("s", r"\sen(\X^3)"), ("dy", r"\,\dY"), ("dx", r"\,\dX")], 1120, 400, 40,
               caneta=False)
        jj = list(gl(B1, "ii"))
        alto = max(jj, key=lambda x: x.height)
        supB = [k for k in sel(B1, "ii") if B1[0][k] is not alto and B1[0][k].get_center()[1] > alto.get_center()[1]]
        x2lab = VGroup(*[x for x in rcv2.f[0] if x.get_center()[0] > rcv2.f.get_center()[0]])
        voos(self, [(x2lab.copy(), parte(B1, supB, "x²"))], rt=1.0)                  # o x² voa da parábola para o limite de cima
        self.pena(parte(B1, [k for k in range(len(B1[0])) if k not in supB], "resto"))
        self.gat("como seno de xis")
        realce(self, tv, pe2, ps2)                                     # a fatia em pé, de 0 até x²
        # v2 (D2): os dois painéis da fatia ficam na faixa de baixo da coluna (nada por cima do palco)
        self.gat("não depende de ípsilon")
        realce(self, tv, cor=E1)
        hh = math.sin(X0 ** 3)
        ln = X0 * X0
        pn1 = painel(1120, 705, 350, 300)
        tl1 = leg("ESTA FATIA", 1145, 750, GEO, "left", 26)
        M1 = Lat(1160, 960, 300, 200)
        a1 = seta_px(M1.px(-.03, 0), M1.px(.9, 0), E2, 2.5, 14, z=6)
        f1 = seta_px(M1.px(0, -.03), M1.px(0, .8), CI, 2.5, 14, z=6)
        rp = poly_px([M1.px(0, 0), M1.px(ln, 0), M1.px(ln, hh), M1.px(0, hh)], mixh(BG_, CI, .3), z=5)
        rp.set_stroke(E1, W(4), 1)
        q = M1.px(ln, hh)
        lh = TC(r"\Ci{\sen(\X^3)}", q[0] + 12, q[1] + 4, 26, "l")
        q = M1.px(ln / 2, 0)
        lc = TC(r"\Co{\X^2}", q[0], q[1] + 30, 28, "c")
        self.play(Create(pn1), GrowFromPoint(a1, M1.P(0, 0)), GrowFromPoint(f1, M1.P(0, 0)), run_time=0.5)
        self.pena(tl1)
        self.play(GrowFromEdge(rp, DOWN), run_time=0.6)
        self.pena(lh, lc, lag=0.2)
        realce(self, tv, ps2, rcv2)
        # C7 (handoff v3 §2): a coluna sobe; a integral trocada vira o cabeçalho; a de dentro inteira, com o x² voando da chave do comprimento
        self.gat("e a de dentro dá")
        H_ = L([("io", r"\int_0^1\!"), ("ii", r"\int_{\Az{0}}^{\Co{\X^2}}"), ("s", r"\sen(\X^3)"), ("dy", r"\,\dY"), ("dx", r"\,\dX")], 1120, 190, 36,
               caneta=False)
        ja_escrita(H_)
        self.play(FadeOut(A), *[FadeOut(m) for m in spc.p], FadeOut(gl(B1, "eq")), ReplacementTransform(VGroup(*gl(B1, "io", "ii", "s", "dy", "dx")), H_),
                  run_time=0.7)
        self.remove(A, *spc.p, B1)
        # handoff final D4 · linha a: ∫₀^{x²} sen(x³) dy = sen(x³)·[y]₀^{x²} (o sen(x³) desliza para fora; o y do dy vira o [y], o d sai)
        INT = r"\int_{\Az{0}}^{\Co{\X^2}}"
        Da0 = L([("io", INT), ("s", r"\sen(\X^3)"), ("dy", r"\,\dY")], 1120, 290, 34)
        self.pena(Da0)
        Da = L([("io", INT), ("s", r"\sen(\X^3)"), ("dy", r"\,\dY"), ("e1", "="), ("s2", r"\sen(\X^3)"), ("d", r"\cdot"), ("lb", r"\Big["),
                ("y", r"\Y"), ("rb", r"\Big]"), ("lim", r"_0^{\X^2}")], 1120, 290, 34, caneta=False)
        self.gat("vezes ípsilon de")
        alto0 = max(sel(Da0, "io"), key=lambda k: Da0[0][k].height)
        lim0 = [k for k in sel(Da0, "io") if k != alto0]
        passo(self, Da0, Da, [("io", "io"), ("s", "s"), ("dy", "dy"), (lim0, "lim", {"path_arc": -0.7, "run_time": 0.5}),
                              ("s", "s2", {"path_arc": -1.6, "delay": 0.3, "run_time": 0.6}),
                              ([sel(Da0, "dy")[-1]], "y", {"path_arc": 1.6, "delay": 0.3, "run_time": 0.6})], rt=1.1,
              nota="mapa D4a (B6: o sen(x³) sai da integral; o y do dy vira [y]; os limites passam ao colchete)")
        realce(self, tv, pe2, ps2)
        # linha b: = sen(x³)·(x² − 0) = x² sen(x³) (o x² voa da chave do comprimento; o − 0 acende em GEO e não segue)
        Db1 = L([("e1", "="), ("s", r"\sen(\X^3)"), ("d", r"\cdot"), ("pa", r"\big("), ("x2", r"\X^2"), ("m", "-"), ("z", "0"), ("pc", r"\big)")],
                1120, 370, 34, caneta=False)
        Db = L([("e1", "="), ("s", r"\sen(\X^3)"), ("d", r"\cdot"), ("pa", r"\big("), ("x2", r"\X^2"), ("m", "-"), ("z", "0"), ("pc", r"\big)"),
                ("e2", "="), ("r", r"\X^2\sen(\X^3)")], 1120, 370, 34, caneta=False)
        self.gat("até xis ao quadrado xis")
        zero_lim = min(sel(Da, "lim"), key=lambda k: Da[0][k].get_center()[1])
        passo(self, Da, Db1, [("s2", "s"), ("d", "d"), ([zero_lim], "z")], voos=[(lc.copy(), "x2")],
              rt=0.9, copia=True, nota="mapa D4b (B6: sen(x³) e · descem; o 0 do limite vira o − 0; x² voa da chave)")
        self.gat("xis ao quadrado vezes")
        acende(self, (VGroup(*gl(Db1, "m", "z")), GEO), rt=0.7)
        rr = sel(Db, "r")
        passo(self, Db1, Db, [(k, k) for k in ("e1", "s", "d", "pa", "x2", "m", "z", "pc")] + [("x2", rr[:2], {"path_arc": 2.4, "run_time": 0.5}),
                                                                                              ("s", rr[2:], {"path_arc": 1.2, "delay": 0.45, "run_time": 0.55})], rt=1.1,
              nota="mapa D4c (B6: x² e sen(x³) viram x² sen(x³); o − 0 fica para trás)")
        D1 = Db
        self.gat("no sino o")
        realce(self, tv, ps2, cor=E1)
        self.gat("aqui trouxe xis")
        D2 = L([("i", r"\int_0^1"), ("r", r"\X^2\sen(\X^3)"), ("dx", r"\,\dX")], 1120, 455, 36, caneta=False)
        voos(self, [(VGroup(*gl(D1, "r")).copy(), parte(D2, sel(D2, "r"), "x² sen(x³)"))], rt=0.9)
        self.pena(parte(D2, sel(D2, ["i", "dx"]), "∫ dx"))
        D2._esc = True
        self.gat("quase a derivada de")
        r2 = list(gl(D2, "r"))
        acende(self, (VGroup(*r2[:2]), E1), (VGroup(*r2[-3:-1]), E1), rt=0.9)        # o x² e o x³, juntos
        self.gat("chama u de")
        pain = [pn1, tl1, a1, f1, rp, lh, lc]
        sobe = [m for m in (H_, Da, Db) if m in self.mobjects]
        self.play(*[FadeOut(m) for m in pain], *[m.animate.shift(UP * .5).set_opacity(0) for m in sobe], run_time=0.3)
        self.remove(*pain, *sobe)
        self.play(D2.animate.shift(UP * (455 - 190) / 120), run_time=0.4)   # handoff final D4: a coluna rola (≤ 7 linhas), sem cruzar as que saem
        D3 = L([("u", r"u=\X^3"), ("i1", r"\ \Rightarrow\ "), ("du", r"du=3\X^2\,\dX"), ("i2", r"\ \Rightarrow\ "), ("xd", r"\X^2\,\dX=\dfrac{du}{3}")],
               1120, 290, 34)
        self.pena(parte(D3, sel(D3, "u"), "u = x³"))
        self.gat("dê u é três")
        self.pena(parte(D3, sel(D3, ["i1", "du"]), "⇒ du = 3x² dx"))
        realce(self, reg, cv2)
        self.pena(parte(D3, sel(D3, ["i2", "xd"]), "⇒ x² dx = du/3"))
        D3._esc = True
        self.gat("xis de zero a um")
        D4 = L([("a", r"\X=0\to u=0"), ("q", r"\qquad"), ("b", r"\X=1\to u=1")], 1120, 385, 34)
        self.pena(parte(D4, sel(D4, "a"), "x = 0 → u = 0"), parte(D4, sel(D4, "b"), "x = 1 → u = 1"), lag=0.8)
        realce(self, sx, t1x[0], cor=E1)
        D4._esc = True
        self.gat("fica um terço")
        D5 = L([("a", r"=\dfrac{1}{3}\int_0^1\sen u\,du"), ("e", "="), ("b", r"\dfrac{1}{3}\Big[-\cos u\Big]_0^1")], 1120, 490, 36)
        self.pena(parte(D5, sel(D5, "a"), "= ⅓∫₀¹ sen u du"))
        realce(self, reg, cv2)
        self.gat("a primitiva é menos")
        self.pena(parte(D5, sel(D5, ["e", "b"]), "= ⅓[−cos u]₀¹"))
        realce(self, tv, pe2, ps2)
        D5._esc = True
        self.gat("menos cosseno de um")
        D6 = L([("a", r"=\dfrac{1}{3}(-\cos 1+\cos 0)"), ("e", "="), ("r", r"\dfrac{1-\cos 1}{3}"), ("ap", r"\approx\Me{0{,}153}")], 1120, 610, 36)
        self.pena(parte(D6, sel(D6, "a"), "= ⅓(−cos 1 + cos 0)"))
        realce(self, reg, cor=MEN)
        self.gat("resultado um menos")
        self.pena(parte(D6, sel(D6, ["e", "r"]), "= (1 − cos 1)/3"))
        realce(self, cv2, rcv2)
        self.gat("zero vírgula um")
        self.pena(parte(D6, sel(D6, "ap"), "≈ 0,153"))
        D6._esc = True
        self.marca("v3_b6", agora=True)
        realce(self, reg, cv2, atraso=0.4)
        self.sai_fim()
