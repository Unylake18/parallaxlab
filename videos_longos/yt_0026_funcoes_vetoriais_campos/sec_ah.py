"""Lote PAH: A1 (bem-vindos, título, NESTE VÍDEO; o canto entra) e o hook H1–H3: a mesma fórmula (−y, x) como transformação
(a malha com a bandeira gira +90° de uma vez) e como campo (redemoinho; pontinhos girando com um Rotate do grupo a 1 rad/s). Sem fórmulas."""
from kit import *  # noqa: F401,F403

GIRO = lambda x, y: (-y, x)
K_H = 0.2        # escala do campo do hook: maior seta (r = 3) = 0,675 = 0,9 × espaçamento 0,75
PASSO_H = 0.75


def pontinhos(pl):
    pos = [(0.7, 0.3), (1.3, -0.9), (-0.4, 1.5), (-1.6, -0.5), (2.2, 0.8), (-2.0, 1.6), (0.3, -2.3), (-1.1, -1.9), (1.7, 1.9), (2.6, -1.0)]
    return VGroup(*[ponto(pl.c2p(x, y), POS, 0.085) for x, y in pos])


class LoteAH(Base):
    CANTO = False

    def corpo(self):
        # ── A1 ──
        self.an("A1")
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(P3(0, 0.9)), num_dashes=48).set_stroke(GEO, 2.2, opacity=o) for r, o in ((2.1, 0.45), (2.45, 0.25))])
        bv = txt("BEM-VINDOS AO PARALLAX LAB", 34).move_to(P3(0, -2.5))
        self.play(FadeIn(logo, scale=0.94), FadeIn(aneis), FadeIn(bv, shift=0.1 * UP), run_time=0.8)
        self.play(Rotate(aneis[0], 0.5), Rotate(aneis[1], -0.4), rate_func=linear, run_time=3.0)
        self.gat("o assunto de hoje")
        tit = VGroup(txt("FUNÇÕES A VALORES VETORIAIS", 46, bold=True), txt("E CAMPOS VETORIAIS", 46, bold=True)).arrange(DOWN, buff=0.18).move_to(P3(0, 1.1))
        nv = linha_texto(txt("NESTE VÍDEO:", 28, bold=True, color=CAMPO), txt("TRANSFORMAÇÃO · IMAGEM · CAMPO VETORIAL", 28)).move_to(P3(0, -1.0))
        self.play(FadeOut(logo), FadeOut(aneis), FadeOut(bv), run_time=0.35)
        self.remove(logo, aneis, bv)
        self.play(FadeIn(tit, shift=0.1 * UP), FadeIn(self.h1), run_time=0.7)
        self.gat("a gente vai ver")
        self.play(FadeIn(nv, shift=0.1 * UP), run_time=0.6)
        self.gat("como transformação e como campo")
        self.play(pulso(nv[1], 1.04), run_time=1.0)
        self.gat("para começar")
        self.play(FadeOut(tit), FadeOut(nv), run_time=0.4)
        self.remove(tit, nv)

        # ── H1 · a malha gira +90° (transformação aplicada uma vez) ──
        self.an("H1")
        O = P3(0, -0.25)
        pl = Plano(O, 1.0)
        folha = malha(pl, -3, 3, -3, 3, 0.6)                 # chapa do domínio ±3: o mesmo tamanho do disco do campo (H3)
        band = bandeira(pl, s=1.5).set_z_index(3)            # bandeira coral (objeto de teste), com contorno
        centro = ponto(O, GEO, 0.07, z=7)
        grupo = VGroup(folha, band)
        self.play(FadeIn(folha), run_time=0.8)
        self.gat("com uma bandeirinha desenhada")
        self.play(FadeIn(band, shift=0.1 * UP), FadeIn(centro), run_time=0.6)
        self.gat("o plano inteiro gira")
        self.play(Rotate(grupo, PI / 2, about_point=O), run_time=2.6)
        self.ate(0.97)

        # ── H2 · a mesma regra como campo: redemoinho e pontinhos girando ──
        self.an("H2")
        folha0 = malha(pl, -3, 3, -3, 3, 0.6)
        self.play(FadeOut(grupo), FadeIn(folha0), run_time=0.7)
        self.remove(grupo)
        cmp = campo(pl, lambda x, y: (-y, x), grade_pts(3.0, PASSO_H), K_H, "H2 giro (−y, x)", passo=PASSO_H)
        self.gat("pendura em cada ponto")
        self.play(folha0[1].animate.set_stroke(opacity=0.25), LaggedStart(*[GrowArrow(s) for s in sorted(cmp, key=lambda s: math.hypot(*s._xy))], lag_ratio=0.04),
                  run_time=2.4)
        part_h = Particulas(self, GIRO, lambda xy: np.array([pl.c2p(x, y) for x, y in xy]), lambda x, y: math.hypot(x, y) < 3.1, n=100, vel=1.0, rmax=3.1, semente=8)
        self.add(part_h)      # v6 §6: o redemoinho do gancho também corre
        self.gat("solta uns pontinhos")
        pts = pontinhos(pl)
        self.play(FadeIn(pts, scale=0.5), run_time=0.4)
        rt = self.resta() - 0.1
        self.play(Rotate(pts, rt * 1.0, about_point=O), rate_func=linear, run_time=rt)       # 1 rad/s, o mesmo período para todos
        ang = rt

        # ── H3 · tela dividida: à esquerda a bandeira girada, à direita o redemoinho; a pergunta no alto ──
        self.an("H3")
        part_h.clear_updaters()
        self.remove(part_h)
        s = 0.72                                             # v3: os dois painéis com o mesmo tamanho (chapa ±3), 20% maiores
        E, D = P3(-3.95, -0.55) - O, P3(3.95, -0.55) - O
        esq = VGroup(malha(pl, -3, 3, -3, 3, 0.6), bandeira(pl, s=1.5), ponto(O, GEO, 0.07))
        esq.rotate(PI / 2, about_point=O).scale(s, about_point=O).shift(E)
        dir_ = VGroup(folha0, cmp)
        self.play(dir_.animate.scale(s, about_point=O).shift(D), pts.animate.scale(s, about_point=O).shift(D),
                  FadeOut(centro), FadeIn(esq, shift=0.2 * RIGHT), run_time=1.0)
        self.remove(centro)
        perg = txt("MESMA FÓRMULA. QUAL É O DESENHO CERTO?", 32, bold=True).move_to(P3(0, 2.75))
        self.gat("é a mesma fórmula")
        self.play(FadeIn(perg, shift=0.1 * DOWN), run_time=0.6)
        rt = self.resta() - 0.45
        self.play(Rotate(pts, rt, about_point=O + D), rate_func=linear, run_time=rt)
        ang += rt
        print(f"[hook] pontinhos giraram {ang:.2f} rad = {ang / (2 * PI):.2f} voltas a 1 rad/s")
        self.sai_fim()
