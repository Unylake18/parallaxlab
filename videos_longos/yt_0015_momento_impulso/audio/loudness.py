"""yt_0015 — loudness da narração para o master (revisão GPT, item C): −14 LUFS integrado, teto −1 dBTP.

Sem ffmpeg/pyloudnorm no ambiente: medida ITU-R BS.1770-4 (filtro K, blocos de 400 ms com 75% de sobreposição, portas −70 LUFS
absoluta e −10 LU relativa) e pico real por sobreamostragem 4× (scipy). Ganho fixo até o alvo + limitador com antecipação (5 ms,
liberação 80 ms) sobre o pico real; repete o ajuste de ganho até o integrado ficar a ±0,1 LU do alvo.
Uso: uv run --no-sync python audio/loudness.py [entrada.wav] [saida.wav] [--medir arquivo.(wav|mp4) ...]
"""
import json
import sys
import wave
from pathlib import Path

import numpy as np
from scipy.signal import lfilter, resample_poly
from scipy.ndimage import minimum_filter1d

AQUI = Path(__file__).resolve().parent
ALVO, TETO = -14.0, -1.0


def biquad(G, Q, fc, rate, tipo):
    A = 10 ** (G / 40)
    w0 = 2 * np.pi * fc / rate
    al = np.sin(w0) / (2 * Q)
    c = np.cos(w0)
    if tipo == "shelf":
        b = [A * ((A + 1) + (A - 1) * c + 2 * np.sqrt(A) * al), -2 * A * ((A - 1) + (A + 1) * c), A * ((A + 1) + (A - 1) * c - 2 * np.sqrt(A) * al)]
        a = [(A + 1) - (A - 1) * c + 2 * np.sqrt(A) * al, 2 * ((A - 1) - (A + 1) * c), (A + 1) - (A - 1) * c - 2 * np.sqrt(A) * al]
    else:
        b = [(1 + c) / 2, -(1 + c), (1 + c) / 2]
        a = [1 + al, -2 * c, 1 - al]
    return np.array(b) / a[0], np.array(a) / a[0]


def lufs(x, rate):
    y = x
    for args in ((4.0, 1 / np.sqrt(2), 1500.0, rate, "shelf"), (0.0, 0.5, 38.0, rate, "hp")):
        b, a = biquad(*args)
        y = lfilter(b, a, y)
    T, step = int(0.4 * rate), int(0.1 * rate)
    z = np.array([np.mean(y[i:i + T] ** 2) for i in range(0, len(y) - T + 1, step)])
    l = -0.691 + 10 * np.log10(z + 1e-20)
    z1 = z[l > -70]
    rel = -0.691 + 10 * np.log10(np.mean(z1)) - 10
    z2 = z1[(-0.691 + 10 * np.log10(z1 + 1e-20)) > rel]
    return -0.691 + 10 * np.log10(np.mean(z2))


def pico_real(x):
    return 20 * np.log10(np.max(np.abs(resample_poly(x, 4, 1))) + 1e-20)


def limita(x, rate, teto_lin):
    env = np.abs(resample_poly(x, 4, 1))
    env = np.maximum.reduceat(env, np.arange(0, len(env), 4))[:len(x)]
    g = np.minimum(1.0, teto_lin / np.maximum(env, 1e-12))
    la = int(0.005 * rate)
    g = minimum_filter1d(g, size=2 * la + 1)                     # antecipação: o ganho já desce antes do pico
    rel = np.exp(-1 / (0.08 * rate))
    out = np.empty_like(g)
    cur = 1.0
    for i, gi in enumerate(g):                                    # ataque imediato, liberação exponencial
        cur = gi if gi < cur else gi + (cur - gi) * rel
        out[i] = cur
    return x * out


def ler(p):
    p = Path(p)
    if p.suffix.lower() == ".wav":
        with wave.open(str(p), "rb") as w:
            rate, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
            x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768
        return x.reshape(-1, ch).mean(axis=1), rate
    import av
    c = av.open(str(p))
    rs = av.AudioResampler(format="flt", layout="mono", rate=44100)
    xs = [f.to_ndarray().ravel() for fr in c.decode(audio=0) for f in rs.resample(fr)]
    return np.concatenate(xs).astype(np.float64), 44100


if "--medir" in sys.argv:
    for arq in sys.argv[sys.argv.index("--medir") + 1:]:
        x, r = ler(arq)
        print(f"{arq}: {lufs(x, r):.2f} LUFS integrado · pico real {pico_real(x):.2f} dBTP")
    sys.exit(0)
ent = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "narracao_v4.wav"
sai = Path(sys.argv[2]) if len(sys.argv) > 2 else AQUI / "narracao_master.wav"
x, rate = ler(ent)
L0, P0 = lufs(x, rate), pico_real(x)
teto = 10 ** ((TETO - 0.5) / 20)                     # folga para o AAC e para o pico entre amostras
ganho = ALVO - L0
for _ in range(6):
    y = limita(x * 10 ** (ganho / 20), rate, teto)
    L = lufs(y, rate)
    if abs(L - ALVO) <= 0.1:
        break
    ganho += ALVO - L
P = pico_real(y)
pcm = np.clip(np.round(y * 32767), -32768, 32767).astype(np.int16)
with wave.open(str(sai), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(rate)
    w.writeframes(pcm.tobytes())
rel = {"entrada": ent.name, "saida": sai.name, "antes": {"lufs": round(L0, 2), "pico_real_dbtp": round(P0, 2)},
       "depois": {"lufs": round(L, 2), "pico_real_dbtp": round(P, 2)}, "ganho_db": round(ganho, 2), "alvo": ALVO, "teto": TETO}
(AQUI / "loudness_master.json").write_text(json.dumps(rel, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(rel, ensure_ascii=False))
