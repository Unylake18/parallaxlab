"""yt_0045 final: renders/final/qa/correcoes_final.jpg · antes (preview v2) × depois (final) das correções R1–R8 (stills 1080p reduzidos a 50 %; R5/R8 a partir dos MP4 de 540p)."""
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
QA = U / "renders" / "final" / "qa"
A, D = QA / "antes_v2", QA / "comparacao" / "stills"


def quadro(mp4, t):
    c = av.open(str(mp4))
    s = c.streams.video[0]
    c.seek(int(t / s.time_base), stream=s)
    for fr in c.decode(video=0):
        if fr.time >= t - 1e-3:
            return fr.to_image().resize((960, 540))
    return Image.new("RGB", (960, 540))


def par(nome, rot):
    return (Image.open(A / nome).convert("RGB").resize((960, 540)), Image.open(D / nome).convert("RGB").resize((960, 540)), rot)


MV2 = U / "renders" / "v2" / "yt_0045_preview_v2_540p15.mp4"
MF = U / "renders" / "final" / "yt_0045_preview_final_540p15.mp4"
LIN = [par("01_H1_helice_lata.png", "R1 (conta e seta F na 2ª volta) · R2 (eixo z atrás da frente) · H1"),
       par("14_B7-1_helice_montando.png", "R2 · R3 (2 setas curtas) · R4 (sem a 2ª volta) · B7-1"),
       par("16_B7-3_lendo_resposta.png", "R2 · R4 (2ª volta só no B7-3, laranja apagado) · B7-3"),
       par("09_B4-3_no_raio.png", "R6 (setas só até t = 1,5; ponta de sentido entre a última seta e o círculo) · B4-3"),
       par("12_B6-1_outra_notacao.png", "R7 (placa a 48 px do último dt) · B6-1"),
       (quadro(MV2, 1.0), quadro(MF, 1.0), "R5 (a lata entra na 1ª palavra: palco do H1 em t = 1,0 s)"),
       (quadro(MV2, 0.0), quadro(MF, 0.0), "R8 (canto inteiro no quadro 0, sem escrita)")]
im = Image.new("RGB", (1920, 40 + len(LIN) * 580), (16, 14, 40))
d = ImageDraw.Draw(im)
d.text((12, 10), "yt_0045 · correções R1–R8: ANTES (preview v2, esquerda) × DEPOIS (final, direita)", fill=(240, 240, 240))
for i, (a, b, r) in enumerate(LIN):
    y = 40 + i * 580
    d.text((12, y + 4), r, fill=(255, 200, 120))
    im.paste(a, (0, y + 24))
    im.paste(b, (960, y + 24))
im.save(QA / "correcoes_final.jpg", quality=90)
print("ok", im.size)
