"""yt_0030 · monta o preview inteiro (960×540, 15 fps, sem áudio) a partir dos lotes, com a COSTURA de 0,4 s: os últimos 6 quadros do lote N (a
saída do layout antigo, depois do fim da fala) são compostos com os 6 primeiros do lote N+1 (a entrada do novo). Composição: onde os dois quadros
são iguais (canto, logo, fundo) fica o quadro; onde diferem, N + (N+1) − fundo (cada um traz o seu desenho sobre o mesmo fundo liso).
Saídas: renders/v1/yt_0030_preview_v1_540p15.mp4 e renders/v1/lotes_v1.json (quadro absoluto do início de cada lote).
uso: python montar.py [rodada]"""
import json
import sys
from pathlib import Path

import av
import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
ROOT = U.parents[1]
RODADA = sys.argv[1] if len(sys.argv) > 1 else "v1"
ORDEM = ["PH", "PD1", "PD2", "PD3", "PD3B", "PD4", "PD5", "PA1", "PA2", "PA4", "PA3", "PS"]
K = 6                                    # 0,4 s a 15 fps
FUNDO = np.asarray(Image.open(ROOT / "assets/calculo/fundo_calculo_violeta_liso_960x540.png").convert("RGB"), np.int16)


def quadros(lote):
    c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
    for fr in c.decode(video=0):
        yield fr.to_ndarray(format="rgb24")
    c.close()


def compoe(a, b):
    a16, b16 = a.astype(np.int16), b.astype(np.int16)
    igual = np.abs(a16 - b16).max(axis=2, keepdims=True) <= 6
    soma = np.clip(a16 + b16 - FUNDO, 0, 255)
    return np.where(igual, a16, soma).astype(np.uint8)


def main():
    out_dir = U / "renders" / RODADA
    out_dir.mkdir(parents=True, exist_ok=True)
    saida = out_dir / f"yt_0030_preview_{RODADA}_540p15.mp4"
    o = av.open(str(saida), "w")
    st = o.add_stream("libx264", rate=15)
    st.width, st.height, st.pix_fmt = 960, 540, "yuv420p"
    st.options = {"crf": "18", "preset": "veryfast"}
    n, ini, buf = 0, {}, []

    def escreve(arr):
        nonlocal n
        for p in st.encode(av.VideoFrame.from_ndarray(arr, format="rgb24")):
            o.mux(p)
        n += 1

    for i, lote in enumerate(ORDEM):
        it = quadros(lote)
        ini[lote] = n
        if buf:
            for b in buf:
                escreve(compoe(b, next(it)))
            buf = []
        hold = []
        for a in it:
            hold.append(a)
            if len(hold) > K:
                escreve(hold.pop(0))
        if i < len(ORDEM) - 1:
            buf = hold
        else:
            for a in hold:
                escreve(a)
        print(f"[montar] {lote}: começa no quadro {ini[lote]} ({ini[lote] / 15:.2f} s)")
    for p in st.encode():
        o.mux(p)
    o.close()
    (out_dir / f"lotes_{RODADA}.json").write_text(json.dumps({"quadros": n, "duracao_s": round(n / 15, 2), "inicio": ini}, indent=1), encoding="utf-8")
    print(f"[montar] {saida.name}: {n} quadros = {n / 15:.2f} s = {int(n / 15) // 60}:{n / 15 % 60:05.2f}")


if __name__ == "__main__":
    main()
