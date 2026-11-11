"""yt_0027 final §6: lado a lado (alvo × preview com os tempos da voz) e prancha das 43 âncoras no instante da 1ª palavra.
Saídas em renders/v5/qa/: lado_NN.png (alvo à esquerda, render à direita, 960×540 cada) e ancoras_1a_palavra_K.png (grades 3×3, 960×540 por quadro).
uso: python lado_v5.py"""
import json
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
OUT = U / "renders" / "v5" / "qa"
OUT.mkdir(parents=True, exist_ok=True)
VID = U / "renders" / "preview_yt0027_v5_960x540.mp4"
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
Q = json.loads((U / "renders" / "quadros_v5.json").read_text(encoding="utf-8"))
ordem = A["ordem"]
FPS = 15
fim = {a: Q[ordem[i + 1]] for i, a in enumerate(ordem[:-1])}


def gat_q(lote, anc, frase):
    log = (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\[gatilho\] " + re.escape(anc) + r"\s+([0-9.]+)s \(alvo[^)]*\) " + re.escape(frase), log)
    return Q[anc] + round(float(m.group(1)) * FPS)


# (nº, arquivo do alvo, quadro do render, legenda)
R4, R5 = U / "referencia_v4", U / "referencia_v5"
PEDIDOS = [
    (18, R5 / "18_B1-2_lupa_seta_e_vizinha.jpg", fim["B1-2"] - 8, "B1-2 lupa: seta e vizinha, mesmo pé, ΔF, ∂F/∂x"),
    (19, R5 / "19_B3-3_mais_forte_mais_fraca.jpg", fim["B3-3"] - 8, "B3-3 mais forte × mais fraca"),
    (20, R5 / "20_B4-4_entra_e_sai_nas_quatro_paredes.jpg", fim["B4-4"] - 8, "B4-4 entra e sai nas quatro paredes"),
    (21, R5 / "21_S4_previa_proximo_video.jpg", gat_q("PS", "S4", "se essa aula te ajudou") - 3, "S4 prévia do próximo vídeo"),
    (11, R4 / "11_S4_terceira_coisa_e_gancho.jpg", gat_q("PS", "S4", "no próximo vídeo") - 3, "S4 a terceira coisa"),
    (14, R4 / "14_B1-1a_definicao_P_Q.jpg", fim["B1-1a"] - 8, "B1-1a P e Q"),
    (15, R4 / "15_B2-6_P_Q_e_vorticidade.jpg", fim["B2-6"] - 8, "B2-6 vorticidade"),
    (16, R4 / "16_B6-0_definicao_geral.jpg", fim["B6-0"] - 8, "B6-0 em qualquer dimensão"),
    (17, R4 / "17_B6-3_rot_expandido.jpg", fim["B6-3"] - 8, "B6-3 rot aberto"),
]
# quadros de prova dos itens do §2 (render)
PROVAS = {
    "item01_B1-1a": fim["B1-1a"] - 8,
    "item02_B1-2_seta_e_vizinha": gat_q("PB1", "B1-2", "que a gente chama de agá") + 12,
    "item02_B1-2_coral": gat_q("PB1", "B1-2", "essa setinha coral") + 12,
    "item03_B3-3": fim["B3-3"] - 8,
    "item04_B4-4_entra_esquerda": gat_q("PB4", "B4-4", "pela da esquerda") + 15,
    "item04_B4-4_entra_embaixo": fim["B4-4"] - 8,
    "item05_B5-2_area_nao_muda": gat_q("PB5", "B5-2", "a área não muda") + 12,
    "item05_B5-2_div0_por_ultimo": fim["B5-2"] - 8,
    "item06_B5-3": fim["B5-3"] - 8,
    "item07_B6-1_painel_saiu": gat_q("PB6", "B6-1", "com seis paredes"),
    "item08_B7-1_rotulos": fim["B7-1"] - 8,
    "item08_B7-2_rotulos": fim["B7-2"] - 8,
    "item09_S4_previa": gat_q("PS", "S4", "se essa aula te ajudou") - 3,
    "item09_S4_cta": Q["S4"] + round((A["ancoras"]["S4"]["dur"] + 2.0) * FPS),
    "item10_B3-5_tem_giro": gat_q("PB3", "B3-5", "esse rio tem giro ou não") + 12,
    "item11_B4-6_agua": fim["B4-6"] - 8,
    "item13_B3-4_rankine": fim["B3-4"] - 8,
}
quer = sorted({q for _, _, q, _ in PEDIDOS} | set(PROVAS.values()) | set(Q[a] + round(A["ancoras"][a]["t"][0] * FPS) for a in ordem))
fr = {}
c = av.open(str(VID))
for i, f in enumerate(c.decode(video=0)):
    if i in quer:
        fr[i] = f.to_image()
    if i > quer[-1]:
        break
fonte = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
for n, alvo, q, leg in PEDIDOS:
    im = Image.new("RGB", (1920, 580), "#0b1020")
    im.paste(Image.open(alvo).convert("RGB").resize((960, 540)), (0, 40))
    im.paste(fr[q], (960, 40))
    d = ImageDraw.Draw(im)
    d.text((10, 8), f"ALVO {n} · {leg}", fill="#FF7A8A", font=fonte)
    d.text((970, 8), f"RENDER v5 · {q / FPS // 60:.0f}:{q / FPS % 60:04.1f}", fill="#8CFFD2", font=fonte)
    im.save(OUT / f"lado_{n}.png")
for nome, q in PROVAS.items():
    fr[q].save(OUT / f"{nome}.png")
k = 0
for p in range(0, len(ordem), 9):
    grade = Image.new("RGB", (960 * 3, 580 * 3), "#0b1020")
    d = ImageDraw.Draw(grade)
    for j, a in enumerate(ordem[p:p + 9]):
        q = Q[a] + round(A["ancoras"][a]["t"][0] * FPS)
        x, y = (j % 3) * 960, (j // 3) * 580
        grade.paste(fr[q], (x, y + 40))
        d.text((x + 10, y + 8), f"{a} · 1ª palavra «{A['ancoras'][a]['fala'].split()[0]}» · {q / FPS // 60:.0f}:{q / FPS % 60:04.1f}", fill="#A9CCFF", font=fonte)
    k += 1
    grade.save(OUT / f"ancoras_1a_palavra_{k}.png")
print(len(PEDIDOS), "lado a lado;", len(PROVAS), "provas;", k, "pranchas de âncoras em", OUT)
