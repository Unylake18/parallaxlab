"""Lote PC (v4): coda — a luz também tem momento. C-1 (redesenho v4): raias em painéis, feixe amarelo (LUZ), fótons em pacotes de onda,
placas penduradas (a preta absorve com flash de calor, o espelho reflete e inclina o dobro), F e 2F, p = E/c (2D).
C-2/C-3: vela solar refletora 3D (threejs/cena3d/vela.js) abrindo no espaço, fótons batendo e voltando, a seta da força crescendo;
números na CONTA. Sol 1.361 W/m²: 4,5 μPa (absorvida), 9,1 μPa (refletida); vela de 100 m²: ≈ 0,9 mN; laser de 1 W: 3,3 nN."""
from kit import *  # noqa: F401,F403

C_LUZ, I_SOL = 2.998e8, 1361.0
P_ABS, P_REF = I_SOL / C_LUZ, 2 * I_SOL / C_LUZ
F_VELA, F_LASER = P_REF * 100, 1.0 / C_LUZ
assert abs(P_ABS - 4.54e-6) < 0.01e-6 and abs(P_REF - 9.08e-6) < 0.01e-6 and abs(F_VELA - 0.908e-3) < 0.002e-3
assert abs(F_LASER - 3.34e-9) < 0.01e-9


def num(s, cor=WHITE_, size=M_LAB):
    return MathTex(s, font_size=size, color=cor)


class LoteCoda(Base):
    def construct(self):
        self.setup_base(cap="A LUZ TAMBÉM TEM MOMENTO")
        self.c1()
        self.c2_3()
        self.fim()
        self.relatorio()

    def feixe(self, y, x0, x1, volta=False):
        g = VGroup(Rectangle(width=x1 - x0, height=0.34).move_to(P3((x0 + x1) / 2, y)).set_stroke(width=0).set_fill(WHITE_, 0.08))

        def ondas():
            s = self.clk.get_value()
            h = VGroup()
            L = x1 - x0
            for k in range(7):
                x = x0 + ((s * 1.4 + k * L / 7) % L)
                h.add(Line(P3(x, y + (0.08 if volta else 0)), P3(min(x + 0.3, x1), y + (0.08 if volta else 0))).set_stroke(WHITE_, 3, opacity=0.8))
                if volta:
                    xr = x1 - ((s * 1.4 + k * L / 7) % L)
                    h.add(Line(P3(xr, y - 0.1), P3(max(xr - 0.3, x0), y - 0.1)).set_stroke(WHITE_, 3, opacity=0.5))
            return h
        return g, always_redraw(ondas)

    def c1(self):
        """v4: a luz absorvida e refletida (Manim 2D). Duas raias em painéis; emissor; feixe amarelo com brilho em camadas; fótons
        como pacotes de onda (um em destaque leva p⃗); placas penduradas por fios: a preta engole o fóton com um flash laranja (calor) e
        se inclina um ângulo pequeno; o espelho devolve o fóton (p⃗ → −p⃗) e se inclina o dobro; F⃗ e 2F⃗ na razão 1 : 2."""
        self.an("C-1")
        t0 = self.clk.get_value()
        X_EM, X_PL, VF = -6.55, -1.35, 2.1               # emissor, placa (pivô), velocidade dos fótons na tela
        TH0 = math.radians(7.0)                          # inclinação da placa preta (a do espelho: o dobro)
        raias = []
        # v7 (3D): as duas placas numa campânula de vácuo (placas.js); os lasers do lado de fora; a câmera vai de 3/4 para frontal no
        # "Olha as duas placas". Fótons, setas e rótulos continuam no Manim, presos à projeção exata da câmera.
        tfr = self.clk_de("C-1", "Olha as duas placas", 0.1)

        def cam_(t):
            a = min(1.0, max(0.0, (t - tfr) / 1.6))
            u = a * a * (3 - 2 * a)
            a0 = -62 - 9 * min(1.0, max(0.0, (t - t0) / 9.0))         # antes: deriva lenta (palco vivo), 1°/s
            return {"modo": "obl", "az": a0 + (-90 - a0) * u, "el": 14 + (3 - 14) * u,
                    "alvo": [-3.4, 0, -0.4], "K": 0.95 + 0.05 * u, "fov": 14, "xc": -3.4, "yc": -0.4}
        self.cam_c1 = cam_
        for yc, rot, refl in ((1.05, "SUPERFÍCIE PRETA · ABSORVE", False), (-1.85, "ESPELHO · REFLETE", True)):
            lab = txt(rot, 18, color=DIM).move_to(P3(-6.35, yc + 1.0), aligned_edge=LEFT)   # v7: à direita do pé do laser
            raias.append(dict(y=yc - 0.15, topo=yc + 1.12, refl=refl, est=VGroup(VMobject(), lab, VMobject())))
        L_FIO, H_PL = 1.0, 1.0
        PER_F, N_F = 0.9, 6                              # um fóton a cada 0,9 s

        def theta(refl):
            s = self.clk.get_value() - t0
            return (2 if refl else 1) * TH0 * suave((s - 1.5) / 3.0)

        def est3(t):
            s_ = t - t0
            rows = []
            for r in raias:
                th = (2 if r["refl"] else 1) * TH0 * suave((s_ - 1.5) / 3.0)
                rows.append({"y": r["y"], "piv": [X_PL, r["topo"] - 0.08], "th": th, "refl": r["refl"],
                             "quente": 0.0 if r["refl"] else 0.35 * suave((s_ - 1.5) / 8.0) / 0.35})
            return {"rows": rows, "xem": X_EM, "feixe": 1.0, "cam": cam_(t)}
        self.f3p = Fundo3D(self, "placas", est3, op=0.0)
        self.f3p.conta.set_value(1.0)
        self.add(self.f3p)

        def P(x, y):                                      # ponto do plano das placas (3D: x, z = y) → Manim
            return proj3d(cam_(self.clk.get_value()), (x, 0, y))

        def placa(r):
            th = theta(r["refl"])
            piv = P3(X_PL, r["topo"] - 0.08)
            # v5: suspensão de dois fios paralelos: a placa se desloca sem girar, e a luz incide sempre perpendicular à face
            topo_pl = piv + L_FIO * P3(math.sin(th), -math.cos(th))
            c = topo_pl + P3(0, -H_PL / 2)
            if r["refl"]:
                corpo = Rectangle(width=0.2, height=H_PL).set_stroke(GEO, 1.5).set_fill(color=[STEEL, GEO], opacity=1)
                corpo.set_sheen_direction(RIGHT)
                brilho = Line(P3(-0.05, -0.4), P3(-0.05, 0.4)).set_stroke(WHITE_, 2, opacity=0.8)
                pl = VGroup(corpo, brilho)
            else:
                s = self.clk.get_value() - t0
                quente = 0.35 * suave((s - 1.5) / 8.0)
                pl = VGroup(Rectangle(width=0.2, height=H_PL).set_stroke("#2A2F3A", 1.5)
                            .set_fill(interpolate_color(ManimColor("#0B0D12"), ManimColor(HEAT), quente), 1))
            pl.move_to(c)
            face = c + P3(-0.1, 0)                                       # a face que recebe a luz (no meio da placa)
            return VGroup(VMobject(), VMobject(), pl.move_to(P(c[0], c[1])).set_opacity(0)), face

        def pacote(xc, y, op=1.0, sent=1):
            us = np.linspace(-1, 1, 36)
            pts = [P(xc + 0.3 * u, y + 0.13 * math.exp(-(1.7 * u) ** 2) * math.sin(3 * PI * (u + 1) * sent)) for u in us]
            g = VGroup()
            for w, o, c in ((10, 0.12, LUZ), (5, 0.3, LUZ), (2.2, 1.0, LUZ_B)):
                g.add(VMobject().set_points_smoothly(pts).set_stroke(c, w, opacity=o * op))
            return g

        def cena():
            s = self.clk.get_value() - t0
            g = VGroup()
            for k, r in enumerate(raias):
                y = r["y"]
                pl, face = placa(r)
                xf = face[0]
                # v7: o feixe (com brilho volumétrico) e as placas são do 3D
                L = xf - (X_EM + 0.31)
                tv = L / VF
                jmax = int((s - 0.6) // PER_F)
                for j in range(max(0, jmax - N_F), jmax + 1):    # os fótons saem sem parar, um a cada PER_F
                    ti = s - 0.6 - j * PER_F
                    if ti < 0 or ti > 2 * tv + 0.4:
                        continue
                    destaque = j % 7 == 1                        # de tempos em tempos, um fóton leva a seta p
                    if ti < tv:                              # indo
                        x = X_EM + 0.31 + VF * ti
                        g.add(pacote(x, y))
                        if destaque:                          # v5 (V17): acima do feixe; some antes de chegar na placa
                            a = arrow(P(x - 0.25, y + 0.45), P(x + 0.3, y + 0.45), color=MAG, width=5, tip=0.13, z=12)
                            ga = VGroup(a, mtex(r"\vec p", MAG, 28).next_to(a, UP, buff=0.08))
                            g.add(escala_op(ga, min(1.0, max(0.0, (xf - 0.5 - x) / 0.5))))
                    elif not r["refl"]:                      # absorvido: some dentro da placa, flash laranja (calor)
                        if ti < tv + 0.3:
                            u = (ti - tv) / 0.3
                            g.add(Circle(radius=0.08 + 0.25 * u).move_to(P(xf, y)).set_stroke(HEAT, 4, opacity=1 - u).set_fill(HEAT, 0.5 * (1 - u)))
                    elif ti < 2 * tv:                        # refletido: volta pelo feixe de volta, a 60 %
                        x = xf - VF * (ti - tv)
                        g.add(pacote(x, y - 0.22, 0.6, -1))
                        if destaque:
                            a = arrow(P(x + 0.25, y - 0.67), P(x - 0.3, y - 0.67), color=MAG, width=5, tip=0.13, z=12)
                            g.add(a, mtex(r"-\vec p", MAG, 28).next_to(a, DOWN, buff=0.08))
                # a força na placa (atrás dela), na razão 1 : 2
                o = suave((s - 1.5) / 1.5)
                if o > 0.01:
                    Lf = 0.55 * (2 if r["refl"] else 1)
                    c = face + P3(0.1, 0)                  # v7: no plano das placas, projetado
                    fa = arrow(P(c[0] + 0.22, c[1]), P(c[0] + 0.22 + Lf, c[1]), color=FC, width=7, tip=0.18, z=12)
                    g.add(escala_op(VGroup(fa, mtex(r"2\vec F" if r["refl"] else r"\vec F", FC, 32).next_to(fa.get_end(), UP, buff=0.14)), o))   # V17: sobre a ponta livre, longe da placa e dos fios
            return g
        est = VGroup(*[r["est"] for r in raias])
        cn = always_redraw(cena)
        self.play(self.f3p.op.animate.set_value(1.0), FadeIn(cn), run_time=0.3)      # v7: os rótulos das raias entram na vista frontal

        def caixa(i):                                    # o contorno da placa i (3D) no quadro corrente, para o Circumscribe
            r = raias[i]
            th = theta(r["refl"])
            cx = X_PL + L_FIO * math.sin(th)
            cz = r["topo"] - 0.08 - L_FIO * math.cos(th) - H_PL / 2
            a, b = P(cx - 0.45, cz - 0.65), P(cx + 0.45, cz + 0.65)
            return Rectangle(width=abs(b[0] - a[0]), height=abs(b[1] - a[1])).move_to((a + b) / 2)
        # Δp da placa do espelho: p − (−p) = 2p (o mini-diagrama ao lado da placa)
        dpl = Mc((r"\Delta\vec p_{\text{placa}}", MAG), "=", (r"\vec p-(-\vec p)", MAG), "=", (r"2\vec p", MAG), size=34)
        na_conta(dpl, 0.65)                              # v5 (V17): na CONTA, abaixo de p = E/c (nada sobre as raias)
        pe = Mc((r"p", MAG), "=", (r"\frac{E}{c}", WHITE_), size=M_MAIN)
        pe[2][0].set_color(LUZ)
        na_conta(pe, 1.75)
        self.diz("O momento de um pulso de luz")
        self.play(FadeIn(pe[:2], shift=0.1 * UP), run_time=0.6)
        self.diz("a energia dele dividida")
        self.play(FadeIn(pe[2], shift=0.1 * UP), run_time=0.7)
        self.diz("Olha as duas placas")
        self.wait(1.4)
        self.play(FadeIn(est), Circumscribe(caixa(0), color=LUZ_B, buff=0.02, time_width=0.8),
                  Circumscribe(caixa(1), color=LUZ_B, buff=0.02, time_width=0.8), run_time=1.0)
        ab = linha("ABSORVE:", tex(r"\vec F", FC, 36), size=20, buff=0.18)
        rf = linha("REFLETE:", tex(r"2\vec F", FC, 36), size=20, buff=0.18)
        na_conta(ab, -1.85); na_conta(rf, -2.45)
        self.diz("Na preta, a luz é absorvida")
        self.play(Indicate(est[0][1], color=WHITE_), FadeIn(ab), run_time=0.8)
        self.diz("No espelho, a luz volta")
        self.play(Indicate(est[1][1], color=WHITE_), FadeIn(rf), run_time=0.8)
        self.diz("o momento de ida e o de volta")
        self.play(FadeIn(dpl, shift=0.1 * UP), run_time=0.7)
        fr = Mc((r"\frac{\Delta p}{\Delta t}", MAG), "=", (r"F", FC), size=50)
        nf = txt("MOMENTO POR SEGUNDO É FORÇA", 18, color=DIM)
        na_conta(fr, -0.35); na_conta(nf, -1.2)
        self.diz("a placa recebe momento a cada segundo")
        self.play(FadeIn(fr, shift=0.1 * UP), run_time=0.8)
        self.diz("momento por segundo é força")
        self.play(FadeIn(nf), run_time=0.5)
        self.diz("Por isso o espelho")
        self.play(Indicate(rf, color=WHITE_, scale_factor=1.1), Circumscribe(caixa(1), color=LUZ_B, buff=0.02, time_width=0.8),
                  run_time=1.0)
        self.ate(0.97)
        cn.clear_updaters()
        self.virada(est, cn, dpl, pe, fr, nf, ab, rf, self.f3p)
        self.remove(self.f3p)

    def c2_3(self):
        self.an("C-2")
        t0 = self.clk.get_value()
        self.afasta = None

        def estado(t):
            s = t - t0
            # C-3: a vela se afasta empurrada pela luz; a câmera acompanha (o alvo segue a vela) e recua um pouco, então ela encolhe
            # sem sair do PALCO nem entrar na CONTA
            da = 0.0 if self.afasta is None else t - self.afasta
            x = 0.08 * da ** 2
            K = 1.0 - 0.3 * min(1.0, da / 9.0)
            return {"abre": min(1.0, s / 6.0), "ang": 0.22 * math.sin(0.18 * s), "fase": s, "x": x, "vis_f": 1.0,
                    "cam": {"modo": "obl", "az": -120, "el": 18, "fov": 30, "K": K, "alvo": [x, 0, 0], "xc": -3.3, "yc": -0.1}}
        f3d = Fundo3D(self, "vela", estado, op=0.0)
        f3d.conta.set_value(1.0)                         # v5 (V18): fundo da CONTA escuro (degradê de x = 0,6): fótons só no PALCO
        self.add(f3d)
        self.play(f3d.op.animate.set_value(1.0), run_time=1.0)
        fseta = always_redraw(lambda: VGroup(
            arrow(P3(-2.2, -2.45), P3(-2.2 + 1.5 * min(1.0, (self.clk.get_value() - t0) / 6.0), -2.45), color=FC, width=7, tip=0.18, z=12),
            mtxt("FORÇA DA LUZ NA VELA", 15, color=FC).move_to(P3(-1.5, -2.85))))
        self.play(FadeIn(fseta), run_time=0.6)
        c1 = txt("LUZ DO SOL", 22, bold=True)
        q1 = num(r"1.361\ \mathrm{W/m^2}", WHITE_, 36)
        q2 = linha(tex(r"4{,}5\ \mu\mathrm{Pa}", FC, 38), "ABSORVIDA", size=16, buff=0.15)
        q3 = linha(tex(r"9{,}1\ \mu\mathrm{Pa}", FC, 38), "REFLETIDA", size=16, buff=0.15)
        c2 = txt("VELA SOLAR DE 100 M² REFLETORA", 20, bold=True)
        q4 = tex(r"\approx 0{,}9\ \mathrm{mN}", FC, 44)
        c3 = linha("LASER DE 1 W (ABSORVIDO):", tex(r"3{,}3\ \mathrm{nN}", FC, 40), size=20, buff=0.2)   # v5: luz absorvida
        arroz = txt("≈ PESO DE 3 A 4 GRÃOS DE ARROZ", 14, color=DIM)
        for m_, y in ((c1, 2.35), (q1, 1.8), (q2, 1.2), (q3, 0.65), (c2, -0.15), (q4, -0.75), (c3, -1.6)):
            na_conta(m_, y)
        arroz.next_to(q4, RIGHT, buff=0.3)
        self.diz("A luz do Sol chega")
        self.play(FadeIn(c1), run_time=0.5)
        self.diz("mil trezentos e sessenta e um")
        self.play(FadeIn(q1), run_time=0.6)
        self.diz("quatro vírgula cinco micropascais")
        self.play(FadeIn(q2, shift=0.1 * UP), run_time=0.6)
        self.diz("com o dobro, uns nove")
        self.play(FadeIn(q3, shift=0.1 * UP), run_time=0.6)
        self.diz("Uma vela solar refletora")
        self.play(FadeIn(c2), run_time=0.6)
        self.diz("nove décimos de milinewton")
        self.play(FadeIn(q4, shift=0.1 * UP), run_time=0.6)
        self.diz("três ou quatro grãos de arroz")
        self.play(FadeIn(arroz), run_time=0.5)
        vac = txt("NO VÁCUO, EMPURRANDO O TEMPO TODO", 16, color=DIM)
        na_conta(vac, -2.25)
        self.diz("no vácuo, não tem atrito")
        self.play(FadeIn(vac), run_time=0.5)
        self.diz("E um laser de um watt")
        self.play(FadeIn(c3[0], shift=0.1 * UP), run_time=0.6)
        self.diz("três vírgula três nanonewtons")
        self.play(FadeIn(c3[1:], shift=0.1 * UP), run_time=0.5)               # v6 (1.3): o número quando é dito
        self.ate(0.97)
        # C-3 — a vela se afasta; a frase de fechamento entra na CONTA com o PALCO trabalhando
        self.an("C-3")
        self.afasta = self.clk.get_value()
        self.play(FadeOut(VGroup(c1, q1, q2, q3, c2, q4, c3, vac, arroz)), run_time=0.6)
        a = txt("O MODELO CORPUSCULAR DO NEWTON CAIU.", 30, bold=True, color=APAGADO)
        b = txt("A CONSERVAÇÃO DO MOMENTO FICOU.", 30, bold=True, color=MAG)
        na_conta(a, 1.0); na_conta(b, 0.2)
        for m_, y_ in ((a, 1.0), (b, 0.2)):
            if m_.get_right()[0] > 7.4:
                m_.scale_to_fit_width(7.4 - XC0); na_conta(m_, y_)
        self.play(FadeIn(a, shift=0.1 * UP), run_time=0.8)
        self.diz("Mas a conservação do momento ficou")
        self.play(FadeIn(b, shift=0.1 * UP), run_time=0.8)
        v1 = txt("VALE PARA A LUZ, NA FÍSICA QUÂNTICA", 16, color=DIM)
        v2 = txt("E EM TUDO O QUE A GENTE SABE MEDIR", 16, color=DIM)
        na_conta(v1, -0.7); na_conta(v2, -1.1)
        self.diz("Ela vale para a luz")
        self.play(FadeIn(v1), run_time=0.6)
        self.diz("e vale em tudo")
        self.play(FadeIn(v2), run_time=0.6)
        self.sobra(0.55)
        fseta.clear_updaters()
        self.clear(rt=0.5)
