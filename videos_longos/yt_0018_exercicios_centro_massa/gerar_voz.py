"""yt_0018 v6: gera a narração com ElevenLabs v4 (voz qw7jgPZWOKrl10GsjQ82, eleven_v4) em blocos cortados só em fim de âncora.

Fonte: `## Texto corrido (para gravação)` de narracao_tags_v1_3.md (uma linha = uma âncora, na ordem de ancoras.json). Usa o endpoint
/with-timestamps: além do áudio vem o instante de cada caractere, e é dele que o cortar_voz.py tira o início e o fim de cada âncora e de cada palavra
(sem ASR). A chave vem só de ELEVENLABS_API_KEY.

uso:
    python gerar_voz.py --seco                 # lista os blocos, sem chamar a API
    python gerar_voz.py                        # gera os blocos que ainda não existem em audio/voz/
    python gerar_voz.py --bloco 2 --refazer    # regera um bloco
    python gerar_voz.py --ancora X3-6          # novo take só dessa âncora (audio/voz/take_X3-6_N.*); o cortar_voz.py usa o último
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
VOZ, MODELO, FMT = "qw7jgPZWOKrl10GsjQ82", "eleven_v4", "mp3_44100_192"
URL = "https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps?output_format={fmt}"
LIMITE = 4200                                   # caracteres por bloco (limite da API: 5000)
SAIDA = AQUI / "audio" / "voz"


def ler_texto():
    t = (AQUI / "narracao_tags_v1_3.md").read_text(encoding="utf-8")
    corpo = t[t.index("## Texto corrido (para gravação)"):].split("\n", 1)[1]
    linhas = [l.strip() for l in corpo.splitlines() if l.strip()]
    ordem = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))["ordem"]
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
        with urllib.request.urlopen(req, timeout=600) as r:
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
    p.add_argument("--ancora")
    a = p.parse_args()
    par = ler_texto()
    bl = blocos(par)
    print(f"{len(par)} âncoras em {len(bl)} bloco(s): " + ", ".join(f"{len(b)} âncoras/{sum(len(l) + 1 for _, l in b)} car." for b in bl))
    if a.seco:
        for i, b in enumerate(bl, 1):
            print(f"\n--- bloco {i}: {b[0][0]} … {b[-1][0]} ---")
            print("\n".join(f"[{aid}] {l[:90]}…" for aid, l in b))
        return
    chave = os.environ.get("ELEVENLABS_API_KEY")
    if not chave:
        sys.exit("Defina ELEVENLABS_API_KEY no ambiente.")
    if a.ancora:
        k = next(i for i, (aid, _) in enumerate(par) if aid == a.ancora)
        antes = par[k - 1][1] if k else ""
        depois = par[k + 1][1] if k + 1 < len(par) else ""
        n = 1 + len(list(SAIDA.glob(f"take_{a.ancora}_*.mp3")))
        print(f"take {n} de {a.ancora} ...", flush=True)
        gravar(f"take_{a.ancora}_{n}", par[k][1], [a.ancora], chamar(chave, par[k][1], antes, depois))
        return
    for i, b in enumerate(bl, 1):
        if a.bloco and a.bloco != i:
            continue
        if (SAIDA / f"bloco_{i:02d}.mp3").exists() and not a.refazer:
            print(f"bloco {i}: já existe")
            continue
        texto = "\n".join(l for _, l in b)
        antes = bl[i - 2][-1][1] if i > 1 else ""
        depois = bl[i][0][1] if i < len(bl) else ""
        print(f"bloco {i}/{len(bl)} ({b[0][0]}…{b[-1][0]}, {len(texto)} car.) ...", flush=True)
        gravar(f"bloco_{i:02d}", texto, [aid for aid, _ in b], chamar(chave, texto, antes, depois))
    print("ok")


if __name__ == "__main__":
    main()
