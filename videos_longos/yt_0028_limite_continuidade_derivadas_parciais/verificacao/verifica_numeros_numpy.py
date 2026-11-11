"""yt_0028: conferência numérica (numpy) dos valores da tela (handoff v1.2 §4). Substitui a rodada do sympy, que não está na .venv (não instalado,
por regra do AGENTS.md). uso: python verifica_numeros_numpy.py"""
import math

import numpy as np

F = lambda x, y: np.array([1 + math.sin(x) - math.sin(y), 2 * math.sin(x) + 2 - math.cos(x) - math.cos(y)])
P = F(0, 0)
ok = []


def chk(nome, v, alvo, tol=5e-3):
    r = bool(np.allclose(v, alvo, atol=tol))
    ok.append(r)
    print(f"{r}  {nome}: {np.round(v, 4)} (alvo {alvo})")


chk("F(P)", P, [1, 0])
h = 1e-6
dFx, dFy = (F(h, 0) - F(-h, 0)) / (2 * h), (F(0, h) - F(0, -h)) / (2 * h)
chk("∂F/∂x(P)", dFx, [1, 2])
chk("∂F/∂y(P)", dFy, [-1, 0])
J = np.stack([dFx, dFy], 1)
chk("rot = ∂Q/∂x − ∂P/∂y", J[1, 0] - J[0, 1], 3)
chk("div = ∂P/∂x + ∂Q/∂y", J[0, 0] + J[1, 1], 1)
chk("deformação 1 = ∂P/∂x − ∂Q/∂y", J[0, 0] - J[1, 1], 1)
chk("deformação 2 = ∂Q/∂x + ∂P/∂y", J[1, 0] + J[0, 1], 1)
for hh, al in ((1, (.84, 2.14)), (.5, (.96, 2.16)), (.2, (.99, 2.09)), (.1, (1.00, 2.05))):
    chk(f"quociente em x, h = {hh}", (F(hh, 0) - P) / hh, al)
for kk, al in ((1, (-.84, .46)), (.5, (-.96, .25)), (.2, (-.99, .10)), (.1, (-1.00, .05))):
    chk(f"quociente em y, k = {kk}", (F(0, kk) - P) / kk, al)


def raio_max(d):
    th = np.linspace(0, 2 * math.pi, 4001)
    return max(np.linalg.norm(F(d * math.cos(t), d * math.sin(t)) - P) for t in th)


def delta_max(eps):
    lo, hi = 0.0, 1.0
    for _ in range(40):
        m = (lo + hi) / 2
        dd = np.linspace(1e-4, m, 60)
        lo, hi = (m, hi) if max(raio_max(d) for d in dd[-3:]) < eps else (lo, m)
    return lo


for eps, d in ((1, .41), (.5, .21)):
    r = raio_max(d)
    ok.append(r < eps)
    print(f"{r < eps}  ε = {eps}: com δ = {d}, maior |F(X) − F(P)| na borda = {r:.4f} < ε (maior δ ≈ {delta_max(eps):.3f})")
w = math.sqrt(7) / 2


def expJ(t):
    e, c, s = math.exp(t / 2), math.cos(w * t), math.sin(w * t) / w
    return e * (c * np.eye(2) + s * (np.array([[1, -1], [2, 0]]) - .5 * np.eye(2)))


from scipy.linalg import expm  # noqa: E402  (só para conferir a fórmula fechada)

chk("exp(0,35 J) fechada = expm", expJ(.35), expm(.35 * np.array([[1, -1], [2, 0]])), 1e-9)
chk("área × det e^(0,35 J)", np.linalg.det(expJ(.35)), 1.42)
chk("gancho: área 1,2·e^0,55 × 1,2·e^−0,55", 1.2 * math.exp(.55) * 1.2 * math.exp(-.55), 1.44)
chk("gancho: lados", [1.2 * math.exp(.55), 1.2 * math.exp(-.55)], [2.08, .69], 6e-3)
for m in (0, 1, -1):
    chk(f"G na reta y = {m}x", 2 * m / (1 + m * m), m)
print(f"\n{sum(ok)} de {len(ok)} checagens True")
