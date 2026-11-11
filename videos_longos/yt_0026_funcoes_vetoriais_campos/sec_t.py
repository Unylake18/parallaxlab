"""Lote PT · abertura do Cálculo III (handoff v7): quadros-alvo 01–08. Só setas, curvas, fórmulas e formas sólidas; nada em volta se mexe sem explicar.
T0 uma seta → o campo (−y, x) · T1 colunas (3D) · T2 trabalho · T3 fluxo (3D) · T4a/T4b Green: as setas de circulação das células, o par que se cancela, sobra a borda ·
T4c a mesma ideia, três vezes (Green, Stokes, Gauss só como fórmula) · T5 cartão. Rótulo único centralizado (sem canto)."""
from v7 import *  # noqa: F401,F403

GIRO = lambda x, y: (-y, x)
F_GIRO = r"\F(\X,\Y) = -\Y\,\ii + \X\,\jj"


class LoteT(Base):
    CANTO = False

    def corte(self, velhos, novos, rt=0.25):
        anims = [m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in velhos]
        anims += [m.op.animate.set_value(1.0) if isinstance(m, Fundo3D) else FadeIn(m) for m in novos]
        self.play(*anims, run_time=rt)
        for m in velhos:
            m.clear_updaters()
        self.remove(*velhos)

    def corpo(self):
        set_dy(0)
        seg = {}

        # ── T0 · uma seta, num ponto só; depois uma seta em cada ponto (quadro 01) ──
        self.an("T0")
        rot0 = rot_abertura("UMA SETA EM CADA PONTO")
        v0 = Vista(620, 600, 115)
        g0 = campo7(v0, GIRO, -3, 3, -3, 3, passo=0.5, rmin=0.4, rmax=3.2, mmax=3.2, nome="T0 (−y, x)")
        ordem = sorted(g0, key=lambda s: math.hypot(*s._xy))
        uno = ordem[0]
        f0 = TC(F_GIRO, 1120, 520, 58)
        l0 = legenda("CAMPO VETORIAL", 1124, 620, CAMPO2)
        self.grade(v0)                                  # papel v2: grade do plano do campo
        self.play(FadeIn(rot0), GrowArrow(uno), run_time=0.7)
        self.play(pulso(uno, 1.3, 1.5), run_time=0.8)
        self.gat("junta infinitas delas")
        c0 = caneta(f0, ritmo=0.7)
        self.play(LaggedStart(*[GrowArrow(s) for s in ordem[1:]], lag_ratio=0.012, run_time=2.6), c0,
                  Succession(Wait(max(0.1, c0.tot - 0.6)), FadeIn(l0, run_time=0.5)), run_time=max(c0.tot, 2.6))
        self._fecha()

        # ── T1 · colunas finíssimas viram volume (quadro 02) ──
        self.an("T1")
        seg["c"] = self.t
        BOX1 = [180, 230, 880, 760]

        def est_col(t):
            nivel = 0
            for k, n in (("l1", 1), ("l2", 2)):
                if k in seg and t >= seg[k]:
                    nivel = n
            return {"nivel": nivel, "box": BOX1}
        col = Fundo3D(self, "c7_colunas", est_col, op=0.0)
        self.add(col)
        rot1 = rot_abertura("VOLUME")
        f1 = TC(r"V = \iint_{\G R} \S{f}(\X,\Y)\,dA", 1120, 520, 58)
        l1 = legenda("SOMA DE COLUNAS FININHAS", 1124, 630)
        self.grade()                                    # 3D: violeta liso
        self.corte([g0, rot0, f0, l0], [col, rot1], rt=0.4)
        self.gat("empilha colunas finíssimas")
        seg["l1"] = self.t
        c1 = self.caneta_ate(f1, "e elas viram um volume", ritmo=0.6)
        self.play(c1, Succession(Wait(max(0.1, c1.tot - 0.5)), FadeIn(l1, run_time=0.5)), run_time=c1.tot)
        self.gat("e elas viram um volume")
        seg["l2"] = self.t
        self.wait(max(0.1, self.resta() - 0.2))
        self._fecha()

        # ── T2 · trabalho: o campo ao longo de cada pedacinho do caminho (quadro 03) ──
        self.an("T2")
        v2 = Vista(620, 600, 110)
        Fv = lambda X, Y: (0.8 + 0.35 * math.sin(0.9 * Y), 0.35 * math.cos(0.8 * X))
        g2 = campo7(v2, Fv, -3.5, 3.5, -3, 3, passo=0.7, rmin=0, mmax=1.2, lmax=0.5, alpha=0.85, nome="T2")
        cur = lambda t: (-3.2 + 6.4 * t, 1.1 * math.sin(PI * 1.2 * t) - 0.4)
        curva = linha7([v2.c2p(*cur(i / 120)) for i in range(121)], POS7, 6)
        contorno(curva)
        paradas, setas2, pts2 = [0.15, 0.32, 0.5, 0.68, 0.85], VGroup(), VGroup()
        for t in paradas:
            a, b = cur(t), cur(t + 0.005)
            d = (b[0] - a[0], b[1] - a[1])
            L = math.hypot(*d)
            u = (d[0] / L, d[1] / L)
            f = Fv(*a)
            ft = f[0] * u[0] + f[1] * u[1]
            setas2.add(seta7(v2.c2p(*a), v2.c2p(a[0] + u[0] * ft * 0.9, a[1] + u[1] * ft * 0.9), WHITE_, 6, 22).set_z_index(7))
            pts2.add(ponto7(v2.c2p(*a), POS7, 8))
        rot2 = rot_abertura("TRABALHO")
        f2 = TC(r"W = \int_{\P{C}} \F\cdot d\vec r", 1120, 520, 58)
        l2 = legenda("O CAMPO AO LONGO DE CADA PEDACINHO", 1124, 630)
        self.grade(v2)
        self.corte([col, rot1, f1, l1], [rot2, g2], rt=0.3)
        self.play(Create(curva), run_time=0.9)
        self.gat("em cada pedacinho")
        c2 = caneta(f2)
        passos = []
        for k in range(5):
            passos += [FadeIn(pts2[k], scale=0.5, run_time=0.25), GrowArrow(setas2[k], run_time=0.35)]
        self.play(c2, Succession(*passos), Succession(Wait(max(0.1, c2.tot - 0.5)), FadeIn(l2, run_time=0.5)), run_time=max(c2.tot, 3.0))
        self._fecha()

        # ── T3 · fluxo: o que atravessa cada pedacinho da superfície (quadro 04) ──
        self.an("T3")
        seg["f"] = self.t
        BOX3 = [200, 250, 840, 700]
        fl = Fundo3D(self, "c7_fluxo", lambda t: {"box": BOX3, "sobe": 0.25 * (1 - math.cos(2 * PI * (t - seg["f"]) / 3.0))}, op=0.0)
        self.add(fl)
        rot3 = rot_abertura("FLUXO")
        f3 = TC(r"\Phi = \iint_{\S{S}} \F\cdot\vec n\,dS", 1120, 520, 58)
        l3 = legenda("O QUE ATRAVESSA CADA PEDACINHO", 1124, 630)
        self.grade()                                    # 3D: violeta liso
        self.corte([g2, curva, setas2, pts2, rot2, f2, l2], [fl, rot3], rt=1 / FPS)
        c3 = caneta(f3)
        self.play(c3, Succession(Wait(max(0.1, c3.tot - 0.5)), FadeIn(l3, run_time=0.5)), run_time=c3.tot)
        self.wait(max(0.1, self.resta() - 0.2))
        self._fecha()

        # ── T4 · as trocas entre vizinhos se cancelam: Green (quadros 05 e 06) ──
        self.an("T4")
        v4 = Vista(620, 600, 130)
        n, s, x0, y0, q, h = 3, 1.6, -2.4, -2.4, 0.42, 0.8 - 0.17
        chapa = chapa7([v4.c2p(x0, y0), v4.c2p(x0 + n * s, y0), v4.c2p(x0 + n * s, y0 + n * s), v4.c2p(x0, y0 + n * s)])
        grade = VGroup()
        for k in range(n + 1):
            ext = k in (0, n)
            for a, b in (((x0 + k * s, y0), (x0 + k * s, y0 + n * s)), ((x0, y0 + k * s), (x0 + n * s, y0 + k * s))):
                grade.add(linha7([v4.c2p(*a), v4.c2p(*b)], GEO, 3 if ext else 2, 0.9 if ext else 0.45))
        celulas, internas, externas = [], VGroup(), VGroup()
        for i in range(n):
            for j in range(n):
                cx, cy = x0 + (i + 0.5) * s, y0 + (j + 0.5) * s
                cel = VGroup()
                for A, B, interna in (((cx - q, cy - h), (cx + q, cy - h), j > 0), ((cx + h, cy - q), (cx + h, cy + q), i < n - 1),
                                      ((cx + q, cy + h), (cx - q, cy + h), j < n - 1), ((cx - h, cy + q), (cx - h, cy - q), i > 0)):
                    a_ = seta7(v4.c2p(*A), v4.c2p(*B), CAMPO if interna else CAMPO2, 5, 20).set_z_index(5)
                    cel.add(a_)
                    (internas if interna else externas).add(a_)
                celulas.append(cel)
        rot4a = rot_abertura("PEDACINHO POR PEDACINHO")
        e = v4.c2p(x0 + s, y0 + 1.5 * s)
        coral = RoundedRectangle(width=68 / 120, height=148 / 120, corner_radius=12 / 120).move_to(e).set_fill(opacity=0).set_stroke(DEST, 3.5 / 1.2, 1).set_z_index(9)
        coral._sem_contorno = True
        la1, la2, la3 = (legenda("CADA PEDACINHO GIRA UM POUCO", 1120, 480, WHITE_, "left", 34), legenda("NA PAREDE ENTRE DOIS VIZINHOS,", 1120, 560, SAI_F),
                         legenda("AS DUAS SETAS SE CANCELAM", 1120, 600, DEST))
        self.grade((v4, None, 0.2))                     # passo 0,2 (26 px): as paredes das células (múltiplos de 0,8) caem em linhas da grade
        self.corte([fl, rot3, f3, l3], [rot4a, chapa, grade], rt=1 / FPS)
        self.play(LaggedStart(*[AnimationGroup(*[GrowArrow(a_) for a_ in cel]) for cel in celulas], lag_ratio=0.18, run_time=2.2), FadeIn(la1, run_time=0.5))
        self.gat("as trocas entre vizinhos se cancelam")
        self.play(Create(coral), FadeIn(la2), FadeIn(la3), run_time=0.8)
        self.gat("só sobra o que passa pela borda")
        rot4b = rot_abertura("SÓ SOBRA A BORDA")
        bordaL = linha7([v4.c2p(*p) for p in ((x0, y0), (x0 + n * s, y0), (x0 + n * s, y0 + n * s), (x0, y0 + n * s), (x0, y0))], CAMPO2, 5, 0.5)
        f4 = TC(r"\oint_{\G C} \F\cdot d\vec r \;=\; \iint_{\G R} (\rot \F)\,dA", 1120, 500, 52)
        lb1, lb2, lb3 = legenda("NA BORDA", 1150, 610, SAI_F), legenda("SOMA DOS GIROS DE DENTRO", 1430, 610, CAMPO2), T("TEOREMA DE GREEN", 1124, 720, 34)
        c4 = self.caneta_ate(f4, "no plano", ritmo=0.22, folga=0.5)
        self.play(FadeOut(internas), FadeOut(coral), FadeOut(la1), FadeOut(la2), FadeOut(la3), FadeOut(rot4a), FadeIn(rot4b), FadeIn(bordaL), c4,
                  Succession(Wait(max(0.1, c4.tot - 0.7)), FadeIn(lb1), FadeIn(lb2), FadeIn(lb3, run_time=0.5)), run_time=max(c4.tot, 1.0))
        self.remove(internas)

        # ── T4c · a mesma ideia, três vezes (quadro 07): só fórmulas ──
        rot4c = rot_abertura("A MESMA IDEIA, TRÊS VEZES")
        ch1, ch2 = legenda("NA BORDA", 800, 270, SAI_F, "center"), legenda("EM CADA PEDACINHO DE DENTRO", 1330, 270, CAMPO2, "center")
        self.wait(max(0.1, self.falta("no plano") - 0.45))       # v9: a troca (0,4 s) termina no gatilho de "no plano"
        self.grade(None)                                # só fórmulas: papel()
        self.play(*[FadeOut(m) for m in (rot4b, chapa, grade, externas, bordaL, f4, lb1, lb2, lb3)], FadeIn(rot4c), FadeIn(ch1), FadeIn(ch2), run_time=0.4)
        self.remove(rot4b, chapa, grade, externas, bordaL, f4, lb1, lb2, lb3)
        linhas = [("GREEN", r"\oint_{\G C} \F\cdot d\vec r", r"\iint_{\G R} (\nabla\times\F)\cdot\vec k\,dA"),
                  ("STOKES", r"\oint_{\G C} \F\cdot d\vec r", r"\iint_{\S{S}} (\nabla\times\F)\cdot\vec n\,dS"),
                  ("GAUSS", r"\oiint_{\S{S}} \F\cdot\vec n\,dS", r"\iiint_{\G V} \nabla\cdot\F\,dV")]
        for k, (nome, a, b) in enumerate(linhas):
            Y = 370 + k * 150
            self.gat(["no plano", "numa superfície", "num volume"][k])
            rn = T(nome, 220, Y + 12, 36)
            ta, ig, tb = TC(a, 960, Y, 52, "r", caneta=False), TC("=", 990, Y, 52, "c", caneta=False), TC(b, 1030, Y, 52, "l", caneta=False)
            self.play(FadeIn(rn), FadeIn(ta, shift=0.1 * UP), FadeIn(ig), FadeIn(tb, shift=0.1 * UP), run_time=0.6)
        self.gat("o local e o global")
        g1, g2_ = T("O LOCAL E O GLOBAL", 960, 890, 66, "center"), T("ESTÃO CONECTADOS.", 960, 970, 66, "center", SAI_F)
        self.play(FadeIn(g1, shift=0.1 * UP), FadeIn(g2_, shift=0.1 * UP), run_time=0.7)
        self.wait(max(0.1, self.resta() - 0.1))
        self._fecha()

        # ── T5 · o cartão (quadro 08) ──
        self.an("T5")
        self.papel(True)
        v5 = Vista(960, 540, 110)
        g5 = campo7(v5, GIRO, -8, 8, -4.6, 4.6, passo=0.8, rmin=0.5, mmax=8, lmax=0.5, alpha=0.16, nome="T5 contexto")
        painel5 = RoundedRectangle(width=1000 / 120, height=320 / 120, corner_radius=18 / 120).move_to(PX(960, 530)).set_fill(ESC, 0.86).set_stroke(SAI_F, 2 / 1.2, 0.5).set_z_index(20)
        painel5._sem_contorno = True
        card = T("CÁLCULO III", 960, 520, 110, "center").set_z_index(21)
        acento = seta7(v5.c2p(-0.6, -0.55), v5.c2p(0.6, -0.55), CAMPO, 6, 24).set_z_index(21)
        l5 = legenda("DO INFINITAMENTE PEQUENO AO ESPAÇO INTEIRO.", 960, 648, SAI_F, "center", 34).set_z_index(21)
        sai = [m for m in self.snap()]
        self.gat("isso é cálculo três")
        self.play(*[FadeOut(m) for m in sai], FadeIn(g5), FadeIn(painel5), FadeIn(card, scale=0.97), run_time=0.7)       # v9: o cartão entra junto da troca
        self.remove(*sai)
        self.play(GrowArrow(acento), run_time=0.5)
        self.gat("do infinitamente pequeno")
        self.play(FadeIn(l5, shift=0.1 * UP), run_time=0.6)
        self.gat("aquela seta")
        self.play(pulso(acento, 1.25, 1.6), run_time=1.0)
        self.sai_fim()
