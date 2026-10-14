"""QA do único preview V2: metadados e amostragem dos estados/transições."""
import json
import math
from pathlib import Path
import av
from PIL import Image, ImageDraw, ImageFont

UNIT=Path(__file__).resolve().parent
VIDEO=UNIT/'media/videos/cena_v2/960p15/preview_silencioso_v2.mp4'
TEMPOS=[(2,'plano'),(8,'morph'),(13,'corte_3d'),(16,'regiao_no_liquido'),
        (20,'secao_2d'),(24,'zoom'),(29,'movimento_dimensoes'),(35,'forcas'),
        (42,'taylor'),(44,'substituicao'),(46,'cancelamento_pressao'),(48,'gradiente'),
        (57,'newton'),(59,'cancelamento_newton'),(63,'pressao_radial'),(71,'giro_vertical'),
        (76,'hidrostatica'),(85,'isobarica_3d'),(89,'match_superficie_2d'),(92,'dr_dz'),
        (96,'regra_cadeia'),(105,'substituicao_gradientes'),(111,'tangente_movel'),
        (121,'diferencial'),(124,'integrais'),(128,'solucao'),(134,'espelhamento'),
        (143,'sintese_pressao'),(146,'sintese_superficie'),(151,'match_meridiana'),
        (155,'revela_paralaxe'),(161,'delta_h'),(166,'branding')]


def main():
    folder=UNIT/'qa_v2'
    folder.mkdir(exist_ok=True)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    with av.open(str(VIDEO)) as c:
        s=c.streams.video[0]
        duration=float(s.duration*s.time_base)
        meta=dict(duracao_s=duration,fps=float(s.base_rate),fps_medio=float(s.average_rate),
                  largura=s.width,altura=s.height,quadros=s.frames,codec=s.codec_context.name,
                  pixel_format=s.codec_context.format.name,audio_streams=len(c.streams.audio),bytes=VIDEO.stat().st_size)
        assert (s.width,s.height)==(540,960)
        assert float(s.base_rate)==15 and abs(float(s.average_rate)-15)<.001
        assert not c.streams.audio
        assert abs(duration-168)<.25
        sheets=[]
        for page in range(math.ceil(len(TEMPOS)/16)):
            count=min(16,len(TEMPOS)-page*16)
            sheets.append(Image.new('RGB',(864,math.ceil(count/4)*414),'#050816'))
        for i,(t,name) in enumerate(TEMPOS):
            c.seek(int(t/s.time_base),stream=s)
            frame=next(f for f in c.decode(s) if f.time>=t-1e-5)
            img=frame.to_image().convert('RGB')
            if t in (2,161):
                pixels=img.crop((0,0,350,70)).get_flattened_data()
                assert sum(sum(abs(c[j]-[5,8,22][j]) for j in range(3))>30 for c in pixels)>100,'Header ausente'
            img.save(folder/f'{t:03d}_{name}.png')
            page,local=divmod(i,16)
            x,y=(local%4)*216,(local//4)*414
            draw=ImageDraw.Draw(sheets[page])
            draw.text((x+5,y+6),f'{t//60}:{t%60:02d} {name}',font=font,fill='white')
            sheets[page].paste(img.resize((216,384)),(x,y+30))
    for page,sheet in enumerate(sheets,1):
        sheet.save(folder/f'folha_qa_{page}.png')
    (folder/'metadados.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    print(json.dumps(meta,indent=2))


if __name__=='__main__':
    main()
