from pathlib import Path
U = Path(__file__).resolve().parent
def patch(f, pares):
    p = U / f
    s = p.read_text(encoding="utf-8")
    for a, b in pares:
        assert a in s, (f, a[:70])
        s = s.replace(a, b, 1)
    p.write_text(s, encoding="utf-8", newline="\n")
