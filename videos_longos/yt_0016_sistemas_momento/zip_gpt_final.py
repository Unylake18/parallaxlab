"""Zip para o GPT da versão final: um quadro a cada 6 do master 1080p30 (5 fps, JPG 960×540) + master + .srt + capítulos + ficha; e prancha de 60 quadros.
uso: python zip_gpt_final.py → renders/final_para_gpt.zip, renders/prancha_final.png"""
import av, io, zipfile, os
from PIL import Image, ImageDraw
SRC, ZP, FPS = 'renders/master_yt0016_1920x1080_30fps.mp4', 'renders/final_para_gpt.zip', 30
c = av.open(SRC); st = c.streams.video[0]
dur = float(st.frames) / FPS if st.frames else 1366.7
alvo = set(int(i * (dur - 0.7) / 59 * FPS) for i in range(60))
thumbs, tot = [], 0
with zipfile.ZipFile(ZP, 'w', zipfile.ZIP_STORED) as z:
    for i, fr in enumerate(c.decode(st)):
        if i % 6 and i not in alvo:
            continue
        im = fr.to_image()
        if i % 6 == 0:
            b = io.BytesIO(); im.resize((960, 540), Image.LANCZOS).save(b, 'JPEG', quality=85)
            z.writestr(f'quadros/q{i:05d}_{i / FPS:07.2f}s.jpg', b.getvalue()); tot += 1
        if i in alvo:
            thumbs.append((i, im.resize((320, 180))))
    z.write(SRC, os.path.basename(SRC))
    for f in ['final/legenda - yt0016.srt', 'final/capitulos - yt0016.txt', 'renders/qa_final/en2_granada.png', 'renders/qa_final/t10_1237.png',
              'ficha.md', 'handoff_v7.md', 'ancoras.json', 'sec_fim.py', 'sec_t10.py']:
        if os.path.exists(f):
            z.write(f, os.path.basename(f))
    W, H = 320, 180
    sh = Image.new('RGB', (W * 6, (H + 16) * 10), 'black'); d = ImageDraw.Draw(sh)
    for k, (i, t) in enumerate(thumbs[:60]):
        x, y = (k % 6) * W, (k // 6) * (H + 16); sh.paste(t, (x, y + 16)); s = i / FPS
        d.text((x + 4, y + 2), f'{int(s // 60)}:{s % 60:04.1f}', fill='yellow')
    sh.save('renders/prancha_final.png')
    z.write('renders/prancha_final.png', 'prancha_final.png')
print(tot, 'quadros', round(os.path.getsize(ZP) / 1e6, 1), 'MB')
