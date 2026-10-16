"""Âncoras partitura(V6, marcos_score.json) -> tempo real da voz (alinhamento_final.json). Saída: ancoras.json."""
import json
import re
import wave
from pathlib import Path

PASTA = Path(__file__).resolve().parent
pal = json.loads((PASTA / 'alinhamento_final.json').read_text(encoding='utf-8'))
marcas = json.loads((PASTA / 'marcos_score.json').read_text(encoding='utf-8'))
norm = lambda s: re.sub(r'[^\wáéíóúâêôãõàç]', '', s.lower())
W = [norm(p['word']) for p in pal]

# marca -> (frase falada, borda 'i' início | 'f' fim, deslocamento em s)
F = dict(
    intro=('imagine', 'i', 0), idf=('a corda puxa', 'i', 0), arc=('formando', 'i', 0), sw1=('horizontal', 'i', 0),
    comp=('primeiro', 'i', 0), ind1=('a horizontal', 'i', 0), ind2=('e a vertical', 'i', 0), sw2=('mudando', 'i', 0),
    vert=('agora olha', 'i', 0), wn=('o peso', 'i', 0), stack=('equilibrado', 'i', 0), eq1a=('mais a parte', 'i', 0),
    eq1b=('ou seja', 'i', 0), sw3=('quanto mais', 'i', 0), atr=('e o atrito', 'i', 0), eq2=('o atrito estático', 'i', 0),
    sw4=('então se', 'i', 0), lim=('no limiar', 'i', 0), eqA=('a parte horizontal', 'i', 0), ind3=('ao atrito', 'i', 0),
    sw5=('é o momento', 'i', 0), B=('então trocamos', 'i', 0), C=('lembrando', 'i', 0), D=('agora distribuímos', 'i', 0),
    E=('depois passamos', 'i', 0), Fa=('e colocamos', 'i', 0), annot=('por fim', 'i', 0), fin=('e chegamos', 'i', 0),
    boxf=('cada ângulo', 'i', 0),
    reorg=('para enxergar', 'i', 0), dot=('a força necessária na', 'i', 0), zero=('na horizontal', 'i', 0),
    ev=('o ângulo é zero', 'i', 0), ev98=('dá noventa', 'i', 0), curve=('agora aumentamos', 'i', 0),
    ret=('por isso', 'i', 0), halo=('o ângulo ideal', 'i', 0), labs=('de cerca', 'i', 0), lm=('para achar', 'i', 0), num=('o numerador', 'i', 0), den=('então quanto', 'i', 0),
    d1=('por isso procuramos', 'i', 0), d2=('no máximo do', 'i', 0), d2b=('isso dá', 'i', 0), d2c=('dividindo', 'i', 0),
    d3=('a tangente', 'i', 0), frame=('igual ao coeficiente', 'i', 0), d4=('com coeficiente zero', 'i', 0),
    chk=('seis graus', 'f', 0), cmp1=('puxando na', 'i', -0.05), cmp2=('no ângulo ideal', 'i', 0),
    red=('de cerca de dez', 'i', 0),
)
out, pos = [], 0
for nome, score in sorted(marcas.items(), key=lambda kv: kv[1]):
    frase, borda, off = F[nome]
    seq = [norm(x) for x in frase.split()]
    k = next(i for i in range(pos, len(W) - len(seq) + 1) if W[i:i + len(seq)] == seq)
    t = (pal[k]['start'] if borda == 'i' else pal[k + len(seq) - 1]['end']) + off
    out.append((nome, score, round(t, 3)))
    pos = k + 1
ok = True
for (n0, s0, r0), (n1, s1, r1) in zip(out, out[1:]):
    f = (r1 - r0) / (s1 - s0)
    marca = '' if 0.55 <= f <= 1.8 else ('  <-- APERTADO' if f < 0.55 else '  <-- ESTICADO')
    print(f'{n0:>6}->{n1:<6} score {s1 - s0:5.2f}s real {r1 - r0:5.2f}s x{f:4.2f}{marca}')
    ok &= r1 > r0
assert ok
cta = next(p['start'] for p in pal if norm(p['word']) == 'gostou')
with wave.open(str(PASTA / 'audio' / 'narracao_final.wav')) as w:
    dur = w.getnframes() / w.getframerate()
(PASTA / 'ancoras.json').write_text(json.dumps(dict(map=[[s, r] for _, s, r in out], cta=cta, audio_end=round(dur, 3))), encoding='utf-8')
print('âncoras', len(out), '| cta', cta, '| fim', round(dur, 3))
