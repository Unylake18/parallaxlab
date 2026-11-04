"""Render final com voz: emenda os lotes 1080p30 (media_final_<lote>) na ordem do vídeo, com a mesma transição do preview (G13: o lote
anterior apaga até o fundo e o novo acende, sem mudar a duração), e cola a voz de cada âncora (audio/ancoras_v42/<ID>.wav) no início real
dela (log_final_<lote>.txt, linhas [ancora]) + 0,15 s. Vídeo H.264 CRF 14 yuv420p; áudio AAC 192 kb/s.
Saídas: renders/yt0017_com_voz_1080p30.mp4, audio/narracao_v42_montada.wav e renders/capitulos_final.txt.
uso: python montar_final.py"""
import json
import re
import wave
from fractions import Fraction
from pathlib import Path

import av
import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
W, H, FPS, TAXA, ENTRA = 1920, 1080, 30, 44100, 0.15
M = lambda c: U / f"media_final_{c}/videos/cena/1080p30/{c}.mp4"
partes = [("PH", None), ("P1", "ONDE ESTÁ O CENTRO DE MASSA?"), ("P2", "COMO ELE SE MOVE?"), ("P3", "QUE ENERGIA É DO MOVIMENTO RELATIVO?"),
          ("P4", "COMO ACHAR O CENTRO DE MASSA DE UM CORPO INTEIRO?"), ("P5", "EXERCÍCIO 1 · PLACA COM ENTALHE")]
DENTRO = {"P5": {"E2-1": "EXERCÍCIO 2 · REMADOR E ESTACA", "S1": "RESUMO", "EN1": "CENTRO DE MASSA NAS COLISÕES", "EN2": "ENCERRAMENTO"}}
SAI = 10
voz = json.loads((U / "audio/ancoras_v42/duracoes.json").read_text(encoding="utf-8"))
FUNDO = np.asarray(Image.open(U / "fundo_lab.png").convert("RGB").resize((W, H)), dtype=np.float32)
saida = U / "renders" / "yt0017_com_voz_1080p30.mp4"

# 1) vídeo emendado (sem áudio) e as posições de cada âncora no vídeo inteiro
tmp = U / "renders" / "_final_sem_audio.mp4"
refaz = not tmp.exists()                         # já emendado (uma montagem anterior caiu depois do passo 1): só recalcula as marcas
if refaz:
    out = av.open(str(tmp) + ".parcial.mp4", "w")
    s = out.add_stream("libx264", rate=Fraction(FPS))
    s.width, s.height, s.pix_fmt = W, H, "yuv420p"
    s.options = {"crf": "14", "preset": "medium"}
t, marcas, inicio, ultimo = 0, [], {}, None
for nome, cap in partes:
    c = av.open(str(M(nome)))
    total = c.streams.video[0].frames
    n = 0 if refaz else total
    for fr in (c.decode(video=0) if refaz else []):
        img = fr.to_ndarray(format="rgb24")
        if ultimo is not None and n < SAI:
            w = (n + 1) / (SAI + 1)
            img = (img.astype(np.float32) * w + FUNDO * (1 - w) + 0.5).astype(np.uint8)
        if nome != partes[-1][0] and n >= total - SAI:
            w = (total - n) / (SAI + 1)
            img = (img.astype(np.float32) * w + FUNDO * (1 - w) + 0.5).astype(np.uint8)
        for p in s.encode(av.VideoFrame.from_ndarray(img, format="rgb24")):
            out.mux(p)
        n += 1
    ultimo = True
    c.close()
    marcas.append((cap, t / FPS))
    for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", (U / f"log_final_{nome}.txt").read_text(encoding="utf-8", errors="replace")):
        if m.group(1) != "FIM":
            inicio[m.group(1)] = t / FPS + float(m.group(2))
            if m.group(1) in DENTRO.get(nome, {}):
                marcas.append((DENTRO[nome][m.group(1)], t / FPS + float(m.group(2))))
    t += n
if refaz:
    for p in s.encode():
        out.mux(p)
    out.close()
    Path(str(tmp) + ".parcial.mp4").replace(tmp)
dur = t / FPS

# 2) a narração montada: cada âncora começa a falar 0,15 s depois do início dela
pista = np.zeros(int(dur * TAXA) + TAXA, dtype=np.float32)
for a, t0 in inicio.items():
    with wave.open(str(U / f"audio/ancoras_v42/{a}.wav")) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    i = int(round((t0 + ENTRA - voz[a]["ini"]) * TAXA))
    if i < 0:
        x, i = x[-i:], 0
    pista[i:i + len(x)] += x[: len(pista) - i]
pista = np.clip(pista[: int(dur * TAXA)], -1, 1)
with wave.open(str(U / "audio/narracao_v42_montada.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(TAXA); w.writeframes((pista * 32767).astype(np.int16).tobytes())

# 3) junta vídeo (cópia, sem recompressão) e áudio AAC
vi, ai = av.open(str(tmp)), av.open(str(U / "audio/narracao_v42_montada.wav"))
out = av.open(str(saida), "w")
sv = out.add_stream_from_template(vi.streams.video[0])
sa = out.add_stream("aac", rate=TAXA)
sa.bit_rate, sa.layout = 192000, "mono"
for pk in vi.demux(vi.streams.video[0]):
    if pk.dts is not None:
        pk.stream = sv
        out.mux(pk)
for fr in ai.decode(audio=0):
    fr.pts = None
    for pk in sa.encode(fr):
        out.mux(pk)
for pk in sa.encode():
    out.mux(pk)
out.close(); vi.close(); ai.close()
tmp.unlink()
(U / "renders" / "capitulos_final.txt").write_text(
    "\n".join(f"{int(t0 // 60)}:{int(t0 % 60):02d} {cap or 'ABERTURA'}" for cap, t0 in marcas) + "\n", encoding="utf-8")
print(json.dumps({"saida": str(saida), "duracao_s": round(dur, 2), "ancoras": len(inicio)}, ensure_ascii=False))
