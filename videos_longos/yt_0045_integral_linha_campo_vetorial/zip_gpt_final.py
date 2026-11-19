"""yt_0045 · zips para o GPT avaliar o preview final com voz (temporários: não commitar, nunca em entregas/).
- yt0045_final_para_gpt.zip: o MP4, lotes_final.json, os relatórios de QA (txt), a prancha dos alvos, a prancha das emendas e os 18 stills 1080p + comparações.
- yt0045_final_quadros_parteN.zip: TODOS os quadros do preview (um JPEG por quadro, 960×540, nome q<índice>_<mm-ss.ss>_<lote>.jpg), em partes de até ~450 MB."""
import io
import json
import zipfile
from pathlib import Path

import av

U = Path(__file__).resolve().parent
V = U / "renders/final"
QA = V / "qa"
MP4 = V / "yt_0045_preview_final_540p15_com_voz.mp4"
MP4Q = V / "yt_0045_preview_final_540p15.mp4"
ini = json.loads((V / "lotes_final.json").read_text())["inicio"]
ordem = sorted(ini.items(), key=lambda kv: kv[1])

with zipfile.ZipFile(V / "yt0045_final_para_gpt.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.write(MP4, MP4.name)
    z.write(V / "lotes_final.json", "lotes_final.json")
    for f in sorted(QA.glob("*.txt")):
        z.write(f, f"qa/{f.name}")
    for f in [f for f in ("prancha_alvos.jpg", "emendas_final.jpg", "correcoes_final.jpg") if (QA / f).exists()]:
        z.write(QA / f, f"qa/{f}")
    for f in sorted((QA / "comparacao").glob("*.jpg")):
        z.write(f, f"qa/comparacao/{f.name}")
    for f in sorted((QA / "comparacao/stills").glob("*.png")):
        z.write(f, f"qa/stills_1080p/{f.name}")
with zipfile.ZipFile(V / "yt0045_final_para_gpt.zip", "a", zipfile.ZIP_DEFLATED) as z:
    for rel, nome in ((U / "qa" / "sync_voz.txt", "qa/sync_voz.txt"), (U / "qa" / "voz.txt", "qa/voz.txt"), (V / "qa_1080.txt", "qa/qa_1080.txt"),
                      (V / "ancoras_master_1080.jpg", "qa/ancoras_master_1080.jpg"), (U / "legenda.srt", "legenda.srt"), (U / "renders" / "capitulos_final.txt", "capitulos_final.txt")):
        if rel.exists():
            z.write(rel, nome)
print("principal:", round((V / "yt0045_final_para_gpt.zip").stat().st_size / 1e6, 1), "MB")

LIM = 450e6
parte, tam, z = 0, 0, None
c = av.open(str(MP4Q))
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
        z = zipfile.ZipFile(V / f"yt0045_final_quadros_parte{parte}.zip", "w", zipfile.ZIP_STORED)
    z.writestr(f"q{i:05d}_{int(t // 60):02d}-{t % 60:05.2f}_{lote}.jpg", b.getvalue())
    tam += b.tell()
z.close()
c.close()
for f in sorted(V.glob("yt0045_final_quadros_parte*.zip")):
    with zipfile.ZipFile(f) as zz:
        nomes = zz.namelist()
    print(f.name, round(f.stat().st_size / 1e6, 1), "MB", len(nomes), "quadros", nomes[0], "…", nomes[-1])
