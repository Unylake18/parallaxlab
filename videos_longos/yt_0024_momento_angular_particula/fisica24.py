"""yt_0024 — física da mesa com furo (handoff v1 §4.7) e conferência do Anexo B. Fonte única das posições do disco no 3D e no Manim.

Unidades SI; origem no centro do furo, tampo em z = 0, z para cima; giro anti-horário visto de cima (θ cresce).
- puxada (H2, B6): m = 0,20 kg; r0 = 0,60 m, v0 = 1,50 m/s (ω0 = 2,50 rad/s); v_r com rampa de cosseno de 0,15 s até −0,30 m/s,
  constante, rampa de 0,15 s até zero; termina em r = 0,30 m (1,15 s). θ̇ = L/(m r²) com L = 0,180 kg·m²/s (dt = 1e-4 s).
- reta (B2): disco livre, 1,50 m/s em +x ao longo de y = +0,40 m, de x = −0,75 a +0,75 m.
- círculo acelerado (B4): r = 0,60 m, F_t = 0,30 N por 1,0 s (α = 2,5 rad/s²): ω 2,5 → 5,0 rad/s.
uso: python fisica24.py → mesa_tab.json + conferência impressa (e renders/fisica_conferencia.txt)."""
import json
import math
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
G = 9.8
M = 0.20
R0, R1 = 0.60, 0.30
V0 = 1.50
W0 = V0 / R0                    # 2,5 rad/s
LZ = M * R0 * V0                # 0,180 kg·m²/s
VR = 0.30                       # m/s (fase constante)
TR = 0.15                       # s (cada rampa)
DT = 1e-4
FPS = 15


def _vr(t, t_const):
    """v_r(t) (≤ 0) da puxada iniciada em t = 0: rampa de cosseno, constante por t_const, rampa de volta."""
    if t <= 0:
        return 0.0
    if t < TR:
        return -VR * 0.5 * (1 - math.cos(math.pi * t / TR))
    if t < TR + t_const:
        return -VR
    if t < 2 * TR + t_const:
        u = t - TR - t_const
        return -VR * 0.5 * (1 + math.cos(math.pi * u / TR))
    return 0.0


T_CONST = (R0 - R1 - VR * TR) / VR          # 0,85 s (cada rampa anda VR·TR/2)
T_PUX = 2 * TR + T_CONST                    # 1,15 s


def _integra():
    n = int(round(T_PUX / DT)) + 1
    t = np.arange(n) * DT
    vr = np.array([_vr(x, T_CONST) for x in t])
    r = np.empty(n)
    th = np.empty(n)
    r[0], th[0] = R0, 0.0
    for i in range(1, n):                     # trapézio em r; θ̇ = L/(m r²) com r do meio do passo
        r[i] = r[i - 1] + 0.5 * (vr[i - 1] + vr[i]) * DT
        rm = 0.5 * (r[i] + r[i - 1])
        th[i] = th[i - 1] + LZ / (M * rm * rm) * DT
    return t, r, th, vr


TAB_T, TAB_R, TAB_TH, TAB_VR = _integra()
TH_PUX = float(TAB_TH[-1])                  # ângulo varrido durante a puxada (rad)
W1 = LZ / (M * R1 * R1)                     # 10,0 rad/s


def puxada(t):
    """Estado da puxada t s depois do início (t < 0: órbita de r0; t > T_PUX: órbita de r1). θ contínuo."""
    if t <= 0:
        r, th, vr = R0, W0 * t, 0.0
    elif t >= T_PUX:
        r, th, vr = R1, TH_PUX + W1 * (t - T_PUX), 0.0
    else:
        i = t / DT
        k = min(len(TAB_T) - 2, int(i))
        f = i - k
        r = TAB_R[k] * (1 - f) + TAB_R[k + 1] * f
        th = TAB_TH[k] * (1 - f) + TAB_TH[k + 1] * f
        vr = TAB_VR[k] * (1 - f) + TAB_VR[k + 1] * f
    r, th, vr = float(r), float(th), float(vr)
    w = LZ / (M * r * r)
    vth = w * r
    I = M * r * r
    Idot = 2 * M * r * vr
    alfa = -Idot * w / I
    K = 0.5 * M * (vr * vr + vth * vth)
    return dict(t=t, r=r, th=th, x=r * math.cos(th), y=r * math.sin(th), vr=vr, vth=vth, w=w, I=I, Idot=Idot, alfa=alfa, L=M * r * vth, K=K,
                zp=-(R0 - r))


def tracao_rdd0(r):
    """Tração com r̈ = 0 (B6-9): T = L²/(m r³)."""
    return LZ * LZ / (M * r ** 3)


# ── reta (B2) ──
RETA_Y, RETA_V, RETA_X0, RETA_X1 = 0.40, 1.50, -0.75, 0.75
O1, O2, O3 = (-0.30, 0.40), (0.0, 0.0), (0.30, 0.80)


def reta(t):
    x = RETA_X0 + RETA_V * t
    return dict(x=x, y=RETA_Y)


def Lz_ponto(px, py, x, y, vx, vy, m=M):
    return m * ((x - px) * vy - (y - py) * vx)


# ── círculo acelerado (B4) ──
FT, T_EMP = 0.30, 1.0
ALFA_B4 = FT * R0 / (M * R0 * R0)            # 2,5 rad/s²


def circulo(t, t_emp=None):
    """Órbita de r0 com ω0; empurrão tangencial de 1,0 s começando em t_emp (None = sem empurrão)."""
    if t_emp is None or t <= t_emp:
        return dict(th=W0 * t, w=W0)
    u = min(t - t_emp, T_EMP)
    th = W0 * t + 0.5 * ALFA_B4 * u * u + (ALFA_B4 * T_EMP * (t - t_emp - T_EMP) if t - t_emp > T_EMP else 0.0)
    return dict(th=th, w=W0 + ALFA_B4 * u)


# ── pedra (B3) ──
M_PEDRA, D_PEDRA, T_QUEDA = 0.50, 0.40, 0.60

# ── Kepler (B5-5) ──
A_ELI, E_ELI = 2.6, 0.6


def kepler_pontos(n=12):
    """Pontos de mesmo tempo na elipse (foco na origem): M = E − e sen E, M_k = 2πk/n."""
    out = []
    for k in range(n):
        Mk = 2 * math.pi * k / n
        E = Mk
        for _ in range(60):
            E -= (E - E_ELI * math.sin(E) - Mk) / (1 - E_ELI * math.cos(E))
        b = A_ELI * math.sqrt(1 - E_ELI ** 2)
        out.append((A_ELI * (math.cos(E) - E_ELI), b * math.sin(E)))
    return out


def conferencia():
    linhas = []
    ok = True

    def c(nome, val, alvo, tol):
        nonlocal ok
        bom = abs(val - alvo) <= tol
        ok &= bom
        linhas.append(f"[{'OK ' if bom else 'FALHA'}] {nome}: {val:.5g} (alvo {alvo:g} ± {tol:g})")
    c("T_PUX (s)", T_PUX, 1.15, 1e-9)
    c("r final (m)", float(TAB_R[-1]), R1, 1e-4)
    c("ω final (rad/s)", LZ / (M * TAB_R[-1] ** 2), 10.0, 0.05)
    Ls = M * TAB_R ** 2 * np.gradient(TAB_TH, DT)
    c("L máx desvio relativo na puxada", float(np.max(np.abs(Ls / LZ - 1))), 0.0, 0.005)
    linhas.append(f"[NOTA] voltas na puxada: {TH_PUX / (2 * math.pi):.3f} (Anexo B: ≈ 0,8; integração exata dá 0,94; número fora da tela e da fala)")
    e = puxada(TR + (R0 - VR * TR / 2 - 0.45) / VR)
    c("r em B6-3 (m)", e["r"], 0.45, 1e-4)
    c("I em 0,45 (kg m²)", e["I"], 0.0405, 1e-5)
    c("ω em 0,45 (rad/s)", e["w"], 4.444, 0.001)
    c("v_θ em 0,45 (m/s)", e["vth"], 2.00, 1e-3)
    c("İ em 0,45", e["Idot"], -0.054, 1e-4)
    c("İω em 0,45", e["Idot"] * e["w"], -0.240, 1e-3)
    c("α em 0,45 (rad/s²)", e["alfa"], 5.93, 0.01)
    c("ângulo v × tangente em 0,45 (°)", math.degrees(math.atan2(-e["vr"], e["vth"])), 8.5, 0.05)
    c("T em 0,45 com r̈ = 0 (N)", tracao_rdd0(0.45), 1.78, 0.005)
    c("P em 0,45 (W)", tracao_rdd0(0.45) * VR, 0.53, 0.005)
    c("T em 0,60 (N)", tracao_rdd0(0.60), 0.75, 1e-9)
    c("T em 0,30 (N)", tracao_rdd0(0.30), 6.0, 1e-9)
    c("K0 (J)", 0.5 * M * V0 ** 2, 0.225, 1e-9)
    c("Kf (J)", 0.5 * M * (W1 * R1) ** 2, 0.900, 1e-9)
    c("dA/dt puxada (m²/s)", LZ / (2 * M), 0.450, 1e-9)
    c("área por 0,20 s (m²)", LZ / (2 * M) * 0.20, 0.090, 1e-9)
    c("L_z em O2 (reta)", Lz_ponto(*O2, 0, RETA_Y, RETA_V, 0), -0.12, 1e-9)
    c("L_z em O3 (reta)", Lz_ponto(*O3, 0, RETA_Y, RETA_V, 0), +0.12, 1e-9)
    c("L_z em O1 (reta)", Lz_ponto(*O1, 0, RETA_Y, RETA_V, 0), 0.0, 1e-9)
    c("área por 0,50 s na reta (m²)", 0.5 * RETA_V * 0.5 * RETA_Y, 0.150, 1e-9)
    c("dA/dt reta (m²/s)", 0.12 / (2 * M), 0.30, 1e-9)
    c("τ_z pedra (N m)", -M_PEDRA * G * D_PEDRA, -1.96, 1e-9)
    c("L_z pedra em 0,60 s", -M_PEDRA * G * D_PEDRA * T_QUEDA, -1.176, 1e-9)
    c("queda em 0,60 s (m)", 0.5 * G * T_QUEDA ** 2, 1.764, 1e-9)
    c("I B4 (kg m²)", M * R0 ** 2, 0.072, 1e-9)
    c("τ B4 (N m)", FT * R0, 0.18, 1e-9)
    c("α B4", ALFA_B4, 2.5, 1e-9)
    c("ω B4 após 1 s", circulo(5.0, 4.0)["w"], 5.0, 1e-9)
    c("L B4 após 1 s", M * R0 ** 2 * 5.0, 0.36, 1e-9)
    c("aliasing máx a 15 fps (°/quadro) em r1", math.degrees(W1 / FPS), 38.2, 0.1)
    return ok, linhas


def tabela():
    """mesa_tab.json: por quadro (15 fps) da puxada (−2 s … T_PUX + 2 s, tempo físico), estado do disco e do puxador."""
    q = []
    for f in range(-2 * FPS, int(round((T_PUX + 2) * FPS)) + 1):
        e = puxada(f / FPS)
        q.append({k: round(v, 6) for k, v in e.items()} | {"T_rdd0": round(tracao_rdd0(e["r"]), 5) if abs(e["vr"] + VR) < 1e-9 or e["vr"] == 0 else None})
    return q


if __name__ == "__main__":
    ok, lin = conferencia()
    print("\n".join(lin))
    print("CONFERÊNCIA", "OK" if ok else "FALHA")
    (U / "renders").mkdir(exist_ok=True)
    (U / "renders" / "fisica_conferencia.txt").write_text("\n".join(lin) + f"\nCONFERÊNCIA {'OK' if ok else 'FALHA'}\n", encoding="utf-8")
    (U / "mesa_tab.json").write_text(json.dumps(dict(fps=FPS, m=M, L=LZ, r0=R0, r1=R1, T_puxada=T_PUX, puxada=tabela(),
                                                     nota="tempo físico; as cenas usam a mesma função puxada(t) (câmera lenta = t/2)"), indent=0), encoding="utf-8")
