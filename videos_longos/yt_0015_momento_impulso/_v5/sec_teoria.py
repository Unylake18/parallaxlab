"""Lote PC (v4): T4 — da conservação à terceira lei (discos em loop, Δp⃗ saindo do contato, cronômetro encolhendo Δt).
v3: grade de layout (PALCO + CONTA, CENTRO, LEGENDA), equações por Write/TransformByGlyphMap, realces nas pausas."""
from MF_Tools import TransformByGlyphMap

from kit import *  # noqa: F401,F403


def tex(s, cor=WHITE_, size=M_MID):
    return MathTex(s, font_size=size, color=cor)


def foguete(esc=1.0):
    k = esc
    corpo = RoundedRectangle(corner_radius=0.25 * k, width=0.6 * k, height=1.6 * k).set_stroke(mix(STEEL, 0.5), 2).set_fill(STEEL, 1.0)
    nariz = Triangle().set_stroke(mix(STEEL, 0.5), 2).set_fill(GEO, 1.0).scale(0.3 * k).next_to(corpo, UP, buff=-0.02)
    a1 = Polygon(P3(-0.3, -0.8), P3(-0.62, -1.1), P3(-0.3, -0.35)).scale(k, about_point=ORIGIN).set_stroke(mix(STEEL, 0.5), 2).set_fill(STEEL, 1.0)
    a2 = a1.copy().flip(UP, about_point=ORIGIN)
    return VGroup(a1, a2, corpo, nariz)


def disco(cor, num, r=0.55):
    c = Circle(radius=r).set_stroke(mix(cor, 0.5), 2.5).set_fill(cor, 1)
    n = MathTex(num, font_size=36, color=BACKGROUND_COLOR if cor == GEO else WHITE_)
    return VGroup(c, n).set_z_index(5)


def relogio(c, r, frac):
    """Cronômetro da colisão: mostrador, setor do intervalo Δt (fração da volta, ValueTracker) e ponteiro."""
    c = np.asarray(c, float)
    base = VGroup(Circle(radius=r).set_stroke(GEO, 2.5).set_fill(PANEL, 0.9).move_to(c),
                  RoundedRectangle(corner_radius=0.04, width=0.22, height=0.16).set_stroke(GEO, 2).set_fill(STEEL, 1).move_to(c + P3(0, r + 0.1)))
    for k in range(12):
        a = PI / 2 - k * TAU / 12
        base.add(Line(c + 0.82 * r * P3(math.cos(a), math.sin(a)), c + 0.95 * r * P3(math.cos(a), math.sin(a))).set_stroke(DIM, 1.5))

    def setor():
        f = max(frac.get_value(), 0.004)
        s = Sector(radius=0.8 * r, angle=-TAU * f, start_angle=PI / 2, arc_center=c).set_stroke(width=0).set_fill(JC, 0.55)
        a = PI / 2 - TAU * f
        return VGroup(s, Line(c, c + 0.8 * r * P3(math.cos(a), math.sin(a))).set_stroke(WHITE_, 3), Dot(c, radius=0.05, color=WHITE_))
    return VGroup(base, always_redraw(setor))


class LoteTeoria(Base):
    def construct(self):
        self.setup_base(cap="DA CONSERVAÇÃO À TERCEIRA LEI")
        self.t3()
        self.fim()
        self.relatorio()

    def loop_discos(self, y, per=4.2):
        """Experiência 2 em loop (no relógio da cena): o disco 1 chega, para; o 2 sai com a mesma velocidade."""
        d1, d2 = opac_rel(disco(GEO, "1"), 1.0), opac_rel(disco(STEEL, "2"), 1.0)
        t0 = self.clk.get_value()
        vel = 1.45

        def est():
            t = (self.clk.get_value() - t0) % per
            tc = 1.4
            x1 = -0.57 - vel * max(0.0, tc - t)
            x2 = 0.57 + vel * max(0.0, t - tc)
            op = min(1.0, t / 0.3, (per - t) / 0.3)
            return x1, x2, op
        d1.add_updater(lambda m: opac_rel(m.move_to(P3(est()[0], y)), est()[2]))
        d2.add_updater(lambda m: opac_rel(m.move_to(P3(est()[1], y)), est()[2]))
        return d1, d2

    # ── T3 ──────────────────────────────────────────────────────────────────────────────────────────────────
    def t3(self):
        self.an("T4-1")
        y = 1.75
        pista = placa(10.4, 2.2, P3(0, 1.5))
        d1, d2 = self.loop_discos(y)
        yd = 0.8
        cont = Dot(P3(0, yd), radius=0.07, color=WHITE_).set_z_index(9)
        lc = DashedLine(P3(0, y - 0.55), P3(0, yd), dash_length=0.06).set_stroke(DIM, 1.4, opacity=0.8)      # do ponto de contato
        dp1 = arrow(P3(0, yd), P3(-2.6, yd), color=MAG, width=8)
        dp2 = arrow(P3(0, yd), P3(2.6, yd), color=MAG, width=8)
        l1 = tex(r"\Delta\vec p_1", MAG, 44).next_to(dp1, LEFT, buff=0.14)
        l2 = tex(r"\Delta\vec p_2", MAG, 44).next_to(dp2, RIGHT, buff=0.14)
        e1 = centro(MathTex(r"\Delta\vec p_1=-\Delta\vec p_2", font_size=80), -1.45)
        self.colore(e1[0], [0, 1, 2, 3, 6, 7, 8, 9], MAG)
        frase = legenda("O QUE UM GANHA, O OUTRO PERDE")
        self.play(FadeIn(pista), FadeIn(d1), FadeIn(d2), run_time=0.7)
        self.ate(0.3)
        self.play(FadeIn(cont), FadeIn(lc), GrowArrow(dp1), GrowArrow(dp2), run_time=0.9)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.4)
        self.lc, self.cont = lc, cont
        self.ate(0.55)
        self.play(FadeIn(frase), run_time=0.5)
        self.ate(0.6)
        self.play(ReplacementTransform(fixa(l1), VGroup(*e1[0][0:4])), ReplacementTransform(fixa(l2), VGroup(*e1[0][6:10])),
                  FadeIn(VGroup(e1[0][4], e1[0][5])), run_time=1.1)
        self.add(e1)
        self.ate(0.97)
        # T4-2 — ÷Δt (o Δt entra embaixo dos dois lados) e Δt → 0; o cronômetro da colisão encolhe ----------------------
        self.an("T4-2")
        fr = ValueTracker(0.35)
        rel = relogio(P3(5.4, -0.55), 0.62, fr)
        lrel = MathTex(r"\Delta t", font_size=40, color=JC).next_to(rel, DOWN, buff=0.15)
        self.play(FadeOut(self.lc), FadeIn(rel), FadeIn(lrel), run_time=0.6)
        tag = MathTex(r"\div\,\Delta t", font_size=52, color=JC).next_to(e1, RIGHT, buff=0.6)
        self.play(FadeOut(frase), ReplacementTransform(fixa(lrel), tag), run_time=0.6)
        e2 = centro(MathTex(r"\frac{\Delta\vec p_1}{\Delta t}=-\frac{\Delta\vec p_2}{\Delta t}", font_size=80), -1.45)
        self.colore(e2[0], [0, 1, 2, 3, 9, 10, 11, 12], MAG)
        self.ate(0.2)
        self.play(TransformByGlyphMap(e1, e2, ([0, 1, 2, 3], [0, 1, 2, 3]), ([4], [7]), ([5], [8]), ([6, 7, 8, 9], [9, 10, 11, 12]),
                                      ([], [4, 13]), ([], [5, 6, 14, 15], {"shift": 0.5 * UP})),
                  FadeOut(tag, shift=0.5 * LEFT), run_time=1.4)
        lim = MathTex(r"\Delta t\to 0", font_size=48, color=JC).move_to(P3(0, LEGENDA_Y))
        self.ate(0.45)
        self.play(Write(lim), fr.animate.set_value(0.02), run_time=2.0)
        e3 = centro(MathTex(r"\frac{d\vec p_1}{dt}=-\frac{d\vec p_2}{dt}", font_size=80), -1.45)
        self.colore(e3[0], [0, 1, 2, 3, 9, 10, 11, 12], MAG)
        self.ate(0.62)
        self.play(TransformByGlyphMap(e2, e3, ([0], [0]), ([5], [5]), ([9], [9]), ([14], [14])), run_time=1.3)
        taxa = legenda("TAXA DE VARIAÇÃO DO MOMENTO")
        self.play(FadeOut(lim), FadeIn(taxa), run_time=0.5)
        self.ate(0.97)
        # T4-3 — a taxa é a força: F₁₍₂₎ = −F₂₍₁₎ -------------------------------------------------------------------
        self.an("T4-3")
        e4 = centro(MathTex(r"\vec F_{1(2)}=-\vec F_{2(1)}", font_size=84), -1.45)
        fx = faixas(r"\vec F_{1(2)}", "=", "-", r"\vec F_{2(1)}")
        self.colore(e4[0], fx[0] + fx[3], FC)
        self.ate(0.25)
        self.play(FadeOut(rel), FadeOut(lrel), run_time=0.4)
        self.play(TransformByGlyphMap(e3, e4, ([0, 1, 2, 3, 4, 5, 6], fx[0]), ([7], fx[1]), ([8], fx[2]),
                                      ([9, 10, 11, 12, 13, 14, 15], fx[3])), FadeOut(taxa), run_time=1.4)
        f1 = arrow(P3(0, yd), P3(-2.6, yd), color=FC, width=9)
        f2 = arrow(P3(0, yd), P3(2.6, yd), color=FC, width=9)
        lf1 = tex(r"\vec F_{1(2)}", FC, 44).next_to(f1, LEFT, buff=0.14)
        lf2 = tex(r"\vec F_{2(1)}", FC, 44).next_to(f2, RIGHT, buff=0.14)
        self.play(ReplacementTransform(dp1, f1), ReplacementTransform(dp2, f2), ReplacementTransform(l1, lf1), ReplacementTransform(l2, lf2),
                  run_time=1.0)
        lei = legenda("TERCEIRA LEI DE NEWTON", T_MAIN, color=WHITE_)
        cx = SurroundingRectangle(e4, color=FC, buff=0.25, stroke_width=2.5, corner_radius=0.1)
        self.ate(0.6)
        self.play(FadeIn(lei, shift=0.1 * UP), Create(cx), run_time=0.9)
        self.play(Indicate(e4, color=WHITE_, scale_factor=1.05), run_time=0.8)
        self.ate(0.97)
        # T4-4 — ação e reação em corpos diferentes: PALCO mesa + bloco; Terra à direita -------------------------------
        self.an("T4-4")
        self.clear(rt=0.5)
        aco = lambda m: m.set_stroke(GEO, 2.5).set_fill(STEEL, 1)
        tampo = aco(Rectangle(width=4.8, height=0.24)).move_to(P3(-3.4, -0.7))
        pern = VGroup(*[aco(Rectangle(width=0.24, height=2.1)).move_to(P3(x, -1.93)) for x in (-5.4, -1.4)])
        blk = Corpo("", STEEL, 1.5, 1.1).at(-3.4, -0.58)
        blk.front.set_stroke(GEO, 2.5)
        cb = blk.get_center()
        P_ = arrow(cb, cb + P3(0, -1.6), color=FC, width=8)
        N_ = arrow(cb, cb + P3(0, 1.6), color=FC, width=8)
        lP = tex(r"\vec P", FC, 46).next_to(P_.get_end(), RIGHT, buff=0.2)
        lN = tex(r"\vec N", FC, 46).next_to(N_.get_end(), RIGHT, buff=0.2)
        nb = linha(txt("AS DUAS NO", T_SMALL, color=GEO), txt("BLOCO", T_SMALL, color=GEO), buff=0.12).next_to(N_.get_end(), LEFT, buff=0.35)
        terra = Circle(radius=1.9).set_stroke(GEO, 2.5).set_fill(PANEL, 1).move_to(P3(3.7, -0.8))
        tl = txt("TERRA", T_SMALL, color=GEO).next_to(terra, DOWN, buff=0.2)
        esc = txt("FORA DE ESCALA", 18, color=DIM).next_to(terra, UP, buff=0.2)
        cen = Dot(terra.get_center(), radius=0.08, color=WHITE_).set_z_index(6)
        R_ = arrow(terra.get_center(), terra.get_center() + P3(0, 1.6), color=FC, width=8, tip=0.24)
        lR = tex(r"-\vec P", FC, 44).move_to(P3(6.15, 1.25))
        lr2 = txt("REAÇÃO DO PESO", T_SMALL, color=FC).move_to(P3(6.15, 0.75))
        fio_t = Line(P3(5.6, 1.0), terra.get_center() + P3(0.08, 0.85)).set_stroke(FC, 1.2, opacity=0.7)
        frase = legenda("AÇÃO E REAÇÃO AGEM EM CORPOS DIFERENTES", T_MAIN, color=WHITE_)
        self.play(Create(tampo), Create(pern), run_time=0.7)
        self.play(FadeIn(blk, shift=0.3 * DOWN), run_time=0.5)
        self.play(FadeIn(frase, shift=0.1 * UP), run_time=0.7)
        self.ate(0.35)
        self.play(GrowArrow(P_), run_time=0.6)
        self.play(FadeIn(lP), GrowArrow(N_), run_time=0.6)
        self.play(FadeIn(lN), FadeIn(nb), run_time=0.5)
        self.ate(0.68)
        self.play(FadeIn(terra), FadeIn(cen), FadeIn(tl), FadeIn(esc), run_time=0.7)
        self.play(GrowArrow(R_), run_time=0.7)
        self.play(FadeIn(lR), FadeIn(lr2), Create(fio_t), Indicate(VGroup(P_, R_), color=WHITE_, scale_factor=1.06), run_time=0.9)
        self.ate(0.97)
        # T4-5 — cargas: PALCO (cargas, v violeta, F azul, nuvem); CONTA a desigualdade; LEGENDA o momento do campo -------
        self.an("T4-5")
        self.clear(rt=0.5)
        q1c, q2c = P3(-4.6, -1.2), P3(-1.6, 1.0)
        nuvem = VGroup(*[Ellipse(width=3.6 + 1.1 * k, height=2.3 + 0.7 * k).set_stroke(DIM, 1.6, opacity=0.36 - 0.045 * k)
                         .move_to((q1c + q2c) / 2).rotate(0.6) for k in range(6)])
        cargas = VGroup(*[VGroup(Circle(radius=0.36).set_stroke(GEO, 2).set_fill(GEO, 1).move_to(c),
                                 MathTex("+", font_size=44, color=BACKGROUND_COLOR).move_to(c)).set_z_index(6) for c in (q1c, q2c)])
        v1 = arrow(q1c + P3(0.42, 0), q1c + P3(2.0, 0), color=VEL, width=7)
        v2 = arrow(q2c + P3(0, 0.42), q2c + P3(0, 1.6), color=VEL, width=7)
        lv1 = tex(r"\vec v_1", VEL, 38).next_to(v1, DOWN, buff=0.15)
        lv2 = tex(r"\vec v_2", VEL, 38).next_to(v2, LEFT, buff=0.15)
        F1 = arrow(q1c + P3(-0.3, 0.3), q1c + P3(-1.3, 1.3), color=FC, width=8)
        F2 = arrow(q2c + P3(0.42, 0.0), q2c + P3(2.0, 0.0), color=FC, width=8)
        lF1 = tex(r"\vec F_{1(2)}", FC, 40).next_to(F1.get_end(), UP, buff=0.15)
        lF2 = tex(r"\vec F_{2(1)}", FC, 40).next_to(F2.get_end(), DOWN, buff=0.2)
        neq = tex(r"\vec F_{1(2)}\neq-\vec F_{2(1)}", FC, 52)
        nq2 = txt("ENTRE CARGAS EM MOVIMENTO", T_SMALL, color=DIM)
        conta(neq, nq2, topo=1.3, buff=0.35)
        caixa_t = txt("MOMENTO DAS PARTÍCULAS + MOMENTO DO CAMPO = CONSTANTE", 28, bold=True)
        caixa = VGroup(RoundedRectangle(corner_radius=0.12, width=caixa_t.width + 0.7, height=caixa_t.height + 0.45)
                       .set_stroke(MAG, 2).set_fill(BACKGROUND_COLOR, 0.92), caixa_t).set_z_index(20)
        caixa_t.move_to(caixa[0])
        centro(caixa, LEGENDA_Y)
        self.play(FadeIn(cargas, scale=0.8), run_time=0.6)
        self.play(GrowArrow(v1), GrowArrow(v2), run_time=0.7)
        self.play(FadeIn(lv1), FadeIn(lv2), FadeIn(nq2), run_time=0.5)
        self.ate(0.2)
        self.play(GrowArrow(F1), GrowArrow(F2), run_time=0.8)
        self.play(FadeIn(lF1), FadeIn(lF2), run_time=0.4)
        self.play(Write(neq), run_time=0.9)
        self.ate(0.52)
        self.play(LaggedStart(*[Create(e) for e in nuvem], lag_ratio=0.15), run_time=1.6)
        self.ate(0.66)
        self.play(FadeIn(caixa, shift=0.1 * UP), run_time=0.8)
        self.play(Indicate(caixa_t, color=MAG, scale_factor=1.04), run_time=0.9)
        self.ate(0.97)

    def colore(self, glifos, idx, cor):
        for i in idx:
            glifos[i].set_color(cor)
