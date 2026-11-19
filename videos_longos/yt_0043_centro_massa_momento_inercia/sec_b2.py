"""yt_0043 · Lote PB2: B2-1 (a taça: montar) e B2-2 (a taça: a conta — calibração de escrita, GM4, GM5 e 3D)."""
from k43 import *  # noqa: F401,F403

COL = 1020


class PB2(B43):
    ANTES = "SIMETRIA: OS DOIS PRECISAM GIRAR"

    def corpo(self):
        # ── B2-1 · a taça: montar (alvo 08) ───────────────────────────────────────────────────────────────
        self.an("B2-1")
        pal = self.palco("taca", cam_alvo("b21"), sonda=0.0, cm=0.0, meio=0.0)
        rz = self.rot3(pal, "ez", r"\Z", size=38, ancora="c")
        self.add(pal.fundo)
        self.titulo("A TAÇA")

        self.gat("uma taça")
        self.pena(rz.f, extra=[FadeIn(rz[0])])

        self.gat("x ao quadrado mais y ao quadrado vira s ao quadrado")
        f1 = mixl([("t", "TAÇA", GEO), ("m", r"\X^2+\Y^2\le\Z\le1,\quad\de=k")], COL, 180, 44)
        f2 = mixl([("t", "EM CILÍNDRICAS", GEO), ("m", r"\S^2\le\Z\le1")], COL, 280, 44)
        self.pena(f1)
        self.col("B2-1", f1)
        self.pena(f2)
        self.col("B2-1", f2)

        self.gat("ela entra pelo fundo curvo")
        sq1, lg1 = legq(AZC, "ENTRA EM z = s²", 120, 1020, 30)
        sq2, lg2 = legq(CORAL, "SAI EM z = 1", 480, 1020, 30)
        self.play(*pal.anim(rt=1.3, sonda=1.0), FadeIn(sq1), FadeIn(sq2))
        self.pena(lg1, lg2)

        self.gat("A sombra no chão")
        f3 = mixl([("t", "SOMBRA", GEO), ("m", r"0\le\S\le1,\ \ 0\le\T\le2\pi")], COL, 380, 42)
        self.pena(f3)
        self.col("B2-1", f3)

        self.gat("a simetria já matou")
        cg, cf, cm_ = chipm([("t", "SIMETRIA", GEO), ("m", r"\Rightarrow\ \xb=\yb=0")], COL, 470, 30)
        self.chip_pena(cg, cf, cm_)
        self.col("B2-1", cg, chips=1)

        self.gat("Sobra o z barra")
        f4 = TC(r"\zb=\dfrac{\Mxy}{M}=\dfrac{k\iiint\Z\,dV}{k\iiint dV}", COL, 620, 50)
        self.pena(f4)
        self.col("B2-1", f4, chips=1)

        self.gat("o k sai das duas")
        l1 = leg("O k CANCELA: z̄ SÓ DEPENDE DA FORMA", COL, 750, GEO, "left", 30)
        self.pena(l1)
        self.col("B2-1", l1, chips=1)

        self.gat("o meio da altura")
        sm, st = selo("CHUTE: z̄ = 1/2 ?", COL, 850, SOMB, 32)
        self.pena(st, extra=[Create(sm)])
        self.col("B2-1", st, chips=2)
        self.marca("08_B2-1")
        self._fecha(antes=0.75)
        self.sobe_sai(f1, f2, f3, cg, f4, l1, sm, st, sq1, lg1, sq2, lg2, rt=0.35)
        self.titulo("A TAÇA: A CONTA", rt=0.35)

        # ── B2-2 · a taça: a conta (alvo 09 — calibração obrigatória) ─────────────────────────────────────
        self.an("B2-2")

        self.gat("Primeiro o volume")
        self.degrau("C3.1", "V = int_0^2pi int_0^1 int_{s^2}^1 s dz ds dtheta")
        v1 = TC(r"V=\int_0^{2\pi}\!\!\int_0^1\!\!\int_{\S^2}^1\Js\,\dZ\,\dS\,\dT", COL, 270, 42)
        self.pena(v1)
        self.col("B2-2a", v1)

        self.gat("A de dentro, em z")
        self.degrau("C3.2", "int_{s^2}^1 s dz = [s z]_{s^2}^1 = s * 1 - s * s^2 = s - s^3")
        v2a = L([("pre", r"\int_{\S^2}^1\Js\,\dZ="), ("col", r"\Big[\Js\,\Z\Big]_{\S^2}^1")], COL, 400, 40)
        v2b = L([("pre", r"\int_{\S^2}^1\Js\,\dZ=\Big[\Js\,\Z\Big]_{\S^2}^1="), ("meio", r"\Js\cdot1-\Js\cdot\S^2="), ("res", r"\S-\S^3")], COL, 400, 40)
        self.pena(v2a)
        self.gm(4, v2a, v2b, [("pre", "pre"), ("col", "res")], rt=0.9, nota="GM4: [sz]_{s^2}^1 -> s - s^3")
        self.col("B2-2a", v2b)

        self.gat("Agora em s")
        self.degrau("C3.3", "int_0^1 (s - s^3) ds = [s^2/2 - s^4/4]_0^1 = 1/2 - 1/4 = 1/4")
        v3 = TC(r"\int_0^1(\S-\S^3)\,\dS=\Big[\dfrac{\S^2}{2}-\dfrac{\S^4}{4}\Big]_0^1", COL, 510, 40)
        self.pena(v3)
        self.col("B2-2a", v3)
        self.degrau("C3.3b", "= (1/2 - 1/4) - (0 - 0) = 1/4   (G(b) - G(a))")
        v3b = TC(r"=\Big(\dfrac12-\dfrac14\Big)-(0-0)=\dfrac14", COL + 40, 625, 40)
        self.pena(v3b)
        self.col("B2-2a", v3b)

        self.gat("a volta inteira em téta")
        self.degrau("C3.4", "V = 2pi * 1/4 = pi/2")
        v4 = TC(r"V=2\pi\cdot\dfrac14=\dfrac{\pi}{2}", COL, 750, 44)
        self.pena(v4)
        self.col("B2-2a", v4)

        self.gat("Agora o momento")
        cg_v, cf_v, cm_v = chip(r"V=\dfrac{\pi}{2}", COL, 150, 30)
        self.sobe_sai(v1, v2b, v3, v3b, v4, rt=0.45)
        self.chip_pena(cg_v, cf_v, cm_v)
        self.degrau("C4.1", "iiint z dV = int_0^2pi int_0^1 int_{s^2}^1 z s dz ds dtheta")
        m1 = TC(r"\iiint\Z\,dV=\int_0^{2\pi}\!\!\int_0^1\!\!\int_{\S^2}^1\Z\,\Js\,\dZ\,\dS\,\dT", COL, 270, 42)
        self.pena(m1)
        self.col("B2-2b", cg_v, m1, chips=1)

        self.gat("o s fica parado")
        self.degrau("C4.2", "int_{s^2}^1 z s dz = s[z^2/2]_{s^2}^1 = s(1/2 - s^4/2) = s/2 - s^5/2")
        m2 = TC(r"\int_{\S^2}^1\Z\,\Js\,\dZ=\Js\Big[\dfrac{\Z^2}{2}\Big]_{\S^2}^1=\Js\Big(\dfrac12-\dfrac{\S^4}{2}\Big)=\dfrac{\S}{2}-\dfrac{\S^5}{2}", COL, 400, 40)
        self.pena(m2)
        self.col("B2-2b", m2, chips=1)

        self.gat("potência de novo")
        self.degrau("C4.3", "int_0^1 (s/2 - s^5/2) ds = [s^2/4 - s^6/12]_0^1 = 1/4 - 1/12 = 1/6")
        m3 = TC(r"\int_0^1\Big(\dfrac{\S}{2}-\dfrac{\S^5}{2}\Big)\dS=\Big[\dfrac{\S^2}{4}-\dfrac{\S^6}{12}\Big]_0^1", COL, 510, 40)
        self.pena(m3)
        self.col("B2-2b", m3, chips=1)
        self.degrau("C4.3b", "= (1/4 - 1/12) - (0 - 0) = 1/6   (G(b) - G(a))")
        m3b = TC(r"=\Big(\dfrac14-\dfrac1{12}\Big)-(0-0)=\dfrac16", COL + 40, 625, 40)
        self.pena(m3b)
        self.col("B2-2b", m3b, chips=1)

        self.gat("multiplica por dois pi")
        self.degrau("C4.4", "iiint z dV = 2pi * 1/6 = pi/3")
        m4 = TC(r"\iiint\Z\,dV=2\pi\cdot\dfrac16=\dfrac{\pi}{3}", COL, 750, 44)
        self.pena(m4)
        self.col("B2-2b", m4, chips=1)

        self.wait(2.2)
        self.degrau("C4.5", "zbar = (pi/3)/(pi/2) = 2/3")
        m5a = L([("pre", r"\zb="), ("frac", r"\dfrac{\pi/3}{\pi/2}")], COL + 10, 880, 54)
        m5b = L([("pre", r"\zb="), ("meio", r"\dfrac{\pi/3}{\pi/2}="), ("res", r"\dfrac23")], COL + 10, 880, 54)
        self.pena(m5a)

        self.gat("dois terços")
        mol_z = caixa_men(m5b)
        q23 = pal.pt("z23")
        cmm = cm_mark(q23[0], q23[1])
        r23 = TP(r"\dfrac23", q23[0] - 60, q23[1] - 6, 30, "r")
        r23._p3d = ("taca", "z23", 0, 0)
        self._rots3.append(r23)
        self.gm(5, m5a, m5b, [("pre", "pre"), ("frac", "res")], rt=0.55,
                extra=[*pal.anim(rt=0.55, cm=1.0), Create(mol_z), FadeIn(cmm), FadeIn(r23[0])],
                nota="GM5: (pi/3)/(pi/2) -> 2/3")
        self.pena(r23.f, rt=0.25)
        self.col("B2-2b", m5b, chips=1)

        self.gat("acima do meio")
        q12 = pal.pt("z12")
        th12 = traco_h(q12[0] - 150, q12[0] + 150, q12[1])
        r12 = TP(r"\dfrac12", q12[0] - 150 - 18, q12[1] - 8, 30, "r")      # R11: na ponta esquerda do tracejado, fora da taça e longe da sonda
        r12._p3d = ("taca", "z12", 0, 0)
        self._rots3.append(r12)
        lg_f = leg("ACIMA DO MEIO: A TAÇA É LARGA EM CIMA", COL, 990, GEO, "left", 30)
        self.play(*pal.anim(rt=0.4, meio=1.0), Create(th12), FadeIn(r12[0]))
        self.pena(r12.f, lg_f)
        self.col("B2-2b", lg_f, chips=2)
        self.marca("09_B2-2")

        self.sai_fim()
