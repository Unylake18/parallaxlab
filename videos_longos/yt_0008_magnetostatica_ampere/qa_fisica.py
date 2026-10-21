"""QA numérico independente do 5.3 (μ0 = 1). uv run --no-sync python qa_fisica.py → imprime OK/FALHA por item."""
import math
import sys

import numpy as np

from fisica import (TAU, b_fio, b_cilindro, bphi_cilindro, circulacao, enlace_fio, rot_numerico, div_numerico, b_espira,
                    b_toroide)

rng = np.random.default_rng(3)
falhas = []


def ok(nome, cond, info=""):
    print(("OK    " if cond else "FALHA ") + nome + (f"  [{info}]" if info else ""))
    if not cond:
        falhas.append(nome)


# N02 · fio infinito: rot B = 0 e div B = 0 fora do eixo
pts = [rng.uniform(-3, 3, 3) for _ in range(40)]
pts = [p for p in pts if math.hypot(p[0], p[2]) > 0.3]
ok("N02 rot B = 0 para s>0", max(np.abs(rot_numerico(b_fio, p)).max() for p in pts) < 1e-5)
ok("N05 div B = 0 para s>0", max(abs(div_numerico(b_fio, p)) for p in pts) < 1e-5)
# N02 · (1/s) d/ds (s B_φ) = 0
s = np.linspace(0.3, 4, 50)
ok("N02 s·B_φ constante", np.ptp(s * (1 / (TAU * s))) < 1e-12)
# N03 · micro-loops em várias orientações: (1/A)∮ → 0
P = np.array([1.6, 0.0, 0.0])
vals = [circulacao(b_fio, P, 0.05, n) / (math.pi * 0.05 ** 2) for n in ([0, 1, 0], [1, 0, 0], [0, 0, 1], [1, 1, 1])]
ok("N03 (1/A)∮B·dℓ ≈ 0 em toda orientação", max(abs(v) for v in vals) < 1e-6, f"{max(abs(v) for v in vals):.1e}")
# N04 · laço que cresce: 0 enquanto não enlaça, I quando enlaça
for c, r, esp in [((1.6, 0, 0), 0.4, 0.0), ((0.5, 0, 0), 1.2, 1.0), ((0, 0, 0), 1.6, 1.0)]:
    v = circulacao(b_fio, c, r, [0, 1, 0], 4000)
    ok(f"N04 ∮B·dℓ centro {c} raio {r} = {esp}", abs(v - esp) < 1e-3 and enlace_fio(c, r) == esp, f"{v:.5f}")
# N11/N12 · cilindro: rot_y = μ0 J dentro, 0 fora; continuidade em s=a; fora = I/(2π s)
a = 0.8
Jv = 1 / (math.pi * a * a)
f = lambda p: b_cilindro(p, a)
ok("N11 (rot B)_y = μ0 J dentro", abs(rot_numerico(f, [0.3, 0, 0.2])[1] - Jv) < 1e-4, f"{rot_numerico(f, [0.3, 0, 0.2])[1]:.5f} vs {Jv:.5f}")
ok("N12 rot B = 0 fora", np.abs(rot_numerico(f, [1.5, 0, 0.4])).max() < 1e-5)
ok("N12 B contínuo em s=a", abs(bphi_cilindro(a - 1e-9, a) - bphi_cilindro(a + 1e-9, a)) < 1e-7)
ok("N12 C_ext = μ0 J a²/2 = μ0 I/(2π)", abs(Jv * a * a / 2 - 1 / TAU) < 1e-12)
ok("N11 regularidade: B(0) finito com C=0", bphi_cilindro(1e-9, a) < 1e-6)
# N13 · a→0 com I fixo: B externo não muda; J·πa² = I
ok("N13 B externo independe de a", abs(bphi_cilindro(2.0, 0.8) - bphi_cilindro(2.0, 0.05)) < 1e-12)
ok("N13 circulação interna total = μ0 I para qualquer a", all(abs(circulacao(lambda p, aa=aa: b_cilindro(p, aa), [0, 0, 0], 1.2, [0, 1, 0], 2000) - 1) < 1e-3 for aa in (0.8, 0.3, 0.05)))
# N09 · fluxo de R/R³ por esfera = 4π (qualquer raio)
for rad in (0.1, 1.0, 5.0):
    N = 200
    tot = 0.0
    for i in range(N):
        th = math.pi * (i + 0.5) / N
        for j in range(2 * N):
            ph = math.pi * (j + 0.5) / N
            n = np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)])
            F = rad * n / rad ** 3
            tot += F @ n * rad * rad * math.sin(th) * (math.pi / N) ** 2
    ok(f"N09 ∮(R/R³)·da = 4π (R={rad})", abs(tot - 4 * math.pi) < 1e-3, f"{tot:.5f}")
# N06 · F = −∇(1/R): ∇×F = 0
F = lambda p: np.asarray(p) / np.linalg.norm(p) ** 3
ok("N06 ∇×(R/R³) = 0", max(np.abs(rot_numerico(F, p)).max() for p in pts) < 1e-4)
ok("N09 ∇·(R/R³) = 0 para R≠0", max(abs(div_numerico(F, p)) for p in pts) < 1e-4)
# N10 · F(r−r'): ∂F/∂x = −∂F/∂x'
r, rp, h = np.array([0.7, 0.2, -0.4]), np.array([-0.3, 0.5, 0.1]), 1e-5
dx = (F(r + [h, 0, 0] - rp) - F(r - [h, 0, 0] - rp)) / (2 * h)
dxp = (F(r - (rp + [h, 0, 0])) - F(r - (rp - [h, 0, 0]))) / (2 * h)
ok("N10 ∇F = −∇'F", np.abs(dx + dxp).max() < 1e-6)
# N17 · fio por Ampère: B 2πs = μ0 I
ok("N17 B(2πs) = μ0 I", abs(np.linalg.norm(b_fio([1.3, 0, 0])) * TAU * 1.3 - 1) < 1e-12)
# N18 · lâmina (fios lado a lado): B ≈ μ0 K/2, paralelo à lâmina, sentidos opostos
K, Nw, Lh = 1.0, 4001, 400.0
xs = np.linspace(-Lh, Lh, Nw)
Iw = K * (xs[1] - xs[0])
# lâmina no plano y=0 do 2D (x horizontal, y vertical), correntes saindo da tela (+z): B de cada fio = I/(2π r) φ̂
def b_lamina(px, py):
    dxs, dys = px - xs, py - 0.0
    r2 = dxs ** 2 + dys ** 2
    return np.array([np.sum(-Iw * dys / (TAU * r2)), np.sum(Iw * dxs / (TAU * r2))])
bc, bb = b_lamina(0.3, 1.0), b_lamina(0.3, -1.0)
ok("N18 B = μ0K/2 acima (−x) e abaixo (+x)", abs(bc[0] + 0.5) < 2e-3 and abs(bb[0] - 0.5) < 2e-3 and abs(bc[1]) < 2e-3, f"{bc}, {bb}")
# N19 · solenoide longo (espiras): dentro ≈ n I, fora ≈ 0, uniforme
R, n_esp, Lsol = 1.0, 20, 40.0
ys = np.arange(-Lsol / 2, Lsol / 2, 1 / n_esp)
def b_sol(p):
    return sum(b_espira(p, R, y0, 1.0, 120) for y0 in ys)
bi, bi2, bo = b_sol([0, 0, 0]), b_sol([0.6, 0, 0]), b_sol([1.8, 0, 0])
ok("N19 B dentro ≈ μ0 n I e uniforme", abs(bi[1] / n_esp - 1) < 5e-3 and abs(bi2[1] / n_esp - 1) < 5e-3, f"{bi[1] / n_esp:.4f}, {bi2[1] / n_esp:.4f}")
ok("N19 B fora ≈ 0 (solenoide longo)", abs(bo[1]) / n_esp < 2e-3, f"{bo[1] / n_esp:.1e}")
ok("N19 sentido: corrente +φ em torno de +y → B dentro +y", bi[1] > 0)
# N20 · toroide ideal: 0 em s<a e s>b; NI/(2πs) entre
ok("N20 B(s) toroide", b_toroide(0.5, 1, 2, 10) == 0 and b_toroide(3, 1, 2, 10) == 0 and abs(b_toroide(1.5, 1, 2, 10) - 10 / (TAU * 1.5)) < 1e-12)
# N06–N10 · região de corrente: J tangente às elipses desenhadas e ∇'·J = 0
from fisica import J_at, BLOB_C, BLOB_A, BLOB_B
tang = []
for k in (0.35, 0.65, 0.92, 0.999):
    for t in np.linspace(0, TAU, 25)[:-1]:
        p = BLOB_C + k * np.array([BLOB_A * math.cos(t), BLOB_B * math.sin(t)])
        n = np.array([math.cos(t) / BLOB_A, math.sin(t) / BLOB_B])
        j = J_at(*p)
        tang.append(abs(j @ n) / (np.linalg.norm(j) * np.linalg.norm(n)))
ok("N06 J tangente às elipses (J·n̂ = 0, inclusive na borda)", max(tang) < 1e-12, f"{max(tang):.1e}")
hh = 1e-5
divs = [abs((J_at(x + hh, y)[0] - J_at(x - hh, y)[0]) / (2 * hh) + (J_at(x, y + hh)[1] - J_at(x, y - hh)[1]) / (2 * hh))
        for x, y in rng.uniform([-1.3, -0.9], [0.9, 0.5], (30, 2)) if ((x - BLOB_C[0]) / BLOB_A) ** 2 + ((y - BLOB_C[1]) / BLOB_B) ** 2 < 0.9]
ok("N07 ∇'·J = 0 na região", max(divs) < 1e-6, f"{max(divs):.1e}")
# N11 · sonda local do fio finito (V5): a sonda inicial fica INTEIRA dentro do condutor e le exatamente mu0 J
a_f, pr_f, zc, s0_f = 0.75, 0.14, 0.25, 0.25
alcance = math.hypot(s0_f, zc) + pr_f
ok("N11 sonda inicial inteira dentro do fio (alcance < a)", alcance < a_f, f"{alcance:.3f} < {a_f}")
Jf = 1 / (math.pi * a_f ** 2)
lei = circulacao(lambda q: b_cilindro(q, a_f), [s0_f, 0, zc], pr_f, [0, 1, 0], 240) / (math.pi * pr_f ** 2) / Jf
ok("N11 leitura da sonda dentro = mu0 J (1.000)", abs(lei - 1.0) < 1e-6, f"{lei:.6f}")
fora = circulacao(lambda q: b_cilindro(q, a_f), [1.55, 0, zc], pr_f, [0, 1, 0], 240) / (math.pi * pr_f ** 2) / Jf
ok("N11 leitura da sonda fora = 0", abs(fora) < 1e-3, f"{fora:.1e}")
cruza = circulacao(lambda q: b_cilindro(q, a_f), [0.7, 0, zc], pr_f, [0, 1, 0], 240) / (math.pi * pr_f ** 2) / Jf
ok("N11 leitura parcial na fronteira entre 0 e 1", 0.0 < cruza < 1.0, f"{cruza:.3f}")
# N12/N13 · grafico: familia C/s passa por B(a) so para C = Cext; pico a->0 acima do teto do grafico
ok("N12 continuidade em s=a: C_ext = mu0 J a^2/2 = mu0 I/(2 pi)", abs(Jf * a_f ** 2 / 2 - 1 / (TAU)) < 1e-12)
ok("N13 pico B(a) = 1/(2 pi a) > teto do grafico para a = 0,05", (1 / (TAU * 0.05)) / (1 / (TAU * 0.75)) > 1.15)
# N09 · F = R/R^3: |F| = 1/R^2 (fluxo 4 pi independe do raio)
for Rr in (0.5, 1.0, 2.0):
    ok(f"N09 fluxo de F numa esfera de raio {Rr} = 4 pi", abs((1 / Rr ** 2) * 4 * math.pi * Rr ** 2 - 4 * math.pi) < 1e-12)
# espira: B no centro = μ0 I/(2R) em +y
bc = b_espira([0, 0, 0], 1.0)
ok("aux espira: B(0) = μ0 I/(2R), +y", abs(bc[1] - 0.5) < 1e-4)

print("\nTUDO OK" if not falhas else f"\n{len(falhas)} FALHA(S): {falhas}")
sys.exit(1 if falhas else 0)
