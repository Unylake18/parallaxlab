"""Quadro de um lote: python q.py LOTE ANCORA OFFSET [ALVO] → renders/still/LOTE_ANCORA_OFF.png (t = início da âncora no lote + OFFSET; OFFSET < 0 conta do fim)
e, com ALVO (nº do quadro-alvo), a comparação cmp_*.png (alvo em cima, render embaixo)."""
import sys
from pathlib import Path
import av
from PIL import Image
from tempos import ANC_DADOS
U = Path(__file__).resolve().parent
LOTE0 = {"PH": "H-1", "PD1": "D1-1", "PD2": "D2-1", "PD3": "D3-1", "PD3B": "D3b-1", "PD4": "D4-1", "PD5": "D5-1", "PA1": "P2-1", "PA2": "A2-1",
         "PA4": "A4-1", "PA3": "A3-1", "PS": "S-1"}


def t_de(lote, aid, off):
    A = ANC_DADOS["ancoras"]
    a = A[aid]
    base = A[LOTE0[lote]]["ini"]
    return (a["ini"] - base) + (off if off >= 0 else a["dur"] + off)


def quadro(lote, t):
    c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
    q = round(t * 15)
    im = None
    for i, fr in enumerate(c.decode(video=0)):
        im = fr
        if i >= q:
            break
    c.close()
    return im.to_image()


if __name__ == "__main__":
    lote, aid, off = sys.argv[1], sys.argv[2], float(sys.argv[3])
    t = t_de(lote, aid, off)
    im = quadro(lote, t)
    nome = f"{lote}_{aid}_{off:g}"
    (U / "renders/still").mkdir(parents=True, exist_ok=True)
    im.save(U / "renders/still" / f"{nome}.png")
    if len(sys.argv) > 4:
        a = Image.open(iter(list((U / "referencia_v1").glob(f"{sys.argv[4]}_*.jpg")) + list((U / "referencia_v2").glob(f"{sys.argv[4]}_*.jpg"))).__next__()).convert("RGB").resize((960, 540), Image.LANCZOS)
        o = Image.new("RGB", (960, 1084), (255, 255, 255))
        o.paste(a, (0, 0))
        o.paste(im, (0, 544))
        o.save(U / "renders/still" / f"cmp_{nome}.png")
    print(nome, f"t = {t:.2f}")
