"""Lote PB6 · DE VOLTA AO REDEMOINHO (B6-1…B6-7), layout A (quadros 16 e 17): F⃗ = −y i⃗ + x j⃗ desenhado com três perguntas (valores; ‖F⃗‖ = r constante nas circunferências;
F⃗ · X = 0, perpendicular ao vetor posição); trajetórias γ(t) = r(cos t, sen t) com γ′(t) = F⃗(γ(t)) (a seta violeta pousa sobre a do campo); as circunferências levam o mesmo
tempo (disco rígido com um raio girando); a bandeira gira com o campo por t = π/2. Sem pontinhos soltos: só o ponto da explicação."""
from v7 import *  # noqa: F401,F403

V = Vista(620, 600, 115)
GIRO = lambda x, y: (-y, x)


def anel_setas(r, n, mmax=3.3, lmax=0.5):
    """Setas do giro centradas nos n pontos da circunferência de raio r (comprimento e cor pela intensidade, como o campo7)."""
    g = VGroup()
    for (x, y) in circ_pts(r, n):
        f = GIRO(x, y)
        t = min(1.0, math.hypot(*f) / mmax)
        L = lmax * (0.4 + 0.6 * t)
        u = (f[0] / math.hypot(*f) * L, f[1] / math.hypot(*f) * L)
        s = seta7(V.c2p(x - u[0] / 2, y - u[1] / 2), V.c2p(x + u[0] / 2, y + u[1] / 2), mix(CAMPO, CAMPO2, t), 5, 19)
        s._xy = (x, y)
        g.add(s)
    return g


class LoteB6(Base):
    def corpo(self):
        # ── B6-1 · a regra do começo ──
        self.an("B6-1")
        self.secao("DE VOLTA AO REDEMOINHO")
        ax = VGroup(eixos7(V, -3.2, 3.2, -3.2, 3.2, alpha=0.35))
        self.play(Create(ax), run_time=1.0)
        fF = TC(r"\F(\X,\Y) = -\Y\,\ii + \X\,\jj", 1120, 430, 54)
        self.gat("a regra que troca as coordenadas")
        self.play(caneta(fF))
        mal = malha7(V, 3, 1.0)
        band = bandeira7(V, 0.0, (0, 0), DEST)
        mm = VGroup(mal, band)
        self.gat("como transformação ela leva")
        self.play(FadeIn(mm), run_time=0.6)
        self.play(Rotate(mm, PI / 2, about_point=V.c2p(0, 0)), run_time=2.0)
        self.gat("vamos desenhar sem decorar nada")
        self.play(FadeOut(mm), run_time=0.5)
        self.remove(mm)

        # ── B6-2 · 1: valores em quatro pontos ──
        self.an("B6-2")
        q1 = legenda("1 · VALORES", 1120, 497, SAI_F, "left", 28)
        self.play(FadeIn(q1), run_time=0.4)
        quatro = VGroup()

        def entra(x, y):
            f = GIRO(x, y)
            d = ponto7(V.c2p(x, y), GEO, 7)
            s = seta7(V.c2p(x, y), V.c2p(x + 0.5 * f[0], y + 0.5 * f[1]), CAMPO2, 6, 22)
            quatro.add(d, s)
            return AnimationGroup(FadeIn(d, scale=0.5), GrowArrow(s), run_time=0.7)
        PTS = (((1, 0), "à direita da origem"), ((0, 1), "no ponto uma unidade acima"), ((-1, 0), "à esquerda da origem"), ((0, -1), "embaixo para a direita"))
        f1 = TC(r"\F(\X,\Y) = \F(1,0) = \jj".replace(r"\F(\X,\Y) = ", ""), 1120, 580, 48)
        f2 = TC(r"\F(0,1) = -\ii", 1120, 660, 48)
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
        q2 = legenda("2 · TAMANHO", 1120, 497, SAI_F, "left", 28)
        n3 = TC(r"\|\F\| = \sqrt{x^2+y^2}", 1120, 580, 48)
        self.play(FadeOut(VGroup(f1, f2)), FadeOut(q1), FadeIn(q2), run_time=0.4)
        self.gat("o tamanho dessa seta é a raiz")
        self.play(caneta(n3))
        circ = VGroup(*[circ7(V, r, GEO, 2, (10, 9), 0.6) for r in (1, 2)])
        aneis = VGroup(anel_setas(1.0, 8), anel_setas(2.0, 12))
        self.gat("em cada circunferência centrada")
        self.play(FadeOut(quatro), Create(circ), run_time=0.9)
        self.remove(quatro)
        self.play(LaggedStart(*[FadeIn(a) for a in aneis], lag_ratio=0.4), run_time=1.6)

        # ── B6-4 · 3: perpendicular ao vetor posição (quadro 16) ──
        self.an("B6-4")
        q3 = legenda("3 · DIREÇÃO", 1120, 497, SAI_F, "left", 28)
        self.play(FadeOut(q2), FadeOut(n3), FadeIn(q3), run_time=0.4)
        p = (2 * math.cos(0.6), 2 * math.sin(0.6))
        f = GIRO(*p)
        pos = seta7(V.c2p(0, 0), V.c2p(*p), POS7, 6, 24)
        fP = seta7(V.c2p(*p), V.c2p(p[0] + f[0] * 0.55, p[1] + f[1] * 0.55), CAMPO, 7, 28)
        u_, v_, s = (p[0] / 2, p[1] / 2), (f[0] / 2, f[1] / 2), 0.22
        ang = linha7([V.c2p(p[0] - u_[0] * s, p[1] - u_[1] * s), V.c2p(p[0] - u_[0] * s + v_[0] * s, p[1] - u_[1] * s + v_[1] * s), V.c2p(p[0] + v_[0] * s, p[1] + v_[1] * s)], WHITE_, 2.5)
        dp = ponto7(V.c2p(*p), POS7, 9)
        xy = TC(r"\P{(x,y)}", *(lambda q: (q[0] * 120 + 960, 4.5 * 120 - q[1] * 120))(V.c2p(p[0] + 0.55, p[1] - 0.35)), 36, "c", caneta=False)
        prod = TC(r"\F\cdot\P{(x,y)} = -yx + xy = 0", 1120, 580, 54)
        self.gat("para onde a seta aponta")
        self.play(GrowArrow(pos), FadeIn(dp), FadeIn(xy), run_time=0.8)
        self.play(GrowArrow(fP), run_time=0.6)
        self.gat("faz o produto escalar")
        self.play(caneta(prod))
        self.gat("quer dizer perpendicular")
        self.play(Create(ang), run_time=0.6)
        ctx = campo7(V, GIRO, -3, 3, -3, 3, passo=0.6, rmin=0.4, rmax=3.3, mmax=3.3, lmax=0.5, alpha=0.35, nome="B6 contexto")
        leg4 = legenda("A SETA É SEMPRE PERPENDICULAR AO RAIO", 1124, 660)
        self.gat("junta as três respostas")
        self.play(FadeOut(aneis), FadeIn(ctx), FadeIn(leg4), run_time=0.9)
        self.remove(aneis)

        # ── B6-5 · trajetórias: γ′(t) = F⃗(γ(t)) (quadro 17) ──
        self.an("B6-5")
        self.play(FadeOut(VGroup(pos, ang, q3, prod, leg4, xy, fP, fF)), run_time=0.5)
        self.remove(pos, ang, q3, prod, leg4, xy, fP, fF)
        R = 2.0
        t0 = 1.0
        p5 = (R * math.cos(t0), R * math.sin(t0))
        traj = Circle(radius=R * V.ux).move_to(V.c2p(0, 0)).set_stroke(POS7, 5 / 1.2, 1).set_fill(opacity=0)
        contorno(traj)
        dot = ponto7(V.c2p(*p5), POS7, 10)
        g = TC(r"\P{\gamma(t)} = (r\cos t,\; r\,\sen t)", 1120, 400, 50)
        self.gat("lê o campo como velocidade")
        self.play(Create(traj), run_time=0.9)
        self.gat("de quem passa por ali")
        cg = caneta(g)
        self.play(cg, FadeIn(dot), Rotate(dot, 2 * PI, about_point=V.c2p(0, 0), rate_func=linear), run_time=cg.tot)
        gd = TC(r"\gp = (-r\,\sen t,\; r\cos t)", 1120, 510, 50)
        g2 = TC(r"\gp = \F(\P{\gamma(t)})", 1120, 640, 58)
        f5 = GIRO(*p5)
        alvo_c = seta7(V.c2p(*p5), V.c2p(p5[0] + f5[0] * 0.55, p5[1] + f5[1] * 0.55), CAMPO, 7, 28)
        vel = seta7(V.c2p(*p5), V.c2p(p5[0] + f5[0] * 0.55, p5[1] + f5[1] * 0.55), VEL, 8, 30).set_z_index(8)
        voando = vel.copy().shift(0.7 * RIGHT + 0.5 * UP)
        outras = VGroup(*[circ7(V, r, POS7, 2.6, (10, 9), 0.85) for r in (1, 2.5)])
        self.gat("a derivada dessa curva")
        w1, w2 = self.falta("é exatamente o vetor que o campo pendura"), self.falta("as circunferências são as trajetórias")
        cgd, c2 = caneta(gd), caneta(g2, atraso=w1)
        self.add(alvo_c)
        self.play(cgd, c2, Succession(Wait(w1), FadeIn(voando, run_time=0.3), Transform(voando, vel, run_time=1.2)),
                  Succession(Wait(w2), AnimationGroup(Create(outras), pulso(traj, 1.0), run_time=1.0)), run_time=max(cgd.tot, c2.tot, w2 + 1.0))
        d_px = np.linalg.norm(voando.get_end() - alvo_c.get_end()) * 120
        print(f"[qa] B6-5 ponta violeta × ponta verde em γ(1): {d_px:.2f} px")
        leg5 = legenda("A VELOCIDADE DA CIRCUNFERÊNCIA É O PRÓPRIO CAMPO", 1124, 750)
        self.play(FadeIn(leg5), run_time=0.4)

        # ── B6-6 · mesmo período para todos: um disco rígido (só o raio gira) ──
        self.an("B6-6")
        self.play(FadeOut(VGroup(voando, g, gd, g2, dot, leg5, alvo_c)), traj.animate.set_stroke(opacity=0.5), run_time=0.5)
        self.remove(voando, g, gd, g2, dot, leg5, alvo_c)
        cs = VGroup(*[circ7(V, r, GEO, 3, None, 0.9) for r in (1, 2, 3)])
        centro = ponto7(V.c2p(0, 0), WHITE_, 9)
        self.gat("toda circunferência leva o mesmo tempo")
        self.play(LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.4), run_time=1.8)
        w = min(self.falta("bem no centro"), 2.5)
        self.play(FadeIn(centro), run_time=0.3)
        self.play(pulso(centro, 1.8, 1.0), run_time=0.8)
        disco = VGroup(Circle(radius=3.0 * V.ux).move_to(V.c2p(0, 0)).set_fill(CH_IMG, 0.55).set_stroke(GEO, 1.7, 0.8),
                       Line(V.c2p(0, 0), V.c2p(3.0, 0)).set_stroke(POS7, 3 / 1.2, 1)).set_z_index(-2)
        for m in disco:
            m._sem_contorno = True
        self.gat("cada pedacinho de um disco rígido")
        self.play(FadeIn(disco), FadeOut(VGroup(traj, outras)), run_time=0.6)
        self.remove(traj, outras)
        rt = self.resta() - 0.2
        self.play(Rotate(disco, rt * 0.6, about_point=V.c2p(0, 0)), rate_func=linear, run_time=rt)

        # ── B6-7 · a bandeira gira com o campo por t = π/2 e para na silhueta da rotação de 90° ──
        self.an("B6-7")
        self.play(FadeOut(VGroup(disco, cs, centro)), run_time=0.5)
        self.remove(disco, cs, centro)
        band = bandeira7(V, 0.0, (0, 0), DEST)
        silh = bandeira7(V, PI / 2, (0, 0), DEST, preenchida=False)
        silh_t = VGroup(*[DashedVMobject(m, num_dashes=18) for m in silh])
        self.gat("a transformação dá um quarto de volta")
        self.play(FadeIn(band), FadeIn(silh_t), run_time=1.0)
        n_q = 26
        nums = [MathTex(f"{k * (PI / 2) / n_q:.2f}".replace(".", "{,}"), font_size=M_L) for k in range(n_q + 1)]
        rot_t = MathTex("t", "=", font_size=M_L).move_to(PX(1100, 560))
        for nm in nums:
            nm.next_to(rot_t, RIGHT, buff=0.2)
        cont = nums[0].copy()
        self.gat("o campo lido como velocidade")
        self.play(FadeIn(rot_t), FadeIn(cont), run_time=0.5)
        self.gat("deixa esse giro correr")

        def troca(m, a):
            m.become(nums[min(n_q, int(round(a * n_q)))])
        self.play(Rotate(band, PI / 2, about_point=V.c2p(0, 0)), UpdateFromAlphaFunc(cont, troca), rate_func=linear, run_time=3.6)
        fim_t = MathTex(r"\tfrac{\pi}{2}", font_size=M_L).next_to(rot_t, RIGHT, buff=0.2)
        self.play(FadeOut(cont), FadeIn(fim_t), run_time=0.4)
        self.remove(cont)
        self.gat("e cada ponto chega exatamente")
        self.play(pulso(VGroup(band, silh_t), 1.0, 1.6), run_time=1.0)
        self.sai_fim()
