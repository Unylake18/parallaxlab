"""yt_0028 final §9.2: tiras que provam os ajustes 2.1–2.7 (quadros do preview 540p emendado, nos instantes da voz). → renders/final/qa/tira_*.jpg"""
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
Q = json.loads((U / "renders" / "final" / "quadros_final.json").read_text(encoding="utf-8"))
OUT = U / "renders" / "final" / "qa"


def t_frase(aid, frase, d=0.0):
    fala = A[aid]["fala"].split()
    al = frase.lower().split()
    k = next(i for i in range(len(fala)) if fala[i:i + len(al)] == al)
    return Q[aid] / 15 + A[aid]["t"][k] + d


TIRAS = {
    "2.1_A1_logo": [("A1", "fala pessoal", 1.2), ("A1", "esse é o terceiro episódio", 1.2), ("A1", "para isso entram três ideias", 0.8),
                    ("A1", "numa tabela de quatro números", 1.0), ("A1", "então vamos começar pelo chão", 1.0)],
    "2.2_S2_gancho": [("S2", "no próximo vídeo", 0.5), ("S2", "o integrador do módulo", 0.6), ("S2", "rotacional", 0.4), ("S2", "derivadas parciais", 2.5),
                      ("S2", "se essa aula te ajudou", 1.0)],
    "2.3_M1_onda": [("B1-1", "vamos", -0.15 + k * 0.133) for k in range(7)],
    "2.4_M2_seta": [("B1-1", "a seta do lugar onde você está", 0.8), ("B1-1", "eu trago essa seta", 0.15), ("B1-1", "eu trago essa seta", 0.35),
                    ("B1-1", "eu trago essa seta", 1.0), ("B1-2", "os dois números de baixo", 0.8)],
    "2.5_M3_caminhantes": [("B3-2", "no campo elétrico de uma carga", 1.0), ("B3-2", "no campo elétrico de uma carga", 2.6),
                           ("B3-2", "dependendo do caminho por onde você chega", 1.0), ("B3-2", "dependendo do caminho por onde você chega", 2.6),
                           ("B3-2", "chegando de qualquer lado", 2.0)],
    "2.6_M4_quadradinho": [("B7-3", "olha cada um agindo no quadradinho", 0.0), ("B7-3", "o redemoinho gira", 1.2), ("B7-3", "a explosão cresce", 1.2),
                           ("B7-3", "a deformação estica de um lado", 1.3)],
    "2.7_tag_zoom": [("B6-1", "olha que campo arrumadinho", 0.0), ("B6-4", "tudo isso no modelo linear", 0.0), ("S1", "resumindo", 1.5)],
}
pedidos = {}
for nome, L in TIRAS.items():
    for aid, fr, d in L:
        pedidos.setdefault(round(t_frase(aid, fr, d) * 15), []).append((nome, aid, fr, d))
ims = {}
c = av.open(str(U / "renders" / "final" / "yt_0028_preview_final_540p15.mp4"))
for i, f in enumerate(c.decode(video=0)):
    if i in pedidos:
        for p in pedidos[i]:
            ims[p[1:]] = (f.to_image(), i / 15)
c.close()
fonte = ImageFont.load_default()
for nome, L in TIRAS.items():
    W = min(len(L), 4)
    H = (len(L) + W - 1) // W
    pr = Image.new("RGB", (960 * W, 568 * H), (5, 11, 24))
    for k, p in enumerate(L):
        im, t = ims[p]
        x, y = 960 * (k % W), 568 * (k // W)
        pr.paste(im, (x, y + 28))
        ImageDraw.Draw(pr).text((x + 8, y + 8), f"{p[0]} «{p[1]}» {p[2]:+.2f} s → {int(t // 60)}:{t % 60:05.2f}", fill=(255, 220, 90), font=fonte)
    pr.save(OUT / f"tira_{nome}.jpg", quality=90)
    print(nome, len(L))
