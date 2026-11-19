"""Lote PD1 · D1 MESMA FÓRMULA, DOIS FILMES (alvos 04, 05, 06). Layout B (origens (408, 540) e (1260, 540), 144 px/u): reta (o eixo u acende e uma
cópia voa pelo mapa linear para a diagonal y = x), quadrado (cantos ①–④ voando na ordem da fala; lados, chapa e malha; ÁREA 1 → 2 · ESPELHADO; setas
curvas GEO ↺/↻ por 1,5 s), círculo (r → r√2; a conta expandida, os termos cruzados cancelam e o resto se junta por TransformByGlyphMap). Depois o
layout A com a rede de f₁ por colunas, os destaques dos eixos e a coluna da pergunta (GUARDA O PALPITE)."""
from lib30 import *  # noqa: F401,F403

VL = VB(BE, 408, 540, 140)
VR = VB(BD, 1260, 540, 140)
PHI = lambda u, v: (u + v, u - v)
CANTOS = [(0, 0), (1, 0), (1, 1), (0, 1)]
DL_ = [(-.3, -.3), (.3, -.3), (.3, .3), (-.3, .3)]
DR_ = [(-.35, 0), (0, .38), (.38, 0), (0, -.38)]


def eixos30(v, a, b, c, d, al=.55):
    return VGroup(vlinha(v, [(a, 0), (b, 0)], GEO, 2, alpha=al), vlinha(v, [(0, c), (0, d)], GEO, 2, alpha=al)).set_z_index(2)


def rotulo_n(n, v, p, d):
    g = num_circ(n, BR, 44)
    g.move_to(PX(*canto_xy(v, p[0] + d[0], p[1] + d[1])))
    return VGroup(placa7(g, 6, 4), g).set_z_index(26)


class LoteD1(Base):
    def corpo(self):
        # ── D1-1 · enunciado (layout B) ──
        self.an("D1-1")
        self.secao("MESMA FÓRMULA, DOIS FILMES")
        zera_chapas()
        pe, pd = chapa_px(*BE, nome="D1 painel esq.", v=VL), chapa_px(*BD, nome="D1 painel dir.", v=VR)
        ee, ed = eixos30(VL, -1.8, 2.8, -2.4, 2.4), eixos30(VR, -1.1, 3.6, -2.4, 2.4)
        troca(self, "A → D1 (layout B; entra o canto)")
        self.play(FadeIn(pe), FadeIn(pd), Create(ee), Create(ed), run_time=0.8)
        phi = TC(r"\varphi(\Uu,\Vv)=(\Uu+\Vv,\ \Uu-\Vv)", 600, 962, 40, "c")
        self.gat("na primeira coordenada")
        self.play(caneta(phi, ritmo=0.3))
        n1 = legenda("ONDE VOCÊ ESTÁ (u, v)", 480, 868, GEO, "center", 28, up=False)
        n2 = legenda("ONDE VAI PARAR (x, y)", 1440, 868, GEO, "center", 28, up=False)
        self.gat("no plano da esquerda")
        self.play(FadeIn(n1, shift=0.05 * UP), run_time=0.4)
        self.gat("no da direita")
        self.play(FadeIn(n2, shift=0.05 * UP), run_time=0.4)
        itens = legenda("RETA · QUADRADO · CÍRCULO", 1440, 962, GEO, "center", 32)
        self.gat("três itens")
        self.play(FadeIn(itens, shift=0.05 * UP), run_time=0.4)
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.ate(1.0)

        # ── D1-2 · a reta ──
        self.an("D1-2")
        eu = vlinha(VL, [(-1.6, 0), (2.6, 0)], AMB, 5).set_z_index(6)
        self.gat("o eixo horizontal da esquerda")
        self.play(Create(eu), run_time=0.7)
        v0 = TP(r"\Vv = 0", *canto_xy(VL, 2.1, .35), 32)
        self.gat("onde o segundo número é zero")
        self.play(FadeIn(v0), run_time=0.4)
        seg = vlinha(VL, [(-1, 0), (2.3, 0)], AMB, 5).set_z_index(6)          # o trecho que cabe no painel da direita depois do mapa
        diag = vlinha(VR, [(-1, -1), (2.3, 2.3)], AMB, 5).set_z_index(6)
        yx = TP(r"\Y = \X", *canto_xy(VR, 2.55, 1.95), 32)
        self.gat("o eixo vai parar na diagonal")
        self.play(TransformFromCopy(seg, diag), run_time=1.2)
        self.play(FadeIn(yx), run_time=0.4)
        self.ate(1.0)

        # ── D1-3 · o quadrado (alvo 04) ──
        self.an("D1-3")
        qe = Pedaco(VL, CANTOS, n=4, k=30)
        pts_e = [ponto7(VL.c2p(*p), POS, 8, 12) for p in CANTOS]
        nums_e = [rotulo_n(i + 1, VL, p, d) for i, (p, d) in enumerate(zip(CANTOS, DL_))]
        self.gat("agora o quadrado de lado um")
        self.play(FadeIn(qe), LaggedStart(*[FadeIn(VGroup(a, b)) for a, b in zip(pts_e, nums_e)], lag_ratio=0.25), run_time=1.0)
        IM = [PHI(*p) for p in CANTOS]
        pts_d = [ponto7(VR.c2p(*p), POS, 8, 12) for p in IM]
        nums_d = [rotulo_n(i + 1, VR, p, d) for i, (p, d) in enumerate(zip(IM, DR_))]
        for i, fr in enumerate(("a origem fica parada", "o canto um zero vai para", "o canto um um vai para", "e o canto zero um vai para")):
            self.gat(fr)
            self.play(TransformFromCopy(VGroup(pts_e[i], nums_e[i]), VGroup(pts_d[i], nums_d[i])), run_time=0.9)
            print(f"[D1] canto {i + 1}: {CANTOS[i]} → {IM[i]}")
        qd = Pedaco(VR, IM, n=4, k=30)
        lados = vlinha(VR, IM + [IM[0]], CORAL, 4).set_z_index(9)
        self.gat("liga os pontos")
        self.play(Create(lados), run_time=0.8)
        self.play(FadeIn(qd), run_time=0.5)
        self.remove(lados)
        print(f"[D1] área do quadrado: {qe.area():.3f} → {qd.area():.3f} (lado {math.hypot(1, 1):.4f})")
        ar = T("ÁREA 1 → 2 · ESPELHADO", 1440, 962, 32, "center", CORAL)
        self.gat("a área era um")
        troca_linha(self, itens, ar)
        ge = giro30(VL, (.5, .5), .3, True, GEO, 3, 14, a0=-.6, a1=PI * 1.15)
        gd = giro30(VR, (1, 0), .42, False, GEO, 3, 14, a0=PI * 1.15, a1=-.6)
        self.gat("olha a ordem dos cantos")
        self.play(Create(ge), Create(gd), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(ge), FadeOut(gd), run_time=0.4)
        self.remove(ge, gd)
        self.ate(1.0)

        # ── D1-4 · o círculo (alvo 05) ──
        self.an("D1-4")
        ang = .6
        ce = VGroup(vcirc(VL, 1, CORAL, 4).set_z_index(6), ponto7(VL.c2p(0, 0), GEO, 6, 8),
                    seta7(VL.c2p(0, 0), VL.c2p(math.cos(ang), math.sin(ang)), GEO, 3, 14).set_z_index(8))
        cd = VGroup(vcirc(VR, SQ2, CORAL, 4).set_z_index(6), ponto7(VR.c2p(0, 0), GEO, 6, 8),
                    seta7(VR.c2p(0, 0), VR.c2p(SQ2 * math.cos(ang), SQ2 * math.sin(ang)), GEO, 3, 14).set_z_index(8))
        lr = TP(r"r", *canto_xy(VL, .25, .45), 32)
        lr2 = TP(r"r\sqrt2", *canto_xy(VR, .2, .75), 32)
        sai = [qe, qd, *pts_e, *nums_e, *pts_d, *nums_d, phi, ar, eu, v0, diag, yx]
        self.gat("e um círculo em volta da origem")
        self.play(*[FadeOut(m) for m in sai], Create(ce[0]), FadeIn(ce[1]), GrowArrow(ce[2]), FadeIn(lr), run_time=0.8)
        self.remove(*sai)
        P0 = [r"(\Uu+\Vv)^2", "+", r"(\Uu-\Vv)^2", "="]
        A = Pz(P0 + [r"\Uu^2", "+", r"2\Uu\Vv", "+", r"\Vv^2", "+", r"\Uu^2", "-", r"2\Uu\Vv", "+", r"\Vv^2"], 960, 962, 42, "c", caneta=False)
        C = Pz(P0 + [r"\Uu^2", "+", r"\Vv^2", "+", r"\Uu^2", "+", r"\Vv^2"], 960, 962, 42, "c", caneta=False)
        B = Pz(P0 + ["2", "(", r"\Uu^2", "+", r"\Vv^2", ")"], 960, 962, 42, "c", caneta=False)
        g0 = VGroup(*[A[0][i] for r_ in A._rg[:3] for i in r_])
        g1 = VGroup(*[A[0][i] for r_ in A._rg[3:] for i in r_])
        self.gat("soma ao quadrado mais diferença")
        self.play(caneta(g0, ritmo=0.3))
        self.play(caneta(g1, ritmo=0.25))
        self.remove(g0, g1)
        self.add(A)
        self.gat("os termos cruzados se cancelam")
        self.play(tbgm30(A, C, [(i, i) for i in range(4)] + [(4, 4), (7, 5), (8, 6), (9, 7), (10, 8), (13, 9), (14, 10)], rt=1.2))
        self.remove(A)
        limpa_soltos(self)
        self.add(C)
        self.gat("e sobra duas vezes")
        self.play(tbgm30(C, B, [(i, i) for i in range(4)] + [([4, 8], 6), (5, 7), ([6, 10], 8)], rt=1.2))
        self.remove(C)
        limpa_soltos(self)
        self.add(B)
        self.gat("e o círculo vira um círculo")
        self.play(TransformFromCopy(ce, cd), run_time=1.2)
        self.play(FadeIn(lr2), run_time=0.4)
        self.ate(1.0)

        # ── D1-5 · como campo (layout A, alvo 06) ──
        self.an("D1-5")
        zera_chapas()
        chA = chapa_px(*LA, nome="D1 palco A", v=VA)
        cmp = campo30(VA, F1, rmin=0, mmax=5, skip=clar28([(-.25, -.25, .25, .25)]), nome="D1 f₁ (campo)")
        p0 = ponto7(VA.c2p(0, 0), GEO, 6, 8)
        fF = TC(r"\F(\X,\Y)=(\X+\Y,\ \X-\Y)", 1120, 330, 46)
        lg = legenda("A MESMA FÓRMULA, AGORA COMO CAMPO", 1124, 420, GEO)
        self.gat("agora a mesma fórmula")
        self.limpa_junto()
        troca(self, "D1 layout B → layout A")
        self.play(FadeIn(chA), FadeIn(p0), caneta(fF, ritmo=0.3), run_time=1.0)
        self.play(FadeIn(lg, shift=0.05 * UP), run_time=0.4)
        self.gat("você pendura a seta")
        self.play(por_colunas(cmp, 1.0))
        for fr, sel in (("no eixo horizontal à direita", lambda s: abs(s._xy[1]) < 1e-6 and s._xy[0] > 0),
                        ("no eixo vertical em cima", lambda s: abs(s._xy[0]) < 1e-6)):
            self.gat(fr)
            self.play(recolore(self, cmp, lambda s, sel=sel: not sel(s)), run_time=0.4)
            self.wait(2.0)
            self.play(recolore(self, cmp, lambda s: False), run_time=0.4)
        self.ate(1.0)

        # ── D1-6 · a pergunta guardada ──
        self.an("D1-6")
        ct1, ct2 = T("COMO TRANSFORMAÇÃO:", 1120, 540, 34), T("ÁREA × 2", 1120, 595, 40, cor=CORAL)
        cc1, cc2 = T("COMO CAMPO:", 1120, 700, 34), T("A ÁREA TAMBÉM DOBRA?", 1120, 755, 40, cor=SAIC)
        gp = legenda("GUARDA O PALPITE", 1124, 820, GEO)
        self.gat("como transformação a área dobrou")
        self.play(FadeIn(ct1, shift=0.05 * UP), FadeIn(ct2, shift=0.05 * UP), run_time=0.5)
        self.gat("como campo se a gente soltar")
        self.play(FadeIn(cc1, shift=0.05 * UP), run_time=0.4)
        self.gat("a área dele também dobra")
        self.play(FadeIn(cc2, shift=0.05 * UP), run_time=0.4)
        self.gat("guarda o seu palpite")
        self.play(FadeIn(gp, shift=0.05 * UP), run_time=0.4)
        self.sai_fim()
