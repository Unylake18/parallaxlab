"""Material terrestre amostrado no recorte visível, à resolução da saída.

Um único campo de iluminação e material serve a globo e horizonte. O cache
retém só dois recortes RGBA; nunca se amplia uma textura de resolução fixa.
"""
from functools import lru_cache
import math
import numpy as np
from manim import config, Group, VGroup, ImageMobject, VMobject, Circle

BLUE='#267BFF'; WHITE='#F5F7FF'; VIOLET='#745CFF'


def suave(a,b,x):
    t=np.clip((x-a)/(b-a),0,1)
    return t*t*(3-2*t)


@lru_cache(maxsize=2)
def recorte_rgba(cx,cy,k,incl,roll,fw,fh,pw,ph):
    pp=pw/fw
    x0=max(0,math.floor((cx-k+fw/2)*pp)-2)
    x1=min(pw,math.ceil((cx+k+fw/2)*pp)+2)
    y0=max(0,math.floor((fh/2-cy-k)*pp)-2)
    y1=min(ph,math.ceil((fh/2-cy+k)*pp)+2)
    if x1<=x0 or y1<=y0:
        return None
    # Centros dos pixels em coordenadas lógicas do próprio frame.
    x=(np.arange(x0,x1,dtype=float)[None,:]+.5)/pp-fw/2
    y=fh/2-(np.arange(y0,y1,dtype=float)[:,None]+.5)/pp
    xx=(x-cx)/k; yy=(y-cy)/k
    rr=xx*xx+yy*yy
    zz=np.sqrt(np.maximum(0,1-rr))
    xr=xx*np.cos(roll)+yy*np.sin(roll)
    yr=-xx*np.sin(roll)+yy*np.cos(roll)
    wy=yr*np.cos(incl)+zz*np.sin(incl)
    wz=-yr*np.sin(incl)+zz*np.cos(incl)
    luz=np.clip(-.58*xr+.72*wy+.38*wz,0,1)
    detalhe=1-float(suave(4,22,k))
    material=np.full(rr.shape,.36,dtype=np.float32)
    grade=0
    if detalhe>.001:
        lon=np.arctan2(wz,xr); lat=np.arcsin(np.clip(wy,-1,1))
        campo=(np.sin(2.6*lon+.9*np.sin(3*lat))+.67*np.cos(4.2*lat-lon)
               +.22*np.sin(9*lon+5*lat)+.11*np.cos(19*lon-11*lat))
        terra=suave(.59,.69,campo)
        material += detalhe*(terra-.35)*.22
        grade=detalhe*.055*(1-suave(.012,.032,np.minimum(np.abs(np.sin(lon*6)),np.abs(np.sin(lat*6)))))
    fator=material*(.24+.76*luz)+grade
    rgb=fator[...,None]*np.array([38,123,255])+luz[...,None]**5*np.array([245,247,255])*.045
    # Distância assinada à silhueta, estável também em aumentos extremos.
    distancia=k*(1-rr)/(1+np.sqrt(rr))
    alpha=np.clip(.5+distancia*pp,0,1)*255
    rgba=np.dstack([np.clip(rgb,0,255).astype(np.uint8),alpha.astype(np.uint8)])
    centro=np.array([(x0+x1)/2/pp-fw/2,fh/2-(y0+y1)/2/pp,0])
    return rgba,centro,(x1-x0)/pp,(y1-y0)/pp


def superficie(centro,raio,incl=0,roll=0,opacidade=1):
    cx,cy=float(centro[0]),float(centro[1]); k=max(float(raio),1e-8)
    fw,fh=float(config.frame_width),float(config.frame_height)
    pw,ph=int(config.pixel_width),int(config.pixel_height)
    dados=recorte_rgba(cx,cy,k,float(incl),float(roll),fw,fh,pw,ph)
    if dados is None: return Group()
    rgba,cp,w,h=dados
    im=ImageMobject(rgba).stretch_to_fit_width(w).stretch_to_fit_height(h).move_to(cp).set_opacity(opacidade).set_z_index(10)
    # O contorno é geométrico em qualquer escala, independente do material.
    if k<12:
        borda=Circle(radius=k,stroke_color=BLUE,stroke_width=1.15,stroke_opacity=opacidade).move_to(centro)
    else:
        theta=math.atan2(-cy,-cx)
        delta=min(math.pi,1.5*math.asin(min(1,math.hypot(fw,fh)/k)))
        ang=np.linspace(theta-delta,theta+delta,240)
        ps=np.column_stack([cx+k*np.cos(ang),cy+k*np.sin(ang),np.zeros(len(ang))])
        borda=VMobject().set_points_as_corners(ps).set_stroke(BLUE,1.15,opacity=opacidade).set_fill(opacity=0)
    borda.set_z_index(11)
    return Group(im,borda)


def lua_visual(centro,raio):
    """Disco e crateras vetoriais, sem textura de resolução fixa."""
    from manim import interpolate_color, ManimColor
    r=max(.001,float(raio)); cp=np.asarray(centro)
    disco=Circle(r,color=WHITE,stroke_width=1,fill_color=interpolate_color(ManimColor(BLUE),ManimColor(WHITE),.58),fill_opacity=1).move_to(cp)
    ang=np.linspace(-np.pi/2,np.pi/2,90)
    externo=np.column_stack([r*np.cos(ang),r*np.sin(ang),np.zeros(len(ang))])+cp
    interno=np.column_stack([.25*r*np.cos(ang),r*np.sin(ang),np.zeros(len(ang))])+cp
    sombra=VMobject().set_points_as_corners(np.vstack([externo,interno[::-1],externo[:1]])).set_fill(BLUE,.33).set_stroke(width=0)
    crateras=VGroup()
    nivel=float(suave(.14,.35,r))
    for x,y,s in [(-.32,.35,.15),(-.28,-.27,.20),(.28,.17,.10),(.12,-.51,.08)]:
        crateras.add(Circle(s*r,stroke_color=BLUE,stroke_width=max(.4,min(1.3,r)),stroke_opacity=nivel,fill_color=BLUE,fill_opacity=.16*nivel).move_to(cp+r*np.array([x,y,0])))
    return VGroup(disco,sombra,crateras).set_z_index(35)
