from pathlib import Path
from ptch6 import patch
U = Path(__file__).resolve().parent
s = (U / "kit.py").read_text(encoding="utf-8")
i = s.index("_REF_M = {}")
j = s.index("def eqp(*partes")
novo = r'''_REF_M = {}


def _massas_em_compostos(m, partes, idx, cores, size, COMP):
    """v7 #15/#33: massa (m, m_0, m_f, m_{02}, dm, P, f, f_1, f_2) dentro de ln, frac e int sai âmbar. Acha os glifos do tamanho principal por forma
    (a ordem do SVG segue a da string) e pareia com os tokens da string, em ordem; subíndice e o 'd' do dm acompanham."""
    for sym, pad in (("m", r"(?<![A-Za-z\\])(d?)m(?:_\{([^}]*)\}|_([0-9A-Za-z]))?(?![A-Za-z])"),
                     ("P", r"(?<![A-Za-z\\])()P(?:_\{([^}]*)\}|_([0-9A-Za-z]))?(?![A-Za-z])"),
                     ("f", r"(?<![A-Za-z\\])()f(?:_\{([^}]*)\}|_([0-9A-Za-z]))?(?![A-Za-z])")):
        key = (sym, size)
        if key not in _REF_M:
            _REF_M[key] = MathTex(sym, font_size=size)[0][0]
        ref = _REF_M[key]
        rp = ref.points - ref.get_center()
        for i, t in enumerate(partes):
            if i in cores or t in COMP or "mathrm" in t or cor_esperada(t) is not None:
                continue
            toks = [mt for mt in _re.finditer(pad, t)]
            if not toks:
                continue
            ms = [j for j in idx[i] if m[0][j].points.shape == ref.points.shape and np.abs((m[0][j].points - m[0][j].get_center()) - rp).max() < 2e-3]
            if len(ms) != len(toks):
                print(f"[aviso] massas em composto ({sym}): {len(toks)} tokens × {len(ms)} glifos em {t!r}")
                continue
            for mt, j in zip(toks, ms):
                gl = [j]
                if mt.group(1):
                    gl.append(j - 1)
                sub = mt.group(2) if mt.group(2) is not None else (mt.group(3) or "")
                gl += [j + 1 + k for k in range(len(sub.replace("\\", "")))]
                for g_ in gl:
                    m[0][g_].set_color(MAS)
                    m[0][g_].set_stroke(MAS, width=1.8, background=False)


'''
s = s[:i] + novo + s[j:]
s = s.replace(r'''    ((WHITE_,), (r"[=+\-()<>]", r"R", r"f", r"\\cdot")),''', r'''    ((WHITE_,), (r"[=+\-()<>]", r"R", r"\\cdot")),''', 1)
s = s.replace(r'''    ((MAS,), (r"m", r"m_0",''', r'''    ((MAS,), (r"P", r"f", r"f_1", r"f_2", r"m", r"m_0",''', 1)
(U / "kit.py").write_text(s, encoding="utf-8", newline="\n")
patch("sec_e1.py", [
 (r'''self.hip([["SUBIDA VERTICAL ·", MathTex("g", font_size=36, color=ACC), rot("= 9,8 m/s² · SEM AR", 26)]], x0=-2.0, wmax=9.4)''',
  r'''self.hip([["SUBIDA VERTICAL ·", MathTex("g", font_size=32, color=ACC), rot("= 9,8 m/s²", 24), "· SEM AR"]], x0=-2.0, wmax=9.4)'''),
 (r'''        l_dm = VGroup(MathTex(r"\left|\frac{dm}{dt}\right|=", font_size=36, color=MAS), rot("120 kg/s", 26, MAS)).arrange(RIGHT, buff=0.1).next_to(P3(XR - 0.85, YB - 0.7), LEFT, buff=0.1)''',
  r'''        l_dm = VGroup(MathTex(r"\left|\frac{dm}{dt}\right|=", font_size=36, color=MAS), rot("120 kg/s", 26, MAS)).arrange(DOWN, buff=0.08, aligned_edge=RIGHT)
        l_dm.move_to(P3(XR - 1.15 - l_dm.width / 2, YB + 0.55))                         # v7 #26: à esquerda da perna da torre, fora dela'''),
])
patch("sec_e2.py", [
 (r'''self.hip([["ESTRUTURA =", MathTex(r"0{,}1\,f", font_size=34), "· PERDAS JÁ NOS", rot("9 km/s", 26)]], x0=-2.0, wmax=9.4)''',
  r'''self.hip([["ESTRUTURA = 0,1", MathTex("f", font_size=32, color=MAS), "· PERDAS JÁ NOS", rot("9 km/s", 24)]], x0=-2.0, wmax=9.4)'''),
])
print("ok")
