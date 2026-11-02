"""yt_0018 v7: cola a narração CONTÍNUA (audio/narracao_v7.wav, do unir_voz.py) no preview mudo, sem recodificar o vídeo.

A voz é a régua: o WAV começa junto com o vídeo e nada é cortado nem deslocado por âncora. Depois do fim da voz o áudio continua com a cama de sala
até o fim do vídeo (fade de 0,5 s). Copia os pacotes de vídeo de renders/preview_yt0018_v7mudo_960x540.mp4 e acrescenta o áudio em AAC 192 kb/s
→ renders/preview_yt0018_v7_960x540.mp4.
uso: python montar_audio.py [video_mudo]"""
import sys
import wave
from fractions import Fraction
from pathlib import Path

import av
import numpy as np

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from unir_voz import cama  # noqa: E402

SR = 44100


def main():
    entrada = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "renders" / "preview_yt0018_v7mudo_960x540.mp4"
    saida_v = Path(sys.argv[2]) if len(sys.argv) > 2 else AQUI / "renders" / "preview_yt0018_v7_960x540.mp4"
    if not entrada.exists():
        sys.exit(f"sem {entrada}")
    ci = av.open(str(entrada))
    vi = ci.streams.video[0]
    dur_v = float(vi.frames / vi.average_rate) if vi.frames else float(ci.duration / 1e6)
    with wave.open(str(AQUI / "audio" / "narracao_v7.wav")) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        voz = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    n = int(round(dur_v * SR))
    if len(voz) < n:                                                  # a cama de sala segue até o fim do vídeo
        resto = cama(n)[len(voz):]
        f = min(len(resto), int(0.5 * SR))
        resto[-f:] *= np.linspace(1, 0, f, dtype=np.float32)
        voz = np.concatenate([voz, resto])
    pcm = np.clip(np.round(voz[:n]), -32768, 32767).astype(np.int16)
    print(f"vídeo {dur_v:.2f} s; narração {len(pcm) / SR:.2f} s (voz termina em {len(voz) / SR:.2f} s antes do preenchimento)")
    co = av.open(str(saida_v), "w")
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
