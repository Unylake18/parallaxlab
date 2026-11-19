# Verificação das contas do 3.5-T3 Coordenadas cilíndricas (yt_0042 provisório · EP. 17)
# Notação: (s, θ, z), s = distância ao eixo z; r = distância à origem; ρ = densidade; R raio fixo; h altura.
# Cada linha imprime ID, descrição, True/False. Rode: python verifica_calc3_35t3_sympy.py
import sympy as sp
s, th, z, R, h, u, t, x, y = sp.symbols('s theta z R h u t x y', positive=True)
ok = []
def chk(i, d, c):
    c = bool(c); ok.append(c); print(f"{i:6s} {d:74s} {c}")
S = sp.simplify
X = s*sp.cos(th); Y = s*sp.sin(th); Zc = z

# H1 · a lata em cartesianas trava
f = sp.sqrt(x**2 + y**2 + z**2)
Gz = z*f/2 + (x**2 + y**2)/2*sp.log(z + f)
chk("H1a", "primitiva em z de sqrt(x²+y²+z²) = z·raiz/2 + (x²+y²)/2·ln(z+raiz)", S(sp.diff(Gz, z) - f) == 0)
# H1 · em esféricas a fórmula da sonda racha: parede r = 1/sen φ, tampa r = 1/cos φ, iguais em φ = π/4
p = sp.symbols('phi', positive=True)
chk("H1b", "1/sen φ = 1/cos φ em φ = π/4 (a quina)", S((1/sp.sin(p) - 1/sp.cos(p)).subs(p, sp.pi/4)) == 0)

# H2 / B2-1 · as duas células: Δs = 1/2, Δθ = π/6, Δz = 1/2
def cel(s1, s2):
    return sp.integrate(s, (s, s1, s2))*(sp.pi/6)*sp.Rational(1, 2)
VE, VP = cel(0, sp.Rational(1, 2)), cel(sp.Rational(1, 2), 1)
chk("B2a", "célula do eixo = π/96 ≈ 0,033", S(VE - sp.pi/96) == 0 and abs(float(VE) - 0.0327) < 5e-4)
chk("B2b", "célula da parede = π/32 = 3π/96 ≈ 0,098", S(VP - sp.pi/32) == 0 and abs(float(VP) - 0.0982) < 5e-4)
chk("B2c", "razão parede/eixo = 3", S(VP/VE - 3) == 0)
chk("B2d", "s̄ Δs Δθ Δz com s̄ = 1/4 dá o exato (eixo)", S(sp.Rational(1, 4)*sp.Rational(1, 2)*sp.pi/6*sp.Rational(1, 2) - VE) == 0)
chk("B2e", "s̄ Δs Δθ Δz com s̄ = 3/4 dá o exato (parede)", S(sp.Rational(3, 4)*sp.Rational(1, 2)*sp.pi/6*sp.Rational(1, 2) - VP) == 0)
a_, b_ = sp.symbols('a b', positive=True)
chk("B2f", "∫_a^b s ds = s̄(b − a) com s̄ = (a+b)/2 (por que o ≈ acerta)", S(sp.integrate(s, (s, a_, b_)) - (a_ + b_)/2*(b_ - a_)) == 0)

# B1 · o endereço e o ponto (2, π/3, 3/2)
chk("B1a", "x² + y² = s²", S(X**2 + Y**2 - s**2) == 0)
chk("B1b", "x² + y² + z² = s² + z² (r² = s² + z²)", S(X**2 + Y**2 + Zc**2 - (s**2 + z**2)) == 0)
Pt = {s: 2, th: sp.pi/3, z: sp.Rational(3, 2)}
chk("B1c", "x = 2 cos(π/3) = 1", S(X.subs(Pt) - 1) == 0)
chk("B1d", "y = 2 sen(π/3) = √3", S(Y.subs(Pt) - sp.sqrt(3)) == 0)
chk("B1e", "x² + y² = 1 + 3 = 4 = 2²", S((X**2 + Y**2).subs(Pt) - 4) == 0)
chk("B1f", "r = √(4 + 9/4) = √(25/4) = 5/2", S(sp.sqrt(4 + sp.Rational(9, 4)) - sp.Rational(5, 2)) == 0)

# B2-3 · o determinante
Jm = sp.Matrix([X, Y, Zc]).jacobian([s, th, z])
chk("B2g", "matriz: [[cos θ, −s sen θ, 0], [sen θ, s cos θ, 0], [0, 0, 1]]",
    Jm == sp.Matrix([[sp.cos(th), -s*sp.sin(th), 0], [sp.sin(th), s*sp.cos(th), 0], [0, 0, 1]]))
M33 = sp.Matrix([[sp.cos(th), -s*sp.sin(th)], [sp.sin(th), s*sp.cos(th)]]).det()
chk("B2h", "Laplace na linha de baixo: 0·M31 − 0·M32 + 1·M33 = M33", S(Jm.det() - M33) == 0)
chk("B2i", "M33 = cos θ·s cos θ − (−s sen θ)·sen θ = s cos²θ + s sen²θ", S(M33 - (s*sp.cos(th)**2 + s*sp.sin(th)**2)) == 0)
chk("B2j", "det = s (≥ 0, então |det| = s)", S(Jm.det() - s) == 0)

# B2-4 · o teste: cilindro de raio R e altura h
V = sp.integrate(s, (z, 0, h), (s, 0, R), (th, 0, 2*sp.pi))
chk("B2k", "[z]_0^h = h; [s²/2]_0^R = R²/2; [θ]_0^{2π} = 2π", S(h*R**2/2*2*sp.pi - V) == 0)
chk("B2l", "V = πR²h (base × altura)", S(V - sp.pi*R**2*h) == 0)
Vsem = sp.integrate(1, (z, 0, h), (s, 0, R), (th, 0, 2*sp.pi))
chk("B2m", "sem o s: h·R·2π = 2πRh (área do rótulo, unidade m²)", S(Vsem - 2*sp.pi*R*h) == 0)

# B4 · o cilindro deslocado com telhado: (x−1)² + y² ≤ 1, 0 ≤ z ≤ x + y, x ≥ 0, y ≥ 0
chk("B4a", "x² + y² − 2x ≤ 0 ⇔ (x−1)² + y² ≤ 1 (completa o quadrado: soma 1 dos dois lados)", S((x**2 + y**2 - 2*x + 1) - ((x - 1)**2 + y**2)) == 0)
Xd = 1 + s*sp.cos(th)
Jd = sp.Matrix([Xd, Y, Zc]).jacobian([s, th, z]).det()
chk("B4b", "polo deslocado x = 1 + s cos θ: o jacobiano continua s", S(Jd - s) == 0)
teto = 1 + s*sp.cos(th) + s*sp.sin(th)
chk("B4c", "teto: x + y = 1 + s cos θ + s sen θ", S(Xd + Y - teto) == 0)
in1 = sp.integrate(s, (z, 0, teto))
chk("B4d", "[s z]_0^{teto} = s + s² cos θ + s² sen θ", S(in1 - (s + s**2*sp.cos(th) + s**2*sp.sin(th))) == 0)
in2 = sp.integrate(in1, (s, 0, 1))
chk("B4e", "∫_0^1 ... ds = 1/2 + (1/3)cos θ + (1/3)sen θ", S(in2 - (sp.Rational(1, 2) + sp.cos(th)/3 + sp.sin(th)/3)) == 0)
G4 = th/2 + sp.sin(th)/3 - sp.cos(th)/3
chk("B4f", "primitiva θ/2 + (1/3)sen θ − (1/3)cos θ", S(sp.diff(G4, th) - in2) == 0)
chk("B4g", "G(π) = π/2 + 0 + 1/3; G(0) = 0 + 0 − 1/3", S(G4.subs(th, sp.pi) - (sp.pi/2 + sp.Rational(1, 3))) == 0 and S(G4.subs(th, 0) + sp.Rational(1, 3)) == 0)
V4 = sp.integrate(in2, (th, 0, sp.pi))
chk("B4h", "V = π/2 + 2/3 ≈ 2,24", S(V4 - (sp.pi/2 + sp.Rational(2, 3))) == 0 and abs(float(V4) - 2.2375) < 1e-3)
V4o = sp.integrate(sp.integrate(s*(s*sp.cos(th) + s*sp.sin(th)), (s, 0, 2*sp.cos(th))), (th, 0, sp.pi/2))
chk("B4i", "desafio: polo na origem (s ≤ 2cos θ, θ ∈ [0, π/2]) dá o mesmo π/2 + 2/3", S(V4o - (sp.pi/2 + sp.Rational(2, 3))) == 0)
chk("B4j", "(o livro imprime π/2 + 3/2 na Observação: é erro de digitação)", S(V4o - (sp.pi/2 + sp.Rational(3, 2))) != 0)
# conferência numérica em cartesianas
from scipy import integrate as si
import math
vnum = si.tplquad(lambda zz, yy, xx: 1.0, 0, 2, lambda xx: 0, lambda xx: math.sqrt(max(0, 1 - (xx - 1)**2)), lambda xx, yy: 0, lambda xx, yy: xx + yy)[0]
chk("B4k", f"cartesianas no computador: {vnum:.5f} ≈ π/2 + 2/3", abs(vnum - float(V4)) < 1e-6)

# B5 · a lata pesada: ρ = √(s² + z²), 0 ≤ s ≤ 1, 0 ≤ θ ≤ 2π, 0 ≤ z ≤ 1
rho = sp.sqrt(s**2 + z**2)
inner = sp.integrate(rho*s, (s, 0, 1))
chk("B5a", "u = s² + z², du = 2s ds ⇒ s ds = du/2; s=0→u=z², s=1→u=1+z²", S(sp.diff(s**2 + z**2, s) - 2*s) == 0)
chk("B5b", "(1/2)·(2/3)[u^{3/2}] = (1/3)[(1+z²)^{3/2} − (z²)^{3/2}]", S(inner - sp.Rational(1, 3)*((1 + z**2)**sp.Rational(3, 2) - (z**2)**sp.Rational(3, 2))) == 0)
chk("B5c", "(z²)^{3/2} = z³ porque z ≥ 0", S((z**2)**sp.Rational(3, 2) - z**3) == 0)
Gzs = z*sp.sqrt(s**2 + z**2)/2 + s**2/2*sp.asinh(z/s)
chk("B5d", "se integrar z primeiro: ∫√(s²+z²) dz tem logaritmo (asinh) → TRAVA", S(sp.diff(Gzs, z) - rho) == 0)
chk("B5e", "∫_0^1 (1/3) z³ dz = (1/3)[z⁴/4]_0^1 = 1/12", sp.integrate(z**3/3, (z, 0, 1)) == sp.Rational(1, 12))
I = sp.integrate((1 + z**2)**sp.Rational(3, 2), (z, 0, 1))
Iex = 7*sp.sqrt(2)/8 + sp.Rational(3, 8)*sp.log(1 + sp.sqrt(2))
chk("B5f", "I = ∫_0^1 (1+z²)^{3/2} dz = 7√2/8 + (3/8) ln(1+√2) ≈ 1,568", abs(float(I) - float(Iex)) < 1e-12 and abs(float(Iex) - 1.5679) < 1e-3)
chk("B5g", "z = tg t: 1 + tg²t = sec²t; dz = sec²t dt", S(1 + sp.tan(t)**2 - sp.sec(t)**2) == 0 and S(sp.diff(sp.tan(t), t) - sp.sec(t)**2) == 0)
chk("B5h", "limites: z = 0 → t = 0; z = 1 → t = π/4", sp.tan(0) == 0 and sp.tan(sp.pi/4) == 1)
sec5 = float(sp.Integral(sp.sec(t)**5, (t, 0, sp.pi/4)).evalf(30))
chk("B5i", "(sec²t)^{3/2}·sec²t = sec⁵t (sec > 0 em [0, π/4]); ∫_0^{π/4} sec⁵ = I", abs(sec5 - float(Iex)) < 1e-12)
# recorrência: ∫secⁿ = secⁿ⁻² tg/(n−1) + (n−2)/(n−1) ∫secⁿ⁻²  (derivando)
for n in (5, 3):
    lhs = sp.diff(sp.sec(t)**(n - 2)*sp.tan(t)/(n - 1), t) + sp.Rational(n - 2, n - 1)*sp.sec(t)**(n - 2)
    chk(f"B5j{n}", f"recorrência n = {n}: d/dt[sec^{n-2} tg/{n-1}] + {n-2}/{n-1}·sec^{n-2} = sec^{n}", S(sp.simplify(lhs - sp.sec(t)**n).rewrite(sp.cos)) == 0)
chk("B5k", "∫sec = ln|sec + tg| (derivando)", S(sp.diff(sp.log(sp.sec(t) + sp.tan(t)), t) - sp.sec(t)) == 0)
chk("B5l", "em π/4: sec = √2, tg = 1; em 0: sec = 1, tg = 0", S(sp.sec(sp.pi/4) - sp.sqrt(2)) == 0 and sp.tan(sp.pi/4) == 1 and sp.sec(0) == 1 and sp.tan(0) == 0)
chk("B5m", "[sec³ tg / 4]_0^{π/4} = 2√2/4 − 0 = √2/2", S(sp.sqrt(2)**3*1/4 - sp.sqrt(2)/2) == 0)
s3 = sp.sqrt(2)/2 + sp.log(1 + sp.sqrt(2))/2
chk("B5n", "∫_0^{π/4} sec³ = [sec tg/2 + ln(sec+tg)/2] = √2/2 + (1/2)ln(1+√2) − 0", abs(float(sp.Integral(sp.sec(t)**3, (t, 0, sp.pi/4)).evalf(30)) - float(s3)) < 1e-12 and sp.log(1) == 0)
chk("B5o", "I = √2/2 + (3/4)(√2/2 + (1/2)ln(1+√2)) = √2/2 + 3√2/8 + (3/8)ln(1+√2)", S(sp.sqrt(2)/2 + sp.Rational(3, 4)*s3 - (sp.sqrt(2)/2 + 3*sp.sqrt(2)/8 + sp.Rational(3, 8)*sp.log(1 + sp.sqrt(2)))) == 0)
chk("B5p", "√2/2 + 3√2/8 = 4√2/8 + 3√2/8 = 7√2/8", S(sp.sqrt(2)/2 + 3*sp.sqrt(2)/8 - 7*sp.sqrt(2)/8) == 0)
Mz = Iex/3 - sp.Rational(1, 12)
chk("B5q", "(1/3)I − 1/12 = 7√2/24 + (1/8)ln(1+√2) − 1/12 ≈ 0,439", S(Mz - (7*sp.sqrt(2)/24 + sp.log(1 + sp.sqrt(2))/8 - sp.Rational(1, 12))) == 0 and abs(float(Mz) - 0.4393) < 1e-3)
M = 2*sp.pi*Mz
Mfin = sp.pi/12*(7*sp.sqrt(2) - 2 + 3*sp.log(1 + sp.sqrt(2)))
chk("B5r", "M = 2π[...] = 7√2π/12 + (π/4)ln(1+√2) − π/6", S(M - (7*sp.sqrt(2)*sp.pi/12 + sp.pi/4*sp.log(1 + sp.sqrt(2)) - sp.pi/6)) == 0)
chk("B5s", "M = (π/12)(7√2 − 2 + 3 ln(1+√2)) ≈ 2,76", S(M - Mfin) == 0 and abs(float(Mfin) - 2.7603) < 1e-3)
mnum = si.tplquad(lambda zz, yy, xx: math.sqrt(xx*xx + yy*yy + zz*zz), -1, 1, lambda xx: -math.sqrt(1 - xx*xx), lambda xx: math.sqrt(1 - xx*xx), lambda xx, yy: 0, lambda xx, yy: 1)[0]
chk("B5t", f"cartesianas no computador: {mnum:.5f} ≈ 2,7603", abs(mnum - float(Mfin)) < 1e-5)
chk("B5u", "densidade média M/V = M/π ≈ 0,88 (bola do EP. 16: 3/4)", abs(float(Mfin/sp.pi) - 0.8786) < 1e-3)
chk("B5v", "a quina mais longe da origem: r = √(1 + 1) = √2 ≈ 1,41", S(sp.sqrt(1 + 1) - sp.sqrt(2)) == 0)
print(f"   7√2 = {float(7*sp.sqrt(2)):.4f}; 3 ln(1+√2) = {float(3*sp.log(1+sp.sqrt(2))):.4f}; soma − 2 = {float(7*sp.sqrt(2)-2+3*sp.log(1+sp.sqrt(2))):.4f}; × π/12 = {float(Mfin):.4f}")

# S2 · gancho (não vai à tela calculado): momento de inércia da lata homogênea k em torno do eixo z
k = sp.symbols('k', positive=True)
Iz = sp.integrate(k*s**2*s, (s, 0, 1), (th, 0, 2*sp.pi), (z, 0, 1))
chk("S2a", "(reserva) I_z da lata homogênea = kπ/2 = M·1²/2 (não mostrado)", S(Iz - k*sp.pi/2) == 0)

print(f"\nTOTAL: {sum(ok)}/{len(ok)} True")
