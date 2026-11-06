"""Gera timeline.json do 3D (v2): τ por quadro, fase de x (Gx, com o pistão), moléculas (mesmo gerador de fisica.py), hook, câmera, batidas e contadores.
Uso (na raiz): uv run python videos/vid_0033_pvnrt/gerar_timeline.py
"""
import json
from pathlib import Path

import numpy as np

import fisica as F
import roteiro as RT

UNIT = Path(__file__).resolve().parent
N_HOOK = 60


def main():
    nq = RT.NQ
    tau = RT.tau_por_quadro()
    tauH = RT.tau_por_quadro(RT.TAXA_HOOK)
    Lx = RT.lx_por_quadro()
    Gx = np.concatenate([[0.], np.cumsum(2. / Lx[:-1] * np.diff(tau))])          # fase de x: dG = (2/Lx)·dτ  (Lx = 2 fora do pistão)
    ghost = np.array([RT.ghost(q / RT.FPS) for q in range(nq + 1)])
    s0, sp = F.conjunto_3d()
    fb = int(round(RT.T_BATIDA * RT.FPS))
    s0[0, 0] = (2. - sp[0, 0] * Gx[fb]) % 4.                                     # a 1ª batida acompanhada cai em T_BATIDA
    # batidas na parede móvel (+x): cruzamentos de s ≡ 2 (mod 4) por quadro
    S = s0[:, 0:1] + sp[:, 0:1] * Gx[None, :]                                   # (N, nq+1)
    K = np.floor((S - 2.) / 4.)
    hits = np.diff(K, axis=1, prepend=K[:, :1]).clip(min=0).sum(axis=0).astype(int)   # batidas por quadro (todas)
    H = np.cumsum(hits)
    W = int(round(RT.PIST['W'] * RT.FPS))                                       # janela deslizante (mesmo tamanho nos dois estados)
    cont = np.array([H[f] - H[max(f - W, 0)] for f in range(nq + 1)])
    a1 = [int(round(t * RT.FPS)) for t in RT.PIST['estado1']]
    a2 = [int(round(t * RT.FPS)) for t in RT.PIST['estado2']]
    n1, n2 = float(cont[a1[0]:a1[1] + 1].mean()), float(cont[a2[0]:a2[1] + 1].mean())
    razao = n2 / n1
    n1r, n2r = int(round(n1)), int(round(n2))
    assert abs(razao - 2.0) <= .1, razao
    (UNIT / 'qa').mkdir(exist_ok=True)
    (UNIT / 'qa' / 'contadores.txt').write_text(f'janela deslizante de {RT.PIST["W"]} s na face do pistão (mesmas moléculas e velocidades): estado 1 (V, recipiente maior) = {n1:.1f} batidas [mostrar {n1r}]; estado 2 (V/2) = {n2:.1f} [mostrar {n2r}]; razão {razao:.3f} (2,00 ± 0,1)' + chr(10), encoding='utf-8')
    # batidas da acompanhada (quadros fracionários)
    St = S[0]
    kt = K[0]
    bat0 = []
    for f in range(1, nq + 1):
        if kt[f] > kt[f - 1]:
            alvo = 4. * kt[f] + 2.
            bat0.append(round(float(f - 1 + (alvo - St[f - 1]) / (St[f] - St[f - 1])), 2))
    rng = np.random.default_rng(5)
    hook = {'y': rng.uniform(-.18, .18, N_HOOK).round(4).tolist(), 'z': rng.uniform(-.18, .18, N_HOOK).round(4).tolist(),
            's0': rng.uniform(0, 4, N_HOOK).round(4).tolist(), 'sp': rng.uniform(.8, 1.7, N_HOOK).round(4).tolist(),
            'xmin': .6, 'patch': .13}
    tl = {
        'fps': RT.FPS, 'nq': nq, 'duracao_s': RT.DURACAO, 'cenas': RT.CENAS, 'r_esf': RT.R_ESF,
        'tau': tau.round(6).tolist(), 'tauH': tauH.round(6).tolist(), 'hv': [round(RT.interp(RT.HV, q / RT.FPS), 4) for q in range(nq + 1)], 'mv': [round(RT.interp(RT.MV, q / RT.FPS), 4) for q in range(nq + 1)], 'fade': [round(RT.interp(RT.FADE, q / RT.FPS), 4) for q in range(nq + 1)], 'tile': [round(RT.interp(RT.TILE, q / RT.FPS), 4) for q in range(nq + 1)], 'fill': [round(RT.interp(RT.FILL, q / RT.FPS), 4) for q in range(nq + 1)], 'Lx': Lx.round(5).tolist(), 'Gx': Gx.round(6).tolist(), 'ghost': ghost.round(4).tolist(),
        's0': np.round(s0, 6).tolist(), 'sp': np.round(sp, 6).tolist(), 'hook': hook,
        'camera': RT.CAM, 'batidas_acompanhada_quadros': bat0, 'cont': cont.tolist(), 'cont_estado1': n1r, 'cont_estado2': n2r, 'bal': [round(RT.interp(RT.BAL, q / RT.FPS), 4) for q in range(nq + 1)],
    }
    (UNIT / 'timeline.json').write_text(json.dumps(tl), encoding='utf-8')
    print(f"timeline.json: {nq} quadros; batidas da acompanhada: {len(bat0)}; alvo {fb}; contadores (janela deslizante): estado 1 = {n1:.1f}, estado 2 = {n2:.1f}, razão {razao:.3f}")


if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(UNIT))
    main()
