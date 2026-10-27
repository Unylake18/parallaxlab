"""Normalização sem recompressão, QA do MP4 e pacote desta rodada."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import av
import numpy as np
from verificar_preview import verificar
from amostrar_movimento import amostrar

p=Path(__file__).resolve().parent
video=p/'media_acabamento/preview_acabamento_0007_960x540_15fps.mp4'
timing=p/'timing_acabamento.json'
qa=p/'qa_acabamento'


def preparar():
    origem=p/'media_acabamento/videos/cena/540p15/OrbitaQuedaContinua007.mp4'
    montado=p/'media_acabamento/preview_acabamento_montado.mp4'
    if montado.exists(): origem=montado
    with av.open(str(origem)) as entrada, av.open(str(video),'w') as saida:
        s=entrada.streams.video[0]; out=saida.add_stream_from_template(s)
        out.time_base=Fraction(1,15360); count=0
        for packet in entrada.demux(s):
            if packet.dts is None: continue
            pts=round(packet.pts*packet.time_base*15)
            dts=round(packet.dts*packet.time_base*15)
            packet.pts=pts*1024; packet.dts=dts*1024
            packet.duration=1024; packet.time_base=out.time_base; packet.stream=out
            saida.mux(packet); count+=1
    with av.open(str(video)) as c:
        assert c.streams.video[0].average_rate==15
        assert c.streams.video[0].frames==count
    verificar(video,timing,'qa_acabamento')
    amostrar(video,timing,qa/'movimento')
    # Auditoria de amarelo no vídeo montado, fora da marca oficial.
    suspeitos=[]; contagem=0
    with av.open(str(video)) as c:
        for f in c.decode(video=0):
            rgb=f.to_ndarray(format='rgb24')[::4,::4].astype(float)
            rgb[:18,-38:]=0
            r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
            mask=(r>120)&(g>90)&(r>1.05*g)&(r<1.8*g)&(b<.70*g)
            if np.count_nonzero(mask)>2: suspeitos.append(float(f.time))
            contagem+=1
    assert contagem==count,(contagem,count)
    resultado=dict(frames_decodificados=contagem,amostragem_espacial='1 pixel a cada 4 por eixo',
                   marca_oficial_excluida=True,instantes_amarelos=suspeitos)
    (qa/'paleta.json').write_text(json.dumps(resultado,ensure_ascii=False,indent=2),encoding='utf-8')
    assert not suspeitos, suspeitos[:10]
    print(f'QA do vídeo concluído: {count} frames; amarelo não detectado na auditoria.')


def pacote():
    tecnico=json.loads((qa/'tecnico.json').read_text(encoding='utf-8'))
    assert tecnico['blocos']==18 and tecnico['faixas_audio']==0
    assert not json.loads((qa/'paleta.json').read_text(encoding='utf-8'))['instantes_amarelos']
    arquivos=[(video,'video/preview_acabamento_0007.mp4')]
    for f in sorted(qa.glob('N*.png')): arquivos.append((f,'quadros/'+f.name))
    for f in sorted(qa.glob('prancha_*.jpg')): arquivos.append((f,'pranchas/'+f.name))
    for f in sorted((qa/'movimento').glob('*')):
        if f.is_file(): arquivos.append((f,'movimento/'+f.name))
    for f in sorted((qa/'definicao1080').glob('*')):
        if f.is_file(): arquivos.append((f,'teste_definicao_1080/'+f.name))
    teste=p/'media_acabamento/teste1080/videos/teste_camera/1080p15/TesteCamera.mp4'
    arquivos.append((teste,'teste_definicao_1080/zoom_1080p.mp4'))
    for nome in ('qa_acabamento.md','ficha.md','reavaliacao_acabamento.md','timing_acabamento.json','validacao_acabamento.json','montagem_acabamento.json'):
        arquivos.append((p/nome,'documentacao/'+nome))
    for nome in ('tecnico.json','paleta.json'): arquivos.append((qa/nome,'documentacao/'+nome))
    manifesto=[dict(arquivo=n,bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f,n in arquivos]
    destino=p/'avaliacao_acabamento_visual_0007.zip'
    with ZipFile(destino,'w',ZIP_DEFLATED,compresslevel=6) as z:
        for f,n in arquivos: z.write(f,n)
        z.writestr('manifesto.json',json.dumps(manifesto,ensure_ascii=False,indent=2))
        z.writestr('LEIA-ME.txt','LONGO 0007 — ACABAMENTO VISUAL N01–N18\n'
            'Vídeo completo em video/. Comece pelo relatório em documentacao/.\n'
            'quadros/ contém todos os marcos de avaliação e os finais de blocos;\n'
            'movimento/ contém 12 amostras temporais por bloco, além das pranchas.\n'
            'O MP4 contém a sequência integral de frames a 15 fps.\n'
            'teste_definicao_1080/ é uma regressão técnica curta, sem identidade completa.\n'
            'Preview silencioso para revisão editorial.\n')
    with ZipFile(destino) as z: assert z.testzip() is None
    print(json.dumps(dict(zip=str(destino),bytes=destino.stat().st_size,arquivos=len(arquivos)+2),ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('etapa',choices=['preparar','pacote'])
    args=parser.parse_args()
    preparar() if args.etapa=='preparar' else pacote()
