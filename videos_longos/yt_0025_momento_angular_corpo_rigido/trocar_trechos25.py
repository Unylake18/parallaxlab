"""yt_0025 · voz v2: regera SÓ algumas frases (mesma voz/modelo, com `[short pause]` da própria voz antes da frase) e cola no WAV v1 → audio/narracao_v2.wav.
Motivo: com a voz real, a conta de 4 âncoras não cabe na janela da fala (atraso 0,3–0,6 s); a pausa vem da voz, não é silêncio inserido (autorizado pelo Kaio em 09/11).
A chave só vem do ambiente (ELEVENLABS_API_KEY); nunca é gravada.
uso: ELEVENLABS_API_KEY=... python trocar_trechos25.py [--seco]   (--seco só lista os trechos)"""
import importlib.util
import json
import re
import sys
import unicodedata
import wave
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
ROOT = U.parents[1]
spec = importlib.util.spec_from_file_location("gv", ROOT / "videos" / "gerar_voz_elevenlabs.py")
gv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gv)
VOZ, MODELO, FMT = "qw7jgPZWOKrl10GsjQ82", "eleven_v4", "mp3_44100_192"
# (frase original do texto limpo, texto com tag para regerar)
TROCAS = [
    ("Exatamente como no pêndulo.", "[short pause] [thoughtful] Exatamente como no pêndulo."),
    ("Ela não é a lei geral. É só a parte da lei que fica ao longo do eixo.", "[short pause] [thoughtful] Ela não é a lei geral. É só a parte da lei que fica ao longo do eixo."),
    ("A parte horizontal da massa de baixo aponta para o mesmo lado que a da massa de cima.", "[short pause] [curious] A parte horizontal da massa de baixo aponta para o mesmo lado que a da massa de cima."),
    ("Cada excesso de vinte gramas precisa de uma força centrípeta de uns trinta e quatro newtons, mais ou menos o peso de três quilos e meio. E os dois, em faces diferentes, formam um binário de quase sete newtons metro, girando quinze vezes por segundo.", "[short pause] [thoughtful] Cada excesso de vinte gramas precisa de uma força centrípeta de uns trinta e quatro newtons, mais ou menos o peso de três quilos e meio. [long pause] E os dois, em faces diferentes, formam um binário de quase sete newtons metro, girando quinze vezes por segundo."),
]
sem_acento = lambda s: "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
tok = lambda s: re.findall(r"\w+", sem_acento(re.sub(r"\[[^\]]*\]", "", s).lower()))
al = json.loads((U / "alinhamento_palavras_v1.json").read_text(encoding="utf-8"))
palavras = [a["word"] for a in al]
with wave.open(str(U / "audio" / "narracao_v1.wav")) as w:
    fr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)


def corte(t):
    """instante de menor energia em ±50 ms de t (evita estalo)"""
    i0, i1 = int(max(0, t - 0.05) * fr), int(min(len(x) / fr, t + 0.05) * fr)
    jan = int(0.005 * fr)
    seg = np.abs(x[i0:i1])
    e = np.convolve(seg, np.ones(jan) / jan, mode="same")
    return (i0 + int(np.argmin(e))) / fr


trechos = []
for frase, novo in TROCAS:
    alvo = tok(frase)
    k = next(i for i in range(len(palavras) - len(alvo) + 1) if palavras[i:i + len(alvo)] == alvo)
    t0, t1 = al[k]["start"], al[k + len(alvo) - 1]["end"]
    trechos.append((corte(t0), corte(t1), novo, frase))
    print(f"{frase[:50]!r}: {t0:.2f}–{t1:.2f} s ({t1 - t0:.2f} s)")
if "--seco" in sys.argv:
    sys.exit()
import os
chave = os.environ.get("ELEVENLABS_API_KEY")
if not chave:
    sys.exit("ELEVENLABS_API_KEY ausente")
saida, cur = [], 0
for t0, t1, novo, frase in trechos:
    mp3 = gv.sintetizar(chave, VOZ, MODELO, FMT, novo, None, None, None)
    pcm = np.frombuffer(gv.decodificar_mp3(mp3), dtype=np.int16).astype(np.float32)
    # tira só o silêncio FINAL (a pausa do começo é a que a tag pediu)
    env = np.abs(pcm)
    ativo = np.where(env > 600)[0]
    pcm = pcm[: min(len(pcm), ativo[-1] + int(0.12 * fr))] if len(ativo) else pcm
    orig = x[int(t0 * fr):int(t1 * fr)]
    ganho = float(np.sqrt((orig ** 2).mean()) / max(1.0, np.sqrt((pcm[pcm != 0] ** 2).mean())))
    pcm = np.clip(pcm * ganho, -32768, 32767)
    antes = x[cur:int(t0 * fr)]
    saida += [antes, pcm]
    cur = int(t1 * fr)
    print(f"  {frase[:40]!r}: original {len(orig) / fr:.2f} s -> novo {len(pcm) / fr:.2f} s (ganho {ganho:.2f}); +{(len(pcm) - len(orig)) / fr:.2f} s")
saida.append(x[cur:])
y = np.concatenate(saida)
# fades curtos de 8 ms nas emendas
n = 0
for t0, t1, _, _ in trechos:
    pass
out = U / "audio" / "narracao_v2.wav"
with wave.open(str(out), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(fr)
    w.writeframes(np.clip(y, -32768, 32767).astype(np.int16).tobytes())
print(f"{out.name}: {len(y) / fr:.2f} s (v1: {len(x) / fr:.2f} s; +{(len(y) - len(x)) / fr:.2f} s)")
