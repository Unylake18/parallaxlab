"""yt_0028 v4 (handoff v4 §5, R10): nenhuma tela vazia (só canto e logo) por mais de 0,8 s. Mede no PIXEL do preview inteiro (pega também as emendas
entre lotes e os waits, que o contador da cena não vê): em cada quadro, a fração de pixels da área útil (fora do canto e do logo) que se afasta do
degradê violeta liso (> 10 níveis de brilho) — grade, moldura, seta, texto contam como objeto. Quadro "vazio" = fração < 0,02 %.
Também conta os objetos visíveis da cena por quadro nas trocas de layout (componentes conexos da máscara, 960×540).
Saída: renders/v4/qa/transicoes_v4.txt.  uso: python transicoes.py [rodada]"""
import json
import io
import sys
from pathlib import Path

import av
import numpy as np
from scipy import ndimage

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v4"
V = U / "renders" / R / f"yt_0028_preview_{R}_540p15.mp4"
q = json.loads((U / "renders" / R / f"quadros_{R}.json").read_text(encoding="utf-8"))
TOPO, BASE = np.array([0x18, 0x14, 0x3A], float), np.array([0x0F, 0x0C, 0x26], float)
H, W = 540, 960
fundo = (TOPO[None, :] * (1 - np.linspace(0, 1, H)[:, None]) + BASE[None, :] * np.linspace(0, 1, H)[:, None])[:, None, :]
util = np.ones((H, W), bool)
util[:72, :460] = False           # canto (2 linhas)
util[:62, 800:] = False           # logo
TROCAS = [("A → B1-1", "B1-1"), ("B3-2 → B3-3", "B3-3"), ("B4-4/B4-5 → B5-1", "B5-1"), ("B5-1 → B5-2", "B5-2"), ("B5-2 → B5-3", "B5-3"),
          ("B5-4 → B5-5 (alvo 22)", None), ("B6-7 → B7-1", "B7-1")]

fr, cont, nobj = [], [], []
c = av.open(str(V))
for i, f in enumerate(c.decode(video=0)):
    a = f.to_ndarray(format="rgb24").astype(float)
    m = (np.abs(a - fundo).max(2) > 10) & util
    cont.append(m.mean())
    fr.append(m)
    if len(fr) > 1:
        fr[-2] = None
c.close()
cont = np.array(cont)
N, FPS = len(cont), 15
vazio = cont < 0.0002
L = [f"yt_0028 {R} · R10 transições (preview {N} quadros, {N / FPS:.1f} s): quadro vazio = < 0,02 % da área útil fora do fundo liso; limite 0,8 s (12 quadros)", ""]
runs, i = [], 0
while i < N:
    if vazio[i]:
        j = i
        while j < N and vazio[j]:
            j += 1
        runs.append((i, j))
        i = j
    else:
        i += 1
ruins = [(a, b) for a, b in runs if b - a > 12]
L.append(f"trechos vazios (qualquer duração): {len(runs)}; mais longo {max((b - a for a, b in runs), default=0) / FPS:.2f} s; > 0,8 s: {len(ruins)}")
for a, b in ruins:
    L.append(f"  VAZIO {a / FPS:7.2f}–{b / FPS:7.2f} s ({(b - a) / FPS:.2f} s)")
L += ["", "trocas de layout (janela de 3 s em volta do início da âncora; por quadro: % da área útil com objeto · nº de objetos (componentes conexos)):"]
c = av.open(str(V))
frames = {}
alvo_q = set()
for nome, anc in TROCAS:
    if anc is None:
        continue
    k = q[anc]
    alvo_q |= set(range(max(0, k - 30), min(N, k + 30)))
for i, f in enumerate(c.decode(video=0)):
    if i in alvo_q:
        a = f.to_ndarray(format="rgb24").astype(float)
        m = (np.abs(a - fundo).max(2) > 10) & util
        frames[i] = ndimage.label(ndimage.binary_dilation(m, iterations=2))[1]
c.close()
for nome, anc in TROCAS:
    if anc is None:
        L.append(f"  {nome}: troca dentro do lote PB5 (gatilho «dividindo o erro pelo passo»); coberta pela varredura de quadros vazios acima")
        continue
    k = q[anc]
    js = range(max(0, k - 30), min(N, k + 30))
    mn = min(cont[j] for j in js)
    ob = [frames[j] for j in js]
    vz = max((b - a for a, b in runs if a < js[-1] and b > js[0]), default=0)
    L.append(f"  {nome}: {(k - 30) / FPS:.2f}–{(k + 30) / FPS:.2f} s · mínimo {100 * mn:.2f} % da área · objetos {min(ob)}–{max(ob)} · maior vazio {vz / FPS:.2f} s "
             f"→ {'OK' if vz <= 12 else 'FALHA'}")
L += ["", f"R10: {len(ruins)} ocorrências de tela vazia > 0,8 s"]
(U / "renders" / R / "qa" / f"transicoes_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
