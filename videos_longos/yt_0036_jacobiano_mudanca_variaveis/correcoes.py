"""yt_0036 · prancha das correções v2 (handoff v2, entrega 2): cada quadro de erro do v1 (Q01–Q16, F1–F3) ao lado do still do v2 no mesmo
ponto da fala. O ponto da fala: a âncora do v1 que contém o tempo do quadro e a mesma fração da âncora no v2 (narração v1.1).
Saída: renders/v2/qa/correcoes_v2.jpg.  uso: python correcoes.py"""
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
QE = U / "referencia" / "v2" / "yt_0036_v1_quadros_erros"
MP4 = U / "renders" / "v2" / "yt_0036_preview_v2_540p15.mp4"
OUT = U / "renders" / "v2" / "qa" / "correcoes_v2.jpg"
ITENS = [("Q01", "0:25"), ("Q02", "2:32"), ("Q03", "3:56"), ("Q04", "5:00"), ("Q05", "5:32"), ("Q06", "5:48"), ("Q07", "6:50"), ("Q08", "8:40"),
         ("Q09", "10:24"), ("Q10", "11:08"), ("Q11", "12:40"), ("Q12", "15:00"), ("Q13", "15:44"), ("Q14", "16:50"), ("Q15", "17:48"), ("Q16", "18:24"),
         ("F1_fundo_antes_depois", "5:32"), ("F2_fundo_antes_depois", "15:00"), ("F3_fundo_antes_depois", "8:40")]


def seg(s):
    m, x = s.split(":")
    return int(m) * 60 + float(x)


def ini_real(aid, padrao):
    """Início da âncora NO PREVIEW v2: início do lote (lotes_v2.json) + [ancora] do log do lote (os lotes esticados empurram os seguintes)."""
    import re
    ini = json.loads((U / "renders" / "v2" / "lotes_v2.json").read_text())["inicio"]
    for lote, q0 in ini.items():
        p = U / f"log_{lote}.txt"
        if p.exists():
            m = re.search(rf"^\[ancora\] {re.escape(aid)} ([\d.]+)", p.read_text(encoding="utf-8", errors="ignore"), re.M)
            if m:
                return q0 / 15 + float(m.group(1))
    return padrao


def v1_para_v2(t):
    a1 = json.loads((U / "referencia" / "ancoras_v1.json").read_text(encoding="utf-8"))["ancoras"]
    a2 = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
    for aid, d in a1.items():
        if d["ini"] <= t < d["fim"]:
            fr = (t - d["ini"]) / (d["fim"] - d["ini"])
            e = a2[aid]
            fim2 = e.get("fim", e["ini"] + e.get("dur", 0))
            return aid, fr, ini_real(aid, e["ini"]) + fr * (fim2 - e["ini"])
    raise ValueError(t)


def quadros(ts):
    """Os quadros do preview v2 nos tempos ts (s), num passe só."""
    alvo = sorted((round(t * 15), k) for k, t in enumerate(ts))
    out, i = {}, 0
    c = av.open(str(MP4))
    for q, f in enumerate(c.decode(video=0)):
        while i < len(alvo) and alvo[i][0] == q:
            out[alvo[i][1]] = f.to_image()
            i += 1
        if i >= len(alvo):
            break
    c.close()
    return [out[k] for k in range(len(ts))]


def main():
    try:
        fn = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        fn = ImageFont.load_default()
    info = [(nome, tv1, *v1_para_v2(seg(tv1))) for nome, tv1 in ITENS]
    fr = quadros([x[4] for x in info])
    W, H = 1920, 0
    linhas = []
    for (nome, tv1, aid, f_, t2), im2 in zip(info, fr):
        im1 = Image.open(QE / f"{nome}.jpg").convert("RGB")
        if im1.width > 960:                                 # F1–F3 já vêm com o par v1 | pedido: entra a imagem inteira em cima
            im1 = im1.resize((1920, round(im1.height * 1920 / im1.width)))
            alto = im1.height + 540 + 36
            row = Image.new("RGB", (W, alto), (14, 12, 28))
            row.paste(im1, (0, 0))
            row.paste(im2.resize((960, 540)), (480, im1.height + 36))
            d = ImageDraw.Draw(row)
            d.text((490, im1.height + 6), f"v2 · {int(t2 // 60)}:{t2 % 60:05.2f} · {aid} (mesma fração da âncora)", fill=(250, 220, 90), font=fn)
        else:
            im1 = im1.resize((960, round(im1.height * 960 / im1.width)))
            alto = max(im1.height, 540 + 36)
            row = Image.new("RGB", (W, alto), (14, 12, 28))
            row.paste(im1, (0, 0))
            row.paste(im2.resize((960, 540)), (960, 36))
            d = ImageDraw.Draw(row)
            d.text((970, 6), f"{nome} · v1 {tv1} → v2 {int(t2 // 60)}:{t2 % 60:05.2f} · {aid} (mesma fração da âncora)", fill=(250, 220, 90), font=fn)
        linhas.append(row)
        H += alto + 8
    pr = Image.new("RGB", (W, H), (0, 0, 0))
    y = 0
    for r in linhas:
        pr.paste(r, (0, y))
        y += r.height + 8
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pr.save(OUT, quality=88)
    print(OUT, pr.size)
    for nome, tv1, aid, f_, t2 in info:
        print(f"{nome}: v1 {tv1} → v2 {t2:.2f} s ({aid}, fração {f_:.2f})")


if __name__ == "__main__":
    main()
