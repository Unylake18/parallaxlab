"""yt_0025: oito lotes de preview silencioso, 960×540 / 15 fps."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import latex25
from cenas25 import Video25
from conteudo25 import LOTES
for nome in LOTES:
    globals()[nome]=type(nome,(Video25,),{})
