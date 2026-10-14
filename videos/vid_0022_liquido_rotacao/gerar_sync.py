"""Alinha a narração do vid_0022 ao áudio e gera alinhamento_palavras.json e legenda.srt.

Sem ASR (como nos vídeos 8 e 9): as palavras recebem peso por sílabas, os finais das frases são
ancorados nas pausas medidas no WAV (programação dinâmica), com interpolação silábica interna.
Uso: gerar_sync.py, gerar_ancoras.py e sincronizar_preview.py, nesta ordem.
"""

import json
import re
import wave
from pathlib import Path

import numpy as np
from PIL import ImageFont

PASTA = Path(__file__).resolve().parent
WAV = PASTA / "audio" / "narracao_final.wav"
TEXTO = (PASTA / "texto_narracao.txt").read_text(encoding="utf-8")
norm = lambda q: re.sub(r"[^\wáéíóúâêôãõàç]", "", q.lower())

PUNCT = {",": 0.9, ":": 1.0, ";": 1.0, ".": 1.6, "?": 1.6, "!": 1.6}


def silabas(palavra: str) -> int:
    p = re.sub(r"[^\wáéíóúâêôãõàç]", "", palavra.lower())
    return max(1, len(re.findall(r"[aeiouáéíóúâêôãõàü]+", p)))


def pausas(sinal, sr, limiar=0.03, minimo=0.12):
    w = int(sr * 0.01)
    e = np.sqrt(np.convolve(sinal ** 2, np.ones(w) / w, "same"))[::w]
    sil = e < limiar
    runs, ini = [], None
    for i, s in enumerate(sil):
        if s and ini is None:
            ini = i
        if (not s) and ini is not None:
            if (i - ini) * 0.01 >= minimo:
                runs.append((ini * 0.01, i * 0.01))
            ini = None
    t0 = int(np.argmax(~sil)) * 0.01
    t1 = (len(sil) - int(np.argmax(~sil[::-1]))) * 0.01
    return runs, t0, t1


def main():
    with wave.open(str(WAV)) as w:
        n, sr, ch = w.getnframes(), w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(float)
    if ch > 1:
        x = x.reshape(-1, ch).mean(1)
    x /= np.abs(x).max()
    dur = n / sr
    runs, t0, t1 = pausas(x, sr)
    runs = [r for r in runs if r[0] > t0 + 0.05 and r[1] < t1 - 0.05]

    palavras = TEXTO.split()
    pal_leg = list(palavras)
    peso = np.array([silabas(p) + 0.3 + PUNCT.get(p[-1], 0.0) for p in palavras])
    cum = np.cumsum(peso)
    fim_pal = t0 + cum / cum[-1] * (t1 - t0)          # previsão do fim de cada palavra
    limites = [i for i, p in enumerate(palavras) if p[-1] in PUNCT]   # índice da palavra que antecede a pausa
    cand = [(a, b) for a, b in runs]

    # fim de cada frase: programação dinâmica pelo ritmo (sílabas/s parecido entre frases)
    fins = [i for i, p in enumerate(palavras) if p[-1] in ".?!"]
    inicios = [0] + [i + 1 for i in fins[:-1]]
    sil_f = [sum(silabas(q) for q in palavras[a_:b_ + 1]) for a_, b_ in zip(inicios, fins)]
    longas = list(cand)
    R = sum(sil_f) / (t1 - t0 - 0.3 * len(fins))

    def dp_frases():
        F, P = len(fins), len(longas)
        INF = 1e12
        best = np.full((F, P + 1), INF)               # best[i][k]: frase i termina na pausa k (k=P: fim da fala)
        back = {}
        for i in range(F):
            ks = range(P) if i < F - 1 else [P]
            for k in ks:
                a_fim = longas[k][0] if k < P else t1
                if i == 0:
                    dt = a_fim - t0
                    best[i][k] = ((sil_f[0] / dt - R) / (0.2 * R)) ** 2 if dt > 0.2 else INF
                    continue
                for j in range(P):
                    if best[i - 1][j] >= INF or longas[j][1] >= a_fim:
                        continue
                    dt = a_fim - longas[j][1]
                    if dt < max(0.2, (fins[i]-inicios[i]+1)/4.5):
                        continue
                    dur_j = longas[j][1] - longas[j][0]
                    c = best[i - 1][j] + ((sil_f[i] / dt - R) / (0.2 * R)) ** 2 + max(0.0, 0.3 - dur_j) * 8
                    if c < best[i][k]:
                        best[i][k], back[(i, k)] = c, j
        k, forcado = P, {}
        for i in range(F - 1, 0, -1):
            j = back[(i, k)]                          # a frase i-1 termina na pausa j
            forcado[fins[i - 1]] = longas[j]
            k = j
        return forcado

    forcado = dp_frases()

    uso = forcado

    # Tempos internos estimados por sílabas; apenas fins de frases ancorados.
    # Evita que uma pausa de vírgula estique uma única palavra por vários segundos.
    # tempos de cada palavra: dentro de cada trecho (entre pausas ancoradas), proporcional ao peso
    marcos = sorted(uso)
    ini_w, fim_w = np.zeros(len(palavras)), np.zeros(len(palavras))
    a_prev, i_prev = t0, 0
    for i in marcos + [len(palavras) - 1]:
        a_fim = uso[i][0] if i in uso else t1
        if i_prev > i:
            continue
        seg = peso[i_prev:i + 1]
        edges = a_prev + np.concatenate([[0], np.cumsum(seg)]) / seg.sum() * (a_fim - a_prev)
        ini_w[i_prev:i + 1], fim_w[i_prev:i + 1] = edges[:-1], edges[1:]
        if i in uso:
            a_prev = uso[i][1]
        i_prev = i + 1

    json.dump([dict(word=p,start=round(float(a),4),end=round(float(b),4)) for p,a,b in zip(palavras,ini_w,fim_w)], open(PASTA / 'alinhamento_palavras.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    # diagnóstico: ritmo (sílabas/s) por frase
    print(f"áudio {dur:.2f} s; fala {t0:.2f}–{t1:.2f}; {len(runs)} pausas; {len(uso)}/{len(limites)} limites ancorados")
    ini_f = 0
    for i, p in enumerate(palavras):
        if p[-1] in ".?!":
            sil = sum(silabas(q) for q in palavras[ini_f:i + 1])
            d = fim_w[i] - ini_w[ini_f]
            print(f"  {ini_w[ini_f]:7.2f}–{fim_w[i]:7.2f}  {sil / d:4.1f} síl/s  {' '.join(palavras[ini_f:i + 1])[:60]}")
            ini_f = i + 1

    # legenda: no máximo 2 linhas, largura <= 446 px (a 540 de largura), cues curtas
    fonte = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 27)
    larg = lambda s: fonte.getlength(s)
    MAXW = 440

    def quebra(ws):
        if larg(" ".join(ws)) <= MAXW:
            return [" ".join(ws)]
        melhor = None
        for k in range(len(ws) + 1):
            l1, l2 = " ".join(ws[:k]), " ".join(ws[k:])
            if (k and larg(l1) > MAXW) or (l2 and larg(l2) > MAXW):
                continue
            custo = max(larg(l1), larg(l2)) if l2 else larg(l1)
            if melhor is None or custo < melhor[0]:
                melhor = (custo, [l for l in (l1, l2) if l])
        return melhor[1] if melhor else None

    FRACAS = {"a", "o", "as", "os", "um", "uma", "de", "do", "da", "dos", "das", "no", "na", "em", "ao", "à",
              "e", "que", "para", "por", "com", "se", "é", "mas", "ou", "como", "ela", "esse", "essa", "nos"}

    def custo_cue(a_, b_, fim_frase):
        ws = pal_leg[a_:b_ + 1]
        if quebra(ws) is None or (fim_w[b_] - ini_w[a_]) > 3.8:
            return None
        c = 1.0 + 2.5 * (1 - min(1.0, larg(" ".join(ws)) / (1.5 * MAXW)))   # prefere cues cheias
        if not fim_frase:
            ult = palavras[b_]
            c += 0.0 if ult[-1] in ",:;" else (1.6 if norm(ult) in FRACAS else 0.5)
        if (fim_w[b_] - ini_w[a_]) < 0.9 and not fim_frase:
            c += 1.5                                  # evita cues-relâmpago no meio da frase
        if len(ws) == 1 and not fim_frase:
            c += 1.0
        return c

    # frases (juntando as muito curtas, como "Não.", à anterior)
    grupos, ini_g = [], 0
    for i, p in enumerate(palavras):
        if p[-1] in ".?!" or i == len(palavras) - 1:
            if grupos and (i - ini_g + 1) <= 2:
                grupos[-1] = (grupos[-1][0], i)
            else:
                grupos.append((ini_g, i))
            ini_g = i + 1
    cues = []
    for g0, g1 in grupos:
        L = g1 - g0 + 1
        best = [1e9] * (L + 1)
        prev = [0] * (L + 1)
        best[0] = 0.0
        for e in range(1, L + 1):
            for b in range(e):
                c = custo_cue(g0 + b, g0 + e - 1, e == L)
                if c is not None and best[b] + c < best[e]:
                    best[e], prev[e] = best[b] + c, b
        assert best[L] < 1e8, f"frase não cabe em cues: {palavras[g0:g1 + 1]}"
        e, partes = L, []
        while e > 0:
            partes.append(list(range(g0 + prev[e], g0 + e)))
            e = prev[e]
        cues.extend(reversed(partes))
    srt, ant = [], 0.0
    for n_, c in enumerate(cues, 1):
        ini = max(float(ini_w[c[0]]), ant + 0.02)
        fim = float(fim_w[c[-1]]) + (0.12 if palavras[c[-1]][-1] in ".?!" else 0.0)
        if n_ < len(cues):
            fim = min(fim, float(ini_w[cues[n_][0]]) - 0.02)
        fim = max(fim, ini + 0.4)
        ant = fim
        def ts(t):
            total = round(t * 1000)
            seconds, milliseconds = divmod(total, 1000)
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
        linhas = quebra([pal_leg[q] for q in c])
        srt.append(f"{n_}\n{ts(ini)} --> {ts(fim)}\n" + "\n".join(linhas))
    (PASTA / "legenda.srt").write_text("\n\n".join(srt) + "\n", encoding="utf-8")
    print(f"legenda.srt: {len(srt)} blocos; rode gerar_ancoras.py em seguida")


if __name__ == "__main__":
    main()

