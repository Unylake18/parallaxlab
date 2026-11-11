"""v4: fundo violeta + grade do eixo; 144 px/u. Lote PB1 · CHEGAR PERTO (v3: alvos 03–07; chapas B encaixadas, topo em y = 135 com placa, B1-5 novo (ponto de acumulação), sombras no papel a 240 px/u). Da v2: Layout B (140 px/u nos dois painéis): P vazado (o limite ignora o ponto); à direita a seta-alvo L⃗.
B1-2: X sai de (0,45; 0,35) e anda UMA vez em espiral até ~0,03 de P; contadores ‖X − P‖ e ‖F(X) − L‖ (E1: a seta nunca sai do painel, R6).
B1-3: ∀ε (disco ε = 1), ∃δ (disco δ cresce até 0,41), a MANCHA (imagem do disco δ, recalculada) e as duas metades da definição.
B1-4: δ = 0,7 vaza (ALERTA) e desce devagar até 0,41; ε 0,5 → δ 0,21; ε 0,25 → δ 0,10 (tabela). B1-5: o próprio P fica de fora; a definição.
B1-6 (layout A, 170 px/u): as sombras, as faixas, o quadrado e o disco √2·ε."""
from v28 import *  # noqa: F401,F403

VE, VD = VB(LAY_BE, 480, 540, 140), VB(LAY_BD, 1250, 560, 140)          # v4: 144 px/u, origens nos nós (480, 540) e (1260, 576)
ANG = 0.9
X0 = (0.45, 0.35)
TAB_X, TAB_Y = (1648, 1732), (364, 398, 434, 470)


def nomes_b(a="ONDE VOCÊ ANDA", b="ONDE A SETA CHEGA"):
    return VGroup(legenda(a, 480, 868, GEO, "center", 28), legenda(b, 1440, 868, GEO, "center", 28))


def seta_x(X, esc=.8, w=6, head=18):
    f = F_AULA(*X)
    m = math.hypot(*f)
    L = .84 * .5 * (.4 + .6 * min(1, m / 3.5)) * esc
    return seta7(VE.c2p(*X), VE.c2p(X[0] + f[0] / m * L, X[1] + f[1] / m * L), CAMPO2, w, head).set_z_index(9)


def metades(y=955):
    return (TC(r"\Xp\in A,\ \ 0<\|\Xp-\Pt\|<\del", 480, y, 40, "c"), TC(r"\Longrightarrow", 960, y, 44, "c"), TC(r"\|\F(\Xp)-\Lv\|<\eps", 1440, y, 40, "c"))


class LoteB1(Base):
    ANTES = None

    def corpo(self):
        # ── B1-1 · duas telas ──
        self.an("B1-1")
        self.secao("CHEGAR PERTO")
        zera_chapas()
        pE, pD = painel(130, 260, 700, 560, v=VE), painel(1090, 260, 700, 560, v=VD)
        zn = zona_px(120, 900, 1800, 1020, "linha de baixo B (B1)")
        st = {"X": None, "d": 0.0, "topo": False}
        cmp = campo28(VE, F_AULA, -2.25, 2.25, -1.75, 1.75, .5, rmin=0, mmax=3.5, ctx=True, nome="B1 campo da aula (contexto)")

        def teste():
            fs_ = [clar28([(-.85, -.5, -.45, .15)], [(0, 0, max(st["d"], .1) + .12)])]
            if st["d"] > .05:
                fs_.append(clar28([(-st["d"] - .45, -.15, -st["d"] - .05, .25)]))          # o rótulo δ anda com o disco
            if st["X"] is not None:
                X, Y = st["X"]
                fs_.append(clar28([(X - .2, Y + .15, X + .4, Y + .62)], [(X, Y, .12)]))
                f = F_AULA(X, Y)
                m = math.hypot(*f)
                fs_.append(clarSeg([((X, Y), (X + f[0] / m * .4, Y + f[1] / m * .4))], .22))
            if st["topo"]:
                fs_.append(lambda X, Y: Y > 1.5)
            return ou(*fs_)
        clareira(cmp, teste)
        P = anel7(VE.c2p(0, 0), POS, 9)
        lP = TP(r"\Pt", *canto_xy(VE, -.25, -.3), 36)
        self.play(FadeIn(pE), FadeIn(pD), FadeIn(zn), cresce_campo(cmp, 0.6), FadeIn(P, scale=0.5), FadeIn(lP), run_time=0.6)     # v4 R10: entra com a saída do NESTE VÍDEO
        nm = nomes_b()
        self.gat("é ali que você anda")
        self.play(FadeIn(nm[0], shift=0.06 * UP), run_time=0.5)
        org = ponto7(VD.c2p(0, 0), GEO, 6)
        sL = seta7(VD.c2p(0, 0), VD.c2p(1, 0), CAMPO2, 7, 24).set_z_index(9)
        lL = TP(r"\Lv", *canto_xy(VD, -.3, -.45), 32)
        self.gat("na da direita")
        self.play(FadeIn(org, scale=0.5), GrowArrow(sL), FadeIn(lL), run_time=0.8)
        self.gat("só onde a ponta dela chega")
        self.play(FadeIn(nm[1], shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)

        # ── B1-2 · X chega perto (espiral, uma vez); contadores ──
        self.an("B1-2")
        st["X"] = X0
        Xd = ponto7(VE.c2p(*X0), POS, 6, 10)
        aX = seta_x(X0)
        aFX = seta7(VD.c2p(0, 0), VD.c2p(*F_AULA(*X0)), CAMPO, 5, 20).set_z_index(8)
        lX = TP(r"\Xp", *canto_xy(VE, X0[0] + .05, X0[1] + .36), 30)
        f0 = F_AULA(*X0)
        lFX = TP(r"\F(\Xp)", *canto_xy(VD, f0[0] - .35, f0[1] + .3), 30)
        Xd.add_updater(lambda m: m.move_to(VE.c2p(*st["X"])))
        aX.add_updater(lambda m: m.become(seta_x(st["X"])))
        aFX.add_updater(lambda m: m.become(seta7(VD.c2p(0, 0), VD.c2p(*F_AULA(*st["X"])), CAMPO, 5, 20).set_z_index(8)))
        segue(lX, lambda: canto_xy(VE, st["X"][0] + .05, st["X"][1] + .36))
        segue(lFX, lambda: canto_xy(VD, F_AULA(*st["X"])[0] - .35, F_AULA(*st["X"])[1] + .3))
        guarda(self, aFX, PAINEL_D, "seta F(X)")
        guarda(self, aX, PAINEL_E, "seta de X")
        self.gat("conforme você chega perto")
        self.play(FadeIn(Xd, scale=0.5), GrowArrow(aX), GrowArrow(aFX), FadeIn(lX), FadeIn(lFX), run_time=0.8)
        print(f"[E1] X começa em {X0} (|X − P| = {math.hypot(*X0):.3f}); F(X) = ({f0[0]:.3f}; {f0[1]:.3f})")
        cX, vX = contador(r"\|\Xp-\Pt\|", POS, 480, 955, 36)
        cF, vF = contador(r"\|\F(\Xp)-\Lv\|", CAMPO2, 1440, 955, 36)
        r0, th0 = math.hypot(*X0), math.atan2(X0[1], X0[0])

        def atualiza_cont():
            X = st["X"]
            vX.set_value(math.hypot(*X))
            f = F_AULA(*X)
            vF.set_value(math.hypot(f[0] - 1, f[1]))
        atualiza_cont()
        def espiral_u(u):
            s_ = smooth(u)
            r = r0 * (1 - s_) + .03 * s_
            th = th0 + 2 * PI * s_
            st["X"] = (r * math.cos(th), r * math.sin(th))
            atualiza_cont()
        # v2 (holds): a espiral é UMA só, mais lenta, do "conforme" até "encolhe junto"; os contadores entram no meio dela
        t1 = max(1.0, self.falta("os dois números de baixo"))
        T = max(t1 + 3.0, self.falta("encolhe junto") + 1.0)
        u1 = t1 / T
        print(f"[B1-2] espiral única em {T:.1f} s (contadores aos {t1:.1f} s)")
        self.play(UpdateFromAlphaFunc(Xd, lambda m, a: espiral_u(u1 * a)), run_time=t1, rate_func=linear)
        self.play(FadeIn(cX), FadeIn(cF), UpdateFromAlphaFunc(Xd, lambda m, a: espiral_u(u1 + (1 - u1) * a)), run_time=T - t1, rate_func=linear)
        self.gat("então a definição vira um desafio")
        for m in (Xd, aX, aFX, lX, lFX):
            m.clear_updaters()
        self.play(FadeOut(cX), FadeOut(cF), FadeOut(Xd), FadeOut(aX), FadeOut(aFX), FadeOut(lX), FadeOut(lFX), run_time=0.5)
        self.remove(cX, cF, Xd, aX, aFX, lX, lFX)
        st["X"] = None
        self.ate(0.97)

        # ── B1-3 · ∀ε, ∃δ, a mancha (alvo 02) ──
        self.an("B1-3")
        ep_v, d_v = ValueTracker(1.0), ValueTracker(0.0)
        cE = vcirc(VD, 1.0, CAMPO2, 3, c=(1, 0)).set_z_index(6)
        lE = TP(r"\eps", *canto_xy(VD, 1 + .75 + .22, .75 + .2), 36)
        fa, fe = linha_partes([r"\forall\,\eps>0", r"\exists\,\del>0"], 960, 135, 44, gap=88)
        pfa, pfe = placa7(fa), placa7(fe)
        self.gat("um disquinho de raio épsilon")
        self.play(Create(cE), FadeIn(lE), run_time=1.0)
        cE.add_updater(lambda m: m.become(vcirc(VD, ep_v.get_value(), CAMPO2, 3, c=(1, 0)).set_z_index(6)))
        segue(lE, lambda: canto_xy(VD, 1 + ep_v.get_value() * .75 + .22, ep_v.get_value() * .75 + .2))
        guarda(self, cE, PAINEL_D, "disco ε")
        self.gat("qualquer épsilon pode ser escolhido")
        self.play(FadeIn(pfa), caneta(fa, ritmo=1.2))

        def disco_d():
            d = max(1e-3, d_v.get_value())
            g = VGroup(preenche(VE, circ_pts(d), DELTA_C, 1, 4), vcirc(VE, d, POS, 3).set_z_index(5))
            return g
        dD = disco_d()
        dD.add_updater(lambda m: m.become(disco_d()))
        lD = TP(r"\del", *canto_xy(VE, -.05 - .25, .05), 36)
        segue(lD, lambda: canto_xy(VE, -max(d_v.get_value(), .05) - .25, .05))

        def sync_d():
            st["d"] = d_v.get_value()
        self.add(dD)
        self.gat("depois é a sua vez")
        self.play(d_v.animate.set_value(0.41), FadeIn(lD), UpdateFromFunc(dD, lambda m: sync_d()), run_time=1.4)
        self.play(FadeIn(pfe), caneta(fe, ritmo=0.6))
        # o X de amostra (a 0,62·δ, ângulo 0,9), com a sua seta e o F(X)
        ang_v, fx_v = ValueTracker(ANG), ValueTracker(.62)
        Xa = lambda: (fx_v.get_value() * d_v.get_value() * math.cos(ang_v.get_value()), fx_v.get_value() * d_v.get_value() * math.sin(ang_v.get_value()))
        st["X"] = Xa()
        Xd = ponto7(VE.c2p(*st["X"]), POS, 6, 10)
        aX = seta_x(st["X"])
        aFX = seta7(VD.c2p(0, 0), VD.c2p(*F_AULA(*st["X"])), CAMPO, 5, 20).set_z_index(8)
        lX = TP(r"\Xp", *canto_xy(VE, st["X"][0] + .05, st["X"][1] + .36), 30)
        lFX = TP(r"\F(\Xp)", *canto_xy(VD, F_AULA(*st["X"])[0] - .35, F_AULA(*st["X"])[1] + .3), 30)

        def liga():
            Xd.add_updater(lambda m: m.move_to(VE.c2p(*Xa())))
            aX.add_updater(lambda m: m.become(seta_x(Xa())))
            aFX.add_updater(lambda m: m.become(seta7(VD.c2p(0, 0), VD.c2p(*F_AULA(*Xa())), CAMPO, 5, 20).set_z_index(8)))
            segue(lX, lambda: canto_xy(VE, Xa()[0] + .05, Xa()[1] + .36))
            segue(lFX, lambda: canto_xy(VD, F_AULA(*Xa())[0] - .35, F_AULA(*Xa())[1] + .3))
        self.gat("e olha o que acontece do outro lado")
        self.play(FadeIn(Xd, scale=0.5), GrowArrow(aX), GrowArrow(aFX), FadeIn(lX), FadeIn(lFX), run_time=0.8)
        liga()
        guarda(self, aFX, PAINEL_D, "seta F(X)")
        self.gat("cada ponto do seu disco")
        self.play(ang_v.animate.set_value(ANG + 2 * PI), run_time=3.0, rate_func=linear)      # uma volta: cada ponto do disco manda a ponta para um lugar
        dm = ValueTracker(0.0)
        man = Mancha(VD, lambda: dm.get_value(), lambda: ep_v.get_value())
        guarda(self, man, PAINEL_D, "mancha")
        lm = leg_mix(["A MANCHA = TODAS AS PONTAS QUE SAEM DO DISCO", r"$\delta$"], 1440, 300, GEO, "center", 26, up=True, gap=6)
        self.gat("formam uma mancha")
        self.add(man)
        man.add_updater(lambda m: m.atualiza())
        self.play(dm.animate.set_value(0.41), FadeIn(lm), run_time=1.4)
        man.clear_updaters()
        dm_lig = lambda: d_v.get_value()
        man.d_fn = dm_lig
        man.add_updater(lambda m: m.atualiza())
        print(f"[ε-δ] δ = 0,41, ε = 1: maior |F(X) − L| na borda da mancha = {man.atualiza().dist:.4f}")
        L1, L2, L3 = metades()
        self.gat("a pergunta é uma só")
        self.play(caneta(L1, ritmo=0.5))
        self.play(caneta(L2, ritmo=0.6))
        self.play(caneta(L3, ritmo=0.5))
        self.ate(0.97)

        # ── B1-4 · δ = 0,7 vaza; diminui; a tabela (alvo 03) ──
        self.an("B1-4")
        dl = TC(r"\del=", 430, 955, 40, "l", caneta=False)
        dn = NumBR(0.7, num_decimal_places=2, font_size=fs(40)).set_color(POS)
        dn.next_to(dl, RIGHT, buff=0.1)
        dn.add_updater(lambda m: m.set_value(round(d_v.get_value(), 2)))
        for g in dn.get_family():
            g._sem_contorno = True
        dg = VGroup(dl, dn).set_z_index(25)
        dg.shift(RIGHT * (PX(480, 0)[0] - dg.get_center()[0]))
        al = leg_mix(["ALGUMAS PONTAS ESCAPAM:", r"$\delta$", "GRANDE DEMAIS"], 1440, 962, ALERTA, "center", 30, up=True, gap=7)
        self.gat("com delta igual a zero vírgula sete")
        self.play(FadeOut(L1), FadeOut(L2), FadeOut(L3), run_time=0.35)
        self.remove(L1, L2, L3)
        self.play(d_v.animate.set_value(0.7), UpdateFromFunc(dD, lambda m: sync_d()), FadeIn(dg), run_time=1.2)
        print(f"[ε-δ] δ = 0,7: {100 * man.atualiza().frac_fora:.0f} % da borda fora, distância máxima {man.dist:.3f}")
        self.play(FadeIn(al, shift=0.06 * UP), run_time=0.5)
        self.gat("diminui o delta")
        self.play(d_v.animate.set_value(0.41), UpdateFromFunc(dD, lambda m: sync_d()), run_time=2.5)
        L1, L2, L3 = metades()
        self.gat("achou")
        self.play(FadeOut(al), FadeOut(dg), run_time=0.35)
        self.remove(al, dg)
        self.play(caneta(L1, ritmo=0.3), caneta(L2, ritmo=0.3), caneta(L3, ritmo=0.3))
        # tabela ε | δ no canto do painel direito
        tl = VGroup(Line(PX(1690, 348), PX(1690, 486)).set_stroke(WHITE_, 1.6), Line(PX(1612, 381), PX(1772, 381)).set_stroke(WHITE_, 1.6))
        for m in tl:
            m._sem_contorno = True
        cab = [TC(r"\eps", TAB_X[0], TAB_Y[0], 34, "c"), TC(r"\del", TAB_X[1], TAB_Y[0], 34, "c")]
        lin = [(r"1", r"0{,}41"), (r"0{,}5", r"0{,}21"), (r"0{,}25", r"0{,}10")]
        rows = [[TC(a, TAB_X[0], y, 34, "c"), TC(b, TAB_X[1], y, 34, "c")] for (a, b), y in zip(lin, TAB_Y[1:])]
        self.gat("se o desafio aperta para meio")
        self.play(Create(tl), caneta(cab[0], ritmo=0.5), caneta(cab[1], ritmo=0.5), run_time=0.8)
        self.play(caneta(rows[0][0], ritmo=0.4), caneta(rows[0][1], ritmo=0.4))
        self.play(ep_v.animate.set_value(0.5), d_v.animate.set_value(0.21), UpdateFromFunc(dD, lambda m: sync_d()), run_time=1.5)
        self.play(caneta(rows[1][0], ritmo=0.4), caneta(rows[1][1], ritmo=0.4))
        self.gat("para um quarto")
        self.play(ep_v.animate.set_value(0.25), d_v.animate.set_value(0.10), UpdateFromFunc(dD, lambda m: sync_d()), run_time=1.5)
        self.play(caneta(rows[2][0], ritmo=0.4), caneta(rows[2][1], ritmo=0.4))
        print(f"[ε-δ] ε = 0,25, δ = 0,10: maior |F(X) − L| = {man.atualiza().dist:.4f}")
        self.ate(0.97)

        # ── B1-5 · o próprio P fica de fora; a definição (alvo 04) ──
        self.an("B1-5")
        self.play(ep_v.animate.set_value(0.5), d_v.animate.set_value(0.21), UpdateFromFunc(dD, lambda m: sync_d()), run_time=1.0)
        st["topo"] = True
        fora = legenda("O PRÓPRIO P FICA DE FORA", 480, 300, POS, "center", 26)
        self.gat("o próprio ponto fica de fora")
        self.play(Transform(P, P.copy().scale(1.4), rate_func=there_and_back), FadeIn(fora, shift=0.06 * DOWN), run_time=0.9)
        self.gat("é o maior que zero")
        zero = VGroup(*[g for g in glifos(L1) if PX(398, 0)[0] < g.get_center()[0] < PX(478, 0)[0]])
        print(f"[B1-5] destaque do '0 <': {len(zero)} glifos")
        self.play(escala_ida_volta(zero, 1.25, 0.9))
        self.gat("o limite só olha para quem está chegando")
        self.play(fx_v.animate.set_value(.12), UpdateFromFunc(dD, lambda m: sync_d()), run_time=2.5)     # X chega perto de P, sem nunca ser P
        # ── v3 · o ponto de acumulação e o ponto isolado (alvo 05): as chapas ficam, o conteúdo troca ──
        for m in (Xd, aX, aFX, lX, lFX, cE, lE, dD, lD, man, cmp):
            m.clear_updaters()
        esq = [cmp, P, lP, dD, lD, Xd, aX, lX, fora]
        dir_ = [man, cE, lE, org, sL, lL, aFX, lFX, lm, tl, *cab, *[r_ for row in rows for r_ in row]]
        DOM = mix(CAMPO, CHAPA_F, 0.84).to_hex()
        A_ = circ_pts(1.45, (-.75, 0), 240)
        domA = VGroup(preenche(VE, A_, DOM, 1, 2), vlinha(VE, A_, CAMPO, 2, dash=(9, 8)).set_z_index(3))
        Pa = (.7, 0.0)
        anP = anel7(VE.c2p(*Pa), POS, 10, z=12)
        lPa = TP(r"\Pt", *canto_xy(VE, .95, -.78), 34)                 # v4: entre o 1º e o 2º círculo tracejado
        lA = TC("A", *canto_xy(VE, -1.35, .95), 40, "c")
        self.gat("nem precisa estar no domínio")
        self.play(*[FadeOut(m) for m in esq + [fa, fe, pfa, pfe]], run_time=0.5)
        self.remove(*esq, fa, fe, pfa, pfe)
        self.play(FadeIn(domA), FadeIn(anP, scale=0.6), FadeIn(lPa), caneta(lA, ritmo=0.6))
        discos, pts_ = [], []
        for r_, phi in ((1.0, 2.75), (.6, 2.95), (.3, 3.05)):
            discos.append(vlinha(VE, circ_pts(r_, Pa), POS, 2.5, dash=(7, 7)).set_z_index(6))
            pts_.append(ponto7(VE.c2p(Pa[0] + .72 * r_ * math.cos(phi), Pa[1] + .72 * r_ * math.sin(phi)), WHITE_, 6, 9))
        tdl = VGroup(legenda("TODO DISCO EM VOLTA DE P", 480, 265, BR, "center", 26), legenda("TEM PONTO DE A", 480, 302, BR, "center", 26))
        self.gat("tão perto dele quanto você quiser")
        for c_, p_ in zip(discos, pts_):
            self.play(Create(c_), FadeIn(p_, scale=0.5), run_time=0.45)
        self.play(FadeIn(tdl, shift=0.05 * UP), run_time=0.4)
        acu = TC(r"\Pt\ \text{de acumulação de } A:\quad \forall\,\del>0,\ \exists\,\Xp\in A,\ \ 0<\|\Xp-\Pt\|<\del", 960, 960, 38, "c")
        nmE = legenda("P: PONTO DE ACUMULAÇÃO", 480, 868, GEO, "center", 28)
        self.gat("o nome disso é ponto de acumulação")
        self.play(FadeOut(L1), FadeOut(L2), FadeOut(L3), FadeOut(nm[0]), FadeIn(nmE), run_time=0.4)
        self.remove(L1, L2, L3, nm[0])
        self.play(caneta(acu, ritmo=0.35))
        VQ = VB(LAY_BD, 1440, 540, 140)                 # v4: (1440, 540), nó da mesma grade do painel direito
        B_ = circ_pts(1.3, (-1.05, -.3), 240)               # o alvo usa raio 1,45 em (−1,45; −0,3), que passa da moldura da chapa (R7)
        domB = VGroup(preenche(VQ, B_, DOM, 1, 2), vlinha(VQ, B_, CAMPO, 2, dash=(9, 8)).set_z_index(3))
        Qp = (1.1, .85)
        dQ = VGroup(preenche(VQ, circ_pts(.5, Qp), mix(GEO, CHAPA_F, .9).to_hex(), 1, 4), vlinha(VQ, circ_pts(.5, Qp), POS, 2.5, dash=(7, 7)).set_z_index(5))
        pQ = ponto7(VQ.c2p(*Qp), CAMPO, 9, 9)
        lQ = TP("Q", *canto_xy(VQ, 1.1, 1.2), 32)
        lB = TC("A", *canto_xy(VQ, -1.6, .45), 40, "c")
        qso = VGroup(legenda("Q É DE A, MAS ESTÁ SOZINHO:", 1440, 265, BR, "center", 26), legenda("NINGUÉM CHEGA PERTO DELE", 1440, 302, BR, "center", 26))
        nmD = legenda("Q: PONTO ISOLADO", 1440, 868, GEO, "center", 28)
        self.gat("sozinho sem vizinhos")
        self.play(*[FadeOut(m) for m in dir_ + [nm[1]]], run_time=0.5)
        self.remove(*dir_, nm[1])
        self.play(FadeIn(domB), FadeIn(dQ), FadeIn(pQ, scale=0.5), FadeIn(lQ), caneta(lB, ritmo=0.6), FadeIn(qso, shift=0.05 * UP), FadeIn(nmD))
        print("[B1-5] P = (0,7; 0) na borda do disco aberto A (centro (−0,75; 0), raio 1,45): fora de A, e todo disco em volta de P toca A")
        acum = [domA, anP, lPa, lA, *discos, *pts_, tdl, nmE, acu, domB, dQ, pQ, lQ, lB, qso, nmD]
        top = TP(r"\lim\limits_{\Xp\to\Pt}\F(\Xp)=\Lv\iff\forall\,\eps>0\ \ \exists\,\del>0:", 960, 135, 42, "c", caneta=True)
        L1, L2, L3 = metades()
        self.gat("agora sim escrito")
        fx_v.set_value(.62)                 # o X de amostra volta à posição do alvo 06 antes de reaparecer
        Xd.move_to(VE.c2p(*Xa()))
        aX.become(seta_x(Xa()))
        aFX.become(seta7(VD.c2p(0, 0), VD.c2p(*F_AULA(*Xa())), CAMPO, 5, 20).set_z_index(8))
        lX.move_to(PX(*canto_xy(VE, Xa()[0] + .05, Xa()[1] + .36)))
        lFX.move_to(PX(*canto_xy(VD, F_AULA(*Xa())[0] - .35, F_AULA(*Xa())[1] + .3)))
        self.play(*[FadeOut(m) for m in acum], *[FadeIn(m) for m in esq + dir_ + [nm[0], nm[1]]], run_time=0.5)
        self.remove(*acum)
        self.play(FadeIn(top[0]), caneta(top.f, ritmo=1.2))
        self.play(caneta(L1, ritmo=0.3), caneta(L2, ritmo=0.3), caneta(L3, ritmo=0.3))
        self.gat("a metade da esquerda")
        self.play(escala_ida_volta(L1, 1.08, 0.9))
        self.gat("a da direita")
        self.play(escala_ida_volta(L3, 1.08, 0.9))
        self.ate(0.97)
        for m in (Xd, aX, aFX, lX, lFX, cE, lE, dD, lD, man, dn, cmp):
            m.clear_updaters()

        # ── B1-6 · o atalho: sombras e faixas (v3 alvo 07; PAPEL a 240 px/u, as faixas nas linhas grossas) ──
        self.an("B1-6")
        V = Vista(600, 540, 240)
        gB17 = grade_v(V, None, "B1-7 sombras (tela cheia, 240 px/u)")
        for xx in (360, 840):
            ALINHA.append(("faixa", "borda vertical |x| = ε", xx, 180, xx, 900))
        for yy in (300, 780):
            ALINHA.append(("faixa", "borda horizontal |y| = ε", 120, yy, 1080, yy))
        sai = self.snap()
        zA = zona_px(1080, 180, 1920, 1020, "coluna (B1-7)")
        disco = vcirc(V, 1, CAMPO2, 3).set_z_index(6)
        pL = ponto7(V.c2p(0, 0), CAMPO2, 8, 9)
        lpL = TP(r"\text{ponta de }\Lv", *canto_xy(V, -.55, -.32), 28)
        T_ = (.55, .6)
        pT = ponto7(V.c2p(*T_), CAMPO, 9, 10)
        lT = TP(r"\F(\Xp)", *canto_xy(V, T_[0] + .5, T_[1] - .3), 28)         # v4: longe do |Q − L₂| < ε
        self.gat("e tem um atalho")
        zera_chapas()
        self.play(*[FadeOut(m) for m in sai], FadeIn(zA), FadeIn(gB17), Create(disco), FadeIn(pL), FadeIn(lpL), FadeIn(pT, scale=0.5), FadeIn(lT), run_time=0.9)
        self.remove(*sai)
        sh = seta7(V.c2p(0, 0), V.c2p(T_[0], 0), E1, 5, 16).set_z_index(9)
        sv = seta7(V.c2p(0, 0), V.c2p(0, T_[1]), E2, 5, 16).set_z_index(9)
        dh = vlinha(V, [T_, (T_[0], 0)], E1, 2, dash=(5, 6)).set_z_index(7)
        dv = vlinha(V, [T_, (0, T_[1])], E2, 2, dash=(5, 6)).set_z_index(7)
        c1 = TC(r"\|\F-\Lv\|<\eps\ \Rightarrow\ |\Pp-L_1|<\eps\ \text{e}\ |\Qq-L_2|<\eps", 1130, 300, 34)
        self.gat("as duas sombras dela")
        self.play(Create(dh), Create(dv), GrowArrow(sh), GrowArrow(sv), run_time=0.9)
        self.gat("ficam a menos de épsilon")
        self.play(caneta(c1, ritmo=0.22))
        fv = faixa(V, [(-1, -1.5), (1, -1.5), (1, 1.5), (-1, 1.5)])
        fh = faixa(V, [(-2, -1), (2, -1), (2, 1), (-2, 1)])
        fq = faixa(V, [(-1, -1), (1, -1), (1, 1), (-1, 1)], FAIXA2, 1.5)
        bordas = VGroup(*[vlinha(V, s_, GEO, 2, dash=(8, 8)).set_z_index(2) for s_ in (((-1, -1.5), (-1, 1.5)), ((1, -1.5), (1, 1.5)), ((-2, -1), (2, -1)), ((-2, 1), (2, 1)))])
        lfp = TP(r"|\Pp-L_1|<\eps", *canto_xy(V, 0, 1.3), 30)
        lfq = TP(r"|\Qq-L_2|<\eps", *canto_xy(V, 1.55, .78), 30)
        le = TP(r"\eps", *canto_xy(V, -.55, .8), 36)
        self.gat("o contrário também vale")
        self.play(FadeIn(fv), FadeIn(fh), Create(bordas), FadeIn(lfp), FadeIn(lfq), FadeIn(le), run_time=1.0)
        self.gat("a ponta cai num quadrado")
        self.play(FadeIn(fq), run_time=0.6)
        r2 = vcirc(V, math.sqrt(2), GEO, 2, dash=(6, 8)).set_z_index(5)
        lr2 = TP(r"\sqrt2\,\eps", *canto_xy(V, -1.22, 1.12), 28)
        c2 = TC(r"|\Pp-L_1|<\eps\ \text{e}\ |\Qq-L_2|<\eps\ \Rightarrow\ \|\F-\Lv\|<\sqrt2\,\eps", 1130, 410, 34)
        self.gat("um pouquinho maior")
        self.play(Create(r2), FadeIn(lr2), run_time=0.8)
        self.play(caneta(c2, ritmo=0.18))
        c3 = TC(r"\lim\F=\Lv\iff\lim\Pp=L_1\ \text{e}\ \lim\Qq=L_2", 1130, 560, 36)
        self.gat("então o limite de um campo existe")
        self.play(caneta(c3, ritmo=0.5))
        ctl = legenda("CONTROLAR A SETA = CONTROLAR AS DUAS SOMBRAS", 1134, 680, GEO)
        self.gat("o limite de cada componente existe")
        self.play(FadeIn(ctl, shift=0.06 * UP), run_time=0.5)
        self.ate(0.97)
        self.sai_fim()
