"""yt_0045 §5: seis amostras curtas de pronúncia (mp3) em audio/teste_pronuncia/. Chave só do ambiente (ELEVENLABS_API_KEY)."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "videos"))
from gerar_voz_elevenlabs import sintetizar  # noqa: E402

U = Path(__file__).resolve().parent
FR = ["F de gama de t, escalar gama linha de t, d t.",
      "Integral sobre gama de P d x mais Q d y mais R d z.",
      "Gama de t igual a cosseno de t, seno de t, c t.",
      "Dois pi menos meio, mais ou menos cinco vírgula setenta e oito.",
      "c é um sobre quatro pi, e o trabalho zera quando c vale um.",
      "n R ao quadrado seno de dois pi sobre n: a soma de Riemann do redemoinho."]
for i, f in enumerate(FR, 1):
    d = sintetizar(os.environ["ELEVENLABS_API_KEY"], "qw7jgPZWOKrl10GsjQ82", "eleven_v4", "mp3_44100_192", "[thoughtful] " + f, "", "", None)
    (U / "audio" / "teste_pronuncia" / f"amostra_{i}.mp3").write_bytes(d)
    print(i, len(d), f)
