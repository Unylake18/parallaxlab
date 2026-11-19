"""Lote PD1 · D1 MESMA FÓRMULA, DOIS FILMES · v2 (alvos v2_d1q, v2_d1r, v2_d1c + 04–06 v1). Tudo com origem (R11): a reta por φ(u, 0) = (u + 0, u − 0)
= (u, u); cada canto por substituição com o 1 e o 0 voando do rótulo do canto; lado ℓ = √(1² + 1²) = √2 e área (√2)² = 2; o círculo por quatro glyph
maps (x² + y² = (u + v)² + (u − v)², abre os quadrados, cancela ±2uv, funde); o campo com F(x, 0) = (x, x) e F(0, y) = (y, −y)."""
from alg30 import *  # noqa: F401,F403

VL = VB(BE, 408, 540, 140)
VR = VB(BD, 1260, 540, 140)
PHI = lambda u, v: (u + v, u - v)
CANTOS = [(0, 0), (1, 0), (1, 1), (0, 1)]
DL_ = [(-.3, -.3), (.3, -.3), (.3, .3), (-.3, .3)]
DR_ = [(-.35, 0), (0, .38), (.38, 0), (0, -.38)]
U, V_, AM, MG = r"\Uu", r"\Vv", r"\Am", r"\Mg"


def eixos30(v, a, b, c, d, al=.55):
    return VGroup(vlinha(v, [(a, 0), (b, 0)], GEO, 2, alpha=al), vlinha(v, [(0, c), (0, d)], GEO, 2, alpha=al)).set_z_index(2)


def rotulo_n(n, v, p, d):
    g = num_circ(n, BR, 44)
    g.move_to(PX(*canto_xy(v, p[0] + d[0], p[1] + d[1])))
    return VGroup(placa7(g, 6, 4), g).set_z_index(26)


def phi_lin(a, b, y=945, x=1440, res=None):
    """φ(a, b) = (a + b, a − b) [= res] com chaves estáveis (as peças variáveis têm chave própria)."""
    p = [("phi", r"\varphi("), ("a", a), ("vg", ","), ("b", b), ("ab", ")=("), ("a2", a), ("mais", "+"), ("b2", b), ("vg2", r",\ "),
         ("a3", a), ("menos", "-"), ("b3", b), ("fc", ")")]
    if res:
        p.append(("res", res))
    return L(p, x, y, 36, "c")


class LoteD1(Base):
    def corpo(self):
        # ── D1-1 · enunciado: layout B com os eixos e o quadrado já no painel esquerdo ──
        self.an("D1-1")
        self.secao("MESMA FÓRMULA, DOIS FILMES")
        zera_chapas()
        pe, pd = chapa_px(*BE, nome="D1 painel esq.", v=VL), chapa_px(*BD, nome="D1 painel dir.", v=VR)
        ee, ed = eixos30(VL, -1.8, 2.8, -2.4, 2.4), eixos30(VR, -1.1, 3.6, -2.4, 2.4)
        qe = Pedaco(VL, CANTOS, n=4, k=30)
        pts_e = [ponto7(VL.c2p(*p), POS, 8, 12) for p in CANTOS]
        nums_e = [rotulo_n(i + 1, VL, p, d) for i, (p, d) in enumerate(zip(CANTOS, DL_))]
        troca(self, "A → D1 (layout B com o quadrado; entra o canto)")
        self.play(FadeIn(pe), FadeIn(pd), Create(ee), Create(ed), FadeIn(qe), *[FadeIn(VGroup(a, b)) for a, b in zip(pts_e, nums_e)], run_time=0.8)
        phi = L([("phi", r"\varphi("), ("a", U), ("vg", ","), ("b", V_), ("ab", ")=("), ("a2", U), ("mais", "+"), ("b2", V_), ("vg2", r",\ "),
                 ("a3", U), ("menos", "-"), ("b3", V_), ("fc", ")")], 480, 945, 36, "c")
        self.gat("na primeira coordenada")
        escreve(self, phi, 0.3)
        n1 = legenda("ONDE VOCÊ ESTÁ (u, v)", 480, 868, GEO, "center", 28, up=False)
        n2 = legenda("ONDE VAI PARAR (x, y)", 1440, 868, GEO, "center", 28, up=False)
        self.gat("no plano da esquerda")
        self.play(FadeIn(n1, shift=0.05 * UP), run_time=0.4)
        self.gat("no da direita")
        self.play(FadeIn(n2, shift=0.05 * UP), run_time=0.4)
        itens = legenda("RETA · QUADRADO · CÍRCULO", 1440, 955, GEO, "center", 32)
        self.gat("três itens")
        self.play(FadeIn(itens, shift=0.05 * UP), run_time=0.4)
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.ate(1.0)

        # ── D1-2 · a reta: φ(u, 0) = (u + 0, u − 0) = (u, u) ──
        self.an("D1-2")
        eu = vlinha(VL, [(-1.6, 0), (2.6, 0)], AMB, 5).set_z_index(6)
        self.gat("o eixo horizontal da esquerda")
        self.play(Create(eu), run_time=0.6)
        v0 = rot(r"\Vv = 0", *canto_xy(VL, 2.1, .35), 32)
        self.gat("onde o segundo número é zero")
        self.add(v0[0])
        escreve(self, v0.f, 0.4, rt=0.5)
        r0 = phi_lin(U, MG + "{0}")
        zero = v0.f[0][-1]
        self.play(FadeOut(itens), run_time=0.3)
        self.remove(itens)
        gm(self, phi, r0, rt=0.8, copia=True, voos={"b": zero, "b2": zero, "b3": zero})
        r1 = L([("phi", r"\varphi("), ("a", U), ("vg", ","), ("b", MG + "{0}"), ("ab", ")=("), ("a2", U), ("vg2", r",\ "), ("a3", U), ("fc", ")")], 1440, 945, 36, "c")
        self.gat("aí a soma e a diferença")
        tr = cancela(self, r0, "b2", "b3")
        gm(self, r0, r1, rt=0.7, somem=tr)
        seg = vlinha(VL, [(-1, 0), (2.3, 0)], AMB, 5).set_z_index(6)
        diag = vlinha(VR, [(-1, -1), (2.3, 2.3)], AMB, 5).set_z_index(6)
        yx = rot(r"\Y = \X", *canto_xy(VR, 2.55, 1.95), 32)
        self.gat("o eixo vai parar na diagonal")
        self.play(TransformFromCopy(seg, diag), run_time=1.0)
        self.add(yx[0])
        voa(self, r1.p("a2", "vg2", "a3"), yx.f, rt=0.6)
        self.ate(1.0)

        # ── D1-3 · os cantos (alvo v2_d1q), o lado e a área (alvo 04 v1) ──
        self.an("D1-3")
        IM = [PHI(*p) for p in CANTOS]
        pts_d = [ponto7(VR.c2p(*p), POS, 8, 12) for p in IM]
        nums_d = [rotulo_n(i + 1, VR, p, d) for i, (p, d) in enumerate(zip(IM, DR_))]
        self.gat("a origem fica parada")
        self.play(FadeOut(r1), TransformFromCopy(VGroup(pts_e[0], nums_e[0]), VGroup(pts_d[0], nums_d[0])), run_time=0.8)
        self.remove(r1)
        l10 = rot(r"(\Am1,\,\Mg0)", *canto_xy(VL, 1.35, -.75), 30)
        self.gat("o canto um zero a soma")
        self.add(l10[0])
        escreve(self, l10.f, 0.4, rt=0.5)
        um, ze = l10.f[0][1], l10.f[0][3]
        s1 = phi_lin(AM + "{1}", MG + "{0}")
        gm(self, phi, s1, rt=0.8, copia=True, voos={"a": um, "a2": um, "a3": um, "b": ze, "b2": ze, "b3": ze})
        nota = legenda("O 1 E O 0 VOAM DO CANTO; O (1, 1) VOA PARA A DIREITA", 1440, 1015, GEO, "center", 24)
        s1r = phi_lin(AM + "{1}", MG + "{0}", res=r"=(1,\,1)")
        self.gat("ele vai para um um")
        gm(self, s1, s1r, rt=0.6, extra=[FadeIn(nota)])
        lab11 = rot(r"(1,\,1)", *canto_xy(VR, 1.0, 1.62), 26)
        self.add(lab11[0])
        voa(self, s1r.p("res"), lab11.f, rt=0.7, extra=[TransformFromCopy(VGroup(pts_e[1], nums_e[1]), VGroup(pts_d[1], nums_d[1]))])
        cur = s1r
        for i, (a, b, res, fr) in enumerate(((1, 1, r"=(2,\,0)", "o canto um um vai para"), (0, 1, r"=(1,\,-1)", "e o canto zero um vai para")), start=2):
            nv = phi_lin(AM + "{%d}" % a, MG + "{%d}" % b, res=res)
            self.gat(fr)
            cur = gm(self, cur, nv, rt=0.6)
            self.play(TransformFromCopy(VGroup(pts_e[i], nums_e[i]), VGroup(pts_d[i], nums_d[i])), run_time=0.7)
            print(f"[D1] canto {i + 1}: {CANTOS[i]} → {IM[i]}")
        qd = Pedaco(VR, IM, n=4, k=30)
        lados = vlinha(VR, IM + [IM[0]], CORAL, 4).set_z_index(9)
        self.gat("liga os pontos")
        self.play(Create(lados), FadeOut(nota), run_time=0.7)
        self.play(FadeIn(qd), run_time=0.4)
        self.remove(lados, nota)
        print(f"[D1] área do quadrado: {qe.area():.3f} → {qd.area():.3f} (lado {math.hypot(1, 1):.4f})")
        ll = L([("l", r"\ell^2="), ("a", r"1^2"), ("m", "+"), ("b", r"1^2"), ("res", r"\ \Rightarrow\ \ell=\sqrt2")], 1440, 945, 36, "c")
        self.gat("com lado raiz de dois")
        self.play(FadeOut(cur), run_time=0.3)
        self.remove(cur)
        escreve_p(self, ll, ["l", "m"], 0.4)
        voa(self, lab11.f[0][1], ll.p("a"), rt=0.5)
        voa(self, lab11.f[0][3], ll.p("b"), rt=0.5)
        escreve_p(self, ll, ["res"], 0.4)
        junta(self, ll)
        ar = L([("A", r"\text{área}="), ("res", r"(\sqrt2)^2"), ("r2", "=2")], 1440, 945, 36, "c")
        self.gat("agora é raiz de dois ao quadrado")
        gm(self, ll, ar, rt=0.8)
        ge = giro30(VL, (.5, .5), .3, True, GEO, 3, 14, a0=-.6, a1=PI * 1.15)
        gd = giro30(VR, (1, 0), .42, False, GEO, 3, 14, a0=PI * 1.15, a1=-.6)
        self.gat("olha a ordem dos cantos")
        self.play(Create(ge), Create(gd), run_time=0.5)
        esp = T("ESPELHADO", 1640, 1020, 30, "center", CORAL)
        self.gat("o quadrado foi espelhado")
        self.play(FadeIn(esp, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D1-4 · o círculo (alvo v2_d1r → alvo 05 v1) ──
        self.an("D1-4")
        ang = .6
        ce = VGroup(vcirc(VL, 1, CORAL, 4).set_z_index(6), ponto7(VL.c2p(0, 0), GEO, 6, 8),
                    seta7(VL.c2p(0, 0), VL.c2p(math.cos(ang), math.sin(ang)), GEO, 3, 14).set_z_index(8))
        cd = VGroup(vcirc(VR, SQ2, CORAL, 4).set_z_index(6), ponto7(VR.c2p(0, 0), GEO, 6, 8),
                    seta7(VR.c2p(0, 0), VR.c2p(SQ2 * math.cos(ang), SQ2 * math.sin(ang)), GEO, 3, 14).set_z_index(8))
        lr = rot(r"r", *canto_xy(VL, .25, .45), 32)
        lr2 = rot(r"r\sqrt2", *canto_xy(VR, .2, .75), 32)
        sai = [qe, qd, *pts_e, *nums_e, *pts_d, *nums_d, ar, eu, v0, diag, yx, l10, lab11, ge, gd, esp]
        self.gat("e um círculo em volta da origem")
        self.play(*[FadeOut(m) for m in sai], Create(ce[0]), FadeIn(ce[1]), GrowArrow(ce[2]), run_time=0.8)
        self.remove(*sai)
        self.add(lr[0])
        escreve(self, lr.f, 0.5, rt=0.4)
        P1 = [("xy", r"\X^2+\Y^2"), ("eq", "="), ("q1", r"(\Uu+\Vv)^2"), ("mais", "+"), ("q2", r"(\Uu-\Vv)^2")]
        l1 = L(P1, 960, 940, 36, "c")
        self.gat("soma ao quadrado mais diferença")
        voa(self, phi.p("a2", "mais", "b2"), l1.p("q1"), rt=0.6)
        voa(self, phi.p("a3", "menos", "b3"), l1.p("q2"), rt=0.6)
        self.play(FadeOut(phi), run_time=0.3)
        self.remove(phi)
        escreve_p(self, l1, ["xy", "eq", "mais"], 0.3)
        junta(self, l1)
        EXP = [("e2", "="), ("q1", r"\Uu^2"), ("q1", r"+2\Uu\Vv"), ("q1", r"+\Vv^2"), ("q2", r"+\Uu^2"), ("q2", r"-2\Uu\Vv"), ("q2", r"+\Vv^2")]
        l1b = L(P1 + EXP, 960, 940, 36, "c")
        l1b.ks = ["xy", "eq", "q1", "mais", "q2", "e2", "q1", "q1", "q1", "q2", "q2", "q2"]
        self.gat("abre os dois quadrados")
        gm(self, l1, l1b, rt=1.0)
        l1b.ks = ["xy", "eq", "q1", "mais", "q2", "e2", "u2", "c1", "v2", "u2", "c2", "v2"]
        self.gat("esses termos cruzados se cancelam")
        tr = cancela(self, l1b, "c1", "c2")
        l1c = L(P1 + [("e2", "="), ("u2", r"\Uu^2"), ("v2", r"+\Vv^2"), ("u2", r"+\Uu^2"), ("v2", r"+\Vv^2")], 960, 940, 36, "c")
        gm(self, l1b, l1c, rt=0.8, somem=tr)
        l2 = L([("e3", "="), ("u2", r"2\Uu^2"), ("m", "+"), ("v2", r"2\Vv^2")], 960, 1015, 36, "c")
        self.gat("e sobra duas vezes")
        gm(self, l1c, l2, rt=0.8, copia=True)
        l2c = L([("e3", "="), ("u2", r"2\Uu^2"), ("m", "+"), ("v2", r"2\Vv^2"), ("e4", "="), ("dois", "2("), ("u3", r"\Uu^2"), ("m2", "+"), ("v3", r"\Vv^2"),
                 ("fp", ")"), ("imp", r"\ \Rightarrow\ r^{\prime}=\sqrt2\,r")], 960, 1015, 36, "c")
        l2b = L([("e3", "="), ("u2", r"2\Uu^2"), ("m", "+"), ("v2", r"2\Vv^2"), ("e4", "="), ("dois", "2("), ("u3", r"\Uu^2"), ("m2", "+"), ("v3", r"\Vv^2"), ("fp", ")")],
                l2c.get_left()[0] * 120 + 960, 1015, 36, "l")
        l2b.ks = ["e3", "u2", "m", "v2", "e4", "dois", "u2", "m2", "v2", "fp"]
        gm(self, l2, l2b, rt=0.8)
        self.gat("então a distância até a origem")
        escreve_p(self, l2c, ["imp"], 0.3)
        self.remove(*[m for m in self.mobjects if isinstance(m, VGroup) and len(m) and all(g in l2c[0].submobjects for g in m.submobjects)])
        self.remove(l2b)
        self.add(l2c)
        l2c._origem = "c"
        self.gat("e o círculo vira um círculo")
        self.play(TransformFromCopy(ce, cd), run_time=1.0)
        self.add(lr2[0])
        voa(self, l2c.p("imp"), lr2.f, rt=0.6)
        fin = L([("q1", r"(\Uu+\Vv)^2"), ("mais", "+"), ("q2", r"(\Uu-\Vv)^2"), ("e4", "="), ("dois", "2("), ("u3", r"\Uu^2"), ("m2", "+"), ("v3", r"\Vv^2"), ("fp", ")")],
                960, 962, 42, "c")
        self.gat("e como a área vai com o quadrado")
        funde(self, [l1c, l2c], fin, rt=1.0)
        self.ate(1.0)

        # ── D1-5 · como campo (alvo v2_d1c) ──
        self.an("D1-5")
        zera_chapas()
        chA = chapa_px(*LA, nome="D1 palco A", v=VA)
        cmp = campo30(VA, F1, rmin=0, mmax=5, ctx=True, skip=clar28([(-.25, -.25, .25, .25)]), nome="D1 f₁ (contexto)")
        p0 = ponto7(VA.c2p(0, 0), GEO, 6, 8)
        FF = [("F", r"\F("), ("x", r"\X"), ("vg", ","), ("y", r"\Y"), ("ig", ")=("), ("x2", r"\X"), ("mais", "+"), ("y2", r"\Y"), ("vg2", r",\ "),
              ("x3", r"\X"), ("menos", "-"), ("y3", r"\Y"), ("fc", ")")]
        fF = L(FF, 1120, 300, 42)
        self.gat("agora a mesma fórmula")
        self.limpa_junto()
        troca(self, "D1 layout B → layout A")
        self.play(FadeIn(chA), FadeIn(p0), run_time=0.6)
        escreve(self, fF, 0.3)
        self.gat("você pendura a seta")
        self.play(por_colunas(cmp, 1.0))
        h1 = leg_mix(["NO EIXO HORIZONTAL (y = 0):"], 1124, 390, AMB, "left", 28)
        eixo_h = [s for s in cmp if abs(s._xy[1]) < 1e-6]
        eixo_v = [s for s in cmp if abs(s._xy[0]) < 1e-6]
        self.gat("no eixo horizontal a coordenada vertical")
        self.play(FadeIn(h1, shift=0.05 * UP), recolore(self, eixo_h, lambda s: False), run_time=0.5)
        z0 = h1[0][-3]
        fx = L([*FF[:3], ("y", r"0"), FF[4], FF[5], FF[6], ("y2", "0"), FF[8], FF[9], FF[10], ("y3", "0"), FF[12]], 1120, 450, 36)
        gm(self, fF, fx, rt=0.8, copia=True, voos={"y": z0, "y2": z0, "y3": z0})
        fx2 = L([*FF[:3], ("y", "0"), FF[4], FF[5], FF[6], ("y2", "0"), FF[8], FF[9], FF[10], ("y3", "0"), FF[12], ("r", r"=(\X,\ \X)")], 1120, 450, 36)
        d1 = legenda("AS DUAS COMPONENTES IGUAIS: DIAGONAL", 1124, 510, GEO, "left", 26)
        self.gat("então as duas componentes ficam iguais")
        gm(self, fx, fx2, rt=0.7, extra=[FadeIn(d1)])
        h2 = leg_mix(["NO EIXO VERTICAL (x = 0):"], 1124, 610, MAG, "left", 28)
        self.gat("no eixo vertical a seta é")
        self.play(FadeIn(h2, shift=0.05 * UP), recolore(self, eixo_v, lambda s: False), run_time=0.5)
        z1 = h2[0][-3]
        fy = L([FF[0], ("x", "0"), FF[2], FF[3], FF[4], ("x2", "0"), FF[6], FF[7], FF[8], ("x3", "0"), FF[10], FF[11], FF[12]], 1120, 670, 36)
        gm(self, fF, fy, rt=0.8, copia=True, voos={"x": z1, "x2": z1, "x3": z1})
        fy2 = L([FF[0], ("x", "0"), FF[2], FF[3], FF[4], ("x2", "0"), FF[6], FF[7], FF[8], ("x3", "0"), FF[10], FF[11], FF[12], ("r", r"=(\Y,\ -\Y)")], 1120, 670, 36)
        d2 = leg_mix(["EM CIMA: ", r"$\searrow$", " · EMBAIXO: ", r"$\nwarrow$"], 1124, 730, GEO, "left", 26)
        self.gat("em cima da origem as setas")
        gm(self, fy, fy2, rt=0.7, extra=[FadeIn(d2)])
        self.ate(1.0)

        # ── D1-6 · a pergunta guardada (alvo 06 v1) ──
        self.an("D1-6")
        fF2 = L(FF, 1120, 330, 46)
        lg = legenda("A MESMA FÓRMULA, AGORA COMO CAMPO", 1124, 420, GEO)
        self.gat("e aqui fica uma pergunta")
        self.play(*[FadeOut(m) for m in (h1, fx2, d1, h2, fy2, d2)], recolore(self, cmp, lambda s: False), FadeIn(lg), run_time=0.6)
        self.remove(h1, fx2, d1, h2, fy2, d2)
        gm(self, fF, fF2, rt=0.5)
        ct1, ct2 = T("COMO TRANSFORMAÇÃO:", 1120, 540, 34), T("ÁREA × 2", 1120, 595, 40, cor=CORAL)
        cc1, cc2 = T("COMO CAMPO:", 1120, 700, 34), T("A ÁREA TAMBÉM DOBRA?", 1120, 755, 40, cor=SAIC)
        gp = legenda("GUARDA O PALPITE", 1124, 820, GEO)
        self.gat("como transformação a área dobrou")
        self.play(FadeIn(ct1, shift=0.05 * UP), FadeIn(ct2, shift=0.05 * UP), run_time=0.5)
        self.gat("como campo se a gente soltar")
        self.play(FadeIn(cc1, shift=0.05 * UP), run_time=0.4)
        self.gat("a área dele também dobra")
        self.play(FadeIn(cc2, shift=0.05 * UP), run_time=0.4)
        self.gat("guarda o seu palpite")
        self.play(FadeIn(gp, shift=0.05 * UP), run_time=0.4)
        self.sai_fim()
