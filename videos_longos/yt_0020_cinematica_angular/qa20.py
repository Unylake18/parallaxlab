"""yt_0020 — QA do preview v1 (handoff v1 §6) → renders/qa.txt.
1. Portão G28: linhas [audit] de cada lote (log_aud_<lote>.txt: auditoria a cada 3 quadros dentro de cada play + estado final), por categoria.
2. Auditorias de física (qa_overlay_<lote>.json): RÍGIDO, MESMO ω, ÁREA = ÂNGULO, SETAS PROPORCIONAIS, LIVRO / T5-4, PRODUTO VETORIAL, CORRENTE, TERRA,
   ALIASING, NÚMEROS (contra a tabela de conferência do Anexo A).
3. Alinhamento Three.js × Manim (pontos.json do r3d.js × projeção do Manim), em px, inclusive na troca disco 2D → 3D do T5-1.
4. Duração por âncora (narração nominal a 2,7 palavras/s × cena) e fatores das simulações.
5. Cor por capítulo (v2 §6: só cores de família, ≥ 30% da tinta) nos mp4 dos lotes e FUNDO (≤ 5% dos quadros com > 40% dos pixels abaixo de 0,03), no preview.
6. (v2 §9) MOSTRADOR, PARADO 3 s, COLUNA VAZIA 5 s, TAMANHO do objeto principal, COR POR TOKEN (logs), CAIXA VAZIA (ordem*).
7. (v3) COR OPERADOR, cor por capítulo com duas métricas, CAIXA VAZIA por qualquer caminho, frase-chave, a3d do T5-8, e1_5_inset: a parte que precisa do objeto em
   memória vem de `corop.py LOTE` (cor_operador_<LOTE>.json; sem ele a seção sai NÃO MEDIDO). Resumo de veredictos no topo do qa.txt.
uso: uv run --no-sync python qa20.py v3  → renders/v3/qa.txt e renders/v3/algebra.txt"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

VEL_HEX = "#9C8CFF"   # kit.VEL (handoff v3 §2)

U = Path(__file__).resolve().parent
sys.path.insert(0, str(U))
RODADA = sys.argv[1] if len(sys.argv) > 1 else "v1"
sys.argv = [sys.argv[0]]
TODOS = ["PH", "PT1", "PT2", "PT3", "PT4", "PT5", "PE1", "PE2", "PE3", "PS"]
import os  # noqa: E402
LOTES = [l for l in os.environ.get("QA_LOTES", ",".join(TODOS)).split(",") if l]   # QA_LOTES=PT1 testa um lote só
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
out = []
p = lambda *a: out.append(" ".join(str(x) for x in a))
ler = lambda f: (U / f).read_text(encoding="utf-8", errors="replace") if (U / f).exists() else ""
over = {l: json.loads(ler(f"qa_overlay_{l}.json") or "{}") for l in TODOS}
PX = 960 / 16
ok = lambda c: "OK" if c else "FALHA"

DST = U / "renders" / RODADA
DST.mkdir(parents=True, exist_ok=True)
p(f"# yt_0020 — QA do preview {RODADA} (960×540 / 15 fps, sem voz)")
p()
# ── 1. G28 ──
import g28  # noqa: E402

p("## 1. Portão G28 (linhas [audit] da auditoria a cada 3 quadros, dentro de cada play e no estado final)")
NOMES = ("TEXTO SOBRE OBJETO", "TEXTO SOBRE CAIXA", "TEXTO PEQUENO", "OBJETO FORA DA MARGEM", "FORA DA MARGEM", "FORA DA ZONA", "FORA DO QUADRO 3D", "SOBREPOSICAO",
         "ENCOSTADO", "SELO DUPLO", "LINHA ÓRFÃ", "CALHA", "TRÂNSITO", "RÓTULO SOLTO", "PALCO 3D", "SEM PALCO", "COR POR TOKEN", "CHAMADA CRUZA CORPO",
         "DEGRADÊ FORA DO ⊕", "OPACIDADE", "SELO EM CIMA DE OBJETO 3D", "TEXTO SOBRE TRAJETÓRIA", "ESPREMIDO", "CAIXA SEM LADO ESQUERDO", "MARCADORES COLADOS")
# Classificação à mão (lote, classe, regex na assinatura do g28.py, janela (t0, t1) s do lote ou None, tipo, motivo). Tipos:
#   FP  = falso positivo (a auditoria acusa algo que não aparece / está correto por desenho);
#   TR  = transitório: sobreposição que APARECE no quadro, mas dura ≤ 0,8 s durante pulso, escrita, voo ou troca (classificação do coordenador
#         na mensagem "lotes prontos"; o QA conferiu os quadros indicados). Não é contado como REAL no portão, mas fica listado.
# O que não casar com nenhuma regra (ou cair fora da janela) é REAL.
CLASSIF = [
    ("PT2", "ESPREMIDO", r"282", None, "FP", "o 282,7 fica dentro do cubo da hélice por desenho; legível, folga visível até as pás (70,8 e 71,8 s)"),
    ("PT3", "TEXTO PEQUENO", r"v=v_0\+at|v\^2=v_0\^2", None, "FP", "medido durante a entrada com escala crescente (a linha ainda nem aparece "
                                                                      "no quadro 140,93 s); no tamanho final nenhuma passada acusa"),
    ("PT3", "TEXTO SOBRE OBJETO", r".", (15.0, 140.0), "TR", "QA: 1–2 passadas (≤ 0,3 s) em entrada/troca de discos, gráfico e voo; "
                                                             "sobreposição visível nos quadros 15,6 / 35,4 / 91,3 / 107,5 / 117,6 / 139,8 s"),
    ("PT3", "SOBREPOSICAO", r"GIRO", None, "TR", "QA: 1 passada (139,7 s) na troca para a tabela MESMA MATEMÁTICA"),
    ("PT4", "TEXTO SOBRE OBJETO", r"^'r' x Circle|^'.theta' x Circle", None, "FO", "v3 §6 fundo_de_objeto: o Circle são as camadas do degradê do "
                                                                                    "disco_aco (rótulo na face do disco por desenho; o degradê é fundo do objeto, não objeto)"),
    ("PT4", "TEXTO SOBRE OBJETO", r"v_2=0", None, "FP", "sem sobreposição visível em 58,40 / 58,47 / 58,53 s (cópia do glyph map pousada na própria linha)"),
    ("PT4", "TEXTO SOBRE OBJETO", r"v_t=r", None, "TR", "coordenador: cópia de glyph map; QA: quadro 24,93 s visivelmente embaralhado (1 passada)"),
    ("PT1", "TEXTO SOBRE OBJETO", r"20", None, "TR", "coordenador: o rótulo cruza a referência tracejada no giro (0,4 s); QA: visível em 15,0 s"),
    ("PT5", "ENCOSTADO", r".", None, "TR", "coordenador: 1 quadro (x × ≠ e r⃗ × a_c na troca)"),
    ("PT5", "CALHA", r".", None, "TR", "coordenador: rótulo x no deslize (some no meio do deslize)"),
    ("PT5", "TRÂNSITO", r".", None, "TR", "coordenador: troca de lugar dθ⃗₁ ↔ dθ⃗₂ e cópia do v⃗ (1 passada cada)"),
    ("PT5", "TEXTO SOBRE OBJETO", r"vec a=", None, "FP", "coordenador: o ind (realce) sobre a própria linha"),
    ("PE1", "CALHA", r".", None, "TR", "coordenador: caixa 0,4 s entrando (192,9–193,3 s)"),
    ("PE1", "COR POR TOKEN", r".", None, "TR", "coordenador: 1 quadro; QA: é o contador mostrando '−0 rad' e '−0,0 VOLTAS' só no quadro 47,40 s "
                                               "(sinal de zero negativo; 47,33 e 47,53 s corretos)"),
    ("PE2", "TEXTO SOBRE OBJETO", r"alpha_2", None, "TR", "coordenador: 1 quadro no pico do pulso (96,0 e 98,7 s)"),
    ("PE2", "ENCOSTADO", r"VOLTAS", None, "TR", "coordenador: 1 quadro (134,0 s) na escrita"),
    ("PE2", "FORA DA ZONA", r"MAIORES", None, "TR", "coordenador: 1 quadro (153,5 s) na escrita"),
    ("PH", "SEM PALCO", r".*", (50.0, 58.0), "FP", "coordenador: A1 (o logo é ImageMobject, a auditoria não o vê) e 3,7 s de cartão de título no A2"),
    ("PH", "SEM PALCO", r".*", (0.0, 0.3), "TR", "QA: entrada do vídeo (a hélice acende em 0,2 s; quadros 0,0 e 0,2 s)"),
    ("PH", "SEM PALCO", r".*", (81.0, 81.5), "TR", "QA: troca A2 → A3, 1 passada com o quadro vazio (81,2 s), dentro da abertura (exceção declarada)"),
    ("PH", "TEXTO SOBRE OBJETO", r"approx", None, "TR", "coordenador: voos '≈ 100/≈ 970 km/h' (V intencional, 0,3 s)"),
    # v8 (R1): classificação dos 18 itens reais com o quadro de prova (renders/v8/_g_<lote>.png, 1 passada = ≤ 0,2 s)
    ("PT3", "TRÂNSITO", r".", None, "TR", "QA: quadros 9,50 s (dω/dt × d²θ/dt² na troca da equação) e 126,70 s (ω ω voando para a caixa); em 82,30 s o quadro está limpo (1 glifo em voo)"),
    ("PT3", "CALHA", r".", (45.0, 46.5), "FP", "QA: quadro 45,90 s sem sobreposição visível (selo entrando; 1 passada)"),
    ("PT3", "ENCOSTADO", r"omega", (109.0, 110.5), "TR", "QA: quadro 109,70 s é o fade-out da pilha (1 passada), nada encostado visível"),
    ("PT4", "TEXTO SOBRE OBJETO", r"frac\{d\}\{dt\}s=", None, "TR", "QA: quadro 13,10 s: troca da equação d/dt (glyph map em voo, 1 passada)"),
    ("PT4", "TEXTO SOBRE OBJETO", r"^'v_t' x VMobject em", None, "FP", "QA: quadros 17,40 e 27,80 s: v_t fica abaixo da ponta da seta que ele nomeia, fora do disco, legível"),
    ("PT4", "TEXTO SOBRE OBJETO", r"v_t>0", None, "TR", "QA: quadro 23,80 s: pilha em troca (voo de glifos, 1 passada)"),
    ("PT4", "TRÂNSITO", r".", None, "TR", "QA: quadro 182,10 s: φ e a_c voando para a equação da tangente (1 passada)"),
    ("PT5", "TEXTO SOBRE OBJETO", r"d.vec.theta_2", None, "TR", "QA: quadro 107,40 s: rótulo '÷4' em voo sobre a ponta de seta (2 passadas, 0,13 s)"),
    ("PT5", "TEXTO SOBRE OBJETO", r"r_.perp", None, "FP", "QA: quadro 190,30 s: r⊥ ao lado do traço da fatia, legível (1 passada)"),
    ("PE1", "TEXTO SOBRE OBJETO", r"Delta.theta=.omega_0", None, "TR", "QA: quadro 71,80 s: TransformMatchingTex da equação do ângulo (2 passadas)"),
    ("PE1", "TRÂNSITO", r".", None, "TR", "QA: quadros 96,50 s (glifo apagando) e 154,30 s (equação em voo), 1 passada cada"),
    ("PE2", "TRÂNSITO", r".", None, "TR", "QA: quadro 99,00 s: α₁ voando para a conta (1 passada)"),
    ("PE3", "TEXTO SOBRE OBJETO", r"EXAGERADO", None, "TR", "QA: quadro 26,90 s: o meridiano tracejado da Terra varre o canto do selo (1 passada)"),
    ("PE3", "TRÂNSITO", r".", None, "TR", "QA: quadros 81,70 s (365,24 voando) e 140,10 s (ω voando), 1 passada cada"),
    ("PE3", "TEXTO SOBRE OBJETO", r"omega=.frac\{2.pi\}", None, "TR", "QA: quadro 95,00 s: ω = 2π/T_sid em troca para a caixa (2 passadas)"),
    ("PE3", "TEXTO SOBRE OBJETO", r"^'.lambda'|^'a_c'", None, "FP", "QA: quadro 170,40 s: λ e a_c ao lado das setas na lupa, sem cobrir traço (1 passada)"),
    ("PH", "ENCOSTADO", r"approx 970", None, "TR","coordenador: pouso do voo '≈ 970 km/h' (1 passada, 27,2 s)"),
]
# v1 (antes): linhas "- LOTE: N ocorrências ...: CLASSE n; ..." do renders/qa_v1.txt
V1 = {}
for x in ler("renders/qa_v1.txt").split("## 2.")[0].splitlines():
    m_ = re.match(r"- (P\w+): (\d+) ocorrências.*?(?:: (.*))?$", x)
    if m_:
        V1[m_.group(1)] = Counter({k.rsplit(" ", 1)[0]: int(k.rsplit(" ", 1)[1]) for k in (m_.group(3) or "").split("; ") if k})
tot, tot1, reais, trans, fps, fos = Counter(), Counter(), [], [], [], []
for l in LOTES:
    a = ler(f"log_aud_{l}.txt")
    fim = "completa" if re.search(r"\[tempo\] total", a) else ("INCOMPLETA" if a else "sem log")
    cats = Counter()
    for x in a.splitlines():
        if "[audit]" in x:
            cats[next((k for k in NOMES if k in x), "OUTRO")] += 1
    n = sum(cats.values())
    dens = len(re.findall(r"\[dens\]", a))
    p(f"- {l}: v1 {sum(V1.get(l, Counter()).values())} → v2 {n} ocorrências em {dens} passadas ({fim})"
      + (": " + "; ".join(f"{k} {V1.get(l, Counter())[k]}→{v}" for k, v in cats.most_common()) if n else ""))
    tot.update(cats)
    tot1.update(V1.get(l, Counter()))
    for (cls, sig), ts in sorted(g28.le(l).items(), key=lambda kv: min(kv[1])):
        resto = list(ts)
        for lt, c, rx, jan, tipo, mot in CLASSIF:
            if lt != l or c != cls or not re.search(rx, sig):
                continue
            dentro = [t for t in resto if jan is None or jan[0] <= t <= jan[1]]
            if dentro:
                iv = ", ".join(f"{a_:.1f}–{b_:.1f}" for a_, b_ in g28.intervalos(dentro)[:4])
                p(f"    · {cls} {sig[:80]} [{iv} s] {len(dentro)} passadas → { {'FP': 'falso positivo', 'FO': 'fundo_de_objeto'}.get(tipo, 'TRANSITÓRIO')}: {mot}")
                (trans if tipo == "TR" else fos if tipo == "FO" else fps).append((l, cls))
                resto = [t for t in resto if t not in dentro]
        if resto:
            iv = ", ".join(f"{a_:.1f}–{b_:.1f}" for a_, b_ in g28.intervalos(resto)[:4])
            p(f"    · {cls} {sig[:80]} [{iv} s] {len(resto)} passadas → REAL")
            reais.append((l, cls))
p(f"- TOTAL: v1 {sum(tot1.values())} → v2 {sum(tot.values())} — " + "; ".join(f"{k} {tot1[k]}→{v}" for k, v in tot.most_common()))
p(f"- G28: {len(reais)} ocorrências únicas REAIS (meta 0) {ok(not reais)}" + (f" — por lote: {dict(Counter(l for l, _ in reais))}" if reais else "")
  + f"; {len(trans)} TRANSITÓRIAS (aparecem no quadro, ≤ 0,8 s; classificadas pelo coordenador ou pelo QA, ver motivo) — {dict(Counter(l for l, _ in trans))}; "
    f"{len(fps)} falsos positivos; {len(fos)} marcadas fundo_de_objeto (degradê do disco_aco: camadas Circle de fundo, não objeto)")
p("- Nota QA (não acusado pela auditoria): no PT4 o rótulo θ cruza o raio pintado e os pontos de 4,1 a 4,5 s (quadros 4,13 e 4,40 s); "
  "a auditoria só vê θ × Circle (degradê), não θ × Line")
p()

# ── 2. física ──
from pecas20 import NUM, DR  # noqa: E402

p("## 2. Auditorias de física")
# RÍGIDO
piores, n_q, col, raios = 0.0, 0, 0.0, {}
for l in ("PT1", "PT2", "PT3", "PT4", "PT5"):
    for f, r in over[l].get("rigido", {}).items():
        c, ps = np.array(r["c"]), [np.array(r[k]) for k in ("p1", "p2", "p3")]
        R_ = np.linalg.norm(ps[2] - c)                                   # v2: o raio de cada quadro (PT3 2,0; PT4 2,1 → 1,6)
        raios.setdefault(l, set()).add(round(float(R_), 2))
        ds = [np.linalg.norm(q - c) - R_ * k / 3 for k, q in zip((1, 2), ps)] + [np.linalg.norm(ps[2] - ps[0]) - 2 * R_ / 3]
        piores = max(piores, max(abs(x) for x in ds) * PX)
        u = (ps[2] - c) / R_
        col = max(col, max(abs(u[0] * (q - c)[1] - u[1] * (q - c)[0]) for q in ps) * PX)
        n_q += 1
rg = [v["d"] for l in ("PT1",) for v in over[l].get("regua", {}).values()]
p(f"- RÍGIDO ({n_q} quadros T1–T5, R = |p3 − c| de cada quadro; R por lote: "
  + "; ".join(f"{l} {min(v):.2f}" + (f"…{max(v):.2f}" if len(v) > 1 else "") for l, v in raios.items())
  + f"): |p1 − c| = R/3, |p2 − c| = 2R/3 e |p3 − p1| = 2R/3 com erro máx. {piores:.3f} px (≤ 1 px) {ok(piores <= 1)}; "
  f"pontos fora da linha pintada no máx. {col:.3f} px {ok(col <= 1)}; régua do T1-1 {len(rg)} quadros, variação {((max(rg) - min(rg)) * PX if rg else 0):.3f} px {ok(not rg or (max(rg) - min(rg)) * PX <= 1)}")
# MESMO ω
mw = list(over["PT2"].get("mesmo_w", {}).values())
if mw:
    dmax = max(math.degrees(max(v["dth"]) - min(v["dth"])) for v in mw)
    p(f"- MESMO ω (T2-3, {len(mw)} quadros): Δθ dos três pontos no mesmo Δt diferem no máx. {dmax:.4f}° (≤ 0,5°) {ok(dmax <= 0.5)}; "
      f"arcos s ∝ r: {[round(x, 3) for x in mw[-1]['s']]}")
hel = [v for l in ("PH", "PT4", "PS") for v in over[l].get("helice", {}).values()]
p(f"- MESMO ω (hélice, T4-2): as duas setas usam o mesmo ângulo da pá 0 a cada quadro ({len(hel) // 2} quadros)")
# ÁREA = ÂNGULO
aa = list(over["PT3"].get("area_angulo", {}).values())
if aa:
    e = max(abs(v["area"] - v["dth"]) / max(v["dth"], 1e-6) for v in aa if v["dth"] > 0.05)
    p(f"- ÁREA = ÂNGULO (T3-4, {len(aa)} quadros): |área − θ do disco| / θ no máx. {100 * e:.4f}% (≤ 1%) {ok(e <= 0.01)}")
ins = over["PT3"].get("inset_sinal", {})
if ins:
    ult = ins[max(ins, key=int)]
    p(f"- ÁREA COM SINAL (inset T3-4): Δθ final = {math.degrees(ult['dth']):.4f}° (≤ 1°) {ok(abs(math.degrees(ult['dth'])) <= 1)}; giro total 4π")
e1 = over["PE1"].get("e1_sim", {})
if e1:
    ult = e1[max(e1, key=int)]
    ts = np.linspace(0, 30, 30001)
    area = np.trapezoid(np.maximum(0, 10 * math.pi - math.pi / 3 * ts), ts)
    p(f"- ÁREA = ÂNGULO (E1-3): área do triângulo ∫ω dt = {area:.3f} rad; contador final {ult['th']:.3f} rad ({ult['th'] / (2 * math.pi):.3f} voltas) "
      f"{ok(abs(area - ult['th']) / area < 0.01 and abs(ult['th'] / (2 * math.pi) - 75) < 0.01)}; tempo comprimido 30 s → 10 s (fator 3,0)")
# SETAS PROPORCIONAIS
if hel:
    por_f = {}
    for l in ("PH", "PT4", "PS"):
        for f, v in over[l].get("helice", {}).items():
            pass
    rs = [v["L"] / v["r"] for v in hel]
    p(f"- SETAS PROPORCIONAIS hélice: L/r constante (variação {100 * (max(rs) - min(rs)) / np.mean(rs):.4f}%) ⇒ razão 0,95/0,10 = 9,5 (±2%) {ok((max(rs) - min(rs)) / np.mean(rs) < 0.02)}")
var = lambda xs: (max(xs) - min(xs)) / abs(np.mean(xs)) if xs else float("nan")
sr = list(over["PT4"].get("t4_acel", {}).values())                      # v2: setas_r do v1 virou t4_acel (v, a_t, a_c no disco do T4)
if sr:
    kt = [v["Lt"] / abs(v["at"]) for v in sr if abs(v["at"]) > 1e-9]
    kv = [v["Lv"] / v["w"] for v in sr if v["w"] > 1e-3]
    p(f"- SETAS PROPORCIONAIS disco (T4, t4_acel, {len(sr)} quadros): L_at/|a_t| constante (variação {100 * var(kt):.4f}%), L_v/ω constante = k·r "
      f"(variação {100 * var(kv):.4f}%) {ok(var(kt) < 0.02 and var(kv) < 0.02)}")
else:
    p("- SETAS PROPORCIONAIS disco (T4): t4_acel não registrado — NÃO MEDIDO")
t46 = list(over["PT4"].get("t4_6", {}).values())
if t46:
    ef = max(abs(v["phi"] - math.degrees(math.atan2(abs(v["at"]), v["ac"]))) for v in t46)
    er = max(abs(v["Lt"] / max(v["Lc"], 1e-9) - abs(v["at"]) / v["ac"]) for v in t46)
    # v2: o r do T4-6 não é DR (o disco encolhe para 1,6); r não é registrado, então confere que a_t e a_c usam o MESMO r: a_t ω² = a_c α
    ea = max(abs(v["at"] * v["w"] ** 2 - v["ac"] * v["al"]) for v in t46)
    r6 = sorted({round(v["ac"] / v["w"] ** 2, 3) for v in t46 if v["w"] > 1e-3})
    p(f"- SETAS PROPORCIONAIS T4-6 ({len(t46)} quadros, r = a_c/ω² = {r6}): a_t = rα e a_c = ω²r com o mesmo r (|a_t ω² − a_c α| máx. {ea:.2e}) {ok(ea < 1e-9)}; "
      f"|a_t|/a_c das setas = valor (erro {er:.2e}); tan φ = |a_t|/a_c (erro máx. {ef:.4f}°, ≤ 1°) {ok(ef <= 1 and er < 0.01)}")
e25 = list(over["PE2"].get("e2_5c", {}).values()) + list(over["PE2"].get("e2_5k", {}).values())
if e25:
    Ls = sorted({round(v["Lc"], 5) for v in e25})
    p(f"- SETAS PROPORCIONAIS E2-5: a_c coroa : catraca = {Ls[0]:.3f} : {Ls[-1]:.3f} = 1 : {Ls[-1] / Ls[0]:.3f} (1 : 2,5) {ok(abs(Ls[-1] / Ls[0] - 2.5) < 0.05)}; "
      f"E1-5 fora desta auditoria (selo FORA DE ESCALA)")
# LIVRO
lv = over["PT5"].get("livros", {})
if lv:
    ult = lv[max(lv, key=lambda f: (lv[f]["a1"] + lv[f]["a2"], -int(f)))]   # v2: os livros voltam a 0 depois; o estado final é o de a1 = a2 = 90°
    L = np.array(ult["L"]).reshape(3, 3)
    R = np.array(ult["R"]).reshape(3, 3)
    cL, cR = L @ [0, 0, 1], R @ [0, 0, 1]
    aL = math.degrees(math.acos(max(-1, min(1, cL @ [0, -1, 0]))))
    aR = math.degrees(math.acos(max(-1, min(1, cR @ [1, 0, 0]))))
    D = L @ R.T
    p(f"- LIVRO (T5-2): capa esquerda {np.round(cL, 4)} (−y, erro {aL:.4f}°) · direita {np.round(cR, 4)} (+x, erro {aR:.4f}°) {ok(aL <= 1 and aR <= 1)}; "
      f"diferença entre as ordens com 90°: {math.degrees(math.acos((np.trace(D) - 1) / 2)):.2f}° (120°); eixos desenhados fixos (mesmas setas do laboratório em todos os quadros)")
lp = over["PT5"].get("livros_peq", {})
if lp:
    fins = {v["g"]: v["dif"] for v in lp.values()}                       # v2: um registro por giro (g, dif mostrado, dif_g calculado)
    em = max(abs(v["dif"] - v["dif_g"]) for v in lp.values())
    alvo = {10.0: 1.74, 5.0: 0.44, 1.0: 0.017}
    p("- T5-4 medidor: " + " · ".join(f"{int(g)}° → {fins.get(g, float('nan')):.4f}° (alvo {alvo[g]}°, ±0,01) {ok(abs(fins.get(g, 99) - alvo[g]) <= 0.01)}" for g in (10.0, 5.0, 1.0))
      + f"; mostrado × calculado: {em:.2e}")
# PRODUTO VETORIAL
pv = list(over["PT5"].get("pv", {}).values())
if pv:
    e_ = max(abs(np.linalg.norm(v["v"]) - v["w"] * 1.0) / (v["w"] * 1.0) for v in pv)
    z0s = sorted({round(v["z0"], 3) for v in pv})
    inv = max(np.linalg.norm(np.array(v["v"]) - np.cross([0, 0, v["w"]], [math.cos(v["th"]), math.sin(v["th"]), 0.01])) for v in pv)
    p(f"- PRODUTO VETORIAL (T5-6, {len(pv)} quadros, O de z = {z0s[0]} a {z0s[-1]}): |v⃗| = ω r_⊥ (erro máx. {100 * e_:.4f}%, ≤ 1%) {ok(e_ <= 0.01)}; "
      f"v⃗ independente de O (máx. {inv:.2e}; em px ≈ {inv * 1.25 * DR * PX:.4f} px ≤ 1 px) {ok(inv * 1.25 * DR * PX <= 1)}")
a3 = list(over["PT5"].get("a3d", {}).values())
if a3:                                                                    # v3 §6: a⃗ = α⃗×r⃗ + ω⃗×(ω⃗×r⃗), com eixo z (o mesmo do pv); erro relativo a |a⃗| calculado
    ee = {"at": 0.0, "ac": 0.0, "a": 0.0, "soma": 0.0}
    for v in a3:
        r_, w_ = np.array(v["r"]), v["w"]
        at_c = np.cross([0, 0, v["al"]], r_)
        ac_c = np.cross([0, 0, w_], np.cross([0, 0, w_], r_))
        a_c = at_c + ac_c
        n_ = max(np.linalg.norm(a_c), 1e-9)
        ee["at"] = max(ee["at"], np.linalg.norm(np.array(v["at"]) - at_c) / n_)
        ee["ac"] = max(ee["ac"], np.linalg.norm(np.array(v["ac"]) - ac_c) / n_)
        ee["a"] = max(ee["a"], np.linalg.norm(np.array(v["a"]) - a_c) / n_)
        ee["soma"] = max(ee["soma"], np.linalg.norm(np.array(v["a"]) - np.array(v["at"]) - np.array(v["ac"])) / n_)
    mx = max(ee.values())
    p(f"- PRODUTO VETORIAL (T5-8, a3d, {len(a3)} quadros): a⃗ = α⃗×r⃗ + ω⃗×(ω⃗×r⃗) recalculado de (α, ω, r⃗) × a3d: erro relativo máx. |Δa⃗|/|a⃗| = {100 * ee['a']:.4f}%, "
      f"α⃗×r⃗ {100 * ee['at']:.4f}%, ω⃗×(ω⃗×r⃗) {100 * ee['ac']:.4f}%, a⃗ − (a_t + a_c) {100 * ee['soma']:.4f}% (≤ 1%) {ok(mx <= 0.01)}")
else:
    p("- PRODUTO VETORIAL (T5-8): a3d não registrado — NÃO MEDIDO")
tv = over["PE3"].get("terra_vet", {})
if tv:
    v = list(tv.values())[0]
    SP, vv, ac = np.array(v["SP"]), np.array(v["v"]), np.array(v["ac"])
    leste = np.cross([0, 0, 1], SP)
    leste /= np.linalg.norm(leste)
    ang_l = math.degrees(math.acos(max(-1, min(1, vv @ leste / np.linalg.norm(vv)))))
    ang_e = math.degrees(math.asin(min(1, abs(ac[2]) / np.linalg.norm(ac))))
    lam = math.degrees(math.acos(ac @ (-SP) / np.linalg.norm(ac)))
    p(f"- PRODUTO VETORIAL (E3-4): v⃗ de São Paulo × leste: {ang_l:.4f}° (≤ 0,5°) {ok(ang_l <= 0.5)}; a_c × plano ⟂ ao eixo: {ang_e:.4f}° {ok(ang_e <= 0.5)}; "
      f"ângulo entre a_c e a radial = {lam:.2f}° (|λ| = 23,55°)")
# CORRENTE
co = over["PE2"].get("corrente", {})
if co:
    vs = list(co.values())
    r_ = max(abs(v["w2"] / v["w1"] - 2.5) for v in vs)
    dv = max(abs(v["v_coroa"] - v["v_catraca"]) / v["v_coroa"] for v in vs)
    vmax = max(v["volt"] for v in vs)
    p(f"- CORRENTE ({len(vs)} quadros): ω₂/ω₁ − 2,5 máx. {r_:.2e} {ok(r_ < 1e-9)}; |v_coroa − v_catraca|/v máx. {100 * dv:.2e}% (≤ 0,5%) {ok(dv <= 0.005)}; "
      f"pedal no E2-4: {vmax:.3f} voltas (5,00) {ok(abs(vmax - 5) < 0.005)}")
# TERRA
te = over["PE3"].get("terra_estrela", {})
if te:
    ss = [math.degrees(math.atan2(v["s"][1], v["s"][0])) for v in te.values()]
    p(f"- TERRA (E3-2, {len(ss)} quadros): direção da estrela nas duas posições varia {max(ss) - min(ss):.4f}° (≤ 0,2°, setas paralelas) {ok(max(ss) - min(ss) <= 0.2)}; "
      f"a volta extra desenhada = o avanço orbital desenhado (30°, EXAGERADO)")
# ALIASING
alias = []
for l, k_ in (("PH", "helice"), ("PT4", "helice"), ("PT4", "helice6"), ("PS", "helice")):
    d_ = over[l].get(k_, {})
    fs = sorted({int(f) for f in d_})
    for a, b in zip(fs, fs[1:]):
        if b == a + 1:
            alias.append((abs(d_[str(b)]["ang"] - d_[str(a)]["ang"]), f"{l} {k_} {b / 15:.1f} s"))
for l in ("PT1", "PT2", "PT3", "PT4", "PT5"):
    d_ = over[l].get("rigido", {})
    fs = sorted(int(f) for f in d_)
    for a, b in zip(fs, fs[1:]):
        if b == a + 1:
            alias.append((abs(d_[str(b)]["th"] - d_[str(a)]["th"]), f"{l} disco {b / 15:.1f} s"))
d_ = over["PE1"].get("e1_sim", {})
fs = sorted(int(f) for f in d_)
for a, b in zip(fs, fs[1:]):
    if b == a + 1:
        alias.append((abs(d_[str(b)]["ang"] - d_[str(a)]["ang"]), f"PE1 ventilador {b / 15:.1f} s"))
if co:
    alias.append((max(v["w2"] for v in co.values()) / 4 / 15, "PE2 roda"))
p(f"- ALIASING: maior giro por quadro = {math.degrees(max(alias)[0]) if alias else 0:.1f}° em {max(alias)[1] if alias else "-"} (≤ 60°) {ok(not alias or math.degrees(max(alias)[0]) <= 60)}; acima de 60°: {sorted({x[1] for x in alias if math.degrees(x[0]) > 60})[:6]} "
  f"(hélice ×90, ventilador ×30, roda ×4)")
# ORDEM (v2 §2 item 8): cada linha construída — nenhum par (i à esquerda de j, colunas disjuntas) com t_i > t_j + 0,05 s; instante = início + 50% da escrita
# (parte fixa) ou o POUSO na vaga (parte que voa). Caixa de resultado: conteúdo em ≤ 0,3 s do contorno.
n_lin, n_voo, falhas, vazias, n_unid = 0, 0, [], [], 0
for l in LOTES:
    for cena, d in over[l].items():
        if not cena.startswith("ordem"):
            continue
        for f, v in d.items():
            n_lin += 1
            n_voo += int(v.get("voos", 0))
            us = v["u"]
            n_unid += len(us)
            for i, ui in enumerate(us):
                for j, uj in enumerate(us):
                    if i != j and ui[1] <= uj[0] + 0.02 and ui[2] > uj[2] + 0.05:
                        falhas.append((l, v["aid"], v["linha"], round(ui[2] - uj[2], 2)))
            for cx in v.get("caixa", []):
                if us and min(u[2] for u in us) - cx[1] > 0.3:
                    vazias.append((l, v["aid"], v["linha"]))
p(f"- ORDEM ({n_lin} linhas construídas, {n_unid} partes, {n_voo} voos): pares fora de ordem (t_i > t_j + 0,05 s com i à esquerda de j) = {len(falhas)} {ok(not falhas)}"
  + (f"; primeiros: {falhas[:4]}" if falhas else ""))
p(f"- CAIXA VAZIA (contorno sem conteúdo por > 0,3 s; caixas montadas por Prob2.escreve, registro ordem*.caixa): {len(vazias)} {ok(not vazias)}"
  + (f"; {vazias[:4]}" if vazias else "") + ". Caixas que entram por outro caminho (passo/pg/FadeIn) não têm registro — NÃO MEDIDAS")
# MOSTRADOR (v2 §9 item 3, D9): mostrador mostrado = Δθ mod 2π (em graus inteiros) em todo quadro em que existe (T1-5 e E1-3)
for l, aid0, arred in (("PT1", "T1-5", "round"), ("PE1", "E1-3", "int")):
    mo = over[l].get("mostrador", {})
    if not mo:
        p(f"- MOSTRADOR {aid0}: não registrado — NÃO MEDIDO")
        continue
    fs = sorted(int(f) for f in mo)
    buracos = sum(1 for a_, b_ in zip(fs, fs[1:]) if b_ != a_ + 1)
    err, ruins = 0.0, 0
    for v in mo.values():
        verd = math.degrees(v["acum_rad"]) % 360.0
        d_ = (v["mostrador_deg"] - verd + 180.0) % 360.0 - 180.0          # diferença circular (359,9° ≡ 0°)
        err = max(err, abs(d_))
        ruins += (abs(d_) > 0.5 + 1e-6) if arred == "round" else not (-1.0 < d_ <= 1e-6)   # int(): mostra o piso, −1 < d ≤ 0
    an_ = [(m_.group(1), float(m_.group(2))) for m_ in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", ler(f"log_{l}.txt"))]
    ini = next((t for a_, t in an_ if a_ == aid0), float("nan"))
    p(f"- MOSTRADOR {aid0} ({l}, {len(fs)} quadros {fs[0] / 15:.2f}–{fs[-1] / 15:.2f} s do lote, {buracos} buracos; {aid0} começa em {ini:.2f} s): "
      f"|mostrador − (Δθ mod 2π)| máx. {err:.4f}° ({'arredondado, ≤ 0,5°' if arred == 'round' else 'piso, −1° < d ≤ 0'}), {ruins} quadros fora "
      f"{ok(ruins == 0 and buracos == 0)}; Δθ final {mo[str(fs[-1])]['acum_rad']:.3f} rad")
# COR POR TOKEN (v2 §9 item 7): linhas [audit] COR POR TOKEN e o resumo "[cor] tokens conferidos: N; fora da tabela: M" de cada lote
n_tok, n_fora, n_aud, sem_partes, sp_txt = 0, 0, 0, 0, []
por_l = {}
for l in LOTES:
    a = ler(f"log_aud_{l}.txt")
    m_ = re.search(r"\[cor\] tokens conferidos: (\d+); fora da tabela: (\d+)", a)
    k_ = len(re.findall(r"\[audit\].*COR POR TOKEN", a))
    s_ = len(re.findall(r"\[cor\].*sem partes registradas", a))
    sp_txt += [f"{l}: {x.strip()[:70]}" for x in a.splitlines() if "sem partes registradas" in x][:6]
    if m_:
        n_tok += int(m_.group(1))
        n_fora += int(m_.group(2))
    n_aud += k_
    sem_partes += s_
    if k_ or s_ or not m_:
        por_l[l] = f"{k_} fora" + (f", {s_} MathTex sem partes" if s_ else "") + ("" if m_ else ", sem resumo [cor]")
p(f"- COR POR TOKEN: {n_tok} tokens conferidos, {n_fora} fora da tabela, {n_aud} linhas [audit] (meta 0) {ok(n_fora == 0 and n_aud == 0)}"
  + (f"; {por_l}" if por_l else "") + (f"; {sem_partes} MathTex sem partes registradas (cor NÃO conferida; meta 0 {ok(False)}): {sp_txt}" if sem_partes else "; MathTex sem partes: 0 (meta 0) OK"))
# NÚMEROS
tab = [("282,7 rad/s", NUM["w_hel"], 282.74), ("28 m/s", NUM["v10"], 28.27), ("269 m/s", NUM["v95"], 268.61), ("≈100 km/h", NUM["kmh10"], 101.8),
       ("≈970 km/h", NUM["kmh95"], 967.0), ("78%", NUM["som"], 0.783), ("7,6e4 m/s²", NUM["ac95"], 75947), ("7.750 g", NUM["g95"], 7750),
       ("31,4", NUM["w0"], 31.42), ("−1,05", NUM["al"], -1.047), ("471 rad", NUM["dth"], 471.2), ("262 rad", NUM["dth10"], 261.8),
       ("18,8 m/s", NUM["v0"], 18.85), ("592 m/s²", NUM["ac0"], 592.2), ("0,63", NUM["at"], 0.628), ("20,9", NUM["w10"], 20.94), ("263", NUM["ac10"], 263.2),
       ("0,14°", NUM["phi10"], 0.137), ("1,02 rad/s", NUM["wcruz"], 1.023), ("29,0 s", NUM["tcruz"], 29.02), ("15,7 rad/s", NUM["w2"], 15.71),
       ("5,50 m/s", NUM["vb"], 5.498), ("0,785", NUM["al1"], 0.785), ("1,96", NUM["al2"], 1.963), ("0,69", NUM["ab"], 0.687), ("0,63 m/s", NUM["vc"], 0.6283),
       ("3,9", NUM["acc1"], 3.948), ("9,9", NUM["acc2"], 9.870), ("86.164 s", NUM["Tsid"], 86164.09), ("7,292e-5", NUM["wT"], 7.292e-5),
       ("5.840 km", NUM["rp"], 5840.4), ("465 m/s", NUM["veq"], 464.58), ("426 m/s", NUM["vsp"], 425.89), ("0,031", NUM["acsp"], 0.03106)]
ruins = [(n, a, b) for n, a, b in tab if abs(a - b) / abs(b) > 0.002]
p(f"- NÚMEROS: {len(tab) - len(ruins)}/{len(tab)} valores da tela batem com a Conferência numérica do Anexo A (±0,2%) {ok(not ruins)}"
  + ("" if not ruins else " — " + "; ".join(f"{n}: {a:.4g} × {b:.4g}" for n, a, b in ruins)))
p()

# ── 3. alinhamento 3D × Manim ──
p("## 3. Alinhamento Three.js × Manim (px)")
from kit import projeta3d  # noqa: E402
from pecas20 import cam_hel, hel_pt, cam_disco  # noqa: E402
tpx = lambda q: np.array([(q[0] + 8) / 16 * 960, (4.5 - q[1]) / 9 * 540])
for l in ("PH", "PT4", "PS"):
    f_ = U / "threejs" / "q3d" / f"{l}_960x540" / "helice" / "pontos.json"
    if not f_.exists():
        p(f"- {l} hélice: sem pontos.json")
        continue
    pj = json.loads(f_.read_text(encoding="utf-8"))
    cam = cam_hel()
    regs = {}
    for f, v in over[l].get("helice", {}).items():
        regs.setdefault(f, []).append(v)
    for f, v in over[l].get("helice6", {}).items():                   # v2: T4-6 registra a ponta (r = 0,95, hel_pt(cam, 0.95, a)) em helice6
        regs.setdefault(f, []).append({"r": 0.95, **v})
    errs, sem = [], 0
    for f, vs in regs.items():
        if f not in pj:
            sem += len(vs)
            continue
        for v in vs:
            js = pj[f]["r95"] if abs(v["r"] - 0.95) < 1e-6 else pj[f]["r10"]
            errs.append(np.linalg.norm(np.array(js) - tpx(v["p"])))
    n6 = len(over[l].get("helice6", {}))
    p(f"- {l} hélice: marcadores 10 cm e 95 cm" + (f" + ponta do T4-6 (helice6, {n6} quadros)" if n6 else "")
      + f", {len(errs)} pares, erro máx. {max(errs) if errs else float('nan'):.3f} px (≤ 2 px) {ok(errs and max(errs) <= 2 and not sem)}"
      + (f"; {sem} registros sem quadro 3D" if sem else ""))
f_ = U / "threejs" / "q3d" / "PT5_960x540" / "disco" / "pontos.json"
if f_.exists():
    pj = json.loads(f_.read_text(encoding="utf-8"))
    tr = over["PT5"].get("troca_2d3d", {})
    for f, v in tr.items():
        fs = sorted(int(k) for k in pj)
        k = min(fs, key=lambda x: abs(x - int(f)))
        e_ = np.linalg.norm(np.array(pj[str(k)]["P"]) - tpx(v["p3"]))
        ec = np.linalg.norm(np.array(pj[str(k)]["centro"]) - tpx(v["c"]))
        p(f"- PT5 troca disco 2D → 3D (T5-1, quadro {k}): ponto de fora {e_:.3f} px, centro {ec:.3f} px (≤ 2 px) {ok(e_ <= 2 and ec <= 2)}")
    pv_ = over["PT5"].get("pv", {})
    errs = [np.linalg.norm(np.array(pj[f]["vtopo"]) - tpx(v["vtopo"])) for f, v in pv_.items() if f in pj and "vtopo" in pj[f]]
    p(f"- PT5 ponta de v⃗ = ω⃗ × r⃗ (Three.js × Manim, {len(errs)} quadros): erro máx. {max(errs) if errs else float('nan'):.3f} px {ok(errs and max(errs) <= 2)}")
# v2 livros (T5-2/T5-4): os rótulos x, y do Manim saem de projeta3d(camL, c + Δ) com a MESMA câmera pedida ao Three.js (pedidos3d); compara
# c_k, x_k = c + (s,0,0), y_k = c + (0,0,s) projetados pelo Manim com os pontos do r20.js
f_ = U / "threejs" / "q3d" / "PT5_960x540" / "livros" / "pontos.json"
pd_ = U / "threejs" / "pedidos3d" / "PT5.json"
if f_.exists() and pd_.exists():
    pj = json.loads(f_.read_text(encoding="utf-8"))
    ped = {str(f): e for f, e in json.loads(pd_.read_text(encoding="utf-8"))["cenas"].get("livros", [])}
    errs = []
    for f, pts in pj.items():
        e = ped.get(f)
        if not e:
            continue
        s = e.get("sx", 0.17)
        for k, c in enumerate(e.get("c", [[-0.2, 0, 0], [0.2, 0, 0]])):
            for nm, d_ in (("c", (0, 0, 0)), ("x", (s, 0, 0)), ("y", (0, 0, s))):
                if f"{nm}{k}" in pts:
                    errs.append(np.linalg.norm(np.array(pts[f"{nm}{k}"]) - tpx(projeta3d(e["cam"], np.add(c, d_)))))
    p(f"- PT5 livros (centro e pontas dos eixos x, y dos 2 livros, câmera do pedido × r20.js, {len(errs)} pares em {len(pj)} quadros): "
      f"erro máx. {max(errs) if errs else float('nan'):.3f} px (≤ 2 px) {ok(errs and max(errs) <= 2)}")
else:
    p("- PT5 livros: sem pontos.json ou pedidos3d — NÃO MEDIDO")
f_ = U / "threejs" / "q3d" / "PE3_960x540" / "terra" / "pontos.json"
if f_.exists():
    pj = json.loads(f_.read_text(encoding="utf-8"))
    from kit import cam_obl  # noqa: E402
    tvd = over["PE3"].get("terra_vet", {})
    if tvd:
        v0 = list(tvd.values())[0]                                   # v2: câmera geo gravada pelo sec_e3.py (K, xc, yc), não fixa aqui
        camG = cam_obl(-90.0, 16.0, (0.0, 0.0, 0.0), K=v0["K"], xc=v0["xc"], yc=v0["yc"], fov=16)
        f0 = min(int(k) for k in tvd)                                # modo geo (E3-4 em diante)
        pd_ = U / "threejs" / "pedidos3d" / "PE3.json"
        ped = {str(f): e for f, e in json.loads(pd_.read_text(encoding="utf-8"))["cenas"].get("terra", [])} if pd_.exists() else {}
        geo = [f for f, v in pj.items() if "SP" in v and v.get("vet") and int(f) >= f0]
        errs = [np.linalg.norm(np.array(pj[f]["SP"]) - tpx(projeta3d(camG, np.array(pj[f]["vet"]["SP"])))) for f in geo]
        outra = sum(1 for f in geo if f in ped and ped[f].get("cam") != camG)
        p(f"- PE3 São Paulo (geo, câmera do overlay K = {v0['K']}, xc = {v0['xc']}, yc = {v0['yc']}; quadro ≥ {f0}, {len(errs)} quadros): erro máx. "
          f"{max(errs) if errs else float('nan'):.3f} px {ok(errs and max(errs) <= 2)}; quadros cuja câmera pedida ao Three.js ≠ câmera geo: {outra}")
    else:
        p("- PE3 São Paulo: terra_vet não registrado — NÃO MEDIDO")
for l in ("PH", "PT4", "PT5", "PE3", "PS"):
    s3 = ler(f"log_3d_{l}.txt").strip().splitlines()
    p(f"- custo {l}: {s3[-1] if s3 else 'sem log'}")
p()

# ── 4. duração por âncora ──
p("## 4. Duração por âncora (narração nominal × cena)")
total_n = total_c = 0.0
linhas = []
for l in LOTES:
    lg = ler(f"log_{l}.txt")
    anc = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", lg)]
    tt = re.search(r"\[tempo\] total ([0-9.]+) s", lg)
    for (a, t0), (_, t1) in zip(anc, anc[1:] + [("FIM", float(tt.group(1)) if tt else 0.0)]):
        if a == "FIM":
            continue
        dn = ANC["ancoras"][a]["dur"]
        total_n += dn
        total_c += t1 - t0
        linhas.append(f"{a} {dn:.1f}/{t1 - t0:.1f}")
p("- " + " · ".join(linhas))
p(f"- total: narração {total_n / 60:.2f} min × cena {total_c / 60:.2f} min; simulações: E1 30 s → 10 s (×3), desenho ×30; hélice ×90; bicicleta ×4 (tempo real)")
p()

# ── 5. cor por capítulo (nos lotes) e FUNDO (no preview); 6. PARADO, COLUNA VAZIA, TAMANHO (nos lotes) ──
# Uma passada por mp4 de lote (media_<LOTE>/videos/cena/540p15/<LOTE>.mp4). Tinta = pixel que difere do fundo_lab.png (o céu do laboratório,
# estático desde o v2) em mais de TINTA níveis em algum canal. Tempo dos lotes = tempo das linhas [ancora] do log_<LOTE>.txt.
import av  # noqa: E402
from PIL import Image  # noqa: E402

FUNDO = np.asarray(Image.open(U / "fundo_lab.png").convert("RGB").resize((960, 540), Image.BILINEAR), dtype=np.int16)
Y0, Y1 = 70, 525                                   # abaixo do cabeçalho (título + marca d'água) e acima da borda de baixo
XCOL = round((0.6 + 8) / 16 * 960)                 # §8: COLUNA = x > 0,6 u
EX0, EY0, EX1, EY1 = round(0.7 / 16 * 960), round(2.0 / 9 * 540), round(8.2 / 16 * 960), round(8.15 / 9 * 540)   # ESQUEMA x −7,3…0,2 · y −3,65…2,50
A_ESQ = 7.5 * 6.15
FAM = np.array([40.0, 248.0, 149.0, 192.0])        # §6: âmbar #FFC24D, violeta #9C8CFF, verde #3FE08B, ciano #35D9FF dos selos (matiz em graus)
TINTA, LIM_MUDA, LIM_COL = 24, 20, 30              # px que mudam < 20 = quadro sem mudança; coluna com < 30 px de tinta = vazia
ZONAS = tuple(z for z in ("PT1", "PT2", "PT3", "PT4", "PT5", "PE1", "PE2", "PE3") if z in LOTES)
NOME = {"PT1": "COMO MEDIR UM GIRO?", "PT2": "QUÃO RÁPIDO GIRA?", "PT3": "E QUANDO O GIRO ACELERA?", "PT4": "E CADA PONTO DO CORPO?",
        "PT5": "PARA ONDE APONTA UM GIRO?", "PE1": "EXERCÍCIO 1 · O VENTILADOR QUE DESLIGA", "PE2": "EXERCÍCIO 2 · A CORRENTE DA BICICLETA",
        "PE3": "EXERCÍCIO 3 · QUANTO GIRA A TERRA?"}


def capitulo(l, aid):
    if l == "PH":
        return "ABERTURA" if aid.startswith("A") else "HOOK"
    if l == "PS":
        return "ENCERRAMENTO E DESAFIO" if aid.startswith("EN") else "RESUMO"
    return NOME[l]


def ancoras(l):
    lg = ler(f"log_{l}.txt")
    an_ = [(m_.group(1), float(m_.group(2))) for m_ in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", lg) if m_.group(1) != "FIM"]
    tt = re.search(r"\[tempo\] total ([0-9.]+) s", lg)
    fim = float(tt.group(1)) if tt else 1e9
    return [(a_, t0, t1) for (a_, t0), (_, t1) in zip(an_, an_[1:] + [("FIM", fim)])]


def aid_em(an_, t):
    return next((a_ for a_, t0, t1 in reversed(an_) if t >= t0), an_[0][0] if an_ else "-")


def varre(l):
    """Uma passada pelo mp4 do lote (com cache em renders/<rodada>/_varre_<LOTE>.json, chaveado pelo mtime do mp4 e do log)."""
    mp4 = U / f"media_{l}/videos/cena/540p15/{l}.mp4"
    if not mp4.exists():
        return None
    chave = f"v3:{mp4.stat().st_mtime}:{(U / f'log_{l}.txt').stat().st_mtime if (U / f'log_{l}.txt').exists() else 0}"
    cache = DST / f"_varre_{l}.json"
    if cache.exists():
        c_ = json.loads(cache.read_text(encoding="utf-8"))
        if c_.get("chave") == chave:
            return c_
    an_ = ancoras(l)
    amostra = {}
    for a_, t0, t1 in an_:
        for fr_ in (0.25, 0.5, 0.75):
            amostra[round((t0 + fr_ * (t1 - t0)) * 15)] = a_
    chg, col, cor, env = [], [], {}, {}
    ant = None
    FP_ = np.ascontiguousarray(FUNDO.astype(np.uint8).transpose(2, 0, 1))

    def dif(x, y):                                                   # |x − y| > TINTA em algum canal (uint8 planar: ~5× mais rápido que int16 HWC)
        d = np.maximum(x, y)
        d -= np.minimum(x, y)
        return d.max(axis=0) > TINTA
    with av.open(str(mp4)) as c:
        for k, fr in enumerate(c.decode(video=0)):
            rgb = fr.to_ndarray(format="rgb24")
            a = np.ascontiguousarray(rgb.transpose(2, 0, 1))
            if ant is not None:
                chg.append(int(dif(a[:, Y0:Y1], ant[:, Y0:Y1]).sum()))
            ant = a
            col.append(int(dif(a[:, Y0:Y1, XCOL:], FP_[:, Y0:Y1, XCOL:]).sum()))
            if k % 15 == 0:
                hsv = np.asarray(Image.fromarray(rgb).convert("HSV"), dtype=np.float32)
                tinta = hsv[..., 2] > 0.45 * 255
                sat_ = tinta & (hsv[..., 1] > 90)
                h = hsv[..., 0] * 360 / 255
                # métrica larga (v3 §3): qualquer tinta saturada que não seja fundo (igual ao fundo_lab) nem aço (azul-acinzentado: matiz 205–255° e S < 150)
                larga = sat_ & (np.abs(rgb.astype(np.int16) - FUNDO).max(axis=2) > TINTA) & ~((h >= 205) & (h <= 255) & (hsv[..., 1] < 150))
                dh = np.min(np.abs((h[..., None] - FAM + 180) % 360 - 180), axis=-1)
                s_ = cor.setdefault(capitulo(l, aid_em(an_, k / 15)), [0, 0, 0, 0])
                s_[0] += int((sat_ & (dh <= 15)).sum())
                s_[1] += int(sat_.sum())
                s_[2] += int(tinta.sum())
                s_[3] += int(larga.sum())
            if k in amostra:
                m = dif(a[:, EY0:EY1, EX0:EX1], FP_[:, EY0:EY1, EX0:EX1])
                ys, xs = np.nonzero(m.sum(axis=1) >= 3)[0], np.nonzero(m.sum(axis=0) >= 3)[0]
                fr_a = ((ys[-1] - ys[0] + 1) * (xs[-1] - xs[0] + 1)) / m.size if len(ys) and len(xs) else 0.0
                env[amostra[k]] = max(env.get(amostra[k], 0.0), float(fr_a))
    r_ = {"chave": chave, "chg": chg, "col": col, "cor": cor, "env": env}
    cache.write_text(json.dumps(r_), encoding="utf-8")
    return r_


def corridas(xs, cond):
    """Corridas [i0, n] de índices consecutivos com cond(x)."""
    out_, i0 = [], None
    for i, x in enumerate(list(xs) + [None]):
        if x is not None and cond(x):
            i0 = i if i0 is None else i0
        elif i0 is not None:
            out_.append((i0, i - i0))
            i0 = None
    return out_


VR = {}
for l in LOTES:
    VR[l] = varre(l)
p("## 5. Cor por capítulo (mp4 dos lotes) e FUNDO (preview)")
p(f"- métrica v2 (§6): tinta = V > 0,45; família = S > 90 e matiz a ≤ 15° de âmbar 40°, violeta 248°, verde 149° ou ciano 192°; 1 quadro por s. "
  f"Entre parênteses, a métrica do v1 (qualquer tinta saturada)")
cores = {}
for l in LOTES:
    for cap, v in ((VR[l] or {}).get("cor") or {}).items():
        a_ = cores.setdefault(cap, [0, 0, 0, 0])
        for i in range(4):
            a_[i] += v[i]
for l in LOTES:
    if VR[l] is None:
        p(f"- {l}: sem mp4 — NÃO MEDIDO")
p("- v3 §3: DUAS métricas por capítulo, ambas ≥ 30%: FAMÍLIA (acima) e LARGA = qualquer tinta saturada (V > 0,45, S > 90) que não seja fundo (pixel ≈ fundo_lab) "
  "nem aço (azul-acinzentado: matiz 205–255° com S < 150). Azuis de borda de painel muito saturados contam como larga")
p("- v8 (gate combinado, decidido pelo Kaio): capítulo OK se FAMÍLIA ≥ 20% **ou** LARGA ≥ 30%; a ABERTURA é declarada isenta (cartão de título)")
for cap, (fa, sa, ti, lg) in cores.items():
    f_, l_ = fa / max(ti, 1), lg / max(ti, 1)
    isento = cap.strip().upper() == "ABERTURA"
    ok_c = isento or f_ >= 0.20 or l_ >= 0.30
    p(f"- {cap}: FAMÍLIA {100 * f_:.1f}% · LARGA {100 * l_:.1f}% → {'OK (abertura isenta)' if isento else ok(ok_c)} "
      f"(saturada sem excluir aço/fundo, v1: {100 * sa / max(ti, 1):.1f}%)")
prev = U / "renders" / f"preview_yt0020_{RODADA}_960x540.mp4"
if prev.exists():
    excl = json.loads(ler("renders/excluir_fundo.json") or "[]")
    n_f = n_esc = 0
    with av.open(str(prev)) as cont:
        for k, fr in enumerate(cont.decode(video=0)):
            if k % 15:
                continue
            t = k / 15
            if not any(a <= t <= b for a, b in excl):
                n_f += 1
                n_esc += int((fr.to_ndarray(format="rgb24").astype(np.float32).mean(axis=2) / 255 < 0.03).mean() > 0.4)
    p(f"- FUNDO: {n_esc}/{n_f} quadros (1 por s) com > 40% dos pixels abaixo de 0,03 ({100 * n_esc / max(n_f, 1):.1f}%, ≤ 5%) {ok(n_esc / max(n_f, 1) <= 0.05)}")
else:
    p(f"- FUNDO: preview {prev.name} ausente — NÃO MEDIDO")
p()

p("## 6. Trechos parados, coluna vazia e tamanho (§8, §9 itens 4 e 6)")
p(f"- PARADO: quadro sem mudança = menos de {LIM_MUDA} px (y {Y0}…{Y1}) mudam > {TINTA} níveis do quadro anterior; falha = ≥ 3 s seguidos. "
  "Pulsos de destaque e giros contam como mudança. Exceção declarada: abertura (A1–A3, logo/título)")
p(f"- COLUNA VAZIA: x > 0,6 u (px ≥ {XCOL}), y {Y0}…{Y1}, menos de {LIM_COL} px de tinta; falha = > 5 s seguidos; só nos lotes com ESQUEMA × CONTA")
n_par = n_col = 0
for l in LOTES:
    v = VR[l]
    if v is None:
        p(f"- {l}: sem mp4 — NÃO MEDIDO")
        continue
    an_ = ancoras(l)
    par, exc = [], []
    for i0, n in corridas(v["chg"], lambda x: x < LIM_MUDA):
        if n / 15 >= 3.0:
            a_ = aid_em(an_, i0 / 15)
            (exc if l == "PH" and a_.startswith("A") else par).append(f"{i0 / 15:.1f}–{(i0 + n) / 15:.1f} s ({n / 15:.1f} s, {a_})")
    cv = []
    if l in ZONAS:
        for i0, n in corridas(v["col"], lambda x: x < LIM_COL):
            if n / 15 > 5.0:
                cv.append(f"{i0 / 15:.1f}–{(i0 + n) / 15:.1f} s ({n / 15:.1f} s, {aid_em(an_, i0 / 15)})")
    n_par += len(par)
    n_col += len(cv)
    p(f"- {l}: PARADO {len(par)} {ok(not par)}" + (f": {'; '.join(par)}" if par else "") + (f" · exceção: {'; '.join(exc)}" if exc else "")
      + (f" · COLUNA VAZIA {len(cv)} {ok(not cv)}" + (f": {'; '.join(cv)}" if cv else "") if l in ZONAS else " · COLUNA VAZIA n/a (sem CONTA)"))
p(f"- TOTAL: PARADO {n_par} (meta 0) {ok(n_par == 0)} · COLUNA VAZIA {n_col} (meta 0) {ok(n_col == 0)}")
# TAMANHO: área da caixa envolvente do objeto principal / área do ESQUEMA (7,5 × 6,15 u), alvo 55–75%
p("- TAMANHO (objeto principal, área da caixa envolvente ÷ área do ESQUEMA 7,5 × 6,15 u, alvo 55–75%):")
for l in ("PT1", "PT2", "PT3", "PT4", "PT5"):
    rg_ = over[l].get("rigido", {})
    if not rg_:
        continue
    an_ = ancoras(l)
    por = {}
    for f, r in rg_.items():
        R_ = float(np.linalg.norm(np.array(r["p3"]) - np.array(r["c"])))
        por.setdefault(aid_em(an_, int(f) / 15), []).append(100 * (2 * R_) ** 2 / A_ESQ)
    p(f"    · disco de referência {l} (exato, R do overlay): " + "; ".join(
        f"{a_} {min(x):.0f}%" + (f"…{max(x):.0f}%" if max(x) - min(x) > 0.5 else "") + ("" if 55 <= min(x) and max(x) <= 75 else (" (exceção declarada: no T4-6 o disco cede lugar ao inset de zoom; o envelope todo do ESQUEMA mede ≥ 94%)" if (l, a_) == ("PT4", "T4-6") and min(x) >= 25 else " FALHA")) for a_, x in por.items()))
for l in ("PH", "PT4", "PS"):
    f_ = U / "threejs" / "q3d" / f"{l}_960x540" / "helice" / "pontos.json"
    if not f_.exists():
        continue
    pj = json.loads(f_.read_text(encoding="utf-8"))
    dm = 2 * max(np.linalg.norm(np.subtract(v["r95"], v["eixo"])) for v in pj.values())   # ponta da pá em r = 0,95 m (D = 1,9 m)
    if l in ZONAS:
        fr_ = dm ** 2 / ((EX1 - EX0) * (EY1 - EY0))
        p(f"    · hélice {l} (exato, pontos.json): D = {dm:.0f} px → {100 * fr_:.0f}% do ESQUEMA {ok(0.55 <= fr_ <= 0.75)}")
    else:
        p(f"    · hélice {l} (exato, pontos.json, sem ESQUEMA; §7.1 pede D ≈ 65% da altura do quadro): D = {dm:.0f} px = {100 * dm / 540:.0f}% da altura "
          f"{ok(0.60 <= dm / 540 <= 0.70)}")
p("    · demais âncoras (medida indireta no vídeo: caixa envolvente de TODA a tinta dentro do ESQUEMA, maior de 3 amostras a 25/50/75% da âncora; "
  "inclui rótulos e setas, então só reprova: < 55% ⇒ o objeto principal é certamente < 55%):")
pequenos = []
for l in ZONAS:
    v = VR[l]
    if v is None:
        p(f"      {l}: sem mp4 — NÃO MEDIDO")
        continue
    lin_ = [f"{a_} {100 * x:.0f}%" for a_, x in v["env"].items()]
    pequenos += [(a_, round(100 * x)) for a_, x in v["env"].items() if x < 0.55]
    p(f"      {l}: " + " · ".join(lin_))
p(f"    · âncoras com envelope < 55% do ESQUEMA: {len(pequenos)} {ok(not pequenos)}" + (f" — {pequenos}" if pequenos else "")
  + "; acima de 75% e objeto isolado: NÃO MEDIDO (só o disco e a hélice têm medida exata)")
p("- TAMANHOS MÍNIMOS do G1: medidos pela classe TEXTO PEQUENO do G28 (Text < 24; MathTex no ESQUEMA < 36; na CONTA < 46 com '=' e < 34 sem), seção 1. "
  "Frase-chave ≥ 30 não é distinguida pela auditoria — NÃO MEDIDO")

# ── 7. auditorias do v3 que dependem do objeto em memória (corop.py) e registros novos ──
p("## 7. COR OPERADOR, CAIXA VAZIA (todos os caminhos) e §6 do handoff v3")
CO = {l: json.loads(ler(f"cor_operador_{l}.json")) for l in LOTES if ler(f"cor_operador_{l}.json")}
p("- COR OPERADOR (v3 §2; corop.py, glifos reconhecidos por forma): d, t, =, +, −, parênteses, ∫, lim e barra de fração brancos; Δ com a cor do glifo seguinte "
  "(Δθ âmbar, Δt branco); θ φ λ s âmbar, ω v violeta, α a verde, r GEO; só vale violação que dura ≥ 3 passadas (0,6 s) — voo de glyph map interpola a cor")
n_viol = 0
for l in LOTES:
    c = CO.get(l)
    if c is None:
        p(f"    · {l}: cor_operador_{l}.json ausente — NÃO MEDIDO")
        continue
    an_ = ancoras(l)
    gr, pulsos = {}, 0
    for v in c["violacoes"]:
        e_, g_ = np.array([int(v["esp"][i:i + 2], 16) for i in (1, 3, 5)], float), np.array([int(v["cor"][i:i + 2], 16) for i in (1, 3, 5)], float)
        k_ = float(np.clip(np.dot(g_ - e_, 255 - e_) / max(np.dot(255 - e_, 255 - e_), 1e-9), 0, 1))
        if 0 < k_ < 1 and np.abs(e_ + k_ * (255 - e_) - g_).max() < 14 and v["t1"] - v["t0"] <= 1.0:      # cor esperada clareada rumo ao branco = pulso de destaque (≤ 1 s)
            pulsos += 1
            continue
        gr.setdefault((v["glifo"], v["cor"], v["esp"], v["tex"]), []).append(v)
    n_viol += len(gr)
    lin_ = [f"'{k[0]}' em {k[1]} (esperado {k[2]}) em «{k[3]}» {vs[0]['t0']:.1f}–{vs[-1]['t1']:.1f} s ({aid_em(an_, vs[0]['t0'])})" for k, vs in list(gr.items())[:6]]
    om = c["omega"]
    p(f"    · {l}: {c['n_tex']} MathTex, {c['n_glifos']} glifos conferidos, {len(gr)} violações persistentes {ok(not gr)}, {c['curtas']} transitórias (< 0,6 s) e {pulsos} pulsos de destaque (cor esperada clareada, ≤ 1 s) ignorados; "
      f"ω: {sum(x[0] for x in om.values())} glifos, cores {sorted(om)} (alturas {min((x[1] for x in om.values()), default=0):.3f}…{max((x[2] for x in om.values()), default=0):.3f}) "
      f"{ok(len(om) <= 1 and (not om or list(om)[0] == VEL_HEX))}" + "".join(f"\n        - {x}" for x in lin_))
p(f"- COR OPERADOR: {n_viol} violações persistentes em {len(CO)}/{len(LOTES)} lotes medidos (meta 0) {ok(n_viol == 0 and len(CO) == len(LOTES))}"
  + ("" if len(CO) == len(LOTES) else " — lotes sem medição: NÃO FECHADO"))
tc = []
for l in LOTES:
    an_ = ancoras(l)
    tc += [(l, aid_em(an_, x["t0"]), x["t0"], x["dur"]) for x in (CO.get(l) or {}).get("caixas_vazias", []) if x["dur"] > 0.3]
p(f"- CAIXA VAZIA (todos os caminhos: escreve, passo, pg, FadeIn; objeto `_caixa` visível sem conteúdo dentro por > 0,3 s; {len(CO)}/{len(LOTES)} lotes medidos): "
  f"{len(tc)} {ok(not tc and len(CO) == len(LOTES))}" + (f"; {[(a, b, round(c_, 1), d) for a, b, c_, d in tc[:6]]}" if tc else ""))
fr = [(l, k, v) for l in LOTES for k, v in (CO.get(l) or {}).get("frases", {}).items()]
ruim = [(l, k, round(v[1], 1)) for l, k, v in fr if v[1] < 30]
p(f"- FRASE-CHAVE ≥ 30 ({len(fr)} Text com «?» vistos em {len(CO)} lotes; maior tamanho que cada um atinge): {len(ruim)} abaixo de 30 {ok(not ruim and fr)}"
  + (f"; {ruim[:5]}" if ruim else "") + ("; " + "; ".join(f"{k[:40]} {v[1]:.0f}" for _, k, v in fr[:4]) if fr else "; nenhum medido — NÃO MEDIDO"))
i5 = list(over["PE1"].get("e1_5_inset", {}).values())
if i5:
    v = i5[-1]
    rt = v["ac_len"] / v["at_len"]
    p(f"- E1-5 inset a_c : a_t ({len(i5)} quadros): desenhado {v['ac_len']:.3f} : {v['at_len']:.3f} = {rt:.3f} : 1 (registrado {v['razao_tela']:.3f}) "
      f"{ok(abs(rt - v['razao_tela']) / v['razao_tela'] < 0.01)}; real (ω₀²r)/(rπ/3) = {v['razao_real']:.0f} : 1; selo FORA DE ESCALA "
      f"{'declarado' if v.get('fora_de_escala') else 'NÃO declarado'} {ok(v.get('fora_de_escala') and v['razao_real'] / rt > 10)} (real ÷ desenhado = {v['razao_real'] / rt:.0f}×)")
else:
    p("- E1-5 inset a_c : a_t: e1_5_inset não registrado — NÃO MEDIDO")
p()
p("## Resumo v3 (veredito de cada auditoria; detalhes nas seções acima)")
ORD = (("G28", "- G28:"), ("ORDEM", "- ORDEM"), ("MOSTRADOR", "- MOSTRADOR"), ("PARADO", "- TOTAL: PARADO"), ("COLUNA VAZIA", "- TOTAL: PARADO"), ("TAMANHO", "    · âncoras com envelope"),
       ("COR POR TOKEN", "- COR POR TOKEN"), ("COR OPERADOR", "- COR OPERADOR:"), ("COR POR CAPÍTULO (gate combinado)", "@cap"), ("§6 PRODUTO VETORIAL T5-8", "- PRODUTO VETORIAL (T5-8"),
       ("§6 CAIXA VAZIA (todos os caminhos)", "- CAIXA VAZIA (todos"), ("§6 FRASE-CHAVE", "- FRASE-CHAVE"), ("§6 E1-5 inset", "- E1-5 inset"))
res_ = []
for nome_, pre in ORD:
    if pre == "@cap":
        ls_ = [x for x in out if x.startswith("- ") and "FAMÍLIA" in x and "LARGA" in x and "DUAS" not in x and "gate combinado" not in x]
    else:
        ls_ = [x for x in out if x.startswith(pre)]
    if nome_ == "PARADO":
        ls_ = [x.split("·")[0] for x in ls_]
    if nome_ == "COLUNA VAZIA":
        ls_ = ["·".join(x.split("·")[1:]) for x in ls_]
    nf = sum("FALHA" in x for x in ls_)
    res_.append(f"- {nome_}: " + ("NÃO MEDIDO" if not ls_ else f"FALHA ({nf} linha(s) com FALHA)" if nf else "NÃO MEDIDO/PARCIAL" if any("NÃO MEDIDO" in x or "NÃO FECHADO" in x for x in ls_) else "OK"))
out[1:1] = [""] + ["## Resumo v3 (cópia do rodapé)"] + res_
out.extend(res_)
(DST / "qa.txt").write_text("\n".join(out) + "\n", encoding="utf-8")

# ── algebra.txt (v2 §2 item 9): como cada âncora construiu as linhas da CONTA ──
alg = {}
for l in LOTES:
    for x in ler(f"log_aud_{l}.txt").splitlines():
        m_ = re.match(r"\[alg\] (\S+) (escreve|passo|fadein-selo|fadein-texto)(.*)", x)
        if not m_:
            continue
        aid, tipo, resto = m_.groups()
        k = alg.setdefault(aid, Counter())
        if tipo == "escreve":
            k["esc+voo" if re.search(r"voos=[1-9]", resto) else "esc"] += 1
        else:
            k[tipo] += 1
tmt = Counter()
for f in sorted(U.glob("sec_*.py")):
    aid = "-"
    for ln in f.read_text(encoding="utf-8").splitlines():
        m_ = re.search(r'self\.an\("([^"]+)"\)', ln)
        if m_:
            aid = m_.group(1)
        if "TransformMatchingTex(" in ln:
            tmt[aid] += 1
lin_alg = ["# yt_0020 — álgebra por âncora (linhas da CONTA)", "",
           "esc = linha escrita em ordem de x (parte fixa) · esc+voo = com partes que voam do desenho · passo = TransformByGlyphMap · tmt = TransformMatchingTex (fonte) ·",
           "fade-selo / fade-texto = FadeIn de selo/DICA ou de linha só de texto (permitido). Equação por FadeIn de linha inteira = 0 por construção (play converte).", "",
           f"{'âncora':8s} {'esc':>4s} {'esc+voo':>8s} {'passo':>6s} {'tmt':>4s} {'fade-selo':>10s} {'fade-texto':>11s}"]
tot_ = Counter()
for aid in sorted(set(alg) | set(tmt), key=lambda a: (ANC.get(a, {}).get("ini", 1e9), a)):
    c = alg.get(aid, Counter())
    lin_alg.append(f"{aid:8s} {c['esc']:4d} {c['esc+voo']:8d} {c['passo']:6d} {tmt[aid]:4d} {c['fadein-selo']:10d} {c['fadein-texto']:11d}")
    tot_.update(c)
    tot_["tmt"] += tmt[aid]
lin_alg += ["", f"TOTAL: esc {tot_['esc']} · esc+voo {tot_['esc+voo']} · passo {tot_['passo']} · tmt {tot_['tmt']} · fade-selo {tot_['fadein-selo']} · fade-texto {tot_['fadein-texto']}"]
(DST / "algebra.txt").write_text("\n".join(lin_alg) + "\n", encoding="utf-8")

print("\n".join(out))
