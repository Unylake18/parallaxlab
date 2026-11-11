"""Lote PB4 · DIVERGENTE (handoff v2; quadros 11 a 14). Layout A. B4-1/2: explosão (x, y), o quadrado (lado 0,7 em (1,25; 0,85)) pelo fluxo exato
t 0 → 0,35 UMA vez com o fantasma; ÁREA 0,49 → 0,99; div F e 1 + 1 = 2. B4-3/4: campo em contexto, a caixa [0,5; 2]², as setas das paredes (só a componente
normal; escala 0,45), h, k, x0, x0 + h com placa; três linhas. B4-5: fonte-anel, os quadrados aninhados 1, ½, ¼, ⅛ em (1, ½) um por frase com a tabela;
div = 2 − x² − y² → 2 − 1 − ¼ = 0,750 (TransformByGlyphMap). B4-6: luz e sombra, círculo de div 0, um quadrado cresce e outro encolhe (uma vez)."""
from MF_Tools import TransformByGlyphMap

from v27 import *  # noqa: F401,F403

V = Vista(600, 540, 120)


def lbl(s, X, Y, size=40, al="c"):
    x, y = canto_xy(V, X, Y)
    return TP(s, x, y, size, al)


def saldo_caixa(Ff, x0, y0, h, n=2000):
    u = (np.arange(n) + 0.5) / n * h - h / 2
    d = np.mean(Ff(x0 + h / 2 + 0 * u, y0 + u)[0]) * h - np.mean(Ff(x0 - h / 2 + 0 * u, y0 + u)[0]) * h
    c = np.mean(Ff(x0 + u, y0 + h / 2 + 0 * u)[1]) * h - np.mean(Ff(x0 + u, y0 - h / 2 + 0 * u)[1]) * h
    return (d + c) / (h * h)


class LoteB4(Base):
    ANTES = "DOIS ENGANOS"
    def corpo(self):
        # ── B4-1 ──
        self.an("B4-1")
        self.secao("DIVERGENTE")
        ce = campo7(V, F_EXPL, mmax=3.0, nome="B4 explosão")
        self.play(cresce_campo(ce, 1.6))
        c0, s0 = (1.25, 0.85), 0.7
        fant = contorno_ini(V, [(c0[0] - s0 / 2, c0[1] - s0 / 2), (c0[0] + s0 / 2, c0[1] - s0 / 2), (c0[0] + s0 / 2, c0[1] + s0 / 2), (c0[0] - s0 / 2, c0[1] + s0 / 2)])
        q = Pedaco(V, uv_quad(c0, s0), fl_expl)                                # v4 §4: chapa com malha 4×4 levada pelo fluxo
        xa, ya = canto_xy(V, 1.0, 2.1)
        ar_t = legenda("ÁREA:", xa, ya, CORAL, size=30)
        ar_n = NumBR(s0 * s0, num_decimal_places=2, font_size=fs(30), color=CORAL).next_to(ar_t, RIGHT, buff=0.12).align_to(ar_t, DOWN)
        for m_ in ar_n.get_family():
            m_._sem_contorno = True
        ar_f = legenda("ÁREA: 0,49 → 0,99", 1124, 780, CORAL)                  # alvo 12: o resultado vai para a coluna
        pl_a = placa7(VGroup(ar_t, ar_n).copy().stretch(1.9, 0, about_edge=LEFT), 8, 5)
        cl1 = esconde(ce, clar([(0.65, 0.25, 2.55, 1.95), (0.75, 1.9, 2.95, 2.35)]))
        self.gat("aqui o quadradinho não gira")
        self.play(some(cl1), FadeIn(q, scale=0.7), FadeIn(fant), FadeIn(pl_a), FadeIn(ar_t), FadeIn(ar_n), run_time=0.6)
        self.gat("ele cresce")
        A0 = s0 * s0
        self.play(*corre(self, [q], 0.35, 3.0), UpdateFromAlphaFunc(ar_n, lambda m_, a: m_.set_value(A0 * math.exp(2 * 0.35 * a))), run_time=3.0)
        self.play(FadeOut(ar_n), FadeOut(ar_t), FadeOut(pl_a), FadeIn(ar_f), run_time=0.4)
        self.remove(ar_n, ar_t)
        print(f"[área] B4-1: área {A0:.3f} → {A0 * math.exp(0.7):.3f} (exata: A0·e^(2t), t = 0,35)")
        self.ate(0.97)

        # ── B4-2 ──
        self.an("B4-2")
        fD = TC(r"\dv \F = \dfrac{\partial \Pp}{\dx} + \dfrac{\partial \Qq}{\dy}", 1120, 360, 56)
        self.gat("o divergente mede exatamente isso")
        self.play(caneta(fD))
        num = legenda("É UM NÚMERO", 1124, 470)
        self.gat("o resultado é um número")
        self.play(FadeIn(num, shift=0.1 * UP), run_time=0.5)
        fE = TC(r"\F = (\X,\ \Y)", 1120, 580, 48)
        f2 = TC(r"\dv \F = 1 + 1 = \D{2}", 1120, 680, 52)
        self.gat("na explosão o divergente vale dois")
        self.play(caneta(fE))
        self.play(caneta(f2))
        self.ate(0.97)

        # ── B4-3 · a caixa parada ──
        self.an("B4-3")
        sai = [q, fant, ar_f, fD, num, fE, f2]
        self.play(*[FadeOut(m_) for m_ in sai], UpdateFromAlphaFunc(ce, lambda m_, a: m_.contexto(a > 0.5)), volta(cl1), run_time=0.6)
        self.remove(*sai)
        x0, x1, y0, y1 = 0.5, 2.0, 0.5, 2.0
        cx = VGroup(preenche(V, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], CHAPA, 0.55, 4), vlinha(V, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], GEO, 3))
        cl2 = esconde(ce, clar([(0.0, 0.0, 3.3, 2.3), (0.0, 0.0, 2.3, 3.3)], [(0.5, -0.22), (2.0, -0.22), (-0.05, 1.25), (1.25, 0.02)], 0.4))   # final §2.4
        self.gat("uma caixa parada")
        self.play(some(cl2), FadeIn(cx), run_time=0.7)
        se = T("SAI − ENTRA", 1120, 250, 34, "left", SAI)
        self.gat("sai mais fluido do que entra")
        self.play(FadeIn(se, shift=0.1 * DOWN), run_time=0.5)
        self.ate(0.97)

        # ── B4-4 · as paredes ──
        self.an("B4-4")
        s = 0.6               # final §2.4: comprimento = s·(componente na parede): sai 2 → 1,2 u; entra 0,5 → 0,3 u (4× menor, legível)
        dirS = VGroup(*[seta7(V.c2p(x1, Y), V.c2p(x1 + s * x1, Y), CAMPO2, 6, 22) for Y in (0.8, 1.25, 1.7)])
        esqS = VGroup(*[seta7(V.c2p(x0 - s * x0, Y), V.c2p(x0, Y), CAMPO2, 6, 15) for Y in (0.8, 1.25, 1.7)])
        cimS = VGroup(*[seta7(V.c2p(X, y1), V.c2p(X, y1 + s * y1), CAMPO2, 6, 22) for X in (0.8, 1.25, 1.7)])
        baiS = VGroup(*[seta7(V.c2p(X, y0 - s * y0), V.c2p(X, y0), CAMPO2, 6, 15) for X in (0.8, 1.25, 1.7)])
        print(f"[caixa] B4-4: entra {s * x0 * V.u:.0f} px (P = {x0}), sai {s * x1 * V.u:.0f} px (P = {x1})")
        for g in (dirS, esqS, cimS, baiS):
            g.set_z_index(10)
        self.gat("pela parede da direita")
        self.play(LaggedStart(*[GrowArrow(a) for a in dirS], lag_ratio=0.2), run_time=0.8)
        self.gat("pela da esquerda")
        self.play(LaggedStart(*[GrowArrow(a) for a in esqS], lag_ratio=0.2), run_time=0.8)
        lh, lk = lbl(r"\h", 1.25, 0.02), lbl(r"\k", -0.05, 1.25)
        lx0, lx1 = lbl(r"\xo", 0.5, -0.22, 34), lbl(r"\xo+\h", 2.0, -0.22, 34)
        L1 = TC(r"[\Pp(\xo+\h) - \Pp(\xo)]\,\k \approx \dfrac{\partial \Pp}{\dx}\,\h\k", 1120, 360, 42)
        self.gat("a diferença vezes a altura")
        self.play(FadeIn(lh), FadeIn(lk), FadeIn(lx0), FadeIn(lx1), run_time=0.5)
        self.play(caneta(L1))
        L2 = TC(r"[\Qq(\yo+\k) - \Qq(\yo)]\,\h \approx \dfrac{\partial \Qq}{\dy}\,\h\k", 1120, 500, 42)
        self.gat("em cima e embaixo")
        self.play(LaggedStart(*[GrowArrow(a) for a in [*cimS, *baiS]], lag_ratio=0.12), run_time=0.9)
        self.play(caneta(L2, ritmo=0.67))                                          # final: no piso, para a 3ª linha ficar inteira na tela
        L3 = TC(r"\dfrac{\D{\text{saldo}}}{\h\k} \;\longrightarrow\; \dfrac{\partial \Pp}{\dx} + \dfrac{\partial \Qq}{\dy} = \dv\F", 1120, 660, 46)
        self.play(caneta(L3, ritmo=0.8), self.em("somando e dividindo pela área", pulso(cx, 1.04, run_time=0.6)))   # final: L3 logo depois da L2
        self.ate(0.97)

        # ── B4-5 · a caixa que encolhe ──
        self.an("B4-5")
        self.limpa_junto(rt=0.5)
        ca = campo7(V, F_ANEL, mmax=1.1, nome="B4-5 fonte-anel")
        fF = TC(r"\F = \left(\X - \dfrac{\X^3}{3},\ \Y - \dfrac{\Y^3}{3}\right)", 1120, 250, 44)
        self.gat("vamos testar num campo de verdade")
        self.play(cresce_campo(ca, 1.4))
        self.play(caneta(fF))
        c = (1.0, 0.5)
        hd = VGroup(legenda("LADO", 1150, 355, GEO), legenda("SALDO ÷ ÁREA", 1400, 355, SAI))
        linhas = [("1", "0{,}583", 1.0), (r"\tfrac12", "0{,}708", 0.5), (r"\tfrac14", "0{,}740", 0.25), (r"\tfrac18", "0{,}747", 0.125)]
        for i, (l_, v_, h_) in enumerate(linhas):
            calc = saldo_caixa(F_ANEL, *c, h_)
            print(f"[caixa] B4-5 lado {h_}: saldo/área numérico {calc:.5f}; fórmula {2 - 1 - 0.25 - h_ ** 2 / 6:.5f}; na tela {v_}")
        frases = ("calcula o que sai menos o que entra", "encolhe a caixa pela metade", "e de novo zero vírgula setenta e quatro", "e de novo zero vírgula setenta e cinco")
        pc = ponto7(V.c2p(*c), CORAL, 5, 9)
        cl3 = esconde(ca, clar([(0.35, -0.15, 1.65, 1.15)]))
        for i, ((l_, v_, h_), fr) in enumerate(zip(linhas, frases)):
            self.gat(fr)
            qd = quadrado(V, c, h_, CORAL if i == 3 else GEO, dash=(7, 7) if i else None, fill=None if i else CHAPA, w=2.5 if i else 3.5, alpha=0.55)
            tl, tv = TC(l_, 1180, 420 + i * 70, 40, "c"), TC(r"\D{" + v_ + "}", 1400, 420 + i * 70, 40)
            extra = [FadeIn(hd), FadeIn(pc), some(cl3)] if i == 0 else []
            self.play(Create(qd), *extra, run_time=0.6)
            self.play(caneta(tl), caneta(tv, atraso=0.2))
        seta_b = TC(r"\downarrow", 1440, 700, 40, "c")
        D1 = TC(r"\dv \F = 2 - \X^2 - \Y^2", 1120, 790, 46)
        D2 = TC(r"\dv \F\left(1,\tfrac12\right) = 2 - 1 - \tfrac14 = \D{0{,}750}", 1120, 890, 46)
        self.play(caneta(seta_b), caneta(D1, atraso=0.2))                       # final: a forma geral logo depois da última linha
        self.gat("três quartos é exatamente o divergente")
        self.play(caneta(D2))
        self.ate(0.97)

        # ── B4-6 · o mapa ──
        self.an("B4-6")
        self.limpa_junto(ca, *ca.submobjects, rt=0.5)              # final: as setas do campo estão soltas na cena; ficam todas
        r0 = math.sqrt(2)
        som = preenche(V, circ_pts(3.05), ESC, 0.55, 0.5)
        luz = preenche(V, circ_pts(r0), SAI, 0.22, 0.6)
        fd = TC(r"\dv \F = 2 - \X^2 - \Y^2", 1120, 330, 52)
        cl4 = esconde(ca, clar([(1.4, 1.15, 3.0, 1.75), (-0.15, -0.2, 1.05, 0.95), (1.55, -1.75, 2.55, -0.75)], [(-0.55, -0.75), (-2.1, -1.95)], 0.4))
        mais = T("+", *canto_xy(V, -0.55, -0.75), 90, "center", SAI)
        menos = T("−", *canto_xy(V, -2.1, -1.95), 90, "center", GEO)
        g1 = contorno_ini(V, [(0.1, 0.05), (0.6, 0.05), (0.6, 0.55), (0.1, 0.55)])
        g2 = contorno_ini(V, [(1.8, -1.5), (2.3, -1.5), (2.3, -1.0), (1.8, -1.0)])
        qi = Pedaco(V, uv_quad((0.35, 0.3), 0.5), fl_anel)
        qo = Pedaco(V, uv_quad((2.05, -1.25), 0.5), fl_anel)
        lmais = legenda("+  CADA PEDACINHO SE EXPANDE", 1124, 450, SAI)
        self.gat("pintar o plano inteiro")
        self.play(FadeIn(som), FadeIn(luz), UpdateFromAlphaFunc(ca, lambda m_, a: m_.contexto(a > 0.5)), volta(VGroup(*[s_ for s_ in cl3 if s_ not in cl4])),
                  some(VGroup(*[s_ for s_ in cl4 if s_ not in cl3])), caneta(fd),
                  self.em("dentro de um disco", self.surge(mais, lmais, qi, g1)))      # final: o + e o pedacinho de dentro entram na fala, durante a fórmula
        self.play(*corre(self, [qi], 0.28, 2.0))
        print(f"[área] B4-6 dentro: {area_poly(ret_pts((0.35, 0.3), 0.5)):.4f} → {area_poly(qi.XY):.4f}")
        self.gat("fora dele é negativo")
        self.play(FadeIn(menos), FadeIn(legenda("−  CADA PEDACINHO SE CONTRAI", 1124, 510, GEO)), FadeIn(qo), FadeIn(g2), run_time=0.6)
        self.play(*corre(self, [qo], 0.2, 2.0))
        print(f"[área] B4-6 fora: {area_poly(ret_pts((2.05, -1.25), 0.5)):.4f} → {area_poly(qo.XY):.4f}")
        zero = vcirc(V, r0, GEO, 3, dash=(10, 9))
        lz = lbl(r"\dv\F = 0", 1.55, 1.45, 38, "l")
        print(f"[mapa] B4-6: círculo de div 0 em r = √2 = {r0:.4f}")
        self.gat("um círculo inteiro de divergente zero")
        self.play(Create(zero), FadeIn(lz), run_time=0.9)
        self.gat("ninguém está criando nem destruindo")
        self.play(FadeIn(legenda("NINGUÉM CRIA NEM DESTRÓI FLUIDO", 1124, 600, BR)), run_time=0.5)
        self.gat("a água por exemplo")
        agua = legenda("ÁGUA:", 1124, 745, BR)                      # final §2.11: rótulo em Space Grotesk; v⃗ na cor do campo
        self.play(FadeIn(agua, shift=0.1 * UP), caneta(TC(r"\dv\textcolor{cc}{\vec v} \approx 0", agua.get_right()[0] * 120 + 960 + 16, 730, 44)))
        self.gat("bomba de bicicleta")
        self.play(caneta(TC(r"\text{ar comprimido na bomba: }\ \dv\vec v < 0", 1120, 830, 40)))
        self.ate(0.97)
        self.sai_fim()
