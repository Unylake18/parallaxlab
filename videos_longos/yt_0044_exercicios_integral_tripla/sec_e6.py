"""yt_0044 · Lote PE6: E6-1 a E6-3 (o teorema dos eixos paralelos; o cubo pela aresta; a bola tangente e o erro clássico). C6.1–C6.12, GM20–GM21,
alvos 22 a 24. Tudo 2D."""
from k44 import *  # noqa: F401,F403

C61 = 920
C62 = 720
C63 = 700


def lado(A, B, ga=None, gb=0, gap=12):
    B.shift(RIGHT * (A.get_right()[0] - B.get_left()[0] + gap / 120))
    ya = A[0][ga].get_center()[1] if ga is not None else A.get_center()[1]
    B.shift(UP * (ya - B[0][gb].get_center()[1]))
    return B


def placa(tex, X, Y, size=26, al="c"):
    t = TC(tex, X, Y, size, al)
    g = VGroup(placa_min(t), t)
    g._txt = tex
    g.f = t
    return g


class PE6(B44):
    ANTES = "CONFERINDO: POLO NA DOBRADIÇA"

    def corpo(self):
        circ = [(math.cos(a), math.sin(a)) for a in np.linspace(0, 2 * PI, 97)]
        # ── E6-1 · o teorema dos eixos paralelos (alvo 22, C6.1–C6.2, GM20) ──────────────────────────────────
        self.an("E6-1")
        pn = painel2d44(60, 160, 800, 780)
        lb = leg("DE CIMA: UM CORPO QUALQUER", 84, 202, GEO, "left", 26)
        v = Vista2D(330, 560, 200)
        blob = []
        for a in np.linspace(0, 2 * PI, 161):
            r = 1.15 + .18 * math.sin(3 * a) + .1 * math.cos(2 * a)
            blob.append((r * math.cos(a), .85 * r * math.sin(a)))
        bf = poly_px([v.P(*p) for p in blob], mixh("#16123A", GEO, .30), 1.0, z=1)
        bl = v.linha(blob, GEO, 3)
        q0 = v.P(0, 0)
        cm0 = cm_mark(q0[0], q0[1], 15)
        e_cm = mixl([("t", "EIXO PELO CM", BR)], 0, 0, 24)
        e_cm.shift(RIGHT * ((q0[0] - 20) / 120 - 8 - e_cm.get_center()[0]) + UP * ((540 - (q0[1] - 40)) / 120 - e_cm.get_center()[1]))
        g_cm = VGroup(placa_min(e_cm), e_cm)
        g_cm._txt = "EIXO PELO CM"
        self.titulo("O TEOREMA DOS EIXOS PARALELOS", rt=0.4, junto=[FadeIn(pn), FadeIn(bf), Create(bl)])
        self.pena(lb)

        self.gat("um corpo qualquer")
        self.degrau("C6.1a", "centro de massa na origem: xbar = ybar = 0")
        self.play(FadeIn(cm0), run_time=0.3)
        self.pena(g_cm)
        self.dentro(pn._painel, lb, e_cm)
        a1 = mixl([("t", "CENTRO DE MASSA NA ORIGEM:", GEO), ("m", r"\xb=\yb=0")], C61, 190, 38)
        self.pena(a1)
        self.col("E6-1", a1)

        self.gat("um eixo paralelo")
        self.degrau("C6.1b", "eixo novo paralelo ao z, por (d, 0)")
        pN = v.ponto((1.9, 0), AL, 10)
        fd = v.linha([(0, 0), (1.9, 0)], LIL, 4)
        qd = v.P(.95, 0)
        td = TC(r"\dd", qd[0], qd[1] + 30, 30, "c")
        qn = v.P(1.9, 0)
        e_nv = mixl([("t", "EIXO NOVO", BR)], 0, 0, 24)
        e_nv.shift(RIGHT * (qn[0] / 120 - 8 - e_nv.get_center()[0]) + UP * ((540 - (qn[1] - 34)) / 120 - e_nv.get_center()[1]))
        g_nv = VGroup(placa_min(e_nv), e_nv)
        g_nv._txt = "EIXO NOVO"
        self.play(Create(fd), FadeIn(pN), run_time=0.5)
        self.pena(td, g_nv)
        self.dentro(pn._painel, td, e_nv)
        a2 = mixl([("t", "EIXO NOVO: PARALELO AO z, POR", GEO), ("m", r"(\dd,0)")], C61, 270, 38)
        self.pena(a2)
        self.col("E6-1", a2)

        self.gat("quadrado da distância até ele")
        self.degrau("C6.1c", "I = iiint ((x - d)^2 + y^2) dm")
        Pc = (.55, .65)
        qc = v.P(*Pc)
        cel = ret_px(qc[0] - 11, qc[1] - 11, qc[0] + 11, qc[1] + 11, fill=LI, fop=1.0, stroke=None, z=8)
        tdm = TC(r"\dm", qc[0] + 18, qc[1] - 14, 26, "l")
        f0 = v.linha([(0, 0), Pc], GEO, 2, dash=(7, 6))
        f1 = v.linha([(1.9, 0), Pc], AL, 2, dash=(7, 6))
        self.play(FadeIn(cel), Create(f0), Create(f1), run_time=0.5)
        self.pena(tdm)
        self.dentro(pn._painel, tdm)
        a3a = L([("pre", r"I=\iiint\big("), ("q", r"(\X-\dd)^2+\Y^2"), ("pos", r"\big)\,\dm")], C61, 370, 46)
        self.pena(a3a)
        self.col("E6-1", a3a)

        self.gat("Abre o quadrado")
        self.degrau("C6.1", "(x - d)^2 + y^2 = (x^2 + y^2) - 2dx + d^2")
        a4a = L([("q", r"(\X-\dd)^2+\Y^2"), ("eq", "=")], C61, 480, 42)
        self.escreve(a4a, voos=[(gl(a3a, "q"), "q")], rt_voo=0.8, nota="(x - d)^2 + y^2 voa da linha I")
        a4b = L([("r", r"(\X^2+\Y^2)-2\dd\X+\dd^2")], C61, 480, 42)
        lado(a4a, a4b, sel(a4a, "eq")[0], 0)
        a4b.shift(UP * (a4a[0][sel(a4a, "eq")[0]].get_center()[1] - a4b.get_center()[1]))
        self.gm(20, a4a, a4b, [("q", "r")], rt=1.0, copia=True, nota="GM20a: (x - d)^2 + y^2 -> (x^2 + y^2) - 2dx + d^2")
        self.col("E6-1", a4a, a4b)

        self.gat("A integral separa")          # a linha começa com a frase inteira ("A integral separa em três integrais"): 0,67 s antes do gatilho listado
        self.degrau("C6.2a", "I = iiint (x^2 + y^2) dm - 2d iiint x dm + d^2 iiint dm")
        a5 = TC(r"I=\iiint(\X^2+\Y^2)\,\dm-2\dd\iiint\X\,\dm+\dd^2\iiint\dm", C61, 590, 40)
        self.pena(a5)
        self.col("E6-1", a5)

        self.gat("cada uma tem nome")
        self.degrau("C6.2b", "= I_cm - 2d * M xbar + Md^2")
        a6 = L([("eq", "="), ("icm", r"\Icm"), ("mid", r"-2\dd\cdot M\xb"), ("md", r"+M\dd^2")], C61 + 40, 700, 44)
        self.pena(a6)
        self.col("E6-1", a6)

        self.gat("o centro de massa está na origem")
        self.degrau("C6.2", "xbar = 0 => I = I_cm + Md^2")
        self.sub(gl(a6, "mid"), rt=0.5, cor=AL)
        a7 = L([("pre", r"\xb=0\ \Rightarrow\ I="), ("icm", r"\Icm"), ("md", r"+M\dd^2")], C61 + 10, 820, 52)
        self.gm(20, a6, a7, [("icm", "icm"), ("md", "md")], rt=1.0, copia=True, nota="GM20b: -2d * M xbar -> 0 quando xbar = 0")
        mol7 = caixa_men(a7)
        self.play(Create(mol7), run_time=0.4)
        self.col("E6-1", a7)

        self.gat("o mais barato")
        cg_b, cf_b, cm_b = chipm([("t", "O EIXO MAIS BARATO PASSA PELO CENTRO DE MASSA", MEN)], C61, 940, 26, MEN)
        self.chip_pena(cg_b, cf_b, cm_b)
        self.col("E6-1", cg_b, chips=1)
        self.marca("22_E6-1")
        self.sai(pn, lb, bf, bl, cm0, g_cm, pN, fd, td, g_nv, cel, tdm, f0, f1, a1, a2, a3a, a4a, a4b, a5, a6, a7, mol7, cg_b, rt=0.35)

        # ── E6-2 · o cubo girando pela aresta (alvo 23, C6.3–C6.7) ──────────────────────────────────────────────
        self.an("E6-2")
        pn = painel2d44(60, 160, 600, 780)
        lb = leg("DE CIMA", 84, 202, GEO, "left", 26)
        v = Vista2D(360, 560, 190)
        sq_f = poly_px([v.P(-1, -1), v.P(1, -1), v.P(1, 1), v.P(-1, 1)], mixh("#16123A", GEO, .30), 1.0, z=1)
        sq_l = v.linha([(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)], GEO, 3)
        qL = v.P(0, -1)
        tL = TC("L", qL[0], qL[1] + 32, 28, "c")
        self.titulo("O CUBO GIRANDO PELA ARESTA", rt=0.4, junto=[FadeIn(pn), FadeIn(sq_f), Create(sq_l)])
        self.pena(lb)

        self.gat("um cubo de aresta L")
        self.degrau("C6.3a", "cubo de aresta L, rho = k, M = kL^3")
        self.pena(tL)
        self.dentro(pn._painel, lb, tL)
        b1 = mixl([("t", "CUBO DE ARESTA", GEO), ("m", r"L,\ \de=k,\ M=kL^3")], C62, 190, 34)
        self.pena(b1)
        self.col("E6-2", b1)

        self.gat("Pelo centro primeiro")
        self.degrau("C6.3b", "I_cm = k iiint (x^2 + y^2) dV, cubo centrado: -L/2 <= x, y, z <= L/2")
        q0 = v.P(0, 0)
        cmc = cm_mark(q0[0], q0[1], 15)
        self.play(FadeIn(cmc), run_time=0.3)
        b1b = mixl([("m", r"\Icm=k\iiint(\X^2+\Y^2)\,dV,"), ("t", "CENTRADO:", GEO), ("m", r"-\frac L2\le\X,\Y,\Z\le\frac L2")], C62, 245, 30)
        self.pena(b1b)
        self.col("E6-2", b1b)

        self.gat("A integral de x ao quadrado")
        self.degrau("C6.3", "iiint x^2 dV = int_{-L/2}^{L/2} x^2 dx * L * L = [x^3/3]_{-L/2}^{L/2} L^2 = (L^3/24 + L^3/24) L^2 = L^5/12")
        b2 = TC(r"\iiint\X^2dV=\int_{-L/2}^{L/2}\X^2\dX\cdot L\cdot L=\Big[\dfrac{\X^3}{3}\Big]_{-L/2}^{L/2}L^2=\Big(\dfrac{L^3}{24}+\dfrac{L^3}{24}\Big)L^2=\dfrac{L^5}{12}", C62, 330, 34)
        self.pena(b2)
        self.col("E6-2", b2)

        self.gat("O y ao quadrado dá o mesmo")
        self.degrau("C6.4", "I_cm = k(L^5/12 + L^5/12) = kL^5/6 = ML^2/6")
        b3 = TC(r"\Icm=k\Big(\dfrac{L^5}{12}+\dfrac{L^5}{12}\Big)=\dfrac{kL^5}{6}=\dfrac{ML^2}{6}", C62, 440, 42)
        self.pena(b3)
        self.col("E6-2", b3)

        self.gat("a meia diagonal")
        self.degrau("C6.5", "d = L/sqrt(2) (meia diagonal da face) => d^2 = L^2/2")
        pA = v.ponto((1, 1), AL, 10)
        fdd = v.linha([(0, 0), (1, 1)], LIL, 4)
        qd = v.P(.3, .62)
        gd = placa(r"\dd=\dfrac{L}{\sqrt2}", qd[0] - 20, qd[1] - 20, 28, "r")
        qa = v.P(1, 1)
        ea = mixl([("t", "ARESTA", BR)], 0, 0, 24)
        ea.shift(RIGHT * ((qa[0] + 10) / 120 - 8 - ea.get_center()[0]) + UP * ((540 - (qa[1] - 34)) / 120 - ea.get_center()[1]))
        gA = VGroup(placa_min(ea), ea)
        gA._txt = "ARESTA"
        self.play(Create(fdd), FadeIn(pA), run_time=0.5)
        self.pena(gd, gA)
        self.dentro(pn._painel, gd.f, ea)
        b4 = mixl([("m", r"\dd=\dfrac L{\sqrt2}"), ("t", "(MEIA DIAGONAL DA FACE)", GEO), ("m", r"\Rightarrow\ \dd^2=\dfrac{L^2}{2}")], C62, 560, 40)
        self.pena(b4)
        self.col("E6-2", b4)

        self.gat("Steiner")
        self.degrau("C6.6", "I_aresta = ML^2/6 + ML^2/2 = ML^2/6 + 3ML^2/6 = 4ML^2/6 = (2/3) ML^2")
        b5 = TC(r"I_{\mathrm{ARESTA}}=\dfrac{ML^2}{6}+\dfrac{ML^2}{2}=\dfrac{ML^2}{6}+\dfrac{3ML^2}{6}=\dfrac{4ML^2}{6}=\dfrac23\,ML^2", C62 + 10, 690, 40)
        self.pena(b5)
        mol5 = caixa_men(b5)
        self.play(Create(mol5), run_time=0.4)
        self.col("E6-2", b5)

        self.gat("sem atalho")
        self.degrau("C6.7", "confere direto: k int int int (x^2 + y^2) dz dy dx = k(L^5/3 + L^5/3) = (2/3) ML^2 ✓")
        b6 = mixl([("t", "CONFERE DIRETO:", MEN), ("m", r"k\int_0^L\!\!\int_0^L\!\!\int_0^L(\X^2+\Y^2)\,\dZ\,\dY\,\dX=k\Big(\dfrac{L^5}{3}+\dfrac{L^5}{3}\Big)=\dfrac23ML^2\ \Me{\checkmark}")],
                  C62, 840, 30)
        self.pena(b6)
        self.col("E6-2", b6)
        self.marca("23_E6-2")
        self._fecha(antes=0.35)
        self.sai(pn, lb, sq_f, sq_l, tL, cmc, pA, fdd, gd, gA, b1, b1b, b2, b3, b4, b5, mol5, b6, rt=0.35)

        # ── E6-3 · a bola encostada e o erro clássico (alvo 24, C6.8–C6.12, GM21) ─────────────────────────────
        self.an("E6-3")
        p1 = painel2d44(60, 160, 560, 360)
        lb1 = leg("BOLA COM EIXO TANGENTE", 84, 202, GEO, "left", 26)
        v1 = Vista2D(300, 360, 110)
        bfl = poly_px([v1.P(*p) for p in circ], mixh("#16123A", GEO, .30), 1.0, z=1)
        bln = v1.linha(circ, GEO, 3)
        q = v1.P(0, 0)
        cmb = cm_mark(q[0], q[1], 14)
        tg = v1.linha([(1, -1.3), (1, 1.3)], AL, 3, dash=(9, 7))
        rdl = v1.linha([(0, 0), (1, 0)], LIL, 4)
        q = v1.P(.5, 0)
        tdr = TC(r"\dd=R", q[0], q[1] + 26, 26, "c")
        self.titulo("A BOLA ENCOSTADA E O ERRO CLÁSSICO", rt=0.4, junto=[FadeIn(p1), FadeIn(bfl), Create(bln), FadeIn(cmb), Create(tg), Create(rdl)])
        self.pena(lb1)

        self.gat("uma bola girando em volta de uma reta que encosta nela")
        self.degrau("C6.8", "bola, eixo tangente: I = (2/5)MR^2 + MR^2 = (7/5)MR^2")
        self.pena(tdr)
        self.dentro(p1._painel, lb1, tdr)
        c1 = mixl([("t", "BOLA, EIXO TANGENTE:", GEO), ("m", r"I=\dfrac25MR^2+MR^2=\dfrac75\,MR^2")], C63 + 10, 250, 40)
        self.pena(c1)
        mol1 = caixa_men(c1)
        self.play(Create(mol1), run_time=0.4)
        self.col("E6-3", c1)

        self.gat("o erro clássico")
        self.degrau("C6.10", "erro clássico: I_B = I_A + M(2R)^2 = (3/2 + 4)MR^2 = (11/2)MR^2")
        p2 = painel2d44(60, 560, 560, 380)
        lb2 = leg("PAREDE → PAREDE OPOSTA", 84, 602, GEO, "left", 26)
        v2 = Vista2D(340, 770, 120)
        lfl = poly_px([v2.P(*p) for p in circ], mixh("#16123A", GEO, .30), 1.0, z=1)
        lln = v2.linha(circ, GEO, 3)
        pA2, pB2 = v2.ponto((-1, 0), AL, 10), v2.ponto((1, 0), AL, 10)
        q = v2.P(0, 0)
        cml = cm_mark(q[0], q[1], 14)
        qa, qb = v2.P(-1, 0), v2.P(1, 0)
        tA = TC("A", qa[0] - 26, qa[1], 28, "r")
        tB = TC("B", qb[0] + 24, qb[1], 28, "l")
        direta = v2.linha([(-1, .55), (1, .55)], AL, 3)
        self.pena(lb2, tA, tB, extra=[FadeIn(p2), FadeIn(lfl), Create(lln), FadeIn(pA2), FadeIn(pB2), FadeIn(cml), Create(direta)])
        self.dentro(p2._painel, lb2, tA, tB)
        xr = L([("x", r"\Al{\times}\ "), ("lhs", r"I_B="), ("ia", "I_A"), ("p", "+"), ("m2", r"M(2R)^2"), ("res", r"=\Big(\dfrac32+4\Big)MR^2=\dfrac{11}{2}MR^2")],
               C63 + 14, 430, 34)
        x0, y0 = pxof(xr.get_corner(UL))
        x1, y1 = pxof(xr.get_corner(DR))
        molx = moldura(C63, y0 - 12, (x1 - x0) + 28, (y1 - y0) + 24, AL, 1.0, 2, 8)
        self.pena(xr, extra=[Create(molx)])
        self.col("E6-3", xr)

        self.gat("Dá errado")
        qx = v2.P(0, .55)
        cx_ = cruz_px(qx[0], qx[1], AL, 1.0)
        risco = lin_px([pxof(gl(xr, "ia", "p", "m2").get_left()), pxof(gl(xr, "ia", "p", "m2").get_right())], AL, 3, z=30)
        self.play(Create(cx_), Create(risco), run_time=0.5)

        self.gat("volta primeiro ao centro")
        self.degrau("C6.12a", "✓ volta ao centro: I_cm = I_A - MR^2 = (3/2 - 1)MR^2 = MR^2/2")
        cam1 = v2.linha([(-1, -.1), (-.05, -.1)], MEN, 4)
        y3 = mixl([("m", r"\Me{\checkmark}"), ("t", "VOLTA AO CENTRO:", MEN), ("L", [("lhs", r"\Icm="), ("ia", "I_A"), ("m", r"-MR^2"),
                                                                                  ("res", r"=\Big(\dfrac32-1\Big)MR^2=\dfrac{MR^2}{2}")])], C63, 560, 38)
        self.play(Create(cam1), run_time=0.4)
        self.pena(y3.p[0], y3.p[1])
        self.gm(21, xr, y3.p[2], [("ia", "ia")], rt=1.0, copia=True, nota="GM21a: I_A + M(2R)^2 (riscado) -> I_A - MR^2 (volta ao centro)")
        self.col("E6-3", y3)

        self.gat("e depois vai")
        self.degrau("C6.12", "✓ vai à outra parede: I_B = MR^2/2 + MR^2 = (3/2)MR^2")
        cam2 = v2.linha([(.05, -.1), (1, -.1)], MEN, 4)
        y4 = mixl([("m", r"\Me{\checkmark}"), ("t", "VAI À OUTRA PAREDE:", MEN), ("L", [("lhs", r"I_B="), ("h", r"\dfrac{MR^2}{2}"), ("p", r"+MR^2"),
                                                                                     ("res", r"=\dfrac32\,MR^2")])], C63, 680, 38)
        self.play(Create(cam2), run_time=0.4)
        self.pena(y4.p[0], y4.p[1])
        self.gm(21, y3.p[2], y4.p[2], [("res", "h")], rt=1.0, copia=True, nota="GM21b: MR^2/2 -> + MR^2 (vai à outra parede)")
        self.col("E6-3", y4)

        self.gat("sempre passa pelo centro de massa")
        lg = leg("STEINER SEMPRE PASSA PELO CENTRO DE MASSA", C63, 820, MEN, "left", 32)
        self.pena(lg)
        self.col("E6-3", lg)
        self.marca("24_E6-3")

        self.sai_fim(rt=0.35)
