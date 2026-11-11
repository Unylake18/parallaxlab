"""Lote PS · RESUMO (layout A; alvo 18) e CTA. O palco do B6 (modelo linear local em contexto, ZOOM × 10) com o quadradinho final; a matriz e,
uma por gatilho do resumo, rot = 3 (violeta), div = 1 (azul-claro) e deformação = 1 e 1 (lima). Sem repetir os cartões. CTA padrão do canal."""
from v28 import *  # noqa: F401,F403
from sec_b6 import SQ, V, modelo_lbl, zoom_lbl


class LoteS(Base):
    ANTES = "O DESAFIO"

    def corpo(self):
        # ── S1 ──
        self.an("S1")
        self.secao("RESUMO")
        M = expJA(.35)
        fl = [tuple(M @ np.array(p, float)) for p in SQ]
        cmp = campo28(V, F_LIN, y1=2.5, rmin=.3, mmax=6, ctx=True, skip=ou(clarPoly(fl, .25), clarPoly(SQ, .15)), nome="S modelo linear (contexto)")
        ped = Pedaco(V, fl)
        P = ponto7(V.c2p(0, 0), POS, 10, 12)
        self.play(cresce_campo(cmp, 1.0), FadeIn(ped), FadeIn(P), FadeIn(zoom_lbl()), FadeIn(modelo_lbl()), run_time=1.0)
        jn = TC(r"J=\begin{pmatrix}\Am{1} & \Mg{-1}\\ \Am{2} & \Mg{0}\end{pmatrix}", 1120, 330, 48)
        self.gat("a derivada parcial diz")
        self.play(caneta(jn, ritmo=0.6))
        r = TC(r"\V{\rot = 3}", 1120, 480, 44)
        d = TC(r"\D{\dv = 1}", 1120, 560, 44)
        f = TC(r"\Lm{\text{deformação} = 1 \text{ e } 1}", 1120, 640, 44)
        for m, g in zip((r, d, f), ("giro", "área", "deformação")):
            self.gat(g)
            self.play(caneta(m, ritmo=0.35))
        self.ate(0.97)

        # ── S2 · CTA ──
        self.an("S2")
        self.gat("no próximo vídeo")
        logo_cta(self)
