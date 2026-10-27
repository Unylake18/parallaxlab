"""Interpolação temporal local dos PNGs 3D, sem alterar o arsenal."""
import math
import numpy as np
from PIL import Image

def interpolar(source,mob):
    original=mob.set_fase
    def set_fase(phase):
        original(phase)
        f=min(max(phase,0),1)*(source.frames-1) if source.unico else (phase%1)*source.frames
        i=int(math.floor(f));weight=f-i
        if weight>1e-5 and source.frames>1:
            a,b=source.quadro(i),source.quadro(min(i+1,source.frames-1) if source.unico else i+1)
            arr=np.array(Image.blend(Image.fromarray(a),Image.fromarray(b),weight))
            mob.pixel_array=arr.copy();mob.orig_alpha_pixel_array=arr[:,:,3].copy()
            if mob.stroke_opacity<1:
                mob.pixel_array[:,:,3]=(arr[:,:,3]*mob.stroke_opacity).astype(np.uint8)
        return mob
    mob.set_fase=set_fase
    return mob
