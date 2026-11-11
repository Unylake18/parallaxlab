"""v4: fundo violeta + grade do eixo; cartões a 60 px/u com rede de passo 1. Lote PB3 · CONTINUIDADE (v3; alvos 11, 12 e 13). B3-1 (chapas B): o desafio do B1 com δ = 0,41 e ε = 1, P CHEIO e L⃗ = F⃗(P); os três
pedaços no alto (y = 150, com placa). B3-2 (cartões C nas linhas grossas, centros 360 | 960 | 1560): os cartões entram em "três jeitos de dar
errado", e o que quebra cada pedaço entra na sua palavra. B3-3 (novo, página limpa): por componentes; constante + senos; o quociente da carga."""
from v28 import *  # noqa: F401,F403
from sec_b1 import ANG, nomes_b

VE, VD = VB(LAY_BE, 480, 540, 140), VB(LAY_BD, 1250, 560, 140)
CX = [360, 960, 1560]


def circ_n(n, cor=CAMPO2, size=30):
    return num_circ(n, cor, size)


def pedacos():
    gs = [leg_mix([circ_n(1), "P NO DOMÍNIO", r"$\checkmark$"], 960, 150, CAMPO2, "left", 30, up=False, gap=10),
          leg_mix([circ_n(2), "O LIMITE EXISTE", r"$\checkmark$"], 960, 150, CAMPO2, "left", 30, up=False, gap=10),
          leg_mix([circ_n(3), "LIMITE = F(P)", r"$\checkmark$"], 960, 150, CAMPO2, "left", 30, up=False, gap=10)]
    tot = sum(g.width for g in gs) + 2 * 62 / 120
    x = -tot / 2
    for g in gs:
        g.shift(RIGHT * (x - g.get_left()[0]))
        x += g.width + 62 / 120
    return gs


CART = [(1, "FORA DO DOMÍNIO", ["F(P) NEM EXISTE"]), (2, "SEM LIMITE", ["F(P) EXISTE, O LIMITE NÃO"]),
        (3, "SALTO NO PONTO", ["O LIMITE EXISTE, MAS", r"$\neq$", "F(P)"])]


def cartao(i):
    n, t1, t2 = CART[i]
    cx = CX[i]
    v = VB(LAY_C[i], cx, 540, 56)                  # v4: 60 px/u, quadradinho de 30 px (passo 0,5)
    p = painel(cx - 240, 250, 480, 460, v=v)
    partes = []
    if i == 0:
        cmp = campo28(v, F_CARGA, -3, 3, -3, 3, 1.0, rmin=1.1, mmax=1, nome="B3 ① carga")
        partes.append(VGroup(preenche(v, circ_pts(.7), ESC, 1, 6), vcirc(v, .7, GEO, 3, dash=(7, 7)).set_z_index(6.5), preenche(v, circ_pts(.42), CARGA, 1, 7),
                             T("+", *canto_xy(v, 0, -.28), 34, "center")))
    elif i == 1:
        cmp = campo28(v, F_DIAG, -3, 3, -3, 3, 1.0, rmin=.3, prop=True, skip=clar28([(-.2, -1.9, 3.1, -.95)]), nome="B3 ② G")
        partes.append(VGroup(ponto7(v.c2p(0, 0), POS, 8), TP(r"\G(0,0) = \vec 0", *canto_xy(v, 1.45, -1.4), 30)))
    else:
        cmp = campo28(v, lambda X, Y: (1.0, 0.0), -3, 3, -3, 3, 1.0, rmin=0, mmax=1, skip=clar28([(-1.9, -.6, 1.9, 2.4)], [(0, 0, .6)]), nome="B3 ③ salto")
        partes.append(VGroup(vlinha(v, [(0, 0), (1.6, 0)], GEO, 3, dash=(7, 7)), seta7(v.c2p(1.3, 0), v.c2p(1.62, 0), GEO, 3, 14),
                             ponto7(v.c2p(0, 0), POS, 8, 10), TP(r"\Lv", *canto_xy(v, 1.2, .45), 28)))
        partes.append(VGroup(seta7(v.c2p(0, 0), v.c2p(0, 1.6), CAMPO2, 7, 20).set_z_index(9), TP(r"\F(\Pt)", *canto_xy(v, -.95, 1.25), 28)))
    tit = leg_mix([circ_n(n, WHITE_, 32), t1], cx, 835, WHITE_, "center", 32, up=False, bold=True, gap=8)
    leg = leg_mix(t2, cx, 880, GEO, "center", 26, up=False, gap=6)
    p._v = v
    return p, cmp, partes, VGroup(tit, leg)


# ── final §2.5 (M3): caminhantes. Um ponto X (laranja, raio 8) anda até perto do ponto especial por uma trilha tracejada curta (GEO), que some no
#    fim; a seta de X fica em destaque (traço 9, #8CFFD2) e as setas de campo na vizinhança dela saem (clareira viva). ──
def seta_carga(X):
    r = math.hypot(*X)
    L = min(6.0 / (r * r), 1.6)                       # ∝ 1/r², com teto que cabe no cartão
    return (-X[0] / r * -L, -X[1] / r * -L)


def seta_diag(X):
    g = F_DIAG(*X)[0]
    return None if abs(g) < .05 else (g * 1.0, 0.0)


def caminha(cena, v, cmp, a, b, rt, fvec, fica=True, nome=""):
    """X anda de `a` até `b` (unidades do cartão) em `rt` s; a seta de X = fvec(X) (vetor no plano) ou None. Devolve (X, seta) se `fica`."""
    st = {"X": a}
    X = ponto7(v.c2p(*a), POS, 8, 12)

    def seta_de(P):
        u = fvec(P)
        if u is None:
            m = VMobject()
            m._sem_contorno = True
            return m
        return seta7(v.c2p(*P), v.c2p(P[0] + u[0], P[1] + u[1]), CAMPO2, 9, 28).set_z_index(11)

    def trilha(P):
        if math.hypot(P[0] - a[0], P[1] - a[1]) < .15:
            m = VMobject()
            m._sem_contorno = True
            return m
        return vlinha(v, [a, P], GEO, 3, dash=(7, 7)).set_z_index(5)
    sx, tr = seta_de(a), trilha(a)
    sx.add_updater(lambda m: m.become(seta_de(st["X"])))
    tr.add_updater(lambda m: m.become(trilha(st["X"])))
    X.add_updater(lambda m: m.move_to(v.c2p(*st["X"])))

    def clar():
        P = st["X"]
        u = fvec(P) or (0.0, 0.0)
        return ou(lambda x, y: math.hypot(x - P[0], y - P[1]) < .55, clarSeg([(P, (P[0] + u[0], P[1] + u[1]))], .5))
    cl = clareira(cmp, clar)
    cena.add(tr)
    cena.play(FadeIn(X, scale=0.5), FadeIn(sx), run_time=0.25)
    cena.play(UpdateFromAlphaFunc(X, lambda m, al: st.update(X=(a[0] + (b[0] - a[0]) * smooth(al), a[1] + (b[1] - a[1]) * smooth(al)))), run_time=rt)
    for m in (X, sx, tr):
        m.clear_updaters()
    u = fvec(b)
    print(f"[M3] {nome}: X de {a} a {b} em {rt:.1f} s; seta de X no fim = {u}")
    if fica:
        cena.play(FadeOut(tr), run_time=0.25)
        cena.remove(tr)
        return X, sx, cl
    cena.play(FadeOut(tr), FadeOut(X), FadeOut(sx), run_time=0.25)
    cena.remove(tr, X, sx)
    cmp.remove_updater(cl)
    return None


class LoteB3(Base):
    ANTES = "QUANDO O LIMITE NÃO EXISTE"

    def corpo(self):
        # ── B3-1 · três pedaços; o desafio com o ε em F(P) (alvo 11) ──
        self.an("B3-1")
        self.secao("CONTINUIDADE")
        d, ep = .41, 1.0
        zera_chapas()
        pE, pD = painel(130, 260, 700, 560, v=VE), painel(1090, 260, 700, 560, v=VD)
        zn = zona_px(120, 900, 1800, 1020, "linha de baixo B (B3)")
        Xa = (.62 * d * math.cos(ANG), .62 * d * math.sin(ANG))
        cmp = campo28(VE, F_AULA, -2.25, 2.25, -1.75, 1.75, .5, rmin=0, mmax=3.5, ctx=True,
                      skip=clar28([(-.85, -.5, -.45, .15), (Xa[0] - .2, Xa[1] + .15, Xa[0] + .4, Xa[1] + .62)], [(0, 0, d + .12)]), nome="B3-1 campo da aula (contexto)")
        nm = nomes_b()
        self.play(FadeIn(pE), FadeIn(zn), onda(cmp, 1.0), FadeIn(nm[0]), run_time=1.0)   # final M1: onda
        P = ponto7(VE.c2p(0, 0), POS, 9, 11)
        sP = seta7(VE.c2p(0, 0), VE.c2p(.42 * .8, 0), CAMPO2, 6, 18).set_z_index(10)
        lP = TP(r"\Pt", *canto_xy(VE, -.25, -.3), 36)
        pc = pedacos()
        plc = placa7(VGroup(*pc), 10, 6)
        self.gat("um o ponto está no domínio")
        self.play(FadeIn(P, scale=0.5), GrowArrow(sP), FadeIn(lP), FadeIn(plc), FadeIn(pc[0], shift=0.06 * DOWN), run_time=0.8)
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
        self.play(FadeIn(pD), FadeIn(nm[1]), FadeIn(org), GrowArrow(sL), FadeIn(lL), Create(cE), FadeIn(lE), FadeIn(dD), FadeIn(lD), run_time=1.0)
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

        # ── B3-2 · três jeitos de dar errado (alvo 12): os cartões entram juntos; o que quebra cada pedaço, na sua palavra ──
        self.an("B3-2")
        sai = [m for m in self.snap() if m is not dfn]
        zera_chapas()
        cards = [cartao(i) for i in range(3)]
        znC = zona_px(120, 780, 1800, 1020, "títulos C (B3)")
        self.gat("três jeitos de dar errado")
        self.play(*[FadeOut(m) for m in sai], FadeIn(znC), dfn.animate.move_to(PX(960, 962)), *[a for p, c, _, _ in cards for a in (FadeIn(p), cresce_campo(c, 0.9))], run_time=1.0)
        self.remove(*sai)
        # (v3, holds) cada peça na sua palavra: o que quebra; o título ("falha o …"); o subtítulo. final §2.5: os caminhantes (M3)
        etapas = [[("no campo elétrico de uma carga", 0), ("no campo elétrico de uma carga", "w"), ("falha o primeiro pedaço", "t"), ("em todo o resto ele é contínuo", "s")],
                  [("definido como zero na origem", 0), ("dependendo do caminho por onde você chega", "w"), ("falha o segundo", "t"), ("e neste aqui", "s")],
                  [("menos a do centro", 1), ("chegando de qualquer lado", "w"), ("o limite existe e é a seta para a direita", 0), ("a seta do ponto é outra", "s"),
                   ("falha o terceiro", "t")]]
        for k, ((p, c, partes, txs), passos) in enumerate(zip(cards, etapas)):
            v = p._v
            g0 = None
            for g, qual in passos:
                if g != g0:                     # o caminhante ① sai logo depois da carga, na mesma frase (sem 2º gatilho)
                    self.gat(g)
                g0 = g
                if qual == "w":
                    if k == 0:
                        caminha(self, v, c, (-3.1, 1.8), (-1.7, 1.0), 2.0, seta_carga, nome="① carga")
                    elif k == 1:
                        caminha(self, v, c, (-3.4, 0.0), (-0.9, 0.0), 1.1, seta_diag, fica=False, nome="② eixo horizontal")
                        caminha(self, v, c, (3.2, 3.2), (0.9, 0.9), 1.1, seta_diag, nome="② diagonal de subida")
                        caminha(self, v, c, (-3.2, 3.2), (-0.9, 0.9), 1.1, seta_diag, fica=False, nome="② outra diagonal")
                    else:
                        caminha(self, v, c, (-3.4, 0.0), (-1.45, 0.0), 1.6, lambda P: (0.95, 0.0), nome="③ salto")
                    continue
                m = txs[0] if qual == "t" else (txs[1] if qual == "s" else partes[qual])
                self.play(FadeIn(m, shift=0.04 * UP), run_time=0.6)
        self.ate(0.97)

        # ── B3-3 · por componentes (alvo 13, página limpa) ──
        self.an("B3-3")
        sai = self.snap()
        zP = grade_v(Vista(960, 540, 120), None, "B3-3 página (tela cheia, unidade padrão)")
        zera_chapas()
        l1 = TC(r"\F=(\Pp,\ \Qq)\ \text{contínuo}\iff \Pp\ \text{e}\ \Qq\ \text{contínuas}", 960, 270, 46, "c")
        self.gat("cada componente é contínua")
        self.play(AnimationGroup(*[FadeOut(m) for m in sai], FadeIn(zP), run_time=0.4), caneta(l1, ritmo=0.3))      # v4 R10
        self.remove(*sai)
        ops = leg_mix(["SOMA · PRODUTO · QUOCIENTE (DENOMINADOR", r"$\neq$", "0) · COMPOSIÇÃO"], 960, 880, CAMPO2, "center", 32, up=True, bold=True, gap=6)
        ops2 = legenda("DE FUNÇÕES CONTÍNUAS CONTINUAM CONTÍNUAS", 960, 935, GEO, "center", 28)
        self.gat("somas produtos quocientes")
        self.play(FadeIn(ops, shift=0.06 * UP), run_time=0.6)
        self.gat("e composições de funções contínuas")
        self.play(FadeIn(ops2, shift=0.06 * UP), run_time=0.5)
        ub = lambda a, b: r"\underbrace{" + a + r"}_{\textcolor{cg}{\text{" + b + "}}}"
        l2 = TC(r"\Pp=" + ub("1", "constante") + "+" + ub(r"\sen\X", "composição") + "-" + ub(r"\sen\Y", "composição"), 960, 450, 48, "c")
        self.gat("uma constante mais senos")
        self.play(caneta(l2, ritmo=0.2))
        l3 = TC(r"\E=\left(\dfrac{\X}{(\X^2+\Y^2)^{3/2}},\ \dfrac{\Y}{(\X^2+\Y^2)^{3/2}}\right)", 960, 640, 44, "c")
        l4 = legenda("QUOCIENTE: CONTÍNUO ONDE O DENOMINADOR NÃO É ZERO, OU SEJA, FORA DA CARGA", 960, 740, GEO, "center", 26)
        self.gat("o campo da carga é um quociente")
        self.play(caneta(l3, ritmo=0.3))
        self.play(FadeIn(l4, shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)
        self.sai_fim()
