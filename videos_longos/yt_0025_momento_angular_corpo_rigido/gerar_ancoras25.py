"""yt_0025 · grava ancoras.json com os tempos REAIS da voz (audio/narracao_v2.wav). Reproduzível: roda de novo depois de qualquer regeração da voz.

Entradas: narracao_limpa.md (texto da fala), audio/asr_palavras_v2.json (faster-whisper small, só para os tempos; o texto de referência é o da narração),
tabela INICIOS abaixo (handoff final §5: primeiras palavras de cada âncora) e o ancoras.json anterior (campos tela/original/hold são preservados).
Saída: ancoras.json (palavras, ini, fim, dur, nominal, fala, t) com ini/fim contínuos (sem silêncio inserido; a soma = duração do WAV) e
alinhamento_palavras.json (palavra, âncora, início, fim). Backup do nominal em ancoras_v2_nominal.json na primeira execução.
"""
import difflib
import json
import re
import unicodedata
import wave
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
ANTES = 0.45          # a âncora seguinte abre ANTES s antes da 1ª palavra (preparação da cena); a imagem sai ~LEAD s antes da palavra
WAV = AQUI / "audio" / "narracao_v2.wav"
ASR = AQUI / "audio" / "asr_palavras_v2.json"
INICIOS = [
    ("H1", "Olha esses dois halteres"), ("H2", "Agora repara nas bancadas"), ("H3", "Só que aqui o centro de massa"),
    ("A1", "Fala, pessoal!"), ("A2", "O caminho tem três paradas"), ("B1-0", "Vamos começar pelo mais simples"),
    ("B1-1", "Hipóteses: fio sem massa"), ("B1-2", "Pela regra da mão direita aplicada"), ("B1-3", "Vamos separar essa seta"),
    ("B1-4", "Agora deixa o pêndulo girar"), ("B1-5", "Quanto? Num intervalo pequeno"), ("B1-6", "E isso já rende física"),
    ("B1-7", "E um cuidado com as palavras"), ("B2-1", "Agora vamos sair da bolinha"), ("B2-2", "Pega um pedacinho só"),
    ("B2-3", "O momento angular se quebra"), ("B2-4", "Soma só as partes verticais"), ("B2-5", "Então, olhando só essa parte"),
    ("B2-6", "Mas essa igualdade fala"), ("B3-1", "Um haltere inclinado"), ("B3-2", "Cada massa descreve"),
    ("B3-3", "Agora a massa de baixo"), ("B3-4", "Leva os dois momentos angulares"), ("B3-5", "De lado, dá para ver tudo"),
    ("B3-6", "Ela vem de somar"), ("B3-7", "E, com o haltere girando"), ("B4-1", "Então, que distribuição"),
    ("B4-2", "Quando isso acontece"), ("B4-3", "E um detalhe importante"), ("B5-1", "Agora, de volta ao haltere inclinado"),
    ("B5-2", "Com uma volta por segundo, dá"), ("B5-3", "Quem faz esse torque?"), ("B5-4", "Dá para conferir só com forças"),
    ("B6-1", "Agora o exemplo"), ("B6-2", "Mas, girando, é exatamente"), ("B6-3", "A cem quilômetros por hora"),
    ("B6-4", "Esse binário passa"), ("B6-5", "É por isso que, na borracharia"), ("S1", "Então, vamos fechar"),
    ("S2", "E, antes de ir"), ("EN", "Se essas conexões"),
]


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def tok(s):
    return re.findall(r"\w+", sem_acento(re.sub(r"\[[^\]]*\]", "", s).lower()))


def main():
    texto = (AQUI / "narracao_limpa.md").read_text(encoding="utf-8").split("\n", 1)[1]
    palavras = tok(texto)
    # início de cada âncora = 1ª ocorrência da frase depois da âncora anterior (busca sequencial); "O momento angular se quebra" admite o texto "O momento angular se quebra junto"
    comeco, pos = {}, 0
    for aid, fr in INICIOS:
        alvo = tok(fr)
        k = next((i for i in range(pos, len(palavras) - len(alvo) + 1) if palavras[i:i + len(alvo)] == alvo), None)
        assert k is not None, f"início da âncora {aid} não encontrado: {fr!r} (a partir da palavra {pos})"
        comeco[aid] = k
        pos = k + 1
    ordem = [a for a, _ in INICIOS]
    assert comeco[ordem[0]] == 0, "a primeira âncora tem de começar na primeira palavra"
    fim_idx = {a: (comeco[ordem[n + 1]] if n + 1 < len(ordem) else len(palavras)) for n, a in enumerate(ordem)}
    dono = [None] * len(palavras)
    for a in ordem:
        for k in range(comeco[a], fim_idx[a]):
            dono[k] = a

    with wave.open(str(WAV)) as w:
        DUR = w.getnframes() / w.getframerate()
    asr = json.loads(ASR.read_text(encoding="utf-8"))
    B, Bi = [], []
    for a in asr:
        ps = tok(a["word"])
        for k, q in enumerate(ps):
            d = (a["end"] - a["start"]) / len(ps)
            B.append(q)
            Bi.append((a["start"] + k * d, a["start"] + (k + 1) * d))
    ini_w = np.full(len(palavras), np.nan)
    fim_w = np.full(len(palavras), np.nan)
    casados = 0
    for blk in difflib.SequenceMatcher(None, palavras, B, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            ini_w[blk.a + k], fim_w[blk.a + k] = Bi[blk.b + k]
            casados += 1
    print(f"ASR: {len(B)} tokens; {casados}/{len(palavras)} palavras do texto casadas ({100 * casados / len(palavras):.1f}%)")
    silabas = lambda p: max(1, len(re.findall(r"[aeiou]+", p)))
    peso = np.array([silabas(p) + 0.3 for p in palavras])
    i = 0
    while i < len(palavras):
        if np.isnan(ini_w[i]):
            j = i
            while j < len(palavras) and np.isnan(ini_w[j]):
                j += 1
            a_t = fim_w[i - 1] if i > 0 else 0.0
            b_t = ini_w[j] if j < len(palavras) else DUR
            seg = peso[i:j]
            e = a_t + np.concatenate([[0], np.cumsum(seg)]) / seg.sum() * max(0.05, b_t - a_t)
            ini_w[i:j], fim_w[i:j] = e[:-1], e[1:]
            i = j
        else:
            i += 1
    for k in range(len(palavras) - 1):                      # monotonia
        ini_w[k + 1] = max(ini_w[k + 1], ini_w[k] + 0.01)
        fim_w[k] = min(max(fim_w[k], ini_w[k] + 0.01), ini_w[k + 1])

    antigo = AQUI / "ancoras_v2_nominal.json"
    if not antigo.exists():
        antigo.write_bytes((AQUI / "ancoras.json").read_bytes())
    velho = json.loads(antigo.read_text(encoding="utf-8"))["ancoras"]
    out, ini = {}, 0.0
    for n_, aid in enumerate(ordem):
        ks = list(range(comeco[aid], fim_idx[aid]))
        if n_ + 1 < len(ordem):
            fim = max(fim_w[ks[-1]] + 0.02, ini_w[comeco[ordem[n_ + 1]]] - ANTES)
        else:
            fim = DUR
        n = len(ks)
        extra = {c: velho[aid][c] for c in ("tela", "hold") if aid in velho and c in velho[aid]}
        out[aid] = {"palavras": n, "ini": round(ini, 4), "fim": round(fim, 4), "dur": round(fim - ini, 4),
                    "nominal": round(0.15 + n / 2.7 + 0.35, 2), "fala": " ".join(palavras[k] for k in ks),
                    "t": [round(float(ini_w[k]) - ini, 3) for k in ks], **extra}
        ini = fim
    (AQUI / "ancoras.json").write_text(json.dumps({"origem": "voz real narracao_v2.wav (ElevenLabs v4) + ASR faster-whisper small; handoff final §5",
                                                  "ordem": ordem, "ancoras": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    (AQUI / "alinhamento_palavras.json").write_text(json.dumps(
        [dict(word=p, aid=d, start=round(float(a), 3), end=round(float(b), 3)) for p, d, a, b in zip(palavras, dono, ini_w, fim_w)],
        ensure_ascii=False), encoding="utf-8")
    print(f"voz {DUR:.2f} s = {DUR / 60:.2f} min; soma das âncoras {ini:.2f} s; {len(palavras)} palavras ({len(palavras) / DUR:.2f} p/s)")
    for a, v in out.items():
        print(f"{a:5s} {v['ini']:8.2f} {v['fim']:8.2f} {v['dur']:6.2f}s {v['palavras']:3d}p  ritmo {v['palavras'] / v['dur']:.2f}  1ªpal {v['t'][0]:.2f}s")


if __name__ == "__main__":
    main()
