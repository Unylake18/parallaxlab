"""Planejador de sincronização do vid_0025.

Entradas: ancoras.json (instante de cada frase na voz), nat.json (duração natural de cada trecho visual, medida pela cena
em modo MEDIR), alinhamento_palavras.json e audio/narracao_v5.wav.
Para cada trecho k (de uma âncora à seguinte): V = intervalo na voz; nat = duração natural da animação.
O trecho recebe D = max(V, SFLOOR * nat): se a voz for curta demais para a animação (sem passar de SFLOOR de velocidade),
insere-se uma pausa de silêncio na voz, no vão entre as frases, no fim do trecho. Escala do trecho = min(1, D / nat).
Saídas: sync.json (T = instante de cada âncora no VÍDEO, S = escala, NAT, pads) e audio/narracao_sync.wav (voz + pausas).

Uso: uv run --no-sync python plan_sync.py [--sfloor 0.72]
"""
import argparse
import json
import wave
from pathlib import Path

import numpy as np

PASTA = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--sfloor", type=float, default=0.72)
ap.add_argument("--maxpad", type=float, default=3.0, help="pausa máxima por trecho (s); o excedente vira lentidão da animação")
a = ap.parse_args()

AN = json.loads((PASTA / "ancoras.json").read_text(encoding="utf-8"))
NAT = json.loads((PASTA / "nat.json").read_text(encoding="utf-8"))
PAL = json.loads((PASTA / "alinhamento_palavras.json").read_text(encoding="utf-8"))
order, A = AN["order"], AN["A"]
assert all(n in NAT for n in order), [n for n in order if n not in NAT]

T, S, pads, rows = {order[0]: A[order[0]]}, {}, [], []
for k in range(len(order) - 1):
    n0, n1 = order[k], order[k + 1]
    V = A[n1] - A[n0]
    nat = NAT[n1] - NAT[n0]
    need = a.sfloor * nat
    pad = max(0.0, need - V)
    pad = min(pad, a.maxpad)
    D = V + pad
    S[n0] = round(min(1.5, D / nat), 4) if nat > 1e-6 else 1.0
    T[n1] = round(T[n0] + D, 3)
    if pad > 0.02 and n1 != "fim":
        i = next(j for j, p in enumerate(PAL) if abs(p["start"] - A[n1]) < 1e-6)
        pos = (PAL[i - 1]["end"] + PAL[i]["start"]) / 2
        pads.append((round(pos, 3), round(pad, 3)))
    rows.append((n0, round(V, 2), round(nat, 2), round(D, 2), round(pad, 2), S[n0]))
S["fim"] = 1.0
total_pad = sum(p for _, p in pads)
(PASTA / "sync.json").write_text(json.dumps(dict(T=T, S=S, NAT=NAT, order=order, pads=pads, end=T["fim"]), indent=1), encoding="utf-8")

print("%-6s %6s %6s %6s %6s %6s" % ("trecho", "voz", "nat", "dur", "pausa", "escala"))
for r in rows:
    flag = "  <-- pausa" if r[4] > 0.02 else ""
    print("%-6s %6.2f %6.2f %6.2f %6.2f %6.2f%s" % (*r, flag))
print("TOTAL de pausas: %.1f s | vídeo termina em %.1f s (limite 179)" % (total_pad, T["fim"]))

# áudio com as pausas
with wave.open(str(PASTA / "audio" / "narracao_v5.wav")) as w:
    sr, nch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
    pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
assert nch == 1 and sw == 2
out, last = [], 0
for pos, pad in sorted(pads):
    i = int(pos * sr)
    out.append(pcm[last:i])
    out.append(np.zeros(int(round(pad * sr)), dtype=np.int16))
    last = i
out.append(pcm[last:])
fim_pcm = np.concatenate(out)
need = int(round(T["fim"] * sr)) - len(fim_pcm)          # cartão final: silêncio até o fim do vídeo
if need > 0:
    fim_pcm = np.concatenate([fim_pcm, np.zeros(need, dtype=np.int16)])
dest = PASTA / "audio" / "narracao_sync.wav"
with wave.open(str(dest), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(fim_pcm.tobytes())
print("áudio:", dest.name, "%.2f s" % (len(fim_pcm) / sr))
