"""Mede, por âncora, a fala real (ASR) contra a janela do preview e escolhe os complementos (handoff complemento v3).
Uso: compl_medir.py            -> escreve audio/compl_plano.json e imprime a tabela
Entrada: alinhamento_palavras.json (gerar_ancoras_voz23.py), ancoras_v1_nominal.json (janelas), complemento_v3.json."""
import json, re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
alin = json.loads((AQUI / "alinhamento_palavras.json").read_text(encoding="utf-8"))
jan = json.loads((AQUI / "ancoras_v1_nominal.json").read_text(encoding="utf-8"))
ordem = jan["ordem"]
comp = json.loads((AQUI / "complemento_v3.json").read_text(encoding="utf-8"))
ALVO = 0.97 * 1862.0
ini, fim = {}, {}
for w in alin:
    a = w["aid"]
    ini.setdefault(a, w["start"])
    fim[a] = w["end"]
fala = {a: fim[a] - ini[a] for a in ordem}
voz = fim[ordem[-1]]
rat = {a: fala[a] / jan["ancoras"][a]["dur"] for a in ordem}
print(f"voz {voz:.1f} s; alvo {ALVO:.0f} s; déficit {ALVO - voz:.0f} s")
total, escolhidos = voz, []
for a, txt in comp:
    if rat[a] >= 0.92:
        print(f"  {a}: {rat[a]*100:.0f}% da janela: não precisa")
        continue
    if total >= ALVO:
        break
    n = len(re.findall(r"\w+", txt))
    add = n / 3.0
    escolhidos.append(a)
    total += add
    print(f"  {a}: {rat[a]*100:.0f}% ({fala[a]:.1f}/{jan['ancoras'][a]['dur']:.1f} s) + {n} palavras ≈ {add:.1f} s -> total {total:.0f} s")
(AQUI / "audio" / "compl_plano.json").write_text(json.dumps({"escolhidos": escolhidos, "voz": voz, "estimado": total,
                                                             "ratio_antes": {a: rat[a] for a in ordem}, "fala_antes": fala}, ensure_ascii=False, indent=1), encoding="utf-8")
print("escolhidos:", len(escolhidos), "estimado final", round(total), "s")
rest = [a for a in ordem if rat[a] < 0.92 and a not in escolhidos and a not in [c[0] for c in comp]]
print("sem complemento mas abaixo de 92%:", rest)
