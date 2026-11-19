"""yt_0043 · Lote PH: H1 (a lata que gira, alvo 01) e H2 (uma conta por pedaço, alvo 02)."""
from k43 import *  # noqa: F401,F403

COL = 1020


class PH(B43):
    ANTES = "A LATA PESADA GIRA"

    def corpo(self):
        # ── H1 · a lata que gira (alvo 01) ────────────────────────────────────────────────────────────────
        self.an("H1")
        pal1 = self.palco("lataGiro", cam_alvo("h1"), giro=30.0, seta=0.0)
        rx1 = self.rot3(pal1, "ex", r"\X", size=38, ancora="c")
        ry1 = self.rot3(pal1, "ey", r"\Y", size=38, ancora="c")
        rz1 = self.rot3(pal1, "ez", r"\Z", size=38, ancora="c")
        for _r in (rx1, ry1, rz1):
            pronto(_r)
        self.add(pal1.fundo, rx1, ry1, rz1)

        self.gat("Lembra da lata pesada")
        self.play(*pal1.anim(rt=3.8, giro=0.0))

        self.gat("mais densa conforme se afasta")
        sq1, lg1 = legq("#5FA8C8", "LEVE NA ORIGEM", 120, 1020, 30)
        sq2, lg2 = legq(CI, "PESADA NA QUINA", 540, 1020, 30)
        self.play(FadeIn(sq1), FadeIn(sq2), run_time=0.25)
        self.pena(lg1, lg2)

        self.gat("A densidade é a distância até a origem")
        f1 = mixl([("t", "DENSIDADE", CI), ("m", r"\de=\Ci{\sqrt{\X^2+\Y^2+\Z^2}}=\Ci{\sqrt{\S^2+\Z^2}}")], COL, 180, 44)
        self.pena(f1)
        self.col("H1", f1)

        self.gat("uma caixa em cilíndricas")
        f2 = mixl([("t", "LATA", GEO), ("m", r"0\le\S\le1,\ \ 0\le\T\le2\pi,\ \ 0\le\Z\le1")], COL, 290, 40)
        self.pena(f2)
        self.col("H1", f2)

        self.gat("onde ela equilibra")
        ct1 = cartao(COL, 360, 840, 200)
        t_c1 = T(" 1   ONDE ELA EQUILIBRA?", COL + 30, 420, 36)
        c_n1 = Circle(radius=16 / 120, stroke_color=BR, stroke_width=2.2, fill_opacity=0).move_to(glifos(t_c1)[0].get_center()).set_z_index(12)
        self.dentro(ct1._painel, t_c1)
        self.pena(t_c1, extra=[FadeIn(ct1), Create(c_n1)])
        self.col("H1", ct1)

        self.gat("quanto custa colocar ela para girar")
        rom = self.rot3(pal1, "omega", r"\omega", dx=-30, dy=26, size=34, ancora="l")
        ct2 = cartao(COL, 600, 840, 200)
        t_c2 = T(" 2   QUANTO CUSTA GIRAR?", COL + 30, 660, 36)
        c_n2 = Circle(radius=16 / 120, stroke_color=BR, stroke_width=2.2, fill_opacity=0).move_to(glifos(t_c2)[0].get_center()).set_z_index(12)
        self.dentro(ct2._painel, t_c2)
        self.play(*pal1.anim(rt=0.45, seta=1.0), FadeIn(rom[0]))
        self.pena(rom.f, t_c2, extra=[FadeIn(ct2), Create(c_n2)])
        self.col("H1", ct2)

        self.gat("Se a lata fosse comum")
        c1_l = mixl([("t", "LATA COMUM: NO MEIO,", GEO), ("m", r"\zb=\dfrac12")], COL + 30, 505, 40)
        c2_l = mixl([("t", "LATA COMUM:", GEO), ("m", r"I=\dfrac12\,M R^2")], COL + 30, 745, 40)
        self.dentro(ct1._painel, c1_l)
        self.dentro(ct2._painel, c2_l)
        self.pena(c1_l)
        self.pena(c2_l)

        self.gat("E a lata pesada")
        f_fim = T("E A LATA PESADA?", COL, 900, 46, "left", CI)
        self.pena(f_fim)
        self.col("H1", f_fim, chips=2)
        self.marca("01_H1")
        self._fecha(antes=0.7)
        self.sai(rx1, ry1, rom, sq1, lg1, sq2, lg2, f1, f2, ct1, t_c1, c_n1, c1_l, ct2, t_c2, c_n2, c2_l, f_fim, rt=0.35)
        pal2 = self.palco("lataDuas", cam_alvo("h2"), traco=1.0, cel1=0.0, cel2=0.0)
        rz1.clear_updaters()
        pal2.prende(rz1, "ez", 0, 0, "c")
        self.remove(pal1.fundo)
        self.add(pal2.fundo)
        self.titulo("UMA CONTA POR PEDAÇO", rt=0.3)

        # ── H2 · uma conta por pedaço (alvo 02) ───────────────────────────────────────────────────────────
        self.an("H2")

        self.gat("pega um pedacinho da lata")
        rc1 = self.rot3(pal2, "c1", r"\dm", dx=-4, dy=52, size=34, ancora="l")
        rc2 = self.rot3(pal2, "c2", r"\dm", dx=2, dy=-12, size=34, ancora="l")
        sq3, lg3 = legq("#5FA8C8", "PERTO DA ORIGEM: LEVE", 120, 1020, 30)
        sq4, lg4 = legq(CI, "NA QUINA: PESADO", 540, 1020, 30)
        self.play(*pal2.anim(rt=0.7, cel1=1.0, cel2=1.0), FadeIn(rc1[0]), FadeIn(rc2[0]), FadeIn(sq3), FadeIn(sq4))
        self.pena(rc1.f, rc2.f, lg3, lg4)

        self.gat("A massa de um pedacinho é a densidade vezes o volume")
        h2_1 = TC(r"\dm=\de\,dV", COL, 200, 54)
        self.pena(h2_1)
        self.col("H2", h2_1)

        self.gat("Para o equilíbrio")
        h2_2 = mixl([("t", " 1   ALTURA PESADA:", GEO), ("m", r"\Z\cdot\dm")], COL, 330, 46)
        c_h2_2 = Circle(radius=19 / 120, stroke_color=GEO, stroke_width=2.2, fill_opacity=0).move_to(glifos(h2_2[0])[0].get_center()).set_z_index(12)
        self.pena(h2_2, extra=[Create(c_h2_2)])
        self.col("H2", h2_2)

        self.gat("Para o giro")
        rf2 = self.rot3(pal2, "f2", r"\S", dx=-10, dy=-34, size=34, ancora="c")
        h2_3 = mixl([("t", " 2   CADA PEDAÇO CUSTA", GEO), ("m", r"\S^2\cdot\dm")], COL, 450, 46)
        c_h2_3 = Circle(radius=19 / 120, stroke_color=GEO, stroke_width=2.2, fill_opacity=0).move_to(glifos(h2_3[0])[0].get_center()).set_z_index(12)
        self.play(*pal2.anim(rt=0.65, cel1=2.0), FadeIn(rf2[0]), Create(c_h2_3))
        self.pena(rf2.f, h2_3)
        self.col("H2", h2_3)

        self.gat("E a integral tripla soma")
        h2_4 = mixl([("t", "SOMA DE TUDO:", GEO), ("m", r"\iiint \Z\,\dm,\qquad \iiint \S^2\,\dm")], COL, 590, 46)
        self.pena(h2_4)
        self.col("H2", h2_4)
        self.marca("02_H2")

        self.sai_fim()
