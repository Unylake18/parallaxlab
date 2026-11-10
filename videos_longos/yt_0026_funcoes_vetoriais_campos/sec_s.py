"""Lote PS · RESUMO (S1, S2) e CTA. Funciona depois do B6 e depois do B7 (começa do papel vazio, com a linha 1 do canto).
S1: bandeira girada e redemoinho; depois, um de cada vez na sua palavra, o disco das polares, a tigela e o redemoinho; embaixo, as duas leituras.
S2: disco e redemoinho lado a lado. CTA: tudo sai (canto e marca d'água também); barquinho parado no redemoinho e a pergunta; logo e INSCREVA-SE,
sem prévia de próximo vídeo."""
from kit import *  # noqa: F401,F403

GIRO = lambda x, y: (-y, x)


def mini_bandeira(c, s=0.36):
    pl = Plano(c, s)
    g = VGroup(malha(pl, -3, 3, -3, 3, 1.0, w=1.5), bandeira(pl))
    return g.rotate(PI / 2, about_point=pl.c2p(0, 0))


def mini_redemoinho(c, s=0.36):
    pl = Plano(c, s)
    return campo(pl, GIRO, grade_pts(3.0, 1.0), 0.28, f"S redemoinho (escala {s})", w=3.0)


def mini_disco(c, r=0.95):
    g = VGroup(chapa(Circle(radius=r).move_to(c), "img"))
    g.add(*[Line(c, c + r * np.array([math.cos(a), math.sin(a), 0])).set_stroke(E1, W_FAM) for a in np.arange(0, 2 * PI, PI / 4)])
    g.add(*[Circle(radius=k * r).move_to(c).set_stroke(E2, W_FAM if k < 1 else W_FAM_B) for k in (0.5, 1.0)])
    return contorno(g)


def mini_tigela(c, w=1.25):
    """Tigela sólida em 2D, com os dois tons do 3D: fora #6E9EF0, dentro #35589E, borda clara."""
    perfil = [c + P3(x, 0.55 * x * x - 0.7) for x in np.linspace(-w, w, 41)]
    yt = 0.55 * w * w - 0.7
    corpo = VMobject().set_points_as_corners(perfil + [perfil[0]]).set_stroke(SAI_F, 3).set_fill("#6E9EF0", 1)
    meio = Arc(start_angle=PI, angle=PI).stretch_to_fit_width(2 * w * 0.6).stretch_to_fit_height(0.42 * 0.3).move_to(c + P3(0, 0.55 * (0.6 * w) ** 2 - 0.7 - 0.06))
    meio.set_stroke(E2, W_FAM)
    topo = Ellipse(width=2 * w, height=0.42).move_to(c + P3(0, yt)).set_stroke("#DCEBFF", 3).set_fill("#35589E", 1)
    return contorno(VGroup(corpo, meio, topo))


def barquinho(c, s=0.55):
    """Objeto de teste (coral), com contorno."""
    casco = Polygon(c + s * P3(-0.75, 0), c + s * P3(0.75, 0), c + s * P3(0.5, -0.35), c + s * P3(-0.5, -0.35)).set_stroke(DEST, 2.5).set_fill(DEST, 1)
    vela = Polygon(c + s * P3(0, 0.05), c + s * P3(0, 0.9), c + s * P3(0.5, 0.05)).set_stroke(SAI_F, 2.5).set_fill(SAI_F, 0.9)
    return contorno(VGroup(casco, vela)).set_z_index(8)


class LoteS(Base):
    def corpo(self):
        # ── S1 (v3 §3.5): um redemoinho só; o quadro da esquerda vira bandeira → disco das polares → tigela, no mesmo lugar ──
        self.an("S1")
        self.secao("RESUMO")
        cE, cD = P3(-3.4, 0.55), P3(3.4, 0.55)
        fl = mini_bandeira(cE, s=0.42)
        rd = mini_redemoinho(cD, s=0.42)
        self.play(FadeIn(fl), FadeIn(rd), run_time=0.8)
        plD = Plano(cD, 0.42)
        self.add(Particulas(self, GIRO, lambda xy: np.array([plD.c2p(x, y) for x, y in xy]), lambda x, y: math.hypot(x, y) < 3.1, n=40, vel=1.0, rmax=3.1, semente=21))      # v6 §6: miniatura viva
        f_ = F("f", ":", ("A", GEO), r"\subset", (r"\mathbb{R}^n", GEO), r"\to", (r"\mathbb{R}^m", SAI), size=M_M).move_to(P3(-3.4, -2.75))
        fv = F((r"\vec F", CAMPO), "(", ("X", POS), ")", r"\ \text{aplicado em}\ ", ("X", POS), size=M_M).move_to(P3(3.4, -2.75))
        self.gat("como transformação ela move os pontos")
        self.play(rd.animate.set_opacity(0.3), run_time=0.4)
        self.play(caneta(f_))
        disco = mini_disco(cE, r=1.25)
        self.gat("segmentos viram circunferências")
        self.play(FadeOut(fl), Create(disco[-1]), run_time=0.7)
        self.remove(fl)
        self.gat("retângulos viram discos")
        self.play(FadeIn(VGroup(*disco[:-1])), run_time=0.7)
        tig = mini_tigela(cE, w=1.45)
        self.gat("folhas viram tigelas")
        self.play(FadeTransform(disco, tig), run_time=0.8)
        self.gat("ela pendura uma seta em cada ponto")
        self.play(rd.animate.set_opacity(1.0), run_time=0.5)
        self.play(caneta(fv), pulso(rd, 1.04))
        self.gat("e as duas leituras são necessárias")
        self.play(pulso(tig, 1.04), pulso(rd, 1.04), run_time=1.0)

        # ── S2 · o disco das polares e o redemoinho, lado a lado ──
        self.an("S2")
        disco2 = mini_disco(cE, r=1.25)
        self.play(FadeOut(VGroup(f_, fv)), FadeTransform(tig, disco2), run_time=0.7)
        self.remove(f_, fv)
        self.gat("trocar de coordenadas dentro de uma integral")
        self.play(pulso(disco2, 1.05), run_time=1.0)
        self.gat("os campos voltam")
        self.play(pulso(rd, 1.05), run_time=1.0)

        # ── CTA (v3 §3.5): sem tempo morto; a logo entra logo depois da pergunta, a 100%, com anéis visíveis; hold de 3 s e fim ──
        self.an("CTA")
        tudo = [m for m in self.mobjects if m is not self.clk and not isinstance(m, ValueTracker)]
        ax = Plano((0, -0.45), 1.0)
        rdm = campo(ax, GIRO, grade_pts(3.0, 1.0), 0.28, "CTA redemoinho")
        barco = barquinho(ax.c2p(1.6, 0.0))
        perg = txt("O BARQUINHO GIRA EM TORNO DE SI MESMO?", 34, bold=True).move_to(P3(0, 3.3))
        self.play(*[FadeOut(m) for m in tudo], FadeIn(rdm), run_time=0.6)
        self.remove(*tudo)
        self.h2 = None
        self.play(FadeIn(barco, shift=0.15 * DOWN), FadeIn(perg, shift=0.1 * DOWN), run_time=0.6)
        CL = P3(0, 0.9)
        logo = self.logo(5.6).move_to(CL)
        aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(CL), num_dashes=48).set_stroke(GEO, 2.6, opacity=o) for r, o in ((2.1, 0.85), (2.45, 0.6))])
        ins = VGroup(txt("INSCREVA-SE PARA ACOMPANHAR", 40, bold=True), txt("OS PRÓXIMOS VÍDEOS", 40, bold=True)).arrange(DOWN, buff=0.12).move_to(P3(0, -2.6))
        self.gat("deixa a sua resposta")
        self.play(FadeOut(VGroup(rdm, barco, perg)), FadeIn(logo, scale=0.96), FadeIn(aneis), FadeIn(ins, shift=0.1 * UP), run_time=0.45)
        self.remove(rdm, barco, perg)
        rt = self.resta() + 3.0                                   # até o fim da fala e mais 3 s de hold
        self.play(Rotate(aneis[0], 0.3 * rt, rate_func=linear), Rotate(aneis[1], -0.24 * rt, rate_func=linear), run_time=rt)
