"""Lote PB3 · DOIS ENGANOS (handoff v2; quadros 08, 09, 10). B3-1/2: vórtice no palco (furo 0,55), cruz radial (1,35; 0)–(2,25; 0) e tangencial
(1,8; ±0,45) pelo fluxo exato t 0 → 1,07, fantasma e arco da órbita; arcos ↻/↺; a cruz vira tracejado e a rodinha R = 0,4 anda 2 s sem girar; a regra
do quociente (o meio → o resultado por TransformByGlyphMap), rot F = 0 e o domínio. B3-3: layout B, setas de fora com anel coral, irrotacional.
B3-4: tornado (anéis 0,5…3), rodinha de dentro girando, de fora sem girar. B3-5/6: o rio (setas, margens, perfil), rodinhas presas a y/9 (×3), o mapa
violeta, + e −, fórmulas embaixo."""
from MF_Tools import TransformByGlyphMap

from v27 import *  # noqa: F401,F403
from sec_ha import AN, VD, VE, hook_campos

V = Vista(600, 540, 120)


class LoteB3(Base):
    ANTES = "ROTACIONAL"
    def corpo(self):
        # ── B3-1 ──
        self.an("B3-1")
        self.secao("DOIS ENGANOS")
        cv = campo7(V, F_VORT, rmin=0.75, mmax=1.4, nome="B3 vórtice")
        fu = furo7(V, 0.55)
        self.play(FadeIn(fu), cresce_campo(cv, 1.6))
        fF = TC(r"\F = \dfrac{(-\Y,\ \X)}{\X^2+\Y^2}", 1080, 300, 42)
        self.gat("o mesmo campo de giro")
        self.play(caneta(fF))
        gr = vlinha(V, [(1.35, 0), (2.25, 0)], GEO, 3, dash=(8, 8))
        gt = vlinha(V, [(1.8, -0.45), (1.8, 0.45)], GEO, 3, dash=(8, 8))
        rad = Material(V, seg_pts((1.35, 0), (2.25, 0)), fl_vort, CORAL, 7, pontas=True)
        tan = Material(V, seg_pts((1.8, -0.45), (1.8, 0.45)), fl_vort, CORAL, 7, pontas=True)
        orb = vlinha(V, circ_pts(1.8, (0, 0), 60, 0, 0.33), GEO, 3, alpha=0.7, dash=(6, 8))
        sonda = {"f": lambda: [tuple(float(q[0]) for q in fl_vort(np.array([1.8]), np.array([0.0]), rad.t))]}
        
        self.gat("repara no que isso faz com os vizinhos")
        f_cl = clareira_viva(cv, lambda: sonda["f"](), 1.0)
        cv.suspend_updating()
        for s_ in cv:
            s_._escondida = False
            op_seta(s_, 1)
        alvo_cl = esconde(cv, clar([], sonda["f"](), 1.0))
        self.play(some(alvo_cl), Create(rad.tr), Create(tan.tr), *[FadeIn(p) for p in rad.pontas + tan.pontas], run_time=0.7)
        cv.resume_updating()
        self.add(cv)                                   # o grupo entra na cena: a clareira acompanha a sonda (o updater passa a rodar)
        self.add(rad, tan)
        dt = 3 / FPS
        for b, nome, alvo in ((rad, "radial", -1 / 1.8 ** 2), (tan, "tangencial", 1 / 1.8 ** 2)):
            a0 = b.ang()
            b.em(dt * 0.3)
            w_ = (b.ang() - a0) / (dt * 0.3)
            b.em(0)
            print(f"[braços] B3 {nome}: {w_:+.4f} rad/s no início (∓1/r² em r = 1,8: {alvo:+.4f})")
        self.gat("pega o braço que aponta para fora")
        self.add(gr, gt)
        self.play(*corre(self, [rad, tan], 1.07, 3.0), Create(orb), run_time=3.0)
        m = fl_vort(np.array([1.8]), np.array([0.0]), 1.07)
        mc = (float(m[0][0]), float(m[1][0]))
        print(f"[braços] B3: centro da cruz andou {math.atan2(mc[1], mc[0]):.3f} rad em t = 1,07 (alvo 0,33)")
        a_rad = giro_seta(V, mc, 0.62, 1.45, 0.85)
        self.gat("então esse braço tomba")
        self.play(Create(a_rad), run_time=0.6)
        self.ate(0.97)

        # ── B3-2 ──
        self.an("B3-2")
        a_tan = giro_seta(V, mc, 0.62, -1.9, -1.3)
        self.gat("gira no sentido anti-horário")
        self.play(Create(a_tan), run_time=0.6)
        rd = Roda(V, 0.4).pose(mc, 0.0)
        self.gat("e os dois giram exatamente na mesma rapidez")
        rdash = vlinha(V, [tuple(p) for p in rad.XY[[0, -1]]], CORAL, 4, dash=(8, 8))
        tdash = vlinha(V, [tuple(p) for p in tan.XY[[0, -1]]], CORAL, 4, dash=(8, 8))
        sonda["f"] = lambda: [rd.c]
        self.play(FadeOut(rad), FadeOut(tan), FadeIn(rdash), FadeIn(tdash), FadeIn(rd, scale=0.7), run_time=0.6)
        self.remove(rad, tan)
        self.play(UpdateFromAlphaFunc(rd, lambda m_, a: m_.pose(tuple(float(q[0]) for q in fl_vort(np.array([mc[0]]), np.array([mc[1]]), 0.9 * a)), 0.0)),
                  run_time=2.0, rate_func=smooth)
        print(f"[hook] B3-2: rodinha andou pela órbita sem girar (orientação {math.degrees(rd.ang):.2f}°)")
        A1 = TC(r"\dfrac{\partial \Qq}{\dx} = \dfrac{(\X^2+\Y^2) - \X\cdot 2\X}{(\X^2+\Y^2)^2}", 1080, 450, 40)
        A2 = TC(r"\dfrac{\partial \Qq}{\dx} = \dfrac{(\X^2+\Y^2) - \X\cdot 2\X}{(\X^2+\Y^2)^2} = \dfrac{\Y^2 - \X^2}{(\X^2+\Y^2)^2}", 1080, 450, 40)
        B1 = TC(r"\dfrac{\partial \Pp}{\dy} = \dfrac{-(\X^2+\Y^2) + \Y\cdot 2\Y}{(\X^2+\Y^2)^2}", 1080, 610, 40)
        B2 = TC(r"\dfrac{\partial \Pp}{\dy} = \dfrac{-(\X^2+\Y^2) + \Y\cdot 2\Y}{(\X^2+\Y^2)^2} = \dfrac{\Y^2 - \X^2}{(\X^2+\Y^2)^2}", 1080, 610, 40)
        self.gat("fazendo as derivadas")                                       # final: "as duas parcelas" escritas juntas (a voz real é mais rápida)
        self.play(caneta(A1, ritmo=0.7), caneta(B1, ritmo=0.7, atraso=0.3))
        tb = []
        for a, b in ((A1, A2), (B1, B2)):
            na, nb = len(a[0]), len(b[0])
            tb.append(TransformByGlyphMap(a, b, (list(range(na)), list(range(na))), ([], list(range(na, nb))), printing=False, run_time=1.0))
        self.play(*tb, run_time=1.0)
        for a, b in ((A1, A2), (B1, B2)):
            ja_escrita(b)
            self.remove(a)
            self.add(b)
        nA = len(A2[0])
        self.gat("são iguais")
        self.play(pulso(VGroup(*A2[0][len(A1[0]) + 1:len(A1[0]) + 6], *B2[0][len(B1[0]) + 1:len(B1[0]) + 6]), 1.12), run_time=0.8)
        R0 = TC(r"\rot \F = \vec 0", 1080, 745, 52)
        dom = TC(r"\text{em } \mathbb{R}^2 - \{(0,0)\}", 1080, 845, 40)
        self.gat("e a diferença é zero")
        self.play(caneta(R0))
        self.gat("menos na origem")
        self.play(caneta(dom), pulso(fu, 1.15, 2.0))
        self.ate(0.97)

        # ── B3-3 · os dois painéis ──
        self.an("B3-3")
        self.limpa_soltos()
        self.limpa_junto(rt=0.5)
        self.grade(papel(VE, area_px(VE, 130, 260, 700, 560)), papel(VD, area_px(VD, 1090, 260, 700, 560)))   # final: grade de cada painel
        pE, pD = painel(130, 260, 700, 560), painel(1090, 260, 700, 560)
        cE, cD = hook_campos(nome="B3-3")
        fD = furo7(VD, 0.6)
        c1E, c1D = vcirc(VE, 1, SAIF, 4, alpha=0.9), vcirc(VD, 1, SAIF, 4, alpha=0.9)
        self.play(FadeIn(pE), FadeIn(pD), FadeIn(fD), FadeIn(cE), FadeIn(cD), run_time=0.8)
        self.gat("na circunferência os dois campos")
        self.play(Create(c1E), Create(c1D), run_time=0.8)
        # final §2.3 (alvo 19, sb27 `b33v5`): seta em r = 1,5 (e a de r = 1) acesas com comprimento ∝ |F| (k = 0,5); anel coral e MAIS FORTE / MAIS FRACA
        kL = 0.5
        sk = lambda X, Y: math.hypot(X - 1, Y) < 0.3 or math.hypot(X - 1.5, Y) < 0.3 or (abs(Y + 0.75) < 0.3 and abs(X - 1.5) < 1.0)
        clE, clD = esconde(cE, sk), esconde(cD, sk)
        dst = {}
        for nome_, Vv, Fv in (("E", VE, F_GIRO), ("D", VD, F_VORT)):
            f1, f2 = Fv(1, 0), Fv(1.5, 0)
            dst[nome_] = (seta7(Vv.c2p(1, -f1[1] * kL / 2), Vv.c2p(1, f1[1] * kL / 2), CAMPO2, 7, 22).set_z_index(11),
                          seta7(Vv.c2p(1.5, -f2[1] * kL / 2), Vv.c2p(1.5, f2[1] * kL / 2), CAMPO2, 8, 24).set_z_index(11),
                          vcirc(Vv, 0.42, CORAL, 3.5, c=(1.5, 0)).set_z_index(10))
            print(f"[hook] B3-3 {nome_}: |F| em r = 1: {abs(f1[1]):.3f} ({abs(f1[1]) * kL * Vv.u:.0f} px); em r = 1,5: {abs(f2[1]):.3f} ({abs(f2[1]) * kL * Vv.u:.0f} px)")
        for s1, s2, _ in dst.values():
            s1._xy, s2._xy = (1, 0), (1.5, 0)
        lF = TXP("MAIS FORTE", *canto_xy(VE, 1.5, -0.75), 28, cor=CORAL)
        lFr = TXP("MAIS FRACA", *canto_xy(VD, 1.5, -0.75), 28, cor=CORAL)
        lI = legenda("NA CIRCUNFERÊNCIA: IGUAIS.  LOGO FORA: DIFERENTES.", 960, 880, SAIF, "center", 34)
        self.gat("olha a seta logo ali fora")
        self.play(UpdateFromAlphaFunc(VGroup(cE, cD), lambda m, a: [c_.contexto(a > 0.5) for c_ in m]), some(clE), some(clD),
                  GrowArrow(dst["E"][0]), GrowArrow(dst["E"][1]), GrowArrow(dst["D"][0]), GrowArrow(dst["D"][1]), run_time=0.7)
        self.gat("a seta de fora é mais forte")
        self.play(Create(dst["E"][2]), FadeIn(lF), run_time=0.6)
        self.gat("ela é mais fraca")
        self.play(Create(dst["D"][2]), FadeIn(lFr), run_time=0.6)
        self.play(FadeIn(lI, shift=0.1 * UP), run_time=0.5)
        fI = TC(r"\F\ \text{irrotacional} \iff \rot\F = \vec 0", 960, 960, 46, "c")
        self.gat("se chama irrotacional")
        self.play(caneta(fI))
        self.ate(0.97)

        # ── B3-4 · o tornado ──
        self.an("B3-4")
        self.limpa_junto(rt=0.5)
        self.grade(self.grade0)
        ct = campo_polar(V, F_TORN, [0.5, 1, 1.5, 2, 2.5, 3], arco=0.6, mmax=1.0, nome="B3-4 tornado")
        c1 = vcirc(V, 1, SAIF, 4)
        self.play(cresce_campo(ct, 1.0, lambda s: (round(math.hypot(*s._xy), 3), math.atan2(s._xy[1], s._xy[0]))))
        linhas = [(r"\text{dentro: }\ \F = (-\Y,\ \X)", 1120, 420, 44), (r"\rot\F = \V{2}\,\kk", 1160, 510, 44),
                  (r"\text{fora: }\ \F = \dfrac{(-\Y,\ \X)}{\X^2+\Y^2}", 1120, 650, 44), (r"\rot\F = \vec 0", 1160, 760, 44)]
        LN = [TC(s, x, y, sz) for s, x, y, sz in linhas]
        tt = VGroup(T("MODELO IDEALIZADO:", 1120, 270, 44), T("VÓRTICE DE RANKINE", 1120, 325, 44))    # final §2.13
        ri, ro = Roda(V, 0.3).pose((0, 0.62), 0.0), Roda(V, 0.32).pose((2.05, -0.6), 0.0)
        self.gat("cola os dois redemoinhos")
        self.play(caneta(LN[0]))                                                # final: "dentro" escrito desde "cola os dois redemoinhos"
        self.gat("encaixa certinho")
        self.play(Create(c1, run_time=0.8), caneta(LN[2]), self.em("o modelo clássico de um tornado", self.surge(tt, ri, ro)))
        mt = Motor(self, 0.6, "B3-4 tornado (rodinhas)").liga()
        p_in, p_out = (0.0, 0.62), (2.05, -0.6)

        def anda(p0, giro):
            def f(m_):
                x, y = fl_torn(np.array([p0[0]]), np.array([p0[1]]), mt.tau())
                m_.pose((float(x[0]), float(y[0])), giro * mt.tau())
            return f
        ri.add_updater(anda(p_in, 1.0))
        ro.add_updater(anda(p_out, 0.0))
        arc_i = giro_seta(V, (0, 0), 0.42, -0.3, 0.9, VIO, 3)
        arc_i._c0 = arc_i.get_center() - V.c2p(0, 0)
        arc_i.add_updater(lambda m_: m_.move_to(V.c2p(*ri.c) + m_._c0))
        self.add(arc_i)
        self.gat("o miolo gira como um corpo rígido")
        self.play(caneta(LN[1]))
        self.gat("em volta dele o ar dá voltas")
        self.play(caneta(LN[3]))
        lg = legenda("NA CIRCUNFERÊNCIA AS SETAS SÃO IGUAIS", 1124, 860)
        self.gat("uma rodinha no miolo gira")
        self.play(FadeIn(lg, shift=0.1 * UP), run_time=0.5)
        self.ate(0.97)
        for r in (ri, ro, arc_i):
            r.clear_updaters()

        # ── B3-5 · o rio ──
        self.an("B3-5")
        self.limpa_junto(rt=0.5)
        VR = Vista(960, 500, 90)
        self.grade(papel(VR))                                                 # final: a grade nasce dos eixos do rio (90 px por unidade)
        marg = VGroup(preenche(VR, [(-9.6, 3), (9.6, 3), (9.6, 3.5), (-9.6, 3.5)], CHAPA, 1, 1), preenche(VR, [(-9.6, -3), (9.6, -3), (9.6, -3.5), (-9.6, -3.5)], CHAPA, 1, 1),
                      vlinha(VR, [(-9.6, 3), (9.6, 3)], GEO, 3), vlinha(VR, [(-9.6, -3), (9.6, -3)], GEO, 3))
        cr = Campo7()
        X = -6.5
        while X <= 8.6 + 1e-6:
            for Y in (-2.4, -1.2, 0, 1.2, 2.4):
                cr.add(seta_campo(VR, X, Y, F_RIO(X, Y), 1.15, 1.0))
            X += 1.5
        cr.log("B3-5 rio", 1.5)
        prof = VGroup(vlinha(VR, [(-8.6, -3), (-8.6, 3)], GEO, 2), vlinha(VR, [(-8.6 + 1.3 * (1 - (-3 + 6 * i / 60) ** 2 / 9), -3 + 6 * i / 60) for i in range(61)], GEO, 3))
        self.gat("olha um rio")
        self.play(FadeIn(marg), cresce_campo(cr, 1.2, lambda s: s._xy[0]))
        self.gat("mais rápida no meio")
        self.play(Create(prof), run_time=0.9)
        tg_ = T("TEM GIRO?", 960, 218, 44, "center", SAIF)                      # final §2.10: a pergunta do rio, no alto do palco, fora das setas
        tg = VGroup(placa7(tg_, 10, 6), tg_)
        self.gat("esse rio tem giro ou não")
        self.play(FadeIn(tg, shift=0.1 * DOWN), run_time=0.5)
        rods = []
        XR = (-4.25, 0.25, 4.75)                        # meio passo entre as colunas de setas (−6,5 + 1,5k)
        rio_cl = esconde(cr, clar([], [(x_, y_) for x_ in XR for y_ in (1.8, 0, -1.8)], 0.8))
        for Xr in XR:
            for Yr in (1.8, 0, -1.8):
                r = Roda(VR, 0.38, pino=True).pose((Xr, Yr), 0.0)
                r._xy = (Xr, Yr)
                rods.append(r)
        self.gat("espalha rodinhas presas")
        self.play(some(rio_cl), FadeOut(tg), LaggedStart(*[FadeIn(r, scale=0.5) for r in rods], lag_ratio=0.08), run_time=0.9)
        self.remove(tg)
        mr = Motor(self, 3.0, "B3-5/6 rodinhas do rio (×3: câmera rápida, y = 1,8 → 0,6 rad/s na tela)").liga()
        for r in rods:
            r.add_updater(lambda m_: m_.pose(m_._xy, m_._xy[1] / 9 * mr.tau()))
        self.ate(0.97)

        # ── B3-6 ──
        self.an("B3-6")
        arcos = VGroup()
        for Xr in XR:
            for Yr, s in ((1.8, 1), (-1.8, -1)):
                arcos.add(giro_seta(VR, (Xr, Yr), 0.55, -0.2 * s, 0.9 * s, VIO, 3))
        self.gat("gira no sentido anti-horário")
        self.play(LaggedStart(*[Create(a) for a in arcos[0::2]], lag_ratio=0.2), run_time=0.8)
        self.gat("e ela gira no horário")
        self.play(LaggedStart(*[Create(a) for a in arcos[1::2]], lag_ratio=0.2), run_time=0.8)
        mais = T("+", *canto_xy(VR, -9.1, 2.15), 64, "center", VIO)
        menos = T("−", *canto_xy(VR, -9.1, -2.65), 64, "center", VIO)
        fF = TC(r"\F = \left(1 - \dfrac{\Y^2}{9},\ 0\right)", 260, 940, 46)
        fR = TC(r"\rot \F = -\dfrac{\partial \Pp}{\dy}\,\kk = \V{\dfrac{2\Y}{9}}\,\kk", 960, 940, 46)
        self.gat("a conta confirma")
        self.play(FadeIn(mais), FadeIn(menos), run_time=0.6)
        self.play(caneta(fF))
        self.play(caneta(fR))
        self.ate(0.97)
        for r in rods:
            r.clear_updaters()
            print(f"[rio] rodinha em y = {r._xy[1]:+.1f}: ½ rot = {r._xy[1] / 9:+.4f} rad/s (fluxo); na tela ×3 = {r._xy[1] / 3:+.3f} rad/s") if r._xy[0] == 0.25 else None
        self.sai_fim()

    def limpa_soltos(self):
        for m in list(self.mobjects):
            if isinstance(m, VGroup) and not len(m.family_members_with_points()):
                self.remove(m)
