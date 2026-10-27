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
from superficie import superficie

BLUE='#267BFF'; LIGHT=BLUE; WHITE='#F5F7FF'; VIOLET='#745CFF'


def globo(centro,raio,inclinacao=0,giro=0,opacidade=1):
    return superficie(centro,raio,np.radians(inclinacao),np.radians(giro),opacidade)


class CameraOrbital:
    def __init__(self):
        self.x=ValueTracker(0); self.y=ValueTracker(1.035)
        self.span=ValueTracker(.30); self.incl=ValueTracker(0)
        self.roll=ValueTracker(0); self.stretch=ValueTracker(1)
        self.ax=ValueTracker(0); self.ay=ValueTracker(-.2)
        self.janela=None  # (xmin,xmax,ymin,ymax) em tela; recorta previsões e marca a continuação

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

    def linha(self,pontos,cor=BLUE,largura=2.5,centro=(0,0),ocultar=True,tracejado=False,janela=None):
        ps=np.asarray(pontos)
        if len(ps)<2: ps=np.vstack([ps,ps])
        mask=np.ones(len(ps),dtype=bool)
        if ocultar and abs(self.incl.get_value())>.02:
            d=ps[:,:2]-np.asarray(centro)[:2]
            depth=d[:,1]*np.sin(self.incl.get_value())
            dif=self.transformar(ps)-self.p(centro)
            mask=~((depth < -1e-7)&(np.linalg.norm(dif[:,:2],axis=1)<self.k))
        telas=self.transformar(ps)
        jan=janela or self.janela
        if jan: dentro=(telas[:,0]>jan[0])&(telas[:,0]<jan[1])&(telas[:,1]>jan[2])&(telas[:,1]<jan[3])
        else: dentro=(np.abs(telas[:,0])<9)&(np.abs(telas[:,1])<5)
        janela=dentro
        # Conserva o vizinho de entrada/saída para o recorte não abrir lacunas.
        if not jan: janela=janela|np.r_[False,janela[:-1]]|np.r_[janela[1:],False]
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
                    if jan and i<len(ps) and i-inicio>3:
                        # continuação: seta pequena no ponto onde a janela corta
                        d=parte[-1]-parte[-4]; d=d/max(np.linalg.norm(d),1e-9)
                        ponta=Polygon(parte[-1]+.16*d,parte[-1]-.08*d+.1*np.array([-d[1],d[0],0]),
                                      parte[-1]-.08*d-.1*np.array([-d[1],d[0],0]),
                                      stroke_width=0,fill_color=cor,fill_opacity=1)
                        grupos.add(ponta)
                inicio=None
        return grupos.set_z_index(20)

    def planeta(self,centro=(0,0),opacidade=1):
        return superficie(self.p(centro),self.k,self.incl.get_value(),self.roll.get_value(),opacidade)

    def montanha(self):
        p=self.p
        face=Polygon(*[p(x) for x in [(-.075,.997),(-.047,1.012),(-.026,1.041),(-.012,1.052),(.008,1.052),(.029,1.025),(.061,.998)]],
                     color='#7895AF',stroke_width=.8,fill_color='#36546E',fill_opacity=1)
        sombra=Polygon(*[p(x) for x in [(-.012,1.052),(.008,1.052),(.029,1.025),(.061,.998),(.006,1.01)]],
                       stroke_width=0,fill_color='#172E48',fill_opacity=1)
        camada=VGroup(*[Line(p(a),p(b),color='#526F85',stroke_width=.8) for a,b in [
            ((-.047,1.012),(.016,1.017)),((-.026,1.041),(.016,1.033)),((-.060,1.003),(.032,1.004))]])
        plat=Polygon(*[p(x) for x in [(-.044,1.050),(.006,1.050),(.006,1.053),(-.044,1.053)]],
                     color='#A7BAC9',fill_color='#61788C',fill_opacity=1,stroke_width=1)
        from manim import RoundedRectangle, Ellipse
        # Boca à direita, pedra fora do tubo e duas rodas sob o suporte.
        suporte=Polygon(*[p(x) for x in [(-.030,1.049),(.000,1.049),(-.005,1.058),(-.025,1.058)]],
                        stroke_color=BLUE,fill_color='#142C59',fill_opacity=1,stroke_width=1.2)
        tubo=RoundedRectangle(width=.032,height=.009,corner_radius=.003,
                              stroke_color=WHITE,stroke_width=1.2,fill_color='#506AA1',fill_opacity=1).move_to([-.023,1.060,0])
        tubo.apply_function(lambda q:p(q[:2]))
        culatra=Ellipse(width=max(.0001,.005*self.k),height=max(.0001,.010*self.k),
                        stroke_color=WHITE,stroke_width=1,fill_color='#203D75',fill_opacity=1).move_to(p((-.039,1.060)))
        boca=Ellipse(width=max(.0001,.0035*self.k),height=max(.0001,.010*self.k),
                     stroke_color=WHITE,stroke_width=1.8,fill_color='#050816',fill_opacity=1).move_to(p((-.007,1.060)))
        rodas=VGroup()
        for x in (-.024,-.008):
            cp=p((x,1.050)); r=max(.0001,.0046*self.k)
            rodas.add(Circle(r,color=WHITE,stroke_width=1.4,fill_color='#0E1D44',fill_opacity=1).move_to(cp),
                      Line(cp+[-r*.7,0,0],cp+[r*.7,0,0],color=BLUE,stroke_width=1),
                      Line(cp+[0,-r*.7,0],cp+[0,r*.7,0],color=BLUE,stroke_width=1))
        return VGroup(face,sombra,camada,plat,suporte,rodas,tubo,culatra,boca).set_z_index(25)
