import glob, io, zipfile
from pathlib import Path
import av
U = Path(__file__).resolve().parent
SRC = U/"renders"/"preview_yt0022_v6_960x540_voz.mp4"
ZP = U/"renders"/"yt0022_v6_para_claude.zip"
z = zipfile.ZipFile(ZP, "w", zipfile.ZIP_DEFLATED)
c = av.open(str(SRC)); n = 0
for i, fr in enumerate(c.decode(video=0)):
    if i % 3: continue
    b = io.BytesIO(); fr.to_image().save(b, "JPEG", quality=80)
    z.writestr(f"quadros_5fps/q{i:05d}.jpg", b.getvalue()); n += 1
z.write(SRC, "preview_yt0022_v6_960x540_voz.mp4")
pats = ["renders/chk/*.png","renders/contact/*.png","renders/*.txt","renders/*.json","ficha.md","narracao_tags.md","ancoras.json","kit.py","cena.py","sec_*.py","pecas22.py","prob*.py","qa22.py","parado22.py","sync22.py","montar_preview.py","montar_final1080.py","render_f1080.sh","threejs/cena3d/*.js","threejs/cena3d/*.html","threejs/r3d.js"]
for p in pats:
    for f in glob.glob(str(U/p)):
        z.write(f, str(Path(f).relative_to(U)))
z.close(); print(n, ZP.stat().st_size/1e6, "MB")
