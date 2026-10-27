"""Ajusta o ritmo da cena à voz real: (1) por bloco, acelera/desacelera as animações (rs_v3_1.json);
(2) o excesso que sobrar vira pausa no áudio (pads_v3_1.json). Cada passo roda a cena em modo -s (só tempo, sem vídeo).

  uv run --no-sync python ajustar_ritmo_v3_1.py
"""
import json
import os
import subprocess
import sys
from pathlib import Path

P = Path(__file__).resolve().parent
RAIZ = P.parents[1]
RS0 = 1.3


def medir():
    env = dict(os.environ, TRECHO="", UV_CACHE_DIR=str(P / "renders" / "uv_cache"), QA_LAYOUT="0")
    subprocess.run(["uv", "run", "--no-sync", "python", "-m", "manim", "-s", "-r", "960,540", "--media_dir", str(P / "renders" / "m_dry"),
                    str(P / "cena.py"), "DivergenteRotacional"], cwd=RAIZ, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return {b["id"]: b for b in json.loads((P / "renders" / "blocos_v3_1_completo.json").read_text(encoding="utf-8"))}


def main():
    rs_f, pads_f = P / "rs_v3_1.json", P / "pads_v3_1.json"
    rs = json.loads(rs_f.read_text(encoding="utf-8")) if rs_f.exists() else {}
    for it in range(1, 5):
        b = medir()
        exc = {i: x for i, x in b.items() if x["excesso_s"] > .05}
        print(f"passo {it}: {len(exc)} blocos com excesso; soma {sum(x['excesso_s'] for x in exc.values()):.1f} s")
        if not exc:
            break
        for i, x in exc.items():
            atual = rs.get(i, RS0)
            rs[i] = round(max(.45, atual * x["voz_s"] / x["animacao_s"] * .97), 3)
        rs_f.write_text(json.dumps(rs, indent=1), encoding="utf-8")
    b = medir()
    exc = {i: x["excesso_s"] for i, x in b.items() if x["excesso_s"] > .05}
    print("excesso residual (vira pausa no áudio):", exc)
    pads = {i: round(v + .15, 2) for i, v in exc.items()}
    pads_f.write_text(json.dumps(pads, indent=1), encoding="utf-8")
    subprocess.run([sys.executable, "-c", "pass"])
    subprocess.run(["uv", "run", "--no-sync", "python", str(P / "gerar_sync_v3_1.py"), "montar"], cwd=RAIZ, check=True)
    b = medir()
    exc = {i: x["excesso_s"] for i, x in b.items() if x["excesso_s"] > .05}
    atr = {i: x["atraso_inicio_s"] for i, x in b.items() if x["atraso_inicio_s"] > .2}
    print("após pads: excesso", exc, "| atrasos de início >0,2 s", atr)


main()
