"""yt_0028 final §4.4: checagens automáticas do WAV final → qa/voz.txt. Duração; pico e clipping; silêncio > 1,5 s dentro de parágrafo (entre palavras
do alinhamento forçado); tag lida em voz alta e palavras-chave na transcrição de conferência (STT); fronteiras entre os 4 blocos da API (salto de nível
e intervalo entre a última palavra de um bloco e a primeira do seguinte); taxa real (palavras ÷ segundos de fala)."""
import json
import re
import wave
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
W = U / "audio" / "narracao_final.wav"
with wave.open(str(W)) as w:
    sr, n = w.getframerate(), w.getnframes()
    a = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768
dur = n / sr
L = [f"yt_0028 · QA da voz ({W.name})", f"modelo eleven_v4 · voz qw7jgPZWOKrl10GsjQ82 · texto narracao_tags.md v5 (handoff final §3) · 4 blocos de API",
     f"duração {dur:.2f} s ({int(dur // 60)}:{dur % 60:05.2f}); limite da parada: 17:30 → {'OK' if dur <= 1050 else 'PASSA'}"]
pk = float(np.abs(a).max())
clip = int((np.abs(a) >= 0.999).sum())
L.append(f"pico {20 * np.log10(pk):.2f} dBFS; amostras em clipping (|x| ≥ 0,999): {clip} → {'OK' if clip == 0 else 'FALHA'}")
P = json.loads((U / "alinhamento_palavras.json").read_text(encoding="utf-8"))
md = (U / "narracao_tags.md").read_text(encoding="utf-8").split("## Texto corrido (para gravação)")[1]
pars = [re.findall(r"\w+", re.sub(r"\[[^\]]*\]", "", p).lower()) for p in md.split("\n\n") if p.strip() and not p.startswith("---")]
pars = [p for p in pars if p]
fim_par, k = set(), 0
toks = [(i, t) for i, p in enumerate(P) for t in re.findall(r"\w+", p["word"].lower())]
for p in pars:
    k += len(p)
    fim_par.add(toks[k - 1][0])
gaps = [(P[i]["end"], P[i + 1]["start"], P[i]["word"], P[i + 1]["word"]) for i in range(len(P) - 1)]
dentro = [(x, y, u, v) for i, (x, y, u, v) in enumerate(gaps) if i not in fim_par and y - x > 1.5]
L.append(f"silêncios > 1,5 s dentro de parágrafo: {len(dentro)}" + "".join(f"\n  {x:.2f}–{y:.2f} s ({y - x:.2f} s) entre «{u}» e «{v}»" for x, y, u, v in dentro))
entre = [y - x for i, (x, y, _, _) in enumerate(gaps) if i in fim_par]
L.append(f"pausas entre parágrafos: {len(entre)}; {min(entre):.2f}–{max(entre):.2f} s (média {np.mean(entre):.2f} s); maior pausa entre palavras no texto todo {max(y - x for x, y, _, _ in gaps):.2f} s")
S = json.loads((U / "transcricao_stt.json").read_text(encoding="utf-8"))
st = S.get("text", "").lower()
tags = {t: len(re.findall(t, st)) for t in ("curious", "thoughtful", "emphatic", "excited", "happy")}
L.append(f"tag lida em voz alta (STT): {tags} → {'OK' if not any(tags.values()) else 'FALHA'}")
chave = {"épsilon": r"[ée]psilon", "delta": r"delta", "jacobiana": r"jacobiana", "cê um": r"c[êe] um|c1|c¹", "cê erre": r"c[êe] erre|cr\b|cʳ",
         "newtoniano": r"newtonian", "Parallax Lab": r"parallax lab"}
for nome, rx in chave.items():
    L.append(f"  «{nome}» no STT: {len(re.findall(rx, st))}×")
pal = sum(len(p) for p in pars)
fala = sum(p["end"] - p["start"] for p in P)
L.append(f"palavras {pal}; {pal / dur:.2f} palavras/s no WAV inteiro; {pal / (P[-1]['end'] - P[0]['start']):.2f} palavras/s do início ao fim da fala "
         f"(referência 3,0 palavras/s)")
# fronteiras entre blocos: as primeiras palavras dos blocos 2, 3 e 4 (gerar_voz_elevenlabs.py --seco)
fr = ["então o limite de um campo existe", "a vertical diz quanto muda", "os dois giros no mesmo sentido"]
seq = [t for _, t in toks]
for f in fr:
    al = f.split()
    j = next(i for i in range(len(seq)) if seq[i:i + len(al)] == al)
    wi = toks[j][0]
    x, y = P[wi - 1]["end"], P[wi]["start"]
    rms = lambda t0, t1: 20 * np.log10(np.sqrt(np.mean(a[int(t0 * sr):int(t1 * sr)] ** 2)) + 1e-9)
    L.append(f"fronteira de bloco antes de «{f}»: pausa {y - x:.2f} s ({x:.2f}–{y:.2f}); nível 2 s antes {rms(x - 2, x):.1f} dB × 2 s depois {rms(y, y + 2):.1f} dB")
    # borda abrupta: maior salto entre amostras na pausa
    seg = a[int(x * sr):int(y * sr)]
    L.append(f"  maior salto entre amostras na pausa: {np.abs(np.diff(seg)).max() if len(seg) > 1 else 0:.4f} (clique > 0,2)")
(U / "qa" / "voz.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
