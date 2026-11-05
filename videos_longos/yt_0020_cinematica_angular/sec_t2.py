"""Lote PT2 (v2): T2 — quão rápido gira? Disco de referência (giro de tela ~0,25 volta/s, anti-horário).
T2-1 estroboscopia: o RAIO PINTADO deixa cópias (60% → 15%, no máximo 4) separadas por Δt iguais (régua de tempo embaixo); ω_méd = Δθ/Δt.
T2-2 Δt encolhe; ω = lim Δθ/Δt = dθ/dt (passo); rad/s; seta curva ω. T2-3 os três pontos varrem o mesmo Δθ no mesmo Δt (arcos que seguem os pontos;
auditoria MESMO ω). T2-4 rpm → rad/s com a hélice 2D GRANDE no lugar do disco; o 282,7 voa da CONTA para o cubo. T2-5 cronômetro de voltas (cada volta
acende um segmento do anel com o tempo escrito ao lado); |ω| = 2πf → = 2π/T (passo f → /T); depois o disco acelera e as voltas ficam diferentes.
Álgebra do v2: nenhuma linha de equação da CONTA entra por FadeIn de linha inteira (escrita em ordem, voos do desenho, passo/TransformByGlyphMap)."""
from pecas20 import *  # noqa: F401,F403

W_T = PI / 2                     # rad/s de tela (0,25 volta/s)
RH, RC, W_H = 2.57, 1.1, PI    # hélice 2D (T2-4): raio, raio do cubo (o 282,7 cabe dentro dele) e giro de tela (rad/s, CÂMERA LENTA)
CD, RD, TR = P3(4.95, -2.32), 0.8, 22.0    # cronômetro (T2-5): centro, raio do anel e janela do anel (s; recomeça antes das voltas aceleradas)


def pos_dth(C, R, am, smin=-0.8226):
    """Rótulo Δθ FORA do disco e do arco, no ângulo médio do arco. À direita ele se afasta (rho maior) para não cair sobre a linha de referência
    tracejada; em cima e embaixo (zona do ESQUEMA, régua de tempo) fica parado na borda do setor, no lado mais próximo (smin = seno mínimo)."""
    rho = R + 0.5 + 0.55 * max(0.0, math.cos(am)) ** 4
    sc = min(0.8387 * (R + 0.5) / rho, max(smin * (R + 0.5) / rho, math.sin(am)))
    cs = (1 if math.cos(am) >= 0 else -1) * math.sqrt(max(0.0, 1 - sc * sc))
    return C + rho * P3(cs, sc)


def numw(s_, cor=WHITE_, size=40):
    """num_mob com um respiro entre os glifos (vírgula não encosta no dígito)."""
    g = num_mob(s_, cor, size)
    for i, m in enumerate(g):
        m.shift(RIGHT * 0.035 * i * size / 40)
    return g


def helice2d(c, R, ang, rc=RC):
    """D14 sem 3D: hélice vista de frente, três pás de aço com perfil de aerofólio (corda larga no cubo, afinando até a ponta, leve curvatura),
    faixa clara na ponta de cada pá (o ponto que vai a 967 km/h) e o cubo grande, onde pousa o 282,7. Pá 0 em `ang`; giro anti-horário."""
    g = VGroup()
    r0 = rc - 0.02                                              # raiz da pá fora da caixa do 282,7 (com a folga do G28)
    for k in range(3):
        a = ang + 2 * PI * k / 3
        u, t = P3(math.cos(a), math.sin(a)), P3(-math.sin(a), math.cos(a))

        def borda(s, lado):                                     # lado +1: bordo de ataque (frente do giro); −1: bordo de fuga
            q = (s - r0) / (R - r0)
            corda = R * (0.30 - 0.19 * q)
            return c + u * s + t * (corda * (0.42 if lado > 0 else -0.58) + 0.02 * R * math.sin(PI * q))
        ss = np.linspace(r0, 0.975 * R, 14)
        pa = Polygon(*([borda(s, 1) for s in ss] + [c + u * R + t * 0.03 * R] + [borda(s, -1) for s in ss[::-1]]))
        g.add(aco(pa, 1.6))
        sf = np.linspace(0.84 * R, 0.91 * R, 4)
        g.add(Polygon(*([borda(s, 1) for s in sf] + [borda(s, -1) for s in sf[::-1]])).set_stroke(width=0).set_fill("#E6ECF7", 0.92))
    g.add(aco(Circle(radius=rc).move_to(c), 2.2).set_fill("#2B3445", 1))   # cubo escuro: o 282,7 violeta tem contraste
    return g.set_z_index(5)


class LoteT2(L20):

    def _selo_mob(self, *a, **k):
        """G1: selo de duas linhas com respiro vertical (padding) dentro da caixa."""
        s_ = super()._selo_mob(*a, **k)
        bx, g_ = s_[0], s_[1]
        bx.stretch_to_fit_height(g_.height + 0.38).move_to(g_)
        return s_

    def selo(self, tag, corpo, cor=CYAN, borda=BLUE_L, **k):
        """A pilha desce ANTES de o selo entrar (0,4 s), para o selo não passar por cima da linha de cima."""
        from prob2 import Y_SELO_TOPO, TOPO_PILHA
        novo = self._selo_mob(tag, corpo, cor, borda, wmax=k.get("wmax", LARG_CONTA))
        topo = min(TOPO_PILHA, Y_SELO_TOPO - novo.height - 0.15)
        if abs(topo - self.pilha.topo) > 1e-3 and self.s1 is None:
            self.pilha.topo = topo
            y, mov = topo, []
            for l, d in self.pilha.linhas:
                mov.append(l.animate.move_to(P3(self.pilha.x0 + d + l.width / 2, y - l.height / 2)))
                y -= l.height + self.pilha.buff
            self.play(*mov, run_time=0.4)
        return super().selo(tag, corpo, cor=cor, borda=borda, **k)

    def construct(self):
        self.setup_base()
        self.t2()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def t2(self):
        d = DiscoRef(self, th0=0.4)
        self.add(d.g)
        C, R = d.C, d.R
        # θ(t) do lote: integrado de uma velocidade de tela ω_tela(t) (tracker), de modo que as cópias da estroboscopia saem da história real
        DT1 = 0.8                                                       # Δt da estroboscopia (72°: sem cópias opostas, que pareceriam diâmetros)
        w_t = ValueTracker(0.0)
        self.add(w_t)
        hist = {"t": [0.0], "th": [0.4]}

        def integra(m):
            t = self.clk.get_value()
            if t > hist["t"][-1] + 1e-9:
                th = hist["th"][-1] + w_t.get_value() * (t - hist["t"][-1])
                hist["t"].append(t)
                hist["th"].append(th)
                d.th.set_value(th)
        motor = VGroup()
        motor.add_updater(integra)
        self.add(motor)

        def th_em(t):
            return float(np.interp(t, hist["t"], hist["th"]))
        dts, op_s, nk = ValueTracker(DT1), ValueTracker(0.0), ValueTracker(0.0)
        self.add(dts, op_s, nk)
        X0, Y0, SR = -6.3, -3.55, 1.25                                    # régua de tempo: borda esquerda, altura e escala (u/s)
        SMIN = -0.55                                                     # S6: com a régua na tela, o Δθ não desce até a faixa do Δt

        def strobo():
            o = op_s.get_value()
            if o < 0.01:
                return VGroup()
            t = self.clk.get_value()
            g = VGroup()
            for k in range(1, 5):                                  # D11: cópias só do RAIO pintado, opacidade 60% → 15%, uma a uma
                th_k = th_em(t - k * dts.get_value())
                vis = min(1.0, max(0.0, nk.get_value() - (k - 1)))
                if vis > 0.01:
                    g.add(Line(C, C + R * P3(math.cos(th_k), math.sin(th_k))).set_stroke(WHITE_, 6, opacity=(0.6 - 0.15 * (k - 1)) * vis * o).set_z_index(5))
            th1 = th_em(t - dts.get_value())
            th0_ = th_em(t)
            g.add(arco(C, R + 0.15, th1, th0_, ANG, 9, o, z=8))
            la = mtex(r"\Delta\theta", ANG, 42)
            la.move_to(pos_dth(C, R, (th0_ + th1) / 2, SMIN))         # S6: fora do arco, fora do disco, longe da linha tracejada
            g.add(escala_op(la, o))
            # régua de tempo: marcas a cada Δt (as cópias são esses instantes)
            g.add(Line(P3(X0, Y0), P3(X0 + 5.0, Y0)).set_stroke(WHITE_, 2, opacity=0.7 * o))
            for k in range(0, 5):
                x = X0 + 5.0 - k * dts.get_value() * SR
                if x >= X0:
                    g.add(Line(P3(x, Y0 - 0.12), P3(x, Y0 + 0.12)).set_stroke(WHITE_, 3, opacity=o))
            lt = mtex(r"\Delta t", WHITE_, 40)
            lt.move_to(P3(X0 + 5.0 - 0.5 * dts.get_value() * SR, Y0 + 0.36))
            g.add(escala_op(lt, o))
            return g
        sv = vivo(strobo)
        self.add(sv)
        # ── T2-1 ──
        self.an("T2-1")
        self.secao("QUÃO RÁPIDO GIRA?")
        # coluna ocupada desde o primeiro quadro: a velocidade em 1D (a ideia que o ângulo vai copiar)
        v0 = txt("VELOCIDADE EM 1D (RETA)", 30, bold=True)
        V1, iv1 = eqf([r"v", "="], [r"\Delta x"], [r"\Delta t"], size=56, cores={("pre", 0): VEL})
        self.pilha.poe(v0)
        self.pilha.poe(V1)
        self.play(w_t.animate.set_value(W_T), FadeIn(v0), FadeIn(V1), run_time=1.0)
        self.gat("a ideia é a mesma da velocidade")
        self.play(op_s.animate.set_value(1.0), run_time=0.8)
        self.play(nk.animate(rate_func=linear).set_value(4.0), run_time=max(1.2, self.ate_t("a velocidade angular média") - 0.2))   # as cópias nascem uma a uma
        self.gat("a velocidade angular média")
        self.pilha.limpa(rt=0.35)
        A, ia = eqf([r"\omega_{m\acute{e}d}", "="], [r"\Delta\theta"], [r"\Delta t"], size=60, cores={("pre", 0): VEL, ("num", 0): ANG})
        for j in ia["pre"][0]:                                     # D12: o subscrito méd herda a cor e o corpo da letra (violeta cheio)
            A[0][j].set_color(VEL)
            A[0][j].set_stroke(VEL, width=1.8, background=False)
        self.pilha.poe(A)
        t = self.clk.get_value()
        la_ = mtex(r"\Delta\theta", ANG, 42).move_to(pos_dth(C, R, (th_em(t) + th_em(t - DT1)) / 2, SMIN))
        lt_ = mtex(r"\Delta t", WHITE_, 40).move_to(P3(X0 + 5.0 - 0.5 * DT1 * SR, Y0 + 0.36))
        # §5 T2-1: Δθ voa do arco entre duas cópias, Δt da régua; ω_méd, = e a barra são escritos na vaga (numerador → barra → denominador)
        # (o Δθ pousa junto com a barra: sozinha, a barra, mais larga, nasceria antes do numerador)
        self.voa([(la_, gl(A, ia["num"][0] + ia["bar"])), (lt_, gl(A, ia["den"][0]))], extra=[FadeIn(gl(A, ia["pre"][0] + ia["pre"][1]))], rt=1.1, origem=False)
        self.ate(0.99)
        # ── T2-2: Δt → 0 ──
        self.an("T2-2")
        self.gat("fazendo o intervalo de tempo ir a zero")
        self.play(dts.animate(rate_func=smooth).set_value(0.2), run_time=2.0)
        B, ib = M(r"\omega", "=", r"\lim_{\Delta t\to 0}", r"\frac{\Delta\theta}{\Delta t}", "=", r"\frac{d\theta}{dt}", size=56, cores={0: VEL})
        for j in ib[3][:2] + ib[5][1:2]:                           # só θ e Δθ em âmbar; d, dt e a barra ficam neutros (§2)
            B[0][j].set_color(ANG)
            B[0][j].set_stroke(ANG, width=1.8, background=False)
        self.pilha.poe(B)
        self.gat("a derivada do ângulo em relação ao tempo")
        # GM: o `lim` entra antes da fração; o Δ da fração vira o d de dθ/dt por glifo (cada Δ vai para a fração de cima e para o d de baixo)
        self.passo(A, B, (ia["pre"][0][:1], J(ib, 0)), (ia["pre"][0][1:], []), (ia["pre"][1], J(ib, 1)), ([], J(ib, 2)),
                   (ia["num"][0][:1], [ib[3][0], ib[5][0]]), (ia["num"][0][1:], [ib[3][1], ib[5][1]]),
                   (ia["bar"], ib[3][2:3]), (ia["den"][0][:1], [ib[3][3], ib[5][3]]), (ia["den"][0][1:], [ib[3][4], ib[5][4]]),
                   ([], J(ib, 4)), ([], ib[5][2:3]), rt=1.3)
        for j in ib[5][0:1] + ib[5][2:5] + ib[3][2:5]:             # garante d, dt, barras brancos depois do passo (§2)
            if j in ib[5][:1] + ib[5][2:5] or B[0][j].width > 0.0:
                B[0][j].set_color(WHITE_)
                B[0][j].set_stroke(WHITE_, width=1.8, background=False)
        U, iu = M(r"[\omega]", "=", r"\mathrm{rad/s}", size=52, cores={0: VEL, 2: VEL})
        self.pilha.poe(U)
        self.gat("a unidade é radiano por segundo")
        self.play(FadeIn(U), run_time=0.6)
        # seta curva ω no disco (ω > 0 anti-horário; depois ω < 0 horário)
        sgn = ValueTracker(1.0)
        self.add(sgn)

        def seta_w():
            s = sgn.get_value()
            g = VGroup(seta_curva(C, R + 0.32, 0.9 if s > 0 else 1.9, 1.0 * (1 if s > 0 else -1), VEL, 8))
            lw = mtex(r"\omega > 0" if s > 0 else r"\omega < 0", VEL, 42)
            aw = 2.3 if s > 0 else 0.5                                  # ao lado da ponta da seta, longe do caminho dos pontos da borda
            lw.move_to(C + (R + 0.85) * P3(math.cos(aw), math.sin(aw)))
            g.add(lw)
            return g
        swv = vivo(seta_w)
        self.gat("velocidade angular positiva é giro anti horário")
        self.play(FadeIn(swv), op_s.animate.set_value(0.0), run_time=0.6)
        self.gat("negativa horário")
        self.play(w_t.animate.set_value(-W_T), run_time=0.5)
        sgn.set_value(-1.0)
        self.wait(0.3)
        self.play(w_t.animate.set_value(W_T), run_time=0.5)
        sgn.set_value(1.0)
        self.ate(0.99)
        # ── T2-3: mesmo ω para o corpo todo ──
        self.an("T2-3")
        self.pilha.limpa(rt=0.35, anims=[FadeOut(swv)])
        fr = VGroup(linha_m(txt("MESMO", 30, bold=True), lbl(r"\omega", VEL, 56), buff=0.14), txt("PARA O CORPO TODO", 30, bold=True)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.12)                # duas linhas: cabe na CONTA sem encolher
        self.pilha.poe(fr)
        self.play(FadeIn(fr), run_time=0.5)      # coluna ocupada desde o começo do T2-3
        self.remove(swv, sv)
        t_ini = ValueTracker(-1.0)
        op3 = ValueTracker(0.0)
        self.add(t_ini, op3)
        DT = 1.2

        def tres():
            o = op3.get_value()
            if o < 0.01:
                return VGroup()
            t = self.clk.get_value()
            t0 = t_ini.get_value()
            th2 = d.th.get_value()
            th1 = th_em(max(t0, t - DT))                           # o arco segue os pontos: sempre o giro do último Δt
            g = VGroup()
            for k in (1, 2, 3):                                    # D13: arcos âmbar grossos varridos pelos próprios pontos (sem linhas cinza do centro)
                g.add(arco(C, R * k / 3, th1, th2, ANG, 10, o, z=8))
                g.add(Circle(radius=0.1).move_to(d.p(k, th1)).set_fill(opacity=0).set_stroke(WHITE_, 3, opacity=0.7 * o).set_z_index(8))   # onde cada ponto estava
            g.add(arco(C, 0.42, th1, th2, ANG, 10, o, z=8))         # o MESMO Δθ, marcado uma vez perto do centro
            la = mtex(r"\Delta\theta", ANG, 42).move_to(pos_dth(C, R, (th1 + th2) / 2))
            g.add(escala_op(la, o))
            if not PEDIDOS3D and t >= t0 + DT:
                self.reg("mesmo_w", dth=[(th2 - th1)] * 3, dt=DT, s=[R * k / 3 * (th2 - th1) for k in (1, 2, 3)])
            u, n = d.u()
            for k in (1, 2, 3):                                    # setas violeta cheias (opacidade 100%, espessura 6), 1 : 2 : 3
                p = d.p(k)
                g.add(seta(p, p + n * 0.42 * k, VEL, 8, op=o, z=9))
            return g
        tv = vivo(tres)
        self.add(tv)
        self.gat("os três pontos varrem o mesmo ângulo")
        t_ini.set_value(self.clk.get_value())
        self.play(op3.animate.set_value(1.0), run_time=DT)
        self.foco = fr
        self.gat("então todos têm a mesma velocidade angular")
        W3, iw3 = eqf([r"\omega", "="], [r"\Delta\theta"], [r"\Delta t"], size=60, cores={("pre", 0): VEL, ("num", 0): ANG})
        self.pilha.poe(W3, dx=0.1)
        self.voa([(fr[0][1], gl(W3, iw3["pre"][0]))], extra=[FadeIn(gl(W3, iw3["pre"][1] + iw3["num"][0] + iw3["bar"] + iw3["den"][0]))], rt=1.2)
        self.foco = W3
        self.gat("a velocidade angular não é de um ponto")
        self.wait(1.5)
        self.gat("já a velocidade de cada ponto")
        self.play(Indicate(tv, color=WHITE_, scale_factor=1.0), run_time=0.8)
        self.ate(0.99)
        # ── T2-4: rpm → rad/s, com a hélice grande no lugar do disco ──
        self.an("T2-4")
        self.pilha.limpa(rt=0.35, anims=[op3.animate.set_value(0.0)])
        self.remove(tv)
        t_h = self.clk.get_value()
        hv = vivo(lambda: helice2d(C, RH, 0.35 + W_H * (self.clk.get_value() - t_h)))
        sh = seta_curva(C, RH + 0.32, 0.25, 1.0, VEL, 8)                   # sentido do giro (anti-horário), por fora das pontas
        lh = valor(r"2{.}700\ \mathrm{RPM}", VEL, 44).move_to(P3(-1.35, -3.1))
        hub = lbl(r"282{,}7", VEL, 50).move_to(C)                       # §6: o 282,7 violeta grande, dentro do cubo
        A4, ia4 = M(r"1\ \mathrm{RPM}", "=", r"\frac{2\pi\ \mathrm{rad}}{60\ \mathrm{s}}", size=56, cores={0: VEL})
        for j in ia4[2][:5]:
            A4[0][j].set_color(ANG)
        self.pilha.poe(A4)
        self.gat("motor e ventilador vêm em rotações por minuto")
        self.play(FadeOut(d.g), FadeIn(hv), FadeIn(sh), FadeIn(lh), FadeIn(A4), *self.troca_marcador("CÂMERA LENTA ×90", lado="esq"), run_time=1.2)
        self.remove(d.g)
        self.gat("cada volta vale dois pi radianos")
        self.wait(1.0)
        B4, ib4 = M(r"2{.}700", r"\cdot", r"\frac{2\pi}{60}", size=56, cores={0: VEL})
        for j in ib4[2][:2]:
            B4[0][j].set_color(ANG)
        R4, ir4 = M(r"\approx", r"282{,}7", r"\ \mathrm{rad/s}", size=56, cores={1: VEL, 2: VEL})
        R4b = caixa_l(R4, VEL)
        self.pilha.poe(B4)
        self.pilha.poe(R4b, dx=0.5)
        self.gat("a hélice do começo")
        # §5 T2-4: 2.700 voa do rótulo da hélice; 2π e 60 voam da linha de cima; · e a barra são escritos na vaga (numerador → barra → denominador)
        # (a barra viaja junto com o 2π: a fila ordena por x e a barra, mais larga, passaria na frente do numerador)
        self.voa([(lh[0][:5], mp(B4, ib4, [0])), (gl(A4, ia4[2][0:2] + ia4[2][5:6]), gl(B4, ib4[2][0:3])), (gl(A4, ia4[2][6:8]), gl(B4, ib4[2][3:5]))],
                 extra=[FadeIn(mp(B4, ib4, [1]))], rt=1.6, origem=False)
        self.gat("gira a uns duzentos e oitenta e três")
        self.play(FadeIn(R4b), run_time=0.8)                           # resultado E (caixa e conteúdo juntos)
        self.voa([(mp(R4, ir4, [1]), hub)], rt=0.6, origem=False, alvo=hub)   # D14: o 282,7 voa da CONTA para o cubo da hélice
        self.foco = R4b
        self.ate(0.99)
        # ── T2-5: f e T ──
        self.an("T2-5")
        self.play(FadeOut(hub), run_time=0.25)                         # o 282,7 sai antes de o disco voltar (nunca sobre a linha pintada)
        self.remove(hub)
        self.pilha.limpa(rt=0.35, anims=[FadeOut(hv), FadeOut(sh), FadeOut(lh), *self.troca_marcador(None), FadeIn(d.g)])
        self.remove(hv, sh, lh)
        voltas = {"ini": None, "lista": []}
        # cronômetro de voltas (D15): cada volta acende um segmento do anel, de comprimento ∝ à duração da volta, com o tempo escrito ao lado
        win = {"cum": 0.0, "segs": []}

        def seg_anel(a0_s, dur_, k=0):
            """Segmento do anel: começa em a0_s segundos da janela de TR s (sentido horário a partir do topo); folga fina entre segmentos."""
            ang0 = PI / 2 - 2 * PI * a0_s / TR - 0.03
            ang1 = PI / 2 - 2 * PI * (a0_s + dur_) / TR + 0.03
            return arco(CD, RD, ang0, min(ang0 - 0.01, ang1), ANG, 12, 1.0 if k % 2 == 0 else 0.6, z=6)

        def poe_labs(labs):
            """Tempo de cada volta ao lado do seu segmento: do lado (esq/dir) do meio do segmento, na altura dele, dentro da faixa do cronômetro
            (abaixo da CONTA); rótulos do mesmo lado empilhados com folga; x empurrado para fora até não encostar no anel."""
            for s in (1, -1):
                lado = sorted([(lab, CD[1] + (RD + 0.5) * math.sin(am)) for lab, am in labs if (math.cos(am) >= 0) == (s > 0)], key=lambda p: -p[1])
                ys, h = [], 0.5
                for _, y in lado:
                    ys.append(min(y, -1.65, ys[-1] - h) if ys else min(y, -1.65))
                for i in range(len(ys) - 1, -1, -1):
                    ys[i] = max(ys[i], -3.12 if i == len(ys) - 1 else ys[i + 1] + h)
                for (lab, _), y in zip(lado, ys):
                    w2, h2 = lab.width / 2, lab.height / 2
                    x = CD[0] + s * (w2 + 0.1)
                    while math.hypot(max(abs(x - CD[0]) - w2, 0.0), max(abs(y - CD[1]) - h2, 0.0)) < RD + 0.3:
                        x += 0.05 * s
                    lab.move_to(P3(x, y))

        def crono():
            t = self.clk.get_value()
            th = d.th.get_value()
            if voltas["ini"] is None:
                voltas["ini"] = (t, th)
            t0, th0 = voltas["ini"]
            if th - th0 >= 2 * PI:
                dur_ = t - t0
                voltas["lista"].append(dur_)
                voltas["ini"] = (t, th0 + 2 * PI)
                t0, th0 = t, th0 + 2 * PI
                if win["cum"] + dur_ > TR:                           # o anel dá a volta toda (TR s): recomeça
                    win["cum"], win["segs"] = 0.0, []
                win["segs"].append((win["cum"], dur_))
                win["cum"] += dur_
            g = VGroup(Circle(radius=RD).move_to(CD).set_stroke(GEO, 3, opacity=0.35).set_z_index(4))
            labs = []
            for k, (a0_s, dur_) in enumerate(win["segs"]):
                n_ = len(voltas["lista"]) - len(win["segs"]) + k
                g.add(seg_anel(a0_s, dur_, k=n_))
                am = PI / 2 - 2 * PI * (a0_s + dur_ / 2) / TR
                labs.append((VGroup(numw(f"{dur_:.1f}".replace(".", ","), WHITE_, 36), lbl(r"\mathrm{s}", WHITE_, 36)).arrange(RIGHT, buff=0.06), am))
            poe_labs(labs)
            g.add(*[l for l, _ in labs])
            vivo_ = min(t - t0, max(0.0, TR - win["cum"]))
            if vivo_ > 0.08:
                g.add(seg_anel(win["cum"], vivo_, k=len(voltas["lista"])))
            g.add(arco(C, R + 0.22, th0, th, ANG, 6, 0.9, z=4))
            g.add(txt("VOLTA ATUAL", 26).move_to(P3(0.9, -2.1), aligned_edge=LEFT))
            g.add(VGroup(numw(f"{t - t0:.1f}".replace(".", ","), WHITE_, 46), lbl(r"\mathrm{s}", WHITE_, 46)).arrange(RIGHT, buff=0.1)
                  .move_to(P3(0.9, -2.75), aligned_edge=LEFT))
            return g
        cr = vivo(crono)
        self.pilha.base = -1.35                                       # o cronômetro mora embaixo da CONTA
        self.gat("quando o giro é uniforme")
        self.play(FadeIn(cr), run_time=0.5)
        n1 = linha_m(lbl("f", VEL, 46), txt("= VOLTAS POR SEGUNDO", 26), lbl(r"(\mathrm{Hz})", WHITE_, 40), buff=0.15)
        n2 = linha_m(lbl("T", WHITE_, 46), txt("= TEMPO DE UMA VOLTA", 26), buff=0.15)
        F1, i1 = M(r"|\omega|", "=", r"2\pi f", size=60, cores={0: VEL})
        F1[0][i1[2][2]].set_color(VEL)
        for j in i1[2][:2]:
            F1[0][j].set_color(ANG)
        F2, i2 = M("=", r"\frac{2\pi}{T}", size=60)
        for j in i2[1][:2]:
            F2[0][j].set_color(ANG)
        self.gat("a frequência que é o número de voltas")
        self.pilha.poe(n1, dx=0.1)
        self.play(FadeIn(n1), run_time=0.6)
        self.gat("e o período que é o tempo de uma volta")
        self.pilha.poe(n2, dx=0.1)
        self.play(FadeIn(n2), run_time=0.6)
        self.gat("o tamanho da velocidade angular é dois pi")
        self.pilha.poe(F1, dx=0.1)
        # §5 T2-5: f voa da linha que o define; |ω|, = e 2π são escritos na vaga
        self.voa([(n1[0], gl(F1, i1[2][2:3]))], extra=[FadeIn(gl(F1, J(i1, 0, 1) + i1[2][:2]))], rt=1.2)
        self.gat("ou dois pi dividido pelo período")
        self.pilha.poe(F2)
        # GM f → /T (a filha nasce na vaga de baixo, "=" sob o "="; o |ω| da linha de cima não desce)
        self.passo(F1, F2, (J(i1, 0), []), (J(i1, 1), J(i2, 0)), (i1[2][:2], i2[1][:2]), (i1[2][2:3], i2[1][2:4]), rt=1.2)
        self.gat("repara nas duas ressalvas")
        self.selo("ATENÇÃO", [["SÓ COM GIRO UNIFORME ·", lbl("f>0", VEL, 34)], ["MESMO NO GIRO HORÁRIO"]])
        self.gat("é o tamanho porque a frequência")
        self.ind(F1, i1, [0], color=WHITE_)
        self.gat("e só vale com giro uniforme")
        self.play(w_t.animate(rate_func=linear).set_value(2.6 * W_T), run_time=self.ate_t("e não existe um período só"))
        self.gat("e não existe um período só")
        self.play(w_t.animate.set_value(W_T), run_time=1.0)
        self.ate(0.99)
        motor.clear_updaters()
