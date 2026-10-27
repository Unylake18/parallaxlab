"""Gera a tabela de trajetórias do vid_0028 e a grava em timeline.json['trajetoria'] (o resto do arquivo não muda).

v3 (handoff v3 §5.1): a tela mostra, em cada referencial, a velocidade que AQUELE referencial mede. Tabela por
referencial (unidades de c), composição relativística s = (v − v_ref)/(1 − v·v_ref/c²):

    Terra:      A +0,8   B −0,8     Terra 0
    Foguete A:  A 0      B −40/41   Terra −0,8
    Foguete B:  A +40/41 B 0        Terra +0,8

Nas trocas, s de cada objeto é a média ponderada (suave = 3u² − 2u³) entre as duas tabelas. Posição:
x = x0 + escala·∫ s·fluxo dt. Assim, no referencial de A, B anda a 0,976·escala (não a 1,6) e o colchete entre os
foguetes fecha a 1,6·escala na Terra e a 0,976·escala em A. O 3D e o Manim leem a MESMA tabela (amostras a cada
1/60 s, que cobrem exatamente os quadros de 15 e 30 fps); o Manim usa sA, sB, sE também para as setas.

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


def rel(v, vf):
    return (v - vf) / (1 - v * vf)


def referencial(lista, t):
    """(r_de, r_para, peso) no instante t."""
    if t <= lista[0]['t']:
        return lista[0]['r'], lista[0]['r'], 0.0
    for a, b in zip(lista, lista[1:]):
        if t <= b['t']:
            if a['r'] == b['r']:
                return a['r'], a['r'], 0.0
            return a['r'], b['r'], suave((t - a['t']) / max(b['t'] - a['t'], 1e-9))
    return lista[-1]['r'], lista[-1]['r'], 0.0


def medidas(M, t):
    """Velocidades medidas na tela (A, B, Terra) no instante t."""
    v = {'A': chaves(M['v_A'], t), 'B': chaves(M['v_B'], t), 'E': 0.0}
    vf = {'T': 0.0, 'A': v['A'], 'B': v['B']}
    r0, r1, w = referencial(M['referencial'], t)
    return {o: (1 - w) * rel(v[o], vf[r0]) + w * rel(v[o], vf[r1]) for o in 'ABE'}


def main():
    path = UNIT / 'timeline.json'
    tl = json.loads(path.read_text(encoding='utf-8'))
    M = tl['movimento']
    S, cortes = M['escala'], sorted(M['cortes'], key=lambda c: c['t'])
    n = round(tl['duracao_s'] / PASSO)
    x = {'A': 0.0, 'B': 0.0, 'E': 0.0}
    out = {k: [] for k in ('xA', 'xB', 'xE', 'sA', 'sB', 'sE')}
    ci, folga_min, xmax = 0, (1e9, None), 0.0
    comp = tl['geometria']['comprimento_foguete']
    for i in range(n + 1):
        t = i * PASSO
        while ci < len(cortes) and cortes[ci]['t'] <= t + 1e-9:
            c = cortes[ci]
            x = {'A': c['xA'], 'B': c['xB'], 'E': c['xE']}
            ci += 1
        s = medidas(M, t)
        for o in 'ABE':
            out['x' + o].append(round(x[o], 5))
            out['s' + o].append(round(s[o], 5))
        if t >= tl['eventos']['lateral'] and not (94.0 <= t < 102.7):
            folga = (x['B'] - x['A']) - comp
            if folga < folga_min[0]:
                folga_min = (folga, round(t, 2))
            xmax = max(xmax, abs(x['A']), abs(x['B']))
        h = PASSO / SUB
        for k in range(SUB):
            t0, t1 = t + k * h, t + (k + 1) * h
            s0, s1 = medidas(M, t0), medidas(M, t1)
            f0, f1 = chaves(M['fluxo'], t0), chaves(M['fluxo'], t1)
            for o in 'ABE':
                x[o] += S * .5 * (s0[o] * f0 + s1[o] * f1) * h
    tl.pop('trajetoria', None)
    texto = json.dumps(tl, ensure_ascii=False, indent=1).rstrip()[:-1].rstrip()   # sem o '}' final
    traj = json.dumps({'passo_s': PASSO, **out}, separators=(',', ':'))
    path.write_text(texto + ',\n "trajetoria": ' + traj + '\n}\n', encoding='utf-8')
    print(json.dumps({'amostras': n + 1, 'folga_min_entre_narizes': round(folga_min[0], 3), 'em_t': folga_min[1],
                      'maior_|x|_centro': round(xmax, 3)}))


if __name__ == '__main__':
    main()
