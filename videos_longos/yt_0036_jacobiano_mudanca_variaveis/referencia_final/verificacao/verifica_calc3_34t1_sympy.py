# Verificação da proposta 3.4-T1 (Jacobiano e mudança de variáveis) — Parallax Lab
import sympy as sp, numpy as np
from scipy import integrate
u,v,x,y,t,a,b,c,d,s = sp.symbols('u v x y t a b c d s', real=True)
E = sp.E
res = []
def ck(nome, cond):
    res.append((nome, bool(cond))); print(f"{nome}: {bool(cond)}")

# --- B1: 1D, régua esticada
ck("L1 ∫0^2 x dx = 2", sp.integrate(x,(x,0,2)) == 2)
ck("L2 x=2t: ∫0^1 (2t)·2 dt = 2", sp.integrate(2*t*2,(t,0,1)) == 2)

# --- B3: linear
area_fig = (a+b)*(c+d) - 2*(a*c/2) - 2*(b*d/2) - 2*(b*c)
ck("P1 (a+b)(c+d) − ac − bd − 2bc = ad − bc", sp.expand(area_fig - (a*d-b*c)) == 0)
cr = sp.Matrix([a,c,0]).cross(sp.Matrix([b,d,0]))
ck("P2 (a,c,0)∧(b,d,0) = (0,0,ad−bc)", cr == sp.Matrix([0,0,a*d-b*c]))
M3 = sp.Matrix([[sp.Symbol('i'),sp.Symbol('j'),sp.Symbol('k')],[a,c,0],[b,d,0]])
ck("P3 det 3x3 (i j k; xu yu 0; xv yv 0) = (ad − bc)k", sp.expand(M3.det() - (a*d-b*c)*sp.Symbol('k')) == 0)
ck("P4 det transposta = det", sp.Matrix([[a,c],[b,d]]).det() == sp.Matrix([[a,b],[c,d]]).det())
# exemplo linear do aquecimento: x = 2u + v, y = u + v  (det 1? escolher) -> usar x=2u+v, y=u+3v
Jlin = sp.Matrix([[2,1],[1,3]]).det()
ck("P5 φ(u,v)=(2u+v, u+3v): det = 2·3 − 1·1 = 5", Jlin == 5)
# área do paralelogramo de (2,1) e (1,3) pela figura: (2+1)(1+3) − 2·(2·1/2) − 2·(1·3/2) − 2·(1·1) = 5
ck("P6 figura: 3·4 − 2 − 3 − 2 = 5", 3*4 - 2*(2*1/sp.Integer(2)) - 2*(1*3/sp.Integer(2)) - 2*1 == 5)

# --- trapézio do gancho: u = x + y, v = x − y
X = (u+v)/2; Y = (u-v)/2
ck("T0 inversa: x=(u+v)/2, y=(u−v)/2 devolve u,v", sp.simplify(X+Y-u)==0 and sp.simplify(X-Y-v)==0)
J = sp.Matrix([[sp.diff(X,u), sp.diff(X,v)],[sp.diff(Y,u), sp.diff(Y,v)]])
ck("T1 J = |1/2 1/2; 1/2 −1/2| = −1/2", J.det() == sp.Rational(-1,2))
Jpsi = sp.Matrix([[1,1],[1,-1]]).det()
ck("T2 ∂(u,v)/∂(x,y) = −2 e (−2)(−1/2) = 1", Jpsi == -2 and Jpsi*J.det() == 1)
# grade inclinada: retas x+y=k e x−y=m, distância entre vizinhas 1/√2, célula de área 1/2
ck("T3 célula da grade inclinada: (1/√2)² = 1/2", (1/sp.sqrt(2))**2 == sp.Rational(1,2))
# imagem do quadrado unitário de uv: vértices (0,0),(1/2,1/2),(1,0),(1/2,−1/2) (sentido horário)
def shoelace(P):
    return sp.Rational(1,2)*sum(P[i][0]*P[(i+1)%len(P)][1]-P[(i+1)%len(P)][0]*P[i][1] for i in range(len(P)))
img = [(X.subs({u:p,v:q}), Y.subs({u:p,v:q})) for p,q in [(0,0),(1,0),(1,1),(0,1)]]
ck("T4 quadrado uv → losango de área orientada −1/2 (inverte o sentido)", shoelace(img) == sp.Rational(-1,2))
# vértices do trapézio
V = {(1,0):(1,1),(2,0):(2,2),(0,-2):(-2,2),(0,-1):(-1,1)}
ck("T5 vértices (1,0)(2,0)(0,−2)(0,−1) → (1,1)(2,2)(−2,2)(−1,1)", all((px+py, px-py)==q for (px,py),q in V.items()))
# lados: y=0 → u=v ; x−y=2 → v=2 ; x=0 → u=−v ; x−y=1 → v=1
ck("T6 y=0 ⇒ u=v ; x=0 ⇒ u=−v", sp.simplify((x+0)-(x-0))==0 and sp.simplify((0+y)+(0-y))==0)
inner = sp.integrate(sp.exp(u/v),(u,-v,v))
ck("T7 ∫_{−v}^{v} e^{u/v} du = v(e − 1/e)", sp.simplify(inner - v*(E-1/E))==0)
ck("T8 d/du (v e^{u/v}) = e^{u/v}", sp.simplify(sp.diff(v*sp.exp(u/v),u)-sp.exp(u/v))==0)
ck("T9 ∫1^2 v dv = [v²/2] = 2 − 1/2 = 3/2", sp.integrate(v,(v,1,2)) == sp.Rational(3,2))
tot = sp.Rational(1,2)*sp.integrate(inner,(v,1,2))
ck("T10 total = (3/4)(e − 1/e)", sp.simplify(tot - sp.Rational(3,4)*(E-1/E))==0)
val = float(tot); print("   valor ≈", val)
f = lambda yy,xx: np.exp((xx+yy)/(xx-yy))
# numérica em xy, deitado: y ∈ [−2,−1]: x ∈ [0, y+2]; y ∈ [−1,0]: x ∈ [y+1, y+2]
g = lambda xx,yy: np.exp((xx+yy)/(xx-yy))
n1 = integrate.dblquad(g, -2, -1, lambda yy: 0.0, lambda yy: yy+2)[0]
n2 = integrate.dblquad(g, -1, 0, lambda yy: yy+1, lambda yy: yy+2)[0]
ck("T11 numérica em xy (dblquad) = (3/4)(e − 1/e)", abs(n1+n2-val) < 1e-8)
ck("T12 teste f=1: área uv = 3 e área xy = 3·1/2 = 3/2 (2 − 1/2)", sp.integrate(2*v,(v,1,2))==3 and sp.Rational(2)-sp.Rational(1,2)==sp.Rational(3,2))
# trava nas duas ordens: primitivas não elementares (Ei)
# com x fixo: (x+y)/(x−y) = −1 + 2x/(x−y); t = x − y ⇒ ∫ e^{a/t} dt (a = 2x). Com y fixo: 1 + 2y/(x−y), o mesmo tipo.
aa = sp.symbols('aa', positive=True)
pr = sp.integrate(sp.exp(aa/t), t)
ck("T13 ∫ e^{a/t} dt = t e^{a/t} − a·Ei(a/t): pede Ei (não elementar) nas duas ordens", pr.has(sp.Ei) and sp.simplify(sp.diff(pr,t)-sp.exp(aa/t))==0)
ck("T14 (x+y)/(x−y) = −1 + 2x/(x−y) = 1 + 2y/(x−y)", sp.simplify((x+y)/(x-y) - (-1+2*x/(x-y)))==0 and sp.simplify((x+y)/(x-y)-(1+2*y/(x-y)))==0)

# --- Guidorizzi Ex. 1: u = x − y, v = x + y ; 1 ≤ x+y ≤ 2, x,y ≥ 0 ; ∬ cos(x−y)/sen(x+y) = 1
inG = sp.integrate(sp.cos(u)/sp.sin(v),(u,-v,v))
ck("G1 ∫_{−v}^{v} cos u / sen v du = 2", sp.simplify(inG-2)==0)
ck("G2 (1/2)∫1^2 2 dv = 1", sp.Rational(1,2)*sp.integrate(2,(v,1,2))==1)
h = lambda yy,xx: np.cos(xx-yy)/np.sin(xx+yy)
m1 = integrate.dblquad(lambda yy,xx: np.cos(xx-yy)/np.sin(xx+yy), 0, 1, lambda xx: 1-xx, lambda xx: 2-xx)[0]
m2 = integrate.dblquad(lambda yy,xx: np.cos(xx-yy)/np.sin(xx+yy), 1, 2, lambda xx: 0.0, lambda xx: 2-xx)[0]
ck("G3 numérica em xy = 1", abs(m1+m2-1) < 1e-8)
ck("G4 J de x=(u+v)/2, y=(v−u)/2 = +1/2", sp.Matrix([[sp.Rational(1,2),sp.Rational(1,2)],[sp.Rational(-1,2),sp.Rational(1,2)]]).det()==sp.Rational(1,2))

# --- não linear: φ(u,v) = (u² − v², 2uv) em [0,1]²
Xn, Yn = u**2-v**2, 2*u*v
Jn = sp.Matrix([[sp.diff(Xn,u),sp.diff(Xn,v)],[sp.diff(Yn,u),sp.diff(Yn,v)]]).det()
ck("N1 J = (2u)(2u) − (−2v)(2v) = 4u² + 4v²", sp.expand(Jn-(4*u**2+4*v**2))==0)
ck("N2 bordas: u=1 ⇒ x = 1 − y²/4 ; v=1 ⇒ x = y²/4 − 1", sp.simplify((1-v**2) - (1-(2*v)**2/4))==0 and sp.simplify((u**2-1)-((2*u)**2/4-1))==0)
An = sp.integrate(Jn,(u,0,1),(v,0,1))
ck("N3 área = ∫∫ 4(u²+v²) = 4(1/3 + 1/3) = 8/3", An == sp.Rational(8,3))
Ad = sp.integrate((1-y**2/4)-(y**2/4-1),(y,0,2))
ck("N4 conferência deitada: ∫0^2 (2 − y²/2) dy = 4 − 4/3 = 8/3", Ad == sp.Rational(8,3))
ck("N5 J no canto (0,0) = 0 ; no canto (1,1) = 8", Jn.subs({u:0,v:0})==0 and Jn.subs({u:1,v:1})==8)
# fator local: célula com canto M = (0.75, 0.5)
u0,v0 = sp.Rational(3,4), sp.Rational(1,2)
for D in [sp.Rational(1,4), sp.Rational(1,10), sp.Rational(1,20), sp.Rational(1,100)]:
    exato = sp.integrate(Jn,(u,u0,u0+D),(v,v0,v0+D))
    aprox = Jn.subs({u:u0,v:v0})*D*D
    print(f"   Δ={D}: exata={float(exato):.6f}  |J(M)|ΔuΔv={float(aprox):.6f}  razão={float(exato/aprox):.4f}")
ck("N6 J(0,75; 0,5) = 4(0,5625 + 0,25) = 3,25", Jn.subs({u:u0,v:v0}) == sp.Rational(13,4))
# área exata da célula pela fronteira (shoelace fino), sem usar J
def area_borda(u0,v0,D,n=4000):
    tt = np.linspace(0,1,n,endpoint=False)
    us = np.concatenate([u0+D*tt, np.full(n,u0+D), u0+D-D*tt, np.full(n,u0)])
    vs = np.concatenate([np.full(n,v0), v0+D*tt, np.full(n,v0+D), v0+D-D*tt])
    X_, Y_ = us**2-vs**2, 2*us*vs
    return 0.5*np.sum(X_*np.roll(Y_,-1)-np.roll(X_,-1)*Y_)
ex = float(sp.integrate(Jn,(u,0.75,0.85),(v,0.5,0.6)))
ck("N7 área pela borda (shoelace) = ∬ J da célula Δ=0,1", abs(area_borda(0.75,0.5,0.1)-ex) < 1e-6)
Iy = sp.integrate(Yn*Jn,(u,0,1),(v,0,1))
Iyd = sp.integrate(y*((1-y**2/4)-(y**2/4-1)),(y,0,2))
ck("N8 (reserva) ∬ y dA = 2 nas duas formas", Iy==2 and Iyd==2)

# --- hipótese: injetora. φ(u,v) = (u², v) em [−1,1]×[0,1] dobra
ck("H1 dobra: ∬|J| = ∫∫ 2|u| = 2, mas a área da imagem [0,1]² é 1", sp.integrate(2*sp.Abs(u),(u,-1,1),(v,0,1))==2)
ck("H2 sem módulo, ∬ J = ∫∫ 2u = 0", sp.integrate(2*u,(u,-1,1),(v,0,1))==0)

# --- aplicações / pontes
A = sp.Matrix([[a,b],[c,d]])
ck("D1 d/dt det(I + tJ) em t=0 = traço = div", sp.diff((sp.eye(2)+t*A).det(),t).subs(t,0) == a+d)
ph,lam = sp.symbols('phi lambda', real=True)
ym = sp.log(1/sp.cos(ph)+sp.tan(ph))
ck("M1 Mercator: dy/dφ = sec φ", sp.simplify(sp.diff(ym,ph) - 1/sp.cos(ph))==0)
fat = 1/sp.cos(sp.rad(72))**2
print("   sec²(72°) ≈", float(fat))
ck("M2 sec²(72°) ≈ 10,5", abs(float(fat)-10.47) < 0.05)
# gancho p/ 3.4-T2 (r e θ): disco unitário
gz = integrate.dblquad(lambda yy,xx: np.exp(-(xx*xx+yy*yy)), -1, 1, lambda xx: -np.sqrt(1-xx*xx), lambda xx: np.sqrt(1-xx*xx))[0]
ck("Z1 ∬_disco e^{−(x²+y²)} = π(1 − 1/e) ≈ 1,9859", abs(gz - np.pi*(1-np.exp(-1))) < 1e-8)
print(f"\n{sum(r for _,r in res)}/{len(res)} True")
