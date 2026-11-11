"""yt_0028 v3 (handoff v3 §9.2): QA de alinhamento (R9). Renderiza em 1080p SÓ os stills dos 37 alvos (still1080.sh, -s, sem vídeo), mede no
pixel a moldura de cada chapa (perfil de brilho atravessando a borda) contra a linha grossa da grade (x = 120k, y = 60 + 120k), e junta as zonas,
origens de papel e bordas de faixa registradas no log ([alinha], coordenadas exatas). Critério ≤ 1 px.
Saídas: renders/v3/qa/alinhamento_v3.txt e renders/v3/qa/alinhamento_v3.jpg (um recorte 1:1 de um canto por alvo).
uso: python alinhamento.py [--sem-render]"""
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from comparar import ALVO

U = Path(__file__).resolve().parent
D = U / "renders" / "v3" / "qa" / "alinhamento"
A_ = [(120, 180, 1080, 900)]
B_ = [(120, 180, 840, 900), (1080, 180, 1800, 900)]
C_ = [(120, 300, 600, 780), (720, 300, 1200, 780), (1320, 300, 1800, 780)]
LAY = {}
for n in (1, 2, 8, 17, 18, 23, 24, 25, 26, 27, 28, 29, 35, 36, 37):
    LAY[n] = ("A", A_)
for n in (3, 4, 5, 6, 9, 10, 11, 14, 15, 16, 19, 21, 22):
    LAY[n] = ("B", B_)
for n in (12, 32, 33, 34):
    LAY[n] = ("C", C_)
PAPEL = {7: ("papel 240 px/u", (600, 540)), 13: ("página", (120, 180)), 20: ("papel 120 px/u", (480, 540)),
         30: ("papel 120 px/u", (480, 420)), 31: ("papel 150 px/u", (360, 780))}


def roda():
    tarefas = [(n, lote, round(f(), 2)) for n, (lote, f) in ALVO.items()]

    def um(t):
        n, lote, tt = t
        if (D / f"still1080_{n:02d}.png").exists():
            return f"{n:02d} já existe"
        r = subprocess.run(["bash", str(U / "still1080.sh"), lote, str(tt), f"{n:02d}"], capture_output=True, text=True, cwd=U)
        return r.stdout.strip()
    with ThreadPoolExecutor(6) as ex:
        for linha in ex.map(um, tarefas):
            print(linha, flush=True)


def borda(a, eixo, fixo, alvo, w=7):
    """Centro dos pixels claros da moldura perto de `alvo` (px) ao atravessar a borda (eixo 'x': linha y = fixo)."""
    lum = a.mean(2)
    perf = lum[fixo, alvo - w:alvo + w] if eixo == "x" else lum[alvo - w:alvo + w, fixo]
    base = np.median(perf)
    claros = np.nonzero(perf > base + 12)[0]
    if not len(claros):
        return None
    return float(claros.mean()) + alvo - w + 0.5          # +0,5: a linha grossa ocupa os pixels X−1 e X, centro em X


def mede():
    linhas = ["yt_0028 v3 · alinhamento (R9): cantos de chapa, zonas, origens de papel e bordas de faixa contra as linhas grossas (x = 120k, y = 60 + 120k px no 1080p)",
              "medido no pixel (stills 1080p dos alvos): a moldura de cada chapa, nas 4 bordas, numa linha/coluna fora da grade; critério ≤ 1 px", ""]
    pior = 0.0
    for n, (lote, _) in ALVO.items():
        f = D / f"still1080_{n:02d}.png"
        if not f.exists():
            linhas.append(f"{n:02d} {lote}: still ausente")
            continue
        a = np.asarray(Image.open(f).convert("RGB"), float)
        if n in LAY:
            nome, caixas = LAY[n]
            for (x0, y0, x1, y1) in caixas:
                ym, xm = (y0 + y1) // 2 + 30, (x0 + x1) // 2 + 30
                med = {"esq": borda(a, "x", ym, x0), "dir": borda(a, "x", ym, x1), "topo": borda(a, "y", xm, y0), "base": borda(a, "y", xm, y1)}
                res = {k: (None if v is None else v - alvo) for (k, v), alvo in zip(med.items(), (x0, x1, y0, y1))}
                r = max(abs(v) for v in res.values() if v is not None) if any(v is not None for v in res.values()) else None
                pior = max(pior, r or 0)
                txt = "  ".join(f"{k} {med[k]:.1f}→{alvo} ({res[k]:+.1f})" if med[k] is not None else f"{k} —" for k, alvo in zip(med, (x0, x1, y0, y1)))
                linhas.append(f"{n:02d} {lote:4s} layout {nome} chapa {(x0, y0, x1, y1)}: {txt}  {'OK' if r is not None and r <= 1 else 'VER'}")
        else:
            linhas.append(f"{n:02d} {lote:4s} {PAPEL[n][0]}: origem/canto {PAPEL[n][1]} (exato no código; ver o registro do log abaixo)")
    linhas += ["", f"PIOR RESÍDUO MEDIDO NAS MOLDURAS: {pior:.2f} px", "", "registro do código ([alinha] nos logs; coordenadas exatas, resíduo = distância à linha grossa):"]
    vistos = set()
    for log in sorted(U.glob("log_P*.txt")):
        for m in re.finditer(r"^\[alinha\] (\S+) (.*?) (-?[0-9.]+) (-?[0-9.]+) (-?[0-9.]+) (-?[0-9.]+)$", log.read_text(encoding="utf-8", errors="replace"), re.M):
            tipo, nome = m.group(1), m.group(2)
            v = [float(m.group(k)) for k in range(3, 7)]
            chave = (tipo, nome, tuple(v))
            if chave in vistos:
                continue
            vistos.add(chave)
            rx = max(abs(v[0] - 120 * round(v[0] / 120)), abs(v[2] - 120 * round(v[2] / 120)))
            ry = max(abs((v[1] - 60) - 120 * round((v[1] - 60) / 120)), abs((v[3] - 60) - 120 * round((v[3] - 60) / 120)))
            if tipo == "faixa":
                rx = rx if v[0] == v[2] else 0.0
                ry = ry if v[1] == v[3] else 0.0
            linhas.append(f"  {log.stem[4:]:4s} {tipo:6s} {nome}: ({v[0]:.0f}, {v[1]:.0f}) – ({v[2]:.0f}, {v[3]:.0f})  resíduo {max(rx, ry):.2f} px")
    (U / "renders" / "v3" / "qa" / "alinhamento_v3.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print("\n".join(linhas[:60]))
    # prancha: um recorte 1:1 (200 × 200) de um canto por alvo
    tiles = []
    fonte = ImageFont.load_default()
    for n in ALVO:
        f = D / f"still1080_{n:02d}.png"
        if not f.exists():
            continue
        im = Image.open(f).convert("RGB")
        if n in LAY:
            x, y = LAY[n][1][0][0], LAY[n][1][0][1]
        else:
            x, y = PAPEL[n][1]
        t = im.crop((x - 100, y - 100, x + 100, y + 100))
        T = Image.new("RGB", (200, 218), (5, 11, 24))
        T.paste(t, (0, 18))
        ImageDraw.Draw(T).text((4, 3), f"{n:02d} canto ({x}, {y})", fill=(255, 220, 90), font=fonte)
        tiles.append(T)
    cols = 8
    pr = Image.new("RGB", (cols * 200, ((len(tiles) + cols - 1) // cols) * 218), (0, 0, 0))
    for i, T in enumerate(tiles):
        pr.paste(T, ((i % cols) * 200, (i // cols) * 218))
    pr.save(U / "renders" / "v3" / "qa" / "alinhamento_v3.jpg", quality=92)


if __name__ == "__main__":
    if "--sem-render" not in sys.argv:
        roda()
    mede()
