"""yt_0020 — peças comuns: disco de referência 2D (T1–T4), arcos e setas curvas, gráfico ω(t), estados 3D (hélice, disco, livros, Terra),
ventilador, transmissão da bicicleta, relógio e os números de conferência (Anexo A).

Física congelada (handoff §Física): corpo rígido em eixo fixo = um θ(t); ω, α do corpo; v_t = rω, a_t = rα, a_c = ω²r de cada ponto; positivo anti-horário.
"""
from prob2 import *  # noqa: F401,F403

N_ = lambda s: s.replace(".", "{.}").replace(",", "{,}")
GEO_ = GEO
DC, DR = P3(-3.75, -0.45), 2.6          # disco de referência: centro e raio (unidades de cena)
K_HEL, C_HEL = 2.3, P3(-3.75, -0.25)   # hélice: escala (cena por metro) e centro na tela


# ── números de conferência (Anexo A, conferidos em qa20.py) ────────────────────────────────────────────────
def numeros():
    w_hel = 2700 * 2 * PI / 60
    n = dict(w_hel=w_hel, v10=0.10 * w_hel, v95=0.95 * w_hel, kmh10=0.10 * w_hel * 3.6, kmh95=0.95 * w_hel * 3.6, som=0.95 * w_hel / 343,
             ac95=w_hel ** 2 * 0.95, g95=w_hel ** 2 * 0.95 / 9.8,
             w0=10 * PI, al=-PI / 3, dth=150 * PI, voltas=75.0, dth10=10 * PI * 10 - 0.5 * PI / 3 * 100, v0=0.6 * 10 * PI, ac0=(10 * PI) ** 2 * 0.6,
             at=0.6 * PI / 3, w10=10 * PI - PI / 3 * 10, ac10=(10 * PI - PI / 3 * 10) ** 2 * 0.6, wcruz=math.sqrt(PI / 3),
             w2=5 * PI, vb=5 * PI * 0.35, al1=PI / 4, al2=2.5 * PI / 4, ab=2.5 * PI / 4 * 0.35, vc=2 * PI * 0.10, acc1=(2 * PI * 0.10) ** 2 / 0.10,
             acc2=(2 * PI * 0.10) ** 2 / 0.04, Tsid=86400 / (1 + 1 / 365.2422), R_T=6371.0, lat=23.55)
    n["tcruz"] = (n["w0"] - n["wcruz"]) / (PI / 3)
    n["phi10"] = math.degrees(math.atan(n["at"] / n["ac10"]))
    n["wT"] = 2 * PI / n["Tsid"]
    n["rp"] = 6371 * math.cos(math.radians(23.55))
    n["veq"] = n["wT"] * 6371e3
    n["vsp"] = n["wT"] * n["rp"] * 1e3
    n["acsp"] = n["wT"] ** 2 * n["rp"] * 1e3
    return n


NUM = numeros()


# ── desenho: disco de aço, arcos, setas curvas ─────────────────────────────────────────────────────────────
def disco_aco(R, z=2):
    """Disco 2D de aço com a luz B (gradiente radial suave, centro claro deslocado para o alto à esquerda; recorte #7FB2FF a 35% embaixo à esquerda;
    toque #EA63FF a 12% em cima à direita), anéis finos de usinagem e o eixo no centro."""
    g = VGroup()
    c0, c1, c2 = ManimColor("#222935"), ManimColor("#343D4D"), ManimColor("#4A5568")
    n = 14
    for k in range(n):
        u = k / (n - 1)
        cc = interpolate_color(c0, c1, u / 0.45) if u < 0.45 else interpolate_color(c1, c2, (u - 0.45) / 0.55)
        g.add(Circle(radius=R * (1 - 0.55 * u)).set_stroke(width=0).set_fill(cc, 1).move_to(P3(-0.14 * R * u, 0.15 * R * u)))
    for rr in (0.93, 0.62, 0.3):
        g.add(Circle(radius=R * rr).set_stroke(WHITE_, 1, opacity=0.08))
    wr = max(2.0, 4 * R)
    g.add(Arc(radius=R - 0.004 * wr, start_angle=1.05 * PI, angle=0.62 * PI).set_stroke("#7FB2FF", wr, opacity=0.35))
    g.add(Arc(radius=R - 0.004 * wr, start_angle=0.08 * PI, angle=0.36 * PI).set_stroke(MAG, wr * 0.8, opacity=0.12))
    g.add(Circle(radius=R).set_stroke("#5A6476", 1.6, opacity=0.9))
    for m in g:
        m._degrade = "aco"
    return g.set_z_index(z)


def eixo_mob(c, r=0.11):
    return VGroup(Circle(radius=r).set_stroke(GEO, 2.5).set_fill("#1A2234", 1).move_to(c),
                  Line(c + r * 0.7 * LEFT, c + r * 0.7 * RIGHT).set_stroke(GEO, 2), Line(c + r * 0.7 * DOWN, c + r * 0.7 * UP).set_stroke(GEO, 2)).set_z_index(9)


def arco(c, r, a0, a1, cor=ANG, w=5, op=1.0, z=7):
    if abs(a1 - a0) < 1e-4:
        return VMobject()
    return Arc(radius=r, start_angle=a0, angle=a1 - a0, arc_center=np.asarray(c, float), num_components=max(8, int(abs(a1 - a0) * 12))).set_stroke(cor, w, opacity=op).set_z_index(z)


def seta_curva(c, r, a0, da, cor=VEL, w=6, tip=0.24, op=1.0, z=9):
    """Seta curva (G8: raio ≥ 0,5, ponta legível) de a0 varrendo da (rad, com sinal) em volta de c."""
    c = np.asarray(c, float)
    s = 1 if da >= 0 else -1
    dtip = s * min(abs(da) * 0.45, tip / max(r, 0.3))
    a_end = a0 + da
    corpo = arco(c, r, a0, a_end - dtip, cor, w, op, z)
    b = c + r * P3(math.cos(a_end), math.sin(a_end))
    t = s * P3(-math.sin(a_end - dtip / 2), math.cos(a_end - dtip / 2))
    n = P3(-t[1], t[0])
    base = b - t * tip
    ponta = Polygon(b, base + n * tip * 0.55, base - n * tip * 0.55).set_stroke(cor, 1, opacity=op).set_fill(cor, op).set_z_index(z)
    return VGroup(corpo, ponta)


def ponto_mob(p, r=0.085, z=10):
    return VGroup(Circle(radius=r).set_fill(WHITE_, 1).set_stroke("#2A3550", 2.2).move_to(p)).set_z_index(z)


def tracej(a, b, cor=GEO, w=2.5, op=0.8, dash=0.12, z=4):
    return DashedLine(np.asarray(a, float), np.asarray(b, float), dash_length=dash, dashed_ratio=0.55).set_stroke(cor, w, opacity=op).set_z_index(z)


class DiscoRef:
    """Disco de referência (T1–T4): eixo fixo no centro, LINHA PINTADA branca do centro à borda, três pontos a 1/3, 2/3, 3/3 do raio sobre ela,
    linha fixa de referência tracejada (GEO, horizontal para a direita). Um único ValueTracker θ(t) gira tudo; anti-horário positivo."""

    def __init__(self, cena, C=DC, R=DR, th0=0.0, reg=True):
        self.cena, self.C, self.R = cena, np.asarray(C, float), R
        self.th = ValueTracker(th0)
        self.corpo = disco_aco(R).move_to(self.C)
        self.ref = tracej(self.C, self.C + (R + 0.55) * RIGHT, GEO, 2.5, 0.85, z=3)
        self.eixo = eixo_mob(self.C)
        self._reg = reg
        self.vivo = vivo(self._desenho)
        self.g = VGroup(self.corpo, self.ref, self.vivo, self.eixo)
        cena.add(self.th)

    def p(self, k, th=None):
        th = self.th.get_value() if th is None else th
        return self.C + self.R * k / 3 * P3(math.cos(th), math.sin(th))

    def u(self, th=None):
        th = self.th.get_value() if th is None else th
        return P3(math.cos(th), math.sin(th)), P3(-math.sin(th), math.cos(th))

    def _desenho(self):
        th = self.th.get_value()
        ln = Line(self.C, self.p(3, th)).set_stroke(WHITE_, 6).set_z_index(6)
        pts = VGroup(*[ponto_mob(self.p(k, th)) for k in (1, 2, 3)])
        if self._reg and not PEDIDOS3D:
            self.cena.reg("rigido", th=th, c=self.C, p1=self.p(1, th), p2=self.p(2, th), p3=self.p(3, th))
        return VGroup(ln, pts).set_z_index(6)


# ── câmeras e estados 3D ────────────────────────────────────────────────────────────────────────────────────
def cam_hel(K=K_HEL, c=C_HEL):
    return {"modo": "frente", "K": K, "xc": float(c[0]), "yc": float(c[1]), "camx": 0.0, "fov": 16, "el": 0}


def hel_pt(cam, r, ang, y=-0.07):
    return projeta3d(cam, (r * math.cos(ang), y, r * math.sin(ang)))


def cam_disco(el=89.999, az=-90.0, K=DR, c=DC):
    return {"modo": "obl", "az": az, "el": el, "alvo": [0.0, 0.0, 0.0], "K": K, "xc": float(c[0]), "yc": float(c[1]), "fov": 16}


class Relogio:
    """Contador de tempo de tela da âncora (para simulações comprimidas): t_sim(t_tela)."""

    def __init__(self, fator):
        self.f = fator


def selo_mini(s, cor=WHITE_, borda=BLUE_L, size=24):
    """Selo pequeno preso a um desenho (CÂMERA LENTA ×90, FORA DE ESCALA, EXAGERADO): PANEL com borda."""
    t = txt(s, size, color=cor, bold=True)
    bx = RoundedRectangle(corner_radius=0.08, width=t.width + 0.26, height=t.height + 0.18).move_to(t).set_fill(PANEL, 0.9).set_stroke(borda, 1.6)
    bx._fundo = bx._caixa = True
    return VGroup(bx, t).set_z_index(30)


def nota(s, size=24, cor=WHITE_):
    return txt(s, size, color=cor)


def lbl(tex, cor, size=40):
    """Rótulo MathTex de uma cor só (G12): registra a parte para a auditoria de cor."""
    m = MathTex(tex, font_size=size, color=cor)
    m._partes = [(tex, cor)]
    barras_neutras(m)                                         # v4 §3: barra de fração branca
    return m.set_z_index(12)


def valor(tex, cor, size=36):
    """Número com unidade (rot com Space Grotesk ficaria fora da cor por token): MathTex de uma cor."""
    return lbl(tex, cor, size)


_GL = {}
_GNUM = [0]


def num_mob(s, cor=WHITE_, size=40):
    """Número que muda a cada quadro (contadores, mostrador): glifos MathTex guardados um a um e alinhados pela base (sem compilar LaTeX por quadro).
    Aceita dígitos, ',', '.', '−', '°', 'π' e espaço."""
    tex_ = {",": "{,}", ".": "{.}", "−": "-", "°": r"^\circ", "π": r"\pi", " ": None}
    g = VGroup()
    for ch in s:
        t = tex_.get(ch, ch)
        if t is None:
            g.add(VectorizedPoint())
            continue
        k = (t, cor, size)
        if k not in _GL:
            m = MathTex(t, font_size=size, color=cor)
            m._partes = [(t, cor)]
            _GL[k] = m
        c_ = _GL[k].copy()
        for sub in [c_] + c_.family_members_with_points() + list(c_.submobjects):
            sub._gnum = _GNUM[0]
        g.add(c_)
    _GNUM[0] += 1
    g.arrange(RIGHT, buff=0.02 * size / 40, aligned_edge=DOWN)
    for m, ch in zip(g, s):
        if ch == "°":
            m.shift(0.16 * size / 40 * UP)
        if ch in ",.":
            m.shift(0.05 * size / 40 * DOWN)
    return g.set_z_index(12)


# ── ventilador de teto visto de baixo (E1) ──────────────────────────────────────────────────────────────────
def ventilador(c, R, ang, n=3):
    """Três pás de aço (luz B) e o cubo; ponta da pá 0 em c + R(cos ang, sin ang)."""
    g = VGroup()
    for k in range(n):
        a = ang + 2 * PI * k / n
        u, t = P3(math.cos(a), math.sin(a)), P3(-math.sin(a), math.cos(a))
        r0 = 0.22 * R
        w0, w1 = 0.16 * R, 0.21 * R
        pts = [c + u * r0 - t * w0 / 2, c + u * (R - 0.08 * R) - t * w1 / 2, c + u * R - t * w1 * 0.25, c + u * R + t * w1 * 0.25,
               c + u * (R - 0.08 * R) + t * w1 / 2, c + u * r0 + t * w0 / 2]
        g.add(aco(Polygon(*pts), 1.6))
    g.add(aco(Circle(radius=0.26 * R).move_to(c), 2.0), Circle(radius=0.1 * R).set_fill("#1A2234", 1).set_stroke(GEO, 2).move_to(c))
    return g.set_z_index(5)


# ── transmissão da bicicleta (E2) ───────────────────────────────────────────────────────────────────────────
def engrenagem(c, r, ang, dentes, z=5):
    """Engrenagem de aço com dentes (polígono) girada de `ang`."""
    pts = []
    n = dentes
    for i in range(2 * n):
        a = ang + PI * i / n
        rr = r + (0.055 if i % 2 == 0 else -0.03)
        pts.append(c + rr * P3(math.cos(a), math.sin(a)))
    g = VGroup(aco(Polygon(*pts), 1.4), Circle(radius=0.55 * r).set_fill("#1A2234", 0.9).set_stroke(GEO, 1.5).move_to(c),
               Circle(radius=0.12).set_fill(STEEL, 1).set_stroke(GEO, 2).move_to(c))
    for k in range(5 if r > 0.5 else 3):
        a = ang + 2 * PI * k / (5 if r > 0.5 else 3)
        g.add(Line(c + 0.15 * P3(math.cos(a), math.sin(a)), c + 0.53 * r * P3(math.cos(a), math.sin(a))).set_stroke(STEEL, 5))
    return g.set_z_index(z)


class L20(Prob2):
    """Base dos lotes do yt_0020: o céu do laboratório em todas as cenas (handoff §2.2) e o tempo até um gatilho de fala."""
    FUNDO = "fundo_lab.png"

    def ate_t(self, frase, minimo=0.6):
        """Segundos daqui até o gatilho `frase` da âncora corrente (para um movimento que termina na palavra)."""
        k = self._k_frase(self._aid, frase)
        if k is None:
            print(f"[gatilho-sem-frase] {self._aid}: {frase!r}")
            return minimo
        tw = ANC[self._aid]["t"]
        return max(minimo, tw[k] - LEAD - (self.nq - self._q0) / FPS)

    # ── marcador de canto (handoff v2 §3): CÂMERA LENTA / FORA DE ESCALA / EXAGERADO ──
    def marcador_mob(self, texto, lado="dir", y=-3.32):
        """Marcador pequeno fixo no canto inferior do ESQUEMA (nunca na faixa de selos nem sobre setas): lado 'dir' encosta em x ≈ 0,0; 'esq' em x ≈ −7,2."""
        m = selo_mini(texto)
        x = (-0.05 - m.width / 2) if lado == "dir" else (-7.2 + m.width / 2)
        return m.move_to(P3(x, y))

    def troca_marcador(self, texto=None, lado="dir", y=-3.32):
        """Um marcador por vez: devolve as animações [FadeOut(velho), FadeIn(novo)] para entrar no mesmo play. texto=None só tira o atual."""
        novo = self.marcador_mob(texto, lado, y) if texto else None
        anims = []
        velho = getattr(self, "_marc", None)
        if velho is not None:
            anims.append(FadeOut(velho))
        if novo is not None:
            anims.append(FadeIn(novo))
        self._marc = novo
        return anims
