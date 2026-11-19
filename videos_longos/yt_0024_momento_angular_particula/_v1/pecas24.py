"""yt_0024 — peças comuns: câmeras da mesa (C_34, C_TOPO, C_L) com a MESMA projeção do mesa.js, a mesa viva (Fundo3D 'mesa_furo' dirigido
pelo relógio da cena e pela física de fisica24.py), camadas Manim presas à mesa, mostradores, ⊙/⊗, sublinhado de resultado, auditoria de
OPACIDADE (yt_0023) e registro ÁLGEBRA. Base dos lotes: Lote24."""
from pecas22 import *  # noqa: F401,F403
import fisica24 as F

LMAG = "#F19AFF"
RAD = math.pi / 180


# ── câmeras ────────────────────────────────────────────────────────────────────────────────────────────────
def camd(az, el, alvo, K, fov, xc, yc):
    return dict(az=float(az), el=float(el), alvo=[float(a) for a in alvo], K=float(K), fov=float(fov), xc=float(xc), yc=float(yc))


C34H = camd(-55, 22, (0, 0, -0.34), 4.6, 43.6, 0.0, -0.35)        # hook: a mesa no centro da tela
C34 = camd(-55, 22, (0.0, 0.05, -0.12), 4.4, 43.6, -4.55, -0.55)      # teoria: a mesa na coluna esquerda
CTOPO = camd(-90, 90, (0, 0, 0), 4.7, 0.0, -3.75, -0.95)          # ortográfica de cima: 1,30 m × 1,30 m do tampo na coluna esquerda
CL = camd(-55, 35, (0, 0, 0), 4.1, 43.6, -3.70, -1.25)            # L⃗ saindo do plano


def interp_cam(a, b, u):
    """Dolly contínuo a → b (u já suavizado). Para a ortográfica: o fov encolhe até 0,5° com a escala do alvo fixa; no fim (u = 1) troca para
    a ortográfica (diferença ≤ 0,03 px no plano do tampo)."""
    if u <= 0:
        return dict(a)
    if u >= 1:
        return dict(b)
    c = {k: a[k] + (b[k] - a[k]) * u for k in ("az", "el", "K", "xc", "yc")}
    c["alvo"] = [a["alvo"][i] + (b["alvo"][i] - a["alvo"][i]) * u for i in range(3)]
    fa, fb = a["fov"] or 0.5, b["fov"] or 0.5
    c["fov"] = math.exp(math.log(fa) + (math.log(fb) - math.log(fa)) * u)
    return c


def _base(c):
    a, e = c["az"] * RAD, c["el"] * RAD
    al = np.array(c["alvo"], float)
    d = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    up = np.array([-math.sin(e) * math.cos(a), -math.sin(e) * math.sin(a), math.cos(e)])
    f = -d
    r = np.cross(f, up)
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    return al, d, f, r, u


def proj(c, p):
    """Ponto 3D (m) → Manim, pela mesma câmera do mesa.js (perspectiva com setViewOffset, ou ortográfica)."""
    al, d, f, r, u = _base(c)
    p = np.asarray(p, float)
    if c["fov"] > 0:
        th = math.tan(c["fov"] * RAD / 2)
        D = (9 / c["K"] / 2) / th
        q = p - (al + D * d)
        z = q @ f
        return np.array([c["xc"] + 8 / (th * 16 / 9) * (q @ r) / z, c["yc"] + 4.5 / th * (q @ u) / z, 0.0])
    q = p - al
    return np.array([c["xc"] + c["K"] * (q @ r), c["yc"] + c["K"] * (q @ u), 0.0])


def px_de(m):
    return [(m[0] + 8) / 16 * 960, (4.5 - m[1]) / 9 * 540]


# ── símbolos e peças ────────────────────────────────────────────────────────────────────────────────────────
def sai_entra(c, saindo=True, r=0.22, cor=LMAG, z=14):
    """⊙ (saindo do plano) / ⊗ (entrando) na cor do momento angular."""
    circ = Circle(radius=r).move_to(c).set_stroke(cor, 3.2)
    if saindo:
        mio = Dot(c, radius=0.06 * r / 0.22 + 0.01, color=cor)
    else:
        k = 0.62 * r
        mio = VGroup(Line(c + P3(-k, -k), c + P3(k, k)), Line(c + P3(-k, k), c + P3(k, -k))).set_stroke(cor, 3.0)
    return VGroup(circ, mio).set_z_index(z)


def sublinha(m, cor, w=3, buff=0.1):
    """Sublinhado fino do resultado (no lugar da caixa), na cor da grandeza do lado esquerdo."""
    l = Line(m.get_corner(DL) + DOWN * buff, m.get_corner(DR) + DOWN * buff).set_stroke(cor, w)
    l._sub = True
    return l.set_z_index(m.z_index or 0)


def angulo_reto(v, a, b, s=0.2, cor=GEO, w=2.4):
    """Marca de ângulo reto no vértice v entre as direções v→a e v→b."""
    u1 = (np.asarray(a) - v) / max(np.linalg.norm(np.asarray(a) - v), 1e-6)
    u2 = (np.asarray(b) - v) / max(np.linalg.norm(np.asarray(b) - v), 1e-6)
    return VMobject().set_points_as_corners([v + s * u1, v + s * (u1 + u2), v + s * u2]).set_stroke(cor, w).set_z_index(13)


def arco_ang(v, a, b, r=0.5, cor=ANG, w=4):
    """Arco âmbar no vértice v de v→a até v→b (menor ângulo)."""
    a0 = math.atan2(a[1] - v[1], a[0] - v[0])
    a1 = math.atan2(b[1] - v[1], b[0] - v[0])
    da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return Arc(radius=r, start_angle=a0, angle=da, arc_center=v).set_stroke(cor, w).set_z_index(13)


def pino2d(c, r=0.13):
    """Ponto fixo O como pino de aço 2.5D (disco com brilho)."""
    g = VGroup(Circle(radius=r).move_to(c).set_fill("#7A8696", 1).set_stroke("#C9D3E3", 2),
               Circle(radius=r * 0.45).move_to(c + P3(-0.3 * r, 0.3 * r)).set_fill("#DDE6F3", 0.85).set_stroke(width=0))
    g._degrade = "aco"
    return g.set_z_index(10)


def pedra2d(c, r=0.30):
    """Pedra rosa 2.5D (massa): polígono irregular com sombreado."""
    rng = np.random.default_rng(5)
    pts = [c + r * (0.85 + 0.25 * rng.random()) * np.array([math.cos(a), math.sin(a), 0]) for a in np.linspace(0, 2 * math.pi, 11)[:-1]]
    corpo = Polygon(*pts).set_fill(escuro(MAS, 0.35), 1).set_stroke(MAS, 3)
    luz = Polygon(*[c + 0.45 * (p - c) + P3(-0.08, 0.08) for p in pts]).set_fill(mix(MAS, 0.35), 0.5).set_stroke(width=0)
    return VGroup(corpo, luz).set_z_index(10)


def sol2d(c, r=0.32):
    g = VGroup(*[Circle(radius=r * k).move_to(c).set_fill("#FFC24D", 0.10 + 0.0 * k).set_stroke(width=0) for k in (2.4, 1.8, 1.35)],
               Circle(radius=r).move_to(c).set_fill("#FFD27A", 1).set_stroke("#FFF1C9", 2))
    return g.set_z_index(9)


def mao_rd(c, s=1.0, cor="#C9D3E3"):
    """Ícone 2.5D da regra da mão direita: quatro dedos curvando (de r para p) e o polegar para cima (L)."""
    palma = RoundedRectangle(width=0.55 * s, height=0.42 * s, corner_radius=0.12 * s).move_to(c).set_fill("#3A465A", 1).set_stroke(cor, 2)
    dedos = VGroup(*[Arc(radius=(0.30 - 0.03 * k) * s, start_angle=-0.2, angle=2.6, arc_center=c + P3(0.20 * s, (0.12 - 0.08 * k) * s))
                     .set_stroke(cor, 5 - 0.4 * k) for k in range(4)])
    polegar = Line(c + P3(-0.12 * s, 0.18 * s), c + P3(-0.12 * s, 0.78 * s)).set_stroke(LMAG, 7)
    ponta = Triangle().scale(0.09 * s).move_to(c + P3(-0.12 * s, 0.84 * s)).set_fill(LMAG, 1).set_stroke(width=0)
    return VGroup(palma, dedos, polegar, ponta).set_z_index(16)


def num(v, casas=2, sinal=False):
    s = f"{v:+.{casas}f}" if sinal else f"{v:.{casas}f}"
    return s.replace("-", "-").replace(".", "{,}")


# ── base dos lotes ─────────────────────────────────────────────────────────────────────────────────────────
class Lote24(Lote22):
    """Base: mesa viva (opcional), relógio físico, canto de duas linhas com MathTex, OPACIDADE e ÁLGEBRA."""

    def setup_base(self, cap=None, selo=None):
        super().setup_base(cap, selo)
        self.pilha = Pilha(self, x0=0.7, topo=2.35, base=-3.30, buff=0.30)
        self.f3 = None
        self.camA = self.camB = C34
        self.camu = ValueTracker(0.0)
        self.add(self.camu)
        self._tf0, self._c0, self._vel = 0.0, 0.0, 0.0          # tempo físico = tf0 + vel·(clk − c0)
        self.mov = lambda tf: (F.R0 * math.cos(F.W0 * tf), F.R0 * math.sin(F.W0 * tf))
        self.zp = lambda tf: 0.0
        self.fio, self.pinos, self.desf, self.rastro_on = True, [], 0.0, True
        self.disco_on = True
        self.extra3 = {}
        self.desf_tr = ValueTracker(0.0)
        self.add(self.desf_tr)
        self.tp = 1e9                                            # início da puxada (tempo físico); 1e9 = sem puxada

    # relógio físico
    def tf(self):
        return self._tf0 + self._vel * (self.clk.get_value() - self._c0)

    def anda(self, vel=1.0, tf=None):
        """Muda a velocidade do tempo físico (0 = congela) sem salto de posição; `tf` reposiciona."""
        t = self.tf() if tf is None else tf
        self._tf0, self._c0, self._vel = t, self.clk.get_value(), vel

    def cam(self):
        u = float(self.camu.get_value())
        return interp_cam(self.camA, self.camB, u)

    def dolly(self, para, rt=1.6, *anims):
        """Dolly contínuo da câmera atual até `para` (1,6 s); para exatamente no último quadro."""
        self.camA, self.camB = self.cam(), para
        self.camu.set_value(0.0)
        self.play(self.camu.animate.set_value(1.0), *anims, run_time=rt, rate_func=smooth)
        self.camA = self.camB = para
        self.camu.set_value(0.0)

    def disco(self, tf=None):
        return self.mov(self.tf() if tf is None else tf)

    def rastro(self, tf):
        if not self.rastro_on:
            return []
        n = 150
        pts = [self.mov(tf - 0.9 + 0.9 * k / (n - 1)) for k in range(n)]
        return [[round(x, 4), round(y, 4)] for x, y in pts]

    def estado3d(self, _t=0.0):
        tf = self.tf()
        e = dict(cam=self.cam(), fio=self.fio, zp=self.zp(tf), pinos=self.pinos, desf=float(self.desf_tr.get_value()))
        if self.disco_on:
            x, y = self.mov(tf)
            e["disco"] = [x, y]
            e["rastro"] = self.rastro(tf)
        e.update(self.extra3)
        return r4(e)

    def mesa(self):
        f3 = Fundo3D(self, "mesa_furo", self.estado3d)
        f3._fundo3d = True
        self.f3 = f3
        self.add(f3)
        return f3

    def tela(self, xyz):
        return proj(self.cam(), xyz)

    def tela_disco(self, dz=0.0):
        x, y = self.disco()
        return proj(self.cam(), (x, y, 0.010 + dz))

    # canto (linha 2) com símbolos em MathTex
    def canto(self, *pecas):
        velhos = [m for m in (self.h2,) if m is not None]
        if velhos:
            self.play(*[FadeOut(m) for m in velhos], run_time=0.25)
        pcs = [txt(p, 30) if isinstance(p, str) else p for p in pecas]
        novo = linha_base(pcs, 0.14).next_to(self.h1, DOWN, buff=0.14, aligned_edge=LEFT).set_z_index(40)
        self.h2 = novo
        self._pend.append(FadeIn(novo))

    # ── v2 §4.1 OPACIDADE (yt_0023) ──
    def _auditar_v5(self, t, itens, op):
        super()._auditar_v5(t, itens, op)
        runs = getattr(self, "_op_runs", None)
        if runs is None:
            runs = self._op_runs = {}
        vivos = set()
        for m in itens:
            for x in m.get_family():
                if isinstance(x, (Text, SingleStringMathTex)) and 0.05 < op(x) < 0.6 and not getattr(x, "_fantasma", False):
                    k = id(x)
                    vivos.add(k)
                    runs[k] = runs.get(k, 0) + 1
                    if runs[k] == 3:
                        s = getattr(x, "text", None) or getattr(x, "tex_string", "?")
                        print(f"[audit] {t:7.1f}s OPACIDADE BAIXA {s[:40]!r} em {op(x):.2f} por mais de 6 quadros")
        for k in list(runs):
            if k not in vivos:
                del runs[k]

    # ── ÁLGEBRA: registro por linha (lei, voo, GM, escrita) ──
    def alg(self, metodo, linha, n_voos=0, numero=False):
        tex_ = getattr(linha, "tex_string", None) or "?"
        print(f"[alg] {self._aid} {metodo} voos={n_voos} num={int(numero)} | {tex_[:90]}")

    def lei(self, A, ia, voos=None, rt=1.0, metodo=None, numero=False):
        """Linha já posta na Pilha, construída da esquerda para a direita (voos do desenho; o resto escreve na vez)."""
        voos = voos or {}
        self.monta(A, ia, voos, rt=rt)
        self.alg(metodo or ("voo" if voos else "escrita"), A, len(voos), numero)
        return A

    def gm(self, src, dst, *mapas, rt=1.2, numero=False, extra=()):
        self.passo(src, dst, *mapas, rt=rt, extra=extra)
        self.alg("GM", dst, 0, numero)
        return dst

    def resultado(self, m, cor, rt=0.35):
        """Sublinhado fino na cor da grandeza; ele passa a fazer parte da linha (anda e sai com ela na Pilha)."""
        s = sublinha(m, cor)
        self.play(Create(s), run_time=rt)
        self.remove(s)
        m.add(s)
        return s

    def selo_canto(self, tag, corpo, **kw):
        return self.selo(tag, corpo, **kw)


def mov_puxada(cena):
    """Órbita de r0 até cena.tp, puxada de 1,15 s e órbita de r1 depois (θ contínuo)."""
    def f(tf):
        if cena.tp > 1e8:
            return (F.R0 * math.cos(F.W0 * tf), F.R0 * math.sin(F.W0 * tf))
        e = F.puxada(tf - cena.tp)
        th = e["th"] + F.W0 * cena.tp
        return (e["r"] * math.cos(th), e["r"] * math.sin(th))
    return f


def zp_puxada(cena):
    return lambda tf: 0.0 if cena.tp > 1e8 else F.puxada(tf - cena.tp)["zp"]


def Mx(*partes, size=46, cores=None):
    """Linha da CONTA (MathTex de string única, cor por token)."""
    return M(*partes, size=size, cores=cores)


def mostrador(rot, fn, casas, unidade, cor, pos, size=38):
    """Mostrador vivo: rótulo (MathTex na cor) = valor (na cor) unidade (branca), num painel PANEL com borda na cor."""
    def f():
        v = fn()
        g = VGroup(T(rot, size, cor), T("=", size, WHITE_), T(num(v, casas), size, cor), T(unidade, size, WHITE_)).arrange(RIGHT, buff=0.1)
        g[3].align_to(g[2], DOWN)
        g.move_to(pos, aligned_edge=LEFT)
        bx = RoundedRectangle(corner_radius=0.08, width=g.width + 0.3, height=0.62).move_to(g).set_fill(PANEL, 0.88).set_stroke(cor, 1.6)
        bx._fundo = True
        return VGroup(bx, g).set_z_index(30)
    return vivo(f)
