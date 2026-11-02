"""yt_0019 v9: junta os blocos de voz (audio/voz9/bloco_NN.*) em UM WAV contínuo, audio/narracao_v9.wav (mono, 44,1 kHz, 16 bits), sem cortar por âncora
e sem inserir silêncio: só apara o silêncio das pontas de cada bloco (< -45 dBFS), deixa 0,30 s do silêncio natural do próprio take de cada lado e
faz crossfade de 25 ms. Grava audio/voz9_tempos.json: início/fim de cada palavra de cada âncora NA LINHA DO TEMPO DO WAV FINAL (alinhamento por caractere
do /with-timestamps, somado ao deslocamento do bloco) e as junções.
uso: python unir_voz.py"""
import json
import re
import wave
from pathlib import Path

import av
import numpy as np

AQUI = Path(__file__).resolve().parent
V = AQUI / "audio" / "voz9"
SR = 44100
LIM_DB, MANTER, XF = -45.0, 0.30, 0.025
JUNCAO_MIN = 0.34                      # silêncio total (natural + cama) numa junção de blocos: o mesmo das maiores pausas de parágrafo do próprio take
CAMA_DB = -54.0                        # cama de sala (ruído rosa) sob a voz inteira: o piso do take (mediana -60 dBFS), sem trechos < -80 dBFS
JAN = int(0.010 * SR)


def decodificar(caminho):
    saida = []
    with av.open(str(caminho)) as c:
        rs = av.AudioResampler(format="s16", layout="mono", rate=SR)
        for fr in c.decode(audio=0):
            for r in rs.resample(fr):
                saida.append(np.frombuffer(bytes(r.planes[0])[: r.samples * 2], dtype=np.int16))
        for r in rs.resample(None):
            saida.append(np.frombuffer(bytes(r.planes[0])[: r.samples * 2], dtype=np.int16))
    return np.concatenate(saida).astype(np.float32)


def envelope_db(x):
    n = len(x) // JAN
    e = np.sqrt((x[: n * JAN].reshape(n, JAN) ** 2).mean(axis=1) + 1e-9)
    return 20 * np.log10(e / 32768.0)


def vozeados(texto):
    """Palavras fora de [tags]: (índice do primeiro, do último caractere)."""
    prof, palavras, atual = 0, [], None
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
        if re.match(r"\w", ch):
            if atual is None:
                atual = [i, i]
                palavras.append(atual)
            else:
                atual[1] = i
        else:
            atual = None
    return palavras


def cama(n):
    """Ruído rosa (1/f) estacionário a CAMA_DB dBFS RMS: a sala não some entre as frases."""
    rng = np.random.default_rng(18)
    X = np.fft.rfft(rng.standard_normal(n))
    f = np.arange(len(X), dtype=np.float64)
    f[0] = 1.0
    X = X / np.sqrt(f)
    X[0] = 0.0
    r = np.fft.irfft(X, n)
    r *= 32768.0 * 10 ** (CAMA_DB / 20) / np.sqrt((r ** 2).mean())
    return r.astype(np.float32)


def refinar(tempos, pcm):
    """O alinhamento por caractere chega em média ~0,1 s depois da fala real (medido na onda). Para a palavra depois de uma pausa (>= 0,20 s) usa o
    instante em que o envelope sobe de verdade; as demais ficam com o alinhamento (`ta` guarda o original). Devolve quantas foram corrigidas."""
    db = envelope_db(pcm.astype(np.float32))
    n, corrigidas = len(db), 0
    plano = [(aid, p) for aid, ps in tempos.items() for p in ps]
    for k in range(1, len(plano)):
        aid, p = plano[k]
        p["ta"] = p["t"]
        ant = plano[k - 1][1]
        if p["t"] - ant["e"] < 0.20:
            continue
        i, i0 = int(round(p["t"] / 0.01)), int(round(ant["e"] / 0.01))
        lo, hi = max(1, i0 + 2), min(n - 1, i + 30)
        if hi <= lo + 2:
            continue
        piso = np.percentile(db[lo:max(lo + 1, i - 5)], 20)
        lim = max(-42.0, piso + 12.0)
        for j in range(lo, hi):
            if db[j] >= lim and db[j - 1] < lim:
                novo = j * 0.01
                if -0.40 <= novo - p["t"] <= 0.10:
                    p["t"] = round(novo, 4)
                    corrigidas += 1
                break
    plano[0][1]["ta"] = plano[0][1]["t"]
    return corrigidas


def main():
    blocos = []
    for f in sorted(V.glob("bloco_[0-9][0-9].json")):
        meta = json.loads(f.read_text(encoding="utf-8"))
        x = decodificar(f.with_suffix(".mp3"))
        a = meta["alinhamento"]
        S, E, car = np.array(a["character_start_times_seconds"]), np.array(a["character_end_times_seconds"]), "".join(a["characters"])
        assert car == meta["texto"], f"{f.name}: o alinhamento não bate com o texto enviado"
        env = envelope_db(x)
        voz = np.nonzero(env > LIM_DB)[0]
        t0, t1 = voz[0] * 0.010, (voz[-1] + 1) * 0.010                      # primeira e última janela com fala
        ini = max(0.0, t0 - MANTER)
        fim = min(len(x) / SR, t1 + MANTER)
        linhas, d, ancs = meta["texto"].split("\n"), 0, {}
        for aid, linha in zip(meta["ancoras"], linhas):
            ancs[aid] = [(linha[p:q + 1], float(S[d + p]), float(E[d + q])) for p, q in vozeados(linha)]
            d += len(linha) + 1
        # nível da fala (RMS das janelas acima do limiar) para casar os blocos
        nivel = 20 * np.log10(np.sqrt(np.mean(10 ** (env[env > LIM_DB] / 10))))
        blocos.append({"nome": f.stem, "x": x, "ini": ini, "fim": fim, "ancs": ancs, "nivel": float(nivel), "lead": t0 - ini, "cauda": fim - t1})
    ref = float(np.median([b["nivel"] for b in blocos]))
    print("bloco   duração  fala(dBFS)  ganho   silêncio ini/fim mantido")
    for b in blocos:
        g = float(np.clip(ref - b["nivel"], -3.0, 3.0))
        b["ganho"] = 10 ** (g / 20)
        print(f"{b['nome']}  {len(b['x']) / SR:7.1f}s  {b['nivel']:7.2f}   {g:+.2f} dB   {b['lead']:.2f} / {b['cauda']:.2f} s")
    xf = int(XF * SR)
    saida = np.zeros(0, np.float32)
    tempos, juncoes = {}, []
    for k, b in enumerate(blocos):
        seg = b["x"][int(round(b["ini"] * SR)): int(round(b["fim"] * SR))] * b["ganho"]
        if k == 0:
            pos0 = 0
            saida = seg.copy()
        else:
            falta = max(0.0, JUNCAO_MIN - (b["lead"] + blocos[k - 1]["cauda"]))
            if falta > 0:                                                   # o take acabou colado na fala: completa a junção com a cama de sala (abaixo)
                saida = np.concatenate([saida, np.zeros(int(round(falta * SR)), np.float32)])
            pos0 = len(saida) - xf
            r = np.linspace(0, 1, xf, dtype=np.float32)
            saida[-xf:] = saida[-xf:] * (1 - r) + seg[:xf] * r
            saida = np.concatenate([saida, seg[xf:]])
            juncoes.append({"t": round((pos0 + xf / 2) / SR, 3), "xfade_ms": XF * 1000, "silencio_s": round(b["lead"] + blocos[k - 1]["cauda"] + falta, 3),
                            "entre": [blocos[k - 1]["nome"], b["nome"]]})
        for aid, pal in b["ancs"].items():
            tempos[aid] = [{"w": w, "t": round(pos0 / SR + s - b["ini"], 4), "e": round(pos0 / SR + e - b["ini"], 4)} for w, s, e in pal]
    saida = saida + cama(len(saida))
    pico = float(np.abs(saida).max())
    if pico > 32000:
        saida *= 32000 / pico
    pcm = np.clip(np.round(saida), -32768, 32767).astype(np.int16)
    with wave.open(str(AQUI / "audio" / "narracao_v9.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    corr = refinar(tempos, pcm)
    print(f"{corr} inícios de palavra (depois de pausa) corrigidos pela onda")
    palavras = sum(len(v) for v in tempos.values())
    fala_ini = min(v[0]["t"] for v in tempos.values())
    fala_fim = max(v[-1]["e"] for v in tempos.values())
    (AQUI / "audio" / "voz9_tempos.json").write_text(json.dumps({"duracao": round(len(pcm) / SR, 3), "juncoes": juncoes, "ancoras": tempos}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"narracao_v9.wav: {len(pcm) / SR:.2f} s ({len(pcm) / SR / 60:.2f} min); fala de {fala_ini:.2f} a {fala_fim:.2f} s; {palavras} palavras ({palavras / (fala_fim - fala_ini):.2f} p/s); pico {pico:.0f}")
    for j in juncoes:
        print(f"  junção em {j['t']:.2f} s: {j['entre'][0]} → {j['entre'][1]}, silêncio natural {j['silencio_s']:.2f} s, crossfade {j['xfade_ms']:.0f} ms")


if __name__ == "__main__":
    main()
