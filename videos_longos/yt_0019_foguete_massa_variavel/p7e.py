from ptch6 import patch
patch("sec_t3.py", [
 (r'''            m_[1].next_to(q_ + P3(0, -0.32), DOWN, buff=0.1)''', r'''            m_[1].next_to(q_ + P3(0, 0.32), UP, buff=0.1)                                # v7 #19: acima do rastro, longe do inset'''),
])
patch("sec_t4.py", [
 # painel acompanha o conteúdo (conteúdo + 0,3 u)
 (r'''painel = RoundedRectangle(corner_radius=0.14, width=6.8, height=5.9).move_to(P3(4.1, -0.45)).set_fill("#0E2A52", 0.85).set_stroke(GEO, 1.2, opacity=0.4)''',
  r'''painel = RoundedRectangle(corner_radius=0.14, width=6.8, height=1.6).move_to(P3(4.1, 2.5 - 0.8)).set_fill("#0E2A52", 0.85).set_stroke(GEO, 1.2, opacity=0.4)

        def ajusta():
            h_ = 2.5 - (self.pilha.ultima().get_bottom()[1] - 0.3)
            return painel.animate.stretch_to_fit_height(h_).move_to(P3(4.1, 2.5 - h_ / 2))'''),
 (r'''        B[1][0][0:3].set_color(VEX_C)''', r'''        B[1][0][0:3].set_color(VEX_C)
        B[1][0][0:3].set_stroke(VEX_C, width=1.8, background=False)                  # v7 #25: v_ex legível sobre o painel'''),
 (r'''        self.play(FadeIn(B, shift=0.1 * UP), run_time=0.8)''', r'''        self.play(FadeIn(B, shift=0.1 * UP), ajusta(), run_time=0.8)'''),
 (r'''        self.play(FadeIn(C), ch.animate.set_value(0.7), run_time=0.7)''', r'''        self.play(FadeIn(C), ch.animate.set_value(0.7), ajusta(), run_time=0.7)'''),
 # rótulos de vazão: no fim da curva, ≥ 10 px do eixo
 (r'''        r1.add_updater(lambda m_: m_.next_to(G.pt(tp1(), v_sub(tp1(), 240.0)), RIGHT, buff=0.22).shift(0.28 * DOWN))        # na ponta de cada curva, acompanhando o desenho
        r2.add_updater(lambda m_: m_.next_to(G.pt(tp2(), v_sub(tp2(), 120.0)), RIGHT, buff=0.22).shift(0.62 * DOWN))
        r1.next_to(G.pt(0, 0), RIGHT, buff=0.3).shift(0.28 * DOWN)
        r2.next_to(G.pt(0, 0), RIGHT, buff=0.3).shift(0.62 * DOWN)''',
  r'''        def pos_r(m_, tp, v_, dy, ymin):                                                    # v7 #23: na ponta da curva, nunca a menos de 0,3 u do eixo t
            m_.next_to(G.pt(tp(), v_(tp())), RIGHT, buff=0.22).shift(dy * DOWN)
            if m_.get_center()[1] < G.y0 + ymin:
                m_.shift((G.y0 + ymin - m_.get_center()[1]) * UP)
        r1.add_updater(lambda m_: pos_r(m_, tp1, lambda t_: v_sub(t_, 240.0), 0.28, 0.75))
        r2.add_updater(lambda m_: pos_r(m_, tp2, lambda t_: v_sub(t_, 120.0), 0.0, 0.36))
        pos_r(r1, tp1, lambda t_: v_sub(t_, 240.0), 0.28, 0.75)
        pos_r(r2, tp2, lambda t_: v_sub(t_, 120.0), 0.0, 0.36)'''),
])
