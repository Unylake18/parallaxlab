"""yt_0019: zip para avaliação: um quadro a cada 3 (5 fps, JPG) do preview + MP4 + pranchas + quadros de conferência + QA + capítulos + código.
uso: python zip_gpt.py → renders/v7_para_gpt.zip"""
import glob
import io
import os
import zipfile

import av

SRC, ZP, FPS = "renders/preview_yt0019_v7_960x540.mp4", "renders/v7_para_gpt.zip", 15
EXTRA = ["renders/v7/prancha_*.png", "renders/v7/r0_folha_*.png", "renders/v7/r0/*.png", "renders/v7/extra_*.png", "renders/v7/r0_tabela.md", "renders/cor.txt", "renders/amarelo.txt", "qa_amarelo.py", "qa_cor.py", "conferencia7.py", "renders/v7/prancha_humana_24.png", "renders/capitulos_v5.txt", "renders/qa.txt",
         "ficha.md", "narracao_sugestao.md", "kit.py", "prob.py", "prob2.py", "pecas19.py", "sec_*.py", "qa19.py", "areas.py", "renders/area_morta.txt", "threejs/cena3d/f19.js"]
c = av.open(SRC)
tot = 0
with zipfile.ZipFile(ZP, "w", zipfile.ZIP_DEFLATED) as z:
    for i, fr in enumerate(c.decode(c.streams.video[0])):
        if i % 3:
            continue
        b = io.BytesIO()
        fr.to_image().save(b, "JPEG", quality=85)
        z.writestr(f"quadros/q{i:05d}_{i / FPS:06.1f}s.jpg", b.getvalue())
        tot += 1
    z.write(SRC, os.path.basename(SRC))
    for f in EXTRA:
        for g in sorted(glob.glob(f)):
            z.write(g, os.path.relpath(g, "renders") if g.replace(os.sep, "/").startswith("renders/") else g)
print(tot, "quadros", round(os.path.getsize(ZP) / 1e6, 1), "MB")
