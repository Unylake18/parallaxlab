s = open('kit.py', encoding='utf-8', newline='').read()
a = "        clk.update_rate_info = lambda *a_, **k_: clk          # v5 ALIASING: um `rate_func=` do play (ease, smooth) valia também para o relógio e deformava o tempo da cena (θ do volante 30°–71°/quadro); o relógio fica sempre linear\n"
assert s.count(a) == 1
s = s.replace(a, '')
b = "        clk = UpdateFromAlphaFunc(self.clk, lambda m, a: m.set_value(t0 + a * n / FPS), rate_func=linear, run_time=rtq)\n"
assert s.count(b) == 1
s = s.replace(b, "        clk = _RelogioLinear(self.clk, lambda m, a: m.set_value(t0 + a * n / FPS), rate_func=linear, run_time=rtq)\n")
c = "class OpVivo(Animation):"
assert s.count(c) == 1
s = s.replace(c, '''class _RelogioLinear(UpdateFromAlphaFunc):
    """v5 ALIASING: `Scene.play(..., rate_func=)` faz setattr(rate_func) em TODA animação, inclusive no relógio da cena, e o tempo passava a seguir o ease/smooth
    (θ do volante a 30°–71° por quadro no E1-15). O relógio ignora o rate_func do play e fica sempre linear."""
    @property
    def rate_func(self):
        return linear

    @rate_func.setter
    def rate_func(self, v):
        pass


class OpVivo(Animation):''')
open('kit.py', 'w', encoding='utf-8', newline='').write(s)
