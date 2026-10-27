import json,av,sys
from PIL import Image,ImageDraw
def get(T,i,f):
    b={x['id']:x for x in json.load(open(f'renders/blocos_v3_1_{T}.json'))}[i]
    t=b['inicio']+f*b['voz_s']
    c=av.open(f'renders/m_{T}/videos/cena/540p15/trecho_{T}_v1_6.mp4');s=c.streams.video[0]
    c.seek(int(max(t-1,0)/s.time_base),stream=s)
    for fr in c.decode(s):
        if float(fr.pts*s.time_base)>=t: return fr.to_image()
def sheet(want,out,cols=3):
    ims=[]
    for T,i,f in want:
        im=get(T,i,f).resize((640,360));d=ImageDraw.Draw(im);d.rectangle((0,0,110,20),fill='black');d.text((4,3),f'{i} {int(f*100)}%',fill='white');ims.append(im)
    rows=(len(ims)+cols-1)//cols
    sh=Image.new('RGB',(640*cols,360*rows))
    for k,im in enumerate(ims): sh.paste(im,((k%cols)*640,(k//cols)*360))
    sh.save(out)
sets={'a':[('A','H04',.3),('A','H04',.6),('A','H04',.85),('B','D16',.4),('B','D16',.65),('B','D16',.85),('D','R02',.7),('D','P11',.5),('D','P11',.97)],
 'b':[('F','F01',.5),('F','F01',.9),('F','F02',.15),('F','F02',.55),('F','F02',.95),('F','F04',.5),('F','F04',.97),('E','S09',.7),('E','S09',.97),('E','S05',.5),('E','C06',.5),('E','C06',.8)]}
for k,w in sets.items(): sheet(w,f'renders/qa_v1_7/rev4_{k}.png')
