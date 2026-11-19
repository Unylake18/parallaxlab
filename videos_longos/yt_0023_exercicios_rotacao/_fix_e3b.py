P = 'sec_e3.py'
L = open(P, encoding='utf-8').read().split('\n')
for i, l in enumerate(L):
    if l.strip().startswith('Q4, iq4, _ = self.linha((r"\\alpha", "=", "0", r"\\ \\R'):
        L[i] = ('        Q4, iq4, _ = self.linha((r"\\alpha", "=", "0", r"\\ \\Rightarrow\\ ", r"\\omega", "=", r"\\mathrm{constante}"), size=46, rt=1.1)')
open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
