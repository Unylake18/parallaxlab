"""Gera a narração em blocos de parágrafos inteiros (fronteiras entre âncoras), salva cada bloco e emenda sem silêncio inserido."""
import os, sys, json, re, wave
sys.path.insert(0, '../../videos')
import gerar_voz_elevenlabs as g
VOZ = 'qw7jgPZWOKrl10GsjQ82'; LIM = 4600
src = open('narracao_final_fonte.md', encoding='utf-8').read()
pars = [(m.group(1), m.group(2).strip()) for m in re.finditer(r'^\{([^}]+)\} (.+)$', src, flags=re.M)]
blocos, atual, ids = [], [], []
for i, t in pars:
    if atual and sum(len(x) for x in atual) + 2 * len(atual) + len(t) > LIM:
        blocos.append((ids, atual)); atual, ids = [], []
    atual.append(t); ids.append(i)
blocos.append((ids, atual))
json.dump([{'n': k + 1, 'ids': b[0], 'chars': sum(len(x) for x in b[1])} for k, b in enumerate(blocos)], open('audio/blocos.json', 'w'), indent=1)
chave = os.environ['ELEVENLABS_API_KEY']
só = [int(x) for x in sys.argv[1:]]
for k, (ids, ts) in enumerate(blocos, 1):
    arq = f'audio/bloco_{k}.wav'
    if (só and k not in só) or (not só and os.path.exists(arq)): continue
    print(f'bloco {k}/{len(blocos)} {ids[0]}..{ids[-1]} {sum(map(len, ts))} chars', flush=True)
    dados = g.sintetizar(chave, VOZ, 'eleven_v4', 'mp3_44100_192', '\n\n'.join(ts), '', '', None)
    pcm = g.decodificar_mp3(dados)
    with wave.open(arq, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes(pcm)
pcm = b''
for k in range(1, len(blocos) + 1):
    with wave.open(f'audio/bloco_{k}.wav') as w: pcm += w.readframes(w.getnframes())
with wave.open('audio/narracao_v3.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes(pcm)
print('narracao_v3.wav', len(pcm) / 2 / 44100, 's')
