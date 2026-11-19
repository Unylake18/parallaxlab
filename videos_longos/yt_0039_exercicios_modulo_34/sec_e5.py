"""yt_0039 · E5 · a meia arruela (alvos 10, 11 e 12). E5-1: a meia arruela volta (palco do alvo 10); C5a (B em polares, x̄ = 0, A = 3π/2 e a
conferência 2π − π/2 ✓). E5-2 (alvo 10): o cateto y = r sen θ; C5b (M_x = 14/3; ȳ = 28/(9π) ≈ 0,990); o ⊕ pousa a 0,01 da borda; a lupa ×10;
NO BURACO. E5-3 (alvo 11): cartão; a chapa gira em torno do alfinete (sem balanço) até o ⊕ ficar embaixo; o fio de prumo; pela outra ponta;
as duas retas cruzam no ⊕, no ar; ANEL, FERRADURA, BUMERANGUE. E5-4 (alvo 12): o mapa ρ = k r; C5c (m = 7kπ/3; M_x = 15k/2; ȳ = 45/(14π)
≈ 1,023); a régua em pé (0,98 a 1,03) e o ⊕ sobe do buraco para a chapa: VOLTA PARA A CHAPA."""
from k39 import *
from k39 import _troca_col  # noqa: F401

V10 = Vw(560, 860, 230)
V12 = Vw(520, 860, 210)
YH = 28 / (9 * math.pi)
YK = 45 / (14 * math.pi)


def chapa_arr(v, fill=FUNDO_R, alerta=True, z=1):
    ar = arruela(v, fill=fill, z=z)
    fora = lin_px([v.px(*p) for p in arcoP(2)], GEO, 3, z=5)
    dentro = lin_px([v.px(*p) for p in arcoP(1)], AL if alerta else GEO, 3, z=5)
    base = VGroup(lin_px([v.px(-2, 0), v.px(-1, 0)], GEO, 3, z=5), lin_px([v.px(1, 0), v.px(2, 0)], GEO, 3, z=5))
    return ar, fora, dentro, base


class PE5(B39x):
    ANTES = "5 · A MEIA ARRUELA"
    COLX = 1180

    def corpo(self):
        v = V10
        # ═══ E5-1 · a área ═══
        self.an("E5-1")
        self.gat("agora sim a meia arruela")
        P = monta_palco(self, v, -2.4, 2.45, -.04, 2.45, ticks=[("x", -2, r"\Am{-2}"), ("x", -1, r"\Am{-1}"), ("x", 1, r"\Am{1}"), ("x", 2, r"\Am{2}")])
        ar, fora, dentro, base = chapa_arr(v)
        self.play(FadeIn(ar), Create(fora), Create(dentro), Create(base), run_time=1.0)
        self.colY = 240
        self.gat("em polares ela é um retângulo")
        ins = lambda r_, t_: (150 + (r_ - 1) * 200, 345 - t_ * 150 / math.pi)
        cel_ = celulas(1, 2, 0, math.pi, 4, 8, k=8)

        def pos51(r_, t_, a):
            pa, pb = ins(r_, t_), v.px(r_ * math.cos(t_), r_ * math.sin(t_))
            return (pa[0] + (pb[0] - pa[0]) * a, pa[1] + (pb[1] - pa[1]) * a)
        MA = MapaAcao(cel_, pos51, fill=mixh(BG_, GEO, .42), teste={(0, 3): AZC, (3, 3): CORAL}, z=3)
        lr_i, lt_i = TC(r"\R", 250, 378, 28, "c"), TC(r"\th", 120, 270, 28, "c")
        self.play(FadeIn(MA.g), run_time=0.4)
        self.pena(lr_i, lt_i, lag=0.05)
        self.play(FadeOut(lr_i), FadeOut(lt_i), run_time=0.3)
        self.remove(lr_i, lt_i)
        self.play(MA.anim(2.5), run_time=2.5)
        print(f"[mapa] {self.lote} E5-1 mapa em ação [1,2] × [0,π] → meia arruela (r cos θ, r sen θ): 32 células, 2,5 s")
        self.play(*MA.so_linhas(), run_time=0.4)
        self.gat("r vai de um a dois")
        B1 = linha(self, [("B", r"B:"), ("r", r"\ 1\le\R\le 2,"), ("t", r"\ 0\le\th\le\pi")], 34, escreve=False)
        rr_ = ix_(B1, "r")
        escreve_seq(self, B1, [(P["tk"][2][1], [rr_[0]]), (P["tk"][3][1], [rr_[-2]])], so=ix_(B1, "B", "r"))
        origem(self, "1 e 2 de 1 ≤ r ≤ 2", "marcas 1 e 2 do eixo (borda de dentro e de fora)")
        self.gat("e téta de zero a pi")
        th = ValueTracker(0.0)
        raio = always_redraw(lambda: lin_px([v.px(0, 0), v.px(2 * math.cos(th.get_value()), 2 * math.sin(th.get_value()))], LAR, 3, z=7))
        aT = always_redraw(lambda: lin_px([v.px(.3 * math.cos(t), .3 * math.sin(t)) for t in np.linspace(0, max(1e-3, th.get_value()), 40)], VAG, 3, z=7))
        self.add(th, raio, aT)
        self.play(th.animate.set_value(math.pi), run_time=1.6)
        escreve_seq(self, B1, [], so=ix_(B1, "t"))
        self.play(th.animate.set_value(1.0), run_time=0.8)
        raio.clear_updaters()
        aT.clear_updaters()
        self.gat("x barra é zero")
        sim = lin_px([v.px(0, 0), v.px(0, 2.3)], BR, 2, dash=(8, 8), z=6)
        self.play(Create(sim), FadeOut(MA.g), run_time=0.5)
        self.remove(MA.g)
        X1 = linha(self, [r"\xb=0"], 34, gap=22)
        leg_ao_lado(self, X1, "SIMETRIA", GEO, 24, 26)
        self.gat("a área é a integral")
        A1 = linha(self, [("A", "A"), ("e", "="), ("i1", r"\int_0^{\pi}"), ("i2", r"\!\!\int_1^2"), ("j", r"\Rj"), ("d", r"\,\dr\,\dth")], 34, gap=24)
        self.gat("aquele r é o jacobiano")
        self.leitura(G(A1, ix_(A1, "j")), rt=0.7)
        self.gat("a de dentro r ao quadrado")
        palavra(self, "DE DENTRO", GEO, 26, gap=14)
        D1 = linha_de(self, A1, [("c", r"\left[\dfrac{\R^2}{2}\right]_1^2")], [("j", "c"), ("i2", "c")], n=21, size=34, gap=10, nota="C5a: [r²/2]₁²")
        self.gat("quatro meios menos um meio")
        D1 = cad(self, D1, [("e", "="), ("d", r"\dfrac42-\dfrac12")], [("^c", "d")], n=21, nota="G(2) − G(1)")
        D1 = cad(self, D1, [("e", "="), ("r", r"\dfrac32")], [("^d", "r")], n=21, nota="= 3/2")
        degrau(self, "C5a", "[r²/2]₁² = 4/2 − 1/2 = 3/2")
        self.gat("A de fora é só multiplicar")
        palavra(self, "DE FORA", GEO, 26, gap=14)
        F1 = linha(self, [("f", r"\dfrac32"), ("c", r"\Big[\th\Big]_0^{\pi}")], 34, gap=10, voos=[(G(D1, ix_(D1, "r")), "f")])
        F1 = cad(self, F1, [("e", "="), ("r", r"\dfrac32\,\pi")], [("^f", "r"), ("^c", "r")], n=21, nota="(3/2)π")
        self.gat("a área é três pi")
        A2 = linha(self, [("A", "A"), ("e", "="), ("r", r"\Me{\dfrac{3\pi}{2}}")], 34, gap=22, voos=[(G(F1, ix_(F1, "r")), "r")])
        degrau(self, "C5a", "(3/2)[θ]₀^π = (3/2)π; A = 3π/2")
        self.gat("o meio disco grande")
        sobe_col(self, [m for m in self.colms if m is not A2], y0=240)       # v2 §4.1: a conferência entra com a coluna maior
        hg =poly_px([v.px(*p) for p in arcoP(2)], mixh(BG_, MEN, .25), 1.0, z=2)
        self.play(FadeIn(hg), run_time=0.5)
        K1 = linha(self, [("g", r"\dfrac{\pi\cdot 2^2}{2}"), ("e", "="), ("r", r"2\pi")], 32, gap=24)
        self.gat("o pequeno pi sobre")
        hp = poly_px([v.px(*p) for p in arcoP(1)], mixh(BG_, AL, .35), 1.0, z=3)
        self.play(FadeOut(hg), FadeIn(hp), run_time=0.5)
        self.remove(hg)
        K1 = cad(self, K1, [("q", r"\qquad"), ("p", r"\dfrac{\pi\cdot 1^2}{2}=\dfrac{\pi}{2}")], [], n=21, nota="π·1²/2 = π/2")
        self.gat("a diferença é três pi sobre dois")
        self.play(FadeOut(hp), run_time=0.3)
        self.remove(hp)
        K2 = linha(self, [("d", r"2\pi-\dfrac{\pi}{2}"), ("e", "="), ("r", r"\dfrac{3\pi}{2}")], 32, gap=22, voos=[(G(K1, ix_(K1, "r")), [0, 1])])
        ok_ao_lado(self, K2)
        degrau(self, "C5a", "π·2²/2 − π·1²/2 = 2π − π/2 = 3π/2 ✓")
        self._fecha(antes=0.6)

        # ═══ E5-2 · o momento e o buraco (alvo 10) ═══
        self.an("E5-2")
        chA = chip(self, r"A=\dfrac{3\pi}{2}", 1180, 175, de=G(A2, ix_(A2, "r")).copy())
        limpa_col(self)
        self.play(FadeOut(sim), run_time=0.3)
        self.remove(sim)
        self.colY = 240
        t0, r0 = 1.0, 1.6
        Pq = (r0 * math.cos(t0), r0 * math.sin(t0))
        self.gat("o momento em relação")
        M1 = linha(self, [("M", r"\Mx"), ("e", "="), ("ii", r"\iint"), ("y", r"y\,dA")], 34)
        self.gat("e y é r seno")
        rq = lin_px([v.px(0, 0), v.px(*Pq)], LAR, 3, z=7)
        ca = lin_px([v.px(Pq[0], 0), v.px(*Pq)], E2, 3, z=7)
        self.play(Transform(raio, rq), Create(ca), run_time=0.6)
        lc = rot_m(v, r"y=\R\sen\th", (Pq[0], Pq[1] * .5), 16, 0, 26, "l")
        self.pena(lc)
        M1 = cad(self, M1, [("e", "="), ("i1", r"\int_0^{\pi}"), ("i2", r"\!\!\int_1^2"), ("y", r"\R\sen\th"), ("c", r"\cdot"), ("j", r"\Rj"), ("d", r"\,\dr\,\dth")],
                 [("ii", "i1"), ("ii", "i2")], n=21, voos=[(lc.f, "y")], nota="C5b: o r sen θ voa do cateto")
        origem(self, "r sen θ (C5b)", "cateto magenta do triângulo polar")
        self.gat("A de dentro integra")
        palavra(self, "DE DENTRO", GEO, 26, gap=14)
        D2 = linha_de(self, M1, [("s", r"\sen\th"), ("c", r"\left[\dfrac{\R^3}{3}\right]_1^2")], [("^y", "s"), ("^y", "c"), ("^j", "c"), ("^i2", "c")], n=21, size=34, gap=10,
                      nota="C5b: sen θ [r³/3]₁²")
        # v2 B2: a de dentro é a tira radial (r de 1 a 2) no ângulo do raio
        tt_ = ValueTracker(t0)

        def tira_r():
            a_ = tt_.get_value()
            ts_ = np.linspace(a_ - .05, a_ + .05, 5)
            pts_ = [v.px(math.cos(t_), math.sin(t_)) for t_ in ts_] + [v.px(2 * math.cos(t_), 2 * math.sin(t_)) for t_ in ts_[::-1]]
            return poly_px(pts_, mixh(BG_, LAR, .8), 1.0, z=6)
        tr_ = always_redraw(tira_r)
        self.add(tt_)
        self.play(FadeIn(tr_), run_time=0.4)
        self.gat("oito terços menos um terço")
        R1_ = linha_de(self, D2, [("c", r"\left[\dfrac{\R^3}{3}\right]_1^2"), ("e", "="), ("d", r"\dfrac83-\dfrac13")], [("^c", "c")], n=21, size=34, gap=14,
                       nota="C5b: [r³/3]₁² em linha própria")
        R1_ = cad(self, R1_, [("e", "="), ("r", r"\dfrac73")], [("^d", "r")], n=21, nota="= 7/3")
        degrau(self, "C5b", "[r³/3]₁² = 8/3 − 1/3 = 7/3")
        self.gat("sete terços de seno")
        D2 = cad(self, D2, [("e", "="), ("r", r"\dfrac73\sen\th")], [("^s", "r")], n=21, nota="= (7/3) sen θ", voos=[(G(R1_, ix_(R1_, "r")).copy(), "r")])
        degrau(self, "C5b", "sen θ [r³/3]₁² = (7/3) sen θ")
        self.gat("A de fora é a integral do seno")
        palavra(self, "DE FORA", GEO, 26, gap=14)
        F2 = linha(self, [("f", r"\dfrac73"), ("c", r"\Big[-\cos\th\Big]_0^{\pi}")], 34, gap=10, voos=[(G(D2, ix_(D2, "r")[:3]), "f")])
        # v2 B2: a de fora leva a tira radial de θ = 0 a θ = π
        self.play(tt_.animate.set_value(.05), run_time=0.5)
        self.play(tt_.animate.set_value(math.pi - .05), run_time=4.0, rate_func=linear)
        tr_.clear_updaters()
        self.play(FadeOut(tr_), run_time=0.3)
        self.remove(tr_, tt_)
        print(f"[varre] {self.lote} E5-2 tira radial varre θ de 0 a π em 4,0 s (1 updater)")
        self.gat("menos cosseno de zero a pi")
        S1_ = linha_de(self, F2, [("c", r"\Big[-\cos\th\Big]_0^{\pi}"), ("e", "="), ("d", r"-\cos\pi-(-\cos 0)")], [("^c", "c")], n=21, size=34, gap=14,
                       nota="C5b: G(π) − G(0) com os valores")
        self.gat("aquele dois de sempre")
        S1_ = cad(self, S1_, [("e", "="), ("d", r"-(-1)-(-1)")], [("^d", "d")], n=21, nota="−(−1) − (−1)")
        S1_ = cad(self, S1_, [("e", "="), ("r", "2")], [("^d", "r")], n=21, nota="= 2")
        degrau(self, "C5b", "[−cos θ]₀^π = −cos π − (−cos 0) = −(−1) − (−1) = 2")
        self.gat("o momento é catorze")
        F2 = cad(self, F2, [("e", "="), ("p", r"\dfrac73\cdot 2")], [("^f", "p")], n=21, nota="(7/3)·2", voos=[(G(S1_, ix_(S1_, "r")).copy(), "p")])
        F2 = cad(self, F2, [("e", "="), ("r", r"\dfrac{14}{3}")], [("^p", "r")], n=21, nota="= 14/3")
        degrau(self, "C5b", "(7/3)[−cos θ]₀^π = (7/3)·2 = 14/3")
        chS = chip(self, r"\int_0^{\pi}\sen\th\,\dth=2", 1460, 175, size=28)
        self.gat("é momento sobre área")
        sobe_col(self, [m for m in self.colms if m is not F2], y0=240)
        Y1 = linha(self, [("y", r"\yb"), ("e", "="), ("f", r"\dfrac{14/3}{3\pi/2}")], 34, gap=26, escreve=False)
        nf, bf, df = frac_ix(Y1, "f")
        escreve_seq(self, Y1, [(G(F2, ix_(F2, "r")), nf), (G(chA.m, list(range(2, len(chA.m[0])))), df)])
        origem(self, "3π/2 no denominador de ȳ", "chip A = 3π/2")
        self.gat("inverte e multiplica")
        Y1 = cad(self, Y1, [("e", "="), ("a", r"\dfrac{14}{3}"), ("c", r"\cdot"), ("b", r"\dfrac{2}{3\pi}")], [(nf, "a"), (df, "b")], n=21, nota="(14/3)(2/(3π))")
        self.gat("vinte e oito sobre nove pi")
        Y2 = cad(self, Y1, [("e", "="), ("r", r"\dfrac{28}{9\pi}\approx 0{,}990")], [("^a", "r"), ("^b", "r")], n=21, desce=True, nota="28/(9π) ≈ 0,990")
        degrau(self, "C5b", "ȳ = (14/3)/(3π/2) = (14/3)(2/(3π)) = 28/(9π) ≈ 0,990")
        # v2 A3/A14: o slot de 0,990 < 1 fica 0,45 u abaixo do resultado (vazio até o voo); o ȳ nasce como chip
        n990 = TC(r"0{,}990<1", pxof(Y2.get_left())[0], pxof(Y2.get_bottom())[1] + 54 + 22, 36, "l")
        tira_chips(self, chA)
        chY = chip(self, r"\yb\approx 0{,}990", 1180, de=G(Y2, ix_(Y2, "r")[-5:]).copy())
        self.gat("zero vírgula novecentos e noventa")
        pc = cm(*v.px(0, 2.3), 13)
        self.play(FadeIn(pc), run_time=0.3)
        self.play(pc.animate.move_to(v.P(0, YH)), run_time=1.4)
        self.gat("menor que um por")
        LX_, LY_, LR_ = 230, 300, 120
        sc_ = 230 * 10
        toL = lambda X, Y: (LX_ + X * sc_, LY_ - (Y - 1) * sc_)
        disco_l = circ_px(LX_, LY_, LR_, GEO, 0, fill=BG_, fop=1.0, z=13)
        lim_x = LR_ / sc_
        arcpts = [toL(math.cos(math.pi / 2 + k), math.sin(math.pi / 2 + k)) for k in np.linspace(-lim_x * 1.02, lim_x * 1.02, 41)]
        topo_c = [(LX_ + LR_ * math.cos(a_), LY_ - LR_ * math.sin(a_)) for a_ in np.linspace(0, math.pi, 60)]
        dx0 = arcpts[0][0] - LX_
        chp = poly_px([p for p in topo_c] + arcpts, FUNDO_R, 1.0, z=14)
        brd = lin_px([p for p in arcpts if (p[0] - LX_) ** 2 + (p[1] - LY_) ** 2 <= LR_ ** 2], AL, 4, z=15)
        pcz = cm(*toL(0, YH), 14, z=16)
        mol = lupa_moldura(LX_, LY_, LR_)
        mol.set_z_index(17)
        lch = leg("CHAPA", LX_, LY_ - 60, BR, "center", 26)
        lbu = leg("BURACO", LX_, LY_ + 78, AL, "center", 26)
        for m_ in (lch, lbu):
            m_.set_z_index(18)
        guia = lin_px([v.px(0, YH), (LX_ + 40, LY_ + LR_ - 6)], GEO, 2, dash=(5, 6), z=12)
        self.play(Create(guia), FadeIn(disco_l), FadeIn(chp), Create(brd), Create(mol), FadeIn(pcz), run_time=1.0)
        self.pena(lch, lbu, lag=0.1)
        x10 = leg("× 10", LX_ + LR_ + 14, LY_ - LR_ + 30, GEO, "left", 26)
        self.pena(x10)
        voos(self, [(G(Y2, ix_(Y2, "r")[-5:]).copy(), parte(n990, list(range(5)), "0,990"))], rt=0.9, arco=-0.6)
        self.pena(parte(n990, list(range(5, len(n990[0]))), "< 1"))
        self.colms.append(n990)
        self.gat("cai no buraco")
        nb = placa_t("NO BURACO", *v.px(0, .30), AL, 30, "c")      # C7: dentro do buraco, longe do arco (≥ 14 px)
        self.pena(nb)
        self.marca("10_E5-2")
        self._fecha(antes=0.4)
        self.limpa_tudo(rt=0.4)
        tira_chips(self)

        # ═══ E5-3 · o fio de prumo (alvo 11) ═══
        self.an("E5-3")
        self.secao("5 · O FIO DE PRUMO")
        self.grade = papel_cartao()
        self.play(FadeIn(self.grade), run_time=0.3)
        s_ = 120      # C7: as duas chapas inteiras no palco (nada cortado, nada no canto/título)

        def chapa_px(pin, ox, oy):
            """A meia arruela com o ponto pin (coordenadas da chapa) em (ox, oy) px, sem girar; devolve (grupo, ⊕, f(p) → px)."""
            Rp = lambda p: (ox + (p[0] - pin[0]) * s_, oy - (p[1] - pin[1]) * s_)
            pts = [Rp(p) for p in arcoP(2) + arcoP(1)[::-1]]
            corpo = poly_px(pts, mixh(BG_, GEO, .55), 1.0, z=3)
            borda = lin_px(pts + [pts[0]], GEO, 2.5, z=4)
            c = cm(*Rp((0, YH)), 12, z=8)
            return VGroup(corpo, borda), c, Rp

        lados = [((2, 0), 560, 400, "PENDURADA PELA DIREITA", "pendura por uma ponta"), ((-2, 0), 1160, 400, "PENDURADA PELA ESQUERDA", "pela outra ponta")]
        self.gat("recorta essa meia arruela")
        ch0, c0, _ = chapa_px((2, 0), 560, 400)
        self.play(FadeIn(ch0), FadeIn(c0), run_time=0.6)
        fios = []
        for k, (pin, ox, oy, txt_, frase) in enumerate(lados):
            self.gat(frase)
            if k == 0:
                ch, c, Rp = ch0, c0, None
            else:
                ch, c, _ = chapa_px(pin, ox, oy)
                self.play(FadeIn(ch), FadeIn(c), run_time=0.6)
            al = ponto_px(ox, oy, BR, 7, z=10)
            self.play(FadeIn(al), run_time=0.3)
            if k == 0:
                self.gat("ela gira até o centro")
            vx, vy = 0 - pin[0], YH - pin[1]
            ang = -math.pi / 2 - math.atan2(vy, vx)
            self.play(Rotate(VGroup(ch, c), ang, about_point=PX(ox, oy)), run_time=1.5, rate_func=smooth)
            if k == 0:
                self.gat("pendura um fio de prumo")
            fio = lin_px([(ox, oy), (ox, oy + 3.6 * s_)], BR, 2, z=9)
            peso = poly_px([(ox - 8, oy + 3.6 * s_), (ox + 8, oy + 3.6 * s_), (ox, oy + 3.6 * s_ + 16)], BR, 1.0, z=9)
            self.play(Create(fio), FadeIn(peso), run_time=0.8)
            lt = leg(txt_, ox, 1000, GEO, "center", 26)
            self.pena(lt)
            fios.append(fio)
        self.gat("as duas linhas se cruzam")
        vv = Vw(1640, 800, 100)
        pts = [vv.px(*p) for p in arcoP(2) + arcoP(1)[::-1]]
        chv = VGroup(poly_px(pts, mixh(BG_, GEO, .55), 1.0, z=3), lin_px(pts + [pts[0]], GEO, 2.5, z=4))
        l1 = lin_px([vv.px(2, 0), vv.px(2 - 2 * 1.6, YH * 1.6)], BR, 2, dash=(8, 6), z=6)
        l2 = lin_px([vv.px(-2, 0), vv.px(-2 + 2 * 1.6, YH * 1.6)], BR, 2, dash=(8, 6), z=6)
        pp = VGroup(ponto_px(*vv.px(2, 0), BR, 6, z=9), ponto_px(*vv.px(-2, 0), BR, 6, z=9))
        self.play(FadeIn(chv), FadeIn(pp), run_time=0.6)
        self.play(TransformFromCopy(fios[0], l1), TransformFromCopy(fios[1], l2), run_time=1.0)
        cv = cm(*vv.px(0, YH), 12)
        self.play(FadeIn(cv), run_time=0.4)
        self.gat("no ar onde não tem")
        eq = T("O EQUILÍBRIO FICA NO AR", 1640, 560, 30, "center", MEN)
        self.pena(eq)
        self.gat("acontece com um anel")
        mini = [("ANEL", lambda X, Y: VGroup(circ_px(X, Y, 30, GEO, 2.5), circ_px(X, Y, 18, GEO, 2.5))),
                ("FERRADURA", lambda X, Y: lin_px([(X + 28 * math.cos(t), Y - 28 * math.sin(t)) for t in np.linspace(-.6, math.pi + .6, 40)], GEO, 8)),
                ("BUMERANGUE", lambda X, Y: lin_px([(X - 34, Y + 14), (X, Y - 18), (X + 34, Y + 14)], GEO, 8))]
        frs = ["acontece com um anel", "com uma ferradura", "com um bumerangue"]
        for i, ((nm_, fn), fr) in enumerate(zip(mini, frs)):
            if i:
                self.gat(fr)
            X, Y = 1440 + i * 170, 930
            ic = fn(X, Y)
            dot = cm(X, Y + (0 if i == 0 else 8), 7)
            self.play(Create(ic), FadeIn(dot), run_time=0.5)
            self.pena(leg(nm_, X, Y + 66, GEO, "center", 26))
        self.marca("11_E5-3")
        self._fecha(antes=0.4)
        self.limpa_tudo(rt=0.4)

        # ═══ E5-4 · a borda mais pesada (alvo 12) ═══
        self.an("E5-4")
        self.secao("5 · A BORDA MAIS PESADA")
        v = V12
        P = monta_palco(self, v, -2.35, 2.4, -.04, 2.45, ticks=[("x", -2, r"\Am{-2}"), ("x", -1, r"\Am{-1}"), ("x", 1, r"\Am{1}"), ("x", 2, r"\Am{2}")], rt=0.5)
        ar, fora, dentro, base = chapa_arr(v)
        self.play(FadeIn(ar), Create(fora), Create(dentro), Create(base), run_time=0.6)
        self.colX, self.colY = 1180, 240
        self.gat("e se a borda pesar")
        mp = meia_lua_mapa(v, 1, 2, lambda r: r, 2.0, z=2)
        h54 = [ar, fora, dentro, base, P["sx"], P["sy"]] + [x for t in P["tk"] for x in t]
        pal54, lx54, ly54 = massa_entra(self, "arruela", CAM_M54, 210, 520, 860, h54, P["lx"], P["ly"])
        lr = rot_m(v, r"\rr=\kk\,r", (-2.2, 2.62), 0, 0, 30, "l")
        lp = leg("MAIS PESADA LONGE DO CENTRO", *v.px(-2.2, 2.38), CI, "left", 26)
        self.pena(lr, lp, lag=0.1)
        self.gat("Pensa numa roda de bicicleta")
        M3 = linha(self, [("m", r"\mm"), ("e", "="), ("i1", r"\int_0^{\pi}"), ("i2", r"\!\!\int_1^2"), ("k", r"(\kk\,\R)"), ("c", r"\cdot"), ("j", r"\Rj"), ("d", r"\,\dr\,\dth")], 34,
                   voos=[(lr.f, "k")])
        self.gat("cada um tem um dono")
        k0, k1 = pxof(G(M3, ix_(M3, "k")).get_left())[0], pxof(G(M3, ix_(M3, "k")).get_right())[0]
        j0, j1 = pxof(G(M3, ix_(M3, "j")).get_left())[0], pxof(G(M3, ix_(M3, "j")).get_right())[0]
        yb_ = pxof(M3.get_bottom())[1] + 20
        ck = chave_h(k0, k1, yb_, CI, 2)
        cj = chave_h(j0 - 4, j1 + 4, yb_, LIMA, 2)
        tk_ = T("DENSIDADE", (k0 + k1) / 2 - 40, yb_ + 44, 26, "center", CI, bold=False)
        tj_ = T("JACOBIANO", (j0 + j1) / 2 + 80, yb_ + 44, 26, "center", LIMA, bold=False)
        self.play(Create(ck), Create(cj), run_time=0.4)
        self.pena(tk_, tj_, lag=0.1)
        self.colms += [ck, cj, tk_, tj_]
        self.colY = pxof(tk_.get_bottom())[1]
        self.gat("integra em r ao cubo")
        D3 = linha_de(self, M3, [("c", r"\kk\left[\dfrac{\R^3}{3}\right]_1^2")], [("k", "c"), ("j", "c"), ("i2", "c")], n=22, size=34, gap=16, nota="C5c: k[r³/3]₁²")
        self.gat("oito terços menos um")
        D3 = cad(self, D3, [("e", "="), ("d", r"\kk\left(\dfrac83-\dfrac13\right)")], [("^c", "d")], n=22, nota="G(2) − G(1)")
        self.gat("sete k sobre três a")
        D3 = cad(self, D3, [("e", "="), ("r", r"\dfrac{7\kk}{3}")], [("^d", "r")], n=22, nota="= 7k/3")
        self.gat("a de fora multiplica por pi")
        F3 = linha(self, [("f", r"\dfrac{7\kk}{3}"), ("c", r"\Big[\th\Big]_0^{\pi}"), ("e", "="), ("r", r"\dfrac{7\kk\pi}{3}")], 34, gap=22, voos=[(G(D3, ix_(D3, "r")), "f")])
        degrau(self, "C5c", "m = ∫∫ (k r)·r dr dθ: k[r³/3]₁² = k(8/3 − 1/3) = 7k/3; (7k/3)[θ]₀^π = 7kπ/3")
        self.gat("Agora o momento")
        chm = chip(self, r"\mm=\dfrac{7\kk\pi}{3}", 1180, 175, de=G(F3, ix_(F3, "r")).copy())
        chS2 = chip(self, r"\int_0^{\pi}\sen\th\,\dth=2", 1460, 175, size=28)
        limpa_col(self)
        self.colY = 240
        N3 = linha(self, [("M", r"\Mx"), ("e", "="), ("i1", r"\int_0^{\pi}"), ("i2", r"\!\!\int_1^2"), ("y", r"\R\sen\th"), ("c", r"\cdot"), ("k", r"\kk\,\R"), ("c2", r"\cdot"),
                          ("j", r"\Rj"), ("d", r"\,\dr\,\dth")], 34)
        self.leitura(G(N3, ix_(N3, "y")[:1]), G(N3, ix_(N3, "k")[-1:]), G(N3, ix_(N3, "j")), rt=0.8)
        self.gat("A de dentro é r à quarta")
        D4 = linha_de(self, N3, [("c", r"\kk\sen\th\left[\dfrac{\R^4}{4}\right]_1^2")], [("y", "c"), ("k", "c"), ("j", "c"), ("i2", "c")], n=22, size=34, gap=22,
                      nota="C5c: k sen θ [r⁴/4]₁²")
        self.gat("dezesseis quartos menos")
        D4 = cad(self, D4, [("e", "="), ("d", r"\kk\sen\th\left(\dfrac{16}{4}-\dfrac14\right)")], [("^c", "d")], n=22, nota="G(2) − G(1)")
        self.gat("quinze quartos")
        D4 = cad(self, D4, [("e", "="), ("r", r"\dfrac{15\kk}{4}\sen\th")], [("^d", "r")], n=22, desce=True, nota="= (15k/4) sen θ")
        self.gat("o mesmo dois da integral")
        F4 = linha(self, [("f", r"\dfrac{15\kk}{4}"), ("c", r"\cdot"), ("dois", "2")], 34, gap=22, voos=[(G(D4, ix_(D4, "r")[:5]), "f"), (G(chS2.m, [len(chS2.m[0]) - 1]), "dois")])
        origem(self, "o 2 de (15k/4)·2", "chip ∫₀^π sen θ dθ = 2")
        self.gat("quinze k sobre dois")
        F4 = cad(self, F4, [("e", "="), ("r", r"\dfrac{15\kk}{2}")], [("^f", "r"), ("^dois", "r")], n=22, nota="= 15k/2")
        degrau(self, "C5c", "k sen θ[r⁴/4]₁² = k sen θ(16/4 − 1/4) = (15k/4) sen θ; (15k/4)·2 = 15k/2")
        self.gat("Dividindo momento por massa")
        Y3 = linha(self, [("y", r"\yb"), ("e", "="), ("f", r"\dfrac{15\kk/2}{7\kk\pi/3}")], 34, gap=24, escreve=False)
        nf, bf, df = frac_ix(Y3, "f")
        escreve_seq(self, Y3, [(G(F4, ix_(F4, "r")), nf), (chm.m, df)])
        self.gat("o k cancela")
        Y3 = cad(self, Y3, [("e", "="), ("a", r"\dfrac{15\kk}{2}"), ("c", r"\cdot"), ("b", r"\dfrac{3}{7\kk\pi}")], [(nf, "a"), (df, "b")], n=22, nota="inverte e multiplica")
        na, ba, da = frac_ix(Y3, "a")
        nb, bb_, db = frac_ix(Y3, "b")
        kb = [i for i in db if Y3[0][i].get_center()[0] < G(Y3, db).get_center()[0]][1:2]
        cancela(self, G(Y3, na[-1:]), G(Y3, kb))
        self.gat("quarenta e cinco sobre catorze")
        Y4 = cad(self, Y3, [("e", "="), ("r", r"\dfrac{45}{14\pi}\approx 1{,}023")], [(na[:-1], "r"), (nb, "r"), (da, "r")], n=22, desce=True, nota="o k cancela: 45/(14π) ≈ 1,023")
        degrau(self, "C5c", "ȳ = (15k/2)/(7kπ/3) = (15k/2)(3/(7kπ)) = 45/(14π) ≈ 1,023")
        massa_volta(self, pal54, [mp, ar, fora, dentro, base, P["sx"], P["sy"]] + [x for t in P["tk"] for x in t], lx54, ly54, P["lx"], P["ly"])
        tira_chips(self)
        limpa_col(self)
        h1 = leg("HOMOGÊNEA", 1080, 178, GEO, "left", 26)
        c1 = chip(self, r"\dfrac{28}{9\pi}\approx 0{,}990", 1080, size=28)
        h2 = leg("BORDA MAIS PESADA", 1480, 178, CI, "left", 26)
        c2 = chip(self, r"\dfrac{45}{14\pi}\approx 1{,}023", 1480, size=28, de=G(Y4, ix_(Y4, "r")).copy())
        self.pena(h1, h2, lag=0.1, passo=0.04)
        RX = 1240
        Ry = lambda val: 860 - (val - .98) / .05 * 600
        regua = lin_px([(RX, Ry(.98)), (RX, Ry(1.03))], GEO, 4, z=6)
        ticks_ = VGroup(*[lin_px([(RX - 10, Ry(val)), (RX + 10, Ry(val))], GEO, 2, z=6) for val in np.arange(.98, 1.0301, .01)])
        self.play(Create(regua), Create(ticks_), run_time=0.6)
        hs = [(YH, BR, r"0{,}990", "HOMOGÊNEA", c1), (1.0, AL, r"1{,}000", "BORDA DO BURACO", None), (YK, CI, r"1{,}023", None, c2)]
        for val, cor, ntx, lab, chp_ in hs:
            gl_ = lin_px([v.px(-.3, val), v.px(2.05, val)], cor, 2, dash=(8, 8), z=6)
            q = v.px(2.05, val)
            gp = lin_px([q, (RX - 20, Ry(val))], cor, 2, dash=(4, 6), z=6)
            pt = ponto_px(RX, Ry(val), cor, 10, z=9)
            nn = TC(ntx, RX + 40, Ry(val), 30, "l")
            self.play(Create(gl_), Create(gp), FadeIn(pt), run_time=0.35)
            if chp_ is not None:
                voos(self, [(G(chp_.m, list(range(len(chp_.m[0])))[-5:]).copy(), nn)], rt=0.6)
            else:
                self.pena(nn, passo=0.05)
            if lab:
                self.pena(leg(lab, RX + 160, Ry(val) + 10, cor, "left", 28), passo=0.04)
            else:
                self.pena(TC(r"\rr=\kk\,r", RX + 160, Ry(val), 30, "l"))
        pv = cm(*v.px(0, YH), 10, vaz=True)
        pk = cm(*v.px(0, YH), 12)
        self.play(FadeIn(pv), FadeIn(pk), run_time=0.4)
        self.play(pk.animate.move_to(v.P(0, YK)), run_time=1.0)
        self.gat("volta para a chapa")
        vc = T("VOLTA PARA A CHAPA", 1240, 960, 32, "left", MEN)
        self.pena(vc)
        self.marca("12_E5-4")
        self.sai_fim()
