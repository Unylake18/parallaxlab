"""yt_0036 · peças deste vídeo sobre o lib36.py (portadas dos helpers yt_0036 do referencia/sb34.html): vistas dos palcos, papel do palco,
eixos com rótulos, marcas, região, curvas, tiras em pé e deitadas com o ponto de entrada (azul-claro) e o de saída (coral), rótulo com placa,
painel lateral da fatia, linha mista (Space Grotesk + MathTex), caixas com ✓, selo, chave, passo de álgebra (TransformByGlyphMap do MF-Tools
com o glifo novo escrito pela caneta ou voando da fonte, nunca FadeIn) e o canto sem buraco entre títulos. Tudo em px de 1080p (PX)."""
from lib36 import *  # noqa: F401,F403
from lib36 import _TC_qa  # noqa: F401
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
    return TPt(s, X, Y, max(26, size), cor, {"left": "left", "center": "center", "right": "right"}[al])


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
            m = T(p[1], cx, Y + S * .27, max(26, round(S * .78)), "left", p[2] if len(p) > 2 else BR)        # v3: texto ≥ 26 px
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
def passo(sc, A, B, pares, voos=(), rt=1.0, copia=False, nota="", extra=(), atraso_caneta=0.15, seq=False):
    """A → B com TransformByGlyphMap (auto_fade, mapa explícito). Os glifos de B fora do mapa NÃO entram por fade: ficam apagados durante o mapa
    e depois voam da fonte (voos = [(origem, chave|índices em B)]) ou são escritos pela caneta, da esquerda para a direita."""
    def selm(B, b):
        if isinstance(b, Mobject):
            ids = {id(x) for x in b.submobjects}
            return [i for i, gx in enumerate(B[0]) if id(gx) in ids]
        return sel(B, b)
    if len(pares) == 1 and not voos:
        # v2: um mapa de 1 par não é manipulação, é origem: o termo VOA (TransformFromCopy) e a caneta escreve só os glifos sem fonte (G3/C4)
        pa_, pb_ = pares[0]
        ia, ib = sel(A, pa_), sel(B, pb_)
        resto = [i for i in range(len(B[0])) if i not in ib]
        print(f"[voo1] {sc.lote} {sc._aid} {sc.t:.2f} {nota} :: {A._tex[:50]!r} → {B._tex[:60]!r}")
        if resto:
            g = parte(B, resto, "sem fonte")
            sc.pena(g)
        alvo_ = parte(B, ib, "voo")
        ja_escrita(alvo_)
        for x in alvo_.get_family():
            x._voando = True
        src_ = VGroup(*[A[0][i] for i in ia])
        velho = par_de_voo(sc, src_, alvo_)
        an = tfc(src_, alvo_, rt=rt, arco=0, sc=sc)
        sai = [] if copia else [FadeOut(A)]
        sc.play(an, *sai, *extra, run_time=rt)
        solta_par(src_, velho)
        for x in alvo_.get_family():
            x._voando = False
        sc.remove(an.mobject)
        if not copia:
            sc.remove(A)
        sc.add(alvo_)
        junta(sc, alvo_)
        sc.remove(*[q for q in getattr(B, "_partes", [])])
        B._esc = True
        sc.add(B)
        return B
    alvo = set()
    for _, b in pares:
        alvo |= set(sel(B, b))
    voados = set()
    for v_ in voos:
        voados |= set(selm(B, v_[1]))
    novos = [i for i in range(len(B[0])) if i not in alvo]
    orig = {i: B[0][i].copy() for i in novos}
    for i in novos:
        B[0][i].set_fill(opacity=0).set_stroke(width=0, opacity=0)
    for x in B.get_family():
        x._voando = True
        x._de_linha = True                    # glifo de uma linha da coluna (o QA de órfão não o conta como solto)
    sc._gm_par = frozenset({id(y) for g in (A, B) for y in g.get_family()} | {id(y) for g in (A, B) for d_ in donos_txt(sc, g) for y in d_.get_family()})
    gm(sc, A, B, pares, rt=rt, copia=copia, extra=extra, nota=nota)
    sc._gm_par = None
    if not novos:
        for x in B.get_family():
            x._voando = False
        return B
    if seq and voos:
        # v2 (Q13): os termos voam UM DE CADA VEZ para o lugar deles; cada glifo só reaparece no próprio voo (sem flash)
        for x in B.get_family():
            x._voando = False
        for v_ in voos:
            src, b = v_[0], v_[1]
            idx = selm(B, b)
            for i in idx:
                B[0][i].become(orig[i])
            g = VGroup(*[B[0][i] for i in idx])
            ja_escrita(g)
            velho = par_de_voo(sc, src, g)
            an = tfc(src, g, rt=0.7, via=v_[2] if len(v_) > 2 else None, sc=sc)
            sc.play(an, run_time=0.7)
            solta_par(None, velho)
            sc.remove(an.mobject)
            sc.add(B)
            limpa_restos(sc)
        resto = [i for i in novos if i not in voados]
        if resto:
            for i in resto:
                B[0][i].become(orig[i])
            g = VGroup(*[B[0][i] for i in resto])
            g._tex = B._tex + " (glifos novos)"
            g._caneta, g._esc, g._em_caneta, g._txt = True, False, False, None
            an = caneta(g, ritmo=CANETA_P / 0.30)
            sc.play(an, run_time=an.tot)
        sc.add(B)
        return B
    for i in novos:
        B[0][i].become(orig[i])
    anims, velhos_ = [], []
    fontes = [x for v_ in voos for x in v_[0].get_family()]
    for x in fontes:
        x._voando = True                     # a cópia em voo herda a marca: fora do R5 (a fonte volta ao normal depois)
    for v_ in voos:
        src, b = v_[0], v_[1]
        g = VGroup(*[B[0][i] for i in selm(B, b)])
        velhos_.append(par_de_voo(sc, src, g))
        g._grupo = id(B)                       # os voos de um mesmo glyph map são um movimento só
        anims.append(tfc(src, g, rt=1.0, via=v_[2] if len(v_) > 2 else None, sc=sc))
    for x in fontes:
        x._voando = False
    resto = [i for i in novos if i not in voados]
    if resto:
        g = VGroup(*[B[0][i] for i in resto])
        g._tex = B._tex + " (glifos novos)"
        g._caneta, g._esc, g._em_caneta, g._txt = True, False, False, None
        anims.append(caneta(g, atraso=atraso_caneta if voos else 0.0, ritmo=CANETA_P / 0.30))
    tot = max([1.0 if voos else 0.0] + [a.tot for a in anims if isinstance(a, _Caneta)])
    for x in B.get_family():
        x._voando = False
    em_voo = [x for v_ in voos for i in selm(B, v_[1]) for x in B[0][i].get_family()]
    for x in em_voo:
        x._voando = True                     # o glifo de B que chega voando (TransformFromCopy anima o próprio destino)
    sc.play(*anims, run_time=tot)
    for v_ in velhos_:
        solta_par(None, v_)
    for x in em_voo:
        x._voando = False
    for a in anims:
        if isinstance(a, TransformFromCopy):
            sc.remove(a.mobject)
    sc.add(B)
    limpa_restos(sc)
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


def voos(sc, pares, rt=0.8, arco=-0.6, extra=(), livre=(), via=None, seq=True):
    """Termos nascendo do desenho (ou da fórmula para o desenho): [(origem, alvo)] ou [(origem, alvo, via_px)], TransformFromCopy.
    v2 (Q09): com mais de um par, os voos vão UM DE CADA VEZ (≥ 0,6 s cada), nunca em bolo; seq=False junta (só para pares que não se cruzam)."""
    pares = [tuple(p_) for p_ in pares]
    if seq and len(pares) > 1:
        for k, p_ in enumerate(pares):
            voos(sc, [p_], rt=max(0.45, rt * 0.75), arco=arco, extra=extra if k == 0 else (), livre=livre, via=via, seq=False)
        return
    an, velhos_ = [], []
    fontes = [x for p_ in pares for x in p_[0].get_family()]
    for x in fontes:
        x._voando = True
    for p_ in pares:
        src, alvo_m = p_[0], p_[1]
        ja_escrita(alvo_m)
        for x in alvo_m.get_family():
            if getattr(x, "_caneta", False):
                x._esc = True
        velhos_.append(par_de_voo(sc, src, alvo_m, livre))
        an.append(tfc(src, alvo_m, rt=rt, arco=arco, via=p_[2] if len(p_) > 2 else via, sc=sc))
    for x in fontes:
        x._voando = False
    bs = [p_[1] for p_ in pares]
    for b in bs:
        for x in b.get_family():
            x._voando = True
    sc.play(*an, *extra, run_time=rt)
    for v_ in velhos_:
        solta_par(None, v_)
    for b in bs:
        for x in b.get_family():
            x._voando = False
    for a in an:
        sc.remove(a.mobject)
    sc.add(*bs)
    junta(sc, *bs)
    for b in bs:                                                         # QA CONTAS: termo que pousou por voo
        print(f"[voo] {getattr(sc, 'lote', '?')} {getattr(sc, '_aid', '?')} {(sc.nq - getattr(sc, '_q0', 0)) / FPS:6.2f}s {str(getattr(b, '_tex', ''))[:90]!r} dir={pxof(b.get_right())[0]:.0f}")


def sai_com_canto(sc, rt=0.4):
    """Fim de lote seguido de um bloco sem canto (A1): o conteúdo e as duas linhas do canto saem juntos, dentro da fala."""
    if sc._aid is not None:
        sc._fecha(antes=rt)
    # yt_0036: o canto fica inteiro até o último quadro do lote e sai seco no corte para o A1 (sem quadro de canto apagado)
    cs = [m for m in (sc.h1, sc.h2) if m is not None and m in sc.mobjects]
    ms = sc.snap()
    if ms:
        sc.play(*[FadeOut(m) for m in ms], run_time=rt)
    for m in ms:
        m.clear_updaters()
    sc.remove(*ms)
    sc.remove(*cs)
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


def voa(sc, src, alvo_m, rt=1.0, arco=-0.6, extra=(), livre=(), via=None):
    """Um rótulo/termo inteiro que nasce do desenho: TransformFromCopy em arco (o alvo é liberado do portão FLASH antes do play)."""
    ja_escrita(alvo_m)
    for x in alvo_m.get_family():
        if getattr(x, "_caneta", False):
            x._esc = True
    velho = par_de_voo(sc, src, alvo_m, livre)
    a = tfc(src, alvo_m, rt=rt, arco=arco, via=via, sc=sc)
    for x in alvo_m.get_family():
        x._voando = True
    sc.play(a, *extra, run_time=rt)
    solta_par(None, velho)
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


# ── v2: caminho de voo com ponto de passagem (Bézier quadrática dos centros) e desvio automático pela margem da coluna ─────────────
COL_ESQ = 1090


def caminho_via(S, E, C):
    """path_func do Transform: o centro anda na Bézier S → C → E (px); a forma interpola como sempre."""
    S, E, C = PX(*S), PX(*E), PX(*C)
    off = 2 * C - S - E

    def f(a_pts, b_pts, alpha):
        return a_pts + (b_pts - a_pts) * alpha + alpha * (1 - alpha) * off
    return f


def caminho_poli(pts):
    """path_func por uma poligonal suavizada (px): o centro anda com velocidade constante por S → m1 → … → E."""
    P = np.array([PX(*p) for p in pts])
    seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)]) / max(seg.sum(), 1e-9)

    def pos(a):
        k = int(np.clip(np.searchsorted(cum, a) - 1, 0, len(seg) - 1))
        u = (a - cum[k]) / max(cum[k + 1] - cum[k], 1e-9)
        return P[k] + (P[k + 1] - P[k]) * u

    def f(a_pts, b_pts, alpha):
        # Só usado pelo tfc (TransformFromCopy): a = alvo, b = fonte, alpha = 1 − t. O path_func é chamado GLIFO A GLIFO: o desvio
        # é o do centro do grupo (poligonal − reta S → E no mesmo t), igual para todos os glifos (a forma do grupo se mantém).
        t = 1 - alpha
        return a_pts + (b_pts - a_pts) * alpha + (pos(t) - (P[0] + (P[-1] - P[0]) * t))
    return f


COL_BORDA = [None]                    # margem esquerda da coluna em uso (Coluna36.poe a atualiza)
COL_ATUAL = [None]                    # a coluna em uso (para saber se há linhas entre a fonte e o destino)


def via_auto(src, alvo, via=None):
    """Voo dentro da coluna que pula linhas: passa pela margem esquerda da coluna, por fora das linhas do meio. None = arco normal.
    via: um ponto (Bézier passando por ele) ou uma lista de pontos (poligonal suavizada)."""
    S, E = pxof(src.get_center()), pxof(alvo.get_center())
    if via is not None and isinstance(via, list):
        return caminho_poli([S, *via, E])
    lim = (COL_BORDA[0] - 10) if COL_BORDA[0] else COL_ESQ
    col = COL_ATUAL[0]
    entre = []
    if col is not None:
        y0_, y1_ = sorted((S[1], E[1]))
        entre = [l for l in col.ls if y0_ + 12 < pxof(l.get_center())[1] < y1_ - 12]
    if via is not None:
        m = via
    elif S[0] > lim and E[0] > lim and abs(S[1] - E[1]) > 70 and not entre:
        return caminho_poli([S, E])                                         # linhas vizinhas na coluna: reto
    elif S[0] > lim and E[0] > lim and abs(S[1] - E[1]) > 70:
        w = max(src.width, alvo.width) * 120
        borda = min(pxof(src.get_left())[0], pxof(alvo.get_left())[0], COL_BORDA[0] or 9999)   # a margem esquerda da própria coluna
        m = (borda - 40 - w / 2, (S[1] + E[1]) / 2)
        # v2: a margem DIREITA é preferida quando cabe (a esquerda passa pelos rótulos das linhas e do palco)
        dmax_e = max([pxof(l.get_right())[0] for l in entre] + [pxof(src.get_right())[0], pxof(alvo.get_right())[0]])
        if dmax_e + 40 + w <= 1866:                                       # final K13: a calha da direita fica dentro de x ≤ 1872
            xg = dmax_e + 40 + w / 2
            return caminho_poli([S, (xg, S[1]), (xg, E[1]), E])
        if m[0] - w / 2 < 60 and col is not None:
            # coluna colada na margem esquerda (ex.: C6 em x = 80): o desvio passa pela DIREITA das linhas da coluna
            dmax = max([pxof(l.get_right())[0] for l in col.ls] + [pxof(src.get_right())[0], pxof(alvo.get_right())[0]])
            m = (dmax + 40 + w / 2, m[1])
        if os.environ.get("DEBUG_VOO"):
            print(f"[via] S={S[0]:.0f},{S[1]:.0f} E={E[0]:.0f},{E[1]:.0f} m.x={m[0]:.0f} borda={borda:.0f} w={w:.0f}")
        return caminho_poli([S, (m[0], S[1]), (m[0], E[1]), E])
    else:
        return None
    C = (2 * m[0] - (S[0] + E[0]) / 2, 2 * m[1] - (S[1] + E[1]) / 2)      # a curva passa por m em alpha = 1/2
    return caminho_via(S, E, C)


def sem_traco(m):
    """final K3: glifo (preenchido) sem contorno — o contorno fino é só da caneta, durante a escrita; voo e pouso só com preenchimento."""
    for x in m.get_family():
        if isinstance(x, VMobject) and len(x.points) and x.get_fill_opacity() > 0.3 and type(x).__name__ in ("VMobjectFromSVGPath", "SVGPathMobject"):
            x.set_stroke(width=0)
    return m


def _rush_tfc(t):
    """TransformFromCopy interpola em 1 − t: rush_into(1 − t) sai rápido da fonte e pousa devagar (o rush_from do handoff, no sentido do voo)."""
    return rush_into(t)


def _obstaculos(sc, src, alvo):
    """Caixas (px) dos TEXTOS já na tela que um voo não pode atravessar — a mesma regra do R5: fora os textos liberados para este voo
    (alvo._par: a fonte, o destino e os rótulos do desenho de onde o termo sai), o canto, o chip, o papel e o que está saindo."""
    if sc is None:
        return []
    fx = set()
    try:
        for f_ in sc.fixos():
            if f_ is not None:
                fx |= {id(y) for y in f_.get_family()}
    except Exception:
        pass
    livre = set(getattr(alvo, "_par", None) or ()) | {id(y) for g in (src, alvo) for y in g.get_family()}
    pai = getattr(alvo, "_pai", None)
    if pai is not None:
        livre |= {id(y) for y in pai.get_family()}
    out = []
    for top in sc.mobjects:
        if id(top) in fx:
            continue
        for x in top.get_family():
            if getattr(x, "_txt", None) is None or id(x) in livre or id(x) in fx or _fora_r5(x) or _opac(x) <= 0.15:
                continue
            if any(y is not x and getattr(y, "_txt", None) is not None and x in y.get_family() for y in top.get_family()):
                continue
            out.append(_caixa_px(x))
    return out


def _cruzamentos(obs, S, E, ws, hs, we, he, centro_t):
    n = 0
    for t in np.linspace(0.05, 0.95, 19):
        cx, cy = centro_t(t)
        w, h = ws + (we - ws) * t, hs + (he - hs) * t
        x0, y0, x1, y1 = cx - w / 2 + 2, cy - h / 2 + 2, cx + w / 2 - 2, cy + h / 2 - 2
        if x0 < 48 or y0 < 48 or x1 > 1872 or y1 > 1032:                    # fora da área segura conta como cruzamento (margem)
            n += 1
            continue
        for b in obs:
            if min(x1, b[2]) - max(x0, b[0]) > 0 and min(y1, b[3]) - max(y0, b[1]) > 0:
                n += 1
                break
    return n


def tfc(src, alvo, rt=1.0, arco=-0.6, via=None, sc=None):
    """TransformFromCopy com o caminho do v2 (via_auto) ou em arco. final K3: a cópia voa só com preenchimento (sem contorno), sai rápido
    e pousa devagar; o destino pousa sem contorno; se o caminho cruza um glifo já escrito, troca para o arco livre (|arco| ≥ 0,6 rad)."""
    from manim.utils.paths import path_along_arc
    sem_traco(alvo)
    src_c = sem_traco(src.copy())
    f = via_auto(src, alvo, via)
    S, E = np.array(PX(*pxof(src.get_center()))), np.array(PX(*pxof(alvo.get_center())))
    ws, hs, we, he = src.width * 120, src.height * 120, alvo.width * 120, alvo.height * 120

    def centro_de(pf):
        def c(t):
            p = pf(np.array([E]), np.array([S]), 1 - t)[0]
            return pxof(p)
        return c
    escolha = ("via", f) if f is not None else ("arco", arco)
    if sc is not None and not (via is not None and isinstance(via, list)):
        obs = _obstaculos(sc, src, alvo)
        if True:
            base = f if f is not None else path_along_arc(arco)
            n0 = _cruzamentos(obs, S, E, ws, hs, we, he, centro_de(base))
            if n0:
                melhor = (n0, escolha)
                for a_ in (0.6, -0.6, 1.0, -1.0, 1.4, -1.4, 1.8, -1.8):
                    n_ = _cruzamentos(obs, S, E, ws, hs, we, he, centro_de(path_along_arc(a_)))
                    if n_ < melhor[0] and (n_ == 0 or n_ <= n0 / 2):
                        melhor = (n_, ("arco", a_))
                    if n_ == 0:
                        break
                escolha = melhor[1]
                print(f"[voo-desvio] {getattr(sc, '_aid', '?')} {getattr(sc, 't', 0):.2f}s cruzava {n0} amostras → {escolha[0]} "
                      f"{escolha[1] if escolha[0] == 'arco' else 'via'} ({melhor[0]} amostras)")
    if escolha[0] == "via":
        return TransformFromCopy(src_c, alvo, path_func=escolha[1], run_time=rt, rate_func=_rush_tfc)
    return TransformFromCopy(src_c, alvo, path_arc=escolha[1], run_time=rt, rate_func=_rush_tfc)


# ── QA R5 contínuo (handoff §8.3): a cada 0,5 s do relógio, também DURANTE as animações ────────────────────────────────────
# texto × texto (caixas) e texto × traço (linhas, arestas, curvas, eixos, setas, bordas de painel/cartão): um traço conta quando algum ponto
# dele (densificado) cai dentro da caixa do texto encolhida 2 px. A grade do papel (z ≤ −9) e o 3D (PNG) ficam de fora.
def _caixa_px(x, fora=frozenset()):
    """Caixa a 1080p; `fora`: ids dos glifos em voo (pertencem ao texto de destino, mas ainda estão no caminho)."""
    if fora:
        P = [g.points for g in x.family_members_with_points() if id(g) not in fora and len(g.points)]
        if P:
            P = np.vstack(P)
            return P[:, 0].min() * 120 + 960, 540 - P[:, 1].max() * 120, P[:, 0].max() * 120 + 960, 540 - P[:, 1].min() * 120
    x0, y1 = pxof(x.get_corner(UL))
    x1, y0 = pxof(x.get_corner(DR))
    return x0, y1, x1, y0


def _opac(x):
    """Opacidade visível (v2 §7.1: a meio da escrita conta o contorno da caneta)."""
    gls = [g for g in x.family_members_with_points() if isinstance(g, VMobject)]
    if not gls:
        return 0.0
    return max(max(g.get_fill_opacity(), g.get_stroke_opacity() if g.get_stroke_width() > 0.3 else 0.0) for g in gls)


def _fora_r5(x):
    """Só a leitura (pulso do palco, realce) e o que está saindo em fade ficam fora do R5 (v2 §7.1: voo, glyph map e escrita contam)."""
    return getattr(x, "_leitura", False) or getattr(x, "_saindo", False)


def donos_txt(sc, m):
    """Os textos (com _txt) da cena que contêm m (ou o próprio m)."""
    fam = set(id(y) for y in m.get_family())
    out = []
    for top in sc.mobjects:
        for y in top.get_family():
            if getattr(y, "_txt", None) is not None and (id(y) in fam or any(id(z) in fam for z in y.get_family())):
                out.append(y)
    return out


def par_de_voo(sc, src, alvo, livre=()):
    """Marca a fonte de um voo (a cópia herda): em voo ela é um texto do R5 que não conta contra a própria fonte nem contra o destino.
    livre: o desenho de onde o termo nasce ou onde pousa (a célula, a aresta): a saída/chegada por ele não é sobreposição."""
    ids = {id(y) for g in livre for y in g.get_family()}
    # a fonte costuma vir como .copy(): os textos da cena sob a fonte na partida são a origem do voo
    sx0, sy0, sx1, sy1 = _caixa_px(src)
    for top in sc.mobjects:
        for y in top.get_family():
            if getattr(y, "_txt", None) is None or not y.family_members_with_points():
                continue
            a0, b0, a1, b1 = _caixa_px(y)
            if min(a1, sx1 + 40) - max(a0, sx0 - 40) > 1 and min(b1, sy1 + 40) - max(b0, sy0 - 40) > 1:     # o rótulo do desenho de origem
                ids |= {id(z) for z in y.get_family()}
    # e os traços (régua, aresta, eixo) a até 40 px da fonte na partida: a saída pelo desenho de onde o termo nasce não é sobreposição
    for top in sc.mobjects:
        for y in top.family_members_with_points():
            if getattr(y, "_txt", None) is not None or (y.z_index or 0) <= -9 or not isinstance(y, VMobject) or y.get_stroke_width() < 0.5:
                continue
            P = y.points
            X, Y = P[:, 0] * 120 + 960, 540 - P[:, 1] * 120
            if np.any((X > sx0 - 40) & (X < sx1 + 40) & (Y > sy0 - 40) & (Y < sy1 + 40)):
                ids.add(id(y))
    for g in (src, alvo):
        ids |= {id(y) for y in g.get_family()}
        for d_ in donos_txt(sc, g):
            ids |= {id(y) for y in d_.get_family()}
    velho = (alvo, getattr(alvo, "_txt", None), getattr(alvo, "_par", None), sc)
    fam_ = {id(y) for y in alvo.get_family()} - {id(alvo)}
    sc._em_voo = getattr(sc, "_em_voo", set()) | fam_
    alvo._fam_voo = fam_
    # só glifo em voo é texto do R5; uma curva/aresta/célula em voo é traço (conta contra os textos que ela cruzar)
    glifo = getattr(alvo, "_tex", None) is not None or any(type(y).__name__ in ("VMobjectFromSVGPath", "SingleStringMathTex", "MathTex", "Text")
                                                           for y in alvo.get_family())
    if glifo:
        alvo._txt = velho[1] or ("voo: " + str(getattr(alvo, "_tex", "") or getattr(src, "_tex", "") or getattr(src, "_txt", "")))[:40]
    par = frozenset(ids)
    for y in alvo.get_family():
        y._par_l = par                      # traço em voo: a mesma origem liberada
    alvo._par = par
    return velho


def solta_par(_, velho):
    """Depois do play: o alvo pousou (volta a ser um glifo comum do seu texto)."""
    alvo, txt_, par_, sc = velho
    alvo._txt, alvo._par = txt_, par_
    for y in alvo.get_family():
        y._par_l = None
    sc._em_voo = getattr(sc, "_em_voo", set()) - getattr(alvo, "_fam_voo", set())


def r5b(self, onde="anim"):
    textos, dono = [], {}
    gm_par = getattr(self, "_gm_par", None)
    for m in self.mobjects:
        if m is self.wm:
            continue
        if type(m) is Mobject and gm_par is not None and m.family_members_with_points():
            textos.append(("glyph map", _caixa_px(m), m))             # v2: o contêiner do TransformByGlyphMap em movimento
            m._par = gm_par
            for g in m.get_family():
                dono[id(g)] = m
            continue
        for x in m.get_family():
            if getattr(x, "_txt", None) is None or _fora_r5(x):
                continue
            if any(y is not x and getattr(y, "_txt", None) is not None and x in y.get_family() for y in m.get_family()):
                continue
            if _opac(x) <= 0.15:
                continue
            ev = getattr(self, "_em_voo", set())
            fora = ev if (ev and getattr(x, "_par", None) is None) else frozenset()
            textos.append((x._txt, _caixa_px(x, fora), x))
            for g in x.get_family():
                dono[id(g)] = x
    linhas = []
    for m in self.mobjects:
        if m is self.wm or isinstance(m, (ValueTracker, ImageMobject)):
            continue
        for x in m.family_members_with_points():
            if not isinstance(x, VMobject) or id(x) in dono or (x.z_index or 0) <= -9 or (x.z_index or 0) == 31:   # 31: sublinhado de leitura
                continue
            if x.get_stroke_width() < 0.5 or x.get_stroke_opacity() <= 0.15 or _fora_r5(x):
                continue
            P = x.points
            if len(P) < 2:
                continue
            t = np.linspace(0, 1, 6)[:, None, None]
            Q = (P[:-1][None] * (1 - t) + P[1:][None] * t).reshape(-1, 3)
            linhas.append((type(x).__name__ + " " + ManimColor(x.get_stroke_color()).to_hex(), Q[:, 0] * 120 + 960, 540 - Q[:, 1] * 120, x))
    n = 0
    for i, (ta, (ax0, ay0, ax1, ay1), xa) in enumerate(textos):
        pa = getattr(xa, "_par", None) or frozenset()
        for tb, (bx0, by0, bx1, by1), xb in textos[i + 1:]:
            if xa in xb.get_family() or xb in xa.get_family():
                continue
            pb = getattr(xb, "_par", None) or frozenset()
            if id(xb) in pa or id(xa) in pb or (getattr(xa, "_grupo", None) is not None and getattr(xa, "_grupo", None) == getattr(xb, "_grupo", -1)):
                continue
            ox, oy = min(ax1, bx1) - max(ax0, bx0), min(ay1, by1) - max(ay0, by0)
            if ox > 2 and oy > 2:
                self._r5.append((self._aid, self.t, ta, tb, ox, oy))
                print(f"[R5] {self._aid} {self.t:7.2f}s {ta!r} x {tb!r} ({ox:.0f}x{oy:.0f} px) {onde}")
                n += 1
        for nome, X, Y, xl in linhas:
            if id(xl) in pa or id(xa) in (getattr(xl, "_par", None) or ()) or id(xa) in (getattr(xl, "_par_l", None) or ()):
                continue
            k = int(np.count_nonzero((X > ax0 + 2) & (X < ax1 - 2) & (Y > ay0 + 2) & (Y < ay1 - 2)))
            if k:
                if getattr(xa, "_par", None) is not None or getattr(xl, "_par_l", None) is not None:
                    # v2: termo em voo passando por cima de um traço do desenho (ou traço em voo sob um texto): travessia, listada à parte
                    self._r5v = getattr(self, "_r5v", []) + [(self._aid, self.t, ta, nome, k)]
                    print(f"[R5V] {self._aid} {self.t:7.2f}s {ta!r} atravessa {nome} ({k} pts) {onde}")
                    continue
                self._r5.append((self._aid, self.t, ta, nome, k, 0))
                print(f"[R5L] {self._aid} {self.t:7.2f}s {ta!r} x traço {nome} ({k} pts) {onde}")
                n += 1
    return n


_utt0 = B34.update_to_time


def _utt34(self, t):
    _utt0(self, t)
    if hasattr(self, "clk") and not getattr(self, "_sem_r5", False):
        c = self.clk.get_value()
        if c >= getattr(self, "_prox_r5", 0.0) - 1e-6:
            self._prox_r5 = round(c * FPS + 1) / FPS          # yt_0036 v2 (G10): todo quadro, também nas esperas
            r5b(self)


B34.update_to_time = _utt34
B34.r5 = r5b
