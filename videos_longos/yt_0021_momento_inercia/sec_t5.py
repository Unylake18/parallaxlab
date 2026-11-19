"""Lote PT5: T5 — E SE O EIXO SAIR DO CENTRO? T5-1 barra com o eixo deslizando (ML²/12 → ML²/3, a diferença é M(L/2)²); T5-2 placa
irregular com o CM (ponto branco), eixo pelo CM e eixo paralelo a d; r⃗ᵢ = r⃗′ᵢ + d⃗; T5-3 o termo cruzado some (Σmᵢr⃗′ᵢ = 0) → I = I_cm + Md²;
T5-4 a placa gira em torno de O, o CM anda num círculo de raio d (v_cm = ωd) → K = ½Mv_cm² + ½I_cmω² = ½I_Oω²; T5-5 gráfico I × d e o erro
clássico riscado; T5-6 Three.js 'bastao' (de cima, parado): metades com tinta rosa, CMs das metades, contas por metade → 0,282 e 0,141."""
from pecas21 import *  # noqa: F401,F403

XB5, YB5, LB5 = -6.6, 0.9, 5.4
CP, OP = P3(-3.3, -0.55), P3(-5.4, -1.6)            # T5-2: CM da placa e o outro eixo O


def meia(lead, sinal, m_, d_, size=40):
    """Conta de uma metade do bastão: [m·0,42²/12 + m·d²]; massa em rosa, distâncias em GEO, o 12 e os operadores em branco."""
    partes = [lead, sinal, r"\big[", m_, r"\cdot", r"\tfrac{0{,}42^2}{12}", "+", m_, r"\cdot", d_ + "^2", r"\big]"]
    m, ix = M(*partes, size=size, cores={3: MAS, 5: GEO, 7: MAS, 9: GEO})
    for j in ix[5][-3:]:
        m[0][j].set_color(WHITE_).set_stroke(WHITE_, 0)
    return m, ix


class LoteT5(Lote21):
    def corpo(self):
        self.an("T5-1")
        self.secao("E SE O EIXO SAIR DO CENTRO?")
        piv = ValueTracker(0.5)
        self.add(piv)
        bar = barra_fatias(XB5, YB5, LB5, 0.44, 20, brilho=False)
        cm = cm_pt(P3(XB5 + LB5 / 2, YB5), 0.1)
        ex = always_redraw(lambda: eixo_cruz(P3(XB5 + LB5 * piv.get_value(), YB5), 0.2))
        HI, XI, YI = 2.2, -1.2, -3.1
        barI = vivo(lambda: barra_E(XI, YI, HI * (1 / 12 + (piv.get_value() - 0.5) ** 2) / (1 / 3), 0.5, MAS, hmax=HI))
        lI1 = T("I", 44).move_to(P3(XI, YI - 0.35))
        self.play(FadeIn(bar), FadeIn(cm), FadeIn(ex), FadeIn(barI), FadeIn(lI1), run_time=0.6)
        A1, ia1 = M(r"I_{centro}", "=", r"\tfrac{ML^2}{12}", size=48)
        A2, ia2 = M(r"I_{ponta}", "=", r"\tfrac{ML^2}{3}", size=48)
        self.pilha.poe(A1)
        self.pilha.poe(A2)
        self.gat("lembra da barra")
        self.monta(A1, ia1, {}, rt=0.6)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.gat("pela ponta um terço")
        self.play(piv.animate.set_value(0.0), FadeIn(A2), run_time=1.2)
        cota = VGroup(Line(P3(XB5, YB5 - 0.6), P3(XB5 + LB5 / 2, YB5 - 0.6)).set_stroke(GEO, 2.4),
                      Line(P3(XB5, YB5 - 0.72), P3(XB5, YB5 - 0.48)).set_stroke(GEO, 2.4), Line(P3(XB5 + LB5 / 2, YB5 - 0.72), P3(XB5 + LB5 / 2, YB5 - 0.48)).set_stroke(GEO, 2.4))
        ld = T(r"d=\tfrac{L}{2}", 42).next_to(cota, DOWN, buff=0.12)
        A3, ia3 = M(r"I_{ponta}-I_{centro}", "=", r"\tfrac{ML^2}{4}", size=48)
        A3b, ib3 = M("=", "M", r"\big(\tfrac{L}{2}\big)^2", size=48)      # v6: duas linhas (a linha única saía da margem direita)
        self.pilha.poe(A3)
        self.pilha.poe(A3b)
        self.gat("a diferença é um quarto")
        self.monta(A3, ia3, {}, rt=0.8)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.gat("o quadrado da distância entre os dois eixos")
        self.play(Create(cota), FadeIn(ld), run_time=0.6)
        self.monta(A3b, ib3, {1: mp(A1, ia1, [2])[:1], 2: ld[0][2:]}, rt=0.9)
        self.play(piv.animate(rate_func=there_and_back).set_value(0.5), run_time=1.6)
        self.play(UpdateFromAlphaFunc(piv, lambda m_, a_: m_.set_value(float(np.sin(PI * a_)) ** 1.0)), run_time=2.2)       # v5 G6: o eixo varre a barra até a outra ponta e volta (nada parado)
        self.gat("vale para qualquer corpo")
        self.play(self.ind(A3b, ib3, [1, 2], MAS, 1.12, 0.9), run_time=0.9)
        self.foco = A3b
        self.ate(0.99)
        # ── T5-2: corpo qualquer, dois eixos paralelos ──
        self.an("T5-2")
        ex.clear_updaters()
        self.pilha.limpa(rt=0.3)
        self.guia(['PERGUNTA:', 'E UM EIXO FORA DO CM,', 'PARALELO AO PRIMEIRO?'])
        pl = placa_irregular(CP, 1.05)
        cm2 = cm_pt(CP, 0.1)
        e_cm = eixo_cruz(CP, 0.17)
        e_o = eixo_cruz(OP, 0.2)
        lO = T("O", 42).next_to(OP, DL, buff=0.3)
        pc = CP + P3(1.05, 0.62)
        ped = Square(side_length=0.26).move_to(pc).set_fill(MAS, 0.9).set_stroke(WHITE_, 2).set_z_index(10)
        lmi = T("m_i", 40).next_to(ped, UR, buff=0.3)
        self.troca([bar, cm, ex, cota, ld, barI, lI1], FadeIn(pl), FadeIn(cm2), FadeIn(e_cm), seq=True)
        lcm = txt("CM", 24).next_to(cm2, DL, buff=0.3)
        self.gat("e um eixo pelo centro de massa")
        self.play(FadeIn(lcm), run_time=0.4)
        self.play(Rotate(pl, angle=2 * PI, about_point=CP, rate_func=smooth, run_time=3.2), Flash(CP, color=WHITE_, line_length=0.2, flash_radius=0.3))      # a placa gira uma volta em torno do eixo do CM (trecho antes parado)
        self.gat("um segundo eixo paralelo")
        vd = Arrow(OP, CP, buff=0.12, stroke_width=5, max_tip_length_to_length_ratio=0.12).set_color(VETC).set_z_index(11)
        lvd = T(r"\vec d", 44, VETC).next_to(vd.get_center(), DR, buff=0.3)
        self.play(FadeIn(e_o), FadeIn(lO), GrowArrow(vd), FadeIn(lvd), run_time=0.9)
        for _ in range(4):                                                 # v6 parado 9:41: d cresce de O ao CM e os dois eixos pulsam
            self.play(Indicate(vd, scale_factor=1.12, color=WHITE_), Indicate(pl, scale_factor=1.07, color=WHITE_), Indicate(e_o, scale_factor=1.6, color=WHITE_), Indicate(e_cm, scale_factor=1.6, color=WHITE_), run_time=1.3)
        self.gat("para um pedaço i")
        vrl = Arrow(CP, pc, buff=0.1, stroke_width=4.5, max_tip_length_to_length_ratio=0.15).set_color(VETC).set_z_index(11)
        vr = Arrow(OP, pc, buff=0.12, stroke_width=4.5, max_tip_length_to_length_ratio=0.1).set_color(VETC).set_z_index(11)
        lrl = T(r"\vec r\,'_i", 42, VETC).next_to(vrl.get_center(), DR, buff=0.3)
        lr_ = T(r"\vec r_i", 42, VETC).next_to(vr.point_from_proportion(0.62), UL, buff=0.3)
        self.play(FadeIn(ped), FadeIn(lmi), run_time=0.5)
        self.play(GrowArrow(vrl), FadeIn(lrl), GrowArrow(vr), FadeIn(lr_), run_time=0.9)
        B1, ib1 = M(r"\vec r_i", "=", r"\vec r\,'_i", "+", r"\vec d", size=52, cores={0: VETC, 2: VETC, 4: VETC})
        self.pilha.poe(B1)
        self.gat("a posição vista do segundo eixo")
        self.monta(B1, ib1, {0: lr_, 2: lrl, 4: lvd})
        B2, ib2 = M("r_i^2", "=", r"r'^2_i", "+", "2", r"\vec d\cdot\vec r\,'_i", "+", "d^2", size=52, cores={5: VETC})
        self.pilha.poe(B2)
        self.gat("eleva ao quadrado")
        self.passo(B1, B2, (J(ib1, 1), J(ib2, 1)), (J(ib1, 3), J(ib2, 3)), rt=1.4, origem=False)
        self.foco = B2
        self.ate(0.99)
        # ── T5-3: multiplica por mᵢ e soma ──
        self.an("T5-3")
        C1, ic1 = M("I", "=", r"\sum m_i r'^2_i", "+", r"2\vec d\cdot", r"\Big(\sum m_i\vec r\,'_i\Big)", size=46)
        C1b, ic1b = M("+", r"\Big(\sum m_i\Big)", "d^2", size=46)
        self.pilha.so(B2)
        self.pilha.poe(C1)
        self.pilha.poe(C1b, dx=0.9)
        self.gat("multiplica por m i e soma")
        self.passo(B2, C1, (J(ib2, 1), J(ic1, 1)), (J(ib2, 3), J(ic1, 3)), rt=1.5, origem=False)
        self.monta(C1b, ic1b, {}, rt=0.6)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.gat("o primeiro termo")
        self.play(self.ind(C1, ic1, [2], MAS, 1.1, 0.8), run_time=0.8)
        self.gat("o último é a massa total")
        self.play(self.ind(C1b, ic1b, [1, 2], MAS, 1.1, 0.8), run_time=0.8)
        C2, ic2 = M(r"\sum m_i\vec r\,'_i", "=", r"M\vec R\,'_{cm}", "=", r"\vec 0", size=46)
        self.pilha.poe(C2)
        self.gat("dentro do parêntese")
        self.voa([(mp(C1, ic1, [5]), mp(C2, ic2, [0]))], extra=[FadeIn(mp(C2, ic2, [1, 2]))], rt=1.0, origem=False)
        self.selo("POR QUÊ?", ["O CM, VISTO DE SI MESMO, ESTÁ NA ORIGEM"])
        pts_ = [P3(-6.5, 0.1)]
        for k_ in range(5):
            a_ = math.radians(18 + 72 * k_)
            pts_.append(pts_[-1] + 0.8 * np.array([math.cos(a_), math.sin(a_), 0]))
        cad = VGroup(*[Arrow(pts_[k_], pts_[k_ + 1], buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.3).set_color(VETC).set_z_index(11) for k_ in range(5)])
        lcad = T(r"\sum m_i\vec r\,'_i=\vec 0", 38).move_to(P3(-5.7, 2.2))
        self.gat("zero")
        self.play(LaggedStart(*[GrowArrow(a_) for a_ in cad], lag_ratio=0.7), FadeIn(lcad), run_time=3.0)
        self.play(Flash(pts_[0], color=WHITE_, line_length=0.2, flash_radius=0.3), run_time=0.5)
        zero_ = Dot(pts_[0], radius=0.07, color=WHITE_).set_z_index(12)
        self.add(zero_)
        self.voa([(zero_, mp(C2, ic2, [4]))], extra=[FadeIn(mp(C2, ic2, [3])), Flash(cm2.get_center(), color=WHITE_, line_length=0.2, flash_radius=0.25)], rt=0.9, origem=False)
        self.remove(zero_)
        rs = risco(mp(C1, ic1, [3, 4, 5]))
        self.gat("o termo cruzado desaparece")
        self.play(Create(rs), run_time=0.6)
        D_, id_ = M("I", "=", r"I_{cm}", "+", "M", "d^2", size=58)
        Db = caixa_l(D_, MAS)
        self.pilha.poe(Db)
        self.gat("i igual a i cm mais m d ao quadrado")
        self.cx(Db[0])
        self.passo(C1, D_, (J(ic1, 0, 1), J(id_, 0, 1)), (J(ic1, 2), J(id_, 2)), rt=1.5, extra=[FadeOut(rs)], origem=False)
        self.remove(rs)
        self.foco = Db
        self.ate(0.99)
        # ── T5-4: leitura por energia (o corpo gira em torno de O) ──
        self.an("T5-4")
        self.sem_selo()
        self.pilha.so(Db)
        t0 = self.clk.get_value()
        W5 = 0.42
        S4, OP2 = 0.5, P3(-4.6, -0.1)                 # a mesma placa a 60%, com o eixo O no meio do ESQUEMA (o círculo do CM cabe na margem)
        dd = S4 * np.linalg.norm(CP - OP)
        CP2 = OP2 + S4 * (CP - OP)
        a_cm0 = math.atan2((CP - OP)[1], (CP - OP)[0])
        rot = lambda: W5 * (self.clk.get_value() - t0)

        def giro():
            a = rot()
            g = VGroup(placa_irregular(CP2, 1.05 * S4).rotate(a, about_point=OP2))
            c = OP2 + dd * np.array([math.cos(a_cm0 + a), math.sin(a_cm0 + a), 0])
            g.add(DashedVMobject(Circle(radius=dd).move_to(OP2).set_stroke(GEO, 2, opacity=0.6), num_dashes=50).set_z_index(3))
            g.add(cm_pt(c, 0.1))
            tg = np.array([-math.sin(a_cm0 + a), math.cos(a_cm0 + a), 0])
            g.add(seta(c, c + tg * 0.95, VEL, 6, tip=0.22, z=14))
            g.add(eixo_cruz(OP2, 0.2))
            return g
        gv = vivo(giro)
        self.troca([pl, cm2, e_cm, e_o, ped, lmi, vd, lvd, vrl, vr, lrl, lr_, lcm, lO, cad, lcad], FadeIn(gv), seq=True)
        lO = T("O", 42).next_to(OP2, DL, buff=0.3)
        self.add(lO)
        aw = seta_curva(OP2, 0.75, 1.9, 1.0, VEL, 5)
        lw = T(r"\omega", 42).next_to(OP2 + 0.75 * np.array([math.cos(2.4), math.sin(2.4), 0]), UL, buff=0.25)
        lvc = T(r"v_{cm}=\omega d", 42)
        lvc.move_to(P3(OP2[0] + 0.2, 2.3))
        self.gat("o centro de massa anda num círculo")
        self.play(FadeIn(aw), FadeIn(lw), run_time=0.6)
        self.gat("com velocidade ômega d")
        self.play(FadeIn(lvc), run_time=0.6)
        E1, ie1 = M("K", "=", r"\tfrac{1}{2}", "M", r"v_{cm}^2", "+", r"\tfrac{1}{2}", r"I_{cm}", r"\omega^2", size=48)
        self.pilha.poe(E1)
        self.gat("a energia do corpo é a do centro de massa")
        HK, YK, XA, XI = 2.1, -2.95, -1.9, -1.0
        sh = 0.57                                                      # Md²/(I_cm + Md²) = (K do CM)/(K total): as duas decomposições têm a mesma proporção
        cK1, cK2, cI1, cI2 = "#6FE8FF", "#A6F0FF", MAS, mix(MAS, 0.4)
        seg_cm = barra_E(XA, YK, sh * HK, 0.46, cK1)
        seg_rt = barra_E(XA, YK + sh * HK, (1 - sh) * HK, 0.46, cK2)
        seg_md = barra_E(XI, YK, sh * HK, 0.46, cI1)
        seg_ic = barra_E(XI, YK + sh * HK, (1 - sh) * HK, 0.46, cI2)
        leg = VGroup(*[VGroup(Square(side_length=0.2).set_fill(c_, 0.95).set_stroke(c_, 1), t_).arrange(RIGHT, buff=0.14)
                       for c_, t_ in ((cK1, txt("CM", 24)), (cK2, txt("GIRO", 24)), (cI1, T("Md^2", 36)), (cI2, T("I_{cm}", 36)))]).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(P3(-1.35, 0.45))
        l_k1, l_k2 = T("K", 38).move_to(P3(XA, YK - 0.42)), T("I", 38).move_to(P3(XI, YK - 0.42))
        self.play(FadeIn(mp(E1, ie1, [0, 1, 2, 3, 4])), FadeIn(seg_cm), FadeIn(seg_md), FadeIn(leg[0]), FadeIn(leg[2]), FadeIn(l_k1), FadeIn(l_k2), run_time=0.8)
        self.gat("mais a do giro em torno do centro de massa")
        self.play(FadeIn(mp(E1, ie1, [5, 6, 7, 8])), FadeIn(seg_rt), FadeIn(seg_ic), FadeIn(leg[1]), FadeIn(leg[3]), run_time=0.8)
        E2, ie2 = M("=", r"\tfrac{1}{2}", r"\big(I_{cm}+Md^2\big)", r"\omega^2", size=48)
        self.pilha.poe(E2)
        self.gat("substitui")
        self.passo(E1, E2, (J(ie1, 1), J(ie2, 0)), (J(ie1, 8), J(ie2, 3)), rt=1.4, origem=False)
        E3, ie3 = M("=", r"\tfrac{1}{2}", r"I_O", r"\omega^2", size=48)
        self.pilha.poe(E3)
        self.gat("mas a energia em torno do eixo fixo")
        self.passo(E2, E3, (J(ie2, 0), J(ie3, 0)), (J(ie2, 1), J(ie3, 1)), (J(ie2, 3), J(ie3, 3)), rt=1.2, origem=False)
        self.play(self.ind_copia(VGroup(seg_cm, seg_rt), WHITE_, 1.05, 0.9), self.ind_copia(VGroup(seg_md, seg_ic), WHITE_, 1.05, 0.9), run_time=0.9)
        self.selo("A MESMA ENERGIA", ["LIDA DE DOIS JEITOS"])
        self.reg("t5_4", d=float(dd), w=W5)
        self.foco = E3
        self.ate(0.99)
        # ── T5-5: o gráfico lê a barra (v8): o pino da barra e o ponto da curva dividem o mesmo x ──
        self.an("T5-5")
        lvc.clear_updaters()
        gv.clear_updaters()
        self.sem_selo()
        self.pilha.limpa(rt=0.3)
        AXL, X0g, YAX, YB = 5.0, -3.45, -0.15, -1.25            # 1 L = 5,0 u; o x da barra é o x do gráfico
        ax = Axes(x_range=[-0.55, 0.55, 0.25], y_range=[0, 0.45, 0.1], x_length=1.1 * AXL, y_length=2.7, tips=False,
                  axis_config={"stroke_width": 3, "color": GEO, "include_ticks": False, "include_numbers": False}).set_z_index(2)
        ax.shift(P3(X0g, YAX) - ax.c2p(0, 0))
        f5 = lambda d: 1 / 12 + d * d                            # I(d)/(M L²)
        curva = ax.plot(f5, x_range=[-0.55, 0.55], color=MAS, use_smoothing=False).set_stroke(MAS, 5).set_z_index(4)
        ld_ = T("d", 40).next_to(ax.x_axis.get_end(), RIGHT, buff=0.08)
        lI = T(r"I\ (ML^2)", 38).next_to(ax.y_axis.get_end(), UP, buff=0.2)
        xp = lambda d: X0g + d * AXL
        bar5 = barra_fatias(X0g - AXL / 2, YB, AXL, 0.44, 20, brilho=False)
        cm5 = cm_pt(P3(X0g, YB), 0.1)
        tk5 = VGroup(*[T(s_, 30, WHITE_).move_to(P3(xp(d_), YB - 0.52)) for s_, d_ in ((r"-\tfrac{L}{2}", -0.5), ("0", 0.0), (r"+\tfrac{L}{2}", 0.5))],
                     *[Line(P3(xp(d_), YB - 0.22), P3(xp(d_), YB - 0.3)).set_stroke(WHITE_, 2) for d_ in (-0.5, 0.0, 0.5)])
        dt = ValueTracker(0.0)
        self.add(dt)
        pino = vivo(lambda: eixo_cruz(P3(xp(dt.get_value()), YB), 0.2))
        cv_pts = np.array([curva.point_from_proportion(a_)[:2] for a_ in np.linspace(0, 1, 1201)])

        def dist_curva(p_):                                                # distância do ponto à polilinha da curva (u de tela)
            A_, B_ = cv_pts[:-1], cv_pts[1:]
            AB = B_ - A_
            t_ = np.clip(np.einsum("ij,ij->i", p_[None, :2] - A_, AB) / np.maximum(np.einsum("ij,ij->i", AB, AB), 1e-12), 0, 1)
            return float(np.min(np.linalg.norm(A_ + t_[:, None] * AB - p_[None, :2], axis=1)))

        def pto_():
            d_ = dt.get_value()
            p_ = ax.c2p(d_, f5(d_))
            if not PEDIDOS3D:
                self.reg("t5_5", dist=dist_curva(p_), dx=abs(float(p_[0]) - xp(d_)), d=float(d_))        # v9: PONTO NA CURVA (≤ 0,01 u) e x do pino = x do ponto (≤ 0,005 u)
            return Dot(p_, radius=0.1, color=WHITE_).set_z_index(12)
        pto = vivo(pto_)
        lig = vivo(lambda: DashedLine(P3(xp(dt.get_value()), YB + 0.22), ax.c2p(dt.get_value(), f5(dt.get_value())), dash_length=0.08).set_stroke(GEO, 2).set_z_index(3))

        def lido_():
            d_ = round(dt.get_value() * 50) / 50
            s_ = f"{f5(d_):.3f}".replace(".", "{,}")
            return T(r"I=" + s_ + r"\,ML^2", 34).move_to(ax.c2p(-0.27, 0.37))                   # v10 B4: leitura fixa no alto à esquerda da concavidade (nunca sobre a curva nem o eixo)

        def colch_():
            d_ = dt.get_value()
            if abs(d_) < 0.03:
                return VGroup()
            pa, pb = ax.c2p(d_, 1 / 12), ax.c2p(d_, f5(d_))
            sg = 1 if d_ > 0 else -1
            return VGroup(Line(pa, pb).set_stroke(mix(MAS, 0.5), 4), Line(pa + 0.07 * LEFT, pa + 0.07 * RIGHT).set_stroke(mix(MAS, 0.5), 3),
                          T("Md^2", 32, mix(MAS, 0.5)).move_to((pa + pb) / 2 + sg * 0.5 * RIGHT)).set_z_index(11)
        lido, colch = vivo(lido_), vivo(colch_)
        nivel = lambda v_, ate_: DashedLine(ax.c2p(-0.55, v_), ax.c2p(ate_, v_), dash_length=0.08).set_stroke(GEO, 2, opacity=0.8).set_z_index(1)
        marca = lambda tex_, v_: T(tex_, 30).next_to(ax.c2p(-0.55, v_), LEFT, buff=0.1)
        nv12, m12 = nivel(1 / 12, 0.55), marca(r"\tfrac{1}{12}", 1 / 12)
        nv748 = nivel(7 / 48, 0.25)
        m748 = T(r"\tfrac{7}{48}", 30).move_to(ax.c2p(0.375, 7 / 48))                          # v10 B4: 7/48 à direita de B (longe do 1/12)
        nv13, m13 = nivel(1 / 3, 0.5), marca(r"\tfrac{1}{3}", 1 / 3)
        Db0, idb0 = M("I", "=", r"I_{cm}", "+", "M", "d^2", size=52)
        Dbx = caixa_l(Db0, MAS)
        self.pilha.poe(Dbx)
        self.gat("olha o gráfico")
        self.troca([gv, lO, aw, lw, lvc, seg_cm, seg_rt, seg_md, seg_ic, leg, l_k1, l_k2],
                   FadeIn(ax), FadeIn(ld_), FadeIn(lI), FadeIn(bar5), FadeIn(cm5), FadeIn(tk5), FadeIn(Dbx), FadeIn(curva), FadeIn(pino), FadeIn(pto), FadeIn(lig), seq=True)
        self.selo("O EIXO ANDA, O I MUDA", "")
        self.vivos = [curva, ax]
        self.gat("cada ponto da curva é um eixo paralelo")
        self.play(FadeIn(lido), FadeIn(colch), dt.animate.set_value(-0.5), run_time=0.6)
        self.play(dt.animate.set_value(0.5), run_time=3.0, rate_func=smooth)
        self.gat("o menor momento de inércia")
        self.play(dt.animate.set_value(0.0), run_time=1.0)
        self.play(Flash(ax.c2p(0, 1 / 12), color=WHITE_, line_length=0.18, flash_radius=0.3), FadeIn(nv12), FadeIn(m12), run_time=0.7)
        self.gat("para qualquer lado")
        self.play(dt.animate.set_value(0.25), run_time=0.8)
        self.play(dt.animate.set_value(0.0), run_time=0.6)
        self.play(dt.animate.set_value(-0.25), run_time=0.8)
        self.play(dt.animate.set_value(0.0), run_time=0.6)
        self.gat("o erro clássico")
        uA, uB = -0.25, 0.25
        pA, pB = ax.c2p(uA, f5(uA)), ax.c2p(uB, f5(uB))
        mAB = VGroup(Dot(pA, radius=0.09, color=GEO).set_z_index(10), Dot(pB, radius=0.09, color=GEO).set_z_index(10),
                     DashedLine(P3(xp(uA), YB + 0.22), pA, dash_length=0.07).set_stroke(GEO, 2), DashedLine(P3(xp(uB), YB + 0.22), pB, dash_length=0.07).set_stroke(GEO, 2),
                     T("A", 40, GEO).move_to(P3(xp(uA) - 0.3, YB + 0.62)), T("B", 40, GEO).move_to(P3(xp(uB) + 0.3, YB + 0.62)),
                     eixo_cruz(P3(xp(uA), YB), 0.16), eixo_cruz(P3(xp(uB), YB), 0.16),
                     Line(P3(xp(uA), YB - 1.05), P3(xp(uB), YB - 1.05)).set_stroke(GEO, 2.4),
                     T(r"d_{AB}=\tfrac{L}{2}", 34, GEO).move_to(P3(X0g, YB - 1.4)))
        self.play(FadeOut(pino), FadeOut(pto), FadeOut(lig), FadeOut(lido), FadeOut(colch), Dbx.animate.set_opacity(0.45), FadeIn(mAB), run_time=0.7)
        self.remove(pino, pto, lig, lido, colch)
        self.gat("somar m d ao quadrado dá errado")
        F1, if1 = M(r"I_B", "=", r"I_A", "+", "M", r"d_{AB}^2", size=48)
        F1.set_opacity(0.75)
        self.pilha.poe(F1)
        xx = VGroup(risco(F1, cor=HEAT, w=5))
        nota = txt("A E B FORA DO CM: ERRADO", 26, color=HEAT)
        self.pilha.poe(nota, dx=0.3)
        self.monta(F1, if1, {}, rt=0.5)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.play(Create(xx), FadeIn(nota), run_time=0.5)
        self.gat("a e b têm o mesmo i")
        self.play(FadeIn(nv748), FadeIn(m748), run_time=0.7)
        self.selo("SÓ DO CENTRO DE MASSA PARA FORA", "")
        pE = ax.c2p(uB, 19 / 48)
        erro = VGroup(Arrow(pB + 0.12 * UP, pE + 0.12 * DOWN, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.25).set_color(HEAT),
                      Circle(radius=0.11).move_to(pE).set_stroke(HEAT, 4).set_fill(opacity=0), T(r"+\tfrac{ML^2}{4}", 32, HEAT).move_to(pE + 0.8 * RIGHT),
                      txt("ERRADO", 24, color=HEAT).next_to(pE, UP, buff=0.22)).set_z_index(12)
        F2, if2 = M(r"\tfrac{ML^2}{12}", "+", "M", r"\big(\tfrac{L}{2}\big)^2", "=", r"\tfrac{ML^2}{3}", size=48)
        F2l = linha_m(F2, MathTex(r"\checkmark", font_size=48, color=WHITE_), buff=0.2)
        self.pilha.poe(F2l)
        self.gat("essa conta daria um b bem maior")
        self.play(FadeIn(erro), run_time=0.9)
        self.gat("e a conferência")
        self.play(FadeOut(mAB), FadeOut(erro), FadeOut(nv748), FadeOut(m748), Dbx.animate.set_opacity(1.0), run_time=0.5)
        dt.set_value(0.5)
        self.play(FadeIn(pino), FadeIn(pto), FadeIn(lig), FadeIn(colch), FadeIn(nv13), FadeIn(m13), run_time=0.7)
        self.play(FadeIn(F2l), run_time=0.8)
        self.foco = F2l
        self.ate(0.99)
        g55 = [ax, ld_, lI, curva, bar5, cm5, tk5, pino, pto, lig, colch, nv12, m12, nv13, m13]
        # ── T5-6: o bastão (Three.js, de cima, parado) ──
        self.an("T5-6")
        self.play(FadeOut(xx), run_time=0.25)
        self.remove(xx)
        self.sem_selo()
        self.pilha.limpa(rt=0.3)
        self.guia(['PERGUNTA:', 'E O BASTÃO DO COMEÇO?', 'PELO CABO E PELA PONTA?'])                                      # v6 G4: a coluna da direita não fica vazia
        K6 = 6.2
        cam = cam_b(K=K6)
        X0m, Y0m = -6.75 / K6, 0.35 / K6                   # ponta do cabo na tela (−6,75; 0,35)
        pv = ValueTracker(0.0)
        tint = ValueTracker(0.0)
        giro = ValueTracker(0.0)                                   # v9: o bastão gira de verdade em torno do pino (cabo, depois ponta grossa)
        self.add(pv, tint, giro)

        def est(t):
            g_ = giro.get_value()
            if pv.get_value() < 0.5:
                b = {"x": X0m, "y": Y0m, "ang": g_, "piv": 0, "tint": [0.35 * tint.get_value(), tint.get_value()]}
            else:
                b = {"x": X0m + B_L, "y": Y0m, "ang": PI + g_, "piv": 1, "tint": [0.35 * tint.get_value(), tint.get_value()]}
            if not PEDIDOS3D:
                def gira_(s_):                                      # posição do ponto a s metros da ponta do cabo, com o bastão girado de g_ em torno do pino
                    px_, py_ = b["x"], b["y"]
                    dx_, dy_ = X0m + s_ - px_, 0.0
                    return tela_b(px_ + dx_ * math.cos(g_) - dy_ * math.sin(g_), py_ + dx_ * math.sin(g_) + dy_ * math.cos(g_), cam)
                self.reg("al_t56", pino=tela_b(b["x"], b["y"], cam), cm_cabo=gira_(0.21), cm_grossa=gira_(0.63))
            return r4({"bs": [b], "cam": cam})
        f3 = Fundo3D(self, "bastao", est, op=0.0)
        self.add(f3)
        P = lambda s: tela_b(X0m + s, Y0m, cam)
        self.troca(g55, f3.op.animate.set_value(1.0), tint.animate.set_value(1.0), seq=True)
        cms = VGroup(cm_pt(P(0.21), 0.08), cm_pt(P(0.63), 0.08))
        lmc = nm(r"0{,}25\ \mathrm{kg}", MAS, 38).next_to(P(0.21), UP, buff=0.75)
        lmg = nm(r"0{,}65\ \mathrm{kg}", MAS, 38).next_to(P(0.63), UP, buff=0.78)
        lmeia = VGroup(Line(P(0.0) + 0.75 * DOWN, P(0.42) + 0.75 * DOWN).set_stroke(GEO, 2), Line(P(0.42) + 0.75 * DOWN, P(0.84) + 0.75 * DOWN).set_stroke(GEO, 2),
                       *[Line(P(s) + 0.63 * DOWN, P(s) + 0.87 * DOWN).set_stroke(GEO, 2) for s in (0.0, 0.42, 0.84)])
        l42 = VGroup(nm(r"0{,}42\ \mathrm{m}", GEO, 36).next_to(P(0.21) + 0.75 * DOWN, DOWN, buff=0.22), nm(r"0{,}42\ \mathrm{m}", GEO, 36).next_to(P(0.63) + 0.75 * DOWN, DOWN, buff=0.22))
        self.gat("ele tem duas metades")
        self.play(FadeIn(lmeia), FadeIn(l42), run_time=0.6)
        self.gat("o cabo de duzentos e cinquenta")
        self.play(FadeIn(lmc), run_time=0.5)
        self.gat("e a parte grossa de seiscentos")
        self.play(FadeIn(lmg), run_time=0.5)
        self.gat("cada metade pelo seu centro")
        self.play(FadeIn(cms), run_time=0.5)
        dists = lambda a, b: VGroup(Line(P(0.0 if a == 0 else 0.84) + 1.62 * DOWN, P(b) + 1.62 * DOWN).set_stroke(GEO, 2.4),
                                     Dot(P(b) + 1.62 * DOWN, radius=0.05, color=GEO))
        d1 = VGroup(dists(0, 0.21), nm(r"0{,}21", GEO, 36).next_to(P(0.105) + 1.62 * DOWN, DOWN, buff=0.08),
                    dists(0, 0.63).shift(0.85 * DOWN), nm(r"0{,}63", GEO, 36).next_to(P(0.315) + 2.5 * DOWN, DOWN, buff=0.08))
        exi = always_redraw(lambda: eixo_cruz(P(0.0) if pv.get_value() < 0.5 else P(0.84), 0.18, z=15))
        self.add(exi)
        self.gat("com o eixo na ponta do cabo")
        self.play(FadeIn(d1), run_time=0.7)
        G1, ig1 = meia("I", "=", "0{,}25", "0{,}21")
        G2, ig2 = meia("", "+", "0{,}65", "0{,}63")
        G3, ig3 = M(r"I_{cabo}", "=", r"0{,}282\ \mathrm{kg\cdot m^2}", size=50, cores={2: MAS})
        self.pilha.poe(G1)
        self.pilha.poe(G2, dx=0.6)
        self.monta(G1, ig1, {3: lmc[0][:4], 5: l42[0], 7: lmc[0][:4], 9: d1[1]}, rt=1.4)
        self.monta(G2, ig2, {3: lmg[0][:4], 5: l42[1], 7: lmg[0][:4], 9: d1[3]}, rt=1.4)
        G3b = caixa_l(G3, MAS)
        self.pilha.poe(G3b)
        self.gat("dá zero vírgula dois oito dois")
        self.cx(G3b[0])
        self.monta(G3, ig3, {}, rt=0.7)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        dim1 = VGroup(d1, lmeia, l42, lmc, lmg, cms)
        dim1.save_state()
        self.play(dim1.animate.set_opacity(0.15), run_time=0.3)
        self.play(giro.animate(rate_func=smooth).set_value(2 * PI), run_time=2.2)                  # v9: o bastão gira em torno da ponta do cabo, com a energia de ω = 10 rad/s
        giro.set_value(0.0)
        self.play(Restore(dim1), run_time=0.3)
        # o eixo vai para a ponta grossa
        self.gat("com o eixo na ponta grossa")
        d2 = VGroup(dists(1, 0.63), nm(r"0{,}21", GEO, 36).next_to(P(0.735) + 1.62 * DOWN, DOWN, buff=0.08),
                    dists(1, 0.21).shift(0.85 * DOWN), nm(r"0{,}63", GEO, 36).next_to(P(0.525) + 2.5 * DOWN, DOWN, buff=0.08))
        self.play(FadeOut(d1), run_time=0.3)
        pv.set_value(1.0)
        self.play(FadeIn(d2), run_time=0.7)
        H1, ih1 = meia("I", "=", "0{,}65", "0{,}21")
        H2, ih2 = meia("", "+", "0{,}25", "0{,}63")
        H3, ih3 = M(r"I_{grossa}", "=", r"0{,}141\ \mathrm{kg\cdot m^2}", size=50, cores={2: MAS})
        H3b = caixa_l(H3, MAS)
        self.pilha.so(G3b)
        self.pilha.poe(H1)
        self.pilha.poe(H2, dx=0.6)
        self.monta(H1, ih1, {3: lmg[0][:4], 5: l42[1], 7: lmg[0][:4], 9: d2[1]}, rt=1.3)
        self.monta(H2, ih2, {3: lmc[0][:4], 5: l42[0], 7: lmc[0][:4], 9: d2[3]}, rt=1.3)
        self.pilha.poe(H3b)
        self.gat("dá zero vírgula um quatro um")
        self.cx(H3b[0])
        self.monta(H3, ih3, {}, rt=0.7)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.reg("t5_6", I_cabo=NUM["I_cabo"], I_grossa=NUM["I_grossa"], razao=NUM["I_cabo"] / NUM["I_grossa"])
        self.gat("exatamente a metade")
        self.selo("A RAZÃO", [MathTex(r"0{,}282\div 0{,}141=2", font_size=40, color=MAS)])
        dim2 = VGroup(d2, lmeia, l42, lmc, lmg, cms)
        dim2.save_state()
        self.play(dim2.animate.set_opacity(0.15), run_time=0.3)
        self.play(giro.animate(rate_func=smooth).set_value(2 * PI), run_time=2.6)                  # v9: o bastão gira em torno da ponta grossa
        giro.set_value(0.0)
        self.play(Restore(dim2), run_time=0.3)
        self.gat("três vezes mais perto")
        J_, ij = M(r"0{,}63\to 0{,}21", r":\ \div 3", r"\ \Rightarrow\ ", "d^2", r"\div 9", size=46, cores={0: GEO})
        self.pilha.so(G3b, H3b)
        self.pilha.poe(J_)
        self.play(FadeIn(J_), self.ind_copia(lmg, MAS, 1.15, 0.8), run_time=0.8)
        self.foco = J_
        self.ate(0.99)
        exi.clear_updaters()
        self.play(FadeOut(VGroup(d2, cms, lmc, lmg, lmeia, l42, exi)), f3.op.animate.set_value(0.0), run_time=0.4)
