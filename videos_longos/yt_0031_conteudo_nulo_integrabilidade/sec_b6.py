"""yt_0031 · B6 · continuidade uniforme (alvos 20 e 21; o B6-1 reaproveita o 3D b13t do alvo 06).
v2: o bloco nasce da cena 3D do B5-2 (b52 → b13 sem eixos); barras f(X), f(Y) do alvo 20 v2; na lupa do sen(1/x) quem muda é o ZOOM
(tabela do handoff v2 §3), a régua fica com ~60 px; palco e lupa com supersample (8 amostras por coluna)."""
from v31 import *
from sec_b5 import miniatura_muro

JANELAS = [(0.06, 0.16), (0.05, 0.085), (0.035, 0.06)]       # zoom 1, 2, 3 (m)
SS = 8                                                     # amostras por coluna de pixel


def _rampa(v):
    return hx(RAMP0) * (1 - v[:, None]) + hx(CI) * v[:, None]


def arr_sen1x(L=480):
    xs = (np.arange(L * SS) + 0.5) / (L * SS) * 2
    v = ((np.sin(1 / xs) + 1) / 2).reshape(L, SS).mean(1)
    return np.repeat(_rampa(v)[None, :, :], L, axis=0)


def arr_lupa(a0, a1, w=160, h=400):
    xs = a0 + (np.arange(w * SS) + 0.5) / (w * SS) * (a1 - a0)
    v = ((np.sin(1 / xs) + 1) / 2).reshape(w, SS).mean(1)
    return np.repeat(_rampa(v)[None, :, :], h, axis=0)


class PB6(B31):
    ANTES = "CONTINUIDADE UNIFORME"          # v2 (G2): a linha 2 do canto já está na tela no 1º quadro do bloco

    def corpo(self):
        # ── B6-1 · um δ para a chapa inteira: nasce da cena 3D do B5-2 ───────────────────────────────
        self.an("B6-1")
        p52 = Palco3D("b52", self, CAM_BAIXO, s=1.0, cresce=1.0, muro=1.0)
        self.add(p52.fundo)
        pal = Palco3D("b13", self, CAM_PREDIO31, eixos=False, s=1.0, cresce=1.0, afunda=1.0, tampas=1.0)
        pal.fundo.op.set_value(0.0)
        self.add(pal.fundo)
        self.play(p52.fundo.op.animate.set_value(0.0), pal.fundo.op.animate.set_value(1.0), run_time=0.8)
        p52.fundo.clear_updaters()
        self.remove(p52.fundo, *p52.tr.values(), p52.acende)
        self._palcos.remove(p52)
        self.gat("na chapa de dois metais")
        pn = painel(1120, 600, 640, 330)
        mini = miniatura_muro()
        cm = leg("A CHAPA DE DOIS METAIS", 1440, 970, GEO, "center", 24)
        self.play(Create(pn), FadeIn(mini), run_time=0.8)
        self.pena(cm)
        self.gat("e as tampas eram zero")
        self.sublinha(cm, 1.0)
        self.gat("numa densidade que varia")
        pal.acende3d(1.2)
        self.gat("quase toda célula")
        ta = pal.prende(leg("TAMPAS", 0, 0, CORAL, "left", 26), "tampaAlto", dx=97, dy=-19)      # v3: ≥ 16 px da aresta
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
        sai = [pn, mini, cm, ta, q1, q2]
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

        # ── B6-2 · continuidade uniforme (alvo 20, v2) ─────────────────────────────────────────────────
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
        # v2 (alvo 20): barras em x = 990, base em y = 640 (140 px acima do eixo), 1 unidade de f = 38 px; faixa ε = 38 px
        bx, y0, sc_ = 990, 640, 38
        Yv = lambda v: y0 - v * sc_
        base_b = lin_px([(bx - 46, y0), (bx + 46, y0)], GEO, 2, z=5)

        def barras():
            X = posX(u.get_value())
            Y = (X[0] - .12, X[1] - .12)
            fX, fY = f_dens(*X), f_dens(*Y)
            top = max(fX, fY)
            return VGroup(ret_px(bx - 46, Yv(top), bx + 46, Yv(top - 1), fill=MEN, fop=0.18, stroke=MEN, wpx=2, z=4),
                          ret_px(bx - 34, Yv(fX), bx - 10, y0, fill=CI, z=5), ret_px(bx + 10, Yv(fY), bx + 34, y0, fill=CI, z=5))
        bars = barras()
        self.gat("quaisquer dois pontos")
        self.play(FadeIn(reg), FadeIn(bars), Create(base_b), run_time=0.6)
        bars.add_updater(lambda m: m.become(barras()))
        lfX = TC(r"\f(\XX)", 0, 0, 24, "r")
        lfY = TC(r"\f(\YY)", 0, 0, 24, "l")
        le = TC(r"\eps", 0, 0, 30, "c")          # final F8: ε sobre as barras a 30 px

        def poe_rot(m, qual):
            X = posX(u.get_value())
            Y = (X[0] - .12, X[1] - .12)
            fX, fY = f_dens(*X), f_dens(*Y)
            if qual == "X":
                p = PX(bx - 62, Yv(fX) + 16)
                m.shift(p - np.array([m.get_right()[0], m.get_center()[1], 0]))
            elif qual == "Y":
                p = PX(bx + 54, Yv(fY) + 16)
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
        lX = TP(r"\XX", CH.px(2.08, 2.06)[0] + 12, CH.px(2.08, 2.06)[1] - 12, 28)   # final F8: 12 px acima e à direita (folga ≥ 16 px)
        lY = TP(r"\YY", *CH.px(1.66, 1.62), 28)
        ld = TP(r"\del", *CH.px(1.70, 1.90), 28)
        self.pena(lX, lY, ld, rt=0.9)
        self.gat("com épsilon igual a um")
        ed = TC(r"\eps=1\ \ \to\ \ \del=0{,}17", 1120, 740, 40)
        # final §7: ε desce por dentro das barras (x = 990), passa por baixo da legenda (y = 700) e entra na linha 740; δ sai pela borda da
        # chapa (x = 855), passa por baixo da linha e do rótulo x do eixo (y = 835) e sobe ao lugar — nenhum voo cruza texto
        xe, xd = pxof(ed[0][0].get_center())[0], pxof(ed[0][4].get_center())[0]
        ye0, yd0 = pxof(le.get_center())[1], pxof(ld.f.get_center())[1]
        self.escreve(ed, voos=[(le, [0], [(990, ye0), (990, 700), (xe, 700)]), (ld.f, [4], [(855, yd0), (855, 835), (xd, 835)])], passo=0.05, rt_voo=1.2)
        self.gat("é esse delta que")
        cc = leg("O CANTO DE CIMA ESCOLHE O δ", 1124, 800, GEO, "left", 24)
        self.pena(cc)
        self.marca("20")

        # ── B6-3 · por que fechado e limitado? (alvo 21) ──────────────────────────────────────────────
        self.an("B6-3")
        sai = [k0, e1, e2, nn, o1, o2, ed, cc, reg, bars, base_b, lfX, lfY, le, lX, lY, ld, *ghosts, sx, sy, lxx, lyy]
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
        bl = leg("BORDA DA ESQUERDA FICA FORA", *CH.px(0, 2.12), BR, "left", 24)
        self.pena(bl)

        def janela(k):
            a0, a1 = JANELAS[k]
            P0, P1 = CH.px(a0, 1.1), CH.px(a1, 0.7)
            return lin_px([P0, (P1[0], P0[1]), P1, (P0[0], P1[1]), P0], GEO, 1.5, dash=(5, 5), z=8)

        def lx(a, k):
            a0, a1 = JANELAS[k]
            return 890 + (a - a0) * 160 / (a1 - a0)

        def par(k):
            kk = k + 1
            a1, a2 = 1 / (PI / 2 + 2 * PI * kk), 1 / (3 * PI / 2 + 2 * PI * kk)
            q1, q2 = (lx(a1, k), 510), (lx(a2, k), 510)
            return VGroup(lin_px([q1, q2], POS, 4, z=9), ponto_px(*q1, POS, 8, z=10), ponto_px(*q2, POS, 8, z=10)), q1, q2
        self.gat("ela oscila cada vez")
        jan = janela(0)
        pl = painel(880, 300, 180, 420)
        lup = img_px(arr_lupa(*JANELAS[0]), 890, 310, 160, 400, z=3)
        zm = leg("ZOOM", 970, 750, GEO, "center", 24)
        self.pena(zm, extra=[Create(jan), Create(pl), FadeIn(lup)], rt=0.7)
        p1 = leg("PERTO DA BORDA QUE FALTA:", 1124, 380, GEO, "left", 26)
        p2 = leg("ONDULA CADA VEZ MAIS RÁPIDO", 1124, 420, GEO, "left", 26)
        self.pena(p1, p2, lag=0.3, passo=0.035)
        # zoom 1: o par k = 1 (+1 acima, −1 abaixo) e a distância na coluna
        D = [TC(r"\text{distância}=0{,}036,\quad\text{diferença}=2", 1120, 510, 36),
             TC(r"\text{distância}=0{,}013,\quad\text{diferença}=2", 1120, 510, 36),
             TC(r"\text{distância}=0{,}0065,\quad\text{diferença}=2", 1120, 510, 36),
             TC(r"\text{distância}\to 0,\quad\text{diferença}=2", 1120, 510, 36)]
        npre = nglifos(r"\text{distância}=")
        nd_ = [len(d[0]) for d in D]
        # v3: os três zooms seguem a fala ("dá para achar dois pontos" / "tão próximos" / "quanto você quiser"), 0,3 s cada, a distância troca junto
        self.gat("dá para achar dois")
        rg, q1, q2 = par(0)
        r1 = TP(r"\Ci{+1}", q1[0], 470, 24)
        r2 = TP(r"\Ci{-1}", q2[0], 550, 24)
        self.pena(r1, r2, D[0], extra=[FadeIn(rg)], rt=0.9)

        def zoom(k, fr, A, B, nA, nB):
            self.gat(fr)
            rg2, q1, q2 = par(k)
            r1n, r2n = TP(r"\Ci{+1}", q1[0], 470, 24, caneta=False), TP(r"\Ci{-1}", q2[0], 550, 24, caneta=False)
            lup2 = img_px(arr_lupa(*JANELAS[k]), 890, 310, 160, 400, z=3)
            mapa_ = [(list(range(npre + 3)), list(range(npre + 3))),
                     (list(range(npre + nA, len(A[0]))), list(range(npre + nB, len(B[0]))))]
            self.tbgm(A, B, mapa_, rt=0.3, rotulo=f"distância (zoom {k + 1})", cedo=True,
                      extra=[Transform(rg, rg2), Transform(r1, r1n), Transform(r2, r2n), Transform(lup, lup2), Transform(jan, janela(k))])
        zoom(1, "tão próximos", D[0], D[1], 5, 5)
        zoom(2, "quanto você quiser", D[1], D[2], 5, 6)
        # o +1 e o −1 acendem na sua palavra
        self.gat("um onde o seno vale um")
        self.acende_txt(r1.f, cor=BR, rt=1.0)
        self.gat("outro onde vale menos um")
        self.acende_txt(r2.f, cor=BR, rt=1.0)
        self.gat("a diferença continua dois")
        npre3 = nglifos(r"\text{distância}")
        assert (npre, npre3, nd_) == (11, 10, [29, 29, 30, 25]), (npre, npre3, nd_)
        self.tbgm(D[2], D[3], [(list(range(npre3)), list(range(npre3))), ([npre], [npre3 + 1]), (list(range(npre + 6, nd_[2])), list(range(npre3 + 2, nd_[3])))],
                  rt=0.8, rotulo="distância → 0", cedo=True)
        self.gat("e nenhum delta serve")
        nd = T("NENHUM δ SERVE", 1120, 610, 40, cor=AL)
        self.pena(nd)
        self.marca("21", agora=True, dt=0.6)

        # ── v3 (ALTA 3, alvo 21b): a contradição ganha figura — a chapa fechada e limitada, os pares que se acumulam em P* ──
        self.gat("numa região fechada e limitada isso")
        mapa2 = img_chapa(arr_dens(64))
        esq2 = lin_px([CH.px(0, 0), CH.px(0, 2)], BR, 3, z=6)
        sai = [pl, lup, jan, zm, p1, p2, fs1, D[3], nd, rg, r1, r2, bl]
        self.play(*[FadeOut(m) for m in sai], FadeOut(sen), FadeIn(mapa2), FadeOut(esq), run_time=0.5)
        self.remove(*sai, sen, esq)
        fl = leg("FECHADA E LIMITADA", *CH.px(0, 2.12), BR, "left", 24)
        self.pena(fl, extra=[Create(esq2)], rt=0.6)
        self.gat("se a continuidade uniforme falhasse")
        c1 = leg("SE NENHUM δ SERVISSE:", 1124, 280, GEO, "left", 28)
        self.pena(c1)
        self.gat("haveria pares de pontos")
        cam_ = lin_px([CH.px(.4, .41), CH.px(.8, .66), CH.px(1.085, .857), CH.px(1.3, 1.0)], mixh(BG_, POS, .7), 2, dash=(6, 6), z=7)
        for m in cam_.get_family():
            m._ok_r5 = True                       # o tracejado do caminho passa entre os pares de propósito
        pares = []
        for (A_, B_), op in (([(.28, .33), (.52, .49)], .6), ([(.74, .62), (.86, .70)], .8), ([(1.06, .84), (1.11, .875)], 1.0)):
            cor = mixh(BG_, POS, op)
            pares.append(VGroup(lin_px([CH.px(*A_), CH.px(*B_)], cor, 3, z=8), ponto_px(*CH.px(*A_), cor, 7, z=9), ponto_px(*CH.px(*B_), cor, 7, z=9)))
        c2 = T("PARES CADA VEZ MAIS PRÓXIMOS", 1120, 350, 32)
        self.pena(c2, extra=[Create(cam_), LaggedStart(*[FadeIn(pp, scale=0.6) for pp in pares], lag_ratio=0.45)], rt=1.6)
        self.gat("com valores sempre longe")
        c3 = T("VALORES SEMPRE LONGE", 1120, 410, 32)
        self.pena(c3)
        self.gat("uma sequência que se aproxima")
        qx, qy = CH.px(1.3, 1.0)
        anel = VGroup(circ_px(qx, qy, 24, BR, 3, z=10), ponto_px(qx, qy, BR, 5, z=11))
        lp = TP(r"P^{*}", qx + 34, qy + 30, 30, "l")
        self.play(Create(anel[0]), FadeIn(anel[1], scale=0.5), run_time=0.5)
        self.pena(lp)
        c4 = leg("NA CHAPA FECHADA E LIMITADA,", 1124, 510, GEO, "left", 28)
        c5 = T("OS PARES SE ACUMULAM EM P*", 1120, 570, 32)
        self.pena(c4, c5, lag=0.5)
        self.gat("e ali a função seria descontínua")
        dq = TPt("DESCONTÍNUA EM P*?", qx - 10, qy - 52, 28, CORAL, "center")
        c6 = leg("MAS f É CONTÍNUA EM P*", 1124, 670, CI, "left", 28)
        self.pena(dq, c6, lag=0.4)
        self.gat("contradição")
        c7 = T("CONTRADIÇÃO", 1120, 790, 48, cor=AL)
        self.pena(c7, rt=0.35)
        self.marca("21b", agora=True, dt=0.1)
        # final F1: o quadro 21b fica inteiro até o fim da frase nova ("Então, numa região fechada e limitada, toda função contínua é
        # uniformemente contínua."); em "uniformemente contínua" a borda da chapa acende 1 s (troca de cor e volta). O B6-3 sai depois.
        self.gat("uniformemente contínua")
        bdf = VGroup(borda_ch(CH, CI, 5, z=9), lin_px([CH.px(0, 0), CH.px(0, 2)], CI, 5, z=9))
        for m in bdf.get_family():
            m._ok_r5 = True
        self.play(FadeIn(bdf, rate_func=there_and_back), run_time=1.0)
        self.remove(bdf)
        self.sai_fim()
