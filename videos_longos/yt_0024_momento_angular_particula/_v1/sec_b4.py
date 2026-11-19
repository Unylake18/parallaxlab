"""Lote PB4: B4 — O CÍRCULO (Three.js 'mesa_furo' em C_TOPO; fio preso, órbita de 0,60 m a 1,5 m/s; r⃗ ⟂ v⃗).
|L⃗| = r⊥ p → r⊥ = R → L = m v R → L = m R² ω → L = I ω (I = 0,072 kg·m², L = 0,18). Tração central: τ = 0, L constante.
Empurrão tangencial F_t = 0,30 N por 1,0 s (α = 2,5 rad/s²): ω 2,5 → 5,0 no mostrador; τ_z = dL_z/dt → m R² dω/dt (R FIXO) → I α."""
from pecas24 import *  # noqa: F401,F403


class LoteB4(Lote24):
    def corpo(self):
        self.camA = self.camB = CTOPO
        self.t_emp = None
        self.mov = lambda tf: (F.R0 * math.cos(F.circulo(tf, self.t_emp)["th"]), F.R0 * math.sin(F.circulo(tf, self.t_emp)["th"]))
        self.anda(1.0, tf=0.0)
        f3 = self.mesa()
        f3.op.set_value(0.0)
        self.canto("O CÍRCULO")
        Z = 0.012

        def th():
            return F.circulo(self.tf(), self.t_emp)["th"]

        def pD():
            t = th()
            return np.array([F.R0 * math.cos(t), F.R0 * math.sin(t), Z])

        def tang():
            t = th()
            return np.array([-math.sin(t), math.cos(t), 0.0])

        def r_viva():
            a, b = self.tela((0, 0, Z)), self.tela(pD())
            u = (b - a) / np.linalg.norm(b - a)
            n = np.array([-u[1], u[0], 0])
            return VGroup(seta(a, b - 0.17 * u, VETC, 5, tip=0.18), T("R", 40, VETC).move_to((a + b) / 2 - 0.36 * n))

        def v_viva():
            d = pD()
            w = F.circulo(self.tf(), self.t_emp)["w"]
            a, b = self.tela(d), self.tela(d + 0.14 * w * F.R0 * tang())          # 0,14 m por m/s (cabe na mesa depois do empurrão: v = 3,0 m/s)
            u = (b - a) / np.linalg.norm(b - a)
            return VGroup(seta(a + 0.17 * u, b, VEL, 6, tip=0.2), T(r"\vec v", 40, VEL).move_to(b + 0.35 * u),
                          angulo_reto(a, self.tela((0, 0, Z)), b, s=0.22, cor=WHITE_))

        # ── B4-1: órbita; r⃗ ⟂ v⃗; |L⃗| = r⊥ p → r⊥ = R → L = m v R → L = m R² ω ──
        self.an("B4-1")
        self.play(f3.op.animate.set_value(1.0), run_time=0.6)
        rv, vv = vivo(r_viva), vivo(v_viva)
        self.gat("o vetor posição é sempre perpendicular")
        self.play(OpVivo(rv), OpVivo(vv), run_time=0.6)
        A, ia = Mx(r"|\vec L|", "=", r"r_\perp", "p")
        self.pilha.poe(A)
        self.lei(A, ia, rt=0.9, metodo="lei")
        B, ib = Mx(r"r_\perp", "=", "R")
        self.pilha.poe(B)
        self.gat("o braço é o próprio raio")
        self.lei(B, ib, {2: rv}, rt=0.9)
        C, ic = Mx("L", "=", "m", "v", "R")
        self.pilha.poe(C)
        self.gat("a massa, vezes a velocidade, vezes o raio")
        self.gm(A, C, (J(ia, 0), J(ic, 0)), (J(ia, 1), J(ic, 1)), (J(ia, 3), J(ic, 2, 3)), (J(ia, 2), J(ic, 4)), rt=1.3)
        card, icd = Mx("v", "=", r"\omega", "R", size=40)
        card.move_to(P3(-1.2, 2.2))
        self.gat("a velocidade angular vezes o raio")
        self.play(FadeIn(card), run_time=0.4)
        D, id_ = Mx("L", "=", "m", "R^2", r"\omega", size=56)
        self.pilha.poe(D)
        self.gm(C, D, (J(ic, 0), J(id_, 0)), (J(ic, 1), J(id_, 1)), (J(ic, 2), J(id_, 2)), (J(ic, 4), J(id_, 3)[0:1]), (J(ic, 3), J(id_, 4)),
                ([], J(id_, 3)[1:]), rt=1.4, extra=(Indicate(card, color=VEL),))
        self.ate(0.99)

        # ── B4-2: m R² vira I → L = I ω; números I = 0,072 · L = 0,18 ──
        self.an("B4-2")
        self.play(FadeOut(card), run_time=0.3)
        self.pilha.so(D)
        chave = Brace(VGroup(*[D[0][j] for j in J(id_, 2, 3)]), DOWN, buff=0.06).set_color(MAS)
        lI = T("I", 40, MAS).next_to(chave, DOWN, buff=0.08)
        self.gat("o momento de inércia da partícula")
        self.play(FadeIn(chave), FadeIn(lI), run_time=0.5)
        E, ie = Mx("L", "=", "I", r"\omega", size=58)
        self.pilha.poe(E)
        self.gm(D, E, (J(id_, 0), J(ie, 0)), (J(id_, 1), J(ie, 1)), (J(id_, 2, 3), J(ie, 2)), (J(id_, 4), J(ie, 3)), rt=1.2, extra=(FadeOut(chave), FadeOut(lI)))
        self.resultado(E, LMAG)
        lId = vivo(lambda: T("I", 40, MAS).move_to(self.tela(pD()) + P3(0.45, 0.45)))
        self.play(OpVivo(lId), run_time=0.4)
        G1, g1 = Mx("I", "=", r"0{,}20", r"\cdot", r"0{,}60^2", "=", r"0{,}072", r"\,\mathrm{kg\,m^2}", cores={2: MAS, 4: VETC, 6: MAS})
        self.pilha.poe(G1)
        self.gat("no círculo")
        self.lei(G1, g1, rt=1.3, numero=True)
        G2, g2 = Mx("L", "=", r"0{,}072", r"\cdot", r"2{,}5", "=", r"0{,}18", r"\,\mathrm{kg\,m^2/s}", cores={2: MAS, 4: VEL, 6: LMAG})
        self.pilha.poe(G2)
        self.lei(G2, g2, rt=1.3, numero=True)
        self.ate(0.99)

        # ── B4-3: tração para o centro; τ = 0; L constante no mostrador ──
        self.an("B4-3")
        self.play(OpVivo(lId, entra=False), run_time=0.3)
        self.remove(lId)

        def t_viva():
            a, o = self.tela(pD()), self.tela((0, 0, Z))
            u = (o - a) / np.linalg.norm(o - a)
            return VGroup(seta(a + 0.2 * u, a + 1.15 * u, FC, 6, tip=0.2), T(r"\vec T", 40, FC).move_to(a + 0.7 * u + 0.38 * np.array([-u[1], u[0], 0])))
        Tv = vivo(t_viva)
        self.gat("a tração do fio")
        self.play(OpVivo(Tv), run_time=0.5)
        self.gat("não faz torque")
        t0 = VGroup(T(r"\tau", 46, FC), T(r"=\,0", 46, WHITE_)).arrange(RIGHT, buff=0.1)
        self.pilha.poe(t0)
        self.play(FadeIn(t0), run_time=0.4)
        mL = mostrador("L", lambda: F.M * F.R0 ** 2 * F.circulo(self.tf(), self.t_emp)["w"], 3, r"\mathrm{kg\,m^2/s}", LMAG, P3(-7.2, -3.45))
        self.gat("momento angular constante")
        self.play(OpVivo(mL), run_time=0.4)
        self.ate(0.99)

        # ── B4-4: empurrão tangencial de 1 s; ω 2,5 → 5,0; τ_z = dL_z/dt → … → I α ──
        self.an("B4-4")
        self.pilha.limpa()
        self.play(OpVivo(Tv, entra=False), run_time=0.3)
        self.remove(Tv)
        mw = mostrador(r"\omega", lambda: F.circulo(self.tf(), self.t_emp)["w"], 2, r"\mathrm{rad/s}", VEL, P3(-7.2, -2.7))
        self.play(OpVivo(mw), run_time=0.3)
        self.gat("um empurrão de lado")
        self.t_emp = self.tf() + 0.1

        def ft():
            if self.t_emp is None or not (0 <= self.tf() - self.t_emp <= F.T_EMP):
                return VGroup()
            d = pD()
            a, b = self.tela(d + 0.05 * tang()), self.tela(d + 0.30 * tang())
            u = (b - a) / np.linalg.norm(b - a)
            return VGroup(seta(a, b, FC, 7, tip=0.24), T("F_t", 40, FC).move_to(b + 0.42 * u))
        ftv = vivo(ft)
        self.add(ftv)
        self.wait(1.3)
        self.remove(ftv)
        H1, h1 = Mx(r"\tau_z", "=", r"\frac{dL_z}{dt}")
        self.pilha.poe(H1)
        self.gat("escrevendo a lei")
        self.lei(H1, h1, rt=1.0, metodo="lei")
        H2, h2 = Mx(r"\tau_z", "=", r"\frac{d(m R^2\omega)}{dt}")
        self.pilha.poe(H2)
        self.gm(H1, H2, (J(h1, 0), J(h2, 0)), (J(h1, 1), J(h2, 1)), (J(h1, 2)[0:1], J(h2, 2)[0:1]), (J(h1, 2)[1:3], J(h2, 2)[1:7]), (J(h1, 2)[3:], J(h2, 2)[7:]), rt=1.3)
        rfixo = txt("R FIXO", 26, bold=True, color=VETC)
        self.gat("com o raio fixo")
        H3, h3 = Mx(r"\tau_z", "=", "m", "R^2", r"\frac{d\omega}{dt}")
        self.pilha.poe(H3)
        rfixo.next_to(H3, RIGHT, buff=0.35)
        self.gm(H2, H3, (J(h2, 0), J(h3, 0)), (J(h2, 1), J(h3, 1)), (J(h2, 2)[2:3], J(h3, 2)), (J(h2, 2)[3:5], J(h3, 3)), (J(h2, 2)[0:1], J(h3, 4)[0:1]),
                (J(h2, 2)[5:6], J(h3, 4)[1:2]), (J(h2, 2)[7:], J(h3, 4)[2:]), (J(h2, 2)[1:2] + J(h2, 2)[6:7], []), rt=1.4, extra=(FadeIn(rfixo),))
        H4, h4 = Mx(r"\tau_z", "=", "I", r"\alpha", size=58)
        self.pilha.poe(H4)
        self.gat("sobra o momento de inércia")
        self.gm(H3, H4, (J(h3, 0), J(h4, 0)), (J(h3, 1), J(h4, 1)), (J(h3, 2, 3), J(h4, 2)), (J(h3, 4), J(h4, 3)), rt=1.3)
        self.resultado(H4, FC)
        self.ate(0.99)

        # ── B4-5: R FIXO pisca; nota SÓ PORQUE R NÃO MUDOU ──
        self.an("B4-5")
        self.gat("guarda este detalhe")
        self.play(Indicate(rfixo, color=VETC, scale_factor=1.25), run_time=0.8)
        nota = txt("SÓ PORQUE R NÃO MUDOU", 28, bold=True, color=VETC)
        self.pilha.poe(nota)
        self.gat("só saiu assim")
        self.play(FadeIn(nota), run_time=0.5)
        self.play(Indicate(rfixo, color=VETC, scale_factor=1.25), run_time=0.8)
        self.ate(0.97)
        self.play(OpVivo(rv, entra=False), OpVivo(vv, entra=False), OpVivo(mL, entra=False), OpVivo(mw, entra=False), run_time=0.4)
