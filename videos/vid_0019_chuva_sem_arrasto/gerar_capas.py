"""Dez capas do EP.02, com o compositor e a arte vetorial das capas anteriores.

uv run --no-sync python videos/vid_0019_chuva_sem_arrasto/gerar_capas.py
Não altera o vídeo, os assets ou as unidades de referência.
"""
from pathlib import Path
import importlib.util
import json
import sys
import zipfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
OUT = UNIT / 'capas_v1'
sys.path.insert(0, str(ROOT))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


g = load('cover19_base9', ROOT/'videos/vid_0009_campo_solenoide/gerar_capa.py')
d = load('cover19_draw10', ROOT/'videos/vid_0010_looping_esfera/gerar_capas.py')
g.SERIE = 'ABSURDO CALCULÁVEL · EP. 02'
S = d.S
CY, BL, VI, MG, WH = g.CYAN, g.BLUE, '#9C8CFF', g.MAGENTA, g.WHITE
DIM = '#B2BDDA'


class Art(d.Cena):
    def text(self, x, y, content, size=30, color=WH, bold=False):
        font = d.fnt('bold' if bold else 'medium', size)
        box = font.getbbox(content, anchor='mm')
        assert x*S+box[0] >= 0 and x*S+box[2] <= self.img.width, content
        assert y*S+box[1] >= 0 and y*S+box[3] <= self.img.height, content
        self.texto((x, y), content, font, color)

    def sphere(self, x, y, radius, color=CY, trail=True):
        if trail:
            for offset, height in ((-.65,45),(0,68),(.65,53)):
                xx = x+offset*radius
                self.linha([(xx,max(9,y-radius-height)),(xx,y-radius-7)],color,2,3,alfa=100)
        n = round(2*radius*S)+6
        yy,xx = np.mgrid[0:n,0:n]
        u,v = (xx-n/2)/(radius*S),(yy-n/2)/(radius*S)
        rho = np.hypot(u,v)
        light = np.clip(1-np.hypot(u+.32,v+.4)/1.4,0,1)
        core = np.array(d.rgb(color),float)
        pixels = np.zeros((n,n,4),dtype=np.uint8)
        rgb = np.array([7,19,61])+(core-np.array([7,19,61]))*light[...,None]**1.35
        rgb += 135*np.exp(-((u+.36)**2+(v+.42)**2)/.035)[...,None]
        pixels[:,:,:3] = np.clip(rgb,0,255).astype(np.uint8)
        pixels[:,:,3] = np.where(rho<=1,255,0)
        layer = self.camada()
        layer.alpha_composite(Image.fromarray(pixels), (round((x-radius)*S)-3,round((y-radius)*S)-3))
        ImageDraw.Draw(layer).ellipse(((x-radius)*S,(y-radius)*S,(x+radius)*S,(y+radius)*S),outline=d.rgb(color)+(255,),width=round(2.3*S))
        self.cola(layer,7,.65)

    def rect(self, box, color, opacity=235):
        layer = self.camada()
        ImageDraw.Draw(layer).rounded_rectangle(tuple(v*S for v in box),radius=3*S,fill=d.rgb(color)+(opacity,))
        self.cola(layer,5,.4)

    def footer(self, content='SEM ARRASTO · 2 km · gota intacta por hipótese'):
        self.text(390,255,content,22,DIM)


def falling():
    a=Art()
    a.sphere(170,145,53)
    a.seta((270,68),(270,211),CY,6,21)
    a.text(520,113,'713',120,CY,True)
    a.text(520,194,'km/h',47,WH)
    a.footer()
    return a.img


def speedometer():
    a=Art()
    cx,cy,r=170,180,113
    angles=np.linspace(np.pi,2*np.pi,100)
    a.linha([(cx+r*np.cos(t),cy+r*np.sin(t)) for t in angles],VI,4,4)
    for t in np.linspace(np.pi,2*np.pi,11):
        a.linha([(cx+(r-12)*np.cos(t),cy+(r-12)*np.sin(t)),(cx+r*np.cos(t),cy+r*np.sin(t))],WH,2,1)
    a.seta((cx,cy),(cx+87,cy-50),CY,6,16)
    a.particula(cx,cy,7,CY)
    a.text(cx,215,'VELOCIDADE',24,DIM)
    a.text(500,120,'713',110,CY,True)
    a.text(500,194,'km/h',44)
    a.sphere(686,149,27)
    a.footer()
    return a.img


def on_off():
    a=Art()
    a.linha([(390,19),(390,233)],VI,1.5,1,alfa=130)
    a.text(190,27,'MUNDO REAL',31,CY,True)
    a.text(590,27,'SEM ARRASTO',31,MG,True)
    a.sphere(170,132,30,trail=False)
    a.seta((232,167),(232,78),MG,5,16)
    a.seta((105,89),(105,170),CY,5,16)
    a.text(190,211,'~2–9 m/s',39,CY,True)
    a.sphere(560,127,30)
    a.seta((642,65),(642,182),MG,6,19)
    a.text(590,211,'713 km/h',42,MG,True)
    a.text(190,255,'Gotas de 0,5–5 mm',22,DIM)
    a.text(590,255,'2 km · gota intacta',22,DIM)
    return a.img


def ruler():
    a=Art()
    a.linha([(265,35),(265,213)],DIM,2,1)
    for y in np.linspace(35,213,7):
        a.linha([(254,y),(276,y)],DIM,2,1)
    a.text(132,124,'2 km',49,WH,True)
    a.sphere(310,40,10,trail=False)
    a.sphere(310,191,22)
    a.text(550,111,'713',108,CY,True)
    a.text(550,188,'km/h',44)
    a.footer()
    return a.img


def same_speed():
    a=Art()
    a.text(390,30,'713 km/h',56,CY,True)
    a.sphere(190,143,23)
    a.sphere(590,143,57.5,VI)
    a.text(190,221,'2 mm',33,CY,True)
    a.text(590,221,'5 mm',33,VI,True)
    a.seta((270,109),(270,177),CY,4,16)
    a.seta((687,109),(687,177),VI,4,16)
    a.footer()
    return a.img


def energy():
    a=Art()
    a.text(205,33,'15,625×',52,WH,True)
    a.sphere(126,129,17)
    a.sphere(310,129,42.5,VI)
    a.text(126,191,'2 mm',29,CY,True)
    a.text(310,191,'5 mm',29,VI,True)
    a.linha([(451,219),(733,219)],DIM,2,1)
    a.rect((485,219-150/15.625,555,219),CY)
    a.rect((647,69,717,219),VI)
    a.text(520,243,'0,082 J',26,CY,True)
    a.text(682,243,'1,28 J',26,VI,True)
    a.text(205,242,'Mesma queda · 2 km',24,DIM)
    return a.img


def terminal():
    a=Art()
    a.sphere(390,129,43,trail=False)
    a.seta((298,181),(298,69),MG,6,19)
    a.seta((482,69),(482,181),CY,6,19)
    a.text(164,125,'ARRASTO',30,MG,True)
    a.text(607,125,'PESO',35,CY,True)
    a.text(390,222,'VELOCIDADE TERMINAL',36,WH,True)
    a.text(390,259,'Força resultante ≈ 0',23,DIM)
    return a.img


def drag_off():
    a=Art()
    a.sphere(154,139,51)
    a.seta((266,192),(266,67),MG,5,17)
    a.linha([(236,150),(295,105)],WH,5,4)
    a.text(510,34,'ARRASTO OFF',31,MG,True)
    a.text(510,115,'198 m/s',72,CY,True)
    a.text(510,193,'≈ 713 km/h',42,WH)
    a.footer()
    return a.img


def aircraft():
    a=Art()
    a.linha([(55,25),(371,25)],CY,1.5,1,alfa=150)
    for x,y in ((82,77),(157,57),(245,78),(341,62)):
        a.sphere(x,y,7,trail=False)
        a.seta((x,y+13),(x,y+42),CY,2,8,2)
    layer=a.camada()
    pts=[(75,150),(245,129),(324,142),(357,153),(230,167),(90,165)]
    ImageDraw.Draw(layer).polygon([(x*S,y*S) for x,y in pts],fill=d.rgb(VI)+(200,))
    a.cola(layer,6,.6)
    a.linha([(210,152),(161,109)],VI,7,3)
    a.linha([(210,152),(164,193)],VI,7,3)
    a.linha([(103,151),(74,122)],VI,5,3)
    a.seta((80,213),(350,213),VI,5,16)
    a.text(570,66,'VELOCIDADE',31,WH,True)
    a.seta((695,128),(455,128),MG,6,22)
    a.text(570,190,'RELATIVA',39,MG,True)
    a.footer('Água em relação à superfície')
    return a.img


def atmosphere():
    a=Art()
    a.linha([(52,53),(727,53)],CY,2,3,alfa=170)
    for x,y in ((91,88),(158,120),(247,92),(548,111),(626,88),(698,124)):
        a.sphere(x,y,6,trail=False)
        a.linha([(x,y-16),(x,y-7)],CY,2,2,alfa=150)
    a.sphere(390,157,36,trail=False)
    a.seta((320,113),(320,204),CY,5,16)
    a.seta((460,204),(460,113),MG,5,16)
    a.text(161,188,'GRAVIDADE',27,CY,True)
    a.text(620,188,'ARRASTO',29,MG,True)
    a.footer('A chuva real encontra uma velocidade terminal')
    return a.img


OPTIONS = [
    ('E SE A CHUVA','PERDESSE O FREIO?',falling),
    ('UMA GOTA A','713 km/h?',speedometer),
    ('O AR FREIA','A CHUVA',on_off),
    ('2 km DE QUEDA.','E SEM ARRASTO?',ruler),
    ('GOTAS DIFERENTES.','MESMA VELOCIDADE.',same_speed),
    ('MESMA VELOCIDADE.','ENERGIAS DIFERENTES.',energy),
    ('POR QUE A CHUVA','PARA DE ACELERAR?',terminal),
    ('SEM ESSE FREIO,','QUANTO ACELERA?',drag_off),
    ('A CHUVA','E O AVIÃO',aircraft),
    ('A ATMOSFERA É','O FREIO DA CHUVA',atmosphere),
]


def with_logo(image):
    """Aplica o símbolo oficial diretamente; o recorte da base antiga é frágil."""
    icon=Image.open(ROOT/'assets/branding/master/parallax_lab_icon_transparent.png').convert('RGBA')
    bounds=icon.getchannel('A').point(lambda v:255 if v>32 else 0).getbbox()
    icon=icon.crop(bounds)
    icon=icon.resize((round(icon.width*360/icon.height),360),Image.Resampling.LANCZOS)
    result=image.convert('RGBA')
    result.alpha_composite(icon,(560-icon.width//2,220))
    return result


def package(records):
    sheet=Image.new('RGB',(1620,1248),'#050816')
    draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype(g.BOLD,27)
    for i,record in enumerate(records):
        x,y=(i%5)*324,(i//5)*624
        draw.text((x+16,y+12),f"OPÇÃO {i+1:02d}",font=font,fill='#F5F7FF')
        with Image.open(OUT/record['arquivo']) as im:
            sheet.paste(im.resize((324,576),Image.Resampling.LANCZOS),(x,y+48))
    sheet.save(OUT/'comparativo_10_capas.jpg',quality=95,subsampling=0)
    with zipfile.ZipFile(OUT/'10_capas_ep02.zip','w',zipfile.ZIP_DEFLATED) as z:
        for record in records:
            z.write(OUT/record['arquivo'],record['arquivo'])
        z.write(OUT/'comparativo_10_capas.jpg','comparativo_10_capas.jpg')


def main():
    assert not OUT.exists(), f'Não sobrescrever a pasta existente: {OUT}'
    # Construir e validar as dez artes antes de gravar as entregas.
    panels = [builder() for _,_,builder in OPTIONS]
    OUT.mkdir()
    base = with_logo(g.base())
    g.base = lambda: base.copy()
    records=[]
    for n,((first,second,_),panel) in enumerate(zip(OPTIONS,panels),1):
        size=min(g.fit(text,g.BOLD,870,150).size for text in (first,second))
        lines=[([(first,'white')],size), ([(second,'grad')],size)]
        result=g.cover(lines,panel)
        assert result.size==(1080,1920)
        path=OUT/f'capa_{n:02d}.png'
        result.save(path,optimize=True)
        records.append({'opcao':n,'titulo':first+' / '+second,'arquivo':path.name,'fonte_titulo_px':size,'arte':OPTIONS[n-1][2].__name__})
        print(path,flush=True)
    (OUT/'indice.json').write_text(json.dumps({'serie':g.SERIE,'dimensoes':[1080,1920],'tipografia':'Space Grotesk Medium e Bold oficiais','base':'compositor de vid_0009; primitivas de vid_0010','opcoes':records},ensure_ascii=False,indent=2),encoding='utf-8')
    package(records)
    print('Concluído: dez capas, comparativo e ZIP.',flush=True)


if __name__=='__main__':
    main()
