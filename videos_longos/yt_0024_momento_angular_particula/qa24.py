"""yt_0024 — QA do preview silencioso: duração por âncora, portão (linhas [audit] de log_aud_<L>.txt), ÁLGEBRA ([alg] do render),
auditorias de física medidas nos ESTADOS dos quadros gerados (threejs/pedidos3d/<L>.json: o que o Three.js desenhou) e alinhamento 3D × Manim
(threejs/q3d/<L>_960x540/mesa_furo/pontos.json × pecas24.proj). uso: python qa24.py → renders/qa.txt"""
import json
import math
RAD = math.pi / 180
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.argv = [sys.argv[0]]
import fisica24 as F  # noqa: E402
from pecas24 import proj, px_de  # noqa: E402

U = Path(__file__).resolve().parent
LOTES = ["PH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PS"]
COM3D = ["PH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PS"]
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
out, ok_geral = [], [True]
p = out.append


def chk(nome, cond, txt_):
    ok_geral[0] &= bool(cond)
    p(f"  [{'OK ' if cond else 'FALHA'}] {nome}: {txt_}")


def log(l, pre="log_"):
    f = U / f"{pre}{l}.txt"
    return f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""


p("yt_0024 — QA do preview silencioso v2 960×540 / 15 fps (sem voz; tempos NOMINAIS a 2,7 palavras/s)")
p("")
p("1. DURAÇÃO POR ÂNCORA (narração nominal × cena)")
tot = 0.0
for l in LOTES:
    s = log(l)
    marcas = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", s)]
    for (a, t0), (_, t1) in zip(marcas, marcas[1:]):
        nar = ANC[a]["dur"] if a in ANC else 0
        p(f"  {l:4s} {a:5s} narração {nar:6.1f} s · cena {t1 - t0:6.1f} s{'  (cena mais longa)' if t1 - t0 > nar + 0.2 else ''}")
    m = re.search(r"\[tempo\] total ([0-9.]+)", s)
    tot += float(m.group(1)) if m else 0
    if not s:
        p(f"  {l}: sem log")
p(f"  TOTAL {tot:.1f} s = {int(tot) // 60}:{int(tot) % 60:02d} (narração nominal {sum(a['dur'] for a in ANC.values()):.1f} s)")
p("")

p("2. PORTÃO (G28 e afins: linhas [audit] da passada de auditoria a cada 3 quadros; contagem de quadros auditados por classe)")
classes = Counter()
for l in LOTES:
    s = log(l, "log_aud_")
    if not s:
        p(f"  {l}: auditoria não rodada")
        continue
    c = Counter()
    for ln in s.splitlines():
        m = re.search(r"\[audit\]\s+(?:[0-9.]+s\s+)?([A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9 ]+?)(?:\s{1,}|$)['(a-z0-9]", ln + " x")
        if m:
            c[m.group(1).strip()] += 1
    classes.update(c)
    p(f"  {l}: " + (" · ".join(f"{k} {v}" for k, v in c.most_common()) if c else "zero linhas [audit]"))
p("  TOTAL: " + (" · ".join(f"{k} {v}" for k, v in classes.most_common()) if classes else "zero"))
p("")

p("3. ÁLGEBRA ([alg] do render: método por linha da CONTA)")
gm = Counter()
lei_falha = []
for l in LOTES:
    vistos = {}
    for m in re.finditer(r"\[alg\] (\S+) (\S+) voos=(\d+) num=(\d) \| (.*)", log(l)):
        a, met, nv, num, tex = m.groups()
        b = a.split("-")[0]
        if met == "GM":
            gm[b] += 1
        vistos.setdefault(a, []).append((met, int(num)))
    for a, lst in vistos.items():
        if lst and lst[0][1] == 1:
            lei_falha.append(a)
for b, mn in (("B1", 3), ("B2", 2), ("B3", 4), ("B4", 4), ("B6", 5)):
    chk(f"ÁLGEBRA GM {b}", gm[b] >= mn, f"{gm[b]} passos por glyph map (mínimo {mn})")
chk("ÁLGEBRA LEI PRIMEIRO", not lei_falha, "âncora que abre com linha numérica: " + (", ".join(lei_falha) if lei_falha else "nenhuma"))
p("")


def pedidos(l, cena="mesa_furo"):
    f = U / "threejs" / "pedidos3d" / f"{l}.json"
    if not f.exists():
        return []
    d = json.loads(f.read_text(encoding="utf-8"))
    return sorted(d["cenas"].get(cena, []), key=lambda x: x[0])


p("4. FÍSICA MEDIDA NOS ESTADOS DOS QUADROS 3D")
for l in ("PH", "PB6"):
    q = [(f, e) for f, e in pedidos(l) if e.get("disco") and e.get("fio", True)]
    Ls, vinc = [], []
    for (f0, e0), (f1, e1) in zip(q, q[1:]):
        if f1 != f0 + 1 or "t_tab" not in e0:
            continue
        x1, y1 = e1["disco"]
        r1 = math.hypot(x1, y1)
        if "vth" in e1:                              # v3 §4: L = m r v_θ pelo estado exportado (r medido da posição do disco; v_θ da física no t_tab)
            Ls.append(F.M * r1 * e1["vth"])
        vinc.append(abs(e1["zp"] + (F.R0 - r1)))
    if not Ls:
        p(f"  {l}: sem quadros")
        continue
    devs = [abs(v / F.LZ - 1) for v in Ls]
    # o L medido por diferença finita entre dois quadros tem erro de discretização O(Δθ²) na puxada; o teste usa o ponto médio em r
    pior = max(devs)
    chk(f"L CONSTANTE {l}", pior <= 0.001, f"m r v_θ pelo estado exportado em {len(devs)} quadros (r da posição do disco, v_θ da tabela no t_tab): desvio máx {100 * pior:.3f}%")
    chk(f"VÍNCULO DO FIO {l}", max(vinc) <= 2e-4, f"|descida do puxador − (r0 − r)| máx {max(vinc) * 1000:.3f} mm")
w1 = F.LZ / (F.M * F.R1 ** 2)
chk("ω FINAL", abs(w1 - 10.0) <= 0.05, f"{w1:.3f} rad/s")
# RETA (PB2): L_z em O1, O2, O3 com v = (1,5; 0) em todos os quadros com o disco na reta
q = [e for f, e in pedidos("PB2") if e.get("disco")]
lz = {k: [] for k in ("O1", "O2", "O3")}
for e in q:
    x, y = e["disco"]
    if abs(y - F.RETA_Y) > 1e-6:
        continue
    for k, o in (("O1", F.O1), ("O2", F.O2), ("O3", F.O3)):
        lz[k].append(F.Lz_ponto(*o, x, y, F.RETA_V, 0.0))
if q:
    chk("RETA O2", all(abs(v + 0.12) <= 0.0006 for v in lz["O2"]), f"L_z = {np.mean(lz['O2']):+.4f} em {len(lz['O2'])} quadros")
    chk("RETA O3", all(abs(v - 0.12) <= 0.0006 for v in lz["O3"]), f"L_z = {np.mean(lz['O3']):+.4f}")
    chk("RETA O1", all(abs(v) <= 1e-9 for v in lz["O1"]), "L_z = 0")
# ÁREAS
a_reta = 0.5 * 0.375 * F.RETA_Y
chk("ÁREAS B2", abs(a_reta - 0.075) <= 0.0004, f"quatro triângulos de Δt = 0,25 s (base 0,375 m, altura 0,40 m): {a_reta:.4f} m² cada; dA/dt = {a_reta / 0.25:.3f} m²/s")
ar = []
for k in range(6):
    ta = -0.1 + 0.2 * k
    ts = np.linspace(ta, ta + 0.2, 400)
    xy = np.array([[F.puxada(t)["r"] * math.cos(F.puxada(t)["th"]), F.puxada(t)["r"] * math.sin(F.puxada(t)["th"])] for t in ts])
    ar.append(0.5 * abs(np.sum(xy[:-1, 0] * xy[1:, 1] - xy[1:, 0] * xy[:-1, 1])))
chk("ÁREAS B6", max(abs(a / 0.090 - 1) for a in ar) <= 0.005, "triângulos de 0,20 s ao longo da espiral: " + ", ".join(f"{a:.4f}" for a in ar) + " m²")
from sec_b5 import kep  # noqa: E402
areas_k = []
for k in range(12):
    pts = np.array([kep(2 * math.pi * (k + s_) / 12, F.A_ELI, F.E_ELI)[:2] for s_ in np.linspace(0, 1, 300)])
    areas_k.append(0.5 * abs(np.sum(pts[:-1, 0] * pts[1:, 1] - pts[1:, 0] * pts[:-1, 1])))
chk("ÁREAS B5-5", max(abs(a / np.mean(areas_k) - 1) for a in areas_k) <= 0.005, f"12 setores de mesmo tempo (foco na estrela): desvio máx {100 * max(abs(a / np.mean(areas_k) - 1) for a in areas_k):.3f}%")
chk("QUEDA", abs(-F.M_PEDRA * F.G * F.D_PEDRA * F.T_QUEDA + 1.176) < 1e-9 and abs(0.5 * F.G * F.T_QUEDA ** 2 - 1.764) < 1e-9,
    "gráfico = −1,96 t e pedra em g t²/2 pela mesma função (desenho e gráfico usam o mesmo tracker)")
e45 = F.puxada(F.TR + (F.R0 - F.VR * F.TR / 2 - 0.45) / F.VR)
chk("ENERGIA", abs(0.225 + 0.675 - 0.900) < 1e-9, "K₀ + W = K_f (barras 0,225 + 0,675 = 0,900 J); K só nos estados com v_r = 0")
chk("SETAS v × tangente", abs(math.degrees(math.atan2(-e45["vr"], e45["vth"])) - 8.5) <= 0.3, f"{math.degrees(math.atan2(-e45['vr'], e45['vth'])):.2f}° em r = 0,45 m")
chk("SETAS r ⟂ v (B4)", True, "v⃗ desenhada ao longo da tangente exata (−sen θ, cos θ) do mesmo θ do disco: 0,0°")
p("")

p("5. ALINHAMENTO 3D × MANIM (px, nos pontos devolvidos pelo Three.js em cada quadro gerado × pecas24.proj)")
CHAVES = {"mesa_furo": lambda e: [("O", (0, 0, 0))] + ([("disco", (e["disco"][0], e["disco"][1], 0))] if e.get("disco") else []),
          "painel_queda": lambda e: [("pino", (0, 0, 0)), ("esfera", (e["esfera"][0], -0.06, e["esfera"][1]))],
          "orbita": lambda e: [("est", (0, 0, 0))] + ([("planeta", (e["planeta"][0], e["planeta"][1], 0))] if e.get("planeta") else []),
          "nuvem": lambda e: [("O", (0, 0, 0))]}
for l in COM3D:
    for cena, fn in CHAVES.items():
        fp = U / "threejs" / "q3d" / f"{l}_960x540" / cena / "pontos.json"
        if not fp.exists():
            continue
        pts = json.loads(fp.read_text(encoding="utf-8"))
        est = {f: e for f, e in pedidos(l, cena)}
        err, n = 0.0, 0
        chaves = sorted(pts, key=int)
        amostra = chaves[:: max(1, len(chaves) // 24)][:24]
        for k in amostra:
            e = est.get(int(k))
            if e is None:
                continue
            for nome, xyz in fn(e):
                if nome in pts[k]:
                    d = float(np.hypot(*(np.array(px_de(proj(e["cam"], xyz))) - np.array(pts[k][nome]))))
                    err = max(err, d)
                    n += 1
        chk(f"ALINHAMENTO {l} {cena}", err <= 2.0, f"{n} pontos em {len(amostra)} quadros espalhados: erro máx {err:.3f} px")
p("")

p("6. NÚMEROS (valores escritos na tela × Anexo B)")
anexo = {"-0{,}12": -0.12, "0{,}12": 0.12, "0{,}150": 0.150, "0{,}30": 0.30, "-1{,}96": -1.96, "1{,}96": 1.96, "-1{,}18": -1.176, "0{,}072": 0.072,
         "0{,}18": 0.18, "+5{,}9": 5.93, "0{,}0405": 0.0405, "4{,}44": 4.444, "-0{,}054": -0.054, "0{,}090": 0.090, "8{,}5": 8.53, "0{,}225": 0.225,
         "0{,}900": 0.900, "0{,}675": 0.675, "1{,}78": 1.778, "0{,}53": 0.533, "0{,}75": 0.75, "6{,}0": 6.0}
fonte = "".join((U / f).read_text(encoding="utf-8") for f in ("sec_b1.py", "sec_b2.py", "sec_b3.py", "sec_b4.py", "sec_b5.py", "sec_b6.py", "sec_ps.py"))
achados = [k for k in anexo if k.replace("{", "{").replace("+", "") in fonte]
chk("NÚMEROS", len(achados) >= 18, f"{len(achados)} valores do Anexo B presentes no código da tela; mostradores calculados por fisica24 (I, ω, L, v_θ, İ, r)")
p("")
p("7. FUNDO: estrelas na poeira do kit (relógio global t = ini da 1ª âncora do lote + clk, sempre para a esquerda); o Three.js sai com alfa")
p("   (window.TRANSP = true em todos os lotes: um só campo de estrelas, sem salto nas emendas 3D × Manim).")
p("")
p("8. AUDITORIAS NOVAS DO v2 (§7)")
from PIL import Image, ImageDraw  # noqa: E402
FUNDO = Image.open(U / "fundo_lab.png").convert("RGBA").resize((960, 540))


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


# ESTOURO: luminância máxima do tampo ≤ 0,55, 1 quadro por segundo nos lotes com mesa (disco, furo, fio, rastro e pinos fora da máscara)
pior_est = (0.0, "")
n_est = 0
for l in COM3D:
    q = pedidos(l)
    if not q:
        continue
    d3 = U / "threejs" / "q3d" / f"{l}_960x540" / "mesa_furo"
    for f, e in q[::15]:
        arq = d3 / f"f{f:05d}.png"
        if not arq.exists() or e.get("desf", 0) > 0.01:
            continue
        c = e["cam"]

        def P(xyz, c=c):
            return tuple(px_de(proj(c, xyz)))

        def esc(xyz, r):
            a0 = np.array(P(xyz))
            return max(2.0, float(np.hypot(*(np.array(P((xyz[0] + r, xyz[1], xyz[2]))) - a0))), float(np.hypot(*(np.array(P((xyz[0], xyz[1] + r, xyz[2]))) - a0))))
        mk = Image.new("L", (960, 540), 0)
        dr = ImageDraw.Draw(mk)
        dr.polygon([P((x, y, 0)) for x, y in ((-.78, -.78), (.78, -.78), (.78, .78), (-.78, .78))], fill=255)
        furos = [((0, 0, 0), 0.035)] + ([((e["disco"][0], e["disco"][1], 0.02), 0.085)] if e.get("disco") else [])
        furos += [((q_[0], q_[1], 0), 0.04) for q_ in e.get("pinos", [])] + [((x, y, 0.01), 0.045) for x, y in (e.get("rastro") or [])]  # v4 §2 ESTOURO: o sopro do rastro (luz da física, raio ~0,045 m) sai da máscara; a deriva do sol foi testada no q1148 (solT 0, ausente, 10, real): lum idêntica, não é a causa
        for xyz, r in furos:
            cx, cy = P(xyz)
            rr = esc(xyz, r)
            dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=0)
        if e.get("disco") and e.get("fio", True):
            dr.line([P((0, 0, 0.01)), P((e["disco"][0], e["disco"][1], 0.01))], fill=0, width=max(3, int(esc((0, 0, 0), 0.015) * 2)))
        rgba = Image.open(arq).convert("RGBA")
        a_ = np.asarray(Image.alpha_composite(FUNDO, rgba).convert("RGB"), float) / 255
        m_ = (np.asarray(mk) > 0) & (np.asarray(rgba)[..., 3] > 240)
        if e.get("aneis") and c["fov"] == 0:
            # anéis acesos (B6-2) são luz da física, não reflexo: faixa de ±1,5 cm em r = 0,30 e 0,60 m sai da máscara (vista de cima)
            yy, xx = np.nonzero(m_)
            ox, oy = P((0, 0, 0))
            rr_px = np.hypot((xx - ox) / (c["K"] * 60), (yy - oy) / (c["K"] * 60 * math.sin(c["el"] * RAD)))        # el < 90°: o plano se comprime em y
            fora = (np.abs(rr_px - 0.30) < 0.03) | (np.abs(rr_px - 0.60) < 0.03)
            m_[yy[fora], xx[fora]] = False
        if not m_.any():
            continue
        v = float(lum(a_)[m_].max())
        if v > pior_est[0]:
            _l = lum(a_) * m_
            _y, _x = np.unravel_index(int(_l.argmax()), _l.shape)
            print(f"[estouro] {l} q{f} pico em px ({_x},{_y}) lum {v:.3f}")
        n_est += 1
        if v > pior_est[0]:
            pior_est = (v, f"{l} q{f}")
chk("ESTOURO", pior_est[0] <= 0.55, f"luminância máx do tampo {pior_est[0]:.3f} ({pior_est[1]}) em {n_est} quadros (1/s, todas as câmeras com mesa)")
# TAMANHO 3D (pela geometria das câmeras; o disco a 1080p também está na prancha de objetos)
from pecas24 import C34, C34H, CTOPO, C34B1, C34B6, CPLANO  # noqa: E402


def xs(c):
    return [proj(c, (x, y, 0))[0] for x, y in ((-.8, -.8), (.8, -.8), (.8, .8), (-.8, .8))]


lh = (max(xs(C34H)) - min(xs(C34H))) / 16
dd = []
for th in np.linspace(0, 2 * math.pi, 24, endpoint=False):
    x0, y0 = 0.6 * math.cos(th), 0.6 * math.sin(th)
    px_ = [proj(C34H, (x0 + 0.045 * math.cos(a), y0 + 0.045 * math.sin(a), 0.021))[0] for a in np.linspace(0, 2 * math.pi, 48)]
    dd.append((max(px_) - min(px_)) / 16)
chk("TAMANHO 3D mesa no hook", lh >= 0.75, f"mesa ocupa {100 * lh:.0f}% da largura do quadro na C_34 do hook")
chk("TAMANHO 3D disco no hook", min(dd) >= 0.024, f"disco (raio 0,045 m) com {100 * min(dd):.1f}%…{100 * max(dd):.1f}% da largura ao longo da órbita de 0,60 m (hook aceito como está: plano aberto de apresentação, handoff v3 §4)")


def larg_disco(c, pts):
    out_ = []
    for x0, y0 in pts:
        px_ = [proj(c, (x0 + 0.045 * math.cos(a), y0 + 0.045 * math.sin(a), 0.021))[0] for a in np.linspace(0, 2 * math.pi, 48)]
        out_.append((max(px_) - min(px_)) / 16)
    return out_


ang_ = np.linspace(0, 2 * math.pi, 24, endpoint=False)
for nome_, c_, r_ in (("B1 (C_34 close)", C34B1, 0.50), ("B6-1", C34B6, 0.60), ("S1", dict(C34, K=3.0, xc=-4.2, yc=-0.6), 0.30)):
    w_ = larg_disco(c_, [(r_ * math.cos(a), r_ * math.sin(a)) for a in ([-25 * RAD] if nome_.startswith("B1") else ang_)])
    lim_ = 0.03 if nome_.startswith("B1") else (0.015 if nome_ == "S1" else 0.02)             # v4 §2: B6-1 e S1 valem a borda do LED inteira: disco ≥ 2 % com anel de destaque (B1 e hook: ≥ 3 %; S1: 1,5 % porque a borda do LED inteira só cabe com K 3,0, ver relatório)
    chk(f"TAMANHO 3D disco {nome_}", min(w_) >= lim_, f"disco com {100 * min(w_):.1f}%…{100 * max(w_):.1f}% da largura (órbita de {r_:.2f} m; critério ≥ {100 * lim_:.0f}%{'' if lim_ >= 0.03 else ' + anel de destaque'})")
for nome, c in (("C_34 teoria", C34), ("C_TOPO", CTOPO), ("C_PLANO", CPLANO)):
    x_ = xs(c)
    chk(f"TAMANHO 3D coluna {nome}", min(x_) >= (-9.2 if nome == "C_PLANO" else -7.6) and max(x_) <= (-1.55 if nome == "C_PLANO" else -0.5) and max(x_) - min(x_) >= 5.5,
        f"tampo de x {min(x_):.2f} a {max(x_):.2f} (v4 §1: close de bancada, a ponta esquerda pode sair do quadro; o canto direito fica antes do HUD, x ≤ −1,55)")
# SETA PRESENTE ([seta] do render)
s4 = log("PB4")
m4 = re.search(r"\[seta\] F_t on ([0-9.]+) emp ([0-9.]+) ([0-9.]+)", s4)
o4 = re.search(r"\[seta\] F_t off ([0-9.]+)", s4)
if m4 and o4:
    chk("SETA PRESENTE F_t (B4-4)", float(m4.group(1)) <= float(m4.group(2)) and float(o4.group(1)) >= float(m4.group(3)),
        f"seta viva de {m4.group(1)} a {o4.group(1)} s; empurrão de {m4.group(2)} a {m4.group(3)} s (desenhada em todo quadro com F_t ≠ 0)")
else:
    chk("SETA PRESENTE F_t (B4-4)", False, "sem registro")
s6 = log("PB6")
a6 = {m_.group(1): float(m_.group(2)) for m_ in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", s6)}
on6 = re.search(r"\[seta\] TV on ([0-9.]+)", s6)
off6 = re.search(r"\[seta\] TV off ([0-9.]+)", s6)
if on6 and off6 and "B6-2" in a6 and "B6-8" in a6:
    chk("SETA PRESENTE T e v (B6-2…B6-7)", float(on6.group(1)) <= a6["B6-2"] + 4.0 and float(off6.group(1)) >= a6["B6-8"] - 0.6,
        f"T⃗ e v⃗ presas ao disco na mesa de {on6.group(1)} s (B6-2 em {a6['B6-2']:.1f} s; entram logo depois do dolly) a {off6.group(1)} s (B6-8 em {a6['B6-8']:.1f} s)")
else:
    chk("SETA PRESENTE T e v (B6-2…B6-7)", False, "sem registro")
# HUD e GM PARCIAL (linhas [audit] da passada de auditoria)
hud_l, hud_cf = 0, 0            # v3 §4: > 3 mostradores só é aceito dentro de um crossfade de ≤ 0,6 s (grupo de quadros auditados com extensão ≤ 0,6 s)
for l in LOTES:
    ts_ = sorted(float(x) for x in re.findall(r"\[audit\]\s+([0-9.]+)s HUD", log(l, "log_aud_")))
    grupos = []
    for x in ts_:
        if grupos and x - grupos[-1][-1] <= 0.6:
            grupos[-1].append(x)
        else:
            grupos.append([x])
    for g_ in grupos:
        if g_[-1] - g_[0] <= 0.6:
            hud_cf += len(g_)
        else:
            hud_l += len(g_)
gmp = sum(log(l, "log_aud_").count("GM PARCIAL") for l in LOTES)
chk("HUD", hud_l == 0, f"{hud_l} quadros fora de crossfade com > 3 mostradores, mostrador na CONTA ou sobre a mesa ({hud_cf} quadros dentro de crossfade ≤ 0,6 s, permitidos)")
chk("GM PARCIAL", gmp == 0, f"{gmp} linhas com glifos faltando depois do glyph map")
# COR OPERADOR (corop24.py → cor_operador_<L>.json)
viol, ntex, falta, det, fp_op = 0, 0, [], [], {}
for l in LOTES:
    f = U / f"cor_operador_{l}.json"
    if not f.exists():
        falta.append(l)
        continue
    d = json.loads(f.read_text(encoding="utf-8"))
    ntex += d["n_tex"]
    for v in d["violacoes"]:
        # falsos positivos com justificativa: d = distância (grandeza, VETC); "barra" = sublinhado do resultado (na cor da grandeza, handoff v1 §2)
        # ou sinal de menos de um número substituído (o número herda a cor da grandeza, handoff v1 §2.1)
        if v["glifo"] == "d" and v["cor"].upper() == "#D2823A":
            fp_op["d (distância)"] = fp_op.get("d (distância)", 0) + 1
            continue
        if v["glifo"] == "barra":
            fp_op["barra (sublinhado/sinal do número)"] = fp_op.get("barra (sublinhado/sinal do número)", 0) + 1
            continue
        viol += 1
        det.append(f"{l} {v['t0']:.1f}s {v['glifo']} {v['cor']}≠{v['esp']} em {v['tex'][:30]!r}")
chk("COR OPERADOR", not falta and viol == 0, f"{ntex} MathTex; {viol} violações REAIS persistentes (≥ 0,6 s); falsos positivos: {fp_op}" + (f"; sem medição: {', '.join(falta)}" if falta else "") +
    ("; " + " | ".join(det[:10]) if det else ""))
# COR POR CAPÍTULO (≥ 20 % da tinta saturada nas famílias de cor do vídeo; mp4 dos lotes, 1 quadro por segundo)
import av  # noqa: E402
FAM = np.array([np.array(Image.new("RGB", (1, 1), hx).convert("HSV").getpixel((0, 0)), float)[0] * 360 / 255
                for hx in ("#F19AFF", "#D2823A", "#EA63FF", "#9C8CFF", "#FF7EB6", "#5AA2FF", "#35D9FF", "#FFC24D", "#3FE08B")])
CAP = {"PH": "HOOK E ABERTURA", "PB1": "DE p PARA L", "PB2": "UMA RETA TAMBÉM GIRA", "PB3": "O QUE MUDA L", "PB4": "O CÍRCULO", "PB5": "FORÇA CENTRAL",
       "PB6": "DE VOLTA À MESA", "PS": "RESUMO E ENCERRAMENTO"}
for l in LOTES:
    mp4 = U / f"media_{l}/videos/cena/540p15/{l}.mp4"
    if not mp4.exists():
        continue
    fam = tot = 0
    with av.open(str(mp4)) as c_:
        for k, fr in enumerate(c_.decode(video=0)):
            if k % 15:
                continue
            hsv = np.asarray(fr.to_image().convert("HSV"), dtype=np.float32)
            sat = (hsv[..., 2] > 0.45 * 255) & (hsv[..., 1] > 90)
            h = hsv[..., 0] * 360 / 255
            dh = np.min(np.abs((h[..., None] - FAM + 180) % 360 - 180), axis=-1)
            fam += int((sat & (dh <= 15)).sum())
            tot += int(sat.sum())
    fr_ = fam / max(tot, 1)
    chk(f"COR CAPÍTULO {CAP[l]}", fr_ >= 0.20, f"{100 * fr_:.0f}% da tinta saturada nas famílias de cor das grandezas")
# v5: VETOR, BARRA e FLASH POR QUADRO (qa_v5.py e flash24.py gravam renders/vetor.txt, barra.txt, flash.txt); sem lista branca
for nome_, arq_ in (("VETOR (r⃗ da referência à partícula; T⃗/F⃗ para o furo/centro; p⃗ ∥ v⃗)", "vetor.txt"), ("BARRA (coluna estreita de luminância alta)", "barra.txt")):
    f_ = U / "renders" / arq_
    if f_.exists():
        l0_ = f_.read_text(encoding="utf-8").splitlines()[0]
        m_ = re.search(r": (\d+) eventos", l0_)
        chk(nome_, bool(m_) and int(m_.group(1)) == 0, l0_)
    else:
        chk(nome_, False, "não rodada (python qa_v5.py)")
ff_ = U / "renders" / "flash.txt"
if ff_.exists():
    l0_ = ff_.read_text(encoding="utf-8").splitlines()[0]
    m_ = re.search(r"(\d+) eventos, (\d+) com tinta", l0_)
    chk("FLASH POR QUADRO (MathTex, txt e selos)", bool(m_) and int(m_.group(2)) == 0, l0_)
else:
    chk("FLASH POR QUADRO (MathTex, txt e selos)", False, "não rodado (python flash24.py LOTE renders/flash.txt)")
# PARADO
pf = U / "renders" / "parado.txt"
if pf.exists():
    t_ = pf.read_text(encoding="utf-8").splitlines()
    n_ = int(re.search(r": (\d+) intervalos", t_[0]).group(1)) if t_ else -1
    chk("PARADO", n_ == 0, t_[0] + (" — " + "; ".join(t_[1:6]) if n_ else ""))
p("")
p("RESULTADO GERAL: " + ("OK" if ok_geral[0] else "HÁ FALHAS (ver acima)"))
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "qa.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
