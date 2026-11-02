"""yt_0019 v10: voz contínua SEM chiado. Mesma montagem do unir_voz.py (v9), com três mudanças pedidas no handoff v10:
 1. nenhuma cama de ruído rosa (o piso de -54 dBFS do v9 era a cama somada na montagem);
 2. a âncora EN1 ("se inscreve ... próximos vídeos") sai do meio: o bloco 5 é partido em duas peças (antes de EN1 | EN2), sem regerar nada;
 3. entram os blocos novos do fecho (bloco_06 = FIM-1, bloco_07 = FIM-2), com 1,2 s de silêncio antes do gancho e 0,75 s entre FIM-1 e FIM-2.
Depois da montagem: passa-altas de 70 Hz e expansor suave nas pausas (ganho -18 dB abaixo de -48 dBFS, com rampas e retenção, para não comer
cauda de palavra nem respiração). Tempos das âncoras que já existiam no v9 são copiados do voz9_tempos.json (a voz não se mexe); EN2 só ganha o deslocamento.
Saídas: audio/narracao_v10_cru.wav (sem limpeza), audio/narracao_v10.wav, audio/voz10_tempos.json, audio/audio10_medidas.json.
uso: python unir_voz10.py"""
import json
import wave
from pathlib import Path

import numpy as np

import unir_voz as U
from unir_voz import SR, XF, MANTER, LIM_DB, decodificar, envelope_db, vozeados, refinar

AQUI = Path(__file__).resolve().parent
V = AQUI / "audio" / "voz10"
OUT = AQUI / "audio"
JUNCAO = {"bloco_06": 1.2, "bloco_07": 0.75}
CORTAR = "EN1"                                                # âncora do bloco 5 que sai
LIM_PAUSA, GANHO_PAUSA_DB, RET_ANTES, RET_DEPOIS = -48.0, -18.0, 0.05, 0.18
NR_N, NR_HOP, NR_PISO_DB, NR_ALFA = 2048, 512, -18.0, 2.5        # redução espectral do chiado (perfil tirado das janelas mais quietas)


def pecas():
    out = []
    for f in sorted(V.glob("bloco_[0-9][0-9].json")):
        meta = json.loads(f.read_text(encoding="utf-8"))
        x = decodificar(f.with_suffix(".mp3"))
        a = meta["alinhamento"]
        S, E, car = np.array(a["character_start_times_seconds"]), np.array(a["character_end_times_seconds"]), "".join(a["characters"])
        assert car == meta["texto"]
        linhas, d, ancs = meta["texto"].split("\n"), 0, {}
        for aid, linha in zip(meta["ancoras"], linhas):
            ancs[aid] = [(linha[p:q + 1], float(S[d + p]), float(E[d + q])) for p, q in vozeados(linha)]
            d += len(linha) + 1
        env = envelope_db(x)
        voz = np.nonzero(env > LIM_DB)[0]
        t0, t1 = voz[0] * 0.010, (voz[-1] + 1) * 0.010
        ini, fim = max(0.0, t0 - MANTER), min(len(x) / SR, t1 + MANTER)
        nivel = float(20 * np.log10(np.sqrt(np.mean(10 ** (env[env > LIM_DB] / 10)))))
        ids = list(ancs)
        if CORTAR in ids:
            k = ids.index(CORTAR)
            ant, dep = ids[k - 1], ids[k + 1]
            fimA_p, iniB_p = ancs[ant][-1][2], ancs[dep][0][1]
            iniEN, fimEN = ancs[CORTAR][0][1], ancs[CORTAR][-1][2]
            fimA = min(fimA_p + min(MANTER, (iniEN - fimA_p) / 2), fim)
            iniB = max(ini, iniB_p - min(MANTER, (iniB_p - fimEN) / 2))
            out.append({"nome": f.stem + "a", "x": x, "ini": ini, "fim": fimA, "ancs": {i: ancs[i] for i in ids[:k]}, "nivel": nivel, "lead": t0 - ini, "cauda": fimA - fimA_p})
            out.append({"nome": f.stem + "b", "x": x, "ini": iniB, "fim": fim, "ancs": {i: ancs[i] for i in ids[k + 1:]}, "nivel": nivel, "lead": iniB_p - iniB, "cauda": fim - t1})
        else:
            out.append({"nome": f.stem, "x": x, "ini": ini, "fim": fim, "ancs": ancs, "nivel": nivel, "lead": t0 - ini, "cauda": fim - t1})
    return out


def reduzir_chiado(x):
    """Redução espectral (STFT, hann): perfil de ruído = média da potência dos 4% quadros mais quietos; ganho por bin max(piso, 1 - ALFA*N/|X|^2), suavizado
    no tempo e na frequência. Vale também por baixo da fala (o chiado do take é contínuo). Devolve float32 do mesmo tamanho."""
    n, hop = NR_N, NR_HOP
    w = np.hanning(n + 1)[:-1].astype(np.float32)
    pad = n
    xp = np.concatenate([np.zeros(pad, np.float32), x, np.zeros(pad + n, np.float32)])
    nq = (len(xp) - n) // hop + 1
    from numpy.lib.stride_tricks import sliding_window_view
    jan = sliding_window_view(xp, n)[::hop][:nq]
    en = np.empty(nq, np.float64)
    pot = np.zeros(n // 2 + 1, np.float64)
    C = 4000
    for a in range(0, nq, C):
        X = np.fft.rfft(jan[a:a + C] * w, axis=1)
        P = (np.abs(X) ** 2)
        en[a:a + C] = P.sum(axis=1)
    lim = np.percentile(en[en > 0], 4)
    sel = np.nonzero((en <= lim) & (en > 0))[0]
    for a in sel[:6000]:
        pot += np.abs(np.fft.rfft(jan[a] * w)) ** 2
    ruido = pot / min(len(sel), 6000)
    gmin = 10 ** (NR_PISO_DB / 20)
    y = np.zeros(len(xp) + n, np.float64)
    nor = np.zeros(len(xp) + n, np.float64)
    k = np.array([0.25, 0.5, 0.25])
    for a in range(0, nq, C):
        X = np.fft.rfft(jan[a:a + C] * w, axis=1)
        P = np.abs(X) ** 2
        G = np.maximum(gmin, 1.0 - NR_ALFA * ruido[None, :] / np.maximum(P, 1e-9))
        G = np.sqrt(G) if False else G
        G = np.apply_along_axis(lambda v: np.convolve(np.pad(v, 1, mode="edge"), k, mode="valid"), 1, G)
        G = np.apply_along_axis(lambda v: np.convolve(np.pad(v, 1, mode="edge"), k, mode="valid"), 0, G)
        Y = np.fft.irfft(X * G, n, axis=1) * w
        for j in range(Y.shape[0]):
            o = (a + j) * hop
            y[o:o + n] += Y[j]
            nor[o:o + n] += w * w
    y = y[pad:pad + len(x)] / np.maximum(nor[pad:pad + len(x)], 1e-6)
    return y.astype(np.float32)


def limpar(x):
    """Passa-altas 70 Hz (Butterworth 4ª ordem, em FFT) + expansor de pausas."""
    n = len(x)
    X = np.fft.rfft(x.astype(np.float64))
    f = np.fft.rfftfreq(n, 1 / SR)
    X *= 1.0 / np.sqrt(1.0 + (70.0 / np.maximum(f, 1e-3)) ** 8)
    y = reduzir_chiado(np.fft.irfft(X, n).astype(np.float32))
    db = envelope_db(y)
    jan = int(0.010 * SR)
    ant, dep = int(RET_ANTES / 0.010), int(RET_DEPOIS / 0.010)
    seg = np.zeros(len(db), bool)
    for i in np.nonzero(db > LIM_PAUSA)[0]:
        seg[max(0, i - ant): i + dep + 1] = True
    alvo = np.where(seg, 1.0, 10 ** (GANHO_PAUSA_DB / 20)).astype(np.float64)
    k = np.hanning(9)
    k /= k.sum()
    alvo = np.convolve(np.pad(alvo, 4, mode="edge"), k, mode="valid")
    ganho = np.repeat(alvo, jan)
    ganho = np.concatenate([ganho, np.full(n - len(ganho), alvo[-1])]) if len(ganho) < n else ganho[:n]
    return (y * ganho).astype(np.float32)


def main():
    P = pecas()
    ref = float(np.median([b["nivel"] for b in P]))
    xf = int(XF * SR)
    saida = np.zeros(0, np.float32)
    tempos, juncoes = {}, []
    for k, b in enumerate(P):
        g = float(np.clip(ref - b["nivel"], -3.0, 3.0))
        seg = b["x"][int(round(b["ini"] * SR)): int(round(b["fim"] * SR))] * 10 ** (g / 20)
        if k == 0:
            pos0 = 0
            saida = seg.copy()
        else:
            minimo = JUNCAO.get(b["nome"], U.JUNCAO_MIN)
            falta = max(0.0, minimo - (b["lead"] + P[k - 1]["cauda"]))
            if falta > 0:
                saida = np.concatenate([saida, np.zeros(int(round(falta * SR)), np.float32)])
            pos0 = len(saida) - xf
            r = np.linspace(0, 1, xf, dtype=np.float32)
            saida[-xf:] = saida[-xf:] * (1 - r) + seg[:xf] * r
            saida = np.concatenate([saida, seg[xf:]])
            juncoes.append({"t": round((pos0 + xf / 2) / SR, 3), "silencio_s": round(b["lead"] + P[k - 1]["cauda"] + falta, 3), "entre": [P[k - 1]["nome"], b["nome"]]})
        for aid, pal in b["ancs"].items():
            tempos[aid] = [{"w": w, "t": round(pos0 / SR + s - b["ini"], 4), "e": round(pos0 / SR + e - b["ini"], 4)} for w, s, e in pal]
    pico = float(np.abs(saida).max())
    if pico > 32000:
        saida *= 32000 / pico
    cru = np.clip(np.round(saida), -32768, 32767).astype(np.int16)
    limpo = limpar(saida)
    pico2 = float(np.abs(limpo).max())
    if pico2 > 0.89 * 32768:
        limpo *= 0.89 * 32768 / pico2
    pcm = np.clip(np.round(limpo), -32768, 32767).astype(np.int16)
    for nome, d in (("narracao_v10_cru.wav", cru), ("narracao_v10.wav", pcm)):
        with wave.open(str(OUT / nome), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(d.tobytes())
    v9 = json.loads((AQUI / "audio" / "voz9_tempos.json").read_text(encoding="utf-8"))["ancoras"]
    final = {}
    delta = tempos["EN2"][0]["t"] - v9["EN2"][0]["ta"]
    for aid, pal in tempos.items():
        if aid in v9:
            d_ = delta if aid == "EN2" else 0.0
            final[aid] = [{"w": q["w"], "t": round(q["t"] + d_, 4), "e": round(q["e"] + d_, 4)} for q in v9[aid]]
        else:
            final[aid] = pal
    plano = {"EN2": final["EN2"], "FIM-1": final["FIM-1"], "FIM-2": final["FIM-2"]}
    refinar(plano, pcm)
    db_c, db_l = envelope_db(cru.astype(np.float32)), envelope_db(pcm.astype(np.float32))
    voz_ = db_c > -48
    mc = ~(np.convolve(voz_.astype(float), np.ones(21), "same") > 0)           # pausa = janela de 10 ms a >= 0,1 s de qualquer fala
    mq = db_c < -50
    med = {"pausas_janelas_a_0,1s_da_fala": int(mc.sum()), "pausa_cru_dBFS_mediana": round(float(np.median(db_c[mc])), 1), "pausa_final_dBFS_mediana": round(float(np.median(db_l[mc])), 1),
           "pausa_final_dBFS_p95": round(float(np.percentile(db_l[mc], 95)), 1), "janelas_abaixo_de_-50_cru_mediana": round(float(np.median(db_c[mq])), 1),
           "janelas_abaixo_de_-50_final_mediana": round(float(np.median(db_l[mq])), 1), "pico_final_dBFS": round(float(20 * np.log10(np.abs(pcm).max() / 32768)), 2),
           "cama_v9": "ruído rosa a -54 dBFS RMS somado em toda a faixa (removido)"}
    (OUT / "audio10_medidas.json").write_text(json.dumps(med, indent=1), encoding="utf-8")
    (OUT / "voz10_tempos.json").write_text(json.dumps({"duracao": round(len(pcm) / SR, 3), "juncoes": juncoes, "ancoras": final}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"narracao_v10.wav {len(pcm) / SR:.2f} s;", med)
    for j in juncoes[-5:]:
        print(f"  junção {j['t']:.2f}: {j['entre']} silêncio {j['silencio_s']:.2f}")


if __name__ == "__main__":
    main()
