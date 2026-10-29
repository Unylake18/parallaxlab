"""Lote P4 (handoff v4, lote 2): T4 — como achar o centro de massa de um corpo inteiro?
T4-1 barra uniforme cortada em 4 → 8 → 32 pedaços (pontinho de massa e seta de posição); Σ mᵢ r⃗ᵢ / M → (1/M) ∫ r⃗ dm (Σ → ∫, mᵢ → dm,
sincronizado com Δm → dm no desenho); selo de ligação com a soma de retângulos do vídeo sobre impulso · T4-2 fio, chapa e sólido com o
elemento de massa acendendo · T4-3 barra, disco e esfera com o ⊕ no centro; o anel com o ⊕ no vazio, piscando · T4-4 barra de 2 m do claro
ao escuro (λ = c x): a integral, c e L² cancelam, 2L/3 = 1,33 m; o ⊕ desliza do meio até 1,33 m; DICA."""
from MF_Tools import TransformByGlyphMap

from camadas import *  # noqa: F401,F403


def mp(m, idx, partes):
    return VGroup(*[m[0][j] for k in partes for j in idx[k]])


J = lambda idx, *ks: [j for k in ks for j in idx[k]]


def barra_aco(x0, x1, y, h=0.42, cores=None):
    """Barra 2D de aço com a luz B; `cores`: degradê horizontal (barra de densidade crescente)."""
    r = Rectangle(width=x1 - x0, height=h).move_to(P3((x0 + x1) / 2, y))
    if cores:
        r.set_fill(cores, 1).set_sheen_direction(RIGHT)
    else:
        r.set_fill(["#9AA6B8", "#7A8696", "#3A4252"], 1).set_sheen_direction(UP)
    r.set_stroke("#7FB2FF", 1.8, opacity=0.6)
    r._degrade = "aco"
    return r


class LoteT4(Camadas):
    def construct(self):
        self.setup_base(cap="COMO ACHAR O CENTRO DE MASSA DE UM CORPO INTEIRO?")
        self.t4_1()
        self.t4_2()
        self.t4_3()
        self.t4_4()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    # ── T4-1: de pontos a pedacinhos; Σ → ∫ ───────────────────────────────────────────────────────────────
    def t4_1(self):
        self.an("T4-1")
        X0, X1, Y = -6.6, -0.6, -0.6
        O = P3(X0, Y - 1.35)
        pts = VGroup(*[esfera2d(r).move_to(p) for r, p in ((0.34, P3(-5.6, 0.9)), (0.27, P3(-3.4, 0.2)), (0.27, P3(-4.4, 1.9)))])
        self.play(FadeIn(pts, scale=0.9), run_time=0.7)                                   # "até agora foram pontos"
        bar = barra_aco(X0, X1, Y)
        self.ate(0.15)
        self.play(FadeOut(pts), FadeIn(bar), run_time=0.8)                               # "e um corpo inteiro, uma barra"
        orig = VGroup(Dot(O, radius=0.06, color=GEO), mtex("O", GEO, 36).next_to(O, LEFT, buff=0.12))

        def cortes(n, setas=True):
            g, w = VGroup(), (X1 - X0) / n
            for k in range(1, n):
                g.add(Line(P3(X0 + k * w, Y - 0.21), P3(X0 + k * w, Y + 0.21)).set_stroke(PANEL if n > 16 else "#2A303A", 2 if n < 16 else 1.2))
            for k in range(n):
                c = P3(X0 + (k + 0.5) * w, Y)
                g.add(Dot(c, radius=0.07 if n < 16 else 0.04, color=WHITE_))
                if setas and (n <= 8 or k % 4 == 1):
                    g.add(seta(O + 0.06 * UR, c + 0.08 * DOWN, GEO, 3 if n <= 8 else 2, tip=0.14, op=0.8 if n <= 8 else 0.55))
            return g
        c4, c8, c32 = cortes(4), cortes(8), cortes(32)
        dm4 = VGroup(mtex(r"\Delta m", WHITE_, 40).move_to(P3(X0 + 0.75 * (X1 - X0) / 4 * 1, Y + 0.62)))
        self.ate(0.3)
        self.play(FadeIn(orig), Create(c4), FadeIn(dm4), run_time=1.0)
        S, i_s = eqp(r"\vec R_{cm}", "=", r"\frac{1}{M}", r"\sum_i", r"m_i", r"\vec r_i", size=60, cores={0: CMC, 5: GEO})
        na_conta(S, 1.55)
        self.ate(0.36)
        self.play(FadeIn(S, shift=0.1 * DOWN), run_time=0.8)
        self.ate(0.55)
        self.play(ReplacementTransform(c4, c8), dm4.animate.move_to(P3(X0 + 0.5 * (X1 - X0) / 8 + (X1 - X0) / 8, Y + 0.62)), run_time=0.9)   # "quanto menores"
        dm = mtex(r"dm", WHITE_, 40).move_to(P3(X0 + 1.5 * (X1 - X0) / 32, Y + 0.62))
        self.ate(0.62)
        self.play(ReplacementTransform(c8, c32), ReplacementTransform(dm4, dm), run_time=1.0)                                # Δm → dm
        I, ii = eqp(r"\vec R_{cm}", "=", r"\frac{1}{M}", r"\int", r"\vec r", r"\,dm", size=60, cores={0: CMC, 4: GEO})
        na_conta(I, -0.75)
        self.ate(0.68)
        self.play(TransformByGlyphMap(S.copy(), I, (J(i_s, 0, 1, 2), J(ii, 0, 1, 2)), (J(i_s, 3), J(ii, 3)), (J(i_s, 4), J(ii, 5)), (J(i_s, 5), J(ii, 4))),
                  run_time=1.5)                                                                                       # Σ → ∫, mᵢ → dm
        bx = caixa(I, cor=CMC)
        self.play(FadeIn(bx), run_time=0.5)
        lig = VGroup(txt("COMO NO VÍDEO DO IMPULSO:", 24, color=DIM), txt("A SOMA DE RETÂNGULOS VIRA INTEGRAL", 24, color=DIM)).arrange(DOWN, buff=0.08)
        lig.move_to(P3(PALCO_C[0], -3.3))
        self.ate(0.84)
        self.play(FadeIn(lig), run_time=0.7)
        cm = marcador_cm(P3((X0 + X1) / 2, Y))
        self.ate(0.92)
        self.play(FadeIn(cm, scale=1.4), run_time=0.6)
        self.ate(0.97)

    # ── T4-2: fio, chapa, sólido ────────────────────────────────────────────────────────────────────────────
    def t4_2(self):
        self.an("T4-2")
        velhos = self.snap()
        xs, yi, yf = (-5.1, -0.2, 4.7), 0.7, -1.75
        fio = VMobject().set_points_smoothly([P3(xs[0] + x, yi + 0.6 * math.sin(1.3 * x)) for x in np.linspace(-1.5, 1.5, 30)]).set_stroke("#9AA6B8", 7)
        dl = VMobject().set_points_smoothly([P3(xs[0] + x, yi + 0.6 * math.sin(1.3 * x)) for x in np.linspace(0.15, 0.55, 8)]).set_stroke(CYAN, 10)
        chapa = Rectangle(width=3.0, height=2.0).move_to(P3(xs[1], yi)).set_fill(["#9AA6B8", "#3A4252"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 2, opacity=0.6)
        chapa._degrade = "aco"
        dA = Square(0.36).move_to(P3(xs[1] + 0.45, yi + 0.2)).set_fill(CYAN, 0.85).set_stroke(WHITE_, 1.5)
        d_ = 0.55
        frente = Square(1.9).move_to(P3(xs[2] - 0.25, yi - 0.25))
        cubo = VGroup(Polygon(frente.get_corner(UL), frente.get_corner(UL) + P3(d_, d_), frente.get_corner(UR) + P3(d_, d_), frente.get_corner(UR)),
                      Polygon(frente.get_corner(UR), frente.get_corner(UR) + P3(d_, d_), frente.get_corner(DR) + P3(d_, d_), frente.get_corner(DR)), frente)
        for f_, (a_, b_) in zip(cubo, (("#9AA6B8", "#7A8696"), ("#5A6476", "#3A4252"), ("#9AA6B8", "#3A4252"))):
            f_.set_fill([a_, b_], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 1.8, opacity=0.6)
            f_._degrade = "aco"
        dV = Square(0.34).move_to(frente.get_center() + P3(0.3, 0.25)).set_fill(CYAN, 0.85).set_stroke(WHITE_, 1.5)
        nomes = [txt(s_, 30, bold=True).move_to(P3(x, 2.45)) for s_, x in zip(("FIO", "CHAPA", "SÓLIDO"), xs)]
        eqs = [eqp("dm", "=", c_, d__, size=56, cores={2: GEO})[0].move_to(P3(x, yf)) for c_, d__, x in ((r"\lambda", r"\,d\ell", xs[0]),
                                                                                                       (r"\sigma", r"\,dA", xs[1]), (r"\rho", r"\,dV", xs[2]))]
        self.troca(velhos, FadeIn(fio), FadeIn(chapa), FadeIn(cubo), *[FadeIn(n_) for n_ in nomes], seq=True)
        for k, (el, eq) in enumerate(((dl, eqs[0]), (dA, eqs[1]), (dV, eqs[2]))):
            self.ate((0.25, 0.5, 0.72)[k])
            self.play(FadeIn(el, scale=1.3), Indicate(nomes[k], color=CYAN, scale_factor=1.1), run_time=0.7)
            self.play(TransformFromCopy(el, eq[0][0:2]), FadeIn(eq[0][2:]), run_time=0.9)
        self.ate(0.97)

    # ── T4-3: simetria; o anel ──────────────────────────────────────────────────────────────────────────────
    def t4_3(self):
        self.an("T4-3")
        velhos = self.snap()
        xs, y = (-5.4, -1.9, 1.7, 5.2), 0.2
        bar = barra_aco(xs[0] - 1.25, xs[0] + 1.25, y, h=0.5)
        disco = Circle(radius=1.05).move_to(P3(xs[1], y)).set_fill(["#9AA6B8", "#3A4252"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 2, opacity=0.6)
        disco._degrade = "aco"
        esf = esfera_aco(1.05).move_to(P3(xs[2], y))
        anel = Annulus(inner_radius=0.82, outer_radius=1.05).move_to(P3(xs[3], y)).set_fill(["#9AA6B8", "#3A4252"], 1).set_sheen_direction(UP) \
            .set_stroke("#7FB2FF", 2, opacity=0.6)
        anel._degrade = "aco"
        eixos = VGroup(*[VGroup(DashedLine(P3(x, y - 1.35), P3(x, y + 1.35), dash_length=0.09), DashedLine(P3(x - 1.45, y), P3(x + 1.45, y), dash_length=0.09))
                         .set_stroke(WHITE_, 1.6, opacity=0.55) for x in xs[:3]])
        cms = [marcador_cm(P3(x, y)) for x in xs]
        self.troca(velhos, FadeIn(bar), FadeIn(disco), FadeIn(esf), seq=True)
        self.ate(0.22)
        self.play(Create(eixos), run_time=0.8)                                              # "por simetria"
        self.ate(0.36)
        self.play(*[FadeIn(c_, scale=1.4) for c_ in cms[:3]], run_time=0.7)                 # "está no centro"
        self.ate(0.55)
        self.play(FadeIn(anel), run_time=0.7)                                                # "e olha o anel"
        ea = VGroup(DashedLine(P3(xs[3], y - 1.35), P3(xs[3], y + 1.35), dash_length=0.09),
                    DashedLine(P3(xs[3] - 1.45, y), P3(xs[3] + 1.45, y), dash_length=0.09)).set_stroke(WHITE_, 1.6, opacity=0.55)
        self.ate(0.68)
        self.play(Create(ea), FadeIn(cms[3], scale=1.4), run_time=0.8)
        self.play(onda(P3(xs[3], y)), Indicate(cms[3], color=WHITE_, scale_factor=1.3), run_time=0.9)   # no vazio, piscando
        fora = txt("O CENTRO DE MASSA PODE FICAR FORA DO MATERIAL", 32, bold=True).move_to(P3(0, -2.6))
        self.ate(0.84)
        self.play(FadeIn(fora, shift=0.1 * UP), run_time=0.7)
        self.play(onda(P3(xs[3], y)), run_time=0.9)
        self.ate(0.97)

    # ── T4-4: barra de densidade crescente ──────────────────────────────────────────────────────────────────
    def t4_4(self):
        self.an("T4-4")
        velhos = self.snap()
        X0, L_, Y = -6.6, 5.6, -0.2                                        # 2 m → 5,6 de tela
        px = lambda x: X0 + L_ * x / 2
        bar = barra_aco(X0, X0 + L_, Y, h=0.6, cores=["#C9D2DE", "#7A8696", "#262C38"])
        eixo = VGroup(Line(P3(X0, Y - 0.75), P3(X0 + L_ + 0.3, Y - 0.75)).set_stroke(GEO, 2.2))
        for xm in (0, 1, 2):
            eixo.add(Line(P3(px(xm), Y - 0.85), P3(px(xm), Y - 0.65)).set_stroke(GEO, 2.2), rot(str(xm), 30, GEO).next_to(P3(px(xm), Y - 0.85), DOWN, buff=0.12))
        eixo.add(VGroup(mtex("x", GEO, 36), rot("(m)", 30, GEO)).arrange(RIGHT, buff=0.08).next_to(P3(X0 + L_ + 0.3, Y - 0.75), RIGHT, buff=0.12))
        lam = VGroup(eqp(r"\lambda", "=", "c", "x", size=48, cores={0: GEO, 3: GEO})[0]).next_to(bar, UP, buff=0.4)
        xcm = ValueTracker(1.0)
        self.add(xcm)
        cmv = vivo(lambda: VGroup(marcador_cm(P3(px(xcm.get_value()), Y)),
                                  DashedLine(P3(px(xcm.get_value()), Y - 0.35), P3(px(xcm.get_value()), Y - 0.75), dash_length=0.07).set_stroke(WHITE_, 1.6, opacity=0.7)))
        self.troca(velhos, FadeIn(bar), FadeIn(eixo), seq=True)
        self.ate(0.12)
        self.play(FadeIn(lam, shift=0.1 * DOWN), FadeIn(cmv), run_time=0.8)               # "mais densa de uma ponta para a outra"
        E1 = MathTex(r"X=\frac{\int_0^L x\cdot c x\,dx}{\int_0^L c x\,dx}", font_size=52, color=WHITE_)
        E1[0][0].set_color(CMC)
        E1._partes = [("X", CMC)]
        E2 = MathTex(r"=\frac{c L^3/3}{c L^2/2}", font_size=52, color=WHITE_)
        E3, i3 = eqp("=", r"\frac{2L}{3}", "=", r"\frac{2\cdot 2}{3}", r"=\ ", r"1{,}33\ \mathrm{m}", size=52, cores={5: CMC})
        na_conta(E1, 1.75)
        E2.move_to(P3(XC0 + 0.55 + E2.width / 2, 0.15))
        E3.move_to(P3(XC0 + 0.2 + E3.width / 2, -1.3))
        self.ate(0.3)
        self.play(FadeIn(E1), run_time=0.9)
        self.ate(0.44)
        self.play(FadeIn(E2, shift=0.1 * DOWN), run_time=0.8)
        # c e L² cancelam (glifos achados pela posição: numerador acima da barra da fração)
        g2 = list(E2[0])
        barra_y = [m.get_y() for m in g2 if m.width > 1.0][0]
        num = [m for m in g2[1:] if m.get_y() > barra_y + 0.05]
        den = [m for m in g2[1:] if m.get_y() < barra_y - 0.05]
        cort = VGroup(risco(num[0], WHITE_, 3), risco(den[0], WHITE_, 3), risco(num[2], WHITE_, 3), risco(VGroup(den[1], den[2]), WHITE_, 3))   # L³/L² = L: risca o ³ e o L² inteiro
        self.ate(0.52)
        self.play(Create(cort[:2]), run_time=0.6)                                         # c cancela
        self.play(Create(cort[2:]), run_time=0.6)                                         # L² cancela (sobra um L em cima)
        self.ate(0.6)
        self.play(FadeIn(mp(E3, i3, [0, 1])), run_time=0.8)
        self.ate(0.66)
        self.play(FadeIn(mp(E3, i3, [2, 3, 4, 5])), xcm.animate.set_value(4 / 3), run_time=1.6)     # o ⊕ desliza do meio até 1,33 m
        bx = caixa(mp(E3, i3, [5]), cor=CMC)
        cota_ = VGroup(Line(P3(px(4 / 3), Y - 0.85), P3(px(4 / 3), Y - 0.65)).set_stroke(WHITE_, 2.4), rot("1,33", 30).next_to(P3(px(4 / 3), Y - 0.85), DOWN, buff=0.12))
        self.play(FadeIn(bx), FadeIn(cota_), run_time=0.6)
        self.ate(0.8)
        self.dica_entra(dica("SIMETRIA PRIMEIRO. INTEGRAL SÓ PARA", "O QUE A SIMETRIA NÃO DIZ"))
        self.ate(0.97)
