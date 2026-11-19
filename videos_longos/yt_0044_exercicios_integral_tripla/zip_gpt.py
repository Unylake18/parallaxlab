"""yt_0044 · zips para o GPT avaliar o preview v1 (temporários: não commitar, nunca em entregas/).
- yt0044_v1_para_gpt.zip: o MP4, lotes_v1.json, os relatórios de QA (txt), a prancha dos alvos, a prancha das emendas e os 26 stills 1080p + comparações.
- yt0044_v1_quadros_parteN.zip: TODOS os quadros do preview (um JPEG por quadro, 960×540, nome q<índice>_<mm-ss.ss>_<lote>.jpg), em partes de até ~450 MB."""
import io
import json
import zipfile
from pathlib import Path

import av

U = Path(__file__).resolve().parent
V = U / "renders/v1"
QA = V / "qa"
MP4 = V / "yt_0044_preview_v1_540p15.mp4"
ini = json.loads((V / "lotes_v1.json").read_text())["inicio"]
ordem = sorted(ini.items(), key=lambda kv: kv[1])

with zipfile.ZipFile(V / "yt0044_v1_para_gpt.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.write(MP4, MP4.name)
    z.write(V / "lotes_v1.json", "lotes_v1.json")
    for f in sorted(QA.glob("*.txt")):
        z.write(f, f"qa/{f.name}")
    for f in ("prancha_alvos.jpg", "emendas_v1.jpg"):
        z.write(QA / f, f"qa/{f}")
    for f in sorted((QA / "comparacao").glob("*.jpg")):
        z.write(f, f"qa/comparacao/{f.name}")
    for f in sorted((QA / "comparacao/stills").glob("*.png")):
        z.write(f, f"qa/stills_1080p/{f.name}")
print("principal:", round((V / "yt0044_v1_para_gpt.zip").stat().st_size / 1e6, 1), "MB")

LIM = 450e6
parte, tam, z = 0, 0, None
c = av.open(str(MP4))
for i, fr in enumerate(c.decode(video=0)):
    lote = [l for l, q in ordem if q <= i][-1]
    t = i / 15
    b = io.BytesIO()
    fr.to_image().save(b, "JPEG", quality=88)
    if z is None or tam + b.tell() > LIM:
        if z:
            z.close()
        parte += 1
        tam = 0
        z = zipfile.ZipFile(V / f"yt0044_v1_quadros_parte{parte}.zip", "w", zipfile.ZIP_STORED)
    z.writestr(f"q{i:05d}_{int(t // 60):02d}-{t % 60:05.2f}_{lote}.jpg", b.getvalue())
    tam += b.tell()
z.close()
c.close()
for f in sorted(V.glob("yt0044_v1_quadros_parte*.zip")):
    with zipfile.ZipFile(f) as zz:
        nomes = zz.namelist()
    print(f.name, round(f.stat().st_size / 1e6, 1), "MB", len(nomes), "quadros", nomes[0], "…", nomes[-1])
