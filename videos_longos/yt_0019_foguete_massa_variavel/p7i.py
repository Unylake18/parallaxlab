from ptch6 import patch
patch("kit.py", [
 (r'''    m = screen_text(s, size, color=color, oversample=4).set_opacity(op)
    m._tam = size
    return m''', r'''    m = screen_text(s, size, color=color, oversample=4).set_opacity(op)
    m._tam = size
    m._s, m._rot = s, True
    return m'''),
])
patch("prob2.py", [
 (r'''    s = getattr(m, "_s", None)
    if not s or not isinstance(m, Mobject):
        return 0.0
    s2 = s.upper().translate(str.maketrans({"Ç": "C", "Q": "O", ",": "", ";": "", "J": "I", "Ô": "O"}))
    if s2 == s.upper() or not s2.strip():
        return 0.0
    return max(0.0, m.height - txt(s2, getattr(m, "_tam", 24), bold=getattr(m, "_bold", False)).height)''',
  r'''    s = getattr(m, "_s", None)
    if not s or not isinstance(m, Mobject):
        return 0.0
    # v7: parênteses, colchetes, barras, setas e as descendentes minúsculas (g j p q y) também descem da linha de base
    mapa = {"Ç": "C", "ç": "c", "Q": "O", "q": "o", ",": "", ";": "", "J": "I", "j": "i", "Ô": "O", "g": "o", "p": "o", "y": "v",
            "(": "I", ")": "I", "[": "I", "]": "I", "/": "I", "|": "I", "→": "I", "⇒": "I", "<": "I", ">": "I"}
    rot_ = getattr(m, "_rot", False)
    base = s if rot_ else s.upper()
    s2 = base.translate(str.maketrans(mapa))
    if s2 == base or not s2.strip():
        return 0.0
    ref = rot(s2, getattr(m, "_tam", 24)) if rot_ else txt(s2, getattr(m, "_tam", 24), bold=getattr(m, "_bold", False))
    return max(0.0, m.height - ref.height)'''),
])
print("ok")
