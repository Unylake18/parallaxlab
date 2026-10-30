"""Legenda do vid_0028 a partir de alinhamento_sync.json (palavras já no tempo do VÍDEO: voz + pausas de sync_voz.py).
Até 2 linhas por bloco, sem sobreposição; nenhum bloco atravessa uma pausa; frases coloridas (cores_legenda.py) não quebram.
Uso: python gerar_legenda.py [LARGURA_MAX_LINHA]    Saída: legenda.srt (texto sem tags de áudio)."""
import json
import re
import sys
from pathlib import Path

PASTA = Path(__file__).absolute().parent
MAXL = int(sys.argv[1]) if len(sys.argv) > 1 else 30      # caracteres por linha
pal = json.loads((PASTA / 'alinhamento_sync.json').read_text(encoding='utf-8'))
FIM = ('.', '?', '!', ':')
PAUSA = .45                                               # silêncio que separa blocos
FRACAS = {'a', 'o', 'as', 'os', 'da', 'de', 'do', 'das', 'dos', 'e', 'em', 'um', 'uma', 'que', 'por', 'para', 'com', 'num', 'sobre', 'pela', 'pelo', 'cento', 'vírgula', 'ao', 'à', 'no', 'na'}

sys.path.insert(0, str(PASTA))
from cores_legenda import SUBTITLE_TERM_COLORS  # noqa: E402
FRASES = sorted({t for t in SUBTITLE_TERM_COLORS if ' ' in t and len(t) <= MAXL}, key=lambda t: -len(t.split()))
norm = lambda w: re.sub(r'[^\wáéíóúâêôãõàçü]', '', w.lower())


def agrupa(tokens):
    """junta as palavras de uma frase colorida num único token (nunca quebra no meio)"""
    saida, i = [], 0
    while i < len(tokens):
        for f in FRASES:
            n = len(f.split())
            if [norm(x) for x in tokens[i:i + n]] == [norm(x) for x in f.split()]:
                saida.append(' '.join(tokens[i:i + n]))
                i += n
                break
        else:
            saida.append(tokens[i])
            i += 1
    return saida


def quebra_linhas(tokens):
    """Uma linha se couber; senão, duas balanceadas; só cai na quebra gulosa se não couber em 2."""
    toks = agrupa(tokens)
    if len(' '.join(toks)) <= MAXL:
        return [' '.join(toks)]
    pares = [(' '.join(toks[:k]), ' '.join(toks[k:])) for k in range(1, len(toks))]
    pares = [p for p in pares if len(p[0]) <= MAXL and len(p[1]) <= MAXL]
    if pares:
        return list(min(pares, key=lambda p: max(len(p[0]), len(p[1]))))
    linhas, atual = [], ''
    for t in toks:
        cand = (atual + ' ' + t).strip()
        if len(cand) <= MAXL or not atual:
            atual = cand
        else:
            linhas.append(atual)
            atual = t
    linhas.append(atual)
    return linhas


cues, cur = [], []
for k, w in enumerate(pal):
    if cur and (len(quebra_linhas([x['word'] for x in cur] + [w['word']])) > 2 or w['start'] - cur[-1]['end'] > PAUSA):
        resto = []          # bloco não termina em palavra de ligação ("da", "a", "por"...): ela desce para o próximo
        while len(cur) > 1 and norm(cur[-1]['word']) in FRACAS and cur[-1]['word'] == norm(cur[-1]['word']):
            resto.insert(0, cur.pop())
        cues.append(cur)
        cur = resto
    cur.append(w)
    txt = ' '.join(x['word'] for x in cur)
    if w['word'].endswith(FIM) or (w['word'].endswith(',') and len(txt) >= 24):
        cues.append(cur)
        cur = []
if cur:
    cues.append(cur)

i = 0   # junta blocos muito curtos ao seguinte quando cabe em 2 linhas e não há pausa entre eles
while i < len(cues) - 1:
    dur = cues[i][-1]['end'] - cues[i][0]['start']
    txt = ' '.join(x['word'] for x in cues[i])
    if (dur < .7 or len(txt) < 10) and not txt.endswith(FIM) and len(quebra_linhas([x['word'] for x in cues[i] + cues[i + 1]])) <= 2 \
            and cues[i + 1][0]['start'] - cues[i][-1]['end'] < .4:
        cues[i] = cues[i] + cues.pop(i + 1)
    else:
        i += 1


def ts(t):
    ms = round(t * 1000)
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


saida, prev_fim = [], 0.0
for k, c in enumerate(cues):
    ini = max(c[0]['start'], prev_fim + .02)
    prox = cues[k + 1][0]['start'] if k + 1 < len(cues) else 1e9
    fim = min(c[-1]['end'] + .25, prox - .03)
    fim = max(fim, min(ini + .9, prox - .03))
    if fim <= ini:
        fim = ini + .2
    saida.append(f'{k + 1}\n{ts(ini)} --> {ts(fim)}\n' + '\n'.join(quebra_linhas([x['word'] for x in c])))
    prev_fim = fim
(PASTA / 'legenda.srt').write_text('\n\n'.join(saida) + '\n', encoding='utf-8')
print(len(cues), 'blocos; maior linha', max(len(l) for c in cues for l in quebra_linhas([x['word'] for x in c])), 'caracteres')
