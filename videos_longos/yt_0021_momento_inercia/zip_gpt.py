"""yt_0021: zip para avaliação: um quadro a cada 3 (5 fps, JPG) do preview + MP4 + pranchas + quadros de conferência + QA + capítulos + código.
uso: python zip_gpt.py → renders/v9_para_gpt.zip"""
import glob
import io
import os
import zipfile

import av

SRC, ZP, FPS = "renders/preview_yt0021_v9_960x540_voz.mp4", "renders/v9_para_gpt.zip", 15
EXTRA = ["renders/v9/sync/*", "renders/v9/portao/*", "renders/ponto_curva.txt", "renders/sync_final.txt", "renders/legenda_yt0021.srt", "renders/capitulos_final.txt", "renders/_master_conf1.jpg", "renders/_master_conf2.jpg", "renders/_master_conf3.jpg", "renders/_master_conf4.jpg", "montar_final21.py", "gerar_srt21.py", "entregar_yt0021.py", "render_f1080.sh", "renders/_final_checks1.jpg", "renders/_final_checks2.jpg", "portao_folhas.py", "medir.sh", "renders/v9/ordem/*.jpg", "renders/sync.txt", "renders/ordem_real.txt", "renders/portao_revisado.txt", "renders/coluna.txt", "narracao_tags.md", "alinhamento_palavras.json", "gerar_ancoras_voz.py", "sync21.py", "folhas_sync21.py", "medir.sh", "montar_voz.py", "renders/qa.txt", "renders/portao_unico.txt", "renders/algebra.txt", "renders/parado.txt", "renders/portao_classificado.txt", "renders/equacao.txt", "renders/capitulos_v9.txt", "ficha.md", "narracao_sugestao.md",
         "ancoras.json", "kit.py", "prob.py", "prob2.py", "pecas21.py", "sec_*.py", "qa21.py", "algebra21.py", "parado21.py", "agrupar_portao.py", "classifica_portao.py", "equacao21.py", "conferencia.py", "montar_preview.py", "threejs/cena3d/f21.js", "threejs/cena3d/b3d.js"]
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
            z.write(g, g)
print(tot, "quadros", round(os.path.getsize(ZP) / 1e6, 1), "MB")
