import collections
by = collections.defaultdict(dict)
for ln in open('remapa_gat.txt', encoding='utf-8'):
    ln = ln.rstrip('\n')
    if not ln:
        continue
    fl, old, new = ln.split('|')
    f, n = fl.split(':')
    by[f][int(n)] = (old, new)
bad = 0
for f, d in by.items():
    L = open(f, encoding='utf-8').read().split('\n')
    for n, (old, new) in d.items():
        s = L[n - 1]
        if f'"{old}"' not in s:
            print('NAO ACHOU', f, n, old)
            bad += 1
            continue
        L[n - 1] = s.replace(f'"{old}"', f'"{new}"', 1)
    open(f, 'w', encoding='utf-8').write('\n'.join(L))
print('ok' if not bad else f'{bad} falhas')
