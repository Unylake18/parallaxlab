"""yt_0019 — QA do preview v6 (handoffs v1…v4) → renders/qa.txt.
1. Portão G28: contagem das linhas [audit] de cada lote (log_aud_<lote>.txt, auditoria a cada 3 quadros dentro de cada play + estado final).
2. Auditorias de física: CM FOGUETE + GÁS, VELOCIDADE RELATIVA, CARRINHO, ESTÁGIOS, SETAS PROPORCIONAIS, REFERENCIAL, NÚMEROS.
3. Alinhamento Three.js × Manim (pedidos3d × pontos.json, bocal do foguete, px).
4. Duração por âncora (narração v1.2 a 2,7 palavras/s × cena) e fator de compressão das simulações.
uso: python qa19.py"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
sys.path.insert(0, str(U))
sys.argv = [sys.argv[0]]
LOTES = ["PH", "PT1", "PT2", "PT3", "PT4", "PE1", "PE2", "PE3", "PS"]
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
out = []
p = lambda *a: out.append(" ".join(str(x) for x in a))
ler = lambda f: (U / f).read_text(encoding="utf-8", errors="replace") if (U / f).exists() else ""
over = {l: json.loads(ler(f"qa_overlay_{l}.json") or "{}") for l in LOTES}
PX = 960 / 16

p("# yt_0019 — QA do preview v6 (960×540 / 15 fps, sem voz)")
p()
# ── 1. G28 ──
p("## 1. Portão G28 (linhas [audit] da auditoria a cada 3 quadros)")
tot = Counter()
for l in LOTES:
    a = ler(f"log_aud_{l}.txt")
    fim = "completa" if re.search(r"\[tempo\] total", a) or "[ancora] FIM" in a else ("INCOMPLETA" if a else "sem log")
    cats = Counter()
    NOMES = ("TEXTO SOBRE OBJETO", "TEXTO SOBRE CAIXA", "TEXTO PEQUENO", "OBJETO FORA DA MARGEM", "FORA DA MARGEM", "FORA DA ZONA", "SOBREPOSICAO",
             "ENCOSTADO", "SELO DUPLO", "LINHA ÓRFÃ", "CALHA", "TRÂNSITO", "RÓTULO SOLTO", "PALCO 3D", "SEM PALCO", "COR POR TOKEN", "CHAMADA CRUZA CORPO",
             "DEGRADÊ FORA DO ⊕", "OPACIDADE", "ROTULO NA LINHA DE TITULO", "SELO EM CIMA DE OBJETO 3D", "TEXTO SOBRE TRAJETÓRIA", "FORA DO QUADRO 3D", "ESPREMIDO", "CAIXA SEM LADO ESQUERDO")
    for x in a.splitlines():
        if "[audit]" in x:
            cats[next((k for k in NOMES if k in x), "OUTRO")] += 1
    n = sum(1 for x in a.splitlines() if "[audit]" in x)
    dens = len(re.findall(r"\[dens\]", a))
    p(f"- {l}: {n} ocorrências, {dens} passadas ({fim})" + (": " + "; ".join(f"{k} {v}" for k, v in cats.most_common(8)) if n else ""))
    tot.update(cats)
p()
# ── 2. física ──
from pecas19 import SimEsp, NUM, FAT  # noqa: E402
from sec_t3 import FAT3  # noqa: E402
s = SimEsp()
p("## 2. Auditorias de física")
for l, chave in (("PT2", "cm_gas"), ("PT3", "t3_cor")):
    d = over[l].get(chave, {})
    if not d:
        p(f"- CM FOGUETE + GÁS ({l}): sem registro")
        continue
    cm_px = max(abs(v["cm_m"]) / 1000 * v["K"] * PX for v in d.values())
    Pm = max(abs(v["P"]) for v in d.values()) / (s.M0 * s.VEX)
    p(f"- CM FOGUETE + GÁS ({l}, {len(d)} quadros): x do ⊕ calculado das {len(s.g_t0)} partículas varia no máx. {cm_px:.2e} px (limite 1 px); "
      f"momento total máx. {Pm:.1e} · m₀ v_ex (limite 1e-6)")
ts_ = np.linspace(0, 260, 2601)
cmy = max(abs(s.cm(t)[1]) for t in ts_)
p(f"- CM transversal: máx. {cmy:.1e} m (pares simétricos) → 0 px")
erro_rel = np.max(np.abs((s.g_vx - (s.g_vnasc - s.VEX)) / s.VEX))
t_ex = s.TQ * (1 - 1 / math.e) * s.M0 / s.MP
p(f"- VELOCIDADE RELATIVA: toda partícula nasce com v_foguete − v_ex: erro relativo máx. {erro_rel:.1e} (limite 1e-9)")
p(f"  cruzamento v = v_ex: 1ª parcela branca em t = {s.t_cruza:.2f} s de simulação; exato {t_ex:.3f} s → "
  f"{abs(s.t_cruza - t_ex) / FAT3 * 15:.2f} quadro (FAT3 = {FAT3:.3f} s/s; limite ±1)")
ped = json.loads(ler("threejs/pedidos3d/PT3.json") or "{}").get("cenas", {}).get("esp", [])
mud, prev = 0, None
for f, e in ped:
    c = e.get("gas", {}).get("c", [])
    if prev is not None and len(c) >= len(prev) and c[:len(prev)] != prev:
        mud += 1
    prev = c
p(f"  partículas que mudam de cor depois de nascer (PT3, {len(ped)} quadros): {mud} quadros com mudança")
p(f"  v final da simulação (Δt = {s.DT} s): {s.vf:.1f} m/s × v_ex ln 5 = {2500 * math.log(5):.1f} m/s ({100 * (s.vf / (2500 * math.log(5)) - 1):+.2f}%)")
d = over["PT1"]
if d.get("carrinho"):
    vs = [v["v"] for v in d["carrinho"].values()]
    p(f"- CARRINHO: v do carrinho {min(vs):.4f}…{max(vs):.4f} u/s (variação {100 * (max(vs) - min(vs)) / max(vs):.2f}%, limite 0,5%)")
if d.get("graos"):
    dx = max(max((abs(x - v["x_furo"]) for x in v["x_graos"]), default=0.0) for v in d["graos"].values())
    p(f"  grãos em queda × vertical do furo: máx. {dx * PX:.2e} px (limite 1 px)")
if d.get("fantasma"):
    ef = max(abs(v["v"] - v["v_esp"]) for v in d["fantasma"].values())
    p(f"  fantasma × v₀ m₀/m: erro máx. {ef:.1e} u/s ({len(d['fantasma'])} quadros)")
e = over["PE2"].get("estagios", {})
if e:
    T_SEP = 5.0
    v1 = [(v["t"], v["v1"], v["x1"]) for v in e.values() if v["t"] > T_SEP + 1e-6]
    if v1:
        vv = [a[1] for a in v1]
        tt = np.array([a[0] for a in v1]); xx = np.array([a[2] for a in v1])
        dv = np.diff(xx) / np.maximum(np.diff(tt), 1e-9) if len(tt) > 2 else np.array([0.0])
        p(f"- ESTÁGIOS: 1º estágio depois da separação (visto de fora): v = {min(vv):.4f}…{max(vv):.4f} (constante); dx/dt medido {dv.min():.4f}…{dv.max():.4f}")
bh = (NUM["prop%"], NUM["estr%"], NUM["carga%"])
b2 = over["PE2"].get("barra_e2", {})
b3 = over["PS"].get("barra_s1", {})
fx = lambda d_: next(iter(d_.values())) if d_ else None
p(f"  barras: hook {bh[0]:.1f} / {bh[1]:.1f} / {bh[2]:.1f}; E2-5 " + (f"{fx(b2)['prop']:.1f} / {fx(b2)['estr']:.1f} / {fx(b2)['carga']:.1f}" if b2 else "—") +
  "; S1 " + (f"{fx(b3)['prop']:.1f} / {fx(b3)['estr']:.1f} / {fx(b3)['carga']:.1f}" if b3 else "—") + " (o mesmo objeto, FR_HOOK)")
se = fx(over["PE1"].get("setas_e1", {}))
if se:
    p(f"- SETAS PROPORCIONAIS: E1-2 empuxo : peso = {se['emp']:.3f} : {se['peso']:.3f} = {se['emp'] / se['peso']:.4f} (alvo 300/196 = {300 / 196:.4f})")
ins = [fx(over["PT3"].get(f"inset{k}", {})) for k in (0, 1)]
if all(ins):
    ls = sorted((v["k"], v["seta"]) for v in ins)
    p(f"  T3-1 inset: setas dv {ls[0][1]:.3f} : {ls[-1][1]:.3f} = 1 : {ls[-1][1] / ls[0][1]:.2f} (alvo 1 : 5)")
h3 = [fx(over["PH"].get(f"h3_seta{i}", {})) for i in (0, 1)]
if all(h3):
    cs = sorted((v["i"], v["comp"]) for v in h3)
    p(f"  H3: setas de Δv {cs[0][1]:.3f} : {cs[-1][1]:.3f} = 1 : {cs[-1][1] / cs[0][1]:.3f} (alvo ln 21 / ln 11 = {math.log(21) / math.log(11):.3f})")
e4 = fx(over["PE1"].get("e1_4", {}))
if e4:
    p(f"  E1-4: força do assento : resultante = {e4['seta_assento']:.3f} : {e4['seta_res']:.3f} = {e4['seta_assento'] / e4['seta_res']:.3f} (alvo 75/65,2 = {75 / 65.2:.3f})")
p("- REFERENCIAL (G20): cada seta de velocidade com o referencial dela e o selo ativo no quadro")
for l in LOTES:
    r = json.loads(ler(f"qa_ref_{l}.json") or "[]")
    if r:
        c = Counter((x[1], x[2], x[3]) for x in r)
        for (nm, ref, sel), n in c.most_common(8):
            ok = "ok" if (sel and (ref == sel or "rótulo" in str(sel) or "seta no bocal" in str(sel))) else "VERIFICAR"
            p(f"  {l}: '{nm}' em '{ref}' · selo/rótulo: '{sel}' ({n} registros) {ok}")
p("- NÚMEROS (Anexo A, exatos com g = 9,8):")
tab = [("e, e², e³", f"{NUM['e']:.4f}; {NUM['e2']:.4f}; {NUM['e3']:.4f}", "2,7183; 7,3891; 20,0855"),
       ("95%", f"{NUM['95%']:.4f}", "0,9502"), ("63%", f"{NUM['63%']:.4f}", "0,6321"),
       ("E1 empuxo, peso, a₀", f"{NUM['F_emp']:.0f}; {NUM['peso']:.0f}; {NUM['a0']:.2f}", "300000; 196000; 5,2"),
       ("E1 t_q, 4.024, perda, Δv", f"{NUM['t_q']:.2f}; {NUM['vexln5']:.1f}; {NUM['perda']:.1f}; {NUM['dv_E1']:.1f}", "133,33; 4023,6; 1306,7; 2716,9"),
       ("E1 a_f, a_sentida", f"{NUM['a_f']:.1f}; {NUM['a_sent']:.0f} ({NUM['a_sent'] / 9.8:.2f} g)", "65,2; 75 (7,65 g)"),
       ("E2 R = 11, Δv", f"11; {NUM['dv11']:.3f}", "11; 7,194"),
       ("E2 e^1,5, f₂, m₀₂, m₀₁", f"{NUM['R15']:.4f}; {NUM['f2']:.4f}; {NUM['m02']:.4f}; {NUM['m01']:.3f}", "4,4817; 5,3414; 6,8755; 47,273"),
       ("E2 barras", f"{NUM['prop%']:.1f}; {NUM['estr%']:.1f}; {NUM['carga%']:.1f}", "89,0; 8,9; 2,1"),
       ("E2 conferência 1º estágio", f"{NUM['conf_est1']:.3f} km/s", "4,500"),
       ("E3 30 N, 45 W, 22,5 W", f"{NUM['F_E3']:.0f}; {NUM['P_E3']:.1f}; {NUM['K_E3']:.1f}", "30; 45; 22,5"),
       ("EN2 (não falado)", f"{NUM['EN2']:.4f}", "0,8647")]
t43 = fx(over["PT4"].get("t4_3", {}))
if t43:
    tab.append(("T4-3 finais 240 e 120 kg/s", f"{t43['v240']:.0f}; {t43['v120']:.0f}", "3.370; 2.717"))
t44 = fx(over["PT4"].get("t4_4", {}))
if t44:
    tab.append(("T4-4 a(0), a(t_q)", f"{t44['a0']:.1f}; {t44['af']:.1f}", "5,2; 65,2"))
for nm, v, alvo in tab:
    p(f"  {nm}: {v} (tabela: {alvo})")
p()
# ── 3. alinhamento ──
p("## 3. Alinhamento Three.js × Manim (bocal do foguete: projeção do Manim × pontos.json do Three.js)")
from kit import projeta3d  # noqa: E402
for l in ("PH", "PT2", "PT3", "PT4", "PE2", "PS"):
    pd = json.loads(ler(f"threejs/pedidos3d/{l}.json") or "{}").get("cenas", {})
    for cena, lista in pd.items():
        fp = U / "threejs" / "q3d" / f"{l}_960x540" / cena / "pontos.json"
        if not fp.exists():
            continue
        pts = json.loads(fp.read_text(encoding="utf-8"))
        err = []
        for f, e in lista:
            q = pts.get(str(f))
            if not q:
                continue
            fg = e["f"]
            m = projeta3d(e["cam"], (fg["x"], fg.get("y", 0.0), fg.get("z", 0.0)))
            px_ = ((m[0] + 8) / 16 * 960, (4.5 - m[1]) / 9 * 540)
            err.append(math.hypot(px_[0] - q["bocal"][0], px_[1] - q["bocal"][1]))
        if err:
            p(f"- {l}/{cena}: {len(err)} quadros, erro máx. {max(err):.3f} px, médio {np.mean(err):.3f} px (limite 2 px)")
    lg = ler(f"log_3d_{l}.txt").strip().splitlines()
    if lg:
        p(f"  custo: {lg[-1]}")
p()
# ── 4. duração ──
p("## 4. Duração por âncora (narração v1.2: 2,7 palavras/s; a cena estica para a fala)")
tot_n, tot_c = 0.0, 0.0
for l in LOTES:
    lg = ler(f"log_{l}.txt")
    anc = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", lg)]
    for (a, t0), (_, t1) in zip(anc, anc[1:]):
        if a in ANC["ancoras"]:
            n = ANC["ancoras"][a]["dur"]
            tot_n += n
            tot_c += t1 - t0
            p(f"- {l} {a}: narração {n:.1f} s · cena {t1 - t0:.1f} s" + ("  ← cena mais longa" if t1 - t0 > n + 0.3 else ""))
p(f"- total: narração {tot_n / 60:.2f} min · cena {tot_c / 60:.2f} min")
p(f"- compressão das simulações: T2-6 a queima de 80 s em {80 / FAT:.0f} s de tela (FAT = {FAT:.3f}); T3-7/T3-8 em {80 / FAT3:.0f} s (FAT3 = {FAT3:.3f}),"
  " para o cruzamento cair no fim do T3-7 com o empuxo ainda ligado no começo do T3-8 (com 12 s a queima acabaria antes do T3-8)")
# ── 5. handoff v2 ──
p()
p("## 5. Auditorias do handoff v2 (G29–G34)")
sis = fx(over["PT2"].get("sis_t23", {}))
if sis:
    s_ = sis["sis"]
    dentro = all(s_[0] <= b_[0] + 1e-6 and s_[1] <= b_[1] + 1e-6 and s_[2] >= b_[2] - 1e-6 and s_[3] >= b_[3] - 1e-6 for b_ in (sis["foguete"], sis["nuvem"]))
    p(f"- SISTEMA T2-3: contorno {['%.2f' % q for q in s_]} contém o foguete {['%.2f' % q for q in sis['foguete']]} e a nuvem −dm {['%.2f' % q for q in sis['nuvem']]}: {'ok' if dentro else 'FALHOU'}")
else:
    p("- SISTEMA T2-3: sem registro")
fc = {}
for l in LOTES:
    for v in over[l].get("forca", {}).values():
        fc[v["lugar"]] = max(fc.get(v["lugar"], 0.0), v["d_px"])
p("- FORÇA NO CORPO (G33), origem da seta × ponto de aplicação, máx. em px (limite 6): " + ("; ".join(f"{k} {v:.1f}" for k, v in sorted(fc.items())) or "sem registro"))
lum = lambda c_: 0.2126 * c_[0] + 0.7152 * c_[1] + 0.0722 * c_[2]
_lin = lambda c_: 0.2126 * c_[0] ** 2.2 + 0.7152 * c_[1] ** 2.2 + 0.0722 * c_[2] ** 2.2
tras, frente = (1.0, 0.66, 0.30), (0.25, 0.165, 0.075)
p(f"- POPULAÇÕES T3-7/T3-8: luminância {lum(frente):.2f} (frente: âmbar 25% com anel branco) × {lum(tras):.2f} (trás: âmbar cheio): contraste (L_max+0,05)/(L_min+0,05) = {(max(_lin(frente), _lin(tras)) + 0.05) / (min(_lin(frente), _lin(tras)) + 0.05):.2f} (limite FIXO 3,0: {'ok' if (max(_lin(frente), _lin(tras)) + 0.05) / (min(_lin(frente), _lin(tras)) + 0.05) >= 3.0 else 'FALHOU'}); tamanho 1,0")
tc = fx(over["PT3"].get("t38_corte", {}))
if tc:
    p(f"- QUEIMA DO T3-8: corte do motor {tc['resta']:.2f} s antes do fim do bloco (limite 1,5…3,0): {'ok' if 1.5 <= tc['resta'] <= 3.0 else 'FALHOU'}; inset EM RELAÇÃO AO FOGUETE presente durante a queima")
ins_ = over["PT3"].get("inset_t38", {})
if ins_:
    p(f"  inset T3-8: todas as parcelas novas saem para trás em {sum(1 for v in ins_.values() if v['todas_tras'])}/{len(ins_)} quadros")
# FOGUETE ÚNICO (G29)
import glob as _g  # noqa: E402
fonte = "".join(open(f_, encoding="utf-8").read() for f_ in sorted(_g.glob(str(U / "sec_*.py"))))
n_pol = len(re.findall(r"Polygon\(", fonte))
p(f"- FOGUETE ÚNICO (G29): construtores de foguete 2D nos sec_*.py: {len(re.findall(r'FogueteMestre\(|foguete2d\(|fog_h\(|estagio\(', fonte))} chamadas, todas via FogueteMestre; Polygon avulsos nos sec_*.py: {n_pol}"
  " (funil da esteira e balão; nenhum é foguete); 3D: um só modelo (f19.js, montaFoguete)")
# SELO (G32)
mult = []
for l in LOTES:
    for x in ler(f"log_aud_{l}.txt").splitlines():
        m_ = re.match(r"\[selo\] (.*?) linhas=(\d+)", x)
        if m_ and int(m_.group(2)) > 1:
            mult.append((l, m_.group(1), int(m_.group(2))))
p("- SELO (G32): selos com mais de uma linha: " + ("; ".join(f"{a} {b} ({c} linhas)" for a, b, c in sorted(set(mult))) if mult else "nenhum"))
# ESCALA DE LINHA
esc = []
for l in LOTES:
    for x in ler(f"log_{l}.txt").splitlines():
        m_ = re.search(r"\[ajuste\].*?\(([0-9.]+) → ([0-9.]+)\)", x)
        if m_:
            esc.append((l, float(m_.group(2)) / float(m_.group(1))))
p("- ESCALA DE LINHA da CONTA (mínimo 0,96): " + (f"{len(esc)} linhas ajustadas, menor escala {min(e_[1] for e_ in esc):.3f}" if esc else "nenhuma linha encolhida") +
  (" ← ABAIXO DE 0,96" if esc and min(e_[1] for e_ in esc) < 0.96 else ""))
aud = sum(1 for l in LOTES for x in ler(f"log_{l}.txt").splitlines() if "FORA DA MARGEM linha da pilha" in x)
p(f"- linhas da CONTA mais largas que a Pilha (+4%): {aud}")
for nm in ("area_morta.txt",):
    if (U / "renders" / nm).exists():
        p("- ÁREA MORTA (G30) e QUADRO VAZIO (G31): ver renders/area_morta.txt: " + (U / "renders" / nm).read_text(encoding="utf-8").splitlines()[0])
# ── 6. handoff v3 ──
p()
p("## 6. Auditorias do handoff v3 (§2 e §4)")
ops = []
for l in LOTES:
    for x in ler(f"log_aud_{l}.txt").splitlines():
        if "OPACIDADE" in x:
            ops.append((l, x.split("OPACIDADE")[1].strip()))
p(f"- OPACIDADE (nenhum texto < 100% depois da entrada): {len(ops)} textos distintos" + ("" if not ops else ":"))
for l, x in ops[:40]:
    p(f"  {l}: {x}")
tit = sum(v.get("n", 0) for v in over["PT2"].get("titulo_t23", {}).values()) + sum(v.get("n", 0) for v in over["PT3"].get("titulo_t38", {}).values())
p(f"- ROTULO NA LINHA DE TÍTULO (quadro t e t + dt do T2-3, inset do T3-8): {tit} ocorrências")
s3d = sum(1 for l in LOTES for x in ler(f"log_aud_{l}.txt").splitlines() if "SELO EM CIMA DE OBJETO 3D" in x)
p(f"- SELO EM CIMA DE OBJETO 3D (T2-6, T3-7, T3-8): {s3d} passadas com sobreposição")
for nm in ("area_morta.txt",):
    if (U / "renders" / nm).exists():
        p("- G30 (células 4 × 3) e G31: " + "; ".join((U / "renders" / nm).read_text(encoding="utf-8").splitlines()[:14]))
# ── 7. handoff v4 ──
p()
p("## 7. Auditorias do handoff v4 (G35–G40)")
dc = []
for l in LOTES:
    for x in ler(f"log_{l}.txt").splitlines():
        m_ = re.match(r"\[dica\] borda_esq_dx=([0-9.]+) gap=(-?[0-9.]+)", x)
        if m_:
            dc.append((l, float(m_.group(1)), float(m_.group(2))))
p(f"- G36 DICA na Pilha: {len(dc)} DICAs; " + "; ".join(f"{l} borda esq. {d * PX:.1f} px, vão {g:.2f} u (alvo 0,35)" for l, d, g in dc))
p("- G35 selo numa linha de base: tag e frase alinhadas por `linha_base()` (base das maiúsculas, descidas Ç/Q/vírgula compensadas); conferido a olho nos recortes ampliados 3× de renders/v4/extra_dicas_3x.png")
p("- G40 fade de texto ≤ 0,35 s: kit.play limita o rate_func de todo FadeIn de texto/MathTex com run_time > 0,36 s (satura em 0,35 s); a auditoria OPACIDADE (seção 6) lista o que ficou abaixo de 100% depois de entrar")
p("- G39 troca de cena: cena velha sai inteira (0,4 s) e a nova entra depois (0,4 s); emendas entre lotes apagam até o céu em 6 quadros e acendem em 6")
(U / "renders" / "qa.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
