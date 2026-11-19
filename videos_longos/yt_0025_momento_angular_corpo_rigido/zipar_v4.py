"""Zip de QA do v4 (handoff v4 §5): portões, tiras, sequências, relatório 3D e o preview. uso: python zipar_v4.py"""
import zipfile
from pathlib import Path
U=Path(__file__).resolve().parent;Q=U/'qa';R=U/'renders'
arq=[]
for padrao in ['tamanho_*.txt','contraste_*.txt','residuo_*.txt','cadencia_*.txt','flash_*.txt','flash.txt','angulo_tela_*.txt','g28_resumo.txt','ordem_*.txt','excecoes_layout.md','alinhamento.json','seq_*.png','camera_*.png','v4_*.png']:
    arq+=list(Q.glob(padrao))
arq+=list((Q/'ordem').glob('*.png'))+list((Q/'flash').glob('*.png'))
arq+=[R/'relatorio_3d_v4.md',R/'preview_yt0025_v5_completo_960x540.mp4']
arq+=[U/n for n in ['cenas25.py','pecas25.py','conteudo25.py','fisica25.py','gates25.py','g28_resumo.py','seq25.py','tira25.py','relatorio3d_v4.py','threejs/geometrias25.js','threejs/estado25.js']]
arq=[p for p in dict.fromkeys(arq) if p.exists()]
z=R/'qa_yt0025_v5_completo.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
    for p in arq:out.write(p,p.relative_to(U).as_posix())
print(z,round(z.stat().st_size/1024/1024,1),'MiB;',len(arq),'arquivos')
