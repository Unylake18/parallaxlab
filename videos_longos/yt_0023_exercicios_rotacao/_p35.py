def edit(P, pares):
    s = open(P, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    s = s.replace('\r\n', '\n')
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
edit('prob2.py', [
    ('''        if self._y_topo() - h_ < self.base:
            ficam, saem, herdam = self._sai_blocos(lambda f: self.topo - sum(l.height + self.buff for l, _ in f) - h_ >= self.base, manter)
''', '''        if self._y_topo() - h_ < self.base or len(self.linhas) >= 5:                  # v5 §5: pilha ≤ 5 linhas; os resultados em caixa (até 3) ficam no topo (faixa de resultados)
            pred_ = lambda f: len(f) < 5 and self.topo - sum(l.height + self.buff for l, _ in f) - h_ >= self.base
            caix_ = [l for l, _ in self.linhas if isinstance(l, VGroup) and len(l) and getattr(l[0], "_caixa", False)]
            ficam, saem, herdam = self._sai_blocos(pred_, tuple(manter) + tuple(caix_[-3:]))
            if not pred_(ficam):
                ficam, saem, herdam = self._sai_blocos(pred_, manter)
'''),
    ('''        self.linhas.append((m, dx))
        return m

    def tira(self, *ms):''', '''        self.linhas.append((m, dx))
        print(f"[pilha] {self.cena.clk.get_value():7.1f}s n={len(self.linhas)}", flush=True)
        return m

    def tira(self, *ms):'''),
])
edit('qa23.py', [
    ('''chk("CANETA (termo novo sem fade)",''', '''pl_ = []
for l in LOTES:
    f = U / f"log_{l}.txt"
    if f.exists():
        pl_ += [(l, float(t), int(n)) for t, n in re.findall(r"\[pilha\]\s+([\d.]+)s n=(\d+)", f.read_text(encoding="utf-8", errors="replace"))]
chk("PILHA ≤ 5 linhas", bool(pl_) and max(n for _, _, n in pl_) <= 5, f"máximo {max((n for _, _, n in pl_), default=0)} linhas simultâneas em {len(pl_)} entradas")
chk("CANETA (termo novo sem fade)",'''),
])
print('ok')
