"""Incorpora revisões locais sem recodificar os blocos já conferidos."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import av

p=Path(__file__).resolve().parent
mudaram={5,6,7,8,10,11,12,13}
full=json.loads((p/'timing_acabamento.json').read_text(encoding='utf-8'))
ajuste=json.loads((p/'timing_acabamento_5_6_7_8_11_12_13.json').read_text(encoding='utf-8'))
por_bloco={b['bloco']:b for b in ajuste['blocos']}
local07=json.loads((p/'timing_acabamento_7_8_10.json').read_text(encoding='utf-8'))
por_bloco07={b['bloco']:b for b in local07['blocos']}
origem=p/'media_acabamento/videos/cena/540p15/OrbitaQuedaContinua007.mp4'
patch=p/'media_acabamento/semantica/videos/cena/540p15/OrbitaQuedaContinua007.mp4'
patch07=p/'media_acabamento/local07/videos/cena/540p15/OrbitaQuedaContinua007.mp4'
destino=p/'media_acabamento/preview_acabamento_montado.mp4'
registros=[]; ultimo_dts=None
with av.open(str(origem)) as c, av.open(str(destino),'w') as out:
    stream=out.add_stream_from_template(c.streams.video[0]); stream.time_base=Fraction(1,15360)
    for bloco in full['blocos']:
        n=int(bloco['bloco'][1:]); novo=n in mudaram
        fonte=(por_bloco07[bloco['bloco']] if n in (7,8,10) else por_bloco[bloco['bloco']]) if novo else bloco
        lo,hi=[round(fonte[k]*15) for k in ('inicio','fim')]
        ini,fim=[round(bloco[k]*15) for k in ('inicio','fim')]
        assert hi-lo==fim-ini,(bloco['bloco'],hi-lo,fim-ini)
        arquivo=(patch07 if n in (7,8,10) else patch) if novo else origem
        count=0; digest=hashlib.sha256()
        with av.open(str(arquivo)) as entrada:
            for packet in entrada.demux(video=0):
                if packet.dts is None: continue
                pts=round(packet.pts*packet.time_base*15)
                dts=round(packet.dts*packet.time_base*15)
                if not lo<=pts<hi: continue
                digest.update(bytes(packet))
                packet.pts=(pts-lo+ini)*1024; packet.dts=(dts-lo+ini)*1024
                assert ultimo_dts is None or packet.dts>ultimo_dts
                ultimo_dts=packet.dts
                packet.duration=1024; packet.time_base=stream.time_base; packet.stream=stream
                out.mux(packet); count+=1
        assert count==fim-ini,(bloco['bloco'],count,fim-ini)
        registros.append(dict(bloco=bloco['bloco'],revisado=novo,origem=str(arquivo.relative_to(p)),frames=count,sha256_pacotes=digest.hexdigest()))
with av.open(str(destino)) as c:
    assert c.streams.video[0].average_rate==15
    assert c.streams.video[0].frames==round(full['duracao']*15)
(p/'montagem_acabamento.json').write_text(json.dumps(registros,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(registros)} blocos, {sum(b["frames"] for b in registros)} quadros; pacotes H.264 copiados sem recompressão.')
