"""Lote PAH: A1 (bem-vindos, título, NESTE VÍDEO; o canto entra) e o hook H1–H3: a mesma fórmula (−y, x) como transformação
(a malha com a bandeira gira +90° de uma vez) e como campo (redemoinho; o redemoinho cresce em onda). Sem fórmulas."""
from v7 import *  # noqa: F401,F403

GIRO = lambda x, y: (-y, x)
GIRO = lambda x, y: (-y, x)


class LoteAH(Base):
    CANTO = False

    def corpo(self):
        # ── A1 ──
        self.an("A1")
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(P3(0, 0.9)), num_dashes=48).set_stroke(GEO, 2.2, opacity=o) for r, o in ((2.1, 0.45), (2.45, 0.25))])
        bv = txt("BEM-VINDOS AO PARALLAX LAB", 34).move_to(P3(0, -2.5))
        self.play(FadeIn(logo, scale=0.94), FadeIn(aneis), FadeIn(bv, shift=0.1 * UP), run_time=0.8)
        self.play(Rotate(aneis[0], 0.5), Rotate(aneis[1], -0.4), rate_func=linear, run_time=3.0)
        self.gat("o assunto de hoje")
        tit = VGroup(txt("FUNÇÕES A VALORES VETORIAIS", 46, bold=True), txt("E CAMPOS VETORIAIS", 46, bold=True)).arrange(DOWN, buff=0.18).move_to(P3(0, 1.1))
        nv = linha_texto(txt("NESTE VÍDEO:", 28, bold=True, color=CAMPO), txt("TRANSFORMAÇÃO · IMAGEM · CAMPO VETORIAL", 28)).move_to(P3(0, -1.0))
        self.play(FadeOut(logo), FadeOut(aneis), FadeOut(bv), run_time=0.35)
        self.remove(logo, aneis, bv)
        self.play(FadeIn(tit, shift=0.1 * UP), FadeIn(self.h1), run_time=0.7)
        self.gat("a gente vai ver")
        self.play(FadeIn(nv, shift=0.1 * UP), run_time=0.6)
        self.gat("como transformação e como campo")
        self.play(pulso(nv[1], 1.04), run_time=1.0)
        self.gat("para começar")
        self.play(FadeOut(tit), FadeOut(nv), run_time=0.4)
        self.remove(tit, nv)


        # ── H1 · a malha gira +90° (a bandeira vai junto) ──
        self.an("H1")
        v1 = Vista(960, 580, 105)
        folha = malha7(v1, 3, 1.0)
        band = bandeira7(v1, 0.0, (0, 0), DEST)
        centro = ponto7(v1.c2p(0, 0), WHITE_, 7)
        grupo = VGroup(folha, band)
        self.play(FadeIn(folha), run_time=0.8)
        self.gat("com uma bandeirinha desenhada")
        self.play(FadeIn(band, shift=0.1 * UP), FadeIn(centro), run_time=0.6)
        self.gat("o plano inteiro gira")
        self.play(Rotate(grupo, PI / 2, about_point=v1.c2p(0, 0)), run_time=2.6)
        self.ate(0.97)

        # ── H2 · a mesma regra como campo: o redemoinho cresce em onda (sem pontinhos) ──
        self.an("H2")
        folha0 = malha7(v1, 3, 1.0)
        self.play(FadeOut(grupo), FadeOut(centro), FadeIn(folha0), run_time=0.7)
        self.remove(grupo, centro)
        cmp = campo7(v1, GIRO, -3, 3, -3, 3, passo=0.6, rmin=0.5, rmax=3.3, mmax=3.3, lmax=0.5, nome="H2 (−y, x)")
        self.gat("pendura em cada ponto")
        self.play(LaggedStart(*[GrowArrow(s_) for s_ in sorted(cmp, key=lambda s_: math.hypot(*s_._xy))], lag_ratio=0.03), run_time=2.6)
        self.ate(0.97)

        # ── H3 · dois painéis: a bandeira girada e o redemoinho; a pergunta embaixo (quadro 09) ──
        self.an("H3")
        self.secao("MESMA FÓRMULA, DOIS DESENHOS")
        pe, pd = painel(150, 300, 700, 600), painel(1070, 300, 700, 600)
        vE, vD = Vista(500, 600, 80), Vista(1420, 600, 80)
        mE, silh, bE = malha7(vE, 3, 1.0), bandeira7(vE, 0.0, (0, 0), DEST, alpha=0.22), bandeira7(vE, PI / 2, (0, 0), DEST)
        oE = ponto7(vE.c2p(0, 0), WHITE_, 7)
        mD = malha7(vD, 3, 1.0)
        cD = campo7(vD, GIRO, -3, 3, -3, 3, passo=0.6, rmin=0.5, rmax=3.3, mmax=3.3, lmax=0.5, nome="H3 (−y, x)")
        fH = TC(r"(\X,\Y)\;\longmapsto\;(-\Y,\;\X)", 960, 235, 56, "c")
        lE, lD = legenda("TRANSFORMAÇÃO: A BANDEIRA GIRA", 500, 950, WHITE_, "center"), legenda("CAMPO: UMA SETA EM CADA PONTO", 1420, 950, CAMPO2, "center")
        perg = T("QUAL É O DESENHO CERTO?", 960, 1035, 34, "center", SAI_F)
        self.play(FadeOut(folha0), FadeOut(cmp), FadeIn(pe), FadeIn(pd), FadeIn(mE), FadeIn(silh), FadeIn(bE), FadeIn(oE), FadeIn(mD), FadeIn(cD), run_time=0.9)
        self.gat("é a mesma fórmula")
        cf = caneta(fH)
        self.play(cf, FadeIn(lE), FadeIn(lD), run_time=max(cf.tot, 0.6))
        self.gat("qual dos dois")
        self.play(FadeIn(perg, shift=0.1 * UP), run_time=0.6)
        self.sai_fim()
