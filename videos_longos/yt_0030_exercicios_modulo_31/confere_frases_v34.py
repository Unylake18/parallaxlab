"""yt_0030 · conferência da sincronia v3.4 (HANDOFF v4 §3.2 e §6.1). Rodar na unidade:
    uv run --no-sync python confere_frases_v34.py           # depois de instalar narracao.md v3.4 (antes de mexer na cena)
    uv run --no-sync python confere_frases_v34.py --cena    # depois de implementar as C1–C21: confere também o CÓDIGO
Mesma tokenização da cena (kit._k_frase: \\w+ em minúsculas, COM acento; a cena pega a 1ª ocorrência da frase na âncora).
(1) frases_sincronia_v34.json: toda frase existe na sua âncora; os gatilhos (gat, gat_novo) estão em ordem crescente.
(2) --cena: lê os sec_*.py (ast), pega self.gat("…"), os gat de laço/tabela, le(…, fala) e ate=…, e confere o mesmo contra a fala.
Esperado: 69 âncoras · 6956 palavras · (1) 0 faltando, 0 fora de ordem · (2) 0 faltando, 0 fora de ordem, 0 [gatilho-sem-frase]."""
import ast
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from tempos import ANC_DADOS as D  # noqa: E402

tok = lambda s: re.findall(r"\w+", s.lower())
first = lambda f, al: next((i for i in range(len(f)) if f[i:i + len(al)] == al), None)


def confere(lista, nome):
    falta, ordem, n = [], [], 0
    for aid, itens in lista.items():
        fala = D["ancoras"][aid]["fala"].split()
        ult = -1
        for tipo, fr, *onde in itens:
            n += 1
            i = first(fala, tok(fr))
            if i is None:
                falta.append(f"{aid} [{tipo}] {fr!r} {' '.join(onde)}")
            elif tipo in ("gat", "gat_novo", "gat*"):
                if i <= ult:
                    ordem.append(f"{aid} {fr!r} (posição {i} ≤ {ult}) {' '.join(onde)}")
                ult = max(ult, i)
    print(f"{nome}: {n} frases · faltando {len(falta)} · fora de ordem {len(ordem)}")
    for x in falta:
        print("  FALTA", x)
    for x in ordem:
        print("  ORDEM", x)
    return not falta and not ordem


def do_codigo():
    out = {}
    for f in sorted(AQUI.glob("sec_*.py")):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        ev = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                fn = node.func
                nm = fn.attr if isinstance(fn, ast.Attribute) else (fn.id if isinstance(fn, ast.Name) else None)
                if nm == "an" and node.args and isinstance(node.args[0], ast.Constant):
                    ev.append((node.lineno, node.col_offset, "an", node.args[0].value))
                elif nm == "gat" and node.args and isinstance(node.args[0], ast.Constant):
                    ev.append((node.lineno, node.col_offset, "gat", node.args[0].value))
                elif nm == "le":
                    if len(node.args) >= 4 and isinstance(node.args[3], ast.Constant):
                        ev.append((node.lineno, node.col_offset, "le", node.args[3].value))
                    for kw in node.keywords:
                        if kw.arg == "ate" and isinstance(kw.value, ast.Constant):
                            ev.append((node.lineno, node.col_offset + 1, "ate", kw.value.value))
                elif nm == "tabela" and len(node.args) >= 3 and isinstance(node.args[2], ast.List):
                    for el in node.args[2].elts:
                        if isinstance(el, ast.Tuple) and isinstance(el.elts[0], ast.Constant) and isinstance(el.elts[0].value, str):
                            ev.append((el.lineno, el.col_offset, "gat*", el.elts[0].value))
            if isinstance(node, ast.For) and isinstance(node.iter, (ast.Tuple, ast.List)):
                m = re.search(r"self\.gat\((\w+)\)", ast.unparse(node))
                if m:
                    var, tgt, idx = m.group(1), node.target, None
                    if isinstance(tgt, ast.Tuple):
                        nomes = [getattr(t_, "id", None) for t_ in tgt.elts]
                        idx = nomes.index(var) if var in nomes else None
                    for el in node.iter.elts:
                        if isinstance(el, ast.Tuple) and idx is not None and isinstance(el.elts[idx], ast.Constant):
                            ev.append((el.lineno, el.col_offset, "gat*", el.elts[idx].value))
                        elif isinstance(el, ast.Constant) and idx is None:
                            ev.append((el.lineno, el.col_offset, "gat*", el.value))
        cur = None
        for ln, co, k, v in sorted(ev):
            if k == "an":
                cur = v
                out.setdefault(cur, [])
            elif cur and v is not None:
                out[cur].append([k, v, f"{f.name}:{ln}"])
    return out


pal = sum(D["ancoras"][a]["palavras"] for a in D["ordem"])
print(f"âncoras {len(D['ordem'])} · palavras {pal} · fonte dos tempos: {D['fonte']}")
ok = len(D["ordem"]) == 69
ok &= confere(json.loads((AQUI / "frases_sincronia_v34.json").read_text(encoding="utf-8")), "(1) frases_sincronia_v34.json")
if "--cena" in sys.argv:
    ok &= confere(do_codigo(), "(2) código da cena (sec_*.py)")
sys.exit(0 if ok else 1)
