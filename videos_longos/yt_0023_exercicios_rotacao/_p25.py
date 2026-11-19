def edit(P, pares):
    s = open(P, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    s = s.replace('\r\n', '\n')
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
edit('prob2.py', [
    ('''print(f"[caneta] {getattr(self, '_aid', '?')} passo novos={nc_} fade={nf_}", flush=True)''', '''print(f"[caneta] {getattr(self, '_aid', '?')} passo novos={nc_} fade={nf_} t={self.clk.get_value():.2f}", flush=True)'''),
    ('''print(f"[caneta] {getattr(self, '_aid', '?')} voa fixos={len(fixos)} voos={len(voos)} fade=0", flush=True)''', '''print(f"[caneta] {getattr(self, '_aid', '?')} voa fixos={len(fixos)} voos={len(voos)} fade=0 t={self.clk.get_value():.2f}", flush=True)'''),
])
edit('qa23.py', [
    ('''fade=(\d+)", f.read_text''', '''fade=(\d+)(?: t=[\d.]+)?", f.read_text'''),
])
print('ok')
