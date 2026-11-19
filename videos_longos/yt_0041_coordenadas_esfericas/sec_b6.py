"""yt_0041 · B6 · a casquinha (alvos 13a e 13b, v3). B6-1: o 3D pequeno gira ~30° e para (canto esquerdo), o corte meridiano grande (painel2d, "O CORTE: UMA PÁGINA");
CONE e ESFERA desde as cartesianas (z → r cos φ e √(x²+y²) → r sen φ voam das linhas; glyph maps 15), tg φ = 1 → φ = π/4 e r² = 2r cos φ → r = 2 cos φ; os
rótulos φ = π/4 e r = 2 cos φ voam das linhas para o corte; a receita: θ, φ (π/4 voa do corte) e r (a sonda cresce da origem até a calota; 2 cos φ voa do corte
para o limite de dentro); o encontro (1, 1). B6-2: o corte vai para a esquerda; a conta na ordem (r; u e du; limites novos; (−du); inversão; primitiva); V = π ✓;
CONFERE: o triângulo do cone violeta e a meia bola de cima ciano, no mesmo corte (π/3 e 2π/3 voam das peças)."""
from k41 import *
from sec_b1 import depois

X0 = 1020


def rotP(tex, x, y, size=36, al="c"):
    """Rótulo do corte 2D (painel opaco): fórmula com placa mínima; `.f` é a fórmula (fonte de voos)."""
    f = TC(tex, x, y, size, al)
    g = VGroup(placa_min(f), f)
    g.f = f
    g._txt = tex
    return g


def corte(X0_, Y0_, w, h, u, ox=90):
    """O corte meridiano (página θ = cte) num painel2d41: região, eixos z e s, reta do cone (violeta), círculo r = 2 cos φ (coral), tracejados até (1, 1).
    Devolve um dicionário de peças (cada uma entra no seu gatilho)."""
    O = {}
    O["pan"] = painel2d41(X0_, Y0_, w, h)
    O["tit"] = leg("O CORTE: UMA PÁGINA", X0_ + 24, Y0_ + 44, TH, "left", 26)
    V = Vista2D(X0_ + ox, Y0_ + h - 50, u)
    O["V"] = V
    pts = [(0, 0)] + [(2 * math.cos(f) * math.sin(f), 2 * math.cos(f) * math.cos(f)) for f in np.linspace(0, PI / 4, 41)]
    O["reg"] = Polygon(*[PX(*V.P(*p)) for p in pts]).set_fill(mixh("#16123A", CI, .30), 1).set_stroke(width=0).set_z_index(-1)
    O["eix"] = VGroup(V.seta((0, 0), (1.45, 0), SOMB), V.seta((0, 0), (0, 2.3), EZ))
    O["cone"] = V.linha([(0, 0), (1.35, 1.35)], FI, 5)
    O["circ"] = V.linha([(math.cos(a), 1 + math.sin(a)) for a in np.linspace(-PI / 2, PI / 2, 91)], CORAL, 5)
    O["trac"] = VGroup(V.linha([(1, 1), (1, 0)], GEO, 2, dash=(7, 7)), V.linha([(1, 1), (0, 1)], GEO, 2, dash=(7, 7)), V.ponto((1, 1), BR, 9))
    O["lz"] = TC(r"\Z", V.P(0, 2.3)[0] + 14, V.P(0, 2.3)[1] + 8, 34, "c")
    O["ls"] = TC(r"\Rs", V.P(1.45, 0)[0] - 6, V.P(1.45, 0)[1] - 26, 34, "c")
    O["l1"] = TC("1", V.P(1, 0)[0] - 8, V.P(1, 0)[1] + 24, 30, "c")
    O["l2"] = TC("2", V.P(0, 2)[0] - 34, V.P(0, 2)[1], 30, "c")
    O["l11"] = rotP(r"(1,\,1)", V.P(1, 1)[0] - 14, V.P(1, 1)[1] + 34, 34, "r")
    O["lphi"] = rotP(r"\Fi{\varphi=\dfrac{\pi}{4}}", V.P(1.12, 0.55)[0], V.P(1.12, 0.55)[1], 36, "l")
    return O


class PB6(B41):
    ANTES = "DE VOLTA À BOLA"

    def corpo(self):
        # ── B6-1 ────────────────────────────────────────────────────────────────────────────────────────
        self.an("B6-1")
        self.papel_on(rt=0)                                                     # G1: papel também atrás do 3D
        cq = self.palco("casquinha", cam_alvo("b6"), giro=-30.0, obst=["O", "encontro"], sonda=0.0, duas=0.0, arcofi=0.0, encontro=0.0)
        self.add(cq.fundo)
        self.titulo("A CASQUINHA", rt=0.3)
        self.gat("uma casquinha de sorvete")
        O = corte(60, 560, 640, 480, 150, ox=150)
        V2d = O["V"]
        self.play(cq.tr["giro"].animate(rate_func=smooth).set_value(0.0), Create(O["pan"]), FadeIn(O["reg"]), run_time=2.0)    # gira ~30° e para; o painel entra junto (D12)
        self.play(Create(O["eix"]), Create(O["circ"]), run_time=0.4)
        rz = self.rot3(cq, "ez", r"\Z", dx=14, size=34)

        self.gat("embaixo o cone")
        c1 = mixl([("t", "CONE", FI), ("L", [("z", r"\Z"), ("eq", "="), ("rt", r"\sqrt{\X^2+\Y^2}")])], X0, 210, 46)
        self.pena(c1.p[0])
        self.pena(c1.p[1])
        self.degrau("C10b-cone", "CONE z = √(x² + y²)")
        self.play(Create(O["cone"]), run_time=0.5)
        self.pena(rz, O["tit"], O["lz"], O["ls"], lag=0.08)
        self.dentro(O["pan"]._painel, O["tit"], O["lz"], O["ls"])
        self.gat("em cima a esfera")
        e1 = mixl([("t", "ESFERA", CORAL), ("L", [("l", r"\X^2+\Y^2+\Z^2"), ("eq", "="), ("r", r"2\Z")])], X0, 430, 46)
        self.pena(e1.p[0])
        self.pena(e1.p[1])
        self.degrau("C10b-esfera", "ESFERA x² + y² + z² = 2z")
        self.gat("z é r cosseno de fi")
        A = L([("rc", r"\R\cos\F"), ("eq", "="), ("rs", r"\R\sen\F")], 1050, 310, 46)
        self.voos([(gl(c1.p[1], "z"), parte(A, sel(A, "rc"), "r cos φ"))], rt=0.9, nota="B6-1: o z voa da linha CONE e vira r cos φ")
        self.gat("é a sombra r seno de fi")
        self.voos([(gl(c1.p[1], "rt"), parte(A, sel(A, "rs"), "r sen φ"))], rt=0.9, nota="B6-1: √(x²+y²) voa da linha CONE e vira r sen φ (a sombra)")
        self.pena(parte(A, sel(A, "eq"), "="))
        self.degrau("C10b-cone", "r cos φ = r sen φ")
        self.gat("corta o r dos dois lados")
        B = depois(L([("im", r"\Rightarrow"), ("tg", r"\operatorname{tg}"), ("f", r"\F"), ("eq", "="), ("um", "1")], 0, 310, 46), A, sel(A, "eq")[0], 4, gap=14)
        rc, rs = sel(A, "rc"), sel(A, "rs")               # r, c, o, s, φ
        self.gm(15, A, B, [(rs[1:4] + rc[1:4], "tg"), ([rc[4], rs[4]], "f"), ("eq", "eq"), ([rc[0], rs[0]], "um")], copia=True, nota="r cos φ = r sen φ → tg φ = 1")
        self.degrau("C10b-cone", "⇒ tg φ = 1")
        self.gat("quarenta e cinco graus")
        C = L([("im", r"\Rightarrow"), ("f", r"\F"), ("eq", "="), ("v", r"\dfrac{\pi}{4}")], 0, 310, 46)
        C.shift(B[0][0].get_center() - C[0][0].get_center())
        self.gm(15, B, C, [("im", "im"), ("f", "f"), ("eq", "eq"), ("um", "v")], nota="tg φ = 1 → φ = π/4")
        self.degrau("C10b-cone", "⇒ φ = π/4")
        lcone = O["lphi"]
        self.voos([(VGroup(*C[0][1:]), lcone)], rt=0.9, nota="B6-1: φ = π/4 voa da linha CONE para o corte")
        self.dentro(O["pan"]._painel, lcone)

        self.gat("a soma dos quadrados que a gente já sabe")
        E = L([("l", r"\R^2"), ("eq", "="), ("r", r"2\R\cos\F")], 1050, 530, 46)
        self.voos([(gl(e1.p[1], "l"), parte(E, sel(E, "l"), "r²"))], rt=0.9, arco=0.0, nota="B6-1: x² + y² + z² voa da linha ESFERA e vira r²")
        self.gat("o lado direito dois z")
        self.pena(parte(E, sel(E, "eq"), "="))
        self.voos([(gl(e1.p[1], "r"), parte(E, sel(E, "r"), "2r cos φ"))], rt=0.9, arco=0.0, nota="B6-1: 2z voa da linha ESFERA e vira 2r cos φ")
        self.degrau("C10b-esfera", "r² = 2r cos φ")
        self.gat("divide os dois lados por r")
        pl = leg("(r > 0)", pxof(E.get_right())[0] + 16, 530 + 9, GEO, "left", 28)
        pl_ = VGroup(placa_min(pl, 8, 4), pl)
        pl_._txt = "(r > 0)"
        self.pena(pl_)
        l_, r_ = sel(E, "l"), sel(E, "r")                 # r, ² ; 2, r, c, o, s, φ
        self.acende_sai(VGroup(E[0][l_[1]]), VGroup(E[0][r_[1]]), cor=MEN, rt=0.4, rt_vis=0.3)
        F2 = depois(L([("im", r"\Rightarrow"), ("r", r"\R"), ("eq", "="), ("v", r"2\cos\F")], 0, 530, 46), E, sel(E, "eq")[0], 2, gap=170)
        self.gm(15, E, F2, [([l_[0]], "r"), ("eq", "eq"), ([r_[0]] + r_[2:], "v")], copia=True, extra=[FadeOut(pl_)], nota="r² = 2r cos φ → r = 2 cos φ")
        self.remove(pl_)
        self.acende_sai(VGroup(E[0][l_[1]]), VGroup(E[0][r_[1]]), cor=BR, rt=0.3, rt_vis=0)
        F2.shift(LEFT * (pxof(F2.get_left())[0] - pxof(E.get_right())[0] - 14) / 120)
        self.degrau("C10b-esfera", "⇒ r = 2 cos φ")
        pe = (2 * math.cos(PI / 6) * math.sin(PI / 6), 2 * math.cos(PI / 6) * math.cos(PI / 6))
        lcal = rotP(r"\Co{\R=2\cos\F}", V2d.P(*pe)[0] + 26, V2d.P(*pe)[1] - 8, 36, "l")
        self.voos([(VGroup(*F2[0][1:]), lcal)], rt=0.9, arco=0.0, nota="B6-1: r = 2 cos φ voa da linha ESFERA para o corte")
        self.dentro(O["pan"]._painel, lcal)
        self.gat("completar o quadrado em z")
        cc = mixl([("m", r"\X^2+\Y^2+(\Z-1)^2=1"), ("t", "CENTRO (0, 0, 1)", GEO)], 1050, 620, 36)
        self.pena(*cc.p, lag=0.15)
        self.degrau("C10b-esfera", "x² + y² + (z − 1)² = 1 (centro (0, 0, 1), raio 1)")

        V = L([("V", "V"), ("eq", "="), ("i3", r"\int_0^{2\pi}\!\!"), ("i2", r"\int_0^{\pi/4}\!\!"), ("i1", r"\int_0^{\Co{2\cos}\F}"), ("j", r"\J"),
               ("d", r"\;\dR\,\dF\,\dT")], X0, 780, 50)
        i3, i2, i1 = sel(V, "i3"), sel(V, "i2"), sel(V, "i1")   # ∫ 2 π 0 | ∫ π / 4 0 | ∫ 2 c o s φ 0
        self.gat("agora a receita")
        self.pena(parte(V, sel(V, ["V", "eq"]), "V ="))
        self.gat("a casquinha gira inteira")
        self.pena(parte(V, i3, "∫₀^{2π}"))
        self.degrau("C10b-V", "θ de 0 a 2π")
        self.gat("do eixo até o cone")
        cq.set(arcofi=1.0)
        self.pena(parte(V, [i2[0], i2[-1]], "∫ 0"))
        self.voos([(VGroup(*lcone.f[0][2:]), parte(V, i2[1:-1], "π/4"))], rt=0.9, nota="B6-1: π/4 voa do corte para o limite de φ")
        self.degrau("C10b-V", "φ de 0 a π/4")
        self.gat("a sonda sai da ponta")
        sd = VGroup(V2d.linha([(0, 0), pe], RO, 6), V2d.ponto((0, 0), AZC, 10), V2d.ponto(pe, CORAL, 10),
                    V2d.arco(.5 * 150, PI / 2, PI / 2 - PI / 6, FI, 4))
        lfs = rotP(r"\F", V2d.P(.12, .62)[0] - 4, V2d.P(.12, .62)[1] - 14, 36, "c")
        self.play(cq.tr["sonda"].animate(rate_func=linear).set_value(1.0), Create(sd), run_time=1.6)        # a sonda cresce da origem até a calota
        self.pena(lfs, lcal)
        self.pena(parte(V, [i1[0], i1[-1]], "∫ 0"))
        self.gat("para na esfera em dois cosseno")
        self.voos([(VGroup(*lcal.f[0][2:]), parte(V, i1[1:-1], "2 cos φ"))], rt=0.9, nota="B6-1: 2 cos φ (coral) voa do corte para o limite de dentro")
        self.pena(parte(V, sel(V, ["j", "d"]), "r² sen φ dr dφ dθ"))
        self.degrau("C10b-V", "r de 0 a 2 cos φ; V = ∫₀^{2π}∫₀^{π/4}∫₀^{2cos φ} r² sen φ dr dφ dθ")
        self.gat("o encontro")
        cq.set(encontro=1.0)
        self.play(Create(O["trac"]), run_time=0.5)
        self.pena(O["l11"], O["l1"], O["l2"], lag=0.1)
        self.dentro(O["pan"]._painel, O["l11"], O["l1"], O["l2"], lfs)
        self.col("B6-1", c1, A, e1, E, cc, V)
        self.marca("13_B6a", agora=True)

        # ── B6-2 ────────────────────────────────────────────────────────────────────────────────────────
        self.an("B6-2")
        self.gat("monta a integral")
        self.sobe_sai(c1, A, B, C, e1, E, F2, cc, lcone, lcal, lfs, sd, dy=0.3, rt=0.5)
        cq.set(sonda=0.0, arcofi=0.0)
        self.play(V.animate.scale(0.68, about_point=V.get_left()).shift(PX(720, 200) - V.get_left()), run_time=0.6)
        self.col_zera("B6-1")
        La = L([("pr", r"\Big[\dfrac{\R^3}{3}\Big]_0^{\Co{2\cos}\F}"), ("sf", r"\sen\F"), ("eq", "="), ("c", r"\dfrac{(2\cos\F)^3}{3}"), ("sf2", r"\sen\F"),
                ("m0", r"-0")], 720, 320, 44)
        self.gat("a de dentro em r")
        self.pena(parte(La, sel(La, ["pr", "sf"]), "[r³/3]₀^{2cos φ} sen φ"))
        self.degrau("C10", "[r³/3]₀^{2 cos φ} sen φ")
        self.gat("cuidado com o cubo")
        self.pena(parte(La, sel(La, ["eq", "c"]), "= (2 cos φ)³/3"))
        self.gat("embaixo zero")
        self.pena(parte(La, sel(La, "m0"), "− 0"))
        self.gat("com o seno de fi que estava esperando")
        self.pena(parte(La, sel(La, "sf2"), "sen φ"))
        self.degrau("C10", "= (2 cos φ)³/3 · sen φ − 0")
        self.gat("fica oito terços")
        Lb = L([("eq2", "="), ("r", r"\dfrac83\cos^3\!\F\,\sen\F")], 780, 420, 44)
        c_, s2_, r_ = sel(La, "c"), sel(La, "sf2"), sel(Lb, "r")    # c: (, 2, c, o, s, φ, ), ³, —, 3 ; r: 8, —, 3, c, o, s, ³, φ, s, e, n, φ
        self.gm(16, La, Lb, [([c_[1]], [r_[0]]), ([c_[8]], [r_[1]]), ([c_[9]], [r_[2]]), (c_[2:5], r_[3:6]), ([c_[7]], [r_[6]]), ([c_[5]], [r_[7]]), (s2_, r_[8:])],
                copia=True, nota="(2 cos φ)³/3 · sen φ → (8/3) cos³φ sen φ")
        self.degrau("C10", "= (8/3) cos³φ sen φ")
        La = VGroup(La, Lb)

        U1 = L([("u", r"\uu=\cos\F,"), ("du", r"\ \ \du=-\sen\F\,\dF")], 720, 520, 44)
        self.gat("a do meio pede uma troca de variável")
        self.gat("então u igual a cosseno de fi")
        self.pena(parte(U1, sel(U1, "u"), "u = cos φ"))
        self.gat("e d u igual a menos seno")
        self.pena(parte(U1, sel(U1, "du"), "du = −sen φ dφ"))
        self.degrau("C10", "u = cos φ, du = −sen φ dφ")
        self.gat("troca os limites junto")
        U2 = L([("a", r"\F=0\to\uu=1,"), ("b", r"\ \ \F=\dfrac{\pi}{4}\to\uu=\dfrac{\sqrt2}{2}")], 720, 610, 44)
        self.pena(parte(U2, sel(U2, "a"), "φ = 0 → u = 1"))
        self.gat("e fi pi sobre quatro vira")
        self.pena(parte(U2, sel(U2, "b"), "φ = π/4 → u = √2/2"))
        self.degrau("C10", "limites novos: φ = 0 → u = 1; φ = π/4 → u = √2/2")

        Lf = L([("i", r"\int_0^{\pi/4}"), ("f", r"\dfrac83\cos^3\!\F\,\sen\F"), ("d", r"\,\dF")], 720, 710, 44)
        Lf2 = L([("eq", "="), ("k", r"\dfrac83"), ("iu", r"\int_1^{\sqrt2/2}"), ("u3", r"\uu^3"), ("du", r"(-\du)")], 0, 710, 44)
        Lf2.shift(RIGHT * (Lf.get_right()[0] + 12 / 120 - Lf2.get_left()[0]))
        self.gat("substitui tudo")
        self.pena(parte(Lf, sel(Lf, "i"), "∫₀^{π/4}"))
        self.voos([(gl(Lb, "r"), parte(Lf, sel(Lf, "f"), "(8/3) cos³φ sen φ"))], rt=0.9, nota="B6-2: (8/3) cos³φ sen φ voa da linha 1")
        self.pena(parte(Lf, sel(Lf, "d"), "dφ"))
        self.degrau("C10", "∫₀^{π/4} (8/3) cos³φ sen φ dφ")
        self.pena(Lf2)
        self.degrau("C10", "= (8/3)∫₁^{√2/2} u³ (−du)")
        self.gat("o menos serve justamente")
        Lg = L([("eq", "="), ("k", r"\dfrac83"), ("iu", r"\int_{\sqrt2/2}^{1}"), ("u3", r"\uu^3"), ("du", r"\,\du")], 0, 710, 44)
        Lg.shift(Lf2[0][0].get_center() - Lg[0][0].get_center())
        iu, iv = sel(Lf2, "iu"), sel(Lg, "iu")     # ∫, √, —, 2, /, 2 (cima), 1 (baixo)  →  ∫, 1 (cima), √, —, 2, /, 2 (baixo)
        du_a, du_b = sel(Lf2, "du"), sel(Lg, "du")  # (, −, d, u, )  →  d, u
        lmi = leg("O MENOS INVERTE OS LIMITES", 1290, 822, UU, "left", 30)
        self.pena(lmi)
        self.acende_sai(VGroup(Lf2[0][du_a[1]]), cor=MEN, rt=0.3, rt_vis=0.2)
        self.gm(16, Lf2, Lg, [("eq", "eq"), ("k", "k"), ([iu[0]], [iv[0]]), (iu[1:6], iv[2:7]), ([iu[6]], [iv[1]]), ("u3", "u3"), (du_a[2:4], du_b)],
                nota="(8/3)∫₁^{√2/2} u³(−du) → (8/3)∫_{√2/2}^1 u³ du (os limites trocam de lugar e o menos sai, no mesmo mapa)")
        self.degrau("C10", "= (8/3)∫_{√2/2}^1 u³ du")

        # a coluna rola: as linhas de cima saem; a integral em u sobe com o chip
        self.gat("daí é a primitiva de u ao cubo")
        self.sobe_sai(La, U1, U2, Lf, Lf2, lmi, dy=0.3, rt=0.5, extra=[])
        self.play(Lg.animate.shift(PX(780, 340) - Lg.get_left()), run_time=0.6)
        Lp = L([("eq", "="), ("k", r"\dfrac83"), ("pr", r"\Big[\dfrac{\uu^4}{4}\Big]_{\sqrt2/2}^{1}"), ("eq2", "="), ("k2", r"\dfrac83"), ("a", r"\Big(\dfrac14"),
                ("m", "-"), ("b", r"\dfrac1{16}\Big)")], 720, 470, 44)
        self.pena(parte(Lp, sel(Lp, ["eq", "k", "pr"]), "= (8/3)[u⁴/4]"))
        self.degrau("C10", "= (8/3)[u⁴/4]_{√2/2}^1")
        self.gat("aplica em um")
        self.pena(parte(Lp, sel(Lp, ["eq2", "k2", "a"]), "= (8/3)(1/4"))
        self.degrau("C10", "em 1: 1/4")
        Ls = L([("a", r"\Big(\dfrac{\sqrt2}{2}\Big)^4=\dfrac{4}{16}=\dfrac14"), ("b", r",\quad\dfrac14\div4=\dfrac1{16}")], 780, 590, 34)
        self.gat("raiz de dois sobre dois à quarta")
        self.pena(parte(Ls, sel(Ls, "a"), "(√2/2)⁴ = 4/16 = 1/4"))
        self.degrau("C10", "(√2/2)⁴ = 4/16 = 1/4")
        self.gat("dividido por quatro")
        self.pena(parte(Ls, sel(Ls, "b"), "1/4 ÷ 4 = 1/16"))
        self.degrau("C10", "÷ 4 = 1/16")
        self.pena(parte(Lp, sel(Lp, ["m", "b"]), "− 1/16)"))
        self.degrau("C10", "(8/3)(1/4 − 1/16)")
        self.gat("o mmc é dezesseis")
        Lq = L([("eq", "="), ("k", r"\dfrac83"), ("d", r"\cdot"), ("f", r"\dfrac3{16}")], 780, 700, 44)
        a_, b_ = sel(Lp, "a"), sel(Lp, "b")        # (, 1, —, 4 ; 1, —, 1, 6, )
        self.gm(17, Lp, Lq, [("eq2", "eq"), ("k2", "k"), ([a_[2]] + [b_[1]], [sel(Lq, "f")[1]]), ([a_[1], a_[3], b_[0]], [sel(Lq, "f")[0]]), (b_[2:4], sel(Lq, "f")[2:])],
                copia=True, nota="(8/3)(1/4 − 1/16) → (8/3)(3/16)")
        self.degrau("C10", "= (8/3) · (3/16)")
        self.gat("o três cancela com o três")
        Lh = depois(L([("eq", "="), ("r", r"\dfrac12")], 0, 700, 44), Lq, 0, 0)
        k_, f_ = sel(Lq, "k"), sel(Lq, "f")        # 8, —, 3 ; 3, —, 1, 6
        self.acende_sai(VGroup(Lq[0][k_[0]]), VGroup(*[Lq[0][i] for i in f_[2:]]), cor=MEN, rt=0.35, rt_vis=0.3)        # 8 com 16
        self.acende_sai(VGroup(Lq[0][k_[2]]), VGroup(Lq[0][f_[0]]), cor=E1, rt=0.35, rt_vis=0.3)                        # 3 com 3
        self.gm(17, Lq, Lh, [([k_[1], f_[1]], [2])], copia=True, nota="(8/3)(3/16) → 1/2 (8 com 16, 3 com 3, em dois tempos)")
        self.acende_sai(VGroup(Lq[0][k_[0]]), VGroup(*[Lq[0][i] for i in f_[2:]]), VGroup(Lq[0][k_[2]]), VGroup(Lq[0][f_[0]]), cor=BR, rt=0.3, rt_vis=0)
        self.degrau("C10", "= 1/2")
        self.col("B6-2a", V, Lg, Lp, Ls, Lq)

        # a última linha sobe junto com o chip, numa só animação
        self.gat("a de téta multiplica por dois pi")
        self.sobe_sai(Lg, Lp, Ls, dy=0.3, rt=0.5)
        sobe = self.velhos(Lq, Lh)
        self.play(sobe.animate.shift(UP * (700 - 340) / 120), run_time=0.6)
        Vf = L([("V", "V"), ("eq", "="), ("a", r"2\pi"), ("d", r"\cdot"), ("b", r"\dfrac12")], 720, 470, 46)
        self.gat("o volume é pi")
        self.pena(parte(Vf, sel(Vf, ["V", "eq", "a", "d"]), "V = 2π ·"))
        self.voos([(gl(Lh, "r"), parte(Vf, sel(Vf, "b"), "1/2"))], rt=0.8, nota="B6-2: o 1/2 voa da conta")
        self.degrau("C10", "V = 2π · 1/2")
        Vp = depois(L([("eq", "="), ("p", r"\Me{\pi}")], 0, 470, 46), Vf, 1, 0)
        self.gm(17, Vf, Vp, [(sel(Vf, "a") + sel(Vf, "b"), "p")], copia=True, nota="2π · 1/2 → π")
        self.degrau("C10", "= π")
        ck = check_px(pxof(Vp.get_right())[0] + 40, 470)
        self.play(Create(ck), run_time=0.4)

        self.gat("confere pela geometria")
        cq.set(duas=1.0)                                         # só a cor muda no 3D pequeno; o corte 2D pinta as duas peças
        tri = Polygon(*[PX(*O["V"].P(*p)) for p in [(0, 0), (1, 1), (0, 1)]]).set_fill(mixh("#16123A", FI, .45), 1).set_stroke(width=0).set_z_index(0)
        cap = Polygon(*[PX(*O["V"].P(*p)) for p in [(0, 1)] + [(math.cos(a), 1 + math.sin(a)) for a in np.linspace(0, PI / 2, 31)]]).set_fill(
            mixh("#16123A", CI, .45), 1).set_stroke(width=0).set_z_index(0)
        self.play(FadeIn(tri), FadeIn(cap), run_time=0.4)
        cf = mixl([("t", "CONFERE", MEN), ("L", [("a", r"\dfrac{\pi}{3}"), ("p", "+"), ("b", r"\dfrac{2\pi}{3}")])], 720, 640, 40)
        cb_ = leg("CONE + MEIA BOLA", 780, 730, GEO, "left", 30)
        self.pena(cf.p[0], cb_, lag=0.2)
        p1 = rotP(r"\dfrac{\pi}{3}", O["V"].P(.3, .28)[0], O["V"].P(.3, .28)[1], 32, "c")
        p2 = rotP(r"\dfrac{2\pi}{3}", O["V"].P(.42, 1.5)[0], O["V"].P(.42, 1.5)[1], 32, "c")
        self.gat("embaixo um cone de raio um")
        self.pena(p1)
        self.gat("em cima meia bola")
        self.pena(p2)
        self.gat("somou pi")
        Q = cf.p[1]
        self.voos([(p1.f, parte(Q, sel(Q, "a"), "π/3")), (p2.f, parte(Q, sel(Q, "b"), "2π/3"))], rt=0.8, nota="B6-2: π/3 e 2π/3 voam das duas peças")
        self.pena(parte(Q, sel(Q, "p"), "+"), passo=0.03)
        self.degrau("C10-confere", "π/3 + 2π/3")
        Qr = depois(L([("eq", "="), ("p", r"\pi")], 0, 640, 40), Q, 0, 0, gap=14)
        Qr.shift(UP * (Q.get_center()[1] - Qr.get_center()[1]))
        a_, b_ = sel(Q, "a"), sel(Q, "b")          # π, —, 3 ; 2, π, —, 3
        self.gm(17, Q, Qr, [([a_[0], b_[1]], "p")], copia=True, rt=0.9, nota="π/3 + 2π/3 → π")
        self.degrau("C10-confere", "= π")
        self.col("B6-2b", V, Lq, Vf, cf)
        self.marca("13_B6")
        self.sai_fim()
