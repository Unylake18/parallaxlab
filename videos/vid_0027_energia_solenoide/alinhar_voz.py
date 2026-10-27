"""Alinhamento forçado (ElevenLabs /v1/forced-alignment) da narração do vid_0027: instante exato de cada palavra.
Uso: ELEVENLABS_API_KEY no ambiente; uv run --no-sync python alinhar_voz.py
Entrada: narracao_tags_v4.md (texto sem tags) + audio/narracao_v4.wav. Saída: alinhamento_palavras.json e texto_narracao.txt."""
import json, os, re, uuid, urllib.request
from pathlib import Path

PASTA = Path(__file__).absolute().parent
md = (PASTA / 'narracao_tags_v4.md').read_text(encoding='utf-8').split('## Texto corrido (para gravação)')[1].split('\n## ')[0]
texto = re.sub(r'\s+', ' ', re.sub(r'\[[^\]]*\]', '', md)).strip()
(PASTA / 'texto_narracao.txt').write_text(texto, encoding='utf-8')
wav = (PASTA / 'audio' / 'narracao_v4.wav').read_bytes()
b = uuid.uuid4().hex
corpo = b''.join([
    f'--{b}\r\nContent-Disposition: form-data; name="text"\r\n\r\n'.encode(), texto.encode('utf-8'), b'\r\n',
    f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="narracao.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode(), wav, b'\r\n',
    f'--{b}--\r\n'.encode()])
req = urllib.request.Request('https://api.elevenlabs.io/v1/forced-alignment', data=corpo, method='POST',
    headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': f'multipart/form-data; boundary={b}'})
r = json.loads(urllib.request.urlopen(req, timeout=300).read())
pal = [dict(word=w['text'].strip(), start=round(w['start'], 3), end=round(w['end'], 3), loss=round(w.get('loss', 0), 3))
       for w in r['words'] if w['text'].strip()]
(PASTA / 'alinhamento_palavras.json').write_text(json.dumps(pal, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(pal), 'palavras; perda média', round(r.get('loss', 0), 3), '; fim', pal[-1]['end'])
