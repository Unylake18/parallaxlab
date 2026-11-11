"""yt_0026 (copiado do vid_0033): alinhamento forçado (ElevenLabs /v1/forced-alignment) da voz real + transcrição de conferência (/v1/speech-to-text).
Uso: ELEVENLABS_API_KEY no ambiente; uv run --no-sync python alinhar_voz.py [--stt]
Entrada: narracao_tags.md + audio/narracao_v4.wav. Saída: alinhamento_palavras.json, texto_narracao.txt (e transcricao_stt.json com --stt)."""
import json, os, re, sys, uuid, urllib.request
from pathlib import Path

PASTA = Path(__file__).resolve().parent
md = (PASTA / 'narracao_tags.md').read_text(encoding='utf-8').split('## Texto corrido (para gravação)')[1]
texto = re.sub(r'\s+', ' ', re.sub(r'\[[^\]]*\]', '', md)).strip()
(PASTA / 'texto_narracao.txt').write_text(texto, encoding='utf-8')
wav = (PASTA / 'audio' / 'narracao_v4.wav').read_bytes()


def post(url, campos):
    b = uuid.uuid4().hex
    corpo = b''.join([f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n'.encode() + v.encode('utf-8') + b'\r\n' for k, v in campos.items()]) + \
        f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="narracao.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode() + wav + f'\r\n--{b}--\r\n'.encode()
    req = urllib.request.Request(url, data=corpo, method='POST',
                                 headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': f'multipart/form-data; boundary={b}'})
    return json.loads(urllib.request.urlopen(req, timeout=600).read())


r = post('https://api.elevenlabs.io/v1/forced-alignment', {'text': texto})
pal = [dict(word=w['text'].strip(), start=round(w['start'], 3), end=round(w['end'], 3), loss=round(w.get('loss', 0), 3)) for w in r['words'] if w['text'].strip()]
(PASTA / 'alinhamento_palavras.json').write_text(json.dumps(pal, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(pal), 'palavras; perda média', round(r.get('loss', 0), 3), '; fim', pal[-1]['end'])
if '--stt' in sys.argv:
    s = post('https://api.elevenlabs.io/v1/speech-to-text', {'model_id': 'scribe_v1', 'language_code': 'por'})
    (PASTA / 'transcricao_stt.json').write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding='utf-8')
    print('stt:', len(s.get('text', '')), 'caracteres')
