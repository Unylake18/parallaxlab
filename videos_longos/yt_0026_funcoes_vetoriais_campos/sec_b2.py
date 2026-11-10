"""Lote PB2 · TRANSFORMAÇÃO (B2-1…B2-7): coordenadas polares φ(θ, ρ) = (ρ cos θ, ρ sen θ). Dois planos lado a lado (entrada θρ à esquerda,
com janela; saída xy à direita), seta em arco φ no alto, fórmula embaixo. Pontos voando, segmento ρ = 2 enrolando na circunferência (magenta
nos dois lados), raio θ fixo (âmbar), o retângulo B virando o disco φ(B), as bordas (ρ = 0 esmagado; θ = 0 e θ = 2π colados).
v3 (handoff v4): painéis no tamanho do alvo (retângulo 5,0 × 2,4 u; disco de raio 2,8 u), chapas opacas, famílias com traço 3–4, pontos com
anel, φ(B) em placa, lado ρ = 0 / origem / lados colados em destaque coral (no lugar do pisca branco)."""
from kit import *  # noqa: F401,F403


def paineis(ax_e, ax_s, y_e, y_s, a=(-1.9, 1.75), b=(1.75, 1.95)):
    """Títulos ENTRADA/SAÍDA e a seta de voo em arco φ entre os painéis (no alto), de `a` até `b`."""
    te = txt("ENTRADA", 24, color=DIM).move_to(P3((ax_e.c2p(ax_e.x_range[0], 0)[0] + ax_e.c2p(ax_e.x_range[1], 0)[0]) / 2, y_e))
    ts = txt("SAÍDA", 24, color=DIM).move_to(P3((ax_s.c2p(ax_s.x_range[0], 0)[0] + ax_s.c2p(ax_s.x_range[1], 0)[0]) / 2, y_s))
    arco = voo(P3(*a), P3(*b), angle=-0.75, w=3, tip=0.2)
    phi = F(r"\varphi", size=M_L, caneta=False).move_to(arco.point_from_proportion(0.5) + P3(0, 0.4))
    return te, ts, arco, phi


class LoteB2(Base):
    def corpo(self):
        # ── B2-1 · dois painéis vazios ──
        self.an("B2-1")
        self.secao("TRANSFORMAÇÃO")
        ax_e = eixos((-7, -1), [0, 2 * PI, PI / 2], [0, 2.2, 1], 0.8, 1.2)          # retângulo B: 5,03 × 2,4 u
        ax_s = eixos((4, 0), [-2.2, 2.2, 1], [-2.2, 2.2, 1], 1.4)                    # disco φ(B): raio 2,8 u
        janela_local(self, ax_e)            # exceção registrada: θ com unidade 0,8 por rad não cai na grade
        te, ts, arco, phi = paineis(ax_e, ax_s, 2.15, 3.85, a=(-2.5, 2.2), b=(0.55, 2.5))
        self.play(Create(ax_e), Create(ax_s), run_time=1.2)
        self.gat("à esquerda o plano de entrada")
        self.play(FadeIn(te), pulso(ax_e, 1.02, 1.6), run_time=0.8)
        self.gat("à direita o plano de saída")
        self.play(FadeIn(ts), pulso(ax_s, 1.02, 1.6), run_time=0.8)
        self.gat("quando eu jogo um conjunto")
        self.play(Create(arco), FadeIn(phi), run_time=1.0)

        # ── B2-2 · eixos θ, ρ e a fórmula ──
        self.an("B2-2")
        lt = F(r"\theta", size=M_M, caneta=False).set_color(E1).next_to(ax_e.c2p(2 * PI, 0), RIGHT, buff=0.15)
        lr = F(r"\rho", size=M_M, caneta=False).set_color(E2).next_to(ax_e.c2p(0, 2.2), UP, buff=0.12)
        tk = VGroup(*[F(s, size=26, caneta=False).next_to(ax_e.c2p(v, 0), DOWN, buff=0.14) for s, v in
                      ((r"\tfrac{\pi}{2}", PI / 2), (r"\pi", PI), (r"\tfrac{3\pi}{2}", 3 * PI / 2), (r"2\pi", 2 * PI))])
        tkr = VGroup(*[F(s, size=26, caneta=False).next_to(ax_e.c2p(0, v), LEFT, buff=0.12) for s, v in (("1", 1), ("2", 2))])
        lx = F("x", size=M_M, caneta=False).set_color(SAI).next_to(ax_s.c2p(2.2, 0), RIGHT, buff=0.12)
        ly = F("y", size=M_M, caneta=False).set_color(SAI).next_to(ax_s.c2p(0, 2.2), RIGHT, buff=0.15)
        tks = VGroup(*[F(str(v), size=24, caneta=False).next_to(ax_s.c2p(v, 0), DOWN, buff=0.1) for v in (1, 2)])
        self.gat("o eixo horizontal é um ângulo")
        self.play(FadeIn(lt, shift=0.1 * LEFT), FadeIn(tk), run_time=0.7)
        self.gat("o eixo vertical é um raio")
        self.play(FadeIn(lr, shift=0.1 * DOWN), FadeIn(tkr), run_time=0.7)
        self.play(FadeIn(lx), FadeIn(ly), FadeIn(tks), run_time=0.5)
        form = F(r"\varphi", "(", (r"\theta", E1), ",", (r"\rho", E2), ")", "=", ("(", SAI), (r"\rho", E2), (r"\cos", SAI), (r"\theta", E1), (",", SAI),
                 (r"\ \rho", E2), (r"\,\mathrm{sen}\,", SAI), (r"\theta", E1), (")", SAI), size=M_L).move_to(P3(-3.4, -3.35))
        self.gat("a função pega esse par")
        self.play(caneta(form))
        self.gat("essas duas fórmulas são as componentes")
        cha = [Brace(VGroup(form[8], form[9], form[10]), DOWN, buff=0.06), Brace(VGroup(form[12], form[13], form[14]), DOWN, buff=0.06)]
        for c_ in cha:
            c_.set_fill(SAI_F, 1).set_stroke(width=0)
            c_._sem_contorno = True
        rot_c = [F(r"\varphi_1", size=26, caneta=False).set_color(SAI_F).next_to(cha[0], DOWN, buff=0.04), F(r"\varphi_2", size=26, caneta=False).set_color(SAI_F).next_to(cha[1], DOWN, buff=0.04)]
        self.play(FadeIn(VGroup(*cha)), FadeIn(VGroup(*rot_c)), run_time=0.7)

        # ── B2-3 · três pontos voando ──
        self.an("B2-3")
        mapa = lambda p: ax_s.c2p(*(lambda c: (c[1] * math.cos(c[0]), c[1] * math.sin(c[0])))(ax_e.p2c(p)))
        voos = VGroup()
        for (th, r), fr in (((0, 2), "ângulo zero e raio dois"), ((PI / 2, 2), "ângulo de noventa graus"), ((PI, 1), "ângulo de cento e oitenta graus")):
            self.gat(fr)
            d0 = ponto(ax_e.c2p(th, r), GEO, 0.09)
            d1 = ponto(ax_s.c2p(r * math.cos(th), r * math.sin(th)), SAI, 0.1)
            self.play(FadeIn(d0, scale=0.5), run_time=0.4)
            self.play(TransformFromCopy(d0, d1, path_arc=-0.9), run_time=1.3)
            voos.add(d0, d1)

        # ── B2-4 · uma reta inteira: ρ = 2 enrola na circunferência; θ fixo vira um raio ──
        self.an("B2-4")
        self.play(FadeOut(voos), run_time=0.4)
        self.remove(voos)
        seg_r = Line(ax_e.c2p(0, 2), ax_e.c2p(2 * PI, 2)).insert_n_curves(90).set_stroke(E2, W_CURVA)
        th0 = PI / 3
        seg_t = Line(ax_e.c2p(th0, 0), ax_e.c2p(th0, 2)).insert_n_curves(30).set_stroke(E1, W_CURVA)
        self.gat("fixa o raio em dois")
        self.play(Create(seg_r), run_time=1.6)
        self.gat("do outro lado")
        img_r = seg_r.copy()
        self.play(ApplyPointwiseFunction(mapa, img_r), run_time=2.6)
        self.gat("e se a gente fixa o ângulo")
        self.play(Create(seg_t), run_time=1.0)
        self.gat("sai um segmento que parte da origem")
        img_t = seg_t.copy()
        self.play(ApplyPointwiseFunction(mapa, img_t), run_time=1.8)

        # ── B2-5 · o retângulo inteiro vira o disco: virar e enrolar ──
        self.an("B2-5")
        self.play(FadeOut(VGroup(seg_r, seg_t, img_r, img_t)), run_time=0.4)
        self.remove(seg_r, seg_t, img_r, img_t)
        pol = Polar(ax_e, ax_s, 2.0)
        B_ = retangulo_polar(pol, 2.0)
        lB = F("B", size=M_M, caneta=False).set_color(GEO).next_to(ax_e.c2p(2 * PI, 2), UR, buff=0.08)
        self.gat("olha o retângulo inteiro")
        self.play(FadeIn(B_[0]), Create(B_[1]), Create(B_[2]), FadeIn(lB), run_time=1.4)
        img = B_.copy()
        for a_, b_ in zip(B_.get_family(), img.get_family()):
            if hasattr(a_, "_amostras"):
                b_._amostras, b_._fechada = a_._amostras, a_._fechada
        self.add(img)
        self.play(pol.anim_virar(img, rt=1.0))
        self.gat("cada faixa horizontal vira um anel")
        t0 = self.t
        self.play(pol.anim_enrolar(img, rt=3.4))
        for k in (0.25, 0.5, 0.75, 1.0):
            print(f"[polar] B2-5 k={k:.2f} em {t0 + alfa_de_k(k) * 3.4:.2f}s do lote (quadro {round((t0 + alfa_de_k(k) * 3.4) * FPS)})")
        print(f"[qa] B2-5 polar em k = 1 × φ(θ, ρ): {pol.erro_k1():.3f} px")
        print(f"[qa] B2 tamanho dos painéis a 1080p: retângulo {pol.a_th * 2 * PI * 120:.0f} × {pol.a_rho * 2 * 120:.0f} px; disco de raio {2 * pol.u_s * 120:.0f} px "
              f"(alvo ~565 × 300 e ~330)")
        ancora_d = ax_s.c2p(1.414, 1.414)
        PL = P3(6.95, 2.85)
        lphi = F(r"\varphi", "(", ("B", GEO), ")", size=M_M).move_to(PL)
        p_phi = placa(lphi, SAI_F)
        fio = Line(ancora_d, p_phi[0].get_corner(DL)).set_stroke(SAI_F, 2)
        self.gat("e o retângulo se fecha")
        self.play(img[0].animate.set_fill(CH_IMG, 0.8).set_stroke(SAI_F, 4), run_time=0.8)          # a chapa do domínio vira a chapa da imagem
        self.play(Create(fio), FadeIn(p_phi[0]), run_time=0.3)
        self.play(caneta(lphi))

        # ── B2-6 · as bordas: ρ = 0 vira um ponto; θ = 0 e θ = 2π caem no mesmo segmento (destaque coral) ──
        self.an("B2-6")
        baixo = Line(ax_e.c2p(0, 0), ax_e.c2p(2 * PI, 0)).insert_n_curves(60).set_stroke(DEST, 7)
        self.gat("o lado de baixo do retângulo")
        self.play(FadeIn(baixo), run_time=0.3)
        self.play(pulso(baixo, 1.0, 1.7), run_time=0.8)
        self.gat("vai todo parar num ponto só")
        b2 = baixo.copy()
        self.play(ApplyPointwiseFunction(mapa, b2), run_time=1.8)
        orig = ponto(ax_s.c2p(0, 0), DEST, 0.1, z=8)
        self.play(FadeIn(orig, scale=2.0), Flash(ax_s.c2p(0, 0), color=DEST, line_length=0.2, flash_radius=0.26), run_time=0.7)
        esq = Line(ax_e.c2p(0, 0), ax_e.c2p(0, 2)).insert_n_curves(30).set_stroke(DEST, 7)
        dir_ = Line(ax_e.c2p(2 * PI, 0), ax_e.c2p(2 * PI, 2)).insert_n_curves(30).set_stroke(DEST, 7)
        self.gat("e os dois lados verticais")
        self.play(FadeIn(esq), FadeIn(dir_), run_time=0.3)
        self.play(pulso(VGroup(esq, dir_), 1.0, 1.7), run_time=0.8)
        self.gat("caem exatamente um em cima do outro")
        e2, d2 = esq.copy(), dir_.copy()
        self.play(ApplyPointwiseFunction(mapa, e2), ApplyPointwiseFunction(mapa, d2), run_time=1.8)
        self.play(pulso(VGroup(e2, d2), 1.0, 1.7), run_time=0.8)

        # ── B2-7 · a imagem; aviso: o meio do caminho é só animação ──
        self.an("B2-7")
        lim = F((r"\mathrm{Im}", SAI), "=", r"\varphi", "(", ("B", GEO), ")", size=M_M).move_to(PL + P3(-0.45, 0))
        p_im = placa(lim, SAI_F)
        fio2 = Line(ancora_d, p_im[0].get_corner(DL)).set_stroke(SAI_F, 2)
        self.gat("esse disco tem nome")
        self.play(FadeOut(VGroup(baixo, b2, esq, dir_, e2, d2, orig)), FadeOut(lphi), Transform(p_phi[0], p_im[0]), Transform(fio, fio2), run_time=0.3)
        self.remove(baixo, b2, esq, dir_, e2, d2, orig, lphi)
        self.play(caneta(lim))
        selo = txt("O MEIO DO CAMINHO É SÓ ANIMAÇÃO", 20, color=DIM).move_to(P3(-3.6, -2.4))
        self.gat("só um aviso honesto")
        self.play(FadeIn(selo, shift=0.08 * UP), run_time=0.5)
        self.gat("a função liga direto")
        lig = VGroup()
        for th, r in ((PI / 4, 1.5), (PI, 2), (3 * PI / 2, 1)):
            a, b = ax_e.c2p(th, r), ax_s.c2p(r * math.cos(th), r * math.sin(th))
            lig.add(guia(a, b, GEO, 2.2, 0.9), ponto(a, GEO, 0.07, z=8), ponto(b, SAI, 0.08, z=8))
        self.play(LaggedStart(*[Create(m) for m in lig], lag_ratio=0.15), run_time=1.6)
        self.sai_fim()
