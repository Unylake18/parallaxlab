"""Gera audio/narracao_final.wav (voz gravada + pausa para a conferência + cauda do cartão final) e
os tempos finais: alinhamento_final.json e legenda.srt. Entrada: gerar_sync.py já rodado."""
import json
import re
import wave
from pathlib import Path

import numpy as np

PASTA = Path(__file__).resolve().parent
PAUSA_CONFERENCIA = 1.6     # s inseridos entre "…seis graus." e "Puxando na horizontal"
CAUDA = 2.4                 # s de silêncio após a última palavra (logo + @labparallax)

pal = json.loads((PASTA / 'alinhamento_palavras.json').read_text(encoding='utf-8'))
idx = max(i for i, p in enumerate(pal) if p['word'] == 'graus.')
ponto = (pal[idx]['end'] + pal[idx + 1]['start']) / 2
print('pausa inserida em', round(ponto, 3), 's, após', pal[idx]['word'], 'antes de', pal[idx + 1]['word'])

with wave.open(str(PASTA / 'audio' / 'narracao_gravada.wav')) as w:
    p = w.getparams()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, p.nchannels)
sr = p.framerate
k = int(round(ponto * sr))
y = np.concatenate([x[:k], np.zeros((int(PAUSA_CONFERENCIA * sr), p.nchannels), np.int16), x[k:],
                    np.zeros((int(CAUDA * sr), p.nchannels), np.int16)])
with wave.open(str(PASTA / 'audio' / 'narracao_final.wav'), 'wb') as o:
    o.setparams(p)
    o.writeframes(y.tobytes())
print('narracao_final.wav', round(len(y) / sr, 3), 's')

shift = lambda t: t + (PAUSA_CONFERENCIA if t > ponto else 0.0)
fin = [dict(word=q['word'], start=round(shift(q['start']), 4), end=round(shift(q['end']), 4)) for q in pal]
(PASTA / 'alinhamento_final.json').write_text(json.dumps(fin, ensure_ascii=False, indent=2), encoding='utf-8')


def sec(s):
    h, m, r = s.split(':'); sg, ms = r.split(','); return int(h) * 3600 + int(m) * 60 + int(sg) + int(ms) / 1000


def ts(t):
    total = round(t * 1000); s, ms = divmod(total, 1000); m, s = divmod(s, 60); h, m = divmod(m, 60)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


out = []
for blk in re.split(r'\n\s*\n', (PASTA / 'legenda_gravada.srt').read_text(encoding='utf-8').strip()):
    l = blk.splitlines()
    a, b = (sec(z) for z in l[1].split(' --> '))
    out.append(f'{l[0]}\n{ts(shift(a))} --> {ts(shift(b))}\n' + '\n'.join(l[2:]))
(PASTA / 'legenda.srt').write_text('\n\n'.join(out) + '\n', encoding='utf-8')
print('legenda.srt', len(out), 'blocos')
