"""yt_0020 v8 §1.4 · dx por camada no teste sintético (só estrelas, 960x540, 15 fps): mediana temporal = fundo; correlação de fase (lag 5 quadros) no resíduo."""
import glob, numpy as np, av, sys
S = "C:/Users/Pichau/AppData/Local/Temp/claude/2da2ce851f93e9b8/bceeadd8-b660-49b0-9a11-88f8924400be/scratchpad"
PXU = 60.0  # 960 px / 16 u (frame_width do template horizontal)
esp = {0: 0.40, 1: 0.75, 2: 1.25}
out = []
for T in (0, 780, 1560):
    for C in (0, 1, 2):
        p = glob.glob(f"{S}/media_c{T}_{C}/videos/teste_fundo/540p15/c.mp4")[0]
        c = av.open(p)
        fr = np.stack([f.to_ndarray(format="gray").astype(np.float32) for f in c.decode(video=0)])
        res = np.clip(fr - np.median(fr, axis=0), 0, None)
        lag, vals = 5, []
        for i in range(0, len(fr) - lag, 3):
            a, b = res[i + lag], res[i]
            F = np.fft.fft2(a) * np.conj(np.fft.fft2(b)); F /= np.abs(F) + 1e-9
            r = np.fft.ifft2(F).real
            iy, ix = np.unravel_index(np.argmax(r), r.shape)
            if r.max() < 0.08: continue
            if ix > r.shape[1] // 2: ix -= r.shape[1]
            vals.append(ix / lag)
        v = np.array(vals)
        alvo = -esp[C] * PXU / 15
        out.append((T, C, len(v), float(np.median(v)), alvo, float(np.mean(v < -0.3)), float(np.std(v))))
lin = ["T0(s) camada n_med dx_mediano(px/quadro) esperado razao  frac_esq  desvio"]
for T, C, n, m, al, fe, sd in out:
    lin.append(f"{T:5d} {C} {n:3d} {m:8.2f} {al:8.2f} {m/al:6.2f} {fe:5.2f} {sd:5.2f}")
print("\n".join(lin))
open("videos_longos/yt_0020_cinematica_angular/renders/v8/fundo_camadas.txt", "w").write("\n".join(lin) + "\n")
