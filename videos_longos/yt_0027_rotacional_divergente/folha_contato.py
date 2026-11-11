"""yt_0027 (copiado do yt_0026; v3 = handoff v3 §7.4): folha de contato do preview completo.
  v1/v2: um quadro por âncora, tirado a 70% da âncora.
  v3:    um quadro a cada 2,5 s (páginas de 48 quadros) e a varredura de TODOS os quadros: "vazio" = nada além do papel, do canto e da logo
         (menos de 400 px a 960×540 diferentes do fundo milimetrado); "sem canto" = a linha 2 do canto ausente (fora o cartão final do CTA).
uso: python folha_contato.py [rodada] → renders/folha_contato_<rodada>[_N].png (+ renders/<rodada>/qa/quadros_vazios_<rodada>.txt no v3)"""
import json
import sys
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v1"
c = av.open(str(U / "renders" / f"preview_yt0027_{R}_960x540.mp4"))
n = c.streams.video[0].frames

if R in ("v1", "v2"):
    q = json.loads((U / "renders" / f"quadros_{R}.json").read_text(encoding="utf-8"))
    ordem = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ordem"]
    ini = [q[a] for a in ordem]
    alvo = {int(i0 + 0.7 * (i1 - i0)): a for a, i0, i1 in zip(ordem, ini, ini[1:] + [n])}
    ims = {}
    for i, fr in enumerate(c.decode(video=0)):
        if i in alvo:
            ims[alvo[i]] = (i, fr.to_image())
    W, H, C = 480, 270, 4
    L = (len(ordem) + C - 1) // C
    pr = Image.new("RGB", (W * C, (H + 18) * L), "black")
    d = ImageDraw.Draw(pr)
    for k, a in enumerate(ordem):
        x, y = (k % C) * W, (k // C) * (H + 18)
        if a in ims:
            i, im = ims[a]
            pr.paste(im.resize((W, H)), (x, y + 18))
            d.text((x + 4, y + 3), f"{a}  q{i}  {i // 15 // 60}:{i / 15 % 60:04.1f}", fill="yellow")
    pr.save(U / "renders" / f"folha_contato_{R}.png")
    print(len(ims), "âncoras;", n, "quadros")
    sys.exit()

FPS, PASSO = 15, round(2.5 * 15)
bg = np.asarray(Image.open(U / "renders" / "fundo" / "papel_vazio_960x540.png").convert("RGB"), np.int16)
mask = np.ones((540, 960), bool)
mask[:62, :340] = False          # canto (linhas 1 e 2)
mask[:50, 820:] = False          # logo
canto2 = (slice(36, 58), slice(14, 200))   # faixa da linha 2 do canto (baseline 100 px a 1080p)
vaz, semc, amostra = [], [], []
for i, fr in enumerate(c.decode(video=0)):
    a = fr.to_ndarray(format="rgb24").astype(np.int16)
    dif = np.abs(a - bg).max(2) > 28
    if int(dif[mask].sum()) < 400:
        vaz.append(i)
    if int(dif[canto2].sum()) < 30:
        semc.append(i)
    if i % PASSO == 0:
        amostra.append((i, Image.fromarray(a.astype(np.uint8))))


def trechos(lst):
    out = []
    for i in lst:
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return out


def mmss(i):
    return f"{i // FPS // 60}:{i / FPS % 60:04.1f}"


fim_cta = n - 1
rel = [f"yt_0027 {R}: varredura de {n} quadros ({n / FPS:.1f} s) — quadro vazio = < 400 px diferentes do papel fora do canto e da logo"]
tv = trechos(vaz)
rel.append(f"QUADROS VAZIOS: {len(vaz)} quadros em {len(tv)} trechos")
rel += [f"  {mmss(a)} – {mmss(b)}  ({(b - a + 1) / FPS:.2f} s, q{a}–q{b})" for a, b in tv]
ts = trechos(semc)
rel.append(f"SEM A LINHA 2 DO CANTO: {len(semc)} quadros em {len(ts)} trechos (o cartão final do CTA não tem canto, como no yt_0026)")
rel += [f"  {mmss(a)} – {mmss(b)}  ({(b - a + 1) / FPS:.2f} s)" for a, b in ts]
(U / "renders" / R / "qa").mkdir(parents=True, exist_ok=True)
(U / "renders" / R / "qa" / f"quadros_vazios_{R}.txt").write_text("\n".join(rel) + "\n", encoding="utf-8")
print("\n".join(rel[:40]))

W, H, C, POR = 480, 270, 6, 48
setv = set(vaz)
for pg in range((len(amostra) + POR - 1) // POR):
    bloco = amostra[pg * POR:(pg + 1) * POR]
    L = (len(bloco) + C - 1) // C
    pr = Image.new("RGB", (W * C, (H + 18) * L), "black")
    d = ImageDraw.Draw(pr)
    for k, (i, im) in enumerate(bloco):
        x, y = (k % C) * W, (k // C) * (H + 18)
        pr.paste(im.resize((W, H)), (x, y + 18))
        d.text((x + 4, y + 3), f"{mmss(i)}  q{i}" + ("  VAZIO" if i in setv else ""), fill="red" if i in setv else "yellow")
    pr.save(U / "renders" / f"folha_contato_{R}_{pg + 1}.png")
print(len(amostra), "quadros na folha;", n, "quadros")
