"""Kit visual do yt_0012 (cópia local do kit do yt_0006; cores por token adaptadas à indutância).

Paleta e gramática do yt_0005; MF-Tools (TransformByGlyphMap) para mostrar de onde vem cada termo.

Equação = MathTex de string única, com substrings isoladas ("tokens"). Cada token sabe quais glifos ocupa:
    m.tok = {"I": [[5], [17]], ...}   (ocorrências, em ordem; índices em m[0].submobjects)
Isso permite:
  gmap(A, B, ("I","I"), ...)  → TransformByGlyphMap com mapa por termo (e auto-pareamento do restante)
  src={("I",0): rótulo_do_diagrama} → o termo VOA de uma cópia do rótulo no diagrama até a equação.
"""
import re
from functools import lru_cache

import numpy as np
from manim import (
    AnimationGroup, Arrow, Circle, FadeIn, FadeOut, Line, MathTex, Polygon, RoundedRectangle, SurroundingRectangle,
    VGroup, VMobject, RIGHT, LEFT, UP, DOWN, smooth,
)
from MF_Tools import TransformByGlyphMap

from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR
from template.fonts import screen_text

# ── paleta (idêntica ao yt_0005) ────────────────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR        # E / grandezas auxiliares (α, γ)
MAG = "#EA63FF"             # campo magnético B
BLUE = "#267BFF"
BLUE_L = "#7FB2FF"          # painéis, carga/densidade, construção auxiliar (NÃO é matéria condutora)
STEEL = "#7A8696"           # matéria condutora: fio, espira, lâmina, tubo
VIOLET = "#9C8CFF"          # geometria da separação (R, r, s, a, x, z)
FC = "#5AA2FF"              # força magnética
GREEN = "#3FE08B"           # CORRENTE (I, K, J, dℓ)
PANEL = "#0E2A52"
DIM = "#8FA3C4"

T_BODY, T_NOTE, T_CAP, T_HEAD = 30, 26, 28, 36
M_XL, M_L, M_M, M_S = 54, 48, 40, 32

HEAT = "#FF7A3D"            # calor / Joule / R (único tom quente, como no yt_0010)

# cor por token (texto TeX isolado) — semântica do yt_0012, conforme docs/padrao_video_longo.md
GEO = "#B8C4DA"             # geometria (comprimentos, áreas, volumes, dτ): cinza-claro; violeta só para tempo/velocidade
TOKCOL = {}
for _t in (r"\mathbf B", "B", "B^2", "B(t)", "B_1", r"\mathbf B_1", r"\Lambda", r"\Lambda_1", r"\Lambda_2", r"\Phi", "U_B", "U_B(t)",
           "U_{B,0}", "u_B", "dU_B", r"\frac{dU_B}{dt}", r"\frac{dB}{dt}", r"\mathbf B\cdot d\boldsymbol\ell", r"\frac{B^2}{2\mu_0}"):
    TOKCOL[_t] = MAG
for _t in ("I", "I_0", "I_1", "I_2", r"I_\infty", "I(t)", "I(0)", "I^2", "I_0^2", "dI", r"\frac{dI}{dt}", r"\frac{dI_1}{dt}",
           r"\frac{dI_2}{dt}", r"I_{\rm enc}", "I_1(t)", "I_2(t)"):
    TOKCOL[_t] = GREEN
for _t in (r"\mathcal E_0", r"\mathcal E_L", r"\mathcal E_1", r"\mathcal E_2", r"E_\phi", r"E_{\rm ind}", r"\mathcal E",
           r"P_{\rm fonte}"):
    TOKCOL[_t] = CYAN
for _t in ("P_R", "P_R(t)", r"P_{\rm Joule}", r"E_{\rm calor}", "Q_R", "Q_R(t)"):
    TOKCOL[_t] = HEAT
for _t in ("A", r"\ell", r"A\ell", "V", "n", "n^2", "N_2", "r", "a", "a^2", r"d\tau"):
    TOKCOL[_t] = GEO
for _t in (r"\tau", "dt", r"\frac{t}{\tau}", r"-t/\tau", r"-2t/\tau", r"\frac{\tau}{2}"):
    TOKCOL[_t] = VIOLET
for _t in ("R", "L", "M", "M_{12}", "M_{21}"):
    TOKCOL[_t] = WHITE


def txt(s, size=T_BODY, color=WHITE, opacity=1.0):
    """Texto de tela: Space Grotesk em MAIÚSCULAS (docs/padrao_video_longo.md)."""
    s = s.upper()
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(opacity)


def defn(tex, *tok, size=30, colors=None):
    """Definição de variável em MathTex (símbolo na cor da grandeza, texto em minúsculas e DIM)."""
    m = E(tex, *tok, size=size, colors=colors)
    keep = {i for occs in m.tok.values() for o in occs for i in o}
    for i, g in enumerate(m[0]):
        if i not in keep:
            g.set_color(DIM)
    return m


# ── equações com tokens ─────────────────────────────────────────────────────────────────────────────────────
def _build(tex, iso, size, colors, width):
    iso = tuple(sorted(dict.fromkeys(iso), key=len, reverse=True))   # yt_0012: o mais longo primeiro (dI antes de I)
    m = MathTex(tex, font_size=size, color=WHITE, substrings_to_isolate=list(iso)) if iso else MathTex(tex, font_size=size, color=WHITE)
    leaves = list(m[0].submobjects)
    pos = {id(g): i for i, g in enumerate(leaves)}
    tok = {}
    for t, sid in getattr(m, "matched_strings_and_ids", []):
        if not sid.endswith("substring") or t not in iso:
            continue
        idx = sorted(pos[id(g)] for g in m.id_to_vgroup_dict[sid].family_members_with_points() if id(g) in pos)
        if idx:
            tok.setdefault(t, []).append(idx)
    cmap = {**TOKCOL, **(colors or {})}
    for t, occs in tok.items():
        c = cmap.get(t)
        if c:
            for idx in occs:
                for i in idx:
                    leaves[i].set_color(c)
    if width and m.width > width:
        m.scale_to_fit_width(width)
    m.tok = tok
    m.tex = tex
    return m


_EC = {}


def E(tex, *iso, size=M_M, colors=None, width=None):
    key = (tex, iso, size, tuple(sorted((colors or {}).items())), width)
    if key not in _EC:
        _EC[key] = _build(tex, iso, size, colors, width)
    c = _EC[key].copy()
    c.tok, c.tex = _EC[key].tok, tex
    return c


def glyphs(m, tok, occ=None):
    """VGroup com os glifos do token (todas as ocorrências ou só a occ-ésima)."""
    lst = m.tok[tok]
    sel = lst if occ is None else [lst[occ]]
    return VGroup(*[m[0][i] for idx in sel for i in idx])


def _occ(m, tok, o):
    if tok not in m.tok:
        raise KeyError(f"token {tok!r} ausente em {m.tex!r} (tem {list(m.tok)})")
    lst = m.tok[tok]
    return lst if o is None else [lst[o]]


def _sig(g):
    w, h = g.width, g.height
    if h < 0.045 and w > 0.12:
        return ("bar",)
    return (len(g.points), round(w / max(h, 1e-3), 1))


def gmap(A, B, *pairs, auto=True, structure=True, reserved=(), **kw):
    """TransformByGlyphMap A→B.

    pairs: (tokA, tokB[, occA[, occB]]) transporta; (tokA, None[, occ]) remove; (None, tokB[, occ]) introduz.
    auto: pares restantes — tokens iguais em ordem; depois glifos de estrutura (=, +, barras) por assinatura.
    O que sobrar em A sai (FadeOut) e o que sobrar em B entra (FadeIn)."""
    entries, ua, ub = [], set(), set(reserved)
    explicit_dst = set(reserved)
    for p in pairs:
        ta, tb = p[0], p[1]
        oa = p[2] if len(p) > 2 else None
        ob = p[3] if len(p) > 3 else None
        if ta is None:
            for lst in _occ(B, tb, ob):
                entries.append(([], list(lst)))
                ub.update(lst)
            continue
        if tb is None:
            for lst in _occ(A, ta, oa):
                entries.append((list(lst), []))
                ua.update(lst)
            continue
        if isinstance(ta, list):
            # fusão: vários termos de A [(tok, occ), ...] viram UM termo de B (R·R² → R³, R·R → R²)
            src_idx = [i for (t, o) in ta for lst in _occ(A, t, o) for i in lst]
            dst = [i for lst in _occ(B, tb, ob) for i in lst]
            if set(dst) & explicit_dst:
                raise ValueError(f"destino duplicado em gmap: {ta!r}->{tb!r}")
            explicit_dst.update(dst)
            entries.append((src_idx, dst))
            ua.update(src_idx)
            ub.update(dst)
            continue
        la, lb = _occ(A, ta, oa), _occ(B, tb, ob)
        if len(la) != len(lb):
            raise ValueError(f"par ({ta!r},{tb!r}): {len(la)} ocorrência(s) em A e {len(lb)} em B — use occA/occB")
        for a, b in zip(la, lb):
            if set(b) & explicit_dst:
                raise ValueError(f"destino duplicado em gmap: {ta!r}->{tb!r} (glifos {sorted(set(b) & explicit_dst)}); use um estado intermediário")
            explicit_dst.update(b)
            entries.append((list(a), list(b)))
            ua.update(a)
            ub.update(b)
    if auto:
        for t, occs in A.tok.items():
            if t in B.tok:
                fa = [o for o in occs if not (set(o) & ua)]
                fb = [o for o in B.tok[t] if not (set(o) & ub)]
                for a, b in zip(fa, fb):
                    entries.append((list(a), list(b)))
                    ua.update(a)
                    ub.update(b)
        if structure:
            tokA = {i for occs in A.tok.values() for o in occs for i in o}
            tokB = {i for occs in B.tok.values() for o in occs for i in o}
            ra = [i for i in range(len(A[0])) if i not in ua and i not in tokA]
            rb = [j for j in range(len(B[0])) if j not in ub and j not in tokB]
            for i in ra:
                si = _sig(A[0][i])
                for j in rb:
                    if _sig(B[0][j]) == si:
                        entries.append(([i], [j]))
                        ua.add(i)
                        ub.add(j)
                        rb.remove(j)
                        break
    if not entries:
        # sem nenhum termo em comum: o MF-Tools mostraria índices de depuração; fazemos troca simples
        print(f"[gmap] sem termos em comum: {A.tex!r} -> {B.tex!r}", flush=True)
        return AnimationGroup(FadeOut(A), FadeIn(B))
    kw.setdefault("run_time", 1.6)
    # yt_0012: o que sai termina na 1ª metade e o que entra só começa na 2ª (nada coexiste no mesmo lugar)
    kw.setdefault("default_remover_kwargs", {"rate_func": lambda t: smooth(min(1.0, 2 * t))})
    kw.setdefault("default_introducer_kwargs", {"rate_func": lambda t: smooth(max(0.0, 2 * t - 1))})
    return TransformByGlyphMap(A, B, *entries, auto_fade=True, **kw)


# ── elementos de desenho ────────────────────────────────────────────────────────────────────────────────────
def halo(m, w=7):
    return m.set_stroke(BACKGROUND_COLOR, width=w, background=True)


def arrow(a, b, color=WHITE, width=5, z=4, tip=0.26):
    if np.linalg.norm(np.asarray(b, dtype=float) - np.asarray(a, dtype=float)) < 1e-5:
        return VMobject()
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.35,
                 max_stroke_width_to_length_ratio=50).set_z_index(z)


def panel(w, h, center, op=0.55, color=PANEL, stroke=BLUE_L, z=-1):
    r = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_width=1.5)
    r.set_fill(color, op).set_stroke(stroke, 1.5, 0.55).move_to(center).set_z_index(z)
    return r


def box(m, color=WHITE, buff=0.16, width=3):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=width, corner_radius=0.1)


def rich(s, size=T_CAP, color=WHITE):
    """Texto com matemática embutida entre $...$ (gregos/símbolos saem em MathTex)."""
    parts = s.split("$")
    items = []
    for i, p in enumerate(parts):
        p = p.strip() if i % 2 == 0 else p
        if not p:
            continue
        if i % 2:
            items.append(("m", MathTex(p, font_size=size * 1.18, color=color)))
        else:
            items.append(("t", txt(p, size, color)))
    g = VGroup()
    prev = None
    for kind, m in items:
        if prev is not None:
            punct = kind == "t" and getattr(m, "text", "")[:1] in ",.;:)"
            m.next_to(prev, RIGHT, buff=0.04 if punct else 0.16)
        g.add(m)
        prev = m
    return g
