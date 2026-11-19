"""yt_0023 v5 — quadros de conferência (resolução cheia 960×540) dos lotes renderizados + tiras de 6 quadros consecutivos de um `passo` com termo
novo e de um `voa` (caneta). uso: python conf_v5.py   → renders/v5/conferencia/*.png, renders/v5/prancha_conferencia_v5.png"""
import re
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
OUT = U / "renders/v5/conferencia"
OUT.mkdir(parents=True, exist_ok=True)

PEDE = [("E1-1_a", "PE1a", "E1-1", 0.30), ("E1-1_b", "PE1a", "E1-1", 0.80), ("E1-3", "PE1a", "E1-3", 0.45), ("E1-3_b", "PE1a", "E1-3", 0.85), ("E1-4", "PE1a", "E1-4", 0.55),
        ("E1-5", "PE1a", "E1-5", 0.30), ("E1-6", "PE1a", "E1-6", 0.55), ("E1-9", "PE1a", "E1-9", 0.70),
        ("E3-1", "PE3", "E3-1", 0.45), ("E3-3", "PE3", "E3-3", 0.50), ("E3-3_b", "PE3", "E3-3", 0.95), ("E3-7", "PE3", "E3-7", 0.60),
        ("E2-2", "PE2", "E2-2", 0.55), ("E2-6", "PE2", "E2-6", 0.60), ("E2-9", "PE2", "E2-9", 0.60),
        ("E4-1", "PE4", "E4-1", 0.80), ("E4-7", "PE4", "E4-7", 0.55), ("E4-9", "PE4", "E4-9", 0.60)]


def ancoras(L):
    log = (U / f"log_{L}.txt").read_text(encoding="utf-8", errors="replace")
    return [(n, float(t)) for n, t in re.findall(r"\[ancora\] (\S+) ([\d.]+)", log)]


def mp4(L):
    return U / f"media_{L}/videos/cena/540p15/{L}.mp4"


def quadros(L, ts):
    """{t: imagem} do lote L nos instantes ts (s)."""
    c = av.open(str(mp4(L)))
    fps = float(c.streams.video[0].average_rate)
    want = {}
    for t in ts:
        want.setdefault(int(round(t * fps)), []).append(t)
    got = {}
    for i, f in enumerate(c.decode(video=0)):
        if i in want:
            im = f.to_image()
            for t in want[i]:
                got[t] = im
        if i > max(want):
            break
    return got


def main():
    pedidos = {}
    for nome, L, anc, fr in PEDE:
        if not mp4(L).exists():
            continue
        a = ancoras(L)
        d = dict(a)
        if anc not in d:
            print("sem âncora", anc, L)
            continue
        lst = [t for n, t in a]
        t0 = d[anc]
        t1 = min([t for t in lst if t > t0] + [t0 + 30.0])
        pedidos.setdefault(L, []).append((nome, t0 + fr * (t1 - t0)))
    ims = []
    for L, lst in pedidos.items():
        g = quadros(L, [t for _, t in lst])
        for nome, t in lst:
            if t in g:
                g[t].save(OUT / f"{nome}.png")
                d = g[t].copy()
                ImageDraw.Draw(d).text((6, 4), f"{nome} · {L} {t:.1f}s", fill=(255, 255, 0))
                ims.append((nome, d))
    ordem = [p[0] for p in PEDE]
    ims.sort(key=lambda x: ordem.index(x[0]))
    cols = 3
    rows = (len(ims) + cols - 1) // cols
    P = Image.new("RGB", (960 * cols, 540 * rows))
    for k, (n, im) in enumerate(ims):
        P.paste(im, ((k % cols) * 960, (k // cols) * 540))
    P.save(U / "renders/v5/prancha_conferencia_v5.png")
    print(len(ims), "quadros de conferência")
    # tiras de 6 quadros consecutivos (a 15 fps, passo de 2 quadros = 0,133 s): primeiro `passo` com termo novo e primeiro `voa` de PE1a
    log = (U / "log_PE1a.txt").read_text(encoding="utf-8", errors="replace")
    ev = re.findall(r"\[caneta\] (\S+) (passo|voa) (?:novos=(\d+)|fixos=(\d+)) .*?t=([\d.]+)", log)
    pas = [(a, float(t)) for a, tipo, nv, fx, t in ev if tipo == "passo" and int(nv or 0) > 0]
    voa = [(a, float(t)) for a, tipo, nv, fx, t in ev if tipo == "voa" and int(fx or 0) > 0]
    for nome, lst in (("passo", pas[:3]), ("voa", voa[:3])):
        if not lst:
            print("sem evento", nome)
            continue
        a, t = lst[min(1, len(lst) - 1)]
        c = av.open(str(mp4("PE1a")))
        fps = float(c.streams.video[0].average_rate)
        k0 = int(round(t * fps))
        want = [k0 + 3 * j for j in range(6)]
        fr = {}
        for i, f in enumerate(c.decode(video=0)):
            if i in want:
                fr[i] = f.to_image()
            if i > max(want):
                break
        tira = Image.new("RGB", (960 * 3, 540 * 2))
        for j, k in enumerate(want):
            if k in fr:
                d = fr[k].copy()
                ImageDraw.Draw(d).text((6, 4), f"{nome} {a} t={k / fps:.2f}s", fill=(255, 255, 0))
                tira.paste(d, ((j % 3) * 960, (j // 3) * 540))
        tira.save(U / f"renders/v5/tira_caneta_{nome}.png")
        print("tira", nome, a, t)


if __name__ == "__main__":
    main()
