"""vid_0029 — Por que o campo não escapa do toroide? Camada Manim (transparente) do teste Three.js + Manim. v3.

O 3D (cena3d/, render3d.js) é o fundo; esta cena desenha só raciocínio, vetores, construções e álgebra por cima.
Tempos vêm de timeline.json. Círculo amperiano, seta de raio, setas de B/dℓ, marcadores ⊙/⊗, contador e cursor do
gráfico são funções do tempo absoluto (mesmas regras do cena3d.js), por isso ficam no mesmo quadro do 3D.
v3: elos símbolo ↔ desenho (kit.elo: pulso simultâneo e linha-guia na 1ª vez de cada par), faixa da legenda livre
(y de −4,67 a −6,0; nada abaixo de y = −4,5) e vista de cima reescalada.
Álgebra no padrão dos longos (kit.py, cópia do yt_0012): vetores em negrito, cor por termo, texto de tela em
MAIÚSCULAS e definições "símbolo: significado" em MathTex. Passagens algébricas com correspondência real:
TransformByGlyphMap com mapa explícito (índices em qa/glifos.py); sem correspondência (NI − NI → 0): FadeOut/FadeIn.
Render do preview (na raiz do repositório):
    uv run python -m manim -t -r 540,960 --fps 15 videos/vid_0029_campo_toroide/cena.py CampoToroide029
"""
from pathlib import Path
import json
import sys
import numpy as np
from manim import *
from MF_Tools import TransformByGlyphMap

ROOT = Path(__file__).resolve().parents[2]
UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(UNIT))
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text
from kit import E as _E, defn as _defn, elo, pulso, panel, txt, GREEN, MAG, GEO, DIM, PANEL, BLUE_L

config.media_dir = str(UNIT / 'media_preview')
config.background_color = BACKGROUND_COLOR
TL = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))

G = TL['geometria']
K = G['fator_3d_manim']
CENTER = np.array([*G['centro_topo_manim'], 0.])
R_IN, R_MID, R_OUT = (G['raio_maior'] - G['raio_menor']) * K, G['raio_maior'] * K, (G['raio_maior'] + G['raio_menor']) * K
N_TURNS, PHI0 = G['n_espiras'], G['phi0']
BEAT = {b['id']: b['inicio_s'] for b in TL['beats']}
EV = TL['eventos']
CD, CF, GIRO, ROLL = TL['contagem_dentro'], TL['contagem_fora'], TL['giro_setas'], TL['desenrola_circulo']
# Faixas: manchete no topo; vista de cima; álgebra de y = 0 a −4,5; legenda reservada abaixo (nada desenhado ali).
Y_TOP, Y_REF, Y_EQ, Y_SUP, Y_LOW = 7.0, -.75, -2.0, -3.35, -4.15
M_EQ, M_REF, M_CNT, M_RES, M_DEF = 56, 48, 52, 64, 40
B_GAIN = 1.4 * R_IN   # |B| desenhado = B_GAIN / r: setas no círculo, barra do cursor e curva do gráfico na mesma escala
R_ANG = -PI / 4       # direção da seta de raio (entre duas setas de B)
HALF = dict(default_remover_kwargs={'rate_func': lambda t: smooth(min(1., 2 * t))},
            default_introducer_kwargs={'rate_func': lambda t: smooth(max(0., 2 * t - 1))})
DARK_MAG = '#7A3A86'

# Cores desta unidade sobre o TOKCOL do kit: R e a são raios (GEO), N é número (branco).
COLORS = {'R': GEO, '{R}': GEO, '{a}': GEO, '{r}': GEO, '{n}': GEO, 'N': TEXT_COLOR, '{N}': TEXT_COLOR, '{I}': GREEN,
          r'2\pi r': GEO, r'2\pi R': GEO, r'd\ell': GEO, r'd\boldsymbol\ell': GEO}


def M(tex, *tok, size=M_EQ, y=Y_EQ, x=0):
    return _E(tex, *tok, size=size, colors=COLORS).move_to([x, y, 0]).set_z_index(40)


def D(tex, *tok, size=M_DEF, y=Y_SUP, x=0):
    m = _defn(tex, *tok, size=size, colors=COLORS)
    if m.width > 8.2:
        m.scale_to_fit_width(8.2)
    return m.move_to([x, y, 0]).set_z_index(40)


def T(s, size=24, color=TEXT_COLOR, y=0, x=0):
    m = txt(s, size, color)
    if m.width > 7.6:
        m.scale_to_fit_width(7.6)
    return m.move_to([x, y, 0]).set_z_index(40)


def chip(*parts, color=DIM, y=-1.0, x=0, size=21):
    """Rótulo curto: texto em MAIÚSCULAS e, se houver, símbolo em MathTex."""
    body = VGroup(*[T(p, size, color) if isinstance(p, str) else p for p in parts]).arrange(RIGHT, buff=.14)
    box = RoundedRectangle(width=body.width + .44, height=max(body.height, .3) + .3, corner_radius=.12,
                           stroke_color=color, stroke_width=1.6, stroke_opacity=.8,
                           fill_color=BACKGROUND_COLOR, fill_opacity=.6)
    return VGroup(box, body.move_to(box)).move_to([x, y, 0]).set_z_index(40)


def keyed(keys, t, field):
    """Interpolação entre chaves do timeline; mesma regra de chaves() no cena3d.js."""
    if t <= keys[0]['t']:
        return keys[0][field]
    for a, b in zip(keys, keys[1:]):
        if t <= b['t']:
            u = (t - a['t']) / max(b['t'] - a['t'], 1e-9)
            if b.get('ease') != 'linear':
                u = u * u * (3 - 2 * u)
            return a[field] + (b[field] - a[field]) * u
    return keys[-1][field]


def amp_at(t):
    return keyed(TL['amperiano'], t, 'r'), keyed(TL['amperiano'], t, 'alpha')


def t_k(k, cfg):
    """Instante em que a espira k acende na contagem (mesma fórmula do shader do cena3d.js)."""
    return cfg['inicio_s'] + cfg['dur_s'] * (k / (N_TURNS - 1)) ** cfg['expoente']


def spin(t):
    """Giro rígido do B03 (mesma regra do cena3d.js)."""
    return GIRO['omega_rad_s'] * (min(max(t, GIRO['inicio_s']), GIRO['fim_s']) - GIRO['inicio_s'])


def b_len(r):
    return B_GAIN / r if R_IN <= r <= R_OUT else 0.


def polar(r, phi):
    return CENTER + r * np.array([np.cos(phi), np.sin(phi), 0.])


def nearest_bottom(angles):
    """Ângulo da lista mais próximo de −π/2 (o lado do anel voltado para a álgebra)."""
    return min(angles, key=lambda a: abs((a + PI / 2 + PI) % TAU - PI))


def marker(p, kind, scale=1., glow=0.):
    """⊙ (corrente saindo da tela, +z) ou ⊗ (entrando, −z); verde de corrente, raio 0,11."""
    ring = Circle(radius=.11, stroke_color=GREEN, stroke_width=2.4,
                  fill_color=interpolate_color(ManimColor(BACKGROUND_COLOR), ManimColor(GREEN), .55 * glow), fill_opacity=.6)
    if kind == 'out':
        inner = Dot(radius=.036, color=GREEN)
    else:
        d = .072
        inner = VGroup(Line([-d, -d, 0], [d, d, 0]), Line([-d, d, 0], [d, -d, 0])).set_stroke(GREEN, 2.4)
    return VGroup(ring, inner).scale(scale).move_to(p).set_z_index(30)


def strike(group):
    return Line(group.get_corner(DL) + DL * .05, group.get_corner(UR) + UR * .05, color=TEXT_COLOR, stroke_width=3).set_z_index(45)


class CampoToroide029(Scene):
    def mark(self, name):
        self.events.append({'estado': name, 'segundos': round(self.time, 3)})

    def until(self, t):
        if self.time > t + .15:
            raise RuntimeError(f'Bloco excedeu {t}s: {self.time:.3f}s')
        if t - self.time > .02:
            self.wait(t - self.time)

    def glyph(self, source, target, maps, duration, name=None, extras=()):
        """TransformByGlyphMap com mapa explícito; devolve o alvo já limpo na cena."""
        if name:
            self.mark(name)
        anim = TransformByGlyphMap(source, target, *maps, auto_fade=True, auto_morph=False, printing=False, **HALF)
        assert not anim.show_indices
        self.play(anim, *extras, run_time=duration)
        self.remove(*source.get_family()); self.remove(*target.get_family()); self.add(target)
        return target

    def link(self, glifo, cor, gemeo=None, alvo=None, guia=True, name=None):
        """Um elo por vez (kit.elo), sempre num play próprio."""
        if name:
            self.mark(name)
        self.play(elo(glifo, cor, gemeo, alvo, guia))

    # ---------- pontos dos gêmeos no instante atual (fim da linha-guia) ----------
    def b_angles(self):
        return [TAU * j / 8 + PI / 8 + spin(self.time) for j in range(8)]

    def arrow_point(self, offset=.17):
        r = amp_at(self.time)[0]
        return polar(r + offset, nearest_bottom(self.b_angles()))

    def ring_point(self, kind):
        k_off = 0. if kind == 'out' else .5
        r = R_IN if kind == 'out' else R_OUT
        return polar(r, nearest_bottom([PHI0 + TAU * (k + k_off) / N_TURNS for k in range(N_TURNS)]))

    # ---------- objetos que dependem do tempo absoluto ----------
    def amperian(self):
        """Círculo amperiano (GEO tracejado, anti-horário) e disco; raio, opacidade e giro vêm do timeline."""
        r, alpha = amp_at(self.time)
        if alpha < .01 or r < .02:
            return VGroup()
        n = max(8, round(TAU * r / .22))  # mesma regra do cena3d.js
        rot, pc = spin(self.time), self.pc.get_value()
        dashes = DashedVMobject(Circle(radius=r, stroke_color=GEO, stroke_width=3 + 4 * pc), num_dashes=n, dashed_ratio=.5)
        dashes.move_to(CENTER).rotate(rot, about_point=CENTER).set_stroke(opacity=min(1., (.95 + .3 * pc) * alpha))
        disc = Circle(radius=r, stroke_width=0, fill_color=GEO,
                      fill_opacity=alpha * (.12 * self.disc.get_value() + .3 * self.pdisc.get_value())).move_to(CENTER)
        tips = VGroup()
        for ang in (PI / 4 + rot, 5 * PI / 4 + rot):
            tip = Triangle(fill_color=GEO, fill_opacity=alpha, stroke_width=0).scale(.1)
            tips.add(tip.rotate(ang).move_to(polar(r, ang)))
        return VGroup(disc, dashes, tips).set_z_index(20)

    def radius(self):
        """Seta de raio r (GEO) do centro até o círculo amperiano; acompanha o raio e o giro."""
        r, alpha = amp_at(self.time)
        a = alpha * self.rad.get_value()
        if a < .01 or r < .15:
            return VGroup()
        p, ang = self.pr.get_value(), R_ANG + spin(self.time)
        arrow = Arrow(CENTER, polar(r, ang), buff=0, color=interpolate_color(ManimColor(GEO), WHITE, .4 * p),
                      stroke_width=3 + 3 * p, max_tip_length_to_length_ratio=min(.25, .3 / r)).set_opacity(a)
        label = MathTex('r', font_size=40 * (1 + .3 * p), color=GEO).move_to(polar(r + .3, ang + .1)).set_opacity(a)
        return VGroup(arrow, label, Dot(CENTER, radius=.045, color=GEO).set_opacity(a)).set_z_index(26)

    def vectors(self):
        """8 setas B (magenta, logo fora do círculo) e 8 setas dℓ (GEO, sobre o círculo), tangentes e anti-horárias."""
        r, alpha = amp_at(self.time)
        if alpha < .01 or r < .02:
            return VGroup()
        size = self.bgain.get_value() * (b_len(r) if self.bphys.get_value() > .5 else b_len(R_MID))
        dim = alpha * (1 - .75 * self.blink.get_value())
        dl, pB, pdl = self.dl.get_value(), self.pB.get_value(), self.pdl.get_value()
        group = VGroup()
        for ang in self.b_angles():
            tan = np.array([-np.sin(ang), np.cos(ang), 0.])
            if size > .03:
                p = polar(r + .17, ang)
                group.add(Arrow(p - size / 2 * tan, p + size / 2 * tan, buff=0,
                                color=interpolate_color(ManimColor(MAG), WHITE, .35 * pB), stroke_width=min(5., 10 * size) * (1 + pB),
                                max_tip_length_to_length_ratio=.32, max_stroke_width_to_length_ratio=30).set_opacity(dim))
            if dl > .01:
                q = polar(r, ang)
                group.add(Arrow(q - .17 * tan, q + .17 * tan, buff=0, color=interpolate_color(ManimColor(GEO), WHITE, .4 * pdl),
                                stroke_width=3.5 * (1 + pdl), max_tip_length_to_length_ratio=.42).set_opacity(dl * dim))
        return group.set_z_index(25)

    def markers(self, kind, cfg):
        """⊙/⊗ aparecem um a um em t_k (pulo de escala de 0,15 s), em sincronia com o flash 3D da espira k."""
        if self.mk.get_value() < .01:
            return VGroup()
        glow = (self.pin if kind == 'out' else self.pout).get_value()
        group = VGroup()
        for k in range(N_TURNS):
            u = (self.time - t_k(k, cfg)) / .15
            if u <= 0:
                continue
            phi = PHI0 + TAU * (k + (0. if kind == 'out' else .5)) / N_TURNS
            m = marker(polar(R_IN if kind == 'out' else R_OUT, phi), kind,
                       scale=(1 + .5 * max(0., 1 - u)) * (1 + .35 * glow), glow=glow)
            group.add(m.set_opacity(self.mk.get_value()))
        return group

    def heading(self, content):
        new = T(content, 24, y=Y_TOP).set_opacity(.9) if content else VGroup()
        self.play(FadeOut(self.top), FadeIn(new), run_time=.6)
        self.top = new

    def construct(self):
        self.events = []
        for name in ('disc', 'bgain', 'blink', 'dl', 'rad', 'pB', 'pdl', 'pr', 'pc', 'pdisc', 'pin', 'pout', 'pcurve'):
            setattr(self, name, ValueTracker(0))
        self.bphys, self.mk = ValueTracker(1), ValueTracker(1)
        self.top = VGroup()
        # Tudo que depende do tempo absoluto precisa de um updater com dt: sem ele o Manim trata cada wait como
        # quadro estático e congela círculo, setas, marcadores e cursor.
        self.add(Mobject().add_updater(lambda m, dt: None))

        # Cabeçalho padrão dos curtos (tag da série à esquerda, marca à direita).
        tag = screen_text('POR TRÁS DA FÓRMULA · EP. 09', 20, oversample=2).set_opacity(.65)
        tag.to_corner(UP + LEFT, buff=.4).set_z_index(60)
        logo = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.35).to_corner(UP + RIGHT, buff=.28)
        self.add(tag, logo)
        amp, rad, vec = always_redraw(self.amperian), always_redraw(self.radius), always_redraw(self.vectors)
        self.add(amp, rad, vec)

        # B01 — gancho: o 3D liga a corrente; a manchete faz a pergunta.
        headline = T('Por que o campo não escapa?', 30, y=Y_TOP)
        self.until(BEAT['B01'] + .3)
        self.play(FadeIn(headline, shift=DOWN * .1), run_time=.8)
        self.mark('B01_manchete')
        self.until(BEAT['B01'] + 7.0)
        question = chip('E fora do anel?', color=TEXT_COLOR, y=-1.0, size=24)
        self.play(FadeIn(question), run_time=.5)
        self.until(BEAT['B02'] - .5)
        self.play(FadeOut(question), run_time=.4)

        # B02 — o objeto: modelo ideal, N e I (R e a vão para a vista de cima, no B03).
        self.until(BEAT['B02'] + .3)
        ideal = chip('Modelo ideal', y=-.6)
        self.play(FadeIn(ideal), run_time=.5)
        self.mark('B02_modelo_ideal')
        defs = VGroup(D(r'{N}:\ \text{número de espiras}', '{N}', y=0), D(r'{I}:\ \text{corrente no fio}', '{I}', y=0))
        defs.arrange(DOWN, aligned_edge=LEFT, buff=.3).move_to([0, -2.2, 0])
        card = panel(defs.width + .6, defs.height + .5, defs.get_center(), z=35)
        self.until(BEAT['B02'] + 2.5)
        self.play(FadeIn(card), LaggedStart(FadeIn(defs[0]), FadeIn(defs[1]), lag_ratio=.5), run_time=1.0)
        self.mark('B02_N_I')
        self.until(BEAT['B03'] - .7)
        self.play(FadeOut(VGroup(ideal, card, defs)), run_time=.6)

        # B03 — vista de cima: R e a; seta de raio r; B e dℓ tangentes, iguais, girando junto com o círculo.
        self.until(BEAT['B03'])
        self.play(FadeOut(headline), run_time=.6)
        self.until(EV['camera_topo_pousa'] + .1)
        u_R, u_a = np.array([np.cos(7 * PI / 6), np.sin(7 * PI / 6), 0]), np.array([np.cos(-PI / 6), np.sin(-PI / 6), 0])
        r_arrow = Arrow(CENTER, CENTER + R_MID * u_R, buff=0, color=GEO, stroke_width=3.5, max_tip_length_to_length_ratio=.1)
        r_lab = MathTex('R', font_size=44, color=GEO).move_to(CENTER + .5 * R_MID * u_R + .34 * np.array([-u_R[1], u_R[0], 0]))
        a_seg = Line(CENTER + R_MID * u_a, CENTER + R_OUT * u_a, color=GEO, stroke_width=5)
        ticks = VGroup(*[Line(ORIGIN, .24 * RIGHT, color=GEO, stroke_width=3.5).rotate(PI / 3).move_to(CENTER + r * u_a)
                         for r in (R_MID, R_OUT)])
        a_mid = CENTER + (R_MID + R_OUT) / 2 * u_a
        a_lab = MathTex('a', font_size=48, color=GEO).move_to([3.95, a_mid[1] - .55, 0])
        a_guide = DashedLine(a_mid, a_lab.get_left() + LEFT * .08, dash_length=.07, color=GEO, stroke_width=2)
        geo = VGroup(r_arrow, r_lab, a_seg, ticks, a_guide, a_lab).set_z_index(32)
        defs = VGroup(D(r'{R}:\ \text{raio médio do anel}', '{R}', y=0), D(r'{a}:\ \text{raio do tubo}', '{a}', y=0))
        defs.arrange(DOWN, aligned_edge=LEFT, buff=.3).move_to([0, -2.2, 0])
        card = panel(defs.width + .6, defs.height + .5, defs.get_center(), z=35)
        self.play(FadeIn(geo), FadeIn(card), FadeIn(defs), run_time=.5)
        self.mark('B03_R_a')
        self.wait(1.5)
        self.play(FadeOut(VGroup(geo, card, defs)), run_time=.5)
        outline = VGroup(*[Circle(radius=r, stroke_color=GEO, stroke_width=1.5, stroke_opacity=.5).move_to(CENTER)
                           for r in (R_IN, R_OUT)]).set_z_index(10)
        self.play(Create(outline), run_time=.4)
        self.until(TL['amperiano'][2]['t'] + .3)  # círculo amperiano já aceso
        r_def = D(r'{r}:\ \text{raio do caminho}', '{r}', y=Y_EQ)  # a fala chama r de "raio do caminho"
        self.play(self.rad.animate.set_value(1), FadeIn(r_def), run_time=.5)
        self.mark('B03_seta_r')
        self.until(TL['amperiano'][2]['t'] + 1.0)
        self.play(self.bgain.animate.set_value(1), run_time=.8)
        self.mark('B03_setas_B')
        self.until(GIRO['inicio_s'] + .9)
        self.play(self.dl.animate.set_value(1), run_time=.6)
        self.mark('B03_setas_dl')
        self.until(BEAT['B03'] + 12.0)
        par_tex = M(r'\mathbf B\parallel d\boldsymbol\ell', r'\mathbf B', r'd\boldsymbol\ell', size=44)
        par = chip(par_tex, color=TEXT_COLOR, y=-1.0)
        self.play(FadeIn(par), FadeOut(r_def), run_time=.5)
        self.link(par_tex[0][0], MAG, pulso(self.pB), guia=False)
        self.link(VGroup(*par_tex[0][2:4]), GEO, pulso(self.pdl), guia=False)
        self.until(BEAT['B03'] + 15.5)
        b_glyph = MathTex('B', font_size=40, color=MAG)
        same = chip('Mesmo', b_glyph, 'no círculo todo', color=TEXT_COLOR, y=-2.1, size=22)
        self.play(FadeIn(same), run_time=.5)
        self.link(b_glyph, MAG, pulso(self.pB), guia=False)
        self.until(BEAT['B04'] - .6)
        self.play(FadeOut(par), FadeOut(same), run_time=.5)

        # B04 — Ampère com elos; o círculo se desenrola numa faixa própria, acima da equação.
        y4 = -2.35
        self.until(BEAT['B04'] + .3)
        eq = M(r'\oint\mathbf B\cdot d\boldsymbol\ell=\mu_0\,I_{\rm enc}', r'\mathbf B', r'd\boldsymbol\ell', r'I_{\rm enc}', y=y4)
        self.play(FadeIn(eq), run_time=.8)
        self.mark('B04_ampere')
        self.until(BEAT['B04'] + 1.4)
        self.link(eq[0][1], MAG, pulso(self.pB), self.arrow_point(), name='B04_elo_B')
        self.until(BEAT['B04'] + 2.6)
        self.link(VGroup(*eq[0][3:5]), GEO, pulso(self.pdl), self.arrow_point(0), name='B04_elo_dl')
        self.until(BEAT['B04'] + 3.8)
        note = D(r'I_{\rm enc}:\ \text{corrente que atravessa o disco}', r'I_{\rm enc}', y=-3.65)
        self.play(FadeIn(note), self.disc.animate.set_value(1), run_time=.6)
        self.link(VGroup(*eq[0][8:12]), GREEN, pulso(self.pdisc), CENTER + DOWN * .45 * R_MID, name='B04_elo_Ienc')
        self.until(BEAT['B04'] + 5.8)
        # As setas paralelas piscam: é a justificativa visual de B·dℓ = B dℓ.
        eq = self.glyph(eq, M(r'\oint B\,d\ell=\mu_0\,I_{\rm enc}', 'B', r'd\ell', r'I_{\rm enc}', y=y4),
                        [([0], [0]), ([1], [1]), ([2], []), ([3, 4], [2, 3]), ([5], [4]), ([6, 7], [5, 6]),
                         ([8, 9, 10, 11], [7, 8, 9, 10])], 1.5, 'B04_escalar',
                        extras=[self.blink.animate(rate_func=there_and_back).set_value(1)])
        self.until(BEAT['B04'] + 7.6)
        eq = self.glyph(eq, M(r'B\oint d\ell=\mu_0\,I_{\rm enc}', 'B', r'd\ell', r'I_{\rm enc}', y=y4),
                        [([1], [0], {'path_arc': 1.4}), ([0], [1]), ([2, 3], [2, 3]), ([4], [4]), ([5, 6], [5, 6]),
                         ([7, 8, 9, 10], [7, 8, 9, 10])], 1.5, 'B04_B_sai')
        # Desenrolar, entre o toroide e a equação: uma cópia do círculo (com a sua seta de raio) encolhe e rola.
        rho = ROLL['escala'] * R_MID
        length = TAU * rho
        x0, y0 = -length / 2, -1.2
        roll = ValueTracker(0)

        def rolling():
            p = roll.get_value()
            c = np.array([x0 + p * length, y0 + rho, 0])
            parts = VGroup(Line([x0, y0, 0], [x0 + p * length + 1e-4, y0, 0]))
            if 1 - p > 1e-3:
                parts.add(Arc(radius=rho, start_angle=-PI / 2, angle=(1 - p) * TAU, arc_center=c))
            return parts.set_stroke(GEO, 3.5).set_z_index(41)
        self.until(ROLL['inicio_s'])
        self.mark('B04_desenrola')
        r_now, ang_now = amp_at(self.time)[0], R_ANG + spin(self.time)
        big = VGroup(Circle(radius=r_now, stroke_color=GEO, stroke_width=3.5).move_to(CENTER),
                     Line(CENTER, polar(r_now, ang_now), color=GEO, stroke_width=3)).set_z_index(41)
        c0 = np.array([x0, y0 + rho, 0])
        small = VGroup(Circle(radius=rho, stroke_color=GEO, stroke_width=3.5).move_to(c0),
                       Line(c0, c0 + rho * np.array([np.cos(ang_now), np.sin(ang_now), 0]), color=GEO, stroke_width=3))
        self.play(Transform(big, small), run_time=.8)
        tape = always_redraw(rolling)
        self.remove(big); self.add(tape)
        self.play(roll.animate.set_value(1), run_time=1.4, rate_func=smooth)
        tape.clear_updaters()
        # "2π vezes aquela seta": marcas a cada raio ao longo da reta.
        marks = VGroup(*[Line([x0 + k * rho, y0 - .09, 0], [x0 + k * rho, y0 + .09, 0], color=GEO, stroke_width=2.5)
                         for k in range(1, 7)]).set_z_index(41)
        unit = MathTex('r', font_size=30, color=GEO).move_to([x0 + rho / 2, y0 - .25, 0]).set_z_index(41)
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=.15), FadeIn(unit), run_time=.8)
        label = MathTex(r'2\pi r', font_size=M_EQ, color=GEO).move_to([0, y0 + .45, 0]).set_z_index(42)
        self.play(FadeIn(label, shift=UP * .1), run_time=.4)
        self.link(label, GEO, pulso(self.pc), polar(R_MID, -PI / 2 + .2), name='B04_elo_2pir')
        # O rótulo 2πr voa para o lugar de ∮dℓ; a reta fica na faixa dela.
        self.until(ROLL['inicio_s'] + ROLL['dur_s'] + .3)
        new = M(r'B\,(2\pi r)=\mu_0\,I_{\rm enc}', 'B', r'2\pi r', r'I_{\rm enc}', y=y4)
        self.mark('B04_2pir_voa')
        self.play(ReplacementTransform(eq[0][0], new[0][0]), FadeOut(VGroup(*eq[0][1:4])),
                  ReplacementTransform(label, VGroup(*new[0][2:5]), path_arc=-.6),
                  FadeIn(new[0][1]), FadeIn(new[0][5]),
                  *[ReplacementTransform(eq[0][i], new[0][i + 2]) for i in range(4, 11)], run_time=1.4)
        self.remove(*eq.get_family()); self.remove(*new.get_family()); self.add(new)
        ref = new
        self.play(FadeOut(VGroup(tape, marks, unit)), run_time=.4)
        self.until(BEAT['B04'] + 17.5)
        self.link(VGroup(*ref[0][2:5]), GEO, pulso(self.pc), guia=False)
        self.until(BEAT['B04'] + 19.0)
        self.play(FadeOut(note), run_time=.4)
        self.play(ref.animate.scale(M_REF / M_EQ).move_to([0, Y_REF, 0]), run_time=.8)
        self.until(BEAT['B05'] - 1.2)
        self.play(self.dl.animate.set_value(0), run_time=.5)

        # B05 — buraco: nada fura o disco; as setas encolhem até sumir.
        self.until(BEAT['B05'])
        self.bphys.set_value(0)  # comprimento fixo enquanto o círculo viaja
        self.heading('Teste 1 · no buraco')
        self.until(BEAT['B05'] + 3.2)
        count = M(r'I_{\rm enc}=0', r'I_{\rm enc}', size=M_CNT)
        self.play(FadeIn(count), run_time=.6)
        self.mark('B05_Ienc_0')
        self.link(VGroup(*count[0][0:4]), GREEN, pulso(self.pdisc), guia=False)
        self.until(BEAT['B05'] + 5.5)
        result = M('B=0', 'B', y=Y_SUP)
        self.play(FadeIn(result), run_time=.6)
        self.mark('B05_B_0')
        self.link(result[0][0], MAG, pulso(self.pB), guia=False)
        self.play(self.bgain.animate.set_value(0), run_time=1.0)
        self.until(BEAT['B06'] - .6)
        self.play(FadeOut(count), FadeOut(result), run_time=.5)

        # B06 — dentro: cada espira fura o disco uma vez (⊙). Contador em sincronia com o flash 3D.
        self.until(BEAT['B06'])
        self.heading('Teste 2 · dentro do enrolamento')
        self.until(CD['inicio_s'] - 1.2)
        lhs = M(r'I_{\rm enc}=', r'I_{\rm enc}', size=M_CNT, x=-.9)
        num = Integer(0, font_size=M_CNT, color=GREEN).set_z_index(40)
        sym = MathTex('I', font_size=M_CNT, color=GREEN).set_z_index(40)

        def place(_):
            num.set_value(sum(t_k(k, CD) <= self.time for k in range(N_TURNS)))
            num.next_to(lhs, RIGHT, buff=.16)
            sym.next_to(num, RIGHT, buff=.1).align_to(lhs[0][0], DOWN)
        num.add_updater(place); place(None)
        self.play(FadeIn(lhs), FadeIn(num), FadeIn(sym), run_time=.5)
        dots_in = always_redraw(lambda: self.markers('out', CD))

        def flying():
            group = VGroup()
            for k in range(N_TURNS):
                u = (self.time - t_k(k, CD)) / .45
                if 0 < u < 1:
                    a = polar(R_IN, PHI0 + TAU * k / N_TURNS)
                    group.add(Dot(a + smooth(u) * (num.get_center() - a), radius=.045, color=GREEN).set_opacity(1 - .5 * u))
            return group.set_z_index(44)
        fly = always_redraw(flying)
        self.add(dots_in, fly)
        self.until(CD['inicio_s'])
        self.mark('B06_contagem_inicio')
        self.until(CD['inicio_s'] + CD['dur_s'] + .5)
        self.mark('B06_contagem_fim')
        self.remove(fly)
        num.clear_updaters()
        count = M(r'I_{\rm enc}=24\,I', r'I_{\rm enc}', 'I', size=M_CNT)
        count.shift(lhs[0][0].get_center() - count[0][0].get_center())
        self.remove(lhs, num, sym); self.add(count)
        self.until(CD['inicio_s'] + CD['dur_s'] + 1.1)
        count = self.glyph(count, M(r'I_{\rm enc}=N\,I', r'I_{\rm enc}', 'N', 'I', size=M_CNT),
                           [([0, 1, 2, 3], [0, 1, 2, 3]), ([4], [4]), ([5, 6], [5]), ([7], [6])], 1.2, 'B06_24_vira_N')
        self.link(count[0][5], TEXT_COLOR, pulso(self.pin), self.ring_point('out'), name='B06_elo_N')
        self.until(BEAT['B06'] + 10.5)
        flyer = VGroup(*count[0][5:7]).copy()
        new = M(r'B\,(2\pi r)=\mu_0\,N\,I', 'B', r'2\pi r', 'N', 'I', size=M_REF, y=Y_REF)
        ref = self.glyph(ref, new, [(list(range(9)), list(range(9))), ([9, 10, 11, 12], [])], 1.3, 'B06_substitui',
                         extras=[flyer.animate.move_to(VGroup(*new[0][9:11])).set_opacity(0)])
        self.remove(flyer)
        self.until(BEAT['B06'] + 12.6)
        self.play(FadeOut(count), run_time=.4)
        # 2πr atravessa a igualdade primeiro, com a linha de cima ainda parada (o caminho até o denominador está livre);
        # depois B, =, μ₀, N e I descem para o lugar e a barra entra.
        res = M(r'B=\frac{\mu_0\,N\,I}{2\pi r}', 'B', 'N', 'I', r'2\pi r', size=M_RES)
        for i in (2, 3, 4):
            ref[0][i].set_z_index(60)
        for i in (7, 8, 9):
            res[0][i].set_z_index(60)
        late = {'delay': 1.1, 'run_time': .9}
        res = self.glyph(ref, res, [([2, 3, 4], [7, 8, 9], {'path_arc': .8, 'run_time': 1.1}), ([1, 5], []),
                                    ([0], [0], late), ([6], [1], late), ([7, 8], [2, 3], late), ([9], [4], late), ([10], [5], late),
                                    ([], [6], {'delay': .9, 'run_time': .4})], 2.0, 'B06_2pir_desce')
        self.until(BEAT['B06'] + 16.0)
        self.link(res[0][9], GEO, pulso(self.pr), polar(amp_at(self.time)[0] * .6, R_ANG + spin(self.time)), name='B06_elo_r')
        self.until(BEAT['B06'] + 17.6)
        self.bphys.set_value(1)
        self.play(self.bgain.animate.set_value(1), run_time=1.0)
        self.mark('B06_setas_voltam')
        self.link(res[0][0], MAG, pulso(self.pB), guia=False)
        self.until(BEAT['B06'] + 20.5)
        uniform = chip('Não é uniforme', color=TEXT_COLOR, y=Y_SUP - .2, size=22)
        self.play(FadeIn(uniform), run_time=.5)
        self.until(BEAT['B07'] - .5)
        self.play(FadeOut(uniform), run_time=.4)

        # B07 — fora: cada espira fura duas vezes, em sentidos opostos; NI − NI cancela.
        self.until(BEAT['B07'])
        self.bphys.set_value(0)  # comprimento fixo enquanto o círculo viaja para fora
        self.heading('Teste 3 · fora do anel')
        back = M(r'B\,(2\pi r)=\mu_0\,I_{\rm enc}', 'B', r'2\pi r', r'I_{\rm enc}', size=M_REF, y=Y_REF)
        for i in (7, 8, 9):
            res[0][i].set_z_index(60)
        # Volta: B, =, μ₀ sobem primeiro; o 2πr sobe depois, pelo caminho já livre.
        ref = self.glyph(res, back, [([0], [0], {'run_time': .8}), ([1], [6], {'run_time': .8}), ([2, 3], [7, 8], {'run_time': .8}),
                                     ([4, 5], []), ([6], []), ([7, 8, 9], [2, 3, 4], {'path_arc': -.8, 'delay': .7, 'run_time': 1.0}),
                                     ([], [1, 5], {'delay': 1.2, 'run_time': .5}), ([], [9, 10, 11, 12], {'delay': .6, 'run_time': .6})], 1.7)
        crosses = always_redraw(lambda: self.markers('in', CF))
        self.add(crosses)
        count = M(r'I_{\rm enc}=N\,I-N\,I', r'I_{\rm enc}', 'N', 'I', size=M_CNT)
        self.until(CF['todos_dentro_s'] + .3)
        self.play(FadeIn(VGroup(*count[0][0:7])), run_time=.5)
        self.mark('B07_NI_dentro')
        self.link(VGroup(*count[0][5:7]), GREEN, pulso(self.pin), self.ring_point('out'), name='B07_elo_NI_dentro')
        self.until(CF['inicio_s'] + CF['dur_s'] + .5)
        self.play(FadeIn(VGroup(*count[0][7:10])), run_time=.5)
        self.mark('B07_NI_fora')
        self.link(VGroup(*count[0][8:10]), GREEN, pulso(self.pout), self.ring_point('in'), name='B07_elo_NI_fora')
        self.until(BEAT['B07'] + 11.6)
        strikes = VGroup(strike(VGroup(*count[0][5:7])), strike(VGroup(*count[0][8:10])))
        self.play(Create(strikes[0]), Create(strikes[1]), run_time=.5)
        # Sem correspondência real entre NI − NI e 0: os termos saem e o 0 entra no lugar (sem morphing).
        self.until(BEAT['B07'] + 12.4)
        zero = M(r'I_{\rm enc}=0', r'I_{\rm enc}', size=M_CNT)
        zero.shift(count[0][0].get_center() - zero[0][0].get_center())
        self.mark('B07_cancela')
        self.play(FadeOut(VGroup(*count[0][5:10], strikes)), run_time=.5)
        self.play(FadeIn(zero[0][5]), run_time=.5)
        self.remove(*count.get_family()); self.add(zero)
        count = zero
        self.until(BEAT['B07'] + 14.3)
        result = M('B=0', 'B', y=Y_SUP)
        self.play(FadeIn(result), run_time=.6)
        self.mark('B07_B_0')
        self.link(result[0][0], MAG, pulso(self.pB), guia=False)
        self.play(self.bgain.animate.set_value(0), run_time=1.0)

        # B08 — gráfico B(r): eixo r na escala da vista de cima; barra do cursor = setas do círculo.
        self.until(BEAT['B08'])
        self.play(FadeOut(VGroup(count, result, ref)), FadeOut(self.top), self.mk.animate.set_value(0),
                  self.disc.animate.set_value(.6), run_time=.6)
        self.remove(dots_in, crosses)
        self.top = VGroup()
        self.bphys.set_value(1)
        base, r_max = -3.95, keyed(TL['amperiano'], 1e9, 'r')
        y_of = lambda r: base + b_len(r)
        r_axis = Arrow([-.05, base, 0], [3.9, base, 0], buff=0, color=GEO, stroke_width=2.4, max_tip_length_to_length_ratio=.04)
        b_axis = Arrow([0, base - .12, 0], [0, base + b_len(R_IN) + .6, 0], buff=0, color=MAG, stroke_width=2.4,
                       max_tip_length_to_length_ratio=.09)
        r_name = MathTex('r', font_size=40, color=GEO).move_to([3.85, base - .36, 0])
        b_name = MathTex('B', font_size=40, color=MAG).next_to(b_axis.get_end(), RIGHT, buff=.12)
        axes = VGroup(r_axis, b_axis, r_name, b_name).set_z_index(40)
        self.until(BEAT['B08'] + .8)
        self.play(GrowArrow(r_axis), GrowArrow(b_axis), FadeIn(r_name), FadeIn(b_name), run_time=1.0)
        drops = VGroup(*[DashedLine([r, CENTER[1], 0], [r, base, 0], dash_length=.1, color=GEO, stroke_width=1.5,
                                    stroke_opacity=.7) for r in (R_IN, R_OUT)]).set_z_index(38)
        edge_labels = VGroup(*[MathTex(s, font_size=32, color=GEO).move_to([r, base - .36, 0])
                               for r, s in ((R_IN, r'R-a'), (R_OUT, r'R+a'))]).set_z_index(40)
        self.until(BEAT['B08'] + 2.0)
        self.play(Create(drops), FadeIn(edge_labels), run_time=1.0)
        self.mark('B08_bordas_descem')
        left = M(r'B=\frac{\mu_0\,N\,I}{2\pi r}', 'B', 'N', 'I', r'2\pi r', size=48, x=-2.4, y=-2.3)
        self.play(FadeIn(left), run_time=.6)
        r_glyph = left[0][9]

        def light_r(m):  # o r do denominador acende enquanto o cursor anda dentro do enrolamento
            r_now = amp_at(self.time)[0]
            m.set_color(interpolate_color(ManimColor(GEO), WHITE, .85 if R_IN <= r_now <= R_OUT else 0.))
        self.until(EV['varredura_inicio'] - .2)
        self.bgain.set_value(1)

        def curve_now():
            r_now = amp_at(self.time)[0]
            if r_now < .01:
                return VGroup()
            pieces, w = VGroup(), 5 * (1 + self.pcurve.get_value())
            for a, b in ((0, R_IN), (R_IN, R_OUT), (R_OUT, r_max)):
                hi = min(r_now, b - 1e-6)
                if hi <= a:
                    break
                rs = np.linspace(a + 1e-6, hi, 60)
                pieces.add(VMobject(stroke_color=MAG, stroke_width=w).set_points_as_corners([[r, y_of(r), 0] for r in rs]))
            for r in (R_IN, R_OUT):  # salto do modelo ideal, tracejado
                if r_now >= r:
                    pieces.add(DashedLine([r, base, 0], [r, base + b_len(r), 0], dash_length=.08, color=MAG, stroke_width=2.5))
            bar = Line([r_now, base, 0], [r_now, y_of(r_now) + 1e-3, 0], color=MAG, stroke_width=7, stroke_opacity=.55)
            cursor = Dot([r_now, y_of(r_now), 0], radius=.07, color=MAG)
            return VGroup(bar, pieces, cursor).set_z_index(42)
        plot = always_redraw(curve_now)
        self.until(EV['varredura_inicio'])
        self.add(plot)
        r_glyph.add_updater(light_r)
        self.mark('B08_varredura')
        sweep = lambda r: EV['varredura_inicio'] + (EV['varredura_fim'] - EV['varredura_inicio']) * r / r_max
        zero_in = M('B=0', 'B', size=30, x=.78, y=base + .55)
        self.until(sweep(.55 * R_IN))
        self.play(FadeIn(zero_in), run_time=.3)
        self.link(zero_in, MAG, alvo=[.78, base, 0], name='B08_elo_zero_buraco')
        prop = chip(MathTex(r'\propto 1/r', font_size=36, color=TEXT_COLOR), color=TEXT_COLOR, x=-2.4, y=-3.55)
        self.until(sweep(R_IN + .35 * (R_OUT - R_IN)))
        self.play(FadeIn(prop), run_time=.3)
        self.link(r_glyph, GEO, alvo=[amp_at(self.time + .5)[0], y_of(amp_at(self.time + .5)[0]), 0], name='B08_elo_1_r')
        zero_out = M('B=0', 'B', size=30, x=3.45, y=base + .55)
        self.until(EV['varredura_fim'] + .1)
        r_glyph.clear_updaters(); r_glyph.set_color(GEO)
        self.play(FadeIn(zero_out), run_time=.3)
        self.link(zero_out, MAG, alvo=[3.45, base, 0], name='B08_elo_zero_fora')
        self.until(EV['varredura_fim'] + 2.0)
        compare = VGroup(*[Arrow([r, base, 0], [r, y_of(r), 0], buff=0, color=MAG, stroke_width=6,
                                 max_tip_length_to_length_ratio=.16) for r in (R_IN, R_OUT)]).set_z_index(43)
        self.play(*[GrowArrow(a) for a in compare], run_time=.8)
        ratio = chip(MathTex(r'\approx 1{,}9\times', font_size=36, color=TEXT_COLOR), color=TEXT_COLOR,
                     x=(R_IN + R_OUT) / 2 + .05, y=y_of(R_IN) + .25)
        self.play(FadeIn(ratio), run_time=.5)
        self.mark('B08_razao')
        self.until(EV['varredura_fim'] + 5.0)
        self.link(left, MAG, AnimationGroup(pulso(self.pcurve), pulso(self.pB)), [R_MID, y_of(R_MID), 0], name='B08_elo_formula')
        self.until(BEAT['B09'] - .8)
        plot.clear_updaters()
        self.play(FadeOut(VGroup(axes, drops, edge_labels, left, prop, compare, ratio, zero_in, zero_out, outline)),
                  FadeOut(plot), self.rad.animate.set_value(0), run_time=.6)

        # B09 — caso-limite: anel grande perto da seção ⇒ solenoide.
        self.until(BEAT['B09'] + .2)
        eq = M(r'B=\frac{\mu_0\,N\,I}{2\pi r}', 'B', 'N', 'I', r'2\pi r')
        self.play(FadeIn(eq), run_time=.6)
        self.until(BEAT['B09'] + 1.5)
        approx = M(r'{r}\approx{R}', '{r}', '{R}', size=M_REF, y=Y_REF)
        self.play(FadeIn(approx), run_time=.5)
        self.mark('B09_r_aprox_R')
        self.until(BEAT['B09'] + 3.0)
        eq = self.glyph(eq, M(r'B\approx\frac{\mu_0\,N\,I}{2\pi R}', 'B', 'N', 'I', r'2\pi R'),
                        [(list(range(9)), list(range(9))), ([9], [9])], 1.0, 'B09_r_vira_R')
        self.until(BEAT['B09'] + 4.6)
        eq = self.glyph(eq, M(r'B\approx\mu_0\left(\frac{N}{2\pi R}\right)I', 'B', 'N', 'I', r'2\pi R'),
                        [([0, 1], [0, 1]), ([2, 3], [2, 3]), ([4], [5]), ([5], [11], {'path_arc': -1.0}), ([6], [6]),
                         ([7, 8, 9], [7, 8, 9]), ([], [4]), ([], [10])], 1.4, 'B09_agrupa')
        self.until(BEAT['B09'] + 6.6)
        n_note = D(r'{n}:\ \text{espiras por metro}', '{n}', y=Y_SUP)
        eq = self.glyph(eq, M(r'B\approx\mu_0\,{n}\,I', 'B', '{n}', 'I'),
                        [([0, 1, 2, 3], [0, 1, 2, 3]), ([4, 5, 6, 7, 8, 9, 10], [4]), ([11], [5])], 1.4, 'B09_colapso_n',
                        extras=[FadeIn(n_note)])
        self.until(BEAT['B09'] + 8.5)
        solenoid = chip('Solenoide', color=TEXT_COLOR, y=Y_LOW, size=22)
        self.play(FadeIn(solenoid), run_time=.5)
        self.mark('B09_solenoide')
        self.until(BEAT['B10'] - .6)
        self.play(FadeOut(VGroup(eq, approx, n_note, solenoid)), run_time=.6)

        # B10 — fechamento: painel com o ícone do anel; DENTRO e FORA ligados ao ícone.
        self.until(BEAT['B10'] + .3)
        card = RoundedRectangle(width=8.4, height=3.7, corner_radius=.2, stroke_color=BLUE_L, stroke_width=2,
                                fill_color=PANEL, fill_opacity=.92).move_to([0, -2.2, 0]).set_z_index(36)
        ic = np.array([-3.15, -2.2, 0])
        icon_rings = VGroup(*[Circle(radius=r, stroke_color=GEO, stroke_width=2).move_to(ic) for r in (.36, .7)]).set_z_index(38)
        crown = Annulus(inner_radius=.36, outer_radius=.7, fill_color=MAG, fill_opacity=0, stroke_width=0).move_to(ic).set_z_index(37)
        outside = VGroup(Circle(radius=.36, stroke_width=0, fill_color=DARK_MAG, fill_opacity=.45).move_to(ic),
                         DashedVMobject(Circle(radius=.28, stroke_color=MAG, stroke_width=2), num_dashes=10).move_to(ic),
                         DashedVMobject(Circle(radius=.9, stroke_color=DARK_MAG, stroke_width=2.5), num_dashes=22).move_to(ic)
                         ).set_z_index(37)
        row1 = VGroup(M(r'B=\frac{\mu_0\,N\,I}{2\pi r}', 'B', 'N', 'I', r'2\pi r', size=M_RES, y=0),
                      chip('Dentro', color=TEXT_COLOR, size=22, y=0)).arrange(RIGHT, buff=.4)
        row2 = VGroup(M('B=0', 'B', size=M_RES, y=0), chip('Fora', color=TEXT_COLOR, size=22, y=0)).arrange(RIGHT, buff=.4)
        row1.move_to([.75, -1.45, 0]); row2.move_to([.75, -3.0, 0]).align_to(row1, LEFT)
        self.play(FadeIn(card), FadeIn(icon_rings), run_time=.7)
        self.until(BEAT['B10'] + 1.2)
        self.play(FadeIn(row1), run_time=.8)
        self.mark('B10_dentro')
        self.link(row1[1], MAG, crown.animate.set_fill(opacity=.6), crown, name='B10_elo_dentro')
        self.until(BEAT['B10'] + 3.4)
        self.play(FadeIn(row2), run_time=.8)
        self.mark('B10_fora')
        self.link(row2[1], MAG, FadeIn(outside), outside[2].get_bottom() + UP * .02, name='B10_elo_fora')
        self.until(EV['endcard'] - .5)
        self.remove(amp, rad, vec)
        self.play(FadeOut(VGroup(card, icon_rings, crown, outside, row1, row2, tag)), FadeOut(logo), run_time=.5)
        # End card: somente o handle (degradê oficial ciano → violeta → magenta), sem watermark.
        handle = screen_text('@labparallax', 48, oversample=2).set_z_index(40)  # handle em minúsculas (marca)
        handle.set_color_by_gradient(PRIMARY_COLOR, SECONDARY_COLOR, MAG)
        self.until(EV['endcard'] + .3)
        self.play(FadeIn(handle, scale=.96), run_time=.5)
        self.mark('endcard')
        self.until(TL['duracao_s'] - .45)
        self.play(FadeOut(handle), run_time=.4)
        self.until(TL['duracao_s'])
        self.mark('fim')
        (UNIT / 'media_preview' / 'estados.json').write_text(json.dumps(self.events, ensure_ascii=False, indent=2), encoding='utf-8')
