"""yt_0024 v3 §1.3 — auditorias da caneta, lidas dos logs do render: ORDEM POR X ([ordem] do voa), CADEIA ([linha]: continuação '=' sempre sob uma
linha da mesma cadeia), TAMANHO ÚNICO ([linha] fs), CANETA (FadeIn de termo pronto na CONTA) e FLASH POR QUADRO (flash24.py).
uso: python caneta24.py PB3 PB6 → renders/ordem.txt, renders/cadeia.txt, renders/flash.txt, renders/caneta_resumo.txt"""
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
U = Path(__file__).resolve().parent
LOTES = sys.argv[1:] or ["PB3", "PB6"]
R = U / "renders"
ordem, cadeia, flash, resumo = [], [], [], []
tot = dict(ordem=0, cadeia=0, tam=0, caneta=0, flash=0, gmp=0, passos=0)
PASSOS = {   # v3 §1.5/§5: cadeias que não podem pular passo (trechos literais do LaTeX da linha, em ordem); cada linha fica ≥ 1 s antes da seguinte
    'PB6': [[r'0 = I \alpha', r'I \alpha = -', r'\alpha = \frac{-', r'-(-0{,}054)', r'+5{,}9'],
            [r'W = \Delta K', r'\tfrac{1}{2} 0{,}20 \cdot 3{,}0^2', r'= 0{,}900 - 0{,}225', r'W = 0{,}675']],
    'PB2': [[r'dA =', r'\frac{dA}{dt} = \frac{|\vec r\times\vec p|', r'\frac{|\vec L|}{2m}', r'0{,}30']],
}
for l in LOTES:
    lg = (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace")
    aud = (U / f"log_aud_{l}.txt").read_text(encoding="utf-8", errors="replace") if (U / f"log_aud_{l}.txt").exists() else ""
    ev = [(float(m.group(1)), int(m.group(2)), int(m.group(3))) for m in re.finditer(r"\[ordem\]\s+([0-9.]+)s voa n=(\d+) falhas=(\d+)", lg)]
    ruins = [e for e in ev if e[2] > 0]
    tot["ordem"] += len(ruins)
    ordem.append(f"{l}: {len(ev)} voos com fila por x, {len(ruins)} com falha de ordem" + "".join(f"\n   {t:7.1f}s n={n} falhas={f}" for t, n, f in ruins[:30]))
    lin = [(float(m.group(1)), float(m.group(2)), int(m.group(3)), m.group(4), m.group(5).strip()) for m in
           re.finditer(r"\[linha\]\s+([0-9.]+) fs=([0-9.]+) cont=(\d) acima=(\w+) \| (.*)", lg)]
    orf = [x for x in lin if x[2] == 1 and x[3] != "tex"]
    tot["cadeia"] += len(orf)
    cadeia.append(f"{l}: {len(lin)} linhas na CONTA, {sum(1 for x in lin if x[2])} continuações, {len(orf)} continuação sem linha da cadeia acima" +
                  "".join(f"\n   {t:7.2f}s {tx[:60]}" for t, fs, c, ac, tx in orf[:20]))
    for cad in PASSOS.get(l, []):
        pos_, falt_ = 0, []
        tt_ = []
        for frag in cad:
            ach = [k for k in range(pos_, len(lin)) if frag in lin[k][4]]
            if not ach:
                falt_.append(frag)
                continue
            tt_.append((frag, ach[0]))
            pos_ = ach[0] + 1
        curtos = [f"{frag}: {lin[k + 1][0] - lin[k][0]:.2f}s" for frag, k in tt_ if k + 1 < len(lin) and lin[k + 1][0] - lin[k][0] < 1.0 and frag != cad[-1]]
        tot["passos"] += len(falt_) + len(curtos)
        resumo.append(f"{l}: PASSOS {len(tt_)}/{len(cad)} presentes" + ("; FALTAM " + str(falt_) if falt_ else "") + ("; CURTOS (<1 s) " + str(curtos) if curtos else ""))
    fss = sorted(set(round(x[1], 1) for x in lin))
    ref = max(set(round(x[1], 1) for x in lin), key=lambda v: sum(1 for x in lin if round(x[1], 1) == v)) if lin else 54
    fora = [x for x in lin if abs(x[1] / ref - 1) > 0.03]
    tot["tam"] += len(fora)
    resumo.append(f"{l}: TAMANHO ÚNICO ref {ref} · {len(fora)} linhas fora de ±3 % (fs vistos: {fss[:8]})" + "".join(f"\n   {t:7.2f}s fs={fs:.1f} {tx[:50]}" for t, fs, c, ac, tx in fora[:10]))
    n_can = len([x for x in re.findall(r"CANETA FadeIn de termo pronto '([^']*)'", aud) if "=" in x])      # só linhas de equação (rótulos de desenho não contam)
    n_gmp = len(re.findall(r"GM PARCIAL", aud))
    tot["caneta"] += n_can
    tot["gmp"] += n_gmp
    resumo.append(f"{l}: CANETA (FadeIn de termo pronto na CONTA) {n_can} · GM PARCIAL {n_gmp} (auditoria em log_aud_{l}.txt)")
    r = subprocess.run([sys.executable, "flash24.py", l], cwd=U, capture_output=True, text=True, env=dict(__import__("os").environ, PYTHONIOENCODING="utf-8"))
    flash.append(r.stdout.strip())
    m = re.search(r"(\d+) eventos, (\d+) com tinta antes da vez", r.stdout)
    tot["flash"] += int(m.group(2)) if m else 0
(R / "ordem.txt").write_text("\n".join(ordem) + "\n", encoding="utf-8")
(R / "cadeia.txt").write_text("\n".join(cadeia) + "\n", encoding="utf-8")
(R / "flash.txt").write_text("\n".join(flash) + "\n", encoding="utf-8")
head = f"RESUMO CANETA {LOTES}: ORDEM POR X {tot['ordem']} · CADEIA {tot['cadeia']} · TAMANHO ÚNICO {tot['tam']} · CANETA {tot['caneta']} · FLASH {tot['flash']} · GM PARCIAL {tot['gmp']} · PASSOS {tot['passos']}"
(R / "caneta_resumo.txt").write_text(head + "\n" + "\n".join(resumo) + "\n", encoding="utf-8")
print(head)
print("\n".join(ordem + cadeia + resumo + flash))
