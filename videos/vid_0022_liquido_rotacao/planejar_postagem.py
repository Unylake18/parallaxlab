"""Registra operações aprovadas a 15 fps e planeja render nativo fluido a 30 fps."""
import json,sys
from pathlib import Path
import numpy as np
from manim import tempconfig,Wait
U=Path(__file__).resolve().parent
sys.path.insert(0,str(U))
from cena_v3_1 import LiquidoRotacao022V31
class Registrar(LiquidoRotacao022V31):
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw);self.operations=[]
        self.camera.capture_mobjects=lambda *a,**kw:None
    def play(self,*a,**kw):
        start=self.time;super().play(*a,**kw)
        self.operations.append(dict(index=len(self.operations),start=start,end=self.time,pause=len(a)==1 and isinstance(a[0],Wait),types=[type(x).__name__ for x in a]))
with tempconfig(dict(dry_run=True,skip_animations=True,disable_caching=True,pixel_width=540,pixel_height=960,frame_rate=15,progress_bar='none',verbosity='WARNING')):
    scene=Registrar();scene.render()
assert abs(scene.time-168)<.1
sync=json.loads((U/'sync.json').read_text(encoding='utf-8'))
groups=sync['segments']; fps=30
# Mesmos blocos aprovados, renderizados na ordem original e montados depois por quadros.
ordered=[groups[0],groups[2],groups[1],groups[3]]
intervals=[];offset=0;source_end=0
for group in ordered:
    begin,end=group[0]['visual'],group[-1]['visual']
    if begin>source_end+1e-5:
        count=round((begin-source_end)*fps)
        intervals.append(dict(source=[source_end,begin],frames=[offset,offset+count],keep=False))
        offset+=count
    start=round(group[0]['audio']*fps);stop=round(group[-1]['audio']*fps)
    intervals.append(dict(source=[begin,end],frames=[offset,offset+stop-start],keep=True,group=groups.index(group),points=group))
    offset+=stop-start;source_end=end

def warp(t):
    for entry in intervals:
        a,b=entry['source']; x,y=entry['frames']
        if a-1e-5<=t<=b+1e-5:
            if entry['keep']:
                g=entry['points'];at=np.interp(t,[p['visual'] for p in g],[p['audio'] for p in g])
                return x+round(at*fps)-round(g[0]['audio']*fps)
            return x+round((t-a)*fps)
    raise ValueError(t)
operations=[]
for op in scene.operations:
    total=warp(op['end'])-warp(op['start'])
    assert total>0,op
    math=any(n in {'TransformByGlyphMap','TransformMatchingTex'} for n in op['types'])
    motion=min(total,42) if math and not op['pause'] else total
    operations.append(dict(**op,frames=motion,hold_after=total-motion))
assert sum(op['frames']+op['hold_after'] for op in operations)==offset
assembly=sorted([x for x in intervals if x['keep']],key=lambda x:x['group'])
assert sum(x['frames'][1]-x['frames'][0] for x in assembly)==5124
plan=dict(fps=fps,operations=operations,intervals=intervals,assembly=assembly,render_frames=offset,total_frames=5124,duration=170.8,math_motion_max=1.4)
(U/'timing_postagem.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('PLANO:',len(operations),'operações;',offset,'quadros fonte; 5124 quadros finais; transições algébricas até 1,4s')
