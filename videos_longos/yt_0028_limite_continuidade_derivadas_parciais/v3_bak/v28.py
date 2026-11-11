"""yt_0028 (copiado de ../yt_0027_rotacional_divergente/v27.py, sem importar; acréscimos do sb28.html no fim do arquivo). Origem: yt_0027 · v2 — helpers do sistema visual do yt_0026 v7/v8 (copiados de ../yt_0026_funcoes_vetoriais_campos/v7.py, sem importar de lá) e as peças
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
def T(s, x, y, size=30, al="left", cor=WHITE_, bold=True, up=True):
    """Texto (fillText do storyboard): y = linha de base em px."""
    m = txt(s, ts(size), color=cor, bold=bold, up=up)
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


def legenda(s, x, y, cor=SAIF, al="left", size=28, up=True):
    return T(s, x, y, size, al, cor, bold=False, up=up)


TEX27 = TexTemplate()
TEX27.add_to_preamble(
    r"\usepackage{xcolor}"
    r"\definecolor{ca}{HTML}{FFC24D}\definecolor{cm}{HTML}{EA63FF}\definecolor{cz}{HTML}{35D9FF}\definecolor{cc}{HTML}{2EE6A0}"
    r"\definecolor{cs}{HTML}{7FB2FF}\definecolor{cv}{HTML}{9C8CFF}\definecolor{cr}{HTML}{FF7A8A}\definecolor{cj}{HTML}{3FE08B}"
    r"\definecolor{cg}{HTML}{B8C4DA}\definecolor{cp}{HTML}{E08A3C}"
    r"\def\X{\textcolor{ca}{x}}\def\Y{\textcolor{cm}{y}}\def\Z{\textcolor{cz}{z}}\def\F{\textcolor{cc}{\vec F}}"
    r"\def\Pp{\textcolor{cc}{P}}\def\Qq{\textcolor{cc}{Q}}\def\Rr{\textcolor{cc}{R}}"
    r"\def\dx{\partial \textcolor{ca}{x}}\def\dy{\partial \textcolor{cm}{y}}\def\dz{\partial \textcolor{cz}{z}}"
    r"\def\w{\textcolor{cv}{\omega}}\def\V#1{\textcolor{cv}{#1}}\def\D#1{\textcolor{cs}{#1}}\def\C#1{\textcolor{cr}{#1}}\def\Pt{\textcolor{cp}{P}}"
    r"\def\rot{\operatorname{rot}}\def\dv{\operatorname{div}}\def\h{\textcolor{ca}{h}}\def\k{\textcolor{cm}{k}}"
    r"\def\xo{\textcolor{ca}{x_0}}\def\yo{\textcolor{cm}{y_0}}\def\E{\textcolor{cc}{\vec E}}\def\B{\textcolor{cm}{\vec B}}"
    r"\def\J{\textcolor{cj}{\vec J}}\def\phi{\textcolor{cs}{\varphi}}\def\T{\textcolor{cs}{T}}\def\kk{\vec k}"
    r"\definecolor{cl}{HTML}{C6F26B}\definecolor{ce}{HTML}{8CFFD2}"
    r"\def\G{\textcolor{cc}{\vec G}}\def\Lm{\textcolor{cl}}\def\Am{\textcolor{ca}}\def\Mg{\textcolor{cm}}\def\Xp{\textcolor{cp}{X}}"
    r"\def\eps{\textcolor{ce}{\varepsilon}}\def\del{\textcolor{cp}{\delta}}\def\Lv{\textcolor{cc}{\vec L}}\def\sen{\operatorname{sen}}")


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


def _fecha_qa(self):
    if self._aid is not None and os.environ.get("QA_COLISAO") == "1":
        if self.alvo - self.nq >= 1:
            self.wait((self.alvo - self.nq) / FPS)
        qa_colisao(self, self._aid)
    _fecha0(self)


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


def _fecha_sob(self):
    if self._aid is not None and os.environ.get("QA_SOBREPOS") == "1":
        qa_sobreposicao(self, f"{self._aid} fim")
    _fecha1(self)


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


# ═════════════ yt_0028 (sb28.html, handoff v1.2): campos, clareira R1, pedacinho de fluido com malha, QA R5 da seta inteira ═════════════
from MF_Tools import TransformByGlyphMap  # noqa: E402

LIMA, MALHA = "#C6F26B", "#FFB3BC"
CHAPA_C = mix(CORAL, FUNDO_C, 0.62).to_hex()          # chapa do pedacinho (coral misturado 62 % com o fundo, opaca)


# ── campos do vídeo (handoff §4) ──
def F_AULA(x, y):
    return (1 + np.sin(x) - np.sin(y), 2 * np.sin(x) + 2 - np.cos(x) - np.cos(y))


def F_DIAG(x, y):
    r2 = x * x + y * y
    return (0.0, 0.0) if r2 < 1e-12 else (2 * x * y / r2, 0.0)


def F_CARGA(x, y):
    r3 = (x * x + y * y) ** 1.5
    return (x / r3, y / r3)


F_TROCA = lambda x, y: (y, x)
F_LIN = lambda x, y: (x - y, 2 * x)                   # modelo linear local J·H (B6-3 em diante)


def F_RESID(x, y):
    a = F_AULA(x / 10, y / 10)
    return ((a[0] - 1) * 10, (a[1] - 0) * 10)


def F_ZOOM(x, y):
    return F_AULA(x / 10, y / 10)


JA = np.array([[1.0, -1.0], [2.0, 0.0]])


def expJA(t):
    """exp(tJ) = e^{t/2}[cos(ωt) I + sen(ωt)/ω (J − I/2)], ω = √7/2 (handoff §4)."""
    w = math.sqrt(7) / 2
    e, c, s = math.exp(t / 2), math.cos(w * t), math.sin(w * t) / w
    return e * (c * np.eye(2) + s * (JA - 0.5 * np.eye(2)))


def fl_J(x, y, t):
    M = expJA(t)
    return M[0, 0] * x + M[0, 1] * y, M[1, 0] * x + M[1, 1] * y


def fl_troca(x, y, t):
    c, s = math.cosh(t), math.sinh(t)
    return c * x + s * y, s * x + c * y


def fl_escala(kx, ky):
    """Fluxo diagonal que chega em (×kx, ×ky) em t = 1 (cartões do B7)."""
    return lambda x, y, t: (x * kx ** t, y * ky ** t)


def fl_rot(ang):
    return lambda x, y, t: fl_giro(x, y, ang * t)


# ── clareira (R1) do sb28: retângulos e discos com 0,25 u de margem; polígono; segmentos ──
def clar28(rects=(), discos=()):
    return lambda X, Y: any(a - .25 < X < c + .25 and b - .25 < Y < d + .25 for a, b, c, d in rects) or any(math.hypot(X - a, Y - b) < r + .25 for a, b, r in discos)


def dseg(X, Y, a, b):
    p, q = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((X - a[0]) * p + (Y - a[1]) * q) / (p * p + q * q)))
    return math.hypot(X - a[0] - t * p, Y - a[1] - t * q)


def dentro(X, Y, pts):
    c = False
    j = len(pts) - 1
    for i in range(len(pts)):
        a, b = pts[i]
        e, f = pts[j]
        if (b > Y) != (f > Y) and X < (e - a) * (Y - b) / (f - b) + a:
            c = not c
        j = i
    return c


def clarPoly(pts, m=.25):
    pts = [tuple(p) for p in pts]
    return lambda X, Y: dentro(X, Y, pts) or any(dseg(X, Y, p, pts[(i + 1) % len(pts)]) < m for i, p in enumerate(pts))


def clarSeg(segs, m=.2):
    return lambda X, Y: any(dseg(X, Y, a, b) < m for a, b in segs)


def ou(*fs):
    fs = [f for f in fs if f]
    return lambda X, Y: any(f(X, Y) for f in fs)


NADA = lambda X, Y: False


# ── setas ──
def seta_prop(v, X, Y, f, lmax, ctx=False, cor=None, w=5, head=19):
    """Seta proporcional (só o campo G, |G| ≤ 1): L = lmax·|G|; menos de 6 px não é desenhada."""
    m = math.hypot(*f)
    if m * lmax * v.u < 6:
        return None
    u = (f[0] * lmax, f[1] * lmax)
    c = ManimColor(cor) if cor else (ManimColor(CTX) if ctx else mix(CAMPO, CAMPO2, m))
    s = seta7(v.c2p(X - u[0] / 2, Y - u[1] / 2), v.c2p(X + u[0] / 2, Y + u[1] / 2), c, w, head)
    s._xy, s._L, s._t, s._f = (X, Y), m * lmax, min(1.0, m), f
    return s


def campo28(v, Fv, x0=-3.5, x1=3.5, y0=-3, y1=3, passo=.5, rmin=.3, rmax=9, mmax=1.0, ctx=False, prop=False, skip=None, nome="campo"):
    """campo() do sb28: grade (x0..x1, y0..y1) a cada `passo`, sem as setas com r < rmin ou r > rmax. `skip` = clareira FIXA (não desenha)."""
    g = Campo7()
    g._cor = None
    lmax = .84 * passo
    n = int(math.floor((x1 - x0) / passo + 1e-6))
    m = int(math.floor((y1 - y0) / passo + 1e-6))
    for i in range(n + 1):
        for j in range(m + 1):
            X, Y = x0 + i * passo, y0 + j * passo
            r = math.hypot(X, Y)
            if r < rmin or r > rmax or (skip and skip(X, Y)):
                continue
            f = Fv(X, Y)
            s = seta_prop(v, X, Y, f, lmax, ctx) if prop else seta_campo(v, X, Y, f, lmax, mmax, ctx)
            if s is not None:
                g.add(s)
    g._v, g._passo = v, passo
    if len(g):
        g.log(nome, passo)
    return g.set_z_index(3)


def mesma_grade(cmp, Fv, mmax, ctx=False):
    """Campo novo na MESMA grade de `cmp` (seta a seta, mesma ordem): alvo de um Transform único das setas."""
    g = Campo7()
    g._cor = None
    for s in cmp:
        X, Y = s._xy
        n = seta_campo(cmp._v, X, Y, Fv(X, Y), .84 * cmp._passo, mmax, ctx)
        if n is None:
            n = s.copy()
            n.set_opacity(0)
            n._xy = (X, Y)
        g.add(n)
    g._v, g._passo = cmp._v, cmp._passo
    return g.set_z_index(3)


def herda(cmp, novo):
    """Depois do Transform: as setas de `cmp` passam a carregar os dados (_t, _f, _L) das de `novo`."""
    for a, b in zip(cmp, novo):
        a._t, a._f, a._L = getattr(b, "_t", 0), getattr(b, "_f", (0, 0)), getattr(b, "_L", 0)


# ── clareira viva (R1 com objetos que andam): teste(X, Y) avaliado a cada quadro ──
def clareira(campo, teste_fn):
    """`teste_fn()` devolve o teste atual (X, Y) → bool; a seta some (opacidade real 0, marcada _escondida) enquanto o teste for verdadeiro."""
    def f(m):
        t = teste_fn()
        for s in m.submobjects:
            if not hasattr(s, "_xy"):
                continue
            d = bool(t(*s._xy))
            if d != getattr(s, "_escondida", False):
                op_seta(s, 0 if d else 1)
                s._escondida = d
    campo.add_updater(f)
    f(campo)
    return f


# ── pedacinho de fluido (v1.1): chapa opaca + malha 4×4 + contorno coral; transformado inteiro pelo mesmo mapa ──
class Pedaco(VGroup):
    def __init__(self, v, pts, n=4, k=24, z=7):
        super().__init__()
        self.v = v
        A, B, C, D = [np.asarray(p, float) for p in pts]
        L = lambda a, b, t: a + (b - a) * t
        u = np.linspace(0, 1, k)[:, None]
        self.borda0 = np.concatenate([L(A, B, u), L(B, C, u), L(C, D, u), L(D, A, u)])
        self.linhas0 = []
        for i in range(1, n):
            t = i / n
            self.linhas0.append(L(L(A, B, t), L(D, C, t), u))
            self.linhas0.append(L(L(A, D, t), L(B, C, t), u))
        self.ch = VMobject().set_fill(CHAPA_C, 1).set_stroke(width=0)
        self.ls = VGroup(*[VMobject().set_stroke(MALHA, 2 / 1.2, 1).set_fill(opacity=0) for _ in self.linhas0])
        self.ct = VMobject().set_stroke(CORAL, 4 / 1.2, 1).set_fill(opacity=0)
        self.ct.joint_type = LineJointType.ROUND
        for m in (self.ch, self.ct, *self.ls):
            m._sem_contorno = True
        self.add(self.ch, self.ls, self.ct)
        self.set_z_index(z)
        self.ls.set_z_index(z + 0.1)
        self.ct.set_z_index(z + 0.2)
        self.forma(lambda X, Y: (X, Y))

    def forma(self, fn):
        n = len(self.borda0)
        bx, by = fn(self.borda0[:, 0], self.borda0[:, 1])
        self.XY = np.stack([np.asarray(bx, float) * np.ones(n), np.asarray(by, float) * np.ones(n)], 1)
        P = [self.v.c2p(a, b) for a, b in self.XY]
        self.ch.set_points_as_corners(P + [P[0]])
        self.ct.set_points_as_corners(P + [P[0]])
        for m, l0 in zip(self.ls, self.linhas0):
            k = len(l0)
            lx, ly = fn(l0[:, 0], l0[:, 1])
            m.set_points_as_corners([self.v.c2p(a, b) for a, b in zip(np.asarray(lx, float) * np.ones(k), np.asarray(ly, float) * np.ones(k))])
        return self

    def em(self, fl, t):
        return self.forma(lambda X, Y: fl(X, Y, t))

    def poly(self, n=48):
        idx = np.linspace(0, len(self.XY) - 1, n).astype(int)
        return [tuple(p) for p in self.XY[idx]]

    def area(self):
        return area_poly(self.XY)


def fantasma(v, pts, w=3, z=6):
    """Estado inicial: só o contorno tracejado coral (3 px, 70 %), sem malha."""
    q = list(pts) + [pts[0]]
    return vlinha(v, q, CORAL, w, alpha=0.7, dash=(9, 8)).set_z_index(z)


def quad_pts(c, s):
    return [(c[0] - s / 2, c[1] - s / 2), (c[0] + s / 2, c[1] - s / 2), (c[0] + s / 2, c[1] + s / 2), (c[0] - s / 2, c[1] + s / 2)]


def anda(ped, fl, t1, rt, t0=0.0, rate=smooth, nome=""):
    """Fluxo exato UMA vez (t0 → t1 do fluxo em rt s de tela)."""
    print(f"[motor] {nome}: fluxo de {t0:.3f} a {t1:.3f} em {rt:.2f} s")
    return UpdateFromAlphaFunc(ped, lambda m, a: m.em(fl, t0 + (t1 - t0) * rate(a)), run_time=rt)


# ── álgebra ──
def tbgm(a, b, *mapa, rt=1.4, copia=False):
    an = TransformByGlyphMap(a, b, *mapa, from_copy=copia, auto_fade=True, printing=False, run_time=rt)
    ja_escrita(b)
    return an


def linha_partes(partes, xc, y, size, gap=34, al="c"):
    """Várias fórmulas numa linha só (cada uma escrita na sua vez pela caneta): centradas em xc (ou alinhadas à esquerda em xc)."""
    ms = [TC(p, 960, y, size, "c") for p in partes]
    ws = [m.width for m in ms]
    tot = sum(ws) + gap / 120 * (len(ms) - 1)
    x = PX(xc, 0)[0] - (tot / 2 if al == "c" else 0)
    for m, w in zip(ms, ws):
        m.shift(RIGHT * (x - m.get_left()[0]))
        x += w + gap / 120
    return ms


def colunas_matriz(m):
    """Glifos de uma matriz 2×2 num MathTex: (parênteses grandes [esq, dir], coluna 1, coluna 2, glifos antes da matriz)."""
    gs = glifos(m)
    H = max(g.height for g in gs)
    par = sorted([g for g in gs if g.height > 0.6 * H], key=lambda g: g.get_center()[0])
    pl, pr = par[0], par[-1]
    dentro_ = [g for g in gs if pl.get_right()[0] - 1e-3 < g.get_center()[0] < pr.get_left()[0] + 1e-3 and g is not pl and g is not pr]
    xs = sorted(dentro_, key=lambda g: g.get_center()[0])
    cx = [g.get_center()[0] for g in xs]
    k = int(np.argmax(np.diff(cx))) + 1
    antes = [g for g in gs if g.get_center()[0] < pl.get_center()[0]]
    return [pl, pr], xs[:k], xs[k:], antes


def idx_de(m, gs):
    todos = list(m[0])
    ids = [id(x) for x in todos]
    return [ids.index(id(g)) for g in gs if id(g) in ids]


# ── QA R5 (handoff v1.2 §8.2): a seta INTEIRA (haste e ponta, + 4 px + meia espessura) contra a caixa de cada texto ──
def _amostras_seta(s, n=24):
    a, b = s.haste.get_start(), s.haste.get_end()
    u = np.linspace(0, 1, n)[:, None]
    pts = [a * (1 - u) + b * u]
    tri = np.asarray(s.ponta.get_vertices())[:3]
    for i in range(3):
        pts.append(tri[i] * (1 - u) + tri[(i + 1) % 3] * u)
    return np.concatenate(pts)[:, :2]


def qa_sobreposicao(cena, onde):
    fix = cena.fixos()
    textos, setas, vistas = [], [], set()
    for m in cena.mobjects:
        if m in fix or isinstance(m, ValueTracker):
            continue
        for x in m.get_family():
            if isinstance(x, (MathTex, SingleStringMathTex, Text)) or type(x).__name__ in ("MarkupText",):
                if any(len(g.points) and g.get_fill_opacity() > 0.3 for g in x.family_members_with_points()):
                    textos.append(x)
            if hasattr(x, "_xy") and hasattr(x, "haste") and id(x) not in vistas:
                vistas.add(id(x))
                if x.haste.get_stroke_opacity() > 0.3 and not getattr(x, "_escondida", False):
                    setas.append(x)
    ids, tops = set(), []
    for t in textos:
        if id(t) in ids:
            continue
        tops.append(t)
        ids |= {id(g) for g in t.get_family()}
    caixas = [(t, t.get_corner(DL)[:2], t.get_corner(UR)[:2]) for t in tops]
    amos = [(s, _amostras_seta(s), (4 + s._w * 1.2 / 2) / 120) for s in setas]
    ocorr = []
    for i in range(len(caixas)):
        a, (ax0, ay0), (ax1, ay1) = caixas[i]
        for j in range(i + 1, len(caixas)):
            b, (bx0, by0), (bx1, by1) = caixas[j]
            if ax0 < bx1 and bx0 < ax1 and ay0 < by1 and by0 < ay1:
                ocorr.append(f"texto×texto {nome_t(a)!r} × {nome_t(b)!r}")
        for s, P, m4 in amos:
            if np.any((P[:, 0] > ax0 - m4) & (P[:, 0] < ax1 + m4) & (P[:, 1] > ay0 - m4) & (P[:, 1] < ay1 + m4)):
                ocorr.append(f"seta×texto {nome_t(a)!r} (seta em {tuple(round(float(v), 2) for v in s._xy)})")
                break
    for o in ocorr:
        print(f"[sobrepos] {onde}: {o}")
    print(f"[sobrepos-chk] {onde}: {len(tops)} textos, {len(setas)} setas visíveis, {len(ocorr)} ocorrências")
    return len(ocorr)


def limpa_soltos(cena):
    """O TransformByGlyphMap deixa grupos vazios soltos na cena; tira os que não têm mais pontos."""
    for m in list(cena.mobjects):
        if isinstance(m, VGroup) and not len(m.family_members_with_points()):
            cena.remove(m)


def logo_cta(cena, rt_fim=3.0):
    """CTA padrão do canal (yt_0027 S4): tudo sai; logo com os dois anéis; INSCREVA-SE até o fim da fala + 3 s."""
    CL = P3(0, 0.9)
    logo = cena.logo(5.6).move_to(CL)
    aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(CL), num_dashes=48).set_stroke(GEO, 2.6, opacity=o) for r, o in ((2.1, 0.85), (2.45, 0.6))])
    for m_ in aneis.get_family():
        m_._sem_contorno = True
    ins = VGroup(T("INSCREVA-SE PARA ACOMPANHAR", 960, 0, 66, "center"), T("OS PRÓXIMOS VÍDEOS", 960, 0, 66, "center")).arrange(DOWN, buff=0.12).move_to(P3(0, -2.6))
    s4 = cena.snap()
    sai_c = [m_ for m_ in (cena.h2,) if m_ is not None]
    cena.play(*[FadeOut(m_) for m_ in s4 + sai_c], FadeIn(logo, scale=0.96), FadeIn(aneis), FadeIn(ins, shift=0.1 * UP), run_time=0.6)
    cena.remove(*s4, *sai_c)
    cena.h2 = None
    rt = cena.resta() + rt_fim
    cena.play(Rotate(aneis[0], 0.3 * rt, rate_func=linear), Rotate(aneis[1], -0.24 * rt, rate_func=linear), run_time=rt)


# ── a clareira viva roda como updater do GRUPO do campo; o cresce_campo põe as setas soltas na cena. Antes de cada play/wait, um campo com
#    clareira cujas setas estão soltas na cena volta a entrar como grupo (senão o updater não roda). ──
_REG = []
_clar0 = clareira


def clareira(campo, teste_fn):
    if campo not in _REG:
        _REG.append(campo)
    return _clar0(campo, teste_fn)


def _junta(self):
    ms = self.mobjects
    for c in _REG:
        if c in ms or not c.get_updaters():
            continue
        soltas = [s for s in c.submobjects if s in ms]
        if soltas:
            self.remove(*soltas)
            self.add(c)


_play28, _wait28 = Base.play, Base.wait


def _play_j(self, *a, **k):
    _junta(self)
    return _play28(self, *a, **k)


def _wait_j(self, *a, **k):
    _junta(self)
    return _wait28(self, *a, **k)


Base.play, Base.wait = _play_j, _wait_j


def leg_mix(partes, x, y, cor=GEO, al="center", size=28, up=False, bold=False, gap=8):
    """Legenda com pedaços em MathTex (símbolos que a Space Grotesk não tem: ⇔, ⇒, ∂): `partes` = textos; os que começam com '$' são TeX
    (na cor da legenda). Linha de base dos textos em y px; alinhamento em x."""
    ms = []
    for p in partes:
        if isinstance(p, Mobject):
            p._mob = True
            ms.append(p)
            continue
        if p.startswith("$"):
            m = MathTex(p.strip("$"), font_size=fs(size * 0.95), tex_template=TEX27).set_color(cor)
            m._tex, m._caneta, m._esc, m._em_caneta = p, False, True, False
            for g in m.get_family():
                g._sem_contorno = True
            ms.append(m)
        else:
            ms.append(T(p, 960, y, size, "left", cor, bold=bold, up=up))
    g = VGroup(*ms).arrange(RIGHT, buff=gap / 120)
    base = PX(0, y)[1]
    for m in ms:
        if isinstance(m, MathTex) or getattr(m, "_mob", False):
            m.set_y(base + size * 0.36 / 120)
        else:
            m.shift(UP * (base - base_de(m)))
    dx = PX(x, 0)[0]
    g.shift(RIGHT * (dx - (g.get_center()[0] if al == "center" else g.get_left()[0])))
    return g.set_z_index(30)


# ═════════════ yt_0028 v2 (handoff v2 §3.2): ALERTA, mancha, ponto furado, faixas, R6 (seta dentro do painel), contadores ═════════════
ALERTA = "#FF5D5D"
MANCHA_C = mix(CAMPO2, FUNDO_C, 0.8).to_hex()
ALERTA_C = mix(ALERTA, FUNDO_C, 0.55).to_hex()
FAIXA, FAIXA2 = mix(GEO, FUNDO_C, 0.9).to_hex(), mix(GEO, FUNDO_C, 0.78).to_hex()
DELTA_C = mix(POS, FUNDO_C, 0.86).to_hex()
PAINEL_E, PAINEL_D = (130, 260, 830, 820), (1090, 260, 1790, 820)       # caixas dos painéis do layout B (px a 1080p)


def anel7(p, cor=POS, r=9, w=3, z=9):
    """Ponto furado: anel de 3 px e raio 9 px, miolo da cor do fundo."""
    c = Circle(radius=r / 120).move_to(np.asarray(p, float)).set_fill(FUNDO_C, 1).set_stroke(cor, w / 1.2, 1)
    c._sem_contorno = True
    return c.set_z_index(z)


def borda_mancha(d, n=360, Fv=None):
    th = np.linspace(0, 2 * PI, n, endpoint=False)
    a = (Fv or F_AULA)(d * np.cos(th), d * np.sin(th))
    return np.stack([np.asarray(a[0], float), np.asarray(a[1], float)], 1)


def _raio_raio(poly, c, u):
    """Maior t com c + t·u na borda do polígono (raio a partir de c)."""
    best = 0.0
    P = poly - c
    Q = np.roll(P, -1, axis=0)
    for a, b in zip(P, Q):
        e = b - a
        den = u[0] * e[1] - u[1] * e[0]
        if abs(den) < 1e-12:
            continue
        t = (a[0] * e[1] - a[1] * e[0]) / den
        s = (a[0] * u[1] - a[1] * u[0]) / den
        if t > 0 and -1e-9 <= s <= 1 + 1e-9:
            best = max(best, t)
    return best


class Mancha(VGroup):
    """Mancha = imagem do disco δ pela função original (polígono de 360 pontos), preenchida (menta 80 % no fundo, opaca), contorno menta 2 px.
    Com `vaza=True`, a parte fora do disco ε (centro c, raio ε) fica ALERTA: a mancha inteira em ALERTA por baixo e, por cima, a interseção
    mancha ∩ disco ε (a mancha é estrelada em relação a F(P), então a interseção é min(ε, raio da mancha) em cada direção)."""

    def __init__(self, v, d_fn, eps_fn=None, c=(1.0, 0.0), z=4):
        super().__init__()
        self.v, self.d_fn, self.eps_fn, self.c = v, d_fn, eps_fn, np.array(c, float)
        self.fora = VMobject().set_fill(ALERTA_C, 1).set_stroke(width=0)
        self.dentro = VMobject().set_fill(MANCHA_C, 1).set_stroke(width=0)
        self.borda = VMobject().set_fill(opacity=0).set_stroke(CAMPO2, 2 / 1.2, 1)
        for m in (self.fora, self.dentro, self.borda):
            m._sem_contorno = True
        self.add(self.fora, self.dentro, self.borda)
        self.set_z_index(z)
        self.dentro.set_z_index(z + .1)
        self.borda.set_z_index(z + .2)
        self.vaza = 0.0
        self.atualiza()

    def atualiza(self):
        d = max(1e-4, self.d_fn())
        B = borda_mancha(d)
        P = [self.v.c2p(*p) for p in B]
        self.borda.set_points_as_corners(P + [P[0]])
        self.fora.set_points_as_corners(P + [P[0]])
        eps = self.eps_fn() if self.eps_fn else None
        if eps is None:
            self.dentro.set_points_as_corners(P + [P[0]])
            self.dist = None
            return self
        th = np.linspace(0, 2 * PI, 240, endpoint=False)
        pts = []
        for t in th:
            u = np.array([math.cos(t), math.sin(t)])
            r = min(eps, _raio_raio(B, self.c, u))
            pts.append(self.v.c2p(*(self.c + r * u)))
        self.dentro.set_points_as_corners(pts + [pts[0]])
        self.dist = float(np.max(np.linalg.norm(B - self.c, axis=1)))
        self.frac_fora = float(np.mean(np.linalg.norm(B - self.c, axis=1) > eps))
        return self

    def viva(self):
        self.add_updater(lambda m: m.atualiza())
        return self


def faixa(v, pts, cor=FAIXA, z=1):
    return preenche(v, pts, cor, 1.0, z)


def contador(rotulo, cor, x, y, size=36, casas=2):
    """Contador ao vivo (B1-2): rótulo MathTex fixo + DecimalNumber com vírgula (o número muda, o rótulo não). Devolve (grupo, ValueTracker)."""
    vt = ValueTracker(0.0)
    lab = TC(rotulo + r"\ =", x, y, size, "l", caneta=False)
    num = NumBR(0.0, num_decimal_places=casas, font_size=fs(size)).set_color(cor)
    num.next_to(lab, RIGHT, buff=0.12)
    num.add_updater(lambda m: m.set_value(vt.get_value()))
    for g in num.get_family():
        g._sem_contorno = True
    g = VGroup(lab, num)
    g.shift(RIGHT * (PX(x, 0)[0] - g.get_center()[0]))
    return g.set_z_index(25), vt


# ── R6 (handoff v2 §3.2-5): nenhuma seta, curva ou mancha passa da moldura do seu painel, quadro a quadro ──
def guarda(cena, m, caixa, nome=""):
    cena._r6 = getattr(cena, "_r6", [])
    cena._r6.append((m, caixa, nome or type(m).__name__))
    return m


def _r6_chk(self):
    lst = getattr(self, "_r6", None)
    if not lst:
        return
    fam = set()
    for mob in self.mobjects:
        fam |= {id(x) for x in mob.get_family()}
    self._r6_q = getattr(self, "_r6_q", 0) + 1
    for m, (x0, y0, x1, y1), nome in lst:
        if id(m) not in fam:
            continue
        pts = [p for x in m.family_members_with_points() if (x.get_stroke_opacity() > 0.05 and x.get_stroke_width() > 0) or x.get_fill_opacity() > 0.05 for p in x.points]
        if not pts:
            continue
        P = np.asarray(pts)
        px, py = P[:, 0] * 120 + 960, 540 - P[:, 1] * 120
        fora = max(x0 - px.min(), px.max() - x1, y0 - py.min(), py.max() - y1)
        if fora > 1.0:
            self._r6_n = getattr(self, "_r6_n", 0) + 1
            if getattr(self, "_r6_n", 0) <= 40:
                print(f"[r6] {self._aid} {self.t:7.2f}s {nome}: passa {fora:.1f} px da moldura")


_upd28 = Base.update_to_time


def _update_r6(self, t):
    _upd28(self, t)
    if getattr(self, "_em_play", False):
        _r6_chk(self)


Base.update_to_time = _update_r6
_fim28 = Base.fim


def _fim_r6(self):
    _fim28(self)
    if hasattr(self, "_r6"):
        print(f"[r6-total] {self.lote} {getattr(self, '_r6_n', 0)} quadros fora em {getattr(self, '_r6_q', 0)} quadros checados; {len(self._r6)} objetos guardados")


Base.fim = _fim_r6


def escala_ida_volta(m, s=1.08, rt=0.8):
    """Destaque por escala (sem cor nova, sem brilho): 1 → s → 1."""
    return Transform(m, m.copy().scale(s), rate_func=there_and_back, run_time=rt)


def num_circ(n, cor, size=30):
    """① ② ③ desenhados (a Space Grotesk não tem os números circulados): anel na cor do texto + o algarismo."""
    t = T(str(n), 960, 540, size * 0.72, "center", cor, bold=True)
    r = size * 0.56 / 120
    c = Circle(radius=r).set_stroke(cor, 2 / 1.2, 1).set_fill(opacity=0).move_to(t.get_center())
    c._sem_contorno = True
    return VGroup(c, t)


# ═════════════ yt_0028 v3 (handoff v3 §2): chapas opacas nas linhas grossas, zonas de texto, R7 (seta inteira na chapa), R8 (chapa vazia) ═════════════
# Grade do fundo (medida no fundo.png): linhas grossas em x = 120k e y = 60 + 120k px (1080p). No Manim desta unidade 1 u = 120 px
# (quadro 16 × 9), então uma casa grossa = 1 u e a origem do Manim é um cruzamento grosso.
CHAPA_F = "#060D1E"
ATIVAS = []                 # caixas (px) das chapas do layout atual, usadas pelo filtro R7 na construção das redes de setas
ALINHA = []                 # registro de alinhamento (R9): (tipo, nome, x0, y0, x1, y1)
LAY_A = (120, 180, 1080, 900)
LAY_BE, LAY_BD = (120, 180, 840, 900), (1080, 180, 1800, 900)
LAY_C = [(120, 300, 600, 780), (720, 300, 1200, 780), (1320, 300, 1800, 780)]
PAINEL_E, PAINEL_D = LAY_BE, LAY_BD


def _grade_ok(x, y):
    return abs(x % 120) < 1e-6 and abs((y - 60) % 120) < 1e-6


def chapa_px(x0, y0, x1, y1, nome="chapa", borda=True, z=-30):
    """Chapa (v3 §2.2): RoundedRectangle opaco #060D1E, raio 8 px, moldura GEO 30 % de ~2 px; os 4 cantos nas linhas grossas (assert)."""
    for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
        assert _grade_ok(x, y), f"chapa fora da grade: ({x}, {y})"
    r = RoundedRectangle(width=(x1 - x0) / 120, height=(y1 - y0) / 120, corner_radius=8 / 120)
    r.move_to(PX((x0 + x1) / 2, (y0 + y1) / 2)).set_fill(CHAPA_F, 1).set_stroke(GEO, 2 / 1.2 if borda else 0, 0.30 if borda else 0)
    r._sem_contorno, r._box, r._chapa = True, (x0, y0, x1, y1), True
    ALINHA.append(("chapa", nome, x0, y0, x1, y1))
    if (x0, y0, x1, y1) not in ATIVAS:
        ATIVAS.append((x0, y0, x1, y1))
    return r.set_z_index(z)


def zona_px(x0, y0, x1, y1, nome="zona"):
    """Zona de texto (v3 §2.3): retângulo da cor do fundo, sem moldura, 1 px para dentro das linhas grossas."""
    for x, y in ((x0, y0), (x1, y1)):
        assert _grade_ok(x, y), f"zona fora da grade: ({x}, {y})"
    r = Rectangle(width=(x1 - x0 - 2) / 120, height=(y1 - y0 - 2) / 120).move_to(PX((x0 + x1) / 2, (y0 + y1) / 2))
    r.set_fill(FUNDO_C, 1).set_stroke(width=0)
    r._sem_contorno, r._zona = True, True
    ALINHA.append(("zona", nome, x0, y0, x1, y1))
    return r.set_z_index(-35)


def zera_chapas():
    ATIVAS.clear()


def origem_papel(v, nome):
    """Registra a origem de um papel (gráfico sem chapa) para o QA de alinhamento: tem de cair num cruzamento grosso."""
    x, y = canto_xy(v, 0, 0)
    assert _grade_ok(round(x, 6), round(y, 6)), f"origem de papel fora da grade: {nome} ({x}, {y})"
    ALINHA.append(("origem", nome, x, y, x, y))


def painel(x0, y0, w, h):
    """v3: os painéis da v2 viram chapas encaixadas (sb28v3 `painel`): B 700×560 → 720×720 (x 120/1080, y 180–900); C 480×460 → 480×480 (y 300–780)."""
    if w == 700 and h == 560:
        b = LAY_BE if x0 < 600 else LAY_BD
    elif w == 480:
        b = LAY_C[0] if x0 < 400 else (LAY_C[1] if x0 < 1000 else LAY_C[2])
    else:
        raise ValueError((x0, y0, w, h))
    return chapa_px(*b, nome=f"painel {b}")


def _cabe_px(pa, pb, m=18):
    """R7 na construção: a seta só entra se as duas pontas couberem na chapa (folga de 18 px). Sem chapa por perto, entra."""
    A = (pa[0] * 120 + 960, 540 - pa[1] * 120)
    B = (pb[0] * 120 + 960, 540 - pb[1] * 120)
    c = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    pl = next((p for p in ATIVAS if p[0] - 40 < c[0] < p[2] + 40 and p[1] - 40 < c[1] < p[3] + 40), None)
    if pl is None:
        return True
    return all(pl[0] + m < q[0] < pl[2] - m and pl[1] + m < q[1] < pl[3] - m for q in (A, B))


_seta_campo0, _seta_prop0 = seta_campo, seta_prop


def seta_campo(v, X, Y, f, lmax, mmax, ctx=False, cor=None, w=5, head=19):
    s = _seta_campo0(v, X, Y, f, lmax, mmax, ctx, cor, w, head)
    if s is not None and not _cabe_px(s.get_start(), s.get_end()):
        return None
    return s


def seta_prop(v, X, Y, f, lmax, ctx=False, cor=None, w=5, head=19):
    s = _seta_prop0(v, X, Y, f, lmax, ctx, cor, w, head)
    if s is not None and not _cabe_px(s.get_start(), s.get_end()):
        return None
    return s


# ── checagem por quadro: R7 (seta, curva, mancha a ≥ 18 px da moldura da sua chapa) e R8 (chapa vazia > 0,5 s) ──
def _caixa_px(m):
    pts = [p for x in m.family_members_with_points() if isinstance(x, VMobject) and ((x.get_stroke_opacity() > 0.05 and x.get_stroke_width() > 0) or x.get_fill_opacity() > 0.05) for p in x.points]
    if not pts:
        return None
    P = np.asarray(pts)
    return P[:, 0].min() * 120 + 960, 540 - P[:, 1].max() * 120, P[:, 0].max() * 120 + 960, 540 - P[:, 1].min() * 120


def _r7_chk(self):
    chapas = [m for m in self.mobjects if getattr(m, "_chapa", False) and m.get_fill_opacity() > 0.5]
    self._r7_q = getattr(self, "_r7_q", 0) + 1
    boxes = [m._box for m in chapas]
    if boxes:
        alvos = list(getattr(self, "_r6", []))
        vistos = set()
        for mob in self.mobjects:
            for x in mob.get_family():
                if hasattr(x, "_xy") and hasattr(x, "haste") and id(x) not in vistos:
                    vistos.add(id(x))
                    if x.haste.get_stroke_opacity() > 0.95 and not getattr(x, "_escondida", False):          # durante um fade (troca de layout) não conta
                        alvos.append((x, None, "seta de campo"))
        fam = set()
        for mob in self.mobjects:
            fam |= {id(x) for x in mob.get_family()}
        for m, _, nome in alvos:
            if id(m) not in fam:
                continue
            if max([y.get_stroke_opacity() for y in m.family_members_with_points() if isinstance(y, VMobject)] + [0]) < 0.95 and                     max([y.get_fill_opacity() for y in m.family_members_with_points() if isinstance(y, VMobject)] + [0]) < 0.95:
                continue
            c = _caixa_px(m)
            if c is None:
                continue
            cx, cy = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2
            b = next((b for b in boxes if b[0] < cx < b[2] and b[1] < cy < b[3]), None)
            if b is None:
                continue
            folga = min(c[0] - b[0], b[2] - c[2], c[1] - b[1], b[3] - c[3])
            if folga < 18 - 0.5:
                self._r7_n = getattr(self, "_r7_n", 0) + 1
                if self._r7_n <= 60:
                    print(f"[r7] {self._aid} {self.t:7.2f}s {nome}: {folga:.1f} px da moldura da chapa {b}")
    # R8
    vazias = getattr(self, "_r8_c", {})
    outros = [x for mob in self.mobjects if not getattr(mob, "_chapa", False) and not getattr(mob, "_zona", False) and mob not in self.fixos()
              for x in mob.family_members_with_points() if isinstance(x, VMobject) and ((x.get_stroke_opacity() > 0.05 and x.get_stroke_width() > 0) or x.get_fill_opacity() > 0.05)]
    centros = [((x.get_center()[0]) * 120 + 960, 540 - x.get_center()[1] * 120) for x in outros]
    for m in chapas:
        b = m._box
        vazia = not any(b[0] < cx < b[2] and b[1] < cy < b[3] for cx, cy in centros)
        n = vazias.get(id(m), 0) + 1 if vazia else 0
        vazias[id(m)] = n
        if n == round(0.5 * FPS) + 1:
            self._r8_n = getattr(self, "_r8_n", 0) + 1
            print(f"[r8] {self._aid} {self.t:7.2f}s chapa {b} vazia há mais de 0,5 s")
    self._r8_c = vazias


_update_v2 = Base.update_to_time


def _update_v3(self, t):
    _upd28(self, t)                       # o update original (flash) — a checagem R6 da v2 fica substituída pela R7
    if getattr(self, "_em_play", False):
        _r7_chk(self)


Base.update_to_time = _update_v3
_fim_v2 = Base.fim


def _fim_v3(self):
    _fim_v2(self)
    print(f"[r7-total] {self.lote} {getattr(self, '_r7_n', 0)} ocorrências em {getattr(self, '_r7_q', 0)} quadros checados")
    print(f"[r8-total] {self.lote} {getattr(self, '_r8_n', 0)} chapas vazias por mais de 0,5 s")
    for a in ALINHA:
        print(f"[alinha] {a[0]} {a[1]} {a[2]:.2f} {a[3]:.2f} {a[4]:.2f} {a[5]:.2f}")


Base.fim = _fim_v3


def placa_tc(s, x, y, size, al="c"):
    """Fórmula com a placa mínima R2 atrás (topo dos layouts B, v3 §2.3)."""
    g = TP(s, x, y, size, al, caneta=True)
    return g
