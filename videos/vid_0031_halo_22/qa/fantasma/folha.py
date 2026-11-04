import numpy as np, sys, pathlib
from PIL import Image, ImageDraw
U=pathlib.Path(__file__).resolve().parents[2]
def comp(f):
    fg=np.asarray(Image.open(U/f'media_fant/stills/{f}.png').convert('RGBA')).astype(np.float32)
    bg=np.asarray(Image.open(U/f'frames3d_540x960/f{f:05d}.png').convert('RGB')).astype(np.float32)
    a=fg[...,3:4]/255
    return Image.fromarray((fg[...,:3]*a+bg*(1-a)+.5).astype(np.uint8))
fs=[int(x) for x in sys.argv[2].split(',')]
n=len(fs);W=Image.new('RGB',(540*n,960))
for i,f in enumerate(fs):
    im=comp(f);ImageDraw.Draw(im).text((8,940),f'{f/15:.1f}s',fill='white');W.paste(im,(540*i,0))
W.save(U/f'qa/fantasma/{sys.argv[1]}.png')
