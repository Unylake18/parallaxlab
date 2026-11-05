"""Lote PT1: T1 — como medir um giro? Disco de referência 2D (DiscoRef: um ValueTracker θ gira tudo), CONTA à direita em Pilha.
T1-1 régua tracejada entre os pontos de 1/3 e 3/3 que não muda quando o disco gira (auditoria RÍGIDO no qa20.py). T1-2 θ âmbar a partir da linha fixa.
T1-3 para o mesmo θ = 1,0 rad, arcos s ∝ r nos três raios; θ = s/r; uma volta: s = 2πr. T1-4 s = rθ (θ em rad), π/180 SOBRA, DICA.
T1-5 sinais; três voltas: mostrador 0°–360° (zera) × Δθ acumulado (mostrador = Δθ mod 2π, mesma variável).

v2 (handoff §4: S3 S4 D5–D10; §5: T1-3, T1-4, T1-5): rótulos fora do disco, chamada EIXO FIXO sem linha que cruza o corpo, pontos maiores,
arcos desenhados pelo movimento, contas escritas em ordem (voos do desenho, passo/GlyphMap, TransformMatchingTex)."""
from pecas20 import *  # noqa: F401,F403

R_FIS = 30.0                   # cm: raio físico do disco de referência (só para a régua do T1-1: 1/3 → 3/3 = 20 cm)
ROT0 = -0.3                    # ângulo inicial da linha pintada no T1-1 (a régua e seu rótulo ficam dentro da zona do ESQUEMA)


def num2(s, cor, size=46):
    """num_mob com folga maior entre os glifos (o ENCOSTADO do G28 olha dígitos vizinhos)."""
    g = num_mob(s, cor, size)
    g.arrange(RIGHT, buff=0.07 * size / 40, aligned_edge=DOWN)
    for m_, ch in zip(g, s):
        if ch == "°":
            m_.shift(0.16 * size / 40 * UP)
        if ch in ",.":
            m_.shift(0.05 * size / 40 * DOWN)
    return g


def cartao_p(*linhas, size=30, cor=BLUE_L, px=0.3, py=0.24):
    """cartao() com padding maior (G1: selo em duas linhas com respiro)."""
    t = VGroup(*[txt(l, size) for l in linhas]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    r = RoundedRectangle(corner_radius=0.12, width=t.width + 2 * px, height=t.height + 2 * py).move_to(t).set_fill(PANEL, 0.9).set_stroke(cor, 2)
    r._fundo = True
    return VGroup(r, t).set_z_index(20)


class LoteT1(L20):

    def construct(self):
        self.setup_base()
        self.t1()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    # ── ângulo θ fora do disco: raio da linha pintada prolongado, arco âmbar por fora e (opcional) rótulo ──
    def th_fora(self, d, o, rot_=True):
        C, R = d.C, d.R
        th = d.th.get_value()
        u, _ = d.u(th)
        g = VGroup(tracej(C + R * u, C + (R + 0.8) * u, GEO, 2.2, 0.7 * o, 0.1, z=4),
                   tracej(C + (R + 0.55) * RIGHT, C + (R + 0.8) * RIGHT, GEO, 2.2, 0.7 * o, 0.1, z=4),
                   arco(C, R + 0.8, 0.0, th, ANG, 8, o, z=8))
        if rot_ and o > 0.01:
            la = lbl(r"\theta", ANG, 46)
            am = th / 2
            la.move_to(C + (R + 1.2) * P3(math.cos(am), math.sin(am)))
            g.add(escala_op(la, o))
        return g

    def t1(self):
        d = DiscoRef(self, th0=ROT0)
        self.add(d.g)
        C, R = d.C, d.R
        # ── T1-1: corpo rígido ──
        self.an("T1-1")
        self.secao("COMO MEDIR UM GIRO?")
        # S4: anel no PINO (centro) e o selo EIXO FIXO logo abaixo do disco, nascendo junto do anel; sem linha-guia (qualquer linha até o pino cruzaria o disco)
        anel = Circle(radius=0.2).move_to(C).set_stroke(WHITE_, 3).set_fill(opacity=0).set_z_index(10)
        ef = selo_mini("EIXO FIXO", cor=WHITE_, borda=BLUE_L, size=24)
        ef.move_to(C + P3(0, -(R + 0.12 + ef.height / 2)))
        cart = cartao_p("CORPO RÍGIDO:", "DISTÂNCIAS FIXAS", size=30)          # v3 §11: o selo desde o primeiro quadro (coluna nunca vazia)
        self.pilha.poe(cart, dx=0.1)
        self.play(FadeIn(anel), FadeIn(ef), FadeIn(cart, shift=0.1 * UP), run_time=0.6)
        op_r = ValueTracker(0.0)
        self.add(op_r)

        def regua():
            o = op_r.get_value()
            if o < 0.01:
                return VGroup()
            th = d.th.get_value()
            u, n = d.u(th)
            a, b = d.p(1, th) + 0.3 * n, d.p(3, th) + 0.3 * n
            g = VGroup(tracej(a, b, GEO, 3, o, 0.1, z=9), Line(a - 0.1 * n, a + 0.1 * n).set_stroke(GEO, 3, opacity=o).set_z_index(9),
                       Line(b - 0.1 * n, b + 0.1 * n).set_stroke(GEO, 3, opacity=o).set_z_index(9))
            lab = mtex(r"20\ \mathrm{cm}", GEO, 38)
            lab.move_to(b + u * (0.45 + 0.5 * abs(u[0]) * lab.width + 0.5 * abs(u[1]) * lab.height) + 0.0 * n)
            if lab.get_right()[0] > 0.1:                  # CALHA (x 0,2…0,7): o rótulo para antes dela
                lab.shift((0.1 - lab.get_right()[0]) * RIGHT)
            if not PEDIDOS3D:
                self.reg("regua", d=float(np.linalg.norm(b - a)), th=th)
            return VGroup(g, escala_op(lab, o)).set_z_index(9)
        rg = vivo(regua)
        self.add(rg)
        # v3 §11: a cota 20 cm nasce na primeira fala e o disco já gira devagar (sentido horário: o rótulo não cruza a linha de referência)
        T_ = max(1.0, self.resta() - 0.3 - 0.7)
        GIRO = -0.75
        self.play(op_r.animate.set_value(1.0), d.th.animate(rate_func=linear).set_value(ROT0 + GIRO * 0.7 / (0.7 + T_)), run_time=0.7)
        self.play(d.th.animate(rate_func=linear).set_value(ROT0 + GIRO), run_time=T_)
        self.ate(0.99)
        # ── T1-2: um número descreve o corpo todo ──
        self.an("T1-2")
        self.play(op_r.animate.set_value(0.0), FadeOut(cart), FadeOut(anel), FadeOut(ef), run_time=0.4)
        self.pilha.tira(cart)
        self.remove(rg, cart, anel, ef)
        th_ini = d.th.get_value()
        op_c, op_t = ValueTracker(0.0), ValueTracker(0.0)
        self.add(op_c, op_t)

        def rastros():
            th = d.th.get_value()
            g = VGroup()
            if op_c.get_value() > 0.01:
                for k in (1, 2, 3):
                    g.add(arco(C, R * k / 3, th_ini, th, GEO, 4.5, 0.9 * op_c.get_value(), z=5))
            o = op_t.get_value()
            if o > 0.01:
                g.add(self.th_fora(d, o))
            return g
        rv = vivo(rastros)
        self.add(rv)
        self.gat("repara no que acontece quando ele gira")
        self.play(op_c.animate.set_value(1.0), d.th.animate(rate_func=linear).set_value(th_ini + 1.0), run_time=2.4)
        self.gat("cada ponto anda num círculo centrado no eixo")
        c1 = cartao("CADA PONTO:", "UM CÍRCULO", size=30)
        self.pilha.poe(c1, dx=0.1)
        self.play(FadeIn(c1, shift=0.1 * UP), d.th.animate(rate_func=linear).set_value(th_ini + 2.6), run_time=self.ate_t("e todos os pontos juntos"))
        self.gat("e todos os pontos juntos")
        c2 = cartao("TODOS OS PONTOS:", "MESMO ÂNGULO", size=30)
        self.pilha.limpa(rt=0.3)
        self.pilha.poe(c2, dx=0.1)
        self.play(FadeIn(c2, shift=0.1 * UP), d.th.animate(rate_func=smooth).set_value(th_ini + 3.4), run_time=1.6)
        self.gat("basta um número só")
        self.play(op_c.animate.set_value(0.45), d.th.animate(rate_func=smooth).set_value(0.9), run_time=1.6)
        self.gat("o ângulo entre essa linha pintada")
        self.play(op_t.animate.set_value(1.0), Indicate(d.ref, color=WHITE_, scale_factor=1.0), Indicate(c2, color=WHITE_, scale_factor=1.06), run_time=0.9)
        self.gat("na tela ele aparece como teta")
        th_lab = lbl(r"\theta", ANG, 56)
        self.gat("um corpo rígido girando em torno de um eixo fixo")
        fr = VGroup(txt("UM NÚMERO DESCREVE", 34, bold=True), VGroup(txt("O CORPO TODO:", 34, bold=True), th_lab).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        self.pilha.limpa(rt=0.3)
        self.pilha.poe(fr)
        self.play(FadeIn(fr, shift=0.1 * UP), run_time=0.7)
        self.play(d.th.animate(rate_func=there_and_back).set_value(1.0), run_time=2.0)
        self.foco = fr
        self.ate(0.99)
        # ── T1-3: radiano ──
        self.an("T1-3")
        self.pilha.limpa(rt=0.35)
        self.play(op_t.animate.set_value(0.0), op_c.animate.set_value(0.0), d.th.animate(rate_func=linear).set_value(0.0), run_time=1.0)
        self.remove(rv)
        TH = 1.0
        # D5: pontos ≥ 0,12 u por cima dos pontos do disco
        def pontos_g():
            th = d.th.get_value()
            return VGroup(*[Circle(radius=0.13).set_fill(WHITE_, 1).set_stroke("#2A3550", 2.2).move_to(d.p(k, th)) for k in (1, 2, 3)]).set_z_index(11)
        pg = vivo(pontos_g)
        self.add(pg)
        op_t3 = ValueTracker(0.0)
        self.add(op_t3)

        def arcos():
            th = d.th.get_value()
            g = VGroup()
            for k in (1, 2, 3):
                g.add(arco(C, R * k / 3, 0.0, th, ANG, 8 if k == 3 else 7, 1.0, z=8))
            o = op_t3.get_value()
            if o > 0.01:
                g.add(self.th_fora(d, o, rot_=False))
            if not PEDIDOS3D:
                self.reg("arcos", th=th, s=[R * k / 3 * th for k in (1, 2, 3)], r=[R * k / 3 for k in (1, 2, 3)])
            return g
        av_ = vivo(arcos)
        self.add(av_)
        self.gat("a gente mede em radianos")
        card = cartao_p("ÂNGULO EM RADIANOS:", "ARCO ÷ RAIO", size=30)
        self.pilha.poe(card, dx=0.2)
        self.play(FadeIn(card, shift=0.1 * UP), run_time=0.6)
        self.gat("pega o comprimento do arco")
        self.play(d.th.animate(rate_func=smooth).set_value(TH), op_t3.animate.set_value(1.0), run_time=1.6)
        ls = lbl("s", ANG, 46).move_to(C + (R + 0.32) * P3(math.cos(TH / 2), math.sin(TH / 2)))
        lth = lbl(r"\theta", ANG, 46).move_to(C + (R + 1.2) * P3(math.cos(TH / 2), math.sin(TH / 2)))
        rr = Line(C, C + R * RIGHT).set_stroke(GEO, 4).set_z_index(7)
        lr = lbl("r", GEO_, 46).move_to(C + P3(R + 0.3, -0.45))              # S3: fora do disco e abaixo da linha de referência
        self.play(FadeIn(ls), FadeIn(lth), Create(rr), FadeIn(lr), run_time=0.7)
        self.gat("e divide pela distância dele ao eixo")
        A, ia = eqf([r"\theta", "="], ["s"], ["r"], size=60, cores={("pre", 0): ANG, ("num", 0): ANG, ("den", 0): GEO_})
        self.pilha.poe(A)
        # D6/§5: θ, s e r voam do desenho; "=" e a barra são escritos na vaga
        self.voa([(lth, gl(A, ia["pre"][0])), (ls, gl(A, ia["num"][0])), (lr, gl(A, ia["den"][0]))],
                 extra=[FadeIn(gl(A, ia["pre"][1] + ia["bar"]))], rt=1.4)
        self.gat("olha os três pontos")
        B, ib = M(r"\frac{s_1}{r_1}", "=", r"\frac{s_2}{r_2}", "=", r"\frac{s_3}{r_3}", "=", r"1{,}0\ \mathrm{rad}", size=50, cores={6: ANG})
        for k in (0, 2, 4):
            js = ib[k]
            for j in js[:2]:
                B[0][j].set_color(ANG)
            for j in js[3:]:
                B[0][j].set_color(GEO_)
        self.pilha.buff = 0.5                                      # v3 §11: folga ≥ 0,25 u entre θ = s/r e s₁/r₁ = …
        self.pilha.poe(B, dx=0.15)
        self.pilha.buff = 0.26
        self.play(*[Indicate(m, color=WHITE_, scale_factor=1.0) for m in av_.submobjects[:3]], run_time=0.8)
        self.gat("a divisão dá o mesmo número")
        self.play(FadeIn(B, shift=0.1 * UP), run_time=0.9)
        self.gat("esse número é o ângulo em radianos")
        self.play(Indicate(A, color=WHITE_, scale_factor=1.06), run_time=0.8)
        self.gat("e uma volta inteira")
        self.play(FadeOut(ls), FadeOut(lth), FadeOut(lr), FadeOut(rr), op_t3.animate.set_value(0.0), run_time=0.3)
        A = self.pilha.so(A, rt=2.0, anims=[d.th.animate(rate_func=smooth).set_value(2 * PI)])[0]
        # θ = s/r → θ = 2πr/r (GM: o s vira 2πr) → risco nos dois r → θ = 2π
        C1, ic1 = eqf([r"\theta", "="], [r"2\pi", "r"], ["r"], size=56, cores={("pre", 0): ANG, ("num", 0): ANG, ("num", 1): GEO_, ("den", 0): GEO_})
        self.pilha.poe(C1)
        self.passo(A, C1, (ia["pre"][0], ic1["pre"][0]), (ia["pre"][1], ic1["pre"][1]), (ia["num"][0], J(ic1["num"], 0, 1)),
                   (ia["bar"], ic1["bar"]), (ia["den"][0], ic1["den"][0]), rt=1.0)
        k1 = Line(*[gl(C1, ic1["num"][1]).get_corner(p) for p in (DL, UR)]).set_stroke(WHITE_, 3).set_z_index(30)
        k2 = Line(*[gl(C1, ic1["den"][0]).get_corner(p) for p in (DL, UR)]).set_stroke(WHITE_, 3).set_z_index(30)
        k1._risco = k2._risco = True
        self.play(Create(k1), Create(k2), run_time=0.4)
        Cq, ic = M(r"\theta", "=", r"2\pi", size=56, cores={0: ANG, 2: ANG})
        self.pilha.poe(Cq)
        self.passo(C1, Cq, (ic1["pre"][0], ic[0]), (ic1["pre"][1], ic[1]), (ic1["num"][0], ic[2]),
                   (J(ic1["num"], 1) + ic1["bar"] + ic1["den"][0], []), rt=0.9, extra=[FadeOut(k1), FadeOut(k2)])
        Dq = linha_m(txt("1 VOLTA:", 32, bold=True), M(r"2\pi", r"\ \mathrm{rad}", size=56, cores={0: ANG, 1: ANG})[0], buff=0.2)
        Db = caixa_l(Dq, ANG)
        self.pilha.poe(Db)
        self.play(FadeIn(Db), run_time=0.5)
        self.gat("dois pi radianos")
        self.foco = Db
        self.ate(0.99)
        # ── T1-4: s = r θ, θ em rad ──
        self.an("T1-4")
        self.remove(card)
        self.play(d.th.animate(rate_func=linear).set_value(TH + 2 * PI), run_time=0.8)
        A_ = self.pilha.so(A)[0]
        S, is_ = M("s", "=", "r", r"\theta", size=60, cores={0: ANG, 2: GEO_, 3: ANG})
        self.pilha.poe(S)
        self.gat("o radiano é uma divisão de comprimento")
        self.play(Indicate(gl(A_, ia["num"][0] + ia["den"][0]), color=WHITE_), run_time=0.8)
        self.gat("por isso a relação")
        # GM: o r atravessa o "=" (sai do denominador e pousa à esquerda do θ)
        self.passo(A_, S, (ia["pre"][0], J(is_, 3)), (ia["pre"][1], J(is_, 1)), (ia["num"][0], J(is_, 0)), (ia["bar"], []), (ia["den"][0], J(is_, 2)), rt=1.3)
        th_n = VGroup(txt("(", 28), lbl(r"\theta", ANG, 40), txt("EM", 28), lbl(r"\mathrm{rad})", WHITE_, 40)).arrange(RIGHT, buff=0.1)
        self.pilha.poe(th_n)
        self.play(FadeIn(th_n), run_time=0.5)
        self.gat("se você medir em graus")
        S = self.pilha.so(S, rt=0.5)[0]
        lg = txt("EM GRAUS:", 28)
        self.pilha.poe(lg)
        G_, ig = M("s", "=", "r", r"\theta", r"\cdot", r"\frac{\pi}{180}", size=52, cores={0: ANG, 2: GEO_, 3: ANG})
        self.pilha.poe(G_)
        self.play(FadeIn(lg), run_time=0.4)
        # TMT/GM de s = rθ → s = rθ · π/180: os quatro glifos viajam, o fator π/180 é escrito e destacado
        self.passo(S, G_, (J(is_, 0), J(ig, 0)), (J(is_, 1), J(ig, 1)), (J(is_, 2), J(ig, 2)), (J(is_, 3), J(ig, 3)), rt=1.2)
        self.ind(G_, ig, [4, 5], color=WHITE_, f=1.1, rt=0.7)
        sob = mp(G_, ig, [5])                                      # v3 §11: a caixa só no fator π/180
        bx = SurroundingRectangle(sob, buff=0.12, color=BLUE_L, stroke_width=3)
        bx._fundo = True
        sb = selo_mini("SOBRA", cor=WHITE_, borda=BLUE_L)
        self.pilha.buff = 0.12 + 0.3
        self.pilha.poe(sb, dx=max(0.0, bx.get_center()[0] - sb.width / 2 - self.pilha.x0))
        self.pilha.buff = 0.26
        ptr = Line(sb.get_top(), bx.get_bottom()).set_stroke(BLUE_L, 3).set_z_index(29)
        bxg = VGroup(bx, ptr)                                      # caixa + linha-guia curta selo→fator: um grupo de fundo (não é objeto do QA)
        bxg._fundo = True
        self.play(FadeIn(bxg), FadeIn(sb), run_time=0.6)
        self.gat("é por isso que toda a rotação")
        self.dica18("EM ROTAÇÃO, ÂNGULO SEMPRE EM RADIANOS")
        self.ate(0.99)
        # ── T1-5: sinais; mostrador × acumulado ──
        self.an("T1-5")
        self.pilha.limpa(rt=0.35, anims=[FadeOut(bxg), FadeOut(av_), FadeOut(pg)])
        self.remove(av_, pg)
        self.foco = None
        # S5: o sinal fica DENTRO do giro da seta (centro), longe das pontas; as palavras, embaixo
        sc_p, sc_m = P3(2.3, 1.45), P3(5.1, 1.45)
        sp = seta_curva(sc_p, 0.7, -0.6, 4.6, ANG, 7)
        sm = seta_curva(sc_m, 0.7, PI + 0.6, -4.6, ANG, 7)
        sg_p, sg_m = lbl("+", WHITE_, 56).move_to(sc_p), lbl("-", WHITE_, 56).move_to(sc_m)
        lp_ = txt("ANTI-HORÁRIO", 26).next_to(sc_p + 0.7 * DOWN, DOWN, buff=0.3)
        lm_ = txt("HORÁRIO", 26).next_to(sc_m + 0.7 * DOWN, DOWN, buff=0.3)
        self.gat("o sentido anti horário é positivo")
        self.play(FadeIn(sp), FadeIn(sg_p), FadeIn(lp_), run_time=0.6)
        self.gat("horário é negativo")
        self.play(FadeIn(sm), FadeIn(sg_m), FadeIn(lm_), run_time=0.6)
        self.gat("o ângulo que a gente usa não volta a zero")
        # D9: o disco volta à referência (θ = 0) e o contador parte de Δθ = 0: mostrador = Δθ mod 2π em todo quadro
        th0 = 2 * PI * round(d.th.get_value() / (2 * PI))      # mesma pose de θ = 0 pelo caminho curto (417° → 360°): sem aliasing de 115°/quadro
        self.play(FadeOut(VGroup(sp, sm, sg_p, sg_m, lp_, lm_)), d.th.animate(rate_func=smooth).set_value(th0), run_time=0.6)
        mc = P3(1.95, 0.95)
        t_m = txt("MOSTRADOR", 26).move_to(mc + P3(0, 1.15))
        dial = VGroup(Circle(radius=0.62).move_to(mc).set_stroke(BLUE_L, 3).set_fill(PANEL, 1.0),
                      Line(mc + 0.62 * RIGHT, mc + 0.48 * RIGHT).set_stroke(GEO, 3)).set_z_index(9)
        t_a = txt("ACUMULADO", 26).move_to(P3(5.0, 2.1))
        p_ac = P3(5.0, 0.95)
        opc = ValueTracker(1.0)                                  # v3 §11: o contador ao vivo sai quando entra Δθ = 6π ≈ 18,85 rad (uma vez só)
        self.add(opc)

        def contadores():
            th = d.th.get_value()
            dth = th - th0
            deg = math.degrees(dth) % 360.0                       # mostrador = Δθ mod 2π (a mesma variável do acumulado)
            if deg > 359.995:
                deg = 0.0
            shown = int(round(deg)) % 360
            g = VGroup()
            a = math.radians(deg)
            g.add(Line(mc, mc + 0.52 * P3(math.cos(a), math.sin(a))).set_stroke(ANG, 5).set_z_index(10))
            g.add(num2(f"{shown:d}°", ANG, 46).next_to(dial, DOWN, buff=0.25))
            n_ = int(max(2, dth * 8))
            pts = []
            for k in range(n_ + 1):                              # D8: espiral que cresce para fora a cada volta, saindo de fora do pino
                u_ = dth * k / max(1, n_)
                rr_ = 0.3 + 0.38 * u_ / (2 * PI)
                pts.append(C + rr_ * P3(math.cos(th0 + u_), math.sin(th0 + u_)))
            if dth > 0.02:
                g.add(VMobject().set_points_smoothly(pts).set_stroke(ANG, 5, opacity=0.95).set_z_index(8))
            if opc.get_value() > 0.01:
                g.add(escala_op(VGroup(lbl(r"\Delta\theta", ANG, 46), lbl("=", WHITE_, 46), num2(f"{dth:.2f}".replace(".", ","), ANG, 46), lbl(r"\mathrm{rad}", ANG, 46))
                                .arrange(RIGHT, buff=0.14).move_to(p_ac), opc.get_value()))
            if not PEDIDOS3D:
                self.reg("mostrador", mostrador_deg=float(shown), acum_rad=float(dth), th=th, dth=dth, mod=deg)
            return g
        cv = vivo(contadores)
        self.add(cv)
        self.play(FadeIn(t_m), FadeIn(dial), FadeIn(t_a), run_time=0.6)
        self.gat("se o disco deu três voltas")
        T3 = self.ate_t("o mostrador de zero a trezentos")
        rt_v = max(1.2, (T3 - 0.9 - 1.5) / 3)
        pos_mk = P3(6.0, -0.15)
        lv = txt("VOLTA A VOLTA:", 26).next_to(pos_mk, LEFT, buff=0.6)      # 6π é ângulo, não número de voltas

        def mk_(n):
            m = MathTex(str(n), r"\pi", font_size=56, color=ANG)
            m._partes = [(str(n), ANG), (r"\pi", ANG)]
            return m.set_z_index(12).move_to(pos_mk)
        mk = None
        for k in range(3):
            self.play(d.th.animate(rate_func=linear).set_value(th0 + 2 * PI * (k + 1)), run_time=rt_v)
            novo = mk_(2 * (k + 1))
            if mk is None:
                self.play(FadeIn(lv), FadeIn(novo), run_time=0.3, fixo=True)
            else:
                self.play(TransformMatchingTex(mk, novo), run_time=0.3, fixo=True)          # 2π → 4π → 6π
            mk = novo
        F, iF = M(r"\Delta\theta", "=", r"6\pi", r"\approx", r"18{,}85\ \mathrm{rad}", size=52, cores={0: ANG, 2: ANG, 4: ANG})
        self.play(FadeOut(lv), FadeOut(t_a), opc.animate.set_value(0.0), run_time=0.3)
        self.pilha.topo = -1.0
        self.pilha.poe(F, dx=0.1)
        self.voa([(mk, mp(F, iF, [2]))], extra=[FadeIn(mp(F, iF, [0, 1, 3, 4]))], rt=1.4)
        self.play(FadeOut(mk), run_time=0.3)                       # a cópia que ficou no lugar do 6π sai: Δθ só aparece em Δθ = 6π ≈ 18,85 rad
        self.remove(mk)
        self.gat("o mostrador de zero a trezentos")
        self.play(Indicate(dial, color=WHITE_, scale_factor=1.06), run_time=0.8)
        self.gat("o ângulo acumulado diz quanto")
        self.play(Indicate(F, color=WHITE_, scale_factor=1.04), run_time=0.8)
        self.ate(0.99)
