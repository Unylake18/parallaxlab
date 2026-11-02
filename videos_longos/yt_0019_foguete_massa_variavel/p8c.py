from ptch6 import patch
patch("sec_t2.py", [
 (r'''FadeIn(mp(A, ia, [3, 5, 6, 8])), FadeOut(lm2), FadeOut(nota)], rt=1.0''', r'''FadeIn(mp(A, ia, [3, 5, 6, 8])), FadeOut(lm2, run_time=0.12), FadeOut(nota, run_time=0.12)], rt=1.0'''),
 (r'''        b1b = tx("NADA NA HORIZONTAL", 22)''', r'''        b1b = tx("NADA NA HORIZONTAL", 20)'''),
])
patch("sec_e2.py", [
 (r'''RoundedRectangle(corner_radius=0.08, width=1.85, height=0.5).set_fill(VREL, 0.85).set_stroke(VREL, 1.5).move_to(P3(xc, -0.5))''', r'''RoundedRectangle(corner_radius=0.08, width=1.8, height=0.6).set_fill(VREL, 0.85).set_stroke(VREL, 1.5).move_to(P3(xc, -0.5))'''),
 (r'''VGroup(MathTex(r"v_{ex}=", font_size=30, color=VEX_C), rot("3,0 km/s", 24, VEX_C)).arrange(RIGHT, buff=0.06).move_to(P3(xc, -1.05))''', r'''VGroup(MathTex(r"v_{ex}=", font_size=26, color=VEX_C), rot("3,0 km/s", 22, VEX_C)).arrange(RIGHT, buff=0.05).move_to(P3(xc, -1.1))'''),
])
print("ok")
