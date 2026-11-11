"""Lote PH · H (v3: alvos 01 e 02; chapa A + zona; H3 novo: as derivadas parciais e o chão) + A (bem-vindos). Da v1: Layout A, sem canto até o fim do A.
H: campo (x, −y) (mmax 3), quadradinho coral de lado 1,2 (chapa + malha 4×4); fluxo exato (x eᵗ, y e⁻ᵗ) de 0 a 0,55 UMA vez, com o fantasma;
ÁREA 1,44 → 1,44 (placa); coluna na caneta; MAS DEFORMA (lima); QUE NÚMERO MEDE ISSO? A: abertura padrão; o canto entra no fim."""
from v28 import *  # noqa: F401,F403

V = Vista(600, 540, 120)
S0 = 1.2


def palco_sela(v=V, skip=None, nome="H (x, −y)"):
    return campo28(v, F_SELA, mmax=3, rmin=0, skip=skip, nome=nome)


class LoteH(Base):
    CANTO = False

    def corpo(self):
        # ── H1 ──
        self.an("H1")
        q0 = quad_pts((0, 0), S0)
        ped = Pedaco(V, q0)
        zera_chapas()
        ch, zn = chapa_px(*LAY_A, nome="A (H)"), zona_px(1080, 180, 1920, 1020, "coluna A (H)")
        cmp = palco_sela()
        self.play(FadeIn(ch), FadeIn(zn), cresce_campo(cmp, 1.0), run_time=1.0)
        f1a = TC(r"\F = (\X,", 1120, 330, 52)                 # a fórmula é escrita no ritmo da fala (componente a componente)
        f1b = TC(r"-\Y)", 1120, 330, 52)
        f1b.shift(RIGHT * (f1a.get_right()[0] + 0.17 - f1b.get_left()[0]))
        self.gat("lembra do campo")
        self.play(caneta(f1a))
        self.gat("menos a coordenada vertical")
        self.play(caneta(f1b))
        self.gat("coloca um quadradinho")
        clareira(cmp, lambda: clarPoly(ped.poly(), .25))
        self.play(FadeIn(ped, scale=0.8), run_time=0.6)
        f2 = TC(r"\rot\F = \V{0}", 1120, 450, 52)
        self.gat("o rotacional dá zero")
        self.play(caneta(f2))
        f3 = TC(r"\dv\F = \D{0}", 1120, 560, 52)
        self.gat("o divergente também")
        self.play(caneta(f3))
        self.ate(0.97)

        # ── H2 · deixa o fluido andar ──
        self.an("H2")
        self.gat("deixa o fluido andar")
        fan = fantasma(V, q0)
        self.add(fan)
        a0 = ped.area()
        self.play(anda(ped, fl_sela, 0.55, 6.0, rate=linear, nome="H (x eᵗ, y e⁻ᵗ)"))   # v2 (E8): ~6 s, linear
        print(f"[deforma] H: área {a0:.4f} → {ped.area():.4f}; lados {S0 * math.exp(.55):.3f} × {S0 * math.exp(-.55):.3f}")
        area = TP(r"\text{ÁREA } 1{,}44 \to 1{,}44", *canto_xy(V, 0, -1), 34, "c")
        lbl = clar28([(-1.1, -1.25, 1.1, -.75)])
        cmp.clear_updaters()
        clareira(cmp, lambda: ou(clarPoly(ped.poly(), .25), clarPoly(q0, .15), lbl))
        self.gat("a área continua a mesma")
        self.play(FadeIn(area, shift=0.05 * UP), run_time=0.5)
        md = T("MAS DEFORMA", 1120, 700, 48, cor=LIMA)
        self.gat("mas virou outra coisa")
        self.play(FadeIn(md, shift=0.08 * UP), run_time=0.5)
        self.ate(0.97)

        # ── H3 · que número mede isso? as derivadas parciais; o chão: chegar perto de um ponto (alvo 02) ──
        self.an("H3")
        qn = T("QUE NÚMERO MEDE ISSO?", 1120, 330, 40)
        self.gat("que número mede isso")
        col = [f1a, f1b, f2, f3, md]
        self.play(*[FadeOut(m) for m in col], run_time=0.4)
        self.remove(*col)
        self.play(FadeIn(qn, shift=0.06 * UP), run_time=0.5)
        rp = legenda("A RESPOSTA: AS DERIVADAS PARCIAIS", 1124, 420, GEO, size=30)
        dd = TC(r"\dfrac{\partial\F}{\dx}\qquad\dfrac{\partial\F}{\dy}", 1120, 530, 48)
        self.gat("nas derivadas parciais")
        self.play(FadeIn(rp, shift=0.06 * UP), run_time=0.4)
        self.play(caneta(dd, ritmo=0.6))
        self.gat("começar pelo chão")
        cmp.clear_updaters()
        sai = [ped, fan, area]
        self.play(*[FadeOut(m) for m in sai], run_time=0.6)
        self.remove(*sai)
        ctx = mesma_grade(cmp, F_SELA, 3, ctx=True)
        for a_, b_ in zip(cmp, ctx):
            if math.hypot(*a_._xy) < 1.05 + .25:
                b_.set_opacity(0)
        self.play(Transform(cmp, ctx), run_time=0.8)
        herda(cmp, ctx)
        Pc = ponto7(V.c2p(0, 0), POS, 10, 11)
        lPc = TP(r"\Pt", *canto_xy(V, .22, -.26), 32)
        cs = [vlinha(V, circ_pts(r), POS, 2.5, dash=(8, 8)).set_z_index(6) for r in (.95, .6, .3)]
        mc = legenda("MAS ANTES, O CHÃO:", 1124, 680, GEO, size=30)
        cp = T("CHEGAR PERTO DE UM PONTO", 1120, 735, 38, cor=POS)
        self.gat("chegar perto de um ponto")
        self.play(FadeIn(Pc, scale=0.5), FadeIn(lPc), FadeIn(mc, shift=0.06 * UP), run_time=0.5)
        for c in cs:
            self.play(Create(c), run_time=0.35)
        self.play(FadeIn(cp, shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)
        self.limpa(rt=0.5)

        # ── A1 · abertura padrão; o canto entra no fim ──
        self.an("A1")
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(P3(0, 0.9)), num_dashes=48).set_stroke(GEO, 2.2, opacity=o) for r, o in ((2.1, 0.45), (2.45, 0.25))])
        for m in aneis.get_family():
            m._sem_contorno = True
        bv = T("BEM-VINDOS AO PARALLAX LAB", 960, 870, 56, "center")
        self.play(FadeIn(logo, scale=0.94), FadeIn(aneis), FadeIn(bv, shift=0.1 * UP), run_time=0.8)
        self.play(Rotate(aneis[0], 0.6), Rotate(aneis[1], -0.5), rate_func=linear, run_time=max(1.0, self.falta("hoje são três ideias")))
        tit = T("LIMITE, CONTINUIDADE E DERIVADAS PARCIAIS", 960, 470, 64, "center")
        nv1 = T("NESTE VÍDEO:", 960, 620, 40, "center", CAMPO)
        nv2 = T("CHEGAR PERTO · NÃO PULAR · MEDIR A MUDANÇA", 960, 690, 40, "center", WHITE_, bold=False)
        print(f"[abertura] glifos: título {len(tit)}, nv2 {len(nv2)}")
        self.gat("hoje são três ideias")
        self.play(FadeOut(logo), FadeOut(aneis), FadeOut(bv), run_time=0.35)
        self.remove(logo, aneis, bv)
        self.play(FadeIn(tit, shift=0.1 * UP), FadeIn(nv1, shift=0.1 * UP), run_time=0.7)
        cortes = [0, 11, 20, len(nv2)]                     # CHEGARPERTO (11) · NÃOPULAR (1 + 8) · MEDIRAMUDANÇA (1 + 13)
        for fr, (i0, i1) in zip(("limite", "continuidade", "derivadas parciais"), zip(cortes, cortes[1:])):
            self.gat(fr)
            self.play(FadeIn(nv2[i0:i1]), run_time=0.5)
        self.gat("numa tabela de quatro números")
        self.play(FadeIn(self.h1), run_time=0.5)
        self.ate(0.97)
        self.sai_fim()
