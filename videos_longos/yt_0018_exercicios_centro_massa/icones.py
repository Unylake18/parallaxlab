"""yt_0018 — ícones das quatro ferramentas (A2, A3, S2): desenhos 2D pequenos (o 3D fica só no X2, X5 e EN2, G17)."""
from prob import *  # noqa: F401,F403

ROTULOS = (("TIRAR MASSA",), ("MONTAR", "POR PARTES"), ("⊕ PARADO,", "DOIS REFERENCIAIS"), ("REFERENCIAL", "DO CM"), ("⊕ ACELERA →", "FORÇA EXTERNA"))
CURTOS = ("TIRAR MASSA", "POR PARTES", "⊕ PARADO", "REFERENCIAL DO CM", "⊕ ACELERA")


def icone(k, s=1.0):
    """Ícone k (0 placa com furo · 1 fio no cubo · 2 gafanhoto com duas réguas · 3 naves se afastando), ~1,6 × 1,3 em s = 1."""
    k = (0, 1, 2, 3, 4)[k]
    if k == 0:
        pl = aco(Difference(Square(1.3), Circle(radius=0.3).shift(P3(0.25, 0.25))), 1.6)
        g = VGroup(pl, fantasma_circ(P3(0.25, 0.25), 0.3), marcador_cm(P3(-0.12, -0.12), r=0.11))
    elif k == 1:
        o, ex, ey, ez = P3(-0.55, -0.5), P3(0.75, -0.18), P3(0.42, 0.24), P3(0.0, 0.85)
        c = lambda a, b, d: o + a * ex + b * ey + d * ez
        ar = VGroup()
        for p_ in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)):
            for d_ in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                q = tuple(a + b for a, b in zip(p_, d_))
                if max(q) <= 1:
                    ar.add(Line(c(*p_), c(*q)).set_stroke(GEO, 1.4, opacity=0.35))
        fio = VMobject().set_points_as_corners([c(0, 0, 0), c(1, 0, 0), c(1, 1, 0), c(1, 1, 1)]).set_stroke("#9AA6B8", 6)
        g = VGroup(ar, fio, marcador_cm(c(5 / 6, 1 / 2, 1 / 6), r=0.11))
    elif k == 2:
        fo = folha(1.3, 0.2).shift(P3(-0.55, -0.25))
        ga = gafanhoto(0.42).shift(P3(-0.45, -0.24))
        r1 = VGroup(Line(P3(-0.8, -0.62), P3(0.85, -0.62)).set_stroke(GEO, 2), *[Line(P3(x, -0.62), P3(x, -0.7)).set_stroke(GEO, 2) for x in np.linspace(-0.7, 0.75, 6)])
        r2 = VGroup(Line(P3(-0.55, 0.05), P3(0.75, 0.05)).set_stroke(mix(GEO, 0.25), 2), *[Line(P3(x, 0.05), P3(x, 0.12)).set_stroke(mix(GEO, 0.25), 2) for x in np.linspace(-0.5, 0.7, 5)])
        g = VGroup(r1, fo, ga, r2, marcador_cm(P3(0.15, 0.45), r=0.11))
    elif k == 4:
        base = aco(RoundedRectangle(corner_radius=0.05, width=1.5, height=0.22).move_to(P3(0, -0.62)), 1.4)
        tela = Rectangle(width=0.42, height=0.13).move_to(P3(0.45, -0.62)).set_fill("#06222E", 1).set_stroke(CMC, 1.4)
        sup = VGroup(Line(P3(-0.45, -0.5), P3(-0.45, 0.55)).set_stroke("#9AA6B8", 5), Line(P3(0.45, -0.5), P3(0.45, 0.55)).set_stroke("#9AA6B8", 5),
                     Line(P3(-0.5, 0.55), P3(0.5, 0.55)).set_stroke("#9AA6B8", 5))
        pol = Circle(radius=0.13).move_to(P3(0, 0.55)).set_fill("#3A4252", 1).set_stroke("#7FB2FF", 1.6)
        fio = VGroup(Line(P3(-0.13, 0.55), P3(-0.13, -0.05)).set_stroke(GEO, 1.4), Line(P3(0.13, 0.55), P3(0.13, 0.15)).set_stroke(GEO, 1.4))
        b1, b2 = aco(Square(0.24).move_to(P3(-0.13, -0.17)), 1.2), aco(Square(0.17).move_to(P3(0.13, 0.06)), 1.2)
        g = VGroup(base, tela, sup, fio, pol, b1, b2, marcador_cm(P3(-0.05, -0.12), r=0.1), seta(P3(0.82, 0.2), P3(0.82, -0.3), FC, 3, tip=0.1))
    else:
        n1, n2 = nave(0.75, 0.34, 1).move_to(P3(0.5, 0.15)), nave(0.95, 0.44, -1).move_to(P3(-0.55, 0.15))
        g = VGroup(n1, n2, seta(P3(0.95, -0.35), P3(1.35, -0.35), MAG, 3, tip=0.1), seta(P3(-0.95, -0.35), P3(-1.35, -0.35), MAG, 3, tip=0.1),
                   marcador_cm(P3(-0.2, -0.35), r=0.11))
    return g.scale(s)


def item(k, s=1.0, size=28, linhas=None):
    """Ícone com o rótulo embaixo."""
    lab = VGroup(*[tx(l, size, bold=True) for l in (linhas or ROTULOS[k])]).arrange(DOWN, buff=0.08)
    return VGroup(icone(k, s), lab).arrange(DOWN, buff=0.22)
