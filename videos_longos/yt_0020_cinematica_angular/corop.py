"""yt_0020 v3 — auditorias que só o objeto em memória conhece: COR OPERADOR (§2), CAIXA VAZIA por qualquer caminho (§6) e frase-chave (§6).
Passada a seco (como auditar.sh), com um gancho em kit.Base._auditar; NÃO grava qa_overlay, qa_ref nem log_aud (pode rodar junto de outros agentes).
uso: uv run --no-sync python corop.py LOTE [MEDIA_DIR]  → cor_operador_<LOTE>.json   (qa20.py v3 lê esses arquivos; sem eles, as seções saem NÃO MEDIDO)
Cor dos glifos (por forma, referência normalizada pela altura): d, t, =, + , −, ( ), ∫, l i m (lim), barra de fração → branco; Δ → cor do glifo seguinte;
θ φ λ s → âmbar; ω v → violeta; α a → verde; r → GEO. Só conta violação que dura ≥ 3 passadas (0,6 s): voo de glyph map interpola cor."""
import json
import os
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
LOTE = sys.argv[1] if len(sys.argv) > 1 else "TESTE"
os.environ.update(AUDITORIA="1", SO_AUDITORIA="1", MEDIA_DIR=str(Path(sys.argv[2]) if len(sys.argv) > 2 else U / f"media_cop_{LOTE}"), PYTHONIOENCODING="utf-8")
sys.path.insert(0, str(U))
os.chdir(U)

import numpy as np  # noqa: E402
from manim import MathTex, Text, ManimColor  # noqa: E402

import kit  # noqa: E402
import prob  # noqa: E402

HEX = lambda c: ManimColor(c).to_hex().upper()
BR, ANG, VEL, ACC, GEO = (kit.WHITE_, kit.ANG, kit.VEL, kit.ACC, kit.GEO)
TOL = 30                                                   # L∞ em 0–255
REFS = {}                                                  # n pontos → [(forma normalizada, rótulo, cor esperada ou None)]


def _rgb(c):
    return np.array(ManimColor(c).to_rgb()) * 255


def _norm(g):
    p = g.points - g.get_center()
    return p / max(g.height, 1e-6)


def _refs():
    """Glifos de referência (estilo normal e de índice/expoente)."""
    def add(tex, idx, rot, cor):
        for src, k in ((tex, 0), ("x^{" + tex + "}", -1)):
            gl = list(MathTex(src).family_members_with_points())[k]
            REFS.setdefault(len(gl.points), []).append((_norm(gl), rot, cor))
    for tex, rot, cor in (("d", "d", BR), ("t", "t", BR), ("=", "=", BR), ("+", "+", BR), ("-", "−", BR), ("(", "(", BR), (")", ")", BR),
                          (r"\int", "∫", BR), (r"\theta", "θ", ANG), (r"\phi", "φ", ANG), (r"\varphi", "φ", ANG), (r"\lambda", "λ", ANG), ("s", "s", ANG),
                          (r"\omega", "ω", VEL), ("v", "v", VEL), (r"\alpha", "α", ACC), ("a", "a", ACC), ("r", "r", GEO)):
        add(tex, 0, rot, cor)
    m = MathTex(r"\int_a^b")                               # ∫ no estilo de texto (limites) e display
    REFS.setdefault(len(m[0][0].points), []).append((_norm(m[0][0]), "∫", BR))
    m = MathTex(r"\displaystyle\int_a^b")
    REFS.setdefault(len(m[0][0].points), []).append((_norm(m[0][0]), "∫", BR))
    for k, ch in enumerate("lim"):                         # lim romano (l, i, m romanos; o m itálico da massa é outra forma)
        g = MathTex(r"\lim")[0][k]
        REFS.setdefault(len(g.points), []).append((_norm(g), "lim", BR))
    g = MathTex(r"\Delta")[0][0]
    REFS.setdefault(len(g.points), []).append((_norm(g), "Δ", "DELTA"))


def _classe(g):
    if g.width > 3.0 * max(g.height, 1e-6):
        return "barra", BR
    for pn, rot, cor in REFS.get(len(g.points), ()):
        if np.abs(_norm(g) - pn).max() < 0.03:
            return rot, cor
    return None, None


def _leaf_op(g):
    try:
        return max(g.get_fill_opacity(), g.get_stroke_opacity())
    except Exception:
        return 1.0


def _gcor(g):
    return g.get_fill_color() if g.get_fill_opacity() > 0.05 else g.get_stroke_color()


ST = {"classe": {}, "viol": {}, "n_tex": 0, "n_gl": 0, "omega": {}, "caixa": {}, "frase": {}, "refs_ok": False}


def gancho(self, dentro=False):
    t = round(float(self.clk.get_value()), 3)
    if not ST["refs_ok"]:
        _refs()
        ST["refs_ok"] = True
    vis = []

    def anda(m):
        vis.append(m)
        for s in m.submobjects:
            anda(s)
    fixos = self.fixos()
    for top in self.mobjects:
        if top not in fixos:
            anda(top)
    # COR OPERADOR ------------------------------------------------------------------------------------------------------------------
    for m in vis:
        if isinstance(m, Text):
            tx = getattr(m, "text", "")
            if "?" in tx and max((_leaf_op(x) for x in m.family_members_with_points()), default=0) > 0.3:
                fs = float(getattr(m, "font_size", 0) or 0)
                f_ = ST["frase"].setdefault(tx[:80], [fs, fs, t, t])
                f_[0], f_[1], f_[3] = min(f_[0], fs), max(f_[1], fs), t
        if not isinstance(m, MathTex):
            continue
        gl = [x for x in m.family_members_with_points()]
        if not gl or max(_leaf_op(x) for x in gl) <= 0.3:
            continue
        k = id(m)
        c = ST["classe"].get(k)
        if c is None or c[0] != len(gl):
            c = ST["classe"][k] = (len(gl), m.get_tex_string()[:70], [_classe(g) for g in gl])
            ST["n_tex"] += 1
            ST["n_gl"] += sum(1 for r_, _ in c[2] if r_)
        _, tex, cls = c
        _full = m.get_tex_string()
        _hs = sorted(g_.height for g_, c_ in zip(gl, cls) if c_[0] != "barra")
        _med = _hs[len(_hs) // 2] if _hs else 0.0
        _cy = float(np.median([g_.get_center()[1] for g_, c_ in zip(gl, cls) if c_[0] != "barra"] or [0.0]))
        for j, g in enumerate(gl):
            rot, cor = cls[j]
            if rot is None:
                continue
            if rot == "lim" and r"\lim" not in _full:          # v4 §3: o m de uma unidade (\mathrm{m}) não é "lim"
                continue
            if j > 0 and rot in ("d", "t", "r", "v", "a", "s", "θ") and gl[j - 1] is not g and g.get_center()[1] < gl[j - 1].get_center()[1] - 0.03 and g.height <= 1.02 * gl[j - 1].height                     and 0 < g.get_center()[0] - gl[j - 1].get_center()[0] < 0.6:          # v8: subscrito (t de a_t, v_t; d de v_borda, ω_méd...): herda a cor da grandeza, não é operador
                continue
            if rot in ("d", "t", "r", "v", "a", "ω", "α", "s", "θ") and (g.height < 0.85 * _med or g.get_center()[1] < _cy - 0.18 * _med) and rot != "ω":   # v4 §3: subscrito/expoente herda a cor da grandeza (não é violação)
                continue
            if cor == "DELTA":                                 # Δ leva a cor do glifo seguinte na mesma linha (Δθ âmbar, Δt branco)
                ck = g.get_center()
                viz = [(gl[q].get_center()[0] - ck[0], cls[q][1]) for q in range(len(gl)) if cls[q][0] not in (None, "Δ")
                       and abs(gl[q].get_center()[1] - ck[1]) < 0.15 and 0 < gl[q].get_center()[0] - ck[0] < 0.8]
                if not viz:
                    continue
                prox = min([(gl[q].get_center()[0] - ck[0], cls[q][0]) for q in range(len(gl)) if abs(gl[q].get_center()[1] - ck[1]) < 0.15 and 0 < gl[q].get_center()[0] - ck[0] < 0.8], default=None)
                if prox is not None and prox[1] is None:          # v8: Δ colado a uma grandeza não classificada (Δx, Δy): sem regra de cor
                    continue
                cor = min(viz, key=lambda p: p[0])[1]
            if rot == "ω":
                ST["omega"].setdefault(HEX(_gcor(g)), [0, 1e9, 0])
                o_ = ST["omega"][HEX(_gcor(g))]
                o_[0] += 1
                o_[1], o_[2] = min(o_[1], g.height), max(o_[2], g.height)
            got = _rgb(_gcor(g))
            if np.abs(got - _rgb(cor)).max() > TOL:
                v = ST["viol"].setdefault((k, j), {"tex": tex, "glifo": rot, "cor": HEX(_gcor(g)), "esp": HEX(cor), "n": 0, "t0": t, "t1": t,
                                                  "dono": next((type(tp).__name__ + f"[{len(tp.submobjects)}]" for tp in self.mobjects if m in tp.get_family()), "?"), "x": round(float(g.get_x()), 1), "y": round(float(g.get_y()), 1)})
                v["n"] += 1
                v["t1"] = t
    # CAIXA VAZIA (qualquer caminho: escreve, passo, pg, FadeIn) ------------------------------------------------------------------
    caixas = [m for m in vis if getattr(m, "_caixa", False) and m.points.size and _leaf_op(m) > 0.3]
    if caixas:
        folhas = [x for x in vis if x.points.size and not getattr(x, "_fundo", False) and not getattr(x, "_caixa", False) and _leaf_op(x) > 0.3]
        for cx in caixas:
            x0, y0, _ = cx.get_corner([-1, -1, 0])
            x1, y1, _ = cx.get_corner([1, 1, 0])
            tem = any(x0 - 0.05 <= f.get_center()[0] <= x1 + 0.05 and y0 - 0.05 <= f.get_center()[1] <= y1 + 0.05 for f in folhas)
            e = ST["caixa"].setdefault(id(cx), {"n": 0, "t0": t, "t1": t, "pos": [round(float(cx.get_x()), 1), round(float(cx.get_y()), 1)], "ult": None})
            if tem:
                e["n"], e["ult"] = 0, None
            else:
                if e["n"] == 0:
                    e["t0"] = t
                e["n"] += 1
                e["t1"] = t
                e["max"] = max(e.get("max", 0), e["n"])
                e["t1m"] = t if e["n"] == e["max"] else e.get("t1m", t)


def fim(self):
    _orig_rel(self)
    def _pulso(x):                                          # v8: cor esperada clareada (destaque do foco) por até 1,2 s não é violação
        got, esp = _rgb(x["cor"]), _rgb(x["esp"])
        return (got >= esp - 6).all() and (x["t1"] - x["t0"]) <= 1.2
    v = [dict(x, k=f"{j}") for (k, j), x in ST["viol"].items() if x["n"] >= 3 and not _pulso(x)]
    cx = [dict(x, dur=round(x["max"] * 0.2, 2)) for x in ST["caixa"].values() if x.get("max", 0) >= 3]
    res = {"lote": LOTE, "n_tex": ST["n_tex"], "n_glifos": ST["n_gl"], "violacoes": sorted(v, key=lambda d: d["t0"]),
           "curtas": sum(1 for x in ST["viol"].values() if x["n"] < 3), "omega": ST["omega"],
           "caixas_vazias": sorted(cx, key=lambda d: d["t0"]), "frases": ST["frase"]}
    (U / f"cor_operador_{LOTE}.json").write_text(json.dumps(res, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"[corop] {LOTE}: {ST['n_tex']} MathTex, {ST['n_gl']} glifos classificados, {len(v)} violações persistentes, {len(cx)} caixas vazias")


_orig_aud = kit.Base._auditar
_orig_rel = kit.Base.relatorio


def _aud(self, dentro=False):
    _orig_aud(self, dentro)
    gancho(self, dentro)


kit.Base._auditar = _aud
kit.Base.relatorio = fim
prob.Prob.gravar_reg = lambda self: None                   # não sobrescreve qa_overlay_<LOTE>.json dos outros agentes

if __name__ == "__main__":
    sys.argv = ["manim", "-r", "960,540", "--fps", "15", "--progress_bar", "none", "--disable_caching", "--dry_run", "cena.py", LOTE]
    from manim.__main__ import main  # noqa: E402

    main()
