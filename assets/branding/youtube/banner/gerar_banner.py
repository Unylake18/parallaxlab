"""Banner Parallax Lab: composição com assets e fontes oficiais, sem instalação.

Executar na raiz: python assets/branding/youtube/banner/gerar_banner.py
Requer Pillow e numpy. Todos os resultados ficam ao lado deste arquivo.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
W, H = 2560, 1440
# 1235×338 em 2048×1152, escalados por 1,25; arredondamento conservador.
SAFE = (508, 509, 2052, 931)
WHITE, CYAN = '#F5F7FF', '#35D9FF'
FONT = ROOT / 'assets/fonts'
DISPLAY = FONT / 'space_grotesk/SpaceGrotesk-Bold.ttf'
MEDIUM = FONT / 'space_grotesk/SpaceGrotesk-Medium.ttf'
BODY = FONT / 'inter/Inter-Regular.ttf'
ICON_PATH = ROOT / 'assets/branding/master/parallax_lab_icon_transparent.png'
REPORT = {}


def font(size, family=DISPLAY):
    return ImageFont.truetype(str(family), size)


def background(style):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    arr = np.zeros((H, W, 3), np.float32) + [5, 8, 22]
    strength = [1.0, 1.3, 0.45][style-1]
    for cx, cy, sx, sy, color in [
        (420, 700, 540, 420, (0, 20, 30)),
        (2230, 650, 520, 540, (17, 7, 30)),
        (1270, 1100, 1000, 420, (0, 5, 10)),
    ]:
        g = np.exp(-(((xx-cx)/sx)**2 + ((yy-cy)/sy)**2)/2)
        arr += g[:, :, None] * np.array(color) * strength
    im = Image.fromarray(np.uint8(np.clip(arr, 0, 255)), 'RGB').convert('RGBA')
    deco = Image.new('RGBA', im.size)
    d = ImageDraw.Draw(deco)
    if style != 3:
        rng = np.random.default_rng(150+style)
        for x, y, opacity in zip(rng.integers(40,W-40,100), rng.integers(40,H-40,100), rng.integers(18,65,100)):
            # Espaço negativo integral atrás do texto.
            if 480 < x < 2100 and 490 < y < 960:
                continue
            d.ellipse((int(x),int(y),int(x)+1,int(y)+1), fill=(170,200,255,int(opacity)))
    if style == 1:
        for offset in (0, 65, 130):
            d.line([(150+offset,300),(710+offset,110),(2420+offset,1135)], fill=(53,217,255,12), width=2)
    elif style == 2:
        # Planos deslocados e órbita textural: continuidade nas bordas.
        for off, col in [(0,(53,217,255,28)),(90,(116,92,255,22))]:
            d.polygon([(110+off,430),(530+off,185),(1020+off,940),(600+off,1185)], outline=col, width=2)
        d.ellipse((1570,210,2940,1260), outline=(53,217,255,20), width=2)
        d.ellipse((1620,235,2990,1285), outline=(116,92,255,15), width=1)
    else:
        d.line([(300,720),(455,720)], fill=(53,217,255,65), width=2)
        d.line([(2105,720),(2260,720)], fill=(53,217,255,65), width=2)
    return Image.alpha_composite(im,deco)


def text(im, value, size, x, top, color=WHITE, family=DISPLAY, centered=False):
    f = font(size,family)
    d = ImageDraw.Draw(im)
    bb = d.textbbox((0,0),value,font=f)
    width = bb[2]-bb[0]
    if centered:
        x -= width/2
    pos = (round(x-bb[0]), round(top-bb[1]))
    d.text(pos,value,font=f,fill=color)
    bounds = d.textbbox(pos,value,font=f)
    assert SAFE[0] <= bounds[0] and bounds[2] <= SAFE[2], (value,bounds)
    assert SAFE[1] <= bounds[1] and bounds[3] <= SAFE[3], (value,bounds)
    return list(bounds)


def icon(im, x, y, height):
    source = Image.open(ICON_PATH).convert('RGBA')
    # Recorte do padding transparente apenas; símbolo intacto.
    source = source.crop(source.getbbox())
    width = round(source.width*height/source.height)
    source = source.resize((width,height),Image.Resampling.LANCZOS)
    im.alpha_composite(source,(round(x),round(y)))
    bounds = [round(x),round(y),round(x)+width,round(y)+height]
    assert SAFE[0]<=bounds[0] and bounds[2]<=SAFE[2]
    assert SAFE[1]<=bounds[1] and bounds[3]<=SAFE[3]
    return bounds


def render(style):
    im = background(style)
    boxes = []
    if style == 1:
        # Lockup horizontal centralizado, assinatura em linha única.
        title_width = ImageDraw.Draw(im).textbbox((0,0),'PARALLAX LAB',font=font(100))[2]
        icon_width = round(1218/1225*180)
        left = (W-title_width-icon_width-42)/2
        boxes.append(icon(im,left,568,180))
        boxes.append(text(im,'PARALLAX LAB',100,left+icon_width+42,623))
        boxes.append(text(im,'FÍSICA E MATEMÁTICA POR OUTRA PERSPECTIVA',37,1280,787,color=CYAN,family=MEDIUM,centered=True))
        boxes.append(text(im,'Intuição • Visualização • Rigor',30,1280,851,color='#B9CADA',family=BODY,centered=True))
    elif style == 2:
        boxes.append(icon(im,625,558,310))
        boxes.append(text(im,'PARALLAX LAB',90,1000,584))
        boxes.append(text(im,'FÍSICA E MATEMÁTICA',43,1003,719,family=MEDIUM))
        boxes.append(text(im,'POR OUTRA PERSPECTIVA',43,1003,774,color=CYAN,family=MEDIUM))
        boxes.append(text(im,'Intuição • Visualização • Rigor',30,1003,855,color='#B9CADA',family=BODY))
    else:
        boxes.append(icon(im,1238,550,85))
        boxes.append(text(im,'PARALLAX LAB',105,1280,672,centered=True))
        boxes.append(text(im,'FÍSICA E MATEMÁTICA POR OUTRA PERSPECTIVA',37,1280,809,color=CYAN,family=MEDIUM,centered=True))
        boxes.append(text(im,'Intuição • Visualização • Rigor',30,1280,867,color='#B9CADA',family=BODY,centered=True))
    names = ['01_institucional','02_cinematografico','03_minimalista']
    name = 'banner_'+names[style-1]
    path = OUT / (name+'.png')
    im = im.convert('RGB')
    im.save(path,optimize=True)
    assert path.stat().st_size <= 6_000_000
    REPORT[name] = {'resolucao':im.size,'bytes':path.stat().st_size,'limites_conteudo':boxes,'conteudo_dentro_area_segura':True}
    guide = im.convert('RGBA')
    shade = Image.new('RGBA',im.size,(0,0,0,155))
    ImageDraw.Draw(shade).rectangle(SAFE,fill=(0,0,0,0))
    guide = Image.alpha_composite(guide,shade)
    d = ImageDraw.Draw(guide)
    d.rectangle(SAFE,outline=CYAN,width=3)
    d.line([(0,509),(W,509)],fill=(53,217,255,90),width=1)
    d.line([(0,931),(W,931)],fill=(53,217,255,90),width=1)
    d.text((508,460),'ÁREA SEGURA · 1544 × 422 px · guia conservador',font=font(25,BODY),fill=WHITE)
    guide.convert('RGB').save(OUT/(name+'_guia.png'),optimize=True)
    return im


def review(images):
    # Prancha de revisão, sem simular a interface mutável do YouTube.
    sheet = Image.new('RGB',(1440,1660),'#050816')
    d = ImageDraw.Draw(sheet)
    labels = ['01 / INSTITUCIONAL — recomendada','02 / CINEMATOGRÁFICA','03 / MINIMALISTA']
    for index, (im,label) in enumerate(zip(images,labels)):
        y = 35+index*535
        d.text((40,y),label,font=font(27,MEDIUM),fill=WHITE)
        # Recorte desktop completo, seguido da área segura em largura de celular.
        strip = im.crop((0,509,W,931)).resize((1360,224),Image.Resampling.LANCZOS)
        sheet.paste(strip,(40,y+55))
        mobile = im.crop(SAFE).resize((600,164),Image.Resampling.LANCZOS)
        sheet.paste(mobile,(420,y+315))
        d.text((40,y+305),'Recorte central',font=font(23,BODY),fill='#B9CADA')
        d.text((40,y+338),'600 px para revisão',font=font(20,BODY),fill='#B9CADA')
    sheet.save(OUT/'previa_recortes.png',optimize=True)


if __name__ == '__main__':
    images = [render(i) for i in (1,2,3)]
    review(images)
    REPORT['area_segura'] = SAFE
    (OUT/'qa_banner.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(REPORT,ensure_ascii=False,indent=2))
