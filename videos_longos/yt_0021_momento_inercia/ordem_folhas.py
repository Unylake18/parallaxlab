"""yt_0021 — folhas de contato da ORDEM de escrita: um quadro a cada 0,3 s a partir de cada [ordem] do log (voa), 6 construções por folha → renders/v7/ordem/."""
import re, sys, json
from pathlib import Path
import av
from PIL import Image, ImageDraw
U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v7"
q = json.loads((U / "renders" / f"quadros_{R}.json").read_text(encoding="utf-8")) if (U / "renders" / f"quadros_{R}.json").exists() else {}
ini = {"PH": 0.0, "PA": 60.8, "PT1": 111.5, "PT2": 240.3, "PT3": 331.9, "PT4": 432.4, "PT5": 555.7, "PT6": 755.4, "PE1": 874.8, "PE2": 1022.6, "PE3": 1159.7, "PS": 1358.3}
evs = []
for l, t0 in ini.items():
    f = U / f"log_{l}.txt"
    if not f.exists():
        continue
    for m in re.finditer(r"\[ordem\] +([0-9.]+)s (\w+) n=(\d+)", f.read_text(encoding="utf-8", errors="replace")):
        evs.append((l, float(m.group(1)) + t0, m.group(2), int(m.group(3))))
evs.sort(key=lambda e: e[1])
c = av.open(str(U / "renders" / f"preview_yt0021_{R}_960x540.mp4"))
fr = {}
need = set()
for l, t, n_, k in evs:
    for j in range(6):
        need.add(round((t - 0.1 + 0.3 * j) * 15))
for i, x in enumerate(c.decode(video=0)):
    if i in need:
        fr[i] = x.to_image().crop((480, 40, 960, 310)).resize((320, 180))
    if i > max(need):
        break
out = U / "renders" / R / "ordem"
out.mkdir(parents=True, exist_ok=True)
for s in range(0, len(evs), 6):
    im = Image.new("RGB", (320 * 6, 180 * 6))
    for r, (l, t, n_, k) in enumerate(evs[s:s + 6]):
        for j in range(6):
            g = fr.get(round((t - 0.1 + 0.3 * j) * 15))
            if g is not None:
                im.paste(g, (j * 320, r * 180))
        ImageDraw.Draw(im).text((4, r * 180 + 4), f"{l} {int(t // 60)}:{t % 60:05.2f} {n_} partes", fill=(255, 255, 0))
    im.save(out / f"ordem_{s // 6 + 1:02d}.jpg", quality=82)
print(len(evs), "construções,", (len(evs) + 5) // 6, "folhas")
