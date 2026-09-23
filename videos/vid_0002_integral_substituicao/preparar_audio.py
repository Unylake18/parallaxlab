"""Recria a narração usada na montagem a partir do WAV aprovado.

Remove 1,8 s de silêncio inicial e ajusta somente a frase em 26,12–29,44 s.
O arquivo-fonte nunca é modificado.
"""

from pathlib import Path
import wave

import numpy as np


AUDIO = Path(__file__).resolve().parent / "audio"
SOURCE = AUDIO / "narracao_final.wav"
OUTPUT = AUDIO / "narracao_montagem.wav"
TRIM_SECONDS = 1.8
START, END, FADE, GAIN_DB = 26.12, 29.44, 0.14, 1.2


def main() -> None:
    with wave.open(str(SOURCE), "rb") as reader:
        params = reader.getparams()
        assert (params.nchannels, params.sampwidth, params.framerate) == (2, 2, 44100)
        samples = np.frombuffer(reader.readframes(reader.getnframes()), dtype="<i2")
        samples = samples.reshape(-1, params.nchannels)

    rate = params.framerate
    samples = samples[round(TRIM_SECONDS * rate):].copy()
    start, end, fade = (round(value * rate) for value in (START, END, FADE))
    gain = 10 ** (GAIN_DB / 20)
    envelope = np.full(end - start, gain, dtype=np.float64)
    phase = np.linspace(0, np.pi / 2, fade, endpoint=True)
    envelope[:fade] = 1 + (gain - 1) * np.sin(phase) ** 2
    envelope[-fade:] = 1 + (gain - 1) * np.sin(phase[::-1]) ** 2
    corrected = np.rint(samples[start:end].astype(np.float64) * envelope[:, None])
    assert np.max(np.abs(corrected)) < 32768
    samples[start:end] = corrected.astype("<i2")

    with wave.open(str(OUTPUT), "wb") as writer:
        writer.setparams(params)
        writer.writeframes(samples.tobytes())
    print(f"{OUTPUT}: {len(samples) / rate:.6f} s")


if __name__ == "__main__":
    main()
