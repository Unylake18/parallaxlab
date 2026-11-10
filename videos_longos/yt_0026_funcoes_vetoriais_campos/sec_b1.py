"""Lote PB1 · QUE FUNÇÃO É ESSA (B1-1…B1-4): curva ℝ → ℝᵐ e gráfico ℝⁿ → ℝ; a definição f : A ⊂ ℝⁿ → ℝᵐ com o terceiro ícone e os três
mini-exemplos; a contagem de eixos (2 + 1 = 3 cabe; 2 + 2 = 4, o quarto eixo bate na borda e some); os dois cartões TRANSFORMAÇÃO e CAMPO VETORIAL."""
from kit import *  # noqa: F401,F403

EX, EY, EZ = np.array([-0.55, -0.42, 0.0]), np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])


def pj(c, x, y, z, s=1.0):
    return c + s * (x * EX + y * EY + z * EZ)


def eixos3(c, s=1.0):
    return VGroup(eixo_seta(c, c + s * 1.9 * EX), eixo_seta(c, c + s * 1.9 * EY), seta(c, c + s * 1.9 * EZ, SAI, 3, tip=0.16))


def icone_curva(c):
    o = c + P3(-1.3, -0.9)
    ax = VGroup(eixo_seta(o, o + P3(2.7, 0)), eixo_seta(o, o + P3(0, 2.0)))
    cur = ParametricFunction(lambda t: o + P3(0.25 + 2.1 * t, 0.35 + 1.1 * t + 0.45 * math.sin(5 * t)), t_range=[0, 1]).set_stroke(POS, W_GAMA)
    return VGroup(ax, cur, ponto(cur.point_from_proportion(0.7), POS, 0.09))


def icone_grafico(c):
    o = c + P3(-0.7, -0.75)
    ax = eixos3(o, 0.85)
    f = lambda x, y: 0.55 + 0.25 * math.sin(2.6 * x) * math.cos(2.2 * y)
    sup = VGroup()
    for x in np.linspace(0.15, 1.35, 6):
        sup.add(ParametricFunction(lambda t, x=x: pj(o, x, t, f(x, t), 0.95), t_range=[0.15, 1.6]).set_stroke(SAI, 2))
    for y in np.linspace(0.15, 1.6, 7):
        sup.add(ParametricFunction(lambda t, y=y: pj(o, t, y, f(t, y), 0.95), t_range=[0.15, 1.35]).set_stroke(SAI, 2))
    return VGroup(ax, sup)


def icone_vetorial(c):
    a = chapa(Ellipse(width=1.3, height=0.95).move_to(c + P3(-0.9, -0.1)), "dom")
    b = chapa(Ellipse(width=1.3, height=0.95).move_to(c + P3(0.95, 0.15)), "img")
    pa, pb = ponto(a.get_center() + P3(0.1, 0.05), GEO, 0.07), ponto(b.get_center() + P3(-0.05, 0.1), SAI_F, 0.07)
    arco = voo(pa.get_center() + P3(0.08, 0.12), pb.get_center() + P3(-0.1, 0.12), angle=-1.0, w=2.5, tip=0.14)
    return VGroup(a, b, pa, pb, arco)


def icone_malha(c):
    g = VGroup()
    def w(x, y):
        return c + P3(x + 0.18 * math.sin(2.2 * y), y + 0.18 * math.sin(2.2 * x))
    for k in np.linspace(-1, 1, 5):
        g.add(ParametricFunction(lambda t, k=k: w(k, t), t_range=[-1, 1]).set_stroke(E1, 2.5))
        g.add(ParametricFunction(lambda t, k=k: w(t, k), t_range=[-1, 1]).set_stroke(E2, 2.5))
    return g


def icone_setas(c):
    pl = Plano(c, 0.5)
    return campo(pl, lambda x, y: (-y, x), grade_pts(2.0, 1.0), 0.4, "B1-4 ícone (−y, x)")


class LoteB1(Base):
    def corpo(self):
        # ── B1-1 ──
        self.an("B1-1")
        self.secao("QUE FUNÇÃO É ESSA")
        cA, cB = P3(-3.6, 0.5), P3(3.6, 0.5)
        ic1, ic2 = icone_curva(cA), icone_grafico(cB)
        l1 = F((r"\mathbb{R}", GEO), r"\to", (r"\mathbb{R}^m", SAI), size=M_L).move_to(cA + P3(0, -1.85))
        l2 = F((r"\mathbb{R}^n", GEO), r"\to", (r"\mathbb{R}", SAI), size=M_L).move_to(cB + P3(0, -1.85))
        self.play(run_time=0.4)
        self.gat("uma curva é uma função")
        self.play(Create(ic1[0]), Create(ic1[1]), FadeIn(ic1[2]), run_time=1.4)
        self.play(caneta(l1))
        self.play(MoveAlongPath(ic1[2], ic1[1]), run_time=2.0)
        self.gat("e uma função de várias variáveis")
        self.play(Create(ic2[0]), run_time=0.8)
        self.play(Create(ic2[1]), run_time=1.4)
        self.play(caneta(l2))

        # ── B1-2 ──
        self.an("B1-2")
        cA2, cB2, cC2 = P3(-4.7, 0.2), P3(0.0, 0.2), P3(4.7, 0.2)
        g1, g2 = VGroup(ic1, l1), VGroup(ic2, l2)
        ic3 = icone_vetorial(cC2 + P3(0, 0.35))
        self.gat("agora junta as duas ideias")
        self.play(g1.animate.scale(0.78).move_to(cA2), g2.animate.scale(0.78).move_to(cB2), run_time=0.9)
        self.play(FadeIn(ic3, scale=0.85), run_time=0.7)
        f_ = F("f", ":", ("A", GEO), r"\subset", (r"\mathbb{R}^n", GEO), r"\to", (r"\mathbb{R}^m", SAI), size=M_XL).move_to(P3(0, 2.45))
        self.gat("ela parte de um conjunto")
        self.play(caneta(f_))
        self.gat("repara que as curvas")
        self.play(pulso(ic1, 1.06), pulso(ic2, 1.06), run_time=1.2)
        minis = [F((r"\mathbb{R}^2", GEO), r"\to", (r"\mathbb{R}^2", SAI), size=M_M), F((r"\mathbb{R}^2", GEO), r"\to", (r"\mathbb{R}^3", SAI), size=M_M),
                 F((r"\mathbb{R}^3", GEO), r"\to", (r"\mathbb{R}^3", SAI), size=M_M)]          # v3 §3.4: entrada em GEO, saída em azul-claro
        for m, x in zip(minis, (-3.6, 0.0, 3.6)):
            m.move_to(P3(x, -2.85))
        self.gat("entra um ponto do plano")
        self.play(caneta(minis[0]))
        self.gat("ou do espaço")
        w = self.falta("entra um ponto do espaço")             # v4 §1.3: a terceira começa na sua palavra, com a segunda ainda sendo escrita
        self.play(caneta(minis[1]), caneta(minis[2], atraso=w))
        print(f"[gatilho] B1-2 agendado no play: 'entra um ponto do espaço' a {w:.2f}s do início da caneta anterior (atraso 0,00 s)")
        # v6 §5.4: as funções componentes (cada coordenada da saída é uma função comum)
        comp = F("f", "(", ("X", POS), ")", "=", "(", ("f_1", SAI_F), "(", ("X", POS), ")", ",", r"\ \dots,\ ", ("f_m", SAI_F), "(", ("X", POS), ")", ")", size=M_M).move_to(P3(0, 1.75))
        self.gat("cada coordenada da saída")
        self.play(caneta(comp))

        # ── B1-3 ──
        self.an("B1-3")
        self.limpa(rt=0.4)
        cE, cD = P3(-3.4, -1.4), P3(3.2, -1.4)
        e1 = eixos3(cE, 1.05)
        f = lambda x, y: 0.75 + 0.3 * math.sin(2.4 * x) * math.cos(2.0 * y)
        sup = VGroup(*[ParametricFunction(lambda t, x=x: pj(cE, x, t, f(x, t)), t_range=[0.2, 1.7]).set_stroke(SAI, 2) for x in np.linspace(0.2, 1.4, 6)],
                     *[ParametricFunction(lambda t, y=y: pj(cE, t, y, f(t, y)), t_range=[0.2, 1.4]).set_stroke(SAI, 2) for y in np.linspace(0.2, 1.7, 7)])
        c1 = F(("2", GEO), "+", ("1", SAI), "=", "3", size=M_XL).move_to(cE + P3(0.3, 3.6))
        self.gat("o gráfico é uma superfície")
        self.play(Create(e1[0]), Create(e1[1]), run_time=0.8)
        self.gat("uma para a saída")
        self.play(Create(e1[2]), Create(sup), run_time=1.2)
        self.gat("três no total")
        self.play(caneta(c1))
        e2 = eixos3(cD, 1.05)
        c2 = F(("2", GEO), "+", ("2", SAI), "=", "4", size=M_XL).move_to(cD + P3(0.3, 3.6))
        self.gat("se entram duas coordenadas")
        self.play(Create(e2), run_time=1.0)
        self.play(caneta(c2))
        borda = DashedVMobject(Rectangle(width=5.6, height=4.4).move_to(cD + P3(0.55, 1.05)), num_dashes=60).set_stroke(GEO, 2, 0.8)
        d4 = np.array([0.82, 0.57, 0.0])
        alvo = cD + 3.15 * d4
        quarto = seta(cD, cD + 0.4 * d4, SAI, 3, tip=0.16)
        self.gat("precisaria de quatro eixos")
        self.play(Create(borda), run_time=0.45)
        self.play(Transform(quarto, seta(cD, alvo, SAI, 3, tip=0.16)), run_time=0.95)
        self.gat("não cabe na tela")
        self.play(Wiggle(quarto, scale_value=1.05, rotation_angle=0.06), Flash(alvo, color=SAI_F, line_length=0.18, flash_radius=0.25), run_time=0.9)
        self.play(FadeOut(quarto, shift=-0.4 * d4), run_time=0.7)
        self.remove(quarto)

        # ── B1-4 ──
        self.an("B1-4")
        self.limpa(rt=0.4)
        cards = []
        for x, nome, ic in ((-3.5, "TRANSFORMAÇÃO", icone_malha(P3(-3.5, 0.0))), (3.5, "CAMPO VETORIAL", icone_setas(P3(3.5, 0.0)))):
            r = RoundedRectangle(width=5.4, height=4.6, corner_radius=0.2).move_to(P3(x, -0.4)).set_stroke(GEO, 2, 0.8).set_fill(BG, 0.55)
            t = txt(nome, 32, bold=True).move_to(P3(x, -2.15))
            cards.append(VGroup(r, ic, t))
        self.gat("no primeiro")
        self.play(FadeIn(cards[0][0]), FadeIn(cards[0][2]), Create(cards[0][1]), run_time=1.2)
        self.gat("no segundo")
        self.play(FadeIn(cards[1][0]), FadeIn(cards[1][2]), LaggedStart(*[GrowArrow(s) for s in cards[1][1]], lag_ratio=0.05), run_time=1.3)
        self.gat("são esses dois jeitos")
        self.play(pulso(cards[0][2], 1.05), pulso(cards[1][2], 1.05), run_time=1.0)
        self.sai_fim()
