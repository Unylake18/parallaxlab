"""Lote PH (v4): hook H1–H3 com o cavalo 3D (narração v3, curto) e abertura A1–A6 ligada ao yt_0015 (um corpo → dois corpos → sistema).
v4: o cavalo já anda no primeiro quadro; −T⃗ no balancim (atrás da anca) e T⃗ na pedra; push-in e recuo da câmera; viradas de cena em
sequência (sai tudo, depois entra o novo); A2 com a miniatura parada do último quadro do hook; A3 e A4 rodam o evento uma vez; o cavalo
volta no A5 (a mesma tomada contínua) e sai antes do A6, que é o mapa no centro."""
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


def tres_esferas(c, r=0.2):
    """Ícone das três esferas ligadas por molas (o T7)."""
    ps = [c + P3(-0.42, -0.25), c + P3(0.42, -0.25), c + P3(0, 0.38)]
    g = VGroup(*[mola(ps[i], ps[j], n=4, amp=0.06, cor=FC, w=2) for i, j in ((0, 1), (0, 2), (1, 2))])
    return g.add(*[bola(r, GEO).move_to(q) for q in ps])


RDA, HDA, SA = 1.35, 0.62, 0.5          # v7: o disco 3D do T7-8 (raio, espessura) em escala 0,5 — A3/A4
CAM_A = {"modo": "frente", "K": 1.0, "xc": -3.3, "yc": 1.0, "camx": -3.3, "camz": 0.0, "fov": 14, "el": 9}


def sprite(nome, w):
    """v7: miniatura 3D (assets_unidade/sprites, sprites_v7.py) com borda que some no fundo."""
    return ImageMobject(str(AQUI / "assets_unidade" / "sprites" / f"{nome}.png")).set_width(w)


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
        # o cavalo já está andando no primeiro quadro (sem entrada lenta); câmera lateral baixa
        cv = self.cv = Cavalo3D(self, v=lambda t: 0.42, K=1.1, xt=3.6, yc=-2.5, op=1.0)
        self.add(cv.f3d)
        pulso = ValueTracker(0.0)
        igual = ValueTracker(0.0)

        def setas():   # T⃗ na pedra (para a frente) e −T⃗ no balancim (para trás), mesmo comprimento, rótulos no vão
            k = cv.K.get_value()
            g = cv.setas_corda(FC, FC, L=0.95 * k, w=7 + 3 * pulso.get_value(), lab_a=r"-\vec T", lab_b=r"\vec T", size=34)
            if igual.get_value() > 0.01:   # |T⃗| = |−T⃗|: um "=" pequeno entre os dois rótulos
                g.add(mtex("=", WHITE_, 34).move_to((g[2].get_center() + g[3].get_center()) / 2).set_opacity(igual.get_value()))
            return g
        sg = always_redraw(setas)
        self.diz("numa corda ideal")
        self.play(FadeIn(sg), run_time=0.5)
        self.diz("com forças do mesmo tamanho")
        self.play(pulso.animate(rate_func=there_and_back).set_value(1.0), run_time=0.8)
        self.ate(0.97)
        # H2 — pulsam juntas; o "="; push-in lento até a corda; interrogação suave
        self.an("H2")
        q = always_redraw(lambda: mtxt("?", 80, bold=True, op=0.7).move_to(cv.pts()["topo"] + P3(0, 1.1)))
        self.play(pulso.animate(rate_func=there_and_back).set_value(1.0), igual.animate.set_value(1.0),
                  cv.K.animate(rate_func=rate_functions.ease_in_sine).set_value(1.2),
                  cv.xt.animate(rate_func=rate_functions.ease_in_sine).set_value(4.0), run_time=0.6)
        self.play(cv.K.animate(rate_func=linear).set_value(1.4), cv.xt.animate(rate_func=linear).set_value(5.1),
                  cv.yc.animate(rate_func=linear).set_value(-2.35), pulso.animate(rate_func=there_and_back).set_value(1.0),
                  run_time=self.resta() * 0.45)
        self.diz("como é que o cavalo anda")
        self.play(FadeIn(q), pulso.animate(rate_func=there_and_back).set_value(1.0), run_time=0.8)
        self.ate(0.97)
        # H3 — a câmera recua; o cavalo apaga para 40 %; a pergunta no centro
        self.an("H3")
        p1 = txt("SE A CORDA PUXA O CAVALO PARA TRÁS", 34, bold=True)
        p2 = txt("COM A MESMA FORÇA, COMO ELE ANDA?", 34, bold=True)
        per = VGroup(p1, p2).arrange(DOWN, buff=0.2).move_to(P3(0, 1.7))
        self.play(FadeOut(q), FadeOut(sg), cv.K.animate.set_value(0.82), cv.yc.animate.set_value(-2.3), cv.xt.animate.set_value(2.6),
                  run_time=1.4)
        self.play(FadeIn(per, shift=0.1 * UP), cv.f3d.op.animate.set_value(0.4), run_time=0.8)
        self.ate(0.97)
        self.f_hook = cv.f3d.f                # o último quadro do hook vira a miniatura do A2
        self.per = per

    # ── A1–A6 ─────────────────────────────────────────────────────────────────────────────────────────────
    def abertura(self):
        cv = self.cv
        self.an("A1")
        # o cavalo e a pergunta saem inteiros; depois o logo entra em fundo limpo
        self.virada(self.per, cv.f3d)
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        bv = txt("BEM-VINDOS AO PARALLAX LAB", 30, op=0.9).move_to(P3(0, -0.5))
        self.play(FadeIn(logo, scale=0.94), FadeIn(bv, shift=0.1 * UP), run_time=0.6)
        self.ate(0.97)
        self.a2(logo, bv)
        self.a3()
        self.a4()
        self.a5()
        self.a6()

    def a2(self, logo, bv):
        """Miniatura parada do último quadro do hook (zoom lento 1,00 → 1,05) com a pergunta embaixo; o título na CONTA."""
        self.an("A2")
        self.virada(logo, bv)
        arq = self.cv.f3d.dir / f"f{self.f_hook:05d}.png"
        W = 6.6
        if arq.exists() and not PEDIDOS3D:
            from PIL import Image
            im = ImageMobject(np.array(Image.open(arq).convert("RGBA"))).set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
        else:
            im = ImageMobject(np.full((54, 96, 4), (5, 8, 22, 255), dtype=np.uint8))
        im.set_width(W)
        moldura = Rectangle(width=W, height=W * 9 / 16).set_stroke(GEO, 1.5, opacity=0.7).set_fill(opacity=0)
        mini = Group(im, moldura).move_to(P3(-3.45, 0.55))
        c1 = txt("SE A CORDA PUXA O CAVALO PARA TRÁS COM A MESMA FORÇA,", 17, color=DIM)
        c2 = txt("COMO ELE ANDA?", 17, color=DIM)
        cap = VGroup(c1, c2).arrange(DOWN, buff=0.1).next_to(mini, DOWN, buff=0.22)
        tt = txt("MOMENTO EM SISTEMAS", 38, bold=True)
        s1 = txt("NESTE VÍDEO: O QUE MUDA", 24, color=DIM)
        s2 = txt("O MOMENTO DE VÁRIOS CORPOS", 24, color=DIM)
        bloco = VGroup(tt, s1, s2).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        if bloco.width > 6.6 - XC0:
            bloco.scale_to_fit_width(6.6 - XC0)
        na_conta(bloco, 0.5)
        self.play(FadeIn(mini), FadeIn(cap), FadeIn(tt, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(s1), FadeIn(s2), mini.animate.scale(1.03), run_time=0.9)
        t_q = self.ate_dizer("essa pergunta", mover=False)
        self.play(mini.animate.scale(1.08 / 1.03), run_time=max(0.5, t_q), rate_func=linear)     # v6: push-in lento até a pergunta
        self.diz("essa pergunta")
        self.play(Indicate(cap, color=WHITE_, scale_factor=1.06), mini.animate.scale(1.12 / 1.08), run_time=1.2)
        self.play(mini.animate.scale(1.15 / 1.12), run_time=max(0.5, self.resta() - 0.3), rate_func=linear)
        self.ate(0.97)
        self.a2_mobs = (mini, cap, bloco)

    def a3(self):
        """Um corpo: o disco do vídeo anterior; um empurrão (uma vez); curva F(t) com a área; F_res = dp/dt → J = ∫F dt = Δp."""
        self.an("A3")
        self.virada(*self.a2_mobs, cab="O VÍDEO ANTERIOR: UM CORPO")
        YM = 1.0
        self.dsc = []                                     # v7: os discos 3D (esferas.html, modo mesa de ar)

        def est(t):
            return {"luz": "lab", "esf": [], "molas": [], "piso": 1, "mesa": {"x": -3.35}, "discos": [dict(q) for q in self.dsc], "cam": CAM_A}
        self.f3a = Fundo3D(self, "esferas", est, op=0.0)
        self.f3a.conta.set_value(1.0)
        self.add(self.f3a)
        ms = self.f3a
        tag = txt("UM CORPO", 20, color=DIM).move_to(P3(-6.3, YM - 0.75))
        G = Graf(-6.6, -2.9, 5.6, 1.0, 0, 1.0, 1.6, rot_y=tex(r"F_{\text{res}}", FC, 30))

        t0 = self.clk.get_value()
        V0, V1 = 0.15, 0.3                    # lento: o disco não chega ao fim da mesa no bloco
        TA = self.ate_dizer("A força resultante")   # v5: o empurrão começa quando a voz diz "A força resultante…"
        TB = TA + 1.3

        def Fbump(u):
            return math.sin(PI * u) ** 2

        def v_de(s):
            if s < TA:
                return V0
            if s < TB:
                u = (s - TA) / (TB - TA)
                return V0 + (V1 - V0) * (u - math.sin(2 * PI * u) / (2 * PI))
            return V1

        def x_de(s):                         # integral fechada de v_de
            if s < TA:
                return -6.2 + V0 * s
            D = TB - TA
            u = min(1.0, (s - TA) / D)
            x = -6.2 + V0 * TA + V0 * u * D + (V1 - V0) * D * (u * u / 2 + (math.cos(2 * PI * u) - 1) / (4 * PI * PI))
            return x + (V1 * (s - TB) if s > TB else 0.0)

        def cena():
            s = self.clk.get_value() - t0
            x = x_de(s)
            self.dsc[:] = [{"x": x, "s": SA}]
            topo = proj3d(CAM_A, (x, RDA * SA, HDA * SA))
            esq = proj3d(CAM_A, (x - RDA * SA, -RDA * SA * 0.3, HDA * SA / 2))
            g = VGroup()
            v = v_de(s)
            pa = arrow(P3(x, topo[1] + 0.45), P3(x + 2.6 * v, topo[1] + 0.45), color=MAG, width=7, tip=0.18)
            g.add(pa, mtex(r"\vec p", MAG, 36).next_to(pa, UP, buff=0.08))
            if TA <= s < TB:
                u = (s - TA) / (TB - TA)
                fa = arrow(esq + P3(-1.0 - 0.3 * Fbump(u), 0), esq + P3(-0.05, 0), color=FC, width=7, tip=0.18)
                g.add(fa, mtex(r"\vec F_{\text{res}}", FC, 34).next_to(fa, UP, buff=0.12))
            # a curva F(t) e a área se desenham durante o empurrão (uma vez) e ficam
            uu = min(1.0, max(0.0, (s - TA) / (TB - TA)))
            if s >= TA:
                cur = G.curva(lambda q: Fbump(q), 0.0, max(uu, 1e-3), n=60, cor=FC, w=4)
                pts = [G.pt(q, Fbump(q)) for q in np.linspace(0, max(uu, 1e-3), 40)]
                ar_ = Polygon(G.pt(0, 0), *pts, G.pt(max(uu, 1e-3), 0)).set_stroke(width=0)     # v7 (2D+): área em degradê, curva com brilho
                ar_.set_fill(color=[escuro(JC, 0.7), JC], opacity=0.6).set_sheen_direction(UP)
                g.add(ar_, cur.copy().set_stroke(FC, 12, 0.14), cur)
                if uu > 0.6:
                    g.add(mtex(r"\vec J", JC, 36).move_to(G.pt(0.5, 0.35)))
            return g
        cn = always_redraw(cena)
        self.play(self.f3a.op.animate.set_value(1.0), FadeIn(tag), FadeIn(G.eixos), FadeIn(cn), run_time=0.3)
        while self.clk.get_value() - t0 < TA + 0.55:
            self.wait(1 / FPS)
        e1 = Mc((r"\vec F_{\text{res}}", FC), "=", (r"\frac{d\vec p}{dt}", MAG), size=56)
        na_conta(e1, 1.5)
        fl = [m for m in cn.submobjects if isinstance(m, MathTex) and r"F_{\text{res}}" in m.get_tex_string()]
        pl = [m for m in cn.submobjects if isinstance(m, MathTex) and m.get_tex_string() == r"\vec p"]
        self.play(FadeIn(e1, shift=0.1 * UP), run_time=0.9)                 # v6 (1.5): FadeIn, sem cópia voando
        self.diz("somando essa força")
        e2 = Mc((r"\vec J", JC), "=", r"\int", (r"\vec F_{\text{res}}", FC), r"\,dt", "=", (r"\Delta\vec p", MAG), size=56)
        na_conta(e2, -0.3)
        jl = [m for m in cn.submobjects if isinstance(m, MathTex) and m.get_tex_string() == r"\vec J"]
        area = Polygon(G.pt(0, 0), *[G.pt(q, math.sin(PI * q) ** 2) for q in np.linspace(0, 1, 40)], G.pt(1, 0)).set_stroke(JC, 4) \
            .set_fill(opacity=0)
        self.play(ShowPassingFlash(area.copy(), time_width=0.6), FadeIn(e2[:5], shift=0.1 * UP), run_time=1.1)   # realce da área
        self.diz("que é a variação do momento")
        self.play(FadeIn(e2[5]), FadeIn(e2[6], shift=0.1 * UP), Indicate(e1[2], color=WHITE_), run_time=0.8)   # v7 (1.1): sem glifo voando
        ar = txt("A ÁREA EMBAIXO DA CURVA", 20, color=JC).next_to(e2, DOWN, buff=0.3).align_to(e2, LEFT)
        self.diz("a área embaixo")
        self.play(FadeIn(ar), Indicate(e2[0], color=WHITE_), run_time=0.7)
        self.ate(0.97)
        self.cn, self.eq3, self.mesa, self.tag = cn, VGroup(e1, e2, ar, G.eixos), ms, tag

    def a4(self):
        """Dois corpos: os dois discos colidem uma vez; forças iguais e opostas no contato; Δp1 = −Δp2 → P constante."""
        self.an("A4")
        # a mesa continua (o mesmo objeto); o resto da cena do disco sai antes de os dois discos entrarem
        self.virada(self.cn, self.eq3, self.tag, cab="O VÍDEO ANTERIOR: DOIS CORPOS")
        YM = 1.0
        t0 = self.clk.get_value()
        V, R = 0.22, RDA * SA                     # v5: mais devagar — com a fala mais longa, os discos não saem do PALCO
        TC = self.ate_dizer("Durante o choque") + 0.35    # v5: o contato quando a voz diz "Durante o choque"
        DT = 0.35

        def cena():
            s = self.clk.get_value() - t0
            if s < TC:
                xa, xb, va, vb = -3.35 - R - V * (TC - s), -3.35 + R + V * (TC - s), V, -V
            elif s < TC + DT:
                u = (s - TC) / DT
                va, vb = V * (1 - 2 * u), -V * (1 - 2 * u)
                xa, xb = -3.35 - R + 0.06 * math.sin(PI * u), -3.35 + R - 0.06 * math.sin(PI * u)
            else:
                xa, xb, va, vb = -3.35 - R - V * (s - TC - DT), -3.35 + R + V * (s - TC - DT), -V, V
            self.dsc[:] = [{"x": xa, "s": SA}, {"x": xb, "s": SA}]     # v7: aço claro (1) e grafite (2), sem número escrito no corpo
            ya = proj3d(CAM_A, (xa, RDA * SA, HDA * SA))[1]
            g = VGroup()
            # setas em alturas diferentes e rótulos presos ao lado de fora de cada disco: no contato nada se encavala
            for x, v, nm, h, lado in ((xa, va, r"\vec p_1", 0.45, -1), (xb, vb, r"\vec p_2", 0.85, 1)):
                if abs(v) > 0.05:
                    a = arrow(P3(x, ya + h), P3(x + 1.6 * v, ya + h), color=MAG, width=7, tip=0.17)
                    g.add(a, mtex(nm, MAG, 32).move_to(P3(x + 0.62 * lado, ya + h + 0.05)))
            if TC - 0.05 <= s < TC + DT + 0.05:
                c = proj3d(CAM_A, ((xa + xb) / 2, -R * 0.4, 0.0))
                g.add(arrow(c + P3(-0.05, 0), c + P3(-1.3, 0), color=FC, width=7, tip=0.18, z=12).shift(DOWN * 0.45),
                      arrow(c + P3(0.05, 0), c + P3(1.3, 0), color=FC, width=7, tip=0.18, z=12).shift(DOWN * 0.45))
            return g
        cn = always_redraw(cena)
        lab = txt("DOIS CORPOS", 20, color=DIM).move_to(P3(-6.2, YM - 0.75))
        self.play(FadeIn(cn), FadeIn(lab), run_time=0.3)
        e1 = Mc((r"\Delta\vec p_1", MAG), "=", (r"-\Delta\vec p_2", MAG), size=60)
        na_conta(e1, 1.3)
        while self.clk.get_value() - t0 < TC + DT + 0.1:
            self.wait(1 / FPS)
        self.diz("o momento que um ganha")
        self.play(FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        e2 = linha(tex(r"\vec P", MAG, 60), mais(56, "="), txt("CONSTANTE", 34, bold=True), buff=0.25)
        na_conta(e2, -0.2)
        ds = txt("DOIS CORPOS SOZINHOS", 20, color=DIM).next_to(e2, DOWN, buff=0.28).align_to(e2, LEFT)
        seta = tex(r"\Downarrow", WHITE_, 46).move_to(P3(XC0 + 0.5, 0.55))
        self.diz("Dois corpos sozinhos")
        self.play(FadeIn(seta), FadeIn(e2, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(ds), run_time=0.5)
        self.ate(0.97)
        self.cn2, self.eq4, self.lab4 = cn, VGroup(e1, e2, ds, seta), lab

    def a5(self):
        """O cavalo volta (a mesma tomada contínua): fronteira só no cavalo → fronteira cresce (a corda vira interna)."""
        self.an("A5")
        self.virada(self.cn2, self.eq4, self.lab4, self.f3a, cab="A DIFERENÇA DE HOJE")
        self.remove(self.f3a)
        cv = self.cv
        cv.K.set_value(0.95); cv.xt.set_value(2.7); cv.yc.set_value(-2.55)
        cv.f3d.op.set_value(0.0)
        cv.f3d._quadro()
        self.add(cv.f3d)
        cresce = ValueTracker(0.0)
        cinza = ValueTracker(0.0)

        def front():
            p = cv.pts()
            u = cresce.get_value()
            xr = p["cabeca"][0] + 0.4
            xl_c = p["balancim"][0] - 0.3            # v5 (V1): a fronteira passa 0,3 atrás do balancim; a −T⃗ sai de dentro dela
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

        def forca():   # a −T⃗ do balancim (a mesma do hook): azul → cinza quando a corda vira interna
            k = cv.K.get_value()
            c = interpolate_color(ManimColor(FC), ManimColor(INT), cinza.get_value())
            l = mtex(r"-\vec T", FC, 32) if cinza.get_value() < 0.5 else mtxt("INTERNA", 18, color=INT)
            g = cv.setas_corda(c, c, L=0.95 * k, lab_a=l)
            if cinza.get_value() < 0.5:                  # v5 (V1): rótulo acima da parte da seta FORA da caixa, longe da linha
                xb = cv.corda()[0][0] - 0.3
                g[2].move_to(P3(xb - 0.18 - g[2].width / 2, g[2].get_center()[1]))
            return VGroup(g[0], g[2], g[3][0])           # só a do balancim (com o rótulo e o contorno)
        fc = always_redraw(forca)
        self.play(cv.f3d.op.animate.set_value(1.0), run_time=0.3)
        l1 = txt("UM CORPO: TODA FORÇA CONTA", 24).move_to(P3(0, Y_LEG + 0.05))
        self.diz("Repara na caixa tracejada")
        self.play(FadeIn(fr), run_time=0.6)
        self.diz("ela puxa o cavalo para trás")
        self.play(FadeIn(fc), run_time=0.5)
        self.diz("entra na força resultante")
        self.play(FadeIn(l1, shift=0.1 * UP), run_time=0.6)
        self.diz("Agora a caixa cresce")
        l2 = linha("SISTEMA: INTERNAS", tex(r"\times", WHITE_, 34), "EXTERNAS", size=24, buff=0.15)
        leg = VGroup(l1.copy(), tex(r"\to", WHITE_, 36), l2).arrange(RIGHT, buff=0.3).move_to(P3(0, Y_LEG + 0.05))
        self.play(cresce.animate.set_value(1.0), run_time=2.2)
        self.diz("uma força interna")
        self.play(cinza.animate.set_value(1.0), l1.animate.move_to(leg[0]), run_time=0.5)      # v7 (1.1): primeiro a frase sai do lugar,
        self.play(FadeIn(leg[1]), FadeIn(l2), run_time=0.5)                                    # depois entra a outra (sem letras cobertas)
        self.diz("Então a pergunta de hoje")
        qq = txt("?", 44, bold=True, color=MAG).move_to(P3(5.4, 1.6))
        self.play(FadeIn(qq, scale=0.7), run_time=0.5)
        self.ate(0.97)
        self.fr5, self.fc5, self.leg5 = fr, fc, VGroup(l1, leg[1], l2, qq)

    def a6(self):
        """Mapa dos dois vídeos no CENTRO, sem o cavalo; o '?' vai para o canto da CONTA."""
        self.an("A6")
        self.virada(self.fr5, self.fc5, self.leg5, self.cv.f3d, cab="ONDE A GENTE ESTÁ")
        XE, XD = -3.4, 3.4
        r1 = txt("VÍDEO ANTERIOR · UM CORPO", 24, color=DIM)
        i1 = sprite("disco", 2.6)                       # v7 (2,5D): miniaturas dos objetos 3D reais, com sombra
        q1 = Mc((r"\vec F_{\text{res}}", FC), "=", (r"\frac{d\vec p}{dt}", MAG), size=50)
        c1 = Group(r1, i1, q1).arrange(DOWN, buff=0.25).move_to(P3(XE, 0.3))
        ok = txt("RESOLVIDO", 18, color=DIM).next_to(c1, DOWN, buff=0.3)
        r2 = txt("HOJE · MUITOS CORPOS", 26, bold=True)
        i2 = sprite("esferas", 2.3)
        q = txt("?", 64, bold=True, color=MAG)
        c2 = Group(r2, i2, q).arrange(DOWN, buff=0.25).move_to(P3(XD, 0.3))
        sep = Line(P3(0, -1.6), P3(0, 2.2)).set_stroke(DIM, 1.5, opacity=0.4)
        seta = tex(r"\to", WHITE_, 60).move_to(P3(0, 0.3)).set_z_index(2)
        self.play(FadeIn(c1, shift=0.1 * UP), FadeIn(sep), run_time=0.6)
        self.diz("a gente já resolveu")
        self.play(*[m.animate.set_opacity(0.45) for m in c1], FadeIn(ok), run_time=0.6)
        self.diz("Hoje são muitos corpos")
        self.play(FadeIn(seta), FadeIn(r2, shift=0.1 * UP), FadeIn(i2), run_time=0.7)
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.diz("aquela interrogação no canto")
        self.play(q.animate.move_to(P3(7.0, 2.45)).scale(0.8), run_time=0.9)
        dd = sprite("dois", 2.7).move_to(i2.get_center())
        self.diz("um fato sobre dois discos")
        self.play(i2.animate.set_opacity(0.0), FadeIn(dd, scale=0.8), run_time=0.8)        # v6: os dois discos do A4…
        self.diz("vira uma ferramenta")
        self.play(FadeOut(dd, scale=0.6), i2.animate.set_opacity(1.0).scale(1.2), run_time=0.9)   # …viram as três esferas
        self.play(i2.animate.scale(1 / 1.2), run_time=0.6)
        self.ate(0.97)
