"""Encenação local: projeção comum, esfera opaca iluminada e relevo do canhão.

Coordenadas gráficas em R_T. O estado SI nunca é modificado pela câmera.
Volume procedural no Manim/Cairo; nenhum Blender, textura externa ou dependência nova.
"""
from functools import lru_cache
import math
import numpy as np
from manim import (Circle, Dot, Group, ImageMobject, Line, Polygon, ValueTracker,
                   VGroup, VMobject, DashedVMobject)
from modelo_orbital import R_T

BLUE='#267BFF'; LIGHT='#7FB2FF'; WHITE='#F5F7FF'; VIOLET='#9C8CFF'


@lru_cache(maxsize=24)
def esfera_rgba(inclinacao=0, giro=0):
    n=512
    yy,xx=np.mgrid[-1:1:complex(n),-1:1:complex(n)]
    yy=-yy
    rr=xx*xx+yy*yy
    zz=np.sqrt(np.maximum(0,1-rr))
    a,b=np.radians(inclinacao),np.radians(giro)
    # Inversa da mesma câmera usada para trajetória, corpo e vetores.
    xr=xx*np.cos(b)+yy*np.sin(b)
    yr=-xx*np.sin(b)+yy*np.cos(b)
    wy=yr*np.cos(a)+zz*np.sin(a)
    wz=-yr*np.sin(a)+zz*np.cos(a)
    lon=np.arctan2(wz,xr); lat=np.arcsin(np.clip(wy,-1,1))
    campo=(np.sin(2.6*lon+.9*np.sin(3*lat)) + .67*np.cos(4.2*lat-lon)
           +.22*np.sin(9*lon+5*lat)+.11*np.cos(19*lon-11*lat))
    terra=campo>.64
    luz=np.maximum(0,(-.58*xr+.72*wy+.38*wz)/1.0)
    base=np.where(terra[...,None],np.array([42,83,126]),np.array([13,44,91]))
    brilho=.18+.82*luz
    rgb=base*brilho[...,None]+np.power(luz,5)[...,None]*np.array([13,22,30])
    # Finos meridianos/paralelos pertencem à superfície, não são overlays fixos.
    grade=(np.abs(np.sin(lon*6))<.017)|(np.abs(np.sin(lat*6))<.017)
    rgb=np.where(grade[...,None],rgb+np.array([8,14,20]),rgb)
    alpha=np.clip((1-rr)*n,0,1)*255
    return np.dstack([np.clip(rgb,0,255).astype(np.uint8),alpha.astype(np.uint8)])


def globo(centro,raio,inclinacao=0,giro=0,opacidade=1):
    im=ImageMobject(esfera_rgba(round(inclinacao),round(giro)))
    im.set_width(max(2*raio,.001)).move_to(centro).set_opacity(opacidade).set_z_index(10)
    return im


class CameraOrbital:
    def __init__(self):
        self.x=ValueTracker(0); self.y=ValueTracker(1.035)
        self.span=ValueTracker(.30); self.incl=ValueTracker(0)
        self.roll=ValueTracker(0); self.stretch=ValueTracker(1)
        self.ax=ValueTracker(0); self.ay=ValueTracker(-.2)

    @property
    def k(self): return 13.6/self.span.get_value()

    def transformar(self,p):
        arr=np.asarray(p,dtype=float)
        if arr.ndim==1: arr=arr[None,:]
        if arr.shape[1]==2: arr=np.column_stack([arr,np.zeros(len(arr))])
        a,b=self.incl.get_value(),self.roll.get_value()
        x=arr[:,0]-self.x.get_value()
        y=(arr[:,1]-self.y.get_value())*self.stretch.get_value()
        z=arr[:,2]
        yp=y*np.cos(a)-z*np.sin(a)
        return np.column_stack([(x*np.cos(b)-yp*np.sin(b))*self.k+self.ax.get_value(),
                                (x*np.sin(b)+yp*np.cos(b))*self.k+self.ay.get_value(),
                                np.zeros(len(arr))])

    def p(self,p): return self.transformar(p)[0]

    def si(self,p): return self.p(np.asarray(p)/R_T)

    def visivel(self,p,centro):
        d=np.asarray(p)-np.asarray(centro)
        a=self.incl.get_value()
        depth=d[1]*np.sin(a)+(d[2] if len(d)>2 else 0)*np.cos(a)
        tela=self.p(p)-self.p(centro)
        return not(depth < -1e-7 and np.linalg.norm(tela[:2])<self.k)

    def linha(self,pontos,cor=BLUE,largura=2.5,centro=(0,0),ocultar=True,tracejado=False):
        ps=np.asarray(pontos)
        if len(ps)<2: ps=np.vstack([ps,ps])
        mask=np.ones(len(ps),dtype=bool)
        if ocultar and abs(self.incl.get_value())>.02:
            d=ps[:,:2]-np.asarray(centro)[:2]
            depth=d[:,1]*np.sin(self.incl.get_value())
            dif=self.transformar(ps)-self.p(centro)
            mask=~((depth < -1e-7)&(np.linalg.norm(dif[:,:2],axis=1)<self.k))
        telas=self.transformar(ps)
        janela=(np.abs(telas[:,0])<9)&(np.abs(telas[:,1])<5)
        # Conserva o vizinho de entrada/saída para o recorte não abrir lacunas.
        janela=janela|np.r_[False,janela[:-1]]|np.r_[janela[1:],False]
        mask &= janela
        grupos=VGroup(); inicio=None
        for i,ok in enumerate(np.append(mask,False)):
            if ok and inicio is None: inicio=i
            if not ok and inicio is not None:
                if i-inicio>1:
                    parte=telas[inicio:i]
                    if len(parte)>600:
                        parte=parte[np.linspace(0,len(parte)-1,600,dtype=int)]
                    m=VMobject().set_points_as_corners(parte).set_stroke(cor,largura).set_fill(opacity=0)
                    if tracejado: m=DashedVMobject(m,num_dashes=max(8,min(90,(i-inicio)//5)),dashed_ratio=.52)
                    grupos.add(m)
                inicio=None
        return grupos.set_z_index(20)

    def planeta(self,centro=(0,0),opacidade=1):
        cp=self.p(centro); k=self.k
        if k<26:
            if abs(cp[0])-k>9 or abs(cp[1])-k>5:
                return globo([0,0,0],.001,opacidade=0)
            return globo(cp,k,np.degrees(self.incl.get_value()),np.degrees(self.roll.get_value()),opacidade)
        # Horizonte local: evita ampliar uma imagem para milhões de pixels.
        foco=np.array([self.x.get_value(),self.y.get_value()])-np.asarray(centro)
        theta=math.atan2(foco[0],foco[1]); delta=min(.5,11/k)
        th=np.linspace(theta-delta,theta+delta,90)
        arco=np.column_stack([np.sin(th),np.cos(th)])+centro
        t=self.transformar(arco)
        if np.max(t[:,1]) < -5:
            return VGroup()
        poly=Polygon(*t,[12,-12,0],[-12,-12,0],stroke_width=0,
                     fill_color='#153859',fill_opacity=opacidade).set_z_index(10)
        borda=VMobject().set_points_as_corners(t).set_stroke(LIGHT,1.7,opacity=opacidade).set_fill(opacity=0).set_z_index(11)
        return VGroup(poly,borda)

    def montanha(self):
        p=self.p
        face=Polygon(*[p(x) for x in [(-.075,.997),(-.047,1.012),(-.026,1.041),(-.012,1.052),(.008,1.052),(.029,1.025),(.061,.998)]],
                     color='#7895AF',stroke_width=.8,fill_color='#36546E',fill_opacity=1)
        sombra=Polygon(*[p(x) for x in [(-.012,1.052),(.008,1.052),(.029,1.025),(.061,.998),(.006,1.01)]],
                       stroke_width=0,fill_color='#172E48',fill_opacity=1)
        camada=VGroup(*[Line(p(a),p(b),color='#526F85',stroke_width=.8) for a,b in [
            ((-.047,1.012),(.016,1.017)),((-.026,1.041),(.016,1.033)),((-.060,1.003),(.032,1.004))]])
        plat=Polygon(*[p(x) for x in [(-.023,1.050),(.006,1.050),(.006,1.053),(-.023,1.053)]],
                     color='#A7BAC9',fill_color='#61788C',fill_opacity=1,stroke_width=1)
        tubo=Polygon(*[p(x) for x in [(-.018,1.057),(.001,1.057),(.001,1.061),(-.018,1.061)]],
                     color=WHITE,stroke_width=1,fill_color='#738DA4',fill_opacity=1)
        roda=Circle(radius=max(.0001,.0038*self.k),color='#C5D5E0',stroke_width=1.3,
                    fill_color='#19283B',fill_opacity=1).move_to(p((-.011,1.053)))
        return VGroup(face,sombra,camada,plat,tubo,roda).set_z_index(25)
