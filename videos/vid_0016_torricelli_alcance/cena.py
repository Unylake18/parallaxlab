"""DA EQUAÇÃO AO FENÔMENO — vid_0016 · Torricelli: onde furar para a água chegar mais longe? (vídeo silencioso, ≈185 s)

Estado conceitual único: u = y/H (interno; o público lê y/H). O mesmo `u` (ValueTracker `self.U`, calculado do tempo da cena)
controla o furo e a trajetória do Blender (quadro da sequência), as cotas, os indicadores de v e t, o anel de pouso, a barra de
alcance x e o marcador/traço do gráfico. O sólido `tanque_torricelli` dá só a geometria; todo texto, cota, seta e gráfico são
Manim, posicionados sobre pontos projetados na câmera do Blender (`projecao.json`, gerado por `projecao.py`).

A matemática é construída em cena: MF-Tools (`TransformByGlyphMap`) move, funde e cancela os glifos nas passagens algébricas
(Bernoulli → Torricelli, queda livre → t, substituição em x = vt e cancelamento de g, normalização por H); as demais
passagens usam `TransformMatchingTex`/Replacement. O tanque fica à vista o tempo todo.

Estrutura (tempos aproximados):
  rodada1  0–9,5 s       gancho (y/H = 0,2 e 0,8 alcançam o mesmo ponto) e definição de H, y e H − y            [aprovada]
  seg_a    9,5–35,5 s    Lei de Torricelli: pontos A e B, Bernoulli entre eles, cancelamentos, h = H − y, v = √(2g(H−y))
  seg_b    35,5–40 s     o furo desce: a velocidade cresce (indicador de v)
  seg_c    40–68 s       o tempo no ar: v_y(0) = 0, queda livre, y = ½gt² até t = √(2y/g); o furo desce: t diminui
  seg_d    68–84,5 s     dois efeitos competindo (o furo sobe e desce; v e t reagem)
  seg_e    84,5–100 s    alcance: distância = velocidade × tempo, x = vt, cópia de v e t, cancelamento de g, x = 2√(y(H−y))
  seg_f    100–118,5 s   normalização por H, passo a passo, e os eixos do gráfico
  seg_g    118,5–140 s   o tanque desenha o gráfico (varredura) e o gancho volta: 0,2 e 0,8 com o mesmo alcance
  seg_h    149–185 s     o furo desce até o meio, y = H − y → y = H/2, substituição na função normalizada → x_max = H, síntese e CTA

Sequências Blender (preparar antes; res = 1,2 × o quadro; comandos no fim do arquivo):
  estações (30 quadros, loop de 2 s): y/H = 0,1 · 0,2 · 0,35 · 0,5 · 0,65 · 0,8 · 0,9
  S1: varredura y/H = 0,1 ↔ 0,9 (ciclo de 24 s = 360 quadros a 15 fps, 12 voltas das contas)
  S2: varredura y/H = 0,9 → 0,5 (ciclo de 12 s = 180 quadros, 6 voltas), usada na desaceleração até y/H = 1/2

Preview:  uv run python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0016_torricelli_alcance/media videos/vid_0016_torricelli_alcance/cena.py Vid0016
"""
from contextlib import contextmanager
import json
from pathlib import Path
import re
import sys
import numpy as np
from manim import *
from MF_Tools import TransformByGlyphMap

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experimentos" / "blender" / "arsenal"))
from template.config import BACKGROUND_COLOR, TEXT_COLOR, PRIMARY_COLOR, WATERMARK_PATH
from template.fonts import screen_text
from manim_solido3d import Solido3D

UNIT = Path(__file__).resolve().parent
WHITE, CYAN, VIOLET, MUTED, PINK = TEXT_COLOR, PRIMARY_COLOR, "#9C8CFF", "#ADB8D1", "#EA63FF"
V_COL, T_COL = VIOLET, CYAN                       # v depende de H − y (violeta); t depende de y (ciano)

# Sólido 3D: a imagem tem proporção 9:16 e S vezes o quadro (o fundo é transparente, o excesso fica fora da tela).
S = 1.2                                   # escala da imagem em relação ao quadro 9×16
CX0, CY0 = 0.9, 0.6                       # centro da imagem em unidades do Manim (o maior alcance, u = 1/2, cabe no quadro)
HQ = config.frame_rate >= 24 and config.pixel_width >= 1080       # render final (1080×1920 / 30 fps): sequências a 30 quadros/s e res 1,2× do quadro
FQ = 2 if HQ else 1                       # quadros de sequência por quadro de 15 fps
ASSET_RES = f"{round((1080 if HQ else 540) * S)}x{round((1920 if HQ else 960) * S)}"
NIVEL = 2.2                               # H do sólido (default da ficha)
PROJ = json.loads((UNIT / "projecao.json").read_text(encoding="utf-8"))
TAB = PROJ["tabela"]
TU, TF, TP = np.array(TAB["u"]), np.array(TAB["furo"]), np.array(TAB["pouso"])
EQ_Y = -2.75                              # altura da matemática em construção (faixa de baixo; o tanque fica acima)
MAXW = 6.4                                # largura máxima de uma equação (≈ 70% do quadro de 9 unidades)
EQ2_Y = -3.4                              # álgebra do alcance e da normalização (sem as barras; abaixo do rótulo x)

# Varreduras do Blender: u(φ) = c − a cos 2πφ (a ficha: varrer_furo). Taxa natural = 1 quadro de sequência por quadro do Manim.
TC1, V1, N1 = 24.0, 12, 360               # S1: faixa 0,1–0,9
TC2, V2, N2 = 12.0, 6, 180                # S2: faixa 0,5–0,9
F292, F248, F112, F120 = 292 / 360, 248 / 360, 112 / 360, 120 / 180      # quadros de S1/S2 com u ≈ 0,35 ↓, 0,65 ↓, 0,65 ↑, 0,8 ↓
# ── Linha do tempo guiada pela voz (palavras_tempos.json, gerado por gerar_sync.py) ───────────────────────────────
LEAD = 1.1                                # a abertura visual precede a primeira palavra da fala
FIM_VOZ = 154.24                          # duração da voz recebida (s)
_PAL = json.loads((UNIT / "palavras_tempos.json").read_text(encoding="utf-8"))["palavras"]


def _norm(s):
    return re.sub(r"[^\wáéíóúâêôãõàç]", "", s.lower())


def TAU(frase):
    """Instante (s, no tempo do vídeo) em que a voz começa a dizer `frase`."""
    alvo = [_norm(w) for w in frase.split()]
    pal = [_norm(p["texto"]) for p in _PAL]
    for j in range(len(pal) - len(alvo) + 1):
        if pal[j:j + len(alvo)] == alvo:
            return _PAL[j]["inicio_s"] + LEAD
    raise ValueError(f"Trecho da fala não encontrado: {frase!r}")


# Âncoras. Em cada troca de sequência a fase das contas coincide nas duas imagens (período das estações calculado em `_periodo`).
T_V0 = TAU("quanto maior a profundidade") + 1.55   # estação u = 0,35 → S1 (φ = F292): o furo começa a descer
T_A2 = TAU("acelerada só pela") - 0.6              # S1 chega a u = 0,65 (φ = 1 + F112) → estação u = 0,65
T_D0 = TAU("Agora aparece o conflito")             # estação → S1 (φ = F248): o furo desce
T_MIN = TAU("Se o furo sobe") - 0.5                # S1 em u = 0,1 (φ = 1): o furo passa a subir
T_B1 = TAU("Na horizontal, o movimento")           # S1 em φ = 1 + F248 (u = 0,65) → estação u = 0,65
T_G0 = TAU("Agora cada posição")                   # estação → S1 (φ = F248) para o gráfico
T_B8 = TAU("vinte por cento") - 0.9                # S2 em u = 0,8 → o furo vai a 0,2 (gancho)
T_G1 = T_B8 - 1.0                                  # S1 em u = 0,9 (φ = 1,5) → S2 (φ = 0,5)
T_G2 = TAU("oitenta por cento") - 1.0              # o furo volta a 0,8
T_B8E = TAU("se uma cresce") - 0.3                 # estação u = 0,8 → S2 (φ = F120): o furo desce até o meio
T_S2d = T_B8E + 4.0                                # S2 em u = 0,5 → estação u = 0,5

# φ(t) das varreduras: linear por trechos (a taxa de quadros do Blender acompanha a fala)
KN_S1A = [(T_V0, F292), (T_A2, 1 + F112)]
KN_S1B = [(T_D0, F248), (T_MIN, 1.0), (T_B1, 1 + F248)]
KN_S1C = [(T_G0, F248), (T_G1, 1.5)]
KN_S2A = [(T_G1, 0.5), (T_B8, F120)]
KN_S2B = [(T_B8E, F120), (T_S2d, 1.0)]


def phi_pl(t, knots):
    ts, ps = zip(*knots)
    return float(np.interp(t, ts, ps))


def _periodo(dur, frac):
    """Período da estação para que, depois de `dur` s, a fase das contas avance um número inteiro de voltas mais `frac`."""
    n = max(1, round(dur / 2.0 - frac))
    return dur / (n + frac)


P0 = _periodo(T_V0, (V1 * F292) % 1.0)                          # estação u = 0,35 (desde t = 0) → S1 em φ = F292
P_A = _periodo(T_D0 - T_A2, (V1 * (F248 - F112)) % 1.0)         # estação u = 0,65 (S1 φ = 1 + F112 → φ = F248)
P_B = _periodo(T_G0 - T_B1, 0.0)                                # estação u = 0,65 (S1 φ = 1 + F248 → φ = F248)


def u1(phi):
    return 0.5 - 0.4 * np.cos(2 * np.pi * phi)


def u2(phi):
    return 0.7 - 0.2 * np.cos(2 * np.pi * phi)


def clip(x, a, b):
    return min(max(x, a), b)


def mix_quadros(sol, x):
    """Quadro fracionário x (em quadros da sequência): mistura linear, com alfa pré-multiplicado, dos dois vizinhos."""
    n = sol.frames
    x = x % n
    if config.frame_rate < 24:                      # 15 fps: um quadro do Blender por quadro do Manim, sem mistura
        return sol.quadro(int(round(x)) % n)
    i = int(np.floor(x))
    f = x - i
    a = sol.quadro(i)
    if f < 1e-3:
        return a
    b = sol.quadro((i + 1) % n)
    if f > 1 - 1e-3:
        return b
    fa, fb = a.astype(np.float32), b.astype(np.float32)
    aa, ab = fa[:, :, 3:4] / 255.0, fb[:, :, 3:4] / 255.0
    alfa = aa * (1 - f) + ab * f
    rgb = (fa[:, :, :3] * aa * (1 - f) + fb[:, :, :3] * ab * f) / np.maximum(alfa, 1e-4)
    return np.clip(np.concatenate([rgb, alfa * 255.0], axis=2), 0, 255).astype(np.uint8)


def smooth(x):
    x = clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def u_params(u):
    """Estado conceitual único u = y/H → parâmetros do sólido (câmera fixa, sem seta de velocidade, jato em contas)."""
    return {"altura_furo": round(u * NIVEL, 4), "enquadramento_fixo": 1, "setas": 0, "estilo_jato": 1}


PS1 = {"varrer_furo": 1, "enquadramento_fixo": 1, "setas": 0, "estilo_jato": 1, "voltas_jato": V1, "faixa_min": 0.1, "faixa_max": 0.9}
PS2 = {"varrer_furo": 1, "enquadramento_fixo": 1, "setas": 0, "estilo_jato": 1, "voltas_jato": V2, "faixa_min": 0.5, "faixa_max": 0.9}


def norm2s(nx, ny):
    return np.array([(nx - 0.5) * 9 * S + CX0, (ny - 0.5) * 16 * S + CY0, 0.0])


def pt(u, chave):
    """Ponto projetado do sólido nos estados 0,2 / 0,35 / 0,8 (normalizado 0–1 na imagem) → coordenadas do Manim."""
    nx, ny = PROJ["u"][str(u)][chave]
    return norm2s(nx, ny)


def hole(u):
    return norm2s(np.interp(u, TU, TF[:, 0]), np.interp(u, TU, TF[:, 1]))


def landing(u):
    return norm2s(np.interp(u, TU, TP[:, 0]), np.interp(u, TU, TP[:, 1]))


@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def text(content, size=26, color=WHITE, opacity=1, width=8):
    with wide_pango():
        mob = screen_text(content, size, color=color)
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob.set_opacity(opacity)


def mt(*parts, size=44, color=WHITE):
    return MathTex(*parts, font_size=size, color=color)


def dim_arrow(a, b, color, width=3.2):
    return DoubleArrow(a, b, buff=0, stroke_width=width, color=color, tip_length=0.16,
                       max_tip_length_to_length_ratio=0.3).set_z_index(6)


def guide(a, b, color=MUTED, width=2.2, opacity=0.75):
    return DashedLine(a, b, color=color, stroke_width=width, dash_length=0.1, stroke_opacity=opacity).set_z_index(5)


# ── equações em construção: texto, tamanho e passos de glifos (índices medidos nos MathTex de string única) ─────────────
EQS = {
    "G0": (r"& P_A + \rho g z_A + \tfrac{1}{2} \rho v_A^2 \\ & = P_B + \rho g z_B + \tfrac{1}{2} \rho v_B^2", 56),
    "G1": (r"& P_{atm} + \rho g H + 0 \\ & = P_{atm} + \rho g y + \tfrac{1}{2} \rho v^2", 56),
    "G2": (r"\rho g H = \rho g y + \tfrac{1}{2} \rho v^2", 66),
    "G3": (r"g H = g y + \tfrac{1}{2} v^2", 72),
    "G4": (r"g H - g y = \tfrac{1}{2} v^2", 72),
    "G5": (r"g ( H - y ) = \tfrac{1}{2} v^2", 72),
    "G6": (r"g h = \tfrac{1}{2} v^2", 80),
    "G7": (r"v^2 = 2 g h", 80),
    "G8": (r"v = \sqrt{2 g h}", 80),
    "G9": (r"v = \sqrt{2 g ( H - y )}", 76),
    "T0": (r"\Delta y = v_{0y} t + \tfrac{1}{2} g t^2", 64),
    "Q2": (r"y = 0 \cdot t + \tfrac{1}{2} g t^2", 66),
    "Q3": (r"y = \tfrac{1}{2} g t^2", 76),
    "Q4": (r"2 y = g t^2", 70),
    "Q5": (r"t^2 = \frac{2 y}{g}", 70),
    "Q6": (r"t = \sqrt{\frac{2 y}{g}}", 70),
    "X0": (r"x = v t", 90),
    "XR": (r"x = \sqrt{2 g ( H - y )} \sqrt{\frac{2 y}{g}}", 52),
    "X1": (r"x = \sqrt{2 g ( H - y ) \cdot \frac{2 y}{g}}", 56),
    "X2": (r"x = \sqrt{2 ( H - y ) \cdot 2 y}", 58),
    "X3": (r"x = \sqrt{4 y ( H - y )}", 70),
    "X4": (r"x = 2 \sqrt{y ( H - y )}", 76),
    "N1": (r"\frac{x}{H} = \frac{2}{H} \sqrt{y ( H - y )}", 62),
    "N2": (r"\frac{x}{H} = 2 \sqrt{\frac{y ( H - y )}{H^2}}", 62),
    "N3": (r"\frac{x}{H} = 2 \sqrt{\frac{y}{H} \cdot \frac{H - y}{H}}", 60),
    "N4": (r"\frac{x}{H} = 2 \sqrt{\frac{y}{H} \left( 1 - \frac{y}{H} \right)}", 58),
    # o máximo: y = H − y → y = H/2 → y/H = 1/2, e a substituição na função normalizada
    "M0": (r"y = H - y", 60),
    "M1": (r"y + y = H", 60),
    "M2": (r"2 y = H", 66),
    "M3": (r"y = \frac{H}{2}", 66),
    "M4": (r"\frac{y}{H} = \frac{1}{2}", 60),
    "S0": (r"\frac{x}{H} = 2 \sqrt{\frac{y}{H} \left( 1 - \frac{y}{H} \right)}", 50),
    "S1": (r"\frac{x}{H} = 2 \sqrt{\frac{1}{2} \left( 1 - \frac{1}{2} \right)}", 50),
    "S2": (r"\frac{x}{H} = 2 \sqrt{\frac{1}{2} \cdot \frac{1}{2}}", 52),
    "S3": (r"\frac{x}{H} = 2 \sqrt{\frac{1}{4}}", 56),
    "S4": (r"\frac{x}{H} = 2 \cdot \frac{1}{2}", 60),
    "S5": (r"\frac{x}{H} = 1", 70),
}
MAPAS = {
    ("G0", "G1"): [([0], [0]), ([1], [1]), ([2], [4]), ([3, 4], [5, 6]), ([5], [7]), ([7], [8]), ([8, 9, 10, 11, 12, 13, 14], [9]),
                   ([15], [10]), ([16], [11]), ([17], [12]), ([18], [15]), ([19, 20], [16, 17]), ([21], [18]), ([23], [19]),
                   ([24, 25, 26, 27, 28, 29], [20, 21, 22, 23, 24, 25])],
    ("G1", "G2"): [([5, 6, 7], [0, 1, 2]), ([10], [3]), ([16, 17, 18], [4, 5, 6]), ([19], [7]), ([20, 21, 22, 23, 24, 25], [8, 9, 10, 11, 12, 13])],
    ("G2", "G3"): [([1, 2, 3], [0, 1, 2]), ([5, 6, 7], [3, 4, 5]), ([8, 9, 10], [6, 7, 8]), ([12, 13], [9, 10])],
    ("G3", "G4"): [([0, 1], [0, 1]), ([2], [5]), ([3, 4], [3, 4]), ([5], [2]), ([6, 7, 8, 9, 10], [6, 7, 8, 9, 10])],
    ("G4", "G5"): [([0], [0]), ([1], [2]), ([2], [3]), ([4], [4]), ([5], [6]), ([6, 7, 8, 9, 10], [7, 8, 9, 10, 11])],
    ("G5", "G6"): [([0], [0]), ([1, 2, 3, 4, 5], [1]), ([6], [2]), ([7, 8, 9, 10, 11], [3, 4, 5, 6, 7])],
    ("G6", "G7"): [([6], [0]), ([7], [1]), ([2], [2]), ([5], [3]), ([0], [4]), ([1], [5])],
    ("G7", "G8"): [([0], [0]), ([2], [1]), ([3, 4, 5], [4, 5, 6])],
    ("G8", "G9"): [([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]), ([6], [6, 7, 8, 9, 10])],
    ("T0", "Q2"): [([1], [0]), ([2], [1]), ([3, 4, 5], [2]), ([6], [4]), ([7], [5]), ([8, 9, 10], [6, 7, 8]), ([11], [9]), ([12], [10]), ([13], [11])],
    ("Q2", "Q3"): [([0], [0]), ([1], [1]), ([6, 7, 8], [2, 3, 4]), ([9], [5]), ([10], [6]), ([11], [7])],
    ("Q3", "Q4"): [([0], [1]), ([1], [2]), ([4], [0]), ([5], [3]), ([6], [4]), ([7], [5])],
    ("Q4", "Q5"): [([1], [4]), ([2], [2]), ([0], [3]), ([3], [6]), ([4], [0]), ([5], [1])],
    ("Q5", "Q6"): [([0], [0]), ([2], [1]), ([3], [4]), ([4], [5]), ([5], [6]), ([6], [7])],
    ("XR", "X1"): [(list(range(11)), list(range(11))), ([13], [12]), ([14], [13]), ([15], [14]), ([16], [15])],
    ("X1", "X2"): [([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]), ([6, 7, 8, 9, 10, 11, 12, 13], [5, 6, 7, 8, 9, 10, 11, 12])],
    ("X2", "X3"): [([0, 1, 2, 3], [0, 1, 2, 3]), ([4, 11], [4]), ([12], [5]), ([5, 6, 7, 8, 9], [6, 7, 8, 9, 10])],
    ("X3", "X4"): [([0, 1], [0, 1]), ([4], [2]), ([2], [3]), ([3], [4]), ([5, 6, 7, 8, 9, 10], [5, 6, 7, 8, 9, 10])],
    ("X4", "N1"): [([0], [0]), ([1], [3]), ([2], [4]), ([3], [7]), ([4], [8]), ([5], [9]), ([6, 7, 8, 9, 10], [10, 11, 12, 13, 14])],
    ("N1", "N2"): [([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]), ([5], [13]), ([6], [14]), ([7], [5]), ([8], [6]), ([9], [7]), ([10, 11, 12, 13, 14], [8, 9, 10, 11, 12])],
    ("N2", "N3"): [(list(range(8)), list(range(8))), ([13], [8]), ([14], [9]), ([9, 10, 11], [11, 12, 13])],
    ("N3", "N4"): [(list(range(10)), list(range(10))), ([11], [11]), ([12, 13, 14, 15], [12, 13, 14, 15])],
    ("M0", "M1"): [([0], [0]), ([1], [3]), ([2], [4]), ([3], [1]), ([4], [2])],
    ("M1", "M2"): [([0, 2], [1]), ([3], [2]), ([4], [3])],
    ("M2", "M3"): [([1], [0]), ([2], [1]), ([3], [2]), ([0], [4])],
    ("M3", "M4"): [([0], [0]), ([1], [3]), ([2], [2]), ([3], [5]), ([4], [6])],
    ("S1", "S2"): [(list(range(10)), list(range(10))), ([13, 14, 15], [11, 12, 13])],
    ("S2", "S3"): [(list(range(7)), list(range(7))), ([7, 11], [7]), ([8, 12], [8]), ([9, 13], [9])],
    ("S3", "S4"): [(list(range(5)), list(range(5))), ([7, 8, 9], [6, 7, 8])],
    ("S4", "S5"): [(list(range(4)), list(range(4))), ([4, 5, 6, 7, 8], [4])],
}


class _Vid0016(Scene):
    # ── infraestrutura ────────────────────────────────────────────────────────────────────────────────────────────
    def until(self, t, rotulo=""):
        """Ancora a linha do tempo em `t` (as trocas de sequência dependem da fase das contas)."""
        d = t - self.time
        if d > 1e-6:
            self.wait(d)
        elif d < -0.07:
            print(f"AVISO de tempo: '{rotulo}' atrasou {-d:.2f} s (t = {self.time:.2f}, alvo {t:.2f})")

    def sold(self, u, base=0.0, period=2.0):
        """Estação: sequência de 30 quadros em loop de `period` s no estado u; `base` é a fase das contas no instante da chamada."""
        sol = Solido3D("tanque_torricelli", params=u_params(u), frames=30 * FQ, res=ASSET_RES, render="nunca")
        t0 = self.time
        return self.seq_img(sol, lambda t: base + (t - t0) / period)

    def seq_img(self, sol, phi_fn):
        """Imagem cujo quadro vem da fase φ(t) da sequência (o mesmo tempo que move o resto da cena). Entre dois quadros
        do Blender a imagem é a mistura dos vizinhos (alfa pré-multiplicado): a 15 fps cai exatamente nos quadros; a 30 fps
        a sequência de 15 quadros/s deixa de se repetir quadro sim, quadro não."""
        quadro = lambda: mix_quadros(sol, phi_fn(self.time) * sol.frames)
        mob = ImageMobject(quadro()).set_height(16 * S).move_to([CX0, CY0, 0]).set_z_index(1)

        def passo(m, dt):
            arr = quadro()
            m.pixel_array = arr.copy()
            m.orig_alpha_pixel_array = arr[:, :, 3]
            if m.stroke_opacity < 1:                                  # preserva FadeIn/FadeOut em andamento
                m.pixel_array[:, :, 3] = (arr[:, :, 3] * m.stroke_opacity).astype(m.pixel_array.dtype)

        mob.add_updater(passo)
        return mob

    def u_sched(self, t):
        """O único u da cena, em função do tempo (a mesma lei move o furo do Blender, as cotas, as barras e o gráfico)."""
        if t < T_V0:
            return 0.35
        if t < T_A2:
            return float(u1(phi_pl(t, KN_S1A)))                # desce a 0,1 e sobe a 0,65 (um só movimento de S1)
        if t < T_D0:
            return 0.65
        if t < T_B1:
            return float(u1(phi_pl(t, KN_S1B)))                # desce a 0,1, sobe a 0,9 e desce a 0,65
        if t < T_G0:
            return 0.65
        if t < T_G1:
            return float(u1(phi_pl(t, KN_S1C)))                # o gráfico: desce a 0,1 e sobe a 0,9
        if t < T_B8:
            return float(u2(phi_pl(t, KN_S2A)))                # S2: de 0,9 a 0,8
        if t < T_B8E:                                          # o gancho: 0,8 → 0,2 → 0,8 (fica em 0,8)
            if t < T_B8 + 0.8:
                return 0.8 - 0.6 * smooth((t - T_B8) / 0.8)
            if t < T_G2:
                return 0.2
            if t < T_G2 + 0.8:
                return 0.2 + 0.6 * smooth((t - T_G2) / 0.8)
            return 0.8
        if t < T_S2d:
            return float(u2(phi_pl(t, KN_S2B)))                # S2: desce de 0,8 até 0,5
        return 0.5

    def preparar(self):
        self.camera.background_color = BACKGROUND_COLOR
        rng = np.random.default_rng(16)
        self.add(VGroup(*[Dot([rng.uniform(-4.4, 4.4), rng.uniform(-7.2, 7.2), 0], radius=rng.uniform(0.01, 0.025),
                              color=WHITE, fill_opacity=rng.uniform(0.08, 0.2)) for _ in range(46)]).set_z_index(0))
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(wm.to_corner(UP + RIGHT, buff=0.28).set_z_index(9))
        self.add(text("DA EQUAÇÃO AO FENÔMENO · EP. 05", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4).set_z_index(9))
        self.U = ValueTracker(0.35)
        self.U.add_updater(lambda m, dt: m.set_value(self.u_sched(self.time)))
        self.add(self.U)
        # geometria fixa (câmera fixa): chão, superfície, parede e aresta esquerda do tanque, colunas das cotas
        self.chao_y = pt(0.35, "cota_chao")[1]
        self.sup_y = pt(0.35, "cota_superficie")[1]
        self.parede_x = pt(0.35, "chao_parede")[0]
        self.esq_x = pt(0.35, "esq_chao")[0]
        self.xA, self.xB = self.esq_x - 0.4, self.esq_x - 1.75           # coluna de y e H − y · coluna de H
        self.fim = pt(0.35, "chao_fim")
        self.s1 = Solido3D("tanque_torricelli", params=PS1, frames=N1 * FQ, res=ASSET_RES, render="nunca")
        self.s2 = Solido3D("tanque_torricelli", params=PS2, frames=N2 * FQ, res=ASSET_RES, render="nunca")

    def ring(self, p, color=CYAN, r=0.2):
        return Circle(radius=r, color=color, stroke_width=3.2).move_to(p).set_z_index(7)

    # ── equações: criação e passos de glifos (MF-Tools) ─────────────────────────────────────────────────────────────
    def E(self, chave, y=EQ_Y, x=0.0, cor=None, maxw=MAXW):
        """MathTex em construção: largura limitada (a equação nunca domina a tela) e conferida contra o tanque."""
        s, sz = EQS[chave]
        m = MathTex(s, font_size=sz)
        if m.width > maxw:
            m.scale_to_fit_width(maxw)
        m.move_to([x, y, 0]).set_z_index(6)
        topo = m.get_top()[1]
        if topo > self.chao_y - 0.55 and m.get_bottom()[1] < self.chao_y + 4.2 and abs(x) < 4:
            print(f"AVISO de layout: '{chave}' invade a zona do tanque (topo {topo:.2f}, chão {self.chao_y:.2f})")
        if cor:
            m.set_color(cor)
        return m

    def gpasso(self, de, para, old, rt=1.2, extras=(), cor=None):
        """Uma passagem algébrica por glifos: os termos se movem, se fundem, saem ou entram (MF-Tools)."""
        new = self.E(para, y=old.get_center()[1], x=old.get_center()[0], cor=cor)
        self.play(TransformByGlyphMap(old, new, *MAPAS[(de, para)], auto_fade=True, printing=False), *extras, run_time=rt)
        self.remove(old)
        return new

    def cruzes(self, m, grupos):
        """Cruzes (cancelamentos) sobre grupos de glifos do MathTex `m`."""
        return VGroup(*[Cross(VGroup(*[m[0][i] for i in g]), stroke_color=PINK, stroke_width=5, scale_factor=1.35) for g in grupos]).set_z_index(8)

    # ── RODADA 1 (0–9,5 s): gancho e definição geométrica — aprovada ──────────────────────────────────────────────
    def rodada1(self):
        sa, sb, sd = self.sold(0.2), self.sold(0.8), self.sold(0.35, period=P0)
        self.sd = sd
        h1, h2 = text("O FURO MAIS BAIXO", 44), text("FAZ O JATO IR MAIS LONGE?", 44, CYAN)
        headline = VGroup(h1, h2).arrange(DOWN, buff=0.22).move_to([0, 5.75, 0])
        self.play(FadeIn(sa), FadeIn(headline, shift=UP * 0.15), run_time=0.5)
        ring_a = self.ring(pt(0.2, "furo"))
        self.play(Create(ring_a), run_time=0.3)
        self.play(FadeOut(ring_a), run_time=0.2)
        self.wait(0.3)
        land = pt(0.2, "pouso")                      # o mesmo ponto vale para u = 0,8: x(u) = x(1 − u)
        mark = VGroup(guide(land, land + UP * 2.3, VIOLET, 2.6, 0.9),
                      Circle(radius=0.12, color=WHITE, stroke_width=3.2).move_to(land)).set_z_index(7)
        self.play(Create(mark), run_time=0.4)
        self.wait(0.3)
        self.play(FadeOut(sa), FadeIn(sb), run_time=0.4)
        ring_b = self.ring(pt(0.8, "furo"))
        self.play(Create(ring_b), run_time=0.3)
        self.play(FadeOut(ring_b), run_time=0.2)
        self.play(Indicate(mark[1], color=WHITE, scale_factor=1.7), run_time=0.5)
        self.wait(0.2)

        # a pergunta central do vídeo, antes da derivação: escolher a altura para maximizar o alcance
        pergunta = VGroup(text("QUAL ALTURA DO FURO", 44, WHITE), text("DÁ O MAIOR ALCANCE?", 44, CYAN)
                          ).arrange(DOWN, buff=0.22).move_to([0, 5.75, 0])
        self.play(FadeOut(headline, shift=UP * 0.1), FadeIn(pergunta, shift=UP * 0.1), run_time=0.6)
        self.play(FadeOut(mark), FadeOut(sb), FadeIn(sd), run_time=0.4)          # a pergunta fica enquanto a geometria entra
        self.wait(0.65)
        sub = text("nível da água constante · modelo ideal", 26, opacity=0.7).move_to([0, 5.9, 0])

        chao_y, sup_y, furo = self.chao_y, self.sup_y, pt(0.35, "furo")
        parede_x, esq_x, xA, xB, fim = self.parede_x, self.esq_x, self.xA, self.xB, self.fim

        piso_e = guide([xB - 0.12, chao_y, 0], [esq_x, chao_y, 0], WHITE)
        piso_d = guide([parede_x, chao_y, 0], [fim[0], chao_y, 0], WHITE)
        tag_chao = text("plano de impacto", 22, WHITE, 0.8).move_to([(esq_x + parede_x) / 2, chao_y - 0.42, 0])
        self.play(Create(piso_e), Create(piso_d), FadeIn(tag_chao), run_time=0.55)
        self.wait(0.15)

        sup_e = guide([xB - 0.12, sup_y, 0], [esq_x, sup_y, 0], WHITE)
        seta_H = dim_arrow([xB, chao_y, 0], [xB, sup_y, 0], WHITE)
        lab_H = mt("H", size=46, color=WHITE).move_to([xB, sup_y + 0.45, 0])
        tag_sup = text("superfície", 22, WHITE, 0.8).move_to([parede_x + 1.35, sup_y + 0.42, 0])
        self.play(Create(sup_e), GrowFromCenter(seta_H), FadeIn(lab_H, tag_sup), run_time=0.6)
        self.play(FadeOut(pergunta), FadeIn(sub), run_time=0.4)

        lin_furo = guide([xA - 0.12, furo[1], 0], furo, CYAN, 2.4, 0.8)
        ring_f = self.ring(furo, CYAN, 0.17)
        seta_y = dim_arrow([xA, chao_y, 0], [xA, furo[1], 0], CYAN)
        lab_y = mt("y", size=46, color=CYAN).next_to(seta_y, LEFT, buff=0.16)
        tag_furo = text("furo", 26, CYAN).move_to(furo + np.array([0.95, 0.55, 0]))
        self.play(Create(lin_furo), Create(ring_f), run_time=0.4)
        self.play(GrowFromCenter(seta_y), FadeIn(lab_y, tag_furo), run_time=0.5)
        self.play(FadeOut(ring_f), run_time=0.2)
        self.wait(0.2)

        seta_p = dim_arrow([xA, furo[1], 0], [xA, sup_y, 0], VIOLET)
        lab_p = mt("H", "-", "y", size=38, color=VIOLET).next_to(seta_p, LEFT, buff=0.16)
        self.play(GrowFromCenter(seta_p), FadeIn(lab_p), run_time=0.5)
        self.wait(0.25)

        rel = mt("H", "=", "y", "+", "(H-y)", size=52)
        rel[0].set_color(WHITE), rel[2].set_color(CYAN), rel[4].set_color(VIOLET)
        rel.move_to([0, -2.6, 0])
        self.play(FadeIn(rel, shift=UP * 0.12), run_time=0.5)
        self.wait(0.8)
        self.r1 = dict(sub=sub, rel=rel, piso_e=piso_e, piso_d=piso_d, tag_chao=tag_chao, sup_e=sup_e, seta_H=seta_H, lab_H=lab_H,
                       tag_sup=tag_sup, dependentes=[lin_furo, seta_y, lab_y, tag_furo, seta_p, lab_p])

    # ── cotas, indicadores e alcance vivos (todos leem o mesmo U) ───────────────────────────────────────────────────
    def cotas_vivas(self, com_tag=True):
        U, xA, chao_y, sup_y = self.U, self.xA, self.chao_y, self.sup_y
        hy = lambda: hole(U.get_value())[1]
        lin = always_redraw(lambda: guide([xA - 0.12, hy(), 0], hole(U.get_value()), CYAN, 2.4, 0.8))
        sy = always_redraw(lambda: dim_arrow([xA, chao_y, 0], [xA, hy(), 0], CYAN))
        sp = always_redraw(lambda: dim_arrow([xA, hy(), 0], [xA, sup_y, 0], VIOLET))
        ly = mt("y", size=46, color=CYAN).add_updater(lambda m: m.move_to([xA - 0.45, (chao_y + hy()) / 2, 0]))
        lp = mt("H", "-", "y", size=38, color=VIOLET).add_updater(lambda m: m.move_to([xA - 0.62, min((hy() + sup_y) / 2, sup_y - 0.45), 0]))
        itens = [lin, sy, sp, ly, lp]
        if com_tag:
            itens.append(self.tag_furo())
        for m in itens[3:]:
            m.set_z_index(6)
        return VGroup(*itens)

    def tag_furo(self):
        t = text("furo", 26, CYAN).add_updater(lambda m: m.move_to(hole(self.U.get_value()) + np.array([0.95, 0.55, 0])))
        return t.set_z_index(6)

    def barra(self, nome, cor, y_barra, fn, legenda):
        """Indicador horizontal qualitativo com comprimento ∝ fn(u): v ∝ √(H−y), t ∝ √y (g = 1, H = 1 nas unidades do desenho)."""
        x0 = -2.95
        U = self.U
        barra = always_redraw(lambda: Rectangle(width=max(fn(U.get_value()), 0.02), height=0.26, fill_color=cor, fill_opacity=0.92,
                                                stroke_width=0).move_to([x0 + max(fn(U.get_value()), 0.02) / 2, y_barra, 0]).set_z_index(5))
        lab = mt(nome, size=44, color=cor).move_to([x0 - 0.5, y_barra, 0]).set_z_index(5)
        nota = text(legenda, 17, MUTED, 0.9).set_z_index(5)
        nota.move_to([x0 + nota.width / 2, y_barra + 0.29, 0])        # alinhada à esquerda com a barra
        return barra, lab, nota

    def barra_x(self):
        """Alcance x medido da parede até o ponto de impacto (segue o mesmo U)."""
        U = self.U
        p0 = norm2s(*PROJ["u"]["0.35"]["chao_parede"]) + np.array([0, -0.38, 0])
        seta = always_redraw(lambda: DoubleArrow(p0, landing(U.get_value()) + np.array([0, -0.38, 0]), buff=0, stroke_width=3.4, color=WHITE,
                                                 tip_length=0.16, max_tip_length_to_length_ratio=0.2).set_z_index(6))
        lab = mt("x", size=46, color=WHITE).add_updater(lambda m: m.move_to((p0 + landing(U.get_value())) / 2 + np.array([0, -0.62, 0]))).set_z_index(6)
        return seta, lab

    def nota(self, conteudo, pos, size=24, cor=MUTED, opac=0.95):
        return text(conteudo, size, cor, opac).move_to(pos).set_z_index(6)

    # ── SEG A (9,5–35,5 s): Lei de Torricelli — Bernoulli entre a superfície (A) e o furo (B) ─────────────────────────
    def seg_a(self):
        r1 = self.r1
        self.play(FadeOut(r1["rel"]), FadeOut(r1["sub"]), FadeOut(r1["tag_sup"]), run_time=0.4)
        vivas = self.cotas_vivas(com_tag=False)
        self.remove(*r1["dependentes"])
        self.add(vivas)
        self.vivas = vivas
        cap = text("LEI DE TORRICELLI", 46, CYAN).move_to([0, 6.25, 0])
        sub = text("Bernoulli entre a superfície e o furo", 26, MUTED, 0.95).move_to([0, 5.65, 0])
        self.until(TAU("Comecemos pela velocidade") - 0.1, "título")
        self.play(FadeIn(cap, shift=UP * 0.1), FadeIn(sub), run_time=0.6)
        # pontos A (superfície livre) e B (furo): cada rótulo nasce junto do seu ponto, na fala
        pA, pB = pt(0.35, "superficie_parede"), hole(0.35)
        dotA = Dot(pA, radius=0.09, color=WHITE).set_z_index(7)
        letA = mt("A", size=40, color=WHITE).move_to([1.95, 3.2, 0]).set_z_index(7)
        linA = guide(pA, [1.72, 3.2, 0], WHITE, 1.6, 0.7)
        ringB = self.ring(pB, CYAN, 0.17)
        letB = mt("B", size=40, color=CYAN).move_to([1.95, 0.7, 0]).set_z_index(7)
        linB = guide(pB, [1.72, 0.7, 0], CYAN, 1.6, 0.7)
        self.until(TAU("Aplicamos Bernoulli"), "ponto A")
        self.play(FadeIn(dotA), Create(linA), FadeIn(letA), run_time=0.5)
        self.until(TAU("e o furo"), "ponto B")
        self.play(Create(ringB), Create(linB), FadeIn(letB), run_time=0.5)
        # callouts pequenos: a pressão nos dois pontos, depois as velocidades; z_A = H e z_B = y só aparecem quando a equação os usa
        pres = [mt(s, size=28, color=c).move_to([3.45, y, 0]).set_z_index(7) for s, c, y in
                ((r"P_A = P_{atm}", WHITE, 3.5), (r"P_B = P_{atm}", CYAN, 1.2))]
        vels = [mt(s, size=28, color=c).move_to([3.45, y, 0]).set_z_index(7) for s, c, y in
                ((r"v_A \approx 0", WHITE, 3.0), (r"v_B = v", CYAN, 0.7))]
        zA = mt(r"z_A = H", size=28, color=WHITE).move_to([3.45, 2.5, 0]).set_z_index(7)
        zB = mt(r"z_B = y", size=28, color=CYAN).move_to([3.45, 0.2, 0]).set_z_index(7)
        self.until(TAU("Nos dois pontos"), "pressão atmosférica")
        self.play(*[FadeIn(n, shift=LEFT * 0.1) for n in pres], run_time=0.5)
        # Bernoulli geral (vale ao longo do escoamento) escrito para os dois pontos
        self.until(TAU("E, como o reservatório"), "equação de Bernoulli")
        g0 = self.E("G0", y=-2.9)
        self.play(FadeIn(g0, shift=UP * 0.1), run_time=0.9)
        self.until(TAU("velocidade da superfície"), "velocidade da superfície")
        self.play(*[FadeIn(n, shift=LEFT * 0.1) for n in vels], run_time=0.4)
        g1 = self.gpasso("G0", "G1", g0, rt=1.2, extras=(FadeIn(zA), FadeIn(zB)))
        self.until(TAU("Com essas condições"), "cancelamentos")
        c1 = self.cruzes(g1, [[0, 1, 2, 3], [11, 12, 13, 14]])
        self.play(Create(c1), run_time=0.5)
        self.play(FadeOut(c1), FadeOut(zA), FadeOut(zB), run_time=0.3)
        g2 = self.gpasso("G1", "G2", g1, rt=1.1)
        c2 = self.cruzes(g2, [[0], [4], [11]])
        self.play(Create(c2), run_time=0.5)
        self.play(FadeOut(c2), run_time=0.2)
        g3 = self.gpasso("G2", "G3", g2, rt=1.0)
        self.wait(0.1)
        g4 = self.gpasso("G3", "G4", g3, rt=1.0)
        self.wait(0.1)
        g5 = self.gpasso("G4", "G5", g4, rt=1.0)
        # a cota H − y do tanque é copiada para o termo (H − y) da equação: "essa diferença é a profundidade"
        self.until(TAU("Essa diferença é a profundidade"), "profundidade")
        alvo = VGroup(g5[0][2], g5[0][3], g5[0][4]).get_center()
        copia = self.vivas[4].copy().clear_updaters().set_z_index(8)
        self.add(copia)
        self.play(copia.animate.move_to(alvo).scale(1.15), run_time=0.8)
        self.play(VGroup(g5[0][2], g5[0][3], g5[0][4]).animate.set_color(VIOLET), FadeOut(copia), run_time=0.3)
        hdef = mt("h", "=", "H", "-", "y", size=44)
        hdef[0].set_color(VIOLET), hdef[2].set_color(WHITE), hdef[4].set_color(CYAN)
        hdef.move_to([0, 4.85, 0]).set_z_index(6)
        self.play(FadeIn(hdef, shift=UP * 0.1), run_time=0.4)
        g6 = self.gpasso("G5", "G6", g5, rt=1.0)
        g6[0][1].set_color(VIOLET)
        self.wait(0.1)
        g7 = self.gpasso("G6", "G7", g6, rt=1.0)
        self.wait(0.1)
        g8 = self.gpasso("G7", "G8", g7, rt=1.0)
        self.wait(0.1)
        g9 = self.gpasso("G8", "G9", g8, rt=1.0)
        self.a = dict(cap=cap, sub=sub, hdef=hdef, g9=g9,
                      limpar=[letA, linA, dotA, ringB, linB, letB] + pres + vels)

    # ── SEG B: o resultado sobe para a faixa auxiliar e o indicador de velocidade nasce com o furo descendo ──────────────
    def seg_b(self):
        a = self.a
        b_v, l_v, n_v = self.barra("v", V_COL, -4.05, lambda u: 5.6 * np.sqrt(1 - u), "velocidade de saída")
        self.add(b_v)
        self.play(a["g9"].animate.set_color(V_COL).scale(0.6).move_to([-1.95, 4.15, 0]), FadeOut(a["hdef"]), FadeOut(a["sub"]), FadeIn(l_v), FadeIn(n_v),
                  *[FadeOut(m) for m in a["limpar"]], run_time=0.7)
        self.until(T_V0, "início da descida")
        self.imgS1 = self.seq_img(self.s1, lambda t: phi_pl(t, KN_S1A))
        self.remove(self.sd)
        self.add(self.imgS1)
        tf = self.tag_furo()
        self.add(tf)
        self.b = dict(b_v=b_v, l_v=l_v, n_v=n_v, tf=tf)

    # ── SEG C (40–68 s): de onde vem t — v_y(0) = 0, queda livre, y = ½gt² ─────────────────────────────────────────
    def seg_c(self):
        a, b = self.a, self.b
        U = self.U
        self.until(TAU("O jato sai horizontalmente") - 0.2, "título do tempo")
        cap2 = text("E O TEMPO NO AR?", 46).move_to([0, 6.25, 0])
        self.play(FadeOut(a["cap"]), FadeIn(cap2, shift=UP * 0.1), run_time=0.6)
        # a conta que sai do furo: velocidade horizontal e nenhuma velocidade vertical inicial
        vx = always_redraw(lambda: Arrow(hole(U.get_value()), hole(U.get_value()) + np.array([0.85, 0, 0]), buff=0, stroke_width=5, color=V_COL,
                                         tip_length=0.2, max_tip_length_to_length_ratio=0.35).set_z_index(7))
        vy = mt("v_y(0) = 0", size=34, color=WHITE).add_updater(lambda m: m.move_to(hole(U.get_value()) + np.array([1.6, 1.3, 0]))).set_z_index(7)
        self.add(vx)
        self.until(TAU("então sua velocidade vertical") - 0.2, "v_y(0) = 0")
        self.play(FadeIn(vy), run_time=0.5)
        self.until(T_A2, "estação u = 0,65")
        self.st65a = self.sold(0.65, base=(V1 * F112) % 1.0, period=P_A)         # fase das contas igual à de S1 neste instante
        self.remove(self.imgS1)
        self.add(self.st65a)
        # queda livre: o mesmo y desenhado como queda vertical
        qnota = self.nota("movimento vertical: queda livre", [1.85, -1.95, 0], 22)
        qlin = always_redraw(lambda: guide(hole(U.get_value()) + np.array([0.3, -0.05, 0]), [hole(U.get_value())[0] + 0.3, self.chao_y, 0], CYAN, 2.4, 0.9))
        self.add(qlin)
        self.play(FadeIn(qnota), run_time=0.5)
        self.until(T_A2 + 0.5, "equação do movimento vertical")
        t0 = self.E("T0", y=EQ_Y)
        self.play(FadeIn(t0, shift=UP * 0.1), run_time=0.9)
        self.until(T_A2 + 2.1, "v_0y → 0")
        q2 = self.gpasso("T0", "Q2", t0, rt=1.3, extras=(FadeOut(qnota),))
        self.until(T_A2 + 3.7, "0·t some")
        q3 = self.gpasso("Q2", "Q3", q2, rt=1.3)
        self.until(T_A2 + 5.2, "2y = gt²")
        q4 = self.gpasso("Q3", "Q4", q3, rt=1.2)
        self.until(T_A2 + 6.7, "t² = 2y/g")
        q5 = self.gpasso("Q4", "Q5", q4, rt=1.2)
        self.until(T_A2 + 8.2, "t = √(2y/g)")
        q6 = self.gpasso("Q5", "Q6", q5, rt=1.2)
        self.until(T_D0 - 0.6, "indicador de t")
        # só agora o indicador de tempo: a fórmula já existe e tem origem
        b_t, l_t, n_t = self.barra("t", T_COL, -4.65, lambda u: 5.6 * np.sqrt(u), "tempo de voo")
        self.add(b_t)
        self.play(q6.animate.set_color(T_COL).scale(0.66).move_to([2.55, 4.15, 0]), FadeIn(l_t), FadeIn(n_t), FadeOut(vy), run_time=0.5)
        self.remove(vx)
        self.c = dict(cap2=cap2, q6=q6, b_t=b_t, l_t=l_t, n_t=n_t)

    # ── SEG D (60,5–84,5 s): o furo desce e a seguir sobe e desce: v e t reagem ao mesmo movimento ─────────────────
    def seg_d(self):
        c = self.c
        self.until(T_D0, "descida com t")
        self.imgS1b = self.seq_img(self.s1, lambda t: phi_pl(t, KN_S1B))
        self.remove(self.st65a)
        self.add(self.imgS1b)
        self.until(TAU("Se o furo desce") - 0.1, "dois efeitos")
        cap3 = VGroup(text("FURO MAIS BAIXO", 44), text("jato mais rápido · menos tempo no ar", 34, CYAN)).arrange(DOWN, buff=0.14).move_to([0, 6.15, 0])
        self.play(FadeOut(c["cap2"]), FadeIn(cap3, shift=UP * 0.1), run_time=0.6)
        self.until(T_B1 - 1.0, "fim dos dois efeitos")
        self.d = dict(cap3=cap3)

    # ── SEG E (84,5–100,5 s): o alcance — distância = velocidade × tempo, copiar v e t, cancelar g ─────────────────────
    def seg_e(self):
        a, b, c, d = self.a, self.b, self.c, self.d
        self.until(T_B1, "estação u = 0,65")
        self.st65b = self.sold(0.65, base=(V1 * F248) % 1.0, period=P_B)
        self.remove(self.imgS1b)
        self.add(self.st65b)
        self.remove(b["b_v"], c["b_t"])
        xbar, xlab = self.barra_x()
        self.add(xbar)
        hor = self.nota("movimento horizontal uniforme", [1.7, -2.15, 0], 22)
        self.play(FadeOut(d["cap3"]), FadeOut(b["l_v"]), FadeOut(b["n_v"]), FadeOut(c["l_t"]), FadeOut(c["n_t"]), FadeIn(xlab), FadeIn(hor), run_time=0.8)
        self.xbar, self.xlab = xbar, xlab
        pal = VGroup(text("distância", 34, WHITE), text("=", 34, WHITE), text("velocidade", 34, V_COL), text("×", 34, WHITE), text("tempo", 34, T_COL)).arrange(RIGHT, buff=0.3)
        pal.move_to([0, EQ2_Y, 0]).set_z_index(6)
        self.until(T_B1 + 1.3, "distância = velocidade × tempo")
        self.play(FadeIn(pal, shift=UP * 0.1), run_time=0.8)
        x0 = self.E("X0", y=EQ2_Y)
        x0[0][2].set_color(V_COL), x0[0][3].set_color(T_COL)
        self.until(TAU("alcance é velocidade"), "x = vt")
        self.play(ReplacementTransform(pal[0], x0[0][0]), ReplacementTransform(pal[1], x0[0][1]), ReplacementTransform(pal[2], x0[0][2]),
                  ReplacementTransform(pal[4], x0[0][3]), FadeOut(pal[3]), run_time=1.0)
        xr = self.E("XR", y=EQ2_Y)
        v_rhs = VGroup(*[a["g9"][0][i] for i in range(2, 11)])
        t_rhs = VGroup(*[c["q6"][0][i] for i in range(2, 8)])
        xr[0][2:11].set_color(V_COL)
        xr[0][11:17].set_color(T_COL)
        self.until(TAU("Substituindo as duas") - 0.2, "substituição")
        self.play(ReplacementTransform(x0[0][0:2], xr[0][0:2]), FadeOut(x0[0][2:4]),
                  TransformFromCopy(v_rhs, xr[0][2:11]), TransformFromCopy(t_rhs, xr[0][11:17]), run_time=1.5)
        x1 = self.gpasso("XR", "X1", xr, rt=1.0)
        cg = self.cruzes(x1, [[5], [15]])
        self.play(x1[0][5].animate.set_color(PINK), x1[0][15].animate.set_color(PINK), Create(cg), run_time=0.6)
        self.play(FadeOut(cg), run_time=0.2)
        x2 = self.gpasso("X1", "X2", x1, rt=1.1)
        nota_g = self.nota("o g cancela no alcance ideal", [0, EQ2_Y - 1.3, 0], 26)
        self.play(FadeIn(nota_g), run_time=0.4)
        self.until(TAU("Sobra o produto") - 0.1, "x = 4y(H − y)")
        x3 = self.gpasso("X2", "X3", x2, rt=1.0)
        x4 = self.gpasso("X3", "X4", x3, rt=1.0, extras=(FadeOut(nota_g),))
        self.e = dict(x4=x4, hor=hor)

    # ── SEG F (100–118,5 s): normalização por H, passo a passo ─────────────────────────────────────────────────────────
    def seg_f(self):
        a, c, e = self.a, self.c, self.e
        self.until(TAU("Para comparar tanques") - 0.1, "normalização")
        capn = VGroup(text("VAMOS MEDIR ALTURA E ALCANCE", 40), text("COMO FRAÇÕES DE H", 40, CYAN)).arrange(DOWN, buff=0.14).move_to([0, 6.1, 0])
        self.play(FadeOut(a["g9"]), FadeOut(c["q6"]), FadeIn(capn, shift=UP * 0.1), FadeOut(e["hor"]), run_time=0.7)
        n1 = self.gpasso("X4", "N1", e["x4"], rt=1.2)
        n2 = self.gpasso("N1", "N2", n1, rt=1.2)
        n3 = self.gpasso("N2", "N3", n2, rt=1.2)
        # o que são y/H e x/H: as duas frações de H que nascem na expressão
        gl_y = VGroup(mt(r"\frac{y}{H}", size=40, color=CYAN), text("altura do furo como fração de H", 24, WHITE)).arrange(RIGHT, buff=0.3)
        gl_x = VGroup(mt(r"\frac{x}{H}", size=40, color=WHITE), text("alcance como fração de H", 24, WHITE)).arrange(RIGHT, buff=0.3)
        gl = VGroup(gl_y, gl_x).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 4.6, 0]).set_z_index(6)
        self.play(FadeIn(gl, shift=UP * 0.1), run_time=0.6)
        n4 = self.gpasso("N3", "N4", n3, rt=1.3)
        self.until(TAU("Assim, o gráfico") - 0.3, "eixos do gráfico")
        # a equação sobe e entram os eixos do gráfico, ainda vazios
        n4_top = MathTex(EQS["N4"][0], font_size=50).move_to([0, 5.6, 0]).set_z_index(6)
        axes = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 1], x_length=7.0, y_length=1.95, tips=False,
                    axis_config={"stroke_width": 3.0, "color": MUTED, "include_ticks": True, "tick_size": 0.08}).move_to([0.2, -3.475, 0])
        axes.set_z_index(4)
        tx = VGroup(mt("0", size=32).next_to(axes.c2p(0, 0), DOWN, buff=0.12), mt("1/2", size=32).next_to(axes.c2p(0.5, 0), DOWN, buff=0.12),
                    mt("1", size=32).next_to(axes.c2p(1, 0), DOWN, buff=0.12))
        ty = VGroup(mt("0", size=36).next_to(axes.c2p(0, 0), LEFT, buff=0.18), mt("1", size=36).next_to(axes.c2p(0, 1), LEFT, buff=0.18))
        nx = mt(r"\frac{y}{H}", size=46).next_to(axes.c2p(1, 0), RIGHT, buff=0.12)
        ny = mt(r"\frac{x}{H}", size=46).next_to(axes.c2p(0, 1), UP, buff=0.12).shift(RIGHT * 0.35)
        ex = text("altura do furo", 22, MUTED, 0.95).move_to([axes.c2p(0.3, 0)[0], axes.c2p(0, 0)[1] + 0.4, 0])
        ey = text("alcance", 26, MUTED, 0.95).next_to(ny, RIGHT, buff=0.15)
        self.axes = axes
        self.remove(self.vivas, self.b["tf"])
        self.play(FadeOut(n4, scale=0.9), FadeOut(capn), FadeOut(gl), run_time=0.4)
        self.play(FadeIn(n4_top, shift=DOWN * 0.25), Create(axes), FadeIn(tx, ty, nx, ny, ex, ey),
                  *[FadeOut(m) for m in (self.r1["piso_e"], self.r1["piso_d"], self.r1["tag_chao"], self.r1["sup_e"], self.r1["seta_H"], self.r1["lab_H"])],
                  run_time=1.2)
        self.n4_top = n4_top
        self.grafico_fixo = VGroup(axes, tx, ty, nx, ny, ex, ey)

    # ── SEG G: o tanque desenha o gráfico, e o gancho volta (0,2 e 0,8) na fala ───────────────────────────────────────────
    def seg_g(self):
        U, axes = self.U, self.axes
        self.until(T_G0, "início da varredura")
        imgG = self.seq_img(self.s1, lambda t: phi_pl(t, KN_S1C))
        self.remove(self.st65b)
        self.add(imgG)
        self.imgG = imgG
        # intervalo de u já percorrido pelo marcador: a curva é traçada por ele
        self.umin = ValueTracker(0.65)
        self.umax = ValueTracker(0.65)

        def acompanhar(m, dt):
            u = U.get_value()
            self.umin.set_value(min(self.umin.get_value(), u))
            self.umax.set_value(max(self.umax.get_value(), u))

        self.add(Mobject().add_updater(acompanhar))
        th = lambda u: float(np.arcsin(np.sqrt(clip(u, 0.0, 1.0))))

        def traco():
            a, b = th(self.umin.get_value()), th(self.umax.get_value())
            if b - a < 0.02:
                return VMobject()
            return ParametricFunction(lambda x: axes.c2p(np.sin(x) ** 2, np.sin(2 * x), 0), t_range=[a, b, 0.01], color=CYAN, stroke_width=4.5).set_z_index(4)

        self.traco = always_redraw(traco)
        f = lambda: 2 * np.sqrt(U.get_value() * (1 - U.get_value()))
        marc = always_redraw(lambda: Dot(axes.c2p(U.get_value(), f()), radius=0.12, color=WHITE).set_z_index(8))
        gv = always_redraw(lambda: DashedLine(axes.c2p(U.get_value(), 0), axes.c2p(U.get_value(), f()), color=MUTED, stroke_width=2, dash_length=0.08,
                                              stroke_opacity=0.7).set_z_index(5))
        gh = always_redraw(lambda: DashedLine(axes.c2p(0, f()), axes.c2p(U.get_value(), f()), color=MUTED, stroke_width=2, dash_length=0.08,
                                              stroke_opacity=0.7).set_z_index(5))
        anel_f = always_redraw(lambda: Circle(radius=0.14, color=CYAN, stroke_width=3).move_to(hole(U.get_value())).set_z_index(7))
        anel_p = always_redraw(lambda: Circle(radius=0.12, color=WHITE, stroke_width=3).move_to(landing(U.get_value())).set_z_index(7))
        self.add(self.traco, anel_f, anel_p, marc, gv, gh)
        self.marc, self.anel_f, self.anel_p = marc, anel_f, anel_p
        hint = text("cada altura do furo, um ponto", 24, MUTED, 0.95).move_to([0, 4.55, 0])
        self.play(FadeIn(hint, shift=UP * 0.1), run_time=0.6)
        self.until(T_G0 + 4.0, "hint some")
        self.play(FadeOut(hint), run_time=0.6)
        # S1 chega a 0,9; S2 desce a 0,8 (o gancho)
        self.until(T_G1, "S1 completa")
        img2 = self.seq_img(self.s2, lambda t: phi_pl(t, KN_S2A))
        self.remove(self.imgG)
        self.add(img2)
        self.until(T_B8, "S2 em 0,8")
        # o gancho no gráfico: y/H = 0,2 e 0,8 (mesma altura = mesmo alcance); a estação u = 0,8 entra com a fase de S2 (0)
        st08a = self.sold(0.8, base=(V2 * F120) % 1.0)
        self.remove(img2)
        self.add(st08a)
        st02 = self.sold(0.2)
        self.add(st02)
        self.play(FadeOut(st08a), FadeIn(st02), run_time=0.8)                      # "um furo a vinte por cento da altura"
        p02 = axes.c2p(0.2, 2 * np.sqrt(0.2 * 0.8))
        d02 = Dot(p02, radius=0.1, color=CYAN).set_z_index(9)
        l02 = mt("0{,}2", size=32, color=CYAN).next_to(axes.c2p(0.2, 0), DOWN, buff=0.12).set_z_index(9)
        self.play(FadeIn(d02), FadeIn(l02), Flash(hole(0.2), color=CYAN, flash_radius=0.4), run_time=0.5)
        self.until(T_G2, "volta ao furo alto")
        st08b = self.sold(0.8, base=(-(T_B8E - T_G2) / 2) % 1.0)                   # a fase das contas em T_B8E é 0 (início de S2)
        self.add(st08b)
        self.play(FadeOut(st02), FadeIn(st08b), run_time=0.8)                      # "e outro a oitenta por cento da altura"
        p08 = axes.c2p(0.8, 2 * np.sqrt(0.8 * 0.2))
        d08 = Dot(p08, radius=0.1, color=CYAN).set_z_index(9)
        l08 = mt("0{,}8", size=32, color=CYAN).next_to(axes.c2p(0.8, 0), DOWN, buff=0.12).set_z_index(9)
        land08 = landing(0.8)
        guia = VGroup(guide(land08, land08 + UP * 2.0, VIOLET, 2.6, 0.9), Circle(radius=0.12, color=WHITE, stroke_width=3.2).move_to(land08)).set_z_index(7)
        self.play(FadeIn(d08), FadeIn(l08), Create(guia), Flash(hole(0.8), color=CYAN, flash_radius=0.4), run_time=0.5)
        lig = DashedLine(p02, p08, color=CYAN, stroke_width=3, dash_length=0.1).set_z_index(8)
        mesmo = text("MESMO ALCANCE", 28, CYAN).move_to((p02 + p08) / 2 + np.array([0, -0.5, 0])).set_z_index(9)
        self.until(TAU("chegam exatamente"), "mesmo alcance")
        self.play(Create(lig), FadeIn(mesmo), run_time=0.6)
        self.until(TAU("Então o furo mais baixo") + 2.4, "fim do gancho")
        self.play(FadeOut(mesmo), FadeOut(guia), run_time=0.3)
        self.st08b = st08b
        self.g = dict(d02=d02, d08=d08, l02=l02, l08=l08, lig=lig)

    # ── SEG H: o furo desce até o meio, o máximo é deduzido (y = H − y), substituído e só então anunciado ─────────────────
    def seg_h(self):
        g, axes = self.g, self.axes
        # as cotas do tanque voltam: o furo desce até o meio, y diminui e H − y cresce (a soma é fixa)
        cotas = self.cotas_vivas()
        piso = guide([self.parede_x, self.chao_y, 0], [self.fim[0], self.chao_y, 0], WHITE)
        sup_e = guide([self.xB - 0.12, self.sup_y, 0], [self.esq_x, self.sup_y, 0], WHITE)
        seta_H = dim_arrow([self.xB, self.chao_y, 0], [self.xB, self.sup_y, 0], WHITE)
        lab_H = mt("H", size=46, color=WHITE).move_to([self.xB, self.sup_y + 0.45, 0])
        piso_e = guide([self.xB - 0.12, self.chao_y, 0], [self.esq_x, self.chao_y, 0], WHITE)
        # a expressão dimensional do alcance volta, com o produto y(H − y) em destaque
        e1 = MathTex(EQS["X4"][0], font_size=52).move_to([0, 5.6, 0]).set_z_index(6)
        caixa = SurroundingRectangle(e1[0][5:11], color=PINK, buff=0.1, stroke_width=3.2).set_z_index(7)
        p1 = VGroup(text("PARA O ALCANCE SER MÁXIMO,", 28, WHITE), text("ESSE PRODUTO PRECISA SER MÁXIMO", 28, CYAN)).arrange(DOWN, buff=0.12)
        p1.move_to([0, 4.3, 0]).set_z_index(6)
        self.until(TAU("Então onde está o máximo"), "onde está o máximo")
        self.remove(self.anel_f)
        self.add(cotas)
        self.play(FadeOut(self.n4_top), FadeIn(e1, shift=UP * 0.1), Create(sup_e), Create(piso_e), Create(piso), GrowFromCenter(seta_H), FadeIn(lab_H),
                  run_time=0.9)
        self.until(TAU("O alcance depende do produto"), "produto")
        self.play(Create(caixa), FadeIn(p1), run_time=0.7)
        # soma fixa → no meio as duas alturas são iguais → o produto é máximo
        soma = mt("y", "+", "(H-y)", "=", "H", size=46).move_to([0, 4.75, 0]).set_z_index(6)
        soma[0].set_color(CYAN), soma[2].set_color(VIOLET)
        l1 = text("SOMA FIXA: H", 28, WHITE).move_to([0, 4.05, 0]).set_z_index(6)
        l2 = VGroup(text("PRODUTO MÁXIMO", 30, CYAN), text("QUANDO SÃO IGUAIS", 30, WHITE)).arrange(DOWN, buff=0.1).move_to([0, 4.0, 0]).set_z_index(6)
        rey = SurroundingRectangle(cotas[3], color=CYAN, buff=0.1, stroke_width=3).set_z_index(8)
        rep = SurroundingRectangle(cotas[4], color=VIOLET, buff=0.1, stroke_width=3).set_z_index(8)
        self.until(TAU("somam a altura total") - 0.4, "soma fixa")
        self.play(FadeOut(p1), FadeOut(caixa), run_time=0.3)
        self.play(FadeIn(soma), FadeIn(l1), run_time=0.5)
        # o furo desce até o meio enquanto a fala diz "se uma cresce, a outra diminui"
        self.until(T_B8E, "S2 volta")
        img2b = self.seq_img(self.s2, lambda t: phi_pl(t, KN_S2B))
        self.remove(self.st08b)
        self.add(img2b)
        self.until(T_S2d, "u = 1/2")
        est = self.sold(0.5)                        # fase das contas em t = T_S2d é 0, igual à do fim de S2
        self.remove(img2b)
        self.add(est)
        self.play(Flash(axes.c2p(0.5, 1.0, 0), color=WHITE, flash_radius=0.45), Flash(landing(0.5), color=WHITE, flash_radius=0.4),
                  FadeOut(l1), FadeIn(l2), Create(rey), Create(rep), run_time=0.7)
        self.wait(0.1)
        # y = H − y → y + y = H → 2y = H → y = H/2 → y/H = 1/2 (as duas cotas viram os dois lados da equação)
        self.play(FadeOut(soma), FadeOut(l2), run_time=0.3)
        m0 = self.E("M0", y=4.1)
        m0[0][0].set_color(CYAN), m0[0][2:5].set_color(VIOLET)
        c1 = cotas[3].copy().clear_updaters().set_z_index(8)
        c2 = cotas[4].copy().clear_updaters().set_z_index(8)
        self.add(c1, c2)
        self.play(FadeOut(rey), FadeOut(rep), ReplacementTransform(c1, m0[0][0]), ReplacementTransform(c2, m0[0][2:5]), FadeIn(m0[0][1]), run_time=0.7)
        m1 = self.gpasso("M0", "M1", m0, rt=0.9)
        m2 = self.gpasso("M1", "M2", m1, rt=0.9)
        capm = text("METADE DA ALTURA", 52, WHITE).move_to([0, 6.25, 0])
        esc = text("entre o plano de impacto e a superfície", 24, MUTED, 0.95).move_to([0, 5.6, 0])
        m3 = self.gpasso("M2", "M3", m2, rt=0.9, extras=(FadeOut(e1), FadeIn(capm, shift=UP * 0.1), FadeIn(esc)))
        m4 = self.gpasso("M3", "M4", m3, rt=0.9)
        # a função normalizada volta; y/H = 1/2 entra nos dois lugares de y/H
        s0 = self.E("S0", y=5.95)
        self.play(FadeOut(capm), FadeOut(esc), FadeIn(s0, shift=UP * 0.1), run_time=0.5)
        s1 = self.E("S1", y=5.95)
        meio = m4[0][4:7]
        self.play(TransformByGlyphMap(s0, s1, ([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6]), ([10, 11, 12, 16], [10, 11, 12, 16]),
                                      auto_fade=True, printing=False),
                  TransformFromCopy(meio, s1[0][7:10]), TransformFromCopy(meio, s1[0][13:16]), run_time=1.2)
        self.remove(s0)
        s2 = self.gpasso("S1", "S2", s1, rt=0.9)
        s3 = self.gpasso("S2", "S3", s2, rt=0.9)
        s4 = self.gpasso("S3", "S4", s3, rt=0.9)
        s5 = self.gpasso("S4", "S5", s4, rt=0.9)
        # o resultado: y = H/2 no topo e x_max = H medido na própria seta de alcance
        yfin = mt("y", "=", r"\frac{H}{2}", size=46).move_to([0, 4.4, 0]).set_z_index(6)
        yfin[0].set_color(CYAN)
        ly2 = mt(r"\frac{H}{2}", size=44, color=CYAN)
        lp2 = mt(r"\frac{H}{2}", size=44, color=VIOLET)
        hy = hole(0.5)[1]
        ly2.move_to([self.xA - 0.55, (self.chao_y + hy) / 2, 0])
        lp2.move_to([self.xA - 0.55, (hy + self.sup_y) / 2, 0])
        xh = mt(r"x_{\max}=H", size=40, color=WHITE).move_to(self.xlab.get_center() + np.array([0.2, -0.1, 0])).set_z_index(6)
        self.xlab.clear_updaters()
        b1 = VGroup(text("FURO MAIS BAIXO", 34, CYAN), text("jato mais rápido · menos tempo no ar", 24, WHITE)).arrange(DOWN, buff=0.1)
        b2 = VGroup(text("FURO MAIS ALTO", 34, VIOLET), text("jato mais lento · mais tempo no ar", 24, WHITE)).arrange(DOWN, buff=0.1)
        b1.move_to([0, 6.55, 0]), b2.move_to([0, 5.4, 0])
        self.until(TAU("Nem muito baixo") - 0.1, "nem muito baixo")
        self.play(ReplacementTransform(m4, yfin), FadeOut(s5), ReplacementTransform(self.xlab, xh), ReplacementTransform(cotas[3], ly2),
                  ReplacementTransform(cotas[4], lp2), FadeIn(b1, shift=UP * 0.1), FadeIn(b2, shift=UP * 0.1), run_time=0.8)
        # síntese que responde à pergunta inicial, e o CTA sobre o mesmo estado final
        b3 = text("O MAIOR ALCANCE ACONTECE NO MEIO", 36, WHITE).move_to([0, 5.95, 0])
        self.until(TAU("o maior alcance fica no meio") - 0.2, "o maior alcance fica no meio")
        self.play(FadeOut(b1), FadeOut(b2), run_time=0.3)
        self.play(FadeIn(b3, shift=UP * 0.1), run_time=0.5)
        cta = VGroup(text("Segue o Parallax Lab", 34, WHITE), text("@labparallax", 40, CYAN)).arrange(DOWN, buff=0.24).move_to([0, 5.95, 0])
        self.until(TAU("Segue o Parallax") - 0.3, "CTA")
        self.play(FadeOut(b3), run_time=0.3)
        self.cta_t = self.time
        self.play(FadeIn(cta, shift=UP * 0.1), run_time=0.6)
        self.until(LEAD + FIM_VOZ + 0.8, "fim")


class Vid0016Rodada1(_Vid0016):
    """Só o trecho 0–9,5 s (gancho + definição), aprovado."""

    def construct(self):
        self.preparar()
        self.rodada1()


class Vid0016(_Vid0016):
    """Vídeo silencioso completo."""

    def construct(self):
        self.preparar()
        self.rodada1()
        self.seg_a()
        self.seg_b()
        self.seg_c()
        self.seg_d()
        self.seg_e()
        self.seg_f()
        self.seg_g()
        self.seg_h()


# Preparar as sequências do Blender antes do render (a partir da raiz do repositório; ~19 s cada estação, ~3 min S1):
#   P="python experimentos/blender/arsenal/ponte.py tanque_torricelli --res 648x1152"; C="--set enquadramento_fixo=1 --set setas=0 --set estilo_jato=1"
#   for y in 0.22 0.44 0.77 1.1 1.43 1.76 1.98; do $P --frames 30 --set altura_furo=$y $C; done
#   $P --frames 360 $C --set varrer_furo=1 --set faixa_min=0.1 --set faixa_max=0.9 --set voltas_jato=12
#   $P --frames 180 $C --set varrer_furo=1 --set faixa_min=0.5 --set faixa_max=0.9 --set voltas_jato=6
# Render final 1080×1920 / 30 fps: sequências a 30 quadros/s e 1296×2304 (HQ), ~2× os quadros do preview:
#   P="python experimentos/blender/arsenal/ponte.py tanque_torricelli --res 1296x2304"; C="--set enquadramento_fixo=1 --set setas=0 --set estilo_jato=1"
#   for y in 0.44 0.77 1.1 1.43 1.76; do $P --frames 60 --set altura_furo=$y $C; done
#   $P --frames 720 $C --set varrer_furo=1 --set faixa_min=0.1 --set faixa_max=0.9 --set voltas_jato=12
#   $P --frames 360 $C --set varrer_furo=1 --set faixa_min=0.5 --set faixa_max=0.9 --set voltas_jato=6
#   uv run python -m manim -r 1080,1920 --fps 30 --media_dir videos/vid_0016_torricelli_alcance/media_postagem videos/vid_0016_torricelli_alcance/cena.py Vid0016
