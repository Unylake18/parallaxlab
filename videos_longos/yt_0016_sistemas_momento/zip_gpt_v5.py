"""Zip para o GPT: um quadro a cada 3 (5 fps, JPG) do preview + MP4 + stills + cena/ficha/narração; e prancha de 60 quadros.
uso: python zip_gpt_v3.py → renders/v5_para_gpt.zip, renders/prancha_v5.png"""
import av, io, zipfile, glob, os
from PIL import Image, ImageDraw
SRC, ZP, FPS = 'renders/preview_yt0016_v5_960x540.mp4', 'renders/v5_para_gpt.zip', 15
c = av.open(SRC); st = c.streams.video[0]
dur = float(st.frames) / FPS if st.frames else 1210.0
alvo = set(int(i * (dur - 0.7) / 59 * FPS) for i in range(60))
thumbs, tot = [], 0
with zipfile.ZipFile(ZP, 'w', zipfile.ZIP_STORED) as z:
    for i, fr in enumerate(c.decode(st)):
        if i % 3 and i not in alvo:
            continue
        im = fr.to_image()
        if i % 3 == 0:
            b = io.BytesIO(); im.save(b, 'JPEG', quality=85)
            z.writestr(f'quadros/q{i:05d}_{i / FPS:07.2f}s.jpg', b.getvalue()); tot += 1
        if i in alvo:
            thumbs.append((i, im.resize((320, 180))))
    z.write(SRC, os.path.basename(SRC))
    for f in glob.glob('renders/stills_v5/*.png'):
        z.write(f, os.path.basename(f))
    for f in ['cena.py', 'kit.py', *sorted(glob.glob('sec_*.py')), 'renders/capitulos_v5.txt', 'renders/stills_v5_prancha.png', 'ficha.md',
              'narracao_final_v4.md', 'narracao_tags.md', 'handoff_v5.md', 'ancoras.json', 'mapa_ancoras_v5.txt', 'gerar_ancoras.py',
              'alinhamento_palavras.json', 'audio/asr_v4.json', 'audio/blocos_v4.json', 'voz_v4.py', 'alinhar_voz.py', 'montar_preview_v5.py',
              'qa_alinhamento_v5.py', 'qa_travadas.py', 'qa_sync_v5.py', 'renders/prancha_v5.png', *sorted(glob.glob('renders/ancoras_v5/*.png')), *sorted(glob.glob('log_*_v5.txt')), 'log_voz_v4.txt']:
        if not os.path.exists(f):
            continue
        z.write(f, os.path.basename(f))
W, H = 320, 180
sh = Image.new('RGB', (W * 6, (H + 16) * 10), 'black'); d = ImageDraw.Draw(sh)
for k, (i, t) in enumerate(thumbs[:60]):
    x, y = (k % 6) * W, (k // 6) * (H + 16); sh.paste(t, (x, y + 16)); s = i / FPS
    d.text((x + 4, y + 2), f'{int(s // 60)}:{s % 60:04.1f}', fill='yellow')
sh.save('renders/prancha_v5.png')
print(tot, 'quadros', round(os.path.getsize(ZP) / 1e6, 1), 'MB')
