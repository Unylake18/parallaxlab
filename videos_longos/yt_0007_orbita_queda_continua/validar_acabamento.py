"""Física preservada, densidade nativa e custo do material por enquadramento."""
import json
import time
from pathlib import Path
import numpy as np
from superficie import recorte_rgba
from validar_repagina import verificar


def validar():
    resultado=verificar()
    amostras=[]
    for w,h in [(960,540),(1920,1080)]:
        for k,cy in [(2,0),(12,-11.5),(26,-26.91),(1e6,-1e6)]:
            recorte_rgba.cache_clear()
            inicio=time.perf_counter()
            dados=recorte_rgba(0.,float(cy),float(k),0.,0.,16.,9.,w,h)
            ms=(time.perf_counter()-inicio)*1000
            assert dados is not None
            rgba,cp,largura,altura=dados
            assert rgba.shape[0]<=h and rgba.shape[1]<=w
            assert abs(rgba.shape[1]/largura-w/16)<1e-8
            assert abs(rgba.shape[0]/altura-h/9)<1e-8
            amostras.append(dict(resolucao=f'{w}x{h}',raio_logico=k,
                                 recorte=list(rgba.shape),bytes=rgba.nbytes,ms=round(ms,2)))
        recorte_rgba.cache_clear()
        a=recorte_rgba(0.,-26.91,25.999,0.,0.,16.,9.,w,h)[0]
        b=recorte_rgba(0.,-26.91,26.001,0.,0.,16.,9.,w,h)[0]
        assert a.shape==b.shape
        assert np.mean(np.abs(a.astype(float)-b.astype(float)))<1
        assert recorte_rgba.cache_info().currsize<=2
    resultado.update(material_nativo=amostras,cache_recortes=2,
                     continuidade_antigo_limiar='aprovada',escala_imagem_por_pixel=1)
    p=Path(__file__).resolve().parent/'validacao_acabamento.json'
    p.write_text(json.dumps(resultado,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(status='aprovado',material=amostras),ensure_ascii=False,indent=2))


if __name__=='__main__': validar()
