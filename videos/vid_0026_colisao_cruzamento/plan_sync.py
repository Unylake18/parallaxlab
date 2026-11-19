"""Plano de sincronização do vid_0026: une nat.json (instante natural de cada âncora na cena, MEDIR=1) e voz_ancoras.json
(instante de cada frase na voz). Para cada trecho entre âncoras: fator de ritmo f = (duração da voz / duração da cena), limitado a
[FMIN, FMAX]; se a cena ainda for mais longa que a voz, o áudio ganha uma pausa antes da frase seguinte. A imagem antecipa a voz
em LEAD s. Saída: sync.json (T e f por âncora, para SYNC=sync.json) e audio/narracao_sync.wav (voz recolocada nos tempos T)."""
import json
import wave
from pathlib import Path

import numpy as np

PASTA = Path(__file__).absolute().parent
FMIN, FMAX, LEAD, FOLGA = 0.5, 2.2, 0.15, 0.25
# trechos sem fala própria que podem acelerar mais, para não abrir pausa no meio da voz
# (violeta: resultados indo para as setas/coluna e km/h; kantes: K_antes inteiro antes de "depois, ..."; direcao: fim do C02)
FMIN_TRECHO = {"violeta": 0.4, "kantes": 0.4, "direcao": 0.45}
nat = json.loads((PASTA / "nat.json").read_text(encoding="utf-8"))
voz = json.loads((PASTA / "voz_ancoras.json").read_text(encoding="utf-8"))
nomes = [k for k in nat if not k.startswith("_")]
assert nomes == [k for k in voz if not k.startswith("_")], "âncoras da cena e da voz em ordens diferentes"
V = [voz[n]["ini"] for n in nomes] + [voz["_fim_voz"]]
N = [nat[n] for n in nomes] + [nat["_fim"]]
T, f, pausas = [max(V[0] - LEAD, 0.0)], [], []
for i in range(len(nomes)):
    Ds, Dv = N[i + 1] - N[i], V[i + 1] - V[i]
    if i == len(nomes) - 1:                     # cartão final: ritmo natural; a voz termina dentro dele
        f.append(1.0)
        break
    # FOLGA: cada play arredonda para quadros inteiros; a cena mira chegar um pouco antes da frase e espera por ela
    fi = min(max((Dv - FOLGA) / Ds, FMIN_TRECHO.get(nomes[i], FMIN)), FMAX) if Ds > 1e-6 else 1.0
    f.append(round(fi, 4))
    passo = max(Dv, Ds * fi + FOLGA)
    pausas.append(round(passo - Dv, 3))
    T.append(T[-1] + passo)
A = [t + LEAD for t in T]                       # onde cada frase começa no áudio final
fim_video = T[-1] + (N[-1] - N[-2]) * f[-1]
sync = {"ancoras": {n: {"T": round(T[i], 4), "f": f[i]} for i, n in enumerate(nomes)}, "lead": LEAD,
        "fim_video": round(fim_video, 3)}
(PASTA / "sync.json").write_text(json.dumps(sync, indent=1), encoding="utf-8")

# áudio: cada frase recolocada de modo que o início da sua primeira palavra caia em A. O corte entre frases fica no ponto
# mais silencioso do intervalo entre a última palavra de uma e a primeira da outra (o alinhamento marca a palavra uns
# milissegundos depois de o som começar: cortar em cima do início dela partia a palavra — o "engasgo"), com fade curto.
w = wave.open(str(PASTA / "audio" / "narracao_v3_curta.wav"))
sr, params = w.getframerate(), w.getparams()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
w.close()


def corte_silencioso(t0, t1, jan=0.010):
    """Centro da janela de 10 ms com menor energia em [t0, t1]."""
    a, b, n = int(t0 * sr), int(t1 * sr), int(jan * sr)
    if b - a <= n:
        return (a + b) // 2
    e = np.convolve(x[a:b] ** 2, np.ones(n) / n, mode="valid")
    return a + int(np.argmin(e)) + n // 2


cortes = [0]
for i in range(1, len(nomes)):
    cortes.append(corte_silencioso(voz[nomes[i - 1]]["fim"], voz[nomes[i]]["ini"]))
cortes.append(len(x))
FADE = int(0.008 * sr)
total = int((fim_video + 0.5) * sr)
y = np.zeros(total, dtype=np.float32)
for i in range(len(nomes)):
    seg = x[cortes[i]:cortes[i + 1]].copy()
    if i > 0:
        seg[:FADE] *= np.linspace(0, 1, FADE)
    if i < len(nomes) - 1:
        seg[-FADE:] *= np.linspace(1, 0, FADE)
    ini = int(A[i] * sr) - (int(V[i] * sr) - cortes[i]) if i > 0 else int((A[0] - V[0]) * sr)
    ini = max(ini, 0)
    k = max(0, min(len(seg), total - ini))
    y[ini:ini + k] += seg[:k]
y = np.clip(y, -32768, 32767).astype(np.int16)
o = wave.open(str(PASTA / "audio" / "narracao_sync.wav"), "wb")
o.setparams(params)
o.writeframes(y.tobytes())
o.close()
print(f"vídeo {fim_video:.1f} s (voz pura {V[-1]:.1f} s; pausas inseridas {sum(pausas):.1f} s)")
for i, n in enumerate(nomes[:-1]):
    Ds, Dv = N[i + 1] - N[i], V[i + 1] - V[i]
    marca = "  ← pausa" if pausas[i] > 0.05 else ("  ← espera" if Dv > Ds * f[i] + 0.05 else "")
    print(f"{n:10s} T={T[i]:6.2f}  cena {Ds:5.2f}  voz {Dv:5.2f}  f={f[i]:4.2f}  pausa {pausas[i]:4.2f}{marca}")
