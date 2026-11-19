"""yt_0030 · QA §8.1: render × alvo dos 29 quadros-alvo (960×540 cada; alvo à esquerda, render à direita) → renders/<rodada>/qa/comparacao_<rodada>.jpg e .txt
(tempo do quadro no lote e no preview emendado; deslocamento global por correlação de fase das bordas, px a 1080p; diferença média).
O instante de cada alvo vem do log do lote ([ancora] / [gatilho]), não do orçamento: a cena pode ter se esticado.
uso: python comparar.py [rodada]"""
import json
import re
import sys
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
RODADA = sys.argv[1] if len(sys.argv) > 1 else "v1"
OUT = U / "renders" / RODADA / "qa"
OUT.mkdir(parents=True, exist_ok=True)

ALVO = {1: ("PH", "anc", "A-1", 2.0), 2: ("PH", "anc", "A-1", 49.0), 3: ("PH", "anc", "H-1", -0.5),
        4: ("PD1", "anc", "D1-3", -0.2), 5: ("PD1", "anc", "D1-4", -0.2), 6: ("PD1", "anc", "D1-6", -0.1),
        7: ("PD2", "gat", "D2-3", ("e acima da diagonal", -0.15)), 8: ("PD2", "anc", "D2-5", -0.1),
        9: ("PD3", "gat", "D3-4", ("alfa um dois menos dois", -0.15)), 10: ("PD3", "anc", "D3-5", -0.2), 11: ("PD3", "anc", "D3-6", -0.2),
        12: ("PD3", "anc", "D3-7", -0.1), 13: ("PD3B", "anc", "D3b-2", -0.2), 14: ("PD3B", "anc", "D3b-5", -0.2),
        15: ("PD4", "anc", "D4-3", -0.2), 16: ("PD4", "anc", "D4-4", -0.2), 17: ("PD4", "anc", "D4-6", -0.2), 18: ("PD4", "anc", "D4-7", -0.2),
        19: ("PD5", "anc", "D5-2", -0.2), 20: ("PD5", "anc", "D5-5", -0.2), 21: ("PD5", "anc", "D5-8", -0.2), 22: ("PD5", "anc", "D5-11", -0.2),
        23: ("PA1", "anc", "A1-5", -0.1), 24: ("PA2", "anc", "A2-4", -0.1), 25: ("PA4", "gat", "A4-3", ("o mapa múndi de mercator", -0.15)),
        26: ("PA3", "anc", "A3-3", -0.2), 27: ("PA3", "anc", "A3-6", -0.1), 28: ("PS", "anc", "S-1", -0.2), 29: ("PS", "anc", "S-2", -0.2)}
if RODADA != "v1":         # handoff v2: os 22 alvos novos (estados intermediários das contas)
    ALVO[3] = ("PH", "gat", "H-1", ("por que o campo magnético", -0.3))   # no v2 o fim do gancho já é o quadro v2_h2 (alvo 30)
    ALVO.update({30: ("PH", "anc", "H-1", -0.5), 31: ("PH", "gat", "A-1", ("pausa o vídeo e tenta", -0.3)),
                 32: ("PD1", "gat", "D1-3", ("o canto um um vai para", -0.15)), 33: ("PD1", "gat", "D1-4", ("e o círculo vira um círculo", -0.15)),
                 34: ("PD1", "anc", "D1-5", -0.2), 35: ("PD3", "gat", "D3-3", ("põe a potência com um a menos", -0.15)),
                 36: ("PD3", "gat", "D3-3", ("a distância ao quadrado aparece duas vezes", -0.15)), 37: ("PD3", "anc", "D3-3", -0.2),
                 38: ("PD3", "anc", "D3-7", -0.5), 39: ("PD3B", "gat", "D3b-1", ("no plano só sobra a terceira", -0.15)),
                 40: ("PD3B", "gat", "D3b-3", ("um rotacional nunca diverge", -0.15)), 41: ("PD3B", "gat", "D3b-5", ("o campo magnético tem divergente zero", -0.15)),
                 42: ("PD4", "anc", "D4-3", -0.2), 43: ("PD4", "gat", "D4-7", ("agora olha essa derivada", -0.15)), 44: ("PD5", "anc", "D5-3", -0.2),
                 45: ("PD5", "gat", "D5-10", ("no ponto um zero", -0.15)), 46: ("PD5", "anc", "D5-11", -0.2), 47: ("PA1", "anc", "A1-5", -0.1),
                 48: ("PA2", "anc", "A2-3", -0.2), 49: ("PA4", "gat", "A4-3", ("agora lê como transformação", -0.15)),
                 50: ("PA3", "gat", "A3-5", ("as outras parcelas são iguais", -0.15)), 51: ("PA3", "gat", "A3-5", ("no plano são duas parcelas", 1.0))})


def log(lote):
    return (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")


def ancoras(lote):
    """Início (s do lote) de cada âncora e o fim do lote."""
    L = log(lote)
    a = {m.group(1): float(m.group(2)) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", L)}
    tot = float(re.search(r"\[tempo\] total ([0-9.]+)s", L).group(1))
    return a, tot


def instante(lote, tipo, aid, arg):
    a, tot = ancoras(lote)
    ordem = sorted(a, key=a.get)
    if tipo == "gat":
        frase, d = arg
        m = re.search(r"\[gatilho\] %s +([0-9.]+)s \(alvo[^)]*\) %s" % (re.escape(aid), re.escape(frase)), log(lote))
        return a[aid] + float(m.group(1)) + d
    if arg >= 0:
        return a[aid] + arg
    k = ordem.index(aid)
    fim = a[ordem[k + 1]] if k + 1 < len(ordem) else tot - 0.4
    return fim + arg


def quadro(lote, t):
    c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
    q = round(t * 15)
    im = None
    for i, fr in enumerate(c.decode(video=0)):
        im = fr
        if i >= q:
            break
    c.close()
    return im.to_image()


def bordas(im):
    g = np.asarray(im.convert("L"), float)
    e = np.abs(np.diff(g, axis=1, prepend=g[:, :1])) + np.abs(np.diff(g, axis=0, prepend=g[:1]))
    e[:70, :] = 0
    return e - e.mean()


def deslocamento(a, b):
    A, B = np.fft.fft2(bordas(a)), np.fft.fft2(bordas(b))
    R = A * np.conj(B)
    r = np.fft.ifft2(R / (np.abs(R) + 1e-9)).real
    dy, dx = np.unravel_index(np.argmax(r), r.shape)
    h, w = r.shape
    dy, dx = (dy - h if dy > h // 2 else dy), (dx - w if dx > w // 2 else dx)
    return dx * 2, dy * 2


if __name__ == "__main__":
    ini = json.loads((U / "renders" / RODADA / f"lotes_{RODADA}.json").read_text(encoding="utf-8"))["inicio"]
    fonte = ImageFont.load_default()
    linhas, rel = [], [f"yt_0030 {RODADA} · render × alvo ({len(ALVO)} quadros; 960×540; alvo à esquerda, render à direita). Deslocamento global por correlação de "
                       f"fase das bordas (px a 1080p; tolerância ±20 px = ±10 px a 960×540); diferença média de cor (0–255)."]
    for n in sorted(ALVO):
        lote, tipo, aid, arg = ALVO[n]
        t = instante(lote, tipo, aid, arg)
        r = quadro(lote, t)
        r.save(OUT / f"render_{n:02d}.png")
        arq = next(iter(list((U / "referencia_v1").glob(f"{n:02d}_*.jpg")) + list((U / "referencia_v2").glob(f"{n:02d}_*.jpg"))))
        a = Image.open(arq).convert("RGB").resize((960, 540), Image.LANCZOS)
        dx, dy = deslocamento(r, a)
        dif = float(np.abs(np.asarray(r, float) - np.asarray(a, float)).mean())
        tabs = ini[lote] / 15 + t
        rel.append(f"{n:02d} {arq.stem:10s} lote {lote:5s} âncora {aid:6s} t = {t:7.2f} s no lote · {int(tabs) // 60}:{tabs % 60:05.2f} no preview · "
                   f"deslocamento ({dx:+d}, {dy:+d}) px · diferença {dif:4.1f}")
        lin = Image.new("RGB", (1920, 540 + 26), (5, 11, 24))
        lin.paste(a, (0, 26))
        lin.paste(r, (960, 26))
        d = ImageDraw.Draw(lin)
        d.text((8, 7), f"{n:02d} ALVO {arq.stem}", fill=(160, 220, 255), font=fonte)
        d.text((968, 7), f"RENDER {lote} {aid} t={t:.2f}s  preview {int(tabs) // 60}:{tabs % 60:05.2f}", fill=(255, 220, 90), font=fonte)
        linhas.append(lin)
    pr = Image.new("RGB", (1920, sum(l.height for l in linhas)))
    y = 0
    for l in linhas:
        pr.paste(l, (0, y))
        y += l.height
    pr.save(OUT / f"comparacao_{RODADA}.jpg", quality=88)
    (OUT / f"comparacao_{RODADA}.txt").write_text("\n".join(rel) + "\n", encoding="utf-8")
    print("\n".join(rel))
