from ptch6 import patch
patch("sec_t3.py", [
 (r'''.set_fill(WHITE_, 1).set_stroke(WHITE_, 1)''', r'''.set_fill(MAS, 1).set_stroke(MAS, 1)'''),
 (r'''seta_tr(P3(-6.2, -3.05), P3(-6.2, -3.05 - 1.2 * kx.get_value()), VEX_C, 7, tip=0.24)''', r'''seta_tr(P3(-6.2, -3.05), P3(-6.2, -3.05 - 0.6 * kx.get_value()), VEX_C, 7, tip=0.24)'''),
 (r'''lvx = MathTex(r"v_{ex}", font_size=40, color=VEX_C).move_to(P3(-5.35, -3.7))''', r'''lvx = MathTex(r"v_{ex}", font_size=40, color=VEX_C).move_to(P3(-5.4, -3.3))'''),
 (r'''q_.set_opacity(min(1.0, 3.0 * kx.get_value())))''', r'''q_.set_opacity(min(1.0, 8.0 * kx.get_value())))'''),
 (r'''        t1 = rot("10 s", 26, VEL).next_to(g1.pt(10.0, vf), UP, buff=0.2).shift(0.5 * LEFT)
        t2 = rot("10 min", 26, VEL)
        t2.add_updater(lambda m_: m_.move_to(g1.pt(max(TM * k2.get_value(), 40.0), fv(TM)(max(TM * k2.get_value(), 40.0))) + P3(-0.1, 0.5)))''',
  r'''        t1 = txt("QUEIMA DE 10 s", 24, color=VEL).move_to(g1.pt(10.0, vf * 0.55) + P3(1.5, 0))                       # v7 #17: junto da curva rápida, à direita da subida
        t2 = VGroup(txt("QUEIMA DE", 24, color=VEL), txt("10 min", 24, color=VEL)).arrange(DOWN, buff=0.06)

        def pos_t2(m_):
            pt = g1.pt(max(TM * k2.get_value(), 40.0), fv(TM)(max(TM * k2.get_value(), 40.0)))
            m_.move_to(P3(pt[0] + 0.3, max(pt[1] - 0.7, g1.y0 + 0.62)))
        t2.add_updater(pos_t2)'''),
 (r'''r95 = VGroup(txt("95% PROPELENTE", 26), txt("5% O RESTO", 26))''', r'''r95 = VGroup(txt("95% PROPELENTE", 26, color=MAS), txt("5% O RESTO", 26, color="#B9C4D6"))'''),
])
patch("sec_e2.py", [
 (r'''r95 = VGroup(txt("95% PROPELENTE", 26), txt("5% O RESTO", 26))''', r'''r95 = VGroup(txt("95% PROPELENTE", 26, color=MAS), txt("5% O RESTO", 26, color="#B9C4D6"))'''),
])
print("ok")
