"""vid_0032 v4 — Dá para medir a luz com chocolate? Camada Manim (transparente) do preview silencioso, C01–C07.

O 3D (cena3d/, render3d.js) é o fundo no C01 (0–28 s) e no C05/C06 (127–170 s); fora disso um retângulo da cor de fundo
cobre tudo. No C01 a régua e a etiqueta seguem as projeções do 3D gravadas no timeline.json (projecao_3d), por isso o
render3d.js roda antes. Tudo que oscila é função do tempo absoluto (self.renderer.time). Tempos: timeline.json.
Geometria v2: forno de 36,6 cm = 3λ; 1 unidade = 4,357 cm; paredes em ±4,2; λ = 2,8 na tela.
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
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

config.media_dir = str(UNIT / os.environ.get('MIDIA', 'media_preview'))
config.background_color = BACKGROUND_COLOR
TL = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))
EV, G = TL['eventos'], TL['geometria']
PJ = TL.get('projecao_3d', {}).get('quadros', {})

CYAN, HEAT, GEO, VIO, STEEL, DIM = PRIMARY_COLOR, '#FF7A3D', '#B8C4DA', '#9C8CFF', '#7A8696', '#8FA3C4'
PANEL, BLUE_L, MAG = '#0E2A52', '#7FB2FF', '#EA63FF'
CHOC, CHOC_D, GROOVE = '#4A2C1E', '#6B4029', '#2E1A11'

# gráfico do C06 (unidades do Manim): x de GX0 a GX1 = uma volta; y de GB (calor 0) a GB + GH (calor 1)
GX0, GX1, GB, GH = -2.7, 2.5, -4.15, 1.05

# ---------- geometria (unidades do Manim) ----------
K = G['manim_por_cm']                       # 0,2295: 1 unidade = 4,357 cm
BAR_C = np.array([*G['centro_barra_manim'], 0.])
BAR_W, BAR_H = G['barra']['comprimento_cm'] * K, G['barra']['largura_cm'] * K     # 5,05 × 1,84
SPOTS = [x * K for x in G['manchas_x_cm']]  # −2,1; −0,7; 0,7; 2,1
LAM = 2.8                                   # λ na tela; paredes em ±4,2 = 3λ/2 de cada lado
KW = 2 * PI / LAM
XL, XR = -4.2, 4.2
XS = np.linspace(XL, XR, 241)
NOS = np.arange(XL, XR + .01, LAM / 2)      # 7 nós
PICOS = (NOS[:-1] + NOS[1:]) / 2            # 6 ventres: ±0,7; ±2,1; ±3,5
AMP_A, AMP_B = 0.9, 1.3

# ---------- fase do campo: ω visual por trechos (Hz), θ(t) = 2π ∫ f dt, exata para f linear por trecho ----------
FREQ = [(0, .5), (36, .5), (40, .8), (54, .8), (55.5, .4), (66, .4), (67.5, .8), (1e4, .8)]
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
W_MEAN = 2 * PI * .8                        # ω constante a partir de 67,5 s


def mean_sin2(t):
    """Média de sen²θ de T_MEAN até t (exata, ω constante)."""
    d = t - T_MEAN
    if d < 1e-3:
        return np.sin(theta(max(t, T_MEAN))) ** 2
    return .5 - (np.sin(2 * theta(t)) - np.sin(2 * theta(T_MEAN))) / (4 * W_MEAN * d)


def pico(t0, sinal):
    """Primeiro instante ≥ t0 em que sen θ = sinal (±1)."""
    ts = np.arange(t0, t0 + 4, .002)
    return float(ts[np.argmax(sinal * np.sin([theta(t) for t in ts]) > .9999)])


# ---------- C06: calor no pedaço M a cada ângulo do prato (mesma bilinear e mesmo trapézio de giro do cena3d.js) ----------
_CP = json.loads((UNIT / 'cena3d' / 'campo.json').read_text(encoding='utf-8'))
_NX, _NY, _CA, _CB = _CP['nx'], _CP['ny'], _CP['a_cm'], _CP['b_cm']
_IMED = (np.array(_CP['P']) + np.array(_CP['Q'])) / 2
GM = _CP['gotas_cm'][G['c06']['gota_m']]


def calor(x, y):
    fx = min(max((x + _CA / 2) / _CA * (_NX - 1), 0), _NX - 1.001)
    fy = min(max((y + _CB / 2) / _CB * (_NY - 1), 0), _NY - 1.001)
    i, j = int(fx), int(fy)
    a, b = fx - i, fy - j
    k = j * _NX + i
    return (_IMED[k] * (1 - a) + _IMED[k + 1] * a) * (1 - b) + (_IMED[k + _NX] * (1 - a) + _IMED[k + _NX + 1] * a) * b


def phi_c06(t):
    """Ângulo do prato: trapézio de velocidade, 0 → 2π de c06_giro_ini a c06_giro_fim."""
    a, T = EV['c06_acel'], EV['c06_giro_fim'] - EV['c06_giro_ini']
    v, u = 1 / (T - a), t - EV['c06_giro_ini']
    if u <= 0:
        return 0.
    if u >= T:
        return 2 * PI
    return 2 * PI * (v * u * u / (2 * a) if u < a else v * a / 2 + v * (u - a) if u < T - a else 1 - v * (T - u) ** 2 / (2 * a))


UT = np.linspace(0, 1, 721)
HM = np.array([calor(GM[0] * np.cos(2 * PI * u) - GM[1] * np.sin(2 * PI * u), GM[0] * np.sin(2 * PI * u) + GM[1] * np.cos(2 * PI * u)) for u in UT])
MEDIA_M = HM[:-1].mean()                    # média de M na volta (0,525)
I_CENTRO = calor(0, 0)                      # o centro não anda: calor constante

# ---------- 3D → Manim ----------
def pj(t):
    """Projeções do 3D no quadro mais próximo de t (15 fps), em unidades do Manim."""
    f = round(t * 15)
    q = next((PJ[str(f - k)] for k in range(8) if str(f - k) in PJ), None)
    if q is None:
        return None
    m = lambda p: np.array([p[0] / 540 * 9 - 4.5, 8 - p[1] / 960 * 16, 0])
    return {'manchas': [m(p) for p in q['manchas']], 'etiqueta': [m(p) for p in q['etiqueta']],
            'prato_centro': m(q['prato_centro']), 'M': m(q['M']) if 'M' in q else None, 'caixas': q['caixas']}


# ---------- texto e fórmulas ----------
_ALT = {}


def tx(s, size=24, color=TEXT_COLOR):
    """Texto de tela em maiúsculas, sempre numa linha só (o Pango quebrava com oversample 4)."""
    s = s.upper()
    m = screen_text(s, size, color=color, oversample=2)
    if size not in _ALT:
        _ALT[size] = screen_text('ÁÇ', size, oversample=2).height
    assert m.height <= 1.3 * _ALT[size], f'{s!r} quebrou linha'
    return m


def tex(s, size=48, color=TEXT_COLOR, n=None, cores=()):
    """MathTex de string única; cores = ((cor, [índices de glifo]), ...)."""
    m = MathTex(s, font_size=size, color=color)
    if n is not None:
        assert len(m[0]) == n, f'{s!r}: {len(m[0])} glifos (esperado {n})'
    for c, idx in cores:
        for i in idx:
            m[0][i].set_color(c)
    return m


def titulo(*partes, y=6.15):
    g = VGroup(*[tx(p, 34) if isinstance(p, str) else p for p in partes]).arrange(RIGHT, buff=.18)
    assert g.width < 8.4, partes
    return g.move_to([0, y, 0]).set_z_index(50)


def mancha(x, cor, alfa=.2, camadas=12, y=None):
    """Mancha de decaimento suave (σ = 0,75 cm): círculos concêntricos de opacidade baixa empilhados."""
    s = G['mancha_sigma_cm'] * K
    y = BAR_C[1] if y is None else y
    return VGroup(*[Circle(r, stroke_width=0).set_fill(cor, alfa).move_to([x, y, 0])
                    for r in np.linspace(2.4 * s, .25 * s, camadas)])


def barra_2d():
    corpo = Rectangle(width=BAR_W, height=BAR_H, stroke_width=0).set_fill(CHOC, 1).move_to(BAR_C)
    gx, gy = G['barra']['gomos']
    sulcos = VGroup(*[Line([BAR_C[0] - BAR_W / 2 + i * BAR_W / gx, BAR_C[1] - BAR_H / 2, 0],
                           [BAR_C[0] - BAR_W / 2 + i * BAR_W / gx, BAR_C[1] + BAR_H / 2, 0]) for i in range(1, gx)],
                    *[Line([BAR_C[0] - BAR_W / 2, BAR_C[1] - BAR_H / 2 + j * BAR_H / gy, 0],
                           [BAR_C[0] + BAR_W / 2, BAR_C[1] - BAR_H / 2 + j * BAR_H / gy, 0]) for j in range(1, gy)])
    sulcos.set_stroke(GROOVE, 2.2)
    manchas = VGroup(*[mancha(x, CHOC_D, alfa=.3) for x in SPOTS])
    return VGroup(corpo, sulcos, manchas).set_z_index(5)


def curva(ys, y0, cor, larg, op, xs=XS):
    return VMobject().set_points_as_corners(np.c_[xs, y0 + ys, 0 * xs]).set_stroke(cor, larg, op)


def desvio(dx, dy=0.):
    """path_func: cada ponto vai por uma Bézier quadrática empurrada de (dx, dy) no meio (2× no controle)."""
    d = np.array([dx, dy, 0.]) * 2

    def f(a, b, alpha):
        return (1 - alpha) ** 2 * a + 2 * alpha * (1 - alpha) * ((a + b) / 2 + d) + alpha ** 2 * b
    return f


def painel(m, op=.72, buff=.1):
    """Fundo escuro discreto atrás de um texto sobre o 3D (o rótulo fica dentro do próprio painel)."""
    p = SurroundingRectangle(m, buff=buff, corner_radius=.08, stroke_width=0).set_fill(BACKGROUND_COLOR, op)
    p.es_painel = True                       # o portão de sobreposição aceita rótulos dentro do próprio painel
    return VGroup(p, m)


def brace_h(x0, x1, y, para_baixo=True):
    a, b = ([x1, y, 0], [x0, y, 0]) if para_baixo else ([x0, y, 0], [x1, y, 0])
    return BraceBetweenPoints(a, b, direction=DOWN if para_baixo else UP, color=GEO)


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
        elif d < -.05:
            print(f'ATRASO: cheguei em {self.T():.2f} s para o evento de {t:.2f} s', file=sys.stderr)

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

    def copia(self, fonte, dur):
        """Portão de sobreposição (qa/auditar_sobreposicao.py): os glifos que saem por cópia de 'fonte' podem cruzar a
        própria fonte durante [agora, agora + dur]. É a exceção 'nasce do próprio rótulo'."""
        self.isentos.append((self.T(), self.T() + dur + .05, fonte))

    def troca_titulo(self, novo, *anims, rt=1.):
        """Título velho sai antes (0,3 s), o novo entra depois (0,4 s): nunca juntos."""
        self.play(Succession(FadeOut(self.tit, run_time=.3), Wait(.05), FadeIn(novo, run_time=.4)), *anims,
                  run_time=max(rt, .75))
        self.tit = novo

    def construct(self):
        # Tudo que depende do tempo precisa de um updater com dt (senão o wait vira quadro estático).
        self.add(Mobject().add_updater(lambda m, dt: None))
        self.isentos = []
        tag = screen_text('ABSURDO CALCULÁVEL · EP. 04', 20, oversample=2).set_opacity(.65)
        tag.to_corner(UP + LEFT, buff=.4).set_z_index(60)
        logo = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.35).to_corner(UP + RIGHT, buff=.28)
        self.cab = Group(tag, logo)
        self.add(tag, logo)
        # Estado das zonas A (onda) e B (calor): eixo, escala vertical, opacidade.
        self.yA, self.sA, self.opA = ValueTracker(4.2), ValueTracker(1), ValueTracker(0)
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
    def regua_3d(self, op, salta=True):
        """Régua presa às manchas do macro 3D. Nasce no par 1–2; com salta=True deixa cópia fantasma (40%) e salta para os
        pares 2–3 e 3–4 (a cada 1,1 s, com a mancha pulsando na chegada). O "6,1 cm" nasce em cada par ao chegar."""
        d61 = painel(tex(r'6{,}1\ \text{cm}', 40, GEO, 5))
        ilus = painel(tx('medida ilustrativa', 20, DIM))
        sk = [EV['c01_saltos'] + 1.1 * k for k in range(3)]
        sm = lambda u: u * u * (3 - 2 * u)

        def reg(a, b, alfa):
            u = (b - a) / np.linalg.norm(b - a)
            n = np.array([-u[1], u[0], 0])
            r = VGroup(Line(a, b).set_stroke(GEO, 3))
            for k in range(7):
                c = a + (b - a) * min(k, 6.1) / 6.1
                r.add(Line(c, c + n * (.16 if k in (0, 5) else .1)).set_stroke(GEO, 2))
            r.add(Line(b - n * .08, b + n * .18).set_stroke(GEO, 3), Line(a - n * .08, a + n * .18).set_stroke(GEO, 3))
            return r.set_opacity(alfa)

        def regua(t):
            p, o = pj(t), op.get_value()
            g = VGroup()
            if p is None or o < 1e-3:
                return g
            M = p['manchas']
            pos = sum(sm(min(max((t - sk[k]) / .5, 0), 1)) for k in (1, 2)) if salta else 0.
            j0 = min(int(pos), 2)
            f = pos - j0
            a, b = M[j0] * (1 - f) + M[min(j0 + 1, 3)] * f, M[j0 + 1] * (1 - f) + M[min(j0 + 2, 3)] * f
            for j in range(2):
                if pos > j + 1e-3:
                    g.add(reg(M[j], M[j + 1], .4 * o))
            g.add(reg(a, b, o))
            cx = p['caixas']
            topo = max(cx['barra'][3], cx['prato'][3])
            for j in range(3 if salta else 1):
                vis = sm(min(max((t - (EV['c01_regua'] if j == 0 else sk[j] + .4)) / .3, 0), 1)) if j else 1.
                al = o * vis * (1 - .6 * min(max(pos - j, 0), 1))
                if al < 1e-3:
                    continue
                lab = d61.copy().move_to([(M[j][0] + M[j + 1][0]) / 2, topo + .14 + d61.height / 2, 0])
                lab[1].set_opacity(al)
                lab[0].set_fill(opacity=.72 * al)
                g.add(lab)
            for k in range(3 if salta else 0):
                u = (t - sk[k] - .5) / .5
                if 0 < u < 1:
                    for i in (k, k + 1):
                        g.add(Circle(.3, stroke_color=GEO, stroke_width=3, fill_opacity=0).move_to(M[i]).set_stroke(opacity=o * np.sin(PI * u)))
            il = ilus.copy().move_to([0, min(cx['barra'][1], cx['prato'][1]) - .14 - ilus.height / 2, 0])
            il[1].set_opacity(o)
            il[0].set_fill(opacity=.72 * o)
            g.add(il)
            return g
        return self.live(regua, 20)

    def manchete(self):
        l1 = tx('Essas manchas medem', 38)
        l2 = VGroup(tx('a', 38), tx('velocidade da luz', 38, VIO)).arrange(RIGHT, buff=.2)
        return painel(VGroup(l1, l2).arrange(DOWN, buff=.22), buff=.2).move_to([0, 5.95, 0]).set_z_index(50)

    def c01(self):
        op = ValueTracker(0)
        rg = self.regua_3d(op)
        self.add(rg)
        head = self.manchete()
        self.ate(EV['c01_regua'])
        self.play(op.animate.set_value(1), run_time=.5)
        self.ate(EV['c01_manchete'])
        self.play(FadeIn(head, shift=DOWN * .1), run_time=.6)
        self.ate(EV['c01_manchete_fim'])                     # a régua salta de par em par enquanto isso (c01_saltos)
        self.play(FadeOut(head), run_time=.4)
        self.ate(EV['c01_rebobina'])
        self.play(op.animate.set_value(0), run_time=.4)
        self.remove(rg)
        # etiqueta: realce GEO preso aos cantos projetados (pulso de contorno) e "2450 MHz" em violeta logo abaixo
        opE = ValueTracker(0)
        mhz = tex(r'2450\ \text{MHz}', 44, VIO, 7)

        def etq(t):
            p = pj(t)
            if p is None or opE.get_value() < 1e-3:
                return VGroup()
            q = p['etiqueta']
            u = t - EV['c01_etiqueta_pulso']
            lw = 3 + 5 * np.sin(PI * u / .8) if 0 <= u <= .8 else 3
            poly = Polygon(*q).set_stroke(GEO, lw, opE.get_value()).set_fill(opacity=0)
            ys = [v[1] for v in q]
            pn = painel(mhz.copy()).move_to([np.mean([v[0] for v in q]), min(ys) - .3 - mhz.height / 2, 0])
            pn[1].set_opacity(opE.get_value())
            pn[0].set_fill(opacity=.72 * opE.get_value())
            return VGroup(poly, pn)
        et = self.live(etq, 20)
        self.add(et)
        self.ate(EV['c01_etiqueta'])
        self.play(opE.animate.set_value(1), run_time=.3)
        self.ate(EV['c01_etiqueta_fim'] - .4)
        self.play(opE.animate.set_value(0), run_time=.4)
        self.remove(et)
        sub = painel(tx('prato parado', 28, DIM)).move_to([0, 6.15, 0]).set_z_index(50)
        self.ate(EV['c01_prato_parado'])
        self.play(FadeIn(sub), run_time=.6)
        self.ate(EV['c01_prato_parado_fim'])
        self.play(FadeOut(sub), run_time=.4)
        # roteiro em 3 chips (um por passo), sobre o 3D
        chips = []
        for txt, cor_ in (('1 a onda', CYAN), ('2 o calor', HEAT), ('3 a conta', VIO)):
            m = tx(txt, 26, cor_)
            box = SurroundingRectangle(m, buff=.16, corner_radius=.1, stroke_color=cor_, stroke_width=2).set_fill(BACKGROUND_COLOR, .78)
            chips.append(VGroup(box, m).set_z_index(50))
        row = VGroup(*chips).arrange(RIGHT, buff=.22).move_to([0, 5.2, 0])
        tag, logo = self.cab
        print(f'FOLGA chips x cabeçalho {tag.get_bottom()[1] - row.get_top()[1]:.2f}; x logo {logo.get_bottom()[1] - row.get_top()[1]:.2f}', file=sys.stderr)
        for k, ev in enumerate(('c01_chip1', 'c01_chip2', 'c01_chip3')):
            self.ate(EV[ev])
            self.play(FadeIn(chips[k], shift=UP * .1), run_time=.4)
        self.ate(EV['c01_camera_topo'])
        self.fundo = Rectangle(width=9.4, height=16.4, stroke_width=0).set_fill(BACKGROUND_COLOR, 1).set_z_index(-100)
        self.bar = barra_2d()
        self.play(FadeIn(self.fundo), FadeIn(self.bar), FadeOut(row), run_time=EV['c01_troca_fim'] - EV['c01_camera_topo'])

    # ------------------------------------------------------------------ C02
    def zona_a(self):
        """Paredes, eixo, ondas que vão e voltam (C02, com setas presas às frentes) e estacionária; lido dos trackers."""
        v = (XR - XL) / 2.6

        def f(t):
            y0, s, op = self.yA.get_value(), self.sA.get_value(), self.opA.get_value()
            th = theta(t)
            g = VGroup()
            if op < 1e-3:
                return g
            for x in (XL, XR):
                g.add(Rectangle(width=.14, height=2.2 * s, stroke_width=0).set_fill(STEEL, op).move_to([x, y0, 0]))
            g.add(Line([XL, y0, 0], [XR, y0, 0]).set_stroke(DIM, 1.5, .5 * op))
            a, w = AMP_A * s / 2, self.vai.get_value()
            if w > 1e-3 and t >= EV['c02_viaja']:
                xf = min(XR, XL + v * (t - EV['c02_viaja']))
                xi = XS[XS <= xf + 1e-9]
                if len(xi) > 1:
                    g.add(curva(a * np.cos(th - KW * xi), y0, CYAN, 5, op * w, xi))
                if xf < XR - .05 and xf > XL + .9:
                    g.add(Arrow([xf - .9, 5.5, 0], [xf, 5.5, 0], buff=0, stroke_width=4, color=CYAN,
                                max_tip_length_to_length_ratio=.3).set_opacity(op * w))
                t_ref = EV['c02_viaja'] + 2.6
                if t >= t_ref:
                    xr = max(XL, XR - v * (t - t_ref))
                    xj = XS[XS >= xr - 1e-9]
                    if len(xj) > 1:
                        g.add(DashedVMobject(curva(-a * np.cos(th + KW * xj), y0, CYAN, 5, .8 * op * w, xj),
                                             num_dashes=max(2, int(len(xj) / 5)), dashed_ratio=.6))
                    if XL + .05 < xr < XR - .9:
                        g.add(Arrow([xr + .9, 5.5, 0], [xr, 5.5, 0], buff=0, stroke_width=4, color=CYAN,
                                    max_tip_length_to_length_ratio=.3).set_opacity(.8 * op * w))
            ws = self.stand.get_value()
            if ws > 1e-3:
                g.add(curva(AMP_A * s * np.sin(KW * XS) * np.sin(th), y0, CYAN, 6, op * ws))
            return g
        return self.live(f, 10)

    def c02(self):
        self.ate(EV['c02'])
        self.tit = titulo('A onda bate e volta')
        self.A = self.zona_a()
        self.add(self.A)
        self.play(FadeIn(self.tit), self.opA.animate.set_value(1), run_time=.4)
        self.ate(EV['c02_estacionaria'])
        self.play(self.stand.animate.set_value(1), self.vai.animate.set_value(0), run_time=4.5, rate_func=smooth)
        self.ate(EV['c02_parada'])
        self.troca_titulo(titulo('Onda parada'))
        self.ate(EV['c02_nos'])
        y0 = self.yA.get_value()
        self.nos = VGroup(*[Dot([x, y0, 0], radius=.07, color=GEO) for x in NOS]).set_z_index(14)
        self.no_lbl = tx('nó', 22, GEO).move_to([NOS[2], 2.92, 0]).set_z_index(14)
        topo_lbl = self.no_lbl.get_top()[1] + .06
        self.no_guia = Line([NOS[2], topo_lbl, 0], [NOS[2], y0 - AMP_A - .15 - .1, 0]).set_stroke(DIM, 1.8).set_z_index(13)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in self.nos], lag_ratio=.15), run_time=1.4)
        self.play(FadeIn(self.no_lbl), Create(self.no_guia), run_time=.6)
        self.ate(EV['c02_ventres'])
        setas = []
        for x in PICOS:
            setas += [Arrow([x, y0, 0], [x, y0 + AMP_A, 0], buff=0, stroke_width=2.5, color=CYAN, tip_length=.16,
                            max_tip_length_to_length_ratio=.25),
                      Arrow([x, y0, 0], [x, y0 - AMP_A, 0], buff=0, stroke_width=2.5, color=CYAN, tip_length=.16,
                            max_tip_length_to_length_ratio=.25)]
        self.ventres = VGroup(*setas).set_z_index(13)
        self.ventre_lbl = tx('ventre', 22, CYAN).move_to([PICOS[4], 5.55, 0]).set_z_index(14)
        self.play(LaggedStart(*[GrowArrow(a) for a in setas], lag_ratio=.06), run_time=1.6)
        self.play(FadeIn(self.ventre_lbl), run_time=.5)

    # ------------------------------------------------------------------ C03
    def c03(self):
        self.ate(EV['c03'])
        y0 = self.yA.get_value()
        self.troca_titulo(titulo('O calor vai com', tex('E^2', 48, HEAT, 2)),
                          FadeOut(self.ventres), FadeOut(self.ventre_lbl), FadeOut(self.no_lbl), FadeOut(self.no_guia),
                          self.opA.animate.set_value(.3), self.nos.animate.set_opacity(.3), rt=1)
        # 3a — ventre de perto: seta E em x = 0,7, rótulo E preso à ponta, sempre do lado de fora da onda
        xv = PICOS[3]
        seg = XS[(XS >= xv - LAM / 4) & (XS <= xv + LAM / 4)]
        realce = self.live(lambda t: curva(AMP_A * np.sin(KW * seg) * np.sin(theta(t)), y0, CYAN, 6, 1, seg), 11)
        e_lbl = tex('E', 36, CYAN, 1)
        self.e_pos = lambda t: np.array([xv + .25 + e_lbl.width / 2, y0 + AMP_A * np.sin(theta(t)) + np.sign(np.sin(theta(t))) * (.12 + e_lbl.height / 2), 0])

        def seta(t):
            s = np.sin(theta(t))
            g = VGroup()
            if abs(s) > .08:
                g.add(Arrow([xv, y0, 0], [xv, y0 + AMP_A * s, 0], buff=0, stroke_width=5, color=CYAN, tip_length=.18,
                            max_tip_length_to_length_ratio=.45))
            g.add(e_lbl.copy().move_to(self.e_pos(t)).set_opacity(np.clip((abs(s) - .12) / .2, 0, 1)))
            return g
        vetor = self.live(seta, 15)
        self.ate(EV['c03_seta'])
        self.play(FadeIn(realce), FadeIn(vetor), run_time=.8)
        # medidor E² (zona B) e MF1: o E da seta vira o E² do medidor
        self.ate(EV['c03_medidor'])
        yb = self.yB.get_value()
        eixoB = Line([XL, yb, 0], [XR, yb, 0]).set_stroke(DIM, 1.5, .5).set_z_index(10)
        caixa = Rectangle(width=.35, height=AMP_B, stroke_color=HEAT, stroke_width=2).move_to([xv, yb + AMP_B / 2, 0]).set_z_index(12)
        fill = self.live(lambda t: Rectangle(width=.35, height=max(AMP_B * np.sin(theta(t)) ** 2, 1e-3), stroke_width=0)
                         .set_fill(HEAT, .9).move_to([xv, yb, 0], aligned_edge=DOWN), 12)
        t_up = pico(self.T() + 1.1, 1)
        self.play(Create(eixoB), FadeIn(caixa), FadeIn(fill), run_time=.8)
        self.ate(t_up - .5)
        e_fonte = e_lbl.copy().move_to(self.e_pos(self.T() + .0))
        e2 = tex('E^2', 40, HEAT, 2).move_to([xv + .55, yb + AMP_B / 2, 0]).set_z_index(12)
        e2[0][0].set_color(HEAT)
        self.copia(vetor, 1.0)
        self.play(TransformByGlyphMap(e_fonte, e2, ([0], [0]), (FadeIn, [1]), from_copy=True), run_time=1.0)
        self.assenta(e2)
        # MF2: (+E)² → E² com a seta para cima; (−E)² → E² com a seta para baixo
        mf = []
        for k, (sinal, y) in enumerate(((1, 2.3), (-1, 1.6))):
            tp = pico(max(self.T() + .9, EV['c03_mf2'] if k == 0 else self.T() + .5), sinal)
            a = tex(r'(+E)^2' if sinal > 0 else r'(-E)^2', 44, TEXT_COLOR, 5, ((CYAN, [1, 2]), (HEAT, [4])))
            a.move_to([-4.0, y, 0], aligned_edge=LEFT).set_z_index(20)
            b = tex('E^2', 44, HEAT, 2).move_to(a[0][2], aligned_edge=LEFT).set_z_index(20)
            self.ate(tp - .7)
            self.play(FadeIn(a), run_time=.4)
            self.wait(.3)
            self.play(TransformByGlyphMap(a, b, ([0], []), ([1], []), ([2], [0]), ([3], []), ([4], [1])), run_time=.9)
            self.assenta(b)
            mf.append(b)
        self.ate(EV['c03_instantanea'] - .5)
        self.play(FadeOut(VGroup(*mf)), FadeOut(e2), run_time=.4)

        # 3b — a linha toda: instantânea pulsando e média que converge
        self.ate(EV['c03_instantanea'])
        self.remove(realce)
        self.play(FadeOut(vetor), self.opA.animate.set_value(1), self.nos.animate.set_opacity(1), run_time=.6)
        inst_f = lambda t: curva(AMP_B * self.sB.get_value() * np.sin(KW * XS) ** 2 * np.sin(theta(t)) ** 2,
                                 self.yB.get_value(), HEAT, 2.5, .6 * self.opB.get_value())
        inst = self.live(inst_f, 11)
        onda = curva(AMP_A * np.sin(KW * XS) * np.sin(theta(self.T())), y0, CYAN, 6, 1)
        alvo = inst_f(self.T() + .4).set_z_index(11)
        self.play(TransformFromCopy(onda, alvo), run_time=.4)
        self.remove(alvo)
        self.add(inst)
        self.ate(EV['c03_media'])
        self.media_f = lambda t: curva(AMP_B * self.sB.get_value() * np.sin(KW * XS) ** 2 * mean_sin2(t),
                                       self.yB.get_value(), HEAT, 6, self.opB.get_value())
        media = self.live(self.media_f, 12)
        self.add(media)
        self.ate(EV['c03_medidor_pico'])
        corc = XS[(XS >= xv - LAM / 4) & (XS <= xv + LAM / 4)]
        hump = curva(AMP_B * np.sin(KW * corc) ** 2 * mean_sin2(self.T() + 1.2), yb, HEAT, 6, 1, corc).set_z_index(13)
        rot2 = tex(r'\langle E^2 \rangle', 36, HEAT, 4).move_to([3.8, 2.93, 0]).set_z_index(12)
        self.remove(fill)
        cheio = Rectangle(width=.35, height=AMP_B * np.sin(theta(self.T())) ** 2 + 1e-3, stroke_width=0).set_fill(HEAT, .9)
        cheio.move_to([xv, yb, 0], aligned_edge=DOWN)
        self.play(ReplacementTransform(cheio, hump), FadeOut(caixa), FadeIn(rot2), run_time=1.2)
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
        bA = brace_h(NOS[0], NOS[2], 3.1)
        lA = tex(r'\lambda', 40, GEO, 1).next_to(bA, DOWN, buff=.05)
        bB = brace_h(PICOS[0], PICOS[1], 1.02)
        lB = tex(r'\lambda/2', 40, GEO, 3).next_to(bB, DOWN, buff=.05)
        VGroup(bA, lA, bB, lB).set_z_index(16)
        self.play(GrowFromCenter(bA), FadeIn(lA), run_time=.8)
        self.play(GrowFromCenter(bB), FadeIn(lB), run_time=.8)

        # 3d — as manchas nascem dos picos (a chave λ/2 sai antes das guias nascerem)
        self.ate(EV['c03_manchas'])
        self.play(FadeOut(VGroup(bB, lB)), run_time=.4)
        topo = yb + AMP_B * mean_sin2(self.T() + 1)
        guias = VGroup(*[DashedLine([x, topo, 0], [x, BAR_C[1], 0], dash_length=.12).set_stroke(DIM, 2, .8) for x in PICOS]).set_z_index(6)
        fora = VGroup(*[Circle(.09, stroke_color=DIM, stroke_width=2).move_to([x, BAR_C[1], 0]) for x in (PICOS[0], PICOS[-1])]).set_z_index(6)
        brilho = VGroup(*[mancha(x, HEAT, alfa=0) for x in SPOTS]).set_z_index(7)
        frase = VGroup(tx('uma mancha a cada', 26), tex(r'\lambda/2', 44, GEO, 3)).arrange(RIGHT, buff=.16)
        frase.move_to([0, -2.9, 0]).set_z_index(16)
        self.play(LaggedStart(*[Create(g) for g in guias], lag_ratio=.12), run_time=1.2)
        self.play(*[c.animate.set_fill(HEAT, .22) for b in brilho for c in b], FadeIn(fora), FadeIn(frase), run_time=.8)
        self.play(*[c.animate.set_fill(HEAT, 0) for b in brilho for c in b], run_time=1.2)
        self.remove(brilho)
        self.c03_saida = VGroup(bA, lA, guias, fora, frase)

    # ------------------------------------------------------------------ C04
    def c04(self):
        self.ate(EV['c04'])
        A_alto, A_s = 5.0, .5 / AMP_A
        self.troca_titulo(titulo('A conta'), FadeOut(self.c03_saida), FadeOut(self.rotB), self.nos.animate.set_opacity(0),
                          self.yA.animate.set_value(A_alto), self.sA.animate.set_value(A_s), self.opA.animate.set_value(.25),
                          self.opB.animate.set_value(0), rt=1.2)
        for m in (self.inst, self.media, self.eixoB):
            m.clear_updaters()
        self.remove(self.nos, self.inst, self.media, self.eixoB)
        # régua de centro a centro das manchas do meio, logo acima da barra
        yr = .15
        x0, x1 = SPOTS[1], SPOTS[2]
        regua = VGroup(Line([x0, yr, 0], [x1, yr, 0]).set_stroke(GEO, 3))
        for cm in range(7):
            x = x0 + min(cm, 6.1) * K
            regua.add(Line([x, yr, 0], [x, yr + (.14 if cm % 5 == 0 else .09), 0]).set_stroke(GEO, 2))
        regua.add(Line([x1, yr - .06, 0], [x1, yr + .16, 0]).set_stroke(GEO, 3), Line([x0, yr - .06, 0], [x0, yr + .16, 0]).set_stroke(GEO, 3))
        d_lbl = tex(r'd = 6{,}1\ \text{cm}', 36, GEO, 7, ((TEXT_COLOR, [1]),)).move_to([0, .47, 0])
        ilus = tx('medida ilustrativa', 18, DIM).move_to([0, -2.2, 0])
        VGroup(regua, d_lbl, ilus).set_z_index(16)
        self.ate(EV['c04_regua'])
        self.play(Create(regua), run_time=1)
        self.play(FadeIn(d_lbl), FadeIn(ilus), run_time=.7)

        # L1: d = λ/2 → λ = 2d → λ = 2d = 12,2 cm (MF3)
        self.ate(EV['c04_d_lambda'])
        Y = [3.65, 2.8, 1.95, 1.1]
        L1a = tex(r'd = \frac{\lambda}{2}', 48, TEXT_COLOR, 5, ((GEO, [0, 2]),)).move_to([0, Y[0], 0]).set_z_index(20)
        L1b = tex(r'\lambda = 2d', 48, TEXT_COLOR, 4, ((GEO, [0, 3]),)).move_to([0, Y[0], 0]).set_z_index(20)
        L1 = tex(r'\lambda = 2d = 12{,}2\ \text{cm}', 48, TEXT_COLOR, 11, ((GEO, [0, 3, 5, 6, 7, 8, 9, 10]),)).move_to([0, Y[0], 0]).set_z_index(20)
        self.copia(d_lbl, 1)
        self.play(TransformFromCopy(d_lbl[0][0], L1a[0][0]), FadeIn(VGroup(*L1a[0][1:])), run_time=1)
        self.assenta(L1a)
        self.wait(.6)
        self.play(TransformByGlyphMap(L1a, L1b, ([0], [3]), ([1], [1]), ([2], [0]), ([3], []), ([4], [2])), run_time=1.4)
        self.assenta(L1b)
        self.wait(.4)
        L1h = tex(r'\lambda = 2d', 48, TEXT_COLOR, 4, ((GEO, [0, 3]),)).set_z_index(20)
        L1h.shift(L1[0][0].get_center() - L1h[0][0].get_center())
        self.play(TransformByGlyphMap(L1b, L1h, ([0], [0]), ([1], [1]), ([2], [2]), ([3], [3])), run_time=.5)
        self.assenta(L1h)
        self.wait(.2)                                       # λ = 2d assenta antes de o "= 12,2 cm" entrar
        self.remove(L1h)
        L1[0][4:].set_opacity(0)
        self.add(L1)
        self.play(L1[0][4:].animate.set_opacity(1), run_time=.5)

        # etiqueta do forno, abaixo da barra à direita; MF4 sobe o "2450 MHz" para a L2
        self.ate(EV['c04_etiqueta'])
        etq_box = RoundedRectangle(width=2.0, height=.9, corner_radius=.1, stroke_color=BLUE_L, stroke_width=2).set_fill(PANEL, 1)
        etq_box.move_to([2.6, -2.75, 0])
        etq_box.es_painel = True
        etq_t = tx('frequência', 15).move_to(etq_box.get_center() + UP * .22)
        etq_f = tex(r'2450\ \text{MHz}', 32, VIO, 7).move_to(etq_box.get_center() + DOWN * .13)
        etq = VGroup(etq_box, etq_t, etq_f).set_z_index(18)
        self.play(FadeIn(etq, shift=LEFT * .15), run_time=.7)
        self.wait(1)
        L2a = tex(r'f = 2450\times10^{6}\ \text{Hz}', 48, VIO, 12, ((TEXT_COLOR, [1]),)).move_to([0, Y[1], 0]).set_z_index(20)
        L2 = tex(r'f = 2{,}45\times10^{9}\ \text{Hz}', 48, VIO, 12, ((TEXT_COLOR, [1]),)).move_to([0, Y[1], 0]).set_z_index(20)
        src = etq_f.copy().set_z_index(19)
        etq_f.set_opacity(.3)                               # o original apaga a 30% no mesmo quadro em que a cópia nasce
        self.add(src)
        self.copia(VGroup(src, etq_f), 1.6)
        self.play(L1.animate.set_opacity(.4),
                  TransformByGlyphMap(src, L2a, ([0, 1, 2, 3], [2, 3, 4, 5]), ([4], [6, 7, 8, 9]), ([5, 6], [10, 11]),
                                      (FadeIn, [0, 1]), default_transformer_kwargs={'path_func': desvio(2.4, -.4)}),
                  run_time=1.6)
        self.assenta(L2a)
        self.wait(.5)
        self.play(TransformByGlyphMap(L2a, L2, ([0, 1, 2], [0, 1, 2]), (FadeIn, [3]), ([3, 4], [4, 5]), ([5], []),
                                      ([6, 7, 8], [6, 7, 8]), ([9], [9]), ([10, 11], [10, 11])), run_time=1.4)
        self.assenta(L2)
        self.play(FadeOut(etq), run_time=.5)

        # por que v = λ·f: a onda volta a 100% e viaja; a crista anda um λ por oscilação (L1 e L2 saem e voltam)
        self.ate(EV['c04_viajante'])
        T0, P = EV['c04_viajante'] + 1.2, 3.0
        self.trav = ValueTracker(0)

        def viaja(t):
            y, a, op = self.yA.get_value(), AMP_A * .8, self.trav.get_value()
            u = max(0., min(t, T0 + 2 * P) - T0) / P
            xc = XL + LAM * u
            return VGroup(curva(a * np.cos(2 * PI * u - KW * (XS - XL)), y, CYAN, 6, op),
                          Dot([xc, y + a, 0], radius=.09, color=WHITE).set_opacity(op))
        trav = self.live(viaja, 14)
        self.add(trav)
        self.play(FadeOut(L1), FadeOut(L2), run_time=.4)
        self.play(self.yA.animate.set_value(4.2), self.sA.animate.set_value(1), self.opA.animate.set_value(1),
                  self.stand.animate.set_value(0), self.trav.animate.set_value(1), run_time=.8)
        cont = [tx('1 oscilação', 20, DIM), tx('2 oscilações', 20, DIM)]
        a = AMP_A * .8
        crista = lambda t: np.array([XL + LAM * max(0., min(t, T0 + 2 * P) - T0) / P, 4.2 + a + .35 + cont[0].height / 2, 0])
        for k in range(2):
            yb_ = 4.2 - a - .15 - .05
            b = brace_h(XL + LAM * k, XL + LAM * (k + 1), yb_)
            lb = tex(r'\lambda', 40, GEO, 1).next_to(b, DOWN, buff=.05)
            ch = VGroup(b, lb).set_z_index(16)
            self.ate(T0 + P * k + .2)
            self.play(GrowFromCenter(b), run_time=.6)
            self.ate(T0 + P * (k + 1) - .3)
            rot = cont[k].copy().set_z_index(16)
            rot.add_updater(lambda m, dt: m.move_to(crista(self.T())))
            if k == 0:
                self.play(FadeIn(lb), FadeIn(rot), run_time=.3)
            else:
                self.play(FadeOut(rot_ant), run_time=.15)
                self.play(FadeIn(lb), FadeIn(rot), run_time=.25)
            rot_ant = rot
            self.wait(.5)
            self.play(FadeOut(ch), run_time=.3)
        self.wait(.4)
        self.play(FadeOut(rot_ant), run_time=.3)
        self.play(self.yA.animate.set_value(A_alto), self.sA.animate.set_value(A_s), self.opA.animate.set_value(.25),
                  self.stand.animate.set_value(1), self.trav.animate.set_value(0), run_time=.8)
        self.remove(trav)
        L1.set_opacity(.4)
        L2.set_opacity(1)
        self.play(FadeIn(L1), FadeIn(L2), run_time=.5)

        # L3: c = λf → c = 2df (MF6: o "2d" sai de λ = 2d por fora da linha do f)
        self.ate(EV['c04_c_lambda_f'])
        L3a = tex(r'c = \lambda f', 48, TEXT_COLOR, 4, ((VIO, [0, 3]), (GEO, [2]))).move_to([0, Y[2], 0]).set_z_index(20)
        L3 = tex(r'c = 2df', 48, TEXT_COLOR, 5, ((VIO, [0, 4]), (GEO, [3]))).move_to([0, Y[2], 0]).set_z_index(20)
        self.play(L2.animate.set_opacity(.4), FadeIn(L3a, shift=UP * .1), run_time=.7)
        self.play(L1.animate.set_opacity(1), Indicate(L3a[0][2], color=GEO), run_time=.8)
        self.wait(.6)
        fonte = VGroup(L1[0][2], L1[0][3])

        class VemDe(ReplacementTransform):
            def __init__(self, mob, **kw):
                super().__init__(fonte.copy(), mob, path_func=desvio(-3.4), **kw)
        self.copia(L1, 1.7)
        self.play(TransformByGlyphMap(L3a, L3, ([0], [0]), ([1], [1]), ([2], []), (VemDe, [2, 3]), ([3], [4])), run_time=1.6)
        self.assenta(L3)
        self.play(L1.animate.set_opacity(.4), run_time=.4)

        # L4: números. MF5 traz o 0,061 m da régua; c = 2 vem da L3; o 2,45×10⁹ Hz vem da L2 (por fora da L3)
        self.ate(EV['c04_numeros'])
        N = tex(r'c = 2\,(0{,}061\ \text{m})\,(2{,}45\times10^{9}\ \text{Hz})', 44, TEXT_COLOR, 23,
                ((VIO, [0] + list(range(12, 22))), (GEO, list(range(4, 10)))))
        if N.width > 8.2:
            N.scale_to_fit_width(8.2)
        N.move_to([0, Y[3], 0]).set_z_index(20)
        cm = tex(r'6{,}1\ \text{cm}', 36, GEO, 5)
        cm.move_to(VGroup(*d_lbl[0][2:]).get_center())
        m061 = tex(r'0{,}061\ \text{m}', 44, GEO, 6).match_height(VGroup(*N[0][4:10])).move_to(VGroup(*N[0][4:10]))
        self.copia(d_lbl, 1.3)
        self.play(L3.animate.set_opacity(1),
                  TransformByGlyphMap(cm, m061, ([0], [3]), ([1], [1]), ([2], [4]), ([3], []), ([4], [5]), (FadeIn, [0, 2])),
                  run_time=1.3)
        self.assenta(m061)
        self.wait(.3)
        self.copia(L3, 1.5)
        self.copia(m061, 1.5)
        self.copia(L2, 1.5)
        c2 = VGroup(*L3[0][:3]).copy()
        L3.set_opacity(.4)                                  # c = 2df esmaece antes do voo; a cópia sai com 100%
        self.add(c2)
        self.play(ReplacementTransform(c2, VGroup(*N[0][:3])),
                  FadeIn(VGroup(N[0][3], N[0][10], N[0][11], N[0][22])),
                  ReplacementTransform(m061[0], VGroup(*N[0][4:10])),
                  TransformFromCopy(VGroup(*L2[0][2:]), VGroup(*N[0][12:22]), path_func=desvio(4.0)),
                  run_time=1.5)
        self.assenta(N)
        self.play(FadeOut(L1), FadeOut(L2), FadeOut(L3), run_time=.5)
        # MF7: os números se juntam no resultado, na própria linha da conta; a caixa nasce ali
        self.ate(EV['c04_resultado'])
        R = tex(r'c \approx 2{,}99\times10^{8}\ \text{m/s}', 50, VIO, 13, ((TEXT_COLOR, [1]),)).move_to([0, 1.75, 0]).set_z_index(22)
        N2 = tex(r'c = 2\times0{,}061\times2{,}45\times10^{9}', 44, TEXT_COLOR, 18,
                 ((VIO, [0] + list(range(10, 18))), (GEO, list(range(4, 9))))).move_to([0, Y[3], 0]).set_z_index(20)
        # (1) os números se alinham: sem parênteses nem unidades, só 2 × 0,061 × 2,45×10⁹ (0,8 s, assenta 0,3 s)
        self.play(TransformByGlyphMap(N, N2, ([0], [0]), ([1], [1]), ([2], [2]), ([3], []), ([4, 5, 6, 7, 8], [4, 5, 6, 7, 8]), ([9], []),
                                      ([10], []), ([11], []), ([12, 13, 14, 15], [10, 11, 12, 13]), ([16], [14]), ([17, 18, 19], [15, 16, 17]),
                                      ([20, 21], []), ([22], []), (FadeIn, [3, 9])), run_time=.8)
        self.assenta(N2)
        self.wait(.3)
        # (2) viram o resultado, por caminhos curtos (mesma linha, só o expoente e as unidades mudam)
        self.play(TransformByGlyphMap(N2, R, ([0], [0]), ([1], [1]), ([2, 4, 5, 6, 7, 8, 10, 11, 12, 13], [2, 3, 4, 5]), ([3, 9], []),
                                      ([14], [6]), ([15, 16], [7, 8]), ([17], [9]), (FadeIn, [10, 11, 12])), run_time=1.1)
        self.assenta(R)
        rbox = SurroundingRectangle(R, buff=.16, corner_radius=.12, stroke_color=VIO, stroke_width=3).set_fill(PANEL, 1).set_z_index(21)
        luz = tx('a velocidade da luz', 26).move_to([0, -2.6, 0]).set_z_index(22)
        print(f'FOLGA resultado x d = 6,1 cm: {rbox.get_bottom()[1] - d_lbl.get_top()[1]:.2f}', file=sys.stderr)
        self.play(Create(rbox), run_time=.6)
        self.play(FadeIn(luz), run_time=.5)
        self.ate(EV['c04_pulso'])
        self.play(VGroup(rbox, R).animate.scale(1.06), rate_func=there_and_back, run_time=.8)
        self.c04_saida = VGroup(regua, d_lbl, ilus, luz, rbox, R)

    # ------------------------------------------------------------------ C05
    def c05(self):
        self.ate(EV['c05'])
        R2 = tex(r'c \approx 3\times10^{8}\ \text{m/s}', 40, VIO, 10, ((TEXT_COLOR, [1]),))
        b2 = SurroundingRectangle(R2, buff=.16, corner_radius=.12, stroke_color=VIO, stroke_width=2.5).set_fill(PANEL, 1)
        est = tx('estimativa', 20, DIM)
        self.chip = VGroup(VGroup(b2, R2), est).arrange(RIGHT, buff=.25).move_to([0, 5.0, 0]).set_z_index(22)
        self.A.clear_updaters()
        # o fundo sai e o 3D (forno aberto por cima) aparece; o resultado sai e o chip nasce novo
        # primeiro saem as contas (ainda sobre o fundo), depois o fundo sai e o 3D aparece
        self.play(FadeOut(self.c04_saida), FadeOut(self.A), FadeOut(self.tit), run_time=.4)
        novo = titulo('O forno é uma caixa')
        self.play(FadeOut(self.bar), FadeOut(self.fundo), run_time=.6)
        self.play(FadeIn(novo), run_time=.4)
        self.tit = novo
        self.play(FadeIn(self.chip), run_time=.5)
        self.ate(EV['c05_texto'])
        self.frase = tx('vários padrões se misturam', 24, DIM).move_to([0, -4.05, 0]).set_z_index(16)
        self.play(FadeIn(self.frase), run_time=.8)

    # ------------------------------------------------------------------ C06
    def grafico_m(self):
        """Gráfico do calor no pedaço M: curva traçada pelo ângulo do prato (mesma função do 3D); ponto na ponta."""
        self.opC = ValueTracker(1)

        def f(t):
            u, oc = phi_c06(t) / (2 * PI), self.opC.get_value()
            g = VGroup()
            if u < 1e-3 or oc < 1e-3:
                return g
            us = np.linspace(0, u, max(2, int(u * 200) + 1))
            pts = np.c_[GX0 + (GX1 - GX0) * us, GB + GH * np.interp(us, UT, HM), 0 * us]
            g.add(VMobject().set_points_as_corners(pts).set_stroke(HEAT, 4, oc))
            g.add(Dot(pts[-1], radius=.075, color=HEAT).set_opacity(oc if t < EV['c06_media'] + .5 else 0))
            return g
        return self.live(f, 15)

    def c06(self):
        self.ate(EV['c06'])
        self.troca_titulo(titulo('Por que o prato gira'), FadeOut(self.frase), FadeOut(self.chip), rt=.8)
        BY = -2.2                                            # faixa livre entre o forno e o gráfico (rótulos com fio ao ponto)

        def etiqueta(texto, xc, y_alvo, cor=DIM, tam=24):
            m = painel(tx(texto, tam, cor))
            m.move_to([xc, BY, 0]).set_z_index(30)
            fio = Line([xc, y_alvo, 0], [xc, BY + m.height / 2 + .04, 0]).set_stroke(GEO, 2, .85).set_z_index(29)
            return VGroup(fio, m)

        # pedaço M: o contorno GEO e o halo estão no 3D (vão com a gota); aqui só o rótulo
        pm = pj(EV['c06_m'] + .3)['M']
        r_m = etiqueta('este pedaço', pm[0], pm[1] - .42)
        self.ate(EV['c06_m'])
        self.play(FadeIn(r_m), run_time=.4)
        self.ate(EV['c06_giro_ini'] - .6)
        self.play(FadeOut(r_m), run_time=.4)

        # gráfico: eixos e títulos (estáticos) + curva ao vivo
        eixos = VGroup(Line([GX0, GB, 0], [GX1, GB, 0]).set_stroke(DIM, 2, .8), Line([GX0, GB, 0], [GX0, GB + GH + .12, 0]).set_stroke(DIM, 2, .8),
                       tx('calor no pedaço', 20, DIM).move_to([GX0, GB + GH + .42, 0], aligned_edge=LEFT),
                       tx('uma volta', 20, DIM).move_to([GX1 + .15, GB, 0], aligned_edge=LEFT)).set_z_index(14)
        curva_m = self.grafico_m()
        self.add(curva_m)
        self.ate(EV['c06_grafico'] - .4)
        self.play(FadeIn(eixos), run_time=.4)

        # fim da volta: linha da média (GEO tracejada) e a curva a 50%
        self.ate(EV['c06_media'])
        ym = GB + GH * MEDIA_M
        media = DashedLine([GX0, ym, 0], [GX1, ym, 0], dash_length=.12).set_stroke(GEO, 3).set_z_index(16)
        r_media = tex(r'\text{média}', 34, GEO).move_to([GX1 + .15, ym, 0], aligned_edge=LEFT).set_z_index(16)
        self.play(Create(media), self.opC.animate.set_value(.5), run_time=.8)
        self.play(FadeIn(r_media), run_time=.5)

        # o anel acende no 3D (as gotas do mesmo anel ganham o tom GEO e derretem juntas)
        self.ate(EV['c06_anel'])
        r_anel = etiqueta('mesma média = anel', 0, pm[1] - .42, TEXT_COLOR)
        r_anel[0].set_opacity(0)                             # sem fio: o anel inteiro acende no 3D
        self.play(FadeIn(r_anel), run_time=.5)
        self.ate(EV['c06_centro'] - .5)
        self.play(FadeOut(r_anel), run_time=.4)

        # centro: não anda, não tem média; a reta do gráfico fica na altura do calor que ele recebe
        self.ate(EV['c06_centro'])
        pc = pj(EV['c06_centro'])['prato_centro']
        anel = Circle(.2, stroke_color=GEO, stroke_width=3).move_to(pc).set_z_index(12)
        r_c = etiqueta('centro parado', pc[0], pc[1] - .3, TEXT_COLOR)
        yc_ = GB + GH * I_CENTRO
        reta = Line([GX0, yc_, 0], [GX1, yc_, 0]).set_stroke(HEAT, 4).set_z_index(15)
        r_sem = tx('sem média', 22, GEO).move_to([GX1 + .15, yc_, 0], aligned_edge=LEFT).set_z_index(16)
        self.play(Create(anel), FadeIn(r_c), FadeOut(curva_m), FadeOut(media), FadeOut(r_media), run_time=.6)
        self.remove(curva_m)
        self.play(Create(reta), FadeIn(r_sem), run_time=.8)
        self.c06_saida = VGroup(anel, r_c, reta, r_sem, eixos, self.tit)

    # ------------------------------------------------------------------ C07
    def c07(self):
        self.ate(EV['c07_desafio'])
        self.play(FadeOut(self.c06_saida), FadeIn(self.fundo), run_time=.5)     # o 3D acaba em 170 s, o fundo já cobre
        des = tx('desafio', 48).move_to([0, 2.2, 0])
        f = tex(r'f = 915\ \text{MHz}', 64, VIO, 8, ((TEXT_COLOR, [1]),)).move_to([0, .9, 0])
        d = tex(r'd = \,?', 64, TEXT_COLOR, 3, ((GEO, [0]),)).move_to([0, -.4, 0])
        ideal = tx('no modelo ideal', 24, DIM).move_to([0, -1.45, 0])
        self.play(FadeIn(des, shift=DOWN * .1), run_time=.6)
        self.play(FadeIn(f), run_time=.6)
        self.play(FadeIn(d), FadeIn(ideal), run_time=.6)
        # CTA na própria cena: só o @labparallax em degradê, até o último quadro
        handle = screen_text('@labparallax', 56, oversample=2).move_to([0, -2.7, 0]).set_z_index(40)
        handle.set_color_by_gradient(PRIMARY_COLOR, SECONDARY_COLOR, MAG)
        self.ate(EV['c07_cta'])
        self.play(FadeIn(handle, scale=.96), run_time=.4)
        self.ate(TL['duracao_s'])
