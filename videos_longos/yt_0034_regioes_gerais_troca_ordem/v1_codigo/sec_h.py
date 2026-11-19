"""yt_0034 · H · uma integral que trava (alvo 01) e a ideia do vídeo (alvo 02). Glyph map 1 (a ordem trocada)."""
from pecas34 import *


def limites(m, chave):
    """Glifos de uma peça ∫_a^b sem o sinal ∫ (o glifo mais alto)."""
    g = list(gl(m, chave))
    alto = max(g, key=lambda x: x.height)
    return VGroup(*[x for x in g if x is not alto])


def quarto_disco(sc, rt=0.8, arco_cor=CORAL):
    """Palco do quarto de disco (layout A): papel, região, eixos, marcas 2 e o arco coral."""
    reg = regiao(CH, disco_pts())
    sx, sy, lx, ly = eixos_v(CH, 2.35, 2.35)
    t2x = tick(CH, "x", 2, r"\Am{2}")
    t2y = tick(CH, "y", 2, r"\Mg{2}")
    arc = curva(CH, arco_q(), arco_cor, 4)
    return dict(reg=reg, sx=sx, sy=sy, lx=lx, ly=ly, t2x=t2x, t2y=t2y, arc=arc, g=papel_v(CH, (0, 2.2, 0, 2.2)))


class PH(B34):
    ANTES = "UMA INTEGRAL QUE TRAVA"

    def corpo(self):
        # ── H1 · uma integral que trava (alvo 01) ──
        self.an("H1")
        I0 = L([("io", r"\int_{\Am{0}}^{\Am{1}}\!"), ("ii", r"\int_{\Az{\X}}^{\Co{1}}"), ("e", r"e^{-\Y^2}"), ("dy", r"\,\dY"), ("dx", r"\,\dX")],
               960, 520, 52, "c")
        self.pena(I0, passo=0.07)                                       # "Olha esta integral": a caneta, no centro
        for fr, ch in (("integral de zero a", "io"), ("da integral de xis", "ii"), ("de é elevado a", "e"), ("dê ípsilon dê xis", "dy"), ("dê xis o", "dx")):
            self.gat(fr)
            acende(self, (gl(I0, ch), None), rt=0.7)                   # sublinhado de leitura (Anexo B)
        self.gat("o número de euler")
        acende(self, (VGroup(gl(I0, "e")[0]), None), rt=1.2)
        self.gat("dois vírgula setenta")
        eul = TC(r"e\approx 2{,}718", 960, 620, 34, "c")
        self.pena(eul)
        self.gat("começa por dentro")
        acende(self, (gl(I0, "ii", "e", "dy"), None), rt=1.0)
        self.gat("precisa de uma primitiva")
        acende(self, (gl(I0, "e"), CI), rt=1.4)
        self.gat("e aí trava")
        q = TC(r"\Al{?}", pxof(I0.get_right())[0] + 30, 500, 52, "l")
        self.play(FadeOut(eul), run_time=0.3)
        self.remove(eul)
        self.pena(q)
        pl = placa_txt("SEM PRIMITIVA EM FÓRMULA", 960, 650, AL, 28, "center")
        self.pena(pl)
        nada = []
        for k, (fr, w_) in enumerate((("nada de polinômio", "POLINÔMIO"), ("seno logaritmo", "SENO"), ("logaritmo nada", "LOGARITMO"))):
            self.gat(fr)
            t_ = leg(w_, 760 + 200 * k, 740, AL, "center", 26)
            self.pena(t_)
            nada.append(t_)
        self.gat("a conta de dentro")
        self.play(*[FadeOut(t_) for t_ in nada], run_time=0.4)
        self.remove(*nada)
        acende(self, (gl(I0, "ii", "e", "dy"), AL), rt=1.0)
        self.gat("e a de fora")
        acende(self, (gl(I0, "io"), AL), rt=1.0)

        # "com a ordem trocada": a integral sobe para a coluna; o palco do triângulo nasce (eixos e papel) atrás
        self.gat("com a ordem trocada")
        alvo = L([("io", r"\int_{\Am{0}}^{\Am{1}}\!"), ("ii", r"\int_{\Az{\X}}^{\Co{1}}"), ("e", r"e^{-\Y^2}"), ("dy", r"\,\dY"), ("dx", r"\,\dX")],
                 1120, 250, 50, "l", caneta=False)
        pl2 = placa_txt("SEM PRIMITIVA EM FÓRMULA", 1120, 370, AL, 28, "left")
        ja_escrita(pl2)
        for x in pl2.get_family():
            x._esc = True
        sx, sy, lx, ly = eixos_v(TRI, 1.2, 1.2)
        g = papel_v(TRI, (0, 1.12, 0, 1.12))
        self.grade = g
        self.play(Transform(I0, alvo), Transform(pl, pl2), FadeOut(q), FadeIn(g), GrowFromPoint(sx, TRI.P(0, 0)), GrowFromPoint(sy, TRI.P(0, 0)),
                  run_time=1.2)
        self.remove(q)
        self.pena(lx, ly)
        I1 = L([("eq", "="), ("io", r"\int_{\Mg{0}}^{\Mg{1}}\!"), ("ii", r"\int_{\Az{0}}^{\Co{\Y}}"), ("e", r"e^{-\Y^2}"), ("dx", r"\,\dX"), ("dy", r"\,\dY")],
               1120, 490, 50, "l")
        self.gat("da integral de zero até")
        t1x = tick(TRI, "x", 1, r"\Am{1}")
        t1y = tick(TRI, "y", 1, r"\Mg{1}")
        self.play(Create(t1x[0]), Create(t1y[0]), run_time=0.4)
        acende(self, (limites(I0, "ii"), AL), rt=0.6)                  # os limites que mudam acendem juntos antes
        passo(self, I0, I1, [("io", "io"), ("ii", "ii"), ("e", "e"), ("dy", "dy"), ("dx", "dx")], rt=1.6, copia=True,
              nota="mapa 1 (H1: dy dx troca de lugar; x/1 → 0/y)")
        self.gat("em duas linhas")
        self.pena(t1x[1], t1y[1], lag=0.3)
        self.gat("metade de um menos")
        I2 = L([("eq", "="), ("fr", r"\dfrac{1-1/e}{2}"), ("ap", r"\approx 0{,}316")], 1120, 640, 50, "l", caneta=False)
        self.pena(parte(I2, ix(I2, "eq", "fr"), "exato"))             # o exato primeiro
        self.gat("zero vírgula três um")
        ret = curva(TRI, [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], GEO, 2, dash=(8, 8), alpha=.5, z=3)
        self.pena(parte(I2, ix(I2, "ap"), "≈ 0,316"), extra=[Create(ret)])
        self.gat("os limites mudaram")
        acende(self, (limites(I0, "ii"), BR), (limites(I1, "ii"), BR), rt=0.5)
        self.gat("o xis até um")                                        # a tira em pé da 1.ª ordem e a deitada da 2.ª nascem no palco
        tv = tiraV(TRI, .72, .72, 1)
        th = tiraH(TRI, .42, 0, .42)
        self.play(GrowFromEdge(tv, DOWN), run_time=0.8)
        self.gat("virou zero até")
        self.play(GrowFromEdge(th, LEFT), run_time=0.8)
        self.gat("a gente não trocou")
        self.play(Transform(tv, tiraV(TRI, .35, .35, 1)), Transform(th, tiraH(TRI, .8, 0, .8)), run_time=1.4)
        self.play(Transform(tv, tiraV(TRI, .72, .72, 1)), Transform(th, tiraH(TRI, .42, 0, .42)), run_time=1.4)
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
        # os quatro limites acendem no desenho (voam da fórmula, na ordem da voz): x e 1 na tira em pé, 0 e y na deitada
        pe1, ps1 = pontos_es(TRI, (.72, .72), (.72, 1))
        pe2, ps2 = pontos_es(TRI, (0, .42), (.42, .42))
        lx_ = rot(TRI, r"\Az{\X}", (.72, .72), 22, 8, 30)
        l1_ = rot(TRI, r"\Co{1}", (.72, 1), 22, -26, 30)
        l0_ = rot(TRI, r"\Az{0}", (0, .42), -44, -30, 30)
        ly_ = rot(TRI, r"\Co{\Y}", (.42, .42), 26, -28, 30)
        self.play(FadeIn(pe1, scale=0.5), FadeIn(ps1, scale=0.5), run_time=0.5)
        li0, li1 = limites(I0, "ii"), limites(I1, "ii")
        lo0 = min(li0, key=lambda x: x.get_center()[1])
        hi0 = max(li0, key=lambda x: x.get_center()[1])
        lo1 = min(li1, key=lambda x: x.get_center()[1])
        hi1 = max(li1, key=lambda x: x.get_center()[1])
        self.play(FadeIn(lx_[0]), FadeIn(l1_[0]), run_time=0.2)
        voos(self, [(lo0, lx_.f), (hi0, l1_.f)], rt=0.9)
        self.play(FadeIn(pe2, scale=0.5), FadeIn(ps2, scale=0.5), run_time=0.5)
        self.play(FadeIn(l0_[0]), FadeIn(ly_[0]), run_time=0.2)
        voos(self, [(lo1, l0_.f), (hi1, ly_.f)], rt=0.9)
        mr = leg("MESMA REGIÃO, OUTRA ORDEM", 1120, 760, MEN, "left", 30)
        self.pena(mr)
        self.marca("01", agora=True)
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
        self.gat("reler a mesma região")
        l3 = T("TROCAR A ORDEM = RELER A REGIÃO", 1120, 680, 36, "left", MEN)
        th = tiraH(CH, 1.0, 0, S3, h=.06)                            # palco: a mesma região, fatiada no outro sentido
        self.pena(l3, extra=[GrowFromEdge(th, LEFT)])
        self.gat("fatiando no outro sentido")
        self.play(FadeOut(th), run_time=0.5)
        self.remove(th)
        self.marca("02")
        sai_com_canto(self)
