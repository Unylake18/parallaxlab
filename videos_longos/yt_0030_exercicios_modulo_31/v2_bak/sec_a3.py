"""Lote PA3 · A3 POR QUE UM SOBRE A DISTÂNCIA · v2 (alvos v2_a3p, v2_a3s + 26, 27 v1). Fio: circunferências, o raio r, B em caneta. A fórmula do
D3 volta (lembrança, DO TERCEIRO DEGRAU), v → B por glyph map; 2 − 2α = 0 → 2 = 2α (o 2α atravessa) → α = 1; ‖B‖ = r/r^{2α} = 1/r e o gráfico.
Fio carregado: rot → div por glyph map. Carga: E = X/‖X‖^p; ∂‖X‖/∂x = x/‖X‖; a parcela pela regra do produto e da cadeia (x/‖X‖ voa); as três
parcelas por cópia; a soma; x² + y² + z² → ‖X‖²; R14 no ‖X‖²; (3 − p)/‖X‖^p. p = 3 ⇒ 1/r²; COULOMB · GRAVITAÇÃO; o gráfico 1/r² × 1/r. Fecho."""
from alg30 import *  # noqa: F401,F403

PTS = [(X, Y) for X in np.arange(-3.5, 3.5 + 1e-6, .5) for Y in np.arange(-2.5, 2.5 + 1e-6, .5)
       if math.hypot(X, Y) >= .5 and not (-3.9 - .25 < X < -1.2 + .25 and -2.95 - .25 < Y < -2.45 + .25)]
MM = interp_tab([(.3, 2.2), (1, 2.0)])
NX = r"\|X\|"


def grafico(rot_="|B|", gy=850, dupla=False):
    gx, gw, gh = 1130, 600, 170
    ax = VMobject().set_points_as_corners([PX(gx, gy - gh), PX(gx, gy), PX(gx + gw, gy)]).set_stroke(GEO, 2 / 1.2, 1).set_fill(opacity=0)
    ax._sem_contorno = True
    g = VGroup(ax)
    curvas = [(lambda r: 1 / (r * r), CAMPO2, None)] + ([(lambda r: 1 / r, GEO, (8, 8))] if dupla else []) if dupla else [(lambda r: 1 / r, CAMPO2, None)]
    for f, cor, dash in curvas:
        pts = []
        for i in range(201):
            r = .35 + i / 200 * 3.65
            pts.append(PX(gx + (r / 4) * gw, gy - min(f(r), 2.6) / 2.6 * gh))
        g.add(linha7(pts, cor, 4 if dash is None else 2, 1.0, dash))
    lb = T(rot_, gx - 10, gy - gh - 12, 24, "right", GEO, bold=False, up=False)
    ld = T("distância", gx + gw, gy + 34, 24, "right", GEO, bold=False, up=False)
    g.add(lb, ld)
    return g.set_z_index(20), lb


def fio():
    d = preenche(VA, circ_pts(.22), "#0F0C26", 1.0, 10)
    r = vcirc(VA, .22, BR, 3).set_z_index(11)
    p = ponto7(VA.c2p(0, 0), BR, 5, 12)
    return VGroup(d, r, p)


class LoteA3(Base):
    ANTES = "APLICAÇÃO · MAPAS QUE NÃO ENTORTAM"

    def corpo(self):
        # ── A3-1 · o fio ──
        self.an("A3-1")
        self.secao("APLICAÇÃO · POR QUE UM SOBRE A DISTÂNCIA")
        zera_chapas()
        chA = chapa_px(*LA, nome="A3 palco", v=VA)
        fi = fio()
        lf = TXP30("FIO COM CORRENTE", *canto_xy(VA, -2.55, -2.62), 24, "center", GEO)
        cmp = CampoVivo(VA, PTS, VORTA, MM, .5, p0=1.0, nome="A3 B_α")
        troca(self, "A4 → A3 (palco com o fio)")
        self.play(FadeIn(chA), FadeIn(fi), FadeIn(lf), run_time=0.6)
        self.gat("as linhas do campo magnético")
        self.play(cresce_campo(cmp, 0.8))
        self.gat("pausa e pensa")
        self.pausa()
        self.ate(1.0)

        # ── A3-2 · a simetria e Ampère ──
        self.an("A3-2")
        circs = VGroup(*[linha_rec(VA, circ_pts(r), LA, GEO, 2, .35, dash=(8, 9)) for r in (1, 2)])
        raio = vlinha(VA, [(0, 0), (2 * math.cos(2.5), 2 * math.sin(2.5))], GEO, 3).set_z_index(8)
        rl = rot("r", *canto_xy(VA, -1.25, 1.25), 28)          # centro de uma célula da rede (R5: fora das setas), ao lado do raio
        self.gat("o campo dá a volta no fio")
        self.play(Create(circs), run_time=0.8)
        self.gat("e o tamanho só depende da distância")
        self.play(Create(raio), FadeIn(rl[0]), run_time=0.5)
        escreve(self, rl.f, 0.5, rt=0.3)
        BB = L([("B", r"\B="), ("fr", r"\dfrac{(-\Y,\ \X)}{(\X^2+\Y^2)^{\alpha}}")], 1120, 280, 40)
        self.gat("supondo uma lei de potência")
        BB._origem = "a"
        self.play(troca_p(cmp, .3, 1.0), caneta(BB, ritmo=0.3), run_time=1.4)
        nB, dB = num_den(BB.p("fr"))                             # R16: numerador e denominador citados acendem na fala
        self.gat("menos a coordenada vertical")
        acende(self, [VGroup(*nB)], CAMPO2, 1.0)
        self.gat("elevada a um expoente alfa")
        acende(self, [VGroup(*dB)], AMB, 1.0)
        am = legenda("FORA DO FIO (AMPÈRE):", 1124, 380, GEO, "left", 26)
        self.gat("a lei de ampère diz")
        self.play(FadeIn(am, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── A3-3 · a fórmula guardada; α = 1 (alvo 26 v1) ──
        self.an("A3-3")
        RV = L([("rot", r"\V{\rot\vv}="), ("fr", r"\V{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}")], 1120, 470, 38)
        tg = legenda("DO TERCEIRO DEGRAU", 1124, 550, GEO, "left", 24)
        RV._origem = "lembrança"
        print(f"[origem] lembrança {self.lote} A3-3 {self.t:.2f} {RV._tex!r} (a linha final do D3, no mesmo estilo)")
        self.gat("agora usa a fórmula que a gente guardou")
        self.play(FadeIn(RV), FadeIn(tg), run_time=0.6)
        RB = L([("rot", r"\V{\rot\B}="), ("fr", r"\V{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}")], 1120, 470, 38)
        gm(self, RV, RB, rt=0.6)
        N0 = L([("2", "2"), ("m", "-"), ("a", r"2\alpha"), ("z", "=0")], 1120, 590, 36)
        self.gat("o numerador zera")
        voa(self, VGroup(*num_den(RB.p("fr"))[0]), N0.p("2", "m", "a"), rt=0.5)
        escreve_p(self, N0, ["z"], 0.4)
        junta(self, N0, "b")
        N1 = L([("2", "2"), ("e", "="), ("a", r"2\alpha")], 1120, 590, 36)
        self.gat("dois igual a dois alfa")
        gm(self, N0, N1, rt=0.8, ka=["2", "m", "a", "e"], kb=["2", "e", "a"], nota="(2α atravessa o =)")
        N2 = L([("2", "2"), ("e", "="), ("a", r"2\alpha"), ("i", r"\ \Rightarrow\ "), ("al", r"\alpha=1")], 1120, 590, 36)
        self.gat("e alfa igual a um")
        gm(self, N1, N2, rt=0.5, extra=[troca_p(cmp, 1.0, 0.5)])
        NB = L([("n", r"\|\B\|="), ("a", r"\dfrac{r}{r^{2\alpha}}"), ("b", r"=\dfrac{r}{r^2}"), ("c", r"=\dfrac1r")], 1120, 690, 40)
        self.gat("então o tamanho do campo")
        escreve_p(self, NB, ["n", "a"], 0.25)
        self.gat("a distância dividida pela distância ao quadrado")
        escreve_p(self, NB, ["b"], 0.25)
        self.gat("um sobre a distância o campo")
        escreve_p(self, NB, ["c"], 0.25)
        junta(self, NB)
        gf, lbB = grafico("|B|", gy=880)
        self.gat("o campo do fio cai")
        self.play(Create(gf[0]), Create(gf[1]), FadeIn(gf[2]), FadeIn(gf[3]), FadeOut(tg), run_time=0.8)
        self.remove(tg)
        self.ate(1.0)

        # ── A3-4 · o fio carregado ──
        self.an("A3-4")
        lc = TXP30("FIO CARREGADO", *canto_xy(VA, -2.55, -2.62), 24, "center", GEO)
        EE = L([("B", r"\E="), ("fr", r"\dfrac{(\X,\ \Y)}{(\X^2+\Y^2)^{\alpha}}")], 1120, 280, 40)
        ga = legenda("FORA DO FIO (GAUSS):", 1124, 380, GEO, "left", 26)
        self.gat("faz o mesmo com um fio carregado")
        self.play(FadeOut(lf), FadeIn(lc), run_time=0.4)
        self.remove(lf)
        self.gat("o campo elétrico aponta para fora")
        gm(self, BB, EE, rt=1.0, extra=[gira_setas(cmp, -PI / 2, 1.0), FadeOut(am), FadeIn(ga), FadeOut(circs), FadeOut(raio), FadeOut(rl)])
        self.remove(am, circs, raio, rl)
        DE = L([("rot", r"\D{\dv\E}="), ("fr", r"\D{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}"), ("z", r"=0\ \Rightarrow\ \alpha=1")], 1120, 470, 38)
        self.gat("divergente dois menos dois alfa")
        AB = Duas(RB, N2)
        AB.ks = ["rot", "fr"] + ["z", "z", "z", "z", "z"]
        gm(self, AB, DE, rt=0.9, nota="(rot → div)")
        self.remove(RB, N2)
        NE = L([("n", r"\|\E\|="), ("a", r"\dfrac{r}{r^{2\alpha}}"), ("b", r"=\dfrac{r}{r^2}"), ("c", r"=\dfrac1r")], 1120, 690, 40)
        lbE = T("|E|", lbB.get_right()[0] * 120 + 960, 880 - 170 - 12, 24, "right", GEO, bold=False, up=False)
        self.gat("alfa um e o campo também cai")
        gm(self, NB, NE, rt=0.6, extra=[FadeOut(lbB), FadeIn(lbE)])
        self.remove(lbB)
        self.ate(1.0)

        # ── A3-5 · a carga no espaço (alvos v2_a3p e v2_a3s) ──
        self.an("A3-5")
        cg = VGroup(preenche(VA, circ_pts(.32), CARGA, 1.0, 10), T("+", *canto_xy(VA, 0, -.2), 36, "center").set_z_index(12))
        cc = campo30(VA, F_CARGA, rmin=.6, mmax=1, skip=clar28([(-3.9, -2.95, -1.4, -2.45)]), nome="A3 carga (corte)")
        lco = TXP30("CORTE PELO PLANO", *canto_xy(VA, -2.65, -2.62), 24, "center", GEO)
        col = [EE, ga, DE, NE, gf[0], gf[1], gf[3], lbE]
        EP = L([("E", r"\E="), ("fr", r"\dfrac{X}{" + NX + "^{p}}"), ("x", r",\quad X=(\X,\ \Y,\ \Z)")], 1120, 270, 36)
        self.gat("e uma carga pontual")
        self.secao("APLICAÇÃO · POR QUE UM SOBRE A DISTÂNCIA AO QUADRADO")
        self.play(*[FadeOut(m) for m in col + [fi, lc]], FadeOut(cmp), FadeIn(cg), cresce_campo(cc, 0.8), FadeIn(lco), run_time=0.8)
        self.remove(*col, fi, lc, cmp)
        self.gat("escreve o campo como o vetor posição")
        escreve(self, EP, 0.25)
        DN = L([("d", r"\dfrac{\partial" + NX + r"}{\dx}"), ("e", "="), ("r", r"\dfrac{\X}{" + NX + "}")], 1120, 380, 34)
        PA = L([("d", r"\dfrac{\partial}{\dx}\Big(\dfrac{\X}{" + NX + r"^{p}}\Big)="), ("t1", r"\dfrac{1}{" + NX + r"^{p}}"), ("m", r"+\X\cdot\big(-p\," + NX + r"^{-p-1}\big)\cdot"),
                ("r", r"\dfrac{\X}{" + NX + "}")], 1120, 510, 32)
        self.gat("faz a conta de uma parcela")
        escreve_p(self, PA, ["d"], 0.2)
        self.gat("a derivada da distância nessa direção")
        escreve(self, DN, 0.25)
        self.gat("então dá um sobre a distância")
        escreve_p(self, PA, ["t1", "m"], 0.15)
        voa(self, DN.p("r"), PA.p("r"), rt=0.5)
        junta(self, PA, "b")
        PB = L([("e", "="), ("t1", r"\dfrac{1}{" + NX + r"^{p}}"), ("t2", r"-\dfrac{p\,\X^2}{" + NX + r"^{p+2}}")], 1150, 640, 34)
        self.gat("menos o expoente vezes o quadrado")
        gm(self, PA, PB, rt=0.8, copia=True, ka=["x", "t1", "t2", "t2"])
        lg = legenda("REGRA DO PRODUTO · REGRA DA CADEIA", 1124, 740, GEO, "left", 26)
        self.play(FadeIn(lg, shift=0.05 * UP), run_time=0.3)
        # as três parcelas (alvo v2_a3s)
        Px = L([("d", r"\dfrac{\partial}{\dx}\Big(\dfrac{\X}{" + NX + r"^{p}}\Big)="), ("t1", r"\dfrac{1}{" + NX + r"^{p}}"), ("t2", r"-\dfrac{p\,\X^2}{" + NX + r"^{p+2}}")], 1120, 270, 30)
        self.gat("as outras parcelas são iguais")
        AF = Duas(EP, DN, PA, PB)
        AF.ks = ["x"] * (3 + 3) + ["d", "x", "x", "x"] + ["x", "t1", "t2"]
        gm(self, AF, Px, rt=0.8, nota="(fusão)", extra=[FadeOut(lg)])
        self.remove(EP, DN, PA, PB, lg)
        Py = L([("d", r"\dfrac{\partial}{\dy}\Big(\dfrac{\Y}{" + NX + r"^{p}}\Big)="), ("t1", r"\dfrac{1}{" + NX + r"^{p}}"), ("t2", r"-\dfrac{p\,\Y^2}{" + NX + r"^{p+2}}")], 1120, 365, 30)
        Pz_ = L([("d", r"\dfrac{\partial}{\partial\Z}\Big(\dfrac{\Z}{" + NX + r"^{p}}\Big)="), ("t1", r"\dfrac{1}{" + NX + r"^{p}}"), ("t2", r"-\dfrac{p\,\Z^2}{" + NX + r"^{p+2}}")],
                 1120, 460, 30)
        em_paralelo(self, 0.8, lambda: gm(self, Px, Py, copia=True), lambda: gm(self, Px, Pz_, copia=True))
        SM = L([("dv", r"\D{\dv\E}="), ("t1", r"\dfrac{3}{" + NX + r"^{p}}"), ("t2", r"-\dfrac{p\,(\X^2+\Y^2+\Z^2)}{" + NX + r"^{p+2}}")], 1120, 575, 32)
        self.gat("agora soma")
        A3_ = Duas(Px, Py, Pz_)
        A3_.ks = ["dv", "t1", "t2"] * 3
        gm(self, A3_, SM, rt=0.9, copia=True, nota="(as três parcelas voam para a soma)")
        self.add(Px, Py, Pz_)
        S2 = L([("e", "="), ("t1", r"\dfrac{3}{" + NX + r"^{p}}"), ("m", r"-\dfrac{p\,", 2), ("n2", NX + r"^2"), ("sl", "}{", 1), ("dp", NX + r"^{p}"), ("d2", NX + r"^{2}"),
                ("fc", "}", 0)], 1150, 690, 32)
        self.gat("os quadrados das coordenadas somam")
        gm(self, SM, S2, rt=0.8, copia=True, ka=["x", "t1", "n2"], kb=["e", "t1", "n2", "n2", "n2", "n2", "n2", "n2"])
        self.gat("que cancela o mais dois")
        tr = cancela(self, S2, "n2", "d2", rt=0.25)
        S3 = L([("e", "="), ("t1", r"\dfrac{3}{" + NX + r"^{p}}"), ("m", r"-\dfrac{p\,", 2), ("n2", NX + r"^2"), ("sl", "}{", 1), ("dp", NX + r"^{p}"), ("d2", NX + r"^{2}"),
                ("fc", "}", 0),
                ("r", r"=\D{\dfrac{3-p}{" + NX + r"^{p}}}")], 1150, 690, 32)
        for g in S3.p("n2", "d2"):
            g.set_color(CORAL_C)
        self.gat("sobra o número de parcelas")
        gm(self, S2, S3, rt=0.6)
        np_ = leg_mix(["NO PLANO: 2 PARCELAS ", r"$\Rightarrow$", " (2 − p)"], 1124, 800, GEO, "left", 26)
        self.gat("no plano são duas parcelas")
        self.play(FadeIn(np_, shift=0.05 * UP), run_time=0.4)
        self.gat("o divergente no espaço é três")                 # R16: o resultado citado acende
        acende(self, [S3.p("r")], SAIC, 1.0)
        DF = L([("dv", r"\D{\dv\E}="), ("r", r"\D{\dfrac{3-p}{" + NX + r"^{p}}}")], 1120, 270, 36)
        self.gat("para zerar o expoente é três")
        AD = Duas(Px, Py, Pz_, SM, S3)
        AD.ks = ["x"] * 9 + ["dv", "x", "x"] + ["x"] * 8 + ["r"]
        gm(self, AD, DF, rt=0.8, nota="(fusão)", extra=[FadeOut(np_), *[FadeOut(t) for t in tr]])
        self.remove(Px, Py, Pz_, SM, S3, np_, *tr)
        P3 = L([("p", r"p=3\ \Rightarrow\ "), ("n", r"\|\E\|=\dfrac{r}{r^3}=\dfrac1{r^2}")], 1120, 370, 38)
        escreve(self, P3, 0.25)
        cl = [legenda("COULOMB", 1124, 450, GEO, "left", 26), legenda("· GRAVITAÇÃO", 1290, 450, GEO, "left", 26)]
        gf2, _ = grafico("|E|", gy=700, dupla=True)
        self.gat("a de coulomb")
        self.play(FadeIn(cl[0]), Create(gf2[0]), Create(gf2[1]), Create(gf2[2]), FadeIn(gf2[3]), FadeIn(gf2[4]), run_time=0.6)
        self.gat("e a da gravitação")
        self.play(FadeIn(cl[1]), run_time=0.3)
        self.ate(1.0)

        # ── A3-6 · o fecho: quatro linhas, no máximo duas de cada vez ──
        self.an("A3-6")
        F1 = [legenda("NO PLANO: 2 · NO ESPAÇO: 3", 1124, 790, BR, "left", 26), legenda("O EXPOENTE VEM DA DIMENSÃO", 1124, 835, GEO, "left", 26)]
        F2_ = [leg_mix(["LEI FÍSICA: rot = 0 OU div = 0 FORA DA FONTE"], 1124, 790, BR, "left", 26),
               leg_mix(["+ SIMETRIA ", r"$\Rightarrow$", " NÃO SOBRA ESCOLHA"], 1124, 835, CORAL, "left", 26)]
        sim = legenda("CÍRCULOS EM VOLTA DO FIO · RADIAL EM VOLTA DA CARGA", 1124, 880, GEO, "left", 24)
        self.gat("no plano o número que aparece")
        self.play(FadeIn(F1[0], shift=0.05 * UP), run_time=0.4)
        self.gat("o expoente da lei vem da dimensão")
        self.play(FadeIn(F1[1], shift=0.05 * UP), run_time=0.4)
        self.gat("tem mais lugar para se espalhar")              # R16: a lei 1/r² citada acende
        acende(self, [P3.p("n")], CAMPO2, 1.0)
        self.gat("é a lei física")
        self.play(FadeOut(F1[0]), FadeIn(F2_[0], shift=0.05 * UP), run_time=0.4)
        self.remove(F1[0])
        self.gat("junto com a simetria")
        self.play(FadeOut(F1[1]), FadeIn(F2_[1], shift=0.05 * UP), run_time=0.4)
        self.remove(F1[1])
        self.gat("as linhas em círculo em volta do fio")
        self.play(FadeOut(F2_[0]), FadeIn(sim, shift=0.05 * UP), run_time=0.4)
        self.remove(F2_[0])
        self.sai_fim()
