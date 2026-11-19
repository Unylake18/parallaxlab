"""yt_0024 · fase de voz: grava ancoras.json com os tempos REAIS da voz (audio/narracao_v1.wav).

Entrada: narracao_tags.md (texto da fala) e audio/asr_palavras_v1.json (faster-whisper small, só para os tempos; o texto de referência é o da narração,
não o reconhecido). As 43 âncoras começam nas frases-chave do HANDOFF FINAL §5 (não coincidem com os parágrafos). Alinha por difflib; palavras sem par
são interpoladas por sílabas entre as vizinhas casadas.
Saída: ancoras.json (palavras, ini, fim, dur, nominal, fala, t) com ini/fim contínuos (soma = duração do WAV), alinhamento_palavras.json.
Backup do nominal em ancoras_v12_nominal.json na primeira execução.
"""
import difflib
import json
import re
import wave
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
ANTES = 0.45
BKP = AQUI / "ancoras_v12_nominal.json"
if not BKP.exists():
    BKP.write_bytes((AQUI / "ancoras.json").read_bytes())
ordem = json.loads(BKP.read_text(encoding="utf-8"))["ordem"]

INICIOS = {
    "H1": "olha essa mesa de ar", "H2": "agora a pessoa puxa o fio", "H3": "só que repara numa coisa", "A1": "fala pessoal",
    "A2": "a gente vai ver que até um corpo", "B1-1": "vamos começar pelo que você já conhece", "B1-2": "então vem a pergunta natural",
    "B1-3": "como todo produto vetorial", "B1-4": "e o tamanho", "B1-5": "ou seja o momento angular é o momento linear vezes o braço",
    "B2-1": "agora um teste que pega muita gente", "B2-2": "depende do ponto", "B2-3": "já quem está parado ao lado do corredor",
    "B2-4": "e de um ponto do outro lado da reta", "B2-5": "e tem uma imagem bonita", "B2-6": "e isso não é coincidência",
    "B3-1": "então o que faz o momento angular mudar", "B3-2": "a derivada da posição é a velocidade", "B3-3": "sobra o vetor posição vezes a força",
    "B3-4": "vamos conferir com algo simples", "B3-5": "ganha o braço continua", "B4-1": "agora o caso que todo mundo associa",
    "B4-2": "a massa vezes o raio ao quadrado é o momento de inércia", "B4-3": "no movimento circular uniforme", "B4-4": "agora imagina um empurrão de lado",
    "B4-5": "guarda este detalhe", "B5-1": "agora a ideia mais poderosa", "B5-2": "daí saem duas consequências", "B5-3": "a segunda lembra que a área",
    "B5-4": "o newton tinha uma prova", "B5-5": "por isso um planeta anda mais rápido", "B6-1": "agora sim de volta à mesa",
    "B6-2": "só que agora o disco anda numa espiral", "B6-3": "mas espera torque zero", "B6-4": "com torque zero a primeira parcela",
    "B6-5": "e repara numa diferença", "B6-6": "e as áreas", "B6-7": "falta uma pergunta e a energia", "B6-8": "a energia cinética vai de",
    "B6-9": "e por isso fica cada vez mais difícil puxar", "S1": "a pergunta inicial está respondida", "S2": "e fica uma pergunta para você",
    "EN": "se essas conexões",
}
assert list(INICIOS) == ordem, "ordem das âncoras mudou"

tok = lambda s: re.findall(r"\w+", re.sub(r"\[[^\]]*\]", "", s).lower())
txt = (AQUI / "narracao_tags.md").read_text(encoding="utf-8").split("## Texto corrido (para gravação)")[1]
palavras = tok(txt)

# início de cada âncora (índice da 1ª palavra), em ordem
ini_idx, de = {}, 0
for aid in ordem:
    alvo = tok(INICIOS[aid])
    k = next((i for i in range(de, len(palavras)) if palavras[i:i + len(alvo)] == alvo), None)
    assert k is not None, f"início não achado: {aid}: {INICIOS[aid]!r}"
    ini_idx[aid] = k
    de = k + 1
inicios = [ini_idx[a] for a in ordem] + [len(palavras)]
assert inicios[0] == 0, "o texto precisa começar em H1"
dono = []
for n_, aid in enumerate(ordem):
    dono += [aid] * (inicios[n_ + 1] - inicios[n_])

with wave.open(str(AQUI / "audio" / "narracao_v1.wav")) as w:
    DUR = w.getnframes() / w.getframerate()

asr = json.loads((AQUI / "audio" / "asr_palavras_v1.json").read_text(encoding="utf-8"))
B, Bi = [], []
for a in asr:
    ps = re.findall(r"\w+", a["word"].lower())
    for k, q in enumerate(ps):
        d = (a["end"] - a["start"]) / len(ps)
        B.append(q)
        Bi.append((a["start"] + k * d, a["start"] + (k + 1) * d))


def silabas(p):
    return max(1, len(re.findall(r"[aeiouáéíóúâêôãõàü]+", p)))


ini_w = np.full(len(palavras), np.nan)
fim_w = np.full(len(palavras), np.nan)
casados = 0
for blk in difflib.SequenceMatcher(None, palavras, B, autojunk=False).get_matching_blocks():
    for k in range(blk.size):
        ini_w[blk.a + k], fim_w[blk.a + k] = Bi[blk.b + k]
        casados += 1
print(f"ASR: {len(B)} tokens; {casados}/{len(palavras)} palavras do texto casadas ({100 * casados / len(palavras):.1f}%)")
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
for k in range(len(palavras) - 1):
    ini_w[k + 1] = max(ini_w[k + 1], ini_w[k] + 0.01)
    fim_w[k] = min(max(fim_w[k], ini_w[k] + 0.01), ini_w[k + 1])

out, ini = {}, 0.0
idx = {aid: [k for k, d in enumerate(dono) if d == aid] for aid in ordem}
for n_, aid in enumerate(ordem):
    ks = idx[aid]
    if n_ + 1 < len(ordem):
        prox = idx[ordem[n_ + 1]][0]
        fim = max(fim_w[ks[-1]] + 0.02, ini_w[prox] - ANTES)
    else:
        fim = DUR
    n = len(ks)
    out[aid] = {"palavras": n, "ini": round(ini, 4), "fim": round(fim, 4), "dur": round(fim - ini, 4),
                "nominal": round(0.15 + n / 2.7 + 0.35, 2), "fala": " ".join(palavras[k] for k in ks),
                "t": [round(float(ini_w[k]) - ini, 3) for k in ks]}
    ini = fim
(AQUI / "ancoras.json").write_text(json.dumps({"origem": "voz real audio/narracao_v1.wav (ElevenLabs v4) + ASR", "ordem": ordem, "ancoras": out}, ensure_ascii=False, indent=1), encoding="utf-8")
(AQUI / "alinhamento_palavras.json").write_text(json.dumps(
    [dict(word=p, aid=d, start=round(float(a), 3), end=round(float(b), 3)) for p, d, a, b in zip(palavras, dono, ini_w, fim_w)],
    ensure_ascii=False), encoding="utf-8")
print(f"voz {DUR:.2f} s = {DUR / 60:.2f} min; soma das âncoras {ini:.2f} s; {len(palavras)} palavras; {len(palavras) / DUR:.2f} palavras/s")
ritmo = [(a, v["palavras"] / v["dur"]) for a, v in out.items()]
print("ritmo (palavras/s) min/med/max:", round(min(r for _, r in ritmo), 2), round(float(np.mean([r for _, r in ritmo])), 2), round(max(r for _, r in ritmo), 2))
for a, v in out.items():
    print(f"{a:6s} {v['ini']:8.2f} {v['fim']:8.2f} {v['dur']:6.2f}s {v['palavras']:3d}p  nominal {v['nominal']:5.2f}")
