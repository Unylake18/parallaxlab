"""yt_0044 · Lote PE1: E1-1 a E1-5 (o cubo 0 ≤ x, y, z ≤ 1 com ρ = x + y + z: soma de Riemann, limite das somas, redução, centro de massa,
a folha que não pesa). C1.1–C1.15 + C1 da folha, GM1–GM6, alvos 03 a 07."""
from k44 import *  # noqa: F401,F403

COL = 1020
COLC = 780
C12 = 1010
LEVE = "#2C6A86"


def lado(A, B, ga=None, gb=0, gap=12):
    """B logo à direita de A, com o glifo gb de B na altura do glifo ga de A (por padrão, o centro vertical de A)."""
    B.shift(RIGHT * (A.get_right()[0] - B.get_left()[0] + gap / 120))
    ya = A[0][ga].get_center()[1] if ga is not None else A.get_center()[1]
    B.shift(UP * (ya - B[0][gb].get_center()[1]))
    return B


class PE1(B44):
    ANTES = "EXERCÍCIOS DO MÓDULO"

    def corpo(self):
        # ── E1-1 · o cubo: o chute e a soma de Riemann (alvo 03, C1.1–C1.6, GM1) ─────────────────────────────
        self.an("E1-1")
        pal = self.palco("cubo", OL, grade=0.0)
        rz = self.rot3(pal, "ez", r"\Z", size=38, ancora="c")
        rx = self.rot3(pal, "ex", r"\X", size=38, ancora="c")
        self.titulo("O CUBO: A SOMA DE RIEMANN")
        self.entra(pal.fundo, rt=0.6)
        self.pena(rz, rx)

        self.gat("um cubo de lado um")
        self.degrau("C1.0", "CUBO 0 <= x, y, z <= 1, rho = x + y + z")
        l1 = mixl([("t", "CUBO", GEO), ("m", r"0\le\X,\Y,\Z\le1,\ \ \de=\X+\Y+\Z")], COL, 170, 40)
        self.pena(l1)
        self.col("E1-1", l1)

        self.gat("a densidade é a soma das coordenadas")
        sq1, lq1 = legq(LEVE, "LEVE NA ORIGEM", 120, 1020, 30)
        sq2, lq2 = legq(CI, "PESADO NA QUINA", 480, 1020, 30)
        self.play(FadeIn(sq1), FadeIn(sq2), run_time=0.25)
        self.pena(lq1, lq2)

        self.gat("pelo chute mais preguiçoso")
        self.degrau("C1.1", "CHUTE: rho(centro) * V = 3/2 * 1 = 3/2")
        l2 = mixl([("t", "CHUTE:", SOMB), ("m", r"\de("), ("g", -10), ("t", "CENTRO", BR), ("g", -10), ("m", r")\cdot V=\frac32\cdot1=\frac32")], COL, 265, 40)
        self.pena(l2)
        self.col("E1-1", l2)

        self.gat("Corta cada aresta no meio")
        self.degrau("C1.2a", "n = 2: Delta x = Delta y = Delta z = 1/2, Delta V = 1/8")
        l3 = TC(r"n=2:\ \ \Delta\X=\Delta\Y=\Delta\Z=\frac12,\ \ \Delta V=\frac18", COL, 370, 40)
        self.play(*pal.anim(1.0, grade=1.0), run_time=1.0)
        self.pena(l3)
        self.col("E1-1", l3)

        self.gat("no ponto do meio de cada caixinha")
        self.degrau("C1.2b", "PONTOS MÉDIOS: cada coordenada é 1/4 ou 3/4")
        pal, rots = self.troca3d(pal, [rz, rx], "cuboCaixas", OL, rots=[("ez", r"\Z", dict(size=38, ancora="c")), ("ex", r"\X", dict(size=38, ancora="c"))])
        pls = [self.rot3(pal, n, v, size=28, ancora="c", dy=-4) for n, v in (("c001", r"\frac54"), ("c101", r"\frac74"), ("c011", r"\frac74"), ("c111", r"\frac94"))]
        l4 = leg("PONTOS MÉDIOS: CADA COORDENADA É 1/4 OU 3/4", COL, 455, GEO, "left", 28)
        self.pena(*pls)
        self.pena(l4)
        self.col("E1-1", l4)

        self.gat("quatro caixinhas têm")
        self.degrau("C1.2c", "CADA COORDENADA: 4 * 1/4 + 4 * 3/4 = 1 + 3 = 4")
        t5 = T("CADA COORD.:", COL, 545 + 40 * .27, round(40 * .78), "left", GEO)
        x5 = pxof(t5.get_right())[0] + 14
        a5 = L([("a", r"4\cdot\frac14"), ("p", "+"), ("b", r"4\cdot\frac34")], x5, 545, 40)
        self.pena(t5, a5)
        b5 = L([("eq", "="), ("a", "1"), ("p", "+"), ("b", "3")], x5, 545, 40)
        lado(a5, b5)
        self.gm(1, a5, b5, [("a", "a"), ("p", "p"), ("b", "b")], rt=0.9, copia=True, nota="GM1a: 4*1/4 + 4*3/4 -> 1 + 3")
        c5 = L([("eq", "="), ("r", "4")], x5, 545, 40)
        lado(b5, c5)
        self.gm(1, b5, c5, [(["a", "p", "b"], "r")], rt=0.7, copia=True, nota="GM1b: 1 + 3 -> 4")
        self.col("E1-1", a5, b5, c5)

        self.gat("três coordenadas")
        self.degrau("C1.2d", "SOMA DOS rho: 3 * 4 = 12")
        l6 = mixl([("t", "SOMA DOS ρ:", CI), ("m", r"3\cdot4=12")], COL, 640, 40)
        self.pena(l6)
        self.col("E1-1", l6)

        self.gat("vezes o volume de cada caixinha")
        self.degrau("C1.2", "Sigma rho Delta V = 12 * 1/8 = 3/2")
        l7 = TC(r"\sum\de\,\Delta V=12\cdot\dfrac18=\dfrac32", COL + 10, 770, 50)
        self.pena(l7)
        mol7 = caixa_men(l7)
        self.play(Create(mol7), run_time=0.4)
        self.col("E1-1", l7)

        self.gat("Igualzinho ao chute")
        lg7 = leg("IGUAL AO CHUTE. COINCIDÊNCIA?", COL, 890, GEO, "left", 30)
        self.pena(lg7)
        self.col("E1-1", lg7)
        self.marca("03_E1-1")
        self._fecha(antes=0.35)      # final: a saída só no fim da fala (sem palco vazio entre as âncoras)
        self.sai(pal.fundo, *rots, *pls, l1, l2, l3, l4, t5, a5, b5, c5, l6, l7, mol7, lg7, sq1, lq1, sq2, lq2, rt=0.35)

        # ── E1-2 · o limite: o canto de baixo e o canto de cima (alvo 04, C1.7–C1.8, GM2) ───────────────────
        self.an("E1-2")
        pn = painel2d44(60, 160, 900, 500)
        lbp = leg("VISTA DE FRENTE DE UMA CAMADA", 90, 210, GEO, "left", 26)
        self.titulo("A DEFINIÇÃO: O LIMITE DAS SOMAS", rt=0.3, junto=[FadeIn(pn)])
        self.pena(lbp)

        def quadrado(i, cor, f):
            X0, Y0, Lq = 110 + i * 290, 280, 220
            g = VGroup(lin_px([(X0, Y0), (X0 + Lq, Y0), (X0 + Lq, Y0 + Lq), (X0, Y0 + Lq), (X0, Y0)], GEO, 3, z=6),
                       lin_px([(X0 + Lq / 2, Y0), (X0 + Lq / 2, Y0 + Lq)], GEO, 2, z=6), lin_px([(X0, Y0 + Lq / 2), (X0 + Lq, Y0 + Lq / 2)], GEO, 2, z=6))
            d = 6 if f == .25 else (Lq / 4 if f == .5 else Lq / 2 - 6)
            for a in (0, 1):
                for b in (0, 1):
                    g.add(ponto_px(X0 + a * Lq / 2 + d, Y0 + Lq - (b * Lq / 2 + d), cor, 9, z=8))
            return g

        nomes = [("CANTO DE BAIXO", AZC, .25), ("MEIO", BR, .5), ("CANTO DE CIMA", CORAL, .75)]
        qs = [quadrado(i, c, f) for i, (_, c, f) in enumerate(nomes)]
        tq = [leg(t, 110 + i * 290 + 110, 280 + 220 + 56, c, "center", 26) for i, (t, c, _) in enumerate(nomes)]

        self.gat("troca o ponto escolhido")
        self.play(FadeIn(qs[1]), run_time=0.4)
        self.pena(tq[1])
        self.dentro(pn._painel, lbp, *tq)

        self.gat("no canto de baixo de cada caixinha")
        self.degrau("C1.3a", "BAIXO (0 ou 1/2): 3(4*0 + 4*1/2) = 6 -> 6 * 1/8 = 3/4")
        self.play(FadeIn(qs[0]), run_time=0.4)
        self.pena(tq[0])
        b1 = mixl([("t", "BAIXO:", AZC), ("m", r"3\Big(4\cdot0+4\cdot\frac12\Big)=6\to6\cdot\frac18=\frac34")], C12, 200, 38)
        self.pena(b1)
        self.col("E1-2", b1)

        self.gat("no canto de cima")
        self.degrau("C1.3", "CIMA (1/2 ou 1): 3(4*1/2 + 4*1) = 18 -> 18 * 1/8 = 9/4")
        self.play(FadeIn(qs[2]), run_time=0.4)
        self.pena(tq[2])
        c1 = mixl([("t", "CIMA:", CORAL), ("m", r"3\Big(4\cdot\frac12+4\cdot1\Big)=18\to18\cdot\frac18=\frac94")], C12, 290, 38)
        self.pena(c1)
        self.col("E1-2", c1)

        # régua 0..3 com os pares baixo/cima e o 3/2
        X0r, X1r, Yb = 120, 900, 820
        pxv = lambda v: X0r + (X1r - X0r) * v / 3
        regua = VGroup(lin_px([(X0r, Yb), (X1r, Yb)], GEO, 3, z=6), *[lin_px([(pxv(v), Yb - 10), (pxv(v), Yb + 10)], GEO, 3, z=6) for v in range(4)])
        tr = [leg(str(v), pxv(v), Yb + 44, GEO, "center", 26) for v in range(4)]
        tab = [["n", "BAIXO", "MEIO", "CIMA"], ["2", "0{,}75", "1{,}5", "2{,}25"], ["4", "1{,}125", "1{,}5", "1{,}875"], ["10", "1{,}35", "1{,}5", "1{,}65"]]
        cores_t = [GEO, AZC, BR, CORAL]

        def linha_tab(i):
            out = []
            for j, c in enumerate(tab[i]):
                X, Y = C12 + 40 + j * 190, 380 + i * 58
                out.append(T(c, X, Y + 10, 26, "left", cores_t[j], bold=False) if i == 0 else TC(c, X, Y, 34))
            return out

        pares = [(.75, 2.25), (1.125, 1.875), (1.35, 1.65)]

        self.gat("corta em mais pedaços")
        self.degrau("C1.4", "tabela n | BAIXO | MEIO | CIMA: 2 | 0,75 | 1,5 | 2,25")
        h0 = linha_tab(0)
        r1 = linha_tab(1)
        mm = VGroup(lin_px([(pxv(1.5), Yb - 26), (pxv(1.5), Yb + 26)], MEN, 4, z=7))
        t32 = leg("3/2", pxv(1.5), Yb - 38, MEN, "center", 28)
        pr1 = VGroup(ponto_px(pxv(.75), Yb, AZC, 8, z=8), ponto_px(pxv(2.25), Yb, CORAL, 8, z=8))
        self.play(FadeIn(regua), Create(mm), FadeIn(pr1), run_time=0.5)
        self.pena(*tr, t32)
        self.pena(*h0)
        self.pena(*r1)
        self.col("E1-2", *h0, *r1)

        self.gat("Com quatro divisões")
        self.degrau("C1.5", "4 | 1,125 | 1,5 | 1,875")
        r2 = linha_tab(2)
        pr2 = VGroup(ponto_px(pxv(1.125), Yb, AZC, 8, z=8), ponto_px(pxv(1.875), Yb, CORAL, 8, z=8))
        self.play(FadeIn(pr2), run_time=0.3)
        self.pena(*r2)
        self.col("E1-2", *r2)

        self.gat("Com dez")
        self.degrau("C1.6", "10 | 1,35 | 1,5 | 1,65")
        r3 = linha_tab(3)
        pr3 = VGroup(ponto_px(pxv(1.35), Yb, AZC, 8, z=8), ponto_px(pxv(1.65), Yb, CORAL, 8, z=8))
        self.play(FadeIn(pr3), run_time=0.3)
        self.pena(*r3)
        self.col("E1-2", *r3)

        self.gat("o valor exato fica sempre espremido")
        self.degrau("C1.7", "3/2 - 3/(2n) <= iiint rho dV <= 3/2 + 3/(2n)")
        d1 = TC(r"\dfrac32-\dfrac{3}{2n}\le\iiint\de\,dV\le\dfrac32+\dfrac{3}{2n}", C12, 680, 44)
        self.pena(d1)
        self.col("E1-2", d1)

        self.gat("a diferença entre as duas")
        self.degrau("C1.8", "CIMA - BAIXO = 3/n -> 0 quando Delta = 1/n -> 0")
        tcb = T("CIMA − BAIXO", C12, 800 + 40 * .27, round(40 * .78), "left", GEO)
        xg = pxof(tcb.get_right())[0] + 14
        ga = L([("eq", "="), ("lp", r"\Big("), ("a1", r"\dfrac32"), ("p", "+"), ("f1", r"\dfrac{3}{2n}"), ("rp", r"\Big)"), ("m", "-"), ("lp2", r"\Big("),
                ("a2", r"\dfrac32"), ("mm", "-"), ("f2", r"\dfrac{3}{2n}"), ("rp2", r"\Big)")], xg, 800, 40)
        self.pena(tcb, ga)
        self.sub(gl(ga, "a1"), gl(ga, "a2"), rt=0.5, cor=MEN)
        gb = L([("eq", "="), ("f", r"\dfrac3n")], xg, 800, 40)
        gb.shift(UP * (ga[0][0].get_center()[1] - gb[0][0].get_center()[1]))
        self.gm(2, ga, gb, [("eq", "eq"), (["f1", "f2"], "f")], rt=1.0, nota="GM2: CIMA - BAIXO -> 3/n (os dois 3/2 acendem e saem)")
        gc = mixl([("m", r"\to0\quad(\Delta=\frac1n\to0)")], 0, 800, 40)
        gc.shift(RIGHT * (pxof(gb.get_right())[0] + 12 - pxof(gc.get_left())[0]) / 120 + UP * (gb[0][0].get_center()[1] - gc.p[0][0][0].get_center()[1]))
        self.pena(gc)
        self.col("E1-2", tcb, gb, gc)

        self.gat("a densidade é linear")
        lin1 = leg("ρ LINEAR: NO PONTO MÉDIO, O QUE SOBRA DE UM LADO", C12, 900, MEN, "left", 26)
        lin2 = leg("FALTA DO OUTRO", C12, 938, MEN, "left", 26)
        self.pena(lin1, lin2)
        self.col("E1-2", lin1, lin2)
        self.marca("04_E1-2")
        pal = self.palco("cuboSonda", OC, sonda=0.0)
        rz3 = self.rot3(pal, "ez", r"\Z", size=34, ancora="c")
        self.sai(pn, lbp, *qs, *tq, regua, *tr, mm, t32, pr1, pr2, pr3, b1, c1, *h0, *r1, *r2, *r3, d1, tcb, gb, gc, lin1, lin2, rt=0.35, extra=self.ent3d(pal))

        # ── E1-3 · a conta exata: reduzindo à integral simples (alvo 05, C1.9–C1.11, GM3, GM4) ──────────────
        self.an("E1-3")
        self.titulo("O CUBO: A CONTA EXATA", rt=0.3)
        cg_r, cf_r, cm_r = chipm([("t", "SOMA DE RIEMANN:", GEO), ("m", r"\frac32"), ("t", "PARA TODO", GEO), ("m", "n"), ("t", "(PONTO MÉDIO)", GEO)], COLC, 140, 28)

        self.gat("a gente nunca calcula pela definição")
        self.degrau("C1.9a", "M = int_0^1 int_0^1 int_0^1 (x + y + z) dz dy dx")
        m1 = TC(r"M=\int_0^1\!\!\int_0^1\!\!\int_0^1(\X+\Y+\Z)\,\dZ\,\dY\,\dX", COLC, 280, 48)
        self.pena(m1)
        self.pena(rz3)
        self.chip_pena(cg_r, cf_r, cm_r)
        self.col("E1-3", m1, chips=1)

        self.gat("A de dentro é em z")
        self.degrau("C1.9", "int_0^1 (x + y + z) dz = [xz + yz + z^2/2]_0^1 = x + y + 1/2")
        sqA, lqA = legq(AZC, "ENTRA EM z = 0", 120, 1020, 30)
        sqB, lqB = legq(CORAL, "SAI EM z = 1", 440, 1020, 30)
        self.play(*pal.anim(1.2, sonda=1.0), FadeIn(sqA), FadeIn(sqB), run_time=1.2)
        self.pena(lqA, lqB)
        m2a = L([("pre", r"\int_0^1(\X+\Y+\Z)\,\dZ="), ("lb", r"\Big["), ("xz", r"\X\Z"), ("p1", "+"), ("yz", r"\Y\Z"), ("p2", "+"), ("z2", r"\dfrac{\Z^2}{2}"),
                 ("rb", r"\Big]_0^1")], COLC, 420, 44)
        self.pena(m2a)
        m2b = L([("eq", "="), ("x", r"\X"), ("p1", "+"), ("y", r"\Y"), ("p2", "+"), ("h", r"\dfrac12")], COLC, 420, 44)
        lado(m2a, m2b, ultimo(m2a, "pre"), 0)
        self.gm(3, m2a, m2b, [("xz", "x"), ("p1", "p1"), ("yz", "y"), ("p2", "p2"), ("z2", "h")], rt=1.0, copia=True, nota="GM3: [xz + yz + z^2/2]_0^1 -> x + y + 1/2")
        self.col("E1-3", m2a, m2b, chips=1)

        self.gat("Depois em y")
        self.degrau("C1.10", "int_0^1 (x + y + 1/2) dy = [xy + y^2/2 + y/2]_0^1 = x + 1/2 + 1/2 = x + 1")
        m3a = L([("pre", r"\int_0^1\Big(\X+\Y+\dfrac12\Big)\dY=\Big[\X\Y+\dfrac{\Y^2}{2}+\dfrac{\Y}{2}\Big]_0^1="), ("x", r"\X"), ("p1", "+"), ("h1", r"\dfrac12"),
                 ("p2", "+"), ("h2", r"\dfrac12")], COLC, 560, 42)
        self.pena(m3a)
        m3b = L([("eq", "="), ("x", r"\X"), ("p", "+"), ("one", "1")], COLC, 560, 42)
        lado(m3a, m3b, sel(m3a, "x")[0], sel(m3b, "x")[0])
        self.gm(4, m3a, m3b, [("x", "x"), ("p1", "p"), (["h1", "p2", "h2"], "one")], rt=0.9, copia=True, nota="GM4: x + 1/2 + 1/2 -> x + 1")
        self.col("E1-3", m3a, m3b, chips=1)

        self.gat("por último em x")
        self.degrau("C1.11", "int_0^1 (x + 1) dx = [x^2/2 + x]_0^1 = 1/2 + 1 = 3/2")
        m4 = TC(r"\int_0^1(\X+1)\,\dX=\Big[\dfrac{\X^2}{2}+\X\Big]_0^1=\dfrac12+1=\dfrac32", COLC + 10, 710, 48)
        self.pena(m4)
        mol4 = caixa_men(m4)
        self.play(Create(mol4), run_time=0.4)
        self.col("E1-3", m4, chips=1)

        self.gat("o mesmo três meios")
        mol_s, t_s = selo("CONFERE COM A SOMA DE RIEMANN", COLC + 40, 860, MEN, 30)   # o ✓ é desenhado (o Space Grotesk não tem o glifo)
        x1s = pxof(mol_s.get_right())[0]
        mol_s = moldura(COLC, 860 - 36, x1s - COLC, 52, MEN, 1.0, 2, 8)
        ck_s = check_px(COLC + 26, 848, MEN, .75)
        self.play(Create(mol_s), Create(ck_s), run_time=0.3)
        self.pena(t_s)
        self.col("E1-3", t_s, chips=1)
        self.marca("05_E1-3")
        cg_m, cf_m, cm_m = chip(r"M=\frac32", COLC, 140, 28)
        self.sobe_sai(cg_r, m1, m2a, m2b, m3a, m3b, mol_s, ck_s, t_s, sqA, lqA, sqB, lqB, rt=0.3)
        self.chip_vira(cg_m, cf_m, cm_m, m4, sai=[mol4], rt=0.45, nota="o M = 3/2 vira o chip do E1-4")

        # ── E1-4 · onde o cubo equilibra (alvo 06, C1.12–C1.15, GM5, GM6) ────────────────────────────────────
        self.an("E1-4")
        pal, rots = self.troca3d(pal, [rz3], "cuboDiag", OC, diag=0.0, centro=0.0, rots=[("ez", r"\Z", dict(size=34, ancora="c"))])
        self.titulo("ONDE O CUBO EQUILIBRA", rt=0.25)
        self.col("E1-4", cg_m, chips=1)

        self.gat("trocar o nome das letras")
        self.degrau("C1.12a", "trocar x por y não muda o cubo nem rho => xbar = ybar = zbar")
        s1 = mixl([("t", "TROCAR x POR y NÃO MUDA O CUBO NEM ρ", GEO), ("m", r"\Rightarrow\ \xb=\yb=\zb")], COLC, 230, 38)
        self.pena(s1)
        self.col("E1-4", s1, chips=1)

        self.gat("distribui o x")
        self.degrau("C1.12", "M_yz = iiint x(x + y + z) dV = iiint x^2 dV + iiint xy dV + iiint xz dV")
        ya = L([("lhs", r"\Myz="), ("int", r"\iiint"), ("x", r"\X"), ("lp", "("), ("x2", r"\X"), ("p1", "+"), ("y", r"\Y"), ("p2", "+"), ("z", r"\Z"), ("rp", ")"),
                ("dv", r"\,dV")], COLC, 330, 38)
        self.pena(ya)
        yb = L([("eq", "="), ("i1", r"\iiint"), ("t1", r"\X^2"), ("d1", "dV"), ("p1", "+"), ("i2", r"\iiint"), ("t2", r"\X\Y"), ("d2", r"\,dV"), ("p2", "+"),
                ("i3", r"\iiint"), ("t3", r"\X\Z"), ("d3", r"\,dV")], COLC, 330, 38)
        lado(ya, yb, ultimo(ya, "lhs"), 0)
        self.gm(5, ya, yb, [("int", "i1"), (["x", "x2"], "t1"), ("dv", "d1"), ("p1", "p1"), ("y", "t2"), ("p2", "p2"), ("z", "t3")], rt=1.1, copia=True,
                nota="GM5: iiint x(x + y + z) dV -> iiint x^2 dV + iiint xy dV + iiint xz dV")
        self.col("E1-4", ya, yb, chips=1)

        self.gat("cada pedaço separa")
        self.degrau("C1.12b", "iiint x^2 dV = int x^2 dx * int dy * int dz = 1/3 * 1 * 1 = 1/3")
        y2 = TC(r"\iiint\X^2dV=\int_0^1\!\X^2\dX\cdot\!\int_0^1\!\dY\cdot\!\int_0^1\!\dZ=\frac13\cdot1\cdot1=\frac13", COLC, 430, 38)
        self.pena(y2)
        self.col("E1-4", y2, chips=1)

        self.gat("o x vezes y")
        self.degrau("C1.12c", "iiint xy dV = int x dx * int y dy * int dz = 1/2 * 1/2 * 1 = 1/4 (e iiint xz dV = 1/4)")
        y3 = TC(r"\iiint\X\Y\,dV=\int_0^1\!\X\dX\cdot\!\int_0^1\!\Y\dY\cdot\!\int_0^1\!\dZ=\frac12\cdot\frac12\cdot1=\frac14\ \ (\iiint\X\Z\,dV=\frac14)", COLC, 530, 36)
        self.pena(y3)
        self.col("E1-4", y3, chips=1)

        self.gat("Somando as três")
        self.degrau("C1.13", "M_yz = 1/3 + 1/4 + 1/4 = 4/12 + 3/12 + 3/12 = 10/12 = 5/6")
        y4 = TC(r"\Myz=\frac13+\frac14+\frac14=\frac4{12}+\frac3{12}+\frac3{12}=\frac{10}{12}=\frac56", COLC, 630, 42)
        self.pena(y4)
        self.col("E1-4", y4, chips=1)

        self.gat("Dividindo pela massa")
        self.degrau("C1.14", "xbar = (5/6)/(3/2) = 5/6 * 2/3 = 10/18 = 5/9 approx 0,556")
        xa = L([("lhs", r"\xb="), ("fr", r"\dfrac{5/6}{3/2}")], COLC + 10, 760, 48)
        self.pena(xa)
        xb_ = L([("eq", "="), ("a", r"\dfrac56"), ("dot", r"\cdot"), ("b", r"\dfrac23")], COLC + 10, 760, 48)
        lado(xa, xb_, ultimo(xa, "lhs"), 0)
        self.gm(6, xa, xb_, [("fr", ["a", "dot", "b"])], rt=0.9, copia=True, nota="GM6a: (5/6)/(3/2) -> 5/6 * 2/3")
        xc = L([("eq", "="), ("fr", r"\dfrac{10}{18}")], COLC + 10, 760, 48)
        lado(xb_, xc, 0, 0)
        self.gm(6, xb_, xc, [(["a", "dot", "b"], "fr")], rt=0.8, copia=True, nota="GM6b: 5/6 * 2/3 -> 10/18")
        xd = L([("eq", "="), ("fr", r"\dfrac59"), ("ap", r"\approx0{,}556")], COLC + 10, 760, 48)
        lado(xc, xd, 0, 0)
        self.gm(6, xc, xd, [("fr", "fr")], rt=0.8, copia=True, nota="GM6c: 10/18 -> 5/9")
        x0, y0 = pxof(xa.get_corner(UL))
        x1, y1 = pxof(xd.get_corner(DR))
        top = min(pxof(m.get_corner(UL))[1] for m in (xa, xb_, xc, xd))
        bot = max(pxof(m.get_corner(DR))[1] for m in (xa, xb_, xc, xd))
        molx = moldura(x0 - 14, top - 10, (x1 - x0) + 28, (bot - top) + 20, MEN, 1.0, 3, 12)
        self.play(Create(molx), run_time=0.4)
        self.col("E1-4", xa, xb_, xc, xd, chips=1)

        self.gat("fica na diagonal")
        self.degrau("C1.15", "(xbar, ybar, zbar) = (5/9, 5/9, 5/9): na diagonal, puxado para a quina")
        xm, ym = pal.pt("cm")
        cmk = cm_mark(xm, ym, 13)
        r12 = self.rot3(pal, "t12", r"\tfrac12", size=28, ancora="c")
        r59 = self.rot3(pal, "t59", r"\tfrac59", size=28, ancora="c")
        sqG, lqG = legq(GEO, "CENTRO DO CUBO", 120, 1020, 30)
        sqL, lqL = legq(LIL, "CENTRO DE MASSA", 440, 1020, 30)
        self.play(*pal.anim(1.0, diag=1.0), run_time=1.0)
        pal.set(centro=1.0)
        self.play(FadeIn(cmk), FadeIn(sqG), FadeIn(sqL), run_time=0.4)
        self.pena(lqG, lqL, r12, r59)
        y5 = TC(r"(\xb,\yb,\zb)=\big(\frac59,\frac59,\frac59\big)", COLC, 890, 42)
        lg5 = leg("NA DIAGONAL, PUXADO PARA A QUINA", COLC + 560, 898, GEO, "left", 26)
        self.pena(y5)
        self.pena(lg5)
        self.col("E1-4", y5, lg5, chips=1)
        self.marca("06_E1-4")
        pal5 = self.palco("cuboFolha", OL, folha=0.0, caixas=0.0)
        rz5 = self.rot3(pal5, "ez", r"\Z", size=38, ancora="c")
        self.sai(pal.fundo, *rots, r12, r59, cmk, sqG, lqG, sqL, lqL, cg_m, s1, ya, yb, y2, y3, y4, xa, xb_, xc, xd, molx, y5, lg5, rt=0.35, extra=self.ent3d(pal5))

        # ── E1-5 · a folha que não pesa (alvo 07) ─────────────────────────────────────────────────────────────
        self.an("E1-5")
        self.titulo("A FOLHA QUE NÃO PESA", rt=0.3)
        pal = pal5
        self.pena(rz5)

        self.gat("só a tampa")
        self.degrau("C1.16a", "FOLHA: 0 <= x, y <= 1, z = 1;  iiint_FOLHA rho dV = ?")
        sqF, lqF = legq(LI, "A FOLHA z = 1", 120, 1020, 30)
        self.play(*pal.anim(0.5, folha=1.0), FadeIn(sqF), run_time=0.5)
        self.pena(lqF)
        f1 = mixl([("t", "FOLHA:", LI), ("m", r"0\le\X,\Y\le1,\ \ \Z=1")], COL, 170, 42)
        self.pena(f1)
        f2 = TC(r"\iiint_{\mathrm{FOLHA}}\de\,dV=\ ?", COL, 260, 44)
        self.pena(f2)
        self.col("E1-5", f1, f2)

        self.gat("a densidade não passa de três")
        self.degrau("C1.16b", "NA FOLHA: rho = x + y + 1 <= 3")
        f3 = mixl([("t", "NA FOLHA:", GEO), ("m", r"\de=\X+\Y+1\le3")], COL, 350, 40)
        self.pena(f3)
        self.col("E1-5", f3)

        self.gat("uma camada de caixinhas")
        self.degrau("C1.16c", "0 <= SOMA DE RIEMANN <= 3 * (1 * Delta z) = 3 Delta z -> 0")
        rdz = self.rot3(pal, "dz", r"\Dz", size=30, ancora="l", dx=22, dy=4)
        sqC, lqC = legq("#E9FF9E", "CAIXINHAS DE ALTURA Δz", 440, 1020, 30)
        self.play(*pal.anim(1.2, caixas=1.0), FadeIn(sqC), run_time=1.2)
        self.pena(rdz, lqC)
        f4 = mixl([("m", r"0\le"), ("t", "SOMA", BR), ("m", r"\le3\cdot(1\cdot\Dz)=3\,\Dz\to0")], COL, 445, 42)
        self.pena(f4)
        self.col("E1-5", f4)

        self.gat("vai a zero")
        self.degrau("C1.16", "iiint_FOLHA rho dV = 0")
        f5 = TC(r"\iiint_{\mathrm{FOLHA}}\de\,dV=0", COL + 10, 560, 50)
        self.pena(f5)
        mol5 = caixa_men(f5)
        self.play(Create(mol5), run_time=0.4)
        self.col("E1-5", f5)

        self.gat("Parece uma contradição")
        mol_a, t_a = selo("ρ > 0 E INTEGRAL ZERO?", COL, 690, AL, 30)
        self.play(Create(mol_a), run_time=0.3)
        self.pena(t_a)
        self.col("E1-5", t_a)

        self.gat("não tem nenhum ponto interior")
        g1 = leg("A FOLHA NÃO TEM PONTO INTERIOR:", COL, 780, MEN, "left", 30)
        g2 = leg("VOLUME ZERO, MASSA ZERO", COL, 822, MEN, "left", 30)
        self.pena(g1, g2)
        self.col("E1-5", g1, g2)

        self.gat("Na prática")
        g3 = leg("POR ISSO TAMPA, PAREDE E COSTURA", COL, 900, GEO, "left", 28)
        g4 = leg("NÃO MUDAM A INTEGRAL", COL, 938, GEO, "left", 28)
        self.pena(g3, g4)
        self.col("E1-5", g3, g4)
        self.marca("07_E1-5")

        self.sai_fim(rt=0.35)
