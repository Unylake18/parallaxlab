"""Primitivas locais sobre o kit copiado: paleta sem pintar operadores e aparatos 2D."""
import re
from prob2 import *
import fisica as fis

CORES={'M':MAS,'m':MAS,'I':MAS,r'\sigma':MAS,r'\theta':ANG,r'\Delta':ANG,r'\omega':VEL,'v':VEL,
       r'\alpha':ACC,'a':ACC,'g':ACC,'F':FC,'T':FC,'N':FC,r'\tau':FC,'f':FC,
       'K':KC,'U':KC,'W':KC,'P':KC,'h':GEO,'R':GEO,'r':GEO,'d':GEO,'L':GEO,'l':GEO}
_TEX={}
_TEMPLATE=TexTemplate()
_TEMPLATE.add_to_preamble(r'\usepackage{xcolor}')

def cor_tex(s,periodo=False):
    saved=[]
    def hold(m):
        saved.append(m.group());return f'§{len(saved)-1}§'
    s=re.sub(r'\\(?:mathrm|operatorname|text)\{[^}]*\}',hold,s)
    pattern=r'§\d+§|(?:\\[a-zA-Z]+|mgh|Mg|mg|[a-zA-Z])(?:_(?:\{[^{}]*\}|\\[a-zA-Z]+|[a-zA-Z0-9]))?'
    def sub(m):
        v=m.group()
        if v.startswith('§'):return v
        base=v.split('_',1)[0]
        c=KC if base=='mgh' else FC if base in ('Mg','mg') else CORES.get(base)
        if periodo and base=='T':c=None
        return r'{\color[HTML]{'+c.lstrip('#')+'}'+v+'}' if c else v
    s=re.sub(pattern,sub,s)
    for i,v in enumerate(saved):s=s.replace(f'§{i}§',v)
    return s

def Q(s,size=46,periodo=False):
    key=(s,size,periodo)
    if key not in _TEX:
        m=MathTex(cor_tex(s,periodo),font_size=size,tex_template=_TEMPLATE)
        m._tam=size;m._raw=s;m._partes=[(s,None)]
        _TEX[key]=m
    return _TEX[key].copy()

def label(s,p,color=None,size=36,periodo=False):
    m=Q(s,size,periodo).move_to(p)
    if color:m.set_color(color)
    return m.set_z_index(15)

def cruz(p,r=.08):
    return VGroup(Circle(radius=r,color=WHITE_).move_to(p),Line(p+LEFT*r,p+RIGHT*r,color=WHITE_),Line(p+DOWN*r,p+UP*r,color=WHITE_))

def barra(valor,total,pos,w=4.8,cor=KC):
    base=RoundedRectangle(width=w,height=.19,corner_radius=.04).set_fill(PANEL,1).set_stroke(GEO,.8).move_to(pos)
    n=max(.001,min(1,valor/total))*w
    fill=Rectangle(width=n,height=.17).set_fill(cor,1).set_stroke(width=0).move_to(pos+LEFT*(w-n)/2)
    return VGroup(base,fill)

def haste(th,modo=0):
    o=P3(-4.65,.3);u=np.array([math.cos(th),-math.sin(th),0]);cm=o+1.1*u
    p=o-1.1*u;q=o+3.3*u
    body=Line(p,q).set_stroke(STEEL,14);edge=Line(p+.04*UP,q+.04*UP).set_stroke(GEO,2)
    g=VGroup(body,edge,cruz(o,.11),cruz(cm,.095))
    g.add(label('M',cm+UP*.43,MAS),label('d',P3(-4.05,1.8),GEO))
    if modo>=1:
        g.add(seta(cm,cm+DOWN*1.2,FC,5),label('Mg',cm+RIGHT*.65+DOWN*.7,FC))
        v=fis.forca(th);end=o+1.2*P3(v['fx'],v['fy'])
        g.add(seta(o,end,FC,5),label(r'\vec F',end+LEFT*.37,FC))
        if modo>=2:
            at=v['at']/fis.G*1.2*np.array([-math.sin(th),-math.cos(th),0]);ac=-v['ac']/fis.G*1.2*u
            if np.linalg.norm(at)>.02:
                g.add(seta(cm,cm+at,ACC,5),label('a_t',cm+at+RIGHT*.35,ACC))
            if np.linalg.norm(ac)>.02:
                g.add(seta(cm,cm+ac,ACC,5),label('a_c',cm+ac+LEFT*.35,ACC))
        if modo==3:
            corner=o+1.2*P3(v['fx'],0)
            g.add(DashedLine(o,corner,color=FC),DashedLine(corner,end,color=FC))
    if th>.02:g.add(Arc(radius=.6,start_angle=-th,angle=th,arc_center=o,color=ANG),label(r'\theta',o+P3(.9,-.2),ANG))
    g._objeto=True
    return g

def pendulo(l,t=0,duplo=True,x=-4.7,scale=8.2,simples=False,ang=None):
    o=P3(x,1.7);th=math.radians(5)*math.cos(2*math.pi*t/fis.periodo(l,duplo)) if ang is None else ang
    u=np.array([math.sin(th),-math.cos(th),0]);c=o+scale*l*u
    g=VGroup(Line(o,c,color=GEO,stroke_width=3))
    if duplo:g.add(Circle(radius=scale*.1).set_fill(STEEL,1).set_stroke(GEO,2).move_to(o))
    g.add(Circle(radius=.1 if simples else scale*.1).set_fill(MAS if simples else STEEL,1).set_stroke(MAS if simples else GEO,2).move_to(c))
    g.add(cruz(o,.085),cruz(c,.055),label('l',o+(c-o)/2+RIGHT*.4,GEO),label('M',c+LEFT*(.1*scale+.3),MAS))
    if not simples:g.add(label('R',c+RIGHT*(.1*scale+.26),GEO))
    return g

def curva_periodo(l,x0=.8,y0=-2.95,w=5.85,h=1.75):
    def p(v):return P3(x0+w*(v-.02)/.38,y0+h*(fis.periodo(v)-.7)/.6)
    axes=VGroup(Line(P3(x0,y0),P3(x0+w,y0),color=GEO),Line(P3(x0,y0),P3(x0,y0+h),color=GEO))
    curve=VMobject().set_points_as_corners([p(v) for v in np.linspace(.02,.4,160)]).set_stroke(WHITE_,3)
    dot=Dot(p(l),radius=.075,color=ANG)
    labs=VGroup(label('T',P3(x0-.25,y0+h),size=30,periodo=True),label('l',P3(x0+w+.2,y0),size=30))
    for v in [.05,.07071,.1,.2,.3,.4]:
        xp=x0+w*(v-.02)/.38
        axes.add(Line(P3(xp,y0),P3(xp,y0-.08),color=GEO))
    return VGroup(axes,curve,dot,labs)
