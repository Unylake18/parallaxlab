"""yt_0030 v3 · a escada (alvos v3_ab e v3_s, e o P2): seis degraus da Parte 1 e quatro caixas da Parte 2, cada um com um ícone de 64 px desenhado
com as funções do próprio vídeo (o `icone()` do sb30v3). O mesmo desenho volta na abertura, no P2 e no resumo; no resumo só os rótulos trocam."""
from alg30 import *  # noqa: F401,F403

ESC = [("d1", "DOIS FILMES", "MESMA FÓRMULA, DOIS FILMES", GEO), ("d2", "DESENHAR UM CAMPO", "CURVAS ONDE NÃO MUDA", CAMPO2),
       ("d3", "REDEMOINHOS", "VOLTA ≠ GIRO", VEL), ("d3b", "DUAS REGRAS", "GRADIENTE NÃO GIRA", VEL),
       ("d4", "NÃO MELHORA DE PERTO", "PARCIAIS NÃO BASTAM", CORAL), ("d5", "O DESAFIO", "A TABELA PREVÊ", LIMA)]
APL = [("rio", "O RIO", "RIO QUE GIRA NAS MARGENS", VEL), ("jato", "O JATO NA PAREDE", "PAREDE: SÓ DEFORMA", LIMA),
       ("mapa", "MAPAS", "MAPAS QUE NÃO ENTORTAM", CORAL), ("fio", "1/r E 1/r²", "A CONTA ESCOLHE A LEI", CAMPO2)]


def caixa30(x0, y0, w, h, cor, alpha=1.0, z=18):
    r = RoundedRectangle(width=w / 120, height=h / 120, corner_radius=8 / 120).move_to(PX(x0 + w / 2, y0 + h / 2))
    r.set_fill(PLACA_V4, 0.92 * alpha).set_stroke(cor, 3 / 1.2, alpha)
    r._sem_contorno = True
    return r.set_z_index(z)


def _mini(v, F, cor=CAMPO, n=2, passo=1.0, L=.8):
    g = VGroup()
    k = int(round(n / passo))
    for i in range(-k, k + 1):
        for j in range(-k, k + 1):
            X, Y = i * passo, j * passo
            try:
                f = F(X, Y)
            except ZeroDivisionError:
                continue
            m = math.hypot(float(f[0]), float(f[1]))
            if m < 1e-9:
                continue
            u = (f[0] / m * L, f[1] / m * L)
            s = seta7(v.c2p(X - u[0] / 2, Y - u[1] / 2), v.c2p(X + u[0] / 2, Y + u[1] / 2), cor, 2, 6)
            for x in s.get_family():
                x._sem_contorno = True
            g.add(s)
    return g


def _vl(v, pts, cor, w, dash=None, alpha=1.0):
    m = vlinha(v, pts, cor, w, alpha=alpha, dash=dash)
    for x in m.get_family():
        x._sem_contorno = True
    return m


def _quad_ic(v, pts, n=2, w=2):
    """Quadradinho pequeno (chapa + malha n×n + contorno coral) pelos quatro cantos (bilinear)."""
    A, B, C, D = [np.asarray(p, float) for p in pts]
    P_ = lambda a, b: A + (B - A) * a + (D - A) * b + (A - B + C - D) * a * b
    g = VGroup(preenche(v, [tuple(P_(a, b)) for a, b in ((0, 0), (1, 0), (1, 1), (0, 1))], CHAPA_C, 1.0, 1))
    for k in range(1, n):
        g.add(_vl(v, [tuple(P_(k / n, 0)), tuple(P_(k / n, 1))], CORAL, w * .6), _vl(v, [tuple(P_(0, k / n)), tuple(P_(1, k / n))], CORAL, w * .6))
    g.add(_vl(v, [tuple(P_(a, b)) for a, b in ((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))], CORAL, w))
    return g


def icone(k, cx, cy):
    """Ícone de 64 px (mini-campo) centrado em (cx, cy) px."""
    v = Vista(cx, cy, 13)
    g = VGroup()
    if k == "d1":
        v = Vista(cx, cy, 16)
        g.add(_quad_ic(v, [(-1.4, -1.4), (0, -1.4), (0, 0), (-1.4, 0)]))
        g.add(_quad_ic(v, [(p[0] - .2, p[1] + .3) for p in ((0, 0), (1, 1), (2, 0), (1, -1))]))
    elif k == "d2":
        for c in (-2, 0, 2):
            g.add(_vl(v, [(-2.4, -2.4 - c), (2.4, 2.4 - c)] if c == 0 else ([(-2.4 + c, -2.4), (2.4, 2.4 - c)] if c > 0 else [(-2.4, -2.4 - c), (2.4 + c, 2.4)]),
                      GEO, 1.5, dash=(3, 3)))
        g.add(_mini(v, F2))
    elif k == "d3":
        g.add(_mini(v, VORTA(.5)))
    elif k == "d3b":
        for kk in (1, 4):
            for sg in (1, -1):
                ys = np.linspace(-2.4, 2.4, 25)
                pts = [(sg * math.sqrt(kk + y * y), y) for y in ys if math.sqrt(kk + y * y) <= 2.45]
                if len(pts) > 1:
                    g.add(_vl(v, pts, GEO, 1.5, dash=(3, 3)))
        g.add(_mini(v, F_SELA))
    elif k == "d4":
        g.add(_mini(v, F4))
    elif k == "d5":
        v = Vista(cx, cy, 16)
        g.add(_quad_ic(v, quad_pts((0, 0), 2)))
        g.add(_vl(v, circ_pts(1.5, (0, 0), 20, -.15, 1.75), VEL, 3))
    elif k == "rio":
        g.add(_vl(v, [(-2.4, -2.4), (-2.4, 2.4)], GEO, 2), _vl(v, [(2.4, -2.4), (2.4, 2.4)], GEO, 2))
        g.add(_mini(v, lambda X, Y: (0.0, 1 - X * X / 5.5)))
    elif k == "jato":
        g.add(_vl(v, [(-2.4, -2.2), (2.4, -2.2)], GEO, 3))
        g.add(_mini(v, lambda X, Y: (X, -(Y + 2.2))))
    elif k == "mapa":
        v = Vista(cx - 22, cy + 28, 20)
        f3 = lambda p: (p[0] * p[0] - p[1] * p[1], 2 * p[0] * p[1])
        for kk in range(3):
            g.add(_vl(v, [f3((.5 + kk * .5, i / 20)) for i in range(21)], CORAL, 2))
            g.add(_vl(v, [f3((.5 + i / 20, kk * .5)) for i in range(21)], CORAL, 2))
    elif k == "fio":
        g.add(_mini(v, VORTA(1)))
        g.add(preenche(v, circ_pts(.45), "#0F0C26", 1.0, 1), _vl(v, circ_pts(.45), BR, 1.5))
    for x in g.get_family():
        x._sem_contorno = True
    return g.set_z_index(20)


class Degrau(VGroup):
    """Caixa + ícone + rótulo; .caixa, .ic, .rot. modo 'ab' (tema) ou 's' (lição)."""

    def __init__(self, i, parte=1, modo="ab", alpha=1.0):
        super().__init__()
        if parte == 1:
            ic, a, b, c = ESC[i]
            X0, Y0, w = 120 + i * 130, 905 - i * 96, 505
            self.caixa = caixa30(X0, Y0 - 70, w, 82, c, alpha)
            self.ic = icone(ic, X0 + 46, Y0 - 29)
            self.rot = T(b if modo == "s" else a, X0 + 92, Y0 - 17, 26, cor=BR, up=False)
            self.box = (X0, Y0 - 70, X0 + w, Y0 + 12)
        else:
            ic, a, b, c = APL[i]
            Y0 = 370 + i * 112
            self.caixa = caixa30(1330, Y0, 470, 90, c, alpha)
            self.ic = icone(ic, 1376, Y0 + 45)
            self.rot = T(b if modo == "s" else a, 1422, Y0 + 56, 26, cor=BR, up=False)
            self.box = (1330, Y0, 1800, Y0 + 90)
        self.cor, self.parte, self.i = c, parte, i
        self.rot._leg = False
        self.add(self.caixa, self.ic, self.rot)

    def opacidade(self, a):
        self.caixa.set_fill(PLACA_V4, 0.92 * a).set_stroke(self.cor, 3 / 1.2, a)
        for x in self.ic.family_members_with_points():
            if x.get_stroke_width() > 0:
                x.set_stroke(opacity=a)
            if x.get_fill_opacity() > 0:
                x.set_fill(opacity=a)
        self.rot.set_opacity(a)
        return self


def titulos_escada():
    p1 = legenda("PARTE 1 · A ESCADA", 120, 975, GEO, "left", 28)
    p2 = legenda("PARTE 2 · AS APLICAÇÕES", 1565, 330, GEO, "center", 28)
    return p1, p2


def degrau_entra(cena, ds, rt=0.8, extra=()):
    """Os degraus são desenhados: a caixa (traço), depois o ícone e o texto (dois plays; nada de Succession, que põe o fim na cena no instante 0)."""
    ds = list(ds)
    cena.play(*[Create(d.caixa) for d in ds], *extra, run_time=rt * .45)
    cena.play(*[FadeIn(d.ic) for d in ds], *[FadeIn(d.rot, shift=0.04 * UP) for d in ds], run_time=rt * .55)
