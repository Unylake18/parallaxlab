"""vid_0028 v5 — Soma relativística de velocidades: camada Manim do pipeline Three.js + Manim.

Curto vertical. Camada com fundo TRANSPARENTE (-t → .mov com alfa), composta por cima do 3D (cena3d/, render3d.js) no
compor.py. Física, notação e microderivação congeladas (handoffs v1–v3). Versões anteriores: v1 só-Manim em
cena_v1.py; v2, v3 e v4 em v2_snapshot/, v3_snapshot/ e v4_snapshot/.

Tempo: todo instante vem do timeline.json (`ate(E[...])`); o quadro n é desenhado com renderer.time = n/fps, o mesmo t
do setFrame(n) do 3D. Posições e velocidades do cenário: timeline['trajetoria'] (movimento.py), a MESMA tabela que o
3D lê. v3: a tela mostra em cada referencial a velocidade que ele MEDE (sA, sB, sE), então seta, número e movimento
contam a mesma coisa. Regras v3: um texto por vez; slot `v_B′ = ?` fixo no topo até a C05; nada entra do nada.
v4 (layout em tela cheia, 540×960 em px): marca 0–48 · contexto 56–176 (tag, slot, passos em linhas próprias) ·
palco 3D 190–470 (só setas, rótulos e colchete do Manim) · bloco principal 490–740 · legenda 760–840 livre. A C04
tem tela própria (o 3D sai por inteiro). Dígitos principais ≥ 32 px (MathTex ≥ 76), secundário ≥ 15 px (texto ≥ 26).
v5: cores separadas (v_A violeta, v_B e v_B′ ciano, Terra e soma simples em GEO); C04 começa na cena (B anda dx
num intervalo dt, A anda v_A·dt: Galileu) e só então vai para a álgebra, um passo por vez com legenda.

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
RITMO = TL.get('sync', {}).get('ritmo', {})     # fator das animações por trecho (sync com a voz; 1 = velocidade do preview)
E, G, TR = TL['eventos'], TL['geometria'], TL['trajetoria']
LEGENDA_TOPO = -4.5                      # nada da cena abaixo disto (faixa da legenda: y −4,67 a −6,0)

# ── paleta (handoff §4) ─────────────────────────────────────────────────────────────────────────────────────
VA = '#9C8CFF'      # velocidade de A (v_A, setas e valores de A)
VB = '#35D9FF'      # velocidade de B (v_B, v_B′, setas e valores de B) — ciano da paleta do canal
VEL = VA
GEO = '#B8C4DA'     # régua, marcas, colchete, barras
DIM = '#8FA3C4'     # texto secundário, chips
ICE = TEXT_COLOR    # c (letra e marca da régua)
PANEL = '#0E1A33'
CYAN, PINK = PRIMARY_COLOR, '#EA63FF'   # só no degradê do @labparallax do cartão final

# ── layout (y, unidades do Manim = unidades do 3D na vista lateral) ─────────────────────────────────────────
Y_TAG, Y_SLOT, Y_MAPA = 6.75, 6.0, 5.33                         # contexto: três linhas próprias
Y_R = {'A': G['y_foguete_A'], 'B': G['y_foguete_B']}          # pistas dos foguetes
Y_BRACKET = (Y_R['A'] + Y_R['B']) / 2
Y_GROUND, Y_TERRA, Y_EARR = G['y_chao'], .72, .3
Y_TXT = -1.9                                                   # texto de cena (hook, notas) no bloco principal
RUL_Y, RX0, RU = G['y_regua'], -3.6, 3.6                      # régua: x(v) = RX0 + RU·v/c → c em x = 0
Y_EQ, Y_N1, Y_TXT2 = -2.65, -4.05, -2.4                        # equação, notas, texto de cena com a régua
ROW_REL, ROW_CLS = RUL_Y + .33, RUL_Y + .8                    # linhas dos ponteiros (relativístico, clássico)
ESP = 1.3                                                      # traço extra do LaTeX (contraste no celular)
F_ALG, F_ROT = 40, 40                                          # v7: toda a álgebra num tamanho só, menor (dígito 17 px); rótulos
COL_TOP, COL_PISO, COL_GAP = 3.35, -4.3, .62                    # coluna da derivação na C04 (tela própria); vão com seta ⇓
ALEN, LF = 1.3, G['comprimento_foguete']                       # seta por c; comprimento do foguete (0,7×)
COR_K = {'A': VA, 'B': VB, 'E': GEO}                           # cor de cada velocidade
CHIP_DX = .2                                                   # centro do corpo do foguete × centro geométrico


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


FORMULAS = {  # tex, nº de glifos, {cor: índices}; o resto em branco (inclui todo c). v_A violeta, v_B/v_B′ ciano
    'g_dx': (r"dx'=dx-v_A\,dt", 11, {VA: [7, 8]}),
    'g_dt': (r"dt'=dt", 6, {}),
    'dx': (r"dx'=\gamma(dx-v_A\,dt)", 14, {VA: [9, 10]}),
    'dt': (r"dt'=\gamma\left(dt-\frac{v_A\,dx}{c^2}\right)", 17, {VA: [9, 10]}),
    'v0': (r"v_B'=\frac{dx'}{dt'}", 11, {VB: [0, 1, 2]}),
    'v1': (r"v_B'=\dfrac{\gamma(dx-v_A\,dt)}{\gamma\left(dt-\dfrac{v_A\,dx}{c^2}\right)}", 28,
           {VB: [0, 1, 2], VA: [9, 10, 20, 21]}),
    'v2': (r"v_B'=\dfrac{dx-v_A\,dt}{dt-\dfrac{v_A\,dx}{c^2}}", 22, {VB: [0, 1, 2], VA: [7, 8, 15, 16]}),
    'v2b': (r"v_B'=\dfrac{(dx-v_A\,dt)/dt}{\left(dt-\dfrac{v_A\,dx}{c^2}\right)/dt}", 32,
            {VB: [0, 1, 2], VA: [8, 9, 21, 22]}),
    'v3': (r"v_B'=\dfrac{\dfrac{dx}{dt}-v_A}{1-\dfrac{v_A}{c^2}\dfrac{dx}{dt}}", 25, {VB: [0, 1, 2], VA: [10, 11, 15, 16]}),
    'v4': (r"v_B'=\dfrac{v_B-v_A}{1-\dfrac{v_Av_B}{c^2}}", 19, {VB: [0, 1, 2, 4, 5, 14, 15], VA: [7, 8, 12, 13]}),
    'vB': (r"v_B=\frac{dx}{dt}", 8, {VB: [0, 1]}),
    'S1': (r"v_B'=\dfrac{(-0{,}8c)-(+0{,}8c)}{1-\dfrac{(+0{,}8c)(-0{,}8c)}{c^2}}", 39,
           {VB: [0, 1, 2, 5, 6, 7, 8, 30, 31, 32, 33], VA: [13, 14, 15, 16, 23, 24, 25, 26]}),
    'S2': (r"v_B'=\dfrac{-1{,}6c}{1-\dfrac{(+0{,}8c)(-0{,}8c)}{c^2}}", 29,
           {VB: [0, 1, 2, 20, 21, 22, 23], VA: [13, 14, 15, 16]}),
    'S2b': (r"v_B'=\dfrac{-1{,}6c}{1-\dfrac{-0{,}64\,c^2}{c^2}}", 22, {VB: [0, 1, 2]}),
    'S3': (r"v_B'=\frac{-1{,}6c}{1-(-0{,}64)}", 19, {VB: [0, 1, 2]}),
    'S4': (r"v_B'=\frac{-1{,}6c}{1+0{,}64}", 16, {VB: [0, 1, 2]}),
    'S5': (r"v_B'=\frac{-1{,}6c}{1{,}64}", 14, {VB: [0, 1, 2]}),
    'S6': (r"v_B'=-\frac{1{,}6}{1{,}64}\,c", 14, {VB: [0, 1, 2, 4, 5, 6, 7, 9, 10, 11, 12]}),
    'S7': (r"v_B'=-\frac{40}{41}\,c\approx-0{,}976\,c", 19, {VB: [0, 1, 2, 4, 5, 6, 8, 9, 12, 13, 14, 15, 16, 17]}),
    'S8': (r"|v_B'|\approx0{,}976\,c", 12, {VB: [1, 2, 3, 6, 7, 8, 9, 10]}),
    'G1': (r"\frac{|v_Av_B|}{c^2}\sim10^{-14}", 15, {VA: [1, 2], VB: [3, 4]}),
    'G2': (r"1-\frac{v_Av_B}{c^2}\approx1", 11, {VA: [2, 3], VB: [4, 5]}),
    'G3': (r"v_B'\approx v_B-v_A", 9, {VB: [0, 1, 2, 4, 5], VA: [7, 8]}),
    'H1': (r"|v_B'|=\frac{0{,}5c+0{,}5c}{1+0{,}25}=0{,}8\,c", 27, {VB: [1, 2, 3, 6, 7, 8, 23, 24, 25], VA: [11, 12, 13]}),
    'H2a': (r"|v_B'|=\frac{0{,}99c+0{,}99c}{1+0{,}9801}", 26, {VB: [1, 2, 3, 6, 7, 8, 9], VA: [12, 13, 14, 15]}),
    'hook': (r"0{,}8c+0{,}8c=\,?", 11, {VA: [0, 1, 2], VB: [5, 6, 7]}),
    'naive': (r"0{,}8c+0{,}8c=1{,}6c\,?", 15, {VA: [0, 1, 2], VB: [5, 6, 7], GEO: [10, 11, 12]}),
    'neq': (r"0{,}8c+0{,}8c\neq1{,}6c", 15, {VA: [0, 1, 2], VB: [5, 6, 7], GEO: [11, 12, 13]}),
    'gd': (r"\gamma=\frac{1}{\sqrt{1-v_A^2/c^2}}", 14, {GEO: [0]}),
    'sn2': (r"-(-0{,}64)=+0{,}64", 14, {}),
    'rx': (r"dx-v_A\,dt", 7, {VA: [3, 4]}),
    'rt': (r"dt-\frac{v_A\,dx}{c^2}", 10, {VA: [3, 4]}),
    'pa': (r"v_A\,dt", 4, {VA: [0, 1]}),
    'pb': (r"\frac{v_A\,dx}{c^2}", 7, {VA: [0, 1]}),
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


def tex(key, y=0, size=F_ALG, x=0):
    """Fórmula do dicionário, sempre no mesmo tamanho (nunca reescalada para caber)."""
    s, count, colors = FORMULAS[key]
    mob = MathTex(s, font_size=size, color=TEXT_COLOR)
    assert len(mob[0]) == count, (key, len(mob[0]), count)
    for ink, idx in colors.items():
        for i in idx:
            mob[0][i].set_color(ink)
    mob.set_stroke(width=ESP * min(1, size / 54))      # traço proporcional: no tamanho pequeno não empasta
    assert mob.width <= 8.4, f'{key} largo demais ({mob.width:.2f})'
    mob.move_to([x, y, 0]).set_z_index(40)
    assert mob.get_bottom()[1] > LEGENDA_TOPO, f'{key} invadiu a faixa da legenda'
    return mob


def vtex(s, size=F_ROT, color=VA):
    """Rótulo de velocidade na cor do foguete (A violeta, B ciano); a letra c sempre branca (último glifo)."""
    mob = MathTex(s, font_size=size, color=color)
    if s.endswith('c'):
        mob[0][-1].set_color(ICE)
    return mob.set_stroke(width=ESP).set_z_index(42)


def mtex(s, size=F_ALG, color=TEXT_COLOR):
    """MathTex avulso com o mesmo traço (proporcional ao tamanho)."""
    return MathTex(s, font_size=size, color=color).set_stroke(width=ESP * min(1, size / 54)).set_z_index(40)


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
    return chip(words('REFERENCIAL: ' + name, 0, 28, GEO), pad=(.22, .1)).move_to([0, Y_TAG, 0])


def passo(n, texto):
    """Chip do mapa do vídeo (① REFERENCIAL ② FÓRMULA ③ RESULTADO): número no círculo + rótulo."""
    num_ = words(str(n), 0, 26, DIM)
    circ = Circle(radius=.24, stroke_color=DIM, stroke_width=2, fill_color=GEO, fill_opacity=0).move_to(num_)
    circ.set_z_index(39)
    return VGroup(VGroup(circ, num_), words(texto, 0, 26, DIM)).arrange(RIGHT, buff=.14)


def slot_mob(conteudo, legenda='B MEDIDO POR A', antes=False):
    """Fio condutor no topo: o que estamos procurando (ou já achamos)."""
    m = conteudo if isinstance(conteudo, Mobject) else vtex(conteudo, 54, VB)
    if antes:
        return VGroup(words(legenda, 0, 30, TEXT_COLOR), m).arrange(RIGHT, buff=.22).move_to([0, Y_SLOT, 0]).set_z_index(41)
    g = VGroup(m, words(legenda, 0, 26, GEO)).arrange(RIGHT, buff=.3) if legenda else VGroup(m)
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
            self.seg = nome

    def play(self, *anims, **kw):
        """Sync com a voz: cada trecho (desde o último evento) roda no fator RITMO dele; mede o tempo ocupado por trecho."""
        if any(isinstance(a, Wait) for a in anims):
            return super().play(*anims, **kw)
        rt = kw.get('run_time')
        if rt is None:
            rt = max((a.run_time if isinstance(a, Animation) else 1.0 for a in anims), default=1.0)
        self.ocupado[self.seg] = round(self.ocupado.get(self.seg, 0) + rt, 3)
        kw['run_time'] = rt * RITMO.get(self.seg, 1.0)
        return super().play(*anims, **kw)

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

    def alinha(self, mob):
        """Linhas da derivação com o '=' (glifo 3 de v_B'=) na mesma vertical."""
        return mob.shift(RIGHT * (self.x_igual - mob[0][3].get_x()))

    def empilha(self, linhas):
        """Posições (y do centro) das linhas empilhadas a partir do topo da coluna."""
        ys, topo = [], COL_TOP
        for m in linhas:
            ys.append(topo - m.height / 2)
            topo -= m.height + COL_GAP
        return ys

    def setas_col(self):
        return [m.seta for m, _ in self.coluna if getattr(m, 'seta', None) is not None]

    def rola(self, novo_h, rt=.5, extras=()):
        """Abre espaço para uma linha nova: as mais antigas se desescrevem e a coluna sobe (sem fade)."""
        col = self.coluna
        sai = []
        while sum(m.height for m, _ in col) + novo_h + COL_GAP * len(col) > COL_TOP - COL_PISO:
            m, anexos = col.pop(0)
            sai.append(VGroup(m, *anexos))
        if sai and col and getattr(col[0][0], 'seta', None) is not None:
            sai.append(col[0][0].seta)          # a ⇓ que vinha da linha que saiu
            col[0][0].seta = None
        if sai:
            self.play(*[Unwrite(m) if isinstance(m, VMobject) else Uncreate(m) for m in sai], run_time=rt * .5)
        ys = self.empilha([m for m, _ in col])
        movs = [VGroup(m, *anexos, *([m.seta] if getattr(m, 'seta', None) is not None else [])).animate.shift(UP * (y - m.get_y()))
                for (m, anexos), y in zip(col, ys) if abs(y - m.get_y()) > 1e-3]
        if movs or extras:
            self.play(*movs, *extras, run_time=rt * (.5 if sai else 1))

    def deriva(self, key, *links, rt=1.5, extras=()):
        """Próxima linha da conta: nasce de uma cópia da anterior (MF-Tools), logo abaixo dela."""
        alvo = self.alinha(tex(key))
        self.rola(alvo.height)
        fonte = self.coluna[-1][0]
        alvo.set_y(fonte.get_bottom()[1] - COL_GAP - alvo.height / 2)
        seta = mtex(r'\Downarrow', 36, DIM).move_to([self.x_igual, (fonte.get_bottom()[1] + alvo.get_top()[1]) / 2, 0])
        alvo.seta = seta
        anim = TransformByGlyphMap(fonte, alvo, *links, from_copy=True, auto_fade=True, auto_morph=False, printing=False)
        assert not anim.show_indices
        self.play(anim, GrowFromEdge(seta, UP), *extras, run_time=rt, rate_func=smooth)
        self.remove(*alvo.get_family())
        self.add(alvo, seta)
        self.coluna.append((alvo, []))
        return alvo

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
        self.play(*anims, Write(rest), *[FadeOut(m) for m in fade], *extras, run_time=rt, rate_func=smooth)
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
        y = Y_EARR if k == 'E' else Y_R[k] + .6
        comp = ALEN * v * self.agrow.get_value()
        if abs(comp) < .03:   # corpo parado no referencial atual: seta mínima invisível (sempre com pontos)
            return Arrow([x, y, 0], [x + .01, y, 0], buff=0, color=COR_K[k]).set_opacity(0).set_z_index(22)
        return Arrow([x, y, 0], [x + comp, y, 0], buff=0, color=COR_K[k], stroke_width=8,
                     max_tip_length_to_length_ratio=.25, max_stroke_width_to_length_ratio=12
                     ).set_opacity(self.visivel()).set_z_index(22)

    def label_pos(self, k, mob):
        v, x = self.v(k), self.x(k)
        if k == 'E':
            side = -np.sign(v) if abs(v) > .01 else 1
            return np.array([x + side * (.75 + mob.width / 2), Y_EARR, 0])
        h = mob.width / 2                         # trilho fixo de cada foguete, centrado no corpo, dentro do quadro
        return np.array([min(max(x, -4.4 + h), 4.4 - h), Y_R[k] + 1.02, 0])

    def label(self, k, s):
        m = VGroup(vtex(s, color=COR_K[k]))
        m.add_updater(lambda g: g.move_to(self.label_pos(k, g)).set_opacity(self.visivel()))
        m.update(0)
        return m

    def label_dyn(self, k, op):
        """Rótulo que conta: mostra a velocidade medida agora (ex.: a Terra indo de 0 a −0,8c na troca).
        Entra e sai pela opacidade `op` (FadeIn/FadeOut copiariam o updater e a cópia mudaria de glifos)."""
        def build():
            m = vtex(num(self.v(k)) + 'c', color=COR_K[k])
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
        c = chip(words(k, 0, 24, TEXT_COLOR), pad=(.09, .05))
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
        m = words('TERRA', 0, 26, GEO)
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

    def na_terra_16(self):
        """Resultado que fica escrito na C03/C09: a separação fecha a 1,6c NA TERRA (sem frase: a voz explica)."""
        g = VGroup(vtex(r'1{,}6c', 48, GEO), chip(words('NA TERRA', 0, 26, GEO), stroke=GEO)).arrange(RIGHT, buff=.25)
        return g.move_to([0, Y_TXT2, 0])

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
        base = Line([RX(0) - .12, RUL_Y, 0], [RX(2) + .35, RUL_Y, 0], color=GEO, stroke_width=3.2)
        ticks = VGroup()
        for i in range(21):
            if i == 10:
                continue
            h = .2 if i % 5 == 0 else .1
            ticks.add(Line([RX(i / 10), RUL_Y, 0], [RX(i / 10), RUL_Y + h, 0], color=GEO, stroke_width=2.2,
                           stroke_opacity=1 if i % 5 == 0 else .7))
        cmark = Line([RX(1), RUL_Y - .16, 0], [RX(1), RUL_Y + .25, 0], color=ICE, stroke_width=5)
        nums = VGroup(mtex('0', 52, GEO).move_to([RX(0), RUL_Y - .45, 0]),
                      mtex('c', 60, ICE).move_to([RX(1), RUL_Y - .47, 0]),
                      mtex('2c', 52, GEO).move_to([RX(2), RUL_Y - .45, 0]))
        nums[2][0][1].set_color(ICE)
        unit = mtex('|v|', 40, DIM).move_to([RX(0) - .62, RUL_Y + .08, 0])
        return VGroup(base, ticks, cmark, nums, unit).set_z_index(10)

    def abre_regua(self, ruler, rt=.8):
        """A régua se abre a partir da marca de c (nunca aparece do nada)."""
        alvo = ruler.copy()
        ruler.stretch(.02, 0, about_point=[RX(1), RUL_Y, 0]).set_opacity(0)
        self.add(ruler)
        self.play(Transform(ruler, alvo), run_time=rt)

    def pointer(self, kind):
        tr = self.pr if kind == 'rel' else self.pc
        y = ROW_REL if kind == 'rel' else ROW_CLS

        def build():
            v = tr.get_value()
            if v < .02:
                return VMobject()
            a, b = np.array([RX(0), y, 0]), np.array([RX(v), y, 0])
            if kind == 'rel':
                return Arrow(a, b, buff=0, color=VB, stroke_width=11, max_tip_length_to_length_ratio=.25,
                             max_stroke_width_to_length_ratio=30).set_z_index(15)
            tip = Triangle(fill_color=GEO, fill_opacity=.85, stroke_width=0).scale(.15).rotate(-PI / 2).move_to(b + LEFT * .12)
            line = DashedLine(a, b + LEFT * .22, color=GEO, stroke_width=6, dash_length=.14, dashed_ratio=.55)
            return VGroup(line.set_stroke(opacity=.8), tip).set_z_index(14)
        return always_redraw(build)

    @staticmethod
    def ptr_xy(kind, v, w):
        """Rótulo do ponteiro na própria linha, à direita da ponta; sem espaço, sobe para cima da ponta."""
        y = ROW_REL if kind == 'rel' else ROW_CLS
        x = RX(v) + .2 + w / 2
        if x + w / 2 > 4.4:
            return np.array([min(RX(v), 4.4 - w / 2), y + .45, 0])
        return np.array([x, y, 0])

    def ptr_label(self, kind, s, dim=False):
        tr = self.pr if kind == 'rel' else self.pc
        m = VGroup(vtex(s, 52, VB if kind == 'rel' else GEO))
        if dim:
            m.set_opacity(.75)
        m.add_updater(lambda g: g.move_to(self.ptr_xy(kind, tr.get_value(), g.width)))
        m.update(0)
        return m

    def ptr_conta(self, kind, d=3, sufixo='', dim=False):
        """Rótulo do ponteiro que conta junto com ele (contador ↔ ponteiro)."""
        tr = self.pr if kind == 'rel' else self.pc

        def build():
            if tr.get_value() < .02:
                return VMobject()
            m = vtex(num(tr.get_value(), d, False) + 'c' + sufixo, 52, VB if kind == 'rel' else GEO)
            if dim:
                m.set_opacity(.75)
            return m.move_to(self.ptr_xy(kind, tr.get_value(), m.width))
        return always_redraw(build)

    def zoom_inset(self, v, lo=.94, hi=1.01):
        """Lupa sobre a marca de c: a seta para antes de c (sem parede, só a marca)."""
        cx, cy, w, h = 0, -4.0, 3.6, .98
        box = RoundedRectangle(corner_radius=.12, width=w, height=h, stroke_color=GEO, stroke_width=1.2,
                               stroke_opacity=.6, fill_color=PANEL, fill_opacity=.95).move_to([cx, cy, 0])

        def X(u):
            return cx - w / 2 + .18 + (u - lo) / (hi - lo) * (w - .36)
        yb = cy - .2
        base = Line([X(lo), yb, 0], [X(hi), yb, 0], color=GEO, stroke_width=1.8)
        cm = Line([X(1), yb - .1, 0], [X(1), yb + .42, 0], color=ICE, stroke_width=3.2)
        clab = mtex('c', 44, ICE).next_to(cm, RIGHT, buff=.08).shift(UP * .12)
        arr = Arrow([X(lo) - .05, yb + .14, 0], [X(v), yb + .14, 0], buff=0, color=VB, stroke_width=6,
                    max_tip_length_to_length_ratio=.22)
        ring = Circle(radius=.24, color=GEO, stroke_width=1.8, stroke_opacity=.8).move_to([RX(1) - .03, ROW_REL, 0])
        link = DashedLine(ring.get_bottom(), box.get_top() + RIGHT * .55, color=GEO, stroke_width=1.4,
                          dash_length=.07).set_stroke(opacity=.7)
        return VGroup(ring, link, box, base, cm, clab, arr).set_z_index(16)

    def ghost_tick(self, v):
        return Line([RX(v), RUL_Y - .02, 0], [RX(v), RUL_Y + .24, 0], color=VB, stroke_width=4,
                    stroke_opacity=.75).set_z_index(12)

    def barra(self, x0, x1, y, color=GEO, w=13, op=1.):
        return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w, stroke_opacity=op).set_z_index(30)

    # ── cena ─────────────────────────────────────────────────────────────────────────────────────────────────
    def construct(self):
        assert abs(config.pixel_height / config.pixel_width - 16 / 9) < 1e-3, 'curto vertical 9 × 16'
        self.events, self.atrasos, self.labs = [], [], {}
        self.seg, self.ocupado = 'C01', {}
        self.pr, self.pc, self.agrow, self.bgrow = ValueTracker(0), ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.pc_curva, self.texto, self.slot = None, None, None
        relogio = Mobject()
        relogio.add_updater(self.relogio_upd)      # dt-updater: força quadro a quadro também nos waits
        self.add(relogio)

        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.45).to_corner(UR, buff=.25).set_z_index(60)
        brand = words('DA EQUAÇÃO AO FENÔMENO · EP. 08', 0, 22, DIM).set_opacity(.85).to_corner(UL, buff=.35)
        self.add(wm, brand)

        # ── C01 · cold open (sem texto) → pergunta (slot) → palpite → ≠ 1,6c; o que a voz diz não vira texto (v7) ─
        self.mark('C01')
        self.ate('setas')
        cen = self.cenario({'A': r'+0{,}8c', 'B': r'-0{,}8c'})
        chipsAB, terra_lbl, setas = cen[:2], cen[2], cen[3:]
        self.show(*chipsAB, terra_lbl, *setas, rt=.4)
        self.play(self.agrow.animate.set_value(1), FadeIn(self.labs['A']), FadeIn(self.labs['B']), run_time=.6)
        self.ate('setup')
        self.ate('pergunta')
        self.slot = slot_mob(r"v_B'=\,?").move_to([0, Y_TXT, 0])
        self.play(Write(self.slot), run_time=.8)
        self.ate('slot')
        self.play(self.slot.animate.move_to([0, Y_SLOT, 0]), run_time=1.0)
        self.ate('palpite')
        hook = tex('hook', Y_TXT - .35, 84)
        rotulo = chip(words('PALPITE', 0, 30, TEXT_COLOR), pad=(.22, .1)).next_to(hook, UP, buff=.35)
        la, lb = self.labs['A'][0], self.labs['B'][0]
        self.assemble(hook, [(la[0][1:5], [0, 1, 2, 3], {'path_arc': .6}), (lb[0][1:5], [5, 6, 7, 8], {'path_arc': -.6})],
                      rt=1.1, extras=(FadeIn(rotulo),))
        hook = self.morph(hook, tex('naive', Y_TXT - .35, 84), (list(range(10)), list(range(10))), ([10], [14]),
                          ([], [10, 11, 12, 13]), rt=.8)
        self.ate('nao_e_16')
        hook = self.morph(hook, tex('neq', Y_TXT - .35, 84), (list(range(9)), list(range(9))), ([9], [9, 10]),
                          ([10, 11, 12, 13], [11, 12, 13, 14]), ([14], []), rt=.8)
        self.ate('promessa')
        self.ate('chips')
        self.mapa = VGroup(passo(1, 'REFERENCIAL'), passo(2, 'FÓRMULA'), passo(3, 'RESULTADO')).arrange(RIGHT, buff=.55)
        self.mapa.move_to([0, -3.75, 0])
        self.play(LaggedStart(*[FadeIn(p, shift=UP * .1) for p in self.mapa], lag_ratio=.35), run_time=1.1)
        self.ate('chips_sobem')
        self.play(Unwrite(hook), FadeOut(rotulo), self.mapa.animate.move_to([0, Y_MAPA, 0]), run_time=1.0)

        # ── C02 · troca de referencial: o mundo desliza; B anda a 0,976 (não a 1,6) ──────────────────────────
        self.ate('c02')
        self.acende(0)
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
        self.ate('b_interroga')
        self.relabel('B', r"v_B'=\,?", rt=.6, extras=(Indicate(self.slot, color=VB, scale_factor=1.12),))
        self.ate('nota')
        self.ate('slot_pulsa')
        self.play(Indicate(self.slot, color=TEXT_COLOR, scale_factor=1.15), run_time=.8)

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
        yv = ROW_CLS
        self.ate('vet1')
        v1a = Arrow([RX(0), yv, 0], [RX(.8), yv, 0], buff=0, color=VA, stroke_width=8, max_tip_length_to_length_ratio=.12)
        l1a = vtex(r'0{,}8c', 48, VA).move_to([RX(.4), ROW_REL - .02, 0])
        la, lb = self.labs['A'][0], self.labs['B'][0]
        src = self.arrow_of('A').copy()
        self.play(Transform(src, v1a, path_arc=.5), TransformFromCopy(la[0][4:8], l1a[0], path_arc=.5), run_time=.9)
        self.remove(src, *l1a.get_family())
        self.add(v1a, l1a)
        self.ate('vet2')
        v1b = Arrow([RX(.8), yv, 0], [RX(1.6), yv, 0], buff=0, color=VB, stroke_width=8, max_tip_length_to_length_ratio=.12)
        l1b = vtex(r'0{,}8c', 48, VB).move_to([RX(1.2), ROW_REL - .02, 0])
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
        close = self.na_terra_16()
        a, b = self.narizes()
        self.play(FadeIn(close, target_position=[(a + b) / 2, Y_BRACKET, 0], scale=.6), run_time=.7)
        self.ate('nao_e')
        self.play(Indicate(self.slot, color=VB, scale_factor=1.15), run_time=.8)

        # ── C04 · de onde vem a fórmula. Parte 0 na cena (Terra): B anda dx num intervalo dt; A anda v_A·dt ────
        self.ate('c04')
        self.bgrow.set_value(0)
        self.drop(br, ruler, pc, pcl, close, rt=.6)
        self.texto = None
        self.ate('origem')
        self.acende(1)
        self.ate('anda_txt')
        yB, yA = Y_R['B'] - .62, Y_R['A'] - .62          # faixas dos deslocamentos, logo abaixo de cada pista
        xb0, xa0 = self.x('B') - LF / 2, self.x('A') + LF / 2
        marca = lambda x, y, cor: DashedLine([x, y - .3, 0], [x, y + .95, 0], color=cor, stroke_width=3,
                                             dash_length=.08).set_z_index(24)
        mB0, mA0 = marca(xb0, yB, VB), marca(xa0, yA, VA)
        self.play(Create(mB0), Create(mA0), run_time=.45)
        self.ate('anda')
        trilho = RoundedRectangle(corner_radius=.08, width=4.0, height=.26, stroke_color=GEO, stroke_width=2,
                                  fill_opacity=0).move_to([0, Y_TXT - 1.15, 0])
        enche = ValueTracker(0)
        barra_t = always_redraw(lambda: Rectangle(width=max(.001, 3.9 * enche.get_value()), height=.18, stroke_width=0,
                                                  fill_color=GEO, fill_opacity=.9).align_to(trilho, LEFT).shift(RIGHT * .05)
                                .set_y(trilho.get_y()))
        rot_t = mtex('dt').next_to(trilho, RIGHT, buff=.25)
        self.add(trilho, barra_t)
        self.play(enche.animate.set_value(1), Write(rot_t), run_time=3.0, rate_func=linear)
        self.ate('dx_seta')
        xb1, xa1 = self.x('B') - LF / 2, self.x('A') + LF / 2
        mB1 = marca(xb1, yB, VB)
        sdx = Arrow([xb0, yB, 0], [xb1, yB, 0], buff=0, color=VB, stroke_width=7, max_tip_length_to_length_ratio=.3)
        ldx = mtex('dx').next_to(sdx, LEFT, buff=.15)
        self.play(Create(mB1), GrowArrow(sdx), Write(ldx), run_time=.7)
        self.ate('vb_def')
        vbeq = tex('vB', Y_TXT - .1)
        self.assemble(vbeq, [(ldx[0], [3, 4], {'path_arc': .5}), (rot_t[0], [6, 7], {'path_arc': -.4})],
                      rt=1.1, extras=(Uncreate(VGroup(trilho, barra_t.clear_updaters())), Unwrite(rot_t)))
        self.add(ldx)
        self.ate('a_anda')
        mA1 = marca(xa1, yA, VA)
        sva = Arrow([xa0, yA, 0], [xa1, yA, 0], buff=0, color=VA, stroke_width=7, max_tip_length_to_length_ratio=.3)
        lva = tex('pa').next_to(sva, RIGHT, buff=.15)
        self.play(Create(mA1), GrowArrow(sva), Write(lva), run_time=.9)
        self.ate('rel_gal')
        rel = tex('g_dx', Y_TXT - 1.45)       # Galileu: para A, B se desloca dx − v_A dt
        self.assemble(rel, [(ldx[0], [4, 5], {'path_arc': .5}), (lva[0], [7, 8, 9, 10], {'path_arc': -.5})], rt=1.0)
        self.play(Indicate(VGroup(sdx, ldx), color=VB, scale_factor=1.15), Indicate(VGroup(sva, lva), color=VA, scale_factor=1.15),
                  run_time=.8)
        self.ate('mistura')
        self.play(Indicate(rel, color=GEO, scale_factor=1.08), run_time=.6)
        # ── C04 · parte 1 em tela própria (o 3D sai): as duas equações da cena sobem e viram o ponto de partida ──
        self.ate('tela')
        X_EQ = -1.05                                       # '=' das equações de transformação na mesma vertical
        igual_em = lambda m: m.shift(RIGHT * (X_EQ - m[0][3].get_x()))
        Y_DEF, Y_E1, Y_E2 = 4.3, 2.75, 1.5
        self.drop(*cen, *self.labs.values(), tg, mB0, mA0, mB1, mA1, sdx, ldx, sva, lva, rt=.5,
                  extras=(vbeq.animate.move_to([-2.1, Y_DEF, 0]),
                          rel.animate.move_to(igual_em(rel.copy()).get_center()).set_y(Y_E1)))
        self.labs, self.texto = {}, None
        d1, eg1 = vbeq, rel
        self.ate('defs')
        d2 = tex('v0', Y_DEF, x=2.1)
        self.play(TransformByGlyphMap(d1, d2, ([0, 1], [0, 1]), ([], [2]), ([2], [3]), ([3, 4], [4, 5]), ([], [6]),
                                      ([5], [7]), ([6, 7], [8, 9]), ([], [10]), from_copy=True, auto_fade=True,
                                      auto_morph=False, printing=False),
                  Indicate(self.slot, color=VB, scale_factor=1.1), run_time=1.0)
        self.remove(*d2.get_family())
        self.add(d2)
        self.ate('galileu_eq')
        eg2 = igual_em(tex('g_dt', Y_E2))
        self.play(TransformByGlyphMap(eg1, eg2, ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]), ([10], [5]), ([5, 6, 7, 8, 9], []),
                                      from_copy=True, auto_fade=True, auto_morph=False, printing=False), run_time=.9)
        self.remove(*eg2.get_family())
        self.add(eg2)
        self.ate('lorentz')
        e1 = igual_em(tex('dx', Y_E1))
        e2 = igual_em(tex('dt', Y_E2))
        a1 = TransformByGlyphMap(eg1, e1, ([0, 1, 2, 3], [0, 1, 2, 3]), (list(range(4, 11)), list(range(6, 13))),
                                 ([], [4, 5, 13]), auto_fade=True, auto_morph=False, printing=False)
        a2 = TransformByGlyphMap(eg2, e2, ([0, 1, 2, 3], [0, 1, 2, 3]), ([4, 5], [6, 7]),
                                 ([], [4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16]), auto_fade=True, auto_morph=False, printing=False)
        self.play(a1, a2, run_time=1.6)
        for m in (eg1, eg2, e1, e2):
            self.remove(*m.get_family())
        self.add(e1, e2)
        novos = VGroup(*[Underline(glyphs(m, idx), buff=.06, color=GEO, stroke_width=2.6).set_z_index(45)   # o que é novo
                         for m, idx in ((e1, [4]), (e2, [4]), (e2, list(range(8, 16))))])
        self.play(Create(novos), run_time=.6)
        self.ate('gama_def')
        gd = tex('gd').set_color(GEO)
        gd.move_to([0, e2.get_bottom()[1] - .7 - gd.height / 2, 0])
        self.play(TransformFromCopy(glyphs(e1, [4]), gd[0][0], path_arc=.4), Write(VGroup(*gd[0][1:])), run_time=.8)
        self.remove(*gd.get_family())
        self.add(gd)
        # coluna da derivação: todas as linhas no mesmo tamanho, '=' alinhado, ⇓ entre elas, cada uma nasce da anterior
        larg = [(tex(k)[0][3].get_x() - tex(k).get_left()[0], tex(k).get_right()[0] - tex(k)[0][3].get_x())
                for k in ('v1', 'v2', 'v2b', 'v3', 'v4')]
        self.x_igual = (max(l for l, _ in larg) - max(r for _, r in larg)) / 2
        self.ate('razao')
        self.play(Uncreate(novos), Unwrite(gd), Indicate(d2, color=VB, scale_factor=1.12), run_time=.9)
        self.ate('monta')
        # substituição: os lados direitos de dx′ e dt′ entram na razão; dx′ e dt′ voltam para dentro de v_B′ = dx′/dt′
        v1 = self.alinha(tex('v1'))
        v1.set_y(COL_TOP - v1.height / 2)
        copias = [glyphs(d2, [0, 1, 2, 3]).copy(), glyphs(d2, [7]).copy()]
        self.play(Transform(copias[0], glyphs(v1, [0, 1, 2, 3]).copy(), path_arc=.5),
                  Transform(copias[1], glyphs(v1, [14]).copy(), path_arc=.5),
                  Transform(glyphs(e1, list(range(4, 14))), glyphs(v1, list(range(4, 14))).copy(), path_arc=-.3),
                  Transform(glyphs(e2, list(range(4, 17))), glyphs(v1, list(range(15, 28))).copy(), path_arc=.3),
                  Transform(glyphs(e1, [0, 1, 2, 3]), glyphs(d2, [4, 5, 6]).copy()),
                  Transform(glyphs(e2, [0, 1, 2, 3]), glyphs(d2, [8, 9, 10]).copy()), run_time=1.7, rate_func=smooth)
        self.remove(*copias, *e1.get_family(), *e2.get_family())
        self.add(v1)
        eq = v1
        self.coluna = [(eq, [])]
        self.ate('gama')
        g = glyphs(eq, [4, 15])
        rings = VGroup(*[Circle(radius=.21, color=GEO, stroke_width=2.6).move_to(m) for m in g]).set_z_index(45)
        self.play(g.animate.set_color(GEO), Create(rings), run_time=.8)
        self.ate('gama_risca')
        sk = strikes(glyphs(eq, [4]), glyphs(eq, [15]))
        self.play(Create(sk), run_time=.4)
        self.coluna[-1][1].append(sk)
        self.ate('gama_cancela')
        eq = self.deriva('v2', ([0, 1, 2, 3], [0, 1, 2, 3]), ([4, 5, 13], []), (list(range(6, 13)), list(range(4, 11))),
                         ([14], [11]), ([15, 16, 27], []), (list(range(17, 27)), list(range(12, 22))),
                         rt=1.5, extras=(Uncreate(rings),))
        self.ate('dt_hint')
        self.play(Indicate(glyphs(eq, [9, 10, 12, 13]), color=GEO, scale_factor=1.3), run_time=.5)
        self.ate('dt_divide')
        eq = self.deriva('v2b', ([0, 1, 2, 3], [0, 1, 2, 3]), ([], [4]), (list(range(4, 11)), list(range(5, 12))),
                         ([], [12, 13, 14, 15]), ([11], [16]), ([], [17]), (list(range(12, 22)), list(range(18, 28))),
                         ([], [28, 29, 30, 31]), rt=1.4)
        self.ate('distribui')
        eq = self.deriva('v3', ([0, 1, 2, 3], [0, 1, 2, 3]), ([4, 12], []), ([5, 6], [4, 5]), ([13], [6]), ([14, 15], [7, 8]),
                         ([7], [9]), ([8, 9], [10, 11]), ([10, 11], []), ([16], [12]), ([17, 28], []),
                         ([18, 19], [13]), ([20], [14]), ([21, 22], [15, 16]), ([23, 24], [20, 21]), ([25], [17]),
                         ([26, 27], [18, 19]), ([29, 30, 31], [22, 23, 24]), rt=1.7)
        self.ate('vb')
        self.play(Indicate(d1, color=VB, scale_factor=1.15),
                  glyphs(eq, [4, 5, 6, 7, 8, 20, 21, 22, 23, 24]).animate.set_color(VB), run_time=.9)
        self.ate('formula')
        eq = self.deriva('v4', ([0, 1, 2, 3], [0, 1, 2, 3]), ([4, 5, 6, 7, 8], [4, 5]), ([9], [6]), ([10, 11], [7, 8]),
                         ([12], [9]), ([13], [10]), ([14], [11]), ([15, 16], [12, 13]), ([17], [16]), ([18, 19], [17, 18]),
                         ([20, 21, 22, 23, 24], [14, 15]), rt=1.3)
        self.ate('caixa')
        resto = VGroup(*[VGroup(m, *anexos) for m, anexos in self.coluna[:-1]], *self.setas_col())
        self.play(Unwrite(VGroup(resto, d1, d2)), eq.animate.move_to([0, .3, 0]), run_time=.6)
        box = SurroundingRectangle(eq, buff=.28, corner_radius=.14, color=TEXT_COLOR, stroke_width=2.6)
        self.play(Create(box), run_time=.4)
        self.coluna = []

        # ── C05 · substituição: valores voam dos foguetes; ponteiro e contador encolhem juntos; resultado ao slot ─
        self.ate('c05')
        cen = self.cenario({'A': r'v_A=+0{,}8c', 'B': r'v_B=-0{,}8c'})
        self.agrow.set_value(1)
        tg = tag('TERRA')
        ruler = self.build_ruler()
        eq_low = tex('v4', Y_EQ)
        self.show(*cen, self.labs['A'], self.labs['B'], tg, rt=.8,
                  extras=(Uncreate(box), Transform(eq, eq_low)))
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
        eq = self.assemble(tex('S1', Y_EQ),
                           [(glyphs(eq, [0, 1, 2, 3]), [0, 1, 2, 3]), (glyphs(eq, [6]), [11]), (glyphs(eq, [9]), [19]),
                            (glyphs(eq, [10, 11]), [20, 21]), (glyphs(eq, [16, 17, 18]), [36, 37, 38]),
                            (lb[0][3:8], [5, 6, 7, 8, 9], {'path_arc': -1.1}),
                            (la[0][3:8], [13, 14, 15, 16, 17], {'path_arc': 1.1}),
                            (la[0][3:8], [23, 24, 25, 26, 27], {'path_arc': 1.1}),
                            (lb[0][3:8], [30, 31, 32, 33, 34], {'path_arc': -1.1})],
                           fade=[eq], rt=1.7, rings=(la[0][3:8], lb[0][3:8]))
        self.ate('numerador')
        eq = self.morph(eq, tex('S2', Y_EQ),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([5, 11], [4]), ([6, 7, 8, 14, 15, 16], [5, 6, 7]), ([9, 17], [8]),
                        ([4, 10, 12, 13, 18], []), (list(range(19, 39)), list(range(9, 29))), rt=1.2,
                        extras=(Indicate(VGroup(pc, pcl), color=GEO, scale_factor=1.08),))
        self.ate('sinais')
        sign_note = mtex(r'(+)\cdot(-)=(-)').move_to([0, Y_N1, 0])
        self.play(Indicate(glyphs(eq, [13, 20]), color=TEXT_COLOR, scale_factor=1.6), Write(sign_note), run_time=1.0)
        self.ate('produto')
        eq = self.morph(eq, tex('S2b', Y_EQ),
                        (list(range(12)), list(range(12))), ([13, 20], [12]), ([14, 15, 16, 21, 22, 23], [13, 14, 15, 16]),
                        ([17, 24], [17, 18]), ([12, 18, 19, 25], []), ([26], [19]), ([27], [20]), ([28], [21]), rt=1.2)
        self.ate('c2_risca')
        cc = strikes(glyphs(eq, [17, 18]), glyphs(eq, [20, 21]))
        self.play(Create(cc), run_time=.4)
        self.ate('c2_cancela')
        eq = self.morph(eq, tex('S3', Y_EQ),
                        (list(range(12)), list(range(12))), ([], [12]), ([12], [13]), ([13, 14, 15, 16], [14, 15, 16, 17]),
                        ([17, 18, 19, 20, 21], []), ([], [18]), rt=1.0, extras=(Uncreate(cc),))
        self.ate('sinal_nota2')
        sn2 = tex('sn2', Y_N1)          # o denominador desce para a nota: −(−0,64) = +0,64
        self.play(Unwrite(sign_note), TransformFromCopy(glyphs(eq, list(range(11, 19))), glyphs(sn2, list(range(8)))),
                  Write(glyphs(sn2, list(range(8, 14)))), run_time=.9)
        self.remove(*sn2.get_family())
        self.add(sn2)
        sign_note = sn2
        self.ate('um_mais')
        eq = self.morph(eq, tex('S4', Y_EQ),
                        (list(range(11)), list(range(11))), ([11, 13], [11]), ([12, 18], []),
                        ([14, 15, 16, 17], [12, 13, 14, 15]), rt=1.0)
        self.ate('um64')
        eq = self.morph(eq, tex('S5', Y_EQ),
                        (list(range(11)), list(range(11))), ([11, 12], []), ([13], [11]), ([14], [12]), ([15], [13]),
                        rt=1.0, extras=(Unwrite(sign_note),))
        self.ate('fracao')
        # o ponteiro clássico encolhe com o quociente (1,6 → 1,6/1,64 → 0,976); o rótulo conta junto
        pcl.clear_updaters()
        conta = self.ptr_conta('cls', 3, dim=True)
        self.pc_curva = (E['fracao'], E['encolhe_fim'], 1.6, 40 / 41)
        self.add(conta)
        eq = self.morph(eq, tex('S6', Y_EQ),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([4], [4]), ([5, 6, 7], [5, 6, 7]), ([8], [13], {'path_arc': -.6}),
                        ([9], [8]), ([10, 11, 12, 13], [9, 10, 11, 12]), rt=1.0, extras=(FadeOut(pcl, run_time=.3),))
        self.ate('q4041')
        eq = self.morph(eq, tex('S7', Y_EQ),
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
        self.play(glyphs(eq, [4, 12]).animate.set_color(GEO).set_opacity(.75), run_time=.8)
        self.ate('modulo')
        mod = tex('S8', -3.95)
        # cada pedaço desce direto da sua posição na linha de cima (v_B′, ≈, 0,976c); só as barras do módulo são novas
        mbox = SurroundingRectangle(mod, buff=.09, corner_radius=.1, color=VB, stroke_width=2.4)
        self.play(*[TransformFromCopy(glyphs(eq, a), glyphs(mod, b)) for a, b in
                    (([0, 1, 2], [1, 2, 3]), ([11], [5]), ([13, 14, 15, 16, 17, 18], [6, 7, 8, 9, 10, 11]))],
                  Write(glyphs(mod, [0, 4]), rate_func=lambda u: smooth(max(0, u - .4) / .6)),
                  Create(mbox, rate_func=lambda u: smooth(max(0, u - .5) * 2)), run_time=.9)
        self.remove(*mod.get_family())
        self.add(mod)
        self.ate('ao_slot')
        novo = slot_mob(tex('S8', 0, 54))
        # o slot do topo vira o resultado no lugar (nada atravessa a conta): v_B′ = ? → |v_B′| ≈ 0,976c
        self.play(TransformByGlyphMap(self.slot[0], novo[0], ([0, 1, 2], [1, 2, 3]), ([3], [5]), ([4], [6, 7, 8, 9, 10, 11]),
                                      ([], [0, 4]), auto_fade=True, auto_morph=False, printing=False),
                  self.slot[1].animate.move_to(novo[1]), Indicate(VGroup(mod, mbox), color=VB, scale_factor=1.08),
                  run_time=1.0)
        self.remove(*self.slot.get_family(), *novo.get_family())
        self.add(novo)
        self.slot = novo
        self.ate('lupa')
        lupa = self.zoom_inset(40 / 41)
        self.play(Unwrite(mod), Uncreate(mbox), FadeIn(lupa), run_time=.6)

        # ── C07 · limite clássico: o foguete vira carro; o termo v_A v_B/c² fica visível, perto de 0 ────────────
        self.ate('c07')
        self.drop(eq, pr, prl, lupa, ruler, *cen, *self.labs.values(), self.slot, rt=.4)
        self.labs, self.slot = {}, None
        self.pr.set_value(0)
        self.ate('carros')
        yc = Y_GROUND + .42
        cA = chip(words('A', 0, 24, TEXT_COLOR), pad=(.09, .05)).move_to([-2.4, yc, 0])
        cB = chip(words('B', 0, 24, TEXT_COLOR), pad=(.09, .05)).move_to([2.4, yc, 0])
        kA = Arrow([-2.4, 2.35, 0], [-1.2, 2.35, 0], buff=0, color=VA, stroke_width=8, max_tip_length_to_length_ratio=.25)
        kB = Arrow([2.4, 2.35, 0], [1.2, 2.35, 0], buff=0, color=VB, stroke_width=8, max_tip_length_to_length_ratio=.25)
        tA = vtex(r'v_A=+30\ \mathrm{m/s}', 40).move_to([-2.0, 2.85, 0])
        tB = vtex(r'v_B=-30\ \mathrm{m/s}', 40, VB).move_to([2.0, 2.85, 0])
        terra7 = words('TERRA', Y_TERRA, 26, GEO)
        self.play(FadeIn(VGroup(cA, cB, terra7)), GrowArrow(kA), GrowArrow(kB), FadeIn(tA), FadeIn(tB), run_time=.7)
        self.ate('g1')
        g1 = tex('G1', -.9)
        self.play(Write(g1), run_time=.7)
        self.ate('g2')
        g2 = tex('G2', -2.3)
        self.play(TransformByGlyphMap(g1, g2, ([1, 2, 3, 4], [2, 3, 4, 5]), ([6], [6]), ([7, 8], [7, 8]), ([], [0, 1]),
                                      ([9], [9]), ([10], [10]), ([0, 5, 11, 12, 13, 14], []), from_copy=True,
                                      auto_fade=True, auto_morph=False, printing=False), run_time=.8)
        self.remove(*g2.get_family())
        self.add(g2)
        self.ate('termo_encolhe')
        termo = glyphs(g2, [2, 3, 4, 5, 6, 7, 8])
        anel = SurroundingRectangle(termo, buff=.08, corner_radius=.08, color=GEO, stroke_width=2)
        self.play(termo.animate.scale(.8), Create(anel), run_time=.8)
        self.ate('g3')
        g3 = tex('G3', -3.65)
        g3box = SurroundingRectangle(g3, buff=.14, corner_radius=.12, color=TEXT_COLOR, stroke_width=2.4)
        self.play(Write(g3), Create(g3box), Uncreate(anel), run_time=.8)
        self.ate('galileu')
        self.play(Indicate(g3, color=TEXT_COLOR, scale_factor=1.1), run_time=.6)

        # ── C08 · perto de c: a mesma régua; ponteiro e número andam juntos; sem parede ──────────────────────
        self.ate('c08')
        self.drop(cA, cB, kA, kB, tA, tB, terra7, g1, g2, g3, g3box, rt=.4)
        self.ate('regua8')
        cen = self.cenario({'A': r'v_A=+0{,}5c', 'B': r'v_B=-0{,}5c'})
        ruler = self.build_ruler()
        self.show(*cen, self.labs['A'], self.labs['B'], rt=.4)
        self.abre_regua(ruler, rt=.3)
        self.ate('soma_simples')
        key_c = VGroup(DashedLine(LEFT * .4, RIGHT * .4, color=GEO, stroke_width=6, dash_length=.12).set_stroke(opacity=.8),
                       words('SOMA SIMPLES', 0, 26, GEO)).arrange(RIGHT, buff=.18)
        key_r = VGroup(Line(LEFT * .4, RIGHT * .4, color=VB, stroke_width=10),
                       words('MEDIDO POR A', 0, 26, GEO)).arrange(RIGHT, buff=.18)
        keys = VGroup(key_c, key_r).arrange(RIGHT, buff=.6).move_to([0, -1.95, 0])
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
        h1 = tex('H1', -3.05)
        self.play(Write(h1), run_time=.7)
        self.ate('acelera')
        ticks = VGroup(self.ghost_tick(.8), self.ghost_tick(40 / 41))
        self.relabel('A', r'v_A=+0{,}99c', rt=.5, extras=(FadeIn(ticks),))
        self.relabel('B', r'v_B=-0{,}99c', rt=.4)
        self.ate('cls2')
        self.play(self.pc.animate.set_value(1.98), h1.animate.set_opacity(.35), run_time=.6)
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
        h2 = tex('H2a', -3.05)
        h2 = self.morph(h1, h2, (list(range(8)), list(range(8))), ([8], [8, 9]), ([9], [10]), ([10], [11]),
                        ([11, 12], [12, 13]), ([13], [14, 15]), ([14], [16]), ([15], [17]), ([16], [18]), ([17], [19]),
                        ([18, 19], [20, 21]), ([20, 21], [22, 23, 24, 25]), (list(range(22, 27)), []), rt=.75)
        self.ate('menor_c')
        below = mtex(r'\approx0{,}99995\,c<c')
        below[0][1:8].set_color(VB)
        below.move_to([0, -4.0, 0])
        self.play(Write(below), run_time=.5)

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
        self.slot = slot_mob(tex('S8', 0, 54))
        self.ate('terra9')
        self.show(self.labs['A'], self.labs['B'], prl, self.slot, rt=.3)
        self.ate('fecha9')
        br = self.bracket()
        self.add(br)
        close = self.na_terra_16()
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
        self.troca_slot(slot_mob(vtex(r'0{,}976c', 54, VB), 'A MEDE B A', antes=True), rt=.5)
        self.ate('troca9B')
        self.relabel('B', None, rt=.3)
        self.ate('tagB9')
        tg = self.swap_tag(tg, 'FOGUETE B')
        self.ate('a976')
        self.relabel('A', r'0{,}976c', rt=.5)
        self.ate('slotB')
        self.troca_slot(slot_mob(vtex(r'0{,}976c', 54, VA), 'B MEDE A A', antes=True), rt=.4)
        self.ate('cada')
        self.ate('fecho1')
        self.ate('fecho2')
        f1 = VGroup(words('CORPOS COM MASSA:', 0, 38), mtex('v<c', 54)).arrange(RIGHT, buff=.28)
        f1.move_to([0, -3.3, 0])
        self.play(FadeIn(f1[0], shift=UP * .08), Write(f1[1]), run_time=.8)

        # ── C10 · CTA, separado do fecho físico ──────────────────────────────────────────────────────────────
        self.ate('c10')
        for m in list(self.mobjects):
            if m is not relogio:
                m.clear_updaters()
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not relogio], run_time=.6)
        self.clear()
        self.add(relogio)
        self.ate('cta')
        logo = ImageMobject(str(WATERMARK_PATH)).set_width(4.6).move_to([0, 2.4, 0])
        linha2 = words('SEGUE O PARALLAX LAB', -.6, 44)
        handle = words('@labparallax', -1.8, 48).set_color_by_gradient(CYAN, PINK)
        self.play(FadeIn(logo, scale=.96), run_time=.7)
        self.play(FadeIn(linha2, shift=UP * .08), FadeIn(handle, shift=UP * .08), run_time=.6)
        self.ate('fim')
        self.play(FadeOut(Group(logo, linha2, handle)), run_time=.5)
        self.ate(TL['duracao_s'], 'duracao')
        out = Path(config.media_dir) / ('estados_vid0028_' + os.environ.get('ESTADOS', 'v6') + '.json')
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({'eventos': self.events, 'atrasos': self.atrasos, 'ocupado': self.ocupado,
                                   'duracao': round(self.agora(), 3),
                                   'quadros': round(self.agora() * config.frame_rate)}, ensure_ascii=False, indent=1),
                       encoding='utf-8')
        print('ATRASOS:', self.atrasos)
