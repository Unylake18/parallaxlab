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


def nuvem_pts():
    """As mesmas ~400 partículas do nuvem.js (mesmo gerador: sd = 11, Park–Miller), para projetar as escolhidas no Manim."""
    sd = [11]

    def rnd():
        sd[0] = (sd[0] * 16807) % 2147483647
        return sd[0] / 2147483647
    out = []
    for _ in range(400):
        r = 0.25 + 1.75 * math.sqrt(rnd())
        f = 2 * math.pi * rnd()
        z = (rnd() - 0.5) * 0.35 * (1 - r / 2.2)
        out.append((r, f, z))
    return out


class LotePS(Lote24):
    def cam(self):
        c = dict(self._cam_base)
        c["az"] = self._cam_base["az"] + 8.0 * max(0.0, self.clk.get_value() - self._c_rot) * self._gira
        k = float(self.k_tr.get_value())
        c["K"] = self._cam_base["K"] * (1 - 0.35 * k)
        c["xc"] = self._cam_base["xc"] - 1.2 * k
        return c

    def corpo(self):
        self._cam_base, self._c_rot, self._gira = dict(C34, K=3.0, xc=-4.2, yc=-0.6), 0.0, 1.0
        self.k_tr = ValueTracker(0.0)
        self.add(self.k_tr)
        self.tp = -10.0
        self.mov = mov_puxada(self)
        self.zp = zp_puxada(self)
        self.anda(1.0, tf=0.0)
        f3 = self.mesa()
        f3.op.set_value(1.0)
        self.canto("RESUMO")

        # ── S1 ──
        self.an("S1")
        self.transicao(0.5)
        anel_s = vivo(lambda: Circle(radius=0.34).set_stroke(WHITE_, 1.6, opacity=0.9).move_to(self.tela_disco()).set_z_index(9))     # v4 §2: disco ≥ 2 % com anel de destaque
        self.play(OpVivo(anel_s), run_time=0.4)
        A, ia = Mx(r"\vec L", "=", r"\vec r", r"\times", r"\vec p")
        B, ib = Mx(r"\vec\tau", "=", r"\frac{d\vec L}{dt}")
        C, ic = Mx(r"\vec\tau", "=", "0", r"\ \Rightarrow\ ", r"\vec L", "=")
        self.gat("a pergunta inicial está respondida")
        self.pilha.poe(A)
        self.lei(A, ia, rt=1.0, metodo="escrita")
        self.gat("a tração é central")
        self.pilha.poe(B)
        self.lei(B, ib, rt=1.0, metodo="escrita")
        self.pilha.poe(C)
        self.gat("ficou constante")
        self.lei(C, ic, rt=1.2, metodo="escrita")
        self.texto_na_linha(C, "CONSTANTE", LMAG)
        self.resultado(C, LMAG)
        self.gat("três ideias para levar")
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

        # ── S2: a mesa menor à esquerda; à direita a nuvem de ~400 partículas (Three.js 'nuvem'); 6 acendem com r⃗ × p⃗; as setinhas somam L⃗ ──
        self.an("S2")
        CN = camd(-90, 22, (0, 0, 0.35), 1.45, 43.6, 3.7, -0.9)
        ang = ValueTracker(0.0)
        nac = ValueTracker(0.0)
        self.add(ang, nac)
        ACES = [7, 52, 101, 160, 233, 318]
        pts_n = nuvem_pts()

        def est_n(_t=0.0):
            k = int(round(nac.get_value()))
            return r4(dict(cam=CN, ang=float(ang.get_value()), acesas=ACES[:k]))
        fn = Fundo3D(self, "nuvem", est_n, op=0.0)
        fn._fundo3d = True
        self.add(fn)
        self.remove(anel_s)
        self.play(FadeOut(cs), self.k_tr.animate.set_value(1.0), fn.op.animate.set_value(1.0), run_time=0.8)
        ang.add_updater(lambda m, dt: m.increment_value(0.6 * dt))

        def pos(i):
            r, f, z = pts_n[i]
            a = f + ang.get_value()
            return np.array([r * math.cos(a), r * math.sin(a), z])
        self.gat("e se, em vez de uma partícula")
        self.wait(0.8)

        def setinhas():
            k = int(round(nac.get_value()))
            g = VGroup()
            for i in ACES[:k]:
                p = pos(i)
                g.add(vetor_lab(proj(CN, p), proj(CN, p + np.array([0, 0, 0.22 + 0.16 * pts_n[i][0]])), LMAG, w=4, tip=0.12, origem=False, brilho=False))
            return g.set_z_index(14)
        sv = vivo(setinhas)
        self.add(sv)
        for k in range(1, 7):
            self.play(nac.animate.set_value(k), run_time=0.35, rate_func=lambda t: 1.0 if t > 0 else 0.0)
        lrp = T(r"\vec r\times\vec p", 34)

        def _lrp_pos(m):          # preso à ponta da primeira setinha (§2.5: não fica solto no alto)
            p0 = pos(ACES[0])
            m.move_to(proj(CN, p0 + np.array([0, 0, 0.22 + 0.16 * pts_n[ACES[0]][0]])) + P3(0.0, 0.46))
        _lrp_pos(lrp)
        lrp.add_updater(_lrp_pos)
        self.play(FadeIn(lrp), run_time=0.3)
        perg = linha_base([txt("COMO SOMAR TODOS OS", 28, bold=True), T(r"\vec r\times\vec p", 38), txt("?", 28, bold=True)], 0.14).move_to(P3(3.6, 2.6))
        self.gat("como somar todos esses")
        # as setinhas voam e se somam numa L⃗ grande no eixo
        lrp.clear_updaters()
        copias = sv.copy()
        self.remove(sv)
        self.add(copias)
        base_e = proj(CN, (0, 0, 0.0))
        topo_e = proj(CN, (0, 0, 2.2))
        alvos = [base_e + (topo_e - base_e) * (k / 6) for k in range(6)]
        anims = []
        for k, m in enumerate(copias):
            h = (topo_e - base_e) / 6
            anims.append(m.animate.become(Line(alvos[k], alvos[k] + h).set_stroke(LMAG, 4)))
        self.play(*anims, FadeIn(perg), run_time=1.0)
        Lg = vetor_lab(base_e, topo_e, LMAG, w=8, tip=0.26, origem=False)
        lLg = T(r"\vec L", 46, LMAG).next_to(topo_e, LEFT, buff=0.25)
        self.play(FadeOut(copias), FadeIn(Lg), FadeIn(lLg), run_time=0.5)
        # v13 §2.3.6: a fala também pergunta se o resultado aponta sempre ao longo do eixo
        perg2 = txt("E ELE APONTA AO LONGO DO EIXO?", 26, bold=True).move_to(P3(3.6, 2.17))
        self.gat("será que o resultado")
        self.play(FadeIn(perg2, shift=0.06 * DOWN), Indicate(Lg, color=LMAG, scale_factor=1.05), run_time=0.6)
        self.ate(0.97)
        eixo, nv = VGroup(Lg, lLg, lrp), fn
        perg = VGroup(perg, perg2)

        # ── EN: encerramento padrão ──
        self.an("EN")
        ang.clear_updaters()
        self.play(FadeOut(VGroup(eixo, perg)), fn.op.animate.set_value(0.0), f3.op.animate.set_value(0.0), run_time=0.5)
        logo = self.logo(5.0).move_to(P3(0, 1.45)).set_z_index(30)
        aneis = VGroup(*[Ellipse(width=w, height=h).move_to(P3(0, 1.45)).set_stroke(VEL, 2.5, opacity=0.5 - 0.1 * k) for k, (w, h) in enumerate(((6.2, 1.9), (7.0, 2.3), (7.8, 2.7)))])
        ins = txt("INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS", 32, bold=True).move_to(P3(0, -0.6)).set_z_index(30)
        self.play(FadeIn(logo), FadeIn(aneis), run_time=0.5)
        self.gat("se inscreve no parallax lab")
        self.play(FadeIn(ins, shift=0.06 * UP), run_time=0.5)
        q = VGroup(txt("EM RELAÇÃO A QUAL PONTO UMA PEDRA CAINDO RETO", 30, bold=True, color=ANG),
                   txt("TEM MOMENTO ANGULAR ZERO?", 30, bold=True, color=ANG)).arrange(DOWN, buff=0.14).move_to(P3(0, -2.2)).set_z_index(30)
        self.gat("deixa nos comentários")
        self.play(FadeIn(q, shift=0.06 * UP), run_time=0.6)
        self.ate(0.99)
