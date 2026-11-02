"""v4 §3: os 13 casos da §2 viram teste da auditoria. Para cada caso (tempo no preview v3 → lote e janela local), lista o que a auditoria v4
acusou na janela. uso: python casos13.py [sufixo do log]  (padrão: __teste_v3 → log_aud_<LOTE>__teste_v3.txt; '' → log_aud_<LOTE>.txt, o v4)"""
import re
import sys
from collections import Counter
from pathlib import Path

U = Path(__file__).resolve().parent
SUF = sys.argv[1] if len(sys.argv) > 1 else "__teste_v3"
INICIO_V3 = {"PH": 0.0, "PX0": 85.07, "PX2": 214.27, "PX3": 314.67, "PX4": 571.40, "PX5": 676.33, "PEP": 829.73}
F = 1.5                                                                 # folga em volta da janela (s)
CASOS = [   # (nº, (t0, t1) no preview v3, lote, [(categoria, trecho do texto ou None)], descrição)
    (1, (595.0, 651.0), "PX4", [("CALHA", "p_1"), ("ENCOSTADO", "p_1")], "p⃗₁ encosta no início da CONTA ('p⃗₁P⃗ = 0⃗')"),
    (2, (632.7, 632.7), "PX4", [("ENCOSTADO no selo do referencial", None)], "'1 m/s' colado embaixo do selo VISTO DO CENTRO DE MASSA"),
    (3, (638.8, 638.8), "PX4", [("ENCOSTADO", "000J"), ("CALHA", "3.000J"), ("TEXTO SOBRE OBJETO", "000J")], "2.000 J e 3.000 J empilhados ao lado da barra"),
    (4, (665.0, 675.0), "PX4", [("CALHA", "12m/s"), ("ENCOSTADO", "12m/s")], "'12 m/s' em cima de 'DEPOIS:'"),
    (5, (762.0, 762.0), "PX5", [("ENCOSTADO", "4,9"), ("TEXTO SOBRE OBJETO", "4,9"), ("TEXTO SOBRE CAIXA", "4,9")], "−4,9 sobre a plataforma, no mostrador"),
    (6, (712.0, 712.0), "PX5", [("TRÂNSITO", None), ("SOBREPOSICAO", "M=6"), ("TEXTO SOBRE OBJETO", "M=6"), ("ENCOSTADO", "M=6")], "M = 6 kg sobre o tracejado do SISTEMA"),
    (7, (434.7, 434.7), "PX3", [("TRÂNSITO", None)], "m Δx_g + M Δx_f = 0: glifos pousando uns sobre os outros"),
    (8, (107.7, 107.7), "PX0", [("TRÂNSITO", None)], "substituição m₁ → 1, x₁ → 0… vira sopa de glifos"),
    (9, (183.7, 187.7), "PX0", [("TRÂNSITO", None), ("TEXTO SOBRE CAIXA", "1,95")], "cópia ≈ −1,95 cm atravessa a linha de baixo e a caixa"),
    (10, (485.6, 485.6), "PX3", [("TRÂNSITO", None)], "intervalos de θ se sobrepõem ao entrar na caixa"),
    (11, (284.8, 284.8), "PX2", [("MARCADORES COLADOS", None)], "⊗ da média dos cantos encosta no ⊕"),
    (12, (302.0, 314.0), "PX2", [("FORA DA ZONA cubo", None), ("FORA DA ZONA texto do ESQUEMA embaixo", None), ("OBJETO FORA DA MARGEM cubo", None),
                                 ("CALHA", "'y'")], "eixo x e rótulo y na margem de baixo com o cubo girando"),
    (13, (329.0, 374.0), "PX3", [("RÓTULO SOLTO", None)], "m = 1 g e M = 4 g longe do gafanhoto e da folha"),
]
logs = {}
out = []
ok = 0
for n, (a, b), lote, quer, desc in CASOS:
    if lote not in logs:
        f = U / f"log_aud_{lote}{SUF}.txt"
        logs[lote] = [(float(m.group(1)), m.group(2)) for m in re.finditer(r"\[audit\]\s+([0-9.]+)s (.+)", f.read_text(encoding="utf-8", errors="replace"))] if f.exists() else []
    t0, t1 = a - INICIO_V3[lote], b - INICIO_V3[lote]
    perto = [(t, s) for t, s in logs[lote] if t0 - F <= t <= t1 + F]
    bate = lambda s, q: s.startswith(q[0]) and (q[1] is None or q[1] in s.replace(" ", ""))
    achou = sorted({q[0] for q in quer if any(bate(s, q) for _, s in perto)})
    ok += bool(achou)
    c = Counter(s.split(" '")[0][:30] for _, s in perto)
    ex = next((s for _, s in perto if any(bate(s, q) for q in quer)), "")
    jan = f"{t0:6.1f}s" if abs(t1 - t0) < 0.05 else f"{t0:.1f}–{t1:.1f}s"
    out.append(f"#{n:2d} {lote} {jan} {'ACUSOU' if achou else 'NÃO ACUSOU'} ({', '.join(achou) or '—'}) · {desc}\n      ex.: {ex[:120]}\n      na janela: {dict(c)}")
out.append(f"TOTAL: {ok}/13 casos acusados")
print("\n".join(out))
(U / "renders" / "v4").mkdir(parents=True, exist_ok=True)
(U / "renders" / "v4" / f"casos13{SUF or '_v4'}.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
