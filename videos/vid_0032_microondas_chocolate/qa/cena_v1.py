"""vid_0032 — Dá para medir a luz com chocolate? Camada Manim (transparente) do preview silencioso, C01–C07.

O 3D (cena3d/, render3d.js) é o fundo só no C01; em 13–14 s um retângulo da cor de fundo do template cobre o 3D e a
barra 2D assume, alinhada ao timeline.json. Tudo que oscila é função do tempo absoluto (self.renderer.time), por isso
pular animações (-n) não quebra o estado. Tempos: timeline.json (fonte única). Mapa de calor: mapa_calor.py.
Render do preview (na raiz do repositório):
    uv run python -m manim -t -r 540,960 --fps 15 videos/vid_0032_microondas_chocolate/cena.py Microondas032
"""
from pathlib import Path
import json
import os
import sys
import numpy as np
from manim import *
from MF_Tools import TransformByGlyphMap
from manim.utils.exceptions import EndSceneEarlyException

ROOT = Path(__file__).resolve().parents[2]
UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(UNIT))
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text
import mapa_calor

config.media_dir = str(UNIT / os.environ.get('MIDIA', 'media_preview'))
config.background_color = BACKGROUND_COLOR
TL = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))
EV, G = TL['eventos'], TL['geometria']

CYAN, HEAT, GEO, VIO, STEEL, DIM = PRIMARY_COLOR, '#FF7A3D', '#B8C4DA', '#9C8CFF', '#7A8696', '#8FA3C4'
PANEL, BLUE_L, MAG = '#0E2A52', '#7FB2FF', '#EA63FF'
CHOC, CHOC_D, GROOVE = '#4A2C1E', '#6B4029', '#2E1A11'

# ---------- geometria (unidades do Manim) ----------
K = G['manim_por_cm']                       # 1 unidade = 3,21 cm (C01–C04)
BAR_C = np.array([*G['centro_barra_manim'], 0.])
BAR_W, BAR_H = G['barra']['comprimento_cm'] * K, G['barra']['largura_cm'] * K
SPOTS = [x * K for x in G['manchas_x_cm']]  # −2,85; −0,95; 0,95; 2,85
LAM = 3.8                                   # λ na tela; paredes em ±3,8 = 2λ
KW = 2 * PI / LAM
XL, XR = -3.8, 3.8
XS = np.linspace(XL, XR, 241)
AMP_A, AMP_B = 0.9, 1.3
MAP_C = np.array([0, 0.9, 0])
MAP_W, MAP_H = 7.6, 6.73
KM = MAP_W / 35                             # escala do mapa (C05–C06): 35 cm = 7,6 unidades
R_PLATE = 14 * KM                           # 3,04

# ---------- fase do campo: ω visual por trechos (Hz), θ(t) = 2π ∫ f dt, exata para f linear por trecho ----------
FREQ = [(0, .5), (22, .5), (26, .8), (43, .8), (44.5, .4), (55, .4), (56.5, .8), (1e4, .8)]
_cum = [0.]
for (ta, fa), (tb, fb) in zip(FREQ, FREQ[1:]):
    _cum.append(_cum[-1] + (tb - ta) * (fa + fb) / 2)


def theta(t):
    for i, ((ta, fa), (tb, fb)) in enumerate(zip(FREQ, FREQ[1:])):
        if t <= tb:
            u = t - ta
            return 2 * PI * (_cum[i] + fa * u + (fb - fa) * u * u / (2 * (tb - ta)))
    return 0.


T_MEAN = EV['c03_media']
W_MEAN = 2 * PI * .8                        # ω constante a partir de 56,5 s


def mean_sin2(t):
    """Média de sen²θ de T_MEAN até t (exata, ω constante)."""
    d = t - T_MEAN
    if d < 1e-3:
        return np.sin(theta(max(t, T_MEAN))) ** 2
    return .5 - (np.sin(2 * theta(t)) - np.sin(2 * theta(T_MEAN))) / (4 * W_MEAN * d)


# ---------- texto e fórmulas ----------
def tx(s, size=24, color=TEXT_COLOR):
    s = s.upper()
    return screen_text(s, size, color=color, oversample=4 if len(s) < 30 else 2)


def tex(s, size=48, color=TEXT_COLOR, n=None, cores=()):
    """MathTex de string única; cores = ((cor, [índices de glifo]), ...)."""
    m = MathTex(s, font_size=size, color=color)
    if n is not None:
        assert len(m[0]) == n, f'{s!r}: {len(m[0])} glifos (esperado {n})'
    for c, idx in cores:
        for i in idx:
            m[0][i].set_color(c)
    return m


def titulo(*partes, y=6.1):
    g = VGroup(*[tx(p, 34) if isinstance(p, str) else p for p in partes]).arrange(RIGHT, buff=.18)
    return g.move_to([0, y, 0]).set_z_index(50)


def mancha(x, cor, alfa=.2, camadas=12, y=None):
    """Mancha de decaimento suave (σ = 0,75 cm): círculos concêntricos de opacidade baixa empilhados."""
    s = G['mancha_sigma_cm'] * K
    y = BAR_C[1] if y is None else y
    return VGroup(*[Circle(r, stroke_width=0).set_fill(cor, alfa).move_to([x, y, 0])
                    for r in np.linspace(2.0 * s, .25 * s, camadas)])


def barra_2d():
    corpo = Rectangle(width=BAR_W, height=BAR_H, stroke_width=0).set_fill(CHOC, 1).move_to(BAR_C)
    gx, gy = G['barra']['gomos']
    sulcos = VGroup(*[Line([BAR_C[0] - BAR_W / 2 + i * BAR_W / gx, BAR_C[1] - BAR_H / 2, 0],
                           [BAR_C[0] - BAR_W / 2 + i * BAR_W / gx, BAR_C[1] + BAR_H / 2, 0]) for i in range(1, gx)],
                    *[Line([BAR_C[0] - BAR_W / 2, BAR_C[1] - BAR_H / 2 + j * BAR_H / gy, 0],
                           [BAR_C[0] + BAR_W / 2, BAR_C[1] - BAR_H / 2 + j * BAR_H / gy, 0]) for j in range(1, gy)])
    sulcos.set_stroke(GROOVE, 2.2)
    manchas = VGroup(*[mancha(x, CHOC_D) for x in SPOTS])
    return VGroup(corpo, sulcos, manchas).set_z_index(5)


def curva(ys, y0, cor, larg, op, xs=XS):
    return VMobject().set_points_as_corners(np.c_[xs, y0 + ys, 0 * xs]).set_stroke(cor, larg, op)


class Microondas032(Scene):
    def T(self):
        return self.renderer.time

    def ate(self, t):
        # QA: QUADRO=t (com -s) para no instante t e salva o quadro, sem renderizar o vídeo.
        q = float(os.environ.get('QUADRO', 'inf'))
        if self.T() - 1e-6 <= q <= t:
            if q - self.T() > 1e-3:
                self.wait(q - self.T())
            raise EndSceneEarlyException()
        d = t - self.T()
        if d > 1e-3:
            self.wait(d)

    def live(self, f, z=10):
        m = f(self.T()).set_z_index(z)
        m.add_updater(lambda mob, dt: mob.become(f(self.T()).set_z_index(z)))
        return m

    def assenta(self, m):
        """Depois de um glyph map: troca os pedaços soltos no palco pela equação inteira."""
        fam = {id(x) for x in m.get_family()}
        soltos = [x for x in self.mobjects if x is not m and x.submobjects and id(x) not in fam
                  and all(id(y) in fam for y in x.get_family()[1:] if y.has_points())]
        self.remove(*soltos)
        self.add(m)

    def construct(self):
        # Tudo que depende do tempo precisa de um updater com dt (senão o wait vira quadro estático).
        self.add(Mobject().add_updater(lambda m, dt: None))
        tag = screen_text('ABSURDO CALCULÁVEL · EP. 04', 20, oversample=2).set_opacity(.65)
        tag.to_corner(UP + LEFT, buff=.4).set_z_index(60)
        logo = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.35).to_corner(UP + RIGHT, buff=.28)
        self.cab = Group(tag, logo)
        self.add(tag, logo)
        # Estado das zonas A (onda) e B (calor): eixo, escala vertical, opacidade.
        self.yA, self.sA, self.opA = ValueTracker(4.2), ValueTracker(1), ValueTracker(1)
        self.yB, self.sB, self.opB = ValueTracker(1.2), ValueTracker(1), ValueTracker(1)
        self.stand = ValueTracker(0)          # peso da estacionária na zona A
        self.vai = ValueTracker(1)            # peso das ondas que vão e voltam (só C02)
        self.c01()
        self.c02()
        self.c03()
        self.c04()
        self.c05()
        self.c06()
        self.c07()

    # ------------------------------------------------------------------ C01
    def c01(self):
        h1 = tx('Dá para medir a luz', 40)
        h2 = tx('com chocolate?', 40)
        head = VGroup(h1, h2).arrange(DOWN, buff=.16).move_to([0, 6.1, 0]).set_z_index(50)
        sub = tx('prato parado', 24, DIM).move_to([0, 5.25, 0]).set_z_index(50)
        self.ate(EV['c01_titulo'])
        self.play(FadeIn(head, shift=DOWN * .1), run_time=.8)
        self.ate(EV['c01_prato_parado'])
        self.play(FadeIn(sub), run_time=.6)
        self.ate(EV['c01_camera_topo'])
        self.fundo = Rectangle(width=9.4, height=16.4, stroke_width=0).set_fill(BACKGROUND_COLOR, 1).set_z_index(-100)
        self.bar = barra_2d()
        self.play(FadeIn(self.fundo), FadeIn(self.bar), FadeOut(head), FadeOut(sub), run_time=EV['c01_troca_fim'] - EV['c01_camera_topo'])

    # ------------------------------------------------------------------ C02
    def zona_a(self):
        """Paredes, eixo, ondas viajantes (C02) e estacionária; tudo lido dos trackers."""
        def f(t):
            y0, s, op = self.yA.get_value(), self.sA.get_value(), self.opA.get_value()
            th = theta(t)
            g = VGroup()
            for x in (XL, XR):
                g.add(Rectangle(width=.14, height=2.2 * s, stroke_width=0).set_fill(STEEL, op).move_to([x, y0, 0]))
            g.add(Line([XL, y0, 0], [XR, y0, 0]).set_stroke(DIM, 1.5, .5 * op))
            # C02: onda que vai (frente em xf) e onda que volta (frente em xr), amplitude 0,45 cada.
            a, v = AMP_A * s / 2, 1.9
            w_trav = self.vai.get_value()
            if w_trav > 1e-3 and t >= EV['c02_viaja']:
                xf = min(XR, XL + v * (t - EV['c02_viaja']))
                xi = XS[XS <= xf + 1e-9]
                if len(xi) > 1:
                    g.add(curva(a * np.cos(th - KW * xi), y0, CYAN, 5, op * w_trav, xi))
                if t >= EV['c02_reflete']:
                    xr = max(XL, XR - v * (t - EV['c02_reflete']))
                    xj = XS[XS >= xr - 1e-9]
                    if len(xj) > 1:
                        g.add(DashedVMobject(curva(-a * np.cos(th + KW * xj), y0, CYAN, 4, .5 * op * w_trav, xj),
                                             num_dashes=max(2, int(len(xj) / 6)), dashed_ratio=.6))
            ws = self.stand.get_value()
            if ws > 1e-3:
                g.add(curva(AMP_A * s * np.sin(KW * XS) * np.sin(th), y0, CYAN, 6, op * ws))
            return g
        return self.live(f, 10)

    def c02(self):
        self.ate(EV['c02'])
        self.tit = titulo('Onda parada')
        self.A = self.zona_a()
        self.add(self.A)
        self.play(FadeIn(self.tit), run_time=.6)
        # seta de sentido da onda que vai (some quando a onda chega na parede)
        seta = Arrow([-3.2, 5.45, 0], [-2.2, 5.45, 0], buff=0, stroke_width=4, color=CYAN,
                     max_tip_length_to_length_ratio=.3).set_z_index(12)
        self.play(GrowArrow(seta), run_time=.6)
        self.ate(EV['c02_reflete'] - .6)
        volta = Arrow([3.2, 5.45, 0], [2.2, 5.45, 0], buff=0, stroke_width=4, color=CYAN,
                      max_tip_length_to_length_ratio=.3).set_z_index(12).set_opacity(.5)
        self.play(FadeOut(seta), run_time=.6)
        self.play(GrowArrow(volta), run_time=.6)
        self.ate(EV['c02_estacionaria'])
        self.play(self.stand.animate.set_value(1), self.vai.animate.set_value(0), FadeOut(volta), run_time=5, rate_func=smooth)
        self.ate(EV['c02_nos'])
        y0 = self.yA.get_value()
        self.nos = VGroup(*[Dot([x, y0, 0], radius=.07, color=GEO) for x in np.arange(XL, XR + .01, LAM / 2)]).set_z_index(14)
        self.no_lbl = tx('nó', 20, GEO).move_to([-1.9, y0 - .42, 0]).set_z_index(14)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in self.nos], lag_ratio=.15), run_time=1.4)
        self.play(FadeIn(self.no_lbl), run_time=.5)
        self.ate(EV['c02_ventres'])
        self.ventres = VGroup(*[DoubleArrow([x, y0 - AMP_A, 0], [x, y0 + AMP_A, 0], buff=0, stroke_width=2.5, color=CYAN,
                                            tip_length=.16, max_tip_length_to_length_ratio=.2) for x in SPOTS]).set_z_index(13)
        self.ventre_lbl = tx('ventre', 20, CYAN).move_to([2.85, y0 + AMP_A + .3, 0]).set_z_index(14)
        self.play(LaggedStart(*[GrowFromCenter(a) for a in self.ventres], lag_ratio=.15), run_time=1.4)
        self.play(FadeIn(self.ventre_lbl), run_time=.5)

    # ------------------------------------------------------------------ C03
    def c03(self):
        self.ate(EV['c03'])
        y0 = self.yA.get_value()
        e2 = MathTex('E^2', font_size=48, color=HEAT)
        novo = titulo('O calor vai com', e2)
        self.play(FadeOut(self.tit, shift=UP * .2), FadeIn(novo, shift=UP * .2), FadeOut(self.ventres), FadeOut(self.ventre_lbl),
                  FadeOut(self.no_lbl), self.opA.animate.set_value(.3), self.nos.animate.set_opacity(.3), run_time=1)
        self.tit = novo
        xv = SPOTS[2]                                                   # ventre em x = 0,95
        seg = XS[(XS >= 0) & (XS <= 1.9)]
        realce = self.live(lambda t: curva(AMP_A * np.sin(KW * seg) * np.sin(theta(t)), y0, CYAN, 6, 1, seg), 11)

        def seta(t):
            s = np.sin(theta(t))
            g = VGroup()
            if abs(s) > .08:
                g.add(Arrow([xv, y0, 0], [xv, y0 + AMP_A * s, 0], buff=0, stroke_width=5, color=CYAN, tip_length=.18,
                            max_tip_length_to_length_ratio=.45))
            g.add(MathTex('E', font_size=40, color=CYAN).move_to([xv - .4, y0 + .45 * AMP_A * s, 0]))
            sinal = MathTex('+' if s > 0 else '-', font_size=48, color=CYAN).move_to([xv + .45, y0 + .55 * np.sign(s), 0])
            g.add(sinal.set_opacity(np.clip((abs(s) - .2) / .3, 0, 1)))
            return g
        vetor = self.live(seta, 15)
        yb = self.yB.get_value()
        eixoB = Line([XL, yb, 0], [XR, yb, 0]).set_stroke(DIM, 1.5, .5).set_z_index(10)
        caixa = Rectangle(width=.35, height=AMP_B, stroke_color=HEAT, stroke_width=2).move_to([xv, yb + AMP_B / 2, 0]).set_z_index(12)

        def enche(t):
            s2 = np.sin(theta(t)) ** 2
            g = VGroup(Rectangle(width=.35, height=max(AMP_B * s2, 1e-3), stroke_width=0).set_fill(HEAT, .9)
                       .move_to([xv, yb, 0], aligned_edge=DOWN))
            g.add(MathTex('+', font_size=44, color=HEAT).move_to([xv - .45, yb + AMP_B * .62, 0]).set_opacity(np.clip((s2 - .04) / .2, 0, 1)))
            return g
        fill = self.live(enche, 12)
        rot = MathTex('E^2', font_size=44, color=HEAT).move_to([1.6, yb + AMP_B / 2, 0]).set_z_index(12)
        self.play(FadeIn(realce), FadeIn(vetor), run_time=.8)
        self.ate(EV['c03_medidor_ciclos'])
        self.play(Create(eixoB), FadeIn(caixa), FadeIn(fill), FadeIn(rot), run_time=1)

        # 3b — a linha toda: instantânea pulsando e média que converge
        self.ate(EV['c03_instantanea'])
        self.remove(realce)
        self.play(FadeOut(vetor), self.opA.animate.set_value(1), self.nos.animate.set_opacity(1), run_time=.8)
        inst_f = lambda t: curva(AMP_B * self.sB.get_value() * np.sin(KW * XS) ** 2 * np.sin(theta(t)) ** 2,
                                 self.yB.get_value(), HEAT, 2.5, .6 * self.opB.get_value())
        inst = self.live(inst_f, 11)
        onda = curva(AMP_A * np.sin(KW * XS) * np.sin(theta(self.T())), y0, CYAN, 6, 1)
        alvo = inst_f(self.T() + .8).set_z_index(11)
        self.play(TransformFromCopy(onda, alvo), run_time=.8)
        self.remove(alvo)
        self.add(inst)
        self.ate(EV['c03_media'])
        self.media_f = lambda t: curva(AMP_B * self.sB.get_value() * np.sin(KW * XS) ** 2 * mean_sin2(t),
                                       self.yB.get_value(), HEAT, 6, self.opB.get_value())
        media = self.live(self.media_f, 12)
        self.add(media)
        self.ate(EV['c03_medidor_pico'])
        corc = XS[(XS >= 0) & (XS <= 1.9)]
        hump = curva(AMP_B * np.sin(KW * corc) ** 2 * mean_sin2(self.T() + 1.2), yb, HEAT, 6, 1, corc).set_z_index(13)
        rot2 = MathTex(r'\langle E^2 \rangle', font_size=44, color=HEAT).move_to([3.55, yb + 1.0, 0]).set_z_index(12)
        self.remove(fill)
        cheio = Rectangle(width=.35, height=AMP_B * np.sin(theta(self.T())) ** 2 + 1e-3, stroke_width=0).set_fill(HEAT, .9)
        cheio.move_to([xv, yb, 0], aligned_edge=DOWN)
        self.play(ReplacementTransform(VGroup(caixa, cheio), hump), ReplacementTransform(rot, rot2), run_time=1.2)
        self.remove(hump)
        self.play(inst.animate.set_stroke(opacity=.35), run_time=.3)
        inst.clear_updaters()
        self.remove(inst)
        self.inst = self.live(lambda t: inst_f(t).set_stroke(opacity=.3 * self.opB.get_value()), 11)
        self.add(self.inst)
        self.eixoB, self.media, self.rotB = eixoB, media, rot2
        eixoB.add_updater(lambda m, dt: m.put_start_and_end_on([XL, self.yB.get_value(), 0], [XR, self.yB.get_value(), 0])
                          .set_stroke(opacity=.5 * self.opB.get_value()))

        # 3c — o período cai pela metade
        self.ate(EV['c03_chaves'])
        bA = BraceBetweenPoints([0, y0 - AMP_A - .08, 0], [XL, y0 - AMP_A - .08, 0], direction=DOWN, color=GEO)
        lA = MathTex(r'\lambda', font_size=44, color=GEO).next_to(bA, DOWN, buff=.08)
        bB = BraceBetweenPoints([-.95, yb - .1, 0], [-2.85, yb - .1, 0], direction=DOWN, color=GEO)
        lB = MathTex(r'\lambda/2', font_size=44, color=GEO).next_to(bB, DOWN, buff=.08)
        chaves = VGroup(bA, lA, bB, lB).set_z_index(16)
        self.play(GrowFromCenter(bA), FadeIn(lA), run_time=.8)
        self.play(GrowFromCenter(bB), FadeIn(lB), run_time=.8)

        # 3d — as manchas nascem dos picos
        self.ate(EV['c03_manchas'])
        topo = yb + AMP_B * .5
        guias = VGroup(*[DashedLine([x, topo, 0], [x, BAR_C[1], 0], dash_length=.12).set_stroke(DIM, 2, .8) for x in SPOTS]).set_z_index(6)
        brilho = VGroup(*[mancha(x, HEAT, alfa=.22) for x in SPOTS]).set_z_index(7).set_opacity(0)
        frase = VGroup(tx('uma mancha a cada', 26), MathTex(r'\lambda/2', font_size=44, color=GEO)).arrange(RIGHT, buff=.16)
        frase.move_to([0, -3.0, 0]).set_z_index(16)
        self.play(FadeOut(VGroup(bB, lB)), LaggedStart(*[Create(g) for g in guias], lag_ratio=.15), run_time=1.2)
        for b in brilho:
            for c in b:
                c.set_fill(HEAT, 0)
        self.play(*[c.animate.set_fill(HEAT, .22) for b in brilho for c in b], FadeIn(frase), run_time=.8)
        self.play(*[c.animate.set_fill(HEAT, 0) for b in brilho for c in b], run_time=1.2)
        self.remove(brilho)
        self.c03_saida = VGroup(bA, lA, guias, frase)

    # ------------------------------------------------------------------ C04
    def c04(self):
        self.ate(EV['c04'])
        novo = titulo('A conta')
        self.play(FadeOut(self.tit), FadeIn(novo), FadeOut(self.c03_saida),
                  self.yA.animate.set_value(4.8), self.sA.animate.set_value(.8), self.opA.animate.set_value(.25),
                  self.yB.animate.set_value(2.9), self.sB.animate.set_value(.8), self.opB.animate.set_value(.25),
                  self.rotB.animate.move_to([3.55, 2.9 + .8, 0]).set_opacity(.25),
                  self.nos.animate.set_opacity(0), run_time=1.5)
        self.tit = novo
        self.remove(self.nos)
        # régua de centro a centro das manchas 2 e 3
        yr = BAR_C[1] + BAR_H / 2 + .14
        x0, x1 = SPOTS[1], SPOTS[2]
        regua = VGroup(Line([x0, yr, 0], [x1, yr, 0]).set_stroke(GEO, 3))
        for cm in range(7):
            x = x0 + min(cm, 6.1) * K
            if x <= x1 + 1e-6:
                regua.add(Line([x, yr, 0], [x, yr + (.16 if cm % 5 == 0 else .1), 0]).set_stroke(GEO, 2))
        regua.add(Line([x1, yr - .08, 0], [x1, yr + .18, 0]).set_stroke(GEO, 3), Line([x0, yr - .08, 0], [x0, yr + .18, 0]).set_stroke(GEO, 3))
        d_lbl = tex(r'd = 6{,}1\ \text{cm}', 40, GEO, 7, ((TEXT_COLOR, [1]),)).move_to([-2.35, yr + .12, 0])
        ilus = tx('medida ilustrativa', 18, DIM).move_to([2.4, yr + .1, 0])
        regua.set_z_index(16), d_lbl.set_z_index(16), ilus.set_z_index(16)
        self.play(Create(regua), run_time=1.2)
        self.play(FadeIn(d_lbl), FadeIn(ilus), run_time=.8)

        # d = λ/2 → λ = 2d = 12,2 cm
        self.ate(EV['c04_d_lambda'])
        L1a = MathTex('d', '=', r'\frac{\lambda}{2}', font_size=48).move_to([-3.85, 2.35, 0], aligned_edge=LEFT).set_z_index(20)
        L1a[0].set_color(GEO)
        frac = L1a[2]
        max(frac, key=lambda g: g.get_center()[1]).set_color(GEO)      # λ é o glifo mais alto da fração
        L1b = MathTex(r'\lambda', '=', '2', 'd', '=', r'12{,}2\ \text{cm}', font_size=48).move_to([-3.85, 2.35, 0], aligned_edge=LEFT).set_z_index(20)
        for i in (0, 3, 5):
            L1b[i].set_color(GEO)
        self.play(TransformFromCopy(d_lbl[0][0], L1a[0]), FadeIn(L1a[1:]), run_time=1)
        self.wait(.6)
        self.play(TransformMatchingTex(L1a, L1b), run_time=1.4)
        y0 = self.yA.get_value()
        bA = BraceBetweenPoints([0, y0 - .72 - .08, 0], [XL, y0 - .72 - .08, 0], direction=DOWN, color=GEO)
        lA = MathTex(r'\lambda', font_size=40, color=GEO).next_to(bA, DOWN, buff=.06)
        pisca = VGroup(bA, lA).set_z_index(16)
        self.play(FadeIn(pisca), Indicate(L1b[0], color=GEO, scale_factor=1.15), run_time=.6)
        self.play(Indicate(pisca, color=GEO, scale_factor=1.06), run_time=.8)
        self.play(FadeOut(pisca), run_time=.5)

        # etiqueta do forno
        self.ate(EV['c04_etiqueta'])
        etq_box = RoundedRectangle(width=3.0, height=1.2, corner_radius=.12, stroke_color=BLUE_L, stroke_width=2)
        etq_box.set_fill(PANEL, 1).move_to([2.6, 1.4, 0])
        etq_t = tx('frequência', 20).move_to(etq_box.get_center() + UP * .3)
        etq_f = tex(r'2450\ \text{MHz}', 44, VIO, 7).move_to(etq_box.get_center() + DOWN * .2)
        etq = VGroup(etq_box, etq_t, etq_f).set_z_index(18)
        self.play(FadeIn(etq, shift=LEFT * .2), run_time=.8)
        self.wait(1.5)
        L2 = tex(r'f = 2{,}45\times10^{9}\ \text{Hz}', 48, VIO, 12, ((TEXT_COLOR, [1]),)).move_to([-3.85, 1.68, 0], aligned_edge=LEFT).set_z_index(20)
        self.play(TransformFromCopy(etq_f, L2), run_time=1.4)

        # por que v = λ·f: onda viajante, crista anda um λ por oscilação
        self.ate(EV['c04_viajante'])
        T0, P = EV['c04_viajante'] + 1, 3.0

        def viaja(t):
            y, a = self.yA.get_value(), AMP_A * .8
            u = max(0., min(t, T0 + 2 * P) - T0) / P              # oscilações completas desde T0
            ys = a * np.cos(2 * PI * u - KW * (XS - XL))
            xc = XL + LAM * u
            return VGroup(curva(ys, y, CYAN, 6, self.trav.get_value()),
                          Dot([xc, y + a, 0], radius=.09, color=WHITE).set_opacity(self.trav.get_value()))
        self.trav = ValueTracker(0)
        trav = self.live(viaja, 14)
        self.add(trav)
        self.play(self.opA.animate.set_value(1), self.stand.animate.set_value(0), self.trav.animate.set_value(1), run_time=1)
        y0 = self.yA.get_value()
        cont = [tx('1 oscilação', 20, DIM), tx('2 oscilações', 20, DIM)]
        for c in cont:
            c.move_to([2.75, 5.85, 0]).set_z_index(16)
        for k in range(2):
            b = BraceBetweenPoints([XL + LAM * (k + 1), y0 - .72 - .08, 0], [XL + LAM * k, y0 - .72 - .08, 0], direction=DOWN, color=GEO)
            lb = MathTex(r'\lambda', font_size=40, color=GEO).next_to(b, DOWN, buff=.06)
            ch = VGroup(b, lb).set_z_index(16)
            self.play(GrowFromCenter(b), run_time=P * .25)
            self.ate(T0 + P * (k + 1) - .3)
            self.play(FadeIn(lb), FadeIn(cont[k]) if k == 0 else ReplacementTransform(cont[0], cont[1]), run_time=.3)
            self.wait(.4)
            self.play(FadeOut(ch), run_time=.3)
        self.ate(EV['c04_glyphmap'] - 1)
        self.play(self.opA.animate.set_value(.25), self.stand.animate.set_value(1), self.trav.animate.set_value(0),
                  FadeOut(cont[1]), run_time=1)
        self.remove(trav)

        # c = λf → c = 2df (MF-Tools: o "2d" sai de λ = 2d e entra no lugar de λ)
        A = tex(r'c = \lambda f', 48, TEXT_COLOR, 4, ((VIO, [0, 3]), (GEO, [2]))).move_to([-3.85, 1.0, 0], aligned_edge=LEFT).set_z_index(20)
        Bq = tex(r'c = 2df', 48, TEXT_COLOR, 5, ((VIO, [0, 4]), (GEO, [3]))).move_to([-3.85, 1.0, 0], aligned_edge=LEFT).set_z_index(20)
        self.play(FadeIn(A, shift=UP * .1), run_time=.8)
        self.play(Indicate(A[0][2], color=GEO), Indicate(L1b[0], color=GEO), run_time=1)
        self.wait(1.2)
        fonte = VGroup(L1b[2], L1b[3])

        class VemDe(ReplacementTransform):
            def __init__(self, mob, **kw):
                super().__init__(fonte.copy(), mob, **kw)
        self.play(TransformByGlyphMap(A, Bq, ([0], [0]), ([1], [1]), ([2], []), (VemDe, [2, 3]), ([3], [4])), run_time=1.6)
        self.assenta(Bq)

        # números
        self.ate(EV['c04_resultado'])
        N = tex(r'c = 2\,(0{,}061\ \text{m})\,(2{,}45\times10^{9}\ \text{Hz})', 44, TEXT_COLOR, 23,
                ((VIO, [0] + list(range(12, 22))), (GEO, list(range(4, 10))))).move_to([0, 1.25, 0]).set_z_index(20)
        if N.width > 8.2:
            N.scale_to_fit_width(8.2)
        self.play(FadeOut(VGroup(L1b, L2, etq)), Bq.animate.move_to([0, 2.15, 0]), run_time=.8)
        self.play(TransformByGlyphMap(Bq, N, ([0], [0]), ([1], [1]), ([2], [2]), ([3], list(range(3, 11))),
                                      ([4], list(range(11, 23))), from_copy=True), run_time=1.6)
        self.assenta(N)
        R = tex(r'c \approx 2{,}99\times10^{8}\ \text{m/s}', 56, VIO, 13, ((TEXT_COLOR, [1]),))
        rbox = RoundedRectangle(width=R.width + .6, height=R.height + .5, corner_radius=.14, stroke_color=VIO, stroke_width=3)
        rbox.set_fill(PANEL, 1)
        res = VGroup(rbox, R.move_to(rbox)).move_to([0, -3.0, 0]).set_z_index(22)
        luz = tx('a velocidade da luz', 26).move_to([0, -3.95, 0]).set_z_index(22)
        self.play(FadeIn(res, shift=DOWN * .15), run_time=1)
        self.play(FadeIn(luz), run_time=.6)
        self.ate(EV['c04_pulso'])
        self.play(res.animate.scale(1.06), rate_func=there_and_back, run_time=.8)
        self.c04_saida = VGroup(Bq, N, regua, d_lbl, ilus, luz)
        self.res = res

    # ------------------------------------------------------------------ C05
    def c05(self):
        self.ate(EV['c05'])
        novo = titulo('O forno é uma caixa')
        R2 = tex(r'c \approx 3\times10^{8}\ \text{m/s}', 40, VIO, 10, ((TEXT_COLOR, [1]),))
        b2 = RoundedRectangle(width=R2.width + .44, height=R2.height + .36, corner_radius=.12, stroke_color=VIO, stroke_width=2.5)
        b2.set_fill(PANEL, 1)
        est = tx('estimativa', 20, DIM)
        canto = VGroup(VGroup(b2, R2.move_to(b2)), est).arrange(RIGHT, buff=.25).move_to([0, 5.0, 0]).set_z_index(22)
        A_e_B = [self.A, self.inst, self.media, self.eixoB, self.rotB]
        for m in A_e_B:
            m.clear_updaters()
        self.play(FadeOut(self.tit), FadeIn(novo), FadeOut(self.c04_saida), FadeOut(VGroup(*A_e_B)), FadeOut(self.bar),
                  ReplacementTransform(self.res, canto), run_time=1.6)
        self.tit = novo
        self.ate(EV['c05_mapa'])
        img = ImageMobject(mapa_calor.mapa_rgba()).set_resampling_algorithm(RESAMPLING_ALGORITHMS['bilinear'])
        img.stretch_to_fit_width(MAP_W).stretch_to_fit_height(MAP_H).move_to(MAP_C).set_z_index(4)
        borda = Rectangle(width=MAP_W, height=MAP_H, stroke_color=STEEL, stroke_width=6).move_to(MAP_C).set_z_index(5)
        self.play(Create(borda), run_time=.8)
        self.play(FadeIn(img), run_time=1.5)
        self.ate(EV['c05_setas'])
        L = 3.3
        setas = VGroup(*[DoubleArrow(MAP_C - L * d, MAP_C + L * d, buff=0, stroke_width=3, color=CYAN, tip_length=.2)
                         for d in (RIGHT, UP * .92, normalize(np.array([1, .8, 0])))]).set_opacity(.4).set_z_index(8)
        self.play(LaggedStart(*[GrowFromCenter(s) for s in setas], lag_ratio=.3), run_time=1.5)
        self.wait(.8)
        self.play(FadeOut(setas), run_time=.7)
        self.ate(EV['c05_texto'])
        frase = tx('vários padrões se misturam', 24, DIM).move_to([0, -3.1, 0]).set_z_index(16)
        self.play(FadeIn(frase), run_time=.8)
        img.add_updater(lambda m, dt: m.set_opacity(.95 + .05 * np.sin(2 * PI * (self.T() - EV['c05_texto']) / 3)))
        self.img, self.borda, self.frase, self.canto = img, borda, frase, canto

    # ------------------------------------------------------------------ C06
    def c06(self):
        self.ate(EV['c06'])
        novo = titulo('Por que o prato gira')
        circ = Circle(R_PLATE, stroke_color=GEO, stroke_width=3).move_to(MAP_C).set_z_index(9)
        self.play(FadeOut(self.tit), FadeIn(novo), FadeOut(self.frase), run_time=.8)
        self.tit = novo
        self.play(Create(circ), run_time=1.2)
        self.ate(EV['c06_prato_ini'])
        t0, dur = EV['c06_prato_ini'], EV['c06_prato_fim'] - EV['c06_prato_ini']
        phi = lambda: 2 * PI * min(max(self.T() - t0, 0), dur) / dur
        prato = ImageMobject(mapa_calor.prato_rgba(0)).set_resampling_algorithm(RESAMPLING_ALGORITHMS['bilinear'])
        prato.set_width(2 * R_PLATE).move_to(MAP_C).set_z_index(6)
        prato.add_updater(lambda m, dt: setattr(m, 'pixel_array', mapa_calor.prato_rgba(phi())))
        marca = Dot(radius=.07, color=GEO).set_z_index(10)
        marca.add_updater(lambda m, dt: m.move_to(MAP_C + R_PLATE * np.array([np.cos(PI / 2 + phi()), np.sin(PI / 2 + phi()), 0])))
        self.img.clear_updaters()
        self.add(prato)
        self.play(self.img.animate.set_opacity(.3), FadeIn(marca), run_time=.6)
        self.ate(EV['c06_prato_fim'])
        prato.clear_updaters()
        prato.pixel_array = mapa_calor.prato_rgba(2 * PI)
        marca.clear_updaters()
        self.ate(EV['c06_centro'] + .05)
        centro = Dot(MAP_C, radius=.09, color=GEO).set_z_index(12)
        guia = DashedLine(MAP_C + DOWN * .15, [0, -2.85, 0], dash_length=.1).set_stroke(DIM, 1.8, .8).set_z_index(11)
        rot = tx('centro parado', 22, DIM).move_to([0, -3.15, 0]).set_z_index(16)
        self.play(GrowFromCenter(centro), run_time=.5)
        self.play(Create(guia), FadeIn(rot), run_time=.9)
        self.ate(EV['c06_anel'])
        anel = Annulus(inner_radius=5 * KM, outer_radius=7 * KM, stroke_color=HEAT, stroke_width=2,
                       fill_color=HEAT, fill_opacity=.35).move_to(MAP_C).set_z_index(9)
        self.play(FadeIn(anel, scale=.9), run_time=1)
        self.c06_saida = Group(prato, marca, circ, centro, guia, rot, anel, self.img, self.borda, self.canto, self.tit)

    # ------------------------------------------------------------------ C07
    def c07(self):
        self.ate(EV['c07_desafio'])
        self.play(FadeOut(self.c06_saida), run_time=1)
        des = tx('desafio', 48).move_to([0, 2.2, 0])
        f = tex(r'f = 915\ \text{MHz}', 64, VIO, 8, ((TEXT_COLOR, [1]),)).move_to([0, .9, 0])
        d = tex(r'd = \,?', 64, TEXT_COLOR, 3, ((GEO, [0]),)).move_to([0, -.4, 0])
        ideal = tx('no modelo ideal', 24, DIM).move_to([0, -1.45, 0])
        bloco = VGroup(des, f, d, ideal).set_z_index(20)
        self.play(FadeIn(des, shift=DOWN * .1), run_time=.6)
        self.play(FadeIn(f), run_time=.6)
        self.play(FadeIn(d), FadeIn(ideal), run_time=.6)
        self.ate(EV['endcard'])
        self.play(FadeOut(bloco), FadeOut(self.cab), run_time=.5)
        handle = screen_text('@labparallax', 48, oversample=2).set_z_index(40)
        handle.set_color_by_gradient(PRIMARY_COLOR, SECONDARY_COLOR, MAG)
        self.play(FadeIn(handle, scale=.96), run_time=.4)
        self.ate(TL['duracao_s'] - .45)
        self.play(FadeOut(handle), run_time=.4)
        self.ate(TL['duracao_s'])
