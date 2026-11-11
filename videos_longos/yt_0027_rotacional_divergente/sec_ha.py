"""Lote PHA (handoff v2; quadros 01 e 02): layout B, sem canto. H1: molduras, campos em anéis (r = 1; 1,5; 2; 2,5; mmax comum 2,5), a fita de tinta
radial e as rodinhas em (1, 0). H2: fluxo exato de t = 0 a 2π sincronizado com a fala (completa o giro na frase) e de 2π a 3π. H3: congela em 3π, a
circunferência r = 1, as setas do anel r = 1 engrossam aos pares, a pergunta embaixo. A1: abertura padrão (sem ícones); o canto entra no fim."""
from v27 import *  # noqa: F401,F403

VE, VD = Vista(480, 540, 96), Vista(1440, 540, 96)
AN = [1, 1.5, 2, 2.5]


def hook_campos(ctx=False, cor_e=None, cor_d=None, nome="H"):
    cE = campo_polar(VE, F_GIRO, AN, mmax=2.5, ctx=ctx, cor=cor_e, nome=f"{nome} esquerda (−y, x)")
    cD = campo_polar(VD, F_VORT, AN, mmax=2.5, ctx=ctx, cor=cor_d, nome=f"{nome} direita (−y, x)/r²")
    return cE, cD


class LoteHA(Base):
    CANTO = False

    def corpo(self):
        # ── H1 ──
        self.an("H1")
        pE, pD = painel(130, 260, 700, 560), painel(1090, 260, 700, 560)
        cE, cD = hook_campos()
        fu = furo7(VD, 0.6)
        self.grade(papel(VE, area_px(VE, 130, 260, 700, 560)), papel(VD, area_px(VD, 1090, 260, 700, 560)))   # final: grade de cada painel
        self.play(Create(pE), Create(pD), run_time=0.8)
        anel = lambda s: (round(math.hypot(*s._xy), 3), math.atan2(s._xy[1], s._xy[0]))
        self.play(FadeIn(fu), cresce_campo(cE, 1.8, anel), cresce_campo(cD, 1.8, anel))
        fE, fD = Fita(VE, fl_giro), Fita(VD, fl_vort)
        self.gat("tudo dá voltas em torno do centro")
        self.play(Create(fE), Create(fD), run_time=1.0)
        rE, rD = Roda(VE, 0.42).pose((1, 0), 0), Roda(VD, 0.42).pose((1, 0), 0)
        self.gat("soltar uma rodinha")
        self.play(FadeIn(rE, shift=0.4 * DOWN), FadeIn(rD, shift=0.4 * DOWN), run_time=0.7)
        self.ate(0.97)

        # ── H2 · uma volta (t = 2π) na frase do giro; depois até 3π ──
        self.an("H2")

        def passo(m, a, t0, t1, rapida):
            t = t0 + (t1 - t0) * a
            fE.em(t)
            fD.em(t)
            x, y = fl_giro(np.array([1.0]), np.array([0.0]), t)
            rE.pose((float(x[0]), float(y[0])), t)                 # ½ rot = 1: gira junto com a volta
            x, y = fl_vort(np.array([1.0]), np.array([0.0]), t)
            rD.pose((float(x[0]), float(y[0])), 0.0)               # ½ rot = 0: nunca muda de orientação
        self.gat("no primeiro")
        rt1 = max(3.0, self.falta("ela também completou um giro") + 0.6)
        print(f"[motor] H2: t de 0 a 2π em {rt1:.2f} s (fator {2 * PI / rt1:.3f})")
        self.play(UpdateFromAlphaFunc(VGroup(fE, fD, rE, rD), lambda m, a: passo(m, a, 0.0, 2 * PI, False)), run_time=rt1, rate_func=linear)
        self.gat("no segundo")
        rt2 = max(2.5, self.resta() - 0.3)
        print(f"[motor] H2: t de 2π a 3π em {rt2:.2f} s (fator {PI / rt2:.3f})")
        self.play(UpdateFromAlphaFunc(VGroup(fE, fD, rE, rD), lambda m, a: passo(m, a, 2 * PI, 3 * PI, False)), run_time=rt2, rate_func=linear)
        print(f"[hook] em t = 3π: rodinha esquerda deu {fE.t / (2 * PI):.3f} voltas e girou {rE.ang / (2 * PI):.3f} giros; "
              f"direita: orientação {math.degrees(rD.ang):.3f}° (deve ser 0)")
        qa_fluxo("H fita (−y, x)/r²", VD, F_VORT, np.stack([fD.x0, fD.y0], 1)[:-1], fD.t, fD.larga.points[0::4][: len(fD.x0)])

        # ── H3 · congela; r = 1; setas aos pares; a pergunta ──
        self.an("H3")
        c1E, c1D = vcirc(VE, 1, SAIF, 4, alpha=0.9), vcirc(VD, 1, SAIF, 4, alpha=0.9)
        self.play(Create(c1E), Create(c1D), run_time=0.9)
        uE = sorted([s for s in cE if abs(s._r - 1) < 1e-9], key=lambda s: math.atan2(s._xy[1], s._xy[0]))
        uD = sorted([s for s in cD if abs(s._r - 1) < 1e-9], key=lambda s: math.atan2(s._xy[1], s._xy[0]))
        dmax = max(float(np.linalg.norm((a.get_end() - VE.c2p(0, 0)) - (b.get_end() - VD.c2p(0, 0)))) for a, b in zip(uE, uD)) * 120
        print(f"[hook] anel r = 1: {len(uE)} pares; maior diferença entre as setas dos dois painéis = {dmax:.4f} px a 1080p")
        self.gat("os dois campos são idênticos")
        self.play(LaggedStart(*[AnimationGroup(Transform(a, destaca_seta(a)), Transform(b, destaca_seta(b))) for a, b in zip(uE, uD)], lag_ratio=0.35), run_time=2.2)
        perg = T("AS MESMAS SETAS. POR QUE SÓ UMA GIRA?", 960, 930, 40, "center", SAIF)
        self.gat("então por que uma gira")
        self.play(FadeIn(perg, shift=0.1 * UP), run_time=0.6)
        self.ate(0.97)
        self.grade(self.grade0)                                               # final: a abertura volta à grade padrão
        self.limpa(rt=0.5)

        # ── A1 · abertura padrão; o canto entra no fim ──
        self.an("A1")
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(P3(0, 0.9)), num_dashes=48).set_stroke(GEO, 2.2, opacity=o) for r, o in ((2.1, 0.45), (2.45, 0.25))])
        for m in aneis.get_family():
            m._sem_contorno = True
        bv = T("BEM-VINDOS AO PARALLAX LAB", 960, 870, 56, "center")
        self.play(FadeIn(logo, scale=0.94), FadeIn(aneis), FadeIn(bv, shift=0.1 * UP), run_time=0.8)
        self.play(Rotate(aneis[0], 0.6), Rotate(aneis[1], -0.5), rate_func=linear, run_time=max(1.0, self.falta("hoje a aula")))
        tit = T("ROTACIONAL E DIVERGENTE", 960, 470, 80, "center")
        nv1 = T("NESTE VÍDEO:", 960, 620, 40, "center", CAMPO)
        nv2 = T("GIRO · ESPALHAMENTO · NUM PONTO SÓ", 960, 690, 40, "center", WHITE_, bold=False)
        self.gat("hoje a aula")
        self.play(FadeOut(logo), FadeOut(aneis), FadeOut(bv), run_time=0.35)
        self.remove(logo, aneis, bv)
        self.play(FadeIn(tit, shift=0.1 * UP), run_time=0.7)
        self.gat("duas medidas")
        self.play(FadeIn(nv1, shift=0.1 * UP), run_time=0.5)
        self.gat("o rotacional que mede o giro")
        self.play(FadeIn(nv2[:4]), run_time=0.5)
        self.gat("o divergente que mede o espalhamento")
        self.play(FadeIn(nv2[4:17]), run_time=0.5)
        self.gat("a gente vai descobrir")
        self.play(FadeIn(nv2[17:]), run_time=0.5)
        self.gat("bora")                                                       # final: o canto entra e o título sai no "Bora?" (a fala acaba logo)
        self.play(FadeIn(self.h1), FadeOut(tit), FadeOut(nv1), FadeOut(nv2), run_time=0.4)
        self.remove(tit, nv1, nv2)
        self.sai_fim()
