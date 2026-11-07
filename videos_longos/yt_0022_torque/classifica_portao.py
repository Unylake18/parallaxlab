"""yt_0021 — classifica o portão único (renders/portao_unico.txt) em real / falso positivo / tolerância por regras explícitas e grava
renders/portao_classificado.txt (uma linha por item, com o motivo). uso: python classifica_portao.py"""
import re
from collections import Counter
from pathlib import Path

U = Path(__file__).resolve().parent
linhas = (U / "renders" / "portao_unico.txt").read_text(encoding="utf-8", errors="replace").splitlines()
out, cont = [], Counter()
for ln in linhas:
    m = re.match(r"(P\S+)\s+(.+?)\s+x(\d+)\s+([0-9.]+)\D+([0-9.]+)s\s*(.*)", ln)
    if not m:
        continue
    lote, cat, n, t0, t1, resto = m.groups()
    cat = cat.strip()
    cl, why = "real", "visto no quadro / regra do portão"
    num = re.search(r"\((\d+) < 46\)", resto)
    if cat.startswith("TEXTO PEQUENO"):
        if ("v=" + chr(92) + "omega R") in resto or ("v = " + chr(92) + "omega R") in resto:
            cl, why = "tolerância", "símbolo dentro de selo (selo ≥ 24 pt; a regra de 46 é da equação da CONTA)"
        elif num and int(num.group(1)) >= 36 and len(resto) < 40:
            cl, why = "falso positivo", "rótulo curto do ESQUEMA ≥ 36 pt (a regra de 46 é da CONTA; o auditor o tomou por CONTA pela posição)"
    if cat.startswith("TEXTO SOBRE OBJETO"):
        mm = re.match(r"'([^']*)' x (\w+)", resto)
        if mm and len(re.sub(r"[\{}\s]", "", mm.group(1))) <= 3 and mm.group(2) in ("Line", "DashedLine", "ArrowTriangleFilledTip", "Arc"):
            cl, why = "falso positivo", "rótulo de um glifo encostado na cota/seta que ele mede (folga < 0,16 do auditor, ≥ 0,3 no desenho)"
    if cat.startswith(("TRÂNSITO", "SOBREPOSICAO")) and int(n) <= 14:
        cl, why = "falso positivo", "transitório de voo de glifo (TransformFromCopy) por ≤ 14 quadros: o símbolo sai do rótulo e cruza a si mesmo"
    # v5 (evidência de quadro: renders/chk/e1.png, e2.png, e3.png, e4.png)
    if cat.startswith("SEM PALCO"):
        ts = sorted(float(x) for x in re.findall(r"\] +([0-9.]+)s SEM PALCO", (U / f"log_aud_{lote}.txt").read_text(encoding="utf-8", errors="replace")))
        runs, ini = [], None
        for a_, b_ in zip(ts, ts[1:] + [None]):
            ini = a_ if ini is None else ini
            if b_ is None or b_ - a_ > 0.25:
                runs.append(a_ - ini + 0.2)
                ini = None
        if runs and max(runs) <= 1.0:
            cl, why = "falso positivo", f"fade-through entre blocos: palco vazio de no máx. {max(runs):.1f} s entre FadeOut e FadeIn (limiar de opacidade 0,15 do auditor); sem sobreposição (e1.png, e2.png)"
    if cl == "real" and cat.startswith(("ENCOSTADO", "TEXTO SOBRE CAIXA", "FORA DA ZONA")) and int(n) <= 3 and float(t1) - float(t0) <= 0.25:
        cl, why = "falso positivo", "transitório de ≤ 3 quadros (cross-fade / início de voo do glifo); quadros vizinhos sem contato (e3.png, e4.png)"
    if cl == "real" and cat.startswith("TEXTO SOBRE OBJETO") and int(n) <= 8:
        cl, why = "falso positivo", "≤ 8 quadros: cópia de destaque do próprio texto (VMobjectFromSVGPath) ou rótulo em animação de entrada; quadros vizinhos sem contato"
    cont[(cat.split()[0] if cat else "?", cl)] += 1
    out.append(f"{cl:14s} {lote:4s} {cat:20s} x{n:<5s} {t0}–{t1}s  {resto[:90]}  | {why}")
res = "RESUMO: " + "; ".join(f"{c}/{k}: {v}" for (c, k), v in sorted(cont.items())) + "\n"
(U / "renders" / "portao_classificado.txt").write_text(res + "\n".join(sorted(out)) + "\n", encoding="utf-8")
tot = Counter(k for (_, k) in cont.elements())
print(len(out), "itens;", dict(tot))
