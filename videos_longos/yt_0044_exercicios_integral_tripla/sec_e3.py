"""yt_0044 · Lote PE3: E3-1 a E3-4 (o cone: volume, z̄ e I_z em cilíndricas; o volume conferido em esféricas). C3.1–C3.18, GM11–GM15, alvos 12 a 15."""
from k44 import *  # noqa: F401,F403

COLM = 860
C34 = 700


class PE3(B44):
    ANTES = "ONDE O TETRAEDRO EQUILIBRA"

    def rots_cone(self, pal):
        rz = self.rot3(pal, "ez", r"\Z", size=34, ancora="c")
        rR = self.rot3(pal, "R", "R", size=30, ancora="c")
        rh = self.rot3(pal, "h", "h", size=30, ancora="l")
        return [rz, rR, rh]

    def corpo(self):
        # ── E3-1 · o cone: montar em cilíndricas (alvo 12, C3.1–C3.4, GM11) ─────────────────────────────────
        self.an("E3-1")
        pal = self.palco("cone", OM, sonda=0.0)
        rots = self.rots_cone(pal)
        self.titulo("O CONE: MONTAR EM CILÍNDRICAS", rt=0.5, junto=self.ent3d(pal))

        self.gat("um cone de sorvete")
        self.pena(*rots)

        self.gat("a parede do cone")
        self.degrau("C3.1a", "CONE: (h/R)s <= z <= h, rho = k (entra na parede z = (h/R)s, sai na tampa z = h)")
        l1 = mixl([("t", "CONE:", GEO), ("m", r"\dfrac hR\,\S\le\Z\le h,\ \ \de=k")], COLM, 180, 40)
        sqE, lgE = legq(AZC, "ENTRA NA PAREDE z = (h/R)s", 120, 1020, 30)
        self.pena(l1)
        self.play(FadeIn(sqE), run_time=0.2)
        self.pena(lgE)
        self.col("E3-1", l1)

        self.gat("sombra é o disco")
        self.degrau("C3.1b", "SOMBRA: 0 <= s <= R, 0 <= theta <= 2pi")
        l2 = mixl([("t", "SOMBRA:", SOMB), ("m", r"0\le\S\le R,\ \ 0\le\T\le2\pi")], COLM, 280, 40)
        self.pena(l2)
        self.col("E3-1", l2)

        self.gat("Segunda pergunta")
        self.degrau("C3.1c", "dV = s ds dtheta dz; V = int_0^2pi int_0^R int_{hs/R}^h s dz ds dtheta")
        cg_dv, cf_dv, cm_dv = chip(r"dV=\Js\,\dS\,\dT\,\dZ", COLM + 600, 280, 28, LI)
        self.chip_pena(cg_dv, cf_dv, cm_dv)
        l3 = L([("pre", r"V=\int_0^{2\pi}\!\!\int_0^R\!\!\int_{h\S/R}^{h}"), ("js", r"\Js"), ("pos", r"\,\dZ\,\dS\,\dT")], COLM, 390, 44)
        self.escreve(l3, voos=[(VGroup(cf_dv[0][3]), "js")], rt_voo=0.9, nota="o s lima (fator do volume) voa do chip dV")
        self.col("E3-1", l3, cg_dv, chips=1)

        self.gat("A sonda entra")
        self.degrau("C3.2", "int_{hs/R}^h s dz = s[z]_{hs/R}^h = s(h - hs/R) = hs - (h/R)s^2")
        sqS, lgS = legq(CORAL, "SAI NA TAMPA z = h", 560, 1020, 30)
        self.play(*pal.anim(1.4, sonda=1.0), FadeIn(sqS), run_time=1.4)
        self.pena(lgS)
        l4a = L([("pre", r"\int_{h\S/R}^{h}\S\,\dZ=\S\Big[\Z\Big]_{h\S/R}^{h}="), ("s", r"\S"), ("p1", r"\Big("), ("h", "h"), ("m", "-"),
                 ("fr", r"\dfrac{h\S}{R}"), ("p2", r"\Big)")], COLM, 510, 40)
        self.pena(l4a)
        l4b = L([("eq", "="), ("h", "h"), ("s", r"\S"), ("m", "-"), ("fr", r"\dfrac hR"), ("s2", r"\S^2")], COLM, 510, 40)
        ao_lado(l4a, l4b, ultimo(l4a, "pre"), 0, gap=14)
        self.gm(11, l4a, l4b, [("s", "s"), ("h", "h"), ("m", "m"), ("fr", ["fr", "s2"])], rt=1.0, copia=True,
                nota="GM11: s(h - hs/R) -> hs - (h/R)s^2")
        self.col("E3-1", l4a, l4b, chips=1)

        self.gat("Agora em s")
        self.degrau("C3.3", "int_0^R (hs - (h/R)s^2) ds = [hs^2/2 - (h/R)s^3/3]_0^R = hR^2/2 - hR^2/3 = hR^2/6")
        l5 = TC(r"\int_0^R\Big(h\S-\dfrac hR\S^2\Big)\dS=\Big[\dfrac{h\S^2}{2}-\dfrac hR\dfrac{\S^3}{3}\Big]_0^R=\dfrac{hR^2}{2}-\dfrac{hR^2}{3}=\dfrac{hR^2}{6}",
                COLM, 640, 38)
        self.pena(l5)
        self.col("E3-1", l5, chips=1)

        self.gat("a volta inteira")
        self.degrau("C3.4", "V = 2pi * hR^2/6 = pi R^2 h/3 (um terço do cilindro)")
        l6 = TC(r"V=2\pi\cdot\dfrac{hR^2}{6}=\dfrac{\pi R^2h}{3}", COLM + 10, 780, 50)
        self.pena(l6)
        mol6 = caixa_men(l6)
        lg6 = leg("UM TERÇO DO CILINDRO", COLM + 560, 790, GEO, "left", 28)
        self.play(Create(mol6), run_time=0.4)
        self.pena(lg6)
        self.col("E3-1", l6, lg6, chips=1)
        self.marca("12_E3-1")
        self._fecha(antes=0.9)
        # a coluna do E3-1 sai (o V vira chip no E3-2, voando da moldura); a sonda e as legendas de entra/sai saem junto
        cg_v, cf_v, cm_v = chip(r"V=\dfrac{\pi R^2h}{3}", COLM, 140, 28)
        self.sobe_sai(l1, l2, l3, cg_dv, l4a, l4b, l5, lg6, sqE, lgE, sqS, lgS, rt=0.3)
        self.chip_vira(cg_v, cf_v, cm_v, l6, sai=[mol6], rt=0.45, nota="o V do E3-1 vira o chip do E3-2")

        # ── E3-2 · o cone: onde ele equilibra (alvo 13, C3.5–C3.8) ───────────────────────────────────────────
        self.an("E3-2")
        pal, rots = self.troca3d(pal, rots, "coneCm", OM, cm=0.0, cotas=0.0,
                                 rots=[("ez", r"\Z", dict(size=34, ancora="c")), ("R", "R", dict(size=30, ancora="c"))])
        self.titulo("O CONE: ONDE ELE EQUILIBRA", rt=0.3)
        self.col("E3-2", cg_v, chips=1)

        self.gat("acima da metade")
        g12 = self.rot3(pal, "z12", r"\dfrac h2", size=26, ancora="c")
        sqT, lgT = legq(GEO, "TRACEJADO: METADE DA ALTURA", 440, 1020, 30)
        self.play(*pal.anim(0.5, cm=1.0), FadeIn(sqT), run_time=0.5)
        self.pena(g12, lgT)

        self.gat("A mesma montagem")
        self.degrau("C3.5a", "iiint z dV = int_0^2pi int_0^R int_{hs/R}^h z s dz ds dtheta")
        m1 = TC(r"\iiint\Z\,dV=\int_0^{2\pi}\!\!\int_0^R\!\!\int_{h\S/R}^{h}\Z\,\Js\,\dZ\,\dS\,\dT", COLM, 270, 42)
        self.pena(m1)
        self.col("E3-2", m1, chips=1)

        self.gat("a primitiva de z")
        self.degrau("C3.5", "int z s dz = s[z^2/2]_{hs/R}^h = s(h^2/2 - h^2 s^2/(2R^2)) = h^2 s/2 - h^2 s^3/(2R^2)")
        m2 = TC(r"\int_{h\S/R}^{h}\Z\,\S\,\dZ=\S\Big[\dfrac{\Z^2}{2}\Big]_{h\S/R}^{h}=\S\Big(\dfrac{h^2}{2}-\dfrac{h^2\S^2}{2R^2}\Big)=\dfrac{h^2\S}{2}-\dfrac{h^2\S^3}{2R^2}",
                COLM, 400, 36)
        self.pena(m2)
        self.col("E3-2", m2, chips=1)

        self.gat("Em s")
        self.degrau("C3.6", "int_0^R (...) ds = [h^2 s^2/4 - h^2 s^4/(8R^2)]_0^R = h^2R^2/4 - h^2R^2/8 = h^2R^2/8")
        m3 = TC(r"\int_0^R\Big(\dfrac{h^2\S}{2}-\dfrac{h^2\S^3}{2R^2}\Big)\dS=\Big[\dfrac{h^2\S^2}{4}-\dfrac{h^2\S^4}{8R^2}\Big]_0^R=\dfrac{h^2R^2}{4}-\dfrac{h^2R^2}{8}=\dfrac{h^2R^2}{8}",
                COLM, 530, 34)
        self.pena(m3)
        self.col("E3-2", m3, chips=1)

        self.gat("Vezes dois pi")
        self.degrau("C3.7", "iiint z dV = 2pi * h^2R^2/8 = pi R^2 h^2/4")
        m4 = TC(r"\iiint\Z\,dV=2\pi\cdot\dfrac{h^2R^2}{8}=\dfrac{\pi R^2h^2}{4}", COLM, 650, 42)
        self.pena(m4)
        self.col("E3-2", m4, chips=1)

        self.gat("divide pelo volume")
        self.degrau("C3.8", "zbar = (pi R^2 h^2/4)/(pi R^2 h/3) = 3h/4 (do vértice)")
        m5 = TC(r"\zb=\dfrac{\pi R^2h^2/4}{\pi R^2h/3}=\dfrac{3h}{4}", COLM + 10, 780, 50)
        self.pena(m5)
        mol5 = caixa_men(m5)
        x34, y34 = pal.pt("z34")
        cm5 = cm_mark(x34, y34, 14)
        g34 = self.rot3(pal, "c34", r"\dfrac{3h}{4}", size=26, ancora="l")
        sqC, lgC = legq(LIL, "CENTRO DE MASSA", 120, 1020, 30)
        self.play(Create(mol5), FadeIn(cm5), FadeIn(sqC), *pal.anim(0.5, cotas=1.0), run_time=0.5)
        self.pena(g34, lgC)
        self.col("E3-2", m5, chips=1)

        self.gat("a um quarto da altura")
        lg5 = leg("DO VÉRTICE: 3h/4 · DA TAMPA: h − 3h/4 = h/4", COLM, 910, GEO, "left", 28)
        gh4 = self.rot3(pal, "c14", r"\dfrac{h}{4}", size=26, ancora="l")
        self.pena(gh4, lg5)
        self.col("E3-2", lg5, chips=1)
        self.marca("13_E3-2")
        self._fecha(antes=0.9)
        cg_z, cf_z, cm_z = chip(r"\zb=\dfrac{3h}{4}", COLM, 140, 28)
        self.sobe_sai(cg_v, m1, m2, m3, m4, lg5, g12, cm5, g34, gh4, sqT, lgT, sqC, lgC, rt=0.3)
        self.chip_vira(cg_z, cf_z, cm_z, m5, sai=[mol5], rt=0.45, nota="o z barra do E3-2 vira o chip do E3-3")

        # ── E3-3 · o cone: quanto custa girar (alvo 14, C3.9–C3.12, GM12, GM13) ─────────────────────────────
        self.an("E3-3")
        pal, rots = self.troca3d(pal, rots, "coneCasca", OM, casca=0.0,
                                 rots=[("ez", r"\Z", dict(size=34, ancora="c")), ("R", "R", dict(size=30, ancora="c")),
                                       ("h", "h", dict(size=30, ancora="l"))])
        self.titulo("O CONE: QUANTO CUSTA GIRAR", rt=0.25)
        self.col("E3-3", cg_z, chips=1)

        self.gat("quanto custa girar o cone")
        self.degrau("C3.9a", "I_z = int_0^2pi int_0^R int_{hs/R}^h s^2 * k * s dz ds dtheta (s^2 da distância, s do fator)")
        rs = self.rot3(pal, "s", r"\S", size=28, ancora="c")
        sqK, lgK = legq(SOMB, "CASCA DE RAIO s: TODA À MESMA DISTÂNCIA DO EIXO", 120, 1020, 30)
        self.play(*pal.anim(1.2, casca=1.0), FadeIn(sqK), run_time=1.2)
        self.pena(rs, lgK)
        i1 = L([("pre", r"I_{\Z}=\int_0^{2\pi}\!\!\int_0^R\!\!\int_{h\S/R}^{h}"), ("s2", r"\S^2"), ("k", r"\cdot k\cdot"), ("js", r"\Js"),
                ("pos", r"\,\dZ\,\dS\,\dT")], COLM, 260, 42)
        self.pena(i1)
        self.col("E3-3", i1, chips=1)

        self.gat("s ao cubo")
        i1b = L([("s2", r"\Li{s^2}"), ("dot", r"\mathbin{\Li{\cdot}}"), ("s", r"\Li{s}"), ("res", r"\mathrel{\Li{=}}\Li{s^3}")], COLM + 620, 262, 30)
        i1b.shift(UP * (i1[0][sel(i1, "s2")[0]].get_bottom()[1] - i1b[0][0].get_bottom()[1]))
        self.gm(12, i1, i1b, [("s2", "s2"), ("js", "s")], rt=0.9, copia=True, nota="GM12: s^2 * s -> s^3 (chave lima)")
        self.col("E3-3", i1b, chips=1)

        self.gat("o comprimento da sonda")
        self.degrau("C3.9", "int_{hs/R}^h s^3 dz = s^3(h - hs/R) = hs^3 - (h/R)s^4")
        i2 = TC(r"\int_{h\S/R}^{h}\S^3\,\dZ=\S^3\Big(h-\dfrac{h\S}{R}\Big)=h\S^3-\dfrac hR\S^4", COLM, 380, 40)
        self.pena(i2)
        self.col("E3-3", i2, chips=1)

        self.gat("Em s um quarto menos um quinto")
        self.degrau("C3.10", "int_0^R (hs^3 - (h/R)s^4) ds = [hs^4/4 - (h/R)s^5/5]_0^R = hR^4/4 - hR^4/5 = hR^4/20")
        i3 = TC(r"\int_0^R\Big(h\S^3-\dfrac hR\S^4\Big)\dS=\Big[\dfrac{h\S^4}{4}-\dfrac hR\dfrac{\S^5}{5}\Big]_0^R=\dfrac{hR^4}{4}-\dfrac{hR^4}{5}=\dfrac{hR^4}{20}",
                COLM, 500, 36)
        self.pena(i3)
        self.col("E3-3", i3, chips=1)

        self.gat("Vezes k")
        self.degrau("C3.11", "I_z = k * 2pi * hR^4/20 = pi k R^4 h/10")
        i4 = TC(r"I_{\Z}=k\cdot2\pi\cdot\dfrac{hR^4}{20}=\dfrac{\pi kR^4h}{10}", COLM, 620, 42)
        self.pena(i4)
        self.col("E3-3", i4, chips=1)

        self.gat("a massa, que é")
        self.degrau("C3.12a", "M = k * pi R^2 h/3")
        i4m = TC(r"M=k\cdot\dfrac{\pi R^2h}{3}", COLM + 575, 620, 42)
        self.pena(i4m)
        self.col("E3-3", i4m, chips=1)

        self.gat("Dividindo um pelo outro")
        self.degrau("C3.12", "I_z = (pi k R^4 h/10)/(pi k R^2 h/3) * MR^2 = (3/10) MR^2")
        i5a = L([("lhs", r"I_{\Z}="), ("fr", r"\dfrac{\pi kR^4h/10}{\pi kR^2h/3}"), ("mr", r"\,MR^2")], COLM + 10, 760, 50)
        self.pena(i5a)
        fr_ix = sel(i5a, "fr")
        # π, k, h acendem (sublinhado ciano) e saem: glifos π k … h do numerador e do denominador
        acende = VGroup(*[i5a[0][fr_ix[j]] for j in (0, 1, 4, 9, 10, 13) if j < len(fr_ix)])
        self.sub(acende, rt=0.5, cor=CI)
        i5b = L([("eq", "="), ("tr", r"\dfrac{3}{10}"), ("mr", r"\,MR^2")], COLM + 10, 760, 50)
        ao_lado(i5a, i5b, sel(i5a, "lhs")[-1], 0, gap=14)
        self.gm(13, i5a, i5b, [("fr", "tr"), ("mr", "mr")], rt=1.0, copia=True, nota="GM13: (pi k R^4 h/10)/(pi k R^2 h/3) -> 3/10 (pi, k, h saem)")
        x0, y0 = pxof(i5a.get_corner(UL))
        x1, y1 = pxof(i5b.get_corner(DR))
        mol_i = moldura(x0 - 14, min(y0, pxof(i5b.get_corner(UL))[1]) - 10, (x1 - x0) + 28, (max(y1, pxof(i5a.get_corner(DR))[1]) - min(y0, pxof(i5b.get_corner(UL))[1])) + 20,
                        MEN, 1.0, 3, 12)
        self.play(Create(mol_i), run_time=0.4)
        self.col("E3-3", i5a, i5b, chips=1)

        self.gat("três décimos")
        lg_i = leg("CILINDRO 1/2 · CONE 3/10: A MASSA DO CONE MORA PERTO DO EIXO", COLM, 900, GEO, "left", 26)
        self.pena(lg_i)
        self.col("E3-3", lg_i, chips=1)
        self.marca("14_E3-3")
        self._fecha(antes=0.9)
        cg_vc, cf_vc, cm_vc = chipm([("m", r"V=\dfrac{\pi R^2h}{3}"), ("t", "(CILÍNDRICAS)", BR)], C34, 140, 28)
        self.sobe_sai(cg_z, i1, i1b, i2, i3, i4, i4m, i5a, i5b, mol_i, lg_i, rs, sqK, lgK, rt=0.35)
        self.sai(pal.fundo, *rots, rt=0.4)

        # ── E3-4 · conferindo o volume em esféricas (alvo 15, C3.14–C3.18, GM14, GM15) ──────────────────────
        self.an("E3-4")
        self.titulo("CONFERINDO EM ESFÉRICAS", rt=0.3)
        self.chip_pena(cg_vc, cf_vc, cm_vc)
        self.col("E3-4", cg_vc, chips=1)

        self.gat("nas esféricas")
        self.degrau("C3.14a", "0 <= phi <= alpha, tg alpha = R/h")
        pn = painel2d44(60, 160, 560, 780)
        lb = leg("CORTE PELO EIXO", 84, 202, GEO, "left", 26)
        v = Vista2D(130, 860, 360)
        Hh, Rr, ph = 1.4, 1.0, 0.38
        fill = poly_px([v.P(0, 0), v.P(Rr, Hh), v.P(0, Hh)], mixh("#16123A", GEO, 0.22), 1.0, z=1)
        cont = v.linha([(0, 0), (Rr, Hh), (0, Hh)], GEO, 3)
        eixo = v.linha([(0, -.05), (0, 1.8)], EZ, 3)
        a_al = math.atan(Rr / Hh)
        arc_al = lin_px([(130 + 110 * math.sin(a * a_al / 30), 860 - 110 * math.cos(a * a_al / 30)) for a in range(31)], FI, 3, z=6)
        p_al = v.P(.36, .46)
        t_al = TC(r"\al", p_al[0] + 20, p_al[1] - 40, 30, "l")
        lg_tg = leg("tg α = R/h", 90, 900, FI, "left", 28)
        f1a = TC(r"0\le\F\le\al,\quad \tg\al=\dfrac Rh;", C34, 250, 38)
        self.play(FadeIn(pn), FadeIn(fill), Create(cont), Create(eixo), Create(arc_al), run_time=0.6)
        self.pena(lb, t_al, lg_tg)
        self.pena(f1a)
        self.dentro(pn._painel, lb, t_al, lg_tg)
        self.col("E3-4", f1a, chips=1)

        self.gat("o raio sai pela tampa")
        self.degrau("C3.14", "tampa z = h: r cos phi = h => r = h/cos phi")
        raio = v.linha([(0, 0), (Hh * math.tan(ph), Hh)], RO, 5)
        arc_ph = lin_px([(130 + 70 * math.sin(a * ph / 20), 860 - 70 * math.cos(a * ph / 20)) for a in range(21)], FI, 3, z=6)
        p_ph = v.P(.08, .26)
        t_ph = TC(r"\F", p_ph[0], p_ph[1], 26, "c")
        p_r = v.P(.6, .9)
        t_r = TC(r"\R=\dfrac{h}{\cos\F}", p_r[0] - 180, p_r[1] - 40, 28, "l")
        g_r = VGroup(placa_min(t_r), t_r)
        g_r._txt = "r = h/cos φ"
        p_zh = v.P(.3, Hh)
        t_zh = TC(r"\Z=h", p_zh[0], p_zh[1] - 26, 28, "l")
        p_R = v.P(.5, Hh)
        t_R = TC("R", p_R[0] + 40, p_R[1] - 26, 28, "l")
        self.play(Create(raio), Create(arc_ph), run_time=0.5)
        self.pena(t_ph, g_r, t_zh, t_R)
        self.dentro(pn._painel, t_ph, t_zh, t_R)
        f1b = TC(r"\Z=h:\ \R\cos\F=h\Rightarrow\R=\dfrac h{\cos\F}", C34, 250, 38)
        f1b.shift(RIGHT * (pxof(f1a.get_right())[0] + 70 - pxof(f1b.get_left())[0]) / 120)
        self.pena(f1b)
        self.col("E3-4", f1b, chips=1)

        self.gat("Monta a integral")
        self.degrau("C3.14b", "V = int_0^2pi int_0^alpha int_0^{h/cos phi} r^2 sen phi dr dphi dtheta")
        f2 = TC(r"V=\int_0^{2\pi}\!\!\int_0^{\al}\!\!\int_0^{h/\cos\F}\Jr\,\dR\,\dF\,\dT", C34, 360, 42)
        self.pena(f2)
        self.col("E3-4", f2, chips=1)

        self.gat("A de dentro, em r")
        self.degrau("C3.15", "int_0^{h/cos phi} r^2 dr = [r^3/3]_0^{h/cos phi} = h^3/(3 cos^3 phi)")
        f3 = TC(r"\int_0^{h/\cos\F}\R^2\dR=\Big[\dfrac{\R^3}{3}\Big]_0^{h/\cos\F}=\dfrac{h^3}{3\cos^3\F}", C34, 470, 38)
        self.pena(f3)
        self.col("E3-4", f3, chips=1)

        self.gat("uma substituição")
        self.degrau("C3.16a", "u = cos phi, du = -sen phi dphi; phi = 0 -> u = 1; phi = alpha -> u = cos alpha")
        f4 = TC(r"\uu=\cos\F,\ \du=-\sen\F\,\dF;\quad \F=0\to\uu=1;\ \ \F=\al\to\uu=\cos\al", C34, 570, 36)
        self.pena(f4)
        self.col("E3-4", f4, chips=1)

        self.gat("vira uma potência")
        self.degrau("C3.16", "(h^3/3) int_0^alpha sen phi/cos^3 phi dphi = (h^3/3) int_1^{cos alpha} -u^{-3} du = (h^3/3)[u^{-2}/2]_1^{cos alpha}")
        f5a = L([("c1", r"\dfrac{h^3}{3}"), ("int", r"\int_0^{\al}"), ("fr", r"\dfrac{\sen\F}{\cos^3\F}"), ("df", r"\dF")], C34, 680, 36)
        self.pena(f5a)
        f5b = L([("eq", "="), ("c1", r"\dfrac{h^3}{3}"), ("int", r"\int_1^{\cos\al}"), ("u", r"\!-\uu^{-3}"), ("du", r"\du")], C34, 680, 36)
        ao_lado(f5a, f5b, sel(f5a, "c1")[1], 0, gap=14)
        f5b.shift(UP * (f5a.get_center()[1] - f5b.get_center()[1]))
        self.gm(14, f5a, f5b, [("c1", "c1"), ("int", "int"), ("fr", "u"), ("df", "du")], rt=1.1, copia=True,
                nota="GM14: sen phi/cos^3 phi dphi -> -u^{-3} du; limites 0, alpha -> 1, cos alpha")
        f5c = TC(r"=\dfrac{h^3}{3}\Big[\dfrac{\uu^{-2}}{2}\Big]_1^{\cos\al}", C34, 680, 36)
        f5c.shift(RIGHT * (pxof(f5b.get_right())[0] + 14 - pxof(f5c.get_left())[0]) / 120)
        f5c.shift(UP * (f5b.get_center()[1] - f5c.get_center()[1]))
        self.pena(f5c)
        self.col("E3-4", f5a, f5b, f5c, chips=1)

        self.gat("e isso é a tangente ao quadrado de alfa")
        self.degrau("C3.17a", "= (h^3/3)(1/cos^2 alpha - 1)/2 = (h^3/3) tg^2 alpha/2  (1/cos^2 alpha - 1 = tg^2 alpha)")
        g6a = L([("eq", "="), ("c1", r"\dfrac{h^3}{3}\cdot"), ("fr", r"\dfrac{1/\cos^2\al-1}{2}")], C34 + 40, 795, 36)
        self.pena(g6a)
        cg_tg, cf_tg, cm_tg = chip(r"\dfrac1{\cos^2\al}-1=\tg^2\al", 1420, 470, 28)
        g6b = L([("eq", "="), ("c1", r"\dfrac{h^3}{3}\cdot"), ("fr", r"\dfrac{\tg^2\al}{2}")], C34 + 40, 795, 36)
        ao_lado(g6a, g6b, 0, 0, gap=14)
        g6b.shift(UP * (g6a[0][0].get_center()[1] - g6b[0][0].get_center()[1]))
        self.gm(15, g6a, g6b, [("eq", "eq"), ("c1", "c1"), ("fr", "fr")], rt=1.0, copia=True, nota="GM15a: 1/cos^2 alpha - 1 -> tg^2 alpha")
        self.chip_pena(cg_tg, cf_tg, cm_tg)
        self.col("E3-4", g6a, g6b, cg_tg, chips=2)

        self.gat("a tangente de alfa é")
        self.degrau("C3.17", "tg^2 alpha = R^2/h^2 => (h^3/3) * R^2/(2h^2) = hR^2/6")
        g6c = L([("eq", "="), ("c1", r"\dfrac{h^3}{3}\cdot"), ("fr", r"\dfrac{R^2}{2h^2}")], C34 + 40, 795, 36)
        ao_lado(g6b, g6c, 0, 0, gap=14)
        g6c.shift(UP * (g6b[0][0].get_center()[1] - g6c[0][0].get_center()[1]))
        self.gm(15, g6b, g6c, [("eq", "eq"), ("c1", "c1"), ("fr", "fr")], rt=1.0, copia=True, nota="GM15b: tg^2 alpha -> R^2/h^2")
        g6d = TC(r"=\dfrac{hR^2}{6}", C34, 795, 36)
        ao_lado(g6c, g6d, 0, 0, gap=14)
        g6d.shift(UP * (g6c[0][0].get_center()[1] - g6d[0][0].get_center()[1]))
        self.pena(g6d)
        self.col("E3-4", g6c, g6d, chips=2)

        self.gat("o mesmo número")
        self.degrau("C3.18", "V = 2pi * hR^2/6 = pi R^2 h/3 ✓ (o mesmo hR^2/6)")
        f7 = TC(r"V=2\pi\cdot\dfrac{hR^2}{6}=\dfrac{\pi R^2h}{3}\ \Me{\checkmark}", C34 + 10, 920, 46)
        self.pena(f7)
        mol7 = caixa_men(f7)
        lg7 = leg("O MESMO hR²/6", C34 + 580, 928, MEN, "left", 28)
        self.play(Create(mol7), run_time=0.4)
        self.pena(lg7)
        self.col("E3-4", f7, lg7, chips=2)
        self.marca("15_E3-4")

        self.sai_fim(rt=0.35)
