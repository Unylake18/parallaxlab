"""Lote PH (v2): hook H1–H3 com o cavalo 3D e abertura A1–A6 ligada ao yt_0015 (um corpo → dois corpos → sistema)."""
from kit import *  # noqa: F401,F403
from sec_cavalo import Cavalo3D


def disco(r=0.42, cor=STEEL):
    return VGroup(Circle(radius=r).set_stroke(mix(cor, 0.45), 2.5).set_fill(cor, 1.0),
                  Circle(radius=r * 0.35).set_stroke(width=0).set_fill(mix(cor, 0.25), 1.0))


def mesa(x0, x1, y, h=0.22):
    """Colchão de ar visto de lado: faixa PANEL com furinhos."""
    g = VGroup(Rectangle(width=x1 - x0, height=h).set_stroke(BLUE_L, 1.5, 0.6).set_fill(PANEL, 1.0).move_to(P3((x0 + x1) / 2, y - h / 2)))
    for x in np.arange(x0 + 0.25, x1 - 0.1, 0.42):
        g.add(Dot(P3(x, y - h / 2), radius=0.025, color=BLUE_L).set_opacity(0.5))
    return g


class LoteHook(Base):
    def construct(self):
        self.setup_base()
        self.hook()
        self.abertura()
        self.fim()
        self.relatorio()

    # ── H1–H3 ─────────────────────────────────────────────────────────────────────────────────────────────
    def hook(self):
        self.an("H1")
        cv = self.cv = Cavalo3D(self, v=lambda t: 0.42, K=1.1, xt=1.9, yc=-2.5, op=0.0)
        self.add(cv.f3d)
        self.play(cv.f3d.op.animate.set_value(1.0), run_time=1.0)
        pulso = ValueTracker(0.0)
        L = 1.45

        def setas():
            p = cv.pts()
            k = cv.K.get_value()
            w = 7 + 3 * pulso.get_value()
            a1 = arrow(p["corda_pedra"] + P3(0.05, -0.12), p["corda_pedra"] + P3(0.05 + L * k, -0.12), color=FC, width=w, tip=0.2, z=12)
            a2 = arrow(p["peito"] + P3(0.6 * k + L * k, 0), p["peito"] + P3(0.6 * k, 0), color=FC, width=w, tip=0.2, z=12)
            l1 = mtex(r"\vec F", FC, 40).next_to(a1, DOWN, buff=0.1)
            l2 = mtex(r"-\vec F", FC, 40).next_to(a2, DOWN, buff=0.1)
            return VGroup(a1, a2, l1, l2)
        sg = always_redraw(setas)
        self.ate(0.3)
        self.play(FadeIn(sg), run_time=0.8)
        self.ate(0.97)
        # H2 — pulsam juntas; interrogação suave
        self.an("H2")
        q = always_redraw(lambda: mtxt("?", 80, bold=True, op=0.7).move_to(cv.pts()["topo"] + P3(0, 0.75)))
        for k in range(3):
            self.play(pulso.animate.set_value(1.0), run_time=0.5, rate_func=there_and_back)
            self.wait(0.6)
        self.ate(0.45)
        self.play(FadeIn(q), run_time=0.7)
        for k in range(2):
            self.play(pulso.animate.set_value(1.0), run_time=0.5, rate_func=there_and_back)
            self.wait(0.8)
        self.ate(0.97)
        # H3 — câmera recua, pergunta no centro
        self.an("H3")
        p1 = txt("SE A CORDA PUXA O CAVALO PARA TRÁS", 34, bold=True)
        p2 = txt("COM A MESMA FORÇA, COMO ELE ANDA?", 34, bold=True)
        per = VGroup(p1, p2).arrange(DOWN, buff=0.2).move_to(P3(0, 2.3))
        self.play(FadeOut(q), FadeOut(sg), cv.K.animate.set_value(0.82), cv.yc.animate.set_value(-2.2), cv.xt.animate.set_value(1.2),
                  run_time=1.6)
        q.clear_updaters(); sg.clear_updaters()
        self.remove(q, sg)
        self.play(FadeIn(per, shift=0.1 * UP), cv.f3d.op.animate.set_value(0.55), run_time=0.9)
        self.ate(0.97)
        self.per = per

    # ── A1–A6 ─────────────────────────────────────────────────────────────────────────────────────────────
    def abertura(self):
        cv = self.cv
        self.an("A1")
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        bv = txt("BEM-VINDOS AO PARALLAX LAB", 30, op=0.9).move_to(P3(0, -0.5))
        self.play(FadeOut(self.per), FadeIn(logo, scale=0.94), FadeIn(bv, shift=0.1 * UP), cv.f3d.op.animate.set_value(0.3), run_time=1.0)
        self.ate(0.97)
        # A2 — título do vídeo, cavalo recuado ao fundo
        self.an("A2")
        tt = txt("MOMENTO EM SISTEMAS", 54, bold=True).move_to(P3(0, 1.3))
        sub = txt("NESTE VÍDEO: O QUE MUDA O MOMENTO DE VÁRIOS CORPOS", 26, color=DIM).next_to(tt, DOWN, buff=0.35)
        self.play(FadeOut(logo), FadeOut(bv), run_time=0.4)
        self.play(FadeIn(tt, shift=0.1 * UP), FadeIn(sub), cv.f3d.op.animate.set_value(0.35), run_time=0.9)
        self.ate(0.97)
        self.a3(tt, sub)
        self.a4()
        self.a5()
        self.a6()

    def a3(self, tt, sub):
        """Um corpo: o disco do vídeo anterior; empurrão curto; curva F(t) com a área; F_res = dp/dt → J = ∫F dt = Δp."""
        cv = self.cv
        self.an("A3")
        self.play(FadeOut(tt), FadeOut(sub), cv.f3d.op.animate.set_value(0.0), run_time=0.6)
        self.remove(cv.f3d)
        self.secao("O VÍDEO ANTERIOR: UM CORPO")
        YM = 1.0
        ms = mesa(-7.2, 0.5, YM)
        tag = txt("UM CORPO", 20, color=DIM).move_to(P3(-6.3, YM + 1.45))
        G = Graf(-6.6, -2.7, 5.6, 1.0, 0, 1.0, 1.6, rot_y=tex(r"F_{\text{res}}", FC, 30))
        t0 = self.clk.get_value()
        PER, V0, V1 = 8.0, 0.4, 0.95
        TA, TB = 2.2, 3.4                    # empurrão (s do ciclo)

        def fase():
            return (self.clk.get_value() - t0) % PER

        def Fbump(u):                        # u ∈ [0,1] dentro do empurrão
            return math.sin(PI * u) ** 2

        def v_de(s):
            if s < TA:
                return V0
            if s < TB:
                u = (s - TA) / (TB - TA)
                return V0 + (V1 - V0) * (u - math.sin(2 * PI * u) / (2 * PI))
            return V1

        def x_de(s):
            n = 60
            ss = np.linspace(0, s, n)
            return -6.6 + np.trapz([v_de(q) for q in ss], ss)

        def cena():
            s = fase()
            d = disco().move_to(P3(x_de(s), YM + 0.42))
            g = VGroup(d)
            v = v_de(s)
            pa = arrow(d.get_center() + P3(0.0, 0.75), d.get_center() + P3(0.9 * v, 0.75), color=MAG, width=7, tip=0.18)
            g.add(pa, mtex(r"\vec p", MAG, 36).next_to(pa, UP, buff=0.06))
            if TA <= s < TB:
                u = (s - TA) / (TB - TA)
                fa = arrow(d.get_left() + P3(-1.0 - 0.3 * Fbump(u), 0), d.get_left() + P3(-0.05, 0), color=FC, width=7, tip=0.18)
                g.add(fa, mtex(r"\vec F_{\text{res}}", FC, 34).next_to(fa, UP, buff=0.08))
            # curva F(t) do ciclo e a área até o instante
            uu = min(1.0, max(0.0, (s - TA) / (TB - TA)))
            if s >= TA:
                cur = G.curva(lambda q: Fbump(q), 0.0, max(uu, 1e-3), n=60, cor=FC, w=4)
                pts = [G.pt(q, Fbump(q)) for q in np.linspace(0, max(uu, 1e-3), 40)]
                area = Polygon(G.pt(0, 0), *pts, G.pt(max(uu, 1e-3), 0)).set_stroke(width=0).set_fill(JC, 0.55)
                g.add(area, cur)
                if uu > 0.6:
                    g.add(mtex(r"\vec J", JC, 36).move_to(G.pt(0.5, 0.35)))
            # some/entra suave na troca de ciclo
            op = min(1.0, s / 0.4, (PER - s) / 0.4)
            return g.set_opacity(op) if op < 1 else g
        cn = always_redraw(cena)
        self.play(FadeIn(ms), FadeIn(tag), FadeIn(G.eixos), run_time=0.7)
        self.add(cn)
        self.mesa, self.tag = ms, tag
        # CONTA: F_res = dp/dt, com os símbolos saindo do desenho
        self.ate(0.2)
        while fase() < TA + 0.5 or fase() > TB:
            self.wait(1 / FPS)
        lf = mtex(r"\vec F_{\text{res}}", FC, 34).move_to(P3(-5.5, YM + 0.75))
        e1 = Mc((r"\vec F_{\text{res}}", FC), "=", (r"\frac{d\vec p}{dt}", MAG), size=56)
        na_conta(e1, 1.5)
        fl = [m for m in cn.submobjects if isinstance(m, MathTex) and r"F_{\text{res}}" in m.get_tex_string()]
        pl = [m for m in cn.submobjects if isinstance(m, MathTex) and m.get_tex_string() == r"\vec p"]
        src_f = fl[0].copy() if fl else lf
        src_p = pl[0].copy() if pl else lf
        self.play(TransformFromCopy(src_f, e1[0]), FadeIn(e1[1]), TransformFromCopy(src_p, e1[2]), run_time=1.1)
        self.ate(0.55)
        while fase() < TB - 0.05 or fase() > TB + 0.6:
            self.wait(1 / FPS)
        e2 = Mc((r"\vec J", JC), "=", r"\int", (r"\vec F_{\text{res}}", FC), r"\,dt", "=", (r"\Delta\vec p", MAG), size=56)
        na_conta(e2, -0.3)
        jl = [m for m in cn.submobjects if isinstance(m, MathTex) and m.get_tex_string() == r"\vec J"]
        src_j = jl[0].copy() if jl else e1[0].copy()
        self.play(TransformFromCopy(src_j, e2[0]), FadeIn(e2[1]), FadeIn(e2[2]), TransformFromCopy(e1[0], e2[3]), FadeIn(e2[4]), run_time=1.1)
        self.play(FadeIn(e2[5]), TransformFromCopy(e1[2], e2[6]), run_time=0.8)
        ar = txt("A ÁREA EMBAIXO DA CURVA", 20, color=JC).next_to(e2, DOWN, buff=0.3).align_to(e2, LEFT)
        self.ate(0.85)
        self.play(FadeIn(ar), run_time=0.5)
        self.ate(0.97)
        self.cn, self.eq3 = cn, VGroup(e1, e2, ar, G.eixos)

    def a4(self):
        """Dois corpos: dois discos colidindo em loop; forças iguais e opostas no contato; Δp1 = −Δp2 → P constante."""
        self.an("A4")
        self.secao("O VÍDEO ANTERIOR: DOIS CORPOS")
        self.cn.clear_updaters()
        self.play(FadeOut(self.cn), FadeOut(self.eq3), FadeOut(self.tag), run_time=0.5)
        self.remove(self.cn)
        YM = 1.0
        t0 = self.clk.get_value()
        PER, V, R = 6.0, 1.1, 0.42
        TC = 2.1                                  # instante do contato no ciclo
        DT = 0.35

        def cena():
            s = (self.clk.get_value() - t0) % PER
            # antes: A → (+V), B ← (−V); depois: trocam (massas iguais, elástico)
            if s < TC:
                xa, xb, va, vb = -3.35 - R - V * (TC - s), -3.35 + R + V * (TC - s), V, -V
            elif s < TC + DT:
                u = (s - TC) / DT
                va, vb = V * (1 - 2 * u), -V * (1 - 2 * u)
                xa, xb = -3.35 - R + 0.06 * math.sin(PI * u), -3.35 + R - 0.06 * math.sin(PI * u)
            else:
                xa, xb, va, vb = -3.35 - R - V * (s - TC - DT), -3.35 + R + V * (s - TC - DT), -V, V
            A = disco(R, GEO).move_to(P3(xa, YM + R))
            B = disco(R, STEEL).move_to(P3(xb, YM + R))
            g = VGroup(A, B, mtex(r"1", BACKGROUND_COLOR, 30).move_to(A), mtex(r"2", WHITE_, 30).move_to(B))
            for D, v, nm in ((A, va, r"\vec p_1"), (B, vb, r"\vec p_2")):
                if abs(v) > 0.05:
                    a = arrow(D.get_center() + P3(0, 0.8), D.get_center() + P3(0.95 * v, 0.8), color=MAG, width=7, tip=0.17)
                    g.add(a, mtex(nm, MAG, 32).next_to(a, UP, buff=0.05))
            if TC - 0.05 <= s < TC + DT + 0.05:
                c = (A.get_center() + B.get_center()) / 2
                f1 = arrow(c + P3(-0.05, -0.0), c + P3(-1.3, 0), color=FC, width=7, tip=0.18, z=12).shift(DOWN * 1.05)
                f2 = arrow(c + P3(0.05, 0), c + P3(1.3, 0), color=FC, width=7, tip=0.18, z=12).shift(DOWN * 1.05)
                g.add(f1, f2)
            op = min(1.0, s / 0.35, (PER - s) / 0.35)
            return g.set_opacity(op) if op < 1 else g
        cn = always_redraw(cena)
        lab = txt("DOIS CORPOS", 20, color=DIM).move_to(P3(-6.2, YM + 1.45))
        self.play(FadeIn(cn), FadeIn(lab), run_time=0.6)
        e1 = Mc((r"\Delta\vec p_1", MAG), "=", (r"-\Delta\vec p_2", MAG), size=60)
        na_conta(e1, 1.3)
        self.ate(0.25)
        self.play(FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        e2 = linha(tex(r"\vec P", MAG, 60), mais(56, "="), txt("CONSTANTE", 34, bold=True), buff=0.25)
        na_conta(e2, -0.2)
        ds = txt("DOIS CORPOS SOZINHOS", 20, color=DIM).next_to(e2, DOWN, buff=0.28).align_to(e2, LEFT)
        seta = tex(r"\Downarrow", WHITE_, 46).move_to(P3(XC0 + 0.5, 0.55))
        self.ate(0.6)
        self.play(FadeIn(seta), FadeIn(e2, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(ds), run_time=0.5)
        self.ate(0.97)
        self.cn2, self.eq4, self.lab4 = cn, VGroup(e1, e2, ds, seta), lab

    def a5(self):
        """O cavalo volta: fronteira só no cavalo (corda = força como outra qualquer) → fronteira cresce (corda vira interna)."""
        self.an("A5")
        self.secao("A DIFERENÇA DE HOJE")
        self.cn2.clear_updaters()
        self.play(FadeOut(self.cn2), FadeOut(self.eq4), FadeOut(self.lab4), FadeOut(self.mesa), run_time=0.5)
        self.remove(self.cn2)
        cv = self.cv
        cv.K.set_value(0.95); cv.xt.set_value(2.3); cv.yc.set_value(-2.55)
        self.add(cv.f3d)
        self.play(cv.f3d.op.animate.set_value(1.0), run_time=0.8)
        cresce = ValueTracker(0.0)
        cinza = ValueTracker(0.0)

        def front():
            p = cv.pts()
            u = cresce.get_value()
            xr = p["cabeca"][0] + 0.45
            xl_c = p["cav_tras"][0] - 0.35
            xl_s = p["pedra_tras"][0] - 0.35
            xl = xl_c + (xl_s - xl_c) * u
            y0, y1 = p["cascos"][1] - 0.25, p["topo"][1] + 0.25
            r = RoundedRectangle(corner_radius=0.3, width=xr - xl, height=y1 - y0).move_to(P3((xl + xr) / 2, (y0 + y1) / 2))
            r.set_stroke(WHITE_, 2.2, opacity=0.62)
            d = DashedVMobject(r, num_dashes=int((xr - xl + y1 - y0) * 5), dashed_ratio=0.55).set_z_index(1)
            rot = mtxt("CAVALO" if u < 0.5 else "SISTEMA: CAVALO + CORDA + PEDRA", 18, op=0.8)
            rot.next_to(r.get_corner(UL), UP, buff=0.1).align_to(r, LEFT).shift(0.25 * RIGHT)
            return VGroup(d, rot)
        fr = always_redraw(front)

        def forca():
            p = cv.pts()
            k = cv.K.get_value()
            c = interpolate_color(ManimColor(FC), ManimColor(INT), cinza.get_value())
            a = arrow(p["peito"] + P3(0.6 * k + 1.45 * k, 0), p["peito"] + P3(0.6 * k, 0), color=c, width=7, tip=0.2, z=12)
            l = mtex(r"\vec T", FC, 40) if cinza.get_value() < 0.5 else mtxt("INTERNA", 18, color=INT)
            return VGroup(a, l.next_to(a, DOWN, buff=0.12))
        fc = always_redraw(forca)
        self.ate(0.3)
        self.play(FadeIn(fr), FadeIn(fc), run_time=0.9)
        l1 = txt("UM CORPO: TODA FORÇA CONTA", 24).move_to(P3(0, Y_LEG + 0.05))
        self.play(FadeIn(l1, shift=0.1 * UP), run_time=0.6)
        self.ate(0.6)
        l2 = linha("SISTEMA: INTERNAS", tex(r"\times", WHITE_, 34), "EXTERNAS", size=24, buff=0.15)
        leg = VGroup(l1.copy(), tex(r"\to", WHITE_, 36), l2).arrange(RIGHT, buff=0.3).move_to(P3(0, Y_LEG + 0.05))
        self.play(cresce.animate.set_value(1.0), run_time=2.2)
        self.play(cinza.animate.set_value(1.0), l1.animate.move_to(leg[0]), FadeIn(leg[1]), FadeIn(l2), run_time=1.0)
        self.ate(0.88)
        qq = txt("?", 44, bold=True, color=MAG).next_to(fc, UP, buff=0.25)
        self.play(FadeIn(qq, scale=0.7), run_time=0.5)
        self.ate(0.97)
        self.fr5, self.fc5, self.leg5 = fr, fc, VGroup(l1, leg[1], l2, qq)

    def a6(self):
        """Mapa dos dois vídeos na CONTA, cavalo andando no PALCO; o '?' fica no canto da CONTA."""
        cv = self.cv
        self.an("A6")
        self.secao("ONDE A GENTE ESTÁ")
        for m in (self.fr5, self.fc5):
            m.clear_updaters()
        self.play(FadeOut(self.fr5), FadeOut(self.fc5), FadeOut(self.leg5), cv.K.animate.set_value(0.7), cv.xt.animate.set_value(-1.2),
                  cv.yc.animate.set_value(-2.3), run_time=1.4)
        self.remove(self.fr5, self.fc5)
        r1 = txt("VÍDEO ANTERIOR · UM CORPO", 24, color=DIM)
        q1 = Mc((r"\vec F_{\text{res}}", FC), "=", (r"\frac{d\vec p}{dt}", MAG), size=50)
        r2 = txt("HOJE · MUITOS CORPOS", 26, bold=True)
        b1 = VGroup(r1, q1).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        na_conta(b1, 1.3)
        na_conta(r2, -0.6)
        ok = txt("RESOLVIDO", 18, color=DIM).next_to(q1, RIGHT, buff=0.35)
        self.play(FadeIn(b1, shift=0.1 * UP), run_time=0.8)
        self.play(b1.animate.set_opacity(0.45), FadeIn(ok), run_time=0.6)
        self.ate(0.4)
        self.play(FadeIn(r2, shift=0.1 * UP), run_time=0.7)
        q = txt("?", 64, bold=True, color=MAG).next_to(r2, DOWN, buff=0.3).align_to(r2, LEFT)
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.ate(0.75)
        self.play(q.animate.move_to(P3(6.6, 2.15)).scale(0.8), run_time=0.9)
        self.ate(0.97)
