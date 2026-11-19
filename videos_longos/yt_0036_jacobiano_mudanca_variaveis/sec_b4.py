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
EMENDA_B41 = 830                                              # meio do vão entre o plano u, v (até ~722) e o x, y (de ~938), sob a seta φ
W1XY, W2XY = (2 * UM * DL, 2 * VM * DL), (-2 * VM * DL, 2 * UM * DL)


def par_xy(a, b):
    return (MXY[0] + a * W1XY[0] + b * W2XY[0], MXY[1] + a * W1XY[1] + b * W2XY[1])


def cor_J(J):
    return mixh("#2A2550", LIMA, min(1.0, J / 7) * .85)


class PB4(J36):
    ANTES = "O SINAL E O MÓDULO"
    CHIP = False                            # v2 §6.3: o chip saiu no fim do B3-3 (o B4 fala de outro J)

    def corpo(self):
        # o B3-3 terminou com o plano u, v e a malha 4 × 4: o lote começa com eles (sem animação)
        d4 = plano_b4()
        mm = malha44()
        for m in [d4["lx"], d4["ly"]] + [t[1] for t in d4["tk"]]:
            ja_escrita(m)
        self.fundo(VU4, rt=0)
        self.add(*todos_plano(d4), mm)
        self.an("B4-1")
        self.secao("A GRADE CURVA")
        dX = monta_plano(VX4, AX4, 1.15, 2.2, -1.1, -.05)
        ps, pl = phi_seta(760, 900, 260, r"\varphi(\uu,\vv)=(\uu^2-\vv^2,\;2\uu\vv)", size=30)
        self.gat("que entorta")
        self.fundo(VU4, VX4, emenda=EMENDA_B41)
        self.play(Create(ps), FadeIn(dX["g"]), GrowFromPoint(dX["sx"], VX4.P(0, 0)), GrowFromPoint(dX["sy"], VX4.P(0, 0)), run_time=0.8)
        self.pena(pl, dX["lx"], dX["ly"], lag=0.2)
        # a malha curva (um movimento): cópia da malha do plano u, v levada por φ
        self.gat("a reta u igual a um vira")
        mc = mm.copy()
        for x in mc.get_family():
            x._voando, x._par_l = True, frozenset()     # a malha em movimento: travessia (traço em voo), listada à parte
        self.play(ApplyPointwiseFunction(leva(VU4, VX4, mapC), mc), run_time=2.6)
        for x in mc.get_family():
            x._voando, x._par_l = False, None
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
        # v2 §1.3: a grade do x, y vira a da tela inteira e entra no zoom (anda junto); depois crossfade para o papel do zoom (passo 0,05)
        gX = papel(VX4, area=area_px(VX4, -200, 2100)).set_z_index(-10)
        for x in gX.get_family():
            x._sem_foco = True
        self.fundo(g=gX, rt=0.3, extra=[FadeOut(m) for m in sai])
        self.remove(*sai)
        # final K6: antes do zoom (0,6 s) o preenchimento do mapa de calor vai a 0; só a célula de M (a mesma do MNPQ) ganha chapa + malha.
        # O zoom mira essa célula e termina EXATAMENTE no enquadramento do MNPQ (leva(VX4, VZ) é a mesma vista): sem corte.
        cM = celula(VX4, mapC, UM, UM + DL, VM, VM + DL, wb=3, N=40)
        self.play(*[c.fill.animate.set_fill(opacity=0) for c in mc], *anim_cel(cM), run_time=0.6)
        for m in (self.h1, self.h2, self.wm):
            if m is not None:
                m.set_z_index(60)                                       # canto e logo por cima de tudo
        zoom = VGroup(mc, e_u, e_v, dX["g"], dX["sx"], dX["sy"], cM)
        for x in zoom.get_family():
            x._sem_margem = True                                        # o zoom leva as linhas para fora do quadro (câmera, não layout)
        self.play(ApplyPointwiseFunction(leva(VX4, VZ), zoom), ApplyPointwiseFunction(leva(VX4, VZ), gX), run_time=2.0)
        cM_ref = celula(VZ, mapC, UM, UM + DL, VM, VM + DL, wb=3, N=40)
        d_px = max(float(np.linalg.norm(a - b)) for a, b in zip(cM.borda.get_anchors()[::10], cM_ref.borda.get_anchors()[::10])) * 120
        print(f"[zoom] {self._aid} {self.t:.2f} cantos da célula no fim do zoom × MNPQ: {d_px:.2f} px")
        pM = ponto_px(*VZ.px(*MXY), BR, 7)
        resto_z = VGroup(mc, e_u, e_v, dX["g"], dX["sx"], dX["sy"])
        self.fundo(VZ, passo=.05, rt=0.4, extra=[FadeOut(resto_z), FadeIn(pM)])
        self.remove(resto_z)
        cs = {"M": (UM, VM, -26, 24), "N": (UM + DL, VM, 30, 18), "P": (UM + DL, VM + DL, 26, -14), "Q": (UM, VM + DL, -30, -8)}
        pts, labs = {}, {}
        for nome, (a, b, dx, dy) in cs.items():
            q = VZ.px(*mapC(a, b))
            if nome != "M":
                pts[nome] = ponto_px(*q, BR, 6)
            labs[nome] = TC(nome, q[0] + dx, q[1] + dy, 30, "c")
        self.play(*[FadeIn(p) for p in pts.values()], run_time=0.4)
        self.pena(*labs.values(), lag=0.1)
        # final K7: M = φ(0,75; 0,5) é a 1ª linha da coluna (topo), no tamanho de linha (dígito ≥ 26,7 px), branco; as linhas ARCO descem abaixo
        col = self.col = Coluna36(self, 1120, 200)
        lM = Lp([("a", r"M=\varphi(0{,}75;\ 0{,}5)")], 1120, 0, 40)
        col.poe(lM)
        self.pena(lM)
        self.gat("o lado mn é a")
        sMN = lin_px([VZ.px(*mapC(UM + DL * t, VM)) for t in np.linspace(0, 1, 30)], CU, 6, z=8)
        self.play(Create(sMN), run_time=0.8)
        self.gat("quase a setinha da")
        A_px, B_px = VZ.px(*par_xy(1, 0)), VZ.px(*par_xy(0, 1))
        s1 = seta_px(VZ.px(*MXY), A_px, CU, 5, 20, z=9)
        self.play(GrowFromPoint(s1, VZ.P(*MXY)), run_time=0.8)
        l1 = TP(r"\pu\,\Du", A_px[0] + 30, A_px[1] + 80, 28, "l")
        self.pena(l1)
        a1 = mixl([("t", "ARCO"), ("m", r"MN\cong\left\|\pu\right\|\Du")], 1120, 0, 40)
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
        if esq(l2) < 52:                                               # v2 (margem): ≥ 48 px da borda esquerda
            l2.shift(RIGHT * (52 - esq(l2)) / 120)
        self.pena(l2)
        a2 = mixl([("t", "ARCO"), ("m", r"MQ\cong\left\|\pv\right\|\Dv")], 1120, 0, 40)
        col.poe(a2)
        self.pena(a2)
        # o paralelogramo tracejado das duas setas e a área (estado do alvo 09: arcos, tracejado e ÁREA DE B juntos)
        self.gat("o paralelogramo dessas duas setas")
        tr_ = lin_px([VZ.px(*par_xy(a, b)) for a, b in ((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))], LIMA, 3, dash=(10, 8), z=10)
        self.play(Create(tr_), run_time=0.8)
        self.gat("e a área de um paralelogramo")
        a3 = mixl([("t", "ÁREA DE"), ("m", r"B\cong\Lm{\left\|\pu\wedge\pv\right\|}\Du\,\Dv")], 1120, 0, 40)
        col.poe(a3, gap=40)
        self.pena(a3)
        self.gat("a norma do produto vetorial")
        acende(self, (VGroup(*a3.p[1][0][6:8]), BR), rt=0.3)
        self.marca("09", agora=True)
        # a célula curva vira o paralelogramo das duas setas (antes da decolagem: o 2D da vista de cima = o PNG do cam = 0)
        self.gat("põe as duas setas")
        par = celula(VZ, par_xy, 0, 1, 0, 1, n=1, wb=3, N=40)
        # a grade da tela inteira encolhe para o chão da cena 3D (a troca 2D ↔ PNG continua exata) enquanto a célula vira o paralelogramo
        gZ = papel(VZ, area=AZ, passo=.05).set_z_index(-10)
        gZ._sem_foco = True
        self.fundo(g=gZ, rt=1.0, extra=[Transform(cM.fill, par.fill), Transform(cM.borda, par.borda), FadeOut(cM.malha), FadeOut(sMN), FadeOut(sMQ),
                                        *[FadeOut(p) for p in pts.values()], *[FadeOut(labs[k]) for k in "NPQ"], FadeOut(a1), FadeOut(a2), FadeOut(tr_)])
        self.remove(cM.malha, sMN, sMQ, *pts.values(), *[labs[k] for k in "NPQ"], a1, a2, tr_)
        # decolagem: no mesmo quadro, o 2D (papel do chão, paralelogramo, setas) sai e o PNG do cam = 0 entra (o 3D é liso: regra da série)
        pal = Palco36(self, "cena1", None, s=0.0, sobe=0.0)
        self._fundo = None
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
        h1a = T("ALTURA", 1180, 990, 32, "left", LIMA)
        h1b = T("= ÁREA DO PARALELOGRAMO", dir_(h1a) + 12, 990, 32, "left", LIMA)
        haste = lin_px([pal.pt("M"), pal.pt("topo")], LIMA, 6, z=8)
        # final (R5): a haste acende sobre o vetor e a caneta escreve ALTURA — nada atravessa o rótulo de ∂φ/∂u Δu, preso ao 3D ao lado
        self.play(Create(haste), run_time=0.4)
        self.pena(h1a)
        self.play(FadeOut(haste), run_time=0.3)
        self.remove(haste)
        self.pena(h1b)
        # os deltas são números: saem para fora (glyph map 6, última passagem)
        self.gat("saem para fora")
        PA = [("e", "="), ("n1", r"\Lm{\Big\|}"), ("p1", r"\Big("), ("fu", r"\pu"), ("du", r"\Du"), ("p2", r"\Big)"), ("w", r"\wedge"), ("p3", r"\Big("),
              ("fv", r"\pv"), ("dv", r"\Dv"), ("p4", r"\Big)"), ("n2", r"\Lm{\Big\|}")]
        H2 = Lp(PA, 1180, 760, 40)
        self.escreve_voos(H2, [(lw.f, ["p1", "fu", "du", "p2", "w", "p3", "fv", "dv", "p4"])])
        H3 = Lp([("e", "="), ("du", r"\Du"), ("dv", r"\,\Dv"), ("n1", r"\Lm{\Big\|}"), ("fu", r"\pu"), ("w", r"\wedge"), ("fv", r"\pv"), ("n2", r"\Lm{\Big\|}")],
                1180, 880, 40)
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
        self._fundo = gZ2
        self.fundo(VZ, passo=.05, rt=0.4)                            # a grade volta para a tela inteira logo depois do pouso
        self.marca("B4-2")

        # ════ B4-3 · o jacobiano (v2: §6.2 definição com figura; C5 inteira em degraus; tamanho 40) ════
        self.an("B4-3")
        self.secao("O JACOBIANO")                                       # final K9: o canto troca no 1º quadro da âncora
        self.gat("i jota e cá")             # o palco do pouso fica até a primeira linha do C6 (sem palco vazio)
        self.limpa_tudo()
        self.fundo(rt=0.3)                  # v2 §1.2: B4-3 sem gráfico → papel() na unidade padrão
        # ── fase 1 · palco à direita: o paralelogramo do B4-2 (vista de cima, reduzido) com as pernas de x_u, y_u, x_v, y_v ──
        MP = (1300, 880)
        SP = 1700                                                  # px por unidade de x, y (o B4-2 era 1900)
        P_ = lambda a, b: (MP[0] + (a * W1XY[0] + b * W2XY[0]) * SP, MP[1] - (a * W1XY[1] + b * W2XY[1]) * SP)
        pg = poly_px([P_(0, 0), P_(1, 0), P_(1, 1), P_(0, 1)], CHAPA, 1.0, z=1)
        pgb = lin_px([P_(0, 0), P_(1, 0), P_(1, 1), P_(0, 1), P_(0, 0)], MALHA, 3, z=2)
        sw1 = seta_px(P_(0, 0), P_(1, 0), CU, 5, 20, z=9)
        sw2 = seta_px(P_(0, 0), P_(0, 1), CVV, 5, 20, z=9)
        A1, A2 = P_(1, 0), P_(0, 1)
        hu = lin_px([MP, (A1[0], MP[1])], E1, 3, dash=(8, 7), z=3)        # perna horizontal de ∂φ/∂u Δu: x_u Δu (âmbar)
        vu = lin_px([(A1[0], MP[1]), A1], E2, 3, dash=(8, 7), z=3)        # perna vertical: y_u Δu (magenta)
        hv = lin_px([MP, (A2[0], MP[1])], E1, 3, dash=(8, 7), z=3)        # x_v Δv (para a esquerda: x_v < 0)
        vv_ = lin_px([(A2[0], MP[1]), A2], E2, 3, dash=(8, 7), z=3)
        lhu = TP(r"\xu\,\Du", (MP[0] + A1[0]) / 2, MP[1] + 30, 28, "c")
        lvu = TP(r"\yu\,\Du", A1[0] + 16, (MP[1] + A1[1]) / 2, 28, "l")
        lhv = TP(r"\xv\,\Dv", (MP[0] + A2[0]) / 2, MP[1] + 30, 28, "c")
        lvv = TP(r"\yv\,\Dv", A2[0] - 16, (MP[1] + A2[1]) / 2, 28, "r")
        pMp = ponto_px(*MP, BR, 7)
        lMp = TC("M", MP[0] + 4, MP[1] + 72, 28, "c")
        top = P_(1, 1)
        od = VGroup(sem_ctn(Circle(radius=13 / 120).move_to(PX(top[0] + 46, top[1] - 6)).set_stroke(BR, W(2.5)).set_fill(opacity=0)),
                    ponto_px(top[0] + 46, top[1] - 6, BR, 4)).set_z_index(9)                   # ⊙: o k aponta para fora da tela
        lod = TC(r"\vec k", top[0] + 80, top[1] - 6, 28, "l")
        self.play(FadeIn(pg), Create(pgb), GrowFromPoint(sw1, PX(*MP)), GrowFromPoint(sw2, PX(*MP)), FadeIn(pMp), run_time=0.9)
        self.pena(lMp)
        col6 = Coluna36(self, 80, 200)
        D1 = Lp([("pw", r"\pu\wedge\pv"), ("e", r"=\det"), ("det", r"\begin{bmatrix}\vec i&\vec j&\vec k\\ \xu&\yu&\Ge{0}\\ \xv&\yv&\Ge{0}\end{bmatrix}")],
                80, 0, 40)
        col6.poe(D1)
        D1._xy = (80, centro(D1)[1])
        c3 = casas(D1, D1._ix["det"], 3, 3)
        ent_u, ent_v = c3[(1, 0)] + c3[(1, 1)], c3[(2, 0)] + c3[(2, 1)]
        resto1 = [i for i in range(len(D1[0])) if i not in ent_u + ent_v]
        self.pena(parte(D1, resto1, "i, j, k e os zeros"))
        self.gat("em relação a u na segunda")
        self.play(Create(hu), Create(vu), run_time=0.6)
        self.pena(lhu, lvu, lag=0.2)
        voos(self, [(VGroup(*lhu.f[0][:2]), parte(D1, c3[(1, 0)], "x_u")), (VGroup(*lvu.f[0][:2]), parte(D1, c3[(1, 1)], "y_u"))], rt=0.8)
        self.gat("em relação a vê na terceira")
        self.play(Create(hv), Create(vv_), run_time=0.6)
        self.pena(lhv, lvv, lag=0.2)
        voos(self, [(VGroup(*lhv.f[0][:2]), parte(D1, c3[(2, 0)], "x_v")), (VGroup(*lvv.f[0][:2]), parte(D1, c3[(2, 1)], "y_v"))], rt=0.8)
        self.play(FadeIn(od), run_time=0.4)
        self.pena(lod)
        self.gat("têm zero")
        acende(self, (VGroup(*[D1[0][k] for k in c3[(1, 2)] + c3[(2, 2)]]), GEO), rt=0.8)
        # C6 (mapa M3): o menor 2 × 2 acende antes; os termos de i e de j saem; sobra (x_u y_v − x_v y_u) k
        self.gat("sobra só o cá")
        acende(self, (VGroup(*[D1[0][k] for k in c3[(1, 0)] + c3[(1, 1)] + c3[(2, 0)] + c3[(2, 1)]]), LIMA), rt=0.5)
        xe6 = pxof(D1[0][D1._ix["e"][0]].get_left())[0]
        D2 = deriva(self, D1, [("e", "="), ("p", r"(\xu\yv-\xv\yu)"), ("k", r"\,\vec k")],
                    lambda B: [([D1._ix["e"][0]], "e"), (c3[(1, 0)], B._ix["p"][1:3]), (c3[(2, 1)], B._ix["p"][3:5]), (c3[(2, 0)], B._ix["p"][6:8]),
                               (c3[(1, 1)], B._ix["p"][8:10]), (c3[(0, 2)], "k")], col6, x=xe6, rt=1.4,
                    nota="M3 C6 (3 × 3 → (x_u y_v − x_v y_u) k: i e j somem)")
        self.gat("trocando linha por coluna")
        # a transposta: cada linha da matriz (sem i, j, k) vira uma coluna da 2 × 2 (mapa explícito)
        D3 = Lp([("e", r"=\det"), ("det", r"\begin{bmatrix}\xu&\xv\\ \yu&\yv\end{bmatrix}"), ("k", r"\,\vec k")], 0, 0, 40)
        col6.poe(D3, x=xe6)
        D3._xy = (esq(D3), centro(D3)[1])
        c2_ = casas(D3, D3._ix["det"], 2, 2)
        estava = D1 in self.mobjects
        passo(self, D1, D3, [(D1._ix["e"], "e"), (c3[(1, 0)], c2_[(0, 0)]), (c3[(1, 1)], c2_[(1, 0)]), (c3[(2, 0)], c2_[(0, 1)]),
                             (c3[(2, 1)], c2_[(1, 1)]), (c3[(0, 2)], "k")], copia=True, rt=1.6, nota="M3 C6 (transposta: linha → coluna)")
        if estava and D1 not in self.mobjects:
            self.add(D1)
        self.gat("o jacobiano de xis")
        D4 = Lp([("n", r"\left\|\pu\wedge\pv\right\|"), ("e", "="), ("J", r"\JJ")], 100, 0, 48)          # linha-chave: ≥ 32 px
        col6.poe(D4, x=100, gap=44)
        self.escreve_voos(D4, [(gl(D1, "pw"), [D4._ix["n"][k] for k in range(1, len(D4._ix["n"]) - 1)])])
        mol = moldura(70, pxof(D4.get_top())[1] - 16, 790, D4.height * 120 + 32, LIMA, 1.0, 3, 12)
        jt = T("JACOBIANO", 640, centro(D4)[1] + 10, 30, "left", LIMA)
        self.play(Create(mol), run_time=0.4)
        self.pena(jt)
        acende(self, (VGroup(*D4[0][D4._ix["J"][1]:D4._ix["J"][-1]]), LIMA), rt=0.3)
        self.gat("e a área da célula é")
        t5, D5 = mixLp("ÁREA DE", [("b", r"B\cong"), ("J", r"\JJ"), ("dd", r"\Du\,\Dv")], 80, 0, 40)
        y5 = col6.y_prox(D5, gap=44)
        VGroup(t5, D5).shift(UP * (PX(0, y5)[1] - D5.get_center()[1]))
        col6.registra(D5)
        self.escreve_voos(D5, [(gl(D4, "J"), "J")])
        self.pena(t5)
        self.gat("fator de ampliação")
        fl = leg("FATOR LOCAL DE ÁREA", 100, pxof(D5.get_bottom())[1] + 40, LIMA, "left", 28)
        self.pena(fl)
        # ── fase 2 · o C6 sai; o paralelogramo cede lugar à célula de M que encolhe (palco à esquerda); C5 na coluna da direita ──
        self.gat("na nossa grade")
        sai6 = [m for m in self.snap() if m not in (pg, pgb, sw1, sw2, pMp)]
        self.play(*[FadeOut(m) for m in sai6], run_time=0.5)
        self.remove(*sai6)
        D = ValueTracker(.25)
        MS = (300, 760)

        def vs():
            s = 120 / D.get_value()
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
        lMs = TC("M", MS[0] - 26, MS[1] + 24, 28, "c")
        for x in VGroup(pg, pgb, sw1, sw2, pMp).get_family():
            x._voando = True
        self.play(Transform(VGroup(pg, pgb), VGroup(cd.fill, cd.borda)), FadeOut(sw1), FadeOut(sw2), Transform(pMp, pMs), FadeIn(cd.malha),
                  Create(pd), run_time=1.0)
        self.remove(pg, pgb, sw1, sw2, pMp)
        self.add(cd, pd, pMs)
        VMi = Vw(720, 980, 130)
        mini = VGroup(*[celula(VMi, mapC, i / 4, (i + 1) / 4, j / 4, (j + 1) / 4, n=1, wb=1, N=16) for i in range(4) for j in range(4)])
        for k, c in enumerate(mini):
            i, j = k // 4, k % 4
            c.fill.set_fill(cor_J(4 * (((i + .5) / 4) ** 2 + ((j + .5) / 4) ** 2)))
            c.borda.set_stroke(BG_, W(1))
        lmM = Lp([("M", r"\Ge{M=\varphi(}"), ("a", r"\Ge{0{,}75}"), ("s", r"\Ge{;\ }"), ("b", r"\Ge{0{,}5}"), ("f", r"\Ge{)}")], 80, 1000, 30)
        self.play(*[a for c in mini for a in (FadeIn(c.fill), Create(c.borda))], run_time=0.8)
        self.pena(lMs, lmM, lag=0.2)
        CX5 = 1000
        col5 = Coluna36(self, CX5, 200)
        col5.GAP36 = 28
        E1_ = Lp([("x", r"\X=\uu^2-\vv^2,"), ("y", r"\qquad\Y=2\uu\vv")], CX5, 0, 40)
        col5.poe(E1_)
        self.pena(E1_)
        # C5.2: cada derivada nasce a caneta embaixo da sua fórmula
        E2_ = Lp([("a", r"\dd{\X}{\uu}=2\uu"), ("b", r"\quad\dd{\X}{\vv}=-2\vv"), ("c", r"\quad\dd{\Y}{\uu}=2\vv"), ("d", r"\quad\dd{\Y}{\vv}=2\uu")], CX5, 0, 40)
        col5.poe(E2_)
        for k_, g_ in zip("abcd", ("em relação a u é dois u", "em relação a vê menos dois", "a de ípsilon em relação a u", "e em relação a vê dois u")):
            self.gat(g_)
            self.pena(parte(E2_, E2_._ix[k_], k_))
        # C5.3: as derivadas voam para a matriz
        E3 = Lp([("J", r"\Jq"), ("e", r"=\det"), ("det", r"\begin{bmatrix}2\uu&-2\vv\\ 2\vv&2\uu\end{bmatrix}")], CX5, 0, 40)
        col5.poe(E3)
        E3._xy = (CX5, centro(E3)[1])
        c5 = casas(E3, E3._ix["det"], 2, 2)
        ia = lambda k_, n: E2_._ix[k_][-n:]
        estava = E2_ in self.mobjects
        passo(self, E2_, E3, [(ia("a", 2), c5[(0, 0)]), (ia("b", 3), c5[(0, 1)]), (ia("c", 2), c5[(1, 0)]), (ia("d", 2), c5[(1, 1)])], copia=True, rt=1.4,
              nota="M4 C5.3 (as quatro derivadas → casas da matriz)")
        if estava and E2_ not in self.mobjects:
            self.add(E2_)
        xe5 = pxof(E3[0][E3._ix["e"][0]].get_left())[0]
        # C5.4–C5.6 (mapas): os produtos, o par de sinais −(− em ALERTA, e o + no lugar
        self.gat("dois u vezes dois u")
        E4 = deriva(self, E3, [("e", "="), ("a", r"(2\uu)(2\uu)"), ("m", "-"), ("b", r"(-2\vv)(2\vv)")],
                    lambda B: [([E3._ix["e"][0]], "e"), (c5[(0, 0)] + c5[(1, 1)], [B._ix["a"][k] for k in (1, 2, 5, 6)]),
                               (c5[(0, 1)] + c5[(1, 0)], [B._ix["b"][k] for k in (1, 2, 3, 6, 7)])], col5, x=xe5, rt=1.2,
                    nota="M4 C5.4 (det → (2u)(2u) − (−2v)(2v))")
        a4, b4 = E4._ix["a"], E4._ix["b"]
        E5 = deriva(self, E4, [("e", "="), ("a", r"4\uu^2"), ("m", "-"), ("b", r"(-4\vv^2)")],
                    lambda B: [("e", "e"), ([a4[1], a4[5]], [B._ix["a"][0]]), ([a4[2], a4[6]], [B._ix["a"][1]]), ("m", "m"),
                               ([b4[0]], [B._ix["b"][0]]), ([b4[1]], [B._ix["b"][1]]), ([b4[2], b4[6]], [B._ix["b"][2]]), ([b4[3], b4[7]], [B._ix["b"][3]]),
                               ([b4[8]], [B._ix["b"][5]])], col5, x=xe5, rt=1.2, nota="M4 C5.5 (= 4u² − (−4v²))")
        acende(self, (VGroup(E5[0][E5._ix["m"][0]], E5[0][E5._ix["b"][1]]), AL), rt=0.6)          # −(− em ALERTA
        self.gat("quatro u ao quadrado")
        m5, b5 = E5._ix["m"], E5._ix["b"]
        E6 = deriva(self, E5, [("e", "="), ("a", r"4\uu^2"), ("p", "+"), ("b", r"4\vv^2")],
                    lambda B: [("e", "e"), ("a", "a"), ([m5[0], b5[1]], "p"), (b5[2:5], "b")], col5, x=xe5, rt=1.0,
                    nota="M4 C5.6 (−(− vira +)")
        # as linhas que já serviram saem; J = 4u² + 4v² sobe para o topo da coluna (regra da série)
        self.gat("no ponto m")
        Jt = Lp([("J", r"\Jq"), ("e", "="), ("a", r"\Lm{4\uu^2+4\vv^2}")], CX5, 0, 40)
        Jt.move_to(PX(CX5 + Jt.width * 60, 240))
        ja_escrita(Jt)
        velhas = [E1_, E2_, E3, E4, E5]
        self.play(*[FadeOut(m) for m in velhas], run_time=0.4)  # final K12: troca de página em dois tempos (sai, depois sobe)
        self.play(ReplacementTransform(E6, Jt), run_time=0.6)
        self.remove(*velhas)
        col5.ls = [Jt]
        # C5.7: M = (0,75; 0,5): 4·(0,75)² + 4·(0,5)² — o 0,75 e o 0,5 voam da legenda M = φ(0,75; 0,5)
        self.gat("zero vírgula setenta e cinco")
        E7 = Lp([("P", r"M=(0{,}75;\ 0{,}5):\ "), ("q4", r"4\cdot"), ("ua", "("), ("u", r"0{,}75"), ("ub", ")^2"), ("p", "+"), ("r4", r"4\cdot"),
                 ("va", "("), ("v", r"0{,}5"), ("vb", ")^2")], CX5, 0, 40)
        col5.poe(E7)
        E7._xy = (CX5, centro(E7)[1])
        self.escreve_voos(E7, [(gl(lmM, "a"), "u"), (gl(lmM, "b"), "v")])
        # C5.8 (mapas): 4·(0,75)² → 4·0,5625 → 2,25 · 4·(0,5)² → 4·0,25 → 1 · somando, 3,25
        self.gat("dois vírgula vinte e cinco")
        xe7 = CX5 + 40                                              # a linha toda cabe antes de x = 1872
        E8 = deriva(self, E7, [("e", "="), ("q4", r"4\cdot"), ("u", r"0{,}5625"), ("p", "+"), ("r4", r"4\cdot"), ("v", r"0{,}25")],
                    lambda B: [("q4", "q4"), (E7._ix["ua"] + E7._ix["u"] + E7._ix["ub"], "u"), ("p", "p"), ("r4", "r4"),
                               (E7._ix["va"] + E7._ix["v"] + E7._ix["vb"], "v")], col5, x=xe7, rt=1.0, nota="M4 C5.8 (os quadrados)")
        E8 = cresce(self, E8, [("e2", "="), ("c", r"2{,}25+1")],
                    voos=lambda B: [(VGroup(*[E8[0][i] for i in E8._ix["q4"] + E8._ix["u"]]).copy(), B._ix["c"][:4]),
                                    (VGroup(*[E8[0][i] for i in E8._ix["r4"] + E8._ix["v"]]).copy(), B._ix["c"][5:])], col=col5, nota="M4 C5.8 (= 2,25 + 1)")
        self.gat("somando")
        E8 = cresce(self, E8, [("e3", "="), ("r", r"\Lm{3{,}25}")], voos=lambda B: [(gl(E8, "c").copy(), "r")], col=col5, nota="M4 C5.8 (= 3,25)")
        # a tabela do Δ (abaixo da conta)
        Yt = pxof(E8.get_bottom())[1] + 58
        cols = (CX5 + 10, CX5 + 200, CX5 + 410, CX5 + 680)
        cab = [TC(r"\Delta", cols[0], Yt, 32, "l"), mixl([("t", "EXATA", GEO), ("m", r"\approx")], cols[1], Yt, 32),
               TC(r"|J(M)|\,\Delta^2", cols[2], Yt, 32, "l"), T("RAZÃO", cols[3], Yt + 9, 28, "left", GEO, bold=False)]
        lin_t = lin_px([(CX5, Yt + 32), (1870, Yt + 32)], GEO, 1.5, alpha=.4, z=3)
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
            ld = TP(r"\Delta=" + d_, 80, 930, 30, "l")
            if k == 0:
                self.pena(ld)
                self._ld = ld
            else:
                ja_escrita(ld.f)
                self.play(D.animate.set_value(float(dv)), Transform(self._ld, ld), run_time=1.0)
            self.gat(g2)
            y = Yt + 60 * (k + 1)
            row = [TC(d_, cols[0], y, 40, "l"), TC(ex, cols[1], y, 40, "l"), TC(jj, cols[2], y, 40, "l"), TC(r"\Lm{%s}" % ra, cols[3], y, 40, "l")]
            voa(self, self._ld[1].copy(), row[0], rt=0.5)
            self.pena(*row[1:], lag=0.05, passo=0.03)
        cdd.clear_updaters()
        pdd.clear_updaters()
        # C5.9: J(0, 0) = 4·0² + 4·0² = 0 · J(1, 1) = 4·1² + 4·1² = 8 (os cantos acendem na miniatura do B4-1)
        self.gat("na origem")
        o0 = ponto_px(*VMi.px(0, 0), LIMA, 8)
        self.play(FadeIn(o0), run_time=0.3)
        realca(self, mini[0].borda, cor=LIMA, rt=0.3, wpx=3)
        J0 = Lp([("J", r"J(0,0)"), ("e", "="), ("a", r"4\cdot 0^2+4\cdot 0^2"), ("e2", "="), ("r", "0")], CX5, 0, 40)
        J0.move_to(PX(CX5 + J0.width * 60, Yt + 60 * 5 + 50))       # abaixo da tabela
        col5.registra(J0)
        J0._xy = (CX5, centro(J0)[1])
        self.pena(J0)
        self.gat("no canto um, um")
        o1 = ponto_px(*VMi.px(*mapC(1, 1)), LIMA, 8)
        self.play(FadeIn(o1), run_time=0.3)
        realca(self, mini[15].borda, cor=LIMA, rt=0.3, wpx=3)
        J1 = deriva(self, J0, [("J", r"J(1,1)"), ("e", "="), ("a", r"4\cdot 1^2+4\cdot 1^2"), ("e2", "="), ("r", r"\Lm{8}")],
                    lambda B: [("e", "e"), ([J0._ix["a"][k] for k in (0, 1, 3, 4, 5, 6, 8)], [B._ix["a"][k] for k in (0, 1, 3, 4, 5, 6, 8)]), ("e2", "e2")],
                    col5, x=CX5, rt=1.0, nota="C5.9 J(1, 1) a partir de J(0, 0)")
        self.marca("11")
        self.sai_fim()
