"""QA físico do v3 (sem render): importa as seções (cada uma tem `assert` com os números do handoff §3), imprime os valores,
confere o cavalo do T8 (tomada única: a = 0,32 de 0,30 a 3,5 m/s em 10 s; gelo a ≈ −1,26 até parar), o texto aprovado do T10 e procura referências a livro no texto de tela."""
import re
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import sec_t8 as t8, sec_t9 as t9, sec_t10 as t10, sec_e6 as e6, sec_e7 as e7, sec_e8 as e8, sec_e9 as e9, sec_coda as cd  # noqa: E401,E402

print(f"T8: f_pedra={t8.FP:.0f} N; F_chão={t8.FCH:.0f} N; a={t8.A:.2f} m/s²; T={t8.T:.0f} N; cavalo: F_chão − T = {t8.FCH - t8.T:.0f} N "
      f"= 600·0,32 = {t8.MC * t8.A:.0f} N; gelo: f_máx={t8.FM:.0f} N, a={t8.A_GELO:.3f} m/s²")
c = t8.LoteT8.__new__(t8.LoteT8); c.t_gelo = None; c.t_acc = 0.0
vs = [t8.LoteT8.v(c, k / 15) for k in range(int(t8.TOM * 15) + 1)]
dv = np.diff(vs) * 15
print(f"T8 tomada de aceleração: v de {vs[0]:.2f} a {vs[-1]:.2f} m/s em {t8.TOM:.0f} s; dv/dt = {dv.min():.3f}…{dv.max():.3f} m/s²; "
      f"passo constante fora dela: {t8.V_C:.2f} m/s")
c.t_gelo = 100.0
vg = [t8.LoteT8.v(c, 100.0 + k / 15) for k in range(60)]
dg = np.diff(vg) * 15
print(f"T8 gelo: v de {vg[0]:.2f} m/s, dv/dt = {dg[dg < -0.01].mean():.3f} m/s², para em {next(k for k, v in enumerate(vg) if v <= 0) / 15:.2f} s")
txt10 = Path(AQUI / "sec_t10.py").read_text(encoding="utf-8")
ok = "QUANTO MAIOR A DIFERENÇA DE MASSAS, MAIOR A FRAÇÃO" in txt10 and "DA ENERGIA CINÉTICA QUE FICA COM O MAIS LEVE" in txt10
print("T10 texto aprovado (QUANTO MAIOR A DIFERENÇA DE MASSAS, MAIOR A FRAÇÃO DA ENERGIA CINÉTICA QUE FICA COM O MAIS LEVE):", "OK" if ok else "FALTA")
fim = Path(AQUI / "sec_fim.py").read_text(encoding="utf-8")
print("Resumo, ideia 3 (NÃO CONSERVA? / AUMENTE O SISTEMA) no código:", "OK" if "NÃO CONSERVA?" in fim and "AUMENTE O SISTEMA" in fim else "FALTA")
print(f"T9: t2 = {t9.T2:.4f} s (P = {t9.P(t9.T2):.3f}); t1 = {t9.T1:.4f} s (P = {t9.P(t9.T1):.1e}); atritos {t9.F1:+.2f} N e {t9.F2:+.2f} N; "
      f"v_Terra = {np.sqrt(2 * 9.8 * 10) / 5.97e24:.2e} m/s")
print(f"T10: K = {t10.K1:.0f} J e {t10.K2:.0f} J; fração do leve {t10.K1 / (t10.K1 + t10.K2):.3f}")
print(f"E6: agarra {e6.V_AG:.4f} m/s, K {e6.K_AG:.3f} J (calor {e6.K0 - e6.K_AG:.3f} J); rebate {e6.V_RB:.4f} m/s, K {e6.K_RB:.2f} J; "
      f"rebate/agarra = {e6.V_RB / e6.V_AG:.2f}")
print(f"E7: {e7.V_H:.4f} m/s; 56°: {e7.V_56:.4f} m/s; K bala {e7.KB:.1f} J; K caçador {e7.KCZ:.4f} J; razão {e7.KB / e7.KCZ:.0f}; "
      f"na bala {100 * e7.KB / (e7.KB + e7.KCZ):.4f}%")
print(f"E8: v_bala = {e8.VB:.2f} m/s; p_bala {e8.PB:.3f}; p_rifle {e8.PR:.2f}; p_gases {e8.PG:.3f} kg·m/s")
print(f"E9: 45° → {np.degrees(e9.T2):.2f}° (n = {e9.N_AGUA})")
print(f"Coda: {cd.P_ABS * 1e6:.2f} μPa; {cd.P_REF * 1e6:.2f} μPa; vela {cd.F_VELA * 1e3:.3f} mN; laser {cd.F_LASER * 1e9:.2f} nN")
LIVRO = re.compile(r"HALLIDAY|NUSSENZVEIG|MOYS|TIPLER|SERWAY|YOUNG|FEYNMAN|KLEPPNER|LIVRO|CAP[IÍ]TULO|CAP\.|PROBLEMA \d|§", re.I)
achou = []
for p in sorted(AQUI.glob("sec_*.py")):
    for n, linha in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if linha.lstrip().startswith("#") or '"""' in linha:
            continue
        for s in re.findall(r'(?:txt|mtxt|linha|dica|selo|secao|hl)\([^)]*', linha):
            if LIVRO.search(s):
                achou.append(f"{p.name}:{n}: {s[:90]}")
print("referência a livro na tela:", achou or "nenhuma")
