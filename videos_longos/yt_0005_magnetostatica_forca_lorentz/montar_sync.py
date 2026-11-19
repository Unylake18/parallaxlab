"""yt_0005 — monta o áudio sincronizado (pausas de pads.json inseridas em pausas reais da fala), legenda.srt e capítulos.
  uv run --no-sync python videos_longos/yt_0005_magnetostatica_forca_lorentz/montar_sync.py
Entradas: sync.json, pads.json, blocos.json (gerados pela cena), audio/narracao_v4.wav. Saídas: audio/narracao_montagem.wav, legenda.srt, capitulos_youtube.txt"""
import json
import re
import wave
from pathlib import Path

import numpy as np

PASTA = Path(__file__).resolve().parent
AUD = PASTA / "audio"
FINAL = AUD / "narracao_v4.wav"
MONTAGEM = AUD / "narracao_montagem.wav"
NORM = lambda q: re.sub(r"[^\wáéíóúâêôãõàçü]", "", q.lower())


def ler(path):
    with wave.open(str(path)) as w:
        n, sr, ch = w.getnframes(), w.getframerate(), w.getnchannels()
        raw = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, ch)
    return raw, sr


def grafia_legenda(palavras):
    return list(palavras)


def montar():
    s = json.load(open(PASTA / "sync.json", encoding="utf-8"))
    pads = json.load(open(PASTA / "pads.json", encoding="utf-8"))["pads"]       # [[instante no áudio original, s], ...]
    raw, sr = ler(FINAL)
    pausas_abs = [tuple(p) for p in s["pauses"]]
    # peso da pontuação que fecha a palavra antes de cada pausa: a espera entra de preferência em fim de frase,
    # nunca no meio de uma expressão (pausa sem pontuação) se houver alternativa no trecho
    PESO = {".": 3, "?": 3, "!": 3, ":": 1.5, ";": 1.5, ",": 1}
    fins = [(w[2], PESO.get(w[0][-1], 0)) for w in s["words"]]
    peso = lambda p: max((pw for e, pw in fins if p[0] - 0.15 < e < p[1]), default=0)
    # cada pausa extra entra no meio de uma pausa real entre o marco anterior e o marco atrasado
    cortes, prev = [], 0.0
    for t, d in sorted(pads):
        dentro = [p for p in pausas_abs if prev - 1e-6 <= p[0] and p[1] <= t + 0.05 and peso(p) > 0]
        if dentro:
            p = max(dentro, key=lambda q: peso(q) + (q[1] - q[0]) * 0.5 + q[1] / 100)   # fim de frase, perto do marco
            onde = (p[0] + p[1]) / 2
        else:
            onde = t - 0.02                                                     # sem pausa: logo antes da palavra
        if t < 3.0:
            onde = 0.0                                                          # esperas da 1ª frase viram um silêncio antes da 1ª palavra (sem engasgo no meio da fala)
        cortes.append((round(onde, 3), round(d, 3), round(t, 3)))
        prev = t
    partes, last = [], 0
    for onde, d, _ in sorted(cortes):
        i = int(round(onde * sr))
        partes += [raw[last:i], np.zeros((int(round(d * sr)), raw.shape[1]), dtype=np.int16)]
        last = i
    partes.append(raw[last:])
    full = np.concatenate(partes)
    with wave.open(str(MONTAGEM), "wb") as w:
        w.setnchannels(full.shape[1]); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(full.tobytes())
    json.dump({"fonte": FINAL.name, "insercoes": [{"em_s": o, "silencio_s": d, "marco_s": t} for o, d, t in sorted(cortes)]},
              open(AUD / "narracao_montagem_receita.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    desloc = lambda t: t + sum(d for o, d, _ in cortes if o <= t)
    print(f"narracao_montagem.wav: {len(full) / sr:.2f} s ({len(cortes)} pausas extras, +{sum(d for _, d, _ in cortes):.2f} s)")

    # legenda (YouTube): até 2 linhas de até 42 caracteres, cues de até 6 s, quebradas em pontuação
    pal = [w[0] for w in s["words"]]
    leg = grafia_legenda(pal)
    ini = [desloc(w[1]) for w in s["words"]]
    fim = [desloc(w[2]) for w in s["words"]]
    MAXC = 42
    FRACAS = {"a", "o", "as", "os", "um", "uma", "de", "do", "da", "dos", "das", "no", "na", "em", "ao", "à", "e",
              "que", "para", "pra", "por", "com", "se", "é", "mas", "ou", "como", "esse", "essa", "nos", "num", "numa"}

    def quebra(ws):
        melhor = None
        for k in range(1, len(ws) + 1):
            l1, l2 = " ".join(ws[:k]), " ".join(ws[k:])
            if len(l1) > MAXC or len(l2) > MAXC:
                continue
            custo = max(len(l1), len(l2)) + (0 if not l2 else (14 if ws[k - 1][-1] in ",:;" else 17))   # 1 linha se couber
            if melhor is None or custo < melhor[0]:
                melhor = (custo, [l for l in (l1, l2) if l])
        return melhor[1] if melhor else None

    def custo_cue(a, b, fim_frase):
        ws = leg[a:b + 1]
        if quebra(ws) is None or fim[b] - ini[a] > 6.0:
            return None
        c = 1.0 + 2.5 * (1 - min(1.0, len(" ".join(ws)) / (1.6 * MAXC)))
        if not fim_frase:
            c += 0.0 if pal[b][-1] in ",:;" else (1.6 if NORM(pal[b]) in FRACAS else 0.6)
        if fim[b] - ini[a] < 1.0 and not fim_frase:
            c += 1.5
        return c

    grupos, g0 = [], 0
    for i, p in enumerate(pal):
        if p[-1] in ".?!" or i == len(pal) - 1:
            grupos.append((g0, i))
            g0 = i + 1
    cues = []
    for a0, a1 in grupos:
        L = a1 - a0 + 1
        best, prev_ = [1e9] * (L + 1), [0] * (L + 1)
        best[0] = 0.0
        for e in range(1, L + 1):
            for b in range(e):
                c = custo_cue(a0 + b, a0 + e - 1, e == L)
                if c is not None and best[b] + c < best[e]:
                    best[e], prev_[e] = best[b] + c, b
        assert best[L] < 1e8, f"frase não cabe em cues: {' '.join(pal[a0:a1 + 1])}"
        e, pp = L, []
        while e > 0:
            pp.append(list(range(a0 + prev_[e], a0 + e)))
            e = prev_[e]
        cues += reversed(pp)
    ts = lambda t: f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)) % 1000:03d}"
    srt, ant = [], 0.0
    for n, c in enumerate(cues, 1):
        a = max(ini[c[0]], ant + 0.02)
        b = fim[c[-1]] + (0.25 if pal[c[-1]][-1] in ".?!" else 0.05)
        if n < len(cues):
            b = min(b, ini[cues[n][0]] - 0.04)
        b = max(b, a + 0.6)
        ant = b
        srt.append(f"{n}\n{ts(a)} --> {ts(b)}\n" + "\n".join(quebra([leg[q] for q in c])))
    (PASTA / "legenda.srt").write_text("\n\n".join(srt) + "\n", encoding="utf-8")
    print(f"legenda.srt: {len(srt)} cues")


def capitulos():
    """Capítulos do YouTube a partir do instante (no vídeo) em que cada bloco começa (âncoras da cena)."""
    log = json.load(open(PASTA / "ancoras_log.json", encoding="utf-8"))
    T = {str(l[0]): l[1] for l in log}
    marcas = [(0.0, "Abertura: dois fios e uma pergunta"), (T["6"], "A força de Lorentz e a regra da mão direita"),
              (T["20"], "A trajetória nasce da lei de Lorentz: frequência ciclotrônica e raio"), (T["64"], "A hélice"),
              (T["68"], "Por que a rapidez não muda: trabalho e potência"), (T["80"], "Da carga à corrente: linha, superfície e volume"),
              (T["98"], "Conservação da carga: a equação da continuidade"), (T["113"], "Thomson: o seletor de velocidades"),
              (T["126"], "Medindo a razão carga–massa"), (T["132"], "Síntese e a pergunta que fica")]
    ts = lambda t: f"{int(t // 60):02d}:{int(t % 60):02d}"
    (PASTA / "capitulos_youtube.txt").write_text(chr(10).join(f"{ts(t)} {n}" for t, n in marcas) + chr(10), encoding="utf-8")
    print("capitulos_youtube.txt:", len(marcas))


if __name__ == "__main__":
    montar()
    capitulos()
