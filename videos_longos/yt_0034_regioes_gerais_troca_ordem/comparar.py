"""yt_0034 (copiado do yt_0032) · prancha render × alvo. Lê as marcas `[marca] NN t` dos logs (instante do estado final de cada alvo, em s do lote), tira o quadro do
vídeo do lote (ou do preview inteiro, com o deslocamento de cada lote) e monta uma linha por alvo: render à esquerda, alvo à direita.
uso: python comparar.py [LOTE ...]            → renders/v1/qa/cmp_<LOTE>.jpg (iteração)
     python comparar.py --tudo                → renders/v1/qa/comparacao_v1.jpg (26 alvos, a partir do preview concatenado)"""
import json
import re
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
import os
RODADA = os.environ.get("RODADA", "v1")
REF = AQUI / "referencia"
QA = AQUI / "renders" / RODADA / "qa"
FORA = {"04", "05", "17", "18", "20", "22", "23", "25", "26"} if RODADA == "v2" else set()     # v2: substituídos pelos alvos v2
if RODADA in ("v3", "final540"):       # v3 e final: alvos de conteúdo que o handoff v3 substitui (contas inteiras, sino refeito, H1 sem repetir o resultado, gancho novo)
    FORA = {"04", "05", "17", "18", "20", "22", "23", "25", "26", "01", "06", "10", "12", "14", "15", "16", "19", "21",
            "v2_02", "v2_06", "v2_09", "v2_10", "v2_14"}
V3 = {"v3_01b": "v3_01", "v3_02b": "v3_02"}                   # B4-2: o estado final de cada faca ao lado do alvo da abertura (§9.2)
LOTES = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PB8", "PS"]
FONTE = ImageFont.truetype(str(AQUI.parents[1] / "assets" / "fonts" / "space_grotesk" / "SpaceGrotesk-Bold.ttf"), 26)


def marcas(lote):
    log = AQUI / f"log_{lote}.txt"
    if not log.exists():
        return []
    return [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[marca\] (\S+) ([\d.]+)", log.read_text(encoding="utf-8", errors="ignore"))]


def duracao(lote):
    m = re.findall(r"\[tempo\] total ([\d.]+)s", (AQUI / f"log_{lote}.txt").read_text(encoding="utf-8", errors="ignore"))
    return float(m[-1])


def quadro(mp4, t):
    with av.open(str(mp4)) as c:
        s = c.streams.video[0]
        fps = float(s.average_rate)
        alvo = int(round(t * fps))
        for i, fr in enumerate(c.decode(s)):
            if i >= alvo:
                return fr.to_image()
        return fr.to_image()


def alvo_img(nn):
    nn = V3.get(nn, nn)
    if nn.startswith("v3_"):
        a = sorted((AQUI / "referencia_v3").glob(f"{nn}_*.jpg"))
    else:
        a = sorted((AQUI / "referencia_v2").glob(f"{nn}_*.jpg")) if nn.startswith("v2_") else sorted(REF.glob(f"{nn}_*.jpg"))
    return Image.open(a[0]).convert("RGB") if a else Image.new("RGB", (1920, 1080))


def prancha(linhas, saida, w=960):
    h = w * 9 // 16
    img = Image.new("RGB", (2 * w + 30, len(linhas) * (h + 44) + 10), (12, 10, 30))
    d = ImageDraw.Draw(img)
    for k, (nn, rq, rot) in enumerate(linhas):
        y = 10 + k * (h + 44)
        d.text((10, y), rot, font=FONTE, fill=(240, 240, 255))
        img.paste(rq.resize((w, h)), (10, y + 34))
        img.paste(alvo_img(nn).resize((w, h)), (w + 20, y + 34))
    img.save(saida, quality=88)
    print(saida, len(linhas), "linhas")


if __name__ == "__main__":
    QA.mkdir(parents=True, exist_ok=True)
    if "--tudo" in sys.argv:
        mp4 = AQUI / "renders" / RODADA / f"yt_0034_preview_{RODADA}_540p15.mp4"
        off, linhas, tab = 0.0, [], []
        for L in LOTES:
            for nn, t in marcas(L):
                if nn in FORA:
                    off += 0
                    continue
                tg = off + t - 1 / 15
                linhas.append((nn, quadro(mp4, tg), f"{nn} · {L} · render {int(tg // 60)}:{tg % 60:05.2f}  |  alvo"))
                tab.append({"alvo": nn, "lote": L, "t_lote": t, "t_video": round(tg, 3)})
            off += duracao(L)
        linhas.sort(key=lambda r: (0 if r[0].startswith("v3_") else (2 if r[0].startswith("v2_") else 1), r[0]))
        prancha(linhas, QA / f"comparacao_{RODADA}.jpg")
        (QA / f"marcas_{RODADA}.json").write_text(json.dumps(tab, indent=1), encoding="utf-8")
    else:
        for L in sys.argv[1:]:
            mp4 = AQUI / f"media_{L}" / "videos" / "cena" / "540p15" / f"{L}.mp4"
            linhas = [(nn, quadro(mp4, t - 1 / 15), f"{nn} · {L} · t = {t:.2f} s  |  alvo") for nn, t in marcas(L)]
            prancha(linhas, QA / f"cmp_{L}.jpg")
