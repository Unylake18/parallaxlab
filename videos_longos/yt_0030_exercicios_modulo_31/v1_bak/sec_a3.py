"""Lote PA3 · A3 POR QUE UM SOBRE A DISTÂNCIA (alvos 26, 27). Fio ⊙ no centro (anel branco + ponto) com FIO COM CORRENTE em placa; B = (−y, x)/(x² + y²)^α
com α branco; α corre de 0,3 a 1 (2 s) com o campo se ajustando e 2 − 2α ao vivo (2 casas, vírgula) chegando a 0,00; ⇒ α = 1; ‖B‖ = 1/r e o gráfico
|B| × distância (alvo 26). Fio carregado: cada seta gira 90° no sentido horário (a explosão) e div E = 0 ⇒ α = 1. Carga no espaço: a carga azul +,
o corte radial; a conta de uma parcela e a soma; NO PLANO (2 − p), NO ESPAÇO (3 − p); p = 3 ⇒ 1/r² (alvo 27)."""
from lib30 import *  # noqa: F401,F403

PTS = [(X, Y) for X in np.arange(-3.5, 3.5 + 1e-6, .5) for Y in np.arange(-2.5, 2.5 + 1e-6, .5)
       if math.hypot(X, Y) >= .5 and not (-3.9 - .25 < X < -1.2 + .25 and -2.95 - .25 < Y < -2.45 + .25)]
MM = interp_tab([(.3, 2.2), (1, 2.0)])


def grafico(rot="|B|"):
    gx, gy, gw, gh = 1130, 850, 600, 170
    ax = VMobject().set_points_as_corners([PX(gx, gy - gh), PX(gx, gy), PX(gx + gw, gy)]).set_stroke(GEO, 2 / 1.2, 1).set_fill(opacity=0)
    ax._sem_contorno = True
    pts = []
    for i in range(201):
        r = .35 + i / 200 * 3.65
        yv = min(1 / r, 2.6)
        pts.append(PX(gx + (r / 4) * gw, gy - yv / 2.6 * gh))
    cv = VMobject().set_points_as_corners(pts).set_stroke(CAMPO2, 4 / 1.2, 1).set_fill(opacity=0)
    cv._sem_contorno = True
    lb = T(rot, gx - 10, gy - gh - 12, 24, "right", GEO, bold=False, up=False)
    ld = T("distância", gx + gw, gy + 34, 24, "right", GEO, bold=False, up=False)
    return VGroup(ax, cv, lb, ld).set_z_index(20), lb


def fio():
    d = preenche(VA, circ_pts(.22), "#0F0C26", 1.0, 10)
    r = vcirc(VA, .22, BR, 3).set_z_index(11)
    p = ponto7(VA.c2p(0, 0), BR, 5, 12)
    return VGroup(d, r, p)


class LoteA3(Base):
    ANTES = "APLICAÇÃO · MAPAS QUE NÃO ENTORTAM"

    def corpo(self):
        # ── A3-1 · o fio ──
        self.an("A3-1")
        self.secao("APLICAÇÃO · POR QUE UM SOBRE A DISTÂNCIA")
        zera_chapas()
        chA = chapa_px(*LA, nome="A3 palco", v=VA)
        fi = fio()
        lf = TXP30("FIO COM CORRENTE", *canto_xy(VA, -2.55, -2.62), 24, "center", GEO)
        cmp = CampoVivo(VA, PTS, VORTA, MM, .5, p0=1.0, nome="A3 B_α")
        troca(self, "A4 → A3 (palco)")
        self.play(FadeIn(chA), run_time=0.6)
        self.gat("um fio comprido com corrente")
        self.play(FadeIn(fi), FadeIn(lf), run_time=0.5)
        self.gat("as linhas do campo magnético")
        self.play(cresce_campo(cmp, 0.8))
        self.gat("pausa e pensa")
        self.pausa()
        self.ate(1.0)

        # ── A3-2 · a simetria e Ampère ──
        self.an("A3-2")
        BB = TC(r"\B=\dfrac{(-\Y,\ \X)}{(\X^2+\Y^2)^{\alpha}}", 1120, 280, 40)
        self.gat("supondo uma lei de potência")
        self.play(troca_p(cmp, .3, 1.0), caneta(BB, ritmo=0.35), run_time=1.4)
        am = legenda("FORA DO FIO (AMPÈRE):", 1124, 380, GEO, "left", 26)
        self.gat("a lei de ampère diz")
        self.play(FadeIn(am, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── A3-3 · α = 1 (alvo 26) ──
        self.an("A3-3")
        R0 = TC(r"\rot\B=\V{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}", 1120, 460, 38)
        self.gat("o rotacional é dois menos dois alfa")
        self.play(caneta(R0, ritmo=0.35))
        ct, vt = contador(r"2-2\alpha", BR, 1300, 560, 34)
        vt.set_value(2 - 2 * .3)
        self.gat("para ser zero")
        self.play(FadeIn(ct), run_time=0.3)
        self.play(troca_p(cmp, 1.0, 2.0, rate=linear), vt.animate(rate_func=linear).set_value(0.0), run_time=2.0)
        print(f"[A3] 2 − 2α ao vivo: 1,40 → {vt.get_value():.2f}")
        R1 = TC(r"=0\ \Rightarrow\ \alpha=1", 1120, 460, 38)
        R1.shift(RIGHT * (R0.get_right()[0] + 10 / 120 - R1.get_left()[0]))
        self.gat("alfa igual a um")
        self.play(caneta(R1, ritmo=0.4))
        nb = TC(r"\|\B\|=\dfrac{r}{r^2}=\dfrac1r", 1120, 570, 42)
        self.gat("então o tamanho do campo")
        self.play(FadeOut(ct), caneta(nb, ritmo=0.4), run_time=1.2)
        self.remove(ct)
        gf, lbB = grafico("|B|")
        self.gat("o campo do fio cai")
        self.play(Create(gf[0]), Create(gf[1]), FadeIn(gf[2]), FadeIn(gf[3]), run_time=1.0)
        self.ate(1.0)

        # ── A3-4 · o fio carregado ──
        self.an("A3-4")
        lc = TXP30("FIO CARREGADO", *canto_xy(VA, -2.55, -2.62), 24, "center", GEO)
        EE = TC(r"\E=\dfrac{(\X,\ \Y)}{(\X^2+\Y^2)^{\alpha}}", 1120, 280, 40)
        ga = legenda("FORA DO FIO (GAUSS):", 1124, 380, GEO, "left", 26)
        self.gat("faz o mesmo com um fio carregado")
        self.play(FadeOut(lf), FadeIn(lc), run_time=0.4)
        self.remove(lf)
        self.gat("o campo elétrico aponta para fora")
        self.play(gira_setas(cmp, -PI / 2, 1.2), FadeOut(BB), FadeOut(am), FadeOut(R0), FadeOut(R1), run_time=1.2)
        self.remove(BB, am, R0, R1)
        self.play(caneta(EE, ritmo=0.35))
        self.gat("e a lei de gauss diz")
        self.play(FadeIn(ga, shift=0.05 * UP), run_time=0.4)
        DE = TC(r"\dv\E=\D{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}=0\ \Rightarrow\ \alpha=1", 1120, 460, 38)
        self.gat("divergente dois menos dois alfa")
        self.play(caneta(DE, ritmo=0.3))
        ne = TC(r"\|\E\|=\dfrac{r}{r^2}=\dfrac1r", 1120, 570, 42, caneta=False)
        lbE = T("|E|", lbB.get_right()[0] * 120 + 960, 850 - 170 - 12, 24, "right", GEO, bold=False, up=False)
        self.gat("alfa um e o campo também cai")
        self.play(FadeOut(nb), FadeIn(ne), FadeOut(lbB), FadeIn(lbE), run_time=0.5)
        self.remove(nb, lbB)
        self.ate(1.0)

        # ── A3-5 · a carga no espaço (alvo 27) ──
        self.an("A3-5")
        self.secao("APLICAÇÃO · POR QUE UM SOBRE A DISTÂNCIA AO QUADRADO")
        cg = VGroup(preenche(VA, circ_pts(.32), CARGA, 1.0, 10), T("+", *canto_xy(VA, 0, -.2), 36, "center").set_z_index(12))
        cc = campo30(VA, F_CARGA, rmin=.6, mmax=1, skip=clar28([(-3.9, -2.95, -1.4, -2.45)]), nome="A3 carga (corte)")
        lco = TXP30("CORTE PELO PLANO", *canto_xy(VA, -2.65, -2.62), 24, "center", GEO)
        col = [EE, ga, DE, ne, gf[0], gf[1], gf[3], lbE]
        EP = TC(r"\E=\dfrac{X}{\|X\|^{p}}", 1120, 280, 44)
        self.gat("e uma carga pontual")
        self.play(*[FadeOut(m) for m in col + [fi, lc]], FadeOut(cmp), FadeIn(cg), cresce_campo(cc, 0.8), FadeIn(lco), run_time=0.8)
        self.remove(*col, fi, lc, cmp)
        self.gat("escreve o campo como o vetor posição")
        self.play(caneta(EP, ritmo=0.4))
        np1 = T("NO PLANO:", 1120, 412, 28, cor=GEO, bold=False)
        dp = TC(r"\dv\E=\D{\dfrac{2-p}{\|X\|^{p}}}", 1290, 400, 38)
        self.gat("no plano o divergente seria")
        self.play(FadeIn(np1), caneta(dp, ritmo=0.4), run_time=1.2)
        um = TC(r"\dfrac{\partial}{\dx}\Big[\dfrac{\X}{\|X\|^{p}}\Big]=\dfrac{1}{\|X\|^{p}}-\dfrac{p\,\X^2}{\|X\|^{p+2}}", 1120, 620, 36)
        self.gat("faz a conta de uma parcela")
        self.play(caneta(um, ritmo=0.3))
        so = TC(r"\textstyle\sum:\ \dfrac{3}{\|X\|^{p}}-\dfrac{p\,(\X^2+\Y^2+\Z^2)}{\|X\|^{p+2}}=\dfrac{3-p}{\|X\|^{p}}", 1120, 730, 34)
        self.gat("agora soma")
        self.play(caneta(so, ritmo=0.25))
        ne1 = T("NO ESPAÇO:", 1120, 522, 28, cor=GEO, bold=False)
        de3 = TC(r"\dv\E=\D{\dfrac{3-p}{\|X\|^{p}}}", 1290, 510, 38)
        self.gat("então o divergente no espaço")
        self.play(FadeIn(ne1), caneta(de3, ritmo=0.4), run_time=1.2)
        gs = leg_mix(["FORA DA CARGA (GAUSS): div = 0"], 1124, 600, GEO, "left", 26)
        p3 = TC(r"p=3\ \Rightarrow\ \|\E\|=\dfrac{r}{r^3}=\dfrac1{r^2}", 1120, 680, 42)
        self.gat("para zerar o expoente é três")
        self.play(FadeOut(um), FadeOut(so), FadeIn(gs, shift=0.05 * UP), run_time=0.5)
        self.remove(um, so)
        self.play(caneta(p3, ritmo=0.35))
        self.ate(1.0)

        # ── A3-6 · a dimensão e a hipótese ──
        self.an("A3-6")
        d1 = legenda("O EXPOENTE VEM DA DIMENSÃO: 2 NO PLANO, 3 NO ESPAÇO", 1124, 780, GEO, "left", 24)
        d2 = legenda("HIPÓTESE: A SIMETRIA DO CAMPO", 1124, 820, CORAL, "left", 24)
        self.gat("o expoente da lei vem da dimensão")
        self.play(FadeIn(d1, shift=0.05 * UP), run_time=0.4)
        self.gat("junto com a simetria")
        self.play(FadeIn(d2, shift=0.05 * UP), run_time=0.4)
        self.sai_fim()
