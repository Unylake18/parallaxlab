"""yt_0019 v10: prancha extra (8 quadros), tabela R0, manifesto e zip final (só v10) na raiz do repositório."""
import json
import re
import zipfile
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
R = U / "renders"
V = R / "v10"
MASTER = R / "master_yt0019_v10_1080p30.mp4"
ZP = U.parent.parent / "yt0019_final_v10_para_gpt.zip"

# prancha extra: 8 quadros espalhados, escolhidos fora dos itens do handoff
ALVOS = [75.0, 300.0, 480.0, 700.0, 880.0, 990.0, 1090.0, 1150.0]
c = av.open(str(MASTER))
v = c.streams.video[0]
q = {int(t * 30): t for t in ALVOS}
fr = {}
for i, f in enumerate(c.decode(v)):
    if i in q:
        fr[q[i]] = f.to_image().resize((960, 540))
    if i >= max(q):
        break
fo = Image.new("RGB", (1920, 560 * 4), "black")
d = ImageDraw.Draw(fo)
for k, t in enumerate(ALVOS):
    x, y = (k % 2) * 960, (k // 2) * 560
    fo.paste(fr[t], (x, y + 20))
    d.text((x + 6, y + 4), f"v10 · {int(t // 60)}:{t % 60:04.1f}", fill="white")
fo.save(V / "r0_extra_8quadros.png")

ITENS = [
    ("F1", "empuxo T2-5 (5:12–5:27)", "resolvido", "equação montada inteira em todos os quadros; sem sumiço"),
    ("F2", "T1-2 (1:44–1:48)", "resolvido", "equação acesa por cópia; nunca desmontada"),
    ("F3", "T1-3 (2:16–2:22)", "resolvido", "idem"),
    ("F4", "Tsiolkovsky (7:24)", "resolvido", "realce por cópia"),
    ("F5", "gravidade (10:28–10:32)", "resolvido", "sem glifo órfão; 2ª equação surge por revelação"),
    ("F6", "t_q (11:50–11:54)", "resolvido", "sem FadeOut+FadeIn da mesma equação"),
    ("F7", "a_f (12:26–12:30)", "resolvido", "idem"),
    ("F8", "P / carga (13:38)", "resolvido", "o P solto à direita deixou de existir"),
    ("F9", "m_f, R_max (13:46–13:56)", "resolvido", "acendimento + cópia"),
    ("F10", "m_02 (14:52–14:56)", "resolvido", "idem"),
    ("M1–M9", "trechos mortos", "resolvido, com ressalva", "8 trechos ≥8 s → 0; 48 → 3 trechos de 3,0–3,4 s (0:13,6 · 0:27,2 · 9:58,4): batimento só da poeira estelar; ver relatório"),
    ("Fecho", "síntese → desafio → gancho FIM-1 → cartão FIM-2", "resolvido", "gancho com barras K/CALOR e selo COLISÕES EM 1D; cartão com logo, INSCREVA-SE e moldura livre"),
]
t = ["# R0 · yt_0019 v10 (antes v9 × depois v10)\n", "| item | trecho | estado | nota |", "|---|---|---|---|"]
t += [f"| {a} | {b} | {c_} | {n} |" for a, b, c_, n in ITENS]
(V / "r0_tabela.md").write_text("\n".join(t) + "\n", encoding="utf-8")

med = json.load(open(U / "audio" / "audio10_medidas.json", encoding="utf-8"))
man = {
    "video": "yt_0019 · Por que um foguete é quase todo combustível?",
    "versao": "v10",
    "master": MASTER.name,
    "formato": "1920x1080, 30 fps, H.264 yuv420p, CRF 14.0, AAC",
    "duracao_s": 1157.5,
    "legenda": "legenda - yt0019.srt",
    "capitulos": "capitulos_final_v10.txt",
    "audio": {"piso_pausas_dBFS_p95": med["pausa_final_dBFS_p95"], "pausa_mediana_dBFS": med["pausa_final_dBFS_mediana"],
              "pico_dBFS": med["pico_final_dBFS"], "cama_de_ruido": "removida"},
    "trechos_mortos": {"v9_>=8s": 8, "v10_>=8s": 0, "v10_>=3s": 3},
    "sincronia": {"gatilhos": 185, "atraso_max_s": 0.17, "adiantado_max_s": -0.14},
    "amarelo_pixels": 0,
}
(V / "manifesto.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")

tags = (U / "narracao_v10.md").read_text(encoding="utf-8")
(V / "narracao_tags_v10.md").write_text(tags, encoding="utf-8")

with zipfile.ZipFile(ZP, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(MASTER, "master_yt0019_v10_1080p30.mp4")
    z.write(R / "legenda - yt0019.srt", "legenda - yt0019.srt")
    z.write(R / "capitulos_final_v10.txt", "capitulos_final_v10.txt")
    z.write(V / "manifesto.json", "manifesto.json")
    z.write(U / "audio" / "narracao_v10.wav", "narracao_v10.wav")
    z.write(V / "narracao_tags_v10.md", "narracao_tags_v10.md")
    z.write(V / "r0_tabela.md", "r0_tabela.md")
    z.write(V / "r0_extra_8quadros.png", "r0/extra_8quadros.png")
    z.write(V / "morto_v10.txt", "morto_v10.txt")
    z.write(R / "morto_v9.txt", "morto_v9.txt")
    for p in sorted((V / "r0").glob("*.png")):
        z.write(p, f"r0/{p.name}")
print(ZP, round(ZP.stat().st_size / 1e6, 1), "MB")
