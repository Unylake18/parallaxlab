"""yt_0030 v2 · motor da álgebra passo a passo (handoff v2 §2–§3). Toda linha de fórmula é uma `Lin`: MathTex de string única feito de PEÇAS com chave;
a transformação de uma linha na seguinte é um TransformByGlyphMap (MF-Tools) com o mapa montado pelas chaves (peças com a mesma chave casam; o resto
some/entra por auto_fade). Os VOOS (R11-b) entram no próprio glyph map como introdutores: a peça nova voa de uma peça visível da tela, que acende na
cor dela durante o voo. Cancelamento (R14): o par fica coral, um traço coral risca cada termo e o par some no glyph map seguinte.

Origens (R11): caneta (a), voo (b), glyph map (c) — registradas em [origem]; um MathTex que entra na cena sem origem vira [sem-origem] (QA).
Glyph maps: [gm] (tempo, A → B, pares, auto_fade); a reserva TransformMatchingShapes não existe aqui (um mapa que não fecha levanta erro)."""
from lib30 import *  # noqa: F401,F403
from lib30 import _play_c, _nglifos  # noqa: F401
import lib30 as _l30

CORAL_C = CORAL
GM_LOG = []


_LINS = []                            # todas as Lin criadas (R13 conta as que têm glifos visíveis na cena)


class Lin(MathTex):
    """Linha de conta: pecas = [tex | (chave, tex)]; x, y em px (y = centro), al = 'l' | 'c' | 'r'."""

    def __init__(self, pecas, x=1120, y=540, size=36, al="l"):
        ks, ts, nfix = [], [], []
        for p in pecas:                   # (chave, tex, n): peça que não compila sozinha (ex.: "}{" = traço da fração) com n glifos dados
            k, t = (p[:2] if isinstance(p, tuple) else (p, p))
            ks.append(k)
            ts.append(t)
            nfix.append(p[2] if isinstance(p, tuple) and len(p) > 2 else None)
        import re as _re
        tj = ""
        for t in ts:                      # "\alpha" + "s" não pode virar "\alphas": espaço entre palavra de controle e letra
            if tj and _re.search(r"\\[A-Za-z]+$", tj) and _re.match(r"[A-Za-z]", t):
                tj += " "
            tj += t
        super().__init__(tj, font_size=fs(size), tex_template=TEX27)
        self._tex, self._caneta, self._esc, self._em_caneta = tj, True, False, False
        for g in self.get_family()[1:]:
            g._sem_contorno = True
        p = PX(x, y)
        self.move_to(p)
        if al == "l":
            self.shift(RIGHT * (p[0] - self.get_left()[0]))
        elif al == "r":
            self.shift(RIGHT * (p[0] - self.get_right()[0]))
        self.set_z_index(25)
        ns = [(_nglifos(t) if n is None else n) for t, n in zip(ts, nfix)]
        if any(n < 0 for n in ns) or sum(ns) != len(self[0]):
            raise ValueError(f"[lin] peças não somam {ns} ({sum(ns)}) × {len(self[0])}: {self._tex!r}")
        k0, self._rg = 0, []
        for n in ns:
            self._rg.append(list(range(k0, k0 + n)))
            k0 += n
        self.ks, self.ts, self.size = ks, ts, size
        _LINS.append(self)

    def p(self, *chaves):
        """Glifos das peças com essas chaves (todas as ocorrências), como VGroup."""
        return VGroup(*[self[0][g] for i, k in enumerate(self.ks) if k in chaves for g in self._rg[i]])

    def pi(self, *idx):
        return VGroup(*[self[0][g] for i in idx for g in self._rg[i]])

    def em(self, x=None, y=None, al="l"):
        if y is not None:
            self.set_y(PX(0, y)[1])
        if x is not None:
            p = PX(x, 0)[0]
            self.shift(RIGHT * (p - (self.get_left()[0] if al == "l" else self.get_center()[0] if al == "c" else self.get_right()[0])))
        return self


def L(pecas, x=1120, y=540, size=36, al="l"):
    return Lin(pecas, x, y, size, al)


def _voo_cls(src, cor=None):
    class _Voo(TransformFromCopy):
        def __init__(self, mob, **kw):
            kw.pop("shift", None)
            super().__init__(src, mob, **kw)
    return _Voo


def gm(cena, A, B, rt=0.9, voos=None, copia=False, extra=(), somem=(), nota="", ka=None, kb=None):
    """Glyph map A → B por chave. voos = {chave em B: mobject-fonte} (voa da fonte; a fonte acende na cor do destino).
    copia=True: A fica (o molde é copiado). somem: traços do cancelamento que saem junto."""
    voos = voos or {}
    usadosA, ent = set(), []
    from collections import defaultdict
    ia, ib = defaultdict(list), defaultdict(list)
    for i, k in enumerate(ka or A.ks):
        ia[k].append(i)
    for j, k in enumerate(kb or B.ks):
        ib[k].append(j)
    pares = 0
    for k, js in ib.items():
        if k in voos:
            g = [x for j in js for x in B._rg[j]]
            ent.append(([], g, {}) if False else (_voo_cls(voos[k]), g, {}))
            continue
        is_ = ia.get(k, [])
        if not is_:
            continue
        if len(is_) == len(js):
            for i, j in zip(is_, js):
                ent.append((A._rg[i], B._rg[j]))
                pares += 1
        elif len(js) == 1:
            ent.append(([x for i in is_ for x in A._rg[i]], B._rg[js[0]]))
            pares += 1
        elif len(is_) == 1:
            for j in js:
                ent.append((A._rg[is_[0]], B._rg[j]))
                pares += 1
        else:
            for i, j in zip(is_, js):
                ent.append((A._rg[i], B._rg[j]))
                pares += 1
    ent = [e for e in ent if e[1] or e[0]]
    if not ent:                      # mapa vazio faria o MF-Tools mostrar os índices (depuração): a linha inteira vira a nova
        ent = [(list(range(len(A[0]))), list(range(len(B[0]))))]
        pares = 1
    piscas = [pisca_cor(s, (B.p(k)[0].get_fill_color() if len(B.p(k)) else CAMPO2), rt) for k, s in voos.items()]
    an = TransformByGlyphMap(A, B, *ent, from_copy=copia, auto_fade=True, printing=False, run_time=rt)
    B._origem, B._esc = "c", True
    t = cena.t
    GM_LOG.append((cena.lote, cena._aid, t, A._tex, B._tex, pares, len(voos)))
    print(f"[gm] {cena.lote} {cena._aid} {t:.2f} pares={pares} voos={len(voos)} {nota} :: {A._tex[:70]!r} → {B._tex[:70]!r}")
    print(f"[origem] c {cena.lote} {cena._aid} {t:.2f} {B._tex[:90]!r} ← {A._tex[:60]!r}")
    def post():
        if not copia:
            cena.remove(A)
        limpa_soltos(cena)
        cena.add(B)
        cena.remove(*somem)
    anims = [an, *piscas, *extra, *[FadeOut(s) for s in somem]]
    if getattr(cena, "_lote_gm", None) is not None:
        cena._lote_gm.append((anims, post))
        return B
    cena.play(*anims, run_time=rt)
    post()
    return B


def em_paralelo(cena, rt, *fns, extra=()):
    """Roda vários gm (funções sem argumento que chamam gm) no MESMO play."""
    cena._lote_gm = []
    for f in fns:
        f()
    lote, cena._lote_gm = cena._lote_gm, None
    cena.play(*[a for an, _ in lote for a in an], *extra, run_time=rt)
    for _, p in lote:
        p()


def escreve(cena, m, ritmo=0.35, atraso=0.0, extra=(), rt=None):
    """Caneta (R11-a)."""
    m._origem = "a"
    print(f"[origem] a {cena.lote} {cena._aid} {cena.t:.2f} {getattr(m, '_tex', '')[:90]!r}")
    if rt:
        cena.play(caneta(m, ritmo=ritmo, atraso=atraso), *extra, run_time=rt)
    else:
        cena.play(caneta(m, ritmo=ritmo, atraso=atraso), *extra)
    return m


def escreve_p(cena, m, chaves, ritmo=0.35, extra=()):
    """Caneta só nas peças `chaves` (por índice ou chave); a linha inteira entra na cena no fim (junta)."""
    g = m.pi(*chaves) if all(isinstance(c, int) for c in chaves) else m.p(*chaves)
    print(f"[origem] a {cena.lote} {cena._aid} {cena.t:.2f} {m._tex[:60]!r} (peças {chaves})")
    cena.play(caneta(g, ritmo=ritmo), *extra)
    return g


def voa(cena, src, dst, rt=0.7, extra=()):
    """Voo (R11-b): dst (glifos de uma linha ou mobject) nasce de uma cópia de src; src acende na cor do destino durante o voo."""
    cor = dst[0].get_fill_color() if isinstance(dst, VGroup) and len(dst) else dst.get_fill_color()
    print(f"[origem] b {cena.lote} {cena._aid} {cena.t:.2f} {getattr(dst, '_tex', type(dst).__name__)!s:.60} ← voo")
    if isinstance(dst, MathTex):
        dst._origem = "b"
    cena.play(TransformFromCopy(src, dst), pisca_cor(src, cor, rt), *extra, run_time=rt)
    if isinstance(dst, MathTex):
        dst._origem = "b"
    return dst


def junta(cena, m, origem="a"):
    """Os grupos de glifos de `m` soltos na cena (caneta por partes, voos) viram o MathTex inteiro."""
    junta_partes(cena, m)
    m._origem, m._esc = origem, True
    return m


def pisca_cor(mob, cor, rt=0.7):
    """A peça-fonte acende (cor do destino) e volta, dentro da mesma animação (there_and_back)."""
    gs = [g for g in mob.family_members_with_points()]
    c0 = [ManimColor(g.get_fill_color()) for g in gs]
    c1 = ManimColor(cor)

    def f(m, a):
        u = there_and_back(a)
        for g, c in zip(gs, c0):
            g.set_fill(interpolate_color(c, c1, u))
    return UpdateFromAlphaFunc(mob, f, run_time=rt)


def cancela(cena, m, *chaves, rt=0.3):
    """R14: o par fica coral (0,3 s) e um traço coral de 2 px risca cada termo (0,3 s). Devolve os traços (saem no glyph map seguinte)."""
    gs = [m.p(k) for k in chaves]
    cena.play(*[g.animate.set_color(CORAL_C) for g in gs], run_time=rt)
    tr = []
    for g in gs:
        a, b = g.get_corner(DL), g.get_corner(UR)
        ln = Line(a + np.array([-.03, 0, 0]), b + np.array([.03, 0, 0])).set_stroke(CORAL_C, 2 / 1.2, 1)
        ln._sem_contorno = True
        tr.append(ln.set_z_index(27))
    cena.play(*[Create(t) for t in tr], run_time=rt)
    print(f"[cancela] {cena.lote} {cena._aid} {cena.t:.2f} {chaves}")
    return tr


def acende(cena, mobs, cor, rt=1.0):
    """R15: a peça acende na cor (0,25 s), fica `rt` e volta à cor original."""
    mobs = list(mobs)
    c0 = [[g.get_fill_color() if g.get_fill_opacity() > 0 else g.get_stroke_color() for g in m.family_members_with_points()] for m in mobs]
    cena.play(*[m.animate.set_color(cor) for m in mobs], run_time=0.25)
    cena.wait(max(0.1, rt - 0.5))
    an = []
    for m, cs in zip(mobs, c0):
        t = m.copy()
        for g, c in zip(t.family_members_with_points(), cs):
            g.set_color(c)
        an.append(Transform(m, t))
    cena.play(*an, run_time=0.25)


# ── auditoria R11: MathTex que entra na cena sem origem ──
_SEM = []


def _audita_origem(cena):
    for m in cena.mobjects:
        for x in m.get_family():
            if isinstance(x, MathTex) and not getattr(x, "_origem", None) and not getattr(x, "_aud", False):
                if any(g.get_fill_opacity() > 0.5 for g in x.family_members_with_points()):
                    x._aud = True
                    _SEM.append((cena.lote, cena._aid, cena.t, getattr(x, "_tex", "")))
                    print(f"[sem-origem] {cena.lote} {cena._aid} {cena.t:.2f} {getattr(x, '_tex', '')[:80]!r} {type(x).__name__} {getattr(x, 'tex_string', '')[:40]!r} {[round(v, 2) for v in x.get_center()[:2]]}")


_play_o = Base.play


def _play_aud(self, *a, **k):
    r = _play_o(self, *a, **k)
    _audita_origem(self)
    return r


Base.play = _play_aud

# legendas com pedaços em TeX e o contador não são linhas de conta
_lm0 = leg_mix


def leg_mix(*a, **k):  # noqa: F811
    g = _lm0(*a, **k)
    for x in g.get_family():
        if isinstance(x, MathTex):
            x._origem = "legenda"
    return g


_jp0 = junta_partes


def junta_partes(cena, m):  # noqa: F811
    _jp0(cena, m)
    if not getattr(m, "_origem", None):
        m._origem = "a"
    m._esc = True


_l30.junta_partes = junta_partes


def rot(tex, x, y, size=30, al="c"):
    """Rótulo matemático com placa (escrito pela caneta: chame escreve(cena, r.f) ou voa)."""
    f = TC(tex, x, y, size, al, caneta=True)
    g = VGroup(placa7(f), f)
    g.f = f
    return g


class Duas(VGroup):
    """Duas (ou mais) linhas vistas como uma só fonte de glyph map (fusão R13): [0] = todos os glifos; chaves e faixas concatenadas."""

    def __init__(self, *lins, prefixos=None):
        gl = VGroup(*[g for l in lins for g in l[0]])
        super().__init__(gl)
        self.lins = lins
        self.ks, self._rg, k0 = [], [], 0
        for n, l in enumerate(lins):
            pre = prefixos[n] if prefixos else ""
            self.ks += [pre + k for k in l.ks]
            self._rg += [[k0 + x for x in r] for r in l._rg]
            k0 += len(l[0])
        self._tex = " ‖ ".join(l._tex for l in lins)


def funde(cena, lins, B, rt=1.0, prefixos=None, voos=None, somem=(), ka=None):
    """Funde várias linhas numa só (B) por um glyph map único (chaves; use prefixos para distinguir as linhas)."""
    A = Duas(*lins, prefixos=prefixos)
    gm(cena, A, B, rt=rt, voos=voos, somem=somem, nota="(fusão)", ka=ka)
    cena.remove(*lins)
    limpa_soltos(cena)
    cena.add(B)
    return B


def recolor_lin(m, *chaves, cor):
    for g in m.p(*chaves):
        g.set_fill(cor).set_stroke(cor)


def num_den(m):
    r"""Glifos do numerador e do denominador de uma fração (\dfrac) dentro de m: (num, den), cada um da esquerda para a direita."""
    gs = list(m) if not isinstance(m, MathTex) else list(m[0])
    barra = max(gs, key=lambda g: g.width / max(g.height, 1e-3))
    yb = barra.get_center()[1]
    x0, x1 = barra.get_left()[0] - 1e-3, barra.get_right()[0] + 1e-3
    num = sorted([g for g in gs if g is not barra and g.get_center()[1] > yb and x0 <= g.get_center()[0] <= x1], key=lambda g: g.get_center()[0])
    den = sorted([g for g in gs if g is not barra and g.get_center()[1] < yb and x0 <= g.get_center()[0] <= x1 + .3], key=lambda g: g.get_center()[0])
    return num, den
_Duas = Duas


# ── R13 (handoff v2 §2): em cada gatilho, na coluna (x > 1090 px): linhas de conta visíveis, legendas SG Medium seguidas e linhas "=" órfãs ──
_leg0 = legenda


def legenda(*a, **k):  # noqa: F811
    m = _leg0(*a, **k)
    m._leg = True
    return m


def _lins_visiveis(cena, xmin=-99):
    na_cena = {id(g) for m in cena.mobjects for g in m.get_family()}
    out = []
    for x in _LINS:
        gs = [g for g in x[0]] if len(x) else []
        if gs and all(id(g) in na_cena for g in gs) and max(g.get_fill_opacity() for g in gs) >= 0.5 and x.get_center()[0] >= xmin:
            out.append(x)
    return out


import v30 as _v30q  # noqa: E402
_v30q.EXTRA_TEXTOS = lambda cena: _lins_visiveis(cena)


def _r13(cena, onde):
    xmin = PX(1090, 0)[0]
    itens = []
    for m in cena.mobjects:
        if m in cena.fixos() or isinstance(m, ValueTracker):
            continue
        cand = [m] if not isinstance(m, VGroup) or isinstance(m, MathTex) or getattr(m, "_leg", False) else [m] + list(m.submobjects)
        for x in cand:
            if not (isinstance(x, MathTex) or getattr(x, "_leg", False)):
                continue
            if getattr(x, "_origem", "") == "legenda" and not getattr(x, "_leg", False):
                continue
            gs = [g for g in x.family_members_with_points() if isinstance(g, VMobject)]
            if not gs or max(g.get_fill_opacity() for g in gs) < 0.5 or x.get_center()[0] < xmin:
                continue
            itens.append(x)
    # uma Lin cujo pai saiu da lista da cena (remove de um glifo reestrutura o grupo) continua na tela: conta pelos glifos visíveis
    itens += _lins_visiveis(cena, xmin)
    itens = list({id(x): x for x in itens}.values())
    itens.sort(key=lambda x: -x.get_center()[1])
    todas = [x for x in itens if isinstance(x, MathTex)]
    contas = [x for x in todas if not getattr(x, "_linha_de", None) and not getattr(x, "_moldura", False)]
    run, pior, ant = 0, 0, None       # legendas empilhadas: duas na mesma altura são uma linha; um vão > 60 px (gráfico, chapa) quebra a sequência
    for x in itens:
        if not getattr(x, "_leg", False):
            run, ant = 0, None
            continue
        if ant is not None and abs(x.get_center()[1] - ant.get_center()[1]) < .1:
            continue
        run = 1 if ant is not None and ant.get_bottom()[1] - x.get_top()[1] > .5 else run + 1
        ant = x
        pior = max(pior, run)
    orf = 0
    for x in contas:
        if isinstance(x, Lin) and x.ts and x.ts[0].startswith("="):
            topo = x.get_top()[1]
            if not any(o is not x and -0.1 <= o.get_bottom()[1] - topo < 1.2 and o.get_left()[0] <= x.get_left()[0] + .5 for o in todas):
                orf += 1
                print(f"[r13-orfa] {cena.lote} {onde} {x._tex[:60]!r} acima: {[o._tex[:40] for o in todas if o is not x]}")
    print(f"[r13] {cena.lote} {onde} contas={len(contas)} legendas_seguidas={pior} orfas={orf}")
    if len(contas) > 6 or pior > 2:
        print(f"[r13-itens] {cena.lote} {onde} " + " | ".join(("LEG " if getattr(x, "_leg", False) else "") + str(getattr(x, "_tex", getattr(x, "text", type(x).__name__)))[:35]
                                                              for x in itens))


_gat_r13 = Base.gat


def _gat_r(self, frase):
    _gat_r13(self, frase)
    if os.environ.get("QA_SOBREPOS") == "1":
        _r13(self, f"{self._aid} «{frase}»")


Base.gat = _gat_r
