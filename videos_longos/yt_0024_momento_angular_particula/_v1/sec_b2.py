"""Lote PB2: B2 — UMA RETA TAMBÉM GIRA (Three.js 'mesa_furo', dolly C_34 → C_TOPO; fio removido, bucha vazia; pinos em O1 e O3).
Disco livre a 1,50 m/s em +x ao longo de y = +0,40 m (x de −0,75 a +0,75: 1,0 s por travessia). Nas análises a travessia repete em
CÂMERA LENTA ×0,25 (selo), sem rastro (o disco volta ao início fora da conta). r⃗ do ponto escolhido ao disco, p⃗ no disco, ⊙/⊗ de L
no ponto. B2-5: triângulos de área de Δt = 0,50 s a partir do furo (base 0,75 m, altura 0,40 m, 0,150 m² cada).
Inconsistência do handoff: em x de −0,75 a +0,75 m só cabem DOIS triângulos de 0,50 s (três pediriam 2,25 m de reta; a mesa tem 1,60 m).
Foram desenhados os dois (reportado no qa.txt)."""
from pecas24 import *  # noqa: F401,F403

CT2 = camd(-90, 90, (0, 0, 0), 4.7, 0.0, -3.75, -1.50)


class LoteB2(Lote24):
    def corpo(self):
        self.camA = self.camB = C34
        self.fio = False
        self.rastro_on = False
        Y = F.RETA_Y
        self.ciclo = 4.0                       # s de cena por travessia em câmera lenta ×0,25

        def mov(tf):
            u = (tf % 1.0) if self._loop else min(1.0, max(0.0, tf))
            return (F.RETA_X0 + F.RETA_V * u, Y)
        self._loop = True
        self.mov = mov
        self.disco_on = True
        self.anda(1.0, tf=0.0)
        self.pinos = [list(F.O1), list(F.O3)]
        f3 = self.mesa()
        O1, O2, O3 = [np.array([o[0], o[1], 0.012]) for o in (F.O1, F.O2, F.O3)]
        self.canto("UMA RETA TAMBÉM GIRA")

        def D3():
            x, y = self.disco()
            return np.array([x, y, 0.012])

        def r_de(O):
            return lambda: VGroup(seta(self.tela(O), self.tela(D3()), VETC, 5, tip=0.18),
                                  T(r"\vec r", 40, VETC).move_to(self.tela((O + D3()) / 2) + P3(0, -0.36 if O[1] >= Y - 1e-9 else 0.36)))

        def p_viva():
            d = D3()
            return VGroup(seta(self.tela(d), self.tela(d + np.array([0.20, 0, 0])), MAG, 6, tip=0.2),
                          T(r"\vec p", 40, MAG).move_to(self.tela(d + np.array([0.12, 0, 0])) + P3(0, 0.42)))

        # ── B2-1: dolly para C_TOPO; pinos; o disco atravessa; dados ──
        self.an("B2-1")
        self.play(f3.op.animate.set_value(1.0), run_time=0.4)
        self.dolly(CT2, 1.6)
        lO = VGroup(*[T(n, 38, WHITE_).move_to(self.tela(o) + P3(-0.42, -0.36)) for n, o in ((r"O_1", O1), (r"O_2", O2), (r"O_3", O3))])
        self.play(FadeIn(lO), run_time=0.5)
        self.gat("solta o disco do fio")
        reta = DashedLine(self.tela((F.RETA_X0, Y, 0.01)), self.tela((F.RETA_X1, Y, 0.01)), dash_length=0.12).set_stroke(GEO, 2, opacity=0.8)
        self.play(Create(reta), run_time=0.6)
        self.gat("ninguém faz força nele")
        dados = VGroup(VGroup(T("m", 40, MAS), T(r"=\,", 40, WHITE_), T(r"0{,}20", 40, MAS), T(r"\mathrm{kg}", 36, WHITE_)).arrange(RIGHT, buff=0.08),
                       VGroup(T("v", 40, VEL), T(r"=\,", 40, WHITE_), T(r"1{,}5", 40, VEL), T(r"\mathrm{m/s}", 36, WHITE_)).arrange(RIGHT, buff=0.08)) \
            .arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(P3(-6.0, -2.75))
        cota = VGroup(DoubleArrow(self.tela((0.42, 0, 0.01)), self.tela((0.42, Y, 0.01)), buff=0, stroke_width=4, tip_length=0.16).set_color(VETC))
        l_d = VGroup(T("d", 40, VETC), T(r"=\,", 40, WHITE_), T(r"0{,}40", 40, VETC), T(r"\mathrm{m}", 36, WHITE_)).arrange(RIGHT, buff=0.08) \
            .next_to(cota, RIGHT, buff=0.15)
        self.play(FadeIn(dados), FadeIn(cota), FadeIn(l_d), run_time=0.6)
        self.gat("ele tem momento angular")
        sp = vivo(p_viva)
        self.play(OpVivo(sp), run_time=0.5)
        self.ate(0.99)

        # ── B2-2: em relação a O1 (sobre a reta): r⃗ sempre ao longo de p⃗; L = 0 ──
        self.an("B2-2")
        self.anda(0.25)
        self.selo("CÂMERA LENTA", "×0,25")
        r1 = vivo(r_de(O1))
        self.gat("em cima da própria reta")
        anel = Circle(radius=0.2).move_to(self.tela(O1)).set_stroke(WHITE_, 2.6)
        self.play(OpVivo(r1), Create(anel), run_time=0.6)
        self.gat("o braço é zero")
        L0 = VGroup(T("L", 44, LMAG), T(r"=\,0", 44, WHITE_)).arrange(RIGHT, buff=0.1).move_to(self.tela(O1) + P3(-0.9, 0.55))
        self.play(FadeIn(L0), run_time=0.5)
        self.ate(0.99)

        # ── B2-3: em relação ao furo O2: braço d constante; ⊗; L_z = −m v d = −0,12 ──
        self.an("B2-3")
        self.play(OpVivo(r1, entra=False), FadeOut(anel), FadeOut(L0), run_time=0.4)
        self.remove(r1)
        r2 = vivo(r_de(O2))
        anel2 = Circle(radius=0.2).move_to(self.tela(O2)).set_stroke(WHITE_, 2.6)
        self.gat("em relação ao furo")
        self.play(OpVivo(r2), Create(anel2), run_time=0.6)
        self.gat("sentido horário")
        x_in = sai_entra(self.tela(O2) + P3(0.75, -0.55), saindo=False)
        self.play(FadeIn(x_in), run_time=0.5)
        A, ia = Mx(r"\vec L", "=", r"\vec r", r"\times", r"\vec p")
        self.pilha.poe(A)
        self.lei(A, ia, rt=0.9, metodo="lei")
        B, ib = Mx("L_z", "=", "-", "m", "v", "d", cores={5: VETC})
        self.pilha.poe(B)
        self.gat("o momento angular vale menos")
        self.lei(B, ib, {3: dados[0][0], 4: dados[1][0], 5: l_d[0]}, rt=1.3)
        C, ic = Mx("=", "-", r"0{,}20", r"\cdot", r"1{,}5", r"\cdot", r"0{,}40", cores={2: MAS, 4: VEL, 6: VETC})
        self.pilha.poe(C)
        self.lei(C, ic, {2: dados[0][2], 4: dados[1][2], 6: l_d[2]}, rt=1.4, numero=True)
        Dm, idm = Mx("=", "-", r"0{,}12", r"\,\mathrm{kg\,m^2/s}", size=56, cores={2: LMAG})
        self.pilha.poe(Dm)
        self.gat("zero vírgula doze")
        self.lei(Dm, idm, rt=0.9, numero=True)
        self.resultado(Dm, LMAG)
        self.gat("o sinal negativo")
        self.play(Indicate(x_in, color=LMAG, scale_factor=1.3), run_time=0.7)
        self.ate(0.99)

        # ── B2-4: em relação a O3 (do outro lado): ⊙ e L_z = +0,12 ──
        self.an("B2-4")
        self.play(OpVivo(r2, entra=False), FadeOut(anel2), run_time=0.4)
        self.remove(r2)
        r3 = vivo(r_de(O3))
        anel3 = Circle(radius=0.2).move_to(self.tela(O3)).set_stroke(WHITE_, 2.6)
        self.gat("do outro lado da reta")
        self.play(OpVivo(r3), Create(anel3), run_time=0.6)
        o_out = sai_entra(self.tela(O3) + P3(-2.6, -0.1), saindo=True)
        L3 = VGroup(T("L_z", 44, LMAG), T(r"=\,+", 44, WHITE_), T(r"0{,}12", 44, LMAG)).arrange(RIGHT, buff=0.08).next_to(o_out, RIGHT, buff=0.25)
        self.gat("troca de sinal")
        self.play(FadeIn(o_out), FadeIn(L3), run_time=0.6)
        self.gat("não é uma propriedade só da partícula")
        frase = txt("DEPENDE DO PONTO", 32, bold=True, color=LMAG)
        self.pilha.poe(frase)
        self.play(FadeIn(frase), run_time=0.5)
        self.ate(0.99)

        # ── B2-5: triângulos de Δt = 0,50 s a partir do furo (mesma base, mesma altura); hold de 2 s ──
        self.an("B2-5")
        self.sem_selo()
        self.pilha.limpa()
        self.play(OpVivo(r3, entra=False), FadeOut(VGroup(anel3, o_out, L3, x_in)), run_time=0.4)
        self.remove(r3)
        self._loop = False
        self.anda(0.25, tf=0.0)
        r2b = vivo(r_de(O2))
        self.gat("liga o furo ao disco")
        self.play(OpVivo(r2b), run_time=0.5)
        cores_t = (0.30, 0.20)
        tris = VGroup()
        for k in range(2):
            xa, xb = F.RETA_X0 + 0.75 * k, F.RETA_X0 + 0.75 * (k + 1)
            tri = Polygon(self.tela(O2), self.tela((xa, Y, 0.012)), self.tela((xb, Y, 0.012))).set_fill(GEO, cores_t[k]).set_stroke(GEO, 2)
            tris.add(tri.set_z_index(5))
        self.gat("olha a área")
        self.play(FadeIn(tris[0]), run_time=2.0, rate_func=linear)
        self.play(FadeIn(tris[1]), run_time=2.0, rate_func=linear)
        self.anda(0.0)
        bases = VGroup(*[T(r"0{,}75\,\mathrm{m}", 34, VETC).move_to(self.tela((F.RETA_X0 + 0.75 * k + 0.375, Y, 0)) + P3(0, 0.42)) for k in range(2)])
        alt = DashedLine(self.tela((0, 0, 0.01)), self.tela((0, Y, 0.01)), dash_length=0.08).set_stroke(VETC, 3)
        self.gat("a altura até o furo")
        self.play(FadeIn(bases), Create(alt), run_time=0.6)
        areas = VGroup(*[T(r"0{,}150\,\mathrm{m^2}", 34, WHITE_).move_to(tris[k].get_center() + P3(0.0 if k else -0.25, 0.05)) for k in range(2)])
        self.gat("têm a mesma área")
        self.play(FadeIn(areas), run_time=0.6)
        frase2 = txt("ÁREAS IGUAIS EM TEMPOS IGUAIS", 32, bold=True, color=GEO)
        self.pilha.poe(frase2)
        self.gat("áreas iguais em tempos iguais")
        self.play(FadeIn(frase2), run_time=0.5)
        self.ate(0.99)

        # ── B2-6: dA = ½|r⃗ × v⃗ dt| → dA/dt = |r⃗ × p⃗|/2m → |L⃗|/2m = 0,30 m²/s ──
        self.an("B2-6")
        self.play(FadeOut(VGroup(bases, areas)), run_time=0.3)
        fino = Polygon(self.tela(O2), self.tela((-0.15, Y, 0.012)), self.tela((-0.05, Y, 0.012))).set_fill(GEO, 0.65).set_stroke(GEO, 2).set_z_index(7)
        A1, a1 = Mx("dA", "=", r"\tfrac{1}{2}", r"|\vec r\times\vec v\,dt|")
        self.pilha.poe(A1)
        self.gat("a área de cada triângulo fininho")
        self.play(FadeIn(fino), run_time=0.5)
        self.lei(A1, a1, rt=1.4, metodo="lei")
        A2, a2 = Mx(r"\frac{dA}{dt}", "=", r"\frac{|\vec r\times\vec p|}{2m}")
        self.pilha.poe(A2)
        self.gat("trocando a velocidade")
        self.gm(A1, A2, ([0, 1], [0, 1]), ([12, 13], [3, 4]), ([2], [5]), ([6], [6]), ([7, 8], [7, 8]), ([9], [9]), ([10, 11], [10, 11]),
                ([14], [12]), ([4], [13]), ([5], [14]), ([3], []), ([], [2]), ([], [15]), rt=1.6)
        A3, a3 = Mx(r"\frac{dA}{dt}", "=", r"\frac{|\vec L|}{2m}", size=56)
        self.pilha.poe(A3)
        self.gat("aparece o momento angular")
        self.gm(A2, A3, ([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]), ([6], [6]), ([7, 8, 9, 10, 11], [7, 8]), ([12], [9]), ([13], [10]), ([14], [11]),
                ([15], [12]), rt=1.4)
        self.resultado(A3, GEO)
        A4, a4 = Mx("=", r"0{,}30", r"\,\mathrm{m^2/s}", cores={1: GEO})
        self.pilha.poe(A4)
        self.gat("momento angular constante")
        self.lei(A4, a4, rt=0.9, numero=True)
        self.ate(0.97)
        self.play(OpVivo(r2b, entra=False), OpVivo(sp, entra=False), FadeOut(VGroup(tris, alt, fino, reta, cota, l_d, dados, lO)), run_time=0.4)
