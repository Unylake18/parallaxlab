"""Seis alternativas originais; preserva o compositor e os assets aprovados.

Diagramas vetoriais desenhados em resolução dupla, sem alterar o ambiente Manim.
"""
import ast
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
OUT = UNIT / 'capas_codex'
FONTS = ROOT / 'assets/fonts/space_grotesk'
BOLD = str(FONTS / 'SpaceGrotesk-Bold.ttf')
MEDIUM = str(FONTS / 'SpaceGrotesk-Medium.ttf')
CYAN, WHITE, BLUE, VIOLET, MAGENTA = '#35D9FF', '#F5F7FF', '#267BFF', '#745CFF', '#EA63FF'

# Reutiliza somente as funções do compositor Pillow, sem importar cenas ou Manim.
source = ROOT / 'videos/vid_0009_campo_solenoide/gerar_capa.py'
names = {'gradient', 'encolher_logo', 'desenhar_moldura', 'base', 'glow_paste',
         'text_mask', 'fit', 'center', 'headline_line', 'cover'}
tree = ast.parse(source.read_text(encoding='utf-8'))
ns = dict(np=np, Image=Image, ImageDraw=ImageDraw, ImageFilter=ImageFilter,
          ImageFont=ImageFont, BASE=ROOT / 'videos/vid_0002_integral_substituicao/capa_instagram.png',
          BOLD=BOLD, MEDIUM=MEDIUM, LOGO_K=.78, MOLDURA=(120, 1146, 960, 1474),
          ART_MAX=(780, 275), SERIE='EXERCÍCIO RESOLVIDO · EP. 05',
          BRAND=[(53, 217, 255), (38, 123, 255), (116, 92, 255), (234, 99, 255)])
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef)
                             and n.name in names], type_ignores=[]), str(source), 'exec'), ns)

W, H = 1560, 550


class Panel:
    def __init__(self):
        self.image = Image.new('RGBA', (W, H))
        self.d = ImageDraw.Draw(self.image)

    def label(self, text, xy, size=52, color=WHITE, anchor='mm'):
        self.d.text(xy, text, font=ImageFont.truetype(MEDIUM, size), fill=color, anchor=anchor)

    def line(self, pts, color=CYAN, width=7):
        self.d.line(pts, fill=color, width=width, joint='curve')

    def dot(self, xy, color=WHITE, r=11):
        x, y = xy
        self.d.ellipse((x-r, y-r, x+r, y+r), fill=color)

    def dash(self, a, b, color=VIOLET, width=4):
        a, b = np.array(a), np.array(b)
        length = np.linalg.norm(b-a)
        for t in np.arange(0, length, 26):
            self.line([tuple(a+(b-a)*t/length), tuple(a+(b-a)*min(t+13, length)/length)], color, width)

    def arrow(self, a, b, color=CYAN, width=8):
        self.line([a, b], color, width)
        v = np.array(b, dtype=float)-a
        v /= np.linalg.norm(v)
        q = np.array(b)-v*25
        perp = np.array([-v[1], v[0]])*13
        self.d.polygon([tuple(b), tuple(q+perp), tuple(q-perp)], fill=color)

    def sphere(self, cx, cy, radius=190, cut=False):
        # Iluminação volumétrica; a densidade diminui do centro à borda.
        r = radius
        yy, xx = np.mgrid[-r:r+1, -r:r+1]
        dist = np.sqrt(xx*xx+yy*yy)/r
        z = np.sqrt(np.clip(1-dist*dist, 0, 1))
        light = np.clip(.25+.6*z-.23*xx/r-.26*yy/r, 0, 1)
        c = np.zeros((2*r+1, 2*r+1, 4), dtype=np.uint8)
        c[:, :, 0] = np.clip(30+135*(1-dist)+35*light, 0, 255)
        c[:, :, 1] = np.clip(30+25*light+25*(1-dist), 0, 255)
        c[:, :, 2] = np.clip(100+110*light, 0, 255)
        c[:, :, 3] = np.where(dist<=1, 245, 0)
        self.image.alpha_composite(Image.fromarray(c), (cx-r, cy-r))
        self.d.ellipse((cx-r, cy-r, cx+r, cy+r), outline='#7FB2FF', width=7)
        if cut:
            for k in (.33, .66):
                t = r*k
                self.d.ellipse((cx-t, cy-t, cx+t, cy+t), outline=(234, 99, 255, 150), width=3)
        else:
            self.d.ellipse((cx-r, cy-r*.34, cx+r, cy+r*.34), outline=(127,178,255,150), width=3)
            self.d.ellipse((cx-r*.38, cy-r, cx+r*.38, cy+r), outline=(127,178,255,150), width=3)
        self.dot((cx,cy), MAGENTA, 8)

    def graph(self, x0=710, y0=445, width=720, height=300, region=False):
        xmax=2.0
        point=lambda x: (x0+width*x/xmax, y0-height*((x/3-x*x/4) if x<=1 else 1/(12*x*x))*9)
        if region:
            pts=[(x0,y0)]+[point(x) for x in np.linspace(0,1,100)]+[(x0+width/2,y0)]
            self.d.polygon(pts, fill=(116,92,255,35))
        self.arrow((x0,y0),(x0+width+25,y0), '#A3AECA', 4)
        self.arrow((x0,y0),(x0,y0-height-40), '#A3AECA', 4)
        self.label('E', (x0-36,y0-height-27), 46, CYAN)
        self.label('r', (x0+width+25,y0+40), 42)
        curve=[point(x) for x in np.linspace(0,xmax,350)]
        self.line(curve, CYAN, 10)
        peak=point(2/3)
        border=point(1)
        self.dash((border[0],y0), border, MAGENTA)
        self.dot(border,MAGENTA,10)
        self.label('R',(border[0],y0+45),44,MAGENTA)
        self.dot(peak,WHITE,16)
        return peak,border,point


def panel(n):
    p=Panel()
    if n==1:
        p.sphere(340,280,190,True)
        p.d.ellipse((215,155,465,405),outline=CYAN,width=8)
        p.arrow((340,280),(465,280),WHITE,5)
        p.dot((465,280),WHITE,13)
        p.label('INTERIOR',(340,505),42,CYAN)
        peak,_,_=p.graph(760,440,620,270)
        p.label('máximo',(peak[0]+40,peak[1]-52),48)
        p.arrow((570,280),(660,280),WHITE,7)
    elif n==2:
        p.sphere(320,275,180,True)
        p.dot((440,275),CYAN,14)
        p.dot((500,275),MAGENTA,13)
        p.line([(440,275),(440,95),(650,95)],CYAN,4)
        p.line([(500,275),(590,370),(650,370)],MAGENTA,4)
        p.label('DENTRO',(730,95),42,CYAN,anchor='lm')
        p.arrow((740,180),(1320,180),CYAN,16)
        p.label('NA SUPERFÍCIE',(730,365),42,MAGENTA,anchor='lm')
        p.arrow((740,450),(1175,450),MAGENTA,12)
        p.label('E',(1385,290),90,WHITE)
    elif n==3:
        peak,border,_=p.graph(170,425,1170,300,True)
        p.dash((peak[0],425),peak,CYAN)
        p.label('?',(peak[0],peak[1]-58),72)
        p.label('dentro',(360,492),42,'#9C8CFF')
        p.label('fora',(1110,492),42,'#A3AECA')
    elif n==4:
        p.sphere(300,280,178,True)
        p.label('ρ(r)',(300,50),57,MAGENTA)
        p.arrow((590,280),(750,280),WHITE,8)
        p.label('GAUSS',(665,205),35,'#A3AECA')
        p.graph(890,430,505,270)
        p.label('E(r)',(1180,56),57,CYAN)
    elif n==5:
        peak,_,_=p.graph(160,445,1150,300)
        p.arrow((330,355),(460,213),CYAN,11)
        p.arrow((835,245),(985,333),'#9C8CFF',11)
        p.label('SOBE',(215,190),43,CYAN)
        p.label('DESCE',(1170,228),43,'#9C8CFF')
        p.label('ATÉ AQUI?',(peak[0]+40,65),49)
    else:
        p.sphere(360,285,192,True)
        p.d.ellipse((232,157,488,413),outline=CYAN,width=8)
        p.dot((488,285),WHITE,15)
        p.line([(488,285),(650,285)],WHITE,4)
        p.label('r = ?',(990,240),112,CYAN)
        p.label('CAMPO MÁXIMO',(990,365),43,WHITE)
    return p.image


TITLES={
    1:('O MÁXIMO','ESTÁ LÁ DENTRO?'),
    2:('A BORDA PERDE','PARA O INTERIOR?'),
    3:('ACHE O PONTO','DE CAMPO MÁXIMO'),
    4:('CARGA DESIGUAL.','E O CAMPO?'),
    5:('O CAMPO CRESCE.','ATÉ QUANDO?'),
    6:('UMA ESFERA.','UM PICO ESCONDIDO.'),
}


if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    for n,(a,b) in TITLES.items():
        size=min(ns['fit'](t,BOLD,870,150).size for t in (a,b))
        lines=[([(a,'white')],size), ([(b,'grad')],size)]
        img=ns['cover'](lines,panel(n))
        assert img.size==(1080,1920)
        img.save(OUT/f'capa_codex_{n:02d}.png',optimize=True)
    contact=Image.new('RGB',(1200,1480),'#050816')
    d=ImageDraw.Draw(contact)
    for n in range(1,7):
        x=30+400*((n-1)%3)
        y=65+740*((n-1)//3)
        img=Image.open(OUT/f'capa_codex_{n:02d}.png')
        contact.paste(img.resize((360,640),Image.Resampling.LANCZOS),(x,y))
        d.text((x,y-42),f'{n:02d} / CODEX',font=ImageFont.truetype(MEDIUM,26),fill=WHITE)
    contact.save(OUT/'comparativo_codex.png')
    print('Seis capas 1080×1920 + comparativo:',OUT)
