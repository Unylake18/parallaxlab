"""Campo magnético dentro de um solenoide: B = mu0 n I; preview silencioso.

DA EQUAÇÃO AO FENÔMENO · EP. 03. Continua o episódio da espira (videos/vid_0008_campo_espira/cena.py):
parte da expressão já derivada lá e não rederiva Biot-Savart. Uma ideia só: o campo do solenoide
é a soma dos campos de muitas espiras e, numa bobina longa, B ~= mu0 n I.

Semântica de cor (fixa):
  azul     geometria da bobina, espiras inativas, fios e estrutura;
  ciano    campo B: vetores, curva B(z) e todo termo que representa B;
  verde    corrente: espira ativa, I, N_l, n, I_enc e fios enlaçados;
  magenta  contorno de Ampère: retângulo, d l, l e rho;
  violeta  medidas geométricas (L, dz') e componentes transversais;
  branco   álgebra neutra e o ponto P.

  B1  retomada: UMA espira e o seu campo no eixo, B_esp(dz), do episódio 8.
  B2  superposição: a espira é copiada e deslocada em torno de P; cada cópia acende em magenta,
      manda a sua parcela B_j (ciano) até a soma e volta a azul; B1+B2+B3+... se compacta em Sum.
  B3  soma discreta -> contínua: n = N/L, uma fatia dz' (magenta) tem dN = n dz' espiras;
      dB = B_esp dN, B = Int dB e a integral com a fração explícita.
  B4  bobina finita + gráfico no MESMO x: P percorre o eixo (um tracker) e a seta, o prumo e o
      ponto na curva andam juntos. A curva vem da fórmula fechada b_fin.
  B5  L/R cresce com R fixo: L/sqrt(L^2+4R^2) = 1/sqrt(1+4(R/L)^2) -> 1, junto com a bobina e o
      gráfico; na ponta de uma bobina LONGA, cerca de 1/2.
  B6  limite ideal: L/R -> inf e passagem ao corte do modelo infinito.
  B7  simetria: duas fatias simétricas dão dB com partes axiais iguais e transversais opostas;
      as transversais se cancelam => B axial; a translação vale só no modelo infinito => B(rho) z^.
  B8  Ampère, um só retângulo: cada lado entrega o seu termo; fora ([B(rho1)-B(rho2)] l = 0 =>
      B_fora constante; B -> 0 no infinito => B_fora = 0) e dentro (B_dentro constante).
  B9-B11  atravessando a parede: os termos somem até B l; fios enlaçados (magenta) dão N_l = n l
      e I_enc = n l I; B l = mu0 n l I, os dois l se cancelam: B = mu0 n I.
  B12 lendo a fórmula: I sobe e n dobra (mesmo comprimento) => setas maiores.
  B13 volta à bobina real: as pontas reaparecem enquanto "=" vira "~=".
  B14 atuador: núcleo na ENTRADA, onde o campo varia. B15 fechamento.

Unidades internas: R = 1; b = B / (mu0 I / 2R); passo PITCH = 0,5 R => n = 2/R e mu0 n I vale
B_IDEAL = 4 nessa escala. O gráfico usa B / (mu0 n I) = b / B_IDEAL. l = 3 R => N_l = n l = 6.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, ORIGIN, PI, RIGHT, UP, Circle, Create, DashedLine, Dot, FadeIn, FadeOut, ImageMobject,
    Indicate, LaggedStart, Line, ManimColor, MathTex, Rectangle, RoundedRectangle,
    SurroundingRectangle, Transform, TransformFromCopy, TransformMatchingTex, VGroup, VMobject,
    ValueTracker, always_redraw, interpolate_color, linear, Scene, config,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))   # montar_legendado.py importa esta cena
from comum import (
    BLUE, B_IDEAL, CUT_EXTRA, CUT_Z, CYAN, ENC_Z, L_ELL, MAGENTA, PITCH, VIOLET, WHITE,
    CenaBase, b_loop, boxed, fit, mtex, odot, otimes, plate, right_angle, soft_swap,
    span_mark, tag, tex, text, vec,
)
from template.config import WATERMARK_PATH

PASTA = Path(__file__).resolve().parent
CAL = os.environ.get("SYNC_CAL") == "1"        # calibragem: mede o tempo NATIVO de cada âncora

AMBER = "#3FE08B"         # CORRENTE (verde): I, I_enc, N_l, n, espira ativa e fios enlaçados; nunca ciano, laranja ou amarelo

# Termos coloridos na legenda (montar_legendado.py --color-module), com o mesmo significado da cena:
# campo B ciano, corrente e densidade verdes, comprimento violeta, Ampère/transversais magenta.
SUBTITLE_TERM_COLORS = {
    "campo": CYAN, "campos": CYAN,
    "corrente": AMBER, "densidade de espiras": AMBER, "densidade": AMBER,
    "comprimento": VIOLET,
    "retângulo": MAGENTA, "Ampère": MAGENTA, "transversal": MAGENTA, "transversais": MAGENTA,
    "cancelam": MAGENTA, "cancela": MAGENTA,
}

# ── Modelo físico desta cena ────────────────────────────────────────────────
# Ordem de entrada das espiras em torno de P (z = 0): 0, +1, -1, +2, -2, ... (em passos PITCH).
ORDER = np.array([0] + [s * k for k in range(1, 41) for s in (1, -1)], dtype=float)


def order_turns(nt):
    """Posições e pesos das nt primeiras espiras (nt real: a que entra pesa nt - i)."""
    k = int(np.ceil(nt - 1e-9))
    return ORDER[:k] * PITCH, np.clip(nt - np.arange(k), 0.0, 1.0)


def b_order(z, nt):
    """Superposição real das nt espiras, em unidades de mu0 I / 2R."""
    zs, w = order_turns(nt)
    return float(np.sum(w * b_loop(z, zs)))


def b_fin(z, lr):
    """B_z / (mu0 n I) no eixo de um solenoide CONTÍNUO de comprimento lr (em R), centrado em 0."""
    a = np.asarray(z, dtype=float) + lr / 2
    b = np.asarray(z, dtype=float) - lr / 2
    return 0.5 * (a / np.sqrt(1 + a * a) - b / np.sqrt(1 + b * b))


# ── Conferências do modelo, no import ───────────────────────────────────────
# Sigma -> Int: com n espiras por comprimento, o trecho dz' carrega n dz' espiras; somando
# B_j = mu0 I R^2 / 2[R^2+(z-z')^2]^{3/2} sobre elas, B/(mu0 n I) = (R^2/2) Int dz'/[...]^{3/2}.
_zp = np.linspace(-2.25, 2.25, 40001)
for _z in (0.0, 1.3, 2.25, 4.0):
    _f = b_loop(_z, _zp)
    _int = (_zp[1] - _zp[0]) * (_f.sum() - 0.5 * (_f[0] + _f[-1]))
    assert np.isclose(0.5 * _int, b_fin(_z, 4.5), rtol=1e-6)          # a fórmula fechada do gráfico
for _L in (3.5, 10.5, 40.0):
    assert np.isclose(b_fin(0.0, _L), _L / np.sqrt(_L ** 2 + 4.0))    # B(0) = mu0nI L/sqrt(L^2+4R^2)
assert abs(b_fin(0.0, 4000.0) - 1.0) < 1e-6                           # L >> R: B(0) -> mu0 n I
assert abs(b_fin(2000.0, 4000.0) - 0.5) < 1e-6                        # e na ponta -> mu0 n I / 2
assert b_fin(0.5, 1.0) / b_fin(0.0, 1.0) > 0.75                       # bobina curta: ponta NÃO é metade
assert abs(b_fin(5.25, 10.5) / b_fin(0.0, 10.5) - 0.5) < 0.01         # bobina longa: ponta ~ metade
assert np.allclose(b_fin(-_zp, 4.5), b_fin(_zp, 4.5))                 # simetria em z
for _nt in (9, 21):                                                   # discreto ~ contínuo
    assert abs(b_order(0.0, _nt) / B_IDEAL - b_fin(0.0, _nt * PITCH)) < 0.01
assert np.allclose(np.sort(ORDER[:9]), np.arange(-4, 5))              # 9 espiras: simétricas em P
assert np.allclose(np.diff([b_order(0.0, k) for k in range(1, 12)]) > 0, True)   # cada uma soma
# Regra da mão direita, com x^ no eixo, y^ para cima e z^out saindo da tela. Na bobina pseudo-3D
# a espira é (y, prof) = R (cos phi, sin phi); a corrente anda com phi crescente: no topo
# (phi = 0) ela sai da tela (odot), embaixo entra (otimes).
assert np.allclose(np.array([-np.sin(0.0), np.cos(0.0)]), [0.0, 1.0])
# Fio de cima (corrente +z^out) visto do eixo (r^ = -y^) e fio de baixo (corrente -z^out, r^ = +y^):
_zo, _y = np.array([0, 0, 1.0]), np.array([0, 1.0, 0])
assert np.allclose(np.cross(_zo, -_y), [1, 0, 0]) and np.allclose(np.cross(-_zo, _y), [1, 0, 0])
# Retângulo atravessando a parede de cima, percorrido no sentido anti-horário (normal +z^out):
# as seções odot enlaçadas contam +I cada; N_l = n l.
assert int(len(ENC_Z)) == 6 and np.isclose(L_ELL / PITCH, 6.0)

# Algebra da razão B(0)/mu0nI: dividir por L não muda nada; L/R -> inf leva a 1/sqrt(1+0) = 1.
_LL = np.array([2.0, 5.0, 10.5, 40.0])
assert np.allclose(_LL / np.sqrt(_LL ** 2 + 4.0), 1.0 / np.sqrt(1.0 + 4.0 * (1.0 / _LL) ** 2))
assert np.allclose(b_fin(0.0, _LL), 1.0 / np.sqrt(1.0 + 4.0 * (1.0 / _LL) ** 2))
# dN = n dz': o número de espiras num trecho é n vezes o comprimento (n = 1/PITCH por R).
for _a, _w in ((-0.3, 3.0), (0.4, 1.5), (-2.2, 4.5)):
    _ct = np.sum((CUT_Z >= _a) & (CUT_Z < _a + _w))
    assert abs(_ct - _w / PITCH) <= 1
# Cancelamento transversal: Biot-Savart numérico de duas espiras espelhadas em torno do plano
# de P = (rho, 0, 0). As partes axiais (z) são iguais; as radiais (x) são opostas; a azimutal é nula.
def _dbz_loop(pc, zc, n=4000):
    ph = np.linspace(0.0, 2 * np.pi, n, endpoint=False)
    dl = np.stack([-np.sin(ph), np.cos(ph), np.zeros_like(ph)], axis=1) * (2 * np.pi / n)
    r = pc[None, :] - np.stack([np.cos(ph), np.sin(ph), np.full_like(ph, zc)], axis=1)
    return np.sum(np.cross(dl, r) / np.linalg.norm(r, axis=1)[:, None] ** 3, axis=0)
_P, _d = np.array([0.55, 0.0, 0.0]), 0.9
_b1, _b2 = _dbz_loop(_P, +_d), _dbz_loop(_P, -_d)
assert np.isclose(_b1[2], _b2[2]) and _b1[2] > 0                    # axiais iguais e no mesmo sentido
assert np.isclose(_b1[0], -_b2[0]) and abs(_b1[0]) > 1e-3            # transversais opostas e não nulas
assert abs(_b1[1]) < 1e-9 and abs(_b2[1]) < 1e-9                     # sem componente azimutal
for _zz in (0.0, 0.7, 2.0):                                          # o numérico reproduz o analítico no eixo
    assert np.isclose(_dbz_loop(np.array([0.0, 0.0, _zz]), 0.0)[2] / (2 * np.pi), b_loop(_zz))

# ── Geometria de tela ───────────────────────────────────────────────────────
TILT0 = 0.34              # achatamento da profundidade na projeção oblíqua
RS, AX_Y = 1.25, 1.25     # bobina pseudo-3D: unidades de tela por R e altura do eixo
RC = 1.40                 # corte e Ampère: escala um pouco maior, para o celular
AY_S = 2.0                # eixo da bobina na superposição (escala RS)
RG, AY_G = 0.55, 2.60     # bobina + gráfico: escala e eixo
TOP_Y = 4.45              # expressão de referência, abaixo da manchete
CHAIN_DY = 0.50           # fila de parcelas: abaixo da bobina
ARR_S, ARR_G = 2.0, 1.0   # comprimento da seta de B quando B = mu0 n I
G_Y0, G_H = -2.30, 2.20   # base do gráfico e altura do valor 1
G_XL, G_XR = -3.10, 3.30
X_VIS = 5.2               # só desenhamos o que tem |x| < X_VIS
ARR_IN = 0.62             # seta do campo interno no corte quando B = mu0 n I
NT_SUP, NT_LONG, NT_INF, NT_ACT = 9, 21, 61, 11
SYM_Z = 1.25              # as duas fatias simétricas do corte, em torno de P: z = ±1,25 R
WIRE = "#7FB4FF"          # fio no corte (azul claro)
CX_ACT = -0.90            # a bobina do atuador vai para a esquerda: a válvula fica à direita

RECT_W, RECT_H = L_ELL * RC, 1.05
Y_OUT, Y_FAR, Y_IN, Y_WALL = 3.80, 5.00, 1.75, 2.60     # centros do retângulo amperiano

SUP_OP_Y, NOTE_Y = -1.55, -3.95
AMP_LAW_Y, AMP_OP_Y, AMP_AUX_Y, AMP_NOTE_Y, SHELF_Y = -0.95, -2.05, -3.00, -3.55, -4.15

assert np.isclose(RECT_W / 2 / RC, L_ELL / 2)
assert Y_OUT - RECT_H / 2 - AX_Y > RC                             # fora: os dois lados longos fora
assert AX_Y + RC - (Y_IN + RECT_H / 2) > 0.2                      # dentro: os dois lados dentro
assert Y_WALL - RECT_H / 2 < AX_Y + RC < Y_WALL + RECT_H / 2      # atravessando a parede
assert RG * NT_LONG * PITCH / 2 < G_XR - 0.3                      # as pontas da bobina longa no quadro
assert ARR_S * b_order(0.0, NT_SUP) / B_IDEAL < 3.3               # a fila de parcelas cabe



class CampoSolenoide009(CenaBase):
    op_y, note_y, shelf_y = SUP_OP_Y, NOTE_Y, SHELF_Y

    # ── Bobina pseudo-3D: discreta e contínua ───────────────────────────────
    def coil_pt(self, zc, phi):
        t, rs = self.tilt.get_value(), self.rs.get_value()
        return np.array([self.cx.get_value() + rs * (zc + t * np.sin(phi)),
                         self.ay.get_value() + rs * np.cos(phi), 0.0])

    def px(self):
        return self.cx.get_value() + self.rs.get_value() * self.pz.get_value()

    def turn_pos(self):
        """Com slide = 1 a espira que entra sai da primeira e desliza até o seu lugar (cópia)."""
        zs, w = order_turns(self.nt.get_value())
        e = w * w * (3 - 2 * w)
        return zs * (1.0 - self.slide.get_value() * (1.0 - e)), w

    def coil(self):
        """Espiras discretas: azuis; a espira ativa (self.focus) acende em magenta."""
        op0 = self.coil_op.get_value() * (1.0 - self.cont.get_value())
        g = VGroup()
        if op0 < 0.01:
            return g
        pos, w = self.turn_pos()
        foc, rs, cx = self.focus.get_value(), self.rs.get_value(), self.cx.get_value()
        for near in (False, True):
            phis = np.linspace(0, PI, 25) + (0 if near else PI)
            for j, (zc, wi) in enumerate(zip(pos, w)):
                if wi < 0.01 or abs(cx + rs * zc) >= X_VIS:
                    continue
                on = foc >= 0 and abs(j - foc) < 0.5
                hi = 1.0 if (foc < 0 or on) else 0.4
                g.add(VMobject().set_points_as_corners([self.coil_pt(zc, p) for p in phis])
                      .set_stroke(AMBER if on else BLUE, (8 if on else 6) * rs / RS,
                                  op0 * wi * hi * (1.0 if near else 0.38)))
        return g

    def coil_cont(self):
        """Enrolamento contínuo de comprimento L = nt · passo: tampas, silhueta e trama fina."""
        op = self.coil_op.get_value() * self.cont.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        rs, cx, ay = self.rs.get_value(), self.cx.get_value(), self.ay.get_value()
        half = self.nt.get_value() * PITCH / 2
        x0, x1 = max(cx - rs * half, -X_VIS), min(cx + rs * half, X_VIS)
        col = interpolate_color(ManimColor(BLUE), ManimColor("#8AE9FF"), self.glow.get_value())
        g.add(Rectangle(width=x1 - x0, height=2 * rs).set_stroke(width=0)
              .set_fill(BLUE, 0.10 * op).move_to([(x0 + x1) / 2, ay, 0]))
        for s in (1, -1):
            g.add(Line([x0, ay + s * rs, 0], [x1, ay + s * rs, 0]).set_stroke(BLUE, 1 + 3 * rs / RS, op))
        step = 0.17 / rs
        phis = np.linspace(0, PI, 13)
        for zc in np.arange(-half + step / 2, half, step):
            if abs(cx + rs * zc) < X_VIS:
                g.add(VMobject().set_points_as_corners([self.coil_pt(zc, p) for p in phis])
                      .set_stroke(col, 1.6, 0.45 * op))
        for zc in (-half, half):
            if abs(cx + rs * zc) >= X_VIS:
                continue
            for near in (False, True):
                ph = np.linspace(0, PI, 25) + (0 if near else PI)
                g.add(VMobject().set_points_as_corners([self.coil_pt(zc, p) for p in ph])
                      .set_stroke(BLUE, 3.5, op * (1.0 if near else 0.38)))
        return g

    def current_marks(self):
        """Sentido da corrente (magenta): na face da frente (phi = pi/2) ela desce na tela."""
        op = self.cur_op.get_value() * self.coil_op.get_value() * (1 - self.cont.get_value())
        g = VGroup()
        if op < 0.01:
            return g
        pos, w = self.turn_pos()
        rs = self.rs.get_value()
        for zc, wi in zip(pos, w):
            c = self.coil_pt(zc, PI / 2)
            if wi > 0.99 and abs(c[0]) < 2.9:
                d = 0.21 * rs / RS
                g.add(vec(c + UP * d, c + DOWN * d, AMBER, 4).set_opacity(op * 0.9))
        return g

    def len_span(self):
        """Cota L em cima da bobina (violeta: medida geométrica); acompanha o comprimento."""
        op = self.span_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        rs, cx = self.rs.get_value(), self.cx.get_value()
        half = rs * self.nt.get_value() * PITCH / 2
        y = self.ay.get_value() + rs + 0.28
        a, b = max(cx - half, -X_VIS), min(cx + half, X_VIS)
        g.add(span_mark(np.array([a, y, 0]), np.array([b, y, 0]), VIOLET, op=0.85 * op))
        g.add(self._llab.copy().set_opacity(op).move_to([a - 0.25, y, 0]))
        return g

    def ext_lines(self):
        """Retorno externo da bobina finita: esboço QUALITATIVO (não sai da fórmula axial)."""
        nt = self.nt.get_value()
        op = self.ext_op.get_value() * float(np.clip((30.0 - nt) / 12.0, 0.0, 1.0))
        g = VGroup()
        if op < 0.01:
            return g
        rs, cx, ay = self.rs.get_value(), self.cx.get_value(), self.ay.get_value()
        a, h = rs * (nt * PITCH / 2 + 0.5), rs * 1.6
        th = np.linspace(0, PI, 60)
        for sgn in (1, -1):
            g.add(VMobject().set_points_as_corners(
                [[cx + a * np.cos(t), ay + sgn * h * np.sin(t), 0] for t in th]
            ).set_stroke(CYAN, 2.5, 0.4 * op))
            g.add(vec([cx + 0.18, ay + sgn * h, 0], [cx - 0.18, ay + sgn * h, 0], CYAN, 3).set_opacity(0.6 * op))
        return g

    # ── Ponto P, parcelas e resultante ──────────────────────────────────────
    def bval(self, z):
        """B/(mu0 n I) em z: soma discreta, que se funde na contínua conforme cont -> 1."""
        c, nt = self.cont.get_value(), self.nt.get_value()
        v = 0.0
        if c < 0.999:
            v += (1 - c) * b_order(z, nt) / B_IDEAL
        if c > 1e-3:
            v += c * float(b_fin(z, nt * PITCH))
        return v * self.cur.get_value()

    def p_dot(self):
        op = self.p_op.get_value()
        if op < 0.01:
            return VGroup()
        c = np.array([self.px(), self.ay.get_value(), 0.0])
        return VGroup(Dot(c, 0.09, color=WHITE).set_opacity(op),
                      self._plab.copy().set_opacity(op).move_to(c + np.array([-0.30, 0.30, 0])))

    def p_arrow(self):
        """Campo local em P (ciano): comprimento = soma real das contribuições."""
        op = self.bres_op.get_value()
        L = self.arr_k.get_value() * self.bval(self.pz.get_value())
        if op < 0.01 or L < 0.04:
            return VMobject()
        a = np.array([self.px(), self.ay.get_value(), 0.0])
        return vec(a, a + RIGHT * L, CYAN, 8).set_opacity(op)

    def chain_y(self):
        return self.ay.get_value() - self.rs.get_value() - CHAIN_DY

    def chain(self):
        """As parcelas B_j(P) (ciano), enfileiradas ponta com cauda: o total é a resultante."""
        op = self.chain_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        zs, w = order_turns(self.nt.get_value())
        pz, k, foc = self.pz.get_value(), self.arr_k.get_value(), self.focus.get_value()
        x, y = self.px(), self.chain_y()
        for j, (zj, wj) in enumerate(zip(zs, w)):
            L = k * wj * float(b_loop(pz, zj)) / B_IDEAL
            if L > 0.03:
                on = foc >= 0 and abs(j - foc) < 0.5
                a = 1.0 if (foc < 0 or on) else 0.35
                g.add(vec([x, y, 0], [x + L, y, 0], CYAN, 5)
                      .set_opacity(op * a * (0.95 if j % 2 == 0 else 0.6)))
            x += L
        return g

    def chain_ties(self):
        """Prumos: P e a ponta da resultante sobre o começo e o fim da fila."""
        op = self.tie_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        x0, y0, y1 = self.px(), self.ay.get_value(), self.chain_y()
        x1 = x0 + self.arr_k.get_value() * self.bval(self.pz.get_value())
        for x in (x0, x1):
            g.add(DashedLine([x, y0, 0], [x, y1, 0], dash_length=0.08).set_stroke(WHITE, 2, 0.45 * op))
        return g

    # ── Gráfico B/(mu0 n I) no mesmo x da bobina ────────────────────────────
    def graph_curve(self):
        op = self.curve_op.get_value()
        if op < 0.01:
            return VMobject()
        rs, cx = self.rs.get_value(), self.cx.get_value()
        xmax = min(G_XR, self.px()) if self.curve_follow.get_value() > 0.5 else G_XR
        if xmax <= G_XL + 0.03:
            return VMobject()
        xs = np.linspace(G_XL, xmax, max(3, int(240 * (xmax - G_XL) / (G_XR - G_XL))))
        ys = G_Y0 + G_H * self.cur.get_value() * b_fin((xs - cx) / rs, self.nt.get_value() * PITCH)
        return VMobject().set_points_as_corners(
            np.column_stack([xs, ys, np.zeros_like(xs)])).set_stroke(CYAN, 5, op)

    def graph_mark(self):
        """Prumo magenta de P até o eixo do gráfico e o ponto ciano na curva: o mesmo tracker pz."""
        op = self.mark_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        x = self.px()
        g.add(DashedLine([x, self.ay.get_value(), 0], [x, G_Y0, 0], dash_length=0.08)
              .set_stroke(WHITE, 1.8, 0.6 * op))
        g.add(Dot([x, G_Y0 + G_H * self.bval(self.pz.get_value()), 0], 0.09, color=CYAN).set_opacity(op))
        return g

    def graph_ends(self):
        """As pontas da bobina (azul: geometria), levadas até o gráfico."""
        op = self.ends_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        rs, cx = self.rs.get_value(), self.cx.get_value()
        half = rs * self.nt.get_value() * PITCH / 2
        for x in (cx - half, cx + half):
            if G_XL < x < G_XR:
                g.add(DashedLine([x, self.ay.get_value() - rs, 0], [x, G_Y0, 0], dash_length=0.09)
                      .set_stroke(BLUE, 2.5, 0.75 * op))
        return g

    # ── Corte longitudinal 2D (modelo infinito) ─────────────────────────────
    def cut_rows(self):
        """Fileira de cima saindo (odot), de baixo entrando (otimes); extra_op intercala outra."""
        op0, ex = self.cut_op.get_value(), self.extra_op.get_value()
        g = VGroup()
        if op0 < 0.01:
            return g
        for zs, amp, col in ((CUT_Z, 1.0, WIRE), (CUT_EXTRA, ex, AMBER)):
            if amp < 0.01:
                continue
            for z in zs:
                x = RC * z
                if abs(x) <= X_VIS:
                    g.add(odot([x, AX_Y + RC, 0], col, op0 * amp),
                          otimes([x, AX_Y - RC, 0], col, op0 * amp))
        return g

    def cut_walls(self):
        op = self.cut_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        for sgn in (1, -1):
            y = AX_Y + sgn * RC
            g.add(Line([-X_VIS, y, 0], [X_VIS, y, 0]).set_stroke(BLUE, 3, 0.45 * op))
        return g

    def cut_field(self):
        """Campo interno (ciano): axial; até uni = 1 o valor ainda depende da fileira (não provado)."""
        op, u = self.bin_op.get_value(), self.uni.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        base = ARR_IN * (1.0 + self.extra_op.get_value()) * self.cur.get_value()
        for z in np.arange(-3, 4) * 1.0:
            x = RC * z
            for dy, f in ((-0.70, 0.62), (0.0, 1.0), (0.70, 0.80)):
                L = base * (u + (1 - u) * f)
                a = np.array([x - L / 2, AX_Y + dy, 0.0])
                g.add(vec(a, a + RIGHT * L, CYAN, 5).set_opacity(op * (0.55 + 0.45 * u)))
        return g

    def sym_marks(self):
        """Duas fatias simétricas em torno do plano de P (magenta): fatia e seções de fio."""
        op = self.sym_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        xc = self.sym_x.get_value()
        for sg in (-1, 1):
            x = xc + sg * RC * SYM_Z
            g.add(Rectangle(width=0.34, height=2 * RC + 0.5).set_stroke(width=0)
                  .set_fill(AMBER, 0.22 * op).move_to([x, AX_Y, 0]))
            for yy in (AX_Y + RC, AX_Y - RC):
                g.add(Circle(0.235, color=AMBER, stroke_width=3.5).set_stroke(opacity=op)
                      .move_to([x, yy, 0]))
        return g

    def out_field(self):
        """Campo externo: '?' enquanto desconhecido; depois setas iguais (constante) que encolhem
        com a distância; em B_fora = 0 tudo some."""
        q, b, pr = self.qout_op.get_value(), self.bout_op.get_value(), self.probe.get_value()
        g = VGroup()
        ys = (AX_Y + RC + 0.62, AX_Y + RC + 1.62)
        if q > 0.01:
            for x in (-3.08, 3.08):
                for y in ys:
                    g.add(DashedLine([x - 0.25, y, 0], [x + 0.25, y, 0], dash_length=0.08)
                          .set_stroke(WHITE, 2.5, 0.45 * q))
                    g.add(self._q.copy().set_opacity(0.7 * q).move_to([x, y + 0.26, 0]))
        if b > 0.01:
            for x in (-3.0, 3.0):
                for y in ys:
                    g.add(vec([x - 0.28, y, 0], [x + 0.28, y, 0], CYAN, 4).set_opacity(0.6 * b))
            y0, L = self.amp_y.get_value(), 0.6 * max(0.03, 1.0 - 0.95 * pr)
            for dy in (-RECT_H / 2, RECT_H / 2):
                g.add(vec([0.5 - L / 2, y0 + dy, 0], [0.5 + L / 2, y0 + dy, 0], CYAN, 4)
                      .set_opacity(b * (1.0 - 0.85 * pr)))
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
            g.add(Line([-w2, yy, 0], [w2, yy, 0]).set_stroke(MAGENTA, 2 + 4.5 * a, op * (0.25 + 0.75 * a)))
        for a, s in ((self.actL.get_value(), -1), (self.actR.get_value(), 1)):
            g.add(Line([s * w2, y - h2, 0], [s * w2, y + h2, 0])
                  .set_stroke(MAGENTA, 2 + 4.5 * a, op * (0.25 + 0.75 * a)))
        return g

    def amp_dirs(self):
        """Sentido do percurso (d l), anti-horário: lado de baixo em +x, lado de cima em -x."""
        op = self.amp_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        y = self.amp_y.get_value()
        g.add(vec([-1.95, y - RECT_H / 2, 0], [-1.05, y - RECT_H / 2, 0], MAGENTA, 5).set_opacity(op))
        g.add(vec([-1.05, y + RECT_H / 2, 0], [-1.95, y + RECT_H / 2, 0], MAGENTA, 5).set_opacity(op))
        g.add(self._dl.copy().set_opacity(op).move_to([-1.5, y - RECT_H / 2 + 0.34, 0]))
        return g

    def amp_sides(self):
        """Rótulos rho1 (lado de baixo, mais perto do eixo) e rho2 (lado de cima)."""
        op = self.side_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        y = self.amp_y.get_value()
        for lab, dy in ((self._r1, -RECT_H / 2), (self._r2, RECT_H / 2)):
            g.add(lab.copy().set_opacity(op).move_to([-RECT_W / 2 - 0.5, y + dy, 0]))
        return g

    def ell_mark(self):
        """Cota do comprimento l, acima do lado de cima do retângulo."""
        op = self.ell_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        y = self.amp_y.get_value() + RECT_H / 2 + 0.28
        g.add(span_mark(np.array([-RECT_W / 2, y, 0]), np.array([RECT_W / 2, y, 0]), MAGENTA, op=op))
        g.add(self._ell.copy().set_opacity(op).move_to([0, y + 0.24, 0]))
        return g

    def enc_marks(self):
        """Seções de fio enlaçadas (magenta), marcadas em sequência: uma única fileira, N_l = n l."""
        k = self.enc_n.get_value()
        g = VGroup()
        if k < 0.01:
            return g
        for i, z in enumerate(ENC_Z):
            op = float(np.clip(k - i, 0.0, 1.0))
            if op > 0.01:
                g.add(Circle(0.235, color=AMBER, stroke_width=3.5).set_stroke(opacity=op)
                      .move_to([RC * z, AX_Y + RC, 0]))
        return g

    def dz_mark(self):
        """Delta z: distância axial entre a espira em destaque e o ponto P (violeta, medida geométrica)."""
        op, foc = self.dz_op.get_value(), self.focus.get_value()
        g = VGroup()
        if op < 0.01 or foc < 0:
            return g
        pos, _ = self.turn_pos()
        j = int(round(foc))
        if j >= len(pos):
            return g
        rs, cx, ay = self.rs.get_value(), self.cx.get_value(), self.ay.get_value()
        xt, xp, y = cx + rs * pos[j], self.px(), ay + rs + 0.22
        if abs(xt - xp) < 0.12:
            g.add(self._dz0.copy().set_opacity(op).move_to([xp, y + 0.2, 0]))
            return g
        g.add(span_mark(np.array([xp, y, 0]), np.array([xt, y, 0]), VIOLET, op=0.9 * op))
        g.add(self._dzl.copy().set_opacity(op).move_to([(xp + xt) / 2, y + 0.3, 0]))
        return g

    # ── Expressões ──────────────────────────────────────────────────────────
    @staticmethod
    def sum_expr(k):
        """B(P) = B_1 + ... : partes em ordem, de modo que k -> k+1 só ACRESCENTA partes no fim."""
        parts = ["B(P)", "=", "B_1(P)"]
        for i in range(2, min(k, 3) + 1):
            parts += ["+", f"B_{i}(P)"]
        if k >= 4:
            parts += ["+", r"\cdots"]
        m = mtex(*parts, size=48)
        m[0].set_color(CYAN)
        for p in m[2:]:
            if p.tex_string.startswith("B_"):
                p.set_color(CYAN)
        return fit(m).move_to([0, SUP_OP_Y, 0])

    # ── Sincronia com a narração ────────────────────────────────────────────
    # Cada self.ancora("x") casa um ponto do código com um instante da fala (sync.json). Entre
    # duas âncoras, play/wait são escalados para o trecho durar o que a fala dura; se a cena
    # acabar antes, a âncora seguinte segura o último quadro. native.json guarda o tempo NATIVO
    # de cada âncora (SYNC_CAL=1 regenera; sem os dois arquivos a cena roda em tempo nativo).
    def sync_init(self):
        self.tscale, self.nativos = 1.0, {}
        arq = PASTA / "sync.json"
        self.anc = json.load(open(arq))["anchors"] if arq.exists() else []
        nat = PASTA / "native.json"
        self.nat = json.load(open(nat)) if nat.exists() and not CAL else {}

    def _quadro(self, t):
        """Duração em quadros inteiros (o Manim arredonda para cima)."""
        fps = config.frame_rate
        return max(1, round(t * fps)) / fps

    def play(self, *args, **kwargs):
        if abs(self.tscale - 1.0) > 1e-6 and args and not getattr(self, "_cru", False):
            anims = self.compile_animations(*args, **kwargs)
            for a in anims:
                a.run_time = self._quadro(a.run_time * self.tscale)
            return super().play(*anims)
        return super().play(*args, **kwargs)

    def esperar_cru(self, duracao):
        """Espera SEM escala: Scene.wait chama self.play, que escalaria de novo."""
        self._cru = True
        try:
            Scene.wait(self, duracao)
        finally:
            self._cru = False

    def wait(self, duration=1.0, *a, **k):
        self.esperar_cru(self._quadro(duration * self.tscale))

    def ancora(self, nome):
        agora = self.renderer.time
        if CAL:
            self.nativos[nome] = round(agora, 3)
            if nome == "fim":
                json.dump(self.nativos, open(PASTA / "native.json", "w"), indent=1)
            return
        if not self.anc or nome not in self.nat:
            return
        nomes = [n for n, _ in self.anc]
        i = nomes.index(nome)
        t_a = self.anc[i][1]
        if agora < t_a:
            self.esperar_cru(t_a - agora)
            agora = t_a
        elif agora - t_a > 0.25:
            print("SYNC atraso %.2f s em %s" % (agora - t_a, nome))
        if i + 1 < len(self.anc):
            prox, t_prox = self.anc[i + 1]
            gap_nat = max(0.2, self.nat[prox] - self.nat[nome])
            self.tscale = float(np.clip((t_prox - agora) / gap_nat * 0.985, 0.45, 2.0))
        else:
            self.tscale = 1.0

    # ── Cena ────────────────────────────────────────────────────────────────
    def construct(self):
        self.start_frame()
        self.sync_init()
        watermark = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(watermark.to_corner(UP + RIGHT, buff=0.28))
        series = text("DA EQUAÇÃO AO FENÔMENO · EP. 03", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4)

        T = ValueTracker
        self.nt, self.slide, self.tilt, self.cont = T(1.0), T(1.0), T(TILT0), T(0.0)
        self.rs, self.ay, self.cx = T(RS), T(AY_S), T(0.0)
        self.coil_op, self.cur_op, self.bres_op, self.p_op = T(0), T(0), T(0), T(0)
        self.chain_op, self.tie_op, self.focus, self.pz = T(0), T(0), T(-1), T(0.0)
        self.arr_k, self.cur, self.glow = T(ARR_S), T(1.0), T(0.0)
        self.span_op, self.ext_op, self.curve_op, self.mark_op, self.ends_op = (T(0) for _ in range(5))
        self.cut_op, self.extra_op, self.bin_op, self.uni = T(0), T(0), T(0), T(0)
        self.qout_op, self.bout_op, self.probe = T(0), T(0), T(0)
        self.sym_op, self.sym_x, self.curve_follow, self.dz_op = T(0), T(0.0), T(0), T(0)
        self._state = None
        self.amp_op, self.amp_y, self.side_op = T(0), T(Y_OUT), T(0)
        self.ell_op, self.enc_n = T(0), T(0)
        self.act1, self.act2, self.actL, self.actR = (T(0) for _ in range(4))
        self._plab, self._llab = plate(tex("P", 28, WHITE)), plate(tex("L", 30, VIOLET))
        self._q, self._dl = tex("?", 30), plate(tex(r"d\vec\ell", 36, MAGENTA))
        self._r1, self._r2 = plate(tex(r"\rho_1", 46, MAGENTA)), plate(tex(r"\rho_2", 46, MAGENTA))
        self._ell = plate(tex(r"\ell", 44, MAGENTA))
        self._dzl, self._dz0 = plate(tex(r"\Delta z", 34, VIOLET)), plate(tex(r"\Delta z=0", 32, VIOLET))

        R = always_redraw
        ext, sheet, coil, marks = R(self.ext_lines), R(self.coil_cont), R(self.coil), R(self.current_marks)
        rows, walls, cfield, symm = R(self.cut_rows), R(self.cut_walls), R(self.cut_field), R(self.sym_marks)
        outf, span, ties, chain = R(self.out_field), R(self.len_span), R(self.chain_ties), R(self.chain)
        parr, pdot, dzm = R(self.p_arrow), R(self.p_dot), R(self.dz_mark)
        curve, gmark, gends = R(self.graph_curve), R(self.graph_mark), R(self.graph_ends)
        rect, dirs, sides = R(self.amp_rect), R(self.amp_dirs), R(self.amp_sides)
        ell, enc = R(self.ell_mark), R(self.enc_marks)
        self.add(ext, sheet, coil, marks, rows, walls, symm, cfield, outf, span, ties, chain, parr, pdot, dzm,
                 curve, gmark, gends, rect, dirs, sides, ell, enc)
        self.bleed = [series, coil, sheet, marks, ext, rows, walls, cfield, span, enc, symm, outf]
        self.add(series)

        def mt(*parts, size=48):
            return MathTex(*parts, font_size=size, color=WHITE)

        def nm(expr, size=34):
            """Nota com matemática (a fonte do texto não tem μ, ρ, ⇒, ≫): MathTex ajustada à largura."""
            return fit(MathTex(expr, font_size=size, color=WHITE).set_opacity(0.94), 6.5)

        def swap(old, new):
            """Troca o(s) grupo(s) antigo(s), já transformado(s) sobre o novo, pelo novo sem duplicar partes."""
            for o in (old if isinstance(old, (list, tuple)) else [old]):
                self.remove(o)
            self.remove(*new)
            self.add(new)

        def sweep():
            """Varre órfãos: o '=' de uma expressão que um Transform deixou solto no nível da cena."""
            for m in list(self.mobjects):
                if getattr(m, "tex_string", None) == "=":
                    self.remove(m)

        def mk_state(kind):
            """O resultado de estado da vez, em tamanho legível (um por vez)."""
            if kind == "sym":
                m = mt(r"\vec B", "=", "B", r"(\rho)", r"\,\hat z", size=38)
                m[0].set_color(CYAN)
                m[2].set_color(CYAN)
                m[3].set_color(MAGENTA)
            elif kind == "out":
                m = mt(r"B_{\text{fora}}", "=", "0", size=42)
                m[0].set_color(CYAN)
            else:
                m = mt(r"B_{\text{dentro}}", "=", r"\text{constante}", size=42)
                m[0].set_color(CYAN)
            return m

        def set_state(new):
            new.move_to([0, SHELF_Y, 0])
            old, self._state = self._state, new
            return [soft_swap(old, new)] if old is not None else [FadeIn(new, shift=UP * 0.1)]

        # eixos do gráfico (estáticos: a curva é que se move com cx, rs e nt)
        axes = VGroup(
            Line([G_XL, G_Y0, 0], [G_XR, G_Y0, 0]).set_stroke(WHITE, 2, 0.45),
            Line([G_XL, G_Y0, 0], [G_XL, G_Y0 + G_H + 0.35, 0]).set_stroke(WHITE, 2, 0.45),
            DashedLine([G_XL, G_Y0 + G_H, 0], [G_XR, G_Y0 + G_H, 0], dash_length=0.1).set_stroke(WHITE, 1.8, 0.35),
            tex("1", 26).set_opacity(0.8).next_to([G_XL, G_Y0 + G_H, 0], LEFT, 0.1),
            tex(r"B/\mu_0 n I", 28, CYAN).set_opacity(0.9).move_to([G_XL + 1.0, G_Y0 + G_H + 0.55, 0]),
            tex("z", 30, BLUE).set_opacity(0.8).move_to([G_XR - 0.05, G_Y0 - 0.30, 0]),
        )
        half_line = VGroup(
            DashedLine([G_XL, G_Y0 + G_H / 2, 0], [G_XR, G_Y0 + G_H / 2, 0], dash_length=0.1)
            .set_stroke(VIOLET, 1.8, 0.6),
            tex(r"\tfrac12", 26, VIOLET).next_to([G_XL, G_Y0 + G_H / 2, 0], LEFT, 0.1),
        )

        # ══ B1. Retomada: uma espira ═══════════════════════════════════════════════════════════════
        self.ancora("a00")
        self.play(FadeIn(series), *self.caption("UMA ESPIRA,", "A GENTE JÁ ENTENDEU."),
                  self.coil_op.animate.set_value(1), self.cur_op.animate.set_value(1), run_time=0.80)
        ep8 = mt(r"B_{\text{esp}}(\Delta z)", "=", r"\frac{\mu_0 I R^2}{2\left(R^2+\Delta z^2\right)^{3/2}}", size=38)
        ep8[0].set_color(CYAN)
        ep8[2][2].set_color(AMBER)
        ep8.move_to([0, TOP_Y, 0])
        self.play(FadeIn(ep8, shift=UP * 0.1), self.p_op.animate.set_value(1),
                  self.bres_op.animate.set_value(1), run_time=0.70)
        self.note(tag("campo no eixo — do episódio anterior", 23, 0.9))
        self.check_safe()
        self.wait(1.45)

        # ══ B2. Cada espira entrega a sua parcela B_j ══════════════════════════════════════════════
        self.ancora("a01")
        self.play(*self.caption("E SE FOREM MUITAS?"), self.chain_op.animate.set_value(1), self.dz_op.animate.set_value(1),
                  self.tie_op.animate.set_value(1), run_time=0.60)

        def fly_label(k):
            """A parcela B_k nasce perto da espira k (que acende em magenta)."""
            return tex(f"B_{k}(P)", 40, CYAN).move_to([RS * order_turns(k)[0][k - 1], 0.55, 0])

        s1 = self.sum_expr(1)
        fly = fly_label(1)
        self.play(self.focus.animate.set_value(0), FadeIn(fly, scale=0.5), run_time=0.9)
        self.note(nm(r"\text{esta espira contribui com }B_1"), run_time=0.6)
        self.wait(0.20)
        self.play(Transform(fly, s1[2]), FadeIn(s1[0]), FadeIn(s1[1]),
                  self.focus.animate.set_value(-1), run_time=1.3)
        swap(fly, s1)
        self.wait(0.30)

        s2 = self.sum_expr(2)
        self.ancora("a02")
        self.play(self.nt.animate.set_value(2), self.focus.animate.set_value(1), run_time=1.4)
        fly = fly_label(2)
        self.play(FadeIn(fly, scale=0.5), run_time=0.8)
        self.note(tag("mesma espira, outra distância até P", 21, 0.9), run_time=0.4)
        self.play(*[Transform(s1[i], s2[i]) for i in range(3)], FadeIn(s2[3]), Transform(fly, s2[4]),
                  self.focus.animate.set_value(-1), run_time=1.3)
        swap([s1, fly], s2)
        self.wait(0.30)
        self.check_safe()

        s3 = self.sum_expr(3)
        self.ancora("a02b")
        self.play(self.nt.animate.set_value(3), self.focus.animate.set_value(2), run_time=1.1)
        fly = fly_label(3)
        self.play(FadeIn(fly, scale=0.5), run_time=0.8)
        self.note(tag("cada nova espira soma uma nova parcela", 23, 0.9), run_time=0.4)
        self.play(*[Transform(s2[i], s3[i]) for i in range(5)], FadeIn(s3[5]), Transform(fly, s3[6]),
                  self.focus.animate.set_value(-1), run_time=1.2)
        swap([s2, fly], s3)
        self.wait(0.30)

        s4 = self.sum_expr(4)
        self.ancora("a03")
        self.note(None, run_time=0.4)
        self.play(self.nt.animate.set_value(NT_SUP), *[Transform(s3[i], s4[i]) for i in range(7)],
                  FadeIn(s4[7]), FadeIn(s4[8]), run_time=1.7, rate_func=linear)
        swap(s3, s4)
        self.note(tag("cada espira contribui menos quanto mais longe de P", 21, 0.9),
                  self.focus.animate.set_value(NT_SUP - 1), run_time=0.6)
        self.check_safe()
        self.wait(0.45)

        # B1 + B2 + B3 + ... se compacta em Sum: as parcelas convergem e as sobras encolhem no lugar
        s5 = mt("B(P)", "=", r"\sum_j", "B_j(P)", size=48).move_to([0, SUP_OP_Y, 0])
        s5[0].set_color(CYAN)
        s5[3].set_color(CYAN)
        gather, stale = [s4[2], s4[4], s4[6]], [s4[3], s4[5], s4[7], s4[8]]
        self.ancora("a04")
        self.play(self.focus.animate.set_value(-1),
                  *[m.animate.move_to(s5[3].get_center()).scale(0.5).set_opacity(0) for m in gather],
                  *[m.animate.scale(0.4).set_opacity(0) for m in stale],
                  Transform(s4[0], s5[0]), Transform(s4[1], s5[1]), run_time=1.0)
        self.play(FadeIn(s5[2]), FadeIn(s5[3], scale=1.3), run_time=0.7)
        swap(s4, s5)
        self.wait(0.30)
        s6 = mt("B(z)", "=", r"\sum_j", "B_j(z)", size=48).move_to([0, SUP_OP_Y, 0])
        s6[0].set_color(CYAN)
        s6[3].set_color(CYAN)
        box6 = SurroundingRectangle(s6, color=WHITE, buff=0.24, corner_radius=0.08, stroke_width=2.5)
        self.note(tag("em qualquer ponto do eixo", 22, 0.9),
                  *[Transform(s5[i], s6[i]) for i in range(4)], Create(box6), run_time=1.1)
        swap(s5, s6)
        self.check_safe()
        self.wait(0.50)

        # ══ B3. Soma discreta -> contínua: a fatia dz contém dN = n dz espiras ═════════════════════
        nlab = mt("n", "=", "N", "/", "L", size=44).move_to([-1.6, 0.28, 0])
        nlab[0].set_color(AMBER)
        nlab[2].set_color(AMBER)
        nlab[4].set_color(VIOLET)
        self.ancora("a05")
        self.play(*self.caption("MUITAS ESPIRAS,", "BEM PRÓXIMAS"), self.chain_op.animate.set_value(0), self.dz_op.animate.set_value(0),
                  self.tie_op.animate.set_value(0), self.cur_op.animate.set_value(0),
                  self.span_op.animate.set_value(1), run_time=0.9)
        self.play(self.cont.animate.set_value(1.0), run_time=1.5)
        self.note(tag("espiras muito próximas → enrolamento contínuo", 21, 0.9), run_time=0.6)
        self.wait(0.70)
        self.ancora("a06")
        self.note(nm(r"n:\;\text{espiras por unidade de comprimento}"),
                  FadeIn(nlab), run_time=0.8)
        self.wait(0.85)
        self.ancora("a07")
        SLX, SLW = 1.5, 0.42
        slice_ = Rectangle(width=SLW, height=2 * RS).set_stroke(width=0).set_fill(AMBER, 0.35)
        slice_.move_to([SLX, AY_S, 0])
        brk = span_mark(np.array([SLX - SLW / 2, 0.45, 0]), np.array([SLX + SLW / 2, 0.45, 0]), VIOLET, 0.09)
        dzl = tex(r"dz^{\prime}", 32, VIOLET).move_to([SLX, 0.12, 0])
        self.note(nm(r"\text{uma fatia de largura }dz^{\prime}"), FadeIn(slice_), Create(brk),
                  FadeIn(dzl), run_time=0.9)
        self.wait(0.40)
        eqdN = mt("dN", "=", "n", r"\,dz^{\prime}", size=46).move_to([0, -0.3, 0])
        eqdN[0].set_color(AMBER)
        eqdN[2].set_color(AMBER)
        eqdN[3].set_color(VIOLET)
        self.play(TransformFromCopy(dzl, eqdN[3]), FadeIn(eqdN[0]), FadeIn(eqdN[1]), FadeIn(eqdN[2]),
                  run_time=1.0)
        self.remove(*eqdN)
        self.add(eqdN)
        self.note(nm(r"\text{essa fatia contém }dN=n\,dz^{\prime}\text{ espiras}"), run_time=0.6)
        self.check_safe()
        self.wait(0.50)

        dzs = span_mark(np.array([0.0, AY_S - 0.45, 0]), np.array([SLX, AY_S - 0.45, 0]), VIOLET, 0.09)
        dzlab = plate(tex(r"\Delta z = z - z^{\prime}", 30, VIOLET)).move_to([SLX / 2, AY_S - 0.85, 0])
        self.note(nm(r"P\text{ em }z;\;\text{fatia em }z^{\prime}"), Create(dzs), FadeIn(dzlab), run_time=0.9)
        self.wait(0.4)

        # cada linha SUBSTITUI a anterior: a fatia contribui com B_esp vezes dN
        self.ancora("a08")
        row2 = mt("dB(z)", "=", r"B_{\text{esp}}(z-z^{\prime})", "dN", size=44).move_to([0, -1.55, 0])
        row2[0].set_color(CYAN)
        row2[2].set_color(CYAN)
        row2[3].set_color(AMBER)
        self.note(nm(r"dN\text{ espiras}\to dB=B_{\text{esp}}\,dN"), FadeOut(box6), FadeOut(ep8),
                  Transform(s6[0], row2[0]), Transform(s6[1], row2[1]), Transform(s6[3], row2[2]),
                  s6[2].animate.scale(0.4).set_opacity(0), TransformFromCopy(eqdN[0], row2[3]), run_time=1.2)
        swap(s6, row2)
        self.wait(0.15)
        row3 = mt("dB(z)", "=", r"B_{\text{esp}}(z-z^{\prime})", r"\,n", r"\,dz^{\prime}", size=44)
        row3.move_to([0, -1.55, 0])
        row3[0].set_color(CYAN)
        row3[2].set_color(CYAN)
        row3[3].set_color(AMBER)
        row3[4].set_color(VIOLET)
        self.note(nm(r"\text{substituindo }dN=n\,dz^{\prime}"), *[Transform(row2[i], row3[i]) for i in range(3)],
                  row2[3].animate.scale(0.5).set_opacity(0), TransformFromCopy(eqdN[2], row3[3]),
                  TransformFromCopy(eqdN[3], row3[4]), run_time=1.2)
        swap(row2, row3)
        self.wait(0.15)
        row4 = mt("dB(z)", "=", r"\frac{\mu_0 n I R^2}{2}",
                  r"\frac{dz^{\prime}}{\left[R^2+(z-z^{\prime})^2\right]^{3/2}}", size=40)
        fit(row4, 6.9).move_to([0, -1.55, 0])
        row4[0].set_color(CYAN)
        row4[2][2].set_color(AMBER)
        row4[2][3].set_color(AMBER)
        for k in range(3):
            row4[3][k].set_color(VIOLET)
        rest = VGroup(*[row4[2][i] for i in (0, 1, 3, 4, 5, 6, 7)], *list(row4[3][3:]))
        self.note(tag("substituindo o campo de uma espira", 22, 0.9), FadeOut(eqdN), FadeOut(nlab), FadeOut(dzs), FadeOut(dzlab),
                  Transform(row3[0], row4[0]), Transform(row3[1], row4[1]), Transform(row3[2], rest),
                  Transform(row3[3], row4[2][2]), Transform(row3[4], VGroup(*row4[3][0:3])), run_time=1.5)
        swap(row3, row4)
        self.check_safe()
        self.wait(0.20)

        # B(z) = Int dB, e a integral final: a expressão se abre no mesmo lugar, sem pilha de linhas
        row5 = mt("B(z)", "=", r"\int", "dB", size=50).move_to([0, -1.55, 0])
        row5[0].set_color(CYAN)
        row5[3].set_color(CYAN)
        self.note(tag("somando todas as fatias", 23, 0.9), Transform(row4[0], row5[0]),
                  Transform(row4[1], row5[1]), row4[2].animate.move_to(row5[3]).scale(0.3).set_opacity(0),
                  row4[3].animate.move_to(row5[3]).scale(0.3).set_opacity(0), FadeIn(row5[2]),
                  FadeIn(row5[3], scale=1.4), run_time=1.3)
        swap(row4, row5)
        self.wait(0.15)
        integ = mt("B(z)", "=", r"\frac{\mu_0 n I R^2}{2}", r"\int_{-L/2}^{L/2}",
                   r"\frac{dz^{\prime}}{\left[R^2+(z-z^{\prime})^2\right]^{3/2}}", size=40)
        fit(integ, 6.9).move_to([0, -1.55, 0])
        integ[0].set_color(CYAN)
        integ[2][2].set_color(AMBER)
        integ[2][3].set_color(AMBER)
        for k in range(3):
            integ[4][k].set_color(VIOLET)
        self.note(tag("o somatório virou uma integral", 23, 0.9), Transform(row5[0], integ[0]),
                  Transform(row5[1], integ[1]), Transform(row5[2], integ[3]),
                  Transform(row5[3], VGroup(integ[2], integ[4])), run_time=1.6)
        swap(row5, integ)
        self.check_safe()
        self.ancora("a09")
        self.wait(1.40)
        # ponte: a integral, calculada em cada z, é o perfil B(z) que vamos desenhar
        ibox = SurroundingRectangle(integ, color=WHITE, buff=0.24, corner_radius=0.08, stroke_width=2.5)
        self.note(nm(r"\text{essa integral determina o perfil de }B(z)"), Create(ibox), run_time=0.8)
        self.wait(1.00)

        # ══ B4. A integral, calculada em cada z, desenha o perfil no eixo ══════════════════════════
        self.play(FadeOut(ibox), run_time=0.3)
        self.play(*self.caption("O CAMPO AO LONGO DO EIXO"), FadeOut(VGroup(slice_, brk, dzl)),
                  FadeOut(self.hint), integ.animate.scale(0.82).move_to([0, TOP_Y, 0]),
                  self.rs.animate.set_value(RG), self.ay.animate.set_value(AY_G),
                  self.arr_k.animate.set_value(ARR_G), run_time=1.3)
        self.hint = None
        self.note(nm(r"\text{avaliando a integral em cada }z"), FadeIn(axes), self.ends_op.animate.set_value(1),
                  self.mark_op.animate.set_value(1), self.pz.animate.set_value(-5.0), run_time=1.0)
        self.curve_follow.set_value(1)
        self.curve_op.set_value(1)
        self.check_safe()
        self.ancora("a10")
        self.note(nm(r"\text{longe da bobina: }B\text{ pequeno}"), self.pz.animate.set_value(-3.6),
                  run_time=1.3)
        self.ancora("a10b")
        self.note(nm(r"\text{perto da entrada: }B\text{ cresce rápido}"),
                  self.pz.animate.set_value(-NT_SUP * PITCH / 2), run_time=1.2)
        self.ancora("a10c")
        self.note(nm(r"\text{no centro: }B\text{ é máximo}"), self.pz.animate.set_value(0.0), run_time=1.1)
        self.check_safe()
        self.ancora("a10d")
        self.note(nm(r"\text{na saída: }B\text{ cai novamente}"), self.pz.animate.set_value(6.0),
                  run_time=2.0)
        self.curve_follow.set_value(0)
        self.play(self.pz.animate.set_value(0.0), run_time=0.9)
        self.wait(0.60)

        # ══ B5. L/R cresce com R e n FIXOS: geometria, gráfico e álgebra contam a mesma história ═══
        def ratio(rhs_parts, size=36):
            m = mt(r"\frac{B(0)}{\mu_0 n I}", "=", *rhs_parts, size=size)
            for k in range(4):
                m[0][k].set_color(CYAN)
            m[0][7].set_color(AMBER)
            m[0][8].set_color(AMBER)
            m[2].set_color(VIOLET)
            return m.move_to([0, TOP_Y + 0.35, 0])

        cform1 = ratio([r"\frac{L}{\sqrt{L^2+4R^2}}"])
        lr4 = mt(r"L/R=4{,}5", size=30).set_color(VIOLET).move_to([1.9, G_Y0 + G_H + 0.55, 0])
        fix_tag = text("R e n fixos: só L cresce", 21, WHITE, 0.9).move_to([0, 3.85, 0])
        pre = mt(r"z=0", r"\Rightarrow", r"B(0)=\mu_0 n I\,\frac{L}{\sqrt{L^2+4R^2}}", size=34)
        for k in range(4):
            pre[2][k].set_color(CYAN)
        pre[2][7].set_color(AMBER)
        pre[2][8].set_color(AMBER)
        pre.move_to([0, TOP_Y + 0.35, 0])
        self.ancora("a11")
        self.play(*self.caption("E SE A BOBINA", "FOR MAIS LONGA?"), Transform(integ, pre), FadeOut(self.hint),
                  run_time=1.2)
        self.hint = None
        self.note(nm(r"\text{no centro: }z=0"))
        self.wait(1.3)
        self.play(FadeOut(integ, shift=UP * 0.1), FadeIn(cform1, shift=UP * 0.1), FadeIn(lr4), FadeIn(fix_tag),
                  run_time=1.0)
        self.note(None)
        self.wait(0.70)
        cform2 = ratio([r"\frac{1}{\sqrt{1+4(R/L)^2}}"])
        self.note(nm(r"\text{dividindo por }L\text{: sobra }R/L"), Transform(cform1[2], cform2[2]), run_time=1.0)
        swap(cform1, cform2)
        self.wait(0.50)
        lr10 = mt(r"L/R=10{,}5", size=30).set_color(VIOLET).move_to(lr4)
        self.ancora("a12b")
        self.note(nm(r"L/R\uparrow:\;\text{a região central fica mais plana}"), self.nt.animate.set_value(NT_LONG),
                  Transform(lr4, lr10), run_time=2.4)
        self.check_safe()
        self.wait(0.50)
        cform3 = mt(r"\frac{B(0)}{\mu_0 n I}", r"\xrightarrow{\;L/R\to\infty\;}", r"\frac{1}{\sqrt{1+0}}", "=", "1",
                    size=34)
        for k in range(4):
            cform3[0][k].set_color(CYAN)
        cform3[0][7].set_color(AMBER)
        cform3[0][8].set_color(AMBER)
        cform3[2].set_color(VIOLET)
        cform3[4].set_color(CYAN)
        cform3.move_to([0, TOP_Y + 0.35, 0])
        self.ancora("a12c")
        self.note(nm(r"L/R\to\infty\;\Rightarrow\;R/L\to0\;\Rightarrow\;\frac{B(0)}{\mu_0 n I}\to1", 28),
                  Transform(cform2[0], cform3[0]), Transform(cform2[1], cform3[1]),
                  Transform(cform2[2], cform3[2]), FadeIn(cform3[3]), FadeIn(cform3[4]), run_time=1.3)
        swap(cform2, cform3)
        self.wait(0.95)
        self.ancora("a13")
        self.note(nm(r"\text{na ponta de uma bobina longa: }B\to\tfrac12\,\mu_0 n I"),
                  self.pz.animate.set_value(NT_LONG * PITCH / 2), FadeIn(half_line), FadeOut(fix_tag),
                  run_time=1.2)
        self.check_safe()
        self.wait(0.70)

        # ══ B6. O limite ideal: modelo infinito ════════════════════════════════════════════════════
        ideal = tag("MODELO IDEAL · ENROLAMENTO CONTÍNUO E INFINITO", 20, 0.9, VIOLET).move_to([0, 4.85, 0])
        self.ancora("a14")
        self.play(*self.caption("O LIMITE IDEAL"), FadeOut(cform3), FadeOut(half_line),
                  self.pz.animate.set_value(0.0), run_time=0.6)
        self.note(nm(r"L/R\to\infty:\;\text{modelo infinito}"), self.nt.animate.set_value(NT_INF),
                  FadeOut(lr4), run_time=1.5)
        self.play(FadeOut(axes), self.curve_op.animate.set_value(0), self.mark_op.animate.set_value(0),
                  self.ends_op.animate.set_value(0), self.span_op.animate.set_value(0),
                  self.p_op.animate.set_value(0), self.bres_op.animate.set_value(0), run_time=0.6)
        self.play(self.rs.animate.set_value(RC), self.ay.animate.set_value(AX_Y),
                  self.tilt.animate.set_value(0.0), run_time=1.1)
        self.play(self.cut_op.animate.set_value(1), self.coil_op.animate.set_value(0),
                  self.bin_op.animate.set_value(1), self.qout_op.animate.set_value(1), FadeIn(ideal),
                  run_time=0.7)
        self.note_y, self.op_y = AMP_NOTE_Y, AMP_OP_Y
        self.ancora("a15")
        self.note(tag("modelo infinito: simetria perfeita, resultado exato", 21, 0.9))
        self.check_safe()
        self.wait(0.40)

        # ══ B7. Simetria: as partes transversais se cancelam ═══════════════════════════════════════
        rh1 = VGroup(odot(ORIGIN, WIRE), text("corrente saindo", 20, opacity=0.85)
                     ).arrange(RIGHT, buff=0.18).move_to([0, AX_Y + RC + 0.60, 0])
        rh2 = VGroup(otimes(ORIGIN, WIRE), text("corrente entrando", 20, opacity=0.85)
                     ).arrange(RIGHT, buff=0.18).move_to([0, AX_Y - RC - 0.60, 0])
        self.play(*self.caption("O QUE A SIMETRIA EXIGE"), FadeIn(rh1), FadeIn(rh2), run_time=0.6)
        self.note(tag("mão direita: dentro, o campo aponta para a direita", 21, 0.9))
        self.check_safe()
        self.wait(0.40)
        ps = np.array([0.0, AX_Y + 0.70, 0.0])
        ca, ct = 1.08, 0.59                       # dB = 1,1 a 29°: parte axial e parte transversal
        pdot7 = Dot(ps, 0.09, color=WHITE)
        rmark = span_mark(np.array([0.0, AX_Y, 0.0]), ps, MAGENTA, 0.08, 2.2, 0.9)
        rlab = tex(r"\rho", 30, MAGENTA).next_to(rmark, LEFT, 0.12)
        plane = DashedLine([0, AX_Y - RC - 0.45, 0], [0, AX_Y + RC + 0.45, 0],
                           dash_length=0.1).set_stroke(WHITE, 2, 0.5)
        dB1 = vec(ps, ps + np.array([ca, ct, 0]), CYAN, 4)
        dB2 = vec(ps, ps + np.array([ca, -ct, 0]), CYAN, 4)
        self.ancora("a16")
        self.play(FadeOut(VGroup(rh1, rh2)), self.bin_op.animate.set_value(0.25),
                  self.sym_op.animate.set_value(1), FadeIn(VGroup(pdot7, rmark, rlab)), Create(plane),
                  run_time=0.7)
        self.note(tag("duas fatias simétricas em torno do plano de P", 22, 0.9), Create(dB1), Create(dB2),
                  run_time=0.8)
        ax1 = vec(ps, ps + np.array([ca, 0, 0]), CYAN, 6)
        t_up = vec(ps, ps + np.array([0, ct, 0]), VIOLET, 5)
        t_dn = vec(ps, ps + np.array([0, -ct, 0]), VIOLET, 5)
        self.note(tag("cada contribuição tem uma parte axial e outra transversal", 21, 0.9),
                  dB1.animate.set_opacity(0.3), dB2.animate.set_opacity(0.3), Create(ax1), Create(t_up),
                  Create(t_dn), run_time=0.9)
        self.wait(0.25)
        cancel = mt(r"d\vec B_{\perp}", "+", r"(-d\vec B_{\perp})", "=", "0", size=38).move_to([0, -1.1, 0])
        cancel[0].set_color(VIOLET)
        cancel[2].set_color(VIOLET)
        self.ancora("a17")
        self.note(tag("as transversais se cancelam par a par", 22, 0.9), t_dn.animate.shift(UP * ct),
                  FadeIn(cancel, shift=UP * 0.1), run_time=0.9)
        self.play(FadeOut(VGroup(t_up, t_dn)), run_time=0.4)
        ax2 = ax1.copy()
        tot = vec(ps, ps + np.array([2 * ca, 0, 0]), CYAN, 8)
        self.add(ax2)
        self.ancora("a17b")
        self.note(tag("as axiais apontam no mesmo sentido e se somam", 22, 0.9), ax2.animate.shift(RIGHT * ca),
                  run_time=0.7)
        self.play(Transform(ax1, tot), FadeOut(ax2), FadeOut(VGroup(dB1, dB2)), run_time=0.6)
        self.note(tag("o que sobra é o campo axial", 23, 0.9))
        self.wait(0.35)

        # a geometria em torno de P é a mesma em qualquer z: só vale no modelo infinito
        mover = VGroup(pdot7, rmark, rlab, plane, ax1)
        self.ancora("a18")
        self.note(tag("modelo infinito: deslocar P ao longo do eixo não muda o sistema", 21, 0.9),
                  mover.animate.shift(RIGHT * RC), self.sym_x.animate.set_value(RC), run_time=0.6)
        self.play(mover.animate.shift(LEFT * 2 * RC), self.sym_x.animate.set_value(-RC), run_time=0.9)
        self.play(mover.animate.shift(RIGHT * RC), self.sym_x.animate.set_value(0.0), run_time=0.6)
        sym = mt(r"\vec B", "=", "B", r"(\rho)", r"\,\hat z", size=50).move_to([0, AMP_OP_Y, 0])
        sym[0].set_color(CYAN)
        sym[2].set_color(CYAN)
        sym[3].set_color(MAGENTA)
        symbox = SurroundingRectangle(sym, color=WHITE, buff=0.24, corner_radius=0.08, stroke_width=2.5)
        self.ancora("a18b")
        self.play(FadeIn(VGroup(sym, symbox), shift=UP * 0.1), FadeOut(VGroup(mover, cancel)),
                  self.sym_op.animate.set_value(0), self.bin_op.animate.set_value(1.0), run_time=0.7)
        self.note(nm(r"B\text{ depende só da distância }\rho\text{ ao eixo}", 28))
        self.check_safe()
        self.wait(0.70)

        # ══ B8. Ampère: cada lado do contorno entrega o seu termo ══════════════════════════════════
        law = mt(r"\oint", r"\vec B", r"\cdot", r"d\vec\ell", "=", r"\mu_0", r"I_{\text{enc}}", size=44)
        law.move_to([0, AMP_LAW_Y, 0]).set_opacity(0.9)
        law[1].set_color(CYAN)
        law[3].set_color(MAGENTA)
        law[6].set_color(AMBER)
        self.ancora("a19")
        self.play(*self.caption("LEI DE AMPÈRE"), FadeOut(ideal), FadeIn(law, shift=UP * 0.1),
                  FadeOut(VGroup(sym, symbox)), *set_state(mk_state("sym")), run_time=0.8)
        self.ancora("a20")
        self.play(self.amp_op.animate.set_value(1), self.side_op.animate.set_value(1),
                  self.ell_op.animate.set_value(1), run_time=0.6)
        self.note(nm(r"\text{contorno todo fora: }I_{\text{enc}}=0"))
        ienc0 = mt(r"I_{\text{enc}}", "=", "0", size=42).move_to([0, AMP_AUX_Y, 0])
        ienc0[0].set_color(AMBER)
        self.play(FadeIn(ienc0, shift=UP * 0.1), Indicate(law[6], color=AMBER, scale_factor=1.3),
                  run_time=0.7)
        self.check_safe()

        def Bterm(i, sign=None, size=44):
            parts = ([sign] if sign else []) + ["B", rf"(\rho_{i})", r"\ell"]
            m = mt(*parts, size=size)
            k = 1 if sign else 0
            m[k].set_color(CYAN)
            m[k + 1].set_color(MAGENTA)
            m[k + 2].set_color(MAGENTA)
            return m

        t1, t2 = Bterm(1), Bterm(2, "-")
        z1, z2, eq0 = mt("+", "0", size=44), mt("+", "0", size=44), mt("=", "0", size=44)
        row = VGroup(t1, z1, t2, z2, eq0).arrange(RIGHT, buff=0.14)
        fit(row, 6.9).move_to([0, AMP_OP_Y, 0])

        def emit(term, start, run=0.65):
            """O termo nasce ao lado do lado do contorno e viaja até o seu lugar na equação."""
            spawn = term.copy().move_to(start)
            self.play(FadeIn(spawn, scale=0.6), run_time=0.25)
            self.play(Transform(spawn, term), run_time=run)
            return spawn

        def perp(x, y):
            """B (ciano) atravessa o lado curto em ângulo reto: B · d l = 0."""
            return VGroup(vec([x - 0.34, y, 0], [x + 0.34, y, 0], CYAN, 3),
                          right_angle(np.array([x, y, 0.0]), RIGHT, UP, 0.14, WHITE, 0.85))

        yb, yt = Y_OUT - RECT_H / 2, Y_OUT + RECT_H / 2
        self.note(nm(r"\text{lado de baixo: }B\text{ e }d\vec\ell\text{ no mesmo sentido}"),
                  self.act1.animate.set_value(1), run_time=0.4)
        e1 = emit(t1, [0, yb - 0.38, 0])
        pr = perp(RECT_W / 2, Y_OUT)
        self.note(nm(r"\text{lado curto: }B\perp d\vec\ell\to0"),
                  self.act1.animate.set_value(0.5), self.actR.animate.set_value(1), FadeIn(pr), run_time=0.5)
        e2 = emit(z1, [2.85, Y_OUT, 0])
        self.play(FadeOut(pr), self.actR.animate.set_value(0.5), run_time=0.3)
        self.note(tag("sentidos opostos → sinal negativo", 21, 0.9),
                  self.act2.animate.set_value(1), run_time=0.4)
        e3 = emit(t2, [0, yt + 1.0, 0])
        pl = perp(-RECT_W / 2, Y_OUT)
        self.note(nm(r"\text{outro lado curto: }B\perp d\vec\ell\to0"),
                  self.act2.animate.set_value(0.5), self.actL.animate.set_value(1), FadeIn(pl), run_time=0.5)
        e4 = emit(z2, [-2.85, Y_OUT, 0])
        self.play(FadeOut(pl), self.actL.animate.set_value(0.5), FadeIn(eq0, shift=UP * 0.1), run_time=0.5)
        swap([e1, e2, e3, e4], row)
        self.check_safe()
        self.wait(0.15)

        # os zeros perdem peso e saem; os termos restantes fecham o espaço
        closed = VGroup(t1.copy(), t2.copy(), eq0.copy()).arrange(RIGHT, buff=0.18)
        fit(closed, 6.9).move_to([0, AMP_OP_Y, 0])
        self.note(tag("os termos nulos saem da soma", 23, 0.9), z1.animate.set_opacity(0).scale(0.5),
                  z2.animate.set_opacity(0).scale(0.5), run_time=0.6)
        self.play(t1.animate.move_to(closed[0]), t2.animate.move_to(closed[1]), eq0.animate.move_to(closed[2]),
                  run_time=0.7)
        self.remove(row)
        grp = VGroup(t1, t2, eq0)
        self.add(grp)

        # colchete: o ℓ é comum aos dois termos
        F = mt(r"\big[", "B", r"(\rho_1)", "-", "B", r"(\rho_2)", r"\big]", r"\ell", "=", "0", size=46)
        for i in (1, 4):
            F[i].set_color(CYAN)
        for i in (2, 5, 7):
            F[i].set_color(MAGENTA)
        fit(F, 6.9).move_to([0, AMP_OP_Y, 0])
        self.note(nm(r"\ell\text{ é fator comum}"), Indicate(t1[2], color=MAGENTA, scale_factor=1.6),
                  Indicate(t2[3], color=MAGENTA, scale_factor=1.6), run_time=0.8)
        self.play(Transform(t1[0], F[1]), Transform(t1[1], F[2]), Transform(t1[2], F[7]),
                  Transform(t2[0], F[3]), Transform(t2[1], F[4]), Transform(t2[2], F[5]),
                  t2[3].animate.move_to(F[7]).set_opacity(0), Transform(eq0[0], F[8]),
                  Transform(eq0[1], F[9]), FadeIn(F[0]), FadeIn(F[6]), run_time=1.2)
        swap(grp, F)
        self.check_safe()
        self.wait(0.10)

        # ℓ > 0 sai da equação; o que sobra é B(rho1) = B(rho2)
        G = mt("B", r"(\rho_1)", "=", "B", r"(\rho_2)", size=52).move_to([0, AMP_OP_Y, 0])
        G[0].set_color(CYAN)
        G[3].set_color(CYAN)
        G[1].set_color(MAGENTA)
        G[4].set_color(MAGENTA)
        self.note(nm(r"\text{como }\ell>0:\;B(\rho_1)=B(\rho_2)", 30), Indicate(F[7], color=MAGENTA, scale_factor=1.6),
                  run_time=0.7)
        self.play(F[7].animate.scale(0.3).set_opacity(0), F[0].animate.scale(0.5).set_opacity(0),
                  F[6].animate.scale(0.5).set_opacity(0), F[3].animate.scale(0.5).set_opacity(0),
                  F[9].animate.scale(0.5).set_opacity(0), Transform(F[1], G[0]), Transform(F[2], G[1]),
                  Transform(F[8], G[2]), Transform(F[4], G[3]), Transform(F[5], G[4]), run_time=1.1)
        swap(F, G)
        self.wait(0.10)
        H = mt(r"B_{\text{fora}}", "=", r"\text{constante}", size=50).move_to([0, AMP_OP_Y, 0])
        H[0].set_color(CYAN)
        gl, gr = VGroup(G[0], G[1]), VGroup(G[3], G[4])
        self.note(nm(r"\text{quaisquer }\rho_1,\rho_2\to B_{\text{fora}}\text{ constante}", 28),
                  Transform(gl, H[0]), Transform(G[2], H[1]), Transform(gr, H[2]), FadeOut(ienc0), self.act1.animate.set_value(0),
                  self.act2.animate.set_value(0), self.actL.animate.set_value(0),
                  self.actR.animate.set_value(0), self.qout_op.animate.set_value(0),
                  self.bout_op.animate.set_value(1), run_time=1.0)
        swap([G, gl, gr], H)
        sweep()
        self.check_safe()
        self.wait(0.20)

        # longe do solenoide: B -> 0; só então a constante vale zero
        cond = mt("B", r"(\rho)", r"\to", "0", r"\quad\text{quando}\quad", r"\rho", r"\to", r"\infty", size=38)
        cond.move_to([0, AMP_AUX_Y, 0])
        cond[0].set_color(CYAN)
        cond[1].set_color(MAGENTA)
        cond[5].set_color(MAGENTA)
        self.ancora("a21")
        self.note(nm(r"\text{só o solenoide cria campo: }B\to0\text{ longe dele}"), self.amp_y.animate.set_value(Y_FAR),
                  self.probe.animate.set_value(1.0), FadeIn(cond, shift=UP * 0.1), run_time=1.6)
        self.wait(0.25)
        H0 = mt(r"B_{\text{fora}}", "=", "0", size=54).move_to([0, AMP_OP_Y, 0])
        H0[0].set_color(CYAN)
        hbox = SurroundingRectangle(H0, color=WHITE, buff=0.24, corner_radius=0.08, stroke_width=2.5)
        self.ancora("a22")
        self.play(Transform(H[0], H0[0]), Transform(H[1], H0[1]), Transform(H[2], H0[2]),
                  Indicate(cond[3], color=WHITE, scale_factor=1.4), run_time=0.9)
        swap(H, H0)
        sweep()
        self.note(nm(r"\text{no modelo infinito: }B_{\text{fora}}=0"), Create(hbox),
                  self.bout_op.animate.set_value(0), run_time=0.8)
        self.check_safe()
        self.wait(0.50)
        self.play(FadeOut(VGroup(H0, hbox, cond)), *set_state(mk_state("out")), run_time=0.6)
        sweep()

        # dentro: o mesmo argumento; as setas se igualam
        self.ancora("a23")
        self.play(self.amp_y.animate.set_value(Y_IN), self.probe.animate.set_value(0), run_time=1.0)
        ins = mt(r"I_{\text{enc}}", "=", "0", r"\;\Rightarrow\;", r"B_{\text{dentro}}", "=", r"\text{constante}",
                 size=42)
        ins[0].set_color(AMBER)
        ins[4].set_color(CYAN)
        fit(ins, 6.9).move_to([0, AMP_OP_Y, 0])
        self.play(FadeIn(ins, shift=UP * 0.1), self.act1.animate.set_value(1), self.act2.animate.set_value(1),
                  run_time=0.6)
        self.note(nm(r"\text{no modelo infinito: }B_{\text{dentro}}\text{ é uniforme}"), self.uni.animate.set_value(1.0),
                  run_time=0.9)
        self.check_safe()
        self.wait(0.40)
        self.play(FadeOut(ins), *set_state(mk_state("in")),
                  self.act1.animate.set_value(0), self.act2.animate.set_value(0), run_time=0.6)

        # ══ B9. Atravessando a parede: o contorno vira B ℓ ═════════════════════════════════════════
        self.ancora("a24")
        self.play(*self.caption("ATRAVESSANDO A PAREDE"), self.amp_y.animate.set_value(Y_WALL),
                  *set_state(mk_state("out")), run_time=1.0)
        wa = mt("B", r"\ell", size=46)
        wa[0].set_color(CYAN)
        wa[1].set_color(MAGENTA)
        wz1, wz2 = mt("+", "0", size=46), mt("+", "0", size=46)
        wo = mt("-", r"B_{\text{fora}}", r"\ell", size=46)
        wo[1].set_color(CYAN)
        wo[2].set_color(MAGENTA)
        weq = mt("=", r"\mu_0", r"I_{\text{enc}}", size=46)
        weq[2].set_color(AMBER)
        wrow = VGroup(wa, wz1, wo, wz2, weq).arrange(RIGHT, buff=0.14)
        fit(wrow, 6.9).move_to([0, AMP_OP_Y, 0])
        yw_b = Y_WALL - RECT_H / 2
        self.note(nm(r"\text{lado de dentro: }B\text{ e }d\vec\ell\text{ no mesmo sentido}"), self.act1.animate.set_value(1),
                  run_time=0.4)
        w1 = emit(wa, [0, 1.56, 0])
        pr = perp(RECT_W / 2, Y_WALL)
        self.note(nm(r"\text{lado curto: }B\perp d\vec\ell\to0"), self.act1.animate.set_value(0.5),
                  self.actR.animate.set_value(1), FadeIn(pr), run_time=0.5)
        w2 = emit(wz1, [2.85, 3.45, 0])
        self.play(FadeOut(pr), self.actR.animate.set_value(0.5), run_time=0.3)
        self.note(nm(r"\text{lado de fora: }B_{\text{fora}}\,\ell"), self.act2.animate.set_value(1), run_time=0.4)
        w3 = emit(wo, [0, 4.25, 0])
        pl = perp(-RECT_W / 2, Y_WALL)
        self.note(tag("outro lado curto → 0", 23, 0.9), self.act2.animate.set_value(0.5),
                  self.actL.animate.set_value(1), FadeIn(pl), run_time=0.5)
        w4_ = emit(wz2, [-2.85, 3.45, 0])
        self.play(FadeOut(pl), self.actL.animate.set_value(0.5), FadeIn(weq, shift=UP * 0.1), run_time=0.5)
        swap([w1, w2, w3, w4_], wrow)
        self.check_safe()
        self.wait(0.15)

        # os termos nulos somem um a um; sobra B ℓ
        wo0 = mt("-", "0", r"\ell", size=46).move_to(wo)
        wo0[2].set_color(MAGENTA)
        self.note(tag("termo nulo sai", 23, 0.9), wz1.animate.set_opacity(0).scale(0.5), run_time=0.5)
        self.note(nm(r"B_{\text{fora}}=0\to\text{ o termo some}"), Transform(wo, wo0),
                  Indicate(self._state, color=CYAN), run_time=0.8)
        self.play(wo.animate.set_opacity(0).scale(0.5), run_time=0.5)
        self.note(tag("termo nulo sai", 23, 0.9), wz2.animate.set_opacity(0).scale(0.5), run_time=0.5)
        wclosed = VGroup(wa.copy(), weq.copy()).arrange(RIGHT, buff=0.22).move_to([0, AMP_OP_Y, 0])
        self.play(wa.animate.move_to(wclosed[0]), weq.animate.move_to(wclosed[1]),
                  self.act1.animate.set_value(1), self.act2.animate.set_value(0), self.actL.animate.set_value(0),
                  self.actR.animate.set_value(0), run_time=0.8)
        self.remove(wrow)
        wm = VGroup(wa, weq)
        self.add(wm)
        self.check_safe()
        self.wait(0.10)

        # ══ B10. A corrente envolvida: N_l = n l  ->  I_enc = N_l I  ->  I_enc = n l I ═════════════
        self.ancora("a26")
        self.note(nm(r"\text{em um trecho }\ell:\;N_\ell=n\ell"),
                  self.enc_n.animate.set_value(6.0), run_time=1.3)
        a1 = mt(r"N_\ell", "=", "n", r"\ell", size=44).move_to([0, AMP_AUX_Y, 0])
        a1[0].set_color(AMBER)
        a1[2].set_color(AMBER)
        a1[3].set_color(MAGENTA)
        self.play(FadeIn(a1, shift=UP * 0.1), run_time=0.7)
        self.check_safe()
        self.wait(0.25)
        a2 = mt(r"I_{\text{enc}}", "=", r"N_\ell", r"\,I", size=44).move_to([0, AMP_AUX_Y, 0])
        for i in (0, 2, 3):
            a2[i].set_color(AMBER)
        self.ancora("a26b")
        self.note(nm(r"\text{cada espira leva corrente }I"), Transform(a1[0], a2[2]),
                  Transform(a1[1], a2[1]), a1[2].animate.scale(0.4).set_opacity(0),
                  a1[3].animate.scale(0.4).set_opacity(0), FadeIn(a2[0]), FadeIn(a2[3]), run_time=0.9)
        swap(a1, a2)
        self.wait(0.25)
        a3 = mt(r"I_{\text{enc}}", "=", "n", r"\ell", "I", size=44).move_to([0, AMP_AUX_Y, 0])
        for i in (0, 2, 4):
            a3[i].set_color(AMBER)
        a3[3].set_color(MAGENTA)
        self.note(None, Transform(a2[0], a3[0]), Transform(a2[1], a3[1]),
                  Transform(a2[2], VGroup(a3[2], a3[3])), Transform(a2[3], a3[4]), run_time=1.0)
        swap(a2, a3)
        self.check_safe()
        self.wait(0.40)

        # ══ B11. As duas metades se encaixam ═══════════════════════════════════════════════════════
        w4 = mt("B", r"\ell", "=", r"\mu_0", "n", r"\ell", "I", size=52).move_to([0, AMP_OP_Y, 0])
        w4[0].set_color(CYAN)
        w4[1].set_color(MAGENTA)
        w4[4].set_color(AMBER)
        w4[5].set_color(MAGENTA)
        w4[6].set_color(AMBER)
        self.ancora("a26c")
        self.play(*self.caption("AS DUAS METADES SE ENCAIXAM"), FadeOut(self.hint),
                  self.enc_n.animate.set_value(0.0), Transform(wa[0], w4[0]), Transform(wa[1], w4[1]),
                  Transform(weq[0], w4[2]), Transform(weq[1], w4[3]), weq[2].animate.scale(0.4).set_opacity(0),
                  Transform(a3[2], w4[4]), Transform(a3[3], w4[5]), Transform(a3[4], w4[6]),
                  a3[0].animate.set_opacity(0), a3[1].animate.set_opacity(0), run_time=1.3)
        swap([wm, a3], w4)
        self.hint = None
        self.check_safe()
        self.wait(0.30)
        self.ancora("a27")
        self.note(nm(r"\text{o mesmo }\ell\text{ aparece dos dois lados}\to\text{cancela}"), Indicate(w4[1], color=MAGENTA, scale_factor=1.7),
                  Indicate(w4[5], color=MAGENTA, scale_factor=1.7), run_time=0.9)
        res = mt("B", "=", r"\mu_0", "n", "I", size=62).move_to([0, AMP_OP_Y, 0])
        res[0].set_color(CYAN)
        res[3].set_color(AMBER)
        res[4].set_color(AMBER)
        rbox = SurroundingRectangle(res, color=WHITE, buff=0.24, corner_radius=0.08, stroke_width=2.5)
        self.note(None, w4[1].animate.scale(0.2).set_opacity(0),
                  w4[5].animate.scale(0.2).set_opacity(0), Transform(w4[0], res[0]), Transform(w4[2], res[1]),
                  Transform(w4[3], res[2]), Transform(w4[4], res[3]), Transform(w4[6], res[4]), run_time=1.1)
        swap(w4, res)
        self.play(Create(rbox), run_time=0.5)
        self.note(tag("no modelo infinito: resultado exato", 22, 0.95))
        self.check_safe()
        self.wait(1.60)

        # ══ B12. Lendo a fórmula: I e n controlam o campo ══════════════════════════════════════════
        self.ancora("a28")
        self.play(*self.caption("LENDO A FÓRMULA"), FadeOut(self._state), self.amp_op.animate.set_value(0),
                  self.side_op.animate.set_value(0), self.ell_op.animate.set_value(0), FadeOut(law),
                  run_time=0.6)
        self.note(nm(r"I\uparrow\;\Rightarrow\;B\uparrow", 34),
                  Indicate(res[4], color=AMBER, scale_factor=1.5), self.cur.animate.set_value(1.8),
                  run_time=1.0)
        self.wait(0.25)
        self.play(self.cur.animate.set_value(1.0), run_time=0.5)
        nN2 = mt("n", "=", "N/L", size=38).move_to([0, AMP_AUX_Y, 0])
        nN2[0].set_color(AMBER)
        self.ancora("a29")
        self.note(nm(r"\text{mais espiras no mesmo }L\;\Rightarrow\;n\uparrow\;\Rightarrow\;B\uparrow", 28),
                  Indicate(res[3], color=AMBER, scale_factor=1.5), FadeIn(nN2, shift=UP * 0.1),
                  self.extra_op.animate.set_value(1.0), run_time=1.2)
        self.check_safe()
        self.wait(0.30)
        mu_note = VGroup(tex(r"\mu_0", 32), text(": constante magnética do vácuo", 22, WHITE, 0.9)
                         ).arrange(RIGHT, buff=0.08)
        self.note(mu_note, Indicate(res[2], color=WHITE, scale_factor=1.4),
                  self.extra_op.animate.set_value(0.0), run_time=0.8)
        self.check_safe()
        self.wait(0.40)

        # ══ B13. De volta à bobina real: as pontas reaparecem enquanto "=" vira "≈" ════════════════
        self.ancora("a30")
        self.play(*self.caption("DE VOLTA À BOBINA REAL"), FadeOut(nN2),
                  FadeOut(self.hint), VGroup(res, rbox).animate.scale(50 / 62).move_to([0, TOP_Y, 0]),
                  self.coil_op.animate.set_value(1), self.cut_op.animate.set_value(0),
                  self.bin_op.animate.set_value(0), run_time=0.9)
        self.hint = None
        self.play(self.tilt.animate.set_value(TILT0), self.rs.animate.set_value(RG),
                  self.ay.animate.set_value(AY_G), run_time=1.2)
        self.play(FadeIn(axes), self.curve_op.animate.set_value(1), self.ends_op.animate.set_value(1),
                  self.span_op.animate.set_value(1), run_time=0.7)
        approx = mt("B", r"\approx", r"\mu_0", "n", "I", size=50).move_to([0, TOP_Y, 0])
        approx[0].set_color(CYAN)
        approx[3].set_color(AMBER)
        approx[4].set_color(AMBER)
        abox = SurroundingRectangle(approx, color=WHITE, buff=0.24, corner_radius=0.08, stroke_width=2.5)
        self.note_y = NOTE_Y
        self.ancora("a31")
        self.note(nm(r"\text{região central}+L\gg R:\;B\approx\mu_0 n I"),
                  self.nt.animate.set_value(NT_LONG), self.ext_op.animate.set_value(1.0),
                  TransformMatchingTex(res, approx), Transform(rbox, abox), run_time=2.6)
        self.check_safe()
        self.wait(0.35)
        band_c = Rectangle(width=3.2, height=G_H).set_stroke(width=0).set_fill(VIOLET, 0.30)
        band_c.move_to([0, G_Y0 + G_H / 2, 0])
        self.note(nm(r"\text{no centro, }B\text{ é quase uniforme}"), FadeIn(band_c))
        self.wait(0.55)
        self.ancora("a31b")
        self.note(nm(r"\text{nas pontas }B\text{ varia; fora, não é exatamente zero}"), FadeOut(band_c))
        self.check_safe()
        self.wait(0.70)

        # ══ B14. Onde isso aparece: o atuador, com o núcleo na ENTRADA, onde o campo varia ═════════
        self.ancora("a32")
        self.play(*self.caption("ONDE ISSO APARECE"), FadeOut(VGroup(approx, rbox)),
                  self.ext_op.animate.set_value(0), self.cur.animate.set_value(0),
                  self.span_op.animate.set_value(0), FadeOut(self.hint), run_time=0.7)
        self.hint = None
        self.play(self.nt.animate.set_value(NT_ACT), self.cx.animate.set_value(CX_ACT), run_time=1.0)
        ay, xe = AY_G, CX_ACT + RG * NT_ACT * PITCH / 2          # xe: a entrada da bobina
        plunger = RoundedRectangle(width=1.5, height=0.60, corner_radius=0.12).set_stroke(WHITE, 3, 0.9)
        plunger.set_fill(WHITE, 0.22).move_to([xe + 0.35, ay, 0])
        rod = Line([plunger.get_right()[0], ay, 0], [2.64, ay, 0]).set_stroke(WHITE, 4, 0.85)
        gate = Rectangle(width=0.62, height=0.30).set_stroke(WHITE, 3, 0.9).set_fill(WHITE, 0.3)
        gate.move_to([2.95, ay, 0])
        moving = VGroup(plunger, rod, gate)
        pipe = VGroup(Line([2.6, ay - 1.0, 0], [2.6, ay - 0.2, 0]), Line([2.6, ay + 0.2, 0], [2.6, ay + 1.0, 0]),
                      Line([3.3, ay - 1.0, 0], [3.3, ay + 1.0, 0])).set_stroke(BLUE, 3, 0.8)
        flow = VGroup(vec([2.95, ay + 0.9, 0], [2.95, ay + 0.35, 0], WHITE, 4).set_opacity(0.7),
                      vec([2.95, ay - 0.35, 0], [2.95, ay - 0.9, 0], WHITE, 4).set_opacity(0.7))
        band_e = Rectangle(width=1.3, height=G_H).set_stroke(width=0).set_fill(VIOLET, 0.30)
        band_e.move_to([xe, G_Y0 + G_H / 2, 0])
        state = tag("VÁLVULA FECHADA", 24, 0.9).move_to([0, TOP_Y, 0])
        self.ancora("a32b")
        self.play(FadeIn(VGroup(pipe, moving, state)), run_time=0.6)
        self.note(tag("núcleo ferromagnético na entrada · corrente desligada", 21, 0.9))
        self.check_safe()
        self.wait(0.40)
        self.note(tag("corrente ligada → campo estabelecido", 23, 0.9), self.cur.animate.set_value(1.0),
                  self.glow.animate.set_value(1.0), run_time=0.9)
        self.ancora("a32c")
        self.note(tag("perto da entrada, o campo varia", 23, 0.9), FadeIn(band_e))
        self.check_safe()
        self.wait(0.50)
        new_state = tag("VÁLVULA ABERTA", 24, 0.95).move_to([0, TOP_Y, 0])
        self.ancora("a32d")
        self.play(moving.animate.shift(LEFT * 1.0), run_time=0.9)
        self.ancora("a32e")
        self.note(tag("núcleo ferromagnético atraído para dentro", 21, 0.9), soft_swap(state, new_state),
                  FadeIn(flow), run_time=0.7)
        self.check_safe()
        self.wait(0.80)

        # ══ B15. Fechamento ════════════════════════════════════════════════════════════════════════
        self.ancora("a33")
        self.play(*self.caption("DA ESPIRA AO SOLENOIDE"),
                  FadeOut(VGroup(pipe, moving, flow, new_state, band_e, axes)),
                  self.coil_op.animate.set_value(0), self.curve_op.animate.set_value(0),
                  self.ends_op.animate.set_value(0), FadeOut(self.hint), run_time=0.7)
        self.hint = None
        final = mt("B", r"\approx", r"\mu_0", "n", "I", size=50)
        final[0].set_color(CYAN)
        final[3].set_color(AMBER)
        final[4].set_color(AMBER)
        steps = [text("uma espira", 24), text("muitas espiras: os campos se somam", 24),
                 text("centro de um solenoide longo", 24), boxed(final),
                 text("núcleo atraído para dentro", 22, WHITE, 0.9)]
        downs = [tex(r"\downarrow", 30).set_opacity(0.6) for _ in range(4)]
        rec = VGroup(steps[0], downs[0], steps[1], downs[1], steps[2], downs[2], steps[3], downs[3],
                     steps[4])
        rec.arrange(DOWN, buff=0.16).move_to([0, 1.7, 0])
        self.play(FadeIn(steps[0], shift=UP * 0.1), run_time=0.5)
        self.ancora("a33b")
        self.play(FadeIn(downs[0]), FadeIn(steps[1], shift=UP * 0.1), run_time=0.5)
        self.ancora("a33c")
        self.play(FadeIn(downs[1]), FadeIn(steps[2], shift=UP * 0.1), run_time=0.5)
        self.ancora("a33d")
        self.play(FadeIn(downs[2]), FadeIn(steps[3], shift=UP * 0.1), run_time=0.6)
        self.ancora("a33e")
        self.play(FadeIn(downs[3]), FadeIn(steps[4], shift=UP * 0.1), run_time=0.5)
        self.ancora("a34")
        handle = tag("@labparallax", 22, 0.8).move_to([0, rec.get_bottom()[1] - 0.7, 0])
        self.play(FadeIn(handle, shift=UP * 0.1), run_time=0.5)
        self.check_safe()
        self.wait(1.10)
        self.ancora("fim")
