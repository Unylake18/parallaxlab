"""Junta cada trecho renderizado (A,B,K,D,E,F) à fatia correspondente da voz (narracao_montagem.wav). Avaliação, não é master."""
import json, wave
import av, numpy as np
from pathlib import Path
P = Path(__file__).resolve().parent
dur = json.loads((P / "duracoes_v3_1.json").read_text(encoding="utf-8"))
with wave.open(str(P / "audio/narracao_montagem.wav")) as w:
    sr = w.getframerate(); ch = w.getnchannels()
    raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, ch)
for T in "ABKDEF":
    blocos = json.loads((P / f"renders/blocos_v3_1_{T}.json").read_text(encoding="utf-8"))["blocos"]
    off = dur[blocos[0]["id"]]["t"] - blocos[0]["inicio"]
    src = P / f"renders/m_{T}/videos/cena/540p15/trecho_{T}_v1_6.mp4"
    out = P / f"renders/trechos_com_voz/trecho_{T}_com_voz.mp4"
    with av.open(str(src)) as iv:
        sv = iv.streams.video[0]
        dv = float(iv.duration) / 1e6
        i0 = int(round(max(off, 0) * sr)); i1 = min(len(raw), int(round((off + dv) * sr)))
        seg = raw[i0:i1]
        with av.open(str(out), "w") as o:
            ov = o.add_stream_from_template(sv)
            oa = o.add_stream("aac", rate=sr); oa.layout = "stereo"; oa.bit_rate = 192000
            for p in iv.demux(sv):
                if p.dts is None: continue
                p.stream = ov; o.mux(p)
            frame = av.AudioFrame.from_ndarray(np.ascontiguousarray(seg.reshape(1, -1)), format="s16", layout="stereo"); frame.sample_rate = sr
            rs = av.AudioResampler(format="fltp", layout="stereo", rate=sr)
            for f in rs.resample(frame):
                for p in oa.encode(f): o.mux(p)
            for f in rs.resample(None):
                for p in oa.encode(f): o.mux(p)
            for p in oa.encode(None): o.mux(p)
    print(T, f"t_abs {off:.1f}–{off + dv:.1f} s", round(out.stat().st_size / 1e6, 1), "MB")
