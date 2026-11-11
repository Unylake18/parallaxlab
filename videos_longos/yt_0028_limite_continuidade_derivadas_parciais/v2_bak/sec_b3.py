"""Lote PB3 · CONTINUIDADE (v2; alvos 08 e 09). B3-1 (layout B): o desafio do B1 com δ = 0,41 e ε = 1, agora com P CHEIO e o disco ε em volta
de L⃗ = F⃗(P); os três pedaços da definição entram no alto, um por gatilho. B3-2 (layout C): três cartões, cada um quebrando um pedaço:
① a carga (fora do domínio), ② o G (sem limite), ③ o campo (1, 0) com a seta do centro para cima (salto no ponto)."""
from v28 import *  # noqa: F401,F403
from sec_b1 import ANG, nomes_b

VE, VD = Vista(480, 540, 140), Vista(1250, 560, 140)


def circ_n(n, cor=CAMPO2, size=30):
    return num_circ(n, cor, size)


def pedacos():
    gs = [leg_mix([circ_n(1), "P NO DOMÍNIO", r"$\checkmark$"], 960, 212, CAMPO2, "left", 30, up=False, gap=10),
          leg_mix([circ_n(2), "O LIMITE EXISTE", r"$\checkmark$"], 960, 212, CAMPO2, "left", 30, up=False, gap=10),
          leg_mix([circ_n(3), "LIMITE = F(P)", r"$\checkmark$"], 960, 212, CAMPO2, "left", 30, up=False, gap=10)]
    tot = sum(g.width for g in gs) + 2 * 62 / 120
    x = -tot / 2
    for g in gs:
        g.shift(RIGHT * (x - g.get_left()[0]))
        x += g.width + 62 / 120
    return gs


CART = [(140, 1, "FORA DO DOMÍNIO", ["F(P) NEM EXISTE"]), (720, 2, "SEM LIMITE", ["F(P) EXISTE, O LIMITE NÃO"]),
        (1300, 3, "SALTO NO PONTO", ["O LIMITE EXISTE, MAS", r"$\neq$", "F(P)"])]


def cartao(i):
    X0, n, t1, t2 = CART[i]
    v = Vista(X0 + 240, 480, 56)
    p = painel(X0, 250, 480, 460)
    if i == 0:
        cmp = campo28(v, F_CARGA, -3.6, 3.6, -3.6, 3.6, .9, rmin=1.1, mmax=1, nome="B3 ① carga")
        extra = VGroup(preenche(v, circ_pts(.7), ESC, 1, 6), vcirc(v, .7, GEO, 3, dash=(7, 7)).set_z_index(6.5), preenche(v, circ_pts(.42), CARGA, 1, 7),
                       T("+", *canto_xy(v, 0, -.28), 34, "center"))
    elif i == 1:
        cmp = campo28(v, F_DIAG, -3.6, 3.6, -3.6, 3.6, .9, rmin=.3, prop=True, skip=clar28([(-.2, -1.9, 3.1, -.95)]), nome="B3 ② G")
        extra = VGroup(ponto7(v.c2p(0, 0), POS, 8), TP(r"\G(0,0) = \vec 0", *canto_xy(v, 1.45, -1.4), 30))
    else:
        cmp = campo28(v, lambda X, Y: (1.0, 0.0), -3.6, 3.6, -3.6, 3.6, .9, rmin=0, mmax=1, skip=clar28([(-1.9, -.6, 1.9, 2.4)], [(0, 0, .6)]), nome="B3 ③ salto")
        extra = VGroup(vlinha(v, [(0, 0), (1.6, 0)], GEO, 3, dash=(7, 7)), seta7(v.c2p(1.3, 0), v.c2p(1.62, 0), GEO, 3, 14),
                       seta7(v.c2p(0, 0), v.c2p(0, 1.6), CAMPO2, 7, 20).set_z_index(9), ponto7(v.c2p(0, 0), POS, 8, 10),
                       TP(r"\F(\Pt)", *canto_xy(v, -.95, 1.25), 28), TP(r"\Lv", *canto_xy(v, 1.2, .45), 28))
    tit = leg_mix([circ_n(n, WHITE_, 32), t1], X0 + 240, 775, WHITE_, "center", 32, up=False, bold=True, gap=8)
    leg = leg_mix(t2, X0 + 240, 825, GEO, "center", 26, up=False, gap=6)
    return p, cmp, extra, VGroup(tit, leg)


class LoteB3(Base):
    ANTES = "QUANDO O LIMITE NÃO EXISTE"

    def corpo(self):
        # ── B3-1 · três pedaços; o desafio com o ε em F(P) (alvo 08) ──
        self.an("B3-1")
        self.secao("CONTINUIDADE")
        d, ep = .41, 1.0
        pE, pD = painel(*PAINEL_E[:2], 700, 560), painel(*PAINEL_D[:2], 700, 560)
        Xa = (.62 * d * math.cos(ANG), .62 * d * math.sin(ANG))
        cmp = campo28(VE, F_AULA, -2.25, 2.25, -1.75, 1.75, .5, rmin=0, mmax=3.5, ctx=True,
                      skip=clar28([(-.85, -.5, -.45, .15), (Xa[0] - .2, Xa[1] + .15, Xa[0] + .4, Xa[1] + .62)], [(0, 0, d + .12)]), nome="B3-1 campo da aula (contexto)")
        nm = nomes_b()
        self.play(Create(pE), Create(pD), cresce_campo(cmp, 1.0), FadeIn(nm), run_time=1.0)
        P = ponto7(VE.c2p(0, 0), POS, 9, 11)
        sP = seta7(VE.c2p(0, 0), VE.c2p(.42 * .8, 0), CAMPO2, 6, 18).set_z_index(10)
        lP = TP(r"\Pt", *canto_xy(VE, -.25, -.3), 36)
        pc = pedacos()
        self.gat("um o ponto está no domínio")
        self.play(FadeIn(P, scale=0.5), GrowArrow(sP), FadeIn(lP), FadeIn(pc[0], shift=0.06 * DOWN), run_time=0.8)
        self.gat("dois o limite ali existe")
        self.play(FadeIn(pc[1], shift=0.06 * DOWN), run_time=0.5)
        self.gat("três o limite é igual")
        self.play(FadeIn(pc[2], shift=0.06 * DOWN), run_time=0.5)
        org = ponto7(VD.c2p(0, 0), GEO, 6)
        sL = seta7(VD.c2p(0, 0), VD.c2p(1, 0), CAMPO2, 7, 24).set_z_index(9)
        lL = TP(r"\Lv=\F(\Pt)", *canto_xy(VD, -.2, -.45), 32)
        cE = vcirc(VD, ep, CAMPO2, 3, c=(1, 0)).set_z_index(6)
        lE = TP(r"\eps", *canto_xy(VD, 1 + .75 + .22, .75 + .2), 36)
        dD = VGroup(preenche(VE, circ_pts(d), DELTA_C, 1, 4), vcirc(VE, d, POS, 3).set_z_index(5))
        lD = TP(r"\del", *canto_xy(VE, -d - .25, .05), 36)
        dfn = TC(r"\F\text{ contínua em }\Pt\iff\lim\limits_{\Xp\to\Pt}\F(\Xp)=\F(\Pt)", 960, 960, 42, "c")
        self.gat("na figura")
        self.play(FadeIn(org), GrowArrow(sL), FadeIn(lL), Create(cE), FadeIn(lE), FadeIn(dD), FadeIn(lD), run_time=1.0)
        self.play(caneta(dfn, ritmo=0.5))
        man = Mancha(VD, lambda: d, lambda: ep)
        guarda(self, man, PAINEL_D, "mancha")
        Xd = ponto7(VE.c2p(*Xa), POS, 6, 10)
        fX = F_AULA(*Xa)
        aFX = seta7(VD.c2p(0, 0), VD.c2p(*fX), CAMPO, 5, 20).set_z_index(8)
        lX = TP(r"\Xp", *canto_xy(VE, Xa[0] + .05, Xa[1] + .36), 30)
        lFX = TP(r"\F(\Xp)", *canto_xy(VD, fX[0] - .35, fX[1] + .3), 30)
        self.gat("no nosso campo a mancha cabe")
        self.play(FadeIn(man), FadeIn(Xd, scale=0.5), GrowArrow(aFX), FadeIn(lX), FadeIn(lFX), run_time=0.9)
        print(f"[B3] mancha δ = 0,41 dentro de ε = 1: distância máxima {man.atualiza().dist:.4f}")
        self.ate(0.97)

        # ── B3-2 · três jeitos de dar errado (alvo 09) ──
        self.an("B3-2")
        sai = [m for m in self.snap() if m is not dfn]
        self.play(*[FadeOut(m) for m in sai], dfn.animate.move_to(PX(960, 930)), run_time=0.6)
        self.remove(*sai)
        # v2 (holds): cada cartão entra por partes, no ritmo da fala: campo → o que quebra → título
        etapas = [("no campo elétrico", "nem está no domínio", "falha o primeiro pedaço"),
                  ("no campo encrenqueiro", "a seta existe", "falha o segundo"),
                  ("e neste aqui", "menos a do centro", "falha o terceiro")]
        for i, (g1, g2, g3) in enumerate(etapas):
            p, c, extra, txs = cartao(i)
            self.gat(g1)
            self.play(Create(p), cresce_campo(c, 0.9), run_time=1.0)
            self.gat(g2)
            self.play(FadeIn(extra), run_time=0.7)
            self.gat(g3)
            self.play(FadeIn(txs, shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)

        # ── B3-3 · por componentes ──
        self.an("B3-3")
        cc = leg_mix(["CONTÍNUA", r"$\Leftrightarrow$", "CADA COMPONENTE É CONTÍNUA"], 960, 1012, GEO, "center", 28, up=True)
        self.gat("e de novo por componentes")
        self.play(FadeIn(cc, shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)
        self.sai_fim()
