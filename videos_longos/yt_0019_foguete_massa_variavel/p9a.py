from ptch6 import patch
patch("sec_fim.py", [
 (r'''.arrange(DOWN, buff=0.08).move_to(P3(3.4, 3.65))''', r'''.arrange(DOWN, buff=0.08).move_to(P3(2.7, 3.65))'''),     # v9 §1.1: ≥ 30 px do logo
])
patch("sec_t2.py", [
 (r'''se = arrow(P3(BX, YC + 0.82), P3(BX + 0.7, YC + 0.82), FC, 7, tip=0.22)''', r'''se = arrow(P3(BX, YC + 0.62), P3(BX + 0.7, YC + 0.62), FC, 7, tip=0.22)'''),   # v9 §1.2: folga ≥ 8 px do tracejado (topo em YC + 0,95)
])
patch("sec_e3.py", [
 (r'''sv = arrow(P3(-6.7, YT - 1.15), P3(-6.7 + VB, YT - 1.15), VEL, 7, tip=0.22)''', r'''sv = arrow(P3(-6.7, YT - 0.95), P3(-6.7 + VB, YT - 0.95), VEL, 7, tip=0.22)'''),   # v9 §1.3: rótulo v = 1,5 m/s 12 px mais alto
 (r'''G2 = txt("NÃO DEPENDE DO ATRITO", 28, bold=True)''', r'''G2 = VGroup(txt("NÃO DEPENDE DO", 28, bold=True), txt("COEFICIENTE DE ATRITO", 28, bold=True)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)'''),
])
patch("sec_t4.py", [
 (r'''C = VGroup(txt("SENÃO, ESPERA NA RAMPA", 26), txt("ATÉ A MASSA CAIR", 26))''', r'''C = VGroup(txt("SENÃO, ESPERA ATÉ A MASSA CAIR", 26), txt("· SE O PROPELENTE DURAR", 26))'''),
])
print("ok")
