"""Kit visual do yt_0006 (Biot–Savart).

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
    VGroup, VMobject, RIGHT, LEFT, UP, DOWN,
)
from MF_Tools import TransformByGlyphMap

from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR
from template.fonts import screen_text

# ── paleta (idêntica ao yt_0005) ────────────────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR        # E / grandezas auxiliares (α, γ)
MAG = "#EA63FF"             # campo magnético B
BLUE = "#267BFF"
BLUE_L = "#7FB2FF"          # fios, carga/densidade
STEEL = "#7A8696"            # fio / matéria (cinza-aço): neutro, para a corrente verde destacar
VIOLET = "#9C8CFF"          # geometria da separação (R, r, s, a, x, z)
FC = "#5AA2FF"              # força magnética
GREEN = "#3FE08B"           # CORRENTE (I, K, J, dℓ)
PANEL = "#0E2A52"
DIM = "#8FA3C4"

T_BODY, T_NOTE, T_CAP, T_HEAD = 30, 26, 28, 36
M_XL, M_L, M_M, M_S = 54, 48, 40, 32

# cor por token (texto TeX isolado)
TOKCOL = {}
for _t in (r"\mathbf B", r"d\mathbf B", "dB", "B", "B_z", "dB_z", "B_N", r"\mathbf B_N", "B_1", r"\mathbf B_1", r"B_\infty",
           "B(0)", r"B_{\rm trecho}", r"B_{\rm total}", r"B_{\rm restante}", r"d\mathbf B_\perp", r"\Delta\mathbf B_i",
           r"\Delta\mathbf B", r"d\mathbf B_\perp(\phi)", r"d\mathbf B_\perp(\phi+\pi)", r"\mathbf B_z", "dB_z+dB_z", "B_z(z)",
           r"\mathbf B_{\rm tot}", r"B_{\max}", r"dB_{\max}", r"\Delta\mathbf B_1", r"\Delta\mathbf B_2", r"\Delta\mathbf B_5"):
    TOKCOL[_t] = MAG
for _t in ("I", "I_1", "I_2", r"I_{\rm entra}", r"I_{\rm sai}", "K", "J", r"\mathbf K", r"\mathbf J", r"d\boldsymbol\ell", r"d\ell",
           r"\boldsymbol\ell", r"\ell", "dx", r"dx\,\hat x", r"\hat x", r"d\ell\,dw", "dw", r"dA_\perp", r"\mathbf L", "L", r"\nabla\cdot\mathbf J"):
    TOKCOL[_t] = GREEN
for _t in (r"\mathbf R", r"\hat{\mathbf R}", r"\mathbf r", r"\mathbf r'", r"\mathbf r\prime", "R", "R^2", "R^3", "s", "s^2", "s^3",
           "a", "x", "z", "x^2", "a^2", "|z|", "z^2", r"\hat y", r"\hat z", "d", r"R^2+z^2", "x^2+a^2", r"(R^2+z^2)^{3/2}",
           r"(x^2+a^2)^{3/2}", r"|\mathbf R|", r"\mathbf R=", "R^2s", "s^2s", "r"):
    TOKCOL[_t] = VIOLET
for _t in (r"\mathbf F", r"\mathbf F_2", "F_2", "F"):
    TOKCOL[_t] = FC
for _t in (r"\rho", "Q", r"\frac{dQ}{dt}", r"\frac{\partial\rho}{\partial t}"):
    TOKCOL[_t] = BLUE_L
for _t in (r"\alpha", r"\alpha_1", r"\alpha_2", r"\alpha_A", r"\alpha_B", r"\gamma", r"\tan\alpha", r"\sec\alpha", r"\sec^2\alpha", r"\cos\alpha",
           r"d\alpha", r"\sin\alpha_1", r"\sin\alpha_2", r"\sin\alpha", r"\cos\gamma", r"\sin\gamma"):
    TOKCOL[_t] = CYAN


TOKCOL.update({r"\mathbf B_{\rm total}": MAG, r"\mathbf B_{\rm trecho}": MAG, r"\mathbf B_{\rm restante}": MAG, r"\mathbf 0": VIOLET, "dI": GREEN, r"\hat{\mathbf t}": GREEN, "dw": VIOLET, "da": VIOLET, r"d\tau": VIOLET, r"dA_\perp": VIOLET, r"-x\,\hat x": VIOLET, r"a\,\hat y": CYAN, r"a\,dx": GREEN, r"dx\,\hat x": GREEN, r"a\tan\alpha": CYAN,
               r"a\sec^2\alpha\,d\alpha": CYAN, r"a^3\sec^3\alpha": CYAN, r"a^2\sec^2\alpha": CYAN, r"(x^2+a^2)^{3/2}": VIOLET,
               "x_A": VIOLET, "x_B": VIOLET, r"\hat z": MAG})

# ── 5.3: ajustes de gramática desta unidade ────────────────────────────────────────────────────────────────
# F = R/R³ é geometria da separação (violeta), não força; dℓ é o elemento do CAMINHO (branco), não corrente.
# Famílias das derivações (N06–N10): observador r, ∇ → ciano (OBS); fonte r', ∇', J(r'), dτ' → verde (SRC).
TOKCOL.update({r"\mathbf F": VIOLET, r"d\boldsymbol\ell": WHITE, r"d\ell": WHITE, r"\mathbf 0": WHITE,
               r"\mathbf r": CYAN, r"(\mathbf r)": CYAN, r"\mathbf r'": GREEN, r"(\mathbf r')": GREEN, r"\nabla'": GREEN,
               r"d\tau'": GREEN, r"\mathbf J(\mathbf r')": GREEN, r"\mathbf J(\mathbf r)": GREEN, r"I_{\rm enc}": GREEN,
               "nLI": GREEN, "NI": GREEN, "KL": GREEN,
               r"B_\phi": MAG, r"B(s)": MAG, r"B(a)": MAG, r"B(b)": MAG, r"\mathbf E": CYAN,
               r"\nabla\times\mathbf B": MAG, r"\nabla\cdot\mathbf B": MAG, r"(\nabla\times\mathbf B)_z": MAG,
               r"\delta^3(\mathbf r-\mathbf r')": VIOLET, r"\frac{\mathbf R}{R^3}": VIOLET, r"\frac{1}{R}": VIOLET,
               r"C_{\rm ext}": WHITE, r"\hat{\boldsymbol\phi}": MAG, r"\hat{\mathbf n}": WHITE, r"d\mathbf a": WHITE})
# Padrão do capítulo 5 (5.1/5.2/5.3): matéria = aço, corrente = verde, CAMINHO = branco, B = magenta, interface = azul.
# Elementos de caminho (dℓ, L, dx, x̂, t̂) são GEOMETRIA: brancos, nunca verdes por vizinhança com a corrente.
for _t in (r"d\boldsymbol\ell", r"d\ell", r"\boldsymbol\ell", r"\ell", "dx", r"dx\,\hat x", r"\hat x", r"\hat{\mathbf x}", r"\mathbf L", "L", r"\,L",
           r"\hat{\mathbf t}"):
    TOKCOL[_t] = WHITE
TOKCOL["K"] = GREEN
OBS = {r"\nabla": CYAN, r"\nabla\cdot": CYAN, r"\nabla\times": CYAN, r"(\mathbf r)": CYAN, r"\mathbf r": CYAN}
SRC = {r"\nabla'": GREEN, r"\nabla'\cdot": GREEN, r"(\mathbf r')": GREEN, r"\mathbf r'": GREEN, r"\mathbf J": GREEN, r"d\tau'": GREEN}
FAM = {**OBS, **SRC}


def txt(s, size=T_BODY, color=WHITE, opacity=1.0):
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(opacity)


# ── equações com tokens ─────────────────────────────────────────────────────────────────────────────────────
def _build(tex, iso, size, colors, width):
    iso = tuple(dict.fromkeys(iso))
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
        else:
            # termo composto sem cor própria: pinta por dentro (J verde, F violeta, ∇ ciano...) e continua sendo UM token.
            # Só subtokens com comando/símbolo (nunca letras soltas, que podem estar dentro de \frac, \cdot...).
            fine = sorted({k for k in cmap if k != t and k in t and ((len(k) > 1 and not k.isalpha()) or k in ("I", "J", "K"))},
                          key=len, reverse=True)
            if fine:
                sub = _build(t, tuple(fine), size, colors, None)
                if all(len(sub[0]) == len(idx) for idx in occs):
                    for idx in occs:
                        for i, g in zip(idx, sub[0]):
                            leaves[i].set_color(g.get_color())
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
