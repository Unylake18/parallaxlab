"""yt_0034 · peças deste vídeo sobre o lib34.py (portadas dos helpers yt_0034 do referencia/sb34.html): vistas dos palcos, papel do palco,
eixos com rótulos, marcas, região, curvas, tiras em pé e deitadas com o ponto de entrada (azul-claro) e o de saída (coral), rótulo com placa,
painel lateral da fatia, linha mista (Space Grotesk + MathTex), caixas com ✓, selo, chave, passo de álgebra (TransformByGlyphMap do MF-Tools
com o glifo novo escrito pela caneta ou voando da fonte, nunca FadeIn) e o canto sem buraco entre títulos. Tudo em px de 1080p (PX)."""
from lib34 import *  # noqa: F401,F403
from lib34 import _TC_qa  # noqa: F401
from kit import _Caneta  # noqa: F401

RB = mixh(BG_, GEO, .18)                     # região B: GEO a ≈ 18 % sobre o fundo
GRADE = "#2B2558"
CH = Vw(360, 780, 240)                       # quarto de disco / chapa R = [0, 2]²
TRI = Vw(260, 860, 560)                      # triângulo unitário
TEL = Vw(560, 800, 420)                      # telhado [−1, 1] × [0, 1]
PQ = Vw(300, 640, 200)                       # A-pequeno (B1-2)
gs = lambda y: math.exp(-y * y)
S3 = math.sqrt(3)


# ── canto: a linha 2 troca num movimento só (a nova entra enquanto a velha sai: nunca há canto sem a linha 2) ───────────────────
def _secao34(self, s, rt=0.35):
    if self.h2 is not None and getattr(self.h2, "_s", None) == s:
        return
    novo = self._canto(txt(s, 21.6, color="#F5F7FF", bold=True, up=False), CANTO_Y2, topo_min=self._y1_fim_px() + 10)
    novo._s = s
    velho = self.h2
    anims = [FadeIn(novo)] + ([FadeOut(velho)] if velho is not None else [])
    if self.h1 not in self.mobjects:
        anims.append(FadeIn(self.h1))
    self.play(*anims, run_time=rt)
    if velho is not None:
        self.remove(velho)
    self.h2 = novo


_setup0 = B34.setup_base


def _setup34(self):
    _setup0(self)
    if self.h2 is not None:
        self.h2._s = self.ANTES
    self.wm.set_width(240 / 120).move_to(PX(1650 + 120, 24 + 42.5))


B34.secao = _secao34
B34.setup_base = _setup34


def grade_on34(self, v=CH, area=(0, 2.2, 0, 2.2), rt=0.5, junto=()):
    """Papel do palco: a grade (quadradinho de 0,25 da unidade do gráfico) nasce dos eixos e fica só dentro do palco."""
    if self.grade is not None:
        return
    self.grade = papel(v, area=area).set_z_index(-10)
    if rt > 0:
        self.play(FadeIn(self.grade), *junto, run_time=rt)
    else:
        self.add(self.grade)


B34.grade_on = grade_on34


def papel_v(v, area):
    return papel(v, area=area).set_z_index(-10)


# ── desenho no palco ─────────────────────────────────────────────────────────────────────────────────────
def eixos_v(v, a1, b1, a0=-.06, b0=-.06, lx=r"\X", ly=r"\Y", cx=E1, cy=E2):
    sx = seta_px(v.px(a0, 0), v.px(a1, 0), cx, 3, 16, z=6)
    sy = seta_px(v.px(0, b0), v.px(0, b1), cy, 3, 16, z=6)
    A, B = v.px(a1, 0), v.px(0, b1)
    Lx = TC(lx, A[0] + 22, A[1], 32, "c")
    Ly = TC(ly, B[0], B[1] - 26, 32, "c")
    return sx, sy, Lx, Ly


def tick(v, eixo, val, tex, size=28):
    """Marca no eixo (traço GEO de 14 px) + número (MathTex): eixo 'x' (número embaixo) ou 'y' (número à esquerda)."""
    if eixo == "x":
        q = v.px(val, 0)
        tr = lin_px([(q[0], q[1] - 7), (q[0], q[1] + 7)], GEO, 2, z=6)
        lb = TC(tex, q[0], q[1] + 30, size, "c")
    else:
        q = v.px(0, val)
        tr = lin_px([(q[0] - 7, q[1]), (q[0] + 7, q[1])], GEO, 2, z=6)
        lb = TC(tex, q[0] - 16, q[1], size, "r")
    return tr, lb


def regiao(v, pts, cor=RB, op=1.0, z=1):
    return poly_px([v.px(*p) for p in pts], cor, op, z=z)


def curva(v, pts, cor, wpx=4, dash=None, alpha=1.0, z=5):
    return lin_px([v.px(*p) for p in pts], cor, wpx, alpha=alpha, dash=dash, z=z)


def cX(fn, a0, a1, n=120):
    return [(a0 + (a1 - a0) * i / n, fn(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def cY(fn, b0, b1, n=120):
    return [(fn(b0 + (b1 - b0) * i / n), b0 + (b1 - b0) * i / n) for i in range(n + 1)]


def arco_q(r=2, n=90):
    return [(r * math.cos(PI / 2 * k / n), r * math.sin(PI / 2 * k / n)) for k in range(n + 1)]


def disco_pts():
    return [(0, 0)] + arco_q()


def tiraV(v, a, lo, hi, h=.06, cor=E1, alpha=.55, z=4):
    r = Polygon(v.P(a - h / 2, lo), v.P(a + h / 2, lo), v.P(a + h / 2, hi), v.P(a - h / 2, hi))
    r.set_fill(mixh(BG_, cor, alpha), 1).set_stroke(cor, W(2), 1)
    return sem_ctn(r).set_z_index(z)


def tiraH(v, b, lo, hi, h=.06, cor=E2, alpha=.55, z=4):
    r = Polygon(v.P(lo, b - h / 2), v.P(hi, b - h / 2), v.P(hi, b + h / 2), v.P(lo, b + h / 2))
    r.set_fill(mixh(BG_, cor, alpha), 1).set_stroke(cor, W(2), 1)
    return sem_ctn(r).set_z_index(z)


def pontos_es(v, pe, ps, r=9):
    """Ponto de entrada (azul-claro) e de saída (coral) da tira, em coordenadas do palco."""
    return ponto_px(*v.px(*pe), AZC, r), ponto_px(*v.px(*ps), CORAL, r)


def rot(v, tex, p, dx=0, dy=0, size=30, al="l"):
    q = v.px(*p)
    return TP(tex, q[0] + dx, q[1] + dy, size, al)


def placa_txt(s, X, Y, cor=BR, size=28, al="left"):
    return TPt(s, X, Y, size, cor, {"left": "left", "center": "center", "right": "right"}[al])


# ── painel lateral da fatia (vista de lado) ─────────────────────────────────────────────────────────────────
class Lat:
    """Painel lateral: origem (X0, Y0) px, uy px por unidade no eixo horizontal, uz px por unidade de f. Mesma interface de Vw."""

    def __init__(self, X0, Y0, uy, uz):
        self.cx, self.cy, self.u, self.uy = X0, Y0, uy, uz

    def px(self, a, b):
        return (self.cx + a * self.u, self.cy - b * self.uy)

    def P(self, a, b):
        return PX(*self.px(a, b))

    def c2p(self, a, b):
        return self.P(a, b)


def lateral(Lv, zmax, ymax=2.25, zt=(0, 2, 4, 6), yt=(0, 1, 2), hcor=E2, vcor=CI, hl=r"\Y", vl=r"\f", passo=None, grade=True):
    """Grade (0,25 no horizontal; vertical 0,25/0,5/1 conforme a escala), eixo horizontal e vertical com ponta, rótulos e números (MathTex GEO)."""
    g = {}
    if grade:
        pz = passo or (.25 if Lv.uy * .25 >= 20 else (.5 if Lv.uy * .5 >= 20 else 1))
        ls = VGroup()
        a = 0.0
        while a <= ymax + 1e-9:
            ls.add(lin_px([Lv.px(a, 0), Lv.px(a, zmax)], GRADE, 1.2, z=-9))
            a += .25
        b = 0.0
        while b <= zmax + 1e-9:
            ls.add(lin_px([Lv.px(0, b), Lv.px(ymax, b)], GRADE, 1.2, z=-9))
            b += pz
        g["grade"] = ls
    g["eh"] = seta_px(Lv.px(-.05, 0), Lv.px(ymax + .08, 0), hcor, 3, 16, z=6)
    g["ev"] = seta_px(Lv.px(0, -8 / Lv.uy), Lv.px(0, zmax + .15), vcor, 3, 16, z=6)        # o eixo vertical não desce até o 0 do eixo de baixo
    p = Lv.px(ymax + .2, 0)
    g["lh"] = TC(hl, p[0] + 6, p[1], 32, "l")
    p = Lv.px(0, zmax + .15)
    g["lv"] = TC(vl, p[0], p[1] - 30, 32, "c")
    nums = VGroup()
    for a in yt:
        q = Lv.px(a, 0)
        nums.add(TC(r"\Ge{%s}" % str(a).replace(".", "{,}"), q[0], q[1] + 28, 26, "c"))
    for b in zt:
        q = Lv.px(0, b)
        if b == 0 and 0 in yt:
            continue
        nums.add(TC(r"\Ge{%s}" % str(b).replace(".", "{,}"), q[0] - 14, q[1], 26, "r"))
    g["nums"] = nums
    return g


# ── coluna: linha mista, caixas, selo, chave ─────────────────────────────────────────────────────────────────
def mixl(partes, X, Y, S=36):
    """mixl do sb34: ('m', tex) em MathTex de S px; ('t', texto[, cor]) em Space Grotesk de 0,78·S px, linha de base em Y + 0,27·S; respiro 14 px."""
    g, cx, ps = VGroup(), X, []
    for p in partes:
        if p[0] == "m":
            m = TC(p[1], cx, Y, S, "l")
        elif p[0] == "L":
            m = L(p[1], cx, Y, S, "l")
        else:
            m = T(p[1], cx, Y + S * .27, round(S * .78), "left", p[2] if len(p) > 2 else BR)
        cx = pxof(m.get_right())[0] + 14
        g.add(m)
        ps.append(m)
    g.p = ps
    g._tex = "mixl: " + " | ".join(str(p[1])[:24] for p in partes)
    return g


def caixa_ok(X, Y, w, t, ok=True):
    mol = moldura(X, Y - 45, w, 80, GEO, .45, 2, 12)
    ck = check_px(X + 40, Y - 6, MEN, .9) if ok else cruz_px(X + 40, Y - 6, AL, .9)
    tt = T(t, X + 80, Y + 8, 30)
    return mol, ck, tt


def selo(s, X, Y, cor=GEO, size=26):
    t = leg(s, X + 14, Y + 2, cor, "left", size)
    w = t.width * 120
    mol = moldura(X, Y - size - 6, w + 28, size + 22, cor, 1.0, 2, 8)
    return mol, t


def chave_px(X0, X1, Y, cor=E2, wpx=3):
    """Chave horizontal (abre para cima) de X0 a X1 com a ponta no meio, para baixo (como a do sb34)."""
    def qb(a, c, b, n=10):
        return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]) for t in np.linspace(0, 1, n)]
    m = (X0 + X1) / 2
    pts = qb((X0, Y - 10), (X0, Y), (X0 + 14, Y)) + qb((m - 12, Y), (m, Y), (m, Y + 12)) + qb((m, Y + 12), (m, Y), (m + 12, Y)) + qb((X1 - 14, Y), (X1, Y), (X1, Y - 10))
    return lin_px(pts, cor, wpx, z=6)


# ── álgebra: passo com TransformByGlyphMap (MF-Tools) ─────────────────────────────────────────────────────────
def passo(sc, A, B, pares, voos=(), rt=1.2, copia=False, nota="", extra=(), atraso_caneta=0.15):
    """A → B com TransformByGlyphMap (auto_fade, mapa explícito). Os glifos de B fora do mapa NÃO entram por fade: ficam apagados durante o mapa
    e depois voam da fonte (voos = [(origem, chave|índices em B)]) ou são escritos pela caneta, da esquerda para a direita."""
    def selm(B, b):
        if isinstance(b, Mobject):
            ids = {id(x) for x in b.submobjects}
            return [i for i, gx in enumerate(B[0]) if id(gx) in ids]
        return sel(B, b)
    alvo = set()
    for _, b in pares:
        alvo |= set(sel(B, b))
    voados = set()
    for _, b in voos:
        voados |= set(selm(B, b))
    novos = [i for i in range(len(B[0])) if i not in alvo]
    orig = {i: B[0][i].copy() for i in novos}
    for i in novos:
        B[0][i].set_fill(opacity=0).set_stroke(width=0, opacity=0)
    for x in B.get_family():
        x._voando = True
    gm(sc, A, B, pares, rt=rt, copia=copia, extra=extra, nota=nota)
    if not novos:
        for x in B.get_family():
            x._voando = False
        return B
    for i in novos:
        B[0][i].become(orig[i])
    anims = []
    for src, b in voos:
        g = VGroup(*[B[0][i] for i in selm(B, b)])
        anims.append(TransformFromCopy(src, g, path_arc=-0.6, run_time=1.0))
    resto = [i for i in novos if i not in voados]
    if resto:
        g = VGroup(*[B[0][i] for i in resto])
        g._tex = B._tex + " (glifos novos)"
        g._caneta, g._esc, g._em_caneta, g._txt = True, False, False, None
        anims.append(caneta(g, atraso=atraso_caneta if voos else 0.0, ritmo=CANETA_P / 0.30))
    tot = max([1.0 if voos else 0.0] + [a.tot for a in anims if isinstance(a, _Caneta)])
    for x in B.get_family():
        x._voando = False
    sc.play(*anims, run_time=tot)
    for a in anims:
        if isinstance(a, TransformFromCopy):
            sc.remove(a.mobject)
    sc.add(B)
    return B


def acende(sc, *grupos, cor=None, rt=1.6):
    """Sublinhado de leitura sob um ou mais grupos de glifos ao mesmo tempo (traço fino na cor dada ou branco), aparece e sai."""
    ss = []
    for gg, c in grupos:
        x0, x1 = pxof(gg.get_left())[0], pxof(gg.get_right())[0]
        y = pxof(gg.get_bottom())[1] + 7
        ss.append(sublinha_px(x0 - 2, x1 + 2, y, c or BR, 2.5))
    sc.play(*[Create(s) for s in ss], run_time=0.3)
    sc.wait(rt)
    sc.play(*[FadeOut(s) for s in ss], run_time=0.3)
    sc.remove(*ss)


def sublinha_fica(gg, cor=BR):
    x0, x1 = pxof(gg.get_left())[0], pxof(gg.get_right())[0]
    y = pxof(gg.get_bottom())[1] + 7
    return sublinha_px(x0 - 2, x1 + 2, y, cor, 2.5)


def voos(sc, pares, rt=1.0, arco=-0.6, extra=()):
    """Vários termos nascendo do desenho (ou da fórmula para o desenho) ao mesmo tempo: [(origem, alvo)], TransformFromCopy em arco."""
    an = []
    for src, alvo_m in pares:
        ja_escrita(alvo_m)
        for x in alvo_m.get_family():
            if getattr(x, "_caneta", False):
                x._esc = True
        an.append(TransformFromCopy(src, alvo_m, path_arc=arco, run_time=rt))
    for _, b in pares:
        for x in b.get_family():
            x._voando = True
    sc.play(*an, *extra, run_time=rt)
    for _, b in pares:
        for x in b.get_family():
            x._voando = False
    for a in an:
        sc.remove(a.mobject)
    sc.add(*[b for _, b in pares])
    junta(sc, *[b for _, b in pares])


def sai_com_canto(sc, rt=0.4):
    """Fim de lote seguido de um bloco sem canto (A1): o conteúdo e as duas linhas do canto saem juntos, dentro da fala."""
    if sc._aid is not None:
        sc._fecha(antes=rt)
    ms = sc.snap() + [m for m in (sc.h1, sc.h2) if m is not None and m in sc.mobjects]
    if ms:
        sc.play(*[FadeOut(m) for m in ms], run_time=rt)
    for m in ms:
        m.clear_updaters()
    sc.remove(*ms)
    sc.h2 = None


def risca_voando(sc, pares, rt=1.1):
    """Termo da fórmula que vira traço no desenho (TransformFromCopy glifo → curva): o traço em trânsito não conta no R5 (é o próprio voo)."""
    for _, b in pares:
        for x in b.get_family():
            x._voando = True
    sc.play(*[TransformFromCopy(a, b, path_arc=-0.5) for a, b in pares], run_time=rt)
    for _, b in pares:
        for x in b.get_family():
            x._voando = False


def voa(sc, src, alvo_m, rt=1.0, arco=-0.6, extra=()):
    """Um rótulo/termo inteiro que nasce do desenho: TransformFromCopy em arco (o alvo é liberado do portão FLASH antes do play)."""
    ja_escrita(alvo_m)
    for x in alvo_m.get_family():
        if getattr(x, "_caneta", False):
            x._esc = True
    a = TransformFromCopy(src, alvo_m, path_arc=arco, run_time=rt)
    for x in alvo_m.get_family():
        x._voando = True
    sc.play(a, *extra, run_time=rt)
    for x in alvo_m.get_family():
        x._voando = False
    sc.remove(a.mobject)
    sc.add(alvo_m)
    return alvo_m


# ── região genérica, U, telhado ─────────────────────────────────────────────────────────────────────────────────
def c_b21(X):
    return .35 + .22 * math.sin(1.4 * X)


def d_b21(X):
    return 1.55 + .3 * math.sin(2 * X + .4)


def a_b22(Y):
    return .3 + .2 * math.sin(2.2 * Y)


def b_b22(Y):
    return 1.6 + .25 * math.sin(1.6 * Y + 1)


# ── QA R5 contínuo (handoff §8.3): a cada 0,5 s do relógio, também DURANTE as animações ────────────────────────────────────
# texto × texto (caixas) e texto × traço (linhas, arestas, curvas, eixos, setas, bordas de painel/cartão): um traço conta quando algum ponto
# dele (densificado) cai dentro da caixa do texto encolhida 2 px. A grade do papel (z ≤ −9) e o 3D (PNG) ficam de fora.
def _caixa_px(x):
    x0, y1 = pxof(x.get_corner(UL))
    x1, y0 = pxof(x.get_corner(DR))
    return x0, y1, x1, y0


def r5b(self, onde="anim"):
    textos, dono = [], {}
    for m in self.mobjects:
        if m in (self.wm, self.h1, self.h2):
            continue
        for x in m.get_family():
            if getattr(x, "_txt", None) is None or getattr(x, "_voando", False):
                continue
            if any(y is not x and getattr(y, "_txt", None) is not None and x in y.get_family() for y in m.get_family()):
                continue
            gls = [g for g in x.family_members_with_points() if isinstance(g, VMobject)]
            if not gls or max(g.get_fill_opacity() for g in gls) < 0.3:
                continue
            textos.append((x._txt, _caixa_px(x), x))
            for g in x.get_family():
                dono[id(g)] = x
    linhas = []
    for m in self.mobjects:
        if m in (self.wm, self.h1, self.h2) or isinstance(m, (ValueTracker, ImageMobject)):
            continue
        for x in m.family_members_with_points():
            if not isinstance(x, VMobject) or id(x) in dono or (x.z_index or 0) <= -9 or (x.z_index or 0) == 31:   # 31: sublinhado de leitura
                continue
            if x.get_stroke_width() < 0.5 or x.get_stroke_opacity() < 0.3 or getattr(x, "_voando", False):
                continue
            P = x.points
            if len(P) < 2:
                continue
            t = np.linspace(0, 1, 6)[:, None, None]
            Q = (P[:-1][None] * (1 - t) + P[1:][None] * t).reshape(-1, 3)
            linhas.append((type(x).__name__ + " " + ManimColor(x.get_stroke_color()).to_hex(), Q[:, 0] * 120 + 960, 540 - Q[:, 1] * 120))
    n = 0
    for i, (ta, (ax0, ay0, ax1, ay1), xa) in enumerate(textos):
        for tb, (bx0, by0, bx1, by1), xb in textos[i + 1:]:
            if xa in xb.get_family() or xb in xa.get_family():
                continue
            ox, oy = min(ax1, bx1) - max(ax0, bx0), min(ay1, by1) - max(ay0, by0)
            if ox > 2 and oy > 2:
                self._r5.append((self._aid, self.t, ta, tb, ox, oy))
                print(f"[R5] {self._aid} {self.t:7.2f}s {ta!r} x {tb!r} ({ox:.0f}x{oy:.0f} px) {onde}")
                n += 1
        for nome, X, Y in linhas:
            k = int(np.count_nonzero((X > ax0 + 2) & (X < ax1 - 2) & (Y > ay0 + 2) & (Y < ay1 - 2)))
            if k:
                self._r5.append((self._aid, self.t, ta, nome, k, 0))
                print(f"[R5L] {self._aid} {self.t:7.2f}s {ta!r} x traço {nome} ({k} pts) {onde}")
                n += 1
    return n


_utt0 = B34.update_to_time


def _utt34(self, t):
    _utt0(self, t)
    if getattr(self, "_em_play", False):
        c = self.clk.get_value()
        if c >= getattr(self, "_prox_r5", 0.0):
            self._prox_r5 = math.floor(c / 0.5) * 0.5 + 0.5
            r5b(self)


B34.update_to_time = _utt34
B34.r5 = r5b
