"""yt_0019 v10: R0 antes (master v9) × depois (master v10) no mesmo instante, um PNG por item do handoff v10 (F1–F10, M1–M9, fecho).
Saídas em renders/v10/r0/<item>.png (esquerda v9 | direita v10, 960x540 cada, os instantes empilhados) e renders/v10/r0_itens.json.
uso: python conferencia10.py ANTIGO.mp4 NOVO.mp4"""
import json
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
OUT = U / "renders" / "v10" / "r0"
OUT.mkdir(parents=True, exist_ok=True)
ITENS = {
    "F01_empuxo_T2-5": [319.5, 321.8, 324.6, 326.4],
    "F02_T1-2": [105.5, 106.2],
    "F03_T1-3": [138.0, 140.0],
    "F04_tsiolkovsky": [444.0, 444.6],
    "F05_gravidade": [629.5, 630.5],
    "F06_tq": [711.8, 712.6],
    "F07_af": [747.5, 748.5],
    "F08_P_carga": [818.5, 826.8],
    "F09_mf_Rmax": [833.5, 834.5],
    "F10_m02": [893.5, 894.5],
    "M01_T2-1": [180.5],
    "M02_T2-3": [242.0, 252.0],
    "M03_T2-3b": [273.0],
    "M04_foguete3d": [356.0],
    "M05_curva": [489.0],
    "M06_barra": [553.0],
    "M07_caixa_rel": [575.0],
    "M08_logo": [40.5],
    "M09_neste_video": [50.0, 56.0],
    "FECHO": [1127.0, 1131.0, 1140.0, 1148.0, 1160.0],
}


def pega(arq, alvos):
    c = av.open(str(arq))
    v = c.streams.video[0]
    fps = float(v.average_rate)
    q = {int(round(t * fps)): t for t in alvos}
    out, mx = {}, max(q)
    for i, fr in enumerate(c.decode(v)):
        if i in q:
            out[q[i]] = fr.to_image().resize((960, 540))
        if i >= mx:
            break
    return out


def main():
    antigo, novo = sys.argv[1], sys.argv[2]
    todos = sorted({t for ts in ITENS.values() for t in ts})
    a, b = pega(antigo, todos), pega(novo, todos)
    for nome, ts in ITENS.items():
        fo = Image.new("RGB", (1920, 560 * len(ts)), "black")
        d = ImageDraw.Draw(fo)
        for k, t in enumerate(ts):
            y = 560 * k
            d.text((6, y + 3), f"{nome} · {int(t // 60)}:{t % 60:04.1f}   v9 (antes)  ←→  v10 (depois)", fill="white")
            if t in a:
                fo.paste(a[t], (0, y + 20))
            if t in b:
                fo.paste(b[t], (960, y + 20))
        fo.save(OUT / f"{nome}.png")
    (U / "renders" / "v10" / "r0_itens.json").write_text(json.dumps(ITENS, indent=1), encoding="utf-8")
    print("ok", len(ITENS))


if __name__ == "__main__":
    main()
