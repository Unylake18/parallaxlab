"""yt_0021 — peças comuns: números de conferência, bastão (Three.js 'bastao') e esfera (Three.js 'esfera') por estado, corpos 2D (disco em
pedaços, haltere, barra fatiada, aro, disco em anéis, placa, carretel, haste), barras de energia, eixo, CM, setas curvas, braço em silhueta e a
base dos lotes (Lote21). Kit copiado do yt_0019 (kit.py, prob.py, prob2.py)."""
from prob2 import *  # noqa: F401,F403

# ── números de conferência (Anexo A; qa21.py confere cada valor da tela contra esta tabela) ─────────────────────────────────
G = 9.8
B_M, B_L, M_CABO, M_GROSSA, L_MEIO = 0.90, 0.84, 0.25, 0.65, 0.42


def I_bastao(piv):
    """I do bastão (duas metades uniformes de 0,42 m) pelo cabo (piv 0) ou pela ponta grossa (piv 1): cada metade pelo seu centro + M d²."""
    d_cabo, d_gr = (0.21, 0.63) if piv == 0 else (0.63, 0.21)
    return M_CABO * (L_MEIO ** 2 / 12 + d_cabo ** 2) + M_GROSSA * (L_MEIO ** 2 / 12 + d_gr ** 2)


NUM = {
    "I_cabo": I_bastao(0), "I_grossa": I_bastao(1), "K_cabo": 0.5 * I_bastao(0) * 100, "K_grossa": 0.5 * I_bastao(1) * 100,
    "k_cabo": math.sqrt(I_bastao(0) / B_M), "k_grossa": math.sqrt(I_bastao(1) / B_M),
    "barra_ponta": B_M * B_L ** 2 / 3, "barra_centro": B_M * B_L ** 2 / 12,
    "E1_v": math.sqrt(2 * 1.0 * G * 1.0 / (1.0 + 1.0)), "E1_w": math.sqrt(2 * G / 2.0) / 0.10, "E1_queda": math.sqrt(2 * G), "E1_aro": math.sqrt(2 * G / 3.0),
    "E2_w": math.sqrt(3 * G / 1.0), "E2_bola": 1.5 * math.sqrt(G * 1.0),
    "E3_Id": 0.5 * 2.0 * 0.3 ** 2, "E3_Ir": 0.5 * 0.5 * 0.15 ** 2 + 0.5 * 0.15 ** 2, "E3_w": math.sqrt(8 * G / (13 * 0.3)),
}
NUM["E3_IO"] = NUM["E3_Id"] - NUM["E3_Ir"]
NUM["E3_Icm"] = NUM["E3_IO"] - 1.5 * 0.05 ** 2


def br(x, n=2):
    """Número com vírgula decimal (padrão brasileiro) para MathTex: 0,282 → '0{,}282'."""
    return f"{x:.{n}f}".replace(".", "{,}")


def nm(s, cor, size=40):
    """Número/unidade como MathTex de uma cor (herda a cor da grandeza)."""
    m = MathTex(s.replace(",", "{,}") if "{,}" not in s else s, font_size=size, color=cor)
    m._partes = [(s, cor)]
    return m


# ── marcas do desenho ──────────────────────────────────────────────────────────────────────────────────────
def eixo_cruz(c, s=0.2, cor=GEO, z=14):
    """Eixo visto de topo (perpendicular à tela): círculo + cruz em GEO."""
    c = np.asarray(c, float)
    g = VGroup(Circle(radius=s * 0.6).move_to(c).set_stroke(cor, 2.6).set_fill(BACKGROUND_COLOR, 0.6),
               Line(c + s * LEFT, c + s * RIGHT).set_stroke(cor, 2.6), Line(c + s * DOWN, c + s * UP).set_stroke(cor, 2.6))
    return g.set_z_index(z)


def cm_pt(c, r=0.1, z=16):
    """Centro de massa: ponto branco simples com contorno GEO (o ⊕ em degradê não entra neste vídeo)."""
    g = VGroup(Dot(np.asarray(c, float), radius=r, color=WHITE_), Circle(radius=r + 0.035).move_to(c).set_stroke(GEO, 2.4))
    g._cm = True
    return g.set_z_index(z)


def seta_curva(c, r, a0, da, cor=VEL, w=6, tip=0.24, z=12, op=1.0):
    """Seta curva (ω): arco de raio r ≥ 0,5 a partir do ângulo a0, varrendo da (rad), com ponta legível."""
    c = np.asarray(c, float)
    arc = Arc(radius=r, start_angle=a0, angle=da, arc_center=c).set_stroke(cor, w, opacity=op)
    a1 = a0 + da
    p = c + r * np.array([math.cos(a1), math.sin(a1), 0])
    tg = np.sign(da) * np.array([-math.sin(a1), math.cos(a1), 0])
    n = np.array([-tg[1], tg[0], 0])
    ponta = Polygon(p + tg * tip, p - tg * tip * 0.2 + n * tip * 0.55, p - tg * tip * 0.2 - n * tip * 0.55).set_stroke(cor, 1, opacity=op).set_fill(cor, op)
    return VGroup(arc, ponta).set_z_index(z)


def barra_E(x, yb, h, larg=0.42, cor=KC, hmax=None, op=0.9, z=10):
    """Barra de energia vertical crescendo da base yb até a altura h (moldura até hmax)."""
    g = VGroup()
    if hmax:
        fr = Rectangle(width=larg + 0.08, height=hmax + 0.08).move_to(P3(x, yb + hmax / 2)).set_stroke(GEO, 1.6, opacity=0.6).set_fill(PANEL, 0.4)
        fr._fundo = True
        g.add(fr)
    if h > 0.004:
        g.add(Rectangle(width=larg, height=h).move_to(P3(x, yb + h / 2)).set_stroke(cor, 2).set_fill(cor, op))
    return g.set_z_index(z)


def braco(mao, ang, comp=2.2, cor="#5E6A80", z=18, op=1.0):
    """Braço em silhueta 2D (antebraço + mão, cápsulas preenchidas), visto de cima: a mão em `mao`, o braço saindo na direção `ang`."""
    mao = np.asarray(mao, float)
    u = np.array([math.cos(ang), math.sin(ang), 0])
    cot = mao + u * comp * 0.55
    omb = mao + u * comp
    g = VGroup(capsula2d(cot, omb, 0.2, cor), capsula2d(mao + u * 0.12, cot, 0.15, cor),
               Circle(radius=0.17).move_to(mao).set_stroke(width=0).set_fill(cor, 1))
    for m in g.family_members_with_points():
        m.set_fill(cor, op).set_stroke(mix(cor, 0.25), 1.2, opacity=op)
    return g.set_z_index(z)


def pedaco(c, r0, r1, a0, da, op, z=6):
    """Pedaço de disco (setor de anel) em rosa: opacidade = massa relativa."""
    s = AnnularSector(inner_radius=r0, outer_radius=r1, start_angle=a0, angle=da, arc_center=np.asarray(c, float))
    return s.set_fill(MAS, op).set_stroke(mix(MAS, 0.2), 1.6, opacity=0.9).set_z_index(z)


def disco_aco(c, R, z=4):
    d = Circle(radius=R).move_to(c)
    aco(d, 2.2)
    return d.set_z_index(z)


class DiscoPedacos(VGroup):
    """Disco uniforme de raio R em nr anéis × nt setores. Cada pedaço guarda massa (∝ área) e o raio quadrático médio (r² = (r0² + r1²)/2),
    então Σ m r² dos pedaços = ½ M R² exatamente (auditoria SOMA)."""

    def __init__(self, c, R, nr=4, nt=10, M=1.0, op0=0.28, op1=0.7):
        super().__init__()
        self.c, self.R, self.M = np.asarray(c, float), R, M
        self.corpo = disco_aco(c, R)
        self.pec, self.dados = VGroup(), []
        A = math.pi * R ** 2
        for i in range(nr):
            r0, r1 = R * i / nr, R * (i + 1) / nr
            area = (r1 ** 2 - r0 ** 2) * math.pi / nt
            for k in range(nt):
                a0 = 2 * math.pi * k / nt
                op = op0 + (op1 - op0) * (area / ((R ** 2 - (R * (nr - 1) / nr) ** 2) * math.pi / nt))
                self.pec.add(pedaco(c, r0, r1, a0, 2 * math.pi / nt, op))
                self.dados.append({"m": M * area / A, "r": math.sqrt((r0 ** 2 + r1 ** 2) / 2), "a": a0 + math.pi / nt, "r0": r0, "r1": r1})
        self.add(self.corpo, self.pec)

    def centro_de(self, k):
        d = self.dados[k]
        return self.c + d["r"] * np.array([math.cos(d["a"]), math.sin(d["a"]), 0])


def haltere(c1, c2, rb=0.34, z=8):
    """Haltere 2D: haste leve fina (GEO) e duas massas (esferas de aço com anel rosa: a massa é rosa)."""
    hs = Line(c1, c2).set_stroke(GEO, 4)
    b1, b2 = esfera_aco(rb, z).move_to(c1), esfera_aco(rb, z).move_to(c2)
    a1 = Circle(radius=rb + 0.04).move_to(c1).set_stroke(MAS, 3.5)
    a2 = Circle(radius=rb + 0.04).move_to(c2).set_stroke(MAS, 3.5)
    g = VGroup(hs, b1, b2, a1, a2).set_z_index(z)
    return g


def barra_fatias(x0, y, Lw, h=0.42, n=20, piv=0.0, z=6, brilho=True):
    """Barra de aço fatiada em n fatias; com `brilho`, cada fatia em rosa com opacidade ∝ x² (x = distância ao eixo em `piv`, fração de L)."""
    g = VGroup()
    corpo = Rectangle(width=Lw, height=h).move_to(P3(x0 + Lw / 2, y))
    aco(corpo, 2.0)
    g.add(corpo.set_z_index(z))
    fat = VGroup()
    xm = max(piv, 1 - piv)
    for k in range(n):
        u = (k + 0.5) / n
        w2 = ((u - piv) / xm) ** 2
        f = Rectangle(width=Lw / n, height=h).move_to(P3(x0 + Lw * u, y))
        f.set_stroke(mix(MAS, 0.3), 1.0, opacity=0.7).set_fill(MAS, (0.08 + 0.85 * w2) if brilho else 0.0)
        fat.add(f.set_z_index(z + 1))
    g.add(fat)
    g.fat = fat
    return g


def aro2d(c, R, w=0.16, z=6):
    a = Annulus(inner_radius=R - w / 2, outer_radius=R + w / 2).move_to(c)
    aco(a, 1.6)
    halo = Circle(radius=R).move_to(c).set_stroke(MAS, 3, opacity=0.9)
    return VGroup(a, halo).set_z_index(z)


def placa_irregular(c, s=1.0, z=5):
    pts = [P3(math.cos(t) * (1.55 + 0.32 * math.sin(3 * t + 0.6) + 0.15 * math.cos(5 * t)) * s, math.sin(t) * (1.15 + 0.22 * math.cos(2 * t + 1.1)) * s)
           for t in np.linspace(0, 2 * PI, 80, endpoint=False)]
    p = VMobject().set_points_smoothly(pts + [pts[0]]).shift(np.asarray(c, float))
    aco(p, 2.0)
    return p.set_z_index(z)


# ── 3D: bastão (câmera de cima, z = 0 é o plano do giro) e esfera fatiada ───────────────────────────────────────
K_B = 3.0                                                     # unidades da tela por metro no plano do bastão


def cam_b(K=K_B, xc=0.0, yc=0.0):
    return cam_topo(K=K, xc=xc, yc=yc, camx=0.0, camy=0.0, fov=16)


def tela_b(x, y, cam=None):
    """Ponto (x, y) em metros no plano do giro → Manim (perspectiva exata da câmera do b3d.js)."""
    return projeta3d(cam or cam_b(), (x, y, 0.07))


def ponta_b(px, py, ang, s):
    """Ponto a distância s (m) do pino, na direção do bastão."""
    return px + s * math.cos(ang), py + s * math.sin(ang)


def cam_e(K=2.0, xc=-3.4, yc=-0.35, az=-62.0, el=20.0):
    return cam_obl(az, el, (0.0, 0.0, 0.0), K=K, xc=xc, yc=yc, fov=16)


class Lote21(Prob2):
    """Base dos lotes do yt_0021: canto de duas linhas, selo único na faixa, CONTA em Pilha (x 0,6…6,7; y −3,25…2,35)."""
    FUNDO = "fundo_lab.png"

    def construct(self):
        self.setup_base()
        self.corpo()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def corpo(self):
        raise NotImplementedError

    def lab(self, s, alvo, lados=(UP, RIGHT, DOWN, LEFT, UR, DR, UL, DL), size=40, cor=None, buffs=(0.14, 0.26, 0.38), ignorar=(), zona=None):
        """Rótulo MathTex (cor por token) posto com teste de colisão a ≤ 0,4 do dono."""
        m = T(s, size, cor)
        r = self.rotulo(m, alvo, lados=lados, buffs=buffs, ignorar=ignorar, zona=zona or (-7.45, 7.45, -4.0, 2.5), chamada=False)
        return r[0]


def _monta(self, A, ia, voos, rt=1.0, arco=-0.5, ate=None):
    """Linha A (já posta na Pilha) construída: as partes em `voos` ({parte: rótulo do desenho}) voam do desenho (TransformFromCopy); o resto
    (operadores, números puros) acende nas vagas depois dos voos."""
    pares = [(src, mp(A, ia, [k])) for k, src in voos.items()]
    resto = [k for k in range(len(ia)) if k not in voos and ia[k] and (ate is None or k <= ate)]       # v5 ORDEM: `ate` corta o que ainda não é da vez
    self.voa(pares, extra=[], rt=rt, origem=False, arco_esq=arco, escrever=[mp(A, ia, [k]) for k in resto])      # v5 ORDEM: cada parte fixa na sua vez por x
    self.foco = A


Lote21.monta = _monta


def _guia(self, linhas, cor=None):
    """v6 G4: cartão de PERGUNTA/ENUNCIADO que ocupa a coluna da direita desde o começo da âncora (a equação de partida ainda não chegou)."""
    tag = txt(linhas[0], 24, bold=True, color=CYAN)
    g = VGroup(tag, *[txt(l, 26, color=cor) if cor else txt(l, 26) for l in linhas[1:]]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    self.pilha.poe(g)
    self.play(FadeIn(g, shift=0.08 * DOWN), run_time=0.5)
    self.foco = g
    return g


Lote21.guia = _guia


import kit as _kit  # noqa: E402


def gidx(m, idx, simbolo, k=0):
    """Índice (em m[0]) do glifo de `idx` que a forma reconhece como `simbolo` com tamanho óptico k (0 principal, 1 índice, 2 expoente)."""
    for j in idx:
        r = _kit._id_glifo(m[0][j])
        if r is not None and r == (simbolo, k):
            return j
    return idx[0]
