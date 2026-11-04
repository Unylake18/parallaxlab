"""Tira as pausas entre âncoras do master (pedido do Kaio, 2026-11-03: o vídeo não ficava fluido). Cada âncora tinha 0,9-1,8 s de
silêncio no fim (respiro de ancoras_voz.py); aqui o silêncio vira 0,35 s (0,5 s em troca de capítulo, 0,6 s nas pausas protegidas).
O corte acontece só dentro do silêncio e tira o mesmo tempo da imagem e da voz, então a sincronia antes e depois de cada pausa não muda.
Imagem: corta entre dois quadros iguais (tela parada) dentro do silêncio; onde a tela está em movimento (cavalo, molas, cacos), acelera
o trecho em 2x, tirando um quadro sim, um não, em vez de pular.
Entradas: renders/yt0017_com_voz_1080p30.mp4, audio/narracao_v42_montada.wav, ancoras.json, renders/legenda - yt0017.srt,
renders/capitulos_final.txt. Saídas: renders/yt_0017_master_1080p30.mp4 (H.264 CRF 14, AAC 192k), audio/narracao_final.wav,
renders/legenda - yt0017 - fluido.srt, renders/capitulos_fluido.txt, renders/cortes_pausas.json.
uso: python cortar_pausas.py"""
import json
import re
import wave
from fractions import Fraction
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
FPS, TAXA, MARGEM, LIMIAR = 30, 44100, 0.06, 40
FICA = {0.75: 0.35, 1.2: 0.5, 1.4: 0.6}               # respiro da âncora → silêncio que fica
ENT = U / "renders/yt0017_com_voz_1080p30.mp4"
SAI = U / "renders/yt_0017_master_1080p30.mp4"

# 1) silêncios ≥ 0,6 s na voz montada (janelas de 20 ms abaixo de -35 dB)
with wave.open(str(U / "audio/narracao_v42_montada.wav")) as w:
    voz = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).copy()
x = voz.astype(np.float32) / 32768
j20 = int(TAXA * 0.02)
e = 20 * np.log10(np.sqrt((x[: len(x) // j20 * j20].reshape(-1, j20) ** 2).mean(1)) + 1e-9) < -35
sil, i = [], 0
while i < len(e):
    k = i
    while k < len(e) and e[k]:
        k += 1
    if (k - i) * 0.02 >= 0.6:
        sil.append((i * 0.02, (k - i) * 0.02))
    i = max(k, i + 1)

# respiro da âncora que termina em cada silêncio
a = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
t0, fim = 0.0, []
for k in a["ordem"]:
    v = a["ancoras"][k]
    fim.append((t0 + v["voz_ini"] + v["voz_s"], v["respiro"]))
    t0 += v["dur"]


def fica(t):
    d, r = min((abs(t - f), r) for f, r in fim)
    return FICA[r] if d < 0.4 else 0.35


# 2) quadros que saem em cada silêncio
c = av.open(str(ENT)); s = c.streams.video[0]; s.thread_type = "AUTO"
cortes, tira = [], set()
for t, d in sil:
    lim = int((d - fica(t)) * FPS)
    if lim <= 0:
        continue
    lo, hi = t + MARGEM, t + d - MARGEM
    c.seek(int(max(0, lo - 1) / s.time_base), stream=s)
    q = []
    for f in c.decode(s):
        ft = float(f.pts * s.time_base)
        if ft < lo - 1e-3:
            continue
        if ft > hi:
            break
        q.append((round(ft * FPS), f.to_ndarray(format="gray")[::4, ::4].astype(np.int16)))
    par = (0, 0)
    for p in range(len(q)):
        for r in range(min(len(q) - 1, p + lim), p, -1):
            if r - p <= par[0]:
                break
            if (np.abs(q[p][1] - q[r][1]) > 6).sum() < LIMIAR:
                par = (r - p, p)
                break
    if par[0] >= min(lim, 0.6 * lim):             # tela parada (ou que volta ao mesmo quadro): corte seco
        fora, modo = [q[par[1]][0] + n for n in range(1, par[0] + 1)], "corte"
    else:                                         # tela em movimento: 2x, um quadro sim, um não
        n = min(lim, len(q) // 2)
        meio = (len(q) - 2 * n) // 2
        fora, modo = [q[meio + 2 * m + 1][0] for m in range(n)], "2x"
    tira.update(fora)
    cortes.append({"t": round(t, 2), "silencio": round(d, 2), "tirado": round(len(fora) / FPS, 3), "fica": round(d - len(fora) / FPS, 2),
                   "modo": modo})
c.close()

# 3) voz: tira o mesmo tempo, num pedaço só, do meio de cada silêncio
corte_voz, partes, ult = [], [], 0
for (t, d), ct in zip([x for x in sil if any(abs(x[0] - y["t"]) < 0.01 for y in cortes)], cortes):
    n = round(ct["tirado"] * TAXA)
    i0 = int((t + d / 2) * TAXA) - n // 2
    partes.append(voz[ult:i0]); ult = i0 + n
    corte_voz.append((i0 / TAXA, n / TAXA))
partes.append(voz[ult:])
nova = np.concatenate(partes)
with wave.open(str(U / "audio/narracao_final.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(TAXA); w.writeframes(nova.tobytes())


def novo(t):                                       # tempo do vídeo antigo → tempo no vídeo sem pausas
    return t - sum(min(max(t - i0, 0), n) for i0, n in corte_voz)


# 4) legenda e capítulos no tempo novo
def ts(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def le(m):
    h, mi, se, ms = map(int, re.split("[:,]", m))
    return h * 3600 + mi * 60 + se + ms / 1000


srt = (U / "renders/legenda - yt0017.srt").read_text(encoding="utf-8")
srt = re.sub(r"(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})", lambda m: f"{ts(novo(le(m[1])))} --> {ts(novo(le(m[2])))}", srt)
(U / "renders/legenda - yt0017 - fluido.srt").write_text(srt, encoding="utf-8")
cap = []
for ln in (U / "renders/capitulos_final.txt").read_text(encoding="utf-8").splitlines():
    mi, se, nome = re.match(r"(\d+):(\d+) (.*)", ln).groups()
    t = novo(int(mi) * 60 + int(se))
    cap.append(f"{int(t // 60)}:{int(t % 60):02d} {nome}")
(U / "renders/capitulos_fluido.txt").write_text("\n".join(cap) + "\n", encoding="utf-8")

# 5) vídeo: recodifica sem os quadros tirados (CRF 14) e junta a voz nova
vi, ai = av.open(str(ENT)), av.open(str(U / "audio/narracao_final.wav"))
out = av.open(str(SAI) + ".parcial.mp4", "w")
sv = out.add_stream("libx264", rate=Fraction(FPS))
sv.width, sv.height, sv.pix_fmt = 1920, 1080, "yuv420p"
sv.options = {"crf": "14", "preset": "medium"}
sa = out.add_stream("aac", rate=TAXA)
sa.bit_rate, sa.layout = 192000, "mono"
vi.streams.video[0].thread_type = "AUTO"
n = 0
for k, f in enumerate(vi.decode(video=0)):
    if k in tira:
        continue
    g = av.VideoFrame.from_ndarray(f.to_ndarray(format="yuv420p"), format="yuv420p")
    n += 1
    for p in sv.encode(g):
        out.mux(p)
for p in sv.encode():
    out.mux(p)
for f in ai.decode(audio=0):
    f.pts = None
    for p in sa.encode(f):
        out.mux(p)
for p in sa.encode():
    out.mux(p)
out.close(); vi.close(); ai.close()
Path(str(SAI) + ".parcial.mp4").replace(SAI)
(U / "renders/cortes_pausas.json").write_text(json.dumps(cortes, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"saida": str(SAI), "quadros": n, "duracao_s": round(n / FPS, 2), "voz_s": round(len(nova) / TAXA, 2),
                  "cortes": len(cortes), "tirado_s": round(sum(c["tirado"] for c in cortes), 2),
                  "em_2x": [c["t"] for c in cortes if c["modo"] == "2x"]}, ensure_ascii=False))
