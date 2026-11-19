"""yt_0041 · CÁLCULO III · EP. 16 (provisório) · Coordenadas esféricas na integral tripla — camada da unidade sobre o v41.py (kit copiado do yt_0037).

- Macros do preâmbulo = as do referencia/yt_0041_quadros_alvo_v1_1/sb41.html (\\R, \\F, \\T, \\Rs, \\J, \\de, \\uu…): r laranja, φ violeta, θ verde-água,
  s pêssego, x âmbar, y magenta, z azul, r² sen φ lima (o bloco inteiro), ρ ciano, u #E08A3C.
- Câmeras e pontos 3D = os do c41.js (porte do c3d41.html): `cam41(cena, dx, dy, esc)` reproduz o enquadramento dos alvos (deslocamento e escala do
  sb41.html) com setViewOffset + zoom (fov), sem redimensionar o PNG. `Palco41` = Palco3D do kit + giro da câmera em volta do eixo z (um ValueTracker).
- Escrita: caneta glifo a glifo (B34.pena), voos (TransformFromCopy em arco, sem fantasma: a cópia sai só com preenchimento), glyph maps do MF-Tools
  (`passo`: TransformByGlyphMap com mapa explícito, auto_fade só no que sai; o glifo que entra é escrito pela caneta ou voa da fonte).
- Sem palco "vivo": nenhum pulso, nenhum laço; o kit copiado não tem _pulso (o palco vivo do yt_0037 morava no p37/v2kit, que não foram copiados).
- QA por quadro (a cada 0,2 s, inclusive durante animações e voos): [R5], [R5V] (voo × texto), [R6] (margem 48 px e painel), [vazio], [grade],
  [parado], [3dcanto]; e logs [gm], [degrau], [voo], [pena], [coluna], [marca] para os relatórios do qa41.py.
Tudo em px de 1080p (PX)."""
from v41 import *  # noqa: F401,F403
from v41 import _Caneta  # noqa: F401
from MF_Tools import TransformByGlyphMap

# ── paleta desta unidade (handoff §3.3) ─────────────────────────────────────────────────────────────────────
RO, FI, TH, SOMB, LI, EZ, UU = "#FF9440", "#B48CFF", "#2EE6A6", "#FFC08A", "#C6F26B", "#5AA2FF", "#E08A3C"
TRC = "#6C7698"

TEX31.add_to_preamble(
    r"\definecolor{ro}{HTML}{FF9440}\definecolor{fi}{HTML}{B48CFF}\definecolor{th}{HTML}{2EE6A6}\definecolor{so}{HTML}{FFC08A}"
    r"\definecolor{lim}{HTML}{C6F26B}\definecolor{ez}{HTML}{5AA2FF}\definecolor{uu}{HTML}{E08A3C}"
    r"\def\Z{\textcolor{ez}{z}}\def\dZ{\textcolor{ez}{dz}}\def\dX{\textcolor{ca}{dx}}\def\dY{\textcolor{cm}{dy}}"
    r"\def\R{\textcolor{ro}{r}}\def\F{\textcolor{fi}{\varphi}}\def\T{\textcolor{th}{\theta}}\def\Rs{\textcolor{so}{s}}"
    r"\def\dR{\textcolor{ro}{dr}}\def\dF{\textcolor{fi}{d\varphi}}\def\dT{\textcolor{th}{d\theta}}"
    r"\def\DR{\textcolor{ro}{\Delta r}}\def\DF{\textcolor{fi}{\Delta\varphi}}\def\DT{\textcolor{th}{\Delta\theta}}"
    r"\def\J{\textcolor{lim}{r^2\operatorname{sen}\varphi}}\def\Li#1{\textcolor{lim}{#1}}\def\de{\textcolor{ci}{\rho}}"
    r"\def\Ro#1{\textcolor{ro}{#1}}\def\Fi#1{\textcolor{fi}{#1}}\def\Th#1{\textcolor{th}{#1}}\def\So#1{\textcolor{so}{#1}}\def\Ez#1{\textcolor{ez}{#1}}"
    r"\def\Uu#1{\textcolor{uu}{#1}}\def\uu{\textcolor{uu}{u}}\def\du{\textcolor{uu}{du}}")


# ── câmeras e pontos do c41.js ──────────────────────────────────────────────────────────────────────────────
# ver(pos, alvo, cx, cy) do c3d41.html com o fator DF de distância (pos = alvo + (pos − alvo)·DF), up = +z, fov 22°
VER = {"bola": ((9.2, -6.2, 5.8), (0, 0, -.1), 600, 560, 1.4), "receita": ((9.0, -6.8, 4.6), (0, 0, .25), 600, 560, 1.4), "grade": ((9.0, -6.8, 4.0), (0, 0, .05), 600, 560, 1.4),
       "ponto": ((8.6, -5.4, 4.4), (0, .6, .95), 620, 560, 1.3), "caixa": ((8.2, -5.6, 5.6), (1.15, 1.45, 1.0), 600, 520, 1.15),
       "bolagrade": ((9.0, -6.8, 4.0), (0, 0, .05), 600, 560, 1.4), "caixinha": ((7.2, -6.4, 4.9), (.95, .45, .35), 620, 560, 1.15),
       "cebola": ((9.2, -6.2, 5.8), (0, 0, -.1), 600, 560, 1.4), "casquinha": ((8.6, -6.4, 4.6), (0, 0, 1.2), 600, 560, 1.4),
       "lata": ((8.4, -6.3, 4.4), (0, 0, .6), 600, 560, 1.4)}
# enquadramento dos alvos no sb41.html: cena3d(k, {dx, dy, esc})
ENQ = {"h1": ("bola", -40, 20, 1), "h2": ("grade", -30, 80, .94), "b1": ("ponto", -150, 60, .95), "b13a": ("caixa", 20, 210, .62), "b13b": ("bolagrade", 640, 210, .62),
       "b21": ("caixinha", 190, 150, .58), "b24": ("bolagrade", -180, 60, .9), "b31a": ("caixa", 20, 40, .56), "b31b": ("bolagrade", 700, 40, .56),
       "b32": ("receita", -60, 40, 1), "b4": ("cebola", -40, 20, 1), "b5": ("bola", -40, 20, 1), "b6": ("casquinha", 110, 110, .42), "s2": ("lata", -20, 110, .42)}


def cam41(cena, dx=0.0, dy=0.0, esc=1.0):
    """Câmera do alvo: a do c3d41.html (ver) com o PNG deslocado de (dx, dy) e escalado por esc em volta de (0, 0) = setViewOffset em
    (dx + esc·cx, dy + esc·cy) e fov com tan(fov/2) dividido por esc (zoom exato da perspectiva; o traço é geometria, escala junto)."""
    p, t, cx, cy, DF = VER[cena]
    p, t = np.array(p, float), np.array(t, float)
    pos = t + (p - t) * DF
    fov = 2 * math.degrees(math.atan(math.tan(math.radians(11.0)) / esc))
    return cam_dict(pos, t, (0, 0, 1), dx + esc * cx, dy + esc * cy, fov)


def cam_alvo(k):
    c, dx, dy, esc = ENQ[k]
    return cam41(c, dx, dy, esc)


def gira_cam(c, graus):
    """A câmera girada de `graus` em volta do eixo z que passa pelo alvo (um parâmetro de ângulo)."""
    if abs(graus) < 1e-9:
        return c
    a = math.radians(graus)
    t = np.array(c["tgt"])
    d = np.array(c["pos"]) - t
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    c2 = dict(c)
    c2["pos"] = [float(x) for x in t + R @ d]
    return c2


def _sph(r, f, t):
    return np.array([r * math.sin(f) * math.cos(t), r * math.sin(f) * math.sin(t), r * math.cos(f)])


CAZ = math.atan2(-6.2, 9.2)


def _pontos41():
    P = {}
    # bola (SC = 2)
    SC = 2.0
    WS = lambda r, f, t: SC * _sph(r, f, t)
    Wp = lambda X, Y, Z: SC * np.array([X, Y, Z], float)
    tA, tB = CAZ - PI / 4, CAZ + PI / 4
    P["bola"] = {"ex": (SC * 1.62, 0, 0), "ey": (0, SC * 1.62, 0), "ez": (0, 0, SC * 1.58), "centro": (0, 0, 0), "faceZ": WS(.55, PI / 4, 0), "faceY": WS(.55, PI / 4, -PI / 2),
                 "faceChao": WS(.55, PI / 2, -PI / 4), "casca": WS(1.02, PI * .7, PI * .55), "aR": WS(.65, PI / 2, -PI / 4), "bR": WS(.92, PI / 2, -PI / 4),
                 "c084": WS(.92, PI / 2, -.35), "fora": WS(1.0, PI * .62, PI * .35), "topo": (0, 0, SC + .1)}
    P["cebola"] = dict(P["bola"])
    P["cebola"].update({"casca": WS(.65, PI / 2, -PI / 4), "espessura": WS(.65, PI / 4, 0), "raio": WS(.33, PI / 2, -PI / 4)})
    SC = 2.1
    P["receita"] = {"O": (0, 0, 0), "entra": WS(.5, PI / 4, -.06) , "sai": WS(1.0, PI / 4, -.06), "ez": SC * np.array([0, 0, 1.42]), "cone1": WS(.78, PI / 6, PI * .55),
                    "cone2": WS(.78, PI / 3, PI * 1.2), "casca": WS(1.02, PI / 4, PI * .8)}
    SC = 2.0
    # grade (SC = 2,1)
    SC = 2.1
    t1, t2 = -PI / 2 + .15, -PI / 2 + .15 + PI / 6
    P["grade"] = {"celPolo": WS(1.04, PI / 12, (t1 + t2) / 2), "celEq": WS(1.04, 5 * PI / 12, (t1 + t2) / 2), "celPoloIn": WS(.75, PI / 12, (t1 + t2) / 2),
                  "celEqIn": WS(.75, 5 * PI / 12, (t1 + t2) / 2), "cone": WS(.95, PI / 4, PI * .85), "pagina": WS(.7, PI * .62, -PI / 4), "esfera": WS(1, PI * .7, PI * .15),
                  "ez": (0, 0, SC * 1.35 + .15), "centro": (0, 0, 0), "cascaP": WS(.6, PI * .3, PI * .55)}
    # ponto (SC = 1,35)
    SC = 1.35
    rho, f, t = 2.0, PI / 6, PI / 3
    Pp = _sph(rho, f, t)
    P1 = np.array([Pp[0], Pp[1], 0.0])
    P["ponto"] = {"ex": (SC * 2.58, 0, 0), "ey": (0, SC * 2.53, 0), "ez": (0, 0, SC * 2.5), "P": Wp(*Pp), "P1": Wp(*P1), "meioRho": Wp(*(Pp * .5)),
                  "meioR": Wp(P1[0] * .5, P1[1] * .5, 0), "arcoFi": WS(.78, f * .5, t), "arcoTh": Wp(.85 * math.cos(t * .45), .85 * math.sin(t * .45), 0),
                  "meioZ": Wp(Pp[0], Pp[1], Pp[2] * .5), "zEixo": Wp(0, 0, rho * math.cos(f)), "O": (0, 0, 0), "xP": Wp(Pp[0], 0, 0), "yP": Wp(0, Pp[1], 0)}
    # caixa (SC = 1): Q(r, φ, θ) = (r·A, θ·Cc, φ·B)
    A_, B_, Cc = 2.2, 2.2 / PI, 3.0 / (2 * PI)
    Q = lambda r, f, t: np.array([r * A_, t * Cc, f * B_])
    t1c, t2c = 3 * PI / 2 + .15, 3 * PI / 2 + .15 + PI / 6
    P["caixa"] = {"eRho": Q(1.5, 0, 0), "eTh": Q(1, 0, 2 * PI + 1.05), "eFi": Q(0, PI + .68, 0), "um": Q(1, 0, 0), "pi": Q(0, PI, 0), "dois_pi": Q(1, 0, 2 * PI),
                  "zero": Q(0, 0, 0), "cel": Q(1, 5 * PI / 12, (t1c + t2c) / 2), "faceR0": Q(0, PI / 2, 0), "faceT0": Q(.5, PI / 2, 0), "arestaR0": Q(0, PI, PI),
                  "meioT": Q(1, PI, PI), "cima": Q(1, PI / 2, PI / 2), "baixo": Q(1, PI / 2, 3 * PI / 2), "cortePi": Q(.5, PI, PI), "piTh": Q(1, 0, PI),
                  "m1": Q(.5, PI / 2, PI / 2), "m2": Q(.5, PI / 2, 3 * PI / 2)}
    # bolagrade (SC = 2,1)
    SC = 2.1
    ra, rb, fs, ts = .45, .9, PI / 4, -PI * .42
    P["bolagrade"] = {"cel": WS(1.05, 5 * PI / 12, (t1 + t2) / 2), "origem": (0, 0, 0), "eixo": Wp(0, 0, .85), "costura": WS(.75, PI * .6, 0), "ez": (0, 0, SC + .25),
                      "raioM": WS(.6, PI / 2, -.25), "meridiano": WS(1.04, PI * .62, -PI * .5), "volta": WS(1.03, PI / 2, -PI * .2), "polo": WS(1, 0, 0),
                      "sul": WS(1, PI, 0), "entra": WS(ra, fs, ts), "sai": WS(rb, fs, ts), "regiao": WS(.68, PI / 4, ts + .9)}
    # caixinha (SC = 2,6)
    SC = 2.6
    r1, r2, f1, f2, t1k, t2k = .62, 1.0, PI / 3, PI / 2 - .06, .30, .82
    zc = r2 * math.cos(f2)
    q = _sph(r2, f2, t1k)
    P["caixinha"] = {"dRho": WS((r1 + r2) / 2, f2, t1k), "dFi": WS(r2, (f1 + f2) / 2, t1k), "dTh": WS(r2, f2, (t1k + t2k) / 2), "raioPar": Wp(q[0] * .5, q[1] * .5, zc),
                     "eixoPar": Wp(0, 0, zc), "O": (0, 0, 0), "arcoFi": WS(.34, f1 * .5, t1k), "ez": Wp(0, 0, 1.24), "cel": WS(r2, (f1 + f2) / 2, (t1k + t2k) / 2),
                     "canto": WS(r2, f2, t1k)}
    # casquinha (SC = 1,55)
    SC = 1.55
    CA = math.atan2(-6.4, 8.6)
    ta, tb = CA - PI / 9, CA + PI / 2
    R2 = lambda f: 2 * math.cos(f)
    fs, tm = PI / 6, tb - .035
    P["casquinha"] = {"O": (0, 0, 0), "saida": WS(R2(fs), fs, tm), "cone": WS(1.05, PI / 4, CA - PI * .45), "calota": WS(R2(.35), .35, CA - PI * .5),
                      "encontro": WS(math.sqrt(2), PI / 4, CA - PI * .3), "limite": WS(R2(PI / 4) * .5, PI / 4, tm), "arcoFi": WS(.62, fs * .5, tm),
                      "meioSonda": WS(R2(fs) * .55, fs, tm), "topo": Wp(0, 0, 2), "ez": Wp(0, 0, 2.6), "ex": (SC * 1.72, 0, 0), "ey": (0, SC * 1.72, 0), "um": Wp(0, 0, 1),
                      "faceA": WS(.8, PI / 8, ta), "faceB": WS(.8, PI / 8, tb), "encChao": Wp(math.cos(CA - PI * .3), math.sin(CA - PI * .3), 0),
                      "pecaCone": WS(.75, PI / 8, tb), "pecaBola": WS(1.55, PI / 10, tb)}
    # lata (SC = 2,2)
    SC = 2.2
    CA = math.atan2(-6.3, 8.4)
    ta, tb = CA - PI / 9, CA + PI / 2
    tm = tb - .03
    s1, s2 = PI / 3, PI / 8
    P["lata"] = {"O": (0, 0, 0), "parede": WS(1 / math.sin(s1), s1, tm), "tampa": WS(1 / math.cos(s2), s2, tm), "quina": Wp(math.cos(tm), math.sin(tm), 1),
                 "meio1": Wp(*_sph(1 / math.sin(s1) * .55, s1, tm)), "meio2": Wp(*_sph(1 / math.cos(s2) * .6, s2, tm)), "ez": Wp(0, 0, 1.55),
                 "lado": Wp(math.cos(tb + 1.2), math.sin(tb + 1.2), .5), "meioQ": Wp(math.cos(tm) * .5, math.sin(tm) * .5, .5)}
    # topo de cada eixo z desenhado (QA 3D × canto: o segmento da base até o topo não pode cruzar o título)
    TOPO = {"receita": (0, 0, 2.1 * 1.3), "bola": (0, 0, 2 * 1.45), "grade": (0, 0, 2.1 * 1.35), "ponto": (0, 0, 1.35 * 2.35), "bolagrade": (0, 0, 2.1 * 1.12), "caixinha": (0, 0, 2.6 * 1.0),
            "cebola": (0, 0, 2 * 1.45), "casquinha": (0, 0, 1.55 * 2.5), "lata": (0, 0, 2.2 * 1.45)}
    BASE = {"receita": (0, 0, 0), "bola": (0, 0, 0), "grade": (0, 0, 0), "ponto": (0, 0, 0), "bolagrade": (0, 0, 0), "caixinha": (0, 0, -2.6 * .30), "cebola": (0, 0, 0),
            "casquinha": (0, 0, 0), "lata": (0, 0, 0)}
    for c in TOPO:
        P[c]["eixoTopo"] = TOPO[c]
        P[c]["eixoBase"] = BASE[c]
    return {c: {k: np.array(v, float) for k, v in d.items()} for c, d in P.items()}


P41 = _pontos41()


class Palco41(Palco3D):
    """Palco3D do kit (estado por quadro → pedidos3d → PNG do c41.js) + `giro` (graus) da câmera em volta do eixo z, um ValueTracker só."""

    def __init__(self, sc, cena, cam, giro=0.0, obst=(), **ini):
        self._giro0 = giro
        super().__init__(sc, cena, cam, **ini)
        self.tr["giro"] = ValueTracker(float(giro))
        sc.add(self.tr["giro"])
        self.obst = list(obst)            # pontos do 3D que nenhum rótulo pode cobrir (R5: placa × ponto)
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
        return proj3d(self.cam(), P41[self.cena][nome])

    def ptm(self, nome, dx=0.0, dy=0.0):
        x, y = self.pt(nome)
        return PX(x + dx, y + dy)


# ── texto e peças ────────────────────────────────────────────────────────────────────────────────────────────
GM_LOG = []
_NG = {}


def ng(tex):
    """Nº de glifos de um pedaço de LaTeX (mesmo template e mesma troca do \\sum do TC)."""
    if tex not in _NG:
        _NG[tex] = len(MathTex(r"\textstyle " + tex.replace(r"\sum", r"\sum\nolimits"), font_size=30, tex_template=TEX31)[0]) if tex.strip() else 0
    return _NG[tex]


def L(pecas, x, y, size=40, al="l", caneta=True):
    """Fórmula por peças [(chave, tex), …] (ou tex solto): MathTex de string única + m._ix = {chave: [índices de glifo]}."""
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
    """chave | range | lista de chaves e/ou índices → lista de índices de glifo."""
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
    """mixl do sb41: ('m', tex) em MathTex de S px; ('L', peças) idem com índices; ('t', texto[, cor]) em Space Grotesk de 0,78·S px (≥ 26),
    linha de base em Y + 0,27·S; respiro 14 px."""
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


def painel41(X0, Y0, w, h, alpha=0.35, fop=1.0):
    """Painel do sb41 (borda GEO a 35 %, cantos 14) com fundo OPACO (#131030): por cima do papel de borda a borda."""
    return moldura(X0, Y0, w, h, GEO, alpha, 2, 14, BG_, fop)


def chip(tex, X, Y, size=30, cor=GEO):
    """chip do sb41: fórmula a X + 16 px, moldura arredondada (10 px) com 10 px de folga em cima/embaixo e 16 dos lados, borda a 75 %."""
    f = TC(tex, X + 16, Y, size, "l")
    x0, y0 = pxof(f.get_corner(UL))
    x1, y1 = pxof(f.get_corner(DR))
    mol = moldura(X, y0 - 10, (x1 - x0) + 32, (y1 - y0) + 20, cor, .75, 2, 10)
    return VGroup(mol, f), f, mol


def selo(s, X, Y, cor=GEO, size=26):
    t = leg(s, X + 14, Y + 2, cor, "left", size)
    w = t.width * 120
    mol = moldura(X, Y - size - 6, w + 28, size + 22, cor, 1.0, 2, 8)
    return mol, t


def chave_um(F, idx, size=24, cor=GEO, txt_="=1"):
    """Chave fina sob os glifos idx de F, com o "= 1" pequeno embaixo (o valor que a voz lê: "que é um")."""
    g_ = VGroup(*[F[0][i] for i in idx])
    x0, x1 = pxof(g_.get_left())[0], pxof(g_.get_right())[0]
    y = pxof(g_.get_bottom())[1] + 8
    ch = chave_h(x0 + 2, x1 - 2, y, cor, 2, para_baixo=True)
    um = TC(r"=\,1", (x0 + x1) / 2, y + 26, size, "c")
    return ch, um


def guia41(A, B, cor=GEO, wpx=2):
    return lin_px([A, B], cor, wpx, alpha=.7, dash=(6, 6), z=3)


def chave_h(X0, X1, Y, cor=GEO, wpx=2, para_baixo=True):
    """Chave horizontal fina (abre para cima quando para_baixo: a ponta no meio aponta para baixo)."""
    def qb(a, c, b, n=10):
        return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]) for t in np.linspace(0, 1, n)]
    s = 1 if para_baixo else -1
    m = (X0 + X1) / 2
    pts = (qb((X0, Y - 8 * s), (X0, Y), (X0 + 12, Y)) + qb((m - 10, Y), (m, Y), (m, Y + 10 * s)) + qb((m, Y + 10 * s), (m, Y), (m + 10, Y))
           + qb((X1 - 12, Y), (X1, Y), (X1, Y - 8 * s)))
    return lin_px(pts, cor, wpx, z=6)


def pronto(m):
    """Fórmula/rótulo que entra por transformação (ReplacementTransform/TransformFromCopy) de algo já escrito: libera do portão FLASH."""
    for x in m.get_family():
        if getattr(x, "_caneta", False):
            x._esc = True
    return m


class _Nada(Animation):
    """Introdutor nulo para o TransformByGlyphMap: o glifo novo não entra por FadeIn (fica apagado até a caneta ou o voo)."""

    def interpolate_mobject(self, alpha):
        pass


# ── cena-base do vídeo ───────────────────────────────────────────────────────────────────────────────────────
QA_PASSO = 3            # quadros entre amostras de QA (0,2 s a 15 fps)
MARGEM = 48


class B41(B34):
    """Base desta unidade: canto de duas linhas (a linha 2 desde o 1º quadro do lote), papel de borda a borda nas cenas 2D, palcos 3D, caneta,
    voos, glyph maps e QA por quadro."""
    ANTES = None

    def setup_base(self):
        super().setup_base()
        self._palcos = []
        self._dentro = []          # (item, painel) para o R6
        self._vazio0 = None
        self._parado = []
        self._col = {}
        self._ultimo_qa = -999
        self._ult_seg = -1
        self._r5v = []
        self._t_anim = 0.0

    def remove(self, *ms):
        """Tirar um grupo tira também as suas partes que estejam soltas no topo da cena (nada invisível acumulando)."""
        fam = set()
        for m in ms:
            fam |= {id(x) for x in m.get_family()}
        super().remove(*ms)
        extra = [x for x in self.mobjects if id(x) in fam]
        if extra:
            super().remove(*extra)
        return self

    def _k_frase(self, aid, frase):
        """A ocorrência da frase que vem DEPOIS do ponto atual da âncora (frases repetidas: a 1ª ainda não lida)."""
        import re as _r
        fala = ANC.get(aid, {}).get("fala", "").split()
        alvo = _r.findall(r"\w+", frase.lower())
        ks = [i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo]
        if not ks:
            return None
        agora = (self.nq - self._q0) / FPS
        tw = ANC[aid]["t"]
        pos = getattr(self, "_gpos", {}).get(aid, 0)                      # os gatilhos vêm na ordem da fala: a ocorrência a partir do gatilho anterior
        return next((k for k in ks if k >= pos), ks[-1])

    def gat(self, frase):
        Base.gat(self, frase)            # o R5 desta unidade é o do _qa_quadro (a cada 0,2 s), não o do B34 no gatilho

    # canto ------------------------------------------------------------------------------------------------
    def titulo(self, s, rt=0.4):
        """Troca a linha 2 do canto sem buraco: a velha sai e a nova entra no mesmo play."""
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
        """Grade de borda a borda: nasce dos eixos do palco v (quadradinho 0,25) ou, sem eixos, passo 0,5 da unidade padrão (60 px)."""
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
        return Palco41(self, cena, cam, giro=giro, obst=obst, **{k: float(v) for k, v in ini.items()})

    def rot3(self, pal, nome, tex, dx=0.0, dy=0.0, size=34, ancora="c", placa=True, txtp=False, cor=None):
        """Rótulo preso a um ponto do 3D (Manim), com placa mínima (R2). `txtp`: rótulo de palavra (Space Grotesk)."""
        if txtp:
            f = T(tex, 0, 0, size, "left", cor or BR, bold=False)
        else:
            f = TC(tex, 960, 540, size, "c")
        g = VGroup(placa_min(f), f) if placa else VGroup(f)
        g.f = f
        g._txt = tex
        g._rot3 = True
        pal.prende(g, nome, dx, dy, ancora)
        return g

    # escrita ---------------------------------------------------------------------------------------------
    def degrau(self, conta, desc):
        print(f"[degrau] {self.lote} {self._aid} {(self.nq - self._q0) / FPS:7.2f} {self.t:8.2f} {conta} :: {desc}")

    def origem(self, o, de):
        print(f"[origem] {self.lote} {self._aid} {self.t:.2f} {o} <- {de}")

    def sub(self, *gs, rt=1.0):
        """Sublinhado de leitura (traço branco fino de 2 px) sob os glifos que a voz lê: aparece, fica `rt` s e sai."""
        ss = []
        for g_ in gs:
            x0, x1 = pxof(g_.get_left())[0], pxof(g_.get_right())[0]
            y = pxof(g_.get_bottom())[1] + 7
            ss.append(sublinha_px(x0 - 2, x1 + 2, y, BR, 2))
        self.play(*[Create(s) for s in ss], run_time=0.25)
        if rt > 0:
            self.wait(rt)
        self.play(*[FadeOut(s) for s in ss], run_time=0.25)
        self.remove(*ss)

    def voos(self, pares, rt=1.0, arco=-0.6, extra=(), nota=""):
        """Termos que nascem de uma fonte: [(fonte, alvo)], TransformFromCopy em arco. A cópia voa só com o preenchimento (sem fantasma no pouso);
        a fonte fica como estava."""
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
        """F nasce: os glifos de `voos` = [(fonte, índices|chaves de F)] voam (TransformFromCopy) e o resto é escrito pela caneta, da esquerda
        para a direita, no mesmo play (a caneta começa `atraso` s depois)."""
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

    def gm(self, n, A, B, pares, voos=(), rt=1.2, copia=False, nota="", extra=(), atraso_caneta=0.15):
        """Glyph map n (handoff §3.4): A → B com TransformByGlyphMap (MF-Tools, mapa explícito, auto_fade só no que sai). Os glifos de B fora do
        mapa ficam apagados durante o mapa e depois voam da fonte (voos = [(fonte, chaves|índices em B)]) ou são escritos pela caneta."""
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
        snapA = A.copy() if copia else None            # com cópia, a linha de origem fica intacta (o MF-Tools às vezes leva glifos dela)
        ent_n = ent + ([(_Nada, novos)] if novos else [])          # o glifo que entra NÃO usa FadeIn: fica apagado e depois voa ou é escrito
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
                anims.append(TransformFromCopy(src_c, g_, path_arc=-0.6, run_time=1.0))
            resto = [i for i in novos if i not in voados]
            if resto:
                for i in resto:
                    B[0][i].become(orig[i])
                g_ = VGroup(*[B[0][i] for i in resto])
                g_._tex = B._tex + " (glifos novos)"
                g_._caneta, g_._esc, g_._em_caneta, g_._txt = True, False, False, None
                anims.append(caneta(g_, atraso=atraso_caneta if voos else 0.0, ritmo=CANETA_P / 0.30))
            tot = max([1.0 if voos else 0.0] + [a.tot for a in anims if isinstance(a, _Caneta)])
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
        """Restos do MF-Tools na cena (grupos de glifos de A ou de B soltos no topo): saem; B fica inteiro."""
        gs = {id(x) for x in A[0].submobjects} | {id(x) for x in B[0].submobjects}
        for m in list(self.mobjects):
            if m is A or m is B or getattr(m, "_tex", None) is not None or not isinstance(m, VMobject):
                continue
            fam = [x for x in m.get_family() if x is not m and len(x.points)]
            if (id(m) in gs) or (fam and all(id(x) in gs or any(id(y) in gs for y in x.get_family()) for x in fam)):
                self.remove(m)

    def acende_sai(self, *gs, cor=MEN, rt=0.6, rt_vis=0.8, volta=False):
        """Cancelamento em dois tempos: os glifos acendem (cor); o glyph map seguinte os tira. `volta`: depois de acender, voltam à cor
        (quando a linha velha fica na tela e só a nova não os leva)."""
        membros = [x for g_ in gs for x in g_.family_members_with_points() if isinstance(x, VMobject)]
        orig = [(x.get_fill_color(), x.get_fill_opacity(), x.get_stroke_color()) for x in membros]
        self.play(*[g_.animate.set_fill(cor, 1).set_stroke(cor) for g_ in gs], run_time=rt)
        if rt_vis:
            self.wait(rt_vis)
        if volta:
            alvo = []
            for x, (fc, fo, sc_) in zip(membros, orig):
                y = x.copy().set_fill(fc, fo).set_stroke(sc_)
                alvo.append(Transform(x, y))
            self.play(*alvo, run_time=rt)

    def chip_pena(self, cg, cf, cm_, **kw):
        """Escreve o chip (a fórmula pela caneta, a moldura junto) e deixa na cena só o grupo do chip (sai inteiro depois)."""
        self.pena(cf, extra=[Create(cm_)], **kw)
        self.remove(cf, cm_)
        pronto(cg)
        self.add(cg)
        return cg

    def velhos(self, *ms):
        """Grupo só com o que ainda está na cena (para a tela velha subir e sair sem ressuscitar o que um glyph map já tirou)."""
        vivos = []
        for m in ms:
            if m is None:
                continue
            if any(x in self.mobjects for x in m.get_family()):
                vivos.append(m)
        out = [m for m in vivos if not any(m is not o and m in o.get_family() for o in vivos)]
        return VGroup(*out)

    def sobe_sai(self, *ms, dy=0.5, rt=0.6, extra=()):
        """A tela velha sobe um pouco e sai (sem atravessar o que fica)."""
        g = self.velhos(*ms)
        if len(g):
            self.play(g.animate.shift(UP * dy).set_opacity(0), *extra, run_time=rt)
            self.remove(g)
        elif extra:
            self.play(*extra, run_time=rt)

    # coluna ----------------------------------------------------------------------------------------------
    def col(self, nome, *ms, chips=0):
        """Registra linhas na coluna `nome` (QA: ≤ 6 linhas por etapa, ≤ 8 com chips; folga do rodapé ≥ 40 px)."""
        c = self._col.setdefault(nome, {"linhas": [], "chips": 0, "max": 0, "base": 0})
        for m in ms:
            if m not in c["linhas"]:
                c["linhas"].append(m)
        c["chips"] = max(c["chips"], chips)
        vivos = [m for m in c["linhas"] if any(y in self.mobjects for y in m.get_family()) or any(m in x.get_family() for x in self.mobjects)]
        c["linhas"] = vivos
        base = max([pxof(m.get_bottom())[1] for m in vivos] or [0])
        c["max"] = max(c["max"], len(vivos))
        print(f"[coluna] {self.lote} {self._aid} {self.t:.2f} {nome} linhas={len(vivos)} chips={c['chips']} base={base:.0f} folga={1080 - base:.0f}")

    def col_zera(self, nome):
        if nome in self._col:
            self._col[nome]["linhas"] = []

    def dentro(self, painel_rect, *itens):
        """R6: estes itens não podem sair do painel (x0, y0, x1, y1) em px."""
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
        super().wait(duration, *a, **kw)
        self._em_wait = False
        if duration >= 0.5:
            print(f"[espera] {self.lote} {self._aid} {t0:.2f} {duration:.2f}")

    def _caixas(self):
        """Caixas de texto/fórmula/ponto visíveis (px): (nome, (x0, y0, x1, y1), obst, mob, voando). Desce a árvore e para no primeiro nó
        marcado (_txt ou _obst): o rótulo conta inteiro, uma vez."""
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

    def an(self, aid):
        """Abre a âncora e guarda os textos visíveis nesse instante (QA de linhas órfãs: o que ainda está na tela 4 s depois)."""
        super().an(aid)
        try:
            self._ini_ids = {id(c[3]): c[0] for c in self._caixas() if c[0] != "ponto" and not str(c[0]).startswith("3d:")}
        except Exception:
            self._ini_ids = {}
        self._orfa_chk = False

    def _qa_quadro(self, f):
        t = f / FPS
        caixas = self._caixas()
        if not getattr(self, "_orfa_chk", True) and (f - self._q0) / FPS >= 4.0:
            self._orfa_chk = True
            for c in caixas:
                if id(c[3]) in getattr(self, "_ini_ids", {}):
                    print(f"[orfa] {self.lote} {self._aid} {t:.2f}s {str(c[0])[:80]!r}")
        # R5: texto × texto e texto × ponto (inclusive durante animações); R5V: texto em voo × texto parado
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
        # R6: margem de 48 px e painel
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
        # 3D × canto: o eixo z (do centro ao topo da seta) não cruza o título do canto
        if self.h2 is not None and self.h2 in self.mobjects:
            hx0, hy0 = pxof(self.h2.get_corner(UL))
            hx1, hy1 = pxof(self.h2.get_corner(DR))
            for pal in self._palcos:
                if pal.fundo in self.mobjects and pal.fundo.op.get_value() > 0.5 and "eixoTopo" in P41[pal.cena]:
                    (xa, ya), (xb, yb) = pal.pt("eixoBase"), pal.pt("eixoTopo")
                    for u in np.linspace(0, 1, 40):
                        x, y = xa + (xb - xa) * u, ya + (yb - ya) * u
                        if hx0 - 6 <= x <= hx1 + 6 and hy0 - 6 <= y <= hy1 + 6:
                            print(f"[3dcanto] {self.lote} {self._aid} {t:7.2f}s eixo z de {pal.cena} cruza o canto")
                            break
        # palco vazio e grade (a cada segundo)
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
            tipo = "2D-grade" if grade else ("3D-liso" if tem3d else ("CTA-liso" if cta else "2D-SEM-GRADE"))
            canto2 = self.h2 is not None and self.h2 in self.mobjects
            print(f"[grade] {self.lote} {self._aid} {t:.0f} {tipo} canto2={'sim' if canto2 or cta or not self.CANTO else 'NAO'}")

    def fim(self):
        super().fim()
        print(f"[R5V-total] {self.lote} {len(self._r5v)}")
        for nome, c in self._col.items():
            print(f"[coluna-max] {self.lote} {nome} {c['max']} chips={c['chips']}")

    # utilidades ------------------------------------------------------------------------------------------
    def entra(self, *ms, rt=0.5, extra=()):
        """Desenho que nasce (Create para traço, FadeIn para imagem/3D)."""
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


# ── CTA (o do canal, liso e parado: sem anéis girando; handoff §7 "nada de laço contínuo") ─────────────────────
def cta41(cena, rt_fim=3.0):
    CL = P3(0, 0.9)
    logo = cena.logo(5.6).move_to(CL)
    aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(CL), num_dashes=48).set_stroke(GEO, 2.6, opacity=o) for r, o in ((2.1, 0.85), (2.45, 0.6))])
    sem_ctn(aneis)
    ins = VGroup(T("INSCREVA-SE PARA ACOMPANHAR", 960, 0, 66, "center", caneta=False), T("OS PRÓXIMOS VÍDEOS", 960, 0, 66, "center", caneta=False)
                 ).arrange(DOWN, buff=0.12).move_to(P3(0, -2.6))
    s4 = cena.snap()
    sai_c = [m_ for m_ in (cena.h2, cena.h1) if m_ is not None and m_ in cena.mobjects]
    cena._cta = True
    cena.play(*[(m_.op.animate.set_value(0.0) if isinstance(m_, Fundo3D) else FadeOut(m_)) for m_ in s4 + sai_c], run_time=0.4)     # D5: o S2 sai ANTES do CTA entrar
    cena.play(FadeIn(logo, scale=0.96), FadeIn(aneis), FadeIn(ins, shift=0.1 * UP), run_time=0.5)
    for m_ in s4:
        m_.clear_updaters()
    cena.remove(*s4, *sai_c)
    cena.h2 = None
    cena.grade = None
    print(f"[cta] {cena.lote} {cena.t:.2f}")
    cena.wait(cena.resta() + rt_fim)


def legq(cor, s, x, y, size=30):
    """Legenda colorida do v3 (G4): quadradinho na cor + texto Space Grotesk 30 px (o texto começa em x + 30). Devolve (quadrado, texto)."""
    sq = ret_px(x, y - 9, x + 18, y + 9, fill=cor, fop=1.0, stroke=None, z=6)
    t = leg(s, x + 30, y, cor, "left", size)
    return sq, t


def painel2d41(X0, Y0, w, h, passo=30):
    """`painel2d` do sb41 (handoff v2 §2): painel opaco #16123A com cantos de 14 px, grade PRÓPRIA de 30 px em #2B2558 e borda GEO a 45 %.
    Cobre o papel e o 3D por baixo (nada do 3D aparece atrás). Devolve um VGroup (moldura opaca + linhas da grade)."""
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
    """Desenho 2D dentro de um painel2d41: origem em (cx, cy) px, u px por unidade, y para cima. Peças por px (lin_px, seta_px, ponto_px)."""

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
        """Arco de raio R (unidades de tela, px) em volta da origem, de a0 a a1 (rad, anti-horário, y para cima)."""
        pts = [(self.cx + R * math.cos(a0 + (a1 - a0) * k / n), self.cy - R * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]
        return lin_px(pts, cor, wpx, z=6)


def _fio(self, pal, nome, rot, cor=GEO, folga=26):
    """Fio-guia fino (2 px) do ponto 3D `nome` até a placa do rótulo `rot` (v3 §3.4: placa fora da célula, fio até a aresta). Sempre redesenhado."""
    def f():
        x, y = pal.pt(nome)
        X, Y = pxof(rot.get_center())
        d = math.hypot(X - x, Y - y)
        if d < folga + 6:
            return lin_px([(x, y), (x + .01, y)], cor, 2, 0.0, z=5)
        k = (d - folga) / d
        return lin_px([(x, y), (x + (X - x) * k, y + (Y - y) * k)], cor, 2, .85, z=5)
    return always_redraw(f)


B41.fio = _fio


def legm(cor, tex, x, y, size=36):
    """Legenda colorida com fórmula (G4): quadradinho na cor + MathTex a 30 px do quadrado. `.f` é a fórmula (fonte de voos)."""
    sq = ret_px(x, y - 9, x + 18, y + 9, fill=cor, fop=1.0, stroke=None, z=6)
    f = TC(tex, x + 30, y, size, "l")
    g = VGroup(sq, f)
    g.f = f
    g._txt = tex
    return g


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
_B = B41
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


# ── R2 (final): registro dos tamanhos pedidos (o QA mede a altura real em px: x ≈ 0,43·tam, algarismo ≈ 0,66·tam, a 1080p) ─────────────────────
_CTX = {"lote": "?", "aid": "?"}
_TAM = []
_TC_ORIG, _T_ORIG, _LEG_ORIG = TC, T, leg


def TC(s, x=960, y=540, size=48, al="l", caneta=True):                      # noqa: F811
    # R2: fórmula curta nunca abaixo de 36 (rótulos de eixo, pontos); anotação "= 1" sob a chave: 30; linhas densas (> 40 caracteres) ficam como estão
    if size < 36 and len(str(s)) <= 40:
        size = 30 if str(s).startswith("=\,") else 36
    _TAM.append(("F", _CTX["aid"], size, str(s)[:60]))
    return _TC_ORIG(s, x, y, size, al, caneta)


def T(s, x, y, size=30, al="left", cor=BR, bold=True, caneta=True):          # noqa: F811
    _TAM.append(("T", _CTX["aid"], size, str(s)[:60]))
    return _T_ORIG(s, x, y, size, al, cor, bold, caneta)


def leg(s, x, y, cor=GEO, al="left", size=28, caneta=True):                   # noqa: F811
    _TAM.append(("T", _CTX["aid"], max(26, size), str(s)[:60]))
    return _LEG_ORIG(s, x, y, cor, al, size, caneta)


_an_tam0, _fim_tam0 = B41.an, B41.fim


def _an_tam(self, aid):
    _CTX["lote"], _CTX["aid"] = self.lote, aid
    return _an_tam0(self, aid)


def _fim_tam(self):
    for k, a, sz, tx in _TAM:
        print(f"[tam] {self.lote} {a} {k} {sz} {tx!r}")
    return _fim_tam0(self)


B41.an, B41.fim = _an_tam, _fim_tam
