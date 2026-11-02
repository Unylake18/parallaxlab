"""yt_0018 v6, handoff §1.2 (e os itens novos §1.1, §1.4, §1.5, §1.6): quadros de conferência tirados do PREVIEW COM VOZ, localizados pela palavra da fala
(audio/voz_posicoes.json). Grava renders/v6/conferencia_v6.png (+ um PNG por item em renders/v6/conferencia/) e imprime a medida de "muda algo a cada ≤ 1,5 s"
na DICA do X1 (maior trecho sem pixel novo, na região da tela).
uso: python conferencia_v6.py [video]"""
import json
import re
import sys
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
VID = Path(sys.argv[1]) if len(sys.argv) > 1 else U / "renders" / "preview_yt0018_v6_960x540.mp4"
POS = json.loads((U / "audio" / "voz_posicoes.json").read_text(encoding="utf-8"))
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
OUT = U / "renders" / "v6"
(OUT / "conferencia").mkdir(parents=True, exist_ok=True)


def palavra(aid, frase):
    fala = ANC[aid]["fala"].split()
    alvo = re.findall(r"\w+", frase.lower())
    k = next(i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo)
    return POS[aid]["palavras"][k]


# (rótulo, âncora, frase, deslocamento em s)
ITENS = [
    ("1.1 ZOOM: painel sem cobrir aresta (cantos)", "X2-3b", "quatro cantos", 1.5),
    ("1.1 ZOOM: painel (pegadinha)", "X2-3b", "quem representa cada pedaço", 0.5),
    ("1.1 ZOOM: cubo volta ao tamanho", "X2-4", "e olha onde ele foi parar", 1.0),
    ("1.2 T perdido: X5-7 abertura", "X5-7", "a tração no fio", 1.0),
    ("1.2 T perdido: X5-7 meio", "X5-7", "quarenta e nove newtons de novo", 1.0),
    ("1.2 T perdido: X5-7 fim", "X5-7", "se o bloco leve fosse sumindo", 5.0),
    ("1.2 85,77° a 90°: com o arco", "X3-10", "nos dois ângulos limite", 0.6),
    ("1.2 85,77° a 90°: pousando", "X3-10", "nos dois ângulos limite", 2.5),
    ("1.2 DICA X1 +0 s", "X1-4", "a dica", 0.0),
    ("1.2 DICA X1 +1,5 s", "X1-4", "a dica", 1.5),
    ("1.2 DICA X1 +3 s", "X1-4", "a dica", 3.0),
    ("1.2 DICA X1 +4,5 s", "X1-4", "a dica", 4.5),
    ("1.2 DICA X1 +6 s", "X1-4", "a dica", 6.0),
    ("1.2 M g⃗ com a seta (X3-2)", "X3-2", "os pesos e o empuxo", 2.0),
    ("1.2 M g⃗ com a seta (fim do X3-2)", "X3-2", "nenhuma força de fora", 3.0),
    ("1.2 T / INTERNA (X5-3)", "X5-3", "força interna", 1.5),
    ("1.2 T / INTERNA (X5-3, depois)", "X5-3", "o peso de tudo", 1.0),
    ("1.4 PESADA: v₂ voando (+0,3 s)", "X4-4", "dois mil joules para a leve", 1.4),
    ("1.4 PESADA: v₂ voando (+0,8 s)", "X4-4", "dois mil joules para a leve", 1.9),
    ("1.4 PESADA: v₂ voando (+1,3 s)", "X4-4", "dois mil joules para a leve", 2.4),
    ("1.5 EN2: pergunta do foguete", "EN2", "como um foguete acelera", 2.5),
    ("1.6 X3-10: fecho com 3 cartões", "X3-10", "a folha foge dele", 1.5),
]
alvos = []
for nome, aid, frase, d in ITENS:
    alvos.append((int(round((palavra(aid, frase) + d) * 15)), nome))
quer = {q for q, _ in alvos}
ims = {}
c = av.open(str(VID))
for i, fr in enumerate(c.decode(video=0)):
    if i in quer:
        ims[i] = fr.to_image()
    if i >= max(quer):
        break
c.close()
W, H = 480, 270
cols = 3
lin = (len(alvos) + cols - 1) // cols
pr = Image.new("RGB", (cols * W, lin * (H + 18)), "black")
d = ImageDraw.Draw(pr)
for k, (q, nome) in enumerate(alvos):
    x, y = (k % cols) * W, (k // cols) * (H + 18)
    pr.paste(ims[q].resize((W, H)), (x, y + 18))
    d.text((x + 3, y + 3), f"{nome} · q{q}", fill="yellow")
    ims[q].save(OUT / "conferencia" / f"{k:02d}_{re.sub(r'[^0-9A-Za-z]+', '_', nome)[:40]}.png")
pr.save(OUT / "conferencia_v6.png")
print("ok", len(alvos), "quadros")

# DICA do X1: maior trecho sem pixel novo (região da tela inteira abaixo do cabeçalho) entre "a dica" e o fim da âncora
a0 = palavra("X1-4", "a dica")
a1 = POS["X1-4"]["palavras"][-1] + 0.5                          # até o fim da fala (a folga entre âncoras não conta)
c = av.open(str(VID))
ant, parado, pior, ini_p = None, 0.0, 0.0, a0
for i, fr in enumerate(c.decode(video=0)):
    t = i / 15
    if t < a0:
        continue
    if t > a1:
        break
    a = np.asarray(fr.to_image().resize((240, 135)), float)[18:]
    if ant is not None:
        mudou = float((np.abs(a - ant).max(axis=2) > 12).mean()) > 0.0002
        parado = 0.0 if mudou else parado + 1 / 15
        if parado > pior:
            pior, ini_p = parado, t - parado
    ant = a
c.close()
print(f"DICA do X1: maior trecho sem pixel novo = {pior:.2f} s, de {ini_p:.1f} s (meta ≤ 1,5 s; fala de {a0:.1f} s a {a1:.1f} s)")
