"""Lote PT3 (v4): T3 — POR QUE MASSA VEZES VELOCIDADE? O trilho de ar em 2D/2,5D (sai o 3D do v3, pedido do Kaio): carrinhos em
aço com face de cima, explosão em laranja (HEAT, como no yt_0014), a visão do carro com o fundo correndo, os três casos com a
colisão rodando no trilho reduzido enquanto a conta fecha, e a convergência com o p⃗ = m v⃗ do T1."""
from kit import *  # noqa: F401,F403
from kit import _fundo

YT = -0.95                     # topo do trilho (cena grande)
VU = 1.45                      # u/s por v
DXT, DYT = 0.2, 0.14           # deslocamento da face de cima (2,5D)


def carrinho(w, nome, h=0.62, esc=1.3):
    """Carrinho do trilho de ar, 2,5D: frente em aço (gradiente), face de cima clara, saia escura; base em (0, 0)."""
    frente = Rectangle(width=w, height=h).set_stroke(mix(STEEL, 0.45), 1.8).set_fill([GEO, STEEL], 1.0)
    frente.set_sheen_direction(DOWN)
    frente.move_to(P3(0, h / 2 + 0.06))
    topo = Polygon(P3(-w / 2, h + 0.06), P3(w / 2, h + 0.06), P3(w / 2 + DXT, h + 0.06 + DYT), P3(-w / 2 + DXT, h + 0.06 + DYT)) \
        .set_stroke(mix(STEEL, 0.45), 1.5).set_fill(mix(GEO, 0.35), 1.0)
    lado = Polygon(P3(w / 2, 0.06), P3(w / 2 + DXT, 0.06 + DYT), P3(w / 2 + DXT, h + 0.06 + DYT), P3(w / 2, h + 0.06)) \
        .set_stroke(mix(STEEL, 0.45), 1.2).set_fill(interpolate_color(ManimColor(STEEL), ManimColor(BACKGROUND_COLOR), 0.35), 1.0)
    saia = Rectangle(width=w * 0.92, height=0.07).set_stroke(width=0).set_fill("#2A3142", 1).move_to(P3(0, 0.035))
    filete = Line(P3(-w / 2 + 0.08, h * 0.62), P3(w / 2 - 0.08, h * 0.62)).set_stroke(WHITE_, 1.2, opacity=0.35)
    lab = MathTex(nome, font_size=36, color=BACKGROUND_COLOR).move_to(P3(0, h * 0.36 + 0.06))
    g = VGroup(lado, frente, topo, saia, filete, lab).set_z_index(6).scale(esc, about_point=ORIGIN)
    g.lab = lab
    return g


class Trilho(VGroup):
    """Trilho de ar 2,5D de x0 a x1 com topo em y; os furos correm com `off` (visão do carro)."""

    def __init__(self, x0, x1, y, off=None, esc=1.0):
        super().__init__()
        e = esc
        topo = Polygon(P3(x0, y), P3(x1, y), P3(x1 + DXT * e, y + DYT * e), P3(x0 + DXT * e, y + DYT * e)) \
            .set_stroke(GEO, 1.2, opacity=0.6).set_fill("#3A4357", 1)
        frente = Rectangle(width=x1 - x0, height=0.42 * e).set_stroke(GEO, 1.2, opacity=0.6).set_fill([_fundo(0.2), _fundo(0.1)], 1) \
            .move_to(P3((x0 + x1) / 2, y - 0.21 * e))
        frente.set_sheen_direction(DOWN)
        self.add(frente, topo)
        self.off = off or ValueTracker(0.0)
        self.frente, self.L0 = frente, x1 - x0

        def furos():                                   # seguem a frente do trilho (inclusive quando ele encolhe)
            g = VGroup()
            k = frente.width / self.L0 * e
            xa, xb, yt = frente.get_left()[0], frente.get_right()[0], frente.get_top()[1]
            o = self.off.get_value() * k % (0.42 * k)
            x = xa + 0.2 * k - o
            while x < xb - 0.1 * k:
                if x > xa + 0.08 * k:
                    g.add(Dot(P3(x + DXT * k / 2, yt + DYT * k / 2), radius=0.022 * k, color=BACKGROUND_COLOR).set_opacity(0.8))
                    g.add(Line(P3(x, yt - 0.28 * k), P3(x, yt - 0.36 * k)).set_stroke(DIM, 1.4, opacity=0.7))
                x += 0.42 * k
            return g
        self.add(always_redraw(furos))
        self.set_z_index(2)


def estouro(c, cor=HEAT):
    """Explosão pequena: anel laranja, raios e miolo claro."""
    g = VGroup(Circle(radius=0.16).set_stroke(width=0).set_fill(mix(cor, 0.6), 0.95).move_to(c),
               Circle(radius=0.32).set_stroke(cor, 4).move_to(c))
    for k in range(10):
        a = k * TAU / 10 + 0.15
        g.add(Line(c + 0.38 * P3(math.cos(a), math.sin(a)), c + 0.7 * P3(math.cos(a), math.sin(a))).set_stroke(cor, 4))
    return g.set_z_index(20)


class LoteTrilho(Base):
    def construct(self):
        self.setup_base(cap="POR QUE MASSA VEZES VELOCIDADE?")
        self.t3_1()
        self.t3_2()
        self.t3_3()
        self.t3_4()
        self.t3_5()
        self.fim()
        self.relatorio()

    # ── cena: dois carrinhos num trilho; cinemática por função do tempo ───────────────────────────────────────────
    def montar(self, wA, wB, nA, nB, y=YT, esc=1.0, x0=-6.6, x1=6.6, off=None):
        tr = Trilho(x0, x1, y, off=off, esc=esc)
        A, B = carrinho(wA, nA).scale(esc), carrinho(wB, nB).scale(esc)
        return tr, A, B

    def setas_v(self, A, B, est, y, esc=1.0, lab=True):
        """Setas violeta acima de cada carrinho (ou do par grudado). est() → (va, vb, juntos, rotA, rotB, rotJ)."""
        def f():
            va, vb, junto, ra, rb, rj = est()
            g = VGroup()
            itens = [((A.get_center() + B.get_center()) / 2, va, rj)] if junto else [(A.get_center(), va, ra), (B.get_center(), vb, rb)]
            for c, v, r in itens:
                if abs(v) > 1e-6:
                    a = P3(c[0], y)
                    b = a + P3(0.95 * esc * v, 0)
                    g.add(arrow(a, b, color=VEL, width=6 * esc, tip=0.2 * esc))
                    if lab and r:
                        g.add(MathTex(r, font_size=int(36 * esc), color=VEL).next_to((a + b) / 2, UP, buff=0.1))
                elif lab and r:
                    g.add(MathTex(r, font_size=int(34 * esc), color=DIM).move_to(P3(c[0], y + 0.1)))
            return g
        return always_redraw(f)

    # ── T3-1 · por que essa grandeza? explosão entre carrinhos iguais ───────────────────────────────────────────────
    def t3_1(self):
        self.an("T3-1")
        cand = VGroup(*[MathTex(s, font_size=52) for s in (r"v\ ?", r"m\,v\ ?", r"m\,v^2\ ?")]).arrange(RIGHT, buff=1.3)
        cand[0].set_color(VEL)
        cand[1].set_color(MAG)
        centro(cand, 2.0)
        self.luz = vinheta(P3(0, YT + 0.4), 3.6, HEAT, soma=0.05)
        tr, A, B = self.montar(1.25, 1.25, "m", "m")
        self.tr = tr
        self.play(LaggedStart(*[FadeIn(c, shift=0.1 * UP) for c in cand], lag_ratio=0.35), FadeIn(self.luz), FadeIn(tr), run_time=1.4)
        cap = Circle(radius=0.12).set_stroke(mix(HEAT, 0.3), 2).set_fill(HEAT, 1).set_z_index(7)
        tt = ValueTracker(0.0)
        tex = 0.0

        def est():
            t = tt.get_value()
            d = max(0.0, t - tex)
            return (-1.0 if t > tex else 0.0), (1.0 if t > tex else 0.0), False, ("v" if t > tex else None), ("v" if t > tex else None), None
        A.add_updater(lambda m: m.move_to(P3(-0.81 - VU * est()[1] * (tt.get_value() - tex) * (tt.get_value() > tex), YT + 0.4)))
        B.add_updater(lambda m: m.move_to(P3(0.81 + VU * est()[1] * (tt.get_value() - tex) * (tt.get_value() > tex), YT + 0.4)))
        cap.move_to(P3(0, YT + 0.4))
        sv = self.setas_v(A, B, est, YT + 1.35)
        self.play(FadeIn(A, shift=0.2 * RIGHT), FadeIn(B, shift=0.2 * LEFT), FadeIn(cap), run_time=0.6)
        self.add(sv)
        self.ate(0.3)
        self.play(Indicate(cand[1], color=MAG, scale_factor=1.15), run_time=0.8)
        iguais = legenda("CARRINHOS IGUAIS, PARADOS")
        self.ate(0.5)
        self.play(FadeIn(iguais), Indicate(VGroup(A.lab, B.lab), color=WHITE_, scale_factor=1.3), run_time=0.8)
        # explosão (repete) — sem lado preferido: mesma velocidade para os dois lados
        for k in range(3):
            self.ate(0.62 + 0.13 * k)
            if k:
                tt.set_value(-0.6)
                self.play(FadeIn(cap), tt.animate.set_value(0.0), run_time=0.6, rate_func=linear)
            fl = estouro(P3(0, YT + 0.4))
            self.play(FadeIn(fl, scale=0.5), FadeOut(cap), tt.animate.set_value(0.25), run_time=0.25, rate_func=linear)
            self.play(FadeOut(fl, scale=1.4), tt.animate.set_value(2.2), run_time=1.95, rate_func=linear)
            if k == 0:
                sim = legenda("MESMA VELOCIDADE, UM PARA CADA LADO", T_LAB, color=VEL)
                self.play(FadeOut(iguais), FadeIn(sim), run_time=0.4)
        self.ate(0.97)
        for m in (A, B):
            m.clear_updaters()
        self.play(FadeOut(A), FadeOut(B), FadeOut(sv), FadeOut(sim), FadeOut(cand), run_time=0.4)

    # ── T3-2 · iguais, mesma velocidade, grudam e PARAM ───────────────────────────────────────────────────────────
    def t3_2(self):
        self.an("T3-2")
        _, A, B = self.montar(1.25, 1.25, "m", "m")
        x0 = 4.6
        tc = (x0 - 0.81) / VU
        tt = ValueTracker(0.0)

        def est():
            t = tt.get_value()
            if t < tc:
                return 1.0, -1.0, False, "v", "v", None
            return 0.0, 0.0, True, None, None, "0"
        A.add_updater(lambda m: m.move_to(P3(-x0 + VU * min(tt.get_value(), tc), YT + 0.4)))
        B.add_updater(lambda m: m.move_to(P3(x0 - VU * min(tt.get_value(), tc), YT + 0.4)))
        sv = self.setas_v(A, B, est, YT + 1.35)
        cola = txt("GRUDAM", T_SMALL, color=GEO)
        self.play(FadeIn(A), FadeIn(B), run_time=0.5)
        self.add(sv)
        self.play(tt.animate.set_value(tc), run_time=tc, rate_func=linear)
        fl = flash(P3(0, YT + 0.4))
        self.play(FadeIn(fl, scale=0.6), tt.animate.set_value(tc + 0.2), run_time=0.25)
        param = legenda("PARAM: PURA SIMETRIA", T_LAB, color=WHITE_)
        cola.next_to(P3(0, YT + 2.0), UP, buff=0.35)
        self.play(FadeOut(fl), FadeIn(param), FadeIn(cola), run_time=0.5)
        self.ate(0.97)
        for m in (A, B):
            m.clear_updaters()
        self.play(FadeOut(A), FadeOut(B), FadeOut(sv), FadeOut(param), FadeOut(cola), run_time=0.4)

    # ── T3-3 · a mesma colisão vista de dentro de um carro que anda com o carrinho da esquerda ─────────────────────────
    def t3_3(self):
        self.an("T3-3")
        _, A, B = self.montar(1.25, 1.25, "m", "m")
        off = self.tr.off
        x0 = 4.0
        tc = (2 * x0 - 1.62) / (2 * VU)                   # no chão: ±v; no carro: A parado, B a −2v
        tt = ValueTracker(-1.2)
        xA = -x0 + VU * tc                                 # onde o carrinho A fica na tela (parado no referencial do carro)

        def est():
            t = tt.get_value()
            if t < tc:
                return 0.0, -2.0, False, "0", "2v", None
            return -1.0, -1.0, True, None, None, "v"
        A.move_to(P3(-1.2, YT + 0.4))
        B.add_updater(lambda m: m.move_to(P3(-1.2 + 1.62 + 2 * VU * (tc - min(max(tt.get_value(), 0), tc)), YT + 0.4)
                                          if tt.get_value() < tc else P3(-1.2 + 1.62 - VU * (tt.get_value() - tc), YT + 0.4)))
        A.add_updater(lambda m: m.move_to(P3(-1.2 - VU * max(0.0, tt.get_value() - tc), YT + 0.4)))
        off.add_updater(lambda m: m.set_value(VU * tt.get_value()))
        self.add(off)
        sv = self.setas_v(A, B, est, YT + 1.35)
        # observador: carro estilizado + VISÃO DO CARRO
        corpo = RoundedRectangle(corner_radius=0.12, width=1.4, height=0.42).set_stroke(mix(STEEL, 0.5), 2).set_fill(STEEL, 1.0)
        cab = RoundedRectangle(corner_radius=0.1, width=0.7, height=0.3).set_stroke(mix(STEEL, 0.5), 2).set_fill(GEO, 1.0)
        cab.next_to(corpo, UP, buff=-0.02)
        rodas = VGroup(*[Circle(radius=0.14).set_stroke(mix(STEEL, 0.5), 2).set_fill(BACKGROUND_COLOR, 1.0).move_to(corpo.get_center() + P3(s * 0.4, -0.22))
                         for s in (-1, 1)])
        obs = VGroup(corpo, cab, rodas).move_to(P3(-4.6, -2.45))
        vis = txt("VISÃO DO CARRO", T_LAB, color=WHITE_).next_to(obs, RIGHT, buff=0.3)
        seta_obs = arrow(obs.get_right() + P3(3.35, 0), obs.get_right() + P3(4.35, 0), color=VEL, width=5, tip=0.16)
        lv = MathTex("v", font_size=32, color=VEL).next_to(seta_obs, UP, buff=0.08)
        self.play(FadeIn(obs, shift=0.3 * RIGHT), FadeIn(vis), GrowArrow(seta_obs), FadeIn(lv), run_time=0.8)
        self.play(FadeIn(A), FadeIn(B), run_time=0.5)
        self.add(sv)
        self.ate(0.18)
        self.play(tt.animate.set_value(0.0), run_time=1.2, rate_func=linear)
        self.ate(0.3)
        self.play(tt.animate.set_value(tc), run_time=tc, rate_func=linear)
        fl = flash(P3(-1.2 + 0.81, YT + 0.4))
        self.play(FadeIn(fl, scale=0.6), tt.animate.set_value(tc + 0.25), run_time=0.25, rate_func=linear)
        self.play(FadeOut(fl), tt.animate.set_value(tc + 2.4), run_time=2.15, rate_func=linear)
        orig = legenda("O CONJUNTO PASSA COM A VELOCIDADE ORIGINAL", T_LAB, color=VEL)
        self.play(FadeIn(orig), tt.animate.set_value(tc + 2.9), run_time=0.5, rate_func=linear)
        sobra = (self.alvo - self.nq) / FPS - 0.6
        if sobra > 2.2:                                    # repete a colisão vista do carro (nada parado, nada sai do quadro)
            self.play(FadeOut(A), FadeOut(B), FadeOut(sv), run_time=0.3)
            tt.set_value(-0.3)
            self.play(FadeIn(A), FadeIn(B), FadeIn(sv), run_time=0.3)
            fim_ = min(tc + 2.4, -0.3 + sobra - 0.6)
            self.play(tt.animate.set_value(fim_), run_time=fim_ + 0.3, rate_func=linear)
        self.ate(0.97)
        for m in (A, B, off):
            m.clear_updaters()
        self.play(FadeOut(A), FadeOut(B), FadeOut(sv), FadeOut(orig), FadeOut(obs), FadeOut(vis), FadeOut(seta_obs), FadeOut(lv), run_time=0.4)
        self.remove(off)

    # ── T3-4 · o trilho reduzido em cima roda cada caso enquanto a conta fecha embaixo ────────────────────────────────
    def t3_4(self):
        self.an("T3-4")
        ys, esc = 1.35, 0.72
        self.play(FadeOut(self.luz), self.tr.animate.scale(esc).move_to(P3(0, ys - 0.12)), run_time=0.8)
        casos = [
            (1.0, 1.0, "m", "m", 2.0, 0.0, r"m\cdot 2v+m\cdot 0=2m\cdot v", ("2v", "0", "v"), ([0, 1, 2, 3], [5, 6, 7], [9, 10, 11, 12])),
            (1.0, 1.4, "m", "2m", 2.0, -1.0, r"m\cdot 2v+2m\cdot(-v)=3m\cdot 0", ("2v", "-v", "0"),
             ([0, 1, 2, 3], [5, 6, 7, 8, 9, 10, 11], [13, 14, 15, 16])),
            (1.4, 1.7, "2m", "3m", 3.0, -2.0, r"2m\cdot 3v+3m\cdot(-2v)=5m\cdot 0", ("3v", "-2v", "0"),
             ([0, 1, 2, 3, 4], [6, 7, 8, 9, 10, 11, 12, 13], [15, 16, 17, 18])),
        ]
        eqs = VGroup()
        yeq = (-0.25, -1.35, -2.45)
        for k, (wA, wB, nA, nB, va, vb, tex, rots, idx) in enumerate(casos):
            self.ate((0.05, 0.42, 0.7)[k])
            A, B = carrinho(wA, nA).scale(esc), carrinho(wB, nB).scale(esc)
            mA, mB = {"m": 1, "2m": 2, "3m": 3}[nA], {"m": 1, "2m": 2, "3m": 3}[nB]
            vf = (mA * va + mB * vb) / (mA + mB)
            ytop = ys - 0.12 + 0.06
            ga, gb = wA * 1.3 * esc / 2, wB * 1.3 * esc / 2
            V4 = VU * esc * 1.7
            xa0, xb0 = -3.6, 3.6 if vb != 0 else 0.6
            tc = (xb0 - xa0 - ga - gb) / ((va - vb) * V4)
            tt = ValueTracker(0.0)

            def xs(t, xa0=xa0, xb0=xb0, va=va, vb=vb, tc=tc, vf=vf):
                if t < tc:
                    return xa0 + va * V4 * t, xb0 + vb * V4 * t
                xa, xb = xa0 + va * V4 * tc, xb0 + vb * V4 * tc
                return xa + vf * V4 * (t - tc), xb + vf * V4 * (t - tc)
            A.add_updater(lambda m, xs=xs, tt=tt: m.move_to(P3(xs(tt.get_value())[0], ytop + 0.33)))
            B.add_updater(lambda m, xs=xs, tt=tt: m.move_to(P3(xs(tt.get_value())[1], ytop + 0.33)))

            def est(tt=tt, tc=tc, va=va, vb=vb, vf=vf, rots=rots):
                if tt.get_value() < tc:
                    return va / 1.6, vb / 1.6, False, rots[0], rots[1], None
                return vf, vf, True, None, None, rots[2]
            sv = self.setas_v(A, B, est, ytop + 0.95, esc=0.8)
            eq = MathTex(tex, font_size=56, color=MAG)
            eq.move_to(P3(0, yeq[k]))
            igual = [i for i in range(len(eq[0])) if i not in idx[0] + idx[1] + idx[2] and i > max(idx[1])][0]
            eq.shift(RIGHT * (-eq[0][igual].get_center()[0]))
            self.play(FadeIn(A), FadeIn(B), run_time=0.3)
            self.add(sv)
            antes = VGroup(fixa(A.lab).set_color(MAG), fixa(B.lab).set_color(MAG))
            self.play(ReplacementTransform(antes[0], VGroup(*[eq[0][i] for i in idx[0]])), ReplacementTransform(antes[1], VGroup(*[eq[0][i] for i in idx[1]])),
                      FadeIn(VGroup(*[eq[0][i] for i in range(len(eq[0])) if i not in idx[0] + idx[1] + idx[2]])), run_time=0.7)
            self.play(tt.animate.set_value(tc), run_time=max(tc, 0.6), rate_func=linear)
            fl = flash((A.get_right() + B.get_left()) / 2).scale(0.7)
            self.play(FadeIn(fl, scale=0.6), tt.animate.set_value(tc + 0.2), run_time=0.25, rate_func=linear)
            self.play(FadeOut(fl), tt.animate.set_value(tc + 0.9), run_time=0.7, rate_func=linear)
            self.play(ReplacementTransform(VGroup(fixa(A.lab), fixa(B.lab)).set_color(MAG), VGroup(*[eq[0][i] for i in idx[2]])), run_time=0.8)
            self.add(eq)
            eqs.add(eq)
            self.play(Indicate(eq[0][igual], color=WHITE_, scale_factor=1.4), run_time=0.5)
            for m in (A, B):
                m.clear_updaters()
            self.play(FadeOut(A), FadeOut(B), FadeOut(sv), run_time=0.35)
        fecha = legenda("ANTES = DEPOIS, SEMPRE", T_LAB, color=WHITE_)
        self.ate(0.9)
        self.play(FadeIn(fecha), run_time=0.5)
        self.ate(0.97)
        self.eqs, self.fecha = eqs, fecha

    # ── T3-5 · a mesma grandeza por dois caminhos: segunda lei e simetria ─────────────────────────────────────────
    def t3_5(self):
        self.an("T3-5")
        self.play(FadeOut(self.tr), FadeOut(self.fecha), self.eqs.animate.scale(0.72).move_to(P3(3.6, 0.55)), run_time=0.7)
        # PALCO: o bloco do T1 com v⃗ e p⃗
        yb = -0.75
        blk = Corpo("m", STEEL, 1.3, 1.0, size=48).at(-4.1, yb)
        top = yb + 1.0
        v = arrow(P3(-4.1, top + 0.45), P3(-1.9, top + 0.45), color=VEL, width=8, tip=0.26)
        p = arrow(P3(-4.1, yb - 0.45), P3(-0.6, yb - 0.45), color=MAG, width=9, tip=0.28)
        lv = MathTex(r"\vec v", font_size=44, color=VEL).next_to(v, UP, buff=0.1)
        lp = MathTex(r"\vec p", font_size=44, color=MAG).next_to(p, DOWN, buff=0.1)
        self.play(FadeIn(blk, shift=0.2 * RIGHT), GrowArrow(v), FadeIn(lv), run_time=0.7)
        self.play(GrowArrow(p), FadeIn(lp), run_time=0.6)
        s1 = self.selo("DA SEGUNDA LEI", WHITE_).move_to(P3(-3.3, 2.05))
        s2 = self.selo("DA SIMETRIA", GEO).move_to(P3(3.6, 2.2))
        alvo = MathTex(r"\vec p=m\,\vec v", font_size=M_MAIN)
        for i in (0, 1):
            alvo[0][i].set_color(MAG)
        for i in (4, 5):
            alvo[0][i].set_color(VEL)
        centro(alvo, -2.45)
        bx = caixa(alvo, MAG, buff=0.22)
        self.play(FadeIn(s1, shift=0.1 * DOWN), FadeIn(s2, shift=0.1 * DOWN), run_time=0.6)
        self.ate(0.35)
        c1 = CurvedArrow(P3(-2.3, -1.75), alvo.get_corner(UL) + P3(-0.25, 0.05), angle=0.5, color=DIM, stroke_width=3, tip_length=0.18)
        c2 = CurvedArrow(P3(3.4, -0.55), alvo.get_corner(UR) + P3(0.25, 0.05), angle=-0.5, color=DIM, stroke_width=3, tip_length=0.18)
        self.play(Create(c1), Create(c2), run_time=0.8)
        self.play(ReplacementTransform(VGroup(lp.copy(), lv.copy()), alvo), run_time=1.0)
        self.play(Create(bx), run_time=0.6)
        nome = txt("MOMENTO LINEAR", T_MAIN, color=MAG, bold=True).next_to(bx, RIGHT, buff=0.4)
        self.ate(0.75)
        self.play(FadeIn(nome, shift=0.1 * LEFT), Indicate(VGroup(p, v), color=WHITE_, scale_factor=1.05), run_time=0.8)
        self.ate(0.97)
        self.clear(rt=0.5)

    def selo(self, s, cor):
        t = txt(s, T_LAB, color=cor, bold=True)
        r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.6, height=t.height + 0.38).set_stroke(cor, 2).set_fill(opacity=0)
        r.moldura = True
        t.move_to(r)
        return VGroup(r, t)
