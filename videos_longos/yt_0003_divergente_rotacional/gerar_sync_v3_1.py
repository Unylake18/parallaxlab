"""yt_0003 — alinha a narração V3.1 aos 5 WAV do ElevenLabs (sem ASR, mesmo método do yt_0002) e gera:
  audio/narracao_final.wav   as 5 partes intactas, com pausa GAP entre elas
  sync_v3_1.json             início/fim de cada um dos 92 blocos (âncoras), palavras, pausas
  duracoes_v3_1.json         duração de cada bloco para a cena (voz real; pads de animação em pads_v3_1.json)

  uv run --no-sync python gerar_sync_v3_1.py alinhar     → sync_v3_1.json + narracao_final.wav + relatório de sanidade
  uv run --no-sync python gerar_sync_v3_1.py montar      → duracoes_v3_1.json (com pads) + audio/narracao_montagem.wav
"""
import importlib.util
import json
import re
import sys
import wave
from pathlib import Path

import numpy as np

PASTA = Path(__file__).resolve().parent
AUD = PASTA / "audio"
PARTES = sorted((AUD / "partes").glob("narracao_parte*.wav"))
FINAL = AUD / "narracao_final.wav"
MONTAGEM = AUD / "narracao_montagem.wav"
GAP = 0.9            # pausa entre as partes
LEAD = 0.3           # o evento visual entra LEAD s depois do início da fala do bloco
CAUDA = 1.5          # s de cena depois da última palavra

_spec = importlib.util.spec_from_file_location("sync2", PASTA.parent / "yt_0002_lei_gauss_casos_classicos" / "gerar_sync.py")
S2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S2)          # reaproveita pausas/alinhar_parte/silabas (só lê arquivos do yt_0002)


def blocos():
    md = (PASTA / "narracao_v3_1.md").read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r"### (\w+) — ([^\n]*)\n\*\*Evento visual[^:]*:\*\* ([^\n]*)\n\n> ([^\n]*)", md):
        out.append((m.group(1), " ".join(re.sub(r"\*\*|\\\(|\\\)", "", m.group(4)).split())))
    return out


def partes_de_texto(bl):
    """Reconstrói os 5 blocos TTS exatamente como em roteiro_tts_v3_1/ (mesmo empacotamento)."""
    gr, cur, n = [], [], 0
    for i, tx in bl:
        add = len(tx) + (1 if cur else 0)
        if cur and n + add > 5000:
            gr.append(cur); cur = []; n = 0; add = len(tx)
        cur.append((i, tx)); n += add
    gr.append(cur)
    return gr


def alinhar():
    bl = blocos()
    gr = partes_de_texto(bl)
    assert len(gr) == len(PARTES), (len(gr), len(PARTES))
    for k, g in enumerate(gr, 1):
        arq = (PASTA / "roteiro_tts_v3_1" / f"bloco_{k:02d}.txt").read_text(encoding="utf-8").strip()
        assert " ".join(t for _, t in g) == arq, f"roteiro_tts_v3_1/bloco_{k:02d}.txt difere da narração V3.1"
    palavras, ini, fim, bloco_de, pausas_abs, audio = [], [], [], [], [], []
    off, sr0 = 0.0, None
    for k, (path, g) in enumerate(zip(PARTES, gr)):
        raw, sr = S2.ler(path)
        sr0 = sr0 or sr
        assert sr == sr0
        pals = [(w, i) for i, t in g for w in t.split()]
        print(f"parte {k + 1}: {len(raw) / sr:.2f} s, {len(pals)} palavras, {len(g)} blocos")
        a, b, runs = S2.alinhar_parte(raw, sr, [w for w, _ in pals])
        palavras += [w for w, _ in pals]
        bloco_de += [i for _, i in pals]
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
    ini, fim = np.array(ini), np.array(fim)
    ids = [i for i, _ in bl]
    info = []
    for i in ids:
        idx = [j for j, b in enumerate(bloco_de) if b == i]
        info.append({"id": i, "w0": idx[0], "w1": idx[-1], "ini": round(float(ini[idx[0]]), 3), "fim": round(float(fim[idx[-1]]), 3),
                     "palavras": len(idx), "sil": sum(S2.silabas(palavras[j]) for j in idx)})
    for a, b in zip(info, info[1:]):
        a["evento"] = round(a["ini"] + LEAD, 3)
        a["t_fim"] = round(b["ini"] + LEAD, 3)
    info[-1]["evento"] = round(info[-1]["ini"] + LEAD, 3)
    info[-1]["t_fim"] = round(info[-1]["fim"] + CAUDA, 3)
    json.dump({"dur_audio": round(len(full) / sr0, 3), "blocos": info,
               "words": [[p, round(float(x), 3), round(float(y), 3)] for p, x, y in zip(palavras, ini, fim)],
               "pauses": [[round(a, 3), round(b, 3)] for a, b in pausas_abs]},
              open(PASTA / "sync_v3_1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"audio {len(full) / sr0:.2f} s; {len(info)} blocos")
    # sanidade: ritmo por frase (sílabas/s) — outlier = texto não falado / palavra pulada / alinhamento ruim
    taxas = []
    i0 = 0
    for j, p in enumerate(palavras):
        if p[-1] in ".?!":
            sil = sum(S2.silabas(q) for q in palavras[i0:j + 1])
            taxas.append((sil / (fim[j] - ini[i0]), i0, j))
            i0 = j + 1
    med = float(np.median([t[0] for t in taxas]))
    ruins = [(t, i0_, j_) for t, i0_, j_ in taxas if abs(t - med) / med > .3]
    print(f"ritmo mediano {med:.2f} síl/s; frases {len(taxas)}; fora de ±30%: {len(ruins)}")
    for t, a, b in ruins[:15]:
        print(f"  {t:4.1f} síl/s  {ini[a]:7.1f}–{fim[b]:7.1f}  {' '.join(palavras[a:a + 9])}")
    # cada início de bloco deve vir logo após uma pausa
    pa = np.array(pausas_abs)
    sem_pausa = []
    for b in info[1:]:
        antes = ((pa[:, 1] <= b["ini"] + .05) & (pa[:, 1] >= b["ini"] - .6)).any()
        if not antes:
            sem_pausa.append(b["id"])
    print(f"blocos cujo início NÃO coincide com uma pausa detectada: {sem_pausa}")


def montar():
    sync = json.loads((PASTA / "sync_v3_1.json").read_text(encoding="utf-8"))
    pads_f = PASTA / "pads_v3_1.json"
    pads = json.loads(pads_f.read_text(encoding="utf-8")) if pads_f.exists() else {}
    bl = sync["blocos"]
    dur, acc = {}, 0.0
    prox_ini = {a["id"]: b["ini"] for a, b in zip(bl, bl[1:])}
    for b in bl:
        dur[b["id"]] = {"palavras": b["palavras"], "t": round(b["evento"] + acc, 3), "s": round(b["t_fim"] - b["evento"] + pads.get(b["id"], 0.0), 3),
                        "voz_s": round(b["t_fim"] - b["evento"], 3), "pad_s": round(pads.get(b["id"], 0.0), 3),
                        "gap": round(max(prox_ini.get(b["id"], b["fim"] + 1.0) - b["fim"], 0.0), 3)}
        acc += pads.get(b["id"], 0.0)
    aj_f = PASTA / "ajustes_asr_v3_1.json"
    if aj_f.exists():
        aj = {k: v for k, v in json.loads(aj_f.read_text(encoding="utf-8")).items() if not k.startswith("_")}
        ids = [b["id"] for b in bl]
        for i, t_novo in aj.items():
            k = ids.index(i)
            fim = dur[i]["t"] + dur[i]["s"]
            dur[i]["t"], dur[i]["s"] = round(t_novo, 3), round(fim - t_novo, 3)
            ant = dur[ids[k - 1]]
            ant["s"] = round(t_novo - ant["t"], 3)
    (PASTA / "duracoes_v3_1.json").write_text(json.dumps(dur, ensure_ascii=False, indent=1), encoding="utf-8")
    # áudio de montagem: pausa extra no fim do bloco (a fala não é alterada)
    raw, sr = S2.ler(FINAL)
    cortes = [(0.0, None)]
    saida, ult = [], 0
    for b in bl:
        p = pads.get(b["id"], 0.0)
        if p <= 0:
            continue
        t = b["t_fim"] - LEAD - 0.1          # fim do bloco, antes do início da fala seguinte
        n = int(round(t * sr))
        saida.append(raw[ult:n])
        saida.append(np.zeros((int(round(p * sr)), raw.shape[1]), dtype=np.int16))
        ult = n
    saida.append(raw[ult:])
    full = np.concatenate(saida)
    with wave.open(str(MONTAGEM), "wb") as w:
        w.setnchannels(full.shape[1]); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(full.tobytes())
    print(f"duracoes_v3_1.json ({len(dur)} blocos, {sum(1 for v in pads.values() if v > 0)} com pad); montagem {len(full) / sr:.2f} s")


if __name__ == "__main__":
    {"alinhar": alinhar, "montar": montar}[sys.argv[1]]()
