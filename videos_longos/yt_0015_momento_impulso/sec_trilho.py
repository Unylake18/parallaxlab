"""Lote PT3 (v6): T3 — POR QUE MASSA VEZES VELOCIDADE? refeito em Manim 2D, vista lateral e grande (handoff v6 §2).

Trilho de ar (viga de aço com furinhos, régua a cada 0,5, batentes), carrinhos em U invertido abraçando a viga (A/B no corpo,
massa embaixo; 2m e 3m = dois e três corpos com emenda), mola com trava na explosão, velcro laranja nas colisões que grudam,
setas violeta centradas no carrinho (v = 1,0 unidade), estroboscópio a cada 0,5 s, tela dividida no T3-3 (VISTA DO CHÃO ×
VISTA DE QUEM ANDA JUNTO COM A, com câmera de vídeo e régua que corre) e a conta que nasce dos rótulos no T3-4."""
from kit import *  # noqa: F401,F403

VIGA = "#7A8696"
ACO = "#B8C4DA"
SAIA = "#5E6878"
W1 = 1.4                       # comprimento de um corpo (massa m)
H1 = 0.62                      # altura do corpo
VU = 1.6                       # u/s de tela por "v" (escala 1)
DT_ESTRO = 0.5                 # estroboscópio
OKV = "#7BE0A8"                # ✓ (fecha) no T3-4
ERR = "#FF7A8A"                # ✗ (não fecha) e risco dos candidatos no T3-4


class Pista(VGroup):
    """Viga do trilho de ar entre x0 e x1, topo em yt. `off` (ValueTracker) desloca régua, furos e pés (o chão corre)."""

    def __init__(self, yt, esc=1.0, x0=-6.4, x1=6.4, off=None, batentes=True):
        super().__init__()
        self.yt, self.esc, self.x0, self.x1 = yt, esc, x0, x1
        self.off = off if off is not None else ValueTracker(0.0)      # (ValueTracker tem len 0: `or` o trocaria)
        e = esc
        hv = 0.42 * e
        viga = Rectangle(width=x1 - x0, height=hv).set_stroke(mix(VIGA, 0.25), 1.6).set_fill([mix(VIGA, 0.12), interpolate_color(
            ManimColor(VIGA), ManimColor(BACKGROUND_COLOR), 0.35)], 1).move_to(P3((x0 + x1) / 2, yt - hv / 2))
        viga.set_sheen_direction(DOWN)
        topo = Line(P3(x0, yt), P3(x1, yt)).set_stroke(mix(VIGA, 0.5), 2.2)
        self.add(viga, topo)
        self.topo = topo
        if batentes:
            for s in (-1, 1):
                xb = (x1 - 0.5 * e) if s > 0 else (x0 + 0.5 * e)
                b = RoundedRectangle(corner_radius=0.04, width=0.16 * e, height=0.42 * e).set_stroke(width=0).set_fill("#2B303B", 1)
                b.move_to(P3(xb + s * 0.08 * e, yt + 0.21 * e))
                self.add(b)
        self.xb = (x0 + 0.5 * e, x1 - 0.5 * e)          # faces internas dos batentes

        def marcas():
            g = VGroup()
            yt = self.topo.get_y()
            o = self.off.get_value()
            passo = 0.5
            k0 = math.floor((x0 + o) / passo) - 1
            for k in range(k0, k0 + int((x1 - x0) / passo) + 4):
                xr = k * passo - o
                if x0 + 0.06 < xr < x1 - 0.06:
                    longo = k % 2 == 0
                    g.add(Line(P3(xr, yt - 0.06 * e), P3(xr, yt - (0.2 if longo else 0.13) * e)).set_stroke(DIM, 2.0 if longo else 1.4, opacity=0.9))
                    g.add(Dot(P3(xr + passo / 2, yt - 0.3 * e), radius=0.024 * e, color=BACKGROUND_COLOR).set_opacity(0.9))
            for k in range(math.floor((x0 + o) / 3.0) - 1, math.floor((x1 + o) / 3.0) + 2):   # pés da viga (correm junto)
                xr = k * 3.0 + 1.5 - o
                if x0 + 0.3 < xr < x1 - 0.3:
                    g.add(Polygon(P3(xr - 0.16 * e, yt - hv), P3(xr + 0.16 * e, yt - hv), P3(xr + 0.08 * e, yt - hv - 0.22 * e),
                                  P3(xr - 0.08 * e, yt - hv - 0.22 * e)).set_stroke(mix(VIGA, 0.2), 1.2).set_fill("#2B303B", 1))
            return g.set_z_index(3)
        self.marcas = always_redraw(marcas)
        self.add(self.marcas)
        self.set_z_index(2)


class Carrinho(VGroup):
    """Deslizador do trilho de ar (vista lateral): corpo(s) em aço claro, saia escura abraçando a viga, bandeirola; letra no corpo e
    massa embaixo da viga (fora do carrinho). n = 1, 2, 3 corpos (m, 2m, 3m). `fx` → x do centro (updater próprio)."""

    def __init__(self, pista, n=1, letra="A", massa="m", camera=False):
        super().__init__()
        e = pista.esc
        self.pista, self.n, self.e = pista, n, e
        self.w = W1 * e * n
        yt = pista.yt
        corpo = VGroup()
        for k in range(n):
            r = RoundedRectangle(corner_radius=0.1 * e, width=W1 * e - 0.02, height=H1 * e).set_stroke(VIGA, 2.2) \
                .set_fill([mix(ACO, 0.25), ACO], 1)
            r.set_sheen_direction(DOWN)
            r.move_to(P3(-self.w / 2 + W1 * e * (k + 0.5), yt + 0.05 * e + H1 * e / 2))
            corpo.add(r)
        for k in range(1, n):                            # emenda entre corpos
            corpo.add(Line(P3(-self.w / 2 + W1 * e * k, yt + 0.1 * e), P3(-self.w / 2 + W1 * e * k, yt + H1 * e)).set_stroke(VIGA, 3))
        saia = Rectangle(width=self.w - 0.12 * e, height=0.24 * e).set_stroke(VIGA, 1.4).set_fill(SAIA, 1)
        saia.move_to(P3(0, yt - 0.07 * e))
        xm = -self.w / 2 + 0.3 * e
        mastro = Line(P3(xm, yt + 0.05 * e + H1 * e), P3(xm, yt + (0.05 + 0.4) * e + H1 * e)).set_stroke(GEO, 2)
        band = Polygon(P3(xm, yt + (0.45 - 0.0) * e + H1 * e), P3(xm + 0.26 * e, yt + 0.38 * e + H1 * e), P3(xm, yt + 0.31 * e + H1 * e)) \
            .set_stroke(width=0).set_fill(mix(VEL, 0.3), 1)
        self.corpo = corpo
        self.add(saia, corpo, mastro, band)
        if letra:
            L = txt(letra, 36, color=BACKGROUND_COLOR, bold=True).move_to(P3(0, yt + 0.05 * e + H1 * e / 2))
            self.add(L)
            self.letra = L
        self.lm = MathTex(massa, font_size=38, color=WHITE_).move_to(P3(0, yt - 0.42 * e - 0.47))     # abaixo dos pés da viga
        self.add(self.lm)
        self.vel_R = Rectangle(width=0.07 * e, height=0.34 * e).set_stroke(width=0).set_fill(HEAT, 1).move_to(
            P3(self.w / 2 + 0.035 * e, yt + 0.05 * e + H1 * e / 2)).set_opacity(0)
        self.vel_L = self.vel_R.copy().move_to(P3(-self.w / 2 - 0.035 * e, yt + 0.05 * e + H1 * e / 2))
        self.add(self.vel_R, self.vel_L)
        if camera:
            self.cam = camera_video(0.78 * e).move_to(P3(0.12 * e, yt + 0.05 * e + H1 * e + 0.2 * e))
        self.x = 0.0
        self.fx = lambda: self.x
        self.add_updater(lambda m: m._segue())
        self.set_z_index(6)

    def _segue(self):
        x = self.fx()
        self.shift(RIGHT * (x - self.x))
        self.x = x

    def em(self, x):
        self.shift(RIGHT * (x - self.x))
        self.x = x
        self.fx = lambda x=x: x
        return self

    def fantasma(self, x):
        g = VGroup(*[RoundedRectangle(corner_radius=0.1 * self.e, width=W1 * self.e - 0.02, height=H1 * self.e)
                     .set_stroke(ACO, 2.0, opacity=0.6).set_fill(ACO, 0.1)
                     .move_to(P3(x - self.w / 2 + W1 * self.e * (k + 0.5), self.pista.yt + 0.05 * self.e + H1 * self.e / 2))
                     for k in range(self.n)])
        return g


def camera_video(w):
    """Ícone de câmera de vídeo (corpo, lente para a frente, dois rolos)."""
    corpo = RoundedRectangle(corner_radius=0.05, width=w * 0.62, height=w * 0.36).set_stroke(WHITE_, 1.6).set_fill("#2B303B", 1)
    lente = Polygon(P3(w * 0.31, 0), P3(w * 0.5, w * 0.13), P3(w * 0.5, -w * 0.13)).set_stroke(WHITE_, 1.6).set_fill("#2B303B", 1)
    rolos = VGroup(*[Circle(radius=w * 0.11).set_stroke(WHITE_, 1.6).set_fill("#2B303B", 1).move_to(P3(s * w * 0.15, w * 0.29))
                     for s in (-1, 1)])
    luz = Dot(P3(-w * 0.2, w * 0.06), radius=w * 0.035, color=HEAT)
    return VGroup(rolos, corpo, lente, luz).set_z_index(9)


def mola(xa, xb, y, e, cor=GEO, n=8, amp=0.13):
    """Mola em zigue-zague entre xa e xb (altura y)."""
    pts = [P3(xa, y)]
    L = xb - xa
    for k in range(1, 2 * n):
        pts.append(P3(xa + L * k / (2 * n), y + (amp * e if k % 2 else -amp * e)))
    pts.append(P3(xb, y))
    return VMobject().set_points_as_corners(pts).set_stroke(cor, 3).set_z_index(7)


class LoteTrilho(Base):
    def construct(self):
        self.setup_base(cap="POR QUE MASSA VEZES VELOCIDADE?")
        self.t3_1()
        self.t3_2()
        self.t3_3()
        self.t3_4()
        self.t3_5()
        self.fim()
        self.relatorio()

    # ── setas de velocidade (violeta, centradas no carrinho, v = 1,0 unidade) e rótulos v = 0 ──────────────────────────
    def setas(self, pista, itens, fator=1.0):
        """itens() → [(carrinho_ou_par, v_em_unidades_de_v, rótulo)]; v = 0 escreve `v = 0` embaixo da massa."""
        e = pista.esc

        def f():
            g = VGroup()
            for c, v, r in itens():
                xc = c.get_center()[0] if not isinstance(c, (int, float)) else c
                ym = (c.lm.get_bottom()[1] if hasattr(c, "lm") else pista.yt - 0.42 * e - 0.6)
                if abs(v) > 1e-6:
                    L = abs(v) * 1.0 * e * fator
                    y = pista.yt + (0.05 + 0.62 + 0.62) * e
                    a, b = P3(xc - math.copysign(L / 2, v), y), P3(xc + math.copysign(L / 2, v), y)
                    g.add(arrow(a, b, color=VEL, width=7, tip=0.24, z=9))
                    if r:
                        g.add(rotulo(r, VEL, 40).next_to(P3(xc, y), UP, buff=0.16))
                elif r is not None:
                    g.add(rotulo(r"v = 0", DIM, 34).next_to(P3(xc, ym), DOWN, buff=0.18))
            return g
        return always_redraw(f)

    def estrobo(self, carros, inicio, tt, ate=None):
        """Fantasmas (opacidade 0,25) a cada 0,5 s de movimento: posição de cada carrinho em t = inicio + k·0,5."""
        def f():
            g = VGroup()
            t = tt.get_value() if ate is None else min(tt.get_value(), ate)
            k = 1
            while inicio + k * DT_ESTRO <= t + 1e-6:
                for c, fx in carros:
                    g.add(c.fantasma(fx(inicio + k * DT_ESTRO)))
                k += 1
            return g.set_z_index(5)
        return always_redraw(f)

    # ── T3-1 · explosão entre carrinhos iguais: a mola empurra os dois para fora ────────────────────────────────────────
    def t3_1(self):
        self.an("T3-1")
        yt = 0.62
        P = Pista(yt)
        self.P = P
        A = Carrinho(P, 1, "A", "m")
        B = Carrinho(P, 1, "B", "m")
        gap0 = 0.34
        xa0, xb0 = -(W1 + gap0) / 2, (W1 + gap0) / 2
        A.em(xa0)
        B.em(xb0)
        ym = yt + 0.05 + 0.31
        tt = ValueTracker(-10.0)
        x_stop = P.xb[1] - W1 / 2
        T = (x_stop - xb0) / VU

        def xb(t):
            return xb0 if t <= 0 else xb0 + VU * min(t, T)
        ent = ValueTracker(0.0)                          # v6: os dois deslizam das pontas até o centro e se encaixam na mola
        des = lambda: 4.0 * (1 - smooth(ent.get_value()))   # noqa: E731
        A.em(xa0 - 4.0)                                  # em() fixa a posição; a função de movimento vem depois
        B.em(xb0 + 4.0)
        A.fx = lambda: -xb(tt.get_value()) - des()
        B.fx = lambda: xb(tt.get_value()) + des()
        trava = Line(P3(xa0 + W1 / 2 - 0.02, ym + 0.2), P3(xb0 - W1 / 2 + 0.02, ym + 0.2)).set_stroke(WHITE_, 1.8).set_z_index(8)
        self.mola_on = True

        def fm():
            xa, xbb = A.get_right()[0], B.get_left()[0]
            op = 1.0 - min(1.0, max(0.0, (tt.get_value() - 0.45) / 0.3))     # a mola some em 0,3 s depois de esticar
            if xbb - xa > 1.0:
                return mola(-0.5, 0.5, ym, 1.0).set_stroke(opacity=op)
            return mola(xa, xbb, ym, 1.0).set_stroke(opacity=op)
        ml = always_redraw(fm)
        rv = self.setas(P, lambda: [(A, 0.0, ""), (B, 0.0, "")] if (tt.get_value() <= 0 and ent.get_value() >= 1) else [])
        sv = self.setas(P, lambda: [(A, -1.0, "v"), (B, 1.0, "v")] if 0 < tt.get_value() < T else [])
        cand = VGroup(*[MathTex(s, font_size=52) for s in (r"v\ ?", r"m\,v\ ?", r"m\,v^2\ ?")]).arrange(RIGHT, buff=1.4)
        cand[0].set_color(VEL)
        cand[1].set_color(MAG)
        centro(cand, -1.85)
        self.add(tt, ent)
        self.play(FadeIn(P), FadeIn(A), FadeIn(B), run_time=0.5)
        self.add(rv, sv)
        self.play(ent.animate.set_value(0.45), run_time=1.3, rate_func=linear)
        self.play(ent.animate.set_value(1.0), FadeIn(cand[0], scale=1.8), run_time=1.6, rate_func=linear)
        self.play(FadeIn(ml), Create(trava), run_time=0.5)
        for k, fr in enumerate((0.2, 0.33)):
            self.ate(fr)
            self.play(FadeIn(cand[k + 1], scale=1.8), Indicate(VGroup(A.corpo, B.corpo)[k], color=WHITE_, scale_factor=1.04), run_time=0.6)
        self.ate(0.44)
        cx = caixa(cand[1], MAG, buff=0.16)
        self.play(Indicate(cand[1], color=MAG, scale_factor=1.15), Create(cx), run_time=0.8)
        iguais = legenda("DOIS CARRINHOS IGUAIS · PARADOS", T_LAB, color=WHITE_)
        self.ate(0.53)
        self.play(FadeIn(iguais), Indicate(A.letra, color=HEAT, scale_factor=1.3), Indicate(B.letra, color=HEAT, scale_factor=1.3), run_time=0.8)
        self.wait(1.5)
        # trava queima (flash laranja 0,2 s), a mola estica e empurra: os dois andam no mesmo quadro
        fl = estouro(P3(0, ym + 0.2)).scale(0.55)
        tt.set_value(0.0)
        est = self.estrobo([(A, lambda t: -xb(t)), (B, lambda t: xb(t))], 0.0, tt)
        self.add(est)
        self.play(FadeIn(fl, scale=0.5), FadeOut(trava), tt.animate.set_value(0.2), run_time=0.2, rate_func=linear)
        sim = legenda("MESMO EMPURRÃO, MESMA VELOCIDADE", T_LAB, color=VEL)
        self.play(FadeOut(fl, scale=1.5), FadeOut(iguais), tt.animate.set_value(0.5), run_time=0.3, rate_func=linear)
        self.play(FadeIn(sim), tt.animate.set_value(0.8), run_time=0.3, rate_func=linear)
        self.remove(ml)
        self.play(tt.animate.set_value(T + 0.01), run_time=T - 0.8, rate_func=linear)
        # fantasmas espelhados acendem aos pares, do centro para fora (distâncias iguais = velocidades iguais)
        est.clear_updaters()
        pares = len(est) // 2
        for k in range(pares):
            self.play(*[x.animate.set_fill(opacity=0.35).set_stroke(opacity=1.0) for x in (est[2 * k], est[2 * k + 1])], run_time=0.25)
            self.play(*[x.animate.set_fill(opacity=0.1).set_stroke(opacity=0.6) for x in (est[2 * k], est[2 * k + 1])], run_time=0.2)
        self.ate(0.95)
        self.play(FadeOut(est), FadeOut(cand), FadeOut(cx), run_time=0.4)
        self.A, self.B, self.sim, self.rv, self.sv = A, B, sim, rv, sv

    # ── T3-2 · iguais, mesma velocidade, um contra o outro: grudam e PARAM ─────────────────────────────────────────
    def t3_2(self):
        self.an("T3-2")
        P, A, B = self.P, self.A, self.B
        self.remove(self.rv, self.sv)
        xs = B.x
        tt = ValueTracker(0.0)
        T = (xs - W1 / 2) / VU

        def xb(t):
            return xs - VU * min(max(t, 0), T)
        A.fx = lambda: -xb(tt.get_value())
        B.fx = lambda: xb(tt.get_value())
        sv = self.setas(P, lambda: [(A, 1.0, "v"), (B, -1.0, "v")] if tt.get_value() < T else [(A.get_center()[0] + W1 / 2, 0.0, "")])
        self.add(tt, sv)
        est = self.estrobo([(A, lambda t: -xb(t)), (B, lambda t: xb(t))], 0.0, tt, ate=T)
        self.add(est)
        self.play(A.vel_R.animate.set_opacity(1), B.vel_L.animate.set_opacity(1), FadeOut(self.sim), run_time=0.4)
        self.play(tt.animate.set_value(T), run_time=T, rate_func=linear)
        fl = flash(P3(0, P.yt + 0.36)).set_color(HEAT).set_z_index(12)
        para = legenda("IGUAIS E OPOSTOS: O CONJUNTO PARA", T_LAB, color=WHITE_)
        self.play(FadeIn(fl, scale=0.6), tt.animate.set_value(T + 0.3), run_time=0.3)
        self.play(FadeOut(fl), FadeIn(para), run_time=0.5)
        self.ate(0.72)
        self.play(FadeOut(est), run_time=0.4)
        # o velcro solta (traço) e os dois voltam às posições do T3-3, sem setas
        self.remove(sv)
        sol = Line(P3(0, P.yt + 0.12), P3(0, P.yt + 0.62)).set_stroke(HEAT, 4).set_z_index(12)
        x3 = 3.1
        self.play(Create(sol), run_time=0.25)
        A.em(A.x)
        B.em(B.x)
        self.play(FadeOut(sol), A.animate.shift(RIGHT * (-x3 - A.x)), B.animate.shift(RIGHT * (x3 - B.x)),
                  A.vel_R.animate.set_opacity(0), B.vel_L.animate.set_opacity(0), FadeOut(para), run_time=1.0)
        A.x, B.x = -x3, x3
        A.em(-x3)
        B.em(x3)

    # ── T3-3 · a mesma colisão vista do chão e de quem anda junto com A (câmera), ao mesmo tempo ───────────────────────────
    def t3_3(self):
        self.an("T3-3")
        P, A, B = self.P, self.A, self.B
        e = 0.8
        yc, yb = 1.55, -1.75                           # topo das vigas: faixa de cima e faixa de baixo
        x3 = 3.1
        # a cena grande vira a faixa de cima (VISTA DO CHÃO); a faixa de baixo entra (VISTA DE QUEM ANDA JUNTO COM A)
        P2 = Pista(yc, esc=e)
        A2 = Carrinho(P2, 1, "A", "m").em(-x3)
        B2 = Carrinho(P2, 1, "B", "m").em(x3)
        off = ValueTracker(0.0)
        Pb = Pista(yb, esc=e, off=off, batentes=False)
        wA = W1 * e
        Ab = Carrinho(Pb, 1, "A", "m", camera=True).em(-wA / 2)
        Bb = Carrinho(Pb, 1, "B", "m").em(-wA / 2 + 2 * x3)
        for c in (A2, B2, Ab, Bb):
            c.vel_R.set_opacity(1) if c in (A2, Ab) else c.vel_L.set_opacity(1)
        self.play(ReplacementTransform(P, P2), ReplacementTransform(A, A2), ReplacementTransform(B, B2), run_time=0.8)
        A2.em(-x3)
        B2.em(x3)
        r1 = txt("VISTA DO CHÃO", 21, color=DIM).move_to(P3(0, 0)).align_to(P3(-6.4, 0), LEFT).set_y(yc - 1.25)
        r2 = txt("VISTA DE QUEM ANDA JUNTO COM A", 21, color=DIM).move_to(P3(0, 0)).align_to(P3(-6.4, 0), LEFT).set_y(yb - 1.25)
        sep = DashedLine(P3(-6.4, (yc + yb) / 2 + 0.05), P3(6.4, (yc + yb) / 2 + 0.05), dash_length=0.12).set_stroke(DIM, 1.2, opacity=0.45)
        cam_c = camera_video(0.78 * e)                   # a câmera também aparece na faixa de cima, andando a +v com A
        u = VU * e
        tt = ValueTracker(0.0)
        tc = (2 * x3 - wA) / (2 * u)

        def gA(t):                                     # chão
            return -x3 + u * min(t, tc)

        def gB(t):
            return x3 - u * min(t, tc)
        A2.fx = lambda: gA(tt.get_value())
        B2.fx = lambda: gB(tt.get_value())
        cy_cam = yc + 0.05 * e + H1 * e + 0.2 * e
        cam_c.add_updater(lambda m: m.move_to(P3(-x3 + 0.12 * e + u * tt.get_value(), cy_cam)))
        # referencial de A (anda a +v): x' = x − u·t + (x3 − wA/2)
        c0 = x3 - wA / 2
        Ab.fx = lambda: gA(tt.get_value()) - u * tt.get_value() + c0
        Bb.fx = lambda: gB(tt.get_value()) - u * tt.get_value() + c0
        off.add_updater(lambda m: m.set_value(u * tt.get_value()))
        Ab.cam.move_to(P3(0.12 * e - wA / 2, yb + 0.05 * e + H1 * e + 0.2 * e))
        self.add(off)
        chao = VGroup(arrow(P3(5.9, yb - 0.95), P3(4.9, yb - 0.95), color=DIM, width=5, tip=0.2),
                      txt("CHÃO:", 21, color=DIM), MathTex("v", font_size=36, color=DIM))
        chao[1].next_to(chao[0], LEFT, buff=0.55)
        chao[2].next_to(chao[1], RIGHT, buff=0.1)
        chao[0].next_to(chao[2], RIGHT, buff=0.15)
        chao.move_to(P3(4.9, yb - 1.25))

        t_lento = 0.45

        def itens_c(tt_=None):
            t = (tt_ or tt).get_value()
            if t < tc:
                return [(A2, 1.0, "v"), (B2, -1.0, "v")]
            return [(A2.get_right()[0], 0.0, "")] if t > tc + t_lento + 0.4 else []

        def itens_b():
            t = tt.get_value()
            if t < tc:
                return [(Ab, 0.0, ""), (Bb, -2.0, "2v")]
            return [((Ab.get_center()[0] + Bb.get_center()[0]) / 2, -1.0, "v")] if t > tc + t_lento + 0.4 else []
        sc, sb = self.setas(P2, itens_c), self.setas(Pb, itens_b)
        self.add(tt)
        self.play(FadeIn(Pb), FadeIn(Ab), FadeIn(Bb), FadeIn(r1), FadeIn(r2), Create(sep), run_time=0.7)
        self.add(sc, sb)
        self.play(FadeIn(Ab.cam, shift=0.15 * DOWN), FadeIn(cam_c, shift=0.15 * DOWN), FadeIn(chao), run_time=0.6)
        Ab.cam.add_updater(lambda m: m.move_to(P3(0.12 * e - wA / 2, yb + 0.05 * e + H1 * e + 0.2 * e)))
        self.ate(0.12)
        # corrida 1: normal até perto do contato, câmera lenta (0,5×) no contato, normal depois
        self.play(tt.animate.set_value(tc - t_lento), run_time=tc - t_lento, rate_func=linear)
        lig = DashedLine(P3(0, yc + 0.7), P3(0, yb + 0.05), dash_length=0.1).set_stroke(WHITE_, 1.6, opacity=0.7).set_z_index(1)
        lento = txt("CÂMERA LENTA", 21, color=DIM).move_to(P3(5.2, (yc + yb) / 2 + 0.3))
        self.play(FadeIn(lento), tt.animate.set_value(tc), run_time=2 * t_lento, rate_func=linear)
        fl = VGroup(flash(P3(0, yc + 0.36)).scale(0.8), flash(P3(0, yb + 0.36)).scale(0.8)).set_color(HEAT).set_z_index(12)
        self.play(FadeIn(fl), Create(lig), tt.animate.set_value(tc + 0.25), run_time=1.0, rate_func=linear)
        self.play(FadeOut(fl), FadeOut(lento), tt.animate.set_value(tc + t_lento), run_time=2 * (t_lento - 0.25), rate_func=linear)
        self.play(FadeOut(lig), tt.animate.set_value(tc + t_lento + 0.4), run_time=0.4, rate_func=linear)
        tarja = legenda("MESMA COLISÃO · OUTRO REFERENCIAL", T_LAB, color=WHITE_)
        t_fim = tc + min(3.6, (6.2 - wA) / u - 0.25)
        self.play(FadeIn(tarja), tt.animate.set_value(tc + t_lento + 0.9), run_time=0.5, rate_func=linear)
        self.play(tt.animate.set_value(t_fim), run_time=t_fim - (tc + t_lento + 0.9), rate_func=linear)
        # repetição (sem trilho vazio: o par novo acende enquanto o antigo apaga)
        resto = (self.alvo - self.nq) / FPS - 0.3
        if resto > tc + 1.0:
            velhos = [A2, B2, Ab, Bb, cam_c, Ab.cam]
            for c in velhos:
                c.clear_updaters()
            self.remove(sc, sb)
            tt2 = ValueTracker(0.0)
            A2, B2 = Carrinho(P2, 1, "A", "m").em(-x3), Carrinho(P2, 1, "B", "m").em(x3)
            Ab, Bb = Carrinho(Pb, 1, "A", "m", camera=True).em(-wA / 2), Carrinho(Pb, 1, "B", "m").em(-wA / 2 + 2 * x3)
            A2.vel_R.set_opacity(1)
            Ab.vel_R.set_opacity(1)
            B2.vel_L.set_opacity(1)
            Bb.vel_L.set_opacity(1)
            Ab.cam.move_to(P3(0.12 * e - wA / 2, yb + 0.05 * e + H1 * e + 0.2 * e))
            cam_c = camera_video(0.78 * e).move_to(P3(-x3 + 0.12 * e, cy_cam))
            self.play(*[FadeOut(c) for c in velhos], *[FadeIn(c) for c in (A2, B2, Ab, Bb, cam_c, Ab.cam)], run_time=0.5)
            A2.fx = lambda: gA(tt2.get_value())
            B2.fx = lambda: gB(tt2.get_value())
            Ab.fx = lambda: gA(tt2.get_value()) - u * tt2.get_value() + c0
            Bb.fx = lambda: gB(tt2.get_value()) - u * tt2.get_value() + c0
            cam_c.add_updater(lambda m: m.move_to(P3(-x3 + 0.12 * e + u * tt2.get_value(), cy_cam)))
            Ab.cam.add_updater(lambda m: m.move_to(P3(0.12 * e - wA / 2, yb + 0.05 * e + H1 * e + 0.2 * e)))
            off.clear_updaters()
            o0 = off.get_value()
            off.add_updater(lambda m: m.set_value(o0 + u * tt2.get_value()))

            def ib():
                return [(Ab, 0.0, ""), (Bb, -2.0, "2v")] if tt2.get_value() < tc else [((Ab.get_center()[0] + Bb.get_center()[0]) / 2, -1.0, "v")]
            sc, sb = self.setas(P2, lambda: itens_c(tt2)), self.setas(Pb, ib)
            self.add(tt2, sc, sb)
            dur_ = min(t_fim, resto - 0.5)
            self.play(tt2.animate.set_value(dur_), run_time=dur_, rate_func=linear)
            tt = tt2
        self.ate(0.99)
        self.P2, self.Pb, self.A2, self.B2, self.Ab, self.Bb = P2, Pb, A2, B2, Ab, Bb
        self.cam_c, self.r1, self.r2, self.sep, self.chao, self.tarja, self.sc, self.sb = cam_c, r1, r2, sep, chao, tarja, sc, sb
        self.off, self.tt3 = off, tt

    # ── T3-4 · a faixa de cima sai; a colisão 2v → 0 e a conta nasce dos rótulos; testes de v² e de v sozinha (sincronia) ─────
    def t3_4(self):
        self.an("T3-4")
        e = 0.8
        yt4 = 1.55                                     # faixa 12%–45% da altura
        for c in (self.A2, self.B2, self.cam_c, self.Ab, self.Bb, self.off, self.Ab.cam):
            c.clear_updaters()
        self.remove(self.sc, self.sb)
        cam_b = self.Ab.cam
        Pb = self.Pb
        # a faixa de cima sai; a de baixo sobe (a régua para de correr: daqui em diante é o trilho parado)
        dy = yt4 - Pb.yt
        self.play(FadeOut(VGroup(self.P2, self.A2, self.B2, self.cam_c, self.r1, self.sep, self.tarja)), run_time=0.4)
        self.play(VGroup(Pb, self.Ab, self.Bb, cam_b).animate.shift(UP * dy), FadeOut(self.r2), FadeOut(self.chao), run_time=0.7)
        Pb.yt = yt4
        P4 = Pb
        u4 = 1.3 * e
        casos = [
            dict(nA=1, nB=1, mA="m", mB="m", va=0.0, vb=-2.0, lv=("", "2v"), tex=["m", r"\cdot", "2v", "+", "m", r"\cdot", "0", r"\;=\;", "2m", r"\cdot", "v"],
                 ia=(4, 6), ib=(0, 2), idep=(8, 10), mf="2m", vf=-1.0, lvf="v", xa=-1.6),
            dict(nA=1, nB=2, mA="m", mB="2m", va=2.0, vb=-1.0, lv=("2v", "v"),
                 tex=["m", r"\cdot", "2v", "+", "2m", r"\cdot", "(-", "v", ")", r"\;=\;", "3m", r"\cdot", "0"],
                 ia=(0, 2), ib=(4, 7), idep=(10, 12), mf="3m", vf=0.0, lvf="", xa=-2.6),
            dict(nA=2, nB=3, mA="2m", mB="3m", va=3.0, vb=-2.0, lv=("3v", "2v"),
                 tex=["2m", r"\cdot", "3v", "+", "3m", r"\cdot", "(-", "2v", ")", r"\;=\;", "5m", r"\cdot", "0"],
                 ia=(0, 2), ib=(4, 7), idep=(10, 12), mf="5m", vf=0.0, lvf="", xa=-3.4),
        ]
        # candidatos do T3-1 voltam pequenos no canto (abaixo da marca d'água, acima dos carrinhos)
        # (revisão: coluna à direita, abaixo do trilho — no alto encostava nos rótulos de velocidade dos carrinhos)
        cand = VGroup(*[MathTex(s, font_size=36) for s in (r"v\ ?", r"m\,v\ ?", r"m\,v^2\ ?")]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        cand[0].set_color(VEL)
        cand[1].set_color(MAG)
        cand.move_to(P3(0, -0.45)).align_to(P3(6.5, 0), RIGHT)
        sai_teste = []

        def marca(ok, alvo):
            m = MathTex(r"\checkmark" if ok else r"\times", font_size=56, color=OKV if ok else ERR)
            return m.next_to(alvo, RIGHT, buff=0.35)

        hist = []
        yeq = -0.6                                     # a conta nova nasce logo embaixo do trilho; o histórico desce (os voos não cruzam nada)
        ant, sv_ant = [self.Ab, self.Bb, cam_b], None
        for k, cs in enumerate(casos):
            A = Carrinho(P4, cs["nA"], "A", cs["mA"])
            B = Carrinho(P4, cs["nB"], "B", cs["mB"])
            wa, wb = A.w, B.w
            xa0 = cs["xa"]
            xb0 = min(6.2 - wb / 2, xa0 + (wa + wb) / 2 + 4.0)          # faces a 4,0 de distância (ou o fim do trilho)
            tc = (xb0 - xa0 - (wa + wb) / 2) / ((cs["va"] - cs["vb"]) * u4)
            tt = ValueTracker(0.0)

            def xs(t, xa0=xa0, xb0=xb0, cs=cs, tc=tc):
                if t < tc:
                    return xa0 + cs["va"] * u4 * t, xb0 + cs["vb"] * u4 * t
                xa, xb = xa0 + cs["va"] * u4 * tc, xb0 + cs["vb"] * u4 * tc
                return xa + cs["vf"] * u4 * (t - tc), xb + cs["vf"] * u4 * (t - tc)
            A.em(xa0)
            B.em(xb0)
            A.vel_R.set_opacity(1)
            B.vel_L.set_opacity(1)

            def itens(A=A, B=B, cs=cs, tt=tt, tc=tc):
                if tt.get_value() < tc:
                    return [(A, cs["va"], cs["lv"][0]), (B, cs["vb"], cs["lv"][1])]
                return [((A.get_left()[0] + B.get_right()[0]) / 2, cs["vf"], cs["lvf"])]
            sv = self.setas(P4, itens)
            if k == 1:
                self.ate(0.45)                           # "E a velocidade sozinha…": o caso m × 2m entra com o teste de v
            # o par novo acende enquanto o antigo apaga (o trilho nunca fica vazio)
            if sv_ant is not None:
                self.remove(sv_ant)
            for m in ant:
                m.clear_updaters()
            movs = []
            for j, h in enumerate(hist[::-1]):          # histórico: a conta anterior sobe e encolhe (no máximo 2 linhas)
                movs.append(h.animate.scale(0.7 if j == 0 else 1.0).set_y(yeq - 1.0 - 0.66 * j))
            self.play(*[FadeOut(m) for m in ant + sai_teste], FadeIn(A), FadeIn(B), *movs, run_time=0.45)
            sai_teste = []
            self.add(tt, sv)
            A.fx = lambda xs=xs, tt=tt: xs(tt.get_value())[0]
            B.fx = lambda xs=xs, tt=tt: xs(tt.get_value())[1]
            if k == 0:
                # a colisão nova roda uma vez enquanto a fala a descreve; em "olha a conta" ela rebobina e a conta nasce dos rótulos
                self.play(tt.animate(rate_func=linear).set_value(tc + 1.4), run_time=tc + 1.4)
                self.ate(0.12)
                self.play(tt.animate.set_value(0.0), run_time=0.7)
            if k == 1:
                vt = MathTex(r"2v", "+", r"(-v)", r"\;=\;", "v", r"\;\neq\;", "0", font_size=60)
                for i in (0, 2, 4, 6):
                    vt[i].set_color(VEL)
                centro(vt, yeq)
                xv = marca(False, vt)
                self.play(Write(vt), tt.animate(rate_func=linear).set_value(min(tc, 0.8)), run_time=0.9)
                rv = risco(cand[0], cor=ERR)
                self.play(FadeIn(xv, scale=1.4), Create(rv), tt.animate(rate_func=linear).set_value(min(tc, 1.2)), run_time=0.6)
                self.ate(0.5)                            # "olha os outros casos": só agora as contas com momento
                self.play(FadeOut(vt), FadeOut(xv), tt.animate.set_value(0.0), run_time=0.5)
            eq = MathTex(*cs["tex"], font_size=60)
            for i, s in enumerate(cs["tex"]):
                eq[i].set_color(VEL if ("v" in s or (s == "0")) else WHITE_)
            centro(eq, yeq)
            # massa e velocidade de cada carrinho voam do desenho para a conta, com os carrinhos já andando
            self.update_mobjects(0)
            labs = self.mobjects_rotulos(sv)
            voa = []
            for c, (im, iv) in ((A, cs["ia"]), (B, cs["ib"])):
                voa.append(ReplacementTransform(fixa(c.lm), eq[im]))
                lv = labs.get(id(c))
                if lv is not None:
                    src = fixa(lv[0][-1]) if lv.get_tex_string().startswith("v =") else fixa(lv)
                    voa.append(ReplacementTransform(src, eq[iv]))
                else:
                    voa.append(FadeIn(eq[iv]))
            ops = [eq[i] for i in range(len(cs["tex"])) if i not in (*cs["ia"], *cs["ib"]) and i < cs["idep"][0] - 1]
            t1 = min(tc, 0.8)
            self.play(*voa, tt.animate(rate_func=linear).set_value(t1), run_time=0.8)
            t2 = min(tc, t1 + 0.5)
            self.play(*[FadeIn(o) for o in ops], tt.animate(rate_func=linear).set_value(t2), run_time=0.5)
            if tc > t2:
                self.play(tt.animate(rate_func=linear).set_value(tc), run_time=tc - t2)
            fl = flash((A.get_right() + B.get_left()) / 2).set_color(HEAT).scale(0.8).set_z_index(12)
            par_m = MathTex(cs["mf"], font_size=38, color=WHITE_)
            par_m.add_updater(lambda m, A=A, B=B: m.move_to(P3((A.get_left()[0] + B.get_right()[0]) / 2, A.lm.get_y())))
            self.play(FadeIn(fl, scale=0.6), tt.animate(rate_func=linear).set_value(tc + 0.25), run_time=0.25)
            self.play(FadeOut(fl), A.lm.animate.set_opacity(0), B.lm.animate.set_opacity(0), FadeIn(par_m),
                      tt.animate(rate_func=linear).set_value(tc + 0.7), run_time=0.45)
            self.update_mobjects(0)
            src_v = None
            for x in sv.submobjects:
                if isinstance(x, MathTex):
                    src_v = fixa(x[0][-1]) if x.get_tex_string().startswith("v =") else fixa(x)
            dep = [ReplacementTransform(fixa(par_m), eq[cs["idep"][0]]), FadeIn(eq[cs["idep"][0] + 1]), FadeIn(eq[cs["idep"][0] - 1])]
            dep.append(ReplacementTransform(src_v, eq[cs["idep"][1]]) if src_v is not None else FadeIn(eq[cs["idep"][1]]))
            self.play(*dep, tt.animate(rate_func=linear).set_value(tc + 1.5), run_time=0.8)
            self.consolida(eq)
            if k == 0:
                self.ate(0.22)                           # "Fecha certinho"
            ok = marca(True, eq)
            self.play(Indicate(eq[cs["idep"][0] - 1], color=WHITE_, scale_factor=1.4), FadeIn(ok, scale=1.4),
                      tt.animate(rate_func=linear).set_value(tc + 2.0), run_time=0.5)
            self.remove(ok)
            eq.add(ok)                                   # o ✓ anda com a conta no histórico
            hist.append(eq)
            if len(hist) > 3:
                self.play(FadeOut(hist.pop(0)), run_time=0.3)
            ant, sv_ant = [A, B, par_m], sv
            if k == 0:
                # teste da massa vezes a velocidade ao quadrado, com os rótulos do trilho (2v e 0 antes; 2m e v depois)
                self.ate(0.3)
                q1 = MathTex("m", r"(2v)^2", "+", "m", r"\cdot 0^2", r"\;=\;", r"4\,m v^2", font_size=46)
                q2 = MathTex("2m", r"\cdot", "v^2", r"\;=\;", r"2\,m v^2", font_size=46)
                q1[1].set_color(VEL)
                q1[4].set_color(VEL)
                q2[2].set_color(VEL)
                VGroup(q1, q2).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(P3(0.6, yeq - 1.45))
                la = txt("ANTES", T_SMALL, color=GEO).next_to(q1, LEFT, buff=0.35)
                lb = txt("DEPOIS", T_SMALL, color=GEO).next_to(q2, LEFT, buff=0.35).align_to(la, RIGHT)
                self.play(FadeIn(cand, shift=0.1 * DOWN), FadeIn(la), Write(q1), run_time=1.2)
                self.ate(0.36)                           # "depois, só duas vezes"
                self.play(FadeIn(lb), Write(q2), run_time=0.9)
                self.ate(0.42)                           # "Não fecha"
                nf = MathTex(r"4\neq 2", font_size=50).next_to(VGroup(q1, q2), RIGHT, buff=0.6)
                xq = marca(False, nf)
                rq = risco(cand[2], cor=ERR)
                self.play(FadeIn(nf), FadeIn(xq, scale=1.4), Create(rq), run_time=0.7)
                sai_teste = [la, lb, q1, q2, nf, xq]             # as contas de teste saem junto com a entrada do caso seguinte
        fecha = legenda("ANTES = DEPOIS, SEMPRE", T_LAB, color=WHITE_)
        self.ate(0.8)                                    # "Antes igual a depois, sempre"
        self.play(FadeIn(fecha), run_time=0.5)
        self.ate(0.86)                                   # "Isso não é uma demonstração…": entre os candidatos, m v
        bxc = caixa(cand[1], MAG, buff=0.12)
        self.play(Indicate(cand[1], color=MAG, scale_factor=1.3), Create(bxc), run_time=0.9)
        self.ate(0.97)
        self.hist, self.fecha, self.ant4, self.P4 = hist, fecha, ant + [sv_ant, cand, bxc, rv, rq], P4

    def mobjects_rotulos(self, sv):
        """Rótulos atuais do desenho das setas, por carrinho mais próximo: {id(carrinho): rótulo}."""
        out = {}
        g = sv
        cs = [m for m in self.mobjects if isinstance(m, Carrinho)]
        for x in g.submobjects:
            if isinstance(x, MathTex):
                if not cs:
                    continue
                c = min(cs, key=lambda c: abs(c.get_center()[0] - x.get_center()[0]))
                out[id(c)] = x
        return out

    # ── T3-5 · a mesma grandeza por dois caminhos: segunda lei e simetria ─────────────────────────────────────────
    def t3_5(self):
        self.an("T3-5")
        for m in self.ant4:
            m.clear_updaters()
        self.play(FadeOut(VGroup(*self.ant4, self.P4, self.fecha)), run_time=0.4)
        self.play(VGroup(*self.hist).animate.scale(0.8).arrange(DOWN, buff=0.35).move_to(P3(3.7, 0.9)), run_time=0.6)
        # PALCO: o carrinho A com v⃗ e p⃗ (no lugar do bloco do v5)
        Pp = Pista(-0.9, esc=1.0, x0=-6.4, x1=0.4, batentes=False)
        A = Carrinho(Pp, 1, "A", "m").em(-3.6)
        top = Pp.yt + 0.05 + H1 + 0.62
        v = arrow(P3(-3.6 - 1.0, top), P3(-3.6 + 1.0, top), color=VEL, width=8, tip=0.26)
        p = arrow(P3(-3.6 - 1.4, top + 0.85), P3(-3.6 + 1.4, top + 0.85), color=MAG, width=9, tip=0.28)
        lv = rotulo(r"\vec v", VEL, 44).next_to(v, RIGHT, buff=0.15)
        lp = rotulo(r"\vec p", MAG, 44).next_to(p, RIGHT, buff=0.15)
        self.play(FadeIn(Pp), FadeIn(A, shift=0.3 * RIGHT), GrowArrow(v), FadeIn(lv), run_time=0.7)
        self.play(GrowArrow(p), FadeIn(lp), run_time=0.6)
        s1 = self.selo("DA SEGUNDA LEI", WHITE_).move_to(P3(-3.2, 2.35))
        s2 = self.selo("DA SIMETRIA", GEO).move_to(P3(3.7, 2.35))
        alvo = MathTex(r"\vec p", "=", "m", r"\vec v", font_size=M_MAIN)
        alvo[0].set_color(MAG)
        alvo[3].set_color(VEL)
        centro(alvo, -2.55)
        bx = caixa(alvo, MAG, buff=0.22)
        self.play(FadeIn(s1, shift=0.1 * DOWN), FadeIn(s2, shift=0.1 * DOWN), run_time=0.6)
        self.ate(0.4)
        # os dois selos convergem para UM p⃗ = m v⃗ (nenhuma cópia sobra)
        self.play(s1.animate.scale(0.6).move_to(alvo.get_center() + LEFT * 0.4).set_opacity(0),
                  s2.animate.scale(0.6).move_to(alvo.get_center() + RIGHT * 0.4).set_opacity(0),
                  FadeIn(alvo, scale=0.8), run_time=1.0)
        self.remove(s1, s2)
        self.play(Create(bx), run_time=0.5)
        nome = txt("MOMENTO LINEAR", T_MAIN, color=MAG, bold=True).next_to(bx, RIGHT, buff=0.4)
        self.ate(0.75)
        self.play(FadeIn(nome, shift=0.1 * LEFT), Indicate(VGroup(p, v), color=WHITE_, scale_factor=1.05), run_time=0.8)
        self.ate(0.97)

    def selo(self, s, cor):
        t = txt(s, T_LAB, color=cor, bold=True)
        r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.6, height=t.height + 0.38).set_stroke(cor, 2).set_fill(opacity=0)
        r.moldura = True
        t.move_to(r)
        return VGroup(r, t)


def estouro(c, cor=HEAT):
    """Explosão pequena: anel laranja, raios e miolo claro."""
    g = VGroup(Circle(radius=0.16).set_stroke(width=0).set_fill(mix(cor, 0.6), 0.95).move_to(c),
               Circle(radius=0.32).set_stroke(cor, 4).move_to(c))
    for k in range(10):
        a = k * TAU / 10 + 0.15
        g.add(Line(c + 0.38 * P3(math.cos(a), math.sin(a)), c + 0.7 * P3(math.cos(a), math.sin(a))).set_stroke(cor, 4))
    return g.set_z_index(20)
