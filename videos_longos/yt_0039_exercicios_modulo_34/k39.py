"""yt_0039 · peças do vídeo sobre o v2kit (kit copiado do yt_0037). Macros de cor do EP. 14 (u/r laranja, v/θ verde-água, J lima, w lilás,
a âmbar e b magenta no E4, x̄ âmbar, ȳ e M_x magenta, m/k/ρ ciano), o ⊕ do centro de massa (cheio e vazado), a cadeia de degraus
(`cad`: cada degrau é um TransformByGlyphMap do MF-Tools com mapa explícito; a linha cresce para a direita e, sem espaço, desce com o '='
alinhado sob o primeiro '=' da linha de cima), a coluna (`linha`, `limpa_col`), os chips (`chip`), o selo PASSO n, a lupa e o papel do cartão.
Tudo em px de 1080p (PX), como no referencia/yt_0039_quadros_alvo_v1/sb39.html."""
from v2kit import *  # noqa: F401,F403
from v2kit import _ordem  # noqa: F401
import lib39 as _lib39

TEX31.add_to_preamble(
    r"\definecolor{lil}{HTML}{C9A7FF}"
    r"\def\U{\textcolor{rr}{u}}\def\V{\textcolor{th}{v}}\def\du{\textcolor{rr}{du}}\def\dv{\textcolor{th}{dv}}"
    r"\def\w{\textcolor{lil}{w}}\def\dw{\textcolor{lil}{dw}}\def\aa{\textcolor{ca}{a}}\def\bb{\textcolor{cm}{b}}"
    r"\def\Jl#1{\textcolor{lim}{#1}}\def\Rj{\textcolor{lim}{r}}\def\xb{\textcolor{ca}{\bar x}}\def\yb{\textcolor{cm}{\bar y}}"
    r"\def\Mx{\textcolor{cm}{M_x}}\def\mm{\textcolor{ci}{m}}\def\kk{\textcolor{ci}{k}}\def\th{\textcolor{th}{\theta}}\def\dth{\textcolor{th}{d\theta}}"
    r"\def\Lw#1{\textcolor{lil}{#1}}\def\Ag#1{\textcolor{th}{#1}}")

LIL = "#C9A7FF"
LAR, VAG, LIMA = RR, TH, LI
FUNDO_R = mixh(BG_, GEO, .30)            # região dos alvos (GEO a 30 % sobre o fundo)
_SEQ = [0]


# ── papel ────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def papel_tela(v, passo=None):
    """Grade da tela inteira nascendo dos eixos do palco v (quadradinho 0,25 da unidade do gráfico; passo forçado nos cartões)."""
    return papel(v, passo=passo).set_z_index(-10)


def papel_cartao():
    """Cartões sem gráfico (H2, A1, E5-3, S1, S2): grade de passo 0,5 nascendo do centro do cartão (vista u = 60 px ⇒ 30 px)."""
    return papel(Vw(960, 560, 60), passo=0.5).set_z_index(-10)


def papel_dois(v1, v2, xcorte=540):
    """Dois planos: cada um com a grade na sua metade, emenda vertical fina GEO em x = xcorte."""
    g1 = papel_meia(v1, 0, xcorte)
    g2 = papel_meia(v2, xcorte, 1920)
    em = lin_px([(xcorte, 150), (xcorte, 1080)], GEO, 2, alpha=.35, z=-9)
    return VGroup(g1, g2, em).set_z_index(-10)


# ── ⊕ do centro de massa (cm do sb39: disco com degradê ciano → magenta e cruz fina) e o centroide vazado ─────────────────────
def cm(X, Y, r=16, vaz=False, z=12):
    if vaz:
        c = Circle(radius=r / 120).move_to(PX(X, Y)).set_stroke(BR, W(3)).set_fill(BG_, 0.0)
        cor_cruz = BR
    else:
        c = Circle(radius=r / 120).move_to(PX(X, Y)).set_stroke(width=0)
        c.set_fill([CI, E2], 1)
        c.set_sheen_direction(DR)
        cor_cruz = BG_
    a = Line(PX(X - r * .62, Y), PX(X + r * .62, Y)).set_stroke(cor_cruz, W(3))
    b = Line(PX(X, Y - r * .62), PX(X, Y + r * .62)).set_stroke(cor_cruz, W(3))
    g = VGroup(c, a, b)
    sem_ctn(g).set_z_index(z)
    g._obst = True
    g._cm = "vazado" if vaz else "cheio"
    return g


# ── fórmulas por peças com chave automática ────────────────────────────────────────────────────────────────────────────
def LL(pecas, x, y, size=36, al="l"):
    pp = []
    for p in pecas:
        if isinstance(p, tuple):
            pp.append(p)
        else:
            _SEQ[0] += 1
            pp.append((f"_a{_SEQ[0]}", p))
    m = L(pp, x, y, size, al)
    m._pec, m._size, m._ult = pp, size, {k: k for k, _ in pp}
    return m


def g_(m, *ks):
    """Glifos das peças (chaves locais do último degrau ou chaves globais)."""
    out = []
    for k in ks:
        kk = m._ult.get(k, k) if hasattr(m, "_ult") else k
        out += sel(m, kk)
    return VGroup(*[m[0][i] for i in out])


def ix_(m, *ks):
    out = []
    for k in ks:
        kk = m._ult.get(k, k) if hasattr(m, "_ult") else k
        out += sel(m, kk)
    return out


def _eq_x(m):
    """x (px) do primeiro '=' (ou ⇒/≈) de uma linha: o glifo mais largo que alto na altura do centro, fora de fração."""
    for k, t in m._pec:
        if t.strip() in ("=", r"\Rightarrow", r"\ \Rightarrow\ ", r"\approx"):
            return pxof(m[0][sel(m, k)[0]].get_left())[0]
    return pxof(m.get_left())[0] + 40


def cad(sc, A, novas, mapa=(), n=0, rt=1.1, nota="", wrap=1860, gap=24, voos=(), desce=False, xq=None):
    """Degrau da conta: A (linha na tela) → A + novas. mapa = [(chave em A | '^local' do último degrau de A, chave local em novas)].
    Os glifos de `novas` fora do mapa e dos voos vão pela caneta. Sem espaço à direita (ou desce=True), o degrau desce para a linha de
    baixo, com o primeiro glifo alinhado ao primeiro '=' da linha de cima (A fica; o mapa vira cópia). Devolve a linha nova."""
    _SEQ[0] += 1
    s = _SEQ[0]
    loc, nv = {}, []
    for i, p in enumerate(novas):
        k, t = p if isinstance(p, tuple) else (None, p)
        u = f"{k or 'n'}#{s}.{i}"
        if k:
            loc[k] = u
        nv.append((u, t))

    def src(k):
        if isinstance(k, str) and k.startswith("^"):
            return A._ult.get(k[1:], k[1:])
        return k

    def dst(k):
        return loc.get(k, k)
    Xa, Ya = pxof(A.get_left())[0], pxof(A[0][0].get_center())[1]
    B = L(A._pec + nv, Xa, 0, A._size)
    B.shift(UP * (A[0][0].get_center()[1] - B[0][0].get_center()[1]))
    if not desce and _neq(A._pec) + _neq(nv) > 2:
        desce = True                                                   # v2 §4.1: no máximo 2 igualdades por linha
    cabe = pxof(B.get_right())[0] <= wrap and not desce
    vv = [(f, dst(k)) for f, k in voos]
    if cabe:
        pares = [(k, k) for k, _ in A._pec] + [(src(a), dst(b)) for a, b in mapa]
        B._pec, B._ult, B._size = A._pec + nv, loc, A._size
        B._xeq = getattr(A, "_xeq", None)
        gmap(sc, n, A, B, pares, voos=vv, rt=rt, copia=False, nota=nota)
        _troca_col(sc, A, B)
        return B
    X2 = xq if xq is not None else (getattr(A, "_xeq", None) or _eq_x(A))
    B = L(nv, X2, 0, A._size)
    yb_ = max(pxof(A.get_bottom())[1], sc.colY if A in sc.colms else pxof(A.get_bottom())[1])
    B.shift(UP * ((pxof(B.get_top())[1] - (yb_ + gap)) / 120))
    B._pec, B._ult, B._size, B._xeq = nv, loc, A._size, X2
    if pxof(B.get_bottom())[1] > 1010:
        print(f"[coluna-baixa] {sc._aid} degrau desce até y = {pxof(B.get_bottom())[1]:.0f} px")
    pares = [(src(a), dst(b)) for a, b in mapa]
    if pares:
        gmap(sc, n, A, B, pares, voos=vv, rt=rt, copia=True, nota=nota + " (desce)")
        na_ = {id(x) for t in sc.mobjects for x in t.get_family()}
        falta = sum(1 for x in A[0] if id(x) not in na_)
        if falta:
            print(f"[desce] {sc._aid} a linha de origem perdeu {falta} glifos no mapa em cópia: volta inteira")
            sc.add(A)
        # v2 B6: na linha de cima os termos cancelados ficam cinza e riscados (a história da conta); o degrau de baixo não os traz
    else:
        escreve_seq(sc, B, vv)
    col(B)
    sc.colms.append(B)
    sc.colY = max(sc.colY, pxof(B.get_bottom())[1])
    return B


def _some_cancelados(sc, A):
    """2º tempo do cancelamento quando a linha de origem fica (degrau que desce): os glifos que o `cancela` pôs em GEO saem."""
    geo = ManimColor(GEO).to_hex().upper()
    gs = [x for x in A[0] if x.get_fill_opacity() > .3 and ManimColor(x.get_fill_color()).to_hex().upper() == geo]
    if gs:
        sc.play(*[FadeOut(x) for x in gs], run_time=0.4)
        for x in gs:
            x.set_fill(opacity=0).set_stroke(opacity=0)
        sc.remove(*gs)


def _troca_col(sc, A, B):
    col(B)
    if A in sc.colms:
        sc.colms[sc.colms.index(A)] = B
    else:
        sc.colms.append(B)
    sc.colY = max(sc.colY, pxof(B.get_bottom())[1])


MARG_DIR = 1860
ESC = 1.25          # v2 §4.1: a conta da coluna maior que no v1 (≥ 15 %; 25 % para ocupar a altura útil)


def _neq(pecs):
    """Nº de igualdades (=, ≈, ⇒) nas peças de uma linha (v2 §4.1: no máximo 2 por linha)."""
    return sum(t.count("=") + t.count(chr(92) + "approx") + t.count(chr(92) + "Rightarrow") for _, t in pecs)


def linha(sc, pecas, size=36, x=None, gap=26, voos=(), escreve=True, y=None, rot=None, rot_cor=GEO, rt_voo=0.9, esc=True):
    """Linha nova na coluna, abaixo da última (topo a `gap` px). `rot` = texto à esquerda (selo PASSO n ou palavra) em Space Grotesk."""
    size = round(size * ESC) if esc else size
    gap = round(gap * ESC) if esc else gap
    X = x if x is not None else sc.colX
    r = None
    if rot:
        r = T(rot, X, 0, 26, "left", rot_cor, bold=False)
        X = pxof(r.get_right())[0] + 16
    m = LL(pecas, X, 0, size)
    top = (y - m.height * 60) if y is not None else sc.colY + gap
    m.shift(UP * ((pxof(m.get_top())[1] - top) / 120))
    if r is not None:
        r.shift(UP * ((pxof(r.get_center())[1] - pxof(m[0][0].get_center())[1]) / 120))
        r._col = True
        sc.colms.append(r)
    ov = pxof(m.get_right())[0] - MARG_DIR                             # C4: margem direita da coluna ≥ 60 px
    if ov > 0:
        m.shift(LEFT * ov / 120)
        if r is not None:
            r.shift(LEFT * ov / 120)
        print(f"[margem] {sc._aid} linha deslocada {ov:.0f} px para a esquerda")
    col(m)
    sc.colms.append(m)
    sc.colY = pxof(m.get_bottom())[1]
    if sc.colY > 1010:
        print(f"[coluna-baixa] {sc._aid} linha termina em y = {sc.colY:.0f} px")
    if escreve:
        if r is not None:
            sc.pena(r)
        escreve_seq(sc, m, voos, rt_voo=rt_voo)
    return (m, r) if rot else m


def palavra(sc, s, cor=GEO, size=26, x=None, gap=22, escreve=True):
    """Palavra solta na coluna (DE DENTRO, DE FORA, ESTIMATIVA…): Space Grotesk, ≥ 26 px."""
    X = x if x is not None else sc.colX
    t = T(s, X, 0, size, "left", cor, bold=False)
    t.shift(UP * ((pxof(t.get_top())[1] - (sc.colY + gap)) / 120))
    t._col = True
    sc.colms.append(t)
    sc.colY = pxof(t.get_bottom())[1]
    if escreve:
        sc.pena(t)
    return t


def _na_cena_por_glifo(sc, ms):
    """Objetos da cena que contêm algum glifo/traço de ms (a linha inteira, as partes da caneta e as cópias pousadas)."""
    alvo = set()
    for m in ms:
        alvo |= {id(x) for x in m.family_members_with_points()}
        for p_ in getattr(m, "_partes", []) or []:
            alvo |= {id(x) for x in p_.family_members_with_points()}
    fix = sc.fixos()
    return [m for m in sc.mobjects if m not in fix and not isinstance(m, ValueTracker) and any(id(x) in alvo for x in m.family_members_with_points())]


def tira(sc, *ms, rt=0.35):
    vis = _na_cena_por_glifo(sc, ms)
    if vis:
        sc.play(*[FadeOut(m) for m in vis], run_time=rt)
        for m in vis:
            m.clear_updaters()
        sc.remove(*vis)


def sobe_col(sc, sair, y0=None, rt=0.6):
    """v2 §4.1 (coluna maior): as linhas `sair` saem e o resto da coluna sobe até o topo y0 (px), num movimento só."""
    tira(sc, *sair, rt=0.35)
    sc.colms = [m for m in sc.colms if m not in sair]
    resto = [m for m in sc.colms if m in sc.mobjects]
    vis = _na_cena_por_glifo(sc, resto) if resto else []
    if not vis:
        sc.colY = sc.colY0
        return
    y0 = sc.colY0 if y0 is None else y0
    dy = min(pxof(m.get_top())[1] for m in vis) - y0
    if dy > 2:
        sc.play(*[m.animate.shift(UP * dy / 120) for m in vis], run_time=rt)
        sc.colY -= dy


def limpa_col(sc, keep=(), rt=0.4):
    sai = [m for m in sc.colms if m not in keep]
    vis = _na_cena_por_glifo(sc, sai)
    kk = {id(x) for k in keep for x in k.family_members_with_points()}
    vis = [m for m in vis if not any(id(x) in kk for x in m.family_members_with_points())]
    if vis:
        sc.play(*[FadeOut(m) for m in vis], run_time=rt)
        sc.remove(*vis)
    sc.colms = [m for m in sc.colms if m in keep]
    sc.colY = sc.colY0


def ok_ao_lado(sc, m, dx=36, cor=MEN):
    """✓ menta à direita de m (nasce num traço)."""
    c = check_px(pxof(m.get_right())[0] + dx, pxof(m.get_center())[1], cor, .9)
    sc.play(Create(c), run_time=0.4)
    sc.colms.append(c)
    return c


def leg_ao_lado(sc, m, s, cor=MEN, dx=24, size=28):
    t = T(s, pxof(m.get_right())[0] + dx, pxof(m.get_center())[1] + size * .35, size, "left", cor)
    sc.pena(t)
    sc.colms.append(t)
    return t


# ── chips: o resultado reaproveitado sobe para o topo (moldura GEO a 70 %, raio 10) ───────────────────────────────────────────
CHIP_Y = 90
CHIP_XMAX = 1600


def chip(sc, tex, X, Y=None, de=None, nome=None, size=30, nome_cor=GEO, some=()):
    """Resultado reaproveitado: chip na linha dos chips (y = 90 px, v2 A9/A10), moldura com folga interna ≥ 14 px."""
    Y = CHIP_Y if Y is None or Y in (175, 180) else Y
    m = TC(tex, X + 16, Y, size, "l")
    x1_ = pxof(m.get_corner(DR))[0]
    if x1_ + 14 > CHIP_XMAX:                                           # C3: zona do logo reservada (x ≥ 1640): borda direita do chip ≤ 1600
        m.shift(LEFT * (x1_ + 14 - CHIP_XMAX) / 120)
    x0, y0 = pxof(m.get_corner(UL))
    x1, y1 = pxof(m.get_corner(DR))
    mol = moldura_de(m, x0 - 14, y0 - 10, x1 - x0 + 28, y1 - y0 + 20, GEO, .7, 2, 10)
    nm = None
    if nome:
        nm = T(nome, x1 + 30, (y0 + y1) / 2 + 9, 26, "left", nome_cor, bold=False)
    if de is not None:
        vis = _na_cena_por_glifo(sc, list(some)) if some else []
        voos(sc, [(de, m)], rt=1.0, extra=[FadeOut(x) for x in vis])
        if vis:
            sc.remove(*vis)
            sc.colms = [c for c in sc.colms if c not in some]
        sc.play(Create(mol), run_time=0.3)
    else:
        sc.pena(m)
        sc.play(Create(mol), run_time=0.3)
    if nm is not None:
        sc.pena(nm)
    g = VGroup(mol, m) if nm is None else VGroup(mol, m, nm)
    g.m, g.mol = m, mol
    sc.chs.append(g)
    return g


def tira_chips(sc, *gs, rt=0.35):
    gs = gs or tuple(sc.chs)
    vis = [x for g in gs for x in g if x in sc.mobjects] + [g for g in gs if g in sc.mobjects]
    if vis:
        sc.play(*[FadeOut(x) for x in vis], run_time=rt)
        sc.remove(*vis)
    for g in gs:
        if g in sc.chs:
            sc.chs.remove(g)


# ── palco ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
def eixos_c(v, a0, a1, b0, b1, lx=r"\X", ly=r"\Y", cx=E1, cy=E2, size=32):
    """eixosC do sb39: setas âmbar/magenta de a0 a a1 e de b0 a b1; x à direita da ponta, y acima da ponta."""
    sx = seta_px(v.px(a0, 0), v.px(a1, 0), cx, 3, 16, z=6)
    sy = seta_px(v.px(0, b0), v.px(0, b1), cy, 3, 16, z=6)
    A, B = v.px(a1, 0), v.px(0, b1)
    Lx = TC(lx, A[0] + 22, A[1], size, "c")
    Ly = TC(ly, B[0], B[1] - 26, size, "c")
    return sx, sy, Lx, Ly


def tk(v, eixo, val, tex, size=28):
    """Marca no eixo: traço GEO de 14 px + número (MathTex) com folga >= 12 px do traço (R5)."""
    if eixo == "x":
        q = v.px(val, 0)
        tr = lin_px([(q[0], q[1] - 7), (q[0], q[1] + 7)], GEO, 2, z=6)
        lb = TC(tex, q[0], q[1] + (48 if "frac" in tex else 32), size, "c")
    else:
        q = v.px(0, val)
        tr = lin_px([(q[0] - 7, q[1]), (q[0] + 7, q[1])], GEO, 2, z=6)
        lb = TC(tex, q[0] - 22, q[1], size, "r")
    return tr, lb


def pronto(*ms):
    """Alvo de ReplacementTransform/Transform que entra já escrito (não é caneta nova): libera do portão FLASH."""
    for m in ms:
        for x in m.get_family():
            if getattr(x, "_caneta", False):
                x._esc = True
    return ms[0] if len(ms) == 1 else ms


def monta_palco(sc, v, a0, a1, b0, b1, ticks=(), lx=r"\X", ly=r"\Y", cx=E1, cy=E2, grade=True, rt=0.6, extra=(), passo=None):
    """Grade da tela inteira + eixos + marcas (os números pela caneta). Devolve dict."""
    g = papel_tela(v, passo) if grade else None
    sx, sy, Lx, Ly = eixos_c(v, a0, a1, b0, b1, lx, ly, cx, cy)
    tks = [tk(v, e, val, tex) for e, val, tex in ticks]
    an = [GrowFromPoint(sx, v.P(0, 0)), GrowFromPoint(sy, v.P(0, 0)), *[Create(t[0]) for t in tks], *extra]
    if g is not None:
        sc.grade = g
        an.insert(0, FadeIn(g))
    sc.play(*an, run_time=rt)
    sc.pena(Lx, Ly, *[t[1] for t in tks], lag=0.04)
    return {"g": g, "sx": sx, "sy": sy, "lx": Lx, "ly": Ly, "tk": tks, "todos": [sx, sy, Lx, Ly] + [p for t in tks for p in t]}


def arcoP(r, t0=0.0, t1=PI, n=120, c=(0.0, 0.0)):
    return [(c[0] + r * math.cos(t0 + (t1 - t0) * k / n), c[1] + r * math.sin(t0 + (t1 - t0) * k / n)) for k in range(n + 1)]


def arruela(v, r0=1.0, r1=2.0, fill=FUNDO_R, z=1, n=120):
    pts = arcoP(r1, n=n) + arcoP(r0, n=n)[::-1]
    return poly_px([v.px(*p) for p in pts], fill, 1.0, z=z)


def meia_lua_mapa(v, r0, r1, dens, vmax, z=1, sup=2.0):
    """Mapa radial (imagem calculada uma vez) da meia arruela/meio disco r0 ≤ r ≤ r1, y ≥ 0: cor #10243A → ciano por dens(r)/vmax."""
    X0, Y1 = v.px(-r1, r1)
    X1, Y0 = v.px(r1, 0)
    w, h = int(round((X1 - X0) * sup)), int(round((Y0 - Y1) * sup))
    xs = -r1 + (np.arange(w) + .5) / w * 2 * r1
    ys = r1 - (np.arange(h) + .5) / h * r1
    Xg, Yg = np.meshgrid(xs, ys)
    Rg = np.hypot(Xg, Yg)
    t = np.clip(dens(Rg) / vmax, 0, 1) ** .85
    rgb = hx("#10243A") * (1 - t[..., None]) + hx(CI) * t[..., None]
    a = np.where((Rg >= r0) & (Rg <= r1), 255.0, 0.0)[..., None]
    return img_px(np.concatenate([rgb, a], 2), X0, Y1, X1 - X0, Y0 - Y1, z=z)


def mapa_y(v, xs_fn, y0, y1, dens, vmax, z=1, sup=2.0, xr=1.0):
    """Mapa em faixas horizontais (imagem) da região |x| ≤ xs_fn(y), y0 ≤ y ≤ y1: cor por dens(y)/vmax."""
    X0, Y1 = v.px(-xr, y1)
    X1, Y0 = v.px(xr, y0)
    w, h = int(round((X1 - X0) * sup)), int(round((Y0 - Y1) * sup))
    xs = -xr + (np.arange(w) + .5) / w * 2 * xr
    ys = y1 - (np.arange(h) + .5) / h * (y1 - y0)
    Xg, Yg = np.meshgrid(xs, ys)
    t = np.clip(dens(Yg) / vmax, 0, 1) ** .85
    rgb = hx("#10243A") * (1 - t[..., None]) + hx(CI) * t[..., None]
    a = np.where(np.abs(Xg) <= xs_fn(Yg), 255.0, 0.0)[..., None]
    return img_px(np.concatenate([rgb, a], 2), X0, Y1, X1 - X0, Y0 - Y1, z=z)


def placa_t(s, X, Y, cor=BR, size=28, al="left"):
    """Rótulo de palavra com placa (placaTxt do sb: Y = linha de base)."""
    return TPt(s, X, Y, max(26, size), cor, {"l": "left", "c": "center", "r": "right", "left": "left", "center": "center", "right": "right"}[al])


def rot_m(v, tex, p, dx=0, dy=0, size=28, al="l", placa=True):
    q = v.px(*p)
    return TP(tex, q[0] + dx, q[1] + dy, size, al) if placa else TC(tex, q[0] + dx, q[1] + dy, size, al)


def pausa_sel(X, Y):
    """PAUSE E TENTE (moldura menta, texto menta 26 px), como o pausa() do sb39."""
    t = T("PAUSE E TENTE", X + 16, Y + 2, 26, "left", MEN, bold=True)
    w = t.width * 120 + 32
    mol = moldura_de(t, X, Y - 30, w, 46, MEN, 1.0, 2, 10)
    return mol, t


def poe_pausa(sc, X, Y):
    mol, t = pausa_sel(X, Y)
    sc.pena(t)
    sc.play(Create(mol), run_time=0.3)
    g = VGroup(mol, t)
    sc.colms.append(g)
    return g


def chave_txt(sc, ch, partes, X, Y, S=30):
    """Chave + rótulo misto (mixl) escrito a caneta."""
    lab = mixl(partes, X, Y, S)
    sc.play(Create(ch), run_time=0.4)
    sc.pena(*lab.p, lag=0.05)
    return lab


def icone_bola(X, Y, R=46, oca=False, cor=GEO):
    c = circ_px(X, Y, R, cor, 2.5, z=6)
    if oca:
        d = circ_px(X, Y, R * .48, cor, 2.5, dash=(5, 5), z=6)
        return VGroup(c, d)
    e = Ellipse(width=2 * R / 120, height=2 * 14 / 120).move_to(PX(X, Y)).set_stroke(cor, W(2.5)).set_fill(opacity=0)
    return VGroup(c, sem_ctn(e).set_z_index(6))


def icone_oitavo(X, Y, R=46, cor=GEO):
    """Bola cortada em oito (traço): círculo, a elipse do equador e o meridiano."""
    c = circ_px(X, Y, R, cor, 2.5, z=6)
    e = sem_ctn(Ellipse(width=2 * R / 120, height=2 * 14 / 120).move_to(PX(X, Y)).set_stroke(cor, W(2.5)).set_fill(opacity=0)).set_z_index(6)
    m = sem_ctn(Ellipse(width=2 * 14 / 120, height=2 * R / 120).move_to(PX(X, Y)).set_stroke(cor, W(2.5)).set_fill(opacity=0)).set_z_index(6)
    return VGroup(c, e, m)


def lupa_moldura(X, Y, R):
    return circ_px(X, Y, R, GEO, 2.5, z=14)


def selo_t(s, X, Y, cor=GEO, size=26):
    """Selo de palavra (moldura fina na cor) — Y = linha de base do texto."""
    t = T(s, X + 14, Y, size, "left", cor, bold=False)
    w = t.width * 120 + 28
    mol = moldura_de(t, X, Y - size - 4, w, size + 18, cor, 1.0, 2, 8)
    return mol, t


def poe_selo_t(sc, sl):
    sc.pena(sl[1])
    sc.play(Create(sl[0]), run_time=0.3)
    return VGroup(*sl)


_gmap_kit = gmap


def gmap(sc, n, A, B, pares, voos=(), rt=1.2, copia=True, nota="", extra=()):
    """gmap do kit + limpeza: no modo cópia o MF-Tools deixa na cena as cópias dos glifos da origem (brancas, por cima do destino);
    todo objeto que entrou durante o mapa e não é A, B ou parte de B sai."""
    antes = {id(m) for m in sc.mobjects}
    r = _gmap_kit(sc, n, A, B, pares, voos=voos, rt=rt, copia=copia, nota=nota, extra=extra)
    fb = {id(x) for x in B.get_family()}
    fa = {id(x) for x in A.get_family()}
    lixo = [m for m in sc.mobjects if id(m) not in antes and m is not B and not ({id(x) for x in m.family_members_with_points()} <= fb)
            and not (copia and {id(x) for x in m.family_members_with_points()} <= fa and m is A)]
    lixo = [m for m in lixo if isinstance(m, VMobject) and getattr(m, "_tex", None) is None]
    if lixo and not os.environ.get("SEM_LIXO"):
        print(f"[lixo] {sc._aid} removidos {len(lixo)}: {[type(m).__name__ + str(len(m.family_members_with_points())) for m in lixo][:6]}")
        sc.remove(*lixo)
    _fim_cancela(sc)
    return r


import v2kit as _v2k0
_TFC_init = TransformFromCopy.__init__


_COLX = [1100]


def _tfc_init(self, mobject, target_mobject, *a, **k):
    """Todo voo (TransformFromCopy) registra a caixa da fonte (QA §7.1). v2 A6: voo DENTRO da coluna que sobe/desce mais de 200 px (chip,
    termo reaproveitado lá de cima) contorna a coluna pela esquerda (curva até x ≈ colX − 40) em vez de atravessar as linhas do meio."""
    try:
        _v2k0.VOO_SRC.append(_v2k0._caixa(mobject))
        s, t = pxof(mobject.get_center()), pxof(target_mobject.get_center())
        cx = _COLX[0]
        if s[0] > cx - 30 and t[0] > cx - 30 and abs(s[1] - t[1]) > 200 and "path_func" not in k:
            hw = max(mobject.width, target_mobject.width) * 60
            B = (s[0] + t[0]) / 2 + hw - (cx - 30)
            if B > 0:
                k.pop("path_arc", None)
                Bm = B / 120
                k["path_func"] = lambda st, en, al, Bm=Bm: st + (en - st) * al + np.array([-Bm * np.sin(np.pi * al), 0, 0])
    except Exception:
        pass
    _TFC_init(self, mobject, target_mobject, *a, **k)


TransformFromCopy.__init__ = _tfc_init


class B39x(B39):
    """Base do EP. 14: coluna (colX, colY0), chips; canto de duas linhas (ANTES = a linha 2 do primeiro quadro)."""
    COLX, COLY0 = 1100, 250

    def gat(self, frase):
        super().gat(frase)
        # recuperação de atraso (handoff final §6.4): se a cena já passou da palavra, os play seguintes encolhem até o próximo gatilho
        try:
            kk = self._k_frase(self._aid, frase)
            alvo = self._q0 + max(0.0, ANC[self._aid]["t"][kk] - LEAD) * FPS
            self._deb = max(0.0, (self.nq - alvo) / FPS)
        except Exception:
            self._deb = 0.0

    def play(self, *a, **k):
        _COLX[0] = getattr(self, "colX", 1100)
        d = getattr(self, "_deb", 0.0)
        if d > 0.35:
            f = max(0.3, 1.0 - d / 3.0)
            for x in a:
                if hasattr(x, "run_time") and getattr(x, "run_time", None):
                    x.run_time = max(0.25, x.run_time * f)
            if k.get("run_time"):
                k["run_time"] = max(0.25, k["run_time"] * f)
        r = super().play(*a, **k)
        _v2k0.VOO_SRC.clear()
        return r

    def setup_base(self):
        super().setup_base()
        self.colX, self.colY0 = self.COLX, self.COLY0
        self.colY = self.colY0
        self.colms, self.chs = [], []

    def fixos(self):
        f = set(super().fixos())
        for g in getattr(self, "chs", []):
            f |= {g, *g.submobjects}
        return f

    def marca(self, alvo, agora=True):
        """Instante do quadro-alvo: o estado completo agora (+0,3 s), não o fim da âncora (a construção pode esticar além da fala)."""
        print(f"[marca] {alvo} {self.nq / FPS + 0.3:.3f}")

    def leitura(self, *gs, rt=1.2):
        """Sublinhado de leitura (a voz lê o símbolo): traço branco fino sob os glifos, aparece e sai."""
        acende(self, *[(g, BR) for g in gs], rt=rt)


def linha_de(sc, A, pecas, mapa, n=0, size=None, rot=None, rot_cor=GEO, x=None, gap=26, rt=1.2, nota="", voos=(), y=None):
    """Linha nova na coluna que NASCE de A por glyph map (cópia: A fica). mapa = [(chave em A | '^local', chave em B)]; o resto pela caneta."""
    B = linha(sc, pecas, round(size * ESC) if size else A._size, x=x, gap=round(gap * ESC), escreve=False, rot=rot, rot_cor=rot_cor, y=y, esc=False)
    m, r = (B if rot else (B, None))
    if r is not None:
        sc.pena(r)
    pares = [((A._ult.get(a[1:], a[1:]) if isinstance(a, str) and a.startswith("^") else a), b) for a, b in mapa]
    gmap(sc, n, A, m, pares, voos=voos, rt=rt, copia=True, nota=nota)
    return B


def lims(m, key):
    """(índices do limite de baixo, de cima) de uma peça ∫_a^b (o ∫ é o glifo mais alto)."""
    return lims_de(m, m._ult.get(key, key) if hasattr(m, "_ult") else key)


def frac_ix(m, key):
    """(numerador, traço, denominador) de uma peça com dfrac, por geometria (índices em ordem de x)."""
    fora, num, bar, den = frac_partes(m, m._ult.get(key, key) if hasattr(m, "_ult") else key)
    return num, bar, den


def G(m, idx):
    return VGroup(*[m[0][i] for i in idx])


def cor_glifos(sc, gs, cor, rt=0.5):
    sc.play(*[g.animate.set_color(cor) for g in gs], run_time=rt)


def cancela(sc, *gs, rt=0.5):
    """1º tempo do cancelamento (v2 B6): o par acende em GEO junto e recebe um risco fino coral na diagonal (o 2º tempo é o degrau
    seguinte, que não mapeia esses glifos; o risco sai com eles)."""
    rs = []
    for g in gs:
        a, b = g.get_corner(DL), g.get_corner(UR)
        rs.append(Line(a + (a - b) * .08, b + (b - a) * .08).set_stroke(CORAL, W(2.2)).set_z_index(31))
    sc.play(*[g.animate.set_color(GEO) for g in gs], *[Create(r) for r in rs], run_time=rt)
    sc._riscos = getattr(sc, "_riscos", []) + rs
    sc._canc = getattr(sc, "_canc", []) + [x for g in gs for x in g]
    sc.colms += rs


def _fim_cancela(sc, rt=0.4):
    """C1 (handoff final): os fatores cancelados e os riscos saem JUNTOS no fim do degrau que os substitui (nunca ficam depois que a linha
    seguinte nasceu). Se a linha de origem foi trocada (sem cópia), os glifos já não estão na cena e só os riscos saem."""
    rs = [r for r in getattr(sc, "_riscos", []) if r in sc.mobjects]
    viv = {id(x) for m in sc.mobjects for x in m.get_family()}
    gl = [x for x in getattr(sc, "_canc", []) if id(x) in viv and x.get_fill_opacity() > .05]
    if rs or gl:
        sc.play(*[FadeOut(x) for x in rs + gl], run_time=rt)
        sc.remove(*rs)
        for x in gl:
            x.set_fill(opacity=0).set_stroke(opacity=0)
    sc._riscos, sc._canc = [], []
    sc.colms = [m for m in sc.colms if m not in rs]


def _tira_riscos(sc, rt=0.3):
    rs = [r for r in getattr(sc, "_riscos", []) if r in sc.mobjects]
    if rs:
        sc.play(*[FadeOut(r) for r in rs], run_time=rt)
        sc.remove(*rs)
    sc._riscos = []


# ── v2 B1 · O MAPA EM AÇÃO: a região com uma grade fina deformada continuamente pelo mapa (uma vez, ~2,5 s) ─────────────────────
def celulas(p0, p1, q0, q1, npp, nq, k=10, qlo=None, qhi=None):
    """Células da grade no espaço dos parâmetros (p, q): [(i, j, anel de pontos)]. qlo/qhi(p) = bordas variáveis em q (q vira fração)."""
    out = []
    for i in range(npp):
        pa, pb = p0 + (p1 - p0) * i / npp, p0 + (p1 - p0) * (i + 1) / npp
        for j in range(nq):
            sa, sb = j / nq, (j + 1) / nq

            def Q(p, s):
                lo_ = qlo(p) if qlo else q0
                hi_ = qhi(p) if qhi else q1
                return lo_ + (hi_ - lo_) * s
            ps = [pa + (pb - pa) * t / k for t in range(k + 1)]
            ss = [sa + (sb - sa) * t / k for t in range(k + 1)]
            anel = [(p, Q(p, sa)) for p in ps] + [(pb, Q(pb, s)) for s in ss[1:]] + [(p, Q(p, sb)) for p in ps[::-1][1:]] + [(pa, Q(pa, s)) for s in ss[::-1][1:]]
            out.append((i, j, anel))
    return out


class MapaAcao:
    """Grade de células (fill + traço fino GEO) cujos pontos seguem pos(p, q, α) → (X, Y) px. `teste` = {(i, j): cor} (células de teste
    coloridas, a leitura do jacobiano como razão de áreas). anim(rt) é UMA animação (UpdateFromAlphaFunc), sem updater permanente."""

    def __init__(self, cels, pos, fill=FUNDO_R, fop=.85, teste=None, z=3, wpx=1.1):
        self.cels, self.pos, self.teste = cels, pos, teste or {}
        self.g = VGroup()
        for i, j, anel in cels:
            c = self.teste.get((i, j), fill)
            m = VMobject().set_fill(c, fop if (i, j) not in self.teste else .95).set_stroke(GEO, W(wpx), opacity=.75)
            m._anel = anel
            self.g.add(m)
        sem_ctn(self.g).set_z_index(z)
        self.at(0.0)

    def at(self, a):
        for m in self.g:
            pts = [PX(*self.pos(p, q, a)) for p, q in m._anel]
            m.set_points_as_corners(pts + [pts[0]])
        return self.g

    def anim(self, rt=2.5, rate=smooth):
        return UpdateFromAlphaFunc(self.g, lambda m, a: self.at(rate(a)), run_time=rt)

    def so_linhas(self):
        return [m.animate.set_fill(opacity=0) for m in self.g]


def palco_sai(sc, keep=(), xmax=1090, rt=0.0, extra=()):
    """Tudo o que não é fixo (canto, chips) e está no palco (centro x < xmax px) e não está em `keep` sai: as cópias soltas dos voos também.
    rt = 0: devolve a lista de FadeOut para entrar num play junto com a troca; rt > 0: sai já."""
    ks = set()
    for k in keep:
        ks |= {id(x) for x in k.get_family()}
    fix = sc.fixos()
    sai = []
    for m in list(sc.mobjects):
        if m in fix or isinstance(m, ValueTracker) or m is sc.grade or id(m) in ks or type(m).__name__ == "Fundo3D":
            continue
        try:
            if pxof(m.get_center())[0] < xmax:
                sai.append(m)
        except Exception:
            continue
    if rt > 0:
        if sai or extra:
            sc.play(*[FadeOut(m) for m in sai], *extra, run_time=rt)
        for m in sai:
            m.clear_updaters()
        sc.remove(*sai)
        return []
    return sai



# ── 3D: os mesmos pontos nomeados do c39.js (mundo), para o QA de alinhamento e os rótulos presos ─────────────────────────
import v39 as _v39


def pontos39(cena, e):
    if cena == "massa":
        return {"ex": (1.12, 0, 0), "ey": (0, .78, 0)} if e.get("forma", "elipse") == "elipse" else {"ex": (2.4, 0, 0), "ey": (0, 2.45, 0)}
    sm_ = lambda u: (lambda w: w * w * (3 - 2 * w))(min(1.0, max(0.0, u)))
    if cena == "octante":
        SC = e.get("SC", 2.4)
        cr = max(1e-3, sm_(e.get("casca", 1.0)))
        lx, lz, zl = e.get("lx", SC + .55), e.get("lz", SC + .5), e.get("zl", 1.0)
        Sp = lambda ph, th: (SC * math.sin(ph) * math.cos(th), SC * math.sin(ph) * math.sin(th), SC * math.cos(ph) * cr)
        return {"ex": (lx + .2, 0, 0), "ey": (0, lx + .2, 0), "ez": (0, 0, lz * zl + .22), "a_x": (SC, 0, 0), "a_y": (0, SC, 0), "a_z": (0, 0, SC * cr),
                "origem": (0, 0, 0), "casca": Sp(math.pi / 4.2, math.pi / 4)}
    forma = e.get("forma", "md")
    SC = 2.2 if forma == "md" else (1.15 if forma == "arr" else 1.0)
    PH = e.get("phi", 0.0)
    Gf = lambda x, s_, ph: (x, s_ * math.sin(ph), s_ * math.cos(ph))
    XM = 2.0 if forma == "toro" else (SC + .9 if forma == "md" else 2 * SC + .7)
    P = {"eixo_fim": (XM + .2, 0, 0), "centro": (0, 0, 0)}
    if forma == "md":
        y0, xq = .6 * SC, -.55
        P.update({"quad": Gf(xq, y0, PH), "anel_topo": Gf(xq, y0, PH + math.pi), "anel_frente": Gf(xq, y0, PH + 1.5 * math.pi), "chapa_topo": Gf(0, SC, PH),
                  "borda_dir": (SC, 0, 0), "cm": Gf(0, e.get("cfrac", 4 / (3 * math.pi)) * SC, PH), "quad_dir": Gf(xq + .16, y0, PH)})
    if forma == "arr":
        yb = 28 / (9 * math.pi) * SC
        P.update({"cm": Gf(0, yb, PH), "cm_ini": Gf(0, yb, 0), "cm_fim": Gf(0, yb, PH), "oco": Gf(0, SC * .55, PH * .62), "r1": Gf(SC, 0, PH), "r2": Gf(2 * SC, 0, PH),
                  "topo": Gf(0, 2 * SC, PH), "circ_frente": Gf(0, yb, math.pi / 2), "circ_baixo": Gf(0, yb, math.pi)})
    if forma == "toro":
        P.update({"centro_disco": Gf(0, 2 * SC, PH), "topo_disco": Gf(0, 3 * SC, PH), "base_disco": Gf(0, SC, PH), "circ_baixo": Gf(0, 2 * SC, math.pi),
                  "circ_frente": Gf(0, 2 * SC, math.pi / 2)})
    return P


_v39.pontos3d = pontos39


def cam_oct():
    """Câmera do alvo 06 (octante): ver([11.5, 5.2, 7.6], [0.42·SC, 0.42·SC, 0.28·SC], 600, 580) com o enquadramento do alvo (0,9 e +40, +95)."""
    SC = 2.4
    return cam_esc((11.5, 5.2, 7.6), (.42 * SC, .42 * SC, .28 * SC), 600, 580, .9, 40, 95)


CAM_PAP = cam_dict((8.8, -15.5, 7.2), (0, 0, .25), (0, 0, 1), 640, 560)
CAM_TORO = cam_dict((9.6, -16.7, 7.9), (0, 0, .2), (0, 0, 1), 600, 560)      # C12: disco gerador x1,8 e centrado no palco


def cam_incl(tgt, d, el=32, az=-35, cx=960, cy=560, fov=22):
    e, a = math.radians(el), math.radians(az)
    pos = [tgt[0] + d * math.cos(e) * math.sin(a), tgt[1] - d * math.cos(e) * math.cos(a), tgt[2] + d * math.sin(e)]
    return cam_dict(pos, tgt, (0, 0, 1), cx, cy, fov)


CAM_M43 = cam_incl((0, .25, .3), 6.6, cx=560, cy=620)           # B3: meia elipse ρ = k y (aprovado nos stills)
CAM_M54 = cam_incl((0, .9, .35), 13.5, cx=540, cy=620)          # B3: meia arruela ρ = k r


def massa_entra(sc, forma, cam, k1, cx1, cy1, esconde, lx2, ly2, H=None, rt=1.5):
    """B3 (massa como volume): no mesmo quadro o 2D sai e entra a cena 3D `massa` vista de cima ortográfica (alt = 0, idêntica ao 2D);
    em `rt` s a câmera inclina e a chapa ganha a altura ρ. Os rótulos x e y ficam presos às pontas dos eixos 3D."""
    ini = {"forma": forma, "alt": 0.0}
    if H:
        ini["H"] = float(H)
    pal = Palco37(sc, "massa", cam, **ini)
    pal.fundo.set_z_index(-5)
    pal.sobe(k1, cx1, cy1)
    pal.tr["s"].set_value(1.0)
    sc.add(pal.fundo)
    qx, qy = pal.pt("ex"), pal.pt("ey")
    lx3 = pal.prende(TC(r"\X", 0, 0, 32, "c"), "ex", pxof(lx2.get_center())[0] - qx[0], pxof(lx2.get_center())[1] - qx[1])
    ly3 = pal.prende(TC(r"\Y", 0, 0, 32, "c"), "ey", pxof(ly2.get_center())[0] - qy[0], pxof(ly2.get_center())[1] - qy[1])
    pronto(lx3, ly3)
    sc.remove(*[m for m in esconde if m in sc.mobjects], lx2, ly2)
    sc.add(lx3, ly3)
    print(f"[pouso3d] {sc.lote} {sc._aid} massa/{forma} entrada quadro {sc.nq} (2D → 3D, vista de cima)")
    sc.play(*pal.anim(rt, s=0.0), *pal.anim(rt, alt=1.0), run_time=rt)
    return pal, lx3, ly3


def massa_volta(sc, pal, entram, lx3, ly3, lx2, ly2, rt=2.0):
    """B3: a câmera volta à vista de cima ortográfica e a chapa desce a alt = 0; no último quadro o PNG 3D sai e o 2D entra por cima."""
    sc.play(*pal.anim(rt, s=1.0), *pal.anim(rt, alt=0.0), run_time=rt)
    print(f"[pouso3d] {sc.lote} {sc._aid} massa pouso quadro {sc.nq} (3D → 2D, vista de cima)")
    for m in (lx3, ly3):
        m.clear_updaters()
    sc.remove(lx3, ly3)
    troca_para_2d(sc, pal, list(entram) + [lx2, ly2])


def tira_presos(sc, rt=0.3):
    """Rótulos presos ao 3D (prende) saem junto com o seu objeto (R4), em qualquer posição da tela."""
    ms = [m for m in sc.mobjects if any(getattr(y, "_preso", False) for y in m.get_family())]
    for m in ms:
        m.clear_updaters()
    if ms:
        sc.play(*[FadeOut(m) for m in ms], run_time=rt)
        sc.remove(*ms)


# ── v2 · R5 caixa × caixa (A15): todo texto contra todo texto, folga 10 px (o R5 do kit só conta sobreposição > 2 px) ──────────
import v2kit as _v2k
_r5_kit = _v2k.r5v2


def r5cc(self, onde="anim"):
    n = _r5_kit(self, onde)
    fix = self.fixos()
    tx = []
    for m in self.mobjects:
        if m in fix or getattr(m, "_canto", False):
            continue
        for x in m.get_family():
            if getattr(x, "_txt", None) is None or getattr(x, "_saindo", False) or getattr(x, "_voando", False):
                continue
            if any(y is not x and getattr(y, "_txt", None) is not None and x in y.get_family() for y in m.get_family()):
                continue
            gls = [g for g in x.family_members_with_points() if isinstance(g, VMobject)]
            if not gls or max(g.get_fill_opacity() for g in gls) < 0.3:
                continue
            tx.append((str(x._txt), _v2k._caixa(x), x))
    for i, (ta, a, xa) in enumerate(tx):
        for tb, b, xb in tx[i + 1:]:
            if xa in xb.get_family() or xb in xa.get_family() or _v2k._parente(xa, xb) or _v2k._parente(xb, xa):
                continue
            if getattr(xa, "_pai", None) is not None and getattr(xa, "_pai", None) is getattr(xb, "_pai", None):
                continue
            gx = max(a[0], b[0]) - min(a[2], b[2])
            gy = max(a[1], b[1]) - min(a[3], b[3])
            if gx < 10 and gy < 10 and not (gx < -2 and gy < -2):
                print(f"[R5C] {self._aid} {self.t:7.2f}s {ta[:40]!r} x {tb[:40]!r} folga {max(gx, gy):.0f} px {onde}")
                n += 1
    return n


B39.r5 = r5cc
