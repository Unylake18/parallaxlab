"""yt_0045 · Lote PB7: B7-1 a B7-3 (a hélice da lata: montando; a conta; lendo a resposta). C8.1–C8.14, GM10–GM11, alvos 14 a 16.
v2: lata e hélice em projeção oblíqua 2D no papel (Lata45(300, 780, 240, ¼)), sem Three.js; coluna em 780. Uma volta (0 ≤ t ≤ 2π) é a conta; a 2ª volta fica em traço."""
from k45 import *  # noqa: F401,F403

C7 = 780
C4 = 1 / (4 * PI)


class PB7(B45):
    ANTES = "A ELIPSE E O DOBRO DA ÁREA"

    def corpo(self):
        # ── B7-1 · a hélice da lata: montando (alvo 14, C8.1–C8.3) ────────────────────────────────────────────
        self.an("B7-1")
        self.titulo("A HÉLICE DA LATA: MONTANDO")
        LT = Lata45(300, 780, 240, .25)
        lata = LT.lata(1.0)
        Yc = lambda t: LT.pr(0, -1, C4 * t)[1]                 # R2: cruzamentos da frente com o eixo z
        ez = LT.eixo(1.38, cortes=[LT.pr(0, -1, 1.0)[1]], pontes=[Yc(1.5 * PI), Yc(3.5 * PI)])
        rz = TC(r"\Z", 300, 415, 34, "c")
        hA = LT.helice(C4, 0, 2 * PI, HEL, 6, quebras=[1.5 * PI])
        hB = LT.helice(C4, 2 * PI, 4 * PI, "#A8794F", 3, HELB, zi=6, quebras=[3.5 * PI])   # R4: só entra no B7-3
        p0, p1 = LT.pr(1, 0, 0), LT.pr(1, 0, .5)
        b0, b1 = ponto_px(p0[0], p0[1], BR, 9, z=9), ponto_px(p1[0], p1[1], BR, 9, z=9)
        r0 = TC(r"\Tt=0", p0[0] + 22, p0[1] + 10, 26, "l")
        r2 = TC(r"\Tt=2\pi", p1[0] + 22, p1[1] + 10, 26, "l")

        self.play(Create(lata), Create(ez), run_time=0.55)      # a lata e o eixo entram junto do título: palco vazio ≤ 0,5 s
        self.gat("a hélice da lata")
        self.degrau("C8.1a", "gamma(t) = (cos t, sen t, c t), 0 <= t <= 2pi")
        sqU, lqU = legq(HEL, "UMA VOLTA: 0 ≤ t ≤ 2π", 120, 1020, 28)
        LT.cresce(self, hA, 1.2, {1.5 * PI: ez._pontes[Yc(1.5 * PI)]}, junto=[FadeIn(sqU)])
        self.play(FadeIn(b0), FadeIn(b1), run_time=0.5)
        self.pena(rz, r0, r2, lqU)
        a1 = TC(r"\g(\Tt)=(\cos\Tt,\ \sen\Tt,\ c\,\Tt),\quad 0\le\Tt\le2\pi", C7, 190, 46)
        self.pena(a1)
        self.col("B7-1", a1)

        self.gat("As duas primeiras componentes")
        sqF, lqF = legq(CAMPO, "F = REDEMOINHO + PESO", 470, 1020, 28)
        _st = [(t, LT.seta_F(t, C4, .18, 4, 15)) for t in (1.38 * PI, 1.62 * PI)]
        setas = [m for _, (m, _p, _q) in _st]
        for _t, (_m, _p, _q) in _st:
            LT.mede(f"B7 seta t={_t / PI:.2f}pi", _p, _q, C4, tx=_t, pts=[p0, p1], t0=0, t1=2 * PI)          # R3: duas setas curtas, longe do eixo e da base
        self.play(LaggedStart(*[Create(m) for m in setas], lag_ratio=0.05), FadeIn(sqF), run_time=1.0)
        self.pena(lqF)

        self.gat("Então F é menos y, x, menos um")
        self.degrau("C8.1b", "F(x, y, z) = (-y, x, -1)")
        a2 = TC(r"\Fv(\X,\Y,\Z)=(-\Y,\ \X,\ -1)", C7, 290, 48)
        self.pena(a2)
        self.col("B7-1", a2)

        self.gat("O redemoinho ajuda o tempo todo")
        cgA, cfA, cmA = chipm([("t", "REDEMOINHO: AJUDA", LI)], C7, 390, 32, LI)
        self.chip_pena(cgA, cfA, cmA)
        self.gat("O peso atrapalha o tempo todo")
        xA = pxof(cgA.get_right())[0]
        cgP, cfP, cmP = chipm([("t", "PESO: ATRAPALHA", AL)], xA + 30, 390, 32, AL)
        self.chip_pena(cgP, cfP, cmP)
        self.col("B7-1", cgA, cgP, chips=2)

        self.gat("o trabalho é a integral sobre gama")
        self.degrau("C8.2", "W = int_gamma -y dx + x dy - dz")
        a3 = TC(r"W=\int_{\g}-\Y\,\dX+\X\,\dY-\dZ", C7, 500, 50)
        self.pena(a3)
        self.col("B7-1", a3)

        self.gat("trocar tudo pelo t")
        self.degrau("C8.3", "dx = -sen t dt, dy = cos t dt, dz = c dt")
        a4 = TC(r"\dX=-\sen\Tt\,\dTt,\quad \dY=\cos\Tt\,\dTt,\quad \dZ=c\,\dTt", C7, 610, 44)
        self.pena(a4)
        self.col("B7-1", a4)
        self.marca("14_B7-1")

        # ── B7-2 · a hélice: a conta (alvo 15, C8.4–C8.9, GM10) ───────────────────────────────────────────────
        self.an("B7-2")
        self.titulo("A HÉLICE DA LATA: A CONTA", rt=0.3)

        self.gat("Menos y d x: menos seno")
        self.degrau("C8.4", "-y dx = -sen t . (-sen t dt) = sen^2 t dt")
        cgW, cfW, cmW = chip(r"W=\int_{\g}-\Y\,\dX+\X\,\dY-\dZ", C7, 180, 30)
        self.sobe_sai(a1, a2, cgA, cgP, a4)
        self.chip_vira(cgW, cfW, cmW, a3, nota="o W do B7-1 encolhe e vira o chip do topo")
        self.col_zera("B7-1")
        b1 = TC(r"-\Y\,\dX=-\sen\Tt\cdot(-\sen\Tt\,\dTt)=\sen^2\Tt\,\dTt", C7, 285, 42)
        self.pena(b1)
        self.col("B7-2", cgW, b1, chips=1)

        self.gat("x d y: cosseno vezes cosseno")
        self.degrau("C8.5", "x dy = cos t . cos t dt = cos^2 t dt")
        b2 = TC(r"\X\,\dY=\cos\Tt\cdot\cos\Tt\,\dTt=\cos^2\Tt\,\dTt", C7, 375, 42)
        self.pena(b2)
        self.col("B7-2", b2)

        self.gat("o menos d z")
        self.degrau("C8.6", "-dz = -c dt")
        b3 = TC(r"-\dZ=-c\,\dTt", C7, 460, 42)
        self.pena(b3)
        self.col("B7-2", b3)

        self.gat("Junta tudo debaixo da mesma integral")
        self.degrau("C8.7a", "W = int_0^2pi (sen^2 t + cos^2 t - c) dt")
        b4a = L([("pre", r"W=\int_0^{2\pi}("), ("sc", r"\sen^2\Tt+\cos^2\Tt"), ("mc", "-c"), ("pc", r")\,\dTt")], C7, 565, 42)
        self.pena(b4a)
        self.col("B7-2", b4a)

        self.gat("vira um")
        self.degrau("C8.7b", "= int_0^2pi (1 - c) dt")
        self.play(gl(b4a, "sc").animate.set_color(MEN), run_time=0.4)
        b4b = L([("eq", r"=\int_0^{2\pi}("), ("one", "1"), ("mc", "-c"), ("pc", r")\,\dTt")], C7, 565, 42)
        ao_lado(b4a, b4b, ultimo(b4a, "pc"), ultimo(b4b, "pc"), gap=12)
        self.gm(10, b4a, b4b, [("sc", "one"), ("mc", "mc"), ("pc", "pc")], rt=1.2, copia=True,
                nota="GM10: sen^2 t + cos^2 t - c -> 1 - c (o sen^2 + cos^2 acende menta e vira 1)")
        gl(b4a, "sc").set_color(MEN)                 # o destaque menta fica (alvo 15: \Me{sen²t + cos²t}); o gm por cópia restaura a cor antiga
        self.col("B7-2", b4b)

        self.gat("Integral de constante")
        self.degrau("C8.8", "= (1 - c)[t]_0^2pi = (1 - c)(2pi - 0)")
        b5 = TC(r"=(1-c)\Big[\Tt\Big]_0^{2\pi}=(1-c)(2\pi-0)", C7 + 40, 670, 42)
        self.pena(b5)
        self.col("B7-2", b5)

        self.gat("Distribuindo")
        self.degrau("C8.9", "= 2pi - 2pi c")
        b6 = L([("eq", "="), ("w", r"2\pi-2\pi c")], C7 + 40, 775, 52)
        self.pena(b6)
        m6 = caixa_men(b6, 16)
        self.play(Create(m6), run_time=0.4)
        self.col("B7-2", b6)
        self.marca("15_B7-2")

        # ── B7-3 · lendo a resposta (alvo 16, C8.10–C8.14, GM11) ──────────────────────────────────────────────
        self.an("B7-3")
        self.titulo("LENDO A RESPOSTA", rt=0.3)
        cgR, cfR, cmR = chip(r"W=2\pi-2\pi c", C7, 180, 32)
        self.sobe_sai(cgW, b1, b2, b3, b4a, b4b, b5)
        self.chip_vira(cgR, cfR, cmR, b6, sai=[m6], nota="o resultado do B7-2 encolhe e vira o chip do topo")
        self.col_zera("B7-2")
        self.col("B7-3", cgR, chips=1)

        self.gat("O dois pi veio do redemoinho")
        self.degrau("C8.10", "2pi = 2 . (pi . 1^2) = 2 x AREA DA TAMPA")
        sqT, lqT = legq(LI, "TAMPA: ÁREA π · 1²", 120, 1020, 28)
        sqS, lqS = legq(EZ, "SUBIDA NUMA VOLTA", 470, 1020, 28)
        bs = lata._partes
        self.play(bs["base_frente"].animate.set_stroke(LI, W(4)), bs["base_tras"].animate.set_stroke("#7E9A48", W(3)),
                  FadeOut(sqU), FadeOut(lqU), FadeIn(sqT), run_time=1.0)
        self.remove(sqU, lqU)
        self.pena(lqT)
        c1 = mixl([("m", r"2\pi=2\cdot(\pi\cdot1^2)=2\times"), ("t", "ÁREA DA TAMPA", LI), ("t", "· REDEMOINHO", GEO)], C7, 285, 40)
        self.pena(*c1.p)
        self.col("B7-3", c1)

        self.gat("E o menos dois pi c veio do peso")
        self.degrau("C8.11", "2pi c = z(2pi) - z(0) = SUBIDA NUMA VOLTA => -2pi c = -1 x SUBIDA")
        R0, R1 = (p0[0] + 120, p0[1]), (p1[0] + 120, p1[1])
        reg = VGroup(lin_px([R0, R1], EZ, 4, z=6), lin_px([(R0[0] - 10, R0[1]), (R0[0] + 10, R0[1])], EZ, 3, z=6),
                     lin_px([(R1[0] - 10, R1[1]), (R1[0] + 10, R1[1])], EZ, 3, z=6))
        self.play(Create(reg), FadeOut(sqF), FadeOut(lqF), FadeIn(sqS), run_time=1.0)
        self.remove(sqF, lqF)
        rs = TC(r"\Ez{2\pi c}", R0[0] + 16, (R0[1] + R1[1]) / 2 + 10, 28, "l")
        self.pena(rs, lqS)
        c2 = mixl([("m", r"2\pi c=\Z(2\pi)-\Z(0)"), ("t", "= SUBIDA NUMA VOLTA", EZ)], C7, 385, 40)
        c3 = mixl([("m", r"\Rightarrow\ -2\pi c=-1\times"), ("t", "SUBIDA", EZ), ("t", "· PESO", GEO)], C7 + 40, 465, 40)
        self.pena(*c2.p)
        self.pena(*c3.p)
        self.col("B7-3", c2, c3)

        self.gat("Na nossa lata")
        self.degrau("C8.12", "NOSSA LATA: 2 VOLTAS SOBEM 1 => 2pi c = 1/2 => c = 1/(4pi)")
        LT.cresce(self, hB, 1.5, {3.5 * PI: ez._pontes[Yc(3.5 * PI)]})                    # R4: a 2ª volta, em laranja apagado
        c4 = mixl([("t", "NOSSA LATA: 2 VOLTAS SOBEM 1", GEO), ("L", [("pre", r"\Rightarrow\ "), ("v", r"2\pi c=\tfrac12"), ("pos", r"\ \Rightarrow\ c=\tfrac{1}{4\pi}")])],
                  C7, 570, 38)
        self.pena(*c4.p)
        self.col("B7-3", c4)

        self.gat("O trabalho numa volta dá")
        self.degrau("C8.13", "W = 2pi - 1/2 ~ 5,78 > 0")
        c5a = L([("w", r"W="), ("a", r"2\pi-"), ("v", r"2\pi c")], C7, 685, 50)
        c5 = L([("w", r"W="), ("a", r"2\pi-"), ("v", r"\tfrac12"), ("r", r"\approx5{,}78>0")], C7, 685, 50)
        self.pena(c5a)
        self.gm(11, c5a, c5, [("w", "w"), ("a", "a")], voos=[(gl(c4.p[1], "v")[-3:], "v")], rt=1.0,
                nota="GM11: 2pi - 2pi c com 2pi c = 1/2 -> 2pi - 1/2 (o 1/2 voa da linha da lata)")
        m5 = caixa_men(c5, 16)
        g5 = leg("O REDEMOINHO GANHA", pxof(m5.get_right())[0] + 40 - 16, 698, LI, "left", 30)
        self.play(Create(m5), run_time=0.4)
        self.pena(g5)
        self.col("B7-3", c5)

        self.gat("E dá para empatar")
        self.degrau("C8.14", "W = 0 <=> 2pi - 2pi c = 0 <=> c = 1")
        c6 = TC(r"W=0\iff 2\pi-2\pi c=0\iff c=1", C7, 810, 44)
        self.pena(c6)
        self.col("B7-3", c6)
        self.marca("16_B7-3")
        self.sai_fim(rt=0.35)
