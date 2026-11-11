"""yt_0027 · v2 — helpers do sistema visual do yt_0026 v7/v8 (copiados de ../yt_0026_funcoes_vetoriais_campos/v7.py, sem importar de lá) e as peças
desta unidade, portadas do storyboard `referencia_v2/sb27.html` (canvas 1920×1080). Tudo em px de 1080p: PX(x, y) (1 u do Manim = 120 px);
Vista(cx, cy, u) = plano do storyboard. Regras (handoff v2 §2.1): seta = só a flecha (sem contorno, brilho ou opacidade); campo de contexto = cor
escura opaca; nada de pontinhos de fluido, tinta em xadrez, lupa, laços, sombras ou barras."""
from kit import *  # noqa: F401,F403

# ── paleta (handoff v2 §2.5; sb27.html) ─────────────────────────────────────────────────────────────────
CAMPO2, CTX, FUNDO_C = "#8CFFD2", "#1A5F55", "#091226"
SAIF, BR = "#A9CCFF", "#F5F7FF"
AMB, MAG, E3, VIO, CORAL, POS = "#FFC24D", "#EA63FF", "#35D9FF", "#9C8CFF", "#FF7A8A", "#E08A3C"
CARGA, CORR, CHAPA = "#267BFF", "#3FE08B", "#1A2C52"
FRIO, QUENTE = "#5C8BFF", "#FF9A5C"


def PX(x, y):
    return P3((x - 960) / 120, 4.5 - y / 120)


def fs(px):
    """font_size do MathTex equivalente ao KaTeX de `px` px (medido no yt_0026)."""
    return px * 0.803


def ts(px):
    return px * 0.6


def mix(a, b, t):
    return interpolate_color(ManimColor(a), ManimColor(b), min(1.0, max(0.0, t)))


class Vista(Plano):
    def __init__(self, cx, cy, u, uy=None):
        p = PX(cx, cy)
        super().__init__((p[0], p[1]), u / 120, (uy / 120) if uy else None)
        self.cx, self.cy, self.u = cx, cy, u


def seta7(a, b, cor, w=5, head=20):
    """Seta = haste + ponta cheia (largura = comprimento da ponta); w e head em px de 1080p."""
    s = seta(np.asarray(a, float), np.asarray(b, float), cor, w / 1.2, tip=head / 120)
    for m in s.get_family():
        m._sem_contorno = True
    return s


def _cor_seta(t, ctx, cor):
    if cor:
        return mix(cor, FUNDO_C, 0.65) if ctx else ManimColor(cor)
    return ManimColor(CTX) if ctx else mix(CAMPO, CAMPO2, t)


def seta_campo(v, X, Y, f, lmax, mmax, ctx=False, cor=None, w=5, head=19):
    m = math.hypot(*f)
    if m < 1e-9:
        return None
    t = min(1.0, m / mmax)
    L = lmax * (0.4 + 0.6 * t)
    u = (f[0] / m * L, f[1] / m * L)
    s = seta7(v.c2p(X - u[0] / 2, Y - u[1] / 2), v.c2p(X + u[0] / 2, Y + u[1] / 2), _cor_seta(t, ctx, cor), w, head)
    s._xy, s._L, s._t, s._f = (X, Y), L, t, f
    return s


class Campo7(VGroup):
    """Família de setas (sb27 `campo`/`campoPolar`): centradas no ponto, L = lmax·(0,4 + 0,6·t), t = min(1, |F|/mmax). `ctx(True)` escurece (opaco)."""

    def contexto(self, on=True, cor=None):
        for s in self:
            c = _cor_seta(s._t, on, cor or getattr(self, "_cor", None))
            s.haste.set_stroke(c)
            s.ponta.set_fill(c).set_stroke(c)
        return self

    def log(self, nome, passo):
        Ls = [s._L for s in self]
        if Ls:
            print(f"[campo] {nome}: {len(self)} setas, maior {max(Ls):.3f} u, menor {min(Ls):.3f} u (menor ÷ maior {min(Ls) / max(Ls):.2f}; alvo ≥ 0,40), "
                  f"maior ÷ passo = {max(Ls) / passo:.2f}")
        return self


def campo7(v, Fv, x0=-3, x1=3, y0=-3, y1=3, passo=0.5, rmin=0.3, rmax=3.05, mmax=1.0, ctx=False, cor=None, c=(0, 0), skip=None, nome="campo"):
    g = Campo7()
    g._cor = cor
    n = int(math.floor((x1 - x0) / passo + 1e-6))
    m = int(math.floor((y1 - y0) / passo + 1e-6))
    for i in range(n + 1):
        for j in range(m + 1):
            X, Y = x0 + i * passo, y0 + j * passo
            r = math.hypot(X - c[0], Y - c[1])
            if r < rmin or r > rmax or (skip and skip(X, Y)):
                continue
            s = seta_campo(v, X, Y, Fv(X, Y), 0.84 * passo, mmax, ctx, cor)
            if s is not None:
                g.add(s)
    return g.log(nome, passo).set_z_index(3)


def campo_polar(v, Fv, aneis, arco=0.62, mmax=1.0, ctx=False, cor=None, nome="campo polar"):
    g = Campo7()
    g._cor = cor
    for r in aneis:
        n = max(6, round(2 * PI * r / arco))
        for i in range(n):
            a = 2 * PI * i / n
            X, Y = r * math.cos(a), r * math.sin(a)
            s = seta_campo(v, X, Y, Fv(X, Y), 0.84 * arco, mmax, ctx, cor)
            s._r = r
            g.add(s)
    return g.log(nome, arco).set_z_index(3)


def destaca_seta(s, w=7, head=22, cor=CAMPO2):
    """A mesma seta, mais grossa (7 px, ponta 22 px) — o 'engrossar' do H3."""
    X, Y = s._xy
    a, b = s.get_start(), s.get_end()
    return seta7(a, b, cor, w, head).set_z_index(4)


# ── texto ───────────────────────────────────────────────────────────────────────────────────────────────
def T(s, x, y, size=30, al="left", cor=WHITE_, bold=True):
    """Texto (fillText do storyboard): y = linha de base em px."""
    m = txt(s, ts(size), color=cor, bold=bold)
    b = base_de(m)
    m.shift(UP * (PX(0, y)[1] - b))
    dx = PX(x, 0)[0]
    if al == "left":
        m.shift(RIGHT * (dx - m.get_left()[0]))
    elif al == "center":
        m.shift(RIGHT * (dx - m.get_center()[0]))
    else:
        m.shift(RIGHT * (dx - m.get_right()[0]))
    for g in m.get_family():
        g._sem_contorno = True
    return m.set_z_index(30)


def legenda(s, x, y, cor=SAIF, al="left", size=28):
    return T(s, x, y, size, al, cor, bold=False)


TEX27 = TexTemplate()
TEX27.add_to_preamble(
    r"\usepackage{xcolor}"
    r"\definecolor{ca}{HTML}{FFC24D}\definecolor{cm}{HTML}{EA63FF}\definecolor{cz}{HTML}{35D9FF}\definecolor{cc}{HTML}{2EE6A0}"
    r"\definecolor{cs}{HTML}{7FB2FF}\definecolor{cv}{HTML}{9C8CFF}\definecolor{cr}{HTML}{FF7A8A}\definecolor{cj}{HTML}{3FE08B}"
    r"\definecolor{cg}{HTML}{B8C4DA}\definecolor{cp}{HTML}{E08A3C}"
    r"\def\X{\textcolor{ca}{x}}\def\Y{\textcolor{cm}{y}}\def\Z{\textcolor{cz}{z}}\def\F{\textcolor{cc}{\vec F}}"
    r"\def\Pp{\textcolor{cc}{P}}\def\Qq{\textcolor{cc}{Q}}\def\Rr{\textcolor{cc}{R}}"
    r"\def\dx{\partial \textcolor{ca}{x}}\def\dy{\partial \textcolor{cm}{y}}\def\dz{\partial \textcolor{cz}{z}}"
    r"\def\w{\textcolor{cv}{\omega}}\def\V#1{\textcolor{cv}{#1}}\def\D#1{\textcolor{cs}{#1}}\def\C#1{\textcolor{cr}{#1}}\def\Pt#1{\textcolor{cp}{#1}}"
    r"\def\rot{\operatorname{rot}}\def\dv{\operatorname{div}}\def\h{\textcolor{ca}{h}}\def\k{\textcolor{cm}{k}}"
    r"\def\xo{\textcolor{ca}{x_0}}\def\yo{\textcolor{cm}{y_0}}\def\E{\textcolor{cc}{\vec E}}\def\B{\textcolor{cm}{\vec B}}"
    r"\def\J{\textcolor{cj}{\vec J}}\def\phi{\textcolor{cs}{\varphi}}\def\T{\textcolor{cs}{T}}\def\kk{\vec k}")


def TC(s, x=960, y=540, size=52, al="l", caneta=True):
    """Fórmula do storyboard (mesma string do KaTeX, com os macros do preâmbulo): centro vertical em y px, alinhamento em x px (l | c | r)."""
    m = MathTex(s, font_size=fs(size), tex_template=TEX27)
    m._tex, m._caneta, m._esc, m._em_caneta = s, caneta, not caneta, False
    for g in m.get_family()[1:]:
        g._sem_contorno = True
    p = PX(x, y)
    m.move_to(p)
    if al == "l":
        m.shift(RIGHT * (p[0] - m.get_left()[0]))
    elif al == "r":
        m.shift(RIGHT * (p[0] - m.get_right()[0]))
    return m.set_z_index(25)


def placa7(m, padx=6, pady=4):
    """Placa mínima do v8 atrás de um rótulo: #091226 a 85 %, sem borda (padding em px)."""
    r = RoundedRectangle(width=m.width + 2 * padx / 120, height=m.height + 2 * pady / 120, corner_radius=6 / 120).move_to(m.get_center())
    r.set_fill(FUNDO_C, 0.85).set_stroke(width=0)
    r._sem_contorno = True
    r.set_z_index(m.z_index - 1 if m.z_index else 24)
    return r


def TP(s, x, y, size=40, al="c", caneta=False):
    """Rótulo matemático com placa (o `tex(..., placa=true)` do storyboard). Devolve VGroup(placa, MathTex); o MathTex fica em .f."""
    f = TC(s, x, y, size, al, caneta=caneta)
    g = VGroup(placa7(f), f)
    g.f = f
    return g


def TXP(s, x, y, size=28, al="center", cor=BR, bold=False):
    t = T(s, x, y, size, al, cor, bold)
    g = VGroup(placa7(t, 8, 4), t)
    g.f = t
    return g


def canto_xy(v, X, Y):
    """px de um ponto do plano."""
    p = v.c2p(X, Y)
    return p[0] * 120 + 960, 540 - p[1] * 120


# ── desenho ─────────────────────────────────────────────────────────────────────────────────────────────
def painel(x0, y0, w, h):
    """Painel v8: só a moldura (GEO a 35 %, raio 14), sem preenchimento."""
    r = RoundedRectangle(width=w / 120, height=h / 120, corner_radius=14 / 120).move_to(PX(x0 + w / 2, y0 + h / 2))
    r.set_fill(opacity=0).set_stroke(GEO, 2 / 1.2, 0.35)
    r._sem_contorno = True
    return r.set_z_index(-40)


def linha7(pts, cor, w=5, alpha=1.0, dash=None):
    m = VMobject().set_points_as_corners([np.asarray(p, float) for p in pts]).set_stroke(cor, w / 1.2, alpha).set_fill(opacity=0)
    m.cap_style = CapStyleType.ROUND
    m._sem_contorno = True
    if dash:
        n = max(4, int(m.get_arc_length() * 120 / (dash[0] + dash[1])))
        m = DashedVMobject(m, num_dashes=n, dashed_ratio=dash[0] / (dash[0] + dash[1]))
        for q in m.get_family():
            q._sem_contorno = True
    return m.set_z_index(5)


def vlinha(v, pts, cor, w=5, alpha=1.0, dash=None):
    return linha7([v.c2p(*p) for p in pts], cor, w, alpha, dash)


def circ_pts(r, c=(0, 0), n=200, a0=0.0, a1=2 * PI):
    return [(c[0] + r * math.cos(a0 + (a1 - a0) * i / n), c[1] + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def vcirc(v, r, cor=GEO, w=3, c=(0, 0), dash=None, alpha=1.0):
    return vlinha(v, circ_pts(r, c), cor, w, alpha, dash)


def preenche(v, pts, cor, alpha=1.0, z=1):
    m = Polygon(*[v.c2p(*p) for p in pts]).set_fill(cor, alpha).set_stroke(width=0)
    m._sem_contorno = True
    return m.set_z_index(z)


def ponto7(p, cor, r=9, z=8):
    d = Dot(np.asarray(p, float), radius=r / 120, color=cor).set_z_index(z)
    d._sem_contorno = True
    return d


def giro_seta(v, c, r, a0, a1, cor=VIO, w=4, head=18):
    """Arco (sb27 giroSeta) de a0 a a1 em volta de c, com ponta cheia no fim."""
    pts = circ_pts(r, c, 60, a0, a1)
    arco = vlinha(v, pts, cor, w)
    A, B = np.array(pts[-2]), np.array(pts[-1])
    d = (B - A) / np.linalg.norm(B - A)
    pt = seta7(v.c2p(*(B - d * 0.01)), v.c2p(*(B + d * 0.12)), cor, w, head)
    return VGroup(arco, pt).set_z_index(9)


def braco(v, a, b, cor=CORAL, w=7, dash=None, pontas=True):
    g = VGroup(vlinha(v, [a, b], cor, w, dash=dash))
    if pontas and not dash:
        g.add(ponto7(v.c2p(*a), cor, 10, 9), ponto7(v.c2p(*b), cor, 10, 9))
    return g.set_z_index(8)


def quadrado(v, c, s, cor, dash=None, fill=None, w=4, alpha=0.85, z=6):
    q = [(c[0] - s / 2, c[1] - s / 2), (c[0] + s / 2, c[1] - s / 2), (c[0] + s / 2, c[1] + s / 2), (c[0] - s / 2, c[1] + s / 2), (c[0] - s / 2, c[1] - s / 2)]
    g = VGroup()
    if fill:
        g.add(preenche(v, q[:-1], fill, alpha, z))
    g.add(vlinha(v, q, cor, w, dash=dash).set_z_index(z + 0.5))
    return g


def furo7(v, r=0.55, cor=None, simb=None, simb_px=None):
    g = VGroup(preenche(v, circ_pts(r), ESC, 1.0, 6), vcirc(v, r, GEO, 3).set_z_index(6.5))
    if cor:
        g.add(preenche(v, circ_pts(r * 0.62), cor, 1.0, 7))
        if simb:
            c = canto_xy(v, 0, 0)
            g.add(TC(simb, c[0], c[1], simb_px or r * v.u * 0.9, "c", caneta=False).set_z_index(8))
    return g


class Roda(VGroup):
    """Rodinha (sb27 `roda`): 4 pás coral de 0,2R a R (largura 0,30 R), pá 0 inteira azul-clara (#A9CCFF), cubo escuro (0,24 R) com anel coral 3 px,
    pino GEO opcional. `pose(c, ang)` com c em coordenadas do PLANO e ang em rad (ang = 0: pá marcada para cima). Nunca deforma."""

    def __init__(self, v, R, pino=False, z=9):
        super().__init__()
        self.v, self.R = v, R
        Ru = R * v.ux
        for k in range(4):
            a = PI / 2 + k * PI / 2
            u, n = np.array([math.cos(a), math.sin(a), 0]), np.array([-math.sin(a), math.cos(a), 0])
            w = 0.15 * Ru
            p = Polygon(0.2 * Ru * u - w * n, Ru * u - w * n, Ru * u + w * n, 0.2 * Ru * u + w * n).set_fill(SAIF if k == 0 else CORAL, 1).set_stroke(width=0)
            p._sem_contorno = True
            self.add(p)
        hub = Circle(radius=0.24 * Ru).set_fill(ESC, 1).set_stroke(CORAL, 3 / 1.2, 1)
        hub._sem_contorno = True
        self.add(hub)
        if pino:
            pn = Dot(ORIGIN, radius=5 / 120, color=GEO)
            pn._sem_contorno = True
            self.add(pn)
        self._refs = [(m, m.points.copy()) for m in self.family_members_with_points()]
        self.c, self.ang = (0.0, 0.0), 0.0
        self.set_z_index(z)

    def pose(self, c, ang):
        cs, sn = math.cos(ang), math.sin(ang)
        Rm = np.array([[cs, -sn, 0], [sn, cs, 0], [0, 0, 1.0]])
        o = self.v.c2p(*c)
        for m, ref in self._refs:
            m.set_points(ref @ Rm.T + o)
        self.c, self.ang = tuple(c), ang
        return self


class Fita(VGroup):
    """Fita de tinta (sb27 `fita`): uma faixa radial de r = 0,75 a 2,5 (apontando para cima), levada pelo fluxo exato: largura 14 px azul-clara a
    50 % + linha #A9CCFF fina (2 px a 70 %). Fica por baixo das setas."""

    def __init__(self, v, flow, lw=14, n=300):
        super().__init__()
        self.v, self.flow = v, flow
        r = 0.75 + 1.75 * np.arange(n + 1) / n
        self.x0, self.y0 = np.zeros_like(r), r
        self.larga = VMobject().set_stroke(AZ_FITA, lw / 1.2, 0.5).set_fill(opacity=0)
        self.fina = VMobject().set_stroke(SAIF, 2 / 1.2, 0.7).set_fill(opacity=0)
        for m in (self.larga, self.fina):
            m._sem_contorno = True
            m.cap_style = CapStyleType.ROUND
            m.joint_type = LineJointType.ROUND
        self.add(self.larga, self.fina)
        self.set_z_index(2)
        self.t = 0.0
        self.em(0.0)

    def em(self, t):
        X, Y = self.flow(self.x0, self.y0, t)
        P = np.array([self.v.c2p(a, b) for a, b in zip(X, Y)])
        self.larga.set_points_smoothly(P)
        self.fina.set_points_smoothly(P)
        self.t, self.XY = t, np.stack([X, Y], 1)
        return self


AZ_FITA = "#7FB2FF"


class Material(VGroup):
    """Objeto material (braço, quadrado, setor) definido por pontos do plano e levado pelo fluxo exato; preenchido ou só traço."""

    def __init__(self, v, pts, flow, cor=CORAL, w=7, fill=None, alpha=0.9, pontas=False, z=8):
        super().__init__()
        self.v, self.flow = v, flow
        self.P0 = np.asarray(pts, float)
        self.tr = VMobject().set_stroke(cor, w / 1.2, 1).set_fill(fill or cor, alpha if fill else 0)
        self.tr.cap_style = CapStyleType.ROUND
        self.tr._sem_contorno = True
        self.add(self.tr)
        self.pontas = []
        if pontas:
            self.pontas = [ponto7(ORIGIN, cor, 10, z + 1), ponto7(ORIGIN, cor, 10, z + 1)]
            self.add(*self.pontas)
        self.set_z_index(z)
        self.em(0.0)

    def em(self, t):
        X, Y = self.flow(self.P0[:, 0], self.P0[:, 1], t)
        P = np.array([self.v.c2p(a, b) for a, b in zip(X, Y)])
        self.tr.set_points_as_corners(P)
        if self.pontas:
            self.pontas[0].move_to(P[0])
            self.pontas[1].move_to(P[-1])
        self.t, self.XY = t, np.stack([X, Y], 1)
        return self

    def ang(self):
        d = self.XY[-1] - self.XY[0]
        return math.atan2(d[1], d[0])


def seg_pts(a, b, n=40):
    u = np.linspace(0, 1, n)[:, None]
    return np.asarray(a, float) * (1 - u) + np.asarray(b, float) * u


def ret_pts(c, s, n=30):
    x0, x1, y0, y1 = c[0] - s / 2, c[0] + s / 2, c[1] - s / 2, c[1] + s / 2
    return np.concatenate([seg_pts((x0, y0), (x1, y0), n), seg_pts((x1, y0), (x1, y1), n), seg_pts((x1, y1), (x0, y1), n), seg_pts((x0, y1), (x0, y0), n)])


def setor_pts(r1, r2, a, n=30):
    p = [(r1 * math.cos(-a + 2 * a * i / n), r1 * math.sin(-a + 2 * a * i / n)) for i in range(n + 1)]
    p += [(r2 * math.cos(-a + 2 * a * i / n), r2 * math.sin(-a + 2 * a * i / n)) for i in range(n, -1, -1)]
    p.append(p[0])
    return np.array(p)


def area_poly(p):
    x, y = p[:, 0], p[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


# ── campos e fluxos exatos (Anexo C do v1) ──────────────────────────────────────────────────────────────
F_GIRO = lambda x, y: (-y, x)
F_VORT = lambda x, y: (-y / (x * x + y * y), x / (x * x + y * y))
F_Y2X = lambda x, y: (-y, 2 * x)
F_RIO = lambda x, y: (1 - y * y / 9, 0.0)
F_EXPL = lambda x, y: (x, y)
F_SELA = lambda x, y: (x, -y)
F_ANEL = lambda x, y: (x - x ** 3 / 3, y - y ** 3 / 3)
F_FONTE = lambda x, y: (x / (x * x + y * y), y / (x * x + y * y))


def F_TORN(x, y):
    r2 = x * x + y * y
    if np.ndim(r2) == 0:
        return (-y, x) if r2 < 1 else (-y / r2, x / r2)
    d = r2 < 1
    return np.where(d, -y, -y / r2), np.where(d, x, x / r2)


def fl_giro(x, y, t):
    c, s = np.cos(t), np.sin(t)
    return c * x - s * y, s * x + c * y


def fl_vort(x, y, t):
    r2 = x * x + y * y
    th = np.arctan2(y, x) + t / r2
    r = np.sqrt(r2)
    return r * np.cos(th), r * np.sin(th)


def fl_y2x(x, y, t):
    w = math.sqrt(2)
    c, s = np.cos(w * t), np.sin(w * t)
    return x * c - (y / w) * s, w * x * s + y * c


def fl_expl(x, y, t):
    return x * np.exp(t), y * np.exp(t)


def fl_sela(x, y, t):
    return x * np.exp(t), y * np.exp(-t)


def _anel1(x, t):
    x = np.asarray(x, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        u = 3.0 / (1.0 + (3.0 / (x * x) - 1.0) * np.exp(-2 * t))
    return np.where(np.abs(x) < 1e-12, 0.0, np.sign(x) * np.sqrt(u))


def fl_anel(x, y, t):
    return _anel1(x, t), _anel1(y, t)


def fl_fonte(x, y, t):
    r = np.sqrt(x * x + y * y + 2 * t)
    th = np.arctan2(y, x)
    return r * np.cos(th), r * np.sin(th)


def fl_torn(x, y, t):
    r2 = x * x + y * y
    a1, a2 = fl_giro(x, y, t), fl_vort(x, y, t)
    d = r2 < 1
    return np.where(d, a1[0], a2[0]), np.where(d, a1[1], a2[1])


def rk4(Ff, x, y, t, n=400):
    x, y = np.array(x, float), np.array(y, float)
    h = t / n
    f = lambda a, b: tuple(np.asarray(c, float) * np.ones_like(a) for c in Ff(a, b))
    for _ in range(n):
        k1 = f(x, y)
        k2 = f(x + h / 2 * k1[0], y + h / 2 * k1[1])
        k3 = f(x + h / 2 * k2[0], y + h / 2 * k2[1])
        k4 = f(x + h * k3[0], y + h * k3[1])
        x = x + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y = y + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return x, y


def qa_fluxo(nome, v, Ff, xy0, t, desenhado, n=20):
    """[fluxo] 20 posições desenhadas × integração RK4 do campo (px a 960×540)."""
    xy0 = np.asarray(xy0, float)
    idx = np.linspace(0, len(xy0) - 1, min(n, len(xy0))).astype(int)
    xr, yr = rk4(Ff, xy0[idx, 0], xy0[idx, 1], t) if abs(t) > 1e-9 else (xy0[idx, 0], xy0[idx, 1])
    alvo = np.array([v.c2p(a, b) for a, b in zip(xr, yr)])
    d = np.asarray(desenhado, float)[idx]
    err = np.linalg.norm(alvo[:, :2] - d[:, :2], axis=1).max() * 60
    print(f"[fluxo] {nome}: {len(idx)} pontos em t = {t:.3f}; erro máx {err:.3f} px a 960×540 ({'ok' if err <= 1 else 'FORA'})")
    return err


def corre(cena, objs, t1, rt, t0=0.0, rate=linear):
    """Roda o fluxo exato UMA vez, de t0 a t1 (tempo de fluxo) em rt s de tela (câmera lenta = (t1 − t0)/rt, registrada no log)."""
    print(f"[motor] {getattr(cena, '_aid', '')}: fluxo de {t0:.3f} a {t1:.3f} em {rt:.2f} s (fator {(t1 - t0) / rt:.3f} de fluxo por s)")
    return [UpdateFromAlphaFunc(o, lambda m, a: m.em(t0 + (t1 - t0) * rate(a)), run_time=rt) for o in objs]


class Motor:
    def __init__(self, cena, v, nome=""):
        self.c, self.v, self.tau0, self.t0, self.nome = cena, v, 0.0, None, nome
        print(f"[motor] {nome}: {v:.4f} s de fluxo por s de tela")

    def liga(self, tau=None):
        if tau is not None:
            self.tau0 = tau
        self.t0 = self.c.clk.get_value()
        return self

    def para(self, tau=None):
        self.tau0 = self.tau() if tau is None else tau
        self.t0 = None
        return self

    def tau(self):
        return self.tau0 + (self.v * (self.c.clk.get_value() - self.t0) if self.t0 is not None else 0.0)


class NumBR(DecimalNumber):
    def _get_num_string(self, number):
        return super()._get_num_string(number).replace(".", ",")


def cresce_campo(g, rt=1.4, chave=None):
    """O campo cresce do centro para fora (ou na ordem de `chave`)."""
    ss = sorted(g, key=chave or (lambda s: math.hypot(*s._xy)))
    return LaggedStart(*[GrowFromPoint(s, s.get_center()) for s in ss], lag_ratio=min(0.06, 2.5 / max(1, len(ss))), run_time=rt)


# ── QA [colisão] (handoff v2 §6.4): distância entre cada rótulo/fórmula e qualquer seta ou traço, no fim de cada âncora ──────────────────
def _rotulos_e_tracos(cena):
    fix = cena.fixos()
    rot, tra = [], []
    for m in cena.mobjects:
        if m in fix or m is cena.clk or isinstance(m, ValueTracker):
            continue
        for x in m.get_family():
            if isinstance(x, (MathTex, Text, SingleStringMathTex)) or type(x).__name__ in ("MarkupText", "Paragraph"):
                if x.get_family() and any(len(g.points) for g in x.family_members_with_points()):
                    rot.append(x)
        for x in m.family_members_with_points():
            if not isinstance(x, VMobject) or isinstance(x, (SVGMobject, VMobjectFromSVGPath)):
                continue
            if x.get_stroke_width() > 0.5 and x.get_stroke_opacity() > 0.3 or isinstance(x, Polygon) and x.get_fill_opacity() > 0.5:
                tra.append(x)
    texto = set(id(g) for r in rot for g in r.get_family())
    tra = [t for t in tra if id(t) not in texto and not isinstance(t, (RoundedRectangle,)) and not getattr(t, "_placa", False)]
    return rot, tra


def qa_colisao(cena, aid, lim_px=6.0):
    rot, tra = _rotulos_e_tracos(cena)
    piores = []
    for r in rot:
        x0, y0 = r.get_corner(DL)[:2]
        x1, y1 = r.get_corner(UR)[:2]
        dmin = 1e9
        for t in tra:
            P = t.points[:, :2]
            if not len(P):
                continue
            dx = np.maximum(np.maximum(x0 - P[:, 0], 0), P[:, 0] - x1)
            dy = np.maximum(np.maximum(y0 - P[:, 1], 0), P[:, 1] - y1)
            dmin = min(dmin, float(np.min(np.hypot(dx, dy))) * 120)
        if dmin < lim_px:
            piores.append((dmin, getattr(r, "_tex", None) or getattr(r, "text", None) or type(r).__name__))
    for d, nome in sorted(piores)[:12]:
        print(f"[colisão] {aid}: {str(nome)[:60]!r} a {d:.1f} px de um traço (alvo ≥ {lim_px:.0f})")
    print(f"[colisão-total] {aid}: {len(piores)} rótulos a menos de {lim_px:.0f} px em {len(rot)} rótulos")


_fecha0 = Base._fecha


def _fecha_qa(self, antes=0.0):
    if self._aid is not None and os.environ.get("QA_COLISAO") == "1":
        if self.alvo - self.nq >= 1:
            self.wait((self.alvo - self.nq) / FPS)
        qa_colisao(self, self._aid)
    _fecha0(self, antes=antes)


Base._fecha = _fecha_qa


# ── v3: clareira (R1), campo que entra sem virar pontinhos (§4.2), checagem de sobreposição (R5) ───────────────────────────────────────
def clar(rets=(), pts=(), r=0.3):
    """sb27 `clar`: pula as setas cujo centro cai num retângulo (x0, y0, x1, y1 do plano) ou a menos de r de um ponto."""
    return lambda X, Y: any(a < X < c and b < Y < d for a, b, c, d in rets) or any(math.hypot(X - a, Y - b) < r for a, b in pts)


def campo_polar_skip(v, Fv, aneis, skip, **kw):
    g = campo_polar(v, Fv, aneis, **kw)
    for s in [s for s in g if skip(*s._xy)]:
        g.remove(s)
    return g


def cresce_campo(g, rt=1.0, chave=None):
    """O campo entra JÁ no comprimento final (FadeIn em LaggedStart curto): nunca nasce como pontinhos."""
    ss = sorted(g, key=chave or (lambda s: math.hypot(*s._xy)))
    return LaggedStart(*[FadeIn(s) for s in ss], lag_ratio=min(0.02, 0.6 / max(1, len(ss))), run_time=rt)


def esconde(campo, teste):
    """Setas do campo cujo centro passa no teste: VGroup para FadeOut (clareira) / FadeIn (volta)."""
    return VGroup(*[s for s in campo if teste(*s._xy)])


def clareira_viva(campo, centros, r):
    """Clareira que acompanha objetos em movimento: a cada quadro, some a seta cujo centro está a menos de r de um dos centros (do plano)."""
    def f(m):
        cs = centros()
        for s in m.submobjects:
            dentro = any(math.hypot(s._xy[0] - a, s._xy[1] - b) < r for a, b in cs)
            if dentro != getattr(s, "_escondida", False):
                s.set_opacity(0 if dentro else 1)
                s._escondida = dentro
    campo.add_updater(f)
    f(campo)
    return f


def qa_sobreposicao(cena, onde):
    """R5: (a) caixas de texto/MathTex que se cruzam; (b) seta de campo visível com o centro dentro de uma caixa de texto (+4 px)."""
    fix = cena.fixos()
    textos, setas, vistas = [], [], set()
    for m in cena.mobjects:
        if m in fix or isinstance(m, ValueTracker):
            continue
        for x in m.get_family():
            if isinstance(x, (MathTex, SingleStringMathTex, Text)) or type(x).__name__ in ("MarkupText",):
                if any(len(g.points) and g.get_fill_opacity() > 0.3 for g in x.family_members_with_points()):
                    textos.append(x)
            if hasattr(x, "_xy") and hasattr(x, "haste") and id(x) not in vistas:      # seta de campo (no Campo7 ou solta, depois do cresce_campo)
                vistas.add(id(x))
                if x.haste.get_stroke_opacity() > 0.3 and not getattr(x, "_escondida", False):
                    setas.append(x)
    # só o texto de mais alto nível (um MathTex dentro de outro não conta duas vezes)
    ids = set()
    tops = []
    for t in textos:
        if id(t) in ids:
            continue
        tops.append(t)
        ids |= {id(g) for g in t.get_family()}
    caixas = [(t, t.get_corner(DL)[:2], t.get_corner(UR)[:2]) for t in tops]
    ocorr = []
    m4 = 4 / 120
    for i in range(len(caixas)):
        a, (ax0, ay0), (ax1, ay1) = caixas[i]
        for j in range(i + 1, len(caixas)):
            b, (bx0, by0), (bx1, by1) = caixas[j]
            if ax0 < bx1 and bx0 < ax1 and ay0 < by1 and by0 < ay1:
                ocorr.append(f"texto×texto {nome_t(a)!r} × {nome_t(b)!r}")
        for s in setas:
            cx, cy = s.get_center()[:2]
            if ax0 - m4 < cx < ax1 + m4 and ay0 - m4 < cy < ay1 + m4:
                ocorr.append(f"seta×texto {nome_t(a)!r} (seta em {tuple(round(v, 2) for v in s._xy)})")
                break
    for o in ocorr:
        print(f"[sobrepos] {onde}: {o}")
    print(f"[sobrepos-chk] {onde}: {len(tops)} textos, {len(setas)} setas visíveis, {len(ocorr)} ocorrências")
    return len(ocorr)


def nome_t(m):
    return str(getattr(m, "_tex", None) or getattr(m, "text", None) or getattr(m, "original_text", None) or type(m).__name__)[:50]


_gat0 = Base.gat


def _gat_qa(self, frase):
    _gat0(self, frase)
    if os.environ.get("QA_SOBREPOS") == "1":
        qa_sobreposicao(self, f"{self._aid} «{frase}»")


Base.gat = _gat_qa
_fecha1 = Base._fecha


def _fecha_sob(self, antes=0.0):
    if self._aid is not None and os.environ.get("QA_SOBREPOS") == "1":
        qa_sobreposicao(self, f"{self._aid} fim")
    _fecha1(self, antes=antes)


Base._fecha = _fecha_sob


def op_seta(s, o):
    """Opacidade real da seta (só durante a clareira); não mexe na cor (o verde de contexto continua)."""
    s.haste.set_stroke(opacity=o)
    s.ponta.set_fill(opacity=o).set_stroke(opacity=o)


def some(vg, rt=0.4):
    """Clareira: as setas somem (e ficam marcadas como escondidas para o QA R5)."""
    for s in vg:
        s._escondida = True
    return UpdateFromAlphaFunc(vg, lambda m, a: [op_seta(s, 1 - a) for s in m], run_time=rt)


def volta(vg, rt=0.4):
    for s in vg:
        s._escondida = False
    return UpdateFromAlphaFunc(vg, lambda m, a: [op_seta(s, a) for s in m], run_time=rt)


def clareira_viva(campo, centros, r):
    """Clareira que acompanha objetos em movimento (centros do plano, recalculados a cada quadro)."""
    def f(m):
        cs = centros()
        for s in m.submobjects:
            dentro = any(math.hypot(s._xy[0] - a, s._xy[1] - b) < r for a, b in cs)
            if dentro != getattr(s, "_escondida", False):
                op_seta(s, 0 if dentro else 1)
                s._escondida = dentro
    campo.add_updater(f)
    f(campo)
    return f


def segue(m, fpos):
    """Rótulo que acompanha um ponto: a cada quadro, desloca `m` pela variação de fpos() (px de 1080p)."""
    m._pxy = np.array(fpos(), float)

    def f(m_):
        n = np.array(fpos(), float)
        d = n - m_._pxy
        if abs(d[0]) + abs(d[1]) > 1e-6:
            m_.shift(np.array([d[0] / 120, -d[1] / 120, 0.0]))
            m_._pxy = n
    m.add_updater(f)
    return m


# ── v3 §4.1: sem quadro vazio nas trocas. As saídas (e a troca da linha 2 do canto no começo de um lote) ficam PENDENTES e acontecem dentro
#    da próxima animação de entrada, num trecho [t0, t1] dela (em s): a cena seguinte entra enquanto a anterior sai. ─────────────────────
def _rate_trecho(rt, t0, t1):
    def r(a):
        if a >= 1:
            return 1.0
        return smooth(min(1.0, max(0.0, (a * rt - t0) / max(1e-6, t1 - t0))))
    return r


def _sai_junto(self, *mobs, rt=0.4):
    """Os `mobs` (ou tudo, fora o canto) saem em `rt` s no começo da PRÓXIMA animação, junto com o que entra."""
    sai = list(mobs) or self.snap()
    self._junto = getattr(self, "_junto", []) + [("out", m, 0.0, rt) for m in sai]


def _limpa_junto(self, *keep, rt=0.4):
    _sai_junto(self, *[m for m in self.snap() if m not in keep], rt=rt)


_play_b = Base.play


def _play_junto(self, *anims, run_time=None, **kw):
    if getattr(self, "_r6_m", None) is not None:
        self.remove(self._r6_m)
        self.add(self._r6_m)
    jt = getattr(self, "_junto", None)
    if not jt:
        return _play_b(self, *anims, run_time=run_time, **kw)
    self._junto = []
    rt = run_time if run_time is not None else max([getattr(a, "run_time", 1.0) for a in anims] or [1.0])
    rt = max(rt, max(t1 for _, _, _, t1 in jt))
    ex, fora = [], []
    for k, m, t0, t1 in jt:
        r = _rate_trecho(rt, t0, t1)
        if k == "out":
            fora.append(m)
            ex.append(UpdateFromAlphaFunc(m.op, lambda o, a, r=r: o.set_value(1 - r(a))) if isinstance(m, Fundo3D) else FadeOut(m, rate_func=r))
        else:
            ex.append(FadeIn(m, rate_func=r))
    _play_b(self, *anims, *ex, run_time=rt, **kw)
    for m in fora:
        m.clear_updaters()
    self.remove(*fora)


_secao_b = Base.secao


def _secao_junto(self, s):
    """Linha 2 do canto. No começo de um lote (só o canto na tela), a troca vai junto da primeira entrada: a antiga sai em 0,25 s e a nova entra
    de 0,25 a 0,6 s, sem uma animação própria com a tela vazia."""
    if self.snap() or self.h2 is None or not s:
        return _secao_b(self, s)
    velho = self.h2
    self.h2 = self._canto(txt(s, 21.6, color="#F5F7FF", bold=True), CANTO_Y2, topo_min=self._y1_fim_px() + 10)
    self._junto = getattr(self, "_junto", []) + [("out", velho, 0.0, 0.25), ("in", self.h2, 0.25, 0.6)]


Base.play, Base.secao = _play_junto, _secao_junto
Base.sai_junto, Base.limpa_junto = _sai_junto, _limpa_junto


# ── v4 §4: pedacinho de fluido = chapa opaca coral escura + malha 4×4 + contorno coral, tudo levado pelo fluxo exato (pedaco() do sb27) ────────
PED_F, PED_L = "#6B3A4F", "#E89AAA"


def uv_quad(c, s):
    return lambda u, v: (c[0] - s / 2 + s * u, c[1] - s / 2 + s * v)


def uv_setor(r1, r2, a):
    return lambda u, v: ((r1 + (r2 - r1) * u) * np.cos(-a + 2 * a * v), (r1 + (r2 - r1) * u) * np.sin(-a + 2 * a * v))


class Pedaco(VGroup):
    """Mesma interface do Material (em(t), XY = borda no plano, P0): a borda e as 6 linhas da malha (3 em cada direção, S = 20 pontos por lado)
    são amostradas em (u, v) ∈ [0, 1]² e cada ponto anda pelo fluxo exato."""

    def __init__(self, v, uv, flow, n=4, S=20, z=7):
        super().__init__()
        self.v, self.flow, self.n, self.S = v, flow, n, S
        L = np.linspace(0, 1, S + 1)
        bu = np.concatenate([L, np.ones(S), L[::-1][1:], np.zeros(S)])
        bv = np.concatenate([np.zeros(S + 1), L[1:], np.ones(S), L[::-1][1:]])
        us, vs = [bu], [bv]
        for k in range(1, n):
            us += [np.full(S + 1, k / n), L]
            vs += [L, np.full(S + 1, k / n)]
        U_, V_ = np.concatenate(us), np.concatenate(vs)
        X0, Y0 = uv(U_, V_)
        self.X0, self.Y0, self.nb = np.asarray(X0, float), np.asarray(Y0, float), len(bu)
        self.P0 = np.stack([self.X0[:self.nb], self.Y0[:self.nb]], 1)
        self.chapa = VMobject().set_stroke(width=0).set_fill(PED_F, 1)
        self.malha = VGroup(*[VMobject().set_stroke(PED_L, 2 / 1.2, 1).set_fill(opacity=0) for _ in range(2 * (n - 1))])
        self.borda = VMobject().set_stroke(CORAL, 3.5 / 1.2, 1).set_fill(opacity=0)
        for m in (self.chapa, self.borda, *self.malha):
            m._sem_contorno = True
            m.cap_style = CapStyleType.ROUND
        self.add(self.chapa, self.malha, self.borda)
        self.set_z_index(z)
        self.em(0.0)

    def em(self, t):
        X, Y = self.flow(self.X0, self.Y0, t) if abs(t) > 1e-12 else (self.X0, self.Y0)
        X, Y = np.asarray(X, float), np.asarray(Y, float)
        P = np.stack([X, Y, 0 * X], 1) * [self.v.ux, self.v.uy, 0] + self.v.o if hasattr(self.v, "ux") else np.array([self.v.c2p(a, b) for a, b in zip(X, Y)])
        nb, S = self.nb, self.S
        borda = np.concatenate([P[:nb], P[:1]])
        self.chapa.set_points_as_corners(borda)
        self.borda.set_points_as_corners(borda)
        for k, m in enumerate(self.malha):
            m.set_points_as_corners(P[nb + k * (S + 1): nb + (k + 1) * (S + 1)])
        self.t, self.XY = t, np.stack([X[:nb], Y[:nb]], 1)
        return self


def contorno_ini(v, pts):
    """Contorno inicial tracejado, coral a 60 %."""
    P = [tuple(p) for p in pts] + [tuple(pts[0])]
    return vlinha(v, P, CORAL, 3, alpha=0.6, dash=(8, 8))


# ── v4 R6: QA de sobreposição a cada 0,2 s DURANTE o render (inclusive Transform/FadeIn/FadeOut), com QA_SOBREPOS=1 ─────────────────────
#    texto×texto (caixas + 4 px), seta de campo visível com o centro numa caixa de texto (+4 px) ou cruzando a caixa, imagem (chapa) sobre seta
#    de campo visível, e DUPLICATA (dois MathTex com a mesma string visíveis). Saída: linhas [r6] no log; qa_sobrepos_rel.py junta.
def _op_texto(x):
    ops = [g.get_fill_opacity() for g in x.family_members_with_points()]
    return max(ops) if ops else 0.0


def _seg_cruza(a, b, x0, y0, x1, y1):
    """O segmento a→b cruza o retângulo (Liang–Barsky)?"""
    dx, dy = b[0] - a[0], b[1] - a[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
        if abs(p) < 1e-12:
            if q < 0:
                return False
            continue
        r = q / p
        if p < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return False
    return True


def _r6(self, dt=0):
    f = int(round(self.clk.get_value() * FPS))
    if f % 3 or f == getattr(self, "_r6_f", None):
        return
    self._r6_f = f
    fix = self.fixos()
    textos, setas, imgs, vistas = [], [], [], set()
    for m in self.mobjects:
        if m in fix or m is self.clk or isinstance(m, (ValueTracker, Fundo3D)):
            continue
        for x in m.get_family():
            if id(x) in vistas:
                continue
            vistas.add(id(x))
            if isinstance(x, DecimalNumber):
                vistas |= {id(g) for g in x.get_family()}
                if _op_texto(x) > 0.3:
                    textos.append(x)
            elif isinstance(x, (MathTex, SingleStringMathTex, Text)) or type(x).__name__ == "MarkupText":
                if _op_texto(x) > 0.3:
                    textos.append(x)
            elif hasattr(x, "_xy") and hasattr(x, "haste"):
                if x.haste.get_stroke_opacity() > 0.3 and not getattr(x, "_escondida", False):
                    setas.append(x)
            elif isinstance(x, ImageMobject) and x.get_family() and float(np.max(x.pixel_array[..., 3])) > 0.3 * 255:
                imgs.append(x)
    ids, tops = set(), []
    for t in textos:
        if id(t) in ids:
            continue
        tops.append(t)
        ids |= {id(g) for g in t.get_family()}
    m4 = 4 / 120
    cx = [(t, *t.get_corner(DL)[:2], *t.get_corner(UR)[:2]) for t in tops]
    oc = []
    for i, (a, ax0, ay0, ax1, ay1) in enumerate(cx):
        for b, bx0, by0, bx1, by1 in cx[i + 1:]:
            if ax0 - m4 < bx1 and bx0 - m4 < ax1 and ay0 - m4 < by1 and by0 - m4 < ay1:
                oc.append(f"texto×texto {nome_t(a)!r} × {nome_t(b)!r}")
        for s in setas:
            c = s.get_center()
            if ax0 - m4 < c[0] < ax1 + m4 and ay0 - m4 < c[1] < ay1 + m4:
                oc.append(f"seta×texto(centro) {nome_t(a)!r} (seta {tuple(round(v, 2) for v in s._xy)})")
                break
            if _seg_cruza(s.haste.get_start()[:2], s.ponta.get_center()[:2], ax0 + 2 / 120, ay0 + 2 / 120, ax1 - 2 / 120, ay1 - 2 / 120):
                oc.append(f"seta×texto(cruza) {nome_t(a)!r} (seta {tuple(round(v, 2) for v in s._xy)})")
                break
    for im in imgs:
        x0, y0 = im.get_corner(DL)[:2]
        x1, y1 = im.get_corner(UR)[:2]
        n = sum(1 for s in setas if x0 < s.get_center()[0] < x1 and y0 < s.get_center()[1] < y1)
        if n:
            oc.append(f"imagem×campo: {n} setas de campo sob uma imagem de {im.width * 120:.0f}×{im.height * 120:.0f} px")
    vistos = {}
    for t in tops:
        if isinstance(t, MathTex):
            k = getattr(t, "_tex", None) or t.get_tex_string()
            if len(k) < 8:                    # valores repetidos de propósito (0,219 nas duas paredes, o "0" de cada painel) não são duplicata
                continue
            if k in vistos:
                oc.append(f"DUPLICATA {k[:50]!r}")
            vistos[k] = t
    for o in oc:
        print(f"[r6] {self.lote} {f / FPS:7.2f}s {self._aid}: {o}")
    self._r6_n = getattr(self, "_r6_n", 0) + 1


_setup_r6 = Base.setup_base


def _setup_com_r6(self):
    _setup_r6(self)
    if os.environ.get("QA_SOBREPOS") == "1":
        self._r6_m = VMobject()                       # sonda: updater de objeto, recolocada no FIM da cena a cada play (roda depois das clareiras)
        self._r6_m.add_updater(lambda m, dt: _r6(self, dt))
        self.add(self._r6_m)


Base.setup_base = _setup_com_r6

_fixos_b = Base.fixos


def _fixos_r6(self):
    f = _fixos_b(self)
    if getattr(self, "_r6_m", None) is not None:
        f.add(self._r6_m)                              # a sonda do R6 nunca sai com limpa()/snap()
    return f


Base.fixos = _fixos_r6


def legenda_mat(partes, x, y, cor=SAIF, al="center", size=28):
    """Legenda com símbolo matemático no meio (o txt() põe tudo em caixa alta): partes = [texto | (tex,)], na mesma linha de base."""
    ms = []
    for p in partes:
        if isinstance(p, tuple):
            m = MathTex(p[0], font_size=fs(size * 1.25), tex_template=TEX27, color=cor)
            m._tex, m._esc = p[0], True
            for g in m.get_family():
                g._sem_contorno = True
        else:
            m = legenda(p, 0, y, cor, "left", size)
        ms.append(m)
    g = VGroup(*ms).arrange(RIGHT, buff=0.1, center=False)           # center=False: o arrange não move o grupo para o meio da tela
    yc = ms[0].get_center()[1]                                          # centro da caixa alta do texto
    for m, p in zip(ms[1:], partes[1:]):
        if isinstance(p, tuple):
            m.shift(UP * (yc - m.get_center()[1]))
    dx = PX(x, 0)[0]
    g.shift(RIGHT * (dx - (g.get_center()[0] if al == "center" else g.get_left()[0])))
    return g



# ── final (voz real): PLANO DE SINCRONIA ─────────────────────────────────────────────────────────────────────────────────────
# Trecho = do fim de um gat()/an() até o próximo gat()/_fecha(). Passagem seca com SYNC_PLANO=gravar → qa/plano/<lote>.json (por trecho: c = s de
# play dominado por caneta, o = s do resto, e o fim do trecho). No render, no começo de cada trecho, se c + o não cabe até o alvo do fim, a caneta
# dos plays desse trecho encolhe (fator f ≥ 0,20 s/glifo ÷ passo). Só a caneta muda; a voz nunca.
import kit as _kit  # noqa: E402

_PLANO_DIR = Path(__file__).resolve().parent / "qa" / "plano"
_GRAVA = os.environ.get("SYNC_PLANO") == "gravar"


def _plano(self):
    if not hasattr(self, "_sp"):
        self._sp = {"k": 0, "c": 0.0, "o": 0.0, "segs": [], "f": 1.0, "elast": 0}
        arq = _PLANO_DIR / f"{self.lote}.json"
        self._sp["lido"] = None if _GRAVA or not arq.exists() else json.loads(arq.read_text(encoding="utf-8"))
    return self._sp


def _fronteira(self, tipo, frase=None, antes=0.0):
    sp = _plano(self)
    sp["segs"].append({"c": round(sp["c"], 3), "o": round(sp["o"], 3), "fim": tipo, "aid": self._aid, "frase": frase, "antes": antes})
    sp["k"] += 1
    sp["c"] = sp["o"] = 0.0
    sp["f"] = 1.0


def _comeca(self):
    """Início de trecho (fim de gat/an): calcula o fator da caneta pelo plano gravado."""
    sp = _plano(self)
    sp["f"] = 1.0
    pl = sp["lido"]
    if not pl or sp["k"] >= len(pl) or self._aid is None:
        return
    g = pl[sp["k"]]
    if g["fim"] == "gat":
        k = self._k_frase(self._aid, g["frase"])
        if k is None:
            return
        alvo = self._q0 + max(0.0, ANC[self._aid]["t"][k] - LEAD) * FPS
    else:
        alvo = self.alvo - round(g.get("antes", 0.0) * FPS)
    disp = (alvo - self.nq) / FPS - 0.05
    if g["c"] > 0 and g["c"] + g["o"] > disp:
        sp["f"] = min(1.0, max(0.0, (disp - g["o"]) / g["c"]))
        print(f"[sync] {self.lote} trecho {sp['k']} ({self._aid} → {g['fim']} {g['frase'] or ''}): pede {g['c'] + g['o']:.2f}s, cabe {disp:.2f}s → caneta × {sp['f']:.2f}")


_gat_s0 = Base.gat


def _gat_sync(self, frase):
    _fronteira(self, "gat", frase)
    _plano(self)["elast"] += 1
    _gat_s0(self, frase)
    _plano(self)["elast"] -= 1
    _comeca(self)


_fecha_s0 = Base._fecha


def _fecha_sync(self, antes=0.0):
    if self._aid is not None:
        _fronteira(self, "fecha", None, antes)
    _plano(self)["elast"] += 1
    _fecha_s0(self, antes=antes)
    _plano(self)["elast"] -= 1


_an_s0 = Base.an


def _an_sync(self, aid):
    _an_s0(self, aid)
    _comeca(self)


_ate_s0 = Base.ate


def _ate_sync(self, frac):
    _plano(self)["elast"] += 1
    _ate_s0(self, frac)
    _plano(self)["elast"] -= 1


_wait_s0 = Base.wait


def _wait_sync(self, duration=1.0, *a, **kw):
    sp = _plano(self)
    if not sp["elast"]:
        sp["o"] += max(1, round(duration * FPS)) / FPS
    _wait_s0(self, duration, *a, **kw)


_play_s0 = Base.play


def _play_sync(self, *anims, run_time=None, **kw):
    sp = _plano(self)
    f = sp["f"]
    tc = 0.0
    for a in anims:
        if isinstance(a, _kit._Caneta):
            if f < 1.0 and not getattr(a, "_sync", False):
                ff = max(f, 0.20 / a.passo)
                if ff < 1.0:
                    a.passo, a.dg, a.atraso = a.passo * ff, a.dg * ff, a.atraso * ff
                    a.tot = a.atraso + a.passo * max(0, a.n - 1) + a.dg
                    a.run_time = a.tot
                a._sync = True
            tc = max(tc, a.run_time)
    rt = run_time if run_time is not None else max([getattr(a, "run_time", 1.0) for a in anims] or [1.0])
    q = max(1, round(rt * FPS)) / FPS
    if tc > 0 and tc >= rt - 1e-6:
        sp["c"] += q
    else:
        sp["o"] += q
    return _play_s0(self, *anims, run_time=run_time, **kw)


_fim_s0 = Base.fim


def _fim_sync(self):
    _fim_s0(self)
    sp = _plano(self)
    sp["segs"].append({"c": round(sp["c"], 3), "o": round(sp["o"], 3), "fim": "fim", "aid": None, "frase": None, "antes": 0.0})
    if _GRAVA:
        _PLANO_DIR.mkdir(parents=True, exist_ok=True)
        (_PLANO_DIR / f"{self.lote}.json").write_text(json.dumps(sp["segs"], ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"[sync] plano gravado: {len(sp['segs'])} trechos")


Base.gat, Base._fecha, Base.an, Base.ate, Base.wait, Base.play, Base.fim = _gat_sync, _fecha_sync, _an_sync, _ate_sync, _wait_sync, _play_sync, _fim_sync


def _em(self, frase, anim):
    """final: evento agendado DENTRO de um play (Succession(Wait, anim)) para cair na palavra `frase` sem segurar a animação em curso.
    Só para destaque de objeto já visível (pulso, movimento); nunca para fazer surgir fórmula. Loga como [gatilho] com o atraso previsto."""
    k = self._k_frase(self._aid, frase)
    if k is None:
        print(f"[gatilho-sem-frase] {self._aid}: {frase!r}")
        return anim
    alvo = self._q0 + max(0.0, ANC[self._aid]["t"][k] - LEAD) * FPS
    w = max(0.0, (alvo - self.nq) / FPS)
    wq = round(w * FPS) / FPS
    print(f"[gatilho] {self._aid} {(self.nq - self._q0) / FPS + wq:6.2f}s (alvo {(alvo - self._q0) / FPS:6.2f}s, atraso {(self.nq + wq * FPS - alvo) / FPS:+.2f}s) {frase} (agendado)")
    return Succession(Wait(wq), anim) if wq > 0 else anim


Base.em = _em


def _surge(self, *ms):
    """final: objeto que precisa aparecer DENTRO de um play já em curso (via self.em): entra na cena já invisível e volta com Restore
    (nada de prévia do destino: o objeto não é desenhado antes da vez)."""
    for m in ms:
        m.save_state()
        m.set_opacity(0)
        self.add(m)
    return AnimationGroup(*[Restore(m) for m in ms])


Base.surge = _surge


def _sai_entra(self, sai, entra, f=0.45):
    """final (R6 nas transições): num play só, o que sai some na primeira fração `f` e o que entra aparece depois (rate_func remapeada).
    Dentro de um play o Manim estica toda animação para a duração do play; o run_time individual não vale."""
    out = [FadeOut(m, rate_func=lambda a: smooth(min(1.0, a / f))) for m in sai]
    for x in entra:
        rf = x.rate_func
        x.rate_func = (lambda a, rf=rf: rf(max(0.0, (a - f) / (1.0 - f))))
    return out + list(entra)


def so_no_inicio(cn, seg=0.4):
    """rate_func para uma saída que acontece nos primeiros `seg` s de um play cuja duração é a da caneta `cn` (lida na hora: o plano de sincronia
    pode encolher a caneta)."""
    return lambda a: smooth(min(1.0, a * cn.tot / seg))


Base.sai_entra = _sai_entra


# ── final (11/11): fundo violeta + grade que nasce dos eixos (papel27.py) ───────────────────────────────────────────────────────
from papel27 import area_px, papel  # noqa: E402,F401


def _grade(self, *novas, rt=0.45):
    """Troca a grade (as atuais saem, `novas` entram) JUNTO do próximo play (sem tempo próprio). Sem argumentos: fundo liso (cenas 3D)."""
    velhas = [g for g in self._grades if g not in novas]
    entra = [g for g in novas if g not in self._grades]
    self._junto = getattr(self, "_junto", []) + [("out", g, 0.0, rt) for g in velhas] + [("in", g, 0.0, rt) for g in entra]
    self._grades = list(novas)


Base.grade = _grade
_sai_fim_g = Base.sai_fim


def _sai_fim_grade(self, rt=0.35):
    if self._grades != [self.grade0]:
        self.grade(self.grade0, rt=rt)          # o lote termina na grade padrão (o seguinte começa nela)
    _sai_fim_g(self, rt)


Base.sai_fim = _sai_fim_grade
