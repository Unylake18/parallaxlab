"""yt_0018 v6: grava ancoras.json a partir da VOZ REAL (audio/voz_tempos.json, do cortar_voz.py).

Por âncora: `dur` = janela da cena (clipe de voz + pausas protegidas + folga até a próxima fala), `t` = instante de cada palavra desde o início da
janela (já deslocado pelas pausas), `fala` = as palavras (minúsculas), `pausas` = [[corte no clipe, segundos de silêncio]] e `ritmo` = fator dos plays
da cena (voz mais curta que a janela nominal do v5 → cena mais rápida; nunca > 1). A janela nominal (2,7 palavras/s) fica em ancoras_nominal.json.

Folga entre a última palavra de uma âncora e a primeira da seguinte: 0,75 s (1,2 s antes de uma troca de problema, do epílogo e do resumo).
uso: python gerar_ancoras.py"""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
nom = json.loads((AQUI / "ancoras_nominal.json").read_text(encoding="utf-8"))
ordem = nom["ordem"]
tempos = json.loads((AQUI / "audio" / "voz_tempos.json").read_text(encoding="utf-8"))

ALVO, ALVO_TROCA = 0.75, 1.2
TROCAS = {"A1", "X0-1", "X1-1", "X2-1", "X3-1", "X4-1", "X5-1", "EP1", "S2"}          # a folga ANTES destas é de 1,2 s
RITMO_MIN = 0.62
# Ritmo extra (multiplica o fator): âncoras em que a cena ainda chegava > 0,3 s depois da palavra-gatilho (medido com os dry runs)
RITMO_EXTRA = {}
# Pausas protegidas dentro da âncora (handoff v6 §3): depois destas palavras entra silêncio, para a tela mostrar o que a fala não pode cobrir.
PAUSAS_VOZ = {
    "H2": [("em câmera lenta", 2.0)],               # o salto em câmera lenta e a folha escorregando para trás, sem fala por cima
    "X3-6": [("dá duas faixas", 1.5)],              # as duas faixas aparecendo no círculo
    "X3-7": [("ponta oposta da folha", 1.2)],       # os dois saltos-limite pousando na ponta oposta
    "X5-2": [("marcar cinco quilos", 1.2)],         # o mostrador cai de 6,0 para 5,0 antes do "Por quê?"
    "X5-6": [("como cinco quilos", 1.0)],           # o 5,0 desce até o mostrador
    "EP2": [("o que foi para a direita", 1.2)],     # silêncio antes de "Einstein"
}


def toks(s):
    return re.findall(r"\w+", s.lower())


out, janelas = {}, {}
for k, aid in enumerate(ordem):
    v = tempos[aid]
    pal = v["palavras"]
    ws = [toks(p["w"])[0] if toks(p["w"]) else p["w"].lower() for p in pal]
    t = [p["t"] for p in pal]
    e = [p["e"] for p in pal]
    pausas, extra_total = [], 0.0
    for frase, seg in PAUSAS_VOZ.get(aid, []):
        alvo = toks(frase)
        i = next((i for i in range(len(ws)) if ws[i:i + len(alvo)] == alvo), None)
        assert i is not None and i + len(alvo) < len(ws), (aid, frase)
        j = i + len(alvo) - 1                                                # última palavra da frase
        corte = (e[j] + t[j + 1]) / 2
        pausas.append([round(corte, 3), seg])
        t = [x + seg if x > corte else x for x in t]
        extra_total += seg
    cauda = v["dur_clip"] - v["fim"]
    prox = ordem[k + 1] if k + 1 < len(ordem) else None
    head_prox = tempos[prox]["ini"] if prox else 0.0
    alvo_gap = ALVO_TROCA if prox in TROCAS else ALVO
    folga = max(0.05, alvo_gap - cauda - head_prox) if prox else 0.8
    dur = v["dur_clip"] + extra_total + folga
    nominal = nom["ancoras"][aid]["dur"]
    ritmo = round(min(1.0, max(RITMO_MIN, dur / nominal * RITMO_EXTRA.get(aid, 1.0))), 3)
    out[aid] = {"palavras": len(pal), "dur": round(dur, 3), "fala": " ".join(ws), "t": [round(x, 3) for x in t], "pausas": pausas,
                "folga": round(folga, 3), "clip": f"audio/voz/ancora_{aid}.wav", "ritmo": ritmo, "nominal": nominal}
(AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "ancoras": out}, ensure_ascii=False, indent=1), encoding="utf-8")
tot = sum(v["dur"] for v in out.values())
print(f"{len(out)} âncoras; {tot / 60:.2f} min (nominal v5: {sum(v['nominal'] for v in out.values()) / 60:.2f} min)")
for aid in ordem:
    v = out[aid]
    print(f"{aid:6s} janela {v['dur']:6.2f} s (nominal {v['nominal']:6.2f}) ritmo {v['ritmo']:.2f}" + (f"  pausas {v['pausas']}" if v["pausas"] else ""))
