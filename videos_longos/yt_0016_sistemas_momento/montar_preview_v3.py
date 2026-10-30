"""Emenda os lotes do preview v3 na ordem do vídeo → renders/preview_yt0016_v3_960x540.mp4 (H.264 CRF 14, sem áudio).
Ordem: PH hook+abertura · P7 T7 · P8 T8 · P9 T9 · P10 T10 · Q6 E6 · Q7 E7 · Q8 E8 · Q9 E9 · PC coda · PS síntese e fim.
Transição entre lotes (= capítulos): dissolve de 0,4 s (6 quadros) do último quadro do lote anterior para o novo, sem mudar a duração total.
v3: na faixa do header (linhas 2 e 3, à esquerda) o header antigo sai em 3 quadros e só então o novo entra (nunca os dois sobrepostos):
o quadro intermediário é o mínimo dos dois (tira o texto claro de ambos e mantém o fundo comum).
Grava também renders/capitulos_v3.txt (início de cada capítulo, formato do YouTube)."""
import json
from fractions import Fraction
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
M = lambda c: U / f"media_{c}/videos/cena/540p15/{c}.mp4"
partes = [("PH", None), ("P7", "SISTEMAS DE PARTÍCULAS"), ("P8", "FORÇA INTERNA NÃO MOVE O SISTEMA"), ("P9", "ESCOLHER O SISTEMA"),
          ("P10", "COMO A ENERGIA SE DIVIDE"), ("Q6", "EXERCÍCIO 6 · AGARRAR OU REBATER"), ("Q7", "EXERCÍCIO 7 · O CAÇADOR NO LAGO"),
          ("Q8", "EXERCÍCIO 8 · OS GASES DO RIFLE"), ("Q9", "EXERCÍCIO 9 · NEWTON E A LUZ"), ("PC", "A LUZ TAMBÉM TEM MOMENTO"),
          ("PS", "RESUMO")]
DISS = 6
HY, HX = slice(34, 90), slice(0, 720)          # faixa das linhas 2 e 3 do header (960×540)
saida = U / "renders" / "preview_yt0016_v3_960x540.mp4"
out = av.open(str(saida), "w")
s = out.add_stream("libx264", rate=Fraction(15))
s.width, s.height, s.pix_fmt = 960, 540, "yuv420p"
s.options = {"crf": "14", "preset": "medium"}
t, marcas, ultimo = 0, [], None
for nome, cap in partes:
    c = av.open(str(M(nome)))
    n = 0
    for fr in c.decode(video=0):
        img = fr.to_ndarray(format="rgb24")
        if ultimo is not None and n < DISS:
            novo = img.copy()
            w = 1 - (n + 1) / (DISS + 1)
            img = (img.astype(np.float32) * (1 - w) + ultimo.astype(np.float32) * w + 0.5).astype(np.uint8)
            a, b = ultimo[HY, HX].astype(np.float32), novo[HY, HX].astype(np.float32)
            meio = np.minimum(a, b)
            claro = meio.mean(axis=2, keepdims=True) > 40          # pixel claro nos dois (texto sobre texto): vira fundo
            meio = np.where(claro, np.array([5, 8, 22], np.float32), meio)
            if n < 3:                          # o antigo sai
                u = (n + 1) / 3
                band = a * (1 - u) + meio * u
            else:                              # o novo entra
                u = (n - 2) / (DISS - 2)
                band = meio * (1 - u) + b * u
            img[HY, HX] = (band + 0.5).astype(np.uint8)
        for p in s.encode(av.VideoFrame.from_ndarray(img, format="rgb24")):
            out.mux(p)
        n += 1
        last = img
    ultimo = last
    marcas.append((nome, cap, round(t / 15, 1), round(n / 15, 1)))
    t += n
    c.close()
for p in s.encode():
    out.mux(p)
out.close()
caps = []
for nome, cap, t0, _ in marcas:
    mm, ss = divmod(int(t0), 60)
    caps.append(f"{mm}:{ss:02d} {cap or 'ABERTURA'}")
(U / "renders" / "capitulos_v3.txt").write_text("\n".join(caps) + "\n", encoding="utf-8")
print(json.dumps({"saida": str(saida), "quadros": t, "duracao_s": round(t / 15, 1), "partes": marcas}, ensure_ascii=False))
