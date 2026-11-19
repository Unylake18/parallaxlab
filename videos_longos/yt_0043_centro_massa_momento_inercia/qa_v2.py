"""yt_0043 · QA v2 medido (handoff v2 §7). Lê, de cada still (renders/still/<LOTE>_<T>_caixas.json) e dos segmentos 3D projetados
(threejs/q3d/<LOTE>_1920x1080/<cena>/segs_fNNNNN.json, gravados pelo still.sh via r3d.js --so):

- texto_x_3d_v2.txt      distância mínima (px) entre texto e traço 3D (eixo, seta, aresta da lata, plano); ≥ 24 px
- placas_x_arestas_v2.txt  nenhuma plaquinha cobre segmento 3D projetado
- orfaos_v2.txt          rótulo preso a um 3D que não está na tela (3D sumiu, rótulo ficou)
- paineis_vazios_v2.txt  cartão/painel sem conteúdo
uso: python qa_v2.py [LOTE:T ...]   (sem argumentos: todos os *_caixas.json de renders/still)"""
import json
import math
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
STILL = AQUI / "renders" / "still"
QA = AQUI / "renders" / "v2" / "qa"
QA.mkdir(parents=True, exist_ok=True)
MIN_TEXTO_3D = 24.0


def dist_ponto_caixa(px, py, b):
    dx = max(b[0] - px, 0, px - b[2])
    dy = max(b[1] - py, 0, py - b[3])
    return math.hypot(dx, dy)


def amostra(pl, passo=3.0):
    for (x0, y0), (x1, y1) in zip(pl, pl[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L / passo))
        for k in range(n + 1):
            yield x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n


def segs_de(lote, cena, T):
    f = int(round(T * 15))
    d = AQUI / "threejs" / "q3d" / f"{lote}_1920x1080" / cena
    for ff in (f, f - 1, f + 1):
        p = d / f"segs_f{ff:05d}.json"
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    return None


def sugere(b, segs_all, outros, margem=8.0):
    pts = [(x, y) for _, pl in segs_all for x, y in amostra(pl, 4.0)]
    cands = sorted(((dx, dy) for dx in range(-140, 141, 6) for dy in range(-140, 141, 6)), key=lambda d: abs(d[0]) + abs(d[1]))
    for dx, dy in cands:
        nb = [b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy]
        if nb[0] < 60 or nb[2] > 960 or nb[1] < 150 or nb[3] > 1030:
            continue
        if any(dist_ponto_caixa(x, y, nb) < margem for x, y in pts):
            continue
        if any(not (nb[2] < o[0] - 4 or nb[0] > o[2] + 4 or nb[3] < o[1] - 4 or nb[1] > o[3] + 4) for o in outros):
            continue
        return (dx, dy)
    return None


def main():
    alvos = []
    if len(sys.argv) > 1:
        for a in sys.argv[1:]:
            l, t = a.split(":")
            alvos.append((l, t))
    else:
        for p in sorted(STILL.glob("*_caixas.json")):
            m = re.match(r"(.+?)_([\d.]+)_caixas\.json", p.name)
            alvos.append((m.group(1), m.group(2)))
    t3d, tpl, tor, tpv = ["TEXTO × 3D: pior caso por still (≥ 24 px)"], ["PLAQUINHA × ARESTA: cruzamentos (0 esperado)"], ["ÓRFÃOS: rótulo sem o seu 3D (0 esperado)"], ["PAINÉIS VAZIOS (0 esperado)"]
    for lote, T in alvos:
        arq = STILL / f"{lote}_{T}_caixas.json"
        if not arq.exists():
            continue
        c = json.loads(arq.read_text(encoding="utf-8"))
        tt = float(T)
        ativos = [p for p in c["palcos"] if p["noscene"] and p["op"] > 0.5]
        segs_all = []
        for p in ativos:
            sg = segs_de(lote, p["cena"], tt)
            if sg is None:
                tor.append(f"  {lote} {T}: SEM segs para {p['cena']} (rode o still com --so)")
                continue
            segs_all += [(p["cena"], pl) for pl in sg]
        # rótulos presos ao 3D: não entram em "texto" (ficam perto do 3D por definição), entram em placa × aresta
        rots = {r["txt"] for r in c["rots3"] if r["visivel"]}
        piores = None
        for t in c["textos"]:
            if t["nome"] in rots:
                continue
            b = t["box"]
            if b[1] < 140 and b[0] < 700:
                continue                                           # título do canto
            d = min((dist_ponto_caixa(x, y, b) for _, pl in segs_all for x, y in amostra(pl)), default=999.0)
            if piores is None or d < piores[0]:
                piores = (d, t["nome"], b)
        if ativos:
            if piores:
                t3d.append(f"  {lote} {T}: pior {piores[0]:.1f} px  {piores[1]!r}  {'OK' if piores[0] >= MIN_TEXTO_3D else 'VER'}")
            else:
                t3d.append(f"  {lote} {T}: sem texto fora dos rótulos")
        else:
            t3d.append(f"  {lote} {T}: sem 3D na tela")
        # plaquinha × aresta
        n_cruz = 0
        for pl in c["placas"]:
            b = pl["box"]
            ent = [cena for cena, seg in segs_all for x, y in amostra(seg) if b[0] + 1 < x < b[2] - 1 and b[1] + 1 < y < b[3] - 1]
            if ent:
                n_cruz += 1
                sug = sugere(b, segs_all, [q["box"] for q in c["placas"] if q is not pl] + [t["box"] for t in c["textos"] if t["nome"] not in rots])
                tpl.append(f"  {lote} {T}: plaquinha {pl['nome']!r} {tuple(round(v) for v in b)} cobre traço 3D ({len(ent)} pontos)  VER  sugestão: deslocar {sug} px")
        if not n_cruz:
            tpl.append(f"  {lote} {T}: {len(c['placas'])} plaquinhas, 0 cruzamentos  OK")
        # órfãos
        vivos = {p["cena"] for p in ativos}
        orf = [r for r in c["rots3"] if r["visivel"] and r["cena"] not in vivos]
        if orf:
            for r in orf:
                tor.append(f"  {lote} {T}: rótulo {r['txt']!r} (cena {r['cena']}) sem o 3D na tela  VER")
        else:
            tor.append(f"  {lote} {T}: 0 órfãos  OK")
        # painel vazio
        vz = [p for p in c["paineis"] if p["conteudo"] == 0 and p["op_fill"] > 0.2]
        tpv.append(f"  {lote} {T}: " + (f"{len(vz)} painel(is) vazio(s) {[tuple(round(v) for v in p['box']) for p in vz]}  VER" if vz else "0 vazios  OK"))
    (QA / "texto_x_3d_v2.txt").write_text("\n".join(t3d), encoding="utf-8")
    (QA / "placas_x_arestas_v2.txt").write_text("\n".join(tpl), encoding="utf-8")
    (QA / "orfaos_v2.txt").write_text("\n".join(tor), encoding="utf-8")
    (QA / "paineis_vazios_v2.txt").write_text("\n".join(tpv), encoding="utf-8")
    print("\n".join(t3d + tpl + tor + tpv))


if __name__ == "__main__":
    main()
