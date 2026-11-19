"""yt_0031 · B1 · piso, teto e tampas (alvos 04 a 07). 3D: b13 (prédio por baixo + tampas, x² + y², n = 4)."""
from v31 import *


class PB1(B31):
    ANTES = "PISO, TETO E TAMPAS"          # v2 (G2): a linha 2 do canto já está na tela no 1º quadro do bloco
    def corpo(self):
        # ── B1-1 · piso e teto (alvo 04) ─────────────────────────────────────────────────────────────
        self.an("B1-1")
        mapa = img_chapa(arr_dens(64))
        gr4 = VGroup(*[lin_px([CH.px(a, 0), CH.px(a, 2)], BG_, 3, z=3) for a in (.5, 1, 1.5)],
                     *[lin_px([CH.px(0, b), CH.px(2, b)], BG_, 3, z=3) for b in (.5, 1, 1.5)])
        bd = borda_ch(CH, GEO, 3)
        sx, sy, lx, ly = eixos_chapa()
        self.grade = papel(CH).set_z_index(-10)
        self.play(FadeIn(self.grade), FadeIn(mapa), Create(bd), FadeIn(sx), FadeIn(sy), LaggedStart(*[Create(l) for l in gr4], lag_ratio=0.12), run_time=1.1)
        self.pena(lx, ly, rt=0.5)
        self.gat("pega um retanguinho")
        esc = VGroup(*[ret_px(*CH.px(i / 2, j / 2 + .5), *CH.px(i / 2 + .5, j / 2), fill="#0F0C26", fop=0.55, z=2)
                       for i in range(4) for j in range(4) if not (i == 3 and j == 3)])
        cel = ret_px(*CH.px(1.5, 2), *CH.px(2, 1.5), stroke=BR, wpx=5, z=8)
        self.play(FadeIn(esc), Create(cel), run_time=0.7)
        rij = TP(r"\Rij", *CH.px(1.75, 1.75), 32)
        self.pena(rij)
        # barrinha dos valores
        bx, y0, sc_ = 965, 780, 60
        Yv = lambda v: y0 - v * sc_
        eixo = VGroup(lin_px([(bx - 40, Yv(1.2)), (bx - 40, Yv(8.6))], GEO, 2),
                      *[lin_px([(bx - 46, Yv(v)), (bx - 34, Yv(v))], GEO, 2) for v in (2, 4, 6, 8)])
        nums = [leg(str(v), bx - 56, Yv(v) + 8, GEO, "right", 20) for v in (2, 4, 6, 8)]
        vf = leg("VALORES DE f", bx - 40, Yv(8.6) - 18, CI, "center", 22)
        barra = ret_px(bx - 8, Yv(8), bx + 8, Yv(4.5), fill=CI, z=6)
        self.gat("a função assume vários")
        self.play(Create(eixo), run_time=0.6)
        self.pena(vf, *nums, extra=[GrowFromEdge(barra, DOWN)], rt=1.2)
        self.gat("agora procura o maior")
        tr_m = ret_px(bx - 26, Yv(4.5) - 3, bx + 26, Yv(4.5) + 3, fill=AZC, z=7)
        tr_M = ret_px(bx - 26, Yv(8) - 3, bx + 26, Yv(8) + 3, fill=CORAL, z=7)
        lm = TC(r"\mij", bx + 34, Yv(4.5), 32)
        lM = TC(r"\Mij", bx + 34, Yv(8), 32)
        self.play(GrowFromCenter(tr_m), run_time=0.4)
        self.pena(lm)
        self.gat("esse é o piso da")
        f1 = TC(r"\mij:\ \text{piso de }\f\text{ em }\Rij", 1120, 300, 40)
        self.escreve(f1, voos=[(lm, [0, 1, 2])])
        l1 = leg("O MAIOR NÚMERO ABAIXO DE TODOS", 1124, 360, AZC, "left", 24)
        self.pena(l1)
        self.gat("o teto é o contrário")
        self.play(GrowFromCenter(tr_M), run_time=0.4)
        self.pena(lM)
        f2 = TC(r"\Mij:\ \text{teto de }\f\text{ em }\Rij", 1120, 500, 40)
        self.escreve(f2, voos=[(lM, [0, 1, 2])])
        l2 = leg("O MENOR NÚMERO ACIMA DE TODOS", 1124, 560, CORAL, "left", 24)
        self.pena(l2)
        i1 = leg("ÍNFIMO", 1124, 400, GEO, "left", 24)
        i2 = leg("SUPREMO", 1124, 600, GEO, "left", 24)
        self.gat("ínfimo e supremo")
        self.pena(i1)
        self.gat("e supremo nos")
        self.pena(i2)
        # v2 (G8): sem pontos extras; o piso e o teto acendem na barrinha quando a voz diz "o menor" e "o maior"
        self.gat("eles são o menor")
        self.acende_txt(tr_m, BR)
        self.gat("e o maior valor")
        self.acende_txt(tr_M, BR)
        self.gat("por isso o nome certo")
        self.sublinha(i1, 0.6)
        self.sublinha(i2, 0.6)
        self.gat("e a gente trabalha")
        fl = T("f LIMITADA: PISO E TETO EXISTEM", 1120, 720, 28)
        self.pena(fl)
        self.marca("04")

        # ── B1-2 · as duas somas (alvo 05): pouso de entrada no b13 ─────────────────────────────────
        self.an("B1-2")
        col = [f1, f2, l1, l2, i1, i2, fl, lm, lM, tr_m, tr_M, barra, eixo, vf, *nums, rij, esc, cel]
        self.play(*[FadeOut(m) for m in col], run_time=0.5)
        self.remove(*col)
        pal = Palco3D("b13", self, CAM_PREDIO31, chao=1.0, cresce=0.0, tampas=0.0)
        entra3d(self, pal, saem=[mapa, gr4, bd, sx, sy, lx, ly], rt_cam=2.0, junto_cam=pal.anim(2.0, chao=0.0))
        ex = pal.prende(TC(r"\X", 0, 0, 30, "c"), "ex")
        ez = pal.prende(TC(r"\Ci{z}", 0, 0, 30, "c"), "ez")
        self.play(*pal.anim(1.6, cresce=1.0), run_time=1.6)
        self.pena(ex, ez)
        self.gat("essa é a soma por baixo")
        s1 = TC(r"\sP=\sum_i\sum_j \mij\,\dxi\,\dyj", 1120, 260, 40)
        self.pena(s1)
        b1 = leg("SOMA POR BAIXO", 1124, 322, AZC, "left", 24)
        self.pena(b1)
        self.gat("faz o mesmo com o teto")
        self.play(*pal.anim(1.4, tampas=1.0), run_time=1.4)
        ta = pal.prende(leg("TAMPAS", 0, 0, CORAL, "left", 26), "tampaAlto", dx=40 + 45, dy=-10 - 9)
        s2 = TC(r"\SP=\sum_i\sum_j \Mij\,\dxi\,\dyj", 1120, 430, 40)
        self.pena(ta)
        self.pena(s2)
        b2 = leg("SOMA POR CIMA", 1124, 492, CORAL, "left", 24)
        self.pena(b2)
        # v2: o ponto X_ij desliza na célula do canto (i = 3, j = 0) e a marca dele anda na barrinha, sempre entre o piso e o teto
        self.gat("qualquer ponto que você")
        ZS, lo, hi = .25, f_dens(1.5, 0), f_dens(2, .5)
        BX, Yb = 1010, lambda v: 560 - (v - lo) * 55
        bar = VGroup(lin_px([(BX, Yb(lo) + 12), (BX, Yb(hi) - 12)], GEO, 2), ret_px(BX - 6, Yb(hi), BX + 6, Yb(lo), fill=CI, z=6),
                     ret_px(BX - 18, Yb(lo) - 3, BX + 18, Yb(lo) + 3, fill=AZC, z=7), ret_px(BX - 18, Yb(hi) - 3, BX + 18, Yb(hi) + 3, fill=CORAL, z=7))
        bm = TC(r"\mij", BX + 26, Yb(lo), 34, "l")
        bM = TC(r"\Mij", BX + 26, Yb(hi), 34, "l")
        posis = [(1.6, .1), (1.9, .4), (1.75, .25)]
        u = ValueTracker(0.0)

        def xy_u():
            t = u.get_value()
            k = min(int(t), 1)
            a_, b_ = posis[k], posis[k + 1]
            w = t - k
            return (a_[0] + (b_[0] - a_[0]) * w, a_[1] + (b_[1] - a_[1]) * w)

        def ponto3():
            x_, y_ = xy_u()
            return proj3d(pal.cam(), (x_, 0, ZS * f_dens(x_, y_)))
        pX = ponto_px(*ponto3(), POS, 8, z=12)
        mk = ret_px(BX - 14, Yb(f_dens(*posis[0])) - 2, BX + 14, Yb(f_dens(*posis[0])) + 2, fill=POS, z=8)
        pX.add_updater(lambda m: m.move_to(PX(*ponto3())))
        mk.add_updater(lambda m: m.move_to(PX(BX, Yb(f_dens(*xy_u())))))
        self.play(Create(bar), FadeIn(pX, scale=0.5), FadeIn(mk), run_time=0.6)
        self.pena(bm, bM, rt=0.6)
        self.play(u.animate.set_value(1.0), run_time=1.4)
        self.gat("dá um valor entre")
        self.play(u.animate.set_value(2.0), run_time=1.4)
        pX.clear_updaters()
        mk.clear_updaters()
        self.gat("então qualquer soma")
        self.acende_txt(s1.f if hasattr(s1, "f") else s1, AZC)
        self.acende_txt(s2, CORAL)
        # v2: a desigualdade por partes, na ordem do "Lê-se": s(P) e S(P) voam das linhas de cima, f(X_ij) voa do ponto, o resto a caneta
        s3 = TC(r"\sP\ \le\ \sum_i\sum_j \f(\Xij)\,\dxi\,\dyj\ \le\ \SP", 1120, 640, 38)
        assert len(s3[0]) == 26, len(s3[0])
        g3 = list(s3[0])
        s3._em_caneta = True
        partes = []

        def parte(idx, src=None):
            alvo = VGroup(*[g3[i] for i in idx])
            alvo._tex = s3._tex + f"[{idx[0]}:{idx[-1] + 1}]"
            if src is not None:
                self.play(TransformFromCopy(src, alvo, path_arc=-0.5), run_time=0.7)
            else:
                self.play(caneta(alvo, ritmo=CANETA_P / 0.30))
            partes.append(alvo)
        self.gat("lê se esse")
        parte([0, 1, 2, 3], VGroup(*s1[0][0:4]))
        self.gat("é menor ou igual à")
        parte([4])
        self.gat("à soma de riemann")
        parte([5, 6, 7, 8])
        parte([9, 10, 11, 12, 13, 14], pX)
        parte(list(range(15, 21)))
        self.gat("que é menor ou igual")
        parte([21])
        self.gat("maiúsculo de p todas")
        parte([22, 23, 24, 25], VGroup(*s2[0][0:4]))
        self.remove(*partes)
        s3._em_caneta, s3._esc = False, True
        self.add(s3)
        self.origem(s3, "voo + caneta (por partes)", "s(P) e S(P) das linhas de cima; f(X_ij) do ponto")
        self.gat("todas as aproximações")
        self.play(FadeOut(pX), FadeOut(mk), FadeOut(bar), FadeOut(bm), FadeOut(bM), run_time=0.4)
        self.remove(pX, mk, bar, bm, bM)
        b3 = leg("TODA SOMA DE RIEMANN FICA NO MEIO", 1124, 710, GEO, "left", 24)
        self.pena(b3)
        self.marca("05")

        # ── B1-3 · o volume das tampas (alvo 06) ──────────────────────────────────────────────────────
        self.an("B1-3")
        ta.clear_updaters()
        self.play(FadeOut(s3), FadeOut(b3), FadeOut(b1), FadeOut(b2), FadeOut(ta), run_time=0.4)
        self.remove(s3, b3, b1, b2, ta)
        dif = TC(r"\SP-\sP=\sum_i\sum_j(\Mij-\mij)\,\dxi\,\dyj", 1120, 300, 38)
        dph = TC(r"\SP-\sP=\sum_i\sum_j(\phantom{\Mij-\mij})\,\dxi\,\dyj", 1120, 300, 38)
        assert len(s1[0]) == 18 and len(s2[0]) == 18 and len(dif[0]) == 29 and len(dph[0]) == 22, (len(s1[0]), len(s2[0]), len(dif[0]), len(dph[0]))
        r = lambda a, b: list(range(a, b))
        # mapa 1 (§4): as duas somas viram a diferença; Σ, Δ e os lados casam; o "−" e os parênteses a caneta; M_ij e m_ij de cima saem
        AB = CombineTex(s1, s2)
        AB._tex = "s(P)=ΣΣ m_ij ΔxΔy  +  S(P)=ΣΣ M_ij ΔxΔy"
        self.tbgm(AB, dph, [(r(18, 22), r(0, 4)), (r(0, 4), r(5, 9)), ([22], [9]), (r(23, 27), r(10, 14)), (r(5, 9), r(10, 14)),
                            (r(30, 33), r(16, 19)), (r(12, 15), r(16, 19)), (r(33, 36), r(19, 22)), (r(15, 18), r(19, 22))], rt=1.6, rotulo="mapa 1 (B1-3)")
        self.remove(s1, s2)
        self.add(dph)
        # o teto menos o piso: a cota da tampa do canto, e o M_ij − m_ij VOA da cota para a fórmula
        self.gat("sobra o teto menos")
        cota = VGroup()

        def poe_cota(m):
            a, b = pal.pt("tampaBase"), pal.pt("tampaAlto")
            m.become(VGroup(lin_px([(a[0] + 28, a[1]), (b[0] + 28, b[1])], CORAL, 3, z=12),
                            lin_px([(a[0] + 20, a[1]), (a[0] + 36, a[1])], CORAL, 3, z=12),
                            lin_px([(b[0] + 20, b[1]), (b[0] + 36, b[1])], CORAL, 3, z=12)))
        poe_cota(cota)
        a, b = pal.pt("tampaBase"), pal.pt("tampaAlto")
        lc = TP(r"\Mij-\mij", (a[0] + b[0]) / 2 + 44, (a[1] + b[1]) / 2, 34, "l")
        self.play(Create(cota), run_time=0.5)
        self.pena(lc)
        gm = VGroup(*[dif[0][i] for i in range(15, 22)])
        dif._em_caneta = True
        self.play(TransformFromCopy(lc.f, gm, path_arc=-0.6), run_time=1.0)
        self.remove(dph, gm)
        dif._em_caneta, dif._esc = False, True
        self.add(dif)
        self.origem(dif, "glyph map + voo", "mapa 1; M_ij − m_ij voou da cota da tampa")
        self.gat("a oscilação da função")
        osc = VGroup(*[dif[0][i] for i in range(15, 22)])
        xa, xb = pxof(osc.get_left())[0], pxof(osc.get_right())[0]
        yb = pxof(dif.get_bottom())[1] + 10
        chave = lin_px([(xa, yb), (xb, yb)], GEO, 2, z=20)
        lo_ = leg("OSCILAÇÃO", (xa + xb) / 2, yb + 35, GEO, "center", 24)
        self.play(Create(chave), run_time=0.4)
        self.pena(lo_)
        self.gat("tirando o prédio azul")
        self.play(*pal.anim(1.5, afunda=1.0), run_time=1.5)
        self.gat("são as tampas coral")
        pal.acende3d(1.4)
        self.gat("cada tampa tem a altura")
        self.acende_txt(lc.f, CORAL)
        self.gat("o volume de todas")
        vt = T("= VOLUME DAS TAMPAS", 1120, 480, 40, cor=CORAL)
        self.pena(vt)
        self.marca("06", agora=True)
        self.gat("porque ela vai conduzir")
        sai = [dif, chave, lo_, vt, lc, cota, ex, ez]
        for m in sai:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        mapa2 = img_chapa(arr_dens(64))
        bd2 = borda_ch(CH, GEO, 3)
        sai3d(self, pal, entram=[mapa2, bd2], rt_cam=2.0, junto_cam=pal.anim(2.0, afunda=0.0, tampas=0.0, cresce=0.0, chao=1.0))
        # ── B1-4 · quando as tampas somem (alvo 07): o funil ─────────────────────────────────────────
        self.an("B1-4")
        pn = painel(80, 190, 900, 740)
        ox, oy, sxx, syy, L = 180, 840, 1350, 34, 32 / 3
        G = lambda d, s: (ox + d * sxx, oy - s * syy)
        ax_h = lin_px([G(0, 0), G(.56, 0)], GEO, 2.5)
        ax_v = lin_px([G(0, 0), G(0, 18)], GEO, 2.5)
        tk = [leg(str(s), ox - 14, G(0, s)[1] + 8, GEO, "right", 24) for s in (5, 10, 15)]
        tk += [leg(str(d).replace(".", ","), G(d, 0)[0], oy + 32, GEO, "center", 24) for d in (.125, .25, .375, .5)]
        vs = leg("VALOR DA SOMA", ox + 12, 226, GEO, "left", 24)
        ml = leg("MAIOR LADO Δ", G(.3, 0)[0], oy + 66, GEO, "center", 24)
        self.play(FadeOut(mapa2), FadeOut(bd2), Create(pn), Create(ax_h), Create(ax_v), run_time=0.8)
        self.remove(mapa2, bd2)
        self.pena(vs, ml, *tk, rt=1.6)
        D = [(.5, 7, 15), (.25, 8.75, 12.75), (.125, 9.6875, 11.6875), (.0625, 10.17, 11.17)]
        self.gat("se a diferença entre")
        pc = [G(d, c) for d, _, c in D] + [G(0, L)]
        pa = [G(d, b) for d, b, _ in D] + [G(0, L)]
        wc, wa = lin_px(pc, CORAL, 4, z=6), lin_px(pa, AZC, 4, z=6)
        dots = VGroup(*[ponto_px(*G(d, s), cor, 8) for d, b, c in D for s, cor in ((b, AZC), (c, CORAL))])
        pL = ponto_px(*G(0, L), BR, 9, z=9)
        lL = TP(r"L", G(0, L)[0] + 24, G(0, L)[1] - 30, 30)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.1), run_time=0.8)
        self.play(Create(wc), Create(wa), run_time=2.0, rate_func=linear)
        self.play(FadeIn(pL, scale=0.5), run_time=0.3)
        self.pena(lL)
        sd = leg("S(P) DESCE", G(.5, 15)[0] - 10, G(.5, 15)[1] - 24, CORAL, "right", 24)
        ss = leg("s(P) SOBE", G(.5, 7)[0] - 10, G(.5, 7)[1] + 40, AZC, "right", 24)
        self.gat("só deixando a grade")
        self.pena(sd, ss, lag=0.4)
        c4 = T("f É INTEGRÁVEL", 1060, 630, 44, cor=CI)
        self.gat("então a função é integrável")
        self.pena(c4)
        self.gat("em épsilon e delta")
        c1 = TC(r"\forall\eps>0\ \ \exists\del>0:", 1060, 330, 44)
        c2 = TC(r"\Delta<\del\ \Rightarrow\ \SP-\sP<\eps", 1060, 430, 44)
        self.pena(c1)
        self.gat("se o maior lado")
        self.pena(c2)
        c3 = TC(r"\Downarrow", 1200, 530, 44, "c")
        self.pena(c3)
        self.gat("porque toda soma")
        lar = VGroup(*[ponto_px(*G(d, b + (c - b) * k / 4 + (.3 if k == 2 else 0)), POS, 6) for d, b, c in D for k in (1, 2, 3)])
        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in lar], lag_ratio=0.08), run_time=1.4)
        # v2: as duas paredes se aproximam: o vão entre elas (traço GEO) corre de Δ = 0,5 até L e fecha
        self.gat("quando as paredes se")
        dv = ValueTracker(.5)

        def parede(pts_, d):
            xs = [p[0] for p in D] + [0]
            ys = [p[1] if pts_ == "a" else p[2] for p in D] + [L]
            return float(np.interp(d, xs[::-1], ys[::-1]))

        def vao():
            d = dv.get_value()
            return lin_px([G(d, parede("a", d)), G(d, parede("c", d))], BR, 3, z=8)
        gap = vao()
        gap.add_updater(lambda m: m.become(vao()))
        self.play(FadeIn(gap), run_time=0.2)
        self.play(dv.animate.set_value(0.0), run_time=2.2, rate_func=smooth)
        gap.clear_updaters()
        self.play(FadeOut(gap), run_time=0.2)
        self.remove(gap)
        self.gat("todas as escolhas são")
        cop = lar.copy()
        self.play(*[p.animate.move_to(PX(*G(0, L))).set_opacity(0) for p in cop], run_time=1.6)
        self.remove(cop)
        self.gat("persegue uma coisa")
        c5 = leg("TAMPAS SOMEM ⇒ INTEGRAL EXISTE", 1064, 720, GEO, "left", 28)
        self.pena(c5)
        self.gat("fazer o volume das tampas")
        self.acende_txt(c5, CORAL)
        self.marca("07")
        self.sai_fim()
