"""Lote P7 (v2): T7 — sistemas de partículas, derivado passo a passo.
PALCO 3D (threejs/cena3d/esf.js): esferas de aço ligadas por molas, vibrando e derivando devagar (o conjunto tem momento constante);
dois corpos com uma mola (T7-2/3, cancelamento por TransformByGlyphMap) → partícula i → soma → matriz de pares sincronizada com as molas
→ dP/dt = F^ext → disco com binário (vista de cima) → componentes (parábola 2D) + nota do campo."""
from MF_Tools import TransformByGlyphMap

from kit import *  # noqa: F401,F403

R = 0.45
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

    def pos(self, t):
        a = math.sin(W * t) * self.amp.get_value()
        d = self.dois.get_value()
        ab = 0.07 + 0.11 * d
        cx = VD * t
        return [(cx - XB - ab * a, R), (cx + XB + ab * a, R), (cx, ZT - 0.1 * a)], cx

    def estado(self, t):
        ps, cx = self.pos(t)
        pis = 0.5 + 0.5 * math.sin(2 * PI * t / 1.4)
        if self.disco is not None:
            return {"esf": [], "molas": [], "disco": self.disco(t), "piso": 0,
                    "cam": {"modo": "topo", "K": 1.0, "xc": -3.3, "yc": -0.35, "camx": 0, "camy": 0, "fov": 16}}
        return {"esf": [[x, z, int(self.vis[i].get_value() > 0.5), self.ebr[i].get_value()] for i, (x, z) in enumerate(ps)],
                "molas": [[i, j, int(self.mvis[k].get_value() > 0.5), max(self.mbr[k].get_value(), self.pisca.get_value() * pis)]
                          for k, (i, j) in enumerate(((0, 1), (0, 2), (1, 2)))],
                "piso": 1, "cam": cam_frente(K=self.K, xc=self.xt, yc=self.yc, camx=cx, fov=16, el=4)}

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
            y0, y1 = (min(ys) - r - 0.75, max(ys) + r + 0.75) if so_baixo else (min(ys) - r - 0.3, max(ys) + r + 0.4)
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
        self.add(self.f3d)
        self.play(self.f3d.op.animate.set_value(1.0), run_time=1.0)
        fr = self.front()
        self.ate(0.2)
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
        self.ate(0.4)
        self.play(self.pisca.animate.set_value(1.0), FadeIn(b1, shift=0.1 * UP), FadeIn(ic), run_time=0.9)
        self.ate(0.62)
        self.play(ex.animate.set_value(1.0), FadeIn(b2, shift=0.1 * UP), FadeIn(ie), run_time=0.9)
        ch = txt("A ESCOLHA DA FRONTEIRA É NOSSA", 22, bold=True).move_to(P3(0, Y_LEG + 0.05))
        self.ate(0.85)
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
            g.add(mtex(r"\vec F_{1(2)}", FC, 34).move_to(c1 + P3(0, 0.98)))
            g.add(mtex(r"\vec F_{2(1)}", FC, 34).move_to(c2 + P3(0, 0.98)))
            for c, nm in ((c1, r"\vec F_1^{\,ext}"), (c2, r"\vec F_2^{\,ext}")):
                g.add(arrow(c + P3(0, -0.2), c + P3(0, -1.15), color=FC, width=6, tip=0.17, z=12))
                g.add(mtex(nm, FC, 32).move_to(c + P3(-0.75 if c is c1 else 0.75, -0.95)))
            return g
        fz = always_redraw(forcas)
        self.play(FadeIn(fr), FadeIn(fz), run_time=0.8)
        e1 = Mc((r"\frac{d\vec p_1}{dt}", MAG), "=", (r"\vec F_{1(2)}", FC), "+", (r"\vec F_1^{\,ext}", FC), size=52)
        e2 = Mc((r"\frac{d\vec p_2}{dt}", MAG), "=", (r"\vec F_{2(1)}", FC), "+", (r"\vec F_2^{\,ext}", FC), size=52)
        na_conta(e1, 1.6)
        na_conta(e2, 0.15)
        self.ate(0.25)
        self.play(FadeIn(e1[:2]), run_time=0.5)
        self.play(TransformFromCopy(fz[2], e1[2]), run_time=0.9)
        self.ate(0.45)
        self.play(FadeIn(e1[3]), TransformFromCopy(fz[5], e1[4]), run_time=0.9)
        self.ate(0.7)
        self.play(FadeIn(e2[:2]), TransformFromCopy(fz[3], e2[2]), FadeIn(e2[3]), TransformFromCopy(fz[7], e2[4]), run_time=1.1)
        self.ate(0.97)
        # T7-3 — soma; as duas forças da mola se cancelam (TransformByGlyphMap)
        self.an("T7-3")
        ls = Line(P3(XC0, -0.55), P3(XC0 + 5.6, -0.55)).set_stroke(DIM, 2)
        mais_ = tex("+", WHITE_, 44).move_to(P3(XC0 - 0.3, 0.15))
        A = MathTex(r"\frac{d(\vec p_1+\vec p_2)}{dt}=\vec F_{1(2)}+\vec F_{2(1)}+\vec F^{\,ext}", font_size=42, color=WHITE_)
        A[0][0:13].set_color(MAG); A[0][14:20].set_color(FC); A[0][21:27].set_color(FC); A[0][28:33].set_color(FC)
        na_conta(A, -1.45)
        self.play(FadeIn(mais_), Create(ls), run_time=0.6)
        self.play(TransformFromCopy(VGroup(e1[0], e2[0]), A[0][0:13]), TransformFromCopy(VGroup(e1[1], e2[1]), A[0][13]),
                  TransformFromCopy(e1[2], A[0][14:20]), FadeIn(A[0][20]), TransformFromCopy(e2[2], A[0][21:27]), FadeIn(A[0][27]),
                  TransformFromCopy(VGroup(e1[4], e2[4]), A[0][28:33]), run_time=1.4)
        self.ate(0.35)
        tl = txt("TERCEIRA LEI: IGUAIS E OPOSTAS", 20, color=FC).next_to(A, DOWN, buff=0.3).align_to(A, LEFT)
        self.play(Indicate(A[0][14:20], color=WHITE_), Indicate(A[0][21:27], color=WHITE_), FadeIn(tl),
                  fbr.animate(rate_func=there_and_back).set_value(1.0), run_time=1.0)
        self.play(fbr.animate(rate_func=there_and_back).set_value(1.0), run_time=0.8)
        self.ate(0.55)
        Bq = MathTex(r"\frac{d\vec P}{dt}=\vec F^{\,ext}", font_size=56, color=WHITE_)
        Bq[0][0:6].set_color(MAG); Bq[0][7:12].set_color(FC)
        na_conta(Bq, -1.45)
        self.play(TransformByGlyphMap(A, Bq, (list(range(0, 13)), list(range(0, 6))), ([13], [6]), (list(range(28, 33)), list(range(7, 12))),
                                      (list(range(14, 28)), [], {"shift": 0.3 * DOWN}), auto_fade=True), run_time=1.6)
        cx = SurroundingRectangle(Bq, buff=0.14, corner_radius=0.08).set_stroke(MAG, 2.5)
        self.play(Create(cx), run_time=0.5)
        nt = txt("A MOLA TRABALHA; O TOTAL SÓ OUVE O DE FORA", 20, color=DIM).next_to(cx, DOWN, buff=0.3).align_to(cx, LEFT)
        self.ate(0.8)
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
        self.play(FadeIn(fr), self.ebr[0].animate.set_value(1.0), run_time=0.8)
        li = always_redraw(lambda: mtex("i", WHITE_, 40).move_to(self.P(0) + P3(-0.95, 0.35)))
        self.add(li)
        e = Mc((r"\frac{d\vec p_i}{dt}", MAG), "=", r"\sum_j", (r"\vec F_{i(j)}", FC), "+", (r"\vec F_i^{\,ext}", FC), size=54, w=5.0)
        na_conta(e, 1.5)
        lg = linha(tex("i", WHITE_, 36), "RECEBE DE", tex("j", WHITE_, 36), size=22, buff=0.15)
        na_conta(lg, 0.25)
        self.ate(0.25)
        self.play(FadeIn(e, shift=0.1 * UP), run_time=1.0)
        self.play(self.mbr[0].animate.set_value(1.0), self.mbr[1].animate.set_value(1.0), run_time=0.6)
        self.ate(0.6)
        self.play(FadeIn(lg), self.mbr[0].animate.set_value(0.0), self.mbr[1].animate.set_value(0.0), run_time=0.7)
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
        self.ate(0.3)
        self.play(FadeIn(pd, shift=0.1 * UP), FadeIn(pa), run_time=0.8)
        b1 = Brace(VGroup(e2[2], e2[4]), DOWN, buff=0.12, color=DIM)
        b2 = Brace(e2[6], DOWN, buff=0.12, color=DIM).align_to(b1, UP)
        l1 = txt("SOMA DUPLA DAS INTERNAS", 18, color=DIM).next_to(b1, DOWN, buff=0.1)
        l2 = txt("EXTERNA TOTAL", 18, color=DIM).next_to(b2, DOWN, buff=0.1)
        pd.generate_target(); na_conta(pd.target, -1.3)
        self.ate(0.6)
        self.play(MoveToTarget(pd), GrowFromCenter(b1), FadeIn(l1), GrowFromCenter(b2), FadeIn(l2), self.pisca.animate.set_value(1.0), run_time=0.9)
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
        self.play(Create(grade), FadeIn(cab), FadeIn(lin), FadeIn(tc), FadeIn(tl), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(cel[k]) for k in sorted(cel)], lag_ratio=0.08), run_time=1.2)
        pares = [((0, 1), (1, 0), 0), ((0, 2), (2, 0), 1), ((1, 2), (2, 1), 2)]
        zs = VGroup()
        for n, (a, b, k) in enumerate(pares):
            self.ate(0.3 + 0.2 * n)
            hl = VGroup(*[SurroundingRectangle(cel[q], buff=0.08, corner_radius=0.06).set_stroke(BLUE_L, 3) for q in (a, b)])
            self.play(Create(hl), self.mbr[k].animate.set_value(1.0), run_time=0.6)
            if n == 0:
                sm = Mc((rf"\vec F_{{{a[0] + 1}({a[1] + 1})}}", FC), "+", (rf"\vec F_{{{b[0] + 1}({b[1] + 1})}}", FC), "=", "0", size=40)
                sm.move_to(P3(x0 + cw, y0 - 3 * ch + 0.05))
                self.play(TransformFromCopy(VGroup(cel[a], cel[b]), sm), run_time=0.9)
                self.wait(0.6)
                self.play(FadeOut(sm), run_time=0.4)
            self.play(cel[a].animate.set_opacity(0.13), cel[b].animate.set_opacity(0.13), FadeOut(hl), self.mbr[k].animate.set_value(0.0),
                      run_time=0.6)
        tot = Mc((r"\sum_i\sum_j \vec F_{i(j)}", FC), "=", "0", size=44).move_to(P3(x0 + cw, y0 - 3 * ch + 0.05))
        self.ate(0.88)
        self.play(FadeIn(tot, shift=0.1 * UP), self.pisca.animate.set_value(1.0), run_time=0.8)
        self.ate(0.97)
        # T7-7 — o '?' do A6 vira dP/dt = F^ext
        self.an("T7-7")
        fim = Mc((r"\frac{d\vec P}{dt}", MAG), "=", (r"\vec F^{\,ext}", FC), size=72).move_to(P3(4.25, 0.9))
        cx = SurroundingRectangle(fim, buff=0.2, corner_radius=0.1).set_stroke(MAG, 3)
        self.play(FadeOut(VGroup(grade, cab, lin, tc, tl, tot, *cel.values())), self.pisca.animate.set_value(0.0), run_time=0.7)
        self.play(ReplacementTransform(self.q, fim), run_time=1.2)
        self.play(Create(cx), run_time=0.5)
        nt = txt("AS INTERNAS NÃO APARECEM", 22, color=DIM).next_to(cx, DOWN, buff=0.35)
        self.ate(0.4)
        self.play(FadeIn(nt), run_time=0.8)
        self.ate(0.55)
        d = dica("PRIMEIRO DEFINA O SISTEMA.", "SÓ FORÇA EXTERNA ENTRA NA VARIAÇÃO", "DO MOMENTO TOTAL")
        self.dica_entra(d)
        self.ate(0.97)
        self.dica_sai()
        self.fim7 = VGroup(fim, cx, nt)

    # ── T7-8: disco com binário (vista de cima) ──────────────────────────────────────────────────────────
    def t7_8(self):
        self.an("T7-8")
        self.fr5.clear_updaters(); self.pa.clear_updaters()
        self.play(FadeOut(self.fim7), FadeOut(self.fr5), FadeOut(self.pa), self.f3d.op.animate.set_value(0.0), run_time=0.7)
        self.remove(self.fr5, self.pa)
        t0 = self.clk.get_value()
        AL = 0.075                                          # aceleração angular (rad/s²)
        RD = 1.35

        def ang(t):
            return 0.5 * AL * max(0.0, t - t0 - 1.2) ** 2
        self.disco = lambda t: {"vis": 1, "x": 0.0, "y": 0.0, "ang": ang(t)}
        self.play(self.f3d.op.animate.set_value(1.0), run_time=0.8)

        def binario():
            t = self.clk.get_value()
            a = ang(t)
            c = P3(-3.3, -0.35)
            g = VGroup()
            for s in (1, -1):
                p = c + s * RD * P3(math.cos(a), math.sin(a))
                tg = s * P3(-math.sin(a), math.cos(a))
                g.add(arrow(p, p + 1.1 * tg, color=FC, width=7, tip=0.2, z=12))
            g.add(Dot(c, radius=0.07, color=MAG).set_z_index(13))
            return g
        bn = always_redraw(binario)
        cm = txt("O CENTRO NÃO SAI DO LUGAR", 18, color=MAG).move_to(P3(-3.3, -2.75))
        self.ate(0.3)
        self.play(FadeIn(bn), run_time=0.7)
        l1 = linha("SE A FORÇA EXTERNA RESULTANTE", tex("=0", WHITE_, 40), size=24, buff=0.15)
        l2 = linha(tex(r"\Rightarrow", WHITE_, 40), tex(r"\vec P", MAG, 44), "CONSTANTE", size=24, buff=0.2)
        l3 = txt("MAS O DISCO GIRA", 22, color=FC)
        l4 = txt("GIRAR: MÓDULO DE ROTAÇÃO", 18, color=DIM)
        for m_, y in ((l1, 1.6), (l2, 0.75), (l3, -0.5), (l4, -1.3)):
            na_conta(m_, y)
        self.ate(0.15)
        self.play(FadeIn(l1, shift=0.1 * UP), run_time=0.7)
        self.ate(0.3)
        self.play(FadeIn(l2, shift=0.1 * UP), run_time=0.7)
        self.ate(0.55)
        self.play(FadeIn(l3), FadeIn(cm), run_time=0.7)
        self.ate(0.82)
        self.play(FadeIn(l4), run_time=0.5)
        self.ate(0.97)
        bn.clear_updaters()
        self.conta8 = VGroup(l1, l2, l3, l4, cm, bn)

    # ── T7-9: componente por componente; nota do campo ────────────────────────────────────────────────────
    def t7_9(self):
        self.an("T7-9")
        self.play(FadeOut(self.conta8), self.f3d.op.animate.set_value(0.0), run_time=0.6)
        self.remove(self.f3d)
        t0 = self.clk.get_value()
        X0, Y0, VX, VY, G_ = -6.6, -2.6, 1.95, 4.4, 3.0
        TV = 2 * VY / G_
        piso = Line(P3(-7.3, Y0 - 0.22), P3(0.6, Y0 - 0.22)).set_stroke(GEO, 2, 0.5)
        traj = DashedVMobject(VMobject().set_points_smoothly([P3(X0 + VX * s, Y0 + VY * s - 0.5 * G_ * s * s) for s in np.linspace(0, TV, 40)])
                              .set_stroke(DIM, 2, 0.5), num_dashes=40)

        def bola_():
            s = (self.clk.get_value() - t0) % (TV + 0.6)
            s = min(s, TV)
            c = P3(X0 + VX * s, Y0 + VY * s - 0.5 * G_ * s * s)
            vy = VY - G_ * s
            g = VGroup(bola(0.22, GEO).move_to(c))
            g.add(arrow(c + P3(0, -0.25), c + P3(0, -1.05), color=FC, width=6, tip=0.16, z=12))
            g.add(arrow(c + P3(0.28, 0), c + P3(0.28 + 0.55 * VX, 0), color=MAG, width=7, tip=0.17, z=12))
            g.add(mtex(r"P_x", MAG, 30).move_to(c + P3(0.28 + 0.55 * VX + 0.35, 0.22)))
            if abs(vy) > 0.25:
                g.add(arrow(c + P3(-0.3, 0), c + P3(-0.3, 0.28 * vy), color=MAG, width=6, tip=0.15, z=12))
                g.add(mtex(r"P_y", MAG, 30).move_to(c + P3(-0.75, 0.28 * vy * 0.6)))
            return g
        bb = always_redraw(bola_)
        so = txt("PESO SÓ NA VERTICAL", 18, color=FC).move_to(P3(-3.3, 2.45))
        self.play(FadeIn(piso), FadeIn(traj), FadeIn(bb), FadeIn(so), run_time=0.8)
        e1 = Mc((r"\frac{dP_x}{dt}", MAG), "=", (r"F^{\,ext}_x", FC), "=", "0", size=52)
        e2 = Mc((r"\frac{dP_y}{dt}", MAG), "=", (r"F^{\,ext}_y", FC), size=52)
        na_conta(e1, 1.7)
        na_conta(e2, 0.4)
        cp = txt("COMPONENTE POR COMPONENTE", 20, color=DIM)
        na_conta(cp, -0.55)
        self.ate(0.12)
        self.play(FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        self.ate(0.3)
        self.play(FadeIn(e2, shift=0.1 * UP), FadeIn(cp), run_time=0.8)
        # nota do campo: duas cargas em movimento e uma nuvem de campo esboçada
        self.ate(0.62)
        t1 = self.clk.get_value()
        cx_, cy_ = 2.6, -2.15

        def campo():
            u = self.clk.get_value() - t1
            g = VGroup()
            for k in range(3):
                g.add(Ellipse(width=2.2 + 0.5 * k, height=1.0 + 0.25 * k).set_stroke(JC, 1.5, 0.35 - 0.09 * k).move_to(P3(cx_, cy_)))
            g.add(Dot(P3(cx_ - 0.55 + 0.12 * math.sin(1.6 * u), cy_ + 0.1), radius=0.09, color=FC),
                  Dot(P3(cx_ + 0.55, cy_ - 0.1 + 0.12 * math.cos(1.6 * u)), radius=0.09, color=MAG))
            return g
        cpo = always_redraw(campo)
        nl = linha("MOMENTO DAS PARTÍCULAS", mais(28), "MOMENTO DO CAMPO", mais(28, "="), "CONSTANTE", size=18, buff=0.12)
        nl.move_to(P3(4.6, -3.25))
        nl.shift(RIGHT * min(0.0, 7.35 - nl.get_right()[0]))
        self.play(FadeIn(cpo), FadeIn(nl, shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)
        bb.clear_updaters(); cpo.clear_updaters()
        self.clear(rt=0.5)
