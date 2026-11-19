"""yt_0036 · S · síntese (sem alvo) e o próximo vídeo (alvo 16). S1: dx dy = |J| du dv grande no topo e as quatro caixas com ✓, uma por gatilho.
S2: o disco com a integral que trava nas duas ordens, a grade quadrada some e nasce a de círculos e raios, a célula do anel com ÁREA ≅ ? · Δr Δθ,
o cartão do próximo vídeo por ≥ 8 s (sem o CTA por cima) e o CTA padrão."""
from j36 import *

VS, AS = Vw(470, 560, 330), (-1.25, 1.25, -1.25, 1.25)


def polar(r, t):
    return (r * math.cos(t), r * math.sin(t))


class PS(J36):
    ANTES = "O JACOBIANO NO MUNDO"

    def corpo(self):
        self.an("S1")
        self.secao("SÍNTESE")
        top = TC(r"\dX\,\dY\;=\;\Lm{|J|}\,\du\,\dv", 960, 280, 64, "c")
        self.pena(top)
        caixas = [(160, 420, [("t", "RÉGUA:"), ("m", r"\dX=g'(\Uc{t})\,\Uc{dt}")], "na régua do cálculo"),
                  (1000, 420, [("t", "LINEAR:"), ("t", "ÁREA"), ("m", r"\times\,\Lm{|ad-bc|}")], "no caso linear"),
                  (160, 640, [("t", "CURVA:"), ("t", "ÁREA"), ("m", r"\cong\Lm{|J|}\,\Du\,\Dv")], "na transformação curva"),
                  (1000, 640, [("t", "TRAPÉZIO:"), ("m", r"\dfrac{3}{4}\left(e-\dfrac{1}{e}\right)")], "no trapézio a troca")]
        for X, Y, partes, g in caixas:
            self.gat(g)
            mol = moldura(X, Y, 760, 170, GEO, .5, 2, 12)
            ck = check_px(X + 50, Y + 85, MEN)
            m = mixl(partes, X + 100, Y + 85, 40)
            self.play(Create(mol), run_time=0.4)
            self.pena(m)
            self.play(Create(ck), run_time=0.3)
        self.gat("o fator local de área")
        acende(self, (top, LIMA), rt=1.0)

        # ════ S2 · o próximo vídeo e CTA ════
        self.an("S2")
        self.gat("um desafio")              # o S1 fica até o plano do disco entrar (sem palco vazio)
        self.limpa_tudo()
        self.secao("NO PRÓXIMO VÍDEO")
        d = monta_plano(VS, AS, 1.3, 1.3, -1.25, -1.25)
        C = VS.px(0, 0)
        disco = sem_ctn(Circle(radius=330 / 120).move_to(PX(*C)).set_fill(RB, 1).set_stroke(GEO, W(2.5))).set_z_index(1)
        entra_plano(self, d, rt=0.6, extra=[FadeIn(disco)])
        self.gat("a integral de é elevado")
        I = TC(r"\iint_{\X^2+\Y^2\le 1}e^{-(\X^2+\Y^2)}\,dA", 960, 975, 40, "c")
        self.pena(I)
        self.gat("em pé trava")
        tv = tiraV(VS, .45, -math.sqrt(1 - .45 ** 2), math.sqrt(1 - .45 ** 2), h=.05, cor=E1)
        self.play(FadeIn(tv), run_time=0.4)
        p1 = placa_txt2("TRAVA", 90, 945)
        self.pena(p1)
        self.gat("deitado trava")
        th = tiraH(VS, -.4, -math.sqrt(1 - .16), math.sqrt(1 - .16), h=.05, cor=E2)
        self.play(FadeIn(th), run_time=0.4)
        p2 = placa_txt2("TRAVA", 236, 945)
        lg = leg("EM PÉ E DEITADO", 90, 1000, GEO, "left", 26)
        self.pena(p2, lg, lag=0.2)
        self.play(FadeOut(tv), FadeOut(th), run_time=0.4)
        self.remove(tv, th)
        self.gat("círculos e raios")
        circ = VGroup(*[sem_ctn(Circle(radius=330 * r / 120).move_to(PX(*C)).set_stroke(CU, W(1.6), .55).set_fill(opacity=0)).set_z_index(2)
                        for r in (.25, .5, .75, 1.0)])
        raios = VGroup(*[lin_px([C, VS.px(*polar(1, k * PI / 8))], CVV, 1.6, alpha=.55, z=2) for k in range(16)])
        self.play(FadeOut(d["g"]), LaggedStart(*[Create(c) for c in circ], lag_ratio=0.15), LaggedStart(*[Create(r) for r in raios], lag_ratio=0.05),
                  run_time=1.8)
        self.remove(d["g"])
        self.gat("erre e teta")
        lr = TP(r"\Uc{r}", VS.px(.86, 0)[0], VS.px(.86, 0)[1] + 24, 28, "c")
        lt = TP(r"\Vc{\theta}", *VS.px(*polar(.3, PI / 16)), 26, "c")
        self.pena(lr, lt, lag=0.2)
        self.gat("um pedaço de anel")
        cel = celula(VS, polar, .5, .75, PI / 8, PI / 4, n=4, wb=3, N=24)
        entra_cel(self, cel, rt=0.8)
        self.gat("qual é o fator de área")
        q = VS.px(.62, .62)
        ra = rotm([("t", "ÁREA"), ("m", r"\cong\Lm{?}\cdot\Uc{\Delta r}\,\Vc{\Delta\theta}")], q[0] + 40, q[1] - 40, 28, "l")
        self.pena(ra)
        self.gat("no próximo vídeo")
        t0 = self.t
        pc = painel(1060, 300, 800, 330)
        self.play(Create(pc), run_time=0.4)
        c1 = T("NO PRÓXIMO VÍDEO:", 1100, 380, 30, "left", GEO, bold=False)
        c2 = T("COORDENADAS POLARES", 1100, 450, 44)
        c3 = T("QUAL É O FATOR DA", 1100, 540, 38, "left", LIMA)
        c4 = T("GRADE DE CÍRCULOS?", 1100, 595, 38, "left", LIMA)
        self.pena(c1, c2, c3, c4, lag=0.2, passo=0.035)
        self.marca("16", agora=True)
        print(f"[cartao] {self._aid} entra {t0:.2f}")
        self.gat("você já fez sem saber")
        if self.t - t0 < 8.4:
            self.wait(8.4 - (self.t - t0))
        print(f"[cartao] {self._aid} sai {self.t:.2f} ({self.t - t0:.2f} s na tela)")
        print(f"[cta] {self.t:.3f}")
        logo_cta(self)
