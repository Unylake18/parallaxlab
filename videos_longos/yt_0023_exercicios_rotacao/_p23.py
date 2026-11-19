def edit(P, pares):
    s = open(P, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    s = s.replace('\r\n', '\n')
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
edit('prob2.py', [
    ('''        self._voando = set(id(x) for x in c.get_family()) | set(id(x) for x in dst.get_family()) | set(id(x) for x in tb_.mobject.get_family())
        self._voando_raiz = [c, dst, tb_.mobject]
        self._fontes_extra = [src]''', '''        try:                                                          # v5 §3.1b: auditoria CANETA — termo novo do passo entrou por caneta (ou por fade/linha pronta = reprova)
            def _tipos(a_):
                r_ = []
                for b_ in (getattr(a_, "animations", None) or []):
                    r_ += _tipos(b_) if getattr(b_, "animations", None) else [b_]
                return r_
            ts_ = _tipos(tb_)
            nc_ = sum(1 for x_ in ts_ if isinstance(x_, CanetaAnim))
            nf_ = sum(1 for x_ in ts_ if isinstance(x_, (FadeIn, Write)) and not isinstance(x_, CanetaAnim))
            print(f"[caneta] {getattr(self, '_aid', '?')} passo novos={nc_} fade={nf_}", flush=True)
        except Exception:
            pass
        self._voando = set(id(x) for x in c.get_family()) | set(id(x) for x in dst.get_family()) | set(id(x) for x in tb_.mobject.get_family())
        self._voando_raiz = [c, dst, tb_.mobject]
        self._fontes_extra = [src]'''),
    ('''        print(f"[ordem] {self.clk.get_value():7.1f}s voa n={len(pous_)} falhas={viol_}")''', '''        print(f"[ordem] {self.clk.get_value():7.1f}s voa n={len(pous_)} falhas={viol_}")
        print(f"[caneta] {getattr(self, '_aid', '?')} voa fixos={len(fixos)} voos={len(voos)} fade=0", flush=True)'''),
])
print('ok')
