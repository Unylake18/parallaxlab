from ptch6 import patch
patch("sec_t3.py", [
 (r'''        for i_ in range(4):                                                            # v9: a curva lenta cresce em 4 passos, cada um com o rótulo pulsando (tela nunca parada)
            self.play(k2.animate(rate_func=linear).set_value((i_ + 1) / 4), Indicate(t2, color=VEL, scale_factor=1.12), run_time=1.0)''',
  r'''        self.play(k2.animate(rate_func=linear).set_value(1.0), run_time=4.0)'''),
])
patch("sec_e2.py", [
 (r'''        self.play(tt.animate(rate_func=linear).set_value(v_a + (T_OFF - v_a) / 2), Indicate(n1, color=WHITE_, scale_factor=1.12), run_time=t_a / 2)     # v9: a queima do 1º estágio tem o rótulo pulsando
        self.play(tt.animate(rate_func=linear).set_value(T_OFF), Indicate(l1, color=WHITE_, scale_factor=1.08), run_time=t_a / 2)''',
  r'''        self.play(tt.animate(rate_func=linear).set_value(T_OFF), run_time=t_a)'''),
])
