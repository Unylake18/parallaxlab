"""Lote PS: S1 (RESUMO), S2 (a pergunta do corpo rígido) e EN (encerramento padrão).
S1: C_34 girando devagar (azimute +8°/s), disco em órbita de 0,30 m; à direita L⃗ = r⃗ × p⃗ · τ⃗ = dL⃗/dt · τ⃗ = 0 ⇒ L⃗ constante e três cartões PANEL.
S2: a mesa menor à esquerda; à direita uma nuvem de partículas girando em volta de um eixo, cada uma com o seu r⃗ × p⃗ pequeno (L⃗ para cima).
EN: logo, anéis violeta, INSCREVA-SE e a pergunta para os comentários."""
from pecas24 import *  # noqa: F401,F403


def cartao_ideia(pecas, cor=BLUE_L):
    g = linha_base([txt(p, 28, bold=True) if isinstance(p, str) else p for p in pecas], 0.12)
    r = RoundedRectangle(corner_radius=0.1, width=g.width + 0.5, height=g.height + 0.36).move_to(g).set_fill(PANEL, 0.92).set_stroke(cor, 2)
    r._fundo = True
    return VGroup(r, g).set_z_index(20)


class LotePS(Lote24):
    def cam(self):
        c = dict(self._cam_base)
        c["az"] = self._cam_base["az"] + 8.0 * max(0.0, self.clk.get_value() - self._c_rot) * self._gira
        k = float(self.k_tr.get_value())
        c["K"] = self._cam_base["K"] * (1 - 0.35 * k)
        c["xc"] = self._cam_base["xc"] - 1.2 * k
        return c

    def corpo(self):
        self._cam_base, self._c_rot, self._gira = dict(C34, K=3.7, xc=-4.35, yc=-0.75), 0.0, 1.0
        self.k_tr = ValueTracker(0.0)
        self.add(self.k_tr)
        self.tp = -10.0
        self.mov = mov_puxada(self)
        self.zp = zp_puxada(self)
        self.anda(1.0, tf=0.0)
        f3 = self.mesa()
        f3.op.set_value(0.0)
        self.canto("RESUMO")

        # ── S1 ──
        self.an("S1")
        self.play(f3.op.animate.set_value(1.0), run_time=0.6)
        A, ia = Mx(r"\vec L", "=", r"\vec r", r"\times", r"\vec p", size=52)
        B, ib = Mx(r"\vec\tau", "=", r"\frac{d\vec L}{dt}", size=52)
        C, ic = Mx(r"\vec\tau", "=", "0", r"\ \Rightarrow\ ", r"\vec L", r"\ \text{constante}", size=52)
        self.gat("a pergunta inicial está respondida")
        self.pilha.poe(A)
        self.lei(A, ia, rt=1.0, metodo="escrita")
        self.gat("a tração é central")
        self.pilha.poe(B)
        self.lei(B, ib, rt=1.0, metodo="escrita")
        self.pilha.poe(C)
        self.gat("ficou constante")
        self.lei(C, ic, rt=1.2, metodo="escrita")
        self.resultado(C, LMAG)
        self.gat("resumindo em três ideias")
        self.pilha.limpa()
        c1 = cartao_ideia(["NÃO PRECISA DE CÍRCULO"])
        c2 = cartao_ideia(["TORQUE ZERO,", T(r"\omega", 40, VEL), "PODE MUDAR"])
        c3 = cartao_ideia([T("L", 40, LMAG), "CONSERVA,", T("K", 40, KC), "NÃO"])
        cs = VGroup(c1, c2, c3).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(P3(3.6, 0.1))
        self.gat("momento angular não precisa de círculo")
        self.play(FadeIn(c1, shift=0.08 * UP), run_time=0.5)
        self.gat("torque zero não quer dizer")
        self.play(FadeIn(c2, shift=0.08 * UP), run_time=0.5)
        self.gat("conservar momento angular não é conservar energia")
        self.play(FadeIn(c3, shift=0.08 * UP), run_time=0.5)
        self.ate(0.99)

        # ── S2: a mesa menor à esquerda; nuvem de partículas girando em volta de um eixo ──
        self.an("S2")
        self.play(FadeOut(cs), self.k_tr.animate.set_value(1.0), run_time=0.8)
        ang = ValueTracker(0.0)
        self.add(ang)
        ang.add_updater(lambda m, dt: m.increment_value(0.9 * dt))
        C0 = P3(3.6, -0.6)
        rng = np.random.default_rng(3)
        parts = [(rng.uniform(0.4, 2.2), rng.uniform(0, 2 * math.pi), rng.uniform(-1.4, 1.4)) for _ in range(16)]
        eixo = DashedLine(C0 + P3(0, -2.4), C0 + P3(0, 2.6), dash_length=0.12).set_stroke(GEO, 2.4)

        def nuvem():
            g = VGroup()
            a = ang.get_value()
            for r, f0, h in parts:
                x = r * math.cos(f0 + a)
                y = h + 0.32 * r * math.sin(f0 + a)
                p = C0 + P3(x, y)
                front = math.sin(f0 + a) < 0
                g.add(Circle(radius=0.09).move_to(p).set_fill(escuro(MAS, 0.2) if front else escuro(MAS, 0.5), 1).set_stroke(MAS, 2).set_z_index(12 if front else 8))
                g.add(seta(p + P3(0, 0.12), p + P3(0, 0.12 + 0.18 * r), LMAG, 3.5, tip=0.12).set_z_index(12 if front else 8))
            return g
        nv = vivo(nuvem)
        self.gat("e se, em vez de uma partícula")
        self.play(FadeIn(eixo), OpVivo(nv), run_time=0.6)
        perg = linha_base([txt("COMO SOMAR TODOS OS", 28, bold=True), T(r"\vec r\times\vec p", 38), txt("?", 28, bold=True)], 0.14).move_to(P3(3.6, 2.4))
        self.gat("como somar todos esses")
        self.play(FadeIn(perg), run_time=0.5)
        self.ate(0.97)

        # ── EN: encerramento padrão ──
        self.an("EN")
        ang.clear_updaters()
        self.play(FadeOut(VGroup(eixo, perg)), OpVivo(nv, entra=False), f3.op.animate.set_value(0.0), run_time=0.5)
        self.remove(nv)
        logo = self.logo(5.0).move_to(P3(0, 1.45)).set_z_index(30)
        aneis = VGroup(*[Ellipse(width=w, height=h).move_to(P3(0, 1.45)).set_stroke(VEL, 2.5, opacity=0.5 - 0.1 * k) for k, (w, h) in enumerate(((6.2, 1.9), (7.0, 2.3), (7.8, 2.7)))])
        ins = txt("INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS", 32, bold=True).move_to(P3(0, -0.6)).set_z_index(30)
        self.play(FadeIn(logo), FadeIn(aneis), run_time=0.5)
        self.gat("se inscreve no parallax lab")
        self.play(FadeIn(ins, shift=0.06 * UP), run_time=0.5)
        q = VGroup(txt("UMA PEDRA CAINDO RETO TEM MOMENTO ANGULAR?", 30, bold=True, color=ANG),
                   txt("EM RELAÇÃO A QUAL PONTO?", 30, bold=True, color=ANG)).arrange(DOWN, buff=0.14).move_to(P3(0, -2.2)).set_z_index(30)
        self.gat("deixa nos comentários")
        self.play(FadeIn(q, shift=0.06 * UP), run_time=0.6)
        self.ate(0.99)
