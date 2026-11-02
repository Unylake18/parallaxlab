"""vid_0032 v4: escolhe o pedaço M do C06 e confere a função de calor (mesma bilinear do 3D). Uso: python qa/anel_m.py"""
import json
from pathlib import Path
import numpy as np

U = Path(__file__).resolve().parents[1]
C = json.loads((U / 'cena3d' / 'campo.json').read_text(encoding='utf-8'))
nx, ny, CA, CB = C['nx'], C['ny'], C['a_cm'], C['b_cm']
IMED = (np.array(C['P']) + np.array(C['Q'])) / 2
GOTAS = np.array(C['gotas_cm'])


def amostra(x, y):
    fx = np.clip((x + CA / 2) / CA * (nx - 1), 0, nx - 1.001)
    fy = np.clip((y + CB / 2) / CB * (ny - 1), 0, ny - 1.001)
    i, j = int(fx), int(fy)
    a, b = fx - i, fy - j
    k = j * nx + i
    return (IMED[k] * (1 - a) + IMED[k + 1] * a) * (1 - b) + (IMED[k + nx] * (1 - a) + IMED[k + nx + 1] * a) * b


def calor_volta(x, y, n=720):
    r, a0 = np.hypot(x, y), np.arctan2(y, x)
    th = a0 + 2 * np.pi * np.arange(n + 1) / n
    return np.array([amostra(r * np.cos(t), r * np.sin(t)) for t in th])


if __name__ == '__main__':
    print('I: min/max/med', IMED.min().round(2), IMED.max().round(2), np.median(IMED).round(2))
    R = np.hypot(*GOTAS.T)
    res = []
    for g, (x, y) in enumerate(GOTAS):
        if 4.5 < R[g] < 11.5:
            h = calor_volta(x, y)
            res.append((h.std(), g, R[g], h.min(), h.max(), h[:-1].mean()))
    res.sort(reverse=True)
    for s, g, r, lo, hi, me in res[:8]:
        banda = int(((abs(R - r) < .55)).sum())
        print(f'g={g} r={r:.2f} std={s:.3f} min={lo:.2f} max={hi:.2f} media={me:.3f} gotas_na_banda={banda}')
