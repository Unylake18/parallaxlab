import re
from pathlib import Path

U = Path(__file__).resolve().parent


def sub(arq, a, b, n=1, obrig=True):
    p = U / arq
    s = p.read_text(encoding="utf-8")
    if a not in s:
        print("NÃO ACHEI em", arq, ":", a[:70])
        return
    p.write_text(s.replace(a, b, n), encoding="utf-8")


# 1) varredura também em plays fixo (monta escreve a álgebra com fixo=True)
sub("prob2.py", r'''        rt0 = (kw.get("run_time") or max([getattr(x, "run_time", 1.0) for x in a] or [1.0])) * self.ritmo
        if rt0 > 2.4 and not kw.get("fixo", False) and SYNC''', r'''        rt0 = (kw.get("run_time") or max([getattr(x, "run_time", 1.0) for x in a] or [1.0])) * (1.0 if kw.get("fixo", False) else self.ritmo)
        if rt0 > 2.4 and SYNC''')

# 2) hook
sub("sec_hook.py", "move_to(P3(0.2, 2.15))", "move_to(P3(-1.7, 1.5))")
sub("sec_hook.py", r'''T("g", 46, ACC), txt("?", 36, bold=True, color=ACC)], 0.14)''', r'''T("g", 46, ACC), txt("?", 36, bold=True, color=ACC)], 0.24)''')
sub("sec_hook.py", "ch_dob = Line(p_dob + 0.30 * UR, lbl_dob.get_bottom() + 0.08 * DOWN + 0.55 * LEFT)", "ch_dob = Line(p_dob + 0.30 * UR, lbl_dob.get_bottom() + 0.25 * DOWN + 0.55 * LEFT)")
sub("sec_hook.py", "Line(lbl_m2.get_bottom() + 0.06 * DOWN,", "Line(lbl_m2.get_bottom() + 0.24 * DOWN,")
sub("sec_hook.py", "Line(lbl_m1.get_bottom() + 0.06 * DOWN,", "Line(lbl_m1.get_bottom() + 0.24 * DOWN,")
sub("sec_hook.py", "move_to(p_m1_15 + P3(-0.3, 1.15))", "move_to(p_m1_15 + P3(-0.3, 1.7))")
sub("sec_hook.py", r'''[["QUEDA DE", nm("0", GEO, 30), "A", nm(r"0{,}15\ \mathrm{s}", GEO, 30)]]''', r'''[["QUEDA DE", nm("0", GEO, 36), "A", nm(r"0{,}15\ \mathrm{s}", GEO, 36)]]''')
sub("sec_hook.py", r'''tit_lupa = linha_base([txt("ZOOM ×3 ·", 28, color=GEO), T("t", 34, GEO), nm(r"=\ 0{,}15\ \mathrm{s}", GEO, 34)], 0.1).scale_to_fit_width(3.3).next_to(lupa, UP, buff=0.14)''',
    r'''tit_lupa = VGroup(txt("ZOOM ×3", 30, color=GEO), linha_base([T("t", 46, GEO), nm(r"=\ 0{,}15\ \mathrm{s}", GEO, 46)], 0.1)).arrange(DOWN, buff=0.08).next_to(lupa, UP, buff=0.14)''')

# 3) fim
sub("sec_fim.py", "CL = P3(0, 3.15)", "CL = P3(0, 2.95)")
sub("sec_fim.py", "Circle(radius=0.85 + 0.45 * ph)", "Circle(radius=0.75 + 0.30 * ph)")
sub("sec_fim.py", "yi = -0.1", "yi = 0.1")
for a, b in (("-1.6))", "-1.5))"),):
    pass
sub("sec_fim.py", "move_to(P3(0, -2.35))", "move_to(P3(0, -2.1))")
sub("sec_fim.py", "move_to(P3(0, -3.5))", "move_to(P3(0, -3.2))")
sub("sec_fim.py", "Line(lbl_bloco.get_top() + 0.08 * UP + 0.5 * LEFT,", "Line(lbl_bloco.get_top() + 0.22 * UP + 0.5 * LEFT,")
sub("sec_fim.py", r'''T("g", 46, ACC), txt("?", 36, bold=True, color=ACC)], 0.08)''', r'''T("g", 46, ACC), txt("?", 36, bold=True, color=ACC)], 0.24)''')
sub("sec_fim.py", ".next_to(laser, UP, buff=0.12)", ".next_to(laser, UP, buff=0.35)")
sub("sec_fim.py", "            w=6.6,\n        ).move_to(P3(-4.2, -3.05))", "            w=6.0,\n        ).move_to(P3(-3.8, -3.05))")

# 5) T5
sub("sec_t5.py", "C_ENG = P3(-4.9, 0.25)", "C_ENG = P3(-4.9, -0.2)")
sub("sec_t5.py", "r1=0.80, razao=3, n1=8", "r1=0.72, razao=3, n1=8", n=2)
sub("sec_t5.py", "barra_E(1.9, -3.3, 2.0, larg=0.6, cor=KC, hmax=2.2)", "barra_E(1.9, -3.0, 1.8, larg=0.6, cor=KC, hmax=2.0)")
sub("sec_t5.py", "barra_E(3.5, -3.3, 2.0, larg=0.6, cor=KC, hmax=2.2)", "barra_E(3.5, -3.0, 1.8, larg=0.6, cor=KC, hmax=2.0)")
sub("sec_t5.py", "P3(1.9, -3.95)", "P3(1.9, -3.5)")
sub("sec_t5.py", "P3(3.5, -3.95)", "P3(3.5, -3.5)")
sub("sec_t5.py", r'''T(r"\theta_i", 32, GEO)''', r'''T(r"\theta_i", 38, GEO)''')
sub("sec_t5.py", r'''T(r"\theta_f", 32, GEO)''', r'''T(r"\theta_f", 38, GEO)''')

# 6) T6
sub("sec_t6.py", "P_PIV = P3(-3.9, -1.0)\n        gan = gangorra(P_PIV, escala=1.2, ang=0.0)", "P_PIV = P3(-3.7, -1.0)\n        gan = gangorra(P_PIV, escala=1.0, ang=0.0)")
sub("sec_t6.py", r'''T(r"\tfrac{1}{4}Mg", 34, FC)''', r'''T(r"\tfrac{1}{4}Mg", 40, FC)''')
sub("sec_t6.py", r'''T(r"a_{\mathrm{cm}} = \tfrac{3}{4}g", 32, ACC)''', r'''T(r"a_{\mathrm{cm}} = \tfrac{3}{4}g", 38, ACC)''')

# 4) T4
sub("sec_t4.py", "P_DOB = P3(-6.9, 0.35)", "P_DOB = P3(-6.3, 0.35)")
sub("sec_t4.py", "L_ESQ = 6.0", "L_ESQ = 5.7")
sub("sec_t4.py", 'txt("DOBRADIÇA:", 22, bold=True, color=FC)', 'txt("DOBRADIÇA:", 30, bold=True, color=FC)')

# 1) T1
sub("sec_t1.py", 'lbl_dob = txt("DOBRADIÇA", 30, color=GEO).move_to(p_dob + P3(0.0, -0.95))', 'lbl_dob = txt("DOBRADIÇA", 30, color=GEO).move_to(p_dob + P3(0.0, -1.3))')
sub("sec_t1.py", 'lbl_mac = txt("MAÇANETA", 30, color=GEO).move_to(p_mac + P3(0.0, -0.95))', 'lbl_mac = txt("MAÇANETA", 30, color=GEO).move_to(p_mac + P3(0.0, -1.3))')
sub("sec_t1.py", "move_to(p_mac + P3(-0.48, -0.48))", "move_to(p_mac + P3(-0.8, -0.8))")
sub("sec_t1.py", "move_to(P_ap1 + P3(0.76, 0.24))", "move_to(P_ap1 + P3(1.0, 0.10))")
sub("sec_t1.py", "move_to((p_dob + p_mac) / 2 + P3(0.2, -1.05))", "move_to((p_dob + p_mac) / 2 + P3(0.2, 1.45))")
sub("sec_t1.py", "c_pos, c_neg = P3(-4.8, 0.85), P3(-2.0, 0.85)", "c_pos, c_neg = P3(-5.3, 0.85), P3(-1.5, 0.85)")
sub("sec_t1.py", 'txt("ANTI-HORÁRIO", 22, color=GEO)', 'txt("ANTI-HORÁRIO", 34, color=GEO)')
sub("sec_t1.py", 'txt("HORÁRIO", 22, color=GEO)', 'txt("HORÁRIO", 34, color=GEO)')
sub("sec_t1.py", r'''T(r"F_\parallel", 32, GEO)''', r'''T(r"F_\parallel", 38, GEO)''')
sub("sec_t1.py", r'''T(r"F_\perp = F\sin\varphi", 34, FC)''', r'''T(r"F_\perp = F\sin\varphi", 40, FC)''')

# 2) T2
sub("sec_t2.py", "lbl_O = T(\"O\", 40, TQ).next_to(dot_O, UP, buff=0.28)", "lbl_O = T(\"O\", 40, TQ).next_to(dot_O, UP, buff=0.55)")

# global: textos de 22 pt viram 28
for f in sorted(U.glob("sec_*.py")):
    s = f.read_text(encoding="utf-8")
    n = re.sub(r'(txt\("[^"]*", )22([,)])', r'\g<1>28\2', s)
    if n != s:
        f.write_text(n, encoding="utf-8")
        print("22→28 em", f.name)
