"""yt_0018 v7: gera a narração INTEIRA de novo com ElevenLabs v4 (voz qw7jgPZWOKrl10GsjQ82, eleven_v4), em blocos de até 4.500 caracteres
cortados em fim de parágrafo (uma linha de "Texto corrido" = uma âncora), com previous_text/next_text (contexto) e /with-timestamps
(instante de cada caractere, sem ASR). Nenhum take de v1.1/v1.2/v1.3 é reaproveitado.

Fonte: `## Texto corrido (para gravação)` de narracao_tags_v1_4.md. Saída: audio/voz7/bloco_NN.{mp3,json}. A chave vem só de ELEVENLABS_API_KEY.
uso:
    python gerar_voz_v7.py --seco                # lista os blocos
    python gerar_voz_v7.py                       # gera os que não existem
    python gerar_voz_v7.py --bloco 2 --refazer   # gera esse bloco INTEIRO de novo (nunca uma frase isolada)
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
VOZ, MODELO, FMT = "qw7jgPZWOKrl10GsjQ82", "eleven_v4", "mp3_44100_192"
URL = "https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps?output_format={fmt}"
LIMITE = 4500
SAIDA = AQUI / "audio" / "voz7"


def ler_texto():
    t = (AQUI / "narracao_tags_v1_4.md").read_text(encoding="utf-8")
    corpo = t[t.index("## Texto corrido (para gravação)"):].split("\n", 1)[1]
    linhas = [l.strip() for l in corpo.splitlines() if l.strip()]
    ordem = json.loads((AQUI / "ancoras_nominal.json").read_text(encoding="utf-8"))["ordem"]
    assert len(linhas) == len(ordem), (len(linhas), len(ordem))
    return list(zip(ordem, linhas))


def blocos(par):
    saida, atual, n = [], [], 0
    for aid, linha in par:
        if atual and n + len(linha) + 1 > LIMITE:
            saida.append(atual)
            atual, n = [], 0
        atual.append((aid, linha))
        n += len(linha) + 1
    if atual:
        saida.append(atual)
    return saida


def chamar(chave, texto, antes="", depois=""):
    corpo = {"text": texto, "model_id": MODELO}
    if antes:
        corpo["previous_text"] = antes[-500:]
    if depois:
        corpo["next_text"] = depois[:500]
    req = urllib.request.Request(URL.format(voz=VOZ, fmt=FMT), json.dumps(corpo).encode("utf-8"),
                                 {"xi-api-key": chave, "Content-Type": "application/json", "User-Agent": "parallax-lab/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", "replace")[:600]
        if e.code == 400 and ("previous_text" in msg or "next_text" in msg) and (antes or depois):
            print("  (modelo não aceita previous_text/next_text: repetindo sem contexto)")
            return chamar(chave, texto)
        sys.exit(f"ElevenLabs HTTP {e.code}: {msg}")


def gravar(nome, texto, ids, resp):
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / f"{nome}.mp3").write_bytes(base64.b64decode(resp["audio_base64"]))
    meta = {"texto": texto, "ancoras": ids, "alinhamento": resp.get("alignment"), "alinhamento_normalizado": resp.get("normalized_alignment")}
    (SAIDA / f"{nome}.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seco", action="store_true")
    p.add_argument("--bloco", type=int)
    p.add_argument("--refazer", action="store_true")
    a = p.parse_args()
    par = ler_texto()
    bl = blocos(par)
    print(f"{len(par)} âncoras em {len(bl)} bloco(s): " + ", ".join(f"{len(b)} âncoras/{sum(len(l) + 1 for _, l in b)} car." for b in bl))
    for i, b in enumerate(bl, 1):
        print(f"  bloco {i}: {b[0][0]} … {b[-1][0]}")
    if a.seco:
        return
    chave = os.environ.get("ELEVENLABS_API_KEY")
    if not chave:
        sys.exit("Defina ELEVENLABS_API_KEY no ambiente.")
    for i, b in enumerate(bl, 1):
        if a.bloco and a.bloco != i:
            continue
        if (SAIDA / f"bloco_{i:02d}.mp3").exists() and not a.refazer:
            print(f"bloco {i}: já existe")
            continue
        if (SAIDA / f"bloco_{i:02d}.mp3").exists():                   # guarda o anterior (nunca apaga)
            n = 1 + len(list(SAIDA.glob(f"bloco_{i:02d}_antigo*.mp3")))
            for ext in ("mp3", "json"):
                (SAIDA / f"bloco_{i:02d}.{ext}").rename(SAIDA / f"bloco_{i:02d}_antigo{n}.{ext}")
        texto = "\n".join(l for _, l in b)
        antes = bl[i - 2][-1][1] if i > 1 else ""
        depois = bl[i][0][1] if i < len(bl) else ""
        print(f"bloco {i}/{len(bl)} ({b[0][0]}…{b[-1][0]}, {len(texto)} car.) ...", flush=True)
        gravar(f"bloco_{i:02d}", texto, [aid for aid, _ in b], chamar(chave, texto, antes, depois))
    print("ok")


if __name__ == "__main__":
    main()
