"""yt_0010 — confere a sincronização: atrasos das âncoras (atrasos.json) e prancha de quadros no início de cada frase.

Uso: uv run --no-sync python videos_longos/yt_0010_fem_movimento/conferir_sync.py VIDEO.mp4 [N_INICIAL N_FINAL]
Saídas: quadros/sync_NN.png (3 colunas; cada quadro = instante em que a frase começa, legenda = texto falado).
"""
import json
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

PASTA = Path(__file__).resolve().parent


def main():
    video = sys.argv[1]
    n0, n1 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 49)
    try:
        at = json.load(open(PASTA / "atrasos.json"))["atrasos"]
        v = [a for _, a in at]
        print(f"âncoras: {len(v)}; atraso máx {max(v):.2f} s; >0,25 s: {sum(a > 0.25 for a in v)}; >1 s: {sum(a > 1 for a in v)}")
        for sid, a in at:
            if a > 0.25:
                print("  atraso", sid, a)
    except FileNotFoundError:
        pass
    fr = json.load(open(PASTA / "frases.json", encoding="utf-8"))
    alvos = [(k, i, f) for k in sorted(fr) if n0 <= int(k[1:]) <= n1 for i, f in enumerate(fr[k])]
    c = av.open(video)
    s = c.streams.video[0]
    quadros, j = {}, 0
    for fm in c.decode(video=0):
        t = float(fm.pts * s.time_base)
        while j < len(alvos) and t >= alvos[j][2]["t0"] + 0.4:
            quadros[j] = fm.to_image().resize((640, 360))
            j += 1
        if j >= len(alvos):
            break
    fonte = ImageFont.load_default()
    por, cols = 12, 3
    for p in range(0, len(alvos), por):
        grupo = list(range(p, min(p + por, len(alvos))))
        rows = (len(grupo) + cols - 1) // cols
        sh = Image.new("RGB", (640 * cols, 400 * rows), (5, 8, 22))
        d = ImageDraw.Draw(sh)
        for q, jj in enumerate(grupo):
            if jj not in quadros:
                continue
            x, y = (q % cols) * 640, (q // cols) * 400
            sh.paste(quadros[jj], (x, y))
            k, i, f = alvos[jj]
            d.text((x + 4, y + 362), f"{k}.{i} {f['t0']:.1f}s  {f['texto'][:92]}", fill=(230, 235, 255), font=fonte)
        sh.save(PASTA / "quadros" / f"sync_{p // por + 1:02d}.png")
    print(len(alvos), "frases;", (len(alvos) + por - 1) // por, "pranchas")


if __name__ == "__main__":
    main()
