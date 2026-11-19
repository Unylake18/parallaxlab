# Números novos do handoff v2 do yt_0031 (B6-3 zoom da lupa, B4 contagem, B7-2 cancelamentos)
import sympy as sp
ok=[]
for k,(a,b),d in zip([1,2,3],[(0.06,0.16),(0.05,0.085),(0.035,0.06)],[0.036,0.013,0.0065]):
    p=1/(sp.pi/2+2*sp.pi*k); q=1/(3*sp.pi/2+2*sp.pi*k)
    ok.append(a<float(q)<float(p)<b and sp.sin(1/p)==1 and sp.sin(1/q)==-1 and abs(float(p-q)-d)<6e-4)
D=lambda n:sp.Rational(2,n)
ok.append([4*D(n) for n in (4,8,16)]==[2,1,sp.Rational(1,2)])                       # parábola 4Δ
ok.append([2*D(n) for n in (4,8,16,32)]==[1,sp.Rational(1,2),sp.Rational(1,4),sp.Rational(1,8)])  # arco 2Δ
e,al,M=sp.symbols('epsilon alpha M',positive=True)
ok.append(sp.simplify(al*e/(2*al)-e/2)==0 and sp.simplify(4*M*e/(8*M)-e/2)==0)       # B7-2
print(ok, all(ok))
