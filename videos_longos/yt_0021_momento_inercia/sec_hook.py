"""Lote PH: hook H1–H3 (Three.js 'bastao', câmera de cima). Dois bastões iguais (0,90 kg, 0,84 m; cabo 0,25 kg + parte grossa 0,65 kg), cada um
num pino vertical: à esquerda o pino na ponta do cabo, à direita na ponta grossa. Partem do repouso juntos e chegam a ω = 10 rad/s (mesmo
θ(t) nos dois); as barras de ENERGIA (ciano) valem ½Iω² em todo quadro: 14,1 J e 7,06 J no fim. Braço em silhueta 2D empurrando no arranque."""
from pecas21 import *  # noqa: F401,F403

PL, PR = P3(-4.2, -0.6), P3(2.3, -0.6)            # pinos na tela
KH = 2.6                                           # tela/metro (raio varrido 0,84 m → 2,18)
RS = B_L * KH
HB = 3.4 / NUM["K_cabo"]                           # altura da barra por joule
YB = -2.9


class LoteHook(Lote21):
    def corpo(self):
        cam = cam_b(K=KH)
        w0 = lambda p: (p[0] / KH, p[1] / KH)       # tela → metros (plano z = 0, câmera de cima: homotetia exata)
        th, w = ValueTracker(PI / 2), ValueTracker(0.0)
        self.add(th, w)
        self.th, self.w = th, w
        (xl, yl), (xr, yr) = w0(PL), w0(PR)

        def est(t):
            a = th.get_value()
            e = {"bs": [{"x": xl, "y": yl, "ang": a, "piv": 0}, {"x": xr, "y": yr, "ang": a + PI, "piv": 1}], "cam": cam}
            if not PEDIDOS3D:
                self.reg("hook", w=w.get_value(), th=a, I0=I_bastao(0), I1=I_bastao(1), K0=0.5 * I_bastao(0) * w.get_value() ** 2,
                         K1=0.5 * I_bastao(1) * w.get_value() ** 2, U0=0.0, U1=0.0,
                         pino0=tela_b(xl, yl, cam), pino1=tela_b(xr, yr, cam),
                         ponta0=tela_b(*ponta_b(xl, yl, a, B_L), cam), ponta1=tela_b(*ponta_b(xr, yr, a + PI, B_L), cam))
            return r4(e)
        f3 = Fundo3D(self, "bastao", est)
        self.add(f3)
        self.f3 = f3
        self.secao("O MESMO BASTÃO, DOIS EIXOS")
        for a_ in list(self._pend):                                    # v5: a linha 2 do canto já está na tela no primeiro quadro
            if getattr(a_, "mobject", None) is self.h2:
                self._pend.remove(a_)
                self.add(self.h2)
        # ── H1 ──
        self.an("H1")
        circ = VGroup(*[DashedVMobject(Circle(radius=RS).move_to(p).set_stroke(GEO, 1.8, opacity=0.45), num_dashes=70) for p in (PL, PR)]).set_z_index(2)
        nomes = VGroup(*[VGroup(txt(a_, 24), txt(b_, 24)).arrange(DOWN, buff=0.06).move_to(p_ + (RS + 0.62) * DOWN)
                        for p_, a_, b_ in ((PL, "EIXO NA PONTA", "DO CABO"), (PR, "EIXO NA PONTA", "GROSSA"))])
        th.add_updater(lambda m, dt: m.increment_value(0.55 * dt))              # os dois bastões já entram girando devagar
        self.play(FadeIn(circ), run_time=0.8)
        self.wait(1.2)
        self.gat("a única diferença é onde ele está preso")
        self.play(self.ind_copia(VGroup(circ[0], circ[1]), WHITE_, 1.03, 0.9), run_time=0.9)
        self.gat("aqui o eixo passa pela ponta do cabo")
        self.play(FadeIn(nomes[0], shift=0.1 * UP), Flash(PL, color=GEO, line_length=0.25, flash_radius=0.3), run_time=0.8)
        self.gat("aqui pela ponta grossa")
        self.play(FadeIn(nomes[1], shift=0.1 * UP), Flash(PR, color=GEO, line_length=0.25, flash_radius=0.3), run_time=0.8)
        # barras de energia (½Iω² a cada quadro) e braços: arranque a partir do repouso
        XBL, XBR = PL[0] - RS - 0.62, PR[0] + RS + 0.85
        bars = vivo(lambda: VGroup(barra_E(XBL, YB, HB * 0.5 * I_bastao(0) * w.get_value() ** 2, 0.36, hmax=3.4),
                                    barra_E(XBR, YB, HB * 0.5 * I_bastao(1) * w.get_value() ** 2, 0.36, hmax=3.4)))
        lE = VGroup(txt("ENERGIA", 24, color=KC).move_to(P3(XBL + 0.35, YB - 0.32)), txt("ENERGIA", 24, color=KC).move_to(P3(XBR, YB - 0.32)))
        self.gat("e a gente vai levar os dois")
        self.play(FadeIn(bars), FadeIn(lE), run_time=0.6)
        bra = ValueTracker(0.0)
        self.add(bra)

        def bracos():
            return VGroup()
            o = bra.get_value()
            if o < 0.02:
                return VGroup()
            a = th.get_value()
            g = VGroup()
            for p, sgn in ((PL, 1), (PR, -1)):
                s = 0.3 * KH
                aa = a if sgn == 1 else a + PI
                mao = p + s * np.array([math.cos(aa), math.sin(aa), 0])
                g.add(braco(mao, aa - PI / 2, comp=1.7, op=o))
            return g
        bv = vivo(bracos)
        self.add(bv)
        self.play(bra.animate.set_value(1.0), run_time=0.4)
        th.clear_updaters()
        T_ = 2.7                                                  # v9: arranque α constante, 0 → 10 rad/s em 2,7 s (a voz real deixa ~3,7 s depois de "vamos levar os dois"; ω final 10 rad/s = 38°/quadro, sem aliasing)
        a0 = th.get_value()
        self.play(UpdateFromAlphaFunc(th, lambda m, u: m.set_value(a0 + 0.5 * (10 / T_) * (u * T_) ** 2)),
                  UpdateFromAlphaFunc(w, lambda m, u: m.set_value(10 * u)), run_time=T_, rate_func=linear, fixo=True)
        a1, t1 = th.get_value(), self.clk.get_value()
        th.add_updater(lambda m: m.set_value(a1 + 10 * (self.clk.get_value() - t1)))     # ω = 10 rad/s constante (relógio da cena)
        self.play(bra.animate.set_value(0.0), run_time=0.6)
        bv.clear_updaters()
        self.remove(bv)
        self.ate(0.99)
        # ── H2: rótulos nascem nos objetos ──
        self.an("H2")
        lm = VGroup(MathTex("M=", font_size=40, color=MAS), nm(r"0{,}90\ \mathrm{kg}", MAS, 40)).arrange(RIGHT, buff=0.1).move_to(P3(-5.0, 2.0))
        ang_c = -1.0
        cota = VGroup(Line(PL, PL + RS * np.array([math.cos(ang_c), math.sin(ang_c), 0])).set_stroke(GEO, 2.4),
                      Dot(PL + RS * np.array([math.cos(ang_c), math.sin(ang_c), 0]), radius=0.05, color=GEO)).set_z_index(3)
        lL = VGroup(MathTex("L=", font_size=40, color=GEO), nm(r"0{,}84\ \mathrm{m}", GEO, 40)).arrange(RIGHT, buff=0.1).next_to(cota[1], DR, buff=0.1)
        arcs = VGroup(*[seta_curva(p, RS + 0.3, 0.2, 0.75, VEL, 6) for p in (PL, PR)])
        lw = VGroup(*[VGroup(MathTex(r"\omega=", font_size=46, color=VEL), nm(r"10\ \mathrm{rad/s}", VEL, 46)).arrange(RIGHT, buff=0.1)
                      .move_to(P3(x_, 1.8)) for x_ in (-0.9, 5.5)])
        self.gat("nove décimos de quilo")
        self.play(FadeIn(lm, shift=0.08 * UP), run_time=0.6)
        self.gat("oitenta e quatro centímetros")
        self.play(Create(cota), FadeIn(lL), run_time=0.7)
        self.gat("os dois giram até dez radianos")
        self.play(FadeIn(arcs), FadeIn(lw), run_time=0.7)
        self.gat("a gente está de cima")
        self.selo("NÚMEROS DE EXEMPLO", "PLANO HORIZONTAL · EIXO VERTICAL")
        nK = VGroup(nm(r"14{,}1\ \mathrm{J}", KC, 40).move_to(P3(XBL + 0.1, YB + 3.4 + 0.36)),
                    nm(r"7{,}06\ \mathrm{J}", KC, 40).move_to(P3(XBR + 0.1, YB + 3.4 + 0.36)))
        self.gat("segurando pelo cabo")
        self.play(FadeIn(nK[0], shift=0.1 * UP), self.ind_copia(lE[0], KC, 1.15, 0.7), run_time=0.7)
        self.gat("segurando pela ponta grossa")
        self.play(FadeIn(nK[1], shift=0.1 * UP), self.ind_copia(lE[1], KC, 1.15, 0.7), run_time=0.7)
        meia = DashedLine(P3(XBR - 0.3, YB + 3.4), P3(XBR + 0.3, YB + 3.4), dash_length=0.06).set_stroke(KC, 2, opacity=0.6)
        self.gat("exatamente a metade")
        self.play(Create(meia), run_time=0.5)
        self.foco = nK[1]
        self.ate(0.99)
        # ── H3: a pergunta ──
        self.an("H3")
        self.sem_selo()
        self.play(FadeOut(lL), FadeOut(cota), FadeOut(meia), run_time=0.4)
        q = VGroup(txt("POR QUE O MESMO BASTÃO EXIGE", 32, bold=True), txt("O DOBRO DE ENERGIA PARA GIRAR?", 32, bold=True)).arrange(DOWN, buff=0.12).move_to(P3(0.6, 2.8))
        self.play(FadeIn(q, shift=0.1 * DOWN), run_time=0.8)
        self.gat("a massa não mudou")
        self.play(self.ind_copia(lm, MAS, 1.12, 0.8), run_time=0.8)
        self.gat("a velocidade angular final não mudou")
        self.play(*[self.ind_copia(m, VEL, 1.12, 0.8) for m in lw], run_time=0.8)
        self.gat("o que então mudou")
        self.play(*[self.ind_copia(m, KC, 1.15, 0.8) for m in nK], run_time=0.8)
        self.play(*[self.ind_copia(m, KC, 1.15, 0.8) for m in nK], run_time=0.8)
        self.foco = q
        self.ate(0.99)
