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
sets={'a':[('E','S03',.3),('E','S03',.55),('E','S03',.75),('E','S03',.95),('E','S04',.2),('E','S04',.45),('E','S04',.7),('E','S04',.9),('E','S09',.5)],
 'b':[('E','C02',.4),('E','C06',.3),('E','C06',.8),('E','C07',.6),('D','R06',.35),('D','R06',.9),('D','R07',.7),('D','R02',.4),('B','D13',.45)],
 'c':[('D','P07',.4),('D','P07',.62),('D','P07',.8),('D','P08',.35),('D','P08',.6),('D','P08',.9),('F','F03',.3),('F','F03',.6),('F','F03',.95),('F','F04',.5),('F','F04',.75),('F','F04',.97)]}
for k,w in sets.items(): sheet(w,f'renders/qa_v1_7/rev2_{k}.png')
for T in "BDEF":
    b=json.load(open(f'renders/blocos_v3_1_{T}.json'));print(T,[(x['id'],x['excesso_s']) for x in b if x['excesso_s']>.5])
