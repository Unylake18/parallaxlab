"""Lote PB2 · QUANDO O LIMITE NÃO EXISTE (layout A; alvo 04). Campo G = (2xy/(x² + y²), 0) com setas PROPORCIONAIS (nada sobre os eixos).
Três caminhos GEO tracejados, um por vez, cada um com a sua clareira; o ponto laranja anda UMA vez carregando a sua seta (0⃗, (1, 0), (−1, 0))."""
from v28 import *  # noqa: F401,F403

V = Vista(600, 540, 120)
PONTOS = [(1.25, 0.0), (1.1, 1.1), (-1.1, 1.1)]
INICIOS = [(2.8, 0.0), (2.55, 2.55), (-2.55, 2.55)]
SEGS = [((3, 0), (.3, 0)), ((2.7, 2.7), (.22, .22)), ((-2.7, 2.7), (-.22, .22))]
RET_LBL = [(1.0, -.75, 2.0, -.3), (1.3, 1.25, 2.6, 1.75), (-2.6, 1.25, -1.3, 1.75)]
LBL = [(r"\vec 0", (1.5, -.5)), (r"(1,\ 0)", (1.95, 1.5)), (r"(-1,\ 0)", (-1.95, 1.5))]


def seta_g(p):
    g = F_DIAG(*p)
    if math.hypot(*g) < 1e-9:
        return None
    return seta7(V.c2p(p[0] - .1, p[1]), V.c2p(p[0] - .1 + g[0] * .42 * 1.15, p[1]), CAMPO2, 8, 24).set_z_index(9)


class LoteB2(Base):
    ANTES = "CHEGAR PERTO"

    def corpo(self):
        # ── B2-1 ──
        self.an("B2-1")
        self.secao("QUANDO O LIMITE NÃO EXISTE")
        cmp = campo28(V, F_DIAG, prop=True, rmin=.3, nome="B2 campo das diagonais (proporcional)")
        o = ponto7(V.c2p(0, 0), GEO, 5)
        ativos = []                                   # testes de clareira dos caminhos já desenhados
        st = {"p": None}
        clareira(cmp, lambda: ou(*ativos, (clar28([], [(*st["p"], .15)]) if st["p"] else None)))
        self.play(cresce_campo(cmp, 1.0), FadeIn(o), run_time=1.0)
        fG = TC(r"\G = \left(\dfrac{2\X\Y}{\X^2+\Y^2},\ 0\right)", 1120, 320, 48)
        self.gat("campo encrenqueiro")
        self.play(caneta(fG))
        self.ate(0.97)

        # ── B2-2 · três caminhos ──
        self.an("B2-2")
        frases = ["pelo eixo horizontal", "pela diagonal de subida", "pela outra diagonal"]
        for i, fr in enumerate(frases):
            cam = vlinha(V, list(SEGS[i]), GEO, 3, dash=(10, 9))
            a, b = np.array(INICIOS[i]), np.array(PONTOS[i])
            pt = ponto7(V.c2p(*a), POS, 9, 10)
            st["p"] = tuple(a)
            sg = seta_g(tuple(a))
            self.gat(fr)
            ativos.append(clarSeg([SEGS[i]], .2))
            self.play(Create(cam), FadeIn(pt, scale=0.5), *([GrowArrow(sg)] if sg else []), run_time=0.7)

            def anda_(m, al, a=a, b=b, sg=sg):
                p = a + (b - a) * smooth(al)
                st["p"] = (float(p[0]), float(p[1]))
                pt.move_to(V.c2p(*p))
                if sg is not None:
                    sg.become(seta_g(st["p"]))
            self.play(UpdateFromAlphaFunc(pt, anda_), run_time=2.2)
            ativos.append(clar28([RET_LBL[i]], [(*PONTOS[i], .15)]))
            st["p"] = None
            s, xy = LBL[i]
            self.play(FadeIn(TP(s, *canto_xy(V, *xy), 36)), run_time=0.5)
        print(f"[G] nas três retas: {[tuple(round(v, 3) for v in F_DIAG(*p)) for p in PONTOS]}")
        nr = legenda("NA RETA y = m x:", 1124, 450, GEO, up=False)
        fm = TC(r"\G = \left(\dfrac{2m}{1+m^2},\ 0\right)", 1120, 530, 48)
        self.gat("fazendo a conta")
        self.play(FadeIn(nr, shift=0.06 * UP), run_time=0.5)
        self.play(caneta(fm))
        ml = TC(r"m=0 \to 0\quad m=1 \to 1\quad m=-1 \to -1", 1120, 650, 40)
        self.gat("muda a reta")
        self.play(caneta(ml, ritmo=0.5))
        self.ate(0.97)

        # ── B2-3 ──
        self.an("B2-3")
        ne = VGroup(T("NÃO EXISTE O LIMITE", 1120, 780, 40, cor=BR), T("EM (0, 0)", 1120, 830, 40, cor=BR))
        self.gat("então não existe limite")
        self.play(FadeIn(ne, shift=0.08 * UP), run_time=0.6)
        self.ate(0.97)
        cmp.clear_updaters()
        self.sai_fim()
