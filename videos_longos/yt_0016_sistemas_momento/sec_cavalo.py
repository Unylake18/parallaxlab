"""Cavalo 3D (asset CC0 do yt_0015, cena threejs/cena3d/cav.js) dirigido por estado, com os pontos da corda/cascos/pedra em
coordenadas do Manim (mapa analítico da vista 'frente'; o r3d.js grava as projeções reais para o QA de alinhamento).

Movimento: v(t) em unidades/s (1 unidade ≈ 1 m na cena); a posição e a fase do passo são integradas quadro a quadro.
A câmera acompanha o peitoral: ele aparece em Manim x = `xt` (tracker); `K` é o zoom e `yc` a altura do chão no Manim."""
from kit import *  # noqa: F401,F403

LARG, ALT, MEIA, PEITO_Z, CORDA_Z0 = 4.0, 3.3995, 0.471, 2.0397, 0.5045
PEDRA_R, Z_PEDRA, XPF = 0.5, 0.3795, 0.6768
CLIP, PASSO = 1.1667, 2.6          # duração do ciclo Walk (s) e distância por ciclo (unidades)
Y_CORDA = -MEIA - 0.02


class Cavalo3D:
    def __init__(self, cena, v=lambda t: 0.45, L=4.6, K=1.0, xt=1.5, yc=-2.2, op=1.0, deslize=lambda t: 0.0,
                 gelo=lambda t: 0.0, incl=0.05):
        self.cena, self.v, self.L, self.deslize, self.gelo, self.incl = cena, v, L, deslize, gelo, incl
        self.K, self.xt, self.yc = ValueTracker(K), ValueTracker(xt), ValueTracker(yc)
        self.gx = None                      # faixa de gelo (x0, x1) em coordenadas do mundo
        self._x, self._tau = {-1: 0.0}, {-1: 0.0}
        self.f3d = Fundo3D(cena, "cavalo", self.estado, op=op)

    def _acum(self, f):
        if f in self._x:
            return self._x[f], self._tau[f]
        k = max(q for q in self._x if q < f)
        for q in range(k + 1, f + 1):
            t = q / FPS
            vq = self.v(t)
            self._x[q] = self._x[q - 1] + vq / FPS
            self._tau[q] = self._tau[q - 1] + (abs(vq) / PASSO * CLIP + self.deslize(t)) / FPS
        return self._x[f], self._tau[f]

    def cam(self, xp):
        return cam_frente(K=self.K.get_value(), xc=self.xt.get_value(), yc=self.yc.get_value(), camx=xp, fov=16, el=3)

    def estado(self, t):
        f = int(round(t * FPS))
        xp, tau = self._acum(f)
        e = {"xp": xp, "tau": tau % (CLIP * 1000), "incl": self.incl, "L": self.L, "gelo": self.gelo(t), "cam": self.cam(xp)}
        if self.gx:
            e["gx0"], e["gx1"] = self.gx(t, xp) if callable(self.gx) else self.gx
        return e

    def x_mundo(self):
        return self.f3d.e["xp"]

    def pts(self):
        """Pontos do quadro corrente em coordenadas do Manim."""
        e = self.f3d.e
        c, xp = e["cam"], e["xp"]
        xa = xp - self.L
        xpd = xa - XPF * 0.92
        xcav = xp - 0.24 * LARG
        m = lambda x, z, y=0.0: mapa_frente(c, x, z, y)
        return {"peito": m(xp, PEITO_Z, Y_CORDA), "corda_pedra": m(xa, CORDA_Z0, Y_CORDA),
                "cascos": m(xcav, 0), "cascos_tras": m(xcav - 1.3, 0), "cascos_frente": m(xcav + 1.25, 0),
                "topo": m(xcav, ALT + 0.1), "cav_tras": m(xcav - LARG / 2, ALT * 0.55), "cav_frente": m(xcav + LARG / 2, ALT * 0.55),
                "cabeca": m(xcav + LARG / 2 - 0.2, ALT), "pedra": m(xpd, Z_PEDRA), "pedra_base": m(xpd, 0),
                "pedra_tras": m(xpd - PEDRA_R * 1.25, Z_PEDRA), "pedra_topo": m(xpd, 2 * Z_PEDRA)}

    def u_corda(self):
        p = self.pts()
        d = p["peito"] - p["corda_pedra"]
        return d / np.linalg.norm(d)
