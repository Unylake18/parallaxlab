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
        self.play(FadeIn(ch), FadeIn(zn), onda(cmp, 1.0), run_time=1.0)   # final M1: onda
        f1a = TC(r"\F = (\X,", 1120, 330, 52)                 # a fórmula é escrita no ritmo da fala (componente a componente)
        f1b = TC(r"-\Y)", 1120, 330, 52)
        f1b.shift(RIGHT * (f1a.get_right()[0] + 0.17 - f1b.get_left()[0]))
        self.gat("que fechou o episódio passado")      # final (sync): o campo nasce em "lembra do campo"; a fórmula logo depois
        self.play(caneta(f1a))
        self.gat("e a vertical é menos y")
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
        self.gat("olha o que acontece")
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
        self.gat("mas a forma mudou completamente")
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
        self.play(FadeIn(Pc, scale=0.5), FadeIn(lPc), FadeIn(mc, shift=0.06 * UP), LaggedStart(*[Create(c) for c in cs], lag_ratio=0.5), run_time=0.7)
        self.play(FadeIn(cp, shift=0.06 * UP), run_time=0.3)
        self._fecha(antes=0.4)                   # final (sync): a saída do H cabe na fala (sem estouro no A1)
        self.limpa(rt=0.4)

        # ── A1 · handoff final §2.1 (alvos 38 e 39): a logo clássica fica a tela toda; uma peça entra por frase; o canto entra no fim ──
        self.an("A1")
        CL = P3(0, 0.9)
        logo = self.logo(5.6).move_to(CL)
        aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(CL), num_dashes=48).set_stroke(GEO, 2.2, opacity=o) for r, o in ((2.1, 0.45), (2.45, 0.25))])
        for m in aneis.get_family():
            m._sem_contorno = True
        bv = T("BEM-VINDOS AO PARALLAX LAB", 960, 850, 46, "center")
        self.gat("fala pessoal")
        self.play(FadeIn(logo, scale=0.94), FadeIn(aneis), FadeIn(bv, shift=0.1 * UP), FadeOut(self.wm), run_time=0.8)
        self.remove(self.wm)
        gira = lambda rt: (Rotate(aneis[0], 0.12 * rt, about_point=aneis[0].get_center(), rate_func=linear),
                           Rotate(aneis[1], -0.1 * rt, about_point=aneis[1].get_center(), rate_func=linear))
        # etapa 2: a logo sobe e diminui (largura ≈ 380 px, centro y ≈ 250 px) em 0,5 s; entra CÁLCULO III
        cal = T("CÁLCULO III", 960, 478, 28, "center", GEO, bold=False)
        tit = T("LIMITE, CONTINUIDADE E DERIVADAS PARCIAIS", 960, 566, 54, "center")
        nv = T("NESTE VÍDEO:", 960, 646, 30, "center", "#2EE6A0")

        def linha(a, b, y):
            pa = T(a, 0, y, 36, "left")
            pp = T("·", 0, y, 36, "left", "#8CFFD2", bold=False)
            pb = T(b, 0, y, 36, "left", "#8CFFD2", bold=False)
            pp.move_to([pa.get_right()[0] + 14 / 120 + pp.width / 2, pa.get_center()[1], 0])   # o ponto na meia altura das maiúsculas (T alinha pela base do glifo)
            pb.shift(RIGHT * (pp.get_right()[0] + 14 / 120 - pb.get_left()[0]))
            g = VGroup(pa, pp, pb)
            return g.shift(RIGHT * (PX(960, 0)[0] - g.get_center()[0]))
        linhas = [linha(a, b, y) for (a, b), y in zip((("O LIMITE", "CHEGAR PERTO"), ("A CONTINUIDADE", "NÃO PULAR"),
                                                      ("AS DERIVADAS PARCIAIS", "MEDIR A MUDANÇA"), ("A TABELA", "GIRO, ÁREA E DEFORMAÇÃO")), (722, 775, 828, 881))]
        k = 380 / 672
        self.play(*gira(self.falta("esse é o terceiro episódio")), run_time=max(0.2, self.falta("esse é o terceiro episódio")))
        self.gat("esse é o terceiro episódio")
        Lg = Group(logo, aneis)
        self.play(Lg.animate.scale(k).move_to(P3(0, 4.5 - 250 / 120)), FadeOut(bv), run_time=0.5)
        self.remove(bv)
        self.play(FadeIn(cal, shift=0.06 * UP), *gira(0.5), run_time=0.5)
        eventos = [("para isso entram três ideias", tit), ("uma apoiada na outra", nv), ("primeiro o limite", linhas[0]),
                   ("depois a continuidade", linhas[1]), ("e por fim as derivadas parciais", linhas[2]), ("numa tabela de quatro números", linhas[3])]
        for n, (fr, m) in enumerate(eventos):
            rt = self.falta(fr)
            if rt >= 0.2:
                self.play(*gira(rt), run_time=rt)
            self.gat(fr)
            self.play(FadeIn(m, shift=0.06 * UP), *gira(0.5), run_time=0.5)
            print(f"[A1] entra {['título', 'NESTE VÍDEO', 'linha 1', 'linha 2', 'linha 3', 'linha 4'][n]} em «{fr}»")
        rt = self.falta("então vamos começar pelo chão")
        if rt >= 0.2:
            self.play(*gira(rt), run_time=rt)
        self.gat("então vamos começar pelo chão")
        self.wm.set_opacity(0.45)
        self.play(FadeIn(self.h1), FadeIn(self.wm), *gira(0.5), run_time=0.5)          # o canto entra aqui (R10); tudo sai no fim do lote, com o B1 entrando
        rt = self.resta() - 0.35
        if rt >= 0.2:
            self.play(*gira(rt), run_time=rt)
        self.sai_fim()
