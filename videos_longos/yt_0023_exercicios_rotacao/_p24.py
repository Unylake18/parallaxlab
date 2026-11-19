def edit(P, pares):
    s = open(P, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    s = s.replace('\r\n', '\n')
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
edit('qa23.py', [
    ('''p("")
p("6. FUNDO: estrelas pelo relógio global''', '''cn_ = Counter()
fade_ = []
for l in LOTES:
    f = U / f"log_{l}.txt"
    if f.exists():
        for m in re.finditer(r"\[caneta\] (\S+) (passo|voa) (?:novos=(\d+)|fixos=(\d+) voos=(\d+)) fade=(\d+)", f.read_text(encoding="utf-8", errors="replace")):
            a, tipo, nv, fx, vo, fd = m.groups()
            cn_[tipo + "_caneta"] += int(nv or fx or 0)
            cn_[tipo + "_eventos"] += 1
            if int(fd):
                fade_.append(f"{a} {tipo} fade={fd}")
p(f"  CANETA: passo {cn_['passo_eventos']} eventos · {cn_['passo_caneta']} termos novos escritos pela caneta; voa {cn_['voa_eventos']} eventos · {cn_['voa_caneta']} termos fixos escritos pela caneta; termos novos por fade/linha pronta: {len(fade_)}")
chk("CANETA (termo novo sem fade)", not fade_ and (cn_["passo_eventos"] + cn_["voa_eventos"]) > 0, "; ".join(fade_[:10]) if fade_ else "nenhum termo novo entrou por FadeIn/linha pronta")
p("")
p("6. FUNDO: estrelas pelo relógio global'''),
])
print('ok')
