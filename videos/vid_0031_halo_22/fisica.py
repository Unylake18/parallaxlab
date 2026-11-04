"""vid_0031 — física do halo de 22°: funções puras, origem única do raio desenhado, do gráfico, dos pares e do histograma.

cena.py, gerar_timeline.py e o QA importam daqui; nada é desenhado a partir de tabela digitada.
Hexágono: vértices em 30° + 60°k + θ (anti-horário). Face k = vértice k → k + 1, normal externa em 60° + 60°k + θ.
Face 2 = entrada (esquerda); 5 = oposta; 1 e 3 = vizinhas; 0 e 4 = alternadas; no caminho 2 → 4 a face pulada é a 3.
QA da §10: uv run python videos/vid_0031_halo_22/fisica.py  (escreve qa/checagens.txt)
"""
from pathlib import Path

import numpy as np

N_GELO, N_VERMELHO, N_VIOLETA = 1.31, 1.307, 1.317
N_AGUA = 1.333
# v6 (§B.8): gelo Ih a 266 K, Warren & Brandt (2008), arquivo index_ice_rf_warren_2008.txt de
# gwest.gats-inc.com/ice_index, interpolação linear: 656 nm entre 0,650 (1,3080) e 0,660 µm (1,3078) → 1,3079;
# 405 nm entre 0,400 (1,3194) e 0,410 µm (1,3185) → 1,3190. Os mínimos dão 21,68° e 22,52° (na tela: 21,7° e 22,5°).
N_GELO_VERMELHO, N_GELO_VIOLETA = 1.3079, 1.3190
ALPHA0 = -30.0      # direção fixa do raio solar nas cenas 2D (graus; desce da esquerda para a direita)
FRAC_Q = 0.45       # o raio interno passa por Q, no bissetor do prisma, a 0,45 apótema do centro rumo à face pulada


# ── prisma de 60° (§6, fórmulas fechadas) ─────────────────────────────────────────────────────────────────
def desvio(i1_deg, n=N_GELO, A=60.0):
    """Desvio no prisma de ângulo A; NaN se houver reflexão total na saída."""
    i1 = np.radians(i1_deg)
    r1 = np.arcsin(np.sin(i1) / n)
    s = n * np.sin(np.radians(A) - r1)
    return np.where(np.abs(s) < 1, i1_deg + np.degrees(np.arcsin(np.clip(s, -1, 1))) - A, np.nan)


def saida(i1_deg, n=N_GELO, A=60.0):
    """Ângulo de saída i2 (graus)."""
    return desvio(i1_deg, n, A) + A - i1_deg


def par_invertido(i1_deg, n=N_GELO):
    """Ângulo de incidência do caminho invertido (mesmo desvio)."""
    return saida(i1_deg, n)


def d_min(n=N_GELO, A=60.0):
    return 2 * np.degrees(np.arcsin(n * np.sin(np.radians(A / 2)))) - A


def i1_min(n=N_GELO, A=60.0):
    return np.degrees(np.arcsin(n * np.sin(np.radians(A / 2))))


def i1_transmite(n=N_GELO, A=60.0):
    """Menor i1 que ainda sai pela segunda face (r2 = ângulo crítico)."""
    return np.degrees(np.arcsin(n * np.sin(np.radians(A) - np.arcsin(1 / n))))


def faixa_fundo(delta=1.0, n=N_GELO):
    """Intervalo de i1 em que D < D_min + delta (bissecção nos dois ramos do vale)."""
    alvo, im = d_min(n) + delta, i1_min(n)

    def raiz(a, b):
        for _ in range(80):
            m = (a + b) / 2
            if (desvio(m, n) - alvo) * (desvio(a, n) - alvo) <= 0:
                b = m
            else:
                a = m
        return (a + b) / 2
    return raiz(i1_transmite(n) + 1e-9, im), raiz(im, 90.0)


# ── v2: recap do arco-íris e projeção de orientações (handoff v2, §B.3) ──────────────────────────────────
def theta_arco_iris(b_ratio, n=N_AGUA):
    """Ângulo de saída do arco-íris primário (graus) em função de b/R."""
    i = np.arcsin(b_ratio); r = np.arcsin(b_ratio / n)
    return np.degrees(4 * r - 2 * i)          # máximo 42,08° em b/R = 0,861


def projecao_orientacoes(n_pontos=60, i_min=14.0, i_max=89.0):
    """Orientações igualmente espaçadas (ângulo de incidência) e seus desvios."""
    i = np.linspace(i_min, i_max, n_pontos)
    return i, desvio(i)


def angulo_no_olho(sol_dir, olho, cristal):
    """Ângulo (graus) entre a direção do Sol e a direção do cristal, vistos do olho."""
    a = np.asarray(sol_dir, float); a /= np.linalg.norm(a)
    b = np.asarray(cristal, float) - np.asarray(olho, float); b /= np.linalg.norm(b)
    return np.degrees(np.arccos(np.clip(a @ b, -1, 1)))


# ── Snell vetorial e traçado real no hexágono ─────────────────────────────────────────────────────────────
def refrata(d, nrm, eta):
    """d unitário; nrm normal unitária voltada para o lado de onde a luz vem; eta = n_incidente / n_transmitido.
    Vetorizado em (..., 2). Devolve (direção, reflexão_total)."""
    c = -np.sum(d * nrm, axis=-1, keepdims=True)
    k = 1 - eta ** 2 * (1 - c ** 2)
    t = eta * d + (eta * c - np.sqrt(np.clip(k, 0, None))) * nrm
    r = d + 2 * c * nrm
    tir = k[..., 0] < 0
    return np.where(tir[..., None], r, t), tir


def rot(v, ang_deg):
    a = np.radians(ang_deg)
    return np.array([np.cos(a) * v[0] - np.sin(a) * v[1], np.sin(a) * v[0] + np.cos(a) * v[1]])


def u(ang_deg):
    a = np.radians(ang_deg)
    return np.array([np.cos(a), np.sin(a)])


def ang(v):
    return np.degrees(np.arctan2(v[1], v[0]))


def hexagono(c=(0., 0.), R=1., theta=0.):
    return np.array([np.asarray(c, float) + R * u(30 + 60 * k + theta) for k in range(6)])


def normal_face(k, theta=0.):
    return u(60 + 60 * k + theta)


def _bate(p, d, V, excluir=None):
    """Primeira face atingida pelo raio p + t·d (t > 0): (t, face) ou (inf, None)."""
    melhor = (np.inf, None)
    for k in range(6):
        if k == excluir:
            continue
        A, B = V[k], V[(k + 1) % 6]
        M = np.array([d, A - B]).T
        if abs(np.linalg.det(M)) < 1e-12:
            continue
        t, s = np.linalg.solve(M, A - p)
        if t > 1e-9 and -1e-12 <= s <= 1 + 1e-12 and t < melhor[0]:
            melhor = (t, k)
    return melhor


def tracar(p, d, V, n=N_GELO, max_eventos=6):
    """Raio real (Snell vetorial + reflexão total) no hexágono V.
    Devolve pontos de evento, faces, tipos ('entra', 'rt', 'sai') e a direção final; o último ponto é o de saída
    (ou o da última reflexão, se acabar dentro)."""
    p, d = np.asarray(p, float), np.asarray(d, float) / np.linalg.norm(d)
    theta = ang(V[0] - V.mean(axis=0)) - 30
    pontos, faces, tipos, dentro, face = [p], [], [], False, None
    for _ in range(max_eventos):
        t, k = _bate(p, d, V, excluir=face if not dentro else None)
        if k is None:
            break
        p = p + t * d
        N = normal_face(k, theta)
        if not dentro:
            d, _ = refrata(d, N, 1 / n)
            dentro, tipo = True, 'entra'
        else:
            d, tir = refrata(d, -N, n)
            tipo = 'rt' if tir else 'sai'
            dentro = tir
        pontos.append(p); faces.append(k); tipos.append(tipo)
        face = k
        if tipo == 'sai':
            break
    return {'pontos': np.array(pontos), 'faces': faces, 'tipos': tipos, 'd_final': d}


def caminho60(i1, c=(0., 0.), R=1., n=N_GELO, alpha0=ALPHA0, frac=FRAC_Q, desloc=0.):
    """Caminho de 60° (face 2 → face 4) para incidência i1 com o raio solar fixo em alpha0: o cristal gira (θ = α0 + i1).
    O raio interno passa por Q (bissetor do prisma, rumo à face pulada), deslocado de 'desloc' ao longo da face de
    entrada (raios paralelos). O traçado é real: Snell vetorial a partir do raio externo."""
    c = np.asarray(c, float)
    theta = alpha0 + i1
    V = hexagono(c, R, theta)
    ap = R * np.cos(np.radians(30))
    Q = c + frac * ap * normal_face(3, theta)
    r1 = np.degrees(np.arcsin(np.sin(np.radians(i1)) / n))
    w = u(theta - r1)                                   # direção interna prevista
    A, B = V[2], V[3]
    M = np.array([w, A - B]).T
    t, s = np.linalg.solve(M, A - Q)                    # Q + t·w na reta da face 2 (t < 0)
    P1 = A + s * (B - A) + desloc * (B - A) / np.linalg.norm(B - A)
    d_in = u(alpha0)
    tr = tracar(P1 - 6 * d_in, d_in, V, n)
    tr.update(theta=theta, V=V, c=c, R=R, d_in=d_in, Q=Q, i1=i1)
    return tr


def desvio_vetorial(tr):
    """Desvio do traçado: ângulo entre a direção de entrada e a de saída (graus)."""
    return np.degrees(np.arccos(np.clip(np.dot(tr['d_in'], tr['d_final']), -1, 1)))


def espelho_bissetor(pts, tr):
    """Reflete pontos no bissetor do prisma (reta pelo centro na direção da normal da face pulada)."""
    e = normal_face(3, tr['theta'])
    v = np.asarray(pts) - tr['c']
    return tr['c'] + 2 * (v @ e)[:, None] * e - v


# ── histograma de raios por desvio (§6, amostragem documentada) ────────────────────────────────────────────
def amostra_desvios(n=N_GELO, aceitos=24000, seed=31, lote=60000):
    """Hexágono regular de lado 1 (fixo); feixe com orientação φ ~ U(0°, 360°) e parâmetro de impacto uniforme
    ao longo do feixe (b ~ U(−1, 1), cobre o hexágono). Traçado real vetorizado: guarda só os raios que entram por uma
    face e saem pela face alternada (±2) sem reflexão interna. Devolve os desvios (graus) na ordem sorteada."""
    rng = np.random.default_rng(seed)
    V = hexagono()
    NF = np.array([normal_face(k) for k in range(6)])
    out = []
    while sum(len(o) for o in out) < aceitos:
        phi = rng.uniform(0, 2 * np.pi, lote)
        b = rng.uniform(-1, 1, lote)
        d = np.stack([np.cos(phi), np.sin(phi)], 1)
        p = -3 * d + b[:, None] * np.stack([-np.sin(phi), np.cos(phi)], 1)

        def bate(p, d, excl):
            T = np.full((len(p), 6), np.inf)
            for k in range(6):
                A, B = V[k], V[(k + 1) % 6]
                e = B - A
                den = d[:, 0] * (-e[1]) - d[:, 1] * (-e[0])
                w = A - p
                t = (w[:, 0] * (-e[1]) - w[:, 1] * (-e[0])) / np.where(den == 0, np.nan, den)
                s = (d[:, 0] * w[:, 1] - d[:, 1] * w[:, 0]) / np.where(den == 0, np.nan, den)
                ok = (t > 1e-9) & (s >= 0) & (s <= 1) & (k != excl)
                T[:, k] = np.where(ok, t, np.inf)
            return T.min(1), T.argmin(1)

        t1, f1 = bate(p, d, np.full(lote, -1))
        hit = np.isfinite(t1)
        p, d, f1, t1 = p[hit], d[hit], f1[hit], t1[hit]
        p1 = p + t1[:, None] * d
        di, _ = refrata(d, NF[f1], 1 / n)
        t2, f2 = bate(p1, di, f1)
        do, tir = refrata(di, -NF[f2], n)
        ok = (((f2 - f1) % 6 == 2) | ((f2 - f1) % 6 == 4)) & ~tir
        out.append(np.degrees(np.arccos(np.clip(np.sum(d[ok] * do[ok], 1), -1, 1))))
    return np.concatenate(out)[:aceitos]


def contagens(D, a0=20., a1=45., passo=.5):
    bordas = np.arange(a0, a1 + 1e-9, passo)
    return np.histogram(D, bins=bordas)[0], bordas


def perfil_anel(a0=20., a1=45., passo=.1, aceitos=60000):
    """Perfil didático do anel em função do ângulo ao Sol: histograma (bins 0,05°) suavizado por gaussiana σ = 0,12°
    (kernel ≤ 0,3°), dividido por sen(ângulo) (brilho por ângulo sólido) e clampado. Cor: média ponderada das curvas
    de n = 1,307 (vermelho), 1,31 (branco) e 1,317 (violeta): o excesso do vermelho sobre o violeta tinge de vermelho,
    o do violeta tinge de violeta, o equilíbrio fica branco. Devolve (ângulos, rgb N×3 em 0–1)."""
    fino = np.arange(a0, a1 + 1e-9, .05)
    centros = (fino[:-1] + fino[1:]) / 2
    x = np.arange(-.4, .4001, .05)
    ker = np.exp(-x ** 2 / (2 * .12 ** 2)); ker /= ker.sum()
    curvas = []
    for n in (N_VERMELHO, N_GELO, N_VIOLETA):
        h = np.histogram(amostra_desvios(n, aceitos), bins=fino)[0].astype(float)
        curvas.append(np.convolve(h, ker, 'same') / np.sin(np.radians(centros)))
    ref = curvas[1].max()
    angs = np.arange(a0, a1 + 1e-9, passo)
    P = np.array([np.interp(angs, centros, cv / ref) for cv in curvas])        # 3 × N
    vermelho, branco, violeta = np.array([1., .42, .32]), np.ones(3), np.array([.72, .66, 1.])
    soma = P.sum(0)
    e = (P[0] - P[2]) / np.where(soma > 1e-9, soma / 3, 1)                     # excesso relativo: +1 só vermelho
    tom = branco + np.clip(e, 0, 1)[:, None] * (vermelho - branco) + .35 * np.clip(-e, 0, 1)[:, None] * (violeta - branco)
    brilho = np.clip(1.6 * soma / 3, 0, 1) ** .75                             # clamp estético
    return angs, tom * brilho[:, None]


# ── QA numérico (§10) ─────────────────────────────────────────────────────────────────────────────────────
def qa():
    linhas, falhas = [], []

    def chk(nome, obtido, esperado, tol):
        ok = bool(np.all(np.abs(np.asarray(obtido, float) - np.asarray(esperado, float)) <= tol))
        linhas.append(f'[{"OK" if ok else "FALHA"}] {nome}: obtido {np.round(obtido, 4).tolist()} · esperado {esperado} ± {tol}')
        if not ok:
            falhas.append(nome)

    chk('d_min(1,31)', d_min(), 21.84, .01)
    chk('i1 no mínimo', i1_min(), 40.92, .01)
    chk('ângulo crítico', np.degrees(np.arcsin(1 / N_GELO)), 49.76, .01)
    chk('i1 mínimo para transmitir', i1_transmite(), 13.47, .01)
    ii = np.array([20, 25, 30, 35, 45, 50, 55, 60, 70, 80, 90.])
    chk('desvio(20…90)', desvio(ii), [27.5, 24.6, 23.0, 22.2, 22.0, 22.5, 23.4, 24.7, 28.7, 34.8, 43.5], .05)
    g = np.linspace(i1_transmite() + 1e-6, 90, 20001)
    Dg = desvio(g)
    d1 = np.diff(Dg)
    trocas = int(np.sum(np.diff(np.sign(d1)) != 0))
    d2 = np.diff(Dg, 2)
    linhas.append(f'[{"OK" if trocas == 1 and d2.min() > -1e-9 else "FALHA"}] vale único: trocas de sinal de dD/di1 = {trocas}; '
                  f'min d²D (convexidade) = {d2.min():.3e}')
    if trocas != 1 or d2.min() <= -1e-9:
        falhas.append('vale único')
    a, b = faixa_fundo()
    chk('fundo achatado (D < 22,84 ⇔ i1 em)', [a, b], [30.7, 52.1], .05)
    pares = [20, 25, 30, 35, 38, 40, 40.92]
    chk('pares (direto → invertido)', par_invertido(np.array(pares)), [67.5, 59.6, 53.0, 47.2, 43.9, 41.9, 40.9], .06)
    chk('pares (desvio)', desvio(np.array(pares)), [27.5, 24.6, 23.0, 22.2, 21.9, 21.85, 21.84], .06)
    err = np.nanmax(np.abs(desvio(par_invertido(g)) - Dg))
    chk('desvio(par_invertido(a)) == desvio(a) (erro máx.)', err, 0, 1e-9)
    chk('d_min(1,307) / d_min(1,317)', [d_min(N_VERMELHO), d_min(N_VIOLETA)], [21.61, 22.37], .01)
    viz = desvio(np.linspace(0, 90, 901), A=120.)
    linhas.append(f'[{"OK" if np.all(np.isnan(viz)) else "FALHA"}] face vizinha (A = 120°): reflexão total para todo i1 '
                  f'({int(np.isnan(viz).sum())}/901 NaN)')
    if not np.all(np.isnan(viz)):
        falhas.append('face vizinha')
    chk('d_min(1,0)', d_min(1.0), 0, 1e-9)
    D = amostra_desvios(aceitos=24000)
    perto = np.mean(D < d_min() + 1)
    linhas.append(f'[{"OK" if D.min() >= d_min() - 1e-6 and abs(perto - .46) < .03 else "FALHA"}] histograma 2D '
                  f'({len(D)} aceitos): mínimo {D.min():.4f}° (≥ {d_min():.4f}°); {100 * perto:.1f}% a < 1° do mínimo')
    if D.min() < d_min() - 1e-6 or abs(perto - .46) >= .03:
        falhas.append('histograma')
    # traçado vetorial × fórmula fechada (o raio desenhado e o ponto do gráfico concordam)
    piores = 0.
    for i1 in np.arange(14, 88.01, .5):
        tr = caminho60(i1)
        assert tr['faces'] == [2, 4] and tr['tipos'] == ['entra', 'sai'], (i1, tr['faces'], tr['tipos'])
        piores = max(piores, abs(desvio_vetorial(tr) - desvio(i1)))
    chk('traçado vetorial (caminho60, i1 14°–88°) × desvio()', piores, 0, 1e-9)
    # v2 (§B.3)
    b = np.linspace(0, 1, 200001)
    t = theta_arco_iris(b)
    chk('arco-íris: máximo de theta_arco_iris / b/R do máximo', [t.max(), b[t.argmax()]], [42.08, .861], [.02, .002])
    _, Dp = projecao_orientacoes()
    no_fundo = int(np.sum((Dp >= d_min() - 1e-9) & (Dp < d_min() + 1)))
    abaixo = int(np.sum(Dp < d_min() - 1e-9))
    ok = no_fundo == 16 and abaixo == 0
    linhas.append(f'[{"OK" if ok else "FALHA"}] projeção 60 orientações (14°–89°): {no_fundo} em [D_min; D_min + 1°) pela regra '
                  f'estrita; {abaixo} abaixo de D_min')
    if not ok:
        falhas.append('projeção')
    # v3 (§B.3): o ângulo no olho entre o Sol e o cristal é o desvio no cristal (raios do Sol paralelos)
    for D in (d_min(), 30.):
        el = 52.                                       # elevação do Sol na cena de lado
        s_ = u(180 - el)                               # direção do Sol (para cima e para a esquerda)
        cr = 7. * u(180 - el - D)                      # cristal a D do Sol, do lado do zênite
        o = rot(-s_, -D)                               # raio que chega (−s) desviado de D
        dist = abs(o[0] * (0 - cr[1]) - o[1] * (0 - cr[0]))
        ang = angulo_no_olho(s_, (0., 0.), cr)
        chk(f'observador D = {D:.2f}°: distância do raio de saída ao olho / ângulo no olho', [dist, ang], [0, D], [1e-6, .01])
    # v5 (§B.7): as cores — o mínimo de cada índice e o i1 onde ele acontece
    chk('d_min(1,3079) / d_min(1,3190) (v6, Warren & Brandt 2008)', [d_min(N_GELO_VERMELHO), d_min(N_GELO_VIOLETA)], [21.68, 22.52], .01)
    iv, ivi = i1_min(N_GELO_VERMELHO), i1_min(N_GELO_VIOLETA)
    gg = np.linspace(30, 52, 22001)
    num_v, num_vi = gg[np.nanargmin(desvio(gg, N_GELO_VERMELHO))], gg[np.nanargmin(desvio(gg, N_GELO_VIOLETA))]
    ok = abs(iv - num_v) < .002 and abs(ivi - num_vi) < .002 and abs(iv - ivi) > .1
    linhas.append(f'[{"OK" if ok else "FALHA"}] i1 no mínimo: vermelho {iv:.3f}° (numérico {num_v:.3f}°), violeta {ivi:.3f}° '
                  f'(numérico {num_vi:.3f}°): mínimos em i1 diferentes, ambos perto de 40,9°')
    if not ok:
        falhas.append('i1 das cores')
    return linhas, falhas


if __name__ == '__main__':
    linhas, falhas = qa()
    txt = '\n'.join(['vid_0031 — checagens da §10 (fisica.py)', *linhas, '', f'falhas: {falhas or "nenhuma"}'])
    pasta = Path(__file__).resolve().parent / 'qa'
    pasta.mkdir(exist_ok=True)
    (pasta / 'checagens.txt').write_text(txt + '\n', encoding='utf-8')
    print(txt)
