"""Lote PS: S1 (quatro cartões com as descobertas), S2 (método em uma linha, carretel girando devagar atrás), EN1 (logo + inscrição) e
EN2 (desafio do bloco de 20 kg com o volante pequeno no canto). Sem prévia de próximo vídeo."""
from pecas23 import *  # noqa: F401,F403
from icones25 import ic25


class LotePS(Lote23):
    def corpo(self):
        # ── S1 ──
        self.an("S1")
        self.secao("RESUMO")
        xs = (-3.75, 3.75)
        ys = (1.2, -1.85)
        specs = [
            ("no volante", 0, MAS, "VOLANTE", [lbl(r"a=\frac{g}{1+I/(m\,r^2)}", None, 40)], "INÉRCIA EXTRA, NÃO FORÇA EXTRA"),
            ("na haste", 1, FC, "HASTE", [lbl(r"\tfrac{4}{7}\,Mg\ \longrightarrow\ \tfrac{13}{7}\,Mg", FC, 42)], "A FORÇA NO EIXO MUDA NA QUEDA"),
            ("no carretel", 2, FC, "CARRETEL", [lbl(r"m_1R\ \gtrless\ m_2r", None, 44)], "TRAÇÕES NO CARRETEL, PESOS NO SISTEMA"),
            ("e no pêndulo", 3, WHITE_, "PÊNDULO", [VGroup(lbl(r"l=\frac{R}{\sqrt{2}}", None, 38), M("T_{min}", "=", r"2\pi\sqrt{\frac{\sqrt{2}R}{g}}", size=38, cores={0: WHITE_})[0]).arrange(RIGHT, buff=0.4)], "TORQUE E I COMO FERRAMENTA DE PROJETO"),
        ]
        cards = []
        for k, (fr, ic_k, cor, nome, formula, frase) in enumerate(specs):
            self.gat(fr)
            ic = ic25(ic_k, ORIGIN)
            ic.scale(min(1.3 / ic.width, 1.3 / ic.height))
            for f_ in formula:
                f_.scale(1.25)
            linhas_f = quebra(frase, 30, 5.2)
            corpo = VGroup(txt(nome, 32, bold=True, color=cor if cor != WHITE_ else GEO), *formula,
                           *[txt(l_, 30, bold=True, color=GEO) for l_ in linhas_f]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            if corpo.width > 5.3:
                corpo.scale_to_fit_width(5.3)
            g = VGroup(ic, corpo).arrange(RIGHT, buff=0.3)
            c = cartao23(g, cor if k != 2 else MAS, w=7.2)
            c[0].stretch_to_fit_width(7.2).stretch_to_fit_height(2.9)          # v6: as quatro caixas com o mesmo tamanho, conteúdo centrado
            if c[1].height > 2.5:
                c[1].scale_to_fit_height(2.5)
            c[1].move_to(c[0].get_center())
            c.move_to(P3(xs[k % 2], ys[k // 2]))
            self.play(FadeIn(c, shift=0.12 * UP), run_time=0.7)
            cards.append(c)
        self.ate(0.99)

        # ── S2: método em uma linha; carretel (ícone) girando devagar atrás ──
        self.an("S2")
        self.secao("O MÉTODO")
        ang = ValueTracker(0.0)
        ang.add_updater(lambda m, dt: m.increment_value(0.25 * dt))
        self.add(ang)

        def car_():
            c0 = P3(-5.7, 0.55)
            return VGroup(carretel25(c0, 1.3, 0.46, ang.get_value())).set_z_index(2)

        car = vivo(car_)
        self.play(*[c.animate.scale(0.55).set_opacity(0.0) for c in cards], FadeIn(car), run_time=0.7)
        self.remove(*cards)
        passos = ["DESENHA O SISTEMA", "ESCOLHE O EIXO", "ESCREVE AS EQUAÇÕES", "APLICA OS VÍNCULOS", "CONFERE"]
        frases = ["identifica as forças", "escolhe o eixo", "escreve as equações", "usa os vínculos", "depois confere"]
        itens = VGroup(*[txt(p, 32, bold=True, color=(ACC if k == 4 else WHITE_)) for k, p in enumerate(passos)])
        setas_ = VGroup(*[T(r"\rightarrow", 40, CYAN) for _ in range(4)])
        r1 = VGroup(itens[0], setas_[0], itens[1], setas_[1], itens[2]).arrange(RIGHT, buff=0.2)
        r2 = VGroup(setas_[2], itens[3], setas_[3], itens[4]).arrange(RIGHT, buff=0.2)
        VGroup(r1, r2).arrange(DOWN, buff=0.35).move_to(P3(0, -2.05))
        cab = txt("COMEÇA PELA FÍSICA, NÃO PELA FÓRMULA", 36, bold=True, color=CYAN).move_to(P3(0, 2.75))
        self.gat("começa pela física")
        self.play(FadeIn(cab, shift=0.1 * UP), run_time=0.6)
        for k, fr in enumerate(frases):
            self.gat(fr)
            anims = [FadeIn(itens[k], shift=0.08 * UP)]
            if k > 0:
                anims.append(FadeIn(setas_[k - 1]))
            self.play(*anims, run_time=0.5)
        conf = VGroup(txt("CONFERE: ENERGIA · SENTIDOS · CASOS-LIMITE · OUTRO CAMINHO", 30, bold=True, color=GEO)).move_to(P3(0, -3.45))
        self.gat("pela energia")
        self.play(FadeIn(conf, shift=0.08 * UP), run_time=0.6)
        self.ate(0.99)

        # ── EN1 ──
        self.an("EN1")
        velhos = [m for m in (car, cab, itens, setas_, conf) if m is not None]
        self.play(*[FadeOut(m) for m in velhos], run_time=0.5)
        ang.clear_updaters()
        self.remove(*velhos)
        self.secao(None)
        CL = P3(0, 1.4)
        logo = self.logo(4.6).move_to(CL)
        t_en = self.clk.get_value()

        def ondas():
            t = self.clk.get_value() - t_en
            g = VGroup()
            for k in range(3):
                ph = (t / 2.4 + k / 3) % 1.0
                g.add(Circle(radius=1.0 + 0.4 * ph).move_to(CL).set_stroke(VEL, 3.0, opacity=0.5 * math.sin(math.pi * ph)))
            return g

        ov = vivo(ondas)
        ins = VGroup(txt("INSCREVA-SE PARA ACOMPANHAR", 44, bold=True), txt("OS PRÓXIMOS VÍDEOS", 44, bold=True)).arrange(DOWN, buff=0.12).move_to(P3(0, -1.9))
        self.play(FadeIn(logo, scale=0.95), FadeIn(ov), run_time=0.7)
        self.gat("se inscreve no parallax lab")
        self.play(FadeIn(ins, shift=0.1 * UP), run_time=0.7)
        self.gat("um desafio para os comentários")
        self.play(Indicate(ins, color=ACC, scale_factor=1.04), run_time=0.9)
        self.ate(0.99)

        # ── EN2: desafio ──
        self.an("EN2")
        self.secao("DESAFIO")
        self.play(FadeOut(logo), FadeOut(ov), FadeOut(ins), run_time=0.5)
        ov.clear_updaters()
        aV = ValueTracker(0.0)
        aV.add_updater(lambda m, dt: m.increment_value(0.4 * dt))
        self.add(aV)

        def vol():
            o_ = P3(-4.6, 0.9)
            xt_ = o_[0] + 0.158 * 3.4
            return VGroup(volante25(o_, 3.4, aV.get_value()), Line([xt_, o_[1], 0], [xt_, o_[1] - 2.35, 0]).set_stroke("#D8E2F5", 2.6).set_z_index(4.9), bloco25(np.array([xt_, o_[1] - 2.65, 0.0]), 0.55)).set_z_index(4)

        vv = vivo(vol)
        l20 = lbl(r"20\ \mathrm{kg}", MAS, 44).move_to(P3(-4.6 + 0.158 * 3.4 + 1.3, 0.9 - 2.65))
        l10 = lbl(r"10\ \mathrm{kg}", MAS, 44).move_to(l20.get_center())
        self.play(FadeIn(vv), FadeIn(l10), run_time=0.6)
        self.gat("troca o bloco de dez quilos por um de vinte")
        self.play(Transform(l10, l20), run_time=0.7)
        des = cartao23(VGroup(txt("DESAFIO", 34, bold=True, color=MAS), txt("A ACELERAÇÃO DOBRA?", 40, bold=True, color=ACC)).arrange(DOWN, buff=0.16), MAS, w=6.6).move_to(P3(3.3, 1.3))
        self.gat("a aceleração dobra")
        self.play(FadeIn(des, shift=0.1 * UP), run_time=0.7)
        self.gat("usa a fórmula que a gente guardou")
        F_ = lbl(r"a=\frac{g}{1+I/(m\,r^2)}", None, 54)
        bx = caixa_l(F_, ACC).move_to(P3(3.3, -1.35))
        self.play(FadeIn(bx[0]), Write(F_), run_time=1.0)
        self.gat("escreve sua resposta e seu raciocínio")
        com = txt("RESPOSTA NOS COMENTÁRIOS", 30, bold=True, color=CYAN).move_to(P3(3.3, -3.0))
        self.play(FadeIn(com, shift=0.08 * UP), run_time=0.6)
        self.ate(0.99)
