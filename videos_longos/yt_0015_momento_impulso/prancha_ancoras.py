"""python prancha_ancoras.py Lote id1 id2 ... → renders/_<Lote>_<k>.png (fim de cada âncora, 6 por prancha). Tempo = soma das durações + folga."""
import json, subprocess, sys
ANC = json.load(open('ancoras.json', encoding='utf-8'))['ancoras']
lote, ids = sys.argv[1], sys.argv[2:]
t, ts = 0.0, []
for a in ids:
    t += ANC[a]['dur']
    ts.append(t)
vid = f'media_{lote}/videos/cena/540p15/{lote}.mp4'
PY = 'C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe'
for k in range(0, len(ts), 6):
    sel = [max(0.5, x - 0.8 + 0.9 * (k // 6 + 0) ) for x in ts[k:k + 6]]
    subprocess.run([PY, 'prancha.py', vid, f'renders/_{lote}_{k // 6}.png', *[f'{x:.2f}' for x in sel]])
