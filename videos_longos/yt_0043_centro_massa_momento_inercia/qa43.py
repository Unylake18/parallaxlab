"""yt_0043 · QA do preview v1 (handoff v1.1 §2 e §9). Lê os logs do render (log_<LOTE>.txt / log_seco_<LOTE>.txt),
os pontos do 3D (threejs/q3d/<LOTE>_960x540/<cena>/pontos.json) e as projeções do Manim (renders/v1/qa/al/<LOTE>.json),
e grava em renders/v1/qa/:
- prancha_alvos.jpg e comparacao/<k>.jpg (render 1920x1080 × alvo 1920x1080)
- alinhamento3d_v1.txt
- tamanhos_v1.txt
- gatilhos_v1.txt
- sobreposicoes_v1.txt, flash_por_quadro_v1.txt, palco_parado_v1.txt, grade_v1.txt, colunas_v1.txt,
  texto_em_mathtex_v1.txt, glyph_maps_v1.txt, origens_v1.txt, conta_inteira_v1.txt, tempos_render_v1.txt."""
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RODADA = os.environ.get("RODADA", "v1")
ALVO_DIR = f"yt_0043_quadros_alvo_{RODADA}"
COMPARA = "comparacao_v2" if RODADA == "v2" else "comparacao"
QA = AQUI / "renders" / RODADA / "qa"
QA.mkdir(parents=True, exist_ok=True)
(QA / ("comparacao_v2" if RODADA == "v2" else "comparacao")).mkdir(parents=True, exist_ok=True)

LOTES = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PS"]
ANC_DATA = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))
ORDEM = ANC_DATA["ordem"]
ANC = ANC_DATA["ancoras"]
INI_LOTE = {"PH": "H1", "PA": "A1", "PB1": "B1-1", "PB2": "B2-1", "PB3": "B3-1", "PB4": "B4-1", "PS": "S1"}

ALVOS = {
    "01_H1": "01_H1_lata_gira.jpg",
    "02_H2": "02_H2_conta_por_pedaco.jpg",
    "03_B1-1a": "03_B1-1a_tres_bolinhas.jpg",
    "04_B1-1b": "04_B1-1b_corpo.jpg",
    "05_B1-2": "05_B1-2_plano_equilibra.jpg",
    "06_B1-3a": "06_B1-3a_simetria.jpg",
    "07_B1-3b": "07_B1-3b_contraexemplo.jpg",
    "08_B2-1": "08_B2-1_taca_montar.jpg",
    "09_B2-2": "09_B2-2_taca_conta.jpg",
    "10_B3-1": "10_B3-1_momento_inercia.jpg",
    "11_B3-2": "11_B3-2_distancia_eixo.jpg",
    "12_B3-3": "12_B3-3_cilindro.jpg",
    "13_B3-4a": "13_B3-4a_bola_seno_cubo.jpg",
    "13b_B3-4b": "13b_B3-4b_bola_resultado.jpg",
    "14_B3-5": "14_B3-5_quem_gira.jpg",
    "15_B4-1": "15_B4-1_lata_integral_s.jpg",
    "16_B4-2": "16_B4-2_lata_zbarra.jpg",
    "17_B4-3": "17_B4-3_girar_integral_s.jpg",
    "18_B4-4": "18_B4-4_triangulo.jpg",
    "19_B4-5a": "19_B4-5a_secante_setima.jpg",
    "19b_B4-5b": "19b_B4-5b_momento_inercia.jpg",
    "20_B4-6": "20_B4-6_dois_numeros.jpg",
    "21_S2": "21_S2_eixo_parede.jpg",
}


def log(l):
    p = AQUI / f"log_{l}.txt"
    if not p.exists():
        p = AQUI / f"log_seco_{l}.txt"
    return p.read_text(encoding="utf-8", errors="replace").splitlines() if p.exists() else []


def linhas(tag):
    out = []
    for l in LOTES:
        for x in log(l):
            if x.startswith(tag):
                out.append((l, x))
    return out


def t_abs(lote, t):
    return ANC[INI_LOTE[lote]]["ini"] + t


def mmss(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


def fala_em(t0, t1):
    out = []
    for a in ORDEM:
        x = ANC[a]
        ws = x["fala"].split()
        for w, tw in zip(ws, x["t"]):
            ta = x["ini"] + tw
            if t0 <= ta <= t1:
                out.append(w)
    return " ".join(out)


def marcas():
    out = {}
    for l, x in linhas("[marca]"):
        _, nome, t = x.split()[:3]
        out[nome] = (l, float(t))
    return out


# ── 1. Comparação com alvos v1 e prancha consolidada ────────────────────────────────────────────────────────
def prancha():
    import av
    from PIL import Image, ImageDraw, ImageFont
    M = marcas()
    linhas_ = []
    try:
        fnt = ImageFont.truetype("arial.ttf", 24)
        fnt_s = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        fnt = fnt_s = None

    for k, arq in ALVOS.items():
        if k not in M:
            continue
        l, t = M[k]
        # Procura primeiro o still nativo 1920x1080 gerado por still.sh (renders/still/<LOTE>_<T>.png ou renders/v1/qa/still_<k>.png)
        still_1080 = QA / f"still_{k}.png"
        still_raw = AQUI / "renders" / "still" / f"{l}_{t:.3f}.png"
        if not still_raw.exists():
            still_raw = AQUI / "renders" / "still" / f"{l}_{t}.png"
        im = None
        if still_raw.exists():
            im = Image.open(still_raw).convert("RGB")
            im.save(still_1080)
        elif still_1080.exists():
            im = Image.open(still_1080).convert("RGB")
        else:
            mp4 = AQUI / f"media_{l}" / "videos" / "cena" / "540p15" / f"{l}.mp4"
            if mp4.exists():
                c = av.open(str(mp4))
                st = c.streams.video[0]
                alvo_q = int(round((t + 0.10) * 15))
                for i, fr in enumerate(c.decode(st)):
                    if i == alvo_q:
                        im = fr.to_image().convert("RGB")
                        break
                c.close()
                if im is not None:
                    im.save(still_1080)
        if im is None:
            continue

        al_full = Image.open(AQUI / "referencia" / ALVO_DIR / arq).convert("RGB")
        # Salva comparação individual em 1920x1080 (lado a lado 3840x1120)
        im_1080 = im if im.size == (1920, 1080) else im.resize((1920, 1080))
        cmp_im = Image.new("RGB", (3840, 1120), (12, 10, 30))
        dc = ImageDraw.Draw(cmp_im)
        dc.text((16, 8), f"{k}  RENDER ({l} {t:.2f} s = {mmss(t_abs(l, t))}) [{im.size[0]}x{im.size[1]}]", fill=(230, 230, 255), font=fnt)
        dc.text((1936, 8), f"{k}  ALVO {RODADA} (1920x1080)", fill=(230, 230, 255), font=fnt)
        cmp_im.paste(im_1080, (0, 40))
        cmp_im.paste(al_full, (1920, 40))
        cmp_im.save(QA / COMPARA / f"{k}.jpg", quality=92)

        linhas_.append((k, l, t, im.resize((960, 540)), al_full.resize((960, 540))))

    if linhas_:
        W, H, CAB = 960, 540, 34
        pr = Image.new("RGB", (2 * W, len(linhas_) * (H + CAB)), (12, 10, 30))
        d = ImageDraw.Draw(pr)
        for j, (k, l, t, a, b) in enumerate(linhas_):
            y = j * (H + CAB)
            d.text((10, y + 6), f"{k}  RENDER ({l} {t:.2f} s = {mmss(t_abs(l, t))})", fill=(230, 230, 255), font=fnt_s)
            d.text((W + 10, y + 6), f"{k}  ALVO {RODADA}", fill=(230, 230, 255), font=fnt_s)
            pr.paste(a, (0, y + CAB))
            pr.paste(b, (W, y + CAB))
        pr.save(QA / "prancha_alvos.jpg", quality=88)
    return [(k, l, t) for k, l, t, _, _ in linhas_]


# ── 2. Alinhamento 3D × Manim (px de 1080p) ─────────────────────────────────────────────────────────────────
def alinhamento():
    out = ["ALINHAMENTO 3D × MANIM (rótulos presos: ponto projetado pelo Manim × pontos.json do c43.js no mesmo quadro), px de 1080p", ""]
    pior_tot = 0.0
    for l in LOTES:
        p = QA / "al" / f"{l}.json"
        if not p.exists():
            continue
        al = json.loads(p.read_text(encoding="utf-8"))
        por = defaultdict(list)
        for lote, cena, fq, nome, x, y in al:
            por[cena].append((fq, nome, x, y))
        for cena, regs in por.items():
            pj = AQUI / "threejs" / "q3d" / f"{l}_960x540" / cena / "pontos.json"
            if not pj.exists():
                out.append(f"{l} {cena}: sem pontos.json")
                continue
            P = json.loads(pj.read_text(encoding="utf-8"))
            ds = []
            for fq, nome, x, y in regs:
                q = P.get(str(fq), {}).get(nome)
                if q is None:
                    continue
                ds.append(((x - q[0]) ** 2 + (y - q[1]) ** 2) ** .5)
            if ds:
                pior_tot = max(pior_tot, max(ds))
                out.append(f"{l:4s} {cena:12s} amostras={len(ds):6d}  médio={sum(ds) / len(ds):.3f} px  pior={max(ds):.3f} px  {'OK' if max(ds) <= 2 else 'ACIMA DE 2 px'}")
    out += ["", f"PIOR GERAL: {pior_tot:.3f} px (limite 2 px)"]
    (QA / f"alinhamento3d_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")
    return pior_tot


# ── 3. Atrasos de gatilhos (§9.3) ───────────────────────────────────────────────────────────────────────────
def gatilhos():
    gt = linhas("[gatilho]")
    sem = linhas("[gatilho-sem-frase]")
    out = [
        "SINCRONIZAÇÃO DE GATILHOS (handoff v1.1 §9.3: limite de atraso ≤ 0,30 s; gatilhos inexistentes = 0)",
        f"Total de gatilhos acionados: {len(gt)}",
        f"Gatilhos sem frase na narração: {len(sem)}",
        "",
        f"{'Lote':4s}  {'Âncora':6s}  {'Início(s)':>9s}  {'Previsto(s)':>11s}  {'Desvio(s)':>9s}  {'Status':8s}  Frase",
        "-" * 95,
    ]
    pior = 0.0
    acima = 0
    for l, x in gt:
        m = re.match(r"\[gatilho\] (\S+)\s+([\d.]+)s \(alvo\s+([\d.]+)s, atraso ([+-][\d.]+)s\) (.*)", x)
        if not m:
            continue
        aid, tini, talvo, desvio, frase = m.group(1), float(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(5)
        pior = max(pior, desvio)
        ok = desvio <= 0.30
        if not ok:
            acima += 1
        out.append(f"{l:4s}  {aid:6s}  {tini:9.2f}  {talvo:11.2f}  {desvio:+9.2f}  {'OK' if ok else 'ACIMA':8s}  {frase}")
    out += ["", f"Maior atraso medido: {pior:+.2f} s  |  Gatilhos > 0,30 s: {acima}  |  Sem frase: {len(sem)}"]
    (QA / f"gatilhos_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")
    return len(sem), acima, pior


# ── 4. Tamanhos reais das letras (§6.1) ─────────────────────────────────────────────────────────────────────
def tamanhos():
    tm = linhas("[tam]")
    out = [
        "TAMANHOS DE TIPOGRAFIA (handoff v1.1 §6.1: referência 1920x1080; principal 50–54 px, secundária 44–46 px, B4 40–42 px, legendas/chips 30 px, mínimo absoluto 26 px)",
        f"Total de elementos registrados: {len(tm)}",
        "",
    ]
    abaixo = []
    por_aid = defaultdict(list)
    for l, x in tm:
        m = re.match(r"\[tam\] (\S+) (\S+) ([FT]) ([\d.]+) (.*)", x)
        if not m:
            continue
        lote, aid, tipo, sz, tx = m.group(1), m.group(2), m.group(3), float(m.group(4)), m.group(5)
        por_aid[(lote, aid)].append((tipo, sz, tx))
        if sz < 26 - 1e-6:
            abaixo.append((lote, aid, tipo, sz, tx))
    for (lote, aid), itens in por_aid.items():
        szs = [s for _, s, _ in itens]
        out.append(f"  {lote:4s} {aid:6s}  itens={len(itens):3d}  min={min(szs):.0f} px  max={max(szs):.0f} px")
    out += ["", f"Elementos abaixo do mínimo absoluto (26 px): {len(abaixo)}"]
    for it in abaixo:
        out.append(f"  ABAIXO: {it}")
    (QA / f"tamanhos_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")
    return len(abaixo)


# ── 5. R5, R6, flash ───────────────────────────────────────────────────────────────────────────────────────
def sobreposicoes():
    r5 = linhas("[R5]")
    r5v = linhas("[R5V]")
    r6 = linhas("[R6]")
    c3 = linhas("[3dcanto]")
    out = ["R5 · SOBREPOSIÇÃO (a cada 0,2 s, inclusive durante animações e voos)",
           f"R5 (parado ou em animação, fora de voo): {len(r5)}"] + [f"  {l} {x}" for l, x in r5]
    out += ["", f"R5V (glifo EM VOO cruzando texto parado): {len(r5v)}"] + [f"  {l} {x}" for l, x in r5v]
    out += ["", f"R6 (margem de 48 px; item fora do seu painel/cartão): {len(r6)}"] + [f"  {l} {x}" for l, x in r6]
    out += ["", f"EIXO 3D × CANTO: {len(c3)}"] + [f"  {l} {x}" for l, x in c3]
    (QA / f"sobreposicoes_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")
    return len(r5), len(r5v), len(r6), len(c3)


def flash():
    fl = linhas("[flash]")
    tot = linhas("[flash-total]")
    out = ["FLASH POR QUADRO (fórmula de caneta visível antes de ser escrita)", f"eventos: {len(fl)}"]
    out += [f"  {l} {x}" for l, x in fl[:200]] + ["", "totais por lote:"] + [f"  {x}" for _, x in tot]
    (QA / f"flash_por_quadro_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")
    return len(fl)


# ── 6. Palco parado / vazio ─────────────────────────────────────────────────────────────────────────────────
def palco():
    vz = linhas("[vazio]")
    sem2 = [(l, x) for l, x in linhas("[grade]") if "canto2=NAO" in x]
    out = ["PALCO PARADO / VAZIO", f"palco vazio > 0,5 s: {len(vz)}"] + [f"  {l} {x}" for l, x in vz]
    out += ["", f"canto sem a linha 2: {len(sem2)}"] + [f"  {l} {x}" for l, x in sem2]
    (QA / f"palco_parado_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")
    return len(vz), len(sem2)


# ── 7. Grade (papel) ────────────────────────────────────────────────────────────────────────────────────────
def grade():
    c = Counter()
    sem = []
    for l, x in linhas("[grade]"):
        tipo = x.split()[4]
        c[tipo] += 1
        if tipo == "SEM-GRADE":
            sem.append(f"  {l} {x}")
    out = ["GRADE (G1: papel em 100% das cenas 2D e 3D, exceto CTA)",
           *[f"  {k}: {v} s" for k, v in sorted(c.items())], "", f"SEM-GRADE fora do CTA: {len(sem)}", *sem]
    (QA / f"grade_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")
    return c, len(sem)


# ── 8. Colunas ───────────────────────────────────────────────────────────────────────────────────────────────
def colunas():
    mx = {}
    for l, x in linhas("[coluna]"):
        m = re.search(r"\[coluna\] (\S+) (\S+) [\d.]+ (\S+) linhas=(\d+) chips=(\d+) base=(\d+) folga=(-?\d+)", x)
        if not m:
            continue
        k = (m.group(1), m.group(3))
        n, ch, folga = int(m.group(4)), int(m.group(5)), int(m.group(7))
        a = mx.get(k, (0, 0, 9999))
        mx[k] = (max(a[0], n), max(a[1], ch), min(a[2], folga))
    out = ["COLUNAS: máximo de linhas por etapa (≤ 7, chips fora da conta) e folga do rodapé (≥ 40 px)"]
    for (l, nome), (n, ch, f) in mx.items():
        lim = 7
        out.append(f"  {l:4s} {nome:14s} linhas={n} chips/legendas={ch} folga={f} px  {'OK' if n <= lim and f >= 40 else 'VER'}")
    (QA / f"colunas_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")
    return mx


# ── 9. Texto em MathTex ─────────────────────────────────────────────────────────────────────────────────────
def texto_mathtex():
    out = ["TEXTO EM MATHTEX (critério 10): \\text{…} com mais de uma palavra = 0; tfrac = 0"]
    n_txt, n_tf = 0, 0
    for p in sorted(AQUI.glob("sec_*.py")):
        for i, x in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for m in re.finditer(r"\\text\{([^}]*)\}", x):
                if len(m.group(1).split()) > 1:
                    n_txt += 1
                    out.append(f"  {p.name}:{i} \\text{{{m.group(1)}}}")
            if "tfrac" in x:
                n_tf += 1
                out.append(f"  {p.name}:{i} tfrac")
    out += [f"\\text{{…}} com mais de uma palavra: {n_txt}", f"tfrac: {n_tf}"]
    (QA / f"texto_em_mathtex_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")
    return n_txt, n_tf


# ── 10. Glyph maps GM1–GM18 (§7.2) ──────────────────────────────────────────────────────────────────────────
def glyph_maps():
    g = linhas("[gm]")
    vistos = set()
    out = ["GLYPH MAPS (GM1–GM18 obrigatórios, MF-Tools TransformByGlyphMap)", ""]
    for l, x in g:
        m = re.search(r"mapa=(\d+)", x)
        if m:
            vistos.add(int(m.group(1)))
        out.append(f"  {l} {x}")
    falta = [n for n in range(1, 19) if n not in vistos]
    out += ["", f"mapas presentes: {sorted(vistos)}  faltando: {falta or 'nenhum'}",
            f"avisos (glifo de B mapeado duas vezes): {len(linhas('[gm] AVISO'))}"]
    (QA / f"glyph_maps_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")
    return sorted(vistos), falta


# ── 11. Origens / voos ──────────────────────────────────────────────────────────────────────────────────────
def origens():
    v = linhas("[voo]")
    o = linhas("[origem]")
    out = ["ORIGENS / VOOS (TransformFromCopy)", ""] + [f"  {l} {x}" for l, x in v] + [""] + [f"  {l} {x}" for l, x in o]
    (QA / f"origens_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")
    return len(v)


# ── 12. Conta inteira C1–C10 (§7) ───────────────────────────────────────────────────────────────────────────
def contas():
    d = defaultdict(list)
    for l, x in linhas("[degrau]"):
        m = re.match(r"\[degrau\] (\S+) (\S+)\s+([\d.]+)\s+([\d.]+) (\S+) :: (.*)", x)
        if m:
            d[m.group(5)].append((m.group(1), m.group(2), float(m.group(4)), m.group(6)))
    out = ["CONTA INTEIRA (degraus C1–C10)", ""]
    for k in sorted(d):
        out.append(f"{k}:")
        for l, aid, t, desc in d[k]:
            out.append(f"  {mmss(t_abs(l, t))}  {aid:5s} {desc}")
        out.append("")
    (QA / f"conta_inteira_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")
    return sum(len(v) for v in d.values())


# ── 13. Tempos de render ────────────────────────────────────────────────────────────────────────────────────
def tempos():
    out = ["TEMPOS DE RENDER POR LOTE (960×540, 15 fps) e custo por quadro das cenas 3D", ""]
    for l in LOTES:
        r = [x for x in log(l) if x.startswith("[render]")]
        t = [x for x in log(l) if x.startswith("[tempo] total")]
        p3 = AQUI / f"log_3d_{l}.txt"
        j = None
        if p3.exists():
            for x in p3.read_text(encoding="utf-8", errors="replace").splitlines():
                if x.startswith("{"):
                    j = json.loads(x)
        tr = AQUI / f"tempo3d_{l}.txt"
        out.append(f"{l:4s} {r[-1] if r else '(sem render)'}  {t[-1] if t else ''}"
                   + (f"  | 3D: {j['renderizados']} quadros renderizados + {j['copiados']} copiados em {j['segundos']} s = {j['s_por_quadro']} s/quadro" if j else "")
                   + (f"  | pedidos+3D+Manim: {tr.read_text().strip()}" if tr.exists() else ""))
    (QA / f"tempos_render_{RODADA}.txt").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    res = {}
    if "--sem-prancha" not in sys.argv:
        res["prancha"] = prancha()
    res["alinhamento"] = alinhamento()
    res["gatilhos"] = gatilhos()
    res["tamanhos"] = tamanhos()
    res["sobreposicoes"] = sobreposicoes()
    res["flash"] = flash()
    res["palco"] = palco()
    res["grade"] = grade()
    res["colunas"] = colunas()
    res["texto"] = texto_mathtex()
    res["gm"] = glyph_maps()
    res["origens"] = origens()
    res["contas"] = contas()
    tempos()
    print(json.dumps({k: (v if not isinstance(v, Counter) else dict(v)) for k, v in res.items() if k not in ("colunas",)}, ensure_ascii=False, default=str)[:3000])
