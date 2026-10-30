"""Lote Q6 (v4): E6 — agarrar ou rebater. PALCO fixo o exercício inteiro: manequim 3D no gelo (olhando para −x).
v4 (regra 1.2): cada evento roda UMA vez sincronizado com a fala: no fim do E6-1 a bola chega (câmera lenta, chip), no E6-2 ele agarra e
desliza em velocidade real; no E6-3, depois de uma virada em sequência (o 3D sai e volta já parado), a bola rebate; o deslizamento segue
pelo E6-4 (a câmera passa a acompanhar quando ele chega perto da borda; as marcas do gelo mostram o movimento). Sem replay.
CONTA: dados, álgebra (o AGARRA vira uma linha-resumo antes do REBATE) e, no E6-4, as barras de energia.
M = 70,0 kg; m = 0,600 kg; v = 10,0 m/s; volta a 8,0 m/s."""
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
LENTO = 8.0               # a bola em câmera lenta (×8)
XC_ = -0.27               # centro da bola no contato com o peito/mãos (relativo ao quadril)
K_, XT = 2.35, -4.2       # zoom e posição do quadril na tela no começo (câmera parada)
XV0 = (-7.0 - XT) / K_    # x do mundo onde a bola fica visível (borda do PALCO)
HX_LIM = (-1.6 - XT) / K_  # daqui em diante a câmera acompanha o deslizamento
KV = 6.0                  # seta da velocidade do conjunto: unidades por m/s
LENTO_R = 20.0            # v6 (1.2): o rebote em câmera lenta mais forte (~2,5 s até a bola sair pela borda)


class LoteE6(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 6 · AGARRAR OU REBATER", selo="SISTEMA: VOCÊ + A BOLA")
        self.ev = [(0.0, None, "parado")]           # (instante da troca de estado, instante do contato, modo)
        self.kf_ag = None                           # v6: trajetória da bola no agarrar (entra, para no ar, retoma)
        self.mq = Manequim3D(self, self.pose, K=K_, xt=XT, yc=-3.0, camx=0.0, op=0.0)
        self.mq.f3d.conta.set_value(1.0)
        orig = self.mq.estado

        def estado(t):                               # a câmera fica parada até ele chegar perto da borda; depois acompanha
            e = orig(t)
            e["cam"]["camx"] = round(max(0.0, e["hx"] - HX_LIM), 4)
            return e
        self.mq.estado = estado
        self.mq.f3d.fn = estado
        self.add(self.mq.f3d)
        self.e6_1()
        self.e6_2()
        self.e6_3()
        self.e6_4()
        self.fim()
        self.relatorio()

    # ── estado do PALCO por quadro ─────────────────────────────────────────────────────────────────────────
    def evento(self, t):
        return [x for x in self.ev if x[0] <= t + 1e-9][-1]

    def pose(self, t):
        _, tc, modo = self.evento(t)
        if modo == "parado":
            return pose_pe(0.0, -1, resp=1.6 * t)
        vb = VB / LENTO
        s = t - tc                                   # tempo desde o contato (< 0: a bola chegando)
        if s < 0:
            p = pose_agarra(0.0, max(0.0, (s + 0.5) / 0.5) * 0.6, -1) if modo == "agarra" else pose_pe(0.0, -1, resp=1.6 * t)
            if modo == "agarra" and self.kf_ag:
                p["bola"] = [round(float(np.interp(t, *self.kf_ag)), 4), ZB]
            else:
                p["bola"] = [XC_ + vb * s, ZB]
        elif modo == "agarra":
            p = pose_agarra(V_AG * s, min(1.0, 0.6 + s / 0.3 * 0.4), -1)
            p["bola"] = "maos"
        else:
            x = V_RB * s
            p = pose_rebate(x, min(1.0, s / 0.6), -1)
            p["bola"] = [XC_ + x - (VR / LENTO_R) * s, ZB]
        if isinstance(p.get("bola"), list):          # a bola entra e sai em fade dentro do PALCO
            xr = p["bola"][0] - max(0.0, p["hx"] - HX_LIM)
            p["bola_op"] = round(min(1.0, max(0.0, (xr - XV0) / 0.3)), 3)
            if p["bola_op"] <= 0:
                p["bola"] = None
        return p

    def voando(self):
        return isinstance(self.mq.f3d.e.get("bola"), list)

    def setas(self):
        def f():
            t = self.clk.get_value()
            e = self.mq.f3d.e
            _, tc, modo = self.evento(t)
            g = VGroup()
            if modo == "parado":
                return g
            s = t - tc
            b = e.get("bola")
            if isinstance(b, list):
                c = self.mq.m(b[0], b[1])
                v = 1.0 if s < 0 else -VR / VB
                bv = VGroup(arrow(c + P3(0, 0.45), c + P3(1.3 * v, 0.45), color=VEL, width=6, tip=0.16, z=12),
                            mtex(r"10{,}0\ \mathrm{m/s}" if v > 0 else r"8{,}0\ \mathrm{m/s}", VEL, 26).move_to(c + P3(0.65 * v, 0.8)))
                g.add(escala_op(bv, e.get("bola_op", 1.0)))
            if s >= 0:
                V = V_AG if modo == "agarra" else V_RB
                q = self.mq.m(e["hx"], 0.55)
                a = arrow(q + P3(0.35, 0), q + P3(0.35 + KV * V, 0), color=VEL, width=7, tip=0.17, z=12)
                g.add(escala_op(VGroup(a, mtex(r"\vec V", VEL, 32).next_to(a, UP, buff=0.15)), min(1.0, s / 0.3)))
            return g
        return always_redraw(f)

    def lento(self):
        """CÂMERA LENTA enquanto a bola voa."""
        return always_redraw(lambda: chip_lento(0.85 if self.voando() else 0.0, x=-7.1, y=1.8))   # dentro da fronteira

    def chegada(self, modo, dt_contato):
        """Agenda o evento: a bola toca dt_contato s depois de agora (ela entra pela borda do PALCO antes)."""
        t = self.clk.get_value()
        self.ev.append((t, t + dt_contato, modo))

    # ── E6-1 ─────────────────────────────────────────────────────────────────────────────────────────────
    def e6_1(self):
        self.an("E6-1")
        fr = fronteira(7.3, 5.4, P3(-3.75, -0.6), rotulo=["VOCÊ", mais(22), "A BOLA"])
        sg = self.sg = self.setas()
        self.lt = self.lento()
        self.add(sg, self.lt)
        self.play(self.mq.f3d.op.animate.set_value(1.0), run_time=0.8)
        dados = VGroup(MathTex(r"M=70{,}0\ \mathrm{kg}", font_size=40), MathTex(r"m=0{,}600\ \mathrm{kg}", font_size=40),
                       MathTex(r"v=10{,}0\ \mathrm{m/s}", font_size=40, color=VEL)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        na_conta(dados, 1.55)
        hz = txt("NA HORIZONTAL: SEM FORÇA EXTERNA", 18, color=DIM)
        na_conta(hz, 0.15)
        t_in = self.clk_de("E6-1", "joga em você uma bola", 0.1)
        t_h = self.clk_de("E6-1", "a dez metros por segundo", -0.3)
        t_go = self.clk_de("E6-2", "você agarra a bola", 0.1)
        XH = -0.85
        self.kf_ag = ([t_in, t_h, t_go, t_go + 1.5], [XV0 - 0.35, XH, XH, XC_])
        self.ev.append((t_in, t_go + 1.5, "agarra"))
        self.diz("com setenta quilogramas")
        self.play(FadeIn(dados[0]), run_time=0.5)
        self.diz("seiscentos gramas")
        self.play(FadeIn(dados[1]), run_time=0.5)
        self.diz("a dez metros por segundo")
        self.play(FadeIn(dados[2]), run_time=0.5)
        self.diz("O sistema é você mais a bola")
        self.play(Create(fr[0]), FadeIn(fr[1]), run_time=0.8)
        self.diz("na horizontal, não tem")
        self.play(FadeIn(hz), run_time=0.5)
        # v6 (1.2): a bola entra no "joga em você uma bola", para no ar no "dez metros por segundo" e retoma no "você agarra a bola"
        # (câmera lenta de 1,5 s até as mãos)
        self.ate(0.97)
        self.fr, self.dados, self.hz = fr, dados, hz

    # ── E6-2 — agarra (uma vez) ──────────────────────────────────────────────────────────────────────────
    def e6_2(self):
        self.an("E6-2")
        self.play(self.dados.animate.scale(0.8).move_to(P3(XC0 + self.dados.width * 0.4, 2.0)), FadeOut(self.hz), run_time=0.6)
        ag = txt("AGARRA", 22, bold=True)
        na_conta(ag, 0.9)
        e1 = Mc(r"0{,}600\cdot 10{,}0", "=", r"(70{,}0+0{,}600)\,V", size=40)
        na_conta(e1, 0.25)
        e2 = Mc(r"V=\frac{6{,}0}{70{,}6}=", (r"0{,}085\ \mathrm{m/s}", VEL), size=44)
        na_conta(e2, -0.75)
        self.diz("você agarra a bola")
        self.play(FadeIn(ag), run_time=0.5)
        self.diz("zero vírgula seis vezes dez")
        self.play(FadeIn(e1[0], shift=0.1 * UP), run_time=0.6)
        self.diz("seis quilogramas metro por segundo")
        self.play(Circumscribe(e1[0], color=MAG, buff=0.08, time_width=0.6), run_time=1.0)
        self.diz("você e a bola seguem juntos")
        self.play(FadeIn(e1[1:], shift=0.1 * UP), run_time=0.7)
        self.diz("setenta vírgula seis")
        self.play(FadeIn(e2[0], shift=0.1 * UP), run_time=0.7)
        cm = txt("UNS 8,5 CENTÍMETROS POR SEGUNDO", 18, color=DIM)
        na_conta(cm, -1.5)
        self.diz("oito centímetros e meio")
        self.play(FadeIn(e2[1:], shift=0.1 * UP), FadeIn(cm), run_time=0.6)
        self.diz("Bem devagarinho")
        self.play(Indicate(e2[1], color=WHITE_, scale_factor=1.12), run_time=1.0)
        self.ate(0.97)
        self.c2 = VGroup(ag, e1, e2, cm)

    # ── E6-3 — rebate (uma vez) ──────────────────────────────────────────────────────────────────────────
    def e6_3(self):
        self.an("E6-3")
        # o 3D sai (0,3 s) e volta já parado, de pé (0,3 s); na CONTA o AGARRA sai inteiro e vira uma linha-resumo no topo
        res = linha("AGARRA:", Mc(r"V=", (r"0{,}085\ \mathrm{m/s}", VEL), size=36), size=20, buff=0.18).set_opacity(0.6)
        na_conta(res, 2.45)
        self.play(self.mq.f3d.op.animate.set_value(0.0), FadeOut(self.dados), FadeOut(self.c2), run_time=0.3)
        self.ev.append((self.clk.get_value(), None, "parado"))
        self.play(self.mq.f3d.op.animate.set_value(1.0), FadeIn(res), run_time=0.3)
        rb = txt("REBATE: A BOLA VOLTA A 8,0 M/S", 20, bold=True)
        e1 = MathTex(r"70{,}0\cdot V=0{,}600\cdot(10{,}0+8{,}0)", font_size=40)
        e2 = Mc(r"V=", (r"0{,}154\ \mathrm{m/s}", VEL), size=44)
        qd = txt("· QUASE O DOBRO", 20, color=VEL, bold=True)
        for m_, y in ((rb, 1.55), (e1, 0.85), (e2, 0.0)):
            na_conta(m_, y)
        qd.next_to(e2, RIGHT, buff=0.25)
        self.chegada("rebate", max(1.0, self.ate_dizer("bate no seu peito", -0.2, mover=False)))
        self.diz("volta a oito metros")
        self.play(FadeIn(rb), run_time=0.6)
        self.diz("a sua massa vezes a sua velocidade")
        self.play(FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        self.diz("quinze centímetros")
        self.play(FadeIn(e2, shift=0.1 * UP), run_time=0.7)
        self.diz("quase o dobro")
        self.play(FadeIn(qd), run_time=0.5)
        # o chip do vídeo anterior, no rodapé da CONTA, sem tocar em nada
        pa = txt("COMO A PAREDE DO VÍDEO ANTERIOR:", 16, color=DIM)
        pb = txt("REBATER TRANSFERE MAIS QUE AGARRAR", 16, color=DIM)
        cp = VGroup(pa, pb).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        caixa = RoundedRectangle(corner_radius=0.1, width=cp.width + 0.4, height=cp.height + 0.3).set_stroke(BLUE_L, 1.2, opacity=0.6) \
            .set_fill(PANEL, 0.9)
        cp.move_to(caixa)
        chip = VGroup(caixa, cp)
        na_conta(chip, -2.4)
        self.diz("É o mesmo efeito da parede")
        self.play(FadeIn(chip), run_time=0.6)
        self.ate(0.97)
        self.c3 = VGroup(res, rb, e1, e2, qd, chip)

    # ── E6-4 — energia nas barras (CONTA); o PALCO segue com o deslizamento do rebate ──────────────────────
    def e6_4(self):
        self.an("E6-4")
        self.play(FadeOut(self.c3), run_time=0.3)
        yb, S = -1.25, 0.07                 # base das barras; u por joule (v6, N7: folga da DICA)
        mm = txt("MOMENTO: CONSERVADO NOS DOIS", 20, color=MAG, bold=True)
        na_conta(mm, 2.4)
        en = txt("ENERGIA: EM NENHUM", 20, color=KC, bold=True)
        na_conta(en, 1.95)
        cols = []
        for x, nome, dep, vtx, qtx in ((2.0, "AGARRAR", K_AG, r"0{,}25\ \mathrm{J}", r"\approx 29{,}7\ \mathrm{J}"),
                                       (4.9, "REBATER", K_RB, r"\approx 20\ \mathrm{J}", r"\approx 10\ \mathrm{J}")):
            a = barra2(0.62, S * K0, KC).move_to(P3(x, yb + S * K0 / 2))
            hd = max(S * dep, 0.03)
            d = barra2(0.62, hd, KC).move_to(P3(x + 0.95, yb + hd / 2))
            q = barra2(0.62, S * (K0 - dep), HEAT, 0.8).move_to(P3(x + 0.95, yb + S * dep + S * (K0 - dep) / 2))
            la = txt("ANTES", 14, color=DIM).next_to(a, DOWN, buff=0.1)
            ld = txt("DEPOIS", 14, color=DIM).next_to(d, DOWN, buff=0.1).align_to(la, DOWN)
            n = txt(nome, 18, bold=True).move_to(P3(x + 0.47, yb - 0.65))
            va = tex(r"30\ \mathrm{J}", KC, 26).next_to(a, UP, buff=0.08)
            vq = tex(qtx, HEAT, 24).next_to(q, RIGHT, buff=0.08)
            if dep < 1.0:      # a barra minúscula: o valor um pouco acima, com um fio-guia curto (nunca na base nem na coluna vizinha)
                vt = tex(vtx, KC, 26).move_to(P3(x + 0.95 + 0.31 + 0.55, yb + 0.42))
                fio = Line(d.get_right() + P3(0.03, 0), vt.get_left() + P3(-0.06, -0.08)).set_stroke(KC, 1.5)
                vd = VGroup(fio, vt)
                vq.shift(UP * 0.35)
            else:
                vd = tex(vtx, KC, 26).next_to(d, RIGHT, buff=0.08)
            cols.append(VGroup(a, d, q, la, ld, n, va, vd, vq))
        base = Line(P3(1.5, yb), P3(7.0, yb)).set_stroke(DIM, 2)
        lq = VGroup(Square(0.16).set_stroke(width=0).set_fill(HEAT, 0.8), txt("ENERGIA INTERNA: DEFORMAÇÃO, CALOR, SOM", 14, color=HEAT)).arrange(RIGHT, buff=0.1)
        na_conta(lq, 1.55)
        self.play(FadeIn(base), run_time=0.3)
        frases = (("trinta joules", "sobram uns zero vírgula vinte e cinco", "quase trinta viram energia interna"),
                  ("Quando você rebate", "sobram uns vinte", "e uns dez se perdem"))
        for k, (c, (f0, f1, f2)) in enumerate(zip(cols, frases)):
            self.diz(f0)
            self.play(GrowFromEdge(c[0], DOWN), FadeIn(c[3]), FadeIn(c[5]), FadeIn(c[6]), run_time=0.6)
            self.diz(f1)
            self.play(GrowFromEdge(c[1], DOWN), FadeIn(c[4]), FadeIn(c[7]), run_time=0.6)
            self.diz(f2)
            self.play(GrowFromEdge(c[2], DOWN), FadeIn(c[8]), *([FadeIn(lq)] if k == 0 else []), run_time=0.6)
        self.diz("O momento se conservou")
        self.play(FadeIn(mm), run_time=0.5)
        self.diz("a energia cinética, em nenhum")
        self.play(FadeIn(en), run_time=0.5)
        el = txt("SÓ SE CONSERVA SE A COLISÃO FOR ELÁSTICA", 15, color=DIM)
        na_conta(el, -2.35)
        self.diz("Ela só se conserva")
        self.play(FadeIn(el), run_time=0.5)
        d = dica(["NO MOMENTO O SISTEMA É VOCÊ", mais(22), "A BOLA."], "REBATER TRANSFERE MAIS QUE AGARRAR")
        self.dica_entra(d)
        self.sobra(0.55)
        self.sg.clear_updaters(); self.lt.clear_updaters()
        self.clear(rt=0.5)
