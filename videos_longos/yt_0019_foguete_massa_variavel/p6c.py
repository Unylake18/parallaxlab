from ptch6 import patch
patch("sec_e1.py", [
 ("        if rel.get_right()[0] > 0.1:\n            rel.shift((0.1 - rel.get_right()[0]) * RIGHT)",
  "        if rel.get_right()[0] > 0.5:\n            rel.shift((0.5 - rel.get_right()[0]) * RIGHT)"),
 ('lF = VGroup(txt("FORÇA DO", 24, color=FC), txt("ASSENTO", 24, color=FC)).arrange(DOWN, buff=0.06).move_to(P3(PXc - PW / 2 + 0.2 + 0.7, y_s + 1.3))',
  'lF = VGroup(txt("FORÇA DO", 24, color=FC), txt("ASSENTO", 24, color=FC)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)\n        lF.move_to(P3(PXc - PW / 2 + 0.2, y_s + 0.75), aligned_edge=LEFT)'),
])
