"""yt_0037 · S · síntese e próximo vídeo — FINAL (K16, alvos v3_02 e v3_03). S1: os TRÊS painéis (O FATOR · O DISCO · O SINO INTEIRO) entram juntos
no primeiro play, com título e desenho (grade polar com a célula lima, disco em degradê, sino), sobre papel de quadradinhos de 60 px e com fundo
opaco; cada ✓ e cada resultado só no seu gatilho (dA = r dr dθ + ✓ no 1º; π(1 − 1/e) + ✓ no 2º; ∫ e^(−x²) dx = √π, com o √π voando do cartão do
canto, + ✓ no 3º). S2: o gancho do EP. 13 (Massa e centro de massa): o cartão NO PRÓXIMO VÍDEO (≥ 8 s antes do CTA); o meio disco com o mapa radial de
ρ = k r em CIANO (o tom cresce para a borda); o lápis; a reta de simetria com o ? e ONDE ELA EQUILIBRA?; a massa montada em polares, sem calcular:
M = ∫₀^π ∫₀^a (k r) · r dr dθ, com as chaves DENSIDADE (ciano) e JACOBIANO (lima). Sem pulso, sem escala no ?, sem acende."""
from v2kit import *

PW, PH_, PY = 560, 600, 250
PX0 = (60, 680, 1300)
VF = Vw(180, 690, 290)            # painel 1: o quarto de plano polar
VS2 = Vw(560, 760, 400)           # S2: meio disco


def gl(m, key):
    return VGroup(*[m[0][i] for i in sel(m, key)])


def disco_degrade(cx, cy, R, n=220):
    u = (np.arange(n) + .5) / n * 2 - 1
    X, Y = np.meshgrid(u, -u)
    r = np.sqrt(X * X + Y * Y)
    t = np.clip(1 - r, 0, 1) ** .9
    rgb = hx("#163A5C") * (1 - t[..., None]) + hx(CI) * t[..., None]
    a = (r <= 1.0).astype(float) * 255.0
    rgba = np.concatenate([rgb, a[..., None]], axis=-1)
    return img_px(rgba, cx - R, cy - R, 2 * R, 2 * R, z=2)


def painel_k(k, s):
    """Painel k com fundo opaco, o ✓ (guardado, só entra no gatilho do resultado) e o título."""
    x0 = PX0[k]
    pn = painel(x0, PY, PW, PH_)
    pn.set_fill(mixh(BG_, GEO, .09), 1)                   # o painel tem corpo (a grade de 60 px não passa por dentro)
    ck = check_px(x0 + 40, PY + 50, MEN, 1.0)
    tt = T(s, x0 + 76, PY + 62, 32, "left", BR)
    return pn, ck, tt


class PS(B37):
    ANTES = "QUANDO USAR POLARES"
    SUB = "POLAR NÃO É BOTÃO MÁGICO"
    CARTAO = True
    CARTAO_OK = True

    def corpo(self):
        # ── S1 · síntese (alvo v3_02): os três painéis juntos no primeiro play ──
        self.an("S1")
        self.grade = papel(passo=0.5).set_z_index(-10)            # K2: tela sem gráfico = quadradinhos de 60 px
        self.secao("JUNTANDO TUDO")
        self.subt("O FATOR QUE FALTAVA")
        v = VF
        p1, ck1, t1 = painel_k(0, "O FATOR")
        p2, ck2, t2 = painel_k(1, "O DISCO")
        p3, ck3, t3 = painel_k(2, "O SINO INTEIRO")
        ex = seta_px(v.px(0, 0), v.px(1.15, 0), E1, 3, 14, z=5)
        ey = seta_px(v.px(0, 0), v.px(0, 1.1), E2, 3, 14, z=5)
        grd = VGroup(*[arco(v, i / 4, 0, math.pi / 2, GEO, 1.6, z=3).set_stroke(opacity=.55) for i in range(1, 5)],
                     *[lin_px([v.px(0, 0), v.px(math.cos(math.pi / 2 * k / 12), math.sin(math.pi / 2 * k / 12))], GEO, 1.6, alpha=.45, z=3)
                       for k in range(1, 12)])
        cr = ValueTracker(.5)
        cel = always_redraw(lambda: setor(v, cr.get_value(), cr.get_value() + .25 * (.5 + cr.get_value()) / 1.0, math.pi / 6 * 1.0,
                                          math.pi / 6 * 1.0 + math.pi / 12, fill=mixh(BG_, LI, .55), stroke=LI, wpx=3, z=4))
        self.add(cr)
        dd = disco_degrade(PX0[1] + PW / 2, 540, 170)
        dc = circ_px(PX0[1] + PW / 2, 540, 170, GEO, 3, z=5)
        VB = Vw(PX0[2] + PW / 2, 680, 78, 210)
        cv = lin_px([VB.px(x, math.exp(-x * x)) for x in np.linspace(-2.95, 2.95, 181)], CI, 4, z=5)
        sb = poly_px([VB.px(-2.95, 0)] + [VB.px(x, math.exp(-x * x)) for x in np.linspace(-2.95, 2.95, 181)] + [VB.px(2.95, 0)], mixh(BG_, CI, .25), 1.0, z=2)
        eb = lin_px([VB.px(-2.98, 0), VB.px(2.98, 0)], E1, 3, z=4)
        self.pena(t1, t2, t3, lag=0.12, passo=0.03, rt=1.6,
                  extra=[FadeIn(self.grade), FadeIn(p1), FadeIn(p2), FadeIn(p3), GrowFromPoint(ex, v.P(0, 0)), GrowFromPoint(ey, v.P(0, 0)),
                         Create(grd), FadeIn(cel), FadeIn(dd), Create(dc), Create(eb), Create(cv), FadeIn(sb)])
        self.gat("o pedacinho de área é")
        F1 = col(L([("dA", "dA"), ("eq", "="), ("J", r"\J"), ("dr", r"\,\dr"), ("dt", r"\,\dt")], 0, 768, 44))
        F1.shift(RIGHT * ((PX0[0] + PW / 2 - pxof(F1.get_center())[0]) / 120))
        escreve_seq(self, F1, [(cel, "J", 0.6)], rt_voo=0.8, passo=0.04, extra0=[Create(ck1)])
        origem(self, "r lima de dA = r dr dθ", "a célula da grade polar (voo)")
        self.marca("v3_02", agora=True)
        self.gat("quanto mais longe da")
        self.play(cr.animate(rate_func=there_and_back).set_value(.72), run_time=2.0)    # escorrega para fora e cresce (uma vez)
        self.gat("por três caminhos")
        l3 = leg("SETORES · ARCO × LADO · DET", PX0[0] + PW / 2, 828, GEO, "center", 30)
        self.pena(l3, passo=0.03)
        self.gat("os limites saem da")
        th = ValueTracker(0.05)
        son = always_redraw(lambda: lin_px([v.px(0, 0), v.px(1.0 * math.cos(th.get_value()), 1.0 * math.sin(th.get_value()))], RR, 3, dash=(8, 6), z=6))
        self.add(th, son)
        self.play(th.animate(rate_func=smooth).set_value(math.pi / 2 - .05), run_time=1.4)
        self.play(FadeOut(son), run_time=0.3)
        son.clear_updaters()
        self.remove(son, th)
        # o disco: o resultado e o ✓ do painel 2
        self.gat("o disco deu pi")
        R2 = col(L([("r", r"\Me{\pi\,(1-1/e)}")], 0, 780, 44))
        R2.shift(RIGHT * ((PX0[1] + PW / 2 - pxof(R2.get_center())[0]) / 120))
        self.pena(R2, extra=[Create(ck2)])
        # o sino inteiro: o √π voa do cartão do canto, que sai; o ✓ do painel 3
        self.gat("o sino inteiro deu")
        R3 = col(L([("i", r"\displaystyle\int_{-\infty}^{\infty}"), ("f", r"\Ci{e^{-\X^2}}"), ("dx", r"\,\dX"), ("eq", "="), ("sp", r"\Me{\sqrt{\pi}}")], 0, 778, 44))
        R3.shift(RIGHT * ((PX0[2] + PW / 2 - pxof(R3.get_center())[0]) / 120))
        escreve_seq(self, R3, [(self.cart.f[0][0:3], "sp", 0.8)], rt_voo=0.8, passo=0.03, extra0=[Create(ck3)])
        origem(self, "√π do sino inteiro", "cartão √π ? do canto (voo)")
        cart, ok = self.cart, self.cart_ok
        self.cart, self.cart_ok = None, None
        sai = saindo([m for m in (cart, ok) if m is not None])
        self.play(*[FadeOut(m) for m in sai], run_time=0.3)
        self.remove(*sai)
        # ── S2 · o próximo vídeo e CTA (alvo v3_03) ──
        self.an("S2")
        sai = saindo(self.snap())
        v = VS2
        g = papel_v(v, None)                                     # K2: tela inteira, nascendo dos eixos do meio disco
        self.play(*[FadeOut(m) for m in sai], run_time=0.3)
        self.remove(*sai)
        self.secao("E AGORA, A MASSA")
        self.subt(None)
        self.grade = g
        bd = VGroup(arco(v, 1, 0, math.pi, GEO, 3, z=5), lin_px([v.px(-1, 0), v.px(1, 0)], GEO, 3, z=5))
        base = setor(v, 0, 1, 0, math.pi, fill="#132A44", z=0)
        self.play(FadeIn(g), Create(bd), FadeIn(base), run_time=0.8)              # o meio disco já tem corpo; o mapa radial pinta por cima
        self.gat("para o próximo vídeo")
        pn = painel(1140, 250, 680, 250)
        c1 = T("NO PRÓXIMO VÍDEO:", 1180, 318, 30, "left", CANTO_S, bold=False)
        c2 = T("MASSA E", 1180, 394, 58, "left", BR)
        c3 = T("CENTRO DE MASSA", 1180, 464, 58, "left", BR)
        self.pena(c1, c2, c3, lag=0.2, passo=0.035, extra=[Create(pn)])
        t_card = self.t
        self.gat("mais pesado na borda")
        mp = leg("MAIS PESADO NA BORDA", *v.px(0, 1.13), CI, "center", 32)
        self.pena(mp, passo=0.03)
        self.gat("a densidade rô")
        n = 40
        an = [setor(v, i / n, (i + 1) / n, 0, math.pi, fill=mixh("#132A44", CI, .10 + .70 * (i + .5) / n), z=1) for i in range(n)]
        rho = TC(r"\rr=\Ci{k}\,\R", 1140, 590, 46, "l")
        self.play(LaggedStart(*[FadeIn(s_) for s_ in an], lag_ratio=0.06), run_time=2.0)     # do centro para a borda, na ordem de r
        self.pena(rho)
        self.gat("coloca um lápis")
        L0 = v.px(0, 0)
        lap = VGroup(poly_px([(L0[0], L0[1] + 6), (L0[0] - 16, L0[1] + 44), (L0[0] + 16, L0[1] + 44)], "#6C7698", 1.0, z=4),
                     ret_px(L0[0] - 16, L0[1] + 44, L0[0] + 16, L0[1] + 193, fill="#4A5170", z=4))
        self.play(FadeIn(lap, shift=UP * 0.5), run_time=0.8)
        self.gat("onde ela equilibra")
        sim = lin_px([v.px(0, 0), v.px(0, 1)], BR, 2.5, dash=(9, 7), z=6)
        q = T("?", v.px(.14, .45)[0], v.px(.14, .45)[1] + 26, 72, "center", BR)
        oe = T("ONDE ELA EQUILIBRA?", 560, 1016, 44, "center", BR)
        self.play(Create(sim), run_time=0.6)
        self.pena(q, oe, lag=0.2, passo=0.04)
        self.gat("a massa já se monta")
        MM = col(L([("M", "M"), ("eq", "="), ("i1", r"\displaystyle\int_0^{\pi}"), ("i2", r"\!\!\int_0^{a}"), ("kr", r"\Ci{(k}\,\R\Ci{)}"), ("c", r"\cdot"),
                    ("J", r"\J"), ("dr", r"\,\dr"), ("dt", r"\,\dt")], 1140, 720, 46))
        krx = sel(MM, "kr")
        escreve_seq(self, MM, [(VGroup(*[rho[0][k_] for k_ in (2, 3)]), krx[1:3])], rt_voo=0.9, passo=0.04)
        origem(self, "(k r) da integral da massa", "ρ = k r (voo)")
        self.gat("um erre é da densidade")
        yb = pxof(MM.get_bottom())[1] + 30
        xk0, xk1 = pxof(MM[0][krx[0]].get_left())[0], pxof(MM[0][krx[-1]].get_right())[0]
        chD = chave_px(xk0, xk1, yb, CI, 3)
        lD = leg("DENSIDADE", (xk0 + xk1) / 2, yb + 56, CI, "center", 28)
        self.play(Create(chD), run_time=0.4)
        self.pena(lD, passo=0.03)
        self.gat("o erre do jacobiano")
        jx = sel(MM, "J")
        xj0, xj1 = pxof(MM[0][jx[0]].get_left())[0], pxof(MM[0][jx[-1]].get_right())[0]
        chJ = chave_px(xj0 - 4, xj1 + 4, yb, LI, 3)
        lJ = leg("JACOBIANO", (xj0 + xj1) / 2 + 20, yb + 104, LI, "center", 28)
        self.play(Create(chJ), run_time=0.4)
        self.pena(lJ, passo=0.03)
        self.marca("v3_03", agora=True)
        self.gat("deixa o like")
        print(f"[cartao] próximo vídeo na tela por {self.t - t_card:.2f} s antes do CTA")
        saindo(self.snap())
        logo_cta(self)
