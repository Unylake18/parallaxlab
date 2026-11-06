"""vid_0033 — física do gás ideal (funções puras + asserts). Roda sozinho: uv run python videos/vid_0033_pvnrt/fisica.py → qa/checagens.txt

Unidades da CENA (3D): caixa [-1, 1]^3 (L = 2), massa m = 1, velocidades em u/s de vídeo. Unidades SI nas checagens físicas.
Posição por eixo = onda triangular da coordenada "desdobrada" s = s0 + v·τ (colisões elásticas, sem colisão molécula–molécula):
x = −1 + tri(s), tri(s) = 2 − |(s mod 4) − 2|; a velocidade é +v se (s mod 4) < 2, senão −v. Batida na parede +x: s ≡ 2 (mod 4).
"""
from pathlib import Path

import numpy as np

KB = 1.380649e-23          # J/K (exato, SI 2019)
NA = 6.02214076e23         # 1/mol (exato)
R = KB * NA                # 8,314 J/(mol·K)
U = 1.66053906660e-27      # kg
M_N2, M_HE, M_O2 = 28.0134 * U, 4.002602 * U, 31.998 * U
ATM = 101325.0

L, N_MOL = 2.0, 48         # cena
SEMENTE_C04 = 15          # amostra das barras do C04 (achada por escolhe_semente())
SEMENTE_3D = 33


def v_rms(m, T):
    return float(np.sqrt(3 * KB * T / m))


def amostra(n=200_000, m=M_N2, T=300., semente=SEMENTE_C04):
    """Componentes gaussianas independentes de variância kB·T/m (m/s). Forma (n, 3)."""
    return np.random.default_rng(semente).normal(0., np.sqrt(KB * T / m), size=(n, 3))


def medias_prefixo(v, ns):
    """⟨vx²⟩, ⟨vy²⟩, ⟨vz²⟩ das primeiras n moléculas, em unidades de kB·T/m (adimensional), para cada n em ns."""
    sig2 = KB * 300. / M_N2
    q = v ** 2 / sig2
    return {n: q[:n].mean(axis=0).tolist() for n in ns}


def pressao(v, m, V):
    return len(v) * m * float((v ** 2).sum(axis=1).mean()) / (3 * V)


def tri(s):
    return 2. - np.abs(np.mod(s, 4.) - 2.)


def pos_vel(s0, sp, tau):
    """Posição e velocidade (por eixo) da molécula no instante τ; s0, sp: arrays (...,3) (s0 em [0,4), sp > 0)."""
    s = s0 + sp * tau
    return -1. + tri(s), np.where(np.mod(s, 4.) < 2., 1., -1.) * sp


def conjunto_3d(semente=SEMENTE_3D, n=N_MOL):
    """Estado inicial das n moléculas da cena: s0 (n,3) e velocidade por eixo sp (n,3) (u/s). A molécula 0 é a acompanhada."""
    rng = np.random.default_rng(semente)
    sp = np.abs(rng.normal(0., 1.0, size=(n, 3)))
    s0 = rng.uniform(0., 4., size=(n, 3))
    sp[0] = (1.9, .75, .55)                          # acompanhada: vx dominante, mas não único
    s0[0] = (0., 1.1, 2.6)                           # o instante da 1ª batida é ajustado em gerar_timeline.py (s0x)
    return s0, sp


def tempos_batida_x(s0x, spx, t_max):
    """Instantes τ das batidas na parede +x (s ≡ 2 mod 4), de 0 a t_max."""
    t = (2. - (s0x % 4.)) / spx
    t = t if t >= 0 else t + 4. / spx
    out = []
    while t <= t_max:
        out.append(t)
        t += 4. / spx
    return out


def impulso_simulado(s0, sp, T, m=1.):
    """Soma do impulso 2m|vx| das batidas na parede +x até T, dividido por área·T; devolve (simulado, teórico Σ m vx²/V)."""
    imp = 0.
    for i in range(len(s0)):
        imp += 2 * m * sp[i, 0] * len(tempos_batida_x(s0[i, 0], sp[i, 0], T))
    area, V = L * L, L ** 3
    return imp / (area * T), float((m * sp[:, 0] ** 2).sum() / V)


def escolhe_semente():
    """Procura semente cujas médias do prefixo sejam bem diferentes com n = 1 e 5 e quase iguais com n grande (só para a didática)."""
    ns = (1, 5, 50, 500, 5000, 200000)
    for s in range(1, 400):
        d = medias_prefixo(amostra(semente=s), ns)
        ok = (max(d[1]) <= 2.6 and max(d[1]) - min(d[1]) >= 1.2 and max(d[5]) - min(d[5]) >= .45
              and max(d[50]) - min(d[50]) >= .15 and max(d[500]) - min(d[500]) <= .12 and max(d[5000]) - min(d[5000]) <= .05)
        if ok:
            return s
    return None


def tres_moleculas(v):
    """Índices (nas primeiras 200 da amostra) de uma molécula quase toda em x, outra em y e outra equilibrada."""
    q = v[:200] ** 2
    f = q / q.sum(axis=1, keepdims=True)
    return int(np.argmax(f[:, 0])), int(np.argmax(f[:, 1])), int(np.argmin(f.max(axis=1)))


def checagens():
    out = []

    def ok(cond, msg):
        assert cond, msg
        out.append('OK  ' + msg)

    T = 300.
    V = R * T / ATM
    ok(abs(V * 1e3 - 24.6) < .1, f'1 mol, 300 K, 1 atm: V = {V * 1e3:.2f} L (24,6 ± 0,1)')
    ok(abs(v_rms(M_N2, T) - 517) <= 1, f'v_rms(N2, 300 K) = {v_rms(M_N2, T):.1f} m/s (517 ± 1)')
    ok(abs(v_rms(M_HE, T) - 1367) <= 3, f'v_rms(He) = {v_rms(M_HE, T):.0f} m/s (≈ 1367)')
    ok(abs(v_rms(M_O2, T) - 484) <= 2, f'v_rms(O2) = {v_rms(M_O2, T):.0f} m/s (≈ 484)')
    v = amostra()
    razao = float((v[:, 0] ** 2).mean() / (v ** 2).sum(axis=1).mean())
    ok(abs(razao - 1 / 3) <= .005, f'⟨vx²⟩/⟨v²⟩ = {razao:.4f} (1/3 ± 0,005; 200 000 moléculas, semente {SEMENTE_C04})')
    N1 = NA * 1.
    P = N1 * M_N2 * float((v ** 2).sum(axis=1).mean()) / (3 * V)      # N de verdade; ⟨v²⟩ da amostra
    ok(abs(P / ATM - 1) < .01, f'P = N m ⟨v²⟩/(3V) = {P:.0f} Pa (101 325 ± 1 %)')
    Ec = 1.5 * KB * T
    ok(abs(Ec - 6.2e-21) / 6.2e-21 < .01, f'⟨Ec⟩ = 3kBT/2 = {Ec:.3e} J por molécula (6,2e-21 ± 1 %)')
    ok(abs(R - 8.314) < .001, f'R = NA·kB = {R:.4f} J/(mol·K)')
    ok(abs(pressao(v, M_N2, V) * V - len(v) * M_N2 * (v ** 2).sum(axis=1).mean() / 3) < 1e-9, 'PV = ⅓ N m ⟨v²⟩ (identidade na amostra)')
    # PV ∝ N, e P ∝ 1/V
    ok(abs(2 * 1 / (1 / 2) - 4) < 1e-12 and abs(pressao(v, M_N2, V / 2) / pressao(v, M_N2, V) - 2) < 1e-12, 'V/2 com N, T fixos ⇒ P × 2')
    ok(abs(pressao(np.vstack([v, v]), M_N2, V) / pressao(v, M_N2, V) - 2) < 1e-12, '2N com V, T fixos ⇒ P × 2 (mesma ⟨v²⟩)')
    # termômetro de gás (C05): 1 mol, 1 atm; PV/N em joules e PV/(N·T) = kB em três temperaturas
    for T_, Vlit, pvn in ((273.15, 22.41, 3.77e-21), (300., 24.62, 4.14e-21), (373.15, 30.62, 5.15e-21)):
        V_ = R * T_ / ATM
        ok(abs(V_ * 1e3 - Vlit) < .02, f'1 mol, {T_:g} K, 1 atm: V = {V_ * 1e3:.2f} L ({Vlit} ± 0,02)')
        ok(abs(ATM * V_ / NA / pvn - 1) < .005, f'PV/N = {ATM * V_ / NA:.4e} J ({pvn:.2e} ± 0,5 %)')
        ok(abs(ATM * V_ / (NA * T_) / KB - 1) < 1e-4, f'PV/(N·T) = {ATM * V_ / (NA * T_):.5e} J/K = kB ({KB:.5e}; 1e-4 relativo)')
    ok(abs(NA * KB - 8.3145) < .001, f'R = NA·kB = {NA * 1.381e-23:.3f} com kB = 1,381e-23 (conta na tela: 6,022e23 × 1,381e-23 = 8,316); exato: {NA * KB:.4f} J/(mol·K)')
    # impulso simulado na cena 3D
    s0, sp = conjunto_3d()
    Tl = 200 * 4. / sp[:, 0].min()
    sim, teo = impulso_simulado(s0, sp, Tl)
    ok(abs(sim / teo - 1) < .02, f'impulso simulado na cena: {sim:.4f} vs Σ m vx²/V = {teo:.4f} (dif. {100 * abs(sim / teo - 1):.2f} %; T = {Tl:.0f} s ≥ 200 travessias da mais lenta)')
    return out


if __name__ == '__main__':
    linhas = checagens()
    s = escolhe_semente()
    linhas.append(f'semente das barras do C04 achada na busca: {s} (usada: {SEMENTE_C04})')
    v = amostra()
    linhas.append('médias (kBT/m) por n: ' + str({n: [round(x, 3) for x in d] for n, d in medias_prefixo(v, (1, 5, 50, 500, 5000, 200000)).items()}))
    linhas.append('três moléculas (x, y, equilibrada): ' + str(tres_moleculas(v)))
    texto = '\n'.join(linhas)
    print(texto)
    (Path(__file__).parent / 'qa' / 'checagens.txt').write_text(texto + '\n', encoding='utf-8')
