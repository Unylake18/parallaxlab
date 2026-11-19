# Degraus novos do handoff v2 do yt_0036 (CONTA INTEIRA). Cada linha imprime True.
from sympy import *
u,v,x,y=symbols('u v x y',real=True)
R=Rational
ok=[]
# C5 / B4-3
J=Matrix([[2*u,-2*v],[2*v,2*u]]).det()
ok+= [expand(J-(2*u*2*u-(-2*v)*(2*v)))==0, expand((2*u)*(2*u)-(-2*v)*(2*v)-(4*u**2-(-4*v**2)))==0, expand(J-(4*u**2+4*v**2))==0]
Jm=J.subs({u:R(3,4),v:R(1,2)})
ok+= [4*R(3,4)**2==R(9,4), 4*R(1,2)**2==1, Jm==R(13,4), J.subs({u:0,v:0})==0, J.subs({u:1,v:1})==8]
# B5-3 dobra phi=(u^2,v)
Jd=Matrix([[2*u,0],[0,1]]).det(); ok+=[Jd==2*u]
a1=integrate(-2*u,(u,-1,0)); a2=integrate(2*u,(u,0,1))
ok+=[a1==1, a2==1, (0-(-(-1)**2))==1, integrate(Abs(2*u),(u,-1,1))==2, integrate(2,(v,0,1))==2]
# C8 / C9
G=4*u**3/3+4*v**2*u
ok+=[expand(G.subs(u,1)-G.subs(u,0)-(R(4,3)+4*v**2))==0]
H=4*v/3+4*v**3/3; ok+=[H.subs(v,1)-H.subs(v,0)==R(8,3)]
K=2*y-y**3/6; ok+=[K.subs(y,2)-K.subs(y,0)==R(8,3), 4-R(8,6)==R(8,3)]
# C16
ok+=[(v**2).subs(v,2)-(v**2).subs(v,1)==3]
# C17
X=(u+v)/2; Y=(v-u)/2
ok+=[simplify(X+Y-v)==0, simplify(X-Y-u)==0]
Jl=Matrix([[diff(X,u),diff(X,v)],[diff(Y,u),diff(Y,v)]]).det(); ok+=[Jl==R(1,2)]
ok+=[simplify(integrate(cos(u)/sin(v),(u,-v,v))-2)==0, simplify(sin(-v)+sin(v))==0]
ok+=[R(1,2)*((2*v).subs(v,2)-(2*v).subs(v,1))==1]
# C3 cancelamento
a,b,c,d=symbols('a b c d')
ok+=[expand((a+b)*(c+d)-2*a*c/2-2*b*d/2-2*b*c-(a*d-b*c))==0]
for i,o in enumerate(ok,1): print(i,o)
print('TOTAL',sum(ok),'/',len(ok))
