"""Acabamento dos pulsos de corrente (convenção do 5.2): pontas redondas, traço mais grosso, contorno na cor do fundo e
cabeça mais clara que a cauda. Corrente = traço alongado verde (nunca bolinha); dℓ continua branco."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
fails = []


def rep(a, b):
    global s
    if s.count(a) != 1:
        fails.append("(%d x) %s" % (s.count(a), a[:90]))
        return
    s = s.replace(a, b)


rep("from manim import CurvedArrow, DashedVMobject, TransformMatchingTex, ManimColor, TransformFromCopy, interpolate_color",
    "from manim import CurvedArrow, DashedVMobject, TransformMatchingTex, ManimColor, TransformFromCopy, interpolate_color, CapStyleType")
rep('''def panel(m, pad=0.28, op=0.55, color=PANEL, stroke=BLUE_L):''', '''def pulso(a, b, op=1.0, w=7.5, z=2):
    """Pulso de corrente: traço alongado verde de pontas redondas; contorno na cor do fundo (destaca do aço e do fio) e cabeça
    (metade da frente, no sentido a→b) mais clara que a cauda. Nunca uma bolinha (bolinha lê como carga)."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    mid = (a + b) / 2

    def seg(p, q, o):
        ln = Line(p, q, color=GREEN, stroke_width=w, cap_style=CapStyleType.ROUND).set_stroke(opacity=o * op)
        return ln.set_stroke(BACKGROUND_COLOR, w + 3.5, opacity=op, background=True)

    return VGroup(seg(a, mid, 0.55), seg(mid, b, 1.0)).set_z_index(z)


def panel(m, pad=0.28, op=0.55, color=PANEL, stroke=BLUE_L):''')
rep('''                    g.add(Line([wx(sign, y), y, 0], [wx(sign, y2), y2, 0], color=GREEN, stroke_width=5).set_opacity(0.95 * op))''',
    '''                    g.add(pulso([wx(sign, y), y, 0], [wx(sign, y2), y2, 0], op=op))''')
rep('''                    g.add(Line([x, y, 0], [x, y2, 0], color=GREEN, stroke_width=5).set_opacity(0.95 * op * self.g9b.get_value()))''',
    '''                    g.add(pulso([x, y, 0], [x, y2, 0], op=op * self.g9b.get_value()))''')
open(dst, "w", encoding="utf-8").write(s)
print("falhas:", len(fails))
for f in fails:
    print(" -", f)
