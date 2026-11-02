"""v3 §3: os 14 casos da §2 viram teste da auditoria. Para cada caso (tempo no preview v2 → lote e tempo local), lista o que a auditoria v3
acusou em ±1,5 s. uso: python casos14.py [sufixo do log]  (padrão: _teste_v2 → log_aud_<LOTE>__teste_v2.txt; '' → log_aud_<LOTE>.txt)"""
import re
import sys
from collections import Counter
from pathlib import Path

U = Path(__file__).resolve().parent
SUF = sys.argv[1] if len(sys.argv) > 1 else "__teste_v2"
INICIO_V2 = {"PH": 0.0, "PX0": 85.1, "PX2": 216.2, "PX3": 316.6, "PX4": 573.3, "PX5": 679.9, "PEP": 833.3}
CASOS = [   # (nº, tempo no v2, lote, [(categoria, trecho do texto envolvido ou None)], descrição) — conta só o que é o problema do caso
    (1, 85.0, "PX0", [("SEM PALCO", None)], "quadro vazio no começo do X0"),
    (2, 123.4, "PX0", [("LINHA ÓRFÃ", None)], "linha órfã '= (−1/16)/(¾)'"),
    (3, 123.4, "PX0", [("ENCOSTADO", "'O'"), ("TEXTO SOBRE OBJETO", "0,25m"), ("TEXTO SOBRE OBJETO", "'O'"), ("TEXTO SOBRE OBJETO", "MASSA"), ("CHAMADA CRUZA CORPO", None)],
     "'O' e '0,25 m' encostados; MASSA −¼ na borda do furo"),
    (4, 131.2, "PX0", [("SELO DUPLO", None)], "dois selos no crossfade"),
    (5, 138.8, "PX0", [("FORA DA ZONA", "'y'"), ("ENCOSTADO", "'y'"), ("TEXTO SOBRE CAIXA", "'y'"), ("TEXTO SOBRE OBJETO", "10cm"), ("ENCOSTADO", "10cm"), ("FORA DA ZONA", "'1.'")],
     "chip sobre o rótulo y; '10 cm' encostado"),
    (6, 177.4, "PX0", [("CHAMADA CRUZA CORPO", None), ("ENCOSTADO", "1600"), ("SOBREPOSICAO", "1600"), ("TEXTO SOBRE OBJETO", "100")],
     "MASSA ∝ 1600 sobre o y; chamadas cruzam a placa"),
    (7, 391.4, "PX3", [("PALCO 3D", None)], "folha e gafanhoto sumiram"),
    (8, 406.4, "PX3", [("SELO DUPLO", None), ("FORA DA ZONA", "trajetória"), ("FORA DA ZONA", "3D")], "VISTO DA ÁGUA duplicado; trajetória no topo"),
    (9, 436.6, "PX3", [("SOBREPOSICAO", "=1g"), ("SOBREPOSICAO", "=4g"), ("ENCOSTADO", "Delta"), ("TEXTO SOBRE OBJETO", "Delta"), ("ENCOSTADO", "=1g")],
     "m = 1 g sobre m; Δx sobre o 70"),
    (10, 451.8, "PX3", [("LINHA ÓRFÃ", None)], "caixa órfã '= 1,25 v cos θ'"),
    (11, 497.0, "PX3", [("RÉGUA DUPLA", None), ("TEXTO SOBRE OBJETO", "0,1cm"), ("TEXTO SOBRE OBJETO", "infty")], "réguas empilhadas; M → ∞ sobre a folha"),
    (12, 715.0, "PX5", [("TEXTO SOBRE OBJETO", "vec g"), ("ENCOSTADO", "vec g"), ("TEXTO SOBRE OBJETO", "INTERNA"), ("ENCOSTADO", "INTERNA")],
     "M g⃗ no fio e no ⊕; INTERNA na coluna"),
    (13, 733.0, "PX5", [("ESPREMIDO", None), ("TEXTO SOBRE OBJETO", "'a'"), ("TEXTO SOBRE OBJETO", "3g"), ("TEXTO SOBRE OBJETO", "'T'")], "T, a, 3g, 1g espremidos"),
    (14, 760.0, "PX5", [("ENCOSTADO", "2kg"), ("ENCOSTADO", "4,9"), ("SOBREPOSICAO", "4,9"), ("SOBREPOSICAO", "'0'")], "'2 kg0'; ±4,9 sobre os rótulos"),
]
logs = {}
out = []
ok = 0
for n, tv2, lote, quer, desc in CASOS:
    if lote not in logs:
        f = U / f"log_aud_{lote}{SUF}.txt"
        logs[lote] = [(float(m.group(1)), m.group(2)) for m in re.finditer(r"\[audit\]\s+([0-9.]+)s (.+)", f.read_text(encoding="utf-8", errors="replace"))] if f.exists() else []
    tl = tv2 - INICIO_V2[lote]
    perto = [(t, s) for t, s in logs[lote] if abs(t - tl) <= 1.5]
    bate = lambda s, q: s.startswith(q[0]) and (q[1] is None or q[1] in s)
    achou = sorted({q[0] for q in quer if any(bate(s, q) for _, s in perto)})
    ok += bool(achou)
    c = Counter(s.split(" '")[0][:28] for _, s in perto)
    ex = next((s for _, s in perto if any(bate(s, q) for q in quer)), "")
    out.append(f"#{n:2d} {lote} {tl:6.1f}s {'ACUSOU' if achou else 'NÃO ACUSOU'} ({', '.join(achou) or '—'}) · {desc}\n      ex.: {ex[:110]}\n      ±1,5 s: {dict(c)}")
out.append(f"TOTAL: {ok}/14 casos acusados")
print("\n".join(out))
(U / "renders" / "v3").mkdir(parents=True, exist_ok=True)
(U / "renders" / "v3" / f"casos14{SUF or '_v3'}.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
