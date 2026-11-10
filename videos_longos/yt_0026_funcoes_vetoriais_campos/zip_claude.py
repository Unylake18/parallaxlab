"""yt_0026 (padrão do zip_claude.py do yt_0022): pacote zip para avaliação do Claude / GPT.
Inclui: um quadro a cada 3 do preview com B7 (5 fps, JPG 80%); o MP4 preview com B7 (referência: o B7 fica); a folha de contato;
renders/qa_<rodada>.txt (linhas de QA de todos os logs: âncoras, gatilhos, álgebra, cor, campos, flash, qa, estilo, tempo + alinhamento 3D,
transparências e custo por quadro do 3D);
capítulos, quadros e durações; código da unidade; ficha, narração e âncoras; Three.js (cenas, pedidos, timeline).
uso: python zip_claude.py [rodada] → renders/yt0026_<rodada>_para_claude.zip (v2: inclui renders/v2/qa)"""
import glob
import io
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import av

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v1"
SRC = U / "renders" / f"preview_yt0026_{R}_com_b7_960x540.mp4"
ZP = U / "renders" / f"yt0026_{R}_para_claude.zip"
FPS = 15
LOTES = ["PT", "PAH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PS"]

# resumo de QA a partir dos logs do render
linhas = []
for c in LOTES:
    log = (U / f"log_{c}.txt").read_text(encoding="utf-8", errors="replace")
    linhas.append(f"== {c}")
    linhas += [l for l in log.splitlines() if re.match(r"\[(ancora|gatilho|algebra|cor-bloco|campo|flash|flash-total|qa|estouro|hook|polar|estilo|tempo)\]", l)]
q3d = subprocess.run([sys.executable, str(U / "qa3d.py"), "PT", "PB4", "PB7"], capture_output=True, text=True, encoding="utf-8").stdout
linhas += ["== alinhamento 3D × Manim (qa3d.py)"] + [l for l in q3d.splitlines() if l.startswith("[qa3d]")]
linhas.append("== 3D: transparências por cena ([estilo3d]) e custo por quadro (r3d.js)")
for c in ("PT", "PB4", "PB7"):
    l3 = (U / f"log_3d_{c}.txt").read_text(encoding="utf-8", errors="replace").splitlines()
    linhas += [f"{c}: {l}" for l in l3 if "[estilo3d]" in l or "s_por_quadro" in l or "campo_espaco:" in l]
(U / "renders" / f"qa_{R}.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")

EXTRA = [f"renders/folha_contato_{R}.png", f"renders/qa_{R}.txt", f"renders/capitulos_{R}_com_b7.txt", f"renders/quadros_{R}_com_b7.json", f"renders/{R}/qa/*.png",
         "ficha.md", "narracao.md", "ancoras.json", "duracoes_estimadas.json", "*.py", "*.sh",
         "threejs/r3d.js", "threejs/cena3d/b3d.js", "threejs/cena3d/f26.js", "threejs/cena3d/*.html", "threejs/pedidos3d/*.json", "threejs/timeline.json"]

n = 0
with zipfile.ZipFile(ZP, "w", zipfile.ZIP_DEFLATED) as z:
    c = av.open(str(SRC))
    for i, fr in enumerate(c.decode(video=0)):
        if i % 3:
            continue
        buf = io.BytesIO()
        fr.to_image().save(buf, "JPEG", quality=80)
        z.writestr(f"quadros/q{i:05d}_{i / FPS:06.1f}s.jpg", buf.getvalue())
        n += 1
    c.close()
    z.write(SRC, SRC.name)
    for pat in EXTRA:
        for f in sorted(glob.glob(str(U / pat))):
            z.write(f, os.path.relpath(f, U))
print(f"zip: {ZP} ({os.path.getsize(ZP) / 1e6:.1f} MB, {n} quadros JPG + MP4 + código + relatórios)")
