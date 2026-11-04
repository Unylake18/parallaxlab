"""vid_0031 v7 — roteiro: tempos (orçamento ≤ 180 s), câmera do céu, cena de lado (observador) e estado do cristal por quadro.

Fonte única para o 3D (via timeline.json, gerado por gerar_timeline.py) e para o Manim (importa daqui): o cristal 2.5D, o feixe e
o fantasma são calculados por quadro a partir de fisica.py e desenhados UMA vez no 3D; o Manim só lê o mesmo estado para pôr
arcos, rótulos, o ponto do gráfico e o minimapa. Unidades de tela = unidades do Manim (quadro 9 × 16, origem no centro).
"""
import json
import os
from pathlib import Path

import numpy as np

import fisica as F

FPS = int(os.environ.get('FPS_RENDER', 15))      # 15: preview 540×960; 30: final 1080×1920
FW, FH = 9., 16.

# ── tempos (s), v7: fala de 509 palavras (≈ 178,6 s); orçamento por cena = fala (handoff v7 §B.8). ────────────────────────────────────────────────────────────────────────
E = {
    # C01 — hook: halo solar, pergunta e cristais (0–10,5)
    'titulo': .3, 'acende': 0., 'brilhos': 2.0, 'aviso': 6.6, 'raio_hook': 7.4, 'mergulho': 9.3,
    # C02 — a cena de lado: o cristal, o raio, 22° de quê (10,5–31,6)
    'c02': 10.5, 'lupa': 12.4, 'lupa_sai': 16.4, 'pessoa': 16.8, 'paralelas': 18.4, 'lado_arcos': 23.6, 'igual': 26.0,
    'n22': 28.6,
    # C03 — comparação com o arco-íris (31,6–41,8)
    'c03': 31.6, 'ai_sombra': 33.1, 'ai_42': 34.5, 'vira': 36.3, 'halo_lbl': 38.5,
    # C04 — onde ver (41,8–51,6)
    'c04': 41.8, 'selo_verao': 42.4, 'verao_sai': 43.1, 'selo_frio': 43.8, 'globo': 46.0, 'icones': 47.2, 'brasil': 48.4,
    # C05 — o prisma escondido (51,6–62,8): três casos de ~3 s
    'prisma': 51.6, 'feixe_op': 52.4, 'rot_vz': 54.3, 'feixe_vz': 54.9, 'rot_al': 57.1, 'feixe_al': 57.6, 'olho': 58.8,
    'prolonga': 59.4, 'arco60': 60.3, 'pulso': 61.2,
    # C06 — a equação nasce, passo a passo, com o caderno (62,8–92,3)
    'equacao': 62.8, 'b1_i1': 62.9, 'b1_r1': 63.6, 'b1_eq1': 64.2, 'b1_i2': 65.0, 'b1_eq2': 66.4, 'b1_arq': 69.85,
    'b2': 70.45, 'b2_eq': 71.85, 'b2_mf': 74.95, 'b2_arq': 78.4, 'b3': 79.0, 'b3_eq': 81.7, 'soma': 83.6, 'b4_mf1': 84.85, 'd2b': 87.0, 'b4_mf2': 88.4,
    # C07 — girar o cristal (92,3–104,2)
    'girar': 92.3, 'giro_ini': 94.6, 'giro_fim': 99.0, 'faixas': 99.4, 'chaves': 100.8,
    # C08 — a conta: ida e volta, com o caderno (104,2–133,2)
    'conta': 104.2, 'fantasma': 104.4, 'pontos_par': 105.1, 'segmento': 105.45, 'giro2_ini': 106.1, 'giro2_fim': 106.95,
    'coincide': 107.15, 'paralelo': 107.7, 'eq_par': 108.5, 'r30a': 111.05, 'snell1': 111.75, 'r30b': 113.85,
    'snell2': 115.3, 'snell3': 118.15, 'snell4': 121.0, 'snell5': 123.85, 'mf4': 126.7, 'payoff': 130.1,
    # C09 — o amontoado, a cena de lado e o cone saindo da pessoa (133,2–149,1)
    'amontoado': 133.2, 'pontos_ini': 133.75, 'pontos_fim': 134.6, 'projeta_ini': 134.7, 'projeta_fim': 136.1, 'vazio': 136.2,
    'lado9': 138.2, 'acende9': 138.7, 'perto': 139.8, 'longe': 140.8, 'cone': 142.0, 'cone_frente': 144.6, 'ceu_volta': 147.8,
    # C10 — as cores: índice de refração (149,1–163,5)
    'cores': 149.1, 'curva_v': 150.1, 'min_v': 150.9, 'curva_vi': 151.7, 'min_vi': 152.5, 'zoom_txt': 153.2, 'ceu_cores': 156.4,
    'zoom': 156.6, 'barra': 157.9, 'seta_verm': 158.8, 'seta_vio': 159.8,
    # C11 — síntese e CTA (163,5–178,6)
    'sintese': 163.5, 'pulso_faces': 167.5, 'fios': 171.5, 'halo11': 174.8, 'cta': 176.6,
}
_DESL = .75
for _k in [k for k in E if E[k] >= E['r30a']]:
    E[_k] += _DESL
DURACAO = 178.6 + _DESL
CENAS = [('C01', 0, 10.5), ('C02', 10.5, 31.6), ('C03', 31.6, 41.8), ('C04', 41.8, 51.6), ('C05', 51.6, 62.8),
         ('C06', 62.8, 92.3), ('C07', 92.3, 104.2), ('C08', 104.2, 133.2 + _DESL), ('C09', 133.2 + _DESL, 149.1 + _DESL),
         ('C10', 149.1 + _DESL, 163.5 + _DESL), ('C11', 163.5 + _DESL, DURACAO)]
ORCAMENTO = [('C01', 0, 10.5), ('C02', 10.5, 31.6), ('C03', 31.6, 41.8), ('C04', 41.8, 51.6), ('C05', 51.6, 62.8),
             ('C06', 62.8, 92.3), ('C07', 92.3, 104.2), ('C08', 104.2, 132.3), ('C09', 132.3, 149.1), ('C10', 149.1, 163.5),
             ('C11', 163.5, 178.6)]
E_NAT = dict(E)                      # tempos "naturais" (orçamento da fala estimada); o planejador de sincronia os remapeia para a voz real
ESCALA = []                          # (t0, t1, s): fator de velocidade das animações por trecho, lido de sync.json
_SJ = Path(__file__).resolve().parent / 'sync.json'
if _SJ.exists() and not os.environ.get('SEM_SYNC'):
    _S = json.loads(_SJ.read_text(encoding='utf-8'))
    E.update(_S['E'])
    DURACAO = _S['duracao']
    CENAS = [tuple(c) for c in _S['cenas']]
    ESCALA = [tuple(x) for x in _S['escala']]
LEAD = .10                           # a imagem começa 0,10 s antes da palavra (atraso máximo tolerado: 0,2 s depois dela)

# ── câmera do céu (mesma projeção do shader do cena3d.js) ─────────────────────────────────────────────────────────────────
PITCH, FOV_H = 40., 60.          # v3: pitch 40° → Sol a ~52° de elevação (cena de lado com o Sol acima da nuvem)
TAN_H = np.tan(np.radians(FOV_H / 2))
TAN_V = TAN_H * FH / FW
SOL_MANIM = (0., 1.667)          # y_px ≈ 380 de 960


def base(pitch=PITCH):
    p = np.radians(pitch)
    return np.array([1., 0, 0]), np.array([0, np.cos(p), np.sin(p)]), np.array([0, np.sin(p), -np.cos(p)])


def dir_de_manim(x, y):
    r, up, f = base()
    v = (x / (FW / 2)) * TAN_H * r + (y / (FH / 2)) * TAN_V * up + f
    return v / np.linalg.norm(v)


def manim_de_dir(v):
    r, up, f = base()
    z = v @ f
    return np.array([(v @ r) / z / TAN_H * FW / 2, (v @ up) / z / TAN_V * FH / 2])


SOL_DIR = dir_de_manim(*SOL_MANIM)
# vista do céu na tela: tela = tr + esc · vista. C10: zoom na borda do anel (ponto a 22,3° do Sol, rumo −38° na tela) até (0,4; 1,0);
# síntese: o céu inteiro reduzido no andar de cima, com o Sol em (0; 4,85).
def _no_cone(s, ang, phi_tela):
    alvo = manim_de_dir(s) + .01 * np.array([np.cos(np.radians(phi_tela)), np.sin(np.radians(phi_tela))])
    t = dir_de_manim(*alvo) - s
    t -= (t @ s) * s
    t /= np.linalg.norm(t)
    a = np.radians(ang)
    return np.cos(a) * s + np.sin(a) * t


PZ = manim_de_dir(_no_cone(SOL_DIR, 22.3, -38.))
ZOOM = (3.2, (np.array([.4, 1.0]) - 3.2 * PZ).round(4).tolist())                       # C10: zoom na borda (cores)
FAIXA = (.63, (np.array([0., 4.85]) - .63 * np.array(SOL_MANIM)).round(4).tolist())    # C11: céu no terço de cima (anel ≥ 4,0)
PZ0 = manim_de_dir(_no_cone(SOL_DIR, 21.8, -38.))
MERGULHO = (3.0, (np.array([0., 1.2]) - 3.0 * PZ0).round(4).tolist())                   # C01: push-in até a borda de dentro
ESC_HOOK = 1.10                                                                           # C01: push-in 1,00 → 1,10
ANG_HOOK = [-38., 32., 104., 150., 212., 262.]       # C01: cristais na borda do anel (rumo na tela; o 1º é o do mergulho)


def suave(u):
    u = np.clip(u, 0, 1)
    return u * u * (3 - 2 * u)


def cam_hook(t):
    """Escala e translação da vista do céu no C01 (as mesmas chaves do timeline: push-in em torno do Sol, depois o mergulho)."""
    if t <= E['mergulho']:
        e = 1 + (ESC_HOOK - 1) * suave(t / E['mergulho'])
        return e, (1 - e) * np.array(SOL_MANIM)
    u = suave((t - E['mergulho']) / (E['c02'] - E['mergulho']))
    e0, tr0 = ESC_HOOK, (1 - ESC_HOOK) * np.array(SOL_MANIM)
    return e0 + (MERGULHO[0] - e0) * u, tr0 + (np.array(MERGULHO[1]) - tr0) * u


def vista_para_tela(p, esc, tr):
    return np.asarray(tr, float) + esc * np.asarray(p, float)
EL_SOL = float(np.degrees(np.arcsin(SOL_DIR[1])))          # elevação do Sol (graus)

# ── cena de lado (C02, C03, C09), v6: Sol REDONDO e inteiro (R 1,8); todo raio nasce no disco (§B.4) ─────────────────────
OLHO_M = np.array([.6, -2.6])                          # olho da pessoa (Manim); pessoa com H = 1,5, como no vid_0025
CHAO_Y = -4.1
SOL_L, SOL_LR = np.array([-1.95, 4.45]), 1.8           # centro e raio do disco do Sol (inteiro na tela)
EL_LADO = float(np.degrees(np.arctan2(SOL_L[1] - OLHO_M[1], OLHO_M[0] - SOL_L[0])))   # elevação do Sol vista do olho (≈ 70°)
H_NUVEM = 1.95                                          # altura da faixa de nuvem acima do olho
NUVEM_Y = float(OLHO_M[1] + H_NUVEM)
K_LADO = 1.0


def dir_lado(el):
    """Direção na tela (vista de lado) de uma elevação 'el' rumo ao lado do Sol."""
    return np.array([-np.cos(np.radians(el)), np.sin(np.radians(el))])


D_LUZ = -dir_lado(EL_LADO)                              # direção de todos os raios do Sol (paralela à reta Sol → olho)
N_LUZ = np.array([-D_LUZ[1], D_LUZ[0]])


def cristal_lado(phi):
    """Cristal na faixa de nuvem a 'phi' graus do Sol (abaixo do Sol, rumo ao horizonte), visto do olho."""
    el = EL_LADO - phi
    return OLHO_M + H_NUVEM / np.sin(np.radians(el)) * dir_lado(el)


def d_perp(p):
    """Distância de p à reta olho–Sol (o raio paralelo que passa por p nasce no disco se for ≤ 0,85·R)."""
    return float(abs((np.asarray(p) - SOL_L) @ N_LUZ))


def ini_no_disco(p, sol=None, R=None, d=None):
    """Ponto de saída, no contorno do disco do Sol, do raio paralelo que passa por p."""
    sol = SOL_L if sol is None else np.asarray(sol, float)
    R = SOL_LR if R is None else R
    d = D_LUZ if d is None else np.asarray(d, float)
    n = np.array([-d[1], d[0]])
    t = float((np.asarray(p) - sol) @ n)
    assert abs(t) <= .85 * R + 1e-9, (p, t)
    return sol + t * n + np.sqrt(R ** 2 - t ** 2) * d


for _phi in (9., 14., 21.84, 30.):
    assert d_perp(cristal_lado(_phi)) <= .85 * SOL_LR, (_phi, d_perp(cristal_lado(_phi)))
L22 = float(np.linalg.norm(cristal_lado(21.84) - OLHO_M))


def lado(h, y):
    """Ponto a h (horizontal, rumo ao Sol) e y (altura) do olho → Manim."""
    return OLHO_M + K_LADO * np.array([-h, y])


# câmera do cone (C08): u = 0 vista de lado ≈ ortográfica; u = 1 câmera do céu (borda do cone = curva de 22° do C01)
def _rot(axis, ang):
    axis = axis / np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K


B0 = np.array([[0, 0, 1.], [0, 1., 0], [1., 0, 0]])     # linhas: direita, cima, frente (olha para +x; −z fica à esquerda)
B1 = np.array(base())
_Rrel = B1.T @ B0
_ang = np.arccos(np.clip((np.trace(_Rrel) - 1) / 2, -1, 1))
_ax = np.array([_Rrel[2, 1] - _Rrel[1, 2], _Rrel[0, 2] - _Rrel[2, 0], _Rrel[1, 0] - _Rrel[0, 1]])
D_LONGE = 60.


def camera_cone(u):
    u = float(np.clip(u, 0, 1))
    R = _rot(_ax, u * _ang)
    Bu = (R @ B0.T).T
    dist = D_LONGE * (1 - u) ** 3
    tanH0 = (FW / 2) / (K_LADO * D_LONGE)
    tanH = np.exp((1 - u) * np.log(tanH0) + u * np.log(TAN_H)) if u < 1 else TAN_H
    off = (1 - u) ** 2 * OLHO_M
    return Bu, -Bu[2] * dist, tanH, off


def proj_cone(P, u):
    """Ponto 3D (olho na origem; x para a direita da cena de lado, y para cima, −z rumo ao Sol) → Manim (None se atrás)."""
    Bu, C, tanH, off = camera_cone(u)
    v = np.asarray(P, float) - C
    z = v @ Bu[2]
    if z <= 1e-3:
        return None
    return off + np.array([(v @ Bu[0]) / z / tanH * FW / 2, (v @ Bu[1]) / z / (tanH * FH / FW) * FH / 2])


def lado3(h, y, x=0.):
    """Ponto da cena de lado em coordenadas 3D do cone (para proj_cone): −z rumo ao Sol."""
    return np.array([x, y, -h])


# ── cristal 2.5D e feixe por quadro (C04–C07, C09) ───────────────────────────────────────────────────────────────────────
SOL_CR_R = .46                                            # raio do Sol nas cenas do cristal (§B.2.7)
X_SOL = -4.5 + .35 + 2.15 * SOL_CR_R                       # centro do Sol: ícone inteiro na tela, margem 0,35
D_SOL = F.u(F.ALPHA0)
TH_OP, TH_VZ = F.ALPHA0, 54.     # oposta com incidência normal (o feixe passa pelo centro); vizinha: entrada rasante, reflexão total
C05_C, C05_R = (1.55, .9), 2.6    # v7: hexágono do C05 (y ≈ +0,3, circunraio ≥ 2,6), com espaço à esquerda para o Sol


def trilha(chaves, t):
    """Chaves [(t, v), ...] com interpolação suave (mesma regra do cena3d.js)."""
    if t <= chaves[0][0]:
        return chaves[0][1]
    for (t0, v0), (t1, v1) in zip(chaves, chaves[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * suave((t - t0) / max(t1 - t0, 1e-9))
    return chaves[-1][1]


LAYOUT = [  # (t, centro x, centro y, circunraio)
    (0., 2.4, 1.4, .62), (E['lupa_sai'] + .5, 2.4, 1.4, .62),                                         # lupa do C02
    (E['prisma'] - .01, *C05_C, C05_R), (E['pulso'] + .7, *C05_C, C05_R),                              # C05: grande, com o Sol à esquerda
    (E['equacao'] - .1, 0., 3.3, 2.4), (E['girar'], 0., 3.3, 2.4),                                     # C06: em cima do caderno
    (E['girar'] + .9, .1, 3.75, 1.7), (E['amontoado'] + .6, .1, 3.75, 1.7),                            # C07–C08
    (E['sintese'] - .31, .3, -.1, 2.4), (DURACAO, .3, -.1, 2.4)]                                       # C11: andar do meio
I1 = [(E['equacao'], 30.), (E['girar'] + 1.0, 30.), (E['girar'] + 1.6, 14.), (E['giro_ini'], 14.), (E['giro_fim'], 88.),
      (E['faixas'], 88.), (E['faixas'] + 1.0, F.i1_min()), (E['conta'], F.i1_min()), (E['conta'] + .7, 30.),
      (E['giro2_ini'], 30.), (E['giro2_fim'], F.i1_min()), (E['amontoado'], F.i1_min())]
L_FORA = [(E['prisma'], .55), (E['pulso'] + .7, .55), (E['equacao'], 1.1), (E['girar'], 1.1), (E['girar'] + .9, 1.3)]


def layout(t):
    k = [(tt, np.array(v)) for tt, *v in LAYOUT]
    v = trilha(k, t)
    return np.array(v[:2]), float(v[2])


def i1_de(t):
    lin = t >= E['giro_ini'] and t <= E['giro_fim']                     # giro do C06 em velocidade constante
    if lin:
        return 14. + (88. - 14.) * (t - E['giro_ini']) / (E['giro_fim'] - E['giro_ini'])
    return float(trilha(I1, t))


def _dist_contorno(S, V):
    d = 1e9
    for k in range(6):
        a, b = V[k], V[(k + 1) % 6]
        ab = b - a
        d = min(d, float(np.linalg.norm(S - (a + np.clip((S - a) @ ab / (ab @ ab), 0, 1) * ab))))
    return d


D_SOL_MIN = 2.4                   # C05: o centro do Sol fica a ≥ 2,4 do contorno do hexágono (§B.3.1)


def _sol_dist(P1, V):
    """Centro do Sol na reta do feixe, o mais perto de P1 que ainda fica a ≥ D_SOL_MIN do contorno."""
    for L in np.arange(2.4, 9., .05):
        S = P1 - L * D_SOL
        if _dist_contorno(S, V) >= D_SOL_MIN:
            return S
    raise AssertionError('sem posição para o Sol')


def sol_cr(tr, t=None):
    """Centro do Sol na reta do feixe. C06 em diante: x = X_SOL. C05: a ≥ 2,4 do contorno; sai desse lugar junto com o layout."""
    P1 = tr['pontos'][1]
    S_x = P1 - (P1[0] - X_SOL) / D_SOL[0] * D_SOL
    if t is None or t >= E['equacao'] - .1:
        return S_x
    S_d = _sol_dist(P1, tr['V'])
    w = suave((t - E['pulso'] - .7) / (E['equacao'] - .1 - E['pulso'] - .7))
    return (1 - w) * S_d + w * S_x


def _poli(tr, l_fora, S=None):
    """Feixe: nasce no contorno do disco do Sol (C05–C08, C11), entra, sai e segue l_fora."""
    S = sol_cr(tr) if S is None else S
    pts = [S + SOL_CR_R * D_SOL, *tr['pontos'][1:]]
    if tr['tipos'][-1] == 'sai':
        pts.append(pts[-1] + l_fora * tr['d_final'])
    return np.array(pts)


def _caso(c, R, th, s_ok):
    """Feixe de um dos casos do C04 (cristal em θ; ponto de entrada no meio da faixa válida)."""
    V = F.hexagono(c, R, th)
    boas = [s for s in np.linspace(.05, .95, 91)
            if s_ok(F.tracar(V[2] + s * (V[3] - V[2]) - 8 * D_SOL, D_SOL, V, max_eventos=3))]
    s = min(boas, key=lambda x: abs(x - .5))
    return F.tracar(V[2] + s * (V[3] - V[2]) - 8 * D_SOL, D_SOL, V, max_eventos=3)


def _prog(t, t0, dur=1.2):
    return float(np.clip((t - t0) / dur, 0, 1))


def estado_cristal(t):
    """Estado do cristal e do feixe no instante t (None fora das cenas de cristal). Lupa do C02: cristal sem feixe."""
    lupa = E['lupa'] - .3 <= t < E['lupa_sai'] + .5
    if not (lupa or E['prisma'] <= t < E['amontoado'] + .6 or t >= E['sintese'] - .3):
        return None
    c, R = layout(t)
    if lupa:
        a = min(suave((t - E['lupa'] + .3) / .6), 1 - suave((t - E['lupa_sai']) / .5))
        return {'c': c, 'R': R, 'alpha': float(a), 'feixe': None, 'fantasma': None, 'D': None, 'i1': None, 'caso': 'lupa',
                'th': float(90. * (t - E['lupa'] + .3))}
    if t < E['sintese'] - .3:
        a_cr = min(suave((t - E['prisma']) / .6), 1 - suave((t - E['amontoado']) / .6))
        if t > E['amontoado'] + .6:
            return None
    else:
        a_cr = min(suave((t - E['sintese'] + .3) / .8), 1 - suave((t - E['cta']) / .5))
    st = {'c': c, 'R': R, 'alpha': float(a_cr), 'feixe': None, 'fantasma': None, 'D': None, 'i1': None, 'caso': None}
    l_fora = float(trilha(L_FORA, t)) if t < E['sintese'] - .3 else 1.0
    if t < E['feixe_al']:                                                   # C05: três casos, o mesmo feixe
        V_op, V_vz = F.hexagono(c, R, TH_OP), F.hexagono(c, R, TH_VZ)
        tr_op = F.tracar((V_op[2] + V_op[3]) / 2 - 8 * D_SOL, D_SOL, V_op, max_eventos=3)
        assert tr_op['faces'][:2] == [2, 5], tr_op['faces']
        tr_vz = _caso(c, R, TH_VZ, lambda r: r['faces'][:2] == [2, 3] and r['tipos'][1] == 'rt')
        tr_vz = {**tr_vz, 'pontos': tr_vz['pontos'][:4], 'tipos': tr_vz['tipos'][:2] + ['rt_fim']}
        S_op, S_vz = _sol_dist(tr_op['pontos'][1], V_op), _sol_dist(tr_vz['pontos'][1], V_vz)
        S_al = _sol_dist(F.caminho60(30., c, R)['pontos'][1], F.caminho60(30., c, R)['V'])
        S = trilha([(E['prisma'], S_op), (E['rot_vz'], S_op), (E['rot_vz'] + .9, S_vz), (E['rot_al'], S_vz), (E['rot_al'] + .7, S_al)], t)
        if t < E['rot_vz']:
            th, tr, S_c = TH_OP, tr_op, S_op
            pr, al, caso = _prog(t, E['feixe_op']), 1 - suave((t - E['rot_vz'] + .35) / .3), 'oposta'
        elif t < E['rot_al']:
            th, tr, S_c = trilha([(E['rot_vz'], TH_OP), (E['rot_vz'] + .8, TH_VZ)], t), tr_vz, S_vz
            pr, al, caso = _prog(t, E['feixe_vz'], 1.4), 1 - suave((t - E['rot_al'] + .35) / .3), 'vizinha'
        else:
            th, tr, S_c = trilha([(E['rot_al'], TH_VZ), (E['rot_al'] + .6, 0.)], t), None, S_al
            pr, al, caso = 0., 0., 'gira'
        st.update(th=float(th), caso=caso, sol=S)
        if tr is not None and t >= E['feixe_op']:
            if caso == 'vizinha' and t < E['feixe_vz']:
                pr = 0.
            st['feixe'] = {'pts': _poli(tr, l_fora, S_c), 'prog': pr, 'alpha': float(al), 'fade_fim': caso == 'vizinha'}
        return st
    i1 = i1_de(t) if t < E['sintese'] - .3 else F.i1_min()
    tr = F.caminho60(i1, c, R)
    assert tr['faces'] == [2, 4], (t, i1)
    S = sol_cr(tr, t)
    st.update(th=float(tr['theta']), i1=i1, caso='alternada', D=float(F.desvio(i1)), tr=tr, sol=S)
    st['feixe'] = {'pts': _poli(tr, l_fora, S), 'prog': _prog(t, E['feixe_al']) if t < E['equacao'] else 1., 'alpha': 1.,
                   'fade_fim': False}
    a_g = min(suave((t - E['fantasma']) / 1.2), 1 - suave((t - E['coincide']) / .8)) if E['fantasma'] <= t < E['amontoado'] else 0.
    if a_g > .001:
        P1, P2 = tr['pontos'][1:3]
        g = F.espelho_bissetor(np.array([P1 - 1.2 * tr['d_in'], P1, P2, P2 + 1.2 * tr['d_final']]), tr)[::-1]
        st['fantasma'] = {'pts': g, 'alpha': float(a_g)}
    return st


def estado_json(t):
    st = estado_cristal(t)
    if st is None:
        return None
    r = lambda a: np.round(np.asarray(a, float), 4).tolist()
    out = {'c': r(st['c']), 'R': round(st['R'], 4), 'th': round(st['th'], 4), 'a': round(st['alpha'], 4), 'caso': st.get('caso'),
           'v': r(F.hexagono(st['c'], st['R'], st['th']))}
    if st['feixe'] is not None:
        f = st['feixe']
        out['feixe'] = {'pts': r(f['pts']), 'prog': round(f['prog'], 4), 'a': round(f['alpha'], 4), 'fade_fim': f['fade_fim']}
    if st['fantasma'] is not None:
        out['fantasma'] = {'pts': r(st['fantasma']['pts']), 'a': round(st['fantasma']['alpha'], 4)}
    return out


if __name__ == '__main__':
    print('cena de lado: elevação do Sol', round(EL_LADO, 2), 'nuvem y', round(NUVEM_Y, 2), 'cristal 22°', cristal_lado(F.d_min()).round(3),
          'd⊥ 9/14/22/30', [round(d_perp(cristal_lado(p)), 2) for p in (9, 14, 21.84, 30)], '≤', .85 * SOL_LR)
    for t in (19., 62.5, 65., 68.5, 75., 97., 108., 112., 165.):
        st = estado_cristal(t)
        print(t, None if st is None else (st['caso'], round(st['th'], 2), st['D'] and round(st['D'], 2)))
