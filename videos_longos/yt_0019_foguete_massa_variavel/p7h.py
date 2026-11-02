from ptch6 import patch
patch("sec_t3.py", [
 # §2.2: os insets ficam até as setas dv chegarem ao ∫ (cópias em arco, 1,0 s); depois saem em 0,3 s
 (r'''        resto_ins = VGroup(*[ins[k][i_] for k in (0, 1) for i_ in (0, 1, 2, 4, 5)])
        self.play(*[ins[k][3].animate.move_to(alvo_i).scale(0.35).set_opacity(0.0) for k in (0, 1)], FadeOut(resto_ins), run_time=0.8)
        self.remove(ins)''',
  r'''        cps = [ins[k][3].copy() for k in (0, 1)]
        self.add(*cps)
        self.play(*[cp.animate(path_arc=-1.1).move_to(alvo_i).scale(0.4) for cp in cps], run_time=1.0)
        self.play(*[FadeOut(cp) for cp in cps], FadeOut(ins), FadeIn(C, shift=0.1 * UP), run_time=0.3)
        self.remove(ins, *cps)'''),
 (r'''        self.play(FadeIn(C, shift=0.1 * UP), run_time=0.35)                                  # v6: a linha nova entra sem a sopa do passo (o dv do inset já voou para o ∫)''',
  r'''        self.wait(0.2)                                                                       # v7: C já entrou junto com a chegada das setas dv'''),
])
patch("sec_t4.py", [
 (r'''DXF = 0.36 ''', r'''DXF = 0.7 '''),
 (r'''            m_.next_to(G.pt(tp(), v_(tp())), RIGHT, buff=0.22).shift(dy * DOWN)''', r'''            m_.next_to(G.pt(tp(), v_(tp())), RIGHT, buff=0.42).shift(dy * DOWN)'''),
 (r'''        self.voa([(lp, mp(A, ia, [6, 7]))], extra=[FadeIn(mp(A, ia, [5]))], rt=1.0, origem=False)''',
  r'''        self.voa([(lp, mp(A, ia, [6, 7]))], extra=[FadeIn(mp(A, ia, [5])), FadeOut(lp)], rt=1.0, origem=False, arco_esq=-0.6)          # v7 #21: o original sai enquanto a cópia parte'''),
])
print("ok")
