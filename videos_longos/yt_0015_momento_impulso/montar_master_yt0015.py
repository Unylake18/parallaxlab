"""yt_0015 — master: vídeo final 1080p30 (CRF 14, copiado sem recompressão) + narração normalizada em AAC 192 kb/s.

Igual a videos/montar_master.py (usa o mesmo mux), mas fixa o bitrate do AAC: o padrão do encoder sai a ~70 kb/s em mono e,
nesse bitrate, gerou um pico de +2,7 dBTP. Uso: uv run --no-sync python montar_master_yt0015.py
"""
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory

import av

U = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("montar_master", U.parents[1] / "videos" / "montar_master.py")
mm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mm)

VIDEO = U / "renders" / "video_final_yt0015_1920x1080_30fps.mp4"
AUDIO = U / "audio" / "narracao_master.wav"
MASTER = U / "renders" / "master_yt0015.mp4"


def encode_audio(source, target, kbps=192):
    with av.open(str(source)) as inp, av.open(str(target), "w") as out:
        a = inp.streams.audio[0]
        layout = "mono" if a.channels == 1 else "stereo"
        st = out.add_stream("aac", rate=44100)
        st.layout = layout
        st.bit_rate = kbps * 1000
        rs = av.AudioResampler(format="fltp", layout=layout, rate=44100)
        for fr in inp.decode(a):
            for cv in rs.resample(fr):
                for p in st.encode(cv):
                    out.mux(p)
        for cv in rs.resample(None):
            for p in st.encode(cv):
                out.mux(p)
        for p in st.encode(None):
            out.mux(p)


with TemporaryDirectory() as d:
    m4a = Path(d) / "narracao.m4a"
    encode_audio(AUDIO, m4a)
    mm.mux(VIDEO, m4a, MASTER)
with av.open(str(MASTER)) as r:
    v, s = r.streams.video[0], r.streams.audio[0]
    print(f"{MASTER.name}: {v.width}×{v.height}, {float(v.base_rate):.0f} fps, {float(v.duration * v.time_base):.3f} s vídeo, "
          f"{float(s.duration * s.time_base):.3f} s áudio, AAC {s.codec_context.bit_rate // 1000} kb/s")
