import json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image
U = Path(__file__).resolve().parent
d = json.loads((U / 'threejs/pedidos3d/PB6.json').read_text(encoding='utf-8'))
e0 = [x for x in d['cenas']['mesa_furo'] if x[0] == 1356][0][1]
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
def roda(nome, e):
    out = U / f'renders/v5/est2_{nome}.png'
    subprocess.run(['node', 'r3d.js', '--sonda', 'mesa_furo', '--estado', json.dumps(e), '--png', str(out)], cwd=U/'threejs', capture_output=True, text=True, check=True)
    a = np.asarray(Image.open(out).convert('RGBA'), float)/255
    L = lum(a[..., :3])
    return round(float(L[270:325, 235:315].max()), 3)
var = {'base': e0}
v = json.loads(json.dumps(e0)); v['aneis'] = {'r30': 0, 'r60': 0}; var['sem_aneis'] = v
v = json.loads(json.dumps(e0)); v['rastro'] = []; var['sem_rastro'] = v
v = json.loads(json.dumps(e0)); v['disco'] = None; var['sem_disco'] = v
v = json.loads(json.dumps(e0)); v['solT'] = 0.0; var['sol0'] = v
for k, e in var.items():
    print(k, roda(k, e))
