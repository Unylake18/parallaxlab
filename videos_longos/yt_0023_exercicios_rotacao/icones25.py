"""v6: ícones 2.5D dos quatro exercícios (volante, haste, carretel, disco) para a abertura (PH A2) e o resumo (PS S1)."""
from pecas23 import *  # noqa: F401,F403
from pecas23b import haste25
from sec_e4 import disco25


def ic25(k, c, ang=0.0):
    """v6 PS: ícones 2.5D (os mesmos objetos dos exercícios: volante verde-escuro, haste de aço, carretel escuro, disco de aço) no lugar dos ícones de linha."""
    c = np.asarray(c, float)
    if k == 0:
        s = 1.55
        xt = c[0] + 0.158 * s
        return VGroup(volante25(c, s, ang), Line([xt, c[1], 0], [xt, c[1] - 1.0, 0]).set_stroke("#D8E2F5", 2.2).set_z_index(4.9), bloco25(np.array([xt, c[1] - 1.12, 0.0]), 0.26)).set_z_index(4)
    if k == 1:
        th, LH = 0.5, 1.8
        O = c + np.array([-0.7, 0.45, 0.0])
        u = np.array([math.cos(th), -math.sin(th), 0.0])
        return haste25(O, O + 0.25 * LH * u, th, LH, esp=0.26).set_z_index(4)
    if k == 2:
        Rg, Rp = 0.62, 0.22
        return VGroup(carretel25(c, Rg, Rp, ang),
                      Line(c + Rg * RIGHT, c + Rg * RIGHT + 0.85 * DOWN).set_stroke(LINHA_CL, 2.2).set_z_index(5), Line(c + Rp * LEFT, c + Rp * LEFT + 1.2 * DOWN).set_stroke(LINHA_CL, 2.2).set_z_index(5),
                      bloco25(c + Rg * RIGHT + 0.98 * DOWN, 0.26).set_z_index(6), bloco25(c + Rp * LEFT + 1.36 * DOWN, 0.34).set_z_index(6)).set_z_index(4)
    return VGroup(Line(c + 0.85 * UP, c, ).set_stroke("#8FA6C9", 4), disco25(c, 0.3, R=0.55).set_z_index(4.2), pino25_(c + 0.85 * UP)).set_z_index(4)


def pino25_(o):
    return VGroup(Circle(radius=0.1).move_to(o).set_fill("#0F1A33", 1).set_stroke(AÇO_CLARO, 2.2), Dot(o, radius=0.03, color=AÇO_CLARO)).set_z_index(5)
