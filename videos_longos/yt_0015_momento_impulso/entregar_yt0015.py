"""yt_0015 — legenda (.srt), capítulos e pasta final em entregas/Vídeos Longos/ (cópia; não move nem apaga origens).

Uso: uv run --no-sync python entregar_yt0015.py
- final/legenda - yt0015.srt: tempos do alinhamento forçado da voz (audio/alinhamento_forcado_bruto.json); a voz não tem silêncio
  inserido, então o tempo da voz é o tempo do master. Até 2 linhas de ≤ 42 caracteres (mesma regra do yt_0014).
- final/capitulos - yt0015.txt: início de cada bloco = S da primeira âncora dele (sync/mapa.json) − 1 s.
- entregas/Vídeos Longos/<pasta>/: master, legenda, capítulos, audio/, texto/, zip para o GPT e manifesto (origem, tamanho, SHA-256).
O worktree não tem entregas/: o destino é a pasta entregas/ do checkout principal.
"""
import hashlib
import json
import shutil
import textwrap
from pathlib import Path

import av

U = Path(__file__).resolve().parent
ROOT = next(p for p in (U.parents[4], U.parents[1]) if (p / "entregas").is_dir())
N = "yt0015"
DEST = ROOT / "entregas" / "Vídeos Longos" / "Mecânica - Momento - Momento linear e impulso"
F = U / "final"
MAPA = json.loads((U / "sync" / "mapa.json").read_text(encoding="utf-8"))


def fmt(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    ms = int(round((s - int(s)) * 1000))
    if ms == 1000:
        s, ms = s + 1, 0
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{ms:03d}"


def legenda():
    pal = [(w["text"].strip(), w["start"], w["end"]) for w in
           json.loads((U / "audio" / "alinhamento_forcado_bruto.json").read_text(encoding="utf-8"))["words"] if w["text"].strip()]
    blocos, cur = [], []
    for p in pal:
        cur.append(p)
        t = " ".join(q[0] for q in cur)
        if p[0][-1] in ".?!:" or (p[0][-1] in ",;" and len(t) > 45) or len(t) > 64:
            blocos.append(cur)
            cur = []
    if cur:
        blocos.append(cur)
    out = []
    for i, b in enumerate(blocos, 1):
        a, f = b[0][1], b[-1][2] + 0.25
        if i < len(blocos):
            f = min(f, blocos[i][0][1] - 0.02)
        out.append(f"{i}\n{fmt(a)} --> {fmt(f)}\n" + "\n".join(textwrap.wrap(" ".join(q[0] for q in b), 42)))
    (F / f"legenda - {N}.srt").write_text("\n\n".join(out) + "\n", encoding="utf-8")
    return len(blocos)


CAP = [("H1", "Por que dobrar os joelhos salva as pernas?"), ("T1-1", "De onde vem o momento"),
       ("T2-1", "O fato experimental: o momento se conserva"), ("T3-1", "Por que massa vezes velocidade?"),
       ("T4-1", "Da conservação à terceira lei"), ("T5-1", "Impulso"), ("E1-1", "Exemplo: bola na parede"),
       ("E2-1", "Exemplo: chute em 2D"), ("E3-1", "Exemplo: força que cresce com o tempo"), ("T6-1", "Momento ou energia?"),
       ("E4-1", "De volta ao muro"), ("E5-1", "A pulga"), ("S1", "Resumo")]


def capitulos():
    linhas = []
    for aid, tit in CAP:
        t = 0.0 if aid == "H1" else max(0.0, MAPA["ancoras"][aid]["S"] - 1.0)
        linhas.append(f"{int(t) // 60:02d}:{int(t) % 60:02d} {tit}")
    (F / f"capitulos - {N}.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return linhas


def sha(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    F.mkdir(exist_ok=True)
    nleg, caps = legenda(), capitulos()
    (DEST / "audio").mkdir(parents=True, exist_ok=True)
    (DEST / "texto").mkdir(parents=True, exist_ok=True)
    cop = [
        (U / "renders" / "master_yt0015.mp4", f"master - {N}.mp4"),
        (F / f"legenda - {N}.srt", f"legenda - {N}.srt"),
        (F / f"capitulos - {N}.txt", f"capitulos - {N}.txt"),
        (U / "renders" / "final_para_gpt.zip", f"quadros_e_video_para_gpt - {N}.zip"),
        (U / "audio" / "narracao_master.wav", f"audio/narracao_master - {N}.wav"),
        (U / "audio" / "narracao_v4.wav", f"audio/narracao_v4 - {N}.wav"),
        (U / "audio" / "loudness_master.json", f"audio/loudness_master - {N}.json"),
        (U / "ficha.md", f"texto/ficha - {N}.md"),
        (U / "narracao_sugestao.md", f"texto/narracao - {N}.md"),
        (U / "narracao_tags.md", f"texto/narracao_tags - {N}.md"),
        (U / "audio" / "texto_voz_v4.txt", f"texto/texto_narracao - {N}.txt"),
    ]
    arquivos = []
    for o, d in cop:
        shutil.copy2(o, DEST / d)
        arquivos.append({"arquivo": d.replace("/", "\\"), "origem": str(o), "bytes": (DEST / d).stat().st_size,
                         "sha256": sha(DEST / d)})
    with av.open(str(DEST / f"master - {N}.mp4")) as c:
        v = c.streams.video[0]
        info = {"resolucao": f"{v.width}x{v.height}", "fps": float(v.average_rate), "duracao_s": round(float(c.duration) / 1e6, 2),
                "codec": "H.264 yuv420p CRF 14", "audio": bool(c.streams.audio), "loudness": "−14,1 LUFS · −1,3 dBTP (AAC 192 kb/s)"}
    man = {"unidade": "yt_0015", "titulo": "Momento linear e impulso", "pergunta": "Por que dobrar os joelhos salva as suas pernas?",
           "rotulo_na_tela": "Mecânica · Momento linear e impulso", "parte": "1 de 2 (a parte 2 é o yt_0016)",
           "sincronia": f"{len(MAPA['ordem'])} âncoras (sync/mapa.json + sync/ritmo.json), alinhamento forçado ElevenLabs, voz sem silêncio inserido",
           "arquivos": sorted(arquivos, key=lambda a: a["arquivo"]), "video": info}
    (DEST / f"manifesto - {N}.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print("entrega em", DEST)
    print(f"{nleg} legendas; {len(caps)} capítulos")
    print("\n".join(caps))
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    main()
