"""yt_0036 · B7 · pause e tente (sem alvo). Layout A: o trapézio 1 ≤ x + y ≤ 2 no primeiro quadrante no palco, o enunciado e o selo PAUSE E TENTE
(da fala "Pausa o vídeo" até "Pronto?"); depois C17 inteira, linha a linha a caneta (as bordas voam do trapézio); SINAL TROCOU, MÓDULO NÃO no fim."""
from j36 import *

VB, AB = Vw(330, 700, 150), (-.1, 2.3, -.1, 2.3)
REG = [(1, 0), (2, 0), (0, 2), (0, 1)]


class PB7(J36):
    ANTES = "A CONFERÊNCIA"

    def corpo(self):
        self.an("B7")
        self.secao("PAUSE E TENTE")
        d = monta_plano(VB, AB, 2.35, 2.4, -.1, -.1, ticks=[("x", 1, r"\Am{1}"), ("x", 2, r"\Am{2}"), ("y", 1, r"\Mg{1}"), ("y", 2, r"\Mg{2}")])
        reg = poligono(VB, REG, RB, 1.0, GEO, 3, z=1)
        entra_plano(self, d, rt=0.5, extra=[FadeIn(reg[0]), Create(reg[1])], caneta=False)
        col = self.col = Coluna36(self, 760, 196)
        col.GAP36 = 22
        E = Lp([("ii", r"\iint_B"), ("f", r"\dfrac{\Ci{\cos}(\X-\Y)}{\Ci{\sen}(\X+\Y)}"), ("d", r"\,\dX\,\dY")], 760, 0, 34)
        col.poe(E)
        self.gat("pausa o vídeo")
        sl = pausa(dir_(E) + 40, centro(E)[1] + 12)
        poe_selo(self, sl)
        self.pena(E, passo=0.04)
        self.gat("cosseno de xis menos")
        acende(self, (gl(E, "f"), CI), rt=0.8)
        self.gat("no trapézio entre")
        realca(self, reg[1], cor=GEO, rt=0.6, wpx=5)
        self.gat("pronto")
        corta(self, *sl)
        # C17
        self.gat("u igual a xis menos")
        l1 = Lp([("a", r"\uu=\X-\Y,\ \ \vv=\X+\Y"), ("i", r"\ \Rightarrow\ "), ("b", r"\X=\dfrac{\uu+\vv}{2},\ \ \Y=\dfrac{\vv-\uu}{2}")], 760, 0, 30)
        col.poe(l1)
        self.pena(l1, passo=0.04)
        self.gat("o jacobiano um meio")
        l2 = Lp([("J", "J="), ("a", r"\left(\dfrac{1}{2}\right)\left(\dfrac{1}{2}\right)"), ("m", "-"), ("b", r"\left(\dfrac{1}{2}\right)\left(-\dfrac{1}{2}\right)")], 760, 0, 30)
        col.poe(l2)
        l2._xy = (760, centro(l2)[1])
        self.pena(l2, passo=0.04)
        self.gat("um quarto mais um quarto")
        l2 = cresce(self, l2, [("e1", "="), ("q", r"\dfrac{1}{4}+\dfrac{1}{4}")], col=col, nota="16 (produtos → 1/4 + 1/4)")
        self.gat("mais um meio")
        l2 = cresce(self, l2, [("e2", "="), ("r", r"\Lm{+\dfrac{1}{2}}")], voos=lambda B: [(gl(l2, "q").copy(), "r")], col=col, nota="16 (= +1/2)")
        self.gat("as bordas viram")
        bordas = [((1, 0), (0, 1), r"\X+\Y=1", r"\Rightarrow\vv=1,\ "), ((2, 0), (0, 2), r"\X+\Y=2", r"\Rightarrow\vv=2,\ "),
                  ((1, 0), (2, 0), r"\Y=0", r"\Rightarrow\vv=\uu,\ "), ((0, 1), (0, 2), r"\X=0", r"\Rightarrow\vv=-\uu")]
        pec = []
        for k, (_, _, a, b) in enumerate(bordas):
            pec += [(f"a{k}", a), (f"b{k}", b)]
        l3 = Lp(pec, 760, 0, 28)
        col.poe(l3)
        for k, (p0, p1, _, _) in enumerate(bordas):
            ed = lin_px([VB.px(*p0), VB.px(*p1)], LIMA, 5, z=6)
            self.play(Create(ed), run_time=0.3)
            voos(self, [(ed, parte(l3, l3._ix[f"a{k}"], f"borda {k + 1}"))], rt=0.6)
            self.remove(ed)
            self.pena(parte(l3, l3._ix[f"b{k}"], f"v {k + 1}"), passo=0.035)
        self.gat("e vê igual a menos u")
        l3b = Lp([("B", r"B_{uv}:\ \ \Vc{1}\le\vv\le\Vc{2},\ \ \Az{-\vv}\le\uu\le\Co{\vv}")], 760, 0, 30)
        col.poe(l3b)
        self.pena(l3b, passo=0.04)
        self.gat("por dentro um sobre")
        l4 = Lp([("I", r"\int_{\Az{-\vv}}^{\Co{\vv}}"), ("f", r"\dfrac{\Ci{\cos}\uu}{\Ci{\sen}\vv}\,\du")], 760, 0, 30)
        col.poe(l4)
        l4._xy = (760, centro(l4)[1])
        self.pena(l4, passo=0.04)
        l4 = cresce(self, l4, [("e1", "="), ("k", r"\dfrac{1}{\Ci{\sen}\vv}"), ("lb", r"\Big["), ("F", r"\Ci{\sen}\uu"), ("rb", r"\Big]"), ("sb", r"_{\Az{-\vv}}^{\Co{\vv}}")],
                    voos=lambda B: [(VGroup(*[l4[0][k] for k in idx_lims(l4, "I")[0]]).copy(), lims_sb(B, "sb")[0]),
                                    (VGroup(*[l4[0][k] for k in idx_lims(l4, "I")[1]]).copy(), lims_sb(B, "sb")[1])], col=col, nota="16 (1/sen v sai; colchete)")
        self.gat("dá seno de vê menos")
        l4b = Lp([("e", "="), ("d", r"\dfrac{\Ci{\sen}\vv-\Ci{\sen}(-\vv)}{\Ci{\sen}\vv}")], 790, 0, 30)
        col.poe(l4b, x=790)
        l4b._xy = (790, centro(l4b)[1])
        self.pena(l4b, passo=0.04)
        self.gat("dois seno de vê dividido")
        l4b = cresce(self, l4b, [("e2", "="), ("q", r"\dfrac{2\,\Ci{\sen}\vv}{\Ci{\sen}\vv}")], col=col, nota="16 (= 2 sen v / sen v)")
        l4b = cresce(self, l4b, [("e3", "="), ("r", "2")], voos=lambda B: [(gl(l4b, "q").copy(), "r")], col=col, nota="16 (= 2)")
        self.gat("por fora um meio")
        l5 = Lp([("h", r"\Lm{\dfrac{1}{2}}"), ("I", r"\int_{\Vc{1}}^{\Vc{2}}"), ("t", r"2\,\dv")], 760, 0, 30)
        col.poe(l5)
        l5._xy = (760, centro(l5)[1])
        self.escreve_voos(l5, [(gl(l2, "r"), "h"), (gl(l4b, "r"), [l5._ix["t"][0]])])
        l5 = cresce(self, l5, [("e", "="), ("p", r"\Lm{\dfrac{1}{2}}\cdot 2\cdot(2-1)")], col=col, nota="16 (1/2 · 2 · (2 − 1))")
        self.gat("que dá um")
        l5 = cresce(self, l5, [("e2", "="), ("r", "1")], voos=lambda B: [(gl(l5, "p").copy(), "r")], col=col, nota="16 (= 1)")
        ck = check_px(dir_(l5) + 30, centro(l5)[1], MEN)
        self.play(Create(ck), run_time=0.4)
        self.gat("trocaram de papel")
        sl2 = selo("SINAL TROCOU, MÓDULO NÃO", dir_(l2) + 30, centro(l2)[1] + 12, LIMA, 26)
        poe_selo(self, sl2)
        self.marca("B7")
        self.sai_fim()
