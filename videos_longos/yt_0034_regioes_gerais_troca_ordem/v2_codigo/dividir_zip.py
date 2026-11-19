"""yt_0034 · divide renders/yt0034_<rodada>_para_gpt.zip em zips independentes de no máximo LIM bytes (cada parte abre sozinha).
uso: python dividir_zip.py [limite_MB=470] [rodada=v1]"""
import sys
import zipfile
from pathlib import Path

U = Path(__file__).resolve().parent
R = sys.argv[2] if len(sys.argv) > 2 else "v1"
SRC = U / "renders" / f"yt0034_{R}_para_gpt.zip"
LIM = int(float(sys.argv[1]) if len(sys.argv) > 1 else 470) * 2 ** 20
FOLGA = 2 * 2 ** 20                                   # cabeçalhos e diretório central


def main():
    with zipfile.ZipFile(SRC) as z:
        itens = z.infolist()
        partes, atual, tam = [], [], 0
        for it in itens:
            t = it.compress_size + 200 + len(it.filename)
            if atual and tam + t > LIM - FOLGA:
                partes.append(atual)
                atual, tam = [], 0
            atual.append(it)
            tam += t
        if atual:
            partes.append(atual)
        n = len(partes)
        for k, lista in enumerate(partes, 1):
            out = U / "renders" / f"yt0034_{R}_para_gpt_parte{k}de{n}.zip"
            with zipfile.ZipFile(out, "w") as o:
                for it in lista:
                    o.writestr(it, z.read(it.filename), compress_type=it.compress_type)
            print(out.name, round(out.stat().st_size / 2 ** 20, 1), "MB", len(lista), "arquivos", lista[0].filename, "…", lista[-1].filename)


if __name__ == "__main__":
    main()
