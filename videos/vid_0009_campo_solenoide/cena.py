"""Campo magnético dentro de um solenoide: B = mu0 n I; preview silencioso.

DA EQUAÇÃO AO FENÔMENO · EP. 03. Continua o episódio da espira (videos/vid_0008_campo_espira/cena.py):
começa da expressão já derivada lá e não rederiva Biot-Savart.

  B1  retomada: B_z(z) = mu0 I R^2 / 2(R^2+z^2)^{3/2}, deslocada para B_j(z)
  B2  superposição REAL (b_sum): 1 -> 2 -> 4 -> 8 espiras, 1,00 -> 1,83 -> 2,85 ->
      3,58 na escala B/B_1(0). Cada espira acende e manda sua parcela para a barra;
      a resultante é a soma. I e o passo ficam FIXOS e o comprimento cresce — este
      não é o teste de n com L fixo (esse vem em B16).
  B3  bobina finita real: retornos externos qualitativos e B(z) axial quantitativo,
      no mesmo x da bobina; nas pontas, cerca de metade do valor central (54%).
  B4  idealização consciente: finita -> longa -> pontas saem do quadro ->
      distribuição CONTÍNUA e uniforme (as espiras discretas se fundem).
  B5  simetria do modelo ideal: translação ao longo de z, ausência de direção
      azimutal privilegiada e pares de FATIAS do enrolamento simétricas em torno do
      plano transversal de P (esquema, sem escala; db_dirs e b_loop não são usados
      fora do eixo). Conclui B = B(s) z^, SÓ no modelo ideal.
  B6-B9  Ampère num quadro cumulativo: a lei fica ancorada, as conclusões vão para
      uma prateleira e o MESMO retângulo desliza fora -> dentro -> atravessando.
        fora:  cada lado é iluminado e leva sua parcela a
               B(s1) l + 0 - B(s2) l + 0 = 0; tirando os zeros e dividindo por l > 0,
               B_fora = constante. Só então, em OUTRA etapa, a condição física
               (campo do solenoide, sem campo uniforme externo) B -> 0 com s -> inf;
               as duas juntas dão B_fora = 0.
        dentro: I_enc = 0 => B_dentro = constante.
  B10-B13 atravessando: o contorno (esquerda) dá B l e a corrente envolvida
      (direita) conta as SEIS seções de UMA fileira, N_l = n l e I_enc = n l I.
      As duas metades entram na lei ancorada, os dois l ganham a mesma cor e
      dividir por l dá B = mu0 n I.
  B15 desfaz a idealização: pontas e retornos voltam e "=" vira "~=" com a nota
      "região central · solenoide longo" na MESMA transição.
  B16 testes: I sobe (B proporcional a I); depois L e I fixos e N dobra (n = N/L).
  B17 coda do atuador; B18 fechamento.

Unidades internas: R = 1; b = B / (mu0 I / 2R); passo PITCH = 0,5 R => n = 2/R e o
valor ideal é b = 2 R n = 4. l = 3 R => N_l = n l = 6 seções.
"""

import numpy as np
from manim import (
    DOWN, LEFT, ORIGIN, PI, RIGHT, UP, Circle, Create, DashedLine, Dot, FadeIn, FadeOut,
    ImageMobject, Indicate, Line, Rectangle, RoundedRectangle, SurroundingRectangle,
    Transform, TransformFromCopy, TransformMatchingTex, VGroup, VMobject, ValueTracker,
    always_redraw, linear,
)

from comum import (
    BEAT, BLUE, B_IDEAL, CUT_EXTRA, CUT_Z, CYAN, CYAN_L, ENC_Z, L_ELL, MAGENTA, PITCH,
    READ, READ_RES, VIOLET, WHITE, Z_FIN, CenaBase, b_cut, b_loop, b_sum, boxed, fit,
    mtex, odot, otimes, plate, soft_swap, span_mark, tag, tex, text, turn_centers, vec,
)
from template.config import WATERMARK_PATH

# ── Geometria de tela: bobina, barra e gráfico ──────────────────────────────
RS = 1.25                 # unidades de tela por R
AX_Y = 1.25               # altura do eixo do solenoide
TILT0 = 0.34              # achatamento da profundidade na projeção oblíqua
LB = 2.30                 # barra/resultante quando b = B_IDEAL
BAR_Y, BAR_X0 = -0.62, 0.0
GY0, GH = -2.60, 1.35     # curva B(z) da bobina finita
X_VIS = 5.2               # só desenhamos espiras/seções com |x| < X_VIS
N_INF = 38.0              # bobina longa antes da fusão no modelo contínuo
ARR_IN = 0.55             # seta do campo interno no corte quando b = B_IDEAL

RECT_W, RECT_H = L_ELL * RS, 0.90
Y_OUT, Y_IN, Y_WALL = 3.80, 1.75, 2.60              # centros do retângulo nos três estados

# ── Níveis verticais dos quadros ────────────────────────────────────────────
SUP_OP_Y, SUP_NOTE_Y = -2.95, -4.05      # superposição: expressão ativa e nota
AMP_LAW_Y, AMP_SIDE_Y = -0.88, -1.55     # Ampère: lei ancorada e linha da condição
AMP_OP_Y, SHELF_Y = -2.75, -3.90         # operação ativa e prateleira de resultados
COL_X = 1.78                             # colunas CONTORNO / CORRENTE ENVOLVIDA

# ── Conferências específicas desta cena, no import ──────────────────────────
assert np.isclose(RECT_W / 2 / RS, L_ELL / 2)
assert Y_OUT - RECT_H / 2 - AX_Y > RS                             # estado 1: os dois lados fora
assert AX_Y + RS - (Y_IN + RECT_H / 2) > 0.2                      # estado 2: os dois dentro
assert Y_WALL - RECT_H / 2 < AX_Y + RS < Y_WALL + RECT_H / 2      # estado 3: atravessando
assert np.isclose(b_sum(0.0, 1), 1.0)                             # a barra começa em B_1(0)
_par = [b_sum(0.0, n) for n in (1, 2, 4, 8)]
assert np.allclose(_par, [1.0, 1.82615, 2.85015, 3.58197], atol=5e-5)
assert LB * _par[-1] / B_IDEAL < 2 * 3.5 - BAR_X0                 # a barra cabe na margem


class CampoSolenoide009(CenaBase):
    op_y, note_y, shelf_y = SUP_OP_Y, SUP_NOTE_Y, SHELF_Y

    # ── Bobina pseudo-3D e modelo contínuo ──────────────────────────────────
    def coil_pt(self, zc, phi):
        t = self.tilt.get_value()
        return np.array([RS * (zc + t * np.sin(phi)), AX_Y + RS * np.cos(phi), 0.0])

    def coil(self):
        """Espiras discretas; somem conforme self.cont funde tudo na distribuição contínua."""
        op0 = self.coil_op.get_value() * (1.0 - self.cont.get_value())
        g = VGroup()
        if op0 < 0.01:
            return g
        zs, w = turn_centers(self.nf.get_value())
        foc = self.focus.get_value()
        for near in (False, True):
            phis = np.linspace(0, PI, 25) + (0 if near else PI)
            for j, (zc, wi) in enumerate(zip(zs, w)):
                if abs(RS * zc) >= X_VIS:
                    continue
                hi = 1.0 if foc < 0 else (1.0 if abs(j - foc) < 0.5 else 0.32)
                g.add(VMobject().set_points_as_corners([self.coil_pt(zc, p) for p in phis])
                      .set_stroke(BLUE, 6, op0 * wi * hi * (1.0 if near else 0.38)))
        return g

    def coil_sheet(self):
        """Modelo IDEAL: enrolamento contínuo e uniforme (nenhuma espira individual)."""
        op = self.coil_op.get_value() * self.cont.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        g.add(Rectangle(width=2 * X_VIS, height=2 * RS).set_stroke(width=0)
              .set_fill(BLUE, 0.10 * op).move_to([0, AX_Y, 0]))
        for sgn in (1, -1):
            y = AX_Y + sgn * RS
            g.add(Line([-X_VIS, y, 0], [X_VIS, y, 0]).set_stroke(BLUE, 7, op))
            for x in np.arange(-X_VIS, X_VIS, 0.26):
                g.add(Line([x, y, 0], [x, y - sgn * 0.17, 0]).set_stroke(BLUE, 1.6, 0.55 * op))
        return g

    def current_marks(self):
        """Sentido da corrente: na face da frente (phi = pi/2) ela desce na tela."""
        op = self.cur_op.get_value() * self.coil_op.get_value() * (1 - self.cont.get_value())
        g = VGroup()
        if op < 0.01:
            return g
        zs, w = turn_centers(self.nf.get_value())
        for zc, wi in zip(zs, w):
            if wi < 0.99 or abs(RS * zc) > 2.4:
                continue
            c = self.coil_pt(zc, PI / 2)
            g.add(vec(c + UP * 0.26, c + DOWN * 0.26, CYAN_L, 4).set_opacity(op * 0.95))
        return g

    # ── Superposição: parcelas, barra e resultante ──────────────────────────
    def slot(self, j, nf):
        """(x inicial, comprimento) da parcela da espira j na barra, com nf voltas."""
        zs, w = turn_centers(nf)
        if j >= len(zs):
            return BAR_X0, 0.0
        ls = [LB * float(w[i] * b_loop(0.0, zs[i])) / B_IDEAL for i in range(len(zs))]
        return BAR_X0 + sum(ls[:j]), ls[j]

    def b_len(self, z=0.0):
        return LB * b_sum(z, self.nf.get_value()) / B_IDEAL

    def b_arrow(self):
        """Resultante axial: comprimento = soma real das contribuições das espiras."""
        op, L = self.bres_op.get_value(), self.b_len()
        if op < 0.01 or L < 0.03:
            return VMobject()
        a = np.array([BAR_X0, AX_Y, 0.0])
        return vec(a, a + RIGHT * L, CYAN, 8).set_opacity(op)

    def contrib_bar(self):
        """As parcelas enfileiradas: mesma origem em x e mesmo total da resultante."""
        op = self.bar_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        nf = self.nf.get_value()
        foc = self.focus.get_value()
        zs, _ = turn_centers(nf)
        for j in range(len(zs)):
            x, L = self.slot(j, nf)
            if L < 2e-3:
                continue
            a = 1.0 if foc < 0 else (1.0 if abs(j - foc) < 0.5 else 0.3)
            g.add(Line([x, BAR_Y, 0], [x + L, BAR_Y, 0])
                  .set_stroke(CYAN_L, 15, op * a * (1.0 if j % 2 else 0.78)))
        return g

    def bar_tie(self):
        """Prumo ligando a ponta da barra à ponta da seta: mesmo comprimento."""
        op = self.tie_op.get_value()
        if op < 0.01:
            return VMobject()
        x = BAR_X0 + self.b_len()
        return DashedLine([x, BAR_Y, 0], [x, AX_Y, 0], dash_length=0.09).set_stroke(WHITE, 2, 0.5 * op)

    def focus_link(self):
        """Liga a espira em destaque à sua parcela na barra."""
        foc, op = self.focus.get_value(), self.bar_op.get_value()
        if foc < 0 or op < 0.01:
            return VMobject()
        nf = self.nf.get_value()
        zs, _ = turn_centers(nf)
        j = int(round(foc))
        if j >= len(zs):
            return VMobject()
        x, L = self.slot(j, nf)
        return DashedLine([RS * zs[j], AX_Y - RS, 0], [x + L / 2, BAR_Y + 0.14, 0],
                          dash_length=0.08).set_stroke(CYAN_L, 2.5, 0.8 * op)

    def ext_lines(self):
        """Esboço QUALITATIVO dos retornos externos da bobina finita (não sai da fórmula axial)."""
        op = self.ext_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        half = RS * (self.nf.get_value() - 1) / 2 * PITCH
        th = np.linspace(0, PI, 60)
        for k in (0, 1):
            a, h = half + RS * (0.45 + 0.5 * k), RS * (1.5 + 0.85 * k)
            for sgn in (1, -1):
                g.add(VMobject().set_points_as_corners(
                    [[a * np.cos(t), AX_Y + sgn * h * np.sin(t), 0] for t in th]
                ).set_stroke(WHITE, 2.5, 0.45 * op))
        return g

    def axis_curve(self):
        """B(z) no eixo da bobina finita, da soma real, no MESMO x da bobina."""
        op = self.curve_op.get_value()
        if op < 0.01:
            return VMobject()
        zs = np.linspace(-3.3 / RS, 3.3 / RS, 180)
        pts = [[RS * z, GY0 + GH * b_sum(z, self.nf.get_value()) / B_IDEAL, 0] for z in zs]
        return VMobject().set_points_as_corners(pts).set_stroke(CYAN_L, 5, op)

    # ── Corte longitudinal 2D ───────────────────────────────────────────────
    def cut_rows(self):
        """Fileira de cima saindo, de baixo entrando — marcas esquemáticas da corrente.

        Regra da mão direita: com x^ para a direita, y^ para cima e z^out saindo da tela,
        o fio de cima (y = +R, corrente +z^out) dá no eixo j x r^ ~ z^out x (-y^) = +x^;
        o de baixo (y = -R, corrente -z^out) dá (-z^out) x (+y^) = +x^. Campo interno para
        a DIREITA, coerente com a bobina pseudo-3D e com a derivação do episódio anterior.
        """
        op0, zlim, ex = self.cut_op.get_value(), self.zlim.get_value(), self.extra_op.get_value()
        g = VGroup()
        if op0 < 0.01:
            return g
        for zs, amp in ((CUT_Z, 1.0), (CUT_EXTRA, ex)):
            if amp < 0.01:
                continue
            for z in zs:
                x = RS * z
                if abs(x) > X_VIS:
                    continue
                op = op0 * amp * float(np.clip((zlim - abs(z)) / 0.5, 0.0, 1.0))
                if op < 0.01:
                    continue
                g.add(odot([x, AX_Y + RS, 0], CYAN_L, op), otimes([x, AX_Y - RS, 0], CYAN_L, op))
        return g

    def cut_walls(self):
        """Paredes do enrolamento no corte; pontas aparecem quando a bobina é finita."""
        op = self.cut_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        zlim = self.zlim.get_value()
        half = min(RS * zlim, X_VIS)
        for sgn in (1, -1):
            y = AX_Y + sgn * RS
            g.add(Line([-half, y, 0], [half, y, 0]).set_stroke(BLUE, 3, 0.45 * op))
        if zlim < 6.0:
            for s in (-1, 1):
                g.add(Line([s * half, AX_Y - RS, 0], [s * half, AX_Y + RS, 0])
                      .set_stroke(BLUE, 3, 0.55 * op))
        return g

    def cut_b(self, z):
        """Magnitude interna: no ideal CONTÍNUO vale exatamente mu0 n I; na finita, a soma real."""
        c = self.cont.get_value()
        ideal = B_IDEAL * (1.0 + self.extra_op.get_value())
        finite = b_cut(z, self.zlim.get_value(), self.extra_op.get_value())
        return (c * ideal + (1.0 - c) * finite) * self.cur.get_value()

    def cut_field(self):
        """Setas do campo interno."""
        op = self.bin_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        for z in np.arange(-3, 4) * 1.0:
            x = RS * z
            if abs(x) > 3.9:
                continue
            L = ARR_IN * self.cut_b(z) / B_IDEAL
            if L < 0.12:
                continue
            for dy in (-0.62, 0.0, 0.62):
                a = np.array([x - L / 2, AX_Y + dy, 0.0])
                g.add(vec(a, a + RIGHT * L, WHITE, 5).set_opacity(op))
        return g

    def cut_ext(self):
        """Retornos externos da bobina real no corte (esboço qualitativo)."""
        op = self.cutext_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        half = RS * self.zlim.get_value()
        for k in (0, 1):
            h = RS * (1.5 + 0.8 * k)
            a, b = np.array([half, AX_Y, 0.0]), np.array([-half, AX_Y, 0.0])
            for s in (1, -1):
                g.add(VMobject().set_points_smoothly([
                    a, [half * 0.9, AX_Y + s * h * 0.7, 0], [0.0, AX_Y + s * h, 0],
                    [-half * 0.9, AX_Y + s * h * 0.7, 0], b]).set_stroke(WHITE, 2.5, 0.4 * op))
        return g

    # ── Retângulo amperiano (um só, deslizante) ─────────────────────────────
    def amp_rect(self):
        """Quatro lados separados: o trecho em análise fica forte, os outros recuam."""
        op = self.amp_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        y, w2, h2 = self.amp_y.get_value(), RECT_W / 2, RECT_H / 2
        for a, yy in ((self.act1.get_value(), y - h2), (self.act2.get_value(), y + h2)):
            g.add(Line([-w2, yy, 0], [w2, yy, 0]).set_stroke(VIOLET, 3.5 + 3 * a, op * (0.55 + 0.45 * a)))
        for a, s in ((self.actL.get_value(), -1), (self.actR.get_value(), 1)):
            g.add(Line([s * w2, y - h2, 0], [s * w2, y + h2, 0])
                  .set_stroke(VIOLET, 3.5 + 3 * a, op * (0.55 + 0.45 * a)))
        return g

    def amp_dirs(self):
        """Sentido do percurso (dl): lado de baixo em +x, lado de cima em -x."""
        op = self.amp_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        y = self.amp_y.get_value()
        g.add(vec([-1.75, y - RECT_H / 2, 0], [-1.0, y - RECT_H / 2, 0], VIOLET, 4).set_opacity(op))
        g.add(vec([-1.0, y + RECT_H / 2, 0], [-1.75, y + RECT_H / 2, 0], VIOLET, 4).set_opacity(op))
        g.add(plate(tex(r"d\vec\ell", 30, VIOLET).set_opacity(op))
              .move_to([-1.375, y - RECT_H / 2 + 0.30, 0]))
        return g

    def amp_sides(self):
        """Rótulos s1 (lado de baixo, mais perto) e s2 (lado de cima)."""
        op = self.side_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        y = self.amp_y.get_value()
        for lab, dy in ((r"s_1", -RECT_H / 2), (r"s_2", RECT_H / 2)):
            g.add(plate(tex(lab, 40, VIOLET).set_opacity(op)).move_to([-RECT_W / 2 - 0.48, y + dy, 0]))
        return g

    def ell_mark(self):
        """Cota do comprimento l, presa ao lado de baixo do retângulo."""
        op = self.ell_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        y = self.amp_y.get_value() - RECT_H / 2 - 0.30
        g.add(span_mark(np.array([-RECT_W / 2, y, 0]), np.array([RECT_W / 2, y, 0]), VIOLET, op=op))
        g.add(plate(tex(r"\ell", 38, VIOLET).set_opacity(op)).move_to([0, y - 0.03, 0]))
        return g

    def out_field(self):
        """Campo externo AINDA DESCONHECIDO sobre os dois lados longos."""
        op = self.bout_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        y, sh = self.amp_y.get_value(), self.probe.get_value()
        for dy in (-RECT_H / 2, RECT_H / 2):
            for x in (0.45, 1.25):
                L = 0.55 * max(0.12, 1.0 - 0.8 * sh)
                g.add(vec([x, y + dy, 0], [x + L, y + dy, 0], WHITE, 4).set_opacity(op * 0.85))
        return g

    def enc_marks(self):
        """Seções enlaçadas, marcadas em sequência: uma única fileira, N_l = n l."""
        k = self.enc_n.get_value()
        g = VGroup()
        if k < 0.01:
            return g
        for i, z in enumerate(ENC_Z):
            op = float(np.clip(k - i, 0.0, 1.0))
            if op < 0.01:
                continue
            g.add(Circle(0.235, color=MAGENTA, stroke_width=3.5).set_stroke(opacity=op)
                  .move_to([RS * z, AX_Y + RS, 0]))
        return g

    # ── Cena ────────────────────────────────────────────────────────────────
    def construct(self):
        self.start_frame()
        watermark = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(watermark.to_corner(UP + RIGHT, buff=0.28))
        series = text("DA EQUAÇÃO AO FENÔMENO · EP. 03", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4)

        self.nf, self.tilt, self.cont = ValueTracker(1.0), ValueTracker(TILT0), ValueTracker(0)
        self.coil_op, self.cur_op, self.bres_op, self.bar_op = (ValueTracker(0) for _ in range(4))
        self.focus = ValueTracker(-1)
        self.tie_op, self.ext_op, self.curve_op = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.cut_op, self.zlim, self.extra_op = ValueTracker(0), ValueTracker(9.25), ValueTracker(0)
        self.bin_op, self.cur, self.cutext_op = ValueTracker(0), ValueTracker(1), ValueTracker(0)
        self.amp_op, self.amp_y, self.side_op = ValueTracker(0), ValueTracker(Y_OUT), ValueTracker(0)
        self.act1, self.act2, self.actL, self.actR = (ValueTracker(0) for _ in range(4))
        self.ell_op, self.bout_op, self.enc_n = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.probe = ValueTracker(0)
        self.add(self.nf, self.cur, self.focus, self.enc_n, self.probe)

        sheet = always_redraw(self.coil_sheet)
        coil = always_redraw(self.coil)
        marks = always_redraw(self.current_marks)
        bres = always_redraw(self.b_arrow)
        bar = always_redraw(self.contrib_bar)
        tie = always_redraw(self.bar_tie)
        flink = always_redraw(self.focus_link)
        extl = always_redraw(self.ext_lines)
        curve = always_redraw(self.axis_curve)
        rows = always_redraw(self.cut_rows)
        walls = always_redraw(self.cut_walls)
        cfield = always_redraw(self.cut_field)
        cext = always_redraw(self.cut_ext)
        rect = always_redraw(self.amp_rect)
        dirs = always_redraw(self.amp_dirs)
        sides = always_redraw(self.amp_sides)
        ell = always_redraw(self.ell_mark)
        ofield = always_redraw(self.out_field)
        enc = always_redraw(self.enc_marks)
        self.add(extl, sheet, coil, marks, rows, walls, cext, cfield, bres, bar, tie, flink,
                 curve, ofield, rect, dirs, sides, ell, enc)
        self.bleed = [series, coil, sheet, marks, extl, rows, walls, cext, cfield, curve, enc]
        self.add(series)

        # ══ B1. Retomada: a contribuição de UMA espira (0–6 s) ═════════════════════════════════════════
        self.play(FadeIn(series), *self.caption("COMO ENROLAR UM FIO",
                                                "REFORÇA O CAMPO", "DENTRO DA BOBINA?"),
                  self.coil_op.animate.set_value(1), self.cur_op.animate.set_value(1),
                  run_time=0.80)
        eqz = mtex(r"B_z(z)", "=", r"\frac{\mu_0 I R^2}{2\left(R^2+z^2\right)^{3/2}}", size=42)
        self.show_expr(eqz, run_time=0.60, match=False)
        self.note(tag("esta é a contribuição de uma espira", 24, 0.9))
        self.check_safe()
        self.wait(READ)
        eqj = mtex(r"B_j(z)", "=", r"\frac{\mu_0 I R^2}{2\left[R^2+(z-z_j)^2\right]^{3/2}}", size=38)
        self.show_expr(eqj, run_time=0.73)
        self.play(Indicate(eqj[2], color=MAGENTA, scale_factor=1.08), run_time=0.60)
        self.note(tag("a mesma fórmula, deslocada de z_j para cada espira", 21, 0.9))
        self.check_safe()
        self.wait(BEAT)

        # ══ B2. Superposição: cada espira manda a sua parcela (6–19 s) ═════════════════════════════════
        self.play(*self.caption("AS PARCELAS SE SOMAM"), run_time=0.53)
        eqN = mtex("B(z)", "=", r"\sum_j B_j(z)", size=50)
        fit(eqN).move_to([0, self.op_y, 0])
        nbox = SurroundingRectangle(eqN, color=WHITE, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.play(soft_swap(self.expr, VGroup(eqN, nbox)), run_time=0.73)
        self.expr = VGroup(eqN, nbox)
        scale_lab = tex(r"B/B_1(0)", 26).move_to([BAR_X0 + 1.05, BAR_Y - 0.44, 0]).set_opacity(0.7)
        val = tex("1{,}00", 30).move_to([BAR_X0 + 2.75, BAR_Y, 0])
        self.play(self.focus.animate.set_value(0), self.bar_op.animate.set_value(1),
                  FadeIn(scale_lab), FadeIn(val), run_time=0.60)
        self.note(tag("a primeira espira acende e deixa a sua parcela", 22, 0.9))
        self.check_safe()
        self.wait(BEAT)
        self.play(self.bres_op.animate.set_value(1), self.tie_op.animate.set_value(1), run_time=0.60)
        self.wait(BEAT)

        # a segunda espira: a parcela viaja da espira até a barra
        self.play(self.focus.animate.set_value(-1), run_time=0.44)
        x2, L2 = self.slot(1, 2.0)
        flyer = Line([0, 0, 0], [L2, 0, 0]).set_stroke(CYAN_L, 15, 0.95)
        flyer.move_to([RS * PITCH / 2, AX_Y - RS - 0.35, 0])
        self.play(self.nf.animate.set_value(2.0), run_time=0.80, rate_func=linear)
        new_val = tex("1{,}83", 30).move_to([BAR_X0 + 2.75, BAR_Y, 0])
        self.play(FadeIn(flyer), run_time=0.44)
        self.play(flyer.animate.move_to([x2 + L2 / 2, BAR_Y, 0]), soft_swap(val, new_val),
                  run_time=0.73)
        self.remove(flyer)
        val = new_val
        self.note(tag("a segunda entra na fila e a resultante cresce", 22, 0.9))
        self.check_safe()
        self.wait(BEAT)

        self.note(tag("mesma corrente e mesmo passo: a bobina fica mais longa", 21, 0.9))
        for n, v in ((4.0, "2{,}85"), (8.0, "3{,}58")):
            self.play(self.nf.animate.set_value(n), run_time=0.73, rate_func=linear)
            new_val = tex(v, 30).move_to([BAR_X0 + 2.75, BAR_Y, 0])
            self.play(soft_swap(val, new_val), run_time=0.53)
            val = new_val
            self.wait(BEAT)
        for j in (0, 7):
            self.play(self.focus.animate.set_value(j), run_time=0.47)
            self.wait(0.44)
        self.play(self.focus.animate.set_value(-1), run_time=0.47)
        self.note(tag("cada espira contribui menos quanto mais longe de P", 21, 0.9))
        self.check_safe()
        self.wait(BEAT)

        # ══ B3. A bobina real tem pontas (19–28 s) ═════════════════════════════════════════════════════
        self.play(*self.caption("MAS A BOBINA REAL TEM PONTAS"),
                  FadeOut(VGroup(scale_lab, val)), self.bar_op.animate.set_value(0),
                  self.tie_op.animate.set_value(0), self.bres_op.animate.set_value(0),
                  self.cur_op.animate.set_value(0), FadeOut(self.expr), run_time=0.60)
        self.expr = None
        self.play(self.ext_op.animate.set_value(1), run_time=0.73)
        self.note(tag("o campo vaza e volta por fora (esboço qualitativo)", 21, 0.85))
        self.check_safe()
        self.wait(BEAT)
        gz = tex("z", 30, BLUE).move_to([3.15, GY0 - 0.32, 0]).set_opacity(0.75)
        gb = tex("B", 30).move_to([-3.15, GY0 + GH + 0.26, 0]).set_opacity(0.7)
        gax = Line([-3.3, GY0, 0], [3.3, GY0, 0]).set_stroke(WHITE, 2, 0.35)
        band = VGroup(Rectangle(width=2.5, height=GH).set_stroke(width=0).set_fill(VIOLET, 0.22),
                      text("REGIÃO CENTRAL", 17, VIOLET, 0.95).move_to([0, GY0 + GH + 0.24, 0]))
        band[0].move_to([0, GY0 + GH / 2, 0])
        self.play(FadeIn(gax, gz, gb), self.curve_op.animate.set_value(1),
                  self.ext_op.animate.set_value(0), run_time=0.73)
        self.note(tag("o mesmo eixo, agora com o valor do campo", 22, 0.9))
        self.wait(BEAT)
        ends = VGroup(*(DashedLine([s * RS * 2.0, AX_Y - RS, 0], [s * RS * 2.0, GY0, 0],
                                   dash_length=0.09).set_stroke(MAGENTA, 2.5, 0.75) for s in (-1, 1)))
        self.play(Create(ends), FadeIn(band), run_time=0.60)
        self.note(tag("quase plano no meio; nas pontas, cerca de metade", 21, 0.9))
        self.check_safe()
        self.wait(READ_RES)

        # ══ B4. Por que idealizar (28–38 s) ════════════════════════════════════════════════════════════
        self.play(*self.caption("POR QUE IDEALIZAR"),
                  FadeOut(VGroup(gax, gz, gb, ends, band)),
                  self.curve_op.animate.set_value(0), run_time=0.60)
        self.note(tag("primeiro, uma bobina mais longa", 23, 0.85))
        self.play(self.nf.animate.set_value(18.0), run_time=0.93, rate_func=linear)
        self.wait(BEAT)
        self.note(tag("mais longa ainda: as pontas saem do quadro", 22, 0.85))
        self.play(self.nf.animate.set_value(N_INF), run_time=1.30, rate_func=linear)
        self.wait(BEAT)
        self.play(self.cont.animate.set_value(1.0), run_time=1.30)
        ideal = tag("MODELO IDEAL · ENROLAMENTO CONTÍNUO E UNIFORME", 21, 0.9, VIOLET)
        ideal.move_to([0, 4.85, 0])
        self.play(FadeIn(ideal), run_time=0.53)
        self.note(tag("sem pontas, a simetria fica muito mais forte", 22, 0.9))
        self.check_safe()
        self.wait(READ)

        # ══ B5. O que a simetria exige (38–51 s) ═══════════════════════════════════════════════════════
        self.play(*self.caption("O QUE A SIMETRIA EXIGE"), run_time=0.53)
        ps = np.array([0.0, AX_Y + 0.62, 0.0])
        pdot = Dot(ps, 0.09, color=WHITE)
        s_mark = span_mark(np.array([0.0, AX_Y, 0.0]), ps, MAGENTA, 0.08, 2.2, 0.85)
        s_lab = tex("s", 30, MAGENTA).next_to(s_mark, LEFT, 0.12)
        obs = VGroup(pdot, s_mark, s_lab)
        self.play(FadeIn(pdot), Create(s_mark), FadeIn(s_lab), run_time=0.53)
        # 1) pares de fatias simétricas em torno do plano transversal de P
        plane = DashedLine([0, AX_Y - RS - 0.45, 0], [0, AX_Y + RS + 0.45, 0],
                           dash_length=0.1).set_stroke(WHITE, 2, 0.5)
        sl = VGroup(*(Rectangle(width=0.30, height=2 * RS).set_stroke(width=0).set_fill(CYAN_L, 0.35)
                      .move_to([sg * 1.35, AX_Y, 0]) for sg in (-1, 1)))
        beta = 0.48
        f1 = vec(ps, ps + 1.05 * np.array([np.cos(beta), np.sin(beta), 0]), CYAN_L, 5)
        f2 = vec(ps, ps + 1.05 * np.array([np.cos(-beta), np.sin(-beta), 0]), CYAN_L, 5)
        f_lab = tag("contribuições das fatias · esquema, sem escala", 17, 0.9, CYAN_L)
        f_lab.move_to([0, AX_Y + 2.05, 0])
        self.play(Create(plane), FadeIn(sl), FadeIn(f_lab), run_time=0.60)
        self.play(Create(f1), Create(f2), run_time=0.60)
        self.note(tag("duas fatias simétricas em torno do plano de P", 22, 0.9))
        self.check_safe()
        self.wait(BEAT)
        fax = vec(ps, ps + RIGHT * (2 * 1.05 * np.cos(beta)), WHITE, 7)
        self.play(FadeOut(VGroup(f1, f2)), Create(fax), run_time=0.60)
        self.note(tag("as transversais se cancelam; sobra a axial", 22, 0.9))
        self.wait(BEAT)
        # 2) translação ao longo de z: a vizinhança do ponto é sempre a mesma
        self.play(VGroup(obs, fax).animate.shift(RIGHT * 2.1), run_time=0.73)
        self.play(VGroup(obs, fax).animate.shift(LEFT * 4.2), run_time=1.16)
        
        self.note(tag("nenhuma posição ao longo do eixo é especial", 22, 0.9))
        self.check_safe()
        self.wait(BEAT)
        sym = mtex(r"\vec B", "=", "B(s)", r"\,\hat z", size=50)
        fit(sym).move_to([0, self.op_y, 0])
        sbox = SurroundingRectangle(sym, color=WHITE, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.play(FadeIn(VGroup(sym, sbox), shift=UP * 0.1),
                  FadeOut(VGroup(obs, fax, plane, sl, f_lab)), run_time=0.67)
        self.expr = VGroup(sym, sbox)
        self.note(tag("só no modelo ideal infinito", 24, 0.95))
        self.check_safe()
        self.wait(READ_RES)

        # ══ B6. A lei de Ampère, ancorada; o retângulo totalmente FORA (51–58 s) ═══════════════════════
        self.play(*self.caption("CORTE LONGITUDINAL"), FadeOut(self.expr), run_time=0.53)
        self.expr = None
        self.play(self.tilt.animate.set_value(0.0), run_time=0.73)
        self.play(self.coil_op.animate.set_value(0), self.cut_op.animate.set_value(1), run_time=0.60)
        self.play(self.bin_op.animate.set_value(1), run_time=0.53)
        rh1 = VGroup(odot(ORIGIN, CYAN_L), text("corrente saindo", 20, opacity=0.85)
                     ).arrange(RIGHT, buff=0.18).move_to([0, AX_Y + RS + 0.60, 0])
        rh2 = VGroup(otimes(ORIGIN, CYAN_L), text("corrente entrando", 20, opacity=0.85)
                     ).arrange(RIGHT, buff=0.18).move_to([0, AX_Y - RS - 0.60, 0])
        self.play(FadeIn(rh1), FadeIn(rh2), run_time=0.53)
        self.note(tag("mão direita: dentro, o campo aponta para a direita", 22, 0.9))
        self.check_safe()
        self.wait(BEAT)

        self.play(*self.caption("LEI DE AMPÈRE"), FadeOut(VGroup(rh1, rh2)),
                  self.bin_op.animate.set_value(0.4), FadeOut(self.hint), run_time=0.60)
        self.hint = None
        self.op_y, self.note_y = AMP_OP_Y, AMP_SIDE_Y
        law = mtex(r"\oint \vec B\cdot d\vec\ell", "=", r"\mu_0 I_{\text{enc}}", size=40)
        law.move_to([0, AMP_LAW_Y, 0]).set_opacity(0.8)
        self.play(FadeIn(law, shift=UP * 0.1), run_time=0.53)
        self.play(*self.push_chip(r"\vec B = B(s)\,\hat z"), run_time=0.60)
        self.note(tag("ela fica aqui: vale nos três casos a seguir", 23, 0.9))
        self.wait(BEAT)

        # ══ B7. O retângulo totalmente fora: B_fora é constante (58–76 s) ══════════════════════════════
        self.play(*self.caption("UM RETÂNGULO TODO FORA"),
                  self.amp_op.animate.set_value(1), self.side_op.animate.set_value(1),
                  self.ell_op.animate.set_value(1), self.bout_op.animate.set_value(1),
                  run_time=0.73)
        self.note(tag("o campo lá fora ainda é desconhecido", 23, 0.9))
        self.check_safe()
        self.wait(BEAT)
        ienc0 = mtex(r"I_{\text{enc}}", "=", "0", size=44)
        fit(ienc0).move_to([0, self.op_y, 0])
        self.play(FadeIn(ienc0, shift=UP * 0.1), run_time=0.53)
        self.expr = ienc0
        self.note(tag("nenhuma corrente atravessa essa superfície", 22, 0.9))
        self.wait(BEAT)

        # percorrer e iluminar cada lado, levando sua parcela à equação
        terms = VGroup(tex(r"B(s_1)\,\ell", 42), tex("+\\,0", 42), tex(r"-\,B(s_2)\,\ell", 42),
                       tex("+\\,0", 42), tex("=\\,0", 42)).arrange(RIGHT, buff=0.16)
        fit(terms).move_to([0, self.op_y, 0])
        self.play(soft_swap(self.expr, terms[0]), self.act1.animate.set_value(1), run_time=0.67)
        self.wait(0.35)
        self.play(FadeIn(terms[1], shift=RIGHT * 0.1), self.actR.animate.set_value(1),
                  self.act1.animate.set_value(0.35), run_time=0.53)
        self.wait(0.35)
        self.play(FadeIn(terms[2], shift=RIGHT * 0.1), self.act2.animate.set_value(1),
                  self.actR.animate.set_value(0.35), run_time=0.53)
        self.wait(0.35)
        self.play(FadeIn(terms[3], shift=RIGHT * 0.1), self.actL.animate.set_value(1),
                  self.act2.animate.set_value(0.35), run_time=0.53)
        self.wait(0.35)
        self.play(FadeIn(terms[4], shift=RIGHT * 0.1), self.actL.animate.set_value(0.35),
                  Indicate(law[2], color=WHITE, scale_factor=1.15), run_time=0.53)
        self.expr = terms
        self.note(tag("os lados curtos são perpendiculares a B: valem zero", 21, 0.9))
        self.check_safe()
        self.wait(READ)

        noz = mtex(r"B(s_1)\,\ell", "-", r"B(s_2)\,\ell", "=", "0", size=44)
        fit(noz).move_to([0, self.op_y, 0])
        self.play(FadeOut(terms[1], scale=0.3), FadeOut(terms[3], scale=0.3), run_time=0.53)
        self.expr = VGroup(terms[0], terms[2], terms[4])
        self.play(soft_swap(self.expr, noz), run_time=0.60)
        self.expr = noz
        self.wait(BEAT)
        divl = mtex("B(s_1)", "=", "B(s_2)", size=46)
        self.show_expr(divl, run_time=0.67)
        self.note(tag("dividindo por ℓ > 0", 23, 0.9))
        self.wait(BEAT)
        constf = mtex(r"B_{\text{fora}}(s)", "=", r"\text{constante}", size=42)
        self.show_expr(constf, run_time=0.67, match=False)
        self.note(tag("por fora, B não muda com a distância", 22, 0.9))
        self.check_safe()
        self.wait(READ_RES)

        # ══ B8. A condição no infinito, numa etapa separada (76–83 s) ══════════════════════════════════
        self.play(*self.caption("QUANTO VALE ESSA CONSTANTE?"), run_time=0.53)
        cond = VGroup(text("campo do solenoide, sem campo externo imposto", 18, WHITE, 0.8),
                      mtex("B(s)", r"\longrightarrow", "0", r"\quad (s\to\infty)", size=34)
                      ).arrange(DOWN, buff=0.10).move_to([0, -1.80, 0])
        self.note(None)
        self.play(FadeIn(cond, shift=UP * 0.1), self.probe.animate.set_value(1.0), run_time=0.80)
        self.wait(BEAT)
        zero = mtex(r"B_{\text{fora}}", "=", "0", size=50)
        fit(zero).move_to([0, self.op_y, 0])
        zbox = SurroundingRectangle(zero, color=WHITE, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.play(TransformFromCopy(constf, zero), Indicate(cond[1], color=WHITE, scale_factor=1.1),
                  FadeOut(self.expr), run_time=0.93)
        self.play(Create(zbox), self.bout_op.animate.set_value(0), run_time=0.53)
        self.expr = VGroup(zero, zbox)
        self.check_safe()
        self.wait(READ)
        self.play(FadeOut(cond), *self.push_chip(r"B_{\text{fora}} = 0"),
                  FadeOut(self.expr), run_time=0.60)
        self.expr = None

        # ══ B9. O MESMO retângulo, agora dentro (83–88 s) ══════════════════════════════════════════════
        self.play(*self.caption("O MESMO RETÂNGULO, AGORA DENTRO"),
                  self.act1.animate.set_value(0), self.act2.animate.set_value(0),
                  self.actL.animate.set_value(0), self.actR.animate.set_value(0),
                  self.probe.animate.set_value(0), run_time=0.60)
        self.play(self.amp_y.animate.set_value(Y_IN), run_time=1.16)
        in_eq = mtex(r"I_{\text{enc}}=0", r"\;\Rightarrow\;", "B(s_1)", "=", "B(s_2)", size=40)
        fit(in_eq).move_to([0, self.op_y, 0])
        self.play(FadeIn(in_eq, shift=UP * 0.1), self.act1.animate.set_value(1),
                  self.act2.animate.set_value(1), run_time=0.67)
        self.expr = in_eq
        self.wait(BEAT)
        uni = mtex(r"B_{\text{dentro}}", "=", r"\text{constante}", size=44)
        self.show_expr(uni, run_time=0.67, match=False)
        self.note(tag("dentro, o campo é o mesmo em toda parte", 23, 0.9))
        self.check_safe()
        self.wait(BEAT)
        self.play(*self.push_chip(r"B_{\text{dentro}} = \text{const.}"), FadeOut(self.expr),
                  run_time=0.60)
        self.expr = None

        # ══ B10. Atravessando a parede: duas fontes, contorno e corrente (88–91 s) ═════════════════════
        self.play(*self.caption("AGORA ATRAVESSANDO A PAREDE"),
                  self.act1.animate.set_value(0), self.act2.animate.set_value(0), run_time=0.60)
        self.play(self.amp_y.animate.set_value(Y_WALL), run_time=1.16)
        h_left = text("CONTORNO", 19, VIOLET, 0.9).move_to([-COL_X, self.op_y + 0.55, 0])
        h_right = text("CORRENTE ENVOLVIDA", 19, MAGENTA, 0.9).move_to([COL_X, self.op_y + 0.55, 0])
        h_right.scale_to_fit_width(min(h_right.width, 3.1))
        self.play(FadeIn(h_left), FadeIn(h_right), run_time=0.53)
        self.check_safe()
        self.wait(BEAT)

        # ══ B11. O lado do contorno: só o lado de dentro contribui (91–96 s) ═══════════════════════════
        cont_eq = mtex(r"\oint \vec B\cdot d\vec\ell", "=", r"B\,\ell", size=34)
        cont_eq.scale_to_fit_width(min(cont_eq.width, 3.1)).move_to([-COL_X, self.op_y, 0])
        self.play(FadeIn(cont_eq[0], shift=UP * 0.1), self.act1.animate.set_value(1), run_time=0.53)
        self.note(tag("só o lado de dentro contribui", 23, 0.9))
        self.wait(BEAT)
        self.play(self.actL.animate.set_value(1), self.actR.animate.set_value(1),
                  self.act2.animate.set_value(1), run_time=0.53)
        self.note(tag("laterais perpendiculares e lado externo nulo: zero", 21, 0.9))
        self.wait(BEAT)
        self.play(FadeIn(cont_eq[1]), FadeIn(cont_eq[2]),
                  self.actL.animate.set_value(0.3), self.actR.animate.set_value(0.3),
                  self.act2.animate.set_value(0.3), run_time=0.60)
        self.check_safe()
        self.wait(BEAT)

        # ══ B12. O lado da corrente envolvida: N_l = n l, uma fileira só (96–102 s) ════════════════════
        self.note(tag("dentro de ℓ, quantas seções de fio passam?", 22, 0.9))
        self.play(self.enc_n.animate.set_value(6.0), run_time=1.20, rate_func=linear)
        self.wait(BEAT)
        nl = mtex(r"N_\ell", "=", r"n\,\ell", size=38)
        nl.move_to([COL_X, self.op_y, 0])
        self.play(FadeIn(nl, shift=UP * 0.1), run_time=0.53)
        self.note(tag("n é o número de espiras por comprimento", 23, 0.9))
        self.check_safe()
        self.wait(BEAT)
        ienc = mtex(r"I_{\text{enc}}", "=", r"n\,\ell\,I", size=38)
        ienc.move_to([COL_X, self.op_y, 0])
        self.play(soft_swap(nl, ienc), run_time=0.60)
        self.note(tag("cada uma carrega a mesma corrente I", 23, 0.9))
        self.check_safe()
        self.wait(BEAT)

        # ══ B13. As duas metades se encaixam: B = mu0 n I (102–111 s) ══════════════════════════════════
        self.play(*self.caption("AS DUAS METADES SE ENCAIXAM"),
                  FadeOut(VGroup(h_left, h_right)), FadeOut(self.hint),
                  self.enc_n.animate.set_value(0.0),
                  Indicate(law, color=WHITE, scale_factor=1.06), run_time=0.67)
        self.hint = None
        full = mtex("B", r"\ell", "=", r"\mu_0", "n", r"\ell", "I", size=50)
        fit(full).move_to([0, self.op_y, 0])
        self.play(TransformFromCopy(cont_eq[2], VGroup(full[0], full[1])),
                  TransformFromCopy(ienc[2], VGroup(full[4], full[5], full[6])),
                  FadeIn(full[2]), FadeIn(full[3]),
                  FadeOut(cont_eq), FadeOut(ienc), run_time=1.16)
        self.expr = full
        self.check_safe()
        self.wait(BEAT)
        self.play(full[1].animate.set_color(MAGENTA), full[5].animate.set_color(MAGENTA),
                  Indicate(full[1], color=MAGENTA, scale_factor=1.4),
                  Indicate(full[5], color=MAGENTA, scale_factor=1.4), run_time=0.67)
        self.note(tag("o mesmo ℓ dos dois lados", 24, 0.9))
        self.wait(BEAT)
        self.play(full[1].animate.scale(0.1).set_opacity(0),
                  full[5].animate.scale(0.1).set_opacity(0), run_time=0.60)
        res = mtex("B", "=", r"\mu_0", "n", "I", size=58)
        fit(res).move_to([0, self.op_y, 0])
        rbox = SurroundingRectangle(res, color=WHITE, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.play(TransformMatchingTex(full, res), Create(rbox), run_time=0.80)
        self.expr = VGroup(res, rbox)
        self.note(tag("exato no modelo ideal, com as premissas ao lado", 21, 0.95))
        self.check_safe()
        self.wait(READ_RES)

        # ══ B14. O que cada termo quer dizer (111–116 s) ═══════════════════════════════════════════════
        self.play(*self.caption("LENDO A FÓRMULA"), run_time=0.53)
        self.note(tag("n: espiras por comprimento", 24, 0.95))
        self.play(Indicate(res[3], color=CYAN, scale_factor=1.6),
                  self.enc_n.animate.set_value(6.0), run_time=0.67)
        self.wait(BEAT)
        self.note(tag("I: a corrente em cada uma delas", 24, 0.95))
        self.play(Indicate(res[4], color=CYAN_L, scale_factor=1.6),
                  self.bin_op.animate.set_value(1.0), run_time=0.67)
        self.check_safe()
        self.wait(BEAT)

        # ══ B15. De volta ao solenoide real: = vira ~= (116–123 s) ═════════════════════════════════════
        self.play(*self.caption("DE VOLTA À BOBINA REAL"),
                  self.amp_op.animate.set_value(0), self.side_op.animate.set_value(0),
                  self.ell_op.animate.set_value(0), self.enc_n.animate.set_value(0),
                  FadeOut(law), FadeOut(self.shelf), run_time=0.60)
        self.play(self.cont.animate.set_value(0.0), self.zlim.animate.set_value(Z_FIN),
                  self.cutext_op.animate.set_value(1), FadeOut(ideal), run_time=1.30)
        self.note(tag("as pontas e os retornos voltam", 24, 0.9))
        self.wait(BEAT)
        approx = mtex("B", r"\simeq", r"\mu_0", "n", "I", size=58)
        fit(approx).move_to(res.get_center())
        abox2 = SurroundingRectangle(approx, color=WHITE, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.note_y = -3.70
        new_note = tag("região central · solenoide longo, L bem maior que R", 21, 0.95)
        new_note.move_to([0, self.note_y, 0])
        self.play(TransformMatchingTex(res, approx), Transform(rbox, abox2),
                  soft_swap(self.hint, new_note), run_time=1.30)
        self.hint = new_note
        self.expr = VGroup(approx, rbox)
        self.check_safe()
        self.wait(READ_RES)

        # ══ B16. Testando a fórmula (na bobina finita) (123–130 s) ═════════════════════════════════════
        finite_tag = tag("BOBINA LONGA FINITA", 20, 0.85, VIOLET).move_to([0, 4.85, 0])
        self.play(*self.caption("TESTANDO A FÓRMULA"), FadeIn(finite_tag), run_time=0.60)
        self.note(tag("mesma geometria, mais corrente", 23, 0.9))
        self.play(Indicate(approx[4], color=CYAN_L, scale_factor=1.5),
                  self.cur.animate.set_value(1.6), run_time=0.93)
        self.check_safe()
        self.wait(BEAT)
        self.play(self.cur.animate.set_value(1.0), run_time=0.53)
        nlab = mtex("n", "=", r"\tfrac{N}{L}", size=36).move_to([0, AMP_SIDE_Y, 0]).set_opacity(0.85)
        self.note(tag("agora o mesmo L e o mesmo I: só mais voltas", 22, 0.9))
        self.play(FadeIn(nlab, shift=UP * 0.1), Indicate(approx[3], color=CYAN, scale_factor=1.5),
                  self.extra_op.animate.set_value(1.0), run_time=1.30)
        self.check_safe()
        self.wait(READ)

        # ══ B17. Coda: o solenoide como atuador (130–136 s) ════════════════════════════════════════════
        self.play(*self.caption("ONDE ISSO APARECE"), self.cut_op.animate.set_value(0),
                  self.bin_op.animate.set_value(0), self.extra_op.animate.set_value(0),
                  self.cutext_op.animate.set_value(0), FadeOut(self.expr), FadeOut(nlab),
                  FadeOut(finite_tag), FadeOut(self.hint), run_time=0.60)
        self.expr = self.hint = None

        cy = 1.6
        winds = VGroup(*(Line([x, cy - 0.85, 0], [x, cy + 0.85, 0]).set_stroke(BLUE, 5)
                         for x in np.arange(-6, 7) * 0.28))
        core = RoundedRectangle(width=1.7, height=0.62, corner_radius=0.16).set_stroke(WHITE, 3, 0.9)
        core.set_fill(WHITE, 0.18).move_to([1.55, cy, 0])
        yb = cy - 1.55
        circuit = VGroup(Line([-1.68, cy - 0.85, 0], [-1.68, yb, 0]), Line([-1.68, yb, 0], [-1.0, yb, 0]),
                         Line([1.68, cy - 0.85, 0], [1.68, yb, 0]), Line([1.68, yb, 0], [-0.3, yb, 0])
                         ).set_stroke(BLUE, 3, 0.7)
        sw = Line([-1.0, yb, 0], [-0.4, yb + 0.4, 0]).set_stroke(WHITE, 3, 0.85)
        pipe = VGroup(Line([-2.6, -1.95, 0], [2.6, -1.95, 0]),
                      Line([-2.6, -2.95, 0], [2.6, -2.95, 0])).set_stroke(BLUE, 3, 0.7)
        gate = Rectangle(width=0.5, height=1.0).set_stroke(WHITE, 3, 0.9).set_fill(WHITE, 0.25)
        gate.move_to([0.4, -2.45, 0])
        state = tag("VÁLVULA FECHADA", 24, 0.9).move_to([0, -3.4, 0])
        self.note_y = -4.05
        self.play(FadeIn(VGroup(winds, core, circuit, sw)), FadeIn(VGroup(pipe, gate, state)),
                  run_time=0.60)
        self.note(tag("núcleo parcialmente inserido, perto da extremidade", 21, 0.9))
        self.check_safe()
        self.wait(BEAT)
        i_on = tex("I", 32, CYAN_L).move_to([-2.1, yb + 0.3, 0])
        self.play(sw.animate.put_start_and_end_on([-1.0, yb, 0], [-0.3, yb, 0]),
                  circuit.animate.set_stroke(CYAN_L, 3, 1.0), FadeIn(i_on), run_time=0.53)
        self.note(tag("liga a corrente: o campo aparece dentro da bobina", 21, 0.9))
        self.play(core.animate.shift(LEFT * 1.25), run_time=0.80)
        new_state = tag("VÁLVULA ABERTA", 24, 0.95).move_to([0, -3.4, 0])
        self.play(gate.animate.shift(UP * 0.95), soft_swap(state, new_state), run_time=0.60)
        self.note(tag("o núcleo entra e a válvula muda de estado", 21, 0.9))
        self.check_safe()
        self.wait(BEAT)

        # ══ B18. Fechamento (136–139 s) ════════════════════════════════════════════════════════════════
        self.play(*self.caption("SUPERPOSIÇÃO + SIMETRIA + AMPÈRE"),
                  FadeOut(VGroup(winds, core, circuit, sw, i_on, pipe, gate, new_state)),
                  FadeOut(self.hint), run_time=0.60)
        self.hint = None
        final = boxed(mtex("B", r"\simeq", r"\mu_0\,n\,I", size=54)).move_to([0, 0.6, 0])
        handle = tag("@labparallax", 22, 0.8).move_to([0, -0.9, 0])
        self.play(FadeIn(final, shift=UP * 0.1), run_time=0.53)
        self.play(FadeIn(handle, shift=UP * 0.1), run_time=0.53)
        self.check_safe()
        self.wait(1.2)
