"""Zip para avaliação (formato do zip_gpt.py do yt_0016): um quadro a cada 3 (5 fps, JPG) do preview + MP4 + pranchas + QA + código e textos.
uso: python zip_gpt.py lote1  → renders/lote1_para_gpt.zip
     python zip_gpt.py teste3d → renders/teste3d_para_gpt.zip (teste das cenas 3D)"""
import glob
import io
import os
import sys
import zipfile

import av

R = sys.argv[1] if len(sys.argv) > 1 else "lote1"
SRC = {"lote1": "renders/preview_yt0017_lote1_960x540.mp4", "teste3d": "renders/teste3d_yt0017_960x540.mp4"}[R]
ZP, FPS = f"renders/{R}_para_gpt.zip", 15
EXTRA = {"lote1": ["renders/prancha_PH.png", "renders/prancha_P1.png", "renders/prancha_P2.png", "renders/granada_turntable.png", "renders/conferencia/*.png",
                   "renders/capitulos_lote1.txt", "renders/qa_lote1.txt", "renders/conferencia_lote1.png", "ficha.md", "narracao_sugestao.md", "kit.py", "pecas3d.py",
                   "camadas.py", "sec_abertura.py", "sec_t1.py", "sec_t2.py", "threejs/cena3d/cm3d.js", "threejs/cena3d/campo.js",
                   "threejs/cena3d/granada_medidas.json"],
         "teste3d": ["renders/prancha_teste3d.png", "renders/troca_haltere_3d_2d.png", "renders/qa_teste3d.txt", "ficha.md", "kit.py",
                     "sec_teste3d.py", "qa_3d.py", "threejs/cena3d/cm3d.js"]}[R]
c = av.open(SRC)
st = c.streams.video[0]
tot = 0
with zipfile.ZipFile(ZP, "w", zipfile.ZIP_DEFLATED) as z:
    for i, fr in enumerate(c.decode(st)):
        if i % 3:
            continue
        b = io.BytesIO()
        fr.to_image().save(b, "JPEG", quality=85)
        z.writestr(f"quadros/q{i:05d}_{i / FPS:06.1f}s.jpg", b.getvalue())
        tot += 1
    z.write(SRC, os.path.basename(SRC))
    for f in EXTRA:
        for g in glob.glob(f):
            z.write(g, os.path.relpath(g, "renders") if "conferencia/" in g.replace(os.sep, "/") else os.path.basename(g))
print(tot, "quadros", round(os.path.getsize(ZP) / 1e6, 1), "MB")
