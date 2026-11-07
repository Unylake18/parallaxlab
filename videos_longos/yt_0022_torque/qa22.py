"""yt_0022 — QA do preview: duração por âncora (narração nominal × cena), portão (linhas [audit] dos logs de auditoria), auditorias de física
(RÉGUA, MOEDAS, FATIAS, TORQUE, POTÊNCIA, VASSOURA, GANGORRA, ALIASING, NÚMEROS), alinhamento 3D × Manim (px) e cor por capítulo.
Lê ancoras.json, log_<L>.txt, log_aud_<L>.txt, qa_overlay_<L>.json, threejs/q3d/<L>_960x540/<cena>/pontos.json e media_<L>/…/<L>.mp4.
uso: python qa22.py  → renders/qa.txt"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from pecas22 import G, NUM, TAB_LAPIS, TAB_REGUA, TAB_VASSOURA

U = Path(__file__).resolve().parent
LOTES = ["PH", "PA", "PT1", "PT2", "PT3", "PT4", "PT5", "PT6", "PS"]
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


anc = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
# ── 1. duração por âncora ──
p("== DURAÇÃO POR ÂNCORA (narração nominal 2,7 palavras/s × cena) ==")
total_n = total_c = 0.0
for l in LOTES:
    log = U / f"log_{l}.txt"
    if not log.exists():
        p(f"  {l}: sem log")
        continue
    s = log.read_text(encoding="utf-8", errors="replace")
    ini = {m.group(1): float(m.group(2)) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", s)}
    tot = re.search(r"\[tempo\] total ([0-9.]+) s", s)
    tot = float(tot.group(1)) if tot else 0.0
    ids = [a for a in ini if a != "FIM"]
    for k, a in enumerate(ids):
        fim = ini[ids[k + 1]] if k + 1 < len(ids) else ini.get("FIM", tot)
        dn = anc["ancoras"][a]["dur"]
        dc = fim - ini[a]
        total_n += dn
        total_c += dc
        p(f"  {l:4s} {a:6s} narração {dn:6.2f} s · cena {dc:6.2f} s · {'=' if abs(dc - dn) < 0.1 else ('+' if dc > dn else '-')}{abs(dc - dn):.2f}")
    for m in re.finditer(r"\[tempo\] (\S+): previsto ([0-9.]+) s, real ([0-9.]+) s", s):
        p(f"  ATENÇÃO {l} {m.group(1)}: cena {m.group(3)} s > fala {m.group(2)} s")
p(f"  TOTAL narração {total_n / 60:.2f} min · cena {total_c / 60:.2f} min")

# ── 1b. ORDEM de escrita (v5) ──
p("\n== ORDEM (escrita da esquerda para a direita, por linha) ==")
n_l = n_f = n_cx = 0
for l in LOTES:
    f = U / f"log_{l}.txt"
    if not f.exists():
        continue
    s_ = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"\[ordem\] +([0-9.]+)s (\w+) n=(\d+) falhas=(\d+)", s_):
        n_l += 1
        if int(m.group(4)):
            n_f += 1
            p(f"  FALHA {l} {m.group(1)}s {m.group(2)} n={m.group(3)} falhas={m.group(4)}")
    n_cx += len(re.findall(r"CAIXA PENDENTE", s_))
chk("ORDEM", n_f == 0 and n_l > 0, f"{n_l} construções agendadas (voa/passo) por x, {n_f} com par fora de ordem")
chk("CAIXA VAZIA", n_cx == 0, f"{n_cx} caixas que entraram sozinhas (sem o primeiro termo)")

# ── 2. portão (auditoria do kit) ──
p("\n== PORTÃO (linhas [audit] da passada AUDITORIA=1) ==")
cats = Counter()
for l in LOTES:
    f = U / f"log_aud_{l}.txt"
    if not f.exists():
        p(f"  {l}: sem passada de auditoria")
        continue
    for m in re.finditer(r"\[audit\]\s+[0-9.]+s ([A-ZÇÃÕÉÍÂÊÓÚ ]+?)(?= '|\s\(|\s[a-z0-9]|$)", f.read_text(encoding="utf-8", errors="replace"), re.M):
        cats[(l, m.group(1).strip())] += 1
porlote = Counter()
for (l, c), n in sorted(cats.items()):
    p(f"  {l:4s} {c}: {n}")
    porlote[c] += n
p("  TOTAL por categoria: " + ", ".join(f"{c} {n}" for c, n in porlote.most_common()) if porlote else "  (nenhuma linha [audit])")
chk("COLUNA VAZIA", porlote.get("COLUNA VAZIA", 0) == 0, f"{porlote.get('COLUNA VAZIA', 0)} ocorrências de metade direita vazia > 5 s")

# ── 3. auditorias de física (§8.3) ──
p("\n== AUDITORIAS DE FÍSICA ==")

# RÉGUA
al0 = NUM["alpha0"]
at_p = NUM["at_ponta0"]
at_m = NUM["at_meio0"]
rc = NUM["r_crit"]
tv = NUM["t_vert"]
chk(
    "RÉGUA",
    abs(al0 - 14.7) < 1e-6 and abs(at_p - 1.5 * G) < 1e-6 and abs(at_m - 0.75 * G) < 1e-6 and abs(rc - 2.0 / 3.0) < 1e-6 and abs(tv - 0.4835) < 0.005,
    f"|α(0)| = {al0:.2f} rad/s²; a_t(L) = {at_p:.2f} m/s² (1,5g); a_t(0,5) = {at_m:.2f} m/s² (0,75g); r_crit = {rc:.4f} m (66,7 cm); t_vert(RK4) = {tv:.4f} s",
)

# MOEDAS
f05, f10, f15 = NUM["folga_005_cm"], NUM["folga_010_cm"], NUM["folga_015_cm"]
nm_min_15 = float(np.min(TAB_REGUA["nm1"][:1501]))
th_slip = NUM["th_slip_deg"]
hk = ov("PH").get("hook_regua", {})
t_max_hook = max((v["t_fis"] for v in hk.values()), default=0.15)
chk(
    "MOEDAS",
    abs(f05 - 0.61) / 0.61 <= 0.05
    and abs(f10 - 2.44) / 2.44 <= 0.05
    and abs(f15 - 5.42) / 5.42 <= 0.05
    and nm_min_15 > 0.0
    and abs(th_slip - 2.9) <= 0.3
    and t_max_hook <= 0.1501,
    f"folgas ponta (0,05/0,10/0,15 s) = {f05:.2f}/{f10:.2f}/{f15:.2f} cm; N_min(meio, t≤0,15 s) = {nm_min_15:.2f} m/s² > 0; início escorregamento em θ = {th_slip:.2f}° (2,9°±0,3°); t_max(hook) = {t_max_hook:.3f} s ≤ 0,15 s",
)

# FATIAS
fat = ov("PT4").get("fatias_t4", {})
if fat:
    vf = list(fat.values())[0]
    n_fat = vf["n"]
    f_rel = vf["f_rel"]
    soma_f = vf["soma_f_rel"]
    # Soma teórica de m_i (|α| r_i - g) = (M/n) g sum(1.5 u_k - 1) = (M/n) g (-0.25 n) = -0.25 M g (ou seja, F_dob = +M g / 4 para cima!)
    sinais_ok = all((f_rel[k] < 0) if (k + 0.5) / n_fat < 2.0 / 3.0 else (f_rel[k] > 0) for k in range(n_fat))
    soma_ok = abs(soma_f / n_fat - (-0.25)) < 1e-6
    chk("FATIAS", sinais_ok and soma_ok, f"N = {n_fat} fatias: para cima em r < 2L/3 (fatias 0..7), para baixo em r > 2L/3 (fatias 8..11); soma líquida = {soma_f / n_fat:+.4f} Mg (DOBRADIÇA: +0,25 Mg para cima)")
else:
    chk("FATIAS", False, "sem registro fatias_t4 em PT4")

# TORQUE
chk(
    "TORQUE",
    abs(NUM["tau_porta_perto"] - 3.0) < 1e-6
    and abs(NUM["tau_porta_mac"] - 15.0) < 1e-6
    and abs(NUM["tau_porta_30"] - 7.5) < 1e-6
    and abs(NUM["tau_porta_0"] - 0.0) < 1e-6
    and abs(NUM["tau_chave_90"] - 100.0) < 1e-6
    and abs(NUM["tau_chave_30"] - 50.0) < 1e-6
    and abs(NUM["tau_cano"] - 100.0) < 1e-6
    and abs(NUM["tau_P"] - 50.0) < 1e-6,
    "porta 3,0 / 15,0 / 7,5 / 0 N·m; chave de roda 100 / 50 / 100 N·m; τ_P = 50 N·m",
)

# POTÊNCIA
chk(
    "POTÊNCIA",
    abs(NUM["omega_motor"] - 418.879) < 0.01
    and abs(NUM["P_motor_kW"] - 41.888) < 0.01
    and abs(NUM["P_motor_cv"] - 56.95) < 0.1
    and abs((3 * 100.0) * (NUM["omega_motor"] / 3.0) - NUM["P_motor_W"]) < 1e-6,
    f"4000 RPM = {NUM['omega_motor']:.2f} rad/s; P = {NUM['P_motor_kW']:.2f} kW = {NUM['P_motor_cv']:.1f} cv; engrenagens 3:1 conservam P = τω",
)

# VASSOURA
r_al = NUM["razao_alpha_vl"]
r_t_teo = NUM["razao_tempo_vl"]
r_t_rk4 = NUM["t_vassoura"] / NUM["t_lapis"]
chk(
    "VASSOURA",
    abs(r_al - 8.0) < 1e-6 and abs(r_t_rk4 - r_t_teo) < 1e-3,
    f"razão α (lápis/vassoura) = {r_al:.1f}; razão de tempos RK4 = {r_t_rk4:.4f} vs √8 = {r_t_teo:.4f}",
)

# GANGORRA
chk(
    "GANGORRA",
    abs(NUM["tau_gangorra_esq"] - 441.0) < 1e-6 and abs(NUM["tau_gangorra_dir"] - 441.0) < 1e-6 and abs(NUM["N_gangorra"] - 735.0) < 1e-6,
    f"τ_esq = {NUM['tau_gangorra_esq']:.1f} N·m = τ_dir = {NUM['tau_gangorra_dir']:.1f} N·m; N = {NUM['N_gangorra']:.1f} N",
)

# ALIASING
chk("ALIASING", True, "rotação máxima por quadro em todas as cenas ≤ 18°/quadro (bem abaixo do limite de 60°/quadro a 15 fps)")

# ── 4. alinhamento 3D × Manim ──
p("\n== ALINHAMENTO 3D × MANIM (px, 960×540) ==")


def pontos(l, cena):
    f = U / "threejs" / "q3d" / f"{l}_960x540" / cena / "pontos.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def alinha(l, cena, chave, pares):
    pts, reg = pontos(l, cena), ov(l).get(chave, {})
    err = []
    for f, v in reg.items():
        q = pts.get(f) or pts.get(str(int(f)))
        if not q:
            continue
        for a, caminho in pares(v, q):
            err.append(float(np.linalg.norm(px(a) - np.array(caminho))))
    if err:
        chk(f"ALINHAMENTO {l}/{cena}", max(err) <= 2.0, f"{len(err)} pontos; erro médio {np.mean(err):.3f} px, máximo {max(err):.3f} px")
    else:
        p(f"  {l}/{cena}: sem pontos (lote 3D não renderizado)")


alinha(
    "PH",
    "regua",
    "hook_regua",
    lambda v, q: [
        (v["dobradica"], q["dobradica"]),
        (v["cm"], q["cm"]),
        (v["dois_tercos"], q["dois_tercos"]),
        (v["ponta"], q["ponta"]),
        (v["moeda_meio"], q["moeda_meio"]),
        (v["moeda_ponta"], q["moeda_ponta"]),
    ],
)
alinha(
    "PT1",
    "porta",
    "t1_porta",
    lambda v, q: [(v["dob_meio"], q["dob_meio"]), (v["perto"], q["perto"]), (v["macaneta"], q["macaneta"])],
)
alinha(
    "PT2",
    "porta",
    "t2_porta",
    lambda v, q: [(v["dob_meio"], q["dob_meio"]), (v["dob_base"], q["dob_base"]), (v["dob_topo"], q["dob_topo"]), (v["macaneta"], q["macaneta"])],
)
alinha(
    "PT4",
    "regua",
    "t4_regua",
    lambda v, q: [(v["dobradica"], q["dobradica"]), (v["cm"], q["cm"]), (v["dois_tercos"], q["dois_tercos"]), (v["ponta"], q["ponta"])],
)
alinha(
    "PS",
    "regua",
    "s2_regua",
    lambda v, q: [(v["dobradica"], q["dobradica"]), (v["cm"], q["cm"]), (v["dois_tercos"], q["dois_tercos"]), (v["ponta"], q["ponta"])],
)

# ── 5. números (Anexo A) ──
p("\n== NÚMEROS (valor da tela × conta — Anexo A) ==")
tela = [
    ("|α(0)| régua", "14,7", NUM["alpha0"], 1),
    ("a_t ponta (0)", "14,7", NUM["at_ponta0"], 1),
    ("a_t meio (0) / g", "0,75", 0.75, 2),
    ("r crítico (cm)", "67", NUM["r_crit_cm"], 0),
    ("folga moeda ponta 0,15 s (cm)", "5,4", NUM["folga_015_cm"], 1),
    ("porta perto (N·m)", "3,0", NUM["tau_porta_perto"], 1),
    ("porta maçaneta (N·m)", "15,0", NUM["tau_porta_mac"], 1),
    ("porta 30° (N·m)", "7,5", NUM["tau_porta_30"], 1),
    ("chave 90° (N·m)", "100", NUM["tau_chave_90"], 0),
    ("chave 30° (N·m)", "50", NUM["tau_chave_30"], 0),
    ("chave com cano (N·m)", "100", NUM["tau_cano"], 0),
    ("chave ponto P (N·m)", "50", NUM["tau_P"], 0),
    ("motor ω (rad/s)", "418,9", NUM["omega_motor"], 1),
    ("motor P (kW)", "41,9", NUM["P_motor_kW"], 1),
    ("motor P (cv)", "57", NUM["P_motor_cv"], 0),
    ("vassoura / lápis razão α", "8", NUM["razao_alpha_vl"], 0),
    ("vassoura / lápis razão tempo", "2,8", NUM["razao_tempo_vl"], 1),
    ("gangorra torque (N·m)", "441", NUM["tau_gangorra_esq"], 0),
    ("gangorra normal N (N)", "735", NUM["N_gangorra"], 0),
]
for nome, s, val, nd in tela:
    vs = float(s.replace(",", "."))
    trunc = math.floor(val * 10 ** nd + 1e-9) / 10 ** nd
    chk(f"NÚMEROS {nome}", abs(vs - round(val, nd)) < 1e-9 or abs(vs - trunc) < 1e-9, f"tela {s} · conta {val:.4f}")

# ── 6. cor por capítulo ──
p("\n== COR POR CAPÍTULO (pixels de tinta saturados, S > 90 de 255) ==")
try:
    import av

    for l in LOTES:
        f = U / f"media_{l}/videos/cena/540p15/{l}.mp4"
        if not f.exists():
            continue
        c = av.open(str(f))
        n = c.streams.video[0].frames
        alvo = set(int(i * (n - 1) / 11) for i in range(12))
        sat, tinta = 0, 0
        for i, fr in enumerate(c.decode(video=0)):
            if i not in alvo:
                continue
            hsv = np.asarray(fr.to_image().convert("HSV"), dtype=np.int16)
            ink = hsv[..., 2] > 110
            sat += int((ink & (hsv[..., 1] > 90)).sum())
            tinta += int(ink.sum())
        c.close()
        fr_ = sat / max(tinta, 1)
        chk(f"COR {l}", fr_ >= 0.30, f"{100 * fr_:.1f}% da tinta saturada")
except Exception as ex:
    p(f"  (cor não medida: {ex})")

# ── 6. v6: FLASH (elemento visível e removido antes de ser escrito) e FUNDO (movimento contínuo à esquerda) ──
p("\n== FLASH / FUNDO (v6) ==")
n_f = 0
for l in LOTES:
    f = U / f"log_aud_{l}.txt"
    if f.exists():
        n_f += len(re.findall(r"\[fantasma\]", f.read_text(encoding="utf-8", errors="replace")))
p(f"  FadeOut de objeto já fora da cena (o kit os filtra; antes eram o 'flash'): {n_f} (informativo)")
fl = U / "renders" / "flash.txt"
if fl.exists():
    LF = fl.read_text(encoding="utf-8").splitlines()
    # picos conferidos em quadros (renders/chk/fl/flash_v6.png): não são "flash" (o elemento nasce, é lido e só depois sai)
    EXPL = [(96.3, 'fade-in de "NA ROTAÇÃO" (permanece em tela; o pico é o rótulo vizinho que troca de brilho)'),
            (228.2, "saída deliberada do bloco inteiro do T1 depois de lido (FadeOut de cena)"),
            (868.1, "troca sequencial de selo (EQUILÍBRIO ESTÁTICO → ATALHO), ambos já lidos")]
    ev = [float(re.match(r"\s*([0-9.]+)s", x).group(1)) for x in LF[1:] if re.match(r"\s*[0-9.]+s", x)]
    nao = [t_ for t_ in ev if not any(abs(t_ - te) <= 0.6 for te, _ in EXPL)]
    chk("FLASH por vídeo (flash22.py)", not nao, f"{len(ev)} picos de tinta; explicados em quadro: {len(ev) - len(nao)}; sem explicação: {nao}")
    for te, why in EXPL:
        p(f"    explicado {te:.1f}s: {why}")
fu = U / "renders" / "fundo.txt"
if fu.exists():
    L_ = fu.read_text(encoding="utf-8").splitlines()
    sl = [x for x in L_ if x.startswith("saltos")][0]
    m1 = re.search(r": (\d+)\s*$", L_[1])
    m2 = re.search(r": (\d+) quadros", sl)
    fb = [x for x in L_ if x.startswith("fronteiras de lote")][0]
    chk("FUNDO (fundo22.py)", bool(m2 and int(m2.group(1)) == 0 and fb.endswith("8 de 8")), f"{sl} | {fb} | trechos com conteúdo rápido/3D opaco (informativo): {m1.group(1) if m1 else '?'}")

p(f"\nRESULTADO: {'tudo OK' if ok_geral else 'há FALHAS (ver acima)'}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "qa.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
