"""Lote PB2 · TRANSFORMAÇÃO (B2-1…B2-7), layout B (quadro 11): coordenadas polares φ(θ, ρ) = (ρ cos θ, ρ sen θ). Dois painéis do mesmo tamanho (ENTRADA à esquerda, SAÍDA à
direita), seta em arco φ entre eles, fórmula embaixo com as chaves φ₁ e φ₂. Pontos voando, o segmento ρ = 2 enrolando na circunferência, o retângulo B virando o disco φ(B),
as bordas (ρ = 0 esmagado; θ = 0 e θ = 2π colados). Tudo dentro dos painéis."""
from v7 import *  # noqa: F401,F403


def px_de(p):
    """ponto do Manim → (x, y) em px de 1080p"""
    return p[0] * 120 + 960, 4.5 * 120 - p[1] * 120


class LoteB2(Base):
    def corpo(self):
        # ── B2-1 · dois painéis vazios ──
        self.an("B2-1")
        self.secao("TRANSFORMAÇÃO")
        ax_e = Plano(PX(250, 700)[:2], 8.2 / (2 * PI) * 72 / 120, 1.95 * 72 / 120)      # retângulo B: θ de 0 a 2π (590 px), ρ de 0 a 2 (281 px)
        ax_s = Plano(PX(1420, 530)[:2], 1.0)                                          # disco φ(B): raio 2 (240 px)
        pe, ps = painel(130, 250, 740, 560, "ENTRADA", E1), painel(1050, 250, 740, 560, "SAÍDA", SAI)
        arco = arco7(890, 520, 1030, 520, r"\varphi")
        self.gat("à esquerda o plano de entrada")
        self.play(FadeIn(pe), run_time=0.8)
        self.gat("à direita o plano de saída")
        self.play(FadeIn(ps), run_time=0.8)
        self.gat("quando eu jogo um conjunto")
        self.play(FadeIn(arco), run_time=1.0)

        # ── B2-2 · eixos θ, ρ e a fórmula ──
        self.an("B2-2")
        R = lambda t, r: ax_e.c2p(t, r)
        lt = TC(r"\th", px_de(R(2 * PI, 0))[0] + 28, px_de(R(2 * PI, 0))[1] + 10, 40, "c", caneta=False)
        lr = TC(r"\rh", px_de(R(0, 2))[0] - 8, px_de(R(0, 2))[1] - 40, 40, "c", caneta=False)
        tk = [TC(r"2\pi", px_de(R(2 * PI, 0))[0], px_de(R(2 * PI, 0))[1] + 40, 30, "c", caneta=False),
              TC("2", px_de(R(0, 2))[0] - 26, px_de(R(0, 2))[1], 30, "c", caneta=False)]
        ex_e = VGroup(linha7([R(0, 0), R(2 * PI, 0)], GEO, 2, 0.5), linha7([R(0, 0), R(0, 2.3)], GEO, 2, 0.5)).set_z_index(2)
        vs = Vista(1420, 530, 120)
        ex_s = eixos7(vs, -2.4, 2.4, -2.2, 2.2, alpha=0.45)
        self.gat("o eixo horizontal é um ângulo")
        self.play(Create(ex_e), FadeIn(lt, shift=0.1 * LEFT), FadeIn(tk[0]), run_time=0.7)
        self.gat("o eixo vertical é um raio")
        self.play(FadeIn(lr, shift=0.1 * DOWN), FadeIn(tk[1]), Create(ex_s), run_time=0.7)
        form = TC(r"\varphi(\th,\rh) = \S{\big(}\underbrace{\rh\cos\th}_{\S{\varphi_1}},\; \underbrace{\rh\,\sen\th}_{\S{\varphi_2}}\S{\big)}", 960, 935, 54, "c")
        self.gat("a função pega esse par")
        self.play(caneta(form))

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
        lB = TC(r"{\G B}", px_de(R(PI, 2))[0], px_de(R(PI, 2))[1] - 28, 36, "c", caneta=False)
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
        self.gat("e o retângulo se fecha")
        self.play(img[0].animate.set_fill(CH_IMG, 0.8).set_stroke(SAI_F, 4), run_time=0.8)          # a chapa do domínio vira a chapa da imagem

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
        lim = TC(r"\S{\operatorname{Im} = \varphi(B)}", 1660, 300, 36, "c")
        self.gat("esse disco tem nome")
        self.play(FadeOut(VGroup(baixo, b2, esq, dir_, e2, d2, orig)), run_time=0.3)
        self.remove(baixo, b2, esq, dir_, e2, d2, orig)
        self.play(caneta(lim))
        selo = T("O MEIO DO CAMINHO É SÓ ANIMAÇÃO", 500, 850, 24, "center", DIM, bold=False)
        self.gat("só um aviso honesto")
        self.play(FadeIn(selo, shift=0.08 * UP), run_time=0.5)
        self.gat("a função liga direto")
        lig = VGroup()
        for th, r in ((PI / 4, 1.5), (PI, 2), (3 * PI / 2, 1)):
            a, b = ax_e.c2p(th, r), ax_s.c2p(r * math.cos(th), r * math.sin(th))
            lig.add(guia(a, b, GEO, 2.2, 0.9), ponto(a, GEO, 0.07, z=8), ponto(b, SAI, 0.08, z=8))
        self.play(LaggedStart(*[Create(m) for m in lig], lag_ratio=0.15), run_time=1.6)
        self.sai_fim()
