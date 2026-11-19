"""Lote PB5: B5 — FORÇA CENTRAL (Manim 2.5D, sem a mesa).
B5-1 partícula numa órbita com F⃗ sempre para O: τ⃗ = r⃗ × F⃗ → F⃗ ∥ r⃗ → τ⃗ = 0 → dL⃗/dt = 0 → L⃗ constante.
B5-2 plano inclinado (vista como a C_L) com L⃗ fixo perpendicular e a trajetória presa ao plano; L = 0: reta pelo centro.
B5-3 triângulos de mesmo tempo com áreas iguais; dA/dt = |L⃗|/2m. B5-4 construção de Newton (A → B → c fantasma; chute Δp⃗ para O em B; C).
B5-5 elipse (a = 2,6 u, e = 0,6), Sol no foco, 12 setores de mesmo tempo (M = E − e sen E), o planeta acelera perto do Sol."""
from pecas24 import *  # noqa: F401,F403

A_, E_ = F.A_ELI, F.E_ELI
B_ = A_ * math.sqrt(1 - E_ ** 2)
FOCO = P3(-2.75, -0.55)


def kepler(Mk, a=A_, e=E_, foco=FOCO, esc=1.0):
    E = Mk
    for _ in range(40):
        E -= (E - e * math.sin(E) - Mk) / (1 - e * math.cos(E))
    b = a * math.sqrt(1 - e * e)
    return foco + esc * P3(a * (math.cos(E) - e), b * math.sin(E))


class LoteB5(Lote24):
    def corpo(self):
        self.canto("FORÇA CENTRAL")
        Mt = ValueTracker(0.6)
        self.add(Mt)
        O1 = P3(-3.6, -0.6)
        a1, e1 = 2.2, 0.45

        def p1():
            return kepler(Mt.get_value(), a1, e1, O1)

        # ── B5-1: força sempre para O; τ⃗ = 0 → L⃗ constante ──
        self.an("B5-1")
        Mt.add_updater(lambda m, dt: m.increment_value(0.55 * dt))
        orb = VMobject().set_points_smoothly([kepler(t, a1, e1, O1) for t in np.linspace(0, 2 * math.pi, 120)]).set_stroke(RAST, 2.5, opacity=0.7)
        pino = pino2d(O1)
        lO = T("O", 40, WHITE_).next_to(pino, DL, buff=0.3)

        def cena1():
            p = p1()
            u = (O1 - p) / np.linalg.norm(O1 - p)
            return VGroup(seta(O1, p - 0.16 * (p - O1) / np.linalg.norm(p - O1), VETC, 5, tip=0.18),
                          seta(p + 0.18 * u, p + 0.95 * u, FC, 6, tip=0.2),
                          T(r"\vec F", 38, FC).move_to(p + 0.6 * u + 0.36 * np.array([-u[1], u[0], 0])),
                          T(r"\vec r", 38, VETC).move_to((O1 + p) / 2 - 0.36 * np.array([-u[1], u[0], 0])),
                          Circle(radius=0.13).move_to(p).set_fill(escuro(MAS, 0.3), 1).set_stroke(MAS, 3).set_z_index(12))
        c1 = vivo(cena1)
        self.play(FadeIn(orb), FadeIn(pino), FadeIn(lO), OpVivo(c1), run_time=0.7)
        A, ia = Mx(r"\vec\tau", "=", r"\vec r", r"\times", r"\vec F")
        self.pilha.poe(A)
        self.gat("uma força central")
        self.lei(A, ia, rt=1.0, metodo="lei")
        B, ib = Mx(r"\vec F", r"\parallel", r"\vec r")
        self.pilha.poe(B)
        self.gat("na mesma direção do vetor posição")
        self.lei(B, ib, {0: c1, 2: c1}, rt=1.0)
        C, ic = Mx(r"\vec\tau", "=", "0")
        self.pilha.poe(C)
        self.gat("o torque em relação a esse ponto é zero")
        self.gm(A, C, (J(ia, 0), J(ic, 0)), (J(ia, 1), J(ic, 1)), (J(ia, 2, 3, 4), J(ic, 2)), rt=1.2)
        D, id_ = Mx(r"\frac{d\vec L}{dt}", "=", "0")
        self.pilha.poe(D)
        self.gat("torque zero significa")
        self.lei(D, id_, {2: C[0][J(ic, 2)[0]]}, rt=1.0)
        E, ie = Mx(r"\vec L", r"\ \text{constante}", size=58)
        self.pilha.poe(E)
        self.lei(E, ie, rt=0.9)
        self.resultado(E, LMAG)
        self.gat("não importa o tamanho da força")
        self.play(Indicate(E, color=LMAG, scale_factor=1.08), run_time=0.8)
        self.ate(0.99)

        # ── B5-2: plano inclinado, L⃗ fixo perpendicular, trajetória no plano; L = 0 → reta pelo centro ──
        self.an("B5-2")
        Mt.clear_updaters()
        self.play(FadeOut(orb), OpVivo(c1, entra=False), FadeOut(pino), FadeOut(lO), run_time=0.4)
        self.remove(c1)
        self.pilha.so(E)
        ca = camd(-55, 35, (0, 0, 0), 2.1, 30, -3.6, -1.3)
        pr = lambda x, y, z=0.0: proj(ca, (x, y, z))
        plano = Polygon(pr(-1.2, -1.2), pr(1.2, -1.2), pr(1.2, 1.2), pr(-1.2, 1.2)).set_fill(GEO, 0.16).set_stroke(GEO, 2.2).set_z_index(3)
        traj = VMobject().set_points_smoothly([pr(*(kepler(t, 0.85, 0.4, P3(0, 0))[:2])) for t in np.linspace(0, 2 * math.pi, 100)]).set_stroke(RAST, 3).set_z_index(5)
        Lseta = seta(pr(0, 0), pr(0, 0, 1.35), LMAG, 7, tip=0.24)
        lL = T(r"\vec L", 44, LMAG).next_to(pr(0, 0, 1.35), LEFT, buff=0.4)
        O2d = pino2d(pr(0, 0), r=0.1)
        self.gat("perpendicular ao vetor posição")
        self.play(FadeIn(plano), FadeIn(O2d), FadeIn(Lseta), FadeIn(lL), run_time=0.7)
        Mt.set_value(0.0)
        bola = vivo(lambda: Circle(radius=0.11).move_to(pr(*(kepler(Mt.get_value(), 0.85, 0.4, P3(0, 0))[:2]))).set_fill(escuro(MAS, 0.3), 1).set_stroke(MAS, 3).set_z_index(12))
        self.gat("nunca sai do plano")
        self.play(Create(traj), OpVivo(bola), run_time=0.8)
        Mt.add_updater(lambda m, dt: m.increment_value(0.7 * dt))
        f1 = txt("O MOVIMENTO FICA NUM PLANO", 30, bold=True, color=GEO)
        self.pilha.poe(f1)
        self.gat("o movimento fica num plano")
        self.play(FadeIn(f1), run_time=0.5)
        self.gat("se o momento angular for zero")
        radial = DashedLine(pr(-1.1, -0.6), pr(1.1, 0.6), dash_length=0.1).set_stroke(MAG, 3)
        L0 = VGroup(T("L", 40, LMAG), T(r"=\,0", 40, WHITE_)).arrange(RIGHT, buff=0.08).move_to(pr(1.1, 0.6) + P3(0.6, 0.3))
        self.play(Create(radial), FadeIn(L0), run_time=0.7)
        self.ate(0.99)

        # ── B5-3: triângulos de mesmo tempo, áreas iguais; dA/dt = |L⃗|/2m ──
        self.an("B5-3")
        Mt.clear_updaters()
        self.play(FadeOut(VGroup(plano, traj, Lseta, lL, O2d, radial, L0)), OpVivo(bola, entra=False), run_time=0.4)
        self.remove(bola)
        orb2 = VMobject().set_points_smoothly([kepler(t, a1, e1, O1) for t in np.linspace(0, 2 * math.pi, 120)]).set_stroke(RAST, 2.5, opacity=0.8)
        pino = pino2d(O1)
        self.play(FadeIn(orb2), FadeIn(pino), run_time=0.4)
        self.gat("a área varrida por segundo")
        G_, ig = Mx(r"\frac{dA}{dt}", "=", r"\frac{|\vec L|}{2m}")
        self.pilha.poe(G_)
        self.lei(G_, ig, rt=1.2, metodo="lei")
        tris = VGroup()
        for k, t0 in enumerate((-0.35, 2.55)):
            pts = [kepler(t0 + 0.75 * s, a1, e1, O1) for s in np.linspace(0, 1, 12)]
            tris.add(Polygon(O1, *pts).set_fill(GEO, 0.35).set_stroke(GEO, 2).set_z_index(4))
        self.gat("áreas iguais em tempos iguais")
        self.play(FadeIn(tris[0]), run_time=0.7)
        self.play(FadeIn(tris[1]), run_time=0.7)
        f2 = txt("UM FIO · UMA MOLA · A GRAVIDADE DO SOL", 26, bold=True, color=GEO)
        self.pilha.poe(f2)
        self.gat("para qualquer força central")
        self.play(FadeIn(f2), run_time=0.5)
        self.ate(0.99)

        # ── B5-4: construção de Newton (hold) ──
        self.an("B5-4")
        self.play(FadeOut(VGroup(orb2, tris, pino)), run_time=0.4)
        self.pilha.limpa()
        O = P3(-4.9, -3.0)
        A_p, B_p = P3(-6.7, 0.35), P3(-4.55, 1.05)
        c_p = B_p + (B_p - A_p)
        kick = 0.33 * (O - B_p)
        C_p = c_p + kick
        lab = lambda s, p, d: T(s, 40, WHITE_).next_to(p, d, buff=0.32)
        pO = pino2d(O, r=0.11)
        pts = VGroup(*[Dot(p, radius=0.08, color=MAS).set_z_index(12) for p in (A_p, B_p)])
        self.play(FadeIn(pO), FadeIn(lab("O", O, DOWN)), FadeIn(pts), FadeIn(lab("A", A_p, LEFT)), FadeIn(lab("B", B_p, UP)), run_time=0.5)
        self.gat("sem força")
        seg1 = Line(A_p, B_p).set_stroke(RAST, 3)
        fant = DashedLine(B_p, c_p, dash_length=0.1).set_stroke(RAST, 3)
        dc = Dot(c_p, radius=0.08, color=GEO).set_z_index(12)
        t1 = Polygon(O, A_p, B_p).set_fill(GEO, 0.35).set_stroke(GEO, 2).set_z_index(4)
        t2 = Polygon(O, B_p, c_p).set_fill(GEO, 0.35).set_stroke(GEO, 2).set_z_index(4)
        lc = T("c", 40, GEO).next_to(c_p, UR, buff=0.25)
        lc._fantasma = True
        self.play(Create(seg1), FadeIn(t1), run_time=0.7)
        self.play(Create(fant), FadeIn(dc), FadeIn(lc), FadeIn(t2), run_time=0.7)
        N1, n1 = Mx(r"A_{OAB}", "=", r"A_{OBc}", cores={0: GEO, 2: GEO})
        self.pilha.poe(N1)
        self.lei(N1, n1, rt=1.0)
        self.gat("ela leva um chute")
        k_fim = B_p + 1.15 * kick / np.linalg.norm(kick)
        sk = seta(B_p, k_fim, MAG, 6, tip=0.2)
        lk = T(r"\Delta\vec p", 40, MAG).next_to(B_p + 0.6 * kick / np.linalg.norm(kick), LEFT, buff=0.35)
        self.play(FadeIn(sk), FadeIn(lk), run_time=0.6)
        self.gat("ela vai parar em c")
        seg2 = Line(B_p, C_p).set_stroke(RAST, 3)
        dC = Dot(C_p, radius=0.08, color=MAS).set_z_index(12)
        lC = T("C", 40, WHITE_).next_to(C_p, RIGHT, buff=0.14)
        self.play(Create(seg2), FadeIn(dC), FadeIn(lC), t2.animate.set_fill(GEO, 0.30).set_stroke(GEO, 2, opacity=1.0), run_time=0.7)
        self.gat("numa reta paralela")
        u = (B_p - O) / np.linalg.norm(B_p - O)
        par = DashedLine(c_p + 1.0 * u, C_p - 1.4 * u, dash_length=0.12).set_stroke(WHITE_, 2.4)
        base = Line(O, B_p).set_stroke(VETC, 4)
        self.play(Create(par), Create(base), run_time=0.8)
        t3 = Polygon(O, B_p, C_p).set_fill(GEO, 0.45).set_stroke(GEO, 2.5).set_z_index(5)
        self.gat("mesma base, mesma altura")
        self.play(FadeIn(t3), run_time=0.6)
        N2, n2 = Mx(r"A_{OBC}", "=", r"A_{OBc}", cores={0: GEO, 2: GEO})
        self.pilha.poe(N2)
        self.lei(N2, n2, rt=1.0)
        f3_ = txt("CHUTE CENTRAL NÃO MUDA A ÁREA", 30, bold=True, color=GEO)
        self.pilha.poe(f3_)
        self.gat("chute central não muda a área")
        self.play(FadeIn(f3_), run_time=0.5)
        self.ate(0.99)

        # ── B5-5: elipse com o Sol no foco; 12 setores de mesmo tempo; o planeta acelera perto do Sol ──
        self.an("B5-5")
        self.play(FadeOut(VGroup(pO, pts, seg1, fant, dc, lc, t1, t2, sk, lk, seg2, dC, lC, par, base, t3)), *[FadeOut(m) for m in self.mobjects if isinstance(m, MathTex) and m.get_x() < 0.3 and m not in self.fixos()], run_time=0.4)
        self.pilha.limpa()
        el = VMobject().set_points_smoothly([kepler(t) for t in np.linspace(0, 2 * math.pi, 160)]).set_stroke(RAST, 2.5)
        sol = sol2d(FOCO, 0.26)
        setores = VGroup()
        P = [kepler(2 * math.pi * k / 12) for k in range(13)]
        for k in range(12):
            arco = [kepler(2 * math.pi * (k + s) / 12) for s in np.linspace(0, 1, 10)]
            setores.add(Polygon(FOCO, *arco).set_fill(GEO, 0.35 if k % 2 == 0 else 0.20).set_stroke(GEO, 1.2, opacity=0.7).set_z_index(3))
        self.play(FadeIn(el), FadeIn(sol), run_time=0.5)
        self.gat("por isso um planeta")
        self.play(LaggedStart(*[FadeIn(s_) for s_ in setores], lag_ratio=0.25), run_time=2.4)
        Mt.set_value(0.0)
        Mt.add_updater(lambda m, dt: m.increment_value(0.9 * dt))
        planeta = vivo(lambda: Circle(radius=0.13).move_to(kepler(Mt.get_value())).set_fill("#3A5C8E", 1).set_stroke("#9CC7FF", 3).set_z_index(12))
        self.play(OpVivo(planeta), run_time=0.4)
        K1, k1 = Mx(r"\frac{dA}{dt}", "=", r"\frac{|\vec L|}{2m}")
        self.pilha.poe(K1)
        self.lei(K1, k1, rt=1.2)
        f4 = txt("PERTO DO SOL: MAIS RÁPIDO", 28, bold=True, color=GEO)
        self.pilha.poe(f4)
        self.gat("perto, o braço é curto")
        self.play(FadeIn(f4), run_time=0.5)
        self.ate(0.97)
        Mt.clear_updaters()
        self.play(FadeOut(VGroup(el, sol, setores)), OpVivo(planeta, entra=False), run_time=0.4)
