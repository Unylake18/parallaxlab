s = open('qa23.py', encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
s = s.replace('\r\n', '\n')
a = '''    por_classe = Counter()
    linhas_ev = []
    for (classe, desc), ints in sorted(ev.items(), key=lambda kv: kv[1][0][0]):
        motivo = next((mot for pat, mot in INTENCIONAL if re.search(pat, desc)), None)
        for a, b in ints:
            tipo = "INTENCIONAL" if motivo else "REAL"
'''
b = '''    por_classe = Counter()
    linhas_ev = []
    flog = U / f"log_{l}.txt"
    jan_ = [float(t_) for t_ in re.findall(r"\[ordem\]\s+([\d.]+)s (?:voa|passo)", flog.read_text(encoding="utf-8", errors="replace"))] if flog.exists() else []
    for (classe, desc), ints in sorted(ev.items(), key=lambda kv: kv[1][0][0]):
        motivo = next((mot for pat, mot in INTENCIONAL if re.search(pat, desc)), None)
        for a, b in ints:
            mv_ = None
            if not motivo and classe.startswith(("TEXTO SOBRE OBJETO", "SOBREPOSICAO")) and "VMobjectFromSVGP" in desc and any(t0_ - 0.3 <= a <= t0_ + 3.2 for t0_ in jan_):
                mv_ = "voo/passo de glifos (TransformFromCopy ou glyph map): o termo em trânsito sai do rótulo/linha de origem, sobrepõe a origem durante o voo e pousa na vaga; o TRÂNSITO (cruzamento prolongado) continua contado à parte"
            tipo = "INTENCIONAL" if (motivo or mv_) else "REAL"
            if mv_ and not motivo:
                linhas_ev.append(f"      {a:6.1f}–{b:6.1f} s  {tipo:11s} {desc}  ({mv_[:60]}…)")
                continue
'''
assert s.count(a) == 1
s = s.replace(a, b)
open('qa23.py', 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
