"""Lote PB3 · A DOBRA (B3-1…B3-6), layout B (quadro 12): φ(u, v) = (u, u² + v²). Retas v = 1, 2 viram parábolas empilhadas; v = −1 cai sobre a de v = 1;
u = 1 vira a semirreta x = 1, y ≥ 1 percorrida duas vezes; a dobra em duas etapas, (u, v) ↦ (u, |v|) e depois (u, w) ↦ (u, u² + w²); a linha da dobra vira a parábola y = x²;
Im φ = {y ≥ x²} em chapa; pré-imagens de três pontos. Tudo dentro dos painéis (entrada 110 px/u; saída 52 px/u)."""
from v7 import *  # noqa: F401,F403


class LoteB3(Base):
    def corpo(self):
        # ── B3-1 ──
        self.an("B3-1")
        self.secao("A DOBRA")
        ax_e = Vista(440, 530, 110)
        ax_s = Vista(1480, 770, 52)
        pe, ps = painel(130, 250, 620, 560, "ENTRADA", E1), painel(1170, 250, 620, 560, "SAÍDA", SAI)
        arco = arco7(780, 520, 1150, 520, r"\varphi")
        dom = chapa7([ax_e.c2p(*p) for p in ((-2.3, -2.3), (2.3, -2.3), (2.3, 2.3), (-2.3, 2.3))])
        ex_e = eixos7(ax_e, -2.3, 2.3, -2.3, 2.0, alpha=0.5, rx=("u", E1), ry=("v", E2))
        ex_s = eixos7(ax_s, -3.2, 3.2, -0.3, 9.0, alpha=0.5, rx=("x", SAI), ry=("y", SAI))
        self.play(FadeIn(pe), FadeIn(ps), FadeIn(dom), Create(ex_e), Create(ex_s), FadeIn(arco), run_time=1.4)
        form = TC(r"\varphi(\U,\V) = \S{(}\U,\; \U^2+\V^2\S{)}", 440, 920, 48, "c")
        self.gat("uma função que repete")
        self.play(caneta(form))
        mapa = lambda p: ax_s.c2p(*(lambda c: (c[0], c[0] ** 2 + c[1] ** 2))(ax_e.p2c(p)))

        # ── B3-2 · v = k vira y = x² + k² ──
        self.an("B3-2")
        linha = lambda v, cor=E2, w=W_CURVA: Line(ax_e.c2p(-2.3, v), ax_e.c2p(2.3, v)).insert_n_curves(60).set_stroke(cor, w)
        l1, l2 = linha(1), linha(2)
        self.gat("fixa a segunda entrada em um")
        self.play(Create(l1), run_time=0.9)
        self.gat("a parábola padrão levantada")
        p1 = l1.copy()
        self.play(ApplyPointwiseFunction(mapa, p1), run_time=2.2)
        self.gat("com a segunda entrada fixa em dois")
        self.play(Create(l2), run_time=0.9)
        p2 = l2.copy()
        self.play(ApplyPointwiseFunction(mapa, p2), run_time=2.2)
        fk = TC(r"\V = \V_0 \Rightarrow \Y = \X^2 + \V_0^2", 1480, 920, 44, "c")
        self.gat("cada reta horizontal vira uma parábola")
        self.play(caneta(fk))

        # ── B3-3 · v = −1 cai sobre a parábola de v = 1 ──
        self.an("B3-3")
        lm = linha(-1)
        self.gat("a reta em que ela vale menos um")
        self.play(Create(lm), run_time=0.9)
        self.gat("vai parar na mesma parábola")
        pm = lm.copy()
        self.play(ApplyPointwiseFunction(mapa, pm), run_time=2.2)
        self.gat("duas retas diferentes")
        leg = legenda("v = 1 E v = −1 CAEM NA MESMA PARÁBOLA", 960, 1010, WHITE_, "center")
        self.play(pulso(VGroup(l1, lm), 1.0, 1.7), pulso(VGroup(p1, pm), 1.0, 1.7), FadeIn(leg), run_time=1.2)
        rv1 = TC(r"\V=1", ax_e.cx + 1.35 * ax_e.u, ax_e.cy - 1.3 * ax_e.u, 30, "l", caneta=False)
        rv2 = TC(r"\V=-1", ax_e.cx + 1.2 * ax_e.u, ax_e.cy + 0.7 * ax_e.u, 30, "l", caneta=False)
        self.play(FadeIn(rv1), FadeIn(rv2), run_time=0.4)

        # ── B3-4 · u = 1 vira a semirreta x = 1, y ≥ 1, percorrida duas vezes ──
        self.an("B3-4")
        lu1 = Line(ax_e.c2p(1, -2.3), ax_e.c2p(1, 2.3)).set_stroke(E1, W_CURVA)
        vt = ValueTracker(-2.0)
        de = ponto(ORIGIN, GEO, 0.09, z=7).add_updater(lambda d: d.move_to(ax_e.c2p(1, vt.get_value())))
        ds = ponto(ORIGIN, SAI, 0.1, z=7).add_updater(lambda d: d.move_to(ax_s.c2p(1, 1 + vt.get_value() ** 2)))
        self.gat("fixa a primeira entrada em um")
        self.play(Create(lu1), run_time=0.8)
        self.gat("enquanto a segunda entrada vem dos negativos")
        self.add(vt)
        self.play(FadeIn(de), FadeIn(ds), run_time=0.4)
        semi = Line(ax_s.c2p(1, 5), ax_s.c2p(1, 1)).set_stroke(E1, W_CURVA)
        self.play(vt.animate.set_value(0.0), Create(semi), rate_func=linear, run_time=3.6)
        self.gat("quando ela passa de zero")
        self.play(vt.animate.set_value(2.0), rate_func=linear, run_time=3.6)
        self.gat("a reta inteira vira uma semirreta")
        self.play(pulso(semi, 1.0, 1.7), run_time=1.0)
        de.clear_updaters()
        ds.clear_updaters()

        # ── B3-5 · a dobra: dobra + estica ──
        self.an("B3-5")
        self.play(FadeOut(VGroup(l1, l2, lm, p1, p2, pm, lu1, de, ds, semi, fk, leg, rv1, rv2)), run_time=0.5)
        self.remove(l1, l2, lm, p1, p2, pm, lu1, de, ds, semi, fk, vt, leg, rv1, rv2)

        def meia(sinal):
            r = chapa(Polygon(*[ax_e.c2p(*p) for p in ((-2.3, 0), (2.3, 0), (2.3, 2 * sinal), (-2.3, 2 * sinal))]))
            r.insert_n_curves(120)
            vs = VGroup(*[linha(sinal * v, E2, W_FAM) for v in (1, 2)])
            us = VGroup(*[Line(ax_e.c2p(u, 0), ax_e.c2p(u, 2 * sinal)).insert_n_curves(40).set_stroke(E1, W_FAM) for u in (-1, 1)])
            return contorno(VGroup(r, vs, us))
        cima, baixo = meia(1), meia(-1)
        dobra = contorno(linha(0, FORTE, W_IMG)).set_z_index(5)
        self.play(FadeIn(cima), FadeIn(baixo), Create(dobra), FadeOut(dom), run_time=1.0)
        y0 = ax_e.c2p(0, 0)[1]
        baixo0 = baixo.copy()

        def vira(m, a):
            c = math.cos(PI * a)
            m.become(baixo0.copy().apply_function(lambda p: np.array([p[0], y0 + (p[1] - y0) * c, 0.0])))
        self.gat("primeiro dobra o plano ao meio")
        self.play(UpdateFromAlphaFunc(baixo, vira), run_time=2.6)
        self.gat("depois estica essa meia-folha")
        meia_f = VGroup(cima, baixo, dobra)
        img = meia_f.copy()
        self.play(ApplyPointwiseFunction(mapa, img), run_time=2.6)
        pr = [(x, x * x) for x in np.linspace(-3, 3, 91)]
        regiao = VMobject().set_points_as_corners([ax_s.c2p(*p) for p in pr] + [ax_s.c2p(3, 9.4), ax_s.c2p(-3, 9.4)])
        regiao.set_stroke(width=0).set_fill(SAI, 0.22).set_z_index(-1)
        borda = contorno(ParametricFunction(lambda x: ax_s.c2p(x, x * x), t_range=[-3, 3]).set_stroke(FORTE, W_IMG)).set_z_index(5)
        self.gat("e a linha da dobra")
        self.play(pulso(dobra, 1.0, 1.8), pulso(img[2], 1.0, 1.8), run_time=1.2)
        self.gat("a imagem é tudo o que está")
        fim_ = TC(r"\S{\operatorname{Im}\varphi = \{(x,y) \mid y \ge x^2\}}", 1480, 920, 44, "c")
        cf = caneta(fim_)
        w = self.falta("e nada abaixo")                      # o flash do "nada abaixo" entra na palavra, durante a caneta
        rt = max(cf.tot, w + 0.7)
        self.play(FadeIn(regiao), FadeIn(borda), img[0][0].animate.set_opacity(0), img[1][0].animate.set_opacity(0), cf,
                  Succession(Wait(w), Flash(ax_s.c2p(1.6, 1.2), color=DIM, line_length=0.14, flash_radius=0.18, run_time=0.7), Wait(max(0.01, rt - w - 0.7))),
                  run_time=rt)
        print(f"[gatilho] B3-5 agendado no play: 'e nada abaixo' em {w:.2f}s depois do início da caneta (atraso 0,00 s)")

        # ── B3-6 · quem chega num ponto de saída? ──
        self.an("B3-6")
        self.play(FadeOut(VGroup(cima, baixo, dobra)), FadeOut(form), FadeIn(dom), run_time=0.5)
        self.remove(cima, baixo, dobra, form)
        Pa, Pb, Pc = (0.0, 3.0), (1.0, 1.0), (-1.6, 1.2)
        ds_ = VGroup(*[ponto(ax_s.c2p(*p), SAI_F, 0.09, z=8) for p in (Pa, Pb, Pc)])
        self.gat("pega um ponto do plano de saída")
        self.play(FadeIn(ds_, scale=0.5), run_time=0.6)
        pre = TC(r"\U = \S{x_0},\quad \V^2 = \S{y_0 - x_0^2}", 440, 920, 44, "c")
        self.gat("a primeira entrada tem que ser")
        self.play(caneta(pre))

        def chega(uv, alvo):
            a = ax_e.c2p(*uv)
            return VGroup(ponto(a, GEO, 0.08, z=8), voo(a + 0.1 * RIGHT, ax_s.c2p(*alvo) + 0.12 * LEFT, angle=-0.45, w=2.4, tip=0.15).set_z_index(7))
        r3 = math.sqrt(3.0)
        self.gat("acima da parábola")
        dois = VGroup(chega((0, r3), Pa), chega((0, -r3), Pa))
        pa = placa("2 CHEGAM", SAI_F).move_to(ax_s.c2p(*Pa) + P3(0.9, 0.4))
        self.play(LaggedStart(*[Create(m) for m in dois], lag_ratio=0.3), run_time=1.6)
        self.play(FadeIn(pa, shift=0.08 * UP), run_time=0.3)
        self.gat("na parábola ela é zero")
        um = chega((1, 0), Pb)
        pb = placa("1 CHEGA", SAI_F).move_to(ax_s.c2p(*Pb) + P3(0.95, -0.4))
        self.play(Create(um), run_time=1.2)
        self.play(FadeIn(pb, shift=0.08 * UP), run_time=0.3)
        self.gat("e abaixo ela é negativa")
        xis = contorno(Cross(scale_factor=0.11, stroke_color=DEST, stroke_width=4.5)).move_to(ax_s.c2p(*Pc) + P3(-0.3, 0.28)).set_z_index(8)
        pn = placa("NINGUÉM", DEST).move_to(ax_s.c2p(*Pc) + P3(-0.75, -0.42))
        self.play(FadeIn(xis), FadeIn(pn, shift=0.08 * UP), pulso(ds_[2], 1.4, 1.0), run_time=0.8)
        self.sai_fim()
