"""QA numérico do B06 (independente do render): Q_int, dQ/dt e portadores saem do MESMO balanço.

Reproduz o roteiro real de b06_volume (rampas `smooth` de I_ent / I_sai e esperas), roda o modelo `BalancoB06` do cena.py quadro a
quadro (30 fps, como o updater do Manim) e compara com a integral analítica de referência
    Q_ref(t) = Q0 + S_PHYS · ∫0^t (I_ent − I_sai) dτ            (S_PHYS = 0,11 s físico por s de tela).
Uso:  uv run python videos_longos/yt_0005_magnetostatica_forca_lorentz/qa/qa_b06.py
"""
import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
from manim import smooth

U = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cena_yt0005", U / "cena.py")
cena = importlib.util.module_from_spec(spec)
sys.modules["cena_yt0005"] = cena
spec.loader.exec_module(cena)
BalancoB06 = cena.BalancoB06

FPS = 30.0
DT = 1.0 / FPS
# (duração s, tipo, tracker, valor final) — o mesmo roteiro de b06_volume: espera, rampa de I_sai, espera, retorno, espera, rampa de I_ent...
ROT = [(1.6, "hold"), (1.5, "ramp", "out", 2.0), (5.2, "hold"), (1.2, "ramp", "out", 1.0), (0.8, "hold"),
       (1.5, "ramp", "in", 2.0), (5.2, "hold"), (1.2, "ramp", "in", 1.0), (0.6, "hold"), (4.0, "hold")]


def schedule(t):
    """(I_ent, I_sai) em t segundos de tela (rampas com a mesma `smooth` do Manim)."""
    cur = {"in": 1.0, "out": 1.0}
    t0 = 0.0
    for seg in ROT:
        d = seg[0]
        if t < t0 + d or seg is ROT[-1]:
            if seg[1] == "ramp":
                a = min(1.0, max(0.0, (t - t0) / d))
                cur[seg[2]] = cur[seg[2]] + (seg[3] - cur[seg[2]]) * smooth(a)
            return cur["in"], cur["out"]
        if seg[1] == "ramp":
            cur[seg[2]] = seg[3]
        t0 += d
    return cur["in"], cur["out"]


T_TOT = sum(s[0] for s in ROT)
# integral de referência (passo fino, independente do passo de 1/30 s do modelo)
tt = np.arange(0.0, T_TOT + 1e-9, 1e-4)
rate = np.array([schedule(t)[0] - schedule(t)[1] for t in tt])
cum = np.concatenate([[0.0], np.cumsum((rate[1:] + rate[:-1]) * 0.5 * 1e-4)])
Q0 = 1.0
Qref = lambda t: Q0 + cena.BalancoB06().s_phys * np.interp(t, tt, cum)

m = BalancoB06(q0=Q0)
n = int(round(T_TOT * FPS))
ts, Qs, Ns = [], [], []
prev_s = {}
violacoes = []
for i in range(n + 1):
    t = i * DT
    ts.append(t)
    Qs.append(m.q())
    Ns.append(m.A - m.B)
    # portadores: s em [0,1], só entram em s≈0 e só saem em s≈1, avançam sempre (nunca somem no interior)
    cur_s = dict(m.particles())
    for k, s_ in cur_s.items():
        if not (-1e-9 <= s_ <= 1 + 1e-9):
            violacoes.append(("s fora de [0,1]", t, k, s_))
        if k in prev_s and s_ < prev_s[k] - 1e-9:
            violacoes.append(("portador recuou", t, k, prev_s[k], s_))
    for k, s0 in prev_s.items():
        if k not in cur_s and s0 < 0.9:
            violacoes.append(("portador sumiu no interior", t, k, s0))
    for k, s_ in cur_s.items():
        if k not in prev_s and i > 0 and s_ > 0.1:
            violacoes.append(("portador nasceu no interior", t, k, s_))
    prev_s = cur_s
    i_in, i_out = schedule(t)
    m.step(i_in, i_out, DT)
ts, Qs = np.array(ts), np.array(Qs)

linhas = []
ok = True


def check(nome, cond, det):
    global ok
    ok &= bool(cond)
    linhas.append("%s  %s  %s" % ("OK " if cond else "FALHA", nome, det))


# 1) Q(t) contra a integral de referência em TODO o roteiro
err = np.max(np.abs(Qs - Qref(ts)))
check("Q(t) = Q0 + S_PHYS ∫(I_ent − I_sai)dt", err < 4e-3, "erro máximo %.2e C (tol 4e-3)" % err)

# 2) variações Q(t2) − Q(t1) em janelas dos quatro estados e das transições (fronteiras reais do roteiro:
#    espera 0–1,6 · rampa I_sai 1,6–3,1 · espera 3,1–8,3 · retorno 8,3–9,5 · espera 9,5–10,3 · rampa I_ent 10,3–11,8 ·
#    espera 11,8–17,0 · retorno 17,0–18,2 · espera 18,2–18,8 · espera final 18,8–22,8)
jan = {"I_ent = I_sai (inicial)": (0.2, 1.5), "rampa I_sai 1→2": (1.6, 3.1), "I_sai > I_ent (estável)": (3.5, 8.2),
       "retorno I_sai → 1": (8.3, 9.5), "equilíbrio recuperado": (9.8, 10.3), "rampa I_ent 1→2": (10.3, 11.8),
       "I_ent > I_sai (estável)": (12.2, 16.9), "retorno I_ent → 1": (17.0, 18.2), "equilíbrio final": (18.4, 22.8)}
for nome, (a, b) in jan.items():
    dq = float(np.interp(b, ts, Qs) - np.interp(a, ts, Qs))
    ref = float(Qref(b) - Qref(a))
    check("ΔQ em '%s' [%.1f–%.1f s]" % (nome, a, b), abs(dq - ref) < 2.5e-3, "modelo %.4f · ∫ %.4f C" % (dq, ref))

# 3) estados qualitativos
def q_at(t):
    return float(np.interp(t, ts, Qs))


check("estado 1: I_ent = I_sai → Q constante", abs(q_at(1.5) - q_at(0.2)) < 1e-9, "ΔQ = %.2e" % (q_at(1.5) - q_at(0.2)))
check("estado 2: I_sai > I_ent → Q diminui", q_at(8.2) < q_at(3.5) - 0.3, "Q: %.3f → %.3f" % (q_at(3.5), q_at(8.2)))
check("estado 3: I_ent > I_sai → Q aumenta", q_at(16.9) > q_at(12.2) + 0.3, "Q: %.3f → %.3f" % (q_at(12.2), q_at(16.9)))
check("estado 4: retorno → dQ/dt = 0 e Q constante", abs(q_at(10.3) - q_at(9.8)) < 3e-3 and abs(q_at(22.8) - q_at(18.4)) < 3e-3,
      "ΔQ(9,8–10,3) = %.4f · ΔQ(18,4–22,8) = %.4f" % (q_at(10.3) - q_at(9.8), q_at(22.8) - q_at(18.4)))
check("sem saturação artificial (Q não trava durante I_sai > I_ent)", abs((q_at(8.2) - q_at(7.6)) / 0.6 - (-cena.BalancoB06().s_phys)) < 4e-3,
      "dQ/dt medido %.4f · esperado %.4f C/s de tela" % ((q_at(8.2) - q_at(7.6)) / 0.6, -cena.BalancoB06().s_phys))
check("sem saturação artificial (Q não trava durante I_ent > I_sai)", abs((q_at(16.9) - q_at(16.3)) / 0.6 - cena.BalancoB06().s_phys) < 4e-3,
      "dQ/dt medido %.4f · esperado %.4f C/s de tela" % ((q_at(16.9) - q_at(16.3)) / 0.6, cena.BalancoB06().s_phys))
check("Q nunca sai do intervalo físico (N ≥ 1 portador)", min(Ns) >= 1.0, "N mín = %.2f portadores (Q mín = %.3f C)" % (min(Ns), Qs.min()))
check("Q final volta a Q0 (excursões simétricas)", abs(Qs[-1] - Q0) < 4e-3, "Q final %.4f" % Qs[-1])

# 4) portadores: nenhum nasce/some no interior nem recua
check("portadores só entram na face de entrada, só saem na de saída e nunca recuam", not violacoes,
      "%d violações%s" % (len(violacoes), (" · ex.: %s" % (violacoes[0],)) if violacoes else ""))
# 5) contagem visual = Q·N0
cont = [len(BalancoB06.particles(mm)) for mm in []]  # (reservado)
mm = BalancoB06(q0=Q0)
dif = 0
for i in range(n + 1):
    t = i * DT
    dif = max(dif, abs(len(mm.particles()) - mm.q() * mm.n0))
    mm.step(*schedule(t), DT)
check("nº de portadores desenhados ≈ Q·N0 (diferença ≤ 1)", dif <= 1.0 + 1e-9, "diferença máxima %.2f portador" % dif)

linhas.append("")
linhas.append("S_PHYS = %.2f s físicos por s de tela · N0 = %d · R0 = %.2f portadores/s por unidade de corrente" %
              (BalancoB06().s_phys, BalancoB06().n0, BalancoB06().r0))
linhas.append("RESULTADO: %s" % ("TUDO OK" if ok else "FALHAS"))
txt = "\n".join(linhas)
sys.stdout.reconfigure(encoding="utf-8"); print(txt)
(Path(__file__).with_name("qa_b06.txt")).write_text(txt + "\n", encoding="utf-8")
sys.exit(0 if ok else 1)
