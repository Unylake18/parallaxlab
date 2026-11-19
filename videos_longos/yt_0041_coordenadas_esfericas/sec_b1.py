"""yt_0041 · B1 · o endereço esférico (B1-1, alvo 03), um ponto de exemplo (B1-2, alvo 04) e a caixa que vira a bola (B1-3, alvo 05).
B1-1: o 3D `ponto` monta peça por peça (r, φ a partir do eixo z, θ no chão, a página chapada, a altura, a sombra); a coluna escreve z, s, x, y com
os voos do desenho (r e φ dos rótulos; s da linha s; r sen φ da linha s). B1-2: o mesmo 3D (a câmera não recarrega); os rótulos viram números,
que voam para a linha do ponto; √3 e 1 voam do resultado para o desenho; Pitágoras com o glyph map 1. B1-3: a caixa (r, φ, θ) e a bola em
traço; os intervalos voam das arestas da caixa; a célula lima sai da caixa e se deforma até a bola (um objeto só, um ValueTracker); as bordas
ruins acendem na caixa e na bola ao mesmo tempo, e cada linha de BORDAS RUINS nasce da face que acende."""
from k41 import *

COL = 1020


def depois(B, A, ia, ib, gap=10):
    """Põe B logo à direita de A (gap px), com o glifo ib de B na mesma altura do glifo ia de A (os '=' alinhados)."""
    B.shift(RIGHT * (A.get_right()[0] + gap / 120 - B.get_left()[0]))
    B.shift(UP * (A[0][ia].get_center()[1] - B[0][ib].get_center()[1]))
    return B


def de_ponto(alvo, x, y, esc=0.45):
    """Fonte de um voo que nasce de um ponto do desenho: uma cópia pequena do próprio termo, posta no ponto (não entra na cena)."""
    src = alvo.copy().scale(esc).move_to(PX(x, y))
    return src


# ── a célula que se deforma da caixa para a bola (B1-3): polígonos projetados, um ValueTracker ─────────────────────────
A_, B_, CC_ = 2.2, 2.2 / PI, 3.0 / (2 * PI)
T1B = 3 * PI / 2 + .15          # θ da célula na caixa (0 ≤ θ ≤ 2π) ≡ −π/2 + 0,15 na bola
T1E = -PI / 2 + .15


def _Q(r, f, t):
    return np.array([r * A_, t * CC_, f * B_])


def _WS(r, f, t):
    return 2.1 * np.array([r * math.sin(f) * math.cos(t), r * math.sin(f) * math.sin(t), r * math.cos(f)])


LDIR = np.array([.55, -.75, .45]) / np.linalg.norm([.55, -.75, .45])


def cel_morph(pa, pb, s):
    """A célula (r ∈ [r1, 1], φ ∈ [π/3, π/2], θ ∈ [t1, t1 + π/6]) com cada vértice indo da projeção na caixa (câmera de pa) até a projeção na bola
    (câmera de pb). Em s = 0 a célula é a face r = 1 da caixa (r1 = 1, chapada); r1 vai a 1/2 junto. Face visível = a que olha para a câmera na
    geometria da metade em que o vértice está (caixa até s = 0,5, bola depois); o tom de cada face é o da luz fixa (LDIR) do c41.js."""
    u = suave(s)
    r1 = 1.0 - 0.5 * u
    ca, cb = pa.cam(), pb.cam()
    f1, f2, dt = PI / 3, PI / 2, PI / 6
    n = 6
    geo, cam_ = (_Q, ca) if u < 0.5 else (_WS, cb)
    t0 = T1B if u < 0.5 else T1E

    def P(r, f, k):
        a = np.array(proj3d(ca, _Q(r, f, T1B + k * dt)))
        b = np.array(proj3d(cb, _WS(r, f, T1E + k * dt)))
        return a * (1 - u) + b * u

    def M(r, f, k):
        return geo(r, f, t0 + k * dt)

    def borda(F, a0, a1, b0, b1):
        pts = [(a0 + (a1 - a0) * i / n, b0) for i in range(n)] + [(a1, b0 + (b1 - b0) * j / n) for j in range(n)]
        pts += [(a1 - (a1 - a0) * i / n, b1) for i in range(n)] + [(a0, b1 - (b1 - b0) * j / n) for j in range(n)]
        return [F(a, b) for a, b in pts]

    faces = [("ext", lambda f, k: (1.0, f, k), (f1, f2, 0, 1)), ("int", lambda f, k: (r1, f, k), (f2, f1, 0, 1)),
             ("t1", lambda r, f: (r, f, 0), (r1, 1.0, f2, f1)), ("t2", lambda r, f: (r, f, 1), (r1, 1.0, f1, f2)),
             ("f1", lambda r, k: (r, f1, k), (r1, 1.0, 0, 1)), ("f2", lambda r, k: (r, f2, k), (r1, 1.0, 1, 0))]
    cantos = [M(r, f, k) for r in (r1, 1.0) for f in (f1, f2) for k in (0, 1)]
    cen = np.mean(cantos, axis=0)
    pos = np.array(cam_["pos"])
    g = VGroup()
    for nome, F, lim in faces:
        par = borda(F, *lim)
        mw = np.mean([M(*q) for q in par], axis=0)
        nrm = mw - cen
        if np.linalg.norm(nrm) < 1e-4 or nrm @ (pos - mw) <= 0:
            continue
        luz = max(0.0, float(nrm / np.linalg.norm(nrm) @ LDIR))
        cor = mixh(BG_, LI, .40 + .45 * luz)
        pts = [P(*q) for q in par]
        pol = Polygon(*[PX(x, y) for x, y in pts]).set_fill(cor, 1).set_stroke(LI, W(2.0), 1)
        g.add(pol)
    return sem_ctn(g).set_z_index(5)


class PB1(B41):
    ANTES = "O ENDEREÇO ESFÉRICO"

    def corpo(self):
        # ── B1-1 ──────────────────────────────────────────────────────────────────────────────────────────
        self.an("B1-1")
        self.papel_on(rt=0)                                                     # G1: o papel também atrás do 3D
        pt = self.palco("ponto", cam_alvo("b1"), obst=["P", "O"], rho=0.0, fi=0.0, teta=0.0, pagina=0.0, altura=0.0, sombra=0.0, xy=0.0)
        self.add(pt.fundo)
        rx = self.rot3(pt, "ex", r"\X", dy=-16, size=36)
        ry = self.rot3(pt, "ey", r"\Y", size=36)
        rz = self.rot3(pt, "ez", r"\Z", dx=16, size=36)
        rP = self.rot3(pt, "P", "P", dx=22, dy=-26, size=38)
        self.pena(rP, rx, ry, rz, lag=0.12)

        self.gat("a distância de P até a origem")
        lr = self.rot3(pt, "meioRho", r"\R", dx=-48, dy=-30, size=42)
        self.play(pt.tr["rho"].animate(rate_func=linear).set_value(1.0), run_time=1.0)
        self.pena(lr)
        self.gat("o ângulo que o segmento")
        lf = self.rot3(pt, "arcoFi", r"\F", dx=-44, dy=-48, size=40)
        self.play(pt.tr["fi"].animate(rate_func=linear).set_value(1.0), run_time=0.8)
        self.pena(lf)
        self.gat("fi zero é o polo norte")
        legf = leg("φ: DO POLO NORTE (0) AO POLO SUL (π)", 1020, 975, FI)
        self.pena(legf)
        self.gat("o téta de sempre")
        lt = self.rot3(pt, "arcoTh", r"\T", dx=26, dy=30, size=40)
        self.play(pt.tr["teta"].animate(rate_func=linear).set_value(1.0), run_time=0.8)
        legt = leg("θ: A LONGITUDE, IGUAL ÀS POLARES", 1020, 1025, TH)
        self.pena(lt, legt, lag=0.3)

        # vista 1: a página (de lado), painel 420 × 350 em (1000, 150)
        self.gat("olha de lado")
        self.play(pt.tr["pagina"].animate(rate_func=linear).set_value(1.0), run_time=1.0)
        pg = painel2d41(1000, 150, 420, 350)
        self.play(Create(pg), run_time=0.5)
        tpg = leg("PÁGINA (DE LADO)", 1020, 192, TH, "left", 26)
        self.pena(tpg)
        V1 = Vista2D(1090, 480, 125)
        pt1 = (1.0, 1.732)
        ang = math.atan2(pt1[0], pt1[1])
        eix1 = VGroup(V1.seta((0, 0), (1.55, 0), SOMB), V1.seta((0, 0), (0, 2.05), EZ))
        self.play(Create(eix1), run_time=0.5)
        rseg = V1.linha([(0, 0), pt1], RO, 6)
        self.play(Create(rseg), run_time=0.6)
        trac1 = VGroup(V1.linha([pt1, (pt1[0], 0)], GEO, 3, dash=[8, 8]), V1.linha([pt1, (0, pt1[1])], GEO, 3, dash=[8, 8]), V1.ponto(pt1, BR, 9))
        arc1 = V1.arco(.55 * 125, math.pi / 2, math.pi / 2 - ang, FI, 4)
        self.play(Create(trac1), Create(arc1), run_time=0.6)
        pR = TC(r"\R", V1.P(.66, 1.05)[0] + 14, V1.P(.66, 1.05)[1], 38, "c")
        pF = TC(r"\F", V1.P(.12, .78)[0], V1.P(.12, .78)[1], 34, "c")
        pZ = TC(r"\Z", V1.P(0, 2.05)[0] + 14, V1.P(0, 2.05)[1] + 6, 32, "c")
        pS = TC(r"\Rs", V1.P(1.55, 0)[0] - 8, V1.P(1.55, 0)[1] - 26, 32, "c")
        self.pena(pR, pF, pZ, pS, lag=0.1)
        self.dentro(pg._painel, pR, pF, pZ, pS, tpg)

        self.gat("z igual a r cosseno de fi")
        self.play(pt.tr["altura"].animate(rate_func=linear).set_value(1.0), run_time=0.9)
        zl = L([("z", r"\Z"), ("eq", "="), ("r", r"\R"), ("cos", r"\cos"), ("f", r"\F")], 1020, 570, 50)
        self.escreve(zl, voos=[(pZ, "z"), (pR, "r"), (pF, "f")], nota="B1-1: z, r e φ voam do painel PÁGINA")
        self.origem("z, r, φ da linha z", "painel PÁGINA")
        self.degrau("C1", "z = r cos φ")

        self.gat("a sombra de P no chão")
        ls = self.rot3(pt, "meioR", r"\Rs", dx=-40, dy=-30, size=40)
        self.play(pt.tr["sombra"].animate(rate_func=linear).set_value(1.0), run_time=0.9)
        self.pena(ls)
        sl = L([("s", r"\Rs"), ("eq", "="), ("r", r"\R"), ("sen", r"\sen"), ("f", r"\F")], 1450, 570, 50)
        self.gat("s igual a r seno de fi")
        self.escreve(sl, voos=[(pS, "s"), (pR, "r"), (pF, "f")], nota="B1-1: s, r e φ voam do painel PÁGINA")
        self.origem("s, r, φ da linha s", "painel PÁGINA")
        self.degrau("C1", "s = r sen φ")

        # vista 2: o chão (de cima), painel 420 × 350 em (1450, 150)
        self.gat("olha de cima")
        pc = painel2d41(1450, 150, 420, 350)
        self.play(Create(pc), run_time=0.5)
        tpc = leg("CHÃO (DE CIMA)", 1470, 192, SOMB, "left", 26)
        self.pena(tpc)
        V2 = Vista2D(1560, 450, 150)
        qq = (.5, .866)
        eix2 = VGroup(V2.seta((0, 0), (1.6, 0), E1), V2.seta((0, 0), (0, 1.6), E2))
        self.play(Create(eix2), run_time=0.5)
        sseg = V2.linha([(0, 0), qq], SOMB, 6)
        self.play(Create(sseg), run_time=0.6)
        trac2 = VGroup(V2.linha([qq, (qq[0], 0)], GEO, 3, dash=[8, 8]), V2.linha([qq, (0, qq[1])], GEO, 3, dash=[8, 8]), V2.ponto(qq, SOMB, 9))
        arc2 = V2.arco(.45 * 150, 0, math.pi / 3, TH, 4)
        self.play(Create(trac2), Create(arc2), run_time=0.6)
        cS = TC(r"\Rs", V2.P(.08, .62)[0], V2.P(.08, .62)[1], 38, "c")
        cT = TC(r"\T", V2.P(.6, .15)[0], V2.P(.6, .15)[1], 34, "c")
        cX = TC(r"\X", V2.P(1.6, 0)[0] - 6, V2.P(1.6, 0)[1] - 26, 32, "c")
        cY = TC(r"\Y", V2.P(0, 1.6)[0] + 14, V2.P(0, 1.6)[1] + 6, 32, "c")
        self.pena(cS, cT, cX, cY, lag=0.1)
        self.dentro(pc._painel, cS, cT, cX, cY, tpc)

        self.gat("x é s cosseno de téta")
        self.play(pt.tr["xy"].animate(rate_func=linear).set_value(1.0), run_time=0.6)
        xl = L([("x", r"\X"), ("eq", "="), ("s", r"\Rs"), ("ct", r"\cos\T")], 1020, 670, 50)
        self.escreve(xl, voos=[(cX, "x"), (cS, "s")], nota="B1-1: x, s e θ voam do painel CHÃO")
        self.origem("x, s, θ da linha x", "painel CHÃO")
        self.degrau("C1", "x = s cos θ")
        yl = L([("y", r"\Y"), ("eq", "="), ("s", r"\Rs"), ("st", r"\sen\T")], 1020, 770, 50)
        self.escreve(yl, voos=[(cY, "y"), (cS, "s")], nota="B1-1: y, s e θ voam do painel CHÃO")
        self.degrau("C1", "y = s sen θ")

        self.gat("trocando o s")
        xl2 = depois(L([("eq2", "="), ("rsf", r"\R\sen\F"), ("ct", r"\cos\T")], 0, 670, 50), xl, sel(xl, "eq")[0], 0)
        self.gm(1, xl, xl2, [(sel(xl, "ct"), sel(xl2, "ct"))], copia=True, nota="x = s cos θ → = r sen φ cos θ (o s troca)")
        self.degrau("C1", "x = s cos θ = r sen φ cos θ")
        yl2 = depois(L([("eq2", "="), ("rsf", r"\R\sen\F"), ("st", r"\sen\T")], 0, 770, 50), yl, sel(yl, "eq")[0], 0)
        self.gm(1, yl, yl2, [(sel(yl, "st"), sel(yl2, "st"))], copia=True, nota="y = s sen θ → = r sen φ sen θ (o s troca)")
        self.degrau("C1", "y = s sen θ = r sen φ sen θ")

        self.gat("fi só vai até pi")
        il = L([("r", r"\R\ge 0,"), ("f", r"\quad 0\le\F\le\pi,"), ("t", r"\quad 0\le\T\le 2\pi")], 1020, 880, 44)
        poe_parte(self, il)
        self.pena(parte(il, sel(il, "r"), "r ≥ 0"))
        self.pena(parte(il, sel(il, "f"), "φ"))
        self.pena(parte(il, sel(il, "t"), "θ"))
        self.col("B1-1", zl, sl, xl, yl, il, legf, legt, chips=2)
        self.marca("03_B1-1")

        # ── B1-2 ──────────────────────────────────────────────────────────────────────────────────────────
        self.an("B1-2")
        self.titulo("UM PONTO DE EXEMPLO")
        self.sobe_sai(zl, sl, xl, xl2, yl, yl2, il, legf, legt, pg, tpg, eix1, rseg, trac1, arc1, pR, pF, pZ, pS, pc, tpc, eix2, sseg, trac2, arc2,
                      cS, cT, cX, cY, dy=0.0, rt=0.6)
        self.col_zera("B1-1")

        self.gat("R igual a dois")
        n2 = pronto(self.rot3(pt, "meioRho", r"\Ro{2}", dx=22, dy=-14, size=38))
        pl = L([("v", r"(\R,\F,\T)"), ("eq", "="), ("a", r"\big("), ("dois", r"\Ro{2}"), ("c1", r",\,"), ("f", r"\Fi{\dfrac{\pi}{6}}"), ("c2", r"\!,\,"),
                ("t", r"\Th{\dfrac{\pi}{3}}"), ("b", r"\big)")], COL, 200, 46)
        poe_parte(self, pl)
        self.play(ReplacementTransform(lr, n2), run_time=0.6)
        self.pena(parte(pl, sel(pl, ["v", "eq", "a"]), "(r,φ,θ) = ("))
        self.voos([(n2.f, parte(pl, sel(pl, "dois"), "2"))], rt=0.8, nota="B1-2: o 2 voa do desenho")
        self.gat("fi igual a pi sobre seis")
        nf = pronto(self.rot3(pt, "arcoFi", r"\Fi{\pi/6}", dx=-80, dy=-44, size=32))
        self.play(ReplacementTransform(lf, nf), run_time=0.6)
        self.pena(parte(pl, sel(pl, "c1"), ","))
        self.voos([(nf.f, parte(pl, sel(pl, "f"), "π/6"))], rt=0.8, nota="B1-2: π/6 voa do desenho")
        self.gat("téta igual a pi sobre três")
        nt = pronto(self.rot3(pt, "arcoTh", r"\Th{\pi/3}", dx=14, dy=26, size=32))
        self.play(ReplacementTransform(lt, nt), run_time=0.6)
        self.pena(parte(pl, sel(pl, "c2"), ","))
        self.voos([(nt.f, parte(pl, sel(pl, "t"), "π/3"))], rt=0.8, nota="B1-2: π/3 voa do desenho")
        self.pena(parte(pl, sel(pl, "b"), ")"))
        self.degrau("C2", "(r, φ, θ) = (2, π/6, π/3)")

        self.gat("começando pela altura")
        zc = L([("z", r"\Z"), ("eq", "="), ("a", r"2\cos\dfrac{\pi}{6}"), ("eq2", "="), ("b", r"2\cdot\dfrac{\sqrt3}{2}"), ("eq3", "="), ("c", r"\sqrt3")],
               COL, 320, 46)
        poe_parte(self, zc)
        self.pena(parte(zc, sel(zc, ["z", "eq", "a"]), "z = 2 cos π/6"))
        self.degrau("C2", "z = 2 cos(π/6)")
        self.gat("e esse cosseno vocês já sabem")
        self.pena(parte(zc, sel(zc, ["eq2", "b"]), "= 2·√3/2"))
        self.degrau("C2", "= 2 · √3/2")
        self.gat("raiz de três a sombra")
        self.pena(parte(zc, sel(zc, ["eq3", "c"]), "= √3"))
        self.degrau("C2", "= √3")
        nz = self.rot3(pt, "zEixo", r"\sqrt3", dx=-70, size=32)
        self.voos([(gl(zc, "c"), nz)], rt=0.8, extra=[FadeOut(rz)], nota="B1-2: √3 voa do resultado para a altura")
        rz.clear_updaters()
        self.remove(rz)

        self.gat("a mesma ideia com o seno")
        sc_ = L([("s", r"\Rs"), ("eq", "="), ("a", r"2\sen\dfrac{\pi}{6}"), ("eq2", "="), ("b", r"2\cdot\dfrac12"), ("eq3", "="), ("c", "1")], COL, 440, 46)
        poe_parte(self, sc_)
        self.pena(parte(sc_, sel(sc_, ["s", "eq", "a"]), "s = 2 sen π/6"))
        self.degrau("C2", "s = 2 sen(π/6)")
        self.gat("que é um meio")
        self.pena(parte(sc_, sel(sc_, ["eq2", "b"]), "= 2·1/2"))
        self.degrau("C2", "= 2 · 1/2")
        self.gat("s dá um")
        self.pena(parte(sc_, sel(sc_, ["eq3", "c"]), "= 1"))
        self.degrau("C2", "= 1")
        mx, my = pt.pt("meioR")
        n1 = self.rot3(pt, "meioR", r"=1", dx=pxof(ls.get_right())[0] - mx + 4, dy=26, size=32, ancora="l")
        self.play(FadeIn(n1[0]), run_time=0.3)
        self.voos([(gl(sc_, "c"), parte(n1.f, [1], "1"))], rt=0.8, nota="B1-2: o 1 voa do resultado para a sombra (s = 1)")
        self.pena(parte(n1.f, [0], "="))
        self.remove(n1[0], n1.f, *n1.f._partes)
        self.add(n1)
        self.gat("x é o cosseno de sessenta graus")
        xc = L([("x", r"\X"), ("eq", "="), ("a", r"1\cdot\cos\dfrac{\pi}{3}"), ("eq2", "="), ("b", r"\dfrac12")], COL, 560, 46)
        poe_parte(self, xc)
        self.pena(parte(xc, sel(xc, ["x", "eq", "a"]), "x = 1 cos π/3"))
        self.gat("um meio e y é o seno")
        self.pena(parte(xc, sel(xc, ["eq2", "b"]), "= 1/2"))
        self.degrau("C2", "x = 1 · cos(π/3) = 1/2")
        yc = L([("y", r"\Y"), ("eqy", "="), ("ay", r"1\cdot\sen\dfrac{\pi}{3}"), ("eqy2", "="), ("by", r"\dfrac{\sqrt3}{2}")], COL, 680, 46)
        poe_parte(self, yc)
        self.pena(parte(yc, sel(yc, ["y", "eqy", "ay"]), "y = 1 sen π/3"))
        self.gat("o seno raiz de três sobre dois")
        self.pena(parte(yc, sel(yc, ["eqy2", "by"]), "= √3/2"))
        self.degrau("C2", "y = 1 · sen(π/3) = √3/2")

        self.gat("a prova dos nove é pitágoras")
        so = L([("lhs", r"\X^2+\Y^2+\Z^2"), ("eq", "="), ("a", r"\dfrac14"), ("p1", "+"), ("b", r"\dfrac34"), ("p2", "+"), ("c", "3")], COL, 800, 46)
        poe_parte(self, so)
        self.pena(parte(so, sel(so, ["lhs", "eq"]), "x²+y²+z² ="))
        self.gat("eleva cada um ao quadrado")
        self.pena(parte(so, sel(so, "a"), "1/4"))
        self.gat("mais três quartos")
        self.pena(parte(so, sel(so, ["p1", "b"]), "+ 3/4"))
        self.gat("já fecha um inteiro")
        self.pena(parte(so, sel(so, ["p2", "c"]), "+ 3"))
        self.degrau("C2", "x² + y² + z² = 1/4 + 3/4 + 3")
        q4 = depois(TC(r"=4", 0, 800, 46), so, sel(so, "eq")[0], 0)
        self.gat("mais três quatro")
        self.gm(1, so, q4, [(["a", "p1", "b", "p2", "c"], [1])], copia=True, nota="1/4 + 3/4 + 3 → 4")
        self.degrau("C2", "= 4")
        q22 = depois(TC(r"=\Ro{2}^2", 0, 800, 46), q4, 0, 0)
        self.gat("e quatro é dois ao quadrado")
        self.gm(1, q4, q22, [([1], [1, 2])], copia=True, nota="4 → 2²")
        self.degrau("C2", "= 2²")
        ck = check_px(1810, 800)
        self.gat("a distância ao quadrado")
        self.play(Create(ck), run_time=0.4)
        self.gat("isso vale sempre")
        cg, cf, cm_ = chip(r"\X^2+\Y^2+\Z^2=\R^2", COL, 920, 40, MEN)
        self.chip_pena(cg, cf, cm_)
        self.col("B1-2", pl, zc, sc_, xc, yc, so, cg, chips=1)
        self.marca("04_B1-2")
        self.chip_b12 = cg

        # ── B1-3 ──────────────────────────────────────────────────────────────────────────────────────────
        self.an("B1-3")
        velha = self.velhos(pl, zc, sc_, xc, yc, so, q4, q22, ck, cg)
        rot_pt = [x for x in (rx, ry, rP, n2, nf, nt, nz, ls, n1) if x in self.mobjects]
        bg = self.palco("bolagrade", cam_alvo("b13b"), bordas=0.0, celula=0.0)
        bg.fundo.op.set_value(0.0)
        self.add(bg.fundo)
        self.titulo("A CAIXA VIRA A BOLA")
        cx = self.palco("caixa", cam_alvo("b13a"), bordas=0.0, celula=0.0, meia=0.0, sep=0.0)
        cx.fundo.op.set_value(0.0)
        self.add(cx.fundo)
        # a caixa entra junto com a saída do ponto (troca cruzada): o palco nunca fica vazio
        self.play(pt.fundo.op.animate.set_value(0.0), cx.fundo.op.animate.set_value(1.0), *[FadeOut(x) for x in rot_pt],
                  velha.animate.shift(UP * 0.5).set_opacity(0), run_time=0.8)
        for x in rot_pt + [pt.fundo]:
            x.clear_updaters()
        self.remove(*rot_pt, pt.fundo, velha)
        self.col_zera("B1-2")
        self.gat("do lado das coordenadas")
        rr_ = self.rot3(cx, "eRho", r"\R", size=34)
        rt_ = self.rot3(cx, "eTh", r"\T", dx=6, size=34)
        rf_ = self.rot3(cx, "eFi", r"\F", dx=10, size=34)
        u1 = self.rot3(cx, "um", "1", dx=-6, dy=26, size=28)
        upi = self.rot3(cx, "pi", r"\pi", dx=-34, size=28)
        u2pi = self.rot3(cx, "dois_pi", r"2\pi", dx=-6, dy=30, size=28)
        self.pena(rr_, rt_, rf_, u1, upi, u2pi, lag=0.12)
        iv = L([("r0", r"0\le\R\le"), ("um", "1"), ("c1", r",\ \ 0\le\F\le"), ("pi", r"\pi"), ("c2", r",\ \ 0\le\T\le"), ("dpi", r"2\pi")], 120, 990, 40)
        poe_parte(self, iv)
        self.gat("r vai de zero a um")
        self.pena(parte(iv, sel(iv, "r0"), "0 ≤ r ≤"))
        self.voos([(u1.f, parte(iv, sel(iv, "um"), "1"))], rt=0.8, nota="B1-3: o 1 voa da aresta r")
        self.gat("fi de zero a pi")
        self.pena(parte(iv, sel(iv, "c1"), ", 0 ≤ φ ≤"))
        self.voos([(upi.f, parte(iv, sel(iv, "pi"), "π"))], rt=0.8, nota="B1-3: o π voa da aresta φ")
        self.gat("téta de zero a dois pi")
        self.pena(parte(iv, sel(iv, "c2"), ", 0 ≤ θ ≤"))
        self.voos([(u2pi.f, parte(iv, sel(iv, "dpi"), "2π"))], rt=0.8, nota="B1-3: o 2π voa da aresta θ")
        self.gat("é uma caixa")
        uc = leg("UMA CAIXA!", 120, 900, MEN, "left", 38)
        self.pena(uc)
        self.col("B1-3b", uc, iv)

        self.gat("pega uma celulinha")
        self.play(cx.tr["celula"].animate(rate_func=linear).set_value(1.0), run_time=0.5)
        self.wait(1.5)

        self.gat("que aqui se chama t")
        seta = seta_px((760, 540), (930, 540), BR, 4, 18)
        tl = L([("T", "T"), ("a", "("), ("r", r"\R"), ("c1", ","), ("f", r"\F"), ("c2", ","), ("t", r"\T"), ("b", ")")], 845, 440, 32, "l")
        tl.shift(RIGHT * (PX(845, 0)[0] - tl.get_center()[0]))
        tlp = VGroup(placa_min(tl), tl)              # R2: o rótulo T(r, φ, θ) fica sobre a bola 3D: placa mínima
        tlp._txt = "T(r,φ,θ)"
        self.play(Create(seta), bg.fundo.op.animate.set_value(1.0), run_time=0.6)
        rzb = self.rot3(bg, "ez", r"\Z", dx=14, size=36)
        self.pena(rzb)
        self.pena(tlp)

        self.gat("o tijolo vira a bola")
        s_ = ValueTracker(0.0)
        cel = always_redraw(lambda: cel_morph(cx, bg, s_.get_value()))
        self.add(s_, cel)
        self.play(s_.animate(rate_func=linear).set_value(1.0), run_time=2.0)      # a célula se deforma: caixa → bola (um objeto só)
        bg.set(celula=1.0)
        cel.clear_updaters()
        self.remove(cel, s_)
        self.degrau("B1-3", "a célula da caixa vira a célula curva da bola (deformação, sem cópia)")

        bt = leg("BORDAS RUINS", 1380, 340, AL, "left", 30)
        linhas = [mixl([("m", r"\R=0"), ("t", "→ ORIGEM", GEO)], 1380, 420, 36),
                  mixl([("m", r"\F=0,\ \F=\pi"), ("t", "→ EIXO", GEO), ("m", r"\Z")], 1380, 500, 36),
                  mixl([("m", r"\T=0,\ \T=2\pi"), ("t", "→ MESMA PÁGINA", GEO)], 1380, 580, 36)]
        fontes = ["faceR0", "arestaR0", "faceT0"]
        gats = ["a face R igual a zero", "as faces fi igual a zero e fi igual a pi", "e as faces téta igual a zero"]
        for k, (ln, fo, gg) in enumerate(zip(linhas, fontes, gats)):
            self.gat(gg)
            cx.set(bordas=float(k + 1))
            bg.set(bordas=float(k + 1))
            x, y = cx.pt(fo)
            if k == 0:
                self.pena(bt)
            self.voos([(de_ponto(ln.p[0], x, y), ln.p[0])], rt=0.9, nota=f"B1-3: a linha {k + 1} nasce da face que acende")
            self.pena(*ln.p[1:])
            self.degrau("B1-3", f"borda ruim {k + 1}")
        self.col("B1-3", bt, *linhas)
        self.marca("05_B1-3")
        self.sai_fim()
