"""Lote PX4 (v2): X4 as naves que se separam (2D, céu sem piso). Referencial do CM: 1.000 kg sai a +2 m/s e 2.000 kg a −1 m/s (⊕ parado);
momentos iguais (2.000 kg·m/s), energias 2.000 J e 1.000 J (barras 2 : 1 exatas). G23: 1.000 kg, 2.000 kg e 3.000 J nascem no desenho e
voam para a conta; K = ½mv² → K = p²/2m numa linha nova; os resultados descem para as setas e as barras. X4-5: massas iguais / M → ∞
(seta, sem número mudando) e o painel da nave-mãe (150.000 J → 153.000 J; barra do CM quebrada, ESCALA DO PAINEL).
v4 §2 #1–#4: naves centradas no ESQUEMA (⊕ em x = −3,6) e nada do ESQUEMA passa de x = 0,2 (as naves andam no máximo τ = 1,6 a 0,4 por m/s);
p⃗ em cima da seta; velocidades em setas violeta embaixo de cada nave, rótulo embaixo da ponta (que segue a nave); o selo do referencial com
0,3 livre em volta; cada barra com o valor em cima e a massa da nave embaixo; o 3.000 J sai depois de voar para a conta."""
from prob2 import *  # noqa: F401,F403

KX = 0.4
SP = 0.45
SKE = 0.55
XBL, XBH = -3.0, -6.4                       # x das barras da nave leve e da pesada
N = lambda s: s.replace(".", "{.}")


class LoteX4(Prob2):
    def construct(self):
        self.setup_base(cap="PROBLEMA 5 · AS NAVES")
        self.x4()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def x4(self):
        XC, YN = -3.6, 0.2
        mL, mH = 1000.0, 2000.0
        d = 2.0
        xL0, xH0 = XC + d * mH / (mL + mH), XC - d * mL / (mL + mH)
        tau = ValueTracker(0.0)
        op_p, modo = ValueTracker(0.0), ValueTracker(0.0)          # modo: 0 massas reais · 1 iguais · 2 pesadíssima
        op_v, modo_v = ValueTracker(0.0), ValueTracker(0.0)        # setas de velocidade: 0 no referencial do CM (2 e −1 m/s) · 1 na nave-mãe (12 e 9)
        KV = 0.5
        VEL_NAVE = {0: (2.0, -1.0), 1: (12 * 0.07 / KV, 9 * 0.07 / KV)}
        self.add(tau, op_p, modo, op_v, modo_v)
        nL, nH = nave(1.5, 0.62, 1), nave(1.95, 0.82, -1)
        carga = VGroup(RoundedRectangle(corner_radius=0.08, width=0.34, height=0.3).set_fill(escuro(HEAT, 0.3), 1).set_stroke(HEAT, 2),
                       Circle(radius=0.3).set_stroke(width=0).set_fill(HEAT, 0.22)).move_to(P3((xL0 - 0.75 + xH0 + 0.975) / 2, YN))

        def xs():
            t = tau.get_value()
            return xL0 + KX * 2.0 * t, xH0 - KX * 1.0 * t

        def cena():
            xl, xh = xs()
            g = VGroup(nH.copy().move_to(P3(xh, YN)), nL.copy().move_to(P3(xl, YN)))
            xc = (mL * xl + mH * xh) / (mL + mH)
            g.add(marcador_cm(P3(xc, YN), r=0.17))
            o = op_p.get_value()
            if o > 0.01:
                L_ = SP * 2.0
                g.add(seta(P3(xl - 0.45, YN + 0.72), P3(xl - 0.45 + L_, YN + 0.72), MAG, 7, tip=0.22, op=o),
                      seta(P3(xh + 0.45, YN + 0.72), P3(xh + 0.45 - L_, YN + 0.72), MAG, 7, tip=0.22, op=o))
            ov_ = op_v.get_value()
            if ov_ > 0.01:
                vs_ = VEL_NAVE[int(round(modo_v.get_value()))]
                for x_, v_ in ((xl, vs_[0]), (xh, vs_[1])):
                    a_ = P3(x_ - 0.5 * KV * v_, YN - 1.4)
                    g.add(self.seta_v(a_, a_ + P3(KV * v_, 0), "CENTRO DE MASSA" if modo_v.get_value() < 0.5 else "NAVE-MÃE", VEL, 6, tip=0.2, op=ov_, nome=f"{v_:g}"))
            self.reg("naves", cm=P3(xc, YN), esperado=P3(XC, YN), tau=tau.get_value())
            return g
        cv = vivo(cena)
        self._evitar = [lambda: np.array([P3(xs()[0] + dx, YN + dy) for dx in np.linspace(-0.8, 0.8, 9) for dy in (-0.35, 0, 0.35)] +
                                         [P3(xs()[1] + dx, YN + dy) for dx in np.linspace(-1.0, 1.0, 9) for dy in (-0.45, 0, 0.45)])]
        # ── X4-1 ──
        self.an("X4-1")
        self.add(cv, carga)                                                              # v5: as naves já estão na tela no primeiro quadro (a transição do lote cuida da entrada)
        self.chip(3)
        self.pede("REFERENCIAL DO CENTRO DE MASSA")                                      # v5 G32: o selo entra primeiro (a direita nunca fica vazia)
        zona_n = Rectangle(width=8.6, height=2.4).move_to(P3(0, YN))                      # v7: o palco das naves (invisível) é o destaque enquanto o selo e a carga entram
        self.pulsa([zona_n], 0.9, Indicate(carga, color=HEAT, scale_factor=1.15))
        self.pulsa([zona_n], 0.9)
        lL = rot("1.000 kg", 30).move_to(P3(xL0, YN - 0.78))
        lH = rot("2.000 kg", 30).move_to(P3(xH0, YN - 0.88))
        self.gat("o dobro da massa")
        self.play(FadeIn(lH), FadeIn(lL), run_time=0.6)                                   # "uma com o dobro da massa da outra"
        self.ate(0.32)
        self.referencial("DO CENTRO DE MASSA")                                           # depois do chip (canto livre)
        lE = rot("3.000 J", 30, KC).move_to(carga.get_center() + P3(0, 0.88))
        gE = VGroup()
        self.ate(0.6)
        self.gat("dá energia cinética ao conjunto")
        self.play(FadeIn(lE), Indicate(carga, color=HEAT, scale_factor=1.2), run_time=0.9)   # "dá energia cinética ao conjunto"
        self.ate(0.75)
        self.hip("SEM FORÇA EXTERNA · PARADAS NO REFERENCIAL DO CM")
        q = VGroup(tx("COM QUE VELOCIDADE", 28, bold=True), tx("CADA UMA SAI?", 28, bold=True)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(q)
        self.ate(0.88)
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.5)
        self.foco = q
        self.ate(0.97)
        # ── X4-2 ──
        self.an("X4-2")
        fl = flash(carga.get_center(), 0.16, HEAT)
        lib = rot("LIBERADOS", 28, KC)
        lib.move_to(lE.get_center() + RIGHT * (lE.width + lib.width) / 2 + RIGHT * 0.24)
        self.play(FadeIn(fl, scale=0.5), FadeOut(carga), FadeOut(gE), FadeIn(lib), lE.animate.shift(LEFT * (lib.width + 0.24) / 2), lib.animate.shift(LEFT * (lib.width + 0.24) / 2),
                  run_time=0.4)                         # v5: "3.000 J LIBERADOS", ainda preso à carga
        self.play(FadeOut(lib), FadeOut(fl, scale=1.3), run_time=0.3)                                  # o rótulo sai antes de o dado voar (nada no caminho)
        lL.add_updater(lambda m: m.move_to(P3(xs()[0], YN - 0.78)))
        lH.add_updater(lambda m: m.move_to(P3(xs()[1], YN - 0.88)))
        Ed, ied = M(r"E_{lib}", "=", r"3000\ \mathrm{J}", size=48, cores={0: KC, 2: KC})
        self.pilha.poe(Ed)
        self.voa([(lE, mp(Ed, ied, [2]))], extra=[FadeIn(mp(Ed, ied, [0, 1])), tau.animate(rate_func=linear).set_value(1.0)], rt=1.4,
                 origem=False, arco_esq=0.7)                                                                          # o dado voa para a CONTA; nada fica solto no ESQUEMA
        self.play(FadeOut(lE), run_time=0.25)                                                                         # G31: a origem some na chegada (não fica '3.000 J' solto entre as naves)
        lE.clear_updaters()
        self.remove(lE)
        lp = vivo(lambda: VGroup(mtex(r"\vec p_1", MAG, 40).set_opacity(op_p.get_value()).next_to(P3(xs()[0] - 0.45 + SP, YN + 0.72), UP, buff=0.34),
                                 mtex(r"\vec p_2", MAG, 40).set_opacity(op_p.get_value()).next_to(P3(xs()[1] + 0.45 - SP, YN + 0.72), UP, buff=0.34)))   # v4 §2 #1: em cima da seta
        self.add(lp)
        self.ate(0.3)
        self.play(op_p.animate.set_value(1.0), tau.animate(rate_func=linear).set_value(1.25), run_time=0.9)
        P1, ip = M(r"\vec P", "=", r"\vec 0", r"\ \Rightarrow\ ", r"\vec p_1", "+", r"\vec p_2", "=", r"\vec 0", size=48, cores={0: MAG, 4: MAG, 6: MAG})
        self.pilha.poe(P1)
        self.ate(0.4)
        lpc = lp.submobjects[0]
        self.voa([(lpc[0], mp(P1, ip, [4])), (lpc[1], mp(P1, ip, [6]))], extra=[FadeIn(mp(P1, ip, [0, 1, 2, 3, 5, 7, 8])), tau.animate(rate_func=linear).set_value(1.4)], rt=1.2)
        P2, ip2 = M(r"|\vec p_1|", "=", r"|\vec p_2|", "=", "p", size=48, cores={0: MAG, 2: MAG, 4: MAG})
        self.pilha.poe(P2)
        self.ate(0.62)
        self.passo(P1, P2, (J(ip, 4), J(ip2, 0)[1:-1]), (J(ip, 6), J(ip2, 2)[1:-1]), rt=1.3)
        self.ate(0.85)
        self.play(onda(P3(XC, YN)), tau.animate(rate_func=linear).set_value(1.6), run_time=0.8)
        self.foco = P2
        self.ate(0.97)
        # ── X4-3: barras ──
        self.an("X4-3")
        yb = -3.1
        bh = ValueTracker(0.0)
        self.add(bh)

        def barras():
            m_ = modo.get_value()
            mh = 2000.0 - 1000.0 * m_ if m_ <= 1.0 else 1000.0 + 39000.0 * (m_ - 1.0)       # v5: as barras animam a partir das 2 : 1
            kL, kH = 3000 * mh / (mL + mh), 3000 * mL / (mL + mh)
            g = VGroup(Line(P3(-7.0, yb), P3(-2.4, yb)).set_stroke(GEO, 2))
            for x_, k_ in ((XBL, kL), (XBH, kH)):                       # v4: barras longe das setas de velocidade (que andam com as naves)
                h = SKE * k_ / 1000 * bh.get_value()
                if h > 0.005:
                    g.add(Rectangle(width=0.7, height=h).move_to(P3(x_, yb + h / 2)).set_stroke(width=0).set_fill(KC, 1))
            self.reg("barras", kL=kL, kH=kH)
            return g
        bv = vivo(barras)
        bmL = rot("1.000 kg", 26).next_to(P3(XBL, yb), DOWN, buff=0.2)                                  # v4 §2 #3: a massa da nave embaixo da barra
        bmH = rot("2.000 kg", 26).next_to(P3(XBH, yb), DOWN, buff=0.2)
        self.play(FadeIn(bv), bh.animate.set_value(1.0), FadeIn(bmL), FadeIn(bmH), run_time=1.4)
        chave = VGroup(Brace(Line(P3(XBH - 0.5, yb + 2 * SKE + 0.12), P3(XBL + 0.5, yb + 2 * SKE + 0.12)), UP, buff=0.0, color=GEO),
                       VGroup(txt("TOTAL =", 26), rot("3.000 J", 28, KC)).arrange(RIGHT, buff=0.14).move_to(P3((XBL + XBH) / 2, yb + 2 * SKE + 0.12 + 0.52)))
        self.play(FadeIn(chave), run_time=0.6)
        qq = cartao("SE OS MOMENTOS SÃO IGUAIS,", "POR QUE AS ENERGIAS NÃO SÃO?", size=28)
        self.pilha.poe(qq)
        self.ate(0.4)
        self.play(FadeIn(qq, shift=0.1 * UP), run_time=0.7)
        self.foco = qq
        self.ate(0.97)
        # ── X4-4: K = p²/2m ──
        self.an("X4-4")
        self.pilha.so(Ed, anims=[FadeOut(chave)], rt=0.5)
        A1, a1 = M("K", "=", r"\tfrac{1}{2}", "m", "v^2", r"\ ,\ \ ", "v", "=", r"\tfrac{p}{m}", size=48, cores={0: KC, 4: VEL, 6: VEL, 8: MAG})
        A2, a2 = M("K", "=", r"\frac{p^2}{2m}", size=52, cores={0: KC, 2: MAG})
        A2b = caixa_l(A2, KC)
        self.pilha.poe(A1)
        self.play(FadeIn(A1), run_time=0.7)
        self.pilha.poe(A2b)
        self.ate(0.1)
        self.passo(A1, A2, (J(a1, 0), J(a2, 0)), (J(a1, 1), J(a2, 1)), (J(a1, 8)[0:1], J(a2, 2)[0:1]), (J(a1, 4)[1:], J(a2, 2)[1:2]),
                   (J(a1, 2)[2:], J(a2, 2)[3:4]), (J(a1, 3), J(a2, 2)[4:]), extra=[FadeIn(A2b[0])], rt=1.5)
        B1, b1 = M(r"\frac{p^2}{2\cdot 1000}", "+", r"\frac{p^2}{2\cdot 2000}", "=", r"3000\ \mathrm{J}", size=48, cores={4: KC})
        self.pilha.poe(B1)
        self.ate(0.3)
        self.voa([(lL, mp(B1, b1, [0])[-4:]), (lH, mp(B1, b1, [2])[-4:]), (mp(Ed, ied, [2]), mp(B1, b1, [4]))],
                 extra=[FadeIn(mp(B1, b1, [0])[:-4]), FadeIn(mp(B1, b1, [2])[:-4]), FadeIn(mp(B1, b1, [1, 3]))], rt=1.3, arco_esq=-0.9)   # por cima do outro rótulo
        lE.clear_updaters()
        self.remove(lE)
        B2, b2 = M("p^2", r"\cdot\tfrac{3}{4000}", "=", r"3000\ \mathrm{J}", size=48, cores={0: MAG, 3: KC})
        self.pilha.poe(B2)
        self.ate(0.44)
        self.passo(B1, B2, (J(b1, 3), J(b2, 2)), (J(b1, 4), J(b2, 3)), (J(b1, 0)[:2], J(b2, 0)), (J(b1, 0)[2:] + J(b1, 1, 2), J(b2, 1)), rt=1.4)
        B3, b3 = M("p", "=", r"2000\ \mathrm{kg\,m/s}", size=48, cores={0: MAG, 2: MAG})
        B3b = caixa_l(B3, MAG)
        self.pilha.poe(B3b)
        self.ate(0.54)
        self.passo(B2, B3, (J(b2, 0), J(b3, 0)), (J(b2, 2), J(b3, 1)), (J(b2, 1) + J(b2, 3), J(b3, 2)), extra=[FadeIn(B3b[0])], rt=1.1)
        V1, iv = M(r"v_1", "=", r"2\ \mathrm{m/s}", r"\ ,\ ", r"K_1", "=", r"2000\ \mathrm{J}", size=46, cores={0: VEL, 2: VEL, 4: KC, 6: KC})
        V2, iv2 = M(r"v_2", "=", r"1\ \mathrm{m/s}", r"\ ,\ ", r"K_2", "=", r"1000\ \mathrm{J}", size=46, cores={0: VEL, 2: VEL, 4: KC, 6: KC})
        WL = VGroup(txt("LEVE", 24), V1).arrange(DOWN, buff=0.04, aligned_edge=LEFT)
        WP = VGroup(txt("PESADA", 24), V2).arrange(DOWN, buff=0.04, aligned_edge=LEFT)
        self.pilha.poe(WL)
        ponta = lambda k: P3(xs()[k] + 0.5 * KV * VEL_NAVE[0][k], YN - 1.4)
        lv = VGroup(rot("2 m/s", 30, VEL).next_to(ponta(0), DOWN, buff=0.3), rot("1 m/s", 30, VEL).next_to(ponta(1), DOWN, buff=0.3))
        lk = VGroup(rot("2.000 J", 28, KC), rot("1.000 J", 28, KC))
        lk[0].next_to(P3(XBL, yb + SKE * 2), UP, buff=0.22)                                         # v4 §2 #3: o valor em cima da barra
        lk[1].next_to(P3(XBH, yb + SKE), UP, buff=0.22)
        self.gat("a nave leve sai")
        self.voa([(mp(B3, b3, [2]), mp(V1, iv, [2])), (A2, mp(V1, iv, [6]))], extra=[FadeIn(mp(V1, iv, [0, 1, 3, 4, 5])), FadeIn(WL[0])], rt=1.0, origem=False, cada=0.7)   # v = p/m, K = p²/2m (a leve)
        self.play(op_v.animate.set_value(1.0), run_time=0.4)
        self.voa([(mp(V1, iv, [2]), lv[0])], rt=0.9, origem=False)
        lv[0].add_updater(lambda m: m.next_to(ponta(0), DOWN, buff=0.3))                             # o rótulo segue a ponta da seta (e a nave)
        self.pilha.poe(WP)
        self.gat("a pesada a um")                                                                    # v7: cada dado entra na palavra dele (a pesada, 1 m/s)
        self.voa([(mp(B3, b3, [2]), mp(V2, iv2, [2])), (A2, mp(V2, iv2, [6]))], extra=[FadeIn(mp(V2, iv2, [0, 1, 3, 4, 5])), FadeIn(WP[0])], rt=1.0, origem=False, cada=0.7)
        self.voa([(mp(V2, iv2, [2]), lv[1])], rt=0.9, origem=False, arco_esq=0.9)         # v6 §1.4: por baixo da linha (não passa sobre o "v₂ =")
        lv[1].add_updater(lambda m: m.next_to(ponta(1), DOWN, buff=0.3))
        K1, ik = V1, iv

        def cota_sep():
            xl, xh = xs()
            y = YN - 2.15
            return VGroup(Line(P3(xh + 0.98, y), P3(xl - 0.75, y)).set_stroke(GEO, 2), Line(P3(xh + 0.98, y - 0.1), P3(xh + 0.98, y + 0.1)).set_stroke(GEO, 2),
                          Line(P3(xl - 0.75, y - 0.1), P3(xl - 0.75, y + 0.1)).set_stroke(GEO, 2))
        cs = vivo(cota_sep)
        sl = linha_m("SE AFASTAM A", rot("3 m/s", 30, VEL), size=28)                                    # v4: na CONTA (as barras ocupam o ESQUEMA)
        self.pilha.poe(sl)
        self.gat("três metros por segundo")
        self.play(FadeIn(sl, shift=0.1 * UP), run_time=0.8)                                              # as naves seguem afastadas (os rótulos não cruzam as barras)
        self.foco = sl
        # v7: as barras crescem de novo enquanto a fala diz "dois mil joules para a leve e mil para a pesada" (relógio da cena, sem tween)
        self.gat("dois mil joules para a leve")
        A4_ = ANC["X4-4"]
        t_b0 = (self.nq + self._off) / FPS
        t_b1 = A4_["ini"] + A4_["t"][-1] + 0.3
        bh.set_value(0.0)
        bh.add_updater(lambda m: m.set_value(min(1.0, max(0.0, (self.clk.get_value() + self._off / FPS - t_b0) / max(0.5, t_b1 - t_b0)))))
        self.voa([(mp(V1, iv, [6]), lk[0])], rt=0.9, origem=False)
        self.gat("mil para a pesada")
        self.voa([(mp(V2, iv2, [6]), lk[1])], rt=0.9, origem=False, arco_esq=0.9)
        self.foco = WP
        self.ate(0.97)
        bh.clear_updaters()
        bh.set_value(1.0)
        # ── X4-5 ──
        self.an("X4-5")
        for m_ in lv:
            m_.clear_updaters()
        self.pilha.limpa(anims=[FadeOut(VGroup(lk, lv)), op_v.animate.set_value(0.0)])
        self.confere(["MASSAS IGUAIS → BARRAS IGUAIS", "UMA MUITO PESADA → A OUTRA LEVA QUASE TUDO"])
        lH.clear_updaters()
        lH2 = rot("1.000 kg", 30).move_to(lH.get_center())
        bmH2 = rot("1.000 kg", 26).move_to(bmH)
        self.play(FadeOut(lH), FadeOut(bmH), run_time=0.3)
        self.play(modo.animate.set_value(1.0), FadeIn(lH2), FadeIn(bmH2), run_time=0.6)                 # massas iguais
        self.foco = bv
        self.wait(1.2)
        inf = VGroup(mtex("M", WHITE_, 40), mtex(r"\to\infty", WHITE_, 40)).arrange(RIGHT, buff=0.08)
        inf.move_to(lH2.get_center())
        inf2 = VGroup(mtex("M", WHITE_, 36), mtex(r"\to\infty", WHITE_, 36)).arrange(RIGHT, buff=0.08).move_to(bmH)
        self.play(FadeOut(lH2), FadeOut(bmH2), run_time=0.3)
        self.play(modo.animate.set_value(2.0), FadeIn(inf), FadeIn(inf2), run_time=0.6)                   # muito pesada → ∞
        self.wait(1.2)
        lH3 = rot("2.000 kg", 30).move_to(inf.get_center())
        self.play(FadeOut(inf), FadeOut(inf2), run_time=0.3)
        self.play(modo.animate.set_value(0.0), FadeIn(lH3), FadeIn(bmH), run_time=0.5)
        self.ate(0.24)
        self.dica18(["NO REFERENCIAL DO CM, A ENERGIA SE", "DIVIDE NA RAZÃO INVERSA DAS MASSAS"])
        self.ate(0.42)
        self.play(FadeOut(bv), FadeOut(bmL), FadeOut(bmH), FadeOut(self.s1), op_p.animate.set_value(0.0), run_time=0.5)
        bv.clear_updaters()
        self.remove(bv, bmL, bmH, self.s1)
        self.s1 = None
        self.pilha.topo = TOPO_PILHA
        tit = VGroup(txt("VISTO DE UMA NAVE-MÃE A", 26, bold=True), rot("−10 m/s", 30, VEL)).arrange(RIGHT, buff=0.15)
        Q1 = linha_m("ANTES:", M(r"\tfrac12\cdot 3000\cdot 10^2", "=", N(r"150.000\ \mathrm{J}"), size=46, cores={2: KC})[0], size=24)
        Q2 = linha_m("DEPOIS:", M(r"\tfrac12\cdot 1000\cdot 12^2", size=46)[0])
        Q2b, _ = M(r"+\tfrac12\cdot 2000\cdot 9^2", "=", N(r"153.000\ \mathrm{J}"), size=46, cores={2: KC})
        for gl_ in (Q1[1][0][9:11], Q2[1][0][9:11], Q2b[0][10:11]):                    # §7: 10, 12 e 9 (m/s) dentro de ½·m·v² em violeta
            gl_.set_color(VEL)
        Q4 = linha_m("DIFERENÇA:", M(N(r"3.000\ \mathrm{J}"), size=48, cores={0: KC})[0])
        for m_ in (tit, Q1, Q2):
            self.pilha.poe(m_)
        self.pilha.poe(Q2b, dx=0.9)
        self.pilha.poe(Q4)
        self.play(FadeIn(tit), run_time=0.6)
        tau.set_value(1.0)
        self.referencial("DA NAVE-MÃE")
        modo_v.set_value(1.0)
        vv = vivo(lambda: VGroup(mrot("12 m/s", 28, VEL).next_to(P3(xs()[0] + 0.5 * KV * VEL_NAVE[1][0], YN - 1.4), DOWN, buff=0.3),
                                 mrot("9 m/s", 28, VEL).next_to(P3(xs()[1] + 0.5 * KV * VEL_NAVE[1][1], YN - 1.4), DOWN, buff=0.3)))
        self.play(FadeIn(vv), op_v.animate.set_value(1.0), run_time=0.6)
        self.ate(0.55)
        self.gat("cento e cinquenta mil joules")
        self.play(FadeIn(Q1), run_time=0.8)
        self.ate(0.66)
        self.play(FadeIn(Q2), run_time=0.7)
        self.ate(0.75)
        self.play(FadeIn(Q2b), run_time=0.6)
        self.ate(0.84)
        self.play(FadeIn(Q4), run_time=0.6)
        self.foco = Q4
        xb, yb2 = -4.3, -3.5                                                                            # v4: o painel mais baixo e à esquerda (longe das setas)
        base = Rectangle(width=0.9, height=1.1).move_to(P3(xb, yb2 + 0.55)).set_stroke(width=0).set_fill(mix(KC, 0.45), 0.7)
        corte = VGroup(Line(P3(xb - 0.55, yb2 + 0.5), P3(xb + 0.55, yb2 + 0.6)).set_stroke("#08122B", 7),
                       Line(P3(xb - 0.55, yb2 + 0.5), P3(xb + 0.55, yb2 + 0.6)).set_stroke(GEO, 1.5).shift(0.06 * UP),
                       Line(P3(xb - 0.55, yb2 + 0.5), P3(xb + 0.55, yb2 + 0.6)).set_stroke(GEO, 1.5).shift(0.06 * DOWN))
        rel = Rectangle(width=0.9, height=0.4).move_to(P3(xb, yb2 + 1.1 + 0.2)).set_stroke(WHITE_, 2).set_fill(KC, 1)
        cad = cadeado(False, 0.7).move_to(P3(xb - 0.95, yb2 + 0.5))
        lb = VGroup(txt("K DO CENTRO", 24), VGroup(txt("DE MASSA", 24), rot("150.000 J", 26, KC)).arrange(RIGHT, buff=0.16)).arrange(DOWN, buff=0.06, aligned_edge=LEFT) \
            .next_to(P3(xb + 0.5, yb2), RIGHT, buff=0.25).align_to(P3(0, yb2), DOWN)
        lr = VGroup(txt("K RELATIVA", 24), rot("3.000 J", 26, KC)).arrange(DOWN, buff=0.06, aligned_edge=LEFT).next_to(P3(xb + 0.5, yb2 + 1.3), RIGHT, buff=0.25)
        esc = VGroup(txt("ESCALA", 24, color=DIM), txt("DO PAINEL", 24, color=DIM)).arrange(DOWN, buff=0.06, aligned_edge=RIGHT) \
            .next_to(cad, LEFT, buff=0.3)                                                                     # v4 §6: junto das barras do painel
        self.play(FadeIn(base), FadeIn(corte), FadeIn(cad), FadeIn(lb), FadeIn(esc), run_time=0.8)
        self.play(FadeIn(rel, shift=0.15 * UP), FadeIn(lr), run_time=0.7)
        self.ate(0.97)
