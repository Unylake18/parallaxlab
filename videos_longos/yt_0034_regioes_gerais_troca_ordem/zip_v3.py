"""yt_0034 · zips do preview v3 para o GPT (nunca vão para entregas/):
  1) renders/yt0034_v3_para_gpt_parteNdeM.zip — o que o handoff v3 §0 pede: preview, código, QA e ficha, em partes de ≤ 30 MB (cada parte abre sozinha);
  2) renders/yt0034_v3_quadros_parteNdeM.zip — todos os quadros do preview (PNG com índice e tempo), em partes de ≤ 450 MiB (< 480 MB).
uso: python zip_v3.py"""
import io
import zipfile
from pathlib import Path

import av

U = Path(__file__).resolve().parent
R = "v3"
MP4 = U / "renders" / R / f"yt_0034_preview_{R}_540p15.mp4"


def partes(itens, lim, nome):
    """itens: [(arcname, bytes, compress)] → zips independentes de no máximo lim bytes."""
    grupos, atual, tam = [], [], 0
    for it in itens:
        t = len(it[1]) + 300 + len(it[0])
        if atual and tam + t > lim - 2 ** 20:
            grupos.append(atual)
            atual, tam = [], 0
        atual.append(it)
        tam += t
    if atual:
        grupos.append(atual)
    n = len(grupos)
    for old in (U / "renders").glob(f"{nome}_parte*.zip"):
        old.unlink()
    for k, g in enumerate(grupos, 1):
        out = U / "renders" / f"{nome}_parte{k}de{n}.zip"
        with zipfile.ZipFile(out, "w") as z:
            for arc, data, comp in g:
                z.writestr(arc, data, compress_type=comp)
        print(out.name, round(out.stat().st_size / 2 ** 20, 1), "MiB", len(g), "arquivos")


def main():
    D, S = zipfile.ZIP_DEFLATED, zipfile.ZIP_STORED
    it = [(MP4.name, MP4.read_bytes(), S)]
    for f in sorted(U.glob("*.py")) + sorted(U.glob("*.sh")) + [U / "ficha.md", U / "narracao.md", U / "ancoras.json"]:
        it.append((f"codigo/{f.name}", f.read_bytes(), D))
    it.append(("codigo/threejs/cena3d/c34.js", (U / "threejs" / "cena3d" / "c34.js").read_bytes(), D))
    for f in sorted((U / "renders" / R / "qa").glob("*")):
        if f.suffix in (".txt", ".jpg", ".json"):
            it.append((f"qa/{f.name}", f.read_bytes(), S if f.suffix == ".jpg" else D))
    partes(it, 30 * 10 ** 6, f"yt0034_{R}_para_gpt")
    q = []
    c = av.open(str(MP4))
    for i, fr in enumerate(c.decode(video=0)):
        b = io.BytesIO()
        fr.to_image().save(b, "PNG", optimize=False, compress_level=6)
        t = i / 15
        q.append((f"quadros/q{i:05d}_{int(t) // 60:02d}m{t % 60:05.2f}s.png", b.getvalue(), S))
    c.close()
    partes(q, 450 * 2 ** 20, f"yt0034_{R}_quadros")


if __name__ == "__main__":
    main()
