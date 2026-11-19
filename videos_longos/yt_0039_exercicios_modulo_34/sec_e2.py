"""yt_0039 · E2 · as hipérboles (alvos 04 e 05). E2-1 (layout A, palco do alvo 04): hipérboles e retas, a região R, o enunciado, as duas tiras e
2 INTEGRAIS. E2-2 (alvo 04): C2a (u = xy, v = y/x; a grade nova; uv = y², u/v = x² → x, y por mapa; a matriz da ida com as quatro derivadas;
o determinante até 2v; a regra ida × volta = 1 com o 2v atravessando: J = 1/(2v)); a célula lima. E2-3 (alvo 05): o quadrado B_uv; C2b
(área = (ln 2)/2 ≈ 0,347); um movimento de câmera para o palco do alvo 05 e a pipa (√2/4 ≈ 0,354, ESTIMATIVA DA PIPA, sem ✓). E2-4: o
quadrado em faixas ciano; C2c (massa (3/4) ln 2 ≈ 0,520 kg; densidade média 3/2, MEIO DE 1 E 2, ✓)."""
from k39 import *
from k39 import _troca_col  # noqa: F401

V4 = Vw(150, 960, 300)
V5 = Vw(420, 1005, 410)
VQ = Vw(300, 880, 280)
S2 = math.sqrt(2)
xs0, xs1 = 1 / S2, S2
lo = lambda X: max(1 / X, X)
hi = lambda X: min(2 / X, 2 * X)


def regiao_R(v):
    return poly_px([v.px(*p) for p in cX(lo, xs0, xs1) + cX(hi, xs0, xs1)[::-1]], FUNDO_R, 1.0, z=1)


def bordas(v, cor_u=GEO, cor_v=GEO):
    return {"u1": curva(v, cX(lambda X: 1 / X, .5, 1.7), cor_u, 3), "u2": curva(v, cX(lambda X: 2 / X, .85, 1.7), cor_u, 3),
            "v1": curva(v, [(0, 0), (1.6, 1.6)], cor_v, 3), "v2": curva(v, [(0, 0), (1.1, 2.2)], cor_v, 3)}


def quadrado(v, fill=FUNDO_R):
    return poly_px([v.px(*p) for p in [(1, 1), (2, 1), (2, 2), (1, 2)]], fill, 1.0, z=1)


def eixos_q(v):
    sx = seta_px(v.px(-.05, 0), v.px(2.35, 0), LAR, 3, 16, z=6)
    sy = seta_px(v.px(0, -.05), v.px(0, 2.35), VAG, 3, 16, z=6)
    A, B = v.px(2.35, 0), v.px(0, 2.35)
    lu, lv = TC(r"\U", A[0] + 22, A[1], 32, "c"), TC(r"\V", B[0], B[1] - 26, 32, "c")
    tks = [tk(v, "x", 1, r"\Or{1}"), tk(v, "x", 2, r"\Or{2}"), tk(v, "y", 1, r"\Ag{1}"), tk(v, "y", 2, r"\Ag{2}")]
    return {"sx": sx, "sy": sy, "lu": lu, "lv": lv, "tk": tks, "todos": [sx, sy, lu, lv] + [p for t in tks for p in t]}


class PE2(B39x):
    ANTES = "2 · AS HIPÉRBOLES"
    COLX = 1040

    def corpo(self):
        v = V4
        # ═══ E2-1 · dois pedaços ═══
        self.an("E2-1")
        self.gat("segundo problema")
        P = monta_palco(self, v, -.05, 1.85, -.05, 2.55, ticks=[("x", 1, r"\Am{1}"), ("y", 1, r"\Mg{1}"), ("y", 2, r"\Mg{2}")])
        B = bordas(v)
        labs = {"u1": rot_m(v, r"xy=1", (1.62, .62), 10, 10, 26, "l"), "u2": rot_m(v, r"xy=2", (1.66, 1.21), 10, 4, 26, "l"),
                "v1": rot_m(v, r"y=x", (1.5, 1.5), 18, 22, 26, "l"), "v2": rot_m(v, r"y=2x", (1.02, 2.04), 16, 0, 26, "l")}
        for frase, k in (("entre as hipérboles", "u1"), ("x y igual a dois", "u2"), ("as retas y igual a x", "v1"), ("y igual a dois x", "v2")):
            self.gat(frase)
            self.play(Create(B[k]), run_time=0.7)
            self.pena(labs[k])
        RR_ = regiao_R(v)
        cantos = VGroup(*[ponto_px(*v.px(*p), BR, 6, z=9) for p in [(1, 1), (xs1, xs1), (1, 2), (xs0, xs1)]])
        self.play(FadeIn(RR_), FadeIn(cantos), run_time=0.6)
        self.gat("Calcule a área")
        self.colY = 230
        e1 = palavra(self, "ÁREA DE R", BR, 30)
        self.gat("e a massa de uma")
        e2 = linha(self, [r"\rr=xy"], 36, rot="MASSA DE R COM", rot_cor=BR, gap=24)
        self.gat("pausa e tenta")
        pz = poe_pausa(self, self.colX, pxof(e2[0].get_bottom())[1] + 60)
        self.gat("um sobre raiz de dois até")
        t0 = tk(v, "x", xs0, r"\Am{\dfrac{1}{\sqrt2}}")
        q0_ = v.px(xs0, 0)
        t0[1].move_to(PX(q0_[0] - 36, q0_[1] + 44))          # v2 A1: à esquerda e abaixo da marca, ≥ 14 px de qualquer traço
        t1 = tk(v, "x", xs1, r"\Am{\sqrt2}")
        self.play(Create(t0[0]), Create(t1[0]), run_time=0.4)
        self.pena(t0[1], t1[1], lag=0.1)
        self.gat("as bordas trocam")
        tr1 = lin_px([v.px(1, 0), v.px(1, 2.1)], GEO, 2, dash=(8, 8), z=6)
        self.play(Create(tr1), run_time=0.6)
        self.gat("entra na hipérbole de baixo")
        ta = tiraV(v, .85, 1 / .85, 1.7, h=.03, cor=E1)
        pa = pontos_es(v, (.85, 1 / .85), (.85, 1.7))
        self.play(FadeIn(ta), FadeIn(pa[0]), FadeIn(pa[1]), run_time=0.5)
        self.gat("entra na reta de baixo")
        tb = tiraV(v, 1.2, 1.2, 2 / 1.2, h=.03, cor=E1)
        pb = pontos_es(v, (1.2, 1.2), (1.2, 2 / 1.2))
        self.play(FadeIn(tb), FadeIn(pb[0]), FadeIn(pb[1]), run_time=0.5)
        self.gat("seriam duas integrais")
        d2 = placa_t("2 INTEGRAIS", *v.px(1.25, .45), AL, 30, "c")
        self.pena(d2)
        self.gat("olha as bordas de novo")
        self.play(*[Indicate(B[k], color=BR, scale_factor=1.0) for k in B], run_time=1.2)
        self._fecha(antes=0.5)
        self.play(*[FadeOut(m) for m in (ta, *pa, tb, *pb, d2, tr1, pz, t0[0], t0[1], t1[0], t1[1])], run_time=0.5)
        self.remove(ta, *pa, tb, *pb, d2, tr1, pz, *t0, *t1)
        limpa_col(self)

        # ═══ E2-2 · o jacobiano da volta (alvo 04) ═══
        self.an("E2-2")
        self.colY = 200
        self.gat("passo um u igual")
        P1, s1 = linha(self, [("u", r"\U=xy"), ("q", r"\qquad"), ("v", r"\V=\dfrac{y}{x}")], 36, rot="PASSO 1")
        novos = {"u1": rot_m(v, r"\U=1", (1.62, .62), 10, 10, 26, "l"), "u2": rot_m(v, r"\U=2", (1.66, 1.21), 10, 4, 26, "l"),
                 "v1": rot_m(v, r"\V=1", (1.5, 1.5), 18, 22, 26, "l"), "v2": rot_m(v, r"\V=2", (1.02, 2.04), 16, 0, 26, "l")}
        pronto(*novos.values())
        self.gat("Olha como as bordas")
        self.play(*[B[k].animate.set_stroke(LAR if k[0] == "u" else VAG) for k in B], *[ReplacementTransform(labs[k], novos[k]) for k in B], run_time=1.0)
        self.gat("a grade nova é feita")
        # v2 B1 · o mapa em ação: o quadrado [1, 2]² do plano u, v (5 × 5 células iguais) vira a região R por x = √(u/v), y = √(uv);
        # as três células de teste têm a mesma área no uv e ficam com áreas diferentes no xy (as de v pequeno maiores: 1/(2v))
        ins = lambda U, Vv: (780 + (U - 1) * 150, 700 - (Vv - 1) * 150)
        cel_ = celulas(1, 2, 1, 2, 5, 5, k=8)

        def pos22(U, Vv, a):
            pa, pb = ins(U, Vv), v.px(math.sqrt(U / Vv), math.sqrt(U * Vv))
            return (pa[0] + (pb[0] - pa[0]) * a, pa[1] + (pb[1] - pa[1]) * a)
        MA = MapaAcao(cel_, pos22, fill=mixh(BG_, GEO, .42), teste={(2, 0): AZC, (2, 2): CORAL, (2, 4): LIMA}, z=4)
        lu_i, lv_i = TC(r"\U", 855, 738, 28, "c"), TC(r"\V", 752, 625, 28, "c")
        self.play(FadeIn(MA.g), run_time=0.5)
        self.pena(lu_i, lv_i, lag=0.05)
        self.wait(0.6)
        self.play(FadeOut(lu_i), FadeOut(lv_i), run_time=0.3)
        self.remove(lu_i, lv_i)
        self.play(MA.anim(2.5), run_time=2.5)
        print(f"[mapa] {self.lote} E2-2 mapa em ação [1,2]² → R por x = √(u/v), y = √(uv): 25 células, 2,5 s")
        self.play(*MA.so_linhas(), run_time=0.5)
        gn = MA.g
        self.gat("Passo dois")
        P2, s2 = linha(self, [("uv", r"\U\V=y^2"), ("q", r"\qquad"), ("uv2", r"\dfrac{\U}{\V}=x^2")], 36, rot="PASSO 2", gap=22)
        self.gat("o x some")
        M1 = linha(self, [("a", r"\U\V"), ("e", "="), ("b", r"xy\cdot\dfrac{y}{x}"), ("e2", "="), ("r", r"y^2")], 30, gap=16)
        self.gat("o y some")
        M2 = linha(self, [("a", r"\dfrac{\U}{\V}"), ("e", "="), ("b", r"xy\div\dfrac{y}{x}"), ("e2", "="), ("r", r"x^2")], 30, gap=16)
        self.gat("então x é raiz")
        P2b = LL([("x", r"x=\sqrt{\U/\V}"), ("q", r"\qquad"), ("y", r"y=\sqrt{\U\V}")], pxof(P2.get_left())[0], pxof(P2.get_center())[1], 36)
        gmap(self, 6, P2, P2b, [("uv2", "x"), ("q", "q"), ("uv", "y")], rt=1.4, copia=False, nota="C2a: uv = y², u/v = x² → x = √(u/v), y = √(uv)")
        _troca_col(self, P2, P2b)
        degrau(self, "C2a", "x = √(u/v), y = √(uv)")
        self.gat("derivar essas raízes")
        dz = placa_t("DERIVAR DÁ TRABALHO", pxof(P2b.get_right())[0] + 20, pxof(P2b.get_center())[1] + 9, AL, 26)
        self.pena(dz)
        self.colms.append(dz)
        self.gat("Vai o atalho")
        sobe_col(self, [P1, s1, M1, M2], y0=200)
        P3, s3 = linha(self, [("D", r"\dfrac{\partial(\U,\V)}{\partial(x,y)}"), ("e", "="), ("M", r"\begin{vmatrix} y & x\\[10pt] -\dfrac{y}{x^2} & \dfrac{1}{x}\end{vmatrix}")],
                       34, rot="PASSO 3", gap=22, escreve=False)
        P3._matriz = True
        self.pena(s3)
        iM = ix_(P3, "M")
        hM = max(P3[0][i].height for i in iM)
        barras = [i for i in iM if P3[0][i].height > .8 * hM]
        corpo_ = [i for i in iM if i not in barras]
        cyM = G(P3, iM).get_center()[1]
        topo = sorted([i for i in corpo_ if P3[0][i].get_center()[1] > cyM], key=lambda i: P3[0][i].get_center()[0])
        base = sorted([i for i in corpo_ if P3[0][i].get_center()[1] <= cyM], key=lambda i: P3[0][i].get_center()[0])
        xm = G(P3, iM).get_center()[0]
        ent = [[i for i in topo if P3[0][i].get_center()[0] < xm], [i for i in topo if P3[0][i].get_center()[0] >= xm],
               [i for i in base if P3[0][i].get_center()[0] < xm], [i for i in base if P3[0][i].get_center()[0] >= xm]]
        self.pena(parte(P3, ix_(P3, "D", "e") + barras, "∂(u,v)/∂(x,y) = | |"))
        for frase, k in (("u derivado em x dá y", 0), ("em y dá x", 1), ("dá menos y sobre x ao quadrado", 2), ("em y dá um sobre x", 3)):
            self.gat(frase)
            self.pena(parte(P3, ent[k], f"entrada {k}"))
        self.gat("Agora o determinante")
        D1 = linha(self, [("e", "="), ("a", "y"), ("c1", r"\cdot"), ("d", r"\dfrac{1}{x}"), ("m", "-"), ("b", "x"), ("c2", r"\cdot"), ("cc", r"\left(-\dfrac{y}{x^2}\right)")],
                   32, gap=22, escreve=False, x=self.colX + 20)
        gmap(self, 7, P3, D1, [(ent[0], "a"), (ent[3], "d"), (ent[1], "b"), (ent[2], "cc")], rt=1.4, copia=True, nota="C2a: o determinante abre por mapa")
        degrau(self, "C2a", "= y·(1/x) − x·(−y/x²)")
        self.gat("y sobre x mais")
        D1 = cad(self, D1, [("e", "="), ("p", r"\dfrac{y}{x}"), ("m", "+"), ("q", r"\dfrac{y}{x}")], [("^a", "p"), ("^d", "p"), ("^cc", "q")], n=7, nota="y/x + y/x")
        self.gat("dois y sobre x")
        D1 = cad(self, D1, [("e", "="), ("r", r"\dfrac{2y}{x}")], [("^p", "r"), ("^q", "r")], n=7, nota="= 2y/x")
        self.gat("dá dois v")
        D1 = cad(self, D1, [("e", "="), ("r", r"2\V")], [("^r", "r")], n=7, nota="o y/x vira v: = 2v")
        Dv = linha(self, [("a", r"\dfrac{y}{x}"), ("e", "="), ("b", r"\V")], 30, gap=14)
        degrau(self, "C2a", "= y/x + y/x = 2y/x = 2v")
        self.gat("ir e voltar")
        sobe_col(self, [P1, s1, P2b, s2, dz], y0=200)              # v2 §4.1: a coluna maior não cabe; os passos 1 e 2 saem e a conta sobe
        R1 = linha(self, [("vt", r"\dfrac{\partial(x,y)}{\partial(\U,\V)}"), ("c", r"\cdot"), ("ida", r"\dfrac{\partial(\U,\V)}{\partial(x,y)}"), ("e", "="), ("um", "1")],
                   32, gap=22, voos=[(G(P3, ix_(P3, "D")), "ida")])
        sel_ = T("IR E VOLTAR = NÃO FAZER NADA", self.colX, pxof(R1.get_bottom())[1] + 40, 26, "left", MEN)
        self.pena(sel_)
        self.colms.append(sel_)
        self.colY = pxof(sel_.get_bottom())[1]
        self.gat("pela regra da cadeia")
        R2 = LL([("vt", r"\dfrac{\partial(x,y)}{\partial(\U,\V)}"), ("c", r"\cdot"), ("dv", r"2\V"), ("e", "="), ("um", "1")], pxof(R1.get_left())[0], pxof(R1.get_center())[1], 32)
        gmap(self, 8, R1, R2, [("vt", "vt"), ("c", "c"), ("e", "e"), ("um", "um")], voos=[(G(D1, ix_(D1, "r")), "dv")], rt=1.2, copia=False,
             nota="C2a: o determinante da ida (2v) entra no lugar dele")
        _troca_col(self, R1, R2)
        self.gat("um sobre dois v e")
        J1 = linha(self, [("J", "J"), ("e", "="), ("f", r"\Jl{\dfrac{1}{2\V}}")], 36, gap=24, escreve=False)
        gmap(self, 8, R2, J1, [("vt", "J"), ("e", "e"), ("um", sel(J1, "f")[:1]), ("dv", sel(J1, "f")[2:])], rt=1.4, copia=True,
             nota="C2a: o 2v atravessa a igualdade e vira denominador: J = 1/(2v)")
        degrau(self, "C2a", "J = 1/(2v)")
        cel = poly_px([v.px(*p) for p in [(1.06, 1.20), (1.12, 1.27), (1.17, 1.21), (1.10, 1.14)]], LIMA, 1.0, z=6)
        lcel = TP(r"\approx\Jl{\dfrac{1}{2\V}}\,\Delta\U\,\Delta\V", *v.px(1.98, .98), 26, "l")
        la = T("ÁREA", pxof(lcel.get_left())[0] - 18, pxof(lcel.get_center())[1] + 9, 26, "right", LIMA)
        self.play(FadeIn(cel), run_time=0.4)
        self.pena(la, lcel, lag=0.1)
        self.gat("o módulo é o mesmo")
        J1 = cad(self, J1, [("q", r"\qquad"), ("m", r"|J|=\Jl{\dfrac{1}{2\V}}\enspace(\V>0)")], [("^f", "m")], n=8, nota="|J| = 1/(2v)")
        self.marca("04_E2-2")
        self._fecha(antes=0.6)

        # ═══ E2-3 · a área e a pipa (alvo 05) ═══
        self.an("E2-3")
        chJ = chip(self, r"|J|=\Jl{\dfrac{1}{2\V}}", 1100, 175, de=G(J1, ix_(J1, "m")).copy())
        q = VQ
        EQ = eixos_q(q)
        QD = quadrado(q)
        bq = lin_px([q.px(*p) for p in [(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)]], GEO, 3, z=5)
        gq = papel_tela(q)
        pronto(*EQ["todos"])
        sai = palco_sai(self, keep=[RR_])
        limpa_col(self)
        self.play(*[FadeOut(m) for m in sai + [self.grade]], ReplacementTransform(RR_, QD), FadeIn(gq), Create(bq), *[FadeIn(m) for m in EQ["todos"]], run_time=1.0)
        self.remove(*sai)
        self.grade = gq
        self.colX, self.colY = 1200, 250
        self.gat("virou um quadrado")
        lB = TP(r"B_{uv}", *q.px(1.5, 1.5), 30, "c")
        self.pena(lB)
        self.gat("a área é a integral")
        A1, rA = linha(self, [("e", "="), ("i1", r"\int_1^2"), ("i2", r"\!\!\int_1^2"), ("j", r"\Jl{\dfrac{1}{2\V}}"), ("d", r"\,\du\,\dv")], 36, rot="ÁREA", rot_cor=BR,
                       escreve=False)
        l1_, h1_ = lims(A1, "i1")
        l2_, h2_ = lims(A1, "i2")
        self.pena(rA)
        escreve_seq(self, A1, [(EQ["tk"][2][1], l1_), (EQ["tk"][3][1], h1_), (EQ["tk"][0][1], l2_), (EQ["tk"][1][1], h2_), (chJ.m, ix_(A1, "j"))], rt_voo=0.8)
        origem(self, "limites 1, 2 (C2b)", "marcas dos eixos u e v do quadrado; |J| do chip")
        self.gat("a de dentro é em u")
        palavra(self, "DE DENTRO", GEO, 26, gap=16)
        D2 = linha_de(self, A1, [("f", r"\dfrac{1}{2\V}"), ("c", r"\Big[\U\Big]_1^2")], [("j", "f"), ("i2", "c"), ("d", "c")], n=9, size=36, gap=12,
                      nota="C2b: 1/(2v) sai; [u]₁²")
        self.gat("comprimento do quadrado")
        D2 = cad(self, D2, [("e", "="), ("f", r"\dfrac{1}{2\V}"), ("p", r"(2-1)")], [("^f", "f"), ("^c", "p")], n=9, nota="(2 − 1)")
        self.gat("Fica só um sobre dois v")
        D2 = cad(self, D2, [("e", "="), ("r", r"\dfrac{1}{2\V}")], [("^f", "r")], n=9, nota="= 1/(2v)")
        degrau(self, "C2b", "(1/(2v))[u]₁² = (1/(2v))(2 − 1) = 1/(2v)")
        self.gat("A de fora é um meio")
        palavra(self, "DE FORA", GEO, 26, gap=16)
        F2 = linha(self, [("h", r"\dfrac{1}{2}"), ("c", r"\Big[\ln\V\Big]_1^2")], 36, gap=12, voos=[(G(D2, ix_(D2, "r")), "h")])
        self.gat("logaritmo de dois menos")
        F2 = cad(self, F2, [("e", "="), ("h", r"\dfrac{1}{2}"), ("p", r"(\ln 2-\ln 1)")], [("^h", "h"), ("^c", "p")], n=9, nota="(ln 2 − ln 1)")
        self.gat("logaritmo de um é zero")
        chL = chip(self, r"\ln 1=0", 1420, 175)
        self.gat("a área é logaritmo")
        F3 = cad(self, F2, [("e", "="), ("r", r"\Me{\dfrac{\ln 2}{2}\approx 0{,}347}")], [("^h", "r"), ("^p", "r")], n=9, desce=True, nota="(ln 2)/2 ≈ 0,347")
        cor_glifos(self, [G(F3, ix_(F3, "r"))], MEN, 0.3)
        degrau(self, "C2b", "(1/2)[ln v]₁² = (1/2)(ln 2 − ln 1) = (ln 2)/2 ≈ 0,347")
        self.gat("liga os quatro cantos")
        # um movimento de câmera: o quadrado volta à região R no palco do alvo 05
        v5 = V5
        R5 = regiao_R(v5)
        g5 = papel_tela(v5)
        B5 = {"u1": curva(v5, cX(lambda X: 1 / X, xs0, 1), LAR, 3), "u2": curva(v5, cX(lambda X: 2 / X, 1, xs1), LAR, 3),
              "v1": curva(v5, [(1, 1), (xs1, xs1)], VAG, 3), "v2": curva(v5, [(xs0, 2 * xs0), (1, 2)], VAG, 3)}
        sx5, sy5, lx5, ly5 = eixos_c(v5, -.04, 1.55, -.04, 2.1)
        tk5 = [tk(v5, "x", 1, r"\Am{1}"), tk(v5, "y", 1, r"\Mg{1}"), tk(v5, "y", 2, r"\Mg{2}")]
        novos5 = [sx5, sy5, lx5, ly5] + [p for t in tk5 for p in t]
        pronto(*novos5)
        sai = palco_sai(self, keep=[QD])
        keep_res = G(F3, ix_(F3, "r"))
        limpa_col(self, keep=[F3])
        tira_chips(self, chL)
        self.play(*[FadeOut(m) for m in sai + [self.grade]], ReplacementTransform(QD, R5), FadeIn(g5), *[Create(B5[k]) for k in B5],
                  *[FadeIn(m) for m in novos5], run_time=1.4)
        self.remove(*sai)
        self.grade = g5
        rA2 = chip(self, r"\dfrac{\ln 2}{2}\approx 0{,}347", 1420, 175, de=keep_res.copy(), some=[F3])
        self.colms = []
        self.colY = 250
        A_, B_, C_, D_ = (1, 1), (xs1, xs1), (1, 2), (xs0, xs1)
        pipa = lin_px([v5.px(*p) for p in [A_, B_, C_, D_, A_]], BR, 2.5, dash=(10, 7), z=7)
        dg1 = lin_px([v5.px(*A_), v5.px(*C_)], BR, 3, z=7)
        dg2 = lin_px([v5.px(*D_), v5.px(*B_)], BR, 3, z=7)
        pts = VGroup(*[ponto_px(*v5.px(*p), BR, 7, z=9) for p in (A_, B_, C_, D_)])
        cl = [rot_m(v5, r"(1,1)", A_, 16, 22, 26, "l"), rot_m(v5, r"(1,2)", C_, 16, -8, 26, "l"), rot_m(v5, r"(\sqrt2,\sqrt2)", B_, 16, 0, 26, "l"),
              rot_m(v5, r"\left(\dfrac{1}{\sqrt2},\sqrt2\right)", D_, -14, 0, 26, "r")]
        self.play(FadeIn(pts), Create(pipa), run_time=0.8)
        self.pena(*cl, lag=0.05)
        TT = [linha(self, [t_], 30, gap=14) for t_ in (r"(1,1)\to(1,1)", r"(1,2)\to\left(\dfrac{1}{\sqrt2},\sqrt2\right)", r"(2,1)\to(\sqrt2,\sqrt2)", r"(2,2)\to(1,2)")]
        self.gat("uma mede um")
        n1 = rot_m(v5, "1", (1, 1.72), 16, 0, 30, "l")
        self.play(Create(dg1), run_time=0.5)
        self.pena(n1)
        Dg1 = linha(self, [("a", r"2-1"), ("e", "="), ("r", "1")], 30, gap=14)
        self.gat("a outra um sobre raiz de dois")
        n2 = rot_m(v5, r"\dfrac{1}{\sqrt2}", (1.2, xs1), 0, 48, 28, "c")
        self.play(Create(dg2), run_time=0.5)
        self.pena(n2)
        Dg2 = linha(self, [("a", r"\sqrt2-\dfrac{1}{\sqrt2}"), ("e", "="), ("b", r"\dfrac{2-1}{\sqrt2}"), ("e2", "="), ("r", r"\dfrac{1}{\sqrt2}")], 30, gap=14)
        self.gat("diagonal vezes diagonal")
        sobe_col(self, TT, y0=250)
        Pp, rp = linha(self, [("e", "="), ("f", r"\dfrac{1\cdot\dfrac{1}{\sqrt2}}{2}")], 36, rot="PIPA", rot_cor=GEO, escreve=False)
        nf, bf, df = frac_ix(Pp, "f")
        self.pena(rp)
        escreve_seq(self, Pp, [(n1.f, nf[:1]), (n2.f, nf[2:])])
        origem(self, "1 e 1/√2 (PIPA)", "diagonais da pipa (chaves no palco)")
        self.gat("raiz de dois sobre quatro")
        Pp = cad(self, Pp, [("e", "="), ("m", r"\dfrac{1}{2\sqrt2}")], [("^f", "m")], n=9, nota="D9: 1/(2√2)")
        Pp = cad(self, Pp, [("e2", "="), ("r", r"\dfrac{\sqrt2}{4}\approx 0{,}354")], [("^m", "r")], n=9, nota="PIPA = √2/4 ≈ 0,354")
        degrau(self, "C2b", "PIPA = (1·1/√2)/2 = √2/4 ≈ 0,354")
        self.gat("um tiquinho de um")
        fx1 = poly_px([v5.px(*p) for p in cX(lambda X: 1 / X, xs0, 1)] + [v5.px(*D_)], mixh(BG_, MEN, .55), 1.0, z=4)
        fx2 = poly_px([v5.px(*p) for p in cX(lambda X: 2 / X, 1, xs1)], mixh(BG_, AL, .55), 1.0, z=4)
        le_ = placa_t("ENTRA", *v5.px(.62, 1.15), MEN, 26, "r")
        ls_ = placa_t("SAI", *v5.px(1.32, 1.72), AL, 26, "l")
        self.play(FadeIn(fx1), FadeIn(fx2), run_time=0.6)
        self.pena(le_, ls_, lag=0.1)
        self.gat("a pipa chega bem perto")
        Cmp = linha(self, [("a", r"0{,}347\approx 0{,}354")], 36, gap=36, escreve=False)
        voos(self, [(G(rA2.m, list(range(len(rA2.m[0])))[-5:]).copy(), parte(Cmp, sel(Cmp, "a")[:5], "0,347")),
                    (G(Pp, ix_(Pp, "r")[-5:]).copy(), parte(Cmp, sel(Cmp, "a")[-5:], "0,354"))], rt=0.9)
        self.pena(parte(Cmp, sel(Cmp, "a")[5:-5], "≈"))
        self.gat("é uma estimativa")
        est = leg_ao_lado(self, Cmp, "ESTIMATIVA DA PIPA", GEO, 24, 26)
        self.marca("05_E2-3")
        self._fecha(antes=0.6)

        # ═══ E2-4 · a massa e a densidade média ═══
        self.an("E2-4")
        q = VQ
        EQ2 = eixos_q(q)
        pronto(*EQ2["todos"])
        QD2 = quadrado(q)
        gq2 = papel_tela(q)
        mp = mapa_img(q, lambda U, V_: U, 1, 2, 1, 2, lambda t: rampa("#10243A", CI, ((t - 1) / 1) ** .85), n=240, z=2)
        sai = palco_sai(self, keep=[R5])
        limpa_col(self)
        tira_chips(self, rA2)
        self.play(*[FadeOut(m) for m in sai + [self.grade]], ReplacementTransform(R5, QD2), FadeIn(gq2), *[FadeIn(m) for m in EQ2["todos"]], run_time=1.2)
        self.remove(*sai)
        self.grade = gq2
        self.colY = 250
        self.gat("agora a massa")
        lux = rot_m(q, r"\U=xy", (1.5, 2.25), 0, 0, 28, "c")
        self.pena(lux)
        self.play(FadeIn(mp), run_time=0.8)
        M1 = linha(self, [("m", r"\mm"), ("e", "="), ("ii", r"\iint_R"), ("xy", "xy"), ("d", r"\,dA")], 36)
        self.gat("é o nosso u")
        M2 = linha(self, [("e", "="), ("i1", r"\int_1^2"), ("i2", r"\!\!\int_1^2"), ("u", r"\U"), ("c", r"\cdot"), ("j", r"\Jl{\dfrac{1}{2\V}}"), ("d", r"\,\du\,\dv")],
                   36, gap=16, escreve=False, x=pxof(M1[0][sel(M1, "e")[0]].get_left())[0])
        gmap(self, 10, M1, M2, [("e", "e"), ("ii", "i1"), ("ii", "i2"), ("xy", "u"), ("d", "d")], voos=[(lux.f, "u"), (chJ.m, "j")], rt=1.3, copia=True,
             nota="C2c: xy → u (o rótulo u = xy voa); ∬_R → ∫₁²∫₁²")
        degrau(self, "C2c", "m = ∬_R xy dA = ∫₁²∫₁² u · 1/(2v) du dv")
        self.gat("A de dentro é em u")
        palavra(self, "DE DENTRO", GEO, 26, gap=14)
        vt = ValueTracker(1.5)
        tq_ = always_redraw(lambda: VGroup(tiraH(q, vt.get_value(), 1, 2, h=.05, cor=VAG), *pontos_es(q, (1, vt.get_value()), (2, vt.get_value()))))
        self.add(vt)
        self.play(FadeIn(tq_), run_time=0.4)
        D3 = linha_de(self, M2, [("f", r"\dfrac{1}{2\V}"), ("c", r"\left[\dfrac{\U^2}{2}\right]_1^2")], [("j", "f"), ("u", "c"), ("i2", "c")], n=10, size=34, gap=10,
                      nota="C2c: 1/(2v) sai; [u²/2]₁²")
        self.gat("aplica de um a dois")
        D3 = cad(self, D3, [("e", "="), ("f", r"\dfrac{1}{2\V}"), ("p", r"\left(\dfrac{2^2}{2}-\dfrac{1^2}{2}\right)")], [("^f", "f"), ("^c", "p")], n=10, nota="D11: u²/2 em 2 e em 1")
        self.gat("subtração de frações")
        D3 = cad(self, D3, [("e", "="), ("f", r"\dfrac{1}{2\V}"), ("p", r"\left(\dfrac{4}{2}-\dfrac{1}{2}\right)")], [("^f", "f"), ("^c", "p")], n=10, nota="(4/2 − 1/2)")
        self.gat("sobram três meios")
        D3 = cad(self, D3, [("e", "="), ("f", r"\dfrac{1}{2\V}"), ("c", r"\cdot"), ("t", r"\dfrac{3}{2}")], [("^f", "f"), ("^p", "t")], n=10, nota="· 3/2")
        self.gat("três sobre quatro v")
        D3 = cad(self, D3, [("e", "="), ("r", r"\dfrac{3}{4\V}")], [("^f", "r"), ("^t", "r")], n=10, nota="= 3/(4v)")
        degrau(self, "C2c", "(1/(2v))[u²/2]₁² = (1/(2v))(4/2 − 1/2) = (1/(2v))·3/2 = 3/(4v)")
        sobe_col(self, [M1, M2], y0=250)
        self.gat("A de fora é três quartos")
        palavra(self, "DE FORA", GEO, 26, gap=14)
        # v2 B2 · a tira que varre: a de dentro é a tira (u de 1 a 2); a de fora a leva de v = 1 a v = 2
        self.play(vt.animate.set_value(1.0), run_time=0.6)
        self.play(vt.animate.set_value(2.0), run_time=4.0, rate_func=linear)
        tq_.clear_updaters()
        self.play(FadeOut(tq_), run_time=0.3)
        self.remove(tq_, vt)
        print(f"[varre] {self.lote} E2-4 tira deitada varre v de 1 a 2 em 4,0 s (1 updater)")
        F4 = linha(self, [("h", r"\dfrac{3}{4}"), ("c", r"\Big[\ln\V\Big]_1^2")], 34, gap=10, voos=[(G(D3, ix_(D3, "r")), "h")])
        F4 = cad(self, F4, [("e", "="), ("h", r"\dfrac{3}{4}"), ("p", r"(\ln 2-\ln 1)")], [("^h", "h"), ("^c", "p")], n=10, nota="D11: (ln 2 − ln 1)")
        F4 = cad(self, F4, [("e2", "="), ("h", r"\dfrac{3}{4}"), ("p", r"(\ln 2-0)")], [("^h", "h"), ("^p", "p")], n=10, desce=True, nota="(ln 2 − 0)")
        self.gat("três quartos de logaritmo de dois mais")
        F5 = cad(self, F4, [("e", "="), ("r", r"\Me{\dfrac{3}{4}\ln 2\approx 0{,}520\ \mathrm{kg}}")], [("^h", "r"), ("^p", "r")], n=10, desce=True,
                 nota="(3/4) ln 2 ≈ 0,520 kg")
        cor_glifos(self, [G(F5, ix_(F5, "r"))], MEN, 0.3)
        degrau(self, "C2c", "(3/4)[ln v]₁² = (3/4)(ln 2 − 0) = (3/4) ln 2 ≈ 0,520 kg")
        self.gat("a densidade média")
        chm = chip(self, r"\mm=\dfrac34\ln 2", 1420, 175, de=G(F5, ix_(F5, "r")[:6]).copy())
        limpa_col(self)
        self.colY = 260
        Dm, rd = linha(self, [("e", "="), ("f", r"\dfrac{\mm}{A}"), ("e2", "="), ("g", r"\dfrac{\dfrac34\ln 2}{\dfrac12\ln 2}")], 36, rot="DENSIDADE MÉDIA", rot_cor=BR,
                       escreve=False)
        self.pena(rd)
        escreve_seq(self, Dm, [(G(chm.m, list(range(len(chm.m[0])))[2:]), [i for i in frac_ix(Dm, "g")[0]])])
        self.gat("dividida pela área")
        ng_, bg_, dg_ = frac_ix(Dm, "g")
        lnn = [i for i in ng_ if Dm[0][i].get_center()[0] > Dm[0][bg_[0]].get_center()[0] - .01 and i not in ng_[:3]]
        cancela(self, G(Dm, ng_[-3:]), G(Dm, dg_[-3:]))
        Dm2 = linha(self, [("e", "="), ("g", r"\dfrac{\dfrac34}{\dfrac12}"), ("e2", "="), ("r", r"\Me{\dfrac32}")], 36, gap=20, escreve=False,
                    x=pxof(Dm[0][sel(Dm, "e")[0]].get_left())[0])
        n2_, b2_, d2_ = frac_ix(Dm2, "g")
        gmap(self, 11, Dm, Dm2, [("e2", "e"), (ng_[:3], n2_[:3]), (bg_, b2_), (dg_[:3], d2_[:3])], rt=1.3, copia=True, nota="C2c: os ln 2 acendem e somem → (3/4)/(1/2) = 3/2")
        degrau(self, "C2c", "((3/4) ln 2)/((1/2) ln 2) = (3/4)/(1/2) = 3/2")
        self.gat("bem no meio entre")
        mm_ = lin_px([q.px(1.5, 1), q.px(1.5, 2)], BR, 3, z=7)
        lm_ = leg("MEIO DE 1 E 2", *q.px(1.5, .74), BR, "center", 26)
        self.play(Create(mm_), run_time=0.5)
        self.pena(lm_)
        ok_ao_lado(self, Dm2)
        self.gat("o jacobiano só depende")
        self.leitura(chJ.m, rt=1.0)
        self.marca("E2-4", agora=True)
        self.sai_fim()
