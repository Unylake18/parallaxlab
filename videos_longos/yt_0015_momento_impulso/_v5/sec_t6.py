"""Lote PF: T6 — momento ou energia? v4: as mãos/bolas e os barcos ficam no PALCO enquanto K = p²/(2m) se constrói na CONTA. v3: DOIS PAINÉIS que entram com o conteúdo; K = p²/(2m) no CENTRO por
substituição; mãos abertas de perfil recebendo as bolas na palma (recuo d e 5d); barcos opacos em raias de gelo, F⃗ na popa,
m/2m acima do barco, setas p e √2 p na CONTA; DICA."""
from MF_Tools import TransformByGlyphMap

from kit import *  # noqa: F401,F403


def tex(s, cor=WHITE_, size=M_MID):
    return MathTex(s, font_size=size, color=cor)


def mao(esc=1.0):
    """Luva de beisebol de perfil (v5): forma única preenchida, concha aberta para a esquerda, sem antebraço; costuras claras no dorso.
    `palma_x` = x do fundo da concha (onde a bola encosta) em relação ao centro da luva."""
    k = esc
    pts = [(-0.38, 0.78), (-0.08, 0.98), (0.32, 0.93), (0.6, 0.6), (0.7, 0.0), (0.62, -0.55), (0.36, -0.88), (0.0, -0.94),
           (-0.32, -0.74), (-0.18, -0.46), (0.02, -0.22), (0.1, 0.0), (0.02, 0.22), (-0.14, 0.46), (-0.38, 0.78)]
    corpo = VMobject().set_points_smoothly([P3(x * k, y * k) for x, y in pts]).set_stroke(GEO, 2.2).set_fill([GEO, STEEL], 1.0)
    corpo.set_sheen_direction(LEFT)
    costura = VGroup(*[Line(P3(x0 * k, y0 * k), P3(x1 * k, y1 * k)).set_stroke(mix(GEO, 0.5), 1.6, opacity=0.8)
                       for (x0, y0), (x1, y1) in (((0.42, 0.55), (0.5, 0.42)), ((0.52, 0.2), (0.6, 0.1)), ((0.52, -0.15), (0.6, -0.25)),
                                                  ((0.42, -0.48), (0.5, -0.6)))])
    tira = Line(P3(0.28 * k, -0.8 * k), P3(0.62 * k, -0.42 * k)).set_stroke(BACKGROUND_COLOR, 3, opacity=0.6)
    concha = VMobject().set_points_smoothly([P3(x * k, y * k) for x, y in ((-0.3, 0.74), (-0.08, 0.5), (0.1, 0.2), (0.14, 0.0), (0.1, -0.2),
                                                                           (-0.08, -0.44), (-0.26, -0.7))]).set_stroke(STEEL, 5, opacity=0.9)
    dedos = VGroup(*[Arc(radius=r_ * k, start_angle=-0.9, angle=1.8, arc_center=P3(-0.05 * k, y_ * k)).set_stroke(mix(GEO, 0.3), 1.6, opacity=0.6)
                     for r_, y_ in ((0.62, 0.18), (0.5, 0.18), (0.38, 0.18))])
    costura.add(concha, dedos)
    fundo = Dot(P3(0.1 * k, 0.0), radius=0.001).set_opacity(0)
    g = VGroup(corpo, costura, fundo, tira)
    g.palma_x = 0.1 * k - g.get_center()[0]
    return g


def barco(esc=1.0):
    k = esc
    casco = Polygon(P3(-0.9, 0), P3(0.95, 0), P3(0.7, -0.28), P3(-0.75, -0.28)).scale(k, about_point=ORIGIN) \
        .set_stroke(GEO, 2).set_fill(STEEL, 1)
    mastro = Rectangle(width=0.07 * k, height=1.5 * k).set_stroke(width=0).set_fill(GEO, 1).move_to(P3(0.0, 0.75 * k))
    vela = Polygon(P3(0.05, 1.45), P3(0.05, 0.12), P3(0.85, 0.12)).scale(k, about_point=ORIGIN).set_stroke(GEO, 1.5).set_fill("#C9D2E2", 1)
    patins = VGroup(*[RoundedRectangle(corner_radius=0.03 * k, width=0.5 * k, height=0.07 * k).set_stroke(width=0).set_fill(GEO, 1)
                      .move_to(P3(x * k, -0.36 * k)) for x in (-0.5, 0.55)])
    return VGroup(patins, casco, mastro, vela)


class LoteT6(Base):
    def construct(self):
        self.setup_base(cap="MOMENTO OU ENERGIA?", selo="IMPULSO × TRABALHO")
        self.t6_1()
        self.t6_2()
        self.t6_3()
        self.t6_4()
        self.t6_5()
        self.fim()
        self.relatorio()

    # ── T6-1 · a mesma força em cima; DOIS PAINÉIS (tempo → impulso → Δp; distância → trabalho → ΔK) ─────────────
    def t6_1(self):
        self.an("T6-1")
        chao = Line(P3(-2.6, 1.35), P3(2.6, 1.35)).set_stroke(GEO, 2.5, opacity=0.6)
        blk = Corpo("m", STEEL, 0.95, size=38).at(-0.9, 1.35)
        fa = arrow(P3(-0.42, 1.82), P3(1.5, 1.82), color=FC, width=9, tip=0.26)
        fl = tex(r"\vec F_{res}", FC, 42).next_to(fa, RIGHT, buff=0.18)
        self.play(Create(chao), FadeIn(blk), run_time=0.6)
        self.play(GrowArrow(fa), run_time=0.6)
        self.play(FadeIn(fl), run_time=0.4)
        paineis = VGroup()
        for lado, op, nome, res, cor in ((-1, r"\times\,\Delta t", "IMPULSO", r"\Delta\vec p", MAG),
                                         (1, r"\times\,d", "TRABALHO", r"\Delta K", WHITE_)):
            x = lado * PAINEL_X
            pl = painel(lado, 3.85, topo=0.95)
            a = tex(op, WHITE_, 56).move_to(P3(x, 0.25))
            s1 = tex(r"\downarrow", DIM, 42).move_to(P3(x, -0.4))
            b = txt(nome, T_MAIN, color=JC if nome == "IMPULSO" else WHITE_, bold=True).move_to(P3(x, -1.0))
            s2 = tex(r"\downarrow", DIM, 42).move_to(P3(x, -1.6))
            c = tex(res, cor, 60).move_to(P3(x, -2.3))
            paineis.add(VGroup(pl, a, s1, b, s2, c))
        self.ate(0.33)
        self.play(*[FadeIn(p[0]) for p in paineis], *[Write(p[1]) for p in paineis], run_time=0.9)
        for k, frac in ((0, 0.48), (1, 0.74)):
            self.ate(frac)
            p = paineis[k]
            self.play(FadeIn(p[2]), FadeIn(p[3], shift=0.1 * DOWN), run_time=0.6)
            self.play(FadeIn(p[4]), Write(p[5]), run_time=0.7)
            self.play(Indicate(p[5], color=WHITE_, scale_factor=1.15), run_time=0.6)
        self.ate(0.97)
        self.t61 = VGroup(blk, fa, fl, chao, paineis)

    # ── T6-2 · PALCO: as mãos e as bolas já em cena; CONTA: K = ½mv², p = mv → v = p/m entra no lugar de v → K = p²/(2m) ──
    def maos(self):
        linhas = []
        for y, r, mt, vt, kt, rec in ((0.75, 0.36, r"0{,}50\ \mathrm{kg}", r"4{,}0\ \mathrm{m/s}", r"K=4\ \mathrm{J}", 0.5),
                                     (-1.75, 0.2, r"0{,}10\ \mathrm{kg}", r"20\ \mathrm{m/s}", r"K=20\ \mathrm{J}", 2.5)):
            m = mao(1.0)
            linhas.append(dict(y=y, r=r, b=bola(r, GEO if r > 0.3 else STEEL), m=tex(mt, WHITE_, 34), v=tex(vt, VEL, 34),
                               lv=0.35 if r > 0.3 else 1.75, mao=m, rec=rec,
                               p=tex(r"p=2{,}0\ \mathrm{kg\cdot m/s}", MAG, 38), k=tex(kt, WHITE_, 42)))
        XM = -3.3
        for L in linhas:
            y = L["y"]
            L["b"].move_to(P3(-6.2, y))
            L["mao"].move_to(P3(XM, y + 0.05))
            L["m"].next_to(L["b"], DOWN, buff=0.22)
            L["va"] = arrow(P3(-6.2 + L["r"] + 0.1, y + 0.62), P3(-6.2 + L["r"] + 0.1 + L["lv"], y + 0.62), color=VEL, width=6)
            L["v"].next_to(L["va"], UP, buff=0.1)
            grp = VGroup(L["p"], L["k"]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            grp.align_to(P3(CONTA["x0"], 0), LEFT).set_y(y + 0.05)
        return linhas, XM

    def t6_2(self):
        self.an("T6-2")
        self.play(FadeOut(self.t61), run_time=0.5)
        self.linhas, self.XM = linhas, XM = self.maos()
        self.play(*[FadeIn(L[k]) for L in linhas for k in ("b", "m", "mao", "va", "v")], run_time=0.7)
        # v5: K = ½ m v² → K = ½ m (p/m)² → K = p²/(2m), cada passo por TransformMatchingTex (partes casadas pelo TeX)
        a = MathTex("K", "=", r"\frac{1}{2}", "m", "v^{2}", font_size=58)
        a[4].set_color(VEL)
        b = MathTex("p", "=", "m", "v", font_size=58)
        b[0].set_color(MAG)
        b[3].set_color(VEL)
        a.move_to(P3(2.4, 1.85))
        b.move_to(P3(3.4, 0.4))
        self.play(Write(a), Write(b), run_time=0.8)
        b2 = MathTex("v", "=", r"\frac{p}{m}", font_size=58).move_to(b)
        b2[0].set_color(VEL)
        b2[2].set_color(MAG)
        self.play(TransformMatchingTex(b, b2), run_time=0.8)
        c = MathTex("K", "=", r"\frac{1}{2}", "m", r"\left(\frac{p}{m}\right)^{2}", font_size=58)
        c[4].set_color(MAG)
        c.move_to(a, aligned_edge=LEFT)
        self.play(TransformMatchingTex(a, c), FadeOut(b2[2].copy(), target_position=c[4]), Indicate(b2, color=WHITE_, scale_factor=1.05), run_time=1.2)
        d = MathTex("K", "=", r"\frac{p^{2}}{2m}", font_size=72)
        d[2].set_color(MAG)
        d.move_to(P3(3.8, 1.75))
        self.play(FadeOut(b2), TransformMatchingTex(c, d), run_time=1.1)
        cx = caixa(d, MAG, buff=0.22)
        self.play(Create(cx), run_time=0.5)
        self.ate(0.97)
        self.kd = VGroup(d, cx)

    # ── T6-3 · as bolas chegam às mãos (recuo d e 5d); CONTA: p e K por linha, K = p²/(2m) no alto ───────────────────
    def t6_3(self):
        self.an("T6-3")
        linhas, XM = self.linhas, self.XM
        self.play(self.kd.animate.scale(0.75).move_to(P3(5.2, 2.0)), run_time=0.5)
        self.play(*[Write(L["p"]) for L in linhas], run_time=0.8)
        self.ate(0.25)
        self.play(*[Indicate(L["v"], color=WHITE_) for L in linhas], run_time=0.8)
        self.play(*[Indicate(L["p"], color=MAG) for L in linhas], run_time=0.7)
        self.ate(0.42)
        u = ValueTracker(0.0)

        def pos_bola(L):
            s = u.get_value()
            px = XM + L["mao"].palma_x
            if s <= 1:
                return -6.2 + (px - L["r"] + 6.2) * s
            w = min(s - 1, 1.0)
            return px - L["r"] + L["rec"] * (2 * w - w * w)

        def pos_mao(L):
            w = min(max(u.get_value() - 1, 0), 1.0)
            return L["rec"] * (2 * w - w * w)
        for L in linhas:
            L["b"].add_updater(lambda m, L=L: m.move_to(P3(pos_bola(L), L["y"] + 0.1)))
            L["x0m"] = L["mao"].get_center()[0]
            L["mao"].add_updater(lambda m, L=L: m.set_x(L["x0m"] + pos_mao(L)))
        self.play(*[FadeOut(L[k]) for L in linhas for k in ("va", "v", "m")], run_time=0.3)
        self.play(u.animate.set_value(1.0), run_time=1.0, rate_func=linear)
        self.play(u.animate.set_value(2.0), run_time=1.6, rate_func=linear)
        for L in linhas:
            L["b"].clear_updaters()
            L["mao"].clear_updaters()
        mesmo = txt("MESMO TEMPO PARA PARAR", T_SMALL, color=DIM).move_to(P3(0, -0.5)).align_to(P3(CONTA["x0"], 0), LEFT)
        self.play(FadeIn(mesmo), run_time=0.5)
        self.ate(0.62)
        self.play(*[Write(L["k"]) for L in linhas], Indicate(self.kd, color=WHITE_, scale_factor=1.05), run_time=0.9)
        self.ate(0.8)
        recs = VGroup()
        for L, rot in zip(linhas, ("d", "5d")):
            yb = L["y"] - 1.0
            a0, a1 = P3(XM, yb), P3(XM + L["rec"], yb)
            recs.add(DoubleArrow(a0, a1, buff=0, color=GEO, stroke_width=3, tip_length=0.13),
                     tex(rot, GEO, 36).next_to(a1, RIGHT, buff=0.15))
        self.play(Create(recs), run_time=0.8)
        self.play(Indicate(linhas[1]["k"], color=WHITE_, scale_factor=1.15), run_time=0.7)
        self.ate(0.97)
        self.t63 = VGroup(*[L[k] for L in linhas for k in ("b", "mao", "p", "k")], mesmo, recs)

    # ── T6-4 · PALCO: raias de gelo e barcos (rótulos acima de cada barco); CONTA: K = p²/(2m) no alto, p e √2 p ────────
    def t6_4(self):
        self.an("T6-4")
        self.play(FadeOut(self.t63), run_time=0.5)
        X0, XF = -5.2, 0.4
        raias = VGroup(*[Rectangle(width=XF + 0.4 - (-6.8), height=0.42).set_stroke(GEO, 1.5, opacity=0.6).set_fill("#2A3754", 1)
                         .move_to(P3((XF + 0.4 - 6.8) / 2, y)) for y in (0.35, -2.25)])
        linha_ch = DashedLine(P3(XF, 2.35), P3(XF, -2.6), color=GEO, stroke_width=2.5)
        ch_l = txt("CHEGADA", T_SMALL, color=GEO).next_to(linha_ch, UP, buff=0.12)
        b1, b2 = barco(0.75), barco(1.0)
        for b, y in ((b1, 0.35), (b2, -2.25)):
            b.move_to(P3(X0, 0)).shift(UP * (y + 0.21 - b[0].get_bottom()[1]))

        def etiqueta(s):
            t = tex(s, WHITE_, 38)
            fundo = RoundedRectangle(corner_radius=0.1, width=t.width + 0.3, height=t.height + 0.18).set_stroke(GEO, 1.2, opacity=0.6) \
                .set_fill(BACKGROUND_COLOR, 0.9)
            fundo.moldura = True
            return VGroup(fundo, t.move_to(fundo)).set_z_index(15)
        l1, l2 = etiqueta("m"), etiqueta("2m")
        l1.add_updater(lambda m: m.next_to(b1[0], LEFT, buff=0.18))
        l2.add_updater(lambda m: m.next_to(b2[0], LEFT, buff=0.18))
        T1 = 2.6
        t = ValueTracker(0.0)
        x1b, x2b = b1.get_center()[0], b2.get_center()[0]
        D = XF - 0.75 - X0

        def x_de(tt, Tch):
            return D * min(tt / Tch, 1.0) ** 2
        b1.add_updater(lambda m: m.set_x(x1b + x_de(t.get_value(), T1)))
        b2.add_updater(lambda m: m.set_x(x2b + x_de(t.get_value(), T1 * math.sqrt(2))))
        ventos = VGroup(always_redraw(lambda: arrow(b1[1].get_left() + P3(-1.0, 0.2), b1[1].get_left() + P3(-0.02, 0.2), color=FC, width=7)),
                        always_redraw(lambda: arrow(b2[1].get_left() + P3(-1.0, 0.2), b2[1].get_left() + P3(-0.02, 0.2), color=FC, width=7)))
        vl = VGroup(always_redraw(lambda: tex(r"\vec F", FC, 36).next_to(ventos[0], UP, buff=0.1)),
                    always_redraw(lambda: tex(r"\vec F", FC, 36).next_to(ventos[1], UP, buff=0.1)))
        vento_t = legenda("MESMO VENTO, MESMA DISTÂNCIA", x=-3.0)
        self.play(FadeIn(raias), Create(linha_ch), FadeIn(ch_l), FadeIn(b1), FadeIn(b2), FadeIn(l1), FadeIn(l2), run_time=0.8)
        self.play(FadeIn(ventos), FadeIn(vl), FadeIn(vento_t), run_time=0.6)
        self.ate(0.18)
        self.play(t.animate.set_value(T1 * math.sqrt(2)), run_time=T1 * math.sqrt(2) * 1.4, rate_func=linear)
        for m in (b1, b2, l1, l2):
            m.clear_updaters()
        clk = self.clk
        for k, b in enumerate((b1, b2)):
            ventos[k].clear_updaters()
            ventos.submobjects[k] = always_redraw(lambda b=b, k=k: arrow(b[1].get_left() + P3(-1.0 - 0.25 * math.sin(2.2 * clk.get_value() + k), 0.2),
                                                                         b[1].get_left() + P3(-0.02, 0.2), color=FC, width=7))
        self.add(ventos)
        k_ = txt("MESMA ENERGIA", T_MAIN, bold=True)
        L = 1.6
        p1 = arrow(P3(0, 0), P3(L, 0), color=MAG, width=8)
        p2 = arrow(P3(0, 0), P3(L * math.sqrt(2), 0), color=MAG, width=8)
        lp1 = tex(r"p", MAG, 44)
        lp2 = tex(r"\sqrt{2}\,p", MAG, 44)
        r1 = VGroup(tex("m", WHITE_, 38), p1, lp1).arrange(RIGHT, buff=0.25)
        r2 = VGroup(tex("2m", WHITE_, 38), p2, lp2).arrange(RIGHT, buff=0.25)
        mm = linha(txt("MOMENTO", T_LAB, color=MAG, bold=True), MathTex(r"\sqrt{2}", font_size=40, color=MAG),
                   txt("VEZES MAIOR", T_LAB, color=MAG, bold=True), buff=0.15)
        conta(k_, r1, r2, mm, topo=0.95, buff=0.45, x0=1.3)
        self.play(FadeOut(vento_t), Write(k_), Indicate(self.kd, color=WHITE_, scale_factor=1.05), run_time=0.8)
        self.ate(0.6)
        self.play(FadeIn(r1[0]), GrowArrow(p1), FadeIn(lp1), run_time=0.7)
        self.play(FadeIn(r2[0]), GrowArrow(p2), FadeIn(lp2), run_time=0.7)
        self.play(FadeIn(mm, shift=0.1 * UP), run_time=0.7)
        print(f"[QA] T6-4 mesma F e mesma d → mesma K; p = √(2mK) → p(2m)/p(m) = {math.sqrt(2 * 2) / math.sqrt(2 * 1):.4f} (√2)")
        self.ate(0.97)
        self.barcos = VGroup(raias, linha_ch, ch_l, b1, b2, l1, l2)
        self.t64 = VGroup(k_, r1, r2, mm)

    # ── T6-5 · os barcos ficam no PALCO; CONTA: as duas equações; DICA no canto ─────────────────────────────────────
    def t6_5(self):
        self.an("T6-5")
        self.play(FadeOut(self.t64), FadeOut(self.kd), run_time=0.5)
        e1 = Mc((r"\vec F_{res}", FC), (r"\,\Delta t", WHITE_), "=", (r"\Delta\vec p", MAG), size=M_MID)
        e2 = Mc((r"\vec F_{res}", FC), (r"\,d", WHITE_), "=", (r"\Delta K", WHITE_), size=M_MID)
        n1 = txt("FORÇA CONSTANTE", T_SMALL, color=DIM)
        conta(e1, e2, n1, topo=1.9, buff=0.45, x0=1.6)
        self.play(FadeIn(e1, shift=0.1 * UP), Indicate(self.barcos[3], color=WHITE_, scale_factor=1.05), run_time=0.8)
        self.play(FadeIn(e2, shift=0.1 * UP), FadeIn(n1), run_time=0.8)
        sa = lambda: MathTex(r"\to", font_size=26, color=WHITE_)
        self.dica_entra(dica(["TEMPO", sa(), "IMPULSO", sa(), "MOMENTO"], ["DISTÂNCIA", sa(), "TRABALHO", sa(), "ENERGIA"]))
        self.ate(0.96)
        self.clear(rt=0.5)
