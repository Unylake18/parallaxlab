s = open('kit.py', encoding='utf-8', newline='').read()
a = "        clk = UpdateFromAlphaFunc(self.clk, lambda m, a: m.set_value(t0 + a * n / FPS), rate_func=linear, run_time=rtq)\n"
assert s.count(a) == 1
b = a + "        clk.update_rate_info = lambda *a_, **k_: clk          # v5 ALIASING: um `rate_func=` do play (ease, smooth) valia também para o relógio e deformava o tempo da cena (θ do volante 30°–71°/quadro); o relógio fica sempre linear\n"
open('kit.py', 'w', encoding='utf-8', newline='').write(s.replace(a, b))
