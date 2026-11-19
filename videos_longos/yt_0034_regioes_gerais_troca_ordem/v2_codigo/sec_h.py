"""yt_0034 · H · uma integral que trava (alvos v2_01, v2_02 e 01) e a ideia do vídeo (alvo 02). Glyph map 1.
v2 (handoff v2 §3.1): a integral nasce direto na coluna; o palco nasce com o gráfico de f = e^(−y²) (a ideia "a primitiva não se escreve" ganha
imagem: a área de x até 1 existe, mas não tem fórmula); as três famílias riscadas uma por palavra; o x anda e a área muda junto.
Em "com a ordem trocada" o gráfico sai e o palco do triângulo nasce JÁ com a tira em pé da ordem original (eixos nunca vazios); a deitada
nasce com o glyph map 1."""
from pecas34 import *


def limites(m, chave):
    """Glifos de uma peça ∫_a^b sem o sinal ∫ (o glifo mais alto)."""
    g = list(gl(m, chave))
    alto = max(g, key=lambda x: x.height)
    return VGroup(*[x for x in g if x is not alto])


def quarto_disco(sc, rt=0.8, arco_cor=CORAL, v=CH):
    """Palco do quarto de disco (layout A): região, eixos, marcas 2 e o arco coral (o papel vem em "g")."""
    reg = regiao(v, disco_pts())
    sx, sy, lx, ly = eixos_v(v, 2.35, 2.35)
    t2x = tick(v, "x", 2, r"\Am{2}")
    t2y = tick(v, "y", 2, r"\Mg{2}")
    arc = curva(v, arco_q(), arco_cor, 4)
    return dict(reg=reg, sx=sx, sy=sy, lx=lx, ly=ly, t2x=t2x, t2y=t2y, arc=arc, g=papel_v(v, (0, 2.2, 0, 2.2)))


def grade_lat(Lv, a0, a1, b0, b1, pa=.25, pb=.25):
    """Grade do papel nascendo dos eixos de um gráfico de uma variável (escala própria)."""
    g = VGroup()
    a = math.ceil(a0 / pa - 1e-9) * pa
    while a <= a1 + 1e-9:
        g.add(lin_px([Lv.px(a, b0), Lv.px(a, b1)], GRADE, 1.2, z=-9))
        a += pa
    b = math.ceil(b0 / pb - 1e-9) * pb
    while b <= b1 + 1e-9:
        g.add(lin_px([Lv.px(a0, b), Lv.px(a1, b)], GRADE, 1.2, z=-9))
        b += pb
    return g


def chip(s, X, Y):
    """Etiqueta riscada: moldura + ✗ + palavra (30 px). Devolve (grupo, x do fim)."""
    t = T(s, X + 66, Y + 2, 30)
    w = t.width * 120
    mol = moldura(X, Y - 40, w + 90, 62, GEO, .45, 2, 10)
    cz = cruz_px(X + 32, Y - 9, AL, .8)
    return VGroup(mol, cz, t), X + w + 90


class PH(B34):
    ANTES = "UMA INTEGRAL QUE TRAVA"

    def corpo(self):
        # ── H1 · uma integral que trava (alvos v2_01, v2_02 e 01) ──
        self.an("H1")
        G = Lat(560, 800, 210, 420)                                    # gráfico de e^(−y²): 210 px por unidade em y, 420 em f
        gg = grade_lat(G, -2.25, 2.25, 0, 1.25)
        ey = seta_px(G.px(-2.4, 0), G.px(2.5, 0), E2, 3, 16, z=6)
        ef = seta_px(G.px(0, -.04), G.px(0, 1.22), CI, 3, 16, z=6)
        q = G.px(2.5, 0)
        ly = TC(r"\Y", q[0] + 24, q[1], 32, "c")
        q = G.px(0, 1.22)
        lf = TC(r"\f", q[0], q[1] - 26, 32, "c")
        cv = curva(G, cX(gs, -2.3, 2.3), CI, 4, z=5)
        q = G.px(-1.25, gs(-1.25))
        le = TC(r"e^{-\Y^2}", q[0] - 30, q[1] - 34, 34, "r")
        I0 = L([("io", r"\int_{\Am{0}}^{\Am{1}}\!"), ("ii", r"\int_{\Az{\X}}^{\Co{1}}"), ("e", r"e^{-\Y^2}"), ("dy", r"\,\dY"), ("dx", r"\,\dX")],
               1120, 250, 50, "l")
        self.add(gg)
        self.pena(I0, passo=0.07, extra=[GrowFromPoint(ey, G.P(0, 0)), GrowFromPoint(ef, G.P(0, 0))])
        self.play(Create(cv), run_time=2.0, rate_func=linear)          # a curva a caneta, da esquerda para a direita
        self.pena(ly, lf, le, lag=0.2)
        for fr, ch in (("da integral de xis", "ii"), ("de é elevado a", "e"), ("dê ípsilon dê xis", "dy"), ("dê xis o", "dx")):
            self.gat(fr)
            acende(self, (gl(I0, ch), None), rt=0.6)                   # sublinhado de leitura (Anexo B)
        self.gat("o número de euler")
        acende(self, (VGroup(gl(I0, "e")[0]), None), rt=0.8)
        self.gat("dois vírgula setenta")
        eul = TC(r"e\approx 2{,}718", 1470, 250, 34, "l")
        self.pena(eul)
        realce(self, cv)                                               # palco vivo: o sino e^(−y²) acende enquanto a fala lê o e
        self.gat("começa por dentro")
        acende(self, (gl(I0, "ii", "e", "dy"), None), rt=1.0)
        # "precisa de uma primitiva": o x no eixo, as tracejadas e a área de x até 1 (pinta da esquerda para a direita)
        self.gat("precisa de uma primitiva")
        xt = ValueTracker(.3)
        bt = ValueTracker(.3)
        self.add(xt, bt)
        area = always_redraw(lambda: poly_px([G.px(xt.get_value(), 0)] + [G.px(a, gs(a)) for a in np.linspace(xt.get_value(), max(xt.get_value() + 1e-3, bt.get_value()), 40)]
                                             + [G.px(max(xt.get_value() + 1e-3, bt.get_value()), 0)], mixh(BG_, CI, .32), z=2))
        tx = always_redraw(lambda: curva(G, [(xt.get_value(), 0), (xt.get_value(), gs(xt.get_value()))], E1, 2, dash=(6, 6), z=4))
        px_ = always_redraw(lambda: ponto_px(*G.px(xt.get_value(), 0), E1, 9))
        lxp = always_redraw(lambda: TC(r"\Am{\X}", G.px(xt.get_value(), 0)[0], G.px(0, 0)[1] + 34, 32, "c", caneta=False))
        t1 = curva(G, [(1, 0), (1, gs(1))], GEO, 2, dash=(6, 6), z=4)
        l1 = TC("1", G.px(1, 0)[0], G.px(0, 0)[1] + 34, 30, "c")
        self.play(FadeIn(px_, scale=.5), FadeIn(lxp), Create(tx), Create(t1), FadeOut(eul), run_time=0.6)
        self.remove(eul)
        self.pena(l1)
        self.add(area)
        self.play(bt.animate.set_value(1.0), run_time=1.2, rate_func=linear)
        F2 = L([("i", r"\int_{\Az{\X}}^{\Co{1}} e^{-\Y^2}\,\dY="), ("q", r"\ \Al{?}")], 1120, 380, 44, caneta=False)
        self.pena(parte(F2, sel(F2, "i"), "∫ₓ¹ e^(−y²) dy ="))
        self.gat("e aí trava")
        qa = TC(r"\Al{?}", *G.px(.62, .36), 54, "c")
        self.pena(qa, parte(F2, sel(F2, "q"), "?"), lag=0.2)
        pl = placa_txt("SEM PRIMITIVA EM FÓRMULA", 1120, 500, AL, 30, "left")
        self.pena(pl)
        self.gat("primitiva existe mas")
        realce(self, area, cv)                                         # a área existe (só não tem fórmula)
        chips, X = [], 1120
        for k, (fr, w_) in enumerate((("nada de polinômio", "POLINÔMIO"), ("seno logaritmo", "SENO"), ("logaritmo nada", "LOGARITMO"))):
            self.gat(fr)
            c_, Xn = chip(w_, X if k < 2 else 1120, 620 if k < 2 else 720)
            X = Xn + 16
            self.play(Create(c_[0]), run_time=0.3)
            self.pena(c_[2], extra=[Create(c_[1])])
            chips.append(c_)
        self.marca("v2_01", agora=True)
        # "a conta de dentro não sai, e a de fora nem começa": o x anda e a área muda junto (existe, mas não tem fórmula)
        self.gat("a conta de dentro")
        self.play(FadeOut(qa), run_time=0.2)
        self.remove(qa)
        self.play(xt.animate.set_value(.8), run_time=1.4)
        self.gat("e a de fora")
        self.play(xt.animate.set_value(.3), run_time=1.4)

        # "com a ordem trocada": o gráfico sai; o palco do triângulo nasce com a tira em pé da ordem original (x até 1)
        self.gat("com a ordem trocada")
        for m in (area, tx, px_, lxp):
            m.clear_updaters()
        graf = [gg, ey, ef, ly, lf, cv, le, area, tx, px_, lxp, t1, l1, F2] + chips
        pl2 = placa_txt("SEM PRIMITIVA EM FÓRMULA", 1120, 370, AL, 28, "left")
        ja_escrita(pl2)
        for x in pl2.get_family():
            x._esc = True
        self.play(*[FadeOut(m) for m in graf], Transform(pl, pl2), run_time=0.4)
        self.remove(*graf, xt, bt)
        sx, sy, lx, ly2 = eixos_v(TRI, 1.2, 1.2)
        g = papel_v(TRI, (0, 1.12, 0, 1.12))
        self.grade = g
        tv = tiraV(TRI, .72, .72, 1)
        self.play(FadeIn(g), GrowFromPoint(sx, TRI.P(0, 0)), GrowFromPoint(sy, TRI.P(0, 0)), GrowFromEdge(tv, DOWN), run_time=0.8)
        self.pena(lx, ly2)
        lx_ = rot(TRI, r"\Az{\X}", (.72, .72), 22, 8, 30)
        l1_ = rot(TRI, r"\Co{1}", (.72, 1), 22, -26, 30)
        li0 = limites(I0, "ii")
        lo0 = min(li0, key=lambda x: x.get_center()[1])
        hi0 = max(li0, key=lambda x: x.get_center()[1])
        pe1, ps1 = pontos_es(TRI, (.72, .72), (.72, 1))
        self.play(FadeIn(lx_[0]), FadeIn(l1_[0]), FadeIn(pe1, scale=.5), FadeIn(ps1, scale=.5), run_time=0.3)
        voos(self, [(lo0, lx_.f), (hi0, l1_.f)], rt=0.9)
        I1 = L([("eq", "="), ("io", r"\int_{\Mg{0}}^{\Mg{1}}\!"), ("ii", r"\int_{\Az{0}}^{\Co{\Y}}"), ("e", r"e^{-\Y^2}"), ("dx", r"\,\dX"), ("dy", r"\,\dY")],
               1120, 490, 50, "l")
        self.gat("da integral de zero até")
        realce(self, tv, pe1, ps1)                                     # a tira em pé cujos limites vão mudar
        acende(self, (limites(I0, "ii"), AL), rt=0.5)                  # os limites que mudam acendem juntos antes
        passo(self, I0, I1, [("io", "io"), ("ii", "ii"), ("e", "e"), ("dy", "dy"), ("dx", "dx")], rt=1.6, copia=True,
              nota="mapa 1 (H1: dy dx troca de lugar; x/1 → 0/y)")
        th = tiraH(TRI, .42, 0, .42)
        l0_ = rot(TRI, r"\Az{0}", (0, .42), -44, -30, 30)
        ly_ = rot(TRI, r"\Co{\Y}", (.42, .42), 34, 26, 30)       # abaixo e à direita: longe da diagonal
        li1 = limites(I1, "ii")
        lo1 = min(li1, key=lambda x: x.get_center()[1])
        hi1 = max(li1, key=lambda x: x.get_center()[1])
        pe2, ps2 = pontos_es(TRI, (0, .42), (.42, .42))
        self.play(GrowFromEdge(th, LEFT), FadeIn(l0_[0]), FadeIn(ly_[0]), FadeIn(pe2, scale=.5), FadeIn(ps2, scale=.5), run_time=0.6)
        voos(self, [(lo1, l0_.f), (hi1, ly_.f)], rt=0.9)
        t1x = tick(TRI, "x", 1, r"\Am{1}")
        t1y = tick(TRI, "y", 1, r"\Mg{1}")
        self.gat("em duas linhas")
        self.play(Create(t1x[0]), Create(t1y[0]), run_time=0.4)
        self.pena(t1x[1], t1y[1], lag=0.3)
        self.gat("metade de um menos")
        I2 = L([("eq", "="), ("fr", r"\dfrac{1-1/e}{2}"), ("ap", r"\approx 0{,}316")], 1120, 640, 50, "l", caneta=False)
        self.pena(parte(I2, ix(I2, "eq", "fr"), "exato"))             # o exato primeiro
        self.gat("zero vírgula três um")
        ret = curva(TRI, [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], GEO, 2, dash=(8, 8), alpha=.5, z=3)
        self.pena(parte(I2, ix(I2, "ap"), "≈ 0,316"), extra=[Create(ret)])
        self.gat("os limites mudaram")
        acende(self, (limites(I0, "ii"), BR), (limites(I1, "ii"), BR), (VGroup(lx_.f, l1_.f), AZC), (VGroup(l0_.f, ly_.f), AZC), rt=0.8)
        self.marca("v2_02", agora=True)
        rot_ = [lx_, l1_, l0_, ly_]
        self.gat("o xis até um")                                        # a tira em pé percorre (os rótulos dela saem e voltam com ela)
        self.play(FadeOut(lx_), FadeOut(l1_), FadeOut(pe1), FadeOut(ps1), run_time=0.3)
        self.play(Transform(tv, tiraV(TRI, .35, .35, 1)), run_time=0.8)
        self.play(Transform(tv, tiraV(TRI, .72, .72, 1)), run_time=1.0)
        self.play(FadeIn(lx_), FadeIn(l1_), FadeIn(pe1), FadeIn(ps1), run_time=0.3)
        self.gat("a gente não trocou")
        self.play(FadeOut(l0_), FadeOut(ly_), FadeOut(pe2), FadeOut(ps2), run_time=0.3)
        self.play(Transform(th, tiraH(TRI, .8, 0, .8)), run_time=0.8)
        self.play(Transform(th, tiraH(TRI, .42, 0, .42)), run_time=1.0)
        self.play(FadeIn(l0_), FadeIn(ly_), FadeIn(pe2), FadeIn(ps2), run_time=0.3)
        self.gat("mudou o jeito de")                                    # a região nasce no palco (ainda sem as arestas)
        reg = regiao(TRI, [(0, 0), (1, 1), (0, 1)])
        lado = curva(TRI, [(0, 0), (0, 1)], GEO, 2)
        self.play(FadeIn(reg), Create(lado), run_time=1.0)
        self.gat("não mora num retângulo")
        self.play(ret.animate.set_stroke(opacity=1, width=W(3)), run_time=0.9)
        self.gat("ela mora num triângulo")
        dg = curva(TRI, [(0, 0), (1, 1)], BR, 3)
        tp = curva(TRI, [(0, 1), (1, 1)], BR, 3)
        self.play(FadeOut(ret), Create(dg), Create(tp), run_time=1.0)
        self.remove(ret)
        mr = leg("MESMA REGIÃO, OUTRA ORDEM", 1120, 760, MEN, "left", 30)
        self.pena(mr)
        self.marca("01", agora=True)
        self.gat("duas perguntas como")
        realce(self, reg, dg, tp, lado, atraso=0.4)                    # a região que não é retângulo
        # "não é um retângulo": corte seco para o quarto de disco (alvo 02)
        self.gat("não é um retângulo")
        sai = self.snap() + [self.grade]
        self.remove(*sai)
        Q = quarto_disco(self)
        self.grade = Q["g"]
        self.add(Q["g"], Q["reg"], Q["sx"], Q["sy"], Q["lx"], Q["ly"], *Q["t2x"], *Q["t2y"])
        for m in (Q["lx"], Q["ly"], Q["t2x"][1], Q["t2y"][1]):
            ja_escrita(m)
        self.wait(0.4)
        self.gat("os limites novos")
        self.play(Create(Q["arc"]), run_time=1.2)

        # ── H2 · a ideia do vídeo (alvo 02) ──
        self.an("H2")
        self.secao("A IDEIA DO VÍDEO")
        self.gat("no desenho")
        tv = tiraV(CH, 1, 0, S3)
        self.play(GrowFromEdge(tv, DOWN), run_time=0.9)
        F = L([("a", r"\iint_B\f\,dA="), ("io", r"\int_{\Am{0}}^{\Am{2}}\!"), ("ii", r"\int_{\Az{0}}^{\Co{\sqrt{4-\X^2}}}"), ("r", r"\f\,\dY\,\dX")],
              1120, 260, 44, "l")
        self.pena(F)
        self.gat("começa numa curva")
        pe, ps = pontos_es(CH, (1, 0), (1, S3))
        r0 = rot(CH, r"\Az{\Y=0}", (1.12, 0), 0, -30, 28)
        self.play(FadeIn(pe, scale=0.5), run_time=0.4)
        self.pena(r0)
        self.gat("termina em outra")
        r1 = rot(CH, r"\Co{\Y=\sqrt{4-\X^2}}", (1.36, 1.72), 0, 0, 30)
        self.play(FadeIn(ps, scale=0.5), run_time=0.4)
        self.pena(r1)
        self.gat("os limites de fora")                                  # palco: o x de fora vai de 0 a 2 (o eixo acende em âmbar)
        fx = curva(CH, [(0, 0), (2, 0)], E1, 6, z=7)
        self.play(Create(fx), run_time=1.0)
        l1 = T("LIMITES DE FORA: NÚMEROS", 1120, 430, 36, "left", E1)
        self.pena(l1)
        self.play(FadeOut(fx), run_time=0.5)
        self.remove(fx)
        self.gat("passam a ser curvas")
        l2 = T("LIMITES DE DENTRO: CURVAS", 1120, 510, 36, "left", CORAL)
        self.pena(l2, extra=[Q["arc"].animate.set_stroke(width=W(6))])
        self.play(Q["arc"].animate.set_stroke(width=W(4)), run_time=0.5)
        self.gat("que dependem da variável")
        acende(self, (VGroup(*gl(F, "ii")[1:]), CORAL), rt=1.0)
        self.gat("não é só trocar")
        realce(self, tv, pe, ps)                                       # a fatia em pé da ordem de agora
        self.gat("reler a mesma região")
        l3 = T("TROCAR A ORDEM = RELER A REGIÃO", 1120, 680, 36, "left", MEN)
        th = tiraH(CH, 1.0, 0, S3, h=.06)                            # palco: a mesma região, fatiada no outro sentido
        self.pena(l3, extra=[GrowFromEdge(th, LEFT)])
        self.gat("fatiando no outro sentido")
        self.play(FadeOut(th), run_time=0.5)
        self.remove(th)
        self.marca("02")
        sai_com_canto(self)
