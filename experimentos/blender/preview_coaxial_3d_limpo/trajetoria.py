"""Trajetória temporal ÚNICA de r (Python puro): usada pelo Blender (que renderiza os quadros nos instantes reais) e pelo Manim (que escolhe
o quadro por tempo). Nada de reamostragem: o quadro k do vídeo (30 fps) corresponde a t = k/30 e a r_em_quadro(k).
"""

FPS = 30
A, B = 0.5, 1.5                                    # condutor interno e casca externa ideal
R0, RA, RB = 0.25, 1.0, 1.75                       # r inicial, r no vão, r fora
# (nome, duração em quadros, parâmetro): intro = geometria sem gaussiana; hold = r constante; move = suavização cúbica entre dois r
SEGS = [("intro", 45, None), ("h0", 36, R0), ("m1", 78, (R0, RA)), ("h1", 48, RA), ("m2", 66, (RA, RB)), ("h2", 54, RB)]
INICIO, acum = {}, 0
for _nome, _n, _p in SEGS:
    INICIO[_nome] = acum
    acum += _n
TOTAL = acum                                       # quadros da animação (sem os fades de entrada e saída)
ss = lambda x: 0.0 if x <= 0 else 1.0 if x >= 1 else x * x * (3 - 2 * x)      # noqa: E731


def segmento(k):
    """(nome, índice dentro do segmento) do quadro k."""
    k = min(max(k, 0), TOTAL - 1)
    for nome, n, _ in reversed(SEGS):
        if k >= INICIO[nome]:
            return nome, k - INICIO[nome]


def r_em_quadro(k):
    nome, j = segmento(k)
    p = dict((n, q) for n, _, q in SEGS)[nome]
    if p is None:
        return None
    if isinstance(p, tuple):
        n = dict((n_, d) for n_, d, _ in SEGS)[nome]
        return p[0] + (p[1] - p[0]) * ss(j / n)       # j / n: o quadro seguinte (início da pausa) cai exatamente no valor final
    return p


def chave(k):
    """Nome do arquivo do quadro k: um por quadro durante o movimento; um só por pausa (r constante); um para a introdução."""
    nome, j = segmento(k)
    return f"{nome}_{j:03d}" if nome.startswith("m") else nome


def quadros_unicos():
    vistos, out = set(), []
    for k in range(TOTAL):
        c = chave(k)
        if c not in vistos:
            vistos.add(c)
            out.append((c, r_em_quadro(k)))
    return out
