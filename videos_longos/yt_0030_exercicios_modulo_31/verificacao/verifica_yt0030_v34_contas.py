"""yt_0030 v3.4 (CONTA INTEIRA): confere no SymPy cada igualdade nova da coluna (C1–C21 do handoff).
uso: python verifica_yt0030_v34_contas.py   → imprime uma linha por checagem e o total (esperado: tudo True)."""
import sympy as sp
x, y, z, t, h, a, r, p = sp.symbols("x y z t h alpha r p", positive=True)
xr, yr = sp.symbols("x_r y_r", real=True)
I = sp.I
R = []
def ok(nome, expr):
    v = sp.simplify(expr) == 0 if not isinstance(expr, bool) else expr
    R.append((nome, bool(v))); print(f"{'True ' if v else 'FALSE'} {nome}")
s = x**2 + y**2
# C1 · D3-2
ok("C1 ‖(−y,x)‖ = √((−y)²+x²) = √(x²+y²)", sp.sqrt((-y)**2 + x**2) - sp.sqrt(x**2 + y**2))
ok("C1 s^α = (r²)^α = r^{2α}", sp.powsimp((r**2)**a) - r**(2*a))
ok("C1 r / r^{2α} = r^{1−2α}", sp.powsimp(r / r**(2*a)) - r**(1 - 2*a))
v = sp.Matrix([-y, x]) / s**a
ok("C1 ‖v‖ = r^{1−2α} (r = √s)", sp.simplify(sp.sqrt(v.dot(v)) - sp.sqrt(s)**(1 - 2*a)))
# C2 · D3-3
Q, P = x * s**(-a), -y * s**(-a)
ok("C2 (x)' = 1", sp.diff(x, x) - 1)
ok("C2 ∂s/∂x = 2x", sp.diff(s, x) - 2*x)
ok("C2 (s^{−α})'_x = −α s^{−α−1}·2x", sp.diff(s**(-a), x) - (-a * s**(-a - 1) * 2*x))
P2 = 1 * s**(-a) + x * (-a * s**(-a - 1) * 2*x)
ok("C2 ∂Q/∂x = 1·s^{−α} + x(−α s^{−α−1}·2x)", sp.diff(Q, x) - P2)
P3 = s**(-a) - 2*a*x**2 * s**(-a - 1)
ok("C2 = s^{−α} − 2αx² s^{−α−1}", P2 - P3)
ok("C2 K4: s^{−α} = s·s^{−α−1}", s**(-a) - s * s**(-a - 1))
ok("C2 P5: = s^{−α−1}(s − 2αx²)", P3 - s**(-a - 1) * (s - 2*a*x**2))
G2 = -1 * s**(-a) + (-y) * (-a * s**(-a - 1) * 2*y)
ok("C2 ∂P/∂y = −1·s^{−α} + (−y)(−α s^{−α−1}·2y)", sp.diff(P, y) - G2)
G3 = -s**(-a) + 2*a*y**2 * s**(-a - 1)
ok("C2 G3 = −s^{−α} + 2αy² s^{−α−1}", G2 - G3)
ok("C2 G5 = −s^{−α−1}(s − 2αy²)", G3 + s**(-a - 1) * (s - 2*a*y**2))
RS = s**(-a - 1) * (s - 2*a*x**2) - (-(s**(-a - 1)) * (s - 2*a*y**2))
ok("C2 RS = rot", sp.diff(Q, x) - sp.diff(P, y) - RS)
ok("C2 RS5 = s^{−α−1}(2s − 2αs)", RS - s**(-a - 1) * (2*s - 2*a*s))
ok("C2 RS5b = s^{−α−1}·s(2 − 2α)", s**(-a - 1) * (2*s - 2*a*s) - s**(-a - 1) * s * (2 - 2*a))
ok("C2 RS5c = s^{−α}(2 − 2α) = (2 − 2α)/s^α", s**(-a - 1) * s * (2 - 2*a) - (2 - 2*a) / s**a)
ok("C2 DP = −y(−α s^{−α−1}·2x) = 2αxy s^{−α−1}", sp.diff(P, x) - 2*a*x*y * s**(-a - 1))
ok("C2 DQ = x(−α s^{−α−1}·2y) = −2αxy s^{−α−1}", sp.diff(Q, y) + 2*a*x*y * s**(-a - 1))
ok("C2 div = 0", sp.diff(P, x) + sp.diff(Q, y))
# C3 · D3-6 (α = ½: pelo eixo x, X = (t, 0); pelo eixo y, X = (0, t))
vh = lambda X, Y: sp.Matrix([-Y, X]) / sp.sqrt(X**2 + Y**2)
ok("C3 v(t,0) = (0,1)", (vh(t, 0) - sp.Matrix([0, 1])).norm())
ok("C3 v(0,t) = (−1,0)", (vh(0, t) - sp.Matrix([-1, 0])).norm())
ok("C3 α=¼: r^{1−2α} → 0 (r → 0⁺)", sp.limit(r**(1 - 2*sp.Rational(1, 4)), r, 0, "+") == 0)
ok("C3 α=1: r^{1−2α} → ∞ (r → 0⁺)", sp.limit(r**(1 - 2), r, 0, "+") == sp.oo)
# C4/C14 · φ = ½(x² − y²)
phi = (x**2 - y**2) / 2
ok("C4 φ_x = ½·2x = x", sp.diff(phi, x) - x)
ok("C4 φ_y = ½·(−2y) = −y", sp.diff(phi, y) + y)
ok("C14 φ_xx = 1, φ_yy = −1, ∇²φ = 0", sp.diff(phi, x, 2) - 1 + sp.diff(phi, y, 2) + 1 + sp.diff(phi, x, 2) + sp.diff(phi, y, 2))
# C5 · D3b-4
ok("C5 ∂(x sen y)/∂x = sen y", sp.diff(x * sp.sin(y), x) - sp.sin(y))
ok("C5 ∂(cos y)/∂y = −sen y", sp.diff(sp.cos(y), y) + sp.sin(y))
ok("C5 ∂(z − xy)/∂z = 1", sp.diff(z - x*y, z) - 1)
# C6 · D4-6
F4 = lambda X, Y: X*Y / (X**2 + Y**2) * sp.Matrix([X, Y])
ok("C6 homogeneidade F(sx,sy) = s F(x,y)", (F4(t*x, t*y) - t * F4(x, y)).applyfunc(sp.simplify).norm())
ok("C6 F(h,h) = (h·h)/(h²+h²)(h,h) = ½(h,h) = (h/2,h/2)", (F4(h, h) - sp.Matrix([h/2, h/2])).norm())
ok("C6 ‖erro‖ = √(h²/4 + h²/4) = h√2/2", sp.sqrt(h**2/4 + h**2/4) - h*sp.sqrt(2)/2)
ok("C6 ‖H‖ = √(h²+h²) = h√2", sp.sqrt(2*h**2) - h*sp.sqrt(2))
ok("C6 razão = ½", (h*sp.sqrt(2)/2) / (h*sp.sqrt(2)) - sp.Rational(1, 2))
# C7 · D4-7
N, D = x**2*y, x**2 + y**2
ok("C7 N' = 2xy", sp.diff(N, x) - 2*x*y)
ok("C7 D' = 2x", sp.diff(D, x) - 2*x)
ok("C7 abre: 2xy(x²+y²) − x²y·2x = 2x³y + 2xy³ − 2x³y", sp.expand(2*x*y*D - N*2*x) - (2*x**3*y + 2*x*y**3 - 2*x**3*y))
dPx = sp.diff(N / D, x)
ok("C7 ∂P/∂x = 2xy³/(x²+y²)²", dPx - 2*x*y**3 / D**2)
ok("C7 y=0: 0", dPx.subs(y, 0))
ok("C7 x=0: 0", dPx.subs(x, 0))
ok("C7 y=x: 2x·x³/(x²+x²)² = 2x⁴/(2x²)² = 2x⁴/4x⁴ = ½", dPx.subs(y, x) - sp.Rational(1, 2))
# C8 · D5-9 (z²)
P3_, Q3_ = x**2 - y**2, 2*x*y
ok("C8 P_x = 2x − 0", sp.diff(P3_, x) - 2*x)
ok("C8 P_y = 0 − 2y", sp.diff(P3_, y) + 2*y)
ok("C8 Q_x = 2·y·1", sp.diff(Q3_, x) - 2*y)
ok("C8 Q_y = 2·x·1", sp.diff(Q3_, y) - 2*x)
# C9–C11 · A1 (rio)
Qr = 1 - x**2 / 9
ok("C9 Q_x = 0 − 2x/9", sp.diff(Qr, x) + 2*x/9)
ok("C9 Q_y = 0", sp.diff(Qr, y))
rot = sp.diff(Qr, x) - 0
ok("C10 rot(−3) = −2(−3)/9 = 6/9 = 2/3", rot.subs(x, -3) - sp.Rational(2, 3))
ok("C10 rot(3) = −2·3/9 = −2/3", rot.subs(x, 3) + sp.Rational(2, 3))
ok("C10 rot(0) = 0", rot.subs(x, 0))
w = sp.Rational(2, 3) / 2
ok("C10 ω = (2/3)/2 = 1/3", w - sp.Rational(1, 3))
T = 2*sp.pi / w
ok("C10 T = 2π/(1/3) = 6π", T - 6*sp.pi)
ok("C10 6π ≈ 18,8 (≈ 19 s)", abs(float(T) - 18.85) < 0.01)
d2 = sp.diff(Qr, x) + 0
ok("C11 |d₂(±3)| = 2·3/9 = 2/3", abs(d2.subs(x, 3)) - sp.Rational(2, 3) + abs(d2.subs(x, -3)) - sp.Rational(2, 3))
ok("C11 d₂(0) = 0", d2.subs(x, 0))
# C12–C15 · A2 (jato)
u, vv = x, -y
ok("C12 u_x=1, u_y=0, v_x=0, v_y=−1", (sp.Matrix([[sp.diff(u, x), sp.diff(u, y)], [sp.diff(vv, x), sp.diff(vv, y)]]) - sp.Matrix([[1, 0], [0, -1]])).norm())
X_, Y_ = sp.Function("X")(t), sp.Function("Y")(t)
ok("C13 d(xy)/dt = ẋ y + x ẏ", sp.diff(X_*Y_, t) - (sp.diff(X_, t)*Y_ + X_*sp.diff(Y_, t)))
ok("C13 u·y + x·v = xy − xy = 0", u*y + x*vv)
c = sp.symbols("c", positive=True)
ok("C13 xy = c ⇒ y = c/x", sp.solve(sp.Eq(x*y, c), y) == [c/x])
ok("C15 div ∇φ = φ_xx + φ_yy", sp.diff(sp.diff(phi, x), x) + sp.diff(sp.diff(phi, y), y) - (sp.diff(phi, x, 2) + sp.diff(phi, y, 2)))
# C16 · A4-2
ok("C16 (x+iy)² = x² + 2x(iy) + (iy)²", sp.expand((x + I*y)**2 - (x**2 + 2*x*(I*y) + (I*y)**2)))
ok("C16 i² = −1", I**2 + 1)
ok("C16 = (x² − y²) + i(2xy)", sp.expand((x + I*y)**2 - ((x**2 - y**2) + I*(2*x*y))))
ok("C16 CR: P_x = 2x = Q_y", sp.diff(P3_, x) - sp.diff(Q3_, y))
ok("C16 CR: P_y = −2y = −Q_x", sp.diff(P3_, y) + sp.diff(Q3_, x))
# C17 · A4-3
J = sp.Matrix([[sp.diff(P3_, x), sp.diff(P3_, y)], [sp.diff(Q3_, x), sp.diff(Q3_, y)]])
ok("C17 J = (2x −2y; 2y 2x)", (J - sp.Matrix([[2*x, -2*y], [2*y, 2*x]])).norm())
th = sp.atan2(y, x)
ok("C17 J = 2r·R(θ), 2r = √(a²+b²) = 2√(x²+y²)", (J - 2*sp.sqrt(s) * sp.Matrix([[sp.cos(th), -sp.sin(th)], [sp.sin(th), sp.cos(th)]])).applyfunc(sp.simplify).norm())
J11 = J.subs({x: 1, y: 1})
R45 = sp.Matrix([[sp.cos(sp.pi/4), -sp.sin(sp.pi/4)], [sp.sin(sp.pi/4), sp.cos(sp.pi/4)]])
ok("C17 J(1,1) = (2 −2; 2 2) = 2√2·R(45°)", (J11 - 2*sp.sqrt(2)*R45).norm())
ok("C17 colunas (2,2)·(−2,2) = 0, mesmo tamanho 2√2", J11[:, 0].dot(J11[:, 1]) == 0 and J11[:, 0].norm() == J11[:, 1].norm() == 2*sp.sqrt(2))
# C18 · A4-4
Pi, Qi = x**2 - y**2, -2*x*y
Px, Py, Qx, Qy = [sp.diff(f, k) for f in (Pi, Qi) for k in (x, y)]
ok("C18 P_x=2x, P_y=−2y, Q_x=−2y, Q_y=−2x", (Px - 2*x)**2 + (Py + 2*y)**2 + (Qx + 2*y)**2 + (Qy + 2*x)**2)
ok("C18 rot = −2y − (−2y) = 0", Qx - Py)
ok("C18 div = 2x − 2x = 0", Px + Qy)
ok("C18 d₁ = 4x, d₂ = −4y", (Px - Qy - 4*x)**2 + (Qx + Py + 4*y)**2)
# C19 · A3-3
ok("C19 2 − 2α = 0 ⇒ α = 1", sp.solve(sp.Eq(2 - 2*a, 0), a) == [1])
ok("C19 ‖B‖ = r/r^{2α} com α=1 = 1/r", (r / r**(2*a)).subs(a, 1) - 1/r)
# C20 · A3-4
E = sp.Matrix([x, y]) * s**(-a)
T1 = 1*s**(-a) + x*(-a*s**(-a - 1)*2*x)
ok("C20 T1 = ∂(x s^{−α})/∂x", sp.diff(E[0], x) - T1)
ok("C20 T1b = s^{−α} − 2αx² s^{−α−1}", T1 - (s**(-a) - 2*a*x**2*s**(-a - 1)))
S1 = 2*s**(-a) - 2*a*(x**2 + y**2)*s**(-a - 1)
ok("C20 S1 = div E", sp.diff(E[0], x) + sp.diff(E[1], y) - S1)
ok("C20 S3 = 2s^{−α} − 2α s^{−α}", S1 - (2*s**(-a) - 2*a*s**(-a)))
ok("C20 S4 = (2 − 2α)/s^α", S1 - (2 - 2*a)/s**a)
# C21 · A3-5
nX = sp.sqrt(x**2 + y**2 + z**2)
ok("C21 ∂‖X‖/∂x = ½(x²+y²+z²)^{−1/2}·2x = x/‖X‖", sp.diff(nX, x) - x/nX)
PA = 1/nX**p + x*(-p*nX**(-p - 1))*(x/nX)
ok("C21 PA = ∂/∂x (x/‖X‖^p)", sp.diff(x/nX**p, x) - PA)
ok("C21 PB0 = 1/‖X‖^p − p x² ‖X‖^{−p−1}‖X‖^{−1}", PA - (1/nX**p - p*x**2*nX**(-p - 1)*nX**(-1)))
ok("C21 PB1 = … ‖X‖^{−p−2} = PB", PA - (1/nX**p - p*x**2/nX**(p + 2)))
divE = sum(sp.diff(k/nX**p, k) for k in (x, y, z))
ok("C21 div E = (3 − p)/‖X‖^p", divE - (3 - p)/nX**p)
ok("C21 p=3: ‖E‖ = r/r³ = 1/r²", r/r**3 - 1/r**2)
n_ok = sum(v for _, v in R)
print(f"\n{n_ok}/{len(R)} True")
