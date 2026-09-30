"""Campo magnético dentro de um solenoide: B = mu0 n I; preview silencioso.

DA EQUAÇÃO AO FENÔMENO · EP. 03. O espectador acompanha a construção:
geometria -> contribuição -> soma -> simetria -> Ampère -> interpretação.

1) Derivação (Biot-Savart) do campo axial de UMA espira, raio R, corrente I, ponto P
   no eixo a distância z. Da geometria, r^2 = R^2 + z^2. De dB = (mu0 I/4pi) dl x r / r^3,
   com dl SAINDO do plano do corte e r no plano, dl é perpendicular a r e
   |dB| = (mu0 I/4pi) dl/r^2. Dois elementos diametralmente opostos dão dB ~ (R, +z) e
   (R, -z) (db_dirs): as transversais se cancelam e a soma do PAR vale 2 dB_z, isto é,
   duas vezes a projeção axial de UMA contribuição. A integral segue com uma parcela.
   O ângulo entre dB e o eixo é o mesmo ângulo do triângulo no elemento (cos = R/r), de
   onde dB_z/dB = R/r. Com dl = R dphi (vista frontal auxiliar):
   dB_z = mu0 I R^2 dphi / (4pi (R^2+z^2)^{3/2}); só a integral de dphi vale 2pi, e
   2pi/(4pi) = 1/2, dando B_z(z) = mu0 I R^2 / (2 (R^2+z^2)^{3/2}); em z = 0, mu0 I/(2R).

2) Superposição (bobina finita real). A MESMA espira vira a primeira da bobina e
   B_z(z) vira B_j(z) por z -> z - z_j. Parcelas, barra e resultante saem todas de
   b_sum (soma real): 1,00 -> 1,83 -> 2,85 -> 3,58 na escala B/B_1(0). Nessa sequência
   I e o passo ficam fixos e o COMPRIMENTO cresce (não é o teste de n com L fixo).
   A expressão é só axial: retornos externos e campo fora do eixo são esboço qualitativo.

3) Modelo ideal: bobina finita -> solenoide longo -> distribuição CONTÍNUA e uniforme
   (as espiras discretas se fundem; K = n I, [K] = A/m, não vai à tela). No modelo
   contínuo as setas internas valem exatamente mu0 n I — não são a soma de 38 espiras.
   A simetria usa translação em z, ausência de direção azimutal e pares de FATIAS do
   enrolamento simétricas em torno do plano transversal de P (esquema, sem escala);
   db_dirs e b_loop não são usados fora do eixo. Conclui B = B(s) z^.

4) Ampère, no mesmo quadro cumulativo: lei ancorada, premissas guardadas na prateleira
   e operação ativa ao centro. O MESMO retângulo desliza fora -> dentro -> atravessando:
     fora:         cada lado é iluminado e leva sua parcela a
                   B(s1) l + 0 - B(s2) l + 0 = 0; tirando os zeros e dividindo por l > 0,
                   B_fora = constante. Só então, em outra linha, a condição física
                   (campo do solenoide, sem campo uniforme externo) B -> 0 com s -> inf;
                   as duas juntas dão B_fora = 0;
     dentro:       I_enc = 0 => B_dentro = constante (curto);
     atravessando: lado interno -> B l, laterais e lado externo -> 0; as seis seções de
                   UMA fileira são marcadas em sequência, N_l = n l e I_enc = n l I;
                   cópias de B l e n l I entram na lei ancorada, e dividir os dois lados
                   por l dá B = mu0 n I.
   Depois a idealização é desfeita: pontas e retornos voltam, "=" vira "~=" e a nota
   passa a "região central · solenoide longo, L >> R" na MESMA transição.

Unidades internas: R = 1; b = B / (mu0 I / 2R); passo PITCH = 0,5 R => n = 2/R e o valor
ideal é b = 2 R n = 4 (= mu0 n I na mesma escala). l = 3 R => N_l = n l = 6 seções.

Cores com significado estável: azul = R e a geometria da bobina; magenta = z e marcas
sobre o eixo z (e destaque localizado nos blocos em que z não está em cena); violeta = r,
contorno amperiano e l; ciano = corrente, elemento e contribuições individuais;
branco = campo e resultados.
"""

import numpy as np
from manim import (
    DOWN, LEFT, ORIGIN, PI, RIGHT, UP, AnimationGroup, Arc, Arrow, Circle, Create, DashedLine,
    Dot, FadeIn, FadeOut, ImageMobject, Indicate, Line, MathTex, Rectangle,
    RoundedRectangle, Scene, SurroundingRectangle, Transform, TransformFromCopy,
    TransformMatchingTex, VGroup, VMobject, ValueTracker, always_redraw, linear,
)

from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # corrente, elemento e contribuições individuais
MAGENTA = "#EA63FF"       # z e marcas sobre o eixo z; destaque localizado
BLUE = "#267BFF"          # R e a geometria da bobina
VIOLET = SECONDARY_COLOR  # r, contorno amperiano e l

SAFE_BOTTOM = -4.6        # abaixo disso: faixa reservada a legendas
SAFE_X = 3.5              # |x| máximo do conteúdo (o modelo ideal sangra de propósito)
HEADLINE_TOP = 6.85

# Ritmo: leitura estável depois de uma operação e depois de um resultado central.
BEAT = 0.28              # respiro curto entre passos de um mesmo raciocínio
READ = 1.32              # leitura estável depois de uma operação central
READ_RES = 2.55          # leitura de um resultado

# ── Geometria de tela: bobina e corte ───────────────────────────────────────
RS = 1.25                 # unidades de tela por R
AX_Y = 1.25               # altura do eixo do solenoide
PITCH = 0.5               # passo do enrolamento, em unidades de R  => n = 1/PITCH por R
B_IDEAL = 2.0 / PITCH     # mu0 n I na escala b = B/(mu0 I/2R): 2 R n = 4
LB = 2.30                 # barra/resultante quando b = B_IDEAL
BAR_Y, BAR_X0 = -0.62, 0.0
GY0, GH = -2.60, 1.35     # curva B(z) da bobina finita
X_VIS = 5.2               # só desenhamos espiras/seções com |x| < X_VIS

N_INF = 38.0              # bobina longa antes da fusão no modelo contínuo
Z_FIN = 3.0               # semicomprimento da bobina finita no corte, em R
L_ELL = 3.0               # comprimento l do retângulo amperiano, em unidades de R
ARR_IN = 0.55             # seta do campo interno no corte quando b = B_IDEAL

CUT_Z = (np.arange(-19, 19) + 0.5) * PITCH          # seções do fio: ±0,25 … ±9,25
CUT_EXTRA = np.arange(-19, 19) * PITCH              # fileira intercalada: dobra n
ENC_Z = CUT_Z[np.abs(CUT_Z) < L_ELL / 2]            # as seções dentro de l
RECT_W, RECT_H = L_ELL * RS, 0.90
Y_OUT, Y_IN, Y_WALL = 3.55, 1.75, 2.60              # centros do retângulo nos três estados

# ── Geometria de tela: bloco da derivação (espira única, grande) ────────────
DR = 2.25                 # unidades de tela por R na derivação
DOX, DOY = -2.05, 2.35    # centro O da espira
DZ = 1.45                 # z do ponto P, em unidades de R
DTILT = 0.34
LDB = 1.45                # comprimento de desenho de dB
D_O = np.array([DOX, DOY, 0.0])
D_P = np.array([DOX + DR * DZ, DOY, 0.0])
D_TOP = np.array([DOX, DOY + DR, 0.0])   # elemento em phi = 0: corrente saindo do plano
D_BOT = np.array([DOX, DOY - DR, 0.0])   # elemento oposto: corrente entrando
AUX_C, AUX_R = np.array([-2.55, -0.70, 0.0]), 0.58   # vista frontal auxiliar (dl = R dphi)
AUX_PHI, AUX_DPHI = 0.55, 0.72                       # arco dl na vista auxiliar

# ── Níveis verticais dos quadros ────────────────────────────────────────────
DER_OP_Y, DER_NOTE_Y = -2.25, -3.95      # derivação: operação ativa e nota
DER_REF = np.array([2.15, -0.75, 0.0])   # identidade r² = R² + z² guardada
AMP_LAW_Y, AMP_SIDE_Y = -0.60, -1.50     # Ampère: lei ancorada e linha da condição
AMP_OP_Y, SHELF_Y = -2.55, -3.90         # operação ativa e prateleira de resultados


# ── Modelo físico: tudo que se move na tela sai destas funções ──────────────
def b_loop(z, zj=0.0):
    """B_z NO EIXO de uma espira de raio R = 1 centrada em zj, em unidades de mu0 I / 2R."""
    return 1.0 / (1.0 + (np.asarray(z, dtype=float) - zj) ** 2) ** 1.5


def db_dirs(z):
    """Direções de dB dos dois elementos diametralmente opostos, no ponto P = (z, 0) DO EIXO.

    Com x^ no eixo, y^ para cima e z^out saindo da tela (x^ x y^ = z^out):
    elemento de cima em (0, +R), corrente +z^out, r = P - elem = (z, -R);
      dl x r ~ z^out x (z x^ - R y^) = z y^ + R x^      => (R, +z)
    elemento de baixo em (0, -R), corrente -z^out, r = (z, +R);
      (-z^out) x (z x^ + R y^) = -z y^ + R x^           => (R, -z)
    Axiais iguais (+x^), transversais opostas (±z y^): a soma do par é 2 dB_z x^.
    Válido só no eixo — fora dele a simetria é tratada por fatias, sem esta função.
    """
    return np.array([1.0, z, 0.0]), np.array([1.0, -z, 0.0])


def dbz_phi(z):
    """dB_z / dphi em unidades de mu0 I / 4pi, com R = 1: R^2 / (R^2 + z^2)^{3/2}."""
    return 1.0 / (1.0 + z * z) ** 1.5


def turn_centers(nf):
    """Espiras de uma bobina de nf voltas (nf real), centradas em z = 0, passo PITCH.

    A volta i tem peso min(1, nf - i): em nf inteiro o peso é 1 e a soma é exata;
    entre inteiros a volta que entra aparece gradualmente e pesa o mesmo na soma.
    """
    k = int(np.ceil(nf - 1e-9))
    i = np.arange(k)
    return (i - (nf - 1) / 2) * PITCH, np.clip(nf - i, 0.0, 1.0)


def b_sum(z, nf):
    """Superposição axial real das nf espiras (a mesma soma que a barra e a seta usam)."""
    zs, w = turn_centers(nf)
    return float(np.sum(w * b_loop(z, zs)))


def b_cut(z, zlim, extra_op=0.0):
    """Bobina FINITA do corte: soma real da fileira base (|z| <= zlim) + fileira intercalada."""
    wb = np.clip((zlim - np.abs(CUT_Z)) / 0.5, 0.0, 1.0)
    b = float(np.sum(wb * b_loop(z, CUT_Z)))
    if extra_op > 1e-3:
        we = np.clip((zlim - np.abs(CUT_EXTRA)) / 0.5, 0.0, 1.0)
        b += extra_op * float(np.sum(we * b_loop(z, CUT_EXTRA)))
    return b


def dim_mul(*ds):
    """Produto de dimensões representadas como {simbolo: expoente}."""
    out = {}
    for d in ds:
        for k, v in d.items():
            out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v}


# ── Conferências do modelo, no import ───────────────────────────────────────
# Dimensões: [mu0] = T m / A, [n] = 1/m, [I] = A  =>  B em tesla.
MU0_DIM, N_DIM, I_DIM, M = {"T": 1, "m": 1, "A": -1}, {"m": -1}, {"A": 1}, {"m": 1}
assert dim_mul(MU0_DIM, N_DIM, I_DIM) == {"T": 1}
assert dim_mul(MU0_DIM, I_DIM, {"m": 2}, {"m": -3}) == {"T": 1}   # mu0 I R^2 / (R^2+z^2)^{3/2}
assert dim_mul(MU0_DIM, I_DIM, {"m": -1}) == {"T": 1}             # mu0 I / (2R)

assert np.isclose(b_loop(0.0), 1.0) and np.isclose(b_loop(1.0), 2 ** -1.5)
_R, _I, _MU = 1.0, 1.0, 1.0
_z = np.linspace(-4, 4, 4001)
assert np.allclose(_MU * _I * _R ** 2 / (2 * (_R ** 2 + _z ** 2) ** 1.5), b_loop(_z) / 2)
assert np.allclose(b_loop(-_z), b_loop(_z))                       # paridade em z
assert b_loop(20.0) < b_loop(2.0) < b_loop(0.0)                   # decai com a distância
assert abs(b_loop(40.0) * 40.0 ** 3 - 1.0) < 2e-3                 # z >> R: cai com 1/z^3

# Derivação de Biot-Savart, passo a passo, exatamente como vai à tela.
_zt = DZ
_r2 = _R ** 2 + _zt ** 2
_r = np.sqrt(_r2)
assert np.isclose(np.hypot(_R, _zt) ** 2, _r2)                    # r² = R² + z²
_d1, _d2 = db_dirs(_zt)
assert np.isclose(np.dot(_d1, [_zt, -_R, 0.0]), 0.0)              # dB perpendicular a r
assert np.isclose(np.dot(_d2, [_zt, _R, 0.0]), 0.0)
assert np.isclose(_d1[1], -_d2[1]) and abs(_d1[1]) > 0            # transversais opostas
_u1, _u2 = _d1 / np.linalg.norm(_d1), _d2 / np.linalg.norm(_d2)
assert np.allclose(_u1 + _u2, [2 * _u1[0], 0.0, 0.0])             # a soma do par é axial…
assert np.isclose(np.linalg.norm(_u1 + _u2), 2 * _u1[0])          # …e vale 2x a projeção de uma
assert np.isclose(_u1[0], _R / _r)                                # fração axial = R/r
# o ângulo dB-eixo em P é o mesmo ângulo do triângulo no elemento
_ang_P = np.arccos(np.dot(_u1, [1.0, 0.0, 0.0]))
_e_to_o = np.array([0.0, -1.0, 0.0])
_e_to_p = np.array([_zt, -_R, 0.0]) / _r
assert np.isclose(_ang_P, np.arccos(np.dot(_e_to_o, _e_to_p)))
assert np.isclose(np.cos(_ang_P), _R / _r)
# dl = R dphi (comprimento de arco) e dB_z = (mu0 I/4pi)(dl/r^2)(R/r)
assert np.isclose(AUX_R * AUX_DPHI, AUX_R * AUX_DPHI)             # arco = raio x ângulo
assert np.isclose(dbz_phi(_zt), (1.0 / _r2) * (_R / _r) * _R)
assert np.isclose(dbz_phi(_zt), _R ** 2 / _r2 ** 1.5)
# integrar: só dphi depende de phi; 2pi/(4pi) = 1/2
assert np.isclose(2 * PI, 6.283185307179586) and np.isclose(2 * PI / (4 * PI), 0.5)
assert np.isclose(2 * PI * dbz_phi(_zt) / (4 * PI), 0.5 * _R ** 2 / _r2 ** 1.5)
assert np.isclose(2 * PI * dbz_phi(_zt) / (4 * PI) * 2, b_loop(_zt))   # = b_loop da soma
# checagem no centro: z = 0 => r = R e R^2/R^3 = 1/R
assert np.isclose(np.hypot(_R, 0.0), _R)
assert np.isclose(_R ** 2 / _R ** 3, 1.0 / _R)
assert np.isclose(2 * PI * dbz_phi(0.0) / (4 * PI) * 2, 1.0)
assert np.allclose([b_loop(1.3, 0.75)], [b_loop(1.3 - 0.75)])     # deslocamento z - z_j

_b = [b_sum(0.0, n) for n in (1, 2, 4, 8)]
assert np.isclose(_b[0], 1.0)
assert _b[0] < _b[1] < _b[2] < _b[3] < B_IDEAL                    # enrolar mais reforça
assert np.allclose(_b, [1.0, 1.82615, 2.85015, 3.58197], atol=5e-5)
assert abs(b_sum(0.0, 400) - B_IDEAL) < 0.01                      # limite: mu0 n I
assert abs(b_sum(2.0, 8) / b_sum(0.0, 8) - 0.54172) < 5e-4        # ponta ≈ 54% do centro
assert abs(b_cut(0.0, Z_FIN) - B_IDEAL) / B_IDEAL < 0.07          # finita: só aproximado
assert b_cut(Z_FIN, Z_FIN) < 0.65 * b_cut(0.0, Z_FIN)             # e cai na ponta
_dob = b_cut(0.0, Z_FIN, 1.0) / b_cut(0.0, Z_FIN)
assert 1.9 < _dob < 2.1 and not np.isclose(_dob, 2.0, atol=1e-6)  # dobrar n só aproxima 2x
assert int(len(ENC_Z)) == 6 and np.isclose(L_ELL / PITCH, 6.0)    # N_l = n l = 6, uma fileira
assert np.isclose(RECT_W / 2 / RS, L_ELL / 2)
assert Y_OUT - RECT_H / 2 - AX_Y > RS                             # estado 1: os dois lados fora
assert AX_Y + RS - (Y_IN + RECT_H / 2) > 0.2                      # estado 2: os dois dentro
assert Y_WALL - RECT_H / 2 < AX_Y + RS < Y_WALL + RECT_H / 2      # estado 3: atravessando
assert np.isclose(np.linalg.norm(D_TOP - D_O) / DR, _R)           # cateto R verdadeiro
assert np.isclose(np.linalg.norm(D_P - D_O) / DR, _zt)            # cateto z verdadeiro
assert np.isclose(np.linalg.norm(D_P - D_TOP) / DR, _r)           # hipotenusa r verdadeira


# ── Helpers visuais ─────────────────────────────────────────────────────────
def tex(content, size=40, color=WHITE):
    return MathTex(content, font_size=size, color=color)


def mtex(*parts, size=48, color=WHITE):
    return MathTex(*parts, font_size=size, color=color)


# A cor é aplicada DEPOIS de gerar o texto: o SVG do Pango (e o cache em media/texts)
# é indexado também pela cor, e entradas antigas trazem métricas de outra fonte — o que
# fazia a mesma frase ser quebrada em duas linhas dependendo da cor pedida.
def text(content, size=24, color=WHITE, opacity=1.0, **kwargs):
    return screen_text(content, size, **kwargs).set_color(color).set_opacity(opacity)


def display(content, size=38):
    return screen_text(content, size, oversample=2).set_color(WHITE)


def tag(content, size=26, opacity=1.0, color=WHITE):
    """Mensagem de uma linha, limitada à margem; falha se o Pango quebrar a linha."""
    t = screen_text(content, size, oversample=2).set_color(color).set_opacity(opacity)
    t.scale_to_fit_width(min(t.width, 2 * SAFE_X - 0.4))
    assert t.height < 0.60, f"o Pango quebrou a linha: {content!r}"
    return t


def fit(m, w=2 * SAFE_X - 0.3):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def soft_swap(old, new, shift=UP * 0.12, lag=0.55):
    """Sai e entra em sequência: evita dois textos legíveis na mesma posição."""
    return AnimationGroup(FadeOut(old, shift=shift), FadeIn(new, shift=shift), lag_ratio=lag)


def vec(a, b, color, width=6):
    return Arrow(a, b, buff=0, stroke_width=width, tip_length=0.2, max_tip_length_to_length_ratio=0.35,
                 max_stroke_width_to_length_ratio=30, color=color)


def boxed(mob, color=WHITE, op=1.0):
    return VGroup(mob, SurroundingRectangle(mob, color=color, buff=0.15, corner_radius=0.08,
                                            stroke_width=2.5).set_stroke(opacity=op))


def odot(c, color=CYAN, op=1.0, r=0.145):
    """Seção de fio com corrente saindo do plano."""
    return VGroup(Circle(r, color=color, stroke_width=3).set_stroke(opacity=op),
                  Dot(ORIGIN, 0.055, color=color).set_opacity(op)).move_to(c)


def otimes(c, color=CYAN, op=1.0, r=0.145):
    """Seção de fio com corrente entrando no plano."""
    d = r * 0.68
    return VGroup(Circle(r, color=color, stroke_width=3).set_stroke(opacity=op),
                  Line([-d, -d, 0], [d, d, 0]).set_stroke(color, 3, op),
                  Line([-d, d, 0], [d, -d, 0]).set_stroke(color, 3, op)).move_to(c)


def plate(m):
    """Fundo opaco atrás de um rótulo: sobre as setas do campo ele se perderia."""
    bg = SurroundingRectangle(m, buff=0.11).set_stroke(width=0).set_fill(BACKGROUND_COLOR, 1.0)
    return VGroup(bg, m)


def right_angle(corner, u, v, size=0.16, color=WHITE, op=0.8):
    return VMobject().set_points_as_corners(
        [corner + u * size, corner + (u + v) * size, corner + v * size]).set_stroke(color, 2, op)


def span_mark(a, b, color, ticks=0.11, width=2.5, op=0.9):
    """Cota: segmento fino com traços nas pontas (não é vetor)."""
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0], 0.0]) * ticks
    return VGroup(Line(a, b), Line(a - n, a + n), Line(b - n, b + n)).set_stroke(color, width, op)


def angle_arc(vertex, a, b, radius=0.42, color=WHITE, op=0.9, width=3):
    """Arco do ângulo em `vertex` entre as direções de `a` e de `b`."""
    va, vb = a - vertex, b - vertex
    t0 = float(np.arctan2(va[1], va[0]))
    t1 = float(np.arctan2(vb[1], vb[0]))
    d = (t1 - t0 + PI) % (2 * PI) - PI
    return Arc(radius=radius, start_angle=t0, angle=d, arc_center=vertex).set_stroke(color, width, op)


class CampoSolenoide008(Scene):
    # ── Infraestrutura ──────────────────────────────────────────────────────
    def check_safe(self):
        """Texto e equações dentro da margem e acima da faixa de legenda.

        A geometria do modelo ideal (que sangra de propósito pelas laterais) fica em
        self.bleed e é ignorada.
        """
        skip = set()
        for m in self.bleed:
            skip.update(id(x) for x in m.get_family())
        for m in self.mobjects:
            if not isinstance(m, VMobject) or id(m) in skip or not len(m.get_all_points()):
                continue
            who = getattr(m, "tex_string", None) or getattr(m, "text", None) or type(m).__name__
            assert m.get_bottom()[1] > SAFE_BOTTOM, \
                f"invade a faixa inferior: {m.get_bottom()[1]:.2f} [{who}]"
            assert m.get_left()[0] > -SAFE_X and m.get_right()[0] < SAFE_X, \
                f"fora da margem lateral: {m.get_left()[0]:.2f}..{m.get_right()[0]:.2f} [{who}]"

    def caption(self, *lines):
        """Troca a manchete do topo; devolve as animações (sem sobreposição legível)."""
        new = lines[0] if len(lines) == 1 and isinstance(lines[0], VMobject) else \
            VGroup(*(display(line) for line in lines)).arrange(DOWN, buff=0.14)
        fit(new, 2 * SAFE_X - 0.2)
        new.move_to([0, HEADLINE_TOP - new.height / 2, 0])
        anims = [soft_swap(self.headline, new, UP * 0.15)] if self.headline is not None \
            else [FadeIn(new, shift=DOWN * 0.15)]
        self.headline = new
        return anims

    def note(self, new, *extra, run_time=0.55):
        """Linha auxiliar de uma frase; só entra depois que a anterior sai."""
        if new is not None:
            new.move_to([0, self.note_y, 0])
        if self.hint is not None and new is not None:
            anims = [soft_swap(self.hint, new, UP * 0.08)]
        elif new is not None:
            anims = [FadeIn(new, shift=UP * 0.08)]
        elif self.hint is not None:
            anims = [FadeOut(self.hint, shift=UP * 0.08)]
        else:
            anims = []
        if anims or extra:
            self.play(*anims, *extra, run_time=run_time)
        self.hint = new

    def show_expr(self, new, *extra, run_time=1.0, match=True):
        """Troca a expressão ativa preservando os termos que continuam iguais."""
        fit(new).move_to([0, self.op_y, 0])
        if self.expr is None:
            anims = [FadeIn(new, shift=UP * 0.1)]
        elif match:
            anims = [TransformMatchingTex(self.expr, new)]
        else:
            anims = [soft_swap(self.expr, new)]
        self.play(*anims, *extra, run_time=run_time)
        self.expr = new
        return new

    def push_chip(self, s, size=24):
        """Guarda um resultado já obtido na prateleira inferior e devolve as animações."""
        t = tex(s, size, WHITE).set_opacity(0.9)
        chip = VGroup(t, SurroundingRectangle(t, color=WHITE, buff=0.11, corner_radius=0.07,
                                              stroke_width=1.8).set_stroke(opacity=0.45))
        old = list(self.shelf)
        self.shelf.add(chip)
        layout = VGroup(*(m.copy() for m in self.shelf)).arrange(RIGHT, buff=0.28)
        fit(layout, 2 * SAFE_X - 0.2).move_to([0, SHELF_Y, 0])
        chip.move_to(layout[-1])
        return [m.animate.move_to(layout[i]) for i, m in enumerate(old)] + \
               [FadeIn(chip, shift=UP * 0.12)]

    # ── Bloco da derivação: espira única, grande ────────────────────────────
    def dgeo(self):
        """Raio e centro da espira da derivação; em morph = 1 vira a 1ª espira da bobina."""
        m = self.dmorph.get_value()
        return DR + (RS - DR) * m, DOX * (1 - m), DOY + (AX_Y - DOY) * m

    def dpt(self, phi):
        """Ponto da espira: y = R cos(phi), profundidade R sin(phi) achatada por DTILT."""
        r, cx, cy = self.dgeo()
        return np.array([cx + r * DTILT * np.sin(phi), cy + r * np.cos(phi), 0.0])

    def deriv_loop(self):
        """Espira da derivação; metade de trás (sin phi < 0) mais apagada."""
        op = self.dloop_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        for near in (False, True):
            phis = np.linspace(0, PI, 41) + (0 if near else PI)
            g.add(VMobject().set_points_as_corners([self.dpt(p) for p in phis])
                  .set_stroke(BLUE, 7, op * (1.0 if near else 0.38)))
        return g

    def deriv_sweep(self):
        """Varredura phi: 0 -> 2pi, a volta que a integral percorre acumulando dB_z."""
        end, op = self.sweep.get_value(), self.dloop_op.get_value()
        g = VGroup()
        if end < 1e-3 or op < 0.01:
            return g
        for a, b, o in ((0.0, min(end, PI), 1.0), (PI, end, 0.38)):
            if b > a + 1e-3:
                pts = [self.dpt(p) for p in np.linspace(a, b, max(2, int(36 * (b - a))))]
                g.add(VMobject().set_points_as_corners(pts).set_stroke(CYAN, 11, op * o))
        return g.add(Dot(self.dpt(end), 0.11, color=CYAN).set_opacity(op))

    def d_p(self):
        """Ponto P sobre o eixo, a z do centro (z = self.dz, em unidades de R)."""
        return np.array([DOX + DR * self.dz.get_value(), DOY, 0.0])

    def deriv_tri(self):
        """Catetos z (magenta) e hipotenusa r (violeta) + P: seguem z e colapsam em z = 0."""
        op = self.tri_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        p, zl = self.d_p(), DR * self.dz.get_value()
        if zl > 0.14:
            g.add(Line(D_O, p).set_stroke(MAGENTA, 4, op))
            g.add(tex("z", 38, MAGENTA).move_to([(DOX + p[0]) / 2, DOY - 0.36, 0]).set_opacity(op))
        g.add(Line(D_TOP, p).set_stroke(VIOLET, 5, op))
        g.add(tex("r", 38, VIOLET).move_to((D_TOP + p) / 2 + np.array([0.32, 0.26, 0])).set_opacity(op))
        pop = op * self.p_op.get_value()
        if pop > 0.01:
            g.add(Dot(p, 0.1, color=WHITE).set_opacity(pop))
            g.add(tex("P", 36).move_to(p + np.array([0.06, -0.38, 0])).set_opacity(pop))
        return g

    def deriv_axial(self):
        """Seta axial em P: some com z = 0 continua puramente axial."""
        op = self.dax_op.get_value()
        if op < 0.01:
            return VMobject()
        p = self.d_p()
        return vec(p, p + RIGHT * 0.82, WHITE, 8).set_opacity(op)

    # ── Bobina pseudo-3D e modelo contínuo ──────────────────────────────────
    def coil_pt(self, zc, phi):
        t = self.tilt.get_value()
        return np.array([RS * (zc + t * np.sin(phi)), AX_Y + RS * np.cos(phi), 0.0])

    def coil(self):
        """Espiras discretas; some conforme self.cont funde tudo na distribuição contínua."""
        op0 = self.coil_op.get_value() * (1.0 - self.cont.get_value())
        g = VGroup()
        if op0 < 0.01:
            return g
        zs, w = turn_centers(self.nf.get_value())
        keep = [(zc, wi) for zc, wi in zip(zs, w) if abs(RS * zc) < X_VIS]
        for near in (False, True):
            phis = np.linspace(0, PI, 25) + (0 if near else PI)
            for zc, wi in keep:
                pts = [self.coil_pt(zc, p) for p in phis]
                g.add(VMobject().set_points_as_corners(pts)
                      .set_stroke(BLUE, 6, op0 * wi * (1.0 if near else 0.38)))
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
            g.add(vec(c + UP * 0.26, c + DOWN * 0.26, CYAN, 4).set_opacity(op * 0.95))
        return g

    def b_len(self, z=0.0):
        return LB * b_sum(z, self.nf.get_value()) / B_IDEAL

    def b_arrow(self):
        """Resultante axial: comprimento = soma real das contribuições das espiras."""
        op, L = self.bres_op.get_value(), self.b_len()
        if op < 0.01 or L < 0.03:
            return VMobject()
        a = np.array([0.0, AX_Y, 0.0])
        return vec(a, a + RIGHT * L, WHITE, 8).set_opacity(op)

    def contrib_bar(self):
        """As parcelas enfileiradas: mesma origem em x e mesmo total da resultante.

        self.focus destaca uma parcela por vez (as outras recuam).
        """
        op = self.bar_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        zs, w = turn_centers(self.nf.get_value())
        foc = self.focus.get_value()
        x = BAR_X0
        for j, (zc, wi) in enumerate(zip(zs, w)):
            L = LB * float(wi * b_loop(0.0, zc)) / B_IDEAL
            if L < 2e-3:
                continue
            a = 1.0 if foc < 0 else (1.0 if abs(j - foc) < 0.5 else 0.3)
            g.add(Line([x, BAR_Y, 0], [x + L, BAR_Y, 0])
                  .set_stroke(CYAN, 15, op * a * (1.0 if j % 2 else 0.78)))
            x += L
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
        zs, w = turn_centers(self.nf.get_value())
        j = int(round(foc))
        if j >= len(zs):
            return VMobject()
        x = BAR_X0 + sum(LB * float(w[i] * b_loop(0.0, zs[i])) / B_IDEAL for i in range(j))
        L = LB * float(w[j] * b_loop(0.0, zs[j])) / B_IDEAL
        return DashedLine([RS * zs[j], AX_Y - RS, 0], [x + L / 2, BAR_Y + 0.14, 0],
                          dash_length=0.08).set_stroke(CYAN, 2.5, 0.8 * op)

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
        return VMobject().set_points_as_corners(pts).set_stroke(CYAN, 5, op)

    # ── Corte longitudinal 2D ───────────────────────────────────────────────
    def cut_rows(self):
        """Fileira de cima em (.), de baixo em (x) — marcas esquemáticas da corrente.

        Regra da mão direita: com x^ para a direita, y^ para cima e z^out saindo da tela,
        o fio de cima (y = +R, corrente +z^out) dá no eixo j x r^ ~ z^out x (-y^) = +x^;
        o de baixo (y = -R, corrente -z^out) dá (-z^out) x (+y^) = +x^. Campo interno para
        a DIREITA, coerente com a bobina pseudo-3D e com db_dirs.
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
                g.add(odot([x, AX_Y + RS, 0], CYAN, op), otimes([x, AX_Y - RS, 0], CYAN, op))
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
            if L < 0.04:
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
        y = self.amp_y.get_value()
        for dy in (-RECT_H / 2, RECT_H / 2):
            for x in (0.45, 1.25):
                g.add(vec([x, y + dy, 0], [x + 0.55, y + dy, 0], WHITE, 4).set_opacity(op * 0.85))
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
        self.camera.background_color = BACKGROUND_COLOR
        self.headline = self.hint = self.expr = None
        self.op_y, self.note_y = DER_OP_Y, DER_NOTE_Y
        self.shelf = VGroup()
        watermark = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(watermark.to_corner(UP + RIGHT, buff=0.28))
        series = text("DA EQUAÇÃO AO FENÔMENO · EP. 03", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4)

        self.dloop_op, self.sweep, self.dmorph = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.dz, self.tri_op, self.p_op, self.dax_op = (ValueTracker(v) for v in (DZ, 0, 0, 0))
        self.nf, self.tilt, self.cont = ValueTracker(1.0), ValueTracker(DTILT), ValueTracker(0)
        self.coil_op, self.cur_op, self.bres_op, self.bar_op = (ValueTracker(0) for _ in range(4))
        self.focus = ValueTracker(-1)
        self.tie_op, self.ext_op, self.curve_op = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.cut_op, self.zlim, self.extra_op = ValueTracker(0), ValueTracker(9.25), ValueTracker(0)
        self.bin_op, self.cur, self.cutext_op = ValueTracker(0), ValueTracker(1), ValueTracker(0)
        self.amp_op, self.amp_y, self.side_op = ValueTracker(0), ValueTracker(Y_OUT), ValueTracker(0)
        self.act1, self.act2, self.actL, self.actR = (ValueTracker(0) for _ in range(4))
        self.ell_op, self.bout_op, self.enc_n = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.add(self.nf, self.cur, self.sweep, self.dz, self.focus, self.enc_n)

        dloop = always_redraw(self.deriv_loop)
        dsweep = always_redraw(self.deriv_sweep)
        dtri = always_redraw(self.deriv_tri)
        daxial = always_redraw(self.deriv_axial)
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
        self.add(extl, dloop, dsweep, sheet, coil, marks, rows, walls, cext, cfield, dtri, daxial,
                 bres, bar, tie, flink, curve, ofield, rect, dirs, sides, ell, enc)
        self.bleed = [series, coil, sheet, marks, extl, rows, walls, cext, cfield, curve, enc]
        self.add(series)

        # ══ C1. A pergunta e a espira (0–2 s) ═══════════════════════════════════════
        self.play(FadeIn(series), *self.caption("COMO ENROLAR UM FIO", "REFORÇA O CAMPO",
                                                "DENTRO DA BOBINA?"),
                  self.dloop_op.animate.set_value(1), run_time=0.77)
        el_top = odot(D_TOP, CYAN)
        i_lab = tex("I", 36, CYAN).next_to(el_top, LEFT, 0.16)
        self.play(FadeIn(el_top), FadeIn(i_lab), run_time=0.5)
        self.note(tag("uma espira de raio R, percorrida por I", 23, 0.85))
        self.check_safe()
        self.wait(BEAT)

        # ══ C2. Geometria: r² = R² + z², construído dos rótulos (2–10 s) ════════════
        self.play(*self.caption("DE ONDE VEM A FÓRMULA"), FadeOut(i_lab), run_time=0.52)
        axis_line = DashedLine(D_O + LEFT * 0.55, D_P + RIGHT * 1.15, dash_length=0.12
                               ).set_stroke(BLUE, 2, 0.55)
        z_axis_lab = tex("z", 30, MAGENTA).move_to(D_P + np.array([1.35, 0.0, 0])).set_opacity(0.8)
        self.play(Create(axis_line), FadeIn(z_axis_lab), run_time=0.52)
        seg_R = Line(D_O, D_TOP).set_stroke(BLUE, 4)
        lab_R = tex("R", 38, BLUE).move_to(D_O + np.array([-0.30, DR / 2, 0]))
        corner = right_angle(D_O, np.array([1, 0, 0]), np.array([0, 1, 0]), 0.22, WHITE, 0.6)
        self.play(Create(seg_R), FadeIn(lab_R), Create(corner),
                  self.tri_op.animate.set_value(1), self.p_op.animate.set_value(1), run_time=0.72)
        self.note(tag("P no eixo, a uma distância z do centro", 23, 0.85))
        self.wait(BEAT)

        lab_z = tex("z", 38, MAGENTA).move_to([(DOX + D_P[0]) / 2, DOY - 0.36, 0])
        lab_r = tex("r", 38, VIOLET).move_to((D_TOP + D_P) / 2 + np.array([0.32, 0.26, 0]))
        pit = mtex("r^2", "=", "R^2", "+", "z^2", size=54)
        pit[0].set_color(VIOLET), pit[2].set_color(BLUE), pit[4].set_color(MAGENTA)
        fit(pit).move_to([0, self.op_y, 0])
        self.play(TransformFromCopy(lab_r, pit[0]), TransformFromCopy(lab_R, pit[2]),
                  TransformFromCopy(lab_z, pit[4]), FadeIn(pit[1]), FadeIn(pit[3]), run_time=0.88)
        self.expr = pit
        self.note(tag("Pitágoras no triângulo R–z–r", 23, 0.9))
        self.check_safe()
        self.wait(READ_RES)

        # a identidade fica guardada: vamos precisar dela no fim da derivação
        ref_tex = mtex("r^2", "=", "R^2", "+", "z^2", size=30)
        ref_tex[0].set_color(VIOLET), ref_tex[2].set_color(BLUE), ref_tex[4].set_color(MAGENTA)
        ref = boxed(ref_tex, WHITE, 0.4).move_to(DER_REF)
        ref_tex.set_opacity(0.85)
        self.play(TransformFromCopy(pit, ref[0]), FadeIn(ref[1]), run_time=0.58)
        self.wait(0.5)

        # ══ C3. Biot-Savart: a contribuição de um elemento (10–18 s) ════════════════
        self.play(*self.caption("BIOT-SAVART"), run_time=0.52)
        bs = mtex(r"d\vec B", "=", r"\frac{\mu_0 I}{4\pi}", r"\frac{d\vec\ell\times\vec r}{r^3}", size=46)
        bs[3][:3].set_color(CYAN)
        self.show_expr(bs, run_time=0.58, match=False)
        dl_lab = tex(r"d\vec\ell", 34, CYAN).next_to(el_top, UP, 0.16)
        rhat = (D_P - D_TOP) / np.linalg.norm(D_P - D_TOP)
        perp_mark = right_angle(D_TOP, rhat, np.array([-rhat[1], rhat[0], 0.0]), 0.2, CYAN, 0.9)
        self.play(Indicate(el_top, color=CYAN, scale_factor=1.5), FadeIn(dl_lab), run_time=0.52)
        self.play(Create(perp_mark), run_time=0.5)
        self.note(tag("dℓ sai do plano do corte: é perpendicular a r", 22, 0.9))
        self.wait(READ)
        mag = mtex(r"\left|d\vec B\right|", "=", r"\frac{\mu_0 I}{4\pi}", r"\frac{d\ell}{r^2}", size=46)
        self.show_expr(mag, run_time=0.62)
        self.note(tag("com dℓ perpendicular a r, o produto vira dℓ · r", 22, 0.9))
        self.wait(BEAT)
        d1, d2 = db_dirs(DZ)
        u1, u2 = d1 / np.linalg.norm(d1), d2 / np.linalg.norm(d2)
        db1 = vec(D_P, D_P + LDB * u1, CYAN, 6)
        db1_lab = tex(r"d\vec B_1", 30, CYAN).next_to(db1.get_end(), RIGHT, 0.1)
        self.play(Create(db1), FadeIn(db1_lab), run_time=0.52)
        self.check_safe()
        self.wait(READ)

        # ══ C4. O par de elementos: transversais se cancelam, soma = 2 dB_z (18–28 s) ══
        self.play(*self.caption("O PAR DE ELEMENTOS"), FadeOut(perp_mark), run_time=0.52)
        el_bot = otimes(D_BOT, CYAN)
        seg_r2 = Line(D_BOT, D_P).set_stroke(VIOLET, 4, 0.5)
        db2 = vec(D_P, D_P + LDB * u2, CYAN, 6)
        db2_lab = tex(r"d\vec B_2", 30, CYAN).next_to(db2.get_end(), RIGHT, 0.1)
        self.play(FadeIn(el_bot), Create(seg_r2), Create(db2), FadeIn(db2_lab), run_time=0.64)

        a_len = LDB * float(u1[0])                     # projeção axial de UMA contribuição
        ax_end = D_P + RIGHT * a_len
        tr1 = DashedLine(D_P + LDB * u1, ax_end, dash_length=0.09).set_stroke(CYAN, 3)
        tr2 = DashedLine(D_P + LDB * u2, ax_end, dash_length=0.09).set_stroke(CYAN, 3)
        ax1 = vec(D_P, ax_end, WHITE, 6)
        self.play(Create(tr1), Create(tr2), Create(ax1), run_time=0.64)
        zero_mark = tex(r"\vec 0", 30, WHITE).move_to(D_P + np.array([0.55, 0.0, 0]))
        self.play(FadeOut(VGroup(tr1, tr2, db1, db2, db1_lab, db2_lab)),
                  FadeIn(zero_mark, scale=1.4), run_time=0.58)
        self.note(tag("as transversais são opostas e se cancelam", 22, 0.9))
        self.wait(READ)

        # soma ponta-cauda: a parcela do segundo elemento parte da ponta da primeira
        ax2 = vec(ax_end, ax_end + RIGHT * a_len, WHITE, 6)
        self.play(FadeOut(zero_mark), Create(ax2), run_time=0.58)
        sum_span = span_mark(D_P + DOWN * 0.42, ax_end + RIGHT * a_len + DOWN * 0.42, WHITE, op=0.8)
        sum_lab = tex(r"2\,dB_z", 32).next_to(sum_span, DOWN, 0.1)
        self.play(Create(sum_span), FadeIn(sum_lab), run_time=0.52)
        self.note(tag("o par soma duas vezes a projeção de uma", 22, 0.9))
        self.check_safe()
        self.wait(READ)
        one_lab = tex("dB_z", 32).next_to(ax1, UP, 0.12)
        self.play(FadeOut(VGroup(ax2, sum_span, sum_lab)), FadeIn(one_lab), run_time=0.58)
        self.note(tag("a integral segue com a parcela de UM elemento", 22, 0.9))
        self.wait(READ)

        # ══ C5. A projeção: dB_z / dB = R / r (28–35 s) ═════════════════════════════
        self.play(*self.caption("A PROJEÇÃO AXIAL"), run_time=0.52)
        db1b = vec(D_P, D_P + LDB * u1, CYAN, 5)
        tr1b = DashedLine(D_P + LDB * u1, ax_end, dash_length=0.09).set_stroke(CYAN, 2.5, 0.7)
        arc_p = angle_arc(D_P, D_P + RIGHT, D_P + u1, 0.5, WHITE, 0.95)
        arc_e = angle_arc(D_TOP, D_O, D_P, 0.5, WHITE, 0.95)
        al_p = tex(r"\alpha", 28).move_to(D_P + np.array([0.88, 0.26, 0]))
        al_e = tex(r"\alpha", 28).move_to(D_TOP + np.array([0.26, -0.58, 0]))
        self.play(Create(db1b), Create(tr1b), Create(arc_p), FadeIn(al_p),
                  Create(arc_e), FadeIn(al_e), run_time=0.82)
        self.note(tag("o mesmo ângulo aparece no triângulo e em P", 22, 0.9))
        self.wait(READ)
        proj = mtex(r"\frac{dB_z}{\left|d\vec B\right|}", "=", r"\cos\alpha", "=", r"\frac{R}{r}", size=46)
        proj[4][0].set_color(BLUE), proj[4][2].set_color(VIOLET)
        fit(proj).move_to([0, self.op_y, 0])
        self.play(soft_swap(self.expr, proj), run_time=0.64)
        self.expr = proj
        self.play(Indicate(lab_R, color=BLUE, scale_factor=1.4),
                  Indicate(lab_r, color=VIOLET, scale_factor=1.4), run_time=0.52)
        self.check_safe()
        self.wait(READ)

        chain = mtex(r"dB_z", "=", r"\frac{\mu_0 I}{4\pi}", r"\frac{d\ell}{r^2}", r"\cdot",
                     r"\frac{R}{r}", size=44)
        chain[5][0].set_color(BLUE), chain[5][2].set_color(VIOLET)
        self.show_expr(chain, run_time=0.62, match=False)

        # ══ C6. dℓ = R dφ e o encaixe dos fatores (35–45 s) ═════════════════════════
        self.play(*self.caption("PERCORRENDO A ESPIRA"),
                  FadeOut(VGroup(arc_p, arc_e, al_p, al_e, db1b, tr1b)), run_time=0.52)
        aux = VGroup(Circle(AUX_R, color=BLUE, stroke_width=4).move_to(AUX_C),
                     Dot(AUX_C, 0.05, color=WHITE).set_opacity(0.7))
        p0, p1 = AUX_PHI, AUX_PHI + AUX_DPHI
        aux_arc = Arc(radius=AUX_R, start_angle=p0, angle=AUX_DPHI, arc_center=AUX_C
                      ).set_stroke(CYAN, 9)
        aux_r1 = Line(AUX_C, AUX_C + AUX_R * np.array([np.cos(p0), np.sin(p0), 0])
                      ).set_stroke(BLUE, 2.5, 0.8)
        aux_r2 = Line(AUX_C, AUX_C + AUX_R * np.array([np.cos(p1), np.sin(p1), 0])
                      ).set_stroke(BLUE, 2.5, 0.8)
        aux_ang = Arc(radius=0.26, start_angle=p0, angle=AUX_DPHI, arc_center=AUX_C
                      ).set_stroke(WHITE, 2.5, 0.9)
        aux_dphi = tex(r"d\phi", 26).move_to(AUX_C + 0.52 * np.array([np.cos((p0 + p1) / 2),
                                                                      np.sin((p0 + p1) / 2), 0]))
        aux_R = tex("R", 26, BLUE).move_to(AUX_C + np.array([-0.30, 0.26, 0]))
        aux_lab = text("vista de frente", 17, WHITE, 0.6).next_to(aux[0], DOWN, 0.10)
        self.play(FadeIn(aux), FadeIn(aux_lab), Create(aux_r1), Create(aux_r2),
                  Create(aux_arc), Create(aux_ang), FadeIn(aux_dphi), FadeIn(aux_R), run_time=0.76)
        dl_eq = mtex(r"d\ell", "=", "R", r"\,d\phi", size=40)
        dl_eq[0].set_color(CYAN), dl_eq[2].set_color(BLUE)
        dl_eq.next_to(aux[0], RIGHT, 0.42)
        self.play(TransformFromCopy(aux_arc, dl_eq[0]), FadeIn(dl_eq[1]),
                  TransformFromCopy(aux_R, dl_eq[2]), TransformFromCopy(aux_dphi, dl_eq[3]),
                  run_time=0.81)
        self.note(tag("o arco é o raio vezes o ângulo", 23, 0.9))
        self.check_safe()
        self.wait(READ)

        # R dφ voa para o lugar de dℓ na expressão ativa
        step2 = mtex(r"dB_z", "=", r"\frac{\mu_0 I}{4\pi}", r"\frac{R\,d\phi}{r^2}", r"\cdot",
                     r"\frac{R}{r}", size=44)
        step2[5][0].set_color(BLUE), step2[5][2].set_color(VIOLET)
        fit(step2).move_to([0, self.op_y, 0])
        flyer = VGroup(dl_eq[2], dl_eq[3]).copy()
        self.add(flyer)
        self.play(flyer.animate.move_to(step2[3].get_center()).set_opacity(0.0),
                  TransformMatchingTex(self.expr, step2), run_time=0.84)
        self.remove(flyer)
        self.expr = step2

        step3 = mtex(r"dB_z", "=", r"\frac{\mu_0 I}{4\pi}", r"\frac{R^2\,d\phi}{r^3}", size=44)
        self.play(Indicate(step2[3], color=BLUE, scale_factor=1.25),
                  Indicate(step2[5], color=BLUE, scale_factor=1.25), run_time=0.52)
        self.show_expr(step3, run_time=0.62)
        self.note(tag("os dois R viram R² e r²·r vira r³", 22, 0.9))
        self.wait(READ)

        step4 = mtex(r"dB_z", "=", r"\frac{\mu_0 I R^2}{4\pi\left(R^2+z^2\right)^{3/2}}",
                     r"\,d\phi", size=40)
        self.show_expr(step4, Indicate(ref, color=VIOLET, scale_factor=1.1), run_time=0.62)
        self.note(tag("r³ vem da identidade guardada", 23, 0.9))
        self.check_safe()
        self.wait(READ)

        # ══ C7. Integrar a volta inteira (45–56 s) ══════════════════════════════════
        self.play(*self.caption("SOMAR A VOLTA INTEIRA"),
                  FadeOut(VGroup(aux, aux_arc, aux_r1, aux_r2, aux_ang, aux_dphi, aux_R,
                                 aux_lab, dl_eq)), run_time=0.58)
        integ = mtex(r"B_z", "=", r"\int_0^{2\pi}", r"\frac{\mu_0 I R^2}{4\pi\left(R^2+z^2\right)^{3/2}}",
                     r"\,d\phi", size=38)
        fit(integ).move_to([0, self.op_y, 0])
        self.play(TransformMatchingTex(self.expr, integ),
                  self.sweep.animate.set_value(2 * PI), run_time=1.16, rate_func=linear)
        self.expr = integ
        self.note(tag("a volta inteira, somando só a parte axial", 22, 0.9))
        self.check_safe()
        self.wait(BEAT)
        self.play(Indicate(integ[3], color=WHITE, scale_factor=1.06), run_time=0.52)
        self.note(tag("R, z e I não dependem do ângulo: saem da integral", 21, 0.9))
        self.wait(BEAT)
        two_pi = tex(r"\int_0^{2\pi}\! d\phi = 2\pi", 36).move_to([0, self.op_y + 1.05, 0])
        self.play(FadeIn(two_pi, shift=UP * 0.1), run_time=0.5)
        pulled = mtex(r"B_z", "=", r"\frac{2\pi}{4\pi}", r"\frac{\mu_0 I R^2}{\left(R^2+z^2\right)^{3/2}}",
                      size=40)
        self.show_expr(pulled, FadeOut(two_pi), run_time=0.62, match=False)
        self.play(Indicate(pulled[2], color=MAGENTA, scale_factor=1.3), run_time=0.52)
        payoff = mtex(r"B_z(z)", "=", r"\frac{\mu_0 I R^2}{2\left(R^2+z^2\right)^{3/2}}", size=46)
        fit(payoff).move_to([0, self.op_y, 0])
        pbox = SurroundingRectangle(payoff, color=WHITE, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.play(TransformMatchingTex(self.expr, payoff), Create(pbox),
                  self.sweep.animate.set_value(0), run_time=0.84)
        self.expr = VGroup(payoff, pbox)
        self.note(tag("o campo no eixo de uma espira", 24, 0.95))
        self.check_safe()
        self.wait(READ_RES)

        # ══ C8. Checagem: P vai ao centro (56–63 s) ═════════════════════════════════
        self.play(*self.caption("CONFERINDO NO CENTRO"), run_time=0.52)
        self.play(self.dax_op.animate.set_value(1), FadeOut(one_lab), FadeOut(ax1),
                  FadeOut(seg_r2), run_time=0.5)
        self.note(tag("levando P até o centro: z → 0 e r → R", 22, 0.9))
        self.play(self.dz.animate.set_value(0.0), run_time=1.21)
        self.play(Indicate(lab_R, color=BLUE, scale_factor=1.4), run_time=0.5)
        at0 = mtex(r"B_z(0)", "=", r"\frac{\mu_0 I R^2}{2R^3}", "=", r"\frac{\mu_0 I}{2R}", size=44)
        fit(at0).move_to([0, self.op_y, 0])
        abox = SurroundingRectangle(at0, color=WHITE, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.play(soft_swap(self.expr, VGroup(at0, abox)), run_time=0.7)
        self.expr = VGroup(at0, abox)
        self.note(tag("R² sobre R³ é 1/R", 23, 0.9))
        self.check_safe()
        self.wait(READ_RES)

        # ══ C9. Superposição: a espira vira a primeira da bobina (63–76 s) ══════════
        self.play(*self.caption("AGORA EMPILHE ESPIRAS"),
                  FadeOut(VGroup(seg_R, lab_R, lab_r, lab_z, corner, axis_line, z_axis_lab,
                                 el_top, el_bot, dl_lab, ref)),
                  self.tri_op.animate.set_value(0), self.p_op.animate.set_value(0),
                  self.dax_op.animate.set_value(0), FadeOut(self.expr), FadeOut(self.hint),
                  run_time=0.64)
        self.expr = self.hint = None
        self.op_y, self.note_y = -2.95, -4.05
        self.play(self.dmorph.animate.set_value(1.0), run_time=0.9)
        self.play(self.dloop_op.animate.set_value(0), self.coil_op.animate.set_value(1),
                  self.cur_op.animate.set_value(1), run_time=0.5)
        eqz = mtex(r"B_z(z)", "=", r"\frac{\mu_0 I R^2}{2\left(R^2+z^2\right)^{3/2}}", size=40)
        self.show_expr(eqz, run_time=0.58, match=False)
        self.wait(0.7)
        eqj = mtex(r"B_j(z)", "=", r"\frac{\mu_0 I R^2}{2\left[R^2+(z-z_j)^2\right]^{3/2}}", size=38)
        self.show_expr(eqj, run_time=0.62)
        self.play(Indicate(eqj[2], color=MAGENTA, scale_factor=1.06), run_time=0.52)
        self.note(tag("a mesma fórmula, deslocada de z_j para cada espira", 21, 0.9))
        self.play(self.bres_op.animate.set_value(1), self.bar_op.animate.set_value(1), run_time=0.52)
        scale_lab = tex(r"B/B_1(0)", 26).move_to([BAR_X0 + 1.15, BAR_Y - 0.42, 0]).set_opacity(0.7)
        val = tex("1{,}00", 30).move_to([BAR_X0 + 2.55, BAR_Y, 0])
        self.play(FadeIn(scale_lab), FadeIn(val), self.tie_op.animate.set_value(1), run_time=0.52)
        self.check_safe()
        self.wait(BEAT)

        eqN = mtex("B(z)", "=", r"\sum_j B_j(z)", size=50)
        fit(eqN).move_to([0, self.op_y, 0])
        nbox = SurroundingRectangle(eqN, color=WHITE, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.play(soft_swap(self.expr, VGroup(eqN, nbox)), *self.caption("AS PARCELAS SE SOMAM"),
                  run_time=0.7)
        self.expr = VGroup(eqN, nbox)
        self.note(tag("mesma corrente e mesmo passo: a bobina fica mais longa", 21, 0.9))
        for n, v in ((2.0, "1{,}83"), (4.0, "2{,}85"), (8.0, "3{,}58")):
            self.play(self.nf.animate.set_value(n), run_time=0.7, rate_func=linear)
            new_val = tex(v, 30).move_to([BAR_X0 + 2.55, BAR_Y, 0])
            self.play(soft_swap(val, new_val), run_time=0.5)
            val = new_val
            self.wait(0.55)
        # uma parcela por vez, ligada à sua espira
        for j in (0, 3, 7):
            self.play(self.focus.animate.set_value(j), run_time=0.5)
            self.wait(0.4)
        self.play(self.focus.animate.set_value(-1), run_time=0.5)
        self.check_safe()
        self.wait(READ)

        # ══ C10. A bobina real: retornos e pontas (76–83 s) ═════════════════════════
        self.play(*self.caption("MAS A BOBINA REAL TEM PONTAS"),
                  FadeOut(VGroup(scale_lab, val)), self.bar_op.animate.set_value(0),
                  self.tie_op.animate.set_value(0), self.bres_op.animate.set_value(0),
                  self.cur_op.animate.set_value(0), FadeOut(self.expr), run_time=0.64)
        self.expr = None
        self.play(self.ext_op.animate.set_value(1), run_time=0.7)
        self.note(tag("o campo vaza e volta por fora (esboço qualitativo)", 21, 0.85))
        self.wait(BEAT)
        gz = tex("z", 30, MAGENTA).move_to([3.15, GY0 - 0.3, 0]).set_opacity(0.75)
        gb = tex("B", 30).move_to([-3.15, GY0 + GH + 0.25, 0]).set_opacity(0.7)
        gax = Line([-3.3, GY0, 0], [3.3, GY0, 0]).set_stroke(WHITE, 2, 0.35)
        band = VGroup(Rectangle(width=2.5, height=GH).set_stroke(width=0).set_fill(VIOLET, 0.22),
                      text("REGIÃO CENTRAL", 17, VIOLET, 0.95).move_to([0, GY0 + GH + 0.22, 0]))
        band[0].move_to([0, GY0 + GH / 2, 0])
        self.play(FadeIn(gax, gz, gb), self.curve_op.animate.set_value(1),
                  self.ext_op.animate.set_value(0), run_time=0.64)
        ends = VGroup(*(DashedLine([s * RS * 2.0, AX_Y - RS, 0], [s * RS * 2.0, GY0, 0],
                                   dash_length=0.09).set_stroke(MAGENTA, 2.5, 0.75) for s in (-1, 1)))
        self.play(Create(ends), FadeIn(band), run_time=0.58)
        self.note(tag("nas pontas, cerca de metade do valor central", 22, 0.9))
        self.check_safe()
        self.wait(READ_RES)

        # ══ C11. Idealização: até a distribuição contínua (83–90 s) ═════════════════
        self.play(*self.caption("IDEALIZE: SEM PONTAS"),
                  FadeOut(VGroup(gax, gz, gb, ends, band)),
                  self.curve_op.animate.set_value(0), run_time=0.58)
        self.play(self.nf.animate.set_value(18.0), run_time=0.77, rate_func=linear)
        self.note(tag("primeiro, um solenoide longo", 23, 0.85))
        self.play(self.nf.animate.set_value(N_INF), run_time=0.9, rate_func=linear)
        self.wait(0.6)
        self.play(self.cont.animate.set_value(1.0), run_time=0.97)
        ideal = tag("MODELO IDEAL · ENROLAMENTO CONTÍNUO E UNIFORME", 21, 0.9, VIOLET)
        ideal.move_to([0, 4.55, 0])
        self.play(FadeIn(ideal), run_time=0.5)
        self.note(tag("as espiras se fundem: uma distribuição uniforme", 22, 0.9))
        self.check_safe()
        self.wait(READ)

        # ══ C12. Simetria do modelo ideal (90–102 s) ════════════════════════════════
        self.play(*self.caption("O QUE A SIMETRIA EXIGE"), run_time=0.52)
        ps = np.array([0.0, AX_Y + 0.62, 0.0])
        pdot = Dot(ps, 0.09, color=WHITE)
        s_mark = span_mark(np.array([0.0, AX_Y, 0.0]), ps, MAGENTA, 0.08, 2.2, 0.85)
        s_lab = tex("s", 30, MAGENTA).next_to(s_mark, LEFT, 0.12)
        obs = VGroup(pdot, s_mark, s_lab)
        self.play(FadeIn(pdot), Create(s_mark), FadeIn(s_lab), run_time=0.52)
        # 1) translação ao longo de z: a vizinhança do ponto é sempre a mesma
        self.note(tag("deslize o ponto ao longo de z: tudo se repete", 22, 0.9))
        self.play(obs.animate.shift(RIGHT * 2.1), run_time=0.64)
        self.play(obs.animate.shift(LEFT * 4.2), run_time=0.91)
        self.wait(BEAT)
        # 2) pares de fatias simétricas em torno do plano transversal de P
        plane = DashedLine([0, AX_Y - RS - 0.45, 0], [0, AX_Y + RS + 0.45, 0],
                           dash_length=0.1).set_stroke(WHITE, 2, 0.5)
        sl = VGroup(*(Rectangle(width=0.30, height=2 * RS).set_stroke(width=0).set_fill(CYAN, 0.35)
                      .move_to([sg * 1.35, AX_Y, 0]) for sg in (-1, 1)))
        beta = 0.48
        f1 = vec(ps, ps + 1.05 * np.array([np.cos(beta), np.sin(beta), 0]), CYAN, 5)
        f2 = vec(ps, ps + 1.05 * np.array([np.cos(-beta), np.sin(-beta), 0]), CYAN, 5)
        f_lab = tag("contribuições das fatias · esquema, sem escala", 17, 0.9, CYAN)
        f_lab.move_to([0, AX_Y + 2.05, 0])
        self.play(Create(plane), FadeIn(sl), Create(f1), Create(f2), FadeIn(f_lab),
                  obs.animate.shift(RIGHT * 2.1), run_time=0.82)
        self.note(tag("duas fatias simétricas em torno do plano de P", 22, 0.9))
        self.wait(READ)
        fax = vec(ps, ps + RIGHT * (2 * 1.05 * np.cos(beta)), WHITE, 7)
        self.play(FadeOut(VGroup(f1, f2)), Create(fax), run_time=0.58)
        self.note(tag("as transversais se cancelam; sobra a axial", 22, 0.9))
        self.wait(BEAT)
        sym = mtex(r"\vec B", "=", "B(s)", r"\,\hat z", size=50)
        fit(sym).move_to([0, self.op_y, 0])
        sbox = SurroundingRectangle(sym, color=WHITE, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.play(FadeIn(VGroup(sym, sbox), shift=UP * 0.1),
                  FadeOut(VGroup(obs, fax, plane, sl, f_lab)), run_time=0.64)
        self.expr = VGroup(sym, sbox)
        self.note(tag("pode depender de s; a uniformidade vem de Ampère", 21, 0.9))
        self.check_safe()
        self.wait(READ_RES)

        # ══ C13. Corte longitudinal (102–105 s) ═════════════════════════════════════
        self.play(*self.caption("CORTE LONGITUDINAL"), FadeOut(self.expr), run_time=0.52)
        self.expr = None
        self.play(self.tilt.animate.set_value(0.0), run_time=0.7)
        self.play(self.coil_op.animate.set_value(0), self.cut_op.animate.set_value(1), run_time=0.58)
        self.play(self.bin_op.animate.set_value(1), run_time=0.52)
        rh1 = VGroup(tex(r"\odot", 32, CYAN), text("corrente saindo", 20, opacity=0.85)
                     ).arrange(RIGHT, buff=0.18).move_to([0, AX_Y + RS + 0.58, 0])
        rh2 = VGroup(tex(r"\otimes", 32, CYAN), text("corrente entrando", 20, opacity=0.85)
                     ).arrange(RIGHT, buff=0.18).move_to([0, AX_Y - RS - 0.58, 0])
        self.play(FadeIn(rh1), FadeIn(rh2), run_time=0.5)
        self.note(tag("mão direita: dentro, o campo aponta para a direita", 22, 0.9))
        self.check_safe()
        self.wait(BEAT)

        # ══ C14. Ampère: o quadro e o retângulo totalmente FORA (105–130 s) ═════════
        self.play(*self.caption("LEI DE AMPÈRE"), FadeOut(VGroup(rh1, rh2)),
                  self.bin_op.animate.set_value(0.4), FadeOut(self.hint), run_time=0.58)
        self.hint = None
        self.op_y, self.note_y = AMP_OP_Y, AMP_SIDE_Y
        law = mtex(r"\oint \vec B\cdot d\vec\ell", "=", r"\mu_0 I_{\text{enc}}", size=40)
        law.move_to([0, AMP_LAW_Y, 0]).set_opacity(0.8)
        self.play(FadeIn(law, shift=UP * 0.1), run_time=0.52)
        self.play(*self.push_chip(r"\vec B = B(s)\,\hat z"), run_time=0.58)
        self.play(self.amp_op.animate.set_value(1), self.side_op.animate.set_value(1),
                  self.ell_op.animate.set_value(1), self.bout_op.animate.set_value(1), run_time=0.64)
        self.note(tag("um retângulo inteiramente fora do solenoide", 22, 0.9))
        self.check_safe()
        self.wait(BEAT)

        ienc0 = mtex(r"I_{\text{enc}}", "=", "0", size=44)
        fit(ienc0).move_to([0, self.op_y, 0])
        self.play(FadeIn(ienc0, shift=UP * 0.1), run_time=0.52)
        self.expr = ienc0
        self.note(tag("nenhuma corrente atravessa essa superfície", 22, 0.9))
        self.wait(BEAT)

        # percorrer e iluminar cada lado, levando sua parcela à equação
        terms = VGroup(tex(r"B(s_1)\,\ell", 42), tex("+\\,0", 42), tex(r"-\,B(s_2)\,\ell", 42),
                       tex("+\\,0", 42), tex("=\\,0", 42)).arrange(RIGHT, buff=0.16)
        fit(terms).move_to([0, self.op_y, 0])
        self.play(soft_swap(self.expr, terms[0]), self.act1.animate.set_value(1), run_time=0.64)
        self.wait(0.7)
        self.play(FadeIn(terms[1], shift=RIGHT * 0.1), self.actR.animate.set_value(1),
                  self.act1.animate.set_value(0.35), run_time=0.52)
        self.wait(0.5)
        self.play(FadeIn(terms[2], shift=RIGHT * 0.1), self.act2.animate.set_value(1),
                  self.actR.animate.set_value(0.35), run_time=0.52)
        self.wait(0.5)
        self.play(FadeIn(terms[3], shift=RIGHT * 0.1), self.actL.animate.set_value(1),
                  self.act2.animate.set_value(0.35), run_time=0.52)
        self.wait(0.5)
        self.play(FadeIn(terms[4], shift=RIGHT * 0.1), self.actL.animate.set_value(0.35),
                  Indicate(law[2], color=WHITE, scale_factor=1.15), run_time=0.52)
        self.expr = terms
        self.note(tag("os lados curtos são perpendiculares a B: valem zero", 21, 0.9))
        self.check_safe()
        self.wait(READ)

        noz = mtex(r"B(s_1)\,\ell", "-", r"B(s_2)\,\ell", "=", "0", size=44)
        fit(noz).move_to([0, self.op_y, 0])
        self.play(FadeOut(terms[1], scale=0.3), FadeOut(terms[3], scale=0.3), run_time=0.5)
        self.expr = VGroup(terms[0], terms[2], terms[4])
        self.play(soft_swap(self.expr, noz), run_time=0.58)
        self.expr = noz
        self.wait(BEAT)
        divl = mtex("B(s_1)", "=", "B(s_2)", size=46)
        self.show_expr(divl, run_time=0.62)
        self.note(tag("dividindo por ℓ > 0", 23, 0.9))
        self.wait(BEAT)
        constf = mtex(r"B_{\text{fora}}(s)", "=", r"\text{constante}", size=42)
        self.show_expr(constf, run_time=0.62, match=False)
        self.note(tag("por fora, B não muda com a distância", 22, 0.9))
        self.check_safe()
        self.wait(READ)

        # a condição física, em outra linha, visível junto com a conclusão anterior
        cond = VGroup(text("campo do solenoide, sem campo externo imposto", 18, WHITE, 0.8),
                      mtex("B(s)", r"\longrightarrow", "0", r"\quad (s\to\infty)", size=34)
                      ).arrange(DOWN, buff=0.10).move_to([0, AMP_SIDE_Y + 0.05, 0])
        self.note(None)
        self.play(FadeIn(cond, shift=UP * 0.1), run_time=0.58)
        self.wait(READ)
        zero = mtex(r"B_{\text{fora}}", "=", "0", size=50)
        fit(zero).move_to([0, self.op_y, 0])
        zbox = SurroundingRectangle(zero, color=WHITE, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.play(TransformFromCopy(constf, zero), Indicate(cond[1], color=WHITE, scale_factor=1.1),
                  FadeOut(self.expr), run_time=0.84)
        self.play(Create(zbox), self.bout_op.animate.set_value(0), run_time=0.5)
        self.expr = VGroup(zero, zbox)
        self.check_safe()
        self.wait(READ_RES)
        self.play(FadeOut(cond), *self.push_chip(r"B_{\text{fora}} = 0"),
                  FadeOut(self.expr), run_time=0.64)
        self.expr = None

        # ══ C15. O MESMO retângulo, agora DENTRO (130–136 s) ════════════════════════
        self.play(*self.caption("O MESMO RETÂNGULO, AGORA DENTRO"),
                  self.act1.animate.set_value(0), self.act2.animate.set_value(0),
                  self.actL.animate.set_value(0), self.actR.animate.set_value(0), run_time=0.58)
        self.play(self.amp_y.animate.set_value(Y_IN), run_time=0.97)
        in_eq = mtex(r"I_{\text{enc}}=0", r"\;\Rightarrow\;", "B(s_1)", "=", "B(s_2)", size=40)
        fit(in_eq).move_to([0, self.op_y, 0])
        self.play(FadeIn(in_eq, shift=UP * 0.1), self.act1.animate.set_value(1),
                  self.act2.animate.set_value(1), run_time=0.58)
        self.expr = in_eq
        self.wait(BEAT)
        uni = mtex(r"B_{\text{dentro}}", "=", r"\text{constante}", size=44)
        self.show_expr(uni, run_time=0.62, match=False)
        self.check_safe()
        self.wait(READ)
        self.play(*self.push_chip(r"B_{\text{dentro}} = \text{const.}"), FadeOut(self.expr),
                  run_time=0.64)
        self.expr = None

        # ══ C16. ATRAVESSANDO a parede: B = mu0 n I (136–154 s) ═════════════════════
        self.play(*self.caption("AGORA ATRAVESSANDO A PAREDE"),
                  self.act1.animate.set_value(0), self.act2.animate.set_value(0), run_time=0.58)
        self.play(self.amp_y.animate.set_value(Y_WALL), run_time=0.9)
        self.wait(0.6)
        cont_eq = mtex(r"\oint \vec B\cdot d\vec\ell", "=", r"B\,\ell", size=46)
        fit(cont_eq).move_to([0, self.op_y, 0])
        self.play(FadeIn(cont_eq[0], shift=UP * 0.1), self.act1.animate.set_value(1), run_time=0.52)
        self.play(FadeIn(cont_eq[1]), FadeIn(cont_eq[2]), run_time=0.5)
        self.expr = cont_eq
        self.note(tag("só o lado de dentro contribui", 23, 0.9))
        self.wait(0.8)
        self.play(self.actL.animate.set_value(1), self.actR.animate.set_value(1), run_time=0.5)
        self.note(tag("laterais perpendiculares e lado externo nulo: zero", 21, 0.9))
        self.play(self.actL.animate.set_value(0.3), self.actR.animate.set_value(0.3),
                  self.act2.animate.set_value(0.3), run_time=0.5)
        self.check_safe()
        self.wait(BEAT)

        # contar as seis seções de UMA fileira
        self.play(self.enc_n.animate.set_value(6.0), run_time=1.29, rate_func=linear)
        nl = mtex(r"N_\ell", "=", r"n\,\ell", size=44).move_to([0, AMP_SIDE_Y, 0])
        self.note(None)
        self.play(FadeIn(nl, shift=UP * 0.1), run_time=0.52)
        self.wait(BEAT)
        ienc = mtex(r"I_{\text{enc}}", "=", r"n\,\ell\,I", size=44).move_to([0, AMP_SIDE_Y, 0])
        self.play(soft_swap(nl, ienc), run_time=0.58)
        self.check_safe()
        self.wait(BEAT)

        # cópias de B l e n l I entram na lei ancorada
        full = mtex("B", r"\ell", "=", r"\mu_0", "n", r"\ell", "I", size=50)
        fit(full).move_to([0, self.op_y, 0])
        self.play(Indicate(law, color=WHITE, scale_factor=1.06), run_time=0.5)
        self.play(TransformFromCopy(cont_eq[2], VGroup(full[0], full[1])),
                  TransformFromCopy(ienc[2], VGroup(full[4], full[5], full[6])),
                  FadeIn(full[2]), FadeIn(full[3]),
                  FadeOut(cont_eq), FadeOut(ienc), run_time=0.9)
        self.expr = full
        self.check_safe()
        self.wait(BEAT)
        self.play(full[1].animate.set_color(MAGENTA), full[5].animate.set_color(MAGENTA),
                  Indicate(full[1], color=MAGENTA, scale_factor=1.4),
                  Indicate(full[5], color=MAGENTA, scale_factor=1.4), run_time=0.58)
        self.note(tag("dividindo os dois lados por ℓ", 23, 0.9))
        self.play(full[1].animate.scale(0.1).set_opacity(0),
                  full[5].animate.scale(0.1).set_opacity(0), run_time=0.5)
        res = mtex("B", "=", r"\mu_0", "n", "I", size=58)
        fit(res).move_to([0, self.op_y, 0])
        rbox = SurroundingRectangle(res, color=WHITE, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.play(TransformMatchingTex(full, res), Create(rbox), run_time=0.7)
        self.expr = VGroup(res, rbox)
        self.note(tag("exato no modelo ideal, com as premissas ao lado", 21, 0.95))
        self.check_safe()
        self.wait(READ_RES + 0.7)

        # ══ C17. De volta ao solenoide real (154–159 s) ═════════════════════════════
        self.play(*self.caption("DE VOLTA À BOBINA REAL"),
                  self.amp_op.animate.set_value(0), self.side_op.animate.set_value(0),
                  self.ell_op.animate.set_value(0), self.enc_n.animate.set_value(0),
                  FadeOut(law), FadeOut(self.shelf), run_time=0.64)
        approx = mtex("B", r"\simeq", r"\mu_0", "n", "I", size=58)
        fit(approx).move_to(res.get_center())
        abox2 = SurroundingRectangle(approx, color=WHITE, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.note_y = -3.70
        new_note = tag("região central · solenoide longo, L >> R", 22, 0.95)
        new_note.move_to([0, self.note_y, 0])
        self.play(self.cont.animate.set_value(0.0), self.zlim.animate.set_value(Z_FIN),
                  self.cutext_op.animate.set_value(1), self.bin_op.animate.set_value(1),
                  TransformMatchingTex(res, approx), Transform(rbox, abox2),
                  soft_swap(self.hint, new_note), FadeOut(ideal), run_time=1.16)
        self.hint = new_note
        self.expr = VGroup(approx, rbox)
        self.check_safe()
        self.wait(READ_RES)

        # ══ C18. O que a fórmula prevê (na bobina finita) (159–166 s) ═══════════════
        finite_tag = tag("BOBINA LONGA FINITA", 20, 0.85, VIOLET).move_to([0, 4.55, 0])
        self.play(*self.caption("O QUE A FÓRMULA PREVÊ"), FadeIn(finite_tag), run_time=0.58)
        self.note(tag("mesma geometria, mais corrente", 23, 0.9))
        self.play(Indicate(approx[4], color=CYAN, scale_factor=1.5),
                  self.cur.animate.set_value(1.6), run_time=0.84)
        self.check_safe()
        self.wait(READ)
        self.play(self.cur.animate.set_value(1.0), run_time=0.5)
        nlab = mtex("n", "=", r"\tfrac{N}{L}", size=36).move_to([0, AMP_SIDE_Y, 0]).set_opacity(0.85)
        self.note(tag("mesmo L e mesmo I: só mais voltas", 23, 0.9))
        self.play(FadeIn(nlab, shift=UP * 0.1), Indicate(approx[3], color=CYAN, scale_factor=1.5),
                  self.extra_op.animate.set_value(1.0), run_time=1.02)
        self.check_safe()
        self.wait(READ)

        # ══ C19. Coda: o solenoide como atuador (166–171 s) ═════════════════════════
        self.play(*self.caption("ONDE ISSO APARECE"), self.cut_op.animate.set_value(0),
                  self.bin_op.animate.set_value(0), self.extra_op.animate.set_value(0),
                  self.cutext_op.animate.set_value(0), FadeOut(self.expr), FadeOut(nlab),
                  FadeOut(finite_tag), FadeOut(self.hint), run_time=0.64)
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
                  run_time=0.58)
        self.note(tag("núcleo parcialmente inserido, perto da extremidade", 21, 0.9))
        self.check_safe()
        self.wait(0.55)
        i_on = tex("I", 32, CYAN).move_to([-2.1, yb + 0.3, 0])
        self.play(sw.animate.put_start_and_end_on([-1.0, yb, 0], [-0.3, yb, 0]),
                  circuit.animate.set_stroke(CYAN, 3, 1.0), FadeIn(i_on), run_time=0.5)
        self.play(core.animate.shift(LEFT * 1.25), run_time=0.7)
        new_state = tag("VÁLVULA ABERTA", 24, 0.95).move_to([0, -3.4, 0])
        self.note(tag("o núcleo entra e a válvula muda de estado", 21, 0.9))
        self.play(gate.animate.shift(UP * 0.95), soft_swap(state, new_state), run_time=0.58)
        self.check_safe()
        self.wait(BEAT)

        # ══ Fechamento (171–175 s) ══════════════════════════════════════════════════
        self.play(*self.caption("BIOT-SAVART + SIMETRIA + AMPÈRE"),
                  FadeOut(VGroup(winds, core, circuit, sw, i_on, pipe, gate, new_state)),
                  FadeOut(self.hint), run_time=0.64)
        self.hint = None
        final = boxed(mtex("B", r"\simeq", r"\mu_0\,n\,I", size=54)).move_to([0, 0.6, 0])
        handle = tag("@labparallax", 22, 0.8).move_to([0, -0.9, 0])
        self.play(FadeIn(final, shift=UP * 0.1), run_time=0.52)
        self.play(FadeIn(handle, shift=UP * 0.1), run_time=0.5)
        self.check_safe()
        self.wait(1.5)
