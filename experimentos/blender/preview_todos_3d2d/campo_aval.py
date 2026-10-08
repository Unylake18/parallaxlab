"""Regras do campo AVALIADO na gaussiana, por caso (Python puro; usadas pelo Blender e pelo Manim, para o 3D, o corte 2D e o texto concordarem).

ativo(cid, p): True quando E ≠ 0 na posição avaliada p (mesma condição do texto de região). comp(cid, p): comprimento físico da seta de campo (∝ |E|), ou 0.
O comprimento segue o módulo do campo: mesma condição → mesma seta. Exceções declaradas: tetos de comprimento (para a seta não sair do quadro) e, em `duas`/`cap_esf`,
um limite para a seta não atravessar a folha/casca seguinte.
"""

R = 1.0                                    # raio do corpo (casca/maciço, cilindros e esferas)
A_PLACA = 0.7                              # meia-espessura da placa
D = 1.1                                    # meia-distância das duas folhas
A_CAP, B_CAP = 0.8, 1.6                    # capacitor esférico


def ativo(cid, p):
    if cid in ("linha", "macico_cil", "folha", "placa", "face", "macico_esf"):
        return True
    if cid in ("casca_cil", "casca_esf"):
        return p >= R - 1e-3
    if cid == "duas":
        return -D - 1e-3 <= p <= D + 1e-3
    if cid == "cap_esf":
        return A_CAP - 1e-3 <= p <= B_CAP + 1e-3
    raise KeyError(cid)


def comp(cid, p):
    if not ativo(cid, p):
        return 0.0
    if cid in ("linha", "casca_cil"):
        return min(0.60, 0.40 / p)
    if cid == "macico_cil":
        u = p / R
        return 0.50 * (u if u <= 1 else 1 / u)
    if cid in ("folha", "face"):
        return 0.6
    if cid == "placa":
        return 0.6 * min(p / A_PLACA, 1.0)
    if cid == "duas":
        return max(0.15, min(0.6, D - 0.08 - p))
    if cid == "casca_esf":
        return min(0.5, 0.5 / (p / R) ** 2)
    if cid == "macico_esf":
        u = p / R
        return 0.5 * (u if u <= 1 else 1 / u ** 2)
    if cid == "cap_esf":
        return max(0.0, min(0.46 * (A_CAP / p) ** 2, B_CAP - 0.12 - p))
    raise KeyError(cid)


MIN = 0.05                                 # (legado) comprimento físico mínimo para considerar a região "com campo desenhável"
W_REG = 0.08                               # largura (em p) da rampa de entrada/saída das setas nos limites da região: elas crescem/encolhem, não "pipocam"
L_MIN = 0.14                               # comprimento mínimo legível da seta avaliada (o comprimento ∝ |E| vale acima disso)


def ss(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def fator(cid, p):
    """0 → 1: rampa de entrada das setas avaliadas nos limites da região com campo (1 nos casos sem limite)."""
    if cid in ("casca_cil", "casca_esf"):
        return ss((p - R) / W_REG)
    if cid == "duas":
        return ss(min(p + D, D - p) / W_REG)
    if cid == "cap_esf":
        return ss(min(p - A_CAP, B_CAP - p) / W_REG)
    return 1.0


def comp_vis(cid, p):
    """Comprimento (mundo) da seta avaliada a desenhar: ∝ |E| com piso legível e rampa nos limites; 0 se não há campo."""
    if not ativo(cid, p):
        return 0.0
    c = comp(cid, p)
    L = max(c, L_MIN) * fator(cid, p) * ss(c / 0.08)
    return L if L >= 0.02 else 0.0
