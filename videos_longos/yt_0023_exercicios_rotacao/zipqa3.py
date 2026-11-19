import glob, os, zipfile
z = zipfile.ZipFile('renders/qa_yt0023_v3.zip', 'w', zipfile.ZIP_DEFLATED)
fs = ['renders/qa.txt', 'renders/capitulos_v3.txt', 'capitulos_youtube.txt', 'ficha.md', 'ancoras.json', 'renders/prancha_objetos.png', 'renders/conc_objetos.txt', 'renders/prancha_conferencia_v3.png', 'renders/prancha_PE3.png', 'renders/prancha_PE1a.png']
for pat in ('renders/conferencia_v3/*', 'renders/objetos/*.png', 'log_*.txt', '*.py', 'threejs/cena3d/f23.js', 'threejs/*.js'):
    fs += glob.glob(pat)
for p in fs:
    if os.path.isfile(p) and not p.endswith('.mp4'):
        z.write(p, 'yt_0023/' + p.replace(os.sep, '/'))
z.close(); print(os.path.getsize('renders/qa_yt0023_v3.zip') / 1e6, 'MB')
