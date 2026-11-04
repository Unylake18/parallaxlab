"""yt_0022: pacote zip completo para avaliação do Claude / GPT.
Inclui:
- Um quadro a cada 3 do preview (5 fps, JPG comprimido a 80%)
- O MP4 preview completo (renders/preview_yt0022_v1_960x540.mp4)
- Todos os 16 quadros de conferência PNG e as 9 pranchas PNG
- Relatórios de QA (qa.txt, equacao.txt, algebra.txt, parado.txt, capitulos_v1.txt, quadros_v1.json, portao_*)
- Código-fonte completo da unidade (cena.py, kit.py, fisica22.py, sec_*.py, threejs/cena3d/*.js)
- Ficha e narração (ficha.md, narracao_sugestao.md, ancoras.json)
"""
import glob
import io
import os
import zipfile
from pathlib import Path
import av

U = Path(__file__).resolve().parent
SRC = U / "renders" / "preview_yt0022_v1_960x540.mp4"
ZP = U / "renders" / "yt0022_v1_para_claude.zip"
FPS = 15

print("Iniciando montagem do zip para Claude...")
EXTRA_FILES = [
    "renders/v1/pranchas/*.png",
    "renders/v1/conferencia/*.png",
    "renders/*.txt",
    "renders/*.json",
    "ficha.md",
    "narracao_sugestao.md",
    "ancoras.json",
    "fisica22.py",
    "kit.py",
    "cena.py",
    "sec_*.py",
    "qa22.py",
    "equacao22.py",
    "algebra22.py",
    "parado22.py",
    "montar_preview.py",
    "conferencia.py",
    "agrupar_portao.py",
    "classifica_portao.py",
    "threejs/cena3d/*.js",
    "threejs/pedidos3d/*.json"
]

tot_quadros = 0
with zipfile.ZipFile(ZP, "w", zipfile.ZIP_DEFLATED) as z:
    # 1. Quadros amostrados a cada 3 (5 fps)
    print("Decodificando e salvando quadros (5 fps)...")
    c = av.open(str(SRC))
    st = c.streams.video[0]
    for i, fr in enumerate(c.decode(st)):
        if i % 3 != 0:
            continue
        buf = io.BytesIO()
        im = fr.to_image()
        im.save(buf, "JPEG", quality=80)
        z.writestr(f"quadros/q{i:05d}_{i / FPS:06.1f}s.jpg", buf.getvalue())
        tot_quadros += 1
    c.close()
    print(f"Salvos {tot_quadros} quadros JPG.")

    # 2. Preview MP4
    print("Adicionando preview MP4...")
    z.write(SRC, "preview_yt0022_v1_960x540.mp4")

    # 3. Arquivos extras
    print("Adicionando código, relatórios e pranchas...")
    for pat in EXTRA_FILES:
        full_pat = str(U / pat)
        for f in sorted(glob.glob(full_pat)):
            rel = os.path.relpath(f, str(U))
            z.write(f, rel)

tam_mb = round(os.path.getsize(ZP) / 1e6, 1)
print(f"SUCESSO: Zip criado em {ZP} ({tam_mb} MB, {tot_quadros} quadros JPG + MP4 + código + pranchas + relatórios)")
