"""yt_0002 — render final (1920×1080, 30 fps, crf 14) em grupos paralelos de blocos, junção sem recompressão e narração de montagem.

Pré-requisitos (já feitos nesta pasta; ver LEIA-ME_RENDER_FINAL.md): sync.json, ritmo.json, pads.json, blocos.json,
audio/narracao_montagem.wav e legenda.srt consistentes entre si. Este script NÃO refaz o áudio nem a legenda.

    uv run --no-sync python videos_longos/yt_0002_lei_gauss_casos_classicos/render_final.py            # 6 grupos em paralelo
    uv run --no-sync python videos_longos/yt_0002_lei_gauss_casos_classicos/render_final.py --grupos 4
    uv run --no-sync python videos_longos/yt_0002_lei_gauss_casos_classicos/render_final.py --so 8,9    # só estes blocos (teste)
    uv run --no-sync python videos_longos/yt_0002_lei_gauss_casos_classicos/render_final.py --montar-apenas  # reaproveita os trechos já renderizados

Saída: renders/yt_0002_final/master_yt0002.mp4 (vídeo + voz). Trechos em renders/yt_0002_final/gN/.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
SAIDA = RAIZ / "renders" / "yt_0002_final"
CENA = PASTA / "cena.py"
CLASSE = "LeiGaussCasosClassicos002"
FPS = 30


def grupos(n):
    """Divide os blocos (em ordem) em n grupos contíguos de duração parecida, pelos tempos de blocos.json."""
    b = json.loads((PASTA / "blocos.json").read_text(encoding="utf-8"))
    fim = b.pop("fim")
    ks = sorted(int(k) for k in b)
    inicio = {int(k): v for k, v in b.items()}
    dur = {k: (inicio[ks[i + 1]] if i + 1 < len(ks) else fim) - inicio[k] for i, k in enumerate(ks)}
    alvo, gs, atual, acc = sum(dur.values()) / n, [], [], 0.0
    for k in ks:
        atual.append(k)
        acc += dur[k]
        if acc >= alvo and len(gs) < n - 1:
            gs.append(atual)
            atual, acc = [], 0.0
    if atual:
        gs.append(atual)
    return gs, dur


def trecho(i):
    return SAIDA / f"g{i}" / "videos" / "cena" / "1080p30" / f"{CLASSE}.mp4"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grupos", type=int, default=6)
    ap.add_argument("--so", default="", help="blocos separados por vírgula (teste); o resultado não é montado com a voz")
    ap.add_argument("--montar-apenas", action="store_true")
    ap.add_argument("--paralelo", type=int, default=3, help="processos simultâneos (cada um segura a cena inteira em memória; 6 em 1080p estouraram a RAM)")
    ap.add_argument("--apenas", default="", help="índices dos grupos a (re)renderizar, p. ex. 0,2,3,4; os demais mantêm o trecho já pronto")
    a = ap.parse_args()
    SAIDA.mkdir(parents=True, exist_ok=True)
    if a.so:
        gs, dur = [[int(x) for x in a.so.split(",")]], None
    else:
        gs, dur = grupos(a.grupos)
    for i, g in enumerate(gs):
        print(f"grupo {i}: blocos {g}" + (f" ({sum(dur[k] for k in g):.0f} s de vídeo)" if dur else ""))
    if not a.montar_apenas:
        import os
        import time
        fila = [int(x) for x in a.apenas.split(",")] if a.apenas else list(range(len(gs)))
        ativos, falhas = [], []
        while fila or ativos:
            while fila and len(ativos) < a.paralelo:
                i = fila.pop(0)
                env = {**os.environ, "CRF": "14", "SO": ",".join(map(str, gs[i]))}
                cmd = ["uv", "run", "--no-sync", "python", "-m", "manim", "-r", "1920,1080", "--fps", str(FPS), "--disable_caching",
                       "--media_dir", str(SAIDA / f"g{i}"), str(CENA), CLASSE]
                log = open(SAIDA / f"g{i}.log", "w", encoding="utf-8")
                ativos.append((i, subprocess.Popen(cmd, cwd=RAIZ, env=env, stdout=log, stderr=subprocess.STDOUT), log))
                print(f"grupo {i}: iniciado", flush=True)
            for item in list(ativos):
                i, p, log = item
                rc = p.poll()
                if rc is not None:
                    log.close()
                    ativos.remove(item)
                    print(f"grupo {i}: código {rc}", flush=True)
                    if rc != 0:
                        falhas.append(i)
            time.sleep(5)
        if falhas:
            sys.exit(f"falhou nos grupos {falhas}; veja {SAIDA}/gN.log")
    if a.so:
        print(f"trecho de teste: {trecho(0)}")
        return
    destino = SAIDA / "master_yt0002.mp4"
    cmd = ["uv", "run", "--no-sync", "python", str(PASTA / "montar_final.py"), str(destino), *[str(trecho(i)) for i in range(len(gs))]]
    subprocess.run(cmd, cwd=RAIZ, check=True)
    esperado = json.loads((PASTA / "blocos.json").read_text(encoding="utf-8"))["fim"]
    print(f"duração esperada do vídeo (blocos.json): {esperado:.2f} s")


if __name__ == "__main__":
    main()
