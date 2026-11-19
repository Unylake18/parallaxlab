# yt_0030 · handoff v2 · conferência de TODAS as linhas intermediárias dos quadros de conta (SymPy)
from sympy import *
from sympy.core.function import AppliedUndef
from sympy.matrices import MatrixBase
x,y,z,u,v,a,p,t,h,r,th,c=symbols('x y z u v alpha p t h r theta c',real=True)
s=x**2+y**2
ok=[]
import random
def _zero(e):
    if isinstance(e,MatrixBase): return all(_zero(q) for q in e)
    e=sympify(e)
    if simplify(e)==0: return True
    if e.atoms(AppliedUndef): return False
    fs=sorted(e.free_symbols,key=str)
    for _ in range(6):
        val={q:Rational(random.randint(2,19),random.randint(3,11)) for q in fs}
        if abs(N(e.subs(val),30))>1e-20: return False
    return True
def chk(nome,expr):
    b=_zero(expr)
    ok.append(b); print(('OK  ' if b else 'FALHA ')+nome)
# D1
phi=lambda U,V:(U+V,U-V)
chk('D1 φ(1,0)=(1+0,1-0)=(1,1)', Matrix(phi(1,0))-Matrix([1,1]))
chk('D1 φ(1,1)=(2,0)', Matrix(phi(1,1))-Matrix([2,0]))
chk('D1 φ(0,1)=(1,-1)', Matrix(phi(0,1))-Matrix([1,-1]))
chk('D1 φ(u,0)=(u,u)', Matrix(phi(u,0))-Matrix([u,u]))
chk('D1 lado √(1²+1²)=√2', sqrt(1**2+1**2)-sqrt(2))
chk('D1 (u+v)²+(u−v)² = u²+2uv+v²+u²−2uv+v²', (u+v)**2+(u-v)**2-(u**2+2*u*v+v**2+u**2-2*u*v+v**2))
chk('D1 ... = 2u²+2v² = 2(u²+v²)', expand(u**2+2*u*v+v**2+u**2-2*u*v+v**2)-2*(u**2+v**2))
chk('D1 f1(x,0)=(x,x)', Matrix([x+0,x-0])-Matrix([x,x]))
chk('D1 f1(0,y)=(y,-y)', Matrix([0+y,0-y])-Matrix([y,-y]))
# D3
P=-y*s**(-a); Q=x*s**(-a)
chk('D3 ∂Q/∂x = 1·s^-α + x·(−α s^(−α−1)·2x)', diff(Q,x)-(s**(-a)+x*(-a*s**(-a-1)*2*x)))
chk('D3 ∂Q/∂x = s^-α − 2αx² s^(−α−1)', diff(Q,x)-(s**(-a)-2*a*x**2*s**(-a-1)))
chk('D3 ∂Q/∂x = s^(−α−1)(s − 2αx²)', diff(Q,x)-s**(-a-1)*(s-2*a*x**2))
chk('D3 ∂P/∂y = −s^(−α−1)(s − 2αy²)', diff(P,y)+s**(-a-1)*(s-2*a*y**2))
rot=diff(Q,x)-diff(P,y)
chk('D3 rot = s^(−α−1)(s−2αx²+s−2αy²)', rot-s**(-a-1)*(s-2*a*x**2+s-2*a*y**2))
chk('D3 rot = s^(−α−1)(2s−2α(x²+y²))', rot-s**(-a-1)*(2*s-2*a*(x**2+y**2)))
chk('D3 rot = s^(−α−1)·s·(2−2α) = (2−2α)/s^α', rot-(2-2*a)/s**a)
chk('D3 ∂P/∂x = −y·(−α s^(−α−1)·2x) = 2αxy s^(−α−1)', diff(P,x)-2*a*x*y*s**(-a-1))
chk('D3 ∂Q/∂y = x·(−α s^(−α−1)·2y) = −2αxy s^(−α−1)', diff(Q,y)+2*a*x*y*s**(-a-1))
chk('D3 div = 0', diff(P,x)+diff(Q,y))
R_=sqrt(s)
chk('D3 ‖v‖ = r/r^(2α) = r^(1−2α)', simplify(sqrt(P**2+Q**2).subs({x:r*cos(th),y:r*sin(th)}).rewrite(Pow))-r**(1-2*a) if False else (sqrt(simplify((P**2+Q**2)/ (s**(1-2*a))))-1).subs({x:3,y:4,a:Rational(3,7)}))
for al,val in [(0,2),(Rational(1,2),1/R_),(1,0),(2,-2/s**2)]:
    chk(f'D3 α={al}: rot', ((2-2*a)/s**a).subs(a,al)-val)
# giro 90°: w=(Q,−P)
W1,W2=Q,-P
chk('D3 w = (Q,−P) = (x,y)/s^α', Matrix([W1,W2])-Matrix([x,y])*s**(-a))
chk('D3 div w = ∂Q/∂x − ∂P/∂y = rot v', diff(W1,x)+diff(W2,y)-rot)
chk('D3 rot w = −(∂P/∂x + ∂Q/∂y) = −div v = 0', diff(W2,x)-diff(W1,y))
# D3b
f=Function('phi')(x,y,z)
PP,QQ,RR=diff(f,x),diff(f,y),diff(f,z)
rotg=Matrix([diff(RR,y)-diff(QQ,z),diff(PP,z)-diff(RR,x),diff(QQ,x)-diff(PP,y)])
chk('D3b rot ∇φ = 0 (Schwarz)', rotg.norm()**2)
P3,Q3,R3=[Function(n)(x,y,z) for n in 'PQR']
G=Matrix([diff(R3,y)-diff(Q3,z),diff(P3,z)-diff(R3,x),diff(Q3,x)-diff(P3,y)])
chk('D3b div rot F = R_yx − Q_zx + P_zy − R_xy + Q_xz − P_yz = 0', diff(G[0],x)+diff(G[1],y)+diff(G[2],z))
Gt=Matrix([x*sin(y),cos(y),z-x*y])
chk('D3b teste: div = sen y − sen y + 1 = 1', diff(Gt[0],x)+diff(Gt[1],y)+diff(Gt[2],z)-1)
chk('D3b plano: rot ∇φ (3ª linha) com φ=(x²−y²)/2 = 0', diff(diff((x**2-y**2)/2,y),x)-diff(diff((x**2-y**2)/2,x),y))
# D4
k=x*y/s; F4=Matrix([k*x,k*y])
chk('D4 ‖F‖² = (xy)²/s', F4.dot(F4)-(x*y)**2/s)
chk('D4 xy = r² cosθ senθ = r² sen2θ/2', (r*cos(th)*r*sin(th))-r**2*sin(2*th)/2)
chk('D4 ‖F‖ = r|sen2θ|/2 (r>0)', simplify(((x*y)**2/s).subs({x:r*cos(th),y:r*sin(th)}))-(r*sin(2*th)/2)**2)
chk('D4 F(h,0) = 0', F4.subs({x:h,y:0}).norm())
chk('D4 F(0,k) = 0', F4.subs({x:0,y:h}).norm())
S=symbols('S',positive=True)
chk('D4 F(Sx,Sy) = S·F(x,y)', simplify(F4.subs({x:S*x,y:S*y},simultaneous=True)-S*F4).norm())
chk('D4 diagonal F(h,h) = (h/2,h/2)', F4.subs({x:h,y:h})-Matrix([h/2,h/2]))
chk('D4 razão = ½', simplify(sqrt(2*(h/2)**2)/sqrt(2*h**2)).subs(h,1)-Rational(1,2))
PP4=x**2*y/s
chk('D4 P = x²y/(x²+y²)', F4[0]-PP4)
chk('D4 ∂P/∂x = [2xy·s − x²y·2x]/s²', diff(PP4,x)-(2*x*y*s-x**2*y*2*x)/s**2)
chk('D4 ... = (2x³y + 2xy³ − 2x³y)/s²', expand(2*x*y*s-x**2*y*2*x)-(2*x**3*y+2*x*y**3-2*x**3*y))
chk('D4 ∂P/∂x = 2xy³/s²', diff(PP4,x)-2*x*y**3/s**2)
chk('D4 na diagonal: 2t·t³/(2t²)² = ½', (2*x*y**3/s**2).subs(y,x)-Rational(1,2))
chk('D4 na outra diagonal: −½', (2*x*y**3/s**2).subs(y,-x)+Rational(1,2))
chk('D4 no eixo y=0: 0', (2*x*y**3/s**2).subs(y,0))
# D5 e medidas
def med(P,Q):
    Px,Py,Qx,Qy=diff(P,x),diff(P,y),diff(Q,x),diff(Q,y)
    return [simplify(e) for e in (Qx-Py,Px+Qy,Px-Qy,Qx+Py)],(Px,Py,Qx,Qy)
m,J=med(x+y,x-y); chk('D5① J=(1,1;1,−1); rot 0, div 0, d1 2, d2 2', Matrix(list(J)+m)-Matrix([1,1,1,-1,0,0,2,2]))
m,J=med(1+0*x,x-y); chk('D5② J=(0,0;1,−1); rot 1, div −1, d1 1, d2 1', Matrix(list(J)+m)-Matrix([0,0,1,-1,1,-1,1,1]))
m,J=med(x**2-y**2,2*x*y); chk('D5③ J=(2x,−2y;2y,2x); rot 4y, div 4x, d1 0, d2 0', Matrix(list(J)+m)-Matrix([2*x,-2*y,2*y,2*x,4*y,4*x,0,0]))
for pt,rv,dv in [((1,0),0,4),((0,1),4,0),((1,1),4,4)]:
    chk(f'D5③ em {pt}: rot {rv}, div {dv}', Matrix([4*y,4*x]).subs({x:pt[0],y:pt[1]})-Matrix([rv,dv]))
# A1
m,J=med(0*x,1-x**2/9); chk('A1 J=(0,0;−2x/9,0); rot −2x/9, div 0, d1 0, d2 −2x/9', Matrix(list(J)+m)-Matrix([0,0,-2*x/9,0,-2*x/9,0,0,-2*x/9]))
chk('A1 Q(±3)=0, Q(0)=1', Matrix([(1-x**2/9).subs(x,3),(1-x**2/9).subs(x,-3),(1-x**2/9).subs(x,0)-1]))
chk('A1 rot(−3)=2/3, rot(3)=−2/3', Matrix([(-2*x/9).subs(x,-3)-Rational(2,3),(-2*x/9).subs(x,3)+Rational(2,3)]))
chk('A1 ω=1/3, T=2π/ω=6π≈18,85 s', Matrix([Rational(2,3)/2-Rational(1,3), 2*pi/Rational(1,3)-6*pi]))
print('     T =',N(6*pi,4))
# A2
m,J=med(x,-y); chk('A2 J=(1,0;0,−1); rot 0, div 0, d1 2, d2 0', Matrix(list(J)+m)-Matrix([1,0,0,-1,0,0,2,0]))
chk('A2 d(xy)/dt = u·y + x·v = xy − xy = 0', x*y+x*(-y))
ph=(x**2-y**2)/2
chk('A2 ∇φ = (x,−y)', Matrix([diff(ph,x),diff(ph,y)])-Matrix([x,-y]))
chk('A2 ∇²φ = 1 + (−1) = 0', diff(ph,x,2)+diff(ph,y,2))
# A4
chk('A4 (x+iy)² = x² + 2ixy + i²y² = x² − y² + i·2xy', expand((x+I*y)**2)-(x**2-y**2+I*2*x*y))
m,J=med(x**2-y**2,-2*x*y); chk('A4 irmão: J=(2x,−2y;−2y,−2x); rot 0, div 0', Matrix(list(J)+m[:2])-Matrix([2*x,-2*y,-2*y,-2*x,0,0]))
chk('A4 irmão: d1 = 4x, d2 = −4y (só deforma)', Matrix(m[2:])-Matrix([4*x,-4*y]))
# A3
chk('A3 2 − 2α = 0 ⇒ α = 1', Matrix(solve(2-2*a,a))-Matrix([1]))
X3=sqrt(x**2+y**2+z**2)
chk('A3 ∂‖X‖/∂x = x/‖X‖', diff(X3,x)-x/X3)
chk('A3 ∂/∂x(x/‖X‖^p) = 1/‖X‖^p + x·(−p‖X‖^(−p−1))·x/‖X‖', diff(x/X3**p,x)-(1/X3**p+x*(-p*X3**(-p-1))*x/X3))
chk('A3 ... = 1/‖X‖^p − p x²/‖X‖^(p+2)', diff(x/X3**p,x)-(1/X3**p-p*x**2/X3**(p+2)))
dv3=diff(x/X3**p,x)+diff(y/X3**p,y)+diff(z/X3**p,z)
chk('A3 div = 3/‖X‖^p − p(x²+y²+z²)/‖X‖^(p+2)', dv3-(3/X3**p-p*(x**2+y**2+z**2)/X3**(p+2)))
chk('A3 div = (3 − p)/‖X‖^p', dv3-(3-p)/X3**p)
X2=sqrt(x**2+y**2)
chk('A3 plano: div = (2 − p)/‖X‖^p', diff(x/X2**p,x)+diff(y/X2**p,y)-(2-p)/X2**p)
chk('A3 p=3: ‖E‖ = r/r³ = 1/r²', (X3/X3**3-1/X3**2))
print(f'\n{sum(ok)} de {len(ok)} checagens True')
