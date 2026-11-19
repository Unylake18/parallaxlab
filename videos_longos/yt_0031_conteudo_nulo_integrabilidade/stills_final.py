"""yt_0031 final §3/§7: stills de prova F1–F11 (do vídeo 540p de cada lote, com o 3D) e a prancha correcoes_final.jpg (quadro do erro do v3,
em referencia_final/, ao lado do quadro corrigido no gatilho). Instantes tirados dos logs do render (âncora + gatilho, ou [glyphmap]).
uso: python stills_final.py [res]   (res = 540p15 | 1080p30; padrão 540p15)
Saídas: qa/final/F*.png, qa/final/correcoes_final.jpg, qa/final/stills.txt"""
import re
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
RES = sys.argv[1] if len(sys.argv) > 1 else "540p15"
FPS = 30 if RES.startswith("1080") else 15
PRE, LOGP = ("media1080_", "log1080_") if RES.startswith("1080") else ("media_", "log_")
OUT = U / "qa" / "final"
OUT.mkdir(parents=True, exist_ok=True)
REF = U / "referencia_final"


def log(l):
    return (U / f"{LOGP}{l}.txt").read_text(encoding="utf-8", errors="ignore")


def t_gat(l, frase, k=0):
    t = log(l)
    anc = {a: float(x) for a, x in re.findall(r"\[ancora\] (\S+) ([\d.]+)", t)}
    m = [(a, float(r)) for a, r, f in re.findall(r"\[gatilho\] (\S+) +([\d.]+)s \(alvo[^)]*\) (.*)", t) if f.strip() == frase]
    a, r = m[k]
    return anc[a] + r


def t_gm(l, rot):
    m = re.findall(r"\[glyphmap\] +([\d.]+) \S+ " + re.escape(rot), log(l))
    return float(m[0])


def t_total(l):
    return float(re.findall(r"\[tempo\] total ([\d.]+)s", log(l))[-1])


# (id, lote, função do instante (s do lote), deslocamentos (s), referência do v3, o que prova)
ITENS = [
    ("F1", "PB6", lambda: t_gat("PB6", "contradição"), [0.45, 1.95, None], "12m55_47s_B6-3_CONTRADICAO_completa_so_0,4s.png",
     "CONTRADIÇÃO: na palavra (+0,45 s, caneta pronta), +1,5 s e no último quadro do B6-3"),
    ("F2a", "PB7", lambda: t_gm("PB7", "mapa 4a"), [0.1 * k for k in range(1, 7)], "14m42_80s_B7-2_voo_4Me1_cruza_linha550.png",
     "mapa 4a: 4Mε₁ por fora à direita e por baixo da 690; ε/(8M) pela direita da própria linha (a cada 0,1 s)"),
    ("F2b", "PB7", lambda: t_gm("PB7", "ε/2 + ε/2 = ε"), [0.1 * k for k in range(1, 7)] + [0.1 * k for k in range(7, 13, 2)],
     "14m50_80s_B7-2_voo_soma_cruza_ESCOLHA.png", "soma: S(P) − s(P) < a caneta; os dois ε/2 pela direita (x ≥ 1600) e por baixo da 840"),
    ("F3a", "PB4", lambda: t_gm("PB4", "mapa 5a"), [k * 2 / 15 for k in range(0, 8)], "08m10_27s_B4-1_mapa5a_2_sobre_5.png",
     "mapa 5a em dois tempos: some o resultado, os pares abrem espaço, a caneta escreve o 2 (um quadro a cada 2)"),
    ("F3b", "PB4", lambda: t_gm("PB4", "mapa 5b"), [k * 2 / 15 for k in range(0, 8)], "08m11_07s_B4-1_mapa5b_1_sobre_2.png",
     "mapa 5b em dois tempos: o 1 de 0,125 entra no espaço aberto (um quadro a cada 2)"),
    ("F4", "PB2", lambda: t_gat("PB2", "no metal pesado o mesmo"), [1.0], "04m40_00s_B2-1_TAMPA0_placa_encosta_borda.png",
     "TAMPA / 0 em duas linhas, placa ≈ 80 px, folga ≥ 20 px; contorno laranja 4 px"),
    ("F5a", "PB4", lambda: t_gat("PB4", "soma por cima"), [0.6], "09m03_60s_B4-3_topo_coral_quase_invisivel.png", "escada coral pelos topos (6 px)"),
    ("F5b", "PB4", lambda: t_gat("PB4", "soma por baixo"), [0.6], "09m03_60s_B4-3_zoom_topos.png", "escada azul-clara pelas bases (6 px)"),
    ("F6", "PA", lambda: t_gat("PA", "entender o que é conteúdo"), [-0.4, 0.5], "01m32_53s_A1_chip2_contorno_vazio.png",
     "chip 2: o contorno só nasce com o texto (−0,4 s: nenhum contorno vazio)"),
    ("F7", "PB7", lambda: t_gat("PB7", "escolhe os dois épsilons"), [1.4], "14m32_00s_B7-2_ESCOLHA_DOS_DOIS_eps.png",
     "ε da legenda em MathTex próprio, 34 px, menta; 2 sob o 8 em \\textstyle"),
    ("F8", "PB6", lambda: t_gat("PB6", "com épsilon igual a um"), [-0.3], "12m10_93s_B6-2_X_e_eps.png", "X 12 px acima e à direita; ε das barras a 30 px"),
    ("F9", "PS", lambda: t_gat("PS", "ela entra duas vezes"), [1.5], None, "? de \\overset em \\textstyle"),
    ("F10", "PB3", lambda: t_gat("PB3", "um retângulo comprido"), [2.0], "07m37_40s_B3-3_tremor_1px_segmento.png",
     "retângulos do segmento com bordas em y par (sem tremor)"),
    ("F11", "PB4", lambda: t_gat("PB4", "circunferências elipses"), [0.5], "09m26_00s_B4-3_formas_ordem_OK.png", "rótulo CIRCUNFERÊNCIA (24 px)"),
]

caches = {}


def quadros(lote, ts):
    vid = U / f"{PRE}{lote}/videos/cena/{RES}/{lote}.mp4"
    alvos = {max(0, round(t * FPS)): t for t in ts}
    out = {}
    with av.open(str(vid)) as c:
        ult = None
        for k, fr in enumerate(c.decode(video=0)):
            if k in alvos:
                out[alvos[k]] = fr.to_image()
            ult = fr
            if len(out) == len(alvos):
                break
        for t in ts:
            out.setdefault(t, ult.to_image())
    return out


try:
    F = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
except OSError:
    F = ImageFont.load_default()
linhas, pares = [], []
for fid, lote, f_t, offs, ref, prova in ITENS:
    try:
        t0 = f_t()
    except Exception as e:                      # noqa: BLE001
        linhas.append(f"{fid} {lote}: instante não encontrado ({e})")
        continue
    ts = [(t_total(lote) - 1 / FPS - 0.25) if o is None else t0 + o for o in offs]
    ims = quadros(lote, ts)
    for j, t in enumerate(ts):
        nome = f"{fid}_{j + 1}_{lote}_{t:.2f}s.png"
        ims[t].save(OUT / nome)
        linhas.append(f"{fid} {lote} t={t:7.2f} s (lote) → qa/final/{nome}   {prova if j == 0 else ''}")
    pares.append((fid, ref, ims[ts[0]] if fid not in ("F1",) else ims[ts[1]], prova))
(OUT / "stills.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
W, H = 960, 540
P = Image.new("RGB", (2 * W + 36, len(pares) * (H + 44) + 12), (22, 18, 34))
d = ImageDraw.Draw(P)
for i, (fid, ref, im, prova) in enumerate(pares):
    y = 12 + i * (H + 44)
    d.text((12, y + 4), f"{fid} · v3 (erro) × final (corrigido) · {prova}", font=F, fill=(255, 196, 92))
    if ref and (REF / ref).is_file():
        P.paste(Image.open(REF / ref).convert("RGB").resize((W, H)), (12, y + 32))
    else:
        d.text((24, y + 200), "(sem quadro do v3 citado)", font=F, fill=(200, 200, 200))
    P.paste(im.resize((W, H)), (24 + W, y + 32))
P.save(OUT / "correcoes_final.jpg", quality=86)
print("\n".join(linhas))
print("prancha", P.size)
