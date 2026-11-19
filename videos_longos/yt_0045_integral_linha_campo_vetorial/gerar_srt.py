"""yt_0045 (copiado do yt_0032): legenda.srt (pt-BR) a partir do alinhamento forçado da voz real (alinhamento_palavras.json; sem as tags [ ]).
Blocos de até 2 linhas × 42 caracteres, 2 a 5 s, quebra preferida em fim de frase e depois em vírgula. Tempo do WAV = tempo do vídeo (a voz começa no quadro 0).
uso: python gerar_srt.py  → legenda.srt e o resumo (blocos, faixa de duração, maior linha)."""
import json
import re
from pathlib import Path

U = Path(__file__).resolve().parent
W = json.loads((U / "alinhamento_palavras.json").read_text(encoding="utf-8"))
L, MAXC, DMIN, DMAX = 42, 84, 2.0, 5.0
# formas faladas → escritas na legenda (handoff final §6): "Cálculo três/um" → III/I; "cá" → k; "éfe"/"gê" → f/g; "érre, ésse" → (r, s);
# "eme" minúsculo/maiúsculo → m/M; "alfa" → α; "xis"/"ípsilon" → x/y. Duas palavras que viram uma ficam com o tempo das duas.
# yt_0045 (handoff final §6): "éfe" → f, "bê" → B, "bê um/dois" → B₁/B₂, "erre" → R, "teta" → θ, "pi" → π, o "é" de Euler → e,
# "Cálculo um" → Cálculo I; xis/ípsilon → x/y como nos outros vídeos da série.
TROCA = {"pi": "π", "ômega": "Ω", "gama": "γ"}


def _limpa(w):
    m = re.fullmatch(r"(\W*)(\w+)(\W*)", w)
    return m.groups() if m else ("", w, "")


W2 = []
for i, w in enumerate(W):
    if w.get("skip"):
        continue
    pre, core, pos = _limpa(w["word"])
    low = core.lower()
    if W2 and W2[-1]["word"].rstrip(",.").endswith("Cálculo") and low in ("três", "um"):
        W2[-1] = dict(W2[-1], word=W2[-1]["word"] + " " + ("III" if low == "três" else "I") + pos, end=w["end"])
        continue
    nxt = _limpa(W[i + 1]["word"])[1].lower() if i + 1 < len(W) else ""
    if low == "eme" and nxt.startswith(("maiúscul", "minúscul")):
        W2.append(dict(w, word=pre + ("M" if nxt.startswith("maiúscul") else "m") + pos))
        continue
    if low == "érre" and nxt == "ésse":
        W2.append(dict(w, word=pre + "(r, s)" + _limpa(W[i + 1]["word"])[2], end=W[i + 1]["end"]))
        W[i + 1] = dict(W[i + 1], skip=True)
        continue
    if low == "bê" and nxt in ("um", "dois"):
        W2.append(dict(w, word=pre + ("B₁" if nxt == "um" else "B₂") + _limpa(W[i + 1]["word"])[2], end=W[i + 1]["end"]))
        W[i + 1] = dict(W[i + 1], skip=True)
        continue
    if low in ("x", "y", "z") and nxt == "barra":                   # "x barra" → x̄, "y barra" → ȳ, "z barra" → z̄
        W2.append(dict(w, word=pre + low + "̄" + _limpa(W[i + 1]["word"])[2], end=W[i + 1]["end"]))
        W[i + 1] = dict(W[i + 1], skip=True)
        continue
    nxt2 = _limpa(W[i + 2]["word"])[1].lower() if i + 2 < len(W) else ""
    if low == "gama" and nxt == "linha":                            # "gama linha" → γ′
        W2.append(dict(w, word=pre + "γ′" + _limpa(W[i + 1]["word"])[2], end=W[i + 1]["end"]))
        W[i + 1] = dict(W[i + 1], skip=True)
        continue
    if low == "delta" and nxt == "gama":                            # "delta gama i" → Δγᵢ ; "delta gama" → Δγ
        if nxt2 == "i":
            W2.append(dict(w, word=pre + "Δγᵢ" + _limpa(W[i + 2]["word"])[2], end=W[i + 2]["end"]))
            W[i + 1], W[i + 2] = dict(W[i + 1], skip=True), dict(W[i + 2], skip=True)
        else:
            W2.append(dict(w, word=pre + "Δγ" + _limpa(W[i + 1]["word"])[2], end=W[i + 1]["end"]))
            W[i + 1] = dict(W[i + 1], skip=True)
        continue
    if low == "delta" and nxt == "t" and nxt2 == "i":               # "delta t i" → Δtᵢ
        W2.append(dict(w, word=pre + "Δtᵢ" + _limpa(W[i + 2]["word"])[2], end=W[i + 2]["end"]))
        W[i + 1], W[i + 2] = dict(W[i + 1], skip=True), dict(W[i + 2], skip=True)
        continue
    if low == "d" and nxt in ("x", "y", "z", "t"):                  # "d x" → dx, "d y" → dy, "d z" → dz, "d t" → dt
        W2.append(dict(w, word=pre + "d" + nxt + _limpa(W[i + 1]["word"])[2], end=W[i + 1]["end"]))
        W[i + 1] = dict(W[i + 1], skip=True)
        continue
    if low == "delta" and nxt == "z":                               # "delta z" → Δz
        W2.append(dict(w, word=pre + "Δz" + _limpa(W[i + 1]["word"])[2], end=W[i + 1]["end"]))
        W[i + 1] = dict(W[i + 1], skip=True)
        continue
    if low in TROCA:
        W2.append(dict(w, word=pre + TROCA[low] + pos))
        continue
    W2.append(w)
W = W2


def duas_linhas(t):
    if len(t) <= L:
        return [t]
    p = t.split()
    melhor = None
    for i in range(1, len(p)):
        a, b = " ".join(p[:i]), " ".join(p[i:])
        if len(a) <= L and len(b) <= L:
            c = abs(len(a) - len(b)) - (6 if a[-1] in ",.:;?!…" else 0)
            if melhor is None or c < melhor[0]:
                melhor = (c, [a, b])
    return melhor[1] if melhor else None


blocos, cur = [], []
for i, w in enumerate(W):
    if cur:
        txt = " ".join(x["word"] for x in cur + [w])
        dur = w["end"] - cur[0]["start"]
        ultimo = cur[-1]["word"]
        d0 = cur[-1]["end"] - cur[0]["start"]
        fecha = (len(txt) > MAXC or duas_linhas(txt) is None or dur > DMAX
                 or (ultimo[-1] in ".?!…" and d0 >= DMIN)
                 or (ultimo[-1] in ",:;" and d0 >= DMIN and len(" ".join(x["word"] for x in cur)) > 45))
        if fecha:
            blocos.append(cur)
            cur = []
    cur.append(w)
blocos.append(cur)

srt, durs, maior = [], [], 0
for k, b in enumerate(blocos):
    ini = b[0]["start"]
    prox = blocos[k + 1][0]["start"] if k + 1 < len(blocos) else max(b[-1]["end"] + 1.0, ini + DMIN + 0.1)
    fim = min(prox - 0.04, max(b[-1]["end"] + 0.25, ini + DMIN))
    linhas = duas_linhas(" ".join(x["word"] for x in b))
    maior = max(maior, *map(len, linhas))
    durs.append(fim - ini)
    ts = lambda s: (lambda m: f"{m // 3600000:02d}:{m // 60000 % 60:02d}:{m // 1000 % 60:02d},{m % 1000:03d}")(int(round(s * 1000)))
    srt.append(f"{k + 1}\n{ts(ini)} --> {ts(fim)}\n" + "\n".join(linhas) + "\n")
(U / "legenda.srt").write_text("\n".join(srt), encoding="utf-8")
fora = [i + 1 for i, d in enumerate(durs) if d < DMIN - 0.01 or d > DMAX + 0.3]
print(f"{len(blocos)} blocos; duração {min(durs):.2f}–{max(durs):.2f} s; maior linha {maior}; fora de 2–5 s: {fora}")
