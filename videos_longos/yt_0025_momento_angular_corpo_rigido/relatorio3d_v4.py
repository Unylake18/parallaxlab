"""Relatório 3D v4 (AGENTS.md 'Relatório' + handoff v4 §4.2): cenas Three.js, o que foi portado, resolução, custo por quadro e alinhamento 3D × Manim em px.
uso: python relatorio3d_v4.py  → renders/relatorio_3d_v4.md (lê log_3d_*.txt, qa/alinhamento.json, renders/relatorio_3d.md para o custo isolado)"""
import json,re
from pathlib import Path
U=Path(__file__).resolve().parent
al=json.loads((U/'qa/alinhamento.json').read_text(encoding='utf-8'))
por_cam={}
for a in al:por_cam.setdefault(re.sub(r'_?\d+$','',a['quadro']),[]).append(a['erro_px'])
iso=(U/'renders/relatorio_3d.md').read_text(encoding='utf-8')
tab=re.findall(r'^\| (\S+) \| 960×540 \| ([\d.]+) \|$',iso,re.M)
lin=['# Relatório 3D v4 — yt_0025','',
'## Cenas Three.js (todas com geometria própria; nada portado do arsenal Blender)','',
'| Cena | Onde aparece | Câmeras / planos |','|---|---|---|',
'| `pendulo_conico` | PB1 (B1-0…B1-7) | P_34 (geral), P_CLOSE (prego e cone, B1-3/4/5) |',
'| `corpo_voxel` (515 cubos, tensor calculado) | PB2, B4-3 | V_34, V_CLOSE (cubinho, B2-2); remontagem pelo eixo de MENOR inércia (corpo em pé) |',
'| `haltere_torto` | PB3, PB4 (B4-1/2), PB5 | H_34, H_34B (B4), H_LADO (ortográfica, B3-5/6), H_TOPO (ortográfica, vista de cima), H_MANCAL (ortográfica, 180,0° nos mancais) |',
'| `roda_balanceamento` | PB6 | R_34, R_CLOSE, R_AXIAL (ortográfica, eixo = ponto) |',
'| `bancada_dupla` (nova) | PH (hook e A1/A2), S1 | D_34 (ortográfica; régua fixa, balanço de 10° do torto) |',
'| `plataforma_livre` (nova) | S2 | PL_34, PL_TOPO (ortográfica, vista de topo) |',
'','Vistas de topo (TOPO) não são cenas novas: são câmeras ortográficas (`H_TOPO`, `PL_TOPO`) das cenas acima; nelas a base da bancada fica oculta e a sombra de piso é desligada (`sol.castShadow = false`).',
'','Porte de fichas do arsenal: nenhum (`solido_3d: nenhum do arsenal Blender`); as geometrias foram escritas no próprio `threejs/geometrias25.js`.',
'','## Resolução','','Preview 960×540 a 15 fps e render final 1920×1080 a 30 fps (PNG por quadro, máscaras, `pontos.json` com as projeções; lotes `media_F_<lote>`). Originais de objeto a 1920×1080 em `renders/objetos/`.',
'','## Custo por quadro','','Isolado (média de seis `setEstado`, Chromium com GPU, 960×540, sem PNG/disco), medição da rodada anterior:','','| Objeto / estado | ms/quadro |','|---|---:|']
lin+=[f'| {n} | {v} |' for n,v in tab]
lin+=['','Pipeline completo a 540p (PNG + máscaras + projeções + disco), última execução de cada lote:','','| Lote | Quadros renderizados | s/quadro |','|---|---:|---:|']
for l in ['PH','PB1','PB2','PB3','PB4','PB5','PB6','PS']:
    p=U/f'log_3d_{l}.txt'
    if not p.exists():continue
    linhas=re.findall(r'^\{.*\}$',p.read_text(encoding='utf-8',errors='replace'),re.M)
    if linhas:
        d=json.loads(linhas[-1]);lin.append(f"| {l} | {d['renderizados']} | {d['s_por_quadro']:.4f} |")
lin+=['','## Alinhamento 3D × Manim','',f'{len(al)} marcadores rasterizados no Three.js (centroide verde no PNG) contra a projeção Python `proj()`; limite 2 px.','','| Câmera / grupo | marcadores | erro máximo (px) |','|---|---:|---:|']
for k,v in sorted(por_cam.items()):lin.append(f'| {k} | {len(v)} | {max(v):.3f} |')
a1=json.loads((U/'qa/alinhamento_1080.json').read_text(encoding='utf-8')) if (U/'qa/alinhamento_1080.json').exists() else []
lin+=['',f'Erro máximo geral (540p): {max(a["erro_px"] for a in al):.3f} px; falhas (> 2 px): {sum(not a["ok"] for a in al)}.',
'Mesmo teste repetido em 1920×1080 (viewport 1920×1080, esperado = projeção ×2; inclui `D_S1` e `H_34` do v6): '+(f'{len(a1)} marcadores, erro máximo {max(x["erro_px"] for x in a1):.3f} px, falhas (> 2 px): {sum(not x["ok"] for x in a1)}.' if a1 else 'não medido.'),
'','## O que faltou','',
'- Sombra de piso grande no PERFIL da plataforma (S2, PL_34): contato físico plausível, mas escura demais; não alterada.',
'- O alinhamento mede as câmeras (matriz de projeção); o alinhamento de cada vetor/rótulo depende do `pontos.json` por quadro, conferido por amostragem nos portões `ANGULO NA TELA` e `MANCAIS ANGULO`.']
(U/'renders/relatorio_3d_v4.md').write_text('\n'.join(lin)+'\n',encoding='utf-8');print('renders/relatorio_3d_v4.md')
