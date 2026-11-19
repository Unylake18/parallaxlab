"""yt_0023 — QA do preview: duração por âncora (narração nominal × cena), portão (linhas [audit] dos logs de auditoria), auditorias de física
(VÍNCULO, ENERGIA, FORÇA NO EIXO, CURVA, PÊNDULO EM FASE, ALIASING, NÚMEROS), alinhamento 3D × Manim medido nos pontos.json dos quadros
gerados e fundo. uso: python qa23.py → renders/qa.txt"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pecas23 import (A_ARO, A_VOL, AL_C, AL_FREIO, AL_VOL, G, I_ANEL, I_ARO, I_CUBO, I_DISCO, I_VOL, K_VOL, M1, M2, RC, T_1M, T_PARA, T_VOL, W15,
                     forca_eixo, freio_th, periodo, rc, vol_th)

U = Path(__file__).resolve().parent
LOTES = ["PH", "PE1a", "PE1b", "PE2", "PE3", "PE4", "PS"]
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
out = []
p = out.append
ok_geral = True


def chk(nome, cond, txt_):
    global ok_geral
    ok_geral &= bool(cond)
    p(f"  [{'OK ' if cond else 'FALHA'}] {nome}: {txt_}")


def ov(l):
    f = U / f"qa_overlay_{l}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def px(m):
    return np.array([(m[0] + 8) / 16 * 960, (4.5 - m[1]) / 9 * 540])


p("yt_0023 — QA do preview silencioso 960×540 / 15 fps (sem voz; tempos NOMINAIS a 2,7 palavras/s)")
p("")
# ── duração por âncora ──
p("1. DURAÇÃO POR ÂNCORA (narração nominal × cena)")
tot = 0.0
for l in LOTES:
    f = U / f"log_{l}.txt"
    if not f.exists():
        p(f"  {l}: sem log")
        continue
    s = f.read_text(encoding="utf-8", errors="replace")
    marcas = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", s)]
    for (a, t0), (_, t1) in zip(marcas, marcas[1:]):
        nar = ANC["ancoras"][a]["dur"] if a in ANC["ancoras"] else 0
        p(f"  {l:5s} {a:6s} narração {nar:6.1f} s · cena {t1 - t0:6.1f} s{'  (cena mais longa)' if t1 - t0 > nar + 0.2 else ''}")
    m = re.search(r"\[tempo\] total ([0-9.]+)", s)
    if m:
        tot += float(m.group(1))
p(f"  TOTAL {tot:.1f} s = {int(tot) // 60}:{int(tot) % 60:02d}")
p("")

# ── portão ──
p("2. PORTÃO POR EVENTO (v2 §6.2: objeto × intervalo; REAL = a corrigir; INTENCIONAL = lista fechada com motivo)")
INTENCIONAL = [
    (r"ENCOSTADO .*\\checkmark", "✓ da trilha preso ao item (marca de item concluído, 0,1 u acima dele)"),
]
eventos_reais = Counter()
for l in LOTES:
    f = U / f"log_aud_{l}.txt"
    if not f.exists():
        p(f"  {l}: auditoria não rodada")
        continue
    s = f.read_text(encoding="utf-8", errors="replace")
    ev = {}
    for ln in s.splitlines():
        if "[audit]" not in ln:
            continue
        m = re.search(r"\[audit\]\s+([0-9.]+)s\s+(.*)$", ln)
        if not m:
            continue
        t, corpo = float(m.group(1)), m.group(2).strip()
        mc = re.match(r"([A-ZÇÃÉÍÓÚÊÔÂÕ⊕ ]{4,}?)(?:\s{2}|\s[a-z0-9'(\\]|\s[A-Z][a-z]|$)", corpo)
        classe = mc.group(1).strip() if mc else corpo[:24]
        chave = (classe, re.sub(r"[0-9.]+", "#", corpo)[:70])
        lst = ev.setdefault(chave, [])
        if lst and t - lst[-1][1] <= 0.6:
            lst[-1][1] = t
        else:
            lst.append([t, t])
    por_classe = Counter()
    linhas_ev = []
    flog = U / f"log_{l}.txt"
    jan_ = [float(t_) for t_ in re.findall(r"\[ordem\]\s+([\d.]+)s (?:voa|passo)", flog.read_text(encoding="utf-8", errors="replace"))] if flog.exists() else []
    for (classe, desc), ints in sorted(ev.items(), key=lambda kv: kv[1][0][0]):
        motivo = next((mot for pat, mot in INTENCIONAL if re.search(pat, desc)), None)
        for a, b in ints:
            mv_ = None
            if not motivo and classe.startswith(("TEXTO SOBRE OBJETO", "SOBREPOSICAO")) and "VMobjectFromSVGP" in desc and any(t0_ - 0.3 <= a <= t0_ + 3.2 for t0_ in jan_):
                mv_ = "voo/passo de glifos (TransformFromCopy ou glyph map): o termo em trânsito sai do rótulo/linha de origem, sobrepõe a origem durante o voo e pousa na vaga; o TRÂNSITO (cruzamento prolongado) continua contado à parte"
            tipo = "INTENCIONAL" if (motivo or mv_) else "REAL"
            if mv_ and not motivo:
                linhas_ev.append(f"      {a:6.1f}–{b:6.1f} s  {tipo:11s} {desc}  ({mv_[:60]}…)")
                continue
            if not motivo:
                por_classe[classe] += 1
                eventos_reais[classe] += 1
            linhas_ev.append(f"      {a:6.1f}–{b:6.1f} s  {tipo:11s} {desc}" + (f"  ({motivo})" if motivo else ""))
    p(f"  {l}: eventos REAIS por classe: " + (", ".join(f"{k} {v}" for k, v in por_classe.most_common()) if por_classe else "zero"))
    for x in linhas_ev[:400]:
        p(x)
for cl in ("TEXTO PEQUENO", "ENCOSTADO", "TEXTO SOBRE OBJETO", "SOBREPOSICAO", "SOBREPOSIÇÃO", "FORA DA MARGEM", "COLUNA VAZIA", "OPACIDADE", "OPACIDADE BAIXA", "TRÂNSITO", "SEM PALCO", "LINHA ÚNICA"):
    n_ = sum(v for k, v in eventos_reais.items() if k.startswith(cl))
    if n_:
        chk(f"PORTÃO {cl}", False, f"{n_} eventos REAIS")
p("")

# ── física ──
p("3. AUDITORIAS DE FÍSICA")
# VÍNCULO no 3D (pontos dos quadros gerados): carretel na vista frontal → |Δy1|/|Δy2| = R/r = 3
for l in ("PH", "PE3"):
    f = U / f"threejs/q3d/{l}_960x540/carretel/pontos.json"
    if not f.exists():
        p(f"  VÍNCULO {l}: sem pontos.json")
        continue
    pts = json.loads(f.read_text())
    reg = ov(l).get("carretel", {})
    # referência: quadro em repouso (θ = 0) com a MESMA câmera (mesmo eixo na tela, ±0,5 px e mesma distância eixo–bloco 2 a θ = 0)
    refs = [k for k, v in pts.items() if abs(v["th"]) < 1e-4]
    razoes = []
    for k, v in pts.items():
        if v["th"] < 0.3:
            continue
        cand = [k0 for k0 in refs if np.linalg.norm(np.array(pts[k0]["eixo"]) - np.array(v["eixo"])) < 0.5
                and abs((pts[k0]["b1"][0] - pts[k0]["eixo"][0]) - (v["b1"][0] - v["eixo"][0])) < 0.5]
        frontal = abs(abs(v["b1"][0] - v["eixo"][0]) / max(1e-6, abs(v["b2"][0] - v["eixo"][0])) - 3) < 0.05
        if not cand or not frontal:
            continue
        k0 = cand[0]
        d1 = abs(v["b1"][1] - pts[k0]["b1"][1])
        d2 = abs(v["b2"][1] - pts[k0]["b2"][1])
        if d2 > 2:
            razoes.append(d1 / d2)
    if razoes:
        r = np.array(razoes)
        chk(f"VÍNCULO {l}", abs(np.median(r) - 3) < 0.15, f"|Δy₁|/|Δy₂| nos quadros 3D: mediana {np.median(r):.3f} (n={len(r)}, vista frontal; o desvio vem da perspectiva: os tambores estão a 13,5 cm de profundidade um do outro; no mundo 3D o deslocamento é R·Δθ e r·Δθ por construção, razão 3,000)")
a1, a2 = AL_C * RC, AL_C * rc
chk("VÍNCULO a₁/a₂", abs(a1 / a2 - 3) < 0.03, f"a₁ = {a1:.3f}, a₂ = {a2:.3f} m/s², razão {a1 / a2:.3f}")
mgh = 10 * G * 0.15 * vol_th(1.5)
Kb = 10 * (0.15 * AL_VOL * 1.5) ** 2 / 2
chk("ENERGIA E1-13", abs(mgh - Kb - K_VOL) / mgh < 0.005, f"mgh {mgh:.2f} = K_bloco {Kb:.2f} + K_vol {K_VOL:.2f}")
chk("ENERGIA E1-16", abs(4.0 * freio_th(T_PARA) - K_VOL) / K_VOL < 0.005, f"W = τΔθ = {4 * freio_th(T_PARA):.2f} J × K_vol {K_VOL:.2f} J; Δθ {freio_th(T_PARA):.2f} rad")
v1 = math.sqrt(2 * a1 * 1.0)
v2 = v1 / 3
Kt = M1 * v1 ** 2 / 2 + M2 * v2 ** 2 / 2 + 0.5 * (v1 / RC) ** 2 / 2
dU = M1 * G * 1.0 - M2 * G / 3
chk("ENERGIA E3-8", abs(Kt - dU) / dU < 0.005, f"ΔU {dU:.2f} J = K₁ + K₂ + K_c {Kt:.2f} J; v₁ = {v1:.3f} m/s")
h = ov("PE2").get("haste", {})
for alvo, esp in ((0.0, (0.0, 4 / 7)), (math.pi / 4, (-9 / 14, 17 / 14)), (math.pi / 2, (0.0, 13 / 7))):
    cand = [v for v in h.values() if abs(v["th"] - alvo) < 1e-3]
    if cand:
        F = cand[0]["F"]
        chk(f"FORÇA NO EIXO θ={math.degrees(alvo):.0f}°", abs(F[0] - esp[0]) < 0.02 and abs(F[1] - esp[1]) < 0.02, f"F/Mg = ({F[0]:.3f}, {F[1]:.3f}), esperado ({esp[0]:.3f}, {esp[1]:.3f})")
    else:
        p(f"  [—] FORÇA NO EIXO θ={math.degrees(alvo):.0f}°: sem quadro registrado")
if h:
    err = max(abs(np.linalg.norm(v["F"][:2]) - forca_eixo(v["th"])["mod"]) / forca_eixo(v["th"])["mod"] for v in h.values())
    chk("FORÇA NO EIXO (todos os quadros)", err < 0.02, f"erro máximo do módulo {100 * err:.3f}% em {len(h)} quadros")
c = ov("PE4").get("curva", {})
if c:
    e = []
    for v in c.values():
        gx0, gy0, gw, gh = 1.35, -3.15, 5.0, 1.95
        alvo = np.array([gx0 + gw * (v["l"] - 0.02) / 0.38, gy0 + gh * (periodo(v["l"]) - 0.70) / 0.60])
        e.append(np.linalg.norm(px(v["ponto"]) - px(alvo)))
    chk("CURVA", max(e) <= 1.0, f"ponto × T(l) da posição do eixo: erro máx {max(e):.3f} px em {len(e)} quadros")
ls_ = np.linspace(0.02, 0.4, 380001)
lmin = ls_[np.argmin([periodo(x) for x in ls_])]
chk("CURVA mínimo", abs(lmin - 0.0707) < 0.0005, f"mínimo em l = {lmin * 100:.2f} cm, T = {periodo(lmin):.4f} s")
chk("CURVA 5 e 10 cm", abs(periodo(0.05) - periodo(0.10)) < 1e-9 and abs(periodo(0.05) - 0.777) < 0.001, f"T(5) = {periodo(0.05):.4f} s, T(10) = {periodo(0.10):.4f} s")
leq = (0.1 ** 2 + 0.3 ** 2) / 0.3
chk("PÊNDULO EM FASE", abs(periodo(0.3, True) - 2 * math.pi * math.sqrt(leq / G)) < 1e-12, f"T(dois discos) = {periodo(0.3, True):.4f} s = T(simples, l_eq = {leq:.4f} m): defasagem 0° em 3 períodos (mesma lei de tempo)")
# ALIASING
for l, cena in (("PH", "carretel"), ("PE1a", "volante"), ("PE1b", "volante"), ("PE3", "carretel"), ("PE2", "haste3d")):
    r_ = ov(l).get(cena, {})
    if not r_:
        continue
    ks = sorted(int(k) for k in r_)
    th = np.array([r_[str(k)]["th"] for k in ks])
    d = np.abs(np.diff(th))[np.diff(ks) == 1]
    d = d[d < math.pi]                                   # trocas de tomada (reinício do estado) não são giro
    mx = math.degrees(d.max()) if len(d) else 0
    chk(f"ALIASING {l} {cena}", mx <= 60.0, f"máximo {mx:.1f}°/quadro (limite v2/v6: ≤ 60°/quadro)" + (" · nominal do PE1b 37,6°" if l == "PE1b" else ""))
p("")
p("4. NÚMEROS (tela × física integrada)")
nums = [("I_anel", I_ANEL, 1.875, 1e-3), ("I_cubo", I_CUBO, 0.015, 1e-4), ("2 I_disco", 2 * I_DISCO, 0.1275, 1e-4), ("I", I_VOL, 2.0175, 1e-4),
        ("I/r²", I_VOL / 0.0225, 89.7, 0.05), ("a", A_VOL, 0.983, 5e-4), ("α", AL_VOL, 6.56, 5e-3), ("T", T_VOL, 88.2, 0.05),
        ("ω(1,5)", W15, 9.83, 5e-3), ("Δθ(1,5)", vol_th(1.5), 7.37, 6e-3), ("h", 0.15 * vol_th(1.5), 1.11, 5e-3), ("v", 0.15 * W15, 1.47, 6e-3),
        ("a_t borda", AL_VOL * 0.4, 2.62, 5e-3), ("a_c borda", W15 ** 2 * 0.4, 38.7, 0.05), ("ângulo", math.degrees(math.atan(AL_VOL / W15 ** 2)), 3.9, 0.05),
        ("mgh", mgh, 108.4, 0.05), ("K_bloco", Kb, 10.9, 0.05), ("K_vol", K_VOL, 97.5, 0.05), ("P(1,5)", T_VOL * 0.15 * W15, 130, 0.5),
        ("α_f", AL_FREIO, 1.98, 5e-3), ("t parada", T_PARA, 4.96, 5e-3), ("Δθ freio", freio_th(T_PARA), 24.4, 0.05),
        ("I_aro", I_ARO, 3.2, 1e-6), ("I_aro/r²", I_ARO / 0.0225, 142, 0.5), ("a aro", A_ARO, 0.644, 5e-4),
        ("α carretel", AL_C, 6.88, 5e-3), ("a₁", a1, 2.06, 5e-3), ("a₂", a2, 0.688, 5e-4), ("T₁", M1 * (G - a1), 46.4, 0.05), ("T₂", M2 * (G + a2), 104.9, 0.05),
        ("T₁R − T₂r", M1 * (G - a1) * RC - M2 * (G + a2) * rc, 3.44, 5e-3), ("ΔU", dU, 26.1, 0.05), ("v₁", v1, 2.03, 5e-3), ("v₂", v2, 0.677, 5e-4),
        ("T 2 discos", periodo(0.3, True), 1.159, 5e-4), ("T sem disco", periodo(0.3), 1.129, 5e-4), ("T mín", periodo(0.1 / math.sqrt(2)), 0.755, 5e-4),
        ("T(R)", periodo(0.1), 0.777, 5e-4), ("excesso", periodo(0.1) / periodo(0.1 / math.sqrt(2)) - 1, 0.030, 1e-3)]
for n, v, t, tol in nums:
    chk(f"NÚMERO {n}", abs(v - t) <= tol, f"física {v:.5g} · tela {t}")
p("")
p("5. ALINHAMENTO 3D × MANIM (px, medido nos pontos.json dos quadros gerados × projeção usada pelo Manim)")
for l, cena, pares in (("PH", "carretel", (("eixo", "eixo"), ("b1", "b1"), ("b2", "b2"))), ("PE3", "carretel", (("eixo", "eixo"), ("b1", "b1"), ("b2", "b2"))),
                       ("PE1a", "volante", (("eixo", "eixo"), ("b", "bloco"))), ("PE1b", "volante", (("eixo", "eixo"), ("b", "bloco")))):
    f = U / f"threejs/q3d/{l}_960x540/{cena}/pontos.json"
    r_ = ov(l).get(cena, {})
    if not f.exists() or not r_:
        p(f"  {l} {cena}: sem dados")
        continue
    pts = json.loads(f.read_text())
    e = []
    for k, v in pts.items():
        if k in r_:
            for a, b in pares:
                e.append(np.linalg.norm(np.array(v[a]) - px(r_[k][b])))
    if e:
        chk(f"ALINHAMENTO {l} {cena}", max(e) <= 2.0, f"máx {max(e):.2f} px, média {np.mean(e):.2f} px em {len(e)} medidas")
p("")
for l, cena_p, cena_r, fn in (("PE2", "haste", "haste3d", lambda v: [("eixo", v["eixo"])]),
                              ("PE4", "pendulo", "pendulo", lambda v: [("eixo", v["pend"][0]["eixo"]), ("disco", v["pend"][0]["disco"])] if v.get("pend") else [])):
    f = U / f"threejs/q3d/{l}_960x540/{cena_p}/pontos.json"
    r_ = ov(l).get(cena_r, {})
    if not f.exists() or not r_:
        p(f"  {l} {cena_p}: sem dados")
        continue
    pts = json.loads(f.read_text())
    e = []
    for k, v in pts.items():
        if k in r_ and (cena_r != "pendulo" or r_[k].get("u", 1) >= 0.9999):
            for nome, q in fn(v):
                e.append(np.linalg.norm(np.array(q) - px(r_[k][nome])))
    if e:
        chk(f"ALINHAMENTO {l} {cena_p}", max(e) <= 2.0, f"máx {max(e):.2f} px, média {np.mean(e):.2f} px em {len(e)} medidas (frontal)")
p("")
p("5b. CONCÊNTRICO (v2 §1.3; todos os quadros 3D: centros e mancais no eixo ≤ 1 px, pivô ≤ 1 px, fio tangente ≤ 1 px e vertical ≤ 0,5°)")
import conc23  # noqa: E402
for l in LOTES:
    base = U / f"threejs/q3d/{l}_960x540"
    if not base.exists():
        continue
    for d in sorted(base.iterdir()):
        f = d / "pontos.json"
        if d.name == "regua" or not f.exists():
            continue
        pts = json.loads(f.read_text())
        mx = {k: 0.0 for k in conc23.LIM}
        nq = 0
        for v in pts.values():
            if not v:
                continue
            r = conc23.medir(v)
            nq += 1
            for k in mx:
                mx[k] = max(mx[k], r[k])
        fl = [k for k in mx if mx[k] > conc23.LIM[k]]
        chk(f"CONCÊNTRICO {l} {d.name}", not fl, f"{nq} quadros · " + " · ".join(f"{k} {v:.2f}" for k, v in mx.items()))
p("")
p("5c. ÁLGEBRA (v2 §2.3: [alg] do render; por âncora: linhas, GM, voos; mínimo 8 GM por exercício e 3 no D2)")
alg = []
for l in LOTES:
    f = U / f"log_{l}.txt"
    if f.exists():
        for m in re.finditer(r"\[alg\] (\S+) (\S+) voos=(\d+) \| (.*)", f.read_text(encoding="utf-8", errors="replace")):
            alg.append((m.group(1), m.group(2), int(m.group(3)), m.group(4)))
por_anc = {}
for a, met, nv, tex in alg:
    d = por_anc.setdefault(a, Counter())
    d["linhas"] += 1
    d[met] += 1
    d["voos"] += nv
for a, d in por_anc.items():
    p(f"  {a:6s} linhas {d['linhas']:2d} · lei {d['lei']:2d} · GM {d['GM']:2d} · voo {d['voo']:2d} (termos voando {d['voos']:2d}) · escrita {d['escrita']:2d}")
for ex, pref in (("D2", ("D2",)), ("E1", ("E1-",)), ("E2", ("E2-",)), ("E3", ("E3-",)), ("E4", ("E4-",))):
    n_ = sum(d["GM"] for a, d in por_anc.items() if a.startswith(pref))
    chk(f"ÁLGEBRA GM {ex}", n_ >= (3 if ex == "D2" else 8), f"{n_} passos por glyph map")
num_ = re.compile(r"\{,\}|\\mathrm\{(kg|m|s|N|J|W|rad)")
falhas_lei = []
vistos_lit = set()
for a, met, nv, tex in alg:
    if not num_.search(tex):
        vistos_lit.add(a)
    elif a not in vistos_lit and met != "GM":
        falhas_lei.append(f"{a}: {tex[:50]}")
chk("ÁLGEBRA LEI PRIMEIRO", not falhas_lei, "linha numérica sem linha literal antes na âncora: " + ("; ".join(falhas_lei[:12]) if falhas_lei else "nenhuma"))
cn_ = Counter()
fade_ = []
for l in LOTES:
    f = U / f"log_{l}.txt"
    if f.exists():
        for m in re.finditer(r"\[caneta\] (\S+) (passo|voa) (?:novos=(\d+)|fixos=(\d+) voos=(\d+)) fade=(\d+)(?: t=[\d.]+)?", f.read_text(encoding="utf-8", errors="replace")):
            a, tipo, nv, fx, vo, fd = m.groups()
            cn_[tipo + "_caneta"] += int(nv or fx or 0)
            cn_[tipo + "_eventos"] += 1
            if int(fd):
                fade_.append(f"{a} {tipo} fade={fd}")
p(f"  CANETA: passo {cn_['passo_eventos']} eventos · {cn_['passo_caneta']} termos novos escritos pela caneta; voa {cn_['voa_eventos']} eventos · {cn_['voa_caneta']} termos fixos escritos pela caneta; termos novos por fade/linha pronta: {len(fade_)}")
pl_ = []
for l in LOTES:
    f = U / f"log_{l}.txt"
    if f.exists():
        pl_ += [(l, float(t), int(n)) for t, n in re.findall(r"\[pilha\]\s+([\d.]+)s n=(\d+)", f.read_text(encoding="utf-8", errors="replace"))]
chk("PILHA ≤ 5 linhas", bool(pl_) and max(n for _, _, n in pl_) <= 5, f"máximo {max((n for _, _, n in pl_), default=0)} linhas simultâneas em {len(pl_)} entradas")
chk("CANETA (termo novo sem fade)", not fade_ and (cn_["passo_eventos"] + cn_["voa_eventos"]) > 0, "; ".join(fade_[:10]) if fade_ else "nenhum termo novo entrou por FadeIn/linha pronta")
p("")
p("6. FUNDO (v7, decisão do Kaio): degradê vertical estático #0B1A3A → #08122B (fundo_grad.png), sem estrelas, sem updater de fundo; critério: fundo constante entre lotes (a auditoria de estrelas contínuas não se aplica).")
p("")
p(f"RESULTADO GERAL: {'OK' if ok_geral else 'HÁ FALHAS (ver acima)'}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "qa.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
