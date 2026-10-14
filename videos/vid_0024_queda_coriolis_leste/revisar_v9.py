"""Inspeção localizada dos estados críticos V9; não executa QA integral."""
import json
from pathlib import Path
import av
from PIL import Image, ImageDraw

UNIT = Path(__file__).resolve().parent
VIDEO = UNIT / 'media_v9/videos/cena/960p15/QuedaCoriolis024.mp4'
OUT = UNIT / 'qa_v9'
OUT.mkdir(exist_ok=True)
marks = json.loads((UNIT / 'qa_v9_timestamps.json').read_text(encoding='utf-8'))
c = av.open(str(VIDEO))
s = c.streams.video[0]
duration = float(s.duration * s.time_base)

def extract(t, name):
    t = max(0, min(t, duration - .15))
    c.seek(int(t / s.time_base), stream=s)
    for f in c.decode(s):
        if float(f.pts * s.time_base) >= t:
            path = OUT / f'{name}.png'
            f.to_image().save(path)
            return {'t': round(t, 3), 'arquivo': path.name}
    raise RuntimeError(f'Quadro não encontrado em {t}')

wanted = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 20, 21, 23, 25, 26}
selected = []
for m in marks:
    n = int(m['estado'].split()[0])
    if n in wanted:
        selected.append({**m, **extract(m['t'] - .13, f'estado_{n:02d}')})

# Somente as duas pontes e a sincronização do nascimento de x̂/leste.
by = {int(m['estado'].split()[0]): m for m in marks}
for name, t in [('norte_em_perspectiva', (by[6]['t'] + by[7]['t']) / 2),
                ('zoom_em_P', (by[7]['t'] + by[8]['t']) / 2),
                ('antes_de_leste', by[16]['t'] + .65),
                ('nascimento_de_leste', by[16]['t'] + .84)]:
    selected.append({'estado': name, **extract(t, name)})

for start in range(0, len(selected), 12):
    sheet = Image.new('RGB', (1160, 1560), '#151b2a')
    for j, m in enumerate(selected[start:start + 12]):
        tile = Image.new('RGB', (290, 520), '#151b2a')
        tile.paste(Image.open(OUT / m['arquivo']).resize((270, 480)), (10, 28))
        label = m['estado'].split()[0]
        ImageDraw.Draw(tile).text((10, 6), f'{label} | {m["t"]:.2f}s', fill='white')
        sheet.paste(tile, ((j % 4) * 290, (j // 4) * 520))
    sheet.save(OUT / f'estados_criticos_{start // 12 + 1:02d}.jpg')

metadata = {'video': str(VIDEO), 'duracao': duration, 'largura': s.width,
            'altura': s.height, 'fps_medio': float(s.average_rate),
            'escopo': '21 estados críticos e 4 quadros locais de transição; sem QA completo',
            'estados': selected}
(OUT / 'verificacao_localizada.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
c.close()
print(json.dumps({k: v for k, v in metadata.items() if k != 'estados'}, ensure_ascii=False, indent=2))
