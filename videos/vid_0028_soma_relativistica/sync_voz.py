"""Sync do vid_0028 com a voz: reescreve o timeline (3D + Manim) para que cada evento-âncora aconteça LEAD s antes da
palavra que o narra.

Entradas: timeline_v6_base.json (preview silencioso), alinhamento_palavras.json (forced-alignment da voz),
audio/narracao_v1.wav e media_preview/estados_vid0028_medir.json (tempo de animação ocupado por trecho, MEDIR).
Saídas: timeline.json (tempos novos + sync.ritmo), audio/narracao_sync.wav (voz com as pausas inseridas, só em fim de
frase), alinhamento_sync.json (palavras no tempo do vídeo) e sync_relatorio.json.

Regra: entre duas âncoras, cada trecho recebe pelo menos ocupado × FMIN + MARGEM; se a fala não dá esse tempo, entra
uma pausa na voz antes da âncora (só depois de pontuação); se a âncora cai no meio da frase, o trecho acelera mais.
Depois: uv run --no-sync python movimento.py (trajetória) e render.
Uso (na raiz): uv run --no-sync python videos/vid_0028_soma_relativistica/sync_voz.py
"""
import json
import re
import wave
from pathlib import Path

import numpy as np

U = Path(__file__).absolute().parent
LEAD, FMIN, FMIN_DURO, MARGEM = .10, .72, .5, .08
FIM_VOZ_PARA_FIM, FIM_PARA_DURACAO = .9, .6

ANCORAS = [  # (evento do timeline, início da frase que o narra), na ordem da fala
    ('setas', 'Para a Terra'), ('setup', 'cada um vai'), ('pergunta', 'Que velocidade o'), ('palpite', 'O palpite'),
    ('nao_e_16', 'mas a resposta'), ('promessa', 'Neste vídeo'), ('chips', 'em três passos'),
    ('c02', 'Passo um'), ('troca_A', 'Para A, ele'), ('nota', 'e é a Terra'), ('slot_pulsa', 'Queremos'),
    ('regua', 'Na Terra, as'), ('fecha', 'dão um vírgula'), ('na_terra', 'é o ritmo'),
    ('nao_e', 'Não é o que'),
    ('origem', 'Passo dois'), ('anda_txt', 'Na Terra, B'), ('anda', 'percorre um'), ('vb_def', 'a velocidade de B é um'),
    ('a_anda', 'A percorre'), ('rel_gal', 'então, para A'), ('mistura', 'Isso é Galileu'),
    ('defs', 'Para A, a velocidade'), ('lorentz', 'Entra um fator'), ('gama_def', 'e o tempo de A'),
    ('razao', 'Monta a razão'), ('gama', 'o gama aparece'), ('gama_cancela', 'e cancela'), ('dt_hint', 'Divide pelo'),
    ('dt_divide', 'pelo intervalo'), ('distribui', 'sobra deslocamento'), ('vb', 'a velocidade de B'),
    ('formula', 'Chegamos à regra'),
    ('c05', 'Passo três'), ('viajam', 'os números'), ('numerador', 'Em cima'), ('sinais', 'Embaixo'),
    ('produto', 'produto negativo'), ('sinal_nota2', 'o menos vira'), ('um64', 'um vírgula sessenta'),
    ('fracao', 'Dividindo'), ('q4041', 'quarenta sobre'), ('sentido', 'O sinal só'),
    ('carros', 'Com carros'), ('g1', 'esse produto é'), ('g2', 'o denominador vira'), ('g3', 'e sobra a soma'),
    ('galileu', 'Galileu é o limite'),
    ('regua8', 'Com cinquenta'), ('soma_simples', 'a soma daria'), ('rel1', 'medido por A, oitenta'),
    ('acelera', 'Com noventa e nove'), ('cls2', 'quase o dobro'), ('rel2', 'medido por A, noventa'),
    ('menor_c', 'nove cinco'),
    ('c09', 'Resumindo'), ('fecha9', 'a distância fecha'), ('troca9A', 'mas cada foguete'),
    ('fecho1', 'Perto da luz'), ('fecho2', 'Corpo com massa'),
    ('cta', 'Se essa conexão'),
]


def norm(w):
    return re.sub(r'[.,:;!?…]+', '', w.lower())


def main():
    base = json.loads((U / 'timeline_v6_base.json').read_text(encoding='utf-8'))
    pal = json.loads((U / 'alinhamento_palavras.json').read_text(encoding='utf-8'))
    ocup = json.loads((U / 'media_preview' / 'estados_vid0028_medir.json').read_text(encoding='utf-8'))['ocupado']
    E = dict(base['eventos'])
    E.setdefault('C01', 0.0)                  # início fixo em 0 (cold open)
    nomes = sorted(E, key=lambda k: E[k])
    palavras = [norm(w['word']) for w in pal]

    # âncora → índice da primeira palavra da frase (busca em ordem)
    idx, k = {}, 0
    for ev, frase in ANCORAS:
        alvo = [norm(x) for x in frase.split()]
        while palavras[k:k + len(alvo)] != alvo:
            k += 1
            assert k < len(palavras), f'frase não achada: {frase!r}'
        idx[ev] = k
        k += 1
    assert [nomes.index(e) for e, _ in ANCORAS] == sorted(nomes.index(e) for e, _ in ANCORAS), 'âncoras fora da ordem'

    pausas = {}                                   # índice da palavra → pausa inserida antes dela (s)
    desloc = lambda i: sum(p for j, p in pausas.items() if j <= i)
    T, ritmo, rel = {nomes[0]: 0.0}, {}, []
    fim_voz = pal[-1]['end']
    marcos = [(e, idx[e]) for e, _ in ANCORAS] + [('fim', None)]
    ant = nomes[0]
    for ev, wi in marcos:
        trecho = nomes[nomes.index(ant):nomes.index(ev)]
        d_old = [E[nomes[nomes.index(e) + 1]] - E[e] for e in trecho]
        dmin = [ocup.get(e, 0) * FMIN + MARGEM for e in trecho]
        if wi is None:
            tb = fim_voz + desloc(len(pal)) + FIM_VOZ_PARA_FIM
            tb = max(tb, T[ant] + sum(dmin))
        else:
            tb = pal[wi]['start'] + desloc(wi) - LEAD
        A = tb - T[ant]
        pausa = 0.0
        if sum(dmin) > A:
            # pausa na última fronteira de frase entre a âncora anterior e esta (nunca no meio da frase)
            w0 = idx.get(ant, 0) + 1
            fronteira = lambda j, pont: j > 0 and re.search(pont, pal[j - 1]['word'])
            pode = None if wi is None else next(
                (j for pont in (r'[.:!?…]$', r'[,;]$') for j in range(wi, w0 - 1, -1) if fronteira(j, pont)), None)
            if pode is not None:
                pausa = round(sum(dmin) - A + .05, 2)
                pausas[pode] = round(pausas.get(pode, 0) + pausa, 2)
                tb += pausa
                A = tb - T[ant]
            else:   # âncora no meio da frase: acelera mais (até FMIN_DURO)
                dmin = [ocup.get(e, 0) * FMIN_DURO + MARGEM for e in trecho]
                if sum(dmin) > A:
                    print(f'AVISO {ev}: nem com FMIN_DURO cabe ({sum(dmin):.2f} > {A:.2f} s)')
                    dmin = [m * A / sum(dmin) for m in dmin]
        extra = A - sum(dmin)
        w = [max(o - m, .01) for o, m in zip(d_old, dmin)]
        t = T[ant]
        for e, m, wj in zip(trecho, dmin, w):
            d = m + extra * wj / sum(w)
            T[e] = round(t, 4)
            if ocup.get(e, 0) > 0:
                f = min(1.0, (d - MARGEM) / ocup[e])
                if f < .999:
                    ritmo[e] = round(f, 3)
            t += d
        T[ev] = round(tb, 4)
        if wi is not None:
            rel.append({'evento': ev, 'palavra': pal[wi]['word'], 'voz_s': round(pal[wi]['start'] + desloc(wi), 3),
                        'evento_s': T[ev], 'pausa_antes': pausa,
                        'menor_fator': min([ritmo.get(e, 1) for e in trecho], default=1)})
        ant = ev
    for e in nomes[nomes.index('fim') + 1:]:
        T[e] = T['fim'] + (E[e] - E['fim'])
    dur_old, dur_new = base['duracao_s'], round(T['fim'] + FIM_PARA_DURACAO, 3)

    xs = [0.0] + [E[e] for e in nomes] + [dur_old]
    ys = [0.0] + [T[e] for e in nomes] + [dur_new]
    pts = sorted(set(zip(xs, ys)))
    xo, yn = np.array([p[0] for p in pts]), np.array([p[1] for p in pts])
    assert np.all(np.diff(yn) >= 0), 'mapa de tempo não monotônico'

    def warp(t):
        return round(float(np.interp(t, xo, yn)), 4)

    tl = json.loads(json.dumps(base))
    tl['duracao_s'] = dur_new
    tl['eventos'] = {e: T[e] for e in nomes}
    for b in tl['beats']:
        b['inicio_s'], b['fim_s'] = warp(b['inicio_s']), warp(b['fim_s'])
    M = tl['movimento']
    for kk in ('v_A', 'v_B', 'referencial', 'fluxo', 'cortes'):
        for c in M.get(kk, []):
            c['t'] = warp(c['t'])
    for kk in ('camera', 'veu', 'foguetes', 'foguete_dy', 'realce_3d'):
        for c in tl.get(kk, []):
            c['t'] = warp(c['t'])
    tl['qa_alinhamento']['quadros'] = [round(warp(q / 15) * 15) for q in tl['qa_alinhamento']['quadros']]
    tl['sync'] = {'_nota': 'gerado por sync_voz.py: eventos LEAD s antes da palavra; ritmo = fator das animações do trecho',
                  'lead_s': LEAD, 'voz': 'audio/narracao_sync.wav', 'ritmo': ritmo,
                  'mapa': {'antigo': [round(float(x), 4) for x in xo], 'novo': [round(float(y), 4) for y in yn]}}
    tl['_leia_me'] = tl['_leia_me'].replace('vid_0028 v5.', 'vid_0028 v6 sincronizado com a voz (sync_voz.py).')
    (U / 'timeline.json').write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding='utf-8')

    # voz com as pausas: corte no ponto de menor energia entre o fim da palavra anterior e o início da âncora
    with wave.open(str(U / 'audio' / 'narracao_v1.wav')) as w:
        sr, x = w.getframerate(), np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
    partes, ini, fade = [], 0, int(.008 * sr)
    for wi in sorted(pausas):
        a, b = int(pal[wi - 1]['end'] * sr), int(pal[wi]['start'] * sr)
        if b - a < int(.02 * sr):
            a, b = a - int(.03 * sr), b + int(.01 * sr)
        h = int(.01 * sr)
        en = [np.sum(x[j:j + h] ** 2) for j in range(a, max(a + 1, b - h), h // 2)]
        corte = a + int(np.argmin(en)) * (h // 2) + h // 2
        seg = x[ini:corte].copy()
        seg[-fade:] *= np.linspace(1, 0, fade)
        if partes:
            seg[:fade] *= np.linspace(0, 1, fade)
        partes += [seg, np.zeros(int(round(pausas[wi] * sr)), np.float32)]
        ini = corte
    seg = x[ini:].copy()
    if partes:
        seg[:fade] *= np.linspace(0, 1, fade)
    y = np.concatenate(partes + [seg]).clip(-32768, 32767).astype(np.int16)
    with wave.open(str(U / 'audio' / 'narracao_sync.wav'), 'wb') as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(sr)
        w.writeframes(y.tobytes())
    sync_pal = [dict(p, start=round(p['start'] + desloc(i), 3), end=round(p['end'] + desloc(i), 3)) for i, p in enumerate(pal)]
    (U / 'alinhamento_sync.json').write_text(json.dumps(sync_pal, ensure_ascii=False, indent=1), encoding='utf-8')
    (U / 'sync_relatorio.json').write_text(json.dumps({'pausas': {pal[i]['word']: p for i, p in pausas.items()},
                                                       'ancoras': rel, 'duracao_s': dur_new},
                                                      ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'âncoras {len(rel)} · pausas {len(pausas)} (total {sum(pausas.values()):.2f} s) · voz {len(y) / sr:.2f} s · '
          f'vídeo {dur_new:.2f} s · menor fator {min(ritmo.values(), default=1):.2f}')
    for i, p in sorted(pausas.items()):
        print(f'  pausa {p:.2f} s antes de "{pal[i]["word"]}" ({pal[i]["start"]:.2f} s)')


if __name__ == '__main__':
    main()
