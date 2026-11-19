"""yt_0034 · B4 · a troca: desenhar a região pelos limites (alvo 13), o sino z = e^(−y²) em Three.js (cena2: alvos 14 → 15 → 16, pouso
lateral com a saída de escala (a): ZS vai de 1 a 440/560 durante o pouso) e o erro clássico (alvo 17). Glyph maps 8 e 9."""
from pecas34 import *
from sec_b3 import corte3d, pouso, troca_para_2d

def rapido(t):
    """rate_func: a animação acaba em 2/3 do play (o resto do pouso sai em 0,4 s dentro do voo de 0,6 s)."""
    return min(1.0, 1.5 * t)


def pinta_tiras(sc, Gv, f, a, b, dur, cor, alpha=.35, n=20):
    """Área sob y = f de a até b pintada por tiras, da esquerda para a direita, em `dur` s (updater de dt: não bloqueia a cena)."""
    st = {"t": 0.0, "k": 0}
    xs = np.linspace(a, b, n + 1)
    g = VGroup()

    def up(m, dt):
        st["t"] += dt
        kk = min(n, int(st["t"] / dur * n + 1e-9))
        while st["k"] < kk:
            x0, x1 = xs[st["k"]], xs[st["k"] + 1]
            m.add(poly_px([Gv.px(x0, 0)] + [Gv.px(x, f(x)) for x in np.linspace(x0, x1, 6)] + [Gv.px(x1, 0)], mixh(BG_, cor, alpha), z=2))
            st["k"] += 1
        if st["k"] >= n:
            m.clear_updaters()
    g.add_updater(up)
    sc.add(g)
    return g


LAT2 = Lat(200, 820, 560, 440)         # painel do sino: 560 px por metro (x), 440 px por unidade de f
ZS2 = 440 / 560


def integral_hook(X, Y, size, caneta=True):
    return L([("io", r"\int_{\Am{0}}^{\Am{1}}\!"), ("ii", r"\int_{\Az{\X}}^{\Co{1}}"), ("e", r"e^{-\Y^2}"), ("dy", r"\,\dY"), ("dx", r"\,\dX")],
             X, Y, size, "l", caneta)


def sem_alto(m, chave):
    g = list(gl(m, chave))
    a = max(g, key=lambda x: x.height)
    return [x for x in g if x is not a], a


class PB4(B34):
    ANTES = "A TROCA"

    def corpo(self):
        # ── B4-1 · desenhar a região pelos limites (alvo 13) ──
        self.an("B4-1")
        g = papel_v(TRI, (0, 1.12, 0, 1.12))
        self.grade = g
        sx, sy, lx, ly = eixos_v(TRI, 1.2, 1.2)
        chipI = integral_hook(1500, 150, 30, caneta=False)              # o chip da integral do começo, no topo da coluna
        mold_ = RoundedRectangle(width=(chipI.width * 120 + 28) / 120, height=(chipI.height * 120 + 18) / 120, corner_radius=10 / 120)
        mold_.move_to(chipI.get_center()).set_stroke(GEO, W(2)).set_fill(opacity=0).set_z_index(24)
        ja_escrita(chipI)
        for m in (lx, ly):
            ja_escrita(m)
        self.add(g, sx, sy, lx, ly, mold_, chipI)                      # palco armado já no quadro 0 (nunca vazio)
        I = integral_hook(1120, 260, 50, caneta=False)
        voos(self, [(chipI.copy(), I)], rt=0.9, extra=[FadeOut(chipI), FadeOut(mold_)])     # voa do chip direto para a coluna (nunca no centro)
        self.remove(chipI, mold_)
        lo, hi = sem_alto(I, "io")[0][0], sem_alto(I, "io")[0][1]       # os limites de fora (0 e 1) voam logo: eixos sem objeto ≤ 1,5 s
        lo, hi = sorted([lo, hi], key=lambda x: x.get_center()[1])
        t1x = tick(TRI, "x", 1, r"\Am{1}")
        t0 = TC(r"\Am{0}", *TRI.px(0, 0), 28, "c").shift(DOWN * 30 / 120 + LEFT * 22 / 120)
        self.gat("tem um método")
        acende(self, (gl(I, "io", "ii"), None), rt=1.0)
        realce(self, sx, sy)
        self.gat("desenhar a região")
        p1 = T("PASSO 1: DESENHAR A REGIÃO", 1120, 430, 40, "left", MEN)
        self.pena(p1)
        self.gat("a partir dos limites")
        realce(self, sx, sy)                                           # os eixos onde os limites vão pousar
        acende(self, (sem_alto(I, "io")[0][0], E1), (sem_alto(I, "io")[0][1], E1), (VGroup(*sem_alto(I, "ii")[0]), CORAL), rt=0.8)
        self.gat("xis vai de zero a um")                               # handoff final D12: 0 e 1 voam dos limites de fora para o eixo x
        v1 = curva(TRI, [(1, 0), (1, 1)], E1, 2, dash=(6, 7), alpha=.7, z=3)
        voos(self, [(lo, t0), (hi, t1x[1])], rt=0.7, extra=[Create(t1x[0])])
        self.play(Create(v1), run_time=0.5)
        self.gat("para cada xis ípsilon")
        realce(self, v1, t1x[0])                                       # x vai de 0 a 1
        (li, ia) = sem_alto(I, "ii")
        lix, li1 = sorted(li, key=lambda x: x.get_center()[1])
        dg = curva(TRI, [(0, 0), (1, 1)], AZC, 4)
        tp = curva(TRI, [(0, 1), (1, 1)], CORAL, 4)
        t1y = tick(TRI, "y", 1, r"\Mg{1}")
        self.gat("de xis até um")
        acende(self, (lix, AZC), (li1, CORAL), rt=0.8)                 # os limites de dentro, lidos na voz
        self.gat("entra na reta ípsilon")
        tv = tiraV(TRI, .5, .5, 1, alpha=.55)
        pe, ps = pontos_es(TRI, (.5, .5), (.5, 1))
        self.play(GrowFromEdge(tv, DOWN), FadeIn(pe, scale=.5), run_time=0.6)
        self.gat("a diagonal")                                         # D12: a reta y = x voa do limite de baixo
        risca_voando(self, [(lix, dg)], rt=0.7)
        ryx = rot(TRI, r"\Az{\Y=\X}", (.62, .5), 10, 10, 30)
        self.pena(ryx)
        self.gat("ípsilon igual a um")                                 # D12: a reta y = 1 voa do limite de cima
        risca_voando(self, [(li1, tp)], rt=0.7)
        self.play(Create(t1y[0]), FadeIn(ps, scale=.5), run_time=0.3)
        ry1 = rot(TRI, r"\Co{\Y=1}", (.35, 1), 0, -30, 30)
        self.pena(t1y[1], ry1, lag=0.2)
        self.gat("com o xis andando")
        reg = regiao(TRI, [(0, 0), (1, 1), (0, 1)])
        lado = curva(TRI, [(0, 0), (0, 1)], GEO, 2, z=3)
        tiras = [tiraV(TRI, a, a, 1, alpha=.4) for a in (.1, .3, .5, .7, .9)]
        self.play(FadeOut(tv), FadeOut(pe), FadeOut(ps), run_time=0.3)
        self.remove(tv, pe, ps)
        self.gat("essas fatias pintam")                                # D12: as tiras em pé
        self.play(LaggedStart(*[GrowFromEdge(t, DOWN) for t in tiras], lag_ratio=0.3), run_time=1.0)
        self.gat("um triângulo com")
        self.play(FadeIn(reg), Create(lado), run_time=0.8)
        self.gat("com vértices em zero")
        vs = [ponto_px(*TRI.px(*p), GEO, 7) for p in ((0, 0), (0, 1), (1, 1))]
        q01, q11 = TRI.px(0, 1), TRI.px(1, 1)
        l01 = leg("(0, 1)", q01[0] - 20, q01[1] - 22, GEO, "right", 26)
        l11 = leg("(1, 1)", q11[0] + 16, q11[1] - 14, GEO, "left", 26)
        self.play(FadeIn(vs[0], scale=.5), run_time=0.3)
        self.play(FadeIn(vs[1], scale=.5), run_time=0.3)
        self.pena(l01)
        self.play(FadeIn(vs[2], scale=.5), run_time=0.3)
        self.pena(l11)
        self.gat("esse triângulo é")
        self.play(reg.animate.set_fill(mixh(BG_, GEO, .3)), run_time=0.5)
        self.play(reg.animate.set_fill(RB), run_time=0.5)
        self.gat("a integral dupla não")
        realce(self, *tiras)                                           # as fatias em pé: uma ordem entre duas
        self.gat("não sabe nada de")
        so = mixl([("m", r"\iint"), ("t", "SÓ CONHECE REGIÃO E FUNÇÃO", GEO)], 1120, 540, 36)
        self.pena(*so.p, lag=0.15)
        self.marca("13", agora=True)
        self.gat("ela só conhece")                       # as fatias em pé dão lugar às deitadas: a região é a mesma
        deit = [tiraH(TRI, b, 0, b, alpha=.4) for b in (.1, .3, .5, .7, .9)]
        self.play(*[ReplacementTransform(a, b) for a, b in zip(tiras, deit)], run_time=1.4)
        tiras = deit

        # ── B4-2 · reler deitado: o sino vira retângulo (alvos 14 → 15 → 16) ──
        self.an("B4-2")
        self.secao("O SINO")
        self.gat("reler o triângulo deitado")
        p2 = T("PASSO 2: RELER DEITADO", 1120, 280, 40, "left", MEN)
        th = tiraH(TRI, .6, 0, .6)
        pe2, ps2 = pontos_es(TRI, (0, .6), (.6, .6))
        dgc = curva(TRI, [(0, 0), (1, 1)], CORAL, 4)
        rxy = rot(TRI, r"\Co{\X=\Y}", (.62, .5), 10, 10, 30)
        self.play(*[FadeOut(m) for m in [I, p1, so] + tiras + [ry1]], ReplacementTransform(dg, dgc), ReplacementTransform(ryx, rxy),
                  tp.animate.set_stroke(GEO, W(2)), run_time=0.9)
        self.remove(I, p1, so, *tiras, ry1)
        ja_escrita(rxy.f)
        self.pena(p2, extra=[GrowFromEdge(th, LEFT), FadeIn(pe2, scale=.5), FadeIn(ps2, scale=.5)])
        self.gat("o ípsilon vai de")
        R2 = L([("a", r"\Mg{0}\le\Y\le\Mg{1},"), ("q", r"\qquad"), ("b", r"\Az{0}\le\X\le"), ("y", r"\Co{\Y}")], 1120, 390, 42, caneta=False)
        self.pena(parte(R2, sel(R2, "a"), "0 ≤ y ≤ 1"))
        acende(self, (t1y[1], E2), rt=0.5)
        self.gat("para cada ípsilon a")
        for yy_ in (.25, .85, .6):
            pa_, pb_ = pontos_es(TRI, (0, yy_), (yy_, yy_))
            self.play(Transform(th, tiraH(TRI, yy_, 0, yy_)), Transform(pe2, pa_), Transform(ps2, pb_), run_time=0.9)
        self.gat("entra no eixo")
        self.pena(parte(R2, sel(R2, "b"), "0 ≤ x ≤"))
        self.gat("sai na diagonal")
        yy = [x for x in rxy.f[0] if x.get_center()[0] > rxy.f.get_center()[0]][-1:]
        voos(self, [(VGroup(*yy), VGroup(*gl(R2, "y")))], rt=1.0)
        R2._esc = True
        # corte para a cena 2: o sino sobe; a faca em pé dá o teto curvo
        self.gat("olha a peça")
        pal = Palco3D(self, "cena2", CAMP, v3=True, tipo="pe", cresce=0.0, faca=0.0, corte=0.0, face=0.0, sai=0.0, zs=1.0)
        pal.fundo.op.set_value(1.0)
        col_p2 = [p2, R2]
        sai = [m for m in self.snap() if m not in col_p2] + [self.grade]
        self.remove(*sai)
        self.grade = None
        self.add(pal.fundo)
        lx3 = pal.prende(TC(r"\X", 0, 0, 32, "c"), "ex")
        lf3 = pal.prende(TC(r"\f", 0, 0, 32, "c"), "ez", 30, 34)
        ja_escrita(lx3)
        ja_escrita(lf3)
        self.add(lx3, lf3)
        F0 = TC(r"\f(\X,\Y)=e^{-\Y^2}", 1120, 250, 46)
        self.play(*pal.anim(1.2, cresce=1.0), FadeOut(p2), FadeOut(R2), run_time=1.2)
        self.remove(p2, R2)
        self.pena(F0)
        self.gat("em pé em xis")
        realce(self, lx3, lf3, cor=E1)
        self.gat("zero vírgula dois")
        self.play(*pal.anim(0.6, faca=1.0), run_time=0.6)
        self.play(*pal.anim(0.9, corte=1.0), run_time=0.9)            # a parte da frente recua até a faca e vira traço (a peça não se separa)
        self.play(*pal.anim(0.3, faca=0.0), run_time=0.3)
        self.play(*pal.anim(0.3, face=1.0), run_time=0.3)
        px2 = pal.prende(TP(r"\X=0{,}2", 0, 0, 32), "faca_p", 0, -30)
        tc = leg("FATIA EM PÉ: TETO CURVO", 1120, 350, E1, "left", 30)
        self.pena(px2, tc, lag=0.3)
        self.gat("é por isso que")
        F1 = L([("i", r"\int_{\Az{\X}}^{\Co{1}}e^{-\Y^2}\,\dY="), ("q", r"\ \Al{?}")], 1120, 450, 40)
        self.pena(F1)
        self.marca("v3_01b", agora=True)
        # "travava": pouso lateral para a fatia em pé em 2D (o teto curvo)
        self.gat("travava")
        self.play(*pal.anim(0.3, sai=1.0), FadeOut(px2), FadeOut(lx3), FadeOut(lf3), run_time=0.3)
        for m in (px2, lx3, lf3):
            m.clear_updaters()
        self.remove(px2, lx3, lf3)
        LATP = Lat(200, 820, 560, 560)
        pouso(self, pal, (.4, 0, 0), (-1, 0, 0), 280, 200, 820, rt=2.0)
        GP = lateral(LATP, 1.05, ymax=1.1, zt=(0, 1), yt=(0, 1), hcor=E2, hl=r"\Y", vl=r"\f", passo=.25)
        ys_ = np.linspace(.2, 1, 40)
        fat = poly_px([LATP.px(.2, 0)] + [LATP.px(y, math.exp(-y * y)) for y in ys_] + [LATP.px(1, 0)], mixh(BG_, E1, .55), z=2)
        fat.set_stroke("#7A5A10", W(2), 1)
        pxp = TP(r"\X=0{,}2", 280, 240, 30, "c")
        troca_para_2d(self, pal, [GP["grade"], GP["eh"], GP["ev"], GP["lh"], GP["lv"], GP["nums"], fat, pxp])
        print(f"[pouso2d] B4-2 pe p0={LATP.px(.2, 0)} p1={LATP.px(1, 0)} p2={LATP.px(1, math.exp(-1))} p3={LATP.px(.2, math.exp(-.04))}")
        self.wait(0.6)
        # volta: o mesmo sólido (a peça inteira volta a ser opaca) e a órbita de 2 s até a vista de frente da faca deitada
        lat_p = [GP["grade"], GP["eh"], GP["ev"], GP["lh"], GP["lv"], GP["nums"], fat, pxp]
        palB = Palco3D(self, "cena2", CAMP, v3=True, tipo="pe", cresce=1.0, faca=0.0, corte=1.0, face=1.0, sai=1.0, zs=1.0)
        palB.pousa((.4, 0, 0), (-1, 0, 0), 280, 200, 820)
        palB.tr["s"].set_value(1.0)
        palB.fundo.op.set_value(1.0)
        self.remove(*lat_p)
        self.add(palB.fundo)
        self.play(palB.tr["s"].animate(rate_func=linear).set_value(0.0), *palB.anim(0.9, corte=0.0, face=0.0, sai=0.0), run_time=0.9)
        palB.set(tipo="dei")
        palB.rumo(CAMD, arco=True)
        self.play(palB.tr["s"].animate(rate_func=linear).set_value(1.0), run_time=2.0)           # órbita (ease in-out pelo cam_mix)
        lx4 = palB.prende(TC(r"\X", 0, 0, 32, "c"), "ex")
        lf4 = palB.prende(TC(r"\f", 0, 0, 32, "c"), "ez", 30, 34)
        ja_escrita(lx4)
        ja_escrita(lf4)
        self.play(*palB.anim(0.5, faca=1.0), FadeIn(lx4), FadeIn(lf4), run_time=0.5)
        self.play(*palB.anim(0.6, corte=1.0), run_time=0.6)
        self.play(*palB.anim(0.2, faca=0.0), run_time=0.2)
        self.play(*palB.anim(0.3, face=1.0), run_time=0.3)
        py6 = palB.prende(TP(r"\Y=0{,}6", 0, 0, 32), "faca_d", 30, -30)
        td = leg("FATIA DEITADA: RETÂNGULO", 1120, 560, E2, "left", 30)
        self.pena(py6, td, lag=0.3)
        self.marca("v3_02b", agora=True)
        self.gat("um retângulo")
        self.play(*palB.anim(0.3, sai=1.0), *[FadeOut(m) for m in (py6, lx4, lf4)], run_time=0.3)
        for m in (py6, lx4, lf4):
            m.clear_updaters()
        self.remove(py6, lx4, lf4)
        pouso(self, palB, (0, 1.2, 0), (0, 1, 0), 280, 200, 820, rt=1.2, extra_s=palB.anim(1.2, zs=ZS2))
        h = gs(.6)
        G = lateral(LAT2, 1.15, ymax=1.15, zt=(0, 1), yt=(0, 1), hcor=E1, hl=r"\X", vl=r"\f", passo=.25)
        ret = poly_px([LAT2.px(0, 0), LAT2.px(.6, 0), LAT2.px(.6, h), LAT2.px(0, h)], mixh(BG_, E2, .45), z=2)
        cont = lin_px([LAT2.px(0, 0), LAT2.px(.6, 0), LAT2.px(.6, h), LAT2.px(0, h), LAT2.px(0, 0)], E2, 5, z=4)
        py_ = TP(r"\Y=0{,}6", 270, 240, 30, "c")
        troca_para_2d(self, palB, [G["grade"], G["eh"], G["ev"], G["lh"], G["lv"], G["nums"], ret, cont, py_])
        print(f"[pouso2d] B4-2 ret f0={LAT2.px(0, 0)} f1={LAT2.px(.6, 0)} f2={LAT2.px(.6, h)} f3={LAT2.px(0, h)}")

        # ── as áreas das fatias como funções (handoff v3 §3.2; alvo v3_05) ──
        self.gat("agora desenha a")
        self.secao("A ÁREA DE CADA FATIA")
        I0v = 0.746824
        AX = lambda x: math.sqrt(math.pi) / 2 * (math.erf(1) - math.erf(x))
        AY = lambda y: y * math.exp(-y * y)
        GA, GB = Lat(140, 760, 360, 562), Lat(610, 760, 360, 562)
        fat_ = poly_px([LATP.px(.2, 0)] + [LATP.px(y, math.exp(-y * y)) for y in ys_] + [LATP.px(1, 0)], mixh(BG_, E1, .55), z=3)
        fat_.set_stroke(E1, W(3), 1)                                    # a face âmbar do pouso em pé
        col = [F0, tc, F1, td]
        lat = [G["grade"], G["eh"], G["ev"], G["lh"], G["lv"], G["nums"], py_, cont]
        # handoff final D1: as faces encolhem e voam até virar os pontos (0,2; 0,549) e (0,6; 0,419) em 0,6 s; o resto do pouso sai
        # em 0,4 s, junto; só depois os eixos dos gráficos entram
        p1 = ponto_px(*GA.px(.2, AX(.2)), E1, 11, z=9)
        p2_ = ponto_px(*GB.px(.6, AY(.6)), E2, 11, z=9)
        self.play(ReplacementTransform(fat_, p1), ReplacementTransform(ret, p2_), *[FadeOut(m, rate_func=rapido) for m in col + lat], run_time=0.6)
        self.remove(*col, *lat)

        def eixos_a(Gv, cor, lb):
            gg = VGroup()
            for k in range(0, 5):
                gg.add(lin_px([Gv.px(k * .25, 0), Gv.px(k * .25, .75)], GRADE, 1.2, z=-9))
            for k in range(0, 4):
                gg.add(lin_px([Gv.px(0, k * .25), Gv.px(1.0, k * .25)], GRADE, 1.2, z=-9))
            eh = seta_px(Gv.px(-.02, 0), Gv.px(1.1, 0), cor, 3, 16, z=6)
            ev = seta_px(Gv.px(0, -.02), Gv.px(0, .9), GEO, 3, 16, z=6)
            q = Gv.px(1.1, 0)
            lh = TC(lb, q[0] + 24, q[1], 32, "c")
            n0 = TC(r"\Am{0}" if lb == r"\X" else r"\Mg{0}", *Gv.px(0, 0), 26, "c").shift(DOWN * 30 / 120 + LEFT * 22 / 120)
            n1 = TC(r"\Am{1}" if lb == r"\X" else r"\Mg{1}", *Gv.px(1, 0), 26, "c").shift(DOWN * 30 / 120)
            return gg, eh, ev, lh, n0, n1

        ga = eixos_a(GA, E1, r"\X")
        gb = eixos_a(GB, E2, r"\Y")
        self.grade = VGroup(ga[0], gb[0])
        self.play(FadeIn(ga[0]), FadeIn(gb[0]), GrowFromPoint(ga[1], GA.P(0, 0)), GrowFromPoint(ga[2], GA.P(0, 0)),
                  GrowFromPoint(gb[1], GB.P(0, 0)), GrowFromPoint(gb[2], GB.P(0, 0)), run_time=0.5)
        self.pena(ga[3], ga[4], ga[5], gb[3], gb[4], gb[5], lag=0.04, passo=0.035)
        self.gat("em pé a área")
        ta = T("EM PÉ", 150, 240, 32, "left", E1)
        tE = T("EM PÉ", 1120, 232, 30, "left", E1)
        FA = TC(r"A(\X)=\int_{\X}^{\Co{1}}e^{-\Y^2}\,\dY", 1225, 232, 36, "l")
        self.pena(ta, tE, FA, lag=0.15)
        xa = ValueTracker(0.0)
        self.add(xa)
        cva = always_redraw(lambda: curva(GA, cX(AX, 0, max(.002, xa.get_value()), 60), E1, 4, z=6))
        pa = always_redraw(lambda: ponto_px(*GA.px(xa.get_value(), AX(xa.get_value())), E1, 9, z=8))
        self.add(cva, pa)
        self.play(xa.animate.set_value(1.0), run_time=1.8, rate_func=linear)
        cva.clear_updaters()
        self.remove(pa, xa)
        self.gat("não tem fórmula")
        sf = leg("SEM FÓRMULA, MAS EXISTE", 1150, 312, GEO, "left", 28)
        self.pena(sf)
        d1 = curva(GA, [(.2, 0), (.2, AX(.2))], E1, 2, dash=(6, 6), z=5)
        l1 = TP(r"\X=0{,}2", *GA.px(.27, AX(.2) + .055), 28, "l")
        self.play(Create(d1), run_time=0.3)
        self.pena(l1)
        self.gat("deitada a área")
        tb_ = T("DEITADA", 610, 240, 32, "left", E2)
        tD = T("DEITADA", 1120, 422, 30, "left", E2)
        FB = TC(r"A(\Y)=\Y\,e^{-\Y^2}", 1255, 422, 36, "l")
        self.pena(tb_, tD, FB, lag=0.15)
        xb = ValueTracker(0.0)
        self.add(xb)
        cvb = always_redraw(lambda: curva(GB, cX(AY, 0, max(.002, xb.get_value()), 60), E2, 4, z=6))
        pb = always_redraw(lambda: ponto_px(*GB.px(xb.get_value(), AY(xb.get_value())), E2, 9, z=8))
        self.add(cvb, pb)
        self.play(xb.animate.set_value(1.0), run_time=1.5, rate_func=linear)
        cvb.clear_updaters()
        self.remove(pb, xb)
        d2 = curva(GB, [(.6, 0), (.6, AY(.6))], E2, 2, dash=(6, 6), z=5)
        l2 = TP(r"\Y=0{,}6", *GB.px(.64, AY(.6) + .06), 28, "l")
        self.play(Create(d2), run_time=0.3)
        self.pena(l2)
        self.gat("curvas diferentes")
        FI = TC(r"\int_0^1 A(\X)\,\dX=\int_0^1 A(\Y)\,\dY=\Me{0{,}316}", 1120, 560, 36)
        self.pena(FI)
        self.gat("mesma área embaixo")
        aa = poly_px([GA.px(0, 0)] + [GA.px(x, AX(x)) for x in np.linspace(0, 1, 60)] + [GA.px(1, 0)], mixh(BG_, E1, .3), z=2)
        ab = poly_px([GB.px(0, 0)] + [GB.px(y, AY(y)) for y in np.linspace(0, 1, 60)] + [GB.px(1, 0)], mixh(BG_, E2, .3), z=2)
        va = TC(r"\Me{0{,}316}", *GA.px(.42, .12), 32, "c")
        vb = TC(r"\Me{0{,}316}", *GB.px(.32, .12), 32, "c")
        self.play(GrowFromEdge(aa, LEFT), GrowFromEdge(ab, LEFT), run_time=0.6)
        self.pena(va, vb, lag=0.2)
        cd = T("CURVAS DIFERENTES, MESMA ÁREA", 1120, 660, 30, "left", MEN)
        self.gat("da direita")
        realce(self, cvb)                                              # a da direita a gente sabe integrar
        self.pena(cd)
        self.marca("v3_05", agora=True)

        # ── B4-2b · passo 3: calcular (alvo v3_06): o palco é o retângulo da fatia deitada; a conta C4 inteira ──
        self.an("B4-2b")
        self.secao("PASSO 3: CALCULAR")
        sai_ = [m for m in self.snap()] + [self.grade]
        self.play(*[FadeOut(m) for m in sai_], run_time=0.4)
        self.remove(*sai_)
        G = lateral(LAT2, 1.15, ymax=1.15, zt=(1,), yt=(1,), hcor=E1, hl=r"\X", vl=r"\f", passo=.25)
        self.grade = G["grade"]
        ret = poly_px([LAT2.px(0, 0), LAT2.px(.6, 0), LAT2.px(.6, h), LAT2.px(0, h)], mixh(BG_, E2, .45), z=2)
        cont = lin_px([LAT2.px(0, 0), LAT2.px(.6, 0), LAT2.px(.6, h), LAT2.px(0, h), LAT2.px(0, 0)], E2, 5, z=4)
        A_, B_ = LAT2.px(0, h), LAT2.px(.6, 0)
        alt_ = lin_px([(B_[0] + 34, B_[1]), (B_[0] + 34, A_[1])], CI, 3, z=5)
        le = TC(r"e^{-\Y^2}", B_[0] + 60, (A_[1] + B_[1]) / 2 - 22, 32, "l")
        la_ = leg("ALTURA", B_[0] + 60, (A_[1] + B_[1]) / 2 + 22, CI, "left", 26)
        ch = chave_px(A_[0], B_[0], B_[1] + 34, E2)
        cy_ = TC(r"\Y", (A_[0] + B_[0]) / 2, B_[1] + 74, 34, "c")
        cf = leg("COMPRIMENTO", (A_[0] + B_[0]) / 2, B_[1] + 122, E2, "center", 26)
        py_ = TP(r"\Y=0{,}6", 270, 240, 30, "c")
        self.play(FadeIn(G["grade"]), GrowFromPoint(G["eh"], LAT2.P(0, 0)), GrowFromPoint(G["ev"], LAT2.P(0, 0)), GrowFromEdge(ret, DOWN), Create(cont),
                  run_time=0.6)
        self.pena(G["lh"], G["lv"], G["nums"], py_, lag=0.05, passo=0.04)
        self.play(Create(ch), Create(alt_), run_time=0.4)
        self.pena(cy_, cf, le, la_, lag=0.15)
        self.gat("a de dentro é")
        C1 = L([("i", r"\int_{\Az{0}}^{\Co{\Y}}e^{-\Y^2}\,\dX"), ("e1", "="), ("b", r"e^{-\Y^2}\Big[\X\Big]_0^{\Y}"), ("e2", "="), ("r", r"\Y\,e^{-\Y^2}")],
               1120, 190, 36)
        self.pena(parte(C1, sel(C1, "i"), "∫₀^y e^(−y²) dx"))
        percorre(self, LAT2, lambda x: h, 0, .6, dur=4.5, cor=CI)       # palco vivo: o x anda de 0 a y sob o teto reto
        self.gat("o é elevado a")
        realce(self, alt_, le, la_, cor=CI)
        self.gat("não depende de xis")
        realce(self, ret, cont)
        realce(self, ret, cont)
        self.gat("sai para fora")
        self.pena(parte(C1, sel(C1, ["e1", "b"]), "= e^(−y²)[x]₀^y"))
        realce(self, cont)
        # D2 passo 2: "altura vezes comprimento": a chave do comprimento (y) e a da altura (e^(−y²)) acendem uma depois da outra; o produto
        # y e^(−y²) voa do retângulo (dos rótulos dele) para a coluna
        self.gat("altura vezes comprimento")
        realce(self, ch, cy_, cf)
        realce(self, alt_, le, la_, atraso=0.6)
        rD = sel(C1, "r")
        self.pena(parte(C1, sel(C1, "e2"), "="))
        voos(self, [(cy_.copy(), parte(C1, [rD[0]], "y (comprimento)")), (le.copy(), parte(C1, rD[1:], "e^(−y²) (altura)"))], rt=0.9)
        C1._esc = True
        self.gat("agora a de fora")
        C2 = L([("i", r"\int_0^1"), ("r", r"\Y\,e^{-\Y^2}"), ("dy", r"\,\dY")], 1120, 290, 36, caneta=False)
        voos(self, [(VGroup(*gl(C1, "r")).copy(), parte(C2, sel(C2, "r"), "y e^(−y²)"))], rt=0.9)
        self.pena(parte(C2, sel(C2, ["i", "dy"]), "∫ dy"))
        C2._esc = True
        # D2 passo 3: o retângulo encolhe até o ponto (0,6; 0,419); entra o gráfico de A(y) = y e^(−y²) em [0, 1] (escala do v3_05)
        GY = Lat(300, 780, 360, 562)
        pY = ponto_px(*GY.px(.6, AY(.6)), E2, 11, z=9)
        resto = [G["grade"], G["eh"], G["ev"], G["lh"], G["lv"], G["nums"], cont, py_, le, ch, cy_, cf, la_, alt_]
        self.play(ReplacementTransform(ret, pY), *[FadeOut(m, rate_func=rapido) for m in resto], run_time=0.6)
        self.remove(*resto)
        gy = eixos_a(GY, E2, r"\Y")
        self.grade = gy[0]
        q = GY.px(0, .9)
        lA = TC(r"A(\Y)=\Y\,e^{-\Y^2}", q[0] + 26, q[1] + 4, 30, "l")
        self.play(FadeIn(gy[0]), GrowFromPoint(gy[1], GY.P(0, 0)), GrowFromPoint(gy[2], GY.P(0, 0)), run_time=0.5)
        self.pena(gy[3], gy[4], gy[5], lA, lag=0.05, passo=0.04)
        yb = ValueTracker(0.0)
        self.add(yb)
        cvY = always_redraw(lambda: curva(GY, cX(AY, 0, max(.002, yb.get_value()), 60), E2, 4, z=6))
        pdY = always_redraw(lambda: ponto_px(*GY.px(yb.get_value(), AY(yb.get_value())), E2, 9, z=8))
        self.add(cvY, pdY)
        self.play(yb.animate.set_value(1.0), run_time=1.8, rate_func=linear)             # o ponto desliza de y = 0 a y = 1 (a fatia andando)
        cvY.clear_updaters()
        self.remove(pdY, yb)
        self.gat("que veio do comprimento")
        acende(self, (VGroup(gl(C2, "r")[0]), MEN), rt=0.8)
        percorre(self, GY, AY, 0, 1, dur=4.0, cor=E2)                  # palco vivo: a fatia anda de y = 0 a 1
        self.gat("quase a derivada do")
        r2 = list(gl(C2, "r"))
        acende(self, (VGroup(r2[0]), MEN), (VGroup(*r2[2:]), MEN), rt=0.9)    # o y e o −y² do expoente
        # D2 passo 4: "chama u de ípsilon ao quadrado": a régua u = y² embaixo do eixo y (marcas y 0 → u 0, 0,5 → 0,25, 1 → 1)
        self.gat("chama u de")
        C3 = L([("u", r"u=\Y^2"), ("i1", r"\ \Rightarrow\ "), ("du", r"du=2\Y\,\dY"), ("i2", r"\ \Rightarrow\ "), ("yd", r"\Y\,\dY=\dfrac{du}{2}")],
               1120, 385, 34)
        Yr = GY.px(0, 0)[1] + 80
        regua = lin_px([(GY.px(0, 0)[0], Yr), (GY.px(1, 0)[0], Yr)], GEO, 1.5, z=5)
        tks = VGroup(*[lin_px([(GY.px(v, 0)[0], Yr - 7), (GY.px(v, 0)[0], Yr + 7)], GEO, 1.5, z=5) for v in (0, .5, 1)])
        lu = TC(r"\Ge{u=\Y^2}", GY.px(0, 0)[0] - 24, Yr, 26, "r")
        lus = [TC(r"\Ge{%s}" % t_, GY.px(v, 0)[0], Yr + 34, 24, "c") for v, t_ in ((0, "0"), (.5, "0{,}25"), (1, "1"))]
        self.pena(parte(C3, sel(C3, "u"), "u = y²"), extra=[Create(regua), Create(tks)])
        self.pena(lu, *lus, lag=0.1)
        self.gat("dê u é dois")
        percorre(self, GY, AY, 0, 1, dur=5.0, cor=E2)
        self.pena(parte(C3, sel(C3, ["i1", "du"]), "⇒ du = 2y dy"))
        self.gat("então ípsilon dê ípsilon")
        self.pena(parte(C3, sel(C3, ["i2", "yd"]), "⇒ y dy = du/2"))
        C3._esc = True
        # D2 passo 5: as marcas 0 e 1 da régua ganham um sublinhado fino, cada uma no seu gatilho
        self.gat("ípsilon igual a zero")
        C4_ = L([("a", r"\Y=0\to u=0"), ("q", r"\qquad"), ("b", r"\Y=1\to u=1")], 1120, 470, 34)
        self.pena(parte(C4_, sel(C4_, "a"), "y = 0 → u = 0"))
        acende(self, (lus[0], GEO), rt=0.8)
        self.gat("e ípsilon igual a um")
        self.pena(parte(C4_, sel(C4_, "b"), "y = 1 → u = 1"))
        acende(self, (lus[2], GEO), rt=0.8)
        C4_._esc = True
        self.gat("fica meio da")
        C5 = L([("a", r"=\dfrac{1}{2}\int_0^1 e^{-u}\,du"), ("e", "="), ("b", r"\dfrac{1}{2}\Big[-e^{-u}\Big]_0^1")], 1120, 575, 36)
        self.pena(parte(C5, sel(C5, "a"), "= ½∫₀¹ e^(−u) du"))
        realce(self, regua, tks)
        self.gat("de é elevado a menos u")
        realce(self, cvY)
        self.gat("a primitiva é menos")
        self.pena(parte(C5, sel(C5, ["e", "b"]), "= ½[−e^(−u)]₀¹"))
        C5._esc = True
        # D2 passo 6: de "em um, menos um sobre é" até "metade disso", a área sob a curva pinta por tiras (magenta, alpha 0,35)
        self.gat("em um menos")
        k1, k2 = self._k_frase("B4-2b", "em um menos"), self._k_frase("B4-2b", "metade disso")
        tiras_ = pinta_tiras(self, GY, AY, 0, 1, max(1.0, ANC["B4-2b"]["t"][k2] - ANC["B4-2b"]["t"][k1]), E2, .35)
        C6 = L([("a", r"=\dfrac{1}{2}\Big(-e^{-1}"), ("b", r"-(-e^{0})\Big)"), ("e", "="), ("r", r"\dfrac{1-1/e}{2}")], 1120, 690, 36)
        self.pena(parte(C6, sel(C6, "a"), "= ½(−e^(−1)"))
        self.gat("em zero menos")
        self.pena(parte(C6, sel(C6, "b"), "− (−e⁰))"))
        self.gat("menos menos um")
        self.pena(parte(C6, sel(C6, ["e", "r"]), "= (1 − 1/e)/2"))
        C6._esc = True
        self.gat("metade disso")
        C7 = L([("a", r"\approx\dfrac{1-0{,}368}{2}"), ("e", r"\approx"), ("v", r"\Me{0{,}316}")], 1150, 805, 36)
        self.pena(parte(C7, sel(C7, "a"), "≈ (1 − 0,368)/2"))
        # D2 passo 7: o 0,316 menta voa do resultado da coluna para dentro da área
        self.gat("zero vírgula três")
        self.pena(parte(C7, sel(C7, ["e", "v"]), "≈ 0,316"))
        C7._esc = True
        v316 = TC(r"\Me{0{,}316}", *GY.px(.5, .13), 32, "c", caneta=False)
        voos(self, [(VGroup(*gl(C7, "v")).copy(), v316)], rt=0.9)
        self.marca("v3_06", agora=True)
        self.gat("a integral que travava")                # recapitulação no palco: a mesma região, a fatia em pé vira a deitada
        tiras_.clear_updaters()
        lat = [*gy, lA, cvY, pY, regua, tks, lu, *lus, tiras_, v316]
        regT = regiao(TRI, [(0, 0), (1, 1), (0, 1)])
        eT = curva(TRI, [(0, 1), (1, 1)], GEO, 2)
        dT = curva(TRI, [(0, 0), (1, 1)], AZC, 3)
        yT = curva(TRI, [(0, 0), (0, 1)], GEO, 2)
        tvT = tiraV(TRI, .5, .5, 1)
        gT = papel_v(TRI, (0, 1.12, 0, 1.12))
        sxT, syT, lxT, lyT = eixos_v(TRI, 1.2, 1.2)
        k1x, k1y = tick(TRI, "x", 1, r"\Am{1}"), tick(TRI, "y", 1, r"\Mg{1}")
        self.play(*[FadeOut(m) for m in lat], run_time=0.5)
        self.remove(*lat)
        self.play(FadeIn(gT), GrowFromPoint(sxT, TRI.P(0, 0)), GrowFromPoint(syT, TRI.P(0, 0)), FadeIn(regT), Create(eT), Create(dT), Create(yT),
                  Create(k1x[0]), Create(k1y[0]), run_time=0.7)
        self.grade = gT
        ryx = rot(TRI, r"\Az{\Y=\X}", (.62, .5), 10, 10, 30)
        self.pena(lxT, lyT, k1x[1], k1y[1], ryx, lag=0.08, extra=[GrowFromEdge(tvT, DOWN)])
        self.gat("mudou o jeito de")                       # a tira em pé vira a deitada; a diagonal troca de papel (entrada → saída)
        dT2 = curva(TRI, [(0, 0), (1, 1)], CORAL, 3)
        rxy = rot(TRI, r"\Co{\X=\Y}", (.62, .5), 10, 10, 30)
        rx0 = rot(TRI, r"\Az{\X=0}", (0, .78), -18, 0, 28, "r")
        thT = tiraH(TRI, .6, 0, .6)
        self.play(ReplacementTransform(tvT, thT), ReplacementTransform(dT, dT2), ReplacementTransform(ryx, rxy), yT.animate.set_stroke(AZC, W(3)), run_time=1.4)
        ja_escrita(rxy.f)
        self.pena(rx0)

        # ── B4-3 · o erro clássico (alvos v2_07, v2_08), layout A ──
        self.an("B4-3")
        self.secao("O ERRO CLÁSSICO")
        # o palco: o quadrado [0, 1]² (eixos do triângulo) e a reta x = 1; o triângulo sai
        quad = curva(TRI, [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], GEO, 2, dash=(7, 7), alpha=.6, z=3)
        x1c = curva(TRI, [(1, 0), (1, 1.05)], CORAL, 3, z=5)
        rx1 = rot(TRI, r"\Co{\X=1}", (1, .95), 16, 0, 28, "l")
        velhos = [regT, eT, dT2, yT, thT, rxy, rx0]
        self.play(*[FadeOut(m) for m in velhos], Create(quad), Create(x1c), run_time=0.8)
        self.remove(*velhos)
        self.pena(rx1)
        self.gat("trocar só o dê")
        realce(self, quad)                                             # a região lida com os limites de antes
        col = [m for m in self.snap() if pxof(m.get_left())[0] >= 1100]
        self.play(*[FadeOut(m) for m in col], run_time=0.4)
        self.remove(*col)
        Wr = L([("io", r"\int_0^1\!"), ("ii", r"\int_{\Al{\X}}^{1}"), ("e", r"e^{-\Y^2}"), ("dx", r"\,\Al{d\X}"), ("dy", r"\,\dY")], 1120, 260, 50)
        self.pena(Wr)
        so_ = mixl([("t", "SÓ TROCOU", AL), ("m", r"\dX"), ("t", "COM", AL), ("m", r"\dY")], 1120, 370, 36)
        self.pena(*so_.p, lag=0.12)
        self.gat("deixar os limites como")
        realce(self, x1c, rx1)                                         # o limite 1 que ficou como estava
        acende(self, (VGroup(*sem_alto(Wr, "io")[0]), None), (VGroup(*sem_alto(Wr, "ii")[0]), None), rt=0.8)
        self.gat("olha o que acontece")
        realce(self, quad)
        self.gat("passa a ser em")
        acende(self, (gl(Wr, "dx"), AL), rt=0.8)
        # "de xis até um": a tira deitada em y = 0,55 nasce de x até 1; o começo dela é o próprio x (âmbar), com "x ?"
        self.gat("de xis até um o")
        xt = ValueTracker(.45)
        self.add(xt)
        YT = .55
        tira_ = always_redraw(lambda: tiraH(TRI, YT, xt.get_value(), 1, alpha=.5))
        pc = always_redraw(lambda: ponto_px(*TRI.px(xt.get_value(), YT), E1, 10))
        pf = ponto_px(*TRI.px(1, YT), CORAL, 9)
        px0 = always_redraw(lambda: ponto_px(*TRI.px(xt.get_value(), 0), E1, 10))
        tr0 = always_redraw(lambda: curva(TRI, [(xt.get_value(), 0), (xt.get_value(), YT - .03)], E1, 2, dash=(5, 6), alpha=.8, z=4))
        lq = always_redraw(lambda: TP(r"\Al{\X\,?}", TRI.px(xt.get_value(), YT)[0] - 14, TRI.px(xt.get_value(), YT)[1] - 36, 32, "r", caneta=False))
        self.play(GrowFromEdge(tira_.copy(), RIGHT), FadeIn(pf, scale=.5), run_time=0.7)
        self.add(tira_)
        self.play(FadeIn(pc, scale=.5), FadeIn(px0, scale=.5), Create(tr0.copy()), FadeIn(lq), run_time=0.6)
        self.add(tr0)
        # "ao mesmo tempo a variável que anda e o limite dela": o x anda e o começo da fatia anda junto
        self.gat("ao mesmo tempo")
        self.play(xt.animate.set_value(.15), run_time=0.8)
        ext1 = curva(TRI, [(.15, YT - .03), (1, YT - .03), (1, YT + .03), (.15, YT + .03), (.15, YT - .03)], GEO, 2, dash=(5, 6), z=3)
        self.add(ext1)
        self.play(xt.animate.set_value(.75), run_time=0.9)
        ext2 = curva(TRI, [(.75, YT - .03), (1, YT - .03), (1, YT + .03), (.75, YT + .03), (.75, YT - .03)], GEO, 2, dash=(5, 6), z=3)
        self.add(ext2)
        self.play(xt.animate.set_value(.45), run_time=0.7)
        sd1 = seta_px(TRI.px(.45, -.09), TRI.px(.6, -.09), E1, 2.5, 14)
        sd2 = seta_px(TRI.px(.45, -.09), TRI.px(.3, -.09), E1, 2.5, 14)
        ca = mixl([("t", "O COMEÇO ANDA COM", AL), ("m", r"\Al{\X}")], 300, 215, 32)
        self.play(GrowFromPoint(sd1, TRI.P(.45, -.09)), GrowFromPoint(sd2, TRI.P(.45, -.09)), run_time=0.4)
        self.pena(*ca.p, lag=0.12)
        lv = mixl([("m", r"\Al{\X}"), ("t", "É LIMITE E VARIÁVEL", AL)], 1120, 480, 36)
        self.pena(*lv.p, lag=0.12)
        self.marca("v2_07", agora=True)
        self.gat("essa escrita não")
        realce(self, pc, lq)                                   # o x que é ao mesmo tempo limite e variável
        lim, alto = sem_alto(Wr, "ii")
        xl = min(lim, key=lambda x: x.get_center()[1])
        cxl = sublinha_fica(VGroup(xl), AL)
        self.play(Create(cxl), run_time=0.6)
        # "sobra um xis solto": a coluna se reorganiza e o mapa 9 dá (1 − x)·∫…
        self.gat("a conta mesmo assim")
        realce(self, tira_, pc)
        self.gat("sobra um xis solto")
        Wr2 = L([("io", r"\int_0^1\!"), ("ii", r"\int_{\Al{\X}}^{1}"), ("e", r"e^{-\Y^2}"), ("dx", r"\,\Al{d\X}"), ("dy", r"\,\dY")], 1120, 240, 44, caneta=False)
        self.play(FadeOut(cxl), *[FadeOut(m) for m in (*so_.p, *lv.p)], Transform(Wr, Wr2), run_time=0.5)
        self.remove(cxl, *so_.p, *lv.p)
        lim, alto = sem_alto(Wr, "ii")
        xl = min(lim, key=lambda x: x.get_center()[1])
        um_ = max(lim, key=lambda x: x.get_center()[1])
        W1 = L([("eq", "="), ("p1", "("), ("um", "1"), ("mn", "-"), ("x", r"\Al{\X}"), ("p2", ")"), ("d", r"\cdot"), ("io", r"\int_0^1"), ("e", r"e^{-\Y^2}"),
                ("dy", r"\,\dY")], 1120, 350, 42)
        passo(self, Wr, W1, [("io", "io"), ("e", "e"), ("dy", "dy"), ([list(Wr[0]).index(xl)], "x"), ([list(Wr[0]).index(um_)], "um")], rt=1.3, copia=True,
              nota="mapa 9 (B4-3: a forma errada deixa (1 − x) · ∫₀¹ e^(−y²) dy; o 1 e o x vêm dos limites)")
        rc_ = mixl([("t", "RESULTADO COM", AL), ("m", r"\Al{\X}"), ("t", "?", AL)], 1175, 460, 44)
        cz = cruz_px(1140, 458, AL, 1)
        self.play(Create(cz), run_time=0.3)
        self.pena(*rc_.p, lag=0.12)
        # "a integral dupla é um número": o "resultado" em função de x (uma reta), e o valor certo, um número só
        self.gat("só que a integral")
        for m in (tira_, pc, px0, tr0, lq):
            m.clear_updaters()
        palco_ = [m for m in self.snap() if pxof(m.get_right())[0] < 1100] + [self.grade]
        self.play(*[FadeOut(m) for m in palco_], run_time=0.4)
        self.remove(*palco_, xt)
        I0v = 0.746824
        GR = Lat(250, 860, 620, 700)
        gR = VGroup()
        for a_ in np.arange(0, 1.1001, .1):
            gR.add(lin_px([GR.px(a_, 0), GR.px(a_, .9)], GRADE, 1.2, z=-9))
        for b_ in np.arange(0, .9001, .1):
            gR.add(lin_px([GR.px(0, b_), GR.px(1.1, b_)], GRADE, 1.2, z=-9))
        self.grade = gR
        ex_ = seta_px(GR.px(-.03, 0), GR.px(1.12, 0), E1, 3, 16, z=6)
        er_ = seta_px(GR.px(0, -.03), GR.px(0, .92), GEO, 3, 16, z=6)
        lxR = TC(r"\X", GR.px(1.12, 0)[0] + 24, GR.px(1.12, 0)[1], 32, "c")
        lrR = leg("RESULTADO", GR.px(0, .92)[0] + 18, GR.px(0, .92)[1] + 8, GEO, "left", 26)
        k1 = tick(GR, "x", 1, "1")
        self.play(FadeIn(gR), GrowFromPoint(ex_, GR.P(0, 0)), GrowFromPoint(er_, GR.P(0, 0)), Create(k1[0]), run_time=0.4)
        self.pena(lxR, lrR, k1[1], lag=0.05, passo=0.035)
        reta = curva(GR, [(0, I0v), (1, 0)], AL, 4, z=5)
        self.play(Create(reta), run_time=0.7, rate_func=linear)
        pts_ = []
        for xx, sv, fr in ((.2, r"0{,}597", "é um número"), (.8, r"0{,}149", "não pode depender de")):
            self.gat(fr)
            v = (1 - xx) * I0v
            dl = curva(GR, [(xx, 0), (xx, v)], E1, 2, dash=(5, 6), z=4)
            dp_ = ponto_px(*GR.px(xx, v), AL, 10)
            q = GR.px(xx, v)
            lv_ = TC(r"\Al{" + sv + "}", q[0] + 16, q[1] - 28, 30, "l")
            kx = tick(GR, "x", xx, r"\Am{" + str(xx).replace(".", "{,}") + "}")
            self.play(Create(dl), Create(kx[0]), FadeIn(dp_, scale=.5), run_time=0.5)
            self.pena(lv_, kx[1], lag=0.2)
            pts_ += [dl, dp_, lv_, *kx]
        self.gat("é o mesmo aviso")
        m316 = curva(GR, [(0, .316), (1.05, .316)], MEN, 3, dash=(8, 7), z=4)
        q = GR.px(1.06, .316)
        l316 = TC(r"\Me{0{,}316}", q[0] + 8, q[1], 30, "l")
        un = T("UMA INTEGRAL DUPLA É UM NÚMERO", 1120, 600, 34, "left", MEN)
        self.play(Create(m316), run_time=0.7)
        self.pena(l316, un, lag=0.3)
        self.gat("só pode depender da")
        rd = leg("DENTRO: SÓ A VARIÁVEL DE FORA", 1120, 700, GEO, "left", 28)
        self.pena(rd)
        self.marca("v2_08", agora=True)
        realce(self, reta, atraso=0.4)                                 # o "resultado" que depende de x
        self.gat("por isso a troca")
        realce(self, m316, l316, atraso=0.4)                           # o número certo
        # "por isso a troca certa começa pela região": volta o triângulo, com a tira deitada certa (de 0 a y)
        self.gat("começa pela região")
        graf = [gR, ex_, er_, lxR, lrR, *k1, reta, m316, l316, *pts_]
        coluna = [m for m in self.snap() if pxof(m.get_left())[0] >= 1100]
        self.play(*[FadeOut(m) for m in graf + coluna], run_time=0.4)
        self.remove(*graf, *coluna)
        g3 = papel_v(TRI, (0, 1.12, 0, 1.12))
        self.grade = g3
        sx3, sy3, lx3_, ly3_ = eixos_v(TRI, 1.2, 1.2)
        self.play(FadeIn(g3), GrowFromPoint(sx3, TRI.P(0, 0)), GrowFromPoint(sy3, TRI.P(0, 0)), run_time=0.5)
        self.pena(lx3_, ly3_)
        self.gat("primeiro redesenha o")
        tr = regiao(TRI, [(0, 0), (1, 1), (0, 1)])
        d1 = curva(TRI, [(0, 0), (1, 1)], CORAL, 3)
        d2 = curva(TRI, [(0, 1), (1, 1)], GEO, 2)
        d3 = curva(TRI, [(0, 0), (0, 1)], AZC, 3)
        self.play(FadeIn(tr), Create(d1), Create(d2), Create(d3), run_time=0.9)
        self.gat("depois acha os limites")
        tt = tiraH(TRI, .55, 0, .55)
        q1, q2 = pontos_es(TRI, (0, .55), (.55, .55))
        r0_ = rot(TRI, r"\Az{0}", (0, .55), -40, -28, 30)
        ry_ = rot(TRI, r"\Co{\Y}", (.55, .55), 34, -34, 30)
        self.play(GrowFromEdge(tt, LEFT), FadeIn(q1, scale=.5), FadeIn(q2, scale=.5), run_time=0.6)
        self.pena(r0_, ry_, lag=0.2)
        self.gat("e só então escreve")
        realce(self, tt, r0_, ry_)                                     # a fatia deitada que dá os limites
        OK = L([("io", r"\int_0^1\!"), ("ii", r"\int_{\Az{0}}^{\Co{\Y}}"), ("e", r"e^{-\Y^2}"), ("dx", r"\,\dX"), ("dy", r"\,\dY")], 1120, 260, 46)
        self.pena(OK)
        ck = check_px(1800, 260)
        self.play(Create(ck), run_time=0.4)
        self.gat("a região manda")
        realce(self, tr, d1, d2, d3)                                   # a região que escolhe os limites
        ar = leg("A REGIÃO ESCOLHE OS LIMITES", 1120, 360, MEN, "left", 28)
        self.pena(ar)
        self.sai_fim()
