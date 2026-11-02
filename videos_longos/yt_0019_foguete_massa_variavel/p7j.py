from ptch6 import patch
from pathlib import Path
U = Path(__file__).resolve().parent
# 3D: tanque âmbar mais quente (o fundo ciano deixava o tom oliva)
s = (U / "threejs/cena3d/f19.js").read_text(encoding="utf-8")
s = s.replace("color: 0xC77A2B", "color: 0xE8801C", 1).replace("emissive: new T3.Color(0xFFA94D)", "emissive: new T3.Color(0xFF8A2B)", 1)
(U / "threejs/cena3d/f19.js").write_text(s, encoding="utf-8", newline="\n")
patch("sec_t3.py", [
 (r'''            m_.move_to(P3(pt[0] + 0.3, max(pt[1] - 0.7, g1.y0 + 0.62)))''', r'''            m_.move_to(P3(pt[0] + 0.5, max(pt[1] - 1.1, g1.y0 + 0.62)))'''),
 (r'''            m_[1].next_to(q_ + P3(0, 0.32), UP, buff=0.1)                                # v7 #19: acima do rastro, longe do inset''',
  r'''            m_[1].next_to(q_ + P3(0, 0.32), UP, buff=0.1).shift(0.55 * LEFT)              # v7 #19: acima do rastro, longe do inset e do F_emp'''),
])
patch("sec_e1.py", [(r'''rel = txt("EM RELAÇÃO AO FOGUETE", 22)''', r'''rel = txt("EM RELAÇÃO AO FOGUETE", 24)''')])
patch("sec_e3.py", [
 (r'''F2, if2 = M("=", r"\tfrac12\cdot 20\cdot 1{,}5^2", "=", r"22{,}5\ \mathrm{W}", size=46, cores={3: KC})
        F2.scale_to_fit_width(min(F2.width, 5.0))                                           # v7 #42: x <= 912 px''',
  r'''F2, if2 = M("{}=", r"\tfrac12\cdot 20\cdot 1{,}5^2", "=", r"22{,}5\ \mathrm{W}", size=46, cores={3: KC})
        F2.scale_to_fit_width(min(F2.width, 5.05))                                          # v7 #42: x <= 912 px (linha alinhada à esquerda, não mais sob o "=" da mãe)'''),
])
print("ok")
