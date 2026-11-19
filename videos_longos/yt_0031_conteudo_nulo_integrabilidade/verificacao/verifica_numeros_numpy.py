"""yt_0031 · conferência numérica (numpy, sem sympy) dos números da tela que saem de verifica_calc3_32t2_sympy.py (o sympy não está na .venv).
Mesmas regras do script do handoff; amostragem fina (400 pontos por intervalo) para o mínimo/máximo da solda."""
import math
import numpy as np

g = lambda a: 1 + .42 * np.sin(1.7 * np.asarray(a) - .4)
fx = lambda a, b, am=400: (g(np.linspace(a, b, am + 1)).min(), g(np.linspace(a, b, am + 1)).max())
ok = []
A1 = 2 + (.42 / 1.7) * (math.cos(.4) - math.cos(3)); massa = 12 - 2 * A1
ok.append(("V4 A1 ≈ 2,4721 e massa ≈ 7,06", abs(A1 - 2.47214) < 1e-4 and round(massa, 2) == 7.06))
esp = {4: (5, 6.00, 8.50, 2.50), 8: (11, 6.38, 7.75, 1.38), 16: (24, 6.66, 7.41, 0.75), 32: (47, 6.88, 7.25, 0.37), 64: (95, 6.97, 7.15, 0.19)}
for n, (c, lo, hi, d) in esp.items():
    h = 2 / n; r = 0; s = S = 0.0
    for i in range(n):
        mn, mx = fx(i * h, i * h + h)
        for j in range(n):
            cc, dd = j * h, j * h + h; lv, ps = cc <= mx, dd > mn
            r += lv and ps; s += (1 if lv else 3) * h * h; S += (3 if ps else 1) * h * h
    print(f"n={n:3d} vermelhas={r:3d} por baixo={s:.4f} por cima={S:.4f} dif={S - s:.4f}")
    ok.append((f"V5/V6 tabela n={n}", r == c and f"{s:.2f}" == f"{lo:.2f}" and f"{S:.2f}" == f"{hi:.2f}" and abs((S - s) - d) < 0.006 and abs((S - s) - 2 * r * h * h) < 1e-9))
cob = {n: sum((lambda m: m[1] - m[0])(fx(i * 2 / n, (i + 1) * 2 / n)) * 2 / n for i in range(n)) for n in (4, 16, 64)}
print("coberturas da solda:", {k: round(v, 4) for k, v in cob.items()})
ok.append(("B3-2 coberturas 0,46 / 0,12 / 0,03", [f"{cob[k]:.2f}" for k in (4, 16, 64)] == ["0.46", "0.12", "0.03"]))
ok.append(("B4 parábola 4Δ: 2 / 1 / 0,5", [4 * 2 / n for n in (4, 8, 16)] == [2, 1, 0.5]))
xs = np.linspace(0, 2, 200001); gv = g(xs); dg = np.diff(gv)
sobe, desce = dg[dg > 0].sum(), -dg[dg < 0].sum()
print(f"solda sobe {sobe:.4f} desce {desce:.4f} total {sobe + desce:.4f}")
ok.append(("B4 solda 0,58 / 0,36 / 0,94", (round(sobe, 2), round(desce, 2), round(sobe + desce, 2)) == (0.58, 0.36, 0.94)))
ok.append(("B4 arco 2Δ: 1 / 0,5 / 0,25 / 0,125", [4 / n for n in (4, 8, 16, 32)] == [1, 0.5, 0.25, 0.125]))
ok.append(("B6-2 δ = 1/(4√2) ≈ 0,177 → 0,17; f(1,9;1,9)=7,22; f(1,78;1,78)=6,34", round(1 / (4 * math.sqrt(2)), 3) == 0.177 and round(2 * 1.9 ** 2, 2) == 7.22 and round(2 * 1.78 ** 2, 2) == 6.34))
k1 = (1 / (math.pi / 2 + 2 * math.pi), 1 / (3 * math.pi / 2 + 2 * math.pi))
ok.append(("B6-3 par k=1: 0,127 e 0,091", (round(k1[0], 3), round(k1[1], 3)) == (0.127, 0.091)))
ok.append(("B1 célula [1,5;2]²: piso 4,5 e teto 8", (2 * 1.5 ** 2, 2 * 2 ** 2) == (4.5, 8)))
for t, v in ok:
    print(t, ":", v)
print(f"{sum(v for _, v in ok)}/{len(ok)} checagens True")
