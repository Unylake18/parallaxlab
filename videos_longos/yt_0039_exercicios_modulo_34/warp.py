"""yt_0039 · fechamento §3: sincronia por reamostragem do tempo do VÍDEO (nunca da voz). Os lotes renderizados (540p15 ou 1080p30) são emendados e o
tempo é remapeado por partes: cada gatilho (e cada início de âncora) do log tem um instante na tela (t_tela) e outro na voz (t_voz, alinhamento forçado);
entre dois nós o vídeo é reamostrado com velocidade constante (Δt_tela / Δt_voz), repetindo ou pulando quadros. Os nós atrasados passam a cair na
palavra (±1 quadro); o conteúdo e a ordem dos eventos não mudam.
uso: python warp.py 540|1080 [saida.mp4]   (RODADA no ambiente; 540 lê media_<L>/.../540p15, 1080 lê media1080_<L>/.../1080p30 e log1080_<L>.txt)"""
import json
import re
import subprocess
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
RES = sys.argv[1] if len(sys.argv) > 1 else "540"
FPS = 15 if RES == "540" else 30
LOTES = ["PH", "PA", "PE1", "PE2", "PE3", "PE4", "PE5", "PE6", "PS"]
PRE = "log_" if RES == "540" else "log1080_"
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]


def arq(c):
    return U / (f"media_{c}/videos/cena/540p15/{c}.mp4" if RES == "540" else f"media1080_{c}/videos/cena/1080p30/{c}.mp4")


# 1) início de cada lote na emenda e nós (t_tela, t_voz)
ini, t = {}, 0.0
dur = {}
for c in LOTES:
    with av.open(str(arq(c))) as k:
        s = k.streams.video[0]
        d = float(s.frames / FPS) if s.frames else float(k.duration / 1e6)
    ini[c], dur[c] = t, d
    t += d
T_TOTAL = t
nos = [(0.0, 0.0)]
for c in LOTES:
    log = (U / f"{PRE}{c}.txt").read_text(encoding="utf-8", errors="replace")
    q0 = {}
    for l in log.splitlines():
        m = re.match(r"\[ancora\] (\S+) ([0-9.]+)", l)
        if m:
            q0[m.group(1)] = float(m.group(2))
            continue
        m = re.match(r"\[gatilho\] (\S+)\s+([-0-9.]+)s \(alvo\s+([-0-9.]+)s, atraso ([-+0-9.]+)s\) (.*)", l)
        if m:
            a_, rel, fr = m.group(1), float(m.group(2)), m.group(5)
            fala = ANC[a_]["fala"].split()
            al = re.findall(r"\w+", fr.lower())
            k = next((i for i in range(len(fala)) if fala[i:i + len(al)] == al), None)
            if k is None:
                continue
            nos.append((ini[c] + q0.get(a_, 0.0) + rel, ANC[a_]["ini"] + ANC[a_]["t"][k]))
WAV_FIM = ANC[list(ANC)[-1]]["fim"]
nos.append((T_TOTAL, WAV_FIM))
nos.sort(key=lambda x: x[1])
# monotonia estrita: t_tela cresce com t_voz (descarta nós que andam para trás)
mono = [nos[0]]
for tt, tv in nos[1:]:
    if tt > mono[-1][0] + 1e-3 and tv > mono[-1][1] + 1e-3:
        mono.append((tt, tv))
# saltos > 3,5× (conteúdo comprimido demais): funde o nó do fim do trecho com o seguinte
while True:
    v_ = [(mono[i + 1][0] - mono[i][0]) / (mono[i + 1][1] - mono[i][1]) for i in range(len(mono) - 1)]
    pior = max(range(len(v_)), key=lambda i: v_[i])
    if v_[pior] <= 3.5 or pior + 1 >= len(mono) - 1:
        break
    del mono[pior + 1]
tt_ = np.array([a for a, _ in mono])
tv_ = np.array([b for _, b in mono])
vel = np.diff(tt_) / np.diff(tv_)
print(f"nós {len(mono)} de {len(nos)}; velocidade do vídeo entre nós: mín {vel.min():.2f} · máx {vel.max():.2f} · mediana {np.median(vel):.2f}")
(U / "qa").mkdir(exist_ok=True)
L = [f"WARP {RES}p: nós {len(mono)}; velocidade mín {vel.min():.2f} máx {vel.max():.2f}", "", "trechos com velocidade > 1,5 ou < 0,7 (t_voz inicial · velocidade · duração na voz):"]
for i, v_ in enumerate(vel):
    if v_ > 1.5 or v_ < 0.7:
        L.append(f"  {tv_[i]:8.2f} s · ×{v_:.2f} · {tv_[i + 1] - tv_[i]:.2f} s")
(U / "qa" / f"warp_{RES}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")

# 2) reamostragem: quadro de saída k (tempo de voz k/FPS) ← quadro de origem round(t_tela · FPS)
n_out = int(round(WAV_FIM * FPS))
src_idx = np.rint(np.interp(np.arange(n_out) / FPS, tv_, tt_) * FPS).astype(int)
src_idx = np.clip(src_idx, 0, int(round(T_TOTAL * FPS)) - 1)
out = Path(sys.argv[2]) if len(sys.argv) > 2 else U / "renders" / "final" / f"yt_0039_sem_audio_{RES}p{FPS}_warp.mp4"
W, H = (960, 540) if RES == "540" else (1920, 1080)
crf, preset = ("20", "veryfast") if RES == "540" else ("14", "slow")
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
                        "-pix_fmt", "yuv420p", "-crf", crf, "-preset", preset, str(out)], stdin=subprocess.PIPE)
# passada única sobre a emenda: lê os quadros em ordem e escreve o quadro de origem pedido (índices não decrescentes)
quadro, pos = None, -1
def fonte():
    for c in LOTES:
        cont = av.open(str(arq(c)))
        for f in cont.decode(video=0):
            yield f.to_ndarray(format="rgb24")
        cont.close()
gen = fonte()
for si in src_idx:
    while pos < si:
        try:
            quadro = next(gen)
        except StopIteration:
            break
        pos += 1
    enc.stdin.write(quadro.tobytes())
enc.stdin.close()
enc.wait()
print(out, f"{n_out / FPS:.2f} s ({n_out} quadros)")
