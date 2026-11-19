"""Crossfades de conteúdo: captura alfa só nas bordas, com o fundo em relógio global separado."""
import re
from pathlib import Path
import numpy as np
from PIL import Image
from manim.camera.camera import Camera

def instalar(cena,unidade):
    log=Path(unidade)/f'log_ped_{cena.lote}.txt'
    if not log.exists():return
    m=re.findall(r'\[tempo\] total ([0-9.]+)',log.read_text(encoding='utf-8',errors='replace'))
    if not m:return
    total=round(float(m[-1])*15);cont=[0]
    destino=Path(unidade)/'renders/transicoes'/cena.lote;destino.mkdir(parents=True,exist_ok=True)
    w,h=cena.camera.pixel_width,cena.camera.pixel_height
    fg=Camera(pixel_width=w,pixel_height=h,background_opacity=0)
    bg=Camera(pixel_width=w,pixel_height=h,background_color='#08122B',background_opacity=1)
    writer=cena.renderer.file_writer;original=writer.write_frame
    def escreve(frame,*args,**kw):
        f=cont[0]
        if f<12 or f>=total-16:
            ff=[x for x in cena.mobjects if x is not cena.fundo and x is not cena.poeira]
            fg.reset();fg.capture_mobjects(ff)
            Image.fromarray(fg.pixel_array).save(destino/f'fg_{f:05d}.png')
            if f<12:
                bg.reset();bg.capture_mobjects([cena.fundo,cena.poeira])
                Image.fromarray(bg.pixel_array).save(destino/f'bg_{f:05d}.png')
        cont[0]+=kw.get('num_frames',args[0] if args else 1)
        return original(frame,*args,**kw)
    writer.write_frame=escreve
