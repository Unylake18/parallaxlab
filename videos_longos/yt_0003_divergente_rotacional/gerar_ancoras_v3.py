"""Extrai da narração V3 (GPT) as âncoras, o texto corrido e a tabela de compatibilidade com o preview V1.7."""
import re, shutil, sys
from pathlib import Path

aqui = Path(__file__).parent
src = Path(r"K:\Downloads\narracao_yt0003_v3_gpt.md")
V31 = len(sys.argv) > 1 and sys.argv[1] == "3.1"
SUF = "_v3_1" if V31 else "_v3"
if V31:
    dst = aqui / "narracao_v3_1.md"
else:
    dst = aqui / "narracao_v3_gpt.md"
    shutil.copyfile(src, dst)
md = dst.read_text(encoding="utf-8")

# id → (tempo aproximado no preview V1.7 em s, situação visual, nota para a remodelagem)
M = {
 "H01": (.5, "ok", ""), "H02": (2, "ok", ""), "H03": (3.7, "ok", "sonda aparece como rodinha branca"), "H04": (5.9, "ok", "texto 'Como leis sobre superfícies…' fica; segurar"),
 "G01": (8.5, "ok", ""), "G02": (11, "ok", ""), "G03": (13, "ok", ""), "G04": (14.8, "ok", ""), "G05": (21, "ok", ""),
 "G06": (36.3, "ok", ""), "G07": (40.5, "segurar", "Q_env → ∫ρ dV: deixar nuvem visível durante a fala"), "G08": (48.6, "ok", "foco em P entra aqui (56–60 s)"),
 "D01": (64.5, "ok", ""), "D02": (72, "ok", ""), "D03": (80, "ok", ""), "D04": (91, "ok", ""), "D05": (104, "ok", ""),
 "D06": (119, "ok", ""), "D07": (124, "ok", ""), "D08": (140, "ok", ""), "D09": (146, "segurar", "multiplicar/dividir por dx + gráfico"),
 "D10": (150, "segurar", "secante→tangente: animação de 6 s deve acompanhar a fala"), "D11": (158, "ajustar", "texto 'y e z fixos' já existe no gráfico; destacar na fala"),
 "D12": (165, "ok", ""), "D13": (175, "ok", ""), "D14": (188, "novo", "legenda curta 'três taxas de saída, não componentes' junto à soma"),
 "D15": (196, "ok", ""), "D16": (208, "ok", ""), "D17": (212, "ok", ""), "D18": (224, "ok", ""),
 "T01": (226, "ok", ""), "T02": (240, "ok", ""), "T03": (254, "ok", ""), "T04": (266, "ok", ""), "T05": (270, "ok", ""), "T06": (290, "ok", ""),
 "L01": (299, "ok", ""), "L02": (307, "ok", ""), "L03": (313, "ok", ""), "L04": (318, "ok", ""),
 "K01": (329, "ajustar", "legenda do κ pequena demais na V1.7: aumentar"), "K02": (336, "ok", ""), "K03": (346, "ok", "mostrar também ρ = 3ε0κ"),
 "P01": (352, "ok", ""), "P02": (356, "ok", ""), "P03": (377, "ok", ""), "P04": (384, "segurar", "10 s de encolhimento"), "P05": (394, "ok", ""),
 "P06": (406, "ok", ""), "P07": (411, "ajustar", "V3 tirou a discussão da fronteira: simplificar o trecho do flash/atravessar a origem"),
 "P08": (424, "novo", "propriedade de amostragem ∫ f(r) δ³(r) dV = f(0): nova equação/visual"),
 "P09": (428, "ok", ""), "P10": (433, "ok", ""), "P11": (441, "ok", "hold curto"),
 "R01": (454, "ok", ""), "R02": (458, "ok", ""), "R03": (461, "ok", ""), "R04": (468, "novo", "mostrar ∇·F₂ = 0 (hoje só ∇·F₁ = 0 está na tela)"),
 "R05": (491, "ok", ""), "R06": (495, "ok", ""), "R07": (505, "ok", ""), "R08": (516, "ok", ""),
 "C01": (526, "ok", ""), "C02": (531, "ajustar", "legenda 'trabalho por unidade de carga'"), "C03": (538, "ok", ""), "C04": (539, "ok", ""), "C05": (546, "ok", ""),
 "C06": (551, "ok", ""), "C07": (563, "ok", ""), "C08": (568, "ok", ""), "C09": (582, "ok", ""), "C10": (584, "novo", "hold curto antes de Stokes"),
 "S01": (586, "ok", ""), "S02": (597, "ok", ""), "S03": (599, "ajustar", "loops microscópicos com bordas internas se cancelando: enfatizar"), "S04": (601, "ajustar", "mostrar normal junto do eixo do giro"),
 "S05": (609, "ok", ""), "S06": (614, "ok", ""), "S07": (622, "ok", "incluir 'campo regular na região' em legenda curta"), "S08": (628, "ok", ""),
 "S09": (645, "ajustar", "marcar região regular (sem a carga)"), "S10": (658, "ok", ""),
 "M01": (664.3, "ok", ""), "M02": (677, "ok", ""), "M03": (690, "ok", ""),
 "F01": (700, "ok", ""), "F02": (706, "ok", ""), "F03": (720, "ajustar", "mostrar ΔV = −∫E·dℓ ligando à circulação"),
 "F04": (726, "ok", ""), "F05": (731, "ok", ""), "CTA01": (738, "ok", ""), "CTA02": (753, "ok", ""),
}

blocos = []
for m in re.finditer(r"### (\w+) — ([^\n]*)\n\*\*Evento visual[^:]*:\*\* ([^\n]*)\n\n> ([^\n]*)", md):
    i, tit, ev, tx = m.groups()
    tx = re.sub(r"\*\*|\\\(|\\\)", "", tx)
    blocos.append((i, tit, ev, tx))
ids = [b[0] for b in blocos]
faltam = [i for i in ids if i not in M]; sobram = [i for i in M if i not in ids]
assert not faltam and not sobram, (faltam, sobram)
words = lambda s: len(re.findall(r"\w+", s))
tot = sum(words(b[3]) for b in blocos)
ts = [M[i][0] for i in ids]
assert all(a <= b for a, b in zip(ts, ts[1:])), "ordem de tempo"

py = ['"""yt_0003 v3 (GPT) — âncoras: (instante atual do evento no preview V1.7, início da fala). ID = futura chamada self.ancora("ID")."""', "", "ANCORAS = ["]
for i, tit, ev, tx in blocos:
    first = " ".join(tx.split()[:4]).rstrip(",.;:")
    py.append(f'    ({M[i][0]:.1f}, "{first}"),  # {i}')
py.append("]")
(aqui / f"ancoras_voz{SUF}.py").write_text("\n".join(py) + "\n", encoding="utf-8")
(aqui / f"texto_narracao{SUF}.txt").write_text("\n\n".join(b[3] for b in blocos) + "\n", encoding="utf-8")

if V31:
    import json
    dur = {b[0]: {"palavras": words(b[3]), "s": round(words(b[3]) / 2.75 + .5, 2)} for b in blocos}
    (aqui / "duracoes_v3_1.json").write_text(json.dumps(dur, ensure_ascii=False, indent=1), encoding="utf-8")

cnt = {k: sum(1 for v in M.values() if v[1] == k) for k in ("ok", "ajustar", "segurar", "novo")}
rep = [f"# yt_0003 — compatibilidade da narração V3 com a cena (preview V1.7)\n",
       f"{len(blocos)} âncoras, {tot} palavras ≈ {tot/2.75/60:.1f} min a 2,75 palavras/s (≈ {tot/3.0/60:.1f} min a 3,0). Ordem das âncoras confere com a ordem visual do vídeo; nenhuma troca de sequência necessária.\n",
       f"Situação: {cnt['ok']} ok · {cnt['segurar']} segurar (só esperar mais) · {cnt['ajustar']} ajustar · {cnt['novo']} novo visual.\n",
       "| ID | ≈t atual | Situação | O que fazer na remodelagem |\n|---|---|---|---|"]
for i in ids:
    t, s, n = M[i]
    if s != "ok" or n:
        rep.append(f"| {i} | {int(t//60)}:{int(t%60):02d} | {s} | {n} |")
if not V31: (aqui / "compat_v3_cena.md").write_text("\n".join(rep) + "\n", encoding="utf-8")
print(len(blocos), tot, cnt)
