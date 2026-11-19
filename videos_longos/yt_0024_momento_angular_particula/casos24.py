"""yt_0024 v2: tabela dos 31 casos do handoff v2 §4 (+ os quadros vazios) com o quadro de ANTES (preview v1) e o de DEPOIS (lote v2) no
MESMO ponto da narração: o tempo local do caso no v1 vira (âncora, fração dentro da âncora) pelas âncoras do v1 (renders/quadros_v1.json) e
volta a tempo local do v2 pelas linhas [ancora] do log_<L>.txt.  uso: python casos24.py → renders/casos/caso_NN.png e renders/casos_31.txt"""
import json
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
OUT = U / "renders" / "casos"
OUT.mkdir(parents=True, exist_ok=True)
Q1 = json.loads((U / "renders" / "quadros_v1.json").read_text(encoding="utf-8"))
INI = {"PH": "H1", "PB1": "B1-1", "PB2": "B2-1", "PB3": "B3-1", "PB4": "B4-1", "PB5": "B5-1", "PB6": "B6-1", "PS": "S1"}
CASOS = [
    (1, "PH", 6.8, "FURO com chamada cruzando o tampo e a órbita", "anel do furo acende; rótulo logo acima, linha curta dentro da órbita"),
    (2, "PH", 10.3, "PUXADOR com chamada cruzando a travessa", "base nova sem travessa no centro; rótulo embaixo do T, linha curta vertical"),
    (3, "PH", 44.6, "título e NESTE VÍDEO sobre o reflexo estourado", "estouro eliminado; mesa recua (op 0,38 + desfoque); ícones ≥ 120 px"),
    (4, "PB1", 39.5, "O e o anel do ponto dentro do reflexo branco", "mesa v2 sem estouro (ESTOURO ≤ 0,55)"),
    (5, "PB1", 65.9, "ícone da mão rabiscado", "sai a mão; arco de varredura r→p no tampo e L⃗ crescendo, ⟲ no pé"),
    (6, "PB1", 85.7, "r⊥ no reflexo; φ encostado na tracejada", "sem estouro; φ afastado do prolongamento"),
    (7, "PB2", 19.8, "rótulo O₁ debaixo do disco", "rótulos dos pinos do lado oposto à reta"),
    (8, "PB2", 26.4, "r⃗ cruza o rótulo d = 0,40 m", "d no HUD; cota em x = 0,80 m, fora da área varrida"),
    (9, "PB2", 33.1, "rótulo r⃗ encostado no p⃗", "rótulo de r⃗ a 42 % do vetor, do lado oposto à reta"),
    (10, "PB2", 66.1, "⊙ L_z = +0,1… cortado na borda", "⊙ em cima do pino O₃; L_z ao lado por rotulo() dentro da coluna"),
    (11, "PB2", 79.3, "r⃗ e d sobre os triângulos", "d no HUD; r⃗ some quando os triângulos entram"),
    (12, "PB2", 59.5, "⊗ solto embaixo do O₂", "⊗ em cima do furo, anel do furo acende"),
    (13, "PB2", 40.0, "selo CÂMERA LENTA parado durante as contas", "nas contas o disco para e o selo sai"),
    (14, "PB3", 18.5, "cartão F = dp/dt órfão", "F⃗ = dp⃗/dt entra na CONTA quando citado"),
    (15, "PB3", 43.2, "HIPÓTESES em caixa de 4 linhas", "três chips numa linha"),
    (16, "PB3", 80.3, "= d(−mgt) 0 com o 0 solto", "linha escrita da esquerda para a direita"),
    (17, "PB3", 90.0, "m = 0,50 kg atravessado pelo eixo L_z", "gráfico em caixa própria; m, d, g no HUD"),
    (18, "PB3", 98.8, "0,40 órfão; m duplicado; g sobre a seta mg", "voos do HUD com origem e destino; g no HUD"),
    (19, "PB4", 35.1, "I rosa sobre a seta v⃗", "I nasce no anel do disco, por fora da órbita"),
    (20, "PB4", 46.8, "T⃗ sobre R", "rótulos de T⃗ e R em lados opostos do raio"),
    (21, "PB4", 58.5, "mostradores sobre r⃗, disco e v⃗", "HUD à direita da mesa"),
    (22, "PB4", 64.3, "rótulo v⃗ cortado na margem", "v⃗ a 0,14 m por m/s cabe na mesa (C_TOPO K 3,6)"),
    (23, "PB5", 7.2, "F⃗ e r⃗ colados na partícula", "rótulos em lados opostos da reta O–partícula; F⃗ mais curta"),
    (24, "PB5", 50.4, "L = 0 sobre a borda do plano", "rótulo fora do plano"),
    (25, "PB5", 86.4, "Δp⃗ sobre a aresta; OBc e OBC na mesma cor", "pulso paralelo à aresta, por fora; tons 40/25/40 %"),
    (26, "PB6", 58.6, "LEI GERAL em cima da equação", "rótulo acima da linha τ⃗ = dL⃗/dt, alinhado à esquerda"),
    (27, "PB6", 58.6, "estado intermediário do GM visível", "GM numa chamada da linha inteira; auditoria GM PARCIAL"),
    (28, "PB6", 140.6, "inset vazio", "inset entra com disco, v⃗ e direção do furo"),
    (29, "PB6", 152.3, "texto atrás dos mostradores; v⃗ e v_θ colados; v_r sem seta", "v_r desenhada, rótulos separados, MESMO SENTIDO ⇒ W > 0"),
    (30, "PB6", 83.0, "5 caixas de mostrador na CONTA", "HUD (máx. 3) à direita da mesa"),
    (31, "PS", 36.1, "nuvem de alfinetes", "Three.js 'nuvem' (~400 partículas) com 6 r⃗ × p⃗ que somam L⃗"),
    (32, "PB3", 0.0, "abertura de bloco com quadro vazio", "painel e esfera já na tela; varredura de luz"),
    (33, "PB4", 0.0, "abertura de bloco com quadro vazio", "mesa já em movimento; varredura de luz"),
    (34, "PB5", 0.0, "abertura de bloco com quadro vazio", "órbita já em movimento; varredura de luz"),
    (35, "PB6", 0.0, "abertura de bloco com quadro vazio", "mesa já em movimento; varredura de luz"),
    (36, "PB2", 111.8, "mesa vazia no fim do bloco", "triângulos e CONTA ficam até o corte"),
]


def ancoras_v2(l):
    s = (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace")
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", s)]
    tt = re.search(r"\[tempo\] total ([0-9.]+)", s)
    return an, float(tt.group(1)) if tt else an[-1][1] + 10


ordem = sorted(Q1.items(), key=lambda kv: kv[1])


def mapeia(l, t1):
    f = Q1[INI[l]] + round(t1 * 15)                      # quadro global no v1
    k = max(i for i, (_, q) in enumerate(ordem) if q <= f)
    a, q0 = ordem[k]
    q1 = ordem[k + 1][1] if k + 1 < len(ordem) else q0 + 150
    fr = (f - q0) / max(1, q1 - q0)
    an, fim = ancoras_v2(l)
    for j, (x, t0) in enumerate(an):
        if x == a:
            tb = an[j + 1][1] if j + 1 < len(an) else fim
            return f, a, fr, t0 + fr * (tb - t0)
    return f, a, fr, None


def quadro(mp4, n):
    with av.open(str(mp4)) as c:
        for i, fr in enumerate(c.decode(video=0)):
            if i == n:
                return fr.to_image()
    return None


lin = ["yt_0024 v2 — os 31 casos do handoff v2 §4 (+ quadros vazios): antes (preview v1) × depois (lote v2) no mesmo ponto da narração", ""]
pedidos = {}
for n, l, t1, defeito, corr in CASOS:
    f1, a, fr, t2 = mapeia(l, t1)
    pedidos.setdefault("v1", []).append((f1, n))
    if t2 is not None:
        pedidos.setdefault(l, []).append((int(round(t2 * 15)), n))
    lin.append(f"{n:2d} · {l} {t1:6.1f} s (v1) → âncora {a} ({100 * fr:.0f}%) → {t2 if t2 is None else round(t2, 1)} s (v2) · {defeito} → {corr}")
antes, depois = {}, {}
alvo = {f: n for f, n in pedidos.pop("v1")}
with av.open(str(U / "renders" / "preview_yt0024_v1_960x540.mp4")) as c:
    falta = set(alvo)
    for i, fr in enumerate(c.decode(video=0)):
        if i in falta:
            for f_, n_ in [(f_, n_) for f_, n_ in pedidos.get("_", [])]:
                pass
            for n_ in [n_ for f_, n_ in [(f, alvo[f]) for f in [i]]]:
                antes[n_] = fr.to_image()
            falta.discard(i)
        if not falta:
            break
# casos com o mesmo quadro de antes (26/27): repete
for n, l, t1, *_ in CASOS:
    if n not in antes:
        f1 = mapeia(l, t1)[0]
        for m_, l_, t_, *_r in CASOS:
            if m_ in antes and mapeia(l_, t_)[0] == f1:
                antes[n] = antes[m_]
for l, lst in pedidos.items():
    mp4 = U / f"media_{l}/videos/cena/540p15/{l}.mp4"
    if not mp4.exists():
        continue
    want = {}
    for f, n in lst:
        want.setdefault(f, []).append(n)
    with av.open(str(mp4)) as c:
        ult = None
        for i, fr in enumerate(c.decode(video=0)):
            ult = fr
            if i in want:
                for n in want[i]:
                    depois[n] = fr.to_image()
        for f, ns in want.items():
            for n in ns:
                if n not in depois and ult is not None:
                    depois[n] = ult.to_image()
for n, l, t1, defeito, corr in CASOS:
    P = Image.new("RGB", (1920, 580), (8, 12, 24))
    if n in antes:
        P.paste(antes[n], (0, 40))
    if n in depois:
        P.paste(depois[n], (960, 40))
    d = ImageDraw.Draw(P)
    d.text((10, 8), f"CASO {n} · {l} · ANTES (v1): {defeito}", fill=(255, 170, 120))
    d.text((970, 8), f"DEPOIS (v2): {corr}", fill=(140, 240, 170))
    P.save(OUT / f"caso_{n:02d}.png")
(U / "renders" / "casos_31.txt").write_text("\n".join(lin) + "\n", encoding="utf-8")
print("\n".join(lin))
