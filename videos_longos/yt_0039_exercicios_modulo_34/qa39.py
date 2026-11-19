"""yt_0039 · QA do preview v1 (handoff §8). Lê os logs do render (log_<LOTE>.txt), o MP4 concatenado e os pontos 3D, e grava em renders/v1/qa/:
sobreposicoes_v1.txt, alinhamento3d_v1.txt, flash_por_quadro_v1.txt, palco_parado_v1.txt, texto_em_mathtex_v1.txt, glyph_maps_v1.txt,
origens_v1.txt, conta_inteira_v1.txt, grade_tela_v1.txt, tempos_render_v1.txt e a prancha comparacao_v1.jpg.
uso: python qa39.py   (depois de montar.py)"""
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import os as _os
RV = _os.environ.get("RODADA", "v2")
AQUI = Path(__file__).resolve().parent
QA = AQUI / "renders" / RV / "qa"
QA.mkdir(parents=True, exist_ok=True)
LOTES = ["PH", "PA", "PE1", "PE2", "PE3", "PE4", "PE5", "PE6", "PS"]
MP4 = AQUI / "renders" / RV / f"yt_0039_preview_{RV}_540p15.mp4"
FPS = 15
REF = AQUI / "referencia" / "yt_0039_quadros_alvo_v1"
LOG = {c: (AQUI / f"log_{c}.txt").read_text(encoding="utf-8", errors="replace") for c in LOTES if (AQUI / f"log_{c}.txt").exists()}
INI = json.loads((AQUI / "renders" / RV / "inicio_lotes.json").read_text(encoding="utf-8"))      # início (s) de cada lote no MP4


def linhas(tag):
    out = []
    for c in LOTES:
        for ln in LOG.get(c, "").splitlines():
            if ln.startswith(tag):
                out.append((c, ln))
    return out


def grava(nome, txt):
    (QA / nome).write_text(txt, encoding="utf-8")
    print(f"[qa] {nome}")


def ts(c, t_lote):
    s = INI[c] + t_lote
    return f"{int(s // 60)}:{s % 60:05.2f}"


# ── R5 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
def r5():
    L = ["R5 · sobreposição (handoff §8.3). Amostragem: o QA do kit (R5 v2 da caixa de texto × texto/traço/borda, folga 10 px) roda em cada gatilho e",
         "a cada play/espera, INCLUSIVE durante as animações (relógio do lote, ≤ 0,5 s entre amostras nas animações longas). Glifo em voo, guia do",
         "próprio rótulo e placa do próprio rótulo não contam. Escala: px de 1080p.",
         "v2 §7.1 (a única exclusão nova): o voo sobre a PRÓPRIA fonte (a cópia partindo do texto de onde nasceu) e sobre o PRÓPRIO destino",
         "(a linha onde pousa) não conta: é o próprio movimento do termo; o voo sobre QUALQUER outro texto conta e está listado abaixo.", ""]
    tot = Counter()
    ex = defaultdict(list)
    for c, ln in linhas("[R5L]") + linhas("[R5] "):
        m = re.match(r"\[R5L?\] (\S+)\s+([\d.]+)s (.*)", ln)
        if not m:
            continue
        aid, t, resto = m.groups()
        chave = re.sub(r"caixa.*", "", resto).strip()
        tot[(c, aid, chave)] += 1
        if len(ex[(c, aid, chave)]) < 3:
            ex[(c, aid, chave)].append(ts(c, float(t)))
    L.append(f"Total de amostras com colisão: {sum(tot.values())} em {len(tot)} pares distintos.")
    L.append("")
    for (c, aid, ch), n in sorted(tot.items(), key=lambda kv: -kv[1]):
        L.append(f"{c:4s} {aid:6s} {n:5d}×  {ch[:120]}   (ex.: {', '.join(ex[(c, aid, ch)])})")
    grava(f"sobreposicoes_{RV}.txt", "\n".join(L) + "\n")


# ── flash ────────────────────────────────────────────────────────────────────────────────────────────────────────────
def flash():
    L = ["FLASH POR QUADRO (handoff §8.5): portão do kit (_porta_flash) em cada quadro de cada play: fórmula de caneta visível antes de ser escrita.", ""]
    for c in LOTES:
        m = re.findall(r"\[flash-total\] \S+ (\d+)", LOG.get(c, ""))
        L.append(f"{c:4s} flash = {m[-1] if m else '?'}")
    ev = linhas("[flash]")
    L += ["", f"Eventos: {len(ev)}"] + [f"  {c} {ln}" for c, ln in ev[:60]]
    grava(f"flash_por_quadro_{RV}.txt", "\n".join(L) + "\n")


# ── texto em MathTex / tfrac ─────────────────────────────────────────────────────────────────────────────────────────
def texto():
    L = ["TEXTO EM MathTex (handoff §8.8): todo \\text{…} nas fontes desta unidade, e grep tfrac.", ""]
    n = 0
    for f in sorted(AQUI.glob("*.py")):
        if f.name.startswith("qa"):
            continue
        for i, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if f.name.startswith("sec_") and re.search(r"\\text\{", ln):
                L.append(f"{f.name}:{i}: {ln.strip()[:120]}")
                n += 1
    L.append(f"\\text{{…}} nas seções: {n}")
    nt = sum(len(re.findall(r"tfrac", f.read_text(encoding="utf-8"))) for f in AQUI.glob("sec_*.py")) + \
        sum(len(re.findall(r"tfrac", f.read_text(encoding="utf-8"))) for f in [AQUI / "k39.py"])
    L.append(f"grep -n tfrac (seções + k39.py) = {nt}")
    L.append("Observação: o kit copiado define macros com \\textcolor (cor, não texto) e o \\mathrm{kg} da massa do E2 é unidade, não frase.")
    grava(f"texto_em_mathtex_{RV}.txt", "\n".join(L) + "\n")


# ── glyph maps ──────────────────────────────────────────────────────────────────────────────────────────────────────
def gmaps():
    L = ["GLYPH MAPS (handoff §8.6): toda passagem TransformByGlyphMap (MF-Tools 1.4.9, `from MF_Tools import TransformByGlyphMap` em lib39.py),",
         "com o nº do grupo do §3.4 (0 = degrau de cadeia sem número próprio), o bloco, o tempo no MP4 e a nota do mapa. Nenhuma função própria de mapa.", ""]
    por = Counter()
    for c, ln in linhas("[gmap"):
        m = re.match(r"\[gmap(\d+)\] (\S+) (\S+) ([\d.]+)s (.*?) :: (.*)", ln)
        if not m:
            continue
        n, lote, aid, t, nota, resto = m.groups()
        por[int(n)] += 1
        L.append(f"GM{int(n):02d}  {aid:6s} {ts(c, float(t) + float(re.findall(r'\[ancora\] ' + re.escape(aid) + r' ([\d.]+)', LOG[c])[0])) if re.findall(r'\[ancora\] ' + re.escape(aid) + r' ([\d.]+)', LOG[c]) else t}  {nota[:90]}")
    L += ["", "Passagens por grupo: " + ", ".join(f"GM{k:02d}={v}" for k, v in sorted(por.items())),
          "Grupos do §3.4 com passagem: " + ", ".join(str(k) for k in sorted(k for k in por if k > 0)),
          "Grupos sem passagem numerada: " + ", ".join(str(k) for k in range(1, 25) if k not in por)]
    grava(f"glyph_maps_{RV}.txt", "\n".join(L) + "\n")


def ini_aid(c, aid):
    m = re.findall(r"\[ancora\] " + re.escape(aid) + r" ([\d.]+)", LOG.get(c, ""))
    return float(m[0]) if m else 0.0


# ── origens e contas ───────────────────────────────────────────────────────────────────────────────────────────────
def origens():
    L = ["ORIGENS (handoff §8.11): de onde nasce cada número/símbolo. [origem] = anotação do voo obrigatório; [voo] = termo que pousou por voo", "(TransformFromCopy) com o seu tempo na âncora.", ""]
    for c, ln in linhas("[origem]") + linhas("[voo]"):
        L.append(f"{c:4s} {ln[:170]}")
    grava(f"origens_{RV}.txt", "\n".join(L) + "\n")


def contas():
    L = ["CONTA INTEIRA (handoff §8.7): cada degrau escrito na coluna, com o tempo (s desde o início da âncora), por etapa C1a … C6e do §3.1 da proposta.", ""]
    por = defaultdict(list)
    for c, ln in linhas("[degrau]"):
        m = re.match(r"\[degrau\] (\S+) (\S+)\s+([\d.]+)s (\S+) :: (.*)", ln)
        if m:
            lote, aid, t, conta, desc = m.groups()
            por[conta].append(f"   {aid:6s} {float(t):6.2f}s  {desc}")
    for k in sorted(por):
        L.append(k)
        L += por[k]
        L.append("")
    grava(f"conta_inteira_{RV}.txt", "\n".join(L) + "\n")


# ── tempos ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def tempos():
    L = ["TEMPOS DE RENDER (registro; handoff §8.14). Preview 960×540 / 15 fps.", ""]
    for c in LOTES:
        r = re.findall(r"\[render\] \S+ (\d+)s", LOG.get(c, ""))
        q = re.findall(r"\[tempo\] total ([\d.]+)s \((\d+) quadros\)", LOG.get(c, ""))
        L.append(f"{c:4s} render {r[-1] if r else '?':>5}s  duração {q[-1][0] if q else '?':>7}s  quadros {q[-1][1] if q else '?'}")
        t3 = AQUI / f"log_3d_{c}.txt"
        if t3.exists():
            js = [l for l in t3.read_text(encoding="utf-8", errors="replace").splitlines() if l.startswith("{")]
            if js:
                d = json.loads(js[-1])
                L.append(f"      3D Three.js: {d['renderizados']} quadros renderizados + {d['copiados']} copiados em {d['segundos']} s ({d['s_por_quadro']} s/quadro, {d['res']})")
    grava(f"tempos_render_{RV}.txt", "\n".join(L) + "\n")


# ── quadros do MP4 ─────────────────────────────────────────────────────────────────────────────────────────────────
def quadros_mp4():
    c = av.open(str(MP4))
    for f in c.decode(video=0):
        yield f.to_ndarray(format="rgb24")


def palco_parado():
    """Palco (máscara sem a coluna x ≥ 545 px e sem o canto y < 95 px, a 960×540): trecho em que < 40 px mudam > 8 níveis ao longo de 3 s."""
    W = 3 * FPS
    hist = []
    paradas = []
    ini = None
    for i, a in enumerate(quadros_mp4()):
        g = a[95:, :545].astype(np.int16).mean(2)
        hist.append(g)
        if len(hist) > W + 1:
            hist.pop(0)
        if len(hist) == W + 1:
            d = np.abs(hist[-1] - hist[0]) > 8
            mud = int(d.sum())
            if mud < 40:
                if ini is None:
                    ini = i - W
            elif ini is not None:
                paradas.append((ini, i - 1))
                ini = None
    if ini is not None:
        paradas.append((ini, i))
    L = ["PALCO PARADO (handoff §3.2 / §8.10): máscara do palco a 960×540 (x < 545, y ≥ 95: sem a coluna e sem o canto); parado = menos de 40 px",
         "mudam mais de 8 níveis numa janela de 3 s. Abaixo, a duração total de cada trecho parado (a janela de 3 s já inclusa).", ""]
    n35 = n5 = 0
    for a, b in paradas:
        dur = (b - a) / FPS
        cls = "> 5 s" if dur > 5 else ("3–5 s" if dur >= 3 else "< 3 s")
        n5 += dur > 5
        n35 += 3 <= dur <= 5
        L.append(f"{a / FPS // 60:02.0f}:{a / FPS % 60:05.2f} – {b / FPS // 60:02.0f}:{b / FPS % 60:05.2f}  {dur:5.2f} s  {cls}")
    L += ["", f"Trechos > 5 s: {n5}; de 3 a 5 s: {n35}."]
    vz = linhas("[vazia]")
    L += ["", f"Moldura/placa vazia (auditoria por play, [vazia]): {len(vz)}"] + [f"  {c} {l[:140]}" for c, l in vz[:30]]
    grava(f"palco_parado_{RV}.txt", "\n".join(L) + "\n")


def _linhas(faixa, eixo):
    """Nº de linhas finas da grade numa faixa (cinza): picos de brilho ≥ 2,5 níveis acima da mediana local, ao longo do eixo dado."""
    perfil = faixa.mean(axis=eixo)
    from scipy.ndimage import median_filter
    base = median_filter(perfil, size=9)
    pk = (perfil - base > 2.5) & (perfil >= np.roll(perfil, 1)) & (perfil >= np.roll(perfil, -1))
    return int(pk.sum())


def grade_tela():
    """Um still por âncora (4 s depois do início): a grade tem de aparecer de borda a borda nas cenas 2D: linhas verticais na faixa esquerda
    (x < 80) e na direita (x > 880), e linhas horizontais na faixa de cima (y 100–160) e de baixo (y 470–530), a 960×540."""
    blocos = [(c, aid, float(t)) for c in LOTES for aid, t in re.findall(r"\[ancora\] (\S+) ([\d.]+)", LOG.get(c, ""))]
    alvo = {}
    for c, aid, t in blocos:
        alvo[round((INI[c] + t + 4.0) * FPS)] = (c, aid)
    L = ["GRADE NA TELA (handoff §8.9): still 4 s depois do início de cada âncora; nº de linhas da grade (picos finos de brilho) nas faixas",
         "esquerda (x < 200), direita (x > 760), de cima (y 100–160) e de baixo (y 470–530) a 960×540. 3D e CTA são lisos por regra.", ""]
    for i, a in enumerate(quadros_mp4()):
        if i in alvo:
            c, aid = alvo[i]
            g = a.astype(float).mean(2)
            ve, vd = _linhas(g[120:520, :200], 0), _linhas(g[120:520, 760:], 0)
            hc, hb = _linhas(g[100:160, 200:760], 1), _linhas(g[470:530, 200:760], 1)
            ok = min(ve, vd) >= 2 and max(hc, hb) >= 1
            L.append(f"{aid:6s} {i / FPS // 60:02.0f}:{i / FPS % 60:05.2f}  vert. esq {ve:2d} · dir {vd:2d}   horiz. cima {hc:2d} · baixo {hb:2d}   {'GRADE DE BORDA A BORDA' if ok else 'SEM GRADE (3D/liso ou falha)'}")
            Image.fromarray(a).save(QA / "grade" / f"{aid}.png")
    grava(f"grade_tela_{RV}.txt", "\n".join(L) + "\n")


# ── alinhamento 3D ─────────────────────────────────────────────────────────────────────────────────────────────────
def alinhamento():
    L = ["ALINHAMENTO 3D × MANIM (handoff §8.2). (1) Rótulos presos: o ponto que o Manim usou (proj3d em Python) × o ponto do pontos.json do",
         "Three.js no mesmo quadro, em px de 1080p (os PNGs são 960×540; o pontos.json é sempre em px de 1920×1080, sem divisão).", ""]
    for c in ("PE3", "PE6"):
        f = AQUI / "renders" / RV / "qa" / "al" / f"{c}.json"
        if not f.exists():
            L.append(f"{c}: sem registro")
            continue
        reg = json.loads(f.read_text())
        dd = []
        for cena in {r[1] for r in reg}:
            pj = AQUI / "threejs" / "q3d" / f"{c}_960x540" / cena / "pontos.json"
            if not pj.exists():
                continue
            P = json.loads(pj.read_text())
            for lote, cn, fq, nome, x, y in reg:
                if cn != cena or str(fq) not in P or nome not in P[str(fq)]:
                    continue
                X, Y = P[str(fq)][nome]
                dd.append((float(np.hypot(X - x, Y - y)), cena, nome, fq))
        if dd:
            d = np.array([x[0] for x in dd])
            L.append(f"{c}: {len(dd)} amostras (rótulo × quadro); erro médio {d.mean():.3f} px, máximo {d.max():.3f} px; ≤ 2 px: {(d <= 2).mean():.1%}")
    pz = AQUI / "renders" / RV / "qa" / "pouso3d.txt"
    if pz.exists():
        L += ["", "(2) Contorno 2D × contorno 3D no quadro da troca (entrada e pousos):", pz.read_text(encoding="utf-8")]
    grava(f"alinhamento3d_{RV}.txt", "\n".join(L) + "\n")


# ── prancha render × alvo ──────────────────────────────────────────────────────────────────────────────────────────
ALVOS = [("01_H1", "v1_01_H1_centro_no_buraco.jpg"), ("02_E1-2", "v1_02_E1-2_bordas_para_uv.jpg"), ("03_E1-3", "v1_03_E1-3_comprimento_cancela.jpg"),
         ("04_E2-2", "v1_04_E2-2_jacobiano_da_volta.jpg"), ("05_E2-3", "v1_05_E2-3_area_e_pipa.jpg"), ("06_E3-1", "v1_06_E3-1_oitavo_de_bola_3d.jpg"),
         ("07_E3-2", "v1_07_E3-2_polares_quarto_de_disco.jpg"), ("08_E4-1", "v1_08_E4-1_polares_esticadas.jpg"), ("09_E4-3", "v1_09_E4-3_meia_elipse_centro.jpg"),
         ("10_E5-2", "v1_10_E5-2_centro_no_buraco.jpg"), ("11_E5-3", "v1_11_E5-3_fio_de_prumo.jpg"), ("12_E5-4", "v1_12_E5-4_regua_homogenea_x_kr.jpg"),
         ("13_E6-1", "v1_13_E6-1_pappus_anel.jpg"), ("pap_md_E6-1", "r3d_pap_md.png"), ("14_E6-3", "v1_14_E6-3_bola_oca_confere.jpg"),
         ("pap_toro_E6-5", "r3d_pap_toro.png"), ("15_S2", "v1_15_S2_cubo_proximo.jpg")]


def marcas():
    out = {}
    for c in LOTES:
        for nome, t in re.findall(r"\[marca\] (\S+) ([\d.]+)", LOG.get(c, "")):
            out[nome] = INI[c] + float(t)
    return out


def prancha():
    M = marcas()
    quer = {}
    for nome, _ in ALVOS:
        if nome in M:
            dt = 0.0
            quer[round((M[nome] + dt) * FPS)] = nome
    pegos = {}
    for i, a in enumerate(quadros_mp4()):
        if i in quer:
            pegos[quer[i]] = a
    fnt = ImageFont.truetype(str(REF / "SpaceGrotesk-Medium.ttf"), 22)
    linhas_ = []
    for nome, arq in ALVOS:
        alvo = Image.open(REF / arq).convert("RGBA")
        if alvo.mode == "RGBA" and arq.endswith(".png"):
            bg = Image.new("RGBA", alvo.size, (24, 20, 58, 255))
            alvo = Image.alpha_composite(bg, alvo)
        alvo = alvo.convert("RGB").resize((960, 540))
        ren = Image.fromarray(pegos[nome]) if nome in pegos else Image.new("RGB", (960, 540), (60, 0, 0))
        row = Image.new("RGB", (1920, 580), (12, 10, 30))
        row.paste(ren, (0, 40))
        row.paste(alvo, (960, 40))
        d = ImageDraw.Draw(row)
        t = M.get(nome)
        d.text((12, 8), f"RENDER · {nome} · {int(t // 60)}:{t % 60:05.2f}" if t else f"RENDER · {nome} · (sem marca)", fill=(230, 230, 240), font=fnt)
        d.text((972, 8), f"ALVO · {arq}", fill=(230, 230, 240), font=fnt)
        linhas_.append(row)
    out = Image.new("RGB", (1920, 580 * len(linhas_)))
    for i, r in enumerate(linhas_):
        out.paste(r, (0, 580 * i))
    out.save(QA / f"comparacao_{RV}.jpg", quality=86)
    for nome in pegos:
        Image.fromarray(pegos[nome]).save(QA / f"still_{nome}.png")
    print("[qa] comparacao_v1.jpg", len(pegos), "de", len(ALVOS))


# ── v2 §7.2 · R5 caixa × caixa (A15) ───────────────────────────────────────────────────────────────────────────────
def caixa_caixa():
    L = ["R5 CAIXA × CAIXA (handoff v2 §7.2 / A15): todo texto contra todo texto vizinho, folga 10 px (o R5 do kit só conta sobreposição > 2 px).",
         "Amostrado nos mesmos instantes do R5 (cada play/espera e a cada ≤ 0,5 s nas animações: depois de cada escrita, antes e depois de cada voo).",
         "Fora da conta: o glifo em voo (sai no R5 de cima) e o texto que está saindo. Meta: zero.", ""]
    tot, ex = Counter(), defaultdict(list)
    for c, ln in linhas("[R5C]"):
        m = re.match(r"\[R5C\] (\S+)\s+([\d.]+)s (.*?) folga (-?\d+) px", ln)
        if not m:
            continue
        aid, t, par, fg = m.groups()
        tot[(c, aid, par)] += 1
        if len(ex[(c, aid, par)]) < 3:
            ex[(c, aid, par)].append(f"{ts(c, float(t))} ({fg} px)")
    L.append(f"Total: {sum(tot.values())} amostras em {len(tot)} pares.")
    L.append("")
    for (c, aid, par), n in sorted(tot.items(), key=lambda kv: -kv[1]):
        L.append(f"{c:4s} {aid:6s} {n:4d}×  {par[:120]}   (ex.: {', '.join(ex[(c, aid, par)])})")
    grava(f"caixa_caixa_{RV}.txt", "\n".join(L) + "\n")


# ── v2 §7.5 · mapa em ação (B1) e varredura (B2) ─────────────────────────────────────────────────────────────────────
def mapa_varre():
    L = ["MAPA EM AÇÃO (B1) E VARREDURA (B2) (handoff v2 §7.5): cada ocorrência no log do render, com o lote e o tempo de render do lote.", ""]
    for c in LOTES:
        r = re.findall(r"\[render\] \S+ (\d+)s", LOG.get(c, ""))
        for tag in ("[mapa]", "[varre]"):
            for ln in LOG.get(c, "").splitlines():
                if ln.startswith(tag):
                    L.append(f"{c:4s} {ln}   · render do lote {r[-1] if r else '?'} s")
    L += ["", "Mapa em ação: uma UpdateFromAlphaFunc só durante o play (sem updater permanente). Varredura: um always_redraw por cena,",
          "removido (clear_updaters + remove) ao fim da varredura."]
    grava(f"mapa_e_varredura_{RV}.txt", "\n".join(L) + "\n")


# ── v2 §7.3 · recortes 1:1 de A1–A15 ─────────────────────────────────────────────────────────────────────────────────
RECORTES = [  # (item, lote, gatilho ou marca, dt s, caixa px 1080p (x0, y0, x1, y1), o que mostrar)
    ("A1", "PE2", "as bordas trocam", 1.0, (180, 820, 760, 1075), "rótulo 1/√2 à esquerda-abaixo da marca"),
    ("A2", "PE6", "pap_toro_E6-5", 0.0, (1150, 620, 1900, 1040), "a conta do toro com as chaves e rótulos separados"),
    ("A3", "PE5", "10_E5-2", 0.0, (1150, 180, 1900, 1040), "0,990 < 1 no slot abaixo do resultado"),
    ("A4", "PE4", "E4-4", 0.0, (0, 250, 1100, 1060), "bloco ρ = ky fora do meio disco, ȳ à esquerda de x = −1, 0,5 à esquerda do eixo"),
    ("A5", "PE1", "a de dentro é em u", 0.0, (200, 280, 1000, 900), "COMPRIMENTO / = v em duas linhas sob a chave"),
    ("A6", "PE2", "04_E2-2", 0.0, (1000, 60, 1910, 1060), "coluna depois dos voos (chips contornando a coluna)"),
    ("A7", "PH", "01_H1", 0.0, (300, 300, 1300, 1000), "o ? longe dos traços"),
    ("A8", "PS", "deixa o like", 1.2, (300, 100, 1620, 1060), "INSCREVA-SE depois do cubo sair"),
    ("A9", "PE1", "passo quatro", 1.6, (1000, 40, 1910, 600), "chip |J| = 1 na linha dos chips"),
    ("A10", "PE5", "12_E5-4", 0.0, (1040, 40, 1910, 300), "chips dos resultados e legendas"),
    ("A11", "PE1", "02_E1-2", 0.0, (0, 120, 1200, 1060), "E1-2 com o mapa em ação (sem voo atravessando)"),
    ("A12", "PE2", "entre as hipérboles", 1.2, (0, 200, 1000, 1060), "a curva nasce no gatilho"),
    ("A13", "PE6", "qual o volume", 0.6, (0, 120, 1910, 1060), "giro com rótulos e a coluna"),
    ("A14", "PE5", "menor que um por", 2.0, (1150, 180, 1900, 1040), "ȳ como chip e 0,990 < 1 no slot"),
    ("A15", "PE1", "03_E1-3", 0.0, (1040, 60, 1910, 1060), "coluna: linhas sem encostar (caixa × caixa)"),
]


def t_de(c, frase):
    anc = {}
    for ln in LOG.get(c, "").splitlines():
        m = re.match(r"\[ancora\] (\S+) ([\d.]+)", ln)
        if m:
            anc[m.group(1)] = float(m.group(2))
            continue
        m = re.match(r"\[gatilho\] (\S+)\s+([\d.]+)s .*\) (.*)$", ln)
        if m and frase in m.group(3):
            return anc.get(m.group(1), 0.0) + float(m.group(2))
        m = re.match(r"\[marca\] (\S+) ([\d.]+)", ln)
        if m and frase == m.group(1):
            return float(m.group(2))
    return None


def recortes():
    d = QA / "recortes"
    d.mkdir(exist_ok=True)
    L = ["RECORTES 1:1 (handoff v2 §7.3): o quadro do preview (960×540) depois da correção, recortado sem reduzir; caixa dada em px de 1080p.", ""]
    for it, c, fr, dt, (x0, y0, x1, y1), oq in RECORTES:
        t = t_de(c, fr)
        if t is None:
            L.append(f"{it:4s} {c} '{fr}': gatilho não achado")
            continue
        src = AQUI / f"media_{c}" / "videos" / "cena" / "540p15" / f"{c}.mp4"
        tmp = d / f"_{it}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t + dt:.3f}", "-i", str(src), "-frames:v", "1", str(tmp)], check=False)
        if not tmp.exists():
            L.append(f"{it:4s} {c}: quadro fora do clipe (gatilho mudou na v3.1)")
            continue
        im = Image.open(tmp).crop((x0 // 2, y0 // 2, x1 // 2, y1 // 2))
        im.save(d / f"{it}.png")
        tmp.unlink()
        L.append(f"{it:4s} {ts(c, t + dt)}  {c} · {oq} → recortes/{it}.png")
    grava(f"recortes_{RV}.txt", "\n".join(L) + "\n")


if __name__ == "__main__":
    (QA / "grade").mkdir(exist_ok=True)
    for f in (r5, caixa_caixa, mapa_varre, recortes, flash, texto, gmaps, origens, contas, tempos, alinhamento, prancha, palco_parado, grade_tela):
        f()
