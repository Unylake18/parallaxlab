"""yt_0024: quadros de conferência do preview (handoff §7.5) e zip de QA sem .mp4.
Para cada âncora pedida, extrai o quadro a 85 % da âncora (estado montado) do preview, amplia para 1920×1080 (Lanczos) e grava
renders/conferencia/<âncora>.png e uma prancha. Zip: renders/qa_yt0024_<rodada>.zip (pranchas, conferência, objetos, qa.txt, capítulos, logs de auditoria).
uso: python conferencia24.py [rodada]"""
import json
import sys
import zipfile
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v1"
PED = ["H2", "H3", "B1-3", "B1-4", "B2-3", "B2-5", "B3-2", "B3-5", "B4-2", "B4-4", "B5-4", "B5-5", "B6-3", "B6-4", "B6-5", "B6-7", "B6-8", "S1"]
q = json.loads((U / "renders" / f"quadros_{R}.json").read_text(encoding="utf-8"))
ordem = sorted(q.items(), key=lambda kv: kv[1])
alvo = {}
for i, (a, f0) in enumerate(ordem):
    if a in PED:
        f1 = ordem[i + 1][1] if i + 1 < len(ordem) else f0 + 150
        alvo[f0 + int(0.85 * (f1 - f0))] = a
D = U / "renders" / "conferencia"
D.mkdir(parents=True, exist_ok=True)
c = av.open(str(U / "renders" / f"preview_yt0024_{R}_960x540.mp4"))
ims = []
for n, fr in enumerate(c.decode(video=0)):
    if n in alvo:
        im = fr.to_image()
        im.resize((1920, 1080), Image.LANCZOS).save(D / f"{alvo[n]}.png")
        t = im.copy()
        ImageDraw.Draw(t).text((8, 6), f"{alvo[n]}  q{n}  {n / 15:.1f}s", fill=(255, 230, 0))
        ims.append(t)
P = Image.new("RGB", (960 * 3, 540 * ((len(ims) + 2) // 3)))
for k, im in enumerate(ims):
    P.paste(im, ((k % 3) * 960, (k // 3) * 540))
P.save(U / "renders" / "prancha_conferencia.png")
z = U / "renders" / f"qa_yt0024_{R}.zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in sorted((U / "renders").glob("prancha_*.png")):
        zf.write(f, f"pranchas/{f.name}")
    for f in sorted(D.glob("*.png")):
        zf.write(f, f"conferencia_1920x1080/{f.name}")
    for f in sorted((U / "renders" / "objetos").glob("*")):
        zf.write(f, f"objetos_1920x1080/{f.name}")
    for nome in ("qa.txt", f"capitulos_{R}.txt", "fisica_conferencia.txt", "parado.txt", "flash.txt", "portao_classificado.txt"):
        f = U / "renders" / nome
        if f.exists():
            zf.write(f, nome)
    for f in sorted(U.glob("log_aud_*.txt")):
        zf.write(f, f"auditoria/{f.name}")
    for nome in ("ficha.md", "narracao_v1.md", "ancoras.json", "mesa_tab.json"):
        zf.write(U / nome, nome)
print(json.dumps({"quadros": len(ims), "zip": str(z), "mb": round(z.stat().st_size / 1e6, 1)}))
