"""Alinha a narração do vid_0013 ao áudio, monta os respiros e gera sync.json (âncoras) e legenda.srt.

Motor de alinhamento do vid_0012 (sem ASR): as palavras recebem peso por sílabas, os limites de pontuação são
ancorados nas pausas medidas no WAV (programação dinâmica) e o resto é interpolado dentro de cada trecho.

Montagem (orientação da Produção): onde a cena precisa de mais tempo que a fala — integração, álgebra de C,
fatoração, separatriz — insere-se silêncio numa pausa medida da fala, em vez de comprimir a animação. Cada trecho
entre âncoras dura no mínimo LO × o tempo nominal (native.json). Saídas: audio/narracao_montagem.wav (fonte intacta em
audio/narracao_final.wav), montagem.json (receita), sync.json (tempos já na montagem) e legenda.srt (escrita
matemática limpa: ℓ, x(t), F0ℓ/4, ±ℓ, x², x⁴, mv², Ub — sem a grafia usada pelo TTS).
Uso: uv run python videos/vid_0013_potencial_poco_duplo/gerar_sync.py
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
MONTAGEM = PASTA / "audio" / "narracao_montagem.wav"
CAUDA = 1.2           # o último quadro segura depois do fim da fala

# (nome, trecho do texto onde a âncora cai). Em ordem; cada trecho é procurado depois do anterior.
ANCORAS = [
    ("a1", "Essa partícula"), ("a2", "Dá para descobrir"), ("a3", "A seta mostra"), ("a4", "A força depende"),
    ("a5", "Ela se anula"), ("a6", "em x igual a zero"), ("a7", "Em x igual a L"), ("a8", "positiva, para a direita"),
    ("a9", "Cada ponto do gráfico"), ("a10", "Trocar o sinal"), ("a11", "Perto de L"), ("a12", "perto do centro"),
    ("a13", "Que potencial gera"),
    ("b1", "A força é menos"), ("b2", "então o potencial é menos"), ("b3", "Substituímos a força"),
    ("b4", "tiramos F zero"), ("b5", "e integramos termo"), ("b6", "x ao quadrado sobre dois"),
    ("b7", "e x à quarta sobre quatro"), ("b8", "Ao distribuir"), ("b9", "menos com menos"),
    ("c1", "E a constante"), ("c2", "Somar uma constante"), ("c3", "Escolhemos potencial zero"),
    ("c4", "Somando F zero"), ("c5", "a constante vale"),
    ("d1", "Com a constante no lugar"), ("d2", "colocamos F zero"), ("d3", "e aparece um quadrado"),
    ("d4", "o quadrado da razão"),
    ("e1", "São dois mínimos"), ("e2", "Onde a força é positiva"), ("e3", "A segunda derivada"),
    ("f1", "Em uma dimensão"), ("f2", "a cinética é a diferença"), ("f3", "Ela vale um meio"),
    ("f4", "Então só são permitidas"), ("f5", "Cada condição inicial"),
    ("g1", "Com a referência escolhida"), ("g2", "Abaixo da barreira"), ("g3", "Com energia exatamente"),
    ("g5", "Acima da barreira"), ("h1", "A energia decide"),
]
# fração mínima do tempo nominal de cada trecho (âncora -> próxima); abaixo disso entra silêncio na montagem
LO_PAD = 0.55
# protegidos pela Produção: integração (b*) e separatriz (g3); álgebra de C e fatoração com piso intermediário
LO = {"a7": 0.7, "b1": 0.95, "b2": 0.95, "b3": 0.95, "b4": 0.95, "b5": 0.95, "b6": 0.95, "b7": 0.95,
      "b8": 0.95, "b9": 0.9, "c3": 0.7, "c4": 0.8, "d1": 0.7, "d2": 0.7, "d3": 0.7, "d4": 0.7,
      "e1": 0.7, "e2": 0.7, "e3": 0.7, "g2": 0.6, "g3": 1.0}
# legenda: grafia do TTS -> escrita matemática (o bloco de legenda nunca corta uma expressão)
LEGENDA = [
    ("x de tê", "x(t)"), ("F zero L sobre quatro", "F0ℓ/4"), ("três oitavos de F zero", "3F0/8"),
    ("x ao quadrado sobre dois", "x²/2"), ("x à quarta sobre quatro", "x⁴/4"), ("eme vê ao quadrado", "mv²"),
    ("mais ou menos L", "±ℓ"), ("mais e menos L", "±ℓ"), ("L sobre dois", "ℓ/2"), ("vê ao quadrado", "v²"),
    ("x à quarta", "x⁴"), ("F zero", "F0"), ("U bê", "Ub"), ("L", "ℓ"),
]
EXTRAS = []
PAUSAS_FIXAS = []     # (trecho que termina na pontuação, início da pausa em s), se o alinhador errar alguma

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
        bruto = w.readframes(n)
        x = np.frombuffer(bruto, dtype=np.int16).astype(float)
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
    for trecho, t_p in PAUSAS_FIXAS:
        alvo = trecho.split()
        i = next(j + len(alvo) - 1 for j in range(len(palavras)) if palavras[j:j + len(alvo)] == alvo)
        forcado[i] = min(cand, key=lambda c: abs(c[0] - t_p))

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
    # montagem: silêncio onde a cena precisa de mais tempo que a fala (dentro de uma pausa medida)
    nat = json.load(open(PASTA / "native.json", encoding="utf-8"))
    av = dict(saida)
    nomes = [n_ for n_, _ in ANCORAS]
    ins = []
    for a_, b_ in zip(nomes, nomes[1:]):
        v, nn = av[b_] - av[a_], nat[b_] - nat[a_]
        need = LO.get(a_, LO_PAD) * nn - v
        if need > 0.05:
            cands = [r for r in runs if av[a_] < r[1] <= av[b_] + 0.05]
            if not cands:                      # sem pausa medida no trecho: não corta a fala (a cena comprime)
                print(f"  sem pausa para respiro em {a_}->{b_} ({need:.2f} s): a cena comprime")
                continue
            r = max(cands, key=lambda r: r[1])
            ins.append((round((r[0] + r[1]) / 2, 3), round(need, 3), a_, b_))
    sh = lambda t: float(t + sum(d for ti, d, *_ in ins if ti <= t))
    ini_w = np.array([sh(t) for t in ini_w])
    fim_w = np.array([sh(t) for t in fim_w])
    saida = [[n_, round(sh(t), 2)] for n_, t in saida]
    fim = round(sh(t1) + CAUDA, 2)
    saida.append(["fim", fim])
    assert all(a[1] < b[1] for a, b in zip(saida, saida[1:])), "âncoras fora de ordem"
    json.dump({"anchors": saida, "extras": extras}, open(PASTA / "sync.json", "w"), indent=1)
    amost = np.frombuffer(bruto, dtype=np.int16).reshape(-1, ch)
    pedacos, ult = [], 0
    for t_ins, d, *_ in sorted(ins):
        k = int(round(t_ins * sr))
        pedacos += [amost[ult:k], np.zeros((int(round(d * sr)), ch), dtype=np.int16)]
        ult = k
    pedacos.append(amost[ult:])
    with wave.open(str(MONTAGEM), "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(np.concatenate(pedacos).tobytes())
    receita = [{"t_fonte_s": t, "silencio_s": d, "trecho": f"{a_}->{b_}"} for t, d, a_, b_ in ins]
    json.dump({"fonte": "audio/narracao_final.wav", "saida": "audio/narracao_montagem.wav",
               "duracao_fonte_s": round(dur, 2), "silencio_total_s": round(sum(d for _, d, *_ in ins), 2),
               "insercoes": receita}, open(PASTA / "montagem.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"montagem: {len(ins)} respiros, +{sum(d for _, d, *_ in ins):.2f} s; fala termina em {sh(t1):.2f} s; "
          f"vídeo ≈ {fim:.2f} s")
    for t, d, a_, b_ in ins:
        print(f"  respiro {d:5.2f} s em {t:7.2f} s (fonte)  {a_}->{b_}")

    # diagnóstico: ritmo (sílabas/s) por frase
    print(f"áudio {dur:.2f} s; fala {t0:.2f}–{t1:.2f}; {len(runs)} pausas; {len(uso)}/{len(limites)} limites ancorados"
          " (tempos abaixo já na montagem)")
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

    # grafia do TTS -> escrita matemática; as palavras seguintes de uma expressão ficam vazias e indivisíveis
    nobreak = [False] * len(palavras)
    i = 0
    while i < len(palavras):
        for fala, escrita in LEGENDA:
            alvo = [norm(q) for q in fala.split()]
            k = len(alvo)
            if low[i:i + k] == alvo:
                pont = re.search(r"[^\wáéíóúâêôãõàçê]*$", palavras[i + k - 1]).group(0)
                pal_leg[i] = (escrita[0].upper() + escrita[1:] if palavras[i][0].isupper() and escrita[0].isalpha()
                              and escrita[0].islower() and escrita != "x(t)" else escrita) + pont
                for q in range(i + 1, i + k):
                    pal_leg[q] = ""
                for q in range(i, i + k - 1):
                    nobreak[q] = True
                i += k
                break
        else:
            i += 1

    def quebra(ws):
        ws = [w_ for w_ in ws if w_]
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
        if nobreak[b_] or (a_ > 0 and nobreak[a_ - 1]):
            return None
        ws = [w_ for w_ in pal_leg[a_:b_ + 1] if w_]
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
        linhas = quebra([pal_leg[q] for q in c])
        srt.append(f"{n_}\n{ts(ini)} --> {ts(fim)}\n" + "\n".join(linhas))
    (PASTA / "legenda.srt").write_text("\n\n".join(srt) + "\n", encoding="utf-8")
    print(f"legenda.srt: {len(srt)} cues; sync.json: {len(saida)} âncoras")


if __name__ == "__main__":
    main()
