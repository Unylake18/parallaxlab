"""yt_0009 — legenda .srt a partir dos tempos de sync.json (narração v8) + gancho (audio/gancho_v9.wav).

Sem ASR: palavras do v8 já têm início/fim (sync_voz.py); as do gancho são distribuídas por peso de sílabas entre o início e o fim da fala
medidos no WAV. Cada legenda: até 2 linhas de ≤ 42 caracteres, quebrando em pontuação; sem tags de áudio.
"""
import json
import re
import wave
from pathlib import Path

import numpy as np

PASTA = Path(__file__).resolve().parent
GAP = 0.5
MAXC, MAXL = 42, 2
PUNCT_FIM = ".?!"
NORM = lambda q: re.sub(r"[^\wáéíóúâêôãõàçü]", "", q.lower())


def silabas(p):
    return max(1, len(re.findall(r"[aeiouáéíóúâêôãõàü]+", NORM(p))))


def fala_gancho():
    with wave.open(str(PASTA / "audio" / "gancho_v9.wav")) as w:
        sr, n = w.getframerate(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    if x.ndim > 1:
        x = x[:, 0]
    e = np.abs(x) > 0.02
    i0, i1 = int(np.argmax(e)) / sr, (len(e) - int(np.argmax(e[::-1]))) / sr
    return i0, i1, n / sr


def palavras_gancho(t0):
    txt = (PASTA / "narracao_gancho_v9.md").read_text(encoding="utf-8")
    corpo = txt.split("## Texto limpo (legenda)")[1].split("##")[0].strip()
    ws = corpo.split()
    i0, i1, _ = fala_gancho()
    peso = [silabas(w) + (1.2 if w[-1] in ".?!:" else 0.5 if w[-1] in ",;" else 0) for w in ws]
    tot = sum(peso)
    t, out = t0 + i0, []
    dur = i1 - i0
    for w, p in zip(ws, peso):
        d = dur * p / tot
        out.append((w, t, t + d))
        t += d
    return out


def fmt(t):
    h, r = divmod(max(t, 0), 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def main():
    sy = json.load(open(PASTA / "sync.json", encoding="utf-8"))
    pal = [(w[0], w[1], w[2]) for w in sy["words"]]
    pal += palavras_gancho(sy["dur"] + GAP)
    cues, cur = [], []

    def flush():
        if cur:
            cues.append(list(cur))
            cur.clear()

    for w in pal:
        cur.append(w)
        txt = " ".join(x[0] for x in cur)
        fim_frase = w[0][-1] in PUNCT_FIM
        quebra = w[0][-1] in ",;:" and len(txt) > MAXC * 0.6
        if fim_frase or quebra or len(txt) >= MAXC * MAXL - 6:
            flush()
    flush()
    out = []
    for i, c in enumerate(cues, 1):
        txt = " ".join(x[0] for x in c)
        if len(txt) > MAXC:                                   # quebra em duas linhas, no espaço mais próximo do meio
            mid = len(txt) // 2
            sp = [m.start() for m in re.finditer(" ", txt)]
            ok = [p for p in sp if len(txt[:p].split()[-1]) > 2 and len(txt[p + 1:].split()[0]) > 0] or sp
            k = min(ok, key=lambda p: abs(p - mid))
            txt = txt[:k] + "\n" + txt[k + 1:]
        t0, t1 = c[0][1], c[-1][2]
        if i < len(cues):
            t1 = min(max(t1, t0 + 0.8), cues[i][0][1] - 0.02)
        out.append(f"{i}\n{fmt(t0)} --> {fmt(t1)}\n{txt}\n")
    (PASTA / "legenda.srt").write_text("\n".join(out), encoding="utf-8")
    print(f"{len(out)} legendas; última termina em {fmt(cues[-1][-1][2])}")


if __name__ == "__main__":
    main()
