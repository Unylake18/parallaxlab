"""yt_0034 final §3/§7 (copiado do stills_final.py do yt_0032): um still por correção D1–D13 no gatilho (tirado do vídeo 540p do lote, que já
tem o 3D) e a prancha correcoes_final.jpg (quadro do erro do v3, em referencia_final/quadros_do_erro/, ao lado do quadro corrigido).
uso: python stills_final.py [pasta_dos_videos]   (padrão: media_<LOTE>/videos/cena/540p15/<LOTE>.mp4)
Saídas: renders/final/stills/Dxx.png, renders/final/correcoes_final.jpg, renders/final/stills.txt (lote, âncora, t do lote, gatilho)."""
import re
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
OUT = U / "renders" / "final"
(OUT / "stills").mkdir(parents=True, exist_ok=True)
VID = Path(sys.argv[1]) if len(sys.argv) > 1 else None
REF = U / "referencia_final" / "quadros_do_erro"

# (id, lote, gatilho: frase do [gatilho], "gm:<nota>" ou "t:<s do lote>", deslocamento em s, quadro do erro (prefixo) ou None, o que prova)
ITENS = [
    ("D01a", "PB3", "agora olha as fatias", 0.85, "D01a", "cunha: as faces encolhem e viram os pontos; o pouso sai junto"),
    ("D01b", "PB3", "agora olha as fatias", 2.2, "D01b", "cunha: eixos dos gráficos só depois; nenhum polígono do pouso"),
    ("D01c", "PB4", "agora desenha a", 0.85, "D01c", "sino: faces → pontos (0,2; 0,549) e (0,6; 0,419)"),
    ("D01d", "PB4", "agora desenha a", 2.6, "D01d", "sino: eixos dos gráficos limpos, só os pontos"),
    ("D02", "PB4", "zero vírgula três", 1.3, "D02", "passo 3: gráfico de A(y), régua u = y², área pintada, 0,316 voou"),
    ("D03", "PB3", "a integral de dentro", 0.6, "D03", "triângulo âmbar (alpha 0,58, borda âmbar)"),
    ("D04", "PB6", "gm:mapa D4a", 0.55, "D04", "linha a a 50 % do glyph map (sen(x³) sai; o y do dy vira [y])"),
    ("D04c", "PB6", "gm:mapa D4c", 0.55, "D04", "linha b a 50 %: x² e sen(x³) viram x² sen(x³); o − 0 fica"),
    ("D05", "PB3", "gm:mapa 6b", 0.65, "D05", "isola o x a 50 %: x² por cima, y² por baixo"),
    ("D06", "PB1", "um quarto de pi", 2.4, "D06", "π·2²/4 = π inteiro; nenhum 2 solto"),
    ("D07", "PB1", "onde ela entra no", 0.5, "D07", "nenhum rótulo minúsculo na região (R5 MINI = 0)"),
    ("D08", "PH", "dois vírgula setenta", 0.4, "D08", "e ≈ 2,718 em linha própria abaixo da integral"),
    ("D09a", "PS", "virar um retângulo", -1.0, "D09", "1 s antes: a vaga do 3º painel vazia"),
    ("D09b", "PS", "virar um retângulo", 1.0, "D09", "1 s depois: o painel inteiro"),
    ("D10a", "PB3", "a fatia vai de", 0.0, "D10", "cunha em pé: opaca 0 ≤ x ≤ 1, x > 1 em traço"),
    ("D10b", "PB3", "a altura é ípsilon", 1.2, "D10", "cunha deitada: opaca y ≥ 1, y < 1 em traço"),
    ("D11", "PH", "t:4.0", 0.0, "D11", "abertura: topo da peça ≥ 40 px abaixo do canto"),
    ("D12", "PB4", "a diagonal", 0.9, None, "B4-1: y = x voou em «a diagonal»"),
    ("D13", "PH", "de é elevado a", 1.6, None, "H1: o ponto percorre o sino com a altura pontilhada"),
]


def t_lote(lote, chave, dt):
    if chave.startswith("t:"):
        return "-", float(chave[2:]) + dt
    log = (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")
    ini = {m.group(1): float(m.group(2)) for m in re.finditer(r"^\[ancora\] (\S+) ([0-9.]+)", log, re.M)}
    if chave.startswith("gm:"):
        m = re.search(rf"^\[gm\] {lote} (\S+) ([0-9.]+) .*{re.escape(chave[3:])}", log, re.M)
    else:
        m = re.search(rf"^\[gatilho\] (\S+)\s+([0-9.]+)s .*{re.escape(chave)}", log, re.M)
    assert m, (lote, chave)
    aid, t = m.group(1), float(m.group(2))
    return aid, (t if chave.startswith("gm:") else ini[aid] + t) + dt      # [gm] traz o t do lote; [gatilho], o t da âncora


def quadro(lote, t):
    f = (VID / f"{lote}.mp4") if VID else U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"
    c = av.open(str(f))
    s = c.streams.video[0]
    alvo = int(round(t * float(s.average_rate)))
    for k, fr in enumerate(c.decode(s)):
        if k >= alvo:
            im = fr.to_image()
            c.close()
            return im
    raise RuntimeError((lote, t))


try:
    FT = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
    FS = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18)
except OSError:
    FT = FS = ImageFont.load_default()
W, H, CAB = 640, 360, 56
linhas, pares = [], []
for cid, lote, ch, dt, ref, prova in ITENS:
    aid, t = t_lote(lote, ch, dt)
    im = quadro(lote, t)
    p = OUT / "stills" / f"{cid}.png"
    im.save(p)
    linhas.append(f"{cid}\t{lote}\t{aid}\tt={t:7.2f}s\t«{ch}»{dt:+.2f}\t{p.relative_to(U)}\t{prova}")
    ri = next(iter(sorted(REF.glob(f"{ref}_*.jpg"))), None) if ref else None
    a = Image.open(ri).convert("RGB") if ri else Image.new("RGB", (960, 540), (40, 34, 56))
    if not ri:
        ImageDraw.Draw(a).text((380, 255), "(sem quadro do erro)", font=FT, fill=(200, 200, 200))
    pares.append((cid, a, im, prova))
(OUT / "stills.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")

COLS = 2
rows = (len(pares) + COLS - 1) // COLS
P = Image.new("RGB", (COLS * (2 * W + 24) + 24, rows * (H + CAB + 18) + 70), (22, 18, 34))
d = ImageDraw.Draw(P)
d.text((24, 18), "yt_0034 · correções finais D1–D13 · esquerda: v3 (quadro do erro) · direita: corrigido (540p com a voz, no gatilho)", font=FT, fill=(240, 240, 240))
for k, (cid, a, b, prova) in enumerate(pares):
    x0 = 24 + (k % COLS) * (2 * W + 24)
    y0 = 70 + (k // COLS) * (H + CAB + 18)
    d.text((x0, y0 + 4), cid, font=FT, fill=(255, 196, 92))
    d.text((x0 + 80, y0 + 8), prova[:95], font=FS, fill=(220, 220, 220))
    for j, im in enumerate((a, b)):
        im = im.copy()
        im.thumbnail((W, H))
        P.paste(im, (x0 + j * W + (W - im.width) // 2, y0 + CAB + (H - im.height) // 2))
    d.rectangle([x0 + W, y0 + CAB, x0 + W + 1, y0 + CAB + H], fill=(255, 196, 92))
P.save(OUT / "correcoes_final.jpg", quality=88)
print("\n".join(linhas))
