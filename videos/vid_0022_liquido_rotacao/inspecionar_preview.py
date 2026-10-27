"""Extrai apenas os estados do QA solicitado; não renderiza outra versão."""
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parent
VIDEO = UNIT/'media/videos/cena/960p15/preview_silencioso.mp4'
TEMPOS = [
    (2,'plano'),(8,'morph'),(13,'paraboloide'),(16,'transicao_2d'),(23,'aceleracao'),
    (38,'forcas'),(47,'taylor'),(52,'cancelamento_pressao'),(56,'forca_gradiente'),
    (63,'newton'),(69,'gradiente_radial'),(73,'pressao_aumenta'),(85,'hidrostatica'),
    (99,'isobarica'),(104,'derivada_total'),(114,'regra_cadeia'),(126,'inclinacao'),
    (133,'tangente'),(142,'integrais'),(149,'resultado'),(155,'espelhamento'),
    (158,'transicao_secao'),(162,'revela_volume'),(171,'delta_h'),
]


def main():
    pasta=UNIT/'qa'
    pasta.mkdir(exist_ok=True)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    sheet=Image.new('RGB',(864,6*414),'#050816')
    d=ImageDraw.Draw(sheet)
    with av.open(str(VIDEO)) as c:
        s=c.streams.video[0]
        duracao=float(s.duration*s.time_base)
        meta=dict(duracao_s=duracao,fps=float(s.base_rate),fps_medio=float(s.average_rate),largura=s.width,altura=s.height,
                  quadros=s.frames,codec=s.codec_context.name,pixel_format=s.codec_context.format.name,
                  audio_streams=len(c.streams.audio),bytes=VIDEO.stat().st_size)
        assert (s.width,s.height)==(540,960)
        assert float(s.base_rate)==15 and abs(float(s.average_rate)-15)<0.001
        assert not c.streams.audio
        assert abs(duracao-174)<0.2
        for i,(t,nome) in enumerate(TEMPOS):
            c.seek(int(t/s.time_base),stream=s)
            frame=next(f for f in c.decode(s) if f.time>=t-1e-5)
            img=frame.to_image().convert('RGB')
            img.save(pasta/f'{t:03d}_{nome}.png')
            x,y=(i%4)*216,(i//4)*414
            d.text((x+5,y+6),f'{t//60}:{t%60:02d} {nome}',font=font,fill='white')
            sheet.paste(img.resize((216,384)),(x,y+30))
    sheet.save(pasta/'folha_qa.png')
    (pasta/'metadados.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    print(json.dumps(meta,indent=2))


if __name__=='__main__':
    main()
