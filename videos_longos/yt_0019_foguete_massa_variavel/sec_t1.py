"""Lote PT1: T1 — o carrinho que perde areia (2D). Trilho elevado sem atrito; a areia cai por um furo no fundo da caçamba até o piso (grade ciano).
Física (visto do chão): carrinho a v₀ constante; cada grão sai do furo com (v₀, 0) e cai em parábola x = x_furo(t₀) + v₀ (t − t₀),
y = y_furo − ½ g (t − t₀)², sempre na vertical do furo até tocar o piso; a massa cai linearmente de m₀ a 0,5 m₀ (furo aberto → fim do T1-4).
Câmera: acompanha o carrinho no T1-1, T1-2 e T1-4 (o piso rola); no T1-3 para (referencial do chão) para a parábola aparecer, e volta a
acompanhar no fim. Fantasma (T1-2): v_fant = v₀ m₀/m(t), nasce no carrinho e sai na frente; some no T1-3 com o selo NÃO.
A conta errada F = d(mv)/dt nunca fica na tela sem o selo NÃO (Física congelada)."""
from pecas19 import *  # noqa: F401,F403

V0 = 0.33                    # u/s (tela)
KV = 2.55                    # seta: unidades de tela por (u/s) → seta do carrinho 0,84
G_VIS = 3.0
Y_TR, Y_PISO = -1.5, -3.3    # trilho elevado e piso (onde a areia cai)
XC = -5.6                    # x do carrinho na tela enquanto a câmera acompanha
TAXA = 12.0                  # grãos por segundo


class LoteT1(Prob2):
    FUNDO = "fundo_lab_ex.png"

    def construct(self):
        self.setup_base()
        self.t1()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def t1(self):
        T = {a: dur(a) for a in ("T1-1", "T1-2", "T1-3", "T1-4", "T1-5")}
        t_f = 4.0                                                   # furo abre
        t3a = T["T1-1"] + T["T1-2"] + 0.3                            # a câmera para (T1-3)
        t3b = t3a + T["T1-3"] - 4.8                                  # volta a acompanhar
        T_dr = T["T1-1"] + T["T1-2"] + T["T1-3"] + T["T1-4"] - t_f
        a_dr = 0.5 / T_dr
        mfr = lambda t: 1.0 - a_dr * min(max(t - t_f, 0.0), T_dr)    # m/m₀
        # câmera: x_cam(t) = V0 ∫ w(s) ds, w = 1 acompanhando, 0 parada, rampas de 1,0 s
        ts_ = np.arange(0, sum(T.values()) + 30, 1 / FPS / 4)
        w = np.ones_like(ts_)
        w[(ts_ > t3a) & (ts_ < t3b)] = 0.0
        for t0, sgn in ((t3a, -1), (t3b, 1)):
            k = (ts_ > t0 - 1.0) & (ts_ <= t0)
            w[k] = (t0 - ts_[k]) / 1.0 if sgn < 0 else 1.0 - (t0 - ts_[k]) / 1.0
        w[(ts_ > t3a) & (ts_ < t3b)] = 0.0
        cam_tab = np.concatenate([[0.0], np.cumsum(w[:-1]) * (ts_[1] - ts_[0])]) * V0
        cam = lambda t: float(np.interp(t, ts_, cam_tab))
        Xc = lambda t: XC + V0 * t                                   # carrinho (mundo; tela = mundo − cam)
        car0 = carrinho2d(2.4, 1.0)
        y_furo = Y_TR + car0.yb
        t_queda = math.sqrt(2 * (y_furo - Y_PISO) / G_VIS)
        n_gr = int((sum(T.values()) + 30 - t_f) * TAXA)
        tk = t_f + (np.arange(n_gr) + np.random.default_rng(11).uniform(-0.45, 0.45, n_gr)) / TAXA      # espaçamento irregular
        rng = np.random.default_rng(4)
        jit = rng.uniform(-0.045, 0.045, n_gr)                       # ±3 px
        rad = rng.uniform(0.015, 0.03, n_gr)                         # grãos de 2–4 px
        hp = rng.uniform(0.0, 0.09, n_gr)                            # altura do montinho no piso
        self.t_fant = None
        self.d_g = 8.0
        Y_G = 0.9                                                    # faixa paralela do carrinho fantasma (mesmo tamanho do real)
        clk = self.clk
        op_g, op_vg, op_f, op_sis = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.add(op_g, op_vg, op_f, op_sis)

        def fant_x(t):
            tg = self.t_fant
            if tg is None:
                return None
            u = max(0.0, (t - tg) / self.d_g)                        # massa do fantasma: 1 → 0,5 em d_g s (v = v₀ m₀/m, até 2 v₀)
            return V0 * self.d_g * (-2.0 * math.log(1.0 - 0.5 * min(u, 1.0)) - min(u, 1.0))      # avanço sobre o carrinho real (faixa paralela; fica em 0,39 V₀ d_g)

        def fant_v(t):
            u = max(0.0, (t - self.t_fant) / self.d_g)
            return V0 / (1.0 - 0.5 * min(u, 1.0))

        def palco():
            t = clk.get_value()
            c = cam(t)
            g = VGroup()
            g.add(piso_grade(-7.35, 0.2, Y_PISO, prof=0.25, desl=-(c % 0.5)))
            # trilho elevado: viga e postes que rolam com o chão
            def pilar(xc_):
                return aco(Polygon(P3(xc_ - 0.09, Y_TR - 0.1), P3(xc_ + 0.09, Y_TR - 0.1), P3(xc_ + 0.17, Y_PISO), P3(xc_ - 0.17, Y_PISO)), 1.0)
            g.add(aco(Rectangle(width=7.55, height=0.1).move_to(P3(-3.575, Y_TR - 0.05)), 1.4), pilar(-7.2), pilar(0.05))      # viga fina + dois pilares nas pontas
            x_s = Xc(t) - c
            m_ = mfr(t)
            niv = 0.3 + 0.55 * (m_ - 0.5) / 0.5                     # o nível desce de ~85% a ~30%
            car = carrinho2d(2.4, 1.0, niv).shift(P3(x_s, Y_TR))
            g.add(car)
            # grãos (só os da tela)
            nasc = tk <= t
            if t >= t_f:
                a = t - tk[nasc]
                xw = Xc(tk[nasc]) + V0 * np.minimum(a, t_queda) + jit[nasc]
                yw = np.where(a < t_queda, y_furo - 0.5 * G_VIS * a ** 2, Y_PISO + 0.03 + hp[nasc])
                xs = xw - c
                vis = (xs > -7.3) & (xs < 0.15)
                for x_, y_, r_ in zip(xs[vis], yw[vis], rad[nasc][vis]):
                    g.add(Dot(P3(x_, y_), radius=r_, color=SAND).set_z_index(2))
                caindo = (a < t_queda) & (a > 0)
                if caindo.any():
                    xf = Xc(tk[nasc][caindo]) + V0 * a[caindo] - c          # sem o jitter: a vertical do furo
                    self.reg("graos", x_furo=x_s, x_graos=list(map(float, xf)), t=t, v_car=V0, m=m_)
                # setas iguais à do carrinho em grãos em queda (T1-3)
                o = op_vg.get_value()
                if o > 0.01:
                    ks = np.nonzero(caindo)[0][::max(1, int(TAXA * t_queda / 2))]
                    for k in ks[:2]:
                        xg_, yg_ = xs[k], yw[k]
                        if yg_ < Y_TR - 0.32 and a[k] < t_queda - 0.2:                  # a setinha acompanha o grão só no ar
                            g.add(seta(P3(xg_ + 0.06, yg_), P3(xg_ + 0.06 + KV * V0, yg_), VEL, 5, tip=0.16, op=o))
            # seta do carrinho
            yt = Y_TR + car0.yb + 1.12 + 0.25
            g.add(seta(P3(x_s - KV * V0 / 2, yt), P3(x_s + KV * V0 / 2, yt), VEL, 7, tip=0.22))
            self.reg("carrinho", x=x_s, xw=Xc(t), v=V0, t=t, m=m_)
            # fantasma
            xg = fant_x(t)
            of = op_f.get_value()
            if xg is not None and of > 0.01:
                xgs = min(x_s + xg, -3.3)
                fg = carrinho2d(2.4, 1.0, niv)                           # v4 §5: o MESMO desenho do carrinho real, 100% do tamanho, sem furo e sem areia caindo
                fg[0].set_fill(SAND, 0.55 * of)
                for k_ in (1, 2):
                    fg[k_].set_stroke(VEL, 2, opacity=of)
                fg[2].set_fill(PANEL, 0.6 * of)
                for w_ in fg[3]:
                    w_.set_stroke(VEL, 2, opacity=of).set_fill(PANEL, 0.6 * of)
                fg[4].set_opacity(0)
                fg.shift(P3(xgs, Y_G))
                vf = fant_v(t)
                ya = Y_G + 1.08
                g.add(Line(P3(-7.35, Y_G), P3(0.2, Y_G)).set_stroke("#9AA6B8", 2, opacity=of), fg,
                      seta(P3(xgs + 1.43, Y_G + 0.8), P3(xgs + 1.43 + KV * vf, Y_G + 0.8), VEL, 6, tip=0.2, op=of))
                self.reg("fantasma", x=xgs, v=vf, v_esp=V0 / (1.0 - 0.5 * min(max(0.0, (t - self.t_fant) / self.d_g), 1.0)), t=t)
            # contorno SISTEMA (T1-4): carrinho + grãos já saídos
            os_ = op_sis.get_value()
            if os_ > 0.01:
                x0 = max(-6.85, (xs[vis].min() - 0.15) if t >= t_f and vis.any() else x_s - 1.0)
                xc0, xc1 = x_s - 1.4, x_s + 1.4
                ytop, yf = Y_TR + 1.52, Y_PISO
                if t >= t_f and vis.any():
                    pts_ = [P3(xc0, ytop), P3(xc1, ytop), P3(xc1, Y_TR), P3(x_s + 0.3, Y_TR), P3(x_s + 0.3, yf - 0.12), P3(x0, yf - 0.12),
                            P3(x0, yf + 0.25), P3(x_s - 0.3, yf + 0.25), P3(x_s - 0.3, Y_TR), P3(xc0, Y_TR)]
                else:
                    pts_ = [P3(xc0, ytop), P3(xc1, ytop), P3(xc1, Y_TR), P3(xc0, Y_TR)]
                g.add(DashedVMobject(Polygon(*pts_), num_dashes=150, dashed_ratio=0.55).set_stroke(WHITE_, 2.4, opacity=0.8 * os_))
            return g
        pv = vivo(palco)
        self.palco_xs = lambda: Xc(clk.get_value()) - cam(clk.get_value())
        # ── T1-1 ──
        self.an("T1-1")
        self.secao("QUANDO A MASSA MUDA, O QUE VALE?")
        self.play(FadeIn(pv), run_time=0.8)
        yt = Y_TR + car0.yb + 1.12 + 0.25
        lv = MathTex("v", font_size=40, color=VEL)
        pos_v = lambda m: m.next_to(P3(self.palco_xs() + KV * V0 / 2, yt), RIGHT, buff=0.14)
        pos_v(lv)
        sa = txt("TRILHO SEM ATRITO", 24, color=DIM).move_to(P3(-3.4, Y_PISO - 0.5))
        self.play(FadeIn(lv), FadeIn(sa), run_time=0.6)
        lv.add_updater(pos_v)
        self.ate(0.4)
        self.gat("no fundo da caçamba tem um furo")
        self.wait(max(0.0, t_f - self.t))
        q = VGroup(txt("O CARRINHO", 32, bold=True), txt("ACELERA?", 32, bold=True)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        self.pilha.poe(q)
        self.gat("o carrinho acelera")
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.6)
        self.foco = q
        self.ate(0.97)
        # ── T1-2: a conta tentadora (com o selo NÃO desde a primeira linha errada) ──
        self.an("T1-2")
        lm = MathTex("m", font_size=40, color=MAS)
        pos_m = lambda m: m.next_to(P3(self.palco_xs() - 1.5, Y_TR + car0.yb + 0.6), LEFT, buff=0.16)
        pos_m(lm)
        self.play(FadeIn(lm), run_time=0.4)
        lm.add_updater(pos_m)
        A, ia = M("p", "=", "m", "v", size=52, cores={0: MAG, 3: VEL})
        self.pilha.limpa(rt=0.3)
        self.pilha.poe(A)
        self.gat("segunda lei na forma de momento")
        self.voa([(lm, mp(A, ia, [2])), (lv, mp(A, ia, [3]))], extra=[FadeIn(mp(A, ia, [0, 1]))], rt=1.0, origem=False)
        B_, ib = M("F", "=", r"\frac{d(mv)}{dt}", size=52, cores={0: FC, 2: MAG})
        self.pilha.poe(B_)
        self.play(FadeIn(B_), run_time=0.6)
        self.selo("TENTAÇÃO?", "SERÁ QUE VALE?", cor=WHITE_, borda=WHITE_)
        C_, ic = M("=", "m", r"\frac{dv}{dt}", "+", "v", r"\frac{dm}{dt}", size=52, cores={2: ACC, 4: VEL})
        self.pilha.poe(C_, manter=(B_,))
        self.gat("e derivar o produto")
        self.passo(B_, C_, (J(ib, 1), J(ic, 0)), rt=1.2, origem=False)
        C0, ic0 = M("0", "=", "m", r"\frac{dv}{dt}", "+", "v", r"\frac{dm}{dt}", size=52, cores={0: FC, 3: ACC, 5: VEL})
        self.pilha.poe(C0, manter=(B_,))
        self.gat("então isso dá zero")
        self.passo(C_, C0, (J(ic, 0), J(ic0, 1)), (J(ic, 1, 2, 3, 4, 5), J(ic0, 2, 3, 4, 5, 6)), rt=1.1, origem=False)
        D_, id_ = M(r"\frac{dv}{dt}", "=", "-", r"\frac{v}{m}", r"\frac{dm}{dt}", size=52, cores={0: ACC})
        D_[0][id_[3][0]].set_color(VEL)
        self.pilha.poe(D_, manter=(B_,))
        self.gat("e aí sairia que")
        self.passo(C0, D_, (J(ic0, 3), J(id_, 0)), (J(ic0, 1), J(id_, 1)), (J(ic0, 5), id_[3][:1]), (J(ic0, 2), id_[3][2:]), (J(ic0, 6), J(id_, 4)), rt=1.4, origem=False)
        self.t_fant = self.clk.get_value()
        self.d_g = 8.0
        lfv = txt("SE A CONTA VALESSE", 24, color=WHITE_).move_to(P3(-7.3 + 1.45, 2.7))
        E_, ie = M(r"\frac{dm}{dt}<0", r"\ \Rightarrow\ ", r"\frac{dv}{dt}>0", size=52, cores={2: ACC})
        self.pilha.poe(E_, manter=(B_,))
        self.gat("como a massa está diminuindo")
        self.play(FadeIn(mp(E_, ie, [0])), op_f.animate.set_value(1.0), FadeIn(lfv), run_time=0.8)
        self.gat("a aceleração dá positiva")
        self.play(FadeIn(mp(E_, ie, [1, 2])), run_time=0.7)
        self.remove(*[m for m in list(self.mobjects) if m is not E_ and isinstance(m, VGroup) and m.get_family()[1:] and all(any(x is y for y in E_.get_family()) for x in m.get_family()[1:])])
        self.add(E_)
        self.foco = E_
        self.ate(0.97)
        # ── T1-3: a câmera para; grãos em parábola embaixo do carrinho; o fantasma some ──
        self.an("T1-3")
        self.gat("cada um sai do furo")
        self.play(op_vg.animate.set_value(1.0), run_time=0.6)
        rs = risco(E_, HEAT, 5)                                       # o risco cai na conclusão errada
        self.gat("a conta estava errada")
        self.selo("NÃO", "CORPO QUE PERDE MASSA", cor=HEAT, borda=HEAT, anims=[op_f.animate.set_value(0.0), FadeOut(lfv), Create(rs)])   # o NÃO entra no gatilho do risco
        self.remove(lfv)
        self.foco = rs
        self.ate(0.97)
        # ── T1-4: SISTEMA = carrinho + areia que saiu ──
        self.an("T1-4")
        self.play(op_vg.animate.set_value(0.0), run_time=0.4)
        F1, if1 = M(r"\sum \vec F_{ext}", "=", r"\frac{d\vec P}{dt}", size=52, cores={0: FC, 2: MAG})
        F1b = txt("SÓ PARA SISTEMA FECHADO", 28, bold=True)
        self.gat("a lei força externa")
        self.sem_selo()                                              # G31: a Pilha do T1-3 só sai junto com a entrada da nova
        self.pilha.limpa(rt=0.4, anims=[FadeOut(rs)])
        self.remove(rs)
        self.pilha.poe(F1)
        self.pilha.poe(F1b)
        self.play(FadeIn(F1), run_time=0.35)
        self.gat("um sistema fechado")
        self.play(FadeIn(F1b, shift=0.1 * UP), run_time=0.5)
        lsis = txt("SISTEMA", 24, color=WHITE_)
        pos_s = lambda m: m.move_to(P3(self.palco_xs(), Y_TR + 2.12))
        pos_s(lsis)
        self.gat("a gente inclui na conta")
        self.play(op_sis.animate.set_value(1.0), FadeIn(lsis), run_time=0.9)
        lsis.add_updater(pos_s)
        G1 = linha_m(M("P_x", "=", size=52, cores={0: MAG})[0], txt("CONSTANTE", 30, bold=True), buff=0.22)
        G1b = txt("CARRINHO + AREIA QUE SAIU", 28)
        self.pilha.poe(G1)
        self.pilha.poe(G1b)
        self.gat("o momento horizontal total fica constante")
        self.play(FadeIn(G1), FadeIn(G1b), run_time=0.8)
        self.foco = G1
        self.ate(0.97)
        # ── T1-5: DICA ──
        self.an("T1-5")
        self.dica18("INCLUA NO SISTEMA O QUE SAI")
        self.ate(0.97)
        for m in (lv, lm, lsis):
            m.clear_updaters()
