"""Confere o sync do vid_0028: cada evento da cena (estados do Manim) contra o timeline e contra a palavra da voz.
Atraso = quanto a imagem chega DEPOIS da palavra (positivo = imagem atrasada). Limite pedido: 0,2 s.
Uso: python conferir_sync.py media_sync/estados_vid0028_sync.json"""
import json
import sys
from pathlib import Path

U = Path(__file__).absolute().parent
est = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
tl = json.loads((U / 'timeline.json').read_text(encoding='utf-8'))
rel = json.loads((U / 'sync_relatorio.json').read_text(encoding='utf-8'))
cena = {e['estado']: e['segundos'] for e in est['eventos']}
desvio = max(abs(cena[k] - v) for k, v in tl['eventos'].items() if k in cena)
atrasos = [(a['evento'], round(cena[a['evento']] - a['voz_s'], 3)) for a in rel['ancoras']]
pior = max(atrasos, key=lambda x: x[1])
print(f"eventos da cena × timeline: maior desvio {desvio:.3f} s · atrasos do Manim: {est['atrasos'] or 'nenhum'}")
print(f"âncoras {len(atrasos)}: imagem − voz de {min(a for _, a in atrasos):+.3f} a {pior[1]:+.3f} s (pior: {pior[0]})")
print(f"duração {est['duracao']} s · {est['quadros']} quadros")
ok = pior[1] <= .2 and not est['atrasos']
print('OK: nenhuma âncora com a imagem mais de 0,2 s atrás da voz' if ok else 'FALHOU')
sys.exit(0 if ok else 1)
