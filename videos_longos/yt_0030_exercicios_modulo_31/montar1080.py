"""yt_0030 · handoff final §7.2 (adaptado do montar.py): emenda os 12 lotes 1080p30 SEM PERDAS (media1080_<C>, CRF=0) com a COSTURA de 0,4 s
(K = 12 quadros a 30 fps: os últimos 12 quadros do lote N compostos com os 12 primeiros do lote N+1; onde os dois quadros são iguais fica o
quadro, onde diferem N + (N+1) − fundo) e codifica UMA vez: libx264, yuv420p, CRF 14, preset slow.
Saídas: renders/yt_0030_sem_audio_1080p30.mp4 e renders/lotes_final_1080.json (quadro absoluto do início de cada lote).
Depois: uv run python videos/montar_master.py <sem_audio> audio/narracao_final.wav renders/yt_0030_master_final_1080p30.mp4"""
import json
from pathlib import Path

import av
import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
ROOT = U.parents[1]
ORDEM = ["PH", "PD1", "PD2", "PD3", "PD3B", "PD4", "PD5", "PA1", "PA2", "PA4", "PA3", "PS"]
FPS, K, W, H = 30, 12, 1920, 1080
FUNDO = np.asarray(Image.open(ROOT / "assets/calculo/fundo_calculo_violeta_liso_1920x1080.png").convert("RGB"), np.int16)


def quadros(lote):
    c = av.open(str(U / f"media1080_{lote}/videos/cena/1080p30/{lote}.mp4"))
    for fr in c.decode(video=0):
        yield fr.to_ndarray(format="rgb24")
    c.close()


def compoe(a, b):
    a16, b16 = a.astype(np.int16), b.astype(np.int16)
    igual = np.abs(a16 - b16).max(axis=2, keepdims=True) <= 6
    soma = np.clip(a16 + b16 - FUNDO, 0, 255)
    return np.where(igual, a16, soma).astype(np.uint8)


def main():
    saida = U / "renders" / "yt_0030_sem_audio_1080p30.mp4"
    o = av.open(str(saida), "w")
    st = o.add_stream("libx264", rate=FPS)
    st.width, st.height, st.pix_fmt = W, H, "yuv420p"
    st.options = {"crf": "14", "preset": "slow"}
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
        print(f"[montar1080] {lote}: começa no quadro {ini[lote]} ({ini[lote] / FPS:.2f} s)", flush=True)
    for p in st.encode():
        o.mux(p)
    o.close()
    j = {"quadros": n, "duracao_s": round(n / FPS, 3), "fps": FPS, "inicio": ini}
    (U / "renders" / "lotes_final_1080.json").write_text(json.dumps(j, indent=1), encoding="utf-8")
    d = U / "renders" / "final1080"                      # cópia no formato que o qa_sync.py lê (rodada final1080)
    d.mkdir(parents=True, exist_ok=True)
    (d / "lotes_final1080.json").write_text(json.dumps(j, indent=1), encoding="utf-8")
    print(f"[montar1080] {saida.name}: {n} quadros = {n / FPS:.2f} s = {int(n / FPS) // 60}:{n / FPS % 60:05.2f}")


if __name__ == "__main__":
    main()
