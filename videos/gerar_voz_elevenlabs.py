"""Gera a narração pela API do ElevenLabs e grava um WAV (PCM 16 bits, mono).

A chave nunca vai para arquivo do repositório: use a variável de ambiente ELEVENLABS_API_KEY.

Uso:
    uv run python videos/gerar_voz_elevenlabs.py TEXTO.md SAIDA.wav --voz VOICE_ID [--secao "## Texto corrido"]
    uv run python videos/gerar_voz_elevenlabs.py TEXTO.md SAIDA.wav --seco   # só mostra os blocos, sem chamar a API

Voz e modelo também podem vir de ELEVENLABS_VOICE_ID e ELEVENLABS_MODEL.
Textos longos são divididos em blocos (padrão 4500 caracteres, limite do ElevenLabs: 5000),
com previous_text/next_text para manter a continuidade entre blocos.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
import wave

API = "https://api.elevenlabs.io/v1/text-to-speech/{voz}?output_format={fmt}"
# formato -> taxa de amostragem (pcm_44100 exige plano Pro)
TAXAS = {"pcm_44100": 44100, "pcm_24000": 24000, "pcm_22050": 22050, "pcm_16000": 16000,
         "mp3_44100_192": 44100}  # mp3 é decodificado com PyAV (plano Creator+, sem exigir Pro)


def decodificar_mp3(dados: bytes) -> bytes:
    import av
    import io
    saida = bytearray()
    with av.open(io.BytesIO(dados)) as c:
        rs = av.AudioResampler(format="s16", layout="mono", rate=44100)
        for fr in c.decode(audio=0):
            for r in rs.resample(fr):
                saida += bytes(r.planes[0])[: r.samples * 2]
        for r in rs.resample(None):
            saida += bytes(r.planes[0])[: r.samples * 2]
    return bytes(saida)


def extrair(texto: str, secao: str | None) -> str:
    if secao:
        i = texto.find(secao)
        if i < 0:
            sys.exit(f"Seção não encontrada: {secao!r}")
        texto = texto[i + len(secao):]
        m = re.search(r"^#{1,6} ", texto, flags=re.M)  # para no próximo título
        if m:
            texto = texto[:m.start()]
    return texto.strip()


def blocos(texto: str, limite: int) -> list[str]:
    frases = []
    for par in re.split(r"\n\s*\n", texto):
        par = " ".join(par.split())
        if par:
            frases.extend(re.split(r"(?<=[.!?…])\s+", par))
    saida, atual = [], ""
    for f in frases:
        if atual and len(atual) + 1 + len(f) > limite:
            saida.append(atual)
            atual = f
        else:
            atual = f"{atual} {f}".strip()
    if atual:
        saida.append(atual)
    return saida


def sintetizar(chave, voz, modelo, fmt, texto, antes, depois, ajustes):
    corpo = {"text": texto, "model_id": modelo}
    if antes:
        corpo["previous_text"] = antes[-600:]
    if depois:
        corpo["next_text"] = depois[:600]
    if ajustes:
        corpo["voice_settings"] = ajustes
    req = urllib.request.Request(
        API.format(voz=voz, fmt=fmt), json.dumps(corpo).encode("utf-8"),
        {"xi-api-key": chave, "Content-Type": "application/json", "User-Agent": "parallax-lab/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("texto")
    p.add_argument("saida")
    p.add_argument("--voz", default=os.environ.get("ELEVENLABS_VOICE_ID"))
    p.add_argument("--modelo", default=os.environ.get("ELEVENLABS_MODEL", "eleven_v4"))
    p.add_argument("--formato", default="mp3_44100_192", choices=sorted(TAXAS))
    p.add_argument("--contexto", action="store_true",
                   help="envia previous_text/next_text entre blocos (pode não ser aceito por todos os modelos)")
    p.add_argument("--secao", help='só usa o texto depois deste título (ex.: "## Texto corrido")')
    p.add_argument("--limite", type=int, default=4500)
    p.add_argument("--ajustes", help='JSON de voice_settings (ex.: \'{"stability":0.5,"similarity_boost":0.75}\')')
    p.add_argument("--seco", action="store_true", help="não chama a API; lista os blocos")
    a = p.parse_args()

    with open(a.texto, encoding="utf-8") as f:
        partes = blocos(extrair(f.read(), a.secao), a.limite)
    print(f"{len(partes)} bloco(s): {[len(b) for b in partes]} caracteres")
    if a.seco:
        for i, b in enumerate(partes, 1):
            print(f"\n--- bloco {i} ---\n{b}")
        return

    chave = os.environ.get("ELEVENLABS_API_KEY")
    if not chave:
        sys.exit("Defina ELEVENLABS_API_KEY no ambiente (não grave a chave em arquivo do repositório).")
    if not a.voz:
        sys.exit("Informe a voz com --voz ou ELEVENLABS_VOICE_ID.")
    ajustes = json.loads(a.ajustes) if a.ajustes else None

    pcm = b""
    for i, b in enumerate(partes):
        antes = partes[i - 1] if a.contexto and i else ""
        depois = partes[i + 1] if a.contexto and i + 1 < len(partes) else ""
        print(f"bloco {i + 1}/{len(partes)} ...", flush=True)
        dados = sintetizar(chave, a.voz, a.modelo, a.formato, b, antes, depois, ajustes)
        pcm += decodificar_mp3(dados) if a.formato.startswith("mp3") else dados

    with wave.open(a.saida, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(TAXAS[a.formato])
        w.writeframes(pcm)
    print(f"{a.saida}: {len(pcm) / 2 / TAXAS[a.formato]:.1f} s")


if __name__ == "__main__":
    main()
