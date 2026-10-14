from pathlib import Path
import sys
from manim import tempconfig
U=Path(__file__).resolve().parent
sys.path.insert(0,str(U))
import cena_v4 as m
m.RES='540x960';m.CACHE_3D_FILE='cache_3d_v2.json';m.PROJECAO_3D_FILE='projecao_3d_v2.json'
class Conferir(m.LiquidoRotacao022V4):
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw);self.camera.capture_mobjects=lambda *a,**kw:None
with tempconfig(dict(dry_run=True,skip_animations=True,disable_caching=True,pixel_width=540,pixel_height=960,frame_rate=30,progress_bar='none',verbosity='WARNING')):
    c=Conferir();c.render()
assert len(c.maps)==12
print('PREFLIGHT OK:',c.time,'s fonte;',len(c.maps),'mapas;',c.operation_index,'operações')
