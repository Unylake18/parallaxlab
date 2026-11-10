"""Lote PS · RESUMO (S1, S2) e CTA (layout C, quadro 19). Funciona depois do B6 e depois do B7 (começa do papel vazio, com a linha 1 do canto).
S1: três cartões que entram um por vez na fala (TRANSFORMAÇÃO = disco das polares; SUPERFÍCIE = a tigela em 3D; CAMPO = o redemoinho), cada um com a sua fórmula embaixo,
e f : A ⊂ ℝⁿ → ℝᵐ no pé. S2: o disco e o redemoinho lado a lado (layout B). CTA: tudo sai; barquinho parado no redemoinho e a pergunta; logo e INSCREVA-SE."""
from v7 import *  # noqa: F401,F403

GIRO = lambda x, y: (-y, x)
XS = (140, 720, 1300)


def disco_polar(v, w_circ=2.0):
    g = VGroup()
    ch = Circle(radius=2 * v.ux).move_to(v.c2p(0, 0)).set_fill(CHAPA, 0.9).set_stroke(width=0)
    ch._sem_contorno = True
    g.add(ch)
    for k in range(8):
        a = k * PI / 4
        g.add(linha7([v.c2p(0, 0), v.c2p(2 * math.cos(a), 2 * math.sin(a))], E1, w_circ))
    for k in range(1, 5):
        g.add(circ7(v, 0.5 * k, E2, 3.5 if k == 4 else w_circ))
    return g.set_z_index(2)


def barquinho(c, s=0.55):
    """Objeto de teste (coral)."""
    casco = Polygon(c + s * P3(-0.75, 0), c + s * P3(0.75, 0), c + s * P3(0.5, -0.35), c + s * P3(-0.5, -0.35)).set_stroke(DEST, 2.5).set_fill(DEST, 1)
    vela = Polygon(c + s * P3(0, 0.05), c + s * P3(0, 0.9), c + s * P3(0.5, 0.05)).set_stroke(SAI_F, 2.5).set_fill(SAI_F, 0.9)
    return contorno(VGroup(casco, vela)).set_z_index(8)


class LoteS(Base):
    def corpo(self):
        # ── S1 · os três cartões (quadro 19) ──
        self.an("S1")
        self.secao("RESUMO")
        cart = [painel(x, 260, 480, 460, r, WHITE_) for x, r in zip(XS, ("TRANSFORMAÇÃO", "SUPERFÍCIE", "CAMPO"))]
        forms = [TC(r"\varphi(\th,\rh) = (\rh\cos\th,\;\rh\,\sen\th)", XS[0] + 240, 780, 30, "c", caneta=False),
                 TC(r"f(\U,\V) = (\U,\V,\U^2+\V^2)", XS[1] + 240, 780, 30, "c", caneta=False),
                 TC(r"\F(\X,\Y) = -\Y\,\ii + \X\,\jj", XS[2] + 240, 780, 30, "c", caneta=False)]
        v1 = Vista(380, 490, 85)
        dsc = disco_polar(v1)
        BOX = [740, 280, 440, 420]
        tig = Fundo3D(self, "c7_paraboloide", lambda t: {"s": 1.0, "box": BOX}, op=0.0)
        self.add(tig)
        v3 = Vista(1540, 490, 62)
        rdm = campo7(v3, GIRO, -3, 3, -3, 3, passo=0.75, rmin=0.5, rmax=3.3, mmax=3.3, lmax=0.6, nome="S1 redemoinho")
        fdef = TC(r"f : {\G A}\subset\mathbb{R}^n\to\mathbb{R}^m", 960, 920, 56, "c")
        self.gat("como transformação ela move os pontos")
        self.play(caneta(fdef))
        self.gat("segmentos viram circunferências")
        self.play(FadeIn(cart[0]), Create(dsc), FadeIn(forms[0]), run_time=1.4)
        self.gat("folhas viram tigelas")
        self.play(FadeIn(cart[1]), tig.op.animate.set_value(1.0), FadeIn(forms[1]), run_time=1.0)
        self.gat("ela pendura uma seta em cada ponto")
        self.play(FadeIn(cart[2]), LaggedStart(*[GrowArrow(s_) for s_ in rdm], lag_ratio=0.02), FadeIn(forms[2]), run_time=1.6)
        self.gat("e as duas leituras são necessárias")
        self.play(pulso(dsc, 1.04), pulso(rdm, 1.04), run_time=1.0)

        # ── S2 · o disco das polares e o redemoinho, lado a lado ──
        self.an("S2")
        self.play(FadeOut(VGroup(*cart, *forms, fdef)), tig.op.animate.set_value(0.0), run_time=0.5)
        tig.clear_updaters()
        self.remove(*cart, *forms, fdef, tig)
        pa, pb = painel(150, 300, 700, 600), painel(1070, 300, 700, 600)
        vA, vB = Vista(500, 600, 80), Vista(1420, 600, 80)
        d2 = disco_polar(vA)
        r2 = campo7(vB, GIRO, -3, 3, -3, 3, passo=0.6, rmin=0.5, rmax=3.3, mmax=3.3, lmax=0.5, nome="S2 redemoinho")
        self.play(FadeOut(dsc), FadeOut(rdm), FadeIn(pa), FadeIn(pb), FadeIn(d2), FadeIn(r2), run_time=0.8)
        self.remove(dsc, rdm)
        self.gat("trocar de coordenadas dentro de uma integral")
        self.play(pulso(d2, 1.05), run_time=1.0)
        self.gat("os campos voltam")
        self.play(pulso(r2, 1.05), run_time=1.0)

        # ── CTA ──
        self.an("CTA")
        tudo = [m for m in self.mobjects if m is not self.clk and not isinstance(m, ValueTracker)]
        vC = Vista(960, 594, 120)
        rdc = campo7(vC, GIRO, -3, 3, -3, 3, passo=1.0, rmin=0.5, rmax=3.3, mmax=3.3, lmax=0.7, nome="CTA redemoinho")
        barco = barquinho(vC.c2p(1.6, 0.0))
        perg = T("O BARQUINHO GIRA EM TORNO DE SI MESMO?", 960, 150, 40, "center")
        self.play(*[FadeOut(m) for m in tudo], FadeIn(rdc), run_time=0.6)
        self.remove(*tudo)
        self.h2 = None
        self.play(FadeIn(barco, shift=0.15 * DOWN), FadeIn(perg, shift=0.1 * DOWN), run_time=0.6)
        CL = P3(0, 0.9)
        logo = self.logo(5.6).move_to(CL)
        aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(CL), num_dashes=48).set_stroke(GEO, 2.6, opacity=o) for r, o in ((2.1, 0.85), (2.45, 0.6))])
        ins = VGroup(txt("INSCREVA-SE PARA ACOMPANHAR", 40, bold=True), txt("OS PRÓXIMOS VÍDEOS", 40, bold=True)).arrange(DOWN, buff=0.12).move_to(P3(0, -2.6))
        self.gat("deixa a sua resposta")
        self.play(FadeOut(VGroup(rdc, barco, perg)), FadeIn(logo, scale=0.96), FadeIn(aneis), FadeIn(ins, shift=0.1 * UP), run_time=0.45)
        self.remove(rdc, barco, perg)
        rt = self.resta() + 3.0                                   # até o fim da fala e mais 3 s de hold
        self.play(Rotate(aneis[0], 0.3 * rt, rate_func=linear), Rotate(aneis[1], -0.24 * rt, rate_func=linear), run_time=rt)
