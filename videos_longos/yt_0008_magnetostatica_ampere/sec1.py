"""N01–N05 (V2): a pergunta nova, o paradoxo do fio, a sonda local, a circulação global e o divergente de B.

Representação canônica do fio (V2):
  · 2.5D (vista levemente de cima): fio + 3 círculos IGUAIS em alturas igualmente espaçadas → simetria ao longo do fio;
  · vista de cima (2D): círculos concêntricos + vetores tangentes de comprimento ∝ 1/s → dependência radial.
Nunca as duas ideias na mesma geometria. Tudo que depende da vista é `cached`/`pin`; nada é animado filho-a-filho de grupo
persistente (origem dos anéis duplicados da V1); quem sai, sai com `out()`/`purge()`.
"""
import math

import numpy as np
from manim import (
    VGroup, Line, DashedLine, Dot, FadeIn, FadeOut, Create, Indicate, ValueTracker, DecimalNumber, Circle, DashedVMobject,
    TransformFromCopy, ReplacementTransform, Flash, LaggedStart, linear, smooth, there_and_back, UP, DOWN, LEFT, RIGHT, DL, UR,
)
from base import *  # noqa: F401,F403
from fisica import circulacao, b_fio, TAU

S0 = 1.6          # raio canônico: círculo de B que passa por P
RHO = 0.5         # raio da sonda
HS = (-1.35, 0.0, 1.35)
ABERTURA_S = 100.0   # gancho + saudação (≈ 100 s de fala a 2,8 palavras/s)
VIEW_FIO = dict(x=-3.9, y=-0.35, scale=0.95, beta=0, tau=-22)


def bl(s):
    """Comprimento de tela do vetor B (∝ 1/s), escolhido para ser legível: 1,0 em s = S0."""
    return 1.0 * S0 / s


class Sec1:
    # ── utilitários locais ──────────────────────────────────────────────────────────────────────────────────
    def header(self, title):
        self.evento("titulo", title)
        new = txt(title, T_HEAD).move_to([0, 3.3, 0])
        if self.head is not None:
            self.play(FadeOut(self.head), run_time=0.25)
            self.purge(self.head)
        self.play(FadeIn(new), run_time=0.5)
        self.head = new

    def hl_many(self, items, slot="H", color=MAG, rt=1.0):
        eq = self.slots[slot]["eq"]
        rs = VGroup(*[box(glyphs(eq, t, o), color, buff=0.08, width=3) for t, o in items])
        self.play(FadeIn(rs), run_time=0.3)
        self.hold(rt)
        self.out(rs, rt=0.25)

    def strike(self, items, slot="H", color=WHITE):
        """Risca termos (cancelamento visível) antes de o glyph map retirá-los."""
        eq = self.slots[slot]["eq"]
        lines = VGroup()
        for t, o in items:
            g = glyphs(eq, t, o)
            lines.add(Line(g.get_corner(DL) + [-0.04, -0.04, 0], g.get_corner(UR) + [0.04, 0.04, 0], color=color, stroke_width=4).set_z_index(20))
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.3), run_time=0.8)
        return lines

    def readout(self, lhs, value_fn, slot="A", unit=None, places=2, size=M_M):
        """Cartão com leitura numérica viva: lhs (MathTex) + número que segue value_fn()."""
        num = DecimalNumber(value_fn(), num_decimal_places=places, font_size=size * 0.95, unit=unit)
        num.add_updater(lambda m: m.set_value(value_fn()))
        return self.card_group(VGroup(lhs, num).arrange(RIGHT, buff=0.18), slot)

    def card_group(self, g, slot="A"):
        """Coloca um grupo não-token (leituras, inset) no cartão do slot, com ciclo de vida do slot."""
        g.move_to(self.slots[slot]["pos"])
        card = self._card(slot)
        self.play(*([FadeIn(card)] if card is not None else []), FadeIn(g), run_time=0.7)
        self.slots[slot]["eq"] = g
        return g

    def callout(self, label, target_pt, label_pt):
        """Rótulo fora do desenho com linha de chamada até o ponto."""
        label.move_to(label_pt)
        d = np.asarray(target_pt, dtype=float) - label.get_center()
        start = label.get_center() + d / max(np.linalg.norm(d), 1e-6) * (0.5 * max(label.width, label.height) + 0.08)
        ln = Line(start, target_pt, color=DIM, stroke_width=1.8).set_z_index(11)
        return VGroup(ln, label)

    # ── geometria canônica do fio ───────────────────────────────────────────────────────────────────────────
    def fio_ring(self, h, op=1.0):
        return self.cached(lambda h=h: (*self.view_key(), op), lambda h=h: self.ring_y(S0, h, width=3.6, op=op, arrows=2, tip=0.3))

    def top_symbol(self):
        """⊙ no eixo quando a vista é de cima (o fio aparece de ponta)."""
        def f():
            k = max(0.0, min(1.0, (-self.tau.get_value() - 70) / 20))
            return self.out_symbol(self.W([0, 0, 0]), 1, 0.2, GREEN).set_opacity(k)
        return self.cached(self.view_key, f)

    def swap_wire(self, half, *anims, rt=1.0, **kw):
        """Troca o fio por outro de meia-altura `half` (fade cruzado) junto com `anims`: nos zooms o fio longo atravessava título e legenda."""
        old = self.wire
        self.wire = self.cached(self.view_key, lambda: self.wire_y(-half, half))
        oldf = self.wflow
        self.wflow = self.flow_y(-half, half, count=max(4, int(half * 3.3)))
        self.add(self.wflow)
        self.play(FadeOut(old), FadeIn(self.wire), *anims, run_time=rt, **kw)
        self.purge(old)
        self.purge(oldf)

    # ── abertura (gancho + saudação): a tela acompanha a fala, sem texto que repita a narração ──────────────────────
    def cartao(self, conteudo, pos, w, h):
        """Cartão de abertura (painel + conteúdo); não emite evento de sincronismo."""
        conteudo.move_to(pos)
        return VGroup(panel(w, h, pos), conteudo)

    def abertura(self):
        self.section("abertura")
        t0 = float(self.time)
        self.reset_view(**VIEW_FIO)
        ttl = txt("Divergente e rotacional de B: a Lei de Ampère", T_HEAD).move_to([0, 3.3, 0])
        self.head = ttl
        self.wire = self.cached(self.view_key, lambda: self.wire_y(-2.4, 2.4))
        self.play(Create(self.wire), FadeIn(ttl), run_time=1.2)
        self.wflow = self.flow_y(-2.4, 2.4, count=8)
        self.add(self.wflow)
        rings = VGroup(*[self.fio_ring(h) for h in HS])
        self.caption("As linhas de campo dão voltas completas em volta da corrente")       # alvo da voz: «As linhas de campo»
        self.play(Create(rings), run_time=2.0)
        if self.na_fala("tudo parece estar girando"):
            self.destaque(rings, WHITE, 1.0, 1.2)
        self.show(E(r"\nabla\times\mathbf B=\mathbf 0\qquad(s>0)", r"\nabla\times\mathbf B", r"\mathbf 0", r"(s>0)", size=M_XL), rt=1.6, wait=1.0)
        self.caption("Fora do fio, o rotacional é zero. Como pode?")                          # alvo da voz: «Como um campo pode circular»
        if self.na_fala("em torno de uma corrente"):
            self.destaque(rings, WHITE, 1.0, 1.2)
        if self.na_fala("rotacional nulo"):
            eq = self.slots["H"]["eq"]
            bx = box(glyphs(eq, r"\mathbf 0", 0), WHITE, buff=0.12, width=3)
            self.play(FadeIn(bx), run_time=0.3)
            self.hold(1.4)
            self.out(bx, rt=0.25)
        if self.na_fala("aparente contradicao"):
            self.destaque(rings, WHITE, 1.0, 1.0)
            self.destaque(self.slots["H"]["eq"], WHITE, 1.06, 1.0)
        if SYNC is not None:
            # saudação: o fio sai e entra a marca; depois os dois episódios anteriores; depois o caminho que o 5.3 vai seguir
            marca = jb = bj = c51 = c52 = None
            if self.na_fala("fala pessoal"):
                self.out(self.wire, self.wflow, rings, rt=0.7)
                self.drop("H", keep_card=False, rt=0.5)
                marca = VGroup(txt("PARALLAX LAB", 58), txt("MAGNETOSTÁTICA · DIVERGENTE E ROTACIONAL DE B · LEI DE AMPÈRE", 24, DIM)).arrange(DOWN, buff=0.35).move_to([0, 0.2, 0])
                self.play(FadeIn(marca, shift=UP * 0.12), run_time=0.9)
            if self.na_fala("nos videos anteriores") and marca is not None:
                self.out(marca, rt=0.5)
            if self.na_fala("forca magnetica"):
                c51 = self.cartao(txt("Força magnética", 38), [-3.7, 0.3, 0], 5.6, 2.4)
                self.play(FadeIn(c51, shift=UP * 0.1), run_time=0.7)
            if self.na_fala("lei de biot"):
                c52 = self.cartao(txt("Lei de Biot–Savart", 38), [3.7, 0.3, 0], 5.6, 2.4)
                self.play(FadeIn(c52, shift=UP * 0.1), run_time=0.7)
            if self.na_fala("mudar a pergunta") and c52 is not None:
                self.play(Indicate(c52, color=WHITE, scale_factor=1.04), run_time=1.0)
            if self.na_fala("em vez de comecar pela corrente"):
                self.out(*[m for m in (c51, c52) if m is not None], rt=0.5)
                jb = self.cartao(E(r"\mathbf J\ \longrightarrow\ \mathbf B", r"\mathbf J", r"\mathbf B", size=M_XL), [0, 0.4, 0], 6.4, 1.9)
                self.play(FadeIn(jb), run_time=0.7)
            if self.na_fala("olhar para o proprio campo") and jb is not None:
                self.out(jb, rt=0.4)
                bj = self.cartao(E(r"\mathbf B\ \longrightarrow\ \text{?}", r"\mathbf B", r"\text{?}", size=M_XL), [0, 0.4, 0], 6.4, 1.9)
                self.play(FadeIn(bj), run_time=0.7)
            if self.na_fala("geometria revela") and bj is not None:
                self.out(bj, rt=0.4)
                bj = self.cartao(E(r"\mathbf B\ \longrightarrow\ \mathbf J\ \text{?}", r"\mathbf B", r"\mathbf J", r"\text{?}", size=M_XL), [0, 0.4, 0], 6.4, 1.9)
                self.play(FadeIn(bj), run_time=0.7)
            # os três chips do caminho: mesma altura, intervalos iguais e o conjunto centrado na tela (x = 0); cores do vídeo (B magenta, J/I verde, dℓ branco)
            chips = (("ao divergente", r"\nabla\cdot\mathbf B", (r"\nabla\cdot\mathbf B",), 3.0),
                     ("ao seu rotacional", r"\nabla\times\mathbf B", (r"\nabla\times\mathbf B",), 3.0),
                     ("finalmente", r"\oint\mathbf B\cdot d\boldsymbol\ell=\mu_0 I_{\rm env}", (r"\mathbf B", r"d\boldsymbol\ell", r"I_{\rm env}"), 5.6))
            gap, x = 0.45, -(sum(c[3] for c in chips) + 0.45 * (len(chips) - 1)) / 2
            for rx, tex, iso, w in chips:
                cx, x = x + w / 2, x + w + gap
                if self.na_fala(rx):
                    eq = E(tex, *iso, size=M_M)
                    if eq.width > w - 0.4:
                        eq.scale_to_fit_width(w - 0.4)
                    cc = self.cartao(eq, [cx, -2.0, 0], w, 1.5)
                    self.play(FadeIn(cc, shift=UP * 0.1), run_time=0.5)
            self.hold_ate(SYNC["abertura"]["pergunta"] - 0.9)
            self.head = None      # o título sai junto com o resto, no clear() (0,9 s) que termina na fala «Comecemos»
        else:
            self.hold(max(0.0, ABERTURA_S - (float(self.time) - t0) - 1.0))
        self.mark("n00_abertura")
        self.clear()

    # ── N01 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def pergunta(self):
        self.section("pergunta")
        self.reset_view(**VIEW_FIO)
        W = self.W
        self.wire = self.cached(self.view_key, lambda: self.wire_y(-2.4, 2.4))
        self.play(Create(self.wire), run_time=1.2)
        self.wflow = self.flow_y(-2.4, 2.4, count=8)
        self.add(self.wflow)
        self.ia = self.cached(self.view_key, lambda: arrow(self.W([-0.42, -0.85, 0]), self.W([-0.42, 0.25, 0]), GREEN, 6))
        self.il = self.pin(self.lab("I", [0, 0, 0], "I", size=M_M), lambda: self.W([-0.82, -0.3, 0]))
        self.play(FadeIn(self.ia), FadeIn(self.il), run_time=0.8)
        self.caption("Um fio longo, retilíneo, com corrente $I$")
        self.hold(1.5)
        # um círculo, depois o sentido
        mid = self.fio_ring(0.0)
        self.play(Create(mid), run_time=1.6)
        self.caption("O campo de Biot–Savart circula em volta do fio; o sentido vem da mão direita")
        blab = self.pin(self.lab(r"\mathbf B", [0, 0, 0], r"\mathbf B", size=M_L), lambda: self.W([S0 * math.sin(0.75), 0, S0 * math.cos(0.75)]) + np.array([0.45, -0.32, 0]))
        self.play(FadeIn(blab), Indicate(mid, color=WHITE, scale_factor=1.0), run_time=1.0)
        self.show(E(r"\mathbf J\ \longrightarrow\ \text{Biot--Savart}\ \longrightarrow\ \mathbf B", r"\mathbf J", r"\text{Biot--Savart}", r"\mathbf B", size=M_L),
                  rt=1.4, wait=1.0)
        self.mark("n01_um_circulo")
        # o mesmo padrão em outras alturas
        top, bot = self.fio_ring(HS[2]), self.fio_ring(HS[0])
        self.play(TransformFromCopy(mid, top), TransformFromCopy(mid, bot), run_time=1.8)
        self.caption("O mesmo padrão se repete em qualquer altura: o fio infinito é igual ao longo do seu eixo")
        self.rings = VGroup(bot, mid, top)
        self.ring_mid, self.blab = mid, blab
        self.mark("n01_simetria_axial")
        self.hold(2.0)
        self.caption("Agora a pergunta se inverte: dado $\\mathbf B$, o que a geometria dele revela?")
        self.show(E(r"\mathbf B\ \longrightarrow\ \text{?}", r"\mathbf B", r"\text{?}", size=M_XL), (r"\mathbf B", r"\mathbf B"), rt=1.8, wait=1.0)
        self.header("O que a geometria de B revela?")
        self.mark("n01_pergunta")
        self.hold(2.0)

    # ── N02 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def paradoxo(self):
        self.section("paradoxo")
        W = self.W
        self.drop("H", keep_card=False)
        # 2.5D → vista de cima: a dependência radial pede outra geometria
        self.caption("Para ver como $B$ muda com a distância, olhe de cima")
        self.out(self.rings[0], self.rings[2], self.ia, self.blab, rt=0.6)
        sym = self.top_symbol()
        self.add(sym)
        self.play(self.tau.animate.set_value(-90), self.gs.animate.set_value(1.05), self.ox.animate.set_value(-4.3), self.oy.animate.set_value(-0.2),
                  FadeOut(self.wflow), run_time=2.4)
        self.purge(self.wflow)
        circs = VGroup(*[DashedVMobject(Circle(radius=r * self.gs.get_value(), color=MAG, stroke_width=2.4).move_to(W([0, 0, 0])), num_dashes=int(22 * r))
                         .set_stroke(opacity=0.55) for r in (0.8, 2.4)])
        self.play(Create(circs), run_time=1.2)
        P = np.array([S0, 0.0, 0.0])
        sline = Line(W([0, 0, 0]), W(P), color=VIOLET, stroke_width=3).set_z_index(6)
        pd = Dot(W(P), radius=0.08, color=WHITE).set_z_index(9)
        sL = self.lab("s", W(P / 2) + np.array([0, -0.3, 0]), "s", size=M_M)
        pL = self.lab("P", W(P) + np.array([0.32, -0.3, 0]), size=M_M)
        self.play(Create(sline), FadeIn(pd), FadeIn(sL), FadeIn(pL), run_time=1.0)
        bv = arrow(W(P), W(P) + np.array([0, bl(S0), 0]), MAG, 7, tip=0.3).set_z_index(8)
        bL = self.lab(r"\mathbf B", W(P) + np.array([0.42, bl(S0) * 0.75, 0]), r"\mathbf B", size=M_L)
        self.play(Create(bv), FadeIn(bL), run_time=1.0)
        self.caption("Em $P$, $\\mathbf B$ é tangente ao círculo de raio $s$: direção $\\hat{\\boldsymbol\\phi}$")
        self.show(E(r"\mathbf B=\frac{\mu_0 I}{2\pi s}\,\hat{\boldsymbol\phi}", r"\mathbf B", r"\frac{\mu_0 I}{2\pi s}", r"\hat{\boldsymbol\phi}", size=M_L),
                  slot="A", src={(r"\mathbf B", 0): bL}, rt=1.8, wait=1.0)
        self.mark("n02_vista_de_cima")
        # módulo: três raios, três comprimentos
        others = VGroup(*[arrow(W([r, 0, 0]), W([r, 0, 0]) + np.array([0, bl(r), 0]), MAG, 6, tip=0.26).set_z_index(8) for r in (0.8, 2.4)])
        dots = VGroup(*[Dot(W([r, 0, 0]), radius=0.06, color=WHITE).set_z_index(9) for r in (0.8, 2.4)])
        self.play(FadeIn(dots), Create(others), run_time=1.2)
        self.caption("Mais longe, mais fraco: o comprimento de $\\mathbf B$ cai como $1/s$")
        self.hold(2.5)
        self.out(others, dots, rt=0.5)
        # o cálculo: (∇×B)_z em cilíndricas
        self.caption("O rotacional desse campo: em cilíndricas, a componente ao longo do fio é")
        T = (r"(\nabla\times\mathbf B)_z", r"\frac{1}{s}", r"\frac{d}{ds}", r"s\,", r"B_\phi")
        self.show(E(r"(\nabla\times\mathbf B)_z=\frac{1}{s}\frac{d}{ds}\left(s\,B_\phi\right)", *T, size=M_L), rt=1.4, wait=1.5)
        self.hl(r"B_\phi")
        aux = self.slots["A"]["eq"]
        T2 = (r"(\nabla\times\mathbf B)_z", r"\frac{1}{s}", r"\frac{d}{ds}", r"s\,", r"\mu_0 I", r"2\pi", r"\,s")
        self.caption("Entra o valor de Biot–Savart no lugar de $B_\\phi$")
        self.show(E(r"(\nabla\times\mathbf B)_z=\frac{1}{s}\frac{d}{ds}\left(s\,\frac{\mu_0 I}{2\pi\,s}\right)", *T2, size=M_L),
                  (r"B_\phi", None), src={((r"\mu_0 I", 0), (r"2\pi", 0), (r"\,s", 0)): glyphs(aux, r"\frac{\mu_0 I}{2\pi s}", 0)}, rt=2.0, wait=1.0)
        lines = self.strike([(r"s\,", 0), (r"\,s", 0)])
        self.caption("O $s$ que multiplica cancela o $s$ do denominador")
        self.hold(1.0)
        self.play(FadeOut(lines), run_time=0.3)
        self.purge(lines)
        self.show(E(r"(\nabla\times\mathbf B)_z=\frac{1}{s}\frac{d}{ds}\left(\frac{\mu_0 I}{2\pi}\right)", r"(\nabla\times\mathbf B)_z", r"\frac{1}{s}",
                    r"\frac{d}{ds}", r"\mu_0 I", r"2\pi", size=M_L), (r"s\,", None), (r"\,s", None), rt=1.8, wait=1.0)
        self.mark("n02_cancela_s")
        # o desenho responde: s cresce, B diminui, s·B fica igual
        self.caption("$s\\,B_\\phi$ não depende de $s$: afaste $P$ do raio inicial $s_0$ (com $B_0=\\mu_0 I/2\\pi s_0$) e veja o produto ficar constante")
        self.sP = ValueTracker(S0)
        Pd = lambda: np.array([self.sP.get_value(), 0, 0])
        mv = self.cached(lambda: (self.sP.get_value(), *self.view_key()), lambda: VGroup(
            Line(W([0, 0, 0]), W(Pd()), color=VIOLET, stroke_width=3).set_z_index(6),
            Dot(W(Pd()), radius=0.08, color=WHITE).set_z_index(9),
            arrow(W(Pd()), W(Pd()) + np.array([0, bl(self.sP.get_value()), 0]), MAG, 7, tip=0.3).set_z_index(8)))
        self.remove(sline, pd, bv)
        self.add(mv)
        self.play(FadeOut(pL), FadeOut(bL), FadeOut(sL), run_time=0.3)
        self.purge(pL, bL, sL)
        self.drop("A", keep_card=False)
        rows = VGroup(      # leituras adimensionais: s0 = raio inicial, B0 = μ0 I / (2π s0)
            VGroup(E(r"s/s_0=", "s", size=M_S), DecimalNumber(1.0, num_decimal_places=2, font_size=36)).arrange(RIGHT, buff=0.12),
            VGroup(E(r"B_\phi/B_0=", r"B_\phi", size=M_S), DecimalNumber(1.0, num_decimal_places=2, font_size=36)).arrange(RIGHT, buff=0.1),
            VGroup(E(r"\frac{s\,B_\phi}{s_0B_0}=", r"B_\phi", size=M_S), DecimalNumber(1.0, num_decimal_places=2, font_size=36)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rows[0][1].add_updater(lambda m: m.set_value(self.sP.get_value() / S0))
        rows[1][1].add_updater(lambda m: m.set_value(S0 / self.sP.get_value()))
        rows[2][1].add_updater(lambda m: m.set_value(1.0))
        self.card_group(rows, "A")
        self.play(self.sP.animate.set_value(2.6), run_time=3.0)
        self.play(self.sP.animate.set_value(0.75), run_time=3.5)
        self.play(self.sP.animate.set_value(S0), run_time=1.6)
        self.mark("n02_sB_constante")
        for r_ in rows:
            r_[1].clear_updaters()
        self.drop("A", keep_card=False)
        self.caption("A derivada de uma constante é zero")
        self.show(E(r"(\nabla\times\mathbf B)_z=\frac{1}{s}\cdot 0", r"(\nabla\times\mathbf B)_z", r"\frac{1}{s}", "0", size=M_L),
                  (r"\frac{d}{ds}", "0"), (r"\mu_0 I", None), (r"2\pi", None), rt=1.8, wait=1.0, structure=False)
        self.show(E(r"(\nabla\times\mathbf B)_z=0", r"(\nabla\times\mathbf B)_z", "0", size=M_XL), (r"\frac{1}{s}", None), rt=1.4, wait=0.8)
        self.caption("$\\mathbf B$ só tem componente $\\phi$ e só depende de $s$: as outras componentes já são nulas")
        self.hold(2.0)
        self.show(E(r"\nabla\times\mathbf B=\mathbf 0\qquad(s>0)", r"\nabla\times\mathbf B", r"\mathbf 0", r"(s>0)", size=M_XL),
                  (r"(\nabla\times\mathbf B)_z", r"\nabla\times\mathbf B"), ("0", r"\mathbf 0"), rt=1.8, wait=0.5)
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.5)
        self.caption("Linhas de campo curvas e, mesmo assim, rotacional zero em todo ponto fora do fio")
        self.mark("n02_paradoxo_rot_zero")
        self.hold(3.5)
        self.out(bx, circs, mv, rt=0.6)

    # ── N03 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def sonda(self):
        self.section("sonda")
        W = self.W
        self.drop("H", keep_card=False)
        self.header("Rotacional: uma medida local")
        P = np.array([S0, 0.0, 0.0])
        self.th, self.ph, self.prho, self.pc = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(RHO), ValueTracker(0.0)
        # volta à perspectiva, só o círculo do meio (fundo simplificado) e zoom em P
        self.swap_wire(1.45, self.tau.animate.set_value(-26), self.ox.animate.set_value(-4.1), self.oy.animate.set_value(-0.3), self.gs.animate.set_value(1.6),
                       rt=2.2)
        bg = self.cached(self.view_key, lambda: self.ring_y(S0, 0.0, width=2.4, op=0.2, arrows=0))
        loc = self.cached(self.view_key, lambda: VGroup(*[self.vec(np.array([S0 * math.cos(a), 0, S0 * math.sin(a)]), np.array([math.sin(a), 0, -math.cos(a)]),
                                                                   MAG, scale=0.55, width=6, tip=0.24) for a in (-0.6, 0.6)]))
        self.play(FadeOut(self.ring_mid), FadeIn(bg), FadeIn(loc), run_time=0.8)
        self.purge(self.ring_mid)

        def nvec():
            th, ph = math.radians(self.th.get_value()), math.radians(self.ph.get_value())
            return np.array([math.sin(th) * math.cos(ph), math.cos(th), -math.sin(th) * math.sin(ph)])

        def center():
            return (1 - self.pc.get_value()) * P

        self.nvec, self.pcenter = nvec, center
        key = lambda: (self.th.get_value(), self.ph.get_value(), self.prho.get_value(), self.pc.get_value(), *self.view_key())
        probe = self.cached(key, lambda: VGroup(
            self.loop3d(center(), self.prho.get_value(), nvec(), WHITE, 4.5, fill=0.22, fill_color=BLUE_L, arrows=3, tip=0.26, heads=True),
            self.normal(center(), nvec(), 0.9, WHITE, 5)))
        nL = self.pin(self.lab(r"\hat{\mathbf n}", [0, 0, 0], r"\hat{\mathbf n}", size=M_M),
                      lambda: W(center() + 1.12 * nvec()) + 0.25 * np.array([1, 0.4, 0]))
        aC = self.cached(lambda: (*key(),), lambda: self.callout(self.lab(r"\partial A", [0, 0, 0], r"\partial A", size=M_M),
                                                                  W(center() + self.prho.get_value() * np.array([0, 0, 1.0])), W(center()) + np.array([1.55, -1.2, 0])))
        self.play(FadeIn(probe), FadeIn(nL), FadeIn(aC), run_time=1.2)
        self.caption("Uma sonda: um laço pequeno de área $A$ em torno de $P$, com normal $\\hat{\\mathbf n}$ pela mão direita")
        self.hold(2.0)
        self.caption("A circulação por unidade de área, com o laço encolhendo, mede o rotacional naquele ponto")
        self.show(E(r"(\nabla\times\mathbf B)\cdot\hat{\mathbf n}=\lim_{A\to0}\frac{1}{A}\oint_{\partial A}\mathbf B\cdot d\boldsymbol\ell",
                    r"(\nabla\times\mathbf B)", r"\hat{\mathbf n}", r"\lim_{A\to0}", r"\frac{1}{A}", r"\oint_{\partial A}", r"\mathbf B\cdot d\boldsymbol\ell",
                    size=M_M), src={(r"\hat{\mathbf n}", 0): nL, (r"\frac{1}{A}", 0): probe[0][0], (r"\oint_{\partial A}", 0): aC[1]}, rt=2.2, wait=1.0)
        self.play(self.prho.animate.set_value(0.25), run_time=1.6)
        self.play(self.prho.animate.set_value(RHO), run_time=1.0)
        self.mark("n03_definicao_local")
        # por que dá zero: o setor, visto de cima (2D)
        self.caption("Por que zero aqui? Deforme a sonda em dois arcos e dois raios, e olhe de cima")
        self.play(FadeOut(probe), FadeOut(nL), FadeOut(loc), FadeOut(aC), run_time=0.5)   # sonda volta depois: updaters preservados
        self.purge(aC)
        self.play(self.tau.animate.set_value(-90), self.ox.animate.set_value(-4.1), self.oy.animate.set_value(-0.3), self.gs.animate.set_value(1.6), run_time=2.0)
        s1, s2, dph = S0 - 0.42, S0 + 0.42, 0.36
        arc = lambda r: (lambda t: np.array([r * math.cos(t), 0, -r * math.sin(t)]))
        sector = VGroup(
            self.path3d(arc(s2), -dph, dph, P, WHITE, 4.5), self.path3d(arc(s1), -dph, dph, P, WHITE, 4.5),
            Line(W(arc(s1)(dph)), W(arc(s2)(dph)), color=WHITE, stroke_width=4.5), Line(W(arc(s1)(-dph)), W(arc(s2)(-dph)), color=WHITE, stroke_width=4.5),
        ).set_z_index(7)
        fill = self.poly([arc(s2)(t) for t in np.linspace(-dph, dph, 20)] + [arc(s1)(t) for t in np.linspace(dph, -dph, 20)], BLUE_L, 0.2)
        self.play(Create(sector), FadeIn(fill), run_time=1.4)
        bin_ = arrow(W(arc(s1)(0)), W(arc(s1)(0)) + np.array([0, bl(s1) * 0.62, 0]), MAG, 7, tip=0.28).set_z_index(9)
        bout = arrow(W(arc(s2)(0)), W(arc(s2)(0)) + np.array([0, bl(s2) * 0.62, 0]), MAG, 7, tip=0.28).set_z_index(9)
        lin = self.callout(rich("arco curto · $B$ forte", T_NOTE), W(arc(s1)(-0.2)), W(arc(s1)(0)) + np.array([-1.5, -1.55, 0]))
        lout = self.callout(rich("arco longo · $B$ fraco", T_NOTE), W(arc(s2)(0.2)), W(arc(s2)(0)) + np.array([-1.2, 1.75, 0]))
        lrad = self.callout(rich("raios: $\\mathbf B\\perp d\\boldsymbol\\ell$", T_NOTE), W(arc(S0)(-dph)), W(arc(S0)(-dph)) + np.array([0.9, -1.0, 0]))
        self.play(Create(bin_), Create(bout), FadeIn(lin), FadeIn(lout), run_time=1.4)
        self.play(FadeIn(lrad), run_time=0.6)
        self.caption("Dentro o campo é mais forte, mas o arco é mais curto; fora, o contrário")
        self.show(E(r"\oint\mathbf B\cdot d\boldsymbol\ell=\left(s\,B_\phi\right)_{\rm fora}\Delta\phi-\left(s\,B_\phi\right)_{\rm dentro}\Delta\phi",
                    r"\oint", r"\mathbf B\cdot d\boldsymbol\ell", r"\left(s\,B_\phi\right)_{\rm fora}", r"\left(s\,B_\phi\right)_{\rm dentro}",
                    r"\Delta\phi", size=M_M), slot="A", src={(r"\left(s\,B_\phi\right)_{\rm fora}", 0): lout[1], (r"\left(s\,B_\phi\right)_{\rm dentro}", 0): lin[1]},
                  rt=2.2, wait=1.5)
        self.caption("Como $s\\,B_\\phi$ é o mesmo nos dois arcos, as duas parcelas se anulam")
        self.show(E(r"\oint\mathbf B\cdot d\boldsymbol\ell=0", r"\oint", r"\mathbf B\cdot d\boldsymbol\ell", "0", size=M_L),
                  (r"\left(s\,B_\phi\right)_{\rm fora}", None), (r"\left(s\,B_\phi\right)_{\rm dentro}", None), (r"\Delta\phi", None), slot="A", rt=1.8, wait=1.5)
        self.mark("n03_setor_anula")
        self.out(sector, fill, bin_, bout, lin, lout, lrad, rt=0.6)
        self.drop("A", keep_card=False)
        # a sonda gira em perspectiva: cada orientação mede uma componente
        self.play(self.tau.animate.set_value(-26), self.ox.animate.set_value(-4.1), self.oy.animate.set_value(-0.3), self.gs.animate.set_value(1.6), run_time=1.8)
        self.play(FadeIn(probe), FadeIn(nL), FadeIn(loc), run_time=0.8)
        lhs = E(r"\frac{1}{A}\oint\mathbf B\cdot d\boldsymbol\ell=", r"\mathbf B\cdot d\boldsymbol\ell", size=M_M)
        val = lambda: circulacao(b_fio, center(), self.prho.get_value(), nvec(), 180) / (math.pi * self.prho.get_value() ** 2)
        num = DecimalNumber(0, num_decimal_places=2, font_size=M_M * 0.95)
        num.add_updater(lambda m: m.set_value(abs(val())))
        comp = VGroup(*[E(t, size=M_S) for t in (r"(\nabla\times\mathbf B)_z=0", r"(\nabla\times\mathbf B)_s=0", r"(\nabla\times\mathbf B)_\phi=0")]).arrange(RIGHT, buff=0.45)
        for c in comp:
            c[0][:-2].set_color(MAG)
            c.set_opacity(0)
        ro = VGroup(VGroup(lhs, num).arrange(RIGHT, buff=0.15), comp).arrange(DOWN, buff=0.35)
        if ro.width > 6.0:
            ro.scale_to_fit_width(6.0)
        self.card_group(ro, "A")
        self.caption("Gire a sonda: cada orientação de $\\hat{\\mathbf n}$ mede uma componente do rotacional")
        for i, c in enumerate(comp):
            if i == 1:
                self.play(self.th.animate.set_value(90), self.beta.animate.set_value(-20), run_time=2.6)
            elif i == 2:
                self.play(self.ph.animate.set_value(90), self.beta.animate.set_value(14), run_time=2.6)
            self.play(c.animate.set_opacity(1), run_time=0.6)
            self.hold(1.0)
        self.caption("Três orientações, três componentes, todas nulas: o vetor rotacional em $P$ é $\\mathbf 0$")
        self.mark("n03_sonda_gira")
        self.hold(2.5)
        self.play(self.th.animate.set_value(0), self.ph.animate.set_value(0), self.beta.animate.set_value(0), run_time=2.0)
        num.clear_updaters()
        self.drop("A", keep_card=False)
        self.drop("H", keep_card=False)
        self.probe, self.nL, self.bg, self.loc = probe, nL, bg, loc

    # ── N04 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def circulacao_global(self):
        self.section("circulacao")
        W = self.W
        self.header("Do laço local ao laço global")
        self.out(self.nL, self.loc, rt=0.4)
        self.swap_wire(2.4, self.ox.animate.set_value(-3.9), self.oy.animate.set_value(-0.35), self.gs.animate.set_value(0.95), self.tau.animate.set_value(-30),
                       rt=1.8)
        rings = VGroup(self.fio_ring(HS[0], 0.45), self.fio_ring(HS[2], 0.45))
        self.play(FadeIn(rings), run_time=0.6)
        P = np.array([S0, 0, 0])
        g_star = (S0 - RHO) / (2 * S0 - RHO)          # instante em que o laço passa pelo eixo
        st = lambda g: dict(pc=g, rho=RHO + g * (S0 - RHO))
        self.show(E(r"\oint\mathbf B\cdot d\boldsymbol\ell=0", r"\oint", r"\mathbf B\cdot d\boldsymbol\ell", "0", size=M_L), slot="A", rt=1.0, wait=0.2)
        ie = E(r"I_{\rm env}=0", r"I_{\rm env}", "0", size=M_M).next_to(self.slots["A"]["card"], DOWN, buff=0.15)
        self.play(FadeIn(ie), run_time=0.5)
        self.caption("Aumente o laço até o eixo: enquanto o fio fica de fora, nenhuma corrente o atravessa")
        g1 = 0.85 * g_star
        self.play(self.pc.animate.set_value(st(g1)["pc"]), self.prho.animate.set_value(st(g1)["rho"]), run_time=3.0, rate_func=linear)
        self.hold(1.0)
        self.play(self.pc.animate.set_value(st(g_star)["pc"]), self.prho.animate.set_value(st(g_star)["rho"]), run_time=1.2, rate_func=linear)
        self.caption("Sobre o próprio fio $\\mathbf B$ diverge: a circulação não está definida. Valem os laços de antes e de depois")
        iq = E(r"I_{\rm env}:\ \text{laço sobre o fio}", size=M_M).move_to(ie)
        self.play(Flash(W([0, 0, 0]), color=GREEN, line_length=0.35, num_lines=10, flash_radius=0.35), Indicate(self.wire, color=GREEN, scale_factor=1.0),
                  ReplacementTransform(ie, iq), run_time=1.0)
        self.show(E(r"\oint\mathbf B\cdot d\boldsymbol\ell=\text{indefinida}", r"\oint", r"\mathbf B\cdot d\boldsymbol\ell", r"\text{indefinida}", size=M_L),
                  ("0", None), slot="A", rt=0.8, wait=0.6)
        self.caption("Passado o eixo, a corrente $I$ atravessa o laço")
        g2 = min(1.0, g_star + 0.06)
        self.play(self.pc.animate.set_value(st(g2)["pc"]), self.prho.animate.set_value(st(g2)["rho"]), run_time=0.8)
        ie2 = E(r"I_{\rm env}=I", r"I_{\rm env}", "I", size=M_M).move_to(iq)
        self.play(ReplacementTransform(iq, ie2), run_time=0.8)
        self.show(E(r"\oint\mathbf B\cdot d\boldsymbol\ell=\mu_0 I", r"\oint", r"\mathbf B\cdot d\boldsymbol\ell", r"\mu_0 I", size=M_L),
                  (r"\text{indefinida}", None), slot="A", rt=1.2, wait=0.5)
        self.mark("n04_salto_circulacao")
        self.play(self.pc.animate.set_value(1.0), self.prho.animate.set_value(S0), run_time=2.0)
        self.caption("Envolvendo o fio, a circulação vale $\\mu_0 I$ — qualquer que seja o laço")
        self.hold(1.5)
        # a conta global, a partir de Biot–Savart
        cl = self.lab(r"2\pi s", W([-S0, 0, 0.35 * S0]) + np.array([-0.55, -0.15, 0]), r"2\pi s", size=M_M)
        bt = self.vec(P, [0, 0, -1], MAG, scale=0.9, width=7, tip=0.3)
        bL = self.lab(r"B_\phi(s)", W(P + [0, 0, -0.9]) + np.array([0.75, -0.05, 0]), r"B_\phi(s)", size=M_M)
        self.play(FadeIn(cl), Create(bt), FadeIn(bL), run_time=1.0)
        self.caption("No círculo centrado, $B_\\phi$ é o mesmo em todo ponto e acompanha o caminho")
        self.show(E(r"B_\phi(s)\,2\pi s=\mu_0 I", r"B_\phi(s)", r"2\pi s", "I", size=M_XL), src={(r"B_\phi(s)", 0): bL, (r"2\pi s", 0): cl}, rt=2.0, wait=0.5)
        note = txt("calculado com o campo de Biot–Savart", T_NOTE, DIM).next_to(self.slots["H"]["card"], DOWN, buff=0.12)
        self.play(FadeIn(note), FadeOut(ie2), run_time=0.6)
        self.purge(ie2)
        self.mark("n04_circulacao_global")
        self.hold(2.5)
        self.caption("Rotacional zero em todo ponto fora do fio, circulação global $\\neq 0$: como?")
        self.hold(1.5)
        q = self.pin(E(r"?", size=72).set_color(MAG), lambda: self.W([0, 0.35, 0]) + np.array([0.45, 0.45, 0]))
        self.out(cl, bt, bL, rt=0.4)
        self.swap_wire(1.5, self.gs.animate.set_value(1.25), self.ox.animate.set_value(-4.0), FadeIn(q), rt=2.0)
        self.mark("n04_zoom_eixo")
        self.hold(2.5)
        self.swap_wire(2.4, self.gs.animate.set_value(0.95), self.ox.animate.set_value(-3.9), rt=1.2)
        self.out(q, note, rt=0.4)
        self.fio_left = VGroup(rings)

    # ── N05 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def divergente(self):
        self.section("divergente", "Outra sonda: um volume fechado")
        self.clear()
        self.reset_view(x=-3.6, y=-0.2, scale=1.3, beta=28, tau=-22)
        W = self.W
        H = 1.0
        cube = self.cached(self.view_key, lambda: self.box3d([0, 0, 0], H, BLUE_L, 0.07, 2.4))
        self.play(Create(cube), run_time=1.4)
        self.caption("De perto, numa região pequena, o campo do fio é quase uniforme. Envolva-a com uma caixa fechada")
        lines_ = [(y, z) for y in (-0.5, 0.5) for z in (-0.5, 0.5)]
        fl = self.cached(self.view_key, lambda: VGroup(*[Line(W([-2.4, y, z]), W([2.4, y, z]), color=MAG, stroke_width=2.6).set_opacity(0.7).set_z_index(4)
                                                      for y, z in lines_],
                                                    *[self.vec([1.9, y, z], [1, 0, 0], MAG, scale=0.5, width=5, tip=0.22) for y, z in lines_]))
        self.play(FadeIn(fl), run_time=0.8)
        bLab = self.pin(self.lab(r"\mathbf B", [0, 0, 0], r"\mathbf B", size=M_L), lambda: self.W([2.5, 0.5, 0.5]) + np.array([0.3, 0.25, 0]))
        self.play(FadeIn(bLab), run_time=0.4)
        self.hold(1.0)
        # normais para fora
        nrm = self.cached(self.view_key, lambda: VGroup(self.normal([-H, 0, 0], [-1, 0, 0], 0.85, WHITE, 5), self.normal([H, 0, 0], [1, 0, 0], 0.85, WHITE, 5),
                                                     self.normal([0, H, 0], [0, 1, 0], 0.7, WHITE, 3.5)))
        self.play(FadeIn(nrm), run_time=0.8)
        self.caption("As normais $\\hat{\\mathbf n}$ apontam para fora do volume, em cada face")
        self.hold(1.5)
        face = lambda x: self.poly([[x, -H, -H], [x, H, -H], [x, H, H], [x, -H, H]], MAG, 0.32, z=3)
        f_in = self.cached(self.view_key, lambda: face(-H))
        lin = self.pin(self.lab(r"-\Phi_B", [0, 0, 0], r"-\Phi_B", size=M_L, colors={r"-\Phi_B": MAG}), lambda: self.W([-H, -H, 0]) + np.array([-0.9, -0.95, 0]))
        self.play(FadeIn(f_in), FadeIn(lin), run_time=0.8)
        self.caption("Na face de entrada, $\\mathbf B$ aponta contra $\\hat{\\mathbf n}$: o fluxo é negativo")
        self.hold(2.0)
        f_out = self.cached(self.view_key, lambda: face(H))
        lout = self.pin(self.lab(r"+\Phi_B", [0, 0, 0], r"+\Phi_B", size=M_L, colors={r"+\Phi_B": MAG}), lambda: self.W([H, -H, 0]) + np.array([0.9, -0.95, 0]))
        self.play(FadeIn(f_out), FadeIn(lout), run_time=0.8)
        self.caption("Na face de saída, $\\mathbf B$ acompanha $\\hat{\\mathbf n}$: o mesmo fluxo, positivo")
        self.hold(2.0)
        self.caption("Nas outras quatro faces, $\\mathbf B$ corre paralelo a elas: fluxo zero")
        self.hold(2.0)
        self.show(E(r"-\Phi_B+\Phi_B=0", r"-\Phi_B", r"+\Phi_B", "0", size=M_XL, colors={r"-\Phi_B": MAG, r"+\Phi_B": MAG}), slot="A",
                  src={(r"-\Phi_B", 0): lin, (r"+\Phi_B", 0): lout}, rt=2.0, wait=1.0)
        self.show(E(r"\oint_S\mathbf B\cdot d\mathbf a=0", r"\oint_S", r"\mathbf B\cdot d\mathbf a", "0", size=M_L), rt=1.4, wait=1.0)
        self.caption("Somando todas as faces, o fluxo líquido que sai do volume é zero: lei de Gauss para o magnetismo")
        self.mark("n05_fluxo_faces")
        self.show(E(r"\nabla\cdot\mathbf B=\lim_{V\to0}\frac{1}{V}\oint_S\mathbf B\cdot d\mathbf a", r"\nabla\cdot\mathbf B", r"\lim_{V\to0}", r"\frac{1}{V}",
                    r"\oint_S", r"\mathbf B\cdot d\mathbf a", size=M_M), ("0", None), rt=2.0, wait=1.2)
        self.caption("Encolhendo o volume, o fluxo por volume vira o divergente no ponto")
        self.show(E(r"\nabla\cdot\mathbf B=0", r"\nabla\cdot\mathbf B", "0", size=M_XL), (r"\lim_{V\to0}", None), (r"\frac{1}{V}", None),
                  (r"\oint_S", None), (r"\mathbf B\cdot d\mathbf a", None), rt=1.8, wait=0.3)
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.4)
        self.mark("n05_div_zero")
        self.hold(2.0)
        # contraste: carga elétrica, com espaço próprio
        self.drop("A", keep_card=False)
        self.out(bx, rt=0.3)
        self.out(lin, lout, f_in, f_out, nrm, bLab, rt=0.5)
        self.play(self.ox.animate.set_value(-5.1), self.gs.animate.set_value(0.62), run_time=1.6)
        Q = np.array([-1.5, -0.75, 0])
        sph = VGroup(Circle(radius=1.25, color=CYAN, stroke_width=3).set_fill(CYAN, 0.08).move_to(Q),
                     DashedVMobject(Circle(radius=1.25, color=CYAN).stretch(0.32, 1).move_to(Q), num_dashes=30).set_stroke(CYAN, 2, 0.6))
        qd = VGroup(Dot(Q, radius=0.16, color=BLUE), E("+", size=M_S).move_to(Q))
        ea = VGroup(*[arrow(Q + 0.3 * np.array([math.cos(t), math.sin(t), 0]), Q + 1.75 * np.array([math.cos(t), math.sin(t), 0]), CYAN, 3.5, tip=0.2)
                      for t in np.linspace(0, TAU, 12, endpoint=False) + 0.13])
        el = E(r"\mathbf E", r"\mathbf E", size=M_L).move_to(Q + np.array([1.55, 1.35, 0]))
        self.play(FadeIn(qd), run_time=0.5)
        self.play(Create(ea), FadeIn(el), run_time=1.4)
        self.play(FadeIn(sph), run_time=0.8)
        self.caption("Compare com uma carga: as linhas de $\\mathbf E$ só saem da superfície em volta dela")
        self.show(E(r"\oint_S\mathbf E\cdot d\mathbf a=\frac{Q}{\varepsilon_0}>0", r"\mathbf E", "Q", size=M_L), rt=1.6, wait=2.0)
        self.mark("n05_contraste_carga")
        self.caption("A carga é fonte de $\\mathbf E$. Para $\\mathbf B$ não existe fonte nem sumidouro (eletromagnetismo clássico)")
        self.show(E(r"\nabla\cdot\mathbf B=0", r"\nabla\cdot\mathbf B", "0", size=M_XL), rt=1.4, wait=0.3)
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), Indicate(cube, color=MAG, scale_factor=1.0), run_time=0.8)
        self.hold(3.0)
        self.out(bx, rt=0.3)
