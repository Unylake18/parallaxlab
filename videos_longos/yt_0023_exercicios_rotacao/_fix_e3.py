P = 'sec_e3.py'
L = open(P, encoding='utf-8').read().split('\n')
for i, l in enumerate(L):
    if l.strip().startswith('l_a = lbl(') and 'ESTE' in l:
        L[i] = '        l_a = lbl(r"\\mathrm{ESTE\\ FIO}\\to 6{,}0\\ \\mathrm{kg}", MAS, 34)'
    if l.strip().startswith('l_b = lbl(') and 'ESTE' in l:
        L[i] = '        l_b = lbl(r"\\mathrm{ESTE\\ FIO}\\to 10{,}0\\ \\mathrm{kg}", MAS, 34)'
open(P, 'w', encoding='utf-8').write('\n'.join(L))
print([l for l in L if 'ESTE' in l])
