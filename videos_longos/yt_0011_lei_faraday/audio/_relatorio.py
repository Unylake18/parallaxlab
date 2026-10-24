"""Relatório objetivo da voz de teste: duração por N, pausas e ritmo (lê alinhamento_v3_teste.json)."""
import json
from pathlib import Path

P = Path(__file__).resolve().parent
d = json.loads((P / "alinhamento_v3_teste.json").read_text(encoding="utf-8"))
cel, words, pauses = d["celulas"], d["words"], d["pauses"]
idx = [c["palavra"] for c in cel] + [len(words)]
silabas = lambda w: max(1, sum(1 for ch in w.lower() if ch in "aeiouáéíóúâêôãõàü"))
linhas = ["| N | início (s) | fim da fala (s) | duração (s) | pausa até a próxima (s) | palavras | pal/s |", "|---|---|---|---|---|---|---|"]
tot_p = 0
for i, c in enumerate(cel):
    a, b = idx[i], idx[i + 1] - 1
    ini, fim = words[a][1], words[b][2]
    nxt = cel[i + 1]["t"] if i + 1 < len(cel) else d["dur"]
    nw = b - a + 1
    linhas.append(f"| {c['chave']} | {ini:.1f} | {fim:.1f} | {fim - ini:.1f} | {nxt - fim:.1f} | {nw} | {nw / max(0.1, fim - ini):.2f} |")
    tot_p += nxt - fim
longas = [(a, b) for a, b in pauses if b - a >= 0.8]
fala = d["fala"][1] - d["fala"][0]
nw = len(words)
saida = [f"Duração total: {d['dur']:.1f} s ({int(d['dur'] // 60)} min {d['dur'] % 60:04.1f} s)",
         f"Palavras: {nw}; velocidade média (total): {nw / d['dur']:.2f} pal/s; só fala (sem pausas ≥0,12 s): "
         f"{nw / (fala - sum(b - a for a, b in pauses)):.2f} pal/s",
         f"Pausas ≥ 0,8 s: {len(longas)} (soma {sum(b - a for a, b in longas):.1f} s); pausas entre N (fim de fala → próximo início): soma {tot_p:.1f} s",
         "", "Pausas ≥ 1,0 s (início → fim):"]
for a, b in pauses:
    if b - a >= 1.0:
        ant = next((w[0] for w in reversed(words) if w[2] <= a + 0.05), "")
        dep = next((w[0] for w in words if w[1] >= b - 0.05), "")
        saida.append(f"  {a:7.1f}–{b:7.1f} s  ({b - a:.1f} s)  «…{ant}»  →  «{dep}…»")
saida += ["", *linhas]
(P / "duracoes_v3_teste.md").write_text("# Voz de teste v3 — medidas objetivas\n\n```\n" + "\n".join(saida[:saida.index('') + 0] if False else saida[:len(saida) - len(linhas) - 1]) + "\n```\n\n" + "\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(saida[:len(saida) - len(linhas) - 1]))
print("\n".join(linhas))
