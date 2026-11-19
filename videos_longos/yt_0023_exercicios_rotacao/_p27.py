s = open('prob2.py', encoding='utf-8', newline='').read()
i = s.index('\n\nimport os as _os_dbg')
s = s[:i] + '\n'
a = '            ts_ = _tipos(tb_)\n'
b = '            ts_ = list(getattr(tb_, "animations", []))           # só os filhos diretos: o FadeIn interno do Morph4 (troca de glifos mapeados) não é termo novo\n'
assert s.count(a) == 1
s = s.replace(a, b)
open('prob2.py', 'w', encoding='utf-8', newline='').write(s)
