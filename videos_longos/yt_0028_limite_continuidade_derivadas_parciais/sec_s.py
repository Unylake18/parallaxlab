"""Lote PS · RESUMO (v2; alvo 31) e CTA. O palco do B6 (modelo linear local em contexto, ZOOM × 10) com o quadradinho final; a matriz e,
uma por gatilho do resumo, rot = 3, div = 1 e deformação = 1 e 1; em "uma curiosidade", as duas legendas do espaço. E7: o S termina inteiro, fica
1,5 s parado e só então entra o CTA padrão do canal."""
from v28 import *  # noqa: F401,F403
from sec_b6 import SQ, V


class LoteS(Base):
    ANTES = "O DESAFIO"

    def corpo(self):
        # ── S1 ──
        self.an("S1")
        self.secao("RESUMO")
        M = expJA(.35)
        fl = [tuple(M @ np.array(p, float)) for p in SQ]
        zera_chapas()
        chA, znA = chapa_px(*LAY_A, nome="A (S)"), zona_px(1080, 180, 1920, 1020, "coluna A (S)")
        cmp = campo28(V, F_LIN, y1=2.5, rmin=.3, mmax=6, ctx=True, skip=ou(clarPoly(fl, .25), clarPoly(SQ, .15)), nome="S modelo linear (contexto)")
        ped = Pedaco(V, fl)
        P = ponto7(V.c2p(0, 0), POS, 10, 12)
        self.play(FadeIn(chA), FadeIn(znA), cresce_campo(cmp, 1.0), FadeIn(ped), FadeIn(P), run_time=1.0)     # final §2.7: a tag do zoom não aparece no resumo
        jn = TC(r"J=\begin{pmatrix}\Am{1} & \Mg{-1}\\ \Am{2} & \Mg{0}\end{pmatrix}", 1120, 330, 48)
        self.gat("a derivada parcial é a velocidade")
        self.play(caneta(jn, ritmo=0.5))
        r = TC(r"\V{\rot = 3}", 1120, 480, 44)
        d = TC(r"\D{\dv = 1}", 1120, 560, 44)
        f = TC(r"\Lm{\text{deformação} = 1 \text{ e } 1}", 1120, 640, 44)
        for m, g in zip((r, d, f), ("giro", "área", "deformação")):
            self.gat(g)
            self.play(caneta(m, ritmo=0.3))
        e1 = legenda("NO ESPAÇO: 9 NÚMEROS", 1124, 740, GEO, "left", 26)
        e2 = legenda("3 DE GIRO + 1 DE VOLUME + 5 DE DEFORMAÇÃO", 1124, 785, GEO, "left", 26)
        self.gat("uma curiosidade")
        self.play(FadeIn(e1, shift=0.06 * UP), run_time=0.5)
        self.gat("três de giro")
        self.play(FadeIn(e2, shift=0.06 * UP), run_time=0.5)
        self.ate(1.0)                        # final: sem o 1,5 s parado (a fala do S2 começa no fim do S1; o resumo sai na frase do gancho)

        # ── S2 · gancho do próximo vídeo (handoff final §2.2, alvo 40) e CTA ──
        self.an("S2")
        g1 = T("NO PRÓXIMO VÍDEO", 960, 215, 34, "center", GEO, bold=False)
        g2 = T("EXERCÍCIOS DO MÓDULO", 960, 305, 72, "center")
        sai = self.snap() + [m for m in (self.h1, self.h2) if m is not None]
        self.gat("no próximo vídeo")
        self.play(*[FadeOut(m) for m in sai], FadeIn(g1, shift=0.06 * UP), run_time=0.4)        # o resumo sai; o cartão do gancho não tem canto
        self.remove(*sai)
        self.h2 = None
        self.gat("o integrador do módulo")
        self.play(FadeIn(g2, shift=0.06 * UP), run_time=0.4)
        zera_chapas()                           # o palco do resumo saiu: as margens das setas valem contra as miniaturas
        mini = [mini_card(i) for i in range(5)]
        for (fr, _), (card, extra) in zip(MINI, mini):
            self.gat(fr)
            self.play(FadeIn(card), run_time=0.3)
            for e in extra:
                self.play(caneta(e, ritmo=0.5))
            print(f"[S2] miniatura «{fr}»")
        self.gat("se essa aula te ajudou")
        logo_cta(self, rt_fim=2.0)              # o CTA fica até o fim da fala + 3 s (a âncora S2 termina 1 s depois do fim do WAV)


MINI = [("campo vetorial", ("CAMPO", "VETORIAL"), GEO), ("rotacional", ("ROTACIONAL",), VIO), ("divergente", ("DIVERGENTE",), "#7FB2FF"),
        ("limite e continuidade", ("LIMITE E", "CONTINUIDADE"), CAMPO2), ("derivadas parciais", ("DERIVADAS", "PARCIAIS"), AMB)]
MINI = [(a, (b, c)) for a, b, c in MINI]


def mini_card(i):
    """Miniatura 300×300 (x0 = 120 + 345·i, y 410–710), grade do eixo a 60 px/u (quadradinho 30 px), moldura de 4 px na cor do tema; nome embaixo.
    Devolve (grupo para o FadeIn, fórmulas para a caneta)."""
    fr, (nomes, cor) = MINI[i]
    x0 = 120 + 345 * i
    v = Vista(x0 + 150, 560, 60)
    ch = chapa_px(x0, 410, x0 + 300, 710, nome=f"S2 miniatura {i + 1}", v=v)
    ch[-1].set_stroke(cor, 4 / 1.2, 1)
    g = VGroup(ch)
    extra = []
    if i == 0:
        g.add(campo28(v, F_SELA, -1.5, 1.5, -1.5, 1.5, 1.0, rmin=0, mmax=2.2, nome="S2 (x, −y)"))
    elif i in (1, 2):
        s0 = 0.9
        if i == 1:
            a = 0.6
            pts = [(x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)) for x, y in quad_pts((0, 0), s0)]
            g.add(campo28(v, F_GIRO, -1.5, 1.5, -1.5, 1.5, 1.0, rmin=1.0, mmax=2.2, nome="S2 (−y, x)"))
        else:
            pts = quad_pts((0, 0), s0 * 1.3)
            g.add(campo28(v, F_EXPL, -1.5, 1.5, -1.5, 1.5, 1.0, rmin=1.0, mmax=2.2, nome="S2 (x, y)"))
        g.add(Pedaco(v, pts, z=8))
    elif i == 3:
        g.add(vcirc(v, 1.7, CAMPO2, 3).set_z_index(6), ponto7(v.c2p(0, 0), CAMPO2, 5, 9),
              seta7(v.c2p(0, 0), v.c2p(1.7, 0), CAMPO2, 6, 22).set_z_index(9), seta7(v.c2p(0, 0), v.c2p(1.15, .78), CAMPO, 5, 19).set_z_index(9),
              TP(r"\eps", *canto_xy(v, 1.38, 1.42), 26))
    else:
        f1 = TC(r"\dfrac{\partial\F}{\dx}", *canto_xy(v, 0, .95), 40, "c")
        f2 = TC(r"\dfrac{\partial\F}{\dy}", *canto_xy(v, 0, -.95), 40, "c")
        extra = [f1, f2]
    for k, n in enumerate(nomes):
        g.add(T(n, x0 + 150, 775 + 36 * k, 28, "center", cor))
    return g, extra
