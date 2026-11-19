"""yt_0032 final §3/§7: um still por correção C1–C18 no gatilho (tirado do vídeo 540p do lote, que já tem o 3D) e a prancha
correcoes_final.jpg (quadro do erro do v2, em referencia_final/, ao lado do quadro corrigido).
uso: python stills_final.py [pasta_dos_videos]   (padrão: media_<LOTE>/videos/cena/540p15/<LOTE>.mp4)
Saídas: renders/final/stills/Cxx.png, renders/final/correcoes_final.jpg, renders/final/stills.txt (lote, âncora, t do lote, gatilho)."""
import re
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
OUT = U / "renders" / "final"
(OUT / "stills").mkdir(parents=True, exist_ok=True)
VID = Path(sys.argv[1]) if len(sys.argv) > 1 else None

# (id, lote, gatilho: frase do [gatilho] ou "gm:<nota>", deslocamento em s, referência do v2, o que prova)
ITENS = [
    ("C01", "PB1", "independentemente dos pontos", 1.9, "C01_b11_grade_parada", "grade 8×8 nascida no lugar + 64 pontos que pulam"),
    ("C02", "PB1", "a camada dá quatro", 4.2, "C02_b14_153_sem_origem", "ÁREA 4 m² e ÁREA ≈1,53 m² presos às peças; 4 e 1,53 voam"),
    ("C03", "PB2", "e um eme maiúsculo", 1.0, "C03_b22_m_M_soltos", "m=1 e M=3 nas lajes, pares acesos na mesma cor"),
    ("C04", "PB3", "chega a nove vírgula", 3.6, "C04_b32_cota_sem_conta", "cota = 100·área; 100·0,093 → 9,3 (mapa 14)"),
    ("C05", "PB3", "a linha da solda", 2.4, "C05_b33_L_no_zoom", "solda percorrida em laranja; L ≈ 2,25 m sobre ela"),
    ("C06", "PB6", "a um vírgula sessenta", 4.0, "C06_b61_raio_163", "r² = 8/3 → r = √(8/3) ≈ 1,63 (mapa 15) + segmento r no 3D"),
    ("C07", "PB6", "dividindo pela área a", 3.2, "C07_b63_min_max", "m = f(0,0) = 0 e M = f(2,2) = 8 voam para a fórmula; ÷α encostado"),
    ("C08a", "PH", "densidade média da chapa", 4.2, "C08a_h1_media", "MÉDIA = 7,06/4 ≈ 1,76 kg/m² (7,06 voa da soma)"),
    ("C08b", "PB6", "dá para colocar um", -0.1, "C08b_b64_media", "7,06/4 ≈ 1,76 e (1+3)/2 = 2, áreas iguais"),
    ("C09", "PB7", "pelo vertical zero", 2.8, "C09_b71_eixos", "eixo x: 1, eixo y: 0, com conta; os valores voam para o disco"),
    ("C10", "PB7", "que é a área", 4.0, "C10_b72_soma_1", "soma = 1 (mapa 16) e ∬1 = área = π·1² = π (mapa 17)"),
    ("C11", "PS", "gm:mapa 13", 0.1, "C11_s2_area_leve", "ÁREA LEVE: região abaixo da solda acesa em CI"),
    ("C12", "PB3", "uma curva sem espessura", 2.4, "C12_b31_B_e_solda", "S preso na solda; ∬_S"),
    ("C13", "PB4", "o valor da integral", -0.1, "C13_b42_disco_f", "função com furo na origem; ∬_disco x²/(x²+y²); no furo = …"),
    ("C14", "PB5", "a chapa tem quatro", -0.1, "C14_b52_faixa", "faixa de 0,2 m de altura com cota vertical"),
    ("C15", "PB6", "e a função é contínua", -0.1, "C15_b62_caminho", "dois pontos e um caminho contínuo dentro de B"),
    ("C16", "PS", "e o teorema do", -0.1, "C16_s1_lista", "sete propriedades, uma por linha, romanos em CI"),
    ("C17", "PS", "dá para achar a", -0.1, "C17_s2_riscos", "grade 16×16 refinada só com linhas novas no lugar"),
    ("C18a", "PH", "o pedaço leve tem", -0.1, "C18a_h1_quebra", "chapa acima da balança; pedaços descem para os pratos"),
    ("C18b", "PS", "grades cada vez mais", -0.2, "C18b_s2_canto", "canto O PRÓXIMO PASSO no S2"),
    ("C19", "PB3", "e conforme a largura", -0.1, "C05_b33_L_no_zoom", "cordão de 1 mm: 135 g → 13,5 g (0,0135 kg)"),
]


def t_lote(lote, chave, dt):
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
    pares.append((cid, Image.open(U / "referencia_final" / f"{ref}.jpg").convert("RGB"), im, prova))
(OUT / "stills.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")

COLS = 2
rows = (len(pares) + COLS - 1) // COLS
P = Image.new("RGB", (COLS * (2 * W + 24) + 24, rows * (H + CAB + 18) + 70), (22, 18, 34))
d = ImageDraw.Draw(P)
d.text((24, 18), "yt_0032 · correções finais C1–C18 · esquerda: v2 (referencia_final) · direita: corrigido (540p, no gatilho)", font=FT, fill=(240, 240, 240))
for k, (cid, a, b, prova) in enumerate(pares):
    x0 = 24 + (k % COLS) * (2 * W + 24)
    y0 = 70 + (k // COLS) * (H + CAB + 18)
    d.text((x0, y0 + 4), cid, font=FT, fill=(255, 196, 92))
    d.text((x0 + 70, y0 + 8), prova[:95], font=FS, fill=(220, 220, 220))
    for j, im in enumerate((a, b)):
        im = im.copy()
        im.thumbnail((W, H))
        P.paste(im, (x0 + j * W + (W - im.width) // 2, y0 + CAB + (H - im.height) // 2))
    d.rectangle([x0 + W, y0 + CAB, x0 + W + 1, y0 + CAB + H], fill=(255, 196, 92))
P.save(OUT / "correcoes_final.jpg", quality=88)
print("\n".join(linhas))
print("prancha:", OUT / "correcoes_final.jpg", P.size)
