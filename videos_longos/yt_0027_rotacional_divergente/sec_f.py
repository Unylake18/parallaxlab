"""Lote PF · NA FÍSICA (handoff v2; quadros 20 e 21). F1: palco da falsa fonte; o furo vira o fio carregado (azul com +) e FIO CARREGADO (placa); E = constante ×
falsa fonte; ∇·E = ρ/ε0; fora do fio; A CARGA MORA NO FURO. F2: o vórtice; as setas passam de verde-menta a magenta em 1 s; o fio com corrente (verde com ⊙);
B = constante × vórtice; ∇×B = μ0 J; fora do fio; ∇·B = 0 SEMPRE."""
from v27 import *  # noqa: F401,F403

V = Vista(600, 540, 120)


CL_FIO = [(-1.3, -1.42, 1.3, -0.72)]          # S14/S15: clareira no retângulo do rótulo do fio


def rot_fio(s):
    x, y = canto_xy(V, 0, -1.05)
    m = TXP(s, x, y + 10, 28, "center", BR, bold=False)
    return VGroup(placa7(m, 6, 4), m)


class LoteF(Base):
    ANTES = "NO ESPAÇO"

    def corpo(self):
        # ── F1 ──
        self.an("F1")
        self.secao("NA FÍSICA")
        ce = campo7(V, F_FONTE, rmin=0.75, mmax=1.4, nome="F1 campo elétrico (falsa fonte)")
        fu = furo7(V, 0.55)
        self.play(FadeIn(fu), cresce_campo(ce, 1.5))                      # §4.1: o palco entra no começo do lote (sem quadro vazio)
        fio = furo7(V, 0.55, CARGA, "+", 40)
        lf = rot_fio("FIO CARREGADO")
        cl1 = esconde(ce, clar(CL_FIO))
        self.gat("o formato do campo elétrico")
        self.play(some(cl1), FadeIn(fio, scale=0.6), FadeIn(lf), run_time=0.7)
        self.remove(fu)
        fE = TC(r"\E = \dfrac{\lambda}{2\pi\varepsilon_0}\,\dfrac{(\X,\ \Y)}{\X^2+\Y^2}", 1120, 330, 48)
        self.gat("é a nossa falsa fonte")
        self.play(caneta(fE))
        self.play(FadeIn(legenda("= FALSA FONTE × CONSTANTE", 1124, 440)), run_time=0.5)
        fG = TC(r"\nabla\cdot\E = \dfrac{\rho}{\varepsilon_0}", 1120, 570, 56)
        self.gat("a lei de gauss na forma local")
        self.play(caneta(fG))
        fo = TC(r"\text{fora do fio: }\ \rho = 0 \;\Rightarrow\; \nabla\cdot\E = 0", 1120, 700, 40)
        self.gat("fora do fio não tem carga")
        self.play(caneta(fo))
        cm = T("A CARGA MORA NO FURO", 1120, 820, 34, "left", CARGA)
        self.gat("a carga mora toda no furo")
        self.play(FadeIn(cm, shift=0.1 * UP), run_time=0.5)
        self.ate(0.97)

        # ── F2 ──
        self.an("F2")
        cv = campo7(V, F_VORT, rmin=0.75, mmax=1.4, nome="F2 campo magnético (vórtice)")
        fu2 = furo7(V, 0.55)
        cl2 = esconde(cv, clar(CL_FIO))
        for s_ in cl2:
            op_seta(s_, 0)
            s_._escondida = True
        sai = self.snap()
        self.play(*[FadeOut(m_) for m_ in sai], FadeIn(fu2), cresce_campo(VGroup(*[s_ for s_ in cv if s_ not in cl2]), 1.0))   # o vórtice entra enquanto a falsa fonte sai
        self.remove(*sai)
        self.add(*cl2)
        c0 = [s_.haste.get_stroke_color() for s_ in cv]

        def vira(m_, a):
            for s_, c in zip(m_, c0):
                cc = interpolate_color(ManimColor(c), ManimColor(MAG), a)
                s_.haste.set_stroke(cc)
                s_.ponta.set_fill(cc).set_stroke(cc)
        fio = furo7(V, 0.55, CORR, r"\odot", 40)
        lf = rot_fio("FIO COM CORRENTE")
        self.gat("o formato do campo magnético")
        self.play(UpdateFromAlphaFunc(cv, vira), FadeIn(fio, scale=0.6), FadeIn(lf), run_time=1.0)
        self.remove(fu2)
        fB = TC(r"\B = \dfrac{\mu_0 I}{2\pi}\,\dfrac{(-\Y,\ \X)}{\X^2+\Y^2}", 1120, 330, 48)
        self.gat("de novo o nosso vórtice")
        self.play(caneta(fB))
        self.play(FadeIn(legenda("= VÓRTICE × CONSTANTE", 1124, 440)), run_time=0.5)
        fA = TC(r"\nabla\times\B = \mu_0\J", 1120, 560, 56)
        self.gat("o rotacional do campo magnético é proporcional")
        self.play(caneta(fA))
        fo = TC(r"\text{fora do fio: }\ \J = \vec 0 \;\Rightarrow\; \nabla\times\B = \vec 0", 1120, 680, 40)
        self.gat("fora do fio não passa corrente")
        self.play(caneta(fo))
        fD = TC(r"\nabla\cdot\B = 0", 1120, 810, 52)
        self.gat("o divergente do campo magnético é zero sempre")
        self.play(caneta(fD))
        self.play(FadeIn(legenda("SEMPRE", 1420, 820, MAG)), run_time=0.4)
        self.ate(0.97)
        self.sai_fim()
