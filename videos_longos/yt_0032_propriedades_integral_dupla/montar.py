"""yt_0032 · monta o preview inteiro (960×540, 15 fps, sem áudio) concatenando os lotes na ordem do vídeo, quadro a quadro e sem sobreposição
(o início de cada lote cai no início estimado da âncora: os tempos da narração v3 ficam intactos para a voz encaixar depois).
Saídas: renders/v1/yt_0032_preview_v1_540p15.mp4 e renders/v1/lotes_v1.json (quadro do início de cada lote).
uso: python montar.py [rodada]"""
import json
import sys
from pathlib import Path

import av

U = Path(__file__).resolve().parent
RODADA = sys.argv[1] if len(sys.argv) > 1 else "v1"
ORDEM = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PS"]


def main():
    out_dir = U / "renders" / RODADA
    out_dir.mkdir(parents=True, exist_ok=True)
    saida = out_dir / f"yt_0032_preview_{RODADA}_540p15.mp4"
    o = av.open(str(saida), "w")
    st = o.add_stream("libx264", rate=15)
    st.width, st.height, st.pix_fmt = 960, 540, "yuv420p"
    st.options = {"crf": "18", "preset": "veryfast"}
    n, ini = 0, {}
    for lote in ORDEM:
        ini[lote] = n
        c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
        for fr in c.decode(video=0):
            for p in st.encode(av.VideoFrame.from_ndarray(fr.to_ndarray(format="rgb24"), format="rgb24")):
                o.mux(p)
            n += 1
        c.close()
        print(f"[montar] {lote}: começa no quadro {ini[lote]} ({ini[lote] / 15:.2f} s)")
    for p in st.encode():
        o.mux(p)
    o.close()
    (out_dir / f"lotes_{RODADA}.json").write_text(json.dumps({"quadros": n, "duracao_s": round(n / 15, 2), "inicio": ini}, indent=1), encoding="utf-8")
    print(f"[montar] {saida.name}: {n} quadros = {n / 15:.2f} s = {int(n / 15) // 60}:{n / 15 % 60:05.2f}")


if __name__ == "__main__":
    main()
