"""yt_0037 · B6 · a área inteira debaixo do sino — v2 (alvo 08 no B6-1; alvo v2_03 no B6-2; E25–E36). B6-1: a curva e^(−x²) começa a se
desenhar no 1º quadro (E25); I(a); a coluna T1…T5 em escala G1 (GM12, Fubini); em "o sino girado", corte para o gauss na câmera oblíqua com o
sino crescendo (E27), alfa dentro de x ≥ 40 (E28). B6-2: os discos no chão; D_a, D_{a√2} e a√2 fora do sino com guia (E29); em "região maior",
a câmera sobe à vista de cima e o 2D do alvo v2_03 entra no mesmo quadro (papel, quadrado, sino de cima, os dois discos, os raios a e a√2, Q_a,
D_a, D_{a√2}); nada do 2D do B6-1 (E31); a coluna com o chip I(a)² e 6 linhas (GM13), a tabela com o a crescendo (o sino de cima encolhe no
quadrado), o limite e √π em duas linhas; o cartão do canto ganha ✓. B6-3: a curva normal, a substituição, GM14 e 1/√(2π) escrito por inteiro
com o √(2π) voando da coluna (E36); a área vira 1 = 100 %."""
from v2kit import *

VC = Vw(500, 860, 150, 500)       # a curva (B6-1 e B6-3): pico em y = 360
X6 = 1000
SCG, RQ = 1.15, 1.25
RC = RQ * math.sqrt(2)
C1 = (470.0, 620.0)                # vista de cima (alvo v2_03): a origem
HQ = 255.0                         # meio lado do quadrado Q_a em px
K1 = HQ / (SCG * RQ)               # px por unidade do mundo (≈ 177,4)
PXU = K1 * SCG                     # px por unidade de x (a = 1,25): 204
RCP = HQ * math.sqrt(2)            # raio do circunscrito em px (≈ 360,6)
PAP = (88.0, 238.0, 853.0, 1003.0)  # o papel da vista de cima (alvo)
GRL = "#3A3470"


def ordx(m, key):
    return sorted(sel(m, key), key=lambda i: m[0][i].get_center()[0])


def sup_sub(m, key):
    ix_ = sel(m, key)
    base = max(ix_, key=lambda i: m[0][i].height)
    resto = [i for i in ix_ if i != base]
    cy = m[0][base].get_center()[1]
    up = sorted([i for i in resto if m[0][i].get_center()[1] >= cy], key=lambda i: m[0][i].get_center()[0])
    lo = sorted([i for i in resto if m[0][i].get_center()[1] < cy], key=lambda i: m[0][i].get_center()[0])
    return base, up, lo


def gl(m, key):
    return VGroup(*[m[0][i] for i in sel(m, key)])


def curva_palco(f, a0, a1):
    v = VC
    d = {"g": papel_v(v, (-3.0, 3.0, 0, 1.2))}
    d["sx"], d["sy"], d["lx"], d["ly"] = eixos_xy(v, -3.05, 3.15, -.05, 1.22, size=40)
    xs = np.linspace(a0, a1, 241)
    d["c"] = lin_px([v.px(x, f(x)) for x in xs], CI, 4, z=6)
    return d


def sombra(f, s0, s1, cor=None):
    xx = np.linspace(s0, s1, 161)
    return poly_px([VC.px(s0, 0)] + [VC.px(x, f(x)) for x in xx] + [VC.px(s1, 0)], cor or mixh(BG_, CI, .25), 1.0, z=2)


def heat(a, n=200):
    """O sino visto de cima dentro do quadrado [−a, a]² (cor por altura, a mesma rampa do 3D), em px: lado 2·HQ."""
    u = (np.arange(n) + .5) / n * 2 - 1
    X, Y = np.meshgrid(u * a, -u * a)
    v = np.exp(-(X * X + Y * Y))
    t = np.power(np.clip(v, 0, 1), .85)[..., None]
    rgb = hx("#10243A") * (1 - t) + hx(CI) * t
    return img_px(rgb, C1[0] - HQ, C1[1] - HQ, 2 * HQ, 2 * HQ, z=2)


def papel_topo():
    """FINAL (K2): o papel da vista de cima em TELA INTEIRA, nascendo da origem C1 e com linhas a cada a/4 (63,75 px) de borda a borda."""
    return papel(Vw(C1[0], C1[1], HQ), passo=0.25).set_z_index(-10)


class PB6(B37):
    ANTES = "O DISCO QUE PASSA PELA ORIGEM"
    SUB = "A RETA-SONDA SAI DO POLO"
    CARTAO = True

    def corpo(self):
        # ── B6-1 · o sino inteiro (alvo 08) ──
        self.an("B6-1")
        A_ = 1.6
        f1 = lambda x: math.exp(-x * x)
        d = curva_palco(f1, -2.95, 2.95)
        self.grade = d["g"]
        self.play(FadeIn(d["g"]), GrowFromPoint(d["sx"], VC.P(0, 0)), GrowFromPoint(d["sy"], VC.P(0, 0)), Create(d["c"]), run_time=1.0)   # E25: a curva no 1º quadro
        self.secao("O SINO INTEIRO")
        self.subt("A INTEGRAL DE GAUSS")
        self.pena(d["lx"], d["ly"], lag=0.05)
        self.gat("a promessa do começo")
        self.gat("a curva do sino é")
        realca(self, d["c"], cor=CI, rt=0.6)
        lc = TP(r"\Ci{e^{-\X^2}}", *VC.px(1.3, .62), 40, "l")
        self.pena(lc)
        self.gat("a primitiva existe mas")
        sp = leg("SEM PRIMITIVA ELEMENTAR", 265, 300, AL, "center", 30)          # K13: à esquerda do eixo y, longe da coluna
        self.pena(sp, passo=0.025)
        self.gat("chama de i de á")
        At = ValueTracker(A_)
        sh = always_redraw(lambda: sombra(f1, -At.get_value(), At.get_value()))
        self.add(At)
        self.play(FadeIn(sh), run_time=0.6)
        ta = always_redraw(lambda: TC("-a", VC.px(-At.get_value(), 0)[0], VC.px(0, 0)[1] + 34, 40, "c", caneta=False))
        tb = always_redraw(lambda: TC("a", VC.px(At.get_value(), 0)[0], VC.px(0, 0)[1] + 34, 40, "c", caneta=False))
        ch = always_redraw(lambda: chave_px(VC.px(-At.get_value(), 0)[0], VC.px(At.get_value(), 0)[0], VC.px(0, 0)[1] + 66, CI, 2.5))
        lI = TP("I(a)", VC.px(0, 0)[0], VC.px(0, 0)[1] + 114, 40, "c")
        self.play(FadeIn(ta), FadeIn(tb), Create(ch), run_time=0.5)
        self.pena(lI)
        T1 = col(L([("I", "I(a)"), ("eq", "="), ("i", r"\displaystyle\int_{-a}^{a}"), ("f", r"\Ci{e^{-\X^2}}"), ("dx", r"\,\dX")], X6, 215, 44))
        bi, ui, li = sup_sub(T1, "i")
        escreve_seq(self, T1, [(lI.f, "I"), (ta, li), (tb, ui)], rt_voo=0.8, passo=0.04)
        origem(self, "I(a) e os limites −a, a", "chave I(a) e marcas do eixo (voos)")
        self.gat("deixa á crescer")
        self.play(At.animate(rate_func=smooth).set_value(2.5), run_time=1.6)
        self.play(At.animate(rate_func=smooth).set_value(A_), run_time=1.2)
        self.gat("elevar ao quadrado")
        T2 = col(L([("I2", r"I(a)^2"), ("eq", "="), ("Ia", "I(a)"), ("c", r"\cdot"), ("Ib", "I(a)")], X6, 0, 44))
        abaixo(T1, T2, X6, 26)
        self.play(At.animate(rate_func=there_and_back).set_value(2.0), run_time=1.0)
        self.pena(T2)
        # GM12: I(a)·I(a) → ∫ e^(−y²)[∫ e^(−x²) dx] dy → ∬_Q e^(−x²) e^(−y²) dA → ∬_Q e^(−(x²+y²)) dA
        self.gat("escreve uma com xis")
        realca(self, d["c"], cor=CI, rt=0.5)
        T3 = col(L([("eq", "="), ("io", r"\displaystyle\int_{-a}^{a}"), ("fy", r"\Ci{e^{-\Y^2}}"), ("lb", r"\Big["), ("ii", r"\int_{-a}^{a}"), ("fx", r"\Ci{e^{-\X^2}}"),
                    ("dx", r"\,\dX"), ("rb", r"\Big]"), ("dy", r"\,\dY")], X6, 0, 44))
        abaixo(T2, T3, X6, 30)
        gmap(self, 12, T2, T3, [("eq", "eq"), ("Ia", ["io", "fy", "dy"]), ("Ib", ["lb", "ii", "fx", "dx", "rb"])], rt=1.5,
             nota="a) uma com x, a outra com y")
        degrau(self, "B6-1 Fubini", "I(a)² = I(a)·I(a) = ∫ e^(−y²)[∫ e^(−x²) dx] dy")
        self.gat("pelo teorema de fubini")
        self.play(At.animate(rate_func=there_and_back).set_value(2.0), run_time=1.4)
        T4 = col(L([("eq", "="), ("ii", r"\iint_{Q_a}"), ("fx", r"\Ci{e^{-\X^2}}"), ("fy", r"\,\Ci{e^{-\Y^2}}"), ("dA", r"\,dA")], X6, 0, 44))
        abaixo(T3, T4, X6, 30)
        bo, uo, lo = sup_sub(T3, "io")
        bi2, ui2, li2 = sup_sub(T3, "ii")
        qa = [k for k in sel(T4, "ii") if T4[0][k].height < T4[0][sel(T4, "ii")[0]].height * .6] or sel(T4, "ii")[1:]
        big = [k for k in sel(T4, "ii") if k not in qa]
        gmap(self, 12, T3, T4, [("eq", "eq"), ([bo, bi2], big), (uo + lo + ui2 + li2, qa), ("fx", "fx"), ("fy", "fy"), (["dx", "dy"], "dA")], rt=1.5,
             nota="b) Fubini no quadrado Q_a")
        degrau(self, "B6-1 Fubini", "= ∬_{Q_a} e^(−x²) e^(−y²) dA")
        self.gat("que vira i de á")
        acende(self, (T3[0][sel(T3, "lb")[0]:sel(T3, "rb")[-1] + 1], CI), rt=1.0)
        acende(self, (lI.f, CI), rt=0.6)
        self.gat("a de fora dá i")
        self.play(At.animate(rate_func=there_and_back).set_value(1.25), run_time=1.0)
        self.gat("o produto das duas")
        T5 = col(L([("eq", "="), ("ii", r"\iint_{Q_a}"), ("f", r"\Ci{e^{-(\X^2+\Y^2)}}"), ("dA", r"\,dA")], X6, 0, 44))
        abaixo(T4, T5, X6, 30)
        fx4, fy4, f5 = ordx(T4, "fx"), ordx(T4, "fy"), ordx(T5, "f")
        gmap(self, 12, T4, T5, [("eq", "eq"), ("ii", "ii"), (fx4[0:1] + fy4[0:1], f5[0:1]), (fx4[1:2] + fy4[1:2], f5[1:2]), (fx4[2:4], f5[3:5]),
                                (fy4[2:4], f5[6:8]), ("dA", "dA")], rt=1.4, nota="c) o produto vira e^(−(x²+y²))")
        degrau(self, "B6-1 Fubini", "= ∬_{Q_a} e^(−(x²+y²)) dA")
        self.gat("xis ao quadrado mais ípsilon")
        realca(self, d["c"], cor=CI, rt=0.5)
        tela1 = [T1, T2, T3, T4, T5]
        # o sino girado: corte para o gauss na câmera oblíqua, com o sino crescendo (E27); a curva sai no mesmo quadro
        self.gat("o sino girado")
        pal = Palco37(self, "gauss", CAM_GAUSS2, cresce=0.0, discos=0.0)
        pal.fundo.op.set_value(1.0)
        ta.clear_updaters()
        tb.clear_updaters()
        ch.clear_updaters()
        sh.clear_updaters()
        palco1 = [m for m in self.snap() if m not in tela1 and m is not pal.fundo and pxof(m.get_center())[0] < 1000] + [self.grade]
        for m in palco1:
            for x in m.get_family():
                x._esc = True
        self.remove(*palco1, At)
        self.add(pal.fundo)
        self.grade = None
        lx = pal.prende(TC(r"\X", 0, 0, 40, "c"), "ex")
        ly = pal.prende(TC(r"\Y", 0, 0, 40, "c"), "ey", 40, -10)
        self.play(*pal.anim(2.0, cresce=1.0), run_time=2.0)
        self.pena(lx, ly, lag=0.05)
        self.marca("08")
        # ── B6-2 · o confronto (alvo v2_03) ──
        self.an("B6-2")
        self.subt("ENTRE DOIS DISCOS")
        self.gat("entre dois discos")
        self.play(*pal.anim(1.6, discos=1.0), run_time=1.6)
        self.gat("o disco de raio á inscrito")
        lDa = ok3d(pal.prende(TP(r"\Az{D_a}", 0, 0, 40, "c"), "cin", -64, 34))
        self.pena(lDa)
        self.gat("o disco de raio á raiz")
        lDc = ok3d(pal.prende(TP(r"\Co{D_{a\sqrt{2}}}", 0, 0, 40, "c"), "ccirc", -86, 20))
        self.pena(lDc)
        self.gat("a meia diagonal é")
        dg = always_redraw(lambda: lin_px([pal.pt("origem"), pal.pt("quina")], CORAL, 3, dash=(9, 6), z=7))
        lr = ok3d(pal.prende(TP(r"\Co{a\sqrt{2}}", 0, 0, 40, "l"), "quina", 44, 20, "l"))      # E29: no chão, fora do sino, com guia até a quina
        gr = always_redraw(lambda: seta_px((pxof(lr.get_left())[0] - 4, pxof(lr.get_center())[1]), (pal.pt("quina")[0] + 6, pal.pt("quina")[1] + 2),
                                           CORAL, 2, 10, z=7))
        for x in gr.get_family():
            x._guia_de = lr.f
        self.play(Create(dg), run_time=0.6)
        self.pena(lr, extra=[Create(gr)])
        # a câmera sobe pelo relógio a partir de "como o integrando é" (a vista de cima completa chega depois de "região maior", E27);
        # enquanto sobe, a coluna vira o chip I(a)² e a linha das inclusões se escreve (D_a e D_{a√2} voam das placas)
        self.gat("como o integrando é")
        self.play(FadeOut(lx), FadeOut(ly), run_time=0.3)
        self.remove(lx, ly)
        KQ = L([("I2", r"I(a)^2"), ("eq", "="), ("ii", r"\iint_{Q_a}"), ("f", r"\Ci{e^{-(\X^2+\Y^2)}}"), ("dA", r"\,dA")], X6 + 16, 200, 44)
        kq = ja_escrita(parte(KQ, list(range(len(KQ[0]))), "chip I(a)²"))
        src = VGroup(*gl(T2, "I2"), *T5[0])
        sai = saindo([T1, T3, T4, *[T2[0][i] for i in range(len(T2[0])) if i not in sel(T2, "I2")]])
        pal.sobe(K1, *C1)
        s_ = pal.tr["s"]
        t0s = self.clk.get_value()
        s_.add_updater(lambda m: m.set_value(min(1.0, (self.clk.get_value() - t0s) / 2.5)))
        self.play(ReplacementTransform(src, kq), *[FadeOut(m) for m in sai], run_time=0.6)
        self.remove(T1, T3, T4, T2, T5)
        molq = em_volta(KQ, GEO, 14, 2, .55, 10)
        self.gat("região maior dá")
        IN = col(L([("Da", r"\Az{D_a}"), ("s1", r"\subset"), ("Q", "Q_a"), ("s2", r"\subset"), ("Dc", r"\Co{D_{a\sqrt{2}}}"), ("v", r",\qquad"),
                    ("f", r"\Ci{e^{-(\X^2+\Y^2)}}"), ("gt", ">0")], X6, 0, 44))
        IN.shift(UP * ((pxof(IN[0][sel(IN, "s1")[0]].get_center())[1] - 296) / 120))
        escreve_seq(self, IN, [(lDa.f, "Da"), (lDc.f, "Dc"), (gl(KQ, "f"), "f")], rt_voo=0.5, passo=0.03)
        origem(self, "D_a, D_{a√2}", "placas do palco (voos)")
        degrau(self, "B6-2 inclusões", "D_a ⊂ Q_a ⊂ D_{a√2}, integrando > 0")
        resta = t0s + 2.5 - self.clk.get_value()
        if resta > 1e-3:
            self.wait(resta)
        s_.clear_updaters()
        s_.set_value(1.0)
        self.wait(1 / FPS)
        print(f"[sobe] {self.lote} {self._aid} quadro ortográfico {self.nq - 1}")
        print(f"[troca2d] pontos do último PNG: { {k: pal.pt(k) for k in ('cin', 'ccirc', 'quina', 'origem')} }")
        for m in (lDa, lDc, lr):
            m.clear_updaters()
        dg.clear_updaters()
        gr.clear_updaters()
        pal.fundo.clear_updaters()
        self.remove(pal.fundo, *pal.tr.values())
        pt = papel_topo()
        hm = heat(RQ)
        quad = lin_px([(C1[0] - HQ, C1[1] - HQ), (C1[0] + HQ, C1[1] - HQ), (C1[0] + HQ, C1[1] + HQ), (C1[0] - HQ, C1[1] + HQ), (C1[0] - HQ, C1[1] - HQ)],
                      GEO, 2.9, z=5)
        din = circ_px(*C1, HQ, AZC, 3.6, z=6)
        dci = circ_px(*C1, RCP, CORAL, 3.6, z=6)
        exa = seta_px((75, C1[1]), (875, C1[1]), E1, 3.6, 22, z=4)
        eya = seta_px((C1[0], 1015), (C1[0], 215), E2, 3.6, 22, z=4)
        self.add(pt, hm, quad, din, dci, exa, eya)                      # o mesmo quadro (troca 3D → 2D, nada se mexe)
        self.grade = pt
        ra = lin_px([C1, (C1[0], C1[1] + HQ)], AZC, 3.6, z=7)
        rc = lin_px([C1, (C1[0] + HQ, C1[1] - HQ)], CORAL, 3.6, z=7)
        lx2 = TC(r"\X", 897, C1[1], 40, "c")
        ly2 = TC(r"\Y", C1[0], 190, 40, "c")
        lQ = TP("Q_a", 260, 405, 44, "c")
        la = TP(r"\Az{a}", 513, 760, 44, "c")
        for m in (lDa, lDc, lr):
            for x in m.get_family():
                x._voando = True
        self.pena(lx2, ly2, lQ, la, lag=0.04, passo=0.025,
                  extra=[lDa.animate(run_time=0.6).move_to(PX(253, 838)), lDc.animate(run_time=0.6).move_to(PX(783, 912)),
                         lr.animate(run_time=0.6).move_to(PX(567, 435)), FadeOut(dg, run_time=0.4), FadeOut(gr, run_time=0.4),
                         Create(ra, run_time=0.6), Create(rc, run_time=0.6), Create(molq, run_time=0.6)])
        self.remove(dg, gr)
        for m in (lDa, lDc, lr):
            for x in m.get_family():
                x._voando = False
                x._ok3d = False
        # GM13: o disco de raio b (no palco, um disco lima de raio b)
        self.gat("num disco de raio bê")
        bt = ValueTracker(0.0)
        db = always_redraw(lambda: circ_px(*C1, max(1.0, bt.get_value()), LI, 3.2, z=8))
        self.add(bt, db)
        C4 = col(L([("ii", r"\iint_{D_b}"), ("eq", "="), ("i1", r"\int_0^{2\pi}\!\!"), ("i2", r"\int_0^{b}"), ("f", r"\Ci{e^{-\R^2}}"), ("J", r"\J"), ("dr", r"\,\dr"),
                    ("dt", r"\,\dt")], X6, 0, 44))
        abaixo(IN, C4, X6, 34)
        self.pena(C4, passo=0.04, extra=[bt.animate(rate_func=smooth, run_time=0.8).set_value(310.0)])
        degrau(self, "B6-2 disco b", "∬_{D_b} = ∫₀^{2π}∫₀^b e^(−r²) r dr dθ (a mesma conta do disco do começo)")
        self.gat("dois pi vezes menos")
        C5 = col(L([("eq", "="), ("tp", r"2\pi"), ("lb", r"\Big["), ("F", r"-\dfrac{\Ci{e^{-\R^2}}}{2}"), ("rb", r"\Big]_0^{b}")], X6, 0, 44))
        abaixo(C4, C5, X6, 26)                                  # FINAL: cada degrau na sua linha (os voos descem sem cruzar a linha de cima)
        _, u1, l1 = sup_sub(C4, "i1")
        _, u2, l2 = sup_sub(C4, "i2")
        _, ub, lb = sup_sub(C5, "rb")
        fo5, nu5, ba5, de5 = frac_partes(C5, "F")
        gmap(self, 13, C4, C5, [(u1, "tp"), ("f", nu5), (u2, ub), (l2, lb)], rt=1.3, nota="a) 2π[−e^(−r²)/2]₀^b",
             extra=[bt.animate(rate_func=smooth).set_value(200.0)])
        degrau(self, "B6-2 disco b", "= 2π[−e^(−r²)/2]₀^b")
        # K14 · C6a: G(b) − G(0) com os valores (o b e o 0 voam dos limites do colchete)
        self.gat("em bê menos é elevado")
        C6a = col(L([("eq", "="), ("tp", r"2\pi"), ("po", r"\Big("), ("a", r"-\dfrac{\Ci{e^{-b^2}}}{2}"), ("m", "-"), ("qo", r"\Big("),
                     ("b", r"-\dfrac{\Ci{e^{0}}}{2}"), ("qc", r"\Big)"), ("pc", r"\Big)")], X6, 0, 44))
        abaixo(C5, C6a, X6, 26)
        fA, nA, bA, dA = frac_partes(C6a, "a")
        fB, nB, bB, dB = frac_partes(C6a, "b")
        g5 = lambda idx: VGroup(*[C5[0][i_] for i_ in idx])
        escreve_seq(self, C6a, [(g5(sel(C5, "tp")), sel(C6a, "tp")), (g5(fo5), fA), (g5(nu5[0:2]), nA[0:2]), (g5(ub), nA[2:3]),
                                (g5(nu5[3:4]), nA[3:4]), (g5(ba5), bA), (g5(de5), dA)], rt_voo=0.8, passo=0.04, so=sel(C6a, ["eq", "tp", "po", "a"]))
        origem(self, "G(b) = −e^(−b²)/2", "primitiva [−e^(−r²)/2] e o b do limite de cima (voos)")
        degrau(self, "B6-2 disco b", "G(b) = −e^(−b²)/2   [o b do limite vira o expoente]")
        self.gat("em zero menos é elevado")
        escreve_seq(self, C6a, [(g5(fo5), fB), (g5(nu5[0:1]), nB[0:1]), (g5(lb), nB[1:2]), (g5(ba5), bB), (g5(de5), dB)], rt_voo=0.8, passo=0.04,
                    so=sel(C6a, ["m", "qo", "b", "qc", "pc"]))
        origem(self, "G(0) = −e⁰/2", "primitiva [−e^(−r²)/2] e o 0 do limite de baixo (voos)")
        degrau(self, "B6-2 disco b", "G(b) − G(0) = −e^(−b²)/2 − (−e⁰/2)   [o 0 do limite vira o expoente]")
        self.gat("o dois pi multiplica")
        C6 = col(L([("eq", "="), ("tp", r"2\pi"), ("po", r"\Big("), ("a", r"-\dfrac{\Ci{e^{-b^2}}}{2}"), ("p", "+"), ("b", r"\dfrac{1}{2}"), ("pc", r"\Big)")], X6, 0, 44))
        abaixo(C6a, C6, X6, 26)
        fa6, na6, ba6, da6 = frac_partes(C6, "a")
        _, nb6, bb6, db6 = frac_partes(C6, "b")
        gmap(self, 13, C6a, C6, [("eq", "eq"), ("tp", "tp"), ("po", "po"), (fA, fa6), (nA, na6), (bA + dA, ba6 + da6),
                                 (sel(C6a, ["m", "qo"]) + fB, sel(C6, ["p"])), (nB, nb6), (bB, bb6), (dB, db6), ("pc", "pc")],
             rt=1.5, nota="b) e⁰ = 1; −(− → +: 2π(−e^(−b²)/2 + 1/2)",
             extra=[bt.animate(rate_func=smooth).set_value(330.0)])
        degrau(self, "B6-2 disco b", "e⁰ = 1   (menos com menos dá mais)")
        degrau(self, "B6-2 disco b", "= 2π(−e^(−b²)/2 + 1/2)   [F(b) − F(0)]")
        self.gat("pi vezes um menos é elevado")
        C7 = col(L([("eq", "="), ("r", r"\pi\,(1-\Ci{e^{-b^2}})")], X6, 0, 44))
        abaixo(C6, C7, X6, 26)
        r7 = ordx(C7, "r")
        tp6 = ordx(C6, "tp")
        gmap(self, 13, C6, C7, [("eq", "eq"), (tp6[1:2], r7[0:1]), (nb6, r7[2:3]), (fa6, r7[3:4]), (na6, r7[4:8])], rt=1.3, nota="c) o 2 cancela: π(1 − e^(−b²))")
        degrau(self, "B6-2 disco b", "= π(1 − e^(−b²))")
        # K14: C4–C7 viram o chip ∬_{D_b} = π(1 − e^(−b²)) no alto (o resultado voa para o chip); a desigualdade e a tabela vêm abaixo dele
        # FINAL (dispensa do Kaio): o chip é um MathTex próprio, escrito ABAIXO de C7 (sem cobrir a conta): a caneta escreve ∬_{D_b} e^{−r²} dA, e o "=" e o
        # resultado voam da última linha (C7); só depois C4–C7 saem (todos os glifos) e o chip sobe para o alto da coluna.
        CKc = col(L([("ii", r"\iint_{D_b}"), ("f", r"\Ci{e^{-\R^2}}"), ("dA", r"\,dA"), ("eq", "="), ("r", r"\pi\,(1-\Ci{e^{-b^2}})")], X6, 0, 44))
        abaixo(C7, CKc, X6, 26)
        CKref = col(L([("ii", r"\iint_{D_b}"), ("f", r"\Ci{e^{-\R^2}}"), ("dA", r"\,dA"), ("eq", "="), ("r", r"\pi\,(1-\Ci{e^{-b^2}})")], X6, 0, 44))
        abaixo(IN, CKref, X6, 34)
        dy_c = CKref.get_center()[1] - CKc.get_center()[1]
        escreve_seq(self, CKc, [(VGroup(*[C7[0][k] for k in sel(C7, "eq")]), sel(CKc, "eq")), (VGroup(*[C7[0][k] for k in sel(C7, "r")]), sel(CKc, "r"))],
                    rt_voo=0.9, passo=0.04)
        origem(self, "∬_{D_b} e^(−r²) dA = π(1 − e^(−b²))", "o = e o resultado da última linha (voos); ∬ e^(−r²) dA vêm da caneta")
        degrau(self, "B6-2 disco b", "∬_{D_b} e^(−r²) dA = π(1 − e^(−b²))")
        resto_c = [C4, C5, C6a, C6, C7]
        sai = saindo(resto_c)
        self.play(*[FadeOut(m) for m in resto_c], run_time=0.5)
        self.remove(*resto_c, *[x for m in resto_c for x in m.get_family()])
        self.play(CKc.animate(rate_func=smooth).shift(UP * dy_c), run_time=0.5)
        molc_ = em_volta(CKc, LI, 12, 2, .8, 10)
        self.play(Create(molc_), run_time=0.3)
        # a desigualdade: a e a√2 voam dos raios do palco
        self.gat("fica entre pi vezes")
        self.play(FadeOut(db), run_time=0.3)
        db.clear_updaters()
        self.remove(db, bt)
        D6 = col(L([("L", r"\Az{\pi(1-e^{-a^2})}"), ("le1", r"\le"), ("I", r"I(a)^2"), ("le2", r"\le"), ("R", r"\Co{\pi(1-e^{-2a^2})}")], X6, 0, 44))
        abaixo(CKc, D6, X6, 40)
        Lg, Rg = ordx(D6, "L"), ordx(D6, "R")
        # Lg = [π, (, 1, −, e, −, a, 2, )]; Rg = [π, (, 1, −, e, −, 2, a, 2, )]
        escreve_seq(self, D6, [(la.f, Lg[6:7]), (lr.f, Rg[6:8])], rt_voo=0.9, passo=0.035)
        origem(self, "a e a√2 da desigualdade", "raios dos dois discos no palco (voos)")
        degrau(self, "B6-2 confronto", "π(1 − e^(−a²)) ≤ I(a)² ≤ π(1 − e^(−2a²))")
        # a tabela; o a cresce (o sino de cima encolhe no quadrado [−a, a]²)
        YT = 676
        cols = [1040, 1250, 1470, 1690]
        hd = [TC("a", cols[0], YT, 40, "c"), leg("BAIXO", cols[1], YT + 11, AZC, "center", 30), TC(r"I(a)^2", cols[2], YT, 40, "c"),
              leg("CIMA", cols[3], YT + 11, CORAL, "center", 30)]
        self.pena(*hd, lag=0.05)
        a_ = ValueTracker(RQ)
        din2 = Group(heat(RQ, 160))

        def _redesenha(m):                       # Group com imagem não tem become(): troca os filhos a cada quadro
            m.submobjects = [heat(a_.get_value(), 160)]
        din2.add_updater(_redesenha)
        for x in din2.get_family():
            x._sem_foco = True
        self.remove(hm)
        self.add(a_, din2)
        linhas = [("1", "1{,}986", "2{,}231", "2{,}716"), ("2", "3{,}084", "3{,}112", "3{,}141"), ("3", "3{,}1412", "3{,}1415", "3{,}1416")]
        cores = [BR, AZC, BR, CORAL]
        for k, (gg, row) in enumerate(zip(("com á igual a um", "com á igual a dois", "com á igual a três"), linhas)):
            self.gat(gg)
            self.play(a_.animate(rate_func=smooth).set_value(float(row[0])), run_time=1.2)
            cel = [TC(r"\textcolor[HTML]{%s}{%s}" % (cores[j][1:], row[j]), cols[j], YT + 59 + 52 * k, 40, "c") for j in range(4)]
            self.pena(*cel, lag=0.08)
            degrau(self, "B6-2 tabela", f"a = {row[0]}: {row[1]} ≤ {row[2]} ≤ {row[3]}")
        din2.clear_updaters()
        self.remove(a_)
        # o limite e √π (duas linhas)
        self.gat("o teorema do confronto")
        realca(self, din, cor=AZC, rt=0.4)
        realca(self, dci, cor=CORAL, rt=0.4)
        LM = col(L([("a", r"a\to\infty:"), ("q", r"\quad\pi\le\lim I(a)^2\le\pi")], X6, 897, 44))
        self.pena(LM)
        degrau(self, "B6-2 confronto", "a → ∞: π ≤ lim I(a)² ≤ π")
        self.gat("é positivo a integral")
        RP0 = col(L([("im", r"\Rightarrow\ "), ("i", r"\displaystyle\int_{-\infty}^{\infty}"), ("f", r"\Ci{e^{-\X^2}}"), ("dx", r"\,\dX"), ("eq", "=")], 1330, 985, 44))
        self.pena(RP0)
        self.gat("é raiz de pi")
        SPm = L([("sp", r"\Me{\sqrt{\pi}}")], 0, 0, 44)
        SPm.shift(RIGHT * ((pxof(RP0.get_right())[0] + 24 - pxof(SPm.get_left())[0]) / 120))
        SPm.shift(UP * (RP0[0][sel(RP0, "eq")[0]].get_center()[1] - SPm.get_center()[1]))
        self.pena(SPm)
        degrau(self, "B6-2 confronto", "⇒ ∫_{−∞}^{∞} e^(−x²) dx = √π")
        mol = em_volta(SPm, MEN, 12, 2.5, 1.0, 8)
        ck = check_px(0, 0, MEN, .7)
        ck.move_to(PX(pxof(self.cart.get_left())[0] - 30, 155))
        self.play(Create(mol), Create(ck), run_time=0.4)
        self.cart_ok = ck                                   # o cartão com ✓ fica no canto até o S1 (§4.5)
        self.marca("v2_03")
        # ── B6-3 · a curva normal ──
        self.an("B6-3")
        self.secao("A CURVA NORMAL")
        self.subt("O MESMO NÚMERO NA ESTATÍSTICA")
        topo = [m for m in self.snap() if pxof(m.get_center())[0] < 980] + [din2]
        colv = [m for m in self.snap() if m not in topo and m not in (RP0, SPm, mol, self.cart, self.cart_ok)]
        sai = saindo(topo + colv)
        f2 = lambda x: math.exp(-x * x / 2)
        d2 = curva_palco(f2, -2.95, 2.95)
        sh2 = sombra(f2, -2.95, 2.95)
        RPg = VGroup(RP0, SPm, mol)
        dv = PX(X6, 205) - np.array([RPg.get_left()[0], RPg.get_center()[1], 0])
        self.play(*[FadeOut(m) for m in sai], run_time=0.3)                 # o palco velho sai; no quadro seguinte o novo começa
        self.remove(*topo, *colv)
        self.grade = d2["g"]
        self.play(RPg.animate.shift(dv), FadeIn(d2["g"]), GrowFromPoint(d2["sx"], VC.P(0, 0)), GrowFromPoint(d2["sy"], VC.P(0, 0)),
                  Create(d2["c"]), FadeIn(sh2), run_time=0.9)           # K15: o papel, os eixos e a curva juntos (palco nunca só com papel)
        self.pena(d2["lx"], d2["ly"], lag=0.05)
        self.gat("a curva normal padrão")
        lc2 = TP(r"\Ci{e^{-\X^2/2}}", *VC.px(1.45, .78), 40, "l")
        self.pena(lc2)
        N0 = col(L([("i", r"\displaystyle\int_{-\infty}^{\infty}"), ("f", r"\Ci{e^{-\X^2/2}}"), ("dx", r"\,\dX")], X6, 0, 44))
        abaixo(RPg, N0, X6, 40)
        escreve_seq(self, N0, [(lc2.f, "f")], rt_voo=0.9, passo=0.04)
        self.gat("troca xis por raiz")
        realca(self, d2["c"], cor=CI, rt=0.4)
        N1 = col(L([("x", r"\X=\sqrt{2}\,\uu"), ("i", r"\ \Rightarrow\ "), ("dx", r"\dX=\sqrt{2}\,\du")], X6, 0, 40))
        abaixo(N0, N1, X6, 26)
        self.pena(parte(N1, sel(N1, ["x"]), "x = √2 u"))
        degrau(self, "B6-3 substituição", "x = √2 u")
        self.gat("dê xis vira raiz")
        realca(self, sh2, cor=CI, rt=0.4)
        self.pena(parte(N1, sel(N1, ["i", "dx"]), "⇒ dx = √2 du"))
        degrau(self, "B6-3 substituição", "dx = √2 du")
        self.gat("e os limites continuam")
        realca(self, d2["sx"], cor=E1, rt=0.4)
        N2 = col(L([("a", r"\X:\ -\infty\to\infty"), ("i", r"\ \Rightarrow\ "), ("b", r"\uu:\ -\infty\to\infty")], X6, 0, 40))
        abaixo(N1, N2, X6, 20)
        self.pena(N2)
        degrau(self, "B6-3 limites novos", "x: −∞ → ∞ ⇒ u: −∞ → ∞")
        # GM14: √2 ∫ e^(−u²) du; o √π voa do resultado do topo; √(2π)
        self.gat("a integral vira raiz")
        N3 = col(L([("eq", "="), ("s2", r"\sqrt{2}"), ("i", r"\displaystyle\int_{-\infty}^{\infty}"), ("f", r"\Ci{e^{-\uu^2}}"), ("du", r"\,\du")], X6, 0, 44))
        ao_lado(N0, N3, 16, ia=sel(N0, "i")[0], ib=sel(N3, "i")[0])        # na mesma linha da de x: o mapa não cruza nada
        f0, f3 = ordx(N0, "f"), ordx(N3, "f")
        dxN1 = ordx(N1, "dx")
        gmap(self, 14, N0, N3, [("i", "i"), (f0[0:2], f3[0:2])], voos=[(VGroup(*[N1[0][k] for k in dxN1[3:5]]).copy(), "s2"),
                                                                   (VGroup(*[N1[0][k] for k in ordx(N1, "x")[-1:]]).copy(), f3[2:3])],
             rt=1.0, nota="a) √2 ∫ e^(−u²) du (√2 e u da linha da substituição)")
        degrau(self, "B6-3 normal", "∫ e^(−x²/2) dx = √2 ∫ e^(−u²) du")
        self.gat("vezes raiz de pi")
        acende(self, (VGroup(*[N3[0][k] for k in sel(N3, ["i", "f", "du"])]), MEN), rt=0.6)
        N4 = col(L([("eq", "="), ("s2", r"\sqrt{2}"), ("c", r"\cdot"), ("sp", r"\sqrt{\pi}")], X6, 0, 44))
        abaixo(N2, N4, X6, 34)
        self.pena(N4, passo=0.03, extra=[Indicate(gl(SPm, "sp"), color=MEN, scale_factor=1.15)])   # o √π do topo acende junto
        origem(self, "√π de √2 · √π", "resultado ∫ e^(−x²) dx = √π (voo)")
        degrau(self, "B6-3 normal", "= √2 · √π")
        self.gat("raiz de dois pi é")
        N5 = col(L([("eq", "="), ("r", r"\Me{\sqrt{2\pi}}")], X6, 0, 44))
        ao_lado(N4, N5, 14)
        s2_, sp4, r5 = ordx(N4, "s2"), ordx(N4, "sp"), ordx(N5, "r")
        gmap(self, 14, N4, N5, [("eq", "eq"), (s2_[0:1] + sp4[0:1], r5[0:1]), (s2_[1:], r5[1:2]), (sp4[1:], r5[2:])], rt=0.9, nota="c) √(2π)")
        degrau(self, "B6-3 normal", "= √(2π)")
        # 1/√(2π) por inteiro (E36): o √(2π) do denominador voa do resultado; o e^(−x²/2) voa do rótulo da curva
        self.gat("um sobre raiz de dois")
        NF = L([("fr", r"\dfrac{1}{\sqrt{2\pi}}"), ("f", r"\Ci{e^{-\X^2/2}}")], 0, 0, 44)
        NF.shift(PX(110, 300) - np.array([NF.get_left()[0], NF.get_center()[1], 0]))
        fo, nn, bb, dd = frac_partes(NF, "fr")
        escreve_seq(self, NF, [(gl(N5, "r"), dd, 2.3), (lc2.f, "f", 0.6)], rt_voo=0.9, passo=0.05)
        origem(self, "1/√(2π)", "resultado √(2π) da coluna (voo)")
        self.gat("para a área total")
        um = dentro(T("ÁREA = 1 = 100 %", 515, 815, 30, "left", BR))       # dentro da área, abaixo da curva
        self.pena(um)
        realca(self, sh2, cor=MEN, rt=0.6)
        self.sai_fim()
