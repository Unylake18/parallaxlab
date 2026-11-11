"""yt_0028 v2 (handoff v2 §9.6): os 11 erros da v1, antes (preview v1, no instante da avaliação) e depois (v2, no mesmo ponto da fala, achado pelos
gatilhos do log). Saídas: renders/v2/qa/erros_v1_v2.jpg e renders/v2/qa/setas_no_painel_v2.txt (R6, a partir das linhas [r6] dos logs).
uso: python erros_v1_v2.py"""
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

from comparar import ancora, gat, quadro

U = Path(__file__).resolve().parent
OUT = U / "renders" / "v2" / "qa"
V1 = U / "renders" / "v1" / "yt_0028_preview_v1_540p15.mp4"


def q_v1(t):
    c = av.open(str(V1))
    q = round(t * 15)
    for i, fr in enumerate(c.decode(video=0)):
        if i >= q:
            im = fr.to_image()
            c.close()
            return im


E = [("E1 seta do teto", 94.5, "PB1", lambda: gat("PB1", "B1-2", "conforme você chega perto", 0.6)),
     ("E2 setas viram borrão", 524.0, "PB4", lambda: ancora("PB4", "B4-5", 1.6)),
     ("E3 matriz numérica sobreposta", 536.0, "PB6", lambda: gat("PB6", "B6-2", "no nosso ponto", 0.8)),
     ("E4 zoom com cortes", 504.0, "PB6", lambda: gat("PB6", "B6-1", "essa janelinha vira o palco inteiro", 1.6)),
     ("E5 seta errada (vertical)", 386.3, "PB4", lambda: gat("PB4", "B4-4", "agora na vertical", 1.3)),
     ("E6 vírgula decimal", 30.0, "PH", lambda: gat("PH", "H2", "a área continua a mesma", 1.0)),
     ("E7 resumo cortado", 716.0, "PS", lambda: ancora("PS", "S2", -0.1)),
     ("E8 gancho parado", 47.0, "PH", lambda: gat("PH", "H2", "deixa o fluido andar", 3.0)),
     ("E9 fórmula sozinha no B3", 280.0, "PB3", lambda: ancora("PB3", "B3-1", 6.0)),
     ("E10 parado 16 s (B1-3)", 160.0, "PB1", lambda: ancora("PB1", "B1-5", 12.0)),
     ("E11 letras pequenas", 538.0, "PB6", lambda: ancora("PB6", "B6-3", -0.3))]
f = ImageFont.load_default()
linhas = []
for nome, t1, lote, ft in E:
    a, b = q_v1(t1), quadro(lote, ft())
    L = Image.new("RGB", (1920, 568), (5, 11, 24))
    L.paste(a, (0, 28))
    L.paste(b, (960, 28))
    d = ImageDraw.Draw(L)
    d.text((8, 7), f"{nome} · ANTES (v1, {int(t1 // 60)}:{t1 % 60:04.1f})", fill=(255, 120, 120), font=f)
    d.text((968, 7), f"DEPOIS (v2, {lote})", fill=(140, 255, 200), font=f)
    linhas.append(L)
pr = Image.new("RGB", (1920, 568 * len(linhas)))
for i, L in enumerate(linhas):
    pr.paste(L, (0, 568 * i))
pr.save(OUT / "erros_v1_v2.jpg", quality=88)
# R6
LOTES = ["PB1", "PB2", "PB3", "PB4", "PB5"]
out = ["yt_0028 v2 · R6 (seta, curva ou mancha dentro do seu painel), quadro a quadro, nos blocos B1, B2-3, B3-1, B4, B5-2 e B5-4",
       "objetos guardados: setas F(X), F(P+h), F(P+k), quocientes, sombras, discos ε, mancha, segmento [−1, 1], ramos de 2/y, malha imagem, h ∂F/∂x"]
tot = 0
for L_ in LOTES:
    t = (U / f"log_{L_}.txt").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\[r6-total\] (\S+) (\d+) quadros fora em (\d+) quadros checados", t)
    oc = re.findall(r"^\[r6\] (.*)$", t, re.M)
    tot += len(oc)
    out.append(f"  {L_}: {m.group(2) if m else '?'} quadros fora em {m.group(3) if m else '?'} quadros checados")
    out += [f"    {o}" for o in oc]
out.append(f"OCORRÊNCIAS: {tot}")
(OUT / "setas_no_painel_v2.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
