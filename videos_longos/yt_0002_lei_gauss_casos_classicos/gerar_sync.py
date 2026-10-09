"""yt_0002 — alinha a narração ao áudio (3 partes do ElevenLabs), gera o mapa tempo-editorial → tempo-da-voz, o áudio de montagem e a legenda.

Sem ASR (como no yt_0001 e nos vídeos 8, 9 e 12): as palavras recebem peso por sílabas, os fins de frase são ancorados nas
pausas medidas no WAV (programação dinâmica) e o resto é interpolado dentro de cada trecho.

Diferença para o yt_0001: a cena do yt_0002 foi escrita com marcos editoriais absolutos (at(t), t em segundos do orçamento de 18:01).
Cada linha da tabela de `narracao_sugestao.md` (tempo editorial + fala) vira um nó [t_editorial, t_voz]; a cena converte cada at(t)
pelo mapa linear por partes desses nós (sync.json → "knots").

  uv run --no-sync python videos_longos/yt_0002_lei_gauss_casos_classicos/gerar_sync.py alinhar
      → audio/narracao_final.wav (as 3 partes intactas, com pausa entre elas) e sync.json
  uv run --no-sync python videos_longos/yt_0002_lei_gauss_casos_classicos/gerar_sync.py montar
      → audio/narracao_montagem.wav (pausas extras pedidas pela cena em pads.json; a fala não é alterada) e legenda.srt
"""

import json
import re
import sys
import wave
from pathlib import Path

import numpy as np

PASTA = Path(__file__).resolve().parent
AUD = PASTA / "audio"
PARTES = sorted((AUD / "partes").glob("narracao_parte*.wav"))     # uma por bloco de texto (texto_narracao_bloco1..N.txt)
FINAL = AUD / "narracao_final.wav"
MONTAGEM = AUD / "narracao_montagem.wav"
GAP = 0.9                                   # pausa entre as partes (as partes têm bordas de ~0,15 s)
PARAGRAFOS = (PASTA / "texto_narracao.txt").read_text(encoding="utf-8").strip().split("\n\n")
_cortes = json.loads((PASTA / "blocos_texto.json").read_text(encoding="utf-8"))      # índices dos parágrafos onde cada bloco enviado ao ElevenLabs começa/termina
PARTE_DE = [k for k, (i0, i1) in enumerate(zip(_cortes, _cortes[1:])) for _ in range(i0, i1)]
assert len(PARTE_DE) == len(PARAGRAFOS), "blocos_texto.json não bate com texto_narracao.txt"
assert len(PARTES) == len(_cortes) - 1, f"{len(PARTES)} WAV em audio/partes, mas o texto tem {len(_cortes) - 1} blocos"
T_FIM_EDITORIAL = 1081.0                    # fim do orçamento editorial (T_FIM da cena)
CAUDA_FINAL = 1.5                           # s de cena depois da última palavra


def linhas_roteiro():
    """[(t_editorial_s, n_palavras)] de cada linha falada de narracao_sugestao.md, na mesma regra que gerou texto_narracao.txt."""
    s = (PASTA / "narracao_sugestao.md").read_text(encoding="utf-8")
    s = s[s.index("## Narração por blocos de tempo"):s.index("## Contagem")]
    out = []
    for l in s.split("\n"):
        if l.startswith("|") and not l.startswith("|---") and not l.startswith("| Tempo"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            m = re.match(r"(\d+):(\d+)–", c[0])
            fala = re.sub(r"\*\([^)]*\)\*", "", c[-1]).replace("*", "").strip()
            if fala:
                out.append((int(m.group(1)) * 60 + int(m.group(2)), len(fala.split())))
    return out


PUNCT = {",": 0.9, ":": 1.0, ";": 1.0, ".": 1.6, "?": 1.6, "!": 1.6}
NORM = lambda q: re.sub(r"[^\wáéíóúâêôãõàçü]", "", q.lower())


def silabas(palavra):
    p = NORM(palavra)
    return max(1, len(re.findall(r"[aeiouáéíóúâêôãõàü]+", p)))


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
    return runs, t0, t1


def alinhar_parte(raw, sr, palavras):
    """Tempos (início, fim) de cada palavra numa parte; mesma lógica do vid_0012."""
    x = raw.astype(float).mean(1)
    x /= np.abs(x).max()
    runs, t0, t1 = pausas(x, sr)
    runs = [r for r in runs if r[0] > t0 + 0.05 and r[1] < t1 - 0.05]
    peso = np.array([silabas(p) + 0.3 + PUNCT.get(p[-1], 0.0) for p in palavras])
    cum = np.cumsum(peso)
    limites = [i for i, p in enumerate(palavras) if p[-1] in PUNCT]
    cand = list(runs)
    fins = [i for i, p in enumerate(palavras) if p[-1] in ".?!"]
    inicios = [0] + [i + 1 for i in fins[:-1]]
    sil_f = [sum(silabas(q) for q in palavras[a:b + 1]) for a, b in zip(inicios, fins)]
    R = sum(sil_f) / (t1 - t0 - 0.3 * len(fins))

    # fins de frase: programação dinâmica pelo ritmo (sílabas/s parecido entre frases)
    F, P, INF = len(fins), len(cand), 1e12
    best = np.full((F, P + 1), INF)
    back = {}
    for i in range(F):
        for k in (range(P) if i < F - 1 else [P]):
            a_fim = cand[k][0] if k < P else t1
            if i == 0:
                dt = a_fim - t0
                best[i][k] = ((sil_f[0] / dt - R) / (0.2 * R)) ** 2 if dt > 0.2 else INF
                continue
            for j in range(P):
                if best[i - 1][j] >= INF or cand[j][1] >= a_fim:
                    continue
                dt = a_fim - cand[j][1]
                if dt < 0.2:
                    continue
                c = best[i - 1][j] + ((sil_f[i] / dt - R) / (0.2 * R)) ** 2 + max(0.0, 0.3 - (cand[j][1] - cand[j][0])) * 8
                if c < best[i][k]:
                    best[i][k], back[(i, k)] = c, j
    k, forcado = P, {}
    for i in range(F - 1, 0, -1):
        j = back[(i, k)]
        forcado[fins[i - 1]] = cand[j]
        k = j

    # dentro de cada frase: quais pausas são as vírgulas. Programação dinâmica pelo ritmo dos trechos entre pausas
    # (sílabas/s parecido com o da parte); vírgula sem pausa é permitida, com custo pequeno.
    fala_total = (t1 - t0) - sum(r[1] - r[0] for r in runs)
    Rf = sum(silabas(q) for q in palavras) / fala_total             # ritmo da fala sem as pausas
    ini_w, fim_w = np.zeros(len(palavras)), np.zeros(len(palavras))
    peso_w = np.array([silabas(q) + 0.3 for q in palavras])
    n_usadas = 0
    for f, (a0, a1) in enumerate(zip(inicios, fins)):
        s0 = t0 if f == 0 else forcado[fins[f - 1]][1]
        s1 = forcado[a1][0] if a1 in forcado else t1
        internas = [r for r in cand if s0 + 0.05 < r[0] and r[1] < s1 - 0.05]
        bnds = [i for i in range(a0, a1) if palavras[i][-1] in ",:;"]          # vírgulas internas (palavra antes)
        # trechos: palavras entre fronteiras consecutivas
        cortes = [a0 - 1] + bnds + [a1]
        sil_t = [sum(silabas(q) for q in palavras[cortes[j] + 1:cortes[j + 1] + 1]) for j in range(len(cortes) - 1)]
        m, Q = len(bnds), len(internas)
        # estado: (fronteira j usada, pausa q) ; fronteira 0 = início da frase (s0), m+1 = fim (s1)
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
                    pen_puladas = 0.35 * (j - jj - 1)                            # vírgulas sem pausa no meio
                    pen_sobra = 0.25 * max(0, (q - qq - 1))                      # pausas internas não usadas (respiros)
                    c = cst + ((sil / dur - Rf) / (0.3 * Rf)) ** 2 * (j - jj) + pen_puladas + pen_sobra
                    if melhor is None or c < melhor[0]:
                        melhor = (c, (jj, qq))
                if melhor:
                    best[(j, q)] = melhor
        # reconstrução
        chave = (m + 1, Q + 1)
        if chave not in best:                                                   # sem solução: proporcional
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
    print(f"  fala {t0:.2f}–{t1:.2f} s; {len(runs)} pausas; {len(fins)} frases; {n_usadas} vírgulas em pausa; "
          f"ritmo {Rf:.2f} síl/s")
    return ini_w, fim_w, runs


def alinhar():
    palavras, ini, fim, par, pausas_abs = [], [], [], [], []
    audio, off = [], 0.0
    sr0 = None
    for k, path in enumerate(PARTES):
        raw, sr = ler(path)
        sr0 = sr0 or sr
        assert sr == sr0
        pals = [(w, pi) for pi, p in enumerate(PARAGRAFOS) if PARTE_DE[pi] == k for w in p.split()]
        print(f"parte {k + 1}: {len(raw) / sr:.2f} s, {len(pals)} palavras")
        a, b, runs = alinhar_parte(raw, sr, [w for w, _ in pals])
        palavras += [w for w, _ in pals]
        par += [pi for _, pi in pals]
        ini += list(a + off)
        fim += list(b + off)
        pausas_abs += [(r0 + off, r1 + off) for r0, r1 in runs]
        audio.append(raw)
        off += len(raw) / sr
        if k < len(PARTES) - 1:
            pausas_abs.append((off - 0.15, off + GAP))
            audio.append(np.zeros((int(round(GAP * sr)), raw.shape[1]), dtype=np.int16))
            off += GAP
    full = np.concatenate(audio)
    with wave.open(str(FINAL), "wb") as w:
        w.setnchannels(full.shape[1]); w.setsampwidth(2); w.setframerate(sr0)
        w.writeframes(full.tobytes())

    # nós do mapa: início de cada linha do roteiro (tempo editorial) ↔ início da primeira palavra dela na voz
    linhas = linhas_roteiro()
    assert sum(n for _, n in linhas) == len(palavras), f"roteiro tem {sum(n for _, n in linhas)} palavras; texto_narracao.txt tem {len(palavras)}"
    knots, w0 = [], 0
    for t_ed, n in linhas:
        knots.append([float(t_ed), round(float(ini[w0]), 3)])
        w0 += n
    knots.append([T_FIM_EDITORIAL, round(float(fim[-1]) + CAUDA_FINAL, 3)])
    assert all(a[0] < b[0] and a[1] < b[1] for a, b in zip(knots, knots[1:])), "nós fora de ordem"
    json.dump({"audio": FINAL.name, "dur": round(len(full) / sr0, 3), "knots": knots,
               "words": [[p, round(float(x), 3), round(float(y), 3)] for p, x, y in zip(palavras, ini, fim)],
               "pauses": [[round(a, 3), round(b, 3)] for a, b in pausas_abs]},
              open(PASTA / "sync.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"narracao_final.wav: {len(full) / sr0:.2f} s; sync.json: {len(knots)} nós")
    razao = [(b[1] - a[1]) / (b[0] - a[0]) for a, b in zip(knots, knots[1:])]
    print(f"voz / orçamento editorial por trecho: min {min(razao):.2f}, mediana {sorted(razao)[len(razao) // 2]:.2f}, máx {max(razao):.2f}")
    ini_f = 0
    for i, p in enumerate(palavras):
        if p[-1] in ".?!":
            sil = sum(silabas(q) for q in palavras[ini_f:i + 1])
            print(f"  {ini[ini_f]:7.2f}–{fim[i]:7.2f}  {sil / (fim[i] - ini[ini_f]):4.1f} síl/s  {' '.join(palavras[ini_f:i + 1])[:58]}")
            ini_f = i + 1


def grafia_legenda(palavras):
    """Texto do TTS → grafia normal da legenda (a fonética só existe para a voz)."""
    out = []
    for i, p in enumerate(palavras):
        out.append(p)
    return out


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


if __name__ == "__main__":
    {"alinhar": alinhar, "montar": montar}[sys.argv[1]]()
