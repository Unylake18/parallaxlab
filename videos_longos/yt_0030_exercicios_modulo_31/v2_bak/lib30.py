"""yt_0030 · CÁLCULO III · EP. 04 · Exercícios do módulo 3.1 — acréscimos do sb30.html (handoff v1) sobre a biblioteca do yt_0028 (v30.py = cópia
do v28.py; kit.py = cópia do kit do yt_0028). Tudo em px de 1080p (PX, T, TC, legenda); 1 u do Manim = 120 px.

Peças novas: macros (\\Uu, \\Vv, \\vv, \\ww, \\ff, \\Hh, \\B, \\Gg, \\Z, \\R), campos e fluxos exatos do §3, seta proporcional com teto (campoP30),
quadradinho pelo fluxo (Pedaco com 30 pontos por lado + fantasma), seta curva de giro (giro30), chip PAUSE E TENTE (relógio da cena),
linhas recortadas na moldura (R7), mapa de glifos por pedaços de TeX (Pz + tbgm30) e o registro das 10 tags."""
from v30 import *  # noqa: F401,F403
from v30 import _cabe_px, _rate_trecho, _cor_seta, _caixa_px  # noqa: F401

# ── macros do sb30 (o \B do vídeo é menta; \Z é menta-claro) ──
TEX27.add_to_preamble(
    r"\def\Uu{\textcolor{ca}{u}}\def\Vv{\textcolor{cm}{v}}\def\vv{\textcolor{cc}{\vec v}}\def\ww{\textcolor{cc}{\vec w}}"
    r"\def\ff{\textcolor{cc}{\vec f}}\def\Hh{\textcolor{cc}{\vec H}}\def\B{\textcolor{cc}{\vec B}}\def\Gg{\textcolor{cc}{\vec G}}"
    r"\def\Z{\textcolor{ce}{z}}\def\R{\textcolor{cc}{R}}\definecolor{cb}{HTML}{267BFF}")

SAIC = "#7FB2FF"            # div (azul-claro)
BR = "#F5F7FF"
SQ2 = math.sqrt(2)
LA = (120, 180, 1080, 900)                          # palco do layout A
BE, BD = (120, 180, 840, 900), (1080, 180, 1800, 900)
CC = [(120, 300, 600, 780), (720, 300, 1200, 780), (1320, 300, 1800, 780)]
VA = Vista(600, 540, 120)


# ── logo do canto: logo_crop.png 240×85 em (1650, 24) ──
_setup0 = Base.setup_base


def _setup30(self):
    _setup0(self)
    novo = ImageMobject(str(AQUI / "referencia_v1" / "logo_crop.png")).set_width(240 / 120).move_to(PX(1650 + 120, 24 + 42.5)).set_z_index(40)
    if self.wm in self.mobjects:
        self.remove(self.wm)
        self.add(novo)
    self.wm = novo
    self._chips = []


Base.setup_base = _setup30


# ── campos (handoff §3.1) ──
def F1(x, y):
    return (x + y, x - y)


def F2(x, y):
    return (1.0 + 0 * x, x - y)


def F3(x, y):
    return (x * x - y * y, 2 * x * y)


def VORTA(a):
    def f(x, y):
        k = (x * x + y * y) ** (-a)
        return (-y * k, x * k)
    return f


def EXPLA(a):
    def f(x, y):
        k = (x * x + y * y) ** (-a)
        return (x * k, y * k)
    return f


def F4(x, y):
    r2 = x * x + y * y
    if np.ndim(r2) == 0:
        if r2 < 1e-12:
            return (0.0, 0.0)
        k = x * y / r2
        return (k * x, k * y)
    k = x * y / np.where(r2 < 1e-12, 1.0, r2)
    return (k * x, k * y)


def RIO(x, y):
    return (0.0 * x, 1 - x * x / 9)


# ── fluxos exatos (§3.2): fl(x, y, t) com arrays ──
def fl1(x, y, t):
    c, s = np.cosh(SQ2 * t), np.sinh(SQ2 * t) / SQ2
    return c * x + s * (x + y), c * y + s * (x - y)


def fl2(x, y, t):
    return x + t, x + t - 1 + (y - x + 1) * np.exp(-t)


def fl3(x, y, t):
    dr, di = 1 - t * x, -t * y
    d = dr * dr + di * di
    return (x * dr + y * di) / d, (y * dr - x * di) / d


def flV(a):
    def f(x, y, t):
        r = np.hypot(x, y)
        th = r ** (-2 * a) * t
        c, s = np.cos(th), np.sin(th)
        return c * x - s * y, s * x + c * y
    return f


def flRio(x, y, t):
    return x + 0 * y, y + (1 - x * x / 9) * t


def fl4(x, y, t, dt=0.01):
    """F₄ não tem forma fechada: RK4 com dt = 0,01 (handoff §3.2)."""
    x, y = np.array(x, float), np.array(y, float)
    n = max(1, int(round(abs(t) / dt)))
    h = t / n
    for _ in range(n):
        k1 = F4(x, y)
        k2 = F4(x + h / 2 * k1[0], y + h / 2 * k1[1])
        k3 = F4(x + h / 2 * k2[0], y + h / 2 * k2[1])
        k4 = F4(x + h * k3[0], y + h * k3[1])
        x = x + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y = y + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return x, y


def ponto_fl(fl, c, t):
    a, b = fl(np.array([c[0]], float), np.array([c[1]], float), t)
    return (float(a[0]), float(b[0]))


# ── seta proporcional com teto (sb30 campoP): L = lmax·min(1, |F|/mref); < 6 px não é desenhada ──
REDES = []                 # redes de setas criadas (para reagrupar depois de um cresce_campo, que solta as setas na cena)


def campoP30(v, Fv, x0=-3.5, x1=3.5, y0=-3, y1=3, passo=.5, rmin=.3, mref=1.0, ctx=False, skip=None, nome="campoP"):
    g = Campo7()
    g._cor = None
    lmax = .84 * passo
    n = int(math.floor((x1 - x0) / passo + 1e-6))
    m = int(math.floor((y1 - y0) / passo + 1e-6))
    for i in range(n + 1):
        for j in range(m + 1):
            X, Y = x0 + i * passo, y0 + j * passo
            if math.hypot(X, Y) < rmin or (skip and skip(X, Y)):
                continue
            f = Fv(X, Y)
            mm = math.hypot(float(f[0]), float(f[1]))
            if mm < 1e-9:
                continue
            L = lmax * min(1.0, mm / mref)
            if L * v.u < 6:
                continue
            u = (f[0] / mm * L, f[1] / mm * L)
            t = min(1.0, mm / mref)
            c = ManimColor(CTX) if ctx else mix(CAMPO, CAMPO2, t)
            s = seta7(v.c2p(X - u[0] / 2, Y - u[1] / 2), v.c2p(X + u[0] / 2, Y + u[1] / 2), c, 5, 19)
            if not _cabe_px(s.get_start(), s.get_end()):
                continue
            s._xy, s._L, s._t, s._f = (X, Y), L, t, f
            g.add(s)
    g._v, g._passo = v, passo
    REDES.append(g)
    if len(g):
        c = celula(v.u)
        res = max(max(abs((X * v.u) / c - round(X * v.u / c)) * c, abs((Y * v.u) / c - round(Y * v.u / c)) * c) for X, Y in (s._xy for s in g))
        print(f"[alinha-setas] {nome} | origem ({v.cx:.0f}, {v.cy:.0f}) {v.u:g} px/u, quadradinho {c:g} px | {len(g)} setas | resíduo {res:.2f} px")
        g.log(nome, passo)
    return g.set_z_index(3)


def campo30(v, Fv, *a, **k):
    g = campo28(v, Fv, *a, **k)
    REDES.append(g)
    return g


def _reagrupa(cena):
    """Rede cujas setas estão todas soltas na cena (depois de cresce_campo/LaggedStart) volta a entrar como grupo."""
    ms = cena.mobjects
    ids = {id(m) for m in ms}
    for g in REDES:
        if id(g) in ids or not len(g.submobjects):
            continue
        soltas = [x for x in g.submobjects if id(x) in ids]
        if soltas and len(soltas) == len(g.submobjects):
            cena.remove(*soltas)
            cena.add(g)


def recolore(cena, setas, ctx_fn, rt=0.4, cor=None):
    """Cor de cada seta para o contexto (ctx_fn(s) verdadeiro) ou de volta à cor da intensidade; o grupo animado é a rede (que está na cena)."""
    setas = list(setas)
    ini = [ManimColor(s.haste.get_stroke_color()) for s in setas]
    fim = [_cor_seta(s._t, bool(ctx_fn(s)), cor) for s in setas]
    dono = next((g for g in REDES if setas and setas[0] in g.submobjects), VGroup(*setas))

    def f(m, a):
        for s, c0, c1 in zip(setas, ini, fim):
            c = interpolate_color(c0, c1, a)
            s.haste.set_stroke(c)
            s.ponta.set_fill(c).set_stroke(c)
    return UpdateFromAlphaFunc(dono, f, run_time=rt)


def por_colunas(g, rt=1.0):
    """A rede entra por colunas, da esquerda para a direita."""
    return cresce_campo(g, rt, chave=lambda s: (s._xy[0], s._xy[1]))


# ── quadradinho de fluido (§2.7): imagem exata pelo fluxo, 30 pontos por lado, malha 4×4, fantasma tracejado ──
def quad30(v, c, s, z=7):
    return Pedaco(v, quad_pts(c, s), n=4, k=30, z=z)


def clar_ped(ped, m=.25):
    return clarPoly(ped.poly(), m)


def dq(c, s, m=.15):
    return clarPoly(quad_pts(c, s), m)


def borda_fl(fl, c, s, t, n=6):
    """Pontos da borda do quadradinho levado pelo fluxo até t (para a clareira fixa do estado final)."""
    q = np.array(ret_pts(c, s, n))
    a, b = fl(q[:, 0], q[:, 1], t)
    return [(float(p), float(r)) for p, r in zip(np.asarray(a) * np.ones(len(q)), np.asarray(b) * np.ones(len(q)))]


# ── seta curva de giro (§2.7): violeta 4 px, ponta 18 px, ~110° em volta do centro; ccw = anti-horário ──
def giro30(v, c, r, ccw=True, cor=VIO, w=4, head=18, a0=None, a1=None):
    if a0 is None:
        a0, a1 = (-.15, 1.75) if ccw else (1.75, -.15)
    hl = head / v.u                                   # comprimento da ponta, em unidades do plano
    da = hl / r * (1 if ccw else -1)
    pts = circ_pts(r, c, 40, a0, a1 - da * 0.7)
    arco = vlinha(v, pts, cor, w)
    B = np.array([c[0] + r * math.cos(a1), c[1] + r * math.sin(a1)])
    d = np.array([-math.sin(a1), math.cos(a1)]) * (1 if ccw else -1)
    n = np.array([-d[1], d[0]])
    base = B - d * hl
    tri = Polygon(v.c2p(*B), v.c2p(*(base + n * hl * 0.5)), v.c2p(*(base - n * hl * 0.5))).set_fill(cor, 1).set_stroke(cor, 1, 1)
    tri._sem_contorno = True
    g = VGroup(arco, tri).set_z_index(9)
    g._giro = (c, r)
    return g


# ── PAUSE E TENTE (§2.6): chip no canto inferior direito, FadeIn 0,3 s · ≈ 3 s · FadeOut 0,3 s pelo relógio da cena (não segura a cena) ──
REG_PAUSA = []


class Chip(VGroup):
    def __init__(self, texto="PAUSE E TENTE"):
        t = T(texto, 0, 1010, 30)
        w = t.width * 120
        x1 = 1880
        x0 = x1 - w - 44
        t.shift(RIGHT * (PX(x0 + 22, 0)[0] - t.get_left()[0]))
        r = RoundedRectangle(width=(w + 44) / 120, height=62 / 120, corner_radius=10 / 120).move_to(PX((x0 + x1) / 2, 968 + 31))
        r.set_fill(PLACA_V4, 0.9).set_stroke(GEO, 2 / 1.2, 1)
        r._sem_contorno, r._placa = True, True
        super().__init__(r, t)
        self.r, self.t = r, t
        self.set_z_index(45)
        t.set_z_index(46)

    def op(self, o):
        self.r.set_fill(PLACA_V4, 0.9 * o).set_stroke(GEO, 2 / 1.2, o)
        self.t.set_fill(opacity=o)
        return self


def _pausa(self, dur=3.0, texto="PAUSE E TENTE"):
    ch = Chip(texto)
    t0 = self.clk.get_value()
    fim = t0 + 0.3 + dur + 0.3

    def upd(m):
        tt = self.clk.get_value() - t0
        o = tt / 0.3 if tt < 0.3 else (1.0 if tt < 0.3 + dur else max(0.0, 1 - (tt - 0.3 - dur) / 0.3))
        m.op(max(0.0, min(1.0, o)))
    ch.add_updater(upd)
    upd(ch)
    self.add(ch)
    self._chips.append((ch, fim))
    print(f"[pausa] {self.lote} {self._aid} {t0:.2f} {fim:.2f}")
    return ch


def _limpa_chips(self):
    agora = self.clk.get_value()
    for ch, fim in list(self._chips):
        if agora >= fim + 0.05:
            ch.clear_updaters()
            self.remove(ch)
            self._chips.remove((ch, fim))


_fixos0 = Base.fixos


def _fixos30(self):
    return _fixos0(self) | {c for c, _ in getattr(self, "_chips", [])}


_play30, _wait30 = Base.play, Base.wait


def _play_c(self, *a, **k):
    _limpa_chips(self)
    r = _play30(self, *a, **k)
    _reagrupa(self)
    return r


def _wait_c(self, *a, **k):
    _limpa_chips(self)
    return _wait30(self, *a, **k)


Base.pausa, Base.fixos, Base.play, Base.wait = _pausa, _fixos30, _play_c, _wait_c


# ── R7: linhas auxiliares recortadas na moldura (Liang–Barsky em px); registro para a checagem quadro a quadro ──
def _clip(p, q, b):
    x0, y0, x1, y1 = b
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if abs(pp) < 1e-12:
            if qq < 0:
                return None
            continue
        r = qq / pp
        if pp < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return None
    return (p[0] + t0 * dx, p[1] + t0 * dy), (p[0] + t1 * dx, p[1] + t1 * dy)


def linha_rec(v, pts, box, cor=GEO, w=2, alpha=1.0, dash=None, folga=None, z=5):
    """Polilinha do plano recortada no retângulo `box` (px), recuado `folga` px (padrão: meia espessura + 1,5 px)."""
    f = (w / 2 + 1.5) if folga is None else folga
    b = (box[0] + f, box[1] + f, box[2] - f, box[3] - f)
    P = [canto_xy(v, *p) for p in pts]
    runs, cur = [], []
    for p, q in zip(P, P[1:]):
        c = _clip(p, q, b)
        if c is None:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
            continue
        a, bb = c
        if not cur:
            cur = [a, bb]
        elif math.hypot(cur[-1][0] - a[0], cur[-1][1] - a[1]) < 1e-6:
            cur.append(bb)
        else:
            runs.append(cur)
            cur = [a, bb]
        if math.hypot(bb[0] - q[0], bb[1] - q[1]) > 1e-6:
            runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    g = VGroup()
    for r in runs:
        if sum(math.hypot(r[i + 1][0] - r[i][0], r[i + 1][1] - r[i][1]) for i in range(len(r) - 1)) < 2:
            continue
        g.add(linha7([PX(*p) for p in r], cor, w, alpha, dash))
    g._linha_box = box
    return g.set_z_index(z)


def _r7_linhas(self):
    """R7 das linhas recortadas (e de tudo com _linha_box): nenhum ponto visível fora da moldura (+0,5 px)."""
    for mob in self.mobjects:
        for x in mob.get_family():
            b = getattr(x, "_linha_box", None)
            if b is None:
                continue
            c = _caixa_px(x)
            if c is None:
                continue
            fora = max(b[0] - c[0], c[2] - b[2], b[1] - c[1], c[3] - b[3])
            if fora > 0.5:
                self._r7l_n = getattr(self, "_r7l_n", 0) + 1
                if self._r7l_n <= 30:
                    print(f"[r7l] {self._aid} {self.t:7.2f}s linha auxiliar passa {fora:.1f} px da moldura {b}")


_upd30 = Base.update_to_time


def _update30(self, t):
    _upd30(self, t)
    if getattr(self, "_em_play", False):
        _r7_linhas(self)


Base.update_to_time = _update30
_fim30 = Base.fim


def _fim30b(self):
    _fim30(self)
    print(f"[r7l-total] {self.lote} {getattr(self, '_r7l_n', 0)} quadros com linha auxiliar fora da moldura")


Base.fim = _fim30b


# ── texto com placa (txt placa=true do sb30) ──
def TXP30(s, x, y, size=26, al="center", cor=BR, bold=False, up=True):
    t = T(s, x, y, size, al, cor, bold=bold, up=up)
    g = VGroup(placa7(t, 8, 4), t)
    g.f = t
    return g


# ── matemática por pedaços: o MathTex é a concatenação dos pedaços; cada pedaço sabe os seus glifos (para o TransformByGlyphMap) ──
_NG = {}


def _nglifos(p):
    if p not in _NG:
        try:
            _NG[p] = len(MathTex(p, tex_template=TEX27)[0])
        except Exception:
            _NG[p] = -1
    return _NG[p]


def Pz(pecas, x=1120, y=540, size=42, al="l", caneta=True):
    """MathTex de string única = "".join(pecas); m._rg[i] = range dos glifos do pedaço i (conferido: a soma tem de bater com o total)."""
    m = TC("".join(pecas), x, y, size, al, caneta=caneta)
    ns = [_nglifos(p) for p in pecas]
    tot = len(m[0])
    if any(n < 0 for n in ns) or sum(ns) != tot:
        print(f"[pz] AVISO pedaços não somam: {ns} soma {sum(ns)} × total {tot} :: {''.join(pecas)!r}")
        m._rg = None
    else:
        k, rg = 0, []
        for n in ns:
            rg.append(list(range(k, k + n)))
            k += n
        m._rg = rg
    m._pecas = list(pecas)
    return m


def tbgm30(a, b, pares, rt=1.4, copia=False):
    """TransformByGlyphMap por pedaços: pares = [(pedaços de a, pedaços de b)] (índices de pedaço, int ou lista). O resto some/entra (auto_fade)."""
    if a._rg is None or b._rg is None:
        print(f"[pz] sem mapa de glifos: {a._tex!r} → {b._tex!r}; vai por TransformMatchingShapes")
        ja_escrita(b)
        return TransformMatchingShapes(a.copy() if copia else a, b, run_time=rt)
    mp = []
    for ia, ib in pares:
        ia = [ia] if isinstance(ia, int) else ia
        ib = [ib] if isinstance(ib, int) else ib
        ga = [g for i in ia for g in a._rg[i]]
        gb = [g for i in ib for g in b._rg[i]]
        mp.append((ga, gb))
    return tbgm(a, b, *mp, rt=rt, copia=copia)


def troca_linha(cena, velho, novo, rt=0.4):
    """Troca de legenda/linha no mesmo lugar: FadeOut + FadeIn 0,4 s no mesmo play."""
    cena.play(FadeOut(velho), FadeIn(novo), run_time=rt)
    cena.remove(velho)


def acende(objs, cor, rt=0.3):
    return [m.animate.set_color(cor) for m in objs]


def num_txt(s, x, y, size=34, cor=BR, placa=True):
    """Número circulado (①…④) do sb30: txt com placa, centrado em (x, y_baseline)."""
    return TXP30(s, x, y, size, "center", cor, bold=True)


# ── costura entre lotes (R10): o lote termina no fim da fala e só então tudo sai em 0,4 s (a linha 2 do canto também); a montagem sobrepõe
#    esses 0,4 s à entrada do lote seguinte (composição aditiva sobre o fundo), então o layout novo entra enquanto o antigo sai. ──
COSTURA = 0.4


def _sai_fim30(self, rt=COSTURA):
    if self._aid is not None:
        self._fecha()
    sai = self.snap() + [m for m in (self.h2,) if m is not None] + [c for c, _ in self._chips]
    if sai:
        _play30(self, *[FadeOut(m) for m in sai], run_time=rt)
    for m in sai:
        m.clear_updaters()
    self.remove(*sai)
    self.h2 = None
    self._chips = []
    print(f"[costura] {self.lote} saída de {rt:.2f} s depois do fim da fala")


Base.sai_fim = _sai_fim30


def troca(cena, nome):
    """Registro de troca de layout (transicoes_v1.txt)."""
    print(f"[troca] {cena.lote} {cena._aid} {cena.t:.2f} {nome}")


# ── rede viva: as setas são recalculadas a partir de um parâmetro (α do redemoinho) só durante a troca (ValueTracker / UpdateFromAlphaFunc) ──
def seta_pontos(s, a, b, cor=None, head=19):
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = float(np.linalg.norm(b - a))
    if L < 1e-4:
        b = a + np.array([1e-3, 0, 0])
        L = 1e-3
    d = (b - a) / L
    n = np.array([-d[1], d[0], 0.0])
    tl = min(head / 120, 0.45 * L)
    base = b - tl * d
    s.haste.put_start_and_end_on(a, base + 0.3 * tl * d)
    s.ponta.set_points_as_corners([b, base + 0.5 * tl * n, base - 0.5 * tl * n, b])
    if cor is not None:
        s.haste.set_stroke(cor)
        s.ponta.set_fill(cor).set_stroke(cor)
        s._cor = cor


class CampoVivo(Campo7):
    """Setas centradas nos pontos `pts`; em(p): campo Fp(p), comprimento comprimido com mmax_p(p) (ou proporcional com teto mref_p)."""

    def __init__(self, v, pts, Fp, mmax_p, passo=.5, p0=0.0, prop=False, nome="campo vivo"):
        super().__init__()
        self._cor = None
        self.v, self.Fp, self.mm, self.passo, self.prop = v, Fp, mmax_p, passo, prop
        for X, Y in pts:
            s = seta7(v.c2p(X - .1, Y), v.c2p(X + .1, Y), CAMPO, 5, 19)
            s._xy, s._t, s._f, s._L = (X, Y), 0.0, (1, 0), .1
            self.add(s)
        self._v, self._passo = v, passo
        REDES.append(self)
        self.em(p0)
        self.set_z_index(3)
        print(f"[campo] {nome}: {len(self)} setas (rede viva)")

    def em(self, p):
        F, mm = self.Fp(p), self.mm(p)
        lmax = .84 * self.passo
        for s in self.submobjects:
            X, Y = s._xy
            f = F(X, Y)
            m = math.hypot(float(f[0]), float(f[1]))
            if m < 1e-12:
                f, m = (1e-6, 0.0), 1e-6
            t = min(1.0, m / mm)
            L = lmax * t if self.prop else lmax * (.4 + .6 * t)
            u = (f[0] / m * L, f[1] / m * L)
            seta_pontos(s, self.v.c2p(X - u[0] / 2, Y - u[1] / 2), self.v.c2p(X + u[0] / 2, Y + u[1] / 2),
                        _cor_seta(t, getattr(s, "_ctx", False), None))
            s._t, s._f, s._L = t, f, L
        self.p = p
        return self


def troca_p(cmp, p1, rt=1.0, rate=smooth):
    p0 = cmp.p
    return UpdateFromAlphaFunc(cmp, lambda m, a: m.em(p0 + (p1 - p0) * rate(a)), run_time=rt)


def interp_tab(tab):
    """Função linear por partes a partir de [(p, valor)]."""
    def f(p):
        if p <= tab[0][0]:
            return tab[0][1]
        for (a, va), (b, vb) in zip(tab, tab[1:]):
            if p <= b:
                return va + (vb - va) * (p - a) / (b - a)
        return tab[-1][1]
    return f


def gira_setas(cmp, ang, rt=1.2):
    """Cada seta gira `ang` em torno do PRÓPRIO centro (todas juntas)."""
    return AnimationGroup(*[Rotate(s, ang, about_point=cmp._v.c2p(*s._xy)) for s in cmp], run_time=rt)


def caixa_em(m, pad=6, cor=BR, w=2):
    r = Rectangle(width=m.width + 2 * pad / 120, height=m.height + 2 * pad / 120).move_to(m.get_center())
    r.set_stroke(cor, w / 1.2, 1).set_fill(opacity=0)
    r._sem_contorno = True
    return r.set_z_index(26)


def rotulo_tex(tex, x, y_base, size=32, cor=BR):
    """Rótulo em TeX no lugar de um txt do sb30 com símbolo que a Space Grotesk não tem (α, ε, δ, φ, ↺): centro vertical na meia altura das maiúsculas."""
    m = TC(tex, x, y_base - size * 0.36, size, "c", caneta=False)
    m.set_color(cor) if cor else None
    return m


# ── R7: cada seta lembra a chapa para a qual foi construída (na troca de layout as chapas velha e nova coexistem por 0,4 s) ──
import v30 as _v30  # noqa: E402


def _box_px(pa, pb):
    A = (pa[0] * 120 + 960, 540 - pa[1] * 120)
    B = (pb[0] * 120 + 960, 540 - pb[1] * 120)
    c = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    return next((p for p in ATIVAS if p[0] - 40 < c[0] < p[2] + 40 and p[1] - 40 < c[1] < p[3] + 40), None)


_sc30, _sp30 = _v30.seta_campo, _v30.seta_prop


def _seta_campo_b(v, X, Y, f, lmax, mmax, ctx=False, cor=None, w=5, head=19):
    s = _sc30(v, X, Y, f, lmax, mmax, ctx, cor, w, head)
    if s is not None:
        s._box = _box_px(s.get_start(), s.get_end())
    return s


_v30.seta_campo = _seta_campo_b
seta_campo = _seta_campo_b
_c7 = Campo7.add


def _add_box(self, *ms):
    for m in ms:
        if hasattr(m, "_xy") and not hasattr(m, "_box"):
            m._box = _box_px(m.get_start(), m.get_end())
    return _c7(self, *ms)


Campo7.add = _add_box


def _r7_chk30(self):
    chapas = [m for m in self.mobjects if getattr(m, "_chapa", False)]
    self._r7_q = getattr(self, "_r7_q", 0) + 1
    vivos = {m._box for m in chapas}
    if not vivos:
        return
    vistos = set()
    for mob in self.mobjects:
        for x in mob.get_family():
            if not (hasattr(x, "_xy") and hasattr(x, "haste")) or id(x) in vistos:
                continue
            vistos.add(id(x))
            if x.haste.get_stroke_opacity() < 0.95 or getattr(x, "_escondida", False):
                continue
            b = getattr(x, "_box", None)
            if b is None or b not in vivos:
                continue
            c = _caixa_px(x)
            if c is None:
                continue
            folga = min(c[0] - b[0], b[2] - c[2], c[1] - b[1], b[3] - c[3])
            if folga < 18 - 0.5:
                self._r7_n = getattr(self, "_r7_n", 0) + 1
                if self._r7_n <= 60:
                    print(f"[r7] {self._aid} {self.t:7.2f}s seta de campo em {tuple(round(float(v), 2) for v in x._xy)}: {folga:.1f} px da moldura {b}")


_v30._r7_chk = _r7_chk30


# ── canto com número circulado (O DESAFIO · CAMPO ①): a Space Grotesk não tem ①; o número é desenhado (num_circ) ──
def _canto_mob(self, s, n=None):
    t = txt(s, 21.6, color="#F5F7FF", bold=True)
    if n is not None:
        c = num_circ(n, "#F5F7FF", 36)
        c.next_to(t, RIGHT, buff=10 / 120)
        c.set_y(t[0].get_center()[1] if len(t) else t.get_center()[1])
        t = VGroup(t, c)
        t.submobjects_base = True
    return self._canto(t, CANTO_Y2, topo_min=self._y1_fim_px() + 10)


def _secao_n(self, s, n=None):
    """secao() com número circulado; mesma regra do yt_0028 (no começo do lote a troca vai junto da 1ª entrada)."""
    novo = _canto_mob(self, s, n)
    if not self.snap() and self.h2 is not None:
        velho = self.h2
        self.h2 = novo
        self._junto = getattr(self, "_junto", []) + [("out", velho, 0.0, 0.25), ("in", self.h2, 0.25, 0.6)]
        return
    if self.h2 is not None:
        self.play(FadeOut(self.h2), run_time=0.25)
        self.remove(self.h2)
    self.h2 = novo
    self._pend.append(FadeIn(self.h2))


Base.secao_n = _secao_n


def celulas(J):
    """Glifos de cada célula de uma matriz 2×2 num MathTex: ({(i, j): VGroup}, VGroup do resto: 'J =' e parênteses)."""
    (pl, pr), c1, c2, antes = colunas_matriz(J)
    out = {}
    for j, col in enumerate((c1, c2)):
        ys = [g.get_center()[1] for g in col]
        mid = (max(ys) + min(ys)) / 2
        out[(0, j)] = VGroup(*[g for g in col if g.get_center()[1] > mid])
        out[(1, j)] = VGroup(*[g for g in col if g.get_center()[1] <= mid])
    return out, VGroup(pl, pr, *antes)


def junta_partes(cena, m):
    """Depois de escrever um MathTex por partes (caneta/voo de grupos de glifos), troca os grupos soltos pelo MathTex inteiro."""
    ids = {id(g) for g in m[0].submobjects}
    cena.remove(*[x for x in cena.mobjects if isinstance(x, VGroup) and len(x.submobjects) and all(id(g) in ids for g in x.submobjects)])
    cena.add(m)


def sub_pz(m, *ii):
    return VGroup(*[m[0][g] for i in ii for g in m._rg[i]])


def angulos_quinas(ped):
    """Ângulo interno (graus) em cada uma das 4 quinas do polígono do pedaço (30 pontos por lado)."""
    k = len(ped.XY) // 4
    P = ped.XY
    out = []
    for c in range(4):
        i0, i1 = c * k - 1, c * k              # o fim do lado anterior e o começo do seguinte (o mesmo ponto)
        a = P[i0 - 1] - P[i0]
        b = P[(i1 + 1) % len(P)] - P[i1]
        out.append(math.degrees(math.acos(max(-1, min(1, float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))))))))
    return out
