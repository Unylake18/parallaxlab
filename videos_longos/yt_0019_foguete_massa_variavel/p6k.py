from ptch6 import patch
patch("sec_e1.py", [
 (r'''        if rel.get_right()[0] > 0.7:
            rel.shift((0.7 - rel.get_right()[0]) * RIGHT)''',
  r'''        rel.move_to(P3(XR + 1.35 + 0.28 + rel.width / 2, rel.get_center()[1]))          # v6: começa à direita da seta v_ex (a seta não cruza o E)'''),
])
