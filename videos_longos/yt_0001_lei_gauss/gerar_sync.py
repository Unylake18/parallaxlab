"""yt_0001 — alinha a narração ao áudio (3 partes do ElevenLabs), gera âncoras, áudio de montagem e legenda.

Sem ASR (como nos vídeos 8, 9 e 12): as palavras recebem peso por sílabas, os fins de frase são ancorados nas
pausas medidas no WAV (programação dinâmica) e o resto é interpolado dentro de cada trecho.

  uv run --no-sync python videos_longos/yt_0001_lei_gauss/gerar_sync.py alinhar
      → audio/narracao_final.wav (as 3 partes intactas, com pausa de parágrafo entre elas) e sync.json
  uv run --no-sync python videos_longos/yt_0001_lei_gauss/gerar_sync.py montar
      → audio/narracao_montagem.wav (pausas extras pedidas pela cena em pads.json; a fala não é alterada)
        e legenda.srt (grafia normal, tempos da montagem)
"""

import json
import re
import sys
import wave
from pathlib import Path

import numpy as np

PASTA = Path(__file__).resolve().parent
AUD = PASTA / "audio"
PARTES = [AUD / "partes" / f"narracao_parte{i}.wav" for i in (1, 2, 3)]
FINAL = AUD / "narracao_final.wav"
MONTAGEM = AUD / "narracao_montagem.wav"
GAP = 0.9                                   # pausa de parágrafo entre as partes (as partes têm bordas de ~0,15 s)
PARAGRAFOS = (PASTA / "texto_narracao.txt").read_text(encoding="utf-8").strip().split("\n\n")
PARTE_DE = [0] * 5 + [1] * 4 + [2] * 4      # parágrafos 1–5 · 6–9 · 10–13
BLOCO_DE = list(range(1, 13)) + [12]        # o CTA (parágrafo 13) pertence ao bloco 12

# Âncoras: para cada bloco, um trecho por marco c[i] da cena (mesma ordem e quantidade de antes).
ANCORAS = {
    1: ["Olha esses dois problemas", "Nos dois, dá pra desenhar", "No primeiro, a distribuição", "No segundo, eu só tiro",
        "A lei continua verdadeira", "O fluxo continua determinado", "E mesmo assim", "Então, o que mudou"],
    2: ["Fala, pessoal", "Hoje a gente vai entender", "primeiro a fonte", "Pular essa ordem"],
    3: ["Antes de responder", "Pega um pedacinho", "De tão pequeno", "Agora, a normal", "Normal vezes área",
        "Numa superfície fechada, cada ponto", "Agora coloca esse pedaço", "Repara que aparecem dois ângulos",
        "De frente, o fluxo", "Inclinando, ele diminui", "Quando o campo passa tangente", "E se o campo entra",
        "É isso que o produto escalar", "E a integral fechada", "Dica: o fluxo não conta"],
    4: ["Agora coloca uma carga pontual positiva", "Pela Lei de Coulomb", "Na esfera, campo e vetor", "E como todo ponto",
        "Então dá pra tirar o campo", "e o fluxo vira o campo", "Agora olha as barras", "o campo cai com um sobre",
        "mas a área cresce", "Uma coisa compensa", "Por isso, qualquer esfera", "Ou seja, o fluxo mede"],
    5: ["Mas e se a superfície", "Imagina um cone", "Ele corta um pedaço", "Aqui entra uma ideia nova", "No plano, um ângulo",
        "No espaço, é a mesma ideia", "Na prática, o d ômega", "Se o pedaço está inclinado", "Área, inclinação e distância",
        "O d ômega é só tamanho", "E o fluxo pelo pedaço", "A distância sumiu", "Quatro pi esterradianos: a área",
        "Os quatro pi se cancelam", "Agora coloca a carga do lado de fora", "O campo na superfície não some",
        "em alguns pontos", "Mas cada feixe", "No total, o fluxo líquido", "Com várias cargas", "as de fora dão zero",
        "as de dentro dão", "Somando, aparece", "E chegamos à Lei de Gauss", "o fluxo por qualquer superfície"],
    6: ["Agora vem a parte mais importante", "Se a lei vale para qualquer", "Olha: eu desloco", "mas ela continua dentro",
        "O fluxo continua sendo", "exatamente", "Só que os pontos da esfera", "não estão mais à mesma distância",
        "Então o módulo do campo muda", "E quase nunca aponta", "Por isso esse passo", "Não dá pra tirar o campo",
        "A Lei de Gauss me deu", "Mas o campo na superfície é uma função", "Saber o fluxo não é saber"],
    7: ["É aqui que entra a simetria", "E a ordem do raciocínio", "Você não começa escolhendo", "Você começa olhando",
        "Cuidado: formato de esfera", "A pergunta certa", "Aqui, qualquer rotação", "deixa tudo igual",
        "Então não existe campo de lado", "Sobra um campo radial", "Andando à mesma distância", "Só agora escolhemos",
        "nela, campo e vetor área", "e o módulo é constante", "Agora, e só agora", "A superfície explora", "Ela não cria"],
    8: ["Bora usar isso", "Primeiro, o campo dentro dela", "Pela simetria, antes", "Então escolhemos uma gaussiana",
        "O lado do fluxo fica fácil", "Falta a carga envolvida", "Como a densidade é uniforme", "Mas vale ver o caminho",
        "Antes, atenção a três letras", "Um ponto lá dentro", "O segundo é o ângulo polar", "E o terceiro é o ângulo azimutal",
        "Variando cada um", "Na polar, o arco", "Na azimutal, o ponto gira", "Multiplicando os três",
        "Agora integramos a densidade", "As integrais dos ângulos", "Guarda essa", "Com densidade constante",
        "Na Lei de Gauss, o quatro pi", "e o raio ao cubo sobre", "Resultado: o campo cresce", "e no centro vale zero",
        "Agora leva a gaussiana", "Daqui pra frente", "a barra da carga envolvida", "A área continua crescendo",
        "então o campo passa a cair", "E repara: aí fora"],
    9: ["Agora junta tudo", "No centro, o campo começa", "Dentro, cresce em linha reta", "Atinge o máximo", "E fora, cai com",
        "Na superfície, as duas fórmulas", "o campo é contínuo, só", "E é contínuo porque", "Agora repara no que deixou",
        "Não foi a integral", "Foi saber, antes de integrar"],
    10: ["É daí que vêm", "Simetria esférica pede", "Uma linha infinita", "Um plano infinito", "Na linha e no plano",
         "Ou seja: não é receita", "É consequência da simetria"],
    11: ["E isso também explica", "A carga deslocada do começo", "Mas não existe superfície", "Gauss continua dando",
         "o que ela não dá sozinha", "Nesses casos, outro caminho", "Para uma carga pontual isolada", "Para a barra, soma",
         "Para o disco, no eixo", "Para uma distribuição irregular", "na mão ou no computador", "Então, diante de um problema",
         "Pergunta: qual é a simetria", "Ela define a direção", "Diz de que coordenadas", "Existe uma superfície em que",
         "E dá pra calcular", "Se as peças se encaixam", "Se não se encaixam"],
    12: ["Voltando aos dois casos", "Nos dois, a Lei de Gauss é igualmente", "Mas só no primeiro", "A Lei de Gauss fala sobre fluxo",
         "É a simetria da fonte que transforma", "Se esse vídeo te ajudou", "Compartilha com aquele amigo", "E se inscreve no Parallax"],
}
# Marcos extras (instantes absolutos) para animações que antes dependiam de deslocamentos fixos dentro da fala.
EXTRAS = {
    "v2": (5, "a volta inteira vale"), "v3": (5, "Todas as direções juntas"),
    "rowR": (8, "R maiúsculo é o raio"), "rowr": (8, "r é o raio da gaussiana"), "rowp": (8, "e r linha é a variável"),
}
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
    low = [NORM(p) for p in palavras]

    def acha(trecho, a, b, pos):
        alvo = [NORM(q) for q in trecho.split()]
        for j in range(max(a, pos), b - len(alvo) + 1):
            if low[j:j + len(alvo)] == alvo:
                return j
        raise SystemExit(f"Trecho não encontrado: {trecho!r}")

    blocos, extras = {}, {}
    for blk, trechos in ANCORAS.items():
        idx = [i for i, pi in enumerate(par) if BLOCO_DE[pi] == blk]
        a, b = idx[0], idx[-1] + 1
        pos, ts = a, []
        for t in trechos:
            j = acha(t, a, b, pos)
            ts.append(round(float(ini[j]), 3))
            pos = j + 1
        assert ts[0] == round(float(ini[a]), 3), f"bloco {blk}: a 1ª âncora deve abrir o bloco"
        assert all(x <= y for x, y in zip(ts, ts[1:])), f"bloco {blk}: âncoras fora de ordem"
        blocos[str(blk)] = {"cues": ts, "end": round(float(fim[b - 1]), 3)}
    for nome, (blk, trecho) in EXTRAS.items():
        idx = [i for i, pi in enumerate(par) if BLOCO_DE[pi] == blk]
        extras[nome] = round(float(ini[acha(trecho, idx[0], idx[-1] + 1, idx[0])]), 3)
    json.dump({"audio": FINAL.name, "dur": round(len(full) / sr0, 3), "blocks": blocos, "extras": extras,
               "words": [[p, round(float(x), 3), round(float(y), 3)] for p, x, y in zip(palavras, ini, fim)],
               "pauses": [[round(a, 3), round(b, 3)] for a, b in pausas_abs]},
              open(PASTA / "sync.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"narracao_final.wav: {len(full) / sr0:.2f} s; sync.json: {sum(len(v['cues']) for v in blocos.values())} âncoras")
    # diagnóstico: ritmo por frase
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
        q = re.sub(r"[Tt]éta", lambda m: m.group(0)[0] + "eta", p)
        if NORM(p) == "três" and i and NORM(palavras[i - 1]) == "física":
            q = p.replace("três", "3")
        out.append(q)
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
