"""Gera a tabela de trajetórias do vid_0028 e a grava em timeline.json['trajetoria'] (o resto do arquivo não muda).

Movimento visual e galileano (handoff v2 §3): x = x0 + escala·∫(v − v_ref)·fluxo dt, com as chaves de
timeline['movimento'] e a mesma suavização dos dois lados (suave = 3u² − 2u³). O 3D e o Manim leem a MESMA tabela
(amostras a cada 1/60 s, que cobrem exatamente os quadros de 15 e 30 fps), então não há integração duplicada.
Também grava v_A, v_B e v_ref amostrados: o Manim usa a composição relativística para as setas; o 3D usa v − v_ref
para as linhas de velocidade.

Uso (na raiz do repositório): uv run --no-sync python videos/vid_0028_soma_relativistica/movimento.py
"""
import json
from pathlib import Path

UNIT = Path(__file__).resolve().parent
PASSO, SUB = 1 / 60, 8


def suave(u):
    return u * u * (3 - 2 * u)


def chaves(lista, t, campo='v'):
    if t <= lista[0]['t']:
        return lista[0][campo]
    for a, b in zip(lista, lista[1:]):
        if t <= b['t']:
            u = (t - a['t']) / max(b['t'] - a['t'], 1e-9)
            if b.get('ease') != 'linear':
                u = suave(u)
            return a[campo] + (b[campo] - a[campo]) * u
    return lista[-1][campo]


def main():
    path = UNIT / 'timeline.json'
    tl = json.loads(path.read_text(encoding='utf-8'))
    M = tl['movimento']
    S, cortes = M['escala'], sorted(M['cortes'], key=lambda c: c['t'])
    n = round(tl['duracao_s'] / PASSO)
    x = {'A': 0.0, 'B': 0.0, 'E': 0.0}
    out = {k: [] for k in ('xA', 'xB', 'xE', 'vA', 'vB', 'vr')}
    ci, folga_min = 0, (1e9, None)
    comp = tl['geometria']['comprimento_foguete']

    def vel(t):
        vr = chaves(M['v_ref'], t)
        return {'A': chaves(M['v_A'], t) - vr, 'B': chaves(M['v_B'], t) - vr, 'E': -vr}, chaves(M['fluxo'], t)

    for i in range(n + 1):
        t = i * PASSO
        while ci < len(cortes) and cortes[ci]['t'] <= t + 1e-9:
            c = cortes[ci]
            x = {'A': c['xA'], 'B': c['xB'], 'E': c['xE']}
            ci += 1
        out['xA'].append(round(x['A'], 5))
        out['xB'].append(round(x['B'], 5))
        out['xE'].append(round(x['E'], 5))
        out['vA'].append(round(chaves(M['v_A'], t), 5))
        out['vB'].append(round(chaves(M['v_B'], t), 5))
        out['vr'].append(round(chaves(M['v_ref'], t), 5))
        if tl['eventos']['lateral'] <= t < 94.0 or t >= 103.3:
            folga = (x['B'] - x['A']) - comp
            if folga < folga_min[0]:
                folga_min = (folga, round(t, 2))
        # integração do passo seguinte (trapézio em SUB subpassos)
        h = PASSO / SUB
        for k in range(SUB):
            t0, t1 = t + k * h, t + (k + 1) * h
            (v0, f0), (v1, f1) = vel(t0), vel(t1)
            for o in 'ABE':
                x[o] += S * .5 * (v0[o] * f0 + v1[o] * f1) * h
    tl.pop('trajetoria', None)
    texto = json.dumps(tl, ensure_ascii=False, indent=1).rstrip()[:-1].rstrip()   # sem o '}' final
    traj = json.dumps({'passo_s': PASSO, **out}, separators=(',', ':'))
    path.write_text(texto + ',\n "trajetoria": ' + traj + '\n}\n', encoding='utf-8')
    print(json.dumps({'amostras': n + 1, 'folga_min_entre_narizes': round(folga_min[0], 3), 'em_t': folga_min[1]}))


if __name__ == '__main__':
    main()
