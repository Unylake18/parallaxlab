"""Voz do yt_0017 por âncora (ElevenLabs v4): lê `narracao_tags_v4_2.md` (seção "## Por âncora": um `### ID` por âncora, já com a tag de
abertura) e grava audio/ancoras_v42/<ID>.wav; não regera o que já existe (apague o arquivo para regerar uma âncora). No fim escreve
audio/ancoras_v42/duracoes.json (segundos de fala de cada âncora, sem o silêncio das pontas). A chave vem só de ELEVENLABS_API_KEY.
uso: python voz_por_ancora.py [--seco]"""
import json
import os
import re
import sys
import wave
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
sys.path.insert(0, str(U.parents[1] / "videos"))
from gerar_voz_elevenlabs import decodificar_mp3, sintetizar  # noqa: E402

VOZ, MODELO, TAXA = "qw7jgPZWOKrl10GsjQ82", "eleven_v4", 44100
DIR = U / "audio" / "ancoras_v42"


def trechos():
    t = (U / "narracao_tags_v4_2.md").read_text(encoding="utf-8")
    t = t[t.index("## Por âncora"):t.index("## Texto corrido")]
    return [(b.split("\n", 1)[0].strip(), " ".join(b.split("\n", 1)[1].split())) for b in re.split(r"^### ", t, flags=re.M)[1:]]


def fala_s(pcm):
    """Duração entre o primeiro e o último trecho acima de −40 dBFS (janelas de 10 ms)."""
    x = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
    n = TAXA // 100
    rms = np.sqrt(np.mean(x[: len(x) // n * n].reshape(-1, n) ** 2, axis=1))
    on = np.nonzero(rms > 0.01)[0]
    return (on[0] * n / TAXA, (on[-1] + 1) * n / TAXA) if len(on) else (0.0, len(x) / TAXA)


def main():
    ts = trechos()
    print(f"{len(ts)} âncoras, {sum(len(x) for _, x in ts)} caracteres")
    if "--seco" in sys.argv:
        for a, x in ts:
            print(f"{a}: {x[:90]}…")
        return
    chave = os.environ.get("ELEVENLABS_API_KEY")
    if not chave:
        sys.exit("Defina ELEVENLABS_API_KEY no ambiente.")
    DIR.mkdir(parents=True, exist_ok=True)
    dur = {}
    for a, x in ts:
        arq = DIR / f"{a}.wav"
        if not arq.exists():
            print(f"{a} …", flush=True)
            pcm = decodificar_mp3(sintetizar(chave, VOZ, MODELO, "mp3_44100_192", x, "", "", None))
            with wave.open(str(arq), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(TAXA); w.writeframes(pcm)
        with wave.open(str(arq)) as w:
            pcm = w.readframes(w.getnframes())
        i0, i1 = fala_s(pcm)
        dur[a] = {"ini": round(i0, 3), "fim": round(i1, 3), "fala": round(i1 - i0, 3), "arquivo": round(len(pcm) / 2 / TAXA, 3)}
    (DIR / "duracoes.json").write_text(json.dumps(dur, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"fala total {sum(v['fala'] for v in dur.values()) / 60:.2f} min")


if __name__ == "__main__":
    main()
