import json,av
from PIL import Image,ImageDraw
dur=json.load(open('duracoes_v3_1.json'))
EV=[('A',[('G04',120.5,'máxima: vetor de frente'),('G04',123.0,'ainda de frente'),('G04',125.5,'girando p/ tangente'),('G04',127.4,'tangente: zero')]),
('B',[('D10',348.2,'secante'),('D10',352.0,'dx→0 em curso'),('D10',355.6,'secante vira tangente'),('D10',357.8,'derivada legível'),('D11',361.5,'y e z fixos'),('D12',370.6,'entrada D12'),('D12',372.8,'dx dy dz'),('D12',377.5,'dV'),('D12',381.0,'∂Ex/∂x dV')]),
('K',[('K01',634.7,'exemplo simples'),('K03',664.6,'3κ'),('K03',669.4,'densidade uniforme'),('K03',672.0,'ρ=3ε0κ')]),
('D',[('P06',757.0,'motivação (fonte concentrada)'),('P06',764.8,'nome da delta'),('P06',768.3,'notação'),('P08',794.8,'f'),('P08',797.3,'integrando'),('P08',801.6,'seleção'),('P08',805.6,'f(0)=resultado'),('P08',812.0,'sustentado'),('R02',890.5,'eixos'),('R02',893.6,'seta tangente'),('R02',896.8,'Ω')]),
('E',[('S03',1191.2,'par oposto'),('S03',1195.5,'todos os pares'),('S03',1197.9,'cancelam'),('S03',1199.8,'borda externa')]),
('F',[('F04',1421.8,'equipotenciais'),('F04',1424.2,'ponto'),('F04',1426.8,'gradiente'),('F04',1431.8,'E oposto')])]
tiles=[]
for T,lst in EV:
    b=json.load(open(f'renders/blocos_v3_1_{T}.json'))['blocos']
    ref=b[0]; off=dur[ref['id']]['t']-ref['inicio']
    c=av.open(f'renders/m_{T}/videos/cena/540p15/trecho_{T}_v1_6.mp4');s=c.streams.video[0]
    want=sorted([(t-off,i,l,t) for i,t,l in lst]); k=0; got={}
    for f in c.decode(s):
        tt=float(f.pts*s.time_base)
        while k<len(want) and tt>=want[k][0]:
            got[want[k][1]+str(want[k][3])]=f.to_image().resize((640,360)); k+=1
        if k>=len(want): break
    for t_s,i,l,t in sorted(want,key=lambda z:z[3]):
        im=got.get(i+str(t))
        if im is None: im=Image.new('RGB',(640,360))
        d=ImageDraw.Draw(im);d.rectangle((0,0,330,20),fill='black');d.text((4,3),f'{i} {t:.1f}s  {l}',fill='white');tiles.append(im)
for k in range(0,len(tiles),12):
    sh=Image.new('RGB',(1920,1440))
    for j,t in enumerate(tiles[k:k+12]): sh.paste(t,((j%3)*640,(j//3)*360))
    sh.save(f'renders/qa_v1_7/asr_ev_{k//12+1}.jpg',quality=85)
print(len(tiles))
for T in 'ABKDEF':
    d=json.load(open(f'renders/blocos_v3_1_{T}.json'))
    print(T,'marcos atrasados>0.1:',[m for m in d['marcos'] if m['atraso_s']>.1],'excesso>0.2:',[(x['id'],x['excesso_s']) for x in d['blocos'] if x['excesso_s']>.2])
