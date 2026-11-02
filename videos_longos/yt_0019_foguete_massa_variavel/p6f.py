from ptch6 import patch
patch("sec_t2.py", [
 (r'''FT, FB, YC, L_, W_ = 2.35, -1.78, 0.2, 3.2, 0.66''', r'''FT, FB, YC, L_, W_ = 2.35, -1.86, 0.2, 3.2, 0.66'''),
 (r'''Y1, Y2 = -1.24, -1.62''', r'''Y1, Y2 = -1.2, -1.66'''),
 (r'''        b1b = tx("→ NADA NA HORIZONTAL", 26)
        b1b.move_to(P3(-3.55 + b1b.width / 2, -3.45))''',
  r'''        b1b = VGroup(tx("→ NADA NA", 26), tx("HORIZONTAL", 26)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        b1b.move_to(P3(-4.85 - b1b.width / 2, -3.45))                              # v6: à esquerda da queda do grão (a seta v do grão fica livre)'''),
])
