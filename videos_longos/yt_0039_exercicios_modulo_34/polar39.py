"""yt_0037 · peças do vídeo sobre o p39.py: subtítulo do canto (terceira linha, sempre presente desde o 1º quadro quando o lote o declara),
cartão √π ? do canto (H2 → B6-2), desenho polar em px (setor, arco, grade de círculos e raios, disco), segmentos de cadeia `= … = …`
(cada degrau é um MathTex de string única; o glyph map vai de um degrau ao seguinte com from_copy), e o registro de glyph maps/contas para o QA."""
from p39 import *  # noqa: F401,F403
import lib39 as _lib

TAU_ = 2 * math.pi


# ── canto: subtítulo (terceira linha) ───────────────────────────────────────────────────────────────────────────────────────
def _setup37(self):
    _setup_b37(self)
    self.st = None
    self.cart = None
    if getattr(self, "SUB", None):
        self.st = T(self.SUB, 36, 160, 26, "left", CANTO_S, bold=False, caneta=False).set_z_index(40)
        self.st._s = self.SUB
        self.add(self.st)
    self.cart_ok = None
    if getattr(self, "CARTAO", False):
        self.cart = cartao_raiz()
        for m in self.cart.get_family():
            m._esc = True
        self.add(self.cart)
        if getattr(self, "CARTAO_OK", False):           # v2: o √π do canto já ganhou ✓ (B6-2) e fica até o S1
            self.cart_ok = check_px(0, 0, MEN, .7)
            self.cart_ok.move_to(PX(pxof(self.cart.get_left())[0] - 30, 155))
            self.cart_ok._esc = True
            self.add(self.cart_ok)


_setup_b37 = B39.setup_base
B39.setup_base = _setup37


def _subt(self, s, rt=0.15):
    """Troca o subtítulo do canto: o velho sai (0,15 s) e só depois o novo entra (0,15 s)."""
    velho = getattr(self, "st", None)
    if velho is not None and getattr(velho, "_s", None) == s:
        return
    if velho is not None:
        self.st = None
        velho._canto = True
        self.play(FadeOut(velho), run_time=rt)
        self.remove(velho)
    if s:
        novo = T(s, 36, 160, 26, "left", CANTO_S, bold=False, caneta=False).set_z_index(40)
        novo._s = s
        novo._canto = True
        self.st = novo
        self.play(FadeIn(novo), run_time=rt)


B39.subt = _subt
_fixos_b37 = B39.fixos


def _fixos37(self):
    f = set(_fixos_b37(self))
    for k in ("st", "cart"):
        m = getattr(self, k, None)
        if m is not None:
            f.add(m)
    return f


B39.fixos = _fixos37


# ── cartão √π ? (H2 → B6-2), abaixo do logo ────────────────────────────────────────────────────────────────────────────────
def cartao_raiz():
    f = TC(r"\sqrt{\pi}\ ?", 0, 0, 38, "c", caneta=True)
    w = f.width * 120 + 40
    X1 = 1878                                  # borda: ≥ 40 px (G6)
    mol = moldura(X1 - w, 122, w, 70, GEO, .55, 2, 10).set_z_index(39)
    mol._de = f
    f.move_to(PX(X1 - w / 2, 155))
    g = VGroup(mol, f)
    g.mol, g.f = mol, f
    return g


# ── desenho polar em px (vista Vw) ──────────────────────────────────────────────────────────────────────────────────────
def pts_setor(v, r1, r2, t0, t1, n=48, c=(0.0, 0.0)):
    out = [v.px(c[0] + r2 * math.cos(t), c[1] + r2 * math.sin(t)) for t in np.linspace(t0, t1, n + 1)]
    if r1 > 1e-9:
        out += [v.px(c[0] + r1 * math.cos(t), c[1] + r1 * math.sin(t)) for t in np.linspace(t1, t0, n + 1)]
    else:
        out.append(v.px(*c))
    return out


def setor(v, r1, r2, t0, t1, fill=None, fop=1.0, stroke=None, wpx=3, z=2, c=(0.0, 0.0), n=48):
    """Setor de anel r1 ≤ r ≤ r2, t0 ≤ θ ≤ t1 (preenchimento e/ou contorno)."""
    p = pts_setor(v, r1, r2, t0, t1, n, c)
    g = VGroup()
    if fill:
        g.add(poly_px(p, fill, fop, z=z))
    if stroke:
        g.add(lin_px(p + [p[0]], stroke, wpx, z=z + 1))
    return g


def arco(v, r, t0, t1, cor, wpx=3, dash=None, c=(0.0, 0.0), z=5, n=None, alpha=1.0):
    n = n or max(16, int(abs(t1 - t0) * 40))
    return lin_px([v.px(c[0] + r * math.cos(t), c[1] + r * math.sin(t)) for t in np.linspace(t0, t1, n + 1)], cor, wpx, alpha=alpha, dash=dash, z=z)


def gpolar(v, Rm, nr, nt, t0=0.0, t1=TAU_, cor=GEO, alpha=.42, wpx=1.6, z=3, c=(0.0, 0.0), raios=True):
    """Grade polar: nr círculos (Rm·i/nr) e nt + 1 raios de t0 a t1 (o último é omitido no círculo inteiro)."""
    g = VGroup()
    for i in range(1, nr + 1):
        g.add(arco(v, Rm * i / nr, t0, t1, cor, wpx, z=z, c=c, alpha=alpha))
    if raios:
        for k in range(nt + 1):
            t = t0 + (t1 - t0) * k / nt
            if abs(t1 - t0 - TAU_) < 1e-6 and k == nt:
                continue
            g.add(lin_px([v.px(*c), v.px(c[0] + Rm * math.cos(t), c[1] + Rm * math.sin(t))], cor, wpx, alpha=alpha, z=z))
    return g


def disco(v, R, fill, fop=1.0, c=(0.0, 0.0), z=1, n=160):
    return poly_px([v.px(c[0] + R * math.cos(t), c[1] + R * math.sin(t)) for t in np.linspace(0, TAU_, n, endpoint=False)], fill, fop, z=z)


def circulo(v, R, cor, wpx=3, c=(0.0, 0.0), z=5, dash=None, n=160):
    return lin_px([v.px(c[0] + R * math.cos(t), c[1] + R * math.sin(t)) for t in np.linspace(0, TAU_, n + 1)], cor, wpx, dash=dash, z=z)


def ret_v(v, a0, a1, b0, b1, fill, fop=1.0, z=1):
    return poly_px([v.px(a0, b0), v.px(a1, b0), v.px(a1, b1), v.px(a0, b1)], fill, fop, z=z)


def borda_v(v, a0, a1, b0, b1, cor=GEO, wpx=3, z=5, dash=None):
    return lin_px([v.px(a0, b0), v.px(a1, b0), v.px(a1, b1), v.px(a0, b1), v.px(a0, b0)], cor, wpx, dash=dash, z=z)


def eixos_xy(v, a0, a1, b0, b1, lx=r"\X", ly=r"\Y", cx=E1, cy=E2, wpx=3, size=34, ly_cima=True):
    """Eixos com ponta (x âmbar, y magenta) e rótulos: x à direita da ponta, y acima da ponta (como o eixosXY do sb34t2)."""
    sx = seta_px(v.px(a0, 0), v.px(a1, 0), cx, wpx, 16, z=6)
    sy = seta_px(v.px(0, b0), v.px(0, b1), cy, wpx, 16, z=6)
    A, B = v.px(a1, 0), v.px(0, b1)
    Lx = TC(lx, A[0] + 14, A[1], size, "l")
    Ly = TC(ly, B[0], B[1] - 30, size, "c") if ly_cima else TC(ly, B[0] + 22, B[1] + 6, size, "l")
    return sx, sy, Lx, Ly


def cel_txt(s, X, Y, size=26, cor=None):
    """'?' escuro dentro da célula lima (Space Grotesk bold)."""
    return T(s, X, Y, size, "center", cor or BG_, bold=True)


# ── cadeia `= … = …`: cada degrau é um L (MathTex de string única); o seguinte encosta à direita ou desce para a linha de baixo ──────────
def ao_lado(A, B, gap=14, ia=0, ib=0):
    """Põe B à direita de A (gap px) com o glifo ib de B na mesma altura do glifo ia de A (o '=' de cada degrau)."""
    B.shift(RIGHT * ((pxof(A.get_right())[0] + gap - pxof(B.get_left())[0]) / 120))
    B.shift(UP * (A[0][ia].get_center()[1] - B[0][ib].get_center()[1]))
    return B


def abaixo(A, B, X, gap=22, ia=None):
    """Põe B na linha de baixo de A, alinhado à esquerda em X px (o topo de B fica `gap` px abaixo do fundo de A)."""
    B.shift(RIGHT * ((X - pxof(B.get_left())[0]) / 120))
    B.shift(UP * ((pxof(B.get_top())[1] - (pxof(A.get_bottom())[1] + gap)) / 120))
    return B


GMAPS = []          # (nº, bloco, âncora, t, mapa resumido) — QA glyph_maps


def gmap(sc, n, A, B, pares, voos=(), rt=1.2, copia=True, nota="", extra=()):
    """Glyph map obrigatório nº n (handoff §3.4): TransformByGlyphMap do MF-Tools com mapa explícito (via passo do kit: o glifo novo vem
    pela caneta ou voa da fonte, nunca FadeIn). Registra no log [gmapN] para o QA."""
    t = (sc.nq - sc._q0) / FPS
    print(f"[gmap{n}] {sc.lote} {sc._aid} {t:.2f}s {nota} :: {A._tex[:70]!r} → {B._tex[:80]!r} :: pares={[(a, b) for a, b in pares]}")
    return passo(sc, A, B, pares, voos=voos, rt=rt, copia=copia, nota=f"GM{n} {nota}", extra=extra)


def degrau(sc, conta, desc, m=None):
    """QA CONTA INTEIRA: anota o degrau `desc` da conta `conta` no tempo atual da âncora."""
    print(f"[degrau] {sc.lote} {sc._aid} {(sc.nq - sc._q0) / FPS:6.2f}s {conta} :: {desc}")


def origem(sc, o, de):
    """QA ORIGENS: anota de onde nasceu o número/limite o."""
    print(f"[origem] {sc.lote} {sc._aid} {(sc.nq - sc._q0) / FPS:6.2f}s {o} <- {de}")


def escreve(sc, m, voos_=(), rt=0.9, depois=()):
    """Escreve m (L): os glifos sem fonte pela caneta, os que têm fonte voando (voos_ = [(fonte, chave|índices)])."""
    if voos_:
        sc.escreve_voos(m, voos_, depois=depois, rt=rt)
    else:
        sc.pena(m)
    return m


def poe_pronto(sc, *ms):
    for m in ms:
        ja_escrita(m)
        for x in m.get_family():
            if getattr(x, "_caneta", False):
                x._esc = True
    sc.add(*ms)


def frac_partes(m, key):
    """Peça com uma fração \\dfrac (com prefixo/sufixo na altura do traço): (fora, numerador, traço, denominador), cada um em ordem de x.
    O traço é o glifo mais achatado (largura/altura máxima)."""
    ix_ = sel(m, key)
    bar = max(ix_, key=lambda i: m[0][i].width / max(1e-4, m[0][i].height))
    yb = m[0][bar].get_center()[1]
    ox = lambda L: sorted(L, key=lambda i: m[0][i].get_center()[0])
    num = ox([i for i in ix_ if i != bar and m[0][i].get_bottom()[1] > yb])
    den = ox([i for i in ix_ if i != bar and m[0][i].get_top()[1] < yb])
    fora = ox([i for i in ix_ if i != bar and i not in num and i not in den])
    return fora, num, [bar], den


def corte3d(sc, pal, entram=(), rt=0.35, saem=()):
    """O 3D sai (fade curto) enquanto o 2D entra; os rótulos presos saem junto."""
    presos = [m for m in sc.mobjects if any(getattr(x, "_preso", False) for x in m.get_family())]
    an = [pal.fundo.op.animate.set_value(0.0)] + [FadeOut(m) for m in presos + list(saem)] + list(entram)
    sc.play(*an, run_time=rt)
    pal.fundo.clear_updaters()
    for m in presos + list(saem):
        m.clear_updaters()
    sc.remove(pal.fundo, *pal.tr.values(), *presos, *saem)


def anel_proj(pal, Rw, z=0.0, n=120, t0=0.0, t1=TAU_):
    """Pontos px de um anel do mundo (raio Rw em unidades do mundo, altura z) pela câmera atual do palco."""
    return [proj_p(pal, (Rw * math.cos(t), Rw * math.sin(t), z)) for t in np.linspace(t0, t1, n + 1)]
