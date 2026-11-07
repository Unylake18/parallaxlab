"""Lote PH: hook H1–H3 (Three.js 'helice': três pás de aço, diâmetro 1,9 m, câmera frontal ao disco da hélice) e abertura A1–A3.
Giro desenhado a 0,5 volta/s (CÂMERA LENTA ×90; real 2.700 rpm = 45 voltas/s). Marcadores a 0,10 m e 0,95 m na MESMA pá (pá 0), presos pelo Manim
pela mesma câmera do Three.js (projeta3d); setas violeta tangentes proporcionais ao raio (1 : 9,5), recalculadas a cada quadro.
Os valores (≈ 100 km/h, ≈ 970 km/h) nascem no marcador e vão para a legenda fixa à direita (texto nunca sobre a pá que gira)."""
from pecas20 import *  # noqa: F401,F403

REV_TELA = 0.5                     # voltas/s desenhadas (45 / 0,5 = ×90)
K_H, C_H = 3.06, P3(-3.7, 0.35)    # v3 §4: D ≈ 5,85 u = 65% da altura (9 u); C_H = centro final (coluna da direita em H2); em H1 ela fica no centro da tela (X_H1)
X_H1 = 0.0
L_PONTA = 1.45                     # seta da ponta (cena); a de 10 cm é L_PONTA / 9,5 (a varredura da seta fica dentro de 2,75 do eixo: rótulos fora)
DT_RASTRO = 0.45                   # v2 D2: os dois pontos deixam rastro do mesmo intervalo de tempo (0,45 s de tela = 0,225 volta)


class GiroHel:
    """Ângulo da hélice no tempo do lote: giro uniforme a REV_TELA a partir de t0 (anti-horário)."""

    def __init__(self, t0=0.0, a0=0.35):
        self.t0, self.a0 = t0, a0

    def ang(self, t):
        return self.a0 + 2 * PI * REV_TELA * (t - self.t0)


def camada_helice(cena, giro, camf, k_seta, op_set, op_mk, pulso=None, op_rastro=None):
    """Marcadores (10 cm e 95 cm na pá 0), setas violeta tangentes ∝ r, anel no ponto de 10 cm (a seta dele é 1 : 9,5) e rastros de mesmo Δt, a cada quadro."""
    def f():
        t_ = cena.clk.get_value()
        a = giro.ang(t_)
        cam = camf()
        g = VGroup()
        o = op_set.get_value()
        orr = op_rastro.get_value() if op_rastro is not None else 0.0
        c = projeta3d(cam, (0, -0.07, 0))
        for r in (0.10, 0.95):
            p = hel_pt(cam, r, a)
            t = P3(-math.sin(a), math.cos(a))
            L = L_PONTA * r / 0.95
            kk = k_seta.get_value()                    # 0: hipótese "todo ponto igual" (tracejada); 1: proporcional ao raio
            L = (1 - kk) * L_PONTA * 0.5 + kk * L
            if r > 0.5 and abs(t[1]) > 1e-6:           # v8: a seta da ponta não passa do topo do ESQUEMA (2,42) nem do selo de câmera lenta (−3,12)
                for lim_ in (2.42, -3.12):
                    Lc = (lim_ - p[1]) / t[1]
                    if 0 < Lc < L:
                        L = max(Lc, 0.45)
            w = 12 + (2 * pulso.get_value() if pulso is not None else 0)
            if orr > 0.01:                              # v2 D2: rastro do ponto nos últimos DT_RASTRO s (violeta que some para trás): curto no cubo, longo na ponta
                n_ = 12
                for k in range(n_):
                    a0, a1 = giro.ang(t_ - DT_RASTRO * (k + 1) / n_), giro.ang(t_ - DT_RASTRO * k / n_)
                    g.add(Line(hel_pt(cam, r, a0), hel_pt(cam, r, a1)).set_stroke(VEL, 3.2 + 2.2 * (1 - k / n_), opacity=orr * (1 - k / n_) ** 1.3).set_z_index(10))
            if o > 0.01:
                if kk < 0.999:
                    g.add(DashedVMobject(Line(p, p + t * L), num_dashes=max(3, int(L * 6))).set_stroke(VEL, 5, opacity=o * 0.6).set_z_index(11))
                else:
                    g.add(seta(p, p + t * L, VEL, w, tip=min(0.24, 0.45 * L + 0.05), op=o, z=11))
                    if r < 0.5:                         # anel de destaque na seta curta (menos de 0,2 u): ela existe, é só pequena
                        g.add(Circle(radius=0.2).move_to(p + t * L / 2).set_stroke(WHITE_, 2.4, opacity=o * 0.85).set_z_index(12))
            if op_mk.get_value() > 0.01:
                g.add(escala_op(ponto_mob(p, 0.075, z=12), op_mk.get_value()))
            if kk > 0.999 and not PEDIDOS3D:
                cena.reg("helice", r=r, L=L, p=p, c=c, ang=a)
        return g
    return vivo(f)


class LoteHook(L20):
    FUNDO = "fundo_lab.png"

    def construct(self):
        self.setup_base()
        self.hook()
        self.abertura()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def hook(self):
        xs = ValueTracker(X_H1)
        self.add(xs)

        def cam():
            return cam_hel(K_H, P3(xs.get_value(), C_H[1]))
        giro = GiroHel()
        op3 = 0.0
        f3 = Fundo3D(self, "helice", lambda t: {"ang": round(giro.ang(t), 4), "cam": cam()}, op=0.0)
        self.add(f3)
        k_seta, op_set, op_mk, pulso, op_rastro = (ValueTracker(v) for v in (0.0, 0.0, 0.0, 0.0, 0.0))
        self.add(k_seta, op_set, op_mk, pulso, op_rastro)
        cam_ = camada_helice(self, giro, cam, k_seta, op_set, op_mk, pulso, op_rastro)
        self.add(cam_)
        # ── H1 ──
        self.an("H1")
        self.play(f3.op.animate.set_value(1.0), run_time=1.0)
        self.play(*self.troca_marcador("CÂMERA LENTA ×90", "esq"), run_time=0.4)          # v2 §3: marcador de canto, um por vez, fora da faixa de selos
        self.gat("ela gira inteira junto")
        self.play(op_mk.animate.set_value(1.0), run_time=0.6)
        self.gat("então dá vontade de dizer")
        self.play(op_set.animate.set_value(1.0), run_time=0.8)
        self.gat("só que não anda")
        self.play(k_seta.animate.set_value(1.0), run_time=1.0)
        self.play(op_rastro.animate.set_value(1.0), run_time=0.8)                                  # v2 D2: rastros de mesmo Δt mostram a diferença que a seta curta esconde
        self.ate(0.99)
        # ── H2: números típicos ──
        self.an("H2")
        self.play(xs.animate(rate_func=smooth).set_value(C_H[0]), run_time=1.2)          # v3 §4: a hélice desliza do centro para a esquerda quando a coluna vai entrar
        # v2 S1: seta curva NO CUBO (gira no sentido da hélice); a seta da ponta varre r ≤ 2,75 u, então nada dela cruza o cubo; o valor vai para a legenda
        arc_rpm = seta_curva(C_H, 0.62, 2.55, 1.6, VEL, 9, tip=0.2)
        y_cota = -2.95
        cota_ = VGroup(Line(P3(C_H[0] - K_H * 0.95, y_cota), P3(C_H[0] + K_H * 0.95, y_cota)).set_stroke(GEO, 2.4),
                       *[Line(P3(C_H[0] + s_ * K_H * 0.95, y_cota - 0.1), P3(C_H[0] + s_ * K_H * 0.95, y_cota + 0.1)).set_stroke(GEO, 2.4) for s_ in (-1, 1)])
        l_diam = VGroup(txt("DIÂMETRO", 26, color=GEO), valor(r"1{,}9\ \mathrm{m}", GEO, 38)).arrange(RIGHT, buff=0.16)
        l_diam.move_to(P3(-0.05 - l_diam.width / 2, -3.4))      # na borda direita do ESQUEMA: longe da seta da ponta (x ≈ −3,9) e do marcador (esq)
        self.gat("quase dois metros de diâmetro")
        self.selo("NÚMEROS TÍPICOS", "")                                                  # v3 H2: o selo entra junto do primeiro número
        self.play(Create(cota_), FadeIn(l_diam), run_time=0.7)
        # legenda à direita: a seta de cada ponto (no mesmo tamanho da tela) e o valor
        X0 = 1.0
        l_rpm = VGroup(txt("ROTAÇÃO", 28), valor(r"2.700\ \mathrm{RPM}".replace(".", "{.}"), VEL, 42)).arrange(RIGHT, buff=0.16)
        l_rpm.move_to(P3(X0 + l_rpm.width / 2, 2.1))
        self.gat("duas mil e setecentas rotações por minuto")
        self.play(Create(arc_rpm), FadeIn(l_rpm), run_time=0.8)
        l1 = VGroup(txt("A", 28), valor(r"10\ \mathrm{cm}", GEO_, 40), txt("DO EIXO", 28)).arrange(RIGHT, buff=0.14)
        l2 = VGroup(txt("NA PONTA", 28), valor(r"(95\ \mathrm{cm})", GEO_, 40)).arrange(RIGHT, buff=0.14)
        l2[1][0][0].set_color(WHITE_)
        l2[1][0][-1].set_color(WHITE_)      # v6 §2.3: parênteses neutros
        v1 = valor(r"\approx 100\ \mathrm{km/h}", VEL, 46)
        v2 = valor(r"\approx 970\ \mathrm{km/h}", VEL, 46)
        a1 = arrow(P3(X0, 0.75), P3(X0 + L_PONTA * 0.10 / 0.95, 0.75), VEL, 6, tip=0.2)
        a2 = arrow(P3(X0, -0.7), P3(X0 + L_PONTA, -0.7), VEL, 6, tip=0.24)
        l1.move_to(P3(X0 + l1.width / 2, 1.3))
        v1.next_to(a1, RIGHT, buff=0.3)
        l2.move_to(P3(X0 + l2.width / 2, -0.05))
        v2.next_to(a2, RIGHT, buff=0.3)
        ang = giro.ang(self.clk.get_value())
        self.gat("um ponto a dez centímetros do eixo")
        nasce1 = v1.copy().move_to(hel_pt(cam(), 0.10, giro.ang(self.clk.get_value() + 0.3)) + P3(0, 0.55))
        self.play(FadeIn(nasce1, scale=0.8), run_time=0.3)
        self.play(ReplacementTransform(nasce1, v1), FadeIn(l1), GrowArrow(a1), run_time=0.8)
        self.gat("já a ponta da pá")
        self.play(FadeIn(l2), run_time=0.3)          # o rótulo entra antes
        self.play(FadeIn(v2, scale=0.9), GrowArrow(a2), run_time=0.8)          # v7 §3: sem voo (o número cruzava a pá, o cubo e a legenda); nasce já na legenda, ao lado da seta
        # barra da velocidade do som: marca violeta com 78% e a ponta da hélice (o ≈ 970 km/h) ligada a ela por uma linha tracejada
        xb0, xb1, yb = 1.0, 6.6, -2.4
        frac = NUM["som"]
        xt = xb0 + (xb1 - xb0) * frac
        bar_f = Rectangle(width=xb1 - xb0, height=0.32).move_to(P3((xb0 + xb1) / 2, yb)).set_stroke(GEO, 2).set_fill(PANEL, 0.6)
        bar_v = Rectangle(width=(xb1 - xb0) * frac, height=0.32).move_to(P3(xb0 + (xb1 - xb0) * frac / 2, yb)).set_stroke(width=0).set_fill(VEL, 0.85)
        tick = Line(P3(xt, yb - 0.28), P3(xt, yb + 0.28)).set_stroke(VEL, 4)
        t_som = VGroup(txt("VELOCIDADE DO SOM (20 °C):", 26), valor(r"343\ \mathrm{m/s}", VEL, 38)).arrange(RIGHT, buff=0.18)
        t_som.move_to(P3(xb0 + t_som.width / 2, yb - 0.7))
        v_som = VGroup()
        pct = valor(r"78\%", VEL, 40).move_to(P3(xt - 0.75, yb + 0.78))
        lig = DashedLine(P3(xt, v2.get_bottom()[1] - 0.08), P3(xt, yb + 0.34), dash_length=0.1).set_stroke(VEL, 2.6, opacity=0.9)
        self.reg("som", frac=frac)
        self.gat("quase mil quilômetros por hora")
        self.play(FadeIn(bar_f), FadeIn(t_som), FadeIn(v_som), run_time=0.6)
        self.gat("perto de oitenta por cento")
        self.play(GrowFromEdge(bar_v, LEFT), run_time=0.9)
        self.play(Create(tick), FadeIn(pct), Create(lig), run_time=0.5)
        self.foco = v2
        self.ate(0.99)
        # ── H3: a pergunta ──
        self.an("H3")
        self.sem_selo()
        coluna = VGroup(l_rpm, l1, l2, v1, v2)
        q = VGroup(txt("POR QUE A PONTA DA", 40, bold=True), txt("HÉLICE CHEGA A QUASE", 40, bold=True),
                   VGroup(valor(r"1.000\ \mathrm{km/h}".replace(".", "{.}"), VEL, 62), txt("?", 40, bold=True)).arrange(RIGHT, buff=0.16))
        q.arrange(DOWN, buff=0.2).move_to(P3(4.2, -2.3))          # v3 H3: frase-chave maior que os números; a coluna recua a 60% quando ela entra
        self.play(FadeOut(VGroup(bar_f, bar_v, tick, t_som, v_som, pct, lig)), run_time=0.35)      # v4: a coluna só recua quando a pergunta entra
        self.gat("e aí fica a pergunta")
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.7)      # v5 §2.3: a coluna fica a 100% (nada abaixo de 100% depois de entrar)
        self.gat("se a hélice inteira gira no mesmo ritmo")
        for _ in range(2):
            self.play(pulso.animate(rate_func=there_and_back).set_value(1.0), Indicate(a1, color=WHITE_, scale_factor=1.15), Indicate(a2, color=WHITE_, scale_factor=1.04), run_time=0.8)
        self.gat("e que número é esse")
        self.play(Indicate(arc_rpm, color=WHITE_, scale_factor=1.05), Indicate(l_rpm, color=WHITE_), run_time=0.9)
        self.foco = q
        self.ate(0.99)
        self.f3, self.cam_hel = f3, cam_

    def abertura(self):
        # ── A1 ──
        self.an("A1")
        velhos = self.snap()
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        bv = txt("BEM-VINDOS AO PARALLAX LAB", 30).move_to(P3(0, -0.5))
        self.troca(velhos, FadeIn(logo, scale=0.94), FadeIn(bv, shift=0.1 * UP), seq=True)
        self.ate(0.97)
        # ── A2: título e roteiro ──
        self.an("A2")
        tit = VGroup(txt("CINEMÁTICA ANGULAR:", 40, bold=True),
                     VGroup(txt("POR QUE A PONTA DA HÉLICE CHEGA A QUASE", 30, bold=True), valor(r"1.000\ \mathrm{km/h}".replace(".", "{.}"), VEL, 44),
                            txt("?", 30, bold=True)).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.2).move_to(P3(0, 2.3))
        nv = txt("NESTE VÍDEO:", 34, color=CYAN, bold=True).move_to(P3(-5.6, 0.85))
        ic1 = VGroup(Line(ORIGIN, 0.9 * RIGHT).set_stroke(GEO, 3), Line(ORIGIN, 0.9 * P3(math.cos(0.9), math.sin(0.9))).set_stroke(WHITE_, 4),
                     arco(ORIGIN, 0.55, 0, 0.9, ANG, 6))
        ic2 = seta_curva(ORIGIN, 0.5, 0.3, 4.2, VEL, 9)
        dsk = VGroup(Circle(radius=0.8).set_stroke(GEO, 2.5).set_fill(STEEL, 0.6), Line(ORIGIN, 0.8 * RIGHT).set_stroke(WHITE_, 4))
        # v2 D4: o ícone do giro ao ponto leva as duas setas de família: v violeta tangente e a_c verde para o centro
        ic3 = VGroup(dsk, ponto_mob(P3(0.8, 0), 0.08, z=12), arrow(P3(0.8, 0), P3(0.8, 1.0), VEL, 6, tip=0.2), arrow(P3(0.8, 0), P3(0.2, 0), ACC, 6, tip=0.2))      # v3 A2: setas ≥ 40% do diâmetro
        nomes = ("MEDIR UM GIRO", "VELOCIDADE E ACELERAÇÃO ANGULAR", "DO GIRO AO PONTO")
        cols = VGroup()
        for ic, nm in zip((ic1, ic2, ic3), nomes):
            t = VGroup(*[txt(s, 26) for s in (nm.split(" E ") if " E " in nm else [nm])]).arrange(DOWN, buff=0.08)
            if " E " in nm:
                t = VGroup(txt("VELOCIDADE E", 26), txt("ACELERAÇÃO ANGULAR", 26)).arrange(DOWN, buff=0.08)
            cols.add(VGroup(ic.copy().scale_to_fit_height(1.9), t).arrange(DOWN, buff=0.3))          # v2 D4: ícones ≥ 1,2 u
        cols.arrange(RIGHT, buff=1.3).move_to(P3(0, -1.3))
        velhos = self.snap()
        self.troca(velhos, FadeIn(tit, shift=0.1 * DOWN), seq=True)
        self.gat("como descrever o giro de um corpo")
        fant = VGroup(*[c[0].copy() for c in cols])      # §8: o roteiro aparece apagado desde já (sem 10 s de tela vazia)
        for m in fant.family_members_with_points():          # só apaga: traço a 30%, preenchimento que já existia a 25% (arco não vira cunha)
            m.set_stroke(opacity=0.3 * m.get_stroke_opacity())
            m.set_fill(opacity=min(m.get_fill_opacity(), 0.25))
        self.play(FadeIn(nv), FadeIn(fant), run_time=0.4)
        for frase, k in (("como medir um giro com um ângulo", 0), ("quão rápido e quão acelerado", 1), ("como o giro do corpo inteiro vira", 2)):
            self.gat(frase)
            self.play(FadeIn(cols[k], shift=0.12 * UP), FadeOut(fant[k]), run_time=0.6)
        self.gat("três exercícios para firmar tudo")
        self.play(Indicate(nv, color=WHITE_), run_time=0.6)
        self.ate(0.98)
        # ── A3: da partícula ao corpo ──
        self.an("A3")
        rod = VGroup(*[c[0].copy() for c in cols]).arrange(RIGHT, buff=0.6).scale(0.42).move_to(P3(0, -3.1))
        self.play(FadeOut(tit), FadeOut(nv), *[ReplacementTransform(c[0], r) for c, r in zip(cols, rod)], *[FadeOut(c[1]) for c in cols], run_time=0.8)
        self.play(FadeOut(rod), run_time=0.4)
        C, R = DC, 2.3                                                  # v3 A3: partícula e círculo maiores (a partícula é o objeto da cena)
        ph = ValueTracker(0.6)
        self.add(ph)
        circ = Circle(radius=R).move_to(C).set_stroke(GEO, 2.5, opacity=0.8)

        def part():
            a = ph.get_value()
            p = C + R * P3(math.cos(a), math.sin(a))
            t, n = P3(-math.sin(a), math.cos(a)), -P3(math.cos(a), math.sin(a))
            return VGroup(seta(p, p + 1.6 * t, VEL, 7), seta(p + 0.2 * n, p + 1.4 * n, ACC, 7), esfera_aco(0.4).move_to(p))
        pv = vivo(part)
        A, ia = M("a_c", "=", r"\frac{v^2}{r}", size=80, cores={0: ACC})
        k0 = ng("a_c") + ng("=")
        A[0][k0].set_color(VEL)
        A[0][k0 + 1].set_color(VEL)
        A[0][k0 + 3].set_color(GEO_)
        for j in (k0, k0 + 1, k0 + 3):
            A[0][j].set_stroke(A[0][j].get_fill_color(), width=1.8, background=False)
        self.pilha.poe(A)
        l_v = lbl("v", VEL, 44)
        l_a = lbl("a_c", ACC, 44)
        l_r = lbl("r", GEO_, 44).move_to(C + P3(0.0, -R / 2) + P3(0.25, 0))
        rr = Line(C, C + R * DOWN).set_stroke(GEO, 2.5)
        self.gat("você já conhece o movimento circular")
        self.play(Create(circ), FadeIn(pv), ph.animate(rate_func=linear).set_value(1.6), run_time=1.0)
        # v3 A3: a CONTA entra com a primeira fala (v voa da seta violeta, a_c da verde, r do raio)
        a_ = ph.get_value()
        p = C + R * P3(math.cos(a_), math.sin(a_))
        l_v.move_to(p + 1.9 * P3(-math.sin(a_), math.cos(a_)) + 0.4 * P3(math.cos(a_), math.sin(a_)))
        l_a.move_to(p - 1.0 * P3(math.cos(a_), math.sin(a_)) + 0.5 * P3(-math.sin(a_), math.cos(a_)))
        self.play(FadeIn(l_v), FadeIn(l_a), Create(rr), FadeIn(l_r), run_time=0.6)
        self.voa([(l_a, mp(A, ia, [0])), (l_v, VGroup(A[0][k0])), (l_r, VGroup(A[0][k0 + 3]))],
                 extra=[FadeIn(VGroup(A[0][k0 - 1], A[0][k0 + 1], A[0][k0 + 2]))], rt=1.1)
        self.foco = A
        self.play(FadeOut(VGroup(l_v, l_a, l_r, rr)), run_time=0.3)
        self.gat("tem uma aceleração apontando para o centro")
        self.play(ph.animate(rate_func=linear).set_value(2.6), Indicate(mp(A, ia, [0]), color=WHITE_), run_time=1.0)
        self.gat("a velocidade ao quadrado dividida pelo raio")
        self.play(Indicate(VGroup(A[0][k0:k0 + 4]), color=WHITE_), run_time=0.8)
        # muitas partículas, cada uma no seu círculo → o disco de referência
        self.gat("a novidade agora é que o corpo inteiro gira")
        self.wait(0.3)
        pv.clear_updaters()
        self.remove(pv)
        muitos = VGroup(*[Circle(radius=DR * k / 7).move_to(DC).set_stroke(GEO, 2.2, opacity=0.8) for k in range(1, 8)])
        bolas = VGroup(*[esfera_aco(0.17).move_to(DC + DR * k / 7 * P3(math.cos(0.4 * k), math.sin(0.4 * k))) for k in range(1, 8)])
        self.play(ReplacementTransform(circ, muitos[3]), FadeIn(muitos[:3]), FadeIn(muitos[4:]), FadeIn(bolas), run_time=1.0)
        self.gat("cada um no seu círculo")
        self.play(Rotate(bolas, 0.8, about_point=DC), run_time=1.2, rate_func=linear)
        disco = DiscoRef(self, reg=False)
        self.gat("e a gente quer um jeito")
        self.play(FadeOut(muitos), FadeOut(bolas), FadeIn(disco.corpo), FadeIn(disco.ref), FadeIn(disco.vivo), FadeIn(disco.eixo), run_time=1.0)
        self.play(disco.th.animate(rate_func=smooth).set_value(0.5), run_time=1.0)
        self.ate(0.99)
