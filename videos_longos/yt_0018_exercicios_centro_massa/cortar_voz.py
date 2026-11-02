"""yt_0018 v6: corta os blocos de voz (audio/voz/bloco_NN.*) e os takes (audio/voz/take_<ID>_N.*) em um WAV por âncora e grava os tempos
de cada palavra (do alinhamento por caractere do ElevenLabs, sem ASR) → audio/voz/ancora_<ID>.wav e audio/voz_tempos.json.

Um take de âncora vale mais que o bloco (o último take vence). O corte fica no meio do silêncio entre uma âncora e a vizinha.
uso: python cortar_voz.py"""
import io
import json
import re
import wave
from pathlib import Path

import av
import numpy as np

AQUI = Path(__file__).resolve().parent
V = AQUI / "audio" / "voz"
SR = 44100


def decodificar(caminho):
    saida = []
    with av.open(str(caminho)) as c:
        rs = av.AudioResampler(format="s16", layout="mono", rate=SR)
        for fr in c.decode(audio=0):
            for r in rs.resample(fr):
                saida.append(np.frombuffer(bytes(r.planes[0])[: r.samples * 2], dtype=np.int16))
        for r in rs.resample(None):
            saida.append(np.frombuffer(bytes(r.planes[0])[: r.samples * 2], dtype=np.int16))
    return np.concatenate(saida)


def vozeados(texto):
    """Índices dos caracteres falados (fora de [tags] e de espaços) e as palavras (\\w+) com o índice do primeiro e do último caractere."""
    prof, ids, palavras, atual = 0, [], [], None
    for i, ch in enumerate(texto):
        if ch == "[":
            prof += 1
            atual = None
            continue
        if ch == "]":
            prof = max(0, prof - 1)
            continue
        if prof or ch.isspace():
            atual = None
            continue
        ids.append(i)
        if re.match(r"\w", ch):
            if atual is None:
                atual = [i, i]
                palavras.append(atual)
            else:
                atual[1] = i
        else:
            atual = None
    return ids, palavras


def fonte(meta):
    a = meta["alinhamento"]
    return np.array(a["character_start_times_seconds"]), np.array(a["character_end_times_seconds"]), "".join(a["characters"])


def cortar_bloco(meta, pcm, saida, linhas):
    S, E, car = fonte(meta)
    assert car == meta["texto"], "o alinhamento não bate com o texto enviado"
    desloc, itens = 0, []
    for aid, linha in zip(meta["ancoras"], linhas):
        ids, pal = vozeados(linha)
        itens.append((aid, desloc, ids, pal, linha))
        desloc += len(linha) + 1
    for k, (aid, d, ids, pal, linha) in enumerate(itens):
        s0, e1 = S[d + ids[0]], E[d + ids[-1]]
        ant = E[itens[k - 1][1] + itens[k - 1][2][-1]] if k else None
        prox = S[itens[k + 1][1] + itens[k + 1][2][0]] if k + 1 < len(itens) else None
        cin = max(0.0, s0 - 0.25) if ant is None else max(s0 - 0.25, (ant + s0) / 2)
        cout = e1 + 0.35 if prox is None else min(e1 + 0.35, (e1 + prox) / 2)
        saida[aid] = (pcm, cin, cout, s0, e1, [(linha[a:b + 1], S[d + a], E[d + b]) for a, b in pal])


def main():
    texto = (AQUI / "narracao_tags_v1_3.md").read_text(encoding="utf-8")
    corpo = texto[texto.index("## Texto corrido (para gravação)"):].split("\n", 1)[1]
    linhas = [l.strip() for l in corpo.splitlines() if l.strip()]
    ordem = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))["ordem"]
    por_aid = dict(zip(ordem, linhas))
    fontes = {}
    for f in sorted(V.glob("bloco_*.json")):
        meta = json.loads(f.read_text(encoding="utf-8"))
        pcm = decodificar(f.with_suffix(".mp3"))
        cortar_bloco(meta, pcm, fontes, meta["texto"].split("\n"))
    velhas = {}
    for f in sorted(V.glob("take_*.json"), key=lambda p: int(p.stem.rsplit("_", 1)[1])):      # o último take de cada âncora vence
        meta = json.loads(f.read_text(encoding="utf-8"))
        tmp = {}
        cortar_bloco(meta, decodificar(f.with_suffix(".mp3")), tmp, [meta["texto"]])
        velhas.update(tmp)
    fontes.update(velhas)
    tempos = {}
    for aid in ordem:
        pcm, cin, cout, s0, e1, pal = fontes[aid]
        clip = pcm[int(cin * SR): int(cout * SR)]
        with wave.open(str(V / f"ancora_{aid}.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(clip.tobytes())
        tempos[aid] = {"dur_clip": round(len(clip) / SR, 3), "ini": round(s0 - cin, 3), "fim": round(e1 - cin, 3),
                       "palavras": [{"w": w_, "t": round(a - cin, 3), "e": round(b - cin, 3)} for w_, a, b in pal]}
    (AQUI / "audio" / "voz_tempos.json").write_text(json.dumps(tempos, ensure_ascii=False, indent=1), encoding="utf-8")
    fala = sum(v["fim"] - v["ini"] for v in tempos.values())
    pal = sum(len(v["palavras"]) for v in tempos.values())
    print(f"{len(tempos)} âncoras; voz {fala / 60:.2f} min; {pal} palavras; {pal / fala:.2f} palavras/s")
    for aid in ordem:
        v = tempos[aid]
        print(f"{aid:6s} fala {v['fim'] - v['ini']:6.2f} s  {len(v['palavras']):3d} pal  {len(v['palavras']) / (v['fim'] - v['ini']):.2f} p/s")


if __name__ == "__main__":
    main()
