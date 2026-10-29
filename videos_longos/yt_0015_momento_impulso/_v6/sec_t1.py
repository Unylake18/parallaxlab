"""Lote PA: abertura (A1–A3). Lote PB (v4): T2 — o fato experimental: três experiências com discos iguais num colchão de ar,
a tabela antes/depois montada a partir dos discos e a conservação com a colisão em loop (P⃗ sempre do mesmo tamanho)."""
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
        # v6: cartão do título só por ~4 s; o resto vira NESTE VÍDEO (um corpo) × NO PRÓXIMO (miniaturas de colisões)
        tit = centro(txt("MOMENTO LINEAR E IMPULSO", 60, color=CYAN, bold=True), 0.55)
        sub = centro(txt("NESTE VÍDEO: O QUE UMA FORÇA FAZ AO LONGO DO TEMPO", 30, op=0.9), -0.55)
        sob = Line(P3(-4.6, -0.05), P3(4.6, -0.05)).set_stroke(CYAN, 2, opacity=0.6)
        self.play(Write(tit), Create(sob), run_time=1.0)
        self.play(FadeIn(sub, shift=0.1 * UP), run_time=0.7)
        self.wait(1.8)
        self.play(FadeOut(tit), FadeOut(sub), FadeOut(sob), run_time=0.4)
        p1, p2 = painel(-1, 4.6), painel(1, 4.6)
        l1 = txt("NESTE VÍDEO: UM CORPO", T_LAB, color=GEO).move_to(P3(-PAINEL_X, 1.85))
        l2 = txt("NO PRÓXIMO: VÁRIOS CORPOS", T_LAB, color=GEO).move_to(P3(PAINEL_X, 1.85))
        # um corpo empurrado por uma força constante: v⃗ cresce com o tempo (loop de 3,2 s)
        t0 = self.clk.get_value()
        per, yb = 3.2, -0.35

        def corpo():
            u = (self.clk.get_value() - t0) % per
            x = -5.9 + 0.48 * u * u
            op = min(1.0, u / 0.25, (per - u) / 0.25)
            b = bola(0.3, GEO).move_to(P3(x, yb))
            f = arrow(P3(x - 1.25, yb), P3(x - 0.32, yb), color=FC, width=6, tip=0.2)
            v = arrow(P3(x, yb + 0.62), P3(x + 0.12 + 0.5 * u, yb + 0.62), color=VEL, width=6, tip=0.2)
            g = VGroup(b, f, v, rotulo(r"\vec F", FC, 34).next_to(f, DOWN, buff=0.12),
                       rotulo(r"\vec v", VEL, 34).next_to(v, UP, buff=0.1))
            return opac_rel(g, op)
        um = always_redraw(corpo)
        chao = Line(P3(-6.1, yb - 0.32), P3(-0.5, yb - 0.32)).set_stroke(GEO, 2, opacity=0.5)
        ft = txt("UMA FORÇA AO LONGO DO TEMPO", T_SMALL, color=DIM).move_to(P3(-PAINEL_X, -1.6))
        self.play(FadeIn(p1), FadeIn(l1), FadeIn(chao), FadeIn(um), FadeIn(ft), run_time=0.6)
        self.ate(0.6)
        self.play(FadeIn(p2), FadeIn(l2), run_time=0.5)
        minis = []
        for k, fr in enumerate((0.64, 0.76, 0.88)):
            self.ate(fr)
            m = self.mini(k, P3(PAINEL_X, 1.0 - 1.2 * k))
            self.play(FadeIn(m, shift=0.15 * LEFT), run_time=0.5)
            minis.append(m)
        self.an("A3")
        # os vídeos de colisões: as miniaturas vão para o centro e P⃗ᵢ = P⃗_f fecha embaixo
        um.clear_updaters()
        self.play(FadeOut(VGroup(p1, l1, chao, um, ft)), run_time=0.4)
        l3 = txt("DOS VÍDEOS DE COLISÕES", T_LAB, color=GEO).move_to(P3(0, 1.85))
        self.play(VGroup(p2, *minis).animate.shift(LEFT * PAINEL_X), ReplacementTransform(l2, l3), run_time=0.8)
        eq = centro(Mc((r"\vec P_i", MAG), "=", (r"\vec P_f", MAG), size=M_MAIN), -2.6)
        cx = SurroundingRectangle(eq, color=MAG, buff=0.22, stroke_width=2.5, corner_radius=0.1)
        self.ate(0.3)
        self.play(*[TransformFromCopy(m.eqp, eq) for m in minis[:1]], run_time=0.9)
        self.play(Create(cx), *[Indicate(m.eqp, color=MAG, scale_factor=1.15) for m in minis], run_time=0.8)
        self.ate(0.7)
        self.play(Indicate(eq, color=WHITE_, scale_factor=1.08), run_time=0.9)
        self.ate(0.96)
        for m in minis:
            m[1].clear_updaters()
        self.fim()
        self.relatorio()

    def mini(self, k, c):
        """Miniatura k de colisão (loop de 3 s, presa ao relógio): 0 = blocos em 1D (elástica), 1 = carrinhos que grudam,
        2 = discos em 2D. Com um P⃗ᵢ = P⃗_f pequeno à direita (eqp)."""
        t0 = self.clk.get_value()
        per = 3.0
        ref = Dot(c, radius=0.01).set_opacity(0)      # âncora: o desenho segue a miniatura quando ela se move

        def f():
            x0, y0 = ref.get_center()[0] - 1.0, ref.get_center()[1]
            u = (self.clk.get_value() - t0) % per
            op = min(1.0, u / 0.25, (per - u) / 0.25)
            g = VGroup()
            if k < 2:
                g.add(Line(P3(x0 - 2.0, y0 - 0.3), P3(x0 + 2.0, y0 - 0.3)).set_stroke(GEO, 1.6, opacity=0.5))
            if k == 0:
                tc = 1.2
                xa, xb = (x0 - 1.6 + 1.0 * u, x0 + 1.4 - 0.6 * u) if u < tc else (x0 - 0.4 - 0.2 * (u - tc), x0 + 0.68 + 1.0 * (u - tc))
                g.add(Corpo("", GEO, 0.5).move_to(P3(xa, y0 - 0.05)), Corpo("", STEEL, 0.36).move_to(P3(xb, y0 - 0.12)))
            elif k == 1:
                tc = 1.3
                xa = x0 - 1.6 + 1.1 * min(u, tc) + 0.55 * max(0, u - tc)
                xb = x0 + 0.27 + 0.55 * max(0, u - tc) if u >= tc else x0 + 0.27
                g.add(Corpo("", GEO, 0.5, 0.36).move_to(P3(xa, y0 - 0.12)), Corpo("", STEEL, 0.5, 0.36).move_to(P3(xb + 0.0, y0 - 0.12)))
                if u >= tc:
                    g.add(Line(P3(xa + 0.25, y0 - 0.25), P3(xa + 0.25, y0 + 0.01)).set_stroke(HEAT, 3))
            else:
                tc = 1.2
                if u < tc:
                    pa, pb = P3(x0 - 1.7 + 1.4 * u, y0), P3(x0 + 0.4, y0)
                else:
                    w = u - tc
                    pa, pb = P3(x0 - 0.02 + 0.8 * w, y0 + 0.2 * w), P3(x0 + 0.4 + 0.6 * w, y0 - 0.2 * w)     # espalha pouco: não sai da faixa
                g.add(bola(0.22, GEO).move_to(pa), bola(0.22, STEEL).move_to(pb))
            return opac_rel(g, op)
        anim = always_redraw(f)
        eqp = Mc((r"\vec P_i", MAG), "=", (r"\vec P_f", MAG), size=34).move_to(P3(c[0] + 2.1, c[1]))
        g = VGroup(ref, anim, eqp)
        g.eqp = eqp
        return g


# ── colchão de ar visto de cima ──────────────────────────────────────────────────────────────────────────────
MESA_Y, MESA_W, MESA_H = -0.35, 13.4, 3.7
R_DISCO = 0.42
VU = 2.2                                        # u/s da velocidade v na tela


def disco(cor=STEEL):
    c = Circle(radius=R_DISCO).set_stroke(mix(cor, 0.5), 2.5).set_fill(cor, 1.0)
    anel = Circle(radius=R_DISCO * 0.62).set_stroke(WHITE_, 1.5, opacity=0.35).set_fill(opacity=0)
    cen = Dot(radius=0.05, color=GEO)
    return VGroup(c, anel, cen).set_z_index(5)


def cinematica(va, vb, cola, xa0, xb0, R, vu):
    """Dois discos iguais num eixo: posições e velocidades (em unidades de v) no instante t; troca (elástica) ou grudados."""
    t_col = (xb0 - xa0 - 2 * R) / ((va - vb) * vu)

    def xs(t):
        if t <= t_col:
            return xa0 + va * vu * t, xb0 + vb * vu * t, va, vb
        xc_a, xc_b = xa0 + va * vu * t_col, xb0 + vb * vu * t_col
        if cola:
            vm = (va + vb) / 2
            return xc_a + vm * vu * (t - t_col), xc_b + vm * vu * (t - t_col), vm, vm
        return xc_a + vb * vu * (t - t_col), xc_b + va * vu * (t - t_col), vb, va
    return xs, t_col


ROT_V = {1: "+v", -1: "-v", 0: "0", 0.5: r"\tfrac{v}{2}"}


class LoteT1(Base):
    def construct(self):
        self.setup_base(cap="O FATO EXPERIMENTAL")
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

    def ensaio(self, nome, va, vb, cola=False):
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
        pos = ValueTracker(0.0)
        xs, t_col = cinematica(va, vb, cola, xa0, xb0, R_DISCO, VU)

        def setas():
            xa, xb, ua, ub = xs(pos.get_value())
            g = VGroup()
            for x, u in ((xa, ua), (xb, ub)):
                if abs(u) > 1e-6:
                    g.add(arrow(P3(x, y + R_DISCO + 0.35), P3(x + 1.25 * u, y + R_DISCO + 0.35), color=VEL, width=6))
                    lab = {1: "v", -1: "v", 0.5: r"v/2"}.get(u, "v")
                    g.add(MathTex(lab, font_size=36, color=VEL).move_to(P3(x + 0.62 * u, y + R_DISCO + 0.75)))
            return g
        A.add_updater(lambda m: m.move_to(P3(xs(pos.get_value())[0], y)))
        B.add_updater(lambda m: m.move_to(P3(xs(pos.get_value())[1], y)))
        if chic is not None:
            chic.add_updater(lambda m: m.move_to(P3(xs(pos.get_value())[0] + R_DISCO - 0.02, y)))
        sv = always_redraw(setas)
        return A, B, chic, tit, pos, sv, t_col

    def experiencias(self):
        cfgs = [("T2-1", "EXPERIÊNCIA 1", 1, -1, False), ("T2-2", "EXPERIÊNCIA 2", 1, 0, False), ("T2-3", "EXPERIÊNCIA 3", 1, 0, True)]
        for k, (aid, nome, va, vb, cola) in enumerate(cfgs):
            self.an(aid)
            A, B, chic, tit, pos, sv, tc = self.ensaio(nome, va, vb, cola)
            novos = [A, B, tit] + ([chic] if chic is not None else [])
            if k == 0:                                   # v6 (G1): os discos entram no colchão junto com o header
                pre = txt("SEM FORÇA DE FORA?", T_LAB, color=DIM).move_to(P3(0, MESA_Y + MESA_H / 2 + 0.4))
                self.play(FadeIn(self.mesa_g), FadeIn(self.rot_mesa), *[FadeIn(m) for m in novos if m is not tit], run_time=0.6)
                self.play(FadeIn(pre), Indicate(A, color=WHITE_, scale_factor=1.08), Indicate(B, color=WHITE_, scale_factor=1.08), run_time=0.6)
                self.ate(0.3)
                self.play(FadeOut(pre), run_time=0.3)
                self.play(FadeIn(tit), run_time=0.4)
            else:
                self.play(*[FadeIn(m) for m in novos], run_time=0.6)
            self.add(sv)
            if cola:
                ct = txt("CHICLETE", T_SMALL, color=GEO).next_to(chic, DOWN, buff=0.55)
                ct.add_updater(lambda m, c=chic: m.next_to(c, DOWN, buff=0.55))
                self.play(FadeIn(ct), Indicate(chic, color=WHITE_, scale_factor=1.6), run_time=0.8)
                self.ate(0.3)
                novos.append(ct)
            else:
                self.ate(0.45 if k == 0 else 0.2)
            dur_mov = tc + 2.2
            self.play(pos.animate.set_value(tc), run_time=tc, rate_func=linear)
            fl = flash((A.get_center() + B.get_center()) / 2).set_z_index(20)
            self.play(FadeIn(fl, scale=0.6), pos.animate.set_value(tc + 0.25), run_time=0.25, rate_func=linear)
            self.play(FadeOut(fl), pos.animate.set_value(dur_mov), run_time=dur_mov - tc - 0.25, rate_func=linear)
            while (self.alvo - self.nq) / FPS > dur_mov + 1.4:          # sobra fala: a colisão se repete (nada parado)
                vis = [m for m in novos + [sv] if m is not tit]
                self.play(*[FadeOut(m) for m in vis], run_time=0.3)
                pos.set_value(0.0)
                self.play(*[FadeIn(m) for m in vis], run_time=0.3)
                self.play(pos.animate.set_value(dur_mov), run_time=dur_mov, rate_func=linear)
            self.ate(0.97)
            for m in (A, B) + ((chic,) if chic is not None else ()):
                m.clear_updaters()
            sv.clear_updaters()
            self.play(*[FadeOut(m) for m in novos + [sv]], run_time=0.4)

    # ── T2-4 · a tabela montada a partir dos discos (mini-colchão à esquerda de cada linha) ─────────────────────────
    def mini(self, va, vb, cola, y, x0=-6.45, x1=-3.35, r=0.2):
        """Mini-colchão com os dois discos da linha; posição pelo ValueTracker devolvido (tempo do ensaio)."""
        pista = RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=0.95).set_stroke(GEO, 1.2, opacity=0.4) \
            .set_fill(PANEL, 0.5).move_to(P3((x0 + x1) / 2, y - 0.1))
        xa0, xb0 = (x0 + 0.35, x1 - 0.35) if vb != 0 else (x0 + 0.35, (x0 + x1) / 2 + 0.25)
        xs, tc = cinematica(va, vb, cola, xa0, xb0, r, 1.5)
        tt = ValueTracker(0.0)
        A, B = disco(GEO).scale(r / R_DISCO), disco(STEEL).scale(r / R_DISCO)
        A.add_updater(lambda m: m.move_to(P3(xs(tt.get_value())[0], y - 0.22)))
        B.add_updater(lambda m: m.move_to(P3(xs(tt.get_value())[1], y - 0.22)))

        def setas():
            xa, xb, ua, ub = xs(tt.get_value())
            g = VGroup()
            for x, u in ((xa, ua), (xb, ub)):
                if abs(u) > 1e-6:
                    g.add(arrow(P3(x, y + 0.13), P3(x + 0.55 * u, y + 0.13), color=VEL, width=4, tip=0.13))
            return g
        sv = always_redraw(setas)
        return VGroup(pista, A, B, sv), tt, xs, tc

    def tabela(self):
        self.an("T2-4")
        self.play(FadeOut(self.mesa_g), FadeOut(self.rot_mesa), run_time=0.4)
        xa, xd, xdiv = 0.1, 4.4, 2.3
        cab = VGroup(txt("ANTES", T_LAB, color=DIM).move_to(P3(xa, 2.35)), txt("DEPOIS", T_LAB, color=DIM).move_to(P3(xd, 2.35)))
        regua = Line(P3(-6.6, 2.0), P3(6.9, 2.0)).set_stroke(GEO, 1.5, opacity=0.4)
        div = Line(P3(xdiv, 2.6), P3(xdiv, -3.1)).set_stroke(GEO, 1.5, opacity=0.3)
        linhas = [
            (1, -1, False, r"m(+v)+m(-v)", r"=0", r"m(-v)+m(+v)", r"=0", ([2, 3], [8, 9]), ([2, 3], [8, 9])),
            (1, 0, False, r"m\,v+m\cdot 0", r"=m\,v", r"m\cdot 0+m\,v", r"=m\,v", ([1], [5]), ([2], [5])),
            (1, 0, True, r"m\,v+m\cdot 0", r"=m\,v", r"m\,\tfrac{v}{2}+m\,\tfrac{v}{2}", r"=m\,v", ([1], [5]), ([1, 2, 3], [6, 7, 8])),
        ]
        self.play(FadeIn(cab), Create(regua), Create(div), run_time=0.5)
        ys = (1.15, -0.6, -2.35)
        fr = (0.0, 0.3, 0.6)
        ant = None
        for k, ((va, vb, cola, a, ta, d, td, ia, idp), y) in enumerate(zip(linhas, ys)):
            self.ate(fr[k])
            mg, tt, xs, tc = self.mini(va, vb, cola, y)
            nome = txt(f"EXP. {k + 1}", T_SMALL, bold=True).move_to(P3(-2.6, y))
            ma = MathTex(a, ta, font_size=40).move_to(P3(0, y)).align_to(P3(-1.85, 0), LEFT)
            md = MathTex(d, td, font_size=40).move_to(P3(0, y)).align_to(P3(2.6, 0), LEFT)
            for m in (ma, md):
                m[1].set_color(MAG)
            if ant is not None:                                  # a linha anterior para no fim e apaga um pouco
                for x in ant[0][1:3]:
                    x.clear_updaters()
                ant[0][3].clear_updaters()
                self.play(opac_anim(ant[0], 0.45), FadeIn(mg), FadeIn(nome), run_time=0.5)
            else:
                self.play(FadeIn(mg), FadeIn(nome), run_time=0.5)
            # antes: os valores saem dos discos; a colisão roda; depois: idem
            xa_, xb_, ua, ub = xs(0)
            fa = VGroup(*[MathTex(ROT_V[u], font_size=30, color=VEL).move_to(P3(x, y + 0.42)) for x, u in ((xa_, ua), (xb_, ub))])
            self.play(ReplacementTransform(fa[0], VGroup(*[ma[0][i] for i in ia[0]])), ReplacementTransform(fa[1], VGroup(*[ma[0][i] for i in ia[1]])),
                      FadeIn(VGroup(*[g for i, g in enumerate(ma[0]) if i not in ia[0] + ia[1]]), ma[1]), run_time=0.9)
            self.play(tt.animate.set_value(tc + 0.7), run_time=tc + 0.7, rate_func=linear)
            xa_, xb_, ua, ub = xs(tc + 0.7)
            fd = VGroup(*[MathTex(ROT_V[u], font_size=30, color=VEL).move_to(P3(x, y + 0.42)) for x, u in ((xa_, ua), (xb_, ub))])
            self.play(ReplacementTransform(fd[0], VGroup(*[md[0][i] for i in idp[0]])), ReplacementTransform(fd[1], VGroup(*[md[0][i] for i in idp[1]])),
                      FadeIn(VGroup(*[g for i, g in enumerate(md[0]) if i not in idp[0] + idp[1]]), md[1]), run_time=0.9)
            self.add(ma, md)
            self.play(Indicate(ma[1], color=MAG, scale_factor=1.25), Indicate(md[1], color=MAG, scale_factor=1.25), run_time=0.5)
            # repete a colisão da linha atual (loop lento) até a próxima
            t0 = self.clk.get_value()
            per = tc + 0.75
            tt.add_updater(lambda m, t0=t0, per=per: m.set_value((self.clk.get_value() - t0) % per))
            self.add(tt)
            ant = (mg, tt)
        nota = txt("COM MASSAS DIFERENTES: A SOMA TAMBÉM SE MANTÉM", T_SMALL, color=DIM).move_to(P3(0.6, -3.45))
        self.ate(0.84)
        self.play(FadeIn(nota), run_time=0.6)
        self.ate(0.97)
        ant[1].clear_updaters()
        for x in ant[0][1:3]:
            x.clear_updaters()
        self.clear(rt=0.5)

    # ── T2-5 · conservação: a experiência 3 em loop lento; p⃗₁, p⃗₂ e a soma P⃗ (sempre do mesmo tamanho) ──────────────
    def lei(self):
        self.an("T2-5")
        y = 0.55
        pista = placa(7.0, 2.4, P3(-3.0, y - 0.1))
        luz = vinheta(P3(-3.0, y), 2.6, MAG, soma=0.06)
        xs, tc = cinematica(1, 0, True, -6.0, -3.4, R_DISCO, 1.1)
        per = 5.0
        t0 = self.clk.get_value()
        tt = lambda: ((self.clk.get_value() - t0) % per) - 0.4
        A, B = disco(GEO), disco(STEEL)
        chic = Ellipse(width=0.24, height=0.34).set_stroke(GEO, 1.5).set_fill("#D9DFEA", 1).set_z_index(6)

        def xs_(t):
            return xs(max(0.0, t))
        A.add_updater(lambda m: m.move_to(P3(xs_(tt())[0], y)))
        B.add_updater(lambda m: m.move_to(P3(xs_(tt())[1], y)))
        chic.add_updater(lambda m: m.move_to(P3(xs_(tt())[0] + R_DISCO - 0.02, y)))
        KP = 1.7                                          # m v em unidades de tela
        yb = -1.6

        def setas():
            xa, xb, ua, ub = xs_(tt())
            g = VGroup()
            for x, u in ((xa, ua), (xb, ub)):
                if abs(u) > 1e-6:
                    g.add(arrow(P3(x, y + R_DISCO + 0.3), P3(x + KP * u, y + R_DISCO + 0.3), color=MAG, width=7, tip=0.2))
            # P⃗ = p⃗₁ + p⃗₂ cabeça com cauda, abaixo da pista: o total nunca muda
            x0 = -5.1
            g.add(arrow(P3(x0, yb), P3(x0 + KP * ua, yb), color=MAG, width=10, tip=0.22))
            if ub > 1e-6:
                g.add(arrow(P3(x0 + KP * ua, yb), P3(x0 + KP * (ua + ub), yb), color=mix(MAG, 0.35), width=10, tip=0.22))
            g.add(Line(P3(x0, yb - 0.35), P3(x0 + KP, yb - 0.35)).set_stroke(WHITE_, 2, opacity=0.6))
            return g
        sv = always_redraw(setas)
        l1 = MathTex(r"\vec p_1", font_size=38, color=MAG)
        l1.add_updater(lambda m: m.move_to(A.get_center() + P3(0.5, R_DISCO + 0.72)))
        l2 = MathTex(r"\vec p_2", font_size=38, color=MAG)
        l2.add_updater(lambda m: m.move_to(B.get_center() + P3(0.5, R_DISCO + 0.72)).set_opacity(1.0 if xs_(tt())[3] > 1e-6 else 0.0))
        lP = MathTex(r"\vec P", font_size=40, color=MAG).move_to(P3(-5.1 + KP / 2, yb - 0.7))
        tot = txt("SEMPRE DO MESMO TAMANHO", T_SMALL, color=DIM).next_to(lP, RIGHT, buff=0.4)
        eq = MathTex(r"\vec P=\vec p_1+\vec p_2=\text{constante}", font_size=54)
        for i in (0, 1, 3, 4, 5, 7, 8, 9):
            eq[0][i].set_color(MAG)
        t1 = txt("PRINCÍPIO DE CONSERVAÇÃO", T_MAIN, bold=True)
        t1b = txt("DO MOMENTO", T_MAIN, bold=True)
        t2 = txt("(SISTEMA ISOLADO)", T_LAB, color=DIM)
        conta(eq, t1, t1b, t2, topo=1.7, buff=0.3)
        t1.shift(DOWN * 0.25)
        t1b.shift(DOWN * 0.25)
        t2.shift(DOWN * 0.25)
        self.play(FadeIn(pista), FadeIn(luz), FadeIn(A), FadeIn(B), FadeIn(chic), run_time=0.6)
        self.add(sv)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(lP), FadeIn(tot), run_time=0.5)
        self.ate(0.18)
        self.play(ReplacementTransform(fixa(lP), VGroup(*eq[0][0:2])), ReplacementTransform(fixa(l1), VGroup(*eq[0][3:6])),
                  ReplacementTransform(fixa(l2).set_opacity(1), VGroup(*eq[0][7:10])), FadeIn(VGroup(eq[0][2], eq[0][6])), run_time=1.1)
        self.play(Write(VGroup(*eq[0][10:])), run_time=0.8)
        self.add(eq)
        self.ate(0.42)
        self.play(FadeIn(t1, shift=0.1 * UP), FadeIn(t1b, shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(t2), run_time=0.4)
        self.ate(0.7)
        bx = caixa(eq, MAG, buff=0.2)
        self.play(Create(bx), Indicate(lP, color=WHITE_, scale_factor=1.3), run_time=0.9)
        self.ate(0.97)
        for m in (A, B, chic, l1, l2):
            m.clear_updaters()
        self.clear(rt=0.5)


def opac_anim(m, f):
    """Animação curta que leva m à opacidade relativa f."""
    return UpdateFromAlphaFunc(m, lambda x, a: opac_rel(x, 1 + (f - 1) * a))
