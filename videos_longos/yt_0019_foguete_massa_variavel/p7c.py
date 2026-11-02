from ptch6 import patch
patch("kit.py", [
 (r'''    for i, c in cores.items():
        for j in idx[i]:
            m[0][j].set_color(c)
    for i, c in list(cores.items())''',
  r'''    for i, c in cores.items():
        for j in idx[i]:
            m[0][j].set_color(c)
    _massas_em_compostos(m, partes, idx, cores, size, COMP)
    for i, c in list(cores.items())'''),
 (r'''def eqp(*partes, size=M_MID, cores=None):''',
  r'''_REF_M = {}


def _massas_em_compostos(m, partes, idx, cores, size, COMP):
    """v7 #15: massa (m, m_0, m_f, m_{02}, dm) dentro de \ln, \frac e \int sai âmbar. Acha os glifos 'm' do tamanho principal por forma (a ordem do
    SVG segue a da string) e pareia com os tokens de massa da string, em ordem; subíndice e o 'd' do dm acompanham."""
    if size not in _REF_M:
        _REF_M[size] = MathTex("m", font_size=size)[0][0]
    ref = _REF_M[size]
    rp = ref.points - ref.get_center()
    for i, t in enumerate(partes):
        if i in cores or t in COMP or "mathrm" in t or cor_esperada(t) is not None:
            continue
        toks = [mt for mt in _re.finditer(r"(?<![A-Za-z\\])(d?)m(?:_\{([^}]*)\}|_([0-9A-Za-z]))?(?![A-Za-z])", t)]
        if not toks:
            continue
        ms = [j for j in idx[i] if m[0][j].points.shape == ref.points.shape and np.abs((m[0][j].points - m[0][j].get_center()) - rp).max() < 2e-3]
        if len(ms) != len(toks):
            print(f"[aviso] massas em composto: {len(toks)} tokens × {len(ms)} glifos em {t!r}")
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


def eqp(*partes, size=M_MID, cores=None):'''),
])
