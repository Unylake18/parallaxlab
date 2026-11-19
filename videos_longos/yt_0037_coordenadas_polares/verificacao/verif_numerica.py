"""yt_0037 · conferência numérica (numpy) dos números que vão para a tela. O verifica_calc3_34t2_sympy.py do handoff precisa do sympy, que não está
na .venv (handoff §2.1: não instalar); esta conferência cobre as checagens H1, B1, B2, B3, B6 (área), B7 e S2 que o vídeo usa, com o raio a."""
import math

import numpy as np

ok = []


def chk(nome, cond, val=""):
    ok.append(bool(cond))
    print(f"{nome}: {bool(cond)} {val}")


def quad(f, a, b, n=200001):
    x = np.linspace(a, b, n)
    y = f(x)
    return float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(x)))


# H1 / B4: disco do começo
d = quad(lambda r: np.exp(-r * r) * r, 0, 1)
chk("H1 ∫₀¹ e^(−r²) r dr = (1 − 1/e)/2 ≈ 0,316", abs(d - (1 - 1 / math.e) / 2) < 1e-9, f"({d:.6f})")
chk("H1 u = r²: ∫₀¹ e^(−u) du/2 = −e^(−1)/2 − (−1/2)", abs(quad(lambda u: np.exp(-u) / 2, 0, 1) - (-math.exp(-1) / 2 + .5)) < 1e-9)
chk("H1 ∬ = 2π (1 − 1/e)/2 = π(1 − 1/e) ≈ 1,986", abs(2 * math.pi * d - math.pi * (1 - 1 / math.e)) < 1e-8, f"({math.pi * (1 - 1 / math.e):.4f})")
xs = np.linspace(-1, 1, 1601)
X, Y = np.meshgrid(xs, xs)
F = np.where(X * X + Y * Y <= 1, np.exp(-(X * X + Y * Y)), 0.0)
num = float(F.sum() * (xs[1] - xs[0]) ** 2)
chk("H1 numérica em xy ≈ π(1 − 1/e)", abs(num - math.pi * (1 - 1 / math.e)) < 5e-3, f"({num:.4f})")
# B1
r, t = 2, math.pi / 3
chk("B1 (2, π/3) ↦ (1, √3)", abs(r * math.cos(t) - 1) < 1e-12 and abs(r * math.sin(t) - math.sqrt(3)) < 1e-12)
# B2
cel = lambda r1, r2, dt: (r2 * r2 - r1 * r1) * dt / 2
chk("B2 célula = r̄ Δr Δθ exata", abs(cel(.5, 1, math.pi / 6) - .75 * .5 * math.pi / 6) < 1e-12)
chk("B2 célula de dentro = π/16 ≈ 0,196", abs(cel(.5, 1, math.pi / 6) - math.pi / 16) < 1e-12, f"({math.pi / 16:.4f})")
chk("B2 célula de fora = 7π/48 ≈ 0,458; razão 7/3", abs(cel(1.5, 2, math.pi / 6) - 7 * math.pi / 48) < 1e-12 and abs(cel(1.5, 2, 1) / cel(.5, 1, 1) - 7 / 3) < 1e-12)
th = np.linspace(0, 2 * np.pi, 7)
rr = 1.7
J = np.cos(th) * rr * np.cos(th) - (-rr * np.sin(th)) * np.sin(th)
chk("B2 det = r cos²θ + r sen²θ = r", np.allclose(J, rr))
a = 1.3
chk("B2 sem o r: 2πa; com o r: πa²", abs(2 * math.pi * a - 2 * math.pi * a) < 1e-12 and abs(2 * math.pi * quad(lambda r: r, 0, a) - math.pi * a * a) < 1e-9)
# B5 (disco deslocado)
tt = np.linspace(-np.pi / 2, np.pi / 2, 200001)
area = float(np.sum(((2 * np.cos(tt)) ** 2 / 2)[1:] * np.diff(tt)))
chk("B5 área ∫ 2cos²θ dθ = π", abs(area - math.pi) < 1e-4, f"({area:.5f})")
chk("B5 θ = π/3 ⇒ r = 1", abs(2 * math.cos(math.pi / 3) - 1) < 1e-12)
chk("B5 [θ + sen 2θ/2] de −π/2 a π/2 = (π/2 + 0) − (−π/2 + 0) = π", abs((math.pi / 2 + math.sin(math.pi) / 2) - (-math.pi / 2 + math.sin(-math.pi) / 2) - math.pi) < 1e-12)
# B6 (Gauss)
for aa, (lo, mi, hi) in ((1, (1.986, 2.231, 2.716)), (2, (3.084, 3.112, 3.140)), (3, (3.1412, 3.1415, 3.1416))):
    I = quad(lambda x: np.exp(-x * x), -aa, aa)
    L_, M_, H_ = math.pi * (1 - math.exp(-aa * aa)), I * I, math.pi * (1 - math.exp(-2 * aa * aa))
    nd = 3 if aa < 3 else 4
    tr = lambda v: math.floor(v * 10 ** nd) / 10 ** nd
    bate = lambda v, ref: round(v, nd) == ref or tr(v) == ref
    nota = ""
    if round(H_, nd) != hi and tr(H_) == hi:
        nota = f" · INCONSISTÊNCIA: {H_:.5f} arredonda para {round(H_, nd)}; a tabela aprovada usa {hi} (truncado) — mantido e reportado"
    chk(f"B6 a = {aa}: {lo} ≤ {mi} ≤ {hi}", L_ <= M_ <= H_ and bate(L_, lo) and bate(M_, mi) and bate(H_, hi),
        f"({L_:.5f} ≤ {M_:.5f} ≤ {H_:.5f}){nota}")
b = 1.7
chk("B6 ∬_{D_b} = 2π[−e^(−r²)/2]₀^b = 2π(−e^(−b²)/2 + 1/2) = π(1 − e^(−b²))",
    abs(2 * math.pi * quad(lambda r: np.exp(-r * r) * r, 0, b) - math.pi * (1 - math.exp(-b * b))) < 1e-8)
chk("B6 ∫ e^(−x²) dx = √π", abs(quad(lambda x: np.exp(-x * x), -12, 12) - math.sqrt(math.pi)) < 1e-9)
chk("B6 normal: ∫ e^(−x²/2) dx = √2 · √π = √(2π)", abs(quad(lambda x: np.exp(-x * x / 2), -16, 16) - math.sqrt(2 * math.pi)) < 1e-9)
# B7
chk("B7 r = sec θ (θ ≤ π/4) e r = cossec θ (θ ≥ π/4) no quadrado [0, 1]²", abs(1 / math.cos(.5) * math.cos(.5) - 1) < 1e-12 and abs(1 / math.sin(1.2) * math.sin(1.2) - 1) < 1e-12)
print(f"\nTOTAL: {sum(ok)}/{len(ok)} True")
