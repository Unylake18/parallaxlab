"""Lote P8 (v2): T8 — força interna não move o sistema. Cavalo 3D (asset do yt_0015) arrastando a pedra e acelerando de verdade
(0,32 m/s² a partir de 0,3 m/s, em tomadas de 10 s que se repetem; a câmera acompanha); gelo sob as patas no T8-6 (a ≈ −1,26 m/s²);
Cyrano 2D (T8-7); manequim 3D andando (T8-8). Números: 2.352 / 2.800 / 448 / 0,32 / 2.608 / 192 / 588 N."""
from kit import *  # noqa: F401,F403
from sec_cavalo import Cavalo3D
from sec_manequim import Manequim3D, pose_andar

MC, MP, MU, G_ = 600, 800, 0.3, 9.8
FP = MU * MP * G_                    # atrito cinético na pedra
FCH = 2800.0
A = (FCH - FP) / (MC + MP)
T = MP * A + FP
FM = 0.1 * MC * G_                   # gelo: atrito estático máximo nas patas
A_GELO = (FM - FP) / (MC + MP)
assert abs(FP - 2352) < 1e-9 and abs(A - 0.32) < 1e-12 and abs(T - 2608) < 1e-9 and abs(FCH - T - MC * A) < 1e-9 and abs(FM - 588) < 1e-9
assert abs(A_GELO + 1.26) < 0.005
V0, TOM = 0.3, 10.0                  # tomada: v vai de 0,3 a 3,5 m/s em 10 s e recomeça
KS = 0.00057                         # comprimento das setas por newton


def num(s, cor=WHITE_, size=40):
    return MathTex(s, font_size=size, color=cor)


class LoteT8(Base):
    def construct(self):
        self.setup_base(cap="FORÇA INTERNA NÃO MOVE O SISTEMA")
        self.modo = "acelera"
        self.t_gelo = None
        self.montar()
        self.t8_1()
        self.t8_2_3_4()
        self.t8_5()
        self.t8_6()
        self.t8_7()
        self.t8_8()
        self.fim()
        self.relatorio()

    # ── cavalo 3D: velocidade por tomadas ────────────────────────────────────────────────────────────────
    def v(self, t):
        if self.t_gelo is not None and t >= self.t_gelo:
            s = (t - self.t_gelo) % 6.0
            return max(0.0, 2.0 + A_GELO * s)
        s = t % TOM
        return V0 + A * s

    def deslize(self, t):
        if self.t_gelo is not None and t >= self.t_gelo:
            return 1.6                              # cascos girando no gelo
        return 0.0

    def gelo(self, t):
        if self.t_gelo is None or t < self.t_gelo - 1.0:
            return 0.0
        return min(1.0, (t - self.t_gelo + 1.0) / 1.0)

    def mergulho(self, t):
        """Escurece 0,35 s na troca de tomada (a velocidade recomeça)."""
        if self.t_gelo is not None and t >= self.t_gelo - 0.35:
            u, P = (t - self.t_gelo) % 6.0, 6.0
        else:
            u, P = t % TOM, TOM
        return 0.25 + 0.75 * min(1.0, u / 0.35, (P - u) / 0.35)

    def montar(self):
        cv = self.cv = Cavalo3D(self, v=self.v, K=0.92, xt=-1.3, yc=-2.3, op=0.0, deslize=self.deslize, gelo=self.gelo)
        self.add(cv.f3d)
        self._reset = {}
        cv.f3d.mult = self.mergulho

        def faixa(t, xp):                           # o gelo começa sob as patas de trás no início da tomada
            if self.t_gelo is None:
                return (0.0, 0.0)
            k = int(max(0.0, t - self.t_gelo) // 6.0)
            if k not in self._reset:
                f0 = int(round((self.t_gelo + 6.0 * k) * FPS))
                self._reset[k] = cv._acum(f0)[0]
            x0 = self._reset[k]
            return (x0 - 2.45, x0 + 40.0)
        cv.gx = faixa

    def p(self):
        return self.cv.pts()

    def setas(self, fch=lambda: FCH, rot=True, tens=True, num_=False):
        """Setas no cavalo: chão nas patas (FC, para a frente), chão na pedra (FC, para trás), tensão (INT) nas pontas da corda."""
        cv = self.cv

        def f():
            p = cv.pts()
            k = cv.K.get_value()
            g = VGroup()
            yb = p["cascos"][1] - 0.3
            xh = p["cascos"][0] - 0.2
            F = fch()
            g.add(arrow(P3(xh, yb), P3(xh + KS * F * 1.1, yb), color=FC, width=7, tip=0.2, z=12))
            xs = p["pedra_base"][0] + 0.2
            g.add(arrow(P3(xs, yb), P3(xs - KS * FP * 1.1, yb), color=FC, width=7, tip=0.2, z=12))
            if rot:
                g.add(mtxt("CHÃO NAS PATAS", 15, color=FC).next_to(g[0], DOWN, buff=0.08))
                g.add(mtxt("CHÃO NA PEDRA", 15, color=FC).next_to(g[1], DOWN, buff=0.08))
            if num_:
                g.add(mtex(rf"{int(round(F)):,}".replace(",", ".") + r"\ \mathrm{N}", FC, 28).next_to(g[0], UP, buff=0.06))
                g.add(mtex(r"2.352\ \mathrm{N}", FC, 28).next_to(g[1], UP, buff=0.06))
            if tens:
                L = KS * T * 1.0
                g.add(arrow(p["corda_pedra"] + P3(0.05, -0.14), p["corda_pedra"] + P3(0.05 + L, -0.14), color=INT, width=6, tip=0.17, z=12))
                g.add(arrow(p["peito"] + P3(0.55 * k + L, 0), p["peito"] + P3(0.55 * k, 0), color=INT, width=6, tip=0.17, z=12))
            return g
        return always_redraw(f)

    def fronteira_c(self, rot="SISTEMA: CAVALO + CORDA + PEDRA"):
        cv = self.cv

        def f():
            p = cv.pts()
            xl, xr = p["pedra_tras"][0] - 0.3, p["cabeca"][0] + 0.35
            y0, y1 = p["cascos"][1] - 0.15, p["topo"][1] + 0.22
            r = RoundedRectangle(corner_radius=0.3, width=xr - xl, height=y1 - y0).move_to(P3((xl + xr) / 2, (y0 + y1) / 2))
            r.set_stroke(WHITE_, 2.2, opacity=0.62)
            d = DashedVMobject(r, num_dashes=int((xr - xl + y1 - y0) * 5), dashed_ratio=0.55).set_z_index(1)
            lab = mtxt(rot, 16, op=0.8).next_to(r.get_corner(UL), UP, buff=0.1).align_to(r, LEFT).shift(0.25 * RIGHT)
            return VGroup(d, lab)
        return always_redraw(f)

    # ── T8-1 ─────────────────────────────────────────────────────────────────────────────────────────────
    def t8_1(self):
        self.an("T8-1")
        cv = self.cv
        self.play(cv.f3d.op.animate.set_value(1.0), run_time=1.0)
        fr = self.fronteira_c()
        self.ate(0.12)
        self.play(FadeIn(fr), run_time=0.8)
        sg = self.setas(tens=True)
        so = [sg]
        li = txt("INTERNA: A CORDA", 22, color=INT, bold=True)
        di = txt("PUXA A PEDRA E O CAVALO; SOME DA CONTA", 18, color=DIM)
        le = txt("EXTERNAS NA HORIZONTAL", 22, color=FC, bold=True)
        de = txt("CHÃO NAS PATAS E CHÃO NA PEDRA", 18, color=DIM)
        pn = txt("PESO E NORMAL: VERTICAIS, SE CANCELAM", 18, color=DIM)
        for m_, y in ((li, 2.1), (di, 1.7), (le, 0.95), (de, 0.55), (pn, -0.3)):
            na_conta(m_, y)
        self.ate(0.25)
        self.add(sg)
        sg.set_opacity(0)
        self.play(sg.animate.set_opacity(1), FadeIn(li), FadeIn(di), run_time=0.9)
        self.ate(0.55)
        self.play(FadeIn(le), FadeIn(de), run_time=0.8)
        self.ate(0.85)
        self.play(FadeIn(pn), run_time=0.6)
        self.ate(0.97)
        self.fr, self.sg = fr, sg
        self.conta1 = VGroup(li, di, le, de, pn)

    # ── T8-2, T8-3, T8-4 ─────────────────────────────────────────────────────────────────────────────────
    def t8_2_3_4(self):
        cv = self.cv
        self.an("T8-2")
        self.play(FadeOut(self.conta1), run_time=0.4)
        self.sg.clear_updaters(); self.remove(self.sg)
        sg = self.setas(num_=True)
        self.add(sg)
        mc = always_redraw(lambda: mtex(r"600\ \mathrm{kg}", WHITE_, 30).move_to(cv.pts()["topo"] + P3(-1.4, 0.3)))
        mp = always_redraw(lambda: mtex(r"800\ \mathrm{kg}", WHITE_, 28).move_to(cv.pts()["pedra_topo"] + P3(0, 0.32)))
        self.play(FadeIn(mc), FadeIn(mp), run_time=0.6)
        d1 = Mc(r"m_{\text{cavalo}}=", r"600\ \mathrm{kg}", size=40)
        d2 = Mc(r"m_{\text{pedra}}=", r"800\ \mathrm{kg}", size=40)
        na_conta(d1, 2.25); na_conta(d2, 1.75)
        self.ate(0.1)
        self.play(FadeIn(d1[0]), TransformFromCopy(mc, d1[1]), FadeIn(d2[0]), TransformFromCopy(mp, d2[1]), run_time=1.0)
        e1 = Mc((r"f_{\text{pedra}}", FC), r"=0{,}3\cdot 800\cdot 9{,}8=", (r"2.352\ \mathrm{N}", FC), size=40)
        na_conta(e1, 1.05)
        lc = txt("CINÉTICO: A PEDRA JÁ DESLIZA", 16, color=DIM)
        na_conta(lc, 0.6)
        self.ate(0.35)
        self.play(FadeIn(e1[:2]), FadeIn(lc), run_time=0.8)
        self.play(TransformFromCopy(sg[5], e1[2]), run_time=0.8)
        e2 = Mc((r"F_{\text{chão}}", FC), "=", (r"2.800\ \mathrm{N}", FC), size=40)
        na_conta(e2, -0.05)
        self.ate(0.78)
        self.play(FadeIn(e2[:2]), TransformFromCopy(sg[4], e2[2]), run_time=0.9)
        self.ate(0.97)
        # T8-3 — sistema inteiro: a corda nem aparece
        self.an("T8-3")
        e3 = Mc(r"(2.800-2.352)", "=", r"(600+800)", r"\,a", size=42)
        na_conta(e3, -0.85)
        cn = txt("A CORDA NEM APARECE", 16, color=INT)
        self.play(TransformFromCopy(VGroup(e2[2], e1[2]), e3[0]), FadeIn(e3[1]), TransformFromCopy(VGroup(d1[1], d2[1]), e3[2]), FadeIn(e3[3]),
                  run_time=1.2)
        na_conta(cn, -1.35)
        self.play(FadeIn(cn), run_time=0.8)
        e4 = Mc(r"a=", (r"0{,}32\ \mathrm{m/s^2}", VEL), size=46)
        na_conta(e4, -2.15)
        cx = SurroundingRectangle(e4, buff=0.12, corner_radius=0.08).set_stroke(VEL, 2.5)
        self.ate(0.7)
        self.play(FadeIn(e4, shift=0.1 * UP), Create(cx), run_time=0.9)
        av = always_redraw(lambda: VGroup(
            arrow(cv.pts()["topo"] + P3(-0.6, 0.35), cv.pts()["topo"] + P3(0.7, 0.35), color=VEL, width=6, tip=0.17, z=12),
            mtex(r"\vec a", VEL, 32).move_to(cv.pts()["topo"] + P3(0.95, 0.62))))
        self.play(FadeIn(av), run_time=0.6)
        self.ate(0.97)
        # T8-4 — separando os corpos: os dois lados batem
        self.an("T8-4")
        self.play(FadeOut(VGroup(d1, d2, e1, lc, e2, e3, cn)), e4.animate.move_to(P3(6.2, 2.3)), cx.animate.move_to(P3(6.2, 2.3)), run_time=0.8)
        p1 = txt("PEDRA", 20, color=DIM)
        q1 = Mc((r"T", INT), r"-2.352=800\cdot 0{,}32", size=42)
        q1b = Mc(r"\Rightarrow", (r"T", INT), "=", (r"2.608\ \mathrm{N}", INT), size=44)
        p2 = txt("CAVALO", 20, color=DIM)
        q2 = Mc(r"2.800-", (r"T", INT), r"=600\cdot 0{,}32", size=42)
        q2b = Mc(r"\Rightarrow", r"192\ \mathrm{N}", r"=192\ \mathrm{N}", size=44)
        for m_, y in ((p1, 1.6), (q1, 1.1), (q1b, 0.45), (p2, -0.35), (q2, -0.85), (q2b, -1.5)):
            na_conta(m_, y)
        self.play(FadeIn(p1), FadeIn(q1), run_time=0.9)
        self.ate(0.3)
        self.play(FadeIn(q1b, shift=0.1 * UP), run_time=0.8)
        self.ate(0.55)
        self.play(FadeIn(p2), FadeIn(q2), run_time=0.9)
        self.ate(0.78)
        self.play(FadeIn(q2b, shift=0.1 * UP), run_time=0.8)
        ok = txt("FECHA: MESMA TENSÃO NAS DUAS PONTAS", 18, color=DIM)
        na_conta(ok, -2.2)
        self.play(FadeIn(ok), run_time=0.5)
        self.ate(0.97)
        self.sg, self.mc, self.mp, self.av = sg, mc, mp, av
        self.conta4 = VGroup(p1, q1, q1b, p2, q2, q2b, ok)
        self.e4 = VGroup(e4, cx)

    # ── T8-5 — a resposta ─────────────────────────────────────────────────────────────────────────────────
    def t8_5(self):
        cv = self.cv
        self.an("T8-5")
        self.play(FadeOut(self.conta4), run_time=0.5)
        cmp_ = always_redraw(lambda: VGroup(
            mtex(r"2.608\ \mathrm{N}", INT, 28).next_to(self.sg[7], UP, buff=0.06)))
        self.play(FadeIn(cmp_), run_time=0.8)
        r1 = txt("O CAVALO ANDA PORQUE", 30, bold=True)
        r2 = txt("O CHÃO O EMPURRA;", 30, bold=True, color=FC)
        r3 = txt("A CORDA SÓ TRANSMITE", 30, bold=True, color=INT)
        rr = VGroup(r1, r2, r3).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        na_conta(rr, 0.9)
        cp = Mc((r"2.800\ \mathrm{N}", FC), ">", (r"2.608\ \mathrm{N}", INT), size=44)
        na_conta(cp, -0.85)
        self.ate(0.25)
        self.play(TransformFromCopy(self.sg[4], cp[0]), FadeIn(cp[1]), TransformFromCopy(cmp_[0], cp[2]), run_time=1.0)
        self.ate(0.5)
        self.play(FadeIn(r1, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(r2, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(r3, shift=0.1 * UP), run_time=0.6)
        self.ate(0.97)
        self.conta5 = VGroup(rr, cp)
        self.cmp_ = cmp_

    # ── T8-6 — gelo sob as patas ──────────────────────────────────────────────────────────────────────────
    def t8_6(self):
        cv = self.cv
        self.an("T8-6")
        self.cmp_.clear_updaters(); self.av.clear_updaters()
        self.play(FadeOut(self.conta5), FadeOut(self.cmp_), FadeOut(self.av), FadeOut(self.e4), run_time=0.5)
        self.remove(self.cmp_, self.av)
        self.t_gelo = self.clk.get_value() + 1.0
        self.sg.clear_updaters(); self.remove(self.sg)
        enc = ValueTracker(0.0)
        sg = self.setas(fch=lambda: FCH + (FM - FCH) * enc.get_value(), num_=True, tens=False)
        self.add(sg)
        lg = always_redraw(lambda: mtxt("GELO SOB AS PATAS", 16, color=BLUE_L).move_to(cv.pts()["cascos"] + P3(0.6, -1.05)))
        self.wait(1.0)
        self.play(enc.animate.set_value(1.0), FadeIn(lg), run_time=1.2)
        e1 = Mc(r"\mu_e\approx 0{,}1", size=40)
        e2 = Mc((r"f_{\text{máx}}", FC), r"=0{,}1\cdot 600\cdot 9{,}8=", (r"588\ \mathrm{N}", FC), size=40)
        e3 = Mc((r"588", FC), "<", (r"2.352", FC), size=44)
        e4 = Mc(r"a\approx", (r"-1{,}26\ \mathrm{m/s^2}", VEL), size=44)
        ce = txt("CERCA DE: ESCORREGANDO, O ATRITO É UM POUCO MENOR", 15, color=DIM)
        for m_, y in ((e1, 2.15), (e2, 1.45), (e3, 0.6), (e4, -0.25), (ce, -0.8)):
            na_conta(m_, y)
        self.ate(0.18)
        self.play(FadeIn(e1), run_time=0.5)
        self.play(FadeIn(e2[:2]), TransformFromCopy(sg[4], e2[2]), run_time=0.9)
        self.ate(0.5)
        self.play(FadeIn(e3, shift=0.1 * UP), run_time=0.7)
        self.ate(0.65)
        self.play(FadeIn(e4, shift=0.1 * UP), FadeIn(ce), run_time=0.8)
        f1 = txt("O CAVALO É O MESMO, A CORDA É A MESMA.", 20)
        f2 = txt("O QUE MUDOU FOI A FORÇA EXTERNA", 22, bold=True, color=FC)
        for m_, y in ((f1, -1.6), (f2, -2.1)):
            na_conta(m_, y)
        self.ate(0.82)
        self.play(FadeIn(f1), FadeIn(f2), run_time=0.8)
        self.ate(0.97)
        self.sg, self.lg = sg, lg
        self.conta6 = VGroup(e1, e2, e3, e4, ce, f1, f2)

    # ── T8-7 — Cyrano (2D, ilustração leve) ───────────────────────────────────────────────────────────────
    def t8_7(self):
        cv = self.cv
        self.an("T8-7")
        for m_ in (self.sg, self.lg, self.fr, self.mc, self.mp):
            m_.clear_updaters()
        self.play(FadeOut(VGroup(self.sg, self.lg, self.fr, self.mc, self.mp, self.conta6)), cv.f3d.op.animate.set_value(0.0), run_time=0.7)
        self.remove(self.sg, self.lg, self.fr, self.mc, self.mp, cv.f3d)
        Y_CH = -2.2
        piso = chao(-7.2, 0.4, Y_CH)
        t0 = self.clk.get_value()
        PER = 2.6

        def cyr():
            s = ((self.clk.get_value() - t0) % PER) / PER
            # o ímã sobe e volta; a placa (com a pessoa) dá um pulinho para cima e para baixo: o centro de massa não sai do lugar
            yi = 1.5 * math.sin(PI * s)
            yp = 0.06 * math.sin(PI * s)
            g = VGroup()
            chapa = RoundedRectangle(corner_radius=0.05, width=3.4, height=0.26).set_stroke(mix(TERRA, 0.4), 2).set_fill(TERRA, 1) \
                .move_to(P3(-3.4, Y_CH + 0.13 + yp))
            pz = dict(cf=1.52, jf=1.62, ct=1.5, jt=1.6)
            pes = PessoaPerfil(-4.25, yp, 2.5, 1, "joga", quadril=Y_CH + 0.26 + 0.12 + yp, extra=pz)
            mao = pes.pts["mao_f"]
            im = ima().scale(1.25).move_to(mao + P3(0.08, 0.32 + yi))
            g.add(chapa, pes, im)
            if 0.12 < s < 0.88:
                g.add(arrow(im.get_bottom() + P3(0, -0.05), im.get_bottom() + P3(0, -0.6), color=INT, width=5, tip=0.15, z=10))
                g.add(arrow(chapa.get_top() + P3(1.0, 0.02), chapa.get_top() + P3(1.0, 0.6), color=INT, width=5, tip=0.15, z=10))
            return g
        cy = always_redraw(cyr)
        lua = VGroup(Circle(radius=0.42).set_stroke(width=0).set_fill(GEO, 0.85),
                     Circle(radius=0.38).set_stroke(width=0).set_fill(BACKGROUND_COLOR, 1).shift(P3(0.16, 0.08))).move_to(P3(-0.5, 2.2))
        self.play(FadeIn(piso), FadeIn(cy), FadeIn(lua), run_time=1.0)
        fr = fronteira(5.2, 4.7, P3(-3.4, -0.05), rotulo=["PESSOA", mais(), "PLACA", mais(), "ÍMÃ"])
        self.ate(0.42)
        self.play(Create(fr[0]), FadeIn(fr[1]), run_time=1.0)
        c1 = txt("CORDA E ÍMÃ:", 30, bold=True)
        c2 = txt("SÓ FORÇAS INTERNAS", 30, bold=True, color=INT)
        nf = txt("NÃO MUDAM O MOMENTO DO CONJUNTO", 20, color=DIM)
        VGroup(c1, c2, nf).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        for m_ in (c1, c2, nf):
            na_conta(m_, m_.get_y() + 0.6)
        self.ate(0.6)
        self.play(FadeIn(c1, shift=0.1 * UP), FadeIn(c2, shift=0.1 * UP), run_time=0.8)
        self.ate(0.8)
        self.play(FadeIn(nf), run_time=0.5)
        self.ate(0.97)
        cy.clear_updaters()
        self.cyr = VGroup(piso, cy, lua, fr, c1, c2, nf)

    # ── T8-8 — o manequim andando: o atrito do chão no pé ────────────────────────────────────────────────
    def t8_8(self):
        self.an("T8-8")
        self.play(FadeOut(self.cyr), run_time=0.6)
        self.remove(*self.cyr)
        t0 = self.clk.get_value()
        VA, PS = 1.05, 0.62
        CYC = PS / 0.6

        def pose(t):
            x = VA * max(0.0, t - t0)
            p = pose_andar(x, x / CYC, 1, passo=PS)
            p["chao"] = "terra"
            return p
        mq = self.mq = Manequim3D(self, pose, K=2.05, xt=-3.4, yc=-2.75, op=0.0, seguir=True)
        self.add(mq.f3d)
        self.play(mq.f3d.op.animate.set_value(1.0), run_time=0.8)

        def atrito():
            e = mq.f3d.e
            x = e["hx"]
            fase = (x / CYC) % 1.0
            # pé de apoio mais atrás (empurrando)
            cand = [(i, (fase + 0.5 * i) % 1.0) for i in (0, 1)]
            cand = [c for c in cand if c[1] < 0.6]
            i = max(cand, key=lambda c: c[1])[0] if cand else 0
            pe = mq.m(e["pes"][i][0], 0.0)
            g = VGroup(arrow(pe + P3(-0.1, -0.22), pe + P3(1.05, -0.22), color=FC, width=7, tip=0.18, z=12),
                       mtxt("ATRITO DO CHÃO", 15, color=FC).move_to(pe + P3(0.5, -0.52)))
            ch = arrow(pe + P3(0.2, 0.12), pe + P3(-0.7, 0.12), color=INT, width=5, tip=0.15, z=12)
            return VGroup(g, ch, mtxt("PÉ EMPURRA O CHÃO", 14, color=INT).move_to(pe + P3(-0.4, 0.42)))
        at = always_redraw(atrito)
        self.ate(0.15)
        self.play(FadeIn(at), run_time=0.7)
        l1 = txt("A GENTE EMPURRA A TERRA PARA TRÁS", 22)
        l2 = txt("O ATRITO EMPURRA A GENTE PARA A FRENTE", 22, color=FC, bold=True)
        l3 = txt("NO GELO, QUASE NÃO HÁ ATRITO", 18, color=DIM)
        for m_, y in ((l1, 1.8), (l2, 1.2), (l3, 0.35)):
            na_conta(m_, y)
        self.play(FadeIn(l1), run_time=0.6)
        self.ate(0.35)
        self.play(FadeIn(l2), run_time=0.6)
        self.ate(0.55)
        self.play(FadeIn(l3), run_time=0.5)
        self.ate(0.62)
        d = dica("QUEM ACELERA O CONJUNTO É A FORÇA EXTERNA.", "A CORDA SÓ TRANSMITE")
        self.dica_entra(d)
        self.ate(0.97)
        self.dica_sai()
        at.clear_updaters()
        self.clear(rt=0.5)
