"""Executa a construção sem gravar vídeo ou imagens, verificando tempos e mapas."""
import runpy
import sys
from pathlib import Path
from manim import tempconfig

UNIT=Path(__file__).resolve().parent
scene=runpy.run_path(str(UNIT/'cena_v2.py'))['LiquidoRotacao022V2']


class Conferir(scene):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._capturar=self.camera.capture_mobjects
        # A validação temporal não precisa rasterizar todos os estados intermediários.
        self.camera.capture_mobjects=lambda *a,**k:None

    def mark(self,name):
        super().mark(name)
        if '--quadros' in sys.argv and name in {'gradiente_construido','pressao_cresce','vertical',
                'isobarica_3d','regra_cadeia','tangente_na_borda','parabola_integrada','delta_h','branding'}:
            folder=UNIT/'qa_v2_preflight_final'
            folder.mkdir(exist_ok=True)
            self.camera.reset()
            self._capturar(self.mobjects)
            image=self.camera.get_image()
            image.save(folder/f'{name}.png')
            if name=='delta_h':
                pixels=image.convert('RGB').crop((0,0,350,70)).get_flattened_data()
                assert sum(sum(abs(c[i]-[5,8,22][i]) for i in range(3))>30 for c in pixels)>100,'Header ausente'


with tempconfig(dict(dry_run=True,skip_animations=True,disable_caching=True,
                     pixel_width=540,pixel_height=960,frame_rate=15,progress_bar='none')):
    obj=Conferir()
    obj.render()
    assert abs(obj.time-168)<.1,obj.time
    print('CONSTRUCAO V2 OK',obj.time,'s;',len(obj.maps),'mapas MF-Tools')
