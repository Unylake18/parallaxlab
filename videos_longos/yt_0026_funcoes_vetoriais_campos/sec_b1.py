"""Lote PB1 · QUE FUNÇÃO É ESSA (B1-1…B1-4), layout C (quadro 10): três cartões (curva, gráfico, campo) sob f : A ⊂ ℝⁿ → ℝᵐ; as funções componentes;
a contagem de eixos (2 + 1 = 3 cabe; 2 + 2 = 4, o quarto eixo bate na borda e some); os dois painéis TRANSFORMAÇÃO e CAMPO VETORIAL."""
from v7 import *  # noqa: F401,F403

GIRO = lambda x, y: (-y, x)
EX, EY, EZ = np.array([-0.55, -0.42, 0.0]), np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])
XS = (140, 720, 1300)


def pj(c, x, y, z, s=1.0):
    return c + s * (x * EX + y * EY + z * EZ)


def eixos3(c, s=1.0):
    return VGroup(eixo_seta(c, c + s * 1.9 * EX), eixo_seta(c, c + s * 1.9 * EY), seta(c, c + s * 1.9 * EZ, SAI, 3, tip=0.16))


def icone_malha(c):
    g = VGroup()

    def w(x, y):
        return c + P3(x + 0.18 * math.sin(2.2 * y), y + 0.18 * math.sin(2.2 * x))
    for k in np.linspace(-1, 1, 5):
        g.add(ParametricFunction(lambda t, k=k: w(k, t), t_range=[-1, 1]).set_stroke(E1, 2.5))
        g.add(ParametricFunction(lambda t, k=k: w(t, k), t_range=[-1, 1]).set_stroke(E2, 2.5))
    return g


class LoteB1(Base):
    def corpo(self):
        seg = {}
        self.an("B1-1")
        self.secao("QUE FUNÇÃO É ESSA")
        # cartão 1: a curva ℝ → ℝ²
        c1 = painel(XS[0], 400, 480, 420)
        v1 = Vista(380, 620, 70)
        ex1 = eixos7(v1, -2.6, 2.6, -2.2, 2.2, alpha=0.5)
        cv = [v1.c2p(2.1 * math.sin(t), 1.4 * math.sin(2 * t)) for t in np.linspace(-PI, PI, 101)]
        curva = linha7(cv, POS7, 5)
        contorno(curva)
        dcur = ponto7(v1.c2p(2.1 * math.sin(0.9), 1.4 * math.sin(1.8)), POS7, 9)
        t1 = TC(r"\mathbb{R}\to\mathbb{R}^2", XS[0] + 240, 880, 44, "c")
        r1 = legenda("CURVA", XS[0] + 240, 950, GEO, "center")
        # cartão 2: o gráfico ℝ² → ℝ (a tigela do 3D)
        c2 = painel(XS[1], 400, 480, 420)
        BOXG = [740, 420, 440, 380]
        grf = Fundo3D(self, "c7_paraboloide", lambda t: {"s": 1.0, "box": BOXG}, op=0.0)
        t2 = TC(r"\mathbb{R}^2\to\mathbb{R}", XS[1] + 240, 880, 44, "c")
        r2 = legenda("GRÁFICO", XS[1] + 240, 950, GEO, "center")
        self.add(grf)
        self.gat("uma curva é uma função")
        self.play(FadeIn(c1), Create(ex1), run_time=0.7)
        self.play(Create(curva), FadeIn(dcur), run_time=1.2)
        self.play(caneta(t1), FadeIn(r1))
        self.play(MoveAlongPath(dcur, curva), run_time=2.0)
        self.gat("e uma função de várias variáveis")
        self.play(FadeIn(c2), grf.op.animate.set_value(1.0), run_time=1.0)
        self.play(caneta(t2), FadeIn(r2))

        # ── B1-2 · a definição, o terceiro cartão e as funções componentes ──
        self.an("B1-2")
        fdef = TC(r"f : {\G A} \subset \mathbb{R}^n \to \mathbb{R}^m", 960, 280, 64, "c")
        c3 = painel(XS[2], 400, 480, 420)
        borda3 = contorno_painel(XS[2], 400, 480, 420, CAMPO, 3)
        v3 = Vista(1540, 600, 52)
        g3 = campo7(v3, GIRO, -3, 3, -3, 3, passo=1.0, rmin=0.5, mmax=4.3, lmax=0.7, nome="B1 cartão campo")
        t3 = TC(r"\mathbb{R}^2\to\mathbb{R}^2", XS[2] + 240, 880, 44, "c")
        r3 = legenda("NESTE VÍDEO", XS[2] + 240, 950, CAMPO2, "center")
        self.gat("agora junta as duas ideias")
        self.play(FadeIn(c3), Create(borda3), run_time=0.7)
        self.play(LaggedStart(*[GrowArrow(s_) for s_ in g3], lag_ratio=0.04), run_time=1.0)
        self.gat("ela parte de um conjunto")
        self.play(caneta(fdef))
        self.play(caneta(t3), FadeIn(r3), run_time=1.2)
        self.gat("repara que as curvas")
        self.play(pulso(t1, 1.06), pulso(t2, 1.06), run_time=1.0)
        comp = TC(r"f(X) = (f_1(X),\ \dots,\ f_m(X))", 960, 352, 38, "c")
        self.gat("cada coordenada da saída")
        self.play(caneta(comp))

        # ── B1-3 · contagem de eixos ──
        self.an("B1-3")
        self.limpa(rt=0.4)
        cE, cD = P3(-3.4, -1.4), P3(3.2, -1.4)
        e1 = eixos3(cE, 1.05)
        f = lambda x, y: 0.75 + 0.3 * math.sin(2.4 * x) * math.cos(2.0 * y)
        sup = VGroup(*[ParametricFunction(lambda t, x=x: pj(cE, x, t, f(x, t)), t_range=[0.2, 1.7]).set_stroke(SAI, 2) for x in np.linspace(0.2, 1.4, 6)],
                     *[ParametricFunction(lambda t, y=y: pj(cE, t, y, f(t, y)), t_range=[0.2, 1.4]).set_stroke(SAI, 2) for y in np.linspace(0.2, 1.7, 7)])
        k1 = F(("2", GEO), "+", ("1", SAI), "=", "3", size=M_XL).move_to(cE + P3(0.3, 3.2))
        self.gat("o gráfico é uma superfície")
        self.play(Create(e1[0]), Create(e1[1]), run_time=0.8)
        self.gat("uma para a saída")
        self.play(Create(e1[2]), Create(sup), run_time=1.2)
        self.gat("três no total")
        self.play(caneta(k1))
        e2 = eixos3(cD, 1.05)
        k2 = F(("2", GEO), "+", ("2", SAI), "=", "4", size=M_XL).move_to(cD + P3(0.3, 3.2))
        self.gat("se entram duas coordenadas")
        self.play(Create(e2), run_time=1.0)
        self.play(caneta(k2))
        borda = DashedVMobject(Rectangle(width=5.6, height=4.4).move_to(cD + P3(0.55, 0.85)), num_dashes=60).set_stroke(GEO, 2, 0.8)
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

        # ── B1-4 · os dois jeitos de desenhar ──
        self.an("B1-4")
        self.limpa(rt=0.4)
        pa, pb = painel(150, 260, 740, 560, "TRANSFORMAÇÃO", WHITE_), painel(1030, 260, 740, 560, "CAMPO VETORIAL", CAMPO2)
        mal = icone_malha(PX(520, 540)).scale(1.5, about_point=PX(520, 540))
        vb = Vista(1400, 540, 70)
        gb = campo7(vb, GIRO, -3, 3, -3, 3, passo=0.75, rmin=0.5, rmax=3.3, mmax=3.3, lmax=0.6, nome="B1-4 campo")
        self.gat("no primeiro")
        self.play(FadeIn(pa), Create(mal), run_time=1.2)
        self.gat("no segundo")
        self.play(FadeIn(pb), LaggedStart(*[GrowArrow(s_) for s_ in gb], lag_ratio=0.02), run_time=1.3)
        self.gat("são esses dois jeitos")
        self.play(pulso(pa[1], 1.05), pulso(pb[1], 1.05), run_time=1.0)
        self.sai_fim()
