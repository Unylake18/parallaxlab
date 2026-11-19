"""yt_0031 final: versão 960×540 / 15 fps do master 1080p30 (um quadro a cada dois, sem áudio) → renders/final/yt_0031_preview_final_540p15_mudo.mp4,
para o zip do GPT (os quadros e o vídeo leve são do vídeo FINAL). A voz é colada depois com videos/montar_master.py."""
from pathlib import Path

import av
from fractions import Fraction

U = Path(__file__).resolve().parent
out_dir = U / "renders" / "final"
out_dir.mkdir(parents=True, exist_ok=True)
src = av.open(str(U / "renders" / "yt_0031_master_final_1080p30.mp4"))
o = av.open(str(out_dir / "yt_0031_preview_final_540p15_mudo.mp4"), "w")
st = o.add_stream("libx264", rate=15)
st.width, st.height, st.pix_fmt = 960, 540, "yuv420p"
st.options = {"crf": "18", "preset": "veryfast"}
n = 0
for k, fr in enumerate(src.decode(video=0)):
    if k % 2:
        continue
    im = av.VideoFrame.from_ndarray(fr.reformat(width=960, height=540, format="rgb24").to_ndarray(), format="rgb24")
    im.pts, im.time_base = n, Fraction(1, 15)           # PTS explícito (sem ele o mux recusa pacotes no meio do vídeo)
    for p in st.encode(im):
        o.mux(p)
    n += 1
for p in st.encode():
    o.mux(p)
o.close()
print(n, "quadros", round(n / 15, 2), "s")
