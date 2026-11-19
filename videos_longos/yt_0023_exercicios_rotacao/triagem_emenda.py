"""v5 §4 — triagem dos eventos EMENDA (saltos quadro a quadro > 6× a mediana). Agrupa em intervalos e separa pela região que muda:
  CONTA  : ≥ 70% da energia do salto na coluna da direita (x ≥ 480 px) = escrita pela caneta / passo de glyph map / entrada de linha → INTENCIONAL
  ESQUEMA: ≥ 70% na metade esquerda = o desenho muda (câmera planejada, match cut 3D→2.5D, fade do objeto) → candidato; vai para revisão por quadro
  MISTO  : o resto (troca de seção com tudo mudando: fade de seção) → INTENCIONAL (troca de âncora) quando dentro de 1,5 s de uma âncora; senão candidato
uso: python triagem_emenda.py   → renders/v5/triagem_emenda.txt"""
import re
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
LOTES = ["PH", "PE1a", "PE3", "PE2", "PE4"]
out = []
cand = []
for L in LOTES:
    txt = (U / f"renders/gates_v4_{L}.txt").read_text(encoding="utf-8", errors="replace")
    ev = [float(t) for t in re.findall(r"t=([\d.]+)s salto=", txt)]
    anc = [float(t) for n, t in re.findall(r"\[ancora\] (\S+) ([\d.]+)", (U / f"log_{L}.txt").read_text(encoding="utf-8", errors="replace"))]
    ancn = re.findall(r"\[ancora\] (\S+) ([\d.]+)", (U / f"log_{L}.txt").read_text(encoding="utf-8", errors="replace"))
    cl = []
    for t in sorted(ev):
        if cl and t - cl[-1][-1] <= 0.5:
            cl[-1].append(t)
        else:
            cl.append([t])
    c = av.open(str(U / f"media_{L}/videos/cena/540p15/{L}.mp4"))
    fps = float(c.streams.video[0].average_rate)
    need = {}
    for g in cl:
        for t in g:
            k = int(round(t * fps))
            need[k] = 1
            need[k - 1] = 1
    fr = {}
    for i, f in enumerate(c.decode(video=0)):
        if i in need:
            fr[i] = f.to_ndarray(format="gray").astype(np.int16)
        if i > max(need):
            break
    out.append(f"== {L}: {len(ev)} saltos em {len(cl)} intervalos")
    n_int = 0
    for g in cl:
        e_conta = e_esq = 0.0
        for t in g:
            k = int(round(t * fps))
            if k in fr and k - 1 in fr:
                d = np.abs(fr[k] - fr[k - 1])
                e_conta += float(d[:, 480:].sum())
                e_esq += float(d[:, :480].sum())
        tot = max(1.0, e_conta + e_esq)
        a0 = max([(n, float(x)) for n, x in ancn if float(x) <= g[0]] or [("?", 0.0)], key=lambda p: p[1])
        perto = min([abs(g[0] - float(x)) for n, x in ancn] or [99])
        if e_conta / tot >= 0.7:
            tipo, mot = "INTENCIONAL", "CONTA: escrita pela caneta / passo de glyph map / entrada de linha"
        elif e_esq / tot >= 0.7:
            tipo, mot = "CANDIDATO", "ESQUEMA: o desenho muda (câmera planejada, match cut 3D→2.5D ou fade do objeto) — revisar por quadro"
        elif perto <= 1.5:
            tipo, mot = "INTENCIONAL", "troca de seção (fade-through entre âncoras)"
        else:
            tipo, mot = "CANDIDATO", "MISTO fora de âncora — revisar por quadro"
        if tipo == "INTENCIONAL":
            n_int += 1
        else:
            cand.append((L, g[0], g[-1], a0[0], e_esq / tot))
        out.append(f"   {g[0]:7.2f}–{g[-1]:7.2f} s  {a0[0]:6s} {tipo:11s} {mot} (esq {100 * e_esq / tot:.0f}%)")
    out.append(f"   → INTENCIONAL {n_int} · CANDIDATO {len(cl) - n_int}")
(U / "renders/v5").mkdir(exist_ok=True, parents=True)
(U / "renders/v5/triagem_emenda.txt").write_text("\n".join(out), encoding="utf-8")
print("\n".join(l for l in out if l.startswith(("==", "   →"))))
print(len(cand), "candidatos")
