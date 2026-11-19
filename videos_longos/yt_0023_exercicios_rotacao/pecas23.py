"""yt_0023 — peças comuns: números (Anexo A), física integrada (volante, freio, carretel, haste, pêndulo), câmeras 3D ('carretel',
'volante', 'regua'), peças 2D (haste, pêndulo de disco, curva T(l), barras de energia, ícones) e a base dos lotes (Lote23) com a trilha de itens."""
from pecas22 import *  # noqa: F401,F403

# ── números (fonte: tabela "Conferência numérica" do Anexo A) ────────────────────────────────────────────────
G = 9.8
# E1 volante
I_ANEL = 15 * (0.3 ** 2 + 0.4 ** 2) / 2          # 1,875
I_CUBO = 3 * 0.1 ** 2 / 2                        # 0,015
I_DISCO = 0.05 ** 2 / 2 + 0.25 ** 2              # 0,06375
I_VOL = I_ANEL + I_CUBO + 2 * I_DISCO            # 2,0175
R_TB = 0.15
M_BL = 10.0
A_VOL = G / (1 + I_VOL / (M_BL * R_TB ** 2))     # 0,9833
AL_VOL = A_VOL / R_TB                            # 6,555
T_VOL = M_BL * (G - A_VOL)                       # 88,17
W15 = AL_VOL * 1.5                               # 9,833
K_VOL = I_VOL * W15 ** 2 / 2                     # 97,53
AL_FREIO = 4.0 / I_VOL                           # 1,983
T_PARA = W15 / AL_FREIO                          # 4,96
I_ARO = 20 * 0.4 ** 2                            # 3,2
A_ARO = G / (1 + I_ARO / (M_BL * R_TB ** 2))     # 0,644
AL_ARO = A_ARO / R_TB
# E3 carretel
I_C, RC, rc, M1, M2 = 0.50, 0.30, 0.10, 6.0, 10.0
AL_C = (M1 * RC - M2 * rc) * G / (I_C + M1 * RC ** 2 + M2 * rc ** 2)   # 6,877
T_1M = math.sqrt(2 * 1.0 / (AL_C * RC))                                 # 0,985 s

assert abs(I_VOL - 2.0175) < 1e-9 and abs(A_VOL - 0.9833) < 1e-3 and abs(AL_C - 6.877) < 1e-3 and abs(T_PARA - 4.96) < 0.01


def vol_th(t):
    t = clamp(t, 0, 1.5)
    return AL_VOL * t * t / 2


def freio_th(t):
    """Ângulo girado desde o início da frenagem (t s); para em T_PARA."""
    t = clamp(t, 0, T_PARA)
    return W15 * t - AL_FREIO * t * t / 2


def car_th(t):
    t = max(0.0, t)
    return AL_C * t * t / 2


def periodo(l, duplo=False, R=0.1):
    """Período (s) do pêndulo de disco: um disco (l_eq = l + R²/2l) ou dois discos (l_eq = (R² + l²)/l)."""
    leq = (R * R + l * l) / l if duplo else l + R * R / (2 * l)
    return 2 * math.pi * math.sqrt(leq / G)


def integra_haste(dt=1e-4):
    """θ̈ = (12/7)(g/d) cos θ, d = 1,0 m, do repouso na horizontal até a vertical (RK4)."""
    f = 12 / 7 * G
    ts, th, om = [0.0], [0.0], [0.0]
    while th[-1] < math.pi / 2:
        a, w = th[-1], om[-1]
        k1 = (w, f * math.cos(a))
        k2 = (w + dt * k1[1] / 2, f * math.cos(a + dt * k1[0] / 2))
        k3 = (w + dt * k2[1] / 2, f * math.cos(a + dt * k2[0] / 2))
        k4 = (w + dt * k3[1], f * math.cos(a + dt * k3[0]))
        th.append(a + dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6)
        om.append(w + dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6)
        ts.append(ts[-1] + dt)
    return np.array(ts), np.array(th), np.array(om)


HASTE = integra_haste()
T_HASTE = float(HASTE[0][-1])                    # tempo até a vertical (d = 1,0 m)


def haste_th(t):
    return float(np.interp(clamp(t, 0, T_HASTE), HASTE[0], HASTE[1]))


def haste_t_de(th):
    return float(np.interp(th, HASTE[1], HASTE[0]))


def forca_eixo(th):
    """Força do eixo na haste (em unidades de Mg) e acelerações do ⊕ (em g), θ abaixo da horizontal, eixo à esquerda do ⊕.
    Haste ao longo de u = (cos θ, −sen θ); F_r para o eixo (−u); F_⊥ ao longo de n = (sen θ, cos θ) (para cima, contra a queda)."""
    s, c = math.sin(th), math.cos(th)
    fr, fp = 13 / 7 * s, 4 / 7 * c
    u, n = np.array([c, -s, 0.0]), np.array([s, c, 0.0])
    F = -fr * u + fp * n
    return dict(fr=fr, fp=fp, F=F, mod=float(np.linalg.norm(F)), at=3 / 7 * c, ac=6 / 7 * s, u=u, n=n)


# confere com o Anexo A: 4/7 em 0, (−9/14, 17/14) e 1,374 em 45°, 13/7 em 90°
_f45 = forca_eixo(math.pi / 4)
assert abs(_f45["F"][0] + 9 / 14) < 1e-9 and abs(_f45["F"][1] - 17 / 14) < 1e-9 and abs(_f45["mod"] - 1.374) < 1e-3


# ── câmeras ─────────────────────────────────────────────────────────────────────────────────────────────────────
FOV3 = 9.0


def cam_car(u, K=5.2, xc=-3.85, yc=0.8, alvo_z=0.0):
    """Carretel: u = 0 → 3/4 (az −56°, el 14°), u = 1 → frontal pura (eixo apontando para a câmera)."""
    s = smooth(clamp(u, 0, 1))
    if s >= 0.9999:
        return cam_obl(-90.0, 0.0, [0.0, 0.0, alvo_z], K=K, xc=xc, yc=yc, fov=FOV3)
    return cam_obl(-56.0 - 34.0 * s, 14.0 * (1 - s), [0.0, 0.0, alvo_z], K=K, xc=xc, yc=yc, fov=FOV3)


def cam_vol(u, K=3.7, xc=-3.85, yc=1.1, alvo_x=0.0, alvo_z=0.0):
    """Volante: u = 0 → 3/4 (az −60°, el 15°), u = 1 → frontal pura."""
    s = smooth(clamp(u, 0, 1))
    if s >= 0.9999:
        return cam_obl(-90.0, 0.0, [alvo_x, 0.0, alvo_z], K=K, xc=xc, yc=yc, fov=FOV3)
    return cam_obl(-60.0 - 30.0 * s, 15.0 * (1 - s), [alvo_x, 0.0, alvo_z], K=K, xc=xc, yc=yc, fov=FOV3)


def cam_reg():
    return cam_regua_frente(K=6.2, xc=-4.15, yc=0.55, camx=0.42, camz=-0.06, el=12.0)


def pr(cam, p):
    return projeta3d(cam, p)


# ── peças 2D ───────────────────────────────────────────────────────────────────────────────────────────────────
def lbl(s, cor=None, size=40):
    """Rótulo MathTex de uma cor (número herda a cor da grandeza)."""
    return T(s, size, cor)


def bloco2d(c, lado, rotulo=None, z=8):
    q = Square(lado).move_to(c).set_fill(escuro(MAS, 0.55), 1).set_stroke(MAS, 2.6)
    return VGroup(q).set_z_index(z)


def disco2d(c, R, z=4, cor=STEEL):
    return VGroup(Circle(radius=R).move_to(c).set_fill(cor, 1).set_stroke(GEO, 2.2),
                  Circle(radius=R * 0.93).move_to(c).set_stroke(mix(cor, 0.35), 1.2, opacity=0.6)).set_z_index(z)


def haste2d(o, th, comp=4.4, esp=0.2, z=6):
    """Haste de aço com o eixo em `o`, a d/4 da ponta esquerda; θ = ângulo de queda (abaixo da horizontal)."""
    u = np.array([math.cos(th), -math.sin(th), 0.0])
    n = np.array([math.sin(th), math.cos(th), 0.0])
    a, b = o - comp / 4 * u, o + 3 * comp / 4 * u
    corpo = Polygon(a + n * esp / 2, b + n * esp / 2, b - n * esp / 2, a - n * esp / 2).set_fill(STEEL, 1).set_stroke(GEO, 2.0)
    brilho = Line(a + n * esp * 0.3, b + n * esp * 0.3).set_stroke(mix(STEEL, 0.5), 1.4, opacity=0.7)
    return VGroup(corpo, brilho).set_z_index(z)


def pino(c, r=0.13, z=14):
    return VGroup(Circle(radius=r).move_to(c).set_fill(BACKGROUND_COLOR, 1).set_stroke(WHITE_, 3.0),
                  Dot(c, radius=0.035, color=WHITE_)).set_z_index(z)


def cruz_cm(c, r=0.11, z=16):
    """⊕ branco simples (sem degradê)."""
    c = np.asarray(c, float)
    return VGroup(Circle(radius=r).move_to(c).set_stroke(WHITE_, 2.4).set_fill(BACKGROUND_COLOR, 0.6),
                  Line(c + r * LEFT, c + r * RIGHT).set_stroke(WHITE_, 2.0), Line(c + r * DOWN, c + r * UP).set_stroke(WHITE_, 2.0)).set_z_index(z)


def barra_h(x0, y, w, frac, cor, h=0.26, z=10, op=0.95):
    """Barra horizontal de energia: moldura GEO de largura w e preenchimento frac·w (cresce da esquerda)."""
    mold = Rectangle(width=w, height=h).move_to(P3(x0 + w / 2, y)).set_stroke(GEO, 1.6).set_fill(PANEL, 0.6)
    n = max(0.002, clamp(frac, 0, 1.2) * w)
    ench = Rectangle(width=n, height=h - 0.04).move_to(P3(x0 + n / 2, y)).set_stroke(width=0).set_fill(cor, op)
    return VGroup(mold, ench).set_z_index(z)


def seta_s(a, b, cor, w=6, tip=0.2, z=12, op=1.0):
    """Seta reta com o mínimo do G8 (espessura ≥ 5)."""
    g = seta(np.asarray(a, float), np.asarray(b, float), cor, max(5, w), tip=tip, op=op, z=z)
    g._ini, g._fim = np.asarray(a, float), np.asarray(b, float)
    return g


def risco(m, cor=MAS, w=4):
    r = Line(m.get_corner(DL) + 0.05 * DL, m.get_corner(UR) + 0.05 * UR).set_stroke(cor, w)
    r._risco = True
    return r.set_z_index(30)


# ── v3 §3: cotas e rótulos legíveis sobre aço (halo escuro + linha clara + pílula com texto clareado) ──────────────
HALO = "#050B18"
LINHA_CL = "#E6ECF7"
GEO_CL = "#DCE4F2"


C_RAIO = "#C8FF2E"          # v4 §1: lima = raio/distância MAIOR (R, R₂, d, l, D, h…)
C_RAIO_MENOR = "#E040FB"    # magenta-neon = raio MENOR quando há dois no mesmo corpo (r do carretel, R₁ do volante)
AÇO_FRIO = "#33456B"        # peças de aço escuras e frias para o lima/magenta saltarem
AÇO_ARESTA = "#8FA6C9"
AÇO_CLARO = "#C9D8EE"


def circ_raio(c, R, cor, w=4.0, z=14, tracejado=True, n=44):
    """Círculo de cota (v4 §1.2 #2): contorno de ~4 px na cor do raio sobre halo escuro; tracejado quando for o raio menor."""
    base = Circle(radius=R).move_to(c)
    h = base.copy().set_stroke(HALO, w + 21).set_z_index(z - 0.2)                 # v5 CONTRASTE: halo escuro contínuo (mesmo no tracejado), ~6 px por lado a 960×540
    l = (DashedVMobject(base.copy(), num_dashes=n, dashed_ratio=0.62) if tracejado else base.copy()).set_stroke(cor, w).set_z_index(z)
    return VGroup(h, l)


def _pts3d(proj, R, y, n=72, c=(0.0, 0.0)):
    return [proj((c[0] + R * math.cos(2 * PI * k / n), y, c[1] + R * math.sin(2 * PI * k / n))) for k in range(n)]


def circ3d(proj, R, y, cor, w=4.0, tracejado=False, z=14, c=(0.0, 0.0)):
    """Círculo de raio R no plano x–z (eixo y) projetado pela câmera atual `proj` (vira elipse nas vistas oblíquas), sobre halo escuro."""
    pts = _pts3d(proj, R, y, c=c)
    base = VMobject().set_points_as_corners(pts + [pts[0]])
    mk = lambda: (DashedVMobject(base.copy(), num_dashes=40, dashed_ratio=0.6) if tracejado else base.copy())
    return VGroup(base.copy().set_stroke(HALO, w + 21).set_z_index(z - 0.2), mk().set_stroke(cor, w).set_z_index(z))


def anel_tinta3d(proj, R1, R2, y, cor, op=0.18, z=13):
    """Faixa entre R1 e R2 (v4 §1.2 #2): tinte de 15–20% na cor do raio maior."""
    a, b = _pts3d(proj, R2, y), _pts3d(proj, R1, y)
    m = VMobject().set_points_as_corners(a + [a[0]] + b[::-1] + [b[-1]])
    return m.set_fill(cor, op).set_stroke(width=0).set_z_index(z)


def volante25(o, s, ang=0.0, heat=0.0, aro=False):
    """v5 §1.1: volante 2.5D frontal. Anel azul-aço escuro (R1 = 0,30 m, R2 = 0,40 m) com aro claro; cubo, quatro raios e dois discos pequenos
    (0,05 m a ±0,25 m; giram junto com o volante) em cinza-azulado; marca de giro no anel. `s` = unidades de tela por metro. `heat` (0–1) esquenta o
    anel; `aro` desenha só o aro fino (E1-17)."""
    o = np.asarray(o, float)
    R2, R1 = 0.40 * s, (0.385 * s if aro else 0.30 * s)
    quente = "#C4452A"
    fc = interpolate_color(ManimColor("#3E564D"), ManimColor(quente), 0.8 * heat)          # v6 §3: um só volante — anel verde-escuro em todas as cenas
    ac = interpolate_color(ManimColor("#86A898"), ManimColor("#FFB38A"), 0.8 * heat)
    g = VGroup()
    g.add(Annulus(inner_radius=R1, outer_radius=R2).move_to(o).set_fill(fc, 1).set_stroke(ac, 3.0))
    g.add(Circle(radius=R2 * 0.97).move_to(o).set_stroke(ac, 1.4, opacity=0.4))
    for k in range(4):
        a = ang + k * PI / 2 + PI / 4
        u = np.array([math.cos(a), math.sin(a), 0.0])
        if aro:
            g.add(Line(o + 0.1 * s * u, o + R1 * u).set_stroke("#1E2A44", 7), Line(o + 0.1 * s * u, o + R1 * u).set_stroke("#5B6B8C", 4))
        else:
            g.add(Line(o + 0.1 * s * u, o + R1 * u).set_stroke("#1E2A44", 12), Line(o + 0.1 * s * u, o + R1 * u).set_stroke("#5B6B8C", 8))
    a = ang + 0.9
    u = np.array([math.cos(a), math.sin(a), 0.0])
    g.add(Line(o + (R1 + 0.0 * s) * u, o + (R2 - 0.0 * s) * u).set_stroke(AÇO_CLARO, 3.0, opacity=0.9) if aro else Line(o + (R1 + 0.02 * s) * u, o + (R2 - 0.02 * s) * u).set_stroke(AÇO_CLARO, 3.0, opacity=0.8))
    if not aro:
        for sg in (1, -1):
            c = o + sg * 0.25 * s * np.array([math.cos(ang), math.sin(ang), 0.0])
            g.add(Circle(radius=0.05 * s).move_to(c).set_fill(AÇO_CLARO, 1).set_stroke("#1E2A44", 2.5), Dot(c, radius=0.012 * s, color="#1E2A44"))
    g.add(Circle(radius=0.10 * s).move_to(o).set_fill("#5B6B8C", 1).set_stroke(AÇO_CLARO, 2.5), Circle(radius=0.04 * s).move_to(o).set_fill(AÇO_CLARO, 1).set_stroke(width=0), Dot(o, radius=0.012 * s, color=GEO_CL))
    return g.set_z_index(4)


BLOCO_L = 0.62            # lado do bloco de 10 kg em unidades de tela (fixo; o "fantasma" de 90 kg compara com este)
Y_FUNDO = -3.15           # abaixo disto o bloco sai de cena (fica por cima da trilha)


def rig25(o, S, th, cai=0.0, cord=True, freio=False, heat=0.0, aro=False, bloco=True, tambor=True):
    """v5 §1.1: esquema 2.5D vivo do volante (eixo em `o`, `S` u/m): volante, tambor leve (r = 0,15 m, contorno lima), fio e bloco rosa (que desce
    0,15·θ + cai) e a pastilha do freio. Redesenhado por quadro a partir de θ, cai e calor."""
    o = np.asarray(o, float)
    g = VGroup(volante25(o, S, -th, heat=heat, aro=aro))
    if tambor:
        g.add(Circle(radius=0.15 * S).move_to(o).set_fill(AÇO_CLARO, 0.22).set_stroke("#9DB2D6", 2.6).set_z_index(4.6))          # v6: neutro (o lima só aparece quando o raio é falado)
        g.add(Dot(o, radius=0.012 * S, color=GEO_CL).set_z_index(4.7))
    xt = o[0] + 0.158 * S
    yb = o[1] + S * (ZB - 0.15 * th - cai)
    if bloco and cord and yb - BLOCO_L / 2 <= Y_FUNDO - 0.4:                 # o bloco saiu de quadro: o fio segue só até acima da trilha (v7: não cruza os nomes nem sai do quadro)
        g.add(Line([xt, o[1], 0], [xt, -3.38, 0]).set_stroke(HALO, 6).set_z_index(4.8), Line([xt, o[1], 0], [xt, -3.38, 0]).set_stroke("#D8E2F5", 2.6).set_z_index(4.9))
    if bloco and yb - BLOCO_L / 2 > Y_FUNDO - 0.4:
        op = clamp((yb - Y_FUNDO + 0.4) / 0.8, 0.0, 1.0)
        if cord:
            g.add(Line([xt, o[1], 0], [xt, yb + BLOCO_L / 2, 0]).set_stroke(HALO, 6, opacity=op).set_z_index(4.8))
            g.add(Line([xt, o[1], 0], [xt, yb + BLOCO_L / 2, 0]).set_stroke("#D8E2F5", 2.6, opacity=op).set_z_index(4.9))
        g.add(RoundedRectangle(corner_radius=0.07, width=BLOCO_L, height=BLOCO_L).move_to([xt, yb, 0]).set_fill(MAS, 0.88 * op).set_stroke("#FFD0E5", 2.6, opacity=op).set_z_index(5))
    if freio:
        h = 0.07 * S
        pc = interpolate_color(ManimColor("#4A4F66"), ManimColor(HEAT), heat)
        g.add(RoundedRectangle(corner_radius=0.05, width=0.22 * S, height=h).move_to(o + (0.40 * S + h / 2) * UP).set_fill(pc, 1).set_stroke(AÇO_ARESTA, 2.4).set_z_index(5))
        g.add(Line(o + (0.40 * S + h) * UP, o + (0.40 * S + h + 0.12 * S) * UP).set_stroke("#8FA6C9", 5).set_z_index(5))
    return g.set_z_index(4)


def carretel25(o, Rg, Rp, ang, destaque=None):
    """v4 §2.2: carretel 2.5D frontal. Tambor GRANDE azul-aço escuro com flange; tambor PEQUENO claro com sombra projetada (está na frente);
    cubo/eixo; espiras concêntricas; marca de giro (`ang`). Os círculos de raio (lima R, magenta r) são desenhados à parte (circ_raio)."""
    o = np.asarray(o, float)
    k = lambda v: o + np.array([math.cos(v), math.sin(v), 0.0])
    g = VGroup()
    g.add(Circle(radius=Rg).move_to(o).set_fill("#1B2742", 1).set_stroke(AÇO_ARESTA, 3.0))          # v6 §3: mesmo tom escuro do E3-3 em todo o E3
    g.add(Circle(radius=Rg * 0.9).move_to(o).set_fill("#22304D", 1).set_stroke(mix(AÇO_ARESTA, 0.1), 1.5, opacity=0.5))
    for f in (0.96, 0.78, 0.6):
        g.add(Circle(radius=Rg * f).move_to(o).set_stroke(AÇO_ARESTA, 1.4, opacity=0.35))
    for i in range(3):                                           # marcas de giro no grande
        a = ang + i * TAU / 3
        g.add(Line(o + Rg * 0.38 * np.array([math.cos(a), math.sin(a), 0]), o + Rg * 0.86 * np.array([math.cos(a), math.sin(a), 0])).set_stroke(AÇO_ARESTA, 3.0, opacity=0.8))
    sh = 0.07 * np.array([0.55, -0.83, 0])
    g.add(Circle(radius=Rp).move_to(o + sh).set_fill("#000000", 0.38).set_stroke(width=0))
    g.add(Circle(radius=Rp).move_to(o).set_fill(AÇO_CLARO, 1).set_stroke("#1E2A44", 3.0))
    for f in (0.82, 0.62):
        g.add(Circle(radius=Rp * f).move_to(o).set_stroke("#6F86AD", 1.4, opacity=0.7))
    a = ang + 0.4
    g.add(Line(o + Rp * 0.3 * np.array([math.cos(a), math.sin(a), 0]), o + Rp * 0.82 * np.array([math.cos(a), math.sin(a), 0])).set_stroke("#1E2A44", 3.0))
    g.add(Circle(radius=Rp * 0.3).move_to(o).set_fill("#2B3A55", 1).set_stroke(AÇO_ARESTA, 2.0))
    g.add(Dot(o, radius=Rp * 0.1, color=GEO_CL))
    return g.set_z_index(4)


def pilula(rot, cor=GEO, buff=0.1, op=0.92):
    """Pílula PANEL com borda na cor da grandeza (GEO → borda clareada) atrás de um rótulo; o texto GEO vira #DCE4F2."""
    if cor == GEO:
        cor = GEO_CL
    r = RoundedRectangle(corner_radius=0.1, width=rot.width + 2 * buff, height=rot.height + 2 * buff).move_to(rot).set_fill(PANEL, op).set_stroke(cor, 2.4)
    r._fundo = r._caixa = True
    return r.set_z_index(15)


def linha_halo(a, b, cor=LINHA_CL, w=3.0, z=15):
    """Linha clara de 3 px sobre halo escuro de 8 px (nunca cinza sobre cinza)."""
    h = Line(a, b).set_stroke(HALO, w + (22 if w >= 4.0 else 5)).set_z_index(z - 0.2)      # v5 §4: lima/magenta (w ≥ 4) sobre halo escuro largo
    l = Line(a, b).set_stroke(cor, w).set_z_index(z)
    return VGroup(h, l)


def cota23(a, b, rot, lado=RIGHT, d=0.6, cor=GEO, ticks=True):
    """Cota entre os pontos a e b (tela): linha com halo, pontas em T, e o rótulo numa pílula FORA da silhueta ligada por chamada fina.
    Estrutura: VGroup(VGroup(linha, pontas...), chamada, rot)."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    u = (b - a) / max(1e-9, np.linalg.norm(b - a))
    n = np.array([-u[1], u[0], 0.0])
    corp = GEO_CL if cor == GEO else cor
    wl = 3.0 if cor == GEO else 4.5
    t = [linha_halo(a, b, cor=(LINHA_CL if cor == GEO else cor), w=wl)]
    if ticks:
        for p in (a, b):
            t.append(linha_halo(p - 0.09 * n, p + 0.09 * n, cor=(LINHA_CL if cor == GEO else cor), w=wl))
    rot.set_color(corp).set_z_index(17)
    mid = (a + b) / 2
    rot.move_to(mid + d * lado)
    pil = pilula(rot, cor)
    ch = linha_halo(rot.get_edge_center(-lado) + 0.02 * (-lado), mid, cor=corp, w=2.0)
    return VGroup(VGroup(*t), VGroup(pil, ch), rot).set_z_index(15)


def cartao23(conteudo, cor, w=None, buff=0.22):
    w = w or conteudo.width + 2 * buff
    r = RoundedRectangle(corner_radius=0.12, width=w, height=conteudo.height + 2 * buff).move_to(conteudo).set_fill(PANEL, 0.85).set_stroke(cor, 2.6)
    r._fundo = r._caixa = True
    conteudo.set_z_index(max(8, conteudo.z_index or 0))
    return VGroup(r.set_z_index(conteudo.z_index - 1), conteudo)


# ── ícones (A2, S1, EN2) ───────────────────────────────────────────────────────────────────────────────────────
def bloco25(c, lado, cor=MAS):
    """v2 §3.3: bloco 2.5D — face + topo em paralelogramo claro + lateral escura."""
    c = np.asarray(c, float)
    h, d = lado / 2, lado * 0.28
    face = Square(lado).move_to(c).set_fill(escuro(cor, 0.5), 1).set_stroke(cor, 2)
    topo = Polygon(c + h * UP + h * LEFT, c + h * UP + h * RIGHT, c + (h + d) * UP + (h + d) * RIGHT, c + (h + d) * UP + (d - h) * RIGHT).set_fill(mix(cor, 0.35), 1).set_stroke(cor, 1.5)
    lado_ = Polygon(c + h * RIGHT + h * UP, c + h * RIGHT + h * DOWN, c + (h + d) * RIGHT + (d - h) * UP, c + (h + d) * RIGHT + (h + d) * UP).set_fill(escuro(cor, 0.7), 1).set_stroke(cor, 1.5)
    return VGroup(lado_, topo, face)


def disco25(c, R, cor=STEEL, z=4):
    """v2 §3.3: disco 2.5D — aro de espessura deslocado (~5 px), gradiente radial e brilho."""
    c = np.asarray(c, float)
    off = 0.09 * np.array([0.6, -0.8, 0])
    aro_ = Circle(radius=R).move_to(c + off).set_fill(escuro(cor, 0.55), 1).set_stroke(escuro(GEO, 0.3), 1.5)
    face = Circle(radius=R).move_to(c).set_fill([mix(cor, 0.35), cor, escuro(cor, 0.25)], 1).set_stroke(GEO, 2.2)
    face.set_sheen_direction(UL)
    brilho = Arc(radius=R * 0.82, start_angle=0.6 * PI, angle=0.45 * PI, arc_center=c).set_stroke(WHITE_, 2.4, opacity=0.7)
    return VGroup(aro_, face, brilho).set_z_index(z)


def ic_volante(c, s=1.0, ang=0.0):
    c = np.asarray(c, float)
    off = 0.08 * s * np.array([0.6, -0.8, 0])
    g = VGroup(AnnularSector(inner_radius=0.6 * s, outer_radius=0.8 * s, angle=TAU).move_to(c + off).set_fill(escuro(STEEL, 0.55), 1).set_stroke(escuro(GEO, 0.3), 1.5),
               AnnularSector(inner_radius=0.6 * s, outer_radius=0.8 * s, angle=TAU).move_to(c).set_fill([mix(STEEL, 0.35), STEEL], 1).set_stroke(GEO, 2))
    g[1].set_sheen_direction(UL)
    for k in range(4):
        a = ang + k * PI / 2
        g.add(Line(c + 0.2 * s * np.array([math.cos(a), math.sin(a), 0]), c + 0.6 * s * np.array([math.cos(a), math.sin(a), 0])).set_stroke("#3B475A", 4))
    g.add(disco25(c, 0.2 * s))
    for k in (0, 2):
        a = ang + k * PI / 2
        g.add(disco25(c + 0.5 * s * np.array([math.cos(a), math.sin(a), 0]), 0.1 * s))
    g.add(Arc(radius=0.72 * s, start_angle=0.6 * PI, angle=0.4 * PI, arc_center=c).set_stroke(WHITE_, 2.2, opacity=0.7))
    g.add(Line(c + 0.3 * s * RIGHT, c + 0.3 * s * RIGHT + 1.0 * s * DOWN).set_stroke(GEO, 2))
    g.add(bloco25(c + 0.3 * s * RIGHT + 1.15 * s * DOWN, 0.36 * s))
    return g


def ic_haste(c, s=1.0, th=0.35):
    c = np.asarray(c, float)
    comp, esp = 2.0 * s, 0.14 * s
    u = np.array([math.cos(th), -math.sin(th), 0.0])
    n = np.array([math.sin(th), math.cos(th), 0.0])
    a, b = c - comp / 4 * u, c + 3 * comp / 4 * u
    sombra = Polygon(a - n * esp / 2, b - n * esp / 2, b - n * esp * 0.95, a - n * esp * 0.95).set_fill(escuro(STEEL, 0.6), 1).set_stroke(width=0)
    corpo = Polygon(a + n * esp / 2, b + n * esp / 2, b - n * esp / 2, a - n * esp / 2).set_fill(STEEL, 1).set_stroke(GEO, 2.0)
    brilho = Line(a + n * esp * 0.25, b + n * esp * 0.25).set_stroke(mix(STEEL, 0.6), 2.0)
    return VGroup(sombra, corpo, brilho, pino(c, 0.09 * s))


def ic_carretel(c, s=1.0):
    c = np.asarray(c, float)
    g = VGroup(disco25(c, 0.6 * s), disco25(c, 0.2 * s, cor=mix(STEEL, 0.3)))
    g.add(Line(c + 0.6 * s * RIGHT, c + 0.6 * s * RIGHT + 0.85 * s * DOWN).set_stroke(GEO, 2),
          Line(c + 0.2 * s * LEFT, c + 0.2 * s * LEFT + 1.15 * s * DOWN).set_stroke(GEO, 2))
    g.add(bloco25(c + 0.6 * s * RIGHT + 1.0 * s * DOWN, 0.3 * s), bloco25(c + 0.2 * s * LEFT + 1.33 * s * DOWN, 0.36 * s))
    return g


def ic_pendulo(c, s=1.0, ang=0.12):
    c = np.asarray(c, float)
    u = np.array([math.sin(ang), -math.cos(ang), 0])
    p = c + 1.0 * s * u
    return VGroup(Line(c, p).set_stroke(GEO, 3), disco25(p, 0.42 * s), pino(c, 0.08 * s))


ICONES = (ic_volante, ic_haste, ic_carretel, ic_pendulo)


# ── base dos lotes ─────────────────────────────────────────────────────────────────────────────────────────────
class Lote23(Lote22):
    TITULO = "MECÂNICA · EXERCÍCIOS DE ROTAÇÃO"
    FUNDO = "fundo_grad.png"          # v7: degradê estático (o antigo fundo_lab_ex.png trazia a faixa de horizonte)

    # trilha de itens no rodapé do ESQUEMA (v2 §4.1: letra ≥ 34, nome curto ao lado; ativo 1,0 · feito 0,85 · por fazer 0,6)
    def trilha(self, itens, x0=-7.25, y=-3.72):
        g = VGroup()
        for letra, corpo in itens:
            c = corpo if isinstance(corpo, Mobject) else txt(corpo, 30)
            it = VGroup(txt(letra, 34, bold=True, color=CYAN), c).arrange(RIGHT, buff=0.12)
            g.add(it)
        g.arrange(RIGHT, buff=0.42).move_to(P3(x0, y), aligned_edge=LEFT)
        for it in g:
            escala_op(it, 0.6)
            it._on = False
            for x in it.get_family():
                x._op_ok = True
        g.set_z_index(30)
        self._tr = g
        self._tr_ok = VGroup().set_z_index(31)
        self.add(self._tr_ok)
        return g

    def tr_acende(self, k, rt=0.4):
        self._item = k
        anims = []
        for j, it in enumerate(self._tr):
            alvo = 1.0 if j == k else (0.85 if getattr(it, "_feito", False) else 0.6)
            gl = list(it.family_members_with_points())                      # v7: só a opacidade muda (o Transform entre cópias deixava um quadro com a trilha ampliada/deslocada em dobro)
            o0 = [(float(x.get_fill_opacity()), float(x.get_stroke_opacity())) for x in gl]

            def f_(m, a_, gl=gl, o0=o0, alvo=alvo):
                for x, (f0, s0) in zip(gl, o0):
                    x.set_fill(opacity=f0 + ((alvo if f0 > 0 else 0.0) - f0) * a_, family=False)
                    x.set_stroke(opacity=s0 + ((alvo if s0 > 0 else 0.0) - s0) * a_, family=False)
            anims.append(UpdateFromAlphaFunc(it, f_))
        self.play(*anims, run_time=rt)

    def tr_ok(self, k, rt=0.45):
        it = self._tr[k]
        it._feito = True
        v = T(r"\checkmark", 36, ACC).next_to(it, UP, buff=0.1)
        self._tr_ok.add(v)
        self.play(FadeIn(v, scale=1.4), run_time=rt)

    def tr_sai(self, rt=0.4):
        self.play(FadeOut(self._tr), FadeOut(self._tr_ok), run_time=rt)

    # ── v2 §4: nada de esmaecer equações para "dar foco" ──
    def dica_entra(self, d, apagar=False):
        return super().dica_entra(d, apagar=False)

    def _auditar_v5(self, t, itens, op):
        """v2 §4.1 OPACIDADE: texto/MathTex com 0,05 < opacidade < 0,6 por mais de 6 quadros seguidos (auditoria a cada 3 quadros),
        fora dos fantasmas declarados (`_fantasma`)."""
        super()._auditar_v5(t, itens, op)
        runs = getattr(self, "_op_runs", None)
        if runs is None:
            runs = self._op_runs = {}
        vivos = set()
        for m in itens:
            for x in m.get_family():
                if isinstance(x, (Text, SingleStringMathTex)) and 0.05 < op(x) < 0.6 and not getattr(x, "_fantasma", False) and not getattr(x, "_op_ok", False):
                    k = id(x)
                    vivos.add(k)
                    runs[k] = runs.get(k, 0) + 1
                    if runs[k] == 3:
                        s = getattr(x, "text", None) or getattr(x, "tex_string", "?")
                        print(f"[audit] {t:7.1f}s OPACIDADE BAIXA {s[:40]!r} em {op(x):.2f} por mais de 6 quadros")
        for k in list(runs):
            if k not in vivos:
                del runs[k]

    # ── v2 §2: álgebra do zero (lei → especialização por voo → glyph map → números) ──
    def _alg(self, metodo, partes, n_voos=0):
        lst = getattr(self, "_alg_log", None)
        if lst is None:
            lst = self._alg_log = []
        tex_ = " ".join(p if isinstance(p, str) else "?" for p in partes)
        lst.append((self._aid, metodo, n_voos, tex_))
        print(f"[alg] {self._aid} {metodo} voos={n_voos} | {tex_[:90]}")

    @staticmethod
    def Q(partes, size=48, cores=None):
        """Constrói a linha: tupla de partes (MathTex de string única) ou dict {pre, num, den, post} (uma fração com partes separadas).
        Devolve (MathTex, índices por parte, textos das partes) — a fração entra como pre…, num…, frac, den…, post…"""
        if isinstance(partes, dict):
            pre, num, den, post = (tuple(partes.get(k, ())) for k in ("pre", "num", "den", "post"))
            cf = {}
            flat = list(pre) + list(num) + [r"\frac"] + list(den) + list(post)
            n0, n1, n2 = len(pre), len(pre) + len(num), len(pre) + len(num) + 1 + len(den)
            for i, c in (cores or {}).items():
                if i < n0:
                    cf[("pre", i)] = c
                elif i < n1:
                    cf[("num", i - n0)] = c
                elif i == n1:
                    pass
                elif i < n2:
                    cf[("den", i - n1 - 1)] = c
                else:
                    cf[("post", i - n2)] = c
            m, ix = eqf(pre, num, den, post, size=size, cores=cf)
            tinge(m, pular={j for (nome, k) in cf for j in ix[nome][k]})
            ia = list(ix["pre"]) + list(ix["num"]) + [ix["bar"]] + list(ix["den"]) + list(ix["post"])
            m._partes = [(t, WHITE_) for t in flat]
            m._gl = list(zip(flat, ia))
            return m, ia, flat
        m, ia = M(*partes, size=size, cores=cores)
        return m, ia, list(partes)

    def linha(self, partes, voos=None, cores=None, size=48, rt=1.0, caixa_cor=None, dx=0.0, metodo=None):
        """Linha da CONTA construída da esquerda para a direita; `voos` = {índice da parte: rótulo de origem no desenho}."""
        A, ia, flat = self.Q(partes, size=max(46, size), cores=cores)
        alvo = caixa_l(A, caixa_cor) if caixa_cor else A
        self.pilha.poe(alvo, dx=dx)
        if caixa_cor:
            self.cx(alvo[0])
        self._alg(metodo or ("voo" if voos else "escrita"), flat, len(voos or {}))
        self.monta(A, ia, voos or {}, rt=rt)
        self._consolida(alvo)
        self.foco = alvo
        return A, ia, alvo

    def _consolida(self, alvo):
        """v2: a linha entra INTEIRA na cena depois de montada (sem voos o kit deixava só as peças soltas, que o pilha.so/limpa não tiravam)."""
        self.limpa_pecas(alvo)
        if alvo not in self.mobjects:
            self.add(alvo)

    def passo23(self, A, ia, partes, mapas, cores=None, size=48, rt=1.1, caixa_cor=None):
        """Passo de álgebra explícito: mapas = [(partes de A, partes de B)]."""
        B, ib, flat = self.Q(partes, size=max(46, size), cores=cores)
        alvo = caixa_l(B, caixa_cor) if caixa_cor else B
        self.pilha.poe(alvo)
        if caixa_cor:
            self.cx(alvo[0])
        mp_ = [(J(ia, *a), J(ib, *b)) for a, b in mapas]
        self._alg("GM", flat)
        self.passo(A, B, *mp_, rt=rt, origem=True)
        self.foco = alvo
        return B, ib, alvo

    def gm(self, A, ia, partes, riscar=(), mapas=(), cores=None, size=48, rt=1.1, caixa_cor=None, sai=(), voos=None, tag=None):
        """Passo por glyph map com casamento automático: cada parte de B pega a parte de A com o mesmo TeX (o termo SE MOVE: atravessa a
        igualdade, sai em evidência); `riscar` = partes de A que cancelam (risco antes de sumir); `mapas` = pares explícitos (trocas);
        `sai` = partes de A que somem sem risco. Partes de A sem par somem; partes novas de B escrevem na sua vez (ordem por x)."""
        voos = dict(voos or {})
        if voos and not riscar and not mapas and not tag:                    # v6 §1: literal → numérica = linha NOVA embaixo; a literal fica parada 0,4 s, a estrutura sai pela caneta e os números voam da pílula um a um
            self.wait(0.4)
            return self.linha(partes, voos=voos, cores=cores, size=size, rt=max(rt, 1.4), caixa_cor=caixa_cor, metodo="voo")
        B, ib, flat = self.Q(partes, size=max(46, size), cores=cores)
        texA = [t for t, _ in A._partes]
        ea = {i for a, _ in mapas for i in a} | set(riscar) | set(sai)
        eb = {j for _, b in mapas for j in b} | set(voos)
        usados, pares = set(), []
        for j, t in enumerate(flat):
            if j in eb or not ib[j]:
                continue
            cands = [i for i, s in enumerate(texA) if s.strip() == t.strip() and i not in usados and i not in ea and ia[i]]
            if cands:
                i = min(cands, key=lambda i: abs(i / max(1, len(texA) - 1) - j / max(1, len(flat) - 1)))
                usados.add(i)
                pares.append(([i], [j]))
        ma = usados | {i for a, _ in mapas for i in a}
        mb = {j for _, b in pares for j in b} | eb
        todos = list(mapas) + pares + [([i], []) for i in range(len(texA)) if i not in ma and ia[i]] + [([], [j]) for j in range(len(flat)) if j not in mb and ib[j]]
        alvo = caixa_l(B, caixa_cor) if caixa_cor else B
        if tag:
            alvo = VGroup(alvo, txt(tag, 30, bold=True, color=GEO)).arrange(RIGHT, buff=0.3)
        self.pilha.poe(alvo)                                   # primeiro a vaga (a Pilha pode rolar e mover A); depois os riscos, já no lugar certo
        if caixa_cor:
            self.cx(alvo[0] if not tag else alvo[0][0])
        extras = list(A.submobjects[1:])                       # riscos de passos anteriores: fora da cópia do glyph map
        if extras:
            A.remove(*extras)
            self.add(*extras)
        if riscar:
            rk = VGroup(*[risco(mp(A, ia, [i])) for i in riscar])
            self.play(Create(rk), run_time=0.45)
            extras.append(rk)
        todos = [e for e in todos if not (len(e[1]) == 1 and e[1][0] in voos and not e[0])]
        mp_ = [(J(ia, *a), J(ib, *b)) for a, b in todos]
        # partes que voam do desenho: invisíveis no glyph map; a cópia do rótulo voa para a vaga no mesmo play
        alvos_v, voa_ = [], []
        for j, src in voos.items():
            g_ = mp(B, ib, [j])
            mp_.append(([], J(ib, j)))
            tgt = g_.copy()
            g_.set_opacity(0)
            alvos_v.append((g_, tgt))
            voa_.append(TransformFromCopy(src, tgt, path_arc=-0.6, rate_func=rush_from))
        tg_ = [alvo[1]] if tag else []
        self._alg("GM", flat, len(voos))
        self.passo(A, B, *mp_, rt=rt, origem=True, extra=voa_ + [FadeIn(t) for t in tg_])
        for g_, tgt in alvos_v:
            self.remove(tgt)
            g_.set_opacity(1)
        if extras:
            self.remove(*extras)
            A.add(*extras)
        self.foco = alvo
        return B, ib, alvo

    # cartões da CAIXA DE FERRAMENTAS (A3) que voltam pequenos no canto da CONTA
    LEIS = {
        "soma": ((r"I", "=", r"\sum", "m", "r^2"), MAS),
        "haste_ponta": ((r"I_{\mathrm{haste}}", "=", r"\tfrac{1}{3}", "M", "L^2"), MAS),
        "haste_cm": ((r"I_{cm}", "=", r"\tfrac{1}{12}", "M", "d^2"), MAS),
        "pendulo": (("T", "=", r"2\pi", r"\sqrt{\tfrac{l}{g}}"), WHITE_),
        "steiner": ((r"I", "=", r"I_{cm}", "+", "M", "D^2"), MAS),
        "newton_rot": ((r"\sum", r"\tau", "=", "I", r"\alpha"), FC),
        "energia": (("K", "=", r"\tfrac{1}{2}", "I", r"\omega^2"), KC),
        "pontes": (("v", "=", r"\omega", "r", r"\quad", "a_t", "=", r"\alpha", "r", r"\quad", "a_c", "=", r"\omega^2", "r"), VEL),
    }

    def cartao_lei(self, nome):
        """Mostra (ou mantém) o cartão `nome` pequeno no canto inferior direito da CONTA; devolve (MathTex, índices)."""
        atual = getattr(self, "_card", None)
        if atual is not None and atual[0] == nome:
            return atual[1], atual[2]
        partes, cor = self.LEIS[nome]
        C, ic = M(*partes, size=36)
        bx = caixa_l(C, cor)
        bx.move_to(P3(6.75 - bx.width / 2, max(-2.95, self.pilha._y_topo() - 1.1)))          # logo abaixo da vaga da linha nova; sai depois
        bx.set_z_index(25)
        anims = [FadeIn(bx, shift=0.1 * UP)]
        if atual is not None:
            anims.append(FadeOut(atual[3]))
        self.play(*anims, run_time=0.4)
        if atual is not None:
            self.remove(atual[3])
        self._card = (nome, C, ic, bx)
        return C, ic

    def card_sai(self, rt=0.3):
        atual = getattr(self, "_card", None)
        if atual is not None:
            self.play(FadeOut(atual[3]), run_time=rt)
            self.remove(atual[3])
            self._card = None

    def lei(self, nome, partes, voos=None, cores=None, size=48, rt=1.1, caixa_cor=None):
        """Linha que sai do cartão da lei (TransformFromCopy das partes de mesmo TeX); `voos` extras vêm do desenho."""
        C, ic = self.cartao_lei(nome)
        texC = [t for t, _ in C._partes]
        v = dict(voos or {})
        usados = set()
        if not isinstance(partes, dict):
            for j, t in enumerate(partes):
                if j in v:
                    continue
                for i, s in enumerate(texC):
                    if i not in usados and s.strip() == t.strip() and ic[i] and t.strip() not in ("=", "+", r"\quad"):
                        v[j] = mp(C, ic, [i])
                        usados.add(i)
                        break
        r_ = self.linha(partes, voos=v, cores=cores, size=size, rt=rt, caixa_cor=caixa_cor, metodo="lei")
        self.card_sai()
        return r_

    def secao(self, s, selo=None):
        if getattr(self, "_card", None) is not None:
            self.card_sai()
        return super().secao(s, selo)


# ── volante 3D (E1): trackers e projeções compartilhados por PE1a e PE1b ────────────────────────────────────────
ZB = -0.50          # centro do bloco do volante em repouso (m)
Y_TB = -0.085       # profundidade do tambor/bloco


class VolanteMix:
    def volante3d(self, u0=0.0, K0=4.6, yc0=0.55, op=1.0):
        tr = dict(th=ValueTracker(0.0), u=ValueTracker(u0), K=ValueTracker(K0), yc=ValueTracker(yc0), az=ValueTracker(0.0),
                  ex=ValueTracker(0.0), mi=ValueTracker(0.0), mdy=ValueTracker(0.0), heat=ValueTracker(0.0), cai=ValueTracker(0.0),
                  th2=ValueTracker(0.0), x1=ValueTracker(0.0), alvo_x=ValueTracker(0.0), alvo_z=ValueTracker(0.0),
                  wov=ValueTracker(0.0), maz=ValueTracker(-60.0), mel=ValueTracker(15.0), mK=ValueTracker(K0), mxc=ValueTracker(-3.85), myc=ValueTracker(yc0),
                  max=ValueTracker(0.0), maz_=ValueTracker(0.0), corte=ValueTracker(0.0))
        self.add(*tr.values())
        self.vt = tr
        self.v_flags = {"foco": "", "cord": True, "freio": False, "dois": False}
        self.v_thfn = None          # giro livre: θ calculado do relógio na hora de desenhar (independe da ordem dos updaters)

        def cam():
            b = cam_vol(tr["u"].get_value(), K=tr["K"].get_value(), yc=tr["yc"].get_value(),
                        alvo_x=tr["alvo_x"].get_value(), alvo_z=tr["alvo_z"].get_value())
            w = tr["wov"].get_value()
            if w <= 1e-6:
                return b
            m = dict(b)
            for k, ch in (("az", "maz"), ("el", "mel"), ("K", "mK"), ("xc", "mxc"), ("yc", "myc")):
                m[k] = round(b[k] + w * (tr[ch].get_value() - b[k]), 4)
            m["alvo"] = [round(b["alvo"][0] + w * (tr["max"].get_value() - b["alvo"][0]), 4), 0.0,
                         round(b["alvo"][2] + w * (tr["maz_"].get_value() - b["alvo"][2]), 4)]
            return m

        self.vcam = cam

        def est(t):
            e = {"th": self.v_thfn() if self.v_thfn else tr["th"].get_value(), "explode": tr["ex"].get_value(), "miolo": tr["mi"].get_value(), "miolo_dy": tr["mdy"].get_value(),
                 "heat": tr["heat"].get_value(), "cai": tr["cai"].get_value(), "th2": tr["th2"].get_value(), "x1": tr["x1"].get_value(), "corte": round(tr["corte"].get_value(), 3),
                 "zb": ZB, "cam": cam(), **self.v_flags}
            if not PEDIDOS3D:
                c = cam()
                th = e["th"]
                self.reg("volante", th=th, eixo=pr(c, (e["x1"], 0, 0)), bloco=pr(c, (e["x1"] + 0.155, Y_TB, ZB - 0.15 * th - e["cai"])))
            return r4(e)

        f3 = Fundo3D(self, "volante", est, op=op)
        self.add(f3)
        self.f3 = f3
        return f3

    def plano_v(self, nome, az, el, K, xc, yc, ax=0.0, az_=0.0, rt=1.3, extra=()):
        """Plano de câmera nomeado (v3 §2.1): movimento contínuo (ease in-out) e linha [cam] no log."""
        tr = self.vt
        print(f"[cam] {nome} az={az} el={el} K={K}", flush=True)
        self.play(tr["wov"].animate.set_value(1.0), tr["maz"].animate.set_value(az), tr["mel"].animate.set_value(el), tr["mK"].animate.set_value(K),
                  tr["mxc"].animate.set_value(xc), tr["myc"].animate.set_value(yc), tr["max"].animate.set_value(ax), tr["maz_"].animate.set_value(az_),
                  *extra, run_time=rt, rate_func=smooth)

    def geral_v(self, rt=1.3, extra=()):
        self.vt["wov"].set_value(self.vt["wov"].get_value())
        print("[cam] volta GERAL/frontal", flush=True)
        self.play(self.vt["wov"].animate.set_value(0.0), *extra, run_time=rt, rate_func=smooth)

    def vp(self, p):
        """Ponto 3D do volante → tela (câmera corrente). No modo 2.5D (`modo25`) é o esquema frontal plano: x → horizontal, z → vertical."""
        m = getattr(self, "m25", None)
        if m is not None:
            return m[0] + m[1] * np.array([p[0], p[2], 0.0])
        return pr(self.vcam(), p)

    def modo25(self, C=None, S=None):
        """Liga (C e S) ou desliga o modo 2.5D: `vp`, `v_eixo` e `v_bloco` passam a valer no esquema frontal plano (u/m = S, eixo em C)."""
        self.m25 = None if C is None else (np.asarray(C, float), float(S))

    def rig25_vivo(self, dois=False, x2=1.25, S2=None):
        """Esquema 2.5D vivo guiado pelos mesmos trackers do 3D (θ, cai, calor, flags cord/freio). `dois`: o aro fino ao lado (E1-17)."""
        vt = self.vt
        C, S = self.m25

        def f():
            th = self.v_thfn() if self.v_thfn else vt["th"].get_value()
            g = VGroup(rig25(C, S, th, cai=vt["cai"].get_value(), cord=self.v_flags["cord"], freio=self.v_flags["freio"], heat=vt["heat"].get_value()))
            if self.v_flags.get("dois"):
                g.add(rig25(C + S * x2 * RIGHT, S, vt["th2"].get_value(), cord=True, aro=True))
            return g
        return vivo(f)

    def v_bloco(self, dz=0.0):
        th = self.v_thfn() if self.v_thfn else self.vt["th"].get_value()
        return self.vp((self.vt["x1"].get_value() + 0.155, Y_TB, ZB - 0.15 * th - self.vt["cai"].get_value() + dz))

    def v_eixo(self):
        return self.vp((self.vt["x1"].get_value(), 0, 0))


def r4(d):
    """r4 do kit, também para tipos do numpy (np.bool_ e np.float64 não são serializáveis em JSON)."""
    if isinstance(d, dict):
        return {k: r4(v) for k, v in d.items()}
    if isinstance(d, (list, tuple)):
        return [r4(v) for v in d]
    if isinstance(d, (bool, np.bool_)):
        return bool(d)
    if isinstance(d, (float, np.floating)):
        return round(float(d), 4)
    if isinstance(d, np.integer):
        return int(d)
    return d


# v2: pilha.so com linhas que já saíram (rolagem da Pilha cheia) — elas VOLTAM para a pilha (antes ficavam fora da contabilidade e,
# re-adicionadas por um Indicate/passo, nunca mais saíam da tela)
_so_orig = Pilha.so


def _so_v2(self, *keep, anims=(), rt=0.5):
    dentro = [x for x, _ in self.linhas]
    faltam = [l for l in keep if l not in dentro]
    r = _so_orig(self, *[l for l in keep if l in dentro], anims=anims, rt=rt)
    for l in faltam:
        self.poe(l)
        self.cena.play(FadeIn(l), run_time=0.3)
    return r


Pilha.so = _so_v2
