"""Gera narracao_sugestao_v2_aprofundada.md, ancoras_voz_v2.py e texto_narracao_v2.txt a partir de narracao_v2_dados.py."""
import re
from narracao_v2_dados import SECOES

# tempos (s) no preview_v1_7 corrigidos pelos marcos reais e pelas pranchas (±4 s)
T = dict(A01=.5,A02=2,A03=3.7,A04=5.9,A05=8.5,A06=11,A07=13,A08=14.8,A09=17.5,A10=21,A11=25.7,A12=30.3,A13=36.3,A14=40.5,A15=48.6,A16=53.9,A17=56.4,A18=59.9,
 B01=64.5,B02=67.5,B03=72,B04=76,B05=80,B06=85,B07=91,B08=97,B09=104,B10=108,B11=112,B12=115,B13=119,B14=124,B15=131,B16=134,B17=140,B18=146,B19=150,B20=160,B21=165,B22=171,B23=175,B24=184,B25=188,B26=192,B27=196,B28=200,B29=208,B30=212,B31=218,B32=224,
 C01=226,C02=232,C03=236,C04=240,C05=246,C06=254,C07=262,C08=266,C09=270,C10=279,C11=290,C13=299,C14=304,C15=307,C16=313,C17=318,C18=322,
 K01=329,K02=331,K03=336,K03b=346,
 D01=352,D02=356,D03=377,D04=384,D05=394,D06=397,D07=399,D08=406,D09=408,D10=411,D11=417,D12=424,D13=428,D14=433,D15=441,
 D16=454,D17=458,D18=461,D19=468,D20=491,D21=495,D22=505,D23=516,
 E01=526,E02=531,E03=538,E04=539,E05=543,E06=546,E07=551,E08=561,E09=563,E10=568,E11=571,E12=582,
 E13=586,E14=597,E15=601,E16=609,E17=614,E18=622,E19=628,E20=637,E21=645,E22=658,
 F01=664.3,F02=669,F03=677,F04=684.5,F05=690,F06=700,F07=706,F08=714,F09=720,F10=726,F11=731,G01=738,G02=742,G03=750,G04=753)

EXTRA = {
 "A04":" E já adianto: essas duas ferramentas, divergente e rotacional, são a base de metade das equações de Maxwell, o conjunto que descreve toda a eletricidade e todo o magnetismo.",
 "B32":" Pensa numa mangueira: se entra por um lado a mesma água que sai pelo outro, não tem torneira nem ralo no meio, mas a água se move. É isso: divergente zero, campo diferente de zero.",
 "D11":" Quando a origem está exatamente na superfície do volume, o valor não é definido de forma simples. Por isso a gente não afirma nada nesse instante: só olha o antes e o depois.",
 "D15":" Essa mesma ideia aparece na gravitação, onde uma massa pontual é a fonte do campo gravitacional, e na mecânica quântica, onde a delta descreve uma partícula perfeitamente localizada.",
 "E12":" Compara com um redemoinho: na água, ao dar uma volta em torno do centro, você ganha circulação. No campo eletrostático, dar a volta não rende nada.",
 "E18":" É o mesmo truque de cancelamento interno do teorema da divergência, agora para giros em vez de fluxos: um é primo do outro.",
 "F05":" E repara que a eletrostática inteira cabe em duas equações: divergente de E igual a rô sobre epsilon zero, e rotacional de E igual a zero.",
 "F11":" Se você já viu um mapa topográfico, é a mesma ideia: as linhas de nível são as equipotenciais, e a água, como o campo, escorre pela direção de maior descida.",
}
RATE = 2.75   # palavras/s de uma aula calma
words = lambda s: len(re.findall(r"\w+", s))
anc = []; txt = []; resumo = []
tot_w = 0
for s in SECOES:
    blocos = s["blocos"]
    for bl in blocos:
        bl["t"] = T[bl["id"]]
        if bl["id"] in EXTRA:
            bl["texto"] += EXTRA[bl["id"]]
        bl["w"] = words(bl["texto"])
    w = sum(bl["w"] for bl in blocos); tot_w += w
    resumo.append((s["titulo"], w, w / RATE, blocos[0]["t"]))
secs_total = tot_w / RATE

md = []
md.append("# yt_0003 — sugestão de narração v2 (aprofundada, curso pré-vestibular)\n")
md.append(f"Status: **proposta para o GPT lapidar.** Texto sem pressa de relógio: **{tot_w} palavras ≈ {secs_total/60:.1f} min de voz a {RATE} palavras/s**. O vídeo atual (preview V1.7) dura 12:49; **o vídeo passa a se moldar à voz**: cada bloco abaixo é uma âncora, e a cena espera a fala terminar antes do próximo evento visual (marcador [SEGURAR] onde a espera é maior). Mesma física e mesma ordem do vídeo; nada de física nova.\n")
md.append("Princípio: **a voz explica o porquê e nomeia cada grandeza por extenso; o Manim mostra o como.** Estilo de professor de cursinho: devagar, concreto, com analogias e ganchos para assuntos vizinhos, sem ler a tela.\n")
md.append("## Como falar as grandezas\n")
md.append("""| Na tela | Na fala |
|---|---|
| E (vetor) | **o campo elétrico** (nunca só "E"); E_x: **a componente x do campo elétrico** |
| ∇·E | **o divergente do campo elétrico** ("nabla ponto E" na 1ª vez, depois "o divergente") |
| ∇×F, ∇×E | **o rotacional** do campo (F = "um campo vetorial qualquer") |
| Φ | **o fluxo** do campo elétrico ("fi" só na 1ª vez) |
| dA, dA (vetor) | **o elemento de área**; dA vetor = **o elemento de área vetorial** |
| n̂ | **o vetor normal unitário, a normal externa** |
| S | **a superfície gaussiana S** (superfície fechada) |
| Q_env | **a carga envolvida** |
| ρ | **rô, a densidade volumétrica de carga** |
| ε₀ | **epsilon zero, a permissividade elétrica do vácuo** |
| dV, dx, dy, dz | **o elemento de volume**; **dx, dy, dz: pequenos deslocamentos em x, y e z** |
| x̂, ŷ, ẑ | **os vetores unitários nas direções x, y e z** |
| ∂E_x/∂x | **a derivada parcial da componente x do campo em relação a x** |
| κ | **kappa, uma constante** |
| q, r, r̂ | **a carga q**, **a distância r**, **o vetor unitário radial** |
| δ³(r) | **delta de Dirac tridimensional** (o 3 não é potência) |
| Ω | **ômega maiúsculo, constante que controla a intensidade do giro** |
| dℓ | **o deslocamento infinitesimal ao longo do caminho** |
| r_a, r_b | **a distância da carga ao ponto a**; **… ao ponto b** |
| C, C₁, C₂ | **a curva fechada C**; **o caminho C um**; **o caminho C dois** |
| ∮ | **integral sobre um caminho (ou superfície) fechado(a)** |
| B | **o campo magnético**; ∂B/∂t = **a derivada parcial do campo magnético no tempo** |
| V | **o potencial elétrico** (escalar); ∇V = **o gradiente do potencial** |

Regra: toda grandeza nova entra com nome completo; nas repetições próximas pode encurtar ("o campo", "o fluxo"), mas **símbolo solto só quando a tela está apontando para ele**.
""")
md.append("## Como as âncoras funcionam\n")
md.append("""- Cada bloco `A01…G04` começa a ser falado **no instante do evento visual** descrito; a cena (`self.ancora("ID")`, a criar na próxima fase, na linha do evento) espera a voz acabar o bloco antes de seguir.
- Tempo `≈ mm:ss` = onde o evento ocorre **hoje** no preview V1.7 (±4 s); serve só para achar o quadro. O tempo final nasce da voz.
- Mesmo formato do yt_0002 (`ancoras_voz.py`: instante do evento → início da fala); a lista pronta está em `ancoras_voz_v2.py` e o texto corrido (para TTS) em `texto_narracao_v2.txt`.
- Onde a fala é muito mais longa que a animação atual, o bloco traz **[SEGURAR]** e a cena precisa de espera extra (ou animação mais lenta).
""")
for s in SECOES:
    blocos = s["blocos"]
    w = sum(bl["w"] for bl in blocos)
    md.append(f"\n## {s['titulo']}  \n*{s['resumo']}*  \n_{w} palavras ≈ {w/RATE:.0f} s de voz_\n")
    for bl in blocos:
        mm = f"{int(bl['t']//60)}:{int(bl['t']%60):02d}"
        md.append(f"**{bl['id']} · ≈{mm}** — *{bl['evento']}*  \n> {bl['texto']}\n")
        if bl["nota"]:
            md.append(f"_{bl['nota']}_\n")
        first = " ".join(bl["texto"].split()[:4]).rstrip(",.;:")
        anc.append((bl["id"], bl["t"], first))
        txt.append(bl["texto"])
md.append("\n## Comparação voz × cena (por seção)\n")
md.append("| Seção | Palavras | Voz estimada | Início atual no vídeo |\n|---|---|---|---|")
for tit, w, sec, t0 in resumo:
    md.append(f"| {tit} | {w} | {sec:.0f} s | {int(t0//60)}:{int(t0%60):02d} |")
md.append(f"| **Total** | **{tot_w}** | **{secs_total/60:.1f} min** | vídeo atual 12:49 |")
md.append("\nO vídeo tende a ficar com ~2,7× a duração atual (12:49 → ~34 min). Se o GPT achar longo, cortar primeiro os ganchos e as repetições; a ordem e as âncoras não mudam.\n")
open("narracao_sugestao_v2_aprofundada.md", "w", encoding="utf-8").write("\n".join(md))
py = ['"""yt_0003 v2 — âncoras entre a cena e a voz: (instante atual do evento no preview V1.7, início da fala que COMEÇA nesse evento).',
      'Ordem estritamente crescente; o ID (A01…G04) é a futura chamada self.ancora("ID") na cena."""', "", "ANCORAS = ["]
for id_, t, first in anc:
    py.append(f'    ({t:.1f}, "{first}"),  # {id_}')
py.append("]")
open("ancoras_voz_v2.py", "w", encoding="utf-8").write("\n".join(py) + "\n")
open("texto_narracao_v2.txt", "w", encoding="utf-8").write("\n\n".join(txt) + "\n")
print(tot_w, round(secs_total / 60, 1))
ts = [a[1] for a in anc]
print("ordem crescente:", all(x <= y for x, y in zip(ts, ts[1:])), [(anc[i][0], anc[i + 1][0]) for i in range(len(ts) - 1) if ts[i] > ts[i + 1]])
