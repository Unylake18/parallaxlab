"""Zip para o GPT: um quadro a cada 3 (5 fps, JPG) do preview + MP4 + stills + cena/ficha/narração; e prancha de 60 quadros.
uso: python zip_gpt_v7.py → renders/v7_para_gpt.zip, renders/prancha_v7.png"""
import av, io, zipfile, glob, os
from PIL import Image, ImageDraw
SRC, ZP, FPS = 'renders/preview_yt0016_v7_960x540.mp4', 'renders/v7_para_gpt.zip', 15
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
    for f in glob.glob('renders/stills_v7/*.png'):
        z.write(f, os.path.basename(f))
    for f in ['renders/look_v7.png', 'renders/antes_depois_v7.png', 'renders/residuos_v7.png', 'renders/capitulos_v7.txt', 'ancoras.json',
              'handoff_v7.md', 'ficha.md', 'cena.py', 'kit.py', *sorted(glob.glob('sec_*.py')), *[j for j in sorted(glob.glob('threejs/cena3d/*.js')) if os.path.basename(j) not in ('three.min.js', 'GLTFLoader.js', 'cavalo_glb.js', 'fundo_lab.js')],
              'threejs/r3d.js', 'fundo_lab.py', 'assets_unidade/fundo_lab_960x540.png', 'sprites_v7.py', 'sonda_v7.py', 'montar_preview_v7.py',
              'congelado_v7.py', 'contraste_v7.py', 'qa_alinhamento_v7.py', 'qa_sync_v7.py', 'stills_v7.py', 'aud_v7.sh', 'lote_v7.sh',
              *sorted(glob.glob('log_*_v7.txt')), *sorted(glob.glob('log_3d_*.txt')), *sorted(glob.glob('audit_*.txt')), 'renders/prancha_v7.png']:
        if not os.path.exists(f):
            continue
        z.write(f, f.replace('renders/', '') if '/' in f and not f.startswith('threejs') else os.path.basename(f))
W, H = 320, 180
sh = Image.new('RGB', (W * 6, (H + 16) * 10), 'black'); d = ImageDraw.Draw(sh)
for k, (i, t) in enumerate(thumbs[:60]):
    x, y = (k % 6) * W, (k // 6) * (H + 16); sh.paste(t, (x, y + 16)); s = i / FPS
    d.text((x + 4, y + 2), f'{int(s // 60)}:{s % 60:04.1f}', fill='yellow')
sh.save('renders/prancha_v7.png')
print(tot, 'quadros', round(os.path.getsize(ZP) / 1e6, 1), 'MB')
