"""yt_0031: o mesmo conteúdo do zip para o GPT (zip_gpt.py), dividido em partes de até ~450 MB (limite de envio de 500 MB).
Parte 1: MP4 + código + QA + os primeiros quadros; as seguintes: só quadros. Nunca vai para entregas/."""
import io, sys, zipfile
from pathlib import Path
import av
U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v1"
LIM = 450 * 2**20
mp4 = U / "renders" / R / f"yt_0031_preview_{R}_540p15.mp4"
k, tam, z, saidas = 0, 0, None, []

def nova():
    global k, tam, z
    if z:
        z.close()
    k += 1
    p = U / "renders" / f"yt0031_{R}_para_gpt_parte{k}.zip"
    saidas.append(p)
    z = zipfile.ZipFile(p, "w", zipfile.ZIP_STORED)
    tam = 0

nova()
z.write(mp4, mp4.name); tam += mp4.stat().st_size
for f in sorted(U.glob("*.py")) + [U / "ficha.md", U / "narracao.md"]:
    z.write(f, f"codigo/{f.name}", compress_type=zipfile.ZIP_DEFLATED)
for f in sorted((U / "renders" / R / "qa").glob("*")):
    if f.suffix in (".txt", ".jpg"):
        z.write(f, f"qa/{f.name}"); tam += f.stat().st_size
c = av.open(str(mp4))
for i, fr in enumerate(c.decode(video=0)):
    b = io.BytesIO()
    fr.to_image().save(b, "PNG", optimize=False, compress_level=6)
    if tam + b.tell() > LIM:
        nova()
    t = i / 15
    z.writestr(f"quadros/q{i:05d}_{int(t) // 60:02d}m{t % 60:05.2f}s.png", b.getvalue()); tam += b.tell()
c.close(); z.close()
for p in saidas:
    print(p.name, round(p.stat().st_size / 2**20), "MB")
