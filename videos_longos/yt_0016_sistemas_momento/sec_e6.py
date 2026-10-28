"""Lote Q6 (v2): E6 — agarrar ou rebater. PALCO fixo o exercício inteiro: manequim 3D parado no gelo (olhando para −x) e a bola chegando
em câmera lenta; agarra (braços fecham e o conjunto desliza) ou rebate (a bola volta do peito). CONTA: dados, álgebra e, no E6-4,
as barras de energia. M = 70,0 kg; m = 0,600 kg; v = 10,0 m/s; volta a 8,0 m/s."""
from kit import *  # noqa: F401,F403
from sec_manequim import Manequim3D, pose_agarra, pose_pe, pose_rebate

M, MB, VB, VR = 70.0, 0.600, 10.0, 8.0
V_AG = MB * VB / (M + MB)
V_RB = MB * (VB + VR) / M
K0 = 0.5 * MB * VB ** 2
K_AG = 0.5 * (M + MB) * V_AG ** 2
K_RB = 0.5 * MB * VR ** 2 + 0.5 * M * V_RB ** 2
assert abs(V_AG - 0.0850) < 1e-4 and abs(V_RB - 0.1543) < 1e-4 and abs(K0 - 30) < 1e-9 and abs(K_AG - 0.255) < 1e-3
assert abs(K_RB - 20.03) < 0.01 and abs(K0 - K_AG - 29.745) < 1e-3

ZB = 1.32                 # altura da bola (peito)
LENTO = 4.0               # a bola chega em câmera lenta (×4)
XB0 = -2.2                # a bola entra por aqui (m, mundo)
XC_ = -0.27               # centro da bola no contato com o peito/mãos
TA = (XC_ - XB0) / (VB / LENTO)
PER = 7.5


class LoteE6(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 6 · AGARRAR OU REBATER", selo="SISTEMA: VOCÊ + A BOLA")
        self.modo = "parado"
        self.t0 = 0.0
        self.mq = Manequim3D(self, self.pose, K=2.35, xt=-1.9, yc=-3.0, camx=0.0, op=0.0, seguir=True)
        self.add(self.mq.f3d)
        self.e6_1()
        self.e6_2()
        self.e6_3()
        self.e6_4()
        self.fim()
        self.relatorio()

    # ── estado do PALCO por quadro ─────────────────────────────────────────────────────────────────────────
    def ciclo(self, t):
        """(modo do ciclo, s dentro do ciclo). No E6-4 alterna agarrar/rebater."""
        s = t - self.t0
        if self.modo == "replay":
            k = int(s // PER)
            return ("agarra" if k % 2 == 0 else "rebate"), s % PER
        if self.modo == "chega":
            return "chega", s % 3.0
        return self.modo, s % PER

    def pose(self, t):
        modo, s = self.ciclo(t)
        xb = XB0 + (VB / LENTO) * s
        if modo in ("parado", "chega"):
            p = pose_pe(0.0, -1, resp=1.6 * t)
            p["bola"] = [xb, ZB] if modo == "chega" and xb < -0.75 else None
            return p
        if modo == "agarra":
            if s < TA:
                p = pose_agarra(0.0, max(0.0, (s - TA + 0.5) / 0.5) * 0.6, -1)
                p["bola"] = [xb, ZB]
            else:
                x = V_AG * (s - TA)
                p = pose_agarra(x, min(1.0, 0.6 + (s - TA) / 0.3 * 0.4), -1)
                p["bola"] = "maos"
        else:   # rebate
            if s < TA:
                p = pose_pe(0.0, -1)
                p["bola"] = [xb, ZB]
            else:
                x = V_RB * (s - TA)
                p = pose_rebate(x, min(1.0, (s - TA) / 0.6), -1)
                p["bola"] = [XC_ + x - (VR / LENTO) * (s - TA), ZB]
        return p

    def setas(self):
        def f():
            e = self.mq.f3d.e
            modo, s = self.ciclo(self.clk.get_value())
            g = VGroup()
            if modo == "parado":
                return g
            per = 3.0 if modo == "chega" else PER
            op = min(1.0, (per - s) / 0.3, s / 0.3)
            b = e["bola"]
            if isinstance(b, list) and (s < TA or modo == "rebate"):
                c = self.mq.m(b[0], b[1])
                v = 1.0 if s < TA else -VR / VB
                g.add(arrow(c + P3(0, 0.45), c + P3(1.3 * v, 0.45), color=VEL, width=6, tip=0.16, z=12))
                g.add(mtex(r"10{,}0\ \mathrm{m/s}" if s < TA else r"8{,}0\ \mathrm{m/s}", VEL, 26).move_to(c + P3(0.65 * v, 0.8)))
            if s >= TA and modo != "chega":
                V = V_AG if modo == "agarra" else V_RB
                q = self.mq.m(e["hx"], 0.55)
                g.add(arrow(q + P3(0.35, 0), q + P3(0.35 + 9.5 * V, 0), color=VEL, width=7, tip=0.17, z=12))
                g.add(mtex(r"\vec V", VEL, 32).move_to(q + P3(0.35 + 4.75 * V, 0.35)))
            return escala_op(g, max(op, 0)) if op < 1 else g
        return always_redraw(f)

    def novo_ciclo(self, modo):
        self.modo = modo
        self.t0 = self.clk.get_value()

    # ── E6-1 ─────────────────────────────────────────────────────────────────────────────────────────────
    def e6_1(self):
        self.an("E6-1")
        self.play(self.mq.f3d.op.animate.set_value(1.0), run_time=1.0)
        fr = fronteira(7.3, 5.4, P3(-3.75, -0.6), rotulo=["VOCÊ", mais(22), "A BOLA"])
        sg = self.sg = self.setas()
        self.add(sg)
        dados = VGroup(MathTex(r"M=70{,}0\ \mathrm{kg}", font_size=40), MathTex(r"m=0{,}600\ \mathrm{kg}", font_size=40),
                       MathTex(r"v=10{,}0\ \mathrm{m/s}", font_size=40, color=VEL)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        na_conta(dados, 1.55)
        hz = txt("NA HORIZONTAL: SEM FORÇA EXTERNA", 18, color=DIM)
        na_conta(hz, 0.15)
        self.ate(0.15)
        self.play(FadeIn(dados[0]), run_time=0.5)
        self.ate(0.35)
        self.novo_ciclo("chega")
        self.play(FadeIn(dados[1]), FadeIn(dados[2]), run_time=0.6)
        self.ate(0.55)
        self.play(Create(fr[0]), FadeIn(fr[1]), run_time=0.9)
        self.ate(0.8)
        self.play(FadeIn(hz), run_time=0.5)
        self.ate(0.97)
        self.fr, self.dados, self.hz = fr, dados, hz

    # ── E6-2 — agarra ────────────────────────────────────────────────────────────────────────────────────
    def e6_2(self):
        self.an("E6-2")
        self.novo_ciclo("agarra")
        self.play(self.dados.animate.scale(0.8).move_to(P3(XC0 + self.dados.width * 0.4, 2.0)), FadeOut(self.hz), run_time=0.6)
        ag = txt("AGARRA", 22, bold=True)
        na_conta(ag, 0.9)
        e1 = MathTex(r"0{,}600\cdot 10{,}0=(70{,}0+0{,}600)\,V", font_size=40)
        na_conta(e1, 0.25)
        e2 = Mc(r"V=\frac{6{,}0}{70{,}6}=", (r"0{,}085\ \mathrm{m/s}", VEL), size=44)
        na_conta(e2, -0.75)
        self.ate(0.15)
        self.play(FadeIn(ag), FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        self.ate(0.55)
        self.play(FadeIn(e2, shift=0.1 * UP), run_time=0.8)
        cm = txt("UNS 8,5 CENTÍMETROS POR SEGUNDO", 16, color=DIM)
        na_conta(cm, -1.5)
        self.play(FadeIn(cm), run_time=0.5)
        self.ate(0.97)
        self.c2 = VGroup(ag, e1, e2, cm)

    # ── E6-3 — rebate ────────────────────────────────────────────────────────────────────────────────────
    def e6_3(self):
        self.an("E6-3")
        self.novo_ciclo("rebate")
        self.play(FadeOut(self.dados), self.c2.animate.set_opacity(0.4).scale(0.85).move_to(P3(XC0 + self.c2.width * 0.425, 1.3)), run_time=0.6)
        rb = txt("REBATE: A BOLA VOLTA A 8,0 M/S", 20, bold=True)
        na_conta(rb, -0.75)
        e1 = MathTex(r"70{,}0\cdot V=0{,}600\cdot(10{,}0+8{,}0)", font_size=40)
        na_conta(e1, -1.35)
        e2 = Mc(r"V=", (r"0{,}154\ \mathrm{m/s}", VEL), size=44)
        na_conta(e2, -2.05)
        qd = txt("QUASE O DOBRO", 18, color=VEL, bold=True)
        na_conta(qd, -2.65)
        self.ate(0.2)
        self.play(FadeIn(rb), FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        self.ate(0.55)
        self.play(FadeIn(e2, shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(qd), run_time=0.5)
        pa = txt("COMO A PAREDE DO VÍDEO ANTERIOR:", 16, color=DIM)
        pb = txt("REBATER TRANSFERE MAIS QUE AGARRAR", 16, color=DIM)
        na_conta(pa, 2.5); na_conta(pb, 2.15)
        self.ate(0.8)
        self.play(FadeIn(pa), FadeIn(pb), run_time=0.6)
        self.ate(0.97)
        self.c3 = VGroup(rb, e1, e2, qd, pa, pb)

    # ── E6-4 — energia nas barras (CONTA), replay das duas versões no PALCO ───────────────────────────────
    def e6_4(self):
        self.an("E6-4")
        self.novo_ciclo("replay")
        self.play(FadeOut(self.c2), FadeOut(self.c3), run_time=0.5)
        yb, S = -1.75, 0.085                # base das barras; u por joule
        mm = txt("MOMENTO: CONSERVADO NOS DOIS", 20, color=MAG, bold=True)
        na_conta(mm, 2.4)
        en = txt("ENERGIA: EM NENHUM", 20, color=KC, bold=True)
        na_conta(en, 1.95)
        cols = []
        for x, nome, dep, vtx, qtx in ((2.0, "AGARRAR", K_AG, r"0{,}25\ \mathrm{J}", r"\approx 29{,}7\ \mathrm{J}"),
                                       (4.9, "REBATER", K_RB, r"\approx 20\ \mathrm{J}", r"\approx 10\ \mathrm{J}")):
            a = Rectangle(width=0.62, height=S * K0).set_stroke(mix(KC, 0.3), 2).set_fill(KC, 0.75).move_to(P3(x, yb + S * K0 / 2))
            d = Rectangle(width=0.62, height=max(S * dep, 0.03)).set_stroke(mix(KC, 0.3), 2).set_fill(KC, 0.75).move_to(P3(x + 0.95, yb + max(S * dep, 0.03) / 2))
            q = Rectangle(width=0.62, height=S * (K0 - dep)).set_stroke(mix(HEAT, 0.3), 2).set_fill(HEAT, 0.7) \
                .move_to(P3(x + 0.95, yb + S * dep + S * (K0 - dep) / 2))
            la = txt("ANTES", 14, color=DIM).next_to(a, DOWN, buff=0.1)
            ld = txt("DEPOIS", 14, color=DIM).next_to(d, DOWN, buff=0.1).align_to(la, DOWN)
            n = txt(nome, 18, bold=True).move_to(P3(x + 0.47, yb - 0.65))
            va = tex(r"30\ \mathrm{J}", KC, 26).next_to(a, UP, buff=0.08)
            vd = tex(vtx, KC, 26).next_to(d, RIGHT, buff=0.08)
            vq = tex(qtx, HEAT, 24).next_to(q, RIGHT, buff=0.08)
            cols.append(VGroup(a, d, q, la, ld, n, va, vd, vq))
        base = Line(P3(1.5, yb), P3(7.0, yb)).set_stroke(DIM, 2)
        lq = VGroup(Square(0.16).set_stroke(width=0).set_fill(HEAT, 0.8), txt("CALOR E DEFORMAÇÃO", 14, color=HEAT)).arrange(RIGHT, buff=0.1)
        na_conta(lq, 1.5)
        self.play(FadeIn(base), FadeIn(mm), run_time=0.6)
        for k, c in enumerate(cols):
            self.ate(0.15 + 0.25 * k)
            self.play(GrowFromEdge(c[0], DOWN), FadeIn(c[3]), FadeIn(c[5]), FadeIn(c[6]), run_time=0.6)
            self.play(GrowFromEdge(c[1], DOWN), FadeIn(c[4]), FadeIn(c[7]), run_time=0.6)
            self.play(GrowFromEdge(c[2], DOWN), FadeIn(c[8]), *([FadeIn(lq)] if k == 0 else []), run_time=0.6)
        self.ate(0.6)
        self.play(FadeIn(en), run_time=0.5)
        el = txt("SÓ SE CONSERVA SE A COLISÃO FOR ELÁSTICA", 15, color=DIM)
        na_conta(el, -2.7)
        self.ate(0.7)
        self.play(FadeIn(el), run_time=0.5)
        self.ate(0.8)
        d = dica(["NO MOMENTO O SISTEMA É VOCÊ", mais(22), "A BOLA."], "REBATER TRANSFERE MAIS QUE AGARRAR")
        self.play(FadeOut(el), run_time=0.3)
        self.dica_entra(d)
        self.ate(0.97)
        self.sg.clear_updaters()
        self.dica_sai()
        self.clear(rt=0.5)
