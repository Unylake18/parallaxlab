"""yt_0025 · portão SYNC (handoff final §5.5/§6): para cada âncora, atraso entre o início da fala (1ª palavra, alinhamento_palavras.json) e o 1º evento
visual (1ª mudança significativa de imagem depois do início da âncora), medido no vídeo montado. Meta: atraso ≤ 0,2 s (imagem antes da fala é permitida).
uso: python sync25.py VIDEO.mp4  ->  qa/sync.txt"""
import json
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
video = Path(sys.argv[1]) if len(sys.argv) > 1 else U / "renders" / "preview_yt0025_v6_completo_960x540.mp4"
anc = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
ordem, A = anc["ordem"], anc["ancoras"]
al = json.loads((U / "alinhamento_palavras.json").read_text(encoding="utf-8"))
primeira = {}
for p in al:
    primeira.setdefault(p["aid"], p["start"])
c = av.open(str(video))
fps = float(c.streams.video[0].average_rate)
dif, ant = [], None
for f in c.decode(video=0):
    g = f.to_ndarray(format="gray")[::2, ::2].astype(np.int16)
    dif.append(0.0 if ant is None else float(np.abs(g - ant).mean()))
    ant = g
dif = np.array(dif)
# atraso do CONTEÚDO da âncora: instante em que a cena abriu a âncora (tempos_<lote>.json) menos o alvo (ini da voz); > 0 = a cena que fala daquele trecho veio tarde
tardio = {}
for arq in sorted(U.glob("tempos_*.json")):
    ini_ = json.loads(arq.read_text(encoding="utf-8"))["inicios"]
    ids_ = list(ini_)
    base = A[ids_[0]]["ini"]
    for i_ in ids_:
        tardio[i_] = ini_[i_] - (A[i_]["ini"] - base)
L = [f"vídeo: {video.name}; {len(dif)} quadros a {fps:g} fps ({len(dif) / fps:.1f} s)", "âncora   ini    1ªpalavra  1ºevento   atraso(img)  cena_tarde  estado"]
falhas = []
LIM = 0.03          # média de |Δ| em níveis de cinza que conta como mudança visível
for aid in ordem:
    a = A[aid]
    i0, i1 = round(a["ini"] * fps), round(a["fim"] * fps)
    fw = primeira[aid]
    janela = dif[i0:i1]
    idx = np.where(janela > LIM)[0]
    ev = (i0 + (idx[0] if len(idx) else len(janela))) / fps
    atraso = ev - fw
    td = tardio.get(aid, 0.0)
    ok = atraso <= 0.2 and td <= 0.2
    if not ok:
        falhas.append(aid)
    L.append(f"{aid:6s} {a['ini']:8.2f} {fw:8.2f} {ev:9.2f} {atraso:+7.2f}   {td:+8.2f}   {'OK' if ok else 'FALHA'}")
L.append(f"\nSYNC: {len(ordem) - len(falhas)}/{len(ordem)} âncoras com atraso ≤ 0,2 s; falhas: {falhas or 'nenhuma'}")
# tela parada: janelas com variação ~0 por mais de 2 s dentro da fala
parado, i = [], 0
while i < len(dif):
    if dif[i] < 0.002:
        j = i
        while j < len(dif) and dif[j] < 0.002:
            j += 1
        if (j - i) / fps > 2.0:
            parado.append((i / fps, (j - i) / fps))
        i = j
    else:
        i += 1
L.append(f"TELA PARADA > 2 s (variação ~0): {len(parado)} {'OK' if not parado else 'verificar (informação nova?)'}")
for t, d in parado:
    L.append(f"   {t:7.1f} s  duração {d:.1f} s")
(U / "qa").mkdir(exist_ok=True)
(U / "qa" / "sync.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L[-12:]))
