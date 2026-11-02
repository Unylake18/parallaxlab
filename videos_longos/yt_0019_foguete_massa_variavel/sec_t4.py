"""Lote PT4: T4 — e a gravidade? T4-1/T4-2 (Three.js 'rampa' de frente, motor aceso; setas FC empuxo e peso; m dv/dt = v_ex |dm/dt| − m g e a
condição de decolagem), T4-3 (Δv = v_ex ln(m₀/m_f) − g t_q; v × t de dois foguetes com a massa e o propelente do E1, R = 5: 240 kg/s, t_q = 66,7 s
→ 3.370 m/s, e 120 kg/s, t_q = 133 s → 2.717 m/s), T4-4 (a(t) = 300.000/(20.000 − 120 t) − 9,8, de 5,2 a 65,2 m/s²)."""
from pecas19 import *  # noqa: F401,F403

VEX_C = VREL
G_ = 9.8


def v_sub(t, mdot, m0=20000.0, mp=16000.0, vex=2500.0):
    tq = mp / mdot
    tt = min(t, tq)
    return vex * math.log(m0 / (m0 - mdot * tt)) - G_ * tt


class LoteT4(Prob2):
    FUNDO = "fundo_lab_ex.png"

    def construct(self):
        self.setup_base()
        self.t4_rampa()
        self.t4_graficos()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def t4_rampa(self):
        self.an("T4-1")
        self.secao("E A GRAVIDADE?")
        ch, el = ValueTracker(0.0), ValueTracker(9.0)
        self.add(ch, el)
        cam = lambda: cam_obl_(el.get_value(), (0.0, 0.0, 0.5), 4.7, xc=-4.0, yc=-0.55, fov=18)

        def est(t):
            c = ch.get_value()
            n, pp, aa = (140 if c > 0.3 else 0), [], []
            for i in range(n):                                              # jato: a pluma abre rente ao piso a partir do sino
                a = (t * 1.1 + i / n) % 1.0
                th = 2 * math.pi * ((i * 0.6180339) % 1.0)
                rr = 0.02 + 0.30 * a
                pp += [rr * math.cos(th), rr * math.sin(th) * 0.7, 0.03 + 0.11 * (1 - a) * abs(math.sin(i * 3.1))]
                aa.append(round(1 - 0.7 * a, 2))
            return {"f": r4(est_foguete(0.0, 0.0, 0.03, 1.0, "z", ch1=c, torre=0)), "gas": {"p": [round(q, 4) for q in pp], "c": [0] * n, "a": aa, "s": 4.0},
                    "cam": r4(cam())}
        f3 = Fundo3D(self, "rampa", est, op=1.0)                            # a emenda entre lotes já faz o fade
        self.add(f3)
        self.play(el.animate.set_value(6.0), run_time=1.0)
        p = lambda q: projeta3d(cam(), q)
        xa = p((0.0, 0.0, 0.5))[0]
        yn = p((0.0, 0.0, 0.06))[1]
        yc_ = p((0.0, 0.0, 0.42))[1]
        DXF = 0.7                                                                   # v5: setas fora do casco (0,36 u de cada lado do eixo)
        se = arrow(P3(xa + DXF, yn), P3(xa + DXF, yn + 1.9), FC, 7, tip=0.24)        # o empuxo nasce no sino (à direita do eixo)
        sp = arrow(P3(xa - DXF, yc_), P3(xa - DXF, yc_ - 1.1), FC, 7, tip=0.24)      # o peso nasce no centro de massa (à esquerda do eixo)
        self.reg("forca", lugar="T4-1", d_px=0.0, nota="empuxo no sino projetado; peso no CM projetado; deslocamento lateral 14 px (G33 v3)")
        le = MathTex(r"F_{emp}", font_size=40, color=FC).next_to(se, RIGHT, buff=0.3).align_to(se, UP)
        lp = M("m", "g", size=40, cores={1: ACC})[0].next_to(sp, LEFT, buff=0.3).align_to(sp, DOWN)
        self.play(ch.animate.set_value(1.0), GrowArrow(se), FadeIn(le), run_time=0.9)
        self.gat("o peso")
        self.play(GrowArrow(sp), FadeIn(lp), run_time=0.7)
        self.gat("vamos supor subida vertical")
        self.hip([["SUBIDA VERTICAL ·", MathTex("g", font_size=36, color=ACC), "CONSTANTE · SEM AR"]], x0=-2.0, wmax=9.4)
        self.foco = sp
        self.ate(0.97)
        # ── T4-2 ──
        self.an("T4-2")
        painel = RoundedRectangle(corner_radius=0.14, width=6.8, height=1.6).move_to(P3(4.1, 2.5 - 0.8)).set_fill("#0E2A52", 0.85).set_stroke(GEO, 1.2, opacity=0.4)

        def ajusta():
            h_ = 2.5 - (self.pilha.ultima().get_bottom()[1] - 0.3)
            return painel.animate.stretch_to_fit_height(h_).move_to(P3(4.1, 2.5 - h_ / 2))
        painel._fundo = True
        painel.set_z_index(-10)
        self.play(FadeIn(painel), run_time=0.5)
        self.pilha = Pilha(self, x0=1.05, larg=6.2)                         # a conta fica 0,35 para dentro do painel azul
        A, ia = M("m", r"\frac{dv}{dt}", "=", r"v_{ex}", r"\left|\frac{dm}{dt}\right|", "-", "m", "g", size=46, cores={1: ACC, 3: VEX_C, 7: ACC})
        self.pilha.poe(A)
        self.gat("a equação ganha um termo")
        self.play(FadeIn(mp(A, ia, [0, 1, 2, 3, 4])), run_time=0.8)
        self.gat("menos o peso")
        self.voa([(lp, mp(A, ia, [6, 7]))], extra=[FadeIn(mp(A, ia, [5]))], rt=1.0, origem=False, arco_esq=-0.6)          # v8 #7: o rótulo original fica ao lado da seta
        B = VGroup(txt("DECOLA NA LARGADA SE", 26, bold=True), M(r"v_{ex}\left|\frac{dm}{dt}\right|", ">", "m_0", "g", size=46, cores={3: ACC})[0]).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        B[1][0][0:3].set_color(VEX_C)
        B[1][0][0:3].set_stroke(VEX_C, width=1.8, background=False)                  # v7 #25: v_ex legível sobre o painel
        self.pilha.poe(B)
        self.gat("para sair do chão logo na largada")
        self.play(FadeIn(B, shift=0.1 * UP), ajusta(), run_time=0.8)
        C = VGroup(txt("SENÃO, ESPERA ATÉ A MASSA CAIR", 26), txt("· SE O PROPELENTE DURAR", 26)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        self.pilha.poe(C)
        self.gat("se não for")
        self.play(FadeIn(C), ch.animate.set_value(0.7), ajusta(), run_time=0.7)
        self.gat("daqui para a frente")
        self.play(ch.animate.set_value(1.0), Indicate(A, color=WHITE_, scale_factor=1.04), run_time=0.8)
        self.foco = A
        self.ate(0.97)
        self.A42 = A

    def t4_graficos(self):
        self.an("T4-3")
        velhos = list(self.snap())
        self.troca(velhos, seq=True)
        self.s1 = None
        self.layout_v = True                                                    # gráfico largo: sem divisão ESQUEMA × CONTA
        self.pilha = Pilha(self, x0=2.0, larg=5.7)
        C, ic = M("dv", "=", "-", r"v_{ex}", r"\frac{dm}{m}", "-", "g", r"\,dt", size=46, cores={0: VEL, 3: VEX_C, 6: ACC})
        self.pilha.poe(C)
        TM4, VM4, V4 = 170.0, 4400.0, 2500.0 * math.log(5.0)
        G = Graf(-7.2, -3.0, 8.8, TM4, 0, VM4, 4.3 / VM4, rot_y=MathTex("v", font_size=36, color=VEL), rot_x="t")
        k = ValueTracker(0.0)
        self.add(k)
        curvas = vivo(lambda: VGroup(G.curva(lambda t: v_sub(t, 240.0), 0, max(1e-3, min(66.67, 140 * k.get_value())), cor=VEL, w=5),
                                     DashedVMobject(G.curva(lambda t: v_sub(t, 120.0), 0, max(1e-3, min(133.33, 140 * k.get_value())), cor=VEL, w=5), num_dashes=40, dashed_ratio=0.62)))
        lin_sg = DashedLine(G.pt(0, V4), G.pt(TM4, V4), dash_length=0.1).set_stroke(DIM, 1.6, opacity=0.8)
        l_sg = txt("SEM GRAVIDADE", 24, color=DIM).next_to(lin_sg, UP, buff=0.14).align_to(lin_sg, LEFT).shift(0.45 * RIGHT)
        l_sg2 = rot("4.024 m/s", 24, color=VEL).next_to(l_sg, RIGHT, buff=0.2)
        tp1 = lambda: min(66.67, 140 * max(1e-3, k.get_value()))
        tp2 = lambda: min(133.33, 140 * max(1e-3, k.get_value()))
        r1 = rot("240 kg/s", 24)
        r2 = rot("120 kg/s", 24)
        def pos_r(m_, tp, v_, dy, ymin):                                                    # v7 #23: na ponta da curva, nunca a menos de 0,3 u do eixo t
            m_.next_to(G.pt(tp(), v_(tp())), RIGHT, buff=0.42).shift(dy * DOWN)
            if m_.get_center()[1] < G.y0 + ymin:
                m_.shift((G.y0 + ymin - m_.get_center()[1]) * UP)
        r1.add_updater(lambda m_: pos_r(m_, tp1, lambda t_: v_sub(t_, 240.0), 0.28, 0.75))
        r2.add_updater(lambda m_: pos_r(m_, tp2, lambda t_: v_sub(t_, 120.0), 0.0, 0.36))
        pos_r(r1, tp1, lambda t_: v_sub(t_, 240.0), 0.28, 0.75)
        pos_r(r2, tp2, lambda t_: v_sub(t_, 120.0), 0.0, 0.36)
        self.play(FadeIn(G.eixos), FadeIn(curvas), FadeIn(lin_sg), FadeIn(l_sg), FadeIn(l_sg2), FadeIn(r1), FadeIn(r2), k.animate(rate_func=linear).set_value(0.12), run_time=0.8)
        self.gat("integrando de novo")
        self.play(FadeIn(C, shift=0.1 * UP), k.animate(rate_func=linear).set_value(0.3), run_time=1.6)
        D, id_ = M(r"\Delta v", "=", r"v_{ex}", r"\ln\frac{m_0}{m_f}", "-", r"g\,t_q", size=46, cores={0: VEL, 2: VEX_C})
        pinta(D, id_, 5, [(0, ACC)])
        self.pilha.poe(D)
        self.play(FadeIn(D, shift=0.1 * UP), self.ind_copia(mp(C, ic, [3, 5, 6]), WHITE_, 1.08, 1.0), run_time=1.1)                     # v10 F5: a linha chega inteira (sem vagas vazias); os termos de origem pulsam
        self.foco = D
        br = Brace(mp(D, id_, [4, 5]), DOWN, buff=0.08, color=HEAT)
        lb = txt("PERDA POR GRAVIDADE", 24, color=HEAT).next_to(br, DOWN, buff=0.18)
        if lb.get_right()[0] > 7.4:
            lb.shift((7.4 - lb.get_right()[0]) * RIGHT)
        self.pilha.poe(VGroup(br, lb), dx=max(0.0, min(br.get_left()[0] - self.pilha.x0, 5.7 - VGroup(br, lb).width)))
        self.gat("esse último termo é a perda")
        self.play(GrowFromCenter(br), FadeIn(lb), k.animate(rate_func=linear).set_value(0.45), run_time=1.0)
        self.gat("e agora a vazão importa")
        self.play(k.animate(rate_func=linear).set_value(1.0), run_time=4.0)
        f1, f2 = v_sub(1e9, 240.0), v_sub(1e9, 120.0)
        self.reg("t4_3", v240=f1, v120=f2)
        r1.clear_updaters()
        r2.clear_updaters()
        l1 = rot(f"{f1:,.0f} m/s".replace(",", "."), 26, VEL).next_to(r1, DOWN, buff=0.1).align_to(r1, LEFT)
        l2 = rot(f"{f2:,.0f} m/s".replace(",", "."), 26, VEL).next_to(r2, DOWN, buff=0.1).align_to(r2, LEFT)
        pts_ = VGroup(*[Dot(G.pt(tq, fv_), radius=0.07, color=WHITE_).set_z_index(9) for tq, fv_ in ((66.67, f1), (133.33, f2))])
        per = VGroup(*[Line(G.pt(tq, fv_), G.pt(tq, V4)).set_stroke(HEAT, 4).set_z_index(8) for tq, fv_ in ((66.67, f1), (133.33, f2))])
        lper = VGroup(*[rot(f"{V4 - fv_:,.0f} m/s".replace(",", "."), 26, HEAT).next_to(G.pt(tq, (fv_ + V4) / 2), RIGHT, buff=0.3) for tq, fv_ in ((66.67, f1), (133.33, f2))])
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(pts_), run_time=0.6)
        self.play(Create(per), FadeIn(lper), run_time=0.8)
        self.reg("t4_perda", p1=V4 - f1, p2=V4 - f2)
        self.selo("COM GRAVIDADE", "QUEIMAR MAIS RÁPIDO PERDE MENOS", x0=-2.0, wmax=9.4)
        self.foco = l1
        self.ate(0.97)
        # ── T4-4: a aceleração ──
        self.an("T4-4")
        self.sem_selo()
        velhos = [m for m in self.snap() if m not in [l for l, _ in self.pilha.linhas]]
        Ga = Graf(-7.2, -3.0, 8.8, 140.0, 0, 70, 4.5 / 70, rot_y=MathTex("a", font_size=36, color=ACC), rot_x="t")
        ka = ValueTracker(0.0)
        self.add(ka)
        fa = lambda t: 300000.0 / (20000.0 - 120.0 * min(t, 133.33)) - G_
        ca = vivo(lambda: Ga.curva(fa, 0, max(1e-3, 133.33 * ka.get_value()), cor=ACC, w=6))
        self.troca(velhos, FadeIn(Ga.eixos), FadeIn(ca), ka.animate.set_value(0.12), seq=True)
        E, ie = M("a", "=", r"v_{ex}", r"\frac{\left|\frac{dm}{dt}\right|}{m}", "-", "g", size=50, cores={0: ACC, 2: VEX_C, 5: ACC})
        self.pilha.poe(E)
        self.play(FadeIn(E), run_time=0.7)
        den = mp(E, ie, [3])[-1:]
        self.gat("a massa do foguete vai diminuindo")
        self.play(Indicate(den, color=WHITE_, scale_factor=1.5), ka.animate(rate_func=linear).set_value(0.5), run_time=1.6)
        self.play(ka.animate(rate_func=linear).set_value(1.0), run_time=2.0)
        la = VGroup(rot("5,2 m/s²", 26, ACC).next_to(Ga.pt(0, fa(0)), UR, buff=0.3).shift(0.25 * UP),
                    rot("65,2 m/s²", 26, ACC).next_to(Ga.pt(133.33, fa(133.33)), LEFT, buff=0.25).shift(0.15 * UP))
        self.reg("t4_4", a0=fa(0), af=fa(133.33))
        self.play(FadeIn(la), run_time=0.6)
        self.foco = la[1]
        self.ate(0.97)
