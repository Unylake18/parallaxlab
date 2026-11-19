"""Lote PT3: T3 — E QUANDO A MASSA É CONTÍNUA? Barra de aço fatiada em 20 fatias dx (dm = λ dx, rosa); o brilho de cada fatia ∝ x² (x = distância
ao eixo) é a assinatura do vídeo. Embaixo, o gráfico de x² com as mesmas fatias como colunas (a soma das áreas = área sob x², auditoria FATIAS).
T3-2 eixo na ponta → ML²/3; T3-3 eixo no centro → ML²/12 (duas meias-barras pela ponta); T3-4 a barra do bastão: 0,212 e 0,053 kg·m²."""
from pecas21 import *  # noqa: F401,F403

XB0, YBAR, LB, HB_ = -6.85, 1.5, 5.6, 0.46
NF = 20


class LoteT3(Lote21):
    def corpo(self):
        self.an("T3-1")
        self.secao("E QUANDO A MASSA É CONTÍNUA?")
        piv = ValueTracker(0.0)                     # eixo em fração de L (0 = ponta, 0,5 = centro)
        bri = ValueTracker(0.0)                     # brilho ∝ x² ligado
        onda = ValueTracker(-0.3)                   # v9: onda de luz que acende as fatias uma a uma (a barra é uma soma de fatias)
        self.add(piv, bri, onda)

        def barra():
            p = piv.get_value()
            b = bri.get_value()
            g = VGroup()
            corpo = Rectangle(width=LB, height=HB_).move_to(P3(XB0 + LB / 2, YBAR))
            aco(corpo, 2.0)
            g.add(corpo.set_z_index(5))
            xm = max(p, 1 - p)
            for k in range(NF):
                u = (k + 0.5) / NF
                w2 = ((u - p) / xm) ** 2
                ond = 1.0 * math.exp(-((u - onda.get_value()) / 0.2) ** 2)
                f = Rectangle(width=LB / NF, height=HB_ * (1 + 0.7 * ond)).move_to(P3(XB0 + LB * u, YBAR))
                f.set_stroke(mix(MAS, 0.3), 1.0, opacity=0.75).set_fill(MAS, min(1.0, 0.18 * (1 - b) + b * (0.08 + 0.85 * w2) + ond))
                g.add(f.set_z_index(6))
            g.add(eixo_cruz(P3(XB0 + LB * p, YBAR), 0.2))
            return g
        bv = vivo(barra)
        self.play(FadeIn(bv), run_time=0.7)
        self.play(UpdateFromAlphaFunc(piv, lambda m_, a_: m_.set_value(0.5 * float(np.sin(PI * a_)))), onda.animate(rate_func=linear).set_value(1.3), run_time=2.6)      # v6 parado 5:32: o eixo varre a barra e volta (v9: com a onda de luz)
        KSL = 15
        xs = XB0 + LB * (KSL + 0.5) / NF
        hl = Rectangle(width=LB / NF, height=HB_ + 0.12).move_to(P3(xs, YBAR)).set_stroke(WHITE_, 3).set_z_index(9)
        bdx = Brace(Line(P3(xs - LB / NF / 2, YBAR - HB_ / 2), P3(xs + LB / NF / 2, YBAR - HB_ / 2)), DOWN, buff=0.06).set_color(GEO).set_z_index(9)
        ldx = T("dx", 40).next_to(bdx, DOWN, buff=0.08)
        ldm = T(r"dm=\lambda\,dx", 42).next_to(hl, UP, buff=0.16)
        lM = VGroup(T("M,", 40), T("L", 40)).arrange(RIGHT, buff=0.15).next_to(P3(XB0 + 1.0, YBAR + HB_ / 2), UP, buff=0.16)
        self.gat("a massa é contínua")
        self.play(FadeIn(lM), run_time=0.5)
        A, ia = M("I", "=", r"\sum", "m_i", "r_i^2", size=50)
        A2, ia2 = M(r"\ \to\ ", "I", "=", r"\int", "r^2", r"\,dm", size=50)
        self.pilha.poe(A)
        self.monta(A, ia, {}, rt=0.6)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.pilha.poe(A2)
        self.gat("então a soma vira integral")
        self.play(FadeIn(hl), run_time=0.4)
        self.passo(A, A2, (J(ia, 0, 1), J(ia2, 1, 2)), (J(ia, 2), J(ia2, 3)), (J(ia, 3), J(ia2, 5)), (J(ia, 4), J(ia2, 4)), rt=1.3, origem=False)
        B, ib = M(r"\lambda", "=", r"\tfrac{M}{L}", size=50)
        self.pilha.poe(B)
        self.gat("a massa por comprimento")
        self.monta(B, ib, {2: lM})
        self.gat("cada fatia de largura d x")
        self.play(GrowFromCenter(bdx), FadeIn(ldx), run_time=0.6)
        self.play(FadeIn(ldm, shift=0.08 * UP), run_time=0.6)
        self.foco = ldm
        onda.set_value(-0.3)
        self.play(onda.animate(rate_func=linear).set_value(1.3), run_time=2.2)                  # v9: as fatias acendem uma a uma enquanto a fala fecha a ideia de dm
        onda.set_value(-0.3)
        self.play(onda.animate(rate_func=linear).set_value(1.3), run_time=2.2)
        self.ate(0.99)
        # ── T3-2: eixo na ponta, brilho ∝ x², gráfico ──
        self.an("T3-2")
        self.play(FadeOut(VGroup(hl, bdx, ldx, ldm)), run_time=0.3)
        gr = Graf(XB0, -3.05, LB, 1.0, 0, 1.0, 2.9, rot_y=T("x^2", 40), rot_x="x", cor=GEO)
        area = ValueTracker(0.0)
        self.add(area)

        def colunas(p=0.0, simet=False):
            a_ = area.get_value()
            g = VGroup()
            for k in range(NF):
                u = (k + 0.5) / NF
                if u > a_ + 1e-6 and not simet:
                    break
                x = abs(u - p)
                if simet and x > a_ * 0.5 + 1e-6:
                    continue
                h = (x / max(p, 1 - p)) ** 2 * 2.9
                r = Rectangle(width=LB / NF, height=max(h, 0.002)).move_to(P3(XB0 + LB * u, -3.05 + h / 2))
                g.add(r.set_stroke(mix(MAS, 0.3), 1.0, opacity=0.7).set_fill(MAS, 0.08 + 0.8 * (x / max(p, 1 - p)) ** 2).set_z_index(4))
            return g
        cols = vivo(lambda: colunas(piv.get_value(), piv.get_value() > 0.25))
        curva = gr.curva(lambda x: x * x, 0, 1.0, cor=MAS, w=4)
        self.add(cols)
        self.gat("eixo na ponta da barra")
        self.play(FadeIn(gr.eixos), Create(curva), run_time=0.8)
        self.vivos = [curva, gr.eixos]
        self.play(Indicate(bv, scale_factor=1.04, color=WHITE_), run_time=1.3)      # v6 parado 6:02
        self.play(Indicate(bv, scale_factor=1.04, color=WHITE_), run_time=1.3)
        lx = T("x", 40)
        lx.add_updater(lambda m: m.next_to(P3(XB0 + LB * 0.5, YBAR - HB_ / 2), DOWN, buff=0.14))
        lin_x = Line(P3(XB0, YBAR - HB_ / 2 - 0.12), P3(XB0 + LB * 0.75, YBAR - HB_ / 2 - 0.12)).set_stroke(GEO, 2.4)
        self.gat("a fatia que está a uma distância x")
        self.play(Create(lin_x), FadeIn(lx), run_time=0.9)
        C_, ic = M("I", "=", r"\int_0^L", "x^2", r"\tfrac{M}{L}", r"\,dx", size=50)
        self.pilha.limpa(rt=0.3)
        self.pilha.poe(C_)
        self.gat("contribui com x ao quadrado")
        def cresce(m_, dt):                                          # v6 parado 6:02: as colunas x² começam a somar durante a montagem da integral
            m_.set_value(min(0.85, m_.get_value() + dt / 7.5))
            if m_.get_value() >= 0.85:
                m_.clear_updaters()
        area.add_updater(cresce)
        bri.set_value(1.0)
        self.monta(C_, ic, {3: lx, 4: mp(B, ib, [2]) if B in self.mobjects else lM})
        self.gat("integra de zero até l")
        self.play(area.animate.set_value(1.0), run_time=3.2, rate_func=linear)
        D_, id_ = M("=", r"\tfrac{M}{L}", r"\cdot", r"\tfrac{L^3}{3}", size=50)
        self.pilha.poe(D_)
        self.gat("a integral de x ao quadrado")
        self.passo(C_, D_, (J(ic, 1), J(id_, 0)), (J(ic, 4), J(id_, 1)), rt=1.1, origem=False)
        E_, ie = M("I", "=", r"\tfrac{ML^2}{3}", size=56)
        Eb = caixa_l(E_, MAS)
        self.pilha.poe(Eb)
        self.gat("e sobra a massa vezes o comprimento")
        self.cx(Eb[0])
        self.passo(D_, E_, (J(id_, 0), J(ie, 1)), rt=1.2, origem=False)
        soma = sum(((k + 0.5) / NF) ** 2 / NF for k in range(NF))
        self.reg("fatias_ponta", soma=soma, integral=1 / 3)
        self.gat("olha o brilho das fatias")
        self.play(self.ind_copia(bv, WHITE_, 1.02, 0.8), run_time=0.8)
        lx.clear_updaters()
        self.play(FadeOut(lx), FadeOut(lin_x), FadeOut(curva), area.animate.set_value(0.0), run_time=0.35)
        self.pilha.so(C_, Eb)
        self.foco = Eb
        self.ate(0.99)
        # ── T3-3: eixo no centro ──
        self.an("T3-3")
        self.gat("agora o eixo no centro")
        self.play(piv.animate.set_value(0.5), run_time=1.2)
        gr2c = gr.curva(lambda x: ((x - 0.5) / 0.5) ** 2, 0, 1.0, cor=MAS, w=4)
        self.play(Create(gr2c), area.animate.set_value(1.0), run_time=1.4)
        F_, if_ = M("I", "=", r"\int_{-L/2}^{L/2}", "x^2", r"\tfrac{M}{L}", r"\,dx", "=", r"\tfrac{ML^2}{12}", size=48)
        self.pilha.poe(F_)
        self.gat("os limites vão de menos l sobre dois")
        self.passo(C_, F_, (J(ic, 0), J(if_, 0)), (J(ic, 1), J(if_, 1)), (J(ic, 3), J(if_, 3)), (J(ic, 4), J(if_, 4)), (J(ic, 5), J(if_, 5)), rt=1.3, origem=False)
        self.gat("dá m l ao quadrado sobre doze")
        self.play(FadeIn(mp(F_, if_, [6, 7])), run_time=0.7)
        soma_c = sum((abs((k + 0.5) / NF - 0.5)) ** 2 / NF for k in range(NF))
        self.reg("fatias_centro", soma=soma_c, integral=1 / 12, razao=soma_c / soma)
        self.selo("QUATRO VEZES MENOR", ["QUE PELA PONTA"])
        # duas meias-barras pela ponta
        sep = ValueTracker(0.0)
        self.add(sep)
        bv.clear_updaters()
        meias = vivo(lambda: VGroup(*[barra_fatias(XB0 + (0 if s < 0 else LB / 2) + s * sep.get_value(), YBAR, LB / 2, HB_, NF // 2, piv=(1.0 if s < 0 else 0.0))
                                      for s in (-1, 1)], eixo_cruz(P3(XB0 + LB / 2 - sep.get_value(), YBAR), 0.17),
                                    eixo_cruz(P3(XB0 + LB / 2 + sep.get_value(), YBAR), 0.17)))
        self.gat("são duas meias-barras")
        self.remove(bv)
        self.add(meias)
        self.play(sep.animate.set_value(0.35), FadeOut(lM), run_time=1.0)
        lh = VGroup(T(r"\tfrac{M}{2},\ \tfrac{L}{2}", 40).next_to(P3(XB0 + LB / 4 - 0.35, YBAR + HB_ / 2), UP, buff=0.16),
                    T(r"\tfrac{M}{2},\ \tfrac{L}{2}", 40).next_to(P3(XB0 + 3 * LB / 4 + 0.35, YBAR + HB_ / 2), UP, buff=0.16))
        self.play(FadeIn(lh), run_time=0.6)
        G_, ig = M("I", "=", "2", r"\cdot", r"\tfrac{1}{3}", r"\tfrac{M}{2}", r"\big(\tfrac{L}{2}\big)^2", "=", r"\tfrac{ML^2}{12}", size=48)
        self.pilha.poe(G_)
        self.gat("metade da massa")
        self.monta(G_, ig, {5: lh[0][0][:3], 6: lh[1][0][4:]})
        self.foco = G_
        self.ate(0.99)
        # ── T3-4: a barra do bastão ──
        self.an("T3-4")
        meias.clear_updaters()
        self.sem_selo()
        velhos = [meias, cols, gr.eixos, gr2c, lh]
        cols.clear_updaters()
        self.pilha.limpa(rt=0.3)
        self.guia(['PERGUNTA:', 'A MESMA BARRA: PELA PONTA', 'OU PELO CENTRO?'])                                      # v6 G4: a coluna da direita não fica vazia
        Y1, Y2 = 1.1, -1.6
        b1 = VGroup(barra_fatias(-6.6, Y1, 5.0, 0.42, NF, piv=0.0), eixo_cruz(P3(-6.6, Y1), 0.18))
        b2 = VGroup(barra_fatias(-6.6, Y2, 5.0, 0.42, NF, piv=0.5), eixo_cruz(P3(-4.1, Y2), 0.18))
        dados = VGroup(T("M=", 38), nm(r"0{,}90\ \mathrm{kg}", MAS, 38), T(r",\ L=", 38), nm(r"0{,}84\ \mathrm{m}", GEO, 38)).arrange(RIGHT, buff=0.08)
        dados.next_to(b1, UP, buff=0.3).align_to(b1, LEFT)
        lp = txt("PELA PONTA", 26).next_to(b1, DOWN, buff=0.2).align_to(b1, LEFT)
        lc = txt("PELO CENTRO", 26).next_to(b2, DOWN, buff=0.2).align_to(b2, LEFT)
        self.troca(velhos, FadeIn(b1), FadeIn(b2), FadeIn(lp), FadeIn(lc), seq=True)
        self.gat("distribuída uniformemente")
        self.play(FadeIn(dados), run_time=0.6)
        H1, ih1 = M(r"I_{ponta}", "=", r"\tfrac{ML^2}{3}", "=", r"0{,}212\ \mathrm{kg\cdot m^2}", size=46, cores={4: MAS})
        ML_ = VGroup(dados[0][0][:1], dados[2][0][1:2])
        H2, ih2 = M(r"I_{centro}", "=", r"\tfrac{ML^2}{12}", "=", r"0{,}053\ \mathrm{kg\cdot m^2}", size=46, cores={4: MAS})
        self.pilha.poe(H1)
        self.pilha.poe(H2)
        self.gat("pela ponta o momento de inércia seria")
        self.monta(H1, ih1, {2: ML_, 4: VGroup(dados[1], dados[3])}, rt=1.4)
        self.gat("pelo centro zero vírgula zero cinco três")
        self.monta(H2, ih2, {2: ML_, 4: VGroup(dados[1], dados[3])}, rt=1.4)
        self.reg("t3_4", ponta=NUM["barra_ponta"], centro=NUM["barra_centro"])
        self.gat("mesmo corpo dois eixos")
        self.selo("MESMA BARRA, DOIS EIXOS", ["OUTRO I"])
        self.gat("o nosso bastão de verdade não é uniforme")
        self.play(self.ind_copia(H1, WHITE_, 1.06, 0.8), self.ind_copia(H2, WHITE_, 1.06, 0.8), run_time=0.8)
        self.foco = H2
        self.ate(0.99)
