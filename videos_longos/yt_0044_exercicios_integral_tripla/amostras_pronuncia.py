"""yt_0044 §5: seis amostras curtas de pronúncia (mp3) em audio/teste_pronuncia/. Chave só do ambiente (ELEVENLABS_API_KEY)."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "videos"))
from gerar_voz_elevenlabs import sintetizar  # noqa: E402

U = Path(__file__).resolve().parent
FR = ["O x barra é cinco nonos, e o z barra é um quinto.",
      "Com w igual a x mais y, o d w é d y.",
      "Rô igual a k vezes r, e o centro sobe para dois quintos de R.",
      "Com téta indo de menos pi sobre dois a pi sobre dois, s vai até dois R cosseno de téta.",
      "r ao quadrado seno de fi, e a tangente de alfa é R sobre h.",
      "Três décimos de M R ao quadrado, e o cubo pela aresta dá dois terços de M L ao quadrado."]
for i, f in enumerate(FR, 1):
    d = sintetizar(os.environ["ELEVENLABS_API_KEY"], "qw7jgPZWOKrl10GsjQ82", "eleven_v4", "mp3_44100_192", "[thoughtful] " + f, "", "", None)
    (U / "audio" / "teste_pronuncia" / f"amostra_{i}.mp3").write_bytes(d)
    print(i, len(d), f)
