"""yt_0036 · peças desta unidade sobre o pecas36.py (kit copiado do yt_0034): câmeras e pontos das cenas 3D do c35.js (porte do c3d35.html),
pouso lateral, selo do passo sob o canto, PAUSE E TENTE, DICA, cartão dos 4 passos, ícones da escada, perspectiva cavaleira 2D.
Tudo em px de 1080p (PX), como no referencia/sb35.html."""
from pecas36 import *  # noqa: F401,F403
from pecas36 import _TC_qa  # noqa: F401
from kit import _Caneta  # noqa: F401
import v36 as _v

TEX31.add_to_preamble(r"\definecolor{ng}{HTML}{9C8CFF}\def\Ng#1{\textcolor{ng}{#1}}\def\arcsen{\operatorname{arcsen}}")
NEG, GRAVE = "#9C8CFF", "#4A4570"
FUNDO_Q = "#1C1846"
PASSOS = ["DESENHAR A REGIÃO", "ESCOLHER A FATIA", "LIMITES PELA RETA", "CALCULAR E CONFERIR"]
TITULO_CANTO = "CÁLCULO III · MUDANÇA DE VARIÁVEIS"

# ── câmeras (c3d35.html: ver(pos, alvo, cx, cy), up = +z, fov 22°; deslocamentos dos alvos no setViewOffset/escala, handoff §2.2) ──────
VC = tuple(v * 1.6 for v in (6.2, -6.9, 4.4))
TCK = (.3, .1, -.05)
FOV90 = 2 * math.degrees(math.atan(math.tan(math.radians(11)) / 0.9))      # PNG a 90 % (alvos 02 e 29): mesma câmera, fov maior
CAM_T33 = cam_dict((11.5, 6.2, 8.4), (1.25, .2, .55), (0, 0, 1), 550, 600)     # alvo 15: dx = −150
CAM_K71 = cam_dict(VC, TCK, (0, 0, 1), 0.9 * 600 + 60, 0.9 * 560 + 70, FOV90)  # alvos 02 e 29: 90 % e (60, 70)
CAM_K72 = cam_dict(VC, TCK, (0, 0, 1), 420, 560)                                # alvos 30 e 32: dx = −180


def sq1(v):
    return math.sqrt(max(0.0, 1 - v * v))


def pontos35(cena, e):
    """Os mesmos pontos nomeados do c35.js (mundo), para o estado e."""
    P = {}
    if cena == "p1":
        Z = lambda X, Y: .13 * (X - 3 * Y * Y)
        P.update({"ex": (2.62, 0, 0), "ey": (0, 2.62, 0), "ez": (0, 0, .62), "c02": (0, 2, Z(0, 2)), "c21": (2, 1, Z(2, 1)), "chao": (2, 2, 0),
                  "meio": (1, 1.5, Z(1, 1.5))})
    elif cena == "s5":
        h = lambda X: .8 * math.exp(X * X)
        P.update({"ex": (2.72, 0, 0), "ey": (0, 2.57, 0), "ez": (0, 0, 2.72), "entD": (.8, .8, 0), "saiD": (2, .8, 0), "tetoD": (1.5, .8, h(.75) + .14),
                  "facaD": (.8, .8, h(.4) + .16), "y1": (0, .8, 0), "entP": (1.2, 0, 0), "saiP": (1.2, 1.2, 0), "altP": (1.2, 1.25, h(.6) / 2),
                  "baseP": (1.2, .6, 0), "facaP": (1.2, 1.2, h(.6) + .16), "x1": (1.2, 0, 0)})
    elif cena == "g6":
        P.update({"ex": (2.62, 0, 0), "ey": (0, 2.62, 0), "ez": (0, 0, 2.02), "pico": (.54, .04, 1.6), "vale": (.04, .54, -1.6), "diag": (1.5, 1.5, 0),
                  "y0": (1.2, 0, 0), "fat": (1.2, .6, 0)})
    elif cena == "cena1":
        x0 = .4
        A, B, Cz = e.get("ea", 1.0), e.get("eb", 1.0), e.get("ec", 1.0)
        Q = lambda v: (v[0] * A, v[1] * B, v[2] * Cz)
        P.update({"ex": (2.9 * A + .12, 0, 0), "ey": (0, 2.45 * B + .12, 0), "ez": (0, 0, 2.35 * Cz + .12), "fatia": Q((2 * x0, .36, .4)),
                  "faca": (2 * x0 * A, (2 * (1 - x0) + .1) * B, .12), "cat1": Q((2 * x0, 1 - x0, 0)), "cat2": Q((2 * x0, 0, 1 - x0)), "x1": Q((2 * x0, 0, 0)),
                  "topo": Q((0, 0, 2)), "f0": Q((2 * x0, 0, 0)), "f1": Q((2 * x0, 2 * (1 - x0), 0)), "f2": Q((2 * x0, 0, 2 * (1 - x0))),
                  "pa": Q((2, 0, 0)), "pb": Q((0, 2, 0)), "pc": Q((0, 0, 2))})
    else:
        SC, x0 = 1.6, .5
        a = sq1(x0)
        cx_, cy_ = e.get("colx", .35), e.get("coly", -.45)
        P.update({"coltopo": (SC * cx_, SC * cy_, SC * sq1(cx_)), "colmeio": (SC * cx_, SC * cy_, 0), "peca": (0, .2 * SC, SC),
                  "cilA": (SC * math.cos(-.6), SC * math.sin(-.6), SC * 1.45), "cilB": (SC * math.cos(.35), -SC * 1.45, SC * math.sin(.35)),
                  "chao": (0, 0, -SC * 1.02), "fatia": (SC * x0, 0, 0), "lado1": (SC * x0, 0, -SC * a), "lado2": (SC * x0, SC * a, 0),
                  "faca": (SC * x0, SC * a, SC * a + .12), "disco": (SC * x0, 0, 0), "quina": (SC * x0, SC * a, SC * a), "raio": (SC * x0, SC * a * .5, 0),
                  "esf": (0, -SC, SC * .4)})
    return P


_v.pontos3d = pontos35


def pouso(sc, pal, tgt1, d1, k1, cx1, cy1, rt=2.5, extra_s=()):
    """Pouso lateral (yt_0034): câmera até a vista frontal ao plano da fatia (perspectiva → dolly-zoom), e um quadro na ortográfica."""
    pal.pousa(tgt1, d1, k1, cx1, cy1)
    sc.play(pal.tr["s"].animate(run_time=rt, rate_func=linear).set_value(1.0), *extra_s, run_time=rt)
    sc.wait(1 / FPS)
    print(f"[pouso] {sc.lote} {sc._aid} quadro {sc.nq - 1} cena {pal.cena}")


def troca_para_2d(sc, pal, entram):
    """No mesmo quadro: o PNG 3D sai e o painel 2D entra por cima (sem animação)."""
    pal.fundo.clear_updaters()
    sc.remove(pal.fundo, *pal.tr.values())
    for m in entram:
        for x in m.get_family():
            if getattr(x, "_caneta", False):
                x._esc = True
    sc.add(*entram)


# ── cena-base do vídeo: selo do passo sob o canto (handoff §3.2) ────────────────────────────────────────────────────────────
class B36(B34):
    def setup_base(self):
        super().setup_base()
        self.sp = None

    def fixos(self):
        f = super().fixos()
        if getattr(self, "sp", None) is not None:
            f = set(f) | {self.sp}
        return f

    def selo_passo(self, n, rt=0.35):
        """Selo de uma linha logo abaixo da linha 2 do canto (x = 36 px, base 165 px, 26 px, GEO, número em âmbar). n = None: some."""
        velho = self.sp
        novo = None
        if n:
            a = T("PASSO", 36, 165, 26, "left", GEO, bold=False, caneta=False)
            b = T(str(n), pxof(a.get_right())[0] + 8, 165, 26, "left", E1, caneta=False)
            c = T("· " + PASSOS[n - 1], pxof(b.get_right())[0] + 8, 165, 26, "left", GEO, bold=False, caneta=False)
            novo = VGroup(a, b, c).set_z_index(40)
            novo._n = n
            if velho is not None and getattr(velho, "_n", None) == n:
                return
        anims = ([FadeOut(velho)] if velho is not None else []) + ([FadeIn(novo)] if novo is not None else [])
        if anims:
            self.play(*anims, run_time=rt)
        if velho is not None:
            self.remove(velho)
        self.sp = novo


def tick(v, eixo, val, tex, size=28):
    """Marca no eixo (traço GEO de 14 px) + número (MathTex). Fração no eixo x desce mais (não encosta no traço)."""
    if eixo == "x":
        q = v.px(val, 0)
        tr = lin_px([(q[0], q[1] - 7), (q[0], q[1] + 7)], GEO, 2, z=6)
        lb = TC(tex, q[0], q[1] + (48 if "frac" in tex else 30), size, "c")
    else:
        q = v.px(0, val)
        tr = lin_px([(q[0] - 7, q[1]), (q[0] + 7, q[1])], GEO, 2, z=6)
        lb = TC(tex, q[0] - 16, q[1], size, "r")
    return tr, lb


def _limpa_tudo(self, rt=0.4, keep=()):
    """Tudo (fora o canto e o selo do passo) sai, inclusive a grade do palco."""
    sai = [m for m in self.snap() if m not in keep] + ([self.grade] if self.grade is not None else [])
    if sai:
        self.play(*[FadeOut(m) for m in sai], run_time=rt)
    for m in sai:
        m.clear_updaters()
    self.remove(*sai)
    self.grade = None
    for m in [m for m in self.mobjects if isinstance(m, ValueTracker) and m is not self.clk]:
        self.remove(m)


B36.limpa_tudo = _limpa_tudo


# ── selos, PAUSE E TENTE, DICA, cartão dos 4 passos ───────────────────────────────────────────────────────────────────────────
def poe_selo(sc, sl, extra=()):
    """selo = (moldura, texto): a moldura nasce e o texto vem pela caneta."""
    sc.pena(sl[1], extra=[Create(sl[0]), *extra])          # final K2: moldura e texto nascem juntos (nunca a moldura sozinha)


def pausa(X, Y):
    return selo("PAUSE E TENTE", X, Y, E1, 26)


def dica(X, Y, w, l1, l2=None):
    """Cartão DICA (moldura GEO, a palavra em menta 26 px, até duas linhas de 30 px; matemática em MathTex na mesma linha)."""
    h = 140 if l2 else 100
    p = painel(X, Y, w, h)
    d = T("DICA", X + 24, Y + 36, 26, "left", MEN, bold=False)
    ls = []
    for l, yy in ((l1, Y + 80), (l2, Y + 122)):
        if l is None:
            continue
        ls.append(T(l, X + 24, yy, 30) if isinstance(l, str) else mixl(l, X + 24, yy - 10, 36))
    return p, d, ls


def poe_dica(sc, D):
    p, d, ls = D
    sc.play(Create(p), run_time=0.4)
    sc.pena(d)
    for l in ls:
        if hasattr(l, "p"):
            sc.pena(*l.p, lag=0.1)
        else:
            sc.pena(l)


def passos_card(X, Y, sz=34, w=640, on=0):
    """Cartão OS 4 PASSOS (sb35 passos()): número âmbar e texto branco nos acesos; apagados em #4A4570."""
    lh = sz * 1.6
    h = sz * 1.3 + lh * 4 + 16
    g = {"painel": painel(X, Y, w, h), "tit": T("OS 4 PASSOS", X + 28, Y + sz * 1.15, max(26, round(sz * .62)), "left", GEO, bold=False), "n": [], "t": [], "h": h}
    for i, t in enumerate(PASSOS):
        yy = Y + sz * 1.15 + lh * (i + 1)
        c = i < on
        g["n"].append(T(str(i + 1), X + 28, yy, sz, "left", E1 if c else GRAVE))
        g["t"].append(T(t, X + 28 + sz * 1.2, yy, sz, "left", BR if c else GRAVE))
    return g


def acende_passo(sc, g, i, rt=0.5):
    sc.play(g["n"][i].animate.set_fill(E1), g["t"][i].animate.set_fill(BR), run_time=rt)


def poe_card(sc, g, rt=0.5):
    sc.play(Create(g["painel"]), run_time=rt)
    sc.pena(g["tit"])
    sc.pena(*g["n"], *g["t"], lag=0.05)


def grupo_card(g):
    return VGroup(g["painel"], g["tit"], *g["n"], *g["t"])


# ── ícones da escada (sb35 icone(i, X, Y, s)) ─────────────────────────────────────────────────────────────────────────────────
def icone(i, X, Y, s=90):
    v = Vw(X - s / 2, Y + s / 2, s)
    fl = mixh(BG_, CI, .45)
    g = VGroup()
    rr = lambda a, b, c, d, fill=None, st=None: ret_px(*v.px(a, d), *v.px(b, c), fill=fill, stroke=st, wpx=2, z=3)
    pol = lambda pts, c: poly_px([v.px(*p) for p in pts], c, 1.0, z=2)
    ln = lambda pts, c, w=2: lin_px([v.px(*p) for p in pts], c, w, z=4)
    if i == 0:
        g.add(rr(.08, .92, .28, .72, fl, CI))
    if i == 1:
        g.add(pol([(.08, .08), (.92, .08), (.92, .92)], fl), rr(.08, .92, .08, .92, None, GEO))
    if i == 2:
        g.add(pol([(.1, .1), (.9, .1), (.1, .9)], fl), ln([(.1, .1), (.9, .1), (.1, .9), (.1, .1)], CI))
    if i == 3:
        p = [(.08 + a * .84 / 3, .08 + (4 * a - a * a) * .84 / 4) for a in np.linspace(0, 3, 41)]
        g.add(pol(p + [(.08, .08)], fl), ln(p, CORAL), ln([(.08, .08), (.92, .71)], AZC))
    if i == 4:
        p = [(a, .1 + .78 * math.exp(-(((a - .5) * 4.2) ** 2))) for a in np.linspace(.04, .96, 61)]
        g.add(pol(p + [(.96, .08), (.04, .08)], fl), ln(p, CI), ln([(.04, .08), (.96, .08)], GEO))
    if i == 5:
        g.add(pol([(.08, .08), (.92, .08), (.92, .92)], mixh(BG_, CI, .45)), pol([(.08, .08), (.08, .92), (.92, .92)], mixh(BG_, NEG, .45)),
              rr(.08, .92, .08, .92, None, GEO))
    if i == 6:
        q = v.px(.5, .5)
        g.add(rr(.1, .9, .1, .9, None, GEO), circ_px(*q, .4 * s, CI, 2, fill=fl, fop=1.0, z=3))
    if i == 7:
        for b in (.15, .5, .85):
            g.add(ln([(.04, b), (.96, b)], GEO))
        g.add(ln([(.3, .28), (.66, .72)], BR, 3))
    return g


# ── perspectiva cavaleira 2D (sb35 obl) ──────────────────────────────────────────────────────────────────────────────────
def obl(O0, ax, ay, az):
    return lambda X, Y, Z: (O0[0] + X * ax[0] + Y * ay[0] + Z * az[0], O0[1] + X * ax[1] + Y * ay[1] + Z * az[1])


def poly_pp(pts, fill=None, fop=1.0, stroke=None, wpx=2, dash=None, z=2):
    """Polígono com pontos em px: preenchimento e/ou contorno."""
    g = VGroup()
    if fill:
        g.add(poly_px(pts, fill, fop, z=z))
    if stroke:
        g.add(lin_px(list(pts) + [pts[0]], stroke, wpx, dash=dash, z=z + 1))
    return g


def seta_pp(A, B, cor, wpx=3, head=16, z=6):
    return seta_px(A, B, cor, wpx, head, z=z)


# ── utilidades ────────────────────────────────────────────────────────────────────────────────────────────────────────
def cria(sc, *ms, rt=0.6, extra=()):
    """Desenho nasce: traço por Create, preenchimento por FadeIn (sem flash de fórmula)."""
    an = []
    for m in ms:
        if isinstance(m, ImageMobject) or (isinstance(m, VMobject) and m.get_stroke_width() < 0.1 and m.get_fill_opacity() > 0):
            an.append(FadeIn(m))
        else:
            an.append(Create(m))
    sc.play(*an, *extra, run_time=rt)


def eixos_palco(v, a1, b1, lx=r"\X", ly=r"\Y"):
    sx, sy, Lx, Ly = eixos_v(v, a1, b1, lx=lx, ly=ly)
    return sx, sy, Lx, Ly


def palco(sc, v, area, a1, b1, ticks=(), rt=0.6, extra=(), lx=r"\X", ly=r"\Y"):
    """Papel do palco + eixos + marcas: a grade e os eixos nascem juntos; os números pela caneta. Devolve o dict das peças."""
    g = papel_v(v, area)
    sx, sy, Lx, Ly = eixos_v(v, a1, b1, lx=lx, ly=ly)
    tks = [tick(v, e, val, tex) for e, val, tex in ticks]
    sc.grade = g
    sc.play(FadeIn(g), GrowFromPoint(sx, v.P(0, 0)), GrowFromPoint(sy, v.P(0, 0)), *[Create(t[0]) for t in tks], *extra, run_time=rt)
    sc.pena(Lx, Ly, *[t[1] for t in tks], lag=0.05)
    return {"g": g, "sx": sx, "sy": sy, "lx": Lx, "ly": Ly, "tk": tks}


def expande(ms):
    """Grupos de linha mista (mixl/mista) entram na cena parte a parte: devolve as partes junto."""
    out = []
    for m in ms:
        if m is None:
            continue
        out.append(m)
        out += list(getattr(m, "p", []) or [])
    return out


def na_cena(sc, ms):
    """Os objetos de ms que estão na cena; um grupo fora da cena (LaggedStart põe os filhos) é trocado pelos filhos que estão."""
    out = []
    for m in expande(ms):
        if m in sc.mobjects:
            out.append(m)
        elif isinstance(m, (VGroup, Group)) and len(m.submobjects):
            out += na_cena(sc, m.submobjects)
    return out


def corta(sc, *ms, rt=0.35):
    ms = na_cena(sc, ms)
    if ms:
        sc.play(*[FadeOut(m) for m in ms], run_time=rt)
        for m in ms:
            m.clear_updaters()
        sc.remove(*ms)


def mapa_img(v, fun, a0, a1, b0, b1, cor_fn, n=240, z=1, mask=None):
    """Mapa de cor estático (imagem calculada uma vez) sobre [a0, a1] × [b0, b1] da vista v: cor_fn(valor) → (r, g, b) 0..255."""
    X0, Y1 = v.px(a0, b1)
    X1, Y0 = v.px(a1, b0)
    w, h = int(round(X1 - X0)), int(round(Y0 - Y1))
    us = a0 + (np.arange(w) + .5) / w * (a1 - a0)
    vs = b1 - (np.arange(h) + .5) / h * (b1 - b0)
    U, V = np.meshgrid(us, vs)
    rgb = cor_fn(fun(U, V))
    a = np.full(U.shape + (1,), 255.0)
    if mask is not None:
        a = np.where(mask(U, V)[..., None], 255.0, 0.0)
    return img_px(np.concatenate([rgb, a], 2), X0, Y1, w, h, z=z)


def rampa(c0, c1, t):
    t = np.clip(t, 0, 1)[..., None]
    return hx(c0) * (1 - t) + hx(c1) * t


_sai_fim0 = B36.sai_fim


def _sai_fim35(self, rt=0.25):
    """Fim de lote que já fechou a âncora antes (volta de cartão etc.): completa o tempo até o fim da fala antes de sair (sem deriva)."""
    if self._aid is None and self.alvo - self.nq > round(rt * FPS):
        self.wait((self.alvo - self.nq) / FPS - rt)
    _sai_fim0(self, rt)


B36.sai_fim = _sai_fim35


# ── palco vivo (handoff §3.2 "palco parado"): o termo lido acende no desenho; a canto troca junto do próximo play ─────────────────
def realca(sc, *ms, cor=None, rt=1.0, wpx=6):
    """Leitura no desenho: uma cópia só em traço, mais grossa, na cor do objeto (ou `cor`), nasce sobre ele, fica `rt` s e sai. Sem brilho."""
    hs = []
    for m in ms:
        h = m.copy()
        for x in h.family_members_with_points():
            if isinstance(x, VMobject):
                c = cor or (x.get_stroke_color() if x.get_stroke_width() > 0.1 else x.get_fill_color())
                x.set_fill(opacity=0).set_stroke(c, W(wpx), 1)
        sem_ctn(h).set_z_index(8)
        for x in h.get_family():
            x._txt = None
            x._leitura = True                    # yt_0036: a leitura no desenho não é traço para o R5
        hs.append(h)
    sc.play(*[Create(h) for h in hs], run_time=0.5)
    if rt > 0:
        sc.wait(rt)
    sc.play(*[FadeOut(h) for h in hs], run_time=0.4)
    sc.remove(*hs)


def _secao35(self, s, rt=0.35):
    """Linha 2 do canto: a troca entra no próximo play (sem um play só para ela: o palco não espera o canto)."""
    if self.h2 is not None and getattr(self.h2, "_s", None) == s:
        return
    novo = self._canto(txt(s, 21.6, color="#F5F7FF", bold=True, up=False), CANTO_Y2, topo_min=self._y1_fim_px() + 10)
    novo._s = s
    if self.h2 is not None:
        self._pend.append(FadeOut(self.h2))
    if self.h1 not in self.mobjects:
        self._pend.append(FadeIn(self.h1))
    self._pend.append(FadeIn(novo))
    self.h2 = novo


B36.secao = _secao35


def varre(sc, v, a0, lo, hi, amp, rt, sai=(), deitada=False):
    """A tira percorre a região (vai e volta em torno de a0, ±amp) com os pontos de entrada e saída presos às curvas; o que está na posição a0
    sai antes e volta depois."""
    t = ValueTracker(a0)
    if deitada:
        din = always_redraw(lambda: VGroup(tiraH(v, t.get_value(), lo(t.get_value()), hi(t.get_value()), h=.09),
                                           *pontos_es(v, (lo(t.get_value()), t.get_value()), (hi(t.get_value()), t.get_value()))))
    else:
        din = always_redraw(lambda: VGroup(tiraV(v, t.get_value(), lo(t.get_value()), hi(t.get_value()), h=.04),
                                           *pontos_es(v, (t.get_value(), lo(t.get_value())), (t.get_value(), hi(t.get_value())))))
    vis = [m for m in sai if m in sc.mobjects]
    sc.play(*[m.animate.set_opacity(0) for m in vis], run_time=0.3)
    sc.add(t, din)
    sc.play(t.animate(run_time=rt, rate_func=lambda u: math.sin(2 * math.pi * u)).set_value(a0 - amp), run_time=rt)
    din.clear_updaters()
    sc.remove(din, t)
    sc.play(*[m.animate.set_opacity(1) for m in vis], run_time=0.3)



# ══ v2 (handoff v2) ════════════════════════════════════════════════════════════════════════════════════════════════
# G1: o eixo y termina em y ≥ 215 px (1080p) e o rótulo vai à direita da ponta da seta (x + 22 px, centro na altura da ponta)
def eixos_v(v, a1, b1, a0=-.06, b0=-.06, lx=r"\X", ly=r"\Y", cx=E1, cy=E2):
    topo = v.px(0, b1)[1]
    if topo < 215:
        b1 = (v.cy - 215) / v.uy
    sx = seta_px(v.px(a0, 0), v.px(a1, 0), cx, 3, 16, z=6)
    sy = seta_px(v.px(0, b0), v.px(0, b1), cy, 3, 16, z=6)
    A, B = v.px(a1, 0), v.px(0, b1)
    Lx = TC(lx, A[0] + 22, A[1], 32, "c")
    Ly = TC(ly, B[0] + 22, B[1] + 6, 32, "l")
    return sx, sy, Lx, Ly


# G2: o título velho da linha 2 do canto sai (0,25 s) e só depois o novo entra (0,35 s, junto do próximo play); o selo PASSO idem
def _secao_v2(self, s, rt=0.35):
    if self.h2 is not None and getattr(self.h2, "_s", None) == s:
        return
    print(f"[canto] {getattr(self, '_aid', '?')} {self.t:.2f} {s}")      # final §7: QA do canto (a troca cai no 1º play da âncora)
    novo = self._canto(txt(s, 21.6, color="#F5F7FF", bold=True, up=False), CANTO_Y2, topo_min=self._y1_fim_px() + 10)
    novo._s = s
    velho = self.h2 if (self.h2 is not None and self.h2 in self.mobjects) else None
    # F6 (handoff final, retira o cross-fade do v3): o antigo sai em 0,15 s e SÓ DEPOIS o novo entra em 0,15 s; nunca no mesmo play.
    # O que estava pendente (_pend: saída do palco, linha 1) não entra nesses dois plays; volta para o próximo.
    # yt_0036: com título velho na tela, a troca é seca, no mesmo quadro (sem cruzamento, como pede o F6, e sem o quadro de canto vazio
    # entre o FadeOut e o FadeIn, que o QA "canto sem a linha 2" acusava em toda troca de seção).
    if velho is not None:
        self.remove(velho)
        self.add(novo)
        self.h2 = novo
        if self.h1 not in self.mobjects:
            self._pend.append(FadeIn(self.h1))
        return
    # yt_0036: sem título velho (lote que volta do A1): a linha 2 (e a 1, se faltar) entra seca, sem quadro de canto vazio
    if self.h1 not in self.mobjects:
        self.add(self.h1)
    self.add(novo)
    self.h2 = novo
    return
    guarda, self._pend = self._pend, []
    ent = [FadeIn(novo)]
    if self.h1 not in self.mobjects:
        ent.append(FadeIn(self.h1))
        guarda = [a for a in guarda if not (isinstance(a, FadeIn) and a.mobject is self.h1)]
    self.play(*ent, run_time=0.15)
    self.h2 = novo
    self._pend = guarda


B36.secao = _secao_v2
_selo0 = B36.selo_passo


def _selo_v2(self, n, rt=0.35):
    if self.sp is not None and n and getattr(self.sp, "_n", None) == n:
        return
    if self.sp is not None:
        self.play(FadeOut(self.sp), run_time=0.25)
        self.remove(self.sp)
        self.sp = None
    if n:
        _selo0(self, n, rt)


B36.selo_passo = _selo_v2


# Coluna (C1–C4) e chips (C3) ─────────────────────────────────────────────────────────────────────────────────────
COL_X, COL_Y0, COL_Y1, GAP = 1120, 250, 1000, 18


def topo_px(m):
    return pxof(m.get_top())[1]


def base_px(m):
    return pxof(m.get_bottom())[1]


class Coluna:
    """Coluna de fórmulas: cada linha nova começa abaixo da caixa da anterior (≥ 18 px); no máximo 8 linhas."""

    def __init__(self, sc, x=COL_X, y0=COL_Y0):
        self.sc, self.x, self.y0, self.ls = sc, x, y0, []

    def y_prox(self, m=None, gap=GAP):
        """Centro (px) da próxima linha para o mobject m (ou para uma linha de 40 px de altura)."""
        h = m.height * 120 if m is not None else 46
        b = max([base_px(l) for l in self.ls if l in self.sc.mobjects or any(p in self.sc.mobjects for p in getattr(l, "p", []))] or [self.y0 - gap])
        return b + gap + h / 2

    def poe(self, m, x=None, gap=GAP):
        """Encaixa m (já construído) abaixo da última linha, alinhado à esquerda em x."""
        y = self.y_prox(m, gap)
        m.shift(PX(x or self.x, y) - PX(pxof(m.get_left())[0], pxof(m.get_center())[1]))
        self.ls.append(m)
        if len([l for l in self.ls]) > 7:                        # v3: coluna com no máximo 7 linhas
            print(f"[coluna] AVISO {self.sc.lote} {self.sc._aid}: {len(self.ls)} linhas")
        if base_px(m) > COL_Y1:
            print(f"[coluna] AVISO {self.sc.lote} {self.sc._aid}: linha abaixo de {COL_Y1} px: {getattr(m, '_tex', '')[:60]!r}")
        return m

    def registra(self, m):
        self.ls.append(m)
        return m

    def tira(self, *ms):
        for m in ms:
            if m in self.ls:
                self.ls.remove(m)

    def fecha(self, res, saem, rt=1.0, escala=0.85, y=None):
        """C2: as linhas `saem` se fundem na linha-resultado `res`, que sobe ao topo da coluna (escala 0,85)."""
        sc = self.sc
        alvo = res.copy().scale(escala)
        if res not in sc.mobjects and not any(p in sc.mobjects for p in getattr(res, "p", [])):
            vis = [p for m in saem for p in expande([m]) if p in sc.mobjects]
            if vis:
                res.move_to(VGroup(*vis).get_center())
            res.set_opacity(0)
        yy = y or self.y0 + alvo.height * 60
        alvo.shift(PX(self.x, yy) - PX(pxof(alvo.get_left())[0], pxof(alvo.get_center())[1]))
        partes = [p for m in saem for p in expande([m]) if p in sc.mobjects and p is not res]
        voando = [x for p in partes + [res] for x in p.get_family()]
        for x in voando:
            x._voando = True                  # em fusão (C2): fora do R5, como os voos
        ja_escrita(res)                       # a linha-resultado nasce da fusão (a origem são as linhas do bloco), não da caneta
        for x in res.get_family():
            x._esc = True
            if getattr(x, "_caneta", False):
                x._caneta = False
        sc.play(*[Transform(p, alvo.copy().set_opacity(0)) for p in partes], Transform(res, alvo), run_time=rt)
        for x in voando:
            x._voando = False
        sc.remove(*partes)
        for m in saem:
            self.tira(m)
        self.ls = [l for l in self.ls if l is res]
        if res not in self.ls:
            self.ls.append(res)
        return res

    def limpa(self, rt=0.35):
        corta(self.sc, *self.ls, rt=rt)
        self.ls = []


CHIP_Y, CHIP_X1 = 168, 1890


class Chips:
    """C3: resultados usados depois; moldura GEO fina no alto da coluna (à direita), MathTex ≥ 30 px e o nome em Text 22 px."""

    def __init__(self, sc):
        self.sc, self.cs = sc, []

    def novo(self, nome, partes, de=None, rt=1.0, size=30):
        """partes = [(chave, tex)]: MathTex por peças (L) — as chaves servem para os voos. `de` = mobject de onde o valor voa."""
        sc = self.sc
        if partes and isinstance(partes[0], list):          # v3: chip em várias linhas empilhadas (nunca uma cadeia só)
            ls_ = [L(p_, 0, 0, 28, "l", caneta=False) for p_ in partes]
            for k_ in range(1, len(ls_)):
                ls_[k_].next_to(ls_[k_ - 1], DOWN, buff=8 / 120, aligned_edge=LEFT)
            m = VGroup(*ls_)
            m.ls = ls_
            m._tex = " / ".join(x._tex for x in ls_)
        else:
            m = L(partes, 0, 0, size, "l", caneta=False)
        nm = T(nome, 0, 0, 26, "left", GEO, bold=False, caneta=False)
        w = nm.width * 120 + 12 + m.width * 120 + 28
        X1 = min([pxof(c.get_left())[0] - 14 for c in self.cs] or [CHIP_X1])
        X0 = X1 - w
        hh = max(52, m.height * 120 + 18)
        cy_ = max(CHIP_Y, 118 + hh / 2)                     # abaixo do logo
        mol = moldura(X0, cy_ - hh / 2, w, hh, GEO, .55, 1.5, 8)
        nm.shift(PX(X0 + 14, CHIP_Y + 8) - PX(pxof(nm.get_left())[0], base_de(nm) * -120 + 540 if False else pxof(nm.get_center())[1]))
        nm.move_to(PX(X0 + 14 + nm.width * 60, cy_))
        m.move_to(PX(X0 + 14 + nm.width * 120 + 12 + m.width * 60, cy_))
        g = VGroup(mol, nm, m)
        g.m, g.nome = m, nome
        if de is not None:
            sc.play(Create(mol), FadeIn(nm), run_time=0.35)
            voa(sc, de.copy() if de in sc.mobjects else de, m, rt=rt)
        else:
            sc.play(Create(mol), FadeIn(nm), run_time=0.35)
            if hasattr(m, "ls"):
                sc.pena(*m.ls, lag=0.1)
            else:
                sc.pena(m)
        self.cs.append(g)
        return g

    def todos(self):
        return [p for g in self.cs for p in (g, g[0], g[1], g.m, *getattr(g.m, "ls", []))]


def mol_chip_fixos(sc):
    return set(getattr(sc, "chips", None).todos()) if getattr(sc, "chips", None) else set()


_fixos0 = B36.fixos


def _fixos_v2(self):
    f = _fixos0(self)
    ch = getattr(self, "chips", None)
    if ch is not None:
        f = set(f) | set(ch.todos())
    return f


B36.fixos = _fixos_v2


# O1 · primitiva: ∫ … = [F]ₐᵇ = F(b) − F(a) = r, três estados de um MathTex por mapa; os limites voam da integral para o colchete ──────
def lims_de(m, chave):
    g = sel(m, chave)
    alto = max(g, key=lambda k: m[0][k].height)
    cy = m[0][alto].get_center()[1]
    lo = [k for k in g if k != alto and m[0][k].get_center()[1] < cy]
    hi = [k for k in g if k != alto and m[0][k].get_center()[1] >= cy]
    return lo, hi


def lims_sb(m, chave):
    """Índices de baixo e de cima de uma peça `_{a}^{b}` (sub e sobrescrito)."""
    g = sel(m, chave)
    ys = [m[0][k].get_center()[1] for k in g]
    med = (max(ys) + min(ys)) / 2
    return [k for k in g if m[0][k].get_center()[1] < med], [k for k in g if m[0][k].get_center()[1] >= med]


def prim(sc, A, pecas, ik, F, a, b, dif, res, X=None, Y=None, size=None, wrap=780, nota="", res_extra=None, colchete=(r"\Big[", r"\Big]"), pre=None,
         rel3="=", voo_F=None, voo_pre=None):
    """A = linha já na tela (L) com as peças `pecas` [(chave, tex)]; `ik` = chave da peça ∫ (cujos limites voam para o colchete).
    Estados: A → A = [F]_a^b → … = dif → … = res. Se a linha passar de `wrap` px, a continuação desce (linha com '=' sob a de cima).
    Devolve (última linha, lista das linhas criadas)."""
    size = size or A._size if hasattr(A, "_size") else (size or 36)
    X = X if X is not None else pxof(A.get_left())[0]
    Y = Y if Y is not None else pxof(A.get_center())[1]
    lb, rb = colchete
    P1 = pecas + [("e1", "=")] + ([("pre", pre)] if pre else []) + [("lb", lb), ("F", F), ("rb", rb), ("sb", "_{%s}^{%s}" % (a, b))]
    B1 = L(P1, X, Y, size)
    B1._size = size
    lo, hi = lims_de(A, ik)
    slo, shi = lims_sb(B1, "sb")
    vF = ([(voo_F.copy(), "F")] if voo_F is not None else []) + ([(voo_pre.copy(), "pre")] if voo_pre is not None else [])
    passo(sc, A, B1, [(k, k) for k, _ in pecas], voos=[(VGroup(*[A[0][k] for k in lo]).copy(), slo), (VGroup(*[A[0][k] for k in hi]).copy(), shi)] + vF,
          rt=0.6 if voo_F is None else 0.9, nota=f"O1 colchete {nota}")
    linhas = [B1]
    P2 = P1 + [("e2", "="), ("d", dif)]
    B2 = L(P2, X, Y, size)
    if B2.width * 120 <= wrap:
        passo(sc, B1, B2, [(k, k) for k, _ in P1], rt=0.5, nota=f"O1 diferença {nota}")
        linhas[-1] = B2
        cur, Pc = B2, P2
    else:
        Q = [("e2", "="), ("d", dif)]
        B2 = L(Q, X + 40, 0, size)
        B2.shift(UP * ((pxof(B1.get_bottom())[1] + GAP + B2.height * 60) * -1 / 120 + 4.5 - B2.get_center()[1]))
        sc.pena(B2)
        linhas.append(B2)
        cur, Pc = B2, Q
    P3 = Pc + [("e3", rel3), ("r", res)]
    B3 = L(P3, pxof(cur.get_left())[0], pxof(cur.get_center())[1], size)
    if B3.width * 120 <= wrap + 40:
        passo(sc, cur, B3, [(k, k) for k, _ in Pc], rt=0.5, nota=f"O1 número {nota}")
        if cur is B2 and len(linhas) > 1:
            linhas[-1] = B3
        else:
            linhas[-1] = B3
        return B3, linhas
    Q3 = [("e3", rel3), ("r", res)]
    B3 = L(Q3, X + 40, 0, size)
    B3.shift(UP * ((pxof(cur.get_bottom())[1] + GAP + B3.height * 60) * -1 / 120 + 4.5 - B3.get_center()[1]))
    sc.pena(B3)
    linhas.append(B3)
    return B3, linhas


# O2 · chave desenhada no palco (horizontal embaixo ou vertical ao lado), com o rótulo em MathTex na cor da medida ───────────────────
def chave_h(X0, X1, Y, cor=GEO, wpx=2, para_baixo=True):
    """Chave horizontal de X0 a X1 em Y; a ponta aponta para baixo (rótulo embaixo) ou para cima."""
    s = 1 if para_baixo else -1

    def qb(a, c, b_, n=10):
        return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b_[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b_[1]) for t in np.linspace(0, 1, n)]
    m = (X0 + X1) / 2
    pts = qb((X0, Y - 8 * s), (X0, Y), (X0 + 10, Y)) + qb((m - 10, Y), (m, Y), (m, Y + 10 * s)) + qb((m, Y + 10 * s), (m, Y), (m + 10, Y)) + \
        qb((X1 - 10, Y), (X1, Y), (X1, Y - 8 * s))
    return lin_px(pts, cor, wpx, z=6)


def chave_v(X, Y0, Y1, cor=GEO, wpx=2, para_esq=True):
    s = -1 if para_esq else 1

    def qb(a, c, b_, n=10):
        return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b_[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b_[1]) for t in np.linspace(0, 1, n)]
    m = (Y0 + Y1) / 2
    pts = qb((X - 8 * s, Y0), (X, Y0), (X, Y0 + 10)) + qb((X, m - 10), (X, m), (X + 10 * s, m)) + qb((X + 10 * s, m), (X, m), (X, m + 10)) + \
        qb((X, Y1 - 10), (X, Y1), (X - 8 * s, Y1))
    return lin_px(pts, cor, wpx, z=6)


def medida(sc, ch, tex, X, Y, size=28, al="c"):
    """Chave + rótulo (MathTex com placa mínima) escritos a caneta."""
    r = TP(tex, X, Y, size, al)
    sc.play(Create(ch), run_time=0.4)
    sc.pena(r)
    return r


def segura(sc, minimo=2.5, desde=None):
    """G7: um resultado fica ≥ 2,5 s antes de a cena sair."""
    if desde is not None and sc.t - desde < minimo:
        sc.wait(minimo - (sc.t - desde))


def _escreve_com_voos(self, m, voos_, depois=(), rt=0.7, seq=True):
    """G3/C4: os glifos sem fonte vão pela caneta; os voos pousam nos lugares vazios; `depois` (chaves) é escrito depois dos voos.
    voos_ = [(fonte, chaves | índices)]."""
    voadas, dep = set(), set(sel(m, list(depois))) if depois else set()
    for v_ in voos_:
        ks = v_[1]
        voadas |= set(sel(m, ks if isinstance(ks, (list, tuple)) else [ks]))
    resto = [k for k in range(len(m[0])) if k not in voadas and k not in dep]
    if resto:
        self.pena(parte(m, resto, "sem fonte"))
    voos(self, [(v_[0].copy(), parte(m, sel(m, v_[1] if isinstance(v_[1], (list, tuple)) else [v_[1]]), str(v_[1])[:20])) + tuple(v_[2:])
                for v_ in voos_], rt=rt, seq=seq)
    if dep:
        self.pena(parte(m, sorted(dep), "depois"))
    m._esc = True
    return m


def _lin_b(self, pecas, size=34, caneta=True, x=None, gap=GAP):
    m = L(pecas, COL_X, 0, size, "l", caneta=caneta)
    m._size = size
    self.col.poe(m, x=x, gap=gap)
    return m


def _mix_b(self, partes, S=32, x=None, gap=GAP):
    m = mixl(partes, COL_X, 0, S)
    self.col.poe(m, x=x, gap=gap)
    return m


B36.escreve_voos = _escreve_com_voos
if not hasattr(B36, "lin"):
    B36.lin, B36.mix = _lin_b, _mix_b


def nd(m, k):
    """Fração da peça k: (numerador ordenado em x, traço, denominador)."""
    cy = m.get_center()[1]
    idx = sel(m, k)
    ys = [m[0][i].get_center()[1] for i in idx]
    c = (max(ys) + min(ys)) / 2 if ys else cy
    hi = sorted([i for i in idx if m[0][i].get_center()[1] > c + .05], key=lambda i: m[0][i].get_center()[0])
    lo = sorted([i for i in idx if m[0][i].get_center()[1] < c - .05], key=lambda i: m[0][i].get_center()[0])
    bar = [i for i in idx if i not in hi and i not in lo]
    return hi, bar, lo


def tira_chips(sc):
    if getattr(sc, "chips", None) is not None and sc.chips.cs:
        corta(sc, *sc.chips.cs)
        sc.chips.cs = []


# ── G4 (v2): palco vivo automático ────────────────────────────────────────────────────────────────────────────────────────
# Quando o palco (x < 1090 px) fica ≥ 3 s sem animação — conta só na coluna, ou espera da fala —, o próximo play/espera faz a leitura no
# desenho: o contorno da região (ou da curva principal) acende e apaga, como o realca. Assim nenhum trecho passa de 5 s parado.
VIVO_LIM = 2.5


def _no_box(self, x, y):
    """yt_0036: a caixa do palco muda por âncora (J36.an): A = x < 1090; B5-2 = miniaturas à direita; B6-3/B7 = x < 750."""
    x0, x1, y0 = getattr(self, "PALCO_BOX", (0, 1090, 190))
    return x0 <= x < x1 and y > y0


def _mobs_de(a):
    if a.__class__.__name__ == "_AnimationBuilder":
        yield a.mobject
        return
    for k in ("mobject", "target_mobject"):
        if getattr(a, k, None) is not None:
            yield getattr(a, k)
    for b in getattr(a, "animations", None) or []:
        yield from _mobs_de(b)


def _no_palco(self, anims):
    fix = self.fixos()
    for a in anims:
        for m in _mobs_de(a):
            if m is self.clk or m in fix or type(m) is Mobject:      # Mobject puro = o contêiner do TransformByGlyphMap (na origem)
                continue
            try:
                x, y = pxof(m.get_center())
            except Exception:
                continue
            if _no_box(self, x, y):
                if os.environ.get("DEBUG_VIVO"):
                    print(f"[vivo-palco] {self._aid} {self.t:.2f} {type(a).__name__} {type(m).__name__} {getattr(m, '_tex', '')!s:.40} ({x:.0f},{y:.0f})")
                return True
    return False


def _foco_auto(self):
    fix = self.fixos()
    melhor, area = None, 0.0
    for m in self.mobjects:
        if m in fix or m is getattr(self, "grade", None) or not isinstance(m, VMobject) or getattr(m, "_tex", None) is not None:
            continue
        if (m.z_index or 0) <= -9 or getattr(m, "_sem_foco", False):        # yt_0036: papel e famílias de retas não são foco de leitura
            continue
        if getattr(m, "_txt", None) is not None or not m.family_members_with_points():
            continue
        if type(m).__name__ == "Fundo3D" or m.width * 120 > 1400:      # o fundo 3D (tela inteira) não é foco de leitura
            continue
        x, y = pxof(m.get_center())
        if not _no_box(self, x, y):
            continue
        cheio = any(isinstance(g, VMobject) and g.get_fill_opacity() > .3 and g.width * g.height > .05 for g in m.family_members_with_points())
        a_ = m.width * m.height * (3 if cheio else 1)
        if a_ > area and m.width * 120 > 60:
            melhor, area = m, a_
    if melhor is None:                         # palco 3D: o rótulo preso (placa) acende
        for m in self.mobjects:
            if m in fix or not hasattr(m, "f") or not isinstance(m, VGroup) or not len(m.submobjects):
                continue
            x, y = pxof(m.get_center())
            if _no_box(self, x, y) and m.width * m.height > area:
                melhor, area = m[0], m.width * m.height
    if melhor is None and False:               # v2 Q08: fórmula nunca acende em traço (o det "borrado"); sem forma no palco, sem leitura
        for m in self.mobjects:
            if m in fix or getattr(m, "_tex", None) is None or not isinstance(m, VMobject):
                continue
            x, y = pxof(m.get_center())
            if _no_box(self, x, y) and m.width * m.height > area:
                melhor, area = m, m.width * m.height
    return melhor


def _pulso(self, rt):
    f = _foco_auto(self)
    # v2 Q07: numa célula (chapa + malha + borda), a leitura percorre só a borda; percorrer a malha deixava tracinhos brancos no começo
    # de cada linha da malha
    if f is not None and getattr(f, "borda", None) is not None:
        f = f.borda
    if os.environ.get("DEBUG_VIVO"):
        print(f"[vivo-pulso] {self._aid} {self.t:.2f} rt={rt:.2f} box={getattr(self, 'PALCO_BOX', None)} foco={type(f).__name__ if f is not None else None} "
              f"{pxof(f.get_center()) if f is not None else ''}")
    if f is None:
        return None, None
    h = f.copy()
    h.clear_updaters()
    for x in h.family_members_with_points():
        if isinstance(x, VMobject):
            c = x.get_stroke_color() if x.get_stroke_width() > 0.1 else x.get_fill_color()
            if sum(ManimColor(c).to_rgb()) < 0.75:          # placa escura: a leitura acende em GEO
                c = GEO
            c = mixh(ManimColor(c).to_hex(), BR, .55)      # mais claro que o traço de baixo: a leitura aparece mesmo sobre a própria linha
            x.set_fill(opacity=0).set_stroke(c, W(5), 0)
    sem_ctn(h).set_z_index(8)
    for x in h.get_family():
        x._txt = None
        x._leitura = True
    base = h.copy()
    # v2 Q07: as linhas internas de malha (de qualquer célula dentro do foco) não entram na leitura
    malha = {id(y) for x in h.get_family() if getattr(x, "malha", None) is not None for y in x.malha.get_family()}
    fams = [(x, b) for x, b in zip(h.family_members_with_points(), base.family_members_with_points()) if id(x) not in malha]
    for x in h.family_members_with_points():
        if id(x) in malha:
            x.set_stroke(opacity=0)
    for x, b in fams:
        b.set_stroke(opacity=.75)

    nc = max(1, round(rt / 2.4))                   # yt_0036: espera longa = vários ciclos de ~2,4 s (um ciclo só de 8 s quase não muda o quadro)

    def upd(m, a):
        # a leitura percorre o contorno devagar (mudança contínua, sem piscar) e some no fim de cada ciclo
        a = 1.0 if a >= 1 else (a * nc) % 1.0
        p_ = min(1.0, a / .85)
        op = .75 if a < .85 else .75 * (1 - (a - .85) / .15)
        for x, b in fams:
            x.pointwise_become_partial(b, 0, max(1e-3, p_))
            x.set_stroke(opacity=op)
    self.add(h)
    an = UpdateFromAlphaFunc(h, upd, rate_func=linear, run_time=rt)
    return h, an


_play_b35 = B36.play
_wait_b35 = B36.wait


def _play_vivo(self, *anims, run_time=None, **kw):
    rt = run_time if run_time is not None else max([getattr(a, "run_time", 1.0) for a in anims] or [1.0])
    h = None
    if _no_palco(self, anims):
        self._t_palco = self.t + rt
    elif not getattr(self, "_sem_vivo", False) and rt >= 0.5 and self.t - getattr(self, "_t_palco", 0.0) >= VIVO_LIM:
        h, an = _pulso(self, rt)
        if an is not None:
            anims = (*anims, an)
            self._t_palco = self.t + rt
    _play_b35(self, *anims, run_time=run_time, **kw)
    if h is not None:
        self.remove(h)


def _wait_vivo(self, duration=1.0, *a, **kw):
    if not getattr(self, "_sem_vivo", False) and duration >= 0.6 and self.t + duration - getattr(self, "_t_palco", 0.0) >= VIVO_LIM:
        h, an = _pulso(self, duration)
        if an is not None:
            _play_b35(self, an, run_time=duration)
            self.remove(h)
            self._t_palco = self.t
            return
    _wait_b35(self, duration, *a, **kw)


B36.play, B36.wait = _play_vivo, _wait_vivo


# PAUSE E TENTE: o log marca quando o selo entra e quando sai (QA: mínimo 3 s)
_pausa0 = pausa


def pausa(X, Y):
    sl = _pausa0(X, Y)
    for m in sl:
        m._pausa = True
    return sl


_poe_selo0 = poe_selo


def poe_selo(sc, sl, extra=()):
    if getattr(sl[0], "_pausa", False):
        print(f"[pausa] {sc._aid} {sc.t:.2f} entra")
        sc._pausa_on = True
    _poe_selo0(sc, sl, extra)


_remove_b35 = B36.remove


def _remove_pausa(self, *ms):
    if getattr(self, "_pausa_on", False) and any(getattr(m, "_pausa", False) for m in ms):
        print(f"[pausa] {self._aid} {self.t:.2f} sai")
        self._pausa_on = False
    return _remove_b35(self, *ms)


B36.remove = _remove_pausa



# ── v3 §4.2: troca de bloco com fades sobrepostos (o palco seguinte entra enquanto o anterior sai) ─────────────────────────────
def _limpa_v3(self, rt=0.4, keep=()):
    """O que sai entra no próximo play (FadeOut junto da entrada do palco novo); fora do R5 enquanto sai."""
    sai = [m for m in self.snap() if m not in keep] + ([self.grade] if self.grade is not None else [])
    for m in sai:
        m.clear_updaters()
        for x in m.get_family():
            x._saindo = True
            x._esc = True
    self._pend += [FadeOut(m, run_time=rt) for m in sai]
    self._sair = getattr(self, "_sair", []) + sai
    self.grade = None
    for m in [m for m in self.mobjects if isinstance(m, ValueTracker) and m is not self.clk]:
        self.remove(m)


B36.limpa_tudo = _limpa_v3
_play_v2b = B36.play
_wait_v2b = B36.wait


def _tira_sair(self):
    if getattr(self, "_sair", None):
        self.remove(*self._sair)
        self._sair = []


def _play_v3(self, *anims, **kw):
    # v2 §7.1: o que sai em FadeOut fica fora do R5 durante a saída (não é leitura sobreposta, é a troca de palco)
    for a in anims:
        if isinstance(a, FadeOut):
            for x in a.mobject.get_family():
                x._saindo = True
    _play_v2b(self, *anims, **kw)
    _tira_sair(self)


def _wait_v3(self, duration=1.0, *a, **kw):
    if self._pend:
        d = min(duration, 0.4)
        _play_v2b(self, run_time=d)
        _tira_sair(self)
        duration -= d
        if duration < 1 / 15:
            return
    _wait_v2b(self, duration, *a, **kw)


B36.play, B36.wait = _play_v3, _wait_v3


# ── v3: auxiliares compartilhados (2D → 3D, giro da câmera, chave paralela a um segmento qualquer) ─────────────────────────────
def gira_z(c, graus):
    """A câmera c girada em torno do eixo z que passa pelo alvo."""
    a = math.radians(graus)
    p, t = np.array(c["pos"]), np.array(c["tgt"])
    d = p - t
    r = np.array([d[0] * math.cos(a) - d[1] * math.sin(a), d[0] * math.sin(a) + d[1] * math.cos(a), d[2]])
    return cam_dict(t + r, t, c["up"], c["cx"], c["cy"], c["fov"])


def para_3d(sc, pal, rt=0.8):
    """Do palco 2D para o Three.js: o 3D acende por baixo enquanto o palco 2D sai (a coluna fica)."""
    pal.fundo.op.set_value(0.0)
    sc.add(pal.fundo)
    sai = [m for m in sc.snap() if m is not pal.fundo and pxof(m.get_center())[0] < 1090] + ([sc.grade] if sc.grade is not None else [])
    sc.play(*[FadeOut(m) for m in sai], pal.fundo.op.animate.set_value(1.0), run_time=rt)
    for m in sai:
        m.clear_updaters()
    sc.remove(*sai)
    sc.grade = None


def chave_seg(A, B, off=16, cor=GEO, wpx=2):
    """Cota paralela ao segmento AB (px), deslocada `off` px à esquerda do sentido A→B, com tiques nas pontas. Devolve (VGroup, normal)."""
    ax, ay = A
    bx, by = B
    L_ = math.hypot(bx - ax, by - ay)
    nx, ny = -(by - ay) / L_, (bx - ax) / L_
    a2, b2 = (ax + nx * off, ay + ny * off), (bx + nx * off, by + ny * off)
    t = 7
    return VGroup(lin_px([a2, b2], cor, wpx, z=7), lin_px([(a2[0] - nx * t, a2[1] - ny * t), (a2[0] + nx * t, a2[1] + ny * t)], cor, wpx, z=7),
                  lin_px([(b2[0] - nx * t, b2[1] - ny * t), (b2[0] + nx * t, b2[1] + ny * t)], cor, wpx, z=7)), (nx, ny)


def linha_u(sc, u, du, pedaco, k, size=30):
    """O4 · linha u = … ⇒ du = … ⇒ (pedaço) = …du (a caneta escreve; a coluna encaixa)."""
    m = sc.lin([("u", u), ("i1", r"\ \Rightarrow\ "), ("du", du)] + ([("i2", r"\ \Rightarrow\ "), ("p", pedaco)] if pedaco else []), size)
    sc.pena(m)
    return m


def linha_lim(sc, var, a, ua, b, ub, size=30):
    """O4 · linha dos limites novos: var = a → u = ua;  var = b → u = ub (os valores de u em peças, para voar)."""
    m = sc.lin([("a", r"%s=%s\to u=" % (var, a)), ("ua", ua), ("pv", r";\qquad"), ("b", r"%s=%s\to u=" % (var, b)), ("ub", ub)], size)
    sc.pena(m)
    return m


# ── handoff final (F7, F10): rótulo de objeto 3D = chave fina + texto ≥ 28 px FORA da face, sem caixa escura, preso por prende ─────────
def chave_rotulo(pal, A, B, Cc, ponto, partes, off=18, S=30):
    """Chave fina ao longo de AB (px), do lado oposto ao ponto Cc (o interior da face), e o rótulo misto `partes` (mixl) do mesmo lado,
    preso ao ponto 3D `ponto` (cada peça com prende). Devolve (chave, rótulo com .p)."""
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    _, (nx, ny) = chave_seg(A, B, off)
    s = 1 if (mx - Cc[0]) * nx + (my - Cc[1]) * ny > 0 else -1
    k, _ = chave_seg(A, B, s * off, GEO)
    lab = mixl(partes, 0, 0, S)
    w, h = lab.width * 120, lab.height * 120
    d = s * (off + abs(nx) * w / 2 + abs(ny) * h / 2 + 12)
    lab.shift(PX(mx + nx * d, my + ny * d) - lab.get_center())
    q = pal.pt(ponto)
    for m in lab.p:
        mc = pxof(m.get_center())
        pal.prende(m, ponto, mc[0] - q[0], mc[1] - q[1])
    return k, lab
