"""yt_0039 · E1 · a faixa entre parábolas (alvos 02 e 03). E1-1 (layout A): as curvas uma por gatilho, a região A, o enunciado, as duas tiras
com TRAVA, y − x² acende no integrando e nas bordas. E1-2 (layout B, alvo 02): C1a (passos 1–3: u, v; x, y; a matriz e o determinante por
mapa; |J| = 1), a tira em pé que SÓ ESCORREGA, depois C1b (passo 4): cada borda voa do xy para a coluna e a borda nova voa para o uv; os
cantos; o trapézio B_uv. E1-3 (layout A com o uv, alvo 03): C1c (integral montada com os limites voando do palco; de dentro com o par v/v
que cancela; de fora; e² − e ≈ 4,67 com ✓). E1-4 (layout B): C1d (área do trapézio pelas chaves; área de A por duas tiras; 3/2 ✓)."""
from k39 import *
from k39 import _troca_col  # noqa: F401

VXY = Vw(215, 985, 118)
VUV = Vw(720, 770, 170)
VU3 = Vw(260, 820, 250)
lo = lambda X: 1 + X * X if X <= 1 else X + X * X
hi = lambda X: 2 + X * X


def regiao_A(v, fill=FUNDO_R):
    return poly_px([v.px(*p) for p in cX(lo, 0, 2) + cX(hi, 0, 2)[::-1]], fill, 1.0, z=1)


def trapezio(v, fill=FUNDO_R):
    return poly_px([v.px(*p) for p in [(0, 1), (1, 1), (2, 2), (0, 2)]], fill, 1.0, z=1)


def eixos_uv(v, a1=2.4, b1=2.4, ticks=True):
    sx = seta_px(v.px(-.05, 0), v.px(a1, 0), LAR, 3, 16, z=6)
    sy = seta_px(v.px(0, -.05), v.px(0, b1), VAG, 3, 16, z=6)
    A, B = v.px(a1, 0), v.px(0, b1)
    lu = TC(r"\U", A[0] + 22, A[1], 32, "c")
    lv = TC(r"\V", B[0], B[1] - 26, 32, "c")
    tks = []
    if ticks:
        tks = [tk(v, "x", 1, r"\Or{1}"), tk(v, "x", 2, r"\Or{2}"), tk(v, "y", 1, r"\Ag{1}"), tk(v, "y", 2, r"\Ag{2}")]
    pronto(sx, sy, lu, lv, *[q for t in tks for q in t])
    return {"o": v.P(0, 0), "sx": sx, "sy": sy, "lu": lu, "lv": lv, "tk": tks, "todos": [sx, sy, lu, lv] + [p for t in tks for p in t]}


def cria_uv(sc, E, rt=0.6, extra=()):
    sc.play(GrowFromPoint(E["sx"], E["o"]), GrowFromPoint(E["sy"], E["o"]), *[Create(t[0]) for t in E["tk"]], *extra, run_time=rt)
    sc.pena(E["lu"], E["lv"], *[t[1] for t in E["tk"]], lag=0.04)


class PE1(B39x):
    ANTES = "1 · A FAIXA ENTRE PARÁBOLAS"
    COLX = 1080

    def corpo(self):
        v = VXY
        # ═══ E1-1 · trava ═══
        self.an("E1-1")
        self.gat("primeiro problema")
        P = monta_palco(self, v, -.05, 2.55, -.05, 6.35, ticks=[("x", 1, r"\Am{1}"), ("x", 2, r"\Am{2}"), ("y", 2, r"\Mg{2}"), ("y", 6, r"\Mg{6}")])
        self.gat("um mais x ao quadrado")
        c1 = curva(v, cX(lambda X: 1 + X * X, 0, 2.1), GEO, 3)
        l1 = rot_m(v, r"y=1+x^2", (.62, 1.38), 44, 30, 26, "l")
        self.play(Create(c1), run_time=0.8)
        self.pena(l1)
        self.gat("dois mais x ao quadrado")
        c2 = curva(v, cX(lambda X: 2 + X * X, 0, 2.03), GEO, 3)
        l2 = rot_m(v, r"y=2+x^2", (1.15, 3.6), -8, 0, 26, "r")
        self.play(Create(c2), run_time=0.8)
        self.pena(l2)
        self.gat("x mais x ao quadrado")
        c3 = curva(v, cX(lambda X: X + X * X, 0, 2.05), GEO, 2, dash=(9, 7))
        l3 = rot_m(v, r"y=x+x^2", (1.55, 2.3), 10, 0, 26, "l")
        self.play(Create(c3), run_time=0.8)
        self.pena(l3)
        cantos = VGroup(*[ponto_px(*v.px(*p), BR, 6, z=9) for p in [(0, 1), (0, 2), (1, 2), (2, 6)]])
        self.play(FadeIn(cantos[2]), FadeIn(cantos[3]), run_time=0.4)          # v2 §5: as interseções no gatilho da curva que as cria
        self.gat("x maior ou igual a zero")
        RA = regiao_A(v)
        e0 = lin_px([v.px(0, 1), v.px(0, 2)], GEO, 3, z=5)
        self.play(FadeIn(RA), Create(e0), FadeIn(cantos[0]), FadeIn(cantos[1]), run_time=0.8)
        self.gat("calcule a integral dupla")
        En = linha(self, [("ii", r"\iint_A"), ("fr", r"\dfrac{e^{y-x^2}}{y-x^2}"), ("dA", r"\,dA")], 40, y=300)
        self.gat("pausa o vídeo")
        pz = poe_pausa(self, pxof(En.get_right())[0] + 40, 312)
        self.gat("em pé")
        t1 = tiraV(v, .5, lo(.5), hi(.5), h=.06, cor=E1)
        pe1 = pontos_es(v, (.5, lo(.5)), (.5, hi(.5)))
        self.play(FadeIn(t1), FadeIn(pe1[0]), FadeIn(pe1[1]), run_time=0.6)
        # v2 §5 (2:06, 10 s): a integral de dentro da fatia em pé aparece na coluna e trava num "?"
        self.gat("A integral de dentro")
        Ti = linha(self, [("i", r"\int"), ("f", r"\dfrac{e^{y-x^2}}{y-x^2}"), ("d", r"\,dy"), ("e", "="), ("q", r"\Al{?}")], 34, gap=40, escreve=False)
        nT, bT, dT = frac_ix(En, "fr")
        self.pena(parte(Ti, ix_(Ti, "i"), "∫"))
        voos(self, [(G(En, ix_(En, "fr")).copy(), parte(Ti, ix_(Ti, "f"), "integrando"))], rt=0.8)
        self.pena(parte(Ti, ix_(Ti, "d", "e"), "dy ="))
        self.gat("isso não existe")
        self.pena(parte(Ti, ix_(Ti, "q"), "?"))
        self.gat("Trava")
        tv1 = placa_t("TRAVA", *v.px(.5, 2.55), AL, 28, "c")
        self.pena(tv1)
        # D1: o rascunho da substituição t = y − x² e o selo (degraus escritos a caneta na fala que segue)
        R1 = linha(self, [("t", "t"), ("e", "="), ("y", r"y-x^2"), ("q", r"\ ,\ "), ("d", "dt"), ("e2", "="), ("dy", "dy")], 30, gap=14)
        R2 = linha(self, [("i", r"\int"), ("f", r"\dfrac{e^{t}}{t}"), ("d", r"\,dt")], 30, gap=14)
        slo = palavra(self, "SEM PRIMITIVA ELEMENTAR", AL, 26, gap=18)
        self.gat("fatia deitada trava")
        t2 = tiraH(v, 4.0, math.sqrt(2), (-1 + math.sqrt(17)) / 2, h=.12, cor=E2)
        self.play(FadeIn(t2), run_time=0.6)
        self.gat("trava também")
        tv2 = placa_t("TRAVA", *v.px(2.0, 4.2), AL, 28, "c")
        self.pena(tv2)
        self.gat("enxerga")
        num, bar, den = frac_ix(En, "fr")
        g_exp, g_den = G(En, num[1:]), G(En, den)
        cor_glifos(self, [g_exp, g_den], VAG, 0.6)
        self.gat("e as bordas também")
        self.play(c1.animate.set_stroke(VAG), c2.animate.set_stroke(VAG), run_time=0.6)
        self._fecha(antes=0.5)
        self.play(*[FadeOut(m) for m in (t1, *pe1, t2, tv1, tv2, pz)], c1.animate.set_stroke(GEO), c2.animate.set_stroke(GEO), run_time=0.5)
        self.remove(t1, *pe1, t2, tv1, tv2, pz)
        tira(self, Ti, R1, R2, slo)

        # ═══ E1-2 · passos 1 a 4 (layout B, alvo 02) ═══
        self.an("E1-2")
        u = VUV
        gnova = papel_dois(v, u)
        E = eixos_uv(u)
        sphi = seta_px((560, 600), (650, 600), GEO, 3, 14, z=6)
        lphi = TC(r"\varphi", 605, 570, 30, "c")
        self.colX = 1210
        En.generate_target()
        En.target.scale(.82).move_to(PX(1210, 180) + RIGHT * (En.width * .82 / 2))
        self.play(FadeOut(self.grade), FadeIn(gnova), MoveToTarget(En), run_time=0.6)
        self.grade = gnova
        self.colY = 240
        self.gat("passo um")
        L1, r1 = linha(self, [("u", r"\U"), ("e1", "="), ("x", "x"), ("q", r"\qquad"), ("v", r"\V"), ("e2", "="), ("y", "y"), ("m", "-"), ("x2", "x^2")],
                       36, rot="PASSO 1", voos=[(VGroup(*[En[0][i] for i in num[1:]]), ["y", "m", "x2"])])
        self.gat("Chama x de u")
        lin6 = []
        for x_ in (.5, 1.0, 1.5):
            g_ = curva(v, [(x_, lo(x_)), (x_, hi(x_))], "#FF9440", 2)
            lin6.append(g_)
            self.play(Create(g_), run_time=0.5)
        self.gat("adorou de v")
        for c_ in (1.25, 1.5, 1.75):
            g_ = curva(v, cX(lambda X, c_=c_: c_ + X * X, 0, c_), VAG, 2)
            lin6.append(g_)
            self.play(Create(g_), run_time=0.5)
        self.gat("passo dois")
        cria_uv(self, E, extra=[Create(sphi)])
        self.pena(lphi)
        L2, r2 = linha_de(self, L1, [("x", "x"), ("e1", "="), ("u", r"\U"), ("q", r"\qquad"), ("y", "y"), ("e2", "="), ("v", r"\V"), ("p", "+"),
                                    ("u2", r"\U^2")], [("x", "x"), ("e1", "e1"), ("u", "u"), ("q", "q"), ("y", "y"), ("e2", "e2"), ("v", "v"), ("m", "p"), ("x2", "u2")],
                          n=0, rot="PASSO 2", nota="C1a: o x² vira u² e atravessa a igualdade")
        degrau(self, "C1a", "x = u, y = v + u²")
        self.gat("passo três")
        L3, r3 = linha(self, [("J", "J"), ("e", "="), ("M", r"\begin{vmatrix}\dfrac{\partial x}{\partial \U} & \dfrac{\partial x}{\partial \V}\\[14pt] \dfrac{\partial y}{\partial \U} & \dfrac{\partial y}{\partial \V}\end{vmatrix}"),
                                 ("e2", "="), ("N", r"\begin{vmatrix} 1 & 0\\ 2\U & 1\end{vmatrix}")], 32, rot="PASSO 3", escreve=False)
        self.pena(r3)
        L3._matriz = True
        iN = ix_(L3, "N")
        cyN = L3[0][iN[0]].get_center()[1]
        alto = max(iN, key=lambda i: L3[0][i].height)
        hN = L3[0][alto].height
        corpoN = [i for i in iN if L3[0][i].height < .8 * hN]
        top = [i for i in corpoN if L3[0][i].get_center()[1] > G(L3, iN).get_center()[1]]
        bot = [i for i in corpoN if i not in top]
        barras = [i for i in iN if i not in corpoN]
        self.pena(parte(L3, ix_(L3, "J", "e", "M", "e2") + barras, "J = |∂| ="))
        self.gat("A primeira linha na tela")
        self.pena(parte(L3, sorted(top, key=lambda i: L3[0][i].get_center()[0]), "1 0"))
        self.gat("A segunda é a das derivadas de y")
        self.pena(parte(L3, sorted(bot, key=lambda i: L3[0][i].get_center()[0]), "2u 1"))
        degrau(self, "C1a", "J = |1 0; 2u 1|")
        self.gat("Agora o determinante")
        topx = sorted(top, key=lambda i: L3[0][i].get_center()[0])
        botx = sorted(bot, key=lambda i: L3[0][i].get_center()[0])
        L4 = linha(self, [("J", "J"), ("e", "="), ("a", "1"), ("c1", r"\cdot"), ("d", "1"), ("m", "-"), ("b", "0"), ("c2", r"\cdot"), ("cc", r"2\U")],
                   36, escreve=False, x=pxof(L3.get_left())[0])
        gmap(self, 1, L3, L4, [("J", "J"), ("e", "e"), (topx[:1], "a"), (botx[-1:], "d"), (topx[1:], "b"), (botx[:-1], "cc")], rt=1.4, copia=True,
             nota="C1a: o determinante abre por mapa (diagonal − antidiagonal)")
        degrau(self, "C1a", "J = 1·1 − 0·2u")
        self.leitura(G(L4, ix_(L4, "b", "c2", "cc")), rt=0.9)
        Z0 = linha(self, [("z", r"0\cdot 2\U"), ("e", "="), ("r", "0")], 34, gap=18, voos=[(G(L4, ix_(L4, "b", "c2", "cc")), "z")])
        self.gat("o jacobiano é um")
        L4 = cad(self, L4, [("e", "="), ("r", "1")], [("^a", "r")], n=1, nota="C1a: = 1")
        L4 = cad(self, L4, [("q", r"\qquad"), ("mJ", r"|J|=\Jl{1}")], [], n=1, nota="|J| = 1")
        degrau(self, "C1a", "= 1, |J| = 1")
        # v2 B1 · o mapa em ação: a região A com a grade 8 × 5 escorrega (y → y − x²) no próprio xy e pousa no plano u, v como o trapézio
        self.gat("com x parado")
        vlo = lambda U: max(1.0, U)
        cel_ = celulas(0, 2, 1, 2, 8, 5, k=8, qlo=vlo, qhi=lambda U: 2.0)

        def pos12(U, Vv, a):
            a1 = smooth(min(1.0, a / .62))
            a2 = smooth(max(0.0, (a - .62) / .38))
            pa, pb = v.px(U, Vv + (1 - a1) * U * U), u.px(U, Vv)
            return (pa[0] + (pb[0] - pa[0]) * a2, pa[1] + (pb[1] - pa[1]) * a2)
        MA = MapaAcao(cel_, pos12, fill=mixh(BG_, GEO, .42), teste={(1, 2): AZC, (4, 2): CORAL, (6, 0): LIMA})
        self.play(FadeIn(MA.g), RA.animate.set_opacity(.35), run_time=0.5)
        self.gat("cada carta escorrega")
        sl = placa_t("SÓ ESCORREGA", *v.px(.35, 5.2), GEO, 26)
        self.play(UpdateFromAlphaFunc(MA.g, lambda m, a: MA.at(.62 * smooth(a))), run_time=2.5)
        self.pena(sl)
        self.gat("a área não")
        self.play(UpdateFromAlphaFunc(MA.g, lambda m, a: MA.at(.62 + .38 * smooth(a))), RA.animate.set_opacity(1.0), run_time=1.2)
        print(f"[mapa] {self.lote} E1-2 mapa em ação (x, y) → (x, y − x²): 40 células, 2,5 s escorregando + 1,2 s até o uv")
        # ── passo 4 (C1b): a coluna limpa, o chip |J| = 1 sobe ──
        self.gat("passo quatro")
        chJ = chip(self, r"|J|=\Jl{1}", 1210, 175, de=G(L4, ix_(L4, "mJ")).copy())
        self.play(FadeOut(sl), *[FadeOut(g_) for g_ in lin6], *MA.so_linhas(), run_time=0.3)
        self.remove(sl)
        limpa_col(self, keep=())
        self.remove(En)
        self.colY = 240
        bordas = [("y igual a um mais", c1, cX(lambda X: 1 + X * X, 0, 1), l1, r"y=1+x^2", r"\V=1", [(0, 1), (1, 1)], AZC, (.5, 1), (0, -24)),
                  ("a de dois mais x ao quadrado vira", c2, cX(lambda X: 2 + X * X, 0, 2), l2, r"y=2+x^2", r"\V=2", [(0, 2), (2, 2)], CORAL, (1, 2), (0, -26)),
                  ("x igual a zero vira", e0, [(0, 1), (0, 2)], None, r"x=0", r"\U=0", [(0, 1), (0, 2)], AZC, (0, 1.5), (-40, 0)),
                  ("x mais x ao quadrado vira", c3, cX(lambda X: X + X * X, 1, 2), l3, r"y=x+x^2", r"\V=\U", [(1, 1), (2, 2)], CORAL, (1.5, 1.5), (34, 12))]
        segs = []
        for frase, cur, pts, lab, ltx, rtx, seg, cor, pl, dl in bordas:
            self.gat(frase)
            hl = curva(v, pts, cor, 4, z=7)
            self.play(Create(hl), run_time=0.3)
            if segs:
                limpa_col(self, keep=())
                self.colY = 240
            Lb0 = linha(self, [("l", ltx)], 36, escreve=False, gap=22)
            fonte = lab.f if lab is not None else hl
            voos(self, [(fonte.copy(), parte(Lb0, ix_(Lb0, "l"), "esq"))], rt=0.6)
            il = ix_(Lb0, "l")
            src_ = Lb0
            if ltx.startswith("y"):
                mid = {r"y=1+x^2": r"y-x^2=1", r"y=2+x^2": r"y-x^2=2", r"y=x+x^2": r"y-x^2=x"}[ltx]
                Lm = linha(self, [("l", mid)], 36, escreve=False, gap=22)
                im = ix_(Lm, "l")
                gmap(self, 2, Lb0, Lm, [([il[0]], [im[0]]), ([il[3]], [im[1]]), ([il[4], il[5]], [im[2], im[3]]), ([il[1]], [im[4]]), ([il[2]], [im[5]])],
                     rt=0.8, copia=True, nota=f"D3: {ltx} → {mid} (o x² atravessa a igualdade)")
                src_ = Lm
                il = im
            Lb = linha(self, [("r", rtx)], 36, escreve=False, gap=22)
            ir_ = ix_(Lb, "r")
            if ltx.startswith("y"):
                pares = [(il[:4], [ir_[0]]), ([il[4]], [ir_[1]]), ([il[5]], [ir_[2]])]
            else:
                pares = [([il[0]], [ir_[0]]), ([il[1]], [ir_[1]]), ([il[2]], [ir_[2]])]
            gmap(self, 2, src_, Lb, pares, rt=0.8, copia=True, nota=f"D3: {ltx} → {rtx}")
            sg = lin_px([u.px(*p) for p in seg], cor, 4, z=6)
            q = u.px(*pl)
            lb = TP(rtx, q[0] + dl[0], q[1] + dl[1], 26, "c")
            self.play(Create(sg), run_time=0.3)                       # v2 A11: a borda nova acende no trapézio (sem voo atravessando o palco)
            voos(self, [(G(Lb, ix_(Lb, "r")).copy(), lb)], rt=0.6)
            segs += [sg, lb]
            degrau(self, "C1b", f"{ltx} → {rtx}")
        self.gat("os cantos conferem")
        Lc1 = linha(self, [r"(0,1)\to(0,1)", r"\quad", r"(1,2)\to(1,1)"], 32, gap=22, escreve=False)
        Lc2 = linha(self, [r"(0,2)\to(0,2)", r"\quad", r"(2,6)\to(2,2)"], 32, gap=14, escreve=False)
        cu = VGroup(*[ponto_px(*u.px(*p), BR, 6, z=9) for p in [(0, 1), (0, 2), (1, 1), (2, 2)]])
        self.pena(Lc1)
        self.play(TransformFromCopy(cantos[0], cu[0]), TransformFromCopy(cantos[2], cu[2]), run_time=0.8)
        self.pena(Lc2)
        self.play(TransformFromCopy(cantos[1], cu[1]), TransformFromCopy(cantos[3], cu[3]), run_time=0.8)
        self.gat("virou um trapézio")
        TB = trapezio(u)
        lB = TP(r"B_{uv}", *u.px(.55, 1.55), 30, "c")
        self.play(FadeIn(TB), FadeOut(MA.g), run_time=0.6)
        self.remove(MA.g)
        self.pena(lB)
        self.gat("v vai de um a dois")
        Lb5 = linha(self, [("B", r"B_{uv}:"), ("v", r"1\le\V\le 2,"), ("u", r"\enspace 0\le\U\le\V")], 36, gap=22, escreve=False)
        self.pena(parte(Lb5, ix_(Lb5, "B", "v"), "v"))
        self.gat("u vai de zero até v")
        self.pena(parte(Lb5, ix_(Lb5, "u"), "u"))
        self.marca("02_E1-2")
        self._fecha(antes=0.6)

        # ═══ E1-3 · o comprimento cancela (layout A com o uv, alvo 03) ═══
        self.an("E1-3")
        u3 = VU3
        E3 = eixos_uv(u3, 2.4, 2.5)
        TB3 = trapezio(u3)
        bd3 = lin_px([u3.px(*p) for p in [(0, 1), (1, 1), (2, 2), (0, 2), (0, 1)]], GEO, 3, z=5)
        g3 = papel_tela(u3)
        # v2 A11: primeiro o xy sai inteiro; só depois o plano u, v cresce para o palco (nunca dois pares de eixos sobrepostos)
        xy_sai = palco_sai(self, keep=[TB] + [E[k] for k in ("sx", "sy", "lu", "lv")] + [q for t in E["tk"] for q in t]) + [self.grade]
        self.play(*[FadeOut(m) for m in xy_sai], run_time=0.5)
        self.remove(*xy_sai)
        self.play(ReplacementTransform(TB, TB3), *[ReplacementTransform(E[k], E3[k]) for k in ("sx", "sy", "lu", "lv")],
                  *[ReplacementTransform(a, b) for ta_, tb_ in zip(E["tk"], E3["tk"]) for a, b in zip(ta_, tb_)], FadeIn(g3), Create(bd3), run_time=1.0)
        self.grade = g3
        limpa_col(self)
        tira_chips(self)
        chJ = chip(self, r"|J|=\Jl{1}", 1100, 175)
        lvu = rot_m(u3, r"\V=\U", (1.8, 1.75), 16, 0, 28, "l")
        th_ = tiraH(u3, 1.75, 0, 1.75, h=.07, cor=VAG)
        pe = pontos_es(u3, (0, 1.75), (1.75, 1.75))
        a_, b_ = u3.px(0, 1.62), u3.px(1.75, 1.62)
        chv = chave_h(a_[0], b_[0], a_[1] + 10, VAG, 3)
        self.play(FadeIn(th_), FadeIn(pe[0]), FadeIn(pe[1]), run_time=0.5)
        self.pena(lvu)
        # v2 A5: COMPRIMENTO e = v em duas linhas centradas sob a chave, longe da borda coral (≥ 10 px)
        xm_ = (a_[0] + b_[0]) / 2
        lc_t = T("COMPRIMENTO", xm_, a_[1] + 56, 30, "center", VAG)
        lc_m = TC(r"=\V", xm_, a_[1] + 92, 32, "c")
        self.play(Create(chv), run_time=0.4)
        self.pena(lc_t, lc_m, lag=0.05)
        lc = VGroup(lc_t, lc_m)
        lc.p = [lc_t, lc_m]
        self.colX, self.colY = 1100, 250
        self.gat("passo cinco")
        lim_src = {"lo2": pe[0], "hi2": E3["lv"], "lo1": E3["tk"][2][1], "hi1": E3["tk"][3][1]}
        M1 = linha(self, [("A", r"\iint_A \dfrac{e^{y-x^2}}{y-x^2}\,dA"), ("e", "="), ("i1", r"\int_1^2"), ("i2", r"\!\!\int_0^{\V}"),
                          ("f", r"\dfrac{e^{\V}}{\V}"), ("c", r"\cdot"), ("j", r"\Jl{1}"), ("d", r"\enspace\du\,\dv")], 36, escreve=False)
        lo1, hi1 = lims(M1, "i1")
        lo2, hi2 = lims(M1, "i2")
        escreve_seq(self, M1, [(E3["tk"][2][1], lo1), (E3["tk"][3][1], hi1), (pe[0], lo2), (lvu.f, hi2),
                               (G(chJ.m, [len(chJ.m[0]) - 1]), ix_(M1, "j"))], rt_voo=0.8)
        origem(self, "limites 1, 2, 0, v (C1c)", "marcas do eixo v, entrada da tira (u = 0) e saída (v = u)")
        origem(self, "o 1 lima (C1c)", "chip |J| = 1")
        self.gat("entra o módulo do jacobiano")
        self.leitura(G(M1, ix_(M1, "j")), rt=0.8)
        degrau(self, "C1c", "∬_A … dA = ∫₁²∫₀^v (e^v/v)·1 du dv")
        self.gat("a de dentro é em u")
        palavra(self, "DE DENTRO")
        D1 = linha_de(self, M1, [("i", r"\int_0^{\V}"), ("f", r"\dfrac{e^{\V}}{\V}"), ("d", r"\,\du")], [("i2", "i"), ("f", "f"), ("d", "d")], n=3, rt=1.0,
                      nota="C1c: a integral de dentro sai da montada", gap=16)
        self.gat("não depende de u")
        self.leitura(G(D1, ix_(D1, "f")), rt=0.8)
        D1 = cad(self, D1, [("e", "="), ("f", r"\dfrac{e^{\V}}{\V}"), ("cl", r"\Big[\,\U\,\Big]_0^{\V}")], [("f", "f")], n=3, nota="C1c: e^v/v sai; [u]₀^v")
        degrau(self, "C1c", "= (e^v/v)[u]₀^v")
        self.gat("v menos zero")
        D1 = cad(self, D1, [("e", "="), ("f", r"\dfrac{e^{\V}}{\V}"), ("p", r"(\V-0)")], [("^f", "f")], n=3, nota="C1c: (v − 0)",
                 voos=[(G(lc.p[1], [1]).copy() if len(lc.p[1][0]) > 1 else lc.p[1].copy(), "p")])
        origem(self, "(v − 0)", "chave COMPRIMENTO = v da tira deitada (voo) + colchete [u]₀^v")
        degrau(self, "C1c", "= (e^v/v)(v − 0)")
        self.gat("cancela o v que estava embaixo")
        n_, b_, d_ = frac_ix(D1, "f")
        ip = ix_(D1, "p")
        vp = [i for i in ip if D1[0][i].get_center()[0] < G(D1, ip).get_center()[0]][1:2]
        cancela(self, G(D1, d_), G(D1, vp))
        self.gat("Sobra só é elevado a v")
        D1 = cad(self, D1, [("e", "="), ("r", r"e^{\V}")], [(n_, "r")], n=3, nota="C1c: o par v/v some; = e^v")
        degrau(self, "C1c", "= e^v")
        self.gat("a de fora")
        palavra(self, "DE FORA")
        # v2 B2 · a tira que varre: a de dentro é o comprimento da tira (u de 0 a v); a de fora a leva de v = 1 a v = 2
        self.play(FadeOut(chv), FadeOut(lc_t), FadeOut(lc_m), FadeOut(th_), FadeOut(pe[0]), FadeOut(pe[1]), run_time=0.3)
        self.remove(chv, lc_t, lc_m, th_, *pe)
        vt = ValueTracker(1.0)
        tv_ = always_redraw(lambda: VGroup(tiraH(u3, vt.get_value(), 0, vt.get_value(), h=.07, cor=VAG),
                                           *pontos_es(u3, (0, vt.get_value()), (vt.get_value(), vt.get_value()))))
        self.add(vt)
        self.play(FadeIn(tv_), run_time=0.3)
        self.play(vt.animate.set_value(2.0), run_time=3.0, rate_func=linear)
        tv_.clear_updaters()
        print(f"[varre] {self.lote} E1-3 tira deitada varre v de 1 a 2 em 4,5 s (1 updater)")
        F1 = linha(self, [("i", r"\int_1^2"), ("f", r"e^{\V}"), ("d", r"\,\dv")], 36, gap=22, escreve=False)
        lo_, hi_ = lims(F1, "i")
        self.pena(parte(F1, [i for i in ix_(F1, "i") if i not in lo_ + hi_], "∫"))
        voos(self, [(G(M1, lo1).copy(), parte(F1, lo_, "1")), (G(M1, hi1).copy(), parte(F1, hi_, "2")), (G(D1, ix_(D1, "r")).copy(), parte(F1, ix_(F1, "f"), "e^v"))], rt=0.9)
        self.pena(parte(F1, ix_(F1, "d"), "dv"))
        self.gat("a primitiva de é elevado")
        F1 = cad(self, F1, [("e", "="), ("c", r"\Big[e^{\V}\Big]_1^2")], [("f", "c")], n=4, nota="C1c: [e^v]₁²")
        self.gat("aplica de um a dois")
        F1 = cad(self, F1, [("e", "="), ("d", r"e^2-e^1")], [("^c", "d")], n=4, nota="C1c: e² − e¹")
        degrau(self, "C1c", "[e^v]₁² = e² − e¹")
        self.gat("Dá mais ou menos")
        F2a = cad(self, F1, [("e", r"\approx"), ("n", r"7{,}389-2{,}718")], [], n=4, desce=True, nota="D4: e² ≈ 7,389 e e ≈ 2,718")
        F2 = cad(self, F2a, [("e", "="), ("r", r"\Me{4{,}671}")], [("^n", "r")], n=4, nota="D4: = 4,671")
        degrau(self, "C1c", "= e² − e ≈ 4,67")
        cor_glifos(self, [G(F2, ix_(F2, "r"))], MEN, 0.4)
        ok_ao_lado(self, F2)
        self.marca("03_E1-3")
        self._fecha(antes=0.6)

        # ═══ E1-4 · conferindo pela área (layout B) ═══
        self.an("E1-4")
        self.gat("Mas será que está certo")
        sai = palco_sai(self, keep=[TB3, bd3] + [E3[k] for k in ("sx", "sy", "lu", "lv")] + [q for t in E3["tk"] for q in t])
        limpa_col(self)
        tira_chips(self)
        u = VUV
        E4 = eixos_uv(u)
        TB4 = trapezio(u)
        bd4 = lin_px([u.px(*p) for p in [(0, 1), (1, 1), (2, 2), (0, 2), (0, 1)]], GEO, 3, z=5)
        gnova = papel_dois(v, u)
        P2 = {"sx": seta_px(v.px(-.05, 0), v.px(2.55, 0), E1, 3, 16, z=6), "sy": seta_px(v.px(0, -.05), v.px(0, 6.35), E2, 3, 16, z=6)}
        lx2, ly2 = TC(r"\X", *[a + b for a, b in zip(v.px(2.55, 0), (22, 0))], 32, "c"), TC(r"\Y", *[a + b for a, b in zip(v.px(0, 6.35), (0, -26))], 32, "c")
        RA2 = regiao_A(v)
        cc1 = curva(v, cX(lambda X: 1 + X * X, 0, 1), AZC, 3)
        cc2 = curva(v, cX(lambda X: 2 + X * X, 0, 2), CORAL, 3)
        cc3 = curva(v, cX(lambda X: X + X * X, 1, 2), CORAL, 3, dash=(9, 7))
        cc0 = lin_px([v.px(0, 1), v.px(0, 2)], AZC, 3, z=5)
        tks2 = [tk(v, "x", 1, r"\Am{1}"), tk(v, "x", 2, r"\Am{2}"), tk(v, "y", 2, r"\Mg{2}"), tk(v, "y", 6, r"\Mg{6}")]
        self.play(*[FadeOut(m) for m in sai + [self.grade, bd3] if m in self.mobjects], ReplacementTransform(TB3, TB4), *[ReplacementTransform(E3[k], E4[k]) for k in ("sx", "sy", "lu", "lv")],
                  *[ReplacementTransform(a, b) for ta_, tb_ in zip(E3["tk"], E4["tk"]) for a, b in zip(ta_, tb_)], FadeIn(gnova), Create(bd4),
                  GrowFromPoint(P2["sx"], v.P(0, 0)), GrowFromPoint(P2["sy"], v.P(0, 0)), FadeIn(RA2), Create(cc1), Create(cc2), Create(cc3), Create(cc0),
                  *[Create(t[0]) for t in tks2], run_time=1.0)
        self.remove(*sai, bd3)
        self.grade = gnova
        self.pena(lx2, ly2, *[t[1] for t in tks2], lag=0.03)
        self.colX, self.colY = 1210, 220
        self.gat("No plano u v a região")
        k1 = chave_h(*[u.px(0, 1)[0], u.px(1, 1)[0]], u.px(0, 1)[1] + 14, GEO, 2, True)
        kb1 = mixl([("t", "BASE", GEO), ("m", "1")], u.px(.5, 1)[0] - 50, u.px(.5, 1)[1] + 48, 30)
        k2 = chave_h(u.px(0, 2)[0], u.px(2, 2)[0], u.px(0, 2)[1] - 14, GEO, 2, False)
        kb2 = mixl([("t", "BASE", GEO), ("m", "2")], u.px(1, 2)[0] - 50, u.px(1, 2)[1] - 48, 30)
        k3 = chave_v(u.px(0, 1)[0] - 92, u.px(0, 2)[1], u.px(0, 1)[1], GEO, 2, True)
        kh = mixl([("t", "ALTURA", GEO), ("m", "1")], u.px(0, 1.5)[0] - 280, u.px(0, 1.5)[1], 30)
        self.play(Create(k1), Create(k2), Create(k3), run_time=0.6)
        self.pena(*kb1.p, *kb2.p, *kh.p, lag=0.05)
        self.gat("média das bases vezes a altura")
        A1, ra1 = linha(self, [("B", r"B=\dfrac{1+2}{2}\cdot 1")], 34, rot="ÁREA DE", escreve=False)
        nB, bB, dB = frac_ix(A1, "B")
        escreve_seq(self, A1, [(kb1.p[1], [nB[0]]), (kb2.p[1], [nB[2]]), (kh.p[1], [len(A1[0]) - 1])])
        A1._pec = [("B", r"B=\dfrac{1+2}{2}\cdot 1")]
        origem(self, "1, 2 e 1 de (1+2)/2 · 1", "chaves BASE 1, BASE 2 e ALTURA 1 do trapézio")
        self.pena(ra1)
        self.gat("três meios agora")
        A1 = cad(self, A1, [("e", "="), ("r", r"\dfrac{3}{2}")], [], n=5, nota="C1d: área do trapézio = 3/2")
        degrau(self, "C1d", "ÁREA DE B = (1+2)/2 · 1 = 3/2")
        self.gat("de zero a um a fatia")
        s1 = tiraV(v, .5, 1.25, 2.25, h=.05, cor=E1)
        pp1 = pontos_es(v, (.5, 1.25), (.5, 2.25))
        self.play(FadeIn(s1), FadeIn(pp1[0]), FadeIn(pp1[1]), run_time=0.5)
        A2, ra2 = linha(self, [("i", r"A=\int_0^1"), ("b", r"\big[(2+x^2)-(1+x^2)\big]"), ("d", r"\,dx")], 30, rot="ÁREA DE", gap=30)
        self.gat("o x ao quadrado cancela")
        ib = ix_(A2, "b")
        xs = [i for i in ib if A2[0][i].get_center()[1] > A2[0][ib[0]].get_center()[1] + .06]       # os expoentes 2
        xx = sorted([i for i in ib], key=lambda i: A2[0][i].get_center()[0])
        cancela(self, G(A2, [xx[3], xx[4]]), G(A2, [xx[10], xx[11]]))
        A3 = cad(self, A2, [("e", "="), ("i", r"\int_0^1 1\,dx")], [("i", "i")], n=5, desce=True, nota="C1d: os x² acendem e somem: comprimento 1")
        degrau(self, "C1d", "= ∫₀¹ 1 dx")
        self.gat("de um a dois ela entra")
        s2 = tiraV(v, 1.5, 3.75, 4.25, h=.05, cor=E1)
        pp2 = pontos_es(v, (1.5, 3.75), (1.5, 4.25))
        self.play(FadeIn(s2), FadeIn(pp2[0]), FadeIn(pp2[1]), run_time=0.5)
        A4 = linha(self, [("p", "+"), ("i", r"\int_1^2"), ("b", r"\big[(2+x^2)-(x+x^2)\big]"), ("d", r"\,dx")], 30, gap=14, x=pxof(A3.get_left())[0])
        self.gat("o comprimento é dois menos x")
        kk2 = chave_v(v.px(1.5, 0)[0] - 16, v.px(1.5, 4.25)[1], v.px(1.5, 3.75)[1], GEO, 2, True)
        lk2 = TP(r"2-x", v.px(1.5, 0)[0] - 40, v.px(1.5, 4.0)[1], 28, "r")
        self.play(Create(kk2), run_time=0.4)
        self.pena(lk2)
        A4 = cad(self, A4, [("e", "="), ("r", r"\int_1^2(2-x)\,dx")], [("i", "r")], n=5, desce=True, nota="C1d: 2 − x", xq=pxof(A3.get_left())[0])
        degrau(self, "C1d", "+ ∫₁² (2 − x) dx")
        self.gat("A primeira é fácil")
        sobe_col(self, [A2, ra2, A3, A4], y0=220)                                # D5: o que já virou resultado sai; a conta nova sobe
        A5 = linha(self, [("e", "="), ("a", r"\big[x\big]_0^1"), ("p", "+"), ("b", r"\Big[2x-\dfrac{x^2}{2}\Big]_1^2")], 30, gap=16, x=pxof(A3.get_left())[0])
        degrau(self, "C1d", "= [x]₀¹ + [2x − x²/2]₁²")
        self.gat("a gente aplica os limites")
        A6 = linha_de(self, A5, [("e", "="), ("a", r"(1-0)"), ("p", "+"), ("b", r"\Big[(4-2)-\Big(2-\dfrac{1}{2}\Big)\Big]")], [("e", "e"), ("a", "a"), ("p", "p"), ("b", "b")],
                      n=5, size=30, gap=16, x=pxof(A3.get_left())[0], nota="C1d: G(b) − G(a) nos dois colchetes")
        degrau(self, "C1d", "= (1 − 0) + [(4 − 2) − (2 − 1/2)]")
        sobe_col(self, [A1, ra1, A5], y0=220)
        B1 = linha(self, [("a", r"2-\dfrac12"), ("e", "="), ("b", r"\dfrac42-\dfrac12"), ("e2", "="), ("r", r"\dfrac32")], 30, gap=14, x=pxof(A3.get_left())[0])
        B2 = linha(self, [("a", r"2-\dfrac32"), ("e", "="), ("b", r"\dfrac42-\dfrac32"), ("e2", "="), ("r", r"\dfrac12")], 30, gap=14, x=pxof(A3.get_left())[0])
        degrau(self, "D5", "2 − 1/2 = 4/2 − 1/2 = 3/2; 2 − 3/2 = 4/2 − 3/2 = 1/2")
        self.gat("um mais um meio")
        sobe_col(self, [A6, B1], y0=220)
        A7 = linha(self, [("e", "="), ("a", "1"), ("p", "+"), ("b", r"\dfrac{1}{2}"), ("e2", "="), ("a2", r"\dfrac22"), ("p2", "+"), ("b2", r"\dfrac12")], 30, gap=14,
                   x=pxof(A3.get_left())[0])
        A7 = cad(self, A7, [("e3", "="), ("r", r"\dfrac{3}{2}")], [("^a2", "r"), ("^b2", "r")], n=5, desce=True, nota="D5: 1 + 1/2 = 2/2 + 1/2 = 3/2")
        degrau(self, "D5", "= 1 + 1/2 = 2/2 + 1/2 = 3/2")
        self.gat("três meios de novo")
        ok_ao_lado(self, A7)
        ig = T("=", 600, 300, 80, "center", MEN)
        self.pena(ig)
        self.marca("E1-4", agora=True)
        self.sai_fim()
