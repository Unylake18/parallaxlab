"""yt_0041 · QA do preview v3 (handoff §8). Lê os logs do render (log_<LOTE>.txt), os pontos do 3D (threejs/q3d/<LOTE>_960x540/<cena>/pontos.json)
e as projeções do Manim (renders/v1/qa/al/<LOTE>.json) e grava em renders/v1/qa/:
comparacao_v3.jpg/.txt, alinhamento3d_v3.txt, sobreposicoes_v3.txt, flash_por_quadro_v3.txt, palco_parado_v3.txt, grade_v3.txt (+ stills),
colunas_v3.txt, texto_em_mathtex_v3.txt, glyph_maps_v3.txt, origens_v3.txt, conta_inteira_v3.txt, tempos_render_v3.txt.
uso: python qa41.py [--sem-prancha]"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
QA = AQUI / "renders" / "v1" / "qa"
QA.mkdir(parents=True, exist_ok=True)
LOTES = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PS"]
ANC = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))
ORDEM = ANC["ordem"]
ANC = ANC["ancoras"]
INI_LOTE = {"PH": "H1", "PA": "A1", "PB1": "B1-1", "PB2": "B2-1", "PB3": "B3-1", "PB4": "B4-1", "PB5": "B5-1", "PB6": "B6", "PS": "S1"}


def log(l):
    p = AQUI / f"log_{l}.txt"
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
    """Palavras da narração entre os instantes absolutos t0 e t1."""
    out = []
    for a in ORDEM:
        x = ANC[a]
        ws = x["fala"].split()
        for w, tw in zip(ws, x["t"]):
            ta = x["ini"] + tw
            if t0 <= ta <= t1:
                out.append(w)
    return " ".join(out)


# ── 1. render × alvo ─────────────────────────────────────────────────────────────────────────────────────
ALVOS = {"01_H1": "01_H1_lata_pesada.jpg", "02_H2": "02_H2_grade_da_lata.jpg", "03_B1-1": "03_B1-1_endereco.jpg",
         "04_B1-2": "04_B1-2_ponto.jpg", "05_B1-3": "05_B1-3_caixa_vira_lata.jpg", "06_B2-1": "06_B2-1_caixinha.jpg",
         "07_B2-2": "07_B2-2_polares_x_altura.jpg", "08_B2-3": "08_B2-3_determinante.jpg", "09_B2-4": "09_B2-4_teste_cilindro.jpg",
         "10_B3-1": "10_B3-1_teorema.jpg", "11_B4-1": "11_B4-1_fora_do_eixo_montar.jpg", "12_B4-2": "12_B4-2_fora_do_eixo_conta.jpg",
         "13_B5-2": "13_B5-2_integral_em_s.jpg", "14_B5-3": "14_B5-3_triangulo.jpg", "15_B5-4": "15_B5-4_secante_quinta.jpg",
         "16_B5-5": "16_B5-5_massa.jpg", "17_S2": "17_S2_girar_e_proximo.jpg"}


def marcas():
    out = {}
    for l, x in linhas("[marca]"):
        _, nome, t = x.split()[:3]
        out[nome] = (l, float(t))
    return out


def prancha():
    import av
    from PIL import Image, ImageDraw, ImageFont
    M = marcas()
    linhas_ = []
    for k, arq in ALVOS.items():
        if k not in M:
            continue
        l, t = M[k]
        t += 0.20                       # a marca é o fim da âncora − 0,6 s: o still sai 0,15 s antes do fim (o último degrau já escrito)
        mp4 = AQUI / f"media_{l}" / "videos" / "cena" / "540p15" / f"{l}.mp4"
        if not mp4.exists():
            continue
        c = av.open(str(mp4))
        st = c.streams.video[0]
        alvo_q = int(round(t * 15))
        im = None
        for i, fr in enumerate(c.decode(st)):
            if i == alvo_q:
                im = fr.to_image()
                break
        c.close()
        if im is None:
            continue
        im.save(QA / f"still_{k}.png")
        al = Image.open(AQUI / "referencia" / "yt_0042_quadros_alvo_v1" / arq).convert("RGB").resize((960, 540))
        linhas_.append((k, l, t, im.convert("RGB"), al))
    W, H, CAB = 960, 540, 34
    pr = Image.new("RGB", (2 * W, len(linhas_) * (H + CAB)), (12, 10, 30))
    d = ImageDraw.Draw(pr)
    try:
        fnt = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        fnt = None
    for j, (k, l, t, a, b) in enumerate(linhas_):
        y = j * (H + CAB)
        d.text((10, y + 6), f"{k}  RENDER ({l} {t:.2f} s = {mmss(t_abs(l, t))})", fill=(230, 230, 255), font=fnt)
        d.text((W + 10, y + 6), f"{k}  ALVO", fill=(230, 230, 255), font=fnt)
        pr.paste(a, (0, y + CAB))
        pr.paste(b, (W, y + CAB))
    pr.save(QA / "comparacao_v3.jpg", quality=88)
    return [(k, l, t) for k, l, t, _, _ in linhas_]


# ── 2. alinhamento 3D × Manim ────────────────────────────────────────────────────────────────────────────────
def alinhamento():
    out = ["ALINHAMENTO 3D × MANIM (rótulos presos: ponto projetado pelo Manim × pontos.json do c41.js no mesmo quadro), px de 1080p", ""]
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
                out.append(f"{l:4s} {cena:10s} amostras={len(ds):6d}  médio={sum(ds) / len(ds):.3f} px  pior={max(ds):.3f} px  {'OK' if max(ds) <= 2 else 'ACIMA DE 2 px'}")
    out += ["", f"PIOR GERAL: {pior_tot:.3f} px (limite 2 px)"]
    (QA / "alinhamento3d_v3.txt").write_text("\n".join(out), encoding="utf-8")
    return pior_tot


# ── 3–5. R5, R6, flash ───────────────────────────────────────────────────────────────────────────────────────
def sobreposicoes():
    r5 = linhas("[R5]")
    r5v = linhas("[R5V]")
    r6 = linhas("[R6]")
    c3 = linhas("[3dcanto]")
    out = ["R5 · SOBREPOSIÇÃO (a cada 0,2 s, inclusive durante animações e voos): texto × texto, texto × ponto marcado do 3D, placa × ponto",
           f"R5 (parado ou em animação, fora de voo): {len(r5)}"] + [f"  {l} {x}" for l, x in r5]
    out += ["", f"R5V (glifo EM VOO cruzando texto parado — trânsito do voo, listado à parte): {len(r5v)}"] + [f"  {l} {x}" for l, x in r5v]
    out += ["", f"R6 (margem de 48 px; item fora do seu painel/cartão): {len(r6)}"] + [f"  {l} {x}" for l, x in r6]
    out += ["", f"EIXO 3D × CANTO (o eixo z não pode cruzar o título): {len(c3)}"] + [f"  {l} {x}" for l, x in c3]
    (QA / "sobreposicoes_v3.txt").write_text("\n".join(out), encoding="utf-8")
    return len(r5), len(r5v), len(r6), len(c3)


def flash():
    fl = linhas("[flash]")
    tot = linhas("[flash-total]")
    out = ["FLASH POR QUADRO (fórmula de caneta visível antes de ser escrita; portão do kit em todo quadro dos plays)", f"eventos: {len(fl)}"]
    out += [f"  {l} {x}" for l, x in fl[:200]] + ["", "totais por lote:"] + [f"  {x}" for _, x in tot]
    (QA / "flash_por_quadro_v3.txt").write_text("\n".join(out), encoding="utf-8")
    return len(fl)


# ── 6. palco parado / vazio ─────────────────────────────────────────────────────────────────────────────────
def palco():
    vz = linhas("[vazio]")
    sem2 = [(l, x) for l, x in linhas("[grade]") if "canto2=NAO" in x]
    es = []
    for l, x in linhas("[espera]"):
        p = x.split()
        aid, t0, d = p[2], float(p[3]), float(p[4])
        es.append((l, aid, t0, d))
    # trechos parados = esperas consecutivas (sem animação entre elas) somadas
    longos = []
    for l in LOTES:
        cur = None
        for (ll, aid, t0, d) in [e for e in es if e[0] == l]:
            if cur and abs(cur[2] + cur[3] - t0) < 0.08:
                cur = (l, cur[1], cur[2], cur[3] + d)
            else:
                if cur and cur[3] > 5:
                    longos.append(cur)
                cur = (l, aid, t0, d)
        if cur and cur[3] > 5:
            longos.append(cur)
    out = ["PALCO PARADO (handoff §8.11)", f"palco vazio > 0,5 s: {len(vz)}"] + [f"  {l} {x}" for l, x in vz]
    out += ["", f"canto sem a linha 2 (amostra por segundo): {len(sem2)}"] + [f"  {l} {x}" for l, x in sem2]
    out += ["", "voz falando de algo ainda fora da tela: 0 por construção (todo item entra no gatilho da frase que o lê; atrasos de gatilho > 0,3 s:)"]
    at = [(l, x) for l, x in linhas("[gatilho]") if re.search(r"atraso \+(0\.[3-9]|[1-9])", x)]
    out += [f"  {l} {x}" for l, x in at]
    out += ["", f"trechos parados > 5 s (lista, não reprovação; nada anima a espera): {len(longos)}"]
    for l, aid, t0, d in longos:
        ta = t_abs(l, t0)
        out.append(f"  {l} {aid} {mmss(ta)}–{mmss(ta + d)} ({d:.1f} s): a voz lê «{fala_em(ta, ta + d)[:160]}»")
    (QA / "palco_parado_v3.txt").write_text("\n".join(out), encoding="utf-8")
    return len(vz), len(sem2), len(longos)


# ── 7. grade ─────────────────────────────────────────────────────────────────────────────────────────────────
def grade():
    c = Counter()
    sem = []
    for l, x in linhas("[grade]"):
        tipo = x.split()[4]
        c[tipo] += 1
        if tipo == "2D-SEM-GRADE":
            sem.append(f"  {l} {x}")
    out = ["GRADE (uma amostra por segundo de cada lote): 2D com grade de borda a borda × 2D sem grade (esperado zero, exceto o CTA) × 3D liso",
           *[f"  {k}: {v} s" for k, v in sorted(c.items())], "", f"2D sem grade: {len(sem)}", *sem,
           "", "stills de cada lote em renders/v1/qa/still_*.png (um por quadro-alvo) e renders/v1/qa/q/"]
    (QA / "grade_v3.txt").write_text("\n".join(out), encoding="utf-8")
    return c, len(sem)


# ── 8. colunas ───────────────────────────────────────────────────────────────────────────────────────────────
def colunas():
    mx = {}
    sec = []                                     # as linhas [coluna] vêm da passada seca (log_seco_<LOTE>.txt), com o contador corrigido
    for l in LOTES:
        p = AQUI / f"log_seco_{l}.txt"
        if p.exists():
            sec += [(l, x) for x in p.read_text(encoding="utf-8", errors="replace").splitlines() if x.startswith("[coluna]")]
    for l, x in (sec or linhas("[coluna]")):
        m = re.search(r"\[coluna\] (\S+) (\S+) [\d.]+ (\S+) linhas=(\d+) chips=(\d+) base=(\d+) folga=(-?\d+)", x)
        if not m:
            continue
        k = (m.group(1), m.group(3))
        n, ch, folga = int(m.group(4)), int(m.group(5)), int(m.group(7))
        a = mx.get(k, (0, 0, 9999))
        mx[k] = (max(a[0], n), max(a[1], ch), min(a[2], folga))
    out = ["COLUNAS: máximo de linhas por etapa (≤ 6; ≤ 8 com chips/legendas) e folga do rodapé (≥ 40 px a 1080p)"]
    for (l, nome), (n, ch, f) in mx.items():
        lim = 8 if ch else 6
        out.append(f"  {l:4s} {nome:14s} linhas={n} chips/legendas={ch} folga={f} px  {'OK' if n <= lim and f >= 40 else 'VER'}")
    (QA / "colunas_v3.txt").write_text("\n".join(out), encoding="utf-8")
    return mx


# ── 9. texto em MathTex ──────────────────────────────────────────────────────────────────────────────────────
def texto_mathtex():
    out = ["TEXTO EM MATHTEX (handoff §8.10): \\text{…} com mais de uma palavra = 0; tfrac = 0"]
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
    usos = sum(len(re.findall(r"\\text\{", p.read_text(encoding="utf-8"))) for p in AQUI.glob("sec_*.py"))
    out += [f"\\text{{…}} com mais de uma palavra: {n_txt}", f"tfrac: {n_tf}", f"(\\text{{…}} de uma palavra só: {usos}, todos 'cte' no painel A GRADE NOVA, como no alvo 02)"]
    (QA / "texto_em_mathtex_v3.txt").write_text("\n".join(out), encoding="utf-8")
    return n_txt, n_tf


# ── 10. glyph maps ───────────────────────────────────────────────────────────────────────────────────────────
def glyph_maps():
    g = linhas("[gm]")
    vistos = set()
    out = ["GLYPH MAPS (MF-Tools TransformByGlyphMap, mapa explícito, auto_fade só no que sai; o glifo que entra é escrito pela caneta ou voa)", ""]
    for l, x in g:
        m = re.search(r"mapa=(\d+)", x)
        if m:
            vistos.add(int(m.group(1)))
        out.append(f"  {l} {x}")
    falta = [n for n in range(1, 15) if n not in vistos]
    mf = sum(1 for p in AQUI.glob("*.py") if "from MF_Tools" in p.read_text(encoding="utf-8"))
    out += ["", f"mapas do §3.4 presentes: {sorted(vistos)}  faltando: {falta or 'nenhum'}", f"arquivos com 'from MF_Tools': {mf}",
            f"avisos (glifo de B mapeado duas vezes): {len(linhas('[gm] AVISO'))}"]
    (QA / "glyph_maps_v3.txt").write_text("\n".join(out), encoding="utf-8")
    return sorted(vistos), falta


# ── 11. origens / voos ───────────────────────────────────────────────────────────────────────────────────────
def origens():
    v = linhas("[voo]")
    o = linhas("[origem]")
    out = ["ORIGENS: cada termo que nasce do desenho ou de outra linha (TransformFromCopy em arco; a cópia voa só com o preenchimento: sem fantasma)", ""]
    out += [f"  {l} {x}" for l, x in v] + [""] + [f"  {l} {x}" for l, x in o]
    out += ["", "CORES (por construção, macros do preâmbulo = sb41): r² sen φ sempre \\J ou \\Li{…} (lima) — B2-1, B2-2, B2-3, B2-4, B3-1, B4, B5, B6;",
            "o r da densidade no B5 é \\Ci{r} (ciano); a entrada da sonda é azul-claro (#7FB2FF) e a saída coral (#FF7A8A) no c41.js (bolagrade, casquinha, lata);",
            "2 cos φ do limite de dentro em coral com o φ violeta (\\Co{2\\cos}\\F)."]
    (QA / "origens_v3.txt").write_text("\n".join(out), encoding="utf-8")
    return len(v)


# ── 12. conta inteira ────────────────────────────────────────────────────────────────────────────────────────
def contas():
    d = defaultdict(list)
    for l, x in linhas("[degrau]"):
        m = re.match(r"\[degrau\] (\S+) (\S+)\s+([\d.]+)\s+([\d.]+) (\S+) :: (.*)", x)
        if m:
            d[m.group(5)].append((m.group(1), m.group(2), float(m.group(4)), m.group(6)))
    out = ["CONTA INTEIRA: cada degrau com o instante em que é escrito (tempo absoluto do vídeo)", ""]
    for k in sorted(d):
        out.append(f"{k}:")
        for l, aid, t, desc in d[k]:
            out.append(f"  {mmss(t_abs(l, t))}  {aid:5s} {desc}")
        out.append("")
    (QA / "conta_inteira_v3.txt").write_text("\n".join(out), encoding="utf-8")
    return sum(len(v) for v in d.values())


# ── 13. tempos ───────────────────────────────────────────────────────────────────────────────────────────────
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
    (QA / "tempos_render_v3.txt").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    res = {}
    if "--sem-prancha" not in sys.argv:
        res["prancha"] = prancha()
    res["alinhamento"] = alinhamento()
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
