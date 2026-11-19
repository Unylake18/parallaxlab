"""Lote PH · H gancho (alvo 03) + A bem-vindos (alvos 01 e 02). H: layout C, três cartões com a rede (passo 0,75) e o fantasma do quadradinho
(nenhum quadradinho anda no gancho); fórmulas e título em caneta; no "por que o campo magnético" o título troca por POR QUE 1/r? POR QUE 1/r²?.
Sem canto; o logo do canto fica (como no alvo 03 e no EP. 03). A: abertura clássica do EP. 03; a logo sobe e encolhe; as três linhas uma por vez; PAUSE E TENTE (demonstração);
o canto e o logo do canto entram no fim."""
from lib30 import *  # noqa: F401,F403

CARTOES = [(0, F1, r"\F=(\X+\Y,\ \X-\Y)", (0, 0), 1.6, 4), (1, F2, r"\F=(1,\ \X-\Y)", (0, 0), 1.6, 4), (2, F3, r"\F=(\X^2-\Y^2,\ 2\X\Y)", (1, 1), 1.2, 8)]


def cartao_h(i):
    k, Fv, tex, c, s, mm = CARTOES[i]
    X0 = CC[k][0]
    v = VB(CC[k], X0 + 240, 540, 56)
    ch = chapa_px(*CC[k], nome=f"H cartão {k + 1}", v=v)
    cmp = campo30(v, Fv, -3.5, 3.5, -3.5, 3.5, .75, rmin=0, mmax=mm, skip=dq(c, s), nome=f"H cartão {k + 1}")
    fan = fantasma(v, quad_pts(c, s))
    f = TC(tex, X0 + 240, 840, 36, "c")
    return VGroup(ch, cmp, fan), f


class LoteH(Base):
    CANTO = False

    def corpo(self):
        # ── H · gancho (alvo 03) ──
        self.an("H-1")
        zera_chapas()
        cs = [cartao_h(i) for i in range(3)]
        self.play(FadeIn(cs[0][0]), run_time=0.6)
        self.play(FadeIn(cs[1][0]), caneta(cs[0][1], ritmo=0.25), run_time=0.6)
        self.play(FadeIn(cs[2][0]), caneta(cs[1][1], ritmo=0.25), run_time=0.6)
        self.play(caneta(cs[2][1], ritmo=0.25))
        tit = T("QUAL GIRA? QUAL MUDA DE ÁREA? QUAL ENTORTA?", 960, 215, 40, "center")
        tit._caneta, tit._esc, tit._em_caneta, tit._tex = True, False, False, "QUAL GIRA?"
        self.gat("um vai girar")
        self.play(caneta(tit, ritmo=0.12))
        fs_ = legenda("A FÓRMULA JÁ SABE", 960, 930, GEO, "center", 30)
        self.gat("dá e hoje")
        self.play(caneta(fs_, ritmo=0.2))
        t2 = T("POR QUE 1/r? POR QUE 1/r²?", 960, 215, 40, "center", up=False)
        self.gat("por que o campo magnético")
        troca_linha(self, tit, t2)
        self.ate(1.0)

        # ── A · bem-vindos (alvos 01 e 02) ──
        self.an("A-1")
        LC = (960, 420)
        logo = self.logo(668 / 120).move_to(PX(*LC))
        aneis = VGroup(*[DashedVMobject(Circle(radius=r / 120).move_to(PX(*LC)), num_dashes=int(2 * PI * r / 20)).set_stroke(GEO, 2 / 1.2, opacity=0.45)
                         for r in (668 * .467, 668 * .434)])
        for m in aneis.get_family():
            m._sem_contorno = True
        bv = T("BEM-VINDOS AO PARALLAX LAB", 960, 850, 46, "center")
        self.limpa_junto()
        troca(self, "H → A (abertura)")
        self.play(FadeIn(logo, scale=0.94), FadeIn(aneis), FadeIn(bv, shift=0.1 * UP), FadeOut(self.wm), run_time=0.8)
        self.remove(self.wm)
        gira = lambda rt: (Rotate(aneis[0], 0.12 * rt, about_point=aneis[0].get_center(), rate_func=linear),
                           Rotate(aneis[1], -0.1 * rt, about_point=aneis[1].get_center(), rate_func=linear))

        def ate_frase(fr):
            rt = self.falta(fr)
            if rt >= 0.2:
                self.play(*gira(rt), run_time=rt)
            self.gat(fr)

        cal = T("CÁLCULO III", 960, 478, 28, "center", GEO, bold=False)
        tit = T("EXERCÍCIOS DO MÓDULO", 960, 566, 54, "center")
        nv = T("NESTE VÍDEO:", 960, 646, 30, "center", CAMPO)

        def duo(a, b, y):
            pa = T(a, 0, y, 36, "left")
            pp = T("·", 0, y, 36, "left", GEO, bold=False)
            pb = T(b, 0, y, 36, "left", CAMPO2, bold=False)
            pp.move_to([pa.get_right()[0] + 12 / 120 + pp.width / 2, pa.get_center()[1], 0])
            pb.shift(RIGHT * (pp.get_right()[0] + 12 / 120 - pb.get_left()[0]))
            g = VGroup(pa, pp, pb)
            return g.shift(RIGHT * (PX(960, 0)[0] - g.get_center()[0]))
        linhas = [duo("A ESCADA", "CINCO DEGRAUS DE PROBLEMAS", 722), duo("O DESAFIO", "PREVER O QUADRADINHO", 775),
                  duo("AS APLICAÇÕES", "RIO, PAREDE, MAPAS E FIOS", 828)]
        ate_frase("esse é o quarto episódio")
        k = 380 / 668
        Lg = Group(logo, aneis)
        self.play(Lg.animate.scale(k).move_to(PX(960, 250)), FadeOut(bv), FadeIn(cal, shift=0.06 * UP), run_time=1.0)
        self.remove(bv)
        for fr, m in (("o integrador do módulo", tit), ("vai ser uma escada", nv)):
            ate_frase(fr)
            self.play(FadeIn(m, shift=0.06 * UP), *gira(0.5), run_time=0.5)
        self.play(FadeIn(linhas[0], shift=0.06 * UP), *gira(0.5), run_time=0.5)
        for fr, m in (("no topo da escada", linhas[1]), ("na segunda parte", linhas[2])):
            ate_frase(fr)
            self.play(FadeIn(m, shift=0.06 * UP), *gira(0.5), run_time=0.5)
        ate_frase("pausa o vídeo e tenta")
        self.pausa(dur=min(3.0, self.resta() - 0.9))
        self.play(FadeIn(self.h1), FadeIn(self.wm), *gira(0.5), run_time=0.5)     # o canto e o logo do canto entram no fim da abertura (R10)
        rt = self.resta()
        if rt >= 0.2:
            self.play(*gira(rt), run_time=rt)
        self.sai_fim()
