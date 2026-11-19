"""Atraso por âncora (início real do vídeo final − início na voz) e dos gatilhos de fala (gat) — QA de sincronia."""
import json, re, av
anc = json.load(open('ancoras.json', encoding='utf-8'))['ancoras']
L = ["PH", "PE1a", "PE1b", "PE2", "PE3", "PE4", "PS"]
off, rows, gs = 0.0, [], []
for l in L:
    n = av.open(f"media_F_{l}/videos/cena/1080p30/{l}.mp4").streams.video[0].frames
    log = open(f'log_F_{l}.txt', encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'\[ancora\] (\S+) ([0-9.]+)', log):
        a = m.group(1)
        if a not in anc: continue
        real = off + float(m.group(2)); rows.append((a, real - anc[a]['ini'], real))
    for m in re.finditer(r'\[gatilho\] (\S+) ([0-9.]+) (.+)', log):
        gs.append((m.group(1), float(m.group(2)), m.group(3)))
    off += n / 30
print('duração total', round(off, 2), 's; voz', anc['EN2']['fim'])
mx = max(rows, key=lambda r: abs(r[1]))
print(f'âncoras: {len(rows)}; atraso máx {mx[1]:+.2f} s em {mx[0]}; |atraso|>0.2 s em {sum(abs(r[1]) > 0.2 for r in rows)}')
for a, d, r in rows:
    print(f'{a:6s} {anc[a]["ini"]:8.2f} {r:8.2f} {d:+6.2f}')
json.dump({a: d for a, d, r in rows}, open('renders/atraso_final.json', 'w'))
