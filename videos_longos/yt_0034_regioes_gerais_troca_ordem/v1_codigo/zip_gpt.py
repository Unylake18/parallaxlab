"""yt_0034 (copiado do yt_0032). Zip temporário para o GPT (memória do projeto): todos os quadros do preview (PNG, nome com índice e tempo) + MP4 + código + QA. Nunca vai para entregas/."""
import io, sys, zipfile
from pathlib import Path
import av
U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v1"
mp4 = U / "renders" / R / f"yt_0034_preview_{R}_540p15.mp4"
out = U / "renders" / f"yt0034_{R}_para_gpt.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as z:
    z.write(mp4, mp4.name)
    for f in sorted(U.glob("*.py")) + [U / "ficha.md", U / "narracao.md"]:
        z.write(f, f"codigo/{f.name}", compress_type=zipfile.ZIP_DEFLATED)
    for f in sorted((U / "renders" / R / "qa").glob("*")):
        if f.suffix in (".txt", ".jpg"):
            z.write(f, f"qa/{f.name}")
    c = av.open(str(mp4))
    for i, fr in enumerate(c.decode(video=0)):
        b = io.BytesIO()
        fr.to_image().save(b, "PNG", optimize=False, compress_level=6)
        t = i / 15
        z.writestr(f"quadros/q{i:05d}_{int(t) // 60:02d}m{t % 60:05.2f}s.png", b.getvalue())
    c.close()
print(out, round(out.stat().st_size / 2**30, 2), "GB")
