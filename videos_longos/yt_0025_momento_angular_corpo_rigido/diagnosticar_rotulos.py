"""Sonda local do posicionamento; não entra no vídeo."""
import json
import latex25
from pecas25 import *
from PIL import Image
from scipy.ndimage import maximum_filter
estado=dict(json.loads((DIR3D/'pedidos3d/PH.json').read_text())['cenas']['pendulo_conico'])[497]
e=F.pendulo(estado['phi']);c=estado['cam']
mask=maximum_filter(np.array(Image.open(DIR3D/'q3d/PH_960x540/pendulo_conico/mascaras/f00497.png').convert('L')),size=35)>127
for tex,p in [(r'\vec r',.22*e['r']),(r'\vec\tau',.48*e['torque'])]:
    pos=proj(c,p);print(tex,'dono',px(pos))
    for lado in (UP,DOWN,LEFT,RIGHT,UL,UR,DL,DR):
        m=T(tex,36,WHITE_).next_to(Dot(pos,radius=.12),lado,buff=.3)
        x0,y0,_=m.get_corner(DL);x1,y1,_=m.get_corner(UR)
        a,b=max(0,int((x0+8)*60)),min(960,int((x1+8)*60)+1)
        cc,d=max(0,int((4.5-y1)*60)),min(540,int((4.5-y0)*60)+1)
        print(lado[:2],px(m.get_center()),int(mask[cc:d,a:b].sum()))
