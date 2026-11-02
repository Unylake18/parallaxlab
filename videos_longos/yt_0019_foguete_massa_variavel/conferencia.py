"""yt_0019 v6 — R0: conferência visual antes × depois dos 70 pontos (v5 × v6) + pranchas extras.
Para cada ponto: quadro do v5 e do v6 no MESMO tempo, lado a lado, 960×540 cada. Saídas em renders/v6/:
  r0/NN_<tempo>.png (par v3|v4), r0_folha_K.png (12 pares por folha), extra_fantasma.png, extra_balanco.png, extra_tsiolkovsky.png, extra_dicas_3x.png,
  prancha_<bloco>.png (15 quadros por bloco, direto dos lotes v4).  uso: python conferencia.py"""
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
OUT = U / "renders" / "v6"
(OUT / "r0").mkdir(parents=True, exist_ok=True)
mm = lambda s: int(s.split(":")[0]) * 60 + int(s.split(":")[1])
PONTOS = [(1, "1:20"), (2, "1:18"), (3, "1:34"), (4, "1:51"), (5, "2:12"), (6, "2:20"), (7, "2:27"), (8, "2:39"), (9, "3:00"), (10, "3:25"), (11, "3:33"), (12, "3:50"), (13, "4:12"), (14, "4:20"), (15, "4:30"), (16, "5:10"), (17, "5:15"), (18, "5:35"), (19, "5:48"), (20, "6:13"), (21, "6:48"), (22, "7:00"), (23, "7:12"), (24, "7:18"), (25, "7:50"), (26, "8:03"), (27, "8:39"), (28, "8:45"), (29, "8:46"), (30, "8:51"), (31, "9:06"), (32, "9:24"), (33, "10:00"), (34, "10:40"), (35, "11:20"), (36, "11:15"), (37, "11:24"), (38, "11:50"), (39, "11:55"), (40, "12:15"), (41, "12:40"), (42, "12:46"), (43, "12:57"), (44, "13:30"), (45, "13:00"), (46, "13:45"), (47, "14:20"), (48, "14:35"), (49, "15:30"), (50, "15:20"), (51, "15:32"), (52, "15:42"), (53, "16:00"), (54, "16:10"), (55, "16:15"), (56, "16:30"), (57, "16:51"), (58, "17:00"), (59, "17:20"), (60, "17:42"), (61, "17:50"), (62, "18:40"), (63, "18:03"), (64, "18:12"), (65, "18:24"), (66, "18:33"), (67, "19:10"), (68, "19:00"), (69, "20:10"), (70, "20:46")]
FPS = 15
EXTRA = {"extra_balanco": [309 + k * 3.5 for k in range(12)], "extra_tsiolkovsky": [453 + k * 3.8 for k in range(12)], "extra_p0": [912 + k * 5.5 for k in range(6)]}
DICAS = ["3:12", "14:45", "17:33", "19:50"]
FADES = [("#2", "1:18"), ("#4", "1:51"), ("#5", "2:12"), ("#11", "3:33"), ("#27", "8:39"), ("#56", "16:30")]
COR = ["0:20", "2:30", "5:00", "9:00", "11:20", "13:00", "16:30", "18:30", "20:20"]
alvo = {int(mm(t) * FPS): [] for _, t in PONTOS}
for t in DICAS:
    alvo[int(mm(t) * FPS)] = []
for ts in EXTRA.values():
    for t in ts:
        alvo[int(t * FPS)] = []


for t_ in COR:
    alvo[int(mm(t_) * FPS)] = []
for _, t_ in FADES:
    for dq in (0, 5, 10):                        # t, t + 0,33 s, t + 0,67 s
        alvo[int(mm(t_) * FPS) + dq] = []


def pega(arq):
    c = av.open(str(arq))
    out, mx = {}, max(alvo)
    for i, fr in enumerate(c.decode(video=0)):
        if i in alvo:
            out[i] = fr.to_image()
        if i >= mx:
            break
    return out


a = pega(U / "renders" / "preview_yt0019_v5_960x540.mp4")
b = pega(U / "renders" / "preview_yt0019_v6_960x540.mp4")
W, H = 480, 270
folhas = {}
for n, t in PONTOS:
    q = int(mm(t) * FPS)
    par = Image.new("RGB", (1920, 540))
    par.paste(a[q], (0, 0))
    par.paste(b[q], (960, 0))
    par.save(OUT / "r0" / f"{str(n).zfill(2)}_{t.replace(':', 'm')}.png")
    k = len(folhas.get(0, [])) // 12
    folhas.setdefault(k, []).append((n, t, q))
folhas = {}
for idx, (n, t) in enumerate(PONTOS):
    folhas.setdefault(idx // 12, []).append((n, t, int(mm(t) * FPS)))
for k, itens in folhas.items():
    L = (len(itens) + 1) // 2
    fo = Image.new("RGB", (2 * (2 * W + 10), (H + 22) * L), "black")
    d = ImageDraw.Draw(fo)
    for j, (n, t, q) in enumerate(itens):
        x, y = (j % 2) * (2 * W + 10), (j // 2) * (H + 22)
        d.text((x + 4, y + 5), f"#{n} · {t}   (v5 ← → v6)", fill="yellow")
        fo.paste(a[q].resize((W, H)), (x, y + 22))
        fo.paste(b[q].resize((W, H)), (x + W, y + 22))
    fo.save(OUT / f"r0_folha_{k + 1}.png")
for nome, ts in EXTRA.items():
    ims = [b[int(t * FPS)].resize((640, 360)) for t in ts]
    C = 3
    L = (len(ims) + C - 1) // C
    fo = Image.new("RGB", (640 * C, 360 * L), "black")
    for j, im in enumerate(ims):
        fo.paste(im, ((j % C) * 640, (j // C) * 360))
    fo.save(OUT / f"{nome}.png")
fo3 = Image.new("RGB", (3 * 640, 360 * len(FADES)), "black")
for j, (n_, t_) in enumerate(FADES):
    for k_, dq in enumerate((0, 5, 10)):
        fo3.paste(b[int(mm(t_) * FPS) + dq].resize((640, 360)), (640 * k_, 360 * j))
fo3.save(OUT / "extra_fades.png")
fo2 = Image.new("RGB", (2 * 640, 360 * len(COR)), "black")
for j, t in enumerate(COR):
    fo2.paste(a[int(mm(t) * FPS)].resize((640, 360)), (0, 360 * j))
    fo2.paste(b[int(mm(t) * FPS)].resize((640, 360)), (640, 360 * j))
fo2.save(OUT / "extra_cor.png")
fo = Image.new("RGB", (1920, 220 * len(DICAS)), "black")
for j, t in enumerate(DICAS):
    im = b[int(mm(t) * FPS)]
    caixa = (480, 60, 960, 540)
    fo.paste(im.crop((500, 280 if j != 3 else 330, 960, 460)).resize((1380, 540)).crop((0, 0, 1380, 220)), (0, 220 * j))
fo.save(OUT / "extra_dicas_3x.png")


# ── pranchas por bloco ──
BLOCOS = {"PH": ("H1", "A3"), "PA": ("A1", "A3"), "PT1": ("T1-1", "T1-5"), "PT2": ("T2-1", "T2-7"), "PT3": ("T3-1", "T3-8"), "PT4": ("T4-1", "T4-4"),
          "PE1": ("E1-1", "E1-4"), "PE2": ("E2-1", "E2-6"), "PE3": ("E3-1", "E3-5"), "PS-EN": ("S1", "EN2")}
LOTE_DO = {"PH": "PH", "PA": "PH", "PT1": "PT1", "PT2": "PT2", "PT3": "PT3", "PT4": "PT4", "PE1": "PE1", "PE2": "PE2", "PE3": "PE3", "PS-EN": "PS"}


def ancoras(lote):
    log = (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log)]
    return {k: (t0, t1) for (k, t0), (_, t1) in zip(an, an[1:])}


def quadros(lote, idx):
    c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
    al, out = set(idx), {}
    for i, fr in enumerate(c.decode(video=0)):
        if i in al:
            out[i] = fr.to_image()
        if i > max(al):
            break
    return out


def prancha(itens, saida, C=3, Wp=640, Hp=360):
    L = (len(itens) + C - 1) // C
    pr = Image.new("RGB", (Wp * C, (Hp + 20) * L), "black")
    dd = ImageDraw.Draw(pr)
    for k, (rot_, im) in enumerate(itens):
        x, y = (k % C) * Wp, (k // C) * (Hp + 20)
        pr.paste(im.resize((Wp, Hp)), (x, y + 20))
        dd.text((x + 4, y + 4), rot_, fill="yellow")
    pr.save(saida)


for bloco, (a0, a1) in BLOCOS.items():
    lote = LOTE_DO[bloco]
    an = ancoras(lote)
    t0, t1 = an[a0][0], an[a1][1]
    idx = [int((t0 + (t1 - t0) * k / 14) * 15) for k in range(15)]
    ims = quadros(lote, idx)
    prancha([(f"{bloco} q{i} {i / 15:.1f}s", ims[i]) for i in idx if i in ims], OUT / f"prancha_{bloco}.png")
print("ok", len(PONTOS))
