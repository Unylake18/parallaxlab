# Verificação das contas do 3.6-T1 (integral de linha de campo vetorial) · yt_0045 provisório
import sympy as sp
t,u,R,c,n=sp.symbols('t u R c n',positive=True)
ok=[]
def chk(nome,cond):
    v=bool(cond); ok.append(v); print(('True ' if v else 'FALSE'),nome)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def lineint(F,g,a,b,var=t):
    gt=[sp.diff(gi,var) for gi in g]; Fg=[f(*g) for f in F]
    return sp.simplify(sp.integrate(sp.simplify(dot(Fg,gt)),(var,a,b))), sp.simplify(dot(Fg,gt))
# C1 força constante, caminho reto
F=sp.Matrix([2,1]);A=sp.Matrix([1,1]);B=sp.Matrix([4,1]);D=B-A
chk('C1.1 B-A=(3,0)',D==sp.Matrix([3,0]))
chk('C1.2 W=2*3+1*0=6',F.dot(D)==6)
chk('C1.3 |F||D|cos a = 6 (cos a = 2/sqrt5)',sp.simplify(sp.sqrt(5)*3*(2/sp.sqrt(5)))==6)
chk('C1.4 parte de F na direção do caminho = 2, de lado = 1 (trabalho 0)',F.dot(sp.Matrix([1,0]))==2 and sp.Matrix([0,1]).dot(D)==0)
# C2 soma de Riemann exata do redemoinho no círculo: n R^2 sen(2pi/n)
ti=sp.symbols('t_i');dt=sp.symbols('Delta',positive=True)
Fi=sp.Matrix([-R*sp.sin(ti),R*sp.cos(ti)]);Dg=sp.Matrix([R*sp.cos(ti)-R*sp.cos(ti-dt),R*sp.sin(ti)-R*sp.sin(ti-dt)])
chk('C2.1 F(γ(t_i))·Δγ_i = R² sen Δt',sp.simplify(sp.expand_trig(Fi.dot(Dg)-R**2*sp.sin(dt)))==0)
for N,val in [(4,4.0),(8,5.657),(16,6.123)]:
    chk(f'C2.2 n={N}: {N} sen(2π/{N}) ≈ {val}',abs(float(N*sp.sin(2*sp.pi/N))-val)<1e-3)
chk('C2.3 lim n sen(2π/n) = 2π',sp.limit(n*sp.sin(2*sp.pi/n),n,sp.oo)==2*sp.pi)
# C4 redemoinho F=(-y,x) no círculo de raio R
Fr=[lambda x,y:-y,lambda x,y:x]
W,ig=lineint(Fr,[R*sp.cos(t),R*sp.sin(t)],0,2*sp.pi)
chk('C4.1 F(γ)·γ\' = R²',sp.simplify(ig-R**2)==0)
chk('C4.2 W = 2πR²',sp.simplify(W-2*sp.pi*R**2)==0)
chk('C4.3 2πR² = 2·(πR²)',sp.simplify(2*sp.pi*R**2-2*(sp.pi*R**2))==0)
W,ig=lineint(Fr,[t,sp.Integer(0)],0,R)
chk('C4.4 no raio γ=(t,0): F(γ)=(0,t), γ\'=(1,0), produto 0, W=0',ig==0 and W==0)
# C5 F=(x,y), γ=(t,t²), t∈[-1,1]
Fx=[lambda x,y:x,lambda x,y:y];g=[t,t**2]
W,ig=lineint(Fx,g,-1,1)
chk('C5.1 F(γ)·γ\' = t + 2t³',sp.simplify(ig-(t+2*t**3))==0)
G=t**2/2+t**4/2
chk('C5.2 primitiva t²/2 + t⁴/2',sp.simplify(sp.diff(G,t)-(t+2*t**3))==0)
chk('C5.3 G(1)=1, G(-1)=1, W=0',G.subs(t,1)==1 and G.subs(t,-1)==1 and W==0)
chk('C5.4 metade de ida: ∫_{-1}^0 = -1',sp.integrate(t+2*t**3,(t,-1,0))==-1)
chk('C5.5 metade de volta: ∫_0^1 = +1',sp.integrate(t+2*t**3,(t,0,1))==1)
chk('C5.6 G(t) = ½(x²+y²) no ponto γ(t)',sp.simplify(G-sp.Rational(1,2)*(g[0]**2+g[1]**2))==0)
chk('C5.7 integrando ímpar',sp.simplify((t+2*t**3).subs(t,-t)+(t+2*t**3))==0)
# C6 outra notação: P x' + Q y' (forma geral) — identidade simbólica
P,Q,Rf=sp.Function('P'),sp.Function('Q'),sp.Function('R')
x_,y_,z_=sp.Function('x')(t),sp.Function('y')(t),sp.Function('z')(t)
Fv=sp.Matrix([P(x_,y_,z_),Q(x_,y_,z_),Rf(x_,y_,z_)]);gv=sp.Matrix([x_,y_,z_]).diff(t)
chk('C6.1 F(γ)·γ\' = P x\' + Q y\' + R z\'',sp.simplify(Fv.dot(gv)-(P(x_,y_,z_)*x_.diff(t)+Q(x_,y_,z_)*y_.diff(t)+Rf(x_,y_,z_)*z_.diff(t)))==0)
# C7 elipse x=2cos t, y=sen t: ∫ -y dx + x dy
xe,ye=2*sp.cos(t),sp.sin(t)
dxe,dye=sp.diff(xe,t),sp.diff(ye,t)
chk('C7.1 dx = -2 sen t dt, dy = cos t dt',dxe==-2*sp.sin(t) and dye==sp.cos(t))
chk('C7.2 -y dx = 2 sen² t dt',sp.simplify(-ye*dxe-2*sp.sin(t)**2)==0)
chk('C7.3 x dy = 2 cos² t dt',sp.simplify(xe*dye-2*sp.cos(t)**2)==0)
chk('C7.4 soma = 2 dt',sp.simplify(-ye*dxe+xe*dye-2)==0)
chk('C7.5 ∫ = 4π',sp.integrate(2,(t,0,2*sp.pi))==4*sp.pi)
a_,b_=sp.symbols('a b',positive=True);X,Y=sp.symbols('X Y')
area=sp.integrate(sp.integrate(1,(Y,-b_*sp.sqrt(1-X**2/a_**2),b_*sp.sqrt(1-X**2/a_**2))),(X,-a_,a_))
chk('C7.6 área da elipse (a=2,b=1) = 2π, e 4π = 2·2π',sp.simplify(area.subs({a_:2,b_:1})-2*sp.pi)==0)
# C8 hélice γ=(cos t, sen t, c t), F=(-y,x,-1), t∈[0,2π]
gh=[sp.cos(t),sp.sin(t),c*t];Fh=[lambda x,y,z:-y,lambda x,y,z:x,lambda x,y,z:-1]
W,ig=lineint(Fh,gh,0,2*sp.pi)
chk('C8.1 dx=-sen t dt, dy=cos t dt, dz=c dt',[sp.diff(e,t) for e in gh]==[-sp.sin(t),sp.cos(t),c])
chk('C8.2 -y dx = sen² t dt; x dy = cos² t dt; -dz = -c dt',sp.simplify(-gh[1]*sp.diff(gh[0],t)-sp.sin(t)**2)==0 and sp.simplify(gh[0]*sp.diff(gh[1],t)-sp.cos(t)**2)==0)
chk('C8.3 integrando = 1 - c',sp.simplify(ig-(1-c))==0)
chk('C8.4 W = 2π - 2πc',sp.simplify(W-(2*sp.pi-2*sp.pi*c))==0)
chk('C8.5 subida numa volta z(2π)-z(0) = 2πc',sp.simplify(gh[2].subs(t,2*sp.pi)-gh[2].subs(t,0)-2*sp.pi*c)==0)
cl=1/(4*sp.pi)
chk('C8.6 lata do canal: duas voltas sobem 1 ⇒ c = 1/(4π)',sp.simplify(cl*4*sp.pi-1)==0)
Wl=W.subs(c,cl)
chk('C8.7 W(lata) = 2π - 1/2 ≈ 5,78',sp.simplify(Wl-(2*sp.pi-sp.Rational(1,2)))==0 and abs(float(Wl)-5.783)<1e-3)
chk('C8.8 W = 0 ⟺ c = 1',sp.solve(sp.Eq(W,0),c)==[1])
W2,_=lineint(Fh,gh,0,4*sp.pi)
chk('C8.9 duas voltas na lata: 4π - 1',sp.simplify(W2.subs(c,cl)-(4*sp.pi-1))==0)
# conferência numérica por soma de Riemann direta da hélice (n=20000, ponto da direita)
import math
N=20000;cc=float(cl);s=0.0
for i in range(1,N+1):
    t0,t1=2*math.pi*(i-1)/N,2*math.pi*i/N
    P1=(math.cos(t1),math.sin(t1),cc*t1);P0=(math.cos(t0),math.sin(t0),cc*t0)
    Fv1=(-P1[1],P1[0],-1.0);s+=sum(a*(b-d) for a,b,d in zip(Fv1,P1,P0))
chk(f'C8.10 soma com {N} pedaços ≈ 2π − 1/2 (={s:.5f})',abs(s-(2*math.pi-0.5))<1e-3)
# C9 (gancho do 3.6-T2): mesmo círculo duas vezes mais rápido e ao contrário
W,_=lineint(Fr,[R*sp.cos(2*u),R*sp.sin(2*u)],0,sp.pi,var=u)
chk('C9.1 γ₂(u)=(R cos 2u, R sen 2u), u∈[0,π]: 2πR² (igual)',sp.simplify(W-2*sp.pi*R**2)==0)
W,_=lineint(Fr,[R*sp.cos(-t),R*sp.sin(-t)],0,2*sp.pi)
chk('C9.2 ao contrário: -2πR²',sp.simplify(W+2*sp.pi*R**2)==0)
print(f'\n{sum(ok)}/{len(ok)} True')
