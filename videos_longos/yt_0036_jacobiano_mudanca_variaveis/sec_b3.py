"""yt_0036 · B3 · o paralelogramo (alvos 06 e 07). B3-1: a grade de u, v se inclina inteira (um movimento); as setas (2, 1) e (1, 3) voam
para as colunas da matriz; a caixa 3 × 4 e os seis pedaços saindo, cada par levando a sua área para C2; glyph map 2 (12 − 2 − 3 − 2 → 5).
B3-2: a mesma figura com letras e C3 por glyph maps; as células de lados Δu, Δv com 5 Δu Δv e o selo FATOR CONSTANTE.
B3-3: quadrado anti-horário × losango horário, VIROU DE COSTAS, C4, o 1/2 lima voa para o chip; em "Falta a outra" a malha 4 × 4 do B4-1 nasce."""
from j36 import *

VU1, AU1 = Vw(130, 700, 260), (-.1, 1.4, -.1, 1.4)
VX1, AX1 = Vw(800, 900, 160), (-.2, 3.4, -.2, 4.3)
DX2 = -470                                                   # B3-2: o plano x, y anda para a esquerda (layout A)
VX2 = Vw(800 + DX2, 900, 160)
VU3, AU3 = Vw(170, 700, 330), (-.1, 1.3, -.1, 1.3)
VX3, AX3 = Vw(880, 560, 360), (-.1, 1.15, -.65, .65)       # v2: menores, para a coluna em x = 1400 caber no tamanho 40
EMENDA_B31, EMENDA_B33 = 640, 740
VU4, AU4 = Vw(170, 760, 480), (-.05, 1.1, -.05, 1.1)
A_ = ((2, 1), (1, 3))


def malha44(v=VU4):
    return VGroup(*[celula(v, ID, i / 4, (i + 1) / 4, j / 4, (j + 1) / 4, n=1, wb=1.5, fop=.85, N=40) for i in range(4) for j in range(4)])


def plano_b4(sc=None):
    return monta_plano(VU4, AU4, 1.15, 1.15, -.05, -.05, uv=True, ticks=[("x", 1, r"\Uc{1}"), ("y", 1, r"\Vc{1}")])


class PB3(J36):
    ANTES = "A TRANSFORMAÇÃO"

    def corpo(self):
        self.an("B3-1")
        self.secao("O CASO RETO")
        dU = monta_plano(VU1, AU1, 1.45, 1.45, -.1, -.1, uv=True, ticks=[("x", 1, r"\Uc{1}"), ("y", 1, r"\Vc{1}")])
        dX = monta_plano(VX1, AX1, 3.45, 4.35, -.15, -.15)
        gu = VGroup(*[lin_px([VU1.px(k, -.1), VU1.px(k, 1.4)], CU, 1.5, .5, z=-9) for k in (0, 1)],
                    *[lin_px([VU1.px(-.1, k), VU1.px(1.4, k)], CVV, 1.5, .5, z=-9) for k in (0, 1)])
        cU = celula(VU1, ID, 0, 1, 0, 1, wb=3)
        aU = VGroup(seta_px(VU1.px(0, 0), VU1.px(1, 0), CU, 5), seta_px(VU1.px(0, 0), VU1.px(0, 1), CVV, 5))
        fu = familia(VX1, ID, range(-2, 4), "u", AX1, CU, 1.3, .4, todas=True)
        fv = familia(VX1, ID, range(-1, 5), "v", AX1, CVV, 1.3, .4, todas=True)
        cX = celula(VX1, ID, 0, 1, 0, 1, wb=3)
        self.fundo(VU1, VX1, emenda=EMENDA_B31)
        self.play(FadeIn(dU["g"]), FadeIn(dX["g"]), *[GrowFromPoint(d[k], d["v"].P(0, 0)) for d in (dU, dX) for k in ("sx", "sy")],
                  *[Create(t[0]) for t in dU["tk"]], FadeIn(gu), FadeIn(fu), FadeIn(fv), run_time=0.9)
        self.pena(dU["lx"], dU["ly"], *[t[1] for t in dU["tk"]], dX["lx"], dX["ly"], lag=0.05)
        entra_cel(self, cU, cX, rt=0.8, extra=[GrowFromPoint(aU[0], VU1.P(0, 0)), GrowFromPoint(aU[1], VU1.P(0, 0))])
        ps, pl = phi_seta(520, 700, 330)
        self.gat("dois u mais vê")
        fphi = TC(r"\varphi(\uu,\vv)=(2\uu+\vv,\;\uu+3\vv)", 130, 960, 36, "l")
        self.play(Create(ps), run_time=0.5)
        self.pena(pl, fphi, lag=0.3)
        # a grade inteira se inclina (um movimento)
        self.gat("retas viram retas")
        o = VX1.P(0, 0)
        self.play(familia_anim(VX1, fu, lin_mix(A_), AX1, rt=2.4), familia_anim(VX1, fv, lin_mix(A_), AX1, rt=2.4),
                  ApplyMatrix(np.array([[2, 1], [1, 3]]), cX, about_point=o), run_time=2.4)
        self.gat("vai para dois, um")
        s21 = seta_px(VX1.px(0, 0), VX1.px(2, 1), CU, 5, z=9)
        # v2 Q04: (2, 1) e (1, 3) fora da caixa 3 × 4, do lado de fora da ponta (na direção da seta), com placa e 14 px de folga
        l21 = rot_v(VX1, r"\Uc{(2,1)}", (2, 0), 0, 34, 26, "c")      # fora da caixa, sob a ponta (abaixo do eixo x)
        self.play(GrowFromPoint(s21, o), run_time=0.7)
        self.pena(l21)
        self.gat("o lado do vê vai")
        s13 = seta_px(VX1.px(0, 0), VX1.px(1, 3), CVV, 5, z=9)
        l13 = rot_v(VX1, r"\Vc{(1,3)}", (4 / 3, 4), 0, -14 - 14, 26, "c")
        self.play(GrowFromPoint(s13, o), run_time=0.7)
        self.pena(l13)
        # as setas voam para as colunas da matriz
        self.gat("as colunas da matriz")
        Mx = Lp([("M", r"\begin{bmatrix}\Uc{2}&\Vc{1}\\\Uc{1}&\Vc{3}\end{bmatrix}")], 1420, 260, 44)
        cs = casas(Mx, Mx._ix["M"], 2, 2)
        self.pena(parte(Mx, cs["del"], "colchetes"))
        voos(self, [(s21.copy(), parte(Mx, cs[(0, 0)] + cs[(1, 0)], "col 1")), (s13.copy(), parte(Mx, cs[(0, 1)] + cs[(1, 1)], "col 2"))], rt=1.2)
        self.gat("nas derivadas parciais")
        molM = moldura(esq(Mx) - 14, pxof(Mx.get_top())[1] - 10, larg(Mx) + 28, Mx.height * 120 + 20, GEO, .6, 1.5, 8)
        self.play(Create(molM), run_time=0.6)
        # a caixa 3 × 4 e os seis pedaços
        self.gat("numa caixa de três")
        caixa = lin_px([VX1.px(0, 0), VX1.px(3, 0), VX1.px(3, 4), VX1.px(0, 4), VX1.px(0, 0)], GEO, 2, dash=(8, 8), z=5)
        pz = lambda pts, c: poligono(VX1, pts, mixh(BG_, c, .28), 1.0, mixh(BG_, c, .7), 1.5, z=1)
        pares = [[pz([(0, 0), (2, 0), (2, 1)], GEO), pz([(1, 3), (3, 4), (1, 4)], GEO)],
                 [pz([(0, 0), (1, 3), (0, 3)], GEO), pz([(2, 1), (3, 1), (3, 4)], GEO)],
                 [pz([(0, 3), (1, 3), (1, 4), (0, 4)], AL), pz([(2, 0), (3, 0), (3, 1), (2, 1)], AL)]]
        # v2 C2 (forma O2): cada pedaço mostra a ORIGEM (catetos) antes do valor; o valor nasce por glyph map no próprio pedaço (M1)
        nums = [[(1.4, .3), (1.6, 3.7)], [(.33, 2.1), (2.72, 1.9)], [(.5, 3.5), (2.5, .5)]]
        ori = [r"\dfrac{2\cdot 1}{2}", r"\dfrac{1\cdot 3}{2}", r"1\cdot 1"]
        val = ["1", r"\dfrac{3}{2}", "1"]
        nm = [[Lp([("o", r"\Ge{%s}" % ori[k])], *VX1.px(a, b), 26, "c") for a, b in par] for k, par in enumerate(nums)]
        self.play(Create(caixa), *[FadeIn(p) for par in pares for p in par], run_time=1.0)
        col = self.col = Coluna36(self, 1396, 380)
        # a CAIXA quebra no segundo = (não cabe antes de x = 1872 com o tamanho 40)
        c1t, c1 = mixLp("CAIXA:", [("p", r"(2+1)(1+3)"), ("e", r"=3\cdot 4")], 1396, 0, 40)
        y1 = col.y_prox(c1)
        g1 = VGroup(c1t, c1)
        g1.shift(UP * (PX(0, y1)[1] - c1.get_center()[1]))
        col.registra(c1)
        self.pena(c1t, c1, lag=0.2)
        c1b = Lp([("e2", "="), ("r", "12")], 0, 0, 40)
        col.poe(c1b, x=eq_x(c1, "e"))
        c1b._xy = (esq(c1b), centro(c1b)[1])
        self.pena(c1b)
        linhas = []
        for k, (gg, t_, r_) in enumerate((("um de área cada", ori[0], r"=-2"), ("um e meio de área cada", ori[1], r"=-3"),
                                          ("um por um", r"(1\cdot 1)", r"=-2"))):
            self.gat(gg)
            self.pena(*[q for q in nm[k]], lag=0.1,                          # a origem escrita nos dois pedaços (catetos), que acendem juntos
                      extra=[p[0].animate.set_fill(mixh(BG_, AL if k == 2 else GEO, .55)) for p in pares[k]])
            m = Lp([("m", r"-\,2\cdot"), ("t", t_), ("r", r_)], 1396, 0, 40)
            col.poe(m)
            m._xy = (1396, centro(m)[1])
            # o 2 voa do par (os dois pedaços); a fração voa de um deles; o resultado pela caneta
            dois = [m._ix["m"][1]]
            vy = [(1330, centro(m)[1])]                                     # pela margem da coluna, entrando na própria linha
            self.escreve_voos(m, [(VGroup(*[q[0] for q in nm[k]]), dois, vy), (nm[k][1], "t", vy)], depois=["r"], rt=0.5)
            # no pedaço, a origem vira o valor (glyph map, no lugar, os dois pedaços juntos): 2·1/2 → 1 · 1·3/2 → 3/2 · 1·1 → 1
            MV = [[([2], [0])], [([2], [0]), ([3], [1]), ([4], [2])], [([0, 2], [0])]]
            ans, novos = [], []
            for j, q in enumerate(nm[k]):
                v_ = Lp([("v", r"\Ge{%s}" % val[k])], *pxof(q.get_center()), 30, "c")
                v_.move_to(q.get_center())
                ja_escrita(v_)
                v_._esc = True                                            # nasce pelo mapa, não pela caneta
                ent = [(sel(q, a), sel(v_, b)) for a, b in MV[k]]
                ans.append(TransformByGlyphMap(q, v_, *ent, auto_fade=True, run_time=0.45))
                GM_LOG.append((self.lote, self._aid, round(self.t, 2), q._tex, v_._tex))
                print(f"[gm] {self.lote} {self._aid} {self.t:.2f} pares={len(ent)} M1 C2 pedaço {k + 1}.{j + 1} :: {q._tex[:60]!r} → {v_._tex[:70]!r}")
                print(f"[linha] {self.lote} {self._aid} {(self.nq - self._q0) / FPS:6.2f}s gm {v_._tex!r}")
                novos.append(v_)
            self._gm_par = frozenset({id(y) for g in nm[k] + novos for y in g.get_family()})
            self.play(*ans, run_time=0.45)
            self._gm_par = None
            self.remove(*nm[k])
            self.add(*novos)
            nm[k] = novos
            self.play(*[FadeOut(p) for p in pares[k]], *[FadeOut(n) for n in nm[k]], run_time=0.2)
            self.remove(*pares[k], *nm[k])
            linhas.append(m)
        # glyph map 2: ÁREA = 12 − 2 − 3 − 2 → 5
        self.gat("doze menos dois")
        c1 = c1b
        t5, F5 = mixLp("ÁREA", [("e", "="), ("a", "12"), ("b", "-2"), ("c", "-3"), ("d", "-2")], 1396, 0, 40)
        y5 = col.y_prox(F5, gap=30)
        VGroup(t5, F5).shift(UP * (PX(0, y5)[1] - F5.get_center()[1]))
        F5._xy = (esq(F5), y5)
        col.registra(F5)
        self.escreve_voos(F5, [(VGroup(*[c1[0][i] for i in c1._ix["r"]]), "a")] +
                          [(VGroup(*[l_[0][i] for i in l_._ix["r"][1:]]), ch) for l_, ch in zip(linhas, ("b", "c", "d"))], rt=0.45, seq=True)   # um por vez, como a fala lê (rápido: a fala lê os quatro em ≈ 1,7 s)
        self.pena(t5)                                   # ÁREA depois dos voos (nenhum voo cruza o rótulo)
        self.gat("menos dois cinco")
        F5 = cresce(self, F5, [("e2", "="), ("r", r"\Lm{5}")], voos=lambda B: [(VGroup(*[F5[0][i] for k_ in "abcd" for i in F5._ix[k_]]).copy(), "r")],
                    nota="2 (12 − 2 − 3 − 2 → 5)")
        self.marca("06", agora=True)

        # ════ B3-2 · o determinante ════
        self.an("B3-2")
        self.secao("O DETERMINANTE")
        fica = [dX["g"], dX["sx"], dX["sy"], dX["lx"], dX["ly"], fu, fv, cX, caixa, s21, s13, l21, l13]
        colC2 = [c1t, c1, *linhas, t5, F5]                      # a conta do B3-1 fica na tela até a primeira linha do C3
        sai = [m for m in self.snap() if m not in fica and m not in colC2 and not any(x in colC2 for x in getattr(m, "submobjects", []))]
        # v2 §1.3: a grade do x, y anda junto com o plano (uma versão mais larga, para não deixar liso à direita) e depois faz crossfade
        gE = papel(VU1, area=area_px(VU1, 0, EMENDA_B31))
        gD = papel(VX1, area=area_px(VX1, EMENDA_B31, 1920 - DX2))
        self.fundo(g=VGroup(gE, gD).set_z_index(-10), rt=0)
        self.play(*[FadeOut(m) for m in sai], FadeOut(gE), *[m.animate.shift(RIGHT * DX2 / 120) for m in fica], gD.animate.shift(RIGHT * DX2 / 120),
                  run_time=0.8)
        self.remove(*sai)
        self.fundo(VX2, rt=0.3)
        self.gat("agora com letras")
        la = rot_v(VX2, r"(\Uc{a},\Uc{c})", (2, 1), 30, 26, 26, "l")
        lb = rot_v(VX2, r"(\Vc{b},\Vc{d})", (-.1, 3), -6, 0, 26, "r")
        self.play(FadeOut(l21), FadeOut(l13), run_time=0.3)
        self.remove(l21, l13)
        self.pena(la, lb, lag=0.2)
        CX = 1000                                               # v2: coluna do C3 em x = 1000 (a linha 1 tem ~790 px no tamanho 40)
        col = self.col = Coluna36(self, CX, 240)
        self.gat("a caixa é á mais")
        corta(self, *colC2, *[m for m in self.snap() if pxof(m.get_center())[0] > 1390])
        # C3.1
        q1t, Q1 = mixLp("ÁREA", [("e", "="), ("p", r"(\Uc{a}+\Vc{b})(\Uc{c}+\Vc{d})"), ("t1", r"-2\cdot\dfrac{\Uc{a}\Uc{c}}{2}"),
                                ("t2", r"-2\cdot\dfrac{\Vc{b}\Vc{d}}{2}"), ("t3", r"-2\cdot\Vc{b}\Uc{c}")], CX, 0, 40)
        y_ = col.y_prox(Q1)
        VGroup(q1t, Q1).shift(UP * (PX(0, y_)[1] - Q1.get_center()[1]))
        Q1._xy = (esq(Q1), y_)
        col.registra(Q1)
        self.pena(q1t, Q1, lag=0.2)
        xe = eq_x(Q1, "e")
        # C3.2 (mapa): 2 · ac/2 → ac — o 2 de cima e o de baixo acendem juntos e somem; idem bd; −2 · bc → −2bc
        t1, t2, t3 = Q1._ix["t1"], Q1._ix["t2"], Q1._ix["t3"]
        acende(self, (VGroup(Q1[0][t1[1]], Q1[0][t1[6]]), LIMA), (VGroup(Q1[0][t2[1]], Q1[0][t2[6]]), LIMA), rt=0.5)
        Q2 = deriva(self, Q1, [("e", "="), ("p", r"(\Uc{a}+\Vc{b})(\Uc{c}+\Vc{d})"), ("mac", r"-\Uc{a}\Uc{c}"), ("mbd", r"-\Vc{b}\Vc{d}"),
                               ("m2", r"-2\Vc{b}\Uc{c}")],
                    [("e", "e"), ("p", "p"), ([t1[0], t1[3], t1[4]], "mac"), ([t2[0], t2[3], t2[4]], "mbd"), ([t3[0], t3[1], t3[3], t3[4]], "m2")],
                    col, x=xe, nota="M2 C3.2 (2·ac/2 → ac)")
        # C3.3 (mapa do produto aberto): cada letra de (a + b)(c + d) se divide nos dois termos em que aparece
        self.gat("abrindo o produto")
        p = Q2._ix["p"]
        PQ3 = [("e", "="), ("ac", r"\Uc{a}\Uc{c}"), ("pad", r"+\Uc{a}\Vc{d}"), ("pbc", r"+\Vc{b}\Uc{c}"), ("pbd", r"+\Vc{b}\Vc{d}"),
               ("mac", r"-\Uc{a}\Uc{c}"), ("mbd", r"-\Vc{b}\Vc{d}"), ("m2", r"-2\Vc{b}\Uc{c}")]

        def mapa3(B):
            ac, ad, bc, bd = B._ix["ac"], B._ix["pad"], B._ix["pbc"], B._ix["pbd"]
            # final K3: cada glifo de origem vai para UM destino; a segunda cópia de cada letra vem pela caneta
            return [("e", "e"), ([p[1]], [ac[0]]), ([p[3]], [bc[1]]), ([p[6]], [ac[1]]), ([p[8]], [ad[2]]),
                    ([p[2]], [ad[0]]), ([p[7]], [bc[0]]), ("mac", "mac"), ("mbd", "mbd"), ("m2", "m2")]
        Q3 = deriva(self, Q2, PQ3, mapa3, col, x=xe, rt=1.3, nota="M2 C3.3 (produto aberto)")
        # C3.4: os pares ac/−ac e bd/−bd acendem na mesma cor e somem juntos; o mapa fecha os buracos
        # final K4(b): cancelamento em dois tempos — os pares acendem na fala; (1) saem juntos, cada par ao mesmo tempo (0,5 s); (2) logo
        # depois os sobreviventes fecham os buracos NA MESMA LINHA (0,8 s) e o + que sobraria depois do = sai junto: = ad + bc − 2bc
        self.gat("o á cê cancela")
        acende(self, (gl(Q3, "ac"), LIMA), (gl(Q3, "mac"), LIMA), rt=0.5)
        self.gat("o bê dê cancela")
        acende(self, (gl(Q3, "pbd"), CI), (gl(Q3, "mbd"), CI), rt=0.5)
        self.play(*[gl(Q3, k_).animate.set_opacity(0) for k_ in ("ac", "mac", "pbd", "mbd")], run_time=0.5)
        Q4 = Lp([("e", "="), ("ad", r"\Uc{a}\Vc{d}"), ("pbc", r"+\Vc{b}\Uc{c}"), ("m2", r"-2\Vc{b}\Uc{c}")], 0, 0, Q3._size)
        Q4.shift(Q3[0][Q3._ix["e"][0]].get_center() - Q4[0][Q4._ix["e"][0]].get_center())
        Q4._xy = (esq(Q4), centro(Q4)[1])
        for k_ in ("ac", "mac", "pbd", "mbd"):
            for i in Q3._ix[k_]:
                Q3[0][i].set_opacity(0)
        passo(self, Q3, Q4, [("e", "e"), (Q3._ix["pad"][1:], "ad"), ("pbc", "pbc"), ("m2", "m2")], rt=0.8, nota="M2 C3.4 (buracos fecham na linha)")
        col.ls[col.ls.index(Q3)] = Q4
        self.gat("sobra menos bê cê")
        # C3.5: bc − 2bc → −bc
        pb, m2 = Q4._ix["pbc"], Q4._ix["m2"]
        Q5 = deriva(self, Q4, [("e", "="), ("ad", r"\Uc{a}\Vc{d}"), ("mbc", r"-\Vc{b}\Uc{c}")],
                    lambda B: [("e", "e"), ("ad", "ad"), ([m2[0]], [B._ix["mbc"][0]]), ([pb[1], m2[2]], [B._ix["mbc"][1]]),
                               ([pb[2], m2[3]], [B._ix["mbc"][2]])], col, x=xe, nota="M2 C3.5 (bc − 2bc → −bc)")
        self.gat("o determinante da matriz")
        Q5 = cresce(self, Q5, [("e2", "="), ("det", r"\det\begin{bmatrix}\Uc{a}&\Vc{b}\\\Uc{c}&\Vc{d}\end{bmatrix}")],
                    voos=lambda B: [(VGroup(Q5[0][Q5._ix["ad"][0]]).copy(), [casas(B, B._ix["det"][3:], 2, 2)[(0, 0)][0]]),
                                    (VGroup(Q5[0][Q5._ix["ad"][1]]).copy(), [casas(B, B._ix["det"][3:], 2, 2)[(1, 1)][0]]),
                                    (VGroup(Q5[0][Q5._ix["mbc"][1]]).copy(), [casas(B, B._ix["det"][3:], 2, 2)[(0, 1)][0]]),
                                    (VGroup(Q5[0][Q5._ix["mbc"][2]]).copy(), [casas(B, B._ix["det"][3:], 2, 2)[(1, 0)][0]])],
                    col=col, nota="M2 C3.5 (ad − bc = det)")
        self.gat("dois vezes três")
        Q6 = Lp([("e", "="), ("n", r"2\cdot 3-1\cdot 1")], 0, 0, 40)
        col.poe(Q6, x=xe)
        Q6._xy = (esq(Q6), centro(Q6)[1])
        self.pena(Q6)
        Q6 = cresce(self, Q6, [("e2", "="), ("s", "6-1"), ("e3", "="), ("r", r"\Lm{5}")], col=col, nota="C3.5 conferência 6 − 1 = 5")
        ck = check_px(dir_(Q6) + 30, centro(Q6)[1], MEN)
        self.play(Create(ck), run_time=0.4)
        # toda célula da grade: área multiplicada por cinco (v2 Q06: só duas células marcadas, a placa no meio de cada uma)
        self.gat("toda célula da grade")
        cels = VGroup(*[celula(VX2, mapL, a, a + .5, b, b + .5, n=1, wb=2.5) for a, b in ((0, 0), (.5, .5))])
        self.play(FadeOut(cX), *[a for c in cels for a in anim_cel(c)], run_time=1.0)
        self.remove(cX)
        lbs = [TP(r"\Lm{5}\,\Du\,\Dv", *VX2.px(*mapL(a + .25, b + .25)), 26, "c") for a, b in ((0, 0), (.5, .5))]
        self.pena(*lbs, lag=0.15)
        Q7 = mixl([("t", "CÉLULA"), ("m", r"\Du\times\Dv\ \Rightarrow"), ("t", "ÁREA"), ("m", r"=\Lm{5}\,\Du\,\Dv")], CX, 0, 40)
        col.poe(Q7, gap=34)
        self.pena(Q7)
        self.gat("o mesmo em todo lugar")
        sl = selo("FATOR CONSTANTE", CX, pxof(Q7.get_bottom())[1] + 50, LIMA, 26)
        poe_selo(self, sl)
        self.marca("B3-2")

        # ════ B3-3 · o sinal e o módulo ════
        self.an("B3-3")
        self.limpa_tudo()
        self.secao("O SINAL E O MÓDULO")
        dU = monta_plano(VU3, AU3, 1.35, 1.35, -.1, -.1, uv=True)
        dX = monta_plano(VX3, AX3, 1.2, .68, -.1, -.65)
        cU = celula(VU3, ID, 0, 1, 0, 1, wb=3)
        aU = VGroup(seta_px(VU3.px(0, 0), VU3.px(1, 0), CU, 5, z=9), seta_px(VU3.px(0, 0), VU3.px(0, 1), CVV, 5, z=9))
        cX = celula(VX3, mapT, 0, 1, 0, 1, wb=3)
        aX = VGroup(seta_px(VX3.px(0, 0), VX3.px(.5, .5), CU, 5, z=9), seta_px(VX3.px(0, 0), VX3.px(.5, -.5), CVV, 5, z=9))
        ps, pl = phi_seta(650, 820, 330)
        self.fundo(VU3, VX3, emenda=EMENDA_B33)
        self.play(FadeIn(dU["g"]), FadeIn(dX["g"]), *[GrowFromPoint(d[k], d["v"].P(0, 0)) for d in (dU, dX) for k in ("sx", "sy")], Create(ps),
                  *anim_cel(cU), *anim_cel(cX), run_time=1.0)
        self.play(GrowFromPoint(aU[0], VU3.P(0, 0)), GrowFromPoint(aU[1], VU3.P(0, 0)), GrowFromPoint(aX[0], VX3.P(0, 0)),
                  GrowFromPoint(aX[1], VX3.P(0, 0)), run_time=0.6)
        self.pena(dU["lx"], dU["ly"], dX["lx"], dX["ly"], pl, lag=0.05)
        CX3 = 1400
        col = self.col = Coluna36(self, CX3, 250)
        self.gat("de trás para a frente")
        R1 = Lp([("x", r"\X=\dfrac{\uu+\vv}{2},"), ("y", r"\quad\Y=\dfrac{\uu-\vv}{2}")], CX3, 0, 40)
        col.poe(R1)
        self.pena(R1)
        self.gat("as colunas são um meio")
        lu = rot_v(VX3, r"\Uc{\left(\dfrac{1}{2},\dfrac{1}{2}\right)}", (.5, .5), 12, -34, 26, "l")
        lv = rot_v(VX3, r"\Vc{\left(\dfrac{1}{2},-\dfrac{1}{2}\right)}", (.5, -.5), 12, 36, 26, "l")
        self.pena(lu, lv, lag=0.4)
        self.gat("o determinante um meio")
        R2 = Lp([("d", r"\det="), ("a", r"\dfrac{1}{2}"), ("p", r"\cdot"), ("b", r"\left(-\dfrac{1}{2}\right)"), ("m", "-"), ("c", r"\dfrac{1}{2}"),
                 ("q", r"\cdot"), ("e", r"\dfrac{1}{2}")], CX3, 0, 40)
        col.poe(R2)
        R2._xy = (esq(R2), centro(R2)[1])
        self.escreve_voos(R2, [(lu.f, ["a", "e"]), (lv.f, ["b", "c"])])
        # C4 (mapa): (1/2)(−1/2) − (1/2)(1/2) → −1/4 − 1/4 → −1/2 (os 1 se multiplicam no 1, os 2 no 4; o sinal de dentro sai na frente)
        self.gat("menos um quarto menos")
        a_, b_, c_, e_, d_ = R2._ix["a"], R2._ix["b"], R2._ix["c"], R2._ix["e"], R2._ix["d"]

        def mapa4(B):
            q = B._ix["q"]
            return [([d_[3]], "e1"), ([b_[1]], [q[0]]), ([a_[0], b_[2]], [q[1]]), ([a_[1], b_[3]], [q[2]]), ([a_[2], b_[4]], [q[3]]),
                    ("m", [q[4]]), ([c_[0], e_[0]], [q[5]]), ([c_[1], e_[1]], [q[6]]), ([c_[2], e_[2]], [q[7]])]
        R3 = deriva(self, R2, [("e1", "="), ("q", r"-\dfrac{1}{4}-\dfrac{1}{4}")], mapa4, col, x=pxof(R2[0][d_[3]].get_left())[0],
                    nota="M4 C4 (produtos → −1/4 − 1/4)")
        R3 = cresce(self, R3, [("e2", "="), ("r", r"\Al{-\dfrac{1}{2}}")], voos=lambda B: [(gl(R3, "q").copy(), "r")], col=col, nota="4 (−1/4 − 1/4 → −1/2)")
        self.gat("área negativa")
        acende(self, (gl(R3, "r"), AL), rt=0.8)
        self.gat("sentido anti horário")
        cu_ = VU3.px(.5, .5)
        a1 = arco_seta(cu_[0], cu_[1], 80, .4, -PI * 1.2, True)
        lah = leg("ANTI-HORÁRIO", *VU3.px(.5, -.22), GEO, "center", 26)
        self.play(Create(a1), run_time=1.0)
        self.pena(lah)
        self.gat("sentido horário")
        cx_ = VX3.px(.5, 0)
        a2 = arco_seta(cx_[0], cx_[1], 70, PI + .4, -.2, False)
        self.play(Create(a2), run_time=1.0)
        self.gat("virou de costas")
        sl = selo("VIROU DE COSTAS", 1000, 892, AL, 26)
        poe_selo(self, sl)
        self.gat("a área é o módulo")
        r4t, R4 = mixLp("ÁREA", [("e", "="), ("m", r"\left|\Al{-\dfrac{1}{2}}\right|")], CX3, 0, 48)          # linha-chave: ≥ 32 px
        y4 = col.y_prox(R4, gap=40)
        VGroup(r4t, R4).shift(UP * (PX(0, y4)[1] - R4.get_center()[1]))
        R4._xy = (esq(R4), y4)
        col.registra(R4)
        self.escreve_voos(R4, [(gl(R3, "r"), [R4._ix["m"][k] for k in range(1, len(R4._ix["m"]) - 1)])])
        self.pena(r4t)
        pass
        R4 = cresce(self, R4, [("e2", "="), ("r", r"\Lm{\dfrac{1}{2}}")], voos=lambda B: [(VGroup(*[R4[0][k] for k in R4._ix["m"][2:-1]]).copy(), "r")],
                    col=col, nota="4 (|−1/2| → 1/2)")
        self.gat("é o meio do trapézio")
        ch = chip_J()
        self.pena(parte(ch.m, ch.m._ix["J"], "|J| ="), extra=[Create(ch.mol)])        # final K2: a moldura nasce com o |J| =
        voos(self, [(gl(R4, "r").copy(), parte(ch.m, ch.m._ix["h"], "1/2"), [(1848, centro(R4)[1]), (1848, 200)])], rt=1.4)     # sobe pela direita das linhas (≥ 48 px da borda)
        self.remove(ch.m, *getattr(ch.m, "_partes", []))
        self.add(ch)
        self.chipJ = ch
        self.marca("07", agora=True)
        # v2 §6.3: o chip foi mostrado; ele volta para dentro do ÁREA = 1/2 e some (não fica no B4 nem no B5, que falam de outros J)
        self.chipJ = None
        hh = VGroup(*[ch.m[0][i] for i in ch.m._ix["h"]])
        alvo_h = gl(R4, "r")
        par = frozenset({id(y) for g in (R4, r4t) for y in g.get_family()})
        for y in ch.get_family():
            y._par = par
        self.play(FadeOut(ch.mol), *[FadeOut(ch.m[0][i]) for i in ch.m._ix["J"]],
                  hh.animate.move_to(alvo_h.get_center()).match_height(alvo_h), run_time=0.9)
        self.remove(ch)
        # falta a outra: o losango e o quadrado saem e a malha 4 × 4 do B4-1 nasce à esquerda
        self.gat("falta a outra")
        sai = self.snap()
        d4 = plano_b4()
        mm = malha44()
        self.play(*[FadeOut(m) for m in sai], run_time=0.5)
        self.remove(*sai)
        self.fundo(VU4, rt=0.3)
        self.play(FadeIn(d4["g"]), GrowFromPoint(d4["sx"], VU4.P(0, 0)), GrowFromPoint(d4["sy"], VU4.P(0, 0)), *[Create(t[0]) for t in d4["tk"]],
                  LaggedStart(*[FadeIn(c) for c in mm], lag_ratio=0.05), run_time=1.4)
        self.pena(d4["lx"], d4["ly"], *[t[1] for t in d4["tk"]], lag=0.05)
