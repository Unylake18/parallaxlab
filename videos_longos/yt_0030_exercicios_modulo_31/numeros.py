"""yt_0030 · QA §8.8: os números do §3.3 que aparecem na tela, com o instante (preview emendado) e o quadro; vírgula decimal; as medições dos logs
(áreas, giros, quinas do D5 ③). → renders/<rodada>/qa/numeros_<rodada>.txt. uso: python numeros.py [rodada]"""
import json
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
RODADA = sys.argv[1] if len(sys.argv) > 1 else "v1"
R = U / "renders" / RODADA
INI = {k: v / 15 for k, v in json.loads((R / f"lotes_{RODADA}.json").read_text(encoding="utf-8"))["inicio"].items()}
LOG = {l: (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace") for l in INI}

# (bloco, o que aparece na tela, lote, âncora, frase do gatilho)
TAB = [
    ("D1", "cantos ①–④: (0,0)→(0,0); (1,0)→(1,1); (1,1)→(2,0); (0,1)→(1,−1)", "PD1", "D1-3", "a origem fica parada"),
    ("D1", "ÁREA 1 → 2 · ESPELHADO (lado √2: o quadrado girado 45°)", "PD1", "D1-3", "agora é raiz de dois ao quadrado"),
    ("D1", "(u + v)² + (u − v)² = 2(u² + v²); círculo r → r√2", "PD1", "D1-4", "e sobra duas vezes"),
    ("D1", "COMO TRANSFORMAÇÃO: ÁREA × 2", "PD1", "D1-6", "como transformação a área dobrou"),
    ("D2", "x − y = c ⇒ f = (1, c); rótulos (1, 0), (1, 1), (1, 2)", "PD2", "D2-3", "na própria diagonal"),
    ("D2", "rótulos (1, −1), (1, −2) acima da diagonal", "PD2", "D2-3", "e acima da diagonal"),
    ("D3", "‖v‖ = r^{1−2α}: = r (α 0), = 1 (α ½), = 1/r (α 1)", "PD3", "D3-2", "com alfa zero a rapidez cresce"),
    ("D3", "rot v = (2 − 2α)/(x² + y²)^α; div v = 0", "PD3", "D3-3", "nenhum desses redemoinhos"),
    ("D3", "α = 0: rot 2 · α = ½: rot 1/r · α = 1: rot 0", "PD3", "D3-4", "alfa zero dois menos zero"),
    ("D3", "α = 2: rot −2/r⁴ (gira ↻ com a volta ↺)", "PD3", "D3-5", "e alfa dois"),
    ("D3", "origem: 0 < α < ½ contínuo se v(0) = 0; α = ½ sem limite; α = 1 explode; α = 0 já contínuo", "PD3", "D3-6", "com alfa entre zero e meio"),
    ("D3", "giro de 90°: div w = (2 − 2α)/(x² + y²)^α, rot w = 0", "PD3", "D3-7", "o rotacional vira zero"),
    ("D3b", "rot ∇φ = (φ_zy − φ_yz, φ_xz − φ_zx, φ_yx − φ_xy) = 0⃗", "PD3B", "D3b-1", "tudo cancela"),
    ("D3b", "div(rot F) = R_yx − Q_zx + P_zy − R_xy + Q_xz − P_yz = 0 (pares riscados um a um)", "PD3B", "D3b-3", "e elas se cancelam aos pares"),
    ("D3b", "div = sen y − sen y + 1 → = 1 ≠ 0 ⇒ NÃO EXISTE", "PD3B", "D3b-4", "total um"),
    ("D4", "‖F‖ = |xy|/r = r|sen 2θ|/2 ≤ r/2", "PD4", "D4-3", "e isso nunca passa da metade"),
    ("D4", "δ = 2ε; ε de 1 a 0,5 e de volta", "PD4", "D4-4", "venceu para qualquer épsilon"),
    ("D4", "tabela na origem toda zero; rot 0 · div 0 · d₁ 0 · d₂ 0", "PD4", "D4-5", "a tabela é toda zero"),
    ("D4", "F(sX) = sF(X); ZOOM × 1, × 10, × 100", "PD4", "D4-6", "o número aparece ao quadrado em cima"),
    ("D4", "∂P/∂x = 2xy³/(x² + y²)²: 0 nos eixos, ½ e −½ nas diagonais (r = 2,5; 1,25; 0,625)", "PD4", "D4-7", "e vale meio na diagonal inteira"),
    ("D4", "‖erro‖/‖H‖ = ½ na diagonal ↛ 0", "PD4", "D4-7", "e a tabela perde a garantia"),
    ("D5 ①", "J = [[1, 1], [1, −1]]; rot 0, div 0, d₁ 2, d₂ 2", "PD5", "D5-3", "segunda um mais um"),
    ("D5 ②", "J = [[0, 0], [1, −1]]; rot 1, div −1, d₁ 1, d₂ 1", "PD5", "D5-7", "e um mais zero"),
    ("D5 ③", "J = [[2x, −2y], [2y, 2x]]; rot 4y, div 4x, d₁ = d₂ = 0", "PD5", "D5-10", "zero em qualquer ponto"),
    ("A1", "div 0; rot = −2x/9; 2/3 ↺ e −2/3 ↻; galho 1/3 rad/s, uma volta a cada ≈ 19 s; d₁ = 0, d₂ = −2x/9", "PA1", "A1-5", "aqui a primeira deformação"),
    ("A2", "rot 0, div 0, d₁ = 2; u·y + x·v = xy − xy = 0; ∇²φ = 1 − 1 = 0", "PA2", "A2-3", "e o laplaciano dela"),
    ("A4", "d₁ = d₂ = 0 ⇔ Cauchy-Riemann; (x + iy)² = x² − y² + i·2xy; irmão (x² − y², −2xy): rot 0 · div 0", "PA4", "A4-4", "e o irmão desse campo"),
    ("A3", "2 − 2α ao vivo de 1,40 a 0,00 ⇒ α = 1; ‖B‖ = r/r² = 1/r", "PA3", "A3-3", "e alfa igual a um"),
    ("A3", "div E = (2 − 2α)/(x² + y²)^α = 0 ⇒ α = 1", "PA3", "A3-4", "divergente dois menos dois alfa"),
    ("A3", "no plano (2 − p), no espaço (3 − p); p = 3 ⇒ ‖E‖ = r/r³ = 1/r²", "PA3", "A3-5", "para zerar o expoente é três"),
    ("S", "régua 0–20 kg; 8 kg? e 16 kg? (a massa real, 32/3, não aparece)", "PS", "S-2", "pela média dos quatro cantos"),
]


def t_gat(lote, aid, frase):
    a = {m.group(1): float(m.group(2)) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", LOG[lote])}
    m = re.search(r"\[gatilho\] %s +([0-9.]+)s \(alvo[^)]*\) %s\n" % (re.escape(aid), re.escape(frase)), LOG[lote])
    return INI[lote] + a[aid] + float(m.group(1)) if m else None


L = [f"yt_0030 {RODADA} · números na tela (handoff §3.3), instante do gatilho no preview emendado e quadro (15 fps). Vírgula decimal em todos os "
     f"decimais da tela (1,40 → 0,00; 0,5; 2,5 etc.; o rótulo do contador usa NumBR).", ""]
for b, txt, lote, aid, fr in TAB:
    t = t_gat(lote, aid, fr)
    L.append(f"{b:6s} {int(t) // 60}:{t % 60:05.2f} · quadro {round(t * 15):5d} · {txt}" if t is not None else f"{b:6s} (gatilho não achado: {fr}) · {txt}")
L += ["", "MEDIÇÕES NOS LOGS (polígono desenhado):"]
for l in INI:
    for m in re.finditer(r"(\[(?:D1|D3|D3b|D4|D5|A1|A2|A3)\] .+)", LOG[l]):
        L.append(f"  {l:5s} {m.group(1)}")
import math  # noqa: E402

import numpy as np  # noqa: E402


def _fl3(x, y, t):
    dr, di = 1 - t * x, -t * y
    d = dr * dr + di * di
    return (x * dr + y * di) / d, (y * dr - x * di) / d


L += ["", "D5 ③ · quinas também pelo quadrilátero dos 4 cantos (cordas), lado 0,3 e t = 0,1. O polígono desenhado é a borda exata (30 pontos por",
      "lado): nas tangentes das quinas dá 90,0° ± 0,1° (linhas [D5] ③ acima), porque z/(1 − tz) é conforme; as cordas sentem a tabela mudando de um",
      "canto para o outro (o 'tiquinho' da fala):"]
for c in ((1, 0), (0, 1), (1, 1)):
    s = .3
    Q = [np.array(_fl3(x, y, .1)) for x, y in ((c[0] - s / 2, c[1] - s / 2), (c[0] + s / 2, c[1] - s / 2), (c[0] + s / 2, c[1] + s / 2), (c[0] - s / 2, c[1] + s / 2))]
    ang = [math.degrees(math.acos((Q[i - 1] - Q[i]) @ (Q[(i + 1) % 4] - Q[i]) / np.linalg.norm(Q[i - 1] - Q[i]) / np.linalg.norm(Q[(i + 1) % 4] - Q[i]))) for i in range(4)]
    L.append(f"  {c}: {', '.join(f'{a:.2f}°'.replace('.', ',') for a in ang)} · maior desvio {max(abs(a - 90) for a in ang):.2f}°".replace(".", ","))
(R / "qa").mkdir(parents=True, exist_ok=True)
(R / "qa" / f"numeros_{RODADA}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
