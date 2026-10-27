"""QA físico da rodada final do yt_0005 (rodar: uv run python qa_fisica_rodada_final.py).

1) Sinais de q: integra dv/dt = (qB/m)(v_z, -v_y) (RK4) e compara com as soluções analíticas e com a classe Orbit da cena.
2) Módulo constante, raio, período e passo.
3) Primitiva de sen por derivação numérica.
4) Analisador (B08): semicircunferência dentro da região magnética, para q > 0 e q < 0.
"""
import importlib.util
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CENA = os.path.abspath(os.path.join(HERE, "..", "..", "cena.py"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..")))
spec = importlib.util.spec_from_file_location("cena", CENA)
cena = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cena)

ok = True


def check(nome, cond, extra=""):
    global ok
    ok &= bool(cond)
    print(("OK   " if cond else "FALHA"), nome, extra)


M, B, VP = cena.MASS, cena.BM, cena.VP1
OM = cena.OMEGA
R = M * VP / (cena.ABSQ * B)

for s in (+1, -1):
    q = s * cena.ABSQ
    w = q * B / M
    # integra dv_y/dt = w v_z ; dv_z/dt = -w v_y ; dy/dt = v_y ; dz/dt = v_z
    def f(u):
        return np.array([w * u[1], -w * u[0], u[0], u[1]])
    u = np.array([0.0, VP, 0.0, 0.0])
    dt, T = 1e-3, 2 * math.pi / abs(w)
    err_v, err_mod, err_pos = 0.0, 0.0, 0.0
    t = 0.0
    for _ in range(int(T / dt)):
        k1 = f(u); k2 = f(u + dt / 2 * k1); k3 = f(u + dt / 2 * k2); k4 = f(u + dt * k3)
        u = u + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += dt
        vy_a, vz_a = s * VP * math.sin(abs(w) * t), VP * math.cos(abs(w) * t)
        y_a, z_a = s * R * (1 - math.cos(abs(w) * t)), R * math.sin(abs(w) * t)
        err_v = max(err_v, abs(u[0] - vy_a), abs(u[1] - vz_a))
        err_mod = max(err_mod, abs(math.hypot(u[0], u[1]) - VP))
        err_pos = max(err_pos, abs(u[2] - y_a), abs(u[3] - z_a))
    check(f"q{'>' if s > 0 else '<'}0: v_y = {'+' if s > 0 else '-'}v⊥ sen(ωt), v_z = v⊥ cos(ωt)", err_v < 1e-6, f"(erro máx {err_v:.1e})")
    check(f"q{'>' if s > 0 else '<'}0: |v| constante", err_mod < 1e-6, f"(erro {err_mod:.1e})")
    check(f"q{'>' if s > 0 else '<'}0: y−y0 = {'+' if s > 0 else '-'}R(1−cos), z−z0 = R sen", err_pos < 1e-5, f"(erro {err_pos:.1e})")
    # classe Orbit da cena (mesma convenção: horizontal = y, vertical = z)
    clock = type("C", (), {"get_value": lambda self: 0.0})()
    o = cena.Orbit(VP, 0.0, s, clock, 0.0, "#fff")
    e = 0.0
    for uu in np.linspace(0, o.R * 0 + cena.T_PER, 200):
        v = o.vel(uu)
        e = max(e, abs(v[0] - s * VP * math.sin(OM * uu)), abs(v[1] - VP * math.cos(OM * uu)))
        e = max(e, abs(math.hypot(v[0], v[1]) - VP))
        F = o.force(uu)
        # F = q v×B com B = ẑ(mundo) → F_x = q v_y B, F_y = -q v_x B ; aqui (x,y) do desenho
        e = max(e, abs(F[0] - s * v[1] * B), abs(F[1] + s * v[0] * B))
    check(f"Orbit(s={s:+d}) coerente com a solução, o módulo e F = q v×B", e < 1e-9, f"(erro {e:.1e})")
    check(f"R = m v⊥/(|q|B) e T = 2π m/(|q|B) (s={s:+d})", abs(o.R - R) < 1e-12 and abs(cena.T_PER - 2 * math.pi * M / (cena.ABSQ * B)) < 1e-12)

# passo da hélice p = |v∥| T = 2π m |v∥|/(|q|B)
p = cena.VPAR * cena.T_PER
check("passo p = 2π m v∥/(|q|B)", abs(p - 2 * math.pi * M * cena.VPAR / (cena.ABSQ * B)) < 1e-12, f"(p = {p:.3f})")

# primitiva: d/dt[-cos(ωt)/ω + C] = sen(ωt)
w = OM
t = np.linspace(0.1, 4, 50)
h = 1e-6
d = (-(np.cos(w * (t + h))) / w - (-(np.cos(w * (t - h))) / w)) / (2 * h)
check("primitiva: d/dt[−cos(ωt)/ω + C] = sen(ωt)", np.max(np.abs(d - np.sin(w * t))) < 1e-6)
# integral com limites: ∫0^t v⊥ sen(ωt') dt' = (v⊥/ω)(1 − cos ωt)
tt = 3.3
xs = np.linspace(0, tt, 200001)
val = np.trapezoid(VP * np.sin(w * xs), xs)
check("∫0^t v⊥ sen = (v⊥/ω)(1−cos ωt)", abs(val - VP / w * (1 - math.cos(w * tt))) < 1e-8)

# analisador B08: semicircunferência dentro da região B (x ∈ [-1.5, 0.6], |y| ≤ 2.6) para q > 0 e q < 0
class Fake:
    pass


for sg in (+1, -1):
    fake = Fake()
    fake.mode7 = "arc"
    fake.qs7 = type("Q", (), {"get_value": lambda self, sg=sg: float(sg)})()
    pos = lambda s_: cena.YT0005MagnetostaticaM1.beam_pos(fake, s_)
    L = cena.YT0005MagnetostaticaM1.beam_len(fake)
    pts = np.array([pos(L * i / 400) for i in range(401)])
    straight = pts[pts[:, 0] < -1.5 - 1e-9]
    inreg = pts[pts[:, 0] >= -1.5 - 1e-9]
    fora = np.any(pts[:, 0] < -1.5 - 1e-6) and True
    arc = np.array([pos(2.5 + (L - 2.5) * i / 200) for i in range(201)])
    dentro = np.all((arc[:, 0] >= -1.5 - 1e-9) & (arc[:, 0] <= 0.6) & (np.abs(arc[:, 1]) <= 2.6))
    meio = np.array(pos(2.5 + (L - 2.5) / 2))
    saida = np.array(pos(L))
    check(f"B08 q{'>' if sg > 0 else '<'}0: arco inteiramente dentro da região", dentro)
    check(f"B08 q{'>' if sg > 0 else '<'}0: trecho reto fora do campo", np.all(straight[:, 1] == 0.0))
    check(f"B08 q{'>' if sg > 0 else '<'}0: saída em x=−1.5, y = {-sg * 2 * cena.R8:+.1f} (semicircunferência de raio R)",
          abs(saida[0] + 1.5) < 1e-9 and abs(saida[1] - (-sg * 2 * cena.R8)) < 1e-9)
    check(f"B08 q{'>' if sg > 0 else '<'}0: curva para {'baixo' if sg > 0 else 'cima'} (centro do lado de F = q v×B)", np.sign(meio[1]) == -sg)

print("\nRESULTADO:", "TUDO OK" if ok else "HÁ FALHAS")
sys.exit(0 if ok else 1)
