"""vid_0025 — POR QUE O ARCO-ÍRIS TEM 42°? (DA EQUAÇÃO AO FENÔMENO · EP. 07)

Preview silencioso C01–C11, formato curto vertical (9×16). Rodada r6 (voz v5 sincronizada por âncoras, nova abertura, referencial dos 42°). Uma única implementação da
física (helpers puros abaixo) alimenta raios desenhados, gráfico θ × b/R, destaques e QA.
A trajetória de cada raio é calculada por interseção reta–circunferência, refração vetorial
(Snell) e reflexão vetorial; nada é posicionado a olho.

Convenção espacial: eixo x esquerda → direita; luz solar propaga esquerda → direita;
raio protagonista entra na metade superior (b > 0) e sai para a esquerda e para baixo.
"""
from contextlib import contextmanager
from pathlib import Path
import os
import sys

import numpy as np
from manim import *

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")     # avisos do auditor têm acentos e símbolos
except Exception:
    pass

ROOT = Path(__file__).absolute().parents[2]  # .absolute(): a pasta videos/ é uma junção; resolve() sairia do repositório
sys.path.insert(0, str(ROOT))
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import screen_text  # noqa: E402

UNIT = Path(__file__).absolute().parent
config.media_dir = os.environ.get("MEDIA_DIR", str(UNIT / "media"))
config.background_color = BACKGROUND_COLOR
config.max_files_cached = 300

# ----------------------------------------------------------------------------- cores
INK = TEXT_COLOR            # texto, equações, raio solar
CYAN = PRIMARY_COLOR        # θ (protagonista cromático)
VIOLET = SECONDARY_COLOR    # i
PINK = "#EA63FF"            # r
BLUE = "#267BFF"            # gota
DIM = "#8FA3C4"
RED, VIO = "#FF4B4B", "#9B5CFF"
SPECTRUM = ["#FF4B4B", "#FFA03C", "#FFE24B", "#4BE07D", "#3CA4FF", "#9B5CFF"]  # vermelho (fora) → violeta (dentro)

# ----------------------------------------------------------------------------- física (R = 1, radianos)
N_WATER, N_RED, N_VIOLET = 1.333, 1.331, 1.343
N_SAMPLES = 25
CLUSTER_LO, CLUSTER_HI = 0.793, 0.913   # faixa do amontoamento (θ a menos de ~1° do máximo)


def i_from_b_ratio(x):
    """sin i = b/R."""
    return np.arcsin(np.clip(x, -1.0, 1.0))


def r_from_i(i, n):
    """Snell: sin i = n sin r."""
    return np.arcsin(np.sin(i) / n)


def theta_from_i(i, n):
    """θ = 4r − 2i (arco primário; θ medido a partir da direção antissolar)."""
    return 4.0 * r_from_i(i, n) - 2.0 * i


def theta_from_b_ratio(x, n):
    return theta_from_i(i_from_b_ratio(x), n)


def theta_deg_from_b_ratio(x, n):
    return np.degrees(theta_from_b_ratio(x, n))


def i_max(n):
    """dθ/di = 0 → cos² i = (n² − 1)/3."""
    return np.arccos(np.sqrt((n * n - 1.0) / 3.0))


def b_samples(n_samples=N_SAMPLES):
    """Amostras equiponderadas em área do disco incidente: b_k/R = sqrt((k − 1/2)/N)."""
    return np.array([np.sqrt((k - 0.5) / n_samples) for k in range(1, n_samples + 1)])


XS25 = b_samples()
CLUSTER_IDX = [k for k, x in enumerate(XS25) if CLUSTER_LO <= x <= CLUSTER_HI]

# ----------------------------------------------------------------------------- geometria vetorial do raio


def unit(v):
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v)


def ang_between(u, v):
    return float(np.arccos(np.clip(np.dot(unit(u), unit(v)), -1.0, 1.0)))


def circle_hit(p0, d):
    """Menor t > 0 com |p0 + t d|² = 1 (circunferência unitária centrada na origem)."""
    b = float(np.dot(p0, d))
    c = float(np.dot(p0, p0)) - 1.0
    disc = max(b * b - c, 0.0)
    roots = [-b - np.sqrt(disc), -b + np.sqrt(disc)]
    good = [t for t in roots if t > 1e-9]
    return min(good)


def refract(d, normal, eta):
    """d, normal unitários, d·normal < 0; eta = n_origem/n_destino."""
    cosi = -float(np.dot(d, normal))
    k = 1.0 - eta * eta * (1.0 - cosi * cosi)
    return unit(eta * d + (eta * cosi - np.sqrt(max(k, 0.0))) * normal)


def reflect(d, normal):
    return unit(d - 2.0 * float(np.dot(d, normal)) * normal)


def trace_ray(x, n, x_start=-2.4):
    """Trajetória completa (R = 1, centro na origem, luz em +x) para b/R = x."""
    p0 = np.array([x_start, float(x), 0.0])
    d0 = np.array([1.0, 0.0, 0.0])
    P1 = p0 + circle_hit(p0, d0) * d0
    N1 = unit(P1)
    d1 = refract(d0, N1, 1.0 / n)
    P2 = P1 + circle_hit(P1, d1) * d1
    N2 = unit(P2)
    d2 = reflect(d1, N2)
    P3 = P2 + circle_hit(P2, d2) * d2
    N3 = unit(P3)
    d3 = refract(d2, -N3, n)
    back = np.array([-1.0, 0.0, 0.0])
    return dict(
        x=float(x), n=n, p0=p0, P1=P1, P2=P2, P3=P3, N1=N1, N2=N2, N3=N3,
        d0=d0, d1=d1, d2=d2, d3=d3,
        i=ang_between(-d0, N1), r=ang_between(d1, -N1), theta=ang_between(d3, back),
    )


# ----------------------------------------------------------------------------- paleta de apoio (padrão dos longos, docs/padrao_video_longo.md)
GEO = "#B8C4DA"        # geometria (b, R, normais, construções)
PANEL = "#0E2A52"      # painel de destaque
BLUE_L = "#7FB2FF"
SHIRT = "#5AA2FF"
WARM = "#FFC857"       # Sol (decoração; o espectro do arco-íris também usa amarelo)
SUN_CORE = "#FFD166"
SCENE_PACE = {"C01": 0.78, "C02": 0.80, "C03": 0.80, "C04": 0.80, "C05": 0.82, "C06": 0.76,
              "C07": 0.80, "C08": 0.82, "C09": 0.76, "C10": 0.78, "C11": 0.72}


# ----------------------------------------------------------------------------- utilidades de tela


@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width = config.pixel_height = 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def words(content, size=26, color=INK, opacity=1.0, t2c=None, max_width=8.0, oversample=2, caps=True):
    """Texto de tela: Space Grotesk Medium em MAIÚSCULAS (padrão dos longos). Símbolos vão em MathTex."""
    if caps:
        content = content.upper()
        if t2c:
            t2c = {k.upper(): v for k, v in t2c.items()}
    with wide_pango():
        t = screen_text(content, size, oversample=oversample, **({"t2c": t2c} if t2c else {}))
    if not t2c:
        t.set_color(color)
    t.set_opacity(opacity)
    if t.width > max_width:
        t.scale_to_fit_width(max_width)
    return t.set_z_index(40)


def math(*parts, size=44, color=INK, max_width=8.0):
    m = MathTex(*parts, font_size=size, color=color)
    if m.width > max_width:
        m.scale_to_fit_width(max_width)
    return m.set_z_index(40)


def mix(*parts, size=20, color=DIM, opacity=1.0, max_width=8.0, gap=0.13):
    """Linha mista: str vira texto em caixa alta; tupla ("tex"[, cor]) vira MathTex."""
    items = []
    for p in parts:
        if isinstance(p, str):
            items.append(words(p, size, color, opacity, max_width=99))
        else:
            items.append(math(p[0], size=size * 1.4, color=(p[1] if len(p) > 1 else color), max_width=99))
    g = VGroup(*items).arrange(RIGHT, buff=gap)
    if g.width > max_width:
        g.scale_to_fit_width(max_width)
    return g


def lines(*texts, size=22, color=INK, t2c=None, gap=0.14, max_width=8.2):
    """Várias linhas de texto centralizadas."""
    g = VGroup(*[words(t, size, color, t2c=t2c, max_width=max_width) for t in texts]).arrange(DOWN, buff=gap)
    return g


def paint(m, mapping):
    """Colore tokens de MathTex (substring=False para não pintar 'i' dentro de 'sin')."""
    for tok, col in mapping.items():
        m.set_color_by_tex(tok, col, substring=False)
    return m


def panel(mob, pad=0.22, opacity=0.5):
    r = RoundedRectangle(width=mob.width + 2 * pad, height=mob.height + 2 * pad, corner_radius=0.14, fill_color=PANEL,
                         fill_opacity=opacity, stroke_color=BLUE_L, stroke_width=1.6, stroke_opacity=0.85).move_to(mob)
    r.set_z_index(35)
    r.audit_skip = True
    return r


def glow_of(m, color, width=10, opacity=0.16):
    c = m.copy()
    c.set_stroke(color, width=width, opacity=opacity)
    c.set_z_index(max(m.z_index - 1, 0))
    c.audit_skip = True
    return c


def skip_audit(*mobs):
    for m in mobs:
        m.audit_skip = True
    return mobs[0] if len(mobs) == 1 else mobs


def arc_between(vertex, u, v, radius, color, stroke_width=2.6, opacity=1.0):
    """Arco do menor ângulo entre as direções u e v, com vértice em vertex (vetores reais)."""
    a1 = np.arctan2(u[1], u[0])
    a2 = np.arctan2(v[1], v[0])
    delta = (a2 - a1 + np.pi) % (2 * np.pi) - np.pi
    return Arc(radius=radius, start_angle=a1, angle=delta, arc_center=vertex,
               color=color, stroke_width=stroke_width, stroke_opacity=opacity)


def arc_label(vertex, u, v, radius, mob, pad=0.3):
    bis = unit(unit(u) + unit(v))
    return mob.move_to(vertex + (radius + pad) * bis)


def dashed(p, q, color=GEO, opacity=0.5, width=1.6, dash=0.1):
    return DashedLine(p, q, color=color, stroke_opacity=opacity, stroke_width=width, dash_length=dash)


def polyline(pts, **kw):
    m = VMobject(**kw)
    if len(pts) >= 2:
        m.set_points_as_corners(pts)
    return m


def tick_mark(line, size=0.12, color=BLUE, n=1):
    """Marcas de igualdade (n tracinhos perpendiculares no meio do segmento)."""
    mid = line.get_center()
    d = unit(line.get_end() - line.get_start())
    p = np.array([-d[1], d[0], 0.0])
    marks = VGroup()
    for k in range(n):
        off = (k - (n - 1) / 2) * 0.08 * d
        marks.add(Line(mid + off - size * p, mid + off + size * p, color=color, stroke_width=2.6))
    return marks


# ----------------------------------------------------------------------------- arte: pessoa, Sol, gota de chuva


def make_person(foot, H=1.25):
    """Pessoa de perfil, olhando para a direita (de costas para o Sol). O centro da cabeça fica a altura H do pé."""
    fx, fy = float(foot[0]), float(foot[1])
    u = H / 1.25
    P = lambda dx, dy: np.array([fx + dx * u, fy + dy * u, 0.0])
    cap = dict(cap_style=CapStyleType.ROUND)
    head = Circle(radius=0.135 * u, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(P(0, 1.25))
    nose = Polygon(P(0.125, 1.28), P(0.205, 1.235), P(0.125, 1.2), fill_color=INK, fill_opacity=1, stroke_width=0)
    eye = Dot(P(0.065, 1.285), radius=0.022 * u, color=BACKGROUND_COLOR)
    neck = Line(P(0, 1.12), P(0, 1.03), color=INK, stroke_width=6 * u, **cap)
    torso = Polygon(P(-0.15, 1.04), P(0.15, 1.04), P(0.12, 0.60), P(-0.12, 0.60), fill_color=SHIRT, fill_opacity=0.95,
                    stroke_color=SHIRT, stroke_width=3, stroke_opacity=1.0).round_corners(0.05 * u)
    arm_b = Line(P(-0.02, 1.0), P(-0.17, 0.66), color=GEO, stroke_width=6 * u, **cap)
    arm_f = Line(P(0.02, 1.0), P(0.24, 0.72), color=INK, stroke_width=6 * u, **cap)
    leg_b = Line(P(-0.04, 0.6), P(-0.12, 0.04), color=GEO, stroke_width=7 * u, **cap)
    leg_f = Line(P(0.04, 0.6), P(0.12, 0.04), color=INK, stroke_width=7 * u, **cap)
    foot_b = Line(P(-0.12, 0.03), P(-0.01, 0.03), color=GEO, stroke_width=5 * u, **cap)
    foot_f = Line(P(0.12, 0.03), P(0.23, 0.03), color=INK, stroke_width=5 * u, **cap)
    g = VGroup(arm_b, leg_b, foot_b, torso, leg_f, foot_f, arm_f, neck, head, nose, eye)
    g.eye_point = P(0, 1.25)
    return g


def make_sun(c, r=0.3):
    c = np.array([c[0], c[1], 0.0])
    halo = VGroup(*[Circle(radius=r * k, stroke_width=0, fill_color=WARM, fill_opacity=o).move_to(c)
                    for k, o in ((3.1, 0.04), (2.4, 0.07), (1.8, 0.12), (1.4, 0.2))])
    rays = VGroup(*[Line(c + r * 1.55 * np.array([np.cos(q), np.sin(q), 0]), c + r * (2.15 if k % 2 == 0 else 1.9) * np.array([np.cos(q), np.sin(q), 0]),
                         color=WARM, stroke_width=3.2, cap_style=CapStyleType.ROUND)
                    for k, q in enumerate(np.linspace(0, TAU, 12, endpoint=False))])
    core = Circle(radius=r, stroke_width=0, fill_color=SUN_CORE, fill_opacity=1).move_to(c)
    g = VGroup(halo, rays, core)
    g.audit_skip = True
    return g


def make_drop(c, size=0.1, color=BLUE_L, opacity=0.8):
    """Gota de chuva (formato de lágrima)."""
    c = np.array([c[0], c[1], 0.0])
    r = size
    body = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=opacity).move_to(c)
    apex = c + np.array([0, 2.3 * r, 0])
    a1, a2 = np.radians(28), np.radians(152)
    tip = Polygon(c + r * np.array([np.cos(a1), np.sin(a1), 0]), apex, c + r * np.array([np.cos(a2), np.sin(a2), 0]),
                  stroke_width=0, fill_color=color, fill_opacity=opacity)
    g = VGroup(body, tip)
    g.audit_skip = True
    return g


def make_ground(y_top, depth=1.6, color=BLUE, bands=7, op=0.09, width=9.4):
    """Chão em degradê (faixas)."""
    g = VGroup()
    for k in range(bands):
        h = depth / bands
        g.add(Rectangle(width=width, height=h, stroke_width=0, fill_color=color, fill_opacity=op * (1 - k / bands))
              .move_to([0, y_top - h * (k + 0.5), 0]))
    g.audit_skip = True
    return g


class Gota:
    """Mapeia a física normalizada (R = 1) para a cena: ponto = C + R_scene·p."""

    def __init__(self, center, radius, x_left=-4.25):
        self.C = np.array([*center[:2], 0.0])
        self.R = radius
        self.x_left = x_left

    @property
    def x_start_norm(self):
        return (self.x_left - self.C[0]) / self.R

    def pt(self, p):
        return self.C + self.R * np.asarray(p)

    def trace(self, x, n=N_WATER):
        return trace_ray(x, n, x_start=self.x_start_norm)

    def circle(self, **kw):
        kw = dict(color=BLUE, stroke_width=3.2, fill_color=BLUE, fill_opacity=0.08) | kw
        return Circle(radius=self.R, **kw).move_to(self.C)

    def ray_lines(self, tr, exit_len=2.4, color=INK, width=2.4, opacity=1.0, with_incident=True):
        """Quatro segmentos: incidente, corda 1, corda 2, saída (exit_len em unidades de cena)."""
        P1, P2, P3 = self.pt(tr["P1"]), self.pt(tr["P2"]), self.pt(tr["P3"])
        kw = dict(color=color, stroke_width=width, stroke_opacity=opacity)
        segs = []
        if with_incident:
            segs.append(Line(self.pt(tr["p0"]), P1, **kw))
        segs += [Line(P1, P2, **kw), Line(P2, P3, **kw), Line(P3, P3 + exit_len * tr["d3"], **kw)]
        return VGroup(*segs)


# ----------------------------------------------------------------------------- auditoria de sobreposição


def _text_units(mobs):
    out = []

    def rec(m):
        if getattr(m, "audit_skip", False):
            return
        if isinstance(m, (Text, MathTex, DecimalNumber)):
            out.append(m)
            return
        for s in m.submobjects:
            rec(s)

    for m in mobs:
        rec(m)
    return out


def _stroke_leaves(mobs):
    out = []

    def rec(m):
        if getattr(m, "audit_skip", False) or isinstance(m, (Text, MathTex, DecimalNumber, ImageMobject)):
            return
        if isinstance(m, VMobject) and not m.submobjects and m.get_num_points() > 0:
            if m.get_stroke_width() >= 1.0 and m.get_stroke_opacity() >= 0.25:
                out.append(m)
            return
        for s in m.submobjects:
            rec(s)

    for m in mobs:
        rec(m)
    return out


def _sample(m, step=0.07):
    pts = m.get_points()
    n = len(pts) // 4
    if n == 0:
        return np.zeros((0, 3))
    segs = []
    for i in range(n):
        p0, p1, p2, p3 = pts[4 * i:4 * i + 4]
        ln = np.linalg.norm(p3 - p0) + np.linalg.norm(p1 - p0) + np.linalg.norm(p2 - p3)
        k = max(2, int(ln / step))
        t = np.linspace(0, 1, k)[:, None]
        segs.append((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)
    return np.vstack(segs)


def _name(t):
    s = getattr(t, "text", None) or getattr(t, "tex_string", None)
    if s is None and isinstance(t, DecimalNumber):
        s = f"{t.number:.2f}"
    return (s or "?")[:34]


def _bbox(t, shrink=0.025):
    return (t.get_left()[0] + shrink, t.get_right()[0] - shrink, t.get_bottom()[1] + shrink, t.get_top()[1] - shrink)


# ----------------------------------------------------------------------------- sincronização com a voz
import json  # noqa: E402

FPS = int(round(config.frame_rate))     # 15 no preview, 30 no render final (a sincronização é por quadro)
SMAX = 1.5         # as animações podem se alongar até 1,5× para preencher a fala (acima disso, a imagem espera parada)
LEAD = 0.10        # a imagem começa 0,10 s antes da palavra (atraso máximo tolerado: 0,2 s depois dela)
MEDIR = os.environ.get("MEDIR") == "1"       # passe de medição: durações naturais, sem renderizar
_SYNC = UNIT / "sync.json"
SY = json.loads(_SYNC.read_text(encoding="utf-8")) if (not MEDIR and _SYNC.exists()) else None
AUDIT_ON = os.environ.get("AUDIT", "1") == "1" and (not MEDIR or os.environ.get("AUDIT_MEDIR") == "1")
BAIXO = -4.85      # a legenda ocupa y ∈ [−6,3 ; −4,9] (montar_legendado, estilo padrão): nada da cena pode descer abaixo disto
FV = dict(yH=0.9, L=3.6, h=np.radians(20.0))         # vista de frente: horizonte, distância e altura do Sol do teaser


class ArcoIris025(Scene):
    """Rodada r6: voz + sincronização por âncoras (≤ 0,2 s de atraso), nova abertura, referencial dos 42° explícito."""

    scale = 1.0
    carry = 0.0
    clk = 0           # relógio próprio em quadros (igual ao do arquivo; o do Manim erra meio quadro por animação no modo MEDIR)
    _raw = False
    scene_name = "C01"
    audit_log = None

    # ------------------------------------------------------------------ relógio em quadros
    def frame_now(self):
        return self.clk

    def play(self, *args, run_time=None, **kwargs):
        if self._raw:                         # chamada interna do Scene.wait: não reescalar
            return super().play(*args, **kwargs)
        rt = 1.0 if run_time is None else run_time
        x = rt * FPS * self.scale + self.carry
        q = max(1, int(np.floor(x + 0.5)))
        self.carry = x - q
        self.clk += q
        return super().play(*args, run_time=(q - 0.5) / FPS, **kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        x = duration * FPS * self.scale + self.carry
        q = int(np.floor(x + 0.5))
        if q <= 0:
            self.carry = x
            return
        self.carry = x - q
        if AUDIT_ON:
            self.audit()
        self.clk += q
        self._raw = True
        try:
            return super().wait((q + 0.5) / FPS, *args, **kwargs)
        finally:
            self._raw = False

    def _pad(self, frames):
        """Espera exata de `frames` quadros (voz à frente da imagem)."""
        if frames >= 1:
            if AUDIT_ON:
                self.audit()
            self.clk += frames
            self._raw = True
            try:
                super().wait((frames + 0.5) / FPS)
            finally:
                self._raw = False

    def sync(self, name):
        """Marca o início do evento visual ligado à frase `name` da voz."""
        if AUDIT_ON:
            self.audit()                 # estado de leitura ao fim do trecho anterior
        self.scene_name = name
        now = self.frame_now()
        if MEDIR:
            self.nat[name] = round(now / FPS, 4)
            self.scale, self.carry = 1.0, 0.0
            return
        if SY is None:                       # sem plano de sincronização: pré-visualização livre
            self.scale, self.carry = 0.8, 0.0
            return
        target = max(0, int(round((SY["T"][name] - (0.0 if name == "fim" else LEAD)) * FPS)))
        if now < target:
            self._pad(target - now)
            now = self.frame_now()
        self.arr[name] = round(now / FPS, 3)
        self.late[name] = round(now / FPS - SY["T"][name], 3)
        order = SY["order"]
        i = order.index(name)
        if i + 1 < len(order):
            nxt = order[i + 1]
            t_next = max(0, int(round((SY["T"][nxt] - LEAD) * FPS)))
            avail = (t_next - now) / FPS
            nat = SY["NAT"][nxt] - SY["NAT"][name]
            self.scale = float(np.clip(avail / nat, 0.3, SMAX)) if nat > 1e-6 else 1.0
        self.carry = 0.0

    def finish(self):
        if MEDIR:
            (UNIT / "nat.json").write_text(json.dumps(self.nat, indent=1), encoding="utf-8")
        else:
            (UNIT / "chegada.json").write_text(json.dumps(dict(arr=self.arr, late=self.late, frames=self.clk, renderer_frames=int(round(self.renderer.time * FPS))), indent=1), encoding="utf-8")

    # ------------------------------------------------------------------ auditoria de sobreposição
    def audit(self):
        """Confere, num estado de leitura (pausa), texto×texto, texto×traço, limites do quadro e faixa inferior reservada."""
        t_now = self.renderer.time
        texts = [t for t in _text_units(self.mobjects) if t.get_fill_opacity() >= 0.3 and t.width > 1e-3]
        issues = []
        boxes = [(t, _bbox(t)) for t in texts]
        for i in range(len(boxes)):
            ti, bi = boxes[i]
            if bi[0] < -4.48 or bi[1] > 4.48 or bi[3] > 7.9:
                issues.append(f"FORA DO QUADRO: '{_name(ti)}' x[{bi[0]:.2f},{bi[1]:.2f}] y[{bi[2]:.2f},{bi[3]:.2f}]")
            if bi[2] < BAIXO:
                issues.append(f"FAIXA DA LEGENDA: '{_name(ti)}' y_min={bi[2]:.2f}")
            for j in range(i + 1, len(boxes)):
                tj, bj = boxes[j]
                ox = min(bi[1], bj[1]) - max(bi[0], bj[0])
                oy = min(bi[3], bj[3]) - max(bi[2], bj[2])
                if ox > 0.02 and oy > 0.02:
                    issues.append(f"TEXTO×TEXTO: '{_name(ti)}' ~ '{_name(tj)}' ({ox:.2f}×{oy:.2f})")
        strokes = _stroke_leaves(self.mobjects)
        if texts and strokes:
            samples = []
            for s in strokes:
                try:
                    samples.append((s, _sample(s)))
                except Exception:
                    pass
            for t, b in boxes:
                hits, leaves, worst = {}, 0, 0
                for s, P in samples:
                    if len(P) == 0:
                        continue
                    inside = int(((P[:, 0] > b[0]) & (P[:, 0] < b[1]) & (P[:, 1] > b[2]) & (P[:, 1] < b[3])).sum())
                    if inside >= 1:
                        leaves += 1
                        worst = max(worst, inside)
                        hits[type(s).__name__] = hits.get(type(s).__name__, 0) + inside
                if worst >= 3 or leaves >= 3:
                    issues.append(f"TEXTO×TRAÇO: '{_name(t)}' cruzado por {hits}")
        def folhas(ms):
            for m in ms:
                if getattr(m, "audit_bottom_ok", False) or isinstance(m, ImageMobject):
                    continue
                if isinstance(m, VMobject) and not m.submobjects and m.get_num_points() > 0:
                    yield m
                else:
                    yield from folhas(m.submobjects)
        for m in folhas(self.mobjects):
            if m.get_stroke_opacity() >= 0.25 and m.get_stroke_width() >= 1.0 or m.get_fill_opacity() >= 0.25:
                if m.get_bottom()[1] < BAIXO and m.get_top()[1] > -8:
                    issues.append(f"DESENHO NA FAIXA DA LEGENDA: {type(m).__name__} y_min={m.get_bottom()[1]:.2f}")
                    break
        seen = getattr(self, "_seen", set())
        for msg in issues:
            key = (self.scene_name, msg)
            if key in seen:
                continue
            seen.add(key)
            print(f"AUDIT [{key[0]} t={t_now:.1f}s] {msg}")
        self._seen = seen

    # ------------------------------------------------------------------ utilidades de cena
    def heading(self, title, sub=None, run_time=0.8):
        new = words(title, 30).move_to([0, 6.3, 0])
        newsub = words(sub, 20, DIM).move_to([0, 5.6, 0]) if sub else VGroup()
        out = [FadeOut(self.title, shift=UP * 0.08), FadeOut(self.subtitle)]
        inc = [FadeIn(new, shift=UP * 0.08), FadeIn(newsub)]
        self.play(Succession(AnimationGroup(*out), AnimationGroup(*inc)), run_time=run_time)
        self.title, self.subtitle = new, newsub

    def subline(self, sub, run_time=0.5):
        new = words(sub, 20, DIM).move_to([0, 5.6, 0])
        self.play(Succession(FadeOut(self.subtitle), FadeIn(new)), run_time=run_time)
        self.subtitle = new

    def caption(self, *texts, y=-4.25, t2c=None, size=22, color=INK, run_time=0.5):
        """Legenda didática (1–3 linhas): sai a anterior, depois entra a nova (nunca dois textos juntos)."""
        new = lines(*texts, size=size, color=color, t2c=t2c).move_to([0, y, 0])
        old = getattr(self, "cap", None)
        if old is not None and len(old):
            self.play(Succession(FadeOut(old), FadeIn(new, shift=UP * 0.06)), run_time=run_time)
        else:
            self.play(FadeIn(new, shift=UP * 0.06), run_time=run_time)
        self.cap = new
        return new

    def clear_caption(self, run_time=0.4):
        old = getattr(self, "cap", None)
        if old is not None and len(old):
            self.play(FadeOut(old), run_time=run_time)
        self.cap = VGroup()

    def morph(self, old, new, pairs, run_time=1.0, extra=(), keep_old=False):
        """Transição com correspondência explícita de termos (índices de partes)."""
        used_o, used_n, anims, wrappers = set(), set(), [], []
        for o_idx, n_idx in pairs:
            o_idx = [o_idx] if isinstance(o_idx, int) else list(o_idx)
            n_idx = [n_idx] if isinstance(n_idx, int) else list(n_idx)
            src = VGroup(*[old[i] for i in o_idx]).copy() if keep_old else VGroup(*[old[i] for i in o_idx])
            dst = VGroup(*[new[j] for j in n_idx])
            wrappers.append(dst)
            anims.append(ReplacementTransform(src, dst))
            used_o |= set(o_idx)
            used_n |= set(n_idx)
        if not keep_old:
            anims += [FadeOut(old[i]) for i in range(len(old)) if i not in used_o]
        anims += [FadeIn(new[j]) for j in range(len(new)) if j not in used_n]
        self.play(*anims, *extra, run_time=run_time)
        self.remove(*wrappers)
        if not keep_old:
            self.remove(old)
        self.add(new)
        return new

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        if MEDIR:                       # só mede: pula todas as animações (o relógio em quadros continua exato)
            config.from_animation_number = 10 ** 7
            self.renderer.skip_animations = True
        self.nat, self.arr, self.late = {}, {}, {}
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(wm.to_corner(UP + RIGHT, buff=0.28).set_z_index(60))
        tag = words("DA EQUAÇÃO AO FENÔMENO · EP. 07", 20, opacity=0.7).to_corner(UP + LEFT, buff=0.4)
        self.add(tag)
        self.title, self.subtitle, self.cap = VGroup(), VGroup(), VGroup()
        self.c01_gancho()
        self.c02_gota()
        self.c03_entrada()
        self.c04_reflexao_saida()
        self.c05_equacao()
        self.c06_leque_grafico()
        self.c07_amontoado()
        self.c08_maximo()
        self.c09_cores()
        self.c10_cone()
        self.c11_fechamento()
        self.sync("fim")
        if AUDIT_ON:
            self.audit()
        self.finish()

    # ------------------------------------------------------------------ geometria do céu (compartilhada)
    @staticmethod
    def sky_geometry(E, h, L, theta=None):
        """Vista lateral coerente: a = eixo antissolar, u = sua perpendicular, A = E + L·a (sombra da cabeça),
        T = A + L·tan θ·u → ângulo(A−E, T−E) = θ."""
        theta = np.radians(42.078107) if theta is None else theta
        a = np.array([np.cos(h), -np.sin(h), 0.0])
        u = np.array([np.sin(h), np.cos(h), 0.0])
        A = E + L * a
        T = A + L * np.tan(theta) * u
        return dict(a=a, u=u, L=L, A=A, T=T)

    # ------------------------------------------------------------------ C01 — gancho: o arco preso a um ângulo; 42° de quê?
    def c01_gancho(self):
        TH = np.radians(42.078107)
        yH, L10, h10 = FV["yH"], FV["L"], FV["h"]
        rho10 = L10 * np.tan(TH)
        C_fin = np.array([0.0, yH - L10 * np.tan(h10), 0.0])      # centro do arco = ponto antissolar
        top_fin = C_fin + UP * rho10

        # ---------------- teaser: o arco tenta outros lugares e trava a 42°
        self.sync("h1")
        headline = VGroup(words("POR QUE O ARCO-ÍRIS", 44), words("TEM 42°?", 44, t2c={"42°": CYAN}))
        headline.arrange(DOWN, buff=0.16).move_to([0, 5.2, 0])
        sky = VGroup(make_ground(yH, 4.4, BLUE, 7, 0.08), Line([-4.7, yH, 0], [4.7, yH, 0], color=DIM, stroke_width=2.2, stroke_opacity=0.9))
        skip_audit(sky)
        cx, cy, rr, op = ValueTracker(-1.7), ValueTracker(0.2), ValueTracker(1.7), ValueTracker(0.0)

        def bands(c_x, c_y, r0, opac, width=4.4, glow_color=None):
            g = VGroup()
            for k, col in enumerate(SPECTRUM):
                r = r0 * (1.024 - 0.0096 * k)
                run = []
                for t in np.linspace(0, PI, 150):
                    q = np.array([c_x + r * np.cos(t), c_y + r * np.sin(t), 0.0])
                    if q[1] >= yH - 1e-6:
                        run.append(q)
                if len(run) > 1:
                    g.add(polyline(run, color=glow_color or col, stroke_width=width, stroke_opacity=opac))
            return g

        arc_m = always_redraw(lambda: bands(cx.get_value(), cy.get_value(), rr.get_value(), op.get_value()))
        skip_audit(arc_m)
        self.add(arc_m)
        self.play(FadeIn(headline[0], shift=DOWN * 0.1), FadeIn(sky), op.animate.set_value(1.0), run_time=0.7)
        self.play(FadeIn(headline[1], shift=DOWN * 0.1), run_time=0.4)
        self.sync("h1b")      # "em qualquer lugar do céu": o arco tenta outros lugares
        self.play(cx.animate.set_value(1.9), cy.animate.set_value(-0.3), rr.animate.set_value(3.0), run_time=0.55)
        self.play(cx.animate.set_value(-0.3), cy.animate.set_value(1.7), rr.animate.set_value(2.0), run_time=0.55)
        self.sync("h2")       # "ele fica preso a um ângulo": trava no lugar certo
        self.play(cx.animate.set_value(0.0), cy.animate.set_value(float(C_fin[1])), rr.animate.set_value(rho10), run_time=0.7, rate_func=smooth)
        lock = bands(0.0, C_fin[1], rho10, 0.4, 15, CYAN)
        skip_audit(lock)
        self.play(FadeIn(lock), run_time=0.25)
        self.play(FadeOut(lock), run_time=0.45)
        self.sync("h2b")      # "cerca de quarenta e dois graus"
        lab42 = words("42°", 72, CYAN).move_to(top_fin + UP * 0.62)
        self.play(FadeIn(lab42, scale=0.6), run_time=0.6)
        self.sync("h3")       # "mas quarenta e dois graus..."
        self.play(Indicate(lab42, color=WARM, scale_factor=1.22), run_time=0.9)
        self.sync("h3b")      # "de quê?": o centro some do mapa — o ângulo precisa de uma referência
        radial = DashedLine(top_fin, C_fin, color=CYAN, stroke_width=2.6, dash_length=0.12, stroke_opacity=0.9)
        qring = Circle(radius=0.36, color=WARM, stroke_width=2.6).move_to(C_fin)
        qmark = words("?", 60, WARM).move_to(C_fin)
        skip_audit(radial, qring)
        self.play(Create(radial), FadeIn(qring, scale=0.5), FadeIn(qmark, scale=0.5), lab42.animate.move_to([0.62, 1.15, 0]).scale(0.62), run_time=0.9)

        # ---------------- vista lateral: Sol, você, a sombra, a linha antissolar
        h = np.radians(22.0)
        yg, eye_h, xo = -1.3, 1.5, -2.1
        E = np.array([xo, yg + eye_h, 0.0])
        geo = self.sky_geometry(E, h, eye_h / np.sin(h))
        a, u, L, A, T = geo["a"], geo["u"], geo["L"], geo["A"], geo["T"]
        self.sky = dict(h=h, yg=yg, E=E, A=A, T=T, L=L)
        measured = np.degrees(ang_between(A - E, T - E))
        assert abs(measured - 42.078107) < 1e-6, measured
        ground = VGroup(make_ground(yg, 1.1), Line([-4.7, yg, 0], [4.7, yg, 0], color=GEO, stroke_width=2.0, stroke_opacity=0.7))
        skip_audit(ground)
        person = make_person([xo, yg], H=eye_h)
        sun_c = E - 1.95 * a
        sun = make_sun(sun_c, 0.3)
        sun_lbl = words("SOL", 24, WARM).next_to(sun_c, UP, buff=0.62)
        you_lbl = words("VOCÊ", 24).move_to([xo, yg - 0.42, 0])
        self.sync("h4")       # "com o Sol nas costas"
        self.play(op.animate.set_value(0.0), FadeOut(sky), FadeOut(lab42), FadeOut(radial), FadeOut(qring), FadeOut(qmark), run_time=0.5)
        self.remove(arc_m)
        self.play(FadeIn(ground), FadeIn(person, shift=UP * 0.1), FadeIn(sun), FadeIn(sun_lbl), FadeIn(you_lbl), run_time=0.9)
        # luz do Sol: dois raios curtos e o raio que passa pela cabeça e termina na sombra da cabeça
        ray_kw = dict(color=WARM, stroke_width=2.4, buff=0, max_tip_length_to_length_ratio=0.12, stroke_opacity=0.85)
        ray_main = Line(sun_c + 0.42 * a, A, color=WARM, stroke_width=3.0, stroke_opacity=0.9)
        r_short = [Arrow(sun_c + 0.42 * a + off * u, sun_c + 1.45 * a + off * u, **ray_kw) for off in (0.42, -0.2)]
        foot = np.array([xo, yg, 0.0])
        shadow_body = Line(foot + RIGHT * 0.05, A, color=GEO, stroke_width=8, stroke_opacity=0.22)
        shadow_head = Circle(radius=0.12, color=INK, stroke_width=2.4, fill_color=INK, fill_opacity=0.28).move_to(A)
        shadow_lbl = words("SUA SOMBRA", 24).move_to(A + DOWN * 0.46)
        shadow_lbl.shift(LEFT * max(0.0, shadow_lbl.get_right()[0] - 4.3))
        skip_audit(ray_main, *r_short, shadow_body, shadow_head)
        self.sync("h4b")      # "trace uma linha"
        self.play(*[GrowArrow(r) for r in r_short], Create(ray_main), run_time=1.0)
        self.sync("h4c")      # "até a sombra dela"
        self.play(Create(shadow_body), FadeIn(shadow_head, scale=0.5), FadeIn(shadow_lbl), run_time=0.8)
        axis = Line(E, A, color=INK, stroke_width=3.2)
        axis_glow = glow_of(axis, INK, 11, 0.14)
        axis_lbl = words("DIREÇÃO ANTISSOLAR", 21).rotate(-h).move_to(0.5 * A + 0.5 * E - 0.38 * u)
        eye_dot = Dot(E, radius=0.05, color=CYAN).set_z_index(45)
        skip_audit(axis_lbl, axis_glow)
        self.sync("h5")       # "essa é a direção antissolar"
        self.play(Create(axis), FadeIn(axis_glow), FadeIn(axis_lbl), FadeIn(eye_dot), run_time=0.8)
        self.caption("A REFERÊNCIA: A DIREÇÃO ANTISSOLAR", "DO SOL, PELA SUA CABEÇA, ATÉ A SUA SOMBRA", t2c={"ANTISSOLAR": WARM}, y=-3.0, size=24, run_time=0.5)
        # a gota e o ângulo medido a partir da referência
        rng = np.random.default_rng(7)
        pts = []
        while len(pts) < 20:
            p = np.array([rng.uniform(0.5, 4.15), rng.uniform(-0.95, 2.25), 0.0])
            d_line = abs((T - E)[0] * (p - E)[1] - (T - E)[1] * (p - E)[0]) / np.linalg.norm((T - E)[:2])
            if d_line > 0.55 and np.linalg.norm(p - T) > 0.85 and all(np.linalg.norm(p - q) > 0.6 for q in pts):
                pts.append(p)
        rain = VGroup(*[make_drop(p, rng.uniform(0.045, 0.07), BLUE_L, 0.55) for p in pts])
        drop_hi = make_drop(T, 0.11, BLUE_L, 0.95)
        drop_ring = Circle(radius=0.3, color=CYAN, stroke_width=2.2).move_to(T + UP * 0.1)
        drop_lbl = words("UMA GOTA DE CHUVA", 21, CYAN).move_to(T + UP * 0.72)
        drop_lbl.shift(LEFT * max(0.0, drop_lbl.get_right()[0] - 4.35))
        sight = Line(E, T, color=CYAN, stroke_width=3.0)
        sight_glow = glow_of(sight, CYAN, 11, 0.16)
        light = Arrow(T, E, color=INK, stroke_width=3.2, buff=0.3, max_tip_length_to_length_ratio=0.06)
        ang42 = arc_between(E, A - E, T - E, 1.3, CYAN, 4.0)
        lbl42 = arc_label(E, A - E, T - E, 1.3, words("42°", 42, CYAN), pad=0.5)
        skip_audit(rain, drop_hi, drop_ring, sight_glow)
        self.sync("h5b")      # "e é dela que medimos o arco"
        self.play(FadeIn(rain, lag_ratio=0.05), FadeIn(drop_hi, scale=0.5), Create(drop_ring), FadeIn(drop_lbl), run_time=0.8)
        self.play(Create(sight), FadeIn(sight_glow), GrowArrow(light), run_time=0.7)
        self.play(Create(ang42), FadeIn(lbl42, scale=0.7), run_time=0.7)
        self.caption("OS 42° SÃO MEDIDOS A PARTIR DA DIREÇÃO ANTISSOLAR", "NÃO DO CHÃO, NÃO DO HORIZONTE", size=24,
                     t2c={"42°": CYAN, "ANTISSOLAR": WARM}, y=-3.0, run_time=0.5)
        self.c01_objs = dict(headline=headline, rain=rain, sun=sun, sun_lbl=sun_lbl, you_lbl=you_lbl, r_short=r_short, ray_main=ray_main,
                             shadow_lbl=shadow_lbl, axis_lbl=axis_lbl, drop_lbl=drop_lbl, drop_hi=drop_hi, drop_ring=drop_ring, light=light,
                             eye_dot=eye_dot, ground=ground, person=person, axis=axis, axis_glow=axis_glow, shadow_body=shadow_body,
                             shadow_head=shadow_head, ang42=ang42, lbl42=lbl42, sight=sight, sight_glow=sight_glow, T=T, h=h)

    # ------------------------------------------------------------------ C02 — a gota
    def c02_gota(self):
        c = self.c01_objs
        T, h = c["T"], c["h"]
        self.sync("c02")      # "tudo começa numa gota esférica"
        self.clear_caption(0.3)
        C2, R2 = np.array([0.4, 1.9, 0.0]), 2.2
        self.gota = Gota(C2, R2)
        g = self.gota
        tr = g.trace(0.861)
        rot = lambda p: np.array([np.cos(-h) * p[0] - np.sin(-h) * p[1], np.sin(-h) * p[0] + np.cos(-h) * p[1], 0.0])
        s = 0.15
        drop = Circle(radius=s, color=BLUE, stroke_width=2.2, fill_color=BLUE, fill_opacity=0.25).move_to(T)
        stub_in = Line(T + s * rot(tr["p0"]), T + s * rot(tr["P1"]), color=INK, stroke_width=2.4)
        stub_out = Line(T + s * rot(tr["P3"]), T + s * rot(tr["P3"] + 1.1 * tr["d3"]), color=INK, stroke_width=2.4)
        self.c01_exit_dir = rot(tr["d3"])          # conferência: deve apontar de T para E
        zoom_group = VGroup(drop, stub_in, stub_out).set_z_index(8)
        skip_audit(zoom_group)
        self.add(stub_in, stub_out)
        self.play(ReplacementTransform(c["drop_hi"], drop), FadeOut(c["drop_ring"]), FadeOut(c["light"]), FadeOut(c["eye_dot"]),
                  FadeOut(c["rain"]), FadeOut(c["sun"]), FadeOut(c["sun_lbl"]), FadeOut(c["r_short"][0]), FadeOut(c["r_short"][1]),
                  FadeOut(c["headline"]), FadeOut(c["drop_lbl"]), FadeOut(c["shadow_lbl"]), FadeOut(c["axis_lbl"]), FadeOut(c["you_lbl"]),
                  FadeOut(c["ray_main"]), run_time=0.6)
        rest = VGroup(c["ground"], c["person"], c["axis"], c["axis_glow"], c["shadow_body"], c["shadow_head"], c["ang42"], c["lbl42"], c["sight_glow"])
        self.play(FadeOut(rest), c["sight"].animate.set_stroke(opacity=0.4), run_time=0.5)
        self.play(zoom_group.animate.rotate(h, about_point=T).scale(R2 / s, about_point=T).shift(C2 - T), FadeOut(c["sight"]), run_time=1.4)

        self.sync("c02b")     # "atingida por raios de luz paralelos"
        circle = g.circle()
        center = Dot(g.C, radius=0.055, color=INK)
        axis = dashed([g.x_left, g.C[1], 0], g.C + RIGHT * (g.R + 0.5), GEO, 0.45)
        incident = Line(g.pt(tr["p0"]), g.pt(tr["P1"]), color=INK, stroke_width=2.8)
        drop, stub_in, stub_out = zoom_group
        self.play(ReplacementTransform(drop, circle), ReplacementTransform(stub_in, incident), FadeOut(stub_out), run_time=0.5)
        self.heading("A GOTA", "GOTA ESFÉRICA · LUZ PARALELA", run_time=0.7)
        par = VGroup(*[Line(g.pt(g.trace(x)["p0"]), g.pt(g.trace(x)["P1"]), color=INK, stroke_width=1.8, stroke_opacity=0.5)
                       for x in (0.45, -0.3, -0.7)])
        skip_audit(par)
        # b: altura de entrada do raio
        xb = -3.25
        yb = g.pt(tr["P1"])[1]
        bline = Line([xb, g.C[1], 0], [xb, yb, 0], color=GEO, stroke_width=2.4)
        ticks = VGroup(Line([xb - 0.1, g.C[1], 0], [xb + 0.1, g.C[1], 0], color=GEO, stroke_width=2.4),
                       Line([xb - 0.1, yb, 0], [xb + 0.1, yb, 0], color=GEO, stroke_width=2.4))
        b_lbl = math("b", size=50, color=GEO).next_to(bline, LEFT, buff=0.14)
        self.play(FadeIn(center), Create(axis), Create(par), run_time=0.7)
        self.play(Create(bline), FadeIn(ticks), FadeIn(b_lbl, scale=0.6), run_time=0.7)
        self.scene_objs = dict(circle=circle, center=center, axis=axis, incident=incident, par=par, bmark=VGroup(bline, ticks, b_lbl))
        self.tr = tr

    # ------------------------------------------------------------------ C03 — entrada (Snell)
    def c03_entrada(self):
        g, tr, o = self.gota, self.tr, self.scene_objs
        P1, N1 = g.pt(tr["P1"]), tr["N1"]
        self.sync("c03")      # "ao entrar na água, o raio se dobra:"
        self.heading("ENTRADA", "AO ENTRAR, O RAIO SE DOBRA: REFRAÇÃO", run_time=0.7)
        p1dot = Dot(P1, radius=0.07, color=INK)
        radius1 = Line(g.C, P1, color=GEO, stroke_width=1.6, stroke_opacity=0.5)
        normal1 = dashed(P1 - 1.25 * N1, P1 + 1.25 * N1, GEO, 0.65, 1.8)
        n_lbl = words("NORMAL", 18, GEO).next_to(P1 + 1.25 * N1, UP, buff=0.06)
        arc_i = arc_between(P1, -tr["d0"], N1, 0.72, VIOLET, 3.4)
        lbl_i = arc_label(P1, -tr["d0"], N1, 0.72, math("i", size=54, color=VIOLET), pad=0.34)
        self.play(FadeOut(o["par"]), VGroup(o["bmark"]).animate.set_opacity(0.3), FadeIn(p1dot, scale=0.5), Create(radius1), Create(normal1), FadeIn(n_lbl), run_time=0.7)
        self.play(Create(arc_i), FadeIn(lbl_i, scale=0.6), run_time=0.7)
        self.sync("c03b")     # "é a refração."
        chord1 = Line(P1, g.pt(tr["P2"]), color=INK, stroke_width=2.8)
        arc_r = arc_between(P1, tr["d1"], -N1, 0.72, PINK, 3.4)
        lbl_r = arc_label(P1, tr["d1"], -N1, 0.72, math("r", size=54, color=PINK), pad=0.34)
        self.play(Create(chord1), run_time=0.5)
        self.play(Create(arc_r), FadeIn(lbl_r, scale=0.6), run_time=0.6)
        # Snell nasce dos dois ângulos
        snell = math(r"\sin", "i", "=", "n", r"\sin", "r", size=60).move_to([0, -2.9, 0])
        snell[1].set_color(VIOLET); snell[5].set_color(PINK)
        note1 = words("LEI DE SNELL", 22, DIM).move_to([0, -3.75, 0])
        note2 = mix("LEI DE SNELL ·", ("n",), "= ÍNDICE DE REFRAÇÃO DA ÁGUA", size=20).move_to([0, -3.75, 0])
        self.sync("c03c")     # "pela lei de Snell,"
        self.play(FadeIn(note1), FadeOut(n_lbl), run_time=0.5)
        self.sync("c03d")     # "o seno do ângulo de incidência"
        self.play(FadeIn(snell[0]), TransformFromCopy(lbl_i, snell[1]), run_time=0.9)
        self.sync("c03e")     # "é o índice de refração da água"
        self.play(FadeIn(snell[2]), FadeIn(snell[3]), Succession(FadeOut(note1), FadeIn(note2)), run_time=0.8)
        self.sync("c03f")     # "vezes o seno do ângulo de refração."
        self.play(FadeIn(snell[4]), TransformFromCopy(lbl_r, snell[5]), run_time=0.9)
        self.wait(0.8)
        o.update(radius1=radius1, normal1=normal1, p1dot=p1dot, arc_i=arc_i, lbl_i=lbl_i, chord1=chord1, arc_r=arc_r, lbl_r=lbl_r,
                 snell=snell, note2=note2)

    # ------------------------------------------------------------------ C04 — reflexão e saída
    def c04_reflexao_saida(self):
        g, tr, o = self.gota, self.tr, self.scene_objs
        P1, P2, P3 = g.pt(tr["P1"]), g.pt(tr["P2"]), g.pt(tr["P3"])
        N2, N3 = tr["N2"], tr["N3"]
        self.sync("c04")      # "depois o raio reflete no fundo."
        self.heading("REFLEXÃO E SAÍDA", "UMA REFLEXÃO INTERNA", run_time=0.7)
        p2dot = Dot(P2, radius=0.07, color=INK)
        radius2 = Line(g.C, P2, color=GEO, stroke_width=1.6, stroke_opacity=0.5)
        normal2 = dashed(P2 - 1.0 * N2, P2 + 0.9 * N2, GEO, 0.65, 1.8)
        self.play(FadeOut(o["bmark"]), FadeOut(o["note2"]), o["snell"].animate.scale(0.6).move_to([-2.7, -2.9, 0]),
                  VGroup(o["arc_i"], o["lbl_i"], o["normal1"]).animate.set_opacity(0.4),
                  FadeIn(p2dot, scale=0.5), Create(radius2), Create(normal2), run_time=0.9)
        self.sync("c04b")     # "como dois lados do triângulo são raios da gota,"
        tri = Polygon(g.C, P1, P2, color=BLUE, fill_color=BLUE, fill_opacity=0.16, stroke_width=1.6, stroke_opacity=0.7)
        side1 = Line(g.C, P1, color=BLUE_L, stroke_width=3.4)
        side2 = Line(g.C, P2, color=BLUE_L, stroke_width=3.4)
        t1, t2 = tick_mark(side1, color=BLUE_L), tick_mark(side2, color=BLUE_L)
        R1 = math("R", size=40, color=BLUE_L).next_to(side1.get_center(), DOWN + LEFT, buff=0.1)
        R2 = math("R", size=40, color=BLUE_L).next_to(side2.get_center(), DOWN + RIGHT, buff=0.1)
        self.play(FadeIn(tri), Create(side1), Create(side2), run_time=0.7)
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(R1), FadeIn(R2), run_time=0.6)
        self.sync("c04c")     # "o ângulo ali volta a ser o de refração."
        arc_r2 = arc_between(P2, -tr["d1"], -N2, 0.62, PINK, 3.4)
        lbl_r2 = arc_label(P2, -tr["d1"], -N2, 0.62, math("r", size=54, color=PINK), pad=0.3)
        chord2 = Line(P2, P3, color=INK, stroke_width=2.8)
        arc_r3 = arc_between(P2, tr["d2"], -N2, 0.62, PINK, 3.4)
        lbl_r3 = arc_label(P2, tr["d2"], -N2, 0.62, math("r", size=54, color=PINK), pad=0.3)
        self.play(Indicate(o["arc_r"], color=PINK, scale_factor=1.2), TransformFromCopy(o["arc_r"], arc_r2), TransformFromCopy(o["lbl_r"], lbl_r2), run_time=0.9)
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(R1), FadeOut(R2), FadeOut(side1), FadeOut(side2),
                  tri.animate.set_fill(opacity=0.05).set_stroke(opacity=0.25), Create(chord2), run_time=0.7)
        self.play(TransformFromCopy(arc_r2, arc_r3), TransformFromCopy(lbl_r2, lbl_r3), run_time=0.6)
        self.sync("c04d")     # "na saída, volta ao ângulo de incidência."
        p3dot = Dot(P3, radius=0.07, color=INK)
        radius3 = Line(g.C, P3, color=GEO, stroke_width=1.6, stroke_opacity=0.5)
        normal3 = dashed(P3 - 1.0 * N3, P3 + 1.15 * N3, GEO, 0.65, 1.8)
        arc_r4 = arc_between(P3, -tr["d2"], -N3, 0.62, PINK, 3.4)
        lbl_r4 = arc_label(P3, -tr["d2"], -N3, 0.62, math("r", size=54, color=PINK), pad=0.3)
        exit_ray = Line(P3, P3 + 2.7 * tr["d3"], color=INK, stroke_width=2.8)
        arc_i2 = arc_between(P3, tr["d3"], N3, 0.72, VIOLET, 3.4)
        lbl_i2 = arc_label(P3, tr["d3"], N3, 0.72, math("i", size=54, color=VIOLET), pad=0.34)
        self.play(FadeIn(p3dot, scale=0.5), Create(radius3), Create(normal3), TransformFromCopy(arc_r3, arc_r4), TransformFromCopy(lbl_r3, lbl_r4), run_time=0.8)
        self.play(VGroup(o["arc_i"], o["lbl_i"]).animate.set_opacity(1.0), Create(exit_ray), run_time=0.6)
        self.play(TransformFromCopy(o["arc_i"], arc_i2), TransformFromCopy(o["lbl_i"], lbl_i2), run_time=0.8)
        self.wait(0.4)
        self.play(FadeOut(tri),
                  VGroup(arc_r2, lbl_r2, arc_r3, lbl_r3, arc_r4, lbl_r4, o["arc_r"], o["lbl_r"], arc_i2, lbl_i2, o["arc_i"], o["lbl_i"],
                         normal2, normal3, o["normal1"], radius2, radius3, o["radius1"]).animate.set_opacity(0.22), run_time=0.6)
        o.update(radius2=radius2, normal2=normal2, p2dot=p2dot, arc_r2=arc_r2, lbl_r2=lbl_r2, chord2=chord2, arc_r3=arc_r3,
                 lbl_r3=lbl_r3, radius3=radius3, normal3=normal3, p3dot=p3dot, arc_r4=arc_r4, lbl_r4=lbl_r4,
                 exit_ray=exit_ray, arc_i2=arc_i2, lbl_i2=lbl_i2)

    # ------------------------------------------------------------------ C05 — a equação nasce da geometria
    def c05_equacao(self):
        g, tr, o = self.gota, self.tr, self.scene_objs
        P1, P2, P3 = g.pt(tr["P1"]), g.pt(tr["P2"]), g.pt(tr["P3"])
        self.sync("c05")      # "agora somamos as três viradas."
        self.heading("SOMANDO AS VIRADAS", "QUANTO O RAIO GIRA EM CADA PASSO", run_time=0.7)
        eqD = math("D", "=", "(i-r)", "+", r"(180^\circ-2r)", "+", "(i-r)", size=46).move_to([0, -3.0, 0])
        for part in (eqD[2], eqD[6]):
            part[1].set_color(VIOLET); part[3].set_color(PINK)
        eqD[4][-2:].set_color(PINK)
        dnote = mix(("D",), "= DESVIO TOTAL DO RAIO", size=20).move_to([0, -3.85, 0])
        self.play(Succession(FadeOut(o["snell"]), AnimationGroup(FadeIn(eqD[0]), FadeIn(eqD[1]), FadeIn(dnote))), run_time=0.6)

        def turn(P, d_prev, d_new, label_parts, colors, ext=1.0, radius=0.78, pad=0.36, lbl_shift=ORIGIN):
            ext_line = dashed(P, P + ext * d_prev, GEO, 0.7, 1.8)
            arc = arc_between(P, d_prev, d_new, radius, CYAN, 3.2).add_tip(tip_length=0.16, tip_width=0.12)
            lbl = paint(math(*label_parts, size=40), colors)
            arc_label(P, d_prev, d_new, radius, lbl, pad=pad)
            lbl.shift(lbl_shift)
            lbl.add_background_rectangle(color=BACKGROUND_COLOR, opacity=0.75, buff=0.05)
            return ext_line, arc, lbl

        e1, a1, l1 = turn(P1, tr["d0"], tr["d1"], ("i", "-", "r"), {"i": VIOLET, "r": PINK}, ext=1.2, radius=0.95, lbl_shift=RIGHT * 0.55 + UP * 0.12)
        e3, a3, l3 = turn(P3, tr["d2"], tr["d3"], ("i", "-", "r"), {"i": VIOLET, "r": PINK}, ext=1.1, radius=0.95, lbl_shift=RIGHT * 0.5 + DOWN * 0.15)
        e2, a2, l2 = turn(P2, tr["d1"], tr["d2"], (r"180^\circ", "-", "2r"), {"2r": PINK}, ext=1.0, radius=0.95, pad=0.42, lbl_shift=RIGHT * 0.1 + DOWN * 0.1)
        self.sync("c05a")     # "na entrada e na saída, a virada é incidência menos refração;"
        self.play(Create(e1), Create(e3), run_time=0.4)
        self.play(Create(a1), Create(a3), run_time=0.6)
        self.play(FadeIn(l1, scale=0.6), FadeIn(l3, scale=0.6), run_time=0.4)
        self.play(TransformFromCopy(l1[1:], eqD[2]), TransformFromCopy(l3[1:], eqD[6]), FadeIn(eqD[3]), FadeIn(eqD[5]), run_time=0.9)
        self.play(VGroup(e1, a1, e3, a3).animate.set_opacity(0.35), run_time=0.3)
        self.sync("c05b")     # "na reflexão, cento e oitenta graus menos duas vezes a refração."
        self.play(Create(e2), run_time=0.4)
        self.play(Create(a2), run_time=0.6)
        self.play(FadeIn(l2, scale=0.6), run_time=0.4)
        self.play(TransformFromCopy(l2[1:], eqD[4]), run_time=0.9)
        self.play(VGroup(e2, a2).animate.set_opacity(0.35), run_time=0.3)
        self.sync("c05c")     # "o desvio total é cento e oitenta graus mais duas vezes a incidência..."
        eqD2 = math("D", "=", r"180^\circ", "+", "(i+i)", "-", "(r+2r+r)", size=46).move_to([0, -3.0, 0])
        eqD2[4][1].set_color(VIOLET); eqD2[4][3].set_color(VIOLET)
        for k in (1, 3, 4, 6):
            eqD2[6][k].set_color(PINK)
        self.play(FadeOut(dnote), run_time=0.3)
        self.morph(eqD, eqD2, [(0, 0), (1, 1), (4, 2), (3, 3), ([2, 6], 4), (5, 5)], run_time=1.2)
        self.play(Indicate(eqD2[4], color=VIOLET, scale_factor=1.15), run_time=0.55)
        self.play(Indicate(eqD2[6], color=PINK, scale_factor=1.15), run_time=0.55)
        eqD3 = math("D", "=", r"180^\circ", "+", "2i", "-", "4r", size=48).move_to([0, -3.0, 0])
        eqD3[4].set_color(VIOLET); eqD3[6].set_color(PINK)
        self.morph(eqD2, eqD3, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], run_time=0.9)
        self.wait(0.5)
        # D e θ são suplementares (direção paralela ao raio que chegou)
        self.sync("c05d")     # "medindo da direção antissolar:"
        ref = dashed(P3 + LEFT * 4.8, P3 + RIGHT * 1.7, GEO, 0.65, 1.8)
        ref_lbl = lines("PARALELA AO", "RAIO QUE CHEGOU", size=16, color=GEO, gap=0.05).move_to([-3.15, P3[1] + 0.42, 0])
        arc_D = arc_between(P3, tr["d0"], tr["d3"], 1.4, INK, 2.0, 0.6)
        lbl_D = arc_label(P3, tr["d0"], tr["d3"], 1.4, math("D", size=40, color=INK, max_width=1), pad=0.28)
        arc_th = arc_between(P3, tr["d3"], -tr["d0"], 1.4, CYAN, 3.6)
        lbl_th = arc_label(P3, tr["d3"], -tr["d0"], 1.4, math(r"\theta", size=52, color=CYAN), pad=0.32)
        eqT = math(r"\theta", "=", r"180^\circ", "-", "D", size=48).move_to([0, -4.3, 0])
        eqT[0].set_color(CYAN)
        self.play(FadeOut(VGroup(e1, a1, l1, e2, a2, l2, e3, a3, l3)), Create(ref), FadeIn(ref_lbl), run_time=0.5)
        self.play(Create(arc_D), FadeIn(lbl_D), Create(arc_th), FadeIn(lbl_th), run_time=0.8)
        self.play(TransformFromCopy(lbl_th, eqT[0]), FadeIn(eqT[1:]), run_time=0.8)
        self.sync("c05e")     # "o ângulo do arco é quatro vezes a refração menos duas vezes a incidência."
        eqT2 = math(r"\theta", "=", r"180^\circ", "-", "(", r"180^\circ", "+", "2i", "-", "4r", ")", size=44).move_to([0, -4.3, 0])
        eqT2[0].set_color(CYAN); eqT2[7].set_color(VIOLET); eqT2[9].set_color(PINK)
        self.play(ReplacementTransform(eqT[0], eqT2[0]), ReplacementTransform(eqT[1], eqT2[1]), ReplacementTransform(eqT[2], eqT2[2]),
                  ReplacementTransform(eqT[3], eqT2[3]), FadeOut(eqT[4]), FadeIn(eqT2[4]), FadeIn(eqT2[10]),
                  TransformFromCopy(VGroup(*eqD3[2:7]), VGroup(*eqT2[5:10])), run_time=1.1)
        self.remove(eqT); self.add(eqT2)
        eqT3 = math(r"\theta", "=", r"180^\circ", "-", r"180^\circ", "-", "2i", "+", "4r", size=44).move_to([0, -4.3, 0])
        eqT3[0].set_color(CYAN); eqT3[6].set_color(VIOLET); eqT3[8].set_color(PINK)
        self.play(Indicate(eqT2[3], color=CYAN, scale_factor=1.5), run_time=0.5)
        self.morph(eqT2, eqT3, [(0, 0), (1, 1), (2, 2), (3, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8)], run_time=1.0)
        strike = Line(eqT3[2].get_left() + DOWN * 0.08, eqT3[4].get_right() + UP * 0.08, color=CYAN, stroke_width=2.6)
        skip_audit(strike)
        self.play(Create(strike), run_time=0.4)
        eqF = math(r"\theta", "=", "4r", "-", "2i", size=58).move_to([0, -4.3, 0])
        eqF[0].set_color(CYAN); eqF[2].set_color(PINK); eqF[4].set_color(VIOLET)
        self.play(FadeOut(strike), FadeOut(eqD3), FadeOut(arc_D), FadeOut(lbl_D), FadeOut(ref_lbl), run_time=0.4)
        self.morph(eqT3, eqF, [(0, 0), (1, 1), (8, 2), (5, 3), (6, 4)], run_time=1.0)
        pnl = panel(eqF, pad=0.25)
        self.play(FadeIn(pnl), Indicate(eqF, color=CYAN, scale_factor=1.06), run_time=0.7)
        o.update(ref=ref, arc_th=arc_th, lbl_th=lbl_th, eqF=VGroup(eqF, pnl))


    # ------------------------------------------------------------------ C06 — o leque + gráfico
    def make_axes(self, center=(0.2, -3.2), x_length=5.6, y_length=3.6, label_size=30):
        ax = Axes(x_range=[0, 1.0001, 0.25], y_range=[0, 50, 10], x_length=x_length, y_length=y_length,
                  axis_config=dict(color=DIM, stroke_width=1.6, include_ticks=True, tick_size=0.06, include_numbers=False), tips=False)
        ax.move_to([*center, 0])
        skip_audit(ax)
        xl = math("b/R", size=label_size, color=INK).next_to(ax.x_axis.get_end(), RIGHT, buff=0.12).shift(DOWN * 0.05)
        yl = math(r"\theta", size=label_size + 4, color=CYAN).next_to(ax.y_axis.get_end(), RIGHT, buff=0.15)
        xt = VGroup(*[math(s, size=24, color=DIM).next_to(ax.c2p(v, 0), DOWN, buff=0.12) for v, s in ((0, "0"), (0.5, "0{,}5"), (1, "1"))])
        yt = VGroup(*[math(s, size=24, color=DIM).next_to(ax.c2p(0, v), LEFT, buff=0.12) for v, s in ((0, "0^\\circ"), (20, "20^\\circ"), (40, "40^\\circ"))])
        return ax, VGroup(xl, yl, xt, yt)

    def c06_leque_grafico(self):
        o = self.scene_objs
        f = lambda x: theta_deg_from_b_ratio(x, N_WATER)
        self.sync("c06")      # "só que há raios entrando em todas as alturas da gota."
        self.heading("UM RAIO VIRA UMA FAMÍLIA", "O SOL MANDA RAIOS EM TODAS AS ALTURAS", run_time=0.7)
        g_old = self.gota
        g = Gota([1.1, 2.75, 0], 1.65)
        self.gota = g
        k = g.R / g_old.R
        keep = VGroup(o["circle"], o["center"], o["axis"], o["incident"], o["chord1"], o["chord2"], o["exit_ray"])
        gone = VGroup(*[o[kk] for kk in ("radius1", "normal1", "p1dot", "arc_i", "lbl_i", "arc_r", "lbl_r", "radius2", "normal2", "p2dot",
                                          "arc_r2", "lbl_r2", "arc_r3", "lbl_r3", "radius3", "normal3", "p3dot", "arc_r4", "lbl_r4",
                                          "arc_i2", "lbl_i2", "ref", "arc_th", "lbl_th")])
        ax, ax_labels = self.make_axes(x_length=5.4)
        self.play(FadeOut(gone), keep.animate.scale(k, about_point=g_old.C).shift(g.C - g_old.C),
                  o["eqF"].animate.scale(0.72).move_to([-2.6, 0.55, 0]), run_time=1.1)
        axis = dashed([g.x_left, g.C[1], 0], g.C + RIGHT * (g.R + 0.4), GEO, 0.4)
        self.remove(o["axis"]); self.add(axis)
        self.play(Create(ax), FadeIn(ax_labels), FadeOut(o["incident"]), FadeOut(o["chord1"]), FadeOut(o["chord2"]), FadeOut(o["exit_ray"]), run_time=0.9)
        self.sync("c06b")     # "o do centro volta pelo mesmo caminho."
        tr0 = g.trace(0.0)
        ray0 = g.ray_lines(tr0, exit_len=2.2, color=CYAN, width=2.6)
        back0 = Arrow(g.pt(tr0["P3"]), g.pt(tr0["P3"]) + 2.2 * tr0["d3"], color=CYAN, stroke_width=2.6, buff=0,
                      max_tip_length_to_length_ratio=0.08).shift(DOWN * 0.08)
        dot0 = Dot(ax.c2p(0, 0), radius=0.08, color=CYAN)
        lbl0 = paint(math("b/R = 0", r"\;\Rightarrow\;", r"\theta = 0", size=34), {r"\theta = 0": CYAN}).move_to([-2.4, -0.55, 0])
        self.play(Create(ray0[0]), Create(ray0[1]), Create(ray0[2]), run_time=0.7)
        self.play(GrowArrow(back0), FadeIn(lbl0), FadeIn(dot0, scale=0.5), run_time=0.7)
        self.wait(0.4)
        self.play(FadeOut(ray0), FadeOut(back0), FadeOut(lbl0), run_time=0.4)
        # varredura: o mesmo tracker move raio, guia de b/R, ponto e curva
        xt = ValueTracker(0.0)
        proto = always_redraw(lambda: g.ray_lines(g.trace(max(xt.get_value(), 1e-6)), exit_len=2.3, color=CYAN, width=2.6))
        xg = -3.7
        guide = always_redraw(lambda: Line([xg, g.C[1], 0], [xg, g.C[1] + g.R * xt.get_value(), 0], color=CYAN, stroke_width=2.2))
        gval = DecimalNumber(0, num_decimal_places=2, font_size=28, color=CYAN)
        gval.add_updater(lambda m: m.set_value(xt.get_value()).next_to(guide, LEFT, buff=0.08).shift(UP * 0.1))
        glbl = math("b/R", size=24, color=CYAN)
        glbl.add_updater(lambda m: m.next_to(gval, DOWN, buff=0.06))
        pdot = always_redraw(lambda: Dot(ax.c2p(xt.get_value(), f(xt.get_value())), radius=0.08, color=CYAN))
        curve_live = always_redraw(lambda: ax.plot(f, x_range=[0, max(xt.get_value(), 1e-3), 0.004], color=CYAN, stroke_width=2.8))
        up_lbl = words("CRESCE", 20, CYAN).move_to(ax.c2p(0.38, 38))
        max_lbl = words("MÁXIMO", 20, CYAN).move_to(ax.c2p(0.80, 49))
        down_lbl = words("CAI", 20, CYAN).move_to(ax.c2p(1.04, 30))
        self.sync("c06c")     # "subindo a altura, o ângulo de saída cresce..."
        self.add(proto, guide, gval, glbl, pdot, curve_live)
        self.play(FadeOut(dot0), xt.animate.set_value(0.80), FadeIn(up_lbl), run_time=2.3, rate_func=linear)
        self.sync("c06d")     # "cresce menos..."
        self.play(xt.animate.set_value(0.861), run_time=1.0, rate_func=linear)
        self.sync("c06e")     # "chega a um máximo..."
        self.play(FadeIn(max_lbl, scale=0.7), Indicate(pdot, color=WARM, scale_factor=1.8), run_time=0.7)
        self.sync("c06f")     # "e cai."
        self.play(xt.animate.set_value(1.0), FadeIn(down_lbl), run_time=0.6, rate_func=linear)
        curve = ax.plot(f, x_range=[0, 1, 0.002], color=CYAN, stroke_width=2.8)
        self.remove(proto, pdot, curve_live, guide, gval, glbl)
        self.add(curve)
        self.play(FadeOut(up_lbl), FadeOut(max_lbl), FadeOut(down_lbl), FadeOut(o["eqF"]), run_time=0.3)
        self.scene_objs = dict(circle=o["circle"], center=o["center"], axis=axis, ax=ax, ax_labels=ax_labels, curve=curve)

    # ------------------------------------------------------------------ C07 — o amontoado
    def c07_amontoado(self):
        g, o = self.gota, self.scene_objs
        ax = o["ax"]
        f = lambda x: theta_deg_from_b_ratio(x, N_WATER)
        th_max = f(np.sin(i_max(N_WATER)))
        self.sync("c07")      # "e esse máximo é o segredo."
        self.heading("O AMONTOADO", "25 RAIOS · CADA UM COM A MESMA ÁREA", run_time=0.7)
        graph = VGroup(ax, o["ax_labels"], o["curve"])
        self.play(graph.animate.scale(0.66).move_to([2.45, -3.5, 0]), run_time=0.9)
        self.sync("c07b")     # "perto dele, raios que entram em regiões bem diferentes saem quase na mesma direção:"
        fan = VGroup(*[g.ray_lines(g.trace(x), exit_len=2.3, color=INK, width=1.3, opacity=0.6) for x in XS25])
        dots = VGroup(*[Dot(ax.c2p(x, f(x)), radius=0.034, color=INK) for x in XS25])
        seqs = [Succession(Create(r[0], run_time=0.25), Create(r[1], run_time=0.2), Create(r[2], run_time=0.2), Create(r[3], run_time=0.25),
                           FadeIn(d, scale=0.4, run_time=0.15)) for r, d in zip(fan, dots)]
        self.play(LaggedStart(*seqs, lag_ratio=0.18), run_time=4.6)
        others = VGroup(*[fan[k] for k in range(N_SAMPLES) if k not in CLUSTER_IDX])
        odots = VGroup(*[dots[k] for k in range(N_SAMPLES) if k not in CLUSTER_IDX])
        five = [fan[k] for k in CLUSTER_IDX]
        fdots = [dots[k] for k in CLUSTER_IDX]
        self.sync("c07c")     # "eles se amontoam."
        halos = VGroup(*[r[3].copy().set_stroke(CYAN, width=8, opacity=0.22).set_z_index(1) for r in five])
        skip_audit(halos)
        self.play(others.animate.set_stroke(opacity=0.12), odots.animate.set_opacity(0.3),
                  *[r[0].animate.set_stroke(INK, width=1.8, opacity=0.95) for r in five],
                  *[VGroup(r[1], r[2], r[3]).animate.set_stroke(CYAN, width=2.4, opacity=1.0) for r in five],
                  *[d.animate.set_color(CYAN).scale(1.5) for d in fdots], FadeIn(halos), run_time=0.9)
        # detalhe angular (×10): cópias paralelas das direções de saída numa origem comum
        O = np.array([-0.5, -1.25, 0.0])
        K = 10.0
        shown = [k for k, x in enumerate(XS25) if f(x) >= 36.0]

        def det_dir(th):
            ang = np.radians(180.0 + th_max + (th - th_max) * K)
            return np.array([np.cos(ang), np.sin(ang), 0.0])

        RL = 3.1
        wedge = Sector(radius=RL, start_angle=np.radians(180 + th_max - K), angle=np.radians(K),
                       arc_center=O, fill_color=CYAN, fill_opacity=0.3, stroke_opacity=0)
        det_rays = VGroup()
        for k in shown:
            col, w, opa = (CYAN, 3.0, 1.0) if k in CLUSTER_IDX else (INK, 1.4, 0.5)
            det_rays.add(Line(O, O + RL * det_dir(f(XS25[k])), color=col, stroke_width=w, stroke_opacity=opa))
        ref_dir = Line(O, O + RL * np.array([-1, 0, 0]), color=GEO, stroke_width=1.2, stroke_opacity=0.5)
        det_title = lines("DETALHE DAS DIREÇÕES DE SAÍDA · ÂNGULOS ×10", "LINHA CINZA = DIREÇÃO ANTISSOLAR", "SÓ AS DIREÇÕES, NÃO NOVOS TRAJETOS",
                          size=15, color=DIM, gap=0.07, max_width=4.4).move_to([-2.2, -4.3, 0])
        win_lbl = lines("JANELA DE 1°", "ABAIXO DO MÁXIMO", size=16, color=CYAN, gap=0.05).move_to([-0.95, -3.55, 0])
        skip_audit(wedge)
        copies = VGroup(*[r[3].copy() for r in five])
        self.sync("c07d")     # "no modelo geométrico,"
        self.play(FadeIn(det_title), Create(ref_dir), FadeIn(wedge), run_time=0.9)
        self.sync("c07e")     # "cerca de um em cada cinco"
        count = words("5 DE 25", 42, CYAN).move_to([2.5, 0.25, 0])
        count2 = words("≈ UM EM CADA CINCO", 24, INK, max_width=3.7).next_to(count, DOWN, buff=0.1)
        count3 = lines("RAIOS NO MODELO GEOMÉTRICO,", "A MENOS DE 1° DO MÁXIMO", size=15, color=DIM, gap=0.06, max_width=3.7).next_to(count2, DOWN, buff=0.12)
        self.play(ReplacementTransform(copies, VGroup(*[det_rays[j] for j, k in enumerate(shown) if k in CLUSTER_IDX])),
                  FadeIn(VGroup(*[det_rays[j] for j, k in enumerate(shown) if k not in CLUSTER_IDX])), run_time=1.1)
        self.play(FadeIn(count, scale=0.8), FadeIn(count2, shift=UP * 0.1), FadeIn(count3), FadeIn(win_lbl), run_time=0.9)
        self.sync("c07f")     # "a menos de um grau do máximo,"
        top_line = DashedLine(ax.c2p(0, th_max), ax.c2p(1, th_max), color=CYAN, stroke_width=1.6, dash_length=0.08, stroke_opacity=0.85)
        band = Polygon(ax.c2p(CLUSTER_LO, th_max - 1), ax.c2p(CLUSTER_HI, th_max - 1), ax.c2p(CLUSTER_HI, th_max), ax.c2p(CLUSTER_LO, th_max),
                       fill_color=CYAN, fill_opacity=0.3, stroke_opacity=0)
        skip_audit(band)
        self.play(Create(top_line), FadeIn(band), Indicate(win_lbl, color=CYAN, scale_factor=1.1), run_time=0.9)
        self.sync("c07g")     # "e nenhum passa dele."
        lim = paint(math(r"\theta", r"\le", r"42{,}1^\circ", size=38), {r"\theta": CYAN, r"42{,}1^\circ": CYAN})
        lim_note = mix("TETO PARA", ("n = 1{,}333",), size=17)
        none_note = words("NENHUM RAIO PASSA DO TETO", 16, DIM)
        VGroup(lim, lim_note, none_note).arrange(DOWN, buff=0.08).move_to([2.5, -1.75, 0])
        self.play(FadeIn(lim), FadeIn(lim_note), FadeIn(none_note), run_time=0.8)
        self.wait(0.5)
        o.update(graph=graph, halos=halos, fan=fan, dots=dots, det=VGroup(det_title, ref_dir, wedge, det_rays, win_lbl),
                 counts=VGroup(count, count2, count3), top_line=top_line, band=band, lim=VGroup(lim, lim_note, none_note))

    # ------------------------------------------------------------------ C08 — quanto vale o máximo?
    def c08_maximo(self):
        o = self.scene_objs
        ax = o["ax"]
        f = lambda x: theta_deg_from_b_ratio(x, N_WATER)
        im_ = i_max(N_WATER)
        xm = float(np.sin(im_))
        th_max = f(xm)
        self.sync("c08")      # "quanto vale esse máximo?"
        self.heading("QUANTO VALE O MÁXIMO?", "NO TOPO, A CURVA FICA PLANA", run_time=0.6)
        gone = VGroup(o["circle"], o["center"], o["axis"], o["fan"], o["halos"], o["det"], o["counts"], o["lim"], o["band"], o["dots"])
        graph = VGroup(o["graph"], o["top_line"])
        self.play(FadeOut(gone), run_time=0.5)
        self.play(graph.animate.scale(1 / 0.66 * 0.86).move_to([0.0, 2.75, 0]), run_time=0.8)
        pmax = ax.c2p(xm, th_max)
        tangent = Line(pmax + LEFT * 1.2, pmax + RIGHT * 1.2, color=CYAN, stroke_width=2.4)
        mdot = Dot(pmax, radius=0.09, color=CYAN)
        xdrop = DashedLine(pmax, ax.c2p(xm, 0), color=CYAN, stroke_width=1.0, dash_length=0.06, stroke_opacity=0.6)
        xlbl = math("0{,}861", size=26, color=CYAN).next_to(ax.c2p(xm, 0), DOWN, buff=0.12).shift(LEFT * 0.2)
        self.play(FadeOut(o["top_line"]), Create(tangent), FadeIn(mdot, scale=0.5), Create(xdrop), FadeIn(xlbl), run_time=0.8)

        Y1, Y2, YN = -0.55, -1.75, -2.75   # relação principal, relação de apoio, nota

        def nt(obj):
            return obj.move_to([0, YN, 0])

        self.sync("c08b")     # "no topo da curva a inclinação é zero:"
        e1 = math(r"\theta", "=", "4r", "-", "2i", size=46).move_to([0, Y1, 0])
        e1[0].set_color(CYAN); e1[2].set_color(PINK); e1[4].set_color(VIOLET)
        self.play(FadeIn(e1), run_time=0.5)
        e2 = math(r"\frac{d\theta}{di}", "=", r"4\frac{dr}{di}", "-", "2", "=", "0", size=46).move_to([0, Y1, 0])
        e2[0].set_color(CYAN); e2[2].set_color(PINK)
        n2 = nt(mix("DERIVANDO EM", ("i", VIOLET), ": TANGENTE HORIZONTAL NO TOPO", size=21))
        self.morph(e1, e2, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], run_time=0.95, extra=[FadeIn(n2)])
        self.play(Indicate(e2[6], color=CYAN, scale_factor=1.4), run_time=0.6)
        self.sync("c08c")     # "uma pequena mudança na incidência produz só metade dessa mudança na refração."
        e3 = math(r"\frac{dr}{di}", "=", r"\frac{1}{2}", size=46).move_to([0, Y1, 0])
        e3[0].set_color(PINK)
        self.morph(e2, e3, [(2, 0), (5, 1), (4, 2)], run_time=0.95, extra=[FadeOut(n2)])
        self.wait(1.0)
        self.sync("c08d")     # "derivando Snell,"
        self.play(e3.animate.scale(0.8).move_to([2.3, Y2, 0]), run_time=0.5)
        s1 = math(r"\sin", "i", "=", "n", r"\sin", "r", size=46).move_to([0, Y1, 0])
        s1[1].set_color(VIOLET); s1[5].set_color(PINK)
        self.play(FadeIn(s1), run_time=0.5)
        self.sync("c08e")     # "chegamos a três vezes o cosseno ao quadrado da incidência"
        s2 = math(r"\cos", "i", "=", "n", r"\cos", "r", r"\cdot", r"\frac{dr}{di}", size=46).move_to([0, Y1, 0])
        s2[1].set_color(VIOLET); s2[5].set_color(PINK); s2[7].set_color(PINK)
        self.morph(s1, s2, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], run_time=0.9)
        s3 = math(r"\cos", "i", "=", r"\frac{n}{2}", r"\cos", "r", size=46).move_to([0, Y1, 0])
        s3[1].set_color(VIOLET); s3[5].set_color(PINK)
        half = e3[2].copy()
        self.play(ReplacementTransform(s2[0], s3[0]), ReplacementTransform(s2[1], s3[1]), ReplacementTransform(s2[2], s3[2]),
                  ReplacementTransform(VGroup(s2[3], half), s3[3]), ReplacementTransform(s2[4], s3[4]), ReplacementTransform(s2[5], s3[5]),
                  FadeOut(s2[6]), FadeOut(s2[7]), FadeOut(e3), run_time=0.9)
        self.remove(s2); self.add(s3)
        q1 = math("4", r"\cos^2", "i", "=", "n^2", r"\cos^2", "r", size=46).move_to([0, Y1, 0])
        q1[2].set_color(VIOLET); q1[6].set_color(PINK)
        self.morph(s3, q1, [(0, 1), (1, 2), (2, 3), (3, [0, 4]), (4, 5), (5, 6)], run_time=0.9)
        self.sync("c08f")     # "igual ao índice ao quadrado menos um."
        q2 = math("4", r"\cos^2", "i", "=", "n^2", "(", "1", "-", r"\sin^2", "r", ")", size=46).move_to([0, Y1, 0])
        q2[2].set_color(VIOLET); q2[9].set_color(PINK)
        n7 = nt(math(r"\cos^2 r = 1 - \sin^2 r", size=32, color=DIM))
        self.morph(q1, q2, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, [5, 6, 7, 8, 10]), (6, 9)], run_time=0.9, extra=[FadeIn(n7)])
        q4 = math("4", r"\cos^2", "i", "=", "n^2", "-", r"\sin^2", "i", size=46).move_to([0, Y1, 0])
        q4[2].set_color(VIOLET); q4[7].set_color(VIOLET)
        n8 = nt(math(r"n\sin r = \sin i \;\Rightarrow\; n^2 \sin^2 r = \sin^2 i", size=32, color=DIM))
        self.morph(q2, q4, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (7, 5), (8, 6), (9, 7)], run_time=0.9,
                   extra=[Succession(FadeOut(n7), FadeIn(n8))])
        q5 = math("4", r"\cos^2", "i", "=", "n^2", "-", "1", "+", r"\cos^2", "i", size=46).move_to([0, Y1, 0])
        q5[2].set_color(VIOLET); q5[9].set_color(VIOLET)
        n10 = nt(math(r"\sin^2 i = 1 - \cos^2 i", size=32, color=DIM))
        self.morph(q4, q5, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, [6, 7, 8]), (7, 9)], run_time=0.9,
                   extra=[Succession(FadeOut(n8), FadeIn(n10))])
        q6 = math("3", r"\cos^2", "i", "=", "n^2", "-", "1", size=48).move_to([0, Y1, 0])
        q6[2].set_color(VIOLET)
        self.morph(q5, q6, [([0, 8, 9], 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], run_time=0.9, extra=[FadeOut(n10)])
        self.sync("c08g")     # "para a água:"
        q7 = math(r"\cos^2", "i", "=", r"\frac{n^2-1}{3}", size=52).move_to([0, Y1, 0])
        q7[1].set_color(VIOLET)
        self.morph(q6, q7, [(1, 0), (2, 1), (3, 2), ([0, 4, 5, 6], 3)], run_time=0.8)
        box = panel(q7, pad=0.24)
        self.play(FadeIn(box), run_time=0.3)
        # números: substituições visíveis (valores internos sem arredondar nas contas)
        rr = r_from_i(im_, N_WATER)
        th_val = np.degrees(4 * rr - 2 * im_)
        self.sync("c08h")     # "incidência de cinquenta e nove graus,"
        v1 = math(r"\cos^2", "i", "=", r"\frac{1{,}333^2-1}{3}", "=", "0{,}259", size=42).move_to([0, Y1, 0])
        v1[1].set_color(VIOLET)
        self.play(Succession(AnimationGroup(FadeOut(box), FadeOut(q7)), FadeIn(v1)), run_time=0.7)
        vi = math("i", "=", f"{np.degrees(im_):.1f}".replace(".", "{,}") + r"^\circ", size=48).move_to([0, Y1, 0])
        vi[0].set_color(VIOLET); vi[2].set_color(VIOLET)
        self.morph(v1, vi, [(1, 0), (2, 1), (5, 2)], run_time=0.9)
        self.sync("c08i")     # "refração de quarenta..."
        self.play(vi.animate.scale(0.8).move_to([-2.4, Y2, 0]), run_time=0.4)
        sn = math(r"\sin", "r", "=", r"\frac{\sin i}{n}", size=42).move_to([0, Y1, 0])
        sn[1].set_color(PINK)
        self.play(FadeIn(sn), run_time=0.4)
        vr = math("r", "=", f"{np.degrees(rr):.1f}".replace(".", "{,}") + r"^\circ", size=48).move_to([0, Y1, 0])
        vr[0].set_color(PINK); vr[2].set_color(PINK)
        self.morph(sn, vr, [(1, 0), (2, 1), (3, 2)], run_time=0.8)
        self.sync("c08j")     # "e o máximo aparece em quarenta e dois graus."
        self.play(vr.animate.scale(0.8).move_to([0.2, Y2, 0]), run_time=0.4)
        ft = math(r"\theta", "=", "4r", "-", "2i", size=46).move_to([0, Y1, 0])
        ft[0].set_color(CYAN); ft[2].set_color(PINK); ft[4].set_color(VIOLET)
        payoff = math(r"\theta", "=", f"{th_val:.1f}".replace(".", "{,}") + r"^\circ", size=72, color=CYAN).move_to([0, Y1 - 0.1, 0])
        self.play(FadeIn(ft), run_time=0.4)
        self.play(TransformFromCopy(vr, ft[2]), TransformFromCopy(vi, ft[4]), run_time=0.6)
        self.morph(ft, payoff, [(0, 0), (1, 1), ([2, 3, 4], 2)], run_time=0.9)
        link = DashedLine(payoff.get_top() + UP * 0.1, mdot.get_center() + DOWN * 0.12, color=CYAN, stroke_width=1.0, dash_length=0.08, stroke_opacity=0.45)
        self.play(Create(link), Indicate(mdot, color=CYAN, scale_factor=1.6), run_time=0.7)
        o.update(graph=graph, tangent=tangent, mdot=mdot, xdrop=xdrop, xlbl=xlbl, payoff=payoff, vals=VGroup(vi, vr), link=link)

    # ------------------------------------------------------------------ C09 — as cores
    def c09_cores(self):
        o = self.scene_objs
        self.sync("c09")      # "e as cores?"
        self.heading("AS CORES", "O ÍNDICE DE REFRAÇÃO MUDA UM POUCO COM A COR", run_time=0.6)
        g = Gota([1.1, 2.75, 0], 1.65)
        self.gota = g
        circle, center = g.circle(), Dot(g.C, radius=0.045, color=INK)
        axis = dashed([g.x_left, g.C[1], 0], g.C + RIGHT * (g.R + 0.4), GEO, 0.4)
        xm = float(np.sin(i_max(N_WATER)))
        trw, trr, trv = g.trace(xm, N_WATER), g.trace(xm, N_RED), g.trace(xm, N_VIOLET)
        incident = Line(g.pt(trw["p0"]), g.pt(trw["P1"]), color=INK, stroke_width=2.8)
        self.play(Succession(FadeOut(VGroup(o["graph"], o["tangent"], o["mdot"], o["xdrop"], o["xlbl"], o["vals"], o["link"], o["payoff"])),
                             AnimationGroup(FadeIn(circle), FadeIn(center), Create(axis), Create(incident))), run_time=1.1)
        self.sync("c09b")     # "o índice muda um pouco com a cor."
        red = g.ray_lines(trr, exit_len=2.7, color=RED, width=2.6, with_incident=False)
        vio = g.ray_lines(trv, exit_len=2.7, color=VIO, width=2.6, with_incident=False)
        lab_r = mix("VERMELHO ·", ("n = 1{,}331", RED), size=19, color=RED).move_to([-2.2, 0.45, 0])
        lab_v = mix("VIOLETA ·", ("n = 1{,}343", VIO), size=19, color=VIO).next_to(lab_r, DOWN, buff=0.12, aligned_edge=LEFT)
        self.play(Create(red), Create(vio), run_time=1.2)
        self.play(FadeIn(lab_r), FadeIn(lab_v), run_time=0.4)
        # detalhe angular ×10 das duas direções de saída
        O = np.array([-0.9, -1.0, 0.0])
        K = 10.0
        thw = np.degrees(trw["theta"])

        def det_dir(th):
            ang = np.radians(180.0 + thw + (th - thw) * K)
            return np.array([np.cos(ang), np.sin(ang), 0.0])

        dr_ = Line(O, O + 2.0 * det_dir(np.degrees(trr["theta"])), color=RED, stroke_width=3)
        dv_ = Line(O, O + 2.0 * det_dir(np.degrees(trv["theta"])), color=VIO, stroke_width=3)
        dref = Line(O, O + LEFT * 2.0, color=GEO, stroke_width=1.2, stroke_opacity=0.5)
        det_lbl = words("DIREÇÕES DE SAÍDA · ÂNGULOS ×10", 15, DIM).move_to([-2.6, -0.62, 0])
        lr_ = words("42,4°", 22, RED).next_to(dr_.get_end(), DOWN, buff=0.08)
        lv_ = words("40,6°", 22, VIO).next_to(dv_.get_end(), LEFT, buff=0.08).shift(UP * 0.1)
        # gráfico: zoom no topo, curvas recortadas na janela (sem achatar valores)
        zax = Axes(x_range=[0.6, 1.0001, 0.1], y_range=[36, 44, 2], x_length=4.6, y_length=2.3,
                   axis_config=dict(color=DIM, stroke_width=1.6, include_ticks=True, tick_size=0.06, include_numbers=False), tips=False)
        zax.move_to([1.6, -2.85, 0])
        skip_audit(zax)
        zl = VGroup(math("b/R", size=28, color=INK).next_to(zax.x_axis.get_end(), RIGHT, buff=0.1),
                    math(r"\theta", size=32, color=CYAN).next_to(zax.y_axis.get_end(), RIGHT, buff=0.1),
                    *[math(s, size=22, color=DIM).next_to(zax.c2p(v, 36), DOWN, buff=0.1) for v, s in ((0.6, "0{,}6"), (0.8, "0{,}8"), (1.0, "1"))],
                    *[math(s, size=22, color=DIM).next_to(zax.c2p(0.6, v), LEFT, buff=0.1) for v, s in ((36, "36^\\circ"), (40, "40^\\circ"), (44, "44^\\circ"))])
        ztitle = words("ZOOM NO TOPO · RECORTE EM 36°", 15, DIM).next_to(zax, UP, buff=0.14).shift(RIGHT * 0.5)

        def x_window(n):
            ff = lambda x: theta_deg_from_b_ratio(x, n) - 36
            lo, hi = 0.5, float(np.sin(i_max(n)))
            for _ in range(60):
                m = (lo + hi) / 2; lo, hi = (m, hi) if ff(m) < 0 else (lo, m)
            a = hi
            lo, hi = float(np.sin(i_max(n))), 1.0
            for _ in range(60):
                m = (lo + hi) / 2; lo, hi = (lo, m) if ff(m) < 0 else (m, hi)
            return a, lo

        def plot(n, color, w=2.6, opa=1.0):
            a, b = x_window(n)
            return zax.plot(lambda x: theta_deg_from_b_ratio(x, n), x_range=[a, b, 0.002], color=color, stroke_width=w, stroke_opacity=opa)

        cw, cr, cv = plot(N_WATER, INK, 1.2, 0.35), plot(N_RED, RED), plot(N_VIOLET, VIO)
        skip_audit(cw, cr, cv)

        def maxpt(n):
            x = float(np.sin(i_max(n))); return zax.c2p(x, theta_deg_from_b_ratio(x, n))

        mr, mv = Dot(maxpt(N_RED), radius=0.07, color=RED), Dot(maxpt(N_VIOLET), radius=0.07, color=VIO)
        lr = words("VERMELHO 42,4°", 21, RED).next_to(mr, UP, buff=0.12).shift(RIGHT * 0.9)
        lv = words("VIOLETA 40,6°", 21, VIO).next_to(mv, DOWN, buff=0.14).shift(LEFT * 0.9)
        self.sync("c09c")     # "vermelho: quarenta e dois vírgula quatro graus."
        self.play(Create(dref), FadeIn(det_lbl), TransformFromCopy(red[2], dr_), FadeIn(lr_), run_time=0.9)
        self.play(Create(zax), FadeIn(zl), FadeIn(ztitle), Create(cw), Create(cr), FadeIn(mr, scale=0.4), FadeIn(lr), run_time=1.1)
        self.sync("c09d")     # "violeta: quarenta vírgula seis."
        self.play(TransformFromCopy(vio[2], dv_), FadeIn(lv_), run_time=0.7)
        self.play(Create(cv), FadeIn(mv, scale=0.4), FadeIn(lv), run_time=0.8)
        self.sync("c09e")     # "por isso, vermelho por fora e violeta por dentro."
        arc_c = np.array([-2.6, -4.05, 0.0])
        mini = VGroup(Arc(radius=0.8, start_angle=0, angle=PI, arc_center=arc_c, color=RED, stroke_width=5),
                      Arc(radius=0.65, start_angle=0, angle=PI, arc_center=arc_c, color=VIO, stroke_width=5),
                      Dot(arc_c, radius=0.04, color=INK), Line(arc_c + LEFT * 1.1, arc_c + RIGHT * 1.1, color=DIM, stroke_width=1.2))
        skip_audit(mini)
        order = mix("VERMELHO POR FORA ·", "VIOLETA POR DENTRO", size=21, color=INK).move_to([0, -4.6, 0])
        order[0].set_color(RED); order[1].set_color(VIO)
        self.play(FadeIn(mini), FadeIn(order, shift=UP * 0.1), run_time=0.9)
        self.wait(0.5)
        self.c09_objs = VGroup(circle, center, axis, incident, red, vio, lab_r, lab_v, dr_, dv_, dref, det_lbl, lr_, lv_,
                               zax, zl, ztitle, cw, cr, cv, mr, mv, lr, lv, order, mini)


    # ------------------------------------------------------------------ C10 — do ângulo ao arco (cone 2.5D)
    def c10_cone(self):
        TH = np.radians(42.078107)
        yH, L = FV["yH"], FV["L"]
        eye_h = 1.5
        foot_y = yH - eye_h
        h_t = ValueTracker(FV["h"])
        s_t = ValueTracker(0.0)                    # 0 = vista lateral · 1 = vista ao longo do eixo (gnomônica)
        r_op = ValueTracker(0.0)                   # opacidade dos raios de 42° na vista de frente
        E_side = np.array([-2.3, yH, 0.0])
        rho = L * np.tan(TH)
        h0 = h_t.get_value()
        a0 = np.array([np.cos(h0), -np.sin(h0), 0.0])
        u0 = np.array([np.sin(h0), np.cos(h0), 0.0])

        def A_front(h):
            return np.array([0.0, yH - L * np.tan(h), 0.0])

        def E_scr(s, h):
            return (1 - s) * E_side + s * A_front(h)

        def A_side(h):
            return E_side + L * np.array([np.cos(h), -np.sin(h), 0.0])

        def A_scr(s, h):
            return (1 - s) * A_side(h) + s * A_front(h)

        def ring_pt(t, s, h, rfac=1.0):
            r = rfac * rho
            side = E_side + np.array([L * np.cos(h) + r * np.cos(t) * np.sin(h), -L * np.sin(h) + r * np.cos(t) * np.cos(h), 0.0])
            front = A_front(h) + np.array([r * np.sin(t), r * np.cos(t), 0.0])
            return (1 - s) * side + s * front

        def t_horizon(h, rfac=1.0):
            c = L * np.tan(h) / (rfac * rho)
            return float(np.arccos(np.clip(c, -1.0, 1.0))) if c < 1.0 else 0.0

        def ring_above(rfac, color, width):
            def build():
                s, h = s_t.get_value(), h_t.get_value()
                t0 = t_horizon(h, rfac)
                if t0 <= 1e-3:
                    return VMobject()
                return polyline([ring_pt(t, s, h, rfac) for t in np.linspace(-t0, t0, 90)], color=color, stroke_width=width)
            return build

        def ring_below():
            s, h = s_t.get_value(), h_t.get_value()
            t0 = t_horizon(h)
            runs, cur = [], []
            for q in [ring_pt(t, s, h) for t in np.linspace(t0, TAU - t0, 160)]:
                if q[1] >= -3.3:           # o círculo não invade a área das legendas
                    cur.append(q)
                else:
                    if len(cur) > 1:
                        runs.append(cur)
                    cur = []
            if len(cur) > 1:
                runs.append(cur)
            return VGroup(*[polyline(r, color=GEO, stroke_width=1.4, stroke_opacity=0.35) for r in runs])

        def axis_line():
            s, h = s_t.get_value(), h_t.get_value()
            return DashedLine(E_scr(s, h), A_scr(s, h), color=INK, stroke_width=2.4, dash_length=0.1, stroke_opacity=0.8)

        def anti_dot():
            return Dot(A_scr(s_t.get_value(), h_t.get_value()), radius=0.075, color=INK)

        def ground_build():
            s = s_t.get_value()
            y_top = (1 - s) * foot_y + s * yH
            gg = make_ground(y_top, max(y_top + 3.5, 0.2), BLUE, 7, 0.1)
            gg.add(Line([-4.7, y_top, 0], [4.7, y_top, 0], color=GEO, stroke_width=2.0, stroke_opacity=0.7))
            return gg

        horizon = Line([-4.7, yH, 0], [4.7, yH, 0], color=DIM, stroke_width=2.2, stroke_opacity=0.9)
        hor_lbl = words("HORIZONTE", 16, DIM).move_to([3.9, yH + 0.24, 0])
        ground_m = always_redraw(ground_build)
        skip_audit(ground_m)
        person = make_person([E_side[0], foot_y], H=eye_h)
        sun_c = E_side - 1.75 * a0
        sun = make_sun(sun_c, 0.24)
        sun_lbl = words("SOL", 22, WARM).next_to(sun_c, UP, buff=0.55)
        ray_sun = Line(sun_c + 0.4 * a0, E_side - 0.05 * a0, color=WARM, stroke_width=3.0)
        skip_audit(ray_sun)
        axis_m = always_redraw(axis_line)
        anti_m = always_redraw(anti_dot)
        axis_lbl = words("EIXO ANTISSOLAR", 20).rotate(-h0).move_to(0.46 * A_side(h0) + 0.54 * E_side - 0.38 * u0)
        skip_audit(axis_lbl)
        anti_cap = words("PONTO ANTISSOLAR", 19, DIM).move_to(A_side(h0) + DOWN * 0.42 + RIGHT * 0.2)
        T0 = ring_pt(0.0, 0, h0)
        drop0 = make_drop(T0, 0.1, BLUE_L, 0.95)
        light = Arrow(T0, E_side, color=INK, stroke_width=3.0, buff=0.2, max_tip_length_to_length_ratio=0.06)
        sight = dashed(E_side, T0, CYAN, 0.95, 2.4, 0.12)
        a_dir = A_side(h0) - E_side
        arc_up = arc_between(E_side, a_dir, T0 - E_side, 1.15, CYAN, 3.2)
        l_up = arc_label(E_side, a_dir, T0 - E_side, 1.15, words("42°", 28, CYAN), pad=0.78).shift(UP * 0.32)

        self.sync("c10")      # "todas as direções a quarenta e dois graus da direção antissolar"
        self.heading("DO ÂNGULO AO ARCO", "42° EM TODAS AS DIREÇÕES", run_time=0.6)
        self.play(Succession(FadeOut(self.c09_objs),
                             AnimationGroup(FadeIn(ground_m), Create(horizon), FadeIn(hor_lbl), FadeIn(person), FadeIn(sun), FadeIn(sun_lbl),
                                            Create(ray_sun), Create(axis_m), FadeIn(anti_m), FadeIn(axis_lbl), FadeIn(anti_cap))), run_time=1.0)
        self.play(FadeIn(drop0, scale=0.5), GrowArrow(light), Create(sight), Create(arc_up), FadeIn(l_up), run_time=0.9)
        self.caption("OS 42° SÃO MEDIDOS A PARTIR DO EIXO ANTISSOLAR", t2c={"42°": CYAN, "ANTISSOLAR": WARM}, y=-3.95)

        self.sync("c10b")     # "formam um cone,"
        self.play(FadeOut(light), FadeOut(sight), FadeOut(drop0), FadeOut(axis_lbl), FadeOut(anti_cap), FadeOut(l_up), run_time=0.3)
        t_t = ValueTracker(0.0)
        sweep = always_redraw(lambda: Line(E_scr(s_t.get_value(), h_t.get_value()), ring_pt(t_t.get_value(), s_t.get_value(), h_t.get_value()),
                                           color=CYAN, stroke_width=2.4))
        sweep_drop = always_redraw(lambda: make_drop(ring_pt(t_t.get_value(), s_t.get_value(), h_t.get_value()), 0.08, BLUE_L, 0.95))
        skip_audit(sweep, sweep_drop)
        trail = []
        self.add(sweep, sweep_drop)
        n_tr = 8
        for kk in range(1, n_tr + 1):
            tk = TAU * kk / n_tr
            self.play(t_t.animate.set_value(tk), run_time=0.15, rate_func=linear)
            trail.append(tk)
        self.remove(sweep, sweep_drop)

        def spokes():
            s, h = s_t.get_value(), h_t.get_value()
            E = E_scr(s, h)
            return VGroup(*[Line(E, ring_pt(tk, s, h), color=CYAN, stroke_width=1.2, stroke_opacity=0.32 * (1 - 0.85 * s)) for tk in trail])

        spokes_m = always_redraw(spokes)
        skip_audit(spokes_m)
        below_m = always_redraw(ring_below)
        rfacs = [1 + 0.024 - 0.0096 * kk for kk in range(len(SPECTRUM))]   # vermelho fora → violeta dentro
        above_ms = [always_redraw(ring_above(rf, c, 3.4)) for rf, c in zip(rfacs, SPECTRUM)]
        drops_m = always_redraw(lambda: VGroup(*[make_drop(ring_pt(np.radians(q), s_t.get_value(), h_t.get_value()), 0.06, BLUE_L, 0.9)
                                                 for q in (-50, -25, 0, 25, 50)]))
        skip_audit(drops_m, below_m, *above_ms)
        self.add(spokes_m)
        self.play(FadeIn(below_m), *[FadeIn(m) for m in above_ms], FadeIn(drops_m), run_time=0.6)
        self.caption("AS DIREÇÕES A 42° FORMAM UM CONE", "CUJO EIXO É A DIREÇÃO ANTISSOLAR", t2c={"42°": CYAN, "ANTISSOLAR": WARM}, y=-3.95)

        self.sync("c10c")     # "e sua borda aparece como um círculo"
        self.play(FadeOut(person), FadeOut(sun), FadeOut(sun_lbl), FadeOut(ray_sun), FadeOut(arc_up), run_time=0.4)
        self.caption("VISTA DE FRENTE, AO LONGO DO EIXO ANTISSOLAR", t2c={"ANTISSOLAR": WARM}, y=-3.95, run_time=0.4)
        self.play(s_t.animate.set_value(1.0), run_time=2.0)
        anti_lbl = lines("PONTO ANTISSOLAR", "(A SOMBRA DA SUA CABEÇA)", size=17, color=DIM, gap=0.05)
        anti_lbl.add_updater(lambda m: m.move_to(A_front(h_t.get_value()) + DOWN * 0.62))
        spoke_ts = (-1.0, 0.0, 1.0)

        def radials():
            s, h = s_t.get_value(), h_t.get_value()
            return VGroup(*[Line(A_scr(s, h), ring_pt(t, s, h), color=CYAN, stroke_width=2.6, stroke_opacity=r_op.get_value()) for t in spoke_ts])

        radials_m = always_redraw(radials)
        skip_audit(radials_m)
        r42 = words("42°", 30, CYAN)
        r42.add_updater(lambda m: (m.move_to(A_front(h_t.get_value()) + np.array([0.42, 0.55 * rho, 0.0])), m.set_opacity(r_op.get_value())))
        self.sync("c10d")     # "em torno do ponto antissolar."
        self.play(FadeOut(spokes_m), FadeIn(anti_lbl), run_time=0.5)
        self.add(radials_m, r42)
        self.caption("O CÍRCULO: TODAS AS DIREÇÕES", "A 42° DO PONTO ANTISSOLAR", t2c={"42°": CYAN}, y=-3.95)
        self.play(r_op.animate.set_value(1.0), run_time=0.7)

        self.sync("c10e")     # "o horizonte esconde a parte de baixo e sobra o arco."
        self.caption("O HORIZONTE CORTA O CÍRCULO:", "O QUE SOBRA É O ARCO", y=-3.95)
        self.play(Indicate(hor_lbl, color=WARM, scale_factor=1.15), run_time=0.8)
        # indicador separado da altura do Sol (o Sol está atrás de você)
        gx = -3.95
        g0, gs = -0.9, 4.1 / 60.0
        gauge = VGroup(Line([gx, g0, 0], [gx, g0 + 60 * gs, 0], color=DIM, stroke_width=1.6),
                       *[Line([gx - 0.08, g0 + v * gs, 0], [gx + 0.08, g0 + v * gs, 0], color=DIM, stroke_width=1.4) for v in (0, 20, 40, 60)],
                       words("0°", 14, DIM).move_to([gx - 0.3, g0, 0]),
                       lines("ALTURA", "DO SOL", size=15, color=DIM, gap=0.04).move_to([gx + 0.05, g0 + 60 * gs + 0.55, 0]))
        thr_y = g0 + 42.078 * gs
        thr = Line([gx - 0.12, thr_y, 0], [gx + 0.4, thr_y, 0], color=CYAN, stroke_width=1.6, stroke_opacity=0.8)
        thr_lbl = words("42°", 15, CYAN).move_to([gx - 0.38, thr_y, 0])
        sun_i = always_redraw(lambda: Circle(radius=0.15, color=SUN_CORE, fill_color=SUN_CORE, fill_opacity=1, stroke_width=0)
                              .move_to([gx, g0 + gs * np.degrees(h_t.get_value()), 0]))
        skip_audit(sun_i)
        sun_val = DecimalNumber(20, num_decimal_places=0, unit=r"^\circ", font_size=28, color=SUN_CORE)
        sun_val.add_updater(lambda m: m.set_value(np.degrees(h_t.get_value())).next_to(sun_i, RIGHT, buff=0.1))
        top_txt = words("TOPO DO ARCO ACIMA DO HORIZONTE: 42° − SOL =", 17, DIM).move_to([-0.7, -4.6, 0])
        top_val = DecimalNumber(22, num_decimal_places=0, unit=r"^\circ", font_size=26, color=CYAN)
        top_val.add_updater(lambda m: m.set_value(np.degrees(TH - h_t.get_value())).next_to(top_txt, RIGHT, buff=0.1))

        self.sync("c10f")     # "com o Sol no horizonte, um semicírculo."
        self.caption("SOL NO HORIZONTE → SEMICÍRCULO", "CADA PESSOA TEM O SEU CENTRO: A PRÓPRIA SOMBRA", y=-3.95, size=21)
        self.play(FadeIn(gauge), FadeIn(thr), FadeIn(thr_lbl), FadeIn(sun_i), FadeIn(sun_val), FadeIn(top_txt), FadeIn(top_val), run_time=0.6)
        self.play(h_t.animate.set_value(0.0), run_time=1.8, rate_func=smooth)
        self.sync("c10g")     # "se o Sol sobe acima de quarenta e dois graus,"
        self.caption("SOL MAIS ALTO → O CENTRO DESCE", "E O ARCO ENCOLHE", y=-3.95)
        self.play(h_t.animate.set_value(np.radians(45.0)), run_time=2.0, rate_func=smooth)
        self.sync("c10h")     # "o círculo fica abaixo do horizonte."
        self.caption("SOL ACIMA DE 42° →", "ARCO INTEIRO ABAIXO DO HORIZONTE", t2c={"42°": CYAN}, y=-3.95)
        self.wait(0.6)
        self.c10 = dict(h_t=h_t, s_t=s_t, r_op=r_op, above_ms=above_ms, below_m=below_m, drops_m=drops_m, axis_m=axis_m, anti_m=anti_m,
                        sun_i=sun_i, sun_val=sun_val, gauge=gauge, thr=thr, thr_lbl=thr_lbl, top_txt=top_txt, top_val=top_val,
                        anti_lbl=anti_lbl, horizon=horizon, ground_m=ground_m, hor_lbl=hor_lbl, radials_m=radials_m, r42=r42,
                        A_front=A_front, rho=rho, yH=yH, L=L)

    # ------------------------------------------------------------------ C11 — fechamento
    def c11_fechamento(self):
        c = self.c10
        h_t = c["h_t"]
        self.sync("c11")      # "resumindo:"
        self.heading("O ARCO É UM ÂNGULO", "A 42° DO PONTO ANTISSOLAR", run_time=0.6)
        self.clear_caption(0.3)
        self.play(FadeOut(c["top_txt"]), FadeOut(c["top_val"]), FadeOut(c["drops_m"]), FadeOut(c["sun_i"]), FadeOut(c["sun_val"]),
                  FadeOut(c["gauge"]), FadeOut(c["thr"]), FadeOut(c["thr_lbl"]), FadeOut(c["below_m"]), FadeOut(c["ground_m"]),
                  FadeOut(c["axis_m"]), run_time=0.5)
        self.play(h_t.animate.set_value(np.radians(12.0)), run_time=0.7)
        for m in (*c["above_ms"], c["anti_m"], c["anti_lbl"], c["radials_m"], c["r42"]):
            m.clear_updaters()
        A = c["A_front"](h_t.get_value())
        # circuito: gota (raios amontoados) → máximo de θ → círculo no céu
        gm = Gota([-3.0, -2.35, 0], 0.55, x_left=-4.25)
        mini_rays = VGroup(*[gm.ray_lines(gm.trace(x), exit_len=0.55, color=CYAN, width=1.4, opacity=0.9, with_incident=False) for x in XS25[CLUSTER_IDX]])
        mini_rays.add(Line(gm.pt(gm.trace(0.86)["p0"]) + RIGHT * 0.55, gm.pt(gm.trace(0.86)["P1"]), color=INK, stroke_width=1.2, stroke_opacity=0.6))
        mini_g = VGroup(gm.circle(stroke_width=2), mini_rays)
        mx = Axes(x_range=[0, 1, 1], y_range=[0, 50, 50], x_length=1.5, y_length=1.0,
                  axis_config=dict(color=DIM, stroke_width=1.2, include_ticks=False), tips=False).move_to([-0.1, -2.35, 0])
        skip_audit(mx)
        mcurve = mx.plot(lambda x: theta_deg_from_b_ratio(x, N_WATER), x_range=[0, 1, 0.005], color=CYAN, stroke_width=2)
        xm = float(np.sin(i_max(N_WATER)))
        mdot = Dot(mx.c2p(xm, theta_deg_from_b_ratio(xm, N_WATER)), radius=0.05, color=CYAN)
        m42 = words("42°", 17, CYAN).next_to(mdot, UP, buff=0.06)
        mini_c = VGroup(mx, mcurve, mdot, m42)
        arr1 = Arrow([-2.0, -2.35, 0], [-1.2, -2.35, 0], color=DIM, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.25)
        arr2 = Arrow([0.9, -2.35, 0], [1.7, -2.35, 0], color=DIM, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.25)
        arcs_c = np.array([3.0, -2.6, 0.0])
        mini_arc = VGroup(Arc(radius=0.75, start_angle=np.radians(20), angle=np.radians(140), arc_center=arcs_c, color=RED, stroke_width=4),
                          Arc(radius=0.62, start_angle=np.radians(20), angle=np.radians(140), arc_center=arcs_c, color=VIO, stroke_width=4),
                          Dot(arcs_c, radius=0.035, color=INK))
        skip_audit(mini_arc)
        cap1 = words("RAIOS SE AMONTOAM", 16, DIM).move_to([-3.0, -3.5, 0])
        cap2 = words("MÁXIMO DO ÂNGULO", 16, DIM).move_to([-0.1, -3.5, 0])
        cap3 = words("CÍRCULO NO CÉU", 16, DIM).move_to([3.0, -3.5, 0])
        self.sync("c11b")     # "o arco-íris aparece onde os raios saem das gotas concentrados quase na mesma direção:"
        self.play(FadeIn(mini_g), FadeIn(cap1), run_time=0.6)
        self.play(GrowArrow(arr1), FadeIn(mini_c), FadeIn(cap2), run_time=0.6)
        self.sync("c11c")     # "a cerca de quarenta e dois graus do ponto antissolar."
        top = A + c["rho"] * UP
        radial = Line(A, top, color=CYAN, stroke_width=3.0)
        lbl = words("42°", 44, CYAN).next_to(radial, RIGHT, buff=0.2).shift(DOWN * 0.1)
        rad_note = words("DISTÂNCIA ANGULAR NO CÉU, A PARTIR DO PONTO ANTISSOLAR", 14, DIM, max_width=5.2)
        rad_note.next_to(c["anti_lbl"], DOWN, buff=0.08)
        self.play(GrowArrow(arr2), FadeIn(mini_arc), FadeIn(cap3), run_time=0.6)
        self.play(FadeOut(c["radials_m"]), FadeOut(c["r42"]), Create(radial), FadeIn(lbl, scale=0.7), FadeIn(rad_note), run_time=0.8)
        self.sync("c11d")     # "siga o Parallax Lab."
        cta1 = words("SIGA O PARALLAX LAB", 26).move_to([0, -4.0, 0])
        cta2 = words("@labparallax", 26, caps=False).set_color_by_gradient(CYAN, VIOLET, PINK).move_to([0, -4.55, 0])
        self.play(FadeIn(cta1, shift=UP * 0.1), FadeIn(cta2, shift=UP * 0.1), run_time=0.8)
