"""vid_0028 v3 — Soma relativística de velocidades: camada Manim do pipeline Three.js + Manim.

Curto vertical. Camada com fundo TRANSPARENTE (-t → .mov com alfa), composta por cima do 3D (cena3d/, render3d.js) no
compor.py. Física, notação e microderivação congeladas (handoffs v1–v3). Versões anteriores: v1 só-Manim em
cena_v1.py; v2 em v2_snapshot/.

Tempo: todo instante vem do timeline.json (`ate(E[...])`); o quadro n é desenhado com renderer.time = n/fps, o mesmo t
do setFrame(n) do 3D. Posições e velocidades do cenário: timeline['trajetoria'] (movimento.py), a MESMA tabela que o
3D lê. v3: a tela mostra em cada referencial a velocidade que ele MEDE (sA, sB, sE), então seta, número e movimento
contam a mesma coisa. Regras v3: um texto por vez; slot `v_B′ = ?` fixo no topo até a C05; nada entra do nada.

Preview 540×960 / 15 fps (bash, na raiz):
    MEDIA_DIR=videos/vid_0028_soma_relativistica/media_preview uv run --no-sync python -m manim -t -r 540,960 --fps 15 videos/vid_0028_soma_relativistica/cena.py SomaRelativistica028
    uv run --no-sync python videos/vid_0028_soma_relativistica/compor.py --classe SomaRelativistica028 --sufixo v3
"""
from pathlib import Path
import json
import os
import sys
import numpy as np
from manim import *
from MF_Tools import TransformByGlyphMap

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config import PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

UNIT = Path(__file__).absolute().parent
config.media_dir = os.environ.get('MEDIA_DIR', str(UNIT / 'media_preview'))
TL = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))
E, G, TR = TL['eventos'], TL['geometria'], TL['trajetoria']
LEGENDA_TOPO = -4.5                      # nada da cena abaixo disto (faixa da legenda: y −4,67 a −6,0)

# ── paleta (handoff §4) ─────────────────────────────────────────────────────────────────────────────────────
VEL = '#9C8CFF'     # só velocidade: setas, v_A, v_B, v_B', valores
GEO = '#B8C4DA'     # régua, marcas, colchete, barras
DIM = '#8FA3C4'     # texto secundário, chips
ICE = TEXT_COLOR    # c (letra e marca da régua)
PANEL = '#0E1A33'
CYAN, PINK = PRIMARY_COLOR, '#EA63FF'   # só no degradê do @labparallax do cartão final

# ── layout (y, unidades do Manim = unidades do 3D na vista lateral) ─────────────────────────────────────────
Y_TAG, Y_MAPA, Y_SLOT = 6.92, 6.45, 5.92
Y_R = {'A': G['y_foguete_A'], 'B': G['y_foguete_B']}          # pistas dos foguetes
Y_BRACKET = (Y_R['A'] + Y_R['B']) / 2
Y_GROUND, Y_TERRA, Y_EARR = G['y_chao'], 2.44, 2.02
Y_TXT = -.3                                                    # texto de cena antes da régua existir
RUL_Y, RX0, RU = G['y_regua'], -3.6, 3.6                      # régua: x(v) = RX0 + RU·v/c → c em x = 0
Y_EQ, Y_N1, Y_TXT2 = -2.0, -3.55, -1.0                         # equação, notas, texto de cena com a régua
ALEN, LF = 1.3, G['comprimento_foguete']                       # seta por c; comprimento do foguete (0,7×)
CHIP_DX = .18                                                  # centro do corpo do foguete × centro geométrico


def RX(v):
    return RX0 + RU * v


def suave(u):
    return u * u * (3 - 2 * u)


def chaves(lista, t, campo='v'):
    if t <= lista[0]['t']:
        return lista[0][campo]
    for a, b in zip(lista, lista[1:]):
        if t <= b['t']:
            u = (t - a['t']) / max(b['t'] - a['t'], 1e-9)
            if b.get('ease') != 'linear':
                u = suave(u)
            return a[campo] + (b[campo] - a[campo]) * u
    return lista[-1][campo]


def amostra(nome, t):
    lista = TR[nome]
    return lista[max(0, min(len(lista) - 1, int(round(t / TR['passo_s']))))]


def num(v, d=1, sinal=True):
    """Número com vírgula decimal para MathTex (0,8 → 0{,}8); sinal explícito opcional."""
    s = f'{abs(v):.{d}f}'.replace('.', '{,}')
    if abs(v) < .5 * 10 ** -d:
        return '0'
    return (('-' if v < 0 else '+') if sinal else ('-' if v < 0 else '')) + s


FORMULAS = {  # tex, nº de glifos, {cor: índices}; o resto em branco (inclui todo c)
    'dx': (r"dx'=\gamma(dx-v_A\,dt)", 14, {VEL: [9, 10]}),
    'dt': (r"dt'=\gamma\left(dt-\frac{v_A\,dx}{c^2}\right)", 17, {VEL: [9, 10]}),
    'v0': (r"v_B'=\frac{dx'}{dt'}", 11, {VEL: [0, 1, 2]}),
    'v1': (r"v_B'=\frac{\gamma(dx-v_A\,dt)}{\gamma\left(dt-\frac{v_A\,dx}{c^2}\right)}", 28,
           {VEL: [0, 1, 2, 9, 10, 20, 21]}),
    'v2': (r"v_B'=\frac{dx-v_A\,dt}{dt-\frac{v_A\,dx}{c^2}}", 22, {VEL: [0, 1, 2, 7, 8, 15, 16]}),
    'v2b': (r"v_B'=\frac{(dx-v_A\,dt)/dt}{\left(dt-\frac{v_A\,dx}{c^2}\right)/dt}", 32,
            {VEL: [0, 1, 2, 8, 9, 21, 22]}),
    'v3': (r"v_B'=\frac{\frac{dx}{dt}-v_A}{1-\frac{v_A}{c^2}\frac{dx}{dt}}", 25, {VEL: [0, 1, 2, 10, 11, 15, 16]}),
    'v4': (r"v_B'=\frac{v_B-v_A}{1-\frac{v_Av_B}{c^2}}", 19, {VEL: [0, 1, 2, 4, 5, 7, 8, 12, 13, 14, 15]}),
    'vB': (r"v_B=\frac{dx}{dt}", 8, {VEL: [0, 1]}),
    'S1': (r"v_B'=\frac{(-0{,}8c)-(+0{,}8c)}{1-\frac{(+0{,}8c)(-0{,}8c)}{c^2}}", 39,
           {VEL: [0, 1, 2, 5, 6, 7, 8, 13, 14, 15, 16, 23, 24, 25, 26, 30, 31, 32, 33]}),
    'S2': (r"v_B'=\frac{-1{,}6c}{1-\frac{(+0{,}8c)(-0{,}8c)}{c^2}}", 29,
           {VEL: [0, 1, 2, 4, 5, 6, 7, 13, 14, 15, 16, 20, 21, 22, 23]}),
    'S2b': (r"v_B'=\frac{-1{,}6c}{1-\frac{-0{,}64\,c^2}{c^2}}", 22, {VEL: [0, 1, 2, 4, 5, 6, 7]}),
    'S3': (r"v_B'=\frac{-1{,}6c}{1-(-0{,}64)}", 19, {VEL: [0, 1, 2, 4, 5, 6, 7]}),
    'S4': (r"v_B'=\frac{-1{,}6c}{1+0{,}64}", 16, {VEL: [0, 1, 2, 4, 5, 6, 7]}),
    'S5': (r"v_B'=\frac{-1{,}6c}{1{,}64}", 14, {VEL: [0, 1, 2, 4, 5, 6, 7]}),
    'S6': (r"v_B'=-\frac{1{,}6}{1{,}64}\,c", 14, {VEL: [0, 1, 2, 4, 5, 6, 7, 9, 10, 11, 12]}),
    'S7': (r"v_B'=-\frac{40}{41}\,c\approx-0{,}976\,c", 19, {VEL: [0, 1, 2, 4, 5, 6, 8, 9, 12, 13, 14, 15, 16, 17]}),
    'S8': (r"|v_B'|\approx0{,}976\,c", 12, {VEL: [1, 2, 3, 6, 7, 8, 9, 10]}),
    'G1': (r"\frac{|v_Av_B|}{c^2}\sim10^{-14}", 15, {VEL: [1, 2, 3, 4]}),
    'G2': (r"1-\frac{v_Av_B}{c^2}\approx1", 11, {VEL: [2, 3, 4, 5]}),
    'G3': (r"v_B'\approx v_B-v_A", 9, {VEL: [0, 1, 2, 4, 5, 7, 8]}),
    'H1': (r"|v_B'|=\frac{0{,}5c+0{,}5c}{1+0{,}25}=0{,}8\,c", 27, {VEL: [1, 2, 3, 6, 7, 8, 11, 12, 13, 23, 24, 25]}),
    'H2': (r"|v_B'|=\frac{0{,}99c+0{,}99c}{1+0{,}9801}\approx0{,}99995\,c", 35,
           {VEL: [1, 2, 3, 6, 7, 8, 9, 12, 13, 14, 15, 27, 28, 29, 30, 31, 32, 33]}),
    'hook': (r"0{,}8c+0{,}8c=\,?", 11, {VEL: [0, 1, 2, 5, 6, 7]}),
    'naive': (r"0{,}8c+0{,}8c=1{,}6c\,?", 15, {VEL: [0, 1, 2, 5, 6, 7, 10, 11, 12]}),
    'rx': (r"dx-v_A\,dt", 7, {VEL: [3, 4]}),                       # barras da C04
    'rt': (r"dt-\frac{v_A\,dx}{c^2}", 10, {VEL: [3, 4]}),
    'pa': (r"v_A\,dt", 4, {VEL: [0, 1, 2, 3]}),
    'pb': (r"\frac{v_A\,dx}{c^2}", 7, {VEL: [0, 1, 2, 3, 4, 5, 6]}),
}


def words(content, y=0, size=28, color=TEXT_COLOR, x=0, **kw):
    pw, ph = config.pixel_width, config.pixel_height
    try:
        config.pixel_width = config.pixel_height = 4000
        mob = screen_text(content, size, color=color, oversample=2, **kw)
    finally:
        config.pixel_width, config.pixel_height = pw, ph
    if mob.width > 7.8:
        mob.scale_to_fit_width(7.8)
    return mob.move_to([x, y, 0]).set_z_index(40)


def tex(key, y=0, size=46, x=0):
    s, count, colors = FORMULAS[key]
    mob = MathTex(s, font_size=size, color=TEXT_COLOR)
    assert len(mob[0]) == count, (key, len(mob[0]), count)
    for ink, idx in colors.items():
        for i in idx:
            mob[0][i].set_color(ink)
    if mob.width > 7.6:
        mob.scale_to_fit_width(7.6)
    mob.move_to([x, y, 0]).set_z_index(40)
    assert mob.get_bottom()[1] > LEGENDA_TOPO, f'{key} invadiu a faixa da legenda'
    return mob


def vtex(s, size=32):
    """Rótulo de velocidade: tudo violeta, exceto a letra c (sempre branca, último glifo)."""
    mob = MathTex(s, font_size=size, color=VEL)
    if s.endswith('c'):
        mob[0][-1].set_color(ICE)
    return mob.set_z_index(42)


def glyphs(eq, idx):
    return VGroup(*[eq[0][i] for i in idx])


def strikes(*groups, color=TEXT_COLOR):
    return VGroup(*[Line(g.get_corner(DL) + DL * .05, g.get_corner(UR) + UR * .05, color=color, stroke_width=2.6)
                    for g in groups]).set_z_index(45)


def chip(content, pad=(.2, .11), stroke=DIM):
    box = RoundedRectangle(corner_radius=.12, width=content.width + 2 * pad[0], height=content.height + 2 * pad[1],
                           stroke_color=stroke, stroke_width=1.3, stroke_opacity=.75,
                           fill_color=PANEL, fill_opacity=.8).move_to(content).set_z_index(content.z_index - 1)
    return VGroup(box, content)


def tag(name):
    return chip(words('REFERENCIAL: ' + name, 0, 19, DIM)).move_to([0, Y_TAG, 0])


def passo(n, texto):
    """Chip do mapa do vídeo (① REFERENCIAL ② FÓRMULA ③ RESULTADO): número no círculo + rótulo."""
    num_ = words(str(n), 0, 17, DIM)
    circ = Circle(radius=.18, stroke_color=DIM, stroke_width=1.6, fill_color=GEO, fill_opacity=0).move_to(num_)
    circ.set_z_index(39)
    return VGroup(VGroup(circ, num_), words(texto, 0, 18, DIM)).arrange(RIGHT, buff=.12)


def slot_mob(conteudo, legenda='B MEDIDO POR A', antes=False):
    """Fio condutor no topo: o que estamos procurando (ou já achamos)."""
    m = conteudo if isinstance(conteudo, Mobject) else vtex(conteudo, 40)
    if antes:
        return VGroup(words(legenda, 0, 22, TEXT_COLOR), m).arrange(RIGHT, buff=.2).move_to([0, Y_SLOT, 0]).set_z_index(41)
    g = VGroup(m, words(legenda, 0, 16, DIM)).arrange(RIGHT, buff=.25) if legenda else VGroup(m)
    return g.move_to([0, Y_SLOT, 0]).set_z_index(41)


class SomaRelativistica028(Scene):
    # ── tempo ────────────────────────────────────────────────────────────────────────────────────────────────
    def agora(self):
        return self.renderer.time

    def mark(self, name):
        self.events.append({'estado': name, 'segundos': round(self.agora(), 3)})
        print(f'ESTADO {name}: {self.agora():.3f}s')

    def ate(self, alvo, nome=None):
        """Espera até o instante do timeline; avisa (e registra) se a cena chegou atrasada."""
        if isinstance(alvo, str):
            nome, alvo = alvo, E[alvo]
        fps = config.frame_rate
        n = round((alvo - self.agora()) * fps)
        if n > 0:
            self.wait(n / fps - 1e-6)
        elif n < -1:
            self.atrasos.append({'evento': nome, 'alvo': alvo, 'chegou': round(self.agora(), 3)})
            print(f'ATRASO {nome}: alvo {alvo:.2f}s, cena em {self.agora():.2f}s')
        if nome:
            self.mark(nome)

    def relogio_upd(self, m, dt):
        """Animações presas ao relógio (atravessam vários play): encolhimento do ponteiro clássico na C05."""
        if self.pc_curva:
            t0, t1, v0, v1 = self.pc_curva
            u = min(1, max(0, (self.agora() - t0) / (t1 - t0)))
            self.pc.set_value(v0 + (v1 - v0) * suave(u))

    # ── texto de cena: um por vez ────────────────────────────────────────────────────────────────────────────
    def fala(self, new, rt=.45, extras=(), shift=UP * .06):
        """Troca o texto de cena: o que sai, sai antes do que entra."""
        if self.texto is not None:
            self.play(FadeOut(self.texto), run_time=.3)
        if new is not None:
            self.play(FadeIn(new, shift=shift), *extras, run_time=rt)
        elif extras:
            self.play(*extras, run_time=rt)
        self.texto = new

    # ── álgebra ──────────────────────────────────────────────────────────────────────────────────────────────
    def morph(self, source, target, *links, rt=1.6, extras=()):
        anim = TransformByGlyphMap(source, target, *links, auto_fade=True, auto_morph=False, printing=False)
        assert not anim.show_indices
        self.play(anim, *extras, run_time=rt, rate_func=smooth)
        self.remove(*source.get_family())
        self.remove(*target.get_family())
        self.add(target)
        return target

    def assemble(self, target, pairs, fade=(), rt=1.6, extras=(), rings=()):
        """Glifos de outras expressões (ou da cena) navegam até target; o restante de target aparece."""
        if rings:
            marks = [SurroundingRectangle(r, buff=.06, corner_radius=.06, stroke_width=1.6,
                                          color=r.get_color()).set_z_index(44) for r in rings]
            self.play(*[Create(m) for m in marks], run_time=.35)
            extras = (*extras, *[FadeOut(m) for m in marks])
        movers, anims, used = [], [], set()
        for src, idx, *kw in pairs:
            c = src.copy()
            movers.append(c)
            anims.append(Transform(c, glyphs(target, idx).copy(), **(kw[0] if kw else {})))
            used |= set(idx)
        rest = VGroup(*[g for i, g in enumerate(target[0]) if i not in used])
        self.play(*anims, FadeIn(rest), *[FadeOut(m) for m in fade], *extras, run_time=rt, rate_func=smooth)
        self.remove(*movers, rest, *fade)
        self.add(target)
        return target

    # ── cenário (preso à trajetória do 3D) ───────────────────────────────────────────────────────────────────
    def x(self, k):
        return amostra('x' + k, self.agora())

    def v(self, k):
        """Velocidade medida pelo referencial atual (a mesma que move o 3D)."""
        return amostra('s' + k, self.agora())

    def visivel(self):
        return 1 - chaves(TL['veu'], self.agora())

    def arrow_of(self, k):
        v, x = self.v(k), self.x(k)
        y = Y_EARR if k == 'E' else Y_R[k] + .55
        comp = ALEN * v * self.agrow.get_value()
        if abs(comp) < .03:   # corpo parado no referencial atual: seta mínima invisível (sempre com pontos)
            return Arrow([x, y, 0], [x + .01, y, 0], buff=0, color=VEL).set_opacity(0).set_z_index(22)
        return Arrow([x, y, 0], [x + comp, y, 0], buff=0, color=VEL, stroke_width=6,
                     max_tip_length_to_length_ratio=.25, max_stroke_width_to_length_ratio=12
                     ).set_opacity(self.visivel()).set_z_index(22)

    def label_pos(self, k, mob):
        v, x = self.v(k), self.x(k)
        if k == 'E':
            side = -np.sign(v) if abs(v) > .01 else 1
            return np.array([x + side * (.62 + mob.width / 2), Y_EARR, 0])
        return np.array([x, Y_R[k] + .95, 0])     # trilho fixo de cada foguete, centrado no corpo

    def label(self, k, s):
        m = VGroup(vtex(s))
        m.add_updater(lambda g: g.move_to(self.label_pos(k, g)).set_opacity(self.visivel()))
        m.update(0)
        return m

    def label_dyn(self, k, op):
        """Rótulo que conta: mostra a velocidade medida agora (ex.: a Terra indo de 0 a −0,8c na troca).
        Entra e sai pela opacidade `op` (FadeIn/FadeOut copiariam o updater e a cópia mudaria de glifos)."""
        def build():
            m = vtex(num(self.v(k)) + 'c')
            return m.move_to(self.label_pos(k, m)).set_opacity(self.visivel() * op.get_value())
        m = always_redraw(build)
        m.op = op
        return m

    def relabel(self, k, s, rt=.5, extras=(), dyn=False):
        anims, new, depois = [], None, []
        if dyn:
            new = self.label_dyn(k, ValueTracker(0))
            self.add(new)
            anims.append(new.op.animate.set_value(1))
        elif s is not None:
            new = self.label(k, s)
            new.update(0)
            anims.append(FadeIn(new, shift=UP * .05))
        old = self.labs.pop(k, None)
        if old is not None:
            if hasattr(old, 'op'):
                anims.append(old.op.animate.set_value(0))
                depois.append(old)
            else:
                old.clear_updaters()
                anims.append(FadeOut(old, shift=UP * .05))
        if anims or extras:
            self.play(*anims, *extras, run_time=rt)
        for m in depois:
            m.clear_updaters()
            self.remove(m)
        if new is not None:
            self.labs[k] = new

    def body_chip(self, k):
        c = chip(words(k, 0, 16, TEXT_COLOR), pad=(.08, .05))
        dx = -CHIP_DX if k == 'A' else CHIP_DX

        def seg(g):
            a = self.visivel()
            g.move_to([self.x(k) + dx, Y_R[k], 0])
            g[0].set_fill(opacity=.85 * a).set_stroke(opacity=.75 * a)
            g[1].set_opacity(a)
        c.add_updater(seg)
        seg(c)
        return c

    def terra_rotulo(self):
        m = words('TERRA', 0, 16, DIM)
        m.add_updater(lambda g: g.move_to([self.x('E'), Y_TERRA, 0]).set_opacity(self.visivel()))
        m.update(0)
        return m

    def narizes(self):
        return self.x('A') + LF / 2 + .08, self.x('B') - LF / 2 - .08

    def bracket(self):
        """Colchete entre os narizes; nasce dos dois foguetes (bgrow 0 → 1) e fecha com o movimento."""
        def build():
            a, b = self.narizes()
            g, op, y = self.bgrow.get_value(), self.visivel(), Y_BRACKET
            if b - a < .05 or g < .01:
                return Line([a, y, 0], [a + .01, y, 0]).set_opacity(0)
            m = (a + b) / 2
            return VGroup(Line([a, y, 0], [a + (m - a) * g, y, 0], color=GEO, stroke_width=2.4),
                          Line([b, y, 0], [b - (b - m) * g, y, 0], color=GEO, stroke_width=2.4),
                          Line([a, y - .18, 0], [a, y + .18, 0], color=GEO, stroke_width=2.4),
                          Line([b, y - .18, 0], [b, y + .18, 0], color=GEO, stroke_width=2.4)
                          ).set_opacity(op).set_z_index(18)
        return always_redraw(build)

    def cenario(self, labels, setas='ABE'):
        """Chips A/B, setas, rótulos e o nome da Terra, todos presos à trajetória do 3D."""
        objs = [self.body_chip('A'), self.body_chip('B'), self.terra_rotulo()]
        objs += [always_redraw(lambda k=k: self.arrow_of(k)) for k in setas]
        for k, s in labels.items():
            self.labs[k] = self.label(k, s)
        return objs

    def show(self, *mobs, rt=.6, extras=()):
        """FadeIn em grupo; depois cada objeto volta a ser raiz própria (updaters rodam uma vez por quadro)."""
        for m in mobs:
            m.update(0)
        group = VGroup(*mobs)
        self.play(FadeIn(group), *extras, run_time=rt)
        self.remove(group)
        self.add(*mobs)

    def drop(self, *mobs, rt=.6, extras=()):
        mobs = [m for m in mobs if m is not None]
        for m in mobs:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in mobs], *extras, run_time=rt)

    def swap_tag(self, tg, name, rt=.6):
        """Troca da tag por cross-fade (sai uma, entra a outra), nunca morph de letras."""
        new = tag(name)
        self.play(FadeOut(tg), FadeIn(new), run_time=rt)
        return new

    def acende(self, i, rt=.5):
        circ, num_ = self.mapa[i][0]
        lab = self.mapa[i][1]
        self.play(circ.animate.set_stroke(TEXT_COLOR, opacity=1).set_fill(GEO, opacity=.28),
                  num_.animate.set_color(TEXT_COLOR), lab.animate.set_color(TEXT_COLOR),
                  Indicate(self.mapa[i], color=TEXT_COLOR, scale_factor=1.15), run_time=rt)

    def troca_slot(self, novo, rt=.6, extras=()):
        self.play(FadeOut(self.slot, shift=UP * .05), FadeIn(novo, shift=UP * .05), *extras, run_time=rt)
        self.slot = novo

    # ── régua ────────────────────────────────────────────────────────────────────────────────────────────────
    def build_ruler(self):
        base = Line([RX(0) - .12, RUL_Y, 0], [RX(2) + .35, RUL_Y, 0], color=GEO, stroke_width=2.2)
        ticks = VGroup()
        for i in range(21):
            if i == 10:
                continue
            h = .16 if i % 5 == 0 else .08
            ticks.add(Line([RX(i / 10), RUL_Y, 0], [RX(i / 10), RUL_Y + h, 0], color=GEO, stroke_width=1.6,
                           stroke_opacity=.9 if i % 5 == 0 else .5))
        cmark = Line([RX(1), RUL_Y - .14, 0], [RX(1), RUL_Y + .42, 0], color=ICE, stroke_width=3.6)
        nums = VGroup(MathTex('0', font_size=30, color=GEO).move_to([RX(0), RUL_Y - .36, 0]),
                      MathTex('c', font_size=36, color=ICE).move_to([RX(1), RUL_Y - .38, 0]),
                      MathTex('2', 'c', font_size=30, color=GEO).move_to([RX(2), RUL_Y - .36, 0]))
        nums[2][1].set_color(ICE)
        unit = MathTex('|v|', font_size=28, color=DIM).move_to([RX(0) - .55, RUL_Y + .05, 0])
        return VGroup(base, ticks, cmark, nums, unit).set_z_index(10)

    def abre_regua(self, ruler, rt=.8):
        """A régua se abre a partir da marca de c (nunca aparece do nada)."""
        alvo = ruler.copy()
        ruler.stretch(.02, 0, about_point=[RX(1), RUL_Y, 0]).set_opacity(0)
        self.add(ruler)
        self.play(Transform(ruler, alvo), run_time=rt)

    def pointer(self, kind):
        tr = self.pr if kind == 'rel' else self.pc
        y = RUL_Y + (.3 if kind == 'rel' else 1.0)

        def build():
            v = tr.get_value()
            if v < .02:
                return VMobject()
            a, b = np.array([RX(0), y, 0]), np.array([RX(v), y, 0])
            if kind == 'rel':
                return Arrow(a, b, buff=0, color=VEL, stroke_width=7, max_tip_length_to_length_ratio=.25,
                             max_stroke_width_to_length_ratio=20).set_z_index(15)
            tip = Triangle(fill_color=VEL, fill_opacity=.55, stroke_width=0).scale(.12).rotate(-PI / 2).move_to(b + LEFT * .1)
            line = DashedLine(a, b + LEFT * .18, color=VEL, stroke_width=4, dash_length=.13, dashed_ratio=.55)
            return VGroup(line.set_stroke(opacity=.55), tip).set_z_index(14)
        return always_redraw(build)

    def ptr_label(self, kind, s, dim=False):
        tr = self.pr if kind == 'rel' else self.pc
        y = RUL_Y + (.68 if kind == 'rel' else 1.38)
        m = VGroup(vtex(s, 30))
        if dim:
            m.set_opacity(.6)
        m.add_updater(lambda g: g.move_to([min(RX(tr.get_value()), 4.35 - g.width / 2), y, 0]))
        m.update(0)
        return m

    def ptr_conta(self, kind, d=3, sufixo='', dim=False):
        """Rótulo do ponteiro que conta junto com ele (contador ↔ ponteiro)."""
        tr = self.pr if kind == 'rel' else self.pc
        y = RUL_Y + (.68 if kind == 'rel' else 1.38)

        def build():
            if tr.get_value() < .02:
                return VMobject()
            m = vtex(num(tr.get_value(), d, False) + 'c' + sufixo, 30)
            if dim:
                m.set_opacity(.6)
            return m.move_to([min(RX(tr.get_value()), 4.35 - m.width / 2), y, 0])
        return always_redraw(build)

    def zoom_inset(self, v, lo=.94, hi=1.01):
        """Lupa sobre a marca de c: a seta para antes de c (sem parede, só a marca)."""
        cx, cy, w, h = 2.35, RUL_Y + 1.42, 3.3, 1.05
        box = RoundedRectangle(corner_radius=.12, width=w, height=h, stroke_color=GEO, stroke_width=1.2,
                               stroke_opacity=.6, fill_color=PANEL, fill_opacity=.95).move_to([cx, cy, 0])

        def X(u):
            return cx - w / 2 + .18 + (u - lo) / (hi - lo) * (w - .36)
        yb = cy - .2
        base = Line([X(lo), yb, 0], [X(hi), yb, 0], color=GEO, stroke_width=1.8)
        cm = Line([X(1), yb - .1, 0], [X(1), yb + .42, 0], color=ICE, stroke_width=3.2)
        clab = MathTex('c', font_size=34, color=ICE).next_to(cm, RIGHT, buff=.08).shift(UP * .12)
        arr = Arrow([X(lo) - .05, yb + .14, 0], [X(v), yb + .14, 0], buff=0, color=VEL, stroke_width=6,
                    max_tip_length_to_length_ratio=.22)
        ring = Circle(radius=.2, color=GEO, stroke_width=1.4, stroke_opacity=.7).move_to([RX(1) - .03, RUL_Y + .22, 0])
        link = DashedLine(ring.get_top() + RIGHT * .1, box.get_corner(DL) + RIGHT * .25, color=GEO, stroke_width=1.2,
                          dash_length=.07).set_stroke(opacity=.6)
        return VGroup(ring, link, box, base, cm, clab, arr).set_z_index(16)

    def ghost_tick(self, v):
        return Line([RX(v), RUL_Y - .02, 0], [RX(v), RUL_Y + .2, 0], color=VEL, stroke_width=3,
                    stroke_opacity=.55).set_z_index(12)

    def barra(self, x0, x1, y, color=GEO, w=13, op=1.):
        return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w, stroke_opacity=op).set_z_index(30)

    # ── cena ─────────────────────────────────────────────────────────────────────────────────────────────────
    def construct(self):
        assert abs(config.pixel_height / config.pixel_width - 16 / 9) < 1e-3, 'curto vertical 9 × 16'
        self.events, self.atrasos, self.labs = [], [], {}
        self.pr, self.pc, self.agrow, self.bgrow = ValueTracker(0), ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.pc_curva, self.texto, self.slot = None, None, None
        relogio = Mobject()
        relogio.add_updater(self.relogio_upd)      # dt-updater: força quadro a quadro também nos waits
        self.add(relogio)

        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.4).to_corner(UR, buff=.28).set_z_index(60)
        brand = words('DA EQUAÇÃO AO FENÔMENO · EP. 08', 0, 20, DIM).set_opacity(.75).to_corner(UL, buff=.4)
        self.add(wm, brand)

        # ── C01 · cold open (sem texto) → setup → pergunta → palpite → promessa, um texto por vez ─────────────
        self.mark('C01')
        self.ate('setas')
        cen = self.cenario({'A': r'+0{,}8c', 'B': r'-0{,}8c'})
        chipsAB, terra_lbl, setas = cen[:2], cen[2], cen[3:]
        self.show(*chipsAB, terra_lbl, *setas, rt=.4)
        self.play(self.agrow.animate.set_value(1), FadeIn(self.labs['A']), FadeIn(self.labs['B']), run_time=.6)
        self.ate('setup')
        self.fala(words('DOIS FOGUETES · CADA UM A 0,8c\nEM RELAÇÃO À TERRA', Y_TXT, 30, t2c={'0,8c': VEL}))
        self.ate('pergunta')
        self.fala(words('QUE VELOCIDADE O FOGUETE A\nMEDE PARA O FOGUETE B?', Y_TXT, 32))
        self.ate('slot')
        self.slot = slot_mob(r"v_B'=\,?").move_to([0, Y_TXT - 1.05, 0])
        self.play(FadeIn(self.slot, shift=UP * .1), run_time=.5)
        self.play(self.slot.animate.move_to([0, Y_SLOT, 0]), run_time=1.0)
        self.ate('palpite')
        hook = tex('hook', Y_TXT - .15, 66)
        rotulo = chip(words('PALPITE', 0, 18, DIM)).next_to(hook, UP, buff=.25)
        self.play(FadeOut(self.texto), run_time=.3)
        self.texto = None
        la, lb = self.labs['A'][0], self.labs['B'][0]
        self.assemble(hook, [(la[0][1:5], [0, 1, 2, 3], {'path_arc': .6}), (lb[0][1:5], [5, 6, 7, 8], {'path_arc': -.6})],
                      rt=1.1, extras=(FadeIn(rotulo),))
        self.texto = VGroup(hook, rotulo)
        self.ate('nao_e_16')
        self.fala(words('A RESPOSTA NÃO É 1,6c', Y_TXT, 34))
        self.ate('promessa')
        prom = VGroup(words('NESTE VÍDEO:', 0, 20, DIM), words('DE ONDE VEM A REGRA QUE COMPÕE\nVELOCIDADES PERTO DA LUZ', 0, 30))
        prom.arrange(DOWN, buff=.18).move_to([0, Y_TXT, 0])
        self.fala(prom, rt=.6)
        self.ate('chips')
        self.mapa = VGroup(passo(1, 'REFERENCIAL'), passo(2, 'FÓRMULA'), passo(3, 'RESULTADO')).arrange(RIGHT, buff=.42)
        self.mapa.move_to([0, Y_TXT - 1.55, 0])
        self.play(LaggedStart(*[FadeIn(p, shift=UP * .1) for p in self.mapa], lag_ratio=.35), run_time=1.1)
        self.ate('chips_sobem')
        self.fala(None, extras=(self.mapa.animate.scale(.82).move_to([0, Y_MAPA, 0]),), rt=1.0)

        # ── C02 · troca de referencial: o mundo desliza; B anda a 0,976 (não a 1,6) ──────────────────────────
        self.ate('c02')
        self.relabel('A', r'v_A=+0{,}8c', rt=.25)
        self.relabel('B', r'v_B=-0{,}8c', rt=.25)
        self.ate('tag_terra0')
        tg = tag('TERRA')
        self.play(TransformFromCopy(terra_lbl, tg[1]), FadeIn(tg[0]), run_time=.6)
        self.remove(tg[1])
        self.add(tg)
        self.ate('troca_A')
        self.relabel('E', None, dyn=True, rt=.3, extras=(FadeOut(self.labs.pop('A').clear_updaters()),))
        self.ate('tag_A')
        tg = self.swap_tag(tg, 'FOGUETE A')
        self.ate('chip1')
        self.acende(0)
        self.ate('b_interroga')
        self.relabel('B', r"v_B'=\,?", rt=.6, extras=(Indicate(self.slot, color=VEL, scale_factor=1.12),))
        self.ate('nota')
        self.fala(words('A EM REPOUSO · A TERRA SE MOVE PARA TRÁS', Y_TXT, 24, DIM))
        self.ate('slot_pulsa')
        self.fala(None, extras=(Indicate(self.slot, color=TEXT_COLOR, scale_factor=1.15),), rt=.8)

        # ── C03 · o 1,6c: vetores das setas na régua; a separação fecha a 1,6c NA TERRA ─────────────────────
        self.ate('c03')
        self.ate('volta_terra')
        self.relabel('B', None, rt=.3)
        self.ate('tag_terra')
        tg = self.swap_tag(tg, 'TERRA')
        self.ate('b_rotulo')
        self.relabel('B', r'v_B=-0{,}8c', rt=.5)
        self.ate('a_rotulo')
        self.relabel('A', r'v_A=+0{,}8c', rt=.4)
        self.relabel('E', None, rt=.15)
        self.ate('regua')
        ruler = self.build_ruler()
        self.play(Indicate(self.slot, color=TEXT_COLOR, scale_factor=1.08), run_time=.3)
        self.abre_regua(ruler, rt=.5)
        yv = RUL_Y + 1.0
        self.ate('vet1')
        v1a = Arrow([RX(0), yv, 0], [RX(.8), yv, 0], buff=0, color=VEL, stroke_width=6, max_tip_length_to_length_ratio=.12)
        l1a = vtex(r'0{,}8c', 28).move_to([RX(.4), yv + .36, 0])
        la, lb = self.labs['A'][0], self.labs['B'][0]
        src = self.arrow_of('A').copy()
        self.play(Transform(src, v1a, path_arc=.5), TransformFromCopy(la[0][4:8], l1a[0], path_arc=.5), run_time=.9)
        self.remove(src, *l1a.get_family())
        self.add(v1a, l1a)
        self.ate('vet2')
        v1b = Arrow([RX(.8), yv, 0], [RX(1.6), yv, 0], buff=0, color=VEL, stroke_width=6, max_tip_length_to_length_ratio=.12)
        l1b = vtex(r'0{,}8c', 28).move_to([RX(1.2), yv + .36, 0])
        src = self.arrow_of('B').copy()
        self.play(Transform(src, v1b, path_arc=-.5), TransformFromCopy(lb[0][4:8], l1b[0], path_arc=-.5), run_time=.9)
        self.remove(src, *l1b.get_family())
        self.add(v1b, l1b)
        self.ate('fecha')
        br = self.bracket()
        self.add(br)
        pc, pcl = self.pointer('cls'), self.ptr_label('cls', r'1{,}6c\,?', dim=True)
        self.pc.set_value(1.6)
        pc.update(0)
        pcl.update(0)
        self.play(self.bgrow.animate.set_value(1), FadeOut(VGroup(v1a, v1b, l1a, l1b)), FadeIn(pc), FadeIn(pcl), run_time=.5)
        self.ate('na_terra')
        close = VGroup(chip(words('NA TERRA', 0, 20, GEO), stroke=GEO), words('A SEPARAÇÃO FECHA A 1,6c', 0, 28))
        close.arrange(RIGHT, buff=.22).move_to([0, Y_TXT2, 0])
        a, b = self.narizes()
        self.play(FadeIn(close, target_position=[(a + b) / 2, Y_BRACKET, 0], scale=.6), run_time=.7)
        self.texto = close
        self.ate('nao_e')
        but = words('MAS ISSO NÃO É O QUE A MEDE DE B', Y_TXT2 - .7, 28)
        self.play(FadeIn(but, shift=UP * .08), Indicate(self.slot, color=VEL, scale_factor=1.15), run_time=.8)

        # ── C04 · origem da fórmula, em três atos (barras → equações → quociente) ─────────────────────────────
        self.ate('c04')
        self.bgrow.set_value(0)
        self.drop(*cen, br, *self.labs.values(), ruler, pc, pcl, close, but, tg, rt=.7)
        self.labs, self.texto = {}, None
        self.acende(1)
        self.ate('manchete')
        head = words('MUDAR O REFERENCIAL MUDA ESPAÇO E TEMPO', 5.25, 25)
        self.play(FadeIn(head, shift=DOWN * .06), run_time=.6)
        # Ato 1 · barras: cada uma perde um pedaço que depende da outra; resultados em linhas próprias.
        X0, X1, XR = -2.9, 1.5, 1.8
        ya, yb, yra, yrb = 1.85, .95, -.35, -1.25
        cut_a, cut_b = 1.3, 1.0
        self.ate('barras')
        bx, bt = self.barra(X0, X1, ya), self.barra(X0, X1, yb)
        lx = MathTex('dx', font_size=36).next_to([XR, ya, 0], RIGHT, buff=0)
        lt = MathTex('dt', font_size=36).next_to([XR, yb, 0], RIGHT, buff=0)
        rx_ = words('ESPAÇO', 0, 17, DIM).next_to(bx, LEFT, buff=.22)
        rt_ = words('TEMPO', 0, 17, DIM).next_to(bt, LEFT, buff=.22)
        self.play(Create(bx), Create(bt), FadeIn(VGroup(lx, lt, rx_, rt_)), run_time=1.0)
        self.ate('peca1')
        pa = self.barra(X1 - cut_a, X1, ya, VEL, 13)
        la_ = tex('pa', 0, 34).next_to(lx, RIGHT, buff=.3)
        menos_a = MathTex('-', font_size=34, color=VEL).next_to(la_, LEFT, buff=.1)
        self.play(Indicate(bt, color=VEL, scale_factor=1.0), run_time=.5)
        self.play(GrowFromEdge(pa, RIGHT), FadeIn(VGroup(menos_a, la_), shift=LEFT * .1), run_time=.8)
        self.ate('res1')
        rbx = self.barra(X0, X1 - cut_a, yra, TEXT_COLOR, 10)
        lrx = tex('rx', 0, 34).next_to([XR, yra, 0], RIGHT, buff=0)
        self.play(TransformFromCopy(bx, rbx), FadeIn(lrx, shift=DOWN * .1), run_time=.9)
        self.ate('peca2')
        pb = self.barra(X1 - cut_b, X1, yb, VEL, 13)
        lb_ = tex('pb', 0, 32).next_to(lt, RIGHT, buff=.3)
        menos_b = MathTex('-', font_size=34, color=VEL).next_to(lb_, LEFT, buff=.1)
        self.play(Indicate(bx, color=VEL, scale_factor=1.0), run_time=.5)
        self.play(GrowFromEdge(pb, RIGHT), FadeIn(VGroup(menos_b, lb_), shift=LEFT * .1), run_time=.8)
        self.ate('res2')
        rbt = self.barra(X0, X1 - cut_b, yrb, TEXT_COLOR, 10)
        lrt = tex('rt', 0, 34).next_to([XR, yrb, 0], RIGHT, buff=0)
        self.play(TransformFromCopy(bt, rbt), FadeIn(lrt, shift=DOWN * .1), run_time=.9)
        bars = VGroup(bx, bt, lx, lt, rx_, rt_, pa, la_, menos_a, rbx, lrx, pb, lb_, menos_b, rbt, lrt)
        # Ato 2 · equações: as barras viram ícone; cada termo pisca junto do seu pedaço.
        self.ate('icone')
        self.play(bars.animate.scale(.42).move_to([0, 4.25, 0]).set_opacity(.8), run_time=.6)
        self.ate('eq_dx')
        e1 = tex('dx', 1.3, 54)
        self.play(Write(e1), run_time=1.0)
        self.play(Indicate(glyphs(e1, [9, 10, 11, 12]), color=VEL, scale_factor=1.25),
                  Indicate(VGroup(pa, la_), color=VEL, scale_factor=1.25), run_time=.8)
        self.ate('eq_dt')
        e2 = tex('dt', -.2, 54)
        self.play(Write(e2), run_time=1.0)
        self.play(Indicate(glyphs(e2, [9, 10, 11, 12, 13, 14, 15]), color=VEL, scale_factor=1.2),
                  Indicate(VGroup(pb, lb_), color=VEL, scale_factor=1.25), run_time=.8)
        # Ato 3 · quociente: equações antigas escurecem e sobem; um bloco grande por vez.
        self.ate('razao')
        self.play(FadeOut(bars), e1.animate.scale(.75).move_to([0, 1.75, 0]).set_opacity(.45),
                  e2.animate.scale(.75).move_to([0, .55, 0]).set_opacity(.45), run_time=.7)
        eq = tex('v0', Y_EQ, 66)
        self.play(FadeIn(eq, shift=UP * .08), run_time=.6)
        self.ate('monta')
        eq = self.assemble(tex('v1', Y_EQ, 62),
                           [(glyphs(eq, [0, 1, 2, 3]), [0, 1, 2, 3]), (glyphs(eq, [7]), [14]),
                            (glyphs(e1, list(range(4, 14))), list(range(4, 14)), {'path_arc': -.4}),
                            (glyphs(e2, list(range(4, 17))), list(range(15, 28)), {'path_arc': .4})],
                           fade=[eq], rt=1.9)
        self.ate('gama')
        g = glyphs(eq, [4, 15])
        rings = VGroup(*[Circle(radius=.3, color=GEO, stroke_width=2.4).move_to(m) for m in g]).set_z_index(45)
        self.play(g.animate.set_color(GEO), Create(rings), FadeOut(VGroup(e1, e2)), run_time=.7)
        self.ate('gama_risca')
        sk = strikes(glyphs(eq, [4]), glyphs(eq, [15]))
        self.play(Create(sk), run_time=.4)
        self.ate('gama_cancela')
        eq = self.morph(eq, tex('v2', Y_EQ, 64),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([4, 5, 13], []), (list(range(6, 13)), list(range(4, 11))),
                        ([14], [11]), ([15, 16, 27], []), (list(range(17, 27)), list(range(12, 22))),
                        rt=1.6, extras=(FadeOut(rings), FadeOut(sk)))
        self.ate('dt_hint')
        hint = VGroup(words('dividir em cima e embaixo por', 0, 22, DIM), MathTex('dt', font_size=34))
        hint.arrange(RIGHT, buff=.14).move_to([0, Y_EQ - 1.75, 0])
        self.play(FadeIn(hint), run_time=.5)
        self.ate('dt_divide')
        eq = self.morph(eq, tex('v2b', Y_EQ, 60),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([], [4]), (list(range(4, 11)), list(range(5, 12))),
                        ([], [12, 13, 14, 15]), ([11], [16]), ([], [17]), (list(range(12, 22)), list(range(18, 28))),
                        ([], [28, 29, 30, 31]), rt=1.4)
        self.ate('distribui')
        eq = self.morph(eq, tex('v3', Y_EQ, 64),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([4, 12], []), ([5, 6], [4, 5]), ([13], [6]), ([14, 15], [7, 8]),
                        ([7], [9]), ([8, 9], [10, 11]), ([10, 11], []), ([16], [12]), ([17, 28], []),
                        ([18, 19], [13]), ([20], [14]), ([21, 22], [15, 16]), ([23, 24], [20, 21]), ([25], [17]),
                        ([26, 27], [18, 19]), ([29, 30, 31], [22, 23, 24]), rt=1.8)
        self.ate('vb')
        vb = tex('vB', Y_EQ - 1.95, 46)
        vbox = SurroundingRectangle(vb, buff=.14, corner_radius=.1, color=VEL, stroke_width=1.6)
        self.play(FadeOut(hint), FadeIn(vb), Create(vbox),
                  glyphs(eq, [4, 5, 6, 7, 8, 20, 21, 22, 23, 24]).animate.set_color(VEL), run_time=.8)
        self.ate('formula')
        eq = self.morph(eq, tex('v4', Y_EQ, 68),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([4, 5, 6, 7, 8], [4, 5]), ([9], [6]), ([10, 11], [7, 8]),
                        ([12], [9]), ([13], [10]), ([14], [11]), ([15, 16], [12, 13]), ([17], [16]), ([18, 19], [17, 18]),
                        ([20, 21, 22, 23, 24], [14, 15], {'path_arc': -.5}), rt=1.8)
        self.ate('caixa')
        box = SurroundingRectangle(eq, buff=.24, corner_radius=.12, color=TEXT_COLOR, stroke_width=1.8)
        self.play(Create(box), FadeOut(vb), FadeOut(vbox), run_time=.6)

        # ── C05 · substituição: valores voam dos foguetes; ponteiro e contador encolhem juntos; resultado ao slot ─
        self.ate('c05')
        cen = self.cenario({'A': r'v_A=+0{,}8c', 'B': r'v_B=-0{,}8c'})
        self.agrow.set_value(1)
        tg = tag('TERRA')
        ruler = self.build_ruler()
        eq_low = eq.copy().scale(.92).move_to([0, Y_EQ, 0])
        self.show(*cen, self.labs['A'], self.labs['B'], tg, rt=.8,
                  extras=(FadeOut(head), FadeOut(box), Transform(eq, eq_low)))
        self.remove(eq)
        eq = eq_low
        self.add(eq)
        self.abre_regua(ruler, rt=.5)
        self.acende(2)
        self.ate('palpite_regua')
        pc = self.pointer('cls')
        self.add(pc)
        self.play(self.pc.animate.set_value(1.6), run_time=.6)
        pcl = self.ptr_label('cls', r'1{,}6c\,?', dim=True)
        self.play(FadeIn(pcl), run_time=.2)
        self.ate('viajam')
        la, lb = self.labs['A'][0], self.labs['B'][0]
        eq = self.assemble(tex('S1', Y_EQ, 58),
                           [(glyphs(eq, [0, 1, 2, 3]), [0, 1, 2, 3]), (glyphs(eq, [6]), [11]), (glyphs(eq, [9]), [19]),
                            (glyphs(eq, [10, 11]), [20, 21]), (glyphs(eq, [16, 17, 18]), [36, 37, 38]),
                            (lb[0][3:8], [5, 6, 7, 8, 9], {'path_arc': -1.1}),
                            (la[0][3:8], [13, 14, 15, 16, 17], {'path_arc': 1.1}),
                            (la[0][3:8], [23, 24, 25, 26, 27], {'path_arc': 1.1}),
                            (lb[0][3:8], [30, 31, 32, 33, 34], {'path_arc': -1.1})],
                           fade=[eq], rt=1.7, rings=(la[0][3:8], lb[0][3:8]))
        self.ate('numerador')
        eq = self.morph(eq, tex('S2', Y_EQ, 58),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([5, 11], [4]), ([6, 7, 8, 14, 15, 16], [5, 6, 7]), ([9, 17], [8]),
                        ([4, 10, 12, 13, 18], []), (list(range(19, 39)), list(range(9, 29))), rt=1.2,
                        extras=(Indicate(VGroup(pc, pcl), color=VEL, scale_factor=1.08),))
        self.ate('sinais')
        sign_note = MathTex(r'(+)\cdot(-)=(-)', font_size=38, color=TEXT_COLOR).move_to([0, Y_N1, 0])
        self.play(Indicate(glyphs(eq, [13, 20]), color=TEXT_COLOR, scale_factor=1.6), FadeIn(sign_note), run_time=1.0)
        self.ate('produto')
        eq = self.morph(eq, tex('S2b', Y_EQ, 58),
                        (list(range(12)), list(range(12))), ([13, 20], [12]), ([14, 15, 16, 21, 22, 23], [13, 14, 15, 16]),
                        ([17, 24], [17, 18]), ([12, 18, 19, 25], []), ([26], [19]), ([27], [20]), ([28], [21]), rt=1.2)
        self.ate('c2_risca')
        cc = strikes(glyphs(eq, [17, 18]), glyphs(eq, [20, 21]))
        self.play(Create(cc), run_time=.4)
        self.ate('c2_cancela')
        eq = self.morph(eq, tex('S3', Y_EQ, 60),
                        (list(range(12)), list(range(12))), ([], [12]), ([12], [13]), ([13, 14, 15, 16], [14, 15, 16, 17]),
                        ([17, 18, 19, 20, 21], []), ([], [18]), rt=1.0, extras=(FadeOut(cc),))
        self.ate('sinal_nota2')
        sign_note2 = MathTex(r'-(-0{,}64)=+0{,}64', font_size=38, color=TEXT_COLOR).move_to([0, Y_N1, 0])
        self.play(FadeTransform(sign_note, sign_note2), Indicate(glyphs(eq, [11, 13]), color=TEXT_COLOR, scale_factor=1.5),
                  run_time=.9)
        sign_note = sign_note2
        self.ate('um_mais')
        eq = self.morph(eq, tex('S4', Y_EQ, 60),
                        (list(range(11)), list(range(11))), ([11, 13], [11]), ([12, 18], []),
                        ([14, 15, 16, 17], [12, 13, 14, 15]), rt=1.0)
        self.ate('um64')
        eq = self.morph(eq, tex('S5', Y_EQ, 60),
                        (list(range(11)), list(range(11))), ([11, 12], []), ([13], [11]), ([14], [12]), ([15], [13]),
                        rt=1.0, extras=(FadeOut(sign_note),))
        self.ate('fracao')
        # o ponteiro clássico encolhe com o quociente (1,6 → 1,6/1,64 → 0,976); o rótulo conta junto
        pcl.clear_updaters()
        conta = self.ptr_conta('cls', 3, dim=True)
        self.pc_curva = (E['fracao'], E['encolhe_fim'], 1.6, 40 / 41)
        self.add(conta)
        eq = self.morph(eq, tex('S6', Y_EQ, 60),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([4], [4]), ([5, 6, 7], [5, 6, 7]), ([8], [13], {'path_arc': -.6}),
                        ([9], [8]), ([10, 11, 12, 13], [9, 10, 11, 12]), rt=1.0, extras=(FadeOut(pcl, run_time=.3),))
        self.ate('q4041')
        eq = self.morph(eq, tex('S7', Y_EQ, 58),
                        ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]), ([5, 6, 7], [5, 6]), ([8], [7]), ([9, 10, 11, 12], [8, 9]),
                        ([13], [10]), ([], list(range(11, 19)), {'delay': .5}), rt=1.3)
        self.ate('encolhe_fim')
        self.pc_curva = None
        self.pc.set_value(40 / 41)
        pr, prl = self.pointer('rel'), self.ptr_label('rel', r'0{,}976c')
        self.pr.set_value(40 / 41)
        pr.update(0)
        prl.update(0)
        conta.clear_updaters()
        self.play(FadeOut(pc), FadeOut(conta), FadeIn(pr), FadeIn(prl), run_time=.4)
        self.pc.set_value(0)
        self.ate('sentido')
        sense = VGroup(words('o sinal só indica o sentido', 0, 22, DIM),
                       Arrow(RIGHT * .35, LEFT * .35, buff=0, color=DIM, stroke_width=4, max_tip_length_to_length_ratio=.35))
        sense.arrange(RIGHT, buff=.2).move_to([0, Y_EQ - 1.1, 0])
        self.play(glyphs(eq, [4, 12]).animate.set_color(DIM).set_opacity(.45), FadeIn(sense), run_time=.8)
        self.ate('modulo')
        mod = tex('S8', Y_N1 - .4, 62)
        mbox = SurroundingRectangle(mod, buff=.18, corner_radius=.12, color=VEL, stroke_width=2)
        self.play(FadeIn(mod, shift=UP * .1), Create(mbox), run_time=.9)
        self.ate('ao_slot')
        novo = slot_mob(tex('S8', 0, 40))
        voo = mod.copy()
        self.play(Transform(voo, novo[0], path_arc=-.6), FadeOut(self.slot), FadeIn(novo[1]), run_time=1.0)
        self.remove(voo, novo[1])
        self.add(novo)
        self.slot = novo
        self.ate('lupa')
        lupa = self.zoom_inset(40 / 41)
        self.play(FadeIn(lupa), run_time=.6)

        # ── C07 · limite clássico: o foguete vira carro e o termo v_A v_B/c² encolhe ─────────────────────────
        self.ate('c07')
        self.drop(eq, sense, mod, mbox, pr, prl, lupa, ruler, *cen, *self.labs.values(), self.slot, rt=.4)
        self.labs, self.slot = {}, None
        self.pr.set_value(0)
        self.ate('carros')
        yc = Y_GROUND + .3
        cA = chip(words('A', 0, 16, TEXT_COLOR), pad=(.07, .04)).move_to([-2.4, yc, 0])
        cB = chip(words('B', 0, 16, TEXT_COLOR), pad=(.07, .04)).move_to([2.4, yc, 0])
        kA = Arrow([-2.4, 3.7, 0], [-1.3, 3.7, 0], buff=0, color=VEL, stroke_width=6, max_tip_length_to_length_ratio=.25)
        kB = Arrow([2.4, 3.7, 0], [1.3, 3.7, 0], buff=0, color=VEL, stroke_width=6, max_tip_length_to_length_ratio=.25)
        tA = vtex(r'v_A=+30\ \mathrm{m/s}', 30).move_to([-1.85, 4.2, 0])
        tB = vtex(r'v_B=-30\ \mathrm{m/s}', 30).move_to([1.85, 4.2, 0])
        terra7 = words('TERRA', Y_TERRA, 16, DIM)
        self.play(FadeIn(VGroup(cA, cB, terra7)), GrowArrow(kA), GrowArrow(kB), FadeIn(tA), FadeIn(tB), run_time=.7)
        self.ate('g1')
        g1 = tex('G1', .7, 60)
        self.play(FadeIn(g1, shift=UP * .08), run_time=.7)
        self.ate('g2')
        g2 = tex('G2', -1.0, 56)
        self.play(FadeIn(g2, shift=UP * .08), run_time=.7)
        self.ate('termo_encolhe')
        termo = glyphs(g2, [1, 2, 3, 4, 5, 6, 7, 8])
        self.play(termo.animate.scale(.45).set_opacity(.45), run_time=.8)
        self.ate('g3')
        g3 = tex('G3', -2.6, 62)
        g3box = SurroundingRectangle(g3, buff=.2, corner_radius=.12, color=TEXT_COLOR, stroke_width=1.8)
        self.play(FadeIn(g3, shift=UP * .08), Create(g3box), run_time=.8)
        self.ate('galileu')
        gal = words('GALILEU = LIMITE DE BAIXAS VELOCIDADES', -3.9, 27)
        self.play(FadeIn(gal), run_time=.6)

        # ── C08 · perto de c: a mesma régua; ponteiro e número andam juntos; sem parede ──────────────────────
        self.ate('c08')
        self.drop(cA, cB, kA, kB, tA, tB, terra7, g1, g2, g3, g3box, gal, rt=.4)
        self.ate('regua8')
        cen = self.cenario({'A': r'v_A=+0{,}5c', 'B': r'v_B=-0{,}5c'})
        ruler = self.build_ruler()
        self.show(*cen, self.labs['A'], self.labs['B'], rt=.4)
        self.abre_regua(ruler, rt=.3)
        self.ate('soma_simples')
        key_c = VGroup(DashedLine(LEFT * .35, RIGHT * .35, color=VEL, stroke_width=4, dash_length=.12).set_stroke(opacity=.55),
                       words('SOMA SIMPLES', 0, 20, DIM)).arrange(RIGHT, buff=.18)
        key_r = VGroup(Line(LEFT * .35, RIGHT * .35, color=VEL, stroke_width=6),
                       words('MEDIDO POR A', 0, 20, DIM)).arrange(RIGHT, buff=.18)
        keys = VGroup(key_c, key_r).arrange(RIGHT, buff=.6).move_to([0, -.8, 0])
        pc, pr = self.pointer('cls'), self.pointer('rel')
        self.add(pc, pr)
        pcl = self.ptr_conta('cls', 2, dim=True)
        self.add(pcl)
        self.play(FadeIn(keys), self.pc.animate.set_value(1.0), run_time=1.0)
        self.ate('rel1')
        prl = self.ptr_conta('rel', 2)
        self.add(prl)
        self.play(self.pr.animate.set_value(.8), run_time=1.0)
        self.ate('h1')
        h1 = tex('H1', Y_EQ - .4, 54)
        self.play(FadeIn(h1, shift=UP * .08), run_time=.7)
        self.ate('acelera')
        ticks = VGroup(self.ghost_tick(.8), self.ghost_tick(40 / 41))
        self.relabel('A', r'v_A=+0{,}99c', rt=.5, extras=(FadeIn(ticks),))
        self.relabel('B', r'v_B=-0{,}99c', rt=.4)
        self.ate('cls2')
        self.play(self.pc.animate.set_value(1.98), FadeOut(h1), run_time=.6)
        self.ate('rel2')
        prl.clear_updaters()
        self.remove(prl)
        prl = self.ptr_conta('rel', 4)
        self.add(prl)
        self.play(self.pr.animate.set_value(40 / 41), run_time=.8, rate_func=linear)
        self.play(self.pr.animate.set_value(.99995), run_time=1.2, rate_func=rate_functions.ease_out_cubic)
        prl.clear_updaters()
        self.remove(prl)
        prl = self.ptr_label('rel', r'0{,}99995c')
        self.add(prl)
        self.ate('h2')
        h2 = tex('H2', Y_EQ - .4, 52)
        self.play(FadeIn(h2, shift=UP * .08), run_time=.7)
        self.ate('menor_c')
        below = MathTex(r'0{,}99995\,c<c', font_size=42, color=TEXT_COLOR)
        below[0][:7].set_color(VEL)
        below.move_to([0, Y_N1 - .25, 0])
        self.play(FadeIn(below), run_time=.5)

        # ── C09 · síntese: Terra → A → B numa cena só; slot atualiza; colchete fecha em taxas diferentes ─────
        self.ate('c09')
        pcl.clear_updaters()
        prl.clear_updaters()
        self.drop(pc, pcl, keys, h2, below, ticks, prl, *self.labs.values(), rt=.5,
                  extras=(self.pr.animate.set_value(.8),))
        self.labs = {}
        self.pc.set_value(0)
        self.labs['A'] = self.label('A', r'+0{,}8c')
        self.labs['B'] = self.label('B', r'-0{,}8c')
        prl = self.ptr_label('rel', r'0{,}8c')
        self.slot = slot_mob(tex('S8', 0, 40))
        self.ate('terra9')
        self.show(self.labs['A'], self.labs['B'], prl, self.slot, rt=.3)
        self.ate('fecha9')
        br = self.bracket()
        self.add(br)
        close = VGroup(chip(words('NA TERRA', 0, 20, GEO), stroke=GEO), words('SEPARAÇÃO FECHA A 1,6c', 0, 28))
        close.arrange(RIGHT, buff=.22).move_to([0, Y_TXT2, 0])
        a, b = self.narizes()
        self.play(self.bgrow.animate.set_value(1), FadeIn(close, target_position=[(a + b) / 2, Y_BRACKET, 0], scale=.6),
                  run_time=.6)
        self.ate('troca9A')
        self.play(FadeOut(close), run_time=.15)
        self.relabel('E', None, dyn=True, rt=.25, extras=(FadeOut(self.labs.pop('A').clear_updaters()),))
        self.ate('tagA9')
        tg = self.swap_tag(tg, 'FOGUETE A')
        self.ate('b976')
        prl.clear_updaters()
        self.relabel('B', r'0{,}976c', rt=.6, extras=(self.pr.animate.set_value(40 / 41), FadeOut(prl)))
        prl = self.ptr_label('rel', r'0{,}976c')
        self.show(prl, rt=.2)
        self.troca_slot(slot_mob(vtex(r'0{,}976c', 40), 'A MEDE B A', antes=True), rt=.5)
        self.ate('troca9B')
        self.relabel('B', None, rt=.3)
        self.ate('tagB9')
        tg = self.swap_tag(tg, 'FOGUETE B')
        self.ate('a976')
        self.relabel('A', r'0{,}976c', rt=.5)
        self.ate('slotB')
        self.troca_slot(slot_mob(vtex(r'0{,}976c', 40), 'B MEDE A A', antes=True), rt=.4)
        self.ate('cada')
        each = words('CADA UM MEDE O OUTRO A 0,976c', Y_TXT2, 30)
        self.play(FadeIn(each, shift=UP * .08), run_time=.6)
        self.ate('fecho1')
        f1 = VGroup(words('CORPOS COM MASSA:', 0, 32), MathTex('v<c', font_size=54, color=TEXT_COLOR)).arrange(RIGHT, buff=.25)
        f1[1][0][0].set_color(VEL)
        f1.move_to([0, -2.05, 0])
        self.play(FadeOut(each), FadeIn(f1, shift=UP * .08), run_time=.8)
        self.ate('fecho2')
        f2 = words('PERTO DE c, VELOCIDADES NÃO SE SOMAM.\nELAS SE ACUMULAM SEM CHEGAR A c.', -3.3, 31)
        self.play(FadeIn(f2, shift=UP * .08), run_time=.8)

        # ── C10 · CTA, separado do fecho físico ──────────────────────────────────────────────────────────────
        self.ate('c10')
        for m in list(self.mobjects):
            if m is not relogio:
                m.clear_updaters()
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not relogio], run_time=.6)
        self.clear()
        self.add(relogio)
        self.ate('cta')
        logo = ImageMobject(str(WATERMARK_PATH)).set_width(4.4).move_to([0, 2.3, 0])
        linha1 = words('SE ESSA CONEXÃO ENTRE EQUAÇÃO\nE FENÔMENO AJUDOU,', -.2, 30)
        linha2 = words('SEGUE O PARALLAX LAB', -1.45, 38)
        handle = words('@labparallax', -2.6, 40).set_color_by_gradient(CYAN, PINK)
        self.play(FadeIn(logo, scale=.96), run_time=.7)
        self.play(FadeIn(linha1, shift=UP * .08), run_time=.6)
        self.play(FadeIn(linha2, shift=UP * .08), FadeIn(handle, shift=UP * .08), run_time=.6)
        self.ate('fim')
        self.play(FadeOut(Group(logo, linha1, linha2, handle)), run_time=.5)
        self.ate(TL['duracao_s'], 'duracao')
        out = Path(config.media_dir) / 'estados_vid0028_v3.json'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({'eventos': self.events, 'atrasos': self.atrasos, 'duracao': round(self.agora(), 3),
                                   'quadros': round(self.agora() * config.frame_rate)}, ensure_ascii=False, indent=1),
                       encoding='utf-8')
        print('ATRASOS:', self.atrasos)
