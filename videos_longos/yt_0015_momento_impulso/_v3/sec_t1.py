"""Lote PA: abertura (A1–A3). Lote PB: T1 — o fato experimental (Moysés §4.5): três experiências com discos iguais num colchão
de ar e a tabela antes/depois de m·v₁ + m·v₂."""
from kit import *  # noqa: F401,F403


class LoteAbertura(Base):
    def construct(self):
        self.setup_base()
        self.an("A1")
        logo = self.logo(4.6).move_to(P3(0, 0.6))
        wel = txt("BEM-VINDOS AO PARALLAX LAB", 34).move_to(P3(0, -1.3))
        self.play(FadeIn(logo, scale=0.94), FadeIn(wel, shift=0.1 * UP), run_time=1.0)
        self.ate(0.9)
        self.play(FadeOut(logo), FadeOut(wel), run_time=0.4)
        self.an("A2")
        tit = centro(txt("MOMENTO LINEAR E IMPULSO", 60, color=CYAN, bold=True), 0.55)
        sub = centro(txt("NESTE VÍDEO: O QUE UMA FORÇA FAZ AO LONGO DO TEMPO", 30, op=0.9), -0.55)
        sob = Line(P3(-4.6, -0.05), P3(4.6, -0.05)).set_stroke(CYAN, 2, opacity=0.6)
        self.play(Write(tit), run_time=1.2)
        self.play(Create(sob), run_time=0.6)
        self.ate(0.3)
        self.play(FadeIn(sub, shift=0.1 * UP), run_time=0.8)
        self.ate(0.6)
        self.play(Indicate(sub, color=WHITE_, scale_factor=1.04), run_time=0.9)
        self.ate(0.95)
        self.play(FadeOut(tit), FadeOut(sub), FadeOut(sob), run_time=0.5)
        self.an("A3")
        # DOIS PAINÉIS: colisão 1D (blocos) e 2D (discos), animadas; P_i = P_f no CENTRO embaixo
        p1, p2 = painel(-1, 3.9), painel(1, 3.9)
        l1 = txt("COLISÕES EM 1D", T_LAB, color=GEO).move_to(P3(-PAINEL_X, 1.95))
        l2 = txt("COLISÕES EM 2D", T_LAB, color=GEO).move_to(P3(PAINEL_X, 1.95))
        yb = -0.6
        pista = Line(P3(-6.1, yb), P3(-0.5, yb)).set_stroke(GEO, 2, opacity=0.5)
        u = ValueTracker(0.0)
        c1, c2 = Corpo("", GEO, 0.8), Corpo("", STEEL, 0.6)

        def x1d(s_):                                  # blocos: 2 kg a +1, 1 kg a −1; depois (elástica) −1/3 e +5/3
            tc = 1.0
            if s_ < tc:
                return -5.0 + 1.4 * s_, -1.6 - 1.4 * s_
            return -3.6 - 0.47 * (s_ - tc), -3.0 + 2.33 * (s_ - tc)
        c1.add_updater(lambda m: m.move_to(P3(x1d(u.get_value())[0], yb + 0.4)))
        c2.add_updater(lambda m: m.move_to(P3(x1d(u.get_value())[1], yb + 0.3)))
        d1, d2 = bola(0.32, GEO), bola(0.32, STEEL)

        def x2d(s_):
            tc = 1.0
            if s_ < tc:
                return P3(1.4 + 1.5 * s_, -0.2), P3(4.2, -0.2 + 0.0 * s_)
            k = s_ - tc
            return P3(2.9 + 0.9 * k, -0.2 + 0.9 * k), P3(4.2 + 0.9 * k, -0.2 - 0.9 * k)
        d1.add_updater(lambda m: m.move_to(x2d(u.get_value())[0]))
        d2.add_updater(lambda m: m.move_to(x2d(u.get_value())[1]))
        eq = centro(Mc((r"\vec P_i", MAG), "=", (r"\vec P_f", MAG), size=M_MAIN), -2.55)
        cx = SurroundingRectangle(eq, color=MAG, buff=0.22, stroke_width=2.5, corner_radius=0.1)
        self.play(FadeIn(p1), FadeIn(l1), FadeIn(pista), FadeIn(c1), FadeIn(c2), FadeIn(p2), FadeIn(l2), FadeIn(d1), FadeIn(d2), run_time=0.8)
        self.play(u.animate.set_value(2.2), run_time=3.4, rate_func=linear)
        self.ate(0.4)
        self.play(Write(eq), run_time=1.0)
        self.play(Create(cx), run_time=0.6)
        self.ate(0.75)
        self.play(Indicate(eq, color=WHITE_, scale_factor=1.08), run_time=0.9)
        self.ate(0.96)
        for m in (c1, c2, d1, d2):
            m.clear_updaters()
        self.clear(rt=0.5)
        self.fim()
        self.relatorio()


# ── colchão de ar visto de cima ──────────────────────────────────────────────────────────────────────────────
MESA_Y, MESA_W, MESA_H = -0.35, 13.4, 3.7
R_DISCO = 0.42
VU = 2.2                                        # u/s da velocidade v na tela


def disco(cor=STEEL):
    c = Circle(radius=R_DISCO).set_stroke(mix(cor, 0.5), 2.5).set_fill(cor, 1.0)
    anel = Circle(radius=R_DISCO * 0.62).set_stroke(WHITE_, 1.5, opacity=0.35).set_fill(opacity=0)
    cen = Dot(radius=0.05, color=GEO)
    return VGroup(c, anel, cen).set_z_index(5)


class LoteT1(Base):
    def construct(self):
        self.setup_base(cap="O FATO EXPERIMENTAL", selo="MOYSÉS §4.5")
        self.mesa()
        self.experiencias()
        self.tabela()
        self.lei()
        self.fim()
        self.relatorio()

    def mesa(self):
        tampo = RoundedRectangle(corner_radius=0.18, width=MESA_W, height=MESA_H).set_stroke(GEO, 2, opacity=0.55) \
            .set_fill(PANEL, 0.55).move_to(P3(0, MESA_Y))
        furos = VGroup(*[Dot(P3(x, y), radius=0.022, color=DIM).set_opacity(0.45)
                         for x in np.arange(-6.3, 6.31, 0.45) for y in np.arange(MESA_Y - 1.55, MESA_Y + 1.56, 0.45)])
        self.mesa_g = VGroup(tampo, furos).set_z_index(-1)
        self.rot_mesa = txt("COLCHÃO DE AR · VISTO DE CIMA", T_SMALL, color=DIM).next_to(tampo, DOWN, buff=0.2)

    def ensaio(self, nome, va, vb, cola=False, rotulo_extra=None):
        """Dois discos iguais no eixo da mesa; va, vb em unidades de v (antes); depois: troca (elástica) ou grudados."""
        y = MESA_Y
        A, B = disco(GEO), disco(STEEL)
        xa0, xb0 = (-4.6, 4.6) if vb != 0 else (-4.6, 0.6)
        A.move_to(P3(xa0, y))
        B.move_to(P3(xb0, y))
        chic = None
        if cola:
            chic = Ellipse(width=0.24, height=0.34).set_stroke(GEO, 1.5).set_fill("#D9DFEA", 1).set_z_index(6)
            chic.move_to(A.get_center() + P3(R_DISCO - 0.02, 0))
        tit = txt(nome, T_LAB, bold=True).move_to(P3(0, MESA_Y + MESA_H / 2 + 0.4))
        pos = ValueTracker(0.0)            # tempo físico (s de tela)
        t_col = (xb0 - xa0 - 2 * R_DISCO) / ((va - vb) * VU)

        def xs(t):
            if t <= t_col:
                return xa0 + va * VU * t, xb0 + vb * VU * t, va, vb
            xc_a, xc_b = xa0 + va * VU * t_col, xb0 + vb * VU * t_col
            if cola:
                vm = (va + vb) / 2
                return xc_a + vm * VU * (t - t_col), xc_b + vm * VU * (t - t_col), vm, vm
            return xc_a + vb * VU * (t - t_col), xc_b + va * VU * (t - t_col), vb, va

        def setas():
            t = pos.get_value()
            xa, xb, ua, ub = xs(t)
            g = VGroup()
            for x, u in ((xa, ua), (xb, ub)):
                if abs(u) > 1e-6:
                    g.add(arrow(P3(x, y + R_DISCO + 0.35), P3(x + 1.25 * u, y + R_DISCO + 0.35), color=VEL, width=6))
                    lab = {1: "v", -1: "-v", 0.5: r"v/2"}.get(u, "v")
                    g.add(MathTex(lab if u != -1 else "v", font_size=36, color=VEL).move_to(P3(x + 0.62 * u, y + R_DISCO + 0.75)))
            return g
        A.add_updater(lambda m: m.move_to(P3(xs(pos.get_value())[0], y)))
        B.add_updater(lambda m: m.move_to(P3(xs(pos.get_value())[1], y)))
        if chic is not None:
            chic.add_updater(lambda m: m.move_to(P3(xs(pos.get_value())[0] + R_DISCO - 0.02, y)))
        sv = always_redraw(setas)
        return A, B, chic, tit, pos, sv, t_col

    def experiencias(self):
        cfgs = [("T1-1", "EXPERIÊNCIA 1", 1, -1, False), ("T1-2", "EXPERIÊNCIA 2", 1, 0, False), ("T1-3", "EXPERIÊNCIA 3", 1, 0, True)]
        for k, (aid, nome, va, vb, cola) in enumerate(cfgs):
            self.an(aid)
            A, B, chic, tit, pos, sv, tc = self.ensaio(nome, va, vb, cola)
            novos = [A, B, tit] + ([chic] if chic is not None else [])
            if k == 0:
                self.play(FadeIn(self.mesa_g), FadeIn(self.rot_mesa), run_time=0.8)
                self.ate(0.3)
            self.play(*[FadeIn(m) for m in novos], run_time=0.6)
            self.add(sv)
            if cola:
                ct = txt("CHICLETE", T_SMALL, color=GEO).next_to(chic, DOWN, buff=0.55)
                ct.add_updater(lambda m, c=chic: m.next_to(c, DOWN, buff=0.55))
                self.play(FadeIn(ct), Indicate(chic, color=WHITE_, scale_factor=1.6), run_time=0.8)
                self.ate(0.3)
                novos.append(ct)
            else:
                self.ate(0.25 if k == 0 else 0.2)
            dur_mov = tc + 2.2
            self.play(pos.animate.set_value(tc), run_time=tc, rate_func=linear)
            fl = flash((A.get_center() + B.get_center()) / 2 + P3(0, 0)).set_z_index(20)
            self.play(FadeIn(fl, scale=0.6), pos.animate.set_value(tc + 0.25), run_time=0.25, rate_func=linear)
            self.play(FadeOut(fl), pos.animate.set_value(dur_mov), run_time=dur_mov - tc - 0.25, rate_func=linear)
            self.ate(0.97)
            for m in (A, B) + ((chic,) if chic is not None else ()):
                m.clear_updaters()
            sv.clear_updaters()
            self.play(*[FadeOut(m) for m in novos + [sv]], run_time=0.4)

    def tabela(self):
        self.an("T1-4")
        self.play(FadeOut(self.mesa_g), FadeOut(self.rot_mesa), run_time=0.5)
        xa, xd = -1.2, 4.3
        cab = VGroup(txt("ANTES", T_LAB, color=DIM).move_to(P3(xa, 2.35)), txt("DEPOIS", T_LAB, color=DIM).move_to(P3(xd, 2.35)))
        regua = Line(P3(-6.6, 2.0), P3(6.9, 2.0)).set_stroke(GEO, 1.5, opacity=0.4)
        div = Line(P3(1.55, 2.6), P3(1.55, -3.6)).set_stroke(GEO, 1.5, opacity=0.3)
        linhas = [
            ("EXP. 1", r"m(+v)+m(-v)", r"=0", r"m(-v)+m(+v)", r"=0"),
            ("EXP. 2", r"m\,v+m\cdot 0", r"=m\,v", r"m\cdot 0+m\,v", r"=m\,v"),
            ("EXP. 3", r"m\,v+m\cdot 0", r"=m\,v", r"m\,\tfrac{v}{2}+m\,\tfrac{v}{2}", r"=m\,v"),
        ]
        self.play(FadeIn(cab), Create(regua), Create(div), run_time=0.7)
        ys = (1.15, -0.6, -2.35)
        self.ate(0.12)
        for (n, a, ta, d, td), y in zip(linhas, ys):
            rot = txt(n, T_LAB, bold=True).move_to(P3(-5.6, y))
            ma = MathTex(a, ta, font_size=46).move_to(P3(xa, y))
            md = MathTex(d, td, font_size=46).move_to(P3(xd, y))
            for m in (ma, md):
                m[1].set_color(MAG)
            self.play(FadeIn(rot), FadeIn(ma, shift=0.1 * RIGHT), run_time=0.7)
            self.play(FadeIn(md, shift=0.1 * RIGHT), run_time=0.7)
            self.play(Indicate(ma[1], color=MAG, scale_factor=1.25), Indicate(md[1], color=MAG, scale_factor=1.25), run_time=0.8)
            self.ate({1.15: 0.38, -0.6: 0.58, -2.35: 0.75}[y])
        nota = txt("COM MASSAS DIFERENTES: A SOMA TAMBÉM SE MANTÉM", T_SMALL, color=DIM).move_to(P3(1.0, -3.55))
        self.play(FadeIn(nota), run_time=0.6)
        self.ate(0.97)
        self.clear(rt=0.5)

    def lei(self):
        self.an("T1-5")
        eq = Mc((r"\vec P", MAG), "=", (r"\vec p_1", MAG), "+", (r"\vec p_2", MAG), "=", (r"\text{constante}", WHITE_), size=M_MAIN)
        eq.move_to(P3(0, 0.9))
        t1 = txt("PRINCÍPIO DE CONSERVAÇÃO DO MOMENTO", 36, bold=True).move_to(P3(0, -0.7))
        t2 = txt("(SISTEMA ISOLADO)", T_LAB, color=DIM).next_to(t1, DOWN, buff=0.3)
        self.play(FadeIn(eq, shift=0.1 * UP), run_time=1.0)
        self.ate(0.3)
        self.play(FadeIn(t1, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(t2), run_time=0.5)
        caixa = SurroundingRectangle(eq, color=MAG, buff=0.3, stroke_width=2.5, corner_radius=0.1)
        self.ate(0.6)
        self.play(Create(caixa), run_time=0.8)
        self.ate(0.96)
        self.clear(rt=0.5)
