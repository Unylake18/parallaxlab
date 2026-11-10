"""Lote PB5 · CAMPO VETORIAL (B5-1…B5-4): vetor aplicado no ponto X; F⃗ = j⃗ (vento uniforme × colapso num ponto); F⃗ = x i⃗ + y j⃗ (explosão
de setas, ‖F⃗‖ = r, × identidade); quadro das duas perguntas. Plano à esquerda (origem (−3, 0), [−3, 3]², unidade 1), fórmulas à direita."""
from kit import *  # noqa: F401,F403

XF = 3.7          # centro da coluna das fórmulas


def sub_caneta(m, gs, tex):
    """Um pedaço de uma fórmula para a caneta (ex.: a seta de F⃗ acendendo por último, na sua palavra)."""
    g = VGroup(*gs)
    g._tex, g._caneta, g._esc, g._em_caneta = tex, True, False, False
    return g


def mini(c, rotulo):
    pl = Plano(c, 0.32)
    ax = VGroup(Line(pl.c2p(-2.4, 0), pl.c2p(2.4, 0)), Line(pl.c2p(0, -2.4), pl.c2p(0, 2.4))).set_stroke(GEO, 1.5, 0.7)
    for l in ax:
        l._sem_contorno = True
    pts = VGroup(*[Dot(pl.c2p(x, y), radius=0.045, color=GEO) for x in range(-2, 3) for y in range(-2, 3)])
    r = txt(rotulo, 20, color=DIM).move_to(pl.c2p(0, 3.05))
    return pl, VGroup(ax, r), pts


class LoteB5(Base):
    def corpo(self):
        ax = eixos((-3, 0), [-3, 3, 1], [-3, 3, 1], 1.0)

        # ── B5-1 · vetor aplicado no ponto ──
        self.an("B5-1")
        self.secao("CAMPO VETORIAL")
        self.play(Create(ax), run_time=1.0)
        X = ax.c2p(1.5, 1.0)
        dX = ponto(X, POS, 0.09)
        lX = F("X", size=M_M, caneta=False).set_color(POS).next_to(dX, DL, buff=0.08)
        self.gat("em vez de mandar o ponto")
        self.play(FadeIn(dX, scale=0.5), FadeIn(lX), run_time=0.5)
        fant = ponto(ax.c2p(-1.2, 2.4), SAI, 0.08).set_opacity(0.6)
        arc = voo(X + 0.1 * UL, fant.get_center() + 0.1 * DR, angle=0.8, w=2.2, tip=0.15).set_opacity(0.7)
        self.play(Create(arc), FadeIn(fant), run_time=0.9)
        self.play(FadeOut(arc), FadeOut(fant), run_time=0.5)
        self.remove(arc, fant)
        sF = seta(X, ax.c2p(1.5 + 1.3, 1.0 + 0.9), CAMPO_FORTE, 4.5, tip=0.2)
        self.gat("a gente desenha o vetor de saída")
        self.play(GrowArrow(sF), run_time=0.9)
        fx = F((r"\vec F", CAMPO), "(", ("X", POS), ")", size=M_XL).move_to(P3(XF, 2.2))
        gl = glifos(fx)
        flecha = max(gl[:2], key=lambda g: g.get_center()[1])
        corpo_ = sub_caneta(fx, [g for g in gl if g is not flecha], r"F(X)")
        topo = sub_caneta(fx, [flecha], r"\vec{\ }")
        self.gat("a função se chama campo vetorial")
        self.play(caneta(corpo_))
        self.gat("ganha uma setinha em cima")
        self.play(caneta(topo))
        geral = F((r"\vec F", CAMPO), "(", ("x", E1), ",", ("y", E2), ")", "=", ("P", CAMPO), "(", ("x", E1), ",", ("y", E2), ")", r"\,\vec i", "+", ("Q", CAMPO), "(", ("x", E1), ",", ("y", E2), ")", r"\,\vec j", size=M_M).move_to(P3(XF, 0.5))
        self.gat("em geral um campo no plano")
        self.play(caneta(geral))
        self.wait(max(0.1, min(2.0, self.resta() - 0.5)))
        self.play(FadeOut(geral), run_time=0.3)
        self.remove(geral)

        # ── B5-2 · F⃗ = j⃗: vento uniforme × colapso num ponto ──
        self.an("B5-2")
        self.play(FadeOut(VGroup(dX, lX, sF, corpo_, topo)), run_time=0.4)
        self.remove(dX, lX, sF, corpo_, topo)
        f2 = F((r"\vec F", CAMPO), "(", ("x", E1), ",", ("y", E2), ")", "=", r"\vec j", size=M_XL).move_to(P3(XF, 2.2))
        self.gat("um campo que devolve o mesmo vetor")
        self.play(caneta(f2))
        pts = [(x, y) for x in range(-3, 4) for y in range(-3, 3)]          # sem a linha y = 3: a seta subiria até o canto
        c2 = campo(ax, lambda x, y: (0.0, 1.0), pts, 0.8, "B5-2 F = j")
        self.gat("desenhado como campo")
        self.play(LaggedStart(*[GrowArrow(s) for s in c2], lag_ratio=0.02), run_time=1.6)
        pl, moldura, mp = mini(P3(XF, -1.25), "COMO TRANSFORMAÇÃO")
        self.gat("agora a mesma fórmula lida como transformação")
        self.play(FadeIn(moldura), FadeIn(mp), run_time=0.6)
        alvo = ponto(pl.c2p(0, 1), SAI, 0.09)
        self.gat("todo ponto do plano vai parar")
        self.play(*[d.animate.move_to(pl.c2p(0, 1)).set_color(SAI) for d in mp], run_time=1.8)
        self.add(alvo)
        self.gat("o plano inteiro é esmagado")
        self.play(Flash(alvo.get_center(), color=SAI, line_length=0.14, flash_radius=0.2), run_time=0.7)
        self.gat("um desenho mostra vento")
        self.play(pulso(c2, 1.0), run_time=0.9)
        self.play(pulso(alvo, 1.6), run_time=0.7)

        # ── B5-3 · F⃗ = x i⃗ + y j⃗: explosão × identidade ──
        self.an("B5-3")
        self.play(FadeOut(VGroup(f2, c2, moldura, mp, alvo)), run_time=0.4)
        self.remove(f2, c2, moldura, mp, alvo)
        f3 = F((r"\vec F", CAMPO), "(", ("x", E1), ",", ("y", E2), ")", "=", ("x", E1), r"\,\vec i", "+", ("y", E2), r"\,\vec j", size=M_XL).move_to(P3(XF, 2.2))
        self.gat("o campo que devolve em cada ponto")
        self.play(caneta(f3))
        K3 = 0.28
        c3 = campo(ax, lambda x, y: (x, y), [p for p in grade_pts(3.0, 1.0) if p[1] < 2.5], K3, "B5-3 radial (x, y)")   # nada acima de y = 190 px (canto)
        self.gat("cada seta aponta para fora")
        self.play(LaggedStart(*[GrowArrow(s) for s in sorted(c3, key=lambda s: math.hypot(*s._xy))], lag_ratio=0.03), run_time=1.8)
        n3 = F(r"\|", (r"\vec F", CAMPO), r"\|", "=", r"\sqrt{", ("x", E1), "^2+", ("y", E2), "^2}", size=M_L).move_to(P3(XF, 0.95))
        self.gat("o tamanho da seta é igual")
        self.play(caneta(n3))
        circ = VGroup(*[tracejado(Circle(radius=r).move_to(ax.c2p(0, 0)), GEO, W_GUIA, 0.85) for r in (1, 2)])
        aneis = VGroup(*[campo(ax, lambda x, y: (x, y), [(r * math.cos(k * PI / 4), r * math.sin(k * PI / 4)) for k in range(8)], K3, f"B5-3 anel r={r}", w=4.5,
                               fmax=3.0) for r in (1, 2)])
        self.gat("em cima de uma mesma circunferência")
        self.play(Create(circ), run_time=0.9)
        self.play(FadeIn(aneis), c3.animate.set_opacity(0.35), run_time=0.7)
        pl, moldura, mp = mini(P3(XF, -1.6), "COMO TRANSFORMAÇÃO")
        self.gat("e como transformação")
        self.play(FadeIn(moldura), FadeIn(mp), run_time=0.6)
        self.gat("cada ponto vai para")
        self.play(*[pulso(d, 1.8) for d in mp], run_time=1.2)
        self.gat("como campo é uma explosão")
        self.play(c3.animate.set_opacity(1.0), pulso(VGroup(c3, aneis), 1.0), run_time=1.0)

        # ── B5-4 · as duas perguntas ──
        self.an("B5-4")
        self.limpa(rt=0.4)
        div = Line(P3(0, 2.4), P3(0, -2.6)).set_stroke(GEO, 2, 0.6)
        ic_t = VGroup(ponto(P3(-4.6, -0.2), GEO, 0.1), ponto(P3(-2.4, 0.4), SAI, 0.1), voo(P3(-4.45, -0.05), P3(-2.55, 0.45), angle=-0.7, w=3, tip=0.2))
        ic_c = VGroup(ponto(P3(2.6, -0.2), POS, 0.1), seta(P3(2.6, -0.2), P3(4.3, 0.6), CAMPO_FORTE, 4.5, tip=0.22))
        col_t = VGroup(txt("TRANSFORMAÇÃO:", 30, bold=True), txt("PARA ONDE O PONTO VAI?", 30)).arrange(DOWN, buff=0.18).move_to(P3(-3.6, -1.9))
        col_c = VGroup(txt("CAMPO:", 30, bold=True, color=CAMPO), txt("QUE SETA O PONTO CARREGA?", 30)).arrange(DOWN, buff=0.18).move_to(P3(3.6, -1.9))
        self.gat("nenhum dos dois desenhos")
        self.play(Create(div), run_time=0.6)
        self.gat("como transformação a pergunta é")
        self.play(FadeIn(ic_t), FadeIn(col_t, shift=0.1 * UP), run_time=0.8)
        self.gat("como campo a pergunta é")
        self.play(FadeIn(ic_c), FadeIn(col_c, shift=0.1 * UP), run_time=0.8)
        self.sai_fim()
