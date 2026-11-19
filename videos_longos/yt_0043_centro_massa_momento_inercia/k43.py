"""yt_0043 · CÁLCULO III · EP. 18 (provisório) · Centro de massa e momento de inércia na integral tripla — camada da unidade sobre o v41.py (base yt_0041).

- Macros do preâmbulo = as de referencia/yt_0043_quadros_alvo_v1/head43.js.
- Câmeras e pontos 3D = os de c3d43.html e keys43.js.
- Papel de borda a borda (passo 60 px) em 100% das cenas (2D e 3D), exceto no CTA final (G1).
- Escrita: caneta glifo a glifo (pena), voos (TransformFromCopy em arco), glyph maps (TransformByGlyphMap com mapa explícito).
- QA por quadro (a cada 0,2 s): [R5], [R5V], [R6], [vazio], [grade], [3dcanto], [orfa], e logs [gm], [degrau], [voo], [pena], [coluna], [marca], [tam]."""
import v41 as _v41
from v41 import *  # noqa: F401,F403
from v41 import _Caneta  # noqa: F401
from MF_Tools import TransformByGlyphMap

# Acrescentar símbolos Unicode que aparecem em legendas/textos de keys43.js ao parser ESPECIAIS do v41
_NOVOS_ESP = [
    ("x̄", r"\bar{x}"), ("ȳ", r"\bar{y}"), ("z̄", r"\bar{z}"),
    ("Iₙ", r"I_n"), ("secⁿ", r"\sec^n"), ("∫", r"\int"),
]
for _par in _NOVOS_ESP:
    if _par not in _v41.ESPECIAIS:
        _v41.ESPECIAIS.insert(0, _par)
_v41._RX = re.compile("(" + "|".join(re.escape(a) for a, _ in _v41.ESPECIAIS) + ")")

# ── paleta e macros desta unidade (handoff §4.2, head43.js) ──────────────────────────────────────────────────
RO, FI, TH, SOMB, LI, EZ, UU = "#FF9440", "#B48CFF", "#2EE6A6", "#FFC08A", "#C6F26B", "#5AA2FF", "#E08A3C"
TRC = "#6C7698"

TEX31.add_to_preamble(
    r"\definecolor{ro}{HTML}{FF9440}\definecolor{fi}{HTML}{B48CFF}\definecolor{th}{HTML}{2EE6A6}\definecolor{so}{HTML}{FFC08A}"
    r"\definecolor{lim}{HTML}{C6F26B}\definecolor{ez}{HTML}{5AA2FF}\definecolor{uu}{HTML}{E08A3C}"
    r"\def\Z{\textcolor{ez}{z}}\def\dZ{\textcolor{ez}{dz}}\def\DZ{\textcolor{ez}{\Delta z}}"
    r"\def\S{\textcolor{so}{s}}\def\Rs{\textcolor{so}{s}}\def\dS{\textcolor{so}{ds}}\def\DS{\textcolor{so}{\Delta s}}"
    r"\def\T{\textcolor{th}{\theta}}\def\dT{\textcolor{th}{d\theta}}\def\DT{\textcolor{th}{\Delta\theta}}"
    r"\def\R{\textcolor{ro}{r}}\def\dR{\textcolor{ro}{dr}}\def\DR{\textcolor{ro}{\Delta r}}"
    r"\def\F{\textcolor{fi}{\varphi}}\def\dF{\textcolor{fi}{d\varphi}}\def\DF{\textcolor{fi}{\Delta\varphi}}"
    r"\def\J{\textcolor{lim}{r^2\operatorname{sen}\varphi}}\def\Jr{\textcolor{lim}{r^2\operatorname{sen}\varphi}}"
    r"\def\Js{\textcolor{lim}{s}}\def\Li#1{\textcolor{lim}{#1}}\def\de{\textcolor{ci}{\rho}}\def\dV{dV}"
    r"\def\Ro#1{\textcolor{ro}{#1}}\def\Fi#1{\textcolor{fi}{#1}}\def\Th#1{\textcolor{th}{#1}}\def\So#1{\textcolor{so}{#1}}"
    r"\def\Ez#1{\textcolor{ez}{#1}}\def\Uu#1{\textcolor{uu}{#1}}"
    r"\def\uu{\textcolor{uu}{u}}\def\du{\textcolor{uu}{du}}"
    r"\def\ww{\textcolor{uu}{w}}\def\dw{\textcolor{uu}{dw}}"
    r"\def\Tt{\textcolor{uu}{t}}\def\dTt{\textcolor{uu}{dt}}\def\tg{\operatorname{tg}}"
    r"\def\xb{\bar{\textcolor{ca}{x}}}\def\yb{\bar{\textcolor{cm}{y}}}\def\zb{\bar{\textcolor{ez}{z}}}"
    r"\def\dm{\textcolor{ci}{dm}}\def\Sg{\textcolor{so}{s_G}}"
    r"\def\Mxy{M_{\textcolor{ca}{x}\textcolor{cm}{y}}}\def\Myz{M_{\textcolor{cm}{y}\textcolor{ez}{z}}}\def\Mxz{M_{\textcolor{ca}{x}\textcolor{ez}{z}}}"
)

from pathlib import Path as _Path
AQUI_RENDERS = _Path(__file__).resolve().parent / "renders"

# ── câmeras e pontos do c3d43.html / keys43.js (§4.3) ────────────────────────────────────────────────────────
CAMLATA_V = ((9.2, -6.2, 5.8), (0, 0, .45), 600, 560, 1.4)
VER = {
    "lataGiro": CAMLATA_V,
    "lataPesada": CAMLATA_V,
    "lataDuas": CAMLATA_V,
    "cmPontos": ((9.0, -6.4, 5.2), (1.1, 1.1, .6), 560, 600, 1.3),
    "lataCel": CAMLATA_V,
    "lataPlano": CAMLATA_V,
    "lataSim": ((7.6, -5.0, 8.6), (0, 0, .4), 600, 560, 1.4),
    "lataSim2": ((7.6, -5.0, 8.6), (0, 0, .4), 600, 560, 1.4),
    "taca": CAMLATA_V,
    "giroCel": CAMLATA_V,
    "distEixo": ((9.0, -6.4, 5.2), (.9, .9, .6), 560, 600, 1.3),
    "cilindroH": ((9.2, -6.2, 5.0), (0, 0, .65), 600, 560, 1.4),
    "esferaOct": ((9.2, -6.2, 5.0), (0, 0, .3), 600, 560, 1.4),
    "lataParede": CAMLATA_V,
}

OL = {"dx": -100.0, "dy": 80.0, "esc": 0.94}
OC = {"dx": -120.0, "dy": 150.0, "esc": 0.72}

ENQ = {
    "h1": ("lataGiro", -100, 80, .94),
    "h2": ("lataDuas", -100, 80, .94),
    "b11a": ("cmPontos", -60, 30, 1.0),
    "b11b": ("lataCel", -100, 80, .94),
    "b12": ("lataPlano", -100, 80, .94),
    "b13a": ("lataSim", -110, 40, 1.0),
    "b13b": ("lataSim2", -110, 40, 1.0),
    "b21": ("taca", -100, 80, .94),
    "b22": ("taca", -100, 80, .94),
    "b31": ("giroCel", -100, 80, .94),
    "b32": ("distEixo", -40, 20, 1.0),
    "b33": ("cilindroH", -40, 110, .82),
    "b34a": ("esferaOct", -40, 100, .86),
    "b34b": ("esferaOct", -40, 100, .86),
    "b41": ("lataPesada", -20, 190, .60),
    "b42": ("lataPesada", -20, 190, .60),
    "b43": ("lataPesada", -20, 190, .60),
    "s2": ("lataParede", -100, 80, .94),
}


def cam43(cena, dx=0.0, dy=0.0, esc=1.0):
    p, t, cx, cy, DF = VER[cena]
    p, t = np.array(p, float), np.array(t, float)
    pos = t + (p - t) * DF
    fov = 2 * math.degrees(math.atan(math.tan(math.radians(11.0)) / esc))
    return cam_dict(pos, t, (0, 0, 1), dx + esc * cx, dy + esc * cy, fov)


def cam_alvo(k):
    c, dx, dy, esc = ENQ[k]
    return cam43(c, dx, dy, esc)


def gira_cam(c, graus):
    if abs(graus) < 1e-9:
        return c
    a = math.radians(graus)
    t = np.array(c["tgt"])
    d = np.array(c["pos"]) - t
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    c2 = dict(c)
    c2["pos"] = [float(x) for x in t + R @ d]
    return c2


def _cyl(s, t, z):
    return np.array([s * math.cos(t), s * math.sin(t), z], float)


def _sph(r, f, t):
    return np.array([r * math.sin(f) * math.cos(t), r * math.sin(f) * math.sin(t), r * math.cos(f)], float)


def _pontos43():
    P = {}
    # lataGiro / lataPesada (SC = 2.2)
    SC = 2.2
    Wp = lambda X, Y, Z: SC * np.array([X, Y, Z], float)
    WC = lambda s, t, z: Wp(s * math.cos(t), s * math.sin(t), z)
    rr, zz = 0.32, 1.32
    P["lataGiro"] = {
        "quina": WC(1, 0, 1), "fundo": Wp(.08, 0, .08), "O": (0, 0, 0),
        "meio": Wp(0, 0, .5), "zbar": Wp(0, 0, .5549), "ez": Wp(0, 0, 1.45 + .12),
        "ex": Wp(1.68, 0, 0), "ey": Wp(0, 1.68, 0),
        "giro": Wp(rr, 0, zz), "omega": Wp(rr * math.cos(-PI * .35), rr * math.sin(-PI * .35), zz),
    }
    P["lataPesada"] = dict(P["lataGiro"])

    # lataDuas (SC = 2.2)
    a1, a2 = -PI * .30, -PI * .30 + PI / 8
    b1, b2 = -PI * .12, -PI * .12 + PI / 10
    P["lataDuas"] = {
        "ez": Wp(0, 0, 1.45 + .12),
        "c1": WC(.32, a1, .14), "c2": WC(1.02, (b1 + b2) / 2, .9),
        "f1": WC(.06, (a1 + a2) / 2, .18), "f2": WC(.4, (b1 + b2) / 2, .9),
    }

    # cmPontos (SC = 1.2)
    SC = 1.2
    Wp = lambda X, Y, Z: SC * np.array([X, Y, Z], float)
    B = [([2.4, 2.0, .4], 1), ([2.3, .4, 1.1], 3), ([.4, 2.4, 1.8], 2)]
    mt = sum(m for _, m in B)
    cm = [sum(m * p[i] for p, m in B) / mt for i in range(3)]
    P["cmPontos"] = {
        "ex": (SC * 2.4 + .16, 0, 0), "ey": (0, SC * 2.4 + .16, 0), "ez": (0, 0, SC * 1.9 + .16),
        "m1": Wp(*B[0][0]), "m2": Wp(*B[1][0]), "m3": Wp(*B[2][0]),
        "cm": Wp(*cm), "cmChao": Wp(cm[0], cm[1], 0),
    }

    # lataCel (SC = 2.2)
    SC = 2.2
    Wp = lambda X, Y, Z: SC * np.array([X, Y, Z], float)
    WC = lambda s, t, z: Wp(s * math.cos(t), s * math.sin(t), z)
    t1, t2, s1, s2, z1, z2 = -PI * .30, -PI * .30 + PI / 10, .62, .82, .55, .75
    tm, sm_ = (t1 + t2) / 2, (s1 + s2) / 2
    P0 = _cyl(sm_, tm, 0)
    P["lataCel"] = {
        "ez": Wp(0, 0, 1.45 + .12), "ex": Wp(1.68, 0, 0), "ey": Wp(0, 1.68, 0),
        "cel": WC(s2 + .06, tm, (z1 + z2) / 2),
        "px": Wp(P0[0] / 2, 0, 0), "py": Wp(P0[0], P0[1] / 2, 0), "pz": Wp(P0[0], P0[1], z1 / 2),
    }

    # lataPlano (SC = 2.2)
    zb, L_ = .555, .85
    a1, a2 = -PI * .32, -PI * .32 + PI / 10
    b1, b2 = -PI * .10, -PI * .10 + PI / 10
    P["lataPlano"] = {
        "ez": Wp(0, 0, 1.45 + .12),
        "cA": WC(.92, (a1 + a2) / 2, .9), "cB": WC(.67, (b1 + b2) / 2, .17),
        "fA": WC(.8, (a1 + a2) / 2, (.82 + zb) / 2), "fB": WC(.55, (b1 + b2) / 2, (.25 + zb) / 2),
        "plano": Wp(L_, -L_ * .2, zb), "zbar": Wp(0, 0, zb), "ponta": Wp(L_, L_, zb),
    }

    # lataSim / lataSim2 (SC = 2.2)
    t0, d, s1, s2 = -PI * .18, PI / 10, .6, .8
    P["lataSim"] = {
        "ez": Wp(0, 0, 1.45 + .12), "ex": Wp(1.68, 0, 0), "ey": Wp(0, 1.68, 0),
        "cA": WC(s2 + .08, t0 + d / 2, .5), "cB": WC(s2 + .08, t0 + PI + d / 2, .5),
    }
    P["lataSim2"] = dict(P["lataSim"])

    # taca (SC = 2.2)
    ss, tt = .6, -.04
    P["taca"] = {
        "ez": Wp(0, 0, 1.45 + .12),
        "entra": WC(ss, tt, ss * ss), "sai": WC(ss, tt, 1),
        "z23": Wp(0, 0, 2 / 3), "z12": Wp(0, 0, .5),
        "borda": WC(1, PI * .75, 1), "fundoT": Wp(0, 0, 0),
    }

    # giroCel (SC = 2.2)
    t1, t2 = -PI * .05, -PI * .05 + PI / 10
    tm = (t1 + t2) / 2
    P0 = WC(1.0, tm, .55)
    tg = np.array([-math.sin(tm), math.cos(tm), 0.0])
    P["giroCel"] = {
        "ez": Wp(0, 0, 1.45 + .12),
        "giro": Wp(.32, 0, 1.38),
        "omega": Wp(.32 * math.cos(-PI * .35), .32 * math.sin(-PI * .35), 1.38),
        "cel": WC(1.04, tm, .62), "fio": WC(.45, tm, .55),
        "v": P0 + tg * .95,
    }

    # distEixo (SC = 1.3)
    SC = 1.3
    Wp = lambda X, Y, Z: SC * np.array([X, Y, Z], float)
    P["distEixo"] = {
        "ex": (SC * 2.3 + .16, 0, 0), "ey": (0, SC * 2.3 + .16, 0), "ez": (0, 0, SC * 1.9 + .16),
        "P": Wp(1, 1.2, 1), "s": Wp(.5, .6, 1), "fx": Wp(1, .6, .5), "r": Wp(.5, .6, .5), "pe": Wp(0, 0, 1),
    }

    # cilindroH (SC = 1.9)
    SC = 1.9
    Wp = lambda X, Y, Z: SC * np.array([X, Y, Z], float)
    WC = lambda s, t, z: Wp(s * math.cos(t), s * math.sin(t), z)
    Hh, sc = 1.4, .55
    P["cilindroH"] = {
        "ez": Wp(0, 0, Hh + .35 + .12),
        "s": WC(sc * .55, -PI * .30, Hh), "R": WC(.7, PI * .08, Hh), "h": WC(1, -PI * .47, Hh / 2),
    }

    # esferaOct (SC = 1.9)
    rr, ff = .85, PI * .31
    Pp = [rr * math.sin(ff), 0, rr * math.cos(ff)]
    P["esferaOct"] = {
        "ez": Wp(0, 0, 1.45 + .12),
        "P": Wp(*Pp), "r": Wp(Pp[0] * .55, 0, Pp[2] * .55),
        "phi": Wp(.30 * math.sin(ff / 2), 0, .30 * math.cos(ff / 2)),
        "s": Wp(Pp[0] / 2, 0, Pp[2]), "R": Wp(.72, -.72, 0),
    }

    # lataParede (SC = 2.2)
    SC = 2.2
    Wp = lambda X, Y, Z: SC * np.array([X, Y, Z], float)
    P["lataParede"] = {
        "giro": Wp(1 + .30, 0, 1.38),
        "omega": Wp(1 + .30 * math.cos(-PI * .35), .30 * math.sin(-PI * .35), 1.38),
        "reta": Wp(1, 0, 1.65), "ez0": Wp(0, 0, 1.5),
    }

    for c in P:
        top = P[c].get("ez", P[c].get("ez0"))
        if top is not None:
            P[c]["eixoTopo"] = top
            P[c]["eixoBase"] = np.array([0.0, 0.0, 0.0])
    return {c: {k: np.array(v, float) for k, v in d.items()} for c, d in P.items()}


P43 = _pontos43()


class Palco43(Palco3D):
    """Palco3D do kit (estado por quadro → pedidos3d → PNG do c43.js) + `giro` (graus) da câmera em volta do eixo z."""

    def __init__(self, sc, cena, cam, giro=0.0, obst=(), **ini):
        self._giro0 = giro
        super().__init__(sc, cena, cam, **ini)
        if not self.fundo.dir.exists():
            alt = DIR3D / "q3d" / f"{sc.lote}_960x540" / cena
            if alt.exists():
                self.fundo.dir = alt
                self.fundo.f = -1
                self.fundo._quadro()
        self.tr["giro"] = ValueTracker(float(giro))
        sc.add(self.tr["giro"])
        self.obst = list(obst)
        sc._palcos.append(self)

    def cam(self):
        c = super().cam()
        g = self.tr["giro"].get_value() if "giro" in self.tr else self._giro0
        return gira_cam(c, g)

    def estado(self):
        e = super().estado()
        e.pop("giro", None)
        return e

    def pt(self, nome):
        return proj3d(self.cam(), P43[self.cena][nome])

    def ptm(self, nome, dx=0.0, dy=0.0):
        x, y = self.pt(nome)
        return PX(x + dx, y + dy)


# ── texto, peças e elementos visuais ─────────────────────────────────────────────────────────────────────────
GM_LOG = []
_NG = {}


def ng(tex):
    if tex not in _NG:
        _NG[tex] = len(MathTex(r"\textstyle " + tex.replace(r"\sum", r"\sum\nolimits"), font_size=30, tex_template=TEX31)[0]) if tex.strip() else 0
    return _NG[tex]


def L(pecas, x, y, size=40, al="l", caneta=True):
    pecas = [p if isinstance(p, tuple) else (None, p) for p in pecas]
    m = TC(" ".join(t for _, t in pecas), x, y, size, al, caneta)
    ix, k = {}, 0
    for ch, t in pecas:
        n = ng(t)
        if ch is not None:
            ix.setdefault(ch, []).extend(range(k, k + n))
        k += n
    if k != len(m[0]):
        print(f"[pecas] AVISO {k} glifos nas peças × {len(m[0])} na fórmula: {m._tex!r}")
    m._ix = ix
    return m


def sel(m, a):
    if isinstance(a, str):
        return list(m._ix[a])
    out = []
    for x in a:
        out += [x] if isinstance(x, (int, np.integer)) else list(m._ix[x])
    return out


def gl(m, *chaves):
    out = []
    for c in chaves:
        out += sel(m, c) if not isinstance(c, (int, np.integer)) else [c]
    return VGroup(*[m[0][i] for i in out])


def mixl(partes, X, Y, S=36):
    g, cx, ps = VGroup(), X, []
    for p in partes:
        if p[0] == "m":
            m = TC(p[1], cx, Y, S, "l")
        elif p[0] == "L":
            m = L(p[1], cx, Y, S, "l")
        else:
            m = T(p[1], cx, Y + S * .27, max(26, round(S * .78)), "left", p[2] if len(p) > 2 else BR)
        cx = pxof(m.get_right())[0] + 14
        g.add(m)
        ps.append(m)
    g.p = ps
    g._tex = "mixl: " + " | ".join(str(p[1])[:24] for p in partes)
    return g


def moldura(X0, Y0, w, h, cor=GEO, alpha=0.5, wpx=2, raio=10, fill=None, fop=0.0):
    r = RoundedRectangle(width=w / 120, height=h / 120, corner_radius=raio / 120).move_to(PX(X0 + w / 2, Y0 + h / 2))
    r.set_fill(fill or BG_, fop).set_stroke(cor, W(wpx), alpha)
    r._painel = (X0, Y0, X0 + w, Y0 + h)
    return sem_ctn(r).set_z_index(2 if not fop else -4)


def cartao(X0, Y0, w, h, alpha=0.45, fop=0.92):
    """cartao(X0, Y0, w, h) de keys43.js: fundo #131030 a 92%, borda GEO a 45%, raio 14."""
    return moldura(X0, Y0, w, h, GEO, alpha, 2, 14, BG_, fop)


def caixa_men(f, pad=14, cor=MEN):
    """caixaMen(el, pad=14) de keys43.js: moldura menta (wpx=3, raio=12) ao redor da fórmula f."""
    x0, y0 = pxof(f.get_corner(UL))
    x1, y1 = pxof(f.get_corner(DR))
    return moldura(x0 - pad, y0 - pad * .7, (x1 - x0) + 2 * pad, (y1 - y0) + 1.4 * pad, cor, 1.0, 3, 12)


def cm_mark(X, Y, r=17):
    """cmMark(X, Y, r=17) de keys43.js: ⊕ do centro de massa (fundo #16123A, anel ciano→magenta, cruz branca)."""
    fundo = Circle(radius=r / 120).move_to(PX(X, Y)).set_fill("#16123A", 1.0).set_stroke(width=0)
    anel1 = Arc(radius=r / 120, start_angle=PI / 4, angle=PI, arc_center=PX(X, Y)).set_stroke(CI, W(5)).set_fill(opacity=0)
    anel2 = Arc(radius=r / 120, start_angle=-3 * PI / 4, angle=PI, arc_center=PX(X, Y)).set_stroke(E2, W(5)).set_fill(opacity=0)
    lh = Line(PX(X - r + 5, Y), PX(X + r - 5, Y)).set_stroke(BR, W(2.5))
    lv = Line(PX(X, Y - r + 5), PX(X, Y + r - 5)).set_stroke(BR, W(2.5))
    g = sem_ctn(VGroup(fundo, anel1, anel2, lh, lv)).set_z_index(20)
    return g


def traco_h(X0, X1, Y, cor=GEO):
    """tracoH(X0, X1, Y, cor=GEO) de keys43.js: linha tracejada horizontal."""
    return lin_px([(X0, Y), (X1, Y)], cor, 2.5, alpha=1.0, dash=(9, 7), z=15)


def chip(tex, X, Y, size=30, cor=GEO):
    f = TC(tex, X + 16, Y, size, "l")
    x0, y0 = pxof(f.get_corner(UL))
    x1, y1 = pxof(f.get_corner(DR))
    mol = moldura(X, y0 - 10, (x1 - x0) + 32, (y1 - y0) + 20, cor, .75, 2, 10)
    g = VGroup(mol, f)
    g.eh_chip = True
    return g, f, mol


def chipm(partes, X, Y, size=30, cor=GEO):
    """Chip misto: texto Space Grotesk + MathTex alinhados pela linha de base (mixl), com moldura. Retorna (grupo, miolo, moldura)."""
    g = mixl(partes, X + 16, Y, size)
    x0, y0 = pxof(g.get_corner(UL))
    x1, y1 = pxof(g.get_corner(DR))
    mol = moldura(X, y0 - 10, (x1 - x0) + 32, (y1 - y0) + 20, cor, .75, 2, 10)
    c = VGroup(mol, g)
    c.eh_chip = True
    return c, g, mol


def selo(s, X, Y, cor=GEO, size=26):
    t = leg(s, X + 14, Y + 2, cor, "left", size)
    w = t.width * 120
    mol = moldura(X, Y - size - 6, w + 28, size + 22, cor, 1.0, 2, 8)
    return mol, t


def legq(cor, s, x, y, size=30):
    sq = ret_px(x, y - 9, x + 18, y + 9, fill=cor, fop=1.0, stroke=None, z=6)
    t = leg(s, x + 30, y, cor, "left", size)
    return sq, t


def painel2d43(X0, Y0, w, h, passo=30):
    fundo = moldura(X0, Y0, w, h, GEO, .45, 2, 14, "#16123A", 1.0)
    fundo.set_z_index(-3)
    gr = VGroup()
    for X in range(int(X0) + passo, int(X0 + w), passo):
        gr.add(lin_px([(X, Y0 + 3), (X, Y0 + h - 3)], "#2B2558", 1, z=-2))
    for Y in range(int(Y0) + passo, int(Y0 + h), passo):
        gr.add(lin_px([(X0 + 3, Y), (X0 + w - 3, Y)], "#2B2558", 1, z=-2))
    g = VGroup(fundo, gr)
    g._painel = (X0, Y0, X0 + w, Y0 + h)
    return g


class Vista2D:
    def __init__(self, cx, cy, u):
        self.cx, self.cy, self.u = cx, cy, u

    def P(self, x, y):
        return (self.cx + self.u * x, self.cy - self.u * y)

    def seta(self, a, b, cor, wpx=4, head=16):
        return seta_px(self.P(*a), self.P(*b), cor, wpx, head, z=6)

    def linha(self, pts, cor, wpx=4, dash=None):
        return lin_px([self.P(*p) for p in pts], cor, wpx, dash=dash, z=6)

    def ponto(self, p, cor, r=9):
        return ponto_px(*self.P(*p), cor, r, z=9)

    def arco(self, R, a0, a1, cor, wpx=4, n=40):
        pts = [(self.cx + R * math.cos(a0 + (a1 - a0) * k / n), self.cy - R * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]
        return lin_px(pts, cor, wpx, z=6)


def pronto(m):
    for x in m.get_family():
        if getattr(x, "_caneta", False):
            x._esc = True
    return m


class _Nada(Animation):
    def interpolate_mobject(self, alpha):
        pass


# ── cena-base do vídeo ───────────────────────────────────────────────────────────────────────────────────────
QA_PASSO = 3
MARGEM = 48

_ALIAS_GAT = {
    "um plano deitado na altura z barra": "plano deitado na altura z barra",
    "os dois pedaços sem raiz": "dois pedaços sem raiz",
    "a volta inteira em téta": "volta inteira em téta",
}


class B43(B34):
    """Base desta unidade: papel de borda a borda desde o quadro 0 (exceto CTA), palcos 3D, caneta, voos, glyph maps e QA."""
    ANTES = None

    def setup_base(self):
        super().setup_base()
        self._palcos = []
        self._rots3 = []
        self._dentro = []
        self._vazio0 = None
        self._parado = []
        self._col = {}
        self._ultimo_qa = -999
        self._ult_seg = -1
        self._r5v = []
        self._t_anim = 0.0
        # G1: papel de quadrados de 60 px em 1080p em toda a tela, inclusive sob o 3D (exceto CTA)
        self.papel_on(rt=0)
        if STILL is not None:
            _orig_render = self.renderer.render
            self.renderer.render = lambda *a, **k: _orig_render(*a, **k) if self.nq / FPS >= STILL - 0.2 else None

    def remove(self, *ms):
        fam = set()
        for m in ms:
            fam |= {id(x) for x in m.get_family()}
        super().remove(*ms)
        extra = [x for x in self.mobjects if id(x) in fam]
        if extra:
            super().remove(*extra)
        return self

    def _k_frase(self, aid, frase):
        import re as _r
        fala = ANC.get(aid, {}).get("fala", "").split()
        fr = _ALIAS_GAT.get(frase, frase)
        alvo = _r.findall(r"\w+", fr.lower())
        ks = [i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo]
        if not ks:
            return None
        agora = (self.nq - self._q0) / FPS
        tw = ANC[aid]["t"]
        return next((k for k in ks if tw[k] - LEAD >= agora - 0.6), ks[-1])

    def gat(self, frase):
        Base.gat(self, frase)

    # canto ------------------------------------------------------------------------------------------------
    def titulo(self, s, rt=0.4):
        novo = self._canto(txt(s, 21.6, color="#F5F7FF", bold=True, up=False), CANTO_Y2, topo_min=self._y1_fim_px() + 10)
        novo._canto2 = s
        if self.h2 is not None:
            self.play(FadeOut(self.h2), FadeIn(novo), run_time=rt)
            self.remove(self.h2)
        else:
            self.play(FadeIn(novo), run_time=rt)
        self.h2 = novo
        print(f"[canto] {self.lote} {self._aid} {self.t:.2f} {s}")

    # papel -----------------------------------------------------------------------------------------------
    def papel_on(self, v=None, passo=None, rt=0.5, junto=()):
        if self.grade is not None:
            return
        self.grade = (papel(v) if v is not None and passo is None else papel(v, passo=passo or 0.5)).set_z_index(-10)
        if rt > 0:
            self.play(FadeIn(self.grade), *junto, run_time=rt)
        else:
            self.add(self.grade)

    def papel_off(self, rt=0.5, junto=()):
        self.grade_off(rt=rt, junto=junto)

    # 3D --------------------------------------------------------------------------------------------------
    def palco(self, cena, cam, giro=0.0, obst=(), **ini):
        return Palco43(self, cena, cam, giro=giro, obst=obst, **{k: float(v) for k, v in ini.items()})

    def rot3(self, pal, nome, tex, dx=0.0, dy=0.0, size=34, ancora="c", placa=True, txtp=False, cor=None):
        """Rótulo preso a um ponto do 3D (Manim), com placa mínima. Em keys43.js: rotulo3 tem al='l' por padrão, aqui ancora='l'|'c'|'r'."""
        if txtp:
            f = T(tex, 0, 0, size, "left", cor or BR, bold=False)
        else:
            f = TC(tex, 960, 540, size, ancora)
        g = VGroup(placa_min(f), f) if placa else VGroup(f)
        g.f = f
        g._txt = tex
        g._rot3 = True
        pal.prende(g, nome, dx, dy, ancora)
        self._rots3.append(g)
        return g

    def pena(self, *ms, atraso=0.0, passo=None, extra=(), rt=None, lag=0.0):
        super().pena(*ms, atraso=atraso, passo=passo, extra=extra, rt=rt, lag=lag)
        for r in getattr(self, "_rots3", ()):
            if r.f in self.mobjects or r[0] in self.mobjects:
                self.remove(r.f, r[0])
                pronto(r)
                if r not in self.mobjects:
                    self.add(r)

    # escrita ---------------------------------------------------------------------------------------------
    def marca(self, alvo, agora=False):
        if not agora and self._aid is not None:
            _a0 = self._aid
            self._fecha(antes=0.75)
            self._aid = _a0
        t = self.nq / FPS
        print(f"[marca] {alvo} {t:.3f}")

    def degrau(self, conta, desc):
        print(f"[degrau] {self.lote} {self._aid} {(self.nq - self._q0) / FPS:7.2f} {self.t:8.2f} {conta} :: {desc}")

    def origem(self, o, de):
        print(f"[origem] {self.lote} {self._aid} {self.t:.2f} {o} <- {de}")

    def sub(self, *gs, rt=1.0, cor=BR):
        ss = []
        for g_ in gs:
            x0, x1 = pxof(g_.get_left())[0], pxof(g_.get_right())[0]
            y = pxof(g_.get_bottom())[1] + 7
            ss.append(sublinha_px(x0 - 2, x1 + 2, y, cor, 2))
        self.play(*[Create(s) for s in ss], run_time=0.25)
        if rt > 0:
            self.wait(rt)
        self.play(*[FadeOut(s) for s in ss], run_time=0.25)
        self.remove(*ss)

    def voos(self, pares, rt=1.0, arco=-0.6, extra=(), nota=""):
        an = []
        for src, alvo_m in pares:
            ja_escrita(alvo_m)
            for x in alvo_m.get_family():
                if getattr(x, "_caneta", False):
                    x._esc = True
                x._voando = True
            src_c = src.copy()
            for x in src_c.get_family():
                x._voando = True
                if isinstance(x, VMobject) and x.get_fill_opacity() > .1:
                    x.set_stroke(width=0, opacity=0)
            an.append(TransformFromCopy(src_c, alvo_m, path_arc=arco, run_time=rt))
        self.play(*an, *extra, run_time=rt)
        for a in an:
            self.remove(a.mobject)
        for _, b in pares:
            for x in b.get_family():
                x._voando = False
            self.add(b)
            junta(self, b)
            print(f"[voo] {self.lote} {self._aid} {(self.nq - self._q0) / FPS:6.2f}s {self.t:8.2f} {nota} {str(getattr(b, '_tex', getattr(b, '_txt', '')))[:80]!r}")

    def escreve(self, F, voos=(), rt_voo=1.0, extra=(), passo=None, arco=-0.6, atraso=0.0, nota=""):
        p = passo or CANETA_P
        gls = list(F[0])
        anims, voados = [], set()
        for src, idx in voos:
            ii = sel(F, idx) if not isinstance(idx, list) or (idx and not isinstance(idx[0], (int, np.integer))) else idx
            alvo = VGroup(*[gls[i] for i in ii])
            src_c = src.copy()
            for x in src_c.get_family():
                x._voando = True
                if isinstance(x, VMobject) and x.get_fill_opacity() > .1:
                    x.set_stroke(width=0, opacity=0)
            for x in alvo.get_family():
                x._voando = True
            anims.append(TransformFromCopy(src_c, alvo, path_arc=arco, run_time=rt_voo))
            voados |= set(ii)
            print(f"[voo] {self.lote} {self._aid} {(self.nq - self._q0) / FPS:6.2f}s {self.t:8.2f} {nota} {F._tex[:60]!r} glifos {ii[:3]}…")
        resto = VGroup(*[g_ for i, g_ in enumerate(gls) if i not in voados])
        if len(resto):
            resto._tex = F._tex + " (resto)"
            anims.append(caneta(resto, atraso=atraso, ritmo=p / 0.30))
        tot = max([rt_voo if voos else 0.0] + [a.tot for a in anims if isinstance(a, _Caneta)])
        F._em_caneta = True
        self.play(*anims, *extra, run_time=tot)
        for a in anims:
            if isinstance(a, TransformFromCopy):
                self.remove(a.mobject)
        for x in F.get_family():
            x._voando = False
        self.remove(*[a.mobject for a in anims if isinstance(a, _Caneta)])
        F._em_caneta, F._esc = False, True
        self.add(F)
        print(f"[pena] {self.lote} {self._aid} {(self.nq - self._q0) / FPS:6.2f}s {F._tex[:90]!r} dir={pxof(F.get_right())[0]:.0f}")
        return F

    def gm(self, n, A, B, pares, voos=(), rt=1.0, copia=False, nota="", extra=(), atraso_caneta=0.10):
        ent = [(sel(A, a), sel(B, b)) for a, b in pares]
        alvo = set()
        for _, b in ent:
            alvo |= set(b)
        repetidos = [i for _, b in ent for i in b]
        if len(repetidos) != len(set(repetidos)):
            print(f"[gm] AVISO glifo de B mapeado duas vezes no mapa {n}")
        voados = set()
        for _, b in voos:
            voados |= set(sel(B, b))
        novos = [i for i in range(len(B[0])) if i not in alvo]
        orig = {i: B[0][i].copy() for i in novos}
        for i in novos:
            B[0][i].set_fill(opacity=0).set_stroke(width=0, opacity=0)
        B._esc = True
        snapA = A.copy() if copia else None
        ent_n = ent + ([(_Nada, novos)] if novos else [])
        an = TransformByGlyphMap(A, B, *ent_n, from_copy=copia, auto_fade=True, run_time=rt)
        GM_LOG.append((self.lote, self._aid, round(self.t, 2), n, A._tex, B._tex))
        print(f"[gm] {self.lote} {self._aid} {(self.nq - self._q0) / FPS:6.2f}s {self.t:8.2f} mapa={n} pares={len(ent)} novos={len(novos)} {nota} :: "
              f"{A._tex[:70]!r} -> {B._tex[:80]!r}")
        for x in B.get_family():
            x._voando = True
        self.play(an, *extra, run_time=rt)
        if not copia:
            self.remove(A)
        self._limpa_soltos(A, B)
        self.add(B)
        for x in B.get_family():
            x._voando = False
        if novos:
            for i in novos:
                B[0][i].become(orig[i])
                B[0][i].set_fill(opacity=0).set_stroke(width=0, opacity=0)
            anims = []
            for src, b in voos:
                g_ = VGroup(*[B[0][i] for i in sel(B, b)])
                for i in sel(B, b):
                    B[0][i].become(orig[i])
                src_c = src.copy()
                for x in src_c.get_family():
                    x._voando = True
                    if isinstance(x, VMobject) and x.get_fill_opacity() > .1:
                        x.set_stroke(width=0, opacity=0)
                anims.append(TransformFromCopy(src_c, g_, path_arc=-0.6, run_time=0.8))
            resto = [i for i in novos if i not in voados]
            if resto:
                for i in resto:
                    B[0][i].become(orig[i])
                g_ = VGroup(*[B[0][i] for i in resto])
                g_._tex = B._tex + " (glifos novos)"
                g_._caneta, g_._esc, g_._em_caneta, g_._txt = True, False, False, None
                anims.append(caneta(g_, atraso=atraso_caneta if voos else 0.0, ritmo=CANETA_P / 0.30))
            tot = max([0.8 if voos else 0.0] + [a.tot for a in anims if isinstance(a, _Caneta)])
            self.play(*anims, run_time=tot)
            for a in anims:
                if isinstance(a, TransformFromCopy):
                    self.remove(a.mobject)
                if isinstance(a, _Caneta):
                    self.remove(a.mobject)
            self._limpa_soltos(A, B)
            self.add(B)
        if copia and snapA is not None:
            A.become(snapA)
            if not any(A in m.get_family() for m in self.mobjects):
                self.add(A)
        return B

    def _limpa_soltos(self, A, B):
        gs = {id(x) for x in A[0].submobjects} | {id(x) for x in B[0].submobjects}
        for m in list(self.mobjects):
            if m is A or m is B or getattr(m, "_tex", None) is not None or not isinstance(m, VMobject):
                continue
            fam = [x for x in m.get_family() if x is not m and len(x.points)]
            if (id(m) in gs) or (fam and all(id(x) in gs or any(id(y) in gs for y in x.get_family()) for x in fam)):
                self.remove(m)

    def chip_pena(self, cg, cf, cm_, **kw):
        self.pena(cf, extra=[Create(cm_)], **kw)
        self.remove(cf, cm_)
        pronto(cg)
        self.add(cg)
        return cg

    def chip_voo(self, cg, cf, mol, src, extra=(), rt=1.0, nota=""):
        """Chip que voa da linha `src` (TransformFromCopy) e ganha a moldura (Create); o resultado que continua sendo usado."""
        self.voos([(src, cf)], rt=rt, extra=[Create(mol), *extra], nota=nota)
        self.remove(cf, mol)
        pronto(cg)
        self.add(cg)
        return cg

    def chips_voo(self, itens, extra=(), rt=1.0, nota=""):
        """Vários chips voando juntos (cada item: (grupo, miolo, moldura, origem)); as molduras nascem no mesmo play."""
        self.voos([(src, cf) for _, cf, _, src in itens], rt=rt, extra=[Create(mol) for _, _, mol, _ in itens] + list(extra), nota=nota)
        for cg, cf, mol, _ in itens:
            self.remove(cf, mol)
            pronto(cg)
            self.add(cg)

    def velhos(self, *ms):
        vivos = []
        for m in ms:
            if m is None:
                continue
            if any(x in self.mobjects for x in m.get_family()):
                vivos.append(m)
        out = [m for m in vivos if not any(m is not o and m in o.get_family() for o in vivos)]
        return VGroup(*out)

    def sobe_sai(self, *ms, dy=0.5, rt=0.5, extra=()):
        g = self.velhos(*ms)
        if len(g):
            self.play(g.animate.shift(UP * dy).set_opacity(0), *extra, run_time=rt)
            for m in g:
                m.clear_updaters()
            self.remove(g)
        elif extra:
            self.play(*extra, run_time=rt)

    # coluna ----------------------------------------------------------------------------------------------
    def col(self, nome, *ms, chips=0):
        c = self._col.setdefault(nome, {"linhas": [], "chips": 0, "max": 0, "base": 0})
        for m in ms:
            if m not in c["linhas"]:
                c["linhas"].append(m)
        c["chips"] = max(c["chips"], chips)
        vivos = [m for m in c["linhas"] if any(y in self.mobjects for y in m.get_family()) or any(m in x.get_family() for x in self.mobjects)]
        c["linhas"] = vivos
        vivos = [m for m in vivos if not getattr(m, "eh_chip", False)]
        base = max([pxof(m.get_bottom())[1] for m in vivos] or [0])
        c["max"] = max(c["max"], len(vivos))
        print(f"[coluna] {self.lote} {self._aid} {self.t:.2f} {nome} linhas={len(vivos)} chips={c['chips']} base={base:.0f} folga={1080 - base:.0f}")

    def col_zera(self, nome):
        if nome in self._col:
            self._col[nome]["linhas"] = []

    def dentro(self, painel_rect, *itens):
        for it in itens:
            self._dentro.append((it, painel_rect))

    # QA por quadro ---------------------------------------------------------------------------------------
    def update_to_time(self, t):
        super().update_to_time(t)
        if not getattr(self, "_em_play", False) and not getattr(self, "_em_wait", False):
            return
        f = int(round(self.clk.get_value() * FPS))
        if f - self._ultimo_qa >= QA_PASSO:
            self._ultimo_qa = f
            self._qa_quadro(f)

    def play(self, *anims, run_time=None, **kw):
        self._em_wait = False
        super().play(*anims, run_time=run_time, **kw)

    def wait(self, duration=1.0, *a, **kw):
        t0 = self.t
        self._em_wait = True
        _r0 = self.renderer.render
        if not PEDIDOS3D and STILL is None and os.environ.get("SO_AUDITORIA") != "1":
            _feito = [False]

            def _fast_wait_render(sc, tm, mov=None):
                if not _feito[0]:
                    _r0(sc, tm, mov)
                    _feito[0] = True
                else:
                    self.renderer.add_frame(self.renderer.get_frame())

            self.renderer.render = _fast_wait_render
        try:
            super().wait(duration, *a, **kw)
        finally:
            self.renderer.render = _r0
            self._em_wait = False
        if duration >= 0.5:
            print(f"[espera] {self.lote} {self._aid} {t0:.2f} {duration:.2f}")

    def _caixas(self):
        cx = []
        fix = self.fixos()

        def caixa(x):
            vis = [g_ for g_ in x.family_members_with_points() if isinstance(g_, VMobject) and g_.get_fill_opacity() > 0.3
                   and not isinstance(g_, RoundedRectangle)]
            if not vis:
                return
            pts = np.concatenate([g_.points for g_ in vis])
            x0, x1 = pts[:, 0].min() * 120 + 960, pts[:, 0].max() * 120 + 960
            y0, y1 = 540 - pts[:, 1].max() * 120, 540 - pts[:, 1].min() * 120
            voa = any(getattr(g_, "_voando", False) for g_ in x.get_family())
            cx.append((getattr(x, "_txt", None) or "ponto", (x0, y0, x1, y1), getattr(x, "_obst", False), x, voa))

        def desce(x):
            if getattr(x, "_txt", None) is not None or getattr(x, "_obst", False):
                caixa(x)
                return
            for y in x.submobjects:
                desce(y)

        for m in self.mobjects:
            if m in fix or isinstance(m, (Fundo3D, ValueTracker)):
                continue
            desce(m)
        for pal in self._palcos:
            if pal.fundo in self.mobjects and pal.fundo.op.get_value() > 0.5:
                for nome in pal.obst:
                    x, y = pal.pt(nome)
                    cx.append((f"3d:{pal.cena}.{nome}", (x - 9, y - 9, x + 9, y + 9), True, pal, False))
        return cx

    def _still(self):
        if STILL is not None and self.nq / FPS >= STILL:
            self._dump_caixas()
        super()._still()

    def _dump_caixas(self):
        """QA v2 (texto × 3D, plaquinha × aresta, órfãos, painel vazio): caixas em px de 1080p no instante do still."""
        import json as _j
        out = {"t": STILL, "textos": [], "placas": [], "palcos": [], "rots3": [], "paineis": []}
        for nome, box, obst, x, voa in self._caixas():
            if str(nome).startswith("3d:") or voa:
                continue
            out["textos"].append({"nome": str(nome)[:60], "box": [round(float(b), 1) for b in box]})
        for r in self._rots3:
            vis = any(y in self.mobjects for y in r.get_family()) or any(r in m.get_family() for m in self.mobjects)
            p3 = getattr(r.f, "_p3d", None) or getattr(r, "_p3d", None)
            ent = {"txt": str(getattr(r, "_txt", "?"))[:40], "cena": p3[0] if p3 else None, "ponto": p3[1] if p3 else None, "visivel": bool(vis)}
            if vis and len(r) > 1 and len(r[0].points):
                pts = r[0].points
                ent["placa"] = [round(float(pts[:, 0].min() * 120 + 960), 1), round(float(540 - pts[:, 1].max() * 120), 1),
                                round(float(pts[:, 0].max() * 120 + 960), 1), round(float(540 - pts[:, 1].min() * 120), 1)]
                out["placas"].append({"nome": ent["txt"], "box": ent["placa"]})
            out["rots3"].append(ent)
        for pal in self._palcos:
            out["palcos"].append({"cena": pal.cena, "op": round(float(pal.fundo.op.get_value()), 3), "noscene": pal.fundo in self.mobjects})
        for m in self.mobjects:
            for g_ in m.get_family():
                pn = getattr(g_, "_painel", None)
                if pn is not None and isinstance(g_, RoundedRectangle):
                    dentro = 0
                    for o in self.mobjects:
                        if o is m or o is g_:
                            continue
                        for q in o.family_members_with_points():
                            if isinstance(q, VMobject) and q.get_fill_opacity() > .3 and q.get_stroke_opacity() >= 0 and not isinstance(q, RoundedRectangle):
                                cx_, cy_ = q.get_center()[0] * 120 + 960, 540 - q.get_center()[1] * 120
                                if pn[0] <= cx_ <= pn[2] and pn[1] <= cy_ <= pn[3]:
                                    dentro += 1
                    out["paineis"].append({"box": list(pn), "conteudo": dentro, "op_fill": round(float(g_.get_fill_opacity()), 2)})
        d = AQUI_RENDERS / "still"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{self.lote}_{STILL:g}_caixas.json").write_text(_j.dumps(out, ensure_ascii=False), encoding="utf-8")

    def _orfaos(self, t):
        """QA v2 (I1/I2): rótulo preso a um 3D visível enquanto o 3D dele não está na tela (ou já sumiu)."""
        for r in self._rots3:
            if not (any(y in self.mobjects for y in r.get_family()) or any(r in m.get_family() for m in self.mobjects)):
                continue
            ops = [g_.get_fill_opacity() for g_ in r.family_members_with_points() if isinstance(g_, VMobject)]
            if not ops or max(ops) < 0.5:
                continue
            p3 = getattr(r.f, "_p3d", None) or getattr(r, "_p3d", None)
            if not p3:
                continue
            pal = next((p for p in self._palcos if p.cena == p3[0] and p.fundo in self.mobjects), None)
            if pal is None or pal.fundo.op.get_value() < 0.15:
                print(f"[orfao] {self.lote} {self._aid} {t:7.2f}s rótulo {str(getattr(r, '_txt', '?'))[:30]!r} sem o 3D {p3[0]} na tela")

    def _qa_quadro(self, f):
        t = f / FPS
        self._orfaos(t)
        caixas = self._caixas()
        for i in range(len(caixas)):
            for j in range(i + 1, len(caixas)):
                a, b = caixas[i], caixas[j]
                if a[2] and b[2]:
                    continue
                (ax0, ay0, ax1, ay1), (bx0, by0, bx1, by1) = a[1], b[1]
                ox = min(ax1, bx1) - max(ax0, bx0)
                oy = min(ay1, by1) - max(ay0, by0)
                if ox > 2 and oy > 2:
                    if a[4] or b[4]:
                        self._r5v.append((self._aid, t, a[0], b[0]))
                        print(f"[R5V] {self.lote} {self._aid} {t:7.2f}s {str(a[0])[:40]!r} x {str(b[0])[:40]!r} ({ox:.0f}x{oy:.0f} px)")
                    else:
                        self._r5.append((self._aid, t, a[0], b[0], ox, oy))
                        print(f"[R5] {self.lote} {self._aid} {t:7.2f}s {str(a[0])[:40]!r} x {str(b[0])[:40]!r} ({ox:.0f}x{oy:.0f} px)")
        for nome, (x0, y0, x1, y1), obst, m, voa in caixas:
            if obst or voa:
                continue
            if x0 < MARGEM - 1 or x1 > 1920 - MARGEM + 1 or y1 > 1080 - MARGEM + 1 or y0 < MARGEM - 1:
                print(f"[R6] {self.lote} {self._aid} {t:7.2f}s margem {str(nome)[:50]!r} ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
        for it, (px0, py0, px1, py1) in self._dentro:
            if not any(it in x.get_family() for x in self.mobjects):
                continue
            ops = [g_.get_fill_opacity() for g_ in it.family_members_with_points() if isinstance(g_, VMobject)]
            if not ops or max(ops) < 0.3 or getattr(it, "_voando", False):
                continue
            x0, y1_ = pxof(it.get_corner(UL))
            x1, y0_ = pxof(it.get_corner(DR))
            if x0 < px0 + 4 or x1 > px1 - 4 or y1_ < py0 + 4 or y0_ > py1 - 4:
                print(f"[R6] {self.lote} {self._aid} {t:7.2f}s painel {str(getattr(it, '_txt', getattr(it, '_tex', '?')))[:50]!r} ({x0:.0f},{y1_:.0f},{x1:.0f},{y0_:.0f}) "
                      f"fora de ({px0},{py0},{px1},{py1})")
        grupos = {}
        for it, rect in self._dentro:
            grupos.setdefault(tuple(rect), []).append(it)
        for rect, itens in grupos.items():
            card = None
            for m in self.mobjects:
                for g_ in m.get_family():
                    if getattr(g_, "_painel", None) is not None and tuple(g_._painel) == rect and isinstance(g_, RoundedRectangle):
                        card = g_
            if card is None or card.get_fill_opacity() < 0.5:
                continue
            tem = False
            for it in itens:
                if not any(it in x.get_family() for x in self.mobjects):
                    continue
                if any(isinstance(q, VMobject) and (q.get_fill_opacity() > 0.05 or q.get_stroke_opacity() > 0.05) for q in it.family_members_with_points()):
                    tem = True
                    break
            if not tem:
                print(f"[painel-vazio] {self.lote} {self._aid} {t:7.2f}s cartão {rect} sem conteúdo")
        if self.h2 is not None and self.h2 in self.mobjects:
            hx0, hy0 = pxof(self.h2.get_corner(UL))
            hx1, hy1 = pxof(self.h2.get_corner(DR))
            for pal in self._palcos:
                if pal.fundo in self.mobjects and pal.fundo.op.get_value() > 0.5 and "eixoTopo" in P43[pal.cena]:
                    (xa, ya), (xb, yb) = pal.pt("eixoBase"), pal.pt("eixoTopo")
                    for u in np.linspace(0, 1, 40):
                        x, y = xa + (xb - xa) * u, ya + (yb - ya) * u
                        if hx0 - 6 <= x <= hx1 + 6 and hy0 - 6 <= y <= hy1 + 6:
                            print(f"[3dcanto] {self.lote} {self._aid} {t:7.2f}s eixo z de {pal.cena} cruza o canto")
                            break
        fix = self.fixos()
        conteudo = [m for m in self.mobjects if m not in fix and not isinstance(m, ValueTracker) and m is not self.clk]
        vis = 0
        for m in conteudo:
            if isinstance(m, Fundo3D):
                vis += m.op.get_value() > 0.3
            elif isinstance(m, ImageMobject):
                vis += 1
            else:
                vis += any(isinstance(g_, VMobject) and (g_.get_fill_opacity() > 0.3 or g_.get_stroke_opacity() > 0.3) for g_ in m.family_members_with_points())
        if vis == 0:
            if self._vazio0 is None:
                self._vazio0 = t
        else:
            if self._vazio0 is not None and t - self._vazio0 > 0.5:
                print(f"[vazio] {self.lote} {self._aid} {self._vazio0:.2f}–{t:.2f}s palco vazio {t - self._vazio0:.2f}s")
            self._vazio0 = None
        seg = int(t)
        if seg != self._ult_seg:
            self._ult_seg = seg
            tem3d = any(p.fundo in self.mobjects and p.fundo.op.get_value() > 0.5 for p in self._palcos)
            grade = self.grade is not None and self.grade in self.mobjects and self.grade.get_stroke_opacity() > 0.3
            cta = getattr(self, "_cta", False)
            tipo = "3D-grade" if (tem3d and grade) else ("2D-grade" if grade else ("CTA-liso" if cta else "SEM-GRADE"))
            canto2 = self.h2 is not None and self.h2 in self.mobjects
            print(f"[grade] {self.lote} {self._aid} {t:.0f} {tipo} canto2={'sim' if canto2 or cta or not self.CANTO else 'NAO'}")

    def fim(self):
        super().fim()
        print(f"[R5V-total] {self.lote} {len(self._r5v)}")
        for nome, c in self._col.items():
            print(f"[coluna-max] {self.lote} {nome} {c['max']} chips={c['chips']}")

    def entra(self, *ms, rt=0.5, extra=()):
        an = []
        for m in ms:
            if isinstance(m, Fundo3D):
                an.append(m.op.animate.set_value(1.0))
                if m not in self.mobjects:
                    m.op.set_value(0.0)
                    self.add(m)
            elif isinstance(m, (ImageMobject, Group)) and not isinstance(m, VMobject):
                an.append(FadeIn(m))
            else:
                an.append(Create(m))
        self.play(*an, *extra, run_time=rt)

    def sai(self, *ms, rt=0.4, extra=()):
        ms = [m for m in ms if m is not None and m in self.mobjects]
        if not ms and not extra:
            return
        an = [(m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m)) for m in ms]
        self.play(*an, *extra, run_time=rt)
        for m in ms:
            m.clear_updaters()
        self.remove(*ms)


def cta43(cena, rt_fim=0.0):
    CL = P3(0, 0.9)
    logo = cena.logo(5.6).move_to(CL)
    aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(CL), num_dashes=48).set_stroke(GEO, 2.6, opacity=o) for r, o in ((2.1, 0.85), (2.45, 0.6))])
    sem_ctn(aneis)
    ins = VGroup(T("INSCREVA-SE PARA ACOMPANHAR", 960, 0, 66, "center", caneta=False), T("OS PRÓXIMOS VÍDEOS", 960, 0, 66, "center", caneta=False)
                 ).arrange(DOWN, buff=0.12).move_to(P3(0, -2.6))
    s4 = cena.snap()
    sai_c = [m_ for m_ in (cena.h2, cena.h1, cena.grade) if m_ is not None and m_ in cena.mobjects]
    cena._cta = True
    cena.play(*[(m_.op.animate.set_value(0.0) if isinstance(m_, Fundo3D) else FadeOut(m_)) for m_ in s4 + sai_c], run_time=0.4)
    cena.play(FadeIn(logo, scale=0.96), FadeIn(aneis), FadeIn(ins, shift=0.1 * UP), run_time=0.5)
    for m_ in s4:
        m_.clear_updaters()
    cena.remove(*s4, *sai_c)
    cena.h2 = None
    cena.grade = None
    print(f"[cta] {cena.lote} {cena.t:.2f}")
    if cena.resta() + rt_fim > 0.05:
        cena.wait(cena.resta() + rt_fim)


# ── FINAL: PRESSA, duas passadas para a cena seguir a voz real (portado do v2kit.py do yt_0037, que veio do lib34.py do yt_0034) ──────────────
# Passada 1 (PRESSA=grava, --dry_run): cada trecho entre dois gatilhos (gat, an, fim) anota o tempo de animação dele e o atraso com que chegou ao
# gatilho do fim. Fator do trecho = (tempo − atraso que o próprio trecho criou − 0,1 s) ÷ tempo, com piso PISO_PRESSA (0,6: a construção nunca
# fica mais de 1,67× mais rápida). Trechos com folga se esticam (teto 2,6×) em vez de a tela esperar parada. A voz nunca muda.
import json as _json
import os as _os
from pathlib import Path as _Path
import kit as _kit

PRESSA = _os.environ.get("PRESSA", "usa")
PISO_PRESSA = float(_os.environ.get("PISO_PRESSA", "0.6"))
_DIRPR = _Path(__file__).resolve().parent / "renders" / "pressa"
_B = B43
_play_pr0, _wait_pr0, _gat_pr0, _an_pr0, _fim_pr0 = _B.play, _B.wait, _B.gat, _B.an, _B.fim


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
    if abs(f - 1.0) > 0.001:
        for a in anims:
            a.run_time *= f
        rt *= f
        run_time = rt if run_time is not None else None
    S.setdefault(self._seg, {"rt": 0.0, "late": 0.0, "nome": ""})["rt"] += rt
    return _play_pr0(self, *anims, run_time=run_time, **kw)


def _wait_pr(self, duration=1.0, *a, **k):
    S = _pr(self)
    if not self._em_gat and duration > 0.2:
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
        if k is not None:
            if not hasattr(self, "_gpos"):
                self._gpos = {}
            self._gpos[self._aid] = k


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
                fat[s] = round(max(PISO_PRESSA, (d["rt"] - need - 0.1) / d["rt"]), 3)
            elif -d["late"] > 1.2 and d["rt"] > 0.15 and not (d["nome"] == "fim do lote" or d["nome"].startswith("in")):
                fat[s] = round(min(2.6, (d["rt"] - d["late"] - 0.4) / d["rt"]), 3)
            ant = d["late"]
        _DIRPR.mkdir(parents=True, exist_ok=True)
        (_DIRPR / f"{self.lote}.json").write_text(_json.dumps({"fator": fat, "trechos": S}, ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"[pressa] {self.lote}: {len(fat)} trechos ajustados; menor fator {min(fat.values()) if fat else 1:.2f}")
    return _fim_pr0(self)


_B.play, _B.wait, _B.gat, _B.an, _B.fim = _play_pr, _wait_pr, _gat_pr, _an_pr, _fim_pr



# ── Registro de tamanhos para o QA (§6.1) ───────────────────────────────────────────────────────────────────
_CTX = {"lote": "?", "aid": "?"}
_TAM = []
_TC_ORIG, _T_ORIG, _LEG_ORIG = TC, T, leg


def TC(s, x=960, y=540, size=48, al="l", caneta=True):                      # noqa: F811
    _TAM.append(("F", _CTX["aid"], size, str(s)[:60]))
    return _TC_ORIG(s, x, y, size, al, caneta)


def T(s, x, y, size=30, al="left", cor=BR, bold=True, caneta=True):          # noqa: F811
    _TAM.append(("T", _CTX["aid"], size, str(s)[:60]))
    return _T_ORIG(s, x, y, size, al, cor, bold, caneta)


def leg(s, x, y, cor=GEO, al="left", size=28, caneta=True):                   # noqa: F811
    return T(s, x, y, max(26, size), al, cor, bold=False, caneta=caneta)


_v41.TC = TC
_v41.T = T
_v41.leg = leg


_an_tam0, _fim_tam0 = B43.an, B43.fim


def _an_tam(self, aid):
    _CTX["lote"], _CTX["aid"] = self.lote, aid
    return _an_tam0(self, aid)


def _fim_tam(self):
    for k, a, sz, tx in _TAM:
        print(f"[tam] {self.lote} {a} {k} {sz} {tx!r}")
    return _fim_tam0(self)


_quadro_orig = Fundo3D._quadro


def _quadro_fallback(self):
    f = int(round(self.cm.clk.get_value() * FPS))
    if not PEDIDOS3D and f != self.f:
        arq = self.dir / f"f{f:05d}.png"
        if not arq.exists():
            alt_dir = DIR3D / "q3d" / f"{self.cm.lote}_960x540" / self.cena
            if (alt_dir / f"f{f:05d}.png").exists():
                self.dir = alt_dir
    return _quadro_orig(self)


Fundo3D._quadro = _quadro_fallback
B43.an, B43.fim = _an_tam, _fim_tam
