"""yt_0031 · monta o preview inteiro (960×540, 15 fps, sem áudio) concatenando os lotes na ordem (cada lote termina no papel vazio e o
seguinte começa dele). Saídas: renders/v1/yt_0031_preview_v1_540p15.mp4 e renders/v1/lotes_v1.json (início de cada lote em s)."""
import json
from pathlib import Path

import os

import av

U = Path(__file__).resolve().parent
ORDEM = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PB8", "PB9", "PS"]


def main():
    R = os.environ.get("RODADA", "v2")
    out = U / "renders" / R
    out.mkdir(parents=True, exist_ok=True)
    o = av.open(str(out / f"yt_0031_preview_{R}_540p15.mp4"), "w")
    st = o.add_stream("libx264", rate=15)
    st.width, st.height, st.pix_fmt = 960, 540, "yuv420p"
    st.options = {"crf": "18", "preset": "veryfast"}
    n, ini = 0, {}
    for lote in ORDEM:
        ini[lote] = round(n / 15, 3)
        with av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4")) as c:
            for fr in c.decode(video=0):
                for p in st.encode(av.VideoFrame.from_ndarray(fr.to_ndarray(format="rgb24"), format="rgb24")):
                    o.mux(p)
                n += 1
    for p in st.encode():
        o.mux(p)
    o.close()
    (out / f"lotes_{R}.json").write_text(json.dumps({"inicio_s": ini, "total_s": round(n / 15, 3), "quadros": n}, indent=1), encoding="utf-8")
    print(f"{n} quadros = {int(n / 15 // 60)}:{n / 15 % 60:05.2f}")


if __name__ == "__main__":
    main()
