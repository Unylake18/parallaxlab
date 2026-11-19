"""Âncoras de palavra (dentro das células) para B05/B06. Move algumas âncoras de célula e insere self.at(n, k=palavra)."""
import re
import sys

MOVE = {85, 88, 89, 90, 91}                    # âncoras de célula (k=0) que mudam de lugar
AX = [
    (82, 11, '        self.setcap(txt("carga contida no trecho", T_NOTE, opacity=0.95).move_to([0, -0.6, 0]))'),
    (83, 11, '        self.morph(["dq", "=", "lam", "dl"], SZ, AT, run=1.3)'),
    (84, 12, '        self.setcap(VGroup(eq("I", size=32, colors={0: GREEN}), txt("carga / tempo"'),
    (85, 0, '        self.setcap(txt("em dt, cada portador percorre v dt", T_NOTE, opacity=0.95).move_to([0, -0.6, 0]))'),
    (85, 28, '        self.morph(["I", "=", ("f", ["lam", "vs", "dt@n"]'),
    (88, 0, '        self.morph(["dF", "=", "lam", "dl", "vv@a", "times", "Bv"], SZ, AT, alias={"dq": ["lam", "dl"]}, run=1.2)'),
    (88, 13, '        note2 = txt("v e dℓ: mesmo sentido", T_NOTE, opacity=0.9)'),
    (88, 21, '        note3 = eq(r"\\lambda", r"\\,v", "=", "I", size=40'),
    (88, 24, '        self.morph(["dF", "=", "I", "dlv", "times", "Bv"], SZ, AT, alias={"lam": ["I"]}, run=1.4)'),
    (89, 0, '        self.morph(["F", "=", "int", "I", "dlv", "times", "Bv"], SZ, AT, run=1.4)'),
    (90, 0, '        n4 = txt("dℓ segue a corrente convencional"'),
    (91, 0, '        self.play(self.pw.animate.set_value(2.6), RT(c0, c1), run_time=2.0, rate_func=smooth)'),
    (91, 8, '        lab_dw = eq("dw", size=M_M, colors={0: GREEN})'),
    (91, 26, '        _la = eq(r"dA_{\\mathrm{sup}}", size=M_M)'),
    (91, 38, '        c3b = panel(txt("espécie com velocidade v", 20, opacity=0.9), eq(r"\\mathbf K"'),
    (95, 30, '        c6b = panel(txt("espécie com velocidade v", 20, opacity=0.9), eq(r"\\mathbf J"'),
    (99, 14, '        e = eq(r"I", "=", r"\\int_S", r"\\mathbf J", r"\\cdot", r"d\\mathbf a", size=48'),
    (100, 9, '        self.add(l_v)\n'),
    (100, 13, '        self.add(l_dv)\n        self.play(Indicate(self.vol'),
    (100, 20, '        self.add(l_q)\n'),
    (100, 28, '        self.add(l_ji, l_jo)\n'),
    (101, 5, '        root_, new_ = self.build(["dQdt", "=", "Ient", "minus", "Isai"], SZs)'),
    (101, 18, '        self.play(FadeIn(rp), FadeIn(self.reads), FadeIn(slow), run_time=0.8)'),
    (102, 8, '        self.play(self.Iout.animate.set_value(2.0), FadeIn(cap), run_time=1.5)'),
    (102, 12, '        self.play(self.Iin.animate.set_value(2.0), FadeIn(cap2), run_time=1.5)'),
    (103, 1, '        self.add(nL, nR, nl, nr)'),
    (103, 5, '        self.add(sL)\n'),
    (103, 12, '        self.add(sR)\n'),
    (103, 15, '        capf = txt("fluxo líquido para fora:"'),
    (103, 18, '        self.morph(["oint", "Jv", "dot", "da", "=", "Isai", "minus", "Ient"], SZs, ST, run=1.4)'),
    (107, 24, '        self.play(FadeOut(hi_l), FadeOut(hi_r), FadeIn(cells), FadeIn(dvl), run_time=1.2)'),
    (110, 17, '        nm_c = nome("Equação da continuidade"'),
    (111, 19, '        self.morph(["drho", "=", "0"], 52, AT, run=1.2)'),
    (111, 22, '        self.morph(["div", "=", "0"], 58, AT, alias={"drho": ["div"]}, run=1.4)'),
    (112, 11, '        self.play(FadeIn(p2), FadeIn(e2, shift=0.1 * DOWN), run_time=1.0)'),
    (112, 24, '        msg = txt("corrente estacionária: não é nula"'),
]
f = sys.argv[1]
s = open(f, encoding="utf-8").read()
falhas = []
for n in MOVE:
    padrao = "        self.at(%d)\n" % n
    if s.count(padrao) != 1:
        falhas.append("remover at(%d): %d" % (n, s.count(padrao)))
    else:
        s = s.replace(padrao, "")
for n, k, anc in AX:
    if s.count(anc) != 1:
        falhas.append("âncora %d.%d: %d ocorrências: %s" % (n, k, s.count(anc), anc[:70]))
        continue
    j = s.index(anc)
    ls = s.rfind("\n", 0, j) + 1
    s = s[:ls] + "        self.at(%d%s)\n" % (n, ", k=%d" % k if k else "") + s[ls:]
open(f, "w", encoding="utf-8").write(s)
print("falhas:", len(falhas))
for x in falhas:
    print(" -", x)
