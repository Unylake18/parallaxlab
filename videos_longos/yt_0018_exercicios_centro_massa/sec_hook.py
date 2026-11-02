"""Lote PH (v2): hook H1–H3 no lago em Three.js (lago3d.js: gafanhoto procedural com poses, folha 3D, água com reflexos) e abertura A1–A4.
H1 câmera baixa em 3/4 aproximando; a cota L = 30 cm nasce ao longo da folha · H2 agacha, salta a 30°, a folha recua com esteira; rastro
violeta com poses fantasma; respingo e anéis; replay 0,5× de lado com a folha inicial em tracejado · H3 congela; pergunta acima da cena; o ⊕
do sistema · A1 logo · A2 cinco ícones · A3 faixa no rodapé + a granada do yt_0017 + R⃗_cm e M A⃗_cm acendendo token a token · A4 checklist
(sai de cena; nos problemas vira chip, G26)."""
from icones import *  # noqa: F401,F403
from lago2 import *  # noqa: F401,F403


class GranadaMini(Granada3D):
    XC = -3.75

    def cam(self):
        c = super().cam()
        c["xc"] = c.get("xc", 0.0) + self.XC
        return c


class LoteHook(Prob2):
    FUNDO = "fundo_lab.png"

    def construct(self):
        self.setup_base()
        self.hook()
        self.abertura()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def hook(self):
        lg = self.lg = Lago3D(self, theta=30.0, K=17.0, az=-62.0, el=9.0, alvo=(0.13, 0.0, 0.02), xc=0.0, yc=-0.55, fov=16.0, esc=1.5, op=1.0)   # o vídeo abre já no lago
        self.add(*lg.trackers(), lg.f3d)
        lg.f3d._quadro()
        self._futuros.append(lg.futuro)
        T = lg.T()
        traj_op = ValueTracker(0.0)
        ini_op = ValueTracker(0.0)
        self.add(traj_op, ini_op)

        def camada():
            e = lg.f3d.e
            cam = e["cam"]
            tau = lg.tau.get_value()
            g = VGroup()
            if traj_op.get_value() > 0.01 and tau > 0:
                ss = np.linspace(0, min(tau, T), 40)
                pts_ = [q for q in (lg.P(*lg.estado_f(s)[:2], cam=cam) for s in ss) if abs(q[0]) < 7.4 and abs(q[1]) < 3.9]   # dentro do quadro
                if len(pts_) > 2:
                    g.add(VMobject().set_points_smoothly(pts_).set_stroke(VEL, 2.4, opacity=traj_op.get_value()))
            if ini_op.get_value() > 0.01:
                o = ini_op.get_value()
                a, b = lg.P(0.0, 0.004, cam=cam), lg.P(lg.L, 0.004, cam=cam)
                g.add(DashedLine(a, b, dash_length=0.09).set_stroke(WHITE_, 2.4, opacity=0.8 * o),
                      Line(a + 0.12 * DOWN, a + 0.12 * UP).set_stroke(WHITE_, 2, opacity=0.8 * o), Line(b + 0.12 * DOWN, b + 0.12 * UP).set_stroke(WHITE_, 2, opacity=0.8 * o))
                xf = lg.estado_f()[2]
                if xf < -0.01:
                    y = lg.P(0.0, -0.03, cam=cam)[1] - 0.25
                    g.add(seta(P3(lg.P(0.0, 0.0, cam=cam)[0], y), P3(lg.P(xf, 0.0, cam=cam)[0], y), GEO, 5, tip=0.18, op=o))                     # deslocamento: comprimento (GEO)
            lg.reg()
            return g
        cam_ = vivo(camada)
        self.add(cam_)
        # ── H1: câmera baixa em 3/4, aproximando; a cota L nasce ao longo da folha ──
        self.an("H1")
        self.play(lg.f3d.op.animate.set_value(1.0), lg.K.animate(rate_func=linear).set_value(22.0), run_time=1.0)
        self.play(lg.K.animate(rate_func=linear).set_value(26.0), lg.ax.animate(rate_func=linear).set_value(0.14), run_time=max(1.0, 0.5 * dur("H1") - 1.0))

        def cota_l():
            cam = lg.f3d.e["cam"]
            a, b = lg.P(0.0, 0.0, y=-0.12, cam=cam), lg.P(lg.L, 0.0, y=-0.12, cam=cam)
            u = (b - a) / np.linalg.norm(b - a)
            n = np.array([-u[1], u[0], 0.0])
            lab = mrot("L = 30 cm", 30, GEO).move_to((a + b) / 2 - 0.46 * n)
            fundo_ = RoundedRectangle(corner_radius=0.08, width=lab.width + 0.24, height=lab.height + 0.16).move_to(lab).set_fill(PANEL, 0.85).set_stroke(width=0)
            fundo_._fundo = fundo_._caixa = True
            return VGroup(fundo_, Line(a, b).set_stroke(GEO, 2.6), Line(a - 0.1 * n, a + 0.1 * n).set_stroke(GEO, 2.4), Line(b - 0.1 * n, b + 0.1 * n).set_stroke(GEO, 2.4), lab)
        cl = vivo(cota_l)

        def rot_massa():                                                                         # v6 (hook ampliado): "a folha tem quatro vezes a massa dele"
            cam = lg.f3d.e["cam"]
            a, b = lg.P(0.0, 0.0, y=-0.12, cam=cam), lg.P(lg.L, 0.0, y=-0.12, cam=cam)
            u = (b - a) / np.linalg.norm(b - a)
            n = np.array([-u[1], u[0], 0.0])
            lab = mrot("FOLHA = 4 × A MASSA DO GAFANHOTO", 28, WHITE_).move_to((a + b) / 2 - 1.0 * n)
            fundo_ = RoundedRectangle(corner_radius=0.08, width=lab.width + 0.24, height=lab.height + 0.16).move_to(lab).set_fill(PANEL, 0.85).set_stroke(width=0)
            fundo_._fundo = fundo_._caixa = True
            return VGroup(fundo_, lab)
        lm_ = vivo(rot_massa)
        self.gat("trinta centímetros")
        self.play(FadeIn(cl), lg.K.animate(rate_func=linear).set_value(27.5), run_time=1.0)
        self.gat("quatro vezes a massa dele")
        self.play(FadeIn(lm_), run_time=0.6)
        self.play(lg.K.animate(rate_func=linear).set_value(29.0), run_time=max(0.5, self.resta() - 0.03), fixo=True)   # v7: a aproximação segue até o fim da fala (nunca fica parada)
        # ── H2: agacha, salta a 30°; a câmera acompanha; poses fantasma; respingo; depois o replay em câmera lenta (v7: velocidade CONSTANTE, sem pausa) ──
        self.an("H2")
        self.play(FadeOut(cl), FadeOut(lm_), lg.pre.animate.set_value(1.0), run_time=0.5)
        cl.clear_updaters()
        lm_.clear_updaters()
        traj_op.set_value(1.0)
        lg.op_fant.set_value(1.0)
        self.play(lg.tau.animate(rate_func=linear).set_value(T), lg.ax.animate.set_value(0.62), lg.K.animate.set_value(7.5), lg.el.animate.set_value(11.0),
                  lg.az.animate.set_value(-74.0), run_time=1.6)                                    # "ele salta… e passa direto"
        self.play(lg.tau.animate(rate_func=linear).set_value(T + 0.15), lg.anel.animate(rate_func=linear).set_value(1.0), run_time=1.6)    # "cai na água"
        self.gat("olha de novo")
        self.play(lg.tau.animate.set_value(0.0), lg.pre.animate.set_value(0.0), traj_op.animate.set_value(0.0), lg.anel.animate.set_value(0.0),
                  lg.az.animate.set_value(-90.0), lg.el.animate.set_value(20.0), lg.K.animate.set_value(7.4), lg.ax.animate.set_value(0.6),
                  run_time=1.0)                                                                    # v7: o replay mostra o salto INTEIRO (2 m de largura), com a folha recuando
        lg.op_fant.set_value(0.0)
        self.gat("instante do salto")
        self.play(ini_op.animate.set_value(1.0), run_time=0.5)                                   # a posição inicial da folha, tracejada
        self.gat("em câmera lenta")
        # velocidade CONSTANTE: o relógio do replay anda k segundos reais por segundo de vídeo; agacha até "escorrega para trás" (a folha começa a recuar
        # junto com a fala), voa até "e mais cinco problemas" (pouso e respingo, em câmera lenta, até o fim do H3). Nenhum quadro parado.
        fps_ = float(FPS)
        t0_ = (self.nq + self._off) / fps_
        t_dec = ANC["H2"]["ini"] + ANC["H2"]["t"][ANC["H2"]["fala"].split().index("escorrega")] - LEAD
        t_pouso = ANC["H3"]["ini"] + ANC["H3"]["t"][ANC["H3"]["fala"].split().index("mais")] - LEAD
        k_ = T / (t_pouso - t_dec)                                                                   # s reais de movimento por s de vídeo (≈ 1/22)
        Pc_ = k_ * (t_dec - t0_)                                                                     # agachar leva (t_dec − t0) s de vídeo
        print(f"[replay] câmera lenta a 1/{1 / k_:.1f}: agacha {Pc_:.3f} s reais, voo {T:.3f} s, pouso em {t_pouso:.1f} s")

        def replay(m):
            rp = k_ * ((self.clk.get_value() + self._off / fps_) - t0_)
            if rp <= 0:
                return
            if rp < Pc_:
                lg.pre.set_value(rp / Pc_)
                m.set_value(0.0)
            else:
                lg.pre.set_value(1.0)
                m.set_value(min(rp - Pc_, T + 0.40))
        lg.tau.add_updater(replay)
        self.ate(0.97)
        # ── H3: a pergunta aparece com ele ainda no ar; o ⊕ do sistema acompanha o voo; o respingo fecha a cena ──
        self.an("H3")
        p1 = txt("EM QUE ÂNGULO ELE PRECISA PULAR", 36, bold=True)
        p2 = txt("PARA CAIR DE VOLTA NA FOLHA?", 36, bold=True)
        self.pergunta = VGroup(p1, p2).arrange(DOWN, buff=0.16).move_to(P3(-1.2, 3.0)).set_z_index(30)
        self.play(FadeIn(self.pergunta, shift=0.1 * UP), run_time=0.8)

        def cm_vivo():
            xc_, yc_ = lg.cm()
            pc_ = lg.P(xc_, yc_)
            return VGroup(tracejado(lg.P(xc_, -0.03), lg.P(xc_, max(0.08, yc_ + 0.04)), WHITE_, 2, 0.6), marcador_cm(pc_, r=0.18))
        cmm = vivo(cm_vivo)
        self.gat("o centro de massa resolve isso")
        self.play(FadeIn(cmm), run_time=0.7)                                                        # "o centro de massa resolve isso"
        xc0_, yc0_ = lg.cm()
        self.play(onda(lg.P(xc0_, yc0_)), run_time=0.8)
        self.ate(0.8)
        xc1_, yc1_ = lg.cm()
        self.play(onda(lg.P(xc1_, yc1_)), run_time=0.8)
        self.ate(0.97)
        lg.tau.clear_updaters()

    def abertura(self):
        self._futuros.clear()
        # ── A1 ──
        self.an("A1")
        velhos = self.snap()
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        bv = txt("BEM-VINDOS AO PARALLAX LAB", 30, op=0.95).move_to(P3(0, -0.5))
        self.troca(velhos, FadeIn(logo, scale=0.94), FadeIn(bv, shift=0.1 * UP), seq=True)
        self.ate(0.97)
        # ── A2: cinco ícones ──
        self.an("A2")
        tt = txt("CENTRO DE MASSA", 54, bold=True).move_to(P3(0, 2.75))
        sub = txt("6 PROBLEMAS QUE PARECEM IMPOSSÍVEIS", 32).next_to(tt, DOWN, buff=0.3)
        nv = txt("NESTE VÍDEO:", 28, op=0.85).move_to(P3(-6.0, 0.75))
        itens = VGroup(*[item(k, 0.92, 26) for k in range(5)])
        for k, it in enumerate(itens):
            it.move_to(P3(-6.0 + 3.0 * k, -1.2))
        self.play(FadeOut(logo), FadeOut(bv), FadeIn(tt, shift=0.1 * UP), FadeIn(sub), FadeIn(nv), FadeIn(itens[0], shift=0.12 * UP), run_time=0.9)   # palco desde o começo
        self.ate(0.25)
        for k, it in enumerate(itens[1:]):
            self.play(FadeIn(it, shift=0.12 * UP), run_time=0.55)
        self.foco = itens[-1][0]                                                         # PAUSAS: o último ícone pulsa enquanto a fala termina
        self.ate(0.97)
        # ── A3: faixa no rodapé; a granada; R⃗_cm e M A⃗_cm token a token ──
        self.an("A3")
        faixa = VGroup(*[VGroup(icone(k, 0.26), tx(CURTOS[k], 24)).arrange(RIGHT, buff=0.1) for k in range(5)]).arrange(RIGHT, buff=0.22)
        faixa.move_to(P3(0, -3.62))
        g = GranadaMini(self, K=0.48, camx=6.12, yc=-1.45, op=0.0, w=1.0)
        g.tau.set_value(0.3)
        g.f3d._quadro()
        self.add(*g.trackers(), g.f3d)
        par = DashedVMobject(VMobject().set_points_smoothly([g.m(g.ideal(s)) for s in np.linspace(0, 2 * g.TE, 50)]), num_dashes=50, dashed_ratio=0.55) \
            .set_stroke(WHITE_, 2.5, opacity=0.5).set_z_index(6)
        tau0 = g.tau.get_value()

        def cm_cam():
            tau = g.tau.get_value()
            ts = np.linspace(tau0, tau, max(2, int((tau - tau0) * 8) + 2))
            return VGroup(rastro_cm([g.m(g.fis(s)[3]) for s in ts], w=4, op=0.9), marcador_cm(g.cm(), r=0.15))
        cmv = vivo(cm_cam)
        caixa_c = RoundedRectangle(corner_radius=0.12, width=6.6, height=3.9).move_to(P3(4.0, 0.3)).set_fill(PANEL, 0.88).set_stroke(BLUE_L, 1.6)
        caixa_c._fundo = True
        E1, e1 = eqf([r"\vec R_{cm}", "="], [r"\sum_i", r"m_i", r"\vec r_i"], ["M"], size=56, cores={("pre", 0): CMC, ("num", 2): GEO})
        E2, e2 = M("M", r"\vec A_{cm}", "=", r"\vec F^{\,ext}", size=56, cores={1: FC, 3: FC})
        E1.move_to(P3(4.0, 1.25))
        E2.move_to(P3(4.0, -0.75))
        G1 = lambda *ks: gl(E1, [j for kk in ks for j in kk])
        self._em_troca = True                                                                        # G13: troca sequencial (o instante vazio é a troca)
        self.play(FadeOut(VGroup(tt, sub, nv, itens)), FadeIn(faixa, shift=0.1 * DOWN), g.f3d.op.animate.set_value(1.0), FadeIn(caixa_c), Create(par), run_time=0.7)   # v5 G32: entra enquanto sai (cruzamento, sem quadro vazio)
        self._em_troca = False
        self.play(FadeIn(cmv), FadeIn(G1(e1["pre"][0], e1["pre"][1])), g.tau.animate(rate_func=linear).set_value(1.2), run_time=1.0)
        self.gat("média das posições")
        self.play(FadeIn(G1(e1["num"][0], e1["num"][2], e1["bar"])), g.tau.animate(rate_func=linear).set_value(2.0), run_time=0.9)   # "média das posições"
        self.gat("pesada pelas massas")
        self.play(FadeIn(G1(e1["num"][1], e1["den"][0])), g.tau.animate(rate_func=linear).set_value(2.8), run_time=0.9)        # "pesada pelas massas"
        self.foco = E1
        self.gat("se move")
        self.play(FadeIn(mp(E2, e2, [0, 1])), g.tau.animate(rate_func=linear).set_value(3.1), run_time=0.8)                    # v4 §8: M A⃗_cm entra em "se move"
        self.gat("forças de fora", mov=(g.tau, 4.0, Indicate(mp(E2, e2, [0, 1]), color=WHITE_, scale_factor=1.1)))   # PAUSAS: o termo que chegou pulsa
        self.play(FadeIn(mp(E2, e2, [2, 3])), g.tau.animate(rate_func=linear).set_value(g.TE + 0.4), run_time=0.9)              # "forças de fora"
        self.foco = E2
        tauF = g.ttoque[1] - 0.15
        self.ate_mov(0.9, g.tau, tauF)
        cmv.clear_updaters()
        self.ate(0.97)
        # ── A4: as três perguntas; depois saem de cena ──
        self.an("A4")
        velhos = self.snap()
        ck = Checklist.grande().move_to(P3(0, 0.1))
        tit = txt("ANTES DE QUALQUER CONTA", 30, op=0.85).move_to(P3(0, 2.4))
        self.troca(velhos, FadeIn(tit), FadeIn(ck[0], shift=0.15 * RIGHT), seq=True)
        self.foco = ck[0][0]           # a primeira pergunta entra com o título (palco); o ícone dela pulsa
        for k, f_ in enumerate((0.3, 0.5)):
            self.ate(f_)
            self.play(FadeIn(ck[k + 1], shift=0.15 * RIGHT), run_time=0.6)
        self.foco = ck[2][0]
        self.ate(0.72)
        nota = txt("A CONTA QUE VEM DEPOIS É CURTA", 30, bold=True).move_to(P3(0, -2.4))
        self.play(FadeIn(nota, shift=0.1 * UP), run_time=0.6)
        self.ate(0.96)
        from sec_x01 import miniatura_x0
        mini = miniatura_x0()
        self._em_troca = True                                                                       # a lista sai e só então o disco entra (sem um sobre o outro)
        self.play(FadeOut(VGroup(tit, ck, nota)), run_time=0.25)
        self.play(FadeIn(mini), run_time=0.25)                                                      # v3 §9: o disco do X0-1 já nasce aqui (sobreposição com o PX0)
        self._em_troca = False
