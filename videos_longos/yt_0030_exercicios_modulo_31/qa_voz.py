"""yt_0030 · handoff final §4.4 (copiado do yt_0028): checagens automáticas do WAV final → qa/voz.txt. Duração (parada 2 se > 32:30); pico e
clipping; silêncio > 1,5 s dentro de parágrafo (entre palavras do alinhamento forçado); tag lida em voz alta e pronúncias na transcrição de
conferência (STT); fronteiras entre os blocos da API (as mesmas divisões do gerar_voz_elevenlabs.py: pausa, salto de nível, clique);
taxa real (palavras ÷ segundos de fala)."""
import json
import re
import sys
import wave
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
sys.path.insert(0, str(U.parents[1] / "videos"))
from gerar_voz_elevenlabs import blocos, extrair  # noqa: E402

SEC = "## Texto corrido (para gravação)"
W = U / "audio" / "narracao_final.wav"
with wave.open(str(W)) as w:
    sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
    a = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768
dur = n / sr
md_txt = (U / "narracao_tags.md").read_text(encoding="utf-8")
partes = blocos(extrair(md_txt, SEC), 4500)
L = [f"yt_0030 · QA da voz ({W.name})",
     f"modelo eleven_v4 · voz qw7jgPZWOKrl10GsjQ82 · mp3_44100_192 → WAV {ch} canal, {8 * sw} bits, {sr} Hz · texto narracao_tags.md v3.4 · voz v3.3 + 11 trechos v3.4 emendados (22 emendas: ver qa/emendas_v34.txt)",
     f"duração {dur:.2f} s ({int(dur // 60)}:{dur % 60:05.2f}); limite da parada: 41:30 → {'OK' if dur <= 2490 else 'PASSA (parada 2)'}"]
pk = float(np.abs(a).max())
clip = int((np.abs(a) >= 0.999).sum())
L.append(f"pico {20 * np.log10(pk):.2f} dBFS; amostras em clipping (|x| ≥ 0,999): {clip} → {'OK' if clip == 0 else 'FALHA'}")
P = json.loads((U / "alinhamento_palavras.json").read_text(encoding="utf-8"))
md = md_txt.split(SEC)[1]
pars = [re.findall(r"\w+", re.sub(r"\[[^\]]*\]", "", p).lower()) for p in md.split("\n\n") if p.strip() and not p.startswith("---")]
pars = [p for p in pars if p]
toks = [(i, t) for i, p in enumerate(P) for t in re.findall(r"\w+", p["word"].lower())]
fim_par, k = set(), 0
for p in pars:
    k += len(p)
    fim_par.add(toks[k - 1][0])
gaps = [(P[i]["end"], P[i + 1]["start"], P[i]["word"], P[i + 1]["word"]) for i in range(len(P) - 1)]
dentro = [(x, y, u, v) for i, (x, y, u, v) in enumerate(gaps) if i not in fim_par and y - x > 1.5]
L.append(f"parágrafos {len(pars)}; silêncios > 1,5 s dentro de parágrafo: {len(dentro)}"
         + "".join(f"\n  {x:.2f}–{y:.2f} s ({y - x:.2f} s) entre «{u}» e «{v}»" for x, y, u, v in dentro))
entre = [y - x for i, (x, y, _, _) in enumerate(gaps) if i in fim_par]
L.append(f"pausas entre parágrafos: {len(entre)}; {min(entre):.2f}–{max(entre):.2f} s (média {np.mean(entre):.2f} s); "
         f"maior pausa entre palavras no texto todo {max(y - x for x, y, _, _ in gaps):.2f} s")
S = json.loads((U / "transcricao_stt.json").read_text(encoding="utf-8"))
st = S.get("text", "").lower()
tags = {t: len(re.findall(t, st)) for t in ("curious", "thoughtful", "emphatic", "excited", "happy")}
L.append(f"tag lida em voz alta (STT): {tags} → {'OK' if not any(tags.values()) else 'FALHA'}")
chave = {"Parallax Lab": r"parallax\s*lab", "Cálculo três": r"c[áa]lculo (tr[êe]s|3|iii)", "fi": r"\bfi\b|\bphi\b|\bφ", "nabla": r"nabla",
         "alfa": r"\balfa\b|\balpha\b|α", "épsilon": r"[ée]psilon|ε", "delta": r"\bdelta\b|δ", "ípsilon": r"[íi]psilon", "cê um": r"c[êe] um|\bc1\b|c¹",
         "Schwarz": r"schwar[tz]", "Cauchy-Riemann": r"cauchy|riemann", "Laplace": r"laplace", "Mercator": r"mercator",
         "Groenlândia": r"groenl[âa]ndia", "Ampère": r"amp[èe]re", "Gauss": r"gauss", "Coulomb": r"coulomb|culomb", "agá": r"\bag[áa]\b", "tê": r"\bt[êe]\b", "esse": r"\besse\b", "vê": r"\bv[êe]\b"}
esperado = {nome: sum(len(re.findall(rx, " ".join(p))) for p in pars) for nome, rx in chave.items()}
for nome, rx in chave.items():
    L.append(f"  «{nome}» no STT: {len(re.findall(rx, st))}× (no texto: {esperado[nome]}×)")
pal = sum(len(p) for p in pars)
pal_split = sum(len(re.sub(r"\[[^\]]*\]", " ", p).split()) for p in md.split("\n\n") if p.strip())
L.append(f"palavras {pal_split} (tokens \\w+ {pal}); {pal_split / dur:.3f} palavras/s no WAV inteiro; "
         f"{pal_split / (P[-1]['end'] - P[0]['start']):.3f} palavras/s do início ao fim da fala (estimativa 3,0 palavras/s = {pal_split / 3 / 60:.2f} min)")
seq = [t for _, t in toks]
rms = lambda t0, t1: 20 * np.log10(np.sqrt(np.mean(a[int(max(0, t0) * sr):int(t1 * sr)] ** 2)) + 1e-9)
# v3.4: as fronteiras são as 22 emendas (qa_emendas_v34.py → qa/emendas_v34.txt)
(U / "qa").mkdir(exist_ok=True)
(U / "qa" / "voz.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
