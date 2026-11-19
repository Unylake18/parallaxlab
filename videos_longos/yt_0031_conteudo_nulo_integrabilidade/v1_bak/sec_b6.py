"""yt_0031 · B6 · continuidade uniforme (alvos 20 e 21; o B6-1 reaproveita o 3D b13t do alvo 06)."""
from v31 import *
from sec_b5 import miniatura_muro

LUPA_A0, LUPA_A1 = 0.04, 0.16      # janela da lupa em x (o alvo usa 0,06–0,16; alargada para caber os pares com k = 2 e 3)


def arr_sen1x(L=480):
    xs = (np.arange(L) + 0.5) / L * 2
    v = np.where(xs < .025, .5, (np.sin(1 / np.maximum(xs, 1e-6)) + 1) / 2)
    col = hx(RAMP0) * (1 - v[:, None]) + hx(CI) * v[:, None]
    return np.repeat(col[None, :, :], L, axis=0)


def arr_lupa(w=160, h=400):
    xs = LUPA_A0 + (np.arange(w) + 0.5) / w * (LUPA_A1 - LUPA_A0)
    v = (np.sin(1 / xs) + 1) / 2
    col = hx(RAMP0) * (1 - v[:, None]) + hx(CI) * v[:, None]
    return np.repeat(col[None, :, :], h, axis=0)


def lx(a):
    return 890 + (a - LUPA_A0) * 160 / (LUPA_A1 - LUPA_A0)


class PB6(B31):
    ANTES = "FRONTEIRA"

    def corpo(self):
        # ── B6-1 · um δ para a chapa inteira (sem alvo próprio) ───────────────────────────────────────
        self.an("B6-1")
        self.secao("CONTINUIDADE UNIFORME")
        self.gat("na chapa de dois metais")
        pn = painel(1120, 600, 640, 330)
        mini = miniatura_muro(1130, 610, 620, 320)
        cm = leg("A CHAPA DE DOIS METAIS", 1440, 970, GEO, "center", 22)
        self.play(Create(pn), FadeIn(mini), run_time=0.8)
        self.pena(cm)
        self.gat("mas numa densidade que varia")
        pal = Palco3D("b13", self, CAM_PREDIO31, s=1.0, cresce=1.0, afunda=1.0, tampas=0.0)
        pal.fundo.op.set_value(0.0)
        self.add(pal.fundo)
        self.play(pal.fundo.op.animate.set_value(1.0), run_time=0.8)
        ex = pal.prende(TC(r"\X", 0, 0, 30, "c"), "ex")
        ez = pal.prende(TC(r"\Ci{z}", 0, 0, 30, "c"), "ez")
        self.pena(ex, ez)
        self.gat("quase toda célula")
        self.play(*pal.anim(1.6, tampas=1.0), run_time=1.6)
        ta = pal.prende(leg("TAMPAS", 0, 0, CORAL, "left", 26), "tampaAlto", dx=85, dy=-19)
        self.pena(ta)
        self.gat("não basta cuidar")
        self.sublinha(cm, 1.0)
        q1 = T("E ONDE f É CONTÍNUA?", 1120, 300, 48)
        self.gat("onde ela é contínua as")
        self.pena(q1)
        self.gat("ser contínua quer dizer")
        gq = sorted(q1.family_members_with_points(), key=lambda g_: g_.get_left()[0])
        self.sublinha(VGroup(*gq[-9:-1]), 1.2)
        self.gat("mas dá para escolher")
        q2 = T("UM δ PARA A CHAPA INTEIRA?", 1120, 380, 34, cor=POS)
        self.pena(q2)
        self.wait(1.0)
        sai = [pn, mini, cm, ex, ez, ta, q1, q2]
        for m in sai:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        mapa = img_chapa(arr_dens(64))
        bd = borda_ch(CH, GEO, 3)
        sai3d(self, pal, entram=[mapa, bd], rt_cam=1.6, junto_cam=pal.anim(1.6, tampas=0.0, cresce=0.0, chao=1.0, afunda=0.0))
        sx, sy, lxx, lyy = eixos_chapa()
        self.play(FadeIn(sx), FadeIn(sy), run_time=0.4)
        self.pena(lxx, lyy)

        # ── B6-2 · continuidade uniforme (alvo 20) ────────────────────────────────────────────────────
        self.an("B6-2")
        self.gat("dá quando a região")
        k0 = leg("K FECHADO E LIMITADO, f CONTÍNUA EM K", 1124, 250, GEO, "left", 24)
        self.pena(k0)
        self.gat("para todo épsilon maior")
        e1 = TC(r"\forall\eps>0\ \ \exists\del>0:\ \ \forall\,\XX,\YY\in K,", 1120, 330, 38)
        self.pena(e1)
        # a régua de dois pontos (objeto único): X e Y a distância fixa (Y = X − (0,12; 0,12))
        u = ValueTracker(0.0)
        cam = [(.45, .5), (1.2, .45), (1.9, 1.9)]
        L1 = math.dist(cam[0], cam[1])
        L2 = math.dist(cam[1], cam[2])

        def posX(t):
            s_ = t * (L1 + L2)
            if s_ <= L1:
                a = s_ / L1
                return (cam[0][0] + (cam[1][0] - cam[0][0]) * a, cam[0][1] + (cam[1][1] - cam[0][1]) * a)
            a = (s_ - L1) / L2
            return (cam[1][0] + (cam[2][0] - cam[1][0]) * a, cam[1][1] + (cam[2][1] - cam[1][1]) * a)

        def regua_em(X):
            Y = (X[0] - .12, X[1] - .12)
            return VGroup(lin_px([CH.px(*X), CH.px(*Y)], POS, 5, z=9), ponto_px(*CH.px(*X), POS, 9, z=10), ponto_px(*CH.px(*Y), POS, 9, z=10))
        reg = regua_em(cam[0])
        reg.add_updater(lambda m: m.become(regua_em(posX(u.get_value()))))
        bx, y0, sc_ = 975, 740, 60
        Yv = lambda v: y0 - v * sc_

        def barras():
            X = posX(u.get_value())
            Y = (X[0] - .12, X[1] - .12)
            fX, fY = f_dens(*X), f_dens(*Y)
            top = max(fX, fY)
            return VGroup(ret_px(bx - 46, Yv(top), bx + 46, Yv(top - 1), fill=MEN, fop=0.18, stroke=MEN, wpx=2, z=4),
                          ret_px(bx - 34, Yv(fX), bx - 10, y0, fill=CI, z=5), ret_px(bx + 10, Yv(fY), bx + 34, y0, fill=CI, z=5))
        bars = barras()
        self.gat("quaisquer dois pontos")
        self.play(FadeIn(reg), FadeIn(bars), run_time=0.6)
        bars.add_updater(lambda m: m.become(barras()))
        lfX = TC(r"\f(\XX)", 0, 0, 24, "r")
        lfY = TC(r"\f(\YY)", 0, 0, 24, "l")
        le = TC(r"\eps", 0, 0, 28, "c")

        def poe_rot(m, qual):
            X = posX(u.get_value())
            Y = (X[0] - .12, X[1] - .12)
            fX, fY = f_dens(*X), f_dens(*Y)
            if qual == "X":
                p = PX(bx - 52, Yv(fX) + 14)
                m.shift(p - np.array([m.get_right()[0], m.get_center()[1], 0]))
            elif qual == "Y":
                p = PX(bx + 52, Yv(fY) + 14)
                m.shift(p - np.array([m.get_left()[0], m.get_center()[1], 0]))
            else:
                m.shift(PX(bx, Yv(max(fX, fY)) - 24) - m.get_center())
        for m, q_ in ((lfX, "X"), (lfY, "Y"), (le, "e")):
            poe_rot(m, q_)
        self.pena(lfX, lfY, le, rt=1.0)
        for m, q_ in ((lfX, "X"), (lfY, "Y"), (le, "e")):
            m.add_updater(lambda mm, q_=q_: poe_rot(mm, q_))
        self.gat("a menos de delta")
        e2 = TC(r"\|\XX-\YY\|<\del\ \Rightarrow\ |\f(\XX)-\f(\YY)|<\eps", 1120, 420, 38)
        self.pena(e2)
        self.gat("as barras duplas")
        self.sublinha(VGroup(*e2[0][0:5]), 1.2)
        nn = leg("‖ ‖: NORMA, A DISTÂNCIA", 1124, 490, GEO, "left", 24)
        self.pena(nn)
        self.gat("o mesmo delta serve")
        ghosts = []
        for k, t1 in enumerate((L1 / (L1 + L2), 1.0)):
            self.play(u.animate.set_value(t1), run_time=2.6 if k == 0 else 3.2, rate_func=smooth)
            if k == 0:
                X0, Y0 = cam[0], (cam[0][0] - .12, cam[0][1] - .12)
                X1, Y1 = cam[1], (cam[1][0] - .12, cam[1][1] - .12)
                gh = VGroup(*[VGroup(lin_px([CH.px(*X), CH.px(*Y)], POS, 3, dash=(6, 6), z=8), ponto_px(*CH.px(*X), POS, 6, z=8), ponto_px(*CH.px(*Y), POS, 6, z=8))
                              for X, Y in ((X0, Y0), (X1, Y1))])
                self.play(FadeIn(gh), run_time=0.4)
                ghosts.append(gh)
                o1 = T("O MESMO δ SERVE EM TODO LUGAR", 1120, 590, 32)
                o2 = leg("CONTINUIDADE UNIFORME (HEINE-CANTOR)", 1124, 640, CI, "left", 24)
                self.pena(o1)
                self.pena(o2)
        reg.clear_updaters()
        bars.clear_updaters()
        for m in (lfX, lfY, le):
            m.clear_updaters()
        lX = TP(r"\XX", *CH.px(2.03, 2.03), 28)
        lY = TP(r"\YY", *CH.px(1.68, 1.66), 28)
        ld = TP(r"\del", *CH.px(1.68, 1.95), 28)
        self.pena(lX, lY, ld, rt=0.9)
        self.gat("com épsilon igual a um")
        ed = TC(r"\eps=1\ \ \to\ \ \del=0{,}17", 1120, 740, 40)
        self.escreve(ed, voos=[(le, [0]), (ld.f, [4])], passo=0.05)
        self.gat("é esse delta que")
        cc = leg("O CANTO DE CIMA ESCOLHE O δ", 1124, 800, GEO, "left", 24)
        self.pena(cc)
        self.marca("20")

        # ── B6-3 · por que fechado e limitado? (alvo 21) ──────────────────────────────────────────────
        self.an("B6-3")
        sai = [k0, e1, e2, nn, o1, o2, ed, cc, reg, bars, lfX, lfY, le, lX, lY, ld, *ghosts, sx, sy, lxx, lyy]
        self.play(*[FadeOut(m) for m in sai], run_time=0.5)
        self.remove(*sai)
        self.gat("olha esta função")
        sen = img_chapa(arr_sen1x())
        bd2 = VGroup(lin_px([CH.px(2, 0), CH.px(2, 2)], GEO, 3), lin_px([CH.px(0, 0), CH.px(2, 0)], GEO, 3), lin_px([CH.px(0, 2), CH.px(2, 2)], GEO, 3))
        esq = lin_px([CH.px(0, 0), CH.px(0, 2)], BR, 3, dash=(10, 10), z=6)
        self.play(FadeIn(sen), FadeOut(mapa), FadeOut(bd), FadeIn(bd2), run_time=1.0)
        self.remove(mapa, bd)
        fs1 = TC(r"\f(\X,\Y)=\sen\dfrac{1}{\X}", 1120, 280, 42)
        self.pena(fs1)
        self.gat("numa faixa sem a borda")
        self.play(Create(esq), run_time=0.6)
        bl = leg("BORDA DA ESQUERDA FICA FORA", *CH.px(0, 2.12), BR, "left", 22)
        self.pena(bl)
        self.gat("ela oscila cada vez")
        Pj = CH.px(LUPA_A0, 1.1)
        jan = lin_px([Pj, (Pj[0] + (LUPA_A1 - LUPA_A0) * 240, Pj[1]), (Pj[0] + (LUPA_A1 - LUPA_A0) * 240, Pj[1] + 96), (Pj[0], Pj[1] + 96), Pj], GEO, 1.5, dash=(5, 5), z=8)
        pl = painel(880, 300, 180, 420)
        lup = img_px(arr_lupa(), 890, 310, 160, 400, z=3)
        zm = leg("ZOOM", 970, 750, GEO, "center", 20)
        self.play(Create(jan), Create(pl), FadeIn(lup), run_time=0.7)
        self.pena(zm)
        p1 = leg("PERTO DA BORDA QUE FALTA:", 1124, 380, GEO, "left", 26)
        p2 = leg("ONDULA CADA VEZ MAIS RÁPIDO", 1124, 420, GEO, "left", 26)
        self.pena(p1, p2, lag=0.5)
        self.gat("dá para achar dois")

        def par(k):
            a1, a2 = 1 / (PI / 2 + 2 * PI * k), 1 / (3 * PI / 2 + 2 * PI * k)
            q1, q2 = (lx(a1), 510), (lx(a2), 510)
            return VGroup(lin_px([q1, q2], POS, 4, z=9), ponto_px(*q1, POS, 8, z=10), ponto_px(*q2, POS, 8, z=10)), q1, q2
        rg, q1, q2 = par(1)
        self.play(FadeIn(rg), run_time=0.5)
        r1 = TP(r"\Ci{+1}", q1[0], 470, 24)
        r2 = TP(r"\Ci{-1}", q2[0], 550, 24)
        self.pena(r1, r2, rt=0.8)
        self.gat("a diferença continua dois")
        for k in (2,):
            rg2, q1, q2 = par(k)
            r1n, r2n = TP(r"\Ci{+1}", q1[0], 470, 24, caneta=False), TP(r"\Ci{-1}", q2[0], 550, 24, caneta=False)
            self.play(Transform(rg, rg2), Transform(r1, r1n), Transform(r2, r2n), run_time=0.6)
        dd = TC(r"\text{distância}\to 0,\quad\text{diferença}=2", 1120, 510, 36)
        self.pena(dd)
        self.gat("e nenhum delta serve")
        nd = T("NENHUM δ SERVE", 1120, 610, 40, cor=AL)
        self.pena(nd)
        self.gat("numa região fechada e limitada isso")
        self.sublinha(bl, 1.2)
        self.gat("haveria pares de pontos")
        rg2, q1, q2 = par(3)
        r1n, r2n = TP(r"\Ci{+1}", q1[0], 470, 24, caneta=False), TP(r"\Ci{-1}", q2[0], 550, 24, caneta=False)
        self.play(Transform(rg, rg2), Transform(r1, r1n), Transform(r2, r2n), run_time=0.8)
        self.gat("esses pares se aproximam")
        a1_ = leg("FECHADA E LIMITADA: OS PARES", 1124, 720, GEO, "left", 24)
        a2_ = leg("SE ACUMULAM NUM PONTO DA CHAPA", 1124, 760, GEO, "left", 24)
        self.pena(a1_, a2_, lag=0.8)
        self.marca("21")
        self.sai_fim()
