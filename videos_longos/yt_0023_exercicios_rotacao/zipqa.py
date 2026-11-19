import glob
import os
import zipfile

z = zipfile.ZipFile('renders/qa_yt0023_v2.zip', 'w', zipfile.ZIP_DEFLATED)
fs = ['renders/qa.txt', 'renders/_longos.txt', 'renders/capitulos_v2.txt', 'capitulos_youtube.txt', 'ficha.md', 'ancoras.json']
for pat in ('renders/prancha_*.png', 'renders/conferencia/*', 'renders/conc_objetos.txt', 'log_*.txt', '*.py', 'threejs/cena3d/*.js', 'threejs/*.js'):
    fs += glob.glob(pat)
for p in fs:
    if os.path.isfile(p) and not p.endswith('.mp4'):
        z.write(p, 'yt_0023/' + p.replace(os.sep, '/'))
z.close()
print(os.path.getsize('renders/qa_yt0023_v2.zip') / 1e6, 'MB')
