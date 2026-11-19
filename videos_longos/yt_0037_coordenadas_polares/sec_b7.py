"""yt_0037 · B7 · quando usar polares — v2 (alvo v2_04; E37–E38; narração v2.1). O quadrado [0, 1]² grande; o raio laranja varre de 0 a π/2 e
o ponto de saída muda de cor ao trocar de lado (azul-claro no lado x = 1, coral no lado y = 1); dois raios fixos com r = sec θ e r = cossec θ;
a diagonal θ = π/4; as metades se pintam com a varredura de cada integral. Coluna: x = 1 ⇒ r cos θ = 1 ⇒ r = sec θ; a do cossec; as duas
integrais (os limites voam dos rótulos do palco); DUAS INTEGRAIS / EM x E y: UMA SÓ; POLARES VALEM A PENA QUANDO com dois ✓ (sem caixa)."""
from v2kit import *

V7 = Vw(140, 950, 620)
Q4 = math.pi / 4
X7 = 1060
T1_, T2_ = 0.42, 1.18             # os dois raios de exemplo (saída no lado x = 1 e no lado y = 1)


def saida(t):
    return (1.0, math.tan(t)) if t <= Q4 else (1 / math.tan(t), 1.0)


def cor_saida(t):
    return AZC if t <= Q4 else CORAL


def gl(m, key):
    return VGroup(*[m[0][i] for i in sel(m, key)])


def sup_sub(m, key):
    ix_ = sel(m, key)
    base = max(ix_, key=lambda i: m[0][i].height)
    resto = [i for i in ix_ if i != base]
    cy = m[0][base].get_center()[1]
    up = sorted([i for i in resto if m[0][i].get_center()[1] >= cy], key=lambda i: m[0][i].get_center()[0])
    lo = sorted([i for i in resto if m[0][i].get_center()[1] < cy], key=lambda i: m[0][i].get_center()[0])
    return base, up, lo


def fatia(v, t0, t1, cor, op):
    """Parte do quadrado varrida de t0 a t1 (polígono origem + saídas)."""
    if t1 - t0 < 1e-3:
        t1 = t0 + 1e-3
    ts = list(np.linspace(t0, t1, 40))
    if t0 < Q4 < t1:
        ts.append(Q4)
        ts.sort()
    return poly_px([v.px(0, 0)] + [v.px(*saida(t)) for t in ts], mixh(BG_, cor, op), 1.0, z=2)


class PB7(B37):
    ANTES = "A CURVA NORMAL"
    SUB = "O MESMO NÚMERO NA ESTATÍSTICA"
    CARTAO = True
    CARTAO_OK = True

    def corpo(self):
        v = V7
        self.an("B7")
        g = papel_v(v, None, passo=.25)
        self.grade = g
        sx, sy, lx, ly = eixos_xy(v, -.1, 1.28, -.08, 1.13, size=40)      # o y fica abaixo da linha 3 do canto
        qb = borda_v(v, 0, 1, 0, 1, GEO, 3, z=5)
        self.play(FadeIn(g), GrowFromPoint(sx, v.P(0, 0)), GrowFromPoint(sy, v.P(0, 0)), Create(qb), run_time=0.5)   # o quadrado já no 1º quadro
        self.secao("QUANDO USAR POLARES")
        self.subt("POLAR NÃO É BOTÃO MÁGICO")
        self.pena(lx, ly, lag=0.05)
        self.gat("num quadrado o raio")
        t1 = TC("1", *[a + b for a, b in zip(v.px(1, 0), (0, 43))], 40, "c")
        t2 = TC("1", *[a + b for a, b in zip(v.px(0, 1), (-38, 0))], 40, "c")
        realca(self, qb, cor=GEO, rt=0.6)
        self.pena(t1, t2, lag=0.1)
        # o raio varre de 0 a π/2; a saída muda de cor ao trocar de lado
        self.gat("ora pelo lado xis")
        th = ValueTracker(0.04)
        son = always_redraw(lambda: VGroup(lin_px([v.px(0, 0), v.px(*saida(th.get_value()))], RR, 4, z=7),
                                           ponto_px(*v.px(*saida(th.get_value())), cor_saida(th.get_value()), 10, z=9)))
        for x in son.get_family():
            x._sem_foco = True
        self.add(th)
        self.play(FadeIn(son), run_time=0.3)
        self.play(th.animate(rate_func=linear).set_value(math.pi / 2 - .04), run_time=3.2)
        # x = 1 ⇒ r cos θ = 1 ⇒ r = sec θ
        self.gat("no lado xis igual a um")
        self.play(th.animate(rate_func=smooth).set_value(T1_), run_time=1.0)
        r1 = VGroup(lin_px([v.px(0, 0), v.px(*saida(T1_))], RR, 4, z=6), ponto_px(*v.px(*saida(T1_)), AZC, 10, z=8))
        self.add(r1)
        E1_ = col(L([("x", r"\X=1"), ("i1", r"\ \Rightarrow\ "), ("c", r"\R\cos\T=1"), ("i2", r"\ \Rightarrow\ "), ("s", r"\R=\Az{\sec\T}")], X7, 213, 44))
        self.pena(parte(E1_, sel(E1_, ["x", "i1", "c"]), "x = 1 ⇒ r cos θ = 1"))
        self.gat("então erre é secante")
        self.pena(parte(E1_, sel(E1_, ["i2", "s"]), "⇒ r = sec θ"))
        degrau(self, "B7 lados", "x = 1 ⇒ r cos θ = 1 ⇒ r = sec θ")
        lsec = TP(r"\R=\Az{\sec\T}", 0, 0, 40, "l")
        lsec.shift(PX(785, 672) - np.array([lsec.get_left()[0], lsec.get_center()[1], 0]))
        lsec._fonte = E1_
        voa(self, gl(E1_, "s").copy(), lsec, rt=0.8, arco=0.6)
        # y = 1 ⇒ r sen θ = 1 ⇒ r = cossec θ
        self.gat("no lado ípsilon igual a um")
        self.play(th.animate(rate_func=smooth).set_value(T2_), run_time=1.0)
        r2 = VGroup(lin_px([v.px(0, 0), v.px(*saida(T2_))], RR, 4, z=6), ponto_px(*v.px(*saida(T2_)), CORAL, 10, z=8))
        self.add(r2)
        E2_ = col(L([("y", r"\Y=1"), ("i1", r"\ \Rightarrow\ "), ("c", r"\R\sen\T=1"), ("i2", r"\ \Rightarrow\ "), ("s", r"\R=\Co{\cossec\T}")], X7, 298, 44))
        self.pena(parte(E2_, sel(E2_, ["y", "i1", "c"]), "y = 1 ⇒ r sen θ = 1"))
        self.gat("então erre é cossecante")
        self.pena(parte(E2_, sel(E2_, ["i2", "s"]), "⇒ r = cossec θ"))
        degrau(self, "B7 lados", "y = 1 ⇒ r sen θ = 1 ⇒ r = cossec θ")
        lcos = TP(r"\R=\Co{\cossec\T}", 0, 0, 40, "l")
        lcos.shift(PX(280, 280) - np.array([lcos.get_left()[0], lcos.get_center()[1], 0]))
        lcos._fonte = E2_
        voa(self, gl(E2_, "s").copy(), lcos, rt=0.8, arco=0.5)
        # a integral racha em duas, em θ = π/4
        self.gat("a integral racha em")
        self.play(th.animate(rate_func=smooth).set_value(Q4), run_time=0.8)
        d45 = lin_px([v.px(0, 0), v.px(1, 1)], GEO, 3, dash=(10, 7), z=6)
        self.play(Create(d45), FadeOut(son), run_time=0.6)
        son.clear_updaters()
        self.remove(son)
        l45 = TC(r"\T=\pi/4", 0, 0, 40, "l")
        l45.shift(PX(835, 286) - np.array([l45.get_left()[0], l45.get_center()[1], 0]))
        self.pena(l45)
        # de 0 a π/4 até sec θ: a metade de baixo se pinta com a varredura
        self.gat("de zero a pi sobre")
        tb = ValueTracker(0.0)
        f1 = always_redraw(lambda: fatia(v, 0.0, tb.get_value(), AZC, .22))
        self.add(tb, f1)
        I1 = col(L([("ii", r"\iint_Q f\,dA"), ("eq", "="), ("i1", r"\displaystyle\int_0^{\pi/4}"), ("i2", r"\int_0^{\Az{\sec\T}}"), ("f", r"f\,\J\,\dr\,\dt")],
                   X7, 0, 44))
        I1.shift(UP * ((pxof(I1[0][sel(I1, "eq")[0]].get_center())[1] - 408) / 120))
        _, u1, l1 = sup_sub(I1, "i1")
        _, u2, l2 = sup_sub(I1, "i2")
        self.play(tb.animate(rate_func=linear).set_value(Q4), run_time=1.6)
        f1.clear_updaters()
        escreve_seq(self, I1, [(l45[0][2:], u1, -1.0), (lsec.f[0][2:], u2, -0.9)], rt_voo=0.8, passo=0.04)
        origem(self, "π/4 e sec θ", "rótulos θ = π/4 e r = sec θ do palco (voos)")
        degrau(self, "B7 integrais", "∬_Q f dA = ∫₀^{π/4}∫₀^{sec θ} f r dr dθ")
        # de π/4 a π/2 até cossec θ: a metade de cima
        self.gat("de pi sobre quatro a pi")
        tc = ValueTracker(Q4)
        f2 = always_redraw(lambda: fatia(v, Q4, tc.get_value(), CORAL, .20))
        self.add(tc, f2)
        I2 = col(L([("p", "+"), ("i1", r"\displaystyle\int_{\pi/4}^{\pi/2}"), ("i2", r"\int_0^{\Co{\cossec\T}}"), ("f", r"f\,\J\,\dr\,\dt")], X7 + 70, 0, 44))
        abaixo(I1, I2, X7 + 70, 30)
        _, u3, l3 = sup_sub(I2, "i1")
        _, u4, l4 = sup_sub(I2, "i2")
        self.play(tc.animate(rate_func=linear).set_value(math.pi / 2), run_time=1.6)
        f2.clear_updaters()
        escreve_seq(self, I2, [(l45[0][2:], l3, -1.5), (lcos.f[0][2:], u4, -1.3)], rt_voo=0.8, passo=0.04)
        degrau(self, "B7 integrais", "+ ∫_{π/4}^{π/2}∫₀^{cossec θ} f r dr dθ")
        du = leg("DUAS INTEGRAIS", X7, pxof(I2.get_bottom())[1] + 52, AL, "left", 30)
        self.pena(du, passo=0.03)
        self.gat("o quadrado é a região")
        realca(self, qb, cor=GEO, rt=0.8)
        um_ = leg("EM x E y: UMA SÓ", X7 + 300, pxof(du.get_bottom())[1] + 0, CANTO_S, "left", 30)
        um_.shift(UP * (du.get_center()[1] - um_.get_center()[1]))
        self.pena(um_, passo=0.03)
        # polares valem a pena quando (dois ✓, sem caixa)
        self.gat("polar vale a pena")
        hq = T("POLARES VALEM A PENA QUANDO", X7, 750, 30, "left", BR)
        self.pena(hq, passo=0.025)
        self.gat("simetria em torno da")
        aq = arco(v, 1.0, 0, math.pi / 2, MEN, 3, z=6)
        k1 = check_px(X7 + 18, 805, MEN, .9)
        c1 = T("A REGIÃO É REDONDA", X7 + 56, 816, 30, "left", BR)
        self.play(Create(aq), run_time=0.8)
        self.pena(c1, passo=0.03, extra=[Create(k1)])
        self.gat("ou quando o integrando")
        nv = VGroup(*[arco(v, r_, 0, math.pi / 2, MEN, 2, z=5).set_stroke(opacity=.45) for r_ in (.35, .7)])
        k2 = check_px(X7 + 18, 860, MEN, .9)
        c2 = T("O INTEGRANDO TEM", X7 + 56, 871, 30, "left", BR)
        c2m = TC(r"\X^2+\Y^2", pxof(c2.get_right())[0] + 30, 860, 44, "l")
        self.pena(c2, c2m, lag=0.2, passo=0.03, extra=[Create(k2), Create(nv, run_time=0.8)])
        self.gat("melhor ainda quando")
        acende(self, (k1, MEN), (k2, MEN), rt=0.6)
        self.marca("v2_04")
        self.sai_fim()
