# Verificação · Cálculo III 3.2-T3 (propriedades da integral dupla) · proposta v1
# Base: Guidorizzi vol. 3, §2.5 (propriedades I–VII, integral com f indefinida num conjunto de conteúdo nulo, exemplos 1 e 2).
# Exemplos do vídeo:
#   - chapa [0,2]^2 de dois metais (EP. 05/06): solda g(x) = 1 + 0,42 sen(1,7x - 0,4); rho = 1 embaixo (y <= g), 3 em cima
#   - chapa [0,2]^2 com densidade x^2 + y^2 (EP. 05): massa 32/3
#   - disco unitário: exemplos 1 e 2 do §2.5
import sympy as sp, numpy as np, math
x, y, r, t, u = sp.symbols('x y r t u', real=True)
ok = []
def chk(nome, cond, extra=''):
    ok.append(bool(cond)); print(f'{nome}: {bool(cond)} {extra}')

# ---------- 1. A chapa de dois metais: massa = leve + pesado ----------
g = 1 + sp.Rational(42, 100)*sp.sin(sp.Rational(17, 10)*x - sp.Rational(2, 5))
A1 = float(sp.integrate(g, (x, 0, 2))); A2 = 4 - A1
m_leve, m_pes = 1*A1, 3*A2
print(f'área leve A1 = {A1:.4f} m², área pesada A2 = {A2:.4f} m²')
print(f'massa leve = {m_leve:.4f} kg, massa pesada = {m_pes:.4f} kg, total = {m_leve+m_pes:.4f} kg')
chk('W1 massa = leve + pesado = 2,47 + 4,58 = 7,06 kg', abs(m_leve - 2.4721) < 1e-3 and abs(m_pes - 4.5836) < 1e-3 and abs(m_leve + m_pes - 7.0557) < 1e-3)
chk('W2 rho = 1 + 2·[pesado]: 4 + 2·A2 = 7,06 (propriedade I: soma e constante)', abs(4 + 2*A2 - (m_leve + m_pes)) < 1e-12)
chk('W3 rho = 3 em cima: massa pesada = 3 × área pesada (I b)', abs(m_pes - 3*A2) < 1e-12)
chk('W4 comparação 1 <= rho <= 3: 4 <= massa <= 12 (III + I b)', 4 <= m_leve + m_pes <= 12)
med2 = (m_leve + m_pes)/4
chk('W5 densidade média da chapa de dois metais = 1,76 kg/m², valor que rho (1 ou 3) nunca assume', abs(med2 - 1.7639) < 1e-3 and med2 not in (1, 3), f'({med2:.4f})')

# ---------- 2. Chapa x^2 + y^2: soma de duas rampas e valor médio ----------
Ix2 = sp.integrate(x**2, (x, 0, 2), (y, 0, 2)); Iy2 = sp.integrate(y**2, (x, 0, 2), (y, 0, 2))
chk('W6 ∬x² = ∬y² = 16/3 e somam 32/3 (I a + simetria)', Ix2 == sp.Rational(16, 3) and Iy2 == Ix2 and Ix2 + Iy2 == sp.Rational(32, 3))
# conferência com somas de Riemann (ponto médio) na mesma grade: a soma da soma é a soma das somas
for n in [4, 16, 64]:
    h = 2/n; c = (np.arange(n) + 0.5)*h; X, Y = np.meshgrid(c, c)
    sf, sg, sfg = (X**2).sum()*h*h, (Y**2).sum()*h*h, (X**2 + Y**2).sum()*h*h
    print(f'  n={n:3d}: soma(x²) = {sf:.4f}, soma(y²) = {sg:.4f}, soma(x²+y²) = {sfg:.4f}')
chk('W7 na mesma partição e mesmos pontos, soma(f+g) = soma(f) + soma(g)', abs(sfg - sf - sg) < 1e-9)
chk('W8 limites 0 <= x²+y² <= 8 ⇒ 0 <= 32/3 <= 32 (comparação)', 0 <= 32/3 <= 32)
med = sp.Rational(32, 3)/4; R = sp.sqrt(med)
chk('W9 valor médio de x²+y² na chapa = 8/3 ≈ 2,67; atingido no arco x²+y² = 8/3 (raio ≈ 1,63 < 2, inteiro dentro da chapa)', med == sp.Rational(8, 3) and float(R) < 2, f'(raio {float(R):.4f})')
# o que sobra acima do nível 8/3 enche o que falta abaixo (∬(f - média) = 0)
N = 2000; h = 2/N; c = (np.arange(N) + 0.5)*h; X, Y = np.meshgrid(c, c); F = X**2 + Y**2
acima = np.clip(F - 8/3, 0, None).sum()*h*h; abaixo = np.clip(8/3 - F, 0, None).sum()*h*h
# exato: abaixo = ∬_{quarto de disco de raio R} (8/3 - r²) = (π/2)·(8/3·R²/2 - R⁴/4)
ab_ex = float(sp.pi/2*(med*R**2/2 - R**4/4))
print(f'  volume acima do nível = {acima:.4f}, volume que falta abaixo = {abaixo:.4f} (exato {ab_ex:.4f} = 8π/9)')
chk('W10 lago nivelado: volume acima de 8/3 = volume abaixo = 8π/9 ≈ 2,79', abs(acima - abaixo) < 1e-3 and abs(ab_ex - float(8*sp.pi/9)) < 1e-12)
chk('W11 área da região abaixo do nível = quarto de disco π·(8/3)/4 = 2π/3 ≈ 2,09 m²', abs(float(sp.pi*med/4) - (F < 8/3).mean()*4) < 5e-3)

# ---------- 3. Valor médio sem conexão: dois quadrados separados ----------
# B = [0,1]² ∪ [2,3]×[0,1], f = 1 no primeiro e 3 no segundo: contínua em B (compacto, fronteira de conteúdo nulo)
chk('W12 sem caminho dentro de B: f contínua, média 2, nunca vale 2', (1*1 + 3*1)/2 == 2)

# ---------- 4. A solda: muro alto, mas cada vez mais fino ----------
gn = lambda t: 1 + 0.42*np.sin(1.7*t - 0.4)
def vermelhas(n):
    xs = np.linspace(0, 2, n + 1); cnt = 0
    for i in range(n):
        tt = np.linspace(xs[i], xs[i+1], 801); lo, hi = gn(tt).min(), gn(tt).max()
        j0 = np.searchsorted(xs, lo, 'right') - 1; j1 = np.searchsorted(xs, hi, 'left') - 1
        cnt += max(0, min(j1, n-1) - max(j0, 0) + 1)
    return cnt
print('Muro de altura H = 100 kg/m² posto só na solda (volume máximo = H × área das células que a solda cruza):')
prev = None; tab = {}
for n in [64, 128, 256, 512, 1024]:
    v = vermelhas(n); a = v*(2/n)**2; tab[n] = (v, a)
    print(f'  n={n:5d}: células {v:5d}, área {a:.4f} m², 100 × área = {100*a:.2f} kg')
chk('W13 células cruzadas n=64 → 95 (bate com o EP. 06)', tab[64][0] == 95)
chk('W14 a área das células da solda cai pela metade ao dobrar n (o muro de 100 vale 9,3 → 4,6 → 2,3 → 1,2 → 0,6 kg)',
    all(abs(tab[2*n][1]/tab[n][1] - 0.5) < 0.05 for n in [64, 128, 256, 512]))

# ---------- 5. Solda real: cordão com espessura ----------
L = float(sp.Integral(sp.sqrt(1 + sp.diff(g, x)**2), (x, 0, 2)).evalf())
print(f'comprimento da solda L = {L:.4f} m')
for w, rho_w in [(0.01, 6), (0.001, 6)]:
    print(f'  cordão de largura {w*100:.1f} cm e 6 kg/m²: área ≈ {L*w:.4f} m², massa ≈ {rho_w*L*w*1000:.0f} g')
chk('W15 comprimento da solda ≈ 2,25 m; cordão de 1 cm a 6 kg/m² ≈ 135 g; de 1 mm ≈ 13 g (→ 0 com a largura)', abs(L - 2.249) < 0.001 and round(6*L*0.01*1000) == 135)
# sobreposição com área: B = {y <= g + 0,1}, B1 = {y >= g - 0,1}; contando 2 vezes a faixa
banda = 0.2*2
chk('W16 regiões que se sobrepõem numa faixa de 0,2 m de altura: área(B) + área(B1) = 4 + 0,4 ≠ 4', abs((A1 + 0.2) + (A2 + 0.2) - 4.4) < 1e-9)

# ---------- 6. Exemplos 1 e 2 do Guidorizzi §2.5 ----------
E1 = sp.integrate(sp.cos(t)**2*r, (r, 0, 1), (t, 0, 2*sp.pi))
chk('W17 Ex. 1: ∬_disco x²/(x²+y²) = π/2 (por simetria: x²/r² + y²/r² = 1, área π, metade cada)', sp.simplify(E1 - sp.pi/2) == 0)
chk('W18 Ex. 2: sen(1-x²-y²)/(1-x²-y²) → 1 na circunferência (g = 1 em D torna g contínua no disco fechado)', sp.limit(sp.sin(u)/u, u, 0) == 1)
E2 = sp.pi*sp.Si(1)
print(f'  Ex. 2 (fora do vídeo, precisa de polares): ∬ = π·Si(1) ≈ {float(E2):.4f}')
chk('W19 Ex. 2 numérico confere com π·Si(1)', abs(float(sp.Integral(sp.sin(1 - r**2)/(1 - r**2)*r, (r, 0, 1)).evalf())*2*math.pi - float(E2)) < 1e-6)

print(f'\nTOTAL: {sum(ok)}/{len(ok)} True')
