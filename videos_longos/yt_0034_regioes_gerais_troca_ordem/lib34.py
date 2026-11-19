"""yt_0034 (copiado do lib32.py do yt_0032) · peças desta unidade sobre o v34.py: fórmula por peças (índices de glifo para o TransformByGlyphMap), glyph map do MF-Tools,
caneta em parte de uma fórmula, mapas de cor em quadradinhos (transformáveis), balança, régua da massa, cartões, chapa de dois metais vetorial,
CTA. Tudo em px de 1080p (PX), como no sb32.html."""
from v34 import *  # noqa: F401,F403
from MF_Tools import TransformByGlyphMap

LIL = "#C9A7FF"
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
    m = TC(" ".join(t for _, t in pecas), x, y, size, al, caneta)      # espaço entre peças: e + M não vira eM
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


def ix(m, *chaves):
    out = []
    for c in chaves:
        out += list(c) if isinstance(c, (list, tuple, range)) else m._ix[c]
    return out


def sel(m, a):
    """chave | range | lista de chaves e/ou índices → lista de índices de glifo."""
    if isinstance(a, str):
        return list(m._ix[a])
    out = []
    for x in a:
        out += [x] if isinstance(x, (int, np.integer)) else list(m._ix[x])
    return out


def gl(m, *chaves):
    return VGroup(*[m[0][i] for i in ix(m, *chaves)])


def gm(sc, A, B, pares, rt=1.2, copia=False, extra=(), nota=""):
    """TransformByGlyphMap (MF-Tools, auto_fade) com mapa explícito: pares = [(chaves|índices em A, chaves|índices em B), …].
    Glifos de A fora do mapa somem; glifos de B fora do mapa nascem (auto_fade). copia=True: A fica (from_copy)."""
    ent = [(sel(A, p[0]), sel(B, p[1])) + tuple(p[2:]) for p in pares]       # p[2] (opcional): kwargs do par, ex. {"path_arc": 1.6}
    B._esc = True
    an = TransformByGlyphMap(A, B, *ent, from_copy=copia, auto_fade=True, run_time=rt)
    GM_LOG.append((sc.lote, sc._aid, round(sc.t, 2), A._tex, B._tex))
    print(f"[gm] {sc.lote} {sc._aid} {sc.t:.2f} pares={len(ent)} {nota} :: {A._tex[:60]!r} → {B._tex[:70]!r}")
    sc.play(an, *extra, run_time=rt)
    if not copia:
        sc.remove(A)
    for m in list(sc.mobjects):            # restos soltos do MF-Tools (glifos da origem)
        if m is not B and m is not A and isinstance(m, VMobject) and getattr(m, "_tex", None) is None and m in A[0].submobjects:
            sc.remove(m)
    sc.add(B)
    return B


def parte(F, idx, nome=""):
    """Grupo de glifos de F para a caneta escrever por partes (F deixa de ser vigiado como um todo; cada parte é)."""
    F._caneta, F._esc = False, True
    g = VGroup(*[F[0][i] for i in idx])
    g._tex = f"{F._tex} [{nome or idx[0]}]"
    g._caneta, g._esc, g._em_caneta, g._txt = True, False, False, None
    g._pai = F                          # yt_0034: quando todas as partes de F estiverem escritas, F volta inteiro à cena (junta)
    if not hasattr(F, "_partes"):
        F._partes, F._feito = [], set()
    F._partes.append(g)
    return g


def junta(sc, *gs):
    """yt_0034: depois de escrever partes (caneta ou voo), se a fórmula-mãe está completa, troca os grupos-parte pela fórmula inteira."""
    for g in gs:
        F = getattr(g, "_pai", None)
        if F is None:
            continue
        F._feito |= {id(x) for x in g.submobjects}
        noscena = {id(x) for p in F._partes if p in sc.mobjects for x in p.submobjects}
        if all(id(x) in F._feito and id(x) in noscena for x in F[0]):
            sc.remove(*F._partes)
            F._esc = True
            sc.add(F)


def poe_parte(sc, F):
    """Põe F na cena com todos os glifos apagados (as partes vão sendo escritas pela caneta)."""
    for x in F[0]:
        x.set_fill(opacity=0).set_stroke(width=0, opacity=0)
    sc.add(F)


# ── mapas de cor em quadradinhos (transformam: espelho, recolor) ───────────────────────────────────────────
def mapa_q(v, fun, n, cor0, cor1, vmax=1.0, disco=False, z=1, gama=1.0):
    """n×n quadradinhos sem contorno (traço da mesma cor, 0,6 px, para não haver fresta) na vista v; fun(X, Y) em [0, vmax]."""
    h = 2 / n
    g = VGroup()
    for i in range(n):
        for j in range(n):
            X, Y = (i + .5) * h, (j + .5) * h
            if disco and (X - 1) ** 2 + (Y - 1) ** 2 > 1:
                continue
            c = mixh(cor0, cor1, (min(1.0, fun(X, Y) / vmax)) ** gama)
            r = Polygon(v.P(i * h, j * h), v.P((i + 1) * h, j * h), v.P((i + 1) * h, (j + 1) * h), v.P(i * h, (j + 1) * h))
            r.set_fill(c, 1).set_stroke(width=0)
            r.scale(1.06)                     # sobrepõe 3 % de cada lado: sem fresta e sem malha visível
            r._ij = (i, j)
            g.add(r)
    return sem_ctn(g).set_z_index(z)


def recolore(g, n, fun, cor0, cor1, vmax=1.0, gama=1.0):
    """Cópia de um mapa_q (n×n) com novas cores e a mesma geometria: alvo de Transform."""
    alvo = g.copy()
    h = 2 / n
    for r in alvo:
        i, j = r._ij
        c = mixh(cor0, cor1, (min(1.0, fun((i + .5) * h, (j + .5) * h) / vmax)) ** gama)
        r.set_fill(c, 1)
    return alvo


def disco_q(v, fun, n, cor0, cor1, vmax=1.0, z=1):
    return mapa_q(v, fun, n, cor0, cor1, vmax, disco=True, z=z)


# ── chapa de dois metais vetorial (arte v1b: metal com degradê e escovado, cordão de solda com escamas) ──────────────────
LEVE_A, LEVE_B = "#2A6C96", "#163B57"          # leve: topo / base do degradê (média ≈ LEVE)
PES_A, PES_B = "#62D6F2", "#2398BD"            # pesado: topo / base (média ≈ PESADO)
PRATA, PRATA_E, PRATA_C = "#C3CADB", "#69728D", "#EEF1F8"     # cordão: corpo, borda, escamas


def curva_g(v, dy=0.0, n=120, a0=0.0, a1=2.0):
    return [v.px(a, float(g_solda(a)) + dy) for a in np.linspace(a0, a1, n + 1)]


def degrade(m, topo, base):
    """Degradê vertical do preenchimento (topo → base), sem brilho: só a cor do metal variando."""
    m.set_fill([base, topo], 1)
    m.set_sheen_direction(UP)
    return m


def escova(v, lado, cor, passo=6, wpx=1.0, z=2, dy=0.0):
    """Textura de metal escovado: riscos horizontais finos só dentro do pedaço (leve: abaixo da solda; pesado: acima)."""
    xs = np.linspace(0, 2, 241)
    gs = g_solda(xs) + dy
    linhas = VGroup()
    h = passo / v.uy
    k = 0
    for b in np.arange(h / 2, 2, h):
        dentro = (b < gs) if lado == "leve" else (b > gs)
        i = 0
        while i < len(xs):
            if dentro[i]:
                j = i
                while j + 1 < len(xs) and dentro[j + 1]:
                    j += 1
                # riscos irregulares: começa e termina com um pequeno recuo pseudoaleatório (determinístico)
                r = ((k * 7919) % 97) / 97
                a, c = xs[i] + 0.02 * r, xs[j] - 0.02 * (1 - r)
                if c - a > 0.03:
                    linhas.add(lin_px([v.px(a, b), v.px(c, b)], cor, wpx, z=z))
                i = j + 1
            else:
                i += 1
        k += 1
    for l in linhas:
        l.cap_style = CapStyleType.BUTT
    return sem_ctn(linhas)


def metais_liso(v, dy_leve=0.0, dy_pes=0.0, z=1, textura=True):
    """Os dois pedaços da chapa: metal em degradê + escovado (Group(leve, pes); .leve/.pes são as formas)."""
    leve = poly_px([v.px(0, 0), v.px(2, 0)] + curva_g(v, dy_leve)[::-1], LEVE, z=z)
    pes = poly_px([v.px(0, 2), v.px(2, 2)] + curva_g(v, dy_pes)[::-1], PESADO, z=z)
    degrade(leve, LEVE_A, LEVE_B)
    degrade(pes, PES_A, PES_B)
    if textura and v.u >= 90:
        el = escova(v, "leve", mixh(LEVE, "#FFFFFF", .10), max(4, v.u / 40), 1.0, z=z, dy=dy_leve)
        ep = escova(v, "pes", mixh(PESADO, "#FFFFFF", .16), max(4, v.u / 40), 1.0, z=z, dy=dy_pes)
        leve = VGroup(leve, el)
        pes = VGroup(pes, ep)
    return leve, pes


class Cordao(VGroup):
    """Cordão de solda sobre a curva (px): corpo prata, bordas escuras finas e N escamas em V (a marca do cordão real).
    Sempre N escamas, para que dois cordões de tamanhos diferentes se transformem um no outro."""
    N = 26

    def __init__(self, pts, wpx=9.0, z=7, corpo=PRATA, borda=PRATA_E, escama=PRATA_C, N=None):
        super().__init__()
        N = N or self.N
        P = np.array(pts, float)
        d = np.diff(P, axis=0)
        s = np.concatenate([[0], np.cumsum(np.hypot(d[:, 0], d[:, 1]))])
        tang = np.gradient(P, axis=0)
        tang /= np.linalg.norm(tang, axis=1)[:, None]
        nor = np.stack([-tang[:, 1], tang[:, 0]], 1)
        self.corpo = lin_px(P.tolist(), corpo, wpx, z=z)
        self.b1 = lin_px((P + nor * wpx / 2).tolist(), borda, max(1.0, wpx / 7), z=z + 1)
        self.b2 = lin_px((P - nor * wpx / 2).tolist(), borda, max(1.0, wpx / 7), z=z + 1)
        esc = VGroup()
        for k in range(N):
            sk = s[-1] * (k + .5) / N
            i = int(np.searchsorted(s, sk).clip(1, len(s) - 1))
            p, t, n = P[i], tang[i], nor[i]
            a, c = wpx * 0.40, wpx * 0.42
            v = [p + n * a - t * c, p + t * c * 0.15, p - n * a - t * c]
            m = VMobject().set_points_smoothly([PX(*q) for q in v]).set_stroke(escama, W(max(1.0, wpx / 8)), 1).set_fill(opacity=0)
            esc.add(sem_ctn(m).set_z_index(z + 2))
        self.esc = esc
        self.add(self.corpo, self.b1, self.b2, self.esc)
        self._cores = (corpo, borda, escama)
        self._pts, self._w = P, wpx
        sem_ctn(self)

    def cor(self, corpo=None, escama=None):
        """Cópia com outra cor (alvo de Transform: a solda 'acende' sem pulso)."""
        c = self.copy()
        if corpo:
            c.corpo.set_stroke(corpo)
        if escama:
            c.esc.set_stroke(escama)
        return c


def deposita(cord, rt=1.6, quente=POS):
    """A solda sendo depositada: o cordão cresce ao longo da curva atrás de uma ponta quente (laranja); cada escama nasce laranja e
    esfria até a prata em ~0,35 do tempo. Sem brilho: só cor."""
    alvo = cord.copy()
    corpo0, esc0 = cord._cores[0], cord._cores[2]
    N = len(cord.esc)

    def upd(m, a):
        for parte, ref in ((m.corpo, alvo.corpo), (m.b1, alvo.b1), (m.b2, alvo.b2)):
            parte.pointwise_become_partial(ref, 0, max(1e-3, a))
        for k, (e, er) in enumerate(zip(m.esc, alvo.esc)):
            u = a * 1.0 - (k + 1) / N
            if u < 0:
                e.set_stroke(opacity=0)
            else:
                e.set_stroke(interpolate_color(ManimColor(quente), ManimColor(esc0), min(1.0, u / 0.35)), opacity=1)
        # trecho recém-depositado ainda quente: a cor do corpo vai do laranja à prata
        m.corpo.set_stroke(interpolate_color(ManimColor(quente), ManimColor(corpo0), min(1.0, max(0.0, (a - 0.0) / 1.0) ** 0.5 if a < 1 else 1.0)))
    return UpdateFromAlphaFunc(cord, upd, run_time=rt, rate_func=linear)


def cordao_ch(v, wpx=None, dy=0.0, z=7, a0=0.0, a1=2.0):
    return Cordao(curva_g(v, dy, 160, a0, a1), wpx or max(4.0, v.u / 26), z=z)


# ── balança (sb32: balanca(cx, Yp, u)) · arte v1b: trave com pivô e fiel, coluna com base, pratos em cuba, inclinação ────────
def balanca(cx, Yp, u, ang=0.0, wcord=None):
    """Dois pratos com os pedaços da chapa (leve à esquerda, pesado à direita). ang (graus, + = lado direito desce): a trave gira no pivô
    e os pratos pendurados descem/sobem na vertical. Devolve dict de partes (mesmos nomes e estrutura em qualquer escala e ângulo)."""
    Lp, gap = 2 * u, 60
    D = gap / 2 + Lp / 2
    Yb = Yp - 1.6 * u - 40
    th = math.radians(ang)
    El = (cx - D * math.cos(th), Yb - D * math.sin(th))
    Er = (cx + D * math.cos(th), Yb + D * math.sin(th))
    k = u / 110
    P = {}
    P["trave"] = lin_px([El, Er], GEO, max(3, 6 * k), z=6)
    nx, ny = math.sin(th), -math.cos(th)                       # fiel: perpendicular à trave, para cima
    tx, ty = math.cos(th), math.sin(th)
    P["fiel"] = sem_ctn(Polygon(PX(cx + nx * 34 * k, Yb + ny * 34 * k), PX(cx + tx * 5 * k, Yb + ty * 5 * k), PX(cx - tx * 5 * k, Yb - ty * 5 * k))
                        .set_fill(GEO, 1).set_stroke(width=0)).set_z_index(6)
    P["pivo"] = circ_px(cx, Yb, max(4, 9 * k), GEO, max(2, 3 * k), fill=BG_, fop=1, z=7)
    P["poste"] = lin_px([(cx, Yb + 9 * k), (cx, Yp + 92)], GEO, max(3, 4 * k), z=3)
    P["pe"] = sem_ctn(Polygon(PX(cx - 70 * k - 10, Yp + 112), PX(cx + 70 * k + 10, Yp + 112), PX(cx + 26 * k, Yp + 92), PX(cx - 26 * k, Yp + 92))
                      .set_fill(mixh(BG_, GEO, .20), 1).set_stroke(GEO, W(2), 1)).set_z_index(3)
    for lado, E in (("l", El), ("r", Er)):
        x0 = E[0]
        yp = E[1] + (Yp + 6 - Yb)
        P["corda" + lado] = lin_px([(x0 - Lp / 2 - 6, yp - 2), E, (x0 + Lp / 2 + 6, yp - 2)], GEO, max(1.5, 2 * k), z=3)
        P["anel" + lado] = circ_px(*E, max(3, 5 * k), GEO, max(1.5, 2 * k), fill=BG_, fop=1, z=7)
        cuba = ArcBetweenPoints(PX(x0 - Lp / 2 - 14, yp), PX(x0 + Lp / 2 + 14, yp), angle=0.35)
        P["prato" + lado] = sem_ctn(cuba.set_stroke(GEO, W(max(3, 5 * k))).set_fill(opacity=0)).set_z_index(5)
        if lado == "l":
            vl = Vw(x0 - Lp / 2, yp - 6, u)
        else:
            vr = Vw(x0 - Lp / 2, yp - 6 + 0.836 * u, u)
    P["leve"], _ = metais_liso(vl, z=4, textura=False)
    _, P["pes"] = metais_liso(vr, z=4, textura=False)
    w = wcord or max(3.0, 6 * k)
    P["sl"] = cordao_ch(vl, w, z=8)
    P["sp"] = cordao_ch(vr, w, z=8)
    P["_xl"], P["_xr"], P["_L"], P["_vl"], P["_vr"] = vl.cx, vr.cx, Lp, vl, vr
    return P


def balanca_inclina(sc, P, cx, Yp, u, a0, a1, rt=1.6, extra_l=(), extra_r=()):
    """A trave vai de a0 a a1 graus com um balanço amortecido (o lado pesado desce). extra_l/extra_r: rótulos que acompanham cada prato."""
    nomes = [k for k in P if not k.startswith("_")]
    grupo = VGroup(*[P[k] for k in nomes])
    base_l = {id(m): m.get_center().copy() for m in extra_l}
    base_r = {id(m): m.get_center().copy() for m in extra_r}
    Y0 = {s: balanca(cx, Yp, u, a0)["_v" + s].cy for s in ("l", "r")}

    def upd(g, a):
        ang = a1 + (a0 - a1) * math.exp(-4.2 * a) * math.cos(2.6 * PI * a) if a < 1 else a1
        N = balanca(cx, Yp, u, ang)
        for k in nomes:
            P[k].become(N[k])
        for ms, s in ((extra_l, "l"), (extra_r, "r")):
            dy = (N["_v" + s].cy - Y0[s]) / 120
            for m in ms:
                m.move_to((base_l if s == "l" else base_r)[id(m)] + DOWN * dy)
    return UpdateFromAlphaFunc(grupo, upd, run_time=rt, rate_func=linear)


ANG_BAL = 5.0          # inclinação de repouso da balança (pesado 4,584 kg à direita × leve 2,472 kg)


# ── régua da massa (sb32: regua(Y, …)) ──────────────────────────────────────────────────────────────────────
def regua(Y, X0=1120, k=52, ticks=(0, 2, 4, 6, 8, 10, 12)):
    g = VGroup()
    g.add(lin_px([(X0, Y), (X0 + 12 * k + 24, Y)], GEO, 3, z=3))
    g.add(sem_ctn(Polygon(PX(X0 + 12 * k + 34, Y), PX(X0 + 12 * k + 18, Y - 8), PX(X0 + 12 * k + 18, Y + 8)).set_fill(GEO, 1).set_stroke(width=0)).set_z_index(3))
    for t in ticks:
        g.add(lin_px([(X0 + t * k, Y - 7), (X0 + t * k, Y + 7)], GEO, 3, z=3))
    labs = VGroup(*[leg(str(t), X0 + t * k, Y + 38, GEO, "center", 26) for t in ticks], leg("kg", X0 + 12 * k + 40, Y + 36, GEO, "left", 26))
    return g, labs


def regua_faixa(Y, a, b, X0=1120, k=52):
    band = ret_px(X0 + a * k, Y - 13, X0 + b * k, Y + 13, fill=mixh(BG_, GEO, .22), z=2)
    m1 = ret_px(X0 + a * k - 3, Y - 18, X0 + a * k + 3, Y + 18, fill=AZC, z=4)
    m2 = ret_px(X0 + b * k - 3, Y - 18, X0 + b * k + 3, Y + 18, fill=CORAL, z=4)
    return band, m1, m2


# ── cartões ─────────────────────────────────────────────────────────────────────────────────────────────
def cartao(X0, Y0, w, h, t, sub=None, cor=BR):
    p = painel(X0, Y0, w, h)
    tt = T(t, X0 + w / 2, Y0 + h - 58, 28, "center", cor)
    ss = leg(sub, X0 + w / 2, Y0 + h - 22, GEO, "center", 26) if sub else None
    return p, tt, ss


def moldura(X0, Y0, w, h, cor=GEO, alpha=0.5, wpx=2, raio=10):
    r = RoundedRectangle(width=w / 120, height=h / 120, corner_radius=raio / 120).move_to(PX(X0 + w / 2, Y0 + h / 2))
    r.set_fill(opacity=0).set_stroke(cor, W(wpx), alpha)
    return sem_ctn(r).set_z_index(2)


def carimbo(s, X, Y, cor=AL, w=300, h=64, rot=-0.06, size=32):
    car = VGroup(RoundedRectangle(width=w / 120, height=h / 120, corner_radius=8 / 120).set_stroke(cor, W(3)).set_fill(opacity=0),
                 txt(s, ts(size), color=cor, bold=True, up=False))
    car[1].move_to(car[0])
    sem_ctn(car)
    car.move_to(PX(X, Y - 6)).rotate(-rot).set_z_index(26)
    car._txt = s
    return car


def logo_cta(cena, rt_fim=3.0):
    """CTA padrão do canal (copiado do v28.py do yt_0028): tudo sai; logo com os dois anéis; INSCREVA-SE até o fim da fala + 3 s."""
    CL = P3(0, 0.9)
    logo = cena.logo(5.6).move_to(CL)
    aneis = VGroup(*[DashedVMobject(Circle(radius=r).move_to(CL), num_dashes=48).set_stroke(GEO, 2.6, opacity=o) for r, o in ((2.1, 0.85), (2.45, 0.6))])
    for m_ in aneis.get_family():
        m_._sem_contorno = True
    ins = VGroup(T("INSCREVA-SE PARA ACOMPANHAR", 960, 0, 66, "center", caneta=False), T("OS PRÓXIMOS VÍDEOS", 960, 0, 66, "center", caneta=False)
                 ).arrange(DOWN, buff=0.12).move_to(P3(0, -2.6))
    s4 = cena.snap()
    sai_c = [m_ for m_ in (cena.h2, cena.h1) if m_ is not None and m_ in cena.mobjects]
    cena.play(*[FadeOut(m_) for m_ in s4 + sai_c], run_time=0.3)
    cena.remove(*s4, *sai_c)
    cena.play(FadeIn(logo, scale=0.96), FadeIn(aneis), FadeIn(ins, shift=0.1 * UP), run_time=0.4)
    cena.remove(*s4, *sai_c)
    cena.h2 = None
    rt = cena.resta() + rt_fim
    cena.play(Rotate(aneis[0], 0.3 * rt, rate_func=linear), Rotate(aneis[1], -0.24 * rt, rate_func=linear), run_time=rt)


def tira_canto(sc, rt=0.4):
    """Tira as duas linhas do canto (H2, A1, S2 não têm canto)."""
    ms = [m for m in (sc.h1, sc.h2) if m is not None and m in sc.mobjects]
    if ms:
        sc.play(*[FadeOut(m) for m in ms], run_time=rt)
        sc.remove(*ms)
    sc.h2 = None


def poe_canto(sc, titulo):
    """Linha 1 + linha 2 do canto entrando juntas (lote que começa sem canto)."""
    if sc.h1 not in sc.mobjects:
        sc._pend.append(FadeIn(sc.h1))
    sc.secao(titulo)


# ── ajustes da base nesta unidade ─────────────────────────────────────────────────────────────────────────
def _secao32(self, s):
    """Linha 2 do canto sem caixa alta automática (o título do alvo já vem em maiúsculas e mantém o 'f' de 'MUDAR f')."""
    if self.h2 is not None:
        self.play(FadeOut(self.h2), run_time=0.25)
        self.h2 = None
    if s:
        self.h2 = self._canto(txt(s, 21.6, color="#F5F7FF", bold=True, up=False), CANTO_Y2, topo_min=self._y1_fim_px() + 10)
        self._pend.append(FadeIn(self.h2))


def _marca32(self, alvo, agora=False):
    """Instante do estado final do alvo: o fim da âncora (0,6 s antes), mas nunca antes do que já foi escrito (agora + 0,2 s)."""
    t = max(self.nq / FPS + 0.2, self.alvo / FPS - 0.6) if not agora else self.nq / FPS + 0.07
    print(f"[marca] {alvo} {t:.3f}")


B34.secao = _secao32
B34.marca = _marca32


# ── mapas pela geometria da função (sem serrilhado) ──────────────────────────────────────────────────────
def faixas(v, fun, n, cor0, cor1, vmax=1.0, eixo="x", z=1):
    """Mapa de uma função de uma variável só: n faixas finas (verticais se depende de x, horizontais se de y), sem contorno.
    A faixa k fica em [2k/n, 2(k+1)/n]; o espelho na diagonal leva a faixa vertical k na horizontal k (mesma ordem)."""
    g = VGroup()
    h = 2 / n
    for k in range(n):
        c = mixh(cor0, cor1, min(1.0, fun((k + .5) * h) / vmax))
        a, b = k * h, min(2.0, (k + 1) * h + h * 0.35)
        pts = [v.px(a, 0), v.px(b, 0), v.px(b, 2), v.px(a, 2)] if eixo == "x" else [v.px(0, a), v.px(0, b), v.px(2, b), v.px(2, a)]
        r = Polygon(*[PX(*p) for p in pts]).set_fill(c, 1).set_stroke(width=0)
        g.add(r)
    return sem_ctn(g).set_z_index(z)


def disco_setores(cx, cy, R, fun, cor0, cor1, N=240, z=1):
    """Disco de raio R px em (cx, cy) cuja cor depende só do ângulo θ (fun(θ) em [0, 1]): N setores finos, sem contorno.
    O setor k cobre θ ∈ [2πk/N, 2π(k+1)/N]."""
    g = VGroup()
    da = TAU / N
    for k in range(N):
        th = (k + .5) * da
        c = mixh(cor0, cor1, min(1.0, max(0.0, fun(th))))
        s = Sector(radius=R / 120, angle=da * 1.25, start_angle=k * da - da * 0.12, arc_center=PX(cx, cy))
        s.set_fill(c, 1).set_stroke(width=0)
        g.add(s)
    return sem_ctn(g).set_z_index(z)


# ── ritmo: plano de duas passadas para não haver tela parada > 3 s (handoff §3.2) ───────────────────────────
# Passada 1 (PLANO=grava, --dry_run): cada espera >= 3 s depois de um play é anotada como sobra desse play (sobra = espera − 2 s).
# Passadas seguintes: o play anotado dura mais (a caneta escreve mais devagar, o glyph map anda mais devagar), até 3× e no máximo +6 s;
# os gatilhos da fala não mudam (o gat seguinte só espera menos). Sem pulso, sem movimento extra.
PLANO = os.environ.get("PLANO", "usa")
_DIRP = AQUI / "renders" / "plano"
_play0, _wait0 = B34.play, B34.wait


def _plano(self):
    if not hasattr(self, "_pl"):
        self._ip, self._ip_ult = 0, None
        arq = _DIRP / f"{self.lote}.json"
        self._pl = {} if PLANO == "grava" or not arq.exists() else {int(k): v for k, v in json.loads(arq.read_text(encoding="utf-8")).items()}
    return self._pl


def _play_r(self, *anims, run_time=None, **kw):
    pl = _plano(self)
    self._ip += 1
    self._ip_ult = self._ip
    if PLANO != "grava" and self._ip in pl and not getattr(self, "_fixo_rt", False):
        rt = run_time if run_time is not None else max([getattr(a, "run_time", 1.0) for a in anims] or [1.0])
        run_time = min(rt * 5.0, rt + pl[self._ip], rt + 8.0)
    return _play0(self, *anims, run_time=run_time, **kw)


def _wait_r(self, duration=1.0, *a, **k):
    pl = _plano(self)
    if PLANO == "grava" and duration >= 3.0 and self._ip_ult is not None:
        pl[self._ip_ult] = round(pl.get(self._ip_ult, 0.0) + duration - 2.0, 3)
    return _wait0(self, duration, *a, **k)


def _fim_r(self):
    _plano(self)
    if PLANO == "grava":
        _DIRP.mkdir(parents=True, exist_ok=True)
        (_DIRP / f"{self.lote}.json").write_text(json.dumps(self._pl), encoding="utf-8")
        print(f"[plano] {self.lote}: {len(self._pl)} plays alongados, sobra total {sum(self._pl.values()):.1f} s")
    return _fim0(self)


_fim0 = B34.fim
B34.play, B34.wait, B34.fim = _play_r, _wait_r, _fim_r


def disco_img(cx, cy, R, fun, cor0, cor1, z=1, sup=2.0):
    """Disco de raio R px em (cx, cy) com cor fun(θ) ∈ [0, 1] (θ medido do eixo x, anti-horário), como imagem analítica em
    resolução 'sup' × a de 1080p: sem serrilhado e sem moiré; a borda tem 1 px de transição (alfa)."""
    n = int(2 * R * sup)
    u = (np.arange(n) + .5) / n * 2 - 1
    X, Y = np.meshgrid(u, -u)
    th = np.arctan2(Y, X)
    t = np.clip(fun(th), 0, 1)[..., None]
    rgb = hx(cor0) * (1 - t) + hx(cor1) * t
    a = np.clip((1 - np.hypot(X, Y)) * R * sup, 0, 1)[..., None] * 255
    im = img_px(np.concatenate([rgb, a], 2), cx - R, cy - R, 2 * R, 2 * R, z=z)
    im._fun, im._cores = fun, (cor0, cor1)
    return im


def recolore_img(im, cor0, cor1):
    """Mesma imagem (mesma geometria e mesmo desenho do pixel) com outro par de cores: alvo de Transform que só troca a cor."""
    c = im.copy()
    a = c.pixel_array.astype(float)
    c0, c1 = hx(im._cores[0]), hx(im._cores[1])
    t = np.clip(((a[..., :3] - c0) @ (c1 - c0)) / max(1e-9, (c1 - c0) @ (c1 - c0)), 0, 1)[..., None]
    a[..., :3] = hx(cor0) * (1 - t) + hx(cor1) * t
    c.pixel_array = a.astype(np.uint8)
    return c


# ── v2 (handoff v2): linha mista, régua até 14, câmera do b14k ────────────────────────────────────────────
def mista(partes, X, Y, size=34, al="l"):
    """Linha mista do sb32 v2: palavras em Space Grotesk (caixa alta) e matemática em MathTex lado a lado, centro vertical em Y.
    partes = [('t', texto[, cor]) | ('m', tex) | ('L', pecas)]; a matemática usa 1,18 × size (como o KaTeX do alvo).
    Devolve VGroup; .p = lista das partes (T, TC ou L, na ordem)."""
    g, cx, ps = VGroup(), X, []
    for p in partes:
        k = p[0]
        if k == "t":
            m = T(p[1], cx, Y + size * 0.36, size, "left", p[2] if len(p) > 2 else BR)
            cx = pxof(m.get_right())[0] + size * 0.32
        else:
            m = TC(p[1], cx, Y, size * 1.18, "l") if k == "m" else L(p[1], cx, Y, size * 1.18, "l")
            cx = pxof(m.get_right())[0] + size * 0.55
        g.add(m)
        ps.append(m)
    if al == "c":
        g.shift(RIGHT * ((X - (pxof(g.get_left())[0] + pxof(g.get_right())[0]) / 2) / 120))
    g.p = ps
    g._tex = "mista: " + " | ".join(str(p[1])[:30] for p in partes)
    return g


def regua2(Y, X0=1120, k=46, mx=14, ticks=(0, 2, 4, 6, 8, 10, 12, 14)):
    g = VGroup()
    g.add(lin_px([(X0, Y), (X0 + mx * k + 24, Y)], GEO, 3, z=3))
    g.add(sem_ctn(Polygon(PX(X0 + mx * k + 34, Y), PX(X0 + mx * k + 18, Y - 8), PX(X0 + mx * k + 18, Y + 8)).set_fill(GEO, 1).set_stroke(width=0)).set_z_index(3))
    for t in ticks:
        g.add(lin_px([(X0 + t * k, Y - 7), (X0 + t * k, Y + 7)], GEO, 3, z=3))
    labs = VGroup(*[leg(str(t), X0 + t * k, Y + 38, GEO, "center", 26) for t in ticks], leg("kg", X0 + mx * k + 42, Y + 38, GEO, "left", 26))
    return g, labs




# ── QA v2: frações (altura do numerador) e rótulo órfão ──────────────────────────────────────────────────
import v34 as _v32
_TC0 = _v32.TC


def _TC_qa(s, x=960, y=540, size=48, al="l", caneta=True):
    m = _TC0(s, x, y, size, al, caneta)
    if "frac" in s:
        gs = [g for g in m[0]]
        cy = m.get_center()[1]
        num = [g for g in gs if g.get_center()[1] > cy + 0.02]
        alt = (max(g.get_top()[1] for g in num) - min(g.get_bottom()[1] for g in num)) * 120 if num else 0.0
        dig = [g.height * 120 for g in num]
        print(f"[frac] size={size:.1f}px numerador={alt:.1f}px maior_glifo={max(dig) if dig else 0:.1f}px :: {s[:90]}")
    return m


_v32.TC = _TC_qa
TC = _TC_qa
_an0 = B34.an


def _an_qa(self, aid):
    """Rótulo órfão: na fronteira de cada âncora, nenhum rótulo preso a uma cena 3D que já saiu (ou está apagada)."""
    vivos = {m.cena for m in self.mobjects if isinstance(m, Fundo3D) and m.op.get_value() > 0.05}
    for m in self.mobjects:
        for x in m.get_family():
            p3 = getattr(x, "_p3d", None)
            if p3 and p3[0] not in vivos:
                print(f"[orfao] {self.lote} antes de {aid}: rótulo {getattr(x, '_txt', '?')!r} preso a {p3[0]}.{p3[1]} sem a cena 3D")
    return _an0(self, aid)


B34.an = _an_qa


# ── final: linhas novas de uma grade que refina (nascem no lugar; as velhas ficam) e rótulo misto com placa ──────────────
def linhas_novas(v, n, cor, wpx=1, z=3):
    """Só as linhas da grade n×n que não existem na grade n/2 (múltiplos ímpares de 2/n): verticais de baixo para cima, horizontais da
    esquerda para a direita, para o Create nascer no lugar (C1, C17)."""
    g = VGroup()
    for k in range(1, n, 2):
        a = 2 * k / n
        g.add(lin_px([v.px(a, 0), v.px(a, 2)], cor, wpx, z=z))
        g.add(lin_px([v.px(0, a), v.px(2, a)], cor, wpx, z=z))
    return g


def TPm(partes, size=26):
    """Rótulo misto (Space Grotesk + MathTex) com placa mínima, para prender ao 3D. .f = a linha mista (com .p)."""
    m = mista(partes, 0, 0, size)
    g = VGroup(placa_min(m, 8, 4), m)
    g.f = m
    g._txt = m._tex
    return g


# ── final (handoff final §6): PRESSA, duas passadas para a cena seguir a voz real ───────────────────────────────────────────────
# Passada 1 (PRESSA=grava, --dry_run): cada trecho entre dois gatilhos (gat, an, fim) anota o tempo de animação dele e o atraso com que chegou ao
# gatilho do fim. Fator do trecho = (tempo − atraso que o próprio trecho criou − 0,1 s) ÷ tempo, com piso 0,5 (caneta no máximo 2× mais rápida).
# Passadas seguintes (PRESSA=usa, o padrão): os plays e as esperas do trecho andam com esse fator. A voz nunca muda; só a construção encurta.
PRESSA = os.environ.get("PRESSA", "usa")
_DIRPR = AQUI / "renders" / "pressa"
_play_pr0, _wait_pr0, _gat_pr0, _an_pr0, _fim_pr0 = B34.play, B34.wait, B34.gat, B34.an, B34.fim


def _pr(self):
    if not hasattr(self, "_prs"):
        self._prs, self._seg, self._em_gat = {}, 0, False
        arq = _DIRPR / f"{self.lote}.json"
        self._fat = {} if PRESSA != "usa" or not arq.exists() else {int(k): v for k, v in json.loads(arq.read_text(encoding="utf-8"))["fator"].items()}
    return self._prs


def _play_pr(self, *anims, run_time=None, **kw):
    from manim.animation.animation import prepare_animation
    S = _pr(self)
    anims = [prepare_animation(a) for a in anims]
    rt = run_time if run_time is not None else max([a.run_time for a in anims] or [1.0])
    f = self._fat.get(self._seg, 1.0)
    if f < 0.999:
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
        if duration < 1 / FPS:
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
        alvo = self._q0 + max(0.0, ANC[self._aid]["t"][k] - LEAD) * FPS
        _fecha_seg(self, (self.nq - alvo) / FPS, f"{self._aid}: {frase}")
    self._em_gat = True
    try:
        return _gat_pr0(self, frase)
    finally:
        self._em_gat = False


def _an_pr(self, aid):
    _pr(self)
    if self._off is not None:
        _fecha_seg(self, (self.nq - (round(ANC[aid]["ini"] * FPS) - self._off)) / FPS, f"início de {aid}")
    self._em_gat = True
    try:
        return _an_pr0(self, aid)
    finally:
        self._em_gat = False


def _fim_pr(self):
    S = _pr(self)
    _fecha_seg(self, (self.nq - self.alvo) / FPS, "fim do lote")
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
        (_DIRPR / f"{self.lote}.json").write_text(json.dumps({"fator": fat, "trechos": S}, ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"[pressa] {self.lote}: {len(fat)} trechos encurtados; menor fator {min(fat.values()) if fat else 1:.2f}")
    return _fim_pr0(self)


B34.play, B34.wait, B34.gat, B34.an, B34.fim = _play_pr, _wait_pr, _gat_pr, _an_pr, _fim_pr
