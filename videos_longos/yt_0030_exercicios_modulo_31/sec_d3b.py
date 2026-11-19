"""Lote PD3B · D3b DUAS REGRAS · v2 (alvos v2_i1, v2_i2a, v2_i2b + 13 v1). Palco desde o início: as curvas de nível de φ = (x² − y²)/2 e a rede de ∇φ.
F = ∇φ: P = φ_x, Q = φ_y, R = φ_z (legenda do índice); o molde rot F em vetor-coluna (linhas = Lin separadas dentro dos parênteses); cada linha é
copiada para rot ∇φ por glyph map (R_y → φ_zy …); Schwarz; R14 um par por linha → 0⃗. Sela com o quadradinho. div(rot F): cada parêntese voa da
componente; glyph map para as seis mistas; R14 três vezes → 0. O teste parcela a parcela; NÃO EXISTE. div B = 0 ⇔ B = rot A e a metade provada."""
from alg30 import *  # noqa: F401,F403

C1, S1, T1 = (0.0, 0.0), 1.2, .55
C2, S2, T2 = (1.6, 0.0), 1.0, .6


def curvas_nivel():
    """v3 (alvo v3_d3bg): x² − y² = ±k (k = 1; 2,5; 5) e as diagonais, tracejadas GEO 2 px a 60 % (visíveis atrás das setas de passo 1)."""
    g = VGroup()
    for k in (1, 2.5, 5):
        for sg in (1, -1):
            h = [(sg * math.sqrt(k + t * t), t) for t in np.arange(-3.2, 3.2001, .05)]
            v = [(t, sg * math.sqrt(k + t * t)) for t in np.arange(-4.2, 4.2001, .05)]
            g.add(linha_rec(VA, h, LA, GEO, 2, .6, dash=(8, 8)), linha_rec(VA, v, LA, GEO, 2, .6, dash=(8, 8)))
    g.add(linha_rec(VA, [(-4, -4), (4, 4)], LA, GEO, 2, .6, dash=(8, 8)), linha_rec(VA, [(-4, 4), (4, -4)], LA, GEO, 2, .6, dash=(8, 8)))
    return g.set_z_index(2)


def vetor_col(rotulo, linhas, x, y, size=34, larg=None):
    """Vetor-coluna: rótulo (Lin) + parênteses (TeX com linhas fantasmas) + as três linhas (Lin), centradas nas linhas da matriz."""
    ph = r"\\ ".join(r"\phantom{%s}" % l for l in (larg or ["R_y-Q_z"] * 3))
    par = TC(r"\begin{pmatrix}" + ph + r"\end{pmatrix}", x, y, size, "l", caneta=True)
    par._moldura = True
    rot_ = L(rotulo, x, y, size, "l")
    par.shift(RIGHT * (rot_.get_right()[0] + 6 / 120 - par.get_left()[0]))
    h = par.height
    rows = []
    for i, ln in enumerate(linhas):
        r = L(ln, 0, 0, size, "c")
        r.move_to([par.get_center()[0], par.get_center()[1] + (1 - i) * h * 0.30, 0])
        r._linha_de = par                 # R13: o vetor-coluna (rótulo + parênteses + 3 linhas) conta como uma linha de conta
        rows.append(r)
    return rot_, par, rows


class LoteD3b(Base):
    ANTES = "A FAMÍLIA DE REDEMOINHOS · GIRO DE 90°"

    def corpo(self):
        # ── D3b-1 · um gradiente nunca gira (alvo v2_i1) ──
        self.an("D3b-1")
        self.secao("DUAS REGRAS · UM GRADIENTE NUNCA GIRA")
        zera_chapas()
        chA = chapa_px(*LA, nome="D3b palco A", v=VA)
        cn = curvas_nivel()
        sela = campo30(VA, F_SELA, -3, 3, -2, 2, 1, mmax=3, rmin=0, skip=clar28([(-3.9, -2.95, -.25, -2.35)]), nome="D3b ∇φ (sela, passo 1)")
        lab = leg_mix(["CURVAS DE NÍVEL DE ", r"$\varphi$", " E O GRADIENTE"], *canto_xy(VA, -2.05, -2.68), GEO, "center", 24)
        lab = VGroup(placa7(lab, 8, 4), lab)
        troca(self, "D3 → D3b (palco com as curvas de nível)")
        self.play(FadeIn(chA), Create(cn), run_time=0.8)
        self.gat("pega um campo que é o gradiente")
        self.play(cresce_campo(sela, 0.8), FadeIn(lab), run_time=0.8)
        FG = L([("F", r"\F=\nabla\varphi:\quad "), ("P", r"\Pp=\varphi_x,"), ("Q", r"\ \ \Qq=\varphi_y,"), ("R", r"\ \ \R=\varphi_z")], 1120, 265, 34)
        ix = leg_mix(["ÍNDICE = DERIVADA: ", r"$\varphi_x=\partial\varphi/\partial x$"], 1124, 320, GEO, "left", 24)
        self.gat("as componentes são as derivadas parciais")
        escreve(self, FG, 0.3)
        self.gat("na tela nabla fi")                              # leitura 7: ∇φ
        le(self, VGroup(*FG.p("F")[3:5]), 7, "nabla fi: lê-se gradiente de fi", ate="e daqui em diante")
        self.gat("e daqui em diante")                             # leitura 8: o índice x de φ_x (primeira vez)
        self.play(FadeIn(ix, shift=0.05 * UP), run_time=0.4)
        le(self, FG.p("P")[3], 8, "fi com xis pequeno embaixo é a derivada parcial de fi em relação a xis", ate="calcula o rotacional")
        LR = [[("a", r"\R_y"), ("m", "-"), ("b", r"\Qq_z")], [("a", r"\Pp_z"), ("m", "-"), ("b", r"\R_x")], [("a", r"\Qq_x"), ("m", "-"), ("b", r"\Pp_y")]]
        rF, pF, rowsF = vetor_col([("r", r"\rot\F=")], LR, 1120, 420, 34)
        self.gat("calcula o rotacional")
        escreve(self, rF, 0.25)
        for r_ in rowsF:
            r_._origem = "a"
        escreve(self, pF, 0.25, extra=[caneta(r_, ritmo=0.2) for r_ in rowsF])
        LP = [[("a", r"\varphi_{zy}"), ("m", "-"), ("b", r"\varphi_{yz}")], [("a", r"\varphi_{xz}"), ("m", "-"), ("b", r"\varphi_{zx}")],
              [("a", r"\varphi_{yx}"), ("m", "-"), ("b", r"\varphi_{xy}")]]
        rP, pP, rowsP = vetor_col([("r", r"\rot\nabla\varphi=")], LP, 1120, 640, 40, larg=[r"\varphi_{zy}-\varphi_{yz}"] * 3)
        self.gat("a primeira componente é")
        pP._origem = "a"
        escreve(self, rP, 0.3, extra=[caneta(pP, ritmo=0.3)])
        gm(self, rowsF[0], rowsP[0], rt=0.9, copia=True)
        lz = leg_mix([r"$\varphi_{zy}$", ": DERIVA EM z, DEPOIS EM y"], 1124, 790, GEO, "left", 26)
        self.play(FadeIn(lz, shift=0.05 * UP), run_time=0.4)
        self.gat("menos a derivada em relação à profundidade")    # R16: o segundo termo citado acende
        acende(self, [rowsP[0].p("b")], CAMPO2, 1.0)
        self.gat("e as outras duas componentes")
        gm(self, rowsF[1], rowsP[1], rt=0.6, copia=True)
        gm(self, rowsF[2], rowsP[2], rt=0.6, copia=True)
        self.gat("uma derivada mista menos a mesma")             # R16 v3: as mistas citadas acendem, depois as de ordem trocada
        acende(self, [rowsP[1].p("a"), rowsP[2].p("a")], CAMPO2, 0.9)
        self.gat("com a ordem trocada")
        acende(self, [rowsP[1].p("b"), rowsP[2].p("b")], CAMPO2, 0.9)
        sw = leg_mix(["SCHWARZ (", r"$\varphi$", "DE CLASSE", "C²", "):", r"$\varphi_{zy}=\varphi_{yz}$"], 1124, 835, GEO, "left", 26, gap=8)
        self.gat("as derivadas mistas são iguais")
        self.play(FadeIn(sw, shift=0.05 * UP), run_time=0.4)
        zeros = []
        for i in range(3):
            tr = cancela(self, rowsP[i], "a", "b", rt=0.2)
            z = L([("z", "0")], 0, 0, 40, "c").move_to(rowsP[i].get_center())
            z._linha_de = pP                  # o zero é a linha i do vetor-coluna (R13 conta o vetor como uma linha)
            gm(self, rowsP[i], z, rt=0.3, somem=tr)          # final: 0,3 s (sync com a voz: "tudo cancela")
            zeros.append(z)
        zz = L([("z", r"=\V{\vec 0}")], 0, 0, 40, "l")
        zz.next_to(pP, RIGHT, buff=10 / 120)
        self.gat("tudo cancela")
        escreve(self, zz, 0.5)
        self.gat("no plano só sobra a terceira")
        acende(self, [zeros[2], rowsF[2]], VIO, 1.2)
        self.ate(1.0)

        # ── D3b-2 · a sela do episódio passado (alvo 13 v1) ──
        self.an("D3b-2")
        RZ = L([("r", r"\rot\nabla\varphi="), ("z", r"\V{\vec0}")], 1120, 420, 40)
        ped = quad30(VA, C1, S1)
        fan = fantasma(VA, quad_pts(C1, S1))
        clareira(sela, lambda: ou(clar_ped(ped), dq(C1, S1), clar28([(-3.9, -2.95, -.25, -2.35)])))
        self.gat("lembra do campo que esticava")
        A0 = Duas(rF, *rowsF, rP, *zeros, zz)
        A0.ks = ["x"] * (1 + 9) + ["r"] + ["x"] * 3 + ["z"]
        gm(self, A0, RZ, rt=0.9, nota="(fusão)", extra=[FadeOut(pF), FadeOut(pP), FadeOut(lz), FadeIn(ped), FadeIn(fan)])
        self.remove(pF, pP, lz)
        PH1 = L([("phi", r"\varphi="), ("h", r"\tfrac12"), ("p", r"(\X^2-\Y^2)")], 1120, 510, 36)
        self.gat("ele é o gradiente da metade")
        escreve(self, PH1, 0.3)
        # v4 C4: as derivadas de φ antes do ∇φ (o 2 do expoente desce)
        PH2 = L([("fx", r"\varphi_{\Am x}"), ("ex", r"=\tfrac12\cdot2\X"), ("rx", r"=\X"), ("vg", r",\qquad "), ("fy", r"\varphi_{\Mg y}"), ("ey", r"=\tfrac12\cdot(-2\Y)"),
                 ("ry", r"=-\Y")], 1120, 580, 32)
        pp = PH1.p("p")                                               # ( x 2 − y 2 )
        ex, ey = PH2.p("ex"), PH2.p("ey")
        self.gat("derivando fi em xis")
        print(f"[origem] a {self.lote} D3b-2 {self.t:.2f} {PH2._tex[:60]!r} (φ_x; o 2 do expoente voa)")
        self.play(caneta(VGroup(*PH2.p("fx"), *ex[0:5]), ritmo=0.12))
        voa(self, pp[2], ex[5], rt=0.4)
        self.play(caneta(VGroup(ex[6], *PH2.p("rx")), ritmo=0.15))
        self.gat("derivando em ípsilon")
        self.play(caneta(VGroup(*PH2.p("vg", "fy"), *ey[0:7]), ritmo=0.12))
        voa(self, pp[5], ey[7], rt=0.4)
        self.play(caneta(VGroup(*ey[8:], *PH2.p("ry")), ritmo=0.15))
        junta(self, PH2)
        PH3 = L([("g", r"\nabla\varphi="), ("v", r"(\varphi_{\Am x},\ \varphi_{\Mg y})"), ("e", "="), ("r", r"(\X,\ -\Y)")], 1120, 650, 34)
        rr = PH3.p("r")                                               # ( x , − y )
        self.gat("o gradiente é xis menos ípsilon")
        self.play(caneta(VGroup(*PH3.p("g", "v", "e"), rr[0], rr[2], rr[5]), ritmo=0.1))
        voa(self, PH2.p("rx")[1], rr[1], rt=0.4)
        voa(self, PH2.p("ry")[1:3], VGroup(rr[3], rr[4]), rt=0.4)
        junta(self, PH3, origem="b")
        self.gat("e pela regra que acabamos")
        acende(self, [RZ], VIO, 1.0)
        self.gat("por isso o quadradinho deformava")
        a0 = ped.area()
        self.play(anda(ped, fl_sela, T1, 2.0, rate=linear, nome="D3b sela"))
        print(f"[D3b] sela: área {a0:.4f} → {ped.area():.4f}")
        dm = T("DEFORMA, MAS NÃO GIRA", 1120, 715, 40, cor=LIMA)
        self.play(FadeIn(dm, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D3b-3 · um rotacional nunca diverge (alvo v2_i2a) ──
        self.an("D3b-3")
        self.secao("DUAS REGRAS · UM ROTACIONAL NUNCA DIVERGE")
        sela.clear_updaters()
        p2 = quad30(VA, C2, S2)
        f2 = fantasma(VA, quad_pts(C2, S2))
        giro = campo30(VA, F_GIRO, mmax=4, rmin=0, nome="D3b giro")
        clareira(giro, lambda: ou(clar_ped(p2), dq(C2, S2)))
        o0 = ponto7(VA.c2p(0, 0), GEO, 6, 8)
        col = [FG, ix, RZ, PH1, PH2, PH3, dm, sw]
        troca(self, "D3b sela → giro (palco)")
        self.play(*[FadeOut(m) for m in col + [ped, fan, lab]], FadeOut(sela), FadeOut(cn), cresce_campo(giro, 0.8), FadeIn(p2), FadeIn(f2), FadeIn(o0), run_time=0.8)
        self.remove(*col, ped, fan, sela, cn, lab)
        RF = L([("r", r"\rot\F=("), ("c1", r"\R_y-\Qq_z"), ("v1", r",\ \ "), ("c2", r"\Pp_z-\R_x"), ("v2", r",\ \ "), ("c3", r"\Qq_x-\Pp_y"), ("f", ")")], 1120, 270, 34)
        self.gat("calcula o rotacional de um campo")
        escreve(self, RF, 0.25)
        D1_ = L([("d", r"\dv(\rot\F)="), ("dx", r"\dfrac{\partial}{\dx}"), ("c1", r"(\R_y-\Qq_z)"), ("pl", "+"), ("dy", r"\dfrac{\partial}{\dy}"), ("c2", r"(\Pp_z-\R_x)")], 1120, 380, 32)
        D2_ = L([("pl", "+"), ("dz", r"\dfrac{\partial}{\partial\Z}"), ("c3", r"(\Qq_x-\Pp_y)")], 1290, 470, 32)
        self.gat("o divergente desse rotacional")
        escreve_p(self, D1_, ["d"], 0.3)
        for fr, lin, kd, kc in (("a primeira componente é derivada", D1_, ["dx"], "c1"), ("a segunda na vertical", D1_, ["pl", "dy"], "c2"),
                                ("e a terceira na profundidade", D2_, ["pl", "dz"], "c3")):
            self.gat(fr)
            escreve_p(self, lin, kd, 0.3)
            voa(self, RF.p(kc), lin.p(kc), rt=0.6)
        junta(self, D1_)
        junta(self, D2_)
        S6 = L([("e", "="), ("Ryx", r"\R_{yx}"), ("Qzx", r"-\Qq_{zx}"), ("Pzy", r"+\Pp_{zy}"), ("Rxy", r"-\R_{xy}"), ("Qxz", r"+\Qq_{xz}"), ("Pyz", r"-\Pp_{yz}")], 1150, 570, 32)
        self.gat("aparecem seis derivadas mistas")
        A6 = Duas(D1_, D2_)
        A6.ks = ["d", "dx", "c1a", "pl", "dy", "c2a", "pl2", "dz", "c3a"]
        A6._rg = [D1_._rg[0], D1_._rg[1], D1_._rg[2], D1_._rg[3], D1_._rg[4], D1_._rg[5]] + [[len(D1_[0]) + g for g in r] for r in D2_._rg]
        A6.ks = ["d", "dx", "c1", "pl", "dy", "c2", "pl2", "dz", "c3"]
        gm(self, A6, S6, rt=1.0, copia=True, ka=A6.ks, kb=["e", "c1", "c1", "c2", "c2", "c3", "c3"])
        self.remove(A6)
        self.add(D1_, D2_)
        self.gat("e elas se cancelam aos pares")
        cur = S6
        for par in (("Ryx", "Rxy"), ("Qzx", "Qxz"), ("Pzy", "Pyz")):
            tr = cancela(self, cur, *par, rt=0.2)
            ks = [k for k in cur.ks if k not in par]
            nv = L([(k, t) for k, t in zip(cur.ks, cur.ts) if k not in par] if len(ks) > 1 else [("e", "="), ("z", r"\D0")], 1150, 570, 32)
            cur = gm(self, cur, nv, rt=0.3, somem=tr)       # final: 0,3 s (sync com a voz: "um rotacional nunca diverge")
        z0 = cur
        ap = legenda("AS SEIS MISTAS SE CANCELAM AOS PARES (SCHWARZ)", 1124, 760, GEO, "left", 26)
        self.play(FadeIn(ap, shift=0.05 * UP), run_time=0.3)
        self.gat("um rotacional nunca diverge")
        a0 = p2.area()
        self.play(anda(p2, fl_giro, T2, 1.3, rate=linear, nome="D3b giro rígido"))
        print(f"[D3b] giro: área {a0:.4f} → {p2.area():.4f}")
        self.ate(1.0)

        # ── D3b-4 · o teste (alvo v2_i2b) ──
        self.an("D3b-4")
        DZ = L([("d", r"\D{\dv(\rot\F)}"), ("z", r"\D{=0}")], 1120, 270, 38)
        self.gat("e isso vira teste")
        self.secao("DUAS REGRAS · O TESTE")
        AZ = Duas(RF, D1_, D2_, z0)
        AZ.ks = ["x"] * (len(RF.ks) + len(D1_.ks) + len(D2_.ks)) + ["x", "z"]
        AZ.ks[len(RF.ks)] = "d"
        gm(self, AZ, DZ, rt=0.9, nota="(fusão)", extra=[FadeOut(ap)])
        self.remove(RF, D1_, D2_, z0, ap)
        ex = T("EXISTE UM CAMPO G COM", 1120, 370, 30)
        G = L([("r", r"\rot\Gg=("), ("c1", r"\X\sen\Y"), ("v1", r",\ "), ("c2", r"\cos\Y"), ("v2", r",\ "), ("c3", r"\Z-\X\Y"), ("q", r")\ ?")], 1120, 430, 36)
        self.gat("existe outro campo cujo rotacional")
        self.play(FadeIn(ex, shift=0.05 * UP), run_time=0.4)
        escreve(self, G, 0.25)
        DV = L([("d", r"\dv="), ("t1", r"\dfrac{\partial(\X\sen\Y)}{\dx}"), ("p1", "+"), ("t2", r"\dfrac{\partial(\cos\Y)}{\dy}"), ("p2", "+"),
                ("t3", r"\dfrac{\partial(\Z-\X\Y)}{\partial\Z}")], 1120, 545, 30)
        self.gat("calcula o divergente")
        escreve_p(self, DV, ["d", "p1", "p2"], 0.2)
        voa(self, G.p("c1"), DV.p("t1"), rt=0.45, extra=[TransformFromCopy(G.p("c2"), DV.p("t2")), TransformFromCopy(G.p("c3"), DV.p("t3"))])
        junta(self, DV)
        RR = L([("e", "="), ("u1", r"1\cdot"), ("s1", r"\sen\Y"), ("p2", "+"), ("s2", r"(-\sen\Y)"), ("um", "+1")], 1150, 650, 36)
        escreve_p(self, RR, ["e"], 0.3)
        n1_, _ = num_den(DV.p("t1"))                                # ∂ ( x s e n y )
        n3_, _ = num_den(DV.p("t3"))                                # ∂ ( z − x y )
        # v4 C5: em cada parcela, o que fica parado (GEO) e o que varia acendem antes do voo
        self.gat("na primeira o ípsilon fica parado")
        acende(self, [VGroup(*n1_[3:7])], GEO, 0.6)
        acende(self, [n1_[2]], AMB, 0.6)
        self.gat("a primeira parcela dá seno")
        voa(self, n1_[2], RR.p("u1")[0], rt=0.45)                    # o 1 é a derivada de x
        self.play(caneta(RR.p("u1")[1], ritmo=0.2))
        voa(self, VGroup(*n1_[3:7]), RR.p("s1"), rt=0.45)
        self.gat("na segunda a derivada do cosseno")
        acende(self, [DV.p("t2")], MAG, 0.6)
        self.gat("a segunda dá menos seno")
        escreve_p(self, RR, ["p2"], 0.2)
        voa(self, DV.p("t2"), RR.p("s2"), rt=0.5)
        self.gat("na terceira o xis e o ípsilon")
        acende(self, [VGroup(*n3_[3:6])], GEO, 0.6)
        acende(self, [n3_[2]], CAMPO2, 0.6)
        self.gat("e a terceira dá um")
        self.play(caneta(RR.p("um")[0], ritmo=0.2))
        voa(self, n3_[2], RR.p("um")[1], rt=0.45)
        junta(self, RR, origem="b")
        RR2 = L([("e", "="), ("s1", r"\sen\Y"), ("s2", r"-\sen\Y"), ("um", "+1")], 1150, 650, 36)
        self.gat("seno menos seno cancela")
        gm(self, RR, RR2, rt=0.8, ka=["e", "z", "s1", "s2", "s2", "um"], nota="(1·sen y = sen y; +(−sen y) = −sen y)")
        tr = cancela(self, RR2, "s1", "s2", rt=0.2)
        self.gat("total um")
        R2 = L([("e", "="), ("um", r"\D1"), ("res", r"\neq0")], 1150, 650, 36)
        gm(self, RR2, R2, rt=0.6, somem=tr)
        ne = T("NÃO EXISTE", 1120, 760, 44, cor=CORAL)
        self.gat("então não existe")
        self.play(FadeIn(ne, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D3b-5 · na física ──
        self.an("D3b-5")
        GT = L([("r", r"\rot\Gg\ ?:\quad"), ("d", r"\dv="), ("res", r"\D1\neq0")], 1120, 400, 34)
        DB = L([("d", r"\dv\B=0")], 1120, 520, 36)
        self.gat("o campo magnético tem divergente zero")
        AG = Duas(G, DV, R2)
        AG.ks = ["r"] + ["x"] * (len(G.ks) - 1) + ["d"] + ["x"] * (len(DV.ks) - 1) + ["x", "res", "res"]
        gm(self, AG, GT, rt=0.8, nota="(fusão)", extra=[FadeOut(ex), FadeOut(ne)])
        self.remove(G, DV, R2, ex, ne)
        escreve(self, DB, 0.4)
        self.gat("não existe polo magnético isolado")             # R16 v3: a lei citada acende
        acende(self, [DB], SAIC, 1.0)
        DB2 = L([("d", r"\dv\B=0"), ("eq", r"\ \Leftrightarrow\ \B=\rot A")], 1120, 520, 36)
        et = legenda("NO ESPAÇO TODO", 1124, 580, GEO, "left", 26)
        self.gat("o rotacional de outro campo")
        gm(self, DB, DB2, rt=0.7, extra=[FadeIn(et)])
        self.gat("a seta dupla nos dois sentidos")                 # leitura 9: ⇔
        le(self, DB2.p("eq")[0], 9, "a seta dupla nos dois sentidos lê-se se e somente se", ate="as duas ideias andam juntas")
        MP = L([("h", r"\B=\rot A\ \Rightarrow\ "), ("d", r"\dv\B=\dv(\rot A)"), ("z", "=0")], 1120, 660, 36)
        self.gat("a regra de hoje prova uma das metades")
        escreve_p(self, MP, ["h", "d"], 0.25)
        voa(self, DZ.p("z"), MP.p("z"), rt=0.6)
        junta(self, MP)
        self.ate(1.0)

        # ── D3b-6 · a hipótese C² (puxa o D4) ──
        self.an("D3b-6")
        sw2 = leg_mix(["SCHWARZ:", r"$\varphi$", "DE CLASSE", "C²", r"$\Rightarrow$", "MISTAS IGUAIS"], 1124, 780, GEO, "left", 26, gap=9)
        self.gat("e repara na hipótese")
        self.play(FadeIn(sw2, shift=0.05 * UP), run_time=0.4)
        c2 = sw2[3]
        self.gat("classe cê dois sem")
        self.play(c2.animate.set_color(CORAL), run_time=0.25)
        self.wait(1.0)
        self.play(c2.animate.set_color(GEO), run_time=0.25)
        giro.clear_updaters()
        self.sai_fim()
