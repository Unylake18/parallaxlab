"""yt_0030 · voz v3.4, PASSO 1 de 2: gera só os trechos novos (HANDOFF v4 §4.2). Um WAV por trecho em audio/v34/<trecho>.wav.
Usa as MESMAS funções do videos/gerar_voz_elevenlabs.py (que não muda): voz qw7jgPZWOKrl10GsjQ82, eleven_v4, mp3_44100_192 → WAV mono 16 bits.
Contexto: manda previous_text/next_text com o parágrafo vizinho da v3.3 (que fica no WAV) para a entonação casar na emenda;
se a API recusar o contexto, repete sem ele e anota no log. A chave vem de ELEVENLABS_API_KEY (nunca gravar em arquivo, log ou relatório).

uso (na raiz do repositório):
    uv run --no-sync python videos_longos/yt_0030_exercicios_modulo_31/gerar_trechos_v34.py --seco          # só lista os trechos
    uv run --no-sync python videos_longos/yt_0030_exercicios_modulo_31/gerar_trechos_v34.py                 # gera os 11 que faltam
    uv run --no-sync python videos_longos/yt_0030_exercicios_modulo_31/gerar_trechos_v34.py --so T05 --take 2   # refaz um trecho (novo take)
"""
import argparse
import json
import os
import re
import sys
import wave
from pathlib import Path

U = Path(__file__).resolve().parent
sys.path.insert(0, str(U.parents[1] / "videos"))
from gerar_voz_elevenlabs import blocos, decodificar_mp3, extrair, sintetizar  # noqa: E402

VOZ, MODELO, FMT = "qw7jgPZWOKrl10GsjQ82", "eleven_v4", "mp3_44100_192"
SEC = "## Texto corrido (para gravação)"
DIR_T, DIR_A = U / "trechos_v34", U / "audio" / "v34"
limpa = lambda s: " ".join(re.sub(r"\[[^\]]*\]", " ", s).split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seco", action="store_true")
    ap.add_argument("--so", nargs="*", help="prefixos dos trechos (ex.: T01 T05)")
    ap.add_argument("--take", type=int, default=1)
    ap.add_argument("--sem-contexto", action="store_true")
    a = ap.parse_args()
    plano = json.loads((DIR_T / "plano_trechos.json").read_text(encoding="utf-8"))
    DIR_A.mkdir(parents=True, exist_ok=True)
    chave = os.environ.get("ELEVENLABS_API_KEY")
    if not a.seco and not chave:
        sys.exit("Defina ELEVENLABS_API_KEY no ambiente (não grave a chave em arquivo).")
    log = []
    for p in plano:
        nome = p["trecho"]
        if a.so and not any(nome.startswith(s) for s in a.so):
            continue
        saida = DIR_A / (nome + ("" if a.take == 1 else f"_take{a.take}") + ".wav")
        if saida.exists() and not a.so:
            print(f"{nome}: já existe ({saida.name}), pulando")
            continue
        partes = blocos(extrair((DIR_T / f"{nome}.md").read_text(encoding="utf-8"), SEC), 4500)
        print(f"{nome}: {len(partes)} bloco(s) {[len(b) for b in partes]} · âncoras {p['ancoras']}")
        if a.seco:
            continue
        pcm, ctx_ok = b"", not a.sem_contexto
        for i, b in enumerate(partes):
            antes = limpa(p["contexto_antes"]) if i == 0 else partes[i - 1]
            depois = limpa(p["contexto_depois"]) if i == len(partes) - 1 else partes[i + 1]
            try:
                dados = sintetizar(chave, VOZ, MODELO, FMT, b, antes if ctx_ok else "", depois if ctx_ok else "", None)
            except SystemExit as e:
                if ctx_ok and ("previous_text" in str(e) or "next_text" in str(e) or "HTTP 400" in str(e) or "HTTP 422" in str(e)):
                    print(f"  contexto recusado pela API ({str(e)[:120]}…): repetindo sem previous/next_text")
                    ctx_ok = False
                    dados = sintetizar(chave, VOZ, MODELO, FMT, b, "", "", None)
                else:
                    raise
            pcm += decodificar_mp3(dados)
        with wave.open(str(saida), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(44100)
            w.writeframes(pcm)
        dur = len(pcm) / 2 / 44100
        log.append(f"{saida.name}: {dur:.2f} s · contexto {'sim' if ctx_ok else 'não'} · take {a.take}")
        print("  " + log[-1])
    if log:
        with open(U / "audio" / "log_voz_v34.txt", "a", encoding="utf-8") as f:
            f.write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
