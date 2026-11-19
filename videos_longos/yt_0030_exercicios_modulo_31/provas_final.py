"""yt_0030 · provas das correções C1–C7 do handoff final (quadros 960×540 dos lotes, por gatilho) → renders/final/qa/c*_*.png.
uso: python provas_final.py"""
import re
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
OUT = U / "renders" / "final" / "qa"
OUT.mkdir(parents=True, exist_ok=True)
FONTE = ImageFont.load_default()


def t_gat(lote, aid, frase, dt):
    log = (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")
    a = {m.group(1): float(m.group(2)) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log)}
    if frase is None:
        return a[aid] + dt
    m = re.search(r"\[gatilho\] %s +([0-9.]+)s \(alvo[^)]*\) %s" % (re.escape(aid), re.escape(frase)), log)
    return a[aid] + float(m.group(1)) + dt


def quadros(lote, ts):
    c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
    alvo = sorted({round(t * 15): t for t in ts}.items())
    out, k = {}, 0
    for i, fr in enumerate(c.decode(video=0)):
        while k < len(alvo) and i >= alvo[k][0]:
            out[alvo[k][1]] = fr.to_image()
            k += 1
        if k >= len(alvo):
            break
    c.close()
    return [out[t] for t in ts]


def tira(nome, lote, itens, escala=1.0, recorte=None):
    ts = [t_gat(lote, a, f, d) for a, f, d, _ in itens]
    ims = quadros(lote, ts)
    if recorte:
        ims = [im.crop(recorte) for im in ims]
    if escala != 1:
        ims = [im.resize((int(im.width * escala), int(im.height * escala)), Image.LANCZOS) for im in ims]
    w, h = ims[0].size
    pr = Image.new("RGB", (w, (h + 24) * len(ims)), (5, 11, 24))
    d = ImageDraw.Draw(pr)
    for k, (im, (a, f, dt, rot)) in enumerate(zip(ims, itens)):
        pr.paste(im, (0, k * (h + 24) + 24))
        d.text((8, k * (h + 24) + 6), f"{lote} {a} t={ts[k]:.2f}s · {rot}", fill=(255, 220, 90), font=FONTE)
    pr.save(OUT / nome)
    print(OUT / nome)
    return ims


if __name__ == "__main__":
    tira("c1_d4_legenda.png", "PD4", [("D4-7", "a componente horizontal é o quadrado", 0.5, "C1: SÓ A COMPONENTE HORIZONTAL P (sem 'NO PALCO')")])
    tira("c2_a4_tira.png", "PA4", [("A4-1", "iguala cada deformação a zero", 0.0, "A4-1 no meio: campo ③ à direita"),
                                   ("A4-2", "o nosso campo é exatamente o quadrado", 0.45, "'o nosso campo': o campo acende"),
                                   ("A4-3", "agora lê como transformação", 0.5, "50% do voo da malha (o campo já saiu)"),
                                   ("A4-3", "agora lê como transformação", 3.6, "fim da morfose")])
    tira("c3_d4_zoom.png", "PD4", [("D4-6", "item d confere com um zoom", 1.0, "'confere com um zoom': sem moldura vazia à direita"),
                                   ("D4-6", "deixava as setas arrumadinhas", 1.4, "'arrumadinhas': a janela do zoom à esquerda"),
                                   ("D4-6", "aqui olha o zoom de dez vezes", 0.85, "fim do voo: moldura e zoom × 10 juntos")])
    tira("c5_a3_graficos.png", "PA3", [("A3-3", "o campo do fio cai", 1.5, "1/r: toca o teto num ponto"),
                                       ("A3-5", "e a da gravitação", 0.6, "1/r² e 1/r tracejado")], escala=2.0, recorte=(560, 270, 900, 460))
    ims = tira("c6_a3_coulomb.png", "PA3", [("A3-5", "e a da gravitação", 0.6, "COULOMB · GRAVITAÇÃO")], escala=2.0, recorte=(555, 210, 760, 235))
    tira("c7_abertura.png", "PH", [("A-1", None, 2.6, "'bem-vindos': a silhueta da escada"),
                                   ("A-1", "vai ser uma escada", 0.3, "'vai ser uma escada'"),
                                   ("A-1", "pausa o vídeo e tenta", 0.3, "'pausa o vídeo e tenta'")])
