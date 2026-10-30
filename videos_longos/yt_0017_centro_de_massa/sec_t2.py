"""Lote P2 (handoff v3 do lote 1, visual novo): T2 — como ele se move? (⊕ e rastro do ⊕ em degradê; rastros finos aço-azulados)
T2-1 haltere jogado girando: a câmera segue o ⊕ e depois recua (rastro branco do ⊕ × laços cinza); r⃗ᵢ = R⃗_cm + r⃗ᵢ′ desenhado e na CONTA ·
T2-2 haltere maior (câmera no ⊕), velocidades; M R⃗_cm = Σ mᵢ r⃗ᵢ → d/dt (M e mᵢ não mudam) → M V⃗_cm = Σ mᵢ dr⃗ᵢ/dt = Σ mᵢ v⃗ᵢ → V⃗_cm ·
T2-3 o M atravessa; mᵢv⃗ᵢ somam P⃗ no ⊕; P⃗ = M V⃗_cm · T2-4 massas com molas, o conjunto deslizando e vibrando, ⊕ reto; os pares de ação e
reação escritos um a um (= 0⃗, 3ª LEI) → M A⃗_cm = F⃗_ext · T2-5 o dP/dt = F_ext do A4 volta; ONDE? → ⊕ · T2-6 explosão no espaço (3D) ·
T2-7 granada (3D): M g, o M cancela, R⃗_cm(t) = R⃗₀ + V⃗₀ t + ½ g⃗ t²; a resposta do hook · T2-8 o primeiro toque; painel J⃗ → ΔV⃗_cm ·
T2-9 gelo: X_cm = 4 m, F_ext = 0 e V_cm = 0 ⇒ X_cm fixo; Cyrano (DICA). Cores por grandeza (G12); caixas PANEL (G11)."""
from MF_Tools import TransformByGlyphMap

from camadas import *  # noqa: F401,F403

# haltere jogado (metros, s): CM lançado com (4; 11) m/s, giro ω = 3 rad/s; braços 3 m (1 kg) e 1 m (3 kg)
VC0, GT, WG = np.array([4.0, 11.0]), 9.8, 3.0
TV = 2 * VC0[1] / GT
M1, M2 = 1.0, 3.0
RB1, RB2 = 0.8 * (M1 / 3) ** (1 / 3), 0.8 * (M2 / 3) ** (1 / 3)
SVH = 0.08                               # Manim por m/s (velocidades do haltere; escala comum que cabe no PALCO)
SPH = 0.03                               # Manim por kg·m/s (momentos do haltere)


def hal_fis(t):
    """⊕, bola leve, bola pesada e as velocidades (metros, m/s) no instante t do voo."""
    cm = VC0 * t + np.array([0, -0.5 * GT * t * t])
    vc = VC0 + np.array([0, -GT * t])
    a = WG * t + 0.4
    u, du = np.array([math.cos(a), math.sin(a)]), WG * np.array([-math.sin(a), math.cos(a)])
    return cm, cm - 3 * u, cm + 1 * u, vc, vc - 3 * du, vc + du


def mp(m, idx, partes):
    return VGroup(*[m[0][j] for k in partes for j in idx[k]])


J = lambda idx, *ks: [j for k in ks for j in idx[k]]


class LoteT2(Camadas):
    def construct(self):
        self.setup_base(cap="COMO ELE SE MOVE?")
        self.t2_1()
        self.t2_2_3()
        self.t2_4_5()
        self.t2_6()
        self.t2_7_8()
        self.t2_9()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    # ── T2-1, T2-2, T2-3: haltere jogado ────────────────────────────────────────────────────────────────
    def _hal_tela(self):
        """Câmera do haltere: segue o ⊕ (seg = 1, zoom fechado `S0`) → laboratório (seg = 0, voo inteiro centrado no PALCO)."""
        H = VC0[1] ** 2 / (2 * GT)
        fix = np.array([VC0[0] * TV / 2, 0.5 * H])
        S1 = 0.45
        anc = P3(PALCO_C[0], -0.35)

        def tela(p, t):
            s = self.h_seg.get_value()
            S0 = self.h_zoom.get_value()
            cm = hal_fis(t)[0]
            ref = s * cm + (1 - s) * fix
            k = S1 + (S0 - S1) * s
            return anc + k * P3(*(p - ref)), k
        return tela

    def t2_1(self):
        self.an("T2-1")
        tr = [ValueTracker(v) for v in (0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.62, 0.0)]
        self.h_t, self.h_seg, self.h_tr, self.h_v, self.h_p, self.h_soma, self.h_zoom, self.h_dec = tr
        self.add(*tr)
        tela = self.tela = self._hal_tela()
        self.mem_lab = {}

        def cena():
            t = self.h_t.get_value()
            cm, b1, b2, vc, v1, v2 = hal_fis(t)
            P = lambda p: tela(p, t)[0]
            k = tela(cm, t)[1]
            g = VGroup()
            tr_ = self.h_tr.get_value()
            if tr_ > 0.01:
                ts = np.linspace(0, t, max(2, int(t * 40)))
                F = [hal_fis(s) for s in ts]
                g.add(VMobject().set_points_as_corners([P(f[1]) for f in F]).set_stroke(RAST, 2, opacity=0.7 * tr_),
                      VMobject().set_points_as_corners([P(f[2]) for f in F]).set_stroke(RAST, 2, opacity=0.7 * tr_))
            pb1, pb2 = P(b1), P(b2)
            g.add(Line(pb1, pb2).set_stroke(GEO, max(2.0, 9 * k)))
            g.add(esfera2d(RB1 * k).move_to(pb1), esfera2d(RB2 * k).move_to(pb2))
            if tr_ > 0.01:
                g.add(rastro_cm([P(f[0]) for f in F], w=5, op=tr_))
            pc = P(cm)
            od = self.h_dec.get_value()
            if od > 0.01:                                            # r⃗ᵢ = R⃗_cm + r⃗ᵢ′ (bola leve): R⃗_cm da origem ao ⊕, r⃗ᵢ′ do ⊕ à bola
                o0 = P(np.zeros(2))
                g.add(seta(o0, da_borda(pc, o0 - pc, 0.26), CMC, 5, tip=0.22, op=od),
                      seta(da_borda(pc, pb1 - pc, 0.26), da_borda(pb1, pc - pb1, RB1 * k), mix(GEO, 0.45), 5, tip=0.22, op=od),
                      Dot(o0, radius=0.06, color=GEO).set_opacity(od))
            ov = self.h_v.get_value()
            if ov > 0.01:
                for pb, v, r in ((pb1, v1, RB1 * k), (pb2, v2, RB2 * k)):
                    a = da_borda(pb, P3(*v), r)
                    g.add(seta(a, a + P3(*v) * SVH, VEL, 5, tip=0.2, op=ov))
                a = da_borda(pc, P3(*vc), 0.27)
                ub = pb2 - pc
                lado = P3(-vc[1], vc[0])
                lado = lado / (np.linalg.norm(lado) + 1e-9)
                if lado @ ub > 0:                                      # rótulo do lado oposto às bolas
                    lado = -lado
                fimv = a + P3(*vc) * SVH
                uv = P3(*vc) / (np.linalg.norm(vc) + 1e-9)
                lv = mtex(r"\vec V_{cm}", VEL, 38)
                cands = [fimv + uv * d_ for d_ in (0.45, 0.7)] + [m_ + s_ * lado * d_ for d_ in (0.45, 0.7, 1.0) for s_ in (1, -1) for m_ in (fimv, (a + fimv) / 2)]
                pts_ = amostra(pb1, pb2) + amostra(a, fimv)
                for pb, v, r in ((pb1, v1, RB1 * k), (pb2, v2, RB2 * k)):
                    a_ = da_borda(pb, P3(*v), r)
                    pts_ += amostra(a_, a_ + P3(*v) * SVH)
                lv.move_to(lugar_livre(lv, cands, [(pb1, RB1 * k), (pb2, RB2 * k), (pc, 0.27)], pts_, self.mem_lab, "vcm"))
                g.add(seta(a, fimv, VEL, 8, tip=0.26, op=ov).set_z_index(30), lv.set_opacity(ov))
            op_ = self.h_p.get_value()
            if op_ > 0.01:
                u = suave(self.h_soma.get_value())
                vecs = [P3(*(M1 * v1)) * SPH, P3(*(M2 * v2)) * SPH]
                cad0 = da_borda(pc, P3(*vc), 0.27)
                ini = [da_borda(pb1, vecs[0], RB1 * k), da_borda(pb2, vecs[1], RB2 * k)]
                fim = [cad0, cad0 + vecs[0]]
                for v_, a0, a1 in zip(vecs, ini, fim):
                    a = (1 - u) * a0 + u * a1
                    g.add(seta(a, a + v_, MAG, 5, tip=0.2, op=op_))
                if u > 0.98:
                    pt = cad0 + P3(*((M1 + M2) * vc)) * SPH
                    lado = P3(-vc[1], vc[0]) / (np.linalg.norm(vc) + 1e-9)
                    if lado @ (pb2 - pc) > 0:
                        lado = -lado
                    g.add(seta(cad0, pt, MAG, 8, tip=0.24, op=0.5 * op_),
                          mtex(r"\vec P", MAG, 40).set_opacity(op_).move_to(pt + lado * 0.4))
                    self.p_ponta = pt + lado * 0.4
            self.reg("hal2d", cm=pc)
            return g.set_z_index(6)
        self.hv = vivo(cena)
        self.hcm = vivo(lambda: marcador_cm(tela(hal_fis(self.h_t.get_value())[0], self.h_t.get_value())[0]).set_z_index(40))   # ⊕ sempre por cima
        self.add(self.hv, self.hcm)                              # o lote abre com o haltere em cena (G5)
        selo = txt("CÂMERA ACOMPANHANDO O CENTRO DE MASSA", 24, color=DIM, op=0.95).move_to(P3(PALCO_C[0], -3.0))
        self.play(FadeIn(selo), self.h_t.animate(rate_func=linear).set_value(0.7), run_time=2.4)
        self.ate(0.18)
        self.play(self.h_t.animate(rate_func=linear).set_value(0.8), run_time=0.6)
        # a revelação: a câmera recua e aparecem a parábola do ⊕ (branca) e os laços das bolas (cinza)
        self.play(self.h_seg.animate.set_value(0.0), self.h_tr.animate.set_value(1.0), FadeOut(selo),
                  self.h_t.animate(rate_func=linear).set_value(1.3), run_time=2.4)
        self.ate_mov(0.58, self.h_t, TV)                              # devagar até os rótulos (sem tela parada)
        H = VC0[1] ** 2 / (2 * GT)
        topo = tela(np.array([VC0[0] * TV / 2, H]), TV)[0]
        cfim = tela(hal_fis(TV)[0], TV)[0]
        l1 = VGroup(txt("TRANSLAÇÃO DO", 26), marcador_cm(r=0.14)).arrange(RIGHT, buff=0.14)
        lacos = [tela(f[q], TV)[0] for f in (hal_fis(s) for s in np.linspace(0, TV, 160)) for q in (0, 1, 2)]
        l1.move_to(lugar_livre(l1, [topo + P3(dx_, dy_) for dy_ in (1.35, 1.0, 0.6) for dx_ in (0.0, 2.4, 3.0, -2.6)], [(cfim, 1.0)], lacos))
        d1 = topo - l1.get_center()
        e1 = l1.get_center() + d1 * min(l1.width / 2 / (abs(d1[0]) + 1e-9), l1.height / 2 / (abs(d1[1]) + 1e-9)) * 1.12   # sai da borda da caixa
        g1 = Line(e1, topo - 0.12 * d1 / np.linalg.norm(d1)).set_stroke(WHITE_, 1.4, opacity=0.7)
        arco = Arc(radius=0.55, start_angle=-0.2, angle=2.3, arc_center=cfim).set_stroke(GEO, 3).add_tip(tip_length=0.16)
        l2 = VGroup(txt("ROTAÇÃO EM TORNO DO", 26), marcador_cm(r=0.14)).arrange(RIGHT, buff=0.14).move_to(cfim + P3(0.6, -1.75))
        g2 = Line(l2.get_top() + 0.06 * UP, cfim + P3(-0.25, -0.5)).set_stroke(WHITE_, 1.4, opacity=0.7)
        self.ate(0.6)
        self.play(FadeIn(l1, shift=0.1 * UP), Create(g1), run_time=0.6)
        self.ate(0.68)
        self.play(FadeIn(l2, shift=0.1 * UP), Create(g2), Create(arco), run_time=0.7)
        # "a posição de cada bola é a posição do centro de massa mais uma seta que só gira em volta dele"
        self.ate(0.78)
        self.play(FadeOut(VGroup(l1, g1, l2, g2, arco)), self.h_dec.animate.set_value(1.0), self.h_tr.animate.set_value(0.35), run_time=0.7)
        self.h_t.set_value(0.0)
        R_ = mtex(r"\vec R_{cm}", CMC, 40)
        r_ = MathTex(r"\vec r_i'", font_size=40, color=mix(GEO, 0.45))
        def rot_dec():
            t = self.h_t.get_value()
            cm, b1 = hal_fis(t)[0], hal_fis(t)[1]
            pc, pb, o0 = tela(cm, t)[0], tela(b1, t)[0], tela(np.zeros(2), t)[0]
            k = tela(cm, t)[1]
            b2 = tela(hal_fis(t)[2], t)[0]
            n = P3(-(pc - o0)[1], (pc - o0)[0]) / (np.linalg.norm(pc - o0) + 1e-9)
            nr = P3(-(pb - pc)[1], (pb - pc)[0]) / (np.linalg.norm(pb - pc) + 1e-9)
            ur = (pb - pc) / (np.linalg.norm(pb - pc) + 1e-9)
            circ = [(pb, RB1 * k), (b2, RB2 * k), (pc, 0.27), (o0, 0.08)]
            pts_ = amostra(o0, pc, 20) + amostra(pc, pb) + amostra(pb, b2)
            if self.h_tr.get_value() > 0.01:                       # os laços e a parábola (apagados, mas visíveis)
                pts_ += [tela(f[q], t)[0] for f in (hal_fis(s) for s in np.linspace(0, t, max(2, int(t * 12)))) for q in (0, 1, 2)]
            rr = r_.copy()
            m_ = (pc + pb) / 2
            em_volta = [pb + P3(np.cos(a_), np.sin(a_)) * (RB1 * k + 0.4) for a_ in np.linspace(0, 2 * np.pi, 12, endpoint=False)]   # perto da ponta de r⃗ᵢ′
            rr.move_to(lugar_livre(rr, [m_ + s_ * nr * d_ for d_ in (0.4, 0.6) for s_ in (1, -1)] + [pb + ur * (RB1 * k + 0.35)] + em_volta,
                                   circ, pts_, self.mem_lab, "rl"))
            RR = R_.copy()
            RR.move_to(lugar_livre(RR, [o0 + (pc - o0) * f_ + s_ * n * d_ for d_ in (0.4, 0.65) for f_ in (0.5, 0.35, 0.65, 0.2, 0.8) for s_ in (-1, 1)],
                                   circ + [(rr.get_center(), max(rr.width, rr.height) / 2)], pts_, self.mem_lab, "R"))   # sempre ao lado da própria seta
            g = VGroup(RR, rr, self.leg_rel.copy())
            return g.set_opacity(self.h_dec.get_value())
        self.leg_rel = VGroup(r_.copy(), txt("EM RELAÇÃO AO", 24, color=mix(GEO, 0.45)), marcador_cm(r=0.12)).arrange(RIGHT, buff=0.14)   # legenda fixa, na conta
        na_conta(self.leg_rel, -0.4)
        self.dec_lab = vivo(rot_dec)
        self.add(self.dec_lab)
        E, ie = eqp(r"\vec r_i", "=", r"\vec R_{cm}", "+", r"\vec r_i'", size=56, cores={0: GEO, 2: CMC, 4: mix(GEO, 0.45)})
        na_conta(E, 0.6)
        lab = self.dec_lab.submobjects[0]
        self.play(TransformFromCopy(lab[0].copy(), mp(E, ie, [2])), TransformFromCopy(lab[1].copy(), mp(E, ie, [4])), FadeIn(mp(E, ie, [0, 1, 3])),
                  self.h_t.animate(rate_func=linear).set_value(0.35), run_time=1.2)
        self._loop(0.97)
        self.E21 = E

    def _loop(self, ate_frac):
        """Repete o voo devagar (0,3×) até a fração da âncora; o rastro recomeça a cada volta."""
        while True:
            falta = (self._q0 + ate_frac * (self.alvo - self._q0) - self.nq) / FPS
            if falta < 0.7:
                return
            t = self.h_t.get_value()
            if t >= TV - 1e-3:
                self.h_t.set_value(0.0)
                t = 0.0
            dt = min(TV - t, 0.3 * falta)
            self.play(self.h_t.animate(rate_func=linear).set_value(t + dt), run_time=dt / 0.3)

    def t2_2_3(self):
        self.an("T2-2")
        # haltere maior (a câmera volta a acompanhar o ⊕) e as velocidades
        self.dec_lab.clear_updaters()
        self.play(FadeOut(self.E21), FadeOut(self.dec_lab), self.h_dec.animate.set_value(0.0), self.h_tr.animate.set_value(0.0),
                  self.h_seg.animate.set_value(1.0), self.h_zoom.animate.set_value(0.62), self.h_v.animate.set_value(1.0), run_time=1.0)
        self.remove(self.dec_lab)
        G = GEO
        A, ia = eqp("M", r"\vec R_{cm}", "=", r"\sum_i", "m_i", r"\vec r_i", size=52, cores={1: CMC, 5: G})
        na_conta(A, 2.45)
        self.play(FadeIn(A), run_time=0.6)
        dd = VGroup(MathTex(r"\frac{d}{dt}", font_size=44, color=DIM),
                    VGroup(MathTex("M", font_size=42, color=DIM), txt("E", 30, color=DIM), MathTex("m_i", font_size=42, color=DIM),
                           txt("NÃO MUDAM", 30, color=DIM)).arrange(RIGHT, buff=0.14)).arrange(RIGHT, buff=0.3)
        na_conta(dd, 1.45)
        self._loop(0.18)
        self.play(FadeIn(dd, shift=0.1 * DOWN), run_time=0.6)                           # "como as massas não mudam"
        B, ib = eqp("M", r"\vec V_{cm}", "=", r"\sum_i", "m_i", r"\frac{d\vec r_i}{dt}", size=52, cores={1: VEL})
        na_conta(B, 0.3)
        fr_ = ib[5]                                                                    # d, (vec r i), barra, d, t
        for j in fr_[1:4]:
            B[0][j].set_color(G)
        self._loop(0.32)
        # "a derivada passa para dentro da soma": o d/dt do rótulo entra na fração; o mᵢ fica parado (brilha)
        self.play(Indicate(dd[0], color=WHITE_, scale_factor=1.2), run_time=0.5)
        self.play(TransformByGlyphMap(A.copy(), B, (J(ia, 0), J(ib, 0)), (J(ia, 1), J(ib, 1)), (J(ia, 2), J(ib, 2)), (J(ia, 3), J(ib, 3)),
                                      (J(ia, 4), J(ib, 4)), (J(ia, 5), fr_[1:4]), ([], [fr_[0], fr_[4], fr_[5], fr_[6]]), auto_fade=True), run_time=1.4)
        self.play(Indicate(mp(B, ib, [4]), color=WHITE_, scale_factor=1.25), run_time=0.4)
        B2, i2 = eqp("M", r"\vec V_{cm}", "=", r"\sum_i", "m_i", r"\vec v_i", size=52, cores={1: VEL, 5: VEL})
        na_conta(B2, -1.0)
        self._loop(0.5)
        self.play(TransformByGlyphMap(B.copy(), B2, *[(J(ib, k), J(i2, k)) for k in range(5)], (fr_[1:4], J(i2, 5)),
                                      ([fr_[0], fr_[4], fr_[5], fr_[6]], []), auto_fade=True), run_time=1.2)
        self.play(Indicate(mp(B2, i2, [5]), color=VEL, scale_factor=1.2), run_time=0.5)    # dr⃗ᵢ/dt → v⃗ᵢ
        C, ic = eqp(r"\vec V_{cm}", "=", r"\frac{\sum_i m_i\vec v_i}{M}", size=52, cores={0: VEL})
        for j in (9, 10, 11):
            C[0][j].set_color(VEL)
        na_conta(C, -2.4)
        self._loop(0.72)
        self.play(TransformByGlyphMap(B2.copy(), C, (J(i2, 0), [13]), (J(i2, 1), J(ic, 0)), (J(i2, 2), J(ic, 1)), (J(i2, 3, 4, 5), [5, 6, 7, 8, 9, 10, 11]),
                                      ([], [12]), auto_fade=True), run_time=1.3)
        self._loop(0.97)
        # T2-3 — o M atravessa de volta; m_i v_i é o momento total; = P (da seta P do ⊕); caixa magenta
        self.an("T2-3")
        self.play(FadeOut(VGroup(A, dd, B, B2)), C.animate.move_to(P3(XC0 + C.width / 2, 2.0)), run_time=0.7)
        D, idd = eqp("M", r"\vec V_{cm}", "=", r"\sum_i", r"m_i\vec v_i", size=54, cores={1: VEL, 4: MAG})
        na_conta(D, 0.55)
        self.ate(0.08)
        self.play(TransformByGlyphMap(C.copy(), D, ([13], J(idd, 0)), (J(ic, 0), J(idd, 1)), (J(ic, 1), J(idd, 2)), ([5, 6], J(idd, 3)),
                                      ([7, 8, 9, 10, 11], J(idd, 4)), ([12], []), auto_fade=True), run_time=1.6)   # "massa total vezes a velocidade"
        self.play(self.h_v.animate.set_value(0.0), self.h_p.animate.set_value(1.0), run_time=0.8)
        self._loop(0.42)
        self.play(self.h_soma.animate.set_value(1.0), run_time=1.2)
        Dq = Mc("=", (r"\vec P", MAG), size=54).next_to(D, RIGHT, buff=0.18)
        pP = mtex(r"\vec P", MAG, 40).move_to(getattr(self, "p_ponta", CONTA_C))
        self.play(TransformFromCopy(pP, Dq[1]), FadeIn(Dq[0]), run_time=0.9)
        cx_ = Mc((r"\vec P", MAG), "=", "M", (r"\vec V_{cm}", VEL), size=60)
        na_conta(cx_, -1.1)
        bx = caixa(cx_, cor=MAG)
        self._loop(0.62)
        self.play(FadeIn(cx_, shift=0.1 * DOWN), FadeIn(bx), run_time=0.9)
        self._loop(0.97)
        self.hv.clear_updaters(); self.hcm.clear_updaters()
        self.c23 = VGroup(C, D, Dq, cx_, bx, self.hv, self.hcm)

    # ── T2-4, T2-5: massas com molas; ação e reação, par por par ─────────────────────────────────────────
    def t2_4_5(self):
        self.an("T2-4")
        t0 = self.clk.get_value()
        base = [P3(-2.0, -1.1), P3(2.0, -1.1), P3(0.0, 2.2)]          # centróide na origem: o ⊕ é o ponto de referência
        un = [b / np.linalg.norm(b) for b in base]
        amp = [0.32 * un[0], 0.32 * un[1], 0.32 * 0.964 * un[2]]     # modo de "respiração": Σ aᵢ = 0, o ⊕ não oscila
        c0, vd = P3(-4.95, -0.05), P3(0.065, 0.0)                     # o conjunto desliza para a direita (~40% do PALCO no bloco)
        PARES = ((0, 1), (0, 2), (1, 2))
        self.mbr = [ValueTracker(0.0) for _ in range(3)]
        self.add(*self.mbr)

        def pos(t):
            s = math.sin(2 * PI * t / 1.3)
            cm = c0 + vd * t
            return [cm + b + a * s for b, a in zip(base, amp)], cm

        def molas():
            t = self.clk.get_value() - t0
            ps, cm = pos(t)
            g = VGroup()
            ts = np.linspace(max(0.0, t - 3.0), t, 40)
            hist = [pos(s) for s in ts]
            for i in range(3):
                g.add(VMobject().set_points_as_corners([h_[0][i] for h_ in hist]).set_stroke(RAST, 2, opacity=0.7))
            g.add(rastro_cm([h_[1] for h_ in hist], w=5, op=0.95))
            for k, (i, j) in enumerate(PARES):
                br = self.mbr[k].get_value()
                cor = interpolate_color(ManimColor(GEO), ManimColor(FC), br).to_hex()
                a_, b_ = ps[i], ps[j]
                d = (b_ - a_) / np.linalg.norm(b_ - a_)
                g.add(mola(a_ + d * 0.45, b_ - d * 0.45, n=8, amp=0.13, cor=cor, w=3))
                if br > 0.01:                                         # ação e reação: da borda das bolas, 0,15 para fora da mola
                    n_ = P3(-d[1], d[0])
                    if n_ @ ((a_ + b_) / 2 - cm) < 0:
                        n_ = -n_
                    o_ = n_ * 0.3
                    g.add(seta(a_ + d * 0.46 + o_, a_ + d * 1.3 + o_, FC, 6, tip=0.22, op=br), seta(b_ - d * 0.46 + o_, b_ - d * 1.3 + o_, FC, 6, tip=0.22, op=br))
            for p in ps:
                g.add(esfera2d(0.45).move_to(p))
            g.add(marcador_cm(cm))
            self.reg("molas", cm=cm)
            return g
        self.mv = vivo(molas)
        velhos = [self.c23, self.h_t, self.h_seg, self.h_tr, self.h_v, self.h_p, self.h_soma, self.h_zoom, self.h_dec]
        E1, i1 = eqp("M", r"\vec A_{cm}", "=", r"\sum_i", r"m_i\vec a_i", size=48)
        na_conta(E1, 2.5)
        self.troca(velhos, FadeIn(self.mv), FadeIn(E1), seq=True)
        E1b, ib = eqp("=", r"\sum_i", r"\Big(", r"\vec F_i^{\,ext}", "+", r"\sum_j", r"\vec F_{i(j)}", r"\Big)", size=48, cores={3: FC, 6: FC})
        E1b.move_to(P3(XC0 + 0.55 + E1b.width / 2, 1.2))
        self.ate(0.3)
        self.play(TransformFromCopy(mp(E1, i1, [2]), mp(E1b, ib, [0])), FadeIn(mp(E1b, ib, range(1, 8))), run_time=1.0)
        # "As internas vêm em pares de ação e reação": a mola acende, as duas setas aparecem e o par nasce na conta delas
        lugares = [0.3, -0.45, -1.2]
        zeros = []

        def rotulos(k):
            t = self.clk.get_value() - t0
            ps, cm = pos(t)
            i, j = PARES[k]
            d = (ps[j] - ps[i]) / np.linalg.norm(ps[j] - ps[i])
            n_ = P3(-d[1], d[0])
            if n_ @ ((ps[i] + ps[j]) / 2 - cm) < 0:
                n_ = -n_
            li = MathTex(rf"\vec F_{{{j + 1}({i + 1})}}", font_size=36, color=FC)
            lj = MathTex(rf"\vec F_{{{i + 1}({j + 1})}}", font_size=36, color=FC)
            s_ = li.width / 2 * abs(n_[0]) + li.height / 2 * abs(n_[1])            # meia largura da caixa na direção normal
            li.move_to(ps[i] + d * 0.9 + n_ * (0.72 + s_))
            lj.move_to(ps[j] - d * 0.9 + n_ * (0.72 + s_))
            return li, lj
        self.ate(0.5)
        selo3 = None
        for k, (i, j) in enumerate(PARES):
            li, lj = rotulos(k)
            par, ip = eqp("+" if k else "", "(", rf"\vec F_{{{i + 1}({j + 1})}}", "+", rf"\vec F_{{{j + 1}({i + 1})}}", ")", size=46, cores={2: FC, 4: FC})
            par.move_to(P3(XC0 + 0.55 + par.width / 2, lugares[k]))
            z0, iz = eqp("=", r"\vec 0", size=46)
            z0.next_to(par, RIGHT, buff=0.18)
            self.play(self.mbr[k].animate.set_value(1.0), FadeIn(li), FadeIn(lj), run_time=0.35)           # a mola k acende
            if AUDITORIA and (self.mbr[k].get_value() < 0.99 or any(self.mbr[q].get_value() > 0.01 for q in range(3) if q != k)):
                print(f"[audit] {self.t:7.1f}s PAR FORA DE SINCRONIA mola {PARES[k]}")
            self.play(TransformFromCopy(lj, mp(par, ip, [2])), TransformFromCopy(li, mp(par, ip, [4])), FadeIn(mp(par, ip, [0, 1, 3, 5])),
                      FadeOut(li), FadeOut(lj), run_time=0.55)                                               # a linha k nasce no mesmo instante
            self.play(FadeIn(z0, shift=0.1 * LEFT), self.mbr[k].animate.set_value(0.0), run_time=0.35)       # = 0⃗ com a mola apagando
            if k == 0:
                selo3 = txt("3ª LEI", 30, color=FC).next_to(z0, RIGHT, buff=0.25)
                self.play(FadeIn(selo3), run_time=0.3)
            zeros.append((par, z0, iz))
        # "cada par dá zero": os três 0⃗ se juntam em um e somem com o "+"
        Lz, iL = eqp("=", r"\vec F^{\,ext}", "+", r"\vec 0", "+", r"\vec 0", "+", r"\vec 0", size=48, cores={1: FC})
        Lz.move_to(P3(XC0 + 0.55 + Lz.width / 2, -2.05))
        self.ate(0.78)
        self.play(FadeIn(mp(Lz, iL, [0, 1, 2, 4, 6])), *[TransformFromCopy(mp(z0, iz, [1]), mp(Lz, iL, [3 + 2 * k])) for k, (_, z0, iz) in enumerate(zeros)],
                  VGroup(*[VGroup(p_, z_) for p_, z_, _ in zeros], selo3).animate.set_opacity(OP_FUNDO), run_time=0.9)
        Lz1, i1z = eqp("=", r"\vec F^{\,ext}", "+", r"\vec 0", size=48, cores={1: FC})
        Lz1.move_to(Lz, aligned_edge=LEFT)
        self.play(TransformByGlyphMap(Lz, Lz1, (J(iL, 0, 1, 2), J(i1z, 0, 1, 2)), (J(iL, 3, 5, 7), J(i1z, 3)), (J(iL, 4, 6), [])), run_time=0.9)
        Lz2, i2z = eqp("=", r"\vec F^{\,ext}", size=48, cores={1: FC})
        Lz2.move_to(Lz1, aligned_edge=LEFT)
        self.play(TransformByGlyphMap(Lz1, Lz2, (J(i1z, 0, 1), J(i2z, 0, 1)), (J(i1z, 2, 3), [])), run_time=0.9)
        E3, i3 = eqp("M", r"\vec A_{cm}", "=", r"\vec F^{\,ext}", size=60, cores={3: FC})
        na_conta(E3, -3.05)
        bx = caixa(E3, cor=FC)
        self.ate(0.88)
        self.play(TransformFromCopy(VGroup(mp(E1, i1, [0, 1, 2]), mp(Lz2, i2z, [1])), E3[0]), FadeIn(bx), run_time=1.0)
        self.ate(0.97)
        # T2-5 — é o mesmo dP/dt = F_ext do A4 (volta da mesma posição e tamanho); ONDE? vira o ⊕
        self.an("T2-5")
        extras = VGroup(E1, E1b, *[VGroup(p_, z_) for p_, z_, _ in zeros], selo3, Lz2)
        self.play(FadeOut(extras), VGroup(E3, bx).animate.move_to(P3(4.25, 0.55)), run_time=0.8)
        velha = Mc((r"\frac{d\vec P}{dt}", MAG), "=", (r"\vec F^{\,ext}", FC), size=46).move_to(P3(5.45, 2.55))
        q = VGroup(txt("ONDE", 32, bold=True), mtex("?", WHITE_, 56)).arrange(RIGHT, buff=0.08).next_to(velha, LEFT, buff=0.45)   # como no A4
        self.play(FadeIn(velha), FadeIn(q), run_time=0.6)
        selo = VGroup(txt("É O MESMO", 28), velha.copy().scale(40 / 46), txt(", AGORA COM UM LUGAR", 28)).arrange(RIGHT, buff=0.18)
        selo.move_to(P3(0, -2.75))
        self.ate(0.25)
        self.play(FadeIn(selo, shift=0.1 * UP), run_time=0.7)
        lug = marcador_cm(q.get_center(), r=0.22)
        self.ate(0.42)
        self.play(ReplacementTransform(q, lug), run_time=0.9)
        nt = txt("AS FORÇAS DE DENTRO NÃO CHEGAM AO CENTRO DE MASSA", 30, bold=True).move_to(P3(0, -3.55))
        self.ate(0.75)
        self.play(FadeIn(nt, shift=0.1 * UP), selo.animate.set_opacity(OP_FUNDO), run_time=0.7)
        self.ate(0.97)
        self.c45 = VGroup(E3, bx, velha, selo, lug, nt)

    # ── T2-6: explosão no espaço ────────────────────────────────────────────────────────────────────────
    def t2_6(self):
        self.an("T2-6")
        self.mv.clear_updaters()
        velhos = [self.c45, self.mv, *self.mbr]
        E, ie = eqp(r"\vec F^{\,ext}", "=", r"\vec 0", size=52, cores={0: FC})
        na_conta(E, 1.9)
        l2 = VGroup(MathTex(r"\Rightarrow\;\vec V_{cm}", font_size=52, color=WHITE_), txt("CONSTANTE", 30, bold=True)).arrange(RIGHT, buff=0.2)
        l2[0][0][1:].set_color(VEL)
        na_conta(l2, 0.95)
        self.explosao_chao_momento(frac=self.ate, velhos=velhos, eq=(E, ie[2], [l2]))
        self.ate(0.97)

    # ── T2-7, T2-8: a granada ───────────────────────────────────────────────────────────────────────────
    def t2_7_8(self):
        self.an("T2-7")
        velhos = self.snap()
        g = self.nova_granada(cam=self.CAM_VOO, op=0.0, tau=self.T0_VOO)        # o campo de provas como gráfico: eixos, fotos, cotas
        g.fant.set_value(1.0)
        self.troca(velhos, g.f3d.op.animate.set_value(1.0), seq=True)
        par = self.g_par = self.parabola(g)
        cam0 = g.cam()
        c_l = g.m((0.0, 0.0), cam0)
        u_l = P3(0.6, 0.8)
        a0 = da_borda(c_l, u_l, g.r_tela() * 1.05)
        v0l = mtex(r"\vec V_0", VEL, 38).move_to(self.pos_v0(a0, self.SVL))                         # o mesmo lugar da camada
        self.g_extra = [VGroup(seta(a0, a0 + u_l * 50 * self.SVL, VEL, 6)), v0l]                      # o rótulo do peso desvia deles
        self.play(Create(par), self.g_eix.animate.set_value(1.0), self.g_lanc.animate.set_value(1.0), self.g_v0lab.animate.set_value(1.0),
                  self.g_ras.animate.set_value(1.0), run_time=1.0)
        self.play(g.tau.animate(rate_func=linear).set_value(0.6), self.g_cm.animate.set_value(1.0), self.g_cota.animate.set_value(1.0), run_time=1.0)
        self.ate(0.1)
        self.play(self.g_peso.animate.set_value(1.0), g.tau.animate(rate_func=linear).set_value(1.0), run_time=0.6)
        f1, if1 = eqp(r"\vec F^{\,ext}", "=", r"M\vec g", size=50, cores={0: FC, 2: FC})
        f1.move_to(P3(4.7, 3.1))
        c_ = g.cm()
        peso_lab = mtex(r"M\vec g", FC, 40).next_to(c_ + 0.85 * DOWN, RIGHT, buff=0.12)
        self.play(TransformFromCopy(peso_lab, mp(f1, if1, [2])), FadeIn(mp(f1, if1, [0, 1])), g.tau.animate(rate_func=linear).set_value(1.5), run_time=1.0)
        A, ia_ = eqp("M", r"\vec A_{cm}", "=", "M", r"\vec g", size=52, cores={4: FC})
        A.move_to(P3(4.7, 2.3))
        self.ate(0.22)
        self.play(FadeIn(A), g.tau.animate(rate_func=linear).set_value(1.9), run_time=0.9)
        riscos = VGroup(risco(mp(A, ia_, [0]), WHITE_, 3), risco(mp(A, ia_, [3]), WHITE_, 3))
        self.ate(0.3)
        self.play(Create(riscos), g.tau.animate(rate_func=linear).set_value(2.2), run_time=0.7)
        B, ib_ = eqp(r"\vec A_{cm}", "=", r"\vec g", size=60, cores={2: FC})
        B.move_to(A)
        self.play(TransformByGlyphMap(A, B, (ia_[0], []), (ia_[3], []), (ia_[1], ib_[0]), (ia_[2], ib_[1]), (ia_[4], ib_[2]), auto_fade=True),
                  FadeOut(riscos), g.tau.animate(rate_func=linear).set_value(2.6), run_time=1.4)
        # integrando duas vezes: R_cm(t) = R0 + V0 t + ½ g t² (g do g; R0 do ⊕ no lançamento; V0 da seta de lançamento)
        Rt, irt = eqp(r"\vec R_{cm}(t)", "=", r"\vec R_0", "+", r"\vec V_0\,t", "+", r"\tfrac{1}{2}", r"\vec g", r"\,t^2", size=48,
                      cores={0: CMC, 2: CMC, 4: VEL, 7: FC})
        Rt.move_to(P3(7.4 - Rt.width / 2, 1.45))
        marco0 = marcador_cm(c_l, r=0.16)
        self.ate(0.42)
        ts_ = np.linspace(g.tau.get_value(), 3.1, 5)
        self.play(FadeIn(mp(Rt, irt, [0, 1])), g.tau.animate(rate_func=linear).set_value(ts_[1]), run_time=0.5)
        self.play(TransformFromCopy(marco0, mp(Rt, irt, [2])), g.tau.animate(rate_func=linear).set_value(ts_[2]), run_time=0.7)
        mp(Rt, irt, [2]).set_fill(CMC, 1).set_stroke(CMC, width=0)            # o R⃗₀ nasce do ⊕: fica ciano-claro (o degradê é só do ⊕)
        self.play(FadeIn(mp(Rt, irt, [3])), TransformFromCopy(v0l, mp(Rt, irt, [4])), g.tau.animate(rate_func=linear).set_value(ts_[3]), run_time=0.7)
        gpeso = mtex(r"\vec g", FC, 40).move_to(g.cm() + P3(0.75, -1.0))     # o g⃗ do rótulo do peso, no desenho
        self.play(FadeIn(mp(Rt, irt, [5, 6])), TransformFromCopy(gpeso, mp(Rt, irt, [7])), FadeIn(mp(Rt, irt, [8])),
                  g.tau.animate(rate_func=linear).set_value(ts_[4]), run_time=0.8)
        self.play(self.g_lanc.animate.set_value(0.0), g.tau.animate(rate_func=linear).set_value(g.TE), run_time=(g.TE - 3.1) / 0.5)
        self.g_extra = []
        self.play(g.tau.animate(rate_func=linear).set_value(g.TE + 0.25), run_time=1.0)
        self.play(g.tau.animate(rate_func=linear).set_value(g.ttoque[1] - 1.2), self.g_alc.animate.set_value(1.0),
                  run_time=(g.ttoque[1] - 1.2 - g.TE - 0.25) / 0.5)
        # de novo, desde o lançamento ("a mesma parábola que a granada inteira faria")
        self.play(g.f3d.op.animate.set_value(0.0), self.g_cm.animate.set_value(0.0), run_time=0.3)
        g.tau.set_value(self.T0_VOO)
        self.play(g.f3d.op.animate.set_value(1.0), self.g_cm.animate.set_value(1.0), run_time=0.3)
        self.ate_mov(0.87, g.tau, g.ttoque[1] - 1.2)
        resp = VGroup(txt("QUEM CONTINUA NA PARÁBOLA É O", 34, bold=True), marcador_cm(r=0.17)).arrange(RIGHT, buff=0.2)
        resp.move_to(P3(-1.9, 2.75)).set_z_index(30)
        self.play(FadeIn(resp, shift=0.1 * UP), VGroup(f1, B, Rt).animate.set_opacity(OP_FUNDO), self.g_pul.animate(rate_func=there_and_back).set_value(1.0),
                  g.tau.animate(rate_func=linear).set_value(g.ttoque[1] - 1.0), run_time=0.9)            # o pagamento do hook
        self.ate(0.97)
        # T2-8 — o primeiro toque
        self.an("T2-8")
        self.play(FadeOut(resp), FadeOut(VGroup(f1, B, Rt)), self.g_peso.animate.set_value(0.0), self.g_cota.animate.set_value(0.0), run_time=0.6)
        self.t28 = self.granada_toque(g, frac=self.ate, toque_em=0.36)
        self.ate(0.97)
        self.par = par

    # ── T2-9: duas pessoas no gelo; a conta; Cyrano ──────────────────────────────────────────────────────
    def t2_9(self):
        self.an("T2-9")
        velhos = self.snap()
        K, X0, YG = 0.61, -6.0, -1.9
        gl = gelo(-7.3, 0.4, YG)
        for k in range(3):                                         # reflexo no gelo
            gl.add(Line(P3(-6.8 + 2.3 * k, YG - 0.05), P3(-5.9 + 2.3 * k, YG - 0.05)).set_stroke(mix(GELO, 0.7), 2.5, opacity=0.55))
        u = ValueTracker(0.0)
        self.add(u)
        s_fim = 0.85                                               # param com as mãos se tocando (corpos sem se interpenetrar)

        PUXA = dict(cf=0.3, jf=0.08, ct=-0.3, jt=-0.1, bf=1.32, af=1.5, bt=1.18, at=1.45, tr=-0.14)   # pés afastados, corpo para trás

        def base(alt, sen, larg):                                 # G18: silhueta limpa de corpo inteiro (aço + recorte), feita uma vez
            p_ = PessoaPerfil(0.0, YG, alt, sen, PUXA)
            s_ = silhueta(p_)
            s_.stretch(larg, 0, about_point=P3(0, YG))
            s_.pts = {k_: P3(larg * v_[0], v_[1]) for k_, v_ in p_.pts.items()}
            r_ = s_.copy().flip(RIGHT, about_point=P3(0, YG)).set_fill(opacity=0.13).set_stroke(opacity=0)       # reflexo no gelo
            r_._degrade = "aco"
            return s_, r_
        PA, RA = base(2.15, 1, 1.25)                              # 60 kg: 1,1× mais alta e 1,25× mais larga
        PB, RB = base(1.95, -1, 1.0)

        def pessoa(s_, r_, x):
            a_, b_ = s_.copy().shift(x * RIGHT), r_.copy().shift(x * RIGHT)
            a_.pts = {k_: v_ + x * RIGHT for k_, v_ in s_.pts.items()}
            return a_, b_

        def gelo_cena():
            s = s_fim * suave(u.get_value())
            xa, xb = 0.0 + 4.0 * s, 10.0 - 6.0 * s
            pa, ra = pessoa(PA, RA, X0 + K * xa)
            pb, rb = pessoa(PB, RB, X0 + K * xb)
            corda = Line(pa.pts["mao_f"], pb.pts["mao_f"]).set_stroke(INT, 3.5)
            cm = (60 * xa + 40 * xb) / 100
            la = rot("60 kg", 30).next_to(pa.pts["cabeca"], LEFT, buff=0.35)
            lb = rot("40 kg", 30).next_to(pb.pts["cabeca"], RIGHT, buff=0.35)
            g = VGroup(ra, rb, corda, pa, pb, marcador_cm(P3(X0 + K * cm, YG + 1.2)),
                       DashedLine(P3(X0 + K * cm, YG), P3(X0 + K * cm, YG + 2.6), dash_length=0.09).set_stroke(WHITE_, 1.8, opacity=0.65), la, lb)
            self.reg("gelo", cm=P3(X0 + K * cm, YG + 1.2))
            return g
        gv = vivo(gelo_cena)
        d10 = cota(X0, X0 + K * 10, YG - 0.55, rot_cota("10 m"))
        self.troca(velhos, FadeIn(gl), FadeIn(gv), FadeIn(d10), seq=True)
        self.ate(0.1)                                                  # "o centro de massa fica parado para sempre"
        self.play(onda(P3(X0 + K * 4.0, YG + 1.2)), run_time=1.0)
        self.ate(0.19)                                                 # "a dez metros uma da outra"
        self.play(Indicate(d10, color=WHITE_, scale_factor=1.08), run_time=0.8)
        # a conta antes do Cyrano: X_cm = (60·0 + 40·10)/100 = 4 m; F_ext = 0 e V_cm = 0 ⇒ X_cm fixo
        Xc, ix = eqp(r"X_{cm}", "=", r"\frac{60\cdot 0+40\cdot 10}{100}", "=", r"4\ \mathrm{m}", size=46, cores={0: CMC, 4: CMC})
        na_conta(Xc, 2.35)
        fr_ = ix[2]                                                # 6 0 · 0 + 4 0 · 1 0 , barra, 1 0 0
        lab0 = gv.submobjects[0][7]
        lab1 = gv.submobjects[0][8]
        self.ate(0.25)
        self.play(TransformFromCopy(lab0[0:2], VGroup(Xc[0][fr_[0]], Xc[0][fr_[1]])), TransformFromCopy(lab1[0:2], VGroup(Xc[0][fr_[5]], Xc[0][fr_[6]])),
                  TransformFromCopy(d10[1][0:2], VGroup(Xc[0][fr_[8]], Xc[0][fr_[9]])),
                  FadeIn(VGroup(*[Xc[0][j] for j in range(len(Xc[0])) if j not in (fr_[0], fr_[1], fr_[5], fr_[6], fr_[8], fr_[9])])), run_time=1.3)
        L2, il2 = eqp(r"\vec F_{ext}", "=", r"\vec 0", r"\ \ \mathrm{e}\ \ ", r"\vec V_{cm}", "=", r"\vec 0", size=46, cores={0: FC, 4: VEL})
        na_conta(L2, 1.4)
        L3 = VGroup(eqp(r"\Rightarrow\ ", r"X_{cm}", size=46, cores={1: CMC})[0], txt("FIXO", 30, bold=True)).arrange(RIGHT, buff=0.18)
        na_conta(L3, 0.6)
        self.ate(0.36)
        self.play(FadeIn(L2), FadeOut(d10), run_time=0.7)
        self.play(FadeIn(L3), run_time=0.6)
        self.ate(0.45)
        self.play(u.animate(rate_func=linear).set_value(1.0), run_time=4.0)
        d4 = cota(X0, X0 + K * 4, YG - 0.55, rot_cota("4 m"))
        self.play(TransformFromCopy(mp(Xc, ix, [4]), d4[1]), FadeIn(d4[0]), run_time=0.9)       # o 4 m da conta desce até a cota
        d6 = cota(X0 + K * 4, X0 + K * 10, YG - 0.55, rot_cota("6 m"))                          # a mais leve anda mais: 6 m
        self.ate(0.6)
        self.play(FadeIn(d6), run_time=0.7)
        # o Cyrano do vídeo anterior: sem still do yt_0016 disponível, entra só o selo e a frase (G18: nunca um ícone de palito)
        C0 = P3(4.3, 0.6)
        tag = txt("DO VÍDEO ANTERIOR", 26, color=DIM).move_to(C0 + P3(0, 0.75))
        cap = VGroup(txt("CYRANO:", 32, bold=True), txt("JOGAR O ÍMÃ PARA CIMA", 30), txt("NÃO FAZ O CONJUNTO SUBIR", 30)).arrange(DOWN, buff=0.14).move_to(C0 + P3(0, -0.35))
        self.ate(0.72)
        self.play(FadeOut(VGroup(Xc, L2, L3)), run_time=0.4)
        self.play(FadeIn(tag), FadeIn(cap), run_time=0.8)
        self.ate(0.84)
        self.dica_entra(dica("O CENTRO DE MASSA SÓ ESCUTA", "A FORÇA EXTERNA"))
        self.ate(0.97)
