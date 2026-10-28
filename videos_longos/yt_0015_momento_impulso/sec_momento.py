"""Lote PT1 (v4): T1 — DE ONDE VEM O MOMENTO. Uma partícula percorre uma curva lisa no espaço (projeção 2,5D desenhada no Manim,
leve e alinhada por construção); v⃗ = dr⃗/dt e F⃗_res = m d²r⃗/dt² saem da própria curva, quadro a quadro. Da segunda lei para
p⃗ = m v⃗, as componentes em x, y, z e ΣF⃗ = dp⃗/dt (PALCO vivo + CONTA; símbolos descem da animação para a conta)."""
from MF_Tools import TransformByGlyphMap

from kit import *  # noqa: F401,F403
from sec_teoria import foguete

# ── espaço 2,5D: x para o observador (baixo-esquerda), y para a direita, z para cima (destro) ─────────────────────────
O3 = P3(-5.0, -2.05)
ESC3 = 1.3
EX, EY, EZ = ESC3 * np.array([-0.62, -0.40, 0.0]), ESC3 * np.array([0.92, 0.12, 0.0]), ESC3 * np.array([0.0, 1.0, 0.0])


def pj(x, y, z):
    return O3 + x * EX + y * EY + z * EZ


def pjv(v):
    return pj(*v)


# curva r(s) = (X0 + A sen s, Y0 + B cos s, Z0 + C sen 2s), s = ω t (fechada, lisa, reversa): v ∝ dr/ds, F ∝ d²r/ds²
A_, B_, C_ = 1.0, 1.5, 0.45
X0, Y0, Z0 = 1.0, 2.05, 1.55
KV, KF, MASSA = 0.62, 0.36, 1.6           # escalas de tela de v e F; p⃗ = m v⃗ desenhado com m = 1,6
W_LOOP = 2 * PI / 15.0                    # uma volta a cada 15 s


def r_(s):
    return np.array([X0 + A_ * math.sin(s), Y0 + B_ * math.cos(s), Z0 + C_ * math.sin(2 * s)])


def dr_(s):
    return np.array([A_ * math.cos(s), -B_ * math.sin(s), 2 * C_ * math.cos(2 * s)])


def d2r_(s):
    return np.array([-A_ * math.sin(s), -B_ * math.cos(s), -4 * C_ * math.sin(2 * s)])


def esfera(r=0.21):
    c = Circle(radius=r).set_stroke(mix(GEO, 0.3), 1.6).set_fill([WHITE_, GEO, STEEL, "#3E4757"], 1.0)
    c.set_sheen_direction(DR)
    brilho = Circle(radius=r * 0.28).set_stroke(width=0).set_fill(WHITE_, 0.75).move_to(P3(-0.35 * r, 0.38 * r))
    return VGroup(c, brilho).set_z_index(12)


def rot(m, ref, d, gap=0.28):
    """Põe o rótulo m na ponta `ref`, deslocado na direção de tela d."""
    d = np.asarray(d, float)
    n = np.linalg.norm(d)
    u = d / n if n > 1e-6 else UP
    meia = 0.5 * (abs(u[0]) * m.width + abs(u[1]) * m.height)
    return m.move_to(np.asarray(ref, float) + u * (gap + meia))


class LoteMomento(Base):
    def construct(self):
        self.setup_base(cap="DE ONDE VEM O MOMENTO")
        self.mot = Motor(self, s0=0.4, w=W_LOOP)
        self.espaco()
        self.t1_1()
        self.t1_2()
        self.t1_3()
        self.t1_4()
        self.t1_5()
        self.t1_6()
        self.t1_7()
        self.fim()
        self.relatorio()

    # ── o espaço: chão em grade, eixos, partícula, rastro, sombra e vetores (tudo por updater do relógio) ─────────────
    def espaco(self):
        s = self.mot.fase
        grade = VGroup()
        for x in np.arange(0, 2.01, 0.5):
            grade.add(Line(pj(x, 0, 0), pj(x, 3.8, 0)).set_stroke(DIM, 1, opacity=0.16))
        for y in np.arange(0, 3.81, 0.5):
            grade.add(Line(pj(0, y, 0), pj(2.0, y, 0)).set_stroke(DIM, 1, opacity=0.16))
        chao = Polygon(pj(0, 0, 0), pj(2.0, 0, 0), pj(2.0, 3.8, 0), pj(0, 3.8, 0)).set_stroke(width=0).set_fill(PANEL, 0.35)
        ex = arrow(pj(0, 0, 0), pj(2.25, 0, 0), color=GEO, width=3, tip=0.17)
        ey = arrow(pj(0, 0, 0), pj(0, 4.0, 0), color=GEO, width=3, tip=0.17)
        ez = arrow(pj(0, 0, 0), pj(0, 0, 2.95), color=GEO, width=3, tip=0.17)
        lx = MathTex("x", font_size=38, color=GEO).next_to(pj(2.25, 0, 0), UP, buff=0.12)
        ly = MathTex("y", font_size=38, color=GEO).next_to(pj(0, 4.0, 0), DOWN, buff=0.12)
        lz = MathTex("z", font_size=38, color=GEO).next_to(pj(0, 0, 2.95), LEFT, buff=0.12)
        self.eixos3 = VGroup(chao, grade, ex, ey, ez, lx, ly, lz).set_z_index(1)
        self.luz = vinheta(pj(1.0, 2.2, 1.2), 3.4, GEO, soma=0.09)

        def rastro():
            g = VGroup()
            s0 = s()
            n = 34
            pts = [pjv(r_(s0 - 2.6 * (1 - k / n))) for k in range(n + 1)]
            for k in range(n):
                g.add(Line(pts[k], pts[k + 1]).set_stroke(GEO, 2.2, opacity=0.06 + 0.6 * (k / n) ** 1.6))
            return g.set_z_index(4)

        def sombra():
            p = r_(s())
            pe = pj(p[0], p[1], 0)
            return VGroup(DashedLine(pe, pjv(p), dash_length=0.06).set_stroke(DIM, 1.4, opacity=0.5),
                          Ellipse(width=0.34, height=0.14).set_stroke(width=0).set_fill(BACKGROUND_COLOR, 0.75).move_to(pe)).set_z_index(3)
        self.part = esfera()
        self.part.add_updater(lambda m: m.move_to(pjv(r_(s()))))
        self.rastro, self.sombra = always_redraw(rastro), always_redraw(sombra)
        # vetores na partícula: visibilidades por ValueTracker
        self.vv, self.fv, self.av, self.pv, self.pk = (ValueTracker(0.0) for _ in range(5))

        def vec_v():
            if self.vv.get_value() < 0.02:
                return VMobject()
            p = r_(s())
            return arrow(pjv(p), pjv(p + KV * dr_(s())), color=VEL, width=6, tip=0.2, z=11).set_opacity(self.vv.get_value())

        def vec_p():
            if self.pv.get_value() < 0.02:
                return VMobject()
            p = r_(s())
            k = 1 + (MASSA - 1) * self.pk.get_value()
            return arrow(pjv(p), pjv(p + k * KV * dr_(s())), color=MAG, width=9, tip=0.24, z=9).set_opacity(self.pv.get_value())

        def vec_f():
            if self.fv.get_value() < 0.02:
                return VMobject()
            p = r_(s())
            return arrow(pjv(p), pjv(p + KF * d2r_(s())), color=FC, width=6, tip=0.2, z=10).set_opacity(self.fv.get_value())

        def vec_a():
            if self.av.get_value() < 0.02:
                return VMobject()
            p = r_(s())
            a, b = pjv(p), pjv(p + KF / MASSA * d2r_(s()))
            d = (b - a) / max(np.linalg.norm(b - a), 1e-6)
            n = np.array([-d[1], d[0], 0]) * 0.13
            ar = arrow(a + n, b + n, color=GEO, width=3.5, tip=0.15, z=10)
            return DashedVMobject(ar, num_dashes=7).set_opacity(self.av.get_value()) if ar.has_points() else VMobject()
        self.Vv, self.Vp, self.Vf, self.Va = (always_redraw(f) for f in (vec_v, vec_p, vec_f, vec_a))
        # rótulos (criados uma vez; seguem por updater)
        self.lv = MathTex(r"\vec v", font_size=40, color=VEL).set_z_index(13)
        self.lv.add_updater(lambda m: rot(m, pjv(r_(s()) + KV * dr_(s())), (pjv(dr_(s())) - O3), 0.12))
        self.lf = MathTex(r"\Sigma\vec F", font_size=40, color=FC).set_z_index(13)
        self.lf.add_updater(lambda m: rot(m, pjv(r_(s()) + KF * d2r_(s())), (pjv(d2r_(s())) - O3), 0.1))
        self.la = MathTex(r"\vec a", font_size=36, color=GEO).set_z_index(13)

        def pos_a(m):
            p = r_(s())
            a, b = pjv(p), pjv(p + KF / MASSA * d2r_(s()))
            d = (b - a) / max(np.linalg.norm(b - a), 1e-6)
            rot(m, (a + b) / 2, np.array([-d[1], d[0], 0]), 0.2)
        self.la.add_updater(pos_a)
        self.lp = MathTex(r"\vec p", font_size=42, color=MAG).set_z_index(13)
        self.lp.add_updater(lambda m: rot(m, pjv(r_(s()) + (1 + (MASSA - 1) * self.pk.get_value()) * KV * dr_(s())), (pjv(dr_(s())) - O3), 0.12)
                            .set_opacity(self.pv.get_value()))
        self.cena3 = VGroup(self.luz, self.eixos3, self.rastro, self.sombra, self.part, self.Vv, self.Vp, self.Vf, self.Va)

    def rotulos3(self):
        return [self.lv, self.lf, self.la, self.lp]

    def ir_para(self, alvo, rt=1.6):
        """Desacelera a partícula até a fase `alvo` (sempre para a frente) e para."""
        self.mot.para()
        s0 = self.mot.s
        while alvo < s0:
            alvo += 2 * PI
        self.play(UpdateFromAlphaFunc(Mobject(), lambda m, a: setattr(self.mot, "s", s0 + (alvo - s0) * (1 - (1 - a) ** 2))),
                  run_time=rt, rate_func=linear)
        self.mot.s = alvo

    # ── T1-1 · a segunda lei numa trajetória qualquer ─────────────────────────────────────────────────────────────
    def t1_1(self):
        self.an("T1-1")
        self.play(FadeIn(self.luz), FadeIn(self.eixos3[0]), Create(self.eixos3[1]), run_time=0.8)
        self.play(*[GrowArrow(a) for a in self.eixos3[2:5]], FadeIn(self.eixos3[5:]), run_time=0.8)
        self.mot.corre()
        self.add(self.rastro, self.sombra)
        sl = txt("SEGUNDA LEI DE NEWTON", T_LAB, color=DIM).move_to(P3(0, 2.3)).align_to(P3(CONTA["x0"], 0), LEFT)
        self.play(FadeIn(self.part, scale=0.5), FadeIn(sl, shift=0.1 * UP), run_time=0.6)
        self.sl = sl
        ml = MathTex("m", font_size=38, color=WHITE_).set_z_index(13)
        ml.add_updater(lambda m: m.next_to(self.part, UL, buff=0.02))
        self.play(FadeIn(ml), run_time=0.5)
        self.ate(0.3)
        self.add(self.Vv, self.Vf, self.Va)
        self.play(self.vv.animate.set_value(1), FadeIn(self.lv), run_time=0.8)
        self.ate(0.5)
        self.play(self.fv.animate.set_value(1), FadeIn(self.lf), run_time=0.8)
        self.play(self.av.animate.set_value(1), FadeIn(self.la), run_time=0.6)
        self.ml = ml
        # CONTA: ΣF⃗ = m a⃗ (F⃗ e a⃗ descem dos rótulos)
        e0 = MathTex(r"\Sigma\vec F=m\,\vec a", font_size=M_MAIN)
        self.pinta(e0, F=[0, 1, 2], a=[5, 6])
        conta(e0, topo=1.75)
        self.ate(0.7)
        self.play(TransformFromCopy(self.lf, VGroup(*e0[0][0:3])), TransformFromCopy(self.la, VGroup(*e0[0][5:7])),
                  TransformFromCopy(ml, e0[0][4]), FadeIn(e0[0][3]), run_time=1.3)
        self.add(e0)
        self.ate(0.85)
        self.play(Indicate(VGroup(*e0[0][4:7]), color=WHITE_, scale_factor=1.12), run_time=0.8)
        self.e0 = e0

    def pinta(self, m, F=(), a=(), v=(), p=(), J=()):
        for idx, c in ((F, FC), (a, GEO), (v, VEL), (p, MAG), (J, JC)):
            for i in idx:
                m[0][i].set_color(c)
        return m

    # ── T1-2 · a⃗ = dv⃗/dt nasce de dois instantes próximos; o m entra na derivada ────────────────────────────────────
    def t1_2(self):
        self.an("T1-2")
        s1 = 5.55
        self.play(self.av.animate.set_value(0), FadeOut(self.la), run_time=0.4)
        self.ir_para(s1, 1.6)
        ds = ValueTracker(0.75)

        def fantasma():
            s2 = s1 + ds.get_value()
            p1, p2 = r_(s1), r_(s2)
            v1 = KV * dr_(s1)
            v2 = KV * dr_(s2)
            g = VGroup(esfera().set_opacity(0.35).move_to(pjv(p2)),
                       arrow(pjv(p2), pjv(p2 + v2), color=VEL, width=5, tip=0.18).set_opacity(0.4),
                       arrow(pjv(p1), pjv(p1 + v2), color=VEL, width=5, tip=0.18).set_opacity(0.75),
                       arrow(pjv(p1 + v1), pjv(p1 + v2), color=WHITE_, width=5, tip=0.14, z=14))
            return g
        fan = always_redraw(fantasma)
        ldv = MathTex(r"\Delta\vec v", font_size=38, color=WHITE_).set_z_index(14)
        ldv.add_updater(lambda m: rot(m, pjv(r_(s1) + KV * (dr_(s1) + dr_(s1 + ds.get_value())) / 2), DR, 0.32))
        self.play(FadeIn(fan), run_time=0.7)
        self.play(FadeIn(ldv), run_time=0.4)
        lim = MathTex(r"\Delta t\to 0", font_size=40, color=DIM)
        self.play(FadeOut(self.sl), self.e0.animate.align_to(P3(0, 2.15), UP), run_time=0.5)
        conta(self.e0, lim, topo=2.15, buff=0.5)
        self.ate(0.18)
        self.play(FadeIn(lim), ds.animate.set_value(0.07), run_time=2.6, rate_func=smooth)
        ldv2 = MathTex(r"d\vec v", font_size=38, color=WHITE_).set_z_index(14).move_to(ldv)
        ldv2.add_updater(lambda m: rot(m, pjv(r_(s1) + KV * dr_(s1)), DR, 0.3))
        self.play(ReplacementTransform(ldv, ldv2), run_time=0.6)
        # a⃗ = dv⃗/dt na CONTA (dv⃗ desce do desenho)
        ea = MathTex(r"\vec a=\frac{d\vec v}{dt}", font_size=M_MID)
        self.pinta(ea, a=[0, 1], v=[4, 5])
        ea.next_to(self.e0, DOWN, buff=0.45).align_to(self.e0, LEFT)
        self.ate(0.36)
        self.play(FadeOut(lim), TransformFromCopy(ldv2, VGroup(*ea[0][3:6])), FadeIn(VGroup(*ea[0][0:3], *ea[0][6:9])), run_time=1.1)
        self.add(ea)
        # ΣF⃗ = m a⃗ → ΣF⃗ = m dv⃗/dt (a⃗ vira a fração)
        e1 = MathTex(r"\Sigma\vec F=m\,\frac{d\vec v}{dt}", font_size=M_MAIN)
        self.pinta(e1, F=[0, 1, 2], v=[6, 7])
        e1.move_to(self.e0, aligned_edge=LEFT)
        self.ate(0.5)
        self.play(TransformByGlyphMap(self.e0, e1, ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]), ([5, 6], [5, 6, 7, 8, 9, 10])),
                  Indicate(ea, color=WHITE_, scale_factor=1.04), run_time=1.3)
        self.play(FadeOut(fan), FadeOut(ldv2), FadeOut(ea), run_time=0.5)
        self.mot.corre()
        # o m entra na derivada (massa constante)
        e2 = MathTex(r"\Sigma\vec F=\frac{d(m\vec v)}{dt}", font_size=M_MAIN)
        self.pinta(e2, F=[0, 1, 2], v=[7, 8])
        e2.move_to(e1, aligned_edge=LEFT)
        mc = txt("MASSA CONSTANTE", T_SMALL, color=GEO, bold=True)
        mcx = VGroup(RoundedRectangle(corner_radius=0.1, width=mc.width + 0.4, height=mc.height + 0.3).set_stroke(GEO, 1.6), mc)
        mc.move_to(mcx[0])
        mcx[0].moldura = True
        mcx.next_to(e2, DOWN, buff=0.4).align_to(e2, LEFT)
        self.ate(0.7)
        self.play(FadeIn(mcx, shift=0.1 * UP), run_time=0.6)
        self.play(TransformByGlyphMap(e1, e2, ([0, 1, 2, 3], [0, 1, 2, 3]), ([4], [6], {"path_arc": -1.2}), ([5], [4]), ([6, 7], [7, 8]),
                                      ([8], [10]), ([9, 10], [11, 12]), ([], [5, 9])), run_time=1.5)
        self.ate(0.92)
        self.play(Indicate(VGroup(*e2[0][4:10]), color=WHITE_, scale_factor=1.08), run_time=0.8)
        self.e2, self.mcx = e2, mcx

    # ── T1-3 · p⃗ = m v⃗: a seta magenta nasce da violeta, esticada pelo fator m ────────────────────────────────────
    def t1_3(self):
        self.an("T1-3")
        e2 = self.e2
        pe = MathTex(r"\vec p=m\,\vec v", font_size=M_MAIN)
        self.pinta(pe, p=[0, 1], v=[4, 5])
        nome = txt("MOMENTO LINEAR", T_MAIN, color=MAG, bold=True)
        nome2 = txt("OU QUANTIDADE DE MOVIMENTO", T_SMALL, color=DIM)
        un = MathTex(r"[\,p\,]=\mathrm{kg\cdot m/s}", font_size=M_REF, color=MAG)
        self.play(FadeOut(self.mcx), run_time=0.3)
        conta(e2, pe, nome, nome2, un, topo=2.15, buff=0.36)
        pe.shift(DOWN * 0.15)
        hl = caixa(VGroup(*e2[0][5:10]), MAG, buff=0.08, w=2.2)
        self.play(Create(hl), run_time=0.7)
        self.add(self.Vp)
        self.play(self.pv.animate.set_value(1), self.fv.animate.set_value(0.35), FadeOut(self.lf), run_time=0.5)
        self.play(self.pk.animate.set_value(1), FadeIn(self.lp), run_time=1.3)
        self.ate(0.22)
        self.play(TransformFromCopy(self.lp, VGroup(*pe[0][0:2])), FadeIn(pe[0][2]), TransformFromCopy(VGroup(*e2[0][6:9]), VGroup(*pe[0][3:6])),
                  run_time=1.3)
        self.add(pe)
        bx = caixa(pe, MAG, buff=0.18)
        self.play(Create(bx), FadeIn(nome, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(nome2), run_time=0.5)
        self.ate(0.58)
        self.play(Indicate(VGroup(self.lp, self.lv), color=WHITE_, scale_factor=1.25), run_time=0.9)
        self.ate(0.8)
        self.play(Write(un), run_time=0.9)
        self.ate(0.97)
        self.pe, self.pe_bx, self.nomes, self.un, self.hl = pe, bx, VGroup(nome, nome2), un, hl
        self.peg = VGroup(pe, bx)

    # ── T1-4 · vetor de verdade: dois carros iguais, norte e leste (vista de cima) ───────────────────────────────────
    def t1_4(self):
        self.an("T1-4")
        self.mot.para()
        tudo3 = [self.cena3, self.ml, *self.rotulos3()]
        self.play(*[FadeOut(m) for m in tudo3], FadeOut(self.e2), FadeOut(self.hl), FadeOut(self.nomes), FadeOut(self.un),
                  self.peg.animate.move_to(P3(3.8, 1.85)), run_time=0.8)
        for m in tudo3:
            self.remove(m)
        # PALCO: ruas vistas de cima, carro 1 para o norte, carro 2 para o leste (em loop), setas p⃗ magenta iguais
        pista = placa(7.0, 5.3, P3(-3.0, -0.3))
        rua_v = Rectangle(width=1.3, height=5.0).set_stroke(DIM, 1.2, opacity=0.5).set_fill("#151B2B", 1).move_to(P3(-5.6, -0.3))
        rua_h = Rectangle(width=5.25, height=1.3).set_stroke(DIM, 1.2, opacity=0.5).set_fill("#151B2B", 1).move_to(P3(-2.33, -1.9))
        faixa_v = DashedLine(P3(-6.05, -2.75), P3(-6.05, 2.15), dash_length=0.2).set_stroke(DIM, 1.5, opacity=0.4)
        faixa_h = DashedLine(P3(-4.9, -2.4), P3(0.25, -2.4), dash_length=0.2).set_stroke(DIM, 1.5, opacity=0.4)
        ruas = VGroup(rua_v, rua_h, faixa_v, faixa_h)
        rosa = VGroup(arrow(P3(-1.2, 0.6), P3(-1.2, 1.5), color=DIM, width=3, tip=0.15), arrow(P3(-1.2, 0.6), P3(-0.3, 0.6), color=DIM, width=3, tip=0.15),
                      txt("N", 20, color=DIM).move_to(P3(-1.2, 1.75)), txt("L", 20, color=DIM).move_to(P3(-0.05, 0.6)))
        u = ValueTracker(0.0)
        c1 = opac_rel(Carro(1.25, 0.66, GEO, ang=PI / 2), 1.0)
        c2 = opac_rel(Carro(1.25, 0.66, GEO, ang=0), 1.0)
        L1, L2 = 2.7, 2.4                       # trechos (a seta nunca sai da pista); some e volta nas pontas

        def f_(x, L):
            return min(1.0, x / 0.35, (L - x) / 0.35)
        c1.add_updater(lambda m: m.move_to(P3(-5.6, -2.45 + (u.get_value() * 0.45 + 1.0) % L1)))
        c2.add_updater(lambda m: m.move_to(P3(-4.5 + (u.get_value() * 0.45 + 0.3) % L2, -1.9))
)
        LP = 1.45
        op1 = lambda: f_((u.get_value() * 0.45 + 1.0) % L1, L1)
        op2 = lambda: f_((u.get_value() * 0.45 + 0.3) % L2, L2)
        c1.add_updater(lambda m: opac_rel(m, op1()))
        c2.add_updater(lambda m: opac_rel(m, op2()))

        def setas():
            a1 = c1.get_center() + P3(0, 0.75)
            a2 = c2.get_center() + P3(0.75, 0)
            o1, o2 = op1(), op2()
            return VGroup(arrow(a1, a1 + P3(0, LP), color=MAG, width=8, tip=0.24).set_opacity(o1),
                          arrow(a2, a2 + P3(LP, 0), color=MAG, width=8, tip=0.24).set_opacity(o2))
        sp = always_redraw(setas)
        l1 = MathTex(r"\vec p_1", font_size=40, color=MAG)
        l1.add_updater(lambda m: m.next_to(c1.get_center() + P3(0, 0.75 + LP / 2), LEFT, buff=0.2).set_opacity(op1()))
        l2 = MathTex(r"\vec p_2", font_size=40, color=MAG)
        l2.add_updater(lambda m: m.next_to(c2.get_center() + P3(0.75 + LP / 2, 0), UP, buff=0.2).set_opacity(op2()))
        vv = VGroup(MathTex(r"20\ \mathrm{m/s}", font_size=30, color=VEL), MathTex(r"20\ \mathrm{m/s}", font_size=30, color=VEL))
        vv[0].add_updater(lambda m: m.next_to(c1, RIGHT, buff=0.25).set_opacity(op1()))
        vv[1].add_updater(lambda m: m.next_to(c2, DOWN, buff=0.12).set_opacity(op2()))
        clk = self.clk
        u.add_updater(lambda m: m.set_value(clk.get_value()))
        self.add(u)
        self.play(FadeIn(pista), FadeIn(ruas), FadeIn(rosa), run_time=0.7)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.6)
        self.add(sp)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(vv), run_time=0.6)
        m1 = MathTex(r"|\vec p_1|=|\vec p_2|", font_size=M_MAIN)
        self.pinta(m1, p=[1, 2, 3, 7, 8, 9])
        m2 = MathTex(r"\vec p_1\neq\vec p_2", font_size=M_MAIN)
        self.pinta(m2, p=[0, 1, 2, 5, 6, 7])
        t1 = txt("MESMO TAMANHO", T_SMALL, color=DIM)
        t2 = txt("DIREÇÕES DIFERENTES", T_SMALL, color=DIM)
        conta(m1, t1, m2, t2, topo=0.85, buff=0.32, x0=1.4)
        self.ate(0.36)
        self.play(ReplacementTransform(self.fixa(l1), VGroup(*m1[0][1:4])), ReplacementTransform(self.fixa(l2), VGroup(*m1[0][7:10])),
                  FadeIn(VGroup(m1[0][0], m1[0][4], m1[0][5], m1[0][6], m1[0][10])), run_time=1.1)
        self.add(m1)
        self.play(FadeIn(t1), run_time=0.4)
        # as duas setas vão para a mesma origem (comparação)
        o = P3(-2.4, -0.2)
        q1 = arrow(o, o + P3(0, LP), color=MAG, width=8, tip=0.24)
        q2 = arrow(o, o + P3(LP, 0), color=MAG, width=8, tip=0.24)
        self.ate(0.62)
        self.play(ReplacementTransform(self.fixa(sp[0]), q1), ReplacementTransform(self.fixa(sp[1]), q2), run_time=1.0)
        self.play(ReplacementTransform(self.fixa(l1), VGroup(*m2[0][0:3])), ReplacementTransform(self.fixa(l2), VGroup(*m2[0][5:8])), FadeIn(VGroup(*m2[0][3:5])), run_time=1.0)
        self.add(m2)
        self.play(FadeIn(t2), Indicate(VGroup(*m2[0][3:5]), color=WHITE_, scale_factor=1.5), run_time=0.8)
        self.ate(0.96)
        for m in (c1, c2, l1, l2, u, *vv):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in (pista, ruas, rosa, c1, c2, sp, l1, l2, vv, q1, q2, m1, m2, t1, t2)], run_time=0.5)
        self.remove(u)

    # ── T1-5 · componentes: v⃗ na origem, caixa tracejada até os eixos, vx, vy, vz descem para a conta ──────────────────
    def t1_5(self):
        self.an("T1-5")
        s = self.mot.fase
        self.mot.s = 5.2
        self.mot.corre()
        self.vv.set_value(1)
        self.pv.set_value(0)
        self.fv.set_value(0)
        self.play(FadeIn(self.cena3), FadeIn(self.ml), FadeIn(self.lv), run_time=0.8)
        s_ = 5.85                                  # vx, vy, vz > 0 aqui
        self.ir_para(s_, 1.6)
        V = 2.3 * KV * dr_(s_)
        X, Y, Z = V
        ov = arrow(pj(0, 0, 0), pjv(V), color=VEL, width=7, tip=0.22, z=11)
        lo = MathTex(r"\vec v", font_size=40, color=VEL).next_to(pjv(V), UR, buff=0.06)
        self.play(TransformFromCopy(self.Vv, ov), FadeIn(lo), run_time=1.0)
        cs = lambda a, b: DashedLine(pj(*a), pj(*b), dash_length=0.07).set_stroke(GEO, 1.6, opacity=0.8)
        box = VGroup(cs((X, Y, Z), (X, Y, 0)), cs((X, Y, 0), (X, 0, 0)), cs((X, Y, 0), (0, Y, 0)), cs((X, Y, Z), (0, Y, Z)),
                     cs((X, Y, Z), (X, 0, Z)), cs((X, 0, Z), (0, 0, Z)), cs((0, Y, Z), (0, 0, Z)), cs((X, 0, Z), (X, 0, 0)),
                     cs((0, Y, Z), (0, Y, 0))).set_z_index(6)
        self.ate(0.22)
        self.play(Create(box), run_time=1.3)
        comp = VGroup(Line(pj(0, 0, 0), pj(X, 0, 0)), Line(pj(0, 0, 0), pj(0, Y, 0)), Line(pj(0, 0, 0), pj(0, 0, Z))) \
            .set_stroke(VEL, 9).set_z_index(7)
        lx = MathTex("v_x", font_size=38, color=VEL).next_to(pj(X, 0, 0), DOWN, buff=0.12)
        ly = MathTex("v_y", font_size=38, color=VEL).next_to(pj(0.0, Y, 0), DOWN, buff=0.16)
        lz = MathTex("v_z", font_size=38, color=VEL).next_to(pj(0, 0, Z), LEFT, buff=0.14)
        for c, l in zip(comp, (lx, ly, lz)):
            self.play(Create(c), FadeIn(l), run_time=0.6)
        # CONTA: px = m vx · py = m vy · pz = m vz
        eqs = [MathTex(rf"p_{k}=m\,v_{k}", font_size=M_MAIN) for k in "xyz"]
        for e in eqs:
            self.pinta(e, p=[0, 1], v=[4, 5])
        conta(self.peg, *eqs, topo=2.2, buff=0.42)
        VGroup(*eqs).shift(DOWN * 0.15)
        self.ate(0.5)
        for e, l in zip(eqs, (lx, ly, lz)):
            self.play(TransformFromCopy(l, VGroup(*e[0][4:6])), FadeIn(VGroup(*e[0][0:4])), run_time=0.8)
            self.add(e)
        esc = legenda("TRÊS EQUAÇÕES ESCALARES NO LUGAR DE UMA VETORIAL", T_LAB)
        self.ate(0.85)
        self.play(FadeIn(esc), *[Indicate(e, color=WHITE_, scale_factor=1.05) for e in eqs], run_time=0.9)
        self.ate(0.97)
        self.comp5 = VGroup(ov, lo, box, comp, lx, ly, lz)
        self.eqs5, self.esc5 = VGroup(*eqs), esc

    # ── T1-6 · ΣF⃗ = dp⃗/dt e por componente; barras px, py, pz mudando na taxa de Fx, Fy, Fz ──────────────────────────
    def t1_6(self):
        self.an("T1-6")
        s = self.mot.fase
        self.play(FadeOut(self.comp5), FadeOut(self.eqs5), FadeOut(self.esc5), run_time=0.5)
        self.mot.corre()
        e2 = MathTex(r"\Sigma\vec F=\frac{d(m\vec v)}{dt}", font_size=M_MAIN)
        self.pinta(e2, F=[0, 1, 2], v=[7, 8])
        e3 = MathTex(r"\Sigma\vec F=\frac{d\vec p}{dt}", font_size=M_MAIN)
        self.pinta(e3, F=[0, 1, 2], p=[5, 6])
        conta(self.peg, e2, topo=2.2, buff=0.5, x0=1.3)
        e3.move_to(e2, aligned_edge=LEFT)
        self.play(Write(e2), self.fv.animate.set_value(1), FadeIn(self.lf), run_time=1.0)
        self.ate(0.14)
        self.play(TransformByGlyphMap(e2, e3, ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]), ([5, 6, 7, 8, 9], [5, 6]), ([10], [7]), ([11, 12], [8, 9])),
                  Indicate(VGroup(*self.pe[0][0:2]), color=MAG, scale_factor=1.3), run_time=1.3)
        bx = caixa(e3, WHITE_, buff=0.2)
        self.play(Create(bx), run_time=0.6)
        self.play(FadeOut(self.peg), VGroup(e3, bx).animate.shift(UP * (2.2 - bx.get_top()[1])), run_time=0.7)
        # PALCO: barras de px, py, pz (sinal incluído) com a taxa Fx, Fy, Fz em cima de cada uma
        bx0, y0, kb = 0.45, -0.65, 0.52
        xs = [bx0 - 0.36, bx0, bx0 + 0.36]
        moldura = placa(1.25, 4.6, P3(bx0, -0.55))
        zero = Line(P3(bx0 - 0.55, y0), P3(bx0 + 0.55, y0)).set_stroke(DIM, 1.5, opacity=0.7)
        nomes = VGroup(*[MathTex(rf"p_{k}", font_size=32, color=MAG).move_to(P3(x, -2.55)) for x, k in zip(xs, "xyz")])
        self.ov3 = ValueTracker(0.0)

        def barras():
            p = MASSA * dr_(s())
            f = d2r_(s())
            g = VGroup()
            o_ = self.ov3.get_value()
            for x, pc, fc in zip(xs, p, f):
                h = kb * pc
                g.add(Rectangle(width=0.26, height=max(abs(h), 0.01)).set_stroke(mix(MAG, 0.4), 1.5).set_fill(MAG, 0.85)
                      .move_to(P3(x, y0 + h / 2)).set_opacity(o_))
                topo = P3(x, y0 + h)
                g.add(arrow(topo, topo + P3(0, 0.32 * fc), color=FC, width=4, tip=0.12).set_opacity(o_))
            return g.set_z_index(8)
        br = always_redraw(barras)

        def fcomp():
            o_ = self.ov3.get_value()
            if o_ < 0.02:
                return VGroup()
            p = r_(s())
            f = KF * d2r_(s())
            g = VGroup()
            for k in range(3):
                e = np.zeros(3)
                e[k] = f[k]
                ar = arrow(pjv(p), pjv(p + e), color=FC, width=3.5, tip=0.13)
                if ar.has_points():
                    g.add(DashedVMobject(ar, num_dashes=6).set_opacity(0.85 * o_))
            return g.set_z_index(9)
        fc_ = always_redraw(fcomp)
        self.ate(0.36)
        self.add(br, fc_)
        self.play(FadeIn(moldura), Create(zero), FadeIn(nomes), self.ov3.animate.set_value(1), run_time=0.9)
        cs = [MathTex(rf"\Sigma F_{k}=\frac{{dp_{k}}}{{dt}}", font_size=M_REF) for k in "xyz"]
        for c in cs:
            self.pinta(c, F=[0, 1, 2], p=[5, 6])
        VGroup(*cs).arrange(DOWN, buff=0.16, aligned_edge=LEFT).next_to(bx, DOWN, buff=0.3).align_to(bx, LEFT)
        for c, x, k in zip(cs, xs, range(3)):
            self.ate(0.48 + 0.12 * k)
            sel = Rectangle(width=0.48, height=3.9).set_stroke(WHITE_, 1.5, opacity=0.6).move_to(P3(x, -0.6))
            sel.moldura = True
            self.play(TransformFromCopy(nomes[k], VGroup(*c[0][5:7])), FadeIn(VGroup(*c[0][0:5], *c[0][7:])), FadeIn(sel), run_time=0.9)
            self.add(c)
            self.play(FadeOut(sel), run_time=0.3)
        cada = legenda("CADA DIREÇÃO CUIDA DA SUA", T_LAB, color=WHITE_)
        self.ate(0.9)
        self.play(FadeIn(cada), run_time=0.5)
        self.ate(0.97)
        self.e3, self.bx3, self.cs6, self.bar6 = e3, bx, VGroup(*cs, cada), VGroup(moldura, zero, nomes, br, fc_)

    # ── T1-7 · a forma original de Newton; massa variável (foguete) ─────────────────────────────────────────────────
    def t1_7(self):
        self.an("T1-7")
        self.mot.para()
        g3 = [self.cena3, self.ml, *self.rotulos3(), self.bar6]
        self.play(*[FadeOut(m) for m in g3], FadeOut(self.cs6), run_time=0.6)
        for m in g3:
            for x in m.get_family():
                x.clear_updaters()
            self.remove(m)
        self.play(VGroup(self.e3, self.bx3).animate.move_to(P3(3.8, 1.2)), run_time=0.7)
        # PALCO: foguete soltando gás em loop (massa variável)
        fg = foguete(1.5).rotate(-PI / 2)
        bob = ValueTracker(0)
        clk = self.clk
        fg.add_updater(lambda m: m.move_to(P3(-2.4 + 0.18 * math.sin(clk.get_value() * 0.9), -0.3)))

        def gas():
            t = clk.get_value()
            g = VGroup()
            base = fg.get_left()
            for i in range(16):
                f = ((t * 0.9 + i / 16) % 1.0)
                y = 0.32 * math.sin(i * 2.3 + 1.7) * (0.3 + f)
                g.add(Dot(base + P3(-0.15 - 3.4 * f, y), radius=0.1 * (1 - 0.6 * f), color=GEO).set_opacity(0.85 * (1 - f)))
            return g
        gs = always_redraw(gas)
        mv = txt("MASSA VARIÁVEL", T_MAIN, bold=True).move_to(P3(-2.6, 1.55))
        luz = vinheta(P3(-2.6, -0.3), 2.6, GEO, soma=0.08)
        self.play(FadeIn(luz), FadeIn(fg, shift=0.3 * RIGHT), FadeIn(gs), run_time=0.9)
        s1 = self.selo("A FORMA ORIGINAL DE NEWTON", WHITE_)
        s2 = self.selo("REFERENCIAL INERCIAL", GEO)
        VGroup(s1, s2).arrange(DOWN, buff=0.3).next_to(self.bx3, DOWN, buff=0.45)
        self.play(FadeIn(s1, shift=0.1 * UP), run_time=0.6)
        self.ate(0.32)
        self.play(FadeIn(s2, shift=0.1 * UP), run_time=0.6)
        self.ate(0.5)
        self.play(FadeIn(mv, shift=0.1 * UP), Indicate(VGroup(*self.e3[0][4:7]), color=MAG, scale_factor=1.15), run_time=0.8)
        serie = legenda("ESSE CASO FICA PARA UM VÍDEO DESTA SÉRIE", T_LAB)
        self.ate(0.8)
        self.play(FadeIn(serie), run_time=0.6)
        self.ate(0.96)
        fg.clear_updaters()
        self.clear(rt=0.5)

    def fixa(self, m):
        """Cópia parada e opaca de um objeto que se move/apaga por updater (origem de um TransformFromCopy)."""
        c = m.copy()
        for x in c.get_family():
            x.clear_updaters()
        return opac_rel(c, 1.0 / max(1e-3, max([max(x.get_fill_opacity(), x.get_stroke_opacity()) for x in c.family_members_with_points()] or [1])))

    def selo(self, s, cor):
        t = txt(s, T_LAB, color=cor, bold=True)
        r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.6, height=t.height + 0.38).set_stroke(cor, 2).set_fill(opacity=0)
        r.moldura = True
        t.move_to(r)
        return VGroup(r, t)
