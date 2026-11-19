L = open('_p_e1a.py', encoding='utf-8').read().split('\n')
i = next(k for k, l in enumerate(L) if l.startswith('def rw('))
j = next(k for k, l in enumerate(L) if l.startswith('def rep('))
novo = [
    "def rw(P, fn):",
    "    s = open(P, encoding='utf-8').read()          # newline=None: CRLF vira \\n; a escrita devolve o padrão do sistema",
    "    s2 = fn(s)",
    "    open(P, 'w', encoding='utf-8').write(s2)",
    "",
    "",
]
L[i:j] = novo
open('_p_e1a.py', 'w', encoding='utf-8').write('\n'.join(L))
