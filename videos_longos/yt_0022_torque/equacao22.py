"""yt_0021 — auditoria EQUAÇÃO (P0): extrai do código das cenas as linhas de CONTA montadas por M()/eqf() (strings LaTeX), converte para Python e AVALIA cada
igualdade em que os dois lados são numéricos (unidades ignoradas). Falha se dois lados adjacentes diferirem mais que a precisão do arredondamento mostrado.
Ex.: `8·9,8/(13·0,30) = 4,48` falha; `√(8·9,8/(13·0,30)) = 4,48` passa.   uso: python equacao21.py → renders/equacao.txt"""
import ast
import math
import re
from pathlib import Path

U = Path(__file__).resolve().parent
ARQ = sorted(U.glob("sec_*.py"))


def tex_para_py(t):
    B = chr(92)
    t = re.sub(re.escape(B + " ") + "?" + re.escape(B + "mathrm") + r"\{[^{}]*\}", "", t)
    t = re.sub(re.escape(B + "mathrm") + r"\{[^{}]*\}", "", t)
    for a in (B + ",", B + " ", B + "!", B + "bigl", B + "Bigl", B + "bigr", B + "Bigr", B + "big", B + "Big", B + "left", B + "right", B + "quad"):
        t = t.replace(a, " ")
    t = t.replace("{,}", ".").replace(B + "cdot", "*").replace(B + "times", "*").replace(B + "div", "/").replace("−", "-")
    for _ in range(6):
        t = re.sub(re.escape(B) + r"t?frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", t)
        t = re.sub(re.escape(B + "sqrt") + r"\{([^{}]*)\}", r"sqrt(\1)", t)
    t = re.sub(r"\^\{?(\d+)\}?", r"**\1", t)
    return t.strip()


def avalia(s):
    B = chr(92)
    if re.search("[A-Za-z" + re.escape(B) + "]", re.sub("sqrt", "", s)):
        return None
    s = re.sub(r"(\d)\s*\(", r"\1*(", s)
    s = re.sub(r"\)\s*\(", r")*(", s)
    s = re.sub(r"(\d)\s+(\d)", r"\1*\2", s)
    try:
        return float(eval(s, {"sqrt": math.sqrt, "__builtins__": {}}))
    except Exception:
        return None


def linhas(tree):
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(getattr(n, "func", None), ast.Name) and n.func.id in ("M", "eqf"):
            try:
                if n.func.id == "M":
                    partes = [ast.literal_eval(a) for a in n.args]
                    yield n.lineno, " ".join(partes)
                else:
                    pre, num, den = (ast.literal_eval(a) for a in n.args[:3])
                    post = []
                    for k in n.keywords:
                        if k.arg == "post":
                            post = ast.literal_eval(k.value)
                    yield n.lineno, " ".join(pre) + r" \frac{" + " ".join(num) + "}{" + " ".join(den) + "} " + " ".join(post)
            except Exception:
                continue


out, n_ok, n_f, n_lin = [], 0, 0, 0
for f in ARQ:
    try:
        tree = ast.parse(f.read_text(encoding="utf-8"))
    except SyntaxError:
        continue
    for lin, tex in linhas(tree):
        if "=" not in tex:
            continue
        n_lin += 1
        lados = [tex_para_py(x) for x in tex.split("=")]
        vals = [avalia(x) for x in lados]
        for a, b, sa, sb in zip(vals, vals[1:], lados, lados[1:]):
            if a is None or b is None:
                continue
            tol = max(0.007 * abs(b), 0.006)
            ok = abs(a - b) <= tol or abs(round(a, 2) - b) <= 0.006 or abs(round(a, 3) - b) <= 0.0006
            n_ok += ok
            n_f += not ok
            out.append(f"  [{'OK ' if ok else 'FALHA'}] {f.name}:{lin}  {sa.strip()} = {a:.5g}  ×  {sb.strip()} = {b:.5g}")
resumo = f"EQUAÇÃO: {n_lin} linhas com '='; {n_ok + n_f} igualdades numéricas avaliadas: {n_ok} OK, {n_f} FALHA\n"
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "equacao.txt").write_text(resumo + "\n".join(out) + "\n", encoding="utf-8")
print(resumo + "\n".join(x for x in out if "FALHA" in x))
