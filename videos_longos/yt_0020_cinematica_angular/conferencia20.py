"""yt_0020 — pranchas por bloco e quadros de conferência (handoff §6.4), a partir dos renders de cada lote.
Cada quadro é pedido como (âncora, fração da âncora); o tempo vem das linhas [ancora] do log do lote.
uso: python conferencia20.py [rodada]  → renders/<rodada>/prancha_<BLOCO>.png e renders/<rodada>/conferencia/<nome>.png"""
import re
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
RODADA = sys.argv[1] if len(sys.argv) > 1 else "v1"
LOTE_DE = {}
for l in ("PH", "PT1", "PT2", "PT3", "PT4", "PT5", "PE1", "PE2", "PE3", "PS"):
    lg = (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace") if (U / f"log_{l}.txt").exists() else ""
    anc = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", lg)]
    for (a, t0), (_, t1) in zip(anc, anc[1:]):
        LOTE_DE[a] = (l, t0, t1)

CONF = [("H2", 0.85), ("T1-3", 0.6), ("T1-5", 0.9), ("T2-3", 0.7), ("T3-4", 0.45), ("T3-4", 0.97), ("T3-6", 0.95), ("T4-2", 0.6), ("T4-3", 0.8),
        ("T4-6", 0.6), ("T5-2", 0.95), ("T5-4", 0.3), ("T5-4", 0.75), ("T5-6", 0.72), ("T5-6", 0.82), ("T5-8", 0.85), ("E1-3", 0.9), ("E1-6", 0.8),
        ("E2-2", 0.9), ("E2-5", 0.85), ("E3-2", 0.75), ("E3-4", 0.95), ("E3-6", 0.9), ("S1", 0.95)]
BLOCOS = {"PH": ["H1", "H2", "H3"], "PA": ["A1", "A2", "A3"], "PT1": ["T1-1", "T1-2", "T1-3", "T1-4", "T1-5"], "PT2": ["T2-1", "T2-2", "T2-3", "T2-4", "T2-5"],
          "PT3": ["T3-1", "T3-2", "T3-3", "T3-4", "T3-5", "T3-6"], "PT4": ["T4-1", "T4-2", "T4-3", "T4-4", "T4-5", "T4-6"],
          "PT5": ["T5-1", "T5-2", "T5-3", "T5-4", "T5-5", "T5-6", "T5-7", "T5-8"], "PE1": ["E1-1", "E1-2", "E1-3", "E1-4", "E1-5", "E1-6"],
          "PE2": ["E2-1", "E2-2", "E2-3", "E2-4", "E2-5"], "PE3": ["E3-1", "E3-2", "E3-3", "E3-4", "E3-5", "E3-6"], "PS-EN": ["S1", "S2", "EN1", "EN2"]}


def quadros(pedidos):
    """{(âncora, fração): imagem}, lendo cada vídeo de lote uma vez."""
    por_lote = {}
    for a, fr in pedidos:
        if a not in LOTE_DE:
            continue
        l, t0, t1 = LOTE_DE[a]
        por_lote.setdefault(l, []).append((round((t0 + fr * (t1 - t0)) * 15), (a, fr)))
    out = {}
    for l, lst in por_lote.items():
        alvo = {q: k for q, k in lst}
        c = av.open(str(U / f"media_{l}/videos/cena/540p15/{l}.mp4"))
        for i, f in enumerate(c.decode(video=0)):
            if i in alvo:
                out[alvo[i]] = (f.to_image(), l, i)
            if i > max(alvo):
                break
        c.close()
    return out


def prancha(itens, saida, C=3):
    W, H = 640, 360
    L = (len(itens) + C - 1) // C
    pr = Image.new("RGB", (W * C, (H + 20) * L), "black")
    d = ImageDraw.Draw(pr)
    for k, (rot, im) in enumerate(itens):
        x, y = (k % C) * W, (k // C) * (H + 20)
        pr.paste(im.resize((W, H)), (x, y + 20))
        d.text((x + 4, y + 4), rot, fill="yellow")
    pr.save(saida)


dst = U / "renders" / RODADA
(dst / "conferencia").mkdir(parents=True, exist_ok=True)
q = quadros(CONF)
for (a, fr), (im, l, i) in q.items():
    im.save(dst / "conferencia" / f"{a}_{int(fr * 100):02d}.png")
for b, ancs in BLOCOS.items():
    ped = [(a, f) for a in ancs for f in ((0.25, 0.7) if len(ancs) > 4 else (0.2, 0.55, 0.9))]
    qq = quadros(ped)
    itens = [(f"{a} {int(f * 100)}%  ({qq[(a, f)][1]} q{qq[(a, f)][2]})", qq[(a, f)][0]) for a, f in ped if (a, f) in qq]
    if itens:
        prancha(itens, dst / f"prancha_{b}.png")
print(len(q), "quadros de conferência;", len(BLOCOS), "pranchas em", dst)
