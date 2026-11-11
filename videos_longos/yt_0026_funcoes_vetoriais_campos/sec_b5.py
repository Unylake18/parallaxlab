"""Lote PB5 · CAMPO VETORIAL (B5-1…B5-4): layout A (quadro 14) e layout B (quadro 15). O ponto X e a seta que nasce nele; a forma geral P i + Q j; o campo constante j (vento uniforme);
o campo radial x i + y j (círculos tracejados, setas do mesmo tamanho em cada um); as duas perguntas (transformação × campo) em dois painéis. v9: miniatura 3×3 de transformação no B5-2 (colapso em (0, 1)) e no B5-3 (identidade)."""
from v7 import *  # noqa: F401,F403

V = Vista(600, 540, 96)       # v8: origem num cruzamento grosso, unidade 96 px (múltipla de 24)


def mini(cx, cy, u=48):
    """v9: miniatura da leitura como transformação: grade 3×3 de pontos GEO (sem partículas)."""
    vm = Vista(cx, cy, u)
    return vm, VGroup(*[ponto7(vm.c2p(i, j), GEO, 7) for j in (1, 0, -1) for i in (-1, 0, 1)])


def palco():
    g = VGroup(eixos7(V, -3.2, 3.2, -3.2, 3.2))
    return g


class LoteB5(Base):
    def corpo(self):
        set_dy(48)
        # ── B5-1 · um ponto X e o vetor de saída com o pé em X ──
        self.an("B5-1")
        self.secao("CAMPO VETORIAL")
        ax = palco()
        self.play(Create(ax), run_time=1.0)
        X = V.c2p(1.5, 1.0)
        dX = ponto7(X, POS7, 9)
        lX = TC(r"\P{X}", pxy(X)[0] - 22, pxy(X)[1] + 26, 40, "c", caneta=False, placa=True)
        self.gat("em vez de mandar o ponto")
        self.play(FadeIn(dX, scale=0.5), FadeIn(lX), run_time=0.5)
        fant = ponto7(V.c2p(-1.2, 2.4), SAI, 8)
        arc = voo(X + 0.1 * UL, fant.get_center() + 0.1 * DR, angle=0.8, w=2.2, tip=0.15)
        self.play(Create(arc), FadeIn(fant), run_time=0.9)
        self.play(FadeOut(arc), FadeOut(fant), run_time=0.5)
        self.remove(arc, fant)
        sF = seta7(X, V.c2p(2.8, 1.9), CAMPO, 7, 28)
        self.gat("a gente desenha o vetor de saída")
        self.play(GrowArrow(sF), run_time=0.9)
        fx = TC(r"\F(\P{X})", 1120, 420, 64)
        self.gat("a função se chama campo vetorial")
        self.play(caneta(fx))
        geral = TC(r"\F(\X,\Y) = \textcolor{cc}{P}(\X,\Y)\,\ii + \textcolor{cc}{Q}(\X,\Y)\,\jj", 1120, 590, 44)
        self.gat("em geral um campo no plano")
        self.play(caneta(geral))
        self.wait(max(0.1, min(2.0, self.resta() - 0.5)))

        # ── B5-2 · F⃗ = j⃗: vento uniforme ──
        self.an("B5-2")
        self.play(FadeOut(VGroup(dX, lX, sF, fx, geral)), run_time=0.4)
        self.remove(dX, lX, sF, fx, geral)
        f2 = TC(r"\F(\X,\Y) = \jj", 1120, 470, 56)
        self.gat("um campo que devolve o mesmo vetor")
        self.play(caneta(f2))
        c2 = campo7(V, lambda x, y: (0.0, 1.0), -3, 3, -3, 3, passo=0.6, rmin=0, lmax=0.5, mmax=1.0, nome="B5-2 j")
        self.gat("desenhado como campo")
        self.play(LaggedStart(*[GrowArrow(s_) for s_ in sorted(c2, key=lambda s_: s_._xy[1])], lag_ratio=0.01), run_time=1.6)
        l2 = legenda("VENTO UNIFORME", 1124, 580)
        self.play(FadeIn(l2), run_time=0.5)
        vm2, g2 = mini(1320, 780, 48)       # origem num cruzamento grosso, unidade 48 px
        t2 = legenda("COMO TRANSFORMAÇÃO", 1320, 744, GEO, "center", 24)
        self.gat("a mesma fórmula lida como transformação")
        self.play(FadeIn(t2), LaggedStart(*[FadeIn(d, scale=0.5) for d in g2], lag_ratio=0.08), run_time=0.8)
        alvo2 = VGroup(*[ponto7(vm2.c2p(0, 1), SAI, 9) for _ in g2])
        self.gat("todo ponto do plano vai parar")
        self.play(Transform(g2, alvo2), run_time=1.4)
        self.gat("um desenho mostra vento")
        self.play(pulso(c2, 1.0), run_time=0.9)

        # ── B5-3 · F⃗ = x i⃗ + y j⃗ (quadro 14) ──
        self.an("B5-3")
        self.play(FadeOut(VGroup(f2, c2, l2, g2, t2)), run_time=0.4)
        self.remove(f2, c2, l2, g2, t2)
        f3 = TC(r"\F(\X,\Y) = \X\,\ii + \Y\,\jj", 1120, 470, 56)
        self.gat("o campo que devolve em cada ponto")
        self.play(caneta(f3))
        c3 = campo7(V, lambda x, y: (x, y), -3, 3, -3, 3, passo=0.6, rmin=0.4, rmax=3.3, mmax=3.3, lmax=0.5, nome="B5-3 radial")
        o3 = ponto7(V.c2p(0, 0), WHITE_, 6)
        self.gat("cada seta aponta para fora")
        self.play(LaggedStart(*[GrowArrow(s_) for s_ in sorted(c3, key=lambda s_: math.hypot(*s_._xy))], lag_ratio=0.012), FadeIn(o3), run_time=1.8)
        n3 = TC(r"\|\F\| = \sqrt{x^2+y^2}", 1120, 590, 56)
        self.gat("o tamanho da seta é igual")
        self.play(caneta(n3))
        circ = VGroup(*[circ7(V, r, GEO, 2, (10, 9), 0.6) for r in (1, 2)])
        l3 = legenda("MAIS LONGE DA ORIGEM, SETA MAIOR", 1124, 700)
        self.gat("em cima de uma mesma circunferência")
        self.play(Create(circ), FadeIn(l3), run_time=0.9)
        vm3, g3 = mini(1320, 900, 48)
        t3 = legenda("COMO TRANSFORMAÇÃO", 1320, 868, GEO, "center", 24)
        self.gat("e como transformação")
        self.play(FadeIn(t3), LaggedStart(*[FadeIn(d, scale=0.5) for d in g3], lag_ratio=0.08), run_time=0.8)
        i3 = legenda("IDENTIDADE: NADA SE MEXE", 1320, 1046, SAI, "center", 24)
        self.gat("é a identidade")
        self.play(FadeIn(i3), run_time=0.5)
        self.gat("como campo é uma explosão")
        self.play(pulso(c3, 1.0), run_time=1.0)

        # ── B5-4 · as duas perguntas (quadro 15) ──
        self.an("B5-4")
        self.limpa(rt=0.4)
        pa, pb = painel_c(480, 540, 720, 600, "TRANSFORMAÇÃO", WHITE_), painel_c(1440, 540, 720, 600, "CAMPO", CAMPO2)
        vA, vB = Vista(480, 540, 96), Vista(1440, 540, 96)
        dA, dB = ponto7(vA.c2p(-1.6, -0.8), GEO, 11), ponto7(vA.c2p(1.6, 0.9), SAI, 11)
        a_, b_ = vA.c2p(-1.45, -0.65), vA.c2p(1.42, 0.85)
        voo_ = DashedVMobject(VMobject().set_points([a_, a_ + (b_ - a_) * 0.3 + UP * 0.9, b_ + (a_ - b_) * 0.3 + UP * 0.6, b_ - RIGHT * 0.05]).set_stroke(WHITE_, 4 / 1.2, 1).set_fill(opacity=0), num_dashes=22)
        voo_._sem_contorno = True
        tX, tpX = TC("X", *pxy(vA.c2p(-1.9, -1.25)), 40, "c", caneta=False), TC(r"\S{\varphi(X)}", *pxy(vA.c2p(1.7, 1.45)), 40, "c", caneta=False)
        dC = ponto7(vB.c2p(-1, -0.6), POS7, 11)
        sC = seta7(vB.c2p(-1, -0.6), vB.c2p(1.4, 0.6), CAMPO, 7, 28)
        tC1, tC2 = TC(r"\P{X}", *pxy(vB.c2p(-1.3, -1.05)), 40, "c", caneta=False), TC(r"\F(X)", *pxy(vB.c2p(1.2, 1.2)), 40, "c", caneta=False)
        qA, qB = legenda("PARA ONDE O PONTO VAI?", 480, 920, WHITE_, "center", 32), legenda("QUE SETA O PONTO CARREGA?", 1440, 920, CAMPO2, "center", 32)
        self.gat("nenhum dos dois desenhos")
        self.play(FadeIn(pa), FadeIn(pb), run_time=0.6)
        self.gat("como transformação a pergunta é")
        self.play(FadeIn(dA), FadeIn(dB), Create(voo_), FadeIn(tX), FadeIn(tpX), FadeIn(qA, shift=0.1 * UP), run_time=1.0)
        self.gat("como campo a pergunta é")
        self.play(FadeIn(dC), GrowArrow(sC), FadeIn(tC1), FadeIn(tC2), FadeIn(qB, shift=0.1 * UP), run_time=1.0)
        self.sai_fim()
