"""yt_0045 · Lote PH: H1 (a hélice na parede da lata, lata 2D em projeção oblíqua, alvo 01 v2) e H2 (só a parte ao longo do caminho trabalha, 2D, alvo 02)."""
from k45 import *  # noqa: F401,F403

COL = 1020
V2 = Vista2D(480, 600, 120)
fh = lambda s: (-3.4 + 6.6 * s, -1.6 + 2.2 * s + 1.0 * math.sin(PI * 1.6 * s))


class PH(B45):
    ANTES = None

    def corpo(self):
        # ── H1 · a hélice na parede da lata (alvo 01; v2: lata em projeção oblíqua 2D, no papel) ────────────────
        self.an("H1")
        self.titulo("A HÉLICE NA PAREDE DA LATA", rt=0)          # R8: o canto inteiro no quadro 0
        LT = Lata45(480, 780, 300, .20)
        C4 = 1 / (4 * PI)

        # R5: a lata e o eixo z entram na primeira palavra do H1; a hélice, no gatilho de sempre
        lata = LT.lata(1.0)
        Yc = lambda t: LT.pr(0, -1, C4 * t)[1]                   # R2: onde a frente da hélice cruza o eixo (x = CX)
        ez = LT.eixo(1.36, cortes=[LT.pr(0, -1, 1.0)[1]], pontes=[Yc(1.5 * PI), Yc(3.5 * PI)])
        rz = TC(r"\Z", 480, 330, 38, "c")
        self.play(Create(lata), Create(ez), run_time=1.2)

        self.gat("uma hélice enrolada na parede da lata")
        sqH, lqH = legq(HEL, "HÉLICE NA PAREDE DA LATA", 120, 1020, 28)
        hel = LT.helice(C4, 0, 4 * PI, HEL, 5, quebras=[1.5 * PI, 3.5 * PI])
        LT.cresce(self, hel, 1.7, {1.5 * PI: ez._pontes[Yc(1.5 * PI)], 3.5 * PI: ez._pontes[Yc(3.5 * PI)]}, junto=[FadeIn(sqH)])
        h1 = leg("LATA: RAIO 1, ALTURA 1", COL, 190, GEO, "left", 30)
        self.pena(rz, lqH, h1)
        self.col("H1", h1)

        self.gat("Em x, y e z")
        h2 = TC(r"\g(\Tt)=(\cos\Tt,\ \sen\Tt,\ c\,\Tt)", COL, 275, 48)
        self.pena(h2)
        self.col("H1", h2)

        self.gat("uma conta de colar")
        sqF, lqF = legq(CAMPO, "A FORÇA EMPURRA A CONTA", 560, 1020, 28)
        sF, pF, qF = LT.seta_F(3.62 * PI, C4, .30, 5, 20)         # R1: a conta na 2ª volta (frente); seta curta que não fura a base
        bola = ponto_px(pF[0], pF[1], BR, 11, z=9)
        self.play(FadeIn(bola), run_time=0.2)
        self.play(Create(sF), FadeIn(sqF), run_time=0.8)
        rF = TC(r"\Fv", qF[0] + 30, qF[1] - 24, 36, "c")
        LT.mede("H1 seta F", pF, qF, C4, tx=3.62 * PI, caixa=(pxof(rF.get_left())[0], pxof(rF.get_top())[1], pxof(rF.get_right())[0], pxof(rF.get_bottom())[1]))
        h3 = mixl([("m", r"\Fv"), ("t", "= UMA FORÇA EM CADA PONTO", BR)], COL, 370, 42)
        self.pena(rF, lqF)
        self.pena(*h3.p)
        self.col("H1", h3)

        self.gat("Quanto trabalho essa força faz numa volta")
        h4 = T("QUANTO TRABALHO", COL, 480, 48, "left", CI)
        h5 = T("NUMA VOLTA?", COL, 540, 48, "left", CI)
        self.pena(h4, h5)
        self.col("H1", h4, h5)

        self.gat("A curva não tem nenhum dos dois")
        h6 = leg("VOLUME? ÁREA?", COL, 650, GEO, "left", 30)
        h7 = leg("A CURVA NÃO TEM NENHUM DOS DOIS", COL, 695, GEO, "left", 30)
        self.pena(h6, h7)
        self.col("H1", h6, h7)
        self.marca("01_H1")

        # ── H2 · só a parte ao longo do caminho trabalha (alvo 02) ────────────────────────────────────────────
        self.an("H2")
        self.titulo("SÓ A PARTE AO LONGO DO CAMINHO TRABALHA", rt=0.3)
        self.limpa(rt=0.4)
        self.papel_vista(V2, rt=0.3)

        self.gat("conta presa no fio")
        cv = curva(V2, fh, 0, 1, HEL, 6)
        sv = sentido(V2, fh, .85)
        s0 = .42
        p, q = fh(s0), fh(s0 + .001)
        L_ = math.hypot(q[0] - p[0], q[1] - p[1])
        Tg = ((q[0] - p[0]) / L_, (q[1] - p[1]) / L_)
        Nr = (-Tg[1], Tg[0])
        a, b = 1.55, 1.05
        Fv = (a * Tg[0] + b * Nr[0], a * Tg[1] + b * Nr[1])
        pF = (p[0] + Fv[0], p[1] + Fv[1])
        sF = V2.seta(p, pF, CAMPO, 6, 22)
        sF.set_z_index(8)
        pt = V2.ponto(p, BR, 11)
        qF = V2.P(*pF)
        rF2 = placa_tc(r"\Fv", qF[0] + 14, qF[1] - 14, 38, "l")
        self.play(Create(cv), run_time=1.2)
        self.play(FadeIn(sv), FadeIn(pt), run_time=0.3)
        self.play(Create(sF), run_time=0.5)
        self.pena(rF2)

        self.gat("separa a força em duas partes")
        k1 = T("SÓ A PARTE DA FORÇA", COL, 250, 44, "left", BR)
        k2 = T("AO LONGO DO CAMINHO", COL, 310, 44, "left", LI)
        k3 = T("TRABALHA", COL, 370, 44, "left", BR)
        self.pena(k1, k2, k3)
        self.col("H2", k1, k2, k3)

        self.gat("A parte que aponta ao longo do caminho")
        pT = (p[0] + a * Tg[0], p[1] + a * Tg[1])
        sT = V2.seta(p, pT, LI, 4, 16)
        gT = lin_px([V2.P(*pT), V2.P(*pF)], GEO, 2, dash=(6, 6), z=5)
        sqL, lqL = legq(LI, "AO LONGO DO CAMINHO: TRABALHA", 120, 1020, 28)
        self.play(Create(sT), Create(gT), FadeIn(sqL), run_time=0.6)
        self.pena(lqL)

        self.gat("A parte de lado")
        pN = (p[0] + b * Nr[0], p[1] + b * Nr[1])
        sN = V2.seta(p, pN, GEO, 4, 16)
        gN = lin_px([V2.P(*pN), V2.P(*pF)], GEO, 2, dash=(6, 6), z=5)
        sqG, lqG = legq(GEO, "DE LADO: NÃO TRABALHA", 720, 1020, 28)
        self.play(Create(sN), Create(gN), FadeIn(sqG), run_time=0.6)
        self.pena(lqG)

        self.gat("corta o caminho em pedacinhos")
        tiques = []
        for k in range(9):
            s = k / 8
            c = V2.P(*fh(s))
            d = V2.P(*fh(min(1, s + .001)))
            if k == 8:
                d0 = V2.P(*fh(s - .001))
                d = (2 * c[0] - d0[0], 2 * c[1] - d0[1])
            ux, uy = d[0] - c[0], d[1] - c[1]
            Lq = math.hypot(ux, uy)
            nx, ny = -uy / Lq, ux / Lq
            tiques.append(lin_px([(c[0] - 12 * nx, c[1] - 12 * ny), (c[0] + 12 * nx, c[1] + 12 * ny)], GEO, 3, z=7))
        k4 = leg("CAMINHO EM PEDACINHOS:", COL, 500, GEO, "left", 32)
        k5 = leg("SOMA DE TRABALHINHOS", COL, 545, GEO, "left", 32)
        self.play(LaggedStart(*[Create(t) for t in tiques], lag_ratio=0.12), run_time=1.0)
        self.pena(k4, k5)
        self.col("H2", k4, k5)
        self.marca("02_H2")
        self.sai_fim(rt=0.35)
