"""Sincronização do vid_0029 com a voz aprovada (ElevenLabs v4, voz Dioke).

Entrada: audio/narracao_final.wav (fonte aprovada, intocada) e audio/alinhamento_palavras.json (Scribe: início/fim de
cada palavra). O texto exibido vem de narracao_blocos.py (grafia aprovada: R, a, r, Parallax); os tempos vêm do Scribe,
casados palavra a palavra.
Saídas:
- timeline.json: beats, eventos, chaves do 3D e "ancoras" (um instante por evento visual, lido pelo cena.py);
- audio/narracao_montagem.wav: a fonte com os respiros inseridos (GAPS), sem outra edição;
- legenda.srt: uma linha por legenda, nos tempos da montagem.
Regra: o evento visual começa LEAD s antes da primeira palavra que o nomeia (≤ 0,2 s de diferença).
Uso: uv run python videos/vid_0029_campo_toroide/sincronizar.py
"""
import difflib
import json
import re
import sys
import unicodedata
import wave
from pathlib import Path

import numpy as np

UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(UNIT))
from narracao_blocos import BLOCOS  # noqa: E402

LEAD = 0.1
END_HOLD = 2.4           # o handle fica na tela depois do "Siga o Parallax Lab."
GAPS = [('Primeiro teste', 1.2)]   # respiro antes da frase: o 2πr voa para a equação e a linha vira referência


def norm(w):
    w = unicodedata.normalize('NFD', w.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in w if unicodedata.category(c) != 'Mn'))


def tokens_texto():
    out = []
    for beat, _, _, texto in BLOCOS:
        for w in re.sub(r'\[[^\]]*\]', ' ', texto).split():
            out.append((beat, w))
    return out


def casar(texto, scribe):
    a, b = [norm(w) for _, w in texto], [norm(w['text']) for w in scribe]
    times = [None] * len(a)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op in ('equal', 'replace') and (i2 - i1) == (j2 - j1):
            for k in range(i2 - i1):
                times[i1 + k] = (scribe[j1 + k]['start'], scribe[j1 + k]['end'])
        elif op == 'replace':
            s, e = scribe[j1]['start'], scribe[j2 - 1]['end']
            for k in range(i2 - i1):
                f0, f1 = k / (i2 - i1), (k + 1) / (i2 - i1)
                times[i1 + k] = (s + f0 * (e - s), s + f1 * (e - s))
    for i, t in enumerate(times):   # palavra do texto sem par no Scribe: herda o fim da anterior
        if t is None:
            prev = times[i - 1] if i else (0., 0.)
            times[i] = (prev[1], prev[1])
    return times


def main():
    scribe = [w for w in json.loads((UNIT / 'audio' / 'alinhamento_palavras.json').read_text(encoding='utf-8'))['words']
              if w['type'] == 'word']
    texto = tokens_texto()
    raw = casar(texto, scribe)
    normed = [norm(w) for _, w in texto]

    def find(phrase, after=0., base=None):
        base = raw if base is None else base
        p = [norm(w) for w in phrase.split()]
        for i in range(len(normed) - len(p) + 1):
            if normed[i:i + len(p)] == p and base[i][0] >= after:
                return i
        raise KeyError(phrase)

    # respiros: inseridos no meio da pausa que antecede a frase
    cuts = []
    for phrase, dur in GAPS:
        i = find(phrase)
        cuts.append(((raw[i - 1][1] + raw[i][0]) / 2, dur))
    cuts.sort()

    def shift(t):
        return t + sum(d for c, d in cuts if t >= c)
    times = [(shift(s), shift(e)) for s, e in raw]

    def w(phrase, after=0., end=False):
        i = find(phrase, after, times)
        if end:
            return times[i + len(phrase.split()) - 1][1]
        return times[i][0]

    def at(phrase, after=0., lead=LEAD):
        return round(w(phrase, after) - lead, 3)

    voice_end = times[-1][1]
    total = round(voice_end + END_HOLD, 2)
    beat_start = {}
    for (beat, _), (s, _) in zip(texto, times):
        beat_start.setdefault(beat, s)
    beat_start['B01'] = 0.

    A = {
        # B01
        'b01_manchete': .3, 'liga': at('liga a corrente'), 'campo_acende': at('e o campo fica'),
        'chip_fora': at('E fora'),
        # B02
        'b02_inicio': at('Isso é um toroide'), 'modelo_ideal': at('modelo ideal'), 'def_N': at('O número de espiras é'),
        'def_I': at('A corrente, igual'),
        # B03
        'b03_inicio': at('Agora, de cima'), 'def_R': at('O raio médio'), 'def_a': at('o raio do tubo'),
        'desenha': at('Desenha um caminho'), 'circulo': at('um círculo em volta'), 'raio_r': at('com raio r'),
        'simetria': at('a simetria'), 'acompanhar': at('acompanhar esse círculo'), 'mesmo_modulo': at('mesmo módulo'),
        'percorre': at('percorre o caminho'),
        # B04
        'b04_inicio': at('Aí entra'), 'ampere': at('Lei de Ampère'), 'elo_B': at('campo magnético no caminho'),
        'elo_dl': at('no caminho é'), 'atravessa_disco': at('a corrente que atravessa o disco'),
        'apontam_juntos': at('apontam juntos'), 'escalar': at('vira multiplicação'), 'sai_integral': at('sai da integral'),
        'sobra': at('Sobra o tamanho'), 'desenrola': at('Desenrola'), 'dois_pi': at('Dois pi vezes'),
        'raio_caminho_b04': at('raio do caminho', after=w('Dois pi vezes')),
        # B05
        'b05_inicio': at('Primeiro teste'), 'buraco': at('o caminho no buraco'), 'corrente_zero': at('Corrente atravessando'),
        'campo_zero_b05': at('o campo aqui é zero'),
        # B06
        'b06_inicio': at('Segundo teste'), 'por_dentro': at('o caminho por dentro'), 'cada_espira': at('Cada espira fura'),
        'mesmo_sentido_fim': round(w('mesmo sentido', end=True), 3), 'corrente_atravessa_b06': at('A corrente que atravessa é'),
        'numero_espiras': at('o número de espiras vezes a corrente.'), 'vezes_corrente': at('vezes a corrente.', after=w('A corrente que atravessa é')),
        'passa': at('Passa o dois pi'), 'campo_e': at('e o campo é'),
        'raio_denominador': at('raio do caminho', after=w('dividido por dois pi')), 'repara': at('Repara'),
        'nao_uniforme': at('não é uniforme'), 'mais_forte': at('mais forte'),
        # B07
        'b07_inicio': at('E o terceiro'), 'por_fora': at('o caminho por fora'), 'duas_vezes': at('DUAS vezes'),
        'sobe': at('Sobe pelo lado'), 'desce': at('desce pelo lado'), 'cancela': at('cancela a outra'),
        'corrente_zero_b07': at('zero.', after=w('Corrente atravessando', after=w('cancela a outra'))),
        'campo_zero_b07': at('Campo, zero'), 'por_isso': at('É por isso'),
        # B08
        'b08_inicio': at('Agora, o gráfico'), 'aumentando': at('aumentando o raio'), 'no_buraco_zero': at('No buraco, zero'),
        'zero_buraco': at('zero.', after=w('No buraco, zero')), 'entrou': round(w('Entrou no enrolamento'), 3),
        'cai_1_r': at('cai como um sobre o raio'), 'saiu': round(w('Saiu, zero'), 3), 'zero_de_novo': at('zero de novo'),
        'novo_fim': round(w('zero de novo', end=True), 3), 'borda_dentro': at('E na borda de dentro'), 'dobro': at('DOBRO'),
        # B09
        'b09_inicio': at('E dá pra conferir'), 'raio_nao_muda': at('o raio quase não muda'),
        'volta_anel': at('número de espiras dividido'), 'espiras_por_metro': at('vira espiras por metro'),
        'solenoide': at('campo do solenoide'),
        # B10
        'b10_inicio': at('Resumindo'), 'dentro_enrolamento': at('dentro do enrolamento', after=w('Resumindo')),
        'buraco_e_fora': at('No buraco e fora'), 'confina_fim': round(w('próprio campo.', after=w('confina'), end=True), 3),
        'siga': at('Siga o Parallax Lab'),
    }
    for k, v in A.items():
        A[k] = round(v, 3)

    beats = []
    ids = [b for b, *_ in BLOCOS]
    for i, b in enumerate(ids):
        fim = round(beat_start[ids[i + 1]] - LEAD, 3) if i + 1 < len(ids) else total
        beats.append({'id': b, 'inicio_s': round(max(0., beat_start[b] - LEAD), 3) if i else 0., 'fim_s': fim})

    K = tl_k = 3.0 / 2.1
    R_IN, R_MID, R_OUT = round(1.1 * K, 3), round(1.6 * K, 3), round(2.1 * K, 3)
    cd_ini, cd_fim = A['cada_espira'], A['mesmo_sentido_fim']
    tl = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))
    tl['_leia_me'] = ('Fonte única de tempos do vid_0029, SINCRONIZADA com a voz aprovada (gerada por sincronizar.py; não editar '
                      'à mão). "ancoras": instante de cada evento visual (LEAD s antes da palavra). Tempos na montagem do áudio '
                      '(audio/narracao_montagem.wav). Contagens: t_k = inicio + dur * (k/23)^expoente.')
    tl['duracao_s'] = total
    tl['beats'] = beats
    tl['ancoras'] = A
    tl['gaps_inseridos'] = [{'antes_de': p, 'em_s': round(c, 3), 'dur_s': d} for (p, d), (c, _) in zip(GAPS, cuts)]
    tl['eventos'] = {
        'toroide_surge': 0.0, 'corrente_liga': A['liga'], 'campo_acende': A['campo_acende'],
        'camera_topo': round(A['b03_inicio'] - 2.0, 3), 'camera_topo_pousa': round(A['b03_inicio'] + 1.0, 3),
        'desenrola_circulo': A['desenrola'], 'varredura_inicio': A['no_buraco_zero'], 'varredura_fim': A['novo_fim'],
        'camera_solenoide': A['b09_inicio'], 'camera_volta': A['b10_inicio'], 'endcard': A['siga'],
    }
    tl['giro_setas'] = {'inicio_s': A['acompanhar'], 'fim_s': A['b04_inicio'], 'omega_rad_s': 0.12}
    tl['desenrola_circulo'] = {'inicio_s': A['sobra'], 'dur_s': round(A['dois_pi'] - A['sobra'], 3), 'escala': 0.25}
    tl['contagem_dentro'] = {'inicio_s': cd_ini, 'dur_s': round(cd_fim - cd_ini - .3, 3), 'expoente': 0.6,
                             'apaga_s': A['passa']}
    tl['contagem_fora'] = {'todos_dentro_s': A['sobe'], 'inicio_s': A['desce'],
                           'dur_s': round(w('lado de fora.', after=w('desce pelo lado'), end=True) - A['desce'] - .1, 3),
                           'expoente': 0.6, 'apaga_s': A['corrente_zero_b07']}
    tl['realce_3d'] = [{'t': 0.0, 'v': 0.0}, {'t': round(A['b04_inicio'] - .3, 3), 'v': 0.0}, {'t': round(A['b04_inicio'] + .3, 3), 'v': 1.0},
                       {'t': round(A['b09_inicio'] - .2, 3), 'v': 1.0}, {'t': round(A['b09_inicio'] + .4, 3), 'v': 0.0}]
    cam_topo, cam_pousa = tl['eventos']['camera_topo'], tl['eventos']['camera_topo_pousa']
    tl['camera'] = [
        {'t': 0.0, 'modo': 'orbita'}, {'t': cam_topo, 'modo': 'orbita'}, {'t': cam_pousa, 'modo': 'topo'},
        {'t': A['b09_inicio'], 'modo': 'topo'}, {'t': round(A['b09_inicio'] + 2.8, 3), 'modo': 'solenoide'},
        {'t': A['b10_inicio'], 'modo': 'solenoide'}, {'t': round(A['b10_inicio'] + 2.6, 3), 'modo': 'orbita'},
        {'t': A['confina_fim'], 'modo': 'orbita'}, {'t': round(A['confina_fim'] + .5, 3), 'modo': 'preto'},
        {'t': total, 'modo': 'preto'}]
    rb = lambda t: round(t, 3)
    tl['amperiano'] = [
        {'t': 0.0, 'r': R_MID, 'alpha': 0.0}, {'t': A['circulo'], 'r': R_MID, 'alpha': 0.0},
        {'t': rb(A['circulo'] + .7), 'r': R_MID, 'alpha': 1.0},
        {'t': A['buraco'], 'r': R_MID, 'alpha': 1.0}, {'t': rb(A['buraco'] + 1.5), 'r': 1.0, 'alpha': 1.0},
        {'t': A['por_dentro'], 'r': 1.0, 'alpha': 1.0}, {'t': rb(A['por_dentro'] + 1.4), 'r': R_MID, 'alpha': 1.0},
        {'t': A['por_fora'], 'r': R_MID, 'alpha': 1.0}, {'t': rb(A['por_fora'] + 1.5), 'r': 3.3, 'alpha': 1.0},
        {'t': A['b08_inicio'], 'r': 3.3, 'alpha': 1.0}, {'t': rb(A['b08_inicio'] + .5), 'r': 3.3, 'alpha': 0.0},
        {'t': rb(A['no_buraco_zero'] - .3), 'r': 0.0, 'alpha': 0.0},
        {'t': A['no_buraco_zero'], 'r': 0.0, 'alpha': 1.0, 'ease': 'linear'},
        {'t': A['entrou'], 'r': R_IN, 'alpha': 1.0, 'ease': 'linear'},
        {'t': A['saiu'], 'r': R_OUT, 'alpha': 1.0, 'ease': 'linear'},
        {'t': A['novo_fim'], 'r': 3.55, 'alpha': 1.0, 'ease': 'linear'},
        {'t': A['b09_inicio'], 'r': 3.55, 'alpha': 1.0}, {'t': rb(A['b09_inicio'] + .5), 'r': 3.55, 'alpha': 0.0}]
    (UNIT / 'timeline.json').write_text(json.dumps(tl, ensure_ascii=False, indent=2), encoding='utf-8')

    # áudio: a fonte aprovada com os respiros inseridos
    with wave.open(str(UNIT / 'audio' / 'narracao_final.wav')) as f:
        rate, data = f.getframerate(), np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16)
    parts, last = [], 0
    for c, d in cuts:
        k = int(round(c * rate))
        parts += [data[last:k], np.zeros(int(round(d * rate)), np.int16)]
        last = k
    parts.append(data[last:])
    tail = int(round((total - (len(data) / rate + sum(d for _, d in cuts))) * rate))
    parts.append(np.zeros(max(0, tail), np.int16))
    mix = np.concatenate(parts)
    with wave.open(str(UNIT / 'audio' / 'narracao_montagem.wav'), 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(rate); f.writeframes(mix.tobytes())

    # legenda: uma linha por legenda, quebrada na pontuação ou antes de passar de 420 px (Arial 23 px, estilo compacto)
    from PIL import ImageFont
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 23)
    phrases, cur = [], []
    for (beat, word), (s0, e0) in zip(texto, times):
        shown = word if word not in ('PRENDE', 'DUAS', 'DOBRO') else word.lower()
        cur.append((shown, s0, e0))
        line = ' '.join(x for x, _, _ in cur)
        if re.search(r'[.?!:;]$', word) or (word.endswith(',') and font.getlength(line) > 180):
            phrases.append(cur); cur = []
    if cur:
        phrases.append(cur)
    cues, cur = [], []
    for ph in phrases:   # frase longa: partes de largura equilibrada, nunca acima de 420 px
        width = font.getlength(' '.join(x for x, _, _ in ph))
        n = int(np.ceil(width / 420))
        if n <= 1:
            cues.append(ph); continue
        acc, part, target = 0., [], width / n
        for item in ph:
            part.append(item); acc += font.getlength(item[0] + ' ')
            if acc >= target * (len(cues) - len(cues) + 1) and len(part) > 1 and font.getlength(' '.join(x for x, _, _ in part)) >= target * .85:
                cues.append(part); part, acc = [], 0.
        if part:
            if font.getlength(' '.join(x for x, _, _ in cues[-1] + part)) <= 420 and len(part) == 1:
                cues[-1] = cues[-1] + part
            else:
                cues.append(part)
    srt = []
    for i, c in enumerate(cues):
        start = c[0][1]
        end = min(c[-1][2] + .25, cues[i + 1][0][1] - .02) if i + 1 < len(cues) else c[-1][2] + .5
        txt = ' '.join(x for x, _, _ in c).rstrip(',;:')
        stamp = lambda t: f'{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)) % 1000:03d}'
        srt.append(f'{i + 1}\n{stamp(start)} --> {stamp(end)}\n{txt}\n')
    (UNIT / 'legenda.srt').write_text('\n'.join(srt), encoding='utf-8')
    print(json.dumps({'voz_fim_s': round(voice_end, 2), 'duracao_s': total, 'gaps': tl['gaps_inseridos'],
                      'legendas': len(cues), 'beats': {b['id']: (b['inicio_s'], b['fim_s']) for b in beats}}, ensure_ascii=False))


if __name__ == '__main__':
    main()
