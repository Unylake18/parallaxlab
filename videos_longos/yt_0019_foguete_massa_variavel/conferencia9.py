"""yt_0019 v9 — R0 dos 4 ajustes de layout (§1) e dos 2 textos (§2.1): v8 (silencioso) × v9 (com voz), instantes de cada cena em cada vídeo. Saída: renders/v9/."""
from pathlib import Path
import av
from PIL import Image, ImageDraw
U = Path(__file__).resolve().parent
OUT = U / "renders" / "v9"; OUT.mkdir(parents=True, exist_ok=True)
# (id, descrição, t_v8, t_v9, recorte)
IT = [("1_sintese_logo", "Síntese: título × logo", 1225, 1100, (480, 0, 960, 200)),
      ("2_t2_Femp", "T2-5: F_emp sobre o tracejado", 368, 332, (480, 100, 960, 300)),
      ("3_e3_inset", "E3: inset × rótulo v = 1,5 m/s", 1150, 1043, (0, 280, 520, 540)),
      ("4_t2_nada", "T2-7: NADA NA HORIZONTAL", 437, 386, (0, 380, 480, 540)),
      ("5_t4_nota", "T4-2: nota SE O PROPELENTE DURAR", 700, 620, (480, 100, 960, 340)),
      ("6_e3_coef", "E3-4: NÃO DEPENDE DO COEFICIENTE DE ATRITO", 1170, 1062, (480, 60, 960, 300))]
def pega(arq, ts):
    c = av.open(str(arq)); al = {int(t * 15): t for t in ts}; got = {}
    for i, fr in enumerate(c.decode(video=0)):
        if i in al: got[al[i]] = fr.to_image()
        if i >= max(al): break
    return got
a = pega(U / "renders/preview_yt0019_v8_960x540.mp4", [x[2] for x in IT])
b = pega(U / "renders/preview_yt0019_v9_960x540.mp4", [x[3] for x in IT])
fo = Image.new("RGB", (1920, 540 * 0 + 0 + 1)); linhas = []
for n, d, t8, t9, box in IT:
    x0, y0, x1, y1 = box
    w = 960; h = int(w * (y1 - y0) / (x1 - x0))
    par = Image.new("RGB", (1920, h + 22), "black"); dr = ImageDraw.Draw(par)
    dr.text((4, 4), f"#{n} {d}   v8 {t8//60}:{t8%60:02d}  ←→  v9 {t9//60}:{t9%60:02d}", fill="yellow")
    par.paste(a[t8].crop(box).resize((w, h)), (0, 22)); par.paste(b[t9].crop(box).resize((w, h)), (960, 22))
    par.save(OUT / f"r0_{n}.png"); linhas.append(par)
fo = Image.new("RGB", (1920, sum(p.height for p in linhas))); y = 0
for p in linhas: fo.paste(p, (0, y)); y += p.height
fo.save(OUT / "r0_folha.png")
# sorteio de 6 quadros fora da lista
ts = [30, 250, 520, 780, 990, 1110]
g = pega(U / "renders/preview_yt0019_v9_960x540.mp4", ts)
sh = Image.new("RGB", (1920, 720))
for k, t in enumerate(ts): sh.paste(g[t].resize((640, 360)), ((k % 3) * 640, (k // 3) * 360))
sh.save(OUT / "extra_sorteio.png"); print("ok")
