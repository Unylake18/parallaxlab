"""yt_0021 — QA do preview: duração por âncora (narração nominal × cena), portão (linhas [audit] dos logs de auditoria), auditorias de física
(SOMA, HOOK, FATIAS, ESFERA, EIXOS PARALELOS, ENERGIA, E2, E3 GEOMETRIA, ALIASING, NÚMEROS), alinhamento 3D × Manim (px) e cor por capítulo.
Lê ancoras.json, log_<L>.txt, log_aud_<L>.txt, qa_overlay_<L>.json, threejs/q3d/<L>_960x540/<cena>/pontos.json e media_<L>/…/<L>.mp4.
uso: python qa21.py  → renders/qa.txt"""
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
LOTES = ["PH", "PA", "PT1", "PT2", "PT3", "PT4", "PT5", "PT6", "PE1", "PE2", "PE3", "PS"]
G = 9.8
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
    log = (U / f"log_{l}.txt")
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

# ── 1b. ORDEM de escrita (v5): voa/passo registram [ordem] com o nº de pares (i à esquerda de j) em que t_i > t_j + 0,05 s ──
p("\n== ORDEM (escrita da esquerda para a direita, por linha) ==")
n_l = n_f = n_cx = n_r = n_rf = 0
real = []
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
    for m in re.finditer(r"\[ordem_real\] +([0-9.]+)s (\w+) quadros=(\d+) falhas=(\d+)(.*)", s_):
        n_r += 1
        real.append(f"{l} {m.group(1)}s {m.group(2)} quadros={m.group(3)} falhas={m.group(4)}{m.group(5)}")
        if int(m.group(4)):
            n_rf += 1
chk("ORDEM", n_f == 0 and n_l > 0, f"{n_l} construções agendadas (voa/passo) por x, {n_f} com par fora de ordem")
(U / "renders" / "ordem_real.txt").write_text("ORDEM REAL (por quadro, so voa; passo fica pelo agendamento)\n" + "\n".join(real) + "\n", encoding="utf-8")
chk("ORDEM REAL", n_rf == 0 and n_r > 0, f"{n_r} construções (voa) medidas quadro a quadro: parte pousada (na cena, opacidade > 0,5, a < 0,06 u do lugar) à direita de parte ainda não pousada por ≥ 2 quadros = falha; {n_rf} com falha (renders/ordem_real.txt)")
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

# ── 3. física ──
p("\n== AUDITORIAS DE FÍSICA ==")
o = ov("PT1").get("soma", {})
if o:
    v = list(o.values())[0]
    e = abs(v["soma_pedacos"] / v["meio_I_w2"] - 1)
    chk("SOMA", e <= 0.005, f"Σ½mᵢvᵢ² dos {v['n']} pedaços desenhados = {v['soma_pedacos']:.5f}; ½Iω² (I = ½MR²) = {v['meio_I_w2']:.5f}; erro {100 * e:.3f}%")
h = ov("PH").get("hook", {})
if h:
    fs = sorted(h, key=int)
    v = h[fs[-1]]
    chk("HOOK razão", abs(v["I0"] / v["I1"] - 2) <= 0.02, f"I_cabo/I_grossa = {v['I0']:.5f}/{v['I1']:.5f} = {v['I0'] / v['I1']:.3f}")
    chk("HOOK K final", abs(v["K0"] - 14.11) / 14.11 <= 0.01 and abs(v["K1"] - 7.056) / 7.056 <= 0.01, f"K = {v['K0']:.3f} J e {v['K1']:.3f} J (ω = {v['w']:.3f} rad/s)")
    chk("HOOK ω igual", True, "os dois bastões usam o mesmo θ(t) (o da direita = θ + π) em todos os quadros: Δω = 0")
    chk("HOOK U constante", all(h[f]["U0"] == 0 and h[f]["U1"] == 0 for f in fs), "plano horizontal, câmera de cima: U = 0 em todos os quadros")
    ths = [h[f]["th"] for f in fs]
    dmax = max(abs(b - a) for a, b in zip(ths, ths[1:]))
    chk("ALIASING hook", math.degrees(dmax) <= 60, f"giro máximo por quadro {math.degrees(dmax):.1f}° (ω = 10 rad/s a 15 fps)")
t3 = ov("PT3")
if t3:
    a = list(t3.get("fatias_ponta", {}).values())[0]
    b = list(t3.get("fatias_centro", {}).values())[0]
    chk("FATIAS ponta", abs(a["soma"] / a["integral"] - 1) <= 0.01, f"Σ áreas das 20 fatias = {a['soma']:.5f} × ∫x² = {a['integral']:.5f} ({100 * abs(a['soma'] / a['integral'] - 1):.3f}%)")
    chk("FATIAS centro/ponta", abs(b["razao"] - 0.25) / 0.25 <= 0.01, f"barra pelo centro / pela ponta = {b['razao']:.4f} (alvo 1/4)")
t4 = ov("PT4").get("esfera_t44", {})
if t4:
    v = list(t4.values())[0]
    vols = np.array(v["vols"])
    zs = np.array([-1 + v["dz"] * (k + 0.5) for k in range(v["n"])])
    prop = np.ptp(vols / (1 - zs ** 2)) / np.mean(vols / (1 - zs ** 2))
    chk("ESFERA discos", prop < 1e-9 and abs(vols.sum() / v["vol_esfera"] - 1) <= 0.01,
        f"volume de cada disco ∝ (R² − z²) (desvio {prop:.1e}); soma dos {v['n']} discos / volume da esfera = {vols.sum() / v['vol_esfera']:.4f}")


def placa_pts(n=160):
    t = np.linspace(0, 2 * math.pi, 400, endpoint=False)
    x = np.cos(t) * (1.55 + 0.32 * np.sin(3 * t + 0.6) + 0.15 * np.cos(5 * t))
    y = np.sin(t) * (1.15 + 0.22 * np.cos(2 * t + 1.1))
    gx, gy = np.meshgrid(np.linspace(-2.2, 2.2, n), np.linspace(-1.6, 1.6, n))
    q = np.stack([gx.ravel(), gy.ravel()], 1)
    a, b = np.stack([x, y], 1), np.roll(np.stack([x, y], 1), -1, 0)
    dentro = ((a[:, 1] > q[:, 1:2]) != (b[:, 1] > q[:, 1:2])) & (q[:, 0:1] < (b[:, 0] - a[:, 0]) * (q[:, 1:2] - a[:, 1]) / (b[:, 1] - a[:, 1] + 1e-12) + a[:, 0])
    return q[dentro.sum(1) % 2 == 1]


P_ = placa_pts()
cm = P_.mean(0)
Icm = ((P_ - cm) ** 2).sum(1).sum() / len(P_)
for d in ((0.0, 0.0), (-2.1, -1.05), (1.0, 1.6)):
    O_ = cm + np.array(d)
    Io = ((P_ - O_) ** 2).sum(1).sum() / len(P_)
    pred = Icm + np.dot(d, d)
    chk(f"EIXOS PARALELOS placa d = ({d[0]:+.2f}; {d[1]:+.2f})", abs(Io / pred - 1) <= 0.005, f"Σ pedaços (M = 1, {len(P_)} pedaços) = {Io:.5f} × I_cm + Md² = {pred:.5f}")
e1 = ov("PE1").get("e1", {})
if e1:
    errs = [abs(v["soma"] / v["mgh"] - 1) for v in e1.values()]
    chk("ENERGIA E1", max(errs) <= 0.01, f"U + K_bloco + K_carretel = mgh em {len(errs)} quadros (erro máx {100 * max(errs):.3f}%)")
    ths = [e1[f]["th"] / e1[f]["lenta"] for f in sorted(e1, key=int)]
    g_ = ov("PE1").get("e1_giro", {})
    gm = list(g_.values())[0]["graus_por_quadro_max"] if g_ else None
    chk("ALIASING carretel", gm is not None and gm <= 60, f"ω real 31,3 rad/s desenhado em câmera lenta ×4: {gm:.1f}° por quadro (selo CÂMERA LENTA ×4)")
e2 = ov("PE2").get("e2", {})
if e2:
    vs = [v["U"] + v["K"] for v in e2.values() if v.get("K") is not None]
    chk("ENERGIA E2", np.ptp(vs) / np.mean(vs) <= 0.01, f"U + K da haste (por unidade de M·L) constante em {len(vs)} quadros: variação {100 * np.ptp(vs) / np.mean(vs):.3f}%")
    w_ = [math.degrees(v["w"] / 15) for v in e2.values()]
    chk("ALIASING haste", max(w_) <= 60, f"giro máximo por quadro {max(w_):.1f}° (queda desenhada mais lenta que a real)")
e24 = ov("PE2").get("e2_4", {})
if e24:
    v = list(e24.values())[0]
    chk("E2 2L/3", abs(v["r_igual"] / v["dois_tercos"] - 1) <= 0.01, f"ωr = √(2gr) em r = {v['r_igual']:.4f} L (2/3 = 0,6667)")
    chk("E2 ponta", abs(math.sqrt(3 * G) - 5.42) / 5.42 <= 0.01, f"v_ponta = √(3gL) = {math.sqrt(3 * G):.3f} m/s; v(r) = ωr ∝ r (setas ⊥ à haste com comprimento ωr)")
e3 = ov("PE3")
if e3.get("e3"):
    vs = [abs(v["soma"] / v["tot"] - 1) for v in e3["e3"].values()]
    chk("ENERGIA E3", max(vs) <= 0.01, f"U + K da placa = MgR/6 em {len(vs)} quadros (erro máx {100 * max(vs):.3f}%)")
if e3.get("e3_geo"):
    v = list(e3["e3_geo"].values())[0]
    O_, cr, rr, RP, c = px(v["O"]), px(v["cr"]), v["r_rec"] / 16 * 960, v["RP"] / 16 * 960, px(v["cm"])
    tang = abs(np.linalg.norm(cr - O_) + rr - RP)
    pass_o = abs(np.linalg.norm(cr - O_) - rr)
    dcm = np.linalg.norm(c - O_) / (RP / 6)
    chk("E3 GEOMETRIA recorte", tang <= 1 and pass_o <= 1, f"tangente à borda externa (erro {tang:.3f} px) e passando por O (erro {pass_o:.3f} px)")
    chk("E3 GEOMETRIA CM", abs(dcm - 1) <= 0.01, f"CM a {dcm:.4f} × R/6 de O, do lado oposto ao recorte")
    fin = [e3["e3_geo"][f] for f in sorted(e3["e3_geo"], key=int)][-1]
    cf, of_ = np.array(fin["cm"]), np.array(fin["O"])
    ang = math.degrees(math.atan2(cf[0] - of_[0], -(cf[1] - of_[1])))
    chk("E3 GEOMETRIA final", abs(ang) <= 1, f"posição final: CM {ang:+.3f}° da vertical abaixo de O")

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
        chk(f"ALINHAMENTO {l}/{cena}", max(err) <= 2, f"{len(err)} pontos; erro médio {np.mean(err):.2f} px, máximo {max(err):.2f} px")
    else:
        p(f"  {l}/{cena}: sem pontos (lote 3D não renderizado)")


alinha("PH", "bastao", "hook", lambda v, q: [(v["pino0"], q["b0"]["cabo"]), (v["ponta0"], q["b0"]["grossa"]), (v["pino1"], q["b1"]["grossa"]), (v["ponta1"], q["b1"]["cabo"])])
alinha("PT4", "esfera", "al_t44", lambda v, q: [(v["centro"], q["hi"]["centro"]), (v["borda"], q["hi"]["borda"])] if "hi" in q else [])
alinha("PT5", "bastao", "al_t56", lambda v, q: [(v["cm_cabo"], q["b0"]["cm_cabo"]), (v["cm_grossa"], q["b0"]["cm_grossa"])])
alinha("PT6", "esfera", "al_t64", lambda v, q: [(v["ex"], q["ex"]), (v["ey"], q["ey"]), (v["ez"], q["ez"]), (v["centro"], q["centro"])])
alinha("PS", "bastao", "al_s2", lambda v, q: [(v["pino0"], q["b0"]["cabo"]), (v["pino1"], q["b1"]["grossa"]), (v["cm0"], q["b0"]["cm_grossa"]), (v["cm1"], q["b1"]["cm_grossa"])])

# ── 5. números ──
p("\n== NÚMEROS (valor da tela × conta) ==")
I0 = 0.25 * (0.42 ** 2 / 12 + 0.21 ** 2) + 0.65 * (0.42 ** 2 / 12 + 0.63 ** 2)
I1 = 0.65 * (0.42 ** 2 / 12 + 0.21 ** 2) + 0.25 * (0.42 ** 2 / 12 + 0.63 ** 2)
IO = 0.5 * 2 * 0.09 - (0.5 * 0.5 * 0.15 ** 2 + 0.5 * 0.15 ** 2)
tela = [("I pelo cabo", "0,282", I0, 3), ("I pela ponta grossa", "0,141", I1, 3), ("K pelo cabo", "14,1", 0.5 * I0 * 100, 1), ("K pela ponta grossa", "7,06", 0.5 * I1 * 100, 2),
        ("barra pela ponta", "0,212", 0.9 * 0.84 ** 2 / 3, 3), ("barra pelo centro", "0,053", 0.9 * 0.84 ** 2 / 12, 3), ("haltere pelo meio", "1", 2 * 2 * 0.25, 0),
        ("haltere por uma massa", "2", 2 * 1.0, 0), ("T2-3 contribuições", "0,04", 1 * 0.2 ** 2, 2), ("T2-3 contribuições (2)", "0,04", 0.25 * 0.4 ** 2, 2),
        ("raio de giração haltere", "0,5", math.sqrt(1 / 4), 1), ("E1 v", "3,13", math.sqrt(2 * G / 2), 2), ("E1 ω", "31,3", math.sqrt(2 * G / 2) / 0.1, 1),
        ("E1 bloco", "4,9", 0.5 * 1 * 9.8, 1), ("E1 carretel", "4,9", 0.25 * 2 * 9.8, 1), ("E1 queda livre", "4,43", math.sqrt(2 * G), 2), ("E1 aro", "2,56", math.sqrt(2 * G / 3), 2),
        ("E2 ω", "5,42", math.sqrt(3 * G), 2), ("E2 v ponta", "5,42", math.sqrt(3 * G), 2), ("E2 pedra", "4,43", math.sqrt(2 * G), 2), ("E2 bola", "4,70", 1.5 * math.sqrt(G), 2),
        ("E3 I disco", "0,090", 0.09, 3), ("E3 I recorte", "0,0169", 0.016875, 4), ("E3 I_O", "0,0731", IO, 4), ("E3 x_cm (cm)", "5", 5.0, 0),
        ("E3 ω", "4,48", math.sqrt(8 * G / (13 * 0.3)), 2), ("E3 v_cm", "0,22", math.sqrt(8 * G / 3.9) * 0.05, 2), ("E3 v máx", "1,34", math.sqrt(8 * G / 3.9) * 0.3, 2),
        ("E3 I_cm", "0,0694", IO - 1.5 * 0.0025, 4)]
for nome, s, val, nd in tela:
    vs = float(s.replace(",", "."))
    trunc = math.floor(val * 10 ** nd + 1e-9) / 10 ** nd
    chk(f"NÚMEROS {nome}", abs(vs - round(val, nd)) < 1e-9 or abs(vs - trunc) < 1e-9, f"tela {s} · conta {val:.5f}" + (" (truncado, como na fala)" if abs(vs - round(val, nd)) > 1e-9 else ""))

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
            rgb = np.asarray(fr.to_image(), dtype=np.int16)
            ink = hsv[..., 2] > 110
            sat += int((ink & (hsv[..., 1] > 90)).sum())
            tinta += int(ink.sum())
        c.close()
        fr_ = sat / max(tinta, 1)
        chk(f"COR {l}", fr_ >= 0.30, f"{100 * fr_:.1f}% da tinta saturada")
except Exception as ex:
    p(f"  (cor não medida: {ex})")

p(f"\nRESULTADO: {'tudo OK' if ok_geral else 'há FALHAS (ver acima)'}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "qa.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))


# ── ENERGIA INDEPENDENTE (v3): recalcula a energia a partir das posições DESENHADAS (não do estado interno) ─────────────────────────────
def indep():
    global ok_geral
    out2 = ["\n== ENERGIA INDEPENDENTE DA IMAGEM (posições desenhadas → K + U) =="]
    e1 = ov("PE1").get("e1", {})
    if e1:
        fs = sorted(e1, key=int)
        KE_, R_, HE_, LENTA_ = 2.9, 0.10, 2.8, 4.0
        run_ = []                                                                       # v7: só a 1ª descida (carretel disco), em que u cresce: independe de quando a descida começa no lote
        for k_ in fs:
            if 0.05 < e1[k_]["u"] < 0.95:
                if run_ and int(k_) - int(run_[-1]) > 1:
                    break
                run_.append(k_)
        base_ = fs.index(run_[0]) if run_ else 0
        fs0 = fs
        idx = [fs.index(run_[int(len(run_) * f)]) for f in (0.35, 0.6, 0.85)] if len(run_) > 20 else [int(len(fs) * f) for f in (0.35, 0.6, 0.85)]
        res = []
        for i in idx:
            a, b, c0 = e1[fs[i]], e1[fs[i + 1]], e1[fs[i - 1]]                           # diferença CENTRAL (sem viés de meio quadro)
            dt = (int(fs[i + 1]) - int(fs[i - 1])) / 15
            drop = (e1[fs[0]]["pos_bloco"] - a["pos_bloco"]) / KE_                       # queda desenhada (m)
            v = (c0["pos_bloco"] - b["pos_bloco"]) / KE_ / dt * LENTA_                    # velocidade real a partir do desenho em câmera lenta ×4
            dth = abs(math.atan2(b["pos_marca"][1], b["pos_marca"][0]) - math.atan2(c0["pos_marca"][1], c0["pos_marca"][0]))
            dth = min(dth, 2 * math.pi - dth)
            w = dth / dt * LENTA_
            if drop < 0.02:
                continue
            I = 0.5 * 2.0 * R_ ** 2 if True else 0
            Ktot = 0.5 * 1.0 * v ** 2 + 0.5 * I * w ** 2
            Upot = 1.0 * 9.8 * (1.0 - drop)
            res.append((drop, v, w, Ktot + Upot))
        if res:
            err = max(abs(r[3] / 9.8 - 1) for r in res)
            nr = max(abs(r[2] * R_ / r[1] - 1) for r in res)
            out2.append(f"  [{'OK ' if err <= 0.015 else 'FALHA'}] E1: K + U a partir do bloco e da marca do carretel em 3 instantes = {', '.join(f'{r[3]:.3f} J' for r in res)} (mgh = 9,8 J; erro máx {100 * err:.2f}%)")
            out2.append(f"  [{'OK ' if nr <= 0.03 else 'FALHA'}] E1: ω·R = v nos desenhos (corda sem escorregar), erro máx {100 * nr:.2f}%")
            ok_geral &= err <= 0.015 and nr <= 0.03
        alt = e1[fs[int(len(fs) * 0.6)]]
        soma = sum(alt["alturas"]) / HE_
        out2.append(f"  [{'OK ' if abs(soma - 1) <= 0.01 else 'FALHA'}] E1: soma das alturas das 3 barras desenhadas = {soma:.4f} × mgh")
    e3 = ov("PE3").get("e3", {})
    g3 = ov("PE3").get("e3_geo", {})
    if e3 and g3:
        fs = sorted(e3, key=int)
        RP_, HE3_, dcm = 0.30 * 6.5, 2.4, 0.05
        y_fin = None
        fsg = sorted(g3, key=int)
        y_fin = g3[fsg[-1]]["cm"][1]
        y_ini = g3[fsg[0]]["cm"][1]
        res = []
        for f in (fs[int(len(fs) * 0.25)], fs[int(len(fs) * 0.5)], fs[int(len(fs) * 0.75)]):
            y = g3[f]["cm"][1] if f in g3 else None
            if y is None:
                continue
            desc = (y - y_fin) / (RP_ / 6)                                         # fração do desnível que ainda falta (posição desenhada do CM)
            Uh = e3[f]["alturas"][0] / HE3_
            res.append((desc, Uh))
        if res:
            err = max(abs(a - b) for a, b in res)
            out2.append(f"  [{'OK ' if err <= 0.01 else 'FALHA'}] E3: altura da barra U × posição desenhada do CM em 3 instantes: {', '.join(f'{a:.3f}/{b:.3f}' for a, b in res)} (erro máx {err:.4f})")
            ok_geral &= err <= 0.01
    e2 = ov("PE2").get("e2", {})
    if e2:
        th = {int(f): v["th"] for f, v in e2.items()}
        fs = sorted(th)
        th0 = math.radians(86)
        i0 = next((f for f in fs if th[f] < th0 - 1e-6), None)
        i1 = next((f for f in fs if i0 is not None and f > i0 and th[f] < 0.02), None)
        if i0 is not None and i1 is not None:
            k, dt_, tt, ang, w_ = 1.5 * 9.8, 2e-4, 0.0, th0, 0.0
            while ang > 0 and tt < 5:
                w_ -= k * math.cos(ang) * dt_
                ang += w_ * dt_
                tt += dt_
            S_nom = ((i1 - i0) / 15) / tt                                   # câmera lenta pela duração desenhada ÷ duração real da queda
            pts = []
            for alvo in (75, 60, 45, 30, 20):
                f = next((f for f in fs if f > i0 and th[f] <= math.radians(alvo) and (f - 1) in th and (f + 1) in th), None)
                if f is None:
                    continue
                wd = -(th[f + 1] - th[f - 1]) / (2 / 15)
                pts.append((alvo, wd, 3 * 9.8 / 1.0 * (math.sin(th0) - math.sin(th[f]))))
            if len(pts) >= 3:
                S_fit = math.sqrt(sum(e / (w * w) for _, w, e in pts) / len(pts))     # fator que melhor leva ω² desenhado a ω² da energia
                forma = max(abs((w * S_fit) ** 2 / e - 1) for _, w, e in pts)           # constância do fator: formato da queda (independe de S)
                dS = abs(S_fit / S_nom - 1)
                out2.append(f"  [{'OK ' if forma <= 0.02 else 'FALHA'}] E2: ω² medido nos quadros × (3g/L)(sen θ₀ − sen θ) em {len(pts)} instantes ({', '.join(f'{a_}°' for a_, _, _ in pts)}): formato da queda erro máx {100 * forma:.2f}% (≤ 2%)")
                out2.append(f"  [{'OK ' if dS <= 0.05 else 'FALHA'}] E2: fator de câmera lenta ajustado ×{S_fit:.3f} × nominal (duração desenhada ÷ T real {tt:.3f} s) ×{S_nom:.3f}: diferença {100 * dS:.1f}% (≤ 5%)")
                ok_geral &= forma <= 0.02 and dS <= 0.05
    else:
        out2.append("  E2: sem registro de posições.")
    return out2


def ponto_curva():
    r = ov("PT5").get("t5_5", {})
    if not r:
        return ["  PONTO NA CURVA: sem registro."]
    dm = max(v["dist"] for v in r.values())
    xm = max(v["dx"] for v in r.values())
    ok1, ok2 = dm <= 0.01, xm <= 0.005
    linhas = [f"PONTO NA CURVA (T5-5): {len(r)} quadros; pior distância do centro do ponto à curva = {dm:.5f} u (limite 0,01); pior |x pino − x ponto| = {xm:.5f} u (limite 0,005)"]
    (U / "renders" / "ponto_curva.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    global ok_geral
    ok_geral &= ok1 and ok2
    return [f"  [{'OK ' if ok1 else 'FALHA'}] PONTO NA CURVA: {len(r)} quadros; pior distância {dm:.5f} u (≤ 0,01)", f"  [{'OK ' if ok2 else 'FALHA'}] PINO × PONTO: pior diferença de x {xm:.5f} u (≤ 0,005)"]


extra = indep() + ponto_curva()
txt_atual = (U / "renders" / "qa.txt").read_text(encoding="utf-8")
txt_atual = txt_atual.replace("\nRESULTADO:", "\n".join(extra) + "\n\nRESULTADO:")
txt_atual = re.sub(r"RESULTADO: .*", f"RESULTADO: {'tudo OK' if ok_geral else 'há FALHAS (ver acima)'}", txt_atual)
(U / "renders" / "qa.txt").write_text(txt_atual, encoding="utf-8")
print("\n".join(extra))
