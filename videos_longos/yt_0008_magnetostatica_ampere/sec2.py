"""N06–N07: divergente de B a partir de Biot–Savart; os dois pontos (r, r') e os dois operadores (∇, ∇').

Diagrama fonte–observador num "piso" (plano xz do mundo): D(X, Y, h) = [X, h, −Y]. Em tau = −90 ele aparece plano (X, Y);
inclinando tau, o piso entra em perspectiva e h vira altura (pico do delta em N09).
"""
import math

import numpy as np
from manim import (
    VGroup, Line, DashedLine, Dot, Square, FadeIn, FadeOut, Create, Indicate, ValueTracker, LaggedStart, linear, smooth,
    UP, DOWN, LEFT, RIGHT,
)
from base import *  # noqa: F401,F403
from fisica import TAU, J_at, BLOB_C, BLOB_A, BLOB_B   # J tangente às elipses desenhadas (V2: corrigido)

O_DIAG = (-2.55, 1.05)      # origem dos vetores-posição (afastada para r e r' abrirem em leque)


class Sec2:
    def D(self, X, Y, h=0.0):
        return np.array([X, h, -Y])

    def WD(self, X, Y, h=0.0):
        return self.W(self.D(X, Y, h))

    # ── diagrama vivo: região de corrente, r', r, R, F ─────────────────────────────────────────────────────
    def diag_shapes(self):
        F = self.df
        ox, oy = self.r_x.get_value(), self.r_y.get_value()
        sx, sy = self.s_x.get_value(), self.s_y.get_value()
        WD = self.WD
        g = VGroup()
        k_ = self.dimk.get_value()                  # 1 = região de corrente visível; 0 = fora de cena (quando o protagonista é F, N06/N09)
        blob = VGroup()
        ell = [BLOB_C + np.array([BLOB_A * math.cos(t), BLOB_B * math.sin(t)]) for t in np.linspace(0, TAU, 64)]
        blob.add(self.poly([self.D(*p) for p in ell], GREEN, 0.10 * k_, z=1).set_stroke(GREEN, 1.6, 0.55 * k_))
        for k in (0.35, 0.65, 0.92):
            pts = [BLOB_C + k * np.array([BLOB_A * math.cos(t), BLOB_B * math.sin(t)]) for t in np.linspace(0, TAU, 48)]
            blob.add(self.curve([self.D(*p) for p in pts], GREEN, 1.6, 0.35 * k_, z=2))
            for t in (0.4, 0.4 + TAU / 3, 0.4 + 2 * TAU / 3):
                p = BLOB_C + k * np.array([BLOB_A * math.cos(t), BLOB_B * math.sin(t)])
                d = J_at(*p)                          # a seta da corrente usa o MESMO campo J: tangente à elipse desenhada
                d = 0.2 * d / np.linalg.norm(d)
                blob.add(arrow(WD(*(p - d)), WD(*(p + d)), GREEN, 3.2, z=2, tip=0.17).set_opacity(0.8 * k_))
        if k_ > 0.02:
            g.add(blob)
        if F.get("origin", True):
            O = O_DIAG
            g.add(Dot(WD(*O), radius=0.05, color=WHITE).set_z_index(8))
            g.add(arrow(WD(*O), WD(sx, sy), GREEN, 3, z=5, tip=0.16).set_opacity(0.85))
            g.add(arrow(WD(*O), WD(ox, oy), CYAN, 3, z=5, tip=0.16).set_opacity(0.85))
        if F.get("R", True):
            g.add(arrow(WD(sx, sy), WD(ox, oy), VIOLET, 5, z=6, tip=0.22))
        if F.get("cell", True):
            c = 0.17
            g.add(self.poly([self.D(sx - c, sy - c), self.D(sx + c, sy - c), self.D(sx + c, sy + c), self.D(sx - c, sy + c)], GREEN, 0.25, z=4)
                  .set_stroke(GREEN, 2, 0.9))
        j = J_at(sx, sy)
        if F.get("J", True) and np.linalg.norm(j) > 1e-6:
            g.add(arrow(WD(sx, sy), WD(*(np.array([sx, sy]) + 1.25 * j)), GREEN, 7, z=8, tip=0.22))
        if F.get("pts", True):
            g.add(Dot(WD(sx, sy), radius=0.075, color=GREEN).set_z_index(9))
            if k_ > 0.02:
                g.add(Dot(WD(ox, oy), radius=0.085, color=CYAN).set_z_index(9).set_opacity(k_))
        if F.get("Bobs"):
            g.add(arrow(WD(ox, oy), WD(ox + 0.05, oy + 0.75), MAG, 5, z=8, tip=0.2))
        return g

    def diag_key(self):
        return (self.r_x.get_value(), self.r_y.get_value(), self.s_x.get_value(), self.s_y.get_value(),
                tuple(sorted(self.df.items())), round(self.dimk.get_value(), 3), *self.view_key())

    def diag_labels(self):
        WD = self.WD
        ox, oy, sx, sy = (lambda: self.r_x.get_value()), (lambda: self.r_y.get_value()), (lambda: self.s_x.get_value()), (lambda: self.s_y.get_value())
        L = {}
        Ox, Oy = O_DIAG
        L["r"] = self.pin(self.lab(r"\mathbf r", [0, 0, 0], r"\mathbf r", size=M_M),
                          lambda: WD(Ox + 0.5 * (ox() - Ox), Oy + 0.5 * (oy() - Oy)) + np.array([0.0, 0.3, 0]))
        L["rp"] = self.pin(self.lab(r"\mathbf r'", [0, 0, 0], r"\mathbf r'", size=M_M),
                           lambda: WD(Ox + 0.45 * (sx() - Ox), Oy + 0.45 * (sy() - Oy)) + np.array([-0.32, -0.22, 0]))
        L["R"] = self.pin(self.lab(r"\mathbf R", [0, 0, 0], r"\mathbf R", size=M_M), lambda: WD(0.5 * (sx() + ox()), 0.5 * (sy() + oy())) + np.array([0.3, -0.28, 0]))
        L["J"] = self.pin(self.lab(r"\mathbf J(\mathbf r')", [0, 0, 0], r"\mathbf J(\mathbf r')", size=M_S),
                          lambda: WD(*(np.array([sx(), sy()]) + 1.25 * J_at(sx(), sy()))) + np.array([0.35, -0.25, 0]))
        L["dt"] = self.pin(self.lab(r"d\tau'", [0, 0, 0], r"d\tau'", size=M_S), lambda: WD(sx(), sy()) + np.array([-0.5, 0.05, 0]))
        L["B"] = self.pin(self.lab(r"\mathbf B(\mathbf r)", [0, 0, 0], r"\mathbf B(\mathbf r)", size=M_S), lambda: WD(ox(), oy()) + np.array([0.7, 0.45, 0]))
        L["obs"] = self.pin(txt("observador", T_NOTE, CYAN), lambda: WD(ox(), oy()) + np.array([-0.75, 0.42, 0]))
        L["fonte"] = self.pin(txt("fonte", T_NOTE, GREEN), lambda: WD(sx(), sy()) + np.array([-0.85, -0.42, 0]))
        return L

    # ── N06 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def div_formal(self):
        self.section("div_formal", "Divergente de B a partir de Biot–Savart")
        self.clear()
        self.reset_view(x=-4.35, y=-0.15, scale=1.05, beta=0, tau=-90)
        self.r_x, self.r_y = ValueTracker(1.75), ValueTracker(1.3)
        self.s_x, self.s_y = ValueTracker(-0.75), ValueTracker(-0.35)
        self.df = {"origin": True, "R": True, "cell": True, "J": True, "Bobs": True}
        self.dimk = ValueTracker(1.0)
        diag = self.cached(self.diag_key, self.diag_shapes)
        L = self.diag_labels()
        self.diag, self.dL = diag, L
        self.play(FadeIn(diag), run_time=1.2)
        self.play(FadeIn(L["fonte"]), FadeIn(L["obs"]), run_time=0.6)
        self.caption("Uma distribuição de corrente $\\mathbf J$ localizada: ponto-fonte $\\mathbf r'$ dentro dela, observador $\\mathbf r$ fora")
        self.play(FadeIn(L["r"]), FadeIn(L["rp"]), FadeIn(L["J"]), FadeIn(L["dt"]), FadeIn(L["B"]), FadeIn(L["R"]), run_time=1.0)
        self.hold(2.0)
        # a voz leva ~45 s nomeando os papéis: cada rótulo pulsa quando é dito (sem isso o diagrama ficaria parado)
        for rx, k, cor in (("densidade volumetrica de corrente", "J", GREEN), ("elemento de volume", "dt", GREEN), ("posicao da fonte", "rp", GREEN),
                           ("onde queremos calcular", "B", MAG), ("posicao do observador", "r", CYAN), ("vetor que liga", "R", VIOLET)):
            if self.na_fala(rx, antes=0.2):
                self.destaque(L[k], cor)
        self.play(FadeOut(L["fonte"]), FadeOut(L["obs"]), run_time=0.4)      # papéis já nomeados: libera a região densa
        self.relayout("alg", 0.8)
        T = (r"\mathbf B(\mathbf r)", r"\frac{\mu_0}{4\pi}", r"\int", r"\mathbf J(\mathbf r')", r"\frac{\mathbf R}{R^3}", r"d\tau'")
        self.show(E(r"\mathbf B(\mathbf r)=\frac{\mu_0}{4\pi}\int\mathbf J(\mathbf r')\times\frac{\mathbf R}{R^3}\,d\tau'", *T, size=M_L, colors=FAM),
                  src={(r"\mathbf B(\mathbf r)", 0): L["B"], (r"\mathbf J(\mathbf r')", 0): L["J"], (r"\frac{\mathbf R}{R^3}", 0): L["R"],
                       (r"d\tau'", 0): L["dt"]}, rt=2.4, wait=1.5)
        self.caption("Biot–Savart soma cada $d\\tau'$ (elemento de volume da fonte), com densidade de corrente $\\mathbf J$ (A/m²)")
        self.show(E(r"\mathbf R=\mathbf r-\mathbf r'\qquad\mathbf F\equiv\frac{\mathbf R}{R^3}", r"\mathbf R", r"\mathbf r", r"\mathbf r'", r"\mathbf F",
                    r"\frac{\mathbf R}{R^3}", size=M_M, colors=FAM), slot="A",
                  src={(r"\mathbf r", 0): L["r"], (r"\mathbf r'", 0): L["rp"]}, rt=2.0, wait=1.0)
        self.caption("Cor separa os papéis: $\\mathbf r$ do observador (ciano), $\\mathbf r'$ da fonte (verde)")
        self.hold(2.0)
        aux = self.slots["A"]["eq"]
        T2 = (r"\mathbf B(\mathbf r)", r"\frac{\mu_0}{4\pi}", r"\int", r"\mathbf J(\mathbf r')", r"\mathbf F", r"d\tau'")
        self.hl(r"\frac{\mathbf R}{R^3}", color=VIOLET)
        self.show(E(r"\mathbf B(\mathbf r)=\frac{\mu_0}{4\pi}\int\mathbf J(\mathbf r')\times\mathbf F\,d\tau'", *T2, size=M_L, colors=FAM),
                  (r"\frac{\mathbf R}{R^3}", None), src={(r"\mathbf F", 0): glyphs(aux, r"\mathbf F", 0)}, rt=1.8, wait=1.2)
        self.mark("n06_biot_savart")
        # aplica ∇· e o operador entra
        self.caption("Tome o divergente dos dois lados")
        T3 = T2 + (r"\nabla\cdot",)
        self.show(E(r"\nabla\cdot\mathbf B(\mathbf r)=\frac{\mu_0}{4\pi}\,\nabla\cdot\!\int\mathbf J(\mathbf r')\times\mathbf F\,d\tau'", *T3, size=M_L, colors=FAM),
                  (None, r"\nabla\cdot"), rt=1.6, wait=1.0)
        self.caption("$\\nabla$ deriva em $\\mathbf r$; a integral percorre $\\mathbf r'$: o operador entra na integral")
        self.show(E(r"\nabla\cdot\mathbf B(\mathbf r)=\frac{\mu_0}{4\pi}\int\nabla\cdot\big(\mathbf J(\mathbf r')\times\mathbf F\big)\,d\tau'", *T3, size=M_L,
                    colors=FAM), rt=2.0, wait=1.5)
        self.mark("n06_nabla_entra")
        # identidade do divergente de um produto vetorial: diagrama recua, matemática ganha espaço
        self.view_to(-5.6, -0.45, 0.72, 1.0)
        I1, I2 = r"\mathbf C\cdot(\nabla\times\mathbf A)", r"\mathbf A\cdot(\nabla\times\mathbf C)"
        self.show(E(r"\nabla\cdot(\mathbf A\times\mathbf C)=\mathbf C\cdot(\nabla\times\mathbf A)-\mathbf A\cdot(\nabla\times\mathbf C)",
                    r"\nabla\cdot(\mathbf A\times\mathbf C)", I1, I2, size=M_L, colors=FAM), slot="A", rt=1.4, wait=0.5)
        idn = rich("identidade vetorial, com $\\mathbf A=\\mathbf J(\\mathbf r')$ e $\\mathbf C=\\mathbf F$", T_NOTE).next_to(self.slots["A"]["card"], DOWN, buff=0.1)
        self.play(FadeIn(idn), run_time=0.5)
        self.caption("O divergente de um produto vetorial se abre em dois termos")
        self.hold(1.5)
        aux = self.slots["A"]["eq"]
        T5 = (r"\mathbf B(\mathbf r)", r"\frac{\mu_0}{4\pi}", r"\int", r"\nabla\cdot", r"\mathbf J(\mathbf r')", r"\mathbf F", r"\nabla\times", r"d\tau'")
        self.show(E(r"\nabla\cdot\mathbf B(\mathbf r)&=\frac{\mu_0}{4\pi}\int\Big[\mathbf F\cdot\big(\nabla\times\mathbf J(\mathbf r')\big)\\&\qquad-\mathbf J(\mathbf r')\cdot\big(\nabla\times\mathbf F\big)\Big]d\tau'",
                    *T5, size=M_L, colors=FAM),
                  (r"\mathbf J(\mathbf r')", None), (r"\mathbf F", None), (r"\nabla\cdot", None, 1),
                  src={((r"\mathbf F", 0), (r"\nabla\times", 0), (r"\mathbf J(\mathbf r')", 0)): glyphs(aux, I1, 0),
                       ((r"\mathbf J(\mathbf r')", 1), (r"\nabla\times", 1), (r"\mathbf F", 1)): glyphs(aux, I2, 0)}, rt=2.6, wait=0.5, structure=False)
        # correspondência termo a termo antes de eliminar qualquer um
        eqH = self.slots["H"]["eq"]
        pairs_ = [(glyphs(aux, I1, 0), VGroup(glyphs(eqH, r"\mathbf F", 0), glyphs(eqH, r"\nabla\times", 0), glyphs(eqH, r"\mathbf J(\mathbf r')", 0)), WHITE),
                  (glyphs(aux, I2, 0), VGroup(glyphs(eqH, r"\mathbf J(\mathbf r')", 1), glyphs(eqH, r"\nabla\times", 1), glyphs(eqH, r"\mathbf F", 1)), VIOLET)]
        for a_, b_, col in pairs_:
            bxs = VGroup(box(a_, col, buff=0.08, width=3), box(b_, col, buff=0.08, width=3))
            self.play(Create(bxs), run_time=0.6)
            self.hold(1.0)
            self.out(bxs, rt=0.3)
        self.mark("n06_identidade")
        # 1º termo: J(r') não depende de r
        self.play(FadeOut(idn), run_time=0.3)
        self.hl_many([(r"\mathbf F", 0), (r"\nabla\times", 0), (r"\mathbf J(\mathbf r')", 0)], color=CYAN, rt=1.0)
        self.show(E(r"\nabla\times\mathbf J(\mathbf r')=\mathbf 0", r"\nabla\times", r"\mathbf J(\mathbf r')", r"\mathbf 0", size=M_L, colors=FAM),
                  slot="A", rt=1.4, wait=0.3)
        why = rich("$\\mathbf J(\\mathbf r')$ não depende de $\\mathbf r$", T_NOTE).next_to(self.slots["A"]["card"], DOWN, buff=0.1)
        self.play(FadeIn(why), run_time=0.5)
        self.caption("$\\nabla$ deriva em relação a $\\mathbf r$, e $\\mathbf J(\\mathbf r')$ só depende de $\\mathbf r'$ (não é continuidade)")
        self.hold(2.5)
        T6 = (r"\mathbf B(\mathbf r)", r"\frac{\mu_0}{4\pi}", r"\int", r"\nabla\cdot", r"\mathbf J(\mathbf r')", r"\mathbf F", r"\nabla\times", r"d\tau'")
        self.show(E(r"\nabla\cdot\mathbf B(\mathbf r)=-\frac{\mu_0}{4\pi}\int\mathbf J(\mathbf r')\cdot\big(\nabla\times\mathbf F\big)\,d\tau'", *T6, size=M_L, colors=FAM),
                  (r"\mathbf F", None, 0), (r"\nabla\times", None, 0), (r"\mathbf J(\mathbf r')", None, 0),
                  (r"\mathbf J(\mathbf r')", r"\mathbf J(\mathbf r')", 1, 0), (r"\nabla\times", r"\nabla\times", 1, 0), (r"\mathbf F", r"\mathbf F", 1, 0),
                  rt=2.2, wait=1.0)
        self.play(FadeOut(why), run_time=0.3)
        self.view_to(-4.35, -0.15, 1.05, 1.0)
        self.mark("n06_primeiro_termo_some")
        # 2º termo: F é gradiente
        self.df["J"] = False
        self.df["cell"] = False
        self.df["origin"] = False
        self.df.update(R=False, Bobs=False)                 # F é o protagonista: região de corrente, R, B e observador saem de cena
        self.play(*[FadeOut(L[k]) for k in ("J", "dt", "r", "rp", "B", "R")], self.dimk.animate.set_value(0.0), run_time=0.8)
        sx, sy = self.s_x.get_value(), self.s_y.get_value()
        lev = VGroup(*[self.curve([self.D(sx + r * math.cos(t), sy + r * math.sin(t)) for t in np.linspace(0, TAU, 60)], VIOLET, 1.8, 0.5, z=3)
                       for r in (0.5, 0.95, 1.5, 2.1)])
        farr = VGroup(*[arrow(self.WD(sx + 0.55 * math.cos(t), sy + 0.55 * math.sin(t)), self.WD(sx + (0.55 + 0.42) * math.cos(t), sy + (0.55 + 0.42) * math.sin(t)),
                              VIOLET, 3.5, z=6, tip=0.15) for t in np.linspace(0, TAU, 10, endpoint=False)])
        self.play(LaggedStart(*[Create(c) for c in lev], lag_ratio=0.2), run_time=1.4)
        self.play(LaggedStart(*[Create(a) for a in farr], lag_ratio=0.05), run_time=1.0)
        self.caption("$1/R$ diminui para longe de $\\mathbf r'$; $\\mathbf F$ aponta exatamente para onde ela diminui")
        self.show(E(r"\mathbf F=\frac{\mathbf R}{R^3}=-\nabla\frac{1}{R}", r"\mathbf F", r"\frac{\mathbf R}{R^3}", r"\nabla", r"\frac{1}{R}", size=M_L, colors=FAM),
                  slot="A", rt=1.6, wait=1.5)
        self.caption("$\\mathbf F$ é um gradiente; e o rotacional de um gradiente é sempre zero")
        self.show(E(r"\nabla\times\mathbf F=-\nabla\times\nabla\frac{1}{R}=\mathbf 0", r"\nabla\times", r"\mathbf F", r"\nabla", r"\frac{1}{R}", r"\mathbf 0",
                    size=M_L, colors=FAM), (r"\frac{\mathbf R}{R^3}", None), slot="A", rt=2.0, wait=1.5)
        aux = self.slots["A"]["eq"]
        self.hl_many([(r"\nabla\times", 0), (r"\mathbf F", 0)], color=CYAN, rt=0.8)
        self.show(E(r"\nabla\cdot\mathbf B(\mathbf r)=-\frac{\mu_0}{4\pi}\int\mathbf J(\mathbf r')\cdot\mathbf 0\,d\tau'", r"\mathbf B(\mathbf r)", r"\frac{\mu_0}{4\pi}",
                    r"\int", r"\nabla\cdot", r"\mathbf J(\mathbf r')", r"\mathbf 0", r"d\tau'", size=M_L, colors=FAM),
                  (r"\nabla\times", None), (r"\mathbf F", None), src={(r"\mathbf 0", 0): glyphs(aux, r"\mathbf 0", 0)}, rt=2.0, wait=1.2)
        self.drop("A", keep_card=False)
        self.show(E(r"\nabla\cdot\mathbf B=0", r"\nabla\cdot\mathbf B", "0", size=M_XL), rt=1.8, wait=0.3)
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.5)
        self.caption("Da própria lei de Biot–Savart: $\\nabla\\cdot\\mathbf B=0$")
        self.mark("n06_div_B_zero")
        self.hold(3.0)
        self.out(bx, lev, farr, rt=0.6)
        self.drop("H", keep_card=False)

    # ── continuidade em duas escalas (N07 e N10) ────────────────────────────────────────────────────────────
    def cont_celula(self, intro, on_zoom, extra=()):
        """Escala global: linhas de corrente de J (estacionárias; só os traçadores de carga andam, sempre sobre elas).
        Escala local: uma célula pequena, em que J é quase uniforme, ampliada por zoom de câmera, com normais, entrada e saída.
        on_zoom() roda com a célula ampliada e devolve objetos (ou None) que saem junto com ela."""
        L = self.dL
        ellp = lambda k, th: BLOB_C + k * np.array([BLOB_A * math.cos(th), BLOB_B * math.sin(th)])
        TH0, KC, cc = 1.0, 0.65, 0.11
        P0 = ellp(KC, TH0)
        jd = J_at(*P0)
        jd = jd / np.linalg.norm(jd)
        nr = np.array([-jd[1], jd[0]])
        v0 = (self.ox.get_value(), self.oy.get_value(), self.gs.get_value())
        saved = {k: self.df.get(k, True) for k in ("origin", "R", "cell", "J", "pts")}
        gl = []
        labs = ("r", "rp", "R", "J") if intro else ("r", "rp", "R")
        self.df.update(origin=False, R=False, cell=False, J=False, pts=False)      # protagonista: so a continuidade
        self.play(*[FadeOut(L[k]) for k in labs], *[FadeOut(m) for m in extra], run_time=0.6)
        if intro:
            gl = [self.flow([lambda u, k=k: self.WD(*ellp(k, TAU * u)) for k in (0.35, 0.65, 0.92)], count=5, color=GREEN, dash=0.22, width=6)]
            self.add(*gl)
            lab = rich("linhas de corrente de $\\mathbf J$ (A/m²)", T_NOTE, GREEN).move_to([-4.1, -2.2, 0])
            self.play(FadeIn(lab), run_time=0.5)
            self.caption("$\\mathbf J$ é estacionário: as cargas percorrem as linhas de corrente e o campo não muda")
            self.hold(2.5)
            gl.append(lab)
        small = self.poly([self.D(*(P0 + sa * cc * jd + sb * cc * nr)) for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))], WHITE, 0.15, z=7).set_stroke(WHITE, 3)
        tag = txt("célula pequena", T_NOTE, WHITE).move_to(self.WD(*(P0 + np.array([0.0, 0.0]))) + np.array([1.25, 0.65, 0]))
        self.play(FadeIn(small), FadeIn(tag), run_time=0.6)
        self.caption("Escolha uma célula tão pequena que $\\mathbf J$ seja quase uniforme nela, e amplie")
        self.hold(1.2)
        S, T = 6.0, (-3.6, -0.35)
        self.play(*[FadeOut(m) for m in gl], FadeOut(tag), FadeOut(small), run_time=0.4)
        self.purge(small, tag)
        for m in gl:
            if hasattr(m, "get_family"):
                self.purge(m)
        self.play(self.ox.animate.set_value(T[0] - S * P0[0]), self.oy.animate.set_value(T[1] - S * P0[1]), self.gs.animate.set_value(S), self.dimk.animate.set_value(0.0), run_time=2.4)
        # linhas de corrente locais (elipses vizinhas: todas são linhas de J), traçadores sobre elas, J, normais, entrada/saída
        win = np.linspace(TH0 - 0.42, TH0 + 0.42, 30)
        loc = VGroup()
        for k in (0.60, KC, 0.70):
            loc.add(self.curve([self.D(*ellp(k, t)) for t in win], GREEN, 2.4, 0.75, z=3))
        # ponta de seta no sentido da corrente (sobre a linha central)
        pe = ellp(KC, TH0 + 0.36)
        loc.add(self.arrowhead(self.WD(*pe), np.array([jd[0], jd[1], 0.0]), 0.3, GREEN, z=4))
        tr = self.flow([lambda u, k=k: self.WD(*ellp(k, TH0 + (u - 0.5) * 0.84)) for k in (0.60, KC, 0.70)], count=3, color=GREEN, dash=0.22, width=6)
        corners = [P0 + sa * cc * jd + sb * cc * nr for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        cell = self.poly([self.D(*p) for p in corners], WHITE, 0.10, z=7).set_stroke(WHITE, 4)
        jar = VGroup(*[arrow(self.WD(*(P0 + o * nr - 0.085 * jd)), self.WD(*(P0 + o * nr + 0.085 * jd)), GREEN, 7, z=9, tip=0.24) for o in (-0.06, 0.0, 0.06)])
        faces = [(-cc * jd, -jd), (cc * jd, jd), (cc * nr, nr), (-cc * nr, -nr)]
        nvec = VGroup(*[arrow(self.WD(*(P0 + f)), self.WD(*(P0 + f + 0.06 * n)), WHITE, 5, z=9, tip=0.2) for f, n in faces])
        nlab = rich("$\\hat{\\mathbf n}$ para fora", T_NOTE, WHITE).move_to(self.WD(*P0) + np.array([1.9, 0.75, 0]))
        lin = rich("entra: fluxo $-\\Phi_J$", T_NOTE, GREEN).move_to(self.WD(*(P0 - cc * jd)) + np.array([-0.4, -1.2, 0]))
        lout = rich("sai: fluxo $+\\Phi_J$", T_NOTE, GREEN).move_to(self.WD(*(P0 + cc * jd)) + np.array([0.5, 1.2, 0]))
        self.play(Create(loc), FadeIn(cell), run_time=1.0)
        self.add(tr)
        self.play(Create(jar), run_time=0.8)
        self.caption("Aqui $\\mathbf J$ é quase uniforme, e as cargas se movem sobre as linhas de corrente")
        self.hold(1.2)
        self.play(Create(nvec), FadeIn(nlab), run_time=0.9)
        self.caption("Normais para fora em cada face: a corrente entra por uma face e sai pela oposta")
        self.play(FadeIn(lin), FadeIn(lout), run_time=0.8)
        self.hold(1.5)
        self.caption("O que entra é igual ao que sai: nenhuma carga se acumula na célula")
        extra_obj = on_zoom()
        tr.clear_updaters()
        outs = [loc, cell, jar, nvec, nlab, lin, lout, tr] +([extra_obj] if extra_obj is not None else [])
        self.out(*outs, rt=0.6)
        self.df.update(saved)
        anims = [self.ox.animate.set_value(v0[0]), self.oy.animate.set_value(v0[1]), self.gs.animate.set_value(v0[2]), self.dimk.animate.set_value(1.0)]
        anims += [FadeIn(L[k]) for k in labs]
        self.play(*anims, run_time=1.4)
        return extra_obj

    # ── N07 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def dois_nablas(self):
        self.section("dois_nablas", "Dois pontos, dois operadores")
        L = self.dL
        self.relayout("split", 0.6)
        self.view_to(-3.9, -0.35, 1.15, 1.2)
        self.df.update(origin=True, cell=True, J=True, Bobs=False, R=True)
        self.play(*[FadeIn(L[k]) for k in ("J", "r", "rp", "R")], self.dimk.animate.set_value(1.0), run_time=0.8)
        self.caption("$\\nabla$ deriva movendo o observador $\\mathbf r$, com a fonte parada")
        self.show(E(r"\nabla\ \longleftrightarrow\ \mathbf r", r"\nabla", r"\mathbf r", size=M_XL, colors=FAM), rt=1.2, wait=0.5)
        self.play(self.r_x.animate.set_value(2.3), self.r_y.animate.set_value(0.4), run_time=2.4)
        self.play(self.r_x.animate.set_value(1.2), self.r_y.animate.set_value(1.7), run_time=2.4)
        self.pulse(L["J"], GREEN)
        self.caption("$\\mathbf R$ e $\\mathbf F$ mudam; $\\mathbf J(\\mathbf r')$ não muda")
        self.show(E(r"\nabla\,\mathbf J(\mathbf r')=0", r"\nabla", r"\mathbf J(\mathbf r')", size=M_XL, colors=FAM), (r"\nabla", r"\nabla"),
                  src={(r"\mathbf J(\mathbf r')", 0): L["J"]}, rt=1.6, wait=0.3)
        t1 =txt("variáveis independentes", T_NOTE, CYAN).next_to(self.slots["H"]["card"], DOWN, buff=0.1)
        self.play(FadeIn(t1), run_time=0.5)
        self.mark("n07_nabla_observador")
        self.hold(2.0)
        self.caption("$\\nabla'$ deriva movendo a fonte $\\mathbf r'$: aí $\\mathbf J$ muda de um ponto a outro")
        self.show(E(r"\nabla'\ \longleftrightarrow\ \mathbf r'", r"\nabla'", r"\mathbf r'", size=M_XL, colors=FAM), slot="A", rt=1.2, wait=0.3)
        self.play(self.s_x.animate.set_value(0.6), self.s_y.animate.set_value(-0.75), run_time=2.6)
        self.play(self.s_x.animate.set_value(-0.9), self.s_y.animate.set_value(0.35), run_time=2.6)
        # continuidade: linhas de corrente (global) → célula pequena → zoom → ∇'·J = 0
        self.hold(0.6)

        def eq_cont():
            self.show(E(r"\nabla'\cdot\mathbf J=0", r"\nabla'\cdot", r"\mathbf J", size=M_XL, colors=FAM), (r"\nabla'", r"\nabla'\cdot"), slot="A", rt=1.6, wait=0.3)
            t2 = txt("continuidade + magnetostática", T_NOTE, GREEN).next_to(self.slots["A"]["card"], DOWN, buff=0.1)
            self.play(FadeIn(t2), run_time=0.5)
            self.caption("São afirmações diferentes: a de cima é sobre variáveis; a de baixo é física")
            self.mark("n07_dois_nablas")
            self.hold(3.0)
            return t2
        t2 = self.cont_celula(True, eq_cont, extra=[t1])
        self.play(self.r_x.animate.set_value(1.75), self.r_y.animate.set_value(1.3), self.s_x.animate.set_value(-0.75), self.s_y.animate.set_value(-0.35),
                  run_time=1.4)
        self.drop("A", keep_card=False)
        self.drop("H", keep_card=False)
