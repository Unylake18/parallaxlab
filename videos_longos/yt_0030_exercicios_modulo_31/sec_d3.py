"""Lote PD3 · D3 A FAMÍLIA DE REDEMOINHOS · v2 (alvos v2_d3r1, v2_d3r2, v2_d3r3, v2_d3g + 09–12 v1). Palco: v_α numa rede viva (α só muda nas
trocas) com as circunferências r = 1, 2, 3 tracejadas. Rapidez em três glyph maps. rot: molde, Q = x s^{−α} (x e s voam de v), molde da regra do produto,
a cadeia em caneta sincronizada, fusão, evidência, ∂P/∂y por cópia, substituição no molde e 6 glyph maps até (2 − 2α)/(x² + y²)^α. div: molde, só a
cadeia, cópia, substituição, cancelamento R14. Leitura: α voa do seletor para a substituição. Origem e giro de 90° (w = (Q, −P))."""
from alg30 import *  # noqa: F401,F403

C0, S0 = (1.75, 0.0), 0.7
PTS = [(X, Y) for X in np.arange(-3.5, 3.5 + 1e-6, .5) for Y in np.arange(-2.5, 2.5 + 1e-6, .5) if math.hypot(X, Y) >= .3]
MM = interp_tab([(0, 3.0), (.5, 1.0), (1, 1.2), (2, 1.2)])
T_FL = lambda a, c=C0: .35 * math.hypot(*c) ** (2 * a)
IDX_A = {0: 1, .5: 2, 1: 3, 2: 4}
A_, S_, SM, SM1 = r"\alpha", "s", r"s^{-\alpha}", r"s^{-\alpha-1}"
VV = [("v", r"\vv="), ("fr", r"\dfrac{(-\Y,\ \X)}{(\X^2+\Y^2)^{\alpha}}")]


def cartao_alpha(k, a, ccw, c=(2.2, 0.0), s=.6):
    X0 = CC[k][0]
    v = VB(CC[k], X0 + 240, 540, 56)
    ch = chapa_px(*CC[k], nome=f"D3 cartão α = {a}", v=v)
    T_ = .35 / math.pow(2.2, -2 * a)
    fl = flV(a)
    Fc = ponto_fl(fl, c, T_)
    sk = ou(clarPoly(borda_fl(fl, c, s, T_), .25), dq(c, s), clarPoly(circ_pts(.8, Fc, 12), .1))
    cmp = campo30(v, VORTA(a), -3.5, 3.5, -3.5, 3.5, .75, rmin=.6, mmax=3 if a == 0 else 1.2, skip=sk, nome=f"D3 cartão α = {a}")
    ped = quad30(v, c, s).em(fl, T_)
    g = VGroup(ch, cmp, fantasma(v, quad_pts(c, s)), ped, ponto7(v.c2p(0, 0), GEO, 5, 8))
    if ccw is not None:
        g.add(giro30(v, Fc, .62, ccw))
    return g


def SUB(a):
    """Substituição do α na fórmula do rot (a linha de baixo da leitura)."""
    return {0: [("rot", r"\V{\rot}="), ("o", r"(2-2\cdot"), ("a", r"\Am{0}"), ("c", ")"), ("d", r"/s^{0}"), ("res", r"=\V{2}")],
            .5: [("rot", r"\V{\rot}="), ("o", r"(2-"), ("a", r"\Am{1}"), ("c", ")"), ("d", r"/s^{1/2}"), ("res", r"=\V{1/r}")],
            1: [("rot", r"\V{\rot}="), ("o", r"(2-"), ("a", r"\Am{2}"), ("c", ")"), ("d", r"/s"), ("res", r"=\V{0}")],
            2: [("rot", r"\V{\rot}="), ("o", r"(2-"), ("a", r"\Am{4}"), ("c", ")"), ("d", r"/s^{2}"), ("res", r"=\V{-2/r^4}")]}[a]


class LoteD3(Base):
    ANTES = "DESENHAR SEM MIL SETAS"

    def corpo(self):
        # ── D3-1 · enunciado ──
        self.an("D3-1")
        self.secao("A FAMÍLIA DE REDEMOINHOS")
        zera_chapas()
        chA = chapa_px(*LA, nome="D3 palco A", v=VA)
        cmp = CampoVivo(VA, PTS, VORTA, MM, .5, p0=0.0, nome="D3 v_α")
        circs = VGroup(*[linha_rec(VA, circ_pts(r), LA, GEO, 2.5, .8, dash=(8, 9)) for r in (1, 2, 3)])        # v3: GEO 80 %, 2,5 px
        troca(self, "D2 → D3 (palco)")
        self.play(FadeIn(chA), cresce_campo(cmp, 1.0), run_time=1.0)
        fv = L(VV, 1120, 285, 40)
        self.gat("menos a coordenada vertical")
        escreve(self, fv, 0.4)
        _n, _d = num_den(fv.p("fr"))
        self.gat("xis ao quadrado mais ípsilon ao quadrado")        # leitura 4: x² + y²
        le(self, VGroup(*_d[1:6]), 4, "xis ao quadrado mais ípsilon ao quadrado é a distância ao quadrado", ate="cada valor do expoente alfa")
        fa = L([("a", r"\alpha="), ("0", r"0\quad"), ("m", r"\tfrac12\quad"), ("1", r"1\quad"), ("2", "2")], 1120, 380, 38)
        grp = lambda a: fa.pi(IDX_A[a])
        cx = caixa_em(grp(0), pad=10)
        self.gat("cada valor do expoente alfa")
        escreve(self, fa, 0.4)
        self.play(Create(cx), run_time=0.4)
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.ate(1.0)

        # ── D3-2 · as circunferências; a rapidez em três glyph maps; α correndo ──
        self.an("D3-2")
        self.gat("tangentes às circunferências")
        self.play(Create(circs), run_time=1.0)
        n1 = L([("n", r"\|\vv\|="), ("num", r"\|(-\Y,\ \X)\|"), ("bar", "/"), ("den", r"s^{\alpha}")], 1120, 470, 38)
        raio = vlinha(VA, [(0, 0), (2 * math.cos(2.4), 2 * math.sin(2.4))], GEO, 3).set_z_index(8)
        self.gat("o vetor de cima tem tamanho")
        escreve(self, n1, 0.35)
        # v4 C1: ‖(−y, x)‖ = √((−y)² + x²) = √(x² + y²) = r  e  s^α = (x² + y²)^α = (r²)^α = r^{2α}
        _nv, _dv = num_den(fv.p("fr"))
        K1 = L([("n", r"\|(-\Y,\ \X)\|"), ("e", "="), ("r", r"\sqrt{(-\Y)^2+\X^2}")], 1120, 545, 32)
        self.gat("o sinal some no quadrado")
        voa(self, VGroup(*_nv[0:6]), VGroup(*K1.p("n")[1:7]), rt=0.5)
        print(f"[origem] a {self.lote} D3-2 {self.t:.2f} {K1._tex!r} (‖, =, raiz)")
        self.play(caneta(VGroup(K1.p("n")[0], K1.p("n")[7], *K1.p("e"), *K1.p("r")), ritmo=0.1))
        junta(self, K1)
        K1b = L([("n", r"\|(-\Y,\ \X)\|"), ("e", "="), ("r", r"\sqrt{\X^2+\Y^2}"), ("e2", "="), ("rr", "r")], 1120, 545, 32)
        gm(self, K1, K1b, rt=0.8, extra=[Create(raio)], nota="((−y)² = y²; a raiz é a distância r)")
        acende(self, [K1b.p("rr"), raio], AMB, 0.8)
        K2 = L([("n", r"s^{\alpha}"), ("e", "="), ("b", r"(\X^2+\Y^2)^{\alpha}")], 1120, 615, 32)
        self.gat("embaixo a distância ao quadrado elevada")
        voa(self, n1.p("den"), K2.p("n"), rt=0.5)
        escreve_p(self, K2, ["e"], 0.15)
        voa(self, VGroup(*_dv), K2.p("b"), rt=0.5)
        junta(self, K2, origem="b")
        K2b = L([("n", r"s^{\alpha}"), ("e", "="), ("b", r"(\X^2+\Y^2)^{\alpha}"), ("e2", "="), ("c", r"(r^2)^{\alpha}"), ("e3", "="), ("d", r"r^{2\alpha}")], 1120, 615, 32)
        self.gat("potência de potência multiplica")
        gm(self, K2, K2b, rt=0.9, voos={"c": K1b.p("rr")}, nota="(x² + y² = r²; (r²)^α = r^{2α})")
        n2 = L([("n", r"\|\vv\|="), ("num", "r"), ("bar", "/"), ("den", r"r^{2\alpha}")], 1120, 470, 38)
        self.gat("então a rapidez é a distância")
        gm(self, n1, n2, rt=0.8, voos={"num": K1b.p("rr"), "den": K2b.p("d")}, nota="(r de K1, r^{2α} de K2)")
        n3 = L([("n", r"\|\vv\|="), ("rb", "r"), ("ex", r"^{\,1-2\alpha}", 4)], 1120, 470, 38)
        self.gat("na divisão os expoentes se subtraem")
        gm(self, n2, n3, rt=0.9, ka=["n", "rb", "ex", "ex"], extra=[FadeOut(K1b), FadeOut(K2b), FadeOut(raio)], nota="(r/r^{2α} = r^{1−2α})")
        self.remove(K1b, K2b, raio)
        n3.ks = ["n", "num", "num"]
        self.gat("com alfa zero a rapidez cresce")              # R16: o expoente e o α = 0 citados acendem
        acende(self, [n3.p("num"), grp(0)], AMB, 1.0)
        est = {"a": 0}

        def troca_a(a, rt=1.5):
            self.play(troca_p(cmp, a, rt), cx.animate.become(caixa_em(grp(a), pad=10)), run_time=rt)
            est["a"] = a
            print(f"[D3] α = {a}: mmax {MM(a):.2f}")
        self.gat("com alfa meio a rapidez")
        troca_a(.5)
        self.gat("com alfa um ela cai")
        troca_a(1)
        self.ate(1.0)

        # ── D3-3 · a conta do rotacional (alvos v2_d3r1 e v2_d3r2) e do divergente (v2_d3r3) ──
        self.an("D3-3")
        fan = fantasma(VA, quad_pts(C0, S0))
        R0 = L([("rot", r"\V{\rot}="), ("dQ", r"\dfrac{\partial\Qq}{\dx}"), ("men", "-"), ("dP", r"\dfrac{\partial\Pp}{\dy}")], 1120, 400, 38)
        self.gat("agora a conta do rotacional")
        self.play(FadeOut(fa), FadeOut(cx), FadeOut(n3), FadeIn(fan), run_time=0.4)
        self.remove(fa, cx, n3)
        est["a"] = .5
        escreve(self, R0, 0.12, extra=[troca_p(cmp, .5, 1.0)], rt=1.0)
        self.gat("na tela p e q")                                  # leitura 5: P e Q, depois o ∂
        le(self, R0.p("dQ"), 5, "P e Q são as duas componentes", dur=0.3)
        le(self, R0.p("dP"), 5, "P e Q são as duas componentes", ate="e o d arredondado")
        le(self, R0.p("dQ")[3], 5, "o d arredondado é a derivada parcial", ate="o rotacional é a derivada")
        self.gat("menos a derivada da componente horizontal")
        acende(self, [R0.p("dP")], CAMPO2, 0.8)
        QL = L([("Q", r"\Qq="), ("x", r"\X\,"), ("sm", SM), ("vg", r",\qquad "), ("s", "s="), ("s2", r"\X^2+\Y^2")], 1120, 485, 36)
        eixo = [s for s in cmp if abs(s._xy[1]) < 1e-6 and s._xy[0] > 0]
        num, den = num_den(fv.p("fr"))
        self.gat("a componente vertical é a coordenada")
        escreve_p(self, QL, ["Q"], 0.4)
        acende(self, eixo, CAMPO2, 1.0)
        voa(self, num[4], QL.p("x"), rt=0.6)
        escreve_p(self, QL, ["sm"], 0.35)
        self.gat("para encurtar a tela chama")                       # v4 C2: o s = x² + y² entra quando a fala o nomeia
        escreve_p(self, QL, ["vg", "s"], 0.35)
        voa(self, VGroup(*den[1:6]), QL.p("s2"), rt=0.6)
        junta(self, QL)
        PR = L([("dQ", r"\dfrac{\partial\Qq}{\dx}="), ("a", r"(\X)^{\prime}"), ("sm", SM), ("m", "+"), ("x", r"\X\,"), ("b", r"(s^{-\alpha})^{\prime}")], 1120, 580, 36)
        self.gat("regra do produto")
        escreve(self, PR, 0.15)
        self.gat("a derivada do primeiro vezes o segundo")
        acende(self, [PR.p("a", "sm")], AMB, 0.6)
        acende(self, [PR.p("x", "b")], AMB, 0.6)
        # ∂Q/∂x degrau a degrau: linha P (y 750) e chips da regra na linha K (y 665)
        P2 = L([("eq", "="), ("um", r"1\cdot "), ("sm", SM), ("m", "+"), ("x", r"\X"), ("ab", r"\cdot\big("), ("mn", "-"), ("al", r"\alpha\,"), ("pw", SM1),
                ("dt", r"\cdot "), ("d2", "2"), ("dX", r"\X"), ("fp", r"\big)")], 1150, 750, 34)
        self.gat("a primeira parte dá a própria")
        escreve_p(self, P2, ["eq"], 0.2)
        voa(self, PR.p("sm"), P2.p("sm"), rt=0.5)
        Ka1 = L([("a", r"(\X)^{\prime}"), ("e", "="), ("u", "1")], 1560, 665, 30)
        self.gat("porque a derivada de xis em relação")
        escreve(self, Ka1, 0.15)
        voa(self, Ka1.p("u"), P2.p("um")[0], rt=0.5)
        self.play(caneta(P2.p("um")[1], ritmo=0.2))
        self.gat("a segunda pela regra da cadeia")
        escreve_p(self, P2, ["m"], 0.2)
        voa(self, PR.p("x"), P2.p("x"), rt=0.45)
        escreve_p(self, P2, ["ab"], 0.2)
        Ka2 = L([("lhs", r"(s^{-\alpha})^{\prime}"), ("e", "="), ("mn", "-"), ("al", r"\alpha\,"), ("pw", SM1), ("dt", r"\cdot"), ("ds", r"\dfrac{\partial s}{\dx}")],
                1120, 665, 30)
        self.gat("o expoente desce")
        escreve_p(self, Ka2, ["lhs", "e"], 0.12)
        voa(self, VGroup(PR.p("b")[2], PR.p("b")[3]), Ka2.p("mn", "al"), rt=0.5)     # o −α desce do expoente
        escreve_p(self, Ka2, ["pw", "dt", "ds"], 0.15)
        junta(self, Ka2)
        self.gat("e ainda multiplica pela derivada de dentro")
        acende(self, [Ka2.p("ds")], CAMPO2, 0.8)
        Ka3 = L([("ds", r"\dfrac{\partial s}{\dx}"), ("e", "="), ("a", r"2\X"), ("p", "+"), ("z", "0")], 1560, 665, 30)
        self.gat("a derivada de esse em relação a xis")
        self.play(FadeOut(Ka1), run_time=0.25)
        self.remove(Ka1)
        voa(self, Ka2.p("ds"), Ka3.p("ds"), rt=0.4)
        escreve_p(self, Ka3, ["e"], 0.15)
        voa(self, QL.p("s2")[0:2], Ka3.p("a"), rt=0.45)                               # x² → 2x
        escreve_p(self, Ka3, ["p"], 0.15)
        acende(self, [QL.p("s2")[3:5]], CORAL, 0.3)
        voa(self, QL.p("s2")[3:5], Ka3.p("z"), rt=0.45)                               # y² → 0
        junta(self, Ka3, origem="b")
        Ka3b = L([("ds", r"\dfrac{\partial s}{\dx}"), ("e", "="), ("a", r"2\X")], 1560, 665, 30)
        gm(self, Ka3, Ka3b, rt=0.6, nota="(2x + 0 → 2x)")
        Ka2b = L([("lhs", r"(s^{-\alpha})^{\prime}"), ("e", "="), ("mn", "-"), ("al", r"\alpha\,"), ("pw", SM1), ("dt", r"\cdot"), ("d2", r"2\X")], 1120, 665, 30)
        gm(self, Ka2, Ka2b, rt=0.7, voos={"d2": Ka3b.p("a")}, nota="(∂s/∂x = 2x na cadeia)")
        self.gat("vezes duas vezes a coordenada horizontal")
        voa(self, Ka2b.p("mn", "al", "pw", "dt", "d2"), P2.p("mn", "al", "pw", "dt", "d2", "dX"), rt=0.6)
        escreve_p(self, P2, ["fp"], 0.2)
        junta(self, P2, origem="b")
        P3 = L([("eq", "="), ("sm", SM), ("mn", "-"), ("d2", "2"), ("al", r"\alpha"), ("x2", r"\X^2"), ("pw", SM1)], 1150, 750, 34)
        self.gat("xis vezes dois xis dá dois")
        gm(self, P2, P3, rt=0.9, ka=["eq", "z", "sm", "z", "x2", "z", "mn", "al", "pw", "z", "d2", "x2", "z"], nota="(x·2x → 2x²; o − vai para a frente)")
        K4 = L([("a", SM), ("e", "="), ("s", "s"), ("d", r"\cdot"), ("b", SM1), ("n", r"\qquad(-\alpha=1+(-\alpha-1))")], 1120, 665, 30)
        self.gat("agora o truque")
        self.play(FadeOut(Ka2b), FadeOut(Ka3b), run_time=0.3)
        self.remove(Ka2b, Ka3b)
        escreve(self, K4, 0.1)
        P4 = L([("eq", "="), ("s", "s"), ("d", r"\cdot"), ("pw0", SM1), ("mn", "-"), ("c", r"2\alpha\X^2"), ("pw", SM1)], 1150, 750, 34)
        self.gat("põe a potência com um a menos")
        gm(self, P3, P4, rt=0.8, voos={"s": K4.p("s"), "pw0": K4.p("b")}, ka=["eq", "z", "mn", "c", "c", "c", "pw"], nota="(s^{−α} = s·s^{−α−1})")
        P5 = L([("eq", "="), ("pw", SM1), ("ab", r"\,(s"), ("mn", "-"), ("c", r"2\alpha\X^2"), ("fc", ")")], 1150, 750, 34)
        gm(self, P4, P5, rt=0.9, ka=["eq", "ab", "ab", "pw", "mn", "c", "pw"], nota="(evidência: s^{−α−1})")
        F2 = L([("dQ", r"\dfrac{\partial\Qq}{\dx}="), ("sm1", SM1), ("ab", r"\,(s"), ("m2", "-"), ("ax", r"2\alpha\X^2"), ("fc", ")")], 1120, 580, 36)
        funde(self, [PR, P5, K4], F2, rt=1.0, ka=["dQ", "z", "z", "z", "z", "z"] + ["z", "sm1", "ab", "m2", "ax", "fc"] + ["z"] * 6)
        PQ = L([("P", r"\Pp="), ("my", r"-\Y\,"), ("smp", SM), ("vp", r",\ \ "), ("Q", r"\Qq="), ("x", r"\X\,"), ("sm", SM), ("vg", r",\ \ "), ("s", "s="), ("s2", r"\X^2+\Y^2")],
               1120, 485, 34)
        self.gat("a outra derivada é igualzinha")
        gm(self, QL, PQ, rt=0.8, voos={"my": VGroup(*num[1:3])})
        # ∂P/∂y degrau a degrau (v4 C2: antes era cópia de F2)
        G1 = L([("dP", r"\dfrac{\partial\Pp}{\dy}="), ("a1", r"(-\Y)^{\prime}"), ("sm", SM), ("m", "+"), ("a2", r"(-\Y)"), ("b", r"(s^{-\alpha})^{\prime}")], 1120, 665, 32)
        self.gat("a componente horizontal é menos ípsilon")
        my1, my2 = VGroup(*G1.p("a1")[1:3]), VGroup(*G1.p("a2")[1:3])
        resto = VGroup(*[g for g in G1[0] if g not in my1 and g not in my2])
        print(f"[origem] a {self.lote} D3-3 {self.t:.2f} {G1._tex[:60]!r} (molde; o −y voa duas vezes de PQ)")
        self.play(caneta(resto, ritmo=0.1))
        voa(self, PQ.p("my"), my1, rt=0.4)
        voa(self, PQ.p("my"), my2, rt=0.4)
        junta(self, G1)
        G2 = L([("eq", "="), ("m1", r"-1\cdot "), ("sm", SM), ("m", "+"), ("ay", r"(-\Y)"), ("ab", r"\big("), ("mn", "-"), ("al", r"\alpha\,"), ("pw", SM1),
                ("dt", r"\cdot "), ("d2", "2"), ("dY", r"\Y"), ("fp", r"\big)")], 1150, 750, 34)
        um_ = L([("v", "-1")], 0, 0, 26, "c")
        um_.move_to(G1.p("a1").get_center() + UP * 42 / 120)
        self.gat("a derivada de menos ípsilon em relação")
        escreve_p(self, G2, ["eq"], 0.2)
        escreve(self, um_, 0.2)
        voa(self, um_, G2.p("m1")[0:2], rt=0.45, extra=[FadeOut(um_)])
        self.remove(um_)
        self.play(caneta(G2.p("m1")[2], ritmo=0.2))
        voa(self, G1.p("sm"), G2.p("sm"), rt=0.4)
        escreve_p(self, G2, ["m"], 0.2)
        voa(self, G1.p("a2"), G2.p("ay"), rt=0.4)
        escreve_p(self, G2, ["ab", "mn", "al", "pw", "dt", "d2", "dY", "fp"], 0.12)
        junta(self, G2)
        self.gat("e a cadeia agora traz duas vezes")
        acende(self, [G2.p("dt", "d2", "dY"), PQ.p("s2")[3:5]], MAG, 0.6)
        G3 = L([("eq", "="), ("m1", "-"), ("sm", SM), ("pl", "+"), ("d2", "2"), ("al", r"\alpha"), ("y2", r"\Y^2"), ("pw", SM1)], 1150, 750, 34)
        self.gat("sai menos a potência mais")
        acende(self, [G2.p("ay")[1], G2.p("mn")], CORAL, 0.5)
        gm(self, G2, G3, rt=0.9, ka=["eq", "m1", "sm", "pl", "y2", "z", "pl", "al", "pw", "z", "d2", "y2", "z"], nota="((−y)(−α)·2y → +2αy²)")
        K4c = L([("a", SM), ("e", "="), ("s", "s"), ("d", r"\cdot"), ("b", SM1)], 1150, 840, 28)
        G4 = L([("eq", "="), ("m1", "-"), ("s", "s"), ("d", r"\cdot"), ("pw0", SM1), ("pl", "+"), ("d2", "2"), ("al", r"\alpha"), ("y2", r"\Y^2"), ("pw", SM1)], 1150, 750, 34)
        self.gat("em evidência o mesmo parêntese")
        escreve(self, K4c, 0.08)
        gm(self, G3, G4, rt=0.8, voos={"s": K4c.p("s"), "pw0": K4c.p("b")}, ka=["eq", "m1", "z", "pl", "d2", "al", "y2", "pw"], nota="(s^{−α} = s·s^{−α−1})")
        self.play(FadeOut(K4c), run_time=0.3)
        self.remove(K4c)
        G5 = L([("eq", "="), ("m1", "-"), ("pw", SM1), ("ab", r"\,(s"), ("mn", "-"), ("c", r"2\alpha\Y^2"), ("fc", ")")], 1150, 750, 34)
        gm(self, G4, G5, rt=0.9, ka=["eq", "m1", "ab", "z", "pw", "mn", "c", "c", "c", "pw"], nota="(evidência: −s^{−α−1})")
        F3 = L([("dQ", r"\dfrac{\partial\Pp}{\dy}="), ("neg", "-"), ("sm1", SM1), ("ab", r"\,(s"), ("m2", "-"), ("ax", r"2\alpha\Y^2"), ("fc", ")")], 1120, 682, 36)
        # substituição no molde do rot e os 6 glyph maps (alvo v2_d3r2 → r3)
        self.gat("e o sinal trocado")
        acende(self, [G5.p("m1")], CORAL, 0.25)
        funde(self, [G1, G5], F3, rt=0.5,ka=["dQ", "z", "z", "z", "z", "z"] + ["z", "neg", "sm1", "ab", "m2", "ax", "fc"])
        RS = L([("rot", r"\V{\rot}="), ("A", r"s^{-\alpha-1}(s-2\alpha\X^2)"), ("men", "-"), ("ap", r"\big("), ("B", r"-s^{-\alpha-1}(s-2\alpha\Y^2)"), ("fp", r"\big)")],
               1120, 772, 34)
        self.gat("ao subtrair menos com menos")
        gm(self, R0, RS, rt=0.9, copia=True, voos={"A": F2.p("sm1", "ab", "m2", "ax", "fc"), "B": F3.p("neg", "sm1", "ab", "m2", "ax", "fc")})
        RS2 = L([("rot", r"\V{\rot}="), ("A", r"s^{-\alpha-1}(s-2\alpha\X^2)"), ("pl", "+"), ("B", r"s^{-\alpha-1}(s-2\alpha\Y^2)")], 1120, 772, 34)
        gm(self, RS, RS2, rt=0.7, nota="(− com − vira +)")
        RS3 = L([("rot", r"\V{\rot}="), ("e", SM1), ("ap", "("), ("s1", "s"), ("ax", r"-2\alpha\X^2"), ("pl", "+"), ("s2", "s"), ("ay", r"-2\alpha\Y^2"), ("fp", ")")], 1120, 772, 34)
        self.gat("a distância ao quadrado aparece duas vezes")
        AA = Duas(RS2)
        AA.ks = ["rot", "e", "ap", "s1", "ax", "fp", "pl", "e", "ap2", "s2", "ay", "fp"]
        AA._rg = [RS2._rg[0]] + _split(RS2, 1, [5, 1, 1, 5, 1]) + [RS2._rg[2]] + _split(RS2, 3, [5, 1, 1, 5, 1])
        gm(self, AA, RS3, rt=0.9)
        self.remove(RS2)
        RS4 = L([("rot", r"\V{\rot}="), ("e", SM1), ("ap", "("), ("n2", "2"), ("s1", "s"), ("m", "-"), ("al", r"2\alpha"), ("q", r"(\X^2+\Y^2)"), ("fp", ")")], 1120, 772, 34)
        self.gat("os dois termos com alfa se juntam")
        gm(self, RS3, RS4, rt=0.9, ka=["rot", "e", "ap", "s1", "ax", "pl", "s1", "ax", "fp"], kb=["rot", "e", "ap", "s1", "s1", "m", "ax", "ax", "fp"])
        RS5 = L([("rot", r"\V{\rot}="), ("e", SM1), ("ap", "("), ("n2", "2"), ("s1", "s"), ("m", "-"), ("al", r"2\alpha"), ("q", "s"), ("fp", ")")], 1120, 772, 34)
        self.gat("que é a distância ao quadrado de novo")
        gm(self, RS4, RS5, rt=0.8, extra=[pisca_cor(PQ.p("s", "s2"), AMB, 0.8)])
        self.gat("no parêntese sobra dois esse")
        acende(self, [RS5.p("n2", "s1", "m", "al", "q")], AMB, 0.7)
        RS5b = L([("rot", r"\V{\rot}="), ("e", SM1), ("d", r"\cdot"), ("s", "s"), ("ap", "("), ("n2", "2"), ("m", "-"), ("al", r"2\alpha"), ("fp", ")")], 1120, 772, 34)
        self.gat("esse em evidência vezes dois")
        gm(self, RS5, RS5b, rt=0.9, ka=["rot", "e", "ap", "n2", "s", "m", "al", "s", "fp"], nota="(2s − 2αs = s(2 − 2α))")
        K5 = L([("a", "s"), ("d", r"\cdot"), ("b", SM1), ("e", "="), ("c", SM)], 1560, 840, 28)
        RS5c = L([("rot", r"\V{\rot}="), ("e", SM), ("ap", "("), ("n2", "2"), ("m", "-"), ("al", r"2\alpha"), ("fp", ")")], 1120, 772, 34)
        self.gat("e esse vezes a potência com um")
        escreve(self, K5, 0.1)
        gm(self, RS5b, RS5c, rt=0.8, ka=["rot", "e", "e", "e", "ap", "n2", "m", "al", "fp"], extra=[FadeOut(K5)], nota="(s·s^{−α−1} = s^{−α})")
        self.remove(K5)
        RS6 = L([("rot", r"\V{\rot}="), ("fr", r"\V{\dfrac{2-2\alpha}{s^{\alpha}}}")], 1120, 772, 36)
        self.gat("sobra uma fórmula curtinha")
        gm(self, RS5c, RS6, rt=0.9, ka=["rot", "fr", "fr", "fr", "fr", "fr", "fr"])
        RS7 = L([("rot", r"\V{\rot}="), ("fr", r"\V{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}")], 1120, 772, 36)
        gm(self, RS6, RS7, rt=0.8)
        # o divergente (alvo v2_d3r3): as linhas de ∂Q/∂x e ∂P/∂y fundem-se no rot final, que sobe
        RT = L([("rot", r"\V{\rot}="), ("fr", r"\V{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}")], 1120, 395, 36)
        self.gat("e o divergente")
        AT = Duas(R0, PQ, F2, F3, RS7)
        AT.ks = ["x"] * (len(R0.ks) + len(PQ.ks) + len(F2.ks) + len(F3.ks)) + ["rot", "fr"]
        gm(self, AT, RT, rt=1.0, nota="(fusão)")
        self.remove(R0, PQ, F2, F3, RS7)
        limpa_soltos(self)
        DV = L([("div", r"\D{\dv}="), ("dPx", r"\dfrac{\partial\Pp}{\dx}"), ("pl", "+"), ("dQy", r"\dfrac{\partial\Qq}{\dy}")], 1120, 505, 36)
        self.gat("agora é a soma")
        escreve(self, DV, 0.35)
        DP = L([("dPx", r"\dfrac{\partial\Pp}{\dx}="), ("my", r"-\Y"), ("d0", r"\cdot\dfrac{\partial(s^{-\alpha})}{\dx}"), ("c", r"=-\Y\big(-\alpha s^{-\alpha-1}\cdot2\X\big)"),
                ("r", r"=2\alpha\X\Y\,s^{-\alpha-1}")], 1120, 605, 27)
        DQ = L([("dPx", r"\dfrac{\partial\Qq}{\dy}="), ("my", r"\X"), ("d0", r"\cdot\dfrac{\partial(s^{-\alpha})}{\dy}"), ("c", r"=\X\big(-\alpha s^{-\alpha-1}\cdot2\Y\big)"),
                ("r", r"=-2\alpha\X\Y\,s^{-\alpha-1}")], 1120, 700, 27)
        self.gat("na primeira o menos ípsilon é constante")          # v4 C2: a constante sai da derivada
        escreve_p(self, DP, ["dPx", "my", "d0"], 0.15)
        acende(self, [DP.p("my")], GEO, 0.6)
        self.gat("na segunda o xis é constante")
        voa(self, DP.p("dPx", "my", "d0"), DQ.p("dPx", "my", "d0"), rt=0.6)
        acende(self, [DQ.p("my")], GEO, 0.6)
        self.gat("só a regra da cadeia trabalha")
        escreve_p(self, DP, ["c"], 0.1)
        escreve_p(self, DQ, ["c"], 0.1)
        self.gat("e sai o mesmo termo")
        escreve_p(self, DP, ["r"], 0.15)
        escreve_p(self, DQ, ["r"], 0.15)
        junta(self, DP)
        junta(self, DQ, origem="b")
        DS = L([("div", r"\D{\dv}="), ("t1", r"2\alpha\X\Y\,s^{-\alpha-1}"), ("t2", r"-2\alpha\X\Y\,s^{-\alpha-1}")], 1120, 800, 34)
        self.gat("uma vez com sinal de mais")
        gm(self, DV, DS, rt=0.9, copia=True, voos={"t1": DP.p("r")[1:], "t2": DQ.p("r")[1:]})
        self.gat("eles se cancelam zero")
        tr = cancela(self, DS, "t1", "t2")
        DZ = L([("div", r"\D{\dv}="), ("z", r"\D0")], 1120, 800, 34)
        gm(self, DS, DZ, rt=0.7, somem=tr)
        self.gat("nenhum desses redemoinhos")
        ped = quad30(VA, C0, S0)
        st = {"ped": ped, "giro": None}
        clareira(cmp, lambda: ou(clar_ped(st["ped"], .2), dq(C0, S0), clarPoly(circ_pts(.75, st["giro"]._giro[0], 12), .1) if st["giro"] else None))
        self.play(FadeIn(ped), run_time=0.3)
        self.play(anda(ped, flV(.5), T_FL(.5), 2.0, rate=linear, nome="D3 α = ½ (div)"))
        print(f"[D3] α = ½: área {S0 * S0:.3f} → {ped.area():.4f}")
        self.ate(1.0)

        # ── D3-4 · lendo a fórmula (alvo 09 v1 no α = ½) ──
        self.an("D3-4")
        RL = L([("rot", r"\V{\rot\vv}="), ("fr", r"\V{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}")], 1120, 600, 40)
        DL0 = L([("div", r"\D{\dv}\vv="), ("z", r"\D0")], 1120, 780, 40)
        self.gat("agora lê a fórmula")
        AD = Duas(DV, DP, DQ, DZ)
        AD.ks = ["x"] * (len(DV.ks) + len(DP.ks) + len(DQ.ks)) + ["div", "z"]
        fa2 = L([("a", r"\alpha="), ("0", r"0\quad"), ("m", r"\tfrac12\quad"), ("1", r"1\quad"), ("2", "2")], 1120, 400, 38)
        grp = lambda a: fa2.pi(IDX_A[a])
        fa2._origem = "a"
        print(f"[origem] a {self.lote} D3-4 {self.t:.2f} {fa2._tex!r}")
        em_paralelo(self, 0.8, lambda: gm(self, AD, DL0, nota="(fusão)"), lambda: gm(self, RT, RL), extra=[FadeOut(ped), caneta(fa2, ritmo=0.12)])
        self.remove(DV, DP, DQ, DZ, ped)
        limpa_soltos(self)
        st["ped"] = quad30(VA, C0, S0)
        cx = caixa_em(grp(1 if False else 0), pad=10)
        est["sub"] = None

        def le_a(a, ccw, legenda_txt, fr_solta=None):
            sai = [m for m in (st["ped"], st["giro"], st.get("lg")) if m is not None]
            st["giro"], st["lg"] = None, None
            ped = quad30(VA, C0, S0)
            self.play(*[FadeOut(m) for m in sai], FadeIn(ped), troca_p(cmp, a, 1.0), cx.animate.become(caixa_em(grp(a), pad=10)) if cx in self.mobjects else Create(cx), run_time=1.0)
            self.remove(*sai)
            st["ped"] = ped
            nova = L(SUB(a), 1150, 690, 36)
            if est["sub"] is None:
                gm(self, RL, nova, rt=0.8, copia=True, voos={"a": grp(a)})
            else:
                gm(self, est["sub"], nova, rt=0.7, voos={"a": grp(a)})
            est["sub"] = nova
            if fr_solta:
                self.gat(fr_solta)
            T_ = T_FL(a)
            self.play(anda(ped, flV(a), T_, 2.0, rate=linear, nome=f"D3 α = {a}"))
            c1 = ponto_fl(flV(a), C0, T_)
            print(f"[D3] α = {a}: t = {T_:.4f}, centro girou {math.atan2(c1[1], c1[0]):.4f} rad; área {S0 * S0:.3f} → {ped.area():.4f}")
            ans = []
            if ccw is not None:
                st["giro"] = giro30(VA, c1, .68, ccw)
                ans.append(Create(st["giro"]))
            if legenda_txt:
                st["lg"] = legenda(legenda_txt, 1124, 850, GEO, "left", 26)
                ans.append(FadeIn(st["lg"], shift=0.05 * UP))
            if ans:
                self.play(*ans, run_time=0.4)

        self.gat("alfa zero dois menos zero")
        le_a(0, True, "O DISCO GIRANDO RÍGIDO")
        self.gat("alfa meio dois menos um")
        le_a(.5, True, "SETAS DO MESMO TAMANHO, E O QUADRADINHO GIRA")
        self.gat("e mesmo assim o rotacional")                  # R16: a linha do rotacional citada acende
        acende(self, [est["sub"]], VIO, 1.0)
        self.gat("alfa um dois menos dois")
        le_a(1, None, "DÃO A VOLTA, E O QUADRADINHO NÃO GIRA")
        self.ate(1.0)

        # ── D3-5 · α = 2: gira no sentido horário ──
        self.an("D3-5")
        self.gat("e alfa dois")
        le_a(2, False, "VOLTA ANTI-HORÁRIA, GIRO HORÁRIO", fr_solta="e o quadradinho gira no sentido horário")
        a_ = math.atan2(*ponto_fl(flV(2), C0, T_FL(2))[::-1])
        u_ = np.array([math.cos(a_), math.sin(a_)])
        t_ = np.array([-u_[1], u_[0]])
        dest = []
        for r, Lr in ((1.75 - .35 - .2, .62), (1.75 + .35 + .2, .62 * ((1.75 + .55) / (1.75 - .55)) ** -1.8)):
            p = u_ * r
            dest.append(seta7(VA.c2p(*(p - t_ * Lr / 2)), VA.c2p(*(p + t_ * Lr / 2)), CAMPO2, 7, 22).set_z_index(12))
        self.gat("olha por quê")
        self.play(*[GrowArrow(d) for d in dest], run_time=0.5)
        self.gat("a seta do lado de dentro")                       # R16 v3: as setas citadas acendem, depois a borda do quadradinho
        acende(self, [dest[0]], AMB, 0.9)
        self.gat("que a do lado de fora")
        acende(self, [dest[1]], AMB, 0.9)
        self.gat("então a borda de dentro do quadradinho")
        acende(self, [st["ped"]], AMB, 1.0)
        self.play(*[FadeOut(d) for d in dest], run_time=0.4)
        self.remove(*dest)
        zera_chapas()
        cards = [cartao_alpha(0, 0, True), cartao_alpha(1, 1, None), cartao_alpha(2, 2, False)]
        tits = [leg_mix([r"$\alpha=0$", " · GIRA ", r"$\circlearrowleft$"], 360, 835, BR, "center", 32, bold=True),
                leg_mix([r"$\alpha=1$", " · NÃO GIRA"], 960, 835, BR, "center", 32, bold=True),
                leg_mix([r"$\alpha=2$", " · GIRA ", r"$\circlearrowright$"], 1560, 835, BR, "center", 32, bold=True)]
        rots = [L([("r", r"\rot = \V{2}")], 360, 895, 34, "c"), L([("r", r"\rot = \V{0}")], 960, 895, 34, "c"), L([("r", r"\rot = \V{-\dfrac{2}{r^4}}")], 1560, 895, 34, "c")]
        lgc = legenda("TODAS AS SETAS DÃO A VOLTA NO SENTIDO ANTI-HORÁRIO", 960, 968, GEO, "center", 28)
        cmp.clear_updaters()
        self.gat("o sentido da volta não é")
        self.limpa_junto()
        troca(self, "D3 palco → cartões α = 0/1/2")
        for r_, srcs in zip(rots, ("2", "0", "-2/r^4")):
            r_._origem = "b"
        self.play(*[FadeIn(c) for c in cards], *[FadeIn(t) for t in tits], *[TransformFromCopy(est["sub"].p("res"), r_) for r_ in rots], FadeIn(lgc), run_time=0.8)
        self.ate(1.0)

        # ── D3-6 · na origem (alvo 11 v1); em α = ½, os dois caminhos até a origem (alvo v3_d3or) ──
        self.an("D3-6")
        self.secao("A FAMÍLIA DE REDEMOINHOS · NA ORIGEM")

        def cartoes():
            zera_chapas()
            out = []
            for k, (a, mref) in enumerate(((.25, 2), (.5, 1), (1, 1))):
                X0 = CC[k][0]
                v = VB(CC[k], X0 + 240, 540, 56)
                ch = chapa_px(*CC[k], nome=f"D3 origem α = {a}", v=v)
                cp = campoP30(v, VORTA(a), -3.5, 3.5, -3.5, 3.5, .75, rmin=.3, mref=mref, nome=f"D3 origem α = {a}")
                pt = ponto7(v.c2p(0, 0), CAMPO2, 9, 9) if a == .25 else anel7(v.c2p(0, 0), GEO, 9, 3)
                out.append(VGroup(ch, cp, pt))
            return out
        orig = cartoes()
        t1 = [rotulo_tex(r"0<\alpha<\tfrac12", 360, 830, 32), rotulo_tex(r"\alpha=\tfrac12", 960, 830, 32), rotulo_tex(r"\alpha=1", 1560, 830, 32)]
        for m in t1:
            m._origem = "legenda"
        t2 = [legenda(s, x, 875, GEO, "center", 26) for s, x in (("A SETA VAI A ZERO", 360), ("TAMANHO 1, DIREÇÃO MUDA", 960), ("A SETA EXPLODE", 1560))]
        t3 = [T("CONTÍNUO SE v(0) = 0", 360, 920, 28, "center", CAMPO2, up=False), T("SEM LIMITE", 960, 920, 28, "center", CORAL),
              T("SEM LIMITE", 1560, 920, 28, "center", CORAL)]
        a0 = leg_mix([r"$\alpha=0$", " NÃO DIVIDE POR NADA: JÁ É CONTÍNUO NA ORIGEM"], 960, 985, GEO, "center", 26)
        lim = TC(r"\lim_{X\to 0}\F(X)", 600, 240, 34, "c")
        self.limpa_junto()
        troca(self, "D3 cartões α → cartões da origem")
        self.play(*[FadeIn(g) for g in orig], run_time=0.8)
        self.gat("lê-se limite de f quando x tende à origem")       # leitura 6: lim e X → 0 (escrito pequeno nessa hora)
        le(self, VGroup(*lim[0][:6]), 6, "limite de F quando X tende à origem", escreve_antes=lim, ate="com alfa zero não tem divisão")
        self.play(FadeIn(a0, shift=0.05 * UP), run_time=0.4)
        rz0 = L([("v", r"\|\vv\|="), ("n", r"r^{1-2\alpha}")], 1320, 240, 34, "c")
        rz = L([("c", r"0<\alpha<\tfrac12\ \Rightarrow\ 1-2\alpha>0\ \Rightarrow\ "), ("n", r"r^{1-2\alpha}"), ("t", r"\to 0")], 1320, 240, 32, "c")
        self.gat("com alfa entre zero e meio")
        self.play(FadeIn(t1[0], shift=0.05 * UP), FadeIn(t2[0], shift=0.05 * UP), run_time=0.4)
        self.gat("mas olha o expoente da rapidez")                    # v4 C3: por que a rapidez vai a zero
        escreve(self, rz0, 0.2)
        self.gat("distância pequena elevada a um número")
        gm(self, rz0, rz, rt=0.9, nota="(1 − 2α > 0 ⇒ r^{1−2α} → 0)")
        self.gat("a rapidez vai a zero")
        acende(self, [rz.p("t")], CAMPO2, 0.8)
        self.gat("o campo fica contínuo")
        self.play(FadeIn(t3[0], shift=0.05 * UP), run_time=0.4)
        # α = ½: o palco A com os dois caminhos
        self.gat("com alfa meio a rapidez fica um")
        sai = [*orig, t1[0], t2[0], t3[0], a0, lim]
        self.play(*[FadeOut(m) for m in sai], run_time=0.3)
        self.remove(*sai)
        zera_chapas()
        chO = chapa_px(*LA, nome="D3 origem α = ½ (palco)", v=VA)
        fo = campo30(VA, VORTA(.5), passo=.5, rmin=.3, mmax=1, ctx=True,
                     skip=lambda X, Y: (X > .3 and abs(Y) < .3) or (abs(X) < .3 and Y > .3), nome="D3 origem α = ½ (dois caminhos)")
        lx = vlinha(VA, [(3.6, 0), (.18, 0)], POS, 3, dash=(10, 8)).set_z_index(6)
        ly = vlinha(VA, [(0, 2.85), (0, .18)], E2, 3, dash=(10, 8)).set_z_index(6)
        ring = vcirc(VA, .12, BR, 3).set_z_index(8)
        o1 = L([("a", r"\alpha=\tfrac12:\quad "), ("n", r"\|\vv\|=r^{1-2\alpha}"), ("e", r"=r^{0}=1")], 1120, 270, 36)
        self.play(FadeIn(chO), cresce_campo(fo, 0.5), Create(lx), Create(ly), FadeIn(ring), run_time=0.5)
        gm(self, rz, o1, rt=0.5)
        ultimo = {}
        CAMS = (("x", [(2.4, 0), (1.5, 0), (.8, 0)], POS, (0, .32)), ("y", [(0, 2.4), (0, 1.5), (0, .8)], E2, (-.32, 0)))
        pts = {nome: ponto7(VA.c2p(*(3.6, 0) if nome == "x" else (0, 2.85)), cor, 7, 12) for nome, _, cor, _ in CAMS}
        rts = {}
        for nome, _, cor, _ in CAMS:                                  # v4 C3: o ponto de cada caminho tem o rótulo t
            rt_ = L([("t", "t")], 0, 0, 26, "c")
            rt_.move_to(pts[nome].get_center() + (DOWN if nome == "x" else RIGHT) * 26 / 120)
            rts[nome] = rt_
        tpos = legenda("t > 0", 150, 935, GEO, "left", 24)
        self.add(*pts.values())
        self.play(FadeIn(tpos), run_time=0.3)

        def caminho(nome, st, d):
            self.add(pts[nome])
            escreve(self, rts[nome], 0.2)
            rts[nome].add_updater(lambda m, p=pts[nome], n=nome: m.move_to(p.get_center() + (DOWN if n == "x" else RIGHT) * 26 / 120))
            for i in range(3):
                ar = seta7(VA.c2p(st[i][0] - d[0], st[i][1] - d[1]), VA.c2p(st[i][0] + d[0], st[i][1] + d[1]), CAMPO2, 6, 20).set_z_index(10)
                self.play(pts[nome].animate.move_to(VA.c2p(*st[i])), run_time=0.25)
                self.play(GrowArrow(ar), run_time=0.15)
                ultimo[nome] = ar
        o2a = L([("t", r"X=(t,\,0):\ \ "), ("v", r"\vv="), ("f", r"\dfrac{(-0,\ t)}{\sqrt{t^2}}")], 1120, 370, 32)
        o2 = L([("t", r"X=(t,\,0):\ \ "), ("v", r"\vv="), ("f", r"\dfrac{(-0,\ t)}{\sqrt{t^2}}"), ("e", "="), ("g", r"\dfrac{(0,\ t)}{t}"), ("e2", "="), ("val", r"(0,\,1)")],
               1120, 370, 32)
        o3a = L([("t", r"X=(0,\,t):\ \ "), ("v", r"\vv="), ("f", r"\dfrac{(-t,\ 0)}{\sqrt{t^2}}")], 1120, 470, 32)
        o3 = L([("t", r"X=(0,\,t):\ \ "), ("v", r"\vv="), ("f", r"\dfrac{(-t,\ 0)}{\sqrt{t^2}}"), ("e", "="), ("g", r"\dfrac{(-t,\ 0)}{t}"), ("e2", "="),
                ("val", r"(-1,\,0)")], 1120, 470, 32)
        self.gat("chegando pelo eixo xis")
        caminho(*CAMS[0][:2], CAMS[0][3])
        escreve(self, o2a, 0.1)
        self.gat("a seta é zero um")
        gm(self, o2a, o2, rt=0.8, nota="(√(t²) = t, t > 0; (0, t)/t = (0, 1))")
        acende(self, [ultimo["x"], o2.p("val")], CAMPO2, 0.8)
        self.gat("chegando pelo eixo ípsilon")
        caminho(*CAMS[1][:2], CAMS[1][3])
        escreve(self, o3a, 0.1)
        self.gat("dividido por tê menos um")
        gm(self, o3a, o3, rt=0.8, nota="((−t, 0)/t = (−1, 0))")
        acende(self, [ultimo["y"], o3.p("val")], CAMPO2, 0.8)
        for r_ in rts.values():
            r_.clear_updaters()
        ntl = T("NÃO TEM LIMITE", 1120, 650, 40, cor=CORAL)
        self.gat("não tem limite")
        self.play(FadeIn(ntl, shift=0.05 * UP), run_time=0.3)
        # de volta aos cartões (alvo 11)
        self.gat("e com alfa maior que meio")
        sai = [m for m in self.mobjects if m not in self.fixos() and not isinstance(m, ValueTracker) and m is not self.clk]
        self.play(*[FadeOut(m) for m in sai], run_time=0.3)
        self.remove(*sai)
        orig = cartoes()
        rz1 = L([("c", r"1-2\alpha>0\ \Rightarrow\ r^{1-2\alpha}\to 0")], 360, 240, 28, "c")
        rz2 = L([("c", r"1-2\alpha<0\ \Rightarrow\ r^{1-2\alpha}=\dfrac{1}{r^{2\alpha-1}}\to\infty")], 1560, 240, 28, "c")
        self.play(*[FadeIn(g) for g in orig], *[FadeIn(m) for m in (t1[0], t2[0], t3[0], a0, t1[1], t2[1], t3[1])], FadeIn(t1[2]), FadeIn(t2[2]),
                  run_time=0.5)
        escreve(self, rz1, 0.08)
        self.gat("o expoente um menos dois alfa fica negativo")     # v4 C3: por que a seta explode
        escreve(self, rz2, 0.08)
        self.gat("a seta explode")
        self.play(FadeIn(t3[2], shift=0.05 * UP), run_time=0.3)
        self.ate(1.0)

        # ── D3-7 · giro de 90° (alvo v2_d3g) ──
        self.an("D3-7")
        self.secao("A FAMÍLIA DE REDEMOINHOS · GIRO DE 90°")
        zera_chapas()
        vl, vr = VB(BE, 480, 540, 140), VB(BD, 1440, 540, 140)
        pe, pd = chapa_px(*BE, nome="D3 giro esq.", v=vl), chapa_px(*BD, nome="D3 giro dir.", v=vr)
        ce = campo30(vl, VORTA(1), -2.25, 2.25, -1.75, 2.25, .5, rmin=.45, mmax=2, nome="D3 redemoinho α = 1")
        cd = campo30(vr, VORTA(1), -2.25, 2.25, -1.75, 2.25, .5, rmin=.45, mmax=2, nome="D3 cópia (vai girar)")
        ok = {s._xy for s in campo30(vr, EXPLA(1), -2.25, 2.25, -1.75, 2.25, .5, rmin=.45, mmax=2, nome="D3 explosão (só p/ R7)")}
        for s in [s for s in cd if s._xy not in ok]:
            cd.remove(s)
        oe, od = ponto7(vl.c2p(0, 0), GEO, 6, 8), ponto7(vr.c2p(0, 0), GEO, 6, 8)
        n1 = legenda("REDEMOINHO", 480, 868, GEO, "center", 28)
        n2 = leg_mix(["CADA SETA GIRADA 90° ", r"$\circlearrowright$"], 1440, 868, GEO, "center", 28)
        VPQ = L([("v", r"\vv="), ("p", "("), ("P", r"\Pp"), ("vg", r",\ "), ("Q", r"\Qq"), ("fp", ")"), ("eq", "="), ("fr", r"\dfrac{(-\Y,\ \X)}{s^{\alpha}}")], 480, 955, 34, "c")
        sai_ = self.snap()                                         # v3: os cartões saem antes de o layout B entrar (sem legendas cruzadas)
        self.play(*[FadeOut(m) for m in sai_], run_time=0.15)
        self.remove(*sai_)
        troca(self, "D3 cartões → layout B (giro de 90°)")
        self.play(FadeIn(pe), FadeIn(pd), cresce_campo(ce, 0.3), FadeIn(oe), FadeIn(n1), run_time=0.3)
        self.gat("gira cada seta noventa graus")
        escreve(self, VPQ, 0.25, extra=[FadeIn(cd), FadeIn(od)])
        self.play(gira_setas(cd, -PI / 2, 1.2), FadeIn(n2), run_time=1.2)
        WQP = L([("w", r"\ww="), ("p", "("), ("Q", r"\Qq"), ("vg", r",\ "), ("mP", r"-\Pp"), ("fp", ")"), ("eq", "="), ("fr", r"\dfrac{(\X,\ \Y)}{s^{\alpha}}")], 1440, 955, 34, "c")
        self.gat("a componente horizontal nova")
        gm(self, VPQ, WQP, rt=1.0, copia=True, voos={"Q": VPQ.p("Q"), "mP": VPQ.p("P")})
        # v3 (margem ≥ 60 px do rodapé): as duas linhas de cima se fundem na do divergente (glyph map), que fica sozinha na faixa de baixo
        DW2 = L([("dw", r"\D{\dv\ww}="), ("dq", r"\dfrac{\partial\Qq}{\dx}-\dfrac{\partial\Pp}{\dy}"), ("rv", r"=\V{\rot\vv}"), ("fr", r"=\dfrac{2-2\alpha}{s^{\alpha}}"),
                  ("rw", r",\quad \V{\rot\ww}=0")], 960, 958, 30, "c")
        DW = L([("dw", r"\D{\dv\ww}="), ("dq", r"\dfrac{\partial\Qq}{\dx}-\dfrac{\partial\Pp}{\dy}"), ("rv", r"=\V{\rot\vv}"), ("fr", r"=\dfrac{2-2\alpha}{s^{\alpha}}")],
               DW2.get_left()[0] * 120 + 960, 958, 30, "l")
        DWa = L([("dw", r"\D{\dv\ww}="), ("dq", r"\dfrac{\partial\Qq}{\dx}-\dfrac{\partial\Pp}{\dy}")], DW2.get_left()[0] * 120 + 960, 958, 30, "l")
        self.gat("então o divergente novo")
        AW = Duas(VPQ, WQP)
        AW.ks = ["x"] * len(VPQ.ks) + ["dw", "x", "dq", "x", "dq", "x", "x", "x"]
        gm(self, AW, DWa, rt=0.8, nota="(fusão: as componentes novas entram na conta do divergente)")
        self.remove(VPQ, WQP)
        self.gat("exatamente a conta do rotacional antigo")
        gm(self, DWa, DW, rt=0.6)
        self.gat("o rotacional vira zero")
        gm(self, DW, DW2, rt=0.7)
        self.gat("é a falsa fonte do segundo episódio")              # palco: a explosão citada acende; depois o redemoinho
        acende(self, [cd], CAMPO2, 1.2)
        self.gat("guarda essa fórmula")
        acende(self, [ce, DW2.p("fr")], CAMPO2, 1.0)
        self.sai_fim()


def _split(lin, i, ns):
    """Divide a faixa de glifos da peça i de `lin` em sub-faixas de tamanhos ns (para mapear partes de uma peça)."""
    r = lin._rg[i]
    out, k = [], 0
    for n in ns:
        out.append(r[k:k + n])
        k += n
    if k != len(r):
        out[-1] = r[k - ns[-1]:]
    return out
