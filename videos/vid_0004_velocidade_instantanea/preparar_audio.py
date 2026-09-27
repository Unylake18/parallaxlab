"""Gera audio/narracao_montagem.wav a partir de audio/narracao_final.wav (intacta).

Único tratamento: a fala termina em "Segue o Parallax Lab"; o trecho falado
"arroba labparallax" é removido (o @ fica só na tela). Corte no meio da pausa
da vírgula (99,76–100,10 s), com fade-out curto para evitar clique.

Uso, na raiz do repositório:
    uv run python videos/vid_0004_velocidade_instantanea/preparar_audio.py
"""

import wave
from pathlib import Path

import numpy as np

AUDIO = Path(__file__).resolve().parent / "audio"
CUT_S = 99.93
FADE_S = 0.03

with wave.open(str(AUDIO / "narracao_final.wav")) as src:
    params = src.getparams()
    assert params.sampwidth == 2, "esperado PCM 16 bits"
    samples = np.frombuffer(src.readframes(params.nframes), dtype=np.int16)

frames = samples.reshape(-1, params.nchannels)[:round(CUT_S * params.framerate)].astype(np.float32)
fade = round(FADE_S * params.framerate)
frames[-fade:] *= np.linspace(1, 0, fade)[:, None]

with wave.open(str(AUDIO / "narracao_montagem.wav"), "wb") as dst:
    dst.setparams(params)
    dst.writeframes(frames.round().astype(np.int16).tobytes())
print(f"narracao_montagem.wav: {len(frames) / params.framerate:.3f} s")
