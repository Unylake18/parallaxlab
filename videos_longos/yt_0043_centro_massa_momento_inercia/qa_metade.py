"""yt_0043 · QA R14 (handoff final §3, §7): varredura A CADA 0,2 s no vídeo inteiro.
- METADE VAZIA: metade esquerda (x < 960) ou direita (x ≥ 960) só com papel (sem texto, traço ou 3D) por mais de 3 s (fora do A1 e do CTA).
- TELA VAZIA: os dois lados só com papel por mais de 0,5 s (palco vazio).
O "conteúdo" é medido em pixels claros ou saturados (a grade do papel é escura e fica abaixo do limiar); título do canto e logo ficam fora da região medida.
uso: python qa_metade.py [arquivo.mp4] [saida.txt]   (padrão: renders/final/yt_0043_preview_final_540p15.mp4 → qa/metade_vazia_final.txt)"""
import json
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
ARQ = Path(sys.argv[1]) if len(sys.argv) > 1 else U / "renders" / "final" / "yt_0043_preview_final_540p15.mp4"
SAI = Path(sys.argv[2]) if len(sys.argv) > 2 else U / "qa" / "metade_vazia_final.txt"
LIM_PIX = 120          # pixels de conteúdo para a metade "ter algo"
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
EXCETO = []            # (início, fim) em s onde a metade vazia é permitida: A1 inteira e o CTA do fim
if "A1" in ANC:
    EXCETO.append((ANC["A1"]["ini"], ANC["A1"]["fim"]))
c = av.open(str(ARQ))
st = c.streams.video[0]
fps = float(st.average_rate)
passo = max(1, int(round(fps * 0.2)))
amostras = []
for i, fr in enumerate(c.decode(st)):
    if i % passo:
        continue
    a = fr.to_ndarray(format="rgb24")
    reg = a[75:520, 30:930].astype(np.int16)                   # sem o canto (título/logo) nem a borda
    mx, mn = reg.max(axis=2), reg.min(axis=2)
    cont = (mx > 105) | ((mx - mn) > 70)                      # claro ou saturado
    esq, dir_ = int(cont[:, :450].sum()), int(cont[:, 450:].sum())
    baixo = int(cont[125:, :].sum())                              # abaixo da faixa do topo (y ≥ 200 em 540p)
    amostras.append((i / fps, esq, dir_, baixo))
dur = amostras[-1][0]
L = [f"QA R14 · varredura a cada 0,2 s ({len(amostras)} amostras) em {ARQ.name} · limiar {LIM_PIX} px de conteúdo por metade", ""]


def intervalos(sel):
    out, ini = [], None
    for t, e, d, b in amostras:
        v = sel(e, d, b)
        if v and ini is None:
            ini = t
        if not v and ini is not None:
            out.append((ini, t))
            ini = None
    if ini is not None:
        out.append((ini, dur))
    return out


def fora(iv):
    return not any(a <= iv[0] and iv[1] <= b + 0.3 for a, b in EXCETO)


def mm(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


tot_ok = True
for nome, sel, lim, vale in (("METADE ESQUERDA só papel", lambda e, d, b: e < LIM_PIX, 3.0, True),
                             ("TELA ABAIXO DO TOPO só papel (S1 do v2: 18 s)", lambda e, d, b: b < LIM_PIX, 3.0, True),
                             ("TELA INTEIRA só papel (palco vazio)", lambda e, d, b: e < LIM_PIX and d < LIM_PIX, 0.5, True),
                             ("METADE DIREITA só papel (INFO: a coluna espera o 1º gatilho com o 3D/figura na esquerda; não reprova)", lambda e, d, b: d < LIM_PIX, 3.0, False)):
    iv = [x for x in intervalos(sel) if x[1] - x[0] > 0.4]
    ruins = [x for x in iv if x[1] - x[0] > lim and fora(x)]
    L.append(f"{nome}: {len(iv)} intervalos > 0,4 s; acima de {lim:.1f} s fora do A1/CTA: {len(ruins)}  {'OK' if not ruins else ('VER' if vale else 'INFO')}")
    for a, b in iv:
        L.append(f"   {mm(a)}–{mm(b)} ({b - a:.1f} s){'  [A1/CTA]' if not fora((a, b)) else ''}{'  <-- ACIMA DO LIMITE' if (b - a > lim and fora((a, b)) and vale) else ''}")
    tot_ok &= (not ruins) or (not vale)
L.append("")
L.append("RESULTADO: " + ("OK" if tot_ok else "VER"))
SAI.parent.mkdir(exist_ok=True)
SAI.write_text("\n".join(L), encoding="utf-8")
print("\n".join(L[:40]))
