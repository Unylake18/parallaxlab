"""Lote P7 (v2): T7 — sistemas de partículas, derivado passo a passo.
PALCO 3D (threejs/cena3d/esf.js): esferas de aço ligadas por molas, vibrando e derivando devagar (o conjunto tem momento constante);
dois corpos com uma mola (T7-2/3, cancelamento por TransformByGlyphMap) → partícula i → soma → matriz de pares sincronizada com as molas
→ dP/dt = F^ext → disco com binário (vista de cima) → componentes (parábola 2D) + nota do campo."""
from MF_Tools import TransformByGlyphMap

from kit import *  # noqa: F401,F403

R = 0.45
RD, HD = 1.35, 0.62                  # v7: disco 3D (raio, espessura) — os mesmos do esf.js
CAM_B = {"modo": "frente", "K": 0.5, "xc": 0.0, "yc": -2.82, "camx": 0.0, "fov": 16, "el": 5}   # v7: bola da parábola (T7-9)
XB, ZT = 1.15, 2.05                 # esferas de baixo em ±XB; a de cima em z = ZT
VD = 0.12                           # deriva do conjunto (unidades/s): momento total constante
W = 2 * PI / 2.8                    # vibração


def mola2d(a, b, cor=GEO, w=3, n=8, amp=0.12):
    a, b = np.asarray(a), np.asarray(b)
    d = b - a
    L = np.linalg.norm(d)
    u, nrm = d / L, np.array([-d[1], d[0], 0]) / L
    pts = [a + u * L * k / (2 * n + 1) + nrm * amp * (0 if k in (0, 2 * n + 1) else (1 if k % 2 else -1)) for k in range(2 * n + 2)]
    return VMobject().set_points_as_corners(pts).set_stroke(cor, w)


class LoteT7(Base):
    def construct(self):
        self.setup_base(cap="SISTEMAS DE PARTÍCULAS")
        self.q = txt("?", 64, bold=True, color=MAG).scale(0.8).move_to(P3(7.0, 2.45))
        self.add(self.q)
        self.montar_3d()
        self.t7_1()
        self.t7_2_3()
        self.t7_4_5()
        self.t7_6_7()
        self.t7_8()
        self.t7_9()
        self.fim()
        self.relatorio()

    # ── PALCO 3D: estado das esferas por quadro ────────────────────────────────────────────────────────────
    def montar_3d(self):
        self.vis = [ValueTracker(1.0) for _ in range(3)]          # visibilidade de cada esfera
        self.mvis = [ValueTracker(1.0) for _ in range(3)]         # molas (0-1, 0-2, 1-2)
        self.mbr = [ValueTracker(0.0) for _ in range(3)]          # brilho de cada mola
        self.ebr = [ValueTracker(0.0) for _ in range(3)]          # brilho de cada esfera
        self.amp = ValueTracker(1.0)                              # amplitude da vibração (modo triângulo)
        self.dois = ValueTracker(0.0)                             # 1 = só as duas de baixo, mola esticando mais
        self.pisca = ValueTracker(0.0)                            # pulso geral das molas (internas)
        self.K, self.xt, self.yc = 1.5, -3.3, -2.85
        self.disco = None
        self.bola3 = None                                         # v7: bola 3D da parábola (T7-9)
        self.td0 = 0.0

    def pos(self, t):
        a = math.sin(W * t) * self.amp.get_value()
        d = self.dois.get_value()
        ab = 0.07 + 0.11 * d
        cx = VD * t
        return [(cx - XB - ab * a, R), (cx + XB + ab * a, R), (cx, ZT - 0.1 * a)], cx

    def estado(self, t):
        ps, cx = self.pos(t)
        pis = 0.5 + 0.5 * math.sin(2 * PI * t / 1.4)
        if self.disco is not None:                 # v7: disco 3D, câmera 3/4 baixa orbitando ~15° enquanto a CONTA monta
            return {"luz": "lab", "esf": [], "molas": [], "disco": self.disco(t), "piso": 1, "cam": self.cam_d(t)}
        if self.bola3 is not None:
            return {"luz": "lab", "esf": [], "molas": [], "piso": 1, "bola": self.bola3(t), "cam": CAM_B}
        return {"esf": [[x, z, int(self.vis[i].get_value() > 0.5), self.ebr[i].get_value()] for i, (x, z) in enumerate(ps)],
                "molas": [[i, j, int(self.mvis[k].get_value() > 0.5), max(self.mbr[k].get_value(), self.pisca.get_value() * pis)]
                          for k, (i, j) in enumerate(((0, 1), (0, 2), (1, 2)))],
                "piso": 1, "cam": cam_frente(K=self.K, xc=self.xt, yc=self.yc, camx=cx, fov=16, el=4)}

    def cam_d(self, t):
        u = min(1.0, max(0.0, (t - self.td0) / 20.0))
        return {"modo": "obl", "az": -76 + 15 * u * u * (3 - 2 * u), "el": 21, "alvo": [0, 0, HD / 2], "K": 1.2, "fov": 18,
                "xc": -3.3, "yc": -0.55}

    def m(self, x, z):
        return mapa_frente(self.f3d.e["cam"], x, z)

    def P(self, i):
        """Centro da esfera i no Manim (quadro corrente)."""
        x, z, *_ = self.f3d.e["esf"][i]
        return self.m(x, z)

    def front(self, so_baixo=False, rot="SISTEMA"):
        def f():
            ps = [self.P(i) for i in ((0, 1) if so_baixo else (0, 1, 2))]
            xs, ys = [p[0] for p in ps], [p[1] for p in ps]
            r = self.K * R
            x0, x1 = min(xs) - r - 0.45, max(xs) + r + 0.45
            y0, y1 = (min(ys) - r - 0.75, max(ys) + r + 0.98) if so_baixo else (min(ys) - r - 0.3, max(ys) + r + 0.4)   # v5 (V2)
            rr = RoundedRectangle(corner_radius=0.3, width=x1 - x0, height=y1 - y0).move_to(P3((x0 + x1) / 2, (y0 + y1) / 2))
            rr.set_stroke(WHITE_, 2.2, opacity=0.62)
            d = DashedVMobject(rr, num_dashes=int((x1 - x0 + y1 - y0) * 5), dashed_ratio=0.55).set_z_index(1)
            lab = mtxt(rot, 18, op=0.8).next_to(rr.get_corner(UL), UP, buff=0.1).align_to(rr, LEFT).shift(0.25 * RIGHT)
            return VGroup(d, lab)
        return always_redraw(f)

    # ── T7-1 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def t7_1(self):
        self.an("T7-1")
        self.f3d = Fundo3D(self, "esferas", self.estado, op=0.0)
        self.f3d.conta.set_value(1.0)             # v4: o chão 3D não passa atrás da CONTA
        self.add(self.f3d)
        self.play(self.f3d.op.animate.set_value(1.0), run_time=1.0)
        fr = self.front()
        self.diz("como essa caixa tracejada")
        self.play(FadeIn(fr), run_time=0.8)
        ex = ValueTracker(0.0)

        def externas():
            g = VGroup()
            o = ex.get_value()
            if o < 0.01:
                return g
            for i in range(3):
                c = self.P(i)
                a = arrow(c + P3(0, -0.15), c + P3(0, -1.05), color=FC, width=6, tip=0.17, z=12)
                g.add(a)
            for i in (0, 1):
                c = self.P(i)
                g.add(arrow(c + P3(0.42, -self.K * R), c + P3(0.42, -self.K * R + 0.95), color=FC, width=6, tip=0.17, z=12))
            return g.set_opacity(o)
        ext = always_redraw(externas)
        self.add(ext)
        li = txt("INTERNAS", 24, color=FC, bold=True)
        di = txt("FORÇAS ENTRE OS CORPOS DE DENTRO", 20, color=DIM)
        le = txt("EXTERNAS", 24, color=FC, bold=True)
        de = txt("VÊM DE FORA DA FRONTEIRA", 20, color=DIM)
        b1 = VGroup(li, di).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        b2 = VGroup(le, de).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        na_conta(b1, 0.9)
        na_conta(b2, -0.6)
        ic = mola2d(P3(XC0 + 0.0, 1.55), P3(XC0 + 0.9, 1.55), cor=FC, w=3).shift(UP * 0.0)
        b1.shift(RIGHT * 1.15); b1[0].shift(UP * 0.0)
        ic.move_to(P3(XC0 + 0.45, b1[0].get_y()))
        ie = arrow(P3(XC0 + 0.45, b2[0].get_y() + 0.35), P3(XC0 + 0.45, b2[0].get_y() - 0.35), color=FC, width=6, tip=0.15)
        b2.shift(RIGHT * 1.15)
        self.diz("As forças que os corpos de dentro")
        self.play(self.pisca.animate.set_value(1.0), FadeIn(b1, shift=0.1 * UP), FadeIn(ic), run_time=0.9)
        self.diz("As que vêm de fora")
        self.play(ex.animate.set_value(1.0), FadeIn(b2, shift=0.1 * UP), FadeIn(ie), run_time=0.9)
        ch = txt("A ESCOLHA DA FRONTEIRA É NOSSA", 22, bold=True).move_to(P3(0, Y_LEG + 0.05))
        self.diz("Quem escolhe a fronteira")
        self.play(FadeIn(ch, shift=0.1 * UP), run_time=0.6)
        self.ate(0.97)
        self.fr1, self.ext1 = fr, ext
        self.leg1 = VGroup(b1, b2, ic, ie, ch)

    # ── T7-2, T7-3: dois corpos com uma mola ───────────────────────────────────────────────────────────────
    def t7_2_3(self):
        self.an("T7-2")
        self.fr1.clear_updaters(); self.ext1.clear_updaters()
        self.play(FadeOut(self.leg1), FadeOut(self.fr1), FadeOut(self.ext1), self.pisca.animate.set_value(0.0), run_time=0.6)
        self.remove(self.fr1, self.ext1)
        self.vis[2].set_value(0.0); self.mvis[1].set_value(0.0); self.mvis[2].set_value(0.0)
        self.play(self.dois.animate.set_value(1.0), run_time=0.8)
        fr = self.front(so_baixo=True, rot="SISTEMA: 1 + 2")

        fbr = ValueTracker(0.0)

        def forcas():
            t = self.clk.get_value()
            wb = 7 + 6 * fbr.get_value()
            cb = interpolate_color(ManimColor(FC), ManimColor(WHITE_), fbr.get_value())
            a = math.sin(W * t)                        # a > 0: mola esticada → puxa uma para a outra
            g = VGroup()
            c1, c2 = self.P(0), self.P(1)
            L = 0.95 * a
            g.add(arrow(c1 + P3(0, 0.0), c1 + P3(L, 0), color=cb, width=wb, tip=0.17, z=12) if abs(L) > 0.08 else VMobject())
            g.add(arrow(c2 + P3(0, 0.0), c2 + P3(-L, 0), color=cb, width=wb, tip=0.17, z=12) if abs(L) > 0.08 else VMobject())
            # rótulos da mola acima das esferas, do lado de dentro (lado livre da seta); externas abaixo, por dentro
            rs = self.K * R
            g.add(mtex(r"\vec F_{1(2)}", FC, 32).next_to(c1 + P3(0.25, rs), UP, buff=0.2))
            g.add(mtex(r"\vec F_{2(1)}", FC, 32).next_to(c2 + P3(-0.25, rs), UP, buff=0.2))
            for c, nm, lado in ((c1, r"\vec F_1^{\,ext}", RIGHT), (c2, r"\vec F_2^{\,ext}", LEFT)):
                a = arrow(c + P3(0, -0.2), c + P3(0, -1.15), color=FC, width=6, tip=0.17, z=12)
                g.add(a)
                g.add(mtex(nm, FC, 32).next_to(a.get_center() + P3(0, -0.2), lado, buff=0.18))   # do lado de dentro, longe da fronteira
            return g
        fz = always_redraw(forcas)
        self.play(FadeIn(fr), FadeIn(fz), run_time=0.8)
        e1 = Mc((r"\frac{d\vec p_1}{dt}", MAG), "=", (r"\vec F_{1(2)}", FC), "+", (r"\vec F_1^{\,ext}", FC), size=52)
        e2 = Mc((r"\frac{d\vec p_2}{dt}", MAG), "=", (r"\vec F_{2(1)}", FC), "+", (r"\vec F_2^{\,ext}", FC), size=52)
        na_conta(e1, 1.6)
        na_conta(e2, 0.15)
        self.diz("Sobre a primeira esfera")
        self.play(FadeIn(e1[:2]), run_time=0.5)
        self.diz("a força da mola, que vem da segunda")
        self.play(TransformFromCopy(fz[2], e1[2]), fbr.animate(rate_func=there_and_back).set_value(1.0), run_time=0.9)
        self.diz("e o peso, que é externo")
        self.play(FadeIn(e1[3]), TransformFromCopy(fz[5], e1[4]), run_time=0.9)
        self.diz("Pela segunda lei")
        self.play(Circumscribe(e1, color=MAG, buff=0.08, time_width=0.6), run_time=1.1)
        self.diz("Na segunda esfera")
        self.play(FadeIn(e2[:2]), run_time=0.5)
        self.diz("a força da mola, que agora vem da primeira")
        self.play(TransformFromCopy(fz[3], e2[2]), run_time=0.8)
        self.diz("mais o peso dela")
        self.play(FadeIn(e2[3]), TransformFromCopy(fz[7], e2[4]), run_time=0.8)
        self.ate(0.97)
        # T7-3 — soma; as duas forças da mola se cancelam (TransformByGlyphMap)
        self.an("T7-3")
        ls = Line(P3(XC0, -0.55), P3(XC0 + 5.6, -0.55)).set_stroke(DIM, 2)
        mais_ = tex("+", WHITE_, 44).move_to(P3(XC0 - 0.3, 0.15))
        # v4: numa linha não cabe (6,6 de largura); quebra depois do "=", a continuação alinhada pelo "=", 0,3 abaixo da fração
        # (os índices dos glifos são os mesmos da linha única, para o TransformByGlyphMap)
        A = MathTex(r"\frac{d(\vec p_1+\vec p_2)}{dt}=\vec F_{1(2)}+\vec F_{2(1)}+\vec F^{\,ext}", font_size=36, color=WHITE_)
        assert len(A[0]) == 33
        A[0][0:13].set_color(MAG); A[0][14:20].set_color(FC); A[0][21:27].set_color(FC); A[0][28:33].set_color(FC)
        l2 = A[0][14:33]
        fra = A[0][0:13]
        l2.shift(P3(A[0][13].get_left()[0] - l2.get_left()[0], fra.get_bottom()[1] - 0.3 - l2.get_top()[1]))
        na_conta(A, -1.5)
        assert A.get_right()[0] <= 6.6
        self.diz("soma as duas equações")
        self.play(FadeIn(mais_), Create(ls), run_time=0.6)
        self.diz("À esquerda")
        self.play(TransformFromCopy(VGroup(e1[0], e2[0]), A[0][0:13]), TransformFromCopy(VGroup(e1[1], e2[1]), A[0][13]), run_time=1.0)
        self.diz("À direita")
        self.play(TransformFromCopy(e1[2], A[0][14:20]), FadeIn(A[0][20]), TransformFromCopy(e2[2], A[0][21:27]), FadeIn(A[0][27]),
                  TransformFromCopy(VGroup(e1[4], e2[4]), A[0][28:33]), run_time=1.1)
        self.diz("pela terceira lei")
        tl = txt("TERCEIRA LEI: IGUAIS E OPOSTAS", 18, color=WHITE_, op=0.8).next_to(A, DOWN, buff=0.3).align_to(A, LEFT)
        tl.set_y(min(tl.get_y(), -2.7))      # folga ≥ 0,25 da linha 3 e do quadro de dP/dt que entra depois
        self.play(Indicate(A[0][14:20], color=WHITE_), Indicate(A[0][21:27], color=WHITE_), FadeIn(tl),
                  fbr.animate(rate_func=there_and_back).set_value(1.0), run_time=1.0)
        self.play(fbr.animate(rate_func=there_and_back).set_value(1.0), run_time=0.8)
        self.diz("Somadas, elas dão zero")
        Bq = MathTex(r"\frac{d\vec P}{dt}=\vec F^{\,ext}", font_size=56, color=WHITE_)
        Bq[0][0:6].set_color(MAG); Bq[0][7:12].set_color(FC)
        na_conta(Bq, -1.45)
        # v5 (V3): primeiro risca o par da mola, ele sai; só então a linha vira dP/dt = F^ext (sem glifos embaralhados)
        rq = VGroup(risco(A[0][14:20], cor=WHITE_, w=4), risco(A[0][21:27], cor=WHITE_, w=4))
        self.play(Create(rq), run_time=0.6)
        self.play(FadeOut(VGroup(A[0][14:28], rq), shift=0.25 * DOWN), run_time=0.6)
        self.diz("Sobra só a força externa")
        self.play(FadeTransform(A[0][0:13], Bq[0][0:6]), ReplacementTransform(A[0][13], Bq[0][6]),
                  ReplacementTransform(A[0][28:33], Bq[0][7:12]), run_time=1.2)
        self.remove(A)
        self.add(Bq)
        cx = SurroundingRectangle(Bq, buff=0.14, corner_radius=0.08).set_stroke(MAG, 2.5)
        self.play(Create(cx), run_time=0.5)
        nt = txt("A MOLA TRABALHA; O TOTAL SÓ OUVE O DE FORA", 20, color=DIM).next_to(cx, DOWN, buff=0.3).align_to(cx, LEFT)
        self.diz("a mola estica")
        self.play(self.amp.animate(rate_func=there_and_back).set_value(1.8), fbr.animate(rate_func=there_and_back).set_value(1.0), run_time=1.6)
        self.diz("mas o momento total só escuta")
        self.play(FadeOut(tl), FadeIn(nt), run_time=0.6)
        self.ate(0.97)
        fz.clear_updaters(); fr.clear_updaters()
        self.conta2 = VGroup(e1, e2, ls, mais_, Bq, cx, nt)
        self.fz2, self.fr2 = fz, fr

    # ── T7-4, T7-5: partícula i; soma sobre todas ─────────────────────────────────────────────────────────
    def t7_4_5(self):
        self.an("T7-4")
        self.play(FadeOut(self.conta2), FadeOut(self.fz2), FadeOut(self.fr2), self.dois.animate.set_value(0.0), run_time=0.7)
        self.remove(self.fz2, self.fr2)
        self.vis[2].set_value(1.0); self.mvis[1].set_value(1.0); self.mvis[2].set_value(1.0)
        fr = self.front()
        self.play(FadeIn(fr), run_time=0.6)
        self.diz("Pega uma esfera qualquer")
        self.play(self.ebr[0].animate.set_value(1.0), run_time=0.6)
        li = always_redraw(lambda: mtex("i", WHITE_, 40).move_to(self.P(0) + P3(-0.95, 0.35)))
        self.add(li)
        e = Mc((r"\frac{d\vec p_i}{dt}", MAG), "=", r"\sum_j", (r"\vec F_{i(j)}", FC), "+", (r"\vec F_i^{\,ext}", FC), size=54, w=5.0)
        na_conta(e, 1.5)
        lg = linha(tex("i", WHITE_, 36), "RECEBE DE", tex("j", WHITE_, 36), size=22, buff=0.15)
        na_conta(lg, 0.25)
        self.diz("A taxa de variação do momento dela")
        self.play(FadeIn(e[:2], shift=0.1 * UP), run_time=0.7)
        self.diz("todas as outras esferas")
        self.play(FadeIn(e[2:4], shift=0.1 * UP), self.mbr[0].animate.set_value(1.0), self.mbr[1].animate.set_value(1.0), run_time=0.7)
        self.play(FadeIn(lg), run_time=0.5)
        self.diz("mais a força externa")
        self.play(FadeIn(e[4:], shift=0.1 * UP), self.mbr[0].animate.set_value(0.0), self.mbr[1].animate.set_value(0.0), run_time=0.7)
        self.ate(0.97)
        # T7-5 — soma sobre todas; P = Σ p_i; seta do momento total no meio (constante: o conjunto deriva devagar)
        self.an("T7-5")
        e2 = Mc((r"\frac{d\vec P}{dt}", MAG), "=", r"\sum_i", r"\sum_j", (r"\vec F_{i(j)}", FC), "+", (r"\vec F^{\,ext}", FC), size=54, w=5.0)
        na_conta(e2, 1.5)
        pd = Mc((r"\vec P", MAG), "=", (r"\sum_i \vec p_i", MAG), size=44)
        na_conta(pd, 0.1)
        self.play(FadeOut(lg), self.ebr[0].animate.set_value(0.0), FadeOut(li), TransformMatchingTex(e, e2), run_time=1.3)
        li.clear_updaters(); self.remove(li)
        pa = always_redraw(lambda: VGroup(
            arrow(self.m(VD * self.clk.get_value(), 1.0) + P3(-0.45, 0), self.m(VD * self.clk.get_value(), 1.0) + P3(0.75, 0), color=MAG, width=8, tip=0.2, z=14),
            mtex(r"\vec P", MAG, 36).move_to(self.m(VD * self.clk.get_value(), 1.0) + P3(0.15, 0.42))))
        self.diz("a soma dos momentos")
        self.play(FadeIn(pd, shift=0.1 * UP), run_time=0.7)
        self.diz("essa seta magenta")
        self.play(FadeIn(pa), run_time=0.6)
        b1 = Brace(VGroup(e2[2], e2[4]), DOWN, buff=0.12, color=DIM)
        b2 = Brace(e2[6], DOWN, buff=0.12, color=DIM).align_to(b1, UP)
        l1 = txt("SOMA DUPLA DAS INTERNAS", 18, color=DIM).next_to(b1, DOWN, buff=0.1)
        l2 = txt("EXTERNA TOTAL", 18, color=DIM).next_to(b2, DOWN, buff=0.1)
        if l2.get_left()[0] < l1.get_right()[0] + 0.2:          # rótulos lado a lado se tocariam: o da externa desce uma linha
            l2.next_to(b2, DOWN, buff=0.45)
        pd.generate_target(); na_conta(pd.target, -1.3)
        self.diz("uma soma dupla")
        self.play(MoveToTarget(pd), GrowFromCenter(b1), FadeIn(l1), self.pisca.animate.set_value(1.0), run_time=0.8)
        self.diz("e a força externa total")
        self.play(GrowFromCenter(b2), FadeIn(l2), run_time=0.7)
        self.ate(0.97)
        self.e2, self.br5, self.pd5, self.fr5, self.pa = e2, VGroup(b1, b2, l1, l2), pd, fr, pa

    # ── T7-6, T7-7: matriz de pares sincronizada com as molas; resultado ──────────────────────────────────
    def t7_6_7(self):
        self.an("T7-6")
        self.play(FadeOut(self.br5), FadeOut(self.pd5), FadeOut(self.e2), self.pisca.animate.set_value(0.0),
                  run_time=0.8)
        cw, ch = 1.25, 0.92
        x0, y0 = 2.75, 1.05                                    # centro da célula (1,1)
        cel = {}
        grade = VGroup()
        for i in range(3):
            for j in range(3):
                c = P3(x0 + j * cw, y0 - i * ch)
                r = Rectangle(width=cw, height=ch).set_stroke(DIM, 1.5).move_to(c)
                grade.add(r)
                cel[(i, j)] = (tex(r"\cdot", DIM, 40) if i == j else tex(rf"\vec F_{{{i + 1}({j + 1})}}", FC, 36)).move_to(c)
        cab = VGroup(*[tex(str(j + 1), WHITE_, 32).move_to(P3(x0 + j * cw, y0 + 0.72)) for j in range(3)])
        lin = VGroup(*[tex(str(i + 1), WHITE_, 32).move_to(P3(x0 - 0.9, y0 - i * ch)) for i in range(3)])
        tc = txt("COLUNA: QUEM FAZ", 18, color=DIM).move_to(P3(x0 + cw, y0 + 1.2))
        tl = txt("LINHA: QUEM RECEBE", 18, color=DIM).rotate(PI / 2).move_to(P3(x0 - 1.35, y0 - ch))
        self.diz("ela é só uma tabela")
        self.play(Create(grade), FadeIn(cab), FadeIn(lin), LaggedStart(*[FadeIn(cel[k]) for k in sorted(cel)], lag_ratio=0.08),
                  run_time=0.9)
        self.diz("Cada linha é quem recebe")
        self.play(FadeIn(tl), Indicate(lin, color=WHITE_), run_time=0.8)
        self.diz("cada coluna é quem faz")
        self.play(FadeIn(tc), Indicate(cab, color=WHITE_), run_time=0.8)
        pares = [((0, 1), (1, 0), 0), ((0, 2), (2, 0), 1), ((1, 2), (2, 1), 2)]
        zs = VGroup()
        for n, (a, b, k) in enumerate(pares):
            if n == 0:
                self.diz("Aqui está a força")
            elif n == 1:
                self.diz("O mesmo vale para os outros pares")
            hl = VGroup(*[SurroundingRectangle(cel[q], buff=0.08, corner_radius=0.06).set_stroke(BLUE_L, 3) for q in (a, b)])
            self.play(Create(hl), self.mbr[k].animate.set_value(1.0), run_time=0.6 if n == 0 else 0.45)
            if n == 0:
                sm = Mc((rf"\vec F_{{{a[0] + 1}({a[1] + 1})}}", FC), "+", (rf"\vec F_{{{b[0] + 1}({b[1] + 1})}}", FC), "=", "0", size=40)
                sm.move_to(P3(x0 + cw, y0 - 3 * ch - 0.3))             # v5 (V4): 0,3 abaixo da matriz
                self.diz("pela terceira lei ele soma zero")
                self.play(TransformFromCopy(VGroup(cel[a], cel[b]), sm), run_time=0.8)
                self.wait(0.3)
                self.play(FadeOut(sm), run_time=0.3)
            self.play(FadeOut(hl), self.mbr[k].animate.set_value(0.0), run_time=0.4)
        tot = Mc((r"\sum_i\sum_j \vec F_{i(j)}", FC), "=", "0", size=44).move_to(P3(x0 + cw, y0 - 3 * ch - 0.3))
        self.diz("A diagonal fica vazia")
        dg = VGroup(*[SurroundingRectangle(grade[4 * i], buff=-0.06, corner_radius=0.06).set_stroke(WHITE_, 3) for i in range(3)])
        self.play(LaggedStart(*[Create(r_) for r_ in dg], lag_ratio=0.25), run_time=0.9)    # v6 (1.3): a diagonal acende
        self.play(FadeOut(dg), run_time=0.4)
        self.diz("se apagam duas a duas")
        self.play(LaggedStart(*[AnimationGroup(cel[a].animate.set_opacity(0.13), cel[b].animate.set_opacity(0.13), self.mbr[k].animate
                                               (rate_func=there_and_back).set_value(1.0)) for a, b, k in pares], lag_ratio=0.45), run_time=1.8)
        self.diz("a soma dupla inteira vale zero")
        self.play(FadeIn(tot, shift=0.1 * UP), self.pisca.animate.set_value(1.0), run_time=0.8)
        self.ate(0.97)
        # T7-7 — o '?' do A6 vira dP/dt = F^ext
        self.an("T7-7")
        fim = Mc((r"\frac{d\vec P}{dt}", MAG), "=", (r"\vec F^{\,ext}", FC), size=72).move_to(P3(4.25, 0.9))
        cx = SurroundingRectangle(fim, buff=0.2, corner_radius=0.1).set_stroke(MAG, 3)
        self.play(FadeOut(VGroup(grade, cab, lin, tc, tl, tot, *cel.values())), self.pisca.animate.set_value(0.0), run_time=0.7)
        self.play(FadeIn(fim, shift=0.1 * UP), run_time=0.9)
        self.play(Create(cx), run_time=0.5)
        nt = txt("AS INTERNAS NÃO APARECEM", 22, color=DIM).next_to(cx, DOWN, buff=0.35)
        self.diz("As forças internas")
        self.play(FadeIn(nt), self.pisca.animate.set_value(1.0), run_time=0.8)
        self.diz("Só uma força de fora")
        d = dica("PRIMEIRO DEFINA O SISTEMA.", "SÓ FORÇA EXTERNA ENTRA NA VARIAÇÃO", "DO MOMENTO TOTAL")
        self.dica_entra(d)
        self.diz("A interrogação do canto")
        self.play(Indicate(self.q, color=WHITE_, scale_factor=1.3), self.pisca.animate.set_value(0.0), run_time=0.7)
        self.play(self.q.animate.move_to(cx.get_center()).scale(0.3).set_opacity(0), Indicate(fim, color=WHITE_, scale_factor=1.06),
                  run_time=1.1)                                            # v6 (1.3): o "?" voa para dentro da caixa
        self.remove(self.q)
        self.ate(0.97)
        self.dica_sai()
        self.fim7 = VGroup(fim, cx, nt)

    # ── T7-8: disco com binário (vista de cima) ──────────────────────────────────────────────────────────
    def t7_8(self):
        self.an("T7-8")
        self.fr5.clear_updaters(); self.pa.clear_updaters()
        self.play(FadeOut(self.fim7), FadeOut(self.fr5), FadeOut(self.pa), self.f3d.op.animate.set_value(0.25), run_time=0.5)
        self.remove(self.fr5, self.pa)
        t0 = self.clk.get_value()
        AL = 0.075                                          # aceleração angular (rad/s²)
        self.td0 = t0

        tb = [1e9]                                          # v5: o disco começa a girar quando o binário aparece

        def ang(t):
            return 0.5 * AL * max(0.0, t - tb[0] - 0.3) ** 2

        def disco(t):                                       # v7: fantasmas estroboscópicos do giro (a cada 0,3 s), só com giro visível
            a = ang(t)
            fa = [ang(t - 0.3 * k) for k in (1, 2, 3)]
            return {"vis": 1, "x": 0.0, "y": 0.0, "ang": a, "fant": fa if a - fa[-1] > 0.06 else []}
        self.disco = disco
        self.play(self.f3d.op.animate.set_value(1.0), run_time=0.6)

        def binario():                                      # v7: setas presas ao disco 3D (projeção exata da câmera do b3d.js)
            t = self.clk.get_value()
            a = ang(t)
            cam = self.cam_d(t)
            g = VGroup()
            for s in (1, -1):
                p3 = np.array([s * RD * math.cos(a), s * RD * math.sin(a), HD / 2])
                tg = s * np.array([-math.sin(a), math.cos(a), 0.0])
                g.add(arrow(proj3d(cam, p3), proj3d(cam, p3 + 1.25 * tg), color=FC, width=7, tip=0.2, z=12))
            g.add(Dot(proj3d(cam, (0, 0, HD)), radius=0.07, color=MAG).set_z_index(13))
            return g
        bn = always_redraw(binario)
        cm = txt("O CENTRO NÃO SAI DO LUGAR", 18, color=MAG).move_to(P3(-3.3, -2.75))
        l1 = linha("SE A FORÇA EXTERNA RESULTANTE", tex("=0", WHITE_, 40), size=24, buff=0.15)
        l2 = linha(tex(r"\Rightarrow", WHITE_, 40), tex(r"\vec P", MAG, 44), "CONSTANTE", size=24, buff=0.2)
        l3 = txt("MAS O DISCO GIRA", 22, color=FC)
        l4 = txt("GIRAR: MÓDULO DE ROTAÇÃO", 18, color=DIM)
        for m_, y in ((l1, 1.6), (l2, 0.75), (l3, -0.5), (l4, -1.3)):
            na_conta(m_, y)
        ni = txt("NÃO PRECISA ESTAR ISOLADO", 20, color=DIM)          # v5: a sutileza entra quando é dita (sem tela parada)
        na_conta(ni, 2.35)
        self.diz("o sistema não precisa estar isolado")
        self.play(FadeIn(ni, shift=0.1 * UP), run_time=0.6)
        self.diz("basta a força externa resultante")
        self.play(FadeIn(l1, shift=0.1 * UP), run_time=0.7)
        self.diz("Olha esse disco no gelo")
        tb[0] = self.clk.get_value()
        self.play(FadeIn(bn), run_time=0.7)
        self.diz("então o momento não muda")
        self.play(FadeIn(l2, shift=0.1 * UP), run_time=0.7)
        self.diz("o centro do disco")
        self.play(FadeIn(cm), run_time=0.6)
        self.diz("Mas o disco gira")
        self.play(FadeIn(l3), run_time=0.6)
        self.diz("Esse giro fica")
        self.play(FadeIn(l4), run_time=0.5)
        self.ate(0.97)
        bn.clear_updaters()
        self.conta8 = VGroup(l1, l2, l3, l4, cm, bn, ni)

    # ── T7-9: componente por componente; nota do campo ────────────────────────────────────────────────────
    def t7_9(self):
        self.an("T7-9")
        t0 = self.clk.get_value()
        X0, Y0, VX, VY, G_ = -6.6, -2.6, 1.95, 4.4, 3.0
        TV = 2 * VY / G_
        K_ = CAM_B["K"]

        lanc = self.lanc = [-1e9, t0 + self.ate_dizer("Na bola em parábola", mover=False)]   # v6: o voo na fala; antes, a bola parada no início

        def p3(s):                                          # v7: a mesma parábola, agora no 3D (x, z) — chão em z = 0
            return np.array([(X0 + VX * s) / K_, 0.0, R + (VY * s - 0.5 * G_ * s * s) / K_])

        def bola3(tt):
            ti = max(x for x in lanc if x <= tt + 1e-9)
            sr = -1.0 if ti < -1e8 else tt - ti
            s = min(max(sr, 0.0), TV)
            q = p3(s)
            fant = []
            if sr > 0:                                      # rastro estroboscópico: 8 cópias a cada 0,22 s, somem 1 s depois do pouso
                fo = min(1.0, max(0.0, 1 - (sr - TV) / 1.0))
                for k in range(1, 9):
                    sk = sr - 0.22 * k
                    if 0 <= sk <= TV and fo > 0:
                        fq = p3(sk)
                        fant.append([fq[0], fq[2], round(0.42 * (1 - k / 9) * fo, 3)])
            return {"x": q[0], "z": q[2], "fant": fant}
        self.bola3 = bola3

        def bola_():
            tt = self.clk.get_value()
            ti = max(x for x in lanc if x <= tt + 1e-9)
            s = 0.0 if ti < -1e8 else min(tt - ti, TV)
            c = proj3d(CAM_B, p3(s))
            vy = VY - G_ * s
            g = VGroup()
            if tt - ti >= TV:
                return g
            g.add(arrow(c + P3(0, -0.25), c + P3(0, -1.05), color=FC, width=6, tip=0.16, z=12))
            g.add(arrow(c + P3(0.28, 0), c + P3(0.28 + 0.55 * VX, 0), color=MAG, width=7, tip=0.17, z=12))
            g.add(mtex(r"P_x", MAG, 30).move_to(c + P3(0.28 + 0.55 * VX + 0.35, 0.22)))
            if abs(vy) > 0.25:
                g.add(arrow(c + P3(-0.3, 0), c + P3(-0.3, 0.28 * vy), color=MAG, width=6, tip=0.15, z=12))
                g.add(mtex(r"P_y", MAG, 30).move_to(c + P3(-0.75, 0.28 * vy * 0.6)))
            return g
        bb = always_redraw(bola_)
        so = txt("PESO SÓ NA VERTICAL", 18, color=FC).move_to(P3(-3.3, 2.45))
        self.play(FadeOut(self.conta8), self.f3d.op.animate.set_value(0.0), run_time=0.4)
        self.disco = None
        self.play(self.f3d.op.animate.set_value(1.0), FadeIn(bb), FadeIn(so), run_time=0.4)
        e1 = Mc((r"\frac{dP_x}{dt}", MAG), "=", (r"F^{\,ext}_x", FC), "=", "0", size=52)
        e2 = Mc((r"\frac{dP_y}{dt}", MAG), "=", (r"F^{\,ext}_y", FC), size=52)
        na_conta(e1, 1.7)
        na_conta(e2, 0.4)
        cp = txt("COMPONENTE POR COMPONENTE", 20, color=DIM)
        na_conta(cp, -0.55)
        self.diz("o peso só puxa na vertical")
        self.play(Indicate(so, color=WHITE_), run_time=0.8)
        self.diz("o momento horizontal fica constante")
        self.play(FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        self.diz("e o vertical muda")
        self.play(FadeIn(e2, shift=0.1 * UP), run_time=0.8)
        rp = chip_replay()
        self.diz("Uma direção pode conservar")
        self.lanc.append(self.clk.get_value())
        self.play(FadeIn(cp), FadeIn(rp), run_time=0.5)
        while self.clk.get_value() < self.lanc[-1] + TV:
            self.wait(1 / FPS)
        self.play(FadeOut(rp), run_time=0.3)
        # nota do campo: duas cargas em movimento e uma nuvem de campo esboçada
        self.diz("como entre cargas elétricas")
        t1 = self.clk.get_value()
        cx_, cy_ = 2.95, -1.75

        def campo():                                        # v7 (2,5D): duas cargas brilhantes (azul de carga) e linhas de campo com brilho
            u = self.clk.get_value() - t1                   # que correm de uma carga à outra
            a = P3(cx_ - 0.62 + 0.12 * math.sin(1.6 * u), cy_ + 0.08)
            b = P3(cx_ + 0.62, cy_ - 0.08 + 0.12 * math.cos(1.6 * u))
            g = VGroup()
            for k, h in enumerate((-0.62, -0.32, 0.0, 0.32, 0.62)):
                d = b - a
                n = P3(-d[1], d[0]) / max(np.linalg.norm(d), 1e-6)
                cv = CubicBezier(a, a + d * 0.25 + n * h * 1.25, b - d * 0.25 + n * h * 1.25, b)
                g.add(cv.copy().set_stroke(JC, 6, 0.07), cv.copy().set_stroke(JC, 1.6, 0.42))
                f = (0.45 * u + 0.23 * k) % 1.0
                g.add(cv.copy().pointwise_become_partial(cv, f, min(1.0, f + 0.16)).set_stroke(mix(JC, 0.6), 2.6, 0.9))
            for c, cor in ((a, "#267BFF"), (b, BLUE_L)):
                g.add(Dot(c, radius=0.3, color=cor).set_opacity(0.10), Dot(c, radius=0.2, color=cor).set_opacity(0.22),
                      Dot(c, radius=0.12, color=cor), Dot(c + P3(-0.035, 0.04), radius=0.045, color=WHITE_).set_opacity(0.85))
            return g
        cpo = always_redraw(campo)
        # v5 (V6): ícone e legenda inteiros na CONTA: o ícone em cima, a legenda em duas linhas embaixo dele
        nl = VGroup(linha("MOMENTO DAS PARTÍCULAS", mais(28), size=18, buff=0.12),
                    linha("MOMENTO DO CAMPO", mais(28, "="), "CONSTANTE", size=18, buff=0.12)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        nl.move_to(P3(XC0 + nl.width / 2, cy_ - 0.85 - 0.3 - nl.height / 2))
        assert nl.get_right()[0] <= 7.3 and nl.get_bottom()[1] >= -3.6
        self.play(FadeIn(cpo), run_time=0.7)
        self.diz("o momento do campo")
        self.play(FadeIn(nl, shift=0.1 * UP), run_time=0.5)
        self.sobra(0.55)
        bb.clear_updaters(); cpo.clear_updaters()
        self.clear(rt=0.5)
