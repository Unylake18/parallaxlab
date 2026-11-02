"""Zip para avaliação do v7 (formato do zip_gpt.py do yt_0017): um quadro a cada 3 (5 fps, JPG) do preview + MP4 + pranchas + prancha de sincronia +
QA + capítulos + a narração contínua (WAV) e os textos. uso: python zip_gpt.py → renders/v7_para_gpt.zip"""
import glob
import io
import os
import zipfile

import av

SRC, ZP, FPS = "renders/preview_yt0018_v7_960x540.mp4", "renders/v7_para_gpt.zip", 15
EXTRA = ["renders/v7/prancha_*.png", "renders/v7/sync/*.png", "renders/v7/sync/frases.json", "renders/capitulos_v7.txt", "renders/qa.txt",
         "renders/v7/prancha_humana_24.png", "renders/v7/agua.json", "renders/v7/p99.json", "renders/relatorio_final.md", "renders/final/prancha_final.png", "renders/capitulos_final.txt", "montar_final.py", "render_f1080.sh", "entregar_yt0018.py", "notas18.py", "renders/v7_antes_congelamento.txt",
         "renders/v7_antes_voz.txt", "audio/narracao_v7.wav", "audio/voz7_tempos.json", "audio/voz7_deslocamento.json", "narracao_tags_v1_4.md", "ancoras.json",
         "ficha.md", "prob.py", "prob2.py", "kit.py", "lago2.py", "pecas18.py", "icones.py", "sec_*.py", "qa.py", "congelamento.py", "auditoria_voz.py",
         "verifica_tempos.py", "gerar_voz_v7.py", "unir_voz.py", "gerar_ancoras.py", "montar_audio.py", "conferir_sync.py", "idle_plano.py", "medir.sh",
         "threejs/cena3d/cm18.js", "threejs/cena3d/lago3d.js"]
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
