"""yt_0030 · handoff final §6 (C4): a linha 2 do canto nunca some por mais de 0,6 s fora de H e do cartão/CTA → qa/canto.txt.
Varre o vídeo emendado quadro a quadro: a linha 2 (branca #F5F7FF, negrito, baseline em 118 px a 1080p, x ≥ 36 px) está presente quando a faixa
dela tem pixels claros (luminância > 200) acima de um mínimo. Lista cada ausência > 0,6 s com o instante, a âncora e se cai em H/A (antes da
1ª seção) ou no fim do resumo (cartão/CTA).
uso: python qa_canto.py VIDEO.mp4 [fps]"""
import json
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
V = Path(sys.argv[1])
FPS = int(sys.argv[2]) if len(sys.argv) > 2 else 15
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
ANC, ordem = A["ancoras"], A["ordem"]


def ancora(t):
    a = ordem[0]
    for x in ordem:
        if ANC[x]["ini"] <= t:
            a = x
    return a


LIM = 140                    # "some" = abaixo de ~50 % de opacidade: #F5F7FF a 50 % sobre o violeta dá luminância ≈ 140
c = av.open(str(V))
pres = []
for fr in c.decode(video=0):
    im = fr.to_ndarray(format="gray")
    h, w = im.shape
    k = h / 1080
    faixa = im[int(92 * k):int(134 * k), int(30 * k):int(1240 * k)]
    pres.append(int((faixa > LIM).sum()))
c.close()
pres = np.array(pres)
k2 = round((int(sys.argv[3]) if len(sys.argv) > 3 else 40) * (h / 540) ** 2)        # 40 px claros a 540p (a área escala com o quadrado)
on = pres >= k2
corridas, i = [], 0
while i < len(on):
    if not on[i]:
        j = i
        while j < len(on) and not on[j]:
            j += 1
        corridas.append((i, j))
        i = j
    else:
        i += 1
t_d1 = ANC["D1-1"]["ini"]
t_cta = ANC["S-2"]["ini"]                   # cartão do próximo vídeo (S-2) e CTA (S-3)
L = [f"yt_0030 · canto (C4): ausências da linha 2 > 0,6 s em {V.name} ({len(on)} quadros, {FPS} fps; presente = ≥ {k2} px com luminância > {LIM} na faixa, i.e. linha 2 com ≥ ~50 % de opacidade)", ""]
fora = 0
for i, j in corridas:
    d = (j - i) / FPS
    if d <= 0.6:
        continue
    t0 = i / FPS
    exc = "H/A (antes da 1ª seção)" if t0 + d <= t_d1 + 0.6 else ("cartão/CTA (S-2/S-3)" if t0 >= t_cta else "")
    if not exc:
        fora += 1
    L.append(f"  {int(t0) // 60}:{t0 % 60:05.2f} – {(j / FPS) // 60:.0f}:{(j / FPS) % 60:05.2f} ({d:.2f} s) âncora {ancora(t0)} "
             + (f"· exceção permitida: {exc}" if exc else "· FORA DA META"))
curtas = [(j - i) / FPS for i, j in corridas if (j - i) / FPS <= 0.6]
L += ["", f"ausências curtas (≤ 0,6 s, trocas de seção): {len(curtas)}" + (f", até {max(curtas):.2f} s" if curtas else ""),
      f"resumo: ausências > 0,6 s fora das exceções: {fora} → {'OK' if fora == 0 else 'FALHA'}"]
(U / "qa").mkdir(exist_ok=True)
(U / "qa" / f"canto_{V.stem}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
