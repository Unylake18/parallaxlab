"""python splice.py CENA INICIO FIM NOVO.py : troca o trecho [INICIO, FIM) de CENA pelo conteúdo de NOVO (texto exato, sem escapes)."""
import sys
c, a, b, n = sys.argv[1:5]
s = open(c, encoding="utf-8").read(); new = open(n, encoding="utf-8").read()
i = s.index(a); j = s.index(b, i)
open(c, "w", encoding="utf-8").write(s[:i] + new + s[j:])
print("ok", j - i, "->", len(new))
