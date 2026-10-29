"""Gera a narração do yt_0015 em blocos de PARÁGRAFOS inteiros (cada bloco começa numa âncora, com a tag dela).

O `videos/gerar_voz_elevenlabs.py` corta por frase e pode começar um bloco no meio de um parágrafo, sem tag. Aqui os parágrafos de
`narracao_tags.md` são agrupados (≤ 4.500 caracteres), cada grupo vira um .md temporário e o script global é chamado uma vez por
grupo, sem modificá-lo; os WAVs são emendados num só. Uso (na raiz do repositório):
    uv run --no-sync python videos_longos/yt_0015_momento_impulso/gerar_voz_blocos.py --seco
    uv run --no-sync python videos_longos/yt_0015_momento_impulso/gerar_voz_blocos.py audio/narracao_v4.wav
Voz qw7jgPZWOKrl10GsjQ82, modelo eleven_v4, mp3_44100_192 → WAV mono 16 bits 44,1 kHz. Chave só em ELEVENLABS_API_KEY.
"""
import subprocess
import sys
import wave
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
SEC = "## Texto corrido (para gravação)"
VOZ = "qw7jgPZWOKrl10GsjQ82"
LIM = 4500

texto = (AQUI / "narracao_tags.md").read_text(encoding="utf-8").split(SEC, 1)[1].strip()
pars = [p.strip() for p in texto.split("\n\n") if p.strip()]
grupos, atual = [], []
for p in pars:
    if atual and sum(len(x) + 2 for x in atual) + len(p) > LIM:
        grupos.append(atual)
        atual = []
    atual.append(p)
if atual:
    grupos.append(atual)
print(f"{len(pars)} parágrafos em {len(grupos)} blocos: {[sum(len(x) + 2 for x in g) for g in grupos]} caracteres")
seco = "--seco" in sys.argv
tmp = AQUI / "audio" / "_blocos"
tmp.mkdir(parents=True, exist_ok=True)
wavs = []
for i, g in enumerate(grupos, 1):
    md = tmp / f"bloco_{i:02d}.md"
    md.write_text(f"# bloco {i}\n\n{SEC}\n\n" + "\n\n".join(g) + "\n", encoding="utf-8")
    print(f"--- bloco {i}: {len(g)} parágrafos · começa: {g[0][:80]} … termina: …{g[-1][-50:]}")
    if seco:
        continue
    w = tmp / f"bloco_{i:02d}.wav"
    subprocess.run([sys.executable, str(RAIZ / "videos" / "gerar_voz_elevenlabs.py"), str(md), str(w), "--voz", VOZ, "--secao", SEC],
                   check=True, cwd=RAIZ)
    wavs.append(w)
if not seco:
    saida = AQUI / (sys.argv[1] if len(sys.argv) > 1 else "audio/narracao_v4.wav")
    with wave.open(str(saida), "wb") as out:
        for k, w in enumerate(wavs):
            with wave.open(str(w), "rb") as r:
                if k == 0:
                    out.setparams(r.getparams())
                out.writeframes(r.readframes(r.getnframes()))
    with wave.open(str(saida), "rb") as r:
        print(f"{saida}: {r.getnframes() / r.getframerate():.1f} s")
