"""ORDEM POR INÍCIO DE GLIFO (handoff final §2.1): na mesma linha, x1 < x2 ⇒ t_início1 ≤ t_início2 (tolerância de 1 quadro).
Lê as linhas `[glifo] t x0 x1 y` que a CanetaAnim imprime ao começar (instante em que cada glifo começa a ser traçado, relógio do lote)
nos logs de render (log_<L>.txt) e agrupa por linha (|Δy| < 0,35) e por rajada (intervalo < 1,0 s). Voos (TransformFromCopy) não entram: são declarados.
Uso: python ordem_glifo.py PH PB1 ...   → imprime as violações por tempo e centro x; resumo `ORDEM GLIFO violações=N`."""
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
TOL = 1.0 / 15 + 1e-3
total = 0
for L in sys.argv[1:]:
    f = U / f"log_{L}.txt"
    if not f.exists():
        print(f"[{L}] sem log")
        continue
    gl, play = [], 0
    for ln in f.read_text(encoding="utf-8", errors="replace").splitlines():
        if ln.startswith("[ordem]"):                 # cada voa/passo imprime [ordem] antes do play: os [glifo] seguintes são dele
            play += 1
        m = re.match(r"\[glifo\] (\S+) (\S+) (\S+) (\S+)", ln)
        if m:
            t, x0, x1, y = map(float, m.groups())
            gl.append((play, t, x0, x1, y))
    cl = {}
    for pl, t, x0, x1, y in gl:
        cl.setdefault(pl, dict(y=y, g=[]))["g"].append((t, x0, x1))
    cl = list(cl.values())
    viol = 0
    for c in cl:
        g = sorted(c["g"], key=lambda a: a[1])
        for i in range(len(g)):
            for j in range(i + 1, len(g)):
                # i está INTEIRO à esquerda de j (sem sobreposição horizontal: numerador/barra/denominador e índices ficam de fora)
                if g[i][2] <= g[j][1] + 0.02 and g[i][0] > g[j][0] + TOL:
                    viol += 1
                    print(f"[{L}] t={g[i][0]:.2f}s y={c['y']:.2f}: glifo x={g[i][1]:.2f}..{g[i][2]:.2f} começa depois do glifo x={g[j][1]:.2f}..{g[j][2]:.2f} (t={g[j][0]:.2f})")
                    break
            else:
                continue
            break
    print(f"[{L}] {len(gl)} glifos em {len(cl)} plays; ORDEM GLIFO violações={viol}")
    total += viol
print(f"ORDEM GLIFO violações={total}")
