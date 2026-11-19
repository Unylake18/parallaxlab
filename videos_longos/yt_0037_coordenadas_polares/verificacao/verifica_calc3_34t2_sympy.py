# Verificação · Cálculo III 3.4-T2 (Coordenadas polares na integral dupla) · proposta v1
# Base: Guidorizzi vol. 3, §4.1 (Exemplo: retângulo polar) e §4.2 (teorema de mudança de variáveis;
#       Ex. 2 semicírculo, Ex. 5 integral de Gauss pelo confronto, Ex. 8 elipse, Ex. 9 polares deslocadas).
# Didática do Stewart (§15.3): retângulo polar como diferença de setores (exato com o raio médio),
#       disco deslocado r = 2 cos θ, volume por polares.
# Notação da série: polares (r, θ), dA = r dr dθ (ρ continua sendo densidade).
import sympy as sp, numpy as np, math
from scipy.integrate import quad, dblquad
r, th, R, a, b, u, x, y, vmax = sp.symbols('r theta R a b u x y v_max', positive=True)
ok = []
def chk(nome, cond, extra=''):
    ok.append(bool(cond)); print(f'{nome}: {bool(cond)} {extra}')

# ---------- H1 · gancho do 3.4-T1: disco unitário, e^(-(x²+y²)) ----------
inner = sp.integrate(sp.exp(-r**2)*r, (r, 0, 1))
chk('H1 de dentro: ∫_0^1 e^(-r²) r dr = (1 - 1/e)/2 (o mesmo número do sino do EP. 09)',
    sp.simplify(inner - (1 - sp.exp(-1))/2) == 0, f'({sp.N(inner, 6)})')
# conta inteira por u = r², du = 2r dr, limites 0 -> 1
inner_u = sp.integrate(sp.exp(-u)/2, (u, 0, 1))
chk('H1 u = r²: ∫_0^1 e^(-u) du/2 = [-e^(-u)/2]_0^1 = -1/(2e) + 1/2', sp.simplify(inner_u - (-sp.exp(-1)/2 + sp.Rational(1, 2))) == 0)
H1 = sp.integrate(inner, (th, 0, 2*sp.pi))
chk('H1 ∬_disco e^(-(x²+y²)) dA = 2π · (1 - 1/e)/2 = π(1 - 1/e) ≈ 1,9859', sp.simplify(H1 - sp.pi*(1 - sp.exp(-1))) == 0, f'({float(H1):.4f})')
num = dblquad(lambda yy, xx: math.exp(-(xx*xx + yy*yy)), -1, 1, lambda xx: -math.sqrt(1 - xx*xx), lambda xx: math.sqrt(1 - xx*xx))[0]
chk('H1 numérica em xy (dblquad) = π(1 - 1/e)', abs(num - float(H1)) < 1e-8, f'({num:.6f})')
chk('H1 EP. 09: ∫_0^1 y e^(-y²) dy é a MESMA integral de dentro', sp.simplify(sp.integrate(y*sp.exp(-y**2), (y, 0, 1)) - inner) == 0)
# por que trava em xy: a de dentro é e^(-x²) ∫ e^(-y²) dy, sem primitiva elementar
Fy = sp.integrate(sp.exp(-y**2), y)
chk('H1 trava em xy: primitiva de e^(-y²) não é elementar (sympy devolve erf)', Fy.has(sp.erf), f'({Fy})')

# ---------- B1 · coordenadas polares ----------
X, Y = r*sp.cos(th), r*sp.sin(th)
chk('B1 x² + y² = r² (Pitágoras no triângulo)', sp.simplify(X**2 + Y**2 - r**2) == 0)
chk('B1 θ = π/3, r = 2: ponto (1, √3)', (X.subs({r: 2, th: sp.pi/3}), Y.subs({r: 2, th: sp.pi/3})) == (1, sp.sqrt(3)))

# ---------- B2 · o retângulo polar ----------
r1, r2, dth = sp.symbols('r1 r2 Delta_theta', positive=True)
setor = lambda rr: sp.pi*rr**2*dth/(2*sp.pi)
chk('B2 setor de raio r e ângulo Δθ: πr² · Δθ/(2π) = r²Δθ/2', sp.simplify(setor(r) - r**2*dth/2) == 0)
cel = sp.simplify(setor(r2) - setor(r1))
chk('B2 célula = (r2² - r1²)Δθ/2 = (r2 + r1)(r2 - r1)Δθ/2 = r̄ Δr Δθ EXATO', sp.simplify(cel - (r1 + r2)/2*(r2 - r1)*dth) == 0)
c_in = ((r1 + r2)/2*(r2 - r1)*dth).subs({r1: sp.Rational(1, 2), r2: 1, dth: sp.pi/6})
c_out = ((r1 + r2)/2*(r2 - r1)*dth).subs({r1: sp.Rational(3, 2), r2: 2, dth: sp.pi/6})
chk('B2 Δr = 0,5 e Δθ = π/6: célula de 0,5 a 1 = 3/4 · 1/2 · π/6 = π/16 ≈ 0,196', sp.simplify(c_in - sp.pi/16) == 0, f'({float(c_in):.4f})')
chk('B2 célula de 1,5 a 2 = 7/4 · 1/2 · π/6 = 7π/48 ≈ 0,458; razão 7/3', sp.simplify(c_out - 7*sp.pi/48) == 0 and sp.simplify(c_out/c_in) == sp.Rational(7, 3), f'({float(c_out):.4f})')
J = sp.Matrix([[sp.diff(X, r), sp.diff(X, th)], [sp.diff(Y, r), sp.diff(Y, th)]])
chk('B2 matriz jacobiana [[cos θ, -r sen θ], [sen θ, r cos θ]]', J == sp.Matrix([[sp.cos(th), -r*sp.sin(th)], [sp.sin(th), r*sp.cos(th)]]))
detJ = J.det()
chk('B2 det = r cos²θ + r sen²θ = r(cos²θ + sen²θ) = r', sp.expand(detJ) == sp.expand(r*sp.cos(th)**2 + r*sp.sin(th)**2) and sp.simplify(detJ - r) == 0)
chk('B2 erro clássico: ∫_0^{2π}∫_0^R dr dθ = 2πR (perímetro, não área)', sp.integrate(sp.integrate(1, (r, 0, R)), (th, 0, 2*sp.pi)) == 2*sp.pi*R)
chk('B2 certo: ∫_0^{2π}∫_0^R r dr dθ = ∫_0^{2π} R²/2 dθ = πR²', sp.integrate(r, (r, 0, R)) == R**2/2 and sp.integrate(sp.integrate(r, (r, 0, R)), (th, 0, 2*sp.pi)) == sp.pi*R**2)

# ---------- B3 · hipóteses do teorema em polares ----------
# no interior (r > 0, 0 < θ < 2π) φ é injetora e o jacobiano r ≠ 0; na borda r = 0 tudo cai na origem
chk('B3 borda r = 0 vai inteira para a origem (o jacobiano zera só ali)', (X.subs(r, 0), Y.subs(r, 0)) == (0, 0) and detJ.subs(r, 0) == 0)
chk('B3 bordas θ = 0 e θ = 2π caem no mesmo segmento do eixo x', sp.simplify(X.subs(th, 0) - X.subs(th, 2*sp.pi)) == 0 and sp.simplify(Y.subs(th, 2*sp.pi)) == 0)

# ---------- B4 · semicírculo (Guidorizzi Ex. 2) ----------
in4 = sp.integrate(sp.sin(r**2)*r, (r, 0, 1))
chk('B4 u = r²: ∫_0^1 sen(r²) r dr = ½∫_0^1 sen u du = ½[-cos u]_0^1 = ½(1 - cos 1)', sp.simplify(in4 - (1 - sp.cos(1))/2) == 0
    and sp.simplify(sp.integrate(sp.sin(u)/2, (u, 0, 1)) - (-sp.cos(1)/2 + sp.cos(0)/2)) == 0)
S4 = sp.integrate(in4, (th, 0, sp.pi))
chk('B4 ∬ sen(x² + y²) no semicírculo = π/2 · (1 - cos 1) ≈ 0,7221', sp.simplify(S4 - sp.pi/2*(1 - sp.cos(1))) == 0, f'({float(S4):.4f})')
num4 = dblquad(lambda yy, xx: math.sin(xx*xx + yy*yy), -1, 1, lambda xx: 0, lambda xx: math.sqrt(1 - xx*xx))[0]
chk('B4 numérica em xy igual', abs(num4 - float(S4)) < 1e-8, f'({num4:.6f})')
chk('B4 conferência f = 1: ∫_0^π∫_0^1 r dr dθ = π · ½ = π/2 (meio disco)', sp.integrate(sp.integrate(r, (r, 0, 1)), (th, 0, sp.pi)) == sp.pi/2)
chk('B4 trava em xy: ∫ sen(x² + y²) dy não é elementar', sp.integrate(sp.sin(sp.Rational(1, 4) + y**2), y).has(sp.fresnels) or sp.integrate(sp.sin(sp.Rational(1, 4) + y**2), y).has(sp.fresnelc))

# ---------- B5 · volume da esfera por cascas ----------
in5 = sp.integrate(sp.sqrt(R**2 - r**2)*r, (r, 0, R))
chk('B5 u = R² - r², du = -2r dr, r: 0→R ⇒ u: R²→0: ∫_{R²}^0 √u (-du/2) = ½∫_0^{R²} √u du = ½ · ⅔ R³ = R³/3',
    sp.simplify(in5 - R**3/3) == 0 and sp.simplify(sp.integrate(sp.sqrt(u)*(-sp.Rational(1, 2)), (u, R**2, 0)) - R**3/3) == 0
    and sp.simplify(sp.Rational(1, 2)*sp.Rational(2, 3)*(R**2)**sp.Rational(3, 2) - R**3/3) == 0)
V5 = 2*sp.integrate(in5, (th, 0, 2*sp.pi))
chk('B5 V = 2 · 2π · R³/3 = 4πR³/3', sp.simplify(V5 - 4*sp.pi*R**3/3) == 0)
chk('B5 casca: altura total 2√(R² - r²), comprimento 2πr, espessura dr', sp.simplify(sp.integrate(2*sp.sqrt(R**2 - r**2)*2*sp.pi*r, (r, 0, R)) - 4*sp.pi*R**3/3) == 0)

# ---------- B6 · disco deslocado x² + y² ≤ 2x (Stewart; centro (1,0), raio 1) ----------
chk('B6 x² + y² ≤ 2x ⇔ (x - 1)² + y² ≤ 1', sp.expand((x - 1)**2 + y**2 - 1 - (x**2 + y**2 - 2*x)) == 0)
chk('B6 em polares: r² ≤ 2r cos θ ⇒ r ≤ 2 cos θ (r > 0), θ ∈ [-π/2, π/2]', sp.simplify((X**2 + Y**2 - 2*X).subs(r, 2*sp.cos(th))) == 0)
chk('B6 θ = π/3 ⇒ r = 1 ⇒ ponto (1/2, √3/2) está na circunferência', sp.simplify(((X - 1)**2 + Y**2).subs({r: 1, th: sp.pi/3}) - 1) == 0)
A6 = sp.integrate(sp.integrate(r, (r, 0, 2*sp.cos(th))), (th, -sp.pi/2, sp.pi/2))
chk('B6 área: ∫ [r²/2]_0^{2cos θ} dθ = ∫ 2cos²θ dθ = ∫ (1 + cos 2θ) dθ = [θ + sen 2θ/2] = π', sp.simplify(A6 - sp.pi) == 0
    and sp.simplify(sp.integrate(1 + sp.cos(2*th), (th, -sp.pi/2, sp.pi/2)) - sp.pi) == 0)
D6 = sp.integrate(sp.integrate(r*r, (r, 0, 2*sp.cos(th))), (th, -sp.pi/2, sp.pi/2))
chk('B6 ∬ √(x² + y²) dA = ∫ (8/3)cos³θ dθ = (8/3)(4/3) = 32/9', sp.simplify(D6 - sp.Rational(32, 9)) == 0
    and sp.integrate(1 - u**2, (u, -1, 1)) == sp.Rational(4, 3))
num6 = dblquad(lambda yy, xx: math.hypot(xx, yy), 0, 2, lambda xx: -math.sqrt(max(0.0, 1 - (xx - 1)**2)), lambda xx: math.sqrt(max(0.0, 1 - (xx - 1)**2)))[0]
chk('B6 numérica em xy = 32/9', abs(num6 - 32/9) < 1e-7, f'({num6:.6f})')
chk('B6 distância média da margem = 32/(9π) ≈ 1,1318 raio', abs(32/(9*math.pi) - 1.1318) < 1e-4, f'({32/(9*math.pi):.4f})')
# quando NÃO usar polares: quadrado [0,1]², ∬ xy
chk('B6 quadrado: ∫_0^1 x [y²/2]_0^1 dx = ∫ x/2 dx = 1/4', sp.integrate(sp.integrate(x*y, (y, 0, 1)), (x, 0, 1)) == sp.Rational(1, 4))
pol = quad(lambda t: quad(lambda rr: rr**3*math.cos(t)*math.sin(t), 0, 1/math.cos(t))[0], 0, math.pi/4)[0] + \
      quad(lambda t: quad(lambda rr: rr**3*math.cos(t)*math.sin(t), 0, 1/math.sin(t))[0], math.pi/4, math.pi/2)[0]
chk('B6 o mesmo quadrado em polares exige dividir em θ = π/4 (r até sec θ e até cossec θ); numérica 1/4', abs(pol - 0.25) < 1e-9)

# ---------- B7 · integral de Gauss (Guidorizzi Ex. 5, confronto) ----------
disco = lambda A: sp.integrate(sp.integrate(sp.exp(-r**2)*r, (r, 0, A)), (th, 0, 2*sp.pi))
chk('B7 disco de raio A: π(1 - e^(-A²))', sp.simplify(disco(a) - sp.pi*(1 - sp.exp(-a**2))) == 0)
chk('B7 círculo circunscrito ao quadrado [-R, R]² tem raio R√2 (meia diagonal)', sp.sqrt(R**2 + R**2) == sp.sqrt(2)*R)
chk('B7 disco de raio R√2: π(1 - e^(-2R²))', sp.simplify(disco(sp.sqrt(2)*R) - sp.pi*(1 - sp.exp(-2*R**2))) == 0)
I = lambda RR: quad(lambda t: math.exp(-t*t), -RR, RR)[0]
chk('B7 Fubini: ∬_quadrado e^(-x²)e^(-y²) = I(R)² (R = 1, numérica)', abs(dblquad(lambda yy, xx: math.exp(-xx*xx - yy*yy), -1, 1, -1, 1)[0] - I(1)**2) < 1e-10)
tab = []
for RR in (1, 2, 3):
    lo, hi = math.pi*(1 - math.exp(-RR*RR)), math.pi*(1 - math.exp(-2*RR*RR))
    tab.append((RR, lo, I(RR)**2, hi));
chk('B7 confronto vale para R = 1, 2, 3', all(lo <= m <= hi for _, lo, m, hi in tab),
    ' | '.join(f'R={RR}: {lo:.4f} ≤ {m:.4f} ≤ {hi:.4f}' for RR, lo, m, hi in tab))
chk('B7 I(1) ≈ 1,4936 · I(2) ≈ 1,7642 · I(3) ≈ 1,7724; √π ≈ 1,7725', abs(I(1) - 1.4936) < 1e-4 and abs(I(2) - 1.7642) < 1e-4 and abs(I(3) - 1.7724) < 1e-4)
chk('B7 limites: π(1 - e^(-R²)) → π e π(1 - e^(-2R²)) → π', sp.limit(sp.pi*(1 - sp.exp(-R**2)), R, sp.oo) == sp.pi and sp.limit(sp.pi*(1 - sp.exp(-2*R**2)), R, sp.oo) == sp.pi)
chk('B7 ∫_{-∞}^{∞} e^(-x²) dx = √π', sp.integrate(sp.exp(-x**2), (x, -sp.oo, sp.oo)) == sp.sqrt(sp.pi))
chk('B7 normal: x = √2 u, dx = √2 du ⇒ ∫ e^(-x²/2) dx = √2 · √π = √(2π)', sp.integrate(sp.exp(-x**2/2), (x, -sp.oo, sp.oo)) == sp.sqrt(2*sp.pi))

# ---------- B8 · elipse e vazão no cano ----------
Xe, Ye = a*r*sp.cos(th), b*r*sp.sin(th)
Je = sp.Matrix([[sp.diff(Xe, r), sp.diff(Xe, th)], [sp.diff(Ye, r), sp.diff(Ye, th)]]).det()
chk('B8 elipse: x = a r cos θ, y = b r sen θ ⇒ jacobiano = abr cos²θ + abr sen²θ = abr', sp.simplify(Je - a*b*r) == 0)
chk('B8 x²/a² + y²/b² = r² (r ≤ 1 é a elipse)', sp.simplify(Xe**2/a**2 + Ye**2/b**2 - r**2) == 0)
chk('B8 área = ∫_0^{2π}∫_0^1 ab r dr dθ = ab · ½ · 2π = πab; a = b = R dá πR²', sp.integrate(sp.integrate(a*b*r, (r, 0, 1)), (th, 0, 2*sp.pi)) == sp.pi*a*b)
v = vmax*(1 - r**2/R**2)
in8 = sp.integrate(v*r, (r, 0, R))
chk('B8 vazão: v_max ∫_0^R (r - r³/R²) dr = v_max (R²/2 - R²/4) = v_max R²/4', sp.simplify(in8 - vmax*R**2/4) == 0)
Q = sp.integrate(in8, (th, 0, 2*sp.pi))
chk('B8 Q = 2π · v_max R²/4 = πR² v_max/2; média = v_max/2', sp.simplify(Q - sp.pi*R**2*vmax/2) == 0 and sp.simplify(Q/(sp.pi*R**2) - vmax/2) == 0)

# ---------- S2 · gancho para o 3.4-T3 (só confere o que o T3 vai cumprir) ----------
k = sp.symbols('k', positive=True)
M = sp.integrate(sp.integrate(k*r*r, (r, 0, a)), (th, 0, sp.pi))
My = sp.integrate(sp.integrate(r*sp.sin(th)*k*r*r, (r, 0, a)), (th, 0, sp.pi))
chk('S2 meia-lua de raio a, densidade k·r: M = kπa³/3, momento = ka⁴/2, ȳ = 3a/(2π) ≈ 0,477a', sp.simplify(M - k*sp.pi*a**3/3) == 0
    and sp.simplify(My - k*a**4/2) == 0 and sp.simplify(My/M - 3*a/(2*sp.pi)) == 0)

print(f'\nTOTAL: {sum(ok)}/{len(ok)} True')
