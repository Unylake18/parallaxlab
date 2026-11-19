s = open('prob2.py', encoding='utf-8', newline='').read()
a = '''            print(f"[caneta] {getattr(self, '_aid', '?')} passo novos={nc_} fade={nf_} t={self.clk.get_value():.2f}", flush=True)'''
b = a + '''
            if nf_:
                print("[caneta-dbg]", [(type(x_).__name__, getattr(getattr(x_, "mobject", None), "tex_string", None) or type(getattr(x_, "mobject", None)).__name__) for x_ in ts_ if isinstance(x_, (FadeIn, Write)) and not isinstance(x_, CanetaAnim)], flush=True)'''
assert s.count(a) == 1
open('prob2.py', 'w', encoding='utf-8', newline='').write(s.replace(a, b))
