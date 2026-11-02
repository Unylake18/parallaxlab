"""yt_0019 v10: o fecho. FIM-1 = gancho do vídeo de colisões em 1D (a colisão totalmente inelástica do yt_0013, com as barras de energia, refeita aqui no padrão
visual deste vídeo: não importa nada da unidade do yt_0013) e FIM-2 = cartão final (logo + INSCREVA-SE + moldura livre para o elemento de vídeo do YouTube).
Só números que já estavam no vídeo: nenhuma grandeza nova na tela (as barras são relativas)."""
from pecas19 import *  # noqa: F401,F403


class FechoMixin:
    def gancho(self):
        self.an("FIM-1")
        velhos = self.snap()
        self.secao(None)
        w, u_, YT = 1.3, 1.6, -1.5                       # largura dos corpos, velocidade (tela/s) e base do trilho
        t = ValueTracker(-2.2)
        modo = ValueTracker(0.0)                          # 0 = totalmente inelástica (colam), 1 = elástica (trocam as velocidades)
        op = ValueTracker(1.0)
        pop = ValueTracker(0.0)                           # setas de momento
        self.add(t, modo, op, pop)

        def vel_(tt, mm):
            if tt <= 0:
                return u_, 0.0
            return (0.5 * u_, 0.5 * u_) if mm < 0.5 else (0.0, u_)

        def xs():
            tt, mm = t.get_value(), modo.get_value()
            va, vb = vel_(tt, mm)
            return -w / 2 + va * tt, w / 2 + vb * tt

        A, B = Corpo("m", GEO, w), Corpo("m", STEEL, w)
        A.add_updater(lambda m: m.at(xs()[0], YT).set_opacity(op.get_value()))
        B.add_updater(lambda m: m.at(xs()[1], YT).set_opacity(op.get_value()))
        trilho = Line(P3(-6.6, YT), P3(6.6, YT)).set_stroke(WHITE_, 2.5, opacity=0.4)
        L0 = 3.6                                          # comprimento da barra com K = K antes do choque
        zx, yK, yP = -2.6, 1.45, 0.65

        def barraK():
            tt, mm = t.get_value(), modo.get_value()
            K = 1.0 if (tt <= 0 or mm > 0.5) else 0.5
            g = VGroup(Rectangle(width=max(L0 * K, 1e-3), height=0.3, stroke_width=0, fill_color=KC, fill_opacity=0.9).move_to(P3(zx + L0 * K / 2, yK)))
            if K < 0.99:
                g.add(Rectangle(width=L0 * (1 - K), height=0.3, stroke_width=0, fill_color=HEAT, fill_opacity=0.85).move_to(P3(zx + L0 * K + L0 * (1 - K) / 2, yK)))
            return g.set_opacity(op.get_value())
        kbar = always_redraw(barraK)
        pan = placa(8.8, 2.1, P3(0.0, 1.05), op=0.05)
        lK = txt("K", T_LAB, color=KC, bold=True).move_to(P3(zx - 0.55, yK))
        lH = txt("CALOR", T_SMALL, color=HEAT).move_to(P3(zx + L0 + 0.95, yK))
        lH.add_updater(lambda m: m.set_opacity(0.0 if (t.get_value() <= 0 or modo.get_value() > 0.5) else 1.0))
        lP = txt("P", T_LAB, color=MAG, bold=True).move_to(P3(zx - 0.55, yP))
        zero = Line(P3(zx, yP - 0.25), P3(zx, yP + 0.25)).set_stroke(WHITE_, 1.5, opacity=0.5)
        pseta = always_redraw(lambda: arrow(P3(zx, yP), P3(zx + 2.0 * max(pop.get_value(), 0.002), yP), color=MAG, width=8, tip=0.22).set_opacity(min(1.0, pop.get_value() * 4)))

        def p_corpos():
            xa, xb = xs()
            va, vb = vel_(t.get_value(), modo.get_value())
            g = VGroup()
            for x, v in ((xa, va), (xb, vb)):
                if abs(v) > 0.05:
                    g.add(arrow(P3(x, YT - 0.45), P3(x + v * 0.75, YT - 0.45), color=MAG, width=7, tip=0.2))
            return g.set_opacity(pop.get_value())
        pc = always_redraw(p_corpos)
        selo_ = VGroup(RoundedRectangle(corner_radius=0.14, width=5.6, height=0.8).set_fill(PANEL, 0.88).set_stroke(CYAN, 2.5),
                       txt("COLISÕES EM 1D", 34, bold=True, color=WHITE_)).move_to(P3(0.0, 2.75))
        selo_[1].move_to(selo_[0])
        selo_.set_z_index(25)
        self.troca(velhos, FadeIn(VGroup(trilho, pan, lK, lP, zero, lH)), FadeIn(A), FadeIn(B), FadeIn(kbar), seq=True)
        self.add(pseta, pc)
        self.foco = A

        def volta(m):                                       # recomeça o ANTES, mais perto: os corpos somem, reposicionam e voltam
            self.play(op.animate.set_value(0.0), run_time=0.2)
            t.set_value(-1.0)
            modo.set_value(m)
            self.play(op.animate.set_value(1.0), run_time=0.2)

        def corrida(depois=1.1):
            self.play(t.animate(rate_func=linear).set_value(0.0), run_time=max(0.3, -t.get_value() / u_))
            fl = flash(P3(0.0, YT + 0.5 * w), r=0.18)
            self.play(FadeIn(fl), run_time=0.15)
            t.set_value(1e-5)
            self.play(FadeOut(fl), t.animate(rate_func=linear).set_value(depois), run_time=depois / u_ * 0.9)

        def ate_frase(frase):
            """Segundos que faltam, na voz real, até a palavra que abre `frase` (menos o LEAD)."""
            k = self._k_frase(self._aid, frase)
            a = ANC[self._aid]
            return max(0.3, (round(a["ini"] * FPS) - self._off + (a["t"][k] - LEAD) * FPS - self.nq) / FPS)

        self.play(t.animate(rate_func=linear).set_value(-0.9), run_time=1.0)                   # "Lembra da areia na esteira?": os corpos se aproximam
        self.gat("metade da energia virou calor")
        t.set_value(-1.0)
        corrida(depois=1.9)
        self.gat("porque o grão bate")
        self.play(A.animate(rate_func=there_and_back).scale(1.12), B.animate(rate_func=there_and_back).scale(1.12), run_time=0.8)
        self.gat("até pegar a velocidade da esteira")
        self.play(Indicate(lH, color=HEAT, scale_factor=1.25), run_time=0.8)
        self.gat("esse tipo de perda")
        d_ = ate_frase("o das colisões")                         # os corpos seguem juntos, devagar, até a voz nomear o vídeo
        self.play(t.animate(rate_func=linear).set_value(t.get_value() + 0.5 * u_ * d_), run_time=d_, fixo=True)
        self.gat("o das colisões")
        self.play(FadeIn(selo_, shift=0.1 * DOWN), run_time=0.4)
        self.foco = selo_
        self.gat("quando a energia se conserva")
        volta(1.0)
        corrida()
        self.gat("quando ela vira calor")
        volta(0.0)
        corrida()
        self.gat("o que o momento garante")
        volta(0.0)
        self.play(pop.animate.set_value(1.0), run_time=0.4)
        corrida()
        self.ate(0.99)

    def cartao_final(self):
        self.an("FIM-2")
        velhos = self.snap()
        self.secao(None)
        clk = self.clk
        cx, cy = -3.5, 0.55
        logo = self.logo(5.2).move_to(P3(cx, cy + 0.5))
        ar = [(2.5, 0.3), (2.95, 0.18)]
        aneis = VGroup(*[Circle(radius=r).move_to(P3(cx, cy + 0.5)).set_stroke(VEL, 2, opacity=o) for r, o in ar])
        aneis.add_updater(lambda g: [m.set_width(2 * (ar[k][0] + 0.08 * math.sin(clk.get_value() * 1.6 + k))) for k, m in enumerate(g)])
        ins = txt("INSCREVA-SE", 40, bold=True, color=CYAN).move_to(P3(cx, -2.55))
        fr = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=6.2, height=3.49).set_stroke(WHITE_, 2.5, opacity=0.55).move_to(P3(3.65, 0.75)), num_dashes=70)
        lc = txt("VÍDEO DE COLISÕES", 30, bold=True).move_to(P3(3.65, -1.45))
        self.troca(velhos, FadeIn(logo, scale=0.95), FadeIn(aneis), seq=True)
        self.gat("se inscreva no parallax lab")
        self.play(FadeIn(ins, shift=0.1 * UP), run_time=0.6)
        self.foco = ins
        self.gat("o vídeo de colisões")
        self.play(FadeIn(fr), FadeIn(lc, shift=0.1 * UP), run_time=0.7)
        self.foco = lc
        fr.add_updater(lambda m: m.set_opacity(0.78 + 0.22 * math.sin(clk.get_value() * 2.2)))
        self.ate(0.99)
