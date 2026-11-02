from ptch6 import patch
patch("sec_e1.py", [
 (r'''rel = txt("EM RELAÇÃO AO FOGUETE", 24).next_to(l_vx, DOWN, buff=0.14).align_to(l_vx, LEFT)
        if rel.get_right()[0] > 0.5:
            rel.shift((0.5 - rel.get_right()[0]) * RIGHT)''',
  r'''rel = txt("EM RELAÇÃO AO FOGUETE", 22).next_to(l_vx, DOWN, buff=0.14).align_to(l_vx, LEFT)
        if rel.get_right()[0] > 0.7:
            rel.shift((0.7 - rel.get_right()[0]) * RIGHT)'''),
])
patch("sec_t3.py", [
 (r'''        self.passo(B, C, (J(ib, 0), J(ic, 0)[-2:]), (J(ib, 1), J(ic, 1)), (J(ib, 2), J(ic, 2)), (J(ib, 3), J(ic, 3)), (J(ib, 4), J(ic, 4)[-4:]), rt=1.4, origem=False)''',
  r'''        self.play(FadeIn(C, shift=0.1 * UP), run_time=0.35)                                  # v6: a linha nova entra sem a sopa do passo (o dv do inset já voou para o ∫)'''),
])
patch("conferencia.py", [(r'''(v4 ← → v5)''', r'''(v5 ← → v6)''')])
