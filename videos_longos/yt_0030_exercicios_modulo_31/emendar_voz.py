"""yt_0030 · voz v3.4, PASSO 2 de 2: cola os trechos novos (audio/v34/*.wav) no WAV contínuo da v3.3, só nas pausas entre parágrafos
(HANDOFF v4 §4.3). Nada de silêncio inserido: cada emenda corta no MEIO da pausa antiga, e o trecho novo entra com o próprio silêncio dele,
aparado para a mesma meia pausa (se o take tiver menos silêncio, a pausa fica menor; nunca maior). Cruzamento de 10 ms em cada emenda
(as duas pontas estão em silêncio). O nível do trecho novo é igualado ao do trecho antigo (RMS só dos quadros com fala).

entradas: audio/narracao_v33.wav · alinhamento_v33.json · narracao_v33.md (cópias da v3.3, §4.1) · trechos_v34/plano_trechos.json ·
          audio/v34/<trecho>.wav (ou <trecho>_takeN.wav, escolhido por --take T05=2)
saídas:   audio/narracao_v34.wav · audio/emenda_v34.json (onde cada emenda caiu, ganho, ritmo, pausas) · qa/emenda_v34.txt
uso:      uv run --no-sync python videos_longos/yt_0030_exercicios_modulo_31/emendar_voz.py [--take T05=2 ...]
saída 0 = tudo OK; 1 = algum critério falhou (ver qa/emenda_v34.txt, refazer só o trecho com FALHA)."""
import argparse
import json
import re
import sys
import wave
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
LIM_DB, KEEP, XF = -45.0, 0.020, 0.010          # limiar de fala (dBFS), sobra mínima antes/depois da fala (s), cruzamento (s)


def paragrafos(md):
    """Mesma regra do tempos.py: parágrafos depois de cada '### BLOCO ·', sem linhas de título."""
    out, bloco, cont = [], None, {}
    for par in re.split(r"\n\s*\n", md):
        par = par.strip()
        m = re.match(r"###\s+(\S+)\s+·", par)
        if m:
            bloco = m.group(1)
            par = par[m.end():].split("\n", 1)[1].strip() if "\n" in par else ""
            if not par:
                continue
        if bloco is None or not par or par.startswith("#") or par.startswith("*("):
            continue
        cont[bloco] = cont.get(bloco, 0) + 1
        out.append((f"{bloco}-{cont[bloco]}", par))
    return out


def le_wav(p):
    with wave.open(str(p)) as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2, p
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return sr, a


def fala_lim(a, sr, win=0.010):
    """Primeira e última amostra com fala (janela de 10 ms com RMS > LIM_DB)."""
    n = int(sr * win)
    k = len(a) // n
    r = 20 * np.log10(np.sqrt(np.mean(a[:k * n].reshape(k, n) ** 2, axis=1)) + 1e-9)
    on = np.where(r > LIM_DB)[0]
    return on[0] * n, (on[-1] + 1) * n


def rms_fala(a, sr, win=0.020):
    n = int(sr * win)
    k = len(a) // n
    r = np.sqrt(np.mean(a[:k * n].reshape(k, n) ** 2, axis=1))
    r = r[20 * np.log10(r + 1e-9) > -40]
    return float(np.sqrt(np.mean(r ** 2))) if len(r) else 1e-9


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--take", nargs="*", default=[], help="ex.: T05=2 (usa audio/v34/T05_..._take2.wav)")
    ap.add_argument("--velho", default="audio/narracao_v33.wav")
    ap.add_argument("--ali", default="alinhamento_v33.json")
    ap.add_argument("--md", default="narracao_v33.md")
    ap.add_argument("--saida", default="audio/narracao_v34.wav")
    a = ap.parse_args()
    takes = dict(t.split("=") for t in a.take)
    sr, velho = le_wav(U / a.velho)
    P = json.loads((U / a.ali).read_text(encoding="utf-8"))
    pars = paragrafos((U / a.md).read_text(encoding="utf-8"))
    toks = [(i, t) for i, w in enumerate(P) for t in re.findall(r"\w+", w["word"].lower())]
    lim, k = {}, 0                                   # âncora → (início da 1ª palavra, fim da última) no WAV velho
    for aid, par in pars:
        n = len(re.findall(r"\w+", re.sub(r"\[[^\]]*\]", " ", par).lower()))
        i0, i1 = toks[k][0], toks[k + n - 1][0]
        lim[aid] = (P[i0]["start"], P[i1]["end"])
        k += n
    assert k == len(toks), "o alinhamento v3.3 não bate com narracao_v33.md"
    ordem = [aid for aid, _ in pars]
    plano = json.loads((U / "trechos_v34" / "plano_trechos.json").read_text(encoding="utf-8"))
    pedacos, rel, falha, cursor = [], [], False, 0
    for p in plano:
        nome, run = p["trecho"], p["ancoras"]
        i0, i1 = ordem.index(run[0]), ordem.index(run[-1])
        assert ordem[i0 - 1] == p["antes"] and ordem[i1 + 1] == p["depois"], nome
        ini, fim = lim[run[0]][0], lim[run[-1]][1]
        ant, prox = lim[ordem[i0 - 1]][1], lim[ordem[i1 + 1]][0]
        ca, cb = (ant + ini) / 2, (fim + prox) / 2       # cortes no meio das pausas antigas
        tk = takes.get(nome.split("_")[0])
        arq = U / "audio" / "v34" / (nome + (f"_take{tk}" if tk else "") + ".wav")
        srn, novo = le_wav(arq)
        assert srn == sr, (arq, srn, sr)
        s0, s1 = fala_lim(novo, sr)
        meia_a, meia_b = int((ini - ca) * sr), int((cb - fim) * sr)
        a0 = max(0, s0 - max(meia_a, int(KEEP * sr)))
        b0 = min(len(novo), s1 + max(meia_b, int(KEEP * sr)))
        clip = novo[a0:b0].copy()
        g = rms_fala(velho[int(ini * sr):int(fim * sr)], sr) / rms_fala(clip, sr)
        g_db = 20 * np.log10(g)
        clip *= g
        pal = sum(len(re.sub(r"\[[^\]]*\]", " ", par).split()) for aid, par in pars if aid in run)
        pal_novo = len(re.sub(r"\[[^\]]*\]", " ", (U / "trechos_v34" / f"{nome}.md").read_text(encoding="utf-8").split("## Texto corrido (para gravação)")[1]).split())
        pps_v, pps_n = pal / (fim - ini), pal_novo / ((s1 - s0) / sr)
        pausa_a = (ini - ca) + (s0 - a0) / sr
        pausa_b = (cb - fim) + (b0 - s1) / sr
        pedacos.append(velho[cursor:int(ca * sr)])
        pedacos.append(clip)
        cursor = int(cb * sr)
        ok_g, ok_v = abs(g_db) <= 6.0, (abs(pps_n / pps_v - 1) <= 0.12 and 2.6 <= pps_n <= 3.25)
        ok_p = pausa_a >= 0.12 and pausa_b >= 0.12
        falha |= not (ok_g and ok_v and ok_p)
        rel.append({"trecho": nome, "arquivo": arq.name, "corte_a_v33": round(ca, 3), "corte_b_v33": round(cb, 3),
                    "dur_v33": round(fim - ini, 2), "dur_v34": round((s1 - s0) / sr, 2), "ganho_db": round(g_db, 2),
                    "pps_v33": round(pps_v, 3), "pps_v34": round(pps_n, 3), "pausa_antes": round(pausa_a, 3), "pausa_depois": round(pausa_b, 3),
                    "ok": bool(ok_g and ok_v and ok_p), "motivo": ("" if ok_g else "ganho > 6 dB; ") + ("" if ok_v else "ritmo fora; ") + ("" if ok_p else "pausa < 0,12 s")})
    pedacos.append(velho[cursor:])
    xf = int(XF * sr)                                 # cruzamento de 10 ms entre cada par de pedaços (silêncio com silêncio)
    out = pedacos[0]
    for nxt in pedacos[1:]:
        if len(out) > xf and len(nxt) > xf:
            ramp = np.linspace(0, 1, xf, dtype=np.float32)
            meio = out[-xf:] * np.cos(ramp * np.pi / 2) + nxt[:xf] * np.sin(ramp * np.pi / 2)
            out = np.concatenate([out[:-xf], meio, nxt[xf:]])
        else:
            out = np.concatenate([out, nxt])
    pico = float(np.abs(out).max())
    clip_n = int((np.abs(out) >= 0.999).sum())
    if clip_n:
        falha = True
    with wave.open(str(U / a.saida), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(np.clip(np.round(out * 32768), -32768, 32767).astype(np.int16).tobytes())   # mesma escala da leitura: o áudio velho volta bit a bit
    dur = len(out) / sr
    L = [f"yt_0030 · emenda da voz v3.4 ({a.saida}) · {len(plano)} trechos · {2 * len(plano)} emendas",
         f"duração {dur:.2f} s ({int(dur // 60)}:{dur % 60:05.2f}) · v3.3 {len(velho) / sr:.2f} s · +{dur - len(velho) / sr:.2f} s · "
         f"pico {20 * np.log10(pico + 1e-9):.2f} dBFS · clipping {clip_n}"]
    for r_ in rel:
        L.append(f"{'OK   ' if r_['ok'] else 'FALHA'} {r_['trecho']}: v3.3 {r_['dur_v33']} s → v3.4 {r_['dur_v34']} s · ganho {r_['ganho_db']:+.2f} dB · "
                 f"ritmo {r_['pps_v33']:.2f} → {r_['pps_v34']:.2f} p/s · pausas {r_['pausa_antes']:.2f} / {r_['pausa_depois']:.2f} s {r_['motivo']}")
    (U / "audio" / "emenda_v34.json").write_text(json.dumps({"sr": sr, "duracao": dur, "trechos": rel}, ensure_ascii=False, indent=1), encoding="utf-8")
    (U / "qa").mkdir(exist_ok=True)
    (U / "qa" / "emenda_v34.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    sys.exit(1 if falha else 0)


if __name__ == "__main__":
    main()
