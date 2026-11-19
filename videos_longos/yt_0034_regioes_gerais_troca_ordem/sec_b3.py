"""yt_0034 · B3 · a cunha z = y (Three.js cena1): fatia em pé = triângulo (alvos 09 → 10) e fatia deitada = retângulo (alvos 11 → 12).
Pouso lateral duas vezes (perspectiva → dolly-zoom → OrthographicCamera; o painel 2D entra no mesmo quadro em que o PNG 3D sai).
Glyph maps 4, 5, 6 e 7."""
from pecas34 import *
from sec_h import quarto_disco

LAT1 = Lat(200, 880, 300, 300)          # painel lateral da cena 1: 1 m = 300 px nos dois eixos


def corte3d(sc, pal, rt_f=0.9, rt_c=1.0, rt_s=0.5, rt_face=0.5):
    """A faca (só a borda) desce até o lugar, o corte abre (a parte cortada recua), a faca sai para cima e a face cortada acende."""
    sc.play(*pal.anim(rt_f, faca=1.0), run_time=rt_f)
    sc.play(*pal.anim(rt_c, corte=1.0), run_time=rt_c)
    sc.play(*pal.anim(rt_s, faca=0.0), run_time=rt_s)
    sc.play(*pal.anim(rt_face, face=1.0), run_time=rt_face)


def pouso(sc, pal, tgt1, d1, k1, cx1, cy1, rt=2.5, extra_s=()):
    """Pouso lateral: câmera até a vista frontal ao plano da fatia (s linear: a suavização está no cam_pouso), e um quadro na ortográfica."""
    pal.pousa(tgt1, d1, k1, cx1, cy1)
    sc.play(pal.tr["s"].animate(run_time=rt, rate_func=linear).set_value(1.0), *extra_s, run_time=rt)
    sc.wait(1 / FPS)                                  # o último quadro do 3D é o da OrthographicCamera
    print(f"[pouso] {sc.lote} {sc._aid} quadro {sc.nq - 1} cena {pal.cena}")


def troca_para_2d(sc, pal, entram):
    """No mesmo quadro: o PNG 3D sai e o painel 2D entra por cima (sem animação)."""
    pal.fundo.clear_updaters()
    sc.remove(pal.fundo, *pal.tr.values())
    for m in entram:
        for x in m.get_family():
            if getattr(x, "_caneta", False):
                x._esc = True
    sc.add(*entram)


class PB3(B34):
    ANTES = "A CUNHA"

    def corpo(self):
        # ── B3-1 · a cunha: a fatia em pé é um triângulo (alvos 09 → 10) ──
        self.an("B3-1")
        pal = Palco3D(self, "cena1", CAM_P1, v3=True, tipo="pe", cresce=0.0, faca=0.0, corte=0.0, face=0.0, sai=0.0)    # handoff final D10
        pal.fundo.op.set_value(0.0)
        self.add(pal.fundo)
        self.play(pal.fundo.op.animate.set_value(1.0), run_time=0.5)
        lx3 = pal.prende(TC(r"\X", 0, 0, 32, "c"), "ex")
        lf3 = pal.prende(TC(r"\f", 0, 0, 32, "c"), "ez", 30, 34)
        self.pena(lx3, lf3)
        self.gat("densidade que cresce")
        F0 = TC(r"\f(\X,\Y)=\Y", 1120, 280, 48)
        self.pena(F0, extra=pal.anim(1.2, cresce=0.25))
        self.gat("ípsilon quilos por metro")
        ad = leg("ALTURA = DENSIDADE (kg/m²)", 1120, 360, GEO, "left", 28)
        self.pena(ad, extra=pal.anim(1.2, cresce=0.45))
        self.gat("desenhando a densidade")
        self.play(*pal.anim(1.6, cresce=0.7), run_time=1.6)
        self.gat("aparece uma cunha")
        self.play(*pal.anim(1.6, cresce=1.0), run_time=1.6)
        self.gat("em xis igual a")
        ce = mixl([("t", "CORTE EM"), ("m", r"\X=1")], 1120, 485, 48)
        self.pena(*ce.p, lag=0.15, extra=pal.anim(0.8, faca=1.0))
        self.play(*pal.anim(0.9, corte=1.0), run_time=0.9)
        self.play(*pal.anim(0.4, faca=0.0), run_time=0.4)
        self.play(*pal.anim(0.4, face=1.0), run_time=0.4)
        px1 = pal.prende(TP(r"\X=1", 0, 0, 34), "faca", 0, -34)
        pfe = pal.prende(placa_txt("FATIA EM PÉ", 0, 0, E1, 28, "left"), "fatia", -150, 80)
        self.gat("a fatia vai de")
        self.pena(px1, pfe, lag=0.2)
        realce(self, px1, pfe, cor=E1)                                 # a fatia lida no corte
        self.gat("e a altura dela")
        tri = leg("A FATIA EM PÉ É UM TRIÂNGULO", 1120, 580, E1, "left", 30)
        self.pena(tri)
        self.marca("09", agora=True)
        realce(self, pfe, lf3, cor=E1, atraso=0.4)                     # a altura da fatia é a densidade f
        self.gat("é o próprio ípsilon")                # o que está na frente da fatia sai antes; a coluna limpa; os rótulos saem com o objeto
        self.play(*pal.anim(1.0, sai=1.0), *[FadeOut(m) for m in (F0, ad, ce, tri, px1, pfe, lx3, lf3)], run_time=1.0)
        for m in (px1, pfe, lx3, lf3):
            m.clear_updaters()
        self.remove(F0, ad, ce, tri, px1, pfe, lx3, lf3)
        pouso(self, pal, (1, 0, 0), (-1, 0, 0), 300, 200, 880)
        G = lateral(LAT1, 2.1, ymax=2.25, zt=(0, 1, 2), yt=(0, 1, 2), vl=r"\f")
        area = poly_px([LAT1.px(0, 0), LAT1.px(S3, S3), LAT1.px(S3, 0)], mixh(BG_, E1, .58), z=2)
        cont = lin_px([LAT1.px(0, 0), LAT1.px(S3, S3), LAT1.px(S3, 0), LAT1.px(0, 0)], E1, 5, z=4)
        px_ = TP(r"\X=1", 220 + 40, 250 - 10, 30, "c")
        troca_para_2d(self, pal, [G["grade"], G["eh"], G["ev"], G["lh"], G["lv"], G["nums"], area, cont, px_])
        print(f"[pouso2d] B3-1 tri f0={LAT1.px(0, 0)} f1={LAT1.px(S3, 0)} f2={LAT1.px(S3, S3)}")
        # ── C2 (handoff v3 §2): ∫ y dy com colchete, G(b) − G(a), e a de fora com a primitiva inteira ──
        self.gat("a integral de dentro")
        P0 = L([("i", r"\int_{\Az{0}}^{\Co{\sqrt{4-\X^2}}}"), ("y", r"\Y\,\dY"), ("eq", "="), ("br", r"\Big[\dfrac{\Y^2}{2}\Big]_{0}^{\sqrt{4-\X^2}}")],
               1120, 330, 36)
        self.pena(parte(P0, sel(P0, ["i", "y"]), "∫ y dy"))
        realce(self, area, cont)                                       # a fatia triangular que a integral de dentro mede
        percorre(self, LAT1, lambda y: y, 0, S3, dur=4.5, cor=E1)       # palco vivo: o y anda de 0 a √3 sob o teto f = y
        self.gat("é ípsilon ao quadrado")
        self.pena(parte(P0, sel(P0, ["eq", "br"]), "= [y²/2]"))
        P0._esc = True
        self.gat("no limite de cima")
        P1 = L([("eq", "="), ("a", r"\dfrac{\big(\sqrt{4-\X^2}\big)^2}{2}"), ("m", "-"), ("b", r"\dfrac{0^2}{2}")], 1120, 440, 36)
        self.pena(parte(P1, sel(P1, ["eq", "a"]), "= (√(4−x²))²/2"))
        self.gat("no de baixo zero")
        self.pena(parte(P1, sel(P1, ["m", "b"]), "− 0²/2"))
        realce(self, area, cont, cor=E1)
        P1._esc = True
        self.gat("fica quatro menos")
        P2 = L([("eq", "="), ("fr", r"\dfrac{4-\X^2}{2}")], 1120, 545, 36)
        self.pena(P2)
        self.gat("base vezes altura")
        ba = T("BASE · ALTURA / 2", 1120, 230, 36, "left", E1)
        p = LAT1.px(S3 / 2, 0)
        lb1 = leg("BASE", p[0], p[1] + 80, GEO, "center", 26)
        lb2 = TC(r"\Co{\sqrt{4-\X^2}}", p[0], p[1] + 120, 28, "c")
        q = LAT1.px(S3, S3 / 2)
        la1 = leg("ALTURA", q[0] + 24, q[1] - 20, GEO, "left", 26)
        la2 = TC(r"\Co{\sqrt{4-\X^2}}", q[0] + 24, q[1] + 24, 28, "l")
        self.pena(ba)
        bc = curva(LAT1, [(0, 0), (S3, 0)], E1, 8, z=5)
        hc = curva(LAT1, [(S3, 0), (S3, S3)], E1, 8, z=5)
        self.play(Create(bc), run_time=0.4)
        self.pena(lb1, lb2, lag=0.2)
        self.play(FadeOut(bc), Create(hc), run_time=0.4)
        self.pena(la1, la2, lag=0.2)
        self.play(FadeOut(hc), run_time=0.3)
        self.remove(bc, hc)
        self.gat("agora a de fora")
        Q0 = L([("i", r"\int_0^2"), ("fr", r"\dfrac{4-\X^2}{2}"), ("dx", r"\,\dX"), ("eq", "="), ("pr", r"\dfrac{1}{2}\Big[4\X-\dfrac{\X^3}{3}\Big]_0^2")],
               1120, 655, 36, caneta=False)
        voos(self, [(gl(P2, "fr").copy(), parte(Q0, sel(Q0, "fr"), "fr"))], rt=0.9)
        self.pena(parte(Q0, sel(Q0, ["i", "dx"]), "∫ dx"))
        realce(self, area, cont)
        self.gat("o meio sai")
        self.pena(parte(Q0, sel(Q0, ["eq", "pr"]), "= ½[4x − x³/3]"))
        realce(self, la2, lb2, cor=E1)
        Q0._esc = True
        self.gat("em dois oito")
        Q1 = L([("a", r"=\dfrac{1}{2}\Big[\Big(8-\dfrac{8}{3}\Big)"), ("b", r"-(0-0)\Big]")], 1120, 765, 36)
        self.pena(parte(Q1, sel(Q1, "a"), "= ½[(8 − 8/3)"))
        realce(self, area, cont, cor=MEN)
        self.gat("em zero zero")
        self.pena(parte(Q1, sel(Q1, "b"), "− (0 − 0)]"))
        Q1._esc = True
        self.gat("metade de dezesseis")
        Q2 = L([("a", r"=\dfrac{1}{2}\cdot\dfrac{16}{3}"), ("e", "="), ("v", r"\Me{\dfrac{8}{3}}")], 1120, 870, 36)
        self.pena(parte(Q2, sel(Q2, "a"), "= ½ · 16/3"))
        self.gat("oito terços de quilo")
        self.pena(parte(Q2, sel(Q2, ["e", "v"]), "= 8/3"))
        Q2._esc = True
        self.marca("10", agora=True)

        # ── B3-2 · a fatia deitada é um retângulo (alvos 11 → 12) ──
        self.an("B3-2")
        self.secao("A FATIA DEITADA")
        Q = quarto_disco(self)
        self.grade = Q["g"]
        th = tiraH(CH, 1, 0, S3)
        pe, ps = pontos_es(CH, (0, 1), (S3, 1))
        velhos = self.snap()
        self.play(*[FadeOut(m) for m in velhos], run_time=0.3)        # o painel sai (0,3 s) e o disco entra no quadro seguinte
        self.remove(*velhos)
        self.add(Q["g"], Q["reg"], Q["sx"], Q["sy"], Q["arc"])
        for m in (Q["lx"], Q["ly"], Q["t2x"][1], Q["t2y"][1]):
            ja_escrita(m)
        self.add(Q["lx"], Q["ly"], *Q["t2x"], *Q["t2y"])
        self.play(GrowFromEdge(th, LEFT), FadeIn(pe, scale=0.5), FadeIn(ps, scale=0.5), run_time=0.8)
        self.gat("a curva tem que")
        rc = rot(CH, r"\Co{\Y=\sqrt{4-\X^2}}", (1.36, 1.72), 0, 0, 30)
        self.pena(rc, extra=[Q["arc"].animate.set_stroke(width=W(6))])
        self.play(Q["arc"].animate.set_stroke(width=W(4)), run_time=0.4)
        self.gat("ípsilon igual a raiz")
        G0 = L([("y", r"\Co{\Y}"), ("eq", r"\mathrel{\Co{=}}"), ("r", r"\Co{\sqrt{4-\X^2}}")], 1120, 230, 40, caneta=False)
        voa(self, rc.f, G0, rt=1.0)
        self.gat("eleva ao quadrado")
        G1 = L([("y", r"\Y^2"), ("eq", "="), ("q", "4"), ("m", "-"), ("x", r"\X^2")], 1120, 320, 40)
        rr = list(gl(G0, "r"))
        passo(self, G0, G1, [("y", [max(sel(G1, "y"), key=lambda k: G1[0][k].height)]), ("eq", "eq"), (sel(G0, "r"), ["q", "m", "x"])], rt=1.1, copia=True,
              nota="mapa 6a (B3-2: eleva ao quadrado)")
        self.gat("isola o xis")
        G2 = L([("x", r"\X^2"), ("eq", "="), ("q", "4"), ("m", "-"), ("y", r"\Y^2")], 1120, 440, 40)
        passo(self, G1, G2, [("y", "y", {"path_arc": -1.2}), ("x", "x", {"path_arc": -1.2})], rt=1.3, copia=True,
              nota="mapa 6b (B3-2: x² atravessa por cima, y² por baixo; = e − saem e voltam a caneta)")     # handoff final D5
        self.gat("com a raiz positiva")
        G3 = L([("x", r"\Co{\X}"), ("eq", r"\mathrel{\Co{=}}"), ("r", r"\Co{\sqrt{4-\Y^2}}")], 1120, 540, 40)
        xi = sel(G2, "x")
        xb = max(xi, key=lambda k: G2[0][k].height)
        xe = [k for k in xi if k != xb]
        passo(self, G2, G3, [([xb], "x"), ("eq", "eq"), (sel(G2, ["q", "m", "y"]) + xe, "r")], rt=1.1, copia=True,
              nota="mapa 6c (B3-2: x = √(4 − y²))")
        pg = TP(r"\X\ge 0", 1440, 540, 32, "l")
        self.pena(pg)
        self.gat("positivo xis igual")
        realce(self, Q["arc"], rc)                                     # o mesmo arco, lido como x = √(4 − y²)
        rc2 = rot(CH, r"\Co{\X=\sqrt{4-\Y^2}}", (S3, 1), 20, -36, 30)
        self.play(ReplacementTransform(rc, rc2), run_time=0.7)
        ja_escrita(rc2.f)
        # handoff final D10: a mesma peça volta inteira e opaca, de frente para o corte em pé (CAM_P1), e orbita 2 s até ficar de frente
        # para o corte deitado (CAM_D1); só então a faca deitada desce (a peça nunca se separa: y < 1 vira traço)
        pal2 = Palco3D(self, "cena1", CAM_P1, v3=True, tipo="dei", cresce=1.0, faca=0.0, corte=0.0, face=0.0, sai=0.0, lx=2.55, ly=2.5, lz=2.15)
        pal2.fundo.op.set_value(0.0)
        sai = [m for m in self.snap() if m not in (G0, G1, G2, G3, pg)] + [self.grade]
        self.add(pal2.fundo)
        self.play(*[FadeOut(m) for m in sai], pal2.fundo.op.animate.set_value(1.0), run_time=0.4)
        self.remove(*sai)
        self.grade = None
        pal2.rumo(CAM_D1, arco=True)
        self.play(pal2.tr["s"].animate(rate_func=linear).set_value(1.0), run_time=2.0)      # órbita de 2 s com a peça inteira opaca
        lx4 = pal2.prende(TC(r"\X", 0, 0, 32, "c"), "ex")
        lf4 = pal2.prende(TC(r"\f", 0, 0, 32, "c"), "ez", 30, 34)
        ja_escrita(lx4)
        ja_escrita(lf4)
        self.play(FadeIn(lx4), FadeIn(lf4), run_time=0.3)
        self.gat("e olha a fatia")
        self.play(*pal2.anim(0.4, faca=1.0), run_time=0.4)
        self.play(*pal2.anim(0.6, corte=1.0), run_time=0.6)
        self.gat("a altura é ípsilon")
        self.play(*pal2.anim(0.2, faca=0.0), run_time=0.2)
        self.play(*pal2.anim(0.3, face=1.0), run_time=0.3)
        py1 = pal2.prende(TP(r"\Y=1", 0, 0, 34), "faca", 64, -24)
        self.pena(py1)
        self.gat("em todo ponto dela")
        dr = leg("A FATIA DEITADA É UM RETÂNGULO", 1120, 620, E2, "left", 30)
        self.pena(dr)
        self.marca("11", agora=True)
        self.gat("então ela é um")
        self.play(*pal2.anim(0.3, sai=1.0), *[FadeOut(m) for m in (G0, G1, G2, G3, pg, dr, py1, lx4, lf4)], run_time=0.3)
        for m in (py1, lf4):
            m.clear_updaters()
        self.remove(G0, G1, G2, G3, pg, dr, py1, lx4, lf4)
        pouso(self, pal2, (0, 1, 0), (0, 1, 0), 300, 200, 880, rt=1.2)
        G = lateral(LAT1, 2.1, ymax=2.25, zt=(0, 1, 2), yt=(0, 1, 2), hcor=E1, hl=r"\X", vl=r"\f")
        ret = poly_px([LAT1.px(0, 0), LAT1.px(S3, 0), LAT1.px(S3, 1), LAT1.px(0, 1)], mixh(BG_, E2, .35), z=2)
        cont = lin_px([LAT1.px(0, 0), LAT1.px(S3, 0), LAT1.px(S3, 1), LAT1.px(0, 1), LAT1.px(0, 0)], E2, 5, z=4)
        py_ = TP(r"\Y=1", 260, 240, 30, "c")
        troca_para_2d(self, pal2, [G["grade"], G["eh"], G["ev"], G["lh"], G["lv"], G["nums"], ret, cont, py_])
        print(f"[pouso2d] B3-2 ret f0={LAT1.px(0, 0)} f1={LAT1.px(S3, 0)} f2={LAT1.px(S3, 1)} f3={LAT1.px(0, 1)}")
        self.gat("a integral de dentro")
        H0 = L([("i", r"\int_{\Az{0}}^{\Co{\sqrt{4-\Y^2}}}"), ("y", r"\Y\,\dX"), ("eq", "="), ("b", r"\Y\Big[\X\Big]_0^{\sqrt{4-\Y^2}}"), ("e2", "="),
                ("r", r"\Y\sqrt{4-\Y^2}")], 1120, 230, 36)
        self.pena(parte(H0, sel(H0, ["i", "y"]), "∫ y dx"))
        realce(self, ret, cont)                                        # o retângulo da fatia deitada
        self.gat("ípsilon vezes xis")
        self.pena(parte(H0, sel(H0, ["eq", "b"]), "= y[x]"))
        self.gat("altura vezes comprimento")
        p = LAT1.px(S3 / 2, 0)
        lc1 = leg("COMPRIMENTO", p[0], p[1] + 80, GEO, "center", 26)
        lc2 = TC(r"\Co{\sqrt{4-\Y^2}}", p[0], p[1] + 120, 28, "c")
        q = LAT1.px(S3, .5)
        la1 = leg("ALTURA", q[0] + 24, q[1] - 20, GEO, "left", 26)
        la2 = TC(r"\Y", q[0] + 24, q[1] + 22, 30, "l")
        self.pena(la1, la2, lc1, lc2, lag=0.25)
        self.pena(parte(H0, sel(H0, ["e2", "r"]), "= y√(4 − y²)"))
        H0._esc = True
        # C3 (handoff v3 §2): a de fora pela substituição u = 4 − y², com a linha dos limites e o sinal que inverte
        self.gat("agora a de fora")
        K0 = L([("i", r"\int_0^2"), ("r", r"\Y\sqrt{4-\Y^2}"), ("dy", r"\,\dY")], 1120, 330, 36, caneta=False)
        voos(self, [(gl(H0, "r").copy(), parte(K0, sel(K0, "r"), "y√(4 − y²)"))], rt=0.9)
        self.pena(parte(K0, sel(K0, ["i", "dy"]), "∫ dy"))
        K0._esc = True
        self.gat("quase a derivada")
        rr_ = list(gl(K0, "r"))
        acende(self, (VGroup(rr_[0]), MEN), (VGroup(*rr_[-3:]), MEN), rt=0.9)
        self.gat("chama u de")
        K1 = L([("u", r"u=4-\Y^2"), ("i1", r"\ \Rightarrow\ "), ("du", r"du=-2\Y\,\dY"), ("i2", r"\ \Rightarrow\ "), ("yd", r"\Y\,\dY=-\dfrac{du}{2}")],
               1120, 425, 34)
        self.pena(parte(K1, sel(K1, "u"), "u = 4 − y²"))
        self.gat("dê u é menos")
        self.pena(parte(K1, sel(K1, ["i1", "du"]), "⇒ du = −2y dy"))
        self.gat("então ípsilon dê ípsilon")
        dd = list(gl(K1, "du"))
        acende(self, (VGroup(rr_[0]), MEN), (VGroup(*dd[3:6]), MEN), rt=0.6)          # o y que multiplica e o −2y do du, juntos
        self.pena(parte(K1, sel(K1, ["i2", "yd"]), "⇒ y dy = −du/2"))
        K1._esc = True
        self.gat("os limites mudam junto")
        K2 = L([("a", r"\Y=0\to u=4"), ("q", r"\qquad"), ("b", r"\Y=2\to u=0")], 1120, 520, 34)
        self.pena(parte(K2, sel(K2, "a"), "y = 0 → u = 4"))
        self.gat("e ípsilon igual a dois")
        self.pena(parte(K2, sel(K2, "b"), "y = 2 → u = 0"))
        K2._esc = True
        self.gat("o menos inverte")
        K3 = L([("a", r"=-\dfrac{1}{2}\int_4^0\sqrt{u}\,du"), ("e", "="), ("b", r"\dfrac{1}{2}\int_0^4 u^{1/2}\,du")], 1120, 620, 36)
        self.pena(parte(K3, sel(K3, "a"), "= −½∫₄⁰ √u du"))
        realce(self, ret, cont)
        self.gat("fica meio da")
        self.pena(parte(K3, sel(K3, ["e", "b"]), "= ½∫₀⁴ u^{1/2} du"))
        K3._esc = True
        self.gat("a primitiva de raiz")
        K4 = L([("a", r"=\dfrac{1}{2}\Big[\dfrac{2}{3}u^{3/2}\Big]_0^4"), ("b", r"=\dfrac{1}{2}\cdot\dfrac{2}{3}\cdot 8"), ("c", r"="), ("v", r"\Me{\dfrac{8}{3}}")],
               1120, 725, 36)
        self.pena(parte(K4, sel(K4, "a"), "= ½[⅔u^{3/2}]₀⁴"))
        self.gat("e quatro elevado a")
        realce(self, ret, cont, cor=MEN)
        realce(self, la2, lc2, cor=MEN)
        self.gat("meio vezes dois terços")
        self.pena(parte(K4, sel(K4, "b"), "= ½·⅔·8"))
        self.gat("oito terços de novo")
        self.pena(parte(K4, sel(K4, ["c", "v"]), "= 8/3"))
        K4._esc = True
        ck = check_px(1840, 725)
        self.play(Create(ck), run_time=0.4)
        self.marca("12", agora=True)

        # ── as fatias como funções (handoff v3 §3.2; alvo v3_04): duas curvas de área, mesma área embaixo ──
        self.gat("agora olha as fatias")
        self.secao("A ÁREA DE CADA FATIA")
        tri_ = poly_px([LAT1.px(0, 0), LAT1.px(S3, S3), LAT1.px(S3, 0)], mixh(BG_, E1, .58), z=3)     # a face do pouso do B3-1
        tri_.set_stroke(E1, W(3), 1)
        col = [H0, K0, K1, K2, K3, K4, ck]
        lat = [G["grade"], G["eh"], G["ev"], G["lh"], G["lv"], G["nums"], py_, la1, la2, lc1, lc2, cont]
        GA, GB = Lat(150, 780, 200, 240), Lat(640, 780, 200, 240)
        Ax = lambda x: (4 - x * x) / 2
        Ay = lambda y: y * math.sqrt(max(0.0, 4 - y * y))
        # handoff final D1: antes de qualquer eixo, as faces do pouso encolhem e viram os pontos (1; 1,5) em A(x) e (1; 1,73) em A(y),
        # em 0,6 s; o resto do pouso sai em 0,4 s, junto
        p1 = ponto_px(*GA.px(1, Ax(1)), E1, 11, z=9)
        p2 = ponto_px(*GB.px(1, Ay(1)), E2, 11, z=9)
        self.play(ReplacementTransform(tri_, p1), ReplacementTransform(ret, p2), *[FadeOut(m, rate_func=lambda t: min(1.0, 1.5 * t)) for m in col + lat],
                  run_time=0.6)
        self.remove(*col, *lat)

        def eixos_area(Gv, cor, lb):
            gg = VGroup()
            for k in range(0, 9):
                gg.add(lin_px([Gv.px(k * .25, 0), Gv.px(k * .25, 2.0)], GRADE, 1.2, z=-9))
                gg.add(lin_px([Gv.px(0, k * .25), Gv.px(2.0, k * .25)], GRADE, 1.2, z=-9))
            eh = seta_px(Gv.px(-.02, 0), Gv.px(2.12, 0), cor, 3, 16, z=6)
            ev = seta_px(Gv.px(0, -.02), Gv.px(0, 2.1), GEO, 3, 16, z=6)
            q = Gv.px(2.12, 0)
            lh = TC(lb, q[0] + 24, q[1], 32, "c")
            n0 = TC(r"\Am{0}" if lb == r"\X" else r"\Mg{0}", *Gv.px(0, 0), 26, "c").shift(DOWN * 30 / 120)
            n2 = TC(r"\Am{2}" if lb == r"\X" else r"\Mg{2}", *Gv.px(2, 0), 26, "c").shift(DOWN * 30 / 120)
            return gg, eh, ev, lh, n0, n2

        ga = eixos_area(GA, E1, r"\X")
        gb = eixos_area(GB, E2, r"\Y")
        self.grade = VGroup(ga[0], gb[0])
        self.play(FadeIn(ga[0]), FadeIn(gb[0]), GrowFromPoint(ga[1], GA.P(0, 0)), GrowFromPoint(ga[2], GA.P(0, 0)),
                  GrowFromPoint(gb[1], GB.P(0, 0)), GrowFromPoint(gb[2], GB.P(0, 0)), run_time=0.6)
        self.pena(ga[3], ga[4], ga[5], gb[3], gb[4], gb[5], lag=0.05, passo=0.04)
        self.gat("em pé a área")
        ta = T("EM PÉ: TRIÂNGULOS", 150, 240, 32, "left", E1)
        self.pena(ta)
        xa = ValueTracker(0.0)
        self.add(xa)
        cva = always_redraw(lambda: curva(GA, cX(Ax, 0, max(.002, xa.get_value()), 60), E1, 4, z=6))
        pa = always_redraw(lambda: ponto_px(*GA.px(xa.get_value(), Ax(xa.get_value())), E1, 9, z=8))
        self.add(cva, pa)
        self.play(xa.animate.set_value(2.0), run_time=2.0, rate_func=linear)
        cva.clear_updaters()
        self.remove(pa, xa)
        self.gat("é quatro menos xis")
        tE = T("EM PÉ", 1120, 252, 30, "left", E1)
        FA = TC(r"A(\X)=\dfrac{4-\X^2}{2}", 1240, 252, 38, "l")
        self.pena(tE, FA, lag=0.2)
        d1 = curva(GA, [(1, 0), (1, Ax(1))], E1, 2, dash=(6, 6), z=5)
        l1 = TP(r"\X=1", *GA.px(1.25, Ax(1) + .2), 28, "l")
        self.play(Create(d1), run_time=0.4)
        self.pena(l1)
        self.gat("deitada a área")
        tb_ = T("DEITADA: RETÂNGULOS", 640, 240, 32, "left", E2)
        self.pena(tb_)
        xb = ValueTracker(0.0)
        self.add(xb)
        cvb = always_redraw(lambda: curva(GB, cX(Ay, 0, max(.002, xb.get_value()), 90), E2, 4, z=6))
        pb = always_redraw(lambda: ponto_px(*GB.px(xb.get_value(), Ay(xb.get_value())), E2, 9, z=8))
        self.add(cvb, pb)
        self.play(xb.animate.set_value(2.0), run_time=2.0, rate_func=linear)
        cvb.clear_updaters()
        self.remove(pb, xb)
        self.gat("é ípsilon vezes raiz")
        tD = T("DEITADA", 1120, 412, 30, "left", E2)
        FB = TC(r"A(\Y)=\Y\sqrt{4-\Y^2}", 1260, 412, 38, "l")
        self.pena(tD, FB, lag=0.2)
        percorre(self, GB, Ay, 0, 2, dur=4.0, cor=E2)                  # palco vivo: A(y) lido de y = 0 a 2
        d2 = curva(GB, [(1, 0), (1, Ay(1))], E2, 2, dash=(6, 6), z=5)
        l2 = TP(r"\Y=1", GB.px(1, 0)[0] - 16, GB.px(0, Ay(1) + .05)[1] - 6, 28, "r")
        self.play(Create(d2), run_time=0.4)
        self.pena(l2)
        self.gat("a mesma oito terços")
        aa = poly_px([GA.px(0, 0)] + [GA.px(x, Ax(x)) for x in np.linspace(0, 2, 60)] + [GA.px(2, 0)], mixh(BG_, E1, .3), z=2)
        ab = poly_px([GB.px(0, 0)] + [GB.px(y, Ay(y)) for y in np.linspace(0, 2, 90)] + [GB.px(2, 0)], mixh(BG_, E2, .3), z=2)
        self.play(GrowFromEdge(aa, LEFT), GrowFromEdge(ab, LEFT), run_time=0.9)
        va = TC(r"\Me{\dfrac{8}{3}}", *GA.px(.55, .55), 30, "c")
        vb = TC(r"\Me{\dfrac{8}{3}}", *GB.px(.5, .55), 30, "c")
        FI = TC(r"\int_0^2 A(\X)\,\dX=\int_0^2 A(\Y)\,\dY=\Me{\dfrac{8}{3}}", 1120, 570, 38)
        self.pena(va, vb, lag=0.2)
        self.pena(FI)
        self.gat("isso é o fubini")
        percorre(self, GA, Ax, 0, 2, dur=4.0, cor=E1)                  # palco vivo: A(x) lido de x = 0 a 2
        cd = T("CURVAS DIFERENTES, MESMA ÁREA", 1120, 690, 32, "left", MEN)
        self.pena(cd)
        self.marca("v3_04", agora=True)
        self.gat("a soma das áreas")
        realce(self, aa, ab, cor=MEN, atraso=0.4)
        self.gat("guarda essa diferença")
        pn = painel(1120, 760, 760, 150)
        c1 = T("EM PÉ: ALTURA MUDA → TRIÂNGULO", 1150, 805, 28, "left", E1)
        c2 = T("DEITADA: ALTURA FIXA → RETÂNGULO", 1150, 865, 28, "left", E2)
        self.play(Create(pn), run_time=0.5)
        self.pena(c1)
        self.pena(c2)
        self.gat("na direção em que")
        realce(self, cvb, ab, cor=E2)
        self.gat("vira altura vezes")
        realce(self, p2, d2)
        self.gat("o fator que falta")
        fb = list(FB[0])
        acende(self, (VGroup(*fb[-7:]), CORAL), rt=1.2)                # o comprimento √(4 − y²): o fator que a conta de fora aproveita
        realce(self, cvb, cor=CORAL, atraso=0.0)
        self.sai_fim(rt=0.25)                         # palco vazio ≤ 0,5 s na virada para o PB4
