"""yt_0018 v6: monta a narração sobre a linha do tempo REAL do preview e cola no vídeo (sem recomprimir o vídeo).

1. Cada âncora entra na hora em que a cena a abriu (`[ancora] ID t` do log de cada lote + o início do lote no preview). O clipe de voz
   (audio/voz/ancora_<ID>.wav) é cortado nas pausas protegidas (ancoras.json["pausas"]) e ganha o silêncio combinado.
2. Grava audio/narracao_v6.wav (mono, 16 bits, 44,1 kHz) e audio/voz_posicoes.json (início de cada âncora e de cada palavra, para o QA).
3. Copia os pacotes de vídeo de renders/preview_yt0018_v6mudo_960x540.mp4 e acrescenta o áudio em AAC 192 kb/s → renders/preview_yt0018_v6_960x540.mp4.
uso: python montar_audio.py [video_de_entrada]"""
import json
import re
import sys
import wave
from fractions import Fraction
from pathlib import Path

import av
import numpy as np

AQUI = Path(__file__).resolve().parent
SR = 44100
LOTES = ["PH", "PX0", "PX2", "PX3", "PX4", "PX5", "PEP"]
ANC = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]


def log(lote):
    return (AQUI / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")


def inicios_lotes():
    t, ini = 0.0, {}
    for l in LOTES:
        ini[l] = t
        t += int(re.search(r"\[tempo\] total [0-9.]+ s \((\d+) quadros\)", log(l)).group(1)) / 15
    return ini, t


def ler_wav(caminho):
    with wave.open(str(caminho), "rb") as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)


def clipe_com_pausas(aid):
    """Clipe da âncora com os silêncios protegidos; devolve o áudio e a duração."""
    x = ler_wav(AQUI / ANC[aid]["clip"])
    partes, a = [], 0
    for corte, seg in ANC[aid]["pausas"]:
        i = int(corte * SR)
        partes += [x[a:i], np.zeros(int(seg * SR), dtype=np.float32)]
        a = i
    partes.append(x[a:])
    y = np.concatenate(partes)
    n = int(0.012 * SR)                                         # 12 ms de entrada e saída: sem estalo
    y[:n] *= np.linspace(0, 1, n)
    y[-n:] *= np.linspace(1, 0, n)
    return y


def main():
    entrada = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "renders" / "preview_yt0018_v6mudo_960x540.mp4"
    saida_v = AQUI / "renders" / "preview_yt0018_v6_960x540.mp4"
    ini, total = inicios_lotes()
    mix = np.zeros(int((total + 2) * SR), dtype=np.float32)
    pos, fim_voz = {}, 0.0
    for l in LOTES:
        for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log(l)):
            aid, t0 = m.group(1), float(m.group(2))
            if aid == "FIM" or aid not in ANC:
                continue
            y = clipe_com_pausas(aid)
            a = int((ini[l] + t0) * SR)
            mix[a:a + len(y)] += y
            pos[aid] = {"lote": l, "inicio": round(ini[l] + t0, 3), "dur_cena": round(ANC[aid]["dur"], 3), "dur_voz": round(len(y) / SR, 3),
                        "palavras": [round(ini[l] + t0 + x, 3) for x in ANC[aid]["t"]]}
            fim_voz = max(fim_voz, (a + len(y)) / SR)
    faltam = [a for a in ANC if a not in pos]
    assert not faltam, f"âncoras sem posição: {faltam}"
    pico = float(np.abs(mix).max())
    mix = mix[: int(total * SR)]
    pcm = np.clip(mix, -32767, 32767).astype(np.int16)
    (AQUI / "audio").mkdir(exist_ok=True)
    with wave.open(str(AQUI / "audio" / "narracao_v6.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    (AQUI / "audio" / "voz_posicoes.json").write_text(json.dumps(pos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"narração: {len(pcm) / SR:.1f} s · pico {pico:.0f}/32767 · última fala termina em {fim_voz:.1f} s · vídeo {total:.1f} s")

    # cola o áudio no vídeo (os pacotes de vídeo passam sem recodificar)
    if not entrada.exists():
        sys.exit(f"sem {entrada}")
    ci, co = av.open(str(entrada)), av.open(str(saida_v), "w")
    vi = ci.streams.video[0]
    vo = co.add_stream_from_template(vi) if hasattr(co, "add_stream_from_template") else co.add_stream(template=vi)
    ao = co.add_stream("aac", rate=SR)
    ao.layout = "mono"
    ao.bit_rate = 192000
    for pkt in ci.demux(vi):
        if pkt.dts is None:
            continue
        pkt.stream = vo
        co.mux(pkt)
    passo = 1024
    for k in range(0, len(pcm), passo):
        bloco = pcm[k:k + passo]
        if len(bloco) < passo:
            bloco = np.pad(bloco, (0, passo - len(bloco)))
        fr = av.AudioFrame.from_ndarray(bloco.reshape(1, -1), format="s16", layout="mono")
        fr.sample_rate = SR
        fr.pts = k
        fr.time_base = Fraction(1, SR)
        for pkt in ao.encode(fr):
            co.mux(pkt)
    for pkt in ao.encode(None):
        co.mux(pkt)
    co.close()
    ci.close()
    print(f"{saida_v}: {saida_v.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
