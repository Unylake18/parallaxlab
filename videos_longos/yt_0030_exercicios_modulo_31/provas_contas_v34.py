"""yt_0030 · handoff v4 §5: prova de cada conta C1–C21 (um quadro 960×540 por item, no instante em que a conta inteira está na tela) →
qa/contas_v34/Cnn.png e a prancha qa/contas_v34.jpg; e o trecho do log com os [gm]/[gatilho] de cada item → qa/contas_v34/log_Cnn.txt.
uso: python provas_contas_v34.py"""
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
OUT = U / "qa" / "contas_v34"
OUT.mkdir(parents=True, exist_ok=True)
try:
    FT = ImageFont.truetype("arial.ttf", 18)
except OSError:
    FT = ImageFont.load_default()

ITENS = [  # (nome, lote, âncora, frase do gatilho, dt em s depois do gatilho, rótulo, frase que fecha o trecho do log)
    ("C01", "PD3", "D3-2", "então a rapidez é a distância", 1.1, "K1b, K2b e n2 juntos", "na divisão os expoentes se subtraem"),
    ("C02a", "PD3", "D3-3", "põe a potência com um a menos", 1.75, "P5 com K4 (∂Q/∂x degrau a degrau)", "a outra derivada é igualzinha"),
    ("C02b", "PD3", "D3-3", "e o sinal trocado", -0.15, "G5 (∂P/∂y degrau a degrau)", "ao subtrair menos com menos"),
    ("C02c", "PD3", "D3-3", "e esse vezes a potência com um", 1.3, "RS5c = s^{−α}(2 − 2α)", "sobra uma fórmula curtinha"),
    ("C02d", "PD3", "D3-3", "e sai o mesmo termo", 1.6, "DP e DQ completas", "uma vez com sinal de mais"),
    ("C03a", "PD3", "D3-6", "dividido por tê menos um", 1.7, "o2 e o3 com as setas acesas", "não tem limite"),
    ("C03b", "PD3", "D3-6", "a seta explode", 0.7, "cartões com rz1 e rz2", None),
    ("C04", "PD3B", "D3b-2", "e pela regra que acabamos", 0.6, "PH1, PH2, PH3", "por isso o quadradinho deformava"),
    ("C05", "PD3B", "D3b-4", "seno menos seno cancela", -0.15, "RR completa", "total um"),
    ("C06", "PD4", "D4-6", "então o desenho não se aproxima", 0.2, "DF1–DF6 + o palco com H", "tem quadradinho crescendo"),
    ("C07a", "PD4", "D4-7", "os termos com a quarta potência", -0.15, "ND + Q1 + Q2", "agora olha essa derivada"),
    ("C07b", "PD4", "D4-7", "e vale meio na diagonal inteira", 1.5, "EX + DG + os rótulos ½", "o campo não é de classe"),
    ("C08", "PD5", "D5-9", "em ípsilon o xis ao quadrado", 0.9, "o degrau 0 − 2y a caminho da célula", "derivando duas vezes o produto"),
    ("C09", "PA1", "A1-2", "em xis o um some", 0.95, "a célula (1,0) a caminho", "divergente zero mais zero"),
    ("C10a", "PA1", "A1-3", "com pi perto de três vírgula catorze", 1.4, "XR, OM1, OM2", "na margem direita menos dois terços"),
    ("C10b", "PA1", "A1-3", "bem no centro com xis zero", 0.9, "XR′ (as duas margens e o centro)", None),
    ("C11", "PA1", "A1-5", "máxima nas margens", 0.6, "DD1, DD2, DD3", None),
    ("C12", "PA2", "A2-2", "a tabela tem um e zero", 0.3, "a tabela do jato pelas derivadas", "rotacional zero"),
    ("C13", "PA2", "A2-2", "o produto não muda", -0.15, "HP, DT2, CH e D4 juntas", None),
    ("C14", "PA2", "A2-3", "dá um menos um", 1.2, "PH1, PH2, LX, LP", None),
    ("C15", "PA2", "A2-4", "quer dizer laplaciano do potencial igual a zero", 0.8, "a cadeia até Laplace com as derivadas", None),
    ("C16a", "PA4", "A4-2", "a primeira e a segunda componente", 1.0, "Z3 + FZ0 com as chaves", "confere as equações"),
    ("C16b", "PA4", "A4-2", "passou", 0.6, "CR1 + CR2", None),
    ("C17", "PA4", "A4-3", "as duas colunas têm o mesmo tamanho", 0.9, "JC3 + o quadradinho girado na direita", "quadradinhos pequenos viram quadradinhos"),
    ("C18", "PA4", "A4-4", "esse irmão não gira", 0.6, "o irmão com as derivadas", None),
    ("C19", "PA3", "A3-3", "o campo do fio cai", 1.0, "NB com o gráfico embaixo", None),
    ("C20", "PA3", "A3-4", "que é dois alfa vezes a potência", -0.15, "S1 com T1 e T2 na tela", "igual a zero alfa um"),
    ("C21a", "PA3", "A3-5", "o meio com o dois cancela", 0.3, "DN1", "a derivada da distância nessa direção"),
    ("C21b", "PA3", "A3-5", "e as potências da distância se juntam", 1.3, "PB0 → PB1", "então dá um sobre a distância"),
]


def log(lote):
    return (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")


def t_gat(lote, aid, frase):
    L = log(lote)
    a = {m.group(1): float(m.group(2)) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", L)}
    m = re.search(r"\[gatilho\] %s +([0-9.]+)s \(alvo[^)]*\) %s\s*$" % (re.escape(aid), re.escape(frase)), L, re.M)
    if m is None:
        raise SystemExit(f"{lote} {aid}: gatilho «{frase}» não está no log")
    return a[aid] + float(m.group(1))


def trecho(lote, aid, f0, f1):
    L = log(lote).splitlines()
    i0 = next(i for i, l in enumerate(L) if l.startswith(f"[gatilho] {aid} ") and l.rstrip().endswith(f0))
    i1 = next((i for i, l in enumerate(L) if i > i0 and f1 and l.startswith(f"[gatilho] {aid} ") and l.rstrip().endswith(f1)), None)
    if i1 is None:
        i1 = next((i for i, l in enumerate(L) if i > i0 and l.startswith("[ancora]")), len(L))
    return [l for l in L[i0:i1 + 1] if l.startswith(("[gm]", "[gatilho]", "[origem]", "[cancela]", "[leitura]", "[fim-leitura]"))]


def quadros(lote, ts):
    c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
    alvo = sorted({round(t * 15): t for t in ts}.items())
    out, k = {}, 0
    for i, fr in enumerate(c.decode(video=0)):
        while k < len(alvo) and i >= alvo[k][0]:
            out[alvo[k][1]] = fr.to_image()
            k += 1
        if k >= len(alvo):
            break
    c.close()
    return [out[t] for t in ts]


if __name__ == "__main__":
    import sys
    so = set(sys.argv[1:])                                           # opcional: só estes lotes (ex.: PD4 PA1)
    por_lote = {}
    for it in ITENS:
        if not so or it[1] in so:
            por_lote.setdefault(it[1], []).append(it)
    ims = {}
    for lote, its in por_lote.items():
        ts = [t_gat(lote, a, f) + dt for _, _, a, f, dt, _, _ in its]
        for it, im, t in zip(its, quadros(lote, ts), ts):
            ims[it[0]] = (im, t)
            im.save(OUT / f"{it[0]}.png")
            ls = trecho(lote, it[2], it[3], it[6])
            (OUT / f"log_{it[0]}.txt").write_text("\n".join(ls) + "\n", encoding="utf-8")
            print(f"{it[0]} {lote} {it[2]} t={t:.2f}s · {sum(l.startswith('[gm]') for l in ls)} gm · {it[5]}")
    if so:
        raise SystemExit(0)
    COL = 3
    nomes = [it[0] for it in ITENS]
    lin = (len(nomes) + COL - 1) // COL
    pr = Image.new("RGB", (COL * 960, lin * 572), (5, 11, 24))
    d = ImageDraw.Draw(pr)
    for k, n in enumerate(nomes):
        im, t = ims[n]
        x, y = k % COL * 960, k // COL * 572
        pr.paste(im, (x, y + 32))
        it = next(i for i in ITENS if i[0] == n)
        d.text((x + 8, y + 7), f"{n} · {it[2]} · {it[5]}", fill=(255, 220, 90), font=FT)
    pr.save(U / "qa" / "contas_v34.jpg", quality=90)
    print(U / "qa" / "contas_v34.jpg", pr.size)
