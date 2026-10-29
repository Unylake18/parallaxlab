"""yt_0015 — ritmo da sincronia fina: sync/rec_<Lote>.json (passe SYNC=1 SYNC_REC=1) + sync/mapa.json -> sync/ritmo.json, sync/pre.json.

Trecho k de um lote = conteúdo da cena entre o ponto de sincronia k−1 e o ponto k (P = quadros de plays, W = quadros de esperas).
O ponto k é uma palavra da voz (`an(aid)` = 1ª palavra da âncora; `ate(f)` = a palavra f·n). Cada trecho recebe fp (plays) e fw
(esperas) para chegar no ponto k no quadro da palavra (padrão dos longos, yt_0014), sem inserir silêncio na voz:
- sobra tempo: os plays esticam até SMAX (sem esperas no trecho, até SMAX_SO); o resto vira espera da voz, em que o que acabou de
  entrar "respira" (kit._encher), em vez de esticar as esperas paradas;
- falta tempo: as esperas encolhem até FWMIN, depois os plays até FPMIN; se ainda faltar, o atraso passa para o trecho seguinte e
  é relatado (regra do Kaio: atraso áudio–quadro ≤ 0,2 s = 3 quadros).
pre.json: quadros de header que cada lote toca antes da 1ª âncora; o lote anterior termina esse tanto antes (montagem sem folga).
Uso: uv run --no-sync python ritmo.py
"""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FPS = 15                         # o passe de gravação é feito no preview; fp/fw são razões (valem a 30 fps)
SMAX, SMAX_SO, FPMIN, FWMIN, FOLGA = 1.6, 2.2, 0.30, 0.15, 1
LOTES = ["PA", "PT1", "PB", "PT3", "PC", "PD", "PE", "PF", "PG", "PS"]
MAPA = json.loads((AQUI / "sync" / "mapa.json").read_text(encoding="utf-8"))
ORD = MAPA["ordem"]


def tg(aid, f):
    m = MAPA["ancoras"][aid]
    if f <= 0:
        return m["S"]
    if str(f) in m.get("ovr", {}):
        return max(m["S"], m["ovr"][str(f)] - MAPA["lead"])
    arr = m["t5"] if m["v5"] else m["t4"]
    pos = min(1.0, f) * (len(arr) - 1)
    i = int(pos)
    t = arr[i] if i + 1 >= len(arr) else arr[i] + (pos - i) * (arr[i + 1] - arr[i])
    return max(m["S"], t - MAPA["lead"])


rec = {c: json.loads((AQUI / "sync" / f"rec_{c}.json").read_text(encoding="utf-8")) for c in LOTES}
pre = {r["pontos"][0]["aid"]: round(MAPA["ancoras"][r["pontos"][0]["aid"]]["S"] * FPS) - r["F0"] for r in rec.values()}
(AQUI / "sync" / "pre.json").write_text(json.dumps(pre), encoding="utf-8")

ritmo, tot_atraso, avisos, parados = {}, [], [], []
for c in LOTES:
    r = rec[c]
    F0, pts = r["F0"], r["pontos"]
    loc = lambda t: round(t * FPS) - F0
    ult = pts[-1]["aid"]
    i = ORD.index(ult)
    nxt = ORD[i + 1] if i + 1 < len(ORD) else None
    fim = (loc(MAPA["ancoras"][nxt]["S"] - pre.get(nxt, 0) / FPS) if nxt else loc(MAPA["fim"])) - 5
    alvos = [loc(tg(p["aid"], p["f"])) for p in pts] + [fim]
    PW = [(p["P"], p["W"]) for p in pts[1:]] + [(r["fim_P"], r["fim_W"]) if "fim_P" in r else (0, 0)]
    # o 1º trecho (header antes da 1ª âncora) não é escalado: a chegada no ponto 0 é a do passe de gravação
    cheg = pts[0]["chegada"]
    t_ant = max(cheg, alvos[0])
    if cheg > alvos[0]:
        avisos.append((c, pts[0]["aid"], 0.0, round((cheg - alvos[0]) / FPS, 3)))
    rl = {}
    for k in range(1, len(alvos)):
        P, W = PW[k - 1]
        A = alvos[k] - t_ant - FOLGA
        D = P + W
        if A >= D:
            extra = A - D
            fp = min(1 + extra / P, SMAX if W > 0 else SMAX_SO) if P > 0 else 1.0
            fw = 1.0
        else:
            falta = D - A
            if W * (1 - FWMIN) >= falta:
                fp, fw = 1.0, 1 - falta / W
            else:
                fw = FWMIN if W > 0 else 1.0
                falta -= W * (1 - FWMIN)
                fp = max(FPMIN, 1 - falta / P) if P > 0 else 1.0
        dur = P * fp + W * fw
        cheg = t_ant + dur
        atraso = max(0.0, cheg - alvos[k])
        if atraso > 0.5:
            p = pts[k] if k < len(pts) else {"aid": "FIM", "f": 1}
            avisos.append((c, p["aid"], p["f"], round(atraso / FPS, 3)))
        espera = alvos[k] - cheg
        if espera > 6 * FPS:
            p = pts[k] if k < len(pts) else {"aid": "FIM", "f": 1}
            parados.append((c, p["aid"], p["f"], round(espera / FPS, 1)))
        rl[str(k)] = [round(fp, 4), round(fw, 4)]
        t_ant = max(cheg, alvos[k])
    ritmo[c] = rl
    tot_atraso.append((c, len(pts), F0, fim + 5))
(AQUI / "sync" / "ritmo.json").write_text(json.dumps(ritmo, indent=0), encoding="utf-8")
print("lote  pontos  F0(global)  fim(local)")
for x in tot_atraso:
    print(f"{x[0]:5s} {x[1]:6d} {x[2]:10d} {x[3]:10d}")
print("pre:", pre)
print(f"atrasos previstos > 0,5 quadro: {len(avisos)}")
for a in avisos:
    print("  ", a)
print(f"esperas da voz > 6 s (o objeto recém-entrado respira): {len(parados)}")
for a in parados:
    print("  ", a)
