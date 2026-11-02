"""Sync do vid_0032 com a voz (v5): reescreve o timeline para que cada evento-âncora aconteça LEAD s antes da palavra
que o narra. A voz fica contínua (nenhuma pausa é inserida): o vídeo é que se move para a voz.

Entradas: qa/timeline_v4_base.json (preview v4, sem voz), alinhamento_palavras.json (forced alignment da voz).
Saídas: timeline.json (eventos novos, câmera e trechos 3D) e sync_relatorio.json (cada âncora × palavra, atraso 0).
Uso (na raiz): uv run --no-sync python videos/vid_0032_microondas_chocolate/sync_voz.py
"""
import json
import re
from pathlib import Path

U = Path(__file__).absolute().parent
LEAD = .12
FIM_CTA = 1.5                                   # a imagem fica até 1,5 s depois da última palavra


def norm(w):
    return re.sub(r'[.,:;!?…]+', '', w.lower())


base = json.loads((U / 'qa' / 'timeline_v4_base.json').read_text(encoding='utf-8'))
pal = json.loads((U / 'alinhamento_palavras.json').read_text(encoding='utf-8'))
PW = [norm(w['word']) for w in pal]
usados = []


def W(frase, ocorr=0, depois=0):
    """Instante de início da frase (ocorr-ésima ocorrência, procurando só depois da palavra de índice 'depois')."""
    alvo = [norm(x) for x in frase.split()]
    n = 0
    for i in range(depois, len(PW) - len(alvo) + 1):
        if PW[i:i + len(alvo)] == alvo:
            if n == ocorr:
                usados.append((frase, i, pal[i]['start']))
                return pal[i]['start']
            n += 1
    raise AssertionError(f'frase não achada: {frase!r} ({ocorr})')


L = LEAD
E = dict(base['eventos'])
for k in [k for k in E if k.startswith(('c07', 'c06', 'c05'))] + ['endcard']:
    E.pop(k, None)

# ---------------- C01 (0–27 s) ----------------
E.update({
    'c01_regua': 1.0,
    'c01_manchete': W('Parece piada') - L,
    'c01_saltos': W('elas ficam') - 1.1,                      # o 1º salto da régua cai em "elas ficam sempre"
    'c01_manchete_fim': 11.0, 'c01_rebobina': 11.5, 'c01_recua': 11.9,
    'c01_etiqueta': 13.1,
    'c01_mhz': W('dois mil quatrocentos e cinquenta', 0) - .35,   # o "2450 MHz" aparece um pouco antes de ser dito (≥ 3 s legível)
    'c01_etiqueta_pulso': W('dois mil quatrocentos e cinquenta', 0) - L,
    'c01_etiqueta_fim': 17.3,
    'c01_porta_fecha': W('Agora imagina') - L, 'c01_tela_some': 18.5,
    'c01_prato_parado': W('prato parado') - L, 'c01_prato_parado_fim': W('Em três passos') - .0,
    'c01_chip1': W('primeiro') - L, 'c01_chip2': W('Segundo') - L, 'c01_chip3': W('Terceiro') - L,
    'c01_fitas_somem': 25.5, 'c01_teto_some': 25.5, 'c01_derrete_fim': 26.2, 'c01_camera_topo': 26.3, 'c01_troca_fim': 27.0,
})
E['c01_liga'] = E['c01_chip1']
E['c01_fita_reflete'] = E['c01_liga'] + 2.0
E['c01_derrete_ini'] = E['c01_chip2']
E['c01_chips_fim'] = E['c01_camera_topo']
E['c01_entra'] = 17.9

# ---------------- C02 ----------------
E.update({
    'c02': W('O forno solta') - L, 'c02_viaja': W('Elas batem') - 2.6,       # a frente chega à parede em "Elas batem"
    'c02_estacionaria': W('Somando') - L, 'c02_parada': W('é a onda') - .1,
    'c02_nos': W('Nos nós') - .1, 'c02_ventres': W('Nos ventres') - .1,
})

# ---------------- C03 ----------------
E.update({
    'c03': W('Agora vem o pulo') - L, 'c03_seta': W('o que esquenta') - L,
    'c03_e2': W('ao quadrado') + .45,                       # pico de +E: o E do vetor vira E² (a transformação começa 0,5 s antes)
    'c03_mf2': W('O campo aponta') + .1,
    'c03_instantanea': W('Esse aquecimento') - L, 'c03_media': W('então o que importa') - L,
    'c03_medidor_pico': W('Resultado') - L, 'c03_chaves': W('De um ventre') - L, 'c03_manchas': W('Uma mancha') - L,
})
E['c03_medidor'] = E['c03_seta'] + .85

# ---------------- C04 ----------------
i_conta = next(i for i, w in enumerate(pal) if norm(w['word']) == 'digamos')
E.update({
    'c04': W('Agora a conta') - L, 'c04_regua': W('Digamos que') - L,
    'c04_d_lambda': W('Isso é meio') - L, 'c04_l1b': W('então a onda inteira') - L, 'c04_l1_12': W('doze vírgula') - L,
    'c04_etiqueta': W('A etiqueta dá') - L,
    'c04_f_voa': W('dois mil quatrocentos e cinquenta', 1) - L, 'c04_f_gh': W('quase dois bilhões') - L,
    'c04_viajante': 85.8,
    'c04_osc': W('A cada oscilação') - .04,                 # T0: a crista começa a andar em "A cada oscilação"
    'c04_c_lambda_f': W('Então a velocidade') - L, 'c04_ind': W('Como o comprimento') - L,
    'c04_c2df': W('duas vezes a distância') - L, 'c04_numeros': 98.7, 'c04_resultado': 101.15,
    'c04_pulso': W('A velocidade da luz', depois=i_conta) - L,
})

# ---------------- C05 ----------------
E.update({
    'c05': W('Só que o forno') - L, 'c05_fitas': W('Vários padrões') - L, 'c05_texto': W('Vários padrões') - L,
    'c05_relevo': W('e o mapa') - L, 'c05_fitas_fim': 113.3, 'c05_assenta': 116.0, 'c05_derrete': 116.0,
})

# ---------------- C06 ----------------
E.update({
    'c06': W('E é por isso') - L, 'c06_m': W('Olha este') - .1, 'c06_giro_ini': W('Girando') - .1,
    'c06_giro_fim': W('e tem a mesma') - .1, 'c06_anel': W('as manchas viram') - L, 'c06_centro': W('Só o centro') - L,
    'c06_acel': .8,
})
E['c06_grafico'] = E['c06_giro_ini'] + .5
E['c06_media'] = E['c06_giro_fim']

# ---------------- C07 ----------------
fim_voz = pal[-1]['end']
E.update({
    'c07_desafio': W('Desafio') - L, 'c07_ideal': W('no modelo ideal') - L, 'c07_f': W('novecentos') - L,
    'c07_d': W('qual a distância') - L, 'c07_cta': W('Segue o Parallax') - L,
})
E['c06_centro_fim'] = E['c07_desafio']
DUR = round(fim_voz + FIM_CTA, 1)
E['fim'] = DUR

# ---------------- câmera: as chaves do C01 e do C05/C06 acompanham os eventos ----------------
KN = [(0, 0), (7.5, E['c01_rebobina']), (8.3, E['c01_recua']), (9.6, 13.2), (10, 13.6), (13, 17.2), (14.4, 18.2), (14.8, 18.5),
      (17.5, 20.6), (26, 25.4), (27.2, E['c01_camera_topo']), (28, E['c01_troca_fim'])]


def warp(t):
    for (a, A), (b, B) in zip(KN, KN[1:]):
        if t <= b:
            return A + (B - A) * (t - a) / (b - a)
    return t


cam = []
for c in base['camera']:
    if c['t'] <= 28:
        cam.append({**c, 't': round(warp(c['t']), 3)})
cam.append({**base['camera'][-4], 't': round(E['c05'], 3)})                       # chave de 127 s da v4
cam.append({**base['camera'][-3], 't': round(E['c06'], 3)})                       # 142 s
cam.append({**base['camera'][-2], 't': round(E['c06'] + .7, 3)})                  # 142,7 s: o forno sobe
cam.append({**base['camera'][-1], 't': round(E['c07_desafio'] + .6, 3)})
ts = [c['t'] for c in cam]
assert ts == sorted(ts), ts

E = {k: round(v, 3) for k, v in E.items()}
tl = {**base, 'eventos': E, 'camera': cam, 'duracao_s': DUR, 'trechos_3d': [
    [0, round(int(round(E['c01_troca_fim'] * 15)) / 15, 4)],
    [round(int(E['c05'] * 15 - 1) / 15, 4), round(int(round((E['c07_desafio'] + .6) * 15)) / 15, 4)]]}
tl['nota'] = 'Fonte única de tempo do vid_0032 v5 (preview com voz, sincronizado). Tempos em segundos. Gerado por sync_voz.py.'
tl.pop('projecao_3d', None)
(U / 'timeline.json').write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding='utf-8')
(U / 'sync_relatorio.json').write_text(json.dumps({'duracao_s': DUR, 'fim_voz_s': fim_voz, 'lead_s': LEAD, 'ancoras': [
    {'frase': f, 'palavra': i, 'inicio_voz': t} for f, i, t in usados]}, ensure_ascii=False, indent=1), encoding='utf-8')
print('duracao', DUR, 'trechos_3d', tl['trechos_3d'])
for k in sorted(E, key=lambda k: E[k]):
    print(f'{E[k]:8.2f}  {k}')
