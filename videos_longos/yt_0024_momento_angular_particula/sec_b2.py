"""Lote PB2 v2: B2 — UMA RETA TAMBÉM GIRA (Three.js 'mesa_furo' v2, dolly C_34 → C_TOPO; fio removido, bucha vazia; pinos em O1 e O3).
Disco livre a 1,50 m/s em +x ao longo de y = +0,40 m (x de −0,75 a +0,75: 1,0 s por travessia). Nas análises a travessia repete em
CÂMERA LENTA ×0,25 (selo só enquanto o disco anda; nas contas o disco para). r⃗ do ponto escolhido ao disco, p⃗ no disco; ⊗/⊙ EM CIMA do
ponto (O2, O3) com o anel do pino (ou do furo) acendendo na cor do L. Dados m, v e d no HUD à direita da mesa; a cota d fica em x = 0,80 m,
fora da área varrida por r⃗. B2-5 (handoff v2 §1): quatro triângulos de Δt = 0,25 s (base 0,375 m, altura 0,40 m, 0,075 m² cada),
varridos em tempo real pelo area_lab, tons alternando 40 %/25 %."""
from pecas24 import *  # noqa: F401,F403

CT2 = CPLANO


class LoteB2(Lote24):
    def estado3d(self, _t=0.0):
        e = super().estado3d(_t)
        e["pinosLuz"] = [round(float(self.luz1.get_value()), 3), round(float(self.luz3.get_value()), 3)]
        e["furoLuz"] = round(1.0 + 2.0 * float(self.luz2.get_value()), 3)
        gs = [[o[0], o[1], round(float(g.get_value()), 3)] for o, g in zip((F.O1, F.O2, F.O3), self.gr) if g.get_value() > 0.003]
        e["grades"] = sorted(gs, key=lambda q: -q[2])[:2]              # v5 ajuste 4: grade polar centrada na referência ativa (crossfade 0,5 s)
        return e

    def corpo(self):
        self.camA = self.camB = C34
        self.fio = False
        self.rastro_on = False
        self.luz1, self.luz2, self.luz3 = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.add(self.luz1, self.luz2, self.luz3)
        self.gr = [ValueTracker(0.0), ValueTracker(1.0), ValueTracker(0.0)]      # opacidade da grade polar centrada em O1, O2 (furo), O3
        self.add(*self.gr)
        Y = F.RETA_Y

        def troca_ref(de, para, rt=0.5):
            """Crossfade da grade polar: sai a da referência antiga, entra a da nova."""
            return [self.gr[de].animate.set_value(0.0), self.gr[para].animate.set_value(1.0)]

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

        def r_de(O, curvo=False):
            """v5: vec_r (cauda no ponto de referência, ponta no disco); rótulo r⃗ do lado oposto ao de p⃗ (acima da reta só com O3)."""
            def f():
                a, b = self.tela(O), self.tela(D3())
                u = (b - a) / max(np.linalg.norm(b - a), 1e-6)
                n = np.array([-u[1], u[0], 0.0])
                if curvo:                                    # O1 sobre a reta: arco para cima (cauda e ponta exatas), rótulo acima do arco
                    lado = 1.0 if n[1] > 0 else -1.0
                    if n[1] < 0:
                        n = -n
                    if u[0] < 0:                              # r⃗ aponta para a esquerda: rótulo abaixo do arco (longe do rótulo de O₁ e de p⃗)
                        n = -n
                    dist = 0.55
                else:
                    lado, dist = 1.0, 0.42
                    if O[1] < Y and n[0] < 0:                 # v5: rótulo do lado direito de r⃗ (longe do rótulo de O₁, que fica à esquerda, e de p⃗)
                        n = -n
                    if O[1] > Y and n[1] < 0:
                        n = -n
                g = vec_r(self, O, VETC, lado=lado, curvo=curvo, w=6, tip=0.2)
                return VGroup(g, T(r"\vec r", 40, VETC).move_to(a + 0.5 * (b - a) + dist * n))
            return f

        def p_viva(esq=False):
            def f():
                d = D3()
                return VGroup(etiqueta_vec(vetor_lab(self.tela(d), self.tela(d + np.array([0.15, 0, 0])), MAG, w=6, tip=0.2), "sentido",
                                    ref=lambda: self.tela(D3() + np.array([0.1, 0, 0])) - self.tela(D3()), nome="p⃗ B2"),
                              T(r"\vec p", 40, MAG).move_to(self.tela(d + np.array([0.09, 0, 0])) + P3(0.32, 0.50)))
            return f

        # ── B2-1: dolly para C_TOPO; pinos; o disco atravessa; dados no HUD ──
        self.an("B2-1")
        f3.op.set_value(1.0)
        self.transicao(0.5)
        self.dolly(CT2, 1.6)
        # caso 7: rótulos dos pinos do lado oposto à reta (O1 está na reta: rótulo embaixo, longe do disco)
        lO = VGroup(T(r"O_1", 38, WHITE_).move_to(self.tela(O1) + P3(-0.55, -0.48)),
                    T(r"O_2", 38, WHITE_).move_to(self.tela(O2) + P3(-0.55, -0.50)),
                    T(r"O_3", 38, WHITE_).move_to(self.tela(O3) + P3(0.55, -0.05)))
        pn = [pino_ref(self, O) for O in (O1, O2, O3)]           # v5 ajuste 4: cada referência tem pino visível (anel branco com ponto)
        self.play(FadeIn(lO), *[OpVivo(q) for q in pn], run_time=0.5)
        self.gat("solta o disco do fio")
        reta = DashedLine(self.tela((F.RETA_X0, Y, 0.01)), self.tela((F.RETA_X1, Y, 0.01)), dash_length=0.12).set_stroke(GEO, 2, opacity=0.8)
        self.play(Create(reta), run_time=0.6)
        self.gat("ninguém faz força nele")
        h_m = hud("m", lambda: F.M, 2, "KG", MAS, slot=1.9)
        h_v = hud("v", lambda: F.V0, 1, "M/S", VEL, slot=-0.7)
        h_d = hud("d", lambda: F.RETA_Y, 2, "M", VETC, slot=-2.2)
        cota = DoubleArrow(self.tela((0.72, 0, 0.01)), self.tela((0.72, Y, 0.01)), buff=0, stroke_width=4, tip_length=0.16).set_color(VETC).set_z_index(10)
        l_dc = T("d", 40, VETC).move_to((cota.get_start() + cota.get_end()) / 2 + P3(-0.32, 0.0))      # v5: só o símbolo, junto ao centro da seta (o valor está no HUD)
        f_l = txt("DISCO LIVRE: NENHUMA FORÇA", 30, bold=True, color=GEO)
        self.pilha.poe(f_l)
        self.play(OpVivo(h_m), OpVivo(h_v), OpVivo(h_d), FadeIn(cota), FadeIn(l_dc), FadeIn(f_l), run_time=0.6)
        self.gat("ele tem momento angular")
        sp = vivo(p_viva())
        self.play(OpVivo(sp), run_time=0.5)
        self.ate(0.99)

        # ── B2-2: em relação a O1 (sobre a reta): r⃗ sempre ao longo de p⃗; L = 0 ──
        self.an("B2-2")
        self.anda(0.25)
        self.selo("CÂMERA LENTA", "×0,25")
        r1 = vivo(r_de(O1, curvo=True))
        self.gat("em cima da própria reta")
        self.play(OpVivo(r1), self.luz1.animate.set_value(1.0), *troca_ref(1, 0), run_time=0.6)
        self.gat("o braço é zero")
        L0 = VGroup(T("L", 44, LMAG), T(r"=\,0", 44, WHITE_)).arrange(RIGHT, buff=0.1).move_to(self.tela(O1) + P3(1.0, -0.52))      # v5 ajuste 4: L = 0 no próprio pino
        self.play(FadeIn(L0), run_time=0.5)
        self.ate(0.99)

        # ── B2-3: em relação ao furo O2: braço d constante; ⊗ em cima do furo; L_z = −m v d = −0,12 ──
        self.an("B2-3")
        self.play(OpVivo(r1, entra=False), FadeOut(L0), self.luz1.animate.set_value(0.0), run_time=0.4)
        self.remove(r1)
        r2 = vivo(r_de(O2))
        self.gat("em relação ao furo")
        self.play(OpVivo(r2), self.luz2.animate.set_value(1.0), *troca_ref(0, 1), run_time=0.6)
        self.gat("sentido horário")
        x_in = sai_entra(self.tela(O2), saindo=False, r=0.24)
        self.play(FadeIn(x_in, scale=0.7), run_time=0.5)
        # caso 13: nas contas o disco para e o selo sai
        self.anda(0.0)
        self.sem_selo()
        self.pilha.limpa()
        A, ia = Mx(r"\vec L", "=", r"\vec r", r"\times", r"\vec p")
        self.pilha.poe(A)
        self.lei(A, ia, rt=0.9, metodo="lei")
        B, ib = Mx("L_z", "=", "-", "m", "v", "d", cores={5: VETC})
        self.pilha.poe(B)
        self.gat("o momento angular vale menos")
        self.lei(B, ib, {3: h_m, 4: h_v, 5: h_d}, rt=1.3)
        C, ic = Mx("=", "-", r"0{,}20", r"\cdot", r"1{,}5", r"\cdot", r"0{,}40", cores={2: MAS, 4: VEL, 6: VETC})
        self.pilha.poe(C)
        self.lei(C, ic, {2: h_m, 4: h_v, 6: h_d}, rt=1.4, numero=True)
        Dm, idm = Mx("=", "-", r"0{,}12", r"\,\mathrm{kg\,m^2/s}", cores={2: LMAG})
        self.pilha.poe(Dm)
        self.gat("zero vírgula doze")
        self.lei(Dm, idm, rt=0.9, numero=True)
        self.resultado(Dm, LMAG)
        lz2 = VGroup(T("L_z", 40, LMAG), T("=-", 40, WHITE_), T(r"0{,}12", 40, LMAG)).arrange(RIGHT, buff=0.1).move_to(self.tela((0.30, -0.52, 0.0)) + P3(0.55, 0.0))      # v5: canto inferior fixo da mesa, longe de d e do pino
        self.gat("o sinal negativo")
        self.play(FadeIn(lz2), Indicate(x_in, color=LMAG, scale_factor=1.3), run_time=0.7)
        self.anda(0.25)
        self.selo("CÂMERA LENTA", "×0,25")
        self.ate(0.99)

        # ── B2-4: em relação a O3 (do outro lado): ⊙ em cima do pino e L_z = +0,12 ao lado dele ──
        self.an("B2-4")
        self.play(OpVivo(r2, entra=False), FadeOut(VGroup(x_in, lz2)), self.luz2.animate.set_value(0.0), run_time=0.4)
        self.remove(r2)
        r3 = vivo(r_de(O3))
        self.gat("do outro lado da reta")
        self.play(OpVivo(r3), self.luz3.animate.set_value(1.0), *troca_ref(1, 2), run_time=0.6)
        o_out = sai_entra(self.tela(O3), saindo=True, r=0.24)
        L3 = VGroup(T("L_z", 44, LMAG), T(r"=\,+", 44, WHITE_), T(r"0{,}12", 44, LMAG)).arrange(RIGHT, buff=0.08)
        L3.move_to(self.tela(O3) + P3(-0.15, 0.80))                 # v5: canto superior direito do pino O3 (fora de O1, p⃗ e r⃗)
        self.gat("troca de sinal")
        self.play(FadeIn(o_out, scale=0.7), FadeIn(L3), run_time=0.6)
        self.anda(0.0)
        self.sem_selo()
        self.gat("não é uma propriedade só da partícula")
        frase = txt("DEPENDE DO PONTO", 32, bold=True, color=LMAG)
        self.pilha.poe(frase)
        self.play(FadeIn(frase), Indicate(o_out, color=LMAG, scale_factor=1.25), run_time=0.6)
        self.ate(0.99)

        # ── B2-5: quatro triângulos de Δt = 0,25 s a partir do furo, varridos em tempo real; hold de 2 s ──
        self.an("B2-5")
        self.pilha.limpa()
        self.play(OpVivo(r3, entra=False), FadeOut(VGroup(o_out, L3)), self.luz3.animate.set_value(0.0), run_time=0.4)
        self.remove(r3)
        self._loop = False
        self.anda(0.0, tf=0.0)
        f_t = txt("TRIÂNGULOS DE MESMO TEMPO", 30, bold=True, color=GEO)
        self.pilha.poe(f_t)
        self.play(FadeIn(f_t), run_time=0.4)
        self.selo("CÂMERA LENTA", "×0,25")
        self.gat("liga o furo ao disco")
        self.play(self.luz2.animate.set_value(1.0), *troca_ref(2, 1), run_time=0.5)
        self.anda(0.25, tf=0.0)
        ops = (0.40, 0.25, 0.40, 0.25)
        dx = 0.375

        def tri_vivo(k):
            xa = F.RETA_X0 + dx * k

            def f():
                x = min(self.disco()[0], xa + dx)
                if x <= xa + 1e-4:
                    return VGroup()
                return area_lab([self.tela(O2), self.tela((xa, Y, 0.012)), self.tela((x, Y, 0.012))], op=ops[k])
            return vivo(f)
        tris = [tri_vivo(k) for k in range(4)]
        raio = vivo(lambda: Line(self.tela(O2), self.tela(D3())).set_stroke(GEO, 3).set_z_index(8))
        self.add(*tris, raio)
        self.gat("olha a área")
        def cen(k):               # centroide do triângulo k (o número mora DENTRO dele; §3 #2)
            return (self.tela(O2) + self.tela((F.RETA_X0 + dx * k, Y, 0)) + self.tela((F.RETA_X0 + dx * (k + 1), Y, 0))) / 3
        GL = mix(GEO, 0.55)
        nums = []
        for k in range(4):
            self.wait(0.45)
            n_ = T(r"0{,}075", 36, GL).move_to(cen(k)).set_z_index(15)
            self.play(FadeIn(n_, scale=1.2), run_time=0.25)
            self.wait(0.30)                                   # acende e some em 1 s: o anterior sai antes do próximo
            self.play(FadeOut(n_), run_time=0.2)
        self.remove(raio)
        self.anda(0.0)
        self.sem_selo()
        alt = cota          # a altura dos triângulos é a própria cota d (x = 0,72 m), fora da área dos números
        bases = VGroup(*[Line(self.tela((F.RETA_X0 + dx * k, Y + 0.03, 0)), self.tela((F.RETA_X0 + dx * (k + 1), Y + 0.03, 0))).set_stroke(VETC, 4) for k in range(4)])
        lb = T(r"0{,}375\,\mathrm{m}", 36, VETC).move_to(self.tela((F.RETA_X0 + dx * 2.0, Y, 0)) + P3(0, 0.62))
        self.gat("a altura até o furo")
        self.play(Indicate(cota, color=VETC, scale_factor=1.0), Create(bases), FadeIn(lb), run_time=0.6)
        self.gat("têm a mesma área")
        for k in range(4):                      # §3 #2: de novo um por vez (os quatro lado a lado se encostam a 36 pt)
            n_ = T(r"0{,}075", 36, GL).move_to(cen(k)).set_z_index(15)
            self.play(FadeIn(n_, scale=1.2), run_time=0.2)
            self.wait(0.15)
            self.play(FadeOut(n_), run_time=0.2)
        frase2 = txt("ÁREAS IGUAIS EM TEMPOS IGUAIS", 32, bold=True, color=GEO)
        self.pilha.poe(frase2)
        self.gat("áreas iguais em tempos iguais")
        self.play(FadeIn(frase2), run_time=0.5)
        self.ate(0.99)

        # ── B2-6: dA = ½|r⃗ × v⃗ dt| → dA/dt = |r⃗ × p⃗|/2m → |L⃗|/2m = 0,30 m²/s ──
        self.an("B2-6")
        self.play(FadeOut(VGroup(lb, bases)), run_time=0.3)
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
        A3, a3 = Mx(r"\frac{dA}{dt}", "=", r"\frac{|\vec L|}{2m}")
        self.pilha.poe(A3)
        self.gat("aparece o momento angular")
        self.gm(A2, A3, ([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]), ([6], [6]), ([7, 8, 9, 10, 11], [7, 8]), ([12], [9]), ([13], [10]), ([14], [11]),
                ([15], [12]), rt=1.4)
        self.resultado(A3, GEO)
        A4, a4 = Mx("=", r"0{,}30", r"\,\mathrm{m^2/s}", cores={1: GEO})
        self.pilha.poe(A4)
        self.gat("momento angular constante")
        self.lei(A4, a4, rt=0.9, numero=True)
        # fim do bloco: os triângulos repintam (pausa útil) e a mesa nunca fica vazia
        self.ate(0.995)
