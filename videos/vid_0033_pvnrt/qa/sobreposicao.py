"""QA do vid_0033 v5 (v4 + duas linhas, sem motivos, _ ^ { } na tela, cabeçalho×selos, três moléculas, razão do C07) — media_preview/qa_amostras.json (a cada 2 quadros; a cada quadro de −1 s a +2,5 s de cada troca), qa/passos.json, proj.json e
qa/proj_auditoria.json (centro, raio e opacidade de cada esfera, quadros pares).
1. texto × texto e texto × traço/seta (folga 8 px); 2. texto × esferas com opacidade > 35 % (folga 6 px); 3. texto × arestas/aro do 3D (8 px) com o 3D em
   opacidade ≥ 0,5 e rótulo "fora da caixa" × casco convexo do recipiente (6 px); 4. margem de 24 px; 5. faixa da legenda livre (y −6,0 a −4,67);
   6. ponto decimal (d.d) em texto de tela; 7. caderno: itens de linha só dentro da Z_EQ (y −4,5 a +1,17), no máximo 4 linhas por quadro, motivos ≥ 15 px
   de altura, tamanho efetivo das equações (principal/herdada); 8. nenhuma caixa/painel preenchido (itens do tipo "caixa" e a palavra PANEL no código);
   9. passos da álgebra completos e na ordem; 10. cada símbolo apresentado (rótulo preso ao objeto) antes do primeiro uso. → qa/sobreposicao.txt
Uso (raiz): uv run python videos/vid_0033_pvnrt/qa/sobreposicao.py [--midia media_preview]"""
import json
import re
import sys
from pathlib import Path

import numpy as np

UNIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(UNIT))
import roteiro as RT
midia = sys.argv[sys.argv.index('--midia') + 1] if '--midia' in sys.argv else 'media_preview'
dados = json.loads((UNIT / midia / 'qa_amostras.json').read_text(encoding='utf-8'))
trans_t = json.loads((UNIT / midia / 'qa_trans.json').read_text(encoding='utf-8')) if (UNIT / midia / 'qa_trans.json').exists() else []
proj = {int(k): v for k, v in json.loads((UNIT / 'proj.json').read_text(encoding='utf-8')).items()}
pa = UNIT / 'qa' / 'proj_auditoria.json'
aud = {int(k): v for k, v in json.loads(pa.read_text()).items()} if pa.exists() else {}
G8, G6, G12, LX, LY = 8 / 60, 6 / 60, 12 / 60, 4.5 - .4, 8. - .4
Y_EQ_TOP, Y_EQ_BOT = (480 - 410) / 60, (480 - 750) / 60
P = lambda a: np.array([(a[0] - 270) / 60, (480 - a[1]) / 60])


def cam(t):
    K = RT.CAM
    if t <= K[0]['t']:
        return K[0]
    for a, b in zip(K, K[1:]):
        if t <= b['t']:
            u = RT.suave((t - a['t']) / (b['t'] - a['t']))
            return {k: a[k] + (b[k] - a[k]) * u for k in a if k != 't'}
    return K[-1]


def dist(c, pl):
    x0, y0, x1, y1 = c
    pl = np.asarray(pl, float)
    if len(pl) < 2:
        pl = np.vstack([pl, pl])
    best = np.inf
    for p, q in zip(pl[:-1], pl[1:]):
        n = max(2, int(np.linalg.norm(q - p) / .02) + 1)
        pts = p + np.linspace(0, 1, n)[:, None] * (q - p)
        d = np.hypot(np.maximum(np.maximum(x0 - pts[:, 0], 0), pts[:, 0] - x1), np.maximum(np.maximum(y0 - pts[:, 1], 0), pts[:, 1] - y1))
        best = min(best, float(d.min()))
    return best


def hull(pts):
    pts = sorted(map(tuple, pts))
    def meia(ps):
        h = []
        for p in ps:
            while len(h) >= 2 and (h[-1][0] - h[-2][0]) * (p[1] - h[-2][1]) - (h[-1][1] - h[-2][1]) * (p[0] - h[-2][0]) <= 0:
                h.pop()
            h.append(p)
        return h
    return np.array(meia(pts)[:-1] + meia(pts[::-1])[:-1])


def arestas_aro(p):
    c = [P(a) for a in p['cA']]
    ar = [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (1, 3), (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7)]
    pl = [np.array([c[i], c[j]]) for i, j in ar]
    th = np.linspace(0, 2 * np.pi, 24)
    m, r = P(p['m']), p['r'] / 60 * 1.9
    pl.append(np.array([m + r * np.array([np.cos(a), np.sin(a)]) for a in th]))
    return pl


ocorr = {}
vazio_z3d = []
CTA_T = RT.CENAS['CTA']


def reg(k, q):
    ocorr.setdefault(k, []).append(q)


tam_p, tam_h, mot_h = [], [], []
for a in dados:
    q, it = a['q'], a['itens']
    t = q / RT.FPS
    tx = [i for i in it if i['tipo'] == 'texto']
    tr = [i for i in it if i['tipo'] == 'traco']
    K = cam(t)
    q3d = K['op'] >= .5 and K['mix'] < .02 and q in proj
    # conteúdo da Z_3D e da área acima da álgebra (traços, textos e a caixa 3D visível)
    if 0.5 < t < CTA_T:
        ivs = [(i['caixa'][1], i['caixa'][3]) for i in it if i['tipo'] in ('texto', 'traco') and i['caixa'][3] > 1.33 and i['caixa'][1] < 6.95 and not i.get('cab') and not i.get('selo')]
        if K['op'] >= .12 and RT.interp(RT.MV, t) >= .5 and q in proj:
            ys = [(480 - a_[1]) / 60 for a_ in proj[q]['cA']]
            ivs.append((min(ys), max(ys)))
        if not ivs:
            vazio_z3d.append(q)
        topo = [i['caixa'][3] for i in it if i.get('linha') is not None and i['tipo'] == 'texto']
        if topo:
            y_lin = max(topo)
            cur, maior = 6.4, 0.
            for y0, y1 in sorted(ivs, key=lambda v: -v[1]):
                if y1 < cur:
                    maior = max(maior, cur - y1)
                cur = min(cur, y0)
            maior = max(maior, cur - y_lin)
            if maior > 2.0 and not any(abs(t - tt) <= .6 for tt in trans_t):      # só estados estáveis (as trocas duram ≤ 0,6 s)
                reg(('vazio acima da álgebra (> 120 px)', round(maior * 60)), q)

    if any(i['tipo'] == 'caixa' for i in it):
        reg(('caixa/painel preenchido', ), q)
    linhas = {i['linha'] for i in tx if i.get('linha') is not None and i['op'] >= .9}
    if len(linhas) > 2:
        reg(('mais de 2 linhas de álgebra', len(linhas)), q)
    cab = [i for i in tx if i.get('cab')]
    sel = [i for i in tx if i.get('selo')]
    for a_ in cab:
        for b_ in sel:
            gap = a_['caixa'][1] - b_['caixa'][3]
            if gap < 10 / 60 and not (b_['caixa'][1] > a_['caixa'][3]):
                reg(('cabeçalho × selos: folga < 10 px', round(gap * 60, 1)), q)
    for i, A in enumerate(tx):
        c = A['caixa']
        for B in tx[i + 1:]:
            d = B['caixa']
            g_ = G12 if (A.get('linha') is None and B.get('linha') is None) else G8
            if c[0] < d[2] + g_ and c[2] > d[0] - g_ and c[1] < d[3] + g_ and c[3] > d[1] - g_:
                reg(('texto×texto', tuple(np.round(c, 1)), tuple(np.round(d, 1)), A.get('txt'), B.get('txt')), q)
        for T_ in tr:
            if T_.get('guia'):
                continue                       # linha-guia: liga o rótulo ao objeto por definição
            pc = T_['caixa']
            if pc[0] > c[2] + 1 or pc[2] < c[0] - 1 or pc[1] > c[3] + 1 or pc[3] < c[1] - 1:
                continue
            if min(dist(c, pl_) for pl_ in T_['pls']) < G8:
                reg(('texto×traço', tuple(np.round(c, 1)), tuple(np.round(pc, 1))), q)
        if q3d:
            for pl in arestas_aro(proj[q]):
                if dist(c, pl) < G8:
                    reg(('texto×3D (aresta/aro)', tuple(np.round(c, 1)), A.get('txt')), q)
                    break
            if A.get('fora'):
                H = hull([P(a_) for a_ in proj[q]['cA']])
                x0, y0, x1, y1 = c[0] - G6, c[1] - G6, c[2] + G6, c[3] + G6
                if any(all(((H[(k + 1) % len(H)][0] - H[k][0]) * (y - H[k][1]) - (H[(k + 1) % len(H)][1] - H[k][1]) * (x - H[k][0])) > 0 for k in range(len(H))) for x, y in ((x0, y0), (x0, y1), (x1, y0), (x1, y1))):
                    reg(('rótulo "fora da caixa" sobre a silhueta 3D', tuple(np.round(c, 1)), A.get('txt')), q)
        qa_ = q if q in aud else (q - 1 if q - 1 in aud else None)
        if qa_ is not None and aud[qa_].get('todas'):
            for sx, sy, sr, sal in aud[qa_]['todas']:
                if sal <= .35:
                    continue
                cxm, cym, rm = (sx - 270) / 60, (480 - sy) / 60, sr / 60 + G6
                if c[0] - rm < cxm < c[2] + rm and c[1] - rm < cym < c[3] + rm:
                    reg(('texto sob esfera > 35 %', tuple(np.round(c, 1)), A.get('txt')), q)
                    break
        if A.get('txt') and re.search(r'\d\.\d', A['txt']):
            reg(('ponto decimal', A['txt']), q)
        if A.get('txt') and re.search(r'[_^{}]', A['txt']):
            reg(('texto cru com _ ^ { }', A['txt']), q)
        if A.get('linha') is not None and A['op'] >= .9:
            if c[1] < Y_EQ_BOT - .02 or c[3] > Y_EQ_TOP + .02:
                reg(('linha fora da Z_EQ', A['linha'], tuple(np.round(c, 1))), q)
            if A.get('fs'):
                (tam_p if A['linha'] == 1 else tam_h).append(A['fs'])
    for A in it:
        c = A['caixa']
        if c[0] < -LX or c[2] > LX or c[1] < -LY or c[3] > LY:
            reg(('borda (<24 px)', A['tipo'], tuple(np.round(c, 1)), A.get('txt')), q)
        if c[1] < -4.67 and c[3] > -6.0:
            reg(('na faixa da legenda', A['tipo'], tuple(np.round(c, 1))), q)
# Z_3D vazia por mais de 0,5 s
seq_, ini_ = [], None
for q in sorted(vazio_z3d):
    if seq_ and q - seq_[-1] <= 2:
        seq_.append(q)
    else:
        if len(seq_) >= 4:
            reg(('Z_3D vazia > 0,5 s', seq_[0] / 15), seq_[-1])
        seq_ = [q]
if len(seq_) >= 4:
    reg(('Z_3D vazia > 0,5 s', seq_[0] / 15), seq_[-1])
# passos completos e na ordem; símbolos apresentados antes do uso
pj = json.loads((UNIT / 'qa' / 'passos.json').read_text(encoding='utf-8'))
ordem = ['p=mv', 'p_i,p_f', 'dp=pf-pi', '-mv-mv', '-2mv', 'J', 'dt=(L+L)/v', 'dt=2L/v', 'F=J/dt', 'F=2mv/(2L/v)', 'cancela 2', 'P1=F/A', 'A',
         'P1=(mv2/L)/L2', 'L3', 'L3=V', 'P1V', 'soma', 'm sum', 'N<vx2>', 'media def', 'pit i', 'pit media', 'medias iguais', '<v2>=3<vx2>', '<vx2>=<v2>/3', 'subst',
         '1/3Nm<v2>', 'Ec=1/2mv2', 'm<v2>=2Ec', 'subst Ec', '2/3NEc', 'tabela', 'PV=NkBT', '2/3NEc=NkBT', 'Ec=3/2kBT', 'N=nNA', 'R=NAkB', '8,314', 'PV=nRT']
vistos = {k: t for t, k in pj['passos']}
faltam = [k for k in ordem if k not in vistos]
fora_ord = [k for k, k2 in zip(ordem, ordem[1:]) if k in vistos and k2 in vistos and vistos[k] > vistos[k2]]
uso = {'m': 'p=mv', 'v_x': 'p=mv', 'L': 'dt=(L+L)/v', 'A': 'P1=F/A', 'V': 'L3=V'}
apres = {s: (pj['apresentacao'].get(s), vistos.get(k)) for s, k in uso.items()}
sem_apres = [s for s, (a, u) in apres.items() if a is None or u is None or a >= u]
linhas_out = [f'amostras: {len(dados)} · ocorrências distintas: {len(ocorr)} · amostras com ocorrência: {sum(len(v) for v in ocorr.values())}']
for k, qs in sorted(ocorr.items(), key=lambda kv: kv[1][0]):
    linhas_out.append(f'{k[0]} {k[1:]} quadros {qs[0]}–{qs[-1]} ({len(qs)} amostras; t = {qs[0] / 15:.1f}–{qs[-1] / 15:.1f} s)')
linhas_out.append(f'passos da álgebra: {len(ordem) - len(faltam)}/{len(ordem)} presentes' + (f'; FALTAM {faltam}' if faltam else '') + (f'; FORA DE ORDEM {fora_ord}' if fora_ord else '; todos na ordem'))
linhas_out.append('símbolos apresentados antes do uso (t_rótulo < t_uso): ' + ', '.join(f"{s} {a:.1f}<{u:.1f}" if a is not None and u is not None else f'{s} ?' for s, (a, u) in apres.items()) + (f'; PROBLEMA {sem_apres}' if sem_apres else '; OK'))
codigo = (UNIT / 'cena.py').read_text(encoding='utf-8')
linhas_out.append('painel azul preenchido: ' + ('PANEL no código!' if 'PANEL' in codigo else 'nenhum (sem PANEL no código; nenhum item do tipo caixa nas amostras)' if not any(k[0].startswith('caixa') for k in ocorr) else 'ENCONTRADO'))
if tam_p:
    linhas_out.append(f'tamanho efetivo das equações (font_size após o ajuste): linha ativa mín. {min(tam_p):.0f} (alvo ≥ 64) · linha fixa mín. {min(tam_h) if tam_h else 0:.0f} (alvo ≥ 52)')
# três moléculas presentes (88–91 s) e razão do C07
achou = {n: False for n in ('só em x', 'só em y', 'equilibrada')}
for a in dados:
    if 78.2 <= a['q'] / RT.FPS <= 81.0:
        for i in a['itens']:
            if i.get('txt') in achou and i['op'] >= .9:
                achou[i['txt']] = True
linhas_out.append('três moléculas (só em x / só em y / equilibrada) na tela entre 78,2 e 81,0 s: ' + ('OK' if all(achou.values()) else f'FALTAM {[k for k, v in achou.items() if not v]}'))
cont = (UNIT / 'qa' / 'contadores.txt').read_text(encoding='utf-8').strip() if (UNIT / 'qa' / 'contadores.txt').exists() else 'sem contadores.txt'
linhas_out.append('C07 — ' + cont)
mostrar = re.findall(r'mostrar (\d+)', cont)
txts = {i.get('txt') for a in dados for i in a['itens'] if i.get('txt')}
ok_cont = len(mostrar) == 2 and all(m in txts for m in mostrar)
linhas_out.append('contador do C07 na tela = valor medido (' + ' e '.join(mostrar) + '): ' + ('OK' if ok_cont else 'FALHOU'))
hook_ok = all(cam(i / 15)['op'] >= .99 and RT.interp(RT.MV, i / 15) >= .99 for i in range(0, int(10.5 * 15))) and all(v == 0 for _, v in RT.BAL) and all(v == 0 for _, v in RT.HV)
linhas_out.append('hook: caixa 3D visível em 100 % dos quadros de 0 a 10,5 s e sem balão/close: ' + ('OK' if hook_ok else 'FALHOU'))
(UNIT / 'qa' / 'sobreposicao.txt').write_text('\n'.join(linhas_out) + '\n', encoding='utf-8')
print('\n'.join(linhas_out)[:8000])
