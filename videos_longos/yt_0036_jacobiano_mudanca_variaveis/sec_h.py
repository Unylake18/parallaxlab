"""yt_0036 · H · o desafio e a tese (alvos 01 e 02). Layout B direto: o trapézio no papel (direita), as tiras que travam, o expoente que só
enxerga x + y e x − y, a grade nova inclinada, o trapézio que voa para o plano u, v e se endireita, o glyph map 17, o 1/2 ? que ninguém chamou,
as 3 células contra a ÁREA 3/2 e, por último, a célula da grade inclinada com ÁREA ? (a resposta só no B3-3). H2: a célula cresce até o centro."""
from j36 import *

VU, AU = Vw(400, 640, 120), (-2.4, 2.4, -.3, 2.6)
VX, AX = Vw(1180, 330, 175), (-.45, 2.6, -2.45, .55)
VXG = Vw(700, 280, 260)                    # v2 Q01: o papel x, y grande e centrado (centro (1, −1) da caixa do trapézio em (960, 540))
EMENDA_H = 820                             # emenda vertical das duas grades (meio do vão, sob a seta φ)
VH, AH = Vw(520, 560, 300), (-.2, 1.6, -1.3, .6)
TICKS_X = [("x", 1, r"\Am{1}"), ("x", 2, r"\Am{2}"), ("y", -1, r"\Mg{-1}"), ("y", -2, r"\Mg{-2}")]


def desenho_xy(V):
    """Tudo o que mora no papel x, y do H1, construído para a vista V (grande no começo, pequena depois do movimento)."""
    d = monta_plano(V, AX, 2.55, .5, -.4, -2.4, ticks=TICKS_X)
    d["reg"] = poligono(V, TRAP, RB, 1.0, GEO, 3, z=1)
    d["b1"] = lin_px([V.px(0, -1), V.px(1, 0)], CVV, 4, z=4)
    d["b2"] = lin_px([V.px(2, 0), V.px(0, -2)], CVV, 4, z=4)
    d["r1"] = TP(r"\Vc{\X-\Y=1}", V.px(0, -.76)[0] - 14, V.px(0, -.76)[1], 26, "r")
    d["r2"] = rot_v(V, r"\Vc{\X-\Y=2}", (1.25, -.75), 34, 14, 26, "l")
    d["fu"] = familia(V, mapT, range(-3, 4), "u", AX, CU, 1.6, .55)
    d["fv"] = familia(V, mapT, range(-1, 5), "v", AX, CVV, 1.6, .55)
    d["lfu"] = TP(r"\Uc{\uu}", V.px(2.45, -2.45)[0], V.px(2.45, -2.45)[1] + 26, 30, "c")
    d["lfv"] = TP(r"\Vc{\vv}", V.px(2.6, -1.4)[0] + 17, V.px(2.6, -1.4)[1], 30, "l")
    return d


PECAS_XY = ["sx", "sy", "lx", "ly", "reg", "b1", "b2", "r1", "r2", "fu", "fv", "lfu", "lfv"]
TRAP = [(1, 0), (2, 0), (0, -2), (0, -1)]
TRAP_UV = [(1, 1), (2, 2), (-2, 2), (-1, 1)]
LHS = [("ii", r"\iint_B"), ("e", "e"), ("ex", r"^{\frac{\X+\Y}{\X-\Y}}"), ("dA", r"\,dA")]
INT = [("eq", "="), ("int", r"\int_{\Vc{1}}^{\Vc{2}}\!\int_{\Az{-\vv}}^{\Co{\vv}}"), ("e2", "e"), ("ex2", r"^{\uu/\vv}"), ("dd", r"\,\du\,\dv")]
MEIO = [("half", r"\Lm{\dfrac{1}{2}}"), ("q", r"\Al{?}")]


class PH(J36):
    ANTES = "A INTEGRAL QUE TRAVA"          # final K1: quem chega pelo título não precisa ter visto o vídeo passado

    def corpo(self):
        self.an("H1")
        # ── v2 Q01: o papel x, y GRANDE e centrado, já desenhando no quadro 0 (o papel da tela inteira é o dele) ──
        G = desenho_xy(VXG)
        self.fundo(g=grade_tela(VXG), rt=0)
        # final K1: no quadro 0 o papel e os eixos já estão na tela (cenário); o trapézio nasce de 0,0 a 1,0 s e a caneta escreve a integral
        # de 0,2 a 2,0 s, na 1ª palavra da fala ("Olha esta integral")
        for m in [G["sx"], G["sy"], G["lx"], G["ly"]] + [x for t_ in G["tk"] for x in t_]:
            if m is G["lx"] or m is G["ly"] or any(m is t_[1] for t_ in G["tk"]):
                ja_escrita(m)
            self.add(m)
        reg = G["reg"]
        # a integral na faixa de baixo, centrada; no movimento ela desliza para a posição da linha inteira do v1
        B2 = L(LHS + [INT[0]] + MEIO + INT[1:], 0, 968, 44)
        x0 = 960 - larg(B2) / 2
        B2 = L(LHS + [INT[0]] + MEIO + INT[1:], x0, 968, 44)
        A = L(LHS, 0, 968, 44)
        A.shift(RIGHT * (960 - larg(A) / 2 - esq(A)) / 120)
        self.gat("olha esta integral")
        cr = Create(reg[1])
        cr.rate_func = lambda t: smooth(min(1.0, t * 2.0 / 1.0))        # o trapézio completo em 1,0 s dos 2,0 s do play
        fi = FadeIn(reg[0])
        fi.rate_func = lambda t: smooth(min(1.0, t * 2.0 / 1.0))
        self.pena(A, atraso=0.2, rt=2.0, extra=[cr, fi])
        # ── as duas ordens travam ──
        self.gat("fatia em pé")
        tv = tiraV(VXG, .6, -1.4, -.4, h=.06, cor=E1)
        self.play(FadeIn(tv), run_time=0.6)
        self.gat("do cálculo um trava")                                # final: "ela trava nas duas ordens" vem antes na fala nova
        p1 = placa_txt2("TRAVA", 1500, 205)
        self.pena(p1)
        self.gat("fatia deitada")
        th = tiraH(VXG, -.8, .2, 1.2, h=.06, cor=E2)
        self.play(FadeIn(th), run_time=0.6)
        self.gat("trava também")
        p2 = placa_txt2("TRAVA", 1650, 205)
        lg = leg("EM PÉ E DEITADO", 1590, 262, GEO, "center", 26)
        self.pena(p2, lg, lag=0.2)
        self.play(FadeOut(tv), FadeOut(th), run_time=0.5)
        self.remove(tv, th)
        # final K1: "Os cantos do trapézio" — quatro pontos brancos pequenos, um por canto, um por vez (os tiques dos eixos dão os números)
        self.gat("os cantos do trapézio")
        cantos = [ponto_px(*VXG.px(*q), BR, 6, z=9) for q in TRAP]
        for c_ in cantos:
            self.play(FadeIn(c_, scale=0.5), run_time=0.25)
        self.gat("repara no expoente")
        self.play(*[FadeOut(c_) for c_ in cantos], run_time=0.3)
        self.remove(*cantos)
        # ── o expoente só enxerga a soma e a diferença ──
        num, bar, den = nd(A, "ex")
        self.gat("a soma")
        self.play(*[A[0][i].animate.set_fill(CU) for i in num], run_time=0.6)
        acende(self, (VGroup(*[A[0][i] for i in num]), CU), rt=0.6)
        self.gat("a diferença")
        self.play(*[A[0][i].animate.set_fill(CVV) for i in den], run_time=0.6)
        acende(self, (VGroup(*[A[0][i] for i in den]), CVV), rt=0.6)
        self.gat("e as bordas também")
        self.play(Create(G["b1"]), Create(G["b2"]), run_time=0.8)
        self.pena(G["r1"], G["r2"], lag=0.2)
        # ── a grade nova: x + y = k (laranja), depois x − y = m (verde-água) ──
        self.gat("uma grade nova")
        self.play(LaggedStart(*[Create(m) for m in G["fu"]], lag_ratio=0.12), run_time=1.4)
        self.play(LaggedStart(*[Create(m) for m in G["fv"]], lag_ratio=0.12), run_time=1.4)
        # x + y e x − y do expoente voam para os rótulos u e v das duas famílias
        voos(self, [(VGroup(*[A[0][i] for i in num]).copy(), G["lfu"].f)], rt=0.8)
        voos(self, [(VGroup(*[A[0][i] for i in den]).copy(), G["lfv"].f)], rt=0.8)
        self.add(G["lfu"], G["lfv"])
        self.play(FadeIn(G["lfu"][0]), FadeIn(G["lfv"][0]), run_time=0.3)
        # ── um movimento só: o papel x, y vai para a direita (vista do v1), o plano u, v nasce à esquerda, a integral desliza ──
        self.gat("o trapézio fica reto")
        S = desenho_xy(VX)
        for k in ("lx", "ly", "r1", "r2", "lfu", "lfv"):
            ja_escrita(S[k].f if hasattr(S[k], "f") else S[k])
        for (_, _), t_ in zip(G["tk"], S["tk"]):
            ja_escrita(t_[1])
        dU = monta_plano(VU, AU, 2.45, 2.7, -2.45, -.3, uv=True)
        gu = familia(VU, ID, range(-2, 3), "u", AU, CU, 1.6, .35)
        gv = familia(VU, ID, range(0, 3), "v", AU, CVV, 1.6, .35)
        ps, pl = phi_seta(735, 880, 250)
        # a grade grande anda junto (área maior que a tela: encolhida, ainda cobre tudo) e depois faz crossfade para as duas metades
        ext = papel(VXG, area=((-1400 - VXG.cx) / VXG.u, (3300 - VXG.cx) / VXG.u, (VXG.cy - 2200) / VXG.u, (VXG.cy + 1100) / VXG.u)).set_z_index(-10)
        for x in ext.get_family():
            x._sem_foco = True
        self.fundo(g=ext, rt=0)
        mov = []
        for k in PECAS_XY:
            for x in (G[k].get_family() if k in ("fu", "fv") else [G[k]]):
                x._voando = True
            mov.append(Transform(G[k], S[k]))
        for (a_, b_), (c_, d_) in zip(G["tk"], S["tk"]):
            mov += [Transform(a_, c_), Transform(b_, d_)]
        self.play(*mov, ApplyPointwiseFunction(leva(VXG, VX), ext), A.animate.shift(RIGHT * (x0 - esq(A)) / 120),
                  GrowFromPoint(dU["sx"], VU.P(0, 0)), GrowFromPoint(dU["sy"], VU.P(0, 0)), FadeIn(gu), FadeIn(gv), run_time=1.8)
        for k in PECAS_XY:
            for x in G[k].get_family():
                x._voando = False
        self.fundo(VU, VX, emenda=EMENDA_H, rt=0.35, extra=[Create(ps)])
        self.pena(dU["lx"], dU["ly"], pl, lag=0.1)
        voo_reg = poly_px([VX.px(*p) for p in TRAP], RB, 1.0, z=1)
        alvo_reg = poly_px([VU.px(*p) for p in TRAP_UV], RB, 1.0, z=1)
        self.play(Transform(voo_reg, alvo_reg), run_time=1.8)
        self.remove(voo_reg)
        self.add(alvo_reg)
        ed = VGroup(lin_px([VU.px(-1, 1), VU.px(1, 1)], CVV, 3, z=4), lin_px([VU.px(-2, 2), VU.px(2, 2)], CVV, 3, z=4),
                    lin_px([VU.px(-1, 1), VU.px(-2, 2)], AZC, 4, z=4), lin_px([VU.px(1, 1), VU.px(2, 2)], CORAL, 4, z=4))
        lv1 = rot_v(VU, r"\vv=1", (1.1, 1), 14, 0, 26, "l")
        lv2 = rot_v(VU, r"\vv=2", (2.1, 2.15), 4, 0, 26, "l")
        self.play(LaggedStart(*[Create(m) for m in ed], lag_ratio=0.2), run_time=1.0)
        self.pena(lv1, lv2, lag=0.2)
        # ── glyph map 17: x + y vira u, x − y vira v, dA vira du dv ──
        self.gat("a conta sai rapidinho")
        B = L(LHS + INT, x0, 968, 44)
        ib = B._ix["ex2"]
        passo(self, A, B, [("ii", "ii"), ("e", "e"), ("ex", "ex"), ("dA", "dA")],
              voos=[(VGroup(*[A[0][i] for i in num]).copy(), [ib[0]]), (VGroup(*[A[0][i] for i in den]).copy(), [ib[2]]),
                    (gl(A, "dA").copy(), "dd"), (gl(A, "e").copy(), "e2")], rt=1.2, nota="17 (x+y → u, x−y → v, dA → du dv)")
        for i in num:
            B[0][i].set_fill(CU)
        for i in den:
            B[0][i].set_fill(CVV)
        self.gat("um meio na frente")
        for i in num:
            B2[0][i].set_fill(CU)
        for i in den:
            B2[0][i].set_fill(CVV)
        passo(self, B, B2, [(k, k) for k, _ in LHS + INT], rt=0.8, nota="17b (1/2 ? a caneta)")
        # ── as células: 3 da grade nova contra ÁREA 3/2 do papel ──
        self.gat("três quadradinhos")
        c1 = celula(VU, ID, -1, 0, 1, 2, n=3, wb=2)
        c2 = celula(VU, ID, 0, 1, 1, 2, n=3, wb=2)
        t1 = poligono(VU, [(1, 1), (2, 2), (1, 2)], mixh(BG_, CHAPA, .9), 1.0, MALHA, 2, z=3)
        t2 = poligono(VU, [(-1, 1), (-2, 2), (-1, 2)], mixh(BG_, CHAPA, .9), 1.0, MALHA, 2, z=3)
        entra_cel(self, c1, c2, rt=0.8, extra=[FadeIn(t1[0]), Create(t1[1]), FadeIn(t2[0]), Create(t2[1])])
        n1 = T("1", *VU.px(-.5, 1.5)[:1], VU.px(-.5, 1.5)[1] + 12, 34, "center")
        n2 = T("2", VU.px(.5, 1.5)[0], VU.px(.5, 1.5)[1] + 12, 34, "center")
        h1 = TC(r"\dfrac{1}{2}", *VU.px(1.36, 1.68), 34, "c")
        h2 = TC(r"\dfrac{1}{2}", *VU.px(-1.36, 1.68), 34, "c")
        self.pena(n1, n2, h1, h2, lag=0.35)
        # v2: o 3 nasce da contagem (os quatro números das células descem para baixo do trapézio, acima do eixo u)
        X3, Y3 = VU.px(-1.6, .5)
        t3 = T("3", X3, Y3, 30, "left", LIMA)
        tc = T("CÉLULAS", dir_(t3) + 10, Y3, 30, "left", LIMA)
        voa(self, VGroup(n1, n2, h1, h2).copy(), t3, rt=1.0, arco=0.0, livre=(c1, c2, t1, t2, ed, alvo_reg, dU["sx"], dU["sy"]))
        self.pena(tc)
        self.gat("três meios")
        # v2 Q09: nada de bloco colorido voando; a área nasce DENTRO da região (o desenho acende e o número é escrito nele)
        aX, aY = 1192, 522
        at = T("ÁREA", aX, aY + 10, 26, "left", GEO)
        af = TC(r"\Ge{\dfrac{3}{2}}", dir_(at) + 22, aY, 32, "c")
        realca(self, reg[1], cor=GEO, rt=0.5, wpx=5)
        self.pena(at, af, lag=0.2)
        # ── por último: meio quadradinho do papel? uma célula da grade inclinada com ÁREA ? ──
        self.gat("meio quadradinho do papel")
        cx = celula(VX, mapT, 0, 1, 1, 2, wb=2.5)
        entra_cel(self, cx, rt=0.8)
        ra = rotm([("t", "ÁREA", LIMA), ("m", r"\Al{?}")], *VX.px(1.55, -.55), 26, "l")
        self.pena(ra)
        self.marca("01")

        # ════ H2 · a ideia do vídeo ════
        self.an("H2")
        self.secao("A IDEIA DO VÍDEO")
        self.gat("a grade muda")
        cH = celula(VH, mapT, 0, 1, 1, 2, wb=3)
        fu2 = familia(VH, mapT, range(-1, 3), "u", AH, CU, 1.6, .5)
        fv2 = familia(VH, mapT, range(0, 3), "v", AH, CVV, 1.6, .5)
        sai = [m for m in self.snap() if m is not cx]
        self.play(*[FadeOut(m) for m in sai], run_time=0.5)
        self.remove(*sai)
        self.fundo(rt=0.3)                  # v2 §1.2: H2 fora da célula = papel() na unidade padrão
        self.play(Transform(cx, cH), FadeIn(fu2), FadeIn(fv2), run_time=1.4)
        ldu = rot_v(VH, r"\Du", (1.32, -.15), 8, 0, 30, "l")
        ldv = rot_v(VH, r"\Dv", (.68, -.95), -8, 10, 30, "r")
        self.pena(ldu, ldv, lag=0.2)
        self.gat("estica ou encolhe")
        self.play(cx.animate(rate_func=there_and_back).scale(1.12, about_point=cx.get_center()), run_time=1.4)
        self.gat("se chama jacobiano")
        j1 = T("JACOBIANO = FATOR LOCAL DE ÁREA", 1080, 430, 40, "left", LIMA)
        self.pena(j1)
        self.gat("vira o módulo")
        j2 = TC(r"\dX\,\dY\;=\;\Lm{|J|}\,\du\,\dv", 1080, 560, 64, "l")
        self.pena(j2)
        self.marca("02")
        sai_com_canto(self)
