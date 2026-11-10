"""yt_0026 v7: monta, para cada quadro-alvo, a imagem lado a lado (render à esquerda, alvo à direita) a partir dos stills de renders/v6/qa/still_<lote>_<t>.png.
uso: python comparar.py  → renders/v6/qa/lado_a_lado_NN_<nome>.png (1920×540 cada, os dois a 960×540)"""
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
ALVOS = U / "referencia_v7" / "yt_0026_quadros_alvo_v7"
OUT = U / "renders" / "v6" / "qa"
OUT.mkdir(parents=True, exist_ok=True)


def inicios(lote):
    """{âncora: início (s do lote)} lido do log do render."""
    t = (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")
    return {m.group(1): float(m.group(2)) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", t)}


def gatilho(lote, ancora, frase):
    t = (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")
    for l in t.splitlines():
        m = re.match(r"\[gatilho\] (\S+)\s+([0-9.]+)s .*?\) (.*)$", l)
        if m and m.group(1) == ancora and frase in m.group(3):
            return float(m.group(2))
    return None


# (nº, nome, lote, instante) — instante = função(lote) em s do lote
def fim(lote, a, prox, folga=0.4):
    i = inicios(lote)
    return round(i[prox] - folga, 2)


def alvos():
    L = {}
    L[1] = ("T0_campo", "PT", lambda: fim("PT", "T0", "T1"))
    L[2] = ("T1_volume", "PT", lambda: fim("PT", "T1", "T2"))
    L[3] = ("T2_trabalho", "PT", lambda: fim("PT", "T2", "T3"))
    L[4] = ("T3_fluxo", "PT", lambda: fim("PT", "T3", "T4"))
    L[5] = ("T4a_green_cancela", "PT", lambda: inicios("PT")["T4"] + (gatilho("PT", "T4", "as trocas entre vizinhos") or 6) + 1.2)
    L[6] = ("T4b_green_borda", "PT", lambda: inicios("PT")["T4"] + (gatilho("PT", "T4", "no plano") or 11) - 0.3)
    L[7] = ("T4c_tres_teoremas", "PT", lambda: fim("PT", "T4", "T5"))
    L[8] = ("T5_cartao", "PT", lambda: fim("PT", "T5", "T5", -3.0) if False else round(inicios("PT")["T5"] + 7.0, 2))
    L[9] = ("H3_mesma_formula", "PAH", lambda: round(inicios("PAH")["H3"] + 12.0, 2))
    L[10] = ("B1_que_funcao", "PB1", lambda: fim("PB1", "B1-2", "B1-3", 3.5))
    L[11] = ("B2_polares", "PB2", lambda: round(inicios("PB2")["B2-7"] + 4.5, 2))
    L[12] = ("B3_dobra", "PB3", lambda: fim("PB3", "B3-3", "B3-4", 0.5))
    L[13] = ("B4_tigela", "PB4", lambda: round(inicios("PB4")["B4-3"] + 8.0, 2))
    L[14] = ("B5_campo_radial", "PB5", lambda: fim("PB5", "B5-3", "B5-4", 2.0))
    L[15] = ("B5-4_transf_x_campo", "PB5", lambda: round(inicios("PB5")["B5-4"] + 17.0, 2))
    L[16] = ("B6_perpendicular", "PB6", lambda: fim("PB6", "B6-4", "B6-5", 0.6))
    L[17] = ("B6_gamma_linha", "PB6", lambda: fim("PB6", "B6-5", "B6-6", 1.5))
    L[18] = ("B7_espaco", "PB7", lambda: fim("PB7", "B7-1", "B7-2", 1.0))
    L[19] = ("S1_resumo", "PS", lambda: fim("PS", "S1", "S2", 1.2))
    return L


def quadro(lote, t):
    import av
    c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
    alvo = round(t * 15)
    for i, f in enumerate(c.decode(video=0)):
        if i >= alvo:
            return f.to_image()
    return None


if __name__ == "__main__":
    import sys
    plano = {k: (n, l, f()) for k, (n, l, f) in alvos().items()}
    (OUT / "instantes.json").write_text(json.dumps(plano, ensure_ascii=False, indent=1), encoding="utf-8")
    so = {int(x) for x in sys.argv[1:]} or set(plano)
    for k, (n, l, t) in plano.items():
        if k not in so:
            continue
        a = ALVOS / next(p.name for p in ALVOS.glob(f"{k:02d}_*.jpg"))
        fr = quadro(l, t)
        if fr is None:
            print("sem quadro", k)
            continue
        fr.save(OUT / f"quadro_{k:02d}_{n}.png")
        im = Image.new("RGB", (1920, 580), (0, 0, 0))
        im.paste(fr.convert("RGB").resize((960, 540)), (0, 40))
        im.paste(Image.open(a).convert("RGB").resize((960, 540)), (960, 40))
        d = ImageDraw.Draw(im)
        d.text((10, 12), f"{k:02d} {n}: RENDER ({l} a {t}s)", fill=(255, 255, 255))
        d.text((970, 12), "ALVO", fill=(255, 255, 255))
        im.save(OUT / f"lado_a_lado_{k:02d}_{n}.png")
    print("ok")
