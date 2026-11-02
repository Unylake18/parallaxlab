"""yt_0019 v9: CONGELAMENTO — nenhum trecho com a tela parada por mais de 1,5 s enquanto há fala (handoff v9 §2.3 e §5).

1. Tela inteira (freezedetect do ffmpeg, n = 0,0005, d = 1,5 s): diferença absoluta média (luma, 960×540) entre quadros vizinhos, normalizada em [0, 1];
   parado = diferença < n. Conta o trecho parado que dura >= 1,5 s dentro da fala (do começo da primeira palavra ao fim da última).
2. Objetos 3D (a água não conta como movimento): no lago (gafanhoto e folha), o estado enviado ao renderizador (pedidos3d/<LOTE>.json) sem os campos da água
   (tw, aneis, gotas) é comparado quadro a quadro; o gafanhoto NO AR e a câmera parados >= 1,5 s = congelado (no repouso o gafanhoto respira: antenas e abdome no Three.js).
uso: python congelamento.py [video] [--lista]"""
import json
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
VID = Path(args[0]) if args else U / "renders" / "preview_yt0019_v9_960x540.mp4"
FPS, N_, D_ = 15, 0.0005, 1.5
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
T = json.loads((U / "audio" / "voz9_tempos.json").read_text(encoding="utf-8"))["ancoras"]
FALA0 = min(v[0]["t"] for v in T.values())
FALA1 = max(v[-1]["e"] for v in T.values())
import os
if os.environ.get("FALA"):                                        # linha de base (v6): FALA=ini,fim
    FALA0, FALA1 = (float(x) for x in os.environ["FALA"].split(","))
PRIMEIRA = {"PH": "H1", "PX0": "X0-1", "PX2": "X2-1", "PX3": "X3-1", "PX4": "X4-1", "PX5": "X5-1", "PEP": "EP1"}


def corridas(mask, dmin):
    runs, ini = [], None
    for k, m in enumerate(list(mask) + [False]):
        if m and ini is None:
            ini = k
        if not m and ini is not None:
            if (k - ini) / FPS >= dmin:
                runs.append((ini / FPS, (k - ini) / FPS))
            ini = None
    return runs


def na_fala(runs):
    out = []
    for t, d in runs:
        a, b = max(t, FALA0), min(t + d, FALA1)
        if b - a >= D_:
            out.append((round(a, 1), round(b - a, 1)))
    return out


def tela():
    c = av.open(str(VID))
    ant, mafd = None, []
    for fr in c.decode(video=0):
        g = fr.to_ndarray(format="gray").astype(np.int16)
        if ant is not None:
            mafd.append(float(np.abs(g - ant).mean()) / 255.0)
        ant = g
    c.close()
    mafd = np.array(mafd)
    # mafd[i] compara o quadro i+1 com o i; o quadro i+1 está parado se mafd[i] < n
    parado = np.concatenate([[False], mafd < N_])
    return corridas(parado, D_), len(parado)


def objetos3d():
    saida = []
    for lote, aid in PRIMEIRA.items():
        f = U / "threejs" / "pedidos3d" / f"{lote}.json"
        if not f.exists():
            continue
        ini = ANC["ancoras"][aid]["ini"]
        cenas = json.loads(f.read_text(encoding="utf-8"))["cenas"]
        for nome, quadros in cenas.items():
            ant, mask, vis = None, [], []
            if nome != "lago":                      # cubo, foguete, granada: sem água, a diferença de quadro da tela inteira já pega
                continue
            for q, e in quadros:
                e = {k: v for k, v in e.items() if k not in ("tw", "aneis", "gotas", "esteira")}
                if isinstance(e.get("f"), dict):
                    e["f"] = {k: v for k, v in e["f"].items() if k != "bal"}      # a folha balança com a água (ambiente)
                s = json.dumps(e, sort_keys=True)
                no_ar = float(e.get("g", {}).get("z", 0.0)) > 0.003                # parado na folha o gafanhoto respira (antenas e abdome, no JS): só conta no ar
                mask.append(ant == s and no_ar)
                ant = s
            runs = corridas(mask, D_)
            for t, d in runs:
                a = ini + t
                saida.append((lote, nome, round(a, 1), round(d, 1)))
    return [s for s in saida if FALA0 <= s[2] <= FALA1]


if __name__ == "__main__":
    runs, n = tela()
    fala = na_fala(runs)
    print(f"tela inteira: {len(runs)} trechos parados >= {D_} s no vídeo todo; {len(fala)} com fala ativa" + (f": {fala[:40]}" if fala else ""))
    soma = sum(d for _, d in fala)
    print(f"  tempo parado com fala: {soma:.1f} s de {(FALA1 - FALA0):.0f} s ({100 * soma / (FALA1 - FALA0):.1f}%); maior {max([d for _, d in fala], default=0):.1f} s")
    ob = objetos3d()
    print(f"objetos 3D (sem a água): {len(ob)} trechos com o estado 3D parado >= {D_} s" + (f": {ob[:30]}" if ob else ""))
    ok = not fala and not ob
    print("  → " + ("OK" if ok else "FALHA"))
    if "--lista" in sys.argv:
        for t, d in fala:
            print(f"  parado {t:.1f} s ({d:.1f} s)")
