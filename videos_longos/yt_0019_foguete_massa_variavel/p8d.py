from ptch6 import patch
patch("sec_e2.py", [
 (r'''        rotb = VGroup(*[VGroup(MathTex(r"v_{ex}=", font_size=26, color=VEX_C), rot("3,0 km/s", 22, VEX_C)).arrange(RIGHT, buff=0.05).move_to(P3(xc, -1.1)) for xc in XB])''',
  r'''        rotb = VGroup(*[VGroup(MathTex(r"v_{ex}", font_size=34, color=VEX_C), rot("3,0 km/s", 24, VEX_C)).arrange(DOWN, buff=0.06).move_to(P3(xc, -1.25)) for xc in XB])'''),
 (r'''XB = (2.3, 4.2, 6.1)''', r'''XB = (2.25, 4.2, 6.15)'''),
])
print("ok")
