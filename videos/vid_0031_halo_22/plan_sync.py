"""Planejador de sincronização do vid_0031 (voz real × tempos naturais do roteiro).

Cada âncora (frase falada, ancoras.json) dispara um evento visual do roteiro (chave de E_NAT). Entre duas âncoras o trecho
recebe D = V + pausa, onde V = intervalo na voz e a pausa (silêncio inserido na voz, no vão entre as frases, ≤ maxpad)
só existe quando a animação natural, comprimida ao piso SFLOOR, não cabe em V. Os demais eventos do roteiro são
interpolados linearmente dentro do trecho. Saídas:
  sync.json  {E: tempos novos de todos os eventos, escala: [(t0, t1, s)], cenas, duracao, ancoras (alvo no vídeo), pausas}
  audio/narracao_sync.wav  (a voz + pausas; nunca esticada)
O evento começa LEAD = 0,10 s antes da palavra (atraso tolerado: ≤ 0,2 s depois dela).
Uso: SEM_SYNC=1 uv run --no-sync python videos/vid_0031_halo_22/plan_sync.py [--sfloor 0.8] [--maxpad 2.2]
"""
import argparse
import json
import os
import wave
from pathlib import Path

import numpy as np

os.environ['SEM_SYNC'] = '1'
import roteiro as RT  # noqa: E402

PASTA = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--sfloor', type=float, default=.3)
ap.add_argument('--maxpad', type=float, default=.3)
ap.add_argument('--sfloor_crit', type=float, default=.5)
ap.add_argument('--sfloor_cadeia', type=float, default=.35)
ap.add_argument('--maxpad_cadeia', type=float, default=.4)
ap.add_argument('--maxpad_crit', type=float, default=.8)
a = ap.parse_args()

# âncora -> evento (chave de E_NAT) que começa nela
ANC2E = [
    ('C01_halo', 'titulo'), ('C01_cristais', 'brilhos'), ('C01_seguranca', 'aviso'), ('C02_raio_no_cristal', 'c02'),
    ('C02_lupa', 'lupa'), ('C02_pessoa', 'pessoa'), ('C02_paralelas', 'paralelas'), ('C02_arcos', 'lado_arcos'),
    ('C02_igual', 'igual'), ('C02_22', 'n22'), ('C03_arco_iris', 'c03'), ('C03_gotas', 'ai_42'), ('C03_vira', 'vira'),
    ('C03_halo', 'halo_lbl'), ('C04_frio', 'c04'), ('C04_acima', 'selo_frio'), ('C04_globo', 'globo'), ('C04_brasil', 'brasil'),
    ('C05_oposta', 'prisma'), ('C05_oposta2', 'feixe_op'), ('C05_vizinha', 'feixe_vz'), ('C05_alternada', 'feixe_al'),
    ('C05_60', 'arco60'), ('C06_b1_snell1', 'b1_i1'), ('C06_b1_incidencia', 'b1_eq1'), ('C06_b1_refracao', 'b1_i2'),
    ('C06_b2_triangulo', 'b2'), ('C06_b2_eq', 'b2_eq'), ('C06_b2_r60', 'b2_mf'), ('C06_b3_viradas', 'b3'),
    ('C06_b4_D1', 'b3_eq'), ('C06_b4_soma', 'soma'), ('C06_b4_D2', 'b4_mf1'), ('C06_b4_D2b', 'd2b'), ('C06_payoff', 'b4_mf2'),
    ('C07_grafico', 'girar'), ('C07_giro', 'giro_ini'), ('C07_vale', 'giro_fim'), ('C07_fundo', 'faixas'), ('C07_menos1', 'chaves'),
    ('C08_ida_volta', 'conta'), ('C08_par', 'pontos_par'), ('C08_coincide', 'giro2_ini'), ('C08_simetria', 'eq_par'),
    ('C08_snell_1', 'r30a'), ('C08_r30', 'r30b'), ('C08_snell_2', 'snell2'), ('C08_snell_3', 'snell4'), ('C08_snell_4', 'snell5'),
    ('C08_mf4', 'mf4'), ('C08_payoff', 'payoff'), ('C09_pontos', 'amontoado'), ('C09_empilham', 'projeta_ini'),
    ('C09_nenhum', 'vazio'), ('C09_lado', 'lado9'), ('C09_muita_luz', 'acende9'), ('C09_perto', 'perto'), ('C09_longe', 'longe'),
    ('C09_cone', 'cone'), ('C09_anel', 'ceu_volta'), ('C10_zoom', 'cores'), ('C10_vermelho', 'curva_v'), ('C10_21_7', 'min_v'),
    ('C10_violeta', 'curva_vi'), ('C10_cores_ceu', 'barra'), ('C10_azulado', 'seta_vio'), ('C11_sintese', 'sintese'),
    ('C11_duas_faces', 'pulso_faces'), ('C11_fios', 'fios'), ('C11_halo', 'halo11'), ('C11_cta', 'cta'),
]
# trechos em que uma equação precisa ficar parada ≥ 2,0 s (piso de velocidade mais alto e pausa maior)
CRIT = {n: (a.sfloor_crit, a.maxpad_crit) for n in ('C06_b1_refracao', 'C06_b2_r60', 'C06_payoff', 'C08_simetria', 'C08_snell_1', 'C08_mf4',
                                                    'C08_payoff', 'C06_b2_eq', 'C06_b1_incidencia')}
CRIT['C09_cone'] = (.55, 1.1)                                  # o cone precisa de ~2,5–3 s para varrer e girar até o anel
CRIT.update({n: (a.sfloor_cadeia, a.maxpad_cadeia) for n in ('C08_snell_2', 'C08_snell_3', 'C08_snell_4')})   # a cadeia numérica: voz rápida; exceção de leitura
AN = json.loads((PASTA / 'ancoras.json').read_text(encoding='utf-8'))
PAL = json.loads((PASTA / 'alinhamento_palavras.json').read_text(encoding='utf-8'))
assert [n for n, _ in ANC2E] == AN['order'], 'ordem das âncoras ≠ ancoras.json'
En = RT.E_NAT
N = [En[k] for _, k in ANC2E]
assert all(b > a_ for a_, b in zip(N, N[1:])), [(ANC2E[i], ANC2E[i + 1], N[i], N[i + 1]) for i in range(len(N) - 1) if N[i + 1] <= N[i]]
V = [AN['A'][n] for n, _ in ANC2E]

# tempos novos das âncoras no vídeo
T = [V[0]]
pausas, linhas = [], []
for k in range(len(V) - 1):
    v, nat = V[k + 1] - V[k], N[k + 1] - N[k]
    sf, mp = CRIT.get(ANC2E[k][0], (a.sfloor, a.maxpad))
    pad = min(mp, max(0., sf * nat - v))
    T.append(T[-1] + v + pad)
    if pad > .02:
        i = next(j for j, p in enumerate(PAL) if abs(p['start'] - V[k + 1]) < 1e-6)
        pausas.append((round((PAL[i - 1]['end'] + PAL[i]['start']) / 2, 3), round(pad, 3)))
    linhas.append((ANC2E[k][0], v, nat, v + pad, pad))
LEAD = RT.LEAD
alvo = [max(0., t - LEAD) for t in T]                         # início do evento no vídeo


def remapeia(t):
    """tempo natural -> tempo do vídeo (linear por trechos entre os eventos ancorados)."""
    if t <= N[0]:
        return t + (alvo[0] - N[0])
    if t >= N[-1]:
        return alvo[-1] + (t - N[-1])
    i = max(j for j in range(len(N)) if N[j] <= t)
    if i == len(N) - 1:
        return alvo[-1] + (t - N[-1])
    return alvo[i] + (t - N[i]) / (N[i + 1] - N[i]) * (alvo[i + 1] - alvo[i])


Enew = {k: round(remapeia(t), 3) for k, t in En.items()}
for (_, k), t in zip(ANC2E, alvo):
    Enew[k] = round(t, 3)
esc = [(round(alvo[k], 3), round(alvo[k + 1], 3), round(float(np.clip((alvo[k + 1] - alvo[k]) / (N[k + 1] - N[k]), .35, 1.5)), 3))
       for k in range(len(N) - 1)]
duracao = round(remapeia(RT.DURACAO), 3)
cenas = [(c, round(remapeia(a_), 3), round(remapeia(b), 3)) for c, a_, b in RT.CENAS]
(PASTA / 'sync.json').write_text(json.dumps(dict(E=Enew, escala=esc, cenas=cenas, duracao=duracao,
                                                   ancoras={n: round(t, 3) for (n, _), t in zip(ANC2E, T)},
                                                   alvo={k: round(t, 3) for (_, k), t in zip(ANC2E, alvo)}, mapa={n: k for n, k in ANC2E}, pausas=pausas, lead=LEAD),
                                      indent=1, ensure_ascii=False), encoding='utf-8')
print('%-20s %6s %6s %6s %6s' % ('trecho', 'voz', 'nat', 'dur', 'pausa'))
for n, v, nat, d, pad in linhas:
    print('%-20s %6.2f %6.2f %6.2f %6.2f%s' % (n, v, nat, d, pad, '  <-- pausa' if pad > .02 else ''))
print('TOTAL de pausas: %.1f s | vídeo termina em %.2f s (voz %.2f s; limite 179)' % (sum(p for _, p in pausas), duracao, AN['audio_end']))

# áudio com as pausas
with wave.open(str(PASTA / 'audio' / 'narracao_v4.wav')) as w:
    sr, nch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
    pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
assert nch == 1 and sw == 2
out, last = [], 0
for pos, pad in sorted(pausas):
    i = int(pos * sr)
    out.append(pcm[last:i])
    out.append(np.zeros(int(round(pad * sr)), dtype=np.int16))
    last = i
out.append(pcm[last:])
audio = np.concatenate(out)
falta = int(round(duracao * sr)) - len(audio)
if falta > 0:
    audio = np.concatenate([audio, np.zeros(falta, dtype=np.int16)])
with wave.open(str(PASTA / 'audio' / 'narracao_sync.wav'), 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(audio.astype(np.int16).tobytes())
print('áudio: narracao_sync.wav %.2f s' % (len(audio) / sr))
