"""Lote PB3 · CONTINUIDADE (layout C; alvo 05). Três cartões 480×460 (x = 140, 720, 1300; y 250–710; 1 u = 56 px), um por vez:
CONTÍNUO (campo da aula, disco laranja e P), FORA DO DOMÍNIO (campo da carga, carga azul + e anel tracejado vazio), DESCONTÍNUO (G, P na origem e G(0,0) = 0⃗)."""
from v28 import *  # noqa: F401,F403

CARTOES = [(140, "CONTÍNUO", "AS SETAS NÃO SALTAM"), (720, "FORA DO DOMÍNIO", "AQUI O CAMPO NÃO EXISTE"), (1300, "DESCONTÍNUO", "EXISTE, MAS SEM LIMITE")]


def cartao(i):
    X0, t1, t2 = CARTOES[i]
    v = Vista(X0 + 240, 480, 56)
    g = VGroup(painel(X0, 250, 480, 460))
    if i == 0:
        cmp = campo28(v, F_AULA, -3.6, 3.6, -3.6, 3.6, .9, rmin=0, mmax=3.5, skip=clar28([], [(0, 0, .75)]), nome="B3 cartão 1 (aula)")
        extra = VGroup(vcirc(v, .75, POS, 3), ponto7(v.c2p(0, 0), POS, 8), seta7(v.c2p(-.4, 0), v.c2p(.4, 0), CAMPO2, 6, 18).set_z_index(9))
    elif i == 1:
        cmp = campo28(v, F_CARGA, -3.6, 3.6, -3.6, 3.6, .9, rmin=1.1, mmax=1, nome="B3 cartão 2 (carga)")
        mais = T("+", *canto_xy(v, 0, -.28), 34, "center")
        extra = VGroup(preenche(v, circ_pts(.7), ESC, 1, 6), vcirc(v, .7, GEO, 3, dash=(7, 7)).set_z_index(6.5), preenche(v, circ_pts(.42), CARGA, 1, 7), mais)
    else:
        cmp = campo28(v, F_DIAG, -3.6, 3.6, -3.6, 3.6, .9, rmin=.3, prop=True, skip=clar28([(-.2, -1.9, 3.1, -.95)]), nome="B3 cartão 3 (G)")
        extra = VGroup(ponto7(v.c2p(0, 0), POS, 8), TP(r"\G(0,0) = \vec 0", *canto_xy(v, 1.45, -1.4), 30))
    tit = T(t1, X0 + 240, 775, 34, "center")
    leg = legenda(t2, X0 + 240, 825, GEO, "center", 26)
    return g, cmp, extra, VGroup(tit, leg)


class LoteB3(Base):
    ANTES = "QUANDO O LIMITE NÃO EXISTE"

    def corpo(self):
        # ── B3-1 · a definição ──
        self.an("B3-1")
        self.secao("CONTINUIDADE")
        dfn = TC(r"\F \text{ contínua em } \Pt \iff \lim\limits_{\Xp\to\Pt}\F(\Xp)=\F(\Pt)", 960, 930, 44, "c")
        self.gat("quando o limite ali existe e é igual")
        self.play(caneta(dfn, ritmo=0.6))
        self.ate(0.97)

        # ── B3-2 · os três cartões ──
        self.an("B3-2")
        for i, fr in enumerate(("no primeiro", "no segundo", "no terceiro")):
            p, cmp, extra, txs = cartao(i)
            self.gat(fr)
            self.play(Create(p), cresce_campo(cmp, 0.9), FadeIn(extra), run_time=1.0)
            self.play(FadeIn(txs, shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)

        # ── B3-3 · por componentes ──
        self.an("B3-3")
        cc = leg_mix(["CONTÍNUA", r"$\Leftrightarrow$", "CADA COMPONENTE É CONTÍNUA"], 960, 1012, GEO, "center", 28, up=True)
        self.gat("de novo dá para trabalhar por componentes")
        self.play(FadeIn(cc, shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)
        self.sai_fim()
