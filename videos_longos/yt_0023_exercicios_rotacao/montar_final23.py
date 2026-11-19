"""yt_0023 FINAL 1920×1080 / 30 fps: emenda os 7 lotes (media_F_<lote>/videos/cena/1080p30/<lote>.mp4) → renders/master_mudo_yt0023_<rodada>_1920x1080.mp4 (H.264 yuv420p CRF 14, sem áudio).
Alguns lotes (PE1a, PE1b, PE4) começam com um pré-roll (objetos acendendo) ANTES da primeira âncora; esse trecho cai sobre o fim do lote anterior (a âncora é absoluta na voz),
então é DISSOLVIDO sobre a cauda do anterior (sem somar tempo). Lotes sem pré-roll: o anterior apaga até o fundo em SAI quadros e o novo acende em SAI, como no preview.
A duração total fica igual à da voz. Grava capitulos_<rodada>.txt (tempos das âncoras na voz).
uso: python montar_final23.py [rodada]"""
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

import av
import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
M = lambda c: U / f"media_F_{c}/videos/cena/1080p30/{c}.mp4"
RODADA = sys.argv[1] if len(sys.argv) > 1 else "final"
FPS, SAI = 30, 10
LOTES = ["PH", "PE1a", "PE1b", "PE2", "PE3", "PE4", "PS"]
CAPS = [("H1", "QUAL BLOCO DESCE?"), ("A3", "CAIXA DE FERRAMENTAS"), ("D1", "O DESAFIO DA RÉGUA"), ("E1-1", "EXERCÍCIO 1: O VOLANTE"), ("E2-1", "EXERCÍCIO 2: A HASTE E O EIXO"),
        ("E3-1", "EXERCÍCIO 3: O CARRETEL"), ("E4-1", "EXERCÍCIO 4: O PÊNDULO MAIS RÁPIDO"), ("S1", "RESUMO"), ("EN1", "ENCERRAMENTO E DESAFIO")]
FUNDO = np.asarray(Image.open(U / "fundo_grad.png").convert("RGB").resize((1920, 1080)), dtype=np.float32)
anc = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]


TRECHO = {"PE4": (8486, U / "media_F_PE4_t/videos/cena/1080p30/PE4.mp4")}     # v9: o fim de PE4 (E4-10) foi re-renderizado: quadros [0, 8486) do lote + o trecho novo


def quadros_lote(l):
    c = av.open(str(M(l)))
    if l not in TRECHO:
        n = c.streams.video[0].frames
        return n, (f for f in c.decode(video=0)), c
    q0, novo = TRECHO[l]
    c2 = av.open(str(novo))
    n = q0 + c2.streams.video[0].frames

    def gen():
        for k, f in enumerate(c.decode(video=0)):
            if k >= q0:
                break
            yield f
        yield from c2.decode(video=0)
    return n, gen(), c


def pre_roll(l):
    log = (U / f"log_F_{l}.txt").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\[ancora\] (\S+) ([0-9.]+)", log)
    return int(round(float(m.group(2)) * FPS))


def mistura(a, b, w):
    return (a.astype(np.float32) * (1 - w) + b.astype(np.float32) * w + 0.5).astype(np.uint8)


def fundo_w(img, w):
    return (img.astype(np.float32) * w + FUNDO * (1 - w) + 0.5).astype(np.uint8)


saida = U / "renders" / f"master_mudo_yt0023_{RODADA}_1920x1080.mp4"
out = av.open(str(saida), "w")
s = out.add_stream("libx264", rate=Fraction(FPS))
s.width, s.height, s.pix_fmt = 1920, 1080, "yuv420p"
s.options = {"crf": "14", "preset": "medium"}
total = 0
escreve = lambda img: [out.mux(pk) for pk in s.encode(av.VideoFrame.from_ndarray(img, format="rgb24"))]
cauda = []                                   # quadros retidos do lote anterior (sem escrever) para a dissolução
for k, l in enumerate(LOTES):
    n_tot, frames_, c = quadros_lote(l)
    pre = pre_roll(l) if k > 0 else 0
    ultimo = k == len(LOTES) - 1
    reter = 0 if ultimo else pre_roll(LOTES[k + 1])      # quantos quadros do FIM deste lote ficam retidos para o próximo
    n = 0
    novos_cauda = []
    for fr in frames_:
        img = fr.to_ndarray(format="rgb24")
        if k > 0 and pre > 0 and n < pre:
            img = mistura(cauda[n], img, (n + 1) / (pre + 1))            # dissolve o pré-roll sobre a cauda do lote anterior
        elif k > 0 and pre == 0 and n < SAI:
            img = fundo_w(img, (n + 1) / (SAI + 1))
        if not ultimo and reter == 0 and n >= n_tot - SAI:
            img = fundo_w(img, (n_tot - n) / (SAI + 1))
        if reter > 0 and n >= n_tot - reter:
            novos_cauda.append(img)
        else:
            escreve(img)
            total += 1
        n += 1
    c.close()
    cauda = novos_cauda
    print(l, n_tot, "pre", pre, "retidos", len(novos_cauda), "total", total, flush=True)
for pk in s.encode():
    out.mux(pk)
out.close()
caps = [f"{int(anc[a]['ini']) // 60}:{int(anc[a]['ini']) % 60:02d} {cap}" for a, cap in CAPS]
(U / "renders" / f"capitulos_{RODADA}.txt").write_text("\n".join(caps) + "\n", encoding="utf-8")
print(json.dumps({"saida": str(saida), "quadros": total, "duracao_s": round(total / FPS, 2), "capitulos": caps}, ensure_ascii=False))
