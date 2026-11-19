"""yt_0023 v5 §1.3 — peças 2.5D da haste (E2) e do pêndulo de discos (E4): azul-aço escuro, aresta clara, lima nos raios, lupa do pivô."""
from pecas23 import *  # noqa: F401,F403

AÇO_ESC = "#1B2742"


def mancal25(O, z=3):
    """Mancal fixo atrás do pino (o garfo do 3D visto de frente)."""
    O = np.asarray(O, float)
    g = VGroup(RoundedRectangle(corner_radius=0.16, width=1.15, height=1.15).move_to(O).set_fill(AÇO_ESC, 1).set_stroke(AÇO_ARESTA, 2.4))
    for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        g.add(Dot(O + np.array([0.42 * sx, 0.42 * sy, 0.0]), radius=0.05, color="#5B6B8C"))
    return g.set_z_index(z)


def pino25(O, r=0.17, z=6):
    O = np.asarray(O, float)
    return VGroup(Circle(radius=r).move_to(O).set_fill("#0F1A33", 1).set_stroke(AÇO_CLARO, 2.6),
                  Circle(radius=r * 0.48).move_to(O).set_fill(AÇO_CLARO, 1).set_stroke(width=0),
                  Dot(O, radius=0.025, color="#0F1A33")).set_z_index(z)


def haste25(O, cm, th, LH, esp=0.34):
    """Barra uniforme de aço (azul-aço escuro, aro claro, brilho no topo) com o pino no ponto O (eixo) e o mancal fixo atrás."""
    u = np.array([math.cos(th), -math.sin(th), 0.0])
    n = np.array([math.sin(th), math.cos(th), 0.0])
    corpo = RoundedRectangle(corner_radius=0.09, width=LH, height=esp).rotate(-th).move_to(cm).set_fill(AÇO_FRIO, 1).set_stroke(AÇO_ARESTA, 3.0).set_z_index(4)
    brilho = Line(cm - (LH / 2 - 0.14) * u + n * esp * 0.2, cm + (LH / 2 - 0.14) * u + n * esp * 0.2).set_stroke("#5B6B8C", 3.0, opacity=0.75).set_z_index(4.2)
    return VGroup(mancal25(O), corpo, brilho, pino25(O, 0.16, 4.6))


def lupa_pivo(O, th, F, fr=None, fp=None, LC=None, RL=1.1, mag=3.1):
    """Lupa do pivô (E2-6 a E2-10): círculo ampliado ×2,6 com o pino, um pedaço da barra e as setas F (e F_r, F_⊥ tracejadas) no mesmo ângulo.
    Presa ao pivô por duas tangentes finas; fica na coluna da esquerda, fora da barra."""
    O = np.asarray(O, float)
    LC = P3(-6.4, -1.6) if LC is None else np.asarray(LC, float)
    d = LC - O
    dn = d / max(1e-9, np.linalg.norm(d))
    pp = np.array([-dn[1], dn[0], 0.0])
    r0 = 0.3
    g = VGroup()
    for s in (1, -1):
        g.add(linha_halo(O + s * r0 * pp, LC + s * RL * pp, cor=GEO_CL, w=1.8, z=15))
    g.add(Circle(radius=r0).move_to(O).set_fill(PANEL, 0.0).set_stroke(GEO_CL, 2.4).set_z_index(15.5))
    g.add(Circle(radius=RL).move_to(LC).set_fill(PANEL, 0.96).set_stroke(GEO_CL, 2.8).set_z_index(16))
    u = np.array([math.cos(th), -math.sin(th), 0.0])
    n = np.array([math.sin(th), math.cos(th), 0.0])
    esp = 0.34 * mag * 0.55
    stub = RoundedRectangle(corner_radius=0.06, width=1.7, height=esp).rotate(-th).move_to(LC + 0.0 * u).set_fill(AÇO_FRIO, 1).set_stroke(AÇO_ARESTA, 2.4).set_z_index(16.2)
    g.add(stub, pino25(LC, 0.17 * mag * 0.55, 16.4))
    for vec, dash, w in ((F, False, 6), (fr, True, 4), (fp, True, 4)):
        if vec is None:
            continue
        L = float(np.linalg.norm(vec))
        if L < 0.06:
            continue
        v = vec / L * min(0.95, 0.2 + 0.62 * L)
        if dash:
            g.add(DashedLine(LC, LC + v, dash_length=0.07).set_stroke(FC, 3.5).set_z_index(16.6))
        else:
            g.add(seta_s(LC, LC + v, FC, w, tip=0.2, z=16.6))
    return g
