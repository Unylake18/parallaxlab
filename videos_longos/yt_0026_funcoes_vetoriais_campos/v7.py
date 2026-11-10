"""yt_0026 · v7 — helpers do sistema visual simples (handoff v7). Porta as funções do storyboard `referencia_v7/.../sb2.html` (canvas 1920×1080) para o Manim.
Tudo em pixels de 1080p (1 u = 120 px): `PX(x, y)`; `Vista(cx, cy, u)` é o plano matemático do storyboard (u px por unidade). Só setas, curvas, fórmulas e formas sólidas.
Regras: seta sem contorno/brilho/opacidade; campo de contexto = cor escura opaca (mistura com o fundo); sem partículas, sem pontinhos soltos, sem sombras."""
from kit import *  # noqa: F401,F403

CHAPA = "#13234A"
CAMPO2 = "#8CFFD2"
FUNDO_C = "#0B1730"
POS7 = "#E08A3C"


def PX(x, y):
    return P3((x - 960) / 120, 4.5 - y / 120)


def fs(px):
    """font_size do MathTex que equivale ao KaTeX de `px` pixels (altura de caixa medida)."""
    return px * 0.803


def ts(px):
    """size do `txt` (Space Grotesk) que equivale ao fillText de `px` pixels."""
    return px * 0.6


def mix(a, b, t):
    return interpolate_color(ManimColor(a), ManimColor(b), min(1.0, max(0.0, t)))


class Vista(Plano):
    """Plano do storyboard: origem em (cx, cy) px e `u` px por unidade (y para cima)."""

    def __init__(self, cx, cy, u, uy=None):
        p = PX(cx, cy)
        super().__init__((p[0], p[1]), u / 120, (uy / 120) if uy else None)
        self.cx, self.cy, self.u = cx, cy, u


def seta7(a, b, cor, w=5, head=20):
    """Seta (haste + ponta cheia, largura da ponta = comprimento da ponta), em pontos do Manim; w e head em px de 1080p."""
    return seta(np.asarray(a, float), np.asarray(b, float), cor, w / 1.2, tip=head / 120)


def campo7(v, Fv, x0=-3, x1=3, y0=-3, y1=3, passo=0.5, rmin=0.3, rmax=99, lmax=0.42, mmax=1.0, alpha=1.0, c=(0, 0), head=19, nome="campo"):
    """Campo de setas CENTRADAS no ponto da grade; comprimento L = lmax·(0,4 + 0,6·t), t = min(1, |F|/mmax) (nunca vira pontinho); cor de CAMPO a CAMPO2 pela
    intensidade; alpha < 1 = cor escura OPACA (mistura com o fundo). Loga a razão maior seta ÷ passo."""
    g = VGroup()
    n = int(math.floor((x1 - x0) / passo + 1e-6))          # mesma grade do for do storyboard: X de x0 até x1 (inclusive) em passos de `passo`
    m = int(math.floor((y1 - y0) / passo + 1e-6))
    for i in range(n + 1):
        for j in range(m + 1):
            X, Y = x0 + i * passo, y0 + j * passo
            r = math.hypot(X - c[0], Y - c[1])
            if r < rmin or r > rmax:
                continue
            f = Fv(X, Y)
            mag = math.hypot(*f)
            if mag < 1e-9:
                continue
            t = min(1.0, mag / mmax)
            L = lmax * (0.4 + 0.6 * t)
            u = (f[0] / mag * L, f[1] / mag * L)
            cor = mix(CAMPO, FUNDO_C, 1 - alpha) if alpha < 1 else mix(CAMPO, CAMPO2, t)
            s = seta7(v.c2p(X - u[0] / 2, Y - u[1] / 2), v.c2p(X + u[0] / 2, Y + u[1] / 2), cor, 5, head)
            s._xy, s._L, s._t = (X, Y), L, t
            g.add(s)
    Ls = [s._L for s in g]
    if Ls:
        print(f"[campo] {nome}: {len(g)} setas, maior {max(Ls):.3f} u, menor {min(Ls):.3f} u (razão {min(Ls) / max(Ls):.2f}), maior ÷ passo = {max(Ls) / passo:.2f}")
    return g


def T(s, x, y, size=30, al="left", cor=WHITE_, bold=True):
    """Texto de tela (fillText): x e y em px; y é a LINHA DE BASE; al = left | center | right; bold = Space Grotesk Bold, senão Medium."""
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
    return m.set_z_index(30)


def legenda(s, x, y, cor=SAI_F, al="left", size=28):
    return T(s, x, y, size, al, cor, bold=False)


def rot_abertura(s):
    return T(s, 960, 150, 40, "center")


def TX(*pares, x=960, y=540, size=56, al="c", caneta=True):
    """Fórmula (MathTex colorido em partes) com o CENTRO VERTICAL em y px e alinhamento horizontal em x px (c | l | r)."""
    m = F(*pares, size=fs(size), caneta=caneta)
    p = PX(x, y)
    m.move_to(p)
    if al == "l":
        m.shift(RIGHT * (p[0] - m.get_left()[0]))
    elif al == "r":
        m.shift(RIGHT * (p[0] - m.get_right()[0]))
    return m.set_z_index(25)


def painel(x0, y0, w, h, rot=None, cor=GEO):
    """Painel arredondado (raio 14): fundo #091226 a 72 %, borda GEO a 35 %. Rótulo (ENTRADA/SAÍDA…) 18 px acima do topo."""
    r = RoundedRectangle(width=w / 120, height=h / 120, corner_radius=14 / 120).move_to(PX(x0 + w / 2, y0 + h / 2))
    r.set_fill("#091226", 0.72).set_stroke(GEO, 1.7, 0.35)
    r._sem_contorno = True
    r.set_z_index(-40)
    g = VGroup(r)
    if rot:
        g.add(legenda(rot, x0 + w / 2, y0 - 18, cor, "center"))
    return g


def contorno_painel(x0, y0, w, h, cor=CAMPO, wpx=3):
    r = RoundedRectangle(width=w / 120, height=h / 120, corner_radius=14 / 120).move_to(PX(x0 + w / 2, y0 + h / 2)).set_fill(opacity=0).set_stroke(cor, wpx / 1.2, 1)
    r._sem_contorno = True
    return r.set_z_index(2)


def arco7(x0, y0, x1, y1, rot=None):
    """Seta em arco branca (bezier quadrática com o controle 70 px acima), com a ponta cheia; `rot` (LaTeX) 75 px acima do meio."""
    a, b = PX(x0, y0), PX(x1, y1)
    c = PX((x0 + x1) / 2, y0 - 70)
    curva = VMobject().set_points([a, a + 2 / 3 * (c - a), b + 2 / 3 * (c - b), b]).set_stroke(WHITE_, 4 / 1.2, 1).set_fill(opacity=0)
    d = b - c
    d = d / np.linalg.norm(d)
    n = np.array([-d[1], d[0], 0.0])
    ponta = Polygon(b + d * 0.05, b - d * 0.15 + n * 0.085, b - d * 0.15 - n * 0.085).set_fill(WHITE_, 1).set_stroke(width=0)
    for m in (curva, ponta):
        m._sem_contorno = True
    g = VGroup(curva, ponta).set_z_index(6)
    if rot:
        g.add(TX((rot, WHITE_), x=(x0 + x1) / 2, y=y0 - 75, size=44, caneta=False))
    return g


def eixos7(v, x0, x1, y0, y1, rx=None, ry=None, alpha=0.7, cor=GEO):
    g = VGroup()
    for p, q in (((x0, 0), (x1, 0)), ((0, y0), (0, y1))):
        ln = Line(v.c2p(*p), v.c2p(*q)).set_stroke(cor, 2 / 1.2, alpha)
        ln._sem_contorno = True
        g.add(ln)
    if rx:
        e = v.c2p(x1, 0)
        g.add(TX(rx, x=e[0] * 120 + 960 + 18, y=4.5 * 120 - e[1] * 120, size=34, al="l", caneta=False))
    if ry:
        e = v.c2p(0, y1)
        g.add(TX(ry, x=e[0] * 120 + 960, y=4.5 * 120 - e[1] * 120 - 24, size=34, caneta=False))
    return g.set_z_index(2)


def circ7(v, r, cor=GEO, w=2, dash=None, alpha=1.0, c=(0, 0)):
    m = Circle(radius=r * v.ux).move_to(v.c2p(*c)).set_stroke(cor, w / 1.2, alpha).set_fill(opacity=0)
    m._sem_contorno = True
    if dash:
        m = DashedVMobject(m, num_dashes=max(12, int(2 * PI * r * v.u / (dash[0] + dash[1]))), dashed_ratio=dash[0] / (dash[0] + dash[1]))
        m._sem_contorno = True
    return m


def linha7(pts, cor, w=5, alpha=1.0, dash=None):
    m = VMobject().set_points_as_corners(pts).set_stroke(cor, w / 1.2, alpha).set_fill(opacity=0)
    m._sem_contorno = True
    if dash:
        m = DashedVMobject(m, num_dashes=max(6, int(m.get_arc_length() * 120 / (dash[0] + dash[1]))), dashed_ratio=dash[0] / (dash[0] + dash[1]))
        m._sem_contorno = True
    return m


def ponto7(p, cor, r=9):
    d = Dot(p, radius=r / 120, color=cor).set_z_index(8)
    d._sem_contorno = True
    return d


def bandeira7(v, ang=0.0, c=(0, 0), cor=DEST, preenchida=True, alpha=1.0):
    """Bandeira do storyboard: mastro (1, 0)→(1, 1,9) e triângulo (1, 1,9), (2,3, 1,55), (1, 1,2), girada de `ang` em torno de c."""
    def R(p):
        return (c[0] + p[0] * math.cos(ang) - p[1] * math.sin(ang), c[1] + p[0] * math.sin(ang) + p[1] * math.cos(ang))
    mastro = Line(v.c2p(*R((1, 0))), v.c2p(*R((1, 1.9)))).set_stroke(cor, 5 / 1.2, alpha)
    pano = Polygon(*[v.c2p(*R(p)) for p in ((1, 1.9), (2.3, 1.55), (1, 1.2))]).set_fill(cor, alpha if preenchida else 0).set_stroke(cor, 1.2, alpha)
    for m in (mastro, pano):
        m._sem_contorno = True
    return VGroup(mastro, pano).set_z_index(5)


def malha7(v, n=3, s=1.0, cor=GEO):
    g = VGroup()
    for k in range(-n, n + 1):
        for (a, b) in (((k * s, -n * s), (k * s, n * s)), ((-n * s, k * s), (n * s, k * s))):
            ln = Line(v.c2p(*a), v.c2p(*b)).set_stroke(cor, 1.5 / 1.2, 0.7 if k == 0 else 0.35)
            ln._sem_contorno = True
            g.add(ln)
    return g.set_z_index(2)


def chapa7(pts_manim, cor=CHAPA, op=0.9):
    m = Polygon(*pts_manim).set_fill(cor, op).set_stroke(width=0)
    m._sem_contorno = True
    return m.set_z_index(-39)


def circ_pts(r, n):
    return [(round(r * math.cos(2 * PI * k / n), 9) + 0.0, round(r * math.sin(2 * PI * k / n), 9) + 0.0) for k in range(n)]


def no_canto_ok(m, y_min_px=190):
    """[layout] topo do objeto (px) — para o QA."""
    return (4.5 - m.get_top()[1]) * 120


# ── fórmulas: as MESMAS strings do storyboard (KaTeX), com os macros definidos no preâmbulo do LaTeX ─────────────────────────────────────────
TEX7 = TexTemplate()
TEX7.add_to_preamble(
    r"\usepackage{xcolor}\usepackage{esint}"
    r"\definecolor{ca}{HTML}{FFC24D}\definecolor{cm}{HTML}{EA63FF}\definecolor{cc}{HTML}{2EE6A0}\definecolor{cs}{HTML}{7FB2FF}"
    r"\definecolor{cg}{HTML}{B8C4DA}\definecolor{cp}{HTML}{E08A3C}\definecolor{cv}{HTML}{9C8CFF}"
    r"\def\X{\textcolor{ca}{x}}\def\Y{\textcolor{cm}{y}}\def\F{\textcolor{cc}{\vec F}}"
    r"\def\ii{\vec\imath}\def\jj{\vec\jmath}\def\th{\textcolor{ca}{\theta}}\def\rh{\textcolor{cm}{\rho}}"
    r"\def\U{\textcolor{ca}{u}}\def\V{\textcolor{cm}{v}}\def\S#1{\textcolor{cs}{#1}}\def\G#1{\textcolor{cg}{#1}}"
    r"\def\P#1{\textcolor{cp}{#1}}\def\gp{\textcolor{cv}{\gamma'(t)}}\def\sen{\operatorname{sen}}\def\rot{\operatorname{rot}}")


def TC(s, x=960, y=540, size=56, al="l", caneta=True):
    """Fórmula do storyboard (string KaTeX/LaTeX com os macros do preâmbulo) com o centro vertical em y px e o alinhamento horizontal em x px (l | c | r)."""
    import re as _re
    s2 = r"\textstyle " + s if _re.search(r"\\(i+nt|oi+nt|oint)", s) and "displaystyle" not in s else s       # integrais em estilo de texto (como no KaTeX inline do storyboard)
    m = MathTex(s2, font_size=fs(size), tex_template=TEX7)
    m._tex, m._caneta, m._esc, m._em_caneta = s, caneta, not caneta, False
    p = PX(x, y)
    m.move_to(p)
    if al == "l":
        m.shift(RIGHT * (p[0] - m.get_left()[0]))
    elif al == "r":
        m.shift(RIGHT * (p[0] - m.get_right()[0]))
    return m.set_z_index(25)


# ── 3D (c7.js): projeção de um ponto do mundo para o Manim, com a mesma câmera e a mesma caixa do render ────────────────────────────────────
CAMS7 = {"colunas": ((9.6, -8.2, 7.2), (1.5, 1.0, 1.0)), "fluxo": ((9.0, -11.2, 7.0), (0, 0, 1.0)), "paraboloide": ((9.0, -11.2, 7.0), (0, 0, 1.0)),
         "campo": ((8.3, -8.3, 4.6), (0, 0, 0))}


BBOX7 = {"colunas": (560.5, 292.1, 1370.8, 945.7), "fluxo": (628.0, 268.9, 1292.0, 719.7), "paraboloide": (585.3, 77.8, 1399.8, 875.0), "campo": (445.9, 29.4, 1474.6, 1022.4)}


def proj_c7(cena, box, p, az=0.0):
    pos, look = (np.array(a, float) for a in CAMS7[cena])
    if az:
        c, s_ = math.cos(math.radians(az)), math.sin(math.radians(az))
        pos = np.array([pos[0] * c - pos[1] * s_, pos[0] * s_ + pos[1] * c, pos[2]])
    f = look - pos
    f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1.0])
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    q = np.asarray(p, float) - pos
    x, y, z = q @ r, q @ u, q @ f
    th = math.tan(math.radians(22) / 2)
    nx, ny = x / z / (th * 16 / 9), y / z / th
    vx, vy = (nx + 1) / 2 * 1920, (1 - ny) / 2 * 1080
    bx, by, bw, bh = box
    x0, y0, x1, y1 = BBOX7[cena]
    s = 0.94 * min(bw / (x1 - x0), bh / (y1 - y0))
    return PX(bx + bw / 2 + (vx - (x0 + x1) / 2) * s, by + bh / 2 + (vy - (y0 + y1) / 2) * s)


def rotulo3d(texto, p, dx, dy, cor="#CFE2FF"):
    """Rótulo preso a um ponto do 3D (como o `rotulo` do c3d.html): ponto com anel + placa escura com o texto (30 px) deslocada (dx, dy) px."""
    x, y = p[0] * 120 + 960, 4.5 * 120 - p[1] * 120
    pt = Dot(p, radius=7 / 120, color=cor).set_z_index(9)
    pt._sem_contorno = True
    t = T(texto, x + dx + 10, y + dy, 30, "left", cor, bold=False)
    r = RoundedRectangle(width=t.width + 20 / 120, height=40 / 120, corner_radius=8 / 120).move_to(t.get_center()).set_fill("#060C1A", 0.82).set_stroke(cor, 1.7, 1).set_z_index(8)
    r._sem_contorno = True
    return VGroup(r, t, pt)
