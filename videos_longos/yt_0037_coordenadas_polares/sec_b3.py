"""yt_0037 · B3 · o teorema e a receita — v2 (alvo 05; E12–E14). B3-1: o retângulo [0, 1] × [0, 2π] com a grade; o interior acende (0 → 30 %); a
origem e a costura engrossam em ALERTA; em "duas metades" cada metade do retângulo se deforma por φ até a metade do disco (homotopia de 2 s, a
grade junto); em "a soma" as duas metades piscam uma vez cada, na ordem da fala; o enunciado embaixo, com a legenda a ≥ 20 px do palco; os
limites 0, π, 2π voam dos ticks para a linha da soma, escrita em ordem (G4). B3-2: os 4 passos, a reta-sonda radial girando (um ValueTracker),
o cartão θ FORA / r DENTRO e a lista da troca, em escala G1."""
from v2kit import *

VR = Vw(230, 770, 250, 245)       # B3-1: plano rθ (r: 250 px; θ/π: 215 px)
VD = Vw(1080, 520, 260)           # B3-1: disco
VS = Vw(190, 905, 330)            # B3-2: palco da receita
FR = mixh(BG_, GEO, .10)
CIMA_F, BAIXO_F = mixh(BG_, AZC, .30), mixh(BG_, CORAL, .26)
TA, TB, RA, RB = .25, 1.25, .8, 1.8


def linha_t(partes, X, Y, size=30, gap=22, cor=CANTO_S):
    ts, x = [], 0
    for p in partes:
        t = T(p, x, Y, size, "left", cor, bold=False)
        ts.append(t)
        x = pxof(t.get_right())[0] + gap
    g = VGroup(*ts)
    g.shift(RIGHT * ((X - (pxof(g.get_left())[0] + pxof(g.get_right())[0]) / 2) / 120))
    return ts


def sup_sub(m, key):
    ix_ = sel(m, key)
    base = max(ix_, key=lambda i: m[0][i].height)
    resto = [i for i in ix_ if i != base]
    cy = m[0][base].get_center()[1]
    up = sorted([i for i in resto if m[0][i].get_center()[1] >= cy], key=lambda i: m[0][i].get_center()[0])
    lo = sorted([i for i in resto if m[0][i].get_center()[1] < cy], key=lambda i: m[0][i].get_center()[0])
    return base, up, lo


class Metade:
    """Metade do retângulo rθ (θ de t0 a t1) com a grade, guardada em amostras (r, θ); poe(s) mistura o painel rθ (s = 0) com o disco (s = 1)."""

    def __init__(self, t0, t1, fill):
        self.ps = []
        ths = np.linspace(t0, t1, 49)
        rs = np.linspace(0, 1, 13)
        borda = [(r, t0) for r in rs] + [(1.0, t) for t in ths] + [(r, t1) for r in rs[::-1]] + [(0.0, t) for t in ths[::-1]]
        self.fundo = self._m(borda, True, fill=fill, z=2)
        self.lr = [self._m([(i / 4, t) for t in ths], False, cor=RR, w=1.8, a=.45, z=3) for i in range(1, 4)]
        self.lt = [self._m([(r, t0 + (t1 - t0) * k / 6) for r in rs], False, cor=TH, w=1.8, a=.40, z=3) for k in range(1, 6)]
        self.grupo = VGroup(*self.ps)
        self.poe(0.0)

    def _m(self, am, fecha, fill=None, cor=None, w=2, a=1.0, z=3):
        m = VMobject()
        if fecha:
            m.set_fill(fill, 1).set_stroke(width=0)
        else:
            m.set_stroke(cor, W(w), a).set_fill(opacity=0)
        m._am, m._fecha = am, fecha
        self.ps.append(sem_ctn(m).set_z_index(z))
        return m

    def P(self, r, t, s):
        a = np.array(VR.px(r, t / math.pi))
        b = np.array(VD.px(r * math.cos(t), r * math.sin(t)))
        return PX(*((1 - s) * a + s * b))

    def poe(self, s):
        for m in self.ps:
            pts = [self.P(r, t, s) for r, t in m._am]
            if m._fecha:
                pts.append(pts[0])
            m.set_points_as_corners(pts)


class PB3(B37):
    ANTES = "O FATOR É O JACOBIANO"
    SUB = "dA = r dr dθ"
    CARTAO = True

    def corpo(self):
        # ── B3-1 · o teorema, metade por metade (alvo 05) ──
        self.an("B3-1")
        aR = seta_px(VR.px(0, 0), VR.px(1.3, 0), RR, 3, 16, z=6)
        aT = seta_px(VR.px(0, 0), VR.px(0, 2.25), TH, 3, 16, z=6)
        rf = ret_v(VR, 0, 1, 0, 2, FR, z=1)
        rb = borda_v(VR, 0, 1, 0, 2, GEO, 3, z=5)
        grR = VGroup(*[lin_px([VR.px(i / 4, 0), VR.px(i / 4, 2)], RR, 1.8, alpha=.45, z=3) for i in range(1, 4)],
                     *[lin_px([VR.px(0, k / 6 * 2), VR.px(1, k / 6 * 2)], TH, 1.8, alpha=.40, z=3) for k in range(1, 6)])
        ex = eixos_xy(VD, -1.25, 1.3, -1.1, 1.3, size=40)
        df = disco(VD, 1, FR, 1.0, z=1)
        dc = circulo(VD, 1, GEO, 3, z=5)
        self.add(rf, df)
        gR3, gD3 = papel_meia(VR, 0, 655), papel_meia(VD, 655, 1920)    # K2: cada plano com a sua metade (corte entre os dois palcos)
        self.grade = VGroup(gR3, gD3)
        self.secao("O TEOREMA EM POLARES")                              # K6: o canto novo no primeiro play do bloco
        self.subt("CADA METADE CUMPRE O TEOREMA")
        self.play(FadeIn(self.grade), GrowFromPoint(aR, VR.P(0, 0)), GrowFromPoint(aT, VR.P(0, 0)), Create(rb), Create(grR), GrowFromPoint(ex[0], VD.P(0, 0)),
                  GrowFromPoint(ex[1], VD.P(0, 0)), Create(dc), run_time=0.6)
        lR = TC(r"\R", *VR.px(1.38, 0), 40, "l")
        lT = TC(r"\T", *VR.px(0, 2.4), 40, "c")
        tk = [TC("1", *VR.px(1, -.15), 40, "c"), TC(r"\pi", *VR.px(-.13, 1), 40, "c"), TC(r"2\pi", *VR.px(-.18, 2), 40, "c"),
              TC("0", *VR.px(-.1, -.13), 40, "c")]
        self.pena(lR, lT, *tk, ex[2], ex[3], lag=0.04)
        self.gat("é de classe cê um")
        sf = seta_px((590, 240), (800, 240), GEO, 4, 20, z=6)          # acima da faixa varrida pela deformação
        fi = TC(r"\varphi(\R,\T)=(\R\cos\T,\ \R\sen\T)", 770, 190, 40, "c")
        self.play(GrowFromPoint(sf, PX(590, 240)), run_time=0.4)
        self.pena(fi)
        self.gat("seja b erre téta")
        lB1 = TC(r"B_{\R\T}", *VR.px(1.1, 2.15), 40, "l")             # acima do painel: fora da faixa varrida pela deformação
        self.pena(lB1)
        self.gat("e b a imagem")
        lB2 = TC("B", *VD.px(-.95, .95), 40, "c")
        self.pena(lB2)
        # três coisas no interior; o interior acende (0 → 30 %)
        it = linha_t(["NO INTERIOR:  φ(INTERIOR) = INTERIOR", "·  φ INJETORA", "·  r ≠ 0"], 960, 862)
        self.gat("fi leva o interior")
        self.play(Transform(rf, ret_v(VR, .03, .97, .03, 1.97, mixh(BG_, GEO, .30), z=1)), Transform(df, disco(VD, .97, mixh(BG_, GEO, .30), 1.0, z=1)),
                  run_time=1.0)
        self.pena(it[0], passo=0.03)
        self.gat("fi é injetora ali")
        self.pena(it[1], passo=0.03)
        self.gat("não se anula")
        self.pena(it[2], passo=0.03)
        self.gat("então para f integrável")
        TF = TC(r"\iint_B \Ci{f(\X,\Y)}\,\dX\,\dY=\iint_{B_{\R\T}} \Ci{f(\R\cos\T,\ \R\sen\T)}\,\J\,\dr\,\dt", 960, 935, 44, "c")
        self.pena(TF)
        self.gat("a integral dupla de f em")
        realca(self, dc, cor=GEO, rt=0.5)
        self.gat("integral dupla em b erre")
        realca(self, rb, cor=GEO, rt=0.5)
        # a origem e a costura falham: engrossam em ALERTA (2 → 5 px)
        self.gat("a primeira exigência falha")
        o = ponto_px(*VD.px(0, 0), AL, 6, z=9)
        cos_ = lin_px([VD.px(0, 0), VD.px(1, 0)], AL, 2, dash=(10, 7), z=8)
        bR = VGroup(lin_px([VR.px(0, 0), VR.px(0, 2)], AL, 2, dash=(10, 7), z=8), lin_px([VR.px(0, 0), VR.px(1, 0)], AL, 2, dash=(10, 7), z=8),
                    lin_px([VR.px(0, 2), VR.px(1, 2)], AL, 2, dash=(10, 7), z=8))
        self.play(FadeIn(o), Create(cos_), Create(bR), run_time=0.6)
        self.play(o.animate.scale(1.6), cos_.animate.set_stroke(width=W(5)), bR.animate.set_stroke(width=W(5)), run_time=0.8)
        # as duas metades: cada metade do retângulo se deforma por φ até a metade do disco (2 s, a grade junto)
        self.gat("cortar o disco em duas")
        cR = lin_px([VR.px(0, 1), VR.px(1, 1)], AL, 4, dash=(10, 7), z=8)
        cD = lin_px([VD.px(-1, 0), VD.px(0, 0)], AL, 4, dash=(10, 7), z=8)
        self.play(Create(cR), Create(cD), run_time=0.6)
        self.gat("a de cima vem de")
        mc = Metade(0, math.pi, CIMA_F)
        self.play(FadeIn(mc.grupo), run_time=0.4)
        mc2 = Metade(0, math.pi, CIMA_F)
        for x in mc2.grupo.get_family():
            x._voando = True
        s = ValueTracker(0.0)
        self.add(s, mc2.grupo)
        mc2.grupo.add_updater(lambda m: mc2.poe(s.get_value()))
        self.play(s.animate(rate_func=smooth).set_value(1.0), run_time=2.0)
        mc2.grupo.clear_updaters()
        self.remove(s)
        tc1 = dentro(T("CIMA", *VR.px(.5, .5), 30, "center", BR))
        tc2 = dentro(T("CIMA", *VD.px(.5, .45), 30, "center", BR))
        self.pena(tc1, tc2, lag=0.2, passo=0.03, extra=[FadeIn(placa_min(tc1, 8, 5)), FadeIn(placa_min(tc2, 8, 5))])
        self.gat("a de baixo de téta")
        mb = Metade(math.pi, 2 * math.pi, BAIXO_F)
        self.play(FadeIn(mb.grupo), run_time=0.4)
        mb2 = Metade(math.pi, 2 * math.pi, BAIXO_F)
        for x in mb2.grupo.get_family():
            x._voando = True
        s2 = ValueTracker(0.0)
        self.add(s2, mb2.grupo)
        mb2.grupo.add_updater(lambda m: mb2.poe(s2.get_value()))
        self.play(s2.animate(rate_func=smooth).set_value(1.0), run_time=2.0)
        mb2.grupo.clear_updaters()
        self.remove(s2)
        tb1 = dentro(T("BAIXO", *VR.px(.5, 1.5), 30, "center", BR))
        tb2 = dentro(T("BAIXO", *VD.px(.5, -.55), 30, "center", BR))
        self.pena(tb1, tb2, lag=0.2, passo=0.03, extra=[FadeIn(placa_min(tb1, 8, 5)), FadeIn(placa_min(tb2, 8, 5))])
        self.gat("tem conteúdo nulo")
        cn = [leg("O CORTE E A ORIGEM:", 1450, 380, AL, "left", 30), leg("CONTEÚDO NULO", 1450, 422, AL, "left", 30),
              leg("NÃO SOMAM ÁREA", 1450, 464, GEO, "left", 30)]
        self.pena(*cn, lag=0.25, passo=0.025)
        # a soma: as metades piscam uma vez cada, na ordem da fala; os limites voam dos ticks
        self.gat("a soma das duas")
        sai3 = saindo([*it, tc1, tb1, tc1._placa, tb1._placa])                  # as três condições e os nomes do painel rθ já cumpriram; a soma ocupa a linha delas
        self.play(*[FadeOut(m) for m in sai3], run_time=0.3)
        self.remove(*sai3)
        realca(self, mc.fundo, mc2.fundo, cor=AZC, rt=0.0)                                  # K1: um traço fino que nasce e sai (sem preenchimento, sem piscar)
        realca(self, mb.fundo, mb2.fundo, cor=CORAL, rt=0.0)
        SO = col(L([("a", r"\int_{0}^{\pi}"), ("ra", r"\!\cdots\,\dt"), ("p", "+"), ("b", r"\int_{\pi}^{2\pi}"), ("rb", r"\!\cdots\,\dt"), ("eq", "="),
                    ("c", r"\int_{0}^{2\pi}"), ("rc", r"\!\cdots\,\dt")], 0, 862, 40))
        SO.shift(RIGHT * ((960 - pxof(SO.get_center())[0]) / 120))
        _, ua, la = sup_sub(SO, "a")
        _, ub, lb = sup_sub(SO, "b")
        _, uc, lc = sup_sub(SO, "c")
        # a soma em dois tempos: as duas integrais (limites voando dos ticks na ordem de leitura) e, na fala seguinte, o = ∫₀^{2π}
        escreve_seq(self, SO, [(tk[3], la), (tk[1], ua), (tk[1], lb), (tk[2], ub)], rt_voo=0.5, passo=0.03, so=sel(SO, ["a", "ra", "p", "b", "rb"]))
        origem(self, "limites 0, π, 2π das metades", "marcas do painel rθ (voos)")
        self.gat("são a integral com")
        self.pena(parte(SO, sel(SO, ["eq", "c", "rc"]), "= ∫ 0 → 2π"))
        lsoma = leg("DISCO INTEIRO = METADE DE CIMA + METADE DE BAIXO", 960, 1010, GEO, "center", 30)
        self.pena(lsoma, passo=0.02)
        self.marca("05")
        # ── B3-2 · a receita e a reta-sonda radial ──
        self.an("B3-2")
        sai = saindo(self.snap())
        v = VS
        g = papel_v(v, (-.1, 2.3, -.1, 2.15))
        sx, sy, lx, ly = eixos_xy(v, -.1, 2.35, -.1, 2.0, size=40)      # K7: o y abaixo da linha 3 do canto
        self.play(*[FadeOut(m) for m in sai], run_time=0.3)
        self.remove(*sai)
        self.play(FadeIn(g), GrowFromPoint(sx, v.P(0, 0)), GrowFromPoint(sy, v.P(0, 0)), run_time=0.5)
        self.grade = g
        self.secao("A RECEITA EM POLARES")
        self.subt("A RETA-SONDA SAI DA ORIGEM")
        self.pena(lx, ly, lag=0.05)
        self.gat("primeiro desenha a região")
        reg = setor(v, RA, RB, TA, TB, fill=mixh(BG_, GEO, .18), stroke=GEO, wpx=3, z=2)
        self.play(FadeIn(reg[0]), Create(reg[1]), run_time=0.6)
        s1 = selo("PASSO 1 · DESENHAR", 1100, 262, MEN, 30)
        poe_selo(self, s1)
        self.gat("segundo lê a região")
        s2 = selo("PASSO 2 · LER EM POLARES", 1100, 346, MEN, 30)
        poe_selo(self, s2)
        self.gat("os limites de fora")
        ra_ = lin_px([v.px(0, 0), v.px(2.1 * math.cos(TA), 2.1 * math.sin(TA))], TH, 3, dash=(9, 6), z=4)
        rb_ = lin_px([v.px(0, 0), v.px(2.1 * math.cos(TB), 2.1 * math.sin(TB))], TH, 3, dash=(9, 6), z=4)
        arc_ = arco(v, .35, TA, TB, TH, 4, z=6)
        self.play(Create(ra_), Create(rb_), Create(arc_), run_time=0.8)
        k1 = T("θ FORA: NÚMEROS", 1120, 446, 34, "left", TH)
        self.pena(k1)
        self.gat("aqui entra a reta-sonda")
        th = ValueTracker(TA + .05)
        sonda = always_redraw(lambda: VGroup(
            lin_px([v.px(0, 0), v.px(2.15 * math.cos(th.get_value()), 2.15 * math.sin(th.get_value()))], BR, 3, dash=(9, 6), z=7),
            ponto_px(*v.px(RA * math.cos(th.get_value()), RA * math.sin(th.get_value())), AZC, 10, z=9),
            ponto_px(*v.px(RB * math.cos(th.get_value()), RB * math.sin(th.get_value())), CORAL, 10, z=9)))
        self.add(th)
        self.play(FadeIn(sonda), run_time=0.4)
        self.gat("onde ela entra na")
        k2 = T("r DENTRO: DA SONDA", 1120, 500, 34, "left", RR)
        self.pena(k2)
        self.play(th.animate(rate_func=smooth).set_value(TB - .05), run_time=2.0)
        self.play(th.animate(rate_func=smooth).set_value(.75), run_time=1.1)
        sonda.clear_updaters()
        self.remove(th)
        self.gat("terceiro troca")
        s3 = selo("PASSO 3 · TROCAR", 1100, 590, MEN, 30)
        poe_selo(self, s3)
        lista = [(r"\X\ \to\ \R\cos\T", "xis vira erre"), (r"\Y\ \to\ \R\sen\T", "ípsilon vira erre"),
                 (r"\X^2+\Y^2\ \to\ \R^2", "mais ípsilon ao quadrado vira"), (r"dA\ \to\ \J\,\dr\,\dt", "e dê a vira")]
        for k, (tex, fr) in enumerate(lista):
            self.gat(fr)
            m = col(TC(tex, 1120, 660 + 62 * k, 40, "l"))
            self.pena(m)
        self.gat("quarto calcula de dentro")
        self.sai_fim(rt=0.2)
