"""yt_0032 · peças do vídeo (copiado do v31.py do yt_0031, sem importar; portadas de referencia/sb32.html e c3d32.html). Texto/fórmula/placa/painel
vêm do yt_0028 via yt_0031; o resto é desta unidade. Tudo em px de 1080p: PX(x, y) (1 u do Manim = 120 px). Chapa R = [0, 2]² com 1 m = 240 px e canto (0, 0) em (360, 780).
Estilo do sb31: sem contorno escuro, sem brilho; placa mínima #131030 a 88 %; cor por grandeza; operadores brancos."""
import re
import time

from kit import *  # noqa: F401,F403
from kit import _Caneta
from assets.calculo.papel import papel  # noqa: E402

# ── paleta (handoff §3.3; sb31.html) ──────────────────────────────────────────────────────────────────────
CI, AZC, CORAL, POS, E1, E2 = "#35D9FF", "#7FB2FF", "#FF7A8A", "#E08A3C", "#FFC24D", "#EA63FF"
GEO, BR, AL, MEN, BG_ = "#B8C4DA", "#F5F7FF", "#FF5D5D", "#8CFFD2", "#131030"
LEVE, PESADO, RAMP0 = "#1E5072", "#30BBE0", "#10243A"
BASE3D = "#1C1846"


def hx(c):
    c = ManimColor(c).to_hex()
    return np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)


def mixh(a, b, t):
    v = hx(a) + (hx(b) - hx(a)) * min(1.0, max(0.0, t))
    return "#%02X%02X%02X" % tuple(int(round(x)) for x in v)


def PX(x, y):
    return P3((x - 960) / 120, 4.5 - y / 120)


def pxof(p):
    return (p[0] * 120 + 960, 540 - p[1] * 120)


def fs(px):
    """font_size do MathTex equivalente ao KaTeX de `px` px (medido no yt_0026)."""
    return px * 0.803


def ts(px):
    return px * 0.6


def W(px):
    """largura de traço em px de 1080p → stroke_width do Manim."""
    return px / 1.2


def sem_ctn(m):
    for x in m.get_family():
        x._sem_contorno = True
    return m


# ── texto ──────────────────────────────────────────────────────────────────────────────────────────────────
# o Space Grotesk não tem ε δ ∪ ⇒ ᵢ ‖ ρ α: esses pedaços saem do LaTeX na mesma cor, alinhados pela linha de base
ESPECIAIS = [("ε₁", r"\varepsilon_1"), ("ε₂", r"\varepsilon_2"), ("Aᵢ", r"A_i"), ("‖ ‖", r"\|\;\|"), ("ε", r"\varepsilon"), ("δ", r"\delta"),
             ("∪", r"\cup"), ("∩", r"\cap"), ("⇒", r"\Rightarrow"), ("α", r"\alpha"), ("ρ", r"\rho"), ("∅", r"\varnothing")]
_RX = re.compile("(" + "|".join(re.escape(a) for a, _ in ESPECIAIS) + ")")


def T(s, x, y, size=30, al="left", cor=BR, bold=True, caneta=True):
    """Texto (fillText do storyboard): y = linha de base em px; al = left | center | right. Sem caixa alta automática (a string já vem do sb31)."""
    partes = [p for p in _RX.split(s) if p != ""]
    ms, gaps = [], []
    sp = size * 0.26 / 120
    for i, p in enumerate(partes):
        if p in dict(ESPECIAIS):
            m = MathTex(dict(ESPECIAIS)[p], font_size=fs(size) * 1.04).set_fill(cor, 1).set_stroke(cor, 0)
            m._esp = p
        else:
            m = txt(p.strip(), ts(size), color=cor, bold=bold, up=False)
        lead = p[:1] == " "
        trail = p[-1:] == " "
        gaps.append((lead, trail))
        ms.append(m)
    g = VGroup()
    xcur = 0.0
    ref = None
    for i, m in enumerate(ms):
        if i > 0:
            pad = sp if (gaps[i - 1][1] or gaps[i][0]) else size * 0.05 / 120
            xcur += pad
        m.shift(RIGHT * (xcur - m.get_left()[0]))
        xcur = m.get_right()[0]
        g.add(m)
    # linha de base
    for m in ms:
        if getattr(m, "_esp", None):
            continue
        ref = m
        break
    yb = PX(0, y)[1]
    for m in ms:
        if getattr(m, "_esp", None):
            e = m._esp
            if e in ("⇒",):
                m.shift(UP * (yb + size * 0.30 / 120 - m.get_center()[1]))
            elif e in ("‖ ‖",):
                m.shift(UP * (yb - size * 0.12 / 120 - m.get_bottom()[1]))
            elif e in ("ρ", "Aᵢ", "ε₁", "ε₂"):
                m.shift(UP * (yb - m[0][0].get_bottom()[1] + (size * 0.0 / 120 if e != "ρ" else -size * 0.0 / 120)))
                if e == "ρ":
                    m.shift(UP * (yb - (m.get_bottom()[1] + 0.22 * m.height)))
            else:
                m.shift(UP * (yb - m.get_bottom()[1]))
        else:
            m.shift(UP * (yb - base_de(m)))
    dx = PX(x, 0)[0]
    if al == "left":
        g.shift(RIGHT * (dx - g.get_left()[0]))
    elif al == "center":
        g.shift(RIGHT * (dx - g.get_center()[0]))
    else:
        g.shift(RIGHT * (dx - g.get_right()[0]))
    sem_ctn(g)
    g._tex, g._caneta, g._esc, g._em_caneta, g._txt = s, caneta, not caneta, False, s
    return g.set_z_index(30)


def leg(s, x, y, cor=GEO, al="left", size=28, caneta=True):
    """`leg` do sb31: Space Grotesk Medium."""
    return T(s, x, y, size, al, cor, bold=False, caneta=caneta)


TEX31 = TexTemplate()
TEX31.add_to_preamble(
    r"\usepackage{xcolor}"
    r"\definecolor{ci}{HTML}{35D9FF}\definecolor{az}{HTML}{7FB2FF}\definecolor{co}{HTML}{FF7A8A}\definecolor{me}{HTML}{8CFFD2}"
    r"\definecolor{lr}{HTML}{E08A3C}\definecolor{al}{HTML}{FF5D5D}\definecolor{ca}{HTML}{FFC24D}\definecolor{cm}{HTML}{EA63FF}\definecolor{cg}{HTML}{B8C4DA}"
    r"\def\X{\textcolor{ca}{x}}\def\Y{\textcolor{cm}{y}}\def\f{\textcolor{ci}{f}}\def\rr{\textcolor{ci}{\rho}}"
    r"\def\Xij{\textcolor{lr}{X_{ij}}}\def\dxi{\textcolor{ca}{\Delta x_i}}\def\dyj{\textcolor{cm}{\Delta y_j}}"
    r"\def\Ci#1{\textcolor{ci}{#1}}\def\Az#1{\textcolor{az}{#1}}\def\Co#1{\textcolor{co}{#1}}\def\Me#1{\textcolor{me}{#1}}"
    r"\def\Lr#1{\textcolor{lr}{#1}}\def\Al#1{\textcolor{al}{#1}}"
    r"\def\eps{\textcolor{me}{\varepsilon}}\def\del{\textcolor{lr}{\delta}}\def\Rij{R_{ij}}"
    r"\def\mij{\textcolor{az}{m_{ij}}}\def\Mij{\textcolor{co}{M_{ij}}}\def\sP{\textcolor{az}{s(P)}}\def\SP{\textcolor{co}{S(P)}}"
    r"\def\XX{\textcolor{lr}{X}}\def\YY{\textcolor{lr}{Y}}\def\sen{\operatorname{sen}}"
    r"\definecolor{li}{HTML}{C9A7FF}\def\g{\textcolor{li}{g}}\def\Li#1{\textcolor{li}{#1}}\def\Am#1{\textcolor{ca}{#1}}\def\Mg#1{\textcolor{cm}{#1}}"
    r"\def\Ge#1{\textcolor{cg}{#1}}\def\al{\textcolor{cg}{\alpha}}\def\dX{\textcolor{ca}{dx}}\def\dY{\textcolor{cm}{dy}}")


def TC(s, x=960, y=540, size=48, al="l", caneta=True):
    """Fórmula do storyboard (mesma string do KaTeX, com os macros do preâmbulo): centro vertical em y px, alinhamento em x px (l | c | r)."""
    m = MathTex(r"\textstyle " + s.replace(r"\sum", r"\sum\nolimits"), font_size=fs(size), tex_template=TEX31)     # yt_0032: estilo de texto (∬ e Σ com índices ao lado), como o KaTeX inline do alvo
    m._tex, m._caneta, m._esc, m._em_caneta, m._txt = s, caneta, not caneta, False, s
    sem_ctn(m)
    p = PX(x, y)
    m.move_to(p)
    if al == "l":
        m.shift(RIGHT * (p[0] - m.get_left()[0]))
    elif al == "r":
        m.shift(RIGHT * (p[0] - m.get_right()[0]))
    return m.set_z_index(25)


def placa_min(m, padx=6, pady=4, op=0.88):
    """Placa mínima (#131030 a 88 %, cantos 6 px) atrás de um rótulo."""
    r = RoundedRectangle(width=m.width + 2 * padx / 120, height=m.height + 2 * pady / 120, corner_radius=6 / 120).move_to(m.get_center())
    r.set_fill(BG_, op).set_stroke(width=0)
    r._sem_contorno = True
    return r.set_z_index((m.z_index or 25) - 1)


def TP(s, x, y, size=30, al="c", caneta=True):
    """Rótulo matemático com placa. VGroup(placa, MathTex); .f = MathTex. A placa entra junto do primeiro glifo (caneta) e sai com o rótulo."""
    f = TC(s, x, y, size, al, caneta=caneta)
    g = VGroup(placa_min(f), f)
    g.f = f
    g._txt = s
    return g


def TPt(s, x, y, size=26, cor=BR, al="center", bold=True, caneta=True):
    t = T(s, x, y, size, al, cor, bold, caneta=caneta)
    g = VGroup(placa_min(t, 8, 4), t)
    g.f = t
    g._txt = s
    return g


def nglifos(tex, size=40):
    return len(MathTex(tex, font_size=fs(size), tex_template=TEX31)[0])


def faixa_idx(prefixo, peca):
    a = nglifos(prefixo) if prefixo else 0
    return list(range(a, a + nglifos(peca)))


# ── desenho em px ──────────────────────────────────────────────────────────────────────────────────────────
def painel(x0, y0, w, h, alpha=0.35, cor=GEO, raio=14):
    r = RoundedRectangle(width=w / 120, height=h / 120, corner_radius=raio / 120).move_to(PX(x0 + w / 2, y0 + h / 2))
    r.set_fill(opacity=0).set_stroke(cor, W(2), alpha)
    r._sem_contorno = True
    r._painel = (x0, y0, x0 + w, y0 + h)
    return r.set_z_index(-5)


def caixa_px(x0, y0, w, h, cor=GEO, wpx=2, alpha=1.0, raio=12, fill=None, fop=0.0):
    r = RoundedRectangle(width=w / 120, height=h / 120, corner_radius=raio / 120).move_to(PX(x0 + w / 2, y0 + h / 2))
    r.set_fill(fill or BG_, fop).set_stroke(cor, W(wpx), alpha)
    return sem_ctn(r).set_z_index(2)


def ret_px(x0, y0, x1, y1, fill=None, fop=1.0, stroke=None, wpx=2, sop=1.0, z=2):
    r = Polygon(PX(x0, y0), PX(x1, y0), PX(x1, y1), PX(x0, y1))
    r.set_fill(fill or BG_, fop if fill else 0).set_stroke(stroke or BG_, W(wpx) if stroke else 0, sop if stroke else 0)
    return sem_ctn(r).set_z_index(z)


def lin_px(pts, cor, wpx=3, alpha=1.0, dash=None, z=4):
    m = VMobject().set_points_as_corners([PX(*p) for p in pts]).set_stroke(cor, W(wpx), alpha).set_fill(opacity=0)
    m.cap_style = CapStyleType.ROUND
    if dash:
        n = max(4, int(m.get_arc_length() * 120 / (dash[0] + dash[1])))
        m = DashedVMobject(m, num_dashes=n, dashed_ratio=dash[0] / (dash[0] + dash[1]))
        m.set_stroke(cor, W(wpx), alpha)
    return sem_ctn(m).set_z_index(z)


def seta_px(a, b, cor, wpx=5, head=20, z=4):
    """Seta do sb31: haste + ponta cheia (largura = ½ comprimento da ponta), a e b em px."""
    A, B = np.array(a, float), np.array(b, float)
    d = B - A
    L = float(np.hypot(*d))
    u = d / L
    h = min(head, 0.45 * L)
    hw = h * 0.5
    bx = B - u * h
    haste = Line(PX(*A), PX(*(bx + u))).set_stroke(cor, W(wpx))
    haste.cap_style = CapStyleType.ROUND
    n = np.array([-u[1], u[0]])
    ponta = Polygon(PX(*B), PX(*(bx + n * hw)), PX(*(bx - n * hw))).set_fill(cor, 1).set_stroke(cor, 0)
    return sem_ctn(VGroup(haste, ponta)).set_z_index(z)


def ponto_px(x, y, cor, r=9, z=8):
    d = Dot(PX(x, y), radius=r / 120, color=cor).set_stroke(width=0)
    d._obst = True
    return sem_ctn(d).set_z_index(z)


def check_px(X, Y, cor=MEN, s=1.0, z=12):
    m = VMobject().set_points_as_corners([PX(X - 14 * s, Y), PX(X - 3 * s, Y + 11 * s), PX(X + 16 * s, Y - 13 * s)]).set_stroke(cor, W(6 * s)).set_fill(opacity=0)
    m.cap_style = CapStyleType.ROUND
    m.joint_type = LineJointType.ROUND
    return sem_ctn(m).set_z_index(z)


def cruz_px(X, Y, cor=AL, s=1.0, z=12):
    a = Line(PX(X - 12 * s, Y - 12 * s), PX(X + 12 * s, Y + 12 * s))
    b = Line(PX(X + 12 * s, Y - 12 * s), PX(X - 12 * s, Y + 12 * s))
    g = VGroup(a, b).set_stroke(cor, W(6 * s))
    for m in g:
        m.cap_style = CapStyleType.ROUND
    return sem_ctn(g).set_z_index(z)


def circ_px(X, Y, r, cor, wpx=3, dash=None, fill=None, fop=0.0, z=6):
    c = Circle(radius=r / 120).move_to(PX(X, Y)).set_stroke(cor, W(wpx)).set_fill(fill or BG_, fop)
    if dash:
        n = max(6, int(2 * PI * r / (dash[0] + dash[1])))
        c = DashedVMobject(c, num_dashes=n, dashed_ratio=dash[0] / (dash[0] + dash[1])).set_stroke(cor, W(wpx))
    return sem_ctn(c).set_z_index(z)


def sublinha_px(x0, x1, y, cor=BR, wpx=2):
    return sem_ctn(Line(PX(x0, y), PX(x1, y)).set_stroke(cor, W(wpx))).set_z_index(31)


def img_px(arr, x0, y0, w=None, h=None, z=0, nearest=False):
    """ImageMobject de um array RGB(A) uint8; canto superior esquerdo em (x0, y0) px; tamanho em px de 1080p (padrão: o do array)."""
    a = np.asarray(arr)
    if a.dtype != np.uint8:
        a = np.clip(a, 0, 255).astype(np.uint8)
    if a.shape[2] == 3:
        a = np.concatenate([a, np.full(a.shape[:2] + (1,), 255, np.uint8)], 2)
    h_, w_ = a.shape[:2]
    w = w or w_
    h = h or h_
    im = ImageMobject(a).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest" if nearest else "linear"])
    im.stretch_to_fit_width(w / 120).stretch_to_fit_height(h / 120)
    im.move_to(PX(x0 + w / 2, y0 + h / 2))
    return im.set_z_index(z)


# ── chapa e vistas ─────────────────────────────────────────────────────────────────────────────────────────
class Vw:
    """vista(cx, cy, u) do sb31: (a, b) → px = (cx + a·u, cy − b·u)."""

    def __init__(self, cx, cy, u, uy=None):
        self.cx, self.cy, self.u, self.uy = cx, cy, u, uy or u

    def px(self, a, b):
        return (self.cx + a * self.u, self.cy - b * self.uy)

    def P(self, a, b):
        return PX(*self.px(a, b))

    def c2p(self, a, b):          # interface dos eixos (papel)
        return self.P(a, b)


CH = Vw(360, 780, 240)


def g_solda(a):
    return 1 + 0.42 * np.sin(1.7 * np.asarray(a) - 0.4)


def faixa(a, b, am=400):
    v = g_solda(np.linspace(a, b, am + 1))
    return float(v.min()), float(v.max())


def celula_metal(a, b, c, d):
    mn, mx = faixa(a, b)
    leve, pes = c <= mx, d > mn
    return (1 if leve else 3), (3 if pes else 1), (leve and pes)


def celulas_verm(n):
    h = 2 / n
    out = []
    for i in range(n):
        mn, mx = faixa(i * h, i * h + h)
        for j in range(n):
            c, d = j * h, j * h + h
            if c <= mx and d > mn:
                out.append((i, j))
    return out


def f_dens(x, y):
    return x * x + y * y


def cor_dens_arr(v):
    t = np.power(np.clip(v / 8, 0, 1), 0.85)[..., None]
    return hx(RAMP0) * (1 - t) + hx(CI) * t


def arr_celulas(n, cor_fn, L=480):
    """Imagem L×L px da chapa [0,2]² com n×n células de cor cor_fn(i, j) (RGB 0–255). Linha 0 do array = topo (y = 2)."""
    a = np.zeros((L, L, 3))
    e = np.linspace(0, L, n + 1).round().astype(int)
    for i in range(n):
        for j in range(n):
            a[L - e[j + 1]:L - e[j], e[i]:e[i + 1]] = cor_fn(i, j)
    return a


def arr_dens(n=64, L=480):
    h = 2 / n
    return arr_celulas(n, lambda i, j: cor_dens_arr(np.array(f_dens((i + .5) * h, (j + .5) * h))), L)


def arr_metais(n, verm=True, alphaV=0.6, L=480):
    h = 2 / n
    vs = set(celulas_verm(n)) if verm else set()
    cv = hx(mixh(BG_, AL, alphaV))

    def c(i, j):
        if (i, j) in vs:
            return cv
        a, b, cc, d = i * h, i * h + h, j * h, j * h + h
        return hx(PESADO) if (cc + d) / 2 > g_solda((a + b) / 2) else hx(LEVE)
    return arr_celulas(n, c, L)


def arr_metais_liso(L=480, dy_leve=0.0, dy_pes=0.0, transp=False):
    ys = (L - 0.5 - np.arange(L)) / L * 2
    xs = (np.arange(L) + 0.5) / L * 2
    X, Y = np.meshgrid(xs, ys)
    gg = g_solda(X)
    a = np.where((Y > gg)[..., None], hx(PESADO), hx(LEVE))
    return a


def img_chapa(arr, v=CH, z=0):
    x0, y0 = v.px(0, 2)
    x1, y1 = v.px(2, 0)
    return img_px(arr, x0, y0, x1 - x0, y1 - y0, z=z)


def grade_ch(n, v=CH, cor=None, wpx=1, dash=None, z=3, x0=0, x1=2, y0=0, y1=2):
    cor = cor or mixh(BG_, GEO, 0.35)
    ls = VGroup()
    for k in range(1, n):
        a = 2 * k / n
        ls.add(lin_px([v.px(a, y0), v.px(a, y1)], cor, wpx, dash=dash, z=z))
        ls.add(lin_px([v.px(x0, a), v.px(x1, a)], cor, wpx, dash=dash, z=z))
    return ls


def borda_ch(v=CH, cor=GEO, wpx=3, z=5):
    return lin_px([v.px(0, 0), v.px(2, 0), v.px(2, 2), v.px(0, 2), v.px(0, 0)], cor, wpx, z=z)


def solda_px(v=CH, cor=BR, wpx=4, a0=0.0, a1=2.0, z=7, n=120, dy=0.0):
    pts = [v.px(a, float(g_solda(a)) + dy) for a in np.linspace(a0, a1, n + 1)]
    return lin_px(pts, cor, wpx, z=z)


def eixos_chapa(v=CH, z=6):
    """setas âmbar/magenta dos eixos x e y da chapa + rótulos x, y (fórmula)."""
    sx = seta_px(v.px(-0.1, 0), v.px(2.3, 0), E1, 3, 16, z=z)
    sy = seta_px(v.px(0, -0.1), v.px(0, 2.3), E2, 3, 16, z=z)
    lx = TC(r"\X", *v.px(2.4, 0), 32, "c")
    ly = TC(r"\Y", *v.px(0, 2.42), 32, "c")
    return sx, sy, lx, ly


def arco_px(v, cor=CI, wpx=3, r=2, z=6, n=90):
    return lin_px([v.px(r * math.cos(PI / 2 * k / n), r * math.sin(PI / 2 * k / n)) for k in range(n + 1)], cor, wpx, z=z)


def poly_px(pts_px, fill, fop=1.0, z=1):
    p = Polygon(*[PX(*q) for q in pts_px]).set_fill(fill, fop).set_stroke(width=0)
    return sem_ctn(p).set_z_index(z)


def arr_escadaB(n, borda_on=True, L=480, cin=None, cbord=None):
    cin = hx(cin or mixh(BG_, CI, 0.55))
    cbord = hx(cbord or mixh(BG_, AL, 0.55))
    a = np.zeros((L, L, 4))
    e = np.linspace(0, L, n + 1).round().astype(int)
    h = 2 / n
    for i in range(n):
        for j in range(n):
            near, far = (i * h) ** 2 + (j * h) ** 2, ((i + 1) * h) ** 2 + ((j + 1) * h) ** 2
            cx, cy = (i + .5) * h, (j + .5) * h
            c = None
            if borda_on and near < 4 < far:
                c = cbord
            elif cx * cx + cy * cy <= 4:
                c = cin
            if c is not None:
                a[L - e[j + 1]:L - e[j], e[i]:e[i + 1], :3] = c
                a[L - e[j + 1]:L - e[j], e[i]:e[i + 1], 3] = 255
    return a


def mini_metais(X, Y, L, n=16):
    v = Vw(X, Y, L / 2)
    g = Group(img_chapa(arr_metais(n, alphaV=0.6), v), grade_ch(n, v, mixh(BG_, GEO, .35), 1), borda_ch(v, GEO, 2), solda_px(v, BR, 3))
    return g, v


def mini_disco(X, Y, L, n=32):
    v = Vw(X, Y, L / 2)
    g = Group(img_chapa(arr_escadaB(n), v), grade_ch(n, v, mixh(BG_, GEO, .3), 1), borda_ch(v, GEO, 2), arco_px(v, CI, 3))
    return g, v


def mini_dens(X, Y, L):
    v = Vw(X, Y, L / 2)
    return Group(img_chapa(arr_dens(48), v), borda_ch(v, GEO, 2)), v


# ── 3D: câmera do three.js reproduzida em Python (mesma conta do PerspectiveCamera + lookAt + setViewOffset) ──────────────
FOV3D = 22.0


def cam_dict(pos, tgt, up, cx, cy):
    return {"pos": [float(x) for x in pos], "tgt": [float(x) for x in tgt], "up": [float(x) for x in up], "cx": float(cx), "cy": float(cy)}


D_TOPO = 1080 / (2 * 240 * math.tan(math.radians(FOV3D / 2)))          # ≈ 11,57: 240 px/m na vista de cima
CAM_TOPO = cam_dict((1, 1, D_TOPO), (1, 1, 0), (0, 1, 0), 600, 540)      # canto (0, 0) em (360, 780) px, igual à chapa 2D
# câmeras do c3d32.html (ver(pos, alvo, cx, cy), up = +z)
CAM_RAMPA = cam_dict((4.6, -6.6, 5.2), (1, 1, 0.75), (0, 0, 1), 600, 600)      # b12, b21
CAM_PREDIO = cam_dict((3.6, -6.2, 8.6), (1, 1, 0.7), (0, 0, 1), 600, 600)      # b61
CAM_BAIXO = cam_dict((3.9, -7.2, 6.8), (1, 1, 0.35), (0, 0, 1), 600, 600)      # b14, b22, b31, b32
CAM_K = cam_dict((5.4, -8.6, 6.4), (1, 1, 1.05), (0, 0, 1), 600, 610)          # b14 (fase k): mais longe, para k = 2 caber (topo 2·8·ZS)


def cam_mix(c0, c1, s):
    """Interpolação suave entre duas câmeras (s de 0 a 1); up interpolado e normalizado."""
    u = suave(s)
    L = lambda a, b: [a[i] + (b[i] - a[i]) * u for i in range(3)]
    up = np.array(L(c0["up"], c1["up"]))
    up /= np.linalg.norm(up)
    return cam_dict(L(c0["pos"], c1["pos"]), L(c0["tgt"], c1["tgt"]), up, c0["cx"] + (c1["cx"] - c0["cx"]) * u, c0["cy"] + (c1["cy"] - c0["cy"]) * u)


def cam_pouso(c1, s, c0=CAM_TOPO):
    return cam_mix(c0, c1, s)


def proj3d(cam, p):
    """Ponto do mundo → px de 1920×1080 (a mesma conta do three.js)."""
    pos, tgt, up = np.array(cam["pos"]), np.array(cam["tgt"]), np.array(cam["up"])
    z = pos - tgt
    z /= np.linalg.norm(z)
    x = np.cross(up, z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    d = np.asarray(p, float) - pos
    xc, yc, zc = d @ x, d @ y, d @ z
    t = math.tan(math.radians(FOV3D / 2))
    nx = xc / (-zc) / (t * 16 / 9)
    ny = yc / (-zc) / t
    return (cam["cx"] + 960 * nx, cam["cy"] - 540 * ny)


LV = 8 / 3


def pontos3d(cena, e):
    """Os mesmos pontos nomeados do c32.js (mundo), para o estado e."""
    gg = lambda a: float(g_solda(a))
    P = {}
    if cena in ("b12", "b21"):
        ZS = .25
        P.update({"ex": (2.57, 0, 0), "ey": (0, 3.42, 0), "ez": (0, 0, 2.37)})
        for v in (2, 4, 6, 8):
            P["m%d" % v] = (-.13, -.02, v * ZS)
        if cena == "b12":
            P.update({"xq": (1.75, 0, ZS * 1.75 ** 2 * .5 * e.get("cresceA", 1)), "yq": (1.75, .25, ZS * (1.75 ** 2 + .0625) + .02),
                      "topo": (1.75, 1.75, ZS * 2 * 1.75 ** 2)})
        else:
            P.update({"f": (1.75, 0, ZS * 1.75 ** 2 * .6 * e.get("cresceF", 1)), "g": (1.75, .25, ZS * (1.75 ** 2 + .0625 + 1 + .875) + .03),
                      "folga": (1.5, 0, ZS * (1.5625 + .0625 + .6)), "folgaC": (1.25, .25, ZS * (1.5625 + .0625 + .8125))})
    elif cena == "b14":
        if e.get("modo", "k") == "k":
            ZS = .25
            P.update({"ex": (2.57, 0, 0), "ey": (0, e.get("ly", 3.3) + .12, 0), "ez": (0, 0, e.get("lz", 2.25) + .12)})
            for v in (2, 4, 6, 8):
                P["m%d" % v] = (-.13, -.02, v * ZS)
            P["topo"] = (1.75, 1.75, ZS * 2 * 1.75 ** 2 * e.get("k", 1))
        else:
            ZS = .4
            P.update({"ex": (2.57, 0, 0), "ey": (0, e.get("ly", 2.45) + .12, 0), "ez": (0, 0, e.get("lz", 1.55) + .12), "m1": (-.13, -.02, ZS), "m3": (-.13, -.02, 3 * ZS),
                      "camada": (1.9, .15, ZS * .5), "reforco": (.25, 1.85, ZS * 2.2)})
    elif cena == "b22":
        ZS = .5
        P.update({"ex": (2.57, 0, 0), "ey": (0, 2.57, 0), "ez": (0, 0, 2.07), "m1": (-.13, -.02, ZS), "m3": (-.13, -.02, 3 * ZS),
                  "l1": (2, 0, ZS * 1), "l3": (2, 0, ZS * 3)})
    elif cena == "b31":
        ZS = .5
        alt = e.get("alt", 1.5)
        lz = e.get("lz", 1.95)
        P.update({"ex": (2.57, 0, 0), "ey": (0, 2.57, 0), "ez": (0, 0, lz + .12), "M": (-.13, -.02, alt), "muro": (1.159, gg(1.159), alt + .04),
                  "leve": (1.75, .3, 0), "pesado": (.3, 1.8, 0)})
    elif cena == "b61":
        ZS = .25
        P.update({"ex": (2.57, 0, 0), "ey": (0, 3.42, 0), "ez": (0, 0, 2.37)})
        for v in (2, 4, 6, 8):
            P["m%d" % v] = (-.13, -.02, v * ZS)
        r = math.sqrt(LV)
        P.update({"acima": (1.94, 1.94, ZS * 7.6), "abaixo": (.3, .3, ZS * 2), "nivel": (2, 0, ZS * LV), "arco": (r * math.cos(.35), r * math.sin(.35), 0)})
    P.update({"c00": (0, 0, 0), "c20": (2, 0, 0), "c22": (2, 2, 0), "c02": (0, 2, 0)})
    return P


class Palco3D:
    """Fundo 3D por estado. Trackers numéricos (`tr`) + campos fixos (`fixo`, ex.: n, modo) → estado do c32.js a cada quadro.
    A câmera é cam_mix(cam0, cam1, s); `rumo(c)` troca o par (a câmera atual vira cam0) para um novo movimento. Rótulos presos aos pontos."""

    def __init__(self, sc, cena, cam1, cam0=None, s=1.0, **ini):
        self.sc, self.cena = sc, cena
        self.cam0, self.cam1 = cam0 or cam1, cam1
        self.fixo = {k: v for k, v in ini.items() if not isinstance(v, float)}
        self.tr = {"s": ValueTracker(s)}
        for k, v in ini.items():
            if isinstance(v, float):
                self.tr[k] = ValueTracker(v)
        self.fundo = Fundo3D(sc, cena, lambda t: self.estado())
        sc.add(*self.tr.values())

    def cam(self):
        return cam_mix(self.cam0, self.cam1, self.tr["s"].get_value())

    def rumo(self, c):
        self.cam0, self.cam1 = self.cam(), c
        self.tr["s"].set_value(0.0)

    def estado(self):
        e = {"cam": self.cam()}
        for k, t in self.tr.items():
            if k != "s":
                e[k] = round(t.get_value(), 4)
        e.update(self.fixo)
        return e

    def pt(self, nome):
        return proj3d(self.cam(), pontos3d(self.cena, self.estado())[nome])

    def prende(self, m, nome, dx=0.0, dy=0.0, ancora="c"):
        """Prende o centro (ancora c), a borda esquerda (l) ou a direita (r) de `m` ao ponto `nome` + (dx, dy) px; registra para o QA de alinhamento."""
        sc = self.sc
        x, y = self.pt(nome)
        alvo = PX(x + dx, y + dy)
        ref = {"l": np.array([m.get_left()[0], m.get_center()[1], 0]), "r": np.array([m.get_right()[0], m.get_center()[1], 0])}.get(ancora, m.get_center())
        m.shift(alvo - ref)
        m._ref3d = alvo
        m._p3d = (self.cena, nome, dx, dy)

        def f(mm):
            x, y = self.pt(nome)
            alvo = PX(x + dx, y + dy)
            mm.shift(alvo - mm._ref3d)
            mm._ref3d = alvo
            if not PEDIDOS3D:
                fq = int(round(sc.clk.get_value() * FPS))
                sc._al.append((sc.lote, self.cena, fq, nome, round(x, 2), round(y, 2)))
        m.add_updater(f)
        return m

    def anim(self, rt=1.0, rate=smooth, **alvos):
        return [self.tr[k].animate(run_time=rt, rate_func=rate).set_value(v) for k, v in alvos.items()]

    def set(self, **kv):
        for k, v in kv.items():
            if k in self.tr:
                self.tr[k].set_value(v)
            else:
                self.fixo[k] = v


# ── cena-base do vídeo ─────────────────────────────────────────────────────────────────────────────────────
CANETA_P = float(os.environ.get("CANETA_P", "0.055"))      # s entre glifos (traço finíssimo, esquerda → direita)


class B32(Base):
    """Base do kit + caneta rápida, voos, sublinhado de leitura, papel com a grade dos eixos, marcas dos alvos e QA R5/alinhamento."""

    def setup_base(self):
        super().setup_base()
        # logo dos quadros-alvo (sb31: logo_crop.png 240×85 em (1650, 24), opaca), no lugar da marca d'água a 45 % do kit
        self.remove(self.wm)
        self.wm = ImageMobject(str(AQUI / "referencia" / "logo_crop.png")).set_width(240 / 120).move_to(PX(1650 + 120, 24 + 42.5)).set_z_index(40)
        self.add(self.wm)
        self._al = []
        self._r5 = []
        self.grade = None
        self._t0wall = time.time()

    def _estilo(self, anims=()):          # estilo do sb31: sem contorno escuro automático
        return

    # escrita --------------------------------------------------------------------------------------------
    def pena(self, *ms, atraso=0.0, passo=None, extra=(), rt=None, lag=0.0):
        """Caneta em uma ou mais fórmulas/legendas (glifo a glifo, esquerda → direita); `lag` s entre o início de cada uma."""
        p = passo or CANETA_P
        anims = []
        marcados = []
        for k, m in enumerate(ms):
            if not hasattr(m, "_tex"):
                m._tex = getattr(m, "_txt", type(m).__name__)
            for x in m.get_family():
                if getattr(x, "_caneta", False):
                    x._em_caneta = True
                    marcados.append(x)
            anims.append(caneta(m, atraso=atraso + k * lag, ritmo=p / 0.30))
        tot = max(a.tot for a in anims)
        self.play(*anims, *extra, run_time=rt or tot)
        for x in marcados:
            x._em_caneta, x._esc = False, True

    def escreve(self, F, voos=(), atraso_caneta=0.5, rt_voo=1.0, extra=(), passo=None, arco=-0.6):
        """F nasce em parte do desenho (voos = [(origem, [índices de glifo em F[0]])]: TransformFromCopy em arco) e o resto a caneta."""
        p = passo or CANETA_P
        gl = list(F[0]) if len(F.submobjects) == 1 else [g for g in F.family_members_with_points()]
        voados = set()
        anims = []
        for src, idx in voos:
            alvo = VGroup(*[gl[i] for i in idx])
            anims.append(TransformFromCopy(src, alvo, path_arc=arco, run_time=rt_voo))
            voados |= set(idx)
        resto = VGroup(*[g for i, g in enumerate(gl) if i not in voados])
        if len(resto):
            resto._tex = F._tex + " (resto)"
            anims.append(caneta(resto, atraso=atraso_caneta if voos else 0.0, ritmo=p / 0.30))
        tot = max([rt_voo] + [a.tot for a in anims if isinstance(a, _Caneta)])
        F._em_caneta = True
        self.play(*anims, *extra, run_time=tot)
        self.remove(*[a.mobject for a in anims if isinstance(a, _Caneta)])
        for a in anims:
            if isinstance(a, TransformFromCopy):         # no Manim o TransformFromCopy anima o ALVO de trás para a frente: a origem é target_mobject
                self.remove(a.mobject)
        F._em_caneta, F._esc = False, True
        self.add(F)

    def sublinha(self, m_glifos, rt_vis=1.2):
        """Sublinhado de leitura: traço branco fino (2 px) sob os glifos por `rt_vis` s e some (dentro de um único play)."""
        x0, x1 = pxof(m_glifos.get_left())[0], pxof(m_glifos.get_right())[0]
        y = pxof(m_glifos.get_bottom())[1] + 7
        s = sublinha_px(x0 - 2, x1 + 2, y)
        self.play(Create(s), run_time=0.25)
        self.wait(rt_vis)
        self.play(FadeOut(s), run_time=0.25)
        self.remove(s)

    # papel ----------------------------------------------------------------------------------------------
    def grade_on(self, v=CH, rt=0.5, junto=()):
        if self.grade is not None:
            return
        self.grade = papel(v).set_z_index(-10)
        if rt > 0:
            self.play(FadeIn(self.grade), *junto, run_time=rt)
        else:
            self.add(self.grade)

    def grade_off(self, rt=0.5, junto=()):
        if self.grade is None:
            return
        g, self.grade = self.grade, None
        if rt > 0:
            self.play(FadeOut(g), *junto, run_time=rt)
        self.remove(g)

    def fixos(self):
        f = super().fixos()
        if getattr(self, "grade", None) is not None:
            f = set(f) | {self.grade}
        return f

    # marcas e QA ----------------------------------------------------------------------------------------
    def marca(self, alvo, agora=False):
        """Instante do estado final de um quadro-alvo (prancha render × alvo): o fim da âncora corrente (0,2 s antes), ou agora + 0,3 s."""
        t = self.nq / FPS + 0.3 if agora else (self.alvo / FPS - 0.6)
        print(f"[marca] {alvo} {t:.3f}")

    def gat(self, frase):
        super().gat(frase)
        self.r5()

    def r5(self, onde=""):
        """R5: caixas de texto/fórmula visíveis não se cruzam entre si nem com pontos marcados."""
        caixas = []
        for m in self.mobjects:
            for x in m.get_family():
                if getattr(x, "_txt", None) is None and not getattr(x, "_obst", False):
                    continue
                if isinstance(x, VMobject) and not x.family_members_with_points():
                    continue
                ops = [g.get_fill_opacity() for g in x.family_members_with_points() if isinstance(g, VMobject)]
                if not ops or max(ops) < 0.3:
                    continue
                if getattr(x, "_txt", None) is not None and any(getattr(y, "_txt", None) is not None and y is not x and x in y.get_family()
                                                                   for y in m.get_family()):
                    continue
                x0, y1 = pxof(x.get_corner(UL))
                x1, y0 = pxof(x.get_corner(DR))
                caixas.append((getattr(x, "_txt", None) or "ponto", (x0, y1, x1, y0), getattr(x, "_obst", False), x))
        for i in range(len(caixas)):
            for j in range(i + 1, len(caixas)):
                a, b = caixas[i], caixas[j]
                if a[2] and b[2]:
                    continue
                if a[3] in b[3].get_family() or b[3] in a[3].get_family():
                    continue
                (ax0, ay0, ax1, ay1), (bx0, by0, bx1, by1) = a[1], b[1]
                ox = min(ax1, bx1) - max(ax0, bx0)
                oy = min(ay1, by1) - max(ay0, by0)
                if ox > 2 and oy > 2:
                    self._r5.append((self._aid, self.t, a[0], b[0], ox, oy))
                    print(f"[R5] {self._aid} {self.t:7.2f}s {a[0]!r} x {b[0]!r} ({ox:.0f}x{oy:.0f} px) {onde}")

    def fim(self):
        super().fim()
        if self._al:
            d = AQUI / "renders" / "v1" / "qa" / "al"
            d.mkdir(parents=True, exist_ok=True)
            (d / f"{self.lote}.json").write_text(json.dumps(self._al), encoding="utf-8")
        print(f"[R5-total] {self.lote} {len(self._r5)}")
        print(f"[parede] {self.lote} {time.time() - self._t0wall:.0f}s")

    # utilidades ------------------------------------------------------------------------------------------
    def troca(self, saem=(), entram=(), rt=0.5):
        anims = [FadeOut(m) for m in saem] + [FadeIn(m) for m in entram]
        if anims:
            self.play(*anims, run_time=rt)
        self.remove(*saem)

    def some(self, *ms, rt=0.4):
        ms = [m for m in ms if m is not None]
        if ms:
            self.play(*[FadeOut(m) for m in ms], run_time=rt)
            for m in ms:
                m.clear_updaters()
            self.remove(*ms)




def entra3d(sc, palco, saem=(), rt_x=0.5, rt_cam=2.0, junto_cam=()):
    """Pouso de entrada: o 3D (vista de cima, que coincide com a chapa 2D) aparece por baixo enquanto a chapa 2D sai; depois a câmera sobe
    até a câmera do alvo em rt_cam s. A grade do papel sai junto (3D sem grade)."""
    palco.fundo.op.set_value(0.0)
    sc.add(palco.fundo)
    anims = [palco.fundo.op.animate.set_value(1.0)] + [FadeOut(m) for m in saem]
    if sc.grade is not None:
        g, sc.grade = sc.grade, None
        anims.append(FadeOut(g))
        saem = list(saem) + [g]
    sc.play(*anims, run_time=rt_x)
    sc.remove(*saem)
    sc.play(*palco.anim(rt_cam, s=1.0), *junto_cam, run_time=rt_cam)


def sai3d(sc, palco, entram=(), rt_x=0.5, rt_cam=2.0, junto_cam=(), grade=True):
    """Pouso inverso: a câmera desce até a vista de cima (junto_cam: o prédio/muro baixa) e a chapa 2D volta por cima, alinhada."""
    sc.play(*palco.anim(rt_cam, s=0.0), *junto_cam, run_time=rt_cam)
    anims = [palco.fundo.op.animate.set_value(0.0)] + [FadeIn(m) for m in entram]
    if grade and sc.grade is None:
        sc.grade = papel(CH).set_z_index(-10)
        anims.append(FadeIn(sc.grade))
    sc.play(*anims, run_time=rt_x)
    palco.fundo.clear_updaters()
    sc.remove(palco.fundo, *palco.tr.values())


def mapa_glifos(sc, fontes, alvo, mapa, rt=1.4, extra=()):
    """Equivalente ao TransformByGlyphMap com mais de uma fórmula de origem: mapa = [(fórmula, [índices]), [índices no alvo]];
    glifos de origem fora do mapa somem; glifos do alvo fora do mapa nascem (FadeIn), como o auto_fade do MF-Tools."""
    ga = list(alvo[0])
    usados_a, anims = set(), []
    usados_f = {id(F): set() for F in fontes}
    for (F, ii), jj in mapa:
        src = VGroup(*[F[0][i] for i in ii])
        dst = VGroup(*[ga[j] for j in jj])
        anims.append(ReplacementTransform(src.copy(), dst))
        usados_a |= set(jj)
        usados_f[id(F)] |= set(ii)
    for F in fontes:
        resto = [g for i, g in enumerate(F[0]) if i not in usados_f[id(F)]]
        if resto:
            anims.append(FadeOut(VGroup(*resto)))
    novos = [g for j, g in enumerate(ga) if j not in usados_a]
    if novos:
        anims.append(FadeIn(VGroup(*novos)))
    sc.remove(*fontes)
    sc.play(*anims, *extra, run_time=rt)
    sc.remove(*[a.mobject for a in anims])
    for a in anims:
        if isinstance(a, ReplacementTransform):
            sc.remove(a.target_mobject)
    alvo._esc = True
    sc.add(alvo)
