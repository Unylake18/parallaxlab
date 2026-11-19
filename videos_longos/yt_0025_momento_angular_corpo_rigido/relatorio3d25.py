"""Relatório reproduzível de custo e alinhamento das quatro cenas."""
import json
import re
from pathlib import Path
from PIL import Image,ImageDraw
U=Path(__file__).resolve().parent
le=lambda p:json.loads(p.read_text(encoding='utf-8'))
med=le(U/'renders/objetos/medidas.json');ef=le(U/'qa/efeitos.json');al=le(U/'qa/alinhamento.json')
lin=['# Relatório 3D — yt_0025','',
    'Geometrias próprias: pêndulo cônico e pórtico; corpo de 515 cubos e tensor calculado; haltere e mancais de 12 esferas; roda sem marca, com excessos e contrapesos.',
    'O renderer HDR/PBR, câmera, ambiente e bloom foram portados de `mesa.js` do yt_0024 e congelados nos fragmentos locais `renderer25_inicio.js` e `renderer25_pos.js`. A execução usa esses arquivos locais. Nenhuma ficha do arsenal Blender foi portada.',
    '', '## Custo por quadro','',
    'Média de seis chamadas de `setEstado` no Chromium com GPU, incluindo leitura de profundidade; exclui PNG, escrita em disco e composição do Manim. As medições curtas estão sujeitas a variação de carga.',
    '', '| Objeto / estado | Resolução | ms/quadro |','|---|---:|---:|']
lin += [f"| {m['objeto']} | {m['W']}×{m['H']} | {m['ms_por_quadro']:.2f} |" for m in med]
lin+=['','Pipeline completo a 540p, incluindo PNG, máscaras, projeções e disco (lotes processados em paralelo):','','| Lote | Quadros | s/quadro |','|---|---:|---:|']
for l in ['PH','PB1','PB2','PB3','PB4','PB5','PB6','PS']:
    linhas=re.findall(r'^\{.*\}$',(U/f'log_3d_{l}.txt').read_text(encoding='utf-8',errors='replace'),re.M)
    if linhas:
        d=json.loads(linhas[-1]);lin.append(f"| {l} | {d['renderizados']} | {d['s_por_quadro']:.4f} |")
lin+=['','## Efeitos por ablação','','Doze quadros após aquecimento. Os deltas são estimativas por retirada de um efeito, com ruído de GPU; valores negativos indicam ruído da amostra, não ganho físico de desempenho.','',
    '| Cena | Resolução | Configuração | ms/quadro |','|---|---:|---|---:|']
lin += [f"| {m['tipo']} | {m['W']}×{m['H']} | {m['efeito']} | {m['ms_por_quadro']:.2f} |" for m in ef]
lin+=['','Bloom seletivo, DOF com profundidade no hook/abertura, sombra, reflexão aproximada por ambiente PMREM e oito exposições somente no pneu/raios estão implementados. Fresnel no raio X mantém bordas do pneu. Setas e rótulos permanecem no Manim. AO dos cubos usa o número de vizinhos da malha.',
    '', '## Alinhamento','',f"{len(al)} marcadores rasterizados em 24 quadros: erro máximo {max(x['erro_px'] for x in al):.3f} px. Limite: 2 px.",
    '', 'As máscaras completas testam texto sobre sólido; a máscara de palco do voxel separa o corpo da bancada de contexto. As exceções de composição e as falhas ainda abertas constam em `qa.txt`. O resultado não implica aprovação do portão completo.']
(U/'renders/relatorio_3d.md').write_text('\n'.join(lin)+'\n',encoding='utf-8')
nomes=list(dict.fromkeys(m['objeto'] for m in med))
# Cada PNG original é preservado a 1920×1080; a prancha serve apenas como índice.
out=Image.new('RGB',(1440,294*((len(nomes)+2)//3)),'#08122b');d=ImageDraw.Draw(out)
for j,n in enumerate(nomes):
    im=Image.open(U/f'renders/objetos/{n}.png').convert('RGBA');bg=Image.new('RGBA',im.size,'#08122b');bg.alpha_composite(im);bg.thumbnail((480,270));x,y=j%3*480,j//3*294;out.paste(bg.convert('RGB'),(x,y));d.text((x+8,y+274),n,fill='white')
out.save(U/'renders/prancha_objetos.png')
print('Relatório e índice de 11 objetos/estados; originais 1920×1080 preservados')
