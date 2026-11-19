"""Lote PA3 · A3 POR QUE UM SOBRE A DISTÂNCIA · v2 (alvos v2_a3p, v2_a3s + 26, 27 v1). Fio: circunferências, o raio r, B em caneta. A fórmula do
D3 volta (lembrança, DO TERCEIRO DEGRAU), v → B por glyph map; 2 − 2α = 0 → 2 = 2α (o 2α atravessa) → α = 1; ‖B‖ = r/r^{2α} = 1/r e o gráfico.
Fio carregado: rot → div por glyph map. Carga: E = X/‖X‖^p; ∂‖X‖/∂x = x/‖X‖; a parcela pela regra do produto e da cadeia (x/‖X‖ voa); as três
parcelas por cópia; a soma; x² + y² + z² → ‖X‖²; R14 no ‖X‖²; (3 − p)/‖X‖^p. p = 3 ⇒ 1/r²; COULOMB · GRAVITAÇÃO; o gráfico 1/r² × 1/r. Fecho."""
from alg30 import *  # noqa: F401,F403

PTS = [(X, Y) for X in np.arange(-3.5, 3.5 + 1e-6, .5) for Y in np.arange(-2.5, 2.5 + 1e-6, .5)
       if math.hypot(X, Y) >= .5 and not (-3.9 - .25 < X < -1.2 + .25 and -2.95 - .25 < Y < -2.45 + .25)]
MM = interp_tab([(.3, 2.2), (1, 2.0)])
NX = r"\|X\|"


def grafico(rot_="|B|", gy=850, dupla=False, gh=170):
    gx, gw = 1130, 600
    ax = VMobject().set_points_as_corners([PX(gx, gy - gh), PX(gx, gy), PX(gx + gw, gy)]).set_stroke(GEO, 2 / 1.2, 1).set_fill(opacity=0)
    ax._sem_contorno = True
    g = VGroup(ax)
    curvas = [(lambda r: 1 / (r * r), CAMPO2, None)] + ([(lambda r: 1 / r, GEO, (8, 8))] if dupla else []) if dupla else [(lambda r: 1 / r, CAMPO2, None)]
    for f, cor, dash in curvas:
        r0 = 1 / 2.6 if abs(f(.5) - 2.0) < 1e-9 else 1 / math.sqrt(2.6)      # C5: a curva começa onde f(r) = 2,6 (nunca achatada no teto)
        pts = []
        for i in range(201):
            r = r0 + i / 200 * (4.0 - r0)
            pts.append(PX(gx + (r / 4) * gw, gy - f(r) / 2.6 * gh))
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
        self.gat("as linhas do campo magnético")                   # v3 §1.3: o campo nasce do fio para fora, em anéis
        self.play(cresce_campo(cmp, 1.2, chave=lambda s: math.hypot(*s._xy)))
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
        FR = [("fa", r"\V{\dfrac{", 0), ("nu", r"2-2\alpha"), ("fb", "}{", 1), ("de", r"(\X^2+\Y^2)^{\alpha}"), ("fc", "}}", 0)]
        RV = L([("rot", r"\V{\rot\vv}=")] + FR, 1120, 470, 38)
        tg = legenda("DO TERCEIRO DEGRAU", 1124, 550, GEO, "left", 24)
        RV._origem = "lembrança"
        print(f"[origem] lembrança {self.lote} A3-3 {self.t:.2f} {RV._tex!r} (a linha final do D3, no mesmo estilo)")
        self.gat("agora usa a fórmula que a gente guardou")
        self.play(FadeIn(RV), FadeIn(tg), run_time=0.6)
        RB = L([("rot", r"\V{\rot\B}=")] + FR, 1120, 470, 38)
        gm(self, RV, RB, rt=0.6)
        # v3 §3 #4: rot B = (2 − 2α)/(…)^α = 0 → 2 − 2α = 0 → 2 = 2α → α = 1 (três glyph maps; o "= 0" fica)
        RB0 = L([("rot", r"\V{\rot\B}=")] + FR + [("z", "=0")], 1120, 470, 38)
        self.gat("para ser zero")
        gm(self, RB, RB0, rt=0.5)
        DEN = L([("d", r"(\X^2+\Y^2)^{\alpha}"), ("g", r">0")], 1480, 548, 32)       # v4 C19: o denominador nunca é zero (à direita da legenda DO TERCEIRO DEGRAU)
        self.gat("olha o denominador")
        voa(self, RB0.p("de"), DEN.p("d"), rt=0.5)
        escreve_p(self, DEN, ["g"], 0.2)
        junta(self, DEN, "b")
        N0 = L([("nu", r"2-2\alpha"), ("z", "=0")], 1120, 615, 36)
        self.gat("o numerador zera")
        gm(self, RB0, N0, rt=0.7, copia=True, ka=["x", "x", "nu", "x", "x", "x", "z"], extra=[FadeOut(DEN)], nota="(o numerador voa, o denominador sai, o = 0 fica)")
        self.remove(DEN)
        N0.ks, N0._rg = ["2", "m", "a", "z"], [N0._rg[0][:1], N0._rg[0][1:2], N0._rg[0][2:], N0._rg[1]]
        self.gat("passa o dois alfa para o outro lado")
        acende(self, [N0.p("m", "a")], CORAL, 0.6)
        N1 = L([("2", "2"), ("e", "="), ("a", r"2\alpha")], 1120, 615, 36)
        self.gat("dois igual a dois alfa")
        gm(self, N0, N1, rt=0.8, ka=["2", "e", "a", "z"], kb=["2", "e", "a"], nota="(o −2α atravessa o = e troca de sinal)")
        N2 = L([("2", "2"), ("e", "="), ("a", r"2\alpha"), ("i", r"\ \Rightarrow\ "), ("al", r"\alpha"), ("e2", "="), ("um", "1")], 1120, 615, 36)
        self.gat("e alfa igual a um")
        gm(self, N1, N2, rt=0.6, kb=["2", "e", "a", "i", "a", "e", "2"], extra=[troca_p(cmp, 1.0, 0.5)], nota="(divide por 2)")
        # v4 C19: ‖B‖ com origem: o numerador é r; o denominador é r^{2α}; com α = 1, r/r² = 1/r
        bn, bd = num_den(BB.p("fr"))
        NB1 = L([("n", r"\|\B\|="), ("fa", r"\dfrac{", 0), ("nu", r"\|(-\Y,\ \X)\|"), ("fb", "}{", 1), ("de", r"(\X^2+\Y^2)^{\alpha}"), ("fc", "}", 0)], 1120, 700, 38)
        self.gat("então o tamanho do campo")
        escreve_p(self, NB1, ["n", "fb"], 0.15)
        voa(self, VGroup(*bn), VGroup(*NB1.p("nu")[1:-1]), rt=0.45, extra=[caneta(VGroup(NB1.p("nu")[0], NB1.p("nu")[-1]), ritmo=0.15)])
        voa(self, VGroup(*bd), NB1.p("de"), rt=0.45)
        junta(self, NB1, "b")
        Kr = L([("a", r"\|(-\Y,\ \X)\|=\sqrt{\Y^2+\X^2}=r")], 1460, 700, 28)
        NB2 = L([("n", r"\|\B\|="), ("fa", r"\dfrac{", 0), ("nu", "r"), ("fb", "}{", 1), ("de", r"(\X^2+\Y^2)^{\alpha}"), ("fc", "}", 0)], 1120, 700, 38)
        self.gat("em cima o tamanho de menos ípsilon")
        escreve(self, Kr, 0.06)
        gm(self, NB1, NB2, rt=0.7, extra=[FadeOut(Kr)], nota="(‖(−y, x)‖ = r)")
        self.remove(Kr)
        NB3 = L([("n", r"\|\B\|="), ("fa", r"\dfrac{", 0), ("nu", "r"), ("fb", "}{", 1), ("de", r"r^{2\alpha}"), ("fc", "}", 0)], 1120, 700, 38)
        self.gat("embaixo a distância elevada a dois alfa")
        gm(self, NB2, NB3, rt=0.7, nota="((x² + y²)^α = (r²)^α = r^{2α})")
        acende(self, [N2.p("al", "e2", "um")], AMB, 0.6)
        NB4 = L([("n", r"\|\B\|="), ("fa", r"\dfrac{", 0), ("nu", "r"), ("fb", "}{", 1), ("de", r"r^{2}"), ("fc", "}", 0)], 1120, 700, 38)
        self.gat("a distância dividida pela distância ao quadrado")
        gm(self, NB3, NB4, rt=0.7, extra=[pisca_cor(N2.p("um"), AMB, 0.7)], nota="(α = 1 no expoente: r^{2α} = r²)")
        NB = L([("n", r"\|\B\|="), ("fa", r"\dfrac{", 0), ("nu", "r"), ("fb", "}{", 1), ("de", r"r^{2}"), ("fc", "}", 0), ("c", r"=\dfrac1r")], 1120, 700, 38)
        self.gat("um sobre a distância o campo")
        gm(self, NB4, NB, rt=0.6, nota="(r/r² = 1/r)")
        gf, lbB = grafico("|B|", gy=900, gh=118)                  # v3 §1.2: o gráfico abaixo das fórmulas (final: topo em 782 px, o rótulo |B| sai de baixo da ‖B‖)
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
        self.play(FadeOut(lf), run_time=0.2)
        self.play(FadeIn(lc), run_time=0.25)
        self.remove(lf)
        self.gat("o campo elétrico aponta para fora")
        self.play(FadeOut(am), run_time=0.2)
        gm(self, BB, EE, rt=1.0, extra=[gira_setas(cmp, -PI / 2, 1.0), FadeIn(ga), FadeOut(circs), FadeOut(raio), FadeOut(rl)])
        self.remove(am, circs, raio, rl)
        self.gat("fora do fio não tem carga")                       # R16 v3: a lei citada acende
        acende(self, [ga], BR, 1.0)
        # v4 C20: o div E calculado de verdade (regra do produto e da cadeia em cada parcela)
        CB = L([("n", r"\|\B\|="), ("c", r"\dfrac1r")], 1560, 380, 30)
        DV = L([("dv", r"\D{\dv\E}="), ("a", r"\dfrac{\partial(\X s^{-\alpha})}{\dx}"), ("p", "+"), ("b", r"\dfrac{\partial(\Y s^{-\alpha})}{\dy}"), ("s", r",\quad s=\X^2+\Y^2")],
               1120, 460, 32)
        self.gat("calcula o divergente como no terceiro")
        self.play(FadeOut(RB0), FadeOut(N2), run_time=0.3)
        self.remove(RB0, N2)
        gm(self, NB, CB, rt=0.6, ka=["n", "z", "z", "z", "z", "z", "c"], nota="(‖B‖ = 1/r vira chip)")
        escreve(self, DV, 0.08)
        T1 = L([("d", r"\dfrac{\partial(\X s^{-\alpha})}{\dx}="), ("um", r"1\cdot s^{-\alpha}"), ("pl", "+"), ("x", r"\X"), ("c", r"\big(-\alpha s^{-\alpha-1}\cdot2\X\big)")],
               1120, 545, 30)
        self.gat("a primeira parcela é xis vezes")
        voa(self, DV.p("a"), T1.p("d")[:-1], rt=0.45)
        escreve_p(self, T1, ["um", "pl", "x", "c"], 0.08)
        self.play(caneta(T1.p("d")[-1], ritmo=0.2))
        junta(self, T1, "b")
        T1b = L([("d", r"\dfrac{\partial(\X s^{-\alpha})}{\dx}="), ("um", r"s^{-\alpha}"), ("mn", "-"), ("c", r"2\alpha\X^2s^{-\alpha-1}")], 1120, 545, 30)
        self.gat("sai a própria potência menos")
        gm(self, T1, T1b, rt=0.8, ka=["d", "um", "mn", "c", "c"], nota="(1·s^{−α}; x·(−α s^{−α−1}·2x) = −2αx² s^{−α−1})")
        T2 = L([("d", r"\dfrac{\partial(\Y s^{-\alpha})}{\dy}="), ("um", r"s^{-\alpha}"), ("mn", "-"), ("c", r"2\alpha\Y^2s^{-\alpha-1}")], 1120, 625, 30)
        self.gat("a segunda é igual com ípsilon")
        gm(self, T1b, T2, rt=0.7, copia=True, nota="(só o x vira y)")
        S1 = L([("dv", r"\D{\dv\E}="), ("a", r"2s^{-\alpha}"), ("mn", "-"), ("c", r"2\alpha(\X^2+\Y^2)s^{-\alpha-1}")], 1120, 705, 32)
        self.gat("somando aparecem duas vezes")
        gm(self, Duas(T1b, T2), S1, rt=0.9, copia=True, ka=["z", "a", "mn", "c", "z", "a", "mn", "c"], nota="(as duas parcelas somadas)")
        self.add(T1b, T2)
        S2 = L([("dv", r"\D{\dv\E}="), ("a", r"2s^{-\alpha}"), ("mn", "-"), ("c", r"2\alpha\,s\cdot s^{-\alpha-1}")], 1120, 705, 32)
        S3 = L([("dv", r"\D{\dv\E}="), ("a", r"2s^{-\alpha}"), ("mn", "-"), ("c", r"2\alpha\,s^{-\alpha}")], 1120, 705, 32)
        self.gat("que é dois alfa vezes a potência")
        gm(self, S1, S2, rt=0.7, nota="(x² + y² = s)")
        gm(self, S2, S3, rt=0.7, nota="(s·s^{−α−1} = s^{−α})")
        S4 = L([("dv", r"\D{\dv\E}="), ("r", r"\dfrac{2-2\alpha}{s^{\alpha}}")], 1120, 705, 32)
        DE = L([("rot", r"\D{\dv\E}="), ("fr", r"\D{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}")], 1120, 460, 38)
        DE2 = L([("rot", r"\D{\dv\E}="), ("fr", r"\D{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}"), ("z", r"=0\ \Rightarrow\ \alpha=1")], 1120, 460, 38)
        self.gat("divergente dois menos dois alfa")
        gm(self, S3, S4, rt=0.7, ka=["dv", "r", "r", "r"], nota="((2 − 2α) s^{−α})")
        AS = Duas(DV, T1b, T2, S4)
        AS.ks = ["x"] * (len(DV.ks) + len(T1b.ks) + len(T2.ks)) + ["rot", "fr"]
        gm(self, AS, DE, rt=0.9, nota="(fusão)")
        self.remove(DV, T1b, T2, S4)
        self.gat("igual a zero alfa um")
        gm(self, DE, DE2, rt=0.6, nota="(2 − 2α = 0 ⇒ α = 1)")
        DE = DE2
        NE = L([("n", r"\|\E\|="), ("a", r"\dfrac{r}{r^{2\alpha}}"), ("b", r"=\dfrac{r}{r^2}"), ("c", r"=\dfrac1r")], 1120, 690, 40)
        lbE = T("|E|", lbB.get_right()[0] * 120 + 960, 900 - 118 - 12, 24, "right", GEO, bold=False, up=False)
        self.gat("alfa um e o campo também cai")
        self.play(FadeOut(lbB), run_time=0.15)
        gm(self, CB, NE, rt=0.6, extra=[FadeIn(lbE)], nota="(o mesmo r/r^{2α} com α = 1)")
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
        self.play(*[FadeOut(m) for m in col + [fi, lc]], FadeOut(cmp), run_time=0.3)
        self.play(FadeIn(cg), cresce_campo(cc, 0.6), FadeIn(lco), run_time=0.6)
        self.remove(*col, fi, lc, cmp)
        self.gat("escreve o campo como o vetor posição")
        escreve(self, EP, 0.25)
        fe = EP.p("fr")                                            # leitura 22: X, ‖X‖ e p, um de cada vez
        self.gat("o x maiúsculo é o vetor posição")
        le(self, fe[0], 22, "o X maiúsculo é o vetor posição", ate="as barras duplas a distância")
        le(self, VGroup(*fe[2:5]), 22, "as barras duplas, a distância", ate="p o expoente")
        le(self, fe[5], 22, "p, o expoente", dur=0.5)
        DN0 = L([("d", NX), ("e", "="), ("r", r"(\X^2+\Y^2+\Z^2)^{1/2}")], 1120, 380, 32)        # v4 C21: a derivada da distância com a cadeia
        DN1 = L([("d", r"\dfrac{\partial" + NX + r"}{\dx}"), ("e", "="), ("h", r"\tfrac12"), ("r", r"(\X^2+\Y^2+\Z^2)^{-1/2}"), ("c", r"\cdot2\X")], 1120, 380, 32)
        DN = L([("d", r"\dfrac{\partial" + NX + r"}{\dx}"), ("e", "="), ("r", r"\dfrac{\X}{" + NX + "}")], 1120, 380, 32)
        PA = L([("d", r"\dfrac{\partial}{\dx}\Big(\dfrac{\X}{" + NX + r"^{p}}\Big)="), ("t1", r"\dfrac{1}{" + NX + r"^{p}}"), ("m", r"+\X\cdot\big(-p\," + NX + r"^{-p-1}\big)\cdot"),
                ("r", r"\dfrac{\X}{" + NX + "}")], 1120, 510, 32)
        self.gat("faz a conta de uma parcela")
        escreve_p(self, PA, ["d"], 0.2)
        self.gat("primeiro a derivada da distância")
        escreve(self, DN0, 0.15)
        self.gat("o meio desce")
        fh = VGroup(*DN0.p("r")[-3:]).copy()
        gm(self, DN0, DN1, rt=0.8, copia=True, voos={"h": fh}, nota="(o ½ desce do expoente; a cadeia traz 2x)")
        self.remove(DN0, fh)
        self.gat("o meio com o dois cancela")
        acende(self, [DN1.p("h"), DN1.p("c")[1]], CORAL, 0.6)
        self.gat("a derivada da distância nessa direção")
        gm(self, DN1, DN, rt=0.8, ka=["d", "e", "z", "r", "r"], nota="(½·2 = 1; a potência −½ é 1/‖X‖)")
        self.gat("agora a regra do produto com xis")                # v4: a parcela em degraus, um por frase (sem palco parado)
        acende(self, [PA.p("d")], AMB, 0.6)
        self.gat("sobra um sobre a distância elevada ao expoente")
        escreve_p(self, PA, ["t1"], 0.15)
        self.gat("na outra parte menos p vezes a distância")
        escreve_p(self, PA, ["m"], 0.15)
        self.gat("vezes a derivada da distância xis")
        voa(self, DN.p("r"), PA.p("r"), rt=0.5)
        junta(self, PA, "b")
        PB0 = L([("e", "="), ("t1", r"\dfrac{1}{" + NX + r"^{p}}"), ("m", r"-p\,\X^2\," + NX + r"^{-p-1}" + NX + r"^{-1}")], 1150, 640, 32)
        self.gat("xis vezes xis dá xis ao quadrado")
        gm(self, PA, PB0, rt=0.8, copia=True, ka=["x", "t1", "m", "m"], nota="(x·x = x²)")
        PB1 = L([("e", "="), ("t1", r"\dfrac{1}{" + NX + r"^{p}}"), ("m", r"-p\,\X^2\," + NX + r"^{-p-2}")], 1150, 640, 32)
        self.gat("e as potências da distância se juntam")
        acende(self, [PB0.p("m")], AMB, 0.5)
        gm(self, PB0, PB1, rt=0.7, nota="(−p − 1 − 1 = −p − 2)")
        PB = L([("e", "="), ("t1", r"\dfrac{1}{" + NX + r"^{p}}"), ("t2", r"-\dfrac{p\,\X^2}{" + NX + r"^{p+2}}")], 1150, 640, 34)
        self.gat("então dá um sobre a distância")
        gm(self, PB1, PB, rt=0.7, ka=["e", "t1", "t2"], nota="(potência negativa vira denominador)")
        self.gat("menos o expoente vezes o quadrado")
        acende(self, [PB.p("t2")], AMB, 0.7)
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
        # v3 §3 #5: a linha de y nasce no próprio lugar (cópia da linha de x + mapa que só troca x → y); depois a de z; nunca empilhadas
        for Pn in (Py, Pz_):
            cpx = L(list(zip(Px.ks, Px.ts)), 0, 0, Px.size)
            cpx.shift(Pn.get_left() - cpx.get_left())
            voa(self, Px, cpx, rt=0.5)
            gm(self, cpx, Pn, rt=0.5, nota="(só os x trocam de letra)")
        SM = L([("dv", r"\D{\dv\E}="), ("t1", r"\dfrac{3}{" + NX + r"^{p}}"), ("m", r"-\dfrac{p\,", 2), ("sum", r"(\X^2+\Y^2+\Z^2)"), ("sl", "}{", 1),
                ("den", NX + r"^{p+2}"), ("fc", "}", 0)], 1120, 575, 32)
        self.gat("agora soma")
        A3_ = Duas(Px, Py, Pz_)
        A3_.ks = ["dv", "t1", "sum"] * 3
        gm(self, A3_, SM, rt=0.9, copia=True, kb=["dv", "t1", "sum", "sum", "sum", "sum", "sum"], nota="(as três parcelas voam para a soma)")
        self.add(Px, Py, Pz_)
        # v3 §3 #6: quatro mapas — a soma vira ‖X‖² (com a chave "= ‖X‖²" por 1 s); o expoente p + 2 se separa; o par ‖X‖² coral e riscado; (3 − p)/‖X‖^p
        ch_ = TC(r"=" + NX + r"^2", 0, 0, 30, "c")
        ch_.next_to(SM, RIGHT, buff=14 / 120)                      # à direita da linha, na altura da soma (não cobre o denominador)
        ch_.set_y(SM.p("sum").get_center()[1])
        ch_._origem = "a"
        S1 = L([("e", "="), ("t1", r"\dfrac{3}{" + NX + r"^{p}}"), ("m", r"-\dfrac{p\,", 2), ("sum", NX + r"^2"), ("sl", "}{", 1), ("den", NX + r"^{p+2}"),
                ("fc", "}", 0)], 1150, 690, 32)
        self.gat("os quadrados das coordenadas somam")
        print(f"[origem] a {self.lote} {self._aid} {self.t:.2f} {ch_._tex!r} (a chave da soma, 1 s)")
        self.play(caneta(ch_, ritmo=0.15), run_time=0.4)
        self.wait(0.6)
        gm(self, SM, S1, rt=0.8, copia=True, ka=["e", "t1", "m", "sum", "sl", "den", "fc"], extra=[FadeOut(ch_)], nota="(a soma vira ‖X‖²)")
        self.remove(ch_)
        S2 = L([("e", "="), ("t1", r"\dfrac{3}{" + NX + r"^{p}}"), ("m", r"-\dfrac{p\,", 2), ("n2", NX + r"^2"), ("sl", "}{", 1), ("dp", NX + r"^{p}"), ("d2", NX + r"^{2}"),
                ("fc", "}", 0)], 1150, 690, 32)
        self.gat("que cancela o mais dois")
        gm(self, S1, S2, rt=0.6, ka=["e", "t1", "m", "n2", "sl", "den", "fc"], kb=["e", "t1", "m", "n2", "sl", "den", "den", "fc"], nota="(o expoente p + 2 se separa)")
        tr = cancela(self, S2, "n2", "d2", rt=0.3)
        S3a = L([("e", "="), ("t1", r"\dfrac{3}{" + NX + r"^{p}}"), ("m", r"-\dfrac{p", 2), ("sl", "}{", 1), ("dp", NX + r"^{p}"), ("fc", "}", 0)], 1150, 690, 32)
        self.gat("sobra o número de parcelas")
        gm(self, S2, S3a, rt=0.6, ka=["e", "t1", "m", "z", "sl", "dp", "z", "fc"], somem=tr, nota="(o par ‖X‖² sai)")
        S3 = L([("e", "="), ("r", r"\D{\dfrac{3-p}{" + NX + r"^{p}}}")], 1150, 690, 32)
        gm(self, S3a, S3, rt=0.6, ka=["e", "r", "r", "r", "r", "r"], nota="(mesmo denominador: 3 − p)")
        np_ = leg_mix(["NO PLANO: 2 PARCELAS ", r"$\Rightarrow$", " (2 − p)"], 1124, 800, GEO, "left", 26)
        self.gat("no plano são duas parcelas")
        self.play(FadeIn(np_, shift=0.05 * UP), run_time=0.4)
        self.gat("o divergente no espaço é três")                 # R16: o resultado citado acende
        acende(self, [S3.p("r")], SAIC, 1.0)
        DF = L([("dv", r"\D{\dv\E}="), ("r", r"\D{\dfrac{3-p}{" + NX + r"^{p}}}")], 1120, 270, 36)
        self.gat("para zerar o expoente é três")
        AD = Duas(Px, Py, Pz_, SM, S3)
        AD.ks = ["x"] * 9 + ["dv"] + ["x"] * 6 + ["x", "r"]
        gm(self, AD, DF, rt=0.8, nota="(fusão)", extra=[FadeOut(np_), *[FadeOut(t) for t in tr]])
        self.remove(Px, Py, Pz_, SM, S3, np_, *tr)
        P3 = L([("p", r"p=3\ \Rightarrow\ "), ("n", r"\|\E\|=\dfrac{" + NX + "}{" + NX + r"^3}=\dfrac{r}{r^3}=\dfrac1{r^2}")], 1120, 370, 36)
        escreve_p(self, P3, ["p"], 0.2)
        self.gat("a intensidade fica a distância dividida")           # v4 C21: r/r³ com origem (‖X‖ = r)
        escreve_p(self, P3, ["n"], 0.12)
        junta(self, P3)
        c0 = legenda("COULOMB", 1124, 450, GEO, "left", 26)        # C6: o "·" a 10 px do B
        cl = [c0, legenda("· GRAVITAÇÃO", c0.get_right()[0] * 120 + 960 + 10, 450, GEO, "left", 26)]
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
        self.play(FadeOut(F1[0]), run_time=0.2)
        self.play(FadeIn(F2_[0], shift=0.05 * UP), run_time=0.25)
        self.remove(F1[0])
        self.gat("junto com a simetria")
        self.play(FadeOut(F1[1]), run_time=0.2)
        self.play(FadeIn(F2_[1], shift=0.05 * UP), run_time=0.25)
        self.remove(F1[1])
        self.gat("as linhas em círculo em volta do fio")
        self.play(FadeOut(F2_[0]), run_time=0.2)
        self.play(FadeIn(sim, shift=0.05 * UP), run_time=0.25)
        self.remove(F2_[0])
        self.sai_fim()
