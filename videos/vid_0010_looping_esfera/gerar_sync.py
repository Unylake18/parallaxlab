"""Alinha a narração do vid_0010 ao áudio e gera sync.json (âncoras) e legenda.srt.

Sem ASR (como nos vídeos 8 e 9): as palavras recebem peso por sílabas, os limites de pontuação são
ancorados nas pausas medidas no WAV (programação dinâmica) e o resto é interpolado dentro de cada trecho.
Uso: uv run python videos/vid_0010_looping_esfera/gerar_sync.py
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
LEAD = 0.0            # as âncoras visuais podem antecipar a fala; 0 = exatamente no início da palavra

# (nome, trecho do texto onde a âncora cai). Em ordem; cada trecho é procurado depois do anterior.
ANCORAS = [
    ("a00", "Qual é a altura"), ("a01", "Pra descobrir"),
    ("a02", "No topo, peso"), ("a03", "Juntos, dão"), ("a04", "Como a pista"),
    ("a05", "No limite ela zera"), ("a06", "velocidade no topo ao quadrado igual"),
    ("a07", "Agora a energia"), ("a08", "No início, ela"), ("a09", "No topo, a partícula"),
    ("a10", "Troca velocidade"), ("a10b", "corta massa"), ("a11", "dois mais meio"),
    ("a12", "Logo, a altura"), ("a12b", "dois e meio vezes"),
    ("a14", "Agora, a esfera"), ("a15", "A condição no topo muda"), ("a16", "Não. As mesmas"),
    ("a17", "O que muda é a energia"), ("a18", "A esfera também gira"), ("a19", "Quanto ele vale"),
    ("a20", "Divida a esfera"), ("a21", "Para um disco"), ("a22", "Então o raio do disco"),
    ("a23", "A massa do disco"), ("a23b", "e o volume é área"), ("a24", "O momento de inércia desse"),
    ("a25", "Substituindo, os dois"),
    ("a26", "Agora somamos"), ("a27", "A integral dá"), ("a28", "Pela massa total"),
    ("a29", "Os pi cancelam"), ("a30", "Sobra: dois quintos"),
    ("a31", "De volta à energia"), ("a32", "Substituímos o momento"), ("a32b", "a velocidade angular é"),
    ("a33", "Os raios se cancelam"), ("a34", "Somando rotação"),
    ("a35", "Desses sete décimos"), ("a36", "Descendo, potencial"),
    ("a37", "Agora a altura mínima"), ("a38", "No topo, a velocidade é a mesma"),
    ("a39", "A diferença é"), ("a40", "Substitui a condição"), ("a40b", "corta massa e gravidade e soma"),
    ("a41", "vinte e sete décimos"), ("a41b", "ou dois vírgula sete"),
    ("a42", "Soltando a esfera"),
    ("a44", "Por que a esfera precisa"),
]
# instantes extras (o fecho do vídeo os lê direto de sync.json; não são âncoras do motor)
EXTRAS = [("a45", "A velocidade mínima"), ("a45b", "mas parte da energia"), ("a46", "Mais energia, mais altura"),
          ("a47", "Se curtiu")]

PUNCT = {",": 0.9, ":": 1.0, ";": 1.0, ".": 1.6, "?": 1.6}


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
    peso = np.array([silabas(p) + 0.3 + PUNCT.get(p[-1], 0.0) for p in palavras])
    cum = np.cumsum(peso)
    fim_pal = t0 + cum / cum[-1] * (t1 - t0)          # previsão do fim de cada palavra
    limites = [i for i, p in enumerate(palavras) if p[-1] in PUNCT]   # índice da palavra que antecede a pausa
    cand = [(a, b) for a, b in runs]

    # fim de cada frase: programação dinâmica pelo ritmo (sílabas/s parecido entre frases)
    fins = [i for i, p in enumerate(palavras) if p[-1] in ".?"]
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
                    if dt < 0.2:
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

    def dp(pred):
        B, P = len(limites), len(cand)
        INF = 1e9
        skip = [1.2 if palavras[i][-1] == "," else (INF if i in forcado else 4.0) for i in limites]
        best = np.full((B + 1, P + 1), INF)           # best[j][k]: j limites tratados, último par usa pausa < k
        best[0, :] = 0
        back = {}
        for j in range(1, B + 1):
            for k in range(P + 1):
                # pular o limite j
                c0 = best[j - 1][k] + skip[j - 1]
                best[j][k], back[(j, k)] = c0, ("skip", k)
            for k in range(1, P + 1):
                dev = (pred[limites[j - 1]] - cand[k - 1][0]) / 0.6
                dur = cand[k - 1][1] - cand[k - 1][0]
                if limites[j - 1] in forcado:
                    c = best[j - 1][k - 1] if cand[k - 1] == forcado[limites[j - 1]] else INF
                    if c < best[j][k]:
                        best[j][k], back[(j, k)] = c, ("use", k - 1)
                    if best[j][k - 1] < best[j][k]:
                        best[j][k], back[(j, k)] = best[j][k - 1], ("shift", k - 1)
                    continue
                fim_frase = palavras[limites[j - 1]][-1] in ".?"
                if fim_frase and dur < 0.2:
                    c = INF                            # fim de frase tem pausa de verdade
                else:
                    extra = max(0.0, 0.4 - dur) * 6 if fim_frase else 0.0
                    c = best[j - 1][k - 1] + dev ** 2 + extra if abs(dev) < 3.5 else INF
                if c < best[j][k]:
                    best[j][k], back[(j, k)] = c, ("use", k - 1)
                if best[j][k - 1] < best[j][k]:
                    best[j][k], back[(j, k)] = best[j][k - 1], ("shift", k - 1)
        j, k, uso = B, P, {}
        while j > 0:
            acao, k2 = back[(j, k)]
            if acao == "use":
                uso[limites[j - 1]] = cand[k - 1]
                j, k = j - 1, k2
            elif acao == "skip":
                j = j - 1
            else:
                k = k2
        return uso

    pred = fim_pal.copy()
    for _ in range(3):                                 # re-prever entre limites já ancorados
        uso = dp(pred)
        xs = [t0] + [uso[i][0] for i in sorted(uso)] + [t1]
        ps = [0.0] + [cum[i] for i in sorted(uso)] + [cum[-1]]
        pred = np.interp(cum, ps, xs)
    uso = dp(pred)

    # tempos de cada palavra: dentro de cada trecho (entre pausas ancoradas), proporcional ao peso
    marcos = sorted(uso)
    ini_w, fim_w = np.zeros(len(palavras)), np.zeros(len(palavras))
    a_prev, i_prev = t0, 0
    for i in marcos + [len(palavras) - 1]:
        a_fim = uso[i][0] if i in uso else t1
        seg = peso[i_prev:i + 1]
        edges = a_prev + np.concatenate([[0], np.cumsum(seg)]) / seg.sum() * (a_fim - a_prev)
        ini_w[i_prev:i + 1], fim_w[i_prev:i + 1] = edges[:-1], edges[1:]
        if i in uso:
            a_prev = uso[i][1]
        i_prev = i + 1

    # âncoras
    extras = {}
    saida, pos = [], 0
    norm = lambda q: re.sub(r"[^\wáéíóúâêôãõàç]", "", q.lower())
    low = [norm(p) for p in palavras]
    for nome, trecho in ANCORAS:
        alvo = [norm(q) for q in trecho.split()]
        for j in range(pos, len(palavras) - len(alvo) + 1):
            if low[j:j + len(alvo)] == alvo:
                saida.append([nome, round(max(0.0, float(ini_w[j]) - LEAD), 2)])
                pos = j + 1
                break
        else:
            raise SystemExit(f"Trecho não encontrado: {nome}: {trecho!r}")
    for nome, trecho in EXTRAS:
        alvo = [norm(q) for q in trecho.split()]
        for j in range(pos, len(palavras) - len(alvo) + 1):
            if low[j:j + len(alvo)] == alvo:
                extras[nome] = round(float(ini_w[j]), 2)
                pos = j + 1
                break
        else:
            raise SystemExit(f"Trecho não encontrado: {nome}: {trecho!r}")
    saida.append(["fim", round(float(min(dur, t1 + 0.35)), 2)])
    assert all(a[1] < b[1] for a, b in zip(saida, saida[1:])), "âncoras fora de ordem"
    json.dump({"anchors": saida, "extras": extras}, open(PASTA / "sync.json", "w"), indent=1)

    # diagnóstico: ritmo (sílabas/s) por frase
    print(f"áudio {dur:.2f} s; fala {t0:.2f}–{t1:.2f}; {len(runs)} pausas; {len(uso)}/{len(limites)} limites ancorados")
    ini_f = 0
    for i, p in enumerate(palavras):
        if p[-1] in ".?":
            sil = sum(silabas(q) for q in palavras[ini_f:i + 1])
            d = fim_w[i] - ini_w[ini_f]
            print(f"  {ini_w[ini_f]:7.2f}–{fim_w[i]:7.2f}  {sil / d:4.1f} síl/s  {' '.join(palavras[ini_f:i + 1])[:60]}")
            ini_f = i + 1

    # legenda: no máximo 2 linhas, largura <= 446 px (a 540 de largura), cues curtas
    fonte = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 29)
    larg = lambda s: fonte.getlength(s)
    MAXW = 440

    def quebra(ws):
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
        ws = palavras[a_:b_ + 1]
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
        if p[-1] in ".?" or i == len(palavras) - 1:
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
        fim = float(fim_w[c[-1]]) + (0.12 if palavras[c[-1]][-1] in ".?" else 0.0)
        if n_ < len(cues):
            fim = min(fim, float(ini_w[cues[n_][0]]) - 0.02)
        fim = max(fim, ini + 0.4)
        ant = fim
        ts = lambda t: f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)):03d}"
        linhas = quebra([palavras[q] for q in c])
        srt.append(f"{n_}\n{ts(ini)} --> {ts(fim)}\n" + "\n".join(linhas))
    (PASTA / "legenda.srt").write_text("\n\n".join(srt) + "\n", encoding="utf-8")
    print(f"legenda.srt: {len(srt)} cues; sync.json: {len(saida)} âncoras")


if __name__ == "__main__":
    main()
