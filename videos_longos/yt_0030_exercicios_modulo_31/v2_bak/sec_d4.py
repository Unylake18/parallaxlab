"""Lote PD4 · D4 O CAMPO QUE NÃO MELHORA DE PERTO · v2 (alvos v2_d4p, v2_d4q + 15–18 v1). Item a: no palco o ponto a r = 2, θ = 0,6 com r, x, y e o
arco θ, cada peça na palavra que a nomeia; ‖F‖ = (|xy|/r²)·‖(x, y)‖ → |xy|/r → polares → r|sen 2θ|/2 ≤ r/2. ε-δ: a cadeia em quatro pedaços.
Item c: o ponto anda no eixo; F(h, 0) = 0⃗, a derivada pela definição; os zeros voam para J; as quatro medidas pela fórmula-mãe. Item d: F(sx, sy)
com s² cancelando (R14) → s·F; a razão na diagonal. Item e: só a componente P no palco; P = x²y/(x² + y²); o molde do quociente; N′ e D′; a
expansão com R14; y = x dá ½; os pontos nas circunferências. D4-8: ANTES / AGORA com três selos."""
from alg30 import *  # noqa: F401,F403

FUNDO_M = "#141031"
MENTA35 = mix(CAMPO, FUNDO_M, 0.65).to_hex()
Q4 = [((1 / SQ2) * 1.2, (1 / SQ2) * 1.2), (-(1 / SQ2) * 1.2, (1 / SQ2) * 1.2)]
TH, RP = .6, 2.0
QP = (RP * math.cos(TH), RP * math.sin(TH))
dPx_, dPy_, dQx_, dQy_ = r"\Pp_{\Am{x}}", r"\Pp_{\Mg{y}}", r"\Qq_{\Am{x}}", r"\Qq_{\Mg{y}}"


def diagonais(v=VA, box=LA):
    return VGroup(linha_rec(v, [(-4, -4), (4, 4)], box, GEO, 2, .4, dash=(8, 8)), linha_rec(v, [(-4, 4), (4, -4)], box, GEO, 2, .4, dash=(8, 8)))


def rosa_pts(eps, n=400):
    th = np.linspace(0, 2 * PI, n + 1)
    r = eps * np.abs(np.sin(2 * th))
    return np.stack([r * np.cos(th), r * np.sin(th)], 1)


class Rosa(VGroup):
    def __init__(self, v, eps):
        super().__init__()
        self.v = v
        self.ch = VMobject().set_fill(MENTA35, 1).set_stroke(width=0)
        self.bd = VMobject().set_fill(opacity=0).set_stroke(CAMPO2, 2 / 1.2, 1)
        for m in (self.ch, self.bd):
            m._sem_contorno = True
        self.add(self.ch, self.bd)
        self.em(eps)
        self.set_z_index(4)

    def em(self, eps):
        P = [self.v.c2p(*p) for p in rosa_pts(eps)]
        self.ch.set_points_as_corners(P)
        self.bd.set_points_as_corners(P)
        return self


def caixinha(txt_, x, y):
    t = T(txt_, 0, y, 30)
    ck = MathTex(r"\checkmark", font_size=fs(30)).set_color(CAMPO2)
    ck._sem_contorno, ck._origem = True, "legenda"
    g = VGroup(t, ck)
    ck.next_to(t, RIGHT, buff=10 / 120).set_y(t.get_center()[1])
    g.shift(RIGHT * (PX(x, 0)[0] - g.get_center()[0]))
    r = RoundedRectangle(width=g.width + 28 / 120, height=g.height + 22 / 120, corner_radius=8 / 120).move_to(g.get_center())
    r.set_fill(PLACA_V4, 0.9).set_stroke(GEO, 2 / 1.2, 1)
    r._sem_contorno, r._placa = True, True
    return VGroup(r.set_z_index(24), g.set_z_index(25))


def selo(nome, ok, x, y, size=30):
    t = T(nome, 0, y, size)
    mk = MathTex(r"\checkmark" if ok else r"\boldsymbol{\times}", font_size=fs(size)).set_color(CAMPO2 if ok else CORAL)
    mk._sem_contorno, mk._origem = True, "legenda"
    mk.next_to(t, RIGHT, buff=8 / 120).set_y(t.get_center()[1])
    g = VGroup(t, mk)
    return g.shift(RIGHT * (PX(x, 0)[0] - g.get_left()[0]))


def setas_P():
    """Só a componente horizontal P de F₄: setas âmbar horizontais (proporcionais com teto 1,6)."""
    g = VGroup()
    for X in np.arange(-3.5, 3.5001, .5):
        for Y in np.arange(-2.5, 2.5001, .5):
            if math.hypot(X, Y) < .3:
                continue
            f = F4(X, Y)
            if abs(f[0]) < .05:
                continue
            Lu = .42 * min(1, abs(f[0]) / 1.6)
            if Lu * 120 < 6:
                continue
            u = math.copysign(Lu, f[0])
            g.add(seta7(VA.c2p(X - u / 2, Y), VA.c2p(X + u / 2, Y), AMB, 5, 19).set_z_index(3))
    return g


class LoteD4(Base):
    ANTES = "DUAS REGRAS · O TESTE"

    def palco(self, ctx=False, skip=None, mref=1.6, nome="D4 F₄"):
        zera_chapas()
        ch = chapa_px(*LA, nome=f"{nome} palco A", v=VA)
        cp = campoP30(VA, F4, passo=.5, rmin=.3, mref=mref, ctx=ctx, skip=skip, nome=nome)
        return ch, cp

    def corpo(self):
        # ── D4-1 · a fórmula ──
        self.an("D4-1")
        self.secao("O CAMPO QUE NÃO MELHORA DE PERTO")
        ch, cp = self.palco(skip=clar28([(-.2, -2.75, 1.8, -2.25)]))
        o0 = ponto7(VA.c2p(0, 0), POS, 8, 9)
        troca(self, "D3b → D4 (palco)")
        self.play(FadeIn(ch), cresce_campo(cp, 0.8), FadeIn(o0), run_time=0.8)
        FF = L([("F", r"\F=\dfrac{\X\Y}{\X^2+\Y^2}\,(\X,\ \Y)"), ("d0", r",\quad \F(0,0)=\vec0")], 1110, 300, 38)
        self.gat("este campo pega o vetor posição")
        escreve_p(self, FF, ["F"], 0.4)
        self.gat("a gente define a seta como zero")
        escreve_p(self, FF, ["d0"], 0.4)
        junta(self, FF)
        self.ate(1.0)

        # ── D4-2 · o desenho; os itens (alvo 15 v1) ──
        self.an("D4-2")
        dg = diagonais()
        c2 = vcirc(VA, 2, GEO, 2, dash=(8, 8), alpha=.8).set_z_index(5)
        r2 = TXP30("RAIO 2", *canto_xy(VA, .8, -2.55), 24, "center", GEO)
        self.gat("olha o desenho")
        self.play(Create(dg), Create(c2), FadeIn(r2), run_time=0.8)
        l1 = legenda("DIAGONAIS DE SUBIDA: PARA FORA", 1114, 560, GEO)
        l2 = legenda("AS OUTRAS: PARA DENTRO · NOS EIXOS: NENHUMA SETA", 1114, 605, GEO, "left", 26)
        self.gat("nas diagonais de subida")
        self.play(FadeIn(l1, shift=0.05 * UP), run_time=0.4)
        self.gat("nas outras diagonais")
        self.play(FadeIn(l2, shift=0.05 * UP), run_time=0.4)
        it1, it2 = T("ITENS: LIMITE · CONTINUIDADE · PARCIAIS", 1114, 760, 26), T("ZOOM · CLASSE C¹", 1114, 805, 26)
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.play(FadeIn(it1, shift=0.05 * UP), FadeIn(it2, shift=0.05 * UP), run_time=0.5)
        self.ate(1.0)

        # ── D4-3 · item a (alvo v2_d4p) ──
        self.an("D4-3")
        FF2 = L([("F", r"\F=\dfrac{\X\Y}{\X^2+\Y^2}\,(\X,\ \Y)"), ("d0", r",\quad \F(0,0)=\vec0")], 1110, 285, 34)
        self.gat("item a existe limite")
        self.secao("O CAMPO QUE NÃO MELHORA DE PERTO · LIMITE")
        gm(self, FF, FF2, rt=0.6, extra=[FadeOut(VGroup(l1, l2, it1, it2, dg, c2, r2)), *[s.animate.set_color(CTX) for s in cp]])
        self.remove(l1, l2, it1, it2, dg, c2, r2)
        pq = ponto7(VA.c2p(*QP), POS, 9, 12)
        N1 = L([("n", r"\|\F\|="), ("k", r"\dfrac{|\X\Y|}{r^2}"), ("v", r"\,\|(\X,\Y)\|")], 1110, 400, 34)
        self.gat("calcula o tamanho da seta")
        self.play(FadeIn(pq, scale=0.5), run_time=0.3)
        escreve(self, N1, 0.25)
        rr = vlinha(VA, [(0, 0), QP], GEO, 3).set_z_index(8)
        rl = rot("r", *canto_xy(VA, .75, .8), 30)
        N2 = L([("n", r"\|\F\|="), ("k", r"\dfrac{|\X\Y|}{r^2}"), ("v", r"\,r")], 1110, 400, 34)
        self.gat("o vetor posição tem tamanho igual")
        self.play(Create(rr), FadeIn(rl[0]), run_time=0.5)
        escreve(self, rl.f, 0.5, rt=0.3)
        N2b = L([("n", r"\|\F\|="), ("k", r"\dfrac{|\X\Y|}{r^2}"), ("v", r"\,\|(\X,\Y)\|"), ("e1", "="), ("k2", r"\dfrac{|\X\Y|}{r^2}"), ("v2", r"\,r")], 1110, 400, 34)
        gm(self, N1, N2b, rt=0.6, kb=["n", "k", "v", "e1", "k", "v2"], voos={"v2": rl.f})
        N3 = L([("n", r"\|\F\|="), ("k", r"\dfrac{|\X\Y|}{r^2}"), ("v", r"\,\|(\X,\Y)\|"), ("e1", "="), ("k2", r"\dfrac{|\X\Y|}{r^2}"), ("v2", r"\,r"), ("e2", "="), ("f", r"\dfrac{|\X\Y|}{r}")],
               1110, 400, 34)
        self.gat("então a seta tem tamanho igual ao módulo")
        gm(self, N2b, N3, rt=0.6, ka=["n", "k", "v", "e1", "k2", "v2"], kb=["n", "k", "v", "e1", "k2", "v2", "e2", "k2"])
        sx = vlinha(VA, [(0, 0), (QP[0], 0)], AMB, 5).set_z_index(7)
        sy = vlinha(VA, [(QP[0], 0), QP], MAG, 5, dash=(10, 8)).set_z_index(7)
        arc = vlinha(VA, circ_pts(.55, (0, 0), 30, 0, TH), BR, 2).set_z_index(7)
        lx, ly = rot(r"\X", *canto_xy(VA, QP[0] / 2, -.28), 30), rot(r"\Y", *canto_xy(VA, QP[0] + .3, QP[1] / 2), 30)
        lt = TC(r"\theta", *canto_xy(VA, .78, .2), 28, "c")
        self.gat("em polares o produto")
        sob_y = [s for s in cp if hasattr(s, "_xy") and abs(s._xy[0] - 2) < 1e-6 and abs(s._xy[1] - .5) < 1e-6]   # R5: a seta sob o rótulo y
        self.play(Create(sx), Create(sy), Create(arc), FadeIn(lx[0]), FadeIn(ly[0]), *[UpdateFromAlphaFunc(s, lambda m, a: op_seta(m, 1 - a)) for s in sob_y],
                  run_time=0.6)
        clareira(cp, lambda: (lambda X, Y: abs(X - 2) < 1e-6 and abs(Y - .5) < 1e-6))
        ly.f._origem = lt._origem = "a"
        escreve(self, lx.f, 0.5, rt=0.2, extra=[caneta(ly.f, ritmo=0.5), caneta(lt, ritmo=0.5)])
        XY = L([("x", r"\X"), ("cx", r"=r\cos\theta,\qquad "), ("y", r"\Y"), ("cy", r"=r\sen\theta")], 1110, 505, 34)
        voa(self, lx.f, XY.p("x"), rt=0.3, extra=[TransformFromCopy(ly.f, XY.p("y"))])
        escreve_p(self, XY, ["cx", "cy"], 0.3)
        junta(self, XY)
        PP = L([("xy", r"\X\Y"), ("e", "="), ("r2", r"r^2"), ("cs", r"\cos\theta\sen\theta")], 1110, 600, 34)
        self.gat("a distância ao quadrado vezes o cosseno")
        escreve(self, PP, 0.3)
        PP2 = L([("xy", r"\X\Y"), ("e", "="), ("r2", r"r^2"), ("cs", r"\cos\theta\sen\theta"), ("e2", "="), ("r2b", r"r^2\,"), ("s2", r"\dfrac{\sen2\theta}{2}")], 1110, 600, 34)
        self.gat("e cosseno vezes seno é metade")
        gm(self, PP, PP2, rt=0.7, kb=["xy", "e", "r2", "cs", "e2", "r2", "cs"])
        NF = L([("n", r"\|\F\|="), ("f", r"\dfrac{r\,|\sen2\theta|}{2}"), ("le", r"\le\dfrac r2")], 1110, 715, 38)
        NF0 = L([("n", r"\|\F\|="), ("f", r"\dfrac{r\,|\sen2\theta|}{2}")], NF.get_left()[0] * 120 + 960, 715, 38, "l")
        self.gat("então o tamanho da seta é a distância")
        AF = Duas(N3, PP2)
        gm(self, AF, NF0, rt=0.8, copia=True, ka=["n", "x", "x", "x", "x", "x", "x", "f", "x", "x", "x", "x", "x", "x", "f"])
        self.gat("e isso nunca passa da metade")
        escreve_p(self, NF, ["le"], 0.4)
        self.remove(*[m for m in self.mobjects if isinstance(m, VGroup) and len(m) and all(g in NF[0].submobjects for g in m.submobjects)], NF0)
        self.add(NF)
        NF._origem = "c"
        self.ate(1.0)

        # ── D4-4 · ε-δ no layout B (alvo 16 v1) ──
        self.an("D4-4")
        zera_chapas()
        vl, vr = VB(BE, 480, 540, 140), VB(BD, 1440, 540, 140)
        pe, pd = chapa_px(*BE, nome="D4 ε-δ esq.", v=vl), chapa_px(*BD, nome="D4 ε-δ dir.", v=vr)
        ce = campoP30(vl, F4, -2.25, 2.25, -1.75, 2.25, .5, rmin=.3, mref=1, ctx=True,
                      skip=lambda X, Y: abs(math.hypot(X, Y) - 2) < .3 or (-2.35 < X < -.75 and 1.45 < Y < 2.3), nome="D4 ε-δ (contexto)")
        eps = ValueTracker(1.0)
        dc = vcirc(vl, 2, POS, 3).set_z_index(6)
        oe = ponto7(vl.c2p(0, 0), POS, 9, 9)
        de = rot(r"\del = 2\eps", *canto_xy(vl, -1.55, 1.85), 32)
        ne = legenda("ONDE VOCÊ ANDA", 480, 868, GEO, "center", 28)
        ex = VGroup(vlinha(vr, [(-2.4, 0), (2.4, 0)], GEO, 2, alpha=.35), vlinha(vr, [(0, -2.4), (0, 2.4)], GEO, 2, alpha=.35)).set_z_index(2)
        ro = Rosa(vr, 1.0)
        ec = vcirc(vr, 1, CAMPO2, 3).set_z_index(6)
        od = ponto7(vr.c2p(0, 0), GEO, 6, 9)
        el = rot(r"\eps", *canto_xy(vr, .95, 1.0), 34)
        ml = leg_mix(["A MANCHA DAS PONTAS CABE NO DISCO ", r"$\varepsilon$"], 1440, 860, GEO, "center", 26)
        self.gat("agora o desafio do épsilon")
        self.limpa_junto()
        troca(self, "D4 palco → layout B (ε-δ)")
        self.play(FadeIn(pe), FadeIn(pd), cresce_campo(ce, 0.6), FadeIn(oe), FadeIn(ex), FadeIn(od), FadeIn(ne), run_time=0.8)
        self.gat("alguém escolhe um épsilon")
        self.play(Create(ec), FadeIn(el[0]), run_time=0.5)
        escreve(self, el.f, 0.5, rt=0.3)
        CH = L([("a", r"0<\|\Xp\|<\del=2\eps"), ("b", r"\ \Rightarrow\ \|\F(\Xp)\|\le\dfrac{\|\Xp\|}{2}"), ("c", r"<\dfrac{\del}{2}=\eps")], 960, 965, 40, "c")
        self.gat("você responde com delta")
        self.play(Create(dc), FadeIn(de[0]), run_time=0.5)
        escreve(self, de.f, 0.4, rt=0.4)
        escreve_p(self, CH, ["a"], 0.3)
        self.gat("se o ponto está a menos de delta")
        self.play(FadeIn(ro), FadeIn(ml, shift=0.05 * UP), run_time=0.5)
        escreve_p(self, CH, ["b"], 0.25)
        self.gat("ou seja menos que épsilon")
        escreve_p(self, CH, ["c"], 0.3)
        junta(self, CH)
        dc.add_updater(lambda m: m.become(vcirc(vl, 2 * eps.get_value(), POS, 3).set_z_index(6)))
        ro.add_updater(lambda m: m.em(eps.get_value()))
        ec.add_updater(lambda m: m.become(vcirc(vr, eps.get_value(), CAMPO2, 3).set_z_index(6)))
        self.gat("venceu para qualquer épsilon")
        self.play(eps.animate.set_value(.5), run_time=1.2)
        self.play(eps.animate.set_value(1.0), run_time=1.2)
        for m in (dc, ro, ec):
            m.clear_updaters()
        self.ate(1.0)

        # ── D4-5 · item b (caixinhas) e item c (no palco) ──
        self.an("D4-5")
        cx = [caixinha("DOMÍNIO", 620, 985), caixinha("LIMITE", 900, 985), caixinha("IGUAL À SETA", 1220, 985)]
        self.gat("o ponto está no domínio")
        self.play(FadeOut(CH), FadeIn(cx[0]), run_time=0.4)
        self.remove(CH)
        self.gat("o limite existe")
        self.play(FadeIn(cx[1]), run_time=0.4)
        self.gat("e é igual à seta do ponto")
        self.play(FadeIn(cx[2]), run_time=0.4)
        ct = T("CONTÍNUO", 1560, 1000, 40, "center", CAMPO2)
        self.gat("os três pedaços passam")
        self.play(FadeIn(ct, shift=0.05 * UP), run_time=0.4)
        self.secao("O CAMPO QUE NÃO MELHORA DE PERTO")
        ch, cp = self.palco(skip=clar28([(-.2, -2.75, 1.8, -2.25)]), nome="D4 F₄ (item c)")
        o0 = ponto7(VA.c2p(0, 0), POS, 8, 9)
        FF3 = L([("F", r"\F=\dfrac{\X\Y}{\X^2+\Y^2}\,(\X,\ \Y)"), ("d0", r",\quad \F(0,0)=\vec0")], 1110, 285, 34)
        self.gat("item c as derivadas parciais")
        FF3._origem = "lembrança"
        print(f"[origem] lembrança {self.lote} D4-5 {self.t:.2f} {FF3._tex!r} (a fórmula do campo volta ao topo da coluna)")
        self.limpa_junto()
        troca(self, "D4 layout B → palco (item c)")
        self.play(FadeIn(ch), FadeIn(cp), FadeIn(o0), FadeIn(FF3), run_time=0.6)
        pa = ponto7(VA.c2p(-3.4, 0), AMB, 9, 12)
        hl = rot(r"(h,\,0)", *canto_xy(VA, -3.4, -.25), 26)
        FH = L([("F", r"\F(h,0)="), ("k", r"\dfrac{h\cdot0}{h^2}"), ("v", r"(h,0)"), ("z", r"=\vec0")], 1110, 390, 32)
        self.gat("andando pelo eixo horizontal")
        self.play(FadeIn(pa), FadeIn(hl[0]), run_time=0.2)
        escreve(self, hl.f, 0.3, rt=0.2)
        FH._origem = "a"
        self.play(pa.animate.move_to(VA.c2p(3.4, 0)), hl.animate.move_to(PX(*canto_xy(VA, 3.4, -.25))), caneta(FH, ritmo=0.1), run_time=1.0, rate_func=linear)
        DX = L([("d", r"\dfrac{\partial\F}{\dx}(0,0)="), ("lim", r"\lim_{h\to0}\dfrac{\F(h,0)-\F(0,0)}{h}"), ("z", r"=\vec0")], 1110, 480, 32)
        escreve(self, DX, 0.1, rt=0.9)
        J0 = TC(r"J=\begin{pmatrix}\Am{0} & \Mg{0}\\ \Am{0} & \Mg{0}\end{pmatrix}", 1110, 595, 40, caneta=False)
        cel, resto = celulas(J0)
        zx = max(DX.p("z"), key=lambda g: g.height)
        self.play(caneta(resto, ritmo=0.2), TransformFromCopy(zx, cel[(0, 0)]), TransformFromCopy(zx, cel[(1, 0)]), run_time=0.6)
        self.gat("pelo vertical a mesma coisa")
        FV = L([("F", r"\F(0,h)="), ("k", r"\dfrac{0\cdot h}{h^2}"), ("v", r"(0,h)"), ("z", r"=\vec0")], 1110, 390, 32)
        DY = L([("d", r"\dfrac{\partial\F}{\dy}(0,0)="), ("lim", r"\lim_{h\to0}\dfrac{\F(0,h)-\F(0,0)}{h}"), ("z", r"=\vec0")], 1110, 480, 32)
        em_paralelo(self, 0.6, lambda: gm(self, FH, FV), lambda: gm(self, DX, DY), extra=[FadeOut(pa), FadeOut(hl)])
        self.remove(pa, hl)
        zy = max(DY.p("z"), key=lambda g: g.height)
        self.play(TransformFromCopy(zy, cel[(0, 1)]), TransformFromCopy(zy, cel[(1, 1)]), run_time=0.5)
        junta_partes(self, J0)
        J0._origem = "b"
        MD = L([("r", r"\V{\rot}="), ("rf", dQx_ + "-" + dPy_), ("rv", r"=0-0=\V0"), ("sp", r",\quad "), ("d", r"\D{\dv}="), ("df", dPx_ + "+" + dQy_), ("dv", r"=0+0=\D0")],
               1110, 700, 32)
        self.gat("a tabela é toda zero")
        MD2 = L([("a", r"d_1="), ("af", dPx_ + "-" + dQy_), ("av", r"=0-0=\Lm0"), ("sp", r",\quad "), ("b", r"d_2="), ("bf", dQx_ + "+" + dPy_), ("bv", r"=0+0=\Lm0")],
                1110, 770, 32)
        self.play(caneta(MD.p("r", "rf", "sp", "d", "df"), ritmo=0.08), caneta(MD2.p("a", "af", "sp", "b", "bf"), ritmo=0.08), run_time=0.9)
        print(f"[origem] a {self.lote} D4-5 {self.t:.2f} moldes rot/div/d1/d2")
        self.gat("rotacional zero divergente zero")
        voa(self, VGroup(cel[(1, 0)], cel[(0, 1)]), MD.p("rv"), rt=0.5, extra=[TransformFromCopy(VGroup(cel[(0, 0)], cel[(1, 1)]), MD.p("dv"))])
        junta(self, MD, "b")
        self.gat("deformação zero")
        voa(self, VGroup(cel[(0, 0)], cel[(1, 1)]), MD2.p("av"), rt=0.5, extra=[TransformFromCopy(VGroup(cel[(1, 0)], cel[(0, 1)]), MD2.p("bv"))])
        junta(self, MD2, "b")
        pv = legenda("PREVISÃO: PERTO DA ORIGEM, NADA ACONTECE", 1114, 850, GEO, "left", 26)
        self.gat("a previsão seria")
        self.play(FadeIn(pv, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D4-6 · item d: o zoom (alvo 17 v1) ──
        self.an("D4-6")
        zera_chapas()
        pe, pd = chapa_px(*BE, nome="D4 zoom esq.", v=vl), chapa_px(*BD, nome="D4 zoom dir.", v=vr)
        z1 = campoP30(vl, F4, -2.25, 2.25, -1.75, 2.25, .5, rmin=.3, mref=1, nome="D4 zoom × 1")
        peds = [quad30(vr, c, .4) for c in Q4]
        fans = [fantasma(vr, quad_pts(c, .4)) for c in Q4]
        z10 = campoP30(vr, F4, -2.25, 2.25, -1.75, 2.25, .5, rmin=.3, mref=1, nome="D4 zoom × 10")
        st = {"on": False}
        clareira(z10, lambda: ou(*[clar_ped(p, .2) for p in peds], *[dq(c, .4) for c in Q4]) if st["on"] else NADA)
        oz1, oz2 = ponto7(vl.c2p(0, 0), POS, 8, 9), ponto7(vr.c2p(0, 0), POS, 8, 9)
        nz1 = legenda("ZOOM × 1", 480, 868, GEO, "center", 28)
        nz2 = legenda("ZOOM × 10 (MESMO DESENHO)", 1440, 868, GEO, "center", 28)
        nz3 = legenda("ZOOM × 100 (MESMO DESENHO)", 1440, 868, GEO, "center", 28)
        self.gat("item d confere com um zoom")
        self.secao("O CAMPO QUE NÃO MELHORA DE PERTO · ZOOM")
        self.limpa_junto()
        troca(self, "D4 palco → layout B (zoom)")
        self.play(FadeIn(pe), FadeIn(pd), cresce_campo(z1, 0.6), FadeIn(oz1), FadeIn(nz1), run_time=0.8)
        self.gat("deixava as setas arrumadinhas")                  # R16: o zoom × 1 citado acende
        acende(self, [nz1], CAMPO2, 0.8)
        self.gat("aqui olha o zoom de dez vezes")
        self.play(cresce_campo(z10, 0.6), FadeIn(oz2), FadeIn(nz2), run_time=0.6)
        self.gat("e o de cem vezes também")
        troca_linha(self, nz2, nz3)
        HS = L([("F", r"\F(s\X,s\Y)="), ("a", r"\dfrac{", 0), ("s1", r"s^2"), ("n", r"\X\Y"), ("b", "}{", 1), ("s2", r"s^2"), ("d", r"(\X^2+\Y^2)"), ("c", "}", 0),
                ("v", r"\cdot(s\X,\ s\Y)")], 960, 946, 34, "c")
        self.gat("multiplicar a posição por um número")
        escreve(self, HS, 0.2)
        self.gat("o número aparece ao quadrado em cima")
        tr = cancela(self, HS, "s1", "s2", rt=0.25)
        HS2 = L([("F", r"\F(s\X,s\Y)="), ("n", r"\dfrac{\X\Y}{\X^2+\Y^2}"), ("v", r"\,s\,(\X,\ \Y)"), ("r", r"=s\,\F(\X,\Y)")], 960, 946, 34, "c")
        gm(self, HS, HS2, rt=0.7, somem=tr, ka=["F", "x", "x", "n", "n", "x", "n", "x", "v"])
        RZ = L([("a", r"\F(h,h)=(h/2,\,h/2)"), ("b", r"\ \Rightarrow\ \dfrac{\|\text{erro}\|}{\|\Hh\|}=\dfrac{h\sqrt2/2}{h\sqrt2}=\dfrac12")], 960, 1034, 30, "c")
        self.gat("na diagonal a seta tem sempre metade")
        escreve(self, RZ, 0.2)
        self.gat("pelo passo fica em meio")                      # R16: a razão ½ citada acende; depois a razão que teria de ir a zero
        acende(self, [VGroup(*RZ.p("b")[-3:])], AMB, 1.0)
        self.gat("essa razão teria que ir a zero")
        acende(self, [RZ.p("b")], CORAL, 1.0)
        self.gat("tem quadradinho crescendo")
        st["on"] = True
        self.play(*[FadeIn(p) for p in peds], *[FadeIn(f) for f in fans], run_time=0.4)
        a0 = [p.area() for p in peds]
        self.play(*[anda(p, fl4, .6, 2.0, rate=linear, nome=f"D4 zoom quadradinho {i + 1}") for i, p in enumerate(peds)])
        for i, p in enumerate(peds):
            print(f"[D4] quadradinho {Q4[i]}: área {a0[i]:.4f} → {p.area():.4f}")
        self.ate(1.0)

        # ── D4-7 · item e (alvo v2_d4q → alvo 18 v1) ──
        self.an("D4-7")
        self.secao("O CAMPO QUE NÃO MELHORA DE PERTO · CLASSE C¹")
        z10.clear_updaters()
        zera_chapas()
        chE = chapa_px(*LA, nome="D4 item e palco", v=VA)
        sp = setas_P()
        npl = legenda("NO PALCO: SÓ A COMPONENTE HORIZONTAL P", 1124, 850, AMB, "left", 24)
        PQ = L([("P", r"\Pp="), ("k", r"\dfrac{\X\Y}{\X^2+\Y^2}"), ("x", r"\cdot\X"), ("e", "="), ("r", r"\dfrac{\X^2\Y}{\X^2+\Y^2}")], 1110, 290, 36)
        self.gat("item e calcula a derivada")
        self.limpa_junto()
        troca(self, "D4 layout B → palco só com P (item e)")
        self.play(FadeIn(chE), FadeIn(sp), FadeIn(npl), run_time=0.7)
        self.gat("a componente horizontal é o quadrado")
        escreve_p(self, PQ, ["P", "k", "x"], 0.25)
        escreve_p(self, PQ, ["e", "r"], 0.25)
        junta(self, PQ)
        QM = L([("d", r"\dfrac{\partial\Pp}{\dx}="), ("m", r"\dfrac{N^{\prime}D-N\,D^{\prime}}{D^2}"), ("nd", r",\quad N=\X^2\Y,\ \ D=\X^2+\Y^2")], 1110, 405, 32)
        self.gat("regra do quociente")
        escreve_p(self, QM, ["d", "m"], 0.2)
        voa(self, PQ.p("r"), QM.p("nd"), rt=0.5)
        junta(self, QM)
        Q1 = L([("d", r"\dfrac{\partial\Pp}{\dx}="), ("q", r"\dfrac{2\X\Y\,(\X^2+\Y^2)-\X^2\Y\cdot2\X}{(\X^2+\Y^2)^2}")], 1110, 530, 34)
        self.gat("a derivada de cima é duas vezes")
        gm(self, QM, Q1, rt=0.8, copia=True, ka=["d", "q", "q"])
        Q2 = L([("e", "="), ("a", r"\big(2\X^3\Y"), ("b", r"+2\X\Y^3"), ("c", r"-2\X^3\Y\big)"), ("dv", r"/(\X^2+\Y^2)^2")], 1140, 650, 34)
        self.gat("os termos com a quarta potência")
        gm(self, Q1, Q2, rt=0.8, copia=True, ka=["x", "a"], kb=["x", "a", "a", "a", "a"])
        tr = cancela(self, Q2, "a", "c", rt=0.25)
        Q3 = L([("e", "="), ("b", r"2\X\Y^3"), ("dv", r"/(\X^2+\Y^2)^2")], 1140, 650, 34)
        gm(self, Q2, Q3, rt=0.6, somem=tr)
        RES = L([("d", r"\dfrac{\partial\Pp}{\dx}="), ("r", r"\dfrac{2\X\Y^3}{(\X^2+\Y^2)^2}")], 1120, 300, 44)
        RR = (2.5, 1.25, .625)
        ch2, cp2 = self.palco(ctx=True, skip=lambda X, Y: any(abs(math.hypot(X, Y) - r) < .3 for r in RR) or
                              any(math.hypot(X - 2.85 * math.cos(t), Y - 2.75 * math.sin(t)) < .55 for t in (PI / 4, 3 * PI / 4)), nome="D4 F₄ (contexto, item e)")
        circs = [vcirc(VA, r, GEO, 2, alpha=.5).set_z_index(5) for r in RR]
        dP = lambda X, Y: 2 * X * Y ** 3 / (X * X + Y * Y) ** 2
        eixo_p, diag_p = [], []
        for r in RR:
            e_, d_ = [], []
            for k in range(8):
                t = k * PI / 4
                p = (r * math.cos(t), r * math.sin(t))
                v_ = dP(*p)
                (e_ if abs(v_) < 1e-6 else d_).append(ponto7(VA.c2p(*p), GEO if abs(v_) < 1e-6 else AMB, 6 if abs(v_) < 1e-6 else 9, 9))
            eixo_p.append(e_)
            diag_p.append(d_)
        self.gat("agora olha essa derivada")
        AR = Duas(PQ, QM, Q1, Q3)
        AR.ks = ["x"] * len(PQ.ks) + ["d", "x", "x"] + ["x", "x"] + ["x", "r", "x"]
        gm(self, AR, RES, rt=0.8, nota="(fusão)", extra=[FadeOut(sp), FadeOut(npl), FadeIn(cp2), *[Create(c) for c in circs]])
        self.remove(PQ, QM, Q1, Q3, sp, npl)
        labs = {t: rot(s, *canto_xy(VA, 2.85 * math.cos(t), 2.75 * math.sin(t)), 30) for t, s in ((PI / 4, r"\dfrac12"), (3 * PI / 4, r"-\dfrac12"), (0, "0"), (PI / 2, "0"))}
        ne_ = legenda("NOS EIXOS: 0", 1124, 420, GEO)
        self.gat("nos eixos ela vale zero")
        for e_ in eixo_p:
            self.play(*[FadeIn(p, scale=0.5) for p in e_], run_time=0.25)
        self.play(FadeIn(labs[0][0]), FadeIn(labs[PI / 2][0]), FadeIn(ne_, shift=0.05 * UP), run_time=0.3)
        labs[PI / 2].f._origem = "a"
        escreve(self, labs[0].f, 0.5, rt=0.3, extra=[caneta(labs[PI / 2].f, ritmo=0.5)])
        DG = L([("y", r"\Y=\X:\quad "), ("a", r"2\X\cdot\X^3/(2\X^2)^2"), ("b", r"=2\X^4/4\X^4"), ("c", r"=\tfrac12")], 1110, 520, 34)
        self.gat("na diagonal as duas coordenadas são iguais")
        gm(self, RES, DG, rt=0.8, copia=True, ka=["x", "a"], kb=["y", "a", "b", "c"])
        nd = legenda("NA DIAGONAL: ½, POR MAIS PERTO QUE SE CHEGUE", 1124, 465, AMB, "left", 26)
        self.gat("e vale meio na diagonal inteira")
        for d_ in diag_p:
            self.play(*[FadeIn(p, scale=0.5) for p in d_], run_time=0.25)
        self.play(FadeIn(labs[PI / 4][0]), FadeIn(labs[3 * PI / 4][0]), FadeIn(nd, shift=0.05 * UP), run_time=0.3)
        labs[3 * PI / 4].f._origem = "a"
        escreve(self, labs[PI / 4].f, 0.5, rt=0.3, extra=[caneta(labs[3 * PI / 4].f, ritmo=0.5)])
        nc = T("NÃO É C¹", 1120, 615, 44, cor=CORAL)
        self.gat("o campo não é de classe")
        self.play(FadeIn(nc, shift=0.05 * UP), run_time=0.4)
        ra = L([("r", r"\dfrac{\|\text{erro}\|}{\|\Hh\|}=\dfrac12\ \text{na diagonal}\ \not\to 0")], 1120, 700, 36)
        self.gat("e a tabela perde a garantia")
        escreve(self, ra, 0.2)
        cg = legenda("C¹ GARANTE A TABELA; AQUI ELA FALHA", 1124, 825, GEO, "left", 26)
        self.gat("o cê um é uma garantia")
        self.play(FadeIn(cg, shift=0.05 * UP), run_time=0.4)
        nd2 = legenda("NÃO É DIFERENCIÁVEL NA ORIGEM", 1124, 780, BR)
        self.gat("que a aproximação falha")
        self.play(FadeIn(nd2, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D4-8 · ANTES / AGORA ──
        self.an("D4-8")
        an_ = legenda("ANTES: NEM CONTÍNUO", 1124, 780, GEO)
        ag = T("AGORA:", 1120, 840, 28)
        s1, s2, s3 = selo("CONTÍNUO", True, 1240, 840, 28), selo("PARCIAIS", True, 1450, 840, 28), selo("TABELA", False, 1650, 840, 28)
        self.gat("no episódio passado o campo encrenqueiro")
        self.play(FadeOut(cg), FadeOut(nd2), FadeIn(an_, shift=0.05 * UP), run_time=0.4)
        self.remove(cg, nd2)
        self.gat("este é contínuo")
        self.play(FadeIn(ag), FadeIn(s1), run_time=0.4)
        self.gat("tem as duas derivadas parciais")
        self.play(FadeIn(s2), run_time=0.3)
        self.gat("e mesmo assim engana")
        self.play(FadeIn(s3), run_time=0.3)
        pb = legenda("TER DERIVADAS PARCIAIS NÃO BASTA", 1124, 900, CORAL, "left", 26)
        self.gat("ter derivadas parciais não basta")
        self.play(FadeIn(pb, shift=0.05 * UP), run_time=0.4)
        self.sai_fim()
