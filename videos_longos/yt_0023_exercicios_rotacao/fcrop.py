import sys, av
from PIL import Image, ImageDraw
ev = [("PE1a", 90.07, (591, 282, 613, 300)), ("PE3", 272.47, (756, 268, 780, 279)), ("PE3", 301.53, (707, 278, 733, 290)), ("PE2", 159.13, (684, 375, 716, 399)),
      ("PE4", 142.50, (622, 219, 649, 231)), ("PE4", 187.87, (525, 259, 536, 286)), ("PE4", 274.90, (594, 219, 619, 231)), ("PE4", 290.57, (620, 253, 646, 265))]
dts = [-0.8, -0.5, -0.3, 0.0, 0.3, 0.8]
rows = []
for L, t0, (x0, y0, x1, y1) in ev:
    c = av.open(f"media_{L}/videos/cena/540p15/{L}.mp4"); fps = 15
    want = {int(round((t0 + d) * fps)): d for d in dts}
    got = {}
    for i, f in enumerate(c.decode(video=0)):
        if i in want: got[want[i]] = f.to_image().crop((x0 - 60, y0 - 25, x1 + 60, y1 + 25)).resize(((x1 - x0 + 120) * 2, (y1 - y0 + 50) * 2))
        if i > max(want): break
    W = max(g.size[0] for g in got.values()); H = max(g.size[1] for g in got.values())
    row = Image.new("RGB", (W * 6, H))
    for j, d in enumerate(dts):
        if d in got:
            row.paste(got[d], (j * W, 0)); ImageDraw.Draw(row).text((j * W + 3, 2), f"{L} {t0}{d:+}", fill=(255, 255, 0))
    rows.append(row)
Wm = max(r.size[0] for r in rows)
P = Image.new("RGB", (Wm, sum(r.size[1] for r in rows)))
y = 0
for r in rows: P.paste(r, (0, y)); y += r.size[1]
P.save("renders/v5/flash_events.png"); print(P.size)
