"""QA de sobreposição do vid_0030 (v3): máscaras por GRUPO NOMEADO, todas as camadas, todos os quadros.

Entradas (geradas pelo próprio pipeline):
  - Manim: media_preview/caixas_CenaMat.json — caixa de cada glifo visível por quadro, com o grupo (linha de álgebra,
    memo, rótulo...) e a opacidade (cena.py, Base._registra);
  - Remotion: remotion/render_remotion_v5.log — linhas "QA|quadro|[...]" com a caixa real de cada elemento data-g
    (render com --props '{"qa":true}' --log=verbose), opacidade e texto;
  - 3D: mask3d_540x960/fNNNNN.png (render3d.js --mascara): sólido = R, linha auxiliar = G, plano = B.

Regras (px no 540×960):
  1. caixa × caixa de grupos diferentes: qualquer interseção > 0 px é sobreposição. Exceções: o mesmo grupo (fórmula e
     sua caixa; régua, rótulo e chamadas); glifo em trânsito de um glyph map sobre a própria origem/destino (IoU > 0,6:
     é o "pulso" da cópia).
  2. texto × 3D: nenhum pixel de sólido, linha auxiliar ou plano dentro da caixa de um texto. Exceções: rótulos de linha
     auxiliar desenhados sobre o corte (rot_aux) e as chamadas tracejadas da régua (vão até a aresta do anel).
  3. rótulos do 3D (etiqueta do hook, R = …, régua, "raio h/2", contadores): folga ≥ 12 px da silhueta (máscara dilatada).
  4. margens: nada (texto, sólido, linha, plano) a menos de 24 px das bordas laterais.
  5. zona do 3D: sólido e linhas dentro da zona_3d do trecho (timeline "zonas").
  6. opacidade: menor opacidade de texto visível fora de entradas/saídas (rampas monotônicas que começam ou terminam em 0).
  7. dedupe: cada mensagem da tabela aparece num único intervalo contínuo.
Uso (raiz): uv run python videos/vid_0030_anel_guardanapo/qa/sobreposicao.py [saida.json]
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation

UNIT = Path(__file__).resolve().parents[1]
TL = json.loads((UNIT / "timeline.json").read_text(encoding="utf-8"))
FPS, W, H = 15, 540, 960
N = round(TL["duracao_s"] * FPS)
XS = TL["zonas"]["x_seguro"]
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "qa" / "sobreposicao_v5.json"

ISENTO_3D = ("rot_aux",)
# glifos em trânsito (glyph map / cópia) podem passar pela própria origem ou destino declarados — é o caminho da cópia:
# C03: blocos r_ext², r_int² e R² − a² vêm das linhas X, I e do lembrete e o bloco (R² − a²) entra no lembrete
ORIGENS = {}                          # v5: nenhuma isenção de cópia sobre a origem (a cópia nasce fora dela)                         # rótulos de linha auxiliar sobre o desenho
ROTULOS_3D = ("tag_hook", "rot_trio", "C04_raio", "C04_cont", "regua")   # folga ≥ 12 px (só o texto do rótulo)
DEDUPE = {
    "ANEL DE GUARDANAPO": "ANEL DE GUARDANAPO", "ESFERA FURADA": "= ESFERA FURADA", "QUAL TEM MAIS VOLUME?": "QUAL TEM MAIS VOLUME?",
    "MESMA ALTURA": "MESMA ALTURA: h = 6 cm", "RAIO DA ESFERA": "O RAIO DA ESFERA SUMIU",
    "MESMA ÁREA EM TODA ALTURA": "MESMA ÁREA EM TODA ALTURA", "LOGO, ": "LOGO, MESMO VOLUME",
    "DUAS ROTAS": "DUAS ROTAS, O MESMO VOLUME", "MUDA A FORMA": "MUDA A FORMA. NÃO MUDA O VOLUME.",
    "NÃO É QUALQUER FURO": "proteção (frase completa)", "DESDE QUE": "DESDE QUE h SEJA A MESMA (deve sumir)",
    "DETERMINA O VOLUME": "SÓ A ALTURA DETERMINA O VOLUME",
}


def base(g):
    g = g.rstrip("*")
    for suf in ("_chamada", "_rot", "_risco", "_destaque"):
        if g.endswith(suf):
            g = g[: -len(suf)]
    return g


def beat(t):
    return next(b["id"] for b in TL["beats"] if b["inicio_s"] - 1e-6 <= t < b["fim_s"] + 1e-6)


def trecho(t):
    return next(z for z in TL["zonas"]["trechos"] if z["de"] - 1e-6 <= t < z["ate"] + 1e-6)


# ---------- caixas por quadro ----------
cm = json.loads((UNIT / "media_preview" / "caixas_CenaMat.json").read_text(encoding="utf-8"))["quadros"]
caixas = defaultdict(list)            # quadro → [(camada, grupo, x0, y0, x1, y1, op, texto)]
VEL = {}                              # (quadro, índice) → deslocamento do glifo (px) desde o quadro anterior
for f, lst in cm.items():
    for g, x0, y0, x1, y1, op, *v in lst:
        caixas[int(f)].append(("manim", g, x0, y0, x1, y1, op, ""))
        VEL[(int(f), len(caixas[int(f)]) - 1)] = tuple(v) if v else (0.0, 0.0)
log = (UNIT / "remotion" / "render_remotion_v5.log").read_text(encoding="utf-8", errors="replace")
vistos = set()
for m in re.finditer(r"QA\|(\d+)\|(\[.*?\])(?:\x1b|\s*$)", log, re.M):
    f = int(m.group(1))
    if f in vistos:
        continue
    vistos.add(f)
    for g, x0, y0, x1, y1, op, txt in json.loads(m.group(2)):
        caixas[f].append(("remotion", g, x0, y0, x1, y1, op, txt))
faltam = [f for f in range(N) if f not in vistos]


def inter(a, b):
    w, h = min(a[2], b[2]) - max(a[0], b[0]), min(a[3], b[3]) - max(a[1], b[1])
    return max(0.0, w) * max(0.0, h)


def iou(a, b):
    i = inter(a, b)
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i
    return i / ua if ua > 0 else 0.0


DISCO = np.ones((25, 25), bool)
DISCO[np.hypot(*np.mgrid[-12:13, -12:13]) > 12] = False
res = {"caixa_caixa": defaultdict(list), "texto_3d": defaultdict(list), "folga_12px": defaultdict(list),
       "margem": defaultdict(list), "zona_3d": defaultdict(list)}
opac = defaultdict(dict)              # grupo → {quadro: menor opacidade}
textos = defaultdict(set)             # mensagem → quadros
for f in range(N):
    t, bt = f / FPS, beat(f / FPS)
    todas = caixas.get(f, [])
    vel = {id(c): VEL.get((f, i), (0.0, 0.0)) for i, c in enumerate(todas)}
    cx = [c for c in todas if c[6] > 0.02 and c[4] > c[2] and c[5] > c[3]]
    # cópia sem nome exatamente em cima de um glifo nomeado (Indicate/ReplacementTransform deixam o glifo duas vezes
    # na cena): é o mesmo desenho, não sobreposição
    fixos = [c for c in cx if not (c[1] == "transito" or c[1].endswith("*"))]
    soltos = []
    for c in cx:
        if not (c[1] == "transito" or c[1].endswith("*")) or any(iou(c[2:6], d[2:6]) > 0.9 for d in fixos):
            continue
        # glifo sem nome inteiro dentro da caixa de uma fórmula (caixa-chave, memo): é a própria fórmula
        dono = next((d for d in fixos if d[0] == "manim" and d[2] <= c[2] and d[3] <= c[3] and c[4] <= d[4] and c[5] <= d[5]
                     and (d[4] - d[2]) * (d[5] - d[3]) > 6 * (c[4] - c[2]) * (c[5] - c[3])), None)
        soltos.append(c if dono is None else (c[0], dono[1], *c[2:]))
    cx = fixos + soltos
    # 1 · caixa × caixa
    pares = set()
    for i in range(len(cx)):
        for j in range(i + 1, len(cx)):
            a, b = cx[i], cx[j]
            if base(a[1]) == base(b[1]):
                if any(x[1].rstrip("*").endswith(("_risco", "_destaque")) for x in (a, b)):
                    continue                     # risco de cancelamento / moldura de destaque: passar por cima é o gesto
                # v5 · trânsito dentro da MESMA linha: glifo que se move em relação ao vizinho e o cobre (> 15 % da
                # menor caixa) é cruzamento (o a² passando sobre o "=", cópia sobre a origem, termo atravessando ")")
                va, vb = vel.get(id(a), (0, 0)), vel.get(id(b), (0, 0))
                if a[0] == b[0] == "manim" and np.hypot(va[0] - vb[0], va[1] - vb[1]) > 1.0:
                    A_, B_ = a[2:6], b[2:6]
                    Ap = (A_[0] - va[0], A_[1] - va[1], A_[2] - va[0], A_[3] - va[1])
                    Bp = (B_[0] - vb[0], B_[1] - vb[1], B_[2] - vb[0], B_[3] - vb[1])
                    menor = min((A_[2] - A_[0]) * (A_[3] - A_[1]), (B_[2] - B_[0]) * (B_[3] - B_[1]))
                    if (menor > 0 and inter(A_, B_) > 0.15 * menor and inter(A_, B_) > inter(Ap, Bp) + 1
                            and iou(A_, B_) < 0.9):
                        pares.add((base(a[1]) + " (trânsito)", base(b[1])))
                continue
            A, B = a[2:6], b[2:6]
            if inter(A, B) <= 0:
                continue
            trans = [(x, y) for x, y in ((a, b), (b, a)) if x[1].endswith("*")]
            if trans and (iou(A, B) > 0.6 or any(base(y[1]) in ORIGENS.get(base(x[1]), ()) for x, y in trans)):
                continue
            pares.add(tuple(sorted((base(a[1]), base(b[1])))))
    for p in pares:
        res["caixa_caixa"][bt].append([round(t, 2), *p])
    # 2/3/4/5 · máscara do 3D
    mk = np.asarray(Image.open(UNIT / "mask3d_540x960" / f"f{f:05d}.png").convert("RGB"))
    sol, aux, pla = mk[..., 0] > 127, mk[..., 1] > 127, mk[..., 2] > 127
    obj = sol | aux
    dil = binary_dilation(sol, structure=DISCO) if any(c[1].startswith(ROTULOS_3D) for c in cx) else None
    for cam, g, x0, y0, x1, y1, op, txt in cx:
        X0, Y0, X1, Y1 = max(0, int(np.ceil(x0))), max(0, int(np.ceil(y0))), min(W, int(x1)), min(H, int(y1))
        if g.endswith("_chamada") or g in ("cabecalho", "end"):
            pass
        elif X1 > X0 and Y1 > Y0 and not g.startswith(ISENTO_3D):
            k = int(obj[Y0:Y1, X0:X1].sum() + pla[Y0:Y1, X0:X1].sum())
            if k:
                res["texto_3d"][bt].append([round(t, 2), base(g), k])
        rot = g.startswith(ROTULOS_3D) and not g.endswith("_chamada") and (not g.startswith("regua") or g.endswith("_rot"))
        if rot and dil is not None and X1 > X0 and Y1 > Y0:
            k = int(dil[Y0:Y1, X0:X1].sum())
            if k:
                res["folga_12px"][bt].append([round(t, 2), base(g), k])
        if g != "cabecalho" and (x0 < XS[0] - 0.5 or x1 > XS[1] + 0.5):
            res["margem"][bt].append([round(t, 2), base(g), round(x0, 1), round(x1, 1)])
        if not g.endswith("_chamada") and not g.startswith(("regua",)) and g not in ("cabecalho_img",):
            # Manim: opacidade da linha = mediana dos glifos (glifos que nascem/somem num glyph map são minoria);
            # Remotion: cada elemento (grupo + texto) tem a sua série
            chave_op = base(g) if cam == "manim" else f"{base(g)} · {re.sub(r'[-+0-9,]', '', txt)}"
            if cam == "manim" or txt:                    # imagens (marca d'água) ficam fora
                opac[chave_op].setdefault(f, []).append(op)
        for chave in DEDUPE:
            if chave in txt:
                textos[chave].add(f)
    cols = np.where((sol | aux | pla).any(axis=0))[0]
    if cols.size and (cols[0] < XS[0] or cols[-1] >= XS[1]):
        res["margem"][bt].append([round(t, 2), "3D", int(cols[0]), int(cols[-1])])
    z3 = trecho(t)["zona_3d"]
    rows = np.where(obj.any(axis=1))[0]
    if rows.size and (rows[0] < z3[0] or rows[-1] > z3[1]):
        res["zona_3d"][bt].append([round(t, 2), int(rows[0]), int(rows[-1]), z3])

# 6 · opacidade: rampas monotônicas a partir de / até 0 são entradas e saídas; o resto é "estável"
estavel, rampas = {}, {}
# opacidade da linha/elemento = a do glifo mais opaco (glifos que nascem/somem num glyph map não rebaixam a linha;
# uma linha recuada tem todos os glifos no mesmo valor)
opac = {g: {f: float(max(v)) for f, v in serie.items()} for g, serie in opac.items()}
for g, serie in opac.items():
    fs_ = sorted(serie)
    blocos, atual = [], [fs_[0]]
    for f in fs_[1:]:
        if f == atual[-1] + 1:
            atual.append(f)
        else:
            blocos.append(atual)
            atual = [f]
    blocos.append(atual)
    mins, rmax = [], 0
    for bl in blocos:
        v = [serie[f] for f in bl]
        top = max(v)
        i0 = next((i for i, x in enumerate(v) if x >= min(0.75, top) - 1e-3), len(v))
        i1 = len(v) - 1 - next((i for i, x in enumerate(reversed(v)) if x >= min(0.75, top) - 1e-3), len(v))
        rmax = max(rmax, i0, len(v) - 1 - i1)
        meio = v[i0:i1 + 1]
        if meio:
            mins.append(min(meio))
    estavel[g] = round(min(mins), 3) if mins else None
    rampas[g] = round(rmax / FPS, 2)


def intervalos(qs):
    qs = sorted(qs)
    if not qs:
        return []
    out, a = [], qs[0]
    for x, y in zip(qs, qs[1:]):
        if y > x + 1:
            out.append([round(a / FPS, 2), round(x / FPS, 2)])
            a = y
    out.append([round(a / FPS, 2), round(qs[-1] / FPS, 2)])
    return out


def resumo(d):
    return {b: {"quadros": len({x[0] for x in d.get(b, [])}), "exemplos": d.get(b, [])[:6], "intervalos": intervalos([round(x[0] * FPS) for x in d.get(b, [])])} for b in
            [b["id"] for b in TL["beats"]]}


saida = {
    "quadros_avaliados": N, "quadros_sem_log_remotion": len(faltam),
    "sobreposicao_caixa_caixa": resumo(res["caixa_caixa"]),
    "sobreposicao_texto_3d": resumo(res["texto_3d"]),
    "folga_rotulos_12px": resumo(res["folga_12px"]),
    "margem_24px": resumo(res["margem"]),
    "zona_3d": resumo(res["zona_3d"]),
    "opacidade_estavel_min": {g: v for g, v in sorted(estavel.items(), key=lambda kv: (kv[1] is None, kv[1]))},
    "opacidade_menor_geral": min(v for v in estavel.values() if v is not None),
    "rampa_mais_longa_s": rampas,
    "dedupe": {DEDUPE[k]: intervalos(textos[k]) for k in DEDUPE},
    "totais": {k: len({x[0] for v in d.values() for x in v}) for k, d in res.items()},
}
SAIDA.write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"totais": saida["totais"], "opacidade_menor_geral": saida["opacidade_menor_geral"],
                  "sem_log": len(faltam), "dedupe": saida["dedupe"]}, ensure_ascii=False, indent=1))
for k in ("sobreposicao_caixa_caixa", "sobreposicao_texto_3d", "folga_rotulos_12px", "margem_24px", "zona_3d"):
    print(k, {b: v["quadros"] for b, v in saida[k].items() if v["quadros"]})
