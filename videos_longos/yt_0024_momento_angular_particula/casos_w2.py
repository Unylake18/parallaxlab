"""yt_0024 v3 §3: tabela dos 17 casos de sobreposição com o quadro de ANTES (preview v2) e o de DEPOIS (lote v3) no MESMO ponto da narração
(âncora + fração dentro dela). Tempos do handoff v3 = tempo global do preview v2. uso: python casos_w2.py → renders/casos_w2/caso_NN.png e renders/casos_w2.txt"""
import json
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
OUT = U / "renders" / "casos_w2"
OUT.mkdir(parents=True, exist_ok=True)
Q2 = json.loads((U / "renders" / "quadros_v2.json").read_text(encoding="utf-8"))
ordem = sorted(Q2.items(), key=lambda kv: kv[1])
LOTE = lambda a: "PH" if a[0] in "HA" else ("PS" if a[0] in "SE" else "PB" + a[1])
CASOS = [
    (1, 190, "O₃ encostado na borda de cima da mesa", "rótulo O₃ dentro da mesa, ao lado do pino"),
    (2, 254, "números 0,075 dos 4 triângulos se encostando", "cada número dentro do seu triângulo, um por vez (acende e some em 1 s)"),
    (3, 256, "0,375 m em cima da reta da trajetória", "cota acima da reta, longe de O₃ e dos números"),
    (4, 226, "L_z = ∓0,12 encostando no pino e na borda", "rótulos de L_z ao lado do pino, dentro da mesa"),
    (5, 380, "−0,59 cruzado pela reta; −1,96 N m sobre o cateto", "gráfico menor; rótulos fora da reta e do eixo"),
    (6, 378, "mostrador m sobre a base do eixo L_z", "HUD abaixo do gráfico (slot −3,6)"),
    (7, 408, "R voando por cima de mvR", "voo por fora da coluna (arco pela direita)"),
    (8, 424, "rótulo I encostado no disco e no v⃗", "I atrás do disco, do lado de dentro, longe de R e v⃗"),
    (9, 444, "BRAÇO ZERO sobre T⃗ e o raio", "BRAÇO ZERO fixo abaixo da mesa"),
    (10, 496, "periélio: O, F⃗, r⃗ e o planeta empilhados", "setas curtas e rótulos para fora da órbita"),
    (11, 500, "seta F⃗ solta no meio da tela", "voo parte do rótulo F⃗/r⃗ (não da seta)"),
    (12, 582, "Δp⃗ sobre B e a seta; C cortado pela tracejada", "Δp⃗ ao lado do pulso; C′ e C fora da reta"),
    (13, 756, "inset: v⃗, v_θ, 0,30 m/s, T⃗, 0° sobrepostos", "legenda à direita do inset; arco e 0° colados"),
    (14, 734, "triângulos de 0,20 s sobrepostos", "no máximo 3 visíveis, tons alternados"),
    (15, 804, "eixo T encostado na equação", "gráfico 0,35 u mais baixo e menor"),
    (16, 848, "r⃗ × p⃗ solto no alto", "rótulo preso à ponta da 1ª setinha"),
    (17, 824, "S1: mesa cortada pela borda", "câmera K 3,0: borda do LED inteira no quadro"),
]


def ancoras(l):
    s = (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace")
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", s)]
    return an


def quadro(mp4, n):
    with av.open(str(mp4)) as c:
        ult = None
        for i, fr in enumerate(c.decode(video=0)):
            ult = fr
            if i == n:
                return fr.to_image()
        return ult.to_image()


lin = ["yt_0024 v3 — casos do handoff v3 §3: antes (preview v2) × depois (lote v3) no mesmo ponto da narração", ""]
for n, tg, defeito, corr in CASOS:
    f = tg * 15
    k = max(i for i, (_, q) in enumerate(ordem) if q <= f)
    a, q0 = ordem[k]
    q1 = ordem[k + 1][1] if k + 1 < len(ordem) else q0 + 150
    fr = (f - q0) / max(1, q1 - q0)
    l = LOTE(a)
    an = ancoras(l)
    tt = re.search(r"\[tempo\] total ([0-9.]+)", (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace"))
    fim = float(tt.group(1)) if tt else an[-1][1]
    t3 = None
    for j, (x, t0) in enumerate(an):
        if x == a:
            tb = an[j + 1][1] if j + 1 < len(an) else fim
            t3 = t0 + fr * (tb - t0)
    ant = quadro(U / "renders" / "preview_yt0024_v2_960x540.mp4", int(f))
    dep = quadro(U / f"media_{l}/videos/cena/540p15/{l}.mp4", int(round(t3 * 15))) if t3 is not None else None
    P = Image.new("RGB", (1920, 580), (8, 12, 24))
    P.paste(ant, (0, 40))
    if dep is not None:
        P.paste(dep, (960, 40))
    d = ImageDraw.Draw(P)
    d.text((8, 6), f"caso {n} · {l} {a} ({100 * fr:.0f}%) · ANTES (v2, {tg // 60}:{tg % 60:02d}): {defeito}", fill=(255, 230, 0))
    d.text((968, 6), f"DEPOIS (v3, {t3:.1f} s do lote): {corr}", fill=(120, 255, 160))
    P.save(OUT / f"caso_{n:02d}.png")
    lin.append(f"{n:2d} · {l} {a} ({100 * fr:.0f}%) · {tg // 60}:{tg % 60:02d} (v2) → {t3:.1f} s (v3) · {defeito} → {corr}")
(U / "renders" / "casos_w2.txt").write_text("\n".join(lin) + "\n", encoding="utf-8")
print("\n".join(lin))
