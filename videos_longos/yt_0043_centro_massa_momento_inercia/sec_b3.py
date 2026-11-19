"""yt_0043 · Lote PB3: B3-1 (energia e definição de I, C5), B3-2 (distância ao eixo), B3-3 (cilindro, C6, GM6), B3-4 (bola, C7, GM7–GM8), B3-5 (comparação e s_G, C8)."""
from k43 import *  # noqa: F401,F403

COL = 1020


class PB3(B43):
    ANTES = "A TAÇA: A CONTA"

    def corpo(self):
        # ── B3-1 · momento de inércia: de onde vem (alvo 10, C5) ───────────────────────────────────────────
        self.an("B3-1")
        pal1 = self.palco("giroCel", cam_alvo("b31"), seta=0.0, cel=0.0, fio=0.0, v=0.0)
        rz1 = self.rot3(pal1, "ez", r"\Z", size=38, ancora="c")
        pronto(rz1)
        self.add(pal1.fundo, rz1)
        self.titulo("MOMENTO DE INÉRCIA")

        self.gat("girando em volta do eixo")
        rom = self.rot3(pal1, "omega", r"\omega", dx=-34, dy=24, size=34, ancora="l")
        rfio = self.rot3(pal1, "fio", r"\S", dy=-34, size=36, ancora="c")
        rcel = self.rot3(pal1, "cel", r"\dm", dx=-72, dy=-18, size=30, ancora="l")
        self.play(*pal1.anim(rt=0.8, seta=1.0, cel=1.0, fio=1.0), FadeIn(rom[0]), FadeIn(rfio[0]), FadeIn(rcel[0]))
        self.pena(rom.f, rfio.f, rcel.f)

        self.gat("a velocidade de cada pedaço")
        rv = self.rot3(pal1, "v", "v", dx=14, dy=-8, size=34, ancora="l")
        self.degrau("C5.1", "v = omega s")
        f1 = TC(r"v=\omega\,\S", COL, 180, 50)
        self.play(*pal1.anim(rt=0.6, v=1.0), FadeIn(rv[0]))
        self.pena(rv.f, f1)
        self.col("B3-1", f1)

        self.gat("A energia de movimento")
        self.degrau("C5.2", "K = (1/2) dm v^2 = (1/2)(s^2 dm) omega^2")
        f2 = L([("pre", r"K=\dfrac12\,\dm\,v^2=\dfrac12\,("), ("s2dm", r"\S^2\,\dm"), ("pos", r")\,\omega^2")], COL, 300, 48)
        self.pena(f2)
        self.col("B3-1", f2)

        self.gat("o que fica do lado do ômega ao quadrado")
        self.sub(gl(f2, "s2dm"), rt=0.5, cor=LI)
        self.degrau("C5.3", "UM PONTO: I = m s^2")
        f3 = mixl([("t", "UM PONTO", GEO), ("m", r"I=m\,\S^2")], COL, 420, 46)
        self.pena(f3)
        self.col("B3-1", f3)

        self.gat("Com vários pedaços")
        self.degrau("C5.4", "VARIOS: I = sum m_i s_i^2")
        f4 = mixl([("t", "VÁRIOS", GEO), ("m", r"I=\sum m_i\,\S_i^2")], COL, 520, 46)
        self.pena(f4)
        self.col("B3-1", f4)

        self.gat("Num corpo contínuo")
        self.degrau("C5.5", "CORPO: I = iiint s^2 rho dV")
        t_cp = T("CORPO", COL, 668, 36, "left", GEO)
        f5 = TC(r"I=\iiint\S^2\,\de\,dV", COL + 190, 650, 52)
        mol5 = caixa_men(f5)
        self.pena(t_cp)
        self.pena(f5, extra=[Create(mol5)])
        self.col("B3-1", f5)

        self.gat("quilograma vezes metro ao quadrado")
        self.degrau("C5.6", "UNIDADE: kg . m^2")
        cg1, cf1, cm1_ = chipm([("t", "UNIDADE: kg · m²", GEO)], COL, 770, 30)
        self.chip_pena(cg1, cf1, cm1_)
        self.col("B3-1", cg1, chips=1)

        self.gat("A massa diz quanto custa empurrar")
        lg1 = leg("A MASSA RESISTE A EMPURRAR; O I RESISTE A GIRAR", COL, 880, GEO, "left", 28)
        self.pena(lg1)
        self.col("B3-1", lg1, chips=2)
        self.marca("10_B3-1")
        self._fecha(antes=0.7)
        self.sai(pal1.fundo, rz1, rom, rfio, rcel, rv, f1, f2, f3, f4, t_cp, f5, mol5, cg1, lg1, rt=0.35)
        pal2 = self.palco("distEixo", cam_alvo("b32"), P=1.0, s=0.0, fioX=0.0, r=0.0)
        rx2 = self.rot3(pal2, "ex", r"\X", size=38, ancora="c")
        ry2 = self.rot3(pal2, "ey", r"\Y", size=38, ancora="c")
        rz2 = self.rot3(pal2, "ez", r"\Z", size=38, ancora="c")
        rP2 = self.rot3(pal2, "P", "P", dx=16, dy=-24, size=36, ancora="l")
        for _r in (rx2, ry2, rz2, rP2):
            pronto(_r)
        self.add(pal2.fundo, rx2, ry2, rz2, rP2)
        self.titulo("DISTÂNCIA AO EIXO, NÃO À ORIGEM", rt=0.3)

        # ── B3-2 · distância ao eixo, não à origem (alvo 11) ──────────────────────────────────────────────
        self.an("B3-2")

        self.gat("a distância até o eixo, não até a origem")
        rs2 = self.rot3(pal2, "s", r"\S", dy=-30, size=36, ancora="c")
        sq_s, lg_s = legq(SOMB, "ATÉ O EIXO z: s", 120, 1020, 30)
        self.play(*pal2.anim(rt=0.6, s=1.0), FadeIn(rs2[0]), FadeIn(sq_s))
        self.pena(rs2.f, lg_s)

        self.gat("Para o eixo z")
        d1 = mixl([("t", "EIXO z:", EZ), ("m", r"\S^2=\X^2+\Y^2")], COL, 200, 50)
        self.pena(d1)
        self.col("B3-2", d1)

        self.gat("Se o eixo for o x")
        sq_x, lg_x = legq(GEO, "ATÉ O EIXO x", 440, 1020, 30)
        d2 = mixl([("t", "EIXO x:", E1), ("m", r"\Y^2+\Z^2")], COL, 310, 46)
        self.play(*pal2.anim(rt=0.6, fioX=1.0), FadeIn(sq_x))
        self.pena(lg_x, d2)
        self.col("B3-2", d2)

        self.gat("e para o eixo y")
        d3 = mixl([("t", "EIXO y:", E2), ("m", r"\X^2+\Z^2")], COL, 410, 46)
        self.pena(d3)
        self.col("B3-2", d3)

        self.gat("Em cartesianas, o momento em relação ao eixo z")
        d4 = TC(r"I_{\Z}=\iiint(\X^2+\Y^2)\,\de\,dV", COL, 540, 50)
        self.pena(d4)
        self.col("B3-2", d4)

        self.gat("o r é a distância até a origem")
        rr2 = self.rot3(pal2, "r", r"\R", dx=-42, dy=-14, size=36, ancora="l")
        sq_r, lg_r = legq(RO, "ATÉ A ORIGEM: r", 720, 1020, 30)
        sm2, st2 = selo("NÃO É  r² = x² + y² + z²", COL, 680, AL, 32)
        self.play(*pal2.anim(rt=0.6, r=1.0), FadeIn(rr2[0]), FadeIn(sq_r), Create(sm2))
        self.pena(rr2.f, lg_r, st2)
        self.col("B3-2", st2, chips=1)

        self.gat("Troca o eixo")
        lg2 = leg("OUTRO EIXO, OUTRO I", COL, 790, GEO, "left", 32)
        self.pena(lg2)
        self.col("B3-2", lg2, chips=2)
        self.marca("11_B3-2")
        self._fecha(antes=0.7)
        self.sai(pal2.fundo, rx2, ry2, rz2, rP2, rs2, rr2, sq_s, lg_s, sq_x, lg_x, sq_r, lg_r, d1, d2, d3, d4, sm2, st2, lg2, rt=0.35)
        pal3 = self.palco("cilindroH", cam_alvo("b33"), casca=0.0)
        rz3 = self.rot3(pal3, "ez", r"\Z", size=38, ancora="c")
        pronto(rz3)
        self.add(pal3.fundo, rz3)
        self.titulo("O CILINDRO UNIFORME", rt=0.3)

        # ── B3-3 · o cilindro homogêneo (alvo 12, C6, GM6) ────────────────────────────────────────────────
        self.an("B3-3")

        self.gat("o cilindro uniforme")
        rs3 = self.rot3(pal3, "s", r"\S", dy=-30, size=34, ancora="c")
        rR3 = self.rot3(pal3, "R", "R", dx=28, dy=-32, size=34, ancora="c")
        rh3 = self.rot3(pal3, "h", "h", dx=-84, dy=-2, size=36, ancora="l")
        self.play(FadeIn(rR3[0]), FadeIn(rh3[0]), run_time=0.25)
        self.pena(rR3.f, rh3.f)

        self.gat("o s ao quadrado da distância encontra o s do fator")
        # R10: a casca opaca pêssego e a placa s entram aqui, em s = 0,55 (como no alvo 12); o crescimento até a parede fica para o fim
        self.play(*pal3.anim(rt=0.6, casca=0.55), FadeIn(rs3[0]), run_time=0.6)
        self.pena(rs3.f)
        self.degrau("C6.1", "I_z = int_0^2pi int_0^R int_0^h s^2 * k * s dz ds dtheta")
        c61 = TC(r"I_{\Z}=\int_0^{2\pi}\!\!\int_0^R\!\!\int_0^h\S^2\cdot k\cdot\Js\,\dZ\,\dS\,\dT", COL, 190, 44)
        l_s3 = TC(r"\S^2\cdot\Js=\Li{s^3}", COL + 6, 268, 34)
        self.pena(c61)
        self.pena(l_s3)
        self.col("B3-3", c61, l_s3, chips=1)

        self.gat("as três integrais se separam")
        self.degrau("C6.2", "= k * [z]_0^h * [s^4/4]_0^R * [theta]_0^2pi")
        c62 = TC(r"=k\cdot\Big[\Z\Big]_0^h\cdot\Big[\dfrac{\S^4}{4}\Big]_0^R\cdot\Big[\T\Big]_0^{2\pi}", COL, 360, 44)
        self.pena(c62)
        self.col("B3-3", c62, chips=1)
        self.degrau("C6.2b", "= k * (h - 0) * (R^4/4 - 0) * (2pi - 0)   [G(b) - G(a)]")
        c62b = TC(r"=k\cdot(h-0)\cdot\Big(\dfrac{R^4}{4}-0\Big)\cdot(2\pi-0)", COL, 470, 44)
        self.pena(c62b)
        self.col("B3-3", c62b, chips=1)

        self.gat("Multiplica tudo")
        self.degrau("C6.3", "= k * h * R^4/4 * 2pi = pi k R^4 h / 2")
        c63 = TC(r"=\dfrac{\pi k R^4 h}{2}", COL, 590, 46)
        self.pena(c63)
        self.col("B3-3", c63, chips=1)

        self.gat("A massa do cilindro")
        self.degrau("C6.4", "M = k * pi R^2 h")
        c64 = TC(r"M=k\cdot\pi R^2h", COL + 430, 590, 46)
        self.pena(c64)
        c64.eh_chip = True                      # M = kπR²h na mesma linha da conta (não conta como linha própria)
        self.col("B3-3", c64, chips=1)

        self.gat("separa um R ao quadrado")
        self.degrau("C6.5", "I_z = (1/2)(k pi R^2 h) R^2 = (1/2) M R^2")
        c65a = L([("pre", r"I_{\Z}="), ("f", r"\dfrac{\pi k R^4 h}{2}")], COL + 10, 740, 52)
        c65b = L([("pre", r"I_{\Z}="), ("f", r"\dfrac12\,(k\pi R^2h)\,R^2"), ("res", r"=\dfrac12\,M R^2")], COL + 10, 740, 52)
        self.pena(c65a)
        mol6 = caixa_men(c65b)
        self.gm(6, c65a, c65b, [("pre", "pre"), ("f", "f")], rt=0.8, extra=[Create(mol6)], nota="GM6: pi k R^4 h / 2 -> 1/2 (k pi R^2 h) R^2")
        self.col("B3-3", c65b, chips=1)

        self.gat("Se toda a massa estivesse na parede")
        self.degrau("C6.6", "CASCA FINA: I = M R^2")
        sq6, lg6 = legq(SOMB, "A CASCA DE RAIO s: CRESCE ATÉ A PAREDE", 120, 1020, 30)
        c66 = mixl([("t", "CASCA FINA:", SOMB), ("m", r"I=M R^2")], COL, 880, 44)
        # A4/R10: a casca (já em s = 0,55) cresce até a parede R = 1, linear, uma vez só; o still 12 é s = 0,55
        self.play(FadeIn(sq6), run_time=0.25)
        self.pena(lg6, c66)
        self.col("B3-3", c66, chips=1)
        self.marca("12_B3-3", agora=True)
        self.play(*pal3.anim(rt=2.5, rate=linear, casca=1.0), FadeOut(rs3), run_time=2.5)
        self.wait(0.3)
        self._fecha(antes=0.7)
        self.sai(pal3.fundo, rz3, rs3, rR3, rh3, sq6, lg6, c61, l_s3, c62, c62b, c63, c64, c65b, mol6, c66, rt=0.35)
        pal4 = self.palco("esferaOct", cam_alvo("b34a"), P=1.0, r=1.0, phi=1.0, fio=0.0)
        rz4 = self.rot3(pal4, "ez", r"\Z", size=38, ancora="c")
        pronto(rz4)
        self.add(pal4.fundo, rz4)
        self.titulo("A BOLA UNIFORME", rt=0.3)

        # ── B3-4 · a esfera homogênea (alvos 13 e 13b, C7, GM7–GM8) ───────────────────────────────────────
        self.an("B3-4")

        self.gat("a bola uniforme")
        rr4 = self.rot3(pal4, "r", r"\R", dx=-32, dy=38, size=34, ancora="l")
        rphi4 = self.rot3(pal4, "phi", r"\F", dx=0, dy=0, size=32, ancora="c")       # R1: dentro do ângulo, a ~55 px do vértice, fora do arco
        rR4 = self.rot3(pal4, "R", "R", dx=10, dy=24, size=34, ancora="l")
        self.play(FadeIn(rr4[0]), FadeIn(rphi4[0]), FadeIn(rR4[0]), run_time=0.25)
        self.pena(rr4.f, rphi4.f, rR4.f)

        self.gat("a distância até o eixo é a sombra")
        rs4 = self.rot3(pal4, "s", r"\S", dy=-42, size=34, ancora="c")        # R1: 24 px acima do meio da sombra tracejada
        sq7, lg7 = legq(SOMB, "s = r sen φ: A SOMBRA É A DISTÂNCIA AO EIXO", 120, 1020, 30)
        self.degrau("C7.1", "s = r sen phi => s^2 = r^2 sen^2 phi")
        e1 = TC(r"\S=\R\sen\F\ \Rightarrow\ \S^2=\R^2\sen^2\F", COL, 220, 46)
        self.play(*pal4.anim(rt=0.6, fio=1.0), FadeIn(rs4[0]), FadeIn(sq7))
        self.pena(rs4.f, lg7, e1)
        self.col("B3-4a", e1)

        self.gat("o fator das esféricas")
        self.degrau("C7.2", "dV = r^2 sen phi dr dphi dtheta")
        cg7, cf7, cm7_ = chip(r"dV=\J\,\dR\,\dF\,\dT", COL, 320, 30, LI)
        self.chip_pena(cg7, cf7, cm7_)
        self.col("B3-4a", cg7, chips=1)

        self.gat("monta a integral")
        self.degrau("C7.3", "I_z = int_0^2pi int_0^pi int_0^R r^2 sen^2 phi * k * r^2 sen phi dr dphi dtheta")
        e2 = TC(r"I_{\Z}=\int_0^{2\pi}\!\!\int_0^\pi\!\!\int_0^R\R^2\sen^2\F\cdot k\cdot\J\,\dR\,\dF\,\dT", COL, 450, 42)
        self.pena(e2)
        self.col("B3-4a", e2, chips=1)

        self.gat("De novo tudo se separa")
        self.degrau("C7.4", "= k * 2pi * (int_0^pi sen^3 phi dphi) * R^5/5")
        e3 = TC(r"=k\cdot2\pi\cdot\Big(\int_0^\pi\sen^3\F\,\dF\Big)\cdot\dfrac{R^5}{5}", COL, 580, 46)
        self.pena(e3)
        self.col("B3-4a", e3, chips=1)

        self.gat("Seno ao cubo: guarda um seno")
        self.sobe_sai(e1, cg7, e2, e3, rt=0.35)
        cg_iz, cf_iz, cm_iz = chip(r"I_{\Z}=k\cdot2\pi\cdot\Big(\int_0^\pi\sen^3\F\,\dF\Big)\cdot\dfrac{R^5}{5}", COL, 140, 28)
        self.chip_pena(cg_iz, cf_iz, cm_iz)
        self.degrau("C7.5", "sen^3 phi = (1 - cos^2 phi) sen phi")
        s71 = TC(r"\sen^3\F=(1-\cos^2\F)\,\sen\F", COL, 260, 46)
        self.pena(s71)
        self.col("B3-4b", cg_iz, s71, chips=1)

        self.gat("Chama de u o cosseno")
        self.degrau("C7.6", "u = cos phi, du = -sen phi dphi")
        s72 = TC(r"\uu=\cos\F,\qquad \du=-\sen\F\,\dF", COL, 370, 46)
        self.pena(s72)
        self.col("B3-4b", s72, chips=1)

        self.gat("os limites invertem")
        self.degrau("C7.7", "phi = 0 -> u = 1, phi = pi -> u = -1")
        s73 = TC(r"\F=0\to\uu=1,\qquad \F=\pi\to\uu=-1", COL, 470, 44)
        self.pena(s73)
        self.col("B3-4b", s73, chips=1)

        self.gat("O menos do d u")
        self.degrau("C7.8", "int_0^pi sen^3 phi dphi = int_1^-1 (1 - u^2)(-du) = int_-1^1 (1 - u^2) du")
        s74a = L([("pre", r"\int_0^\pi\sen^3\F\,\dF="), ("int1", r"\int_1^{-1}(1-\uu^2)(-\du)")], COL, 600, 38)
        s74b = L([("pre", r"\int_0^\pi\sen^3\F\,\dF=\int_1^{-1}(1-\uu^2)(-\du)="), ("int2", r"\int_{-1}^1(1-\uu^2)\,\du")], COL, 600, 38)
        self.pena(s74a)
        self.gm(7, s74a, s74b, [("pre", "pre"), ("int1", "int2")], rt=0.75, nota="GM7: inversao dos limites com -du")
        self.col("B3-4b", s74b, chips=1)
        l7 = leg("O LIMITE INVERTE; O MENOS DO du DESVIRA", COL, 960, AL, "left", 30)
        self.pena(l7)
        self.col("B3-4b", l7, chips=2)

        self.gat("Aplica os limites")
        self.degrau("C7.9", "= [u - u^3/3]_-1^1 = (1 - 1/3) - (-1 + 1/3) = 4/3")
        s75 = TC(r"=\Big[\uu-\dfrac{\uu^3}{3}\Big]_{-1}^1=\Big(1-\dfrac13\Big)-\Big(-1+\dfrac13\Big)", COL + 40, 730, 40)
        self.pena(s75)
        self.col("B3-4b", s75, chips=1)
        self.degrau("C7.9b", "= 2/3 + 2/3 = 4/3")
        s76 = TC(r"=\dfrac23+\dfrac23=\dfrac43", COL + 40, 850, 44)
        self.pena(s76)
        self.col("B3-4b", s76, chips=2)
        self.marca("13_B3-4a", agora=True)

        self.gat("Junta tudo")
        self.sobe_sai(s71, s72, s73, s74b, s75, s76, l7, rt=0.35)
        cg_s3, cf_s3, cm_s3 = chip(r"\int_0^\pi\sen^3\F\,\dF=\dfrac43", COL, 245, 28)
        self.chip_pena(cg_s3, cf_s3, cm_s3)
        self.degrau("C7.10", "I_z = k * 2pi * 4/3 * R^5/5 = 8 pi k R^5 / 15")
        r71 = TC(r"I_{\Z}=k\cdot2\pi\cdot\dfrac43\cdot\dfrac{R^5}{5}=\dfrac{8\pi kR^5}{15}", COL, 380, 46)
        self.pena(r71)
        self.col("B3-4c", cg_iz, cg_s3, r71, chips=2)

        self.gat("o volume da bola")
        self.degrau("C7.11", "M = k * (4/3) pi R^3")
        r72 = TC(r"M=k\cdot\dfrac43\pi R^3", COL, 490, 46)
        self.pena(r72)
        self.col("B3-4c", r72, chips=2)

        self.wait(1.0)
        self.degrau("C7.12a", "I_z / M = (8 pi k R^5 / 15) / (4 pi k R^3 / 3)")
        d1 = TC(r"\dfrac{I_{\Z}}{M}=\dfrac{8\pi kR^5/15}{4\pi kR^3/3}", COL, 600, 44)
        self.pena(d1)
        self.col("B3-4c", d1, chips=2)
        self.degrau("C7.12b", "= (8/15)(3/4) R^2 = 24/60 R^2 = 2/5 R^2")
        d2 = TC(r"=\dfrac{8}{15}\cdot\dfrac34\,R^2=\dfrac{24}{60}\,R^2=\dfrac25\,R^2", COL, 715, 44)
        self.pena(d2)
        self.col("B3-4c", d2, chips=2)
        self.degrau("C7.12", "I_z = (8/15)/(4/3) MR^2 = (2/5) MR^2")
        r73a = L([("pre", r"I_{\Z}="), ("frac", r"\dfrac{8/15}{4/3}"), ("mr", r"\,MR^2")], COL + 10, 870, 52)
        r73b = L([("pre", r"I_{\Z}="), ("meio", r"\dfrac{8/15}{4/3}\,MR^2="), ("res", r"\dfrac25"), ("mr", r"\,MR^2")], COL + 10, 870, 52)
        self.pena(r73a)

        self.gat("Dois quintos de M R ao quadrado")
        mol7 = caixa_men(r73b)
        self.gm(8, r73a, r73b, [("pre", "pre"), ("frac", "res"), ("mr", "mr")], rt=0.65, extra=[Create(mol7)], nota="GM8: (8/15)/(4/3) -> 2/5")
        self.col("B3-4c", r73b, chips=2)
        self.marca("13b_B3-4b")
        # R12: os cartões do B3-5 começam a entrar enquanto a bola sai (nenhum quadro só de papel)
        cards_spec = [
            ("TUBO FINO", r"I=MR^2", 1.0, "tubo"),
            ("CILINDRO", r"I=\dfrac12\,MR^2", math.sqrt(0.5), "cil"),
            ("BOLA", r"I=\dfrac25\,MR^2", math.sqrt(0.4), "bola"),
        ]
        sgs = VGroup()
        sg_txts = []
        cards = []
        for i, (tit, form, sg, kind) in enumerate(cards_spec):
            X0 = 120 + i * 600
            pn = painel2d43(X0, 180, 480, 420)
            lb = leg(tit, X0 + 24, 226, GEO, "left", 28)
            v = Vista2D(X0 + 240, 520, 110)
            ez_l = v.linha([(0, -0.15), (0, 2.75)], EZ, 2, dash=(7, 6))
            if kind == "tubo":
                des = VGroup(v.linha([(-1.2, 0), (-1.2, 2.4)], GEO, 6), v.linha([(1.2, 0), (1.2, 2.4)], GEO, 6))
            elif kind == "cil":
                pts = [v.P(-1.2, 0), v.P(1.2, 0), v.P(1.2, 2.4), v.P(-1.2, 2.4)]
                des = VGroup(poly_px(pts, mixh("#16123A", GEO, 0.30), 1.0, z=1),
                             v.linha([(-1.2, 0), (1.2, 0), (1.2, 2.4), (-1.2, 2.4), (-1.2, 0)], GEO, 3))
            else:
                pts = [v.P(1.2 * math.cos(a), 1.2 + 1.2 * math.sin(a)) for a in np.linspace(0, 2 * PI, 81)]
                des = VGroup(poly_px(pts, mixh("#16123A", GEO, 0.30), 1.0, z=1),
                             lin_px(pts, GEO, 3, z=4))
            fm = TC(form, X0 + 240, 660, 44, "c")
            xs = 1.2 * sg
            ya, yb = (0.05, 2.35) if kind != "bola" else (1.2 - math.sqrt(1.44 - xs * xs) + 0.04, 1.2 + math.sqrt(1.44 - xs * xs) - 0.04)
            sg_l1 = v.linha([(xs, ya), (xs, yb)], SOMB, 4, dash=(10, 7))
            sg_l2 = v.linha([(-xs, ya), (-xs, yb)], SOMB, 4, dash=(10, 7))
            px_sg, py_sg = v.P(xs, 2.62)
            sg_t = TC(r"\Sg", px_sg + 22, py_sg, 30, "c")
            sgs.add(sg_l1, sg_l2)
            sg_txts.append(sg_t)
            cards.append((pn, ez_l, des, lb, fm))

        self._fecha(antes=0.55)
        self.sai(pal4.fundo, rz4, rr4, rphi4, rR4, rs4, sq7, lg7, cg_iz, cg_s3, r71, r72, d1, d2, r73b, mol7, rt=0.25,
                 extra=[FadeIn(cards[0][0]), Create(cards[0][1]), FadeIn(cards[0][2])])
        self.titulo("QUEM GIRA MAIS FÁCIL", rt=0.25)

        # ── B3-5 · quem gira mais fácil (alvo 14, 2D, C8) ─────────────────────────────────────────────────
        self.an("B3-5")

        self.gat("Coloca os três lado a lado")
        for _i, (_pn, _ez, _des, _lb, _fm) in enumerate(cards):
            if _i > 0:
                self.play(FadeIn(_pn), Create(_ez), FadeIn(_des), run_time=0.35)
            self.pena(_lb, _fm)

        self.gat("quanto da massa mora longe do eixo")
        X0_b, X1_b, Y_b = 420, 1500, 800
        barra = lin_px([(X0_b, Y_b), (X1_b, Y_b)], GEO, 3, z=6)
        ticks = VGroup()
        t_labs = []
        for val, lab in [(0.0, "0"), (0.4, "2/5"), (0.5, "1/2"), (1.0, "1")]:
            X = X0_b + (X1_b - X0_b) * val
            ticks.add(lin_px([(X, Y_b - 12), (X, Y_b + 12)], GEO, 3, z=6))
            t_labs.append(leg(lab, X, Y_b + 50, GEO, "center", 30))
        t_imr = leg("I / MR²", X1_b + 40, Y_b + 10, GEO, "left", 30)
        self.play(Create(barra), Create(ticks), run_time=0.45)
        self.pena(*t_labs, t_imr)

        self.gat("o raio de giração")
        self.degrau("C8.1", "I = M s_G^2; s_G = R, R/sqrt(2) approx 0,71 R, sqrt(2/5) R approx 0,63 R")
        f_sg = TC(r"I=M\,\Sg^2:\qquad \Sg=R,\qquad \dfrac{R}{\sqrt2}\approx0{,}71\,R,\qquad \sqrt{\dfrac25}\,R\approx0{,}63\,R", 960, 950, 40, "c")

        self.gat("num anel fininho")
        self.play(*[Create(s) for s in sgs], run_time=0.5)
        self.pena(*sg_txts, f_sg)
        self.marca("14_B3-5")

        self.sai_fim()
