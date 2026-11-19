"""yt_0044 · Lote PH: H1 (a lata na dobradiça, alvo 01) e H2 (a receita em quatro perguntas, alvo 02)."""
from k44 import *  # noqa: F401,F403

COL = 1020


class PH(B44):
    ANTES = None

    def corpo(self):
        # ── H1 · a lata na dobradiça (alvo 01) ────────────────────────────────────────────────────────────────
        self.an("H1")
        pal = self.palco("lataParede", OL, eixo=0.0, parede=0.0, seta=0.0, cota=0.0)
        self.titulo("A LATA NA DOBRADIÇA", ja=True)
        self.entra(pal.fundo, rt=0.6)

        self.gat("uma lata de material uniforme")
        l1 = mixl([("t", "LATA UNIFORME: RAIO", GEO), ("m", "R,"), ("t", "ALTURA", GEO), ("m", r"h,\ \ \de=k")], COL, 190, 42)
        self.pena(l1)
        self.col("H1", l1)

        self.gat("em volta do eixo central")
        rz = self.rot3(pal, "ez", r"\Z", size=38, ancora="c")
        sq1, lq1 = legq(EZ, "EIXO PELO CENTRO", 120, 1020, 30)
        self.play(*pal.anim(0.8, eixo=1.0), FadeIn(sq1), run_time=0.8)
        self.pena(rz, lq1)
        c1 = cartao(COL, 270, 840, 190)
        n1 = num(1, COL + 48, 318, 40, EZ)
        t1 = T("PELO EIXO CENTRAL", COL + 82, 330, 34, "left", EZ)
        f1 = TC(r"I=\dfrac12\,MR^2", COL + 30, 405, 46)
        self.dentro(c1._painel, n1, t1, f1)
        self.pena(n1, t1, f1, extra=[FadeIn(c1)])
        self.col("H1", t1, f1)

        self.gat("como uma porta na dobradiça")
        rre = self.rot3(pal, "d2R", "2R", size=28, ancora="c")
        sq2, lq2 = legq(AL, "EIXO NA PAREDE", 480, 1020, 30)
        self.play(*pal.anim(0.9, parede=1.0, cota=1.0), FadeIn(sq2), run_time=0.9)
        pal.set(seta=1.0)
        self.pena(rre, lq2)
        c2 = cartao(COL, 500, 840, 190)
        n2 = num(2, COL + 48, 548, 40, AL)
        t2 = T("NA PAREDE, COMO UMA PORTA", COL + 82, 560, 34, "left", AL)
        f2 = TC(r"I=\ ?", COL + 30, 635, 46)
        self.dentro(c2._painel, n2, t2, f2)
        self.pena(n2, t2, f2, extra=[FadeIn(c2)])
        self.col("H1", t2, f2)

        self.gat("Mas quanto mais")
        l4 = T("MAIS CARO. QUANTO MAIS?", COL, 790, 46, "left", CI)
        self.pena(l4)
        self.col("H1", l4)
        self.marca("01_H1")
        h1m = [rz, rre, sq1, lq1, sq2, lq2, l1, c1, n1, t1, f1, c2, n2, t2, f2, l4]

        # ── H2 · a receita em quatro perguntas (alvo 02) ──────────────────────────────────────────────────────
        self.an("H2")
        self.titulo("A RECEITA EM QUATRO PERGUNTAS", rt=0.3)
        T4 = [("ONDE ESTÁ", "O CORPO?"), ("QUAL", "SISTEMA?"), ("ENTRA", "E SAI"), ("CONFERIR", "")]
        gats = ["Primeira pergunta", "Segunda", "Terceira", "E a quarta"]
        for i, ((a, b), g) in enumerate(zip(T4, gats)):
            self.gat(g)
            if i == 0:          # a lata do H1 fica até a primeira pergunta (sem papel vazio no começo do H2)
                self.sai(pal.fundo, *h1m, rt=0.3)
            X0 = 96 + i * 444
            cx = X0 + 200
            ct = cartao(X0, 200, 400, 420)
            nn = num(i + 1, X0 + 40, 246, 36)
            ta = T(a, X0 + 70, 256, 32, "left", BR)
            itens = [nn, ta]
            if b:
                itens.append(T(b, X0 + 70, 300, 32, "left", BR))
            des, txts = [], []
            if i == 0:
                v = Vista2D(cx - 40, 520, 95)
                des += [poly_px([v.P(-1.2, -.2), v.P(1, -.2), v.P(1.6, .5), v.P(-.6, .5)], mixh("#16123A", SOMB, .35), 1.0, z=1),
                        v.linha([(-1.2, -.2), (1, -.2), (1.6, .5), (-.6, .5), (-1.2, -.2)], SOMB, 3),
                        v.linha([(-.6, .2), (.9, .2), (1.2, 1.6), (-.3, 1.6), (-.6, .2)], GEO, 3)]
                txts.append(leg("SOMBRA", cx - 150, 600, SOMB, "left", 26))
            elif i == 1:
                for k, (tx, xx) in enumerate(((r"1", X0 + 30), (r"\Js", X0 + 120), (r"\Jr", X0 + 205))):
                    cg, cf, cm_ = chip(tx, xx, 400, 32, LI)
                    des.append(cm_)
                    txts.append(cf)
                txts.append(leg("CART. · CILÍND. · ESFÉR.", X0 + 30, 480, GEO, "left", 26))
                txts.append(leg("O FATOR DO VOLUME", X0 + 30, 560, LI, "left", 26))
            elif i == 2:
                des += [lin_px([(cx, 560), (cx, 380)], "#E8ECF8", 6, z=6), ponto_px(cx, 560, AZC, 11, z=8), ponto_px(cx, 380, CORAL, 11, z=8)]
                txts += [leg("ENTRA", cx + 24, 568, AZC, "left", 26), leg("SAI", cx + 24, 388, CORAL, "left", 26)]
            else:
                des.append(check_px(cx, 430, MEN, 2.2))
                txts += [leg(s, X0 + 30, y, GEO, "left", 26) for s, y in (("SIMETRIA", 520), ("CASO-LIMITE", 560), ("OUTRO CAMINHO", 600))]
            self.dentro(ct._painel, *[m for m in itens + txts if not isinstance(m, Circle)])
            self.pena(*itens, extra=[FadeIn(ct)] + [FadeIn(d) for d in des])
            self.pena(*txts)
            self.col("H2-%d" % i, *itens)

        self.gat("três fórmulas")
        fa = TC(r"M=\iiint\de\,dV", 260, 800, 46, "c")
        fb = TC(r"\xb=\dfrac{\Myz}{M}", 830, 800, 46, "c")
        fc = mixl([("m", r"I=\iiint("), ("g", -10), ("t", "DIST. AO EIXO", BR), ("g", -10), ("m", r")^2\,\de\,dV")], 0, 800, 40)
        fc.shift(RIGHT * ((1450 - 960) / 120 - fc.get_center()[0]))
        self.pena(fa)
        self.pena(fb)
        self.pena(fc)
        self.col("H2", fa, fb, fc)
        self.marca("02_H2")

        self.sai_fim(rt=0.35)
