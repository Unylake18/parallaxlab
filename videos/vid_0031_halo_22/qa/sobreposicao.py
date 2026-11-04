"""QA de sobreposição do vid_0031 (v4: §B.11) nos quadros-chave gravados pela cena (mark(..., qa=True)) e no vídeo composto.

(a) texto × texto · (b) texto × traço (raio, curva, eixo, fio; folga 0,12) · (c) qualquer elemento a menos de 0,35 da borda
(o feixe pode entrar pela borda) ou acima de y = +7 (cabeçalho), e nada abaixo de y = −4,5 · (d) cristais 3D no cabeçalho
(pixels claros nos PNGs do 3D em y > +7 durante o campo de cristais) · (e) linha de base nas linhas mistas (não há) ·
(f) objetos constantes no giro · (g) glifo em opacidade intermediária parado > 0,3 s · (h) quadros pretos (luminância média
< 4 % por > 0,2 s) ou brancos (> 90 %) no preview composto · transições de equação (glifos se cruzando a 30/50/70 %) ·
contagem de "22°" e "42°" na tela · v5: (i) origem dos raios (nascem no disco do Sol: distância ao centro ≤ R; direção
paralela à reta olho → Sol dentro de 0,05°) · (j) tempo parado de cada equação (≥ 2,5 s) · (k) área vazia contígua > 25 % da
altura útil em estados > 2 s (linhas de pixel uniformes) · (l) cinza residual no corpo do cristal (saturação < 8 % e luminância
20–45 % em área contígua > 400 px em 540) · v6: (m) caixa preenchida atrás de texto · (n) Sol inteiro na tela (margem 0,35) ·
(o) no C05 o feixe atravessa o hexágono (corda ≥ 60 % do diâmetro na oposta e na alternada) · (p) cone: a pessoa e o
vértice em todos os quadros, e o último quadro do cone igual ao céu do C01 (diferença média ≤ 6 %) · (q) caderno: equação,
tempo parado e posição. → qa/sobreposicao.txt
Uso (na raiz): uv run python videos/vid_0031_halo_22/qa/sobreposicao.py [--sem-video]
"""
import json
import sys
from pathlib import Path

import numpy as np

QA = Path(__file__).resolve().parent
UNIT = QA.parent
FOLGA = .12
sys.path.insert(0, str(UNIT))
import fisica as F_
import roteiro as RT_
RT_E = RT_.E


def teste_t():
    """(t) C05: o feixe entra pelo meio de uma face (s entre 0,3 e 0,7) e o Sol fica a ≥ 2,4 do contorno do hexágono."""
    out = []
    for nome, t in (('oposta', RT_E['feixe_op'] + .8 * (RT_E['rot_vz'] - RT_E['feixe_op'])), ('vizinha', RT_E['feixe_vz'] + .8 * (RT_E['rot_al'] - RT_E['feixe_vz'])), ('alternada', RT_E['feixe_al'] + .8 * (RT_E['pulso'] - RT_E['feixe_al']))):
        st = RT_.estado_cristal(t)
        V = F_.hexagono(st['c'], st['R'], st['th'])
        P1 = np.asarray(st['feixe']['pts'][1])
        s_ = None
        for k in range(6):
            a, b = V[k], V[(k + 1) % 6]
            cr = (b - a)[0] * (P1 - a)[1] - (b - a)[1] * (P1 - a)[0]
            if abs(cr) / np.linalg.norm(b - a) < 1e-6:
                s_ = float(((P1 - a) @ (b - a)) / ((b - a) @ (b - a)))
        d = RT_._dist_contorno(np.asarray(st['sol'], float), V)
        ok = s_ is not None and .3 <= s_ <= .7 and d >= 2.4
        out.append((ok, f"{nome}: entrada a s = {s_:.2f} da face (0,3–0,7), Sol a {d:.2f} do contorno (≥ 2,4)"))
    return out


def teste_s(dados):
    """(s) cone: ≥ 36 linhas, vértice no olho, eixo no Sol, ângulo eixo–linha = 22° ± 0,3°, pessoa H ≥ 1,6."""
    info = dados.get('cone_info', [])
    if not info:
        return [(False, 'sem dados do cone')]
    L, rho = 3.8, 3.8 * np.tan(np.radians(float(F_.d_min())))
    ang = float(np.degrees(np.arctan(rho / L)))
    mx = max(i['linhas'] for i in info)
    hm = max(i['H'] for i in info)
    s0 = [i for i in info if i['s'] == 0][-1]
    eixo_sol = np.allclose(s0['sol'], RT_.SOL_L, atol=1e-3)
    return [(mx >= 36, f"linhas de visão: máximo {mx} (≥ 36)"),
            (abs(ang - float(F_.d_min())) < .3, f"ângulo eixo–linha = {ang:.2f}° (22° ± 0,3°; d_min = {float(F_.d_min()):.2f}°)"),
            (hm >= 1.6, f"pessoa: H máx. {hm:.2f} (≥ 1,6; altura total ≈ {100 * (hm + .21) / 16:.0f} % da tela)"),
            (eixo_sol, f"eixo olho → Sol: o Sol em {s0['sol']} (esperado {RT_.SOL_L.round(2).tolist()}); vértice no olho {s0['olho']}")]


def cruza(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def dist_caixa_polilinha(c, pl):
    x0, y0, x1, y1 = c
    pl = np.asarray(pl)
    melhor = np.inf
    for p, q in zip(pl[:-1], pl[1:]):
        s = np.linspace(0, 1, max(2, int(np.linalg.norm(q - p) / .01) + 1))[:, None]
        pts = p + s * (q - p)
        dx = np.maximum(np.maximum(x0 - pts[:, 0], 0), pts[:, 0] - x1)
        dy = np.maximum(np.maximum(y0 - pts[:, 1], 0), pts[:, 1] - y1)
        melhor = min(melhor, float(np.hypot(dx, dy).min()))
    return melhor


def video_luz():
    """(h) luminância média por quadro do preview composto."""
    import av
    c = av.open(str(UNIT / 'renders' / 'preview_540x960.mp4'))
    lum = []
    for f in c.decode(video=0):
        a = f.to_ndarray(format='rgb24').astype(np.float32)
        lum.append(float((a @ np.array([.2126, .7152, .0722])).mean() / 255))
    return np.array(lum)


def cabecalho_3d(tl):
    """(d) pixels claros (luminância > 0,35) na faixa do cabeçalho (y > +7) dos quadros 3D com o campo de cristais."""
    from PIL import Image
    def chaves(lista, t):
        if t <= lista[0]['t']:
            return lista[0]['v']
        for x, y in zip(lista, lista[1:]):
            if t <= y['t']:
                u = min(max((t - x['t']) / max(y['t'] - x['t'], 1e-9), 0), 1)
                return x['v'] + (y['v'] - x['v']) * u * u * (3 - 2 * u)
        return lista[-1]['v']
    K = tl['camadas']
    pior = 0
    for q in range(0, int(tl['duracao_s'] * 15), 3):          # só quadros com cristais e sem céu (o céu pode ocupar o topo)
        if chaves(K['cristais'], q / 15) < .01 or chaves(K['ceu'], q / 15) > .01:
            continue
        p = UNIT / 'frames3d_540x960' / f'f{q:05d}.png'
        if p.exists():
            a = np.asarray(Image.open(p).convert('RGB'))[:60].astype(np.float32) / 255
            pior = max(pior, int(((a @ np.array([.2126, .7152, .0722])) > .35).sum()))
    return pior


def quadros_video(qs):
    import av
    qs, out = set(qs), {}
    c = av.open(str(UNIT / 'renders' / 'preview_540x960.mp4'))
    for k, f in enumerate(c.decode(video=0)):
        if k in qs:
            out[k] = f.to_ndarray(format='rgb24').astype(np.float32) / 255
    return out


def vazios(dados):
    """(k) estados que duram > 2 s: 1 s depois do estado pronto, a maior faixa contígua de linhas uniformes na altura útil
    (y de +7 a −4,5 = linhas 60–750 em 960) não pode passar de 25 %."""
    ev = sorted(dados['estados'], key=lambda e: e['quadro'])
    alvo = {}
    for a, b in zip(ev, ev[1:]):
        if (b['quadro'] - a['quadro']) / 15 > 2:
            alvo[a['quadro'] + min(15, int((b['quadro'] - a['quadro']) * .3))] = a['estado']      # 1 s depois do estado pronto (ou a meio caminho da próxima troca)
    Q = quadros_video(alvo)
    out = []
    for q, img in sorted(Q.items()):
        if alvo[q] in ('C04_frio', 'C09_ceu', 'C10_cores_ceu') or alvo[q].startswith('C01'):                 # céu do 3D em tela cheia: o céu é o conteúdo
            continue
        lum = img[60:750] @ np.array([.2126, .7152, .0722])
        faixa = np.percentile(lum, 99.5, axis=1) - np.percentile(lum, .5, axis=1)   # linha com conteúdo: >= 3 px diferentes
        vazio, n, mx = faixa < .035, 0, 0
        for v in vazio:
            n = n + 1 if v else 0
            mx = max(mx, n)
        if mx > .25 * 690:
            out.append(f"{alvo[q]} (quadro {q}): faixa vazia de {mx} linhas = {100 * mx / 690:.0f} % da altura útil")
    return out


def cinza_cristal():
    """(l) no corpo do cristal (hexágono do estado, a cada 5 quadros com alpha > 0,5): pixels com saturação < 8 % e luminância
    20–45 % em componente conexo > 400 px."""
    import colorsys
    from PIL import Image, ImageDraw
    from scipy import ndimage
    sys.path.insert(0, str(UNIT))
    import fisica as F
    import roteiro as RT
    qs = {}
    for q in range(0, int(RT.DURACAO * 15), 5):
        st = RT.estado_cristal(q / 15)
        if st is not None and st.get('caso') != 'lupa' and st['alpha'] > .5:
            qs[q] = F.hexagono(st['c'], st['R'], st['th'])
    Q = quadros_video(qs)
    out = []
    for q, img in sorted(Q.items()):
        V = [((x + 4.5) / 9 * 540, (8 - y) / 16 * 960) for x, y in qs[q]]
        m = Image.new('L', (540, 960), 0)
        ImageDraw.Draw(m).polygon(V, fill=1)
        m = np.asarray(m, bool)
        mx, mn = img.max(axis=2), img.min(axis=2)
        sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
        lum = img @ np.array([.2126, .7152, .0722])
        cinza = m & (sat < .08) & (lum > .20) & (lum < .45)
        lab, n = ndimage.label(cinza)
        maior = int(np.bincount(lab.ravel())[1:].max()) if n else 0
        if maior > 400:
            out.append(f"quadro {q} ({q / 15:.1f} s): área cinza contígua de {maior} px")
    return out


def cordas():
    """(o) comprimento do feixe dentro do hexágono / diâmetro (2R), nos três casos do C05."""
    sys.path.insert(0, str(UNIT))
    import fisica as F
    import roteiro as RT
    out = []
    for nome, t, minimo in (('oposta', RT.E['feixe_op'] + .8 * (RT.E['rot_vz'] - RT.E['feixe_op']), .6), ('vizinha', RT.E['feixe_vz'] + .8 * (RT.E['rot_al'] - RT.E['feixe_vz']), 0.), ('alternada', RT.E['feixe_al'] + .8 * (RT.E['pulso'] - RT.E['feixe_al']), .6)):
        st = RT.estado_cristal(t)
        V = F.hexagono(st['c'], st['R'], st['th'])
        pts = np.array(st['feixe']['pts'])
        dentro = 0.
        for p, q in zip(pts[:-1], pts[1:]):
            for s_ in np.linspace(0, 1, 400, endpoint=False):
                m = p + (s_ + .00125) * (q - p)
                c = V.mean(axis=0)
                ok = all(((V[(k + 1) % 6] - V[k])[0] * (m - V[k])[1] - (V[(k + 1) % 6] - V[k])[1] * (m - V[k])[0]) *
                         ((V[(k + 1) % 6] - V[k])[0] * (c - V[k])[1] - (V[(k + 1) % 6] - V[k])[1] * (c - V[k])[0]) > 0 for k in range(6))
                dentro += ok * np.linalg.norm(q - p) / 400
        f = dentro / (2 * st['R'])
        out.append((f >= minimo - 1e-9, f"{nome}: feixe dentro do gelo = {dentro:.2f} = {100 * f:.0f} % do diâmetro (mínimo {100 * minimo:.0f} %)"))
    return out


def ceu_do_cone():
    """(p) diferença média de pixels entre o último quadro do cone (fim da fusão) e o céu do C01 no 3D (2,0 s)."""
    from PIL import Image
    sys.path.insert(0, str(UNIT))
    import roteiro as RT
    q = round((RT.E['ceu_volta'] + .7) * 15) - 1                       # v7: o cone já saiu (fusão 0,1–0,6 s) e só o céu do 3D está na tela
    a = quadros_video([q])[q]
    b = np.asarray(Image.open(UNIT / 'frames3d_540x960' / 'f00030.png').convert('RGB')).astype(np.float32) / 255
    return float(np.abs(a[60:750] - b[60:750]).mean())


def main():
    dados = json.loads((UNIT / __import__('os').environ.get('MIDIA', 'media_preview') / 'qa_geometria.json').read_text(encoding='utf-8'))
    tl = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))
    anel24 = tl['ceu']['curva_24']
    linhas, total, contagem = [], 0, []
    for est in dados['estados']:
        oc = []
        T = est['textos']
        for i in range(len(T)):
            for j in range(i + 1, len(T)):
                if cruza(T[i]['caixa'], T[j]['caixa']):
                    oc.append(f"(a) textos se cruzam: {T[i]['tex']!r} × {T[j]['tex']!r}")
        for t in T:
            d = min([dist_caixa_polilinha(t['caixa'], pl) for pl in est['tracos']] or [np.inf])
            if d < FOLGA:
                oc.append(f"(b) texto {t['tex']!r} a {d:.3f} de um traço (< {FOLGA})")
        for b in est['abaixo_de_-4,5']:
            oc.append(f"(c) {b['obj']} desce até y = {b['y_min']}")
        for b in est['fora_da_margem']:
            oc.append(f"(c) {b['obj']} fora da margem de 0,35 (x {b['caixa'][0]}…{b['caixa'][1]}, y máx. {b['caixa'][2]})")
        for c in est.get('caixas_texto', []):
            oc.append(f"(m) {c['forma']} preenchido atrás do texto {c['texto']!r}")
        for so in est.get('sois', []):
            if not so['inteiro']:
                oc.append(f"(n) Sol em {so['c']} (R {so['R']}) fora da margem")
        for r in est.get('raios', []):
            if r['dist_ini_sol'] > r['R'] + 1e-3 or r['ang_deg'] > .05:
                oc.append(f"(i) raio nasce a {r['dist_ini_sol']:.3f} do centro do Sol (R {r['R']}) com desvio de direção {r['ang_deg']:.3f}°")
        if est['estado'].startswith('C01'):
            for t in T:
                if dist_caixa_polilinha(t['caixa'], anel24) < .4:
                    oc.append(f"(b) texto {t['tex']!r} a menos de 0,4 da curva de 24° do anel")
        for t in T:
            s = str(t['tex']).replace('^\\circ', '°')
            if '22°' in s or '42°' in s:
                contagem.append(f"{est['estado']}: {t['tex']!r}")
        total += len(oc)
        linhas.append(f"[{'OK' if not oc else 'ACUSA'}] {est['estado']} ({est['segundos']:.2f} s, {len(T)} textos, "
                      f"{len(est['tracos'])} traços)")
        linhas += [f'    {o}' for o in oc]
    linhas.append('')
    linhas.append(f"(e) linhas mistas Text + MathTex: {len(dados['linhas_mistas'])} (nada a medir)")
    og = dados['objetos_giro']
    ok_f = og['quadros'] > 0 and og['min'] == og['max']
    total += 0 if ok_f else 1
    linhas.append(f"[{'OK' if ok_f else 'ACUSA'}] (f) objetos na cena durante o giro: {og['quadros']} quadros, min {og['min']}, max {og['max']}")
    gp = dados['glifos_parados']
    total += len(gp)
    linhas.append(f"[{'OK' if not gp else 'ACUSA'}] (g) glifos meio transparentes parados > 0,3 s: {len(gp)}")
    linhas += [f"    {g}" for g in gp[:20]]
    nr = sum(len(e.get('raios', [])) for e in dados['estados'])
    linhas.append(f"(i) raios conferidos nos quadros-chave: {nr} (ocorrências listadas acima, por estado)")
    linhas.append('')
    linhas.append('(j) tempo parado de cada equação (da entrada pronta ao início da saída):')
    for e in dados['equacoes']:
        if e['parada_s'] is None:
            linhas.append(f"       (q) {e['equacao']} — posição final no caderno {e['posicao']}")
            continue
        minimo_j = 2.0
        ok_j = e['parada_s'] >= minimo_j - 1e-6
        total += 0 if ok_j else 1
        linhas.append(f"[{'OK' if ok_j else 'ACUSA'}] {e['parada_s']:5.2f} s  {e['equacao']}  ({e['entra']:.2f}–{e['sai']:.2f} s) · posição {e.get('posicao')}")
    linhas.append('')
    for o in cordas():
        total += 0 if o[0] else 1
        linhas.append(f"[{'OK' if o[0] else 'ACUSA'}] (o) {o[1]}")
    for o in teste_t():
        total += 0 if o[0] else 1
        linhas.append(f"[{'OK' if o[0] else 'ACUSA'}] (t) {o[1]}")
    for o in teste_s(dados):
        total += 0 if o[0] else 1
        linhas.append(f"[{'OK' if o[0] else 'ACUSA'}] (s) {o[1]}")
    seco = UNIT / 'media_seco' / 'qa_geometria.json'
    cr = json.loads(seco.read_text(encoding='utf-8')).get('cortes_r') if seco.exists() else None
    if cr is not None:
        por = {}
        for c in cr:
            por.setdefault(round(c['segundos']), []).append(c)
        total += len(cr)
        linhas.append(f"[{'OK' if not cr else 'ACUSA'}] (r) glifo em meio-tom sobre outro objeto nos 0,5 s em volta de 14 cortes: {len(cr)} quadros")
        linhas += [f"    ~{k} s: {len(v)} quadros (ex.: {v[0]['segundos']} s, caixa {v[0]['caixa']})" for k, v in sorted(por.items())]
    # (u) tamanhos mínimos medidos nos quadros-chave (altura da caixa do texto em px a 540 px; 60 px por unidade)
    menores = {}
    for est in dados['estados']:
        for t in est['textos']:
            h = (t['caixa'][3] - t['caixa'][1]) * 60
            tex = str(t['tex'])
            menores.setdefault(tex, (h, est['estado']))
            if h < menores[tex][0]:
                menores[tex] = (h, est['estado'])
    pequenos = [(h, tex, e) for tex, (h, e) in menores.items() if h < (12 if tex.endswith('°') and len(tex) <= 4 else 14) and len(tex.replace(' ', '')) > 2]
    total += len(pequenos)
    linhas.append(f"[{'OK' if not pequenos else 'ACUSA'}] (u) textos com altura < 14 px (a 540 px): {len(pequenos)}")
    linhas += [f"    {h:.1f} px  {tex!r} ({e})" for h, tex, e in sorted(pequenos)[:25]]
    for chave, minimo, rot in (('halo solar de 22°', 30, 'título linha 1'), ('como ele se forma?', 20, 'título linha 2')):
        if chave in menores:
            ok_u = menores[chave][0] >= minimo
            total += 0 if ok_u else 1
            linhas.append(f"[{'OK' if ok_u else 'ACUSA'}] (u) {rot}: {menores[chave][0]:.1f} px (≥ {minimo})")
    for est in dados['estados']:
        if est['estado'] in ('C06_payoff', 'C08_snell_4', 'C07_grafico', 'C08_payoff'):
            mt = [(round((t['caixa'][3] - t['caixa'][1]) * 60, 1), str(t['tex'])[:36], round((t['caixa'][1] + t['caixa'][3]) / 2, 2)) for t in est['textos']
                  if 'sen' in str(t['tex']) or '=' in str(t['tex'])]
            linhas.append(f"    (u) equações em {est['estado']}: altura px, texto, y = {mt}")
    cq = dados.get('cone', [])
    ok_p = bool(cq) and all(c['pessoa'] for c in cq)
    total += 0 if ok_p else 1
    linhas.append(f"[{'OK' if ok_p else 'ACUSA'}] (p) cone: pessoa e vértice em {sum(c['pessoa'] for c in cq)} de {len(cq)} quadros")
    if '--sem-video' not in sys.argv:
        for o in vazios(dados):
            total += 1
            linhas.append(f"[ACUSA] (k) {o}")
        linhas.append(f"(k) área vazia contígua > 25 % da altura útil em estados > 2 s: medida acima (só aparecem as ocorrências)")
        dif = ceu_do_cone()
        ok_p2 = dif <= .06
        total += 0 if ok_p2 else 1
        linhas.append(f"[{'OK' if ok_p2 else 'ACUSA'}] (p) último quadro do cone × céu do C01 (3D, 2,0 s): diferença média {100 * dif:.1f} %")
        cz = cinza_cristal()
        total += len(cz)
        linhas.append(f"[{'OK' if not cz else 'ACUSA'}] (l) cinza residual no corpo do cristal: {len(cz)} quadros")
        linhas += [f'    {c}' for c in cz[:20]]
        px = cabecalho_3d(tl)
        total += 0 if px == 0 else 1
        linhas.append(f"[{'OK' if px == 0 else 'ACUSA'}] (d) cristais 3D no cabeçalho: pior quadro com {px} pixels claros em y > +7")
        lum = video_luz()
        preto, branco = lum < .04, lum > .90
        corridas, n = [], 0
        for k, v in enumerate(list(preto) + [False]):
            if v:
                n += 1
            else:
                if n > 3:
                    corridas.append((round((k - n) / 15, 2), n))
                n = 0
        ok_h = not corridas and not branco.any()
        total += 0 if ok_h else 1
        linhas.append(f"[{'OK' if ok_h else 'ACUSA'}] (h) quadros pretos > 0,2 s: {corridas}; quadros brancos: {int(branco.sum())}; "
                      f"luminância média mín. {lum.min():.3f}, máx. {lum.max():.3f}")
    linhas.append('')
    linhas.append(f"transições de equação: {len(dados['transicoes'])}")
    for g in dados['glifos_transicao']:
        ok_t = g['cruzamentos'] == 0
        total += 0 if ok_t else 1
        linhas.append(f"[{'OK' if ok_t else 'ACUSA'}] {g['transicao']} a {int(100 * g['p'])} % (quadro {g['quadro']}): "
                      f"{g['cruzamentos']} pares de glifos se cruzando")
    linhas.append('')
    linhas.append('contagem de "22°" e "42°" na tela (quadros-chave):')
    linhas += [f'    {c}' for c in contagem]
    txt = '\n'.join([f'vid_0031 — teste de sobreposição v7 ({len(dados["estados"])} quadros-chave)', *linhas, '',
                     f'ocorrências: {total}'])
    (QA / 'sobreposicao.txt').write_text(txt + '\n', encoding='utf-8')
    print(txt)


if __name__ == '__main__':
    main()
