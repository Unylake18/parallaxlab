"""vid_0033 v6 — tempos, câmera, pistão, ladrilho A e preenchimento V (fonte única do timeline.json e do cena.py).
Tempos do Anexo A do handoff v6 (narração v4, estimativa a 2,85 palavras/s). Hook simples: a caixa com as partículas desde o quadro 0."""
import numpy as np

import os
FPS = int(os.environ.get('FPS', 15))             # 15 no preview; 30 no render final (1080×1920/30)
NQ = 2611 * FPS // 15                                   # 174,07 s = voz (171,04 s, narracao_v4.wav) + tela final até 174,07 s
DURACAO = NQ / FPS
CENAS = {'C01': 0.0, 'C02': 10.55, 'C03': 33.95, 'C04': 61.1, 'C05': 97.75, 'C06': 134.8, 'C07': 149.45, 'CTA': 171.05, 'FIM': DURACAO}
R_ESF = .08                                 # raio da esfera: a caixa é desenhada em ±(1 + R_ESF); os CENTROS ficam em [−1, 1]
BALAO = dict(R=1.55, esc_y=1.1)             # (balão do v5: mantido no 3D, mas sempre oculto — BAL = 0)


def sh(t):
    return t


T_BATIDA = 22.55                         # batida acompanhada no C02 ("ela bate e volta")

# zonas em px (540×960) — Manim: y = (480 − py)/60, x = (px − 270)/60
Z = dict(selos=(0, 80), z3d=(60, 400), eq=(410, 750), leg=(760, 840), chip=(850, 930), margem=24)

# pistão (C07): Lx = comprimento do recipiente em x (2 → 1). Os contadores usam janela deslizante de W s (mesmo tamanho nos dois estados).
PIST = dict(t_comp0=150.0, t_comp1=151.6, W=4.0, estado1=(140.8, 149.9), estado2=(155.7, 160.7))

# taxa do tempo da simulação τ por segundo de vídeo (câmera lenta em volta da batida do C02)
TAXA = [(0, 1.0), (19.9, 1.0), (21.3, .16), (22.55, .12), (23.75, .05), (33.4, .05), (34.2, .6), (61.0, .6), (63.5, 1.0)]
TAXA_HOOK = [(0, 1.0), (10, 1.0)]

DEF = dict(az=0, el=0, D=12.7, fov=36, dy=.266, cx=0, op=1, ring=0, mix=0, px=0, py=0, pz=0, lx=0, ly=0, lz=0, ghost=0, pist=0)


def K(t, **kw):
    d = dict(DEF)
    d.update(kw, t=t)
    return d


POSE5 = dict(az=22, el=14, D=12.7, dy=.266)   # C05–C06: caixa com tamanho decente (≈ 280 px), em Z_3D, com baixa opacidade
CAM = [
    K(0.0, az=30, el=18),                                          # hook: a caixa já no primeiro quadro, órbita lenta
    K(10.55, az=0, el=0),                                          # vista frontal na entrada do C02
    K(16.1, ring=0),
    K(16.6, ring=1),                                               # molécula acompanhada ("massa")
    K(70.3, ring=1),
    K(70.9, op=.14, ring=0, **POSE5),                               # C04: o 3D recua para trás do diagrama (sempre em movimento, esferas ≤ 20 %)
    K(97.4, op=.14, **POSE5),
    K(98.3, op=.35, **POSE5),                                      # C05: a caixa volta (≈ 280 px)
    K(112.3, op=.35, **POSE5),
    K(113.1, op=.14, **POSE5),                                      # gráfico PV/N × T na frente; a caixa continua ao fundo, mais fraca
    K(121.2, op=.14, **POSE5),
    K(122.0, op=.35, **POSE5),                                     # depois do gráfico a caixa volta e fica até o C07
    K(148.6, op=.35, **POSE5),
    K(149.45, cx=.1, pist=1),                                      # C07: recipiente com pistão (vista frontal)
    K(PIST['t_comp1'], cx=-.4, pist=1),                            # a câmera acompanha o centro do recipiente quando o pistão chega a V/2
    K(CENAS['CTA'] - .2, cx=-.4, pist=1),
    K(CENAS['CTA'] + .6, cx=-.4, pist=0, op=0),                    # tela final: 3D totalmente apagado
    K(DURACAO, cx=-.4, pist=0, op=0),
]
HV = [(0, 0)]
MV = [(0, 1), (70.3, 1), (70.9, 1), (97.4, 1), (98.3, 1), (112.3, 1), (113.1, 1), (121.2, 1), (122.0, 1), (CENAS['CTA'] - .2, 1), (CENAS['CTA'] + .6, 0)]
FADE = [(0, 0), (16.1, 0), (16.8, .78), (71.5, .78), (98.3, .85), (148.6, .85), (149.45, 0), (CENAS['CTA'] - .2, 0)]
TILE = [(0, 0), (51.8, 0), (52.6, 1), (61.6, 1), (62.4, 0)]
FILL = [(0, 0), (55.6, 0), (56.4, 1), (61.6, 1), (62.4, 0)]
BAL = [(0, 0)]
GH = [(PIST['t_comp0'], 0), (PIST['t_comp0'] + .6, 1), (159.3, 1), (160.1, 0)]


def suave(u):
    u = min(max(u, 0.), 1.)
    return u * u * (3 - 2 * u)


def interp(lista, t):
    if t <= lista[0][0]:
        return lista[0][1]
    for (t0, a), (t1, b) in zip(lista, lista[1:]):
        if t <= t1:
            return a + (b - a) * suave((t - t0) / (t1 - t0))
    return lista[-1][1]


def taxa(t):
    return interp(TAXA, t)


def tau_por_quadro(tabela=TAXA):
    tau, acc = [], 0.
    for q in range(NQ + 1):
        tau.append(acc)
        acc += interp(tabela, q / FPS) / FPS
    return np.array(tau)


def lx_por_quadro():
    return np.array([2. - interp([(PIST['t_comp0'], 0), (PIST['t_comp1'], 1)], q / FPS) for q in range(NQ + 1)])


def ghost(t):
    return interp(GH, t)
