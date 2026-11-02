"""Campo do forno do vid_0032 (C05 e C06 em Three.js): mistura de quatro modos reais de uma cavidade retangular (handoff v2 §6.1).

Cavidade a × b × h = 0,366 × 0,31 × 0,22 m; plano do chocolate z = 0,03 m. Determinístico (nada aleatório sem semente fixa).
exporta() grava em cena3d/:
  campo.json   grades P = |Re E|², Q = |Im E|², R = Re E · Im E (123 × 104, normalizadas pelo máximo de ⟨I⟩), para
               ⟨I⟩ = (P + Q)/2 e I(t) = P cos²ωt + Q sen²ωt − 2R senωt cosωt; e as 234 gotas (x, y em cm, centro do forno).
  relevo.png   textura do relevo: colormap laranja do v1 em ⟨I⟩ e curvas de nível a cada 0,2.
Conferência e exportação:  uv run python videos/vid_0032_microondas_chocolate/mapa_calor.py
"""
import json
from functools import lru_cache
from pathlib import Path

import numpy as np

A, B, H, Z = 0.366, 0.31, 0.22, 0.03
NX, NY = 367, 311
C_LUZ = 2.998e8
# (tipo, m, n, p, amplitude, fase)
MODOS = (('TE', 2, 2, 3, .74, 1.26 * np.pi), ('TE', 1, 4, 2, .68, 1.55 * np.pi),
         ('TM', 1, 5, 0, .55, 1.82 * np.pi), ('TE', 5, 0, 2, .54, .73 * np.pi))
PARADAS = ((0.0, '#120A08'), (0.55, '#FF7A3D'), (1.0, '#FFE3CF'))
GAMA = 0.8
NIVEL, COR_NIVEL = 0.2, (255, 201, 168)
R_GOTAS, PASSO, JITTER, SEMENTE = 12.8, 1.6, 0.25, 2
UNIT = Path(__file__).resolve().parent


def frequencia(m, n, p):
    return C_LUZ / 2 * np.sqrt((m / A) ** 2 + (n / B) ** 2 + (p / H) ** 2)


def campo(x, y, z=Z):
    """Campo complexo (Ex, Ey, Ez) da mistura nos pontos (x, y) em metros (origem num canto do piso)."""
    E = [np.zeros(np.broadcast(x, y).shape, complex) for _ in range(3)]
    for tipo, m, n, p, amp, fase in MODOS:
        kx, ky, kz = m * np.pi / A, n * np.pi / B, p * np.pi / H
        kc2 = kx ** 2 + ky ** 2
        cx, sx, cy, sy = np.cos(kx * x), np.sin(kx * x), np.cos(ky * y), np.sin(ky * y)
        if tipo == 'TM':
            comp = (-(kx * kz / kc2) * cx * sy * np.sin(kz * z), -(ky * kz / kc2) * sx * cy * np.sin(kz * z), sx * sy * np.cos(kz * z))
        else:
            kc = np.sqrt(kc2)
            comp = ((ky / kc) * cx * sy * np.sin(kz * z), -(kx / kc) * sx * cy * np.sin(kz * z), 0 * x)
        w = amp * np.exp(1j * fase)
        for i in range(3):
            E[i] = E[i] + w * comp[i]
    return E


def pqr(x, y):
    E = campo(x, y)
    return (sum(e.real ** 2 for e in E), sum(e.imag ** 2 for e in E), sum(e.real * e.imag for e in E))


@lru_cache(None)
def grade(nx=NX, ny=NY):
    xs, ys = np.linspace(0, A, nx), np.linspace(0, B, ny)
    P, Q, R = pqr(*np.meshgrid(xs, ys))
    return xs, ys, P, Q, R


def media(nx=NX, ny=NY):
    _, _, P, Q, _ = grade(nx, ny)
    return (P + Q) / 2


@lru_cache(None)
def IMAX():
    return media().max()


def colorir(v):
    v = np.clip(v, 0, 1) ** GAMA
    pos = [p for p, _ in PARADAS]
    return np.stack([np.interp(v, pos, [int(c[1 + 2 * k:3 + 2 * k], 16) for _, c in PARADAS]) for k in range(3)], -1)


def gotas():
    """Grade hexagonal de passo 1,6 cm, jitter ±0,25 cm (semente fixa), raio útil 12,8 cm; (x, y) em cm a partir do centro."""
    rng = np.random.default_rng(SEMENTE)
    pts = []
    for j in range(-10, 11):
        for i in range(-10, 11):
            x, y = (i + (j % 2) / 2) * PASSO, j * PASSO * np.sqrt(3) / 2
            if i or j:                                          # a gota do centro fica exatamente no centro
                x, y = x + rng.uniform(-JITTER, JITTER), y + rng.uniform(-JITTER, JITTER)
            if np.hypot(x, y) <= R_GOTAS:
                pts.append((x, y))
    p = np.array(pts)
    p = p[np.argsort(np.hypot(*p.T))]
    return p


def i_media_cm(x, y):
    """⟨I⟩ normalizado em pontos dados em cm a partir do centro do piso."""
    P, Q, _ = pqr(A / 2 + np.asarray(x) / 100, B / 2 + np.asarray(y) / 100)
    return (P + Q) / 2 / IMAX()


def exporta():
    _, _, P, Q, R = grade(123, 104)
    k = IMAX()
    g = gotas()
    dados = {'nota': 'gerado por mapa_calor.py; linha j = y de -b/2 a +b/2 (fundo do forno), coluna i = x de -a/2 a +a/2',
             'a_cm': A * 100, 'b_cm': B * 100, 'nx': 123, 'ny': 104,
             'P': np.round(P / k, 4).ravel().tolist(), 'Q': np.round(Q / k, 4).ravel().tolist(), 'R': np.round(R / k, 4).ravel().tolist(),
             'gotas_cm': np.round(g, 3).tolist()}
    (UNIT / 'cena3d' / 'campo.json').write_text(json.dumps(dados), encoding='utf-8')
    # textura do relevo em 2× (734 × 622): colormap + curvas de nível (3 px), linha 0 = y = −b/2 (frente), como a UV do plano.
    v = media(734, 622) / k
    rgb = colorir(v)
    L = np.floor(v / NIVEL)
    borda = np.zeros(v.shape, bool)
    borda[:, 1:] |= L[:, 1:] != L[:, :-1]
    borda[1:, :] |= L[1:, :] != L[:-1, :]
    for _ in range(1):
        b2 = borda.copy()
        b2[1:] |= borda[:-1]; b2[:-1] |= borda[1:]; b2[:, 1:] |= borda[:, :-1]; b2[:, :-1] |= borda[:, 1:]
        borda = b2
    rgb[borda] = COR_NIVEL
    # alfa: vales quase transparentes (as gotas aparecem), morros a ~0,7; × opacidade 0,8 do material ≈ 0,55 nos morros
    alfa = np.where(borda, .95, .12 + .58 * np.clip(v, 0, 1) ** GAMA) * 255
    from PIL import Image
    Image.fromarray(np.dstack([rgb, alfa])[::-1].round().astype(np.uint8)).save(UNIT / 'cena3d' / 'relevo.png')   # linha 0 em cima = fundo
    return len(g)


if __name__ == '__main__':
    for t, m, n, p, *_ in MODOS:
        print(f'{t}({m},{n},{p}): {frequencia(m, n, p) / 1e9:.3f} GHz')
    xs, ys, *_ = grade()
    I = media() / IMAX()
    picos = [(xs[i] * 100, ys[j] * 100) for j in range(1, NY - 1) for i in range(1, NX - 1)
             if I[j, i] > .35 and I[j, i] == I[j - 1:j + 2, i - 1:i + 2].max()]
    Pp = np.array(picos)
    viz = np.array([np.sort(np.hypot(*(Pp - q).T))[1] for q in Pp])
    print(f'{len(picos)} picos > 0,35; vizinho mais próximo {viz.min():.1f} a {viz.max():.1f} cm (mediana {np.median(viz):.1f})')
    g = gotas()
    print(f'{len(g)} gotas; centro em {g[0]}')
    # média de ⟨I⟩ ao longo de uma volta do prato, por gota, agrupada por anel
    ang = np.linspace(0, 2 * np.pi, 720, endpoint=False)
    r, th0 = np.hypot(*g.T), np.arctan2(g[:, 1], g[:, 0])
    volta = i_media_cm(r[:, None] * np.cos(th0[:, None] + ang), r[:, None] * np.sin(th0[:, None] + ang)).mean(1)
    for a, b in ((0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 12), (12, 13)):
        s = (r >= a) & (r < b)
        print(f'anel {a:2d}–{b:2d} cm: média {volta[s].mean():.2f}, dispersão {volta[s].max() - volta[s].min():.2f} ({s.sum()} gotas)')
    assert abs(volta[0] - i_media_cm(0, 0)) < 1e-9, 'a gota do centro não sai do lugar'
    print('exportadas', exporta(), 'gotas → cena3d/campo.json, cena3d/relevo.png')
