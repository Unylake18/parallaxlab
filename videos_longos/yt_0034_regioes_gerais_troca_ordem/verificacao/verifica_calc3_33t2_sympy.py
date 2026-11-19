# Verificação · Cálculo III 3.3-T2 (Regiões gerais e troca da ordem de integração) · proposta v1
# Base: Guidorizzi vol. 3, §3.1, exemplos 4 a 14 e Corolários 1 e 2 (Fubini em regiões entre gráficos).
# Exemplos do vídeo:
#   - quarto de disco de raio 2 (EP. 05/06/08): área pi pela fatia em pé de 0 até sqrt(4 - x^2)
#   - chapa x^2 + y^2 (EP. 05) cortada pela diagonal y = x: 16/3 nas duas ordens (metade de 32/3)
#   - quarto de disco com densidade y: 8/3 nas duas ordens (inverter a curva)
#   - hook: ∫_0^1 ∫_x^1 e^{-y^2} dy dx (Guidorizzi Ex. 8) = (1 - 1/e)/2 trocando a ordem
#   - ∫_0^1 ∫_{sqrt y}^1 sen(x^3) dx dy (Guidorizzi Ex. 9) = (1 - cos 1)/3
#   - telhado: triângulo (-1,0), (0,1), (1,0) (Guidorizzi Ex. 7): uma ordem divide a região, a outra não
#   - metal leve da chapa de dois metais (EP. 06-08): deitado pede 3 faixas
#   - aplicação: o encontro de dois amigos (faixa em volta da diagonal, 7/16)
#   - gancho para o 3.3-E1: reta y = x e parábola y = 4x - x² (Guidorizzi Ex. 12)
import sympy as sp, numpy as np, math
from scipy.integrate import quad, dblquad
from scipy.optimize import brentq
x, y = sp.symbols('x y', real=True)
ok = []
def chk(nome, cond, extra=''):
    ok.append(bool(cond)); print(f'{nome}: {bool(cond)} {extra}')

# ---------- 1. Quarto de disco: a fatia termina na curva ----------
Q1 = sp.integrate(sp.sqrt(4 - x**2), (x, 0, 2))
chk('Q1 área do quarto de disco: ∫_0^2 sqrt(4 - x²) dx = pi', sp.simplify(Q1 - sp.pi) == 0, f'({Q1})')
chk('Q2 fatia em x = 1 tem altura sqrt(3) ≈ 1,732', abs(math.sqrt(3) - 1.7320508) < 1e-6)
# extensão por zero: a integral da fatia de F em [0, 2] é a mesma que de 0 até sqrt(4 - x²)
xs = 1.0
Ffat = quad(lambda t: 1.0 if t*t <= 4 - xs*xs else 0.0, 0, 2, points=[math.sqrt(3)])[0]
chk('Q3 fatia de F (1 dentro, 0 fora) em x = 1 em [0,2] = sqrt(3) (o zero não soma)', abs(Ffat - math.sqrt(3)) < 1e-9, f'({Ffat:.6f})')

# ---------- 2. A chapa x² + y² cortada pela diagonal ----------
f = x**2 + y**2
beta_T = sp.integrate(f, (y, 0, x))
chk('T1 fatia em pé de 0 até x: beta(x) = x³ + x³/3 = 4x³/3', sp.simplify(beta_T - sp.Rational(4, 3)*x**3) == 0, f'({beta_T})')
MT = sp.integrate(beta_T, (x, 0, 2))
chk('T2 massa do triângulo de baixo = 16/3 (metade de 32/3)', MT == sp.Rational(16, 3) and 2*MT == sp.Rational(32, 3))
alpha_T = sp.expand(sp.integrate(f, (x, y, 2)))
chk('T3 deitado de x = y até 2: alpha(y) = 8/3 + 2y² - 4y³/3', sp.simplify(alpha_T - (sp.Rational(8, 3) + 2*y**2 - sp.Rational(4, 3)*y**3)) == 0, f'({alpha_T})')
chk('T4 ∫_0^2 alpha = 16/3 + 16/3 - 16/3 = 16/3', sp.integrate(alpha_T, (y, 0, 2)) == sp.Rational(16, 3)
    and sp.integrate(sp.Rational(8, 3), (y, 0, 2)) == sp.Rational(16, 3) and sp.integrate(2*y**2, (y, 0, 2)) == sp.Rational(16, 3)
    and sp.integrate(sp.Rational(4, 3)*y**3, (y, 0, 2)) == sp.Rational(16, 3))
chk('T5 simetria: f(x,y) = f(y,x), então o triângulo de cima também pesa 16/3', sp.integrate(sp.integrate(f, (y, x, 2)), (x, 0, 2)) == sp.Rational(16, 3))
chk('T6 caso-limite f = 1: área do triângulo = 2 = metade de 4', sp.integrate(sp.integrate(1, (y, 0, x)), (x, 0, 2)) == 2)
print(f'   fatias: beta(1) = {float(beta_T.subs(x, 1)):.4f}, beta(2) = {float(beta_T.subs(x, 2)):.4f}; alpha(0) = {float(alpha_T.subs(y, 0)):.4f}, alpha(1) = {float(alpha_T.subs(y, 1)):.4f}, alpha(2) = {float(alpha_T.subs(y, 2)):.4f}')

# ---------- 3. Quarto de disco com densidade y (inverter a curva) ----------
I_pe = sp.integrate(sp.integrate(y, (y, 0, sp.sqrt(4 - x**2))), (x, 0, 2))
chk('Y1 em pé: ∫_0^2 ∫_0^{sqrt(4-x²)} y dy dx = ∫_0^2 (4 - x²)/2 dx = 8/3', sp.simplify(sp.integrate(y, (y, 0, sp.sqrt(4 - x**2))) - (4 - x**2)/2) == 0 and I_pe == sp.Rational(8, 3))
chk('Y2 inverter: y = sqrt(4 - x²), x, y ≥ 0  ⇔  x = sqrt(4 - y²)', sp.simplify(sp.sqrt(4 - (sp.sqrt(4 - x**2))**2).subs(x, sp.Rational(3, 2)) - sp.Rational(3, 2)) == 0)
I_dt = sp.integrate(sp.integrate(y, (x, 0, sp.sqrt(4 - y**2))), (y, 0, 2))
chk('Y3 deitado: ∫_0^2 y·sqrt(4 - y²) dy = [-(4 - y²)^{3/2}/3]_0^2 = 8/3', I_dt == sp.Rational(8, 3), f'({I_dt})')
chk('Y4 fatia deitada: f = y não depende de x ⇒ integral de dentro = y · comprimento sqrt(4 - y²)', sp.simplify(sp.integrate(y, (x, 0, sp.sqrt(4 - y**2))) - y*sp.sqrt(4 - y**2)) == 0)

# ---------- 4. Hook: e^{-y²} no triângulo (Guidorizzi Ex. 8) ----------
Fp = sp.integrate(sp.exp(-y**2), y)
chk('G1 a primitiva de e^{-y²} não é elementar (sympy devolve erf)', Fp.has(sp.erf), f'({Fp})')
G = sp.integrate(sp.integrate(sp.exp(-y**2), (x, 0, y)), (y, 0, 1))
chk('G2 trocando: ∫_0^1 ∫_0^y e^{-y²} dx dy = ∫_0^1 y e^{-y²} dy = (1 - 1/e)/2', sp.simplify(G - (1 - sp.exp(-1))/2) == 0, f'≈ {float(G):.6f}')
chk('G3 a de dentro deitada: ∫_0^y e^{-y²} dx = y·e^{-y²} (comprimento × altura)', sp.simplify(sp.integrate(sp.exp(-y**2), (x, 0, y)) - y*sp.exp(-y**2)) == 0)
num = dblquad(lambda yy, xx: math.exp(-yy*yy), 0, 1, lambda xx: xx, lambda xx: 1)[0]
chk('G4 ordem original, numérica (dblquad): ≈ 0,316060', abs(num - float(G)) < 1e-9, f'({num:.6f})')
Gor = sp.integrate(sp.integrate(sp.exp(-y**2), (y, x, 1)), (x, 0, 1))
chk('G5 ordem original com erf (sympy) dá o mesmo', abs(float(Gor) - float(G)) < 1e-12)
chk('G6 região lida dos limites: 0 ≤ x ≤ 1, x ≤ y ≤ 1  ⇔  0 ≤ y ≤ 1, 0 ≤ x ≤ y (mesmo triângulo, área 1/2)',
    sp.integrate(sp.integrate(1, (y, x, 1)), (x, 0, 1)) == sp.Rational(1, 2) == sp.integrate(sp.integrate(1, (x, 0, y)), (y, 0, 1)))
errado = sp.integrate(sp.integrate(sp.exp(-y**2), (x, x, 1)), (y, 0, 1))  # só trocar dx dy sem mexer nos limites
chk('G7 erro clássico (só trocar dy dx por dx dy) devolve uma função de x, não um número', errado.has(x), f'({sp.simplify(errado)})')
print(f'   e^-1 = {math.exp(-1):.6f}; fatias deitadas: y e^(-y²) em y = 0,25/0,5/0,75/1: ' +
      ', '.join(f'{v*math.exp(-v*v):.4f}' for v in [0.25, 0.5, 0.75, 1.0]) + f'; máximo em y = 1/sqrt2 ≈ {1/math.sqrt(2):.4f} (valor {math.exp(-0.5)/math.sqrt(2):.4f})')

# ---------- 5. sen(x³) com curva (Guidorizzi Ex. 9) ----------
Sp = sp.integrate(sp.sin(x**3), x)
chk('S1 sen(x³) não tem primitiva elementar (sympy devolve hipergeométrica)', Sp.has(sp.hyper), f'({Sp})')
S = sp.integrate(sp.integrate(sp.sin(x**3), (y, 0, x**2)), (x, 0, 1))
chk('S2 região: 0 ≤ y ≤ 1, sqrt(y) ≤ x ≤ 1  ⇔  0 ≤ x ≤ 1, 0 ≤ y ≤ x²', sp.integrate(sp.integrate(1, (x, sp.sqrt(y), 1)), (y, 0, 1)) == sp.Rational(1, 3) == sp.integrate(x**2, (x, 0, 1)))
chk('S3 trocando: ∫_0^1 x² sen(x³) dx = (1 - cos 1)/3', sp.simplify(S - (1 - sp.cos(1))/3) == 0, f'≈ {float(S):.6f}')
numS = dblquad(lambda xx, yy: math.sin(xx**3), 0, 1, lambda yy: math.sqrt(yy), lambda yy: 1)[0]
chk('S4 ordem original, numérica ≈ 0,153233', abs(numS - float(S)) < 1e-8, f'({numS:.6f})')

# ---------- 6. Telhado (Guidorizzi Ex. 7): uma ordem divide a região ----------
A_dxdy = sp.integrate(sp.integrate(1, (x, y - 1, 1 - y)), (y, 0, 1))
A_e = sp.integrate(sp.integrate(1, (y, 0, 1 + x)), (x, -1, 0)); A_d = sp.integrate(sp.integrate(1, (y, 0, 1 - x)), (x, 0, 1))
chk('R1 deitado (uma conta): ∫_0^1 [(1 - y) - (y - 1)] dy = 1', A_dxdy == 1)
chk('R2 em pé (duas contas, o teto muda de fórmula em x = 0): 1/2 + 1/2 = 1', A_e == sp.Rational(1, 2) and A_d == sp.Rational(1, 2))
My = sp.integrate(sp.integrate(y, (x, y - 1, 1 - y)), (y, 0, 1))
My2 = sp.integrate(sp.integrate(y, (y, 0, 1 + x)), (x, -1, 0)) + sp.integrate(sp.integrate(y, (y, 0, 1 - x)), (x, 0, 1))
chk('R3 com densidade y: 1/3 nas duas ordens (1/6 + 1/6)', My == sp.Rational(1, 3) == My2)
chk('R4 Guidorizzi Ex. 7: ∬ xy no telhado = 0 (simetria) nas duas ordens',
    sp.integrate(sp.integrate(x*y, (x, y - 1, 1 - y)), (y, 0, 1)) == 0 ==
    sp.integrate(sp.integrate(x*y, (y, 0, 1 + x)), (x, -1, 0)) + sp.integrate(sp.integrate(x*y, (y, 0, 1 - x)), (x, 0, 1)))

# ---------- 7. Metal leve da chapa de dois metais deitado: 3 faixas ----------
g = lambda t: 1 + 0.42*math.sin(1.7*t - 0.4)
xm = (math.pi/2 + 0.4)/1.7
A_leve = quad(g, 0, 2)[0]
g0, g2, gm = g(0), g(2), g(xm)
def x1(yy): return brentq(lambda t: g(t) - yy, 0, xm)
def x2(yy): return brentq(lambda t: g(t) - yy, xm, 2)
fx1 = quad(lambda yy: 2 - x1(yy), g0, g2, limit=200)[0]
fx2 = quad(lambda yy: x2(yy) - x1(yy), g2, gm, limit=200)[0]
A_deit = 2*g0 + fx1 + fx2
chk('M1 metal leve em pé: ∫_0^2 g = 2,4721 m² (EP. 08)', abs(A_leve - 2.472143) < 1e-5, f'({A_leve:.6f})')
chk('M2 deitado: faixa cheia (y < 0,836) + 1 corte (0,836–1,059) + 2 cortes (1,059–1,42) = mesma área',
    abs(A_deit - A_leve) < 1e-7, f'({2*g0:.4f} + {fx1:.4f} + {fx2:.4f} = {A_deit:.6f})')
print(f'   g(0) = {g0:.4f}, g(2) = {g2:.4f}, máximo {gm:.4f} em x = {xm:.4f}')

# ---------- 8. Aplicação: o encontro (região em volta da diagonal) ----------
# Dois amigos chegam ao acaso entre 0 e 1 h (densidade uniforme 1 no quadrado); cada um espera 1/4 h.
q = sp.Rational(1, 4)
P_pe = (sp.integrate(sp.integrate(1, (y, 0, x + q)), (x, 0, q)) + sp.integrate(sp.integrate(1, (y, x - q, x + q)), (x, q, 1 - q))
        + sp.integrate(sp.integrate(1, (y, x - q, 1)), (x, 1 - q, 1)))
chk('L1 encontro: P(|x - y| ≤ 1/4) = 1 - (3/4)² = 7/16, em pé com 3 pedaços', P_pe == sp.Rational(7, 16) == 1 - (1 - q)**2, f'(≈ {float(P_pe):.4f})')
P_dt = (sp.integrate(sp.integrate(1, (x, 0, y + q)), (y, 0, q)) + sp.integrate(sp.integrate(1, (x, y - q, y + q)), (y, q, 1 - q))
        + sp.integrate(sp.integrate(1, (x, y - q, 1)), (y, 1 - q, 1)))
chk('L2 a mesma probabilidade deitado', P_dt == sp.Rational(7, 16))

# ---------- 9. Gancho (3.3-E1): reta y = x e parábola y = 4x - x² (Guidorizzi Ex. 12) ----------
A_pe = sp.integrate(sp.integrate(1, (y, x, 4*x - x**2)), (x, 0, 3))
xe = 2 - sp.sqrt(4 - y); xd = 2 + sp.sqrt(4 - y)
chk('K1 inverter y = 4x - x²: x = 2 ∓ sqrt(4 - y) (os dois ramos)', sp.simplify((4*xe - xe**2) - y) == 0 and sp.simplify((4*xd - xd**2) - y) == 0)
A_dt = sp.integrate(y - xe, (y, 0, 3)) + sp.integrate(xd - xe, (y, 3, 4))
chk('K2 área 9/2: em pé uma conta; deitado 0 ≤ y ≤ 3 (sai na reta) + 3 ≤ y ≤ 4 (sai no ramo direito)', A_pe == sp.Rational(9, 2) and sp.simplify(A_dt - sp.Rational(9, 2)) == 0)

print(f'\n{sum(ok)} de {len(ok)} checagens True')
