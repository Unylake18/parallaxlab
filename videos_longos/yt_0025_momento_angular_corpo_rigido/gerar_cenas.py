"""Porta somente renderer/luz/câmera/pós do kit 24; geometria própria na unidade 25."""
from pathlib import Path
import json
U=Path(__file__).resolve().parent
inicio=U/'threejs/renderer25_inicio.js';pos=U/'threejs/renderer25_pos.js'
if not inicio.exists() or not pos.exists():
    src=(U/'threejs/cena3d/cenas25.js').read_text(encoding='utf-8')
    inicio.write_text(src[src.index('(function ()'):src.index('  const fis=')],encoding='utf-8')
    pos.write_text(src[src.index('  // ── câmeras:'):src.index('  const depthRT=')],encoding='utf-8')
cab=inicio.read_text(encoding='utf-8');camera=pos.read_text(encoding='utf-8')
camera=camera.replace('if (o.isMesh && !brilho.includes(o))','if (o.isMesh && !brilho.includes(o) && !(o.material.userData && o.material.userData.fantasma))')
custom=(U/'threejs/geometrias25.js').read_text(encoding='utf-8')
estado=(U/'threejs/estado25.js').read_text(encoding='utf-8')
(U/'threejs/cena3d/cenas25.js').write_text('// Renderer HDR/PBR, ambiente, câmera e bloom portados de mesa.js do yt_0024.\n'+cab+custom+camera+estado+'\n})();\n',encoding='utf-8')
fis=json.loads((U/'tab25.json').read_text(encoding='utf-8'))
html='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent;overflow:hidden}canvas{display:block}</style></head><body><script>window.FISICA25=FISICA;</script><script src="three.min.js"></script><script src="cenas25.js"></script></body></html>'''.replace('FISICA;',json.dumps(fis)+';')
for nome in ('pendulo_conico','corpo_voxel','haltere_torto','roda_balanceamento','bancada_dupla','plataforma_livre'):
    (U/f'threejs/cena3d/{nome}.html').write_text(html,encoding='utf-8')
