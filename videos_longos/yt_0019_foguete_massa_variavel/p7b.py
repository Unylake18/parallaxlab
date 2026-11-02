from ptch6 import patch
from pathlib import Path
p = Path(__file__).resolve().parent / "sec_t2.py"
s = p.read_text(encoding="utf-8")
i = s.index("        self.play(t3.animate.set_opacity(0), mp(S1, is1, [3])")
j = s.index("        self.pilha.poe(C)\n        self.play(Indicate(mp(S2, is2, [4])")
novo = r'''        S2, is2 = M("0", "=", r"m\,dv", "+", r"v_{ex}\,dm", size=40)
        pinta(S2, is2, 2, [(1, VEL), (2, VEL)])
        pinta(S2, is2, 4, [(0, VEX_C), (1, VEX_C), (2, VEX_C)])
        C, ic = M(r"m\,dv", "=", "-", r"v_{ex}", r"\,dm", size=48, cores={3: VEX_C})
        pinta(C, ic, 0, [(1, VEL), (2, VEL)])
        self.gat("e fica isso")
        fecha(S1, is1, S2, is2, [(0, 0), (1, 1), (2, 2), (5, 3), (6, 4)], [3, 4], extra=[FadeOut(br), FadeOut(n2)])      # v7: o termo de 2ª ordem sai e a linha fecha no mesmo play
        self.wait(0.8)
'''
s = s[:i] + novo + s[j:]
s = s.replace("def fecha(src_, isrc, dst, idst, pares, sai, novo=()):", "def fecha(src_, isrc, dst, idst, pares, sai, novo=(), extra=()):", 1)
s = s.replace("*[FadeIn(mp(dst, idst, [k])) for k in novo], run_time=0.5)", "*[FadeIn(mp(dst, idst, [k])) for k in novo], *extra, run_time=0.5)", 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
