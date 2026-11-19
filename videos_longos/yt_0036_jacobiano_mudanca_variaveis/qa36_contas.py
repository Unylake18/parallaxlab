"""yt_0036 · QA CONTA INTEIRA (handoff §8.7): cada linha de C1 a C18 (§3.5 do v1 e §3 do handoff v2: C2, C3, C5, C8, C9, C16, C17 e C18 novos), degrau a degrau, com o tempo (s do vídeo) em que o degrau
fica escrito na tela e o gatilho falado que o lê (o último [gatilho] antes dele na mesma âncora). Lê as linhas [linha]/[gatilho]/[ancora] dos logs.
Saída: renders/v1/qa/conta_inteira_v1.txt.  uso: python qa36_contas.py"""
import ast
import json
import os
import re
from pathlib import Path

U = Path(__file__).resolve().parent
R = os.environ.get("RODADA", "v1")
QA = U / "renders" / R / "qa"
LOTES = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PB8", "PS"]

# (linha do §3.5, âncora, [degraus: substring do LaTeX (sem espaços) ou (substring, nome da parte)])
C = [
    ("C1.1 ∫₀² x dx = [x²/2]₀² = 2²/2 − 0²/2 = 2", "B1-1", [r"\int_{\Am{0}}^{\Am{2}}\X\,\dX", r"\Big[\dfrac{\X^2}{2}\Big]", r"\dfrac{2^2}{2}-\dfrac{0^2}{2}", r"\dfrac{0^2}{2}=2"]),
    ("C1.2 x = 2t ⇒ dx = 2 dt · x = 0 ⇒ t = 0 · x = 2 ⇒ t = 1", "B1-1", [r"\X=2\Uc{t}", r"\dX=\Lm{2}\,\Uc{dt}", r"\X=\Am{0}\Rightarrow\Uc{t}=", r"\X=\Am{2}\Rightarrow\Uc{t}="]),
    ("C1.3 ∫₀² x dx = ∫₀¹ (2t)·2 dt = 4∫₀¹ t dt = 4[t²/2]₀¹ = 4·(1/2 − 0) = 2 ✓", "B1-1",
     [r"(2\Uc{t})\cdot\Lm{2}\,\Uc{dt}", r"=4\int_{\Uc{0}}^{\Uc{1}}\Uc{t}\,\Uc{dt}", r"4\Big[\dfrac{\Uc{t}^2}{2}\Big]", r"4\cdot\left(\dfrac{1}{2}-0\right)", r"\right)=2"]),
    ("C1.4 x = g(t) ⇒ Δx ≅ g′(t) Δt · FATOR DE COMPRIMENTO: |g′(t)|", "B1-1", [r"\X=g(\Uc{t})", r"FATORDECOMPRIMENTO:"]),
    ("C2 v2 CAIXA (2+1)(1+3) = 3·4 = 12 · cada pedaço com a origem no desenho: 2·1/2 → 1 · 1·3/2 → 3/2 · 1·1 → 1 · ÁREA = 12 − 2 − 3 − 2 = 5", "B3-1",
     [r"(2+1)(1+3)=3\cdot4", r"=12", r"\Ge{\dfrac{2\cdot1}{2}}", r"-2\cdot\dfrac{2\cdot1}{2}=-2", r"\Ge{\dfrac{1\cdot3}{2}}", r"-2\cdot\dfrac{1\cdot3}{2}=-3",
      r"\Ge{\dfrac{3}{2}}", r"\Ge{1\cdot1}", r"-2\cdot(1\cdot1)=-2", r"=12-2-3-2", r"-2=\Lm{5}"]),
    ("C3 v2 ÁREA = (a+b)(c+d) − 2·ac/2 − 2·bd/2 − 2·bc → − ac − bd − 2bc → produto aberto → ad + bc − 2bc → ad − bc = det → 2·3 − 1·1 = 6 − 1 = 5 · CÉLULA → 5 ΔuΔv · FATOR CONSTANTE", "B3-2",
     [r"-2\cdot\dfrac{\Uc{a}\Uc{c}}{2}", r"-\Uc{a}\Uc{c}-\Vc{b}\Vc{d}-2\Vc{b}\Uc{c}", r"=\Uc{a}\Uc{c}+\Uc{a}\Vc{d}+\Vc{b}\Uc{c}+\Vc{b}\Vc{d}", r"=\Uc{a}\Vc{d}+\Vc{b}\Uc{c}-2\Vc{b}\Uc{c}",
      r"=\Uc{a}\Vc{d}-\Vc{b}\Uc{c}", r"=\det\begin{bmatrix}\Uc{a}&\Vc{b}", r"=2\cdot3-1\cdot1", r"=6-1=\Lm{5}", r"CÉLULA", r"FATORCONSTANTE"]),
    ("C4 x = (u+v)/2, y = (u−v)/2 · det = (1/2)(−1/2) − (1/2)(1/2) = −1/4 − 1/4 = −1/2 · ÁREA = |−1/2| = 1/2", "B3-3",
     [r"\X=\dfrac{\uu+\vv}{2}", r"\det=\dfrac{1}{2}\cdot\left(-\dfrac{1}{2}\right)", r"-\dfrac{1}{4}-\dfrac{1}{4}", r"=\Al{-\dfrac{1}{2}}", r"\left|\Al{-\dfrac{1}{2}}\right|",
      r"\right|=\Lm{\dfrac{1}{2}}"]),
    ("C6 ∂φ/∂u ∧ ∂φ/∂v = det[i j k; …] = (x_u y_v − x_v y_u) k = det[x_u x_v; y_u y_v] k · ‖…‖ = |J| · ÁREA DE B ≅ |J| ΔuΔv", "B4-3",
     [r"\pu\wedge\pv=\det\begin{bmatrix}\veci", r"(\xu\yv-\xv\yu)\,\veck", r"=\det\begin{bmatrix}\xu&\xv", r"\left\|\pu\wedge\pv\right\|=\JJ", r"B\cong\JJ\Du\,\Dv",
      r"FATORLOCALDEÁREA"]),
    ("C6 (3D) ‖(∂φ/∂u Δu) ∧ (∂φ/∂v Δv)‖ → Δu Δv ‖∂φ/∂u ∧ ∂φ/∂v‖", "B4-2", [r"\Lm{\Big\|}\Big(\pu\Du\Big)", r"=\Du\,\Dv\Lm{\Big\|}\pu\wedge\pv"]),
    ("C5 v2 (9 linhas) x = u² − v², y = 2uv · as 4 derivadas · J = det[2u −2v; 2v 2u] = (2u)(2u) − (−2v)(2v) = 4u² − (−4v²) = 4u² + 4v² · M: … = 2,25 + 1 = 3,25 · J(0,0) = 0 · J(1,1) = 8", "B4-3",
     [r"\X=\uu^2-\vv^2", (r"\dd{\X}{\uu}=2\uu", "a"), (r"\dd{\X}{\vv}=-2\vv", "b"), (r"\dd{\Y}{\uu}=2\vv", "c"), (r"\dd{\Y}{\vv}=2\uu", "d"),
      r"\Jq=\det\begin{bmatrix}2\uu&-2\vv", r"=(2\uu)(2\uu)-(-2\vv)(2\vv)", r"=4\uu^2-(-4\vv^2)", r"=4\uu^2+4\vv^2", r"M=(0{,}75;0{,}5):4\cdot(0{,}75)^2",
      r"=4\cdot0{,}5625+4\cdot0{,}25", r"=2{,}25+1", r"=\Lm{3{,}25}", r"J(0,0)=4\cdot0^2+4\cdot0^2=0", r"J(1,1)=4\cdot1^2+4\cdot1^2=\Lm{8}"]),
    ("Tabela do B4-3 (Δ · EXATA ≈ · |J(M)| Δ² · RAZÃO)", "B4-3", [r"\Lm{1{,}44}", r"\Lm{1{,}16}", r"\Lm{1{,}08}", r"\Lm{1{,}02}"]),
    ("C7 ① ∬ f ≅ ΣΣ f(x̄, ȳ) α(Bᵢⱼ) · α(Bᵢⱼ) ≅ |J| ΔuΔv · (x̄, ȳ) = φ(ū, v̄) · ② · ③", "B5-1",
     [r"\iint_B\f\,\dX\,\dY\cong\sum_i\sum_j", r"\alpha(B_{ij})\cong\Lm{|J(", r"\cong\sum_i\sum_j\f(\varphi(", r"\to\iint_{B_{uv}}\f(\varphi(\uu,\vv))"]),
    ("Teorema (B5-2): hipóteses 1–6, ⇒, quadro-receita", "B5-2",
     [r"DECLASSE", r"COMPACTO,", r"B=\varphi(B_{uv}),", r"INVERSÍVELNOINTERIOR", r"\neq0", r"INTEGRÁVELEM", r"\Rightarrow\\iint_B\f(\X,\Y)", r"\dX\,\dY=\JJ\,\du\,\dv", r"DETERMINAR"]),
    ("C8 v2 ÁREA = ∬ (4u² + 4v²) · ∫₀¹ … du = [4u³/3 + 4v²u] = (4/3 + 4v²) − (0 + 0) = 4/3 + 4v² · ∫₀¹ … dv = [4v/3 + 4v³/3] = (4/3 + 4/3) − (0 + 0) = 8/3", "B5-4",
     [r"\iint_{[0,1]^2}\Lm{(4\uu^2+4\vv^2)}", r"\Big[\dfrac{4\uu^3}{3}+4\vv^2\uu\Big]_{\uu=0}^{\uu=1}", r"=\left(\dfrac{4}{3}+4\vv^2\right)-(0+0)", r"(0+0)=\dfrac{4}{3}+4\vv^2",
      r"\Big[\dfrac{4\vv}{3}+\dfrac{4\vv^3}{3}\Big]", r"=\left(\dfrac{4}{3}+\dfrac{4}{3}\right)-(0+0)", r"(0+0)=\Lm{\dfrac{8}{3}}"]),
    ("C9 v2 SAÍDA/ENTRADA · COMPRIMENTO = 2 − y²/2 · ∫₀² … dy = [2y − y³/6]₀² = (4 − 8/6) − (0 − 0) = 4 − 4/3 = 8/3 ✓", "B5-4",
     [r"\vv=1:\X=\uu^2-1", r"\Rightarrow\uu=\dfrac{\Y}{2}", r"\Az{\X=\dfrac{\Y^2}{4}-1}", r"\uu=1:\X=1-\vv^2", r"\Co{\X=1-\dfrac{\Y^2}{4}}",
      r"\Co{\left(1-\dfrac{\Y^2}{4}\right)}-\Az{", r"=2-\dfrac{\Y^2}{2}", r"\Big[2\Y-\dfrac{\Y^3}{6}\Big]", r"=\left(4-\dfrac{8}{6}\right)-(0-0)", r"(0-0)=4-\dfrac{4}{3}",
      r"\dfrac{4}{3}=\Lm{\dfrac{8}{3}}"]),
    ("C10 u = x + y · v = x − y · u + v = 2x ⇒ x = (u+v)/2 · u − v = 2y ⇒ y = (u−v)/2", "B6-1",
     [r"\uu=\Uc{\X+\Y}", r"\uu+\vv=2\X", r"\X=\dfrac{\uu+\vv}{2}", r"\uu-\vv=2\Y", r"\Y=\dfrac{\uu-\vv}{2}"]),
    ("C11 ∂x/∂u = 1/2 … · J = … = −1/4 − 1/4 = −1/2 · |J| = 1/2 · ∂(u,v)/∂(x,y) = −2 · (−2)(−1/2) = 1", "B6-1",
     [(r"\dd{\X}{\uu}=\dfrac{1}{2}", "a"), (r"\dd{\X}{\vv}=\dfrac{1}{2}", "b"), (r"\dd{\Y}{\uu}=\dfrac{1}{2}", "c"), (r"\dd{\Y}{\vv}=-\dfrac{1}{2}", "d"),
      r"\Jq=\left(\dfrac{1}{2}\right)", r"=-\dfrac{1}{4}-\dfrac{1}{4}", r"=\Lm{-\dfrac{1}{2}}", r"\dfrac{\partial(\uu,\vv)}{\partial(\X,\Y)}=1\cdot(-1)-1\cdot1",
      r"=\Al{-2}", r"\right)=1"]),
    ("C12 os quatro lados → u = v, v = 2, u = −v, v = 1 · os cantos · B_uv", "B6-2",
     [r"\Y=0:", r"\Co{\uu=\vv}", r"\X-\Y=2}\Rightarrow\Vc{\vv=2}", r"\X=0:", r"\Az{\uu=-\vv}", r"\X-\Y=1}\Rightarrow\Vc{\vv=1}", r"(1,1)", r"(2,2)", r"(-2,2)", r"(-1,1)",
      r"B_{uv}:\quad\Vc{1}\le\vv\le\Vc{2}"]),
    ("C13 ∬ e^{(x+y)/(x−y)} dx dy = ∫₁² ∫_{−v}^{v} e^{u/v} · (1/2) du dv", "B6-3", [r"e^{\uu/\vv}\cdot\Lm{\dfrac{1}{2}}\,\du\,\dv"]),
    ("C14 PRIMITIVA EM u · CONFERE ✓ · [v e^{u/v}] = v e^{v/v} − v e^{−v/v} = v e − v e^{−1} = v(e − 1/e)", "B6-3",
     [r"\uu:\vv\,e^{\uu/\vv}", r"\dfrac{d}{d\uu}\left(\vv\,e^{\uu/\vv}\right)", r"\Big[\vv\,e^{\uu/\vv}\Big]_{\uu=\Az{-\vv}}^{\uu=\Co{\vv}}", r"\vv\,e^{\Co{\vv}/\vv}-\vv\,e^{\Az{-\vv}/\vv}",
      r"=\vv\,e-\vv\,e^{-1}", r"=\vv\left(e-\dfrac{1}{e}\right)"]),
    ("C15 (1/2)∫ v(e − 1/e) dv = (1/2)(e − 1/e)∫ v dv · [v²/2]₁² = 4/2 − 1/2 = 3/2 · = (3/4)(e − 1/e) ≈ 1,763", "B6-3",
     [r"\Lm{\dfrac{1}{2}}\int_{\Vc{1}}^{\Vc{2}}\vv\left(e-\dfrac{1}{e}\right)\dv", r"=\Lm{\dfrac{1}{2}}\left(e-\dfrac{1}{e}\right)\int_{\Vc{1}}^{\Vc{2}}\vv\,\dv",
      r"\Big[\dfrac{\vv^2}{2}\Big]", r"=\dfrac{4}{2}-\dfrac{1}{2}", r"\dfrac{1}{2}=\dfrac{3}{2}", r"\left(\dfrac{3}{2}\right)", r"=\dfrac{3}{4}\left(e-\dfrac{1}{e}\right)", r"\approx1{,}763"]),
    ("C16 v2 PLANO u, v: ∫₁² (v − (−v)) dv = ∫₁² 2v dv = [v²]₁² = 2² − 1² = 4 − 1 = 3 · 3 · 1/2 = 3/2 · PAPEL: 2·2/2 − 1·1/2 = 2 − 1/2 = 3/2 ✓ · 1/2 = O JACOBIANO", "B6-4",
     [r"\uu,\vv:\int_{\Vc{1}}^{\Vc{2}}\left(\Co{\vv}-(\Az{-\vv})\right)\dv", r"=\int_{\Vc{1}}^{\Vc{2}}2\vv\dv", r"=\Big[\vv^2\Big]_{\Vc{1}}^{\Vc{2}}", r"=2^2-1^2", r"=4-1",
      r"4-1=3", r"3\cdot\Lm{\dfrac{1}{2}}=\dfrac{3}{2}", r"\dfrac{2\cdot2}{2}-\dfrac{1\cdot1}{2}", r"=2-\dfrac{1}{2}", r"2-\dfrac{1}{2}=\dfrac{3}{2}", r"=OJACOBIANO"]),
    ("C17 v2 (9 linhas) u = x − y, v = x + y · u + v = 2x ⇒ x = (u+v)/2 · v − u = 2y ⇒ y = (v−u)/2 · as 4 derivadas · J = … = 1/4 + 1/4 = +1/2 · as bordas · B_uv · "
     "∫ cos u/sen v du = (1/sen v)[sen u] = (sen v − sen(−v))/sen v · sen(−v) = −sen v · = (sen v + sen v)/sen v = 2 sen v/sen v = 2 · (1/2)∫₁² 2 dv = (1/2)[2v]₁² = (1/2)(2·2 − 2·1) = (1/2)·2 = 1 ✓", "B7",
     [r"\iint_B\dfrac{\Ci{\cos}(\X-\Y)}", r"\uu=\X-\Y,\vv=\X+\Y", r"\uu+\vv=2\X", r"\Rightarrow\X=\dfrac{\uu+\vv}{2}", r"\vv-\uu=2\Y", r"\Rightarrow\Y=\dfrac{\vv-\uu}{2}",
      r"\dd{\X}{\uu}=\dfrac{1}{2}", r"J=\left(\dfrac{1}{2}\right)\left(\dfrac{1}{2}\right)-", r"=\dfrac{1}{4}+\dfrac{1}{4}", r"=\Lm{+\dfrac{1}{2}}",
      (r"\X+\Y=1", "borda 1"), (r"\X+\Y=2", "borda 2"), (r"\Y=0", "borda 3"), (r"\X=0", "borda 4"), (r"B_{uv}:\Vc{1}\le\vv\le\Vc{2}", "B_uv: ≤ v ≤"),
      (r"\Az{-\vv}\le\uu\le\Co{\vv}", "−v ≤ u ≤ v"), r"\int_{\Az{-\vv}}^{\Co{\vv}}\dfrac{\Ci{\cos}\uu}{\Ci{\sen}\vv}", r"\Big[\Ci{\sen}\uu\Big]_{\uu=\Az{-\vv}}",
      r"\dfrac{\Ci{\sen}\vv-\Ci{\sen}(-\vv)}{\Ci{\sen}\vv}", r"\Ci{\sen}(-\vv)=-\Ci{\sen}\vv", r"\dfrac{\Ci{\sen}\vv+\Ci{\sen}\vv}{\Ci{\sen}\vv}",
      r"\dfrac{2\Ci{\sen}\vv}{\Ci{\sen}\vv}", r"{\Ci{\sen}\vv}=2", r"\Lm{\dfrac{1}{2}}\int_{\Vc{1}}^{\Vc{2}}2\dv", r"\Big[2\vv\Big]_{\Vc{1}}^{\Vc{2}}",
      r"(2\cdot\Vc{2}-2\cdot\Vc{1})", r"\Lm{\dfrac{1}{2}}\cdot2", r"\cdot2=1"]),
    ("C18 (nova) φ(u, v) = (u², v) · x_u = 2u, x_v = 0, y_u = 0, y_v = 1 · J = det[2u 0; 0 1] = 2u·1 − 0·0 = 2u · ∬ |2u| · ∫₋₁¹ |2u| du = ∫₋₁⁰ (−2u) du + ∫₀¹ 2u du · "
     "= [−u²]₋₁⁰ + [u²]₀¹ = (0 − (−1)) + (1 − 0) = 1 + 1 = 2 · ∫₀¹ 2 dv = [2v]₀¹ = 2 − 0 = 2", "B5-3",
     [r"\varphi(\uu,\vv)=(\uu^2,\vv)", (r"\xu=2\uu", "a"), (r"\xv=0", "b"), (r"\yu=0", "c"), (r"\yv=1", "d"), r"J=\det\begin{bmatrix}2\uu&0", r"=2\uu\cdot1-0\cdot0",
      r"=\Lm{2\uu}", r"\iint_{[-1,1]\times[0,1]}\Lm{|2\uu|}", r"=\int_{-1}^{0}(-2\uu)\du+\int_{0}^{1}2\uu\du", (r"\Big[\uu^2\Big]_{0}^{1}", "= [u²]"),
      (r"=\Big[-\uu^2\Big]_{-1}^{0}+", "[−u²] +"), (r"(1-0)", "( − )"), (r"=(0-(-1))+(1-0)", "( − ( ) ) e +"), (r"=1+1=\Al{2}", "= +"),
      r"\int_{\Vc{0}}^{\Vc{1}}2\dv", r"=\Big[2\vv\Big]_{\Vc{0}}^{\Vc{1}}", r"=2-0", r"2-0=\Al{2}"]),
]


def sem_esp(s):
    s = re.sub(r"\\(qquad|quad|,|;|!|\s)", "", s)          # espaçamentos do LaTeX não contam no casamento
    s = re.sub(r"\\(?![A-Za-z{}])", "", s)                   # barra que não abre comando (\\, "\ " já tirado) também não
    return re.sub(r"\s+", "", s)


def main():
    ini = json.loads((U / "renders" / R / f"lotes_{R}.json").read_text())["inicio"] if (U / "renders" / R / f"lotes_{R}.json").exists() else {}
    ev = []          # (aid, t_lote, tipo, conteúdo, lote)
    for l in LOTES:
        p = U / f"log_{l}.txt"
        if not p.exists():
            continue
        an = {}
        for ln in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = re.match(r"\[ancora\] (\S+) ([\d.]+)", ln)
            if m:
                an[m.group(1)] = float(m.group(2))
            m = re.match(r"\[gatilho\] (\S+)\s+([\d.]+)s .*?\) (.*)$", ln)
            if m:
                ev.append((m.group(1), float(m.group(2)), "g", m.group(3), l, an))
            m = re.match(r"\[linha\] \S+ (\S+)\s+([\d.]+)s (\S+) (.*)$", ln)
            if m:
                try:
                    tx = ast.literal_eval(m.group(4))
                except Exception:
                    tx = m.group(4)
                ev.append((m.group(1), float(m.group(2)), "l", tx, l, an))
    out, faltam, tot = [], 0, 0
    for nome, aid, degs in C:
        out.append(f"\n{nome}  [{aid}]")
        es = [e for e in ev if e[0] == aid]
        for d in degs:
            sub, tag = (d if isinstance(d, tuple) else (d, None))
            tot += 1
            hit = None
            for k, e in enumerate(es):
                if e[2] != "l":
                    continue
                tx = sem_esp(e[3])
                if sem_esp(sub) in tx and (tag is None or tx.endswith(sem_esp(f"[{tag}]"))):
                    hit = (k, e)
                    break
            if hit is None:
                faltam += 1
                out.append(f"   FALTA  {sub}")
                continue
            k, e = hit
            g = [x for x in es[:k] if x[2] == "g"]
            gat = g[-1][3] if g else "(início da âncora)"
            t_an = e[5].get(aid, 0.0)
            tv = ini.get(e[4], 0) / 15 + t_an + e[1]
            out.append(f"   {int(tv // 60)}:{tv % 60:05.2f} (âncora {e[1]:6.2f} s) · gatilho «{gat}» · {sub}")
    (QA / f"conta_inteira_{R}.txt").write_text(
        "CONTA INTEIRA (§3.5 do v1 + §3 do v2, C1–C18): cada degrau com o tempo em que fica escrito na tela (fim da caneta ou do glyph map; m:ss do preview) e o gatilho\n"
        "falado que o lê (último gatilho da âncora antes dele). Nenhuma linha fora do §3.5 na coluna; os rótulos de eixo, tiques e placas não são conta.\n"
        f"DEGRAUS: {tot} · FALTANDO: {faltam}\n" + "\n".join(out) + "\n", encoding="utf-8")
    print("degraus", tot, "faltando", faltam)


if __name__ == "__main__":
    main()
