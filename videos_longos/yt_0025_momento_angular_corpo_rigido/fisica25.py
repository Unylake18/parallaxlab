"""Fonte física única do yt_0025. Metros, kg, segundos; z para cima."""
import json
import math
from pathlib import Path
import numpy as np

U = Path(__file__).resolve().parent
G, M, ELL, TH = 9.8, .2, 1., math.pi/6
WP = math.sqrt(G/(ELL*math.cos(TH)))
MH, LH, AH, WH, D = .4, .3, math.pi/6, 2*math.pi, .4
Z = np.array([0., 0., 1.])
AZ_D = math.radians(35)
OFF_D = .75*np.array([-math.sin(AZ_D), math.cos(AZ_D), 0.])   # bancada_dupla: torto em +OFF_D, reto em -OFF_D (lado a lado na tela a az = 35°)
WD = 2*math.pi

def rz(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def pendulo(phi):
    r = ELL*np.array([math.sin(TH)*math.cos(phi), math.sin(TH)*math.sin(phi),-math.cos(TH)])
    v = np.cross(WP*Z, r)
    l = np.cross(r, M*v)
    return dict(O=np.zeros(3), massa=r, r=r, v=v, p=M*v, L=l,
                axial=l*Z, transversal=l*(1-Z), torque=np.cross(r,-M*G*Z))

def haltere(phi, x=0., multiplicador_omega=1.):
    r = LH*np.array([math.sin(AH)*math.cos(phi), math.sin(AH)*math.sin(phi), math.cos(AH)])
    omega=WH*multiplicador_omega
    v = np.cross(omega*Z, r)
    l1 = np.cross(r, MH*v)
    l2 = l1.copy()
    l = 2*l1
    # Segundo haltere a -alfa: só a transversal troca de sinal.
    l = l + x*l*np.array([-1.,-1.,1.])
    torque = np.cross(omega*Z,l)
    fc = -MH*omega**2*r*(1-Z)
    # d z-hat × F_superior = torque.
    fs = -np.cross(Z,torque)/D
    return dict(O=np.zeros(3), massa=r, massa2=-r, r=r, v=v, L1=l1, L2=l2,
                L=l, axial=l*Z, transversal=l*(1-Z), torque=torque,
                Fc=fc, Fc2=-fc, Fsup=fs, Finf=-fs,omega=omega)

def tensor(p, massa=1.):
    return massa*(np.eye(3)*np.sum(p*p)-p.T@p)

def cria_voxel():
    # União de três elipsoides distintos numa grade de 34 mm (cubo 30 mm + folga 4 mm).
    g=np.arange(-.55,.551,.034)
    p=np.array(np.meshgrid(g,g,g,indexing='ij')).reshape(3,-1).T
    formas=[([-.12,0,0],[.18,.13,.42]),([.08,.025,.12],[.14,.105,.27]),([-.04,-.04,-.21],[.13,.12,.23])]
    dentro=np.zeros(len(p),bool)
    for c,r in formas:
        dentro |= np.sum(((p-.7*np.array(c))/(.7*np.array(r)))**2,axis=1)<1
    p=p[dentro]; p-=p.mean(axis=0)
    I=tensor(p)
    val, eixos=np.linalg.eigh(I)
    if np.linalg.det(eixos)<0: eixos[:,0]*=-1
    # A direção do giro fica a 35° do eixo de menor inércia.
    a=math.radians(35)
    eixo=np.array([math.sin(a),0,math.cos(a)])
    # Base principal → laboratório; e3 do corpo é o menor autovetor.
    b=np.column_stack((eixos[:,2], eixos[:,1], eixos[:,0]))
    if np.linalg.det(b)<0: b[:,1]*=-1
    ry=np.array([[math.cos(a),0,math.sin(a)],[0,1,0],[-math.sin(a),0,math.cos(a)]])
    inicial=ry@b.T
    final=np.vstack((eixos[:,1],eixos[:,2],eixos[:,0]))  # v4 V6: menor inércia (maior dimensão) vai ao z; corpo em pé, não panqueca.
    if np.linalg.det(final)<0: final[0]*=-1
    p0=p@inicial.T
    ids=np.where(p0[:,2]>.07)[0]
    rmax=np.max(np.linalg.norm(p0[:,:2],axis=1))
    candidatos=[i for i in ids if abs(np.linalg.norm(p0[i,:2])-.7*rmax)<.03]
    lateral=np.array([-math.sin(math.radians(30)),math.cos(math.radians(30))])
    candidatos=[i for i in candidatos if np.dot(p0[i,:2],lateral)>.7*np.linalg.norm(p0[i,:2])]
    vista=np.array([math.cos(math.radians(22))*math.cos(math.radians(30)),math.cos(math.radians(22))*math.sin(math.radians(30)),math.sin(math.radians(22))])
    destaque=int(max(candidatos or ids,key=lambda i:np.dot(p0[i],vista)))
    viz=[]
    for x in p:
        n=np.sum(np.linalg.norm(p-x,axis=1)<.049)-1
        viz.append(1-.35*min(1,n/18))
    return dict(posicoes=p.tolist(), inicial=inicial.tolist(), final=final.tolist(), tensor=I.tolist(),
                autovalores=val.tolist(), eixos=eixos.tolist(), destaque=destaque, ao=viz,
                cubo=.03, passo=.034, massa_cubo=.01)

VOX=cria_voxel()
_GAUSS_X,_GAUSS_W=np.polynomial.legendre.leggauss(48)

def deformacao(t):
    """Homotetia sem torque em eixo principal: I cresce com s² e omega cai com s²."""
    t=max(0,float(t));esc=1+.18*math.sin(1.6*t)
    ts=t*.5*(_GAUSS_X+1)
    fase=float(t*.5*np.sum(_GAUSS_W*math.pi/(1+.18*np.sin(1.6*ts))**2))
    return esc,fase,math.pi/esc**2

from functools import lru_cache

@lru_cache(maxsize=256)
def orientacao(u):
    from scipy.spatial.transform import Rotation, Slerp
    return Slerp([0,1],Rotation.from_matrix([VOX['inicial'],VOX['final']]))([np.clip(u,0,1)]).as_matrix()[0]

def voxel(phi,u=0):
    R=rz(phi)@orientacao(u)
    p=np.array(VOX['posicoes'])@R.T
    I=tensor(p,.01)
    l=I@(math.pi*Z)
    r=p[VOX['destaque']]
    li=np.cross(r,.01*np.cross(math.pi*Z,r))
    return dict(O=np.zeros(3),massa=r,r=r,v=np.cross(math.pi*Z,r),L=l,L1=li,
                axial=l*Z,transversal=l*(1-Z),posicoes=p,I=I,rotacao=R)

def roda(phi, balanceada=0):
    # Eixo horizontal y: rotação positiva por regra da mão direita.
    r=np.array([.2*math.cos(phi),.1,-.2*math.sin(phi)])
    w=np.array([0.,(100/3.6)/.3,0.])
    l=2*np.cross(r,.02*np.cross(w,r))
    trans=l*np.array([1,0,1])*(1-balanceada)
    fc=-.02*np.linalg.norm(w)**2*r*np.array([1,0,1])
    torque=np.cross(w,trans)
    fa=-np.cross(np.array([0.,1.,0.]),torque)/.5
    return dict(O=np.zeros(3),massa=r,massa2=-r,r=r,L=l*np.array([0,1,0])*(1+balanceada)+trans,
                axial=l*np.array([0,1,0])*(1+balanceada),transversal=trans,Fc=fc,Fc2=-fc,
                torque=torque,Fa1=fa,Fa2=-fa)

# Plataforma livre (gancho): L constante; I = Ip + 2 m r²; o carretel recolhe as massas de 0,40 m para 0,20 m entre t = 2 e 7 s.
PL_IP,PL_M,PL_R0,PL_R1,PL_T0,PL_T1=.020,.5,.40,.20,2.,8.5
I_RETO=2*MH*LH**2   # haltere reto (α = 90°): I_z = 2 m ℓ²

def _pl_r(t):
    u=min(max((t-PL_T0)/(PL_T1-PL_T0),0.),1.);u=u*u*(3-2*u);return PL_R0+(PL_R1-PL_R0)*u

def _pl_I(r):return PL_IP+2*PL_M*r*r

@lru_cache(maxsize=1)
def _pl_tab():
    dt=1/300;ts=np.arange(0,40+dt,dt);I=np.array([_pl_I(_pl_r(t)) for t in ts]);w=WD*_pl_I(PL_R0)/I
    ph=np.concatenate([[0],np.cumsum(.5*(w[1:]+w[:-1])*dt)]);return ts,w,ph

def plataforma(t):
    ts,w,ph=_pl_tab();t=max(0.,float(t))
    return dict(r=_pl_r(t),omega=float(np.interp(t,ts,w)),phi=float(np.interp(t,ts,ph)),I=_pl_I(_pl_r(t)))

def ang(a,b):
    return math.degrees(math.acos(np.clip(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)),-1,1)))

def tabula():
    p,h,v0,v1,r=pendulo(0),haltere(0),voxel(0),voxel(0,1),roda(0)
    return dict(voxel=VOX,pendulo=dict(omega=WP,periodo=2*math.pi/WP,L=float(np.linalg.norm(p['L'])),Lz=p['L'][2],Lh=float(np.linalg.norm(p['transversal'])),torque=float(np.linalg.norm(p['torque']))),
        haltere=dict(Lz=h['L'][2],Lperp=float(np.linalg.norm(h['transversal'])),torque=float(np.linalg.norm(h['torque'])),F=float(np.linalg.norm(h['Fsup'])),Fc=float(np.linalg.norm(h['Fc'])),angulo=ang(h['L'],Z)),
        voxel_angulos=[ang(v0['L'],Z),ang(v1['L'],Z)],roda=dict(omega=(100/3.6)/.3,Fc=float(np.linalg.norm(r['Fc'])),binario=float(np.linalg.norm(r['torque']))))

if __name__=='__main__':
    t=tabula()
    (U/'tab25.json').write_text(json.dumps(t,ensure_ascii=False,indent=1),encoding='utf-8')
    (U/'threejs/cena3d/fisica25.json').write_text(json.dumps(t),encoding='utf-8')
    print(json.dumps({k:v for k,v in t.items() if k!='voxel'},indent=1))
    print('Cubinhos:',len(VOX['posicoes']))
