"""Estado físico independente do renderer. SI; ângulos de queda positivos."""
import math
import numpy as np

G=9.8
I_ANEL=15*(.3**2+.4**2)/2
I_CUBO=3*.1**2/2
I_DISCOS=2*(.05**2/2+.25**2)
I=I_ANEL+I_CUBO+I_DISCOS
R=.15
A=G/(1+I/(10*R**2))
ALPHA=A/R
TRACAO=10*(G-A)
OMEGA=ALPHA*1.5
K_VOL=I*OMEGA**2/2
FREIO=4/I
T_STOP=OMEGA/FREIO
ALPHA_C=(6*.3-10*.1)*G/(.5+6*.3**2+10*.1**2)
T_C=math.sqrt(2/(ALPHA_C*.3))

def volante(t):
    t=max(0,min(1.5,t)); th=ALPHA*t*t/2; om=ALPHA*t
    return dict(th=th, om=om, h=R*th, v=R*om, K=I*om*om/2, U=10*G*R*th)

def freio(t):
    t=max(0,min(T_STOP,t)); om=max(0,OMEGA-FREIO*t)
    return dict(th=OMEGA*t-FREIO*t*t/2, om=om, K=I*om*om/2, calor=K_VOL-I*om*om/2)

def carretel(t):
    t=max(0,min(T_C,t)); th=ALPHA_C*t*t/2
    return dict(th=th, om=ALPHA_C*t, h1=.3*th, h2=.1*th)

def forca(th):
    s,c=math.sin(th),math.cos(th)
    return dict(fr=13/7*s, fp=4/7*c, fx=-9/7*s*c, fy=13/7*s*s+4/7*c*c,
                at=3/7*G*c, ac=6/7*G*s, alpha=12/7*G*c, omega=math.sqrt(max(0,24/7*G*s)))

def periodo(l, duplo=False):
    return 2*math.pi*math.sqrt((l*l+(.1**2 if duplo else .1**2/2))/(G*l))

def integra(fator, limite=math.pi/2, dt=.0001):
    t=[0.]; th=[0.]; om=[0.]
    while th[-1]<limite:
        a,w=th[-1],om[-1]
        k1=np.array([w,fator*math.cos(a)])
        k2=np.array([w+dt*k1[1]/2,fator*math.cos(a+dt*k1[0]/2)])
        k3=np.array([w+dt*k2[1]/2,fator*math.cos(a+dt*k2[0]/2)])
        k4=np.array([w+dt*k3[1],fator*math.cos(a+dt*k3[0])])
        r=np.array([a,w])+dt*(k1+2*k2+2*k3+k4)/6
        t.append(t[-1]+dt); th.append(r[0]); om.append(r[1])
    return np.array(t),np.array(th),np.array(om)

HASTE=integra(12/7*G)
REGUA=integra(9/8*G)

def queda(t, regua=False):
    ts,ths,oms=REGUA if regua else HASTE
    return float(np.interp(t,ts,ths))
