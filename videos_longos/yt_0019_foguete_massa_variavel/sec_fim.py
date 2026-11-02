"""Lote PS: S1 (três cartões PANEL; atrás, o foguete do hook na rampa (Three.js) com a barra 89,0 / 8,9 / 2,1; a pergunta do hook pequena no topo),
EN1 (encerramento padrão: logo com anéis, INSCREVA-SE) e EN2 (desafio dos comentários). Sem prévia de próximo vídeo."""
from pecas19 import *  # noqa: F401,F403
from sec_hook import barra_hook, FR_HOOK
from fecho10 import FechoMixin

VEX_C = VREL


class LoteFim(FechoMixin, Prob2):
    FUNDO = "fundo_lab.png"

    def construct(self):
        self.setup_base()
        self.s1_()
        self.encerramento()
        self.gancho()
        self.cartao_final()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def s1_(self):
        self.an("S1")
        self.secao("SÍNTESE")
        az, lift, sep = ValueTracker(-96.0), ValueTracker(0.0), ValueTracker(0.0)
        self.add(az, lift, sep)

        def est(t):
            s_ = sep.get_value()
            return {"f": r4(est_foguete(0.0, 0.0, 0.03 + lift.get_value(), 1.0, "z", sep=[s_, 0.3 * s_], torre=0, ch1=max(0.0, 1.0 - s_ / 0.25) if s_ > 0.01 else 0.0, ch2=min(1.0, s_ / 0.25))),
                    "cam": r4(cam_obl_(7.0, (0.03, 0.0, 0.5 + lift.get_value() + 0.55 * s_), 5.6, xc=-5.4, yc=-0.4, fov=20, az=az.get_value()))}
        f3 = Fundo3D(self, "rampa", est, op=1.0)
        self.add(f3)
        xb, yb, H = -3.6, -2.7, 4.6
        b, rs, _ = barra_hook(xb, yb, H, size=24)
        q = VGroup(txt("POR QUE UM FOGUETE É QUASE", 24, color=DIM), txt("TODO COMBUSTÍVEL?", 24, color=DIM)).arrange(DOWN, buff=0.08).move_to(P3(2.7, 3.65))
        self.play(FadeIn(b), FadeIn(rs), FadeIn(q), az.animate(rate_func=linear).set_value(-93.0), run_time=1.0)
        self.reg("barra_s1", prop=100 * FR_HOOK[0], estr=100 * FR_HOOK[1], carga=100 * FR_HOOK[2])

        def cartao_(m, w=5.6, extra=0.5, cor=BLUE_L):
            r = RoundedRectangle(corner_radius=0.12, width=w, height=m.height + extra).set_fill(PANEL, 0.88).set_stroke(cor, 2)
            r._fundo = r._caixa = True
            m.move_to(r)
            return VGroup(r, m).set_z_index(20)
        # c0: o ⊕ parado entre o foguete e a nuvem (mini-loop de 3 s)
        rk = FogueteMestre(1.7, 0.38, horizontal=True, bocal=ORIGIN)
        c0r = RoundedRectangle(corner_radius=0.12, width=5.6, height=1.2).set_fill(PANEL, 0.88).set_stroke(BLUE_L, 2)
        c0r._fundo = c0r._caixa = True
        c0r.move_to(P3(3.7, 2.2))
        clk = self.clk

        def mini():
            u = (clk.get_value() % 3.0) / 3.0
            cx_, cy_ = 3.7, 2.2
            g = VGroup(rk.copy().shift(P3(cx_ - 0.35 + 0.6 * u, cy_)))
            for k in range(16):
                a = (u * 1.0 + k / 16.0) % 1.0
                g.add(Dot(P3(cx_ - 0.45 - 2.0 * u * (0.4 + a) * 0.8, cy_ + 0.3 * math.sin(k * 7.3) * (0.3 + a)), radius=0.05, color=GAS_C).set_opacity(0.85))
            g.add(marcador_cm(P3(cx_ + 0.65, cy_), r=0.22))
            return g.set_z_index(22)
        mv = vivo(mini)
        c2 = cartao_(M(r"F_{emp}", "=", r"v_{ex}", r"\left|\frac{dm}{dt}\right|", size=52, cores={0: FC, 2: VEX_C})[0], cor=FC)
        # c3: Δv = v_ex ln(m0/mf) com o mini gráfico do logaritmo e os degraus ×e
        fm = M(r"\Delta v", "=", r"v_{ex}", r"\ln\frac{m_0}{m_f}", size=52, cores={0: VEL, 2: VEX_C})[0]
        cur = VMobject().set_points_as_corners([P3(-1.4 + 2.6 * u_, -0.55 + 0.42 * math.log(1 + 12 * u_)) for u_ in np.linspace(0, 1, 40)]).set_stroke(VEL, 4)
        ejs = VGroup(Line(P3(-1.4, -0.6), P3(1.3, -0.6)).set_stroke(GEO, 2), Line(P3(-1.4, -0.6), P3(-1.4, 0.35)).set_stroke(GEO, 2))
        dg = VGroup(*[Dot(P3(-1.4 + 2.6 * u_, -0.55 + 0.42 * math.log(1 + 12 * u_)), radius=0.06, color=WHITE_) for u_ in (0.12, 0.38, 0.8)])
        mini_g = VGroup(ejs, cur, dg).shift(P3(0, -0.15)).scale(0.68)
        lxe = MathTex(r"\times e", font_size=34, color=WHITE_).move_to(P3(0.55, -0.95))
        c3 = VGroup(fm.copy(), VGroup(mini_g, lxe))
        c3[1].next_to(c3[0], DOWN, buff=0.25)
        c3 = cartao_(c3, extra=0.34, cor=VEL)
        c1 = cartao_(txt("ESCOLHA O SISTEMA", 40, bold=True), w=6.8, extra=0.9)
        c2.move_to(P3(3.7, 1.6 - 0.15 - c2.height / 2))                            # v7 #43: vão de 0,15 u entre os cartões
        c3.move_to(P3(3.7, c2.get_bottom()[1] - 0.15 - c3.height / 2))
        c1.move_to(P3(3.7, -0.1))
        self.gat("empurrando o próprio gás")
        self.play(FadeIn(c0r), FadeIn(mv), run_time=0.6)
        self.gat("velocidade de exaustão vezes a vazão")
        self.play(FadeIn(c2, shift=0.15 * UP), run_time=0.7)
        self.gat("o logaritmo cobra caro")
        self.play(FadeIn(c3, shift=0.15 * UP), run_time=0.7)
        self.gat("dois vírgula sete")
        self.play(Indicate(lxe, color=WHITE_, scale_factor=1.3), run_time=0.8)
        self.gat("quase todo propelente")
        self.play(Indicate(b, color=MAS, scale_factor=1.0), Indicate(rs, color=WHITE_, scale_factor=1.04), run_time=0.9)
        self.gat("dividido em estágios")
        self.play(lift.animate.set_value(0.8), sep.animate.set_value(1.6), run_time=2.0)      # o foguete-mestre separa o 1º estágio (2 s)
        self.gat("escolher o sistema que inclui")
        mv.clear_updaters()
        self.play(FadeOut(mv), FadeOut(c0r), FadeOut(c2), FadeOut(c3), run_time=0.4)                      # G39: os cartões saem inteiros e só então o ESCOLHA O SISTEMA entra
        self.play(FadeIn(c1, scale=0.95), run_time=0.4)
        c1[0].set_stroke([CYAN, MAG], 4)                                                      # borda em degradê ciano → magenta
        self.foco = c1
        resto = max(0.4, self.resta() - 0.2)
        self.play(az.animate(rate_func=linear).set_value(az.get_value() + 0.12 * resto), run_time=resto)
        self.ate(0.99)

    def encerramento(self):
        # v10: a antiga EN1 (INSCREVA-SE no meio) saiu; a fala de inscrição virou o cartão final (FIM-2)
        self.an("EN2")
        velhos = self.snap()
        self.secao(None)
        d1 = txt("DESAFIO PARA OS COMENTÁRIOS", 30, bold=True, color=CYAN).move_to(P3(0, 2.4))
        d2 = VGroup(txt("UM ESTÁGIO, SEM ESTRUTURA,", 36, bold=True),
                    VGroup(M(r"\Delta v", "=", r"2\,v_{ex}", size=56, cores={0: VEL, 2: VEX_C})[0], txt(":", 36, bold=True)).arrange(RIGHT, buff=0.1),
                    txt("QUANTO DO FOGUETE PRECISA SER PROPELENTE?", 36, bold=True)).arrange(DOWN, buff=0.3).move_to(P3(0, 0.2))
        bal = VGroup(RoundedRectangle(corner_radius=0.25, width=1.5, height=1.0).set_stroke(BLUE_L, 3).set_fill(PANEL, 0.9),
                     Polygon(P3(-0.35, -0.5), P3(-0.05, -0.5), P3(-0.45, -0.85)).set_stroke(BLUE_L, 3).set_fill(PANEL, 0.9),
                     VGroup(*[Dot(P3(x, 0), radius=0.07, color=WHITE_) for x in (-0.35, 0, 0.35)])).move_to(P3(0, -2.6))
        bal[1].shift(bal[0].get_bottom() - bal[1].get_top() + 0.02 * UP)
        self.troca(velhos, FadeIn(d1), FadeIn(bal, scale=0.8), seq=True)                      # o balão desde o começo (palco)
        self.play(FadeIn(d2[0], shift=0.1 * UP), run_time=0.6)
        self.gat("precisa ganhar o dobro")
        self.play(FadeIn(d2[1], shift=0.1 * UP), run_time=0.6)
        self.gat("que fração da massa inicial")
        self.play(FadeIn(d2[2], shift=0.1 * UP), run_time=0.7)
        self.foco = bal
        for _ in range(3):
            if self.resta() < 1.2:
                break
            self.play(bal[2].animate(rate_func=there_and_back).shift(0.08 * UP), run_time=0.8)
        self.ate(0.99)
