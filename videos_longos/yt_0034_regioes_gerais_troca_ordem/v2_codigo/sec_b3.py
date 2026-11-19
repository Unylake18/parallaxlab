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
        pal = Palco3D(self, "cena1", CAM_B31, tipo="pe", cresce=0.0, faca=0.0, corte=0.0, face=0.0, sai=0.0)
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
        area = poly_px([LAT1.px(0, 0), LAT1.px(S3, S3), LAT1.px(S3, 0)], mixh(BG_, E1, .35), z=2)
        cont = lin_px([LAT1.px(0, 0), LAT1.px(S3, S3), LAT1.px(S3, 0), LAT1.px(0, 0)], E1, 5, z=4)
        px_ = TP(r"\X=1", 220 + 40, 250 - 10, 30, "c")
        troca_para_2d(self, pal, [G["grade"], G["eh"], G["ev"], G["lh"], G["lv"], G["nums"], area, cont, px_])
        print(f"[pouso2d] B3-1 tri f0={LAT1.px(0, 0)} f1={LAT1.px(S3, 0)} f2={LAT1.px(S3, S3)}")
        self.gat("a integral de dentro")
        P0 = L([("i", r"\int_{\Az{0}}^{\Co{\sqrt{4-\X^2}}}"), ("y", r"\Y\,\dY")], 1120, 370, 40)
        self.pena(P0)
        self.gat("dá ípsilon ao quadrado")
        P1 = L([("i", r"\int_{\Az{0}}^{\Co{\sqrt{4-\X^2}}}"), ("y", r"\Y\,\dY"), ("eq", "="), ("fr", r"\dfrac{\Y^2}{2}"), ("bar", r"\Big|_{0}^{\sqrt{4-\X^2}}")],
               1120, 370, 40)
        ii = list(gl(P0, "i"))
        alto = max(ii, key=lambda x: x.height)
        lim = VGroup(*[x for x in ii if x is not alto])
        ib = list(gl(P1, "bar"))
        barra = max(ib, key=lambda x: x.height)
        passo(self, P0, P1, [("i", "i"), ("y", "y")], voos=[(lim.copy(), [k for k in sel(P1, "bar") if P1[0][k] is not barra])], rt=0.6,
              nota="mapa 4a (B3-1: ∫ y dy = y²/2 |)")
        self.gat("ou seja quatro menos")
        P2 = L([("eq", "="), ("fr", r"\dfrac{4-\X^2}{2}")], 1160, 480, 44)
        num = [k for k in sel(P2, "fr") if P2[0][k].get_center()[1] > P2.get_center()[1] + 0.02]
        den = [k for k in sel(P2, "fr") if k not in num]
        sup_bar = [k for k in sel(P1, "bar") if P1[0][k].get_center()[1] > P1.get_center()[1] + 0.05 and P1[0][k] is not barra]
        den1 = [k for k in sel(P1, "fr") if P1[0][k].get_center()[1] <= P1.get_center()[1] + 0.02]
        passo(self, P1, P2, [("eq", "eq"), (sup_bar, num), (den1, den)], rt=1.3, copia=True, nota="mapa 4b (B3-1: o quadrado come a raiz)")
        self.gat("base vezes altura")
        ba = T("BASE · ALTURA / 2", 1120, 240, 40, "left", E1)
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
        self.gat("somando as fatias")
        Q0 = L([("i", r"\int_0^2"), ("fr", r"\dfrac{4-\X^2}{2}"), ("dx", r"\,\dX")], 1120, 620, 40, caneta=False)
        voos(self, [(gl(P2, "fr").copy(), parte(Q0, sel(Q0, "fr"), "fr"))], rt=0.9)
        self.pena(parte(Q0, sel(Q0, ["i", "dx"]), "∫ dx"))
        Q0._esc = True
        self.gat("oito menos oito terços")
        Q1 = L([("i", r"\int_0^2"), ("fr", r"\dfrac{4-\X^2}{2}"), ("dx", r"\,\dX"), ("eq", "="), ("r", r"\dfrac{8-8/3}{2}")], 1120, 620, 40)
        passo(self, Q0, Q1, [("i", "i"), ("fr", "fr"), ("dx", "dx")], rt=0.6, nota="mapa 5a (B3-1: ∫₀² (4 − x²)/2 dx = (8 − 8/3)/2)")
        self.gat("oito terços de quilo")
        Q2 = L([("i", r"\int_0^2"), ("fr", r"\dfrac{4-\X^2}{2}"), ("dx", r"\,\dX"), ("eq", "="), ("r", r"\dfrac{8-8/3}{2}"), ("e2", "="), ("v", r"\dfrac{8}{3}")],
               1120, 620, 40)
        passo(self, Q1, Q2, [(k, k) for k in ("i", "fr", "dx", "eq", "r")], rt=0.6, nota="mapa 5b (B3-1: = 8/3)")
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
        G2 = L([("x", r"\X^2"), ("eq", "="), ("q", "4"), ("m", "-"), ("y", r"\Y^2")], 1120, 410, 40)
        passo(self, G1, G2, [("y", "y"), ("eq", "eq"), ("q", "q"), ("m", "m"), ("x", "x")], rt=1.3, copia=True,
              nota="mapa 6b (B3-2: x² e y² atravessam a igualdade, cada um trocando de sinal)")
        self.gat("com a raiz positiva")
        G3 = L([("x", r"\Co{\X}"), ("eq", r"\mathrel{\Co{=}}"), ("r", r"\Co{\sqrt{4-\Y^2}}")], 1120, 500, 40)
        xi = sel(G2, "x")
        xb = max(xi, key=lambda k: G2[0][k].height)
        xe = [k for k in xi if k != xb]
        passo(self, G2, G3, [([xb], "x"), ("eq", "eq"), (sel(G2, ["q", "m", "y"]) + xe, "r")], rt=1.1, copia=True,
              nota="mapa 6c (B3-2: x = √(4 − y²))")
        pg = TP(r"\X\ge 0", 1440, 500, 32, "l")
        self.pena(pg)
        self.gat("positivo xis igual")
        realce(self, Q["arc"], rc)                                     # o mesmo arco, lido como x = √(4 − y²)
        self.gat("é a mesma circunferência")
        rc2 = rot(CH, r"\Co{\X=\sqrt{4-\Y^2}}", (S3, 1), 20, -36, 30)
        self.play(ReplacementTransform(rc, rc2), run_time=1.0)
        ja_escrita(rc2.f)
        self.gat("e olha a fatia")
        pal2 = Palco3D(self, "cena1", CAM_B32, tipo="dei", cresce=1.0, faca=0.0, corte=0.0, face=0.0, sai=0.0, lx=2.55, ly=2.5, lz=2.15, ox=2.05, oy=-1.05)
        pal2.fundo.op.set_value(1.0)
        sai = [m for m in self.snap() if m not in (G0, G1, G2, G3, pg)] + [self.grade]
        self.remove(*sai)
        self.grade = None
        self.add(pal2.fundo)
        lx4 = TC(r"\X", 470, 810, 32, "c")
        lf4 = pal2.prende(TC(r"\f", 0, 0, 32, "c"), "ez", 30, 34)
        ja_escrita(lx4)
        ja_escrita(lf4)
        self.add(lx4, lf4)
        corte3d(self, pal2, rt_f=0.8, rt_c=1.0, rt_s=0.4, rt_face=0.4)
        py1 = pal2.prende(TP(r"\Y=1", 0, 0, 34), "faca", 20, -40)
        self.pena(py1)
        self.gat("a altura é ípsilon")
        dr = leg("A FATIA DEITADA É UM RETÂNGULO", 1120, 620, E2, "left", 30)
        self.pena(dr)
        self.marca("11", agora=True)
        self.gat("então ela é um")
        self.play(*pal2.anim(0.8, sai=1.0), *[FadeOut(m) for m in (G0, G1, G2, G3, pg, dr, py1, lx4, lf4)], run_time=0.8)
        for m in (py1, lf4):
            m.clear_updaters()
        self.remove(G0, G1, G2, G3, pg, dr, py1, lx4, lf4)
        pouso(self, pal2, (0, 1, 0), (0, 1, 0), 300, 200, 880)
        G = lateral(LAT1, 2.1, ymax=2.25, zt=(0, 1, 2), yt=(0, 1, 2), hcor=E1, hl=r"\X", vl=r"\f")
        ret = poly_px([LAT1.px(0, 0), LAT1.px(S3, 0), LAT1.px(S3, 1), LAT1.px(0, 1)], mixh(BG_, E2, .35), z=2)
        cont = lin_px([LAT1.px(0, 0), LAT1.px(S3, 0), LAT1.px(S3, 1), LAT1.px(0, 1), LAT1.px(0, 0)], E2, 5, z=4)
        py_ = TP(r"\Y=1", 260, 240, 30, "c")
        troca_para_2d(self, pal2, [G["grade"], G["eh"], G["ev"], G["lh"], G["lv"], G["nums"], ret, cont, py_])
        print(f"[pouso2d] B3-2 ret f0={LAT1.px(0, 0)} f1={LAT1.px(S3, 0)} f2={LAT1.px(S3, 1)} f3={LAT1.px(0, 1)}")
        self.gat("altura vezes comprimento")
        p = LAT1.px(S3 / 2, 0)
        lc1 = leg("COMPRIMENTO", p[0], p[1] + 80, GEO, "center", 26)
        lc2 = TC(r"\Co{\sqrt{4-\Y^2}}", p[0], p[1] + 120, 28, "c")
        q = LAT1.px(S3, .5)
        la1 = leg("ALTURA", q[0] + 24, q[1] - 20, GEO, "left", 26)
        la2 = TC(r"\Y", q[0] + 24, q[1] + 22, 30, "l")
        self.pena(la1, la2, lc1, lc2, lag=0.25)
        H0 = L([("i", r"\int_{\Az{0}}^{\Co{\sqrt{4-\Y^2}}}"), ("y", r"\Y\,\dX")], 1120, 440, 40)
        self.pena(H0)
        H1 = L([("i", r"\int_{\Az{0}}^{\Co{\sqrt{4-\Y^2}}}"), ("y", r"\Y\,\dX"), ("eq", "="), ("ry", r"\Y"), ("rr", r"\sqrt{4-\Y^2}")], 1120, 440, 40)
        alto = max(gl(H0, "i"), key=lambda x: x.height)
        sup = VGroup(*[x for x in gl(H0, "i") if x is not alto and x.get_center()[1] > alto.get_center()[1]])
        passo(self, H0, H1, [("i", "i"), ("y", "y")], voos=[(VGroup(gl(H0, "y")[0]).copy(), "ry", -0.7, 0.0), (sup.copy(), "rr", 0.7, 0.3)], rt=0.5,
              nota="mapa 7a (B3-2: o y sai da integral como altura fixa; voos em sequência, arcos opostos)")
        self.gat("essa tem primitiva")
        K0 = L([("i", r"\int_0^2"), ("ry", r"\Y"), ("rr", r"\sqrt{4-\Y^2}"), ("dy", r"\,\dY")], 1120, 580, 36, caneta=False)
        voos(self, [(gl(H1, "ry", "rr").copy(), parte(K0, sel(K0, ["ry", "rr"]), "y√"))], rt=0.9)
        self.pena(parte(K0, sel(K0, ["i", "dy"]), "∫ dy"))
        K0._esc = True
        self.gat("quase a derivada do")
        rr_ = list(gl(K0, "rr"))
        dentro = VGroup(*[x for x in rr_ if x is not max(rr_, key=lambda z: z.width)])
        acende(self, (gl(K0, "ry"), E2), (dentro, E2), rt=1.2)
        self.gat("resultado oito terços")
        K1 = L([("i", r"\int_0^2"), ("ry", r"\Y"), ("rr", r"\sqrt{4-\Y^2}"), ("dy", r"\,\dY"), ("eq", "="), ("pr", r"\Big[-\dfrac{(4-\Y^2)^{3/2}}{3}\Big]_0^2"),
                ("e2", "="), ("v", r"\dfrac{8}{3}")], 1120, 580, 36)
        passo(self, K0, K1, [(k, k) for k in ("i", "ry", "rr", "dy")], rt=0.5, nota="mapa 7b (B3-2: [−(4 − y²)^{3/2}/3]₀² = 8/3)")
        ck = check_px(1830, 580)
        self.play(Create(ck), run_time=0.4)
        self.gat("guarda essa diferença")
        pn = painel(1120, 170, 740, 170)
        c1 = T("EM PÉ: ALTURA MUDA · TRIÂNGULO", 1150, 235, 30, "left", E1)
        c2 = T("DEITADA: ALTURA FIXA · RETÂNGULO", 1150, 305, 30, "left", E2)
        self.play(Create(pn), run_time=0.5)
        self.pena(c1)
        self.pena(c2)
        self.gat("vira altura vezes")
        realce(self, cont, la2, lc2)                                   # altura · comprimento no retângulo do pouso
        self.gat("o fator que falta")
        acende(self, (lc2, CORAL), (gl(K1, "rr"), CORAL), rt=1.2)
        self.marca("12", agora=True)
        self.sai_fim(rt=0.25)                         # palco vazio ≤ 0,5 s na virada para o PB4
