"""Manequim 3D (geometria do hook do yt_0015, cena threejs/cena3d/maneq.js): poses calculadas aqui, por estado.
Unidades em metros; o Manim mostra com zoom K (vista 'frente', plano y = 0). O manequim olha para +x (esp = 1) ou −x (esp = −1)."""
from kit import *  # noqa: F401,F403

L1 = L2 = 0.46
ANK = 0.085
H_PE = 2 * L1 * math.cos(0.02) + ANK       # altura do quadril em pé
BR0 = [0.12, 0.04, 0.18]                    # braço solto


def alt_q(dobra):
    return 2 * L1 * math.cos(dobra / 2) + ANK


def lerp(a, b, u):
    return a + (b - a) * u


def lerpl(a, b, u):
    return [lerp(x, y, u) for x, y in zip(a, b)]


def pose_pe(x, esp=1, resp=0.0):
    """Em pé, respirando (resp = fase em rad)."""
    r = 0.006 * math.sin(resp)
    return {"hx": x, "hz": H_PE + r, "pes": [[x + 0.07 * esp, ANK, 0], [x - 0.05 * esp, ANK, 0]], "lam": 0.03, "cab": 0.03,
            "bracos": [BR0[:], BR0[:]], "esp": esp}


def pose_agarra(x, u, esp=1):
    """u = 0 (em pé) → 1 (braços fechados na frente do peito, segurando)."""
    p = pose_pe(x, esp)
    p["bracos"] = [lerpl(BR0, [0.28, 1.25, 1.55], u), lerpl(BR0, [0.28, 1.25, 1.55], u)]
    p["lam"] = lerp(0.03, 0.12, u)
    p["hz"] = H_PE - 0.03 * u
    p["cab"] = lerp(0.03, 0.18, u)
    return p


def pose_rebate(x, u, esp=1):
    """u: 0 em pé → 1 tronco recuando com o impacto no peito (braços abrindo)."""
    p = pose_pe(x, esp)
    b = math.sin(PI * min(1.0, u))
    p["bracos"] = [lerpl(BR0, [0.55, 0.5, 0.5], b), lerpl(BR0, [0.55, 0.5, 0.5], b)]
    p["lam"] = 0.03 - 0.16 * b
    p["cab"] = 0.03 - 0.2 * b
    return p


def pose_mira(x, ang, esp=1, recuo=0.0):
    """Segurando o rifle na altura do ombro; ang em rad acima da horizontal; recuo (0–1) joga o tronco para trás."""
    p = pose_pe(x, esp)
    p["pes"] = [[x + 0.16 * esp, ANK, 0], [x - 0.2 * esp, ANK, 0]]
    p["hz"] = alt_q(0.12)
    fl = 1.35 + 0.75 * ang
    p["bracos"] = [[0.35, fl, 0.85 - 0.2 * ang], [0.15, fl + 0.1, 0.45 - 0.1 * ang]]
    p["lam"] = -0.04 - 0.1 * recuo + 0.05 * ang
    p["cab"] = 0.1 - 0.15 * ang
    return p


def pose_andar(x, fase, esp=1, passo=0.62, sobe=0.07):
    """Ciclo de marcha: fase em ciclos (1 = dois passos). O pé de apoio fica parado no chão (atrito estático)."""
    g = []
    for i in (0, 1):
        ph = (fase + 0.5 * i) % 1.0
        if ph < 0.6:                     # apoio: o pé vai de +passo/2 a −passo/2 em relação ao quadril
            u = ph / 0.6
            dx, dz = passo * (0.5 - u), 0.0
        else:                            # balanço
            u = (ph - 0.6) / 0.4
            dx, dz = passo * (-0.5 + u), sobe * math.sin(PI * u)
        g.append([x + dx * esp, ANK + dz, -0.25 * math.sin(PI * u) if ph >= 0.6 else 0.0])
    bob = 0.018 * math.cos(4 * PI * fase)
    sw = 0.38 * math.sin(2 * PI * fase)
    return {"hx": x, "hz": alt_q(0.22) + bob, "pes": g, "lam": 0.08, "cab": 0.02,
            "bracos": [[0.1, sw, 0.3], [0.1, -sw, 0.3]], "esp": esp}


def mao(p, i):
    """Cinemática direta (igual à do maneq.js, no plano xz): posição (x, z) da ponta da mão do braço i."""
    esp, lam = p["esp"], p["lam"]
    abd, f, cot = p["bracos"][i]

    def ry(x, z, th):                                   # rotação em torno de y (convenção do three.js)
        return x * math.cos(th) + z * math.sin(th), -x * math.sin(th) + z * math.cos(th)

    def braco(th, L):
        x, z = math.sin(th) * L, -math.cos(th) * L * math.cos(abd)
        return ry(x, z, lam)
    sx, sz = ry(0.0, 0.33, lam)
    ux, uz = braco(f, 0.29)
    fx, fz = braco(f + cot, 0.32)
    return p["hx"] + esp * (sx + ux + fx), p["hz"] + 0.1 + sz + uz + fz


def mao3(p, i):
    """v5: a mão com a profundidade y (ombro a ±0,19 + abdução), para o mapa em perspectiva: (x, z, y)."""
    lado = 1 if i == 0 else -1
    abd, f, cot = p["bracos"][i]
    y = lado * 0.19 + math.sin(lado * abd) * (0.29 * math.cos(f) + 0.32 * math.cos(f + cot))
    return (*mao(p, i), y)


def boca(p, ang, s=0.0):
    """Boca do cano (e a bala s metros adiante) para o rifle nas mãos com inclinação ang."""
    x0, z0 = mao(p, 0)
    x1, z1 = mao(p, 1)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    d = (p["esp"] * math.cos(ang), math.sin(ang))
    return cx + d[0] * (0.76 + s), cz + d[1] * (0.76 + s), (cx, cz)


class Manequim3D:
    """Fundo 3D com o manequim. `pose(t)` → dict de pose (extras: bola, rifle, bala, chao)."""

    def __init__(self, cena, pose, K=2.0, xt=-3.4, yc=-2.6, camx=0.0, op=1.0, seguir=False, inst=None, cam_de=None):
        self.cena, self.pose, self.seguir = cena, pose, seguir
        if cam_de is not None:
            self.K, self.xt, self.yc, self.camx = cam_de.K, cam_de.xt, cam_de.yc, cam_de.camx
        else:
            self.K, self.xt, self.yc, self.camx = ValueTracker(K), ValueTracker(xt), ValueTracker(yc), ValueTracker(camx)
        self.f3d = Fundo3D(cena, "manequim", self.estado, op=op, inst=inst)

    def estado(self, t):
        e = dict(self.pose(t))
        cx = e["hx"] if self.seguir else self.camx.get_value()
        e["cam"] = cam_frente(K=self.K.get_value(), xc=self.xt.get_value(), yc=self.yc.get_value(), camx=cx, fov=16, el=3)
        return e

    def m(self, x, z, y=0.0):
        """Ponto do mundo (m) → Manim no quadro corrente."""
        return mapa_frente(self.f3d.e["cam"], x, z, y)

    def pts(self):
        e = self.f3d.e
        x, esp = e["hx"], e["esp"]
        return {"quadril": self.m(x, e["hz"]), "peito": self.m(x + 0.1 * esp, e["hz"] + 0.42), "cabeca": self.m(x, e["hz"] + 0.86),
                "pes": self.m(x, 0.0), "pe_frente": self.m(max(p[0] for p in e["pes"]) if esp > 0 else min(p[0] for p in e["pes"]), 0.0),
                "maos": self.m(x + 0.42 * esp, e["hz"] + 0.5)}


class ManequimLoop:
    """Duas instâncias do manequim 3D em crossfade, para loops e trocas de tomada sem corte seco.
    Segmentos: `novo(t, per)` começa um segmento em t (segundos da cena; ≥ agora + xf); com `per`, ele se repete a cada `per` s até o
    segmento seguinte. Cada ciclo (segmento k, repetição n) é de uma instância, alternando; nos `xf` s antes de um ciclo novo a outra
    instância entra já na pose inicial dele e as duas cruzam a opacidade. `pose_ciclo(k, n, s)` devolve a pose (s ≥ 0 desde o começo).
    As setas do Manim usam a instância do ciclo corrente (`e()`, `m()`, `real()`)."""

    def __init__(self, cena, pose_ciclo, K=2.0, xt=-3.4, yc=-2.6, camx=0.0, op=0.0, seguir=False, xf=0.6, per=None):
        self.cena, self.pc, self.xf = cena, pose_ciclo, xf
        self.seg = [[0.0, per, 0]]                  # [início, período, paridade da primeira repetição]
        self._ult = [None, None]
        self.q = [None, None]
        self.q[0] = Manequim3D(cena, lambda t: self._pose(0, t), K=K, xt=xt, yc=yc, camx=camx, op=op, seguir=seguir)
        self.q[1] = Manequim3D(cena, lambda t: self._pose(1, t), op=op, seguir=seguir, inst="b", cam_de=self.q[0])
        for j in (0, 1):
            self.q[j].f3d.mult = (lambda jj: lambda t: self.peso(jj, t))(j)
        self.K, self.xt, self.yc, self.camx = self.q[0].K, self.q[0].xt, self.q[0].yc, self.q[0].camx

    def novo(self, t, per=None):
        T, P, par = self.seg[-1]
        reps = 1 if P is None else int(math.floor((t - T - 1e-9) / P)) + 1
        self.seg.append([t, per, (par + reps) % 2])
        return t

    @property
    def inicios(self):
        return [sg[0] for sg in self.seg]

    def _cic(self, t):
        """(k, n, início, paridade) do ciclo que contém t."""
        k = max([i for i, sg in enumerate(self.seg) if sg[0] <= t + 1e-9] or [0])
        T, P, par = self.seg[k]
        n = 0 if P is None else max(0, int(math.floor((t - T + 1e-9) / P)))
        return k, n, T + (n * P if P else 0.0), (par + n) % 2

    def _prox(self, t):
        """Próximo ciclo (k, n, início, paridade) se começar em até xf s; senão None."""
        k, n, t0, par = self._cic(t)
        T, P, _ = self.seg[k]
        cand = []
        if P is not None:
            cand.append((T + (n + 1) * P, k, n + 1))
        if k + 1 < len(self.seg):
            cand.append((self.seg[k + 1][0], k + 1, 0))
        if not cand:
            return None
        ti, kk, nn = min(cand)
        if ti - t > self.xf:
            return None
        return kk, nn, ti, (self.seg[kk][2] + nn) % 2

    def ciclo(self, t):
        """(k, n, s) do ciclo corrente."""
        k, n, t0, _ = self._cic(t)
        return k, n, t - t0

    def resta(self, t):
        """Peso do ciclo corrente (1 → 0 nos xf s antes do próximo)."""
        nx = self._prox(t)
        return 1.0 if nx is None else max(0.0, (nx[2] - t) / self.xf)

    def peso(self, j, t):
        k, n, t0, par = self._cic(t)
        nx = self._prox(t)
        w = 1.0 if nx is None else max(0.0, (nx[2] - t) / self.xf)
        if par == j:
            return w if nx is None or nx[3] != j else 1.0
        return 1.0 - w if nx is not None and nx[3] == j else 0.0

    def _pose(self, j, t):
        k, n, t0, par = self._cic(t)
        nx = self._prox(t)
        if nx is not None and nx[3] == j and par != j:
            p = self.pc(nx[0], nx[1], 0.0)
        elif par == j:
            p = self.pc(k, n, t - t0)
        else:                                       # escondida: estado congelado (o r3d.js copia o PNG em vez de renderizar)
            return self._ult[j] if self._ult[j] is not None else self.pc(0, 0, 0.0)
        self._ult[j] = p
        return p

    def atual(self):
        return self.q[self._cic(self.cena.clk.get_value())[3]]

    @property
    def f3ds(self):
        return [q.f3d for q in self.q]

    def e(self):
        return self.atual().f3d.e

    def m(self, x, z, y=0.0):
        return self.atual().m(x, z, y)

    def real(self, chave):
        return self.atual().f3d.real(chave)

    def fade(self, valor, run_time=1.0):
        return [q.f3d.op.animate(run_time=run_time).set_value(valor) for q in self.q]


class ManequimTomadas:
    """v4: uma instância só do manequim; cada tomada começa numa virada em sequência (o 3D sai em 0,3 s, a pose troca, volta em
    0,3 s), nunca em crossfade entre duas posições. Mesma interface que o lote usa do ManequimLoop (ciclo, inicios, e, m, real)."""

    def __init__(self, cena, pose_ciclo, K=2.0, xt=-3.4, yc=-2.6, camx=0.0, op=0.0, seguir=False, xf=0.3):
        self.cena, self.pc, self.xf = cena, pose_ciclo, xf
        self.inicios = [0.0]
        self.q = Manequim3D(cena, lambda t: self._pose(t), K=K, xt=xt, yc=yc, camx=camx, op=op, seguir=seguir)
        self.f3d = self.q.f3d
        self.K, self.xt, self.yc, self.camx = self.q.K, self.q.xt, self.q.yc, self.q.camx

    def ciclo(self, t):
        k = max(i for i, t0 in enumerate(self.inicios) if t0 <= t + 1e-9) if t >= self.inicios[0] else 0
        return k, 0, t - self.inicios[k]

    def _pose(self, t):
        k, n, s = self.ciclo(t)
        return self.pc(k, n, s)

    def resta(self, t):
        return 1.0

    def troca(self, *anims):
        """Virada em sequência para uma tomada nova (as `anims` vão junto da saída)."""
        self.cena.play(self.f3d.op.animate.set_value(0.0), *anims, run_time=self.xf)
        self.inicios.append(self.cena.clk.get_value())
        self.cena.play(self.f3d.op.animate.set_value(1.0), run_time=self.xf)

    @property
    def f3ds(self):
        return [self.f3d]

    def e(self):
        return self.f3d.e

    def m(self, x, z, y=0.0):
        return self.q.m(x, z, y)

    def real(self, chave):
        return self.f3d.real(chave)

    def fade(self, valor, run_time=1.0):
        return [self.f3d.op.animate(run_time=run_time).set_value(valor)]
