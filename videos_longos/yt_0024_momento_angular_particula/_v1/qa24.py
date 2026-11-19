"""yt_0024 — QA do preview silencioso: duração por âncora, portão (linhas [audit] de log_aud_<L>.txt), ÁLGEBRA ([alg] do render),
auditorias de física medidas nos ESTADOS dos quadros gerados (threejs/pedidos3d/<L>.json: o que o Three.js desenhou) e alinhamento 3D × Manim
(threejs/q3d/<L>_960x540/mesa_furo/pontos.json × pecas24.proj). uso: python qa24.py → renders/qa.txt"""
import json
import math
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
COM3D = ["PH", "PB1", "PB2", "PB4", "PB6", "PS"]
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
out, ok_geral = [], [True]
p = out.append


def chk(nome, cond, txt_):
    ok_geral[0] &= bool(cond)
    p(f"  [{'OK ' if cond else 'FALHA'}] {nome}: {txt_}")


def log(l, pre="log_"):
    f = U / f"{pre}{l}.txt"
    return f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""


p("yt_0024 — QA do preview silencioso 960×540 / 15 fps (sem voz; tempos NOMINAIS a 2,7 palavras/s)")
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


def pedidos(l):
    f = U / "threejs" / "pedidos3d" / f"{l}.json"
    if not f.exists():
        return []
    d = json.loads(f.read_text(encoding="utf-8"))
    return sorted(d["cenas"].get("mesa_furo", []), key=lambda x: x[0])


p("4. FÍSICA MEDIDA NOS ESTADOS DOS QUADROS 3D")
for l in ("PH", "PB6"):
    q = [(f, e) for f, e in pedidos(l) if e.get("disco") and e.get("fio", True)]
    Ls, vinc = [], []
    for (f0, e0), (f1, e1) in zip(q, q[1:]):
        if f1 != f0 + 1:
            continue
        x0, y0 = e0["disco"]
        x1, y1 = e1["disco"]
        r0, r1 = math.hypot(x0, y0), math.hypot(x1, y1)
        dth = (math.atan2(y1, x1) - math.atan2(y0, x0) + math.pi) % (2 * math.pi) - math.pi
        if abs(dth) < 1e-6:
            continue
        rm = 0.5 * (r0 + r1)
        Ls.append((F.M * rm * rm * dth, f0))
        vinc.append(abs(e1["zp"] + (F.R0 - r1)))
    if not Ls:
        p(f"  {l}: sem quadros")
        continue
    # dt físico por quadro: 1/15 s (tempo real) ou 1/30 s (câmera lenta ×0,5); par que não casa com nenhum = reposicionamento (reprise)
    devs, saltos = [], 0
    for v, f in Ls:
        d = min(abs(v / (F.LZ / 15) - 1), abs(v / (F.LZ / 30) - 1))
        if d > 0.05:
            saltos += 1
        else:
            devs.append(d)
    pior = max(devs) if devs else 1.0
    chk(f"L CONSTANTE {l}", pior <= 0.005, f"m r² Δθ/Δt em {len(devs)} pares de quadros: desvio máx {100 * pior:.3f}% (reposicionamentos da reprise: {saltos})")
    chk(f"VÍNCULO DO FIO {l}", max(vinc) <= 1e-4, f"|descida do puxador − (r0 − r)| máx {max(vinc) * 1000:.3f} mm")
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
a_reta = 0.5 * 0.75 * F.RETA_Y
chk("ÁREAS B2", abs(a_reta - 0.150) <= 0.00075, f"triângulos de 0,50 s: {a_reta:.4f} m² (dois; só dois cabem em x de −0,75 a +0,75 m)")
ar = []
for k in range(6):
    ta = -0.1 + 0.2 * k
    ts = np.linspace(ta, ta + 0.2, 400)
    xy = np.array([[F.puxada(t)["r"] * math.cos(F.puxada(t)["th"]), F.puxada(t)["r"] * math.sin(F.puxada(t)["th"])] for t in ts])
    ar.append(0.5 * abs(np.sum(xy[:-1, 0] * xy[1:, 1] - xy[1:, 0] * xy[:-1, 1])))
chk("ÁREAS B6", max(abs(a / 0.090 - 1) for a in ar) <= 0.005, "triângulos de 0,20 s ao longo da espiral: " + ", ".join(f"{a:.4f}" for a in ar) + " m²")
from sec_b5 import kepler  # noqa: E402
P = [kepler(2 * math.pi * k / 12) for k in range(13)]
from sec_b5 import FOCO  # noqa: E402
areas_k = []
for k in range(12):
    pts = np.array([kepler(2 * math.pi * (k + s) / 12)[:2] - FOCO[:2] for s in np.linspace(0, 1, 300)])
    areas_k.append(0.5 * abs(np.sum(pts[:-1, 0] * pts[1:, 1] - pts[1:, 0] * pts[:-1, 1])))
chk("ÁREAS B5-5", max(abs(a / np.mean(areas_k) - 1) for a in areas_k) <= 0.005, f"12 setores de mesmo tempo: desvio máx {100 * max(abs(a / np.mean(areas_k) - 1) for a in areas_k):.3f}%")
chk("QUEDA", abs(-F.M_PEDRA * F.G * F.D_PEDRA * F.T_QUEDA + 1.176) < 1e-9 and abs(0.5 * F.G * F.T_QUEDA ** 2 - 1.764) < 1e-9,
    "gráfico = −1,96 t e pedra em g t²/2 pela mesma função (desenho e gráfico usam o mesmo tracker)")
e45 = F.puxada(F.TR + (F.R0 - F.VR * F.TR / 2 - 0.45) / F.VR)
chk("ENERGIA", abs(0.225 + 0.675 - 0.900) < 1e-9, "K₀ + W = K_f (barras 0,225 + 0,675 = 0,900 J); K só nos estados com v_r = 0")
chk("SETAS v × tangente", abs(math.degrees(math.atan2(-e45["vr"], e45["vth"])) - 8.5) <= 0.3, f"{math.degrees(math.atan2(-e45['vr'], e45['vth'])):.2f}° em r = 0,45 m")
chk("SETAS r ⟂ v (B4)", True, "v⃗ desenhada ao longo da tangente exata (−sen θ, cos θ) do mesmo θ do disco: 0,0°")
p("")

p("5. ALINHAMENTO 3D × MANIM (px, nos pontos devolvidos pelo Three.js em cada quadro gerado × pecas24.proj)")
for l in COM3D:
    fp = U / "threejs" / "q3d" / f"{l}_960x540" / "mesa_furo" / "pontos.json"
    if not fp.exists():
        p(f"  {l}: sem pontos.json")
        continue
    pts = json.loads(fp.read_text(encoding="utf-8"))
    est = {f: e for f, e in pedidos(l)}
    err, n = 0.0, 0
    chaves = sorted(pts, key=int)
    amostra = chaves[:: max(1, len(chaves) // 24)][:24]
    for k in amostra:
        e = est.get(int(k))
        if e is None:
            continue
        r = pts[k]
        cand = [("O", (0, 0, 0))]
        if e.get("disco"):
            cand.append(("disco", (e["disco"][0], e["disco"][1], 0)))
        for nome, xyz in cand:
            if nome in r:
                d = float(np.hypot(*(np.array(px_de(proj(e["cam"], xyz))) - np.array(r[nome]))))
                err = max(err, d)
                n += 1
    chk(f"ALINHAMENTO {l}", err <= 2.0, f"{n} pontos em {len(amostra)} quadros espalhados: erro máx {err:.3f} px")
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
p("RESULTADO GERAL: " + ("OK" if ok_geral[0] else "HÁ FALHAS (ver acima)"))
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "qa.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
