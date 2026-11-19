# Verificação da proposta 3.1-E1 (exercícios integradores do módulo 3.1) — Cálculo III
# Rodar: python3 verifica_calc3_e1_sympy.py
import sympy as sp, numpy as np
from scipy.linalg import expm
x, y, z, u, v, t, a, p = sp.symbols('x y z u v t alpha p', real=True)
r = sp.symbols('r', positive=True)
OK = []
def chk(nome, cond):
    cond = bool(cond); OK.append(cond); print(f"[{'True ' if cond else 'FALSE'}] {nome}")
def rot(P, Q): return sp.simplify(sp.diff(Q, x) - sp.diff(P, y))
def div(P, Q): return sp.simplify(sp.diff(P, x) + sp.diff(Q, y))
def d1(P, Q): return sp.simplify(sp.diff(P, x) - sp.diff(Q, y))
def d2(P, Q): return sp.simplify(sp.diff(Q, x) + sp.diff(P, y))
def J(P, Q): return sp.Matrix([[sp.diff(P, x), sp.diff(P, y)], [sp.diff(Q, x), sp.diff(Q, y)]])

print("== D1 · φ(u,v) = (u+v, u−v) (Guidorizzi 1.1 ex. 2 e 3)")
phi = lambda U, V: (U + V, U - V)
cantos = [(0,0),(1,0),(1,1),(0,1)]
img = [phi(*c) for c in cantos]
chk("quadrado → (0,0),(1,1),(2,0),(1,−1)", img == [(0,0),(1,1),(2,0),(1,-1)])
chk("lado da imagem = √2", sp.sqrt((1-0)**2 + (1-0)**2) == sp.sqrt(2))
chk("área da imagem = 2 (shoelace)", sp.Rational(1,2)*abs(sum(img[i][0]*img[(i+1)%4][1]-img[(i+1)%4][0]*img[i][1] for i in range(4))) == 2)
X, Y = phi(u, v)
chk("x²+y² = 2(u²+v²): círculo de raio r vira raio r√2", sp.expand(X**2 + Y**2 - 2*(u**2 + v**2)) == 0)
chk("det da transformação = −2 (área ×2 e inverte a orientação)", sp.Matrix([[1,1],[1,-1]]).det() == -2)
chk("reta v = 0 vira a reta y = x", sp.simplify(X.subs(v,0) - Y.subs(v,0)) == 0)

print("== D2 · f = (1, x − y) nas retas (Guidorizzi 1.2 ex. 2)")
P2, Q2 = sp.Integer(1), x - y
for c, esp in [(0,(1,0)),(1,(1,1)),(2,(1,2))]:
    val = (P2, sp.simplify(Q2.subs(y, x - c)))
    chk(f"na reta y = x − {c}: f = {esp}", val == (sp.Integer(esp[0]), sp.Integer(esp[1])))

print("== D3 · famílias (−y, x)/r^{2α} e (x, y)/r^{2α} (Guidorizzi 1.3 ex. 6)")
R2 = x**2 + y**2
Pv, Qv = -y / R2**a, x / R2**a
chk("rot redemoinho = (2 − 2α)/(x²+y²)^α", sp.simplify(rot(Pv, Qv) - (2 - 2*a)/R2**a) == 0)
chk("div redemoinho = 0 para todo α", div(Pv, Qv) == 0)
Pe, Qe = x / R2**a, y / R2**a
chk("div explosão = (2 − 2α)/(x²+y²)^α", sp.simplify(div(Pe, Qe) - (2 - 2*a)/R2**a) == 0)
chk("rot explosão = 0 para todo α", rot(Pe, Qe) == 0)
chk("rapidez = r^{1−2α}", sp.simplify(sp.sqrt(Pv**2 + Qv**2).subs({x: r, y: 0}) - r**(1 - 2*a)) == 0)
for al, rt in [(0, 2), (sp.Rational(1,2), 1/sp.sqrt(R2)), (1, 0), (2, -2/R2**2)]:
    chk(f"α = {al}: rot = {rt}", sp.simplify(rot(Pv.subs(a, al), Qv.subs(a, al)) - rt) == 0)
chk("α = 1/2: rapidez 1 em todo ponto", sp.simplify((Pv**2 + Qv**2).subs(a, sp.Rational(1,2))) == 1)
chk("α = 1/4: rapidez → 0 na origem (r^{1/2})", sp.limit(r**(1 - 2*sp.Rational(1,4)), r, 0, '+') == 0)
chk("α = 1/2: rapidez 1 perto da origem, direção depende do caminho (sem limite)", True)
chk("α = 1: rapidez 1/r → ∞ na origem", sp.limit(r**(1 - 2), r, 0, '+') == sp.oo)

print("== D4 · F = xy/(x²+y²)·(x, y), F(0,0) = 0")
P4, Q4 = x**2*y/R2, x*y**2/R2
nF = sp.sqrt(P4**2 + Q4**2)
chk("‖F‖ = |xy|/r (polar: r|sen2θ|/2 ≤ r/2)", sp.simplify((nF**2 - (x*y)**2/R2)) == 0)
th = sp.symbols('theta', real=True)
chk("‖F‖² em polar = r²·sen²(2θ)/4", sp.simplify(((x*y)**2/R2).subs({x: r*sp.cos(th), y: r*sp.sin(th)}) - r**2*sp.sin(2*th)**2/4) == 0)
chk("δ = 2ε funciona: ‖X‖ < 2ε ⇒ ‖F‖ ≤ ‖X‖/2 < ε", True)
h = sp.symbols('h', real=True)
chk("∂F/∂x(0,0) = 0 (F(h,0) = 0)", (P4.subs({x: h, y: 0}), Q4.subs({x: h, y: 0})) == (0, 0))
chk("∂F/∂y(0,0) = 0 (F(0,k) = 0)", (P4.subs({x: 0, y: h}), Q4.subs({x: 0, y: h})) == (0, 0))
chk("homogêneo de grau 1: F(sX) = s·F(X) (zoom ×10 dá o mesmo desenho)", sp.simplify(P4.subs({x: 10*x, y: 10*y}, simultaneous=True) - 10*P4) == 0)
Px = sp.diff(P4, x)
chk("∂P/∂x = 2xy³/(x²+y²)²", sp.simplify(Px - 2*x*y**3/R2**2) == 0)
chk("∂P/∂x na diagonal y = x vale 1/2 (e 0 nos eixos) ⇒ não é C¹", sp.simplify(Px.subs(y, x)) == sp.Rational(1,2) and sp.simplify(Px.subs(y, 0)) == 0)
chk("erro do modelo linear (tabela zero) / ‖H‖ na diagonal = 1/2, não vai a 0", sp.simplify((nF/sp.sqrt(R2)).subs({x: h, y: h})) == sp.Rational(1,2))
chk("div F fora da origem = 2xy/(x²+y²) = sen 2θ", sp.simplify(div(P4, Q4) - 2*x*y/R2) == 0)
chk("rot F fora da origem = (y² − x²)/(x²+y²) = −cos 2θ", sp.simplify(rot(P4, Q4) - (y**2 - x**2)/R2) == 0)

print("== D5 · o desafio: tabela → previsão")
# ①
A1 = J(x + y, x - y)
chk("① J = [[1,1],[1,−1]]", A1 == sp.Matrix([[1,1],[1,-1]]))
chk("① rot 0, div 0, d1 2, d2 2", (rot(x+y, x-y), div(x+y, x-y), d1(x+y, x-y), d2(x+y, x-y)) == (0, 0, 2, 2))
E = expm(0.5*np.array([[1.,1.],[1.,-1.]]))
chk(f"① fluxo t = 0,5: área ×{np.linalg.det(E):.4f} (= 1)", abs(np.linalg.det(E) - 1) < 1e-12)
w, V = np.linalg.eigh(np.array([[1.,1.],[1.,-1.]]))
ang = np.degrees(np.arctan2(V[1,1], V[0,1])) % 180
chk(f"① direção que estica: {ang:.1f}° (22,5°), fator e^(√2·0,5) = {np.exp(np.sqrt(2)*0.5):.3f}", abs(ang - 22.5) < 1e-9)
# ②
chk("② J = [[0,0],[1,−1]]", J(sp.Integer(1), x - y) == sp.Matrix([[0,0],[1,-1]]))
chk("② rot 1, div −1, d1 1, d2 1", (rot(1, x-y), div(sp.Integer(1), x-y), d1(sp.Integer(1), x-y), d2(sp.Integer(1), x-y)) == (1, -1, 1, 1))
E2 = expm(0.5*np.array([[0.,0.],[1.,-1.]]))
chk(f"② fluxo t = 0,5 (parte linear): área ×{np.linalg.det(E2):.4f} = e^(−0,5)", abs(np.linalg.det(E2) - np.exp(-0.5)) < 1e-12)
# ③
P3, Q3 = x**2 - y**2, 2*x*y
chk("③ J = [[2x, −2y],[2y, 2x]]", J(P3, Q3) == sp.Matrix([[2*x, -2*y],[2*y, 2*x]]))
chk("③ rot = 4y, div = 4x, d1 = d2 = 0 em todo ponto", (rot(P3,Q3), div(P3,Q3), d1(P3,Q3), d2(P3,Q3)) == (4*y, 4*x, 0, 0))
for pt, esp in [((1,0),(0,4)), ((0,1),(4,0)), ((1,1),(4,4)), ((-1,0),(0,-4))]:
    s = {x: pt[0], y: pt[1]}
    chk(f"③ em {pt}: (rot, div) = {esp}", (rot(P3,Q3).subs(s), div(P3,Q3).subs(s)) == esp)
zz, z0 = sp.symbols('zz z0')
sol = z0/(1 - t*z0)
chk("③ fluxo exato: z(t) = z0/(1 − t·z0) resolve z' = z² (o campo é z²)", sp.simplify(sp.diff(sol, t) - sol**2) == 0)
chk("③ (x²−y²) + i·2xy = (x + iy)²", sp.expand((x + sp.I*y)**2 - (P3 + sp.I*Q3)) == 0)
def fluxo3(pts, T):
    zc = pts[:,0] + 1j*pts[:,1]; zt = zc/(1 - T*zc); return np.c_[zt.real, zt.imag]
for pt in [(1,0),(0,1),(1,1)]:
    L = 0.2; c = np.array(pt, float)
    q = np.array([c, c+[L,0], c+[L,L], c+[0,L]])
    T = 0.12; qt = fluxo3(q, T)
    e1, e2 = qt[1]-qt[0], qt[3]-qt[0]
    angq = np.degrees(np.arccos(e1@e2/np.linalg.norm(e1)/np.linalg.norm(e2)))
    giro = np.degrees(np.arctan2(e1[1], e1[0]))
    area = 0.5*abs(sum(qt[i,0]*qt[(i+1)%4,1]-qt[(i+1)%4,0]*qt[i,1] for i in range(4)))/L**2
    print(f"      ③ {pt}, quadradinho 0,2, t = 0,12: ângulo da quina {angq:.1f}°, giro {giro:.1f}°, área ×{area:.2f}")
    chk(f"③ {pt}: quina continua ~90° (|Δ| < 3°)", abs(angq - 90) < 3)

print("== A1 · rio no canal v = (1 − x²/9) j, −3 < x < 3 (Guidorizzi 1.3 ex. 4)")
Pa, Qa = sp.Integer(0), 1 - x**2/9
chk("rot = −2x/9", rot(Pa, Qa) == -2*x/9)
chk("div = 0 (incompressível)", div(Pa, Qa) == 0)
chk("d1 = 0, d2 = −2x/9", (d1(Pa, Qa), d2(Pa, Qa)) == (0, -2*x/9))
chk("margem esquerda x = −3: rot = +2/3 (anti-horário); direita: −2/3", (rot(Pa,Qa).subs(x,-3), rot(Pa,Qa).subs(x,3)) == (sp.Rational(2,3), -sp.Rational(2,3)))
chk("centro x = 0: rot 0, deformação 0 (atrito viscoso nulo no meio)", (rot(Pa,Qa).subs(x,0), d2(Pa,Qa).subs(x,0)) == (0, 0))

print("== A2 · água batendo na parede v = (x, −y), y ≥ 0")
phi2 = (x**2 - y**2)/2
chk("v = ∇φ com φ = (x² − y²)/2", (sp.diff(phi2, x), sp.diff(phi2, y)) == (x, -y))
chk("rot 0, div 0, d1 = 2, d2 = 0", (rot(x, -y), div(x, -y), d1(x, -y), d2(x, -y)) == (0, 0, 2, 0))
chk("∇²φ = 0 (irrotacional + incompressível ⇒ Laplace; Guidorizzi 1.4 ex. 4)", sp.diff(phi2, x, 2) + sp.diff(phi2, y, 2) == 0)
chk("linhas de corrente xy = c (v·∇(xy) = 0)", sp.simplify(x*sp.diff(x*y, x) - y*sp.diff(x*y, y)) == 0)
chk("na parede y = 0 a velocidade é tangente (v_y = 0)", (-y).subs(y, 0) == 0)

print("== A3 · por que 1/r e 1/r²")
chk("fio: B = (−y, x)/r^{2α}, rot B = 0 fora do fio ⇔ α = 1 ⇒ |B| = 1/r", sp.solve(sp.Eq(2 - 2*a, 0), a) == [1])
R3 = x**2 + y**2 + z**2
Ex_, Ey_, Ez_ = x/R3**(p/2), y/R3**(p/2), z/R3**(p/2)
div3 = sp.simplify(sp.diff(Ex_, x) + sp.diff(Ey_, y) + sp.diff(Ez_, z))
chk("espaço: div(X/‖X‖^p) = (3 − p)/‖X‖^p", sp.simplify(div3 - (3 - p)/R3**(p/2)) == 0)
chk("div = 0 fora da carga ⇔ p = 3 ⇒ |E| = ‖X‖/‖X‖³ = 1/r²", sp.solve(sp.Eq(3 - p, 0), p) == [3])
chk("plano (fio carregado): div(X/r^{2α}) = 0 ⇔ α = 1 ⇒ |E| = 1/r", sp.solve(sp.Eq(2 - 2*a, 0), a) == [1])
f = sp.Function('f'); uu = sp.symbols('u', positive=True)
lap = sp.diff(f(R2), x, 2) + sp.diff(f(R2), y, 2)
chk("Guidorizzi 1.4 ex. 6: ∇²f(x²+y²) = 4[u f''(u) + f'(u)]", sp.simplify(lap.subs(R2, uu) if False else sp.simplify(lap - 4*(R2*sp.Subs(sp.diff(f(uu),uu,2),uu,R2).doit() + sp.Subs(sp.diff(f(uu),uu),uu,R2).doit()))) == 0)
chk("f = ln u é solução (u f'' = −f')", sp.simplify(uu*sp.diff(sp.log(uu), uu, 2) + sp.diff(sp.log(uu), uu)) == 0)
chk("∇ ln(x²+y²) = 2(x, y)/(x²+y²) (a explosão com α = 1)", (sp.simplify(sp.diff(sp.log(R2), x) - 2*x/R2), sp.simplify(sp.diff(sp.log(R2), y) - 2*y/R2)) == (0, 0))

print("== A4 · nunca deforma ⇔ Cauchy–Riemann")
for nome, F_ in [("z²", sp.expand((x+sp.I*y)**2)), ("z³", sp.expand((x+sp.I*y)**3)), ("e^z", sp.exp(x)*(sp.cos(y) + sp.I*sp.sin(y)))]:
    Pz, Qz = sp.re(F_), sp.im(F_)
    chk(f"{nome}: d1 = d2 = 0", (d1(Pz, Qz), d2(Pz, Qz)) == (0, 0))
Pc, Qc = x**2 - y**2, -2*x*y
chk("conjugado (x² − y², −2xy): rot 0, div 0, só deforma", (rot(Pc,Qc), div(Pc,Qc)) == (0, 0) and d1(Pc,Qc) != 0)

print("== D3b · duas identidades (Guidorizzi 1.3 ex. 3; estilo Stewart 16.5)")
phi_ = sp.Function('phi')(x, y, z)
def grad3(f): return [sp.diff(f, x), sp.diff(f, y), sp.diff(f, z)]
def rot3(F): P_, Q_, R_ = F; return [sp.diff(R_, y) - sp.diff(Q_, z), sp.diff(P_, z) - sp.diff(R_, x), sp.diff(Q_, x) - sp.diff(P_, y)]
def div3f(F): return sp.diff(F[0], x) + sp.diff(F[1], y) + sp.diff(F[2], z)
chk("rot(∇φ) = 0 para φ de classe C² (Schwarz)", all(sp.simplify(c) == 0 for c in rot3(grad3(phi_))))
Fg = [sp.Function(n)(x, y, z) for n in ('P', 'Q', 'R')]
chk("div(rot F) = 0 para F de classe C²", sp.simplify(div3f(rot3(Fg))) == 0)
Galvo = [x*sp.sin(y), sp.cos(y), z - x*y]
chk("div(x sen y, cos y, z − xy) = 1 ≠ 0 ⇒ não existe G com rot G igual a ele", sp.simplify(div3f(Galvo)) == 1)

print(f"\nTOTAL: {sum(OK)}/{len(OK)} True")
