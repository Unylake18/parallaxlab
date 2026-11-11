"""yt_0027 final §4.4: checagens automáticas do WAV da narração → qa/voz.txt.
Duração, picos/clipping, silêncio > 1,5 s dentro de um parágrafo (pelo alinhamento forçado), tags lidas em voz alta e pronúncias
(pela transcrição STT de conferência), e as emendas entre os blocos da API (salto de nível / clique na palavra que abre cada bloco).
uso: python qa_voz.py"""
import json
import re
import wave
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
WAV = U / "audio" / "narracao_final.wav"
out = []
with wave.open(str(WAV)) as w:
    sr, n = w.getframerate(), w.getnframes()
    x = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768
dur = n / sr
pico = float(np.abs(x).max())
clip = int((np.abs(x) >= 0.999).sum())
out += [f"arquivo: {WAV.name} · {sr} Hz mono 16 bits · duração {dur:.2f} s ({int(dur // 60)}:{dur % 60:05.2f})",
        f"pico {pico:.3f} ({20 * np.log10(pico):.1f} dBFS) · amostras em clipping (|x| ≥ 0,999): {clip}"]

pal = json.loads((U / "alinhamento_palavras.json").read_text(encoding="utf-8"))
txt = (U / "narracao_tags.md").read_text(encoding="utf-8").split("## Texto corrido (para gravação)")[1]
pars = [p for p in re.split(r"\n\s*\n", txt) if p.strip()]
n_par = [len(re.findall(r"\w+", re.sub(r"\[[^\]]*\]", "", p))) for p in pars]
bord, k = set(), 0
for c in n_par:
    k += c
    bord.add(k)
toks = []
for i, p in enumerate(pal):
    for _ in re.findall(r"\w+", p["word"]):
        toks.append(i)
ini_par = {toks[b] for b in bord if b < len(toks)}
sil_in, sil_par = [], []
for i in range(1, len(pal)):
    g = pal[i]["start"] - pal[i - 1]["end"]
    if g > 1.5:
        (sil_par if i in ini_par else sil_in).append((pal[i - 1]["end"], g, pal[i - 1]["word"], pal[i]["word"]))
gaps = [pal[i]["start"] - pal[i - 1]["end"] for i in range(1, len(pal))]
out.append(f"palavras alinhadas: {len(pal)} · maior pausa entre palavras: {max(gaps):.2f} s · silêncio > 1,5 s dentro de parágrafo: {len(sil_in)}"
           f" · entre parágrafos: {len(sil_par)}")
for t, g, a, b in sil_in:
    out.append(f"  [silêncio] {t:8.2f}s  {g:.2f} s  «{a} … {b}»")
fala = pal[-1]["end"] - pal[0]["start"]
npal = sum(n_par)
out.append(f"taxa real: {npal} palavras ÷ {fala:.1f} s de fala = {npal / fala:.2f} palavras/s (estimativa do handoff: 3,0)")

stt = json.loads((U / "transcricao_stt.json").read_text(encoding="utf-8"))
st = stt.get("text", "").lower()
tags = {t: st.count(t) for t in ("curious", "thoughtful", "emphatic", "excited", "happy", "calm", "satisfied")}
out.append(f"tags lidas em voz alta (STT): {sum(tags.values())} {tags if sum(tags.values()) else ''}")
for t in ("ômega", "nabla", "laplaciano", "vorticidade", "parallax lab", "rankine", "classe c1", "chama de h"):
    out.append(f"  pronúncia (STT): «{t}» {st.count(t)}× (texto: {re.sub(r'[\[][^]]*[]]', '', txt).lower().count(t)}×)")

# emendas da API: a palavra que abre cada bloco (mesma divisão do gerar_voz_elevenlabs.py, limite 4500)
import importlib.util
sp = importlib.util.spec_from_file_location("gv", U.parents[1] / "videos" / "gerar_voz_elevenlabs.py")
gv = importlib.util.module_from_spec(sp)
sp.loader.exec_module(gv)
bl = gv.blocos(gv.extrair((U / "narracao_tags.md").read_text(encoding="utf-8"), "## Texto corrido (para gravação)"), 4500)
k = 0
out.append(f"blocos da API: {len(bl)}")
for j, b in enumerate(bl):
    nb = len(re.findall(r"\w+", re.sub(r"\[[^\]]*\]", "", b)))
    if j:
        i = toks[k]
        t0 = (pal[i - 1]["end"] + pal[i]["start"]) / 2
        a = int(pal[i - 1]["end"] * sr)
        bb = int(pal[i]["start"] * sr)
        seg = x[a:bb] if bb > a else x[a - 10:a + 10]
        rms_l = 20 * np.log10(np.sqrt(np.mean(x[max(0, a - int(3.7 * sr)):a] ** 2)) + 1e-9)
        rms_r = 20 * np.log10(np.sqrt(np.mean(x[bb:bb + int(3.7 * sr)] ** 2)) + 1e-9)
        salto = float(np.abs(np.diff(seg)).max()) if len(seg) > 2 else 0.0
        out.append(f"  emenda {j}: {t0:8.2f}s «{pal[i - 1]['word']} | {pal[i]['word']}» pausa {pal[i]['start'] - pal[i - 1]['end']:.2f} s · nível antes {rms_l:.1f} dB,"
                   f" depois {rms_r:.1f} dB (Δ {rms_r - rms_l:+.1f}) · maior salto entre amostras na pausa {salto:.3f}")
    k += nb
(U / "qa").mkdir(exist_ok=True)
(U / "qa" / "voz.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
