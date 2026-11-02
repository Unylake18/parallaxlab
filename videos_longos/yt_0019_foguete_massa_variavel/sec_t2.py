"""Lote PT2: T2 — de onde vem o empuxo. T2-1 (Three.js 'esp': foguete no espaço, câmera junto dele), T2-1b (carrinho × foguete lado a lado,
u_rel,x = 0 × u_rel,x = −v_ex), T2-2/T2-3 (quadros INSTANTE t e INSTANTE t + dt, contorno SISTEMA), T2-4 (conta com cancelamentos, cada termo
saindo do seu rótulo), T2-5 (÷ dt → F_emp = v_ex |dm/dt|), T2-6 (Three.js: SimEsp, ⊕ do foguete + todo o gás parado, câmera recuando) e T2-7
(equação geral m dv⃗/dt = ΣF⃗_ext + u⃗_rel dm/dt; foguete e carrinho)."""
from pecas19 import *  # noqa: F401,F403

VEX_C = VREL


class LoteT2(Prob2):
    FUNDO = "fundo_lab_ex.png"

    def construct(self):
        self.setup_base()
        self.sim = SimEsp()
        self.t2_1()
        self.t2_1b()
        self.t2_esquemas()
        self.t2_6()
        self.t2_7()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    # ── T2-1: o foguete-mestre no espaço (v2: ~45% da largura, chama no sino, jato denso) ──
    def t2_1(self):
        Kt = ValueTracker(6.7)
        self.add(Kt)
        BX = -0.5
        NJ = 170

        def est(t):
            pp, aa = jato_lateral(t, BX, 0.0, n=NJ)
            return {"f": r4(est_foguete(BX, 0.0, 0.0, 1.0, "x", ch1=1.0, torre=0)),
                    "gas": {"p": pp, "c": [0] * NJ, "a": aa, "s": 4.0},
                    "cam": r4(cam_frente(K=Kt.get_value(), xc=0.3, yc=-0.3, camx=0.0, fov=16, el=0))}
        f3 = Fundo3D(self, "esp", est, op=0.0)
        self.add(f3)
        self.an("T2-1")
        self.secao("DE ONDE VEM O EMPUXO?")
        l21 = VGroup(MathTex("m", font_size=44, color=MAS).move_to(P3(0.2, 0.55)),
                     arrow(P3(1.3, 1.0), P3(2.5, 1.0), VEL, 7, tip=0.22), MathTex("v", font_size=44, color=VEL).move_to(P3(2.95, 1.0)),
                     arrow(P3(-2.6, -1.05), P3(-1.2, -1.05), FC, 7, tip=0.22), MathTex(r"F_{emp}\ ?", font_size=44, color=FC).move_to(P3(-0.35, -1.05)))
        self.play(f3.op.animate.set_value(1.0), FadeIn(l21), Kt.animate(rate_func=linear).set_value(6.9), run_time=0.8)
        self.play(Kt.animate(rate_func=linear).set_value(8.2), run_time=self.resta() - 0.15)                 # v10 M1: câmera avança devagar durante toda a fala
        self.ate(0.99)
        self.f3_t21 = f3

    # ── T2-1b: carrinho × foguete ──
    def t2_1b(self):
        self.an("T2-1b")
        velhos = self.snap()
        yb = -0.95
        car = carrinho2d(2.7, 1.13, 0.7).shift(P3(-4.0, yb))
        trilho = VGroup(Line(P3(-7.3, yb), P3(-0.9, yb)).set_stroke("#9AA6B8", 6), piso_grade(-7.3, -0.9, yb - 1.9, prof=0.4))
        fg = fog_h(4.0, 0.8, bocal=P3(3.1, yb + 0.8))
        y_v = yb + 2.05
        sv_c = arrow(P3(-4.5, y_v), P3(-3.5, y_v), VEL, 7, tip=0.22)
        sv_f = arrow(P3(5.1, y_v), P3(6.1, y_v), VEL, 7, tip=0.22)
        lv = VGroup(MathTex("v", font_size=40, color=VEL).next_to(sv_c, RIGHT, buff=0.14), MathTex("v", font_size=40, color=VEL).next_to(sv_f, RIGHT, buff=0.14))
        u = ValueTracker(0.0)
        op_s = ValueTracker(0.0)                                            # setinhas VEL nos grãos (u_rel,x = 0)
        self.add(u, op_s)
        furo = P3(-4.0, yb + car.yb)
        ESP = np.random.default_rng(9).normal(0, 0.09, 26)

        def anima():
            t = u.get_value()
            g = VGroup()
            for k in range(6):                                             # grãos caindo na vertical do furo (referencial do carrinho)
                a = (t + k * 0.22) % 1.3
                p_ = furo + P3(0, -0.5 * 1.6 * a ** 2)
                g.add(Dot(p_, radius=0.035, color=SAND))
                if op_s.get_value() > 0.01 and k in (0, 3) and a > 0.9:     # cada grão leva a mesma seta v do carrinho
                    g.add(seta(p_ + P3(0.08, 0), p_ + P3(0.98, 0), VEL, 4, tip=0.16, op=op_s.get_value()))
            for k in range(26):                                            # gás saindo para trás (referencial do foguete)
                a = (t * 1.0 + k * 0.11) % 2.8
                yy = ESP[k] * a
                if fg.bocal[0] - 0.25 - 1.5 * a > 0.85:                     # o jato não entra na calha
                    g.add(Dot(fg.bocal + P3(-0.25 - 1.5 * a, yy), radius=0.04, color=GAS_C).set_opacity(max(0.15, 1 - a / 2.8)))
            return g.set_z_index(2)
        av = vivo(anima)
        ch = chama2d(fg.bocal, 0.7, 0.4, vertical=False)
        sx = seta_tr(fg.bocal + P3(-0.35, -0.85), fg.bocal + P3(-1.75, -0.85), VEX_C, 7, tip=0.22)
        lex = MathTex(r"v_{ex}", font_size=40, color=VEX_C).next_to(sx, DOWN, buff=0.12)
        rel = txt("EM RELAÇÃO AO FOGUETE", 24, color=WHITE_).next_to(lex, DOWN, buff=0.12)
        rel.shift((0.85 - rel.get_left()[0]) * RIGHT)
        L1, i1 = M(r"u_{rel,x}", "=", "0", size=48, cores={0: VEX_C, 2: VEX_C})
        L2, i2 = M(r"u_{rel,x}", "=", r"-v_{ex}", size=48, cores={0: VEX_C, 2: VEX_C})
        L1.move_to(P3(-4.0, -3.55))
        L2.move_to(P3(5.1, -3.55))
        div = DashedLine(P3(-0.6, -3.4), P3(-0.6, 2.1), dash_length=0.1).set_stroke(GEO, 1.5, opacity=0.4)
        self.troca(velhos, FadeIn(car), FadeIn(trilho), FadeIn(fg), FadeIn(ch), FadeIn(av), FadeIn(div), seq=True)
        self.referencial("DE FORA")
        self.play(FadeIn(sv_c), FadeIn(sv_f), FadeIn(lv), u.animate(rate_func=linear).set_value(1.0), run_time=0.8)
        self.seta_v(P3(-4.5, y_v), P3(-3.5, y_v), "DE FORA", nome="v carrinho")
        self.seta_v(P3(5.1, y_v), P3(6.1, y_v), "DE FORA", nome="v foguete")
        self.gat("com que velocidade, em relação ao corpo")
        self.play(FadeIn(L1, shift=0.1 * DOWN), op_s.animate.set_value(1.0), u.animate(rate_func=linear).set_value(2.0), run_time=0.8)
        self.play(FadeIn(L2, shift=0.1 * DOWN), u.animate(rate_func=linear).set_value(3.0), run_time=0.8)
        self.gat("no foguete, o gás é jogado")
        self.play(Create(sx), FadeIn(lex), FadeIn(rel), u.animate(rate_func=linear).set_value(4.0), run_time=0.9)
        self._refs.append([int(round(self.clk.get_value() * FPS)), "v_ex", "EM RELAÇÃO AO FOGUETE", "rótulo junto da seta"]) if AUDITORIA else None
        self.foco = VGroup(L1, L2)
        self.play(Indicate(L1, color=WHITE_, scale_factor=1.08), Indicate(L2, color=WHITE_, scale_factor=1.08), u.animate(rate_func=linear).set_value(5.2), run_time=1.2)
        self.gat("se o foguete empurra o gás para trás")                    # quem empurra quem? (confirmado só no T2-5/T2-6)
        qy = 0.82                                                     # as duas setas ficam FORA do corpo, uma de cada lado do bocal
        q1 = arrow(fg.bocal + P3(-0.15, qy), fg.bocal + P3(-1.05, qy), FC, 6, tip=0.2)
        q2 = arrow(fg.bocal + P3(0.15, qy), fg.bocal + P3(1.05, qy), FC, 6, tip=0.2)
        qm = VGroup(MathTex("?", font_size=52, color=FC).next_to(q1, UP, buff=0.12), MathTex("?", font_size=52, color=FC).next_to(q2, UP, buff=0.12))
        self.play(GrowArrow(q1), GrowArrow(q2), FadeIn(qm), u.animate(rate_func=linear).set_value(6.0), run_time=0.8)
        self.play(u.animate(rate_func=linear).set_value(6.0 + max(0.5, self.resta() - 0.2)), run_time=max(0.5, self.resta() - 0.2))
        self.ate(0.99)
        av.clear_updaters()

    # ── T2-2 a T2-5: INSTANTE t, INSTANTE t + dt e a conta (v2: quadros lado a lado em cima, CONTA embaixo com a largura toda) ──
    def t2_esquemas(self):
        self.an("T2-2")
        velhos = self.snap()
        self.ref_mob = None
        self.layout_v = True                                       # sem divisão ESQUEMA × CONTA em x (ver kit.SX)
        self.pilha = Pilha(self, x0=-7.2, topo=-2.0, base=-3.8, larg=14.4, buff=0.18)
        FT, FB, YC, L_, W_ = 2.35, -1.8, 0.33, 3.2, 0.66
        fa = RoundedRectangle(corner_radius=0.12, width=7.2, height=FT - FB).move_to(P3(-3.8, (FT + FB) / 2)).set_stroke(GEO, 1.6, opacity=0.5).set_fill(PANEL, 0.25)
        fb = fa.copy().move_to(P3(3.8, (FT + FB) / 2))
        fa._fundo = fb._fundo = True
        ta = VGroup(txt("INSTANTE", 24, color=DIM), MathTex("t", font_size=36, color=DIM)).arrange(RIGHT, buff=0.12)
        ta.move_to(P3(-7.1 + ta.width / 2, FT - 0.26))
        tb = VGroup(txt("INSTANTE", 24, color=DIM), MathTex(r"t+dt", font_size=36, color=DIM)).arrange(RIGHT, buff=0.12)
        tb.move_to(P3(0.5 + tb.width / 2, FT - 0.26))
        # quadro t
        f1 = fog_h(L_, W_, bocal=P3(-6.4, YC))
        sis1 = fronteira(3.8, 1.9, P3(-4.8, YC), rotulo=None)
        sis1[0].set_stroke(CYAN, 2.4, opacity=0.95)                                   # v8 D3
        lab_s1 = txt("SISTEMA", 24, color=WHITE_)
        lab_s1.move_to(P3(-6.7 + lab_s1.width / 2, YC + 0.95 + 0.36))          # colado ao canto superior esquerdo do contorno, por fora
        lm1 = MathTex("m", font_size=40, color=MAS).move_to(P3(-4.8, YC + 0.66))
        s1 = arrow(P3(-2.75, YC), P3(-1.8, YC), VEL, 6, tip=0.2)
        lv1 = MathTex("v", font_size=40, color=VEL).next_to(s1, UP, buff=0.2)
        # quadro t + dt
        BX = 2.5
        f2 = fog_h(L_, W_, bocal=P3(BX, YC))
        g2 = nuvem(P3(1.45, YC), n=16, r=0.28)
        sis2 = fronteira(5.2, 1.9, P3(3.1, YC), rotulo=None)
        sis2[0].set_stroke(CYAN, 2.4, opacity=0.95)
        lab_s2 = txt("SISTEMA", 24, color=WHITE_)
        lab_s2.move_to(P3(0.55 + lab_s2.width / 2, YC + 0.95 + 0.36))
        lm2 = MathTex("m+dm", font_size=40, color=MAS).move_to(P3(4.15, YC + 0.95 + 0.34))
        nota = MathTex(r"(dm<0)", font_size=34, color=MAS).next_to(lm2, RIGHT, buff=0.2)
        s2 = arrow(P3(6.1, YC), P3(6.95, YC), VEL, 6, tip=0.2)
        lv2 = MathTex("v+dv", font_size=36, color=VEL).next_to(s2, UP, buff=0.2).shift(0.1 * RIGHT)
        lg = MathTex("-dm", font_size=40, color=MAS).move_to(P3(1.5, YC + 0.58))
        Y1, Y2 = -1.0, -1.44
        sx = seta_tr(P3(1.75, Y1), P3(0.65, Y1), VEX_C, 6, tip=0.2)
        lex = MathTex(r"v_{ex}", font_size=40, color=VEX_C).next_to(sx, RIGHT, buff=0.2)
        rel = txt("EM RELAÇÃO AO FOGUETE", 24).next_to(lex, RIGHT, buff=0.18)
        sy = arrow(P3(1.75, Y2), P3(1.15, Y2), VEL, 6, tip=0.2)                 # v − v_ex (v < v_ex): para trás, mais curta que a de v_ex
        lgf = M("v", "-", r"v_{ex}", size=40, cores={0: VEL, 2: VEX_C})[0].next_to(sy, RIGHT, buff=0.2)
        fora = txt("VISTO DE FORA", 24, color=WHITE_).next_to(lgf, RIGHT, buff=0.18)
        gh = fog_h(L_, W_, bocal=P3(BX, YC)).set_opacity(0.3)
        gq = VGroup(txt("O QUE MUDA EM", 26, color=DIM), MathTex(r"dt\,?", font_size=40, color=DIM)).arrange(RIGHT, buff=0.14).move_to(P3(3.8, YC + 0.75))
        self.troca(velhos, FadeIn(fa), FadeIn(ta), FadeIn(f1), FadeIn(fb), FadeIn(tb), FadeIn(gh), FadeIn(gq), seq=True)
        self.ate(0.15)
        self.gat("o foguete tem uma massa")
        self.play(FadeIn(lm1), run_time=0.4)
        self.play(GrowArrow(s1), FadeIn(lv1), run_time=0.5)
        self.gat("esse é o nosso sistema")
        self.play(Create(sis1[0]), FadeIn(lab_s1), run_time=0.8)
        self.gat("e duas hipóteses do modelo")
        self.hip([[MathTex(r"v_{ex}", font_size=34, color=VEX_C), "CONSTANTE · SEM PRESSÃO NO BOCAL"]], x0=-2.2, wmax=9.4)
        self.foco = self.s1
        self.ate(0.97)
        # ── T2-3 ──
        self.an("T2-3")
        self.sem_selo()
        self.play(FadeIn(f2), FadeOut(gh), FadeOut(gq), run_time=0.5)
        self.gat("jogou para trás um pouquinho de gás")
        self.play(FadeIn(g2, shift=0.3 * LEFT), run_time=0.6)
        self.play(ReplacementTransform(sis1[0].copy(), sis2[0]), FadeIn(lab_s2), run_time=0.9)      # o mesmo sistema, agora com o gás dentro
        bb = lambda m_: [float(m_.get_left()[0]), float(m_.get_bottom()[1]), float(m_.get_right()[0]), float(m_.get_top()[1])]
        self.reg("sis_t23", sis=bb(sis2[0]), foguete=bb(f2), nuvem=bb(g2))
        self.gat("a variação da massa do foguete")
        self.play(FadeIn(lm2), run_time=0.5)
        self.gat("é negativa")
        self.play(FadeIn(nota), run_time=0.4)
        self.gat("a velocidade aumentou")
        self.play(GrowArrow(s2), FadeIn(lv2), run_time=0.6)
        self.gat("o gás tem massa menos dm")
        self.play(FadeIn(lg), run_time=0.5)
        self.gat("a velocidade de exaustão")
        self.play(Create(sx), FadeIn(lex), FadeIn(rel), run_time=0.7)
        self._refs.append([int(round(self.clk.get_value() * FPS)), "v_ex", "EM RELAÇÃO AO FOGUETE", "rótulo junto da seta"]) if AUDITORIA else None
        self.gat("para quem olha de fora")
        self.play(GrowArrow(sy), FadeIn(lgf), FadeIn(fora), run_time=0.7)
        self.foco = VGroup(lgf, fora)
        bb_ = lambda m_: (float(m_.get_left()[0]), float(m_.get_bottom()[1]), float(m_.get_right()[0]), float(m_.get_top()[1]))
        n_tit = 0                                                                   # v3: ROTULO NA LINHA DE TITULO (nenhum rótulo de objeto dentro da faixa do título do quadro)
        for tt_, lbs in ((ta, (lm1, lab_s1, lv1)), (tb, (lm2, nota, lab_s2, lg, lv2))):
            for m_ in lbs:
                a_, b_ = bb_(tt_), bb_(m_)
                if min(a_[2], b_[2]) - max(a_[0], b_[0]) > 0.02 and min(a_[3], b_[3]) - max(a_[1], b_[1]) > 0.02:
                    n_tit += 1
                    print(f"[audit] {self.clk.get_value():7.1f}s ROTULO NA LINHA DE TITULO {type(m_).__name__} dentro da faixa do título do quadro")
        self.reg("titulo_t23", n=n_tit)
        self.ate(0.97)
        # ── T2-4: a conta (uma linha larga por passo) ──
        self.an("T2-4")
        self.sem_selo()
        A, ia = M("m", "v", "=", "(", "m+dm", ")", "(", "v+dv", ")", "+", "(", "-dm", ")", "(", "v", "-", r"v_{ex}", ")", size=40,
                  cores={1: VEL, 7: VEL, 14: VEL, 16: VEX_C})
        self.pilha.poe(A)
        self.gat("antes")
        self.voa([(lm1, mp(A, ia, [0])), (lv1, mp(A, ia, [1]))], extra=[FadeIn(mp(A, ia, [2]))], rt=0.9, origem=False)
        self.gat("o foguete, massa mais dm")
        self.voa([(lm2, mp(A, ia, [4])), (lv2, mp(A, ia, [7]))], extra=[FadeIn(mp(A, ia, [3, 5, 6, 8])), UpdateFromAlphaFunc(lm2, lambda m_, al: m_.set_opacity(1.0 if al < 0.02 else 0.0)), UpdateFromAlphaFunc(nota, lambda m_, al: m_.set_opacity(1.0 if al < 0.02 else 0.0))], rt=1.0, origem=False)       # v8 #1: nunca duas cópias de "m+dm"
        self.gat("somado com o gás")
        self.voa([(lg, mp(A, ia, [11])), (lgf, mp(A, ia, [14, 15, 16]))], extra=[FadeIn(mp(A, ia, [9, 10, 12, 13, 17]))], rt=1.0, origem=False)
        Bf, ibf = M(r"(m+dm)(v+dv)", "=", "m", "v", "+", r"m\,dv", "+", r"v\,dm", "+", r"dm\,dv", size=40, cores={3: VEL})
        pinta(Bf, ibf, 5, [(1, VEL), (2, VEL)])
        pinta(Bf, ibf, 7, [(0, VEL)])
        pinta(Bf, ibf, 9, [(2, VEL), (3, VEL)])
        Bg, ibg = M(r"(-dm)(v-v_{ex})", "=", "-", r"v\,dm", "+", r"v_{ex}\,dm", size=40)
        pinta(Bg, ibg, 3, [(0, VEL)])
        pinta(Bg, ibg, 5, [(0, VEX_C), (1, VEX_C), (2, VEX_C)])
        B, ib = M("m", "v", "=", "m", "v", "+", r"m\,dv", "+", r"v\,dm", "+", r"dm\,dv", "-", r"v\,dm", "+", r"v_{ex}\,dm", size=40, cores={1: VEL, 4: VEL})
        pinta(B, ib, 6, [(1, VEL), (2, VEL)])
        pinta(B, ib, 8, [(0, VEL)])
        pinta(B, ib, 10, [(2, VEL), (3, VEL)])
        pinta(B, ib, 12, [(0, VEL)])
        pinta(B, ib, 14, [(0, VEX_C), (1, VEX_C), (2, VEX_C)])
        self.pilha.poe(Bf)
        self.pilha.poe(Bg)
        self.gat("abrindo os parênteses")
        self.play(self.ind(A, ia, [3, 4, 5, 6, 7, 8], WHITE_, 1.06, 0.6))          # G37-3: primeiro mostra o que vai mexer
        self.play(FadeIn(Bf, shift=0.08 * DOWN), run_time=0.35)                                                            # (m + dm)(v + dv) aberto, um produto por linha
        self.play(self.ind(A, ia, [10, 11, 12, 13, 14, 15, 16, 17], WHITE_, 1.06, 0.6))
        self.play(FadeIn(Bg, shift=0.08 * DOWN), run_time=0.35)
        self.wait(0.8)                                                                                                     # hold sem nada se mexendo
        self.pilha.poe(B)
        self.play(FadeIn(mp(B, ib, [0, 1, 2])), TransformFromCopy(mp(Bf, ibf, [2, 3, 4, 5, 6, 7, 8, 9]), mp(B, ib, [3, 4, 5, 6, 7, 8, 9, 10])),
                  TransformFromCopy(mp(Bg, ibg, [2, 3, 4, 5]), mp(B, ib, [11, 12, 13, 14])), run_time=1.4)
        self.remove(*[m for m in list(self.mobjects) if m is not B and isinstance(m, VGroup) and m.get_family()[1:] and all(any(x is y for y in B.get_family()) for x in m.get_family()[1:])])
        self.add(B)
        self.wait(0.8)
        # cancelamentos (v7 §2.1): o par pisca em calor, sai e a linha se fecha NO MESMO play (nenhum vão dentro da linha)
        def fecha(src_, isrc, dst, idst, pares, sai, novo=(), extra=()):
            dst.align_to(src_, LEFT)
            dst.move_to(P3(dst.get_center()[0], src_.get_center()[1]))
            self.play(*[ReplacementTransform(mp(src_, isrc, [a]), mp(dst, idst, [b])) for a, b in pares], *[FadeOut(mp(src_, isrc, [k])) for k in sai],
                      *[FadeIn(mp(dst, idst, [k])) for k in novo], *extra, run_time=0.5)
            self.remove(src_)
            self.remove(*[m for m in list(self.mobjects) if m is not dst and isinstance(m, VGroup) and m.get_family()[1:] and all(any(x is y for y in dst.get_family()) for x in m.get_family()[1:])])
            self.add(dst)
            self.pilha.linhas = [((dst if l is src_ else l), d) for l, d in self.pilha.linhas]
        B1, ib1 = M("0", "=", r"m\,dv", "+", r"v\,dm", "+", r"dm\,dv", "-", r"v\,dm", "+", r"v_{ex}\,dm", size=40)
        pinta(B1, ib1, 2, [(1, VEL), (2, VEL)])
        pinta(B1, ib1, 4, [(0, VEL)])
        pinta(B1, ib1, 6, [(2, VEL), (3, VEL)])
        pinta(B1, ib1, 8, [(0, VEL)])
        pinta(B1, ib1, 10, [(0, VEX_C), (1, VEX_C), (2, VEX_C)])
        self.gat("aparece dos dois lados e cancela")
        par1 = VGroup(mp(B, ib, [0, 1]), mp(B, ib, [3, 4]))
        self.play(*[Indicate(x, color=HEAT, scale_factor=1.15) for x in par1], run_time=0.4)
        fecha(B, ib, B1, ib1, [(2, 1), (6, 2), (7, 3), (8, 4), (9, 5), (10, 6), (11, 7), (12, 8), (13, 9), (14, 10)], [0, 1, 3, 4, 5], novo=[0])
        S1, is1 = M("0", "=", r"m\,dv", "+", r"dm\,dv", "+", r"v_{ex}\,dm", size=40)
        pinta(S1, is1, 2, [(1, VEL), (2, VEL)])
        pinta(S1, is1, 4, [(2, VEL), (3, VEL)])
        pinta(S1, is1, 6, [(0, VEX_C), (1, VEX_C), (2, VEX_C)])
        self.gat("os termos com velocidade vezes dm")
        par2 = VGroup(mp(B1, ib1, [4]), mp(B1, ib1, [8]))
        self.play(*[Indicate(x, color=HEAT, scale_factor=1.15) for x in par2], run_time=0.4)
        fecha(B1, ib1, S1, is1, [(0, 0), (1, 1), (2, 2), (3, 3), (6, 4), (9, 5), (10, 6)], [4, 5, 7, 8])
        self.wait(0.8)
        self.gat("sobra um termo dm vezes dv")
        t3 = mp(S1, is1, [4])
        br = Brace(t3, DOWN, buff=0.14, color=DIM)
        n2 = txt("2ª ORDEM", 24, color=DIM).next_to(br, DOWN, buff=0.2)
        self.play(Indicate(t3, color=GEO, scale_factor=1.15), run_time=0.7)
        self.play(GrowFromCenter(br), FadeIn(n2), run_time=0.35)
        self.wait(1.2)                                                         # pausa útil: o cancelamento (hold)
        S2, is2 = M("0", "=", r"m\,dv", "+", r"v_{ex}\,dm", size=40)
        pinta(S2, is2, 2, [(1, VEL), (2, VEL)])
        pinta(S2, is2, 4, [(0, VEX_C), (1, VEX_C), (2, VEX_C)])
        C, ic = M(r"m\,dv", "=", "-", r"v_{ex}", r"\,dm", size=48, cores={3: VEX_C})
        pinta(C, ic, 0, [(1, VEL), (2, VEL)])
        self.gat("e fica isso")
        fecha(S1, is1, S2, is2, [(0, 0), (1, 1), (2, 2), (5, 3), (6, 4)], [3, 4], extra=[FadeOut(br), FadeOut(n2)])      # v7: o termo de 2ª ordem sai e a linha fecha no mesmo play
        self.wait(0.8)
        self.pilha.poe(C)
        self.play(self.ind(S2, is2, [4], VEX_C, 1.12, 0.6))
        self.passo(S2, C, (J(is2, 2), J(ic, 0)), (J(is2, 1), J(ic, 1)), (J(is2, 4), J(ic, 3, 4)), rt=1.3, origem=False)       # v_ex dm atravessa o "=" e o sinal troca
        self.foco = C
        self.ate(0.97)
        # ── T2-5: ÷ dt ──
        self.an("T2-5")
        self.pilha.so(C)
        D, id_ = M("m", r"\frac{dv}{dt}", "=", "-", r"v_{ex}", r"\frac{dm}{dt}", "=", r"v_{ex}", r"\left|\frac{dm}{dt}\right|", size=46,
                   cores={1: ACC, 4: VEX_C, 7: VEX_C})
        cauda = mp(D, id_, [6, 7, 8])
        cauda.set_opacity(0)                                                  # "= v_ex |dm/dt|" só aparece no "do lado direito"
        self.pilha.poe(D)
        self.gat("divide tudo pelo intervalo")
        D.set_opacity(0)                                                      # G34: a linha nova entra sem a sopa de glifos do passo
        self.add(D)
        self.play(self.revela(D, id_, range(6), 0.9))
        self.pilha.so(D)
        self.gat("do lado direito")
        self.play(self.revela(D, id_, [6, 7, 8], 0.8))
        self.gat("a vazão")                                                                                # v9: a fala corre sobre a equação parada; cada termo aceso na hora em que é dito
        self.play(self.ind(D, id_, [5], MAS, 1.15, 0.8))
        self.gat("que fica positiva")
        self.play(self.ind(D, id_, [8], WHITE_, 1.15, 0.8))
        self.gat("faz o papel de uma força")
        self.play(self.ind(D, id_, [7, 8], FC, 1.1, 0.8))
        E, ie = M("F_{emp}", "=", r"v_{ex}", r"\left|\frac{dm}{dt}\right|", size=48, cores={0: FC, 2: VEX_C})
        Eb = caixa_l(E, FC)
        Eb.move_to(P3(0.9 + Eb.width / 2, D.get_y()))                             # a caixa ao lado da linha D: D fica na tela até o fim do T2-5
        self.gat("é o empuxo")
        self.passo(D, E, (J(id_, 7), J(ie, 2)), (J(id_, 8), J(ie, 3)), extra=[FadeIn(Eb[0])], rt=1.3, origem=False)
        se = arrow(P3(BX, YC + 0.62), P3(BX + 0.7, YC + 0.62), FC, 7, tip=0.22)  # nasce no bocal e corre logo acima do corpo
        lse = MathTex("F_{emp}", font_size=38, color=FC).next_to(se, RIGHT, buff=0.12)
        self.play(GrowArrow(se), FadeIn(lse), run_time=0.7)
        U_, iu = M(r"\mathrm{m/s}\cdot\mathrm{kg/s}", "=", r"\mathrm{kg\cdot m/s^2}", "=", r"\mathrm{N}", size=40)
        U_.move_to(P3(-7.2 + U_.width / 2, -3.55))
        self.gat("e as unidades fecham")
        self.play(FadeIn(U_), run_time=0.8)
        self.foco = Eb
        self.ate(0.97)
        self.caixa_emp = Eb

    # ── T2-6: a simulação (⊕ do foguete + todo o gás parado) ──
    def t2_6(self):
        self.an("T2-6")
        velhos = list(self.snap())
        self.layout_v = False
        self.pilha = Pilha(self)
        s = self.sim
        es = EspSim(self, s, "neutro", yc=-0.6, op=0.0, larg=6.2)
        self.add(es.ts, es.chama, es.rec, es.f3d)
        es.rec.add_updater(lambda m_: m_.set_value(0.07 * max(0.0, (es.ts.get_value() - s.TQ) / FAT)))     # voo livre: a câmera recua devagar
        TQ_TELA = s.TQ / FAT

        def camada():
            ts = es.ts.get_value()
            cm = es.tela(ts, s.cm(ts)[0])
            g = VGroup(marcador_cm(cm, r=0.2))
            x, v, m = s.foguete(ts)
            b = es.tela(ts, x)
            o = es.chama.get_value() * (1.0 if ts < s.TQ else max(0.0, 1 - (ts - s.TQ) / (0.4 * FAT)))
            if o > 0.02:
                pass                                                                 # v3: as setas de força ficam no inset de lupa (NO BOCAL)
            km = es.cam(ts)["K"] * 100.0                                    # cota de escala: 100 km no eixo (50, 25… se a barra passar do inset)
            n_km = 100
            while km > 8.8 and n_km > 5:
                km, n_km = km / 2.0, n_km // 2
            y_ = -2.85
            g.add(Line(P3(-6.9, y_), P3(-6.9 + km, y_)).set_stroke(GEO, 2.5), Line(P3(-6.9, y_ - 0.08), P3(-6.9, y_ + 0.08)).set_stroke(GEO, 2.5),
                  Line(P3(-6.9 + km, y_ - 0.08), P3(-6.9 + km, y_ + 0.08)).set_stroke(GEO, 2.5),
                  rot(f"{n_km} km", 26, color=GEO).move_to(P3(-6.4, -3.2)))
            gx, gy, _, _, _ = s.gas(ts)
            if o > 0.02:
                self.reg("forca", lugar="T2-6", d_px=float(np.hypot(0.0, 0.09) * 60))             # origem das setas FC × bocal (no inset: ±0,09)
            self._selo_sobre_3d(b, es.L_TELA)
            self.reg("cm_gas", t=ts, cm_px=float(cm[0]) * 60, cm_y=float(cm[1]), cm_m=s.cm(ts)[0], cm_ym=s.cm(ts)[1], P=s.momento(ts), x=x, v=v, m=m, K=es.cam(ts)["K"])
            return g.set_z_index(8)
        cv = vivo(camada)
        cv._tela_cheia = True                                               # 3D em tela cheia: sem ESQUEMA × CONTA (calha não se aplica)
        lab = tx("⊕ FOGUETE + GÁS", 24)
        lab._tela_cheia = True
        lab.move_to(es.tela(0.0, 0.0) + P3(0, -0.8))                         # o ⊕ fica parado na tela: o rótulo também
        # inset de lupa no bocal (canto inferior direito, 5,0 de largura = 31% da tela)
        IX, IY, IW, IH = 5.1, -2.2, 5.0, 2.5
        moldura = RoundedRectangle(corner_radius=0.12, width=IW, height=IH).move_to(P3(IX, IY)).set_fill(PANEL, 0.9).set_stroke(GEO, 1.8)
        moldura._fundo = moldura._caixa = True
        bx_, by_ = IX - 0.7, IY - 0.05
        mini = FogueteMestre(2.9, 0.8, horizontal=True, bocal=P3(bx_, by_))
        mini.set_opacity(0.55)
        rngi = np.random.default_rng(6)
        gasi = VGroup(*[Dot(P3(bx_ - 0.3 - rngi.uniform(0, 1.2), by_ + rngi.normal(0, 0.12)), radius=0.04, color=GAS_C).set_opacity(0.8) for _ in range(18)])
        chi = chama2d(P3(bx_, by_), 0.5, 0.3, vertical=False)
        a_f = arrow(P3(bx_, by_ + 0.09), P3(bx_ + 1.2, by_ + 0.09), FC, 7, tip=0.22)
        a_g = arrow(P3(bx_, by_ - 0.09), P3(bx_ - 1.2, by_ - 0.09), FC, 7, tip=0.22)
        l_f = txt("NO FOGUETE", 24, color=FC).move_to(P3(bx_ + 1.2, by_ + 0.98))
        l_g = txt("NO GÁS", 24, color=FC).move_to(P3(bx_ - 0.6, by_ - 0.75))
        l_b = VGroup()                                                    # v4 #25: o título do inset já diz; sem 'NO BOCAL'
        inset = VGroup(moldura, mini, gasi, chi, a_f, a_g, l_f, l_g, l_b).set_z_index(30)
        inset._tela_cheia = True
        self.reg("inset_t26", larg=IW, tela=16.0)
        lF = inset
        def pos_lf(m_):
            return m_
        esc = VGroup(txt("FOGUETE FORA DE ESCALA", 24, color=DIM).move_to(P3(-2.6, -3.2)))
        lab_emp = self.caixa_emp.copy().move_to(P3(4.7, 2.55))
        lab_emp._selo = "faixa"
        self.caixa_emp = lab_emp
        esc._tela_cheia = True
        self.troca(velhos, es.f3d.op.animate.set_value(1.0), FadeIn(cv), FadeIn(lab), FadeIn(esc), FadeIn(lab_emp), FadeIn(inset), seq=True)
        self.referencial("DE FORA (O FOGUETE PARTIU DO REPOUSO)")
        self.play(es.chama.animate.set_value(1.0), es.ts.animate(rate_func=linear).set_value(0.6 * FAT), run_time=0.6)
        lF.add_updater(pos_lf)
        lF.add_updater(lambda m_: escala_op(m_, 1.0) if es.ts.get_value() < s.TQ else m_.set_opacity(max(0.0, 1 - (es.ts.get_value() - s.TQ) / (0.4 * FAT))))
        t_rest = self.resta() - 0.2
        self.play(es.ts.animate(rate_func=linear).set_value(0.6 * FAT + t_rest * FAT), run_time=t_rest)
        self.ate(0.99)
        lab.clear_updaters()
        lF.clear_updaters()
        es.rec.clear_updaters()
        self.remove(lF)
        self.es26 = es

    # ── T2-7: a equação geral (v2: os mini-esquemas entram junto da equação, sem tela só com a caixa) ──
    def t2_7(self):
        self.an("T2-7")
        velhos = [m for m in self.snap() if m is not self.caixa_emp]
        G, ig = M("m", r"\frac{d\vec v}{dt}", "=", r"\sum\vec F_{ext}", "+", r"\vec u_{rel}", r"\frac{dm}{dt}", size=50, cores={1: ACC, 3: FC, 5: VEX_C})
        Gb = caixa_l(G, BLUE_L)
        self.ref_mob = None
        self.ref_atual = None
        self._troca_t27 = velhos
        self.pilha.linhas = []
        self.pilha.poe(Gb)
        # mini-esquemas: foguete (em cima) e carrinho (embaixo), prontos junto com a equação
        fg = fog_h(2.2, 0.44, bocal=P3(-5.6, 1.75))
        ch = chama2d(fg.bocal, 0.45, 0.24, vertical=False)
        sx = seta_tr(fg.bocal + P3(-0.3, -0.55), fg.bocal + P3(-1.45, -0.55), VEX_C, 6, tip=0.2)
        a1 = M(r"u_{rel}", "=", r"-v_{ex}", size=40, cores={0: VEX_C, 2: VEX_C})[0].next_to(fg, UP, buff=0.2)
        a1b = VGroup(M(r"u_{rel}", r"\frac{dm}{dt}", ">", "0", size=40, cores={0: VEX_C})[0], tx("→ EMPUXO PARA A FRENTE", 26)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        a1b.move_to(P3(-7.3 + a1b.width / 2, 0.2))
        car = carrinho2d(1.6, 0.66, 0.6).shift(P3(-4.3, -2.7))
        tr = Line(P3(-7.0, -2.7), P3(-1.6, -2.7)).set_stroke("#9AA6B8", 6)
        sc = arrow(P3(-4.75, -1.3), P3(-3.85, -1.3), VEL, 6, tip=0.2)
        b1 = M(r"u_{rel,x}", "=", "0", size=40, cores={0: VEX_C, 2: VEX_C})[0]
        b1.move_to(P3(-7.35 + b1.width / 2, -3.12))                              # v7 #12: abaixo do carrinho, à esquerda da queda do grão
        b1b = tx("NADA NA HORIZONTAL", 18)                                           # v8 #3: sem a seta inicial, o texto termina longe da setinha do grão
        b1b.move_to(P3(-7.35 + b1b.width / 2, -3.58))                              # v6: à esquerda da queda do grão (a seta v do grão fica livre)
        furo = P3(-4.3, -2.7) + P3(0, car.yb)
        ESP7 = np.random.default_rng(5).normal(0, 0.08, 14)

        def anim7():
            t = self.clk.get_value()
            g = VGroup()
            for k in range(14):                                            # gás saindo para trás (referencial do foguete)
                a = (t + k * 0.2) % 2.8
                xx = fg.bocal[0] - 0.25 - 1.3 * a
                if xx > -6.9:
                    g.add(Dot(P3(xx, fg.bocal[1] + ESP7[k] * a), radius=0.04, color=GAS_C).set_opacity(max(0.15, 1 - a / 2.8)))
            a2 = t % 1.3                                                   # grão do carrinho: cai na vertical do furo, com a mesma seta v do carrinho
            p_ = furo + P3(0, -0.5 * 1.6 * a2 ** 2)
            g.add(Dot(p_, radius=0.035, color=SAND))
            if a2 > 0.85:                                                  # só abaixo do trilho (nunca sobre as rodas)
                g.add(seta(p_ + P3(0.08, 0), p_ + P3(0.98, 0), VEL, 4, tip=0.16, op=0.9))
            return g.set_z_index(2)
        av7 = vivo(anim7)
        self.troca(self._troca_t27, FadeIn(fg), FadeIn(ch), FadeIn(car), FadeIn(tr), FadeIn(sc), FadeIn(av7), seq=True)          # v3 G31: a cena nova já nasce com os mini-esquemas (sem 6 s só com a caixa)
        self.gat("massa vezes aceleração é igual")
        E = self.caixa_emp[1]
        self.play(TransformMatchingTex(E, G), ReplacementTransform(self.caixa_emp[0], Gb[0]), run_time=1.4)
        self.remove(self.caixa_emp)
        self.add(Gb)
        nt = VGroup(linha_m(MathTex(r"\vec u_{rel}", font_size=40, color=VEX_C), "= VELOCIDADE DE QUEM ENTRA", size=26), txt("OU SAI, EM RELAÇÃO AO CORPO", 26))
        nt.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(nt)
        self.play(FadeIn(nt), run_time=0.6)
        self.gat("no foguete")
        self.play(Create(sx), FadeIn(a1), run_time=0.6)
        self.gat("e aparece o empuxo")
        self.play(FadeIn(a1b), run_time=0.6)
        self.gat("no carrinho")
        self.play(FadeIn(b1), run_time=0.7)
        self.gat("o termo some")
        self.play(FadeIn(b1b), run_time=0.6)
        self.gat("uma equação, os dois casos")
        self.play(Gb.animate(rate_func=there_and_back).scale(1.05), run_time=0.8)
        self.foco = Gb
        self.ate(0.97)
        av7.clear_updaters()
