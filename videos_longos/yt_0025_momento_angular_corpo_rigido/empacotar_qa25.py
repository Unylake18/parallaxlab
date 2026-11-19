"""Pacote de revisão, sem MP4, áudios, caches nem milhares de quadros intermediários."""
import hashlib,json,zipfile
from pathlib import Path
U=Path(__file__).resolve().parent;R=U/'renders';Q=U/'qa'
res=json.loads((Q/'resumo.json').read_text(encoding='utf-8'))
arquivos=[]
for n in ['qa.txt','relatorio_3d.md','portao_unico.txt','prancha_objetos.png','prancha_24_densos.png']:
    p=R/n
    if p.exists():arquivos.append(p)
arquivos+=list(R.glob('prancha_P*.png'))+list((R/'quadros_qa').glob('*.png'))+list((R/'objetos').glob('*.png'))
arquivos += [p for p in Q.glob('*.json') if '_antes' not in p.name]+list((Q/'alinhamento').glob('*.png'))
arquivos += [p for p in [Q/'excecoes_layout.md',Q/'conferencia_humana.md',U/'patches.json',U/'capitulos_youtube.txt',U/'ancoras.json',U/'tab25.json',U/'ficha.md',U/'handoff_v1.md',U/'narracao_v1.md'] if p.exists()]
for n in ['cena.py','cenas25.py','conteudo25.py','pecas25.py','pecas22.py','kit.py','prob.py','prob2.py','latex25.py','fisica25.py','auditoria25.py','telemetria25.py','verificar_fisica25.py','montar_preview.py','corrigir_ancora25.py','exportar_tabela25.py','transicoes25.py']:
    arquivos.append(U/n)
arquivos += [U/f'tempos_{l}.json' for l in ['PH','PB1','PB2','PB3','PB4','PB5','PB6','PS']]
arquivos += [U/f'algebra_{l}.json' for l in ['PH','PB1','PB2','PB3','PB4','PB5','PB6','PS']]
arquivos += [U/'threejs/geometrias25.js',U/'threejs/estado25.js']
amostra=[]
sel=json.loads((Q/'quadros_selecionados.json').read_text(encoding='utf-8'))
off=json.loads((U/'offsets.json').read_text(encoding='utf-8'))
alvos={}
for ng,area,a,l,f in sel.get('densidade_telemetria',[]):alvos.setdefault(l,set()).add(round(f-off[l]*15))
for l,fs in alvos.items():
    for p in (U/'tab_quadros').glob(f'{l}_*.json'):
        for row in json.loads(p.read_text(encoding='utf-8')):
            if row['quadro'] in fs:amostra.append(dict(lote=l,**row))
sal=R/'tabela_amostra_qa.json';sal.write_text(json.dumps(amostra,separators=(',',':')),encoding='utf-8');arquivos.append(sal)
arquivos=sorted(set(p for p in arquivos if p.exists()))
manifesto=dict(fase='preview silencioso',preview='preview_yt0025_v1_960x540.mp4 (fora do zip)',
    portao_bruto=res['ocorrencias'],status='EM REVISÃO' if res['ocorrencias'] else 'PORTÃO AUTOMÁTICO DE LAYOUT SEM OCORRÊNCIAS; consultar qa.txt para os demais critérios',
    tabelas_completas='tab_quadros/ no projeto; amostra dos 24 estados densos incluída neste zip',
    arquivos=[dict(arquivo=p.relative_to(U).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in arquivos])
mp=R/'manifesto_qa.json';mp.write_text(json.dumps(manifesto,ensure_ascii=False,indent=1),encoding='utf-8')
z=R/'qa_yt0025_v1_sem_mp4.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
    for p in arquivos+[mp]:out.write(p,p.relative_to(U).as_posix())
with zipfile.ZipFile(z) as out:assert not any(n.lower().endswith('.mp4') for n in out.namelist())
print(z,round(z.stat().st_size/1024/1024,2),'MiB;',len(arquivos),'arquivos; zero MP4')
