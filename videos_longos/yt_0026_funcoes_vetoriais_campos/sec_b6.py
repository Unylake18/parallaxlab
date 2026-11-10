"""Lote PB6 · DE VOLTA AO REDEMOINHO (B6-1…B6-7): F⃗ = −y i⃗ + x j⃗ desenhado com três perguntas (valores; ‖F⃗‖ = r constante nas circunferências;
F⃗ · X = 0, perpendicular ao vetor posição); trajetórias γ(t) = r(cos t, sen t) com γ′(t) = F⃗(γ(t)) (seta violeta pousa sobre a ciano);
disco rígido a 1 rad/s; a bandeira gira com o campo por t = π/2 e para na silhueta da rotação de 90°.
v3 §3.3: setas SOBRE as circunferências de raio 1, 2 e 2,5 (8, 12 e 16 setas), fator K = 0,5 no lote inteiro (comprimentos 0,5 / 1,0 / 1,25)."""
from kit import *  # noqa: F401,F403
from MF_Tools import TransformByGlyphMap

XF = 3.8
K = 0.4
GIRO = lambda x, y: (-y, x)
ANEIS = ((1.0, 8), (2.0, 12), (2.5, 12))
FMAX = 2.5        # maior ‖F‖ da cena (raio 2,5): a cor de cada seta é a intensidade ‖F‖/FMAX


def circ_pts(r, n):
    return [(round(r * math.cos(2 * PI * k / n), 9) + 0.0, round(r * math.sin(2 * PI * k / n), 9) + 0.0) for k in range(n)]


def aneis_campo(ax, quais, nome, w=4.0):
    """Setas do giro sobre as circunferências (mesma escala K); o log usa o arco entre setas vizinhas como espaçamento."""
    return VGroup(*[campo(ax, GIRO, circ_pts(r, n), K, f"{nome} r={r}", w=w, passo=2 * PI * r / n, fmax=FMAX) for r, n in quais])


def marca(n, y, rot):
    """Número em círculo + rótulo curto em caixa alta acima dele (v5 §1.4): 1 · VALORES, 2 · TAMANHO, 3 · DIREÇÃO."""
    c = Circle(radius=0.26).set_stroke(GEO, 2).set_fill(BG, 0.6).move_to(P3(0.95, y))
    r = txt(f"{n} · {rot}", 22, bold=True, color=GEO).move_to(ORIGIN).align_to(P3(0.69, 0), LEFT).align_to(P3(0, y + 0.52), DOWN)
    return VGroup(c, txt(str(n), 26, bold=True).move_to(c), r)


class LoteB6(Base):
    def corpo(self):
        ax = eixos((-3, 0), [-3, 3, 1], [-3, 3, 1], 1.0)
        O = ax.c2p(0, 0)

        # ── B6-1 · a regra do começo ──
        self.an("B6-1")
        self.secao("DE VOLTA AO REDEMOINHO")
        self.play(Create(ax), run_time=1.0)
        fF = F((r"\vec F", CAMPO), "(", ("x", E1), ",", ("y", E2), ")", "=", "-", ("y", E2), r"\,\vec i", "+", ("x", E1), r"\,\vec j", size=M_XL).move_to(P3(XF, 2.5))
        self.gat("a regra que troca as coordenadas")
        self.play(caneta(fF))
        pl = Plano(P3(XF, -0.9), 0.32)
        mm = VGroup(malha(pl, -3, 3, -3, 3, 1.0, w=1.5), bandeira(pl))
        self.gat("como transformação ela leva")
        self.play(FadeIn(mm), run_time=0.6)
        self.play(Rotate(mm, PI / 2, about_point=pl.c2p(0, 0)), run_time=2.0)
        self.gat("vamos desenhar sem decorar nada")
        self.play(FadeOut(mm), run_time=0.5)
        self.remove(mm)

        # ── B6-2 · 1: valores em quatro pontos ──
        self.an("B6-2")
        m1 = marca(1, 1.05, "VALORES")
        self.play(FadeIn(m1), run_time=0.4)
        quatro = VGroup()
        PTS = (((1, 0), "à direita da origem"), ((0, 1), "no ponto uma unidade acima"), ((-1, 0), "à esquerda da origem"), ((0, -1), "embaixo para a direita"))
        feitos = []

        def entra(x, y):
            d = ponto(ax.c2p(x, y), GEO, 0.06)
            s = campo(ax, GIRO, [(x, y)], K, f"B6-2 ({x}, {y})", w=4.5, fmax=FMAX)
            quatro.add(d, s)
            return AnimationGroup(FadeIn(d, scale=0.5), GrowArrow(s[0]), run_time=0.7)
        # v5 §1.4: o 1 também tem fórmula, escrita junto com as duas primeiras frases
        f1 = F((r"\vec F", CAMPO), "(", ("1", E1), ",", ("0", E2), ")", "=", (r"\vec j", CAMPO), size=M_L).move_to(ORIGIN).align_to(P3(2.9, 0), LEFT).align_to(P3(0, 1.2), DOWN)
        f2 = F((r"\vec F", CAMPO), "(", ("0", E1), ",", ("1", E2), ")", "=", "-", (r"\vec i", CAMPO), size=M_L).move_to(ORIGIN).align_to(P3(2.9, 0), LEFT).align_to(P3(0, 0.45), DOWN)
        self.gat(PTS[0][1])
        self.play(entra(*PTS[0][0]))
        for i, (fx, trig) in enumerate(((f1, "a seta aponta para cima"), (f2, "aponta para a esquerda"))):
            self.gat(trig)
            w = self.falta(PTS[i + 1][1])
            cf = caneta(fx)
            nx = entra(*PTS[i + 1][0])
            self.play(cf, Succession(Wait(w), nx), run_time=max(cf.tot, w + 0.7))
        self.gat(PTS[3][1])
        self.play(entra(*PTS[3][0]))
        self.gat("já dá para sentir o giro")
        self.play(pulso(quatro, 1.15), run_time=1.0)

        # ── B6-3 · 2: ‖F⃗‖ constante em cada circunferência ──
        self.an("B6-3")
        m2 = marca(2, -0.35, "TAMANHO")
        self.play(FadeIn(m2), run_time=0.4)
        n3 = F(r"\|", (r"\vec F", CAMPO), r"\|", "=", r"\sqrt{", ("x", E1), "^2+", ("y", E2), "^2}", size=M_L).move_to(P3(XF + 0.35, -0.35))
        self.gat("o tamanho dessa seta é a raiz")
        self.play(caneta(n3))
        circ = VGroup(*[tracejado(Circle(radius=r).move_to(O), GEO, W_GUIA, 0.85) for r in (1, 2)])
        aneis = aneis_campo(ax, ANEIS[:2], "B6-3 anel")
        self.gat("em cada circunferência centrada")
        self.play(FadeOut(quatro), FadeOut(VGroup(f1, f2)), Create(circ), run_time=0.9)
        self.remove(quatro, f1, f2)
        self.play(LaggedStart(*[FadeIn(a) for a in aneis], lag_ratio=0.4), run_time=1.6)

        # ── B6-4 · 3: perpendicular ao vetor posição; o campo completo ──
        self.an("B6-4")
        m3 = marca(3, -1.75, "DIREÇÃO")
        self.play(FadeIn(m3), aneis.animate.set_opacity(0.3), circ.animate.set_stroke(opacity=0.35), run_time=0.5)
        P = circ_pts(2.0, 12)[1]                               # (√3, 1): uma das 12 setas do raio 2
        pos = seta(O, ax.c2p(*P), POS, 4.5, tip=0.2)
        fP = campo(ax, GIRO, [P], K, "B6-4 em (√3, 1)", w=4.5, fmax=FMAX)
        self.gat("para onde a seta aponta")
        self.play(GrowArrow(pos), run_time=0.8)
        self.play(GrowArrow(fP[0]), run_time=0.6)
        u = np.array([*P, 0.0]) / math.hypot(*P)
        v = np.array([*GIRO(*P), 0.0]) / math.hypot(*P)
        q = ax.c2p(*P)
        ang = VMobject().set_points_as_corners([q - 0.2 * u, q - 0.2 * u + 0.2 * v, q + 0.2 * v]).set_stroke(GEO, 2.2, 0.9)
        prod = F((r"\vec F", CAMPO), r"\cdot", ("(", POS), ("x", E1), (",", POS), ("y", E2), (")", POS), "=", "-", ("y", E2), ("x", E1), "+", ("x", E1), ("y", E2),
                 "=", "0", size=M_L).move_to(P3(XF + 0.35, -1.75))
        self.gat("faz o produto escalar")
        self.play(caneta(prod))
        self.gat("quer dizer perpendicular")
        self.play(Create(ang), run_time=0.6)
        cheio = VGroup(*[s for g_ in aneis_campo(ax, ANEIS, "B6 giro completo", w=3.5) for s in g_])
        self.gat("junta as três respostas")
        self.play(FadeOut(VGroup(pos, fP, ang, aneis)), run_time=0.4)
        self.remove(pos, fP, ang, aneis)
        self.play(LaggedStart(*[GrowArrow(s) for s in sorted(cheio, key=lambda s: math.hypot(*s._xy))], lag_ratio=0.03), run_time=2.0)

        # ── B6-5 · trajetórias: γ′(t) = F⃗(γ(t)) ──
        self.an("B6-5")
        self.play(FadeOut(VGroup(m1, m2, m3, n3, prod)), circ.animate.set_stroke(opacity=0.0), run_time=0.5)
        self.remove(m1, m2, m3, n3, prod, circ)
        R = 2.0
        traj = Circle(radius=R).move_to(O).set_stroke(POS, W_GAMA)
        dot = ponto(ax.c2p(R, 0), POS, 0.09, z=7)
        g = Fs(r"\gamma(t) = (r\cos t,\ r\,\mathrm{sen}\,t)", {POS: [0, 5, 11, 17]}, size=M_L).move_to(P3(XF, 0.9))
        self.gat("lê o campo como velocidade")
        self.play(Create(traj), FadeIn(dot), run_time=0.9)
        self.gat("de quem passa por ali")                       # v3 §3.6: a caneta começa antes para o GM cair na palavra "derivada"
        cg = caneta(g)
        self.play(cg, Rotate(dot, 2 * PI, about_point=O, rate_func=linear), run_time=cg.tot)       # escreve γ enquanto o ponto dá a volta
        gd = Fs(r"\gamma'(t) = (-r\,\mathrm{sen}\,t,\ r\cos t)", {VEL: [0, 1, 6, 13, 19]}, size=M_L)
        gd.next_to(g, DOWN, buff=0.35).align_to(g, LEFT)
        g2 = Fs(r"= \vec F(\gamma(t))", {CAMPO: [1, 2], POS: [4]}, size=M_L)
        g2.next_to(gd, DOWN, buff=0.3).align_to(gd[0][5], LEFT)
        vel = seta(ax.c2p(R, 0), ax.c2p(R, K * R), VEL, W_VEL, tip=0.24, brilho=True).set_z_index(8)
        alvo_c = [s for s in cheio if s._xy == (2.0, 0.0)][0]
        voando = vel.copy().shift(0.7 * RIGHT + 0.5 * UP)
        outras = VGroup(*[tracejado(Circle(radius=r).move_to(O), POS, 2.6, 0.85) for r in (1, 2.5)])
        self.gat("a derivada dessa curva")
        # v6 §6: γ′ e = F⃗(γ) são escritas em paralelo (as duas caneta) e os gatilhos caem DENTRO do play (eram +3,3 s e +0,4 s)
        w1, w2 = self.falta("é exatamente o vetor que o campo pendura"), self.falta("as circunferências são as trajetórias")
        cgd, c2 = caneta(gd), caneta(g2, atraso=w1)
        self.play(cgd, c2, Succession(Wait(w1), FadeIn(voando, run_time=0.3), Transform(voando, vel, run_time=1.2)),
                  Succession(Wait(w2), AnimationGroup(Create(outras), pulso(traj, 1.0), run_time=1.0)), run_time=max(cgd.tot, c2.tot, w2 + 1.0))
        d_px = np.linalg.norm(voando.get_end() - alvo_c.get_end()) * config.pixel_width / 16
        print(f"[qa] B6-5 ponta violeta × ponta ciano em (2, 0): {d_px:.2f} px; pé: {np.linalg.norm(voando.get_start() - alvo_c.get_start()) * config.pixel_width / 16:.2f} px")

        # ── B6-6 · mesmo período para todos: disco rígido a 1 rad/s ──
        self.an("B6-6")
        self.play(FadeOut(VGroup(voando, g, gd, g2, dot)), traj.animate.set_stroke(opacity=0.5), outras.animate.set_stroke(opacity=0.5), run_time=0.5)
        self.remove(voando, g, gd, g2, dot)
        raio = Line(O, ax.c2p(2.5, 0)).set_stroke(POS, 2, 0.6)
        pts = VGroup(*[ponto(ax.c2p(r, 0), POS, 0.09, z=7) for r in (1, 2, 2.5)])
        centro = ponto(O, GEO, 0.09, z=7)
        roda = VGroup(raio, pts)
        self.play(FadeIn(roda), FadeIn(centro), run_time=0.5)
        self.gat("toda circunferência leva o mesmo tempo")
        w = min(self.falta("bem no centro"), 2 * PI - 0.8)        # v3 §3.6: o destaque do centro entra na palavra, com a volta ainda rodando
        self.play(Rotate(roda, 2 * PI, about_point=O, rate_func=linear),
                  Succession(Wait(w), pulso(centro, 1.8, run_time=0.8), Wait(max(0.01, 2 * PI - w - 0.8))),
                  run_time=2 * PI)          # 1 rad/s: as três completam a volta juntas
        print(f"[gatilho] B6-6 agendado no play: 'bem no centro' a {w:.2f}s do início da volta")
        # v4 §1.3: o disco é uma chapa #1C3A70 a 60% com 8 raios GEO finos que giram juntos; as setas ficam por cima, com contorno
        disco = VGroup(Circle(radius=3.2).move_to(O).set_stroke(GEO, 2, 0.8).set_fill(CH_IMG, 0.6),
                       *[Line(O, O + 3.2 * np.array([math.cos(a), math.sin(a), 0])).set_stroke(GEO, 1.5, 0.55) for a in np.arange(0, 2 * PI, PI / 4)]).set_z_index(-2)
        for l in disco[1:]:
            l._sem_contorno = True
        self.gat("cada pedacinho de um disco rígido")
        self.play(FadeIn(disco), FadeOut(VGroup(traj, outras)), run_time=0.6)
        self.remove(traj, outras)
        rt = self.resta() - 0.2
        self.play(Rotate(VGroup(disco, roda), rt, about_point=O), rate_func=linear, run_time=rt)

        # ── B6-7 · a bandeira gira com o campo por t = π/2 e para na silhueta da rotação de 90° ──
        self.an("B6-7")
        self.play(FadeOut(VGroup(disco, roda, centro)), run_time=0.5)
        self.remove(disco, roda, centro)
        band = bandeira(ax, s=1.5).set_z_index(6)                                             # bandeira coral cheia
        silh = bandeira(ax, s=1.5, silhueta=True).rotate(PI / 2, about_point=O).set_z_index(5)     # posição girada: tracejado coral com contorno tracejado
        self.gat("a transformação dá um quarto de volta")
        self.play(FadeIn(band), FadeIn(silh), cheio.animate.set_opacity(0.45), run_time=1.0)     # as setas do campo baixam para 45% durante a rotação
        n_q = 52
        nums = [MathTex(f"{k * (PI / 2) / n_q:.2f}".replace(".", "{,}"), font_size=M_L) for k in range(n_q + 1)]
        rot_t = MathTex("t", "=", font_size=M_L).move_to(P3(XF - 0.6, 0.6))
        for nm in nums:
            nm.next_to(rot_t, RIGHT, buff=0.2)
        cont = nums[0].copy()
        self.gat("o campo lido como velocidade")
        self.play(FadeIn(rot_t), FadeIn(cont), run_time=0.5)
        self.gat("deixa esse giro correr")

        def troca(m, a):
            m.become(nums[min(n_q, int(round(a * n_q)))])
        self.play(Rotate(band, PI / 2, about_point=O), UpdateFromAlphaFunc(cont, troca), rate_func=linear, run_time=3.6)
        fim_t = MathTex(r"\tfrac{\pi}{2}", font_size=M_L).next_to(rot_t, RIGHT, buff=0.2)
        self.play(FadeOut(cont), FadeIn(fim_t), run_time=0.4)
        self.remove(cont)
        px = config.pixel_width / 16
        e_pe = np.linalg.norm(band[2].get_center() - silh[2].get_center()) * px
        e_topo = np.linalg.norm(band[0].get_end() - silh[0].get_end()) * px
        print(f"[qa] B6-7 bandeira × silhueta: pé {e_pe:.2f} px, topo do mastro {e_topo:.2f} px (pé em {np.round(ax.p2c(band[2].get_center()), 3)})")
        self.gat("e cada ponto chega exatamente")
        self.play(pulso(VGroup(band, silh), 1.0), run_time=1.0)
        self.sai_fim()
