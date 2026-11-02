"""yt_0018 — QA do preview (v7: voz contínua + ATRASO, CONGELAMENTO, VOZ CONTÍNUA, BORDA ABRUPTA, JUNÇÕES; handoff v5 §4 e §6; v4 em _v4/, v3 em _v3/, v2 em _v2/, v1 em _v1/) → renders/qa.txt.
v5: portão G28 v4 + ESQUELETO (G29), 3D × TEXTO (G30), DUPLICATA (G31) e VAZIO (G32: CONTA vazia > 1 s no log; quadro com < 3% de conteúdo > 1 s no preview);
BALANÇA estendida à montagem (G33: mostrador = massa presente em cada quadro); v6: com a VOZ REAL (ElevenLabs v4): gatilhos pelo alinhamento por caractere, pausas de voz, duração medida.
v4: portão G28 v3 + CALHA, TRÂNSITO, RÓTULO SOLTO, MARCADORES COLADOS, FUNDO (≤ 5% dos quadros fora do A1/EN1 com > 40% abaixo de 0,03) e
PALCO 3D da folha; brilho da água por cena e p99 da coluna da lua (renders/v7/agua.json, de agua.py); exposição (renders/v7/p99.json).
v3: a auditoria roda a cada 3 quadros dentro de cada play e no estado final (kit.py); categorias novas no portão G28: ENCOSTADO, SELO DUPLO,
LINHA ÓRFÃ, FORA DA ZONA, CHAMADA CRUZA CORPO, ESPREMIDO, RÉGUA DUPLA, PALCO 3D, FORA DO QUADRO 3D e SEM PALCO (fora do A1/EN1). O portão só
abre com tudo zerado E a prancha humana (24 quadros de maior densidade de texto) gerada. Mais: gatilhos de fala (±0,3 s), percentil 99 da
folha e do gafanhoto (renders/v3/p99.json, de p99.py) e duração por âncora com a narração v2.1.

1. Auditorias do yt_0017 (linhas [audit] dos logs, AUDITORIA=1): TEXTO SOBRE OBJETO, OBJETO FORA DA MARGEM, TEXTO PEQUENO, COR POR TOKEN,
   DEGRADÊ FORA DO ⊕, TEXTO SOBRE TRAJETÓRIA (próximos 2 s), SOBREPOSIÇÃO, TEXTO SOBRE CAIXA, SEM PALCO; PAUSAS (parados.py); FUNDO (quadros do
   preview com > 40% dos pixels abaixo de luminância 0,03, fora do A1/EN1); alinhamento Three.js × Manim (pedidos3d × pontos.json, ≤ 2 px).
2. Novas: GAFANHOTO × FÍSICA (estado 3D do lago contra as fórmulas, projetado, ≤ 2 px; x do ⊕ constante no ar, ≤ 1 px), BALANÇA
   (mostrador × N/g em todo quadro; ⊕ × média ponderada ≤ 1 px; a medida = 4,9 m/s²), REFERENCIAL (cada seta de velocidade × selo ativo),
   CUBO (⊕ do Manim × (5/6; 1/2; 1/6) projetado pelo Three.js, ≤ 2 px), ALINHAMENTO (lago, cubo, foguete), G28 PORTÃO (zero ou justificada).
3. Duração por âncora: narração v2.1 (2,7 palavras/s) × cena.
uso: python qa.py [lotes...]"""
import json
import math
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
LOTES = [a for a in sys.argv[1:]] or ["PH", "PX0", "PX2", "PX3", "PX4", "PX5", "PEP"]
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
PX = 960 / 16                                         # px por unidade do Manim no preview
out = []
p = lambda *a: out.append(" ".join(str(x) for x in a))
CATS = ["TEXTO SOBRE OBJETO", "OBJETO FORA DA MARGEM", "TEXTO PEQUENO", "COR POR TOKEN", "DEGRADÊ FORA DO ⊕", "TEXTO SOBRE TRAJETÓRIA", "SOBREPOSICAO",
        "TEXTO SOBRE CAIXA", "SEM PALCO", "FORA DA MARGEM", "ENCOSTADO", "SELO DUPLO", "LINHA ÓRFÃ", "FORA DA ZONA", "CHAMADA CRUZA CORPO", "ESPREMIDO",
        "RÉGUA DUPLA", "PALCO 3D", "FORA DO QUADRO 3D", "CAIXA SEM LADO ESQUERDO", "CALHA", "TRÂNSITO", "RÓTULO SOLTO", "MARCADORES COLADOS",
        "ESQUELETO", "3D × TEXTO", "DUPLICATA", "VAZIO"]


def isento_palco(l, t, log_):
    """SEM PALCO só é aceito no A1 e no EN1 (logo), v3 §3."""
    anc = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log_)]
    for (a, t0), (_, t1) in zip(anc, anc[1:]):
        if a in ("A1", "EN1") and t0 - 0.05 <= t <= t1 + 0.6:            # o logo e a saída dele
            return True
    return False


def log(l):
    f = U / f"log_{l}.txt"
    return f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""


def log_aud(l):
    """v3: as linhas [audit]/[dens]/[cor] vêm da passada só de auditoria (auditar.sh); sem ela, do log do render."""
    f = U / f"log_aud_{l}.txt"
    return f.read_text(encoding="utf-8", errors="replace") if f.exists() else log(l)


def ov(l):
    f = U / f"qa_overlay_{l}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


# ── 1. auditorias por lote ─────────────────────────────────────────────────────────────────────────────────────
p("=" * 100)
p("1. AUDITORIAS DO yt_0017 (instantes distintos com ocorrência; zero = limpo)")
p("=" * 100)
tot = Counter()
for l in LOTES:
    t = log_aud(l)
    c = Counter()
    exemplos = {}
    for m in re.finditer(r"\[audit\]\s+([0-9.]+)s (.+)", t):
        txt_ = m.group(2)
        cat = next((k for k in CATS if txt_.startswith(k)), txt_[:30])
        if cat == "SEM PALCO" and isento_palco(l, float(m.group(1)), log(l)):
            cat = "SEM PALCO (A1/EN1, isento)"
        c[(cat, m.group(1))] += 1
        exemplos.setdefault(cat, f"{m.group(1)} s: {txt_[:90]}")
    por = Counter(k[0] for k in c)
    tot.update(por)
    ok = "[tempo] total" in t
    p(f"{l:4s} render {'ok' if ok else 'FALTA'} · " + (", ".join(f"{k}: {v}" for k, v in sorted(por.items())) or "nenhuma ocorrência"))
    for k, e in exemplos.items():
        p(f"      ex. {k}: {e}")
    cor = re.search(r"\[cor\] tokens conferidos: (\d+); fora da tabela: (\d+)", t)
    if cor:
        p(f"      COR POR TOKEN: {cor.group(1)} tokens conferidos, {cor.group(2)} fora da tabela")
    ori = re.search(r"\[cor\] origem \(G24 v3\): (\d+) pares conferidos; fora da cor de origem: (\d+)", t)
    if ori:
        p(f"      COR DE ORIGEM (número herda a cor do símbolo): {ori.group(1)} pares conferidos, {ori.group(2)} fora")
    n_aud = len(re.findall(r"\[dens\]", t))
    p(f"      passadas da auditoria (a cada 3 quadros + fim de cada play): {n_aud}")
p("TOTAL:", dict(tot))

# ── 2. auditorias novas ──────────────────────────────────────────────────────────────────────────────────────
p()
p("=" * 100)
p("2. AUDITORIAS NOVAS")
p("=" * 100)
G = 9.8


def fisica(th, tau, rel, v=4.0, m=1.0, M=4.0, L=0.30):
    """Fórmulas da §4, escritas de novo (independentes do lago2.py). Depois do pouso: na folha, os dois param; na água, afunda 1,2 cm e a
    folha segue com V. O pedido guarda θ e τ com 4 casas: no ângulo-limite (pouso exato na ponta) a folga é de 0,1 mm."""
    a = math.radians(th)
    if rel:
        ux = v * math.cos(a)
        vx, V = ux * M / (m + M), -ux * m / (m + M)
    else:
        vx, V = v * math.cos(a), -v * math.cos(a) * m / M
    vy = v * math.sin(a)
    T = 2 * vy / G
    na_folha = (vx - V) * T <= L + 1e-4
    if tau <= 0:
        return 0, 0, 0, T
    if tau <= T:
        return vx * tau, vy * tau - 0.5 * G * tau * tau, V * tau, T
    return vx * T, (0.0 if na_folha else -0.012), V * (T if na_folha else tau), T


p("GAFANHOTO × FÍSICA (hook, X3; lago Three.js): pés e folha do estado 3D × fórmulas, projetados (≤ 2 px); x do ⊕ constante no ar")
sys.path.insert(0, str(U))
from kit import projeta3d  # noqa: E402


def px(q):
    return ((q[0] + 8) / 16 * 960, (4.5 - q[1]) / 9 * 540)


for l in ("PH", "PX3"):
    ped = U / "threejs" / "pedidos3d" / f"{l}.json"
    if not ped.exists():
        p(f"  {l}: sem pedidos")
        continue
    lista = json.loads(ped.read_text(encoding="utf-8"))["cenas"].get("lago", [])
    eg = ef = 0.0
    cms, n = [], 0
    for f, e in lista:
        tau, th, rel = e["fis"]
        cam = e["cam"]
        eg_, ef_ = 1e9, 1e9
        for dt in (0.0, -6e-5, 6e-5):                            # τ com 4 casas: no quadro do pouso vale o lado certo do arredondamento
            xg, yg, xf, T = fisica(th, tau + dt, rel)
            eg_ = min(eg_, math.dist(px(projeta3d(cam, (xg, 0, yg))), px(projeta3d(cam, (e["g"]["x"], 0, e["g"]["z"])))))
            ef_ = min(ef_, math.dist(px(projeta3d(cam, (xf, 0, 0))), px(projeta3d(cam, (e["f"]["x"], 0, 0)))))
        eg, ef = max(eg, eg_), max(ef, ef_)
        T = fisica(th, tau, rel)[3]
        n += 1
        if 0 < tau < T:
            esc = math.dist(px(projeta3d(cam, (0, 0, 0))), px(projeta3d(cam, (1, 0, 0))))       # px por metro neste quadro
            cms.append(((1.0 * e["g"]["x"] + 4.0 * (e["f"]["x"] + 0.15)) / 5.0, esc))
    lin = f"  {l}: {n} quadros · erro máx. gafanhoto {eg:.3f} px, folha {ef:.3f} px"
    var = 0.0
    if cms:
        xs = [c[0] for c in cms]
        var = (max(xs) - min(xs)) * max(c[1] for c in cms)
        lin += f" · ⊕ no ar em {len(cms)} quadros: x = {np.mean(xs):.4f} m, variação {var:.3f} px"
    p(lin + ("  → OK" if eg <= 2 and ef <= 2 and var <= 1 else "  → FALHA"))

p("BALANÇA (X5): mostrador × N/g em todo quadro · ⊕ × média ponderada (≤ 1 px) · a medida nas posições = 4,9 m/s²")
d = ov("PX5").get("balanca", {})
if d:
    import sec_x5 as _b5                                      # geometria do desenho (Manim por metro, alturas, x de cada corpo)
    G_, S_, Y0_, YS_ = 9.8, _b5.S, _b5.Y0, _b5.YS
    a_t = (3 - 1) * G_ / 4
    e_m = e_cm = 0.0
    n_ = nc = nmont = 0
    acs = []
    caso_ja = False
    for f, r in sorted(d.items(), key=lambda kv: int(kv[0])):
        caso_ja = caso_ja or r["caso"] > 0.5                   # do primeiro caso-limite do CONFERE em diante a cena é hipotética (blocos 2 + 2, bloco leve → 0)
        if caso_ja:
            nc += 1
            e_m = max(e_m, 0.0 if r["leitura"] in (6.0, 5.0, 2.0) else 99)   # 5,0 enquanto os blocos ainda viram 2 + 2
            continue
        acm = (3 * (-a_t) + 1 * a_t + 2 * 0) / 6 if r["solto"] > 0.5 else 0.0
        mass_ = r.get("massa", 6.0) if r["solto"] <= 0.5 else 6.0                  # v5 G33: montagem — o mostrador marca a massa que está na balança
        N = mass_ * (G_ + acm)
        e_m = max(e_m, abs(r["leitura"] - round(N / G_, 1)))
        if r["solto"] <= 0.5 and mass_ < 5.99:
            nmont += 1
        n_ += 1
        med_y = (2 * YS_ + 3 * r["y3"] + 1 * r["y1"]) / 6
        med_x = (2 * _b5.XS + 3 * _b5.X3 + 1 * _b5.X1) / 6
        e_cm = max(e_cm, math.hypot(r["cm"][0] - med_x, r["cm"][1] - med_y) * PX)
        if r["solto"] > 0.5 and r["tb"] > 0.2:
            acs.append(2 * (Y0_ - r["y3"]) / S_ / r["tb"] ** 2)
    a_m = float(np.mean(acs)) if acs else float("nan")
    p(f"  {n_} quadros (+ {nc} dos casos-limite; {nmont} da montagem, com o mostrador subindo 0,0 → 2,0 → 6,0 com a massa) · mostrador × N/g: diferença máx. {e_m:.3f} kg · ⊕ × média: {e_cm:.3f} px · "
      f"a medida: {a_m:.4f} m/s² (esperado {a_t:.4f})" + ("  → OK" if e_m < 0.05 and e_cm <= 1 and abs(a_m - a_t) < 0.01 else "  → FALHA"))
else:
    p("  sem registro")

p("REFERENCIAL (G20): cada seta de velocidade × selo ativo no quadro")
for l in LOTES:
    f = U / f"qa_ref_{l}.json"
    if not f.exists():
        continue
    refs = json.loads(f.read_text(encoding="utf-8"))
    if not refs:
        continue
    c = Counter((r[2], r[3]) for r in refs)
    erro = sum(n for (ref, selo), n in c.items() if selo is not None and ref not in selo)
    p(f"  {l}: " + "; ".join(f"seta '{ref}' com selo {('VISTO ' + selo) if selo else '—'}: {n} quadros" for (ref, selo), n in sorted(c.items(), key=str))
      + f"  → {'OK' if erro == 0 else f'{erro} quadros com selo de outro referencial'}")

p("CUBO (X2): ⊕ do Manim × (5/6; 1/2; 1/6) projetado pelo Three.js (pontos.json), ≤ 2 px")
for l, cena, chave in (("PX2", "cubo", "cubo"),):
    pj = U / "threejs" / "q3d" / f"{l}_960x540" / cena / "pontos.json"
    d = ov(l).get(chave, {})
    if pj.exists() and d:
        pts = json.loads(pj.read_text(encoding="utf-8"))
        e = []
        for f, r in d.items():
            if f in pts and pts[f]:
                q = pts[f]["cm"]
                m = ((r["cm"][0] + 8) / 16 * 960, (4.5 - r["cm"][1]) / 9 * 540)
                e.append(math.hypot(q[0] - m[0], q[1] - m[1]))
                for a, b in zip(r["meios"], pts[f]["meios"]):
                    e.append(math.hypot(b[0] - (a[0] + 8) / 16 * 960, b[1] - (4.5 - a[1]) / 9 * 540))
        p(f"  {len(e)} pontos (⊕ e meios das arestas): erro máx. {max(e):.3f} px, médio {np.mean(e):.3f} px" + ("  → OK" if max(e) <= 2 else "  → FALHA"))
    else:
        p("  sem pontos.json/registro")

# ── alinhamento 3D × Manim: a câmera do projeta3d contra o b3d.js ───────────────────────────────────────────────
p()
p("ALINHAMENTO Three.js × Manim (pedidos3d → projeta3d em Python × pontos.json do Three.js, ≤ 2 px)")
for l, cena, fn in (("PX2", "cubo", lambda e: [((5 / 6, 1 / 2, 1 / 6), "cm")]),
                    ("PH", "lago", lambda e: [((e["g"]["x"], 0, e["g"]["z"]), "pe"), ((e["f"]["x"], 0, 0), "folha"), ((e["f"]["x"] + 0.30, 0, 0), "ponta")]),
                    ("PX3", "lago", lambda e: [((e["g"]["x"], 0, e["g"]["z"]), "pe"), ((e["f"]["x"], 0, 0), "folha"), ((e["f"]["x"] + 0.30, 0, 0), "ponta")]),
                    ("PEP", "fog", lambda e: [((e["fg"]["x"], 0, e["fg"]["z"]), "cm_corpo")]),
                    ("PH", "gra", lambda e: [])):
    ped = U / "threejs" / "pedidos3d" / f"{l}.json"
    pj = U / "threejs" / "q3d" / f"{l}_960x540" / cena / "pontos.json"
    if not (ped.exists() and pj.exists()):
        p(f"  {l}/{cena}: sem pedidos/pontos")
        continue
    pts = json.loads(pj.read_text(encoding="utf-8"))
    lista = json.loads(ped.read_text(encoding="utf-8"))["cenas"].get(cena, [])
    e_ = []
    for f, est in lista:
        q = pts.get(str(f))
        if not q:
            continue
        for p3, chave in fn(est):
            alvo = q.get(chave) if isinstance(chave, str) else q[chave[0]][chave[1]]
            if alvo is None:
                continue
            m = px(projeta3d(est["cam"], p3))
            e_.append(math.hypot(m[0] - alvo[0], m[1] - alvo[1]))
    if e_:
        p(f"  {l}/{cena}: {len(e_)} pontos, erro máx. {max(e_):.3f} px, médio {np.mean(e_):.3f} px" + ("  → OK" if max(e_) <= 2 else "  → FALHA"))
    else:
        p(f"  {l}/{cena}: {len(lista)} quadros 3D (granada do yt_0017 sem pontos do ⊕ por quadro: alinhamento herdado do yt_0017)")

# ── FUNDO (v4 §3.3, entra no portão): quadros do preview com > 40% dos pixels abaixo de 0,03, fora do A1/EN1 ──
prev = sorted((U / "renders").glob("preview_yt0018_*_960x540.mp4"), key=lambda f: f.stat().st_mtime)
fundo_ok, fundo_txt = False, "FUNDO: sem preview"
if prev:
    import av
    c = av.open(str(prev[-1]))
    ruins, n = [], 0
    from PIL import Image as _Im
    bgs = [np.asarray(_Im.open(U / nm_).convert("RGB").resize((240, 135)), float) / 255 for nm_ in ("fundo_lab.png", "fundo_lab_ex.png") if (U / nm_).exists()]
    cont = []
    excl = json.loads((U / "renders" / "excluir_fundo.json").read_text()) if (U / "renders" / "excluir_fundo.json").exists() else []
    for i, fr in enumerate(c.decode(video=0)):
        if i % 3:
            continue
        t_ = i / 15
        if any(x0 <= t_ <= x1 for x0, x1 in excl):
            continue
        a = np.asarray(fr.to_image().resize((240, 135)), float) / 255
        Y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
        n += 1
        if (Y < 0.03).mean() > 0.40:
            ruins.append(round(t_, 1))
        if bgs:
            dif_ = min(float((np.abs(a - b_).max(axis=2)[18:, :] > 0.10).mean()) for b_ in bgs)         # sem a faixa do cabeçalho
            cont.append((t_, dif_))
    c.close()
    # VAZIO (G32): quadro com < 3% de conteúdo por mais de 1,0 s (A1–A4 e EN1–EN2 isentos)
    vz_ex = []
    for l_, ids_ in (("PH", ("A1", "A2", "A3", "A4")), ("PEP", ("EN1", "EN2"))):
        s_ = log(l_)
        ini_ = sum(int(re.search(r"\[tempo\] total [0-9.]+ s \((\d+) quadros\)", log(x)).group(1)) for x in LOTES[:LOTES.index(l_)] if log(x)) / 15 if l_ in LOTES else 0
        anc_ = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", s_)]
        for (a_, t0_), (b_, t1_) in zip(anc_, anc_[1:]):
            if a_ in ids_:
                vz_ex.append((ini_ + t0_ - 0.2, ini_ + t1_ + 0.2))
    vz, run_ = [], []
    for t_, f_ in cont + [(1e9, 1.0)]:
        if f_ < 0.03 and not any(x0 <= t_ <= x1 for x0, x1 in vz_ex):
            run_.append(t_)
        else:
            if run_ and run_[-1] - run_[0] + 0.2 > 1.0:
                vz.append((round(run_[0], 1), round(run_[-1] + 0.2, 1)))
            run_ = []
    tot["VAZIO"] += len(vz)
    vazio_txt = f"VAZIO (quadro com < 3% de conteúdo por > 1,0 s; A1–A4 e EN1–EN2 isentos): {len(vz)} trecho(s)" + (f" {vz[:8]}" if vz else "") + ("  → OK" if not vz else "  → FALHA")
    fr_ = len(ruins) / max(n, 1)
    fundo_ok = fr_ <= 0.05
    fundo_txt = (f"FUNDO ({prev[-1].name}): {n} quadros amostrados (1 a cada 3, fora do A1/EN1), com > 40% abaixo de 0,03: {len(ruins)} "
                 f"({100 * fr_:.1f}%; limite 5%) {ruins[:10]}" + ("  → OK" if fundo_ok else "  → FALHA"))

# ── G28: o portão da entrega ─────────────────────────────────────────────────────────────────────────────────────
p()
GATE = ["SOBREPOSICAO", "TEXTO SOBRE OBJETO", "TEXTO SOBRE CAIXA", "FORA DA MARGEM", "OBJETO FORA DA MARGEM", "ENCOSTADO", "SELO DUPLO", "LINHA ÓRFÃ",
        "FORA DA ZONA", "CHAMADA CRUZA CORPO", "ESPREMIDO", "RÉGUA DUPLA", "PALCO 3D", "FORA DO QUADRO 3D", "SEM PALCO", "TEXTO SOBRE TRAJETÓRIA",
        "CAIXA SEM LADO ESQUERDO", "CALHA", "TRÂNSITO", "RÓTULO SOLTO", "MARCADORES COLADOS", "ESQUELETO", "3D × TEXTO", "DUPLICATA", "VAZIO"]
jf = U / "renders" / "justificativas.json"
just = json.loads(jf.read_text(encoding="utf-8")) if jf.exists() else []
prancha_h = U / "renders" / "v7" / "prancha_humana_24.png"
p("G28 v5 PORTÃO (auditoria zerada E prancha humana anexada): " + ", ".join(f"{k}: {tot.get(k, 0)}" for k in GATE) + f" · justificativas escritas: {len(just)}")
for j in just:
    p(f"  JUSTIFICADA {j['lote']} {j['t']} s {j['cat']}: {j['porque']}")
p(f"  prancha humana (24 quadros de maior densidade de texto): {'renders/v7/prancha_humana_24.png' if prancha_h.exists() else 'FALTA'}")
p("  " + fundo_txt)
p("  → PORTÃO " + ("ABERTO" if sum(tot.get(k, 0) for k in GATE) <= len(just) and prancha_h.exists() and fundo_ok else "FECHADO (não entregar)"))

# ── 3. duração por âncora ───────────────────────────────────────────────────────────────────────────────────
p()
p("=" * 100)
p("3. DURAÇÃO POR ÂNCORA (voz real × janela da cena)")
p("=" * 100)
tn = tc = 0.0
for l in LOTES:
    t = log(l)
    anc = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", t)]
    for (a, t0), (_, t1) in zip(anc, anc[1:]):
        nar = ANC[a]["dur"]
        cena = t1 - t0
        tn += nar
        tc += cena
        p(f"  {l:4s} {a:6s} narração {nar:6.2f} s · cena {cena:6.2f} s · {'+' if cena - nar >= 0 else ''}{cena - nar:5.2f} s")
p(f"  TOTAL narração {tn / 60:.2f} min · cena {tc / 60:.2f} min")

# ── 4. ATRASO (v7): instante da imagem − início da palavra, de -0,15 s a +0,20 s ──
p()
p("=" * 100)
p("4. ATRASO DOS GATILHOS (instante da imagem − início da palavra no alinhamento da voz contínua; tolerância -0,15 s … +0,20 s)")
p("=" * 100)
fora_g = n_g = 0
atrasos = []
for l in LOTES:
    for m in re.finditer(r"\[gatilho\] (\S+) ([0-9.]+) (.+)", log(l)):
        aid, te, frase = m.group(1), float(m.group(2)), m.group(3).strip()
        fala = ANC.get(aid, {}).get("fala", "").split()
        alvo = re.findall(r"\w+", frase.lower())
        k = next((i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo), None)
        if k is None:
            p(f"  {l:4s} {aid:6s} '{frase}': frase não está na fala (gatilho só de tela)")
            continue
        tp = ANC[aid]["t"][k]
        n_g += 1
        d_ = te - tp
        atrasos.append(d_)
        ok_ = -0.15 - 1e-6 <= d_ <= 0.20 + 1e-6
        fora_g += not ok_
        p(f"  {l:4s} {aid:6s} '{frase}': palavra {tp:6.2f} s · imagem {te:6.2f} s · {d_:+.2f} s" + ("" if ok_ else "  ← FORA"))
for l in LOTES:
    for m in re.finditer(r"\[abertura\] (\S+) atrasada ([-+0-9.]+) s", log(l)):
        p(f"  {l:4s} {m.group(1):6s} a âncora abriu {m.group(2)} s depois da voz")
if atrasos:
    a_ = np.array(atrasos)
    p(f"  TOTAL: {n_g} gatilhos, {fora_g} fora de [-0,15; +0,20] s · maior atraso {a_.max():+.2f} s · maior adiantamento {a_.min():+.2f} s · média {a_.mean():+.3f} s")
else:
    p("  sem gatilhos")
tot["ATRASO"] = fora_g

# ── 5. EXPOSIÇÃO (v3 §5): percentil 99 dos pixels da folha e do gafanhoto (< 235) ──
p()
jp = U / "renders" / "v7" / "p99.json"
if jp.exists():
    d99 = json.loads(jp.read_text(encoding="utf-8"))
    p("EXPOSIÇÃO (percentil 99 do canal mais claro, pixels da máscara; meta < 235): " +
      "; ".join(f"{k}: folha {v['folha']:.0f}, gafanhoto {v['gaf']:.0f}" for k, v in d99.items()) +
      ("  → OK" if all(v["folha"] < 235 and v["gaf"] < 235 for v in d99.values()) else "  → FALHA"))
else:
    p("EXPOSIÇÃO: sem renders/v3/p99.json (rodar p99.py)")

# ── ÁGUA e LUA (v4 §4): brilho da metade de baixo por cena (≥ 0,09; ≤ 5% abaixo de 0,03) e p99 da coluna da lua no hook (< 235) ──
ja = U / "renders" / "v7" / "agua.json"
if ja.exists():
    da = json.loads(ja.read_text(encoding="utf-8"))
    p()
    p("ÁGUA (metade de baixo dos quadros do lago, por âncora; meta: média ≥ 0,09 e ≤ 5% dos pixels abaixo de 0,03):")
    ok_a = True
    for k, v in da["agua"].items():
        b_ = v["media_baixo"] >= 0.09 and v["frac_escuro"] <= 0.05
        ok_a &= b_
        p(f"  {k:10s} {v['quadros']:4d} quadros · média {v['media_baixo']:.3f} (mín. {v['min_media']:.3f}) · abaixo de 0,03: {100 * v['frac_escuro']:.1f}% "
          f"(máx. {100 * v['max_frac']:.1f}%)" + ("" if b_ else "  ← FORA"))
    p("  → " + ("OK" if ok_a else "FALHA"))
    lu = da.get("lua", {})
    if lu:
        p(f"LUA (hook, 0–20 s): p99 da faixa mais clara da água = {lu['p99_max']:.0f} (t = {lu['t_pior']} s; RGB médio da faixa {lu['rgb_medio_faixa_pior']})"
          + ("  → OK" if lu["p99_max"] < 235 else "  → FALHA"))
else:
    p("ÁGUA/LUA: sem renders/v7/agua.json (rodar agua.py)")

# ── PAUSAS ──────────────────────────────────────────────────────────────────────────────────────────────────
p()
r = subprocess.run([sys.executable, str(U / "parados.py"), *LOTES], capture_output=True, text=True, encoding="utf-8", cwd=U, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
p("PAUSAS (trechos ≥ 4 s sem pixel novo):")
for l_ in r.stdout.strip().splitlines():
    p("  " + l_)
p(fundo_txt)
p(vazio_txt if prev else "VAZIO: sem preview")
# ── VOZ (v7): auditorias do WAV contínuo ──
p()
p("VOZ CONTÍNUA / BORDA ABRUPTA / JUNÇÕES (auditoria_voz.py no audio/narracao_v7.wav):")
rv = subprocess.run([sys.executable, str(U / "auditoria_voz.py")], capture_output=True, text=True, encoding="utf-8", cwd=U, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
for l_ in rv.stdout.strip().splitlines():
    p("  " + l_)
voz_ok = "VOZ CONTÍNUA: 0 " in rv.stdout and "BORDA ABRUPTA: 0 " in rv.stdout
p("  → " + ("OK" if voz_ok else "FALHA"))
# ── CONGELAMENTO (v7) ──
p()
rc = subprocess.run([sys.executable, str(U / "congelamento.py")], capture_output=True, text=True, encoding="utf-8", cwd=U, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
p("CONGELAMENTO (freezedetect n = 0,0005, d = 1,5 s com fala ativa; no 3D, diferença só nos objetos):")
for l_ in rc.stdout.strip().splitlines():
    p("  " + l_)
(U / "renders" / "qa.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
