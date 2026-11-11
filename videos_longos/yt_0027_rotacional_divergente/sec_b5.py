"""Lote PB5 · A FALSA FONTE (handoff v2; quadros 15 e 16). B5-1: palco com a falsa fonte e o furo. B5-2a: o setor coral pelo fluxo exato t 0 → 2 UMA vez
(raios finais 2,33 e 2,56) com o fantasma; as duas derivadas (fala nova) e div F = 0; ÁREA 0,28 → 0,28. B5-2b: campo em contexto, a caixa [1, 2] × [−½, ½],
as quatro setas e os números junto de cada parede; ENTRA, SAI, saldo = 0. B5-3: layout B, explosão × falsa fonte, div = 2 e div = 0."""
from v27 import *  # noqa: F401,F403
from sec_ha import VD, VE

V = Vista(600, 540, 120)


def lbl(s, X, Y, size=40, al="c"):
    x, y = canto_xy(V, X, Y)
    return TP(s, x, y, size, al)


def fluxo_parede(Ff, x0, x1, y0, y1, n=4000):
    u = (np.arange(n) + 0.5) / n
    ys, xs = y0 + (y1 - y0) * u, x0 + (x1 - x0) * u
    return (np.mean(Ff(x0 + 0 * ys, ys)[0]) * (y1 - y0), np.mean(Ff(x1 + 0 * ys, ys)[0]) * (y1 - y0),
            np.mean(Ff(xs, y1 + 0 * xs)[1]) * (x1 - x0), -np.mean(Ff(xs, y0 + 0 * xs)[1]) * (x1 - x0))


class LoteB5(Base):
    ANTES = "DIVERGENTE"
    def corpo(self):
        # ── B5-1 ──
        self.an("B5-1")
        self.secao("A FALSA FONTE")
        cf_ = campo7(V, F_FONTE, rmin=0.75, mmax=1.4, nome="B5 falsa fonte")
        fu = furo7(V, 0.55)
        self.play(FadeIn(fu), cresce_campo(cf_, 1.6))
        fF = TC(r"\F = \dfrac{(\X,\ \Y)}{\X^2+\Y^2}", 1120, 300, 48)
        self.gat("é a explosão dividida")
        self.play(caneta(fF))
        self.ate(0.97)

        # ── B5-2a · o setor ──
        self.an("B5-2")
        P0 = setor_pts(1.2, 1.6, 0.25)
        fant = vlinha(V, [tuple(p) for p in P0], CORAL, 3, alpha=0.6, dash=(8, 7))
        st = Pedaco(V, uv_setor(1.2, 1.6, 0.25), fl_fonte)                      # v4 §4: malha em (r, θ) levada pelo fluxo exato
        cl1 = esconde(cf_, clar([(1.0, -0.75, 2.8, 0.75)]))                 # R1: clareira do setor (início e fim do movimento)
        self.gat("solta um pedacinho de fluido")
        self.play(some(cl1), FadeIn(st, scale=0.7), FadeIn(fant), run_time=0.5)
        self.play(*corre(self, [st], 2.0, max(3.0, self.falta("a área não muda") - 0.2), rate=smooth))
        rr = np.hypot(st.XY[:, 0], st.XY[:, 1])
        print(f"[setor] B5-2: raios em t = 2: {rr.min():.3f} a {rr.max():.3f} (alvo 2,33 e 2,56); área {area_poly(P0):.5f} → {area_poly(st.XY):.5f}")
        la = legenda("ÁREA DO PEDACINHO: 0,28 → 0,28", 1124, 560, CORAL)     # alvo 13
        lm = legenda("MAIS LARGO E MAIS FINO", 1124, 620, GEO)
        self.gat("a área não muda")                                           # final §2.5: aqui só as legendas; div F = 0 fica para o fim
        self.play(FadeIn(la, shift=0.1 * UP), FadeIn(lm, shift=0.1 * UP), run_time=0.6)
        d1 = TC(r"\dfrac{\partial \Pp}{\dx} = \dfrac{\Y^2 - \X^2}{(\X^2+\Y^2)^2}", 1120, 730, 44)
        d2 = TC(r"\dfrac{\partial \Qq}{\dy} = \dfrac{\X^2 - \Y^2}{(\X^2+\Y^2)^2}", 1120, 870, 44)
        self.gat("as derivadas dizem o mesmo")
        self.play(caneta(d1, ritmo=0.8), caneta(d2, ritmo=0.8, atraso=0.3))          # final: "as duas parcelas" escritas juntas
        self.gat("e se cancelam")
        self.play(pulso(VGroup(d1, d2), 1.04), run_time=0.8)    # as parcelas se cancelam

        # ── B5-2b · a caixa ──
        self.gat("coloca uma caixa parada")
        sai = [st, fant, d1, d2, la, lm, fF]
        cl2 = esconde(cf_, clar([(0.45, -1.45, 3.1, 1.45)]))                # S11: clareira no retângulo da caixa e dos números
        self.play(*[FadeOut(m_) for m_ in sai], UpdateFromAlphaFunc(cf_, lambda m_, a: m_.contexto(a > 0.5)),
                  volta(VGroup(*[s_ for s_ in cl1 if s_ not in cl2])), some(VGroup(*[s_ for s_ in cl2 if s_ not in cl1])), run_time=0.5)
        self.remove(*sai)
        x0, x1, y0, y1 = 1, 2, -0.5, 0.5
        cx = VGroup(preenche(V, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], CHAPA, 0.55, 4), vlinha(V, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], GEO, 3))
        setas = [seta7(V.c2p(0.62, 0), V.c2p(1, 0), CAMPO2, 6, 20), seta7(V.c2p(2, 0), V.c2p(2.4, 0), CAMPO2, 6, 20),
                 seta7(V.c2p(1.5, 0.5), V.c2p(1.62, 0.88), CAMPO2, 6, 18), seta7(V.c2p(1.5, -0.5), V.c2p(1.62, -0.88), CAMPO2, 6, 18)]
        nums = [lbl(r"\D{0{,}927}", 0.8, 0.8, 36), lbl(r"\D{0{,}490}", 2.62, 0.32, 36), lbl(r"\D{0{,}219}", 2.05, 1.1, 36), lbl(r"\D{0{,}219}", 2.05, -1.1, 36)]
        e, d, c, b = fluxo_parede(F_FONTE, x0, x1, y0, y1)
        print(f"[caixa] B5-2: entra {e:.4f}; sai {d:.4f} + {c:.4f} + {b:.4f} = {d + c + b:.4f}; saldo {d + c + b - e:+.1e}")
        self.play(FadeIn(cx), run_time=0.5)
        self.play(*[GrowArrow(s_) for s_ in setas], run_time=0.6)
        self.play(*[FadeIn(n_) for n_ in nums], run_time=0.5)
        en = VGroup(legenda("ENTRA", 1124, 360, SAI), TC(r"\D{0{,}927}", 1124, 420, 46))
        sa = VGroup(legenda("SAI", 1124, 520, SAI), TC(r"\D{0{,}490 + 0{,}219 + 0{,}219 = 0{,}927}", 1124, 580, 46))
        # final: ENTRA e SAI escritos juntos em "a gente soma o que entra e o que sai" (a voz real não dá tempo para um depois do outro);
        # em "é exatamente o que sai" a caixa pulsa; a conclusão div F = 0 em Ω por último (o "saldo = 0" separado saiu: a conta SAI = ENTRA já o mostra)
        self.gat("a gente soma o que entra")
        self.play(FadeIn(en[0], run_time=0.4), caneta(en[1]), FadeIn(sa[0], run_time=0.4), caneta(sa[1], atraso=0.3),
                  self.em("é exatamente o que sai", pulso(cx, 1.04, run_time=0.6)))
        d0 = TC(r"\dv\F = \D{0} \ \text{ em } \Omega", 1120, 720, 52)       # final §2.5: a conclusão por último, na coluna, embaixo
        self.gat("o divergente é zero em todo ponto")
        self.play(caneta(d0))
        self.ate(0.97)

        # ── B5-3 · lado a lado ──
        self.an("B5-3")
        self.limpa_junto(rt=0.5)
        self.grade(papel(VE, area_px(VE, 130, 260, 700, 560)), papel(VD, area_px(VD, 1090, 260, 700, 560)))   # final: grade de cada painel
        pE, pD = painel(130, 260, 700, 560), painel(1090, 260, 700, 560)
        cE = campo7(VE, F_EXPL, -3.0, 3.0, -2.4, 2.4, 0.6, rmin=0.3, rmax=2.8, mmax=2.8, nome="B5-3 explosão")
        cD = campo7(VD, F_FONTE, -3.0, 3.0, -2.4, 2.4, 0.6, rmin=0.75, rmax=2.8, mmax=1.4, nome="B5-3 falsa fonte")   # final §2.6: rmin e compressão do B5-1, grade simétrica
        fD = furo7(VD, 0.55)
        self.play(FadeIn(pE), FadeIn(pD), FadeIn(fD), cresce_campo(cE, 1.2), cresce_campo(cD, 1.2))
        tA, tB = TC(r"\dv = \D{2}", 480, 910, 52, "c"), TC(r"\dv = \D{0}", 1440, 910, 52, "c")
        self.gat("não quer dizer fonte")
        self.play(caneta(tA), caneta(tB, atraso=0.4))
        self.ate(0.97)
        self.sai_fim()
