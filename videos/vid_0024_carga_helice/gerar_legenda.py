"""Legenda do vid_0024 a partir do alinhamento forçado (alinhamento_palavras.json): tempos exatos por palavra.
Saída: legenda.srt (até 2 linhas por bloco, sem sobreposição). Uso: python gerar_legenda.py [LARGURA_MAX_LINHA]"""
import json, sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
MAXL = int(sys.argv[1]) if len(sys.argv) > 1 else 30      # caracteres por linha
pal = json.loads((PASTA / 'alinhamento_palavras.json').read_text(encoding='utf-8'))
FIM = ('.', '?', '!', ':')


def quebra_linhas(tokens):
    linhas, atual = [], ''
    for t in tokens:
        cand = (atual + ' ' + t).strip()
        if len(cand) <= MAXL or not atual:
            atual = cand
        else:
            linhas.append(atual); atual = t
    linhas.append(atual)
    return linhas


cues, cur = [], []          # cur: lista de palavras (dict)
def fecha():
    global cur
    if cur:
        cues.append(cur); cur = []

for w in pal:
    prova = quebra_linhas([x['word'] for x in cur] + [w['word']])
    if len(prova) > 2:      # estouraria 2 linhas: fecha antes desta palavra
        fecha()
    cur.append(w)
    txt = ' '.join(x['word'] for x in cur)
    if w['word'].endswith(FIM) or (w['word'].endswith(',') and len(txt) >= 24):
        fecha()
fecha()

# junta blocos muito curtos (< 0,7 s ou < 10 caracteres) ao vizinho quando cabe em 2 linhas
i = 0
while i < len(cues) - 1:
    dur = cues[i][-1]['end'] - cues[i][0]['start']
    txt = ' '.join(x['word'] for x in cues[i])
    if (dur < 0.7 or len(txt) < 10) and len(quebra_linhas([x['word'] for x in cues[i] + cues[i + 1]])) <= 2 \
            and cues[i + 1][0]['start'] - cues[i][-1]['end'] < 0.6:
        cues[i] = cues[i] + cues.pop(i + 1)
    else:
        i += 1


def ts(t):
    ms = round(t * 1000); s, ms = divmod(ms, 1000); m, s = divmod(s, 60); h, m = divmod(m, 60)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


saida, prev_fim = [], 0.0
for k, c in enumerate(cues):
    ini = max(c[0]['start'], prev_fim + 0.02)
    prox = cues[k + 1][0]['start'] if k + 1 < len(cues) else 1e9
    fim = min(c[-1]['end'] + 0.25, prox - 0.03)
    fim = max(fim, min(ini + 0.9, prox - 0.03))
    if fim <= ini: fim = ini + 0.2
    linhas = quebra_linhas([x['word'] for x in c])
    saida.append(f'{k + 1}\n{ts(ini)} --> {ts(fim)}\n' + '\n'.join(linhas))
    prev_fim = fim
(PASTA / 'legenda.srt').write_text('\n\n'.join(saida) + '\n', encoding='utf-8')
print(len(cues), 'blocos; maior linha', max(len(l) for c in cues for l in quebra_linhas([x['word'] for x in c])), 'caracteres')
