"""Lote PT1 (v5): T1 — DE ONDE VEM O MOMENTO. Uma partícula percorre uma curva lisa no espaço (projeção 2,5D desenhada no Manim,
alinhada por construção); v⃗ = dr⃗/dt e F⃗_res = m d²r⃗/dt² saem da própria curva, quadro a quadro.
v5 (polimento): a partícula PARA num ponto de pose em cada passo da álgebra (poses calculadas: ângulo v⃗·ΣF⃗ entre 70° e 110°, vetores
projetados ≥ 1,0 e ≥ 60% do real, nenhum cruzando eixo); ordem de desenho fixa (rastro 0, eixos 1, esfera 2, vetores 3, rótulos 4);
rótulos com contorno de fundo, além da ponta, girando ±60° se colidirem; vetores com haste 4 e ponta ≤ 35%; a⃗ = dv⃗/dt numa lupa;
transformações glifo a glifo sem morph; barras px, py, pz num painel próprio."""
from kit import *  # noqa: F401,F403
from sec_teoria import foguete

# ── espaço 2,5D: x para o observador (baixo-esquerda), y para a direita, z para cima (destro); cena em x ∈ [−6,6; 1,0] ─────────
ESC3 = 1.55
O3 = P3(-4.7, -2.17)
EX, EY, EZ = ESC3 * np.array([-0.62, -0.40, 0.0]), ESC3 * np.array([0.92, 0.12, 0.0]), ESC3 * np.array([0.0, 1.0, 0.0])


def pj(x, y, z):
    return O3 + x * EX + y * EY + z * EZ


def pjv(v):
    return pj(*v)


# curva r(s) = (X0 + A sen s, Y0 + B cos s, Z0 + C sen 2s), s = ω t: v ∝ dr/ds, F ∝ d²r/ds²
A_, B_, C_ = 1.0, 1.5, 0.45
X0, Y0, Z0 = 1.0, 2.05, 1.3
KV, KF, MASSA = 0.75, 0.62, 1.6
W_LOOP = 2 * PI / 12.0
S_POSE2, S_POSE3, S_POSE5 = 3.674, 3.94, 3.5          # poses (ver pose_info)


def r_(s):
    return np.array([X0 + A_ * math.sin(s), Y0 + B_ * math.cos(s), Z0 + C_ * math.sin(2 * s)])


def dr_(s):
    return np.array([A_ * math.cos(s), -B_ * math.sin(s), 2 * C_ * math.cos(2 * s)])


def d2r_(s):
    return np.array([-A_ * math.sin(s), -B_ * math.cos(s), -4 * C_ * math.sin(2 * s)])


EIXOS = [(pj(0, 0, 0), pj(2.0, 0, 0)), (pj(0, 0, 0), pj(0, 4.0, 0)), (pj(0, 0, 0), pj(0, 0, 2.8))]


def pose_info(s):
    """Ângulo entre v⃗ e ΣF⃗ projetados, comprimentos projetados e razão projetado/real."""
    P = pjv(r_(s))
    V, F = pjv(r_(s) + KV * dr_(s)) - P, pjv(r_(s) + KF * d2r_(s)) - P
    lv, lf = np.linalg.norm(V), np.linalg.norm(F)
    ang = math.degrees(math.acos(np.dot(V, F) / lv / lf))
    return ang, lv, lf, lv / (ESC3 * KV * np.linalg.norm(dr_(s))), lf / (ESC3 * KF * np.linalg.norm(d2r_(s)))


def esfera(r=0.21):
    c = Circle(radius=r).set_stroke(mix(GEO, 0.3), 1.6).set_fill([WHITE_, GEO, STEEL, "#3E4757"], 1.0)
    c.set_sheen_direction(DR)
    brilho = Circle(radius=r * 0.28).set_stroke(width=0).set_fill(WHITE_, 0.75).move_to(P3(-0.35 * r, 0.38 * r))
    return VGroup(c, brilho).set_z_index(2)


class LoteMomento(Base):
    def construct(self):
        self.setup_base(cap="DE ONDE VEM O MOMENTO")
        for s in (S_POSE2, S_POSE3, S_POSE5):
            a, lv, lf, rv, rf = pose_info(s)
            print(f"[pose] s = {s:.3f}: ângulo v·F = {a:.1f}°, |v| = {lv:.2f}, |F| = {lf:.2f} (projetado/real {rv:.2f}, {rf:.2f})")
        self.mot = Motor(self, s0=0.0, w=W_LOOP)
        self.qa = dict(rot=(9.0, ""), vet=(9.0, 0.0, ""))
        self.espaco()
        self.t1_1()
        self.t1_2()
        self.t1_3()
        self.t1_4()
        self.t1_5()
        self.t1_6()
        self.t1_7()
        self.fim()
        print(f"[qa-t1] quadros medidos: {self._nqa}")
        print(f"[qa-t1] pior folga de rótulo: {self.qa['rot'][0]:.2f} ({self.qa['rot'][1]}); "
              f"pior vetor: comprimento {self.qa['vet'][0]:.2f}, ponta/comprimento {self.qa['vet'][1]:.2f} ({self.qa['vet'][2]})")
        self.relatorio()

    # ── a cena: chão, eixos, partícula, rastro, sombra, vetores e rótulos (um só updater, ordem fixa) ──────────────────────
    def espaco(self):
        grade = VGroup()
        for x in np.arange(0, 2.01, 0.5):
            grade.add(Line(pj(x, 0, 0), pj(x, 3.8, 0)).set_stroke(DIM, 1, opacity=0.16))
        for y in np.arange(0, 3.81, 0.5):
            grade.add(Line(pj(0, y, 0), pj(2.0, y, 0)).set_stroke(DIM, 1, opacity=0.16))
        chao = Polygon(pj(0, 0, 0), pj(2.0, 0, 0), pj(2.0, 3.8, 0), pj(0, 3.8, 0)).set_stroke(width=0).set_fill(PANEL, 0.35)
        ex = arrow(pj(0, 0, 0), pj(2.0, 0, 0), color=GEO, width=3, tip=0.17, z=1)
        ey = arrow(pj(0, 0, 0), pj(0, 4.0, 0), color=GEO, width=3, tip=0.17, z=1)
        ez = arrow(pj(0, 0, 0), pj(0, 0, 2.8), color=GEO, width=3, tip=0.17, z=1)
        lx = rotulo("x", GEO, 36).next_to(pj(2.0, 0, 0), UP, buff=0.12).set_z_index(1)
        ly = rotulo("y", GEO, 36).next_to(pj(0, 4.0, 0), DOWN, buff=0.12).set_z_index(1)
        lz = rotulo("z", GEO, 36).next_to(pj(0, 0, 2.8), LEFT, buff=0.12).set_z_index(1)
        self.eixos3 = VGroup(chao, grade, ex, ey, ez, lx, ly, lz).set_z_index(1)
        s = self.mot.fase

        def rastro():
            g = VGroup()
            s0, n = s(), 34
            pts = [pjv(r_(s0 - 2.6 * (1 - k / n))) for k in range(n + 1)]
            for k in range(n):
                g.add(Line(pts[k], pts[k + 1]).set_stroke(GEO, 2.2, opacity=0.06 + 0.6 * (k / n) ** 1.6))
            return g.set_z_index(0)

        def sombra():
            p = r_(s())
            pe = pj(p[0], p[1], 0)
            return VGroup(DashedLine(pe, pjv(p), dash_length=0.06).set_stroke(DIM, 1.4, opacity=0.5),
                          Ellipse(width=0.34, height=0.14).set_stroke(width=0).set_fill(BACKGROUND_COLOR, 0.75).move_to(pe)).set_z_index(1)
        self.rastro, self.sombra = always_redraw(rastro), always_redraw(sombra)
        self.part = esfera()
        # vetores (crescimento 0..1 por ValueTracker; desenhados com opacidade 1) e rótulos
        self.gv, self.gf, self.gp = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.pk = ValueTracker(1.0 / MASSA)
        self._geo = {}
        cores = dict(v=VEL, f=FC, p=MAG)
        self.Hv, self.Hf, self.Hp = (always_redraw(lambda n=n: vet(*self._geo[n], cores[n], minimo=0.0) if n in self._geo else VMobject())
                                     for n in ("v", "f", "p"))
        self.lv, self.lf, self.lp = rotulo(r"\vec v", VEL), rotulo(r"\Sigma\vec F", FC), rotulo(r"\vec p", MAG)
        self.ov = {k: ValueTracker(0.0) for k in ("v", "f", "p")}
        self.motor = Mobject()
        self.motor.add_updater(lambda m: self.atualiza())
        for m in (self.part, self.lv, self.lf, self.lp):
            m.add_updater(lambda m_: None)          # conta como "em movimento": o Manim não congela uma cópia no fundo
        self.cena3 = VGroup(self.eixos3, self.rastro, self.sombra, self.part, self.Hp, self.Hv, self.Hf)

    def atualiza(self):
        self._nqa = getattr(self, "_nqa", 0) + 1
        s = self.mot.fase()
        p = r_(s)
        P = pjv(p)
        self.part.move_to(P)
        ocup = [(P[0] - 0.24, P[1] - 0.24, P[0] + 0.24, P[1] + 0.24)]
        segs = list(EIXOS)
        itens = (("p", self.gp, MAG, lambda: self.pk.get_value() * MASSA * KV * dr_(s), self.Hp, self.lp),
                 ("v", self.gv, VEL, lambda: KV * dr_(s), self.Hv, self.lv),
                 ("f", self.gf, FC, lambda: KF * d2r_(s), self.Hf, self.lf))
        pontas = {}
        self._geo = {}
        for nome, g, cor, vec, H, lab in itens:
            k = g.get_value()
            if k <= 1e-3:
                continue
            tip = pjv(p + k * vec())
            if np.linalg.norm(tip - P) >= (0.9 if k > 0.999 else 0.05):
                self._geo[nome] = (P, tip)
                pontas[nome] = tip
                segs.append((P, tip))
                L = np.linalg.norm(tip - P)
                if k > 0.999 and L < self.qa["vet"][0]:
                    self.qa["vet"] = (L, min(0.18, 0.35 * L) / L, f"{nome} em {self.nq / FPS:.1f}s")
        for nome, g, cor, vec, H, lab in itens:
            if nome in pontas and self.ov[nome].get_value() > 0.01:
                lab.set_opacity(self.ov[nome].get_value())
                outros = [sg for sg in segs if not (np.allclose(sg[1], pontas[nome]))]
                cx = coloca(lab, pontas[nome], pontas[nome] - P, ocup, outros)
                folga = min([self._dist(cx, o) for o in ocup[:-1]] + [9.0])
                if folga < self.qa["rot"][0] and self.ov[nome].get_value() > 0.99:
                    self.qa["rot"] = (folga, f"{nome} em {self.nq / FPS:.1f}s")
            else:
                lab.set_opacity(0.0)

    @staticmethod
    def _dist(a, b):
        dx = max(b[0] - a[2], a[0] - b[2], 0.0)
        dy = max(b[1] - a[3], a[1] - b[3], 0.0)
        return math.hypot(dx, dy) if (dx > 0 or dy > 0) else -min(a[2] - b[0], b[2] - a[0], a[3] - b[1], b[3] - a[1])

    def rotulos3(self):
        return [self.lv, self.lf, self.lp]

    def ir_para(self, alvo, rt=0.8):
        """Desacelera até parar na fase `alvo` (para a frente), com velocidade contínua na entrada."""
        self.mot.para()
        s0 = self.mot.s
        while alvo < s0:
            alvo += 2 * PI
        self.play(UpdateFromAlphaFunc(Mobject(), lambda m, a: setattr(self.mot, "s", s0 + (alvo - s0) * (1 - (1 - a) ** 2))),
                  run_time=rt, rate_func=linear)
        self.mot.s = alvo

    def vai_para(self, alvo, rt=1.2):
        """Transição entre poses: parte do repouso e para no alvo (smooth)."""
        self.mot.para()
        s0 = self.mot.s
        while alvo < s0:
            alvo += 2 * PI
        self.play(UpdateFromAlphaFunc(Mobject(), lambda m, a: setattr(self.mot, "s", s0 + (alvo - s0) * smooth(a))), run_time=rt, rate_func=linear)
        self.mot.s = alvo

    def pinta(self, m, F=(), a=(), v=(), p=(), J=()):
        for i, g in enumerate(m[0]):
            g._dono = f"{m.get_tex_string()[:14]}#{i}"
        for idx, c in ((F, FC), (a, GEO), (v, VEL), (p, MAG), (J, JC)):
            for i in idx:
                m[0][i].set_color(c)
        return m

    # ── T1-1 · a segunda lei numa trajetória qualquer (uma volta livre e para na pose) ──────────────────────────────────
    def t1_1(self):
        self.an("T1-1")
        self.add(self.motor)
        sl = txt("SEGUNDA LEI DE NEWTON", T_LAB, color=DIM).move_to(P3(0, 2.3)).align_to(P3(1.3, 0), LEFT)
        # v6: a partícula e a curva entram junto com o selo (nada de selo sozinho na tela)
        t_dec = 0.9 * dur("T1-1") - 1.0                                  # quanto falta até a desaceleração (s)
        self.mot.s = S_POSE2 - W_LOOP * 0.4 - W_LOOP * t_dec
        self.mot.corre()
        self.add(self.rastro, self.sombra, self.Hp, self.Hv, self.Hf, self.lv, self.lf, self.lp)
        self.play(FadeIn(self.eixos3[0]), Create(self.eixos3[1]), *[GrowArrow(a) for a in self.eixos3[2:5]], FadeIn(self.eixos3[5:]),
                  FadeIn(sl, shift=0.1 * UP), FadeIn(self.part, scale=0.5), run_time=1.0)
        ml = rotulo("m", WHITE_, 38)
        ml.add_updater(lambda m: m.next_to(self.part, DL, buff=0.06))
        self.play(FadeIn(ml), run_time=0.5)
        self.ate(0.28)
        self.play(self.gv.animate.set_value(1), self.ov["v"].animate.set_value(1), run_time=0.8)
        self.ate(0.45)
        self.play(self.gf.animate.set_value(1), self.ov["f"].animate.set_value(1), run_time=0.8)
        e0 = MathTex(r"\Sigma\vec F=m\,\vec a", font_size=M_MAIN)
        self.pinta(e0, F=[0, 1, 2], a=[5, 6])
        conta(e0, topo=1.75, x0=1.3)
        self.ate(0.62)
        ml.clear_updaters()
        self.play(ReplacementTransform(fixa(self.lf), VGroup(*e0[0][0:3])), ReplacementTransform(ml, e0[0][4]),
                  FadeIn(e0[0][3]), Write(VGroup(*e0[0][5:7])), run_time=1.3)
        self.consolida(e0)
        self.ate(0.9)
        self.ir_para(S_POSE2, 0.8)
        self.e0, self.sl = e0, sl

    # ── T1-2 · lupa: v⃗(t) e v⃗(t+Δt) da mesma origem, Δv⃗ → dv⃗ paralelo a ΣF⃗; a⃗ = dv⃗/dt vai para a conta; o m entra ─────────
    def t1_2(self):
        self.an("T1-2")
        s1 = S_POSE2
        C = P3(-0.95, -0.25)
        R = 1.15
        lupa = Circle(radius=R).set_stroke(GEO, 2).set_fill(BACKGROUND_COLOR, 0.96).move_to(C).set_z_index(5)
        fio = Line(self.part.get_center(), C + R * (self.part.get_center() - C) / np.linalg.norm(self.part.get_center() - C)) \
            .set_stroke(GEO, 1.2, opacity=0.6).set_z_index(5)
        tit = txt("LUPA", 16, color=DIM).next_to(lupa, UP, buff=0.06).set_z_index(6)
        Oi = C + P3(-0.72, -0.45)
        P1 = pjv(r_(s1))
        V1 = pjv(r_(s1) + KV * dr_(s1)) - P1
        esc = 1.35 / np.linalg.norm(V1)
        Fd = pjv(r_(s1) + KF * d2r_(s1)) - P1
        Fd = Fd / np.linalg.norm(Fd)
        ds = ValueTracker(0.9)

        def dentro():
            V2 = pjv(r_(s1 + ds.get_value()) + KV * dr_(s1 + ds.get_value())) - pjv(r_(s1 + ds.get_value()))
            a1, a2 = Oi + esc * V1, Oi + esc * V2
            g = VGroup(vet(Oi, a1, VEL, minimo=0.3), vet(Oi, a2, mix(VEL, 0.45), minimo=0.3))
            dv = a2 - a1
            n = np.linalg.norm(dv)
            u = dv / n if n > 1e-6 else Fd
            g.add(vet(a1, a1 + u * max(0.55, min(n, 1.0)), WHITE_, minimo=0.3, z=7))
            g.add(DashedLine(a1 - Fd * 0.3, a1 + Fd * 1.1, dash_length=0.07).set_stroke(FC, 1.6, opacity=0.6))
            return g.set_z_index(7)
        ins = always_redraw(dentro)
        lt1 = rotulo(r"\vec v(t)", VEL, 26).set_z_index(8)
        lt1.move_to(Oi + esc * V1 * 0.5 + P3(-0.2, 0.22))
        ldv = rotulo(r"\Delta\vec v", WHITE_, 30).set_z_index(8)
        ldv.add_updater(lambda m: m.move_to(Oi + esc * V1 + P3(0.42, -0.32)))
        self.play(Create(fio), FadeIn(lupa), FadeIn(tit), run_time=0.6)
        self.play(FadeIn(ins), FadeIn(lt1), FadeIn(ldv), run_time=0.6)
        lim = MathTex(r"\Delta t\to 0", font_size=34, color=DIM).next_to(lupa, DOWN, buff=0.12).set_z_index(6)
        self.ate(0.16)
        self.play(FadeIn(lim), ds.animate.set_value(0.04), run_time=2.6, rate_func=smooth)
        ldv2 = rotulo(r"d\vec v", WHITE_, 30).set_z_index(8).move_to(ldv)
        ldv.clear_updaters()
        self.play(ReplacementTransform(ldv, ldv2), run_time=0.5)
        # a⃗ = dv⃗/dt sai da lupa para a conta
        ea = MathTex(r"\vec a=\frac{d\vec v}{dt}", font_size=M_MID)
        self.pinta(ea, a=[0, 1], v=[4, 5])
        self.play(FadeOut(self.sl), self.e0.animate.align_to(P3(0, 2.15), UP), run_time=0.5)
        ea.next_to(self.e0, DOWN, buff=0.45).align_to(self.e0, LEFT)
        self.ate(0.36)
        self.play(ReplacementTransform(ldv2, VGroup(*ea[0][3:6])), FadeIn(VGroup(*ea[0][0:3], *ea[0][6:9])), run_time=1.1)
        self.consolida(ea)
        # ΣF⃗ = m a⃗ → ΣF⃗ = m dv⃗/dt (a⃗ sai; a fração chega da linha de a⃗)
        e1 = MathTex(r"\Sigma\vec F=m\,\frac{d\vec v}{dt}", font_size=M_MAIN)
        self.pinta(e1, F=[0, 1, 2], v=[6, 7])
        e1.move_to(self.e0, aligned_edge=LEFT)
        self.ate(0.5)
        self.play(FadeOut(VGroup(self.e0[0][5], self.e0[0][6])), FadeOut(VGroup(*ea[0][0:3])), run_time=0.45)
        self.play(*[ReplacementTransform(self.e0[0][i], e1[0][i]) for i in range(5)],
                  *[ReplacementTransform(ea[0][i], e1[0][j]) for i, j in zip(range(3, 9), range(5, 11))], run_time=0.9)
        self.remove(self.e0, *self.e0[0], ea, *ea[0])
        self.consolida(e1)
        self.play(FadeOut(ins), FadeOut(lupa), FadeOut(fio), FadeOut(tit), FadeOut(lim), FadeOut(lt1), run_time=0.5)
        ins.clear_updaters()
        # o m viaja inteiro para dentro da derivada (massa constante)
        e2 = MathTex(r"\Sigma\vec F=\frac{d(m\vec v)}{dt}", font_size=M_MAIN)
        self.pinta(e2, F=[0, 1, 2], v=[7, 8])
        e2.move_to(e1, aligned_edge=LEFT)
        mc = txt("MASSA CONSTANTE", T_SMALL, color=GEO, bold=True)
        mcx = VGroup(RoundedRectangle(corner_radius=0.1, width=mc.width + 0.4, height=mc.height + 0.3).set_stroke(GEO, 1.6), mc)
        mc.move_to(mcx[0])
        mcx[0].moldura = True
        mcx.next_to(e2, DOWN, buff=0.4).align_to(e2, LEFT)
        self.ate(0.7)
        self.play(FadeIn(mcx, shift=0.1 * UP), run_time=0.5)
        self.glifos(e1, e2, pares=[(0, 0), (1, 1), (2, 2), (3, 3), (5, 4), (6, 7), (7, 8), (8, 10), (9, 11), (10, 12)],
                    mover=[(4, 6)], entra=[5, 9], rt=1.4)
        self.orfaos("T1-2 m na derivada")
        self.ate(0.92)
        self.play(Indicate(VGroup(*e2[0][4:10]), color=WHITE_, scale_factor=1.08), run_time=0.8)
        self.e2, self.mcx = e2, mcx

    # ── T1-3 · p⃗ = m v⃗: a seta magenta nasce da violeta, esticada pelo fator m (partícula na pose) ─────────────────────────
    def t1_3(self):
        self.an("T1-3")
        e2 = self.e2
        self.vai_para(S_POSE3, 1.0)
        pe = MathTex(r"\vec p=m\,\vec v", font_size=M_MAIN)
        self.pinta(pe, p=[0, 1], v=[4, 5])
        nome = txt("MOMENTO LINEAR", T_MAIN, color=MAG, bold=True)
        nome2 = txt("OU QUANTIDADE DE MOVIMENTO", T_SMALL, color=DIM)
        un = MathTex(r"[\,p\,]=\mathrm{kg\cdot m/s}", font_size=M_REF, color=MAG)
        self.play(FadeOut(self.mcx), run_time=0.3)
        conta(e2, pe, nome, nome2, un, topo=2.15, buff=0.36, x0=1.3)
        pe.shift(DOWN * 0.15)
        hl = caixa(VGroup(*e2[0][5:10]), MAG, buff=0.08, w=2.2)
        self.play(Create(hl), run_time=0.6)
        self.gp.set_value(1.0)
        self.play(self.gf.animate.set_value(0.0), self.ov["f"].animate.set_value(0.0), self.ov["p"].animate.set_value(1), run_time=0.6)
        self.play(self.pk.animate.set_value(1.0), run_time=1.3)
        self.ate(0.22)
        self.play(ReplacementTransform(fixa(self.lp), VGroup(*pe[0][0:2])), FadeIn(pe[0][2]),
                  *[ReplacementTransform(e2[0][i].copy(), pe[0][j]) for i, j in ((6, 3), (7, 4), (8, 5))], run_time=1.3)
        self.consolida(pe)
        bx = caixa(pe, MAG, buff=0.18)
        self.play(Create(bx), FadeIn(nome, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(nome2), run_time=0.5)
        self.ate(0.43)                                   # v6 (G5): a seta p⃗ acende enquanto a fala explica o nome
        self.play(Indicate(self.lp, color=WHITE_, scale_factor=1.3), Indicate(bx, color=WHITE_, scale_factor=1.04), run_time=0.9)
        self.ate(0.58)
        self.play(Indicate(VGroup(self.lp, self.lv), color=WHITE_, scale_factor=1.2), run_time=0.9)
        self.ate(0.8)
        self.play(Write(un), run_time=0.9)
        self.orfaos("T1-3")
        self.ate(0.97)
        self.peg = VGroup(pe, bx)
        self.nomes, self.un, self.hl = VGroup(nome, nome2), un, hl

    # ── T1-4 · vetor de verdade: dois carros iguais, norte e leste (crossfade direto da cena 3D) ──────────────────────────
    def t1_4(self):
        self.an("T1-4")
        pista = placa(7.2, 5.3, P3(-2.95, -0.3))
        rua_v = Rectangle(width=1.3, height=5.0).set_stroke(DIM, 1.2, opacity=0.5).set_fill("#151B2B", 1).move_to(P3(-5.75, -0.3))
        rua_h = Rectangle(width=4.6, height=1.3).set_stroke(DIM, 1.2, opacity=0.5).set_fill("#151B2B", 1).move_to(P3(-1.75, -2.05))
        faixa_v = DashedLine(P3(-5.75, -2.75), P3(-5.75, 2.15), dash_length=0.2).set_stroke(DIM, 1.5, opacity=0.4)
        faixa_h = DashedLine(P3(-4.0, -2.05), P3(0.5, -2.05), dash_length=0.2).set_stroke(DIM, 1.5, opacity=0.4)
        ruas = VGroup(rua_v, rua_h, faixa_v, faixa_h)               # as estradas não se encontram (vão de 0,6 entre elas)
        rosa = VGroup(arrow(P3(-1.0, 0.75), P3(-1.0, 1.55), color=DIM, width=3, tip=0.15), arrow(P3(-1.0, 0.75), P3(-0.2, 0.75), color=DIM, width=3, tip=0.15),
                      txt("N", 20, color=DIM).move_to(P3(-1.0, 1.8)), txt("L", 20, color=DIM).move_to(P3(0.05, 0.75)))
        u = ValueTracker(0.0)
        c1 = opac_rel(Carro(1.25, 0.66, GEO, ang=PI / 2), 1.0)
        c2 = opac_rel(Carro(1.25, 0.66, GEO, ang=0), 1.0)
        L1, L2 = 2.5, 1.9

        def f_(x, L):
            return min(1.0, x / 0.35, (L - x) / 0.35)
        x1 = lambda: (u.get_value() * 0.45 + 1.0) % L1
        x2 = lambda: (u.get_value() * 0.45 + 0.3) % L2
        c1.add_updater(lambda m: opac_rel(m.move_to(P3(-5.75, -2.3 + x1())), f_(x1(), L1)))
        c2.add_updater(lambda m: opac_rel(m.move_to(P3(-3.5 + x2(), -2.05)), f_(x2(), L2)))
        LP = 1.45
        op1, op2 = (lambda: f_(x1(), L1)), (lambda: f_(x2(), L2))

        def setas():
            a1 = c1.get_center() + P3(0, 0.75)
            a2 = c2.get_center() + P3(0.75, 0)
            return VGroup(opac_rel(vet(a1, a1 + P3(0, LP), MAG, w=7, tip=0.24, z=5), op1()), opac_rel(vet(a2, a2 + P3(LP, 0), MAG, w=7, tip=0.24, z=5), op2()))
        sp = always_redraw(setas)
        l1 = rotulo(r"\vec p_1", MAG, 40)
        l1.add_updater(lambda m: m.next_to(c1.get_center() + P3(0, 0.75 + LP / 2), RIGHT, buff=0.22).set_opacity(op1()))
        l2 = rotulo(r"\vec p_2", MAG, 40)
        l2.add_updater(lambda m: m.next_to(c2.get_center() + P3(0.75 + LP / 2, 0), UP, buff=0.22).set_opacity(op2()))
        vv = VGroup(rotulo(r"20\ \mathrm{m/s}", VEL, 28), rotulo(r"20\ \mathrm{m/s}", VEL, 28))
        vv[0].add_updater(lambda m: m.next_to(c1, LEFT, buff=0.12).set_opacity(op1()))
        vv[1].add_updater(lambda m: m.next_to(c2, DOWN, buff=0.12).set_opacity(op2()))
        clk = self.clk
        u.add_updater(lambda m: m.set_value(clk.get_value()))
        self.add(u)
        # crossfade: a cena 3D sai enquanto o painel dos carros entra
        self.mot.para()
        tudo3 = [self.cena3, *self.rotulos3()]
        self.play(*[FadeOut(m) for m in tudo3], FadeOut(self.e2), FadeOut(self.hl), FadeOut(self.nomes), FadeOut(self.un),
                  self.peg.animate.move_to(P3(3.9, 1.85)), FadeIn(pista), FadeIn(ruas), FadeIn(rosa), run_time=0.8)
        self.remove(*tudo3, self.motor)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.5)
        self.add(sp)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(vv), run_time=0.6)
        m1 = MathTex(r"|\vec p_1|=|\vec p_2|", font_size=M_MAIN)
        self.pinta(m1, p=[1, 2, 3, 7, 8, 9])
        m2 = MathTex(r"\vec p_1\neq\vec p_2", font_size=M_MAIN)
        self.pinta(m2, p=[0, 1, 2, 5, 6, 7])
        t1 = txt("MESMO TAMANHO", T_SMALL, color=DIM)
        t2 = txt("DIREÇÕES DIFERENTES", T_SMALL, color=DIM)
        conta(m1, t1, m2, t2, topo=0.85, buff=0.32, x0=1.5)
        self.ate(0.36)
        self.play(ReplacementTransform(fixa(l1), VGroup(*m1[0][1:4])), ReplacementTransform(fixa(l2), VGroup(*m1[0][7:10])),
                  FadeIn(VGroup(m1[0][0], m1[0][4], m1[0][5], m1[0][6], m1[0][10])), run_time=1.1)
        self.consolida(m1)
        self.play(FadeIn(t1), run_time=0.4)
        # as mesmas setas copiadas para uma origem comum (sem rótulos novos)
        o = P3(-2.3, -0.3)
        q1 = vet(o, o + P3(0, LP), MAG, w=7, tip=0.24, z=5)
        q2 = vet(o, o + P3(LP, 0), MAG, w=7, tip=0.24, z=5)
        self.ate(0.62)
        self.play(ReplacementTransform(fixa(sp[0]), q1), ReplacementTransform(fixa(sp[1]), q2), run_time=1.0)
        self.play(ReplacementTransform(fixa(l1), VGroup(*m2[0][0:3])), ReplacementTransform(fixa(l2), VGroup(*m2[0][5:8])),
                  FadeIn(VGroup(*m2[0][3:5])), run_time=1.0)
        self.consolida(m2)
        self.play(FadeIn(t2), Indicate(VGroup(*m2[0][3:5]), color=WHITE_, scale_factor=1.4), run_time=0.8)
        self.orfaos("T1-4")
        self.ate(0.93)
        for m in (c1, c2, l1, l2, u, *vv):
            m.clear_updaters()
        sp.clear_updaters()
        self.carros = [pista, ruas, rosa, c1, c2, sp, l1, l2, vv, q1, q2, m1, m2, t1, t2]
        self.remove(u)

    # ── T1-5 · componentes: v⃗ copiado na origem (≥ 1,8), caixa tracejada, vx, vy, vz descem para a conta ───────────────────
    def t1_5(self):
        self.an("T1-5")
        self.mot.s = S_POSE5
        self.mot.para()
        self.gv.set_value(1)
        self.gp.set_value(0)
        self.gf.set_value(0)
        self.ov["v"].set_value(1)
        self.ov["p"].set_value(0)
        self.ov["f"].set_value(0)
        self.add(self.motor)
        self.atualiza()
        self.add(self.lf, self.lp)
        self.play(*[FadeOut(m) for m in self.carros], FadeIn(self.cena3), FadeIn(self.lv), run_time=0.8)
        d = dr_(S_POSE5)
        k = 2.0 / np.linalg.norm(pjv(d) - O3)
        V = k * d
        X, Y, Z = V
        ov = vet(pj(0, 0, 0), pjv(V), VEL, w=5, tip=0.2)
        lo = rotulo(r"\vec v", VEL, 38).next_to(pjv(V), UR, buff=0.06)
        cl = VGroup(txt("CÓPIA DE", 21, color=GEO), rotulo(r"\vec v", GEO, 30), txt("NA ORIGEM", 21, color=GEO)).arrange(RIGHT, buff=0.1)
        cl.next_to(pjv(V), RIGHT, buff=0.45).shift(DOWN * 0.35)
        self.play(ReplacementTransform(fixa(self.Hv), ov), FadeIn(lo), FadeIn(cl), run_time=1.0)
        cs = lambda a, b: DashedLine(pj(*a), pj(*b), dash_length=0.08).set_stroke(GEO, 1.6, opacity=0.6)
        box = VGroup(cs((X, Y, Z), (X, Y, 0)), cs((X, Y, 0), (X, 0, 0)), cs((X, Y, 0), (0, Y, 0)), cs((X, Y, Z), (0, Y, Z)),
                     cs((X, Y, Z), (X, 0, Z)), cs((X, 0, Z), (0, 0, Z)), cs((0, Y, Z), (0, 0, Z)), cs((X, 0, Z), (X, 0, 0)),
                     cs((0, Y, Z), (0, Y, 0))).set_z_index(2)
        self.ate(0.22)
        self.play(Create(box), run_time=1.2)
        comp = VGroup(Line(pj(0, 0, 0), pj(X, 0, 0)), Line(pj(0, 0, 0), pj(0, Y, 0)), Line(pj(0, 0, 0), pj(0, 0, Z))) \
            .set_stroke(VEL, 5).set_z_index(3)
        lx, ly, lz = rotulo("v_x", VEL, 36), rotulo("v_y", VEL, 36), rotulo("v_z", VEL, 36)
        oc = [caixa_de(lo), caixa_de(cl)]
        for lab, c in zip((lx, ly, lz), comp):
            a, b = c.get_start(), c.get_end()
            nrm = np.array([-(b - a)[1], (b - a)[0], 0.0])
            coloca(lab, (a + b) / 2, nrm if nrm[1] <= 0 else -nrm, oc, list(EIXOS), gap=0.14)
        for c, l in zip(comp, (lx, ly, lz)):
            self.play(Create(c), FadeIn(l), run_time=0.6)
        eqs = [MathTex(rf"p_{k}=m\,v_{k}", font_size=M_MAIN) for k in "xyz"]
        for e in eqs:
            self.pinta(e, p=[0, 1], v=[4, 5])
        conta(self.peg, *eqs, topo=2.2, buff=0.42, x0=1.3)
        VGroup(*eqs).shift(DOWN * 0.15)
        self.ate(0.5)
        for e, l in zip(eqs, (lx, ly, lz)):                          # termo a termo (G2): p_k =, m, e o v_k que desce do desenho
            self.play(FadeIn(VGroup(*e[0][0:3])), run_time=0.35)
            self.play(FadeIn(e[0][3]), run_time=0.25)
            self.play(ReplacementTransform(fixa(l), VGroup(*e[0][4:6])), run_time=0.6)
            self.consolida(e)
        esc = legenda("TRÊS EQUAÇÕES ESCALARES NO LUGAR DE UMA VETORIAL", T_LAB)
        self.ate(0.85)
        self.play(FadeIn(esc), *[Indicate(e, color=WHITE_, scale_factor=1.05) for e in eqs], run_time=0.9)
        self.orfaos("T1-5")
        self.ate(0.97)
        self.comp5 = VGroup(ov, lo, cl, box, comp, lx, ly, lz)
        self.eqs5, self.esc5 = VGroup(*eqs), esc

    # ── T1-6 · ΣF⃗ = dp⃗/dt e por componente; painel das barras px, py, pz (partícula devagar, só ΣF⃗ nela) ──────────────────
    def t1_6(self):
        self.an("T1-6")
        s = self.mot.fase
        self.play(FadeOut(self.comp5), FadeOut(self.eqs5), FadeOut(self.esc5), self.gv.animate.set_value(0), self.ov["v"].animate.set_value(0),
                  run_time=0.5)
        self.gf.set_value(1)
        self.ov["f"].set_value(1)
        self.mot.corre(W_LOOP / 2)
        X0C = 3.75                                               # a CONTA anda para a direita: o painel das barras fica entre a cena e ela
        e2 = MathTex(r"\Sigma\vec F=\frac{d(m\vec v)}{dt}", font_size=52)
        self.pinta(e2, F=[0, 1, 2], v=[7, 8])
        e3 = MathTex(r"\Sigma\vec F=\frac{d\vec p}{dt}", font_size=52)
        self.pinta(e3, F=[0, 1, 2], p=[5, 6])
        self.play(self.peg.animate.scale(0.8).move_to(P3(0, 2.0)).align_to(P3(X0C, 0), LEFT), run_time=0.6)
        e2.next_to(self.peg, DOWN, buff=0.45).align_to(P3(X0C, 0), LEFT)
        e3.move_to(e2, aligned_edge=LEFT)
        self.play(Write(e2), FadeIn(self.lf), run_time=1.0)
        self.ate(0.14)
        self.glifos(e2, e3, pares=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (10, 7), (11, 8), (12, 9)], entra=[5, 6], sai=[5, 6, 7, 8, 9],
                    extras=[Indicate(VGroup(*self.peg[0][0][0:2]), color=MAG, scale_factor=1.3)], rt=1.3)
        bx = caixa(e3, WHITE_, buff=0.2)
        self.play(Create(bx), run_time=0.5)
        self.play(FadeOut(self.peg), VGroup(e3, bx).animate.shift(UP * (2.2 - bx.get_top()[1])), run_time=0.6)
        # painel das barras: à direita da cena, ≥ 0,3 do eixo y e da caixa da conta
        PX0, PX1 = 1.3, X0C - 0.55
        pan = placa(PX1 - PX0, 3.55, P3((PX0 + PX1) / 2, 0.55))
        y0, kb = 0.35, 0.5
        larg, vao = 0.35, 0.36                                   # a seta azul de cada barra mora no vão, à direita dela
        xs = [PX0 + 0.13 + larg / 2 + k * (larg + vao) for k in range(3)]
        zero = Line(P3(PX0 + 0.1, y0), P3(PX1 - 0.1, y0)).set_stroke(DIM, 1.6, opacity=0.8)
        zl = txt("0", 20, color=DIM).next_to(zero, LEFT, buff=0.06)
        nomes = VGroup(*[rotulo(rf"p_{k}", MAG, 36).move_to(P3(x, -0.95)) for x, k in zip(xs, "xyz")])     # embaixo de cada barra
        ob = ValueTracker(0.0)

        def barras():
            p = MASSA * dr_(s())
            f = d2r_(s())
            g = VGroup()
            for x, pc, fc in zip(xs, p, f):
                h = kb * pc
                g.add(Rectangle(width=larg, height=max(abs(h), 0.01)).set_stroke(mix(MAG, 0.4), 1.5).set_fill(MAG, 0.85)
                      .move_to(P3(x, y0 + h / 2)).set_opacity(ob.get_value()))
                xa = x + larg / 2 + 0.1
                topo = P3(xa, y0 + h)
                g.add(vet(topo, topo + P3(0, 0.36 * fc), FC, w=4, tip=0.12, minimo=0.12).set_opacity(ob.get_value()))
            return g.set_z_index(3)
        br = always_redraw(barras)
        self.ate(0.34)
        self.add(br)
        self.play(FadeIn(pan), Create(zero), FadeIn(zl), FadeIn(nomes), ob.animate.set_value(1), run_time=0.9)
        cs = [MathTex(rf"\Sigma F_{k}=\frac{{dp_{k}}}{{dt}}", font_size=42) for k in "xyz"]
        for c in cs:
            self.pinta(c, F=[0, 1, 2], p=[5, 6])
        VGroup(*cs).arrange(DOWN, buff=0.16, aligned_edge=LEFT).next_to(bx, DOWN, buff=0.3).align_to(bx, LEFT)
        for c, x, k in zip(cs, xs, range(3)):
            self.ate(0.48 + 0.12 * k)
            sel = Rectangle(width=larg + 0.26, height=3.3).set_stroke(WHITE_, 1.5, opacity=0.7).move_to(P3(x + 0.08, 0.55))
            sel.moldura = True
            self.play(ReplacementTransform(fixa(nomes[k]), VGroup(*c[0][5:7])), FadeIn(VGroup(*c[0][0:5], *c[0][7:])), FadeIn(sel),
                      Indicate(nomes[k], color=WHITE_, scale_factor=1.2), run_time=0.9)
            self.consolida(c)
            self.play(FadeOut(sel), run_time=0.3)
        cada = legenda("CADA DIREÇÃO CUIDA DA SUA", T_LAB, color=WHITE_)
        self.ate(0.9)
        self.play(FadeIn(cada), run_time=0.5)
        self.orfaos("T1-6")
        self.ate(0.97)
        self.e3, self.bx3, self.cs6, self.bar6 = e3, bx, VGroup(*cs, cada), VGroup(pan, zero, zl, nomes, br)

    # ── T1-7 · a forma original de Newton; massa variável (foguete andando devagar para a direita) ─────────────────────────
    def t1_7(self):
        self.an("T1-7")
        self.mot.para()
        g3 = [self.cena3, *self.rotulos3(), self.bar6]
        clk = self.clk
        t0 = clk.get_value()
        fg = foguete(1.5).rotate(-PI / 2)
        fg.add_updater(lambda m: m.move_to(P3(-4.6 + 0.16 * (clk.get_value() - t0), -0.3)))

        def gas():
            t = clk.get_value()
            g = VGroup()
            base = fg.get_left()
            for i in range(16):
                f = ((t * 0.9 + i / 16) % 1.0)
                y = 0.32 * math.sin(i * 2.3 + 1.7) * (0.3 + f)
                g.add(Dot(base + P3(-0.15 - 2.4 * f, y), radius=0.1 * (1 - 0.6 * f), color=GEO).set_opacity(0.85 * (1 - f)))
            return g
        gs = always_redraw(gas)
        self.play(*[FadeOut(m) for m in g3], FadeOut(self.cs6), VGroup(self.e3, self.bx3).animate.move_to(P3(3.9, 1.2)),
                  FadeIn(fg, shift=0.3 * RIGHT), FadeIn(gs), run_time=0.8)
        for m in g3:
            for x in m.get_family():
                x.clear_updaters()
            self.remove(m)
        self.remove(self.motor)
        s1 = self.selo("A FORMA ORIGINAL DE NEWTON", WHITE_)
        s2 = self.selo("REFERENCIAL INERCIAL", GEO)
        VGroup(s1, s2).arrange(DOWN, buff=0.3).next_to(self.bx3, DOWN, buff=0.45)
        self.play(FadeIn(s1, shift=0.1 * UP), run_time=0.6)
        self.ate(0.32)
        self.play(FadeIn(s2, shift=0.1 * UP), run_time=0.6)
        mv = txt("MASSA VARIÁVEL", T_MAIN, bold=True).move_to(P3(-2.6, 1.55))
        self.ate(0.5)
        self.play(FadeIn(mv, shift=0.1 * UP), Indicate(VGroup(*self.e3[0][4:7]), color=MAG, scale_factor=1.15), run_time=0.8)
        serie = legenda("ESSE CASO FICA PARA UM VÍDEO DESTA SÉRIE", T_LAB)
        self.ate(0.8)
        self.play(FadeIn(serie), run_time=0.6)
        self.ate(0.96)
        fg.clear_updaters()
        self.clear(rt=0.5)

    def selo(self, s, cor):
        t = txt(s, T_LAB, color=cor, bold=True)
        r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.6, height=t.height + 0.38).set_stroke(cor, 2).set_fill(opacity=0)
        r.moldura = True
        t.move_to(r)
        return VGroup(r, t)
