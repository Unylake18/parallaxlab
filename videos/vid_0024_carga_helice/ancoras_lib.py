import json, re
from pathlib import Path
PASTA = Path(__file__).resolve().parent
norm = lambda s: re.sub(r'[^\wáéíóúâêôãõàçü]', '', s.lower())
PAL = json.loads((PASTA / 'alinhamento_palavras.json').read_text(encoding='utf-8'))
W = [norm(p['word']) for p in PAL]
def acha(frase, apos=0, borda='i'):
    seq = [norm(x) for x in frase.split()]
    for i in range(apos, len(W) - len(seq) + 1):
        if W[i:i + len(seq)] == seq:
            return i, (PAL[i]['start'] if borda == 'i' else PAL[i + len(seq) - 1]['end'])
    raise KeyError(frase)
