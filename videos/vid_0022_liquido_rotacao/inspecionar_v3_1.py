"""QA do único preview V3.1: metadados, textos e conclusão em três batidas."""
import json
import math
from pathlib import Path
import av
from PIL import Image, ImageDraw, ImageFont

UNIT=Path(__file__).resolve().parent
VIDEO=UNIT/'media/videos/cena_v3_1/960p15/preview_silencioso_v3_1.mp4'
TEMPOS=[(2,'plano'),(8,'morph'),(13,'corte_3d'),(16,'regiao_no_liquido'),
        (20,'secao_2d'),(23.5,'zoom_contexto_azul'),(24,'zoom'),(29,'movimento_dimensoes'),(35,'forcas'),
        (42,'taylor'),(44,'substituicao'),(46,'cancelamento_pressao'),(48,'gradiente'),
        (57,'newton'),(59,'cancelamento_newton'),(63,'pressao_radial'),(71,'giro_vertical'),
        (76,'hidrostatica'),(85,'isobarica_3d'),(88,'meridiana_imovel'),(89,'match_superficie_2d'),(92,'dr_dz'),
        (96,'regra_cadeia'),(105,'substituicao_gradientes'),(111,'tangente_movel'),
        (121,'diferencial'),(124,'integrais'),(128,'solucao'),(134,'espelhamento'),
        (141,'sintese_pressao'),(142,'sintese_subida'),(144,'sintese_tangente'),(147,'sintese_parabola'),
        (150,'match_meridiana'),(152,'revela_grade'),(154,'paralaxe'),(156,'batida_delta_h'),
        (158.2,'batida_inclinacao'),(159.2,'batida_parabola'),(162,'batida_ideia_central'),(166,'branding')]
TEMPOS += [(36.4,'desigualdade_faces'),(59.6,'cancelamentos_newton'),
           (88.3,'meridiana_sem_deslocamento'),(94.2,'isobara_apos_movimento'),
           (141.6,'gradiente_sintese_completo'),(142.6,'subida_sintese_completa'),
           (145.4,'tangente_sintese_completa'),(146.3,'parabola_sintese_completa')]
TEMPOS.sort()


def main():
    folder=UNIT/'qa_v3_1'
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
            if t<164:
                pixels=img.crop((0,0,350,70)).get_flattened_data()
                assert sum(sum(abs(c[j]-[5,8,22][j]) for j in range(3))>30 for c in pixels)>100,'Header ausente'
            stamp=f'{t:03d}' if isinstance(t,int) else f'{t:.1f}'.replace('.','p')
            img.save(folder/f'{stamp}_{name}.png')
            page,local=divmod(i,16)
            x,y=(local%4)*216,(local//4)*414
            draw=ImageDraw.Draw(sheets[page])
            draw.text((x+5,y+6),f'{int(t)//60}:{int(t)%60:02d} {name}',font=font,fill='white')
            sheets[page].paste(img.resize((216,384)),(x,y+30))
    for page,sheet in enumerate(sheets,1):
        sheet.save(folder/f'folha_qa_{page}.png')
    (folder/'metadados.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    audit=json.loads((UNIT/'marcos_v3_1.json').read_text(encoding='utf-8'))['headlines']
    assert all(abs(m['x'])<1e-4 and m['largura']<=7.401 and m['y']==5.65 for m in audit)
    print('QA:',len(TEMPOS),'quadros;',len(audit),'headlines centralizadas na largura segura')
    print(json.dumps(meta,indent=2))


if __name__=='__main__':
    main()
