"""Base local desta cena: modelo físico, paleta, helpers e a classe de quadro.

Módulo LOCAL da pasta do vídeo — não é helper do template compartilhado.

O vídeo irmão (vid_0009_campo_solenoide) carrega uma cópia idêntica deste
arquivo, que evolui por episódio e pode divergir. A duplicação é deliberada: o Manim
só põe o diretório da própria cena no
sys.path, e cada pasta vid_NNNN precisa continuar reproduzível sozinha depois de
publicada — mexer no módulo de um dos dois não pode mudar o render do outro.

Guarda:
  * o modelo físico (b_loop, b_sum, b_cut, dbz_phi) e suas conferências de import;
  * a paleta semântica e as margens de segurança do formato 9x16;
  * os helpers de texto/vetor/rótulo;
  * a classe CenaBase, com a infraestrutura de quadro cumulativo
    (manchete, nota, expressão ativa, prateleira de resultados, check_safe).

Unidades internas: R = 1; b = B / (mu0 I / 2R); passo PITCH = 0,5 R => n = 2/R e o
valor ideal do solenoide é b = 2 R n = 4 (= mu0 n I na mesma escala).

Cores com significado estável nas DUAS cenas:
  ciano       R (raio) e a resultante axial;
  azul        z (posição no eixo) e o fio/enrolamento;
  violeta     r (distância elemento-ponto), contorno amperiano e l;
  ciano claro dl, corrente e contribuições individuais;
  magenta     componente transversal, cancelamento e destaque localizado;
  branco      campo, resultados e o que já está concluído.
"""

from contextlib import contextmanager

import numpy as np
from manim import (
    DOWN, LEFT, ORIGIN, PI, RIGHT, UP, AnimationGroup, Arc, Arrow, Circle, Dot, FadeIn,
    FadeOut, Line, MathTex, RoundedRectangle, Scene, SurroundingRectangle, TexTemplate,
    VGroup, VMobject, color_to_rgb, config, rate_functions,
)

from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR
from template.fonts import screen_text

WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # R e a resultante axial
CYAN_L = "#8AE9FF"        # dl, corrente e contribuições individuais
BLUE = "#267BFF"          # z e o fio/enrolamento
VIOLET = SECONDARY_COLOR  # r, contorno amperiano e l
MAGENTA = "#EA63FF"       # componente transversal, cancelamento, destaque

SAFE_BOTTOM = -4.6        # abaixo disso: faixa reservada a legendas
SAFE_X = 3.5              # |x| máximo do conteúdo (o modelo ideal sangra de propósito)
HEADLINE_TOP = 6.85

# Ritmo: o espectador vê o objeto, vê a transformação e observa o estado concluído.
BEAT = 0.55               # respiro entre passos de um mesmo raciocínio
READ = 1.60               # estado intermediário novo
READ_RES = 2.55           # resultado importante

PITCH = 0.5               # passo do enrolamento, em unidades de R  => n = 1/PITCH por R
B_IDEAL = 2.0 / PITCH     # mu0 n I na escala b = B/(mu0 I/2R): 2 R n = 4
L_ELL = 3.0               # comprimento l do retângulo amperiano, em unidades de R
Z_FIN = 3.0               # semicomprimento da bobina finita no corte, em R

CUT_Z = (np.arange(-19, 19) + 0.5) * PITCH          # seções do fio: ±0,25 … ±9,25
CUT_EXTRA = np.arange(-19, 19) * PITCH              # fileira intercalada: dobra n
ENC_Z = CUT_Z[np.abs(CUT_Z) < L_ELL / 2]            # as seções dentro de l


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
MU0_DIM, N_DIM, I_DIM = {"T": 1, "m": 1, "A": -1}, {"m": -1}, {"A": 1}
assert dim_mul(MU0_DIM, N_DIM, I_DIM) == {"T": 1}
assert dim_mul(MU0_DIM, I_DIM, {"m": 2}, {"m": -3}) == {"T": 1}   # mu0 I R^2 / (R^2+z^2)^{3/2}
assert dim_mul(MU0_DIM, I_DIM, {"m": -1}) == {"T": 1}             # mu0 I / (2R)

_R, _I, _MU = 1.0, 1.0, 1.0
assert np.isclose(b_loop(0.0), 1.0) and np.isclose(b_loop(1.0), 2 ** -1.5)
_z = np.linspace(-4, 4, 4001)
assert np.allclose(_MU * _I * _R ** 2 / (2 * (_R ** 2 + _z ** 2) ** 1.5), b_loop(_z) / 2)
assert np.allclose(b_loop(-_z), b_loop(_z))                       # paridade em z
assert b_loop(20.0) < b_loop(2.0) < b_loop(0.0)                   # decai com a distância
assert abs(b_loop(40.0) * 40.0 ** 3 - 1.0) < 2e-3                 # z >> R: cai com 1/z^3
assert np.allclose([b_loop(1.3, 0.75)], [b_loop(1.3 - 0.75)])     # deslocamento z - z_j

# Superposição: os valores que a barra, a seta e os rótulos mostram.
_b = [b_sum(0.0, n) for n in (1, 2, 4, 8)]
assert np.isclose(_b[0], 1.0)
assert _b[0] < _b[1] < _b[2] < _b[3] < B_IDEAL                    # enrolar mais reforça
assert np.allclose(_b, [1.0, 1.82615, 2.85015, 3.58197], atol=5e-5)
assert abs(b_sum(0.0, 400) - B_IDEAL) < 0.01                      # limite: mu0 n I
assert abs(b_sum(2.0, 8) / b_sum(0.0, 8) - 0.54172) < 5e-4        # ponta ~ 54% do centro
assert abs(b_cut(0.0, Z_FIN) - B_IDEAL) / B_IDEAL < 0.07          # finita: só aproximado
assert b_cut(Z_FIN, Z_FIN) < 0.65 * b_cut(0.0, Z_FIN)             # e cai na ponta
_dob = b_cut(0.0, Z_FIN, 1.0) / b_cut(0.0, Z_FIN)
assert 1.9 < _dob < 2.1 and not np.isclose(_dob, 2.0, atol=1e-6)  # dobrar n só aproxima 2x
assert int(len(ENC_Z)) == 6 and np.isclose(L_ELL / PITCH, 6.0)    # N_l = n l = 6, uma fileira


# ── Helpers visuais ─────────────────────────────────────────────────────────
# O LaTeX carrega a cor ate o mobject: \textcolor sobrevive a importacao do SVG, e
# com isso a MESMA variavel tem a MESMA cor no desenho e dentro da formula — inclusive
# dentro de \frac, onde MathTex nao consegue separar submobjects por substring.
TEX = TexTemplate()
TEX.add_to_preamble(r"\usepackage{xcolor}")
for _nome, _hex in (("cR", CYAN), ("cZ", BLUE), ("cr", VIOLET), ("cL", CYAN_L), ("cM", MAGENTA)):
    TEX.add_to_preamble(r"\definecolor{%s}{HTML}{%s}" % (_nome, _hex.lstrip("#")))
# atalhos: \vR raio, \vZ posicao no eixo, \vr distancia, \vL elemento, \vM em cancelamento
TEX.add_to_preamble(r"\newcommand{\vR}{\textcolor{cR}{R}}")
TEX.add_to_preamble(r"\newcommand{\vZ}{\textcolor{cZ}{z}}")
TEX.add_to_preamble(r"\newcommand{\vr}{\textcolor{cr}{r}}")
TEX.add_to_preamble(r"\newcommand{\vrv}{\textcolor{cr}{\vec r}}")
TEX.add_to_preamble(r"\newcommand{\vL}{\textcolor{cL}{d\ell}}")
TEX.add_to_preamble(r"\newcommand{\vLv}{\textcolor{cL}{d\vec\ell}}")
TEX.add_to_preamble(r"\newcommand{\vM}[1]{\textcolor{cM}{#1}}")
TEX.add_to_preamble(r"\newcommand{\vB}{\textcolor{cR}{dB_z}}")
TEX.add_to_preamble(r"\newcommand{\vA}{\textcolor{cM}{\alpha}}")
TEX.add_to_preamble(r"\newcommand{\vI}{\textcolor{cM}{I}}")   # corrente em magenta (só nas capas)


def tex(content, size=40, color=None):
    m = MathTex(content, font_size=size, tex_template=TEX)
    return m if color is None else m.set_color(color)


def mtex(*parts, size=48, color=None):
    m = MathTex(*parts, font_size=size, tex_template=TEX)
    return m if color is None else m.set_color(color)


def glyphs(m, color, atol=0.035):
    """Os glifos que receberam esta cor no LaTeX — sem depender de indice.

    Permite pegar "o r do numerador" numa fracao, que MathTex nao separa em partes.
    """
    alvo = np.array(color_to_rgb(color))
    return VGroup(*(g for g in m.family_members_with_points()
                    if np.allclose(np.array(color_to_rgb(g.get_fill_color())), alvo, atol=atol)))


def by_height(g):
    """Os mesmos glifos, do mais alto para o mais baixo (numerador antes do denominador)."""
    return VGroup(*sorted(g, key=lambda x: -x.get_center()[1]))


def panel(m, color=WHITE, fill=0.05, buff=0.24, stroke=0.40):
    """Placa translucida discreta atras de um resultado."""
    bg = RoundedRectangle(width=m.width + 2 * buff, height=m.height + 2 * buff,
                          corner_radius=0.13)
    bg.set_stroke(color, 1.8, stroke).set_fill(color, fill).move_to(m)
    return VGroup(bg, m)


def ficha(titulo, corpo, color=WHITE, lab_size=14):
    """Resultado ja estabelecido, guardado na prateleira: rotulo pequeno + expressao.

    A expressao fica com brilho total; a hierarquia vem do tamanho e da moldura, nao de
    apagar o texto. O fundo tem z_index -1: fica atras da expressao qualquer que seja a
    ordem em que as pecas entram na cena (antes, o fundo entrava depois e a cobria).
    """
    lab = text(titulo, lab_size, color, 0.85)
    corpo.next_to(lab, DOWN, buff=0.10)
    dentro = VGroup(lab, corpo)
    bg = RoundedRectangle(width=dentro.width + 0.36, height=dentro.height + 0.30,
                          corner_radius=0.10)
    bg.set_stroke(color, 1.4, 0.50).set_fill(BACKGROUND_COLOR, 0.92).move_to(dentro)
    bg.set_z_index(-1)
    return VGroup(bg, lab, corpo)


def ficha_mini(titulo, frag, color=WHITE):
    """Ficha INATIVA da prateleira: só título e um fragmento identificador.

    A fórmula completa vive no card grande (ficha), que se abre quando é usada.
    O fundo tem z_index -1, como em ficha().
    """
    lab = text(titulo, 15, color, 0.90)
    frag.next_to(lab, DOWN, buff=0.08)
    dentro = VGroup(lab, frag)
    bg = RoundedRectangle(width=max(dentro.width, 1.25) + 0.40, height=dentro.height + 0.30,
                          corner_radius=0.10)
    bg.set_stroke(color, 1.4, 0.55).set_fill(BACKGROUND_COLOR, 0.92).move_to(dentro)
    bg.set_z_index(-1)
    return VGroup(bg, lab, frag)


def halo(m, width=7):
    """Contorno da cor do fundo que abraca cada glifo.

    Separa o rotulo das linhas que passam atras dele sem a placa retangular, que
    cortava raios, eixos e setas em pedacos.
    """
    m.set_stroke(BACKGROUND_COLOR, width, 1.0, background=True)
    return m


def pulse_ring(point, color=WHITE, raio=0.55, rt=0.85):
    """Anel que cresce e apaga: chama o olho sem decorar a cena."""
    ring = Circle(0.10, color=color, stroke_width=3.5).move_to(point).set_fill(opacity=0)
    anim = ring.animate(rate_func=rate_functions.ease_out_sine).scale(raio / 0.10)
    return ring, anim.set_stroke(opacity=0)


@contextmanager
def wide_pango():
    """Gera o texto sempre na MESMA largura de layout, seja qual for a resolução.

    O Pango quebra a linha na largura de config.pixel_width, e o nome do SVG em
    media/texts NÃO inclui essa largura: a mesma frase sai quebrada ou inteira
    conforme a resolução do render que gerou a entrada do cache primeiro. Num
    preview 540x960 as manchetes quebravam em três linhas; fixando a largura
    aqui, o texto deixa de depender da resolução (e do cache).
    """
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


# A cor é aplicada DEPOIS de gerar o texto: o SVG do Pango é indexado também pela cor,
# e entradas antigas trazem métricas de outra fonte — o que fazia a mesma frase ser
# quebrada em duas linhas dependendo da cor pedida.
def text(content, size=24, color=WHITE, opacity=1.0, **kwargs):
    with wide_pango():
        t = screen_text(content, size, **kwargs)
    return t.set_color(color).set_opacity(opacity)


def display(content, size=38):
    with wide_pango():
        t = screen_text(content, size, oversample=2)
    return t.set_color(WHITE)


def tag(content, size=26, opacity=1.0, color=WHITE):
    """Mensagem de uma linha, limitada à margem; falha se o Pango quebrar a linha."""
    with wide_pango():
        t = screen_text(content, size, oversample=2)
    t.set_color(color).set_opacity(opacity)
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


def odot(c, color=CYAN_L, op=1.0, r=0.145):
    """Seção de fio com corrente saindo do plano."""
    return VGroup(Circle(r, color=color, stroke_width=3).set_stroke(opacity=op),
                  Dot(ORIGIN, 0.055, color=color).set_opacity(op)).move_to(c)


def otimes(c, color=CYAN_L, op=1.0, r=0.145):
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


class CenaBase(Scene):
    """Quadro cumulativo: manchete no topo, expressão ativa ao centro, nota embaixo.

    A prateleira (self.shelf) guarda os resultados já obtidos: nada que continua
    valendo some da tela sem necessidade.
    """

    op_y = -2.30
    note_y = -3.95
    shelf_y = -3.90

    def start_frame(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.headline = self.hint = self.expr = None
        self.shelf = VGroup()
        self.bleed = []

    def check_safe(self):
        """Texto e equações dentro da margem e acima da faixa de legenda.

        A geometria que sangra de propósito pelas laterais fica em self.bleed.
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
        from manim import TransformMatchingTex
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
        fit(layout, 2 * SAFE_X - 0.2).move_to([0, self.shelf_y, 0])
        chip.move_to(layout[-1])
        return [m.animate.move_to(layout[i]) for i, m in enumerate(old)] + \
               [FadeIn(chip, shift=UP * 0.12)]
