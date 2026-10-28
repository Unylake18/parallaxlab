"""QA físico do v1 (sem render): confere os números congelados do handoff §3 nos módulos das seções e mede P(t) e a soma com a Terra."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec_t7 as t7, sec_t8 as t8, sec_t9 as t9, sec_t10 as t10, sec_e6 as e6, sec_e7 as e7, sec_e8 as e8, sec_e9 as e9, sec_coda as cd  # noqa

print("T7 matriz: pares", t7.PARES, "→ células acesas", sorted({(i, j) for i, j in t7.PARES} | {(j, i) for i, j in t7.PARES}),
      "(6 = cada par duas vezes; todas apagadas para opacidade 0,13; diagonal vazia)")
print(f"T8: f_pedra={t8.F_PED:.0f} N; f_chão={t8.F_CHAO:.0f} N; resultante={t8.F_CHAO - t8.F_PED:.0f} N; a={t8.A_SIS:.2f} m/s²; "
      f"T={t8.TENS:.0f} N; cavalo={t8.RES_CAV:.0f} N (= 600·0,32 = {600 * t8.A_SIS:.0f}); gelo={t8.F_GELO:.0f} N")
ts = np.linspace(0, 1.2, 120001)
P = np.array([t9.P(t) for t in ts])
i = P.argmin()
z = ts[np.argmax((ts > 0.6) & (np.abs(P) < 1e-9))]
soma = P + (-P)
print(f"T9: P mín = {P[i]:.4f} kg·m/s em t = {ts[i]:.4f} s (t2 = {t9.T2:.4f}); P volta a 0 em t = {z:.4f} s (t1 = {t9.T1:.4f}); "
      f"max|P + P_Terra| = {np.abs(soma).max():.1e}; leve {t9.x1(9):.4f} m; pesado {t9.x2(9):.4f} m; Terra {1 * 14 / 5.97e24:.2e} m/s")
print(f"T10: K = {t10.K1:.0f} J e {t10.K2:.0f} J; fração do leve {t10.K1 / (t10.K1 + t10.K2):.3f}")
print(f"E6: agarra {e6.V_AG:.4f} m/s, K {e6.K_AG:.3f} J (calor {e6.K0 - e6.K_AG:.2f} J); rebate {e6.V_RB:.4f} m/s, K {e6.K_RB_B:.2f} + {e6.K_RB_V:.3f} J")
print(f"E7: {e7.V_H:.4f} m/s; 56°: {e7.V_56:.4f} m/s; K bala {e7.KB:.1f} J; K caçador {e7.KCZ:.4f} J; razão {e7.KB / e7.KCZ:.0f}; "
      f"na bala {100 * e7.KB / (e7.KB + e7.KCZ):.4f}%")
print(f"E8: v_bala = {e8.VB:.2f} m/s; p_bala {e8.PB:.3f}; p_rifle {e8.PR:.2f}; p_gases {e8.PG:.3f} kg·m/s")
print(f"E9: 45° → {np.degrees(e9.T2):.2f}° (n = {e9.N_AGUA})")
print(f"Coda: {cd.P_ABS * 1e6:.2f} μPa; {cd.P_REF * 1e6:.2f} μPa; vela {cd.F_VELA * 1e3:.3f} mN; laser {cd.F_LASER * 1e9:.2f} nN")
txt = "".join(p.read_text(encoding="utf-8") for p in Path(__file__).parent.glob("sec_*.py"))
print("E9 sem '= n12' em MathTex:", "n_{12}" not in txt and "n_{1" not in txt)
