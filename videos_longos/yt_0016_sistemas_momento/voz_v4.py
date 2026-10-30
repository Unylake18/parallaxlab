"""Voz do yt_0016 (handoff v5 §2): narracao_tags.md → audio/narracao_v4.wav, um bloco por arquivo (para regenerar só o bloco ruim).

Blocos de até 4.500 caracteres fechados em fim de parágrafo (âncora); um bloco que começa sem tag herda a última tag vista.
Cada bloco fica em audio/blocos_v4/bNN.mp3 (+ .txt). As emendas levam 10 ms de fade e 0,25 s de silêncio (sem clique).
Uso: uv run --no-sync python voz_v4.py [--seco] [--refazer N ...]    (chave só em ELEVENLABS_API_KEY; nunca em arquivo)
"""
import argparse
import importlib.util
import json
import os
import re
import sys
import wave
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
spec = importlib.util.spec_from_file_location("gv", RAIZ / "videos" / "gerar_voz_elevenlabs.py")
gv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gv)

VOZ, MODELO, FMT, SR = "qw7jgPZWOKrl10GsjQ82", "eleven_v4", "mp3_44100_192", 44100
PASTA = AQUI / "audio" / "blocos_v4"
SAIDA = AQUI / "audio" / "narracao_v4.wav"


def montar_blocos(limite=4500):
    texto = gv.extrair((AQUI / "narracao_tags.md").read_text(encoding="utf-8"), "## Texto corrido (para gravação)")
    pars = [" ".join(p.split()) for p in re.split(r"\n\s*\n", texto) if p.strip()]
    blocos, atual, tag = [], [], None
    for p in pars:
        if atual and len(" ".join(atual)) + 2 + len(p) > limite:
            blocos.append(atual)
            atual = []
        if not atual and not p.startswith("[") and tag:
            p = f"{tag} {p}"
        atual.append(p)
        m = re.findall(r"\[[^\]]+\]", p)
        if m:
            tag = m[-1]
    blocos.append(atual)
    return ["\n\n".join(b) for b in blocos]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seco", action="store_true")
    ap.add_argument("--refazer", type=int, nargs="*", default=[])
    a = ap.parse_args()
    blocos = montar_blocos()
    print(len(blocos), "blocos:", [len(b) for b in blocos], "caracteres; total", sum(len(b) for b in blocos))
    if a.seco:
        for i, b in enumerate(blocos, 1):
            print(f"\n--- bloco {i} ({len(b)}) ---\n{b[:160]} ... {b[-80:]}")
        return
    chave = os.environ.get("ELEVENLABS_API_KEY")
    if not chave:
        sys.exit("ELEVENLABS_API_KEY ausente: pare e peça ao Kaio.")
    PASTA.mkdir(parents=True, exist_ok=True)
    for i, b in enumerate(blocos, 1):
        mp3 = PASTA / f"b{i:02d}.mp3"
        (PASTA / f"b{i:02d}.txt").write_text(b, encoding="utf-8")
        if mp3.exists() and i not in a.refazer:
            continue
        if mp3.exists():
            mp3.rename(PASTA / f"b{i:02d}_antigo{len(list(PASTA.glob(f'b{i:02d}_antigo*')))}.mp3")
        print(f"bloco {i}/{len(blocos)} ({len(b)} caracteres) ...", flush=True)
        mp3.write_bytes(gv.sintetizar(chave, VOZ, MODELO, FMT, b, "", "", None))
    if SAIDA.exists() and not a.refazer:
        sys.exit(f"{SAIDA.name} já existe: não sobrescrevo (use --refazer para remontar).")
    fade, gap = int(0.010 * SR), np.zeros(int(0.25 * SR), np.float32)
    partes, info = [], []
    for i in range(1, len(blocos) + 1):
        x = np.frombuffer(gv.decodificar_mp3((PASTA / f"b{i:02d}.mp3").read_bytes()), np.int16).astype(np.float32)
        x[:fade] *= np.linspace(0, 1, fade)
        x[-fade:] *= np.linspace(1, 0, fade)
        if partes:
            partes.append(gap)
        ini = sum(len(p) for p in partes) / SR
        partes.append(x)
        info.append({"bloco": i, "inicio": round(ini, 3), "dur": round(len(x) / SR, 3), "chars": len(blocos[i - 1])})
    y = np.concatenate(partes)
    pico = np.abs(y).max() / 32768
    alvo = 10 ** (-1.0 / 20)
    if pico > alvo:
        y *= alvo / pico
    with wave.open(str(SAIDA), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.clip(y, -32768, 32767).astype(np.int16).tobytes())
    (AQUI / "audio" / "blocos_v4.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    print(f"{SAIDA.name}: {len(y) / SR:.1f} s; pico original {20 * np.log10(pico):.2f} dBFS; blocos {info}")


if __name__ == "__main__":
    main()
