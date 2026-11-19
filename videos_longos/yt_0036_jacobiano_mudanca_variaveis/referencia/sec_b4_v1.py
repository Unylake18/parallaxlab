"""yt_0036 · B4 · o fator local (alvos 08 a 11). B4-1: a malha 4 × 4 curva por φ(u, v) = (u² − v², 2uv) (ApplyPointwiseFunction, um movimento)
e as células se pintam pelo tamanho. B4-2: zoom na célula de canto M = φ(0,75; 0,5) (alvo 09); a célula curva vira o paralelogramo das duas
setas; decolagem para a cena Three.js (cena1, porte do c3d36.html) no mesmo quadro; o vetor ∧ sobe até 3,25 (altura = área); glyph map dos
deltas; pouso na vista de cima (ortográfica) e volta ao 2D no mesmo quadro. B4-3: C6 à esquerda, C5 e a tabela do Δ à direita, a célula
encolhendo no palco (um ValueTracker só) e J(0, 0) = 0, J(1, 1) = 8 na miniatura do B4-1."""
from j36 import *
from sec_b3 import VU4, AU4, malha44, plano_b4

VX4, AX4 = Vw(1290, 880, 320), (-1.1, 1.1, -.05, 2.1)
UM, VM = .75, .5
MXY = mapC(UM, VM)                                           # (0,3125; 0,75)
VZ = Vw(330 - MXY[0] * 1900, 860 + MXY[1] * 1900, 1900)       # zoom: M em (330, 860) px, 1900 px por unidade de x, y
AZ = (.2, .6, .7, 1.05)                                       # papel do zoom = o chão da cena 3D
DL = .1
W1XY, W2XY = (2 * UM * DL, 2 * VM * DL), (-2 * VM * DL, 2 * UM * DL)


def par_xy(a, b):
    return (MXY[0] + a * W1XY[0] + b * W2XY[0], MXY[1] + a * W1XY[1] + b * W2XY[1])


def cor_J(J):
    return mixh("#2A2550", LIMA, min(1.0, J / 7) * .85)


class PB4(J36):
    ANTES = "O SINAL E O MÓDULO"
    CHIP = True

    def corpo(self):
        # o B3-3 terminou com o plano u, v e a malha 4 × 4: o lote começa com eles (sem animação)
        d4 = plano_b4()
        mm = malha44()
        for m in [d4["lx"], d4["ly"]] + [t[1] for t in d4["tk"]]:
            ja_escrita(m)
        self.add(*todos_plano(d4), mm)
        self.an("B4-1")
        self.secao("A GRADE CURVA")
        dX = monta_plano(VX4, AX4, 1.15, 2.2, -1.1, -.05)
        ps, pl = phi_seta(760, 900, 260, r"\varphi(\uu,\vv)=(\uu^2-\vv^2,\;2\uu\vv)", size=30)
        self.gat("que entorta")
        self.play(Create(ps), FadeIn(dX["g"]), GrowFromPoint(dX["sx"], VX4.P(0, 0)), GrowFromPoint(dX["sy"], VX4.P(0, 0)), run_time=0.8)
        self.pena(pl, dX["lx"], dX["ly"], lag=0.2)
        # a malha curva (um movimento): cópia da malha do plano u, v levada por φ
        self.gat("a reta u igual a um vira")
        mc = mm.copy()
        for x in mc.get_family():
            x._voando = True                    # a malha em movimento (origem → destino) não conta no R5
        self.play(ApplyPointwiseFunction(leva(VU4, VX4, mapC), mc), run_time=2.6)
        for x in mc.get_family():
            x._voando = False
        e_u = lin_px([VX4.px(*mapC(1, t)) for t in np.linspace(0, 1, 60)], CORAL, 3, z=7)
        r_u = TP(r"\Uc{u=1}:\ \X=1-\dfrac{\Y^2}{4}", *VX4.px(.62, 1.55), 26, "l")
        r_u.shift(RIGHT * 16 / 120)
        self.play(Create(e_u), run_time=0.6)
        self.pena(r_u)
        self.gat("a reta vê igual a um vira")
        e_v = lin_px([VX4.px(*mapC(t, 1)) for t in np.linspace(0, 1, 60)], AZC, 3, z=7)
        r_v = TP(r"\Vc{v=1}:\ \X=\dfrac{\Y^2}{4}-1", *VX4.px(-.62, 1.55), 26, "r")
        r_v.shift(LEFT * 16 / 120)
        self.play(Create(e_v), run_time=0.6)
        self.pena(r_v)
        self.gat("as células viram quadriláteros")
        realca(self, *[c.borda for c in mc], cor=MALHA, rt=0.4, wpx=3)
        self.gat("elas quase somem")
        cp = mc[0]
        self.play(cp.fill.animate.set_fill(cor_J(4 * (.125 ** 2 + .125 ** 2)) if False else mixh(CHAPA, LIMA, .15)), run_time=0.5)
        lp = leg("PEQUENA", VX4.px(.05, .03)[0] + 34, VX4.px(.05, .03)[1] + 44, GEO, "left", 26)
        self.pena(lp)
        self.gat("elas crescem")
        cg = mc[15]
        self.play(cg.fill.animate.set_fill(mixh(CHAPA, LIMA, .6)), run_time=0.5)
        lgd = TPt("GRANDE", *VX4.px(.5, 1.75), 26, BR, "left")
        self.pena(lgd)
        self.gat("aqui não existe um fator")
        an = []
        for k, c in enumerate(mc):
            i, j = k // 4, k % 4
            uc, vc = (i + .5) / 4, (j + .5) / 4
            an += [c.fill.animate.set_fill(cor_J(4 * (uc * uc + vc * vc))), c.borda.animate.set_stroke(BG_, W(1.5))]
        self.play(*an, run_time=1.4)
        self.gat("muda de ponto para ponto")
        fm = T("O FATOR MUDA DE PONTO PARA PONTO", 960, 1010, 32, "center", LIMA)
        self.pena(fm)
        self.marca("08")

        # ════ B4-2 · de perto, um paralelogramo ════
        self.an("B4-2")
        self.secao("DE PERTO, UM PARALELOGRAMO")
        self.gat("dá zoom numa célula")
        sai = [m for m in self.snap() if m not in (mc, e_u, e_v, dX["g"], dX["sx"], dX["sy"])]
        self.play(*[FadeOut(m) for m in sai], run_time=0.5)
        self.remove(*sai)
        zoom = VGroup(mc, e_u, e_v, dX["g"], dX["sx"], dX["sy"])
        self.play(ApplyPointwiseFunction(leva(VX4, VZ), zoom), run_time=2.0)
        gZ = papel(VZ, area=AZ, passo=.05).set_z_index(-10)
        gZ._sem_foco = True
        cM = celula(VZ, mapC, UM, UM + DL, VM, VM + DL, wb=3, N=40)
        pM = ponto_px(*VZ.px(*MXY), BR, 7)
        self.play(FadeOut(zoom), FadeIn(gZ), *anim_cel(cM), FadeIn(pM), run_time=1.0)
        self.remove(zoom)
        cs = {"M": (UM, VM, -26, 24), "N": (UM + DL, VM, 30, 18), "P": (UM + DL, VM + DL, 26, -14), "Q": (UM, VM + DL, -30, -8)}
        pts, labs = {}, {}
        for nome, (a, b, dx, dy) in cs.items():
            q = VZ.px(*mapC(a, b))
            if nome != "M":
                pts[nome] = ponto_px(*q, BR, 6)
            labs[nome] = TC(nome, q[0] + dx, q[1] + dy, 30, "c")
        self.play(*[FadeIn(p) for p in pts.values()], run_time=0.4)
        self.pena(*labs.values(), lag=0.1)
        lM = TC(r"\Ge{M=\varphi(0{,}75;\ 0{,}5)}", 1120, 720, 30, "l")
        self.pena(lM)
        col = self.col = Coluna36(self, 1120, 262)
        self.gat("o lado mn é a")
        sMN = lin_px([VZ.px(*mapC(UM + DL * t, VM)) for t in np.linspace(0, 1, 30)], CU, 6, z=8)
        self.play(Create(sMN), run_time=0.8)
        self.gat("quase a setinha da")
        A_px, B_px = VZ.px(*par_xy(1, 0)), VZ.px(*par_xy(0, 1))
        s1 = seta_px(VZ.px(*MXY), A_px, CU, 5, 20, z=9)
        self.play(GrowFromPoint(s1, VZ.P(*MXY)), run_time=0.8)
        l1 = TP(r"\pu\,\Du", A_px[0] + 30, A_px[1] + 80, 28, "l")
        self.pena(l1)
        a1 = mixl([("t", "ARCO"), ("m", r"MN\cong\left\|\pu\right\|\Du")], 1120, 0, 38)
        col.poe(a1)
        self.pena(a1)
        self.gat("em relação a u vezes")
        acende(self, (l1.f, BR), rt=0.6)
        self.gat("e o lado mq é")
        sMQ = lin_px([VZ.px(*mapC(UM, VM + DL * t)) for t in np.linspace(0, 1, 30)], CVV, 6, z=8)
        s2 = seta_px(VZ.px(*MXY), B_px, CVV, 5, 20, z=9)
        self.play(Create(sMQ), run_time=0.6)
        self.play(GrowFromPoint(s2, VZ.P(*MXY)), run_time=0.8)
        l2 = TP(r"\pv\,\Dv", B_px[0] - 18, B_px[1] - 74, 28, "r")
        self.pena(l2)
        a2 = mixl([("t", "ARCO"), ("m", r"MQ\cong\left\|\pv\right\|\Dv")], 1120, 0, 38)
        col.poe(a2)
        self.pena(a2)
        # o paralelogramo tracejado das duas setas e a área (estado do alvo 09: arcos, tracejado e ÁREA DE B juntos)
        self.gat("o paralelogramo dessas duas setas")
        tr_ = lin_px([VZ.px(*par_xy(a, b)) for a, b in ((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))], LIMA, 3, dash=(10, 8), z=10)
        self.play(Create(tr_), run_time=0.8)
        self.gat("e a área de um paralelogramo")
        a3 = mixl([("t", "ÁREA DE"), ("m", r"B\cong\Lm{\left\|\pu\wedge\pv\right\|}\Du\,\Dv")], 1120, 0, 38)
        col.poe(a3, gap=40)
        self.pena(a3)
        self.gat("a norma do produto vetorial")
        acende(self, (VGroup(*a3.p[1][0][6:8]), BR), rt=0.3)
        self.marca("09", agora=True)
        # a célula curva vira o paralelogramo das duas setas (antes da decolagem: o 2D da vista de cima = o PNG do cam = 0)
        self.gat("põe as duas setas")
        par = celula(VZ, par_xy, 0, 1, 0, 1, n=1, wb=3, N=40)
        self.play(Transform(cM.fill, par.fill), Transform(cM.borda, par.borda), FadeOut(cM.malha), FadeOut(sMN), FadeOut(sMQ),
                  *[FadeOut(p) for p in pts.values()], *[FadeOut(labs[k]) for k in "NPQ"], FadeOut(a1), FadeOut(a2), FadeOut(tr_), run_time=1.0)
        self.remove(cM.malha, sMN, sMQ, *pts.values(), *[labs[k] for k in "NPQ"], a1, a2, tr_)
        # decolagem: no mesmo quadro, o 2D (papel, paralelogramo, setas) sai e o PNG do cam = 0 entra
        pal = Palco36(self, "cena1", None, s=0.0, sobe=0.0)
        self.remove(gZ, cM.fill, cM.borda, s1, s2)
        self.add(pal.fundo)
        print(f"[decolagem] {self.lote} {self._aid} quadro {self.nq}")
        pal.prende(pM, "M")
        pal.prende(labs["M"], "M", -26, 24)
        pal.prende(l1, "w1", esq(l1) - A_px[0], centro(l1)[1] - A_px[1], ancora="l")
        pal.prende(l2, "w2", dir_(l2) - B_px[0], centro(l2)[1] - B_px[1], ancora="r")
        self.play(pal.tr["s"].animate(rate_func=smooth).set_value(1.0), FadeOut(a3), FadeOut(lM), run_time=2.6)
        self.remove(a3, lM)
        col.ls = []
        self.gat("fica em pé")
        self.play(pal.tr["sobe"].animate(rate_func=smooth).set_value(1.0), run_time=1.2)
        print(f"[sobe] {self.lote} {self._aid} quadro {self.nq - 1}")
        tp = pal.pt("topo")
        lk = TP(r"\vec k", tp[0] - 40, tp[1] + 60, 30, "r")
        tz = lin_px([(tp[0] + 30, tp[1]), (tp[0] + 250, tp[1])], LIMA, 2, dash=(6, 8), z=7)
        lw = TP(r"\Big(\pu\Du\Big)\wedge\Big(\pv\Dv\Big)", tp[0] + 270, tp[1], 30, "l")
        self.play(Create(tz), run_time=0.5)
        self.pena(lk, lw, lag=0.15, passo=0.035)
        self.marca("10", agora=True)
        self.gat("a altura dele é a área")
        h1a = T("ALTURA", 1180, 690, 32, "left", LIMA)
        h1b = T("= ÁREA DO PARALELOGRAMO", dir_(h1a) + 12, 690, 32, "left", LIMA)
        haste = lin_px([pal.pt("M"), pal.pt("topo")], LIMA, 6, z=8)
        voa(self, haste, h1a, rt=1.0)
        self.pena(h1b)
        # os deltas são números: saem para fora (glyph map 6, última passagem)
        self.gat("saem para fora")
        PA = [("e", "="), ("n1", r"\Lm{\Big\|}"), ("p1", r"\Big("), ("fu", r"\pu"), ("du", r"\Du"), ("p2", r"\Big)"), ("w", r"\wedge"), ("p3", r"\Big("),
              ("fv", r"\pv"), ("dv", r"\Dv"), ("p4", r"\Big)"), ("n2", r"\Lm{\Big\|}")]
        H2 = Lp(PA, 1180, 760, 32)
        self.escreve_voos(H2, [(lw.f, ["p1", "fu", "du", "p2", "w", "p3", "fv", "dv", "p4"])])
        H3 = Lp([("e", "="), ("du", r"\Du"), ("dv", r"\,\Dv"), ("n1", r"\Lm{\Big\|}"), ("fu", r"\pu"), ("w", r"\wedge"), ("fv", r"\pv"), ("n2", r"\Lm{\Big\|}")],
                1180, 850, 32)
        passo(self, H2, H3, [(k, k) for k in ("e", "du", "dv", "n1", "fu", "w", "fv", "n2")], copia=True, rt=1.4, nota="6 (os deltas saem dos parênteses)")
        # pouso: a mesma trajetória de volta, terminando na OrthographicCamera exata; o vetor vira um ponto sob M
        self.gat("vista de cima")
        self.play(FadeOut(lk), FadeOut(lw), FadeOut(tz), run_time=0.4)
        self.remove(lk, lw, tz)
        self.play(pal.tr["s"].animate(rate_func=smooth).set_value(0.0), pal.tr["sobe"].animate(rate_func=smooth).set_value(0.0), run_time=2.6)
        print(f"[pouso] {self.lote} {self._aid} quadro {self.nq - 1}")
        for m in (pM, labs["M"], l1, l2):
            m.clear_updaters()
            m._p3d = None                                   # de volta ao 2D: não está mais preso à cena 3D
        par2 = celula(VZ, par_xy, 0, 1, 0, 1, n=1, wb=3, N=40)
        s1b = seta_px(VZ.px(*MXY), A_px, CU, 5, 20, z=9)
        s2b = seta_px(VZ.px(*MXY), B_px, CVV, 5, 20, z=9)
        gZ2 = papel(VZ, area=AZ, passo=.05).set_z_index(-10)
        gZ2._sem_foco = True
        troca_para_2d(self, pal, [gZ2, par2, s1b, s2b])
        self.marca("B4-2")

        # ════ B4-3 · o jacobiano ════
        self.an("B4-3")
        self.gat("i jota e cá")             # o palco do pouso fica até a primeira linha do C6 (sem palco vazio)
        self.limpa_tudo()
        self.secao("O JACOBIANO")
        col6 = Coluna36(self, 80, 196)
        D1 = Lp([("pw", r"\pu\wedge\pv"), ("e", "="), ("det", r"\det\begin{bmatrix}\vec i&\vec j&\vec k\\ \xu&\yu&\Ge{0}\\ \xv&\yv&\Ge{0}\end{bmatrix}")],
                80, 0, 32)
        col6.poe(D1)
        D1._xy = (80, centro(D1)[1])
        self.pena(D1)
        c3 = casas(D1, D1._ix["det"][3:], 3, 3)
        self.gat("têm zero")
        acende(self, (VGroup(*[D1[0][k] for k in c3[(1, 2)] + c3[(2, 2)]]), GEO), rt=0.8)
        self.gat("sobra só o cá")
        D2 = Lp([("e", "="), ("p", r"(\xu\yv-\xv\yu)"), ("k", r"\,\vec k")], 110, 0, 32)
        col6.poe(D2, x=110)
        D2._xy = (110, centro(D2)[1])
        pi_ = D2._ix["p"]
        cel = lambda r, c: VGroup(*[D1[0][k] for k in c3[(r, c)]])
        passo(self, D1, D2, [(c3[(1, 0)], pi_[1:3]), (c3[(2, 1)], pi_[3:5]), (c3[(2, 0)], pi_[6:8]), (c3[(1, 1)], pi_[8:10]), (c3[(0, 2)], "k")],
              copia=True, rt=1.4, nota="6 (3 × 3 → (x_u y_v − x_v y_u) k: i e j somem)")
        self.gat("trocando linha por coluna")
        D3 = Lp([("e", "="), ("det", r"\det\begin{bmatrix}\xu&\xv\\ \yu&\yv\end{bmatrix}"), ("k", r"\,\vec k")], 110, 0, 32)
        col6.poe(D3, x=110)
        c2_ = casas(D3, D3._ix["det"][3:], 2, 2)
        # transposta: cada linha da matriz 3 × 3 (sem i, j, k) vira uma coluna da 2 × 2 (mapa explícito)
        passo(self, D1, D3, [(c3[(1, 0)], c2_[(0, 0)]), (c3[(1, 1)], c2_[(1, 0)]), (c3[(2, 0)], c2_[(0, 1)]), (c3[(2, 1)], c2_[(1, 1)]), (c3[(0, 2)], "k")],
              copia=True, rt=1.6, nota="6 (transposta: linha → coluna)")
        self.gat("o jacobiano de xis")
        D4 = Lp([("n", r"\left\|\pu\wedge\pv\right\|"), ("e", "="), ("J", r"\JJ")], 100, 0, 34)
        col6.poe(D4, x=100, gap=40)
        self.escreve_voos(D4, [(gl(D1, "pw"), [D4._ix["n"][k] for k in range(1, len(D4._ix["n"]) - 1)])])
        mol = moldura(70, pxof(D4.get_top())[1] - 16, 900, D4.height * 120 + 32, LIMA, 1.0, 3, 12)
        jt = T("JACOBIANO", 660, centro(D4)[1] + 10, 30, "left", LIMA)
        self.play(Create(mol), run_time=0.4)
        self.pena(jt)
        acende(self, (VGroup(*D4[0][D4._ix["J"][1]:D4._ix["J"][-1]]), LIMA), rt=0.3)
        self.gat("e a área da célula é")
        t5, D5 = mixLp("ÁREA DE", [("b", r"B\cong"), ("J", r"\JJ"), ("dd", r"\Du\,\Dv")], 80, 0, 36)
        y5 = col6.y_prox(D5, gap=44)
        VGroup(t5, D5).shift(UP * (PX(0, y5)[1] - D5.get_center()[1]))
        col6.registra(D5)
        self.pena(t5)
        self.escreve_voos(D5, [(gl(D4, "J"), "J")])
        self.gat("fator de ampliação")
        fl = leg("FATOR LOCAL DE ÁREA", dir_(D5) + 34, centro(D5)[1] + 10, LIMA, "left", 28)
        self.pena(fl)
        # C5 à direita
        col5 = Coluna36(self, 1120, 196)
        col5.GAP36 = 24
        # o palco: a célula de canto M (Δ encolhe; o zoom acompanha) e a miniatura do B4-1
        D = ValueTracker(.25)
        MS = (190, 1012)

        def vs():
            s = 75 / D.get_value()
            return Vw(MS[0] - MXY[0] * s, MS[1] + MXY[1] * s, s)

        def cel_d():
            d = D.get_value()
            return celula(vs(), mapC, UM, UM + d, VM, VM + d, wb=3, N=24)

        def par_d():
            d, v = D.get_value(), vs()
            w1, w2 = (2 * UM * d, 2 * VM * d), (-2 * VM * d, 2 * UM * d)
            q = [(MXY[0] + a * w1[0] + b * w2[0], MXY[1] + a * w1[1] + b * w2[1]) for a, b in ((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))]
            return lin_px([v.px(*p) for p in q], LIMA, 2.5, dash=(8, 7), z=9)
        cd, pd = cel_d(), par_d()
        pMs = ponto_px(*MS, BR, 7)
        lMs = TC("M", MS[0] - 24, MS[1] + 22, 28, "c")
        VMi = Vw(800, 1018, 130)
        mini = VGroup(*[celula(VMi, mapC, i / 4, (i + 1) / 4, j / 4, (j + 1) / 4, n=1, wb=1, N=16) for i in range(4) for j in range(4)])
        for k, c in enumerate(mini):
            i, j = k // 4, k % 4
            c.fill.set_fill(cor_J(4 * (((i + .5) / 4) ** 2 + ((j + .5) / 4) ** 2)))
            c.borda.set_stroke(BG_, W(1))
        lmM = TC(r"\Ge{M=\varphi(0{,}75;\ 0{,}5)}", 420, 1000, 26, "l")
        self.gat("na nossa grade")
        self.play(*anim_cel(cd), Create(pd), FadeIn(pMs), *[a for c in mini for a in (FadeIn(c.fill), Create(c.borda))], run_time=1.0)
        self.pena(lMs, lmM, lag=0.2)
        E1_ = Lp([("x", r"\X=\uu^2-\vv^2,"), ("y", r"\quad\Y=2\uu\vv")], 1120, 0, 32)
        col5.poe(E1_)
        self.pena(E1_)
        E2_ = Lp([("a", r"\dd{\X}{\uu}=2\uu"), ("b", r"\quad\dd{\X}{\vv}=-2\vv"), ("c", r"\quad\dd{\Y}{\uu}=2\vv"), ("d", r"\quad\dd{\Y}{\vv}=2\uu")], 1120, 0, 30)
        col5.poe(E2_)
        for k_, g_ in zip("abcd", ("em relação a u é dois u", "em relação a vê menos dois", "a de ípsilon em relação a u", "e em relação a vê dois u")):
            self.gat(g_)
            self.pena(parte(E2_, E2_._ix[k_], k_))
        self.gat("dois u vezes dois u")
        E3 = Lp([("J", r"\Jq"), ("e", "="), ("det", r"\det\begin{bmatrix}2\uu&-2\vv\\ 2\vv&2\uu\end{bmatrix}")], 1120, 0, 30)
        col5.poe(E3)
        E3._xy = (1120, centro(E3)[1])
        c5 = casas(E3, E3._ix["det"][3:], 2, 2)
        rhs = lambda k_, n: VGroup(*[E2_[0][i] for i in E2_._ix[k_][-n:]])
        ia = lambda k_, n: E2_._ix[k_][-n:]
        passo(self, E2_, E3, [(ia("a", 2), c5[(0, 0)]), (ia("b", 3), c5[(0, 1)]), (ia("c", 2), c5[(1, 0)]), (ia("d", 2), c5[(1, 1)])], copia=True, rt=1.4,
              nota="5 (as quatro derivadas → casas da matriz)")
        E3 = cresce(self, E3, [("e2", "="), ("pr", r"(2\uu)(2\uu)-(-2\vv)(2\vv)")], col=col5, nota="5 (det → produtos)")
        self.gat("quatro u ao quadrado")
        E3b = Lp([("e3", "="), ("r", r"\Lm{4\uu^2+4\vv^2}")], 1500, 0, 32)
        col5.poe(E3b, x=1500)
        self.escreve_voos(E3b, [(gl(E3, "pr"), "r")])
        self.gat("três vírgula vinte e cinco")
        E4 = Lp([("M", r"M:\ 4\cdot"), ("a", r"0{,}5625"), ("p", r"+4\cdot"), ("b", r"0{,}25")], 1120, 0, 30)
        col5.poe(E4)
        E4._xy = (1120, centro(E4)[1])
        num = lmM[0]
        self.escreve_voos(E4, [(VGroup(*num[4:8]), "a"), (VGroup(*num[9:12]), "b")])
        E4 = cresce(self, E4, [("e1", "="), ("c", r"2{,}25+1")], col=col5, nota="5 (M: 2,25 + 1)")
        E4 = cresce(self, E4, [("e2", "="), ("r", r"\Lm{3{,}25}")], voos=lambda B: [(gl(E4, "c").copy(), "r")], col=col5, nota="5 (= 3,25)")
        # a tabela do Δ
        Yt = pxof(E4.get_bottom())[1] + 64
        cols = (1150, 1330, 1530, 1740)
        cab = [TC(r"\Delta", cols[0], Yt, 28, "l"), mixl([("t", "EXATA", GEO), ("m", r"\approx")], cols[1], Yt, 28),
               TC(r"|J(M)|\,\Delta^2", cols[2], Yt, 28, "l"), T("RAZÃO", cols[3], Yt + 9, 26, "left", GEO, bold=False)]
        lin_t = lin_px([(1140, Yt + 30), (1890, Yt + 30)], GEO, 1.5, alpha=.4, z=3)
        self.gat("usando o jacobiano do canto")
        self.play(Create(lin_t), run_time=0.3)
        self.pena(*cab, lag=0.05, passo=0.03)
        realca(self, pMs, cor=LIMA, rt=0.1, wpx=4)
        dados = [(".25", "0{,}25", "0{,}2917", "0{,}2031", "1{,}44", "lado zero vírgula vinte e cinco", "um vírgula quarenta e quatro"),
                 (".1", "0{,}1", "0{,}03777", "0{,}03250", "1{,}16", "com lado zero vírgula um", "um vírgula dezesseis"),
                 (".05", "0{,}05", "0{,}008767", "0{,}008125", "1{,}08", "com zero vírgula zero cinco", "um vírgula zero oito"),
                 (".01", "0{,}01", "0{,}000330", "0{,}000325", "1{,}02", "com zero vírgula zero um", "um vírgula zero dois")]
        self.remove(cd, pd)
        cdd, pdd = always_redraw(cel_d), always_redraw(par_d)
        self.add(cdd, pdd)
        for k, (dv, d_, ex, jj, ra, g1, g2) in enumerate(dados):
            self.gat(g1)
            ld = TP(r"\Delta=" + d_, 420, 940, 28, "l")
            if k == 0:
                self.pena(ld)
                self._ld = ld
            else:
                ja_escrita(ld.f)
                self.play(D.animate.set_value(float(dv)), Transform(self._ld, ld), run_time=1.0)
            self.gat(g2)
            y = Yt + 68 * (k + 1)
            row = [TC(d_, cols[0], y, 30, "l"), TC(ex, cols[1], y, 30, "l"), TC(jj, cols[2], y, 30, "l"), TC(r"\Lm{%s}" % ra, cols[3], y, 30, "l")]
            voa(self, self._ld[1].copy(), row[0], rt=0.5)
            self.pena(*row[1:], lag=0.05, passo=0.03)
        cdd.clear_updaters()
        pdd.clear_updaters()
        self.gat("zero na origem")
        o0 = ponto_px(*VMi.px(0, 0), LIMA, 8)
        j0 = TC(r"J(0,0)=0", 1150, 0, 30, "l")
        j0.move_to(PX(1150 + j0.width * 60, Yt + 68 * 5 + 30))
        self.play(FadeIn(o0), run_time=0.4)
        realca(self, mini[0].borda, cor=LIMA, rt=0.3, wpx=3)
        self.pena(j0)
        self.gat("e oito no canto")
        o1 = ponto_px(*VMi.px(*mapC(1, 1)), LIMA, 8)
        j1 = TC(r"J(1,1)=8", 1150, 0, 30, "l")
        j1.move_to(PX(dir_(j0) + 50 + j1.width * 60, centro(j0)[1]))
        self.play(FadeIn(o1), run_time=0.4)
        realca(self, mini[15].borda, cor=LIMA, rt=0.3, wpx=3)
        self.pena(j1)
        self.marca("11")
        self.sai_fim()
