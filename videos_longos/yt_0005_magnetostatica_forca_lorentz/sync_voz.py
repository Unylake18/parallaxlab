"""yt_0005 — alinha a narração (audio/narracao_v4.wav, um único WAV) ao texto e gera sync.json.

Sem ASR (mesmo método do yt_0001/yt_0002): as palavras recebem peso por sílabas, os fins de frase são ancorados nas pausas medidas no
WAV (programação dinâmica, aqui em FAIXA em torno do instante esperado, porque o áudio tem 25 min) e as vírgulas, nas pausas internas.

  uv run --no-sync python videos_longos/yt_0005_magnetostatica_forca_lorentz/sync_voz.py
      → sync.json: palavras (início, fim), pausas e `celulas`: instante em que começa a fala de cada célula de narracao_sugestao.md
"""
import json
import re
import sys
import wave
from pathlib import Path

import numpy as np

PASTA = Path(__file__).resolve().parent
AUDIO = PASTA / "audio" / "narracao_v4.wav"
PUNCT = {",": 0.9, ":": 1.0, ";": 1.0, ".": 1.6, "?": 1.6, "!": 1.6}
NORM = lambda q: re.sub(r"[^\wáéíóúâêôãõàçü]", "", q.lower())


def silabas(palavra):
    p = NORM(palavra)
    return max(1, len(re.findall(r"[aeiouáéíóúâêôãõàü]+", p)))


def celulas_fala():
    """[(chave, texto)] das células com fala (as marcadas com '—' não iniciam fala), na ordem do roteiro."""
    out, sec = [], ""
    for ln in (PASTA / "narracao_sugestao.md").read_text(encoding="utf-8").split("\n"):
        if ln.startswith("## ") or ln.startswith("### "):
            sec = ln.strip("# ").split(" — ")[0].strip()
        if re.match(r"\|\s*\d+:\d+", ln):
            c = ln.strip()[2:-2].split(" | ")
            if c[2] != "—":
                out.append((f"{sec} {c[0].strip()}", c[2]))
    return out


def ler(path):
    with wave.open(str(path)) as w:
        n, sr, ch = w.getnframes(), w.getframerate(), w.getnchannels()
        raw = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, ch)
    return raw, sr


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
    return runs, t0, t1, e


def alinhar(raw, sr, palavras):
    x = raw.astype(float).mean(1)
    x /= np.abs(x).max()
    runs, t0, t1, env = pausas(x, sr)
    runs = [r for r in runs if r[0] > t0 + 0.05 and r[1] < t1 - 0.05]
    cand = list(runs)
    P = len(cand)
    fins = [i for i, p in enumerate(palavras) if p[-1] in ".?!"]
    inicios = [0] + [i + 1 for i in fins[:-1]]
    F = len(fins)
    sil_f = np.array([sum(silabas(q) for q in palavras[a:b + 1]) for a, b in zip(inicios, fins)], dtype=float)
    R = sil_f.sum() / (t1 - t0 - 0.3 * F)
    print(f"fala {t0:.2f}–{t1:.2f} s; {P} pausas; {F} frases; ritmo médio {R:.2f} síl/s")
    ini_c = np.array([c[0] for c in cand])
    fim_c = np.array([c[1] for c in cand])
    INF = 1e12

    def dp(esperado, larg):
        """DP sobre os fins de frase; para a frase i só valem pausas em esperado[i] ± larg (s)."""
        cands = []
        for i in range(F):
            if i == F - 1:
                cands.append([P])
            else:
                ks = np.nonzero((fim_c > esperado[i] - larg) & (ini_c < esperado[i] + larg))[0].tolist()
                cands.append(ks if ks else [int(np.argmin(np.abs(ini_c - esperado[i])))])
        best = [dict() for _ in range(F)]
        back = [dict() for _ in range(F)]
        for i in range(F):
            for k in cands[i]:
                a_fim = ini_c[k] if k < P else t1
                if i == 0:
                    dt = a_fim - t0
                    best[0][k] = ((sil_f[0] / dt - R) / (0.2 * R)) ** 2 if dt > 0.2 else INF
                    continue
                bc, bj = INF, None
                for j, cj in best[i - 1].items():
                    if cj >= INF or fim_c[j] >= a_fim:
                        continue
                    dt = a_fim - fim_c[j]
                    if dt < 0.2:
                        continue
                    c = cj + ((sil_f[i] / dt - R) / (0.2 * R)) ** 2 + max(0.0, 0.3 - (fim_c[j] - ini_c[j])) * 8
                    if c < bc:
                        bc, bj = c, j
                if bj is not None:
                    best[i][k], back[i][k] = bc, bj
        if P not in best[F - 1]:
            sys.exit("DP sem solução (ajuste a faixa)")
        k, sel = P, {}
        for i in range(F - 1, 0, -1):
            j = back[i][k]
            sel[i - 1] = j
            k = j
        return sel, best[F - 1][P]

    # 1ª passada: esperado proporcional às sílabas (faixa larga); 2ª: esperado a partir da solução (faixa estreita)
    cum = np.cumsum(sil_f + 0.3 * R)
    esperado = t0 + cum / cum[-1] * (t1 - t0)
    for larg in (60.0, 25.0, 12.0):
        sel, custo = dp(esperado, larg)
        esperado = np.array([ini_c[sel[i]] if i in sel else t1 for i in range(F)])
        print(f"  faixa ±{larg:.0f} s: custo {custo:.1f}")
    forcado = {fins[i]: cand[sel[i]] for i in sel}

    # vírgulas dentro de cada frase (idêntico ao yt_0002)
    fala_total = (t1 - t0) - sum(r[1] - r[0] for r in runs)
    Rf = sum(silabas(q) for q in palavras) / fala_total
    ini_w, fim_w = np.zeros(len(palavras)), np.zeros(len(palavras))
    peso_w = np.array([silabas(q) + 0.3 for q in palavras])
    n_usadas = 0
    for f, (a0, a1) in enumerate(zip(inicios, fins)):
        s0 = t0 if f == 0 else forcado[fins[f - 1]][1]
        s1 = forcado[a1][0] if a1 in forcado else t1
        internas = [r for r in cand if s0 + 0.05 < r[0] and r[1] < s1 - 0.05]
        bnds = [i for i in range(a0, a1) if palavras[i][-1] in ",:;"]
        cortes = [a0 - 1] + bnds + [a1]
        sil_t = [sum(silabas(q) for q in palavras[cortes[j] + 1:cortes[j + 1] + 1]) for j in range(len(cortes) - 1)]
        m, Q = len(bnds), len(internas)
        pts = [(s0, s0)] + internas + [(s1, s1)]
        best = {(0, 0): (0.0, None)}
        for j in range(1, m + 2):
            for q in (range(1, Q + 1) if j <= m else [Q + 1]):
                melhor = None
                for (jj, qq), (cst, _) in best.items():
                    if jj >= j or qq >= q:
                        continue
                    dur = pts[q][0] - pts[qq][1]
                    sil = sum(sil_t[jj:j])
                    if dur < 0.12 * (j - jj):
                        continue
                    c = cst + ((sil / dur - Rf) / (0.3 * Rf)) ** 2 * (j - jj) + 0.35 * (j - jj - 1) + 0.25 * max(0, (q - qq - 1))
                    if melhor is None or c < melhor[0]:
                        melhor = (c, (jj, qq))
                if melhor:
                    best[(j, q)] = melhor
        chave = (m + 1, Q + 1)
        if chave not in best:
            usados = [(0, 0), (m + 1, Q + 1)]
        else:
            usados = [chave]
            while best[usados[-1]][1] is not None:
                usados.append(best[usados[-1]][1])
            usados = usados[::-1]
        n_usadas += len(usados) - 2
        for (j0, q0), (j1, q1) in zip(usados, usados[1:]):
            w0, w1 = cortes[j0] + 1, cortes[j1]
            ta, tb = pts[q0][1], pts[q1][0]
            seg = peso_w[w0:w1 + 1]
            edges = ta + np.concatenate([[0], np.cumsum(seg)]) / seg.sum() * (tb - ta)
            ini_w[w0:w1 + 1], fim_w[w0:w1 + 1] = edges[:-1], edges[1:]
    print(f"  {n_usadas} vírgulas em pausa; ritmo sem pausas {Rf:.2f} síl/s")
    return ini_w, fim_w, runs, (t0, t1), x, env


def main():
    cels = celulas_fala()
    palavras, cel_ini = [], []
    for chave, texto in cels:
        cel_ini.append(len(palavras))
        palavras += texto.split()
    print(f"{len(cels)} células com fala, {len(palavras)} palavras")
    raw, sr = ler(AUDIO)
    print(f"áudio: {len(raw) / sr:.2f} s")
    ini, fim, runs, (t0, t1), x, env = alinhar(raw, sr, palavras)

    # ajuste fino: o início de cada célula é puxado para o ataque real da voz (primeiro instante em que a energia sobe depois da pausa)
    LIM = 0.03
    celulas = []
    for (chave, texto), j in zip(cels, cel_ini):
        t = float(ini[j])
        # procura, numa janela ±0,25 s, o fim da pausa mais próxima (onset)
        a, b = int(max(0, (t - 0.25) / 0.01)), int(min(len(env) - 1, (t + 0.25) / 0.01))
        on = [i for i in range(a + 1, b) if env[i - 1] < LIM <= env[i]]
        if on:
            i = min(on, key=lambda q: abs(q * 0.01 - t))
            t_on = i * 0.01
        else:
            t_on = t
        celulas.append({"chave": chave, "palavra": j, "t": round(t, 3), "onset": round(t_on, 3), "texto": texto[:70]})
    json.dump({"audio": AUDIO.name, "dur": round(len(raw) / sr, 3), "fala": [round(t0, 3), round(t1, 3)], "celulas": celulas,
               "words": [[p, round(float(a), 3), round(float(b), 3)] for p, a, b in zip(palavras, ini, fim)],
               "pauses": [[round(a, 3), round(b, 3)] for a, b in runs]},
              open(PASTA / "sync.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    d = [abs(c["onset"] - c["t"]) for c in celulas]
    print(f"sync.json: {len(celulas)} células | desvio médio onset×estimado {np.mean(d):.3f} s, máx {max(d):.3f} s")
    # relatório de ritmo por frase (sílabas por segundo): outliers denunciam alinhamento errado
    ini_f, rit = 0, []
    for i, p in enumerate(palavras):
        if p[-1] in ".?!":
            sil = sum(silabas(q) for q in palavras[ini_f:i + 1])
            rit.append((sil / max(0.05, fim[i] - ini[ini_f]), ini[ini_f], fim[i], " ".join(palavras[ini_f:i + 1])[:50]))
            ini_f = i + 1
    r = np.array([a[0] for a in rit])
    print(f"ritmo por frase: média {r.mean():.2f} síl/s, desvio {r.std():.2f}, mín {r.min():.2f}, máx {r.max():.2f}")
    for a in sorted(rit)[:5] + sorted(rit)[-5:]:
        print(f"  {a[0]:5.1f} síl/s  {a[1]:7.2f}–{a[2]:7.2f}  {a[3]}")


if __name__ == "__main__":
    main()
