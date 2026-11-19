"""yt_0036 · peças deste vídeo sobre o p36.py (kit copiado do yt_0035): cores de u/v/|J|, macros LaTeX, célula no estilo do quadradinho do
EP. 03 (chapa + malha), famílias de retas recortadas no painel, seta φ, planos com papel próprio, rótulos mistos com placa, chip |J| = 1/2,
câmera da decolagem/pouso (vista de cima ortográfica ↔ oblíqua) e pontos da cena 3D (porte de referencia/c3d36.html).
Tudo em px de 1080p (PX), como no referencia/sb36.html."""
from p36 import *  # noqa: F401,F403
from p36 import _TC_qa  # noqa: F401
from kit import _Caneta  # noqa: F401
import v36 as _v

CU, CVV, LIMA, CHAPA, MALHA = "#FF9440", "#2EE6A6", "#C6F26B", "#663A4C", "#FFB3BC"
TEX31.add_to_preamble(
    r"\definecolor{uc}{HTML}{FF9440}\definecolor{vc}{HTML}{2EE6A6}\definecolor{lm}{HTML}{C6F26B}\definecolor{br}{HTML}{F5F7FF}"
    r"\def\uu{\textcolor{uc}{u}}\def\vv{\textcolor{vc}{v}}\def\Uc#1{\textcolor{uc}{#1}}\def\Vc#1{\textcolor{vc}{#1}}\def\Lm#1{\textcolor{lm}{#1}}"
    r"\def\du{\textcolor{uc}{du}}\def\dv{\textcolor{vc}{dv}}\def\Du{\textcolor{uc}{\Delta u}}\def\Dv{\textcolor{vc}{\Delta v}}"
    r"\def\Jq{\dfrac{\partial(\X,\Y)}{\partial(\uu,\vv)}}\def\JJ{\Lm{\left|\Jq\right|}}"
    r"\def\pu{\dfrac{\partial\varphi}{\partial\uu}}\def\pv{\dfrac{\partial\varphi}{\partial\vv}}\def\dd#1#2{\dfrac{\partial #1}{\partial #2}}"
    r"\def\xu{\X_{\uu}}\def\xv{\X_{\vv}}\def\yu{\Y_{\uu}}\def\yv{\Y_{\vv}}")
TITULO_CANTO = "CÁLCULO III · MUDANÇA DE VARIÁVEIS"


def mapT(u, v):
    return ((u + v) / 2, (u - v) / 2)


def mapC(u, v):
    return (u * u - v * v, 2 * u * v)


def mapL(u, v):
    return (2 * u + v, u + 3 * v)


def ID(u, v):
    return (u, v)


def inv(v, p):
    """Ponto do Manim → coordenadas da vista v."""
    X, Y = pxof(p)
    return ((X - v.cx) / v.u, (v.cy - Y) / v.uy)


def leva(v0, v1, F=ID):
    """Função do Manim para ApplyPointwiseFunction: ponto na vista v0 → F → mesma coisa na vista v1."""
    def f(p):
        a, b = inv(v0, p)
        return v1.P(*F(a, b))
    return f


# ── célula (quadradinho do EP. 03: chapa + malha n × n + borda) ───────────────────────────────────────────
def borda_pts(v, F, u0, u1, v0, v1, N=24):
    P = lambda a, b: v.P(*F(a, b))
    return ([P(u0 + (u1 - u0) * i / N, v0) for i in range(N + 1)] + [P(u1, v0 + (v1 - v0) * i / N) for i in range(1, N + 1)] +
            [P(u1 - (u1 - u0) * i / N, v1) for i in range(1, N + 1)] + [P(u0, v1 - (v1 - v0) * i / N) for i in range(1, N)])


def celula(v, F, u0, u1, v0, v1, n=4, wb=3, N=24, z=3, borda=MALHA, fill=CHAPA, fop=1.0, wm=1.5, am=.75):
    pts = borda_pts(v, F, u0, u1, v0, v1, N)
    fl = Polygon(*pts).set_fill(fill, fop).set_stroke(width=0)
    ml = VGroup()
    for k in range(1, n):
        a, b = u0 + (u1 - u0) * k / n, v0 + (v1 - v0) * k / n
        ml.add(VMobject().set_points_as_corners([v.P(*F(a, v0 + (v1 - v0) * i / N)) for i in range(N + 1)]).set_stroke(MALHA, W(wm), am))
        ml.add(VMobject().set_points_as_corners([v.P(*F(u0 + (u1 - u0) * i / N, b)) for i in range(N + 1)]).set_stroke(MALHA, W(wm), am))
    bd = VMobject().set_points_as_corners(pts + [pts[0]]).set_stroke(borda, W(wb), 1).set_fill(opacity=0)
    g = VGroup(fl, ml, bd)
    g.fill, g.malha, g.borda = fl, ml, bd
    sem_ctn(g)
    fl.set_z_index(z)
    ml.set_z_index(z + 1)
    bd.set_z_index(z + 2)
    return g


def poligono(v, pts, fill=None, fop=1.0, cor=None, wpx=3, z=2):
    """Região poligonal (coordenadas da vista) com preenchimento e/ou borda, como VGroup(fill, borda)."""
    g = VGroup()
    if fill:
        g.add(poly_px([v.px(*p) for p in pts], fill, fop, z=z))
    if cor:
        g.add(lin_px([v.px(*p) for p in list(pts) + [pts[0]]], cor, wpx, z=z + 1))
    return g


# ── famílias de retas recortadas no painel ────────────────────────────────────────────────────────────────
def clip_param(P0, d, box):
    a0, a1, b0, b1 = box
    lo, hi = -1e9, 1e9
    for i, (mn, mx) in enumerate(((a0, a1), (b0, b1))):
        if abs(d[i]) < 1e-12:
            if not (mn - 1e-9 <= P0[i] <= mx + 1e-9):
                return None
        else:
            t1, t2 = (mn - P0[i]) / d[i], (mx - P0[i]) / d[i]
            lo, hi = max(lo, min(t1, t2)), min(hi, max(t1, t2))
    return (lo, hi) if hi - lo > 1e-6 else None


def seg_fam(F, k, tipo, box):
    """Reta da família u = k (tipo 'u') ou v = k (tipo 'v') de uma F linear, recortada em box. Devolve 2 pontos (coordenadas da vista) ou None."""
    if tipo == "u":
        P0, P1 = np.array(F(k, 0.0)), np.array(F(k, 1.0))
    else:
        P0, P1 = np.array(F(0.0, k)), np.array(F(1.0, k))
    d = P1 - P0
    r = clip_param(P0, d, box)
    if r is None:
        return None
    return [tuple(P0 + d * r[0]), tuple(P0 + d * r[1])]


def familia(v, F, ks, tipo, box, cor, wpx=1.6, alpha=.55, z=-9, todas=False):
    """todas=True: também as retas que só entram no painel durante um movimento (nascem apagadas)."""
    g = VGroup()
    for k in ks:
        s = seg_fam(F, k, tipo, box)
        if s is None and not todas:
            continue
        if s is None:
            m = lin_px([v.px(0, 0), v.px(0, 0)], cor, wpx, alpha, z=z)
            m.set_stroke(opacity=0)
        else:
            m = lin_px([v.px(*s[0]), v.px(*s[1])], cor, wpx, alpha, z=z)
        m._k, m._tipo, m._alpha = k, tipo, alpha
        g.add(m)
    g._sem_foco = True
    return g


def familia_anim(v, g, Fa, box, rt=2.0):
    """A grade inteira se inclina num movimento só: F(α) = (1 − α) I + α A (linear), cada reta recortada no painel a cada quadro."""
    alfa0 = {id(m): getattr(m, "_alpha", m.get_stroke_opacity()) for m in g}

    def upd(gg, a):
        F = Fa(smooth(a))
        for m in gg:
            s = seg_fam(F, m._k, m._tipo, box)
            if s is None:
                m.set_stroke(opacity=0)
                continue
            m.set_points_as_corners([v.P(*s[0]), v.P(*s[1])])
            m.set_stroke(opacity=alfa0[id(m)])
    return UpdateFromAlphaFunc(g, upd, run_time=rt, rate_func=linear)


def lin_mix(A):
    """α ↦ F linear (1 − α) I + α A (A = ((a, b), (c, d)): (u, v) ↦ (a u + b v, c u + d v))."""
    (a, b), (c, d) = A

    def Fa(al):
        return lambda u, w: ((1 - al) * u + al * (a * u + b * w), (1 - al) * w + al * (c * u + d * w))
    return Fa


# ── papel na tela inteira (handoff v2 §1): a grade de fundo é uma só por cena e cobre os 1920 × 1080 ───────────────────────
def area_px(v, x0=0, x1=1920):
    """Faixa vertical de x0 a x1 px (altura toda) nas unidades da vista v (para o area= do papel)."""
    return ((x0 - v.cx) / v.u, (x1 - v.cx) / v.u, (v.cy - 1080) / v.uy, v.cy / v.uy)


def grade_tela(*vs, emenda=None, passo=None):
    """() → papel() na unidade padrão; (v,) → papel(v) no quadro todo; (vE, vD) → cada grade até a emenda vertical (px a 1080p)."""
    if not vs:
        g = papel()
    elif len(vs) == 1:
        g = papel(vs[0], area=area_px(vs[0]), passo=passo)
    else:
        g = VGroup(papel(vs[0], area=area_px(vs[0], 0, emenda), passo=passo), papel(vs[1], area=area_px(vs[1], emenda, 1920), passo=passo))
    g.set_z_index(-10)
    for x in g.get_family():
        x._sem_foco = True
    g._emenda = emenda
    return g


# ── planos (eixos + marcas; a grade é a do fundo da cena, J36.fundo) ───────────────────────────────────────────────────────
def monta_plano(v, area, a1, b1, a0=-.06, b0=-.06, uv=False, ticks=()):
    g = VGroup()                          # v2: sem papel recortado no painel (o fundo da cena cobre a tela inteira)
    g._sem_foco = True
    kw = dict(lx=r"\uu", ly=r"\vv", cx=CU, cy=CVV) if uv else {}
    sx, sy, Lx, Ly = eixos_v(v, a1, b1, a0, b0, **kw)
    tks = [tick(v, e, val, tex, 26) for e, val, tex in ticks]
    return {"v": v, "g": g, "sx": sx, "sy": sy, "lx": Lx, "ly": Ly, "tk": tks}


def todos_plano(d):
    return [d["g"], d["sx"], d["sy"], d["lx"], d["ly"]] + [x for t in d["tk"] for x in t]


def entra_plano(sc, d, rt=0.6, extra=(), caneta=True):
    v = d["v"]
    sc.play(FadeIn(d["g"]), GrowFromPoint(d["sx"], v.P(0, 0)), GrowFromPoint(d["sy"], v.P(0, 0)), *[Create(t[0]) for t in d["tk"]], *extra, run_time=rt)
    labs = [d["lx"], d["ly"]] + [t[1] for t in d["tk"]]
    if caneta:
        sc.pena(*labs, lag=0.05)
    else:
        for m in labs:
            ja_escrita(m)
        sc.add(*labs)


def plano(sc, v, area, a1, b1, a0=-.06, b0=-.06, uv=False, ticks=(), rt=0.6, extra=()):
    d = monta_plano(v, area, a1, b1, a0, b0, uv, ticks)
    entra_plano(sc, d, rt, extra)
    return d


# ── seta φ (arco por cima, entre os dois planos) ───────────────────────────────────────────────────────────
def phi_seta(X0, X1, Y, tex=r"\varphi", size=36, alto=70, z=6):
    c = ((X0 + X1) / 2, Y - alto)
    pts = [((1 - t) ** 2 * X0 + 2 * (1 - t) * t * c[0] + t * t * X1, (1 - t) ** 2 * Y + 2 * (1 - t) * t * c[1] + t * t * Y) for t in np.linspace(0, 1, 32)]
    curva = lin_px(pts[:-1], GEO, 3, z=z)
    d = np.array([X1 - c[0], Y - c[1]], float)
    d /= np.linalg.norm(d)
    n = np.array([-d[1], d[0]])
    B = np.array([X1, Y], float)
    ponta = sem_ctn(Polygon(PX(*B), PX(*(B - 18 * d + 9 * n)), PX(*(B - 18 * d - 9 * n))).set_fill(GEO, 1).set_stroke(width=0)).set_z_index(z)
    lab = TC(tex, (X0 + X1) / 2, Y - alto + 8 - size * .55, size, "c") if tex else None
    return VGroup(curva, ponta), lab


def arco_seta(cx, cy, r, a0, a1, anti, cor=BR, wpx=4, z=8):
    """Seta circular (ângulos de tela, y para baixo, como o arc() do canvas). anti=True: ângulo decrescente = anti-horário na tela."""
    if anti:
        while a1 > a0:
            a1 -= TAU
    else:
        while a1 < a0:
            a1 += TAU
    ang = np.linspace(a0, a1, 60)
    pts = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in ang]
    corpo = lin_px(pts[:-3], cor, wpx, z=z)
    B = np.array(pts[-1])
    d = B - np.array(pts[-4])
    d /= np.linalg.norm(d)
    n = np.array([-d[1], d[0]])
    ponta = sem_ctn(Polygon(PX(*(B + 6 * d)), PX(*(B - 12 * d + 8 * n)), PX(*(B - 12 * d - 8 * n))).set_fill(cor, 1).set_stroke(width=0)).set_z_index(z)
    return VGroup(corpo, ponta)


# ── rótulos ──────────────────────────────────────────────────────────────────────────────────────────────
def rotm(partes, X, Y, S=26, al="c", placa=True):
    """Rótulo misto (Text + MathTex lado a lado) com placa mínima. partes como no mixl: ('t', texto[, cor]) | ('m', tex)."""
    m = mixl(partes, 0, Y, S)
    L_, R_ = pxof(m.get_left())[0], pxof(m.get_right())[0]
    x0 = X if al == "l" else (X - (R_ - L_) / 2 if al == "c" else X - (R_ - L_))
    m.shift(RIGHT * (x0 - L_) / 120)
    if not placa:
        return m
    g = VGroup(placa_min(m, 8, 4), m)
    g.f = m
    return g


def rot_v(v, tex, p, dx=0, dy=0, size=26, al="c"):
    """Rótulo matemático com placa, preso a um ponto da vista v (+ deslocamento em px)."""
    q = v.px(*p)
    return TP(tex, q[0] + dx, q[1] + dy, size, al)


def placa_txt2(s, X, Y, cor=AL, size=26):
    """Placa preenchida com borda na cor (TRAVA)."""
    t = T(s, X, Y, size, "left", cor)
    r = RoundedRectangle(width=t.width + 24 / 120, height=t.height + 22 / 120, corner_radius=8 / 120).move_to(t.get_center())
    r.set_fill(BG_, .92).set_stroke(cor, W(2), 1)
    sem_ctn(r).set_z_index(29)
    return VGroup(r, t)


def circ_num(n, X, Y, cor=GEO):
    c = circ_px(X, Y, 17, cor, 2, z=26)
    t = T(str(n), X, Y + 9, 26, "center", cor)
    return VGroup(c, t)


def linha_mista(sc, partes, X, Y, S=34):
    m = mixl(partes, X, Y, S)
    return m


# ── matriz: índices de glifo por casa (para os glyph maps) ─────────────────────────────────────────────────
def casas(m, idx, nr, nc):
    """Agrupa os glifos `idx` de uma matriz em casas (linha, coluna) pela posição; os delimitadores (altos) vão em 'del'."""
    gs = [(i, m[0][i]) for i in idx]
    top = max(g.get_top()[1] for _, g in gs)
    bot = min(g.get_bottom()[1] for _, g in gs)
    Ht = top - bot
    dl = [i for i, g in gs if g.height > .6 * Ht]
    en = [(i, g) for i, g in gs if i not in dl]

    def cortes(vals, n):
        s = sorted(vals)
        gaps = sorted(range(len(s) - 1), key=lambda k: s[k + 1] - s[k], reverse=True)[:n - 1]
        return [(s[k] + s[k + 1]) / 2 for k in sorted(gaps)]
    ys = cortes([g.get_center()[1] for _, g in en], nr)[::-1]
    xs = cortes([g.get_center()[0] for _, g in en], nc)
    out = {"del": dl}
    for i, g in en:
        y, x = g.get_center()[1], g.get_center()[0]
        r = sum(1 for c in sorted(ys, reverse=True) if y < c)
        c = sum(1 for c_ in xs if x > c_)
        out.setdefault((r, c), []).append(i)
    return out


# ── chip |J| = 1/2 (do B3-3 ao B6-1) ─────────────────────────────────────────────────────────────────────
CHIP_BOX = (1560, 146, 240, 78)


def chip_J():
    X0, Y0, w, h = CHIP_BOX
    mol = moldura(X0, Y0, w, h, LIMA, 1.0, 2, 10).set_z_index(26)
    m = L([("J", r"\Lm{|J|=}"), ("h", r"\Lm{\dfrac{1}{2}}")], X0 + w / 2, Y0 + h / 2, 32, "c", caneta=False)
    m.move_to(PX(X0 + w / 2, Y0 + h / 2))
    ja_escrita(m)
    g = VGroup(mol, m)
    g.mol, g.m = mol, m
    return g


class J36(B36):
    CHIP = False

    def setup_base(self):
        super().setup_base()
        self.chipJ = None
        if self.CHIP:
            self.chipJ = chip_J()
            self.add(self.chipJ)
        self._fundo = grade_tela()            # v2 §1: todo lote começa com o papel na tela inteira (unidade padrão)
        self.add(self._fundo)

    def fixos(self):
        f = super().fixos()
        if getattr(self, "chipJ", None) is not None:
            f = set(f) | {self.chipJ}
        if getattr(self, "_fundo", None) is not None:
            f = set(f) | {self._fundo}
        return f

    def fundo(self, *vs, emenda=None, passo=None, rt=0.3, g=None, extra=()):
        """Troca o papel da tela inteira (crossfade ≤ 0,4 s): fundo() padrão, fundo(v), fundo(vE, vD, emenda=px). g= uma grade pronta."""
        novo = g if g is not None else grade_tela(*vs, emenda=emenda, passo=passo)
        velho = self._fundo
        self._fundo = novo
        if getattr(velho, "_emenda", None) is not None or getattr(novo, "_emenda", None) is not None:
            print(f"[emenda] {self._aid} {self.t:.2f} x = {getattr(novo, '_emenda', None)}")
        if rt <= 0:
            if velho is not None:
                self.remove(velho)
            self.add(novo)
            return novo
        self.play(FadeIn(novo), *([FadeOut(velho)] if velho is not None else []), *extra, run_time=rt)
        if velho is not None:
            self.remove(velho)
        return novo

    def fundo_sai(self, rt=0.4, extra=()):
        """Só o trecho 3D (e o CTA): a grade sai em fade."""
        velho, self._fundo = self._fundo, None
        if velho is not None:
            self.play(FadeOut(velho), *extra, run_time=rt)
            self.remove(velho)

    def an(self, aid):
        # palco vivo: a caixa do palco segue o layout da âncora (a mesma máscara do QA, qa36._mascara)
        r = super().an(aid)                 # o fim da âncora anterior (espera) ainda usa a caixa dela
        self.PALCO_BOX = BOX36.get(aid, (0, 1090, 190))
        return r


_CAIXAS = {"A": (0, 1090, 190), "B": (0, 1920, 190), "B52": (1450, 1920, 190), "C760": (0, 750, 190)}
_LAYOUT = {"H1": "B", "H2": "B", "A1": "B", "B2-1": "B", "B3-1": "B", "B3-3": "B", "B4-1": "B", "B5-1": "B", "B5-2": "B52", "B5-3": "B",
           "B6-2": "B", "B6-3": "C760", "B7": "C760", "B8": "B", "S1": "B", "S2": "B"}          # as outras âncoras: A (o mesmo PALCO do qa36.py)
BOX36 = {aid: _CAIXAS[k] for aid, k in _LAYOUT.items()}


# ── 3D: cena1 (porte do c3d36.html): o produto vetorial em pé ─────────────────────────────────────────────
W1, W2 = (1.5, 1.0, 0.0), (-1.0, 1.5, 0.0)
HZ = W1[0] * W2[1] - W1[1] * W2[0]                      # 3,25 = área do paralelogramo (unidade local = Δ = 0,1)
M_PX, K_TOPO = (330.0, 860.0), 190.0                    # vista de cima: M em (330, 860) px, 190 px por unidade local
CAM_OBL = {"pos": (-7.2, -11.0, 7.4), "tgt": (0.25, 1.25, 1.45), "cx": 640.0, "cy": 560.0, "fov": 22.0}
FOV_MIN = 0.5


def cam_voo(s):
    """s = 0: OrthographicCamera de cima (M em (330, 860), 190 px/unidade, y para cima); s = 1: a oblíqua do c3d36 (k=obl).
    No meio, perspectiva com dolly-zoom: a direção de visada gira (slerp), o alvo anda, a escala no alvo vai de 190 à da oblíqua (geométrica)
    e o fov abre de 0,5° a 22° com a câmera se aproximando. Começo e fim suaves (o s já vem suavizado do Manim)."""
    if s <= 1e-4:
        c = cam_dict((0, 0, 50), (0, 0, 0), (0, 1, 0), M_PX[0], M_PX[1], FOV_MIN)
        c["orto"], c["k"] = True, K_TOPO
        return c
    u = s
    po, to = np.array(CAM_OBL["pos"]), np.array(CAM_OBL["tgt"])
    dob = (to - po) / np.linalg.norm(to - po)
    dt_ = np.array([0.0, 0.0, -1.0])
    om = math.acos(max(-1.0, min(1.0, float(dob @ dt_))))
    d = (math.sin((1 - u) * om) * dt_ + math.sin(u * om) * dob) / math.sin(om)
    tgt = np.zeros(3) + (to - np.zeros(3)) * u
    ko = 540 / (np.linalg.norm(to - po) * math.tan(math.radians(CAM_OBL["fov"] / 2)))
    k = K_TOPO * (ko / K_TOPO) ** u
    fov = FOV_MIN * (CAM_OBL["fov"] / FOV_MIN) ** u
    dist = 540 / (k * math.tan(math.radians(fov / 2)))
    up = (1 - u) * np.array([0.0, 1.0, 0.0]) + u * np.array([0.0, 0.0, 1.0])
    up = up - (up @ d) * d
    up /= np.linalg.norm(up)
    cx = M_PX[0] + (CAM_OBL["cx"] - M_PX[0]) * u
    cy = M_PX[1] + (CAM_OBL["cy"] - M_PX[1]) * u
    if u >= 1 - 1e-6:
        return cam_dict(po, to, (0, 0, 1), CAM_OBL["cx"], CAM_OBL["cy"], CAM_OBL["fov"])
    return cam_dict(tgt - d * dist, tgt, up, cx, cy, fov)


def pontos36(cena, e):
    h = HZ * e.get("sobe", 0.0)
    return {"M": (0, 0, 0), "w1": W1, "w2": W2, "C": (W1[0] + W2[0], W1[1] + W2[1], 0), "topo": (0, 0, h),
            "w1_meio": (W1[0] / 2, W1[1] / 2, 0), "w2_meio": (W2[0] / 2, W2[1] / 2, 0)}


_v.pontos3d = pontos36


class Palco36(Palco3D):
    """Fundo 3D da cena1: o estado traz a câmera (cam_voo(s)), a altura do vetor (sobe) e o raio da grade do chão (rg)."""

    def cam(self):
        return cam_voo(self.tr["s"].get_value())

    def estado(self):
        s = self.tr["s"].get_value()
        e = {"cam": self.cam(), "sobe": round(self.tr["sobe"].get_value(), 4), "rg": round(.0032 + (.010 - .0032) * s, 5), "th": round(s, 4)}
        return e


def anim_cel(cel):
    return [FadeIn(cel.fill), Create(cel.malha), Create(cel.borda)]


def entra_cel(sc, *cels, rt=0.8, extra=()):
    sc.play(*[a for c in cels for a in anim_cel(c)], *extra, run_time=rt)


def larg(m):
    return m.width * 120


def esq(m):
    return pxof(m.get_left())[0]


def dir_(m):
    return pxof(m.get_right())[0]


def centro(m):
    return pxof(m.get_center())


# ── linha que cresce por glyph map (CONTA INTEIRA: cada degrau aparece à direita do anterior, os glifos velhos parados) ─────────
def Lp(pecas, x, y, size=40, al="l", caneta=True):
    m = L(pecas, x, y, size, al, caneta)
    m._pecas, m._xy, m._size = list(pecas), (x, y), size
    return m


def cresce(sc, A, extra, voos=(), rt=0.7, nota="", col=None, mapa=None):
    """A → B = A + extra (peças novas à direita). final K4(c): a parte já escrita NUNCA entra no mapa — ela fica parada; só o trecho novo
    nasce à direita: o que tem fonte voa (voos = [(fonte, chave|índices)] ou função B → lista), o resto pela caneta. No fim, A dá lugar a B
    no mesmo lugar (os glifos de A e de B coincidem)."""
    B = Lp(A._pecas + list(extra), *A._xy, A._size)
    B.shift(A[0][0].get_center() - B[0][0].get_center())
    for k_, (ch, _) in enumerate(A._pecas):                     # cores mudadas à mão em A (ex.: x + y aceso) passam para B
        if ch is not None and ch in A._ix and ch in B._ix:
            for ia, ib in zip(A._ix[ch], B._ix[ch]):
                B[0][ib].set_fill(A[0][ia].get_fill_color())
    for x in B.get_family():
        x._de_linha = True                                          # glifo de uma linha da coluna (o QA de órfão não o conta como solto)
    velhos = [i for ch, _ in A._pecas if ch is not None and ch in B._ix for i in B._ix[ch]]
    desv = 0.0
    for ch, _ in A._pecas:
        if ch is not None and ch in A._ix and ch in B._ix:
            for ia, ib in zip(A._ix[ch], B._ix[ch]):
                desv = max(desv, float(np.linalg.norm(A[0][ia].get_center() - B[0][ib].get_center())) * 120)
    if desv > 1.5:
        print(f"[cresce-desvio] {sc.lote} {sc._aid} {sc.t:.2f} {desv:.1f} px :: {B._tex[:60]!r}")
    novos = [i for i in range(len(B[0])) if i not in velhos]
    vv = voos(B) if callable(voos) else list(voos)
    voados = []
    alvos = []
    for v_ in vv:
        idx = [i for i in sel(B, v_[1]) if i in novos]
        voados += idx
        alvos.append((v_[0], idx, v_[2] if len(v_) > 2 else None))
    resto = [i for i in novos if i not in voados]
    eq = [i for i in resto if i < (min(voados) if voados else 10 ** 9)]      # o que vem antes do primeiro voo ("=") entra antes dele
    depois = [i for i in resto if i not in eq]
    if eq:
        sc.pena(parte(B, eq, "novos"))
    if alvos:
        pares = [(src.copy(), parte(B, idx, "voo"), *([via] if via is not None else [])) for src, idx, via in alvos]
        voos_mod = sys.modules["pecas36"].voos
        voos_mod(sc, pares, rt=max(0.6, rt), seq=True, livre=(A,))      # a linha antiga é a mesma conta (o termo pousa ao lado dela)
    if depois:
        sc.pena(parte(B, depois, "novos"))
    sc.remove(A, *[q for q in getattr(B, "_partes", [])])
    B._esc = True
    sc.add(B)
    import lib36 as _l
    _l.limpa_restos(sc)
    print(f"[gm-cresce] {sc.lote} {sc._aid} {sc.t:.2f} {nota} :: {B._tex[:70]!r}")
    _log_linha(sc, B, "cresce")
    if col is not None and A in col.ls:
        col.ls[col.ls.index(A)] = B
    return B


def eq_x(A, chave):
    """x (px) da borda esquerda do 1º glifo da peça `chave` de A (para alinhar a linha de baixo no =)."""
    return pxof(A[0][A._ix[chave][0]].get_left())[0]


def deriva(sc, A, pecas, pares, col, voos=(), x=None, nota="", rt=1.0, gap=None, size=None, seq=False):
    """v2 §4 (LINHA DERIVADA): a linha B, ABAIXO de A, nasce por TransformByGlyphMap de uma cópia de A (A fica); só os glifos novos
    vêm pela caneta ou pelo voo. x: borda esquerda de B (alinhar no = de A com eq_x). Devolve B (Lp, registrado na coluna)."""
    B = Lp(pecas, 0, 0, size or A._size)
    col.poe(B, x=x, gap=gap)
    B._xy = (esq(B), centro(B)[1])
    vv = voos(B) if callable(voos) else list(voos)
    pp = pares(B) if callable(pares) else list(pares)
    estava = A in sc.mobjects
    passo(sc, A, B, pp, voos=vv, rt=rt, copia=True, nota=nota, seq=seq)
    if estava and A not in sc.mobjects:          # a linha de cima fica (o mapa nasce de uma CÓPIA dela)
        sc.add(A)
    print(f"[deriva] {sc.lote} {sc._aid} {sc.t:.2f} {nota} :: {B._tex[:70]!r}")
    return B


def idx_lims(m, chave):
    """(baixo, cima) de uma peça com ∫ (lims_de) — índices de glifo."""
    return lims_de(m, chave)


def mixLp(texto, pecas, X, Y, S=34, cor=BR):
    """Linha mista Text + fórmula por peças (que pode crescer por glyph map): (T, Lp). Texto em 0,78·S (≥ 26 px), linha de base em Y + 0,27·S."""
    t = T(texto, X, Y + S * .27, max(26, round(S * .78)), "left", cor)
    F = Lp(pecas, dir_(t) + 14, Y, S)
    F._xy = (dir_(t) + 14, Y)
    return t, F


class Coluna36(Coluna):
    """Coluna com respiro de 32 px entre linhas (o padrão de 18 px deixa a conta apertada)."""
    GAP36 = 32

    def y_prox(self, m=None, gap=None):
        return super().y_prox(m, self.GAP36 if gap is None else gap)

    def poe(self, m, x=None, gap=None):
        _pc.COL_BORDA[0], _pc.COL_ATUAL[0] = self.x, self   # v2: o desvio dos voos da coluna passa por fora da margem esquerda dela
        return super().poe(m, x=x, gap=self.GAP36 if gap is None else gap)

    def registra(self, m):
        _pc.COL_BORDA[0], _pc.COL_ATUAL[0] = self.x, self
        return super().registra(m)


# ── log da linha inteira (QA CONTA INTEIRA): cada escrita a caneta e cada glyph map grava o LaTeX completo com o tempo na âncora ─────────────
import pecas36 as _pc
import sys
_passo0 = _pc.passo


def _log_linha(sc, m, como):
    tx = getattr(m, "_tex", None)
    if tx:
        print(f"[linha] {getattr(sc, 'lote', '?')} {getattr(sc, '_aid', '?')} {(sc.nq - getattr(sc, '_q0', 0)) / FPS:6.2f}s {como} {tx!r}")


def passo(sc, A, B, pares, **kw):
    r = _passo0(sc, A, B, pares, **kw)
    _log_linha(sc, B, "gm" if len(pares) > 1 or kw.get("voos") else "voo")
    return r


_pena0 = B36.pena


def _pena_log(self, *ms, **kw):
    r = _pena0(self, *ms, **kw)
    for m in ms:
        _log_linha(self, m, "pena")
    return r


B36.pena = _pena_log


def _com_log_voos():
    """QA da CONTA INTEIRA: a parte que pousa por voo também vai para o log [linha] (como a caneta e o glyph map)."""
    import sys as _s
    v0 = _s.modules["pecas36"].voos

    def _voos_log(sc, pares, *a, **kw):
        r = v0(sc, pares, *a, **kw)
        if len(pares) > 1 and kw.get("seq", True):
            return r                       # v2: os voos em sequência já gravaram o log, um par por vez
        for p_ in pares:
            alvo = p_[1]
            if getattr(alvo, "_tex", None):
                _log_linha(sc, alvo, "voo")
        return r
    for nome in ("pecas36", "p36", "lib36", "v36", "kit"):
        mod = _s.modules.get(nome)
        if mod is not None and getattr(mod, "voos", None) is v0:
            mod.voos = _voos_log
    return _voos_log


voos = _com_log_voos()


# ── QA v2 §7 por quadro (MOLDURA VAZIA e MARGEM) e TAMANHO no log das linhas ─────────────────────────────────────────────
_HDIG = {}


def h_digito(size):
    """Altura (px a 1080p) do dígito em corpo normal numa linha de tamanho `size` (medida no '2' do próprio L)."""
    if size not in _HDIG:
        m = L([("a", "2")], 0, 0, size)
        _HDIG[size] = round(m[0][0].height * 120, 1)
    return _HDIG[size]


_log_linha0 = _log_linha


def _log_linha(sc, m, como):
    _log_linha0(sc, m, como)
    s_ = getattr(m, "_size", None)
    if s_ and getattr(m, "_tex", None):
        print(f"[tam] {getattr(sc, 'lote', '?')} {getattr(sc, '_aid', '?')} {(sc.nq - getattr(sc, '_q0', 0)) / FPS:6.2f}s size={s_} "
              f"dig={h_digito(s_)} x={esq(m):.0f} {m._tex[:60]!r}")


def _leaf_vis(x):
    if not isinstance(x, VMobject) or len(x.points) == 0:
        return False
    return max(x.get_fill_opacity(), x.get_stroke_opacity() if x.get_stroke_width() > 0.3 else 0.0) > 0.15


def _qa_quadro(sc):
    fx = set()
    for f_ in sc.fixos():
        if f_ is not None:
            fx |= {id(y) for y in f_.get_family()}
    caixas, folhas = [], []
    for top in sc.mobjects:
        if id(top) in fx or isinstance(top, (ValueTracker, ImageMobject)):
            continue
        for x in top.get_family():
            if id(x) in fx or getattr(x, "_sem_foco", False) or (x.z_index or 0) <= -10 or not _leaf_vis(x):
                continue
            x0, y0 = pxof(x.get_corner(UL))
            x1, y1 = pxof(x.get_corner(DR))
            if isinstance(x, RoundedRectangle) and (x1 - x0) < 1800:
                caixas.append((x, (x0, y0, x1, y1)))
            else:
                folhas.append((x, (x0, y0, x1, y1)))
    t = sc.t
    # MARGEM: nada a menos de 48 px da borda (fora o canto, o logo e o papel)
    vist = getattr(sc, "_mg_vist", set())
    for x, (x0, y0, x1, y1) in folhas + caixas:
        if (x0 < 48 or y0 < 48 or x1 > 1872 or y1 > 1032) and id(x) not in vist and not getattr(x, "_sem_margem", False):
            vist.add(id(x))
            nome = getattr(x, "_txt", None) or getattr(x, "_tex", None) or (type(x).__name__ + " " + ManimColor(x.get_stroke_color()).to_hex())
            print(f"[MARGEM] {sc._aid} {t:7.2f}s {str(nome)[:50]!r} caixa=({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
    sc._mg_vist = vist
    # MOLDURA VAZIA: RoundedRectangle (moldura, painel, caixa, selo) sem nenhum objeto visível dentro por mais de 0,5 s
    ini, rep = getattr(sc, "_mv_ini", {}), getattr(sc, "_mv_rep", set())
    vivos = set()
    for r_, (x0, y0, x1, y1) in caixas:
        dentro = False
        for x, (a0, b0, a1, b1) in folhas:
            cx, cy = (a0 + a1) / 2, (b0 + b1) / 2
            if x0 + 4 < cx < x1 - 4 and y0 + 4 < cy < y1 - 4:
                dentro = True
                break
        if dentro:
            ini.pop(id(r_), None)
            continue
        vivos.add(id(r_))
        t0 = ini.setdefault(id(r_), t)
        if t - t0 > 0.1 and id(r_) not in rep:                  # final K2: limite de 0,1 s
            rep.add(id(r_))
            print(f"[MV] {sc._aid} {t0:7.2f}s moldura vazia > 0,1 s caixa=({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
    for k in list(ini):
        if k not in vivos:
            ini.pop(k)
    sc._mv_ini, sc._mv_rep = ini, rep
    _qa_glifos(sc, fx)


_GLIFO = ("VMobjectFromSVGPath", "SVGPathMobject")


def _qa_glifos(sc, fx):
    """final §7: DUPLICADOS (K3), CONTORNO depois do pouso (K3), ÓRFÃOS (K5) e LEGIBILIDADE (K4/K10/K12), em todo quadro."""
    t = sc.t
    gls = []                     # (glifo, caixa px, dono top, nº de pontos)
    orf = []
    dentro_de = set()            # glifos que também pertencem a outro objeto da cena (referência dupla, não estão soltos)
    for top in sc.mobjects:
        if type(top).__name__ not in _GLIFO:
            dentro_de |= {id(y) for y in top.get_family()[1:]}
    for top in sc.mobjects:
        if id(top) in fx or isinstance(top, (ValueTracker, ImageMobject)):
            continue
        fam = [x for x in top.get_family() if type(x).__name__ in _GLIFO and len(x.points) and x.get_fill_opacity() > 0.15
               and not getattr(x, "_sem_foco", False)]
        if not fam:
            continue
        escr = any(getattr(y, "_em_caneta", False) or getattr(y, "_voando", False) for y in top.get_family())
        for x in fam:
            x0, y0 = pxof(x.get_corner(UL))
            x1, y1 = pxof(x.get_corner(DR))
            gls.append((x, (x0, y0, x1, y1), id(top), len(x.points)))
            if escr:
                x._qa_escr = t
        # órfão: objeto de topo pequeno, só de glifos, sem nome de texto (resto solto de mapa/voo)
        ev_ = getattr(sc, "_em_voo", set())
        if id(top) not in dentro_de and not getattr(top, "_de_linha", False) and getattr(top, "_tex", None) is None and getattr(top, "_txt", None) is None and getattr(top, "_pai", None) is None \
                and all(type(y).__name__ in _GLIFO or not len(y.points) for y in top.get_family()) \
                and not any(id(y) in ev_ or getattr(y, "_voando", False) for y in top.get_family()):
            X0, Y0 = pxof(top.get_corner(UL))
            X1, Y1 = pxof(top.get_corner(DR))
            if X1 - X0 < 40 and Y1 - Y0 < 40:
                orf.append((top, (X0, Y0, X1, Y1)))
    # DUPLICADOS: mesma forma (nº de pontos, tamanho ± 10 %) e centros a menos de 1/3 do tamanho
    dup_now = set()
    info = {}
    tops = {id(m): m for m in sc.mobjects}
    cel = {}
    for k, (x, b, own, n) in enumerate(gls):
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        cel.setdefault((n, int(cx // 40), int(cy // 40)), []).append(k)
    for k, (x, b, own, n) in enumerate(gls):
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        w, h = b[2] - b[0], b[3] - b[1]
        tam = max(w, h, 1)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in cel.get((n, int(cx // 40) + dx, int(cy // 40) + dy), []):
                    if j <= k:
                        continue
                    y_, c, own2, _ = gls[j]
                    if own2 == own:
                        continue                                        # o mesmo texto ("III", "ll"): não é cópia
                    w2, h2 = c[2] - c[0], c[3] - c[1]
                    if abs(w2 - w) > .1 * max(w, 1) or abs(h2 - h) > .1 * max(h, 1):
                        continue
                    dd_ = np.hypot((c[0] + c[2]) / 2 - cx, (c[1] + c[3]) / 2 - cy)
                    if 1.5 <= dd_ < tam / 3:                            # < 1,5 px: a cópia exatamente sobre a fonte (fade no lugar) não se vê
                        dup_now.add((id(x), id(y_)))
                        info[(id(x), id(y_))] = (b, own, own2)
    cont = getattr(sc, "_dup_n", {})
    rep = getattr(sc, "_dup_rep", set())
    novo = {}
    ev_ = getattr(sc, "_em_voo", set())
    for kk in dup_now:
        novo[kk] = cont.get(kk, 0) + 1
        bx_, o1_, o2_ = info[kk]
        voo_ = (kk[0] in ev_ or kk[1] in ev_ or type(tops.get(o1_)).__name__ in ("Group", "Mobject")
                or type(tops.get(o2_)).__name__ in ("Group", "Mobject", "VGroup"))
        lim_ = 5 if voo_ else 3                                      # handoff K3: num voo, os 2 primeiros quadros ficam de fora; depois > 2 seguidos
        if novo[kk] == lim_ and kk not in rep:
            rep.add(kk)
            bx, o1, o2 = info[kk]
            nm = lambda o: str(getattr(tops.get(o), "_tex", None) or getattr(tops.get(o), "_txt", None) or type(tops.get(o)).__name__)[:40]
            print(f"[DUP] {sc._aid} {t:7.2f}s dois glifos iguais um sobre o outro por > 2 quadros caixa=({bx[0]:.0f},{bx[1]:.0f}) {nm(o1)!r} × {nm(o2)!r}")
    sc._dup_n, sc._dup_rep = novo, rep
    # CONTORNO: glifo parado (nem escrevendo, nem voando) com contorno > 0,5 px
    wlim = W(0.5)
    crep = getattr(sc, "_cont_rep", set())
    ccnt = getattr(sc, "_cont_n", {})
    cnovo = {}
    for x, b, own, n in gls:
        if x.get_stroke_width() > wlim and x.get_stroke_opacity() > 0.15 and not getattr(x, "_em_caneta", False) and not getattr(x, "_voando", False)                 and t - getattr(x, "_qa_escr", -9) > 0.2:
            cnovo[id(x)] = ccnt.get(id(x), 0) + 1
            if cnovo[id(x)] == 3 and id(x) not in crep:
                crep.add(id(x))
                print(f"[CONTORNO] {sc._aid} {t:7.2f}s glifo parado com contorno {x.get_stroke_width():.2f} (> 0,5 px) caixa=({b[0]:.0f},{b[1]:.0f},{b[2]:.0f},{b[3]:.0f})")
    sc._cont_n, sc._cont_rep = cnovo, crep
    # ÓRFÃOS: > 0,3 s
    oini = getattr(sc, "_orf_ini", {})
    orep = getattr(sc, "_orf_rep", set())
    vivos = set()
    for top, b in orf:
        vivos.add(id(top))
        t0 = oini.setdefault(id(top), t)
        if t - t0 > 0.3 and id(top) not in orep:
            orep.add(id(top))
            print(f"[ORFAO] {sc._aid} {t0:7.2f}s objeto solto {type(top).__name__} caixa=({b[0]:.0f},{b[1]:.0f},{b[2]:.0f},{b[3]:.0f})")
            import os as _os
            if _os.environ.get("DEBUG_ORF"):
                import traceback as _tb
                print("[ORFAO-dbg]", sorted(k for k in vars(top) if k.startswith("_") and not k.startswith("__"))[:30],
                      "idx_em_mobjects", sc.mobjects.index(top), "n_mob", len(sc.mobjects), "op", top.get_fill_opacity())
    sc._orf_ini = {k: v for k, v in oini.items() if k in vivos}
    sc._orf_rep = orep
    # LEGIBILIDADE: glifos de textos diferentes (forma diferente) sobrepostos em > 30 % da menor caixa por > 0,3 s
    leg_now = set()
    cel2 = {}
    for k, (x, b, own, n) in enumerate(gls):
        for gx in range(int(b[0] // 60), int(b[2] // 60) + 1):
            for gy in range(int(b[1] // 60), int(b[3] // 60) + 1):
                cel2.setdefault((gx, gy), []).append(k)
    vistos = set()
    for lst in cel2.values():
        for a_ in range(len(lst)):
            for b_ in range(a_ + 1, len(lst)):
                i, j = lst[a_], lst[b_]
                if (i, j) in vistos:
                    continue
                vistos.add((i, j))
                xi, bi, oi, ni = gls[i]
                xj, bj, oj, nj = gls[j]
                if oi == oj:
                    continue
                ox = min(bi[2], bj[2]) - max(bi[0], bj[0])
                oy = min(bi[3], bj[3]) - max(bi[1], bj[1])
                if ox <= 0 or oy <= 0:
                    continue
                amin = min((bi[2] - bi[0]) * (bi[3] - bi[1]), (bj[2] - bj[0]) * (bj[3] - bj[1]))
                if amin <= 4 or ox * oy < .3 * amin:
                    continue
                if ni == nj and abs((bi[2] - bi[0]) - (bj[2] - bj[0])) <= .1 * max(bi[2] - bi[0], 1):
                    continue                                           # o mesmo glifo (voo/cópia): é o DUPLICADOS
                leg_now.add((id(xi), id(xj)))
    lini = getattr(sc, "_leg_ini", {})
    lrep = getattr(sc, "_leg_rep", set())
    lnovo = {}
    for kk in leg_now:
        lnovo[kk] = lini.get(kk, t)
        if t - lnovo[kk] > 0.3 and kk not in lrep:
            lrep.add(kk)
            print(f"[LEG] {sc._aid} {lnovo[kk]:7.2f}s glifos de textos diferentes sobrepostos > 30 % por > 0,3 s")
    sc._leg_ini, sc._leg_rep = lnovo, lrep


_utt_r5 = _pc.B34.update_to_time


def _utt_qa(self, t):
    _utt_r5(self, t)
    if hasattr(self, "clk") and not getattr(self, "_sem_r5", False):
        c = self.clk.get_value()
        if c >= getattr(self, "_prox_qa", 0.0) - 1e-6:
            self._prox_qa = round(c * FPS + 1) / FPS
            _qa_quadro(self)


_pc.B34.update_to_time = _utt_qa


# ── final §6 (porte do yt_0034): PRESSA, duas passadas para a cena seguir a voz real ─────────────────────────────────────────────
# Passada 1 (PRESSA=grava, --dry_run): cada trecho entre dois gatilhos (gat, an, fim) anota o tempo de animação e o atraso com que chegou ao
# gatilho do fim. Fator do trecho = (tempo − atraso que o próprio trecho criou − 0,1 s) ÷ tempo, com piso 0,4.
# Passadas seguintes (PRESSA=usa, o padrão): os plays e as esperas do trecho andam com esse fator. A voz nunca muda; só a construção encurta.
import os
import json as _json
import kit as _kit
from pathlib import Path as _Path
PRESSA = os.environ.get("PRESSA", "usa")
_DIRPR = _Path(__file__).resolve().parent / "renders" / "pressa"
_play_pr0, _wait_pr0, _gat_pr0, _an_pr0, _fim_pr0 = J36.play, J36.wait, J36.gat, J36.an, J36.fim


def _pr(self):
    if not hasattr(self, "_prs"):
        self._prs, self._seg, self._em_gat = {}, 0, False
        arq = _DIRPR / f"{self.lote}.json"
        self._fat = {} if PRESSA != "usa" or not arq.exists() else {int(k): v for k, v in _json.loads(arq.read_text(encoding="utf-8"))["fator"].items()}
    return self._prs


def _play_pr(self, *anims, run_time=None, **kw):
    from manim.animation.animation import prepare_animation
    S = _pr(self)
    anims = [prepare_animation(a) for a in anims]
    rt = run_time if run_time is not None else max([a.run_time for a in anims] or [1.0])
    f = self._fat.get(self._seg, 1.0)
    if f < 0.999 and not self._em_gat:
        for a in anims:
            a.run_time *= f
        rt *= f
        run_time = rt if run_time is not None else None
    S.setdefault(self._seg, {"rt": 0.0, "late": 0.0, "nome": ""})["rt"] += rt
    return _play_pr0(self, *anims, run_time=run_time, **kw)


def _wait_pr(self, duration=1.0, *a, **k):
    S = _pr(self)
    if not self._em_gat and not getattr(self, "_hold", False) and duration > 0.2:      # os holds de leitura (K9, K10) não encurtam
        f = self._fat.get(self._seg, 1.0)
        duration *= f
        S.setdefault(self._seg, {"rt": 0.0, "late": 0.0, "nome": ""})["rt"] += duration
        if duration < 1 / _kit.FPS:
            return
    return _wait_pr0(self, duration, *a, **k)


def _fecha_seg(self, late, nome):
    S = _pr(self)
    S.setdefault(self._seg, {"rt": 0.0, "late": 0.0, "nome": ""}).update(late=round(late, 3), nome=nome)
    self._seg += 1


def _gat_pr(self, frase):
    _pr(self)
    k = self._k_frase(self._aid, frase)
    if k is not None:
        alvo = self._q0 + max(0.0, _kit.ANC[self._aid]["t"][k] - _kit.LEAD) * _kit.FPS
        _fecha_seg(self, (self.nq - alvo) / _kit.FPS, f"{self._aid}: {frase}")
    self._em_gat = True
    try:
        return _gat_pr0(self, frase)
    finally:
        self._em_gat = False


def _an_pr(self, aid):
    _pr(self)
    if self._off is not None:
        _fecha_seg(self, (self.nq - (round(_kit.ANC[aid]["ini"] * _kit.FPS) - self._off)) / _kit.FPS, f"início de {aid}")
    self._em_gat = True
    try:
        return _an_pr0(self, aid)
    finally:
        self._em_gat = False


def _fim_pr(self):
    S = _pr(self)
    _fecha_seg(self, (self.nq - self.alvo) / _kit.FPS, "fim do lote")
    self._em_gat = True
    if PRESSA == "grava":
        fat, ant = {}, 0.0
        for s in sorted(S):
            d = S[s]
            need = d["late"] - max(0.0, ant)
            if need > 0.05 and d["rt"] > 0.2 and not (self.lote == "PS" and d["nome"] == "fim do lote"):
                fat[s] = round(max(0.4, (d["rt"] - need - 0.1) / d["rt"]), 3)
            ant = d["late"]
        _DIRPR.mkdir(parents=True, exist_ok=True)
        (_DIRPR / f"{self.lote}.json").write_text(_json.dumps({"fator": fat, "trechos": S}, ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"[pressa] {self.lote}: {len(fat)} trechos encurtados; menor fator {min(fat.values()) if fat else 1:.2f}")
    return _fim_pr0(self)


J36.play, J36.wait, J36.gat, J36.an, J36.fim = _play_pr, _wait_pr, _gat_pr, _an_pr, _fim_pr
