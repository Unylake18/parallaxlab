"""Aplica as substituições do fechamento V3.1 sobre narracao_v3_gpt.md e grava narracao_v3_1.md."""
import re
from pathlib import Path

aqui = Path(__file__).parent
md = (aqui / "narracao_v3_gpt.md").read_text(encoding="utf-8")

NOVO = {
"H01": "Tem duas expressões que aparecem o tempo todo quando a gente começa a escrever o eletromagnetismo na forma diferencial. À primeira vista, elas parecem só operações de cálculo vetorial. Mas fisicamente elas respondem duas perguntas muito concretas sobre o campo em cada ponto do espaço.",
"H02": "A primeira pergunta é: existe uma fonte aqui? Em torno desse ponto, está saindo mais campo do que entrando? A quantidade que mede isso é o divergente do campo elétrico, escrito nabla ponto E.",
"H03": "A segunda pergunta é diferente: existe circulação local? Se eu colocasse uma pequena sonda geométrica nesse campo, existiria uma tendência de giro? A quantidade que mede essa estrutura é o rotacional. Por enquanto eu escrevo o rotacional de F, porque F representa um campo vetorial genérico.",
"H04": "E o interessante é que essas duas informações locais vão nascer de leis que, originalmente, falam de objetos inteiros. A Lei de Gauss fala do fluxo através de uma superfície fechada. A circulação fala do campo acumulado ao longo de um caminho. Hoje a gente vai fazer justamente essa passagem: sair do global, aproximar cada vez mais o olhar e descobrir o que essas leis dizem ponto a ponto.",
"D15": "Essa soma recebe um nome: divergente do campo elétrico. Em coordenadas cartesianas, ele é a derivada parcial da componente x em relação a x, mais a derivada parcial da componente y em relação a y, mais a derivada parcial da componente z em relação a z. Mas a interpretação física é mais importante que essa fórmula: o divergente mede quanto fluxo líquido nasce ou desaparece localmente, por unidade de volume.",
"L03": "Agora vem a passagem local. Numa região onde os campos são regulares, essa igualdade vale para qualquer volume que escolhermos — inclusive volumes arbitrariamente pequenos em torno de qualquer ponto. Então a integral da diferença só pode ser zero para todos esses volumes se a própria diferença for zero ponto a ponto. É exatamente aqui que a lei global vira uma equação local.",
"P06": "Então precisamos de um objeto matemático capaz de representar uma quantidade completamente concentrada num ponto. Fora desse ponto, ele não deve contribuir. Mas, quando integramos uma região que contém o ponto, ele precisa guardar uma quantidade finita. Esse objeto é a delta de Dirac tridimensional, escrita delta de Dirac tridimensional de r vetor.",
"P07": "A delta de Dirac não é uma função comum e não precisamos perguntar qual seria o seu \"valor\" ordinário exatamente na origem. Ela é uma distribuição, definida pelo efeito que produz quando aparece dentro de integrais. Se a origem não está no volume de integração, a integral é zero. Se a origem está no interior desse volume, a integral vale um.",
"P08": "Existe uma propriedade ainda mais poderosa. Pegue uma função regular, f de r, multiplique pela delta e integre sobre um volume que contém a origem. A delta seleciona justamente o valor da função naquele ponto: o resultado é f de zero. Por isso ela funciona como um seletor ideal de posição. Toda a integral ignora o restante do espaço e recolhe a informação exatamente onde a delta está concentrada.",
"P11": "Essa ideia aparece em muitos lugares da física. Uma massa pontual em gravitação pode usar uma delta espacial; uma força concentrada num instante pode usar uma delta no tempo; fontes idealizadas e modelos de localização usam a mesma lógica matemática. A dimensionalidade muda, mas o princípio é o mesmo: algo concentrado numa região de medida zero ainda pode produzir um efeito integral finito.",
"R06": "Esse segundo operador é o rotacional do campo vetorial F. Ele transforma a circulação local numa quantidade vetorial. A direção do rotacional fornece o eixo e a orientação desse giro pela regra da mão direita; o módulo mede a intensidade da circulação local por unidade de área. É por isso que uma pequena roda de pás funciona tão bem como imagem mental para esse conceito.",
"R07": "Para o campo que construímos, o rotacional vale dois ômega na direção z positiva. Aqui o fator dois não é um detalhe acidental: se F fosse um campo de velocidades de uma rotação rígida, ômega seria a velocidade angular e o rotacional seria duas vezes esse vetor de rotação. O ponto principal, porém, é geométrico: o campo uniforme e o campo giratório tinham o mesmo divergente, zero, mas o rotacional distingue imediatamente os dois.",
"C02": "Ao caminhar pela curva, o deslocamento infinitesimal, d ell vetor, é sempre tangente ao caminho. Em cada ponto fazemos o produto escalar entre o campo elétrico e esse deslocamento. Esse produto mede a contribuição do campo na direção em que estamos andando. Quando acumulamos essas contribuições ao longo de todo o caminho, obtemos a integral de linha do campo elétrico. Fisicamente, ela representa o trabalho realizado pelo campo por unidade de carga entre os dois pontos.",
"S04": "O rotacional é justamente a quantidade que resume esse comportamento local. Imagine um loop muito pequeno ao redor de um ponto. Pegue a circulação do campo nesse loop e divida pela área delimitada. No limite em que o loop encolhe, essa razão fornece a componente do rotacional perpendicular à superfície. Por isso o eixo do pequeno giro, o vetor rotacional e a normal do patch aparecem todos alinhados.",
"S07": "Esse é o teorema de Stokes. A circulação do campo ao longo da borda C é igual ao fluxo do rotacional através de uma superfície S limitada por essa borda. E existe uma hipótese importante: o campo precisa ser regular na região em que estamos aplicando o teorema. Borda e interior estão codificando a mesma estrutura geométrica, só que de duas perspectivas diferentes.",
"F03": "E agora volta aquela independência do caminho. Como a integral do campo elétrico entre dois pontos depende apenas dos extremos, podemos usar essa integral para definir uma grandeza escalar: o potencial elétrico. Se chamarmos os pontos de a e b, a diferença de potencial, V de b menos V de a, é definida como o negativo da integral do campo elétrico de a até b.",
}
NA_TELA = {
"P08": r"\int_V f(\mathbf r)\,\delta^{(3)}(\mathbf r)\,dV = f(\mathbf 0), \qquad \mathbf 0\in\operatorname{int}(V)",
"F03": r"V_b-V_a = -\int_a^b \mathbf E\cdot d\boldsymbol\ell",
}
for i, tx in NOVO.items():
    pat = re.compile(r"(### " + i + r" — [^\n]*\n\*\*Evento visual[^:]*:\*\* [^\n]*\n\n)> [^\n]*")
    assert pat.search(md), i
    extra = ("\n\n**Na tela:** \\[ " + NA_TELA[i] + " \\]") if i in NA_TELA else ""
    md = pat.sub(lambda m: m.group(1) + "> " + tx + extra, md, count=1)

md = md.replace("# yt_0003 — Narração V3 GPT", "# yt_0003 — Narração V3.1 (CONGELADA PARA SINCRONIZAÇÃO)", 1)
md = md.replace("---\n\n# 1. HOOK", """### Regra extra (V3.1)

Na primeira ocorrência de cada símbolo numa nova seção, pronunciar **nome + significado físico**: não apenas "q", mas a carga q; não apenas "r", mas a distância radial r; não apenas "E x", mas a componente x do campo elétrico, E x; não apenas "ômega", mas a constante escalar ômega; não apenas "d ell", mas o deslocamento infinitesimal d ell vetor; não apenas "V", mas o potencial elétrico V. Depois que o referente estiver inequívoco, a fala pode abreviar naturalmente. Não transformar a locução em leitura de símbolos.

---

# 1. HOOK""", 1)
md = md.replace("## Notas de implementação das âncoras\n", """## Notas de implementação das âncoras

0. (V3.1) A âncora marca o **início de uma unidade conceitual**; a tela não pode ficar congelada até a frase terminar. Dentro de cada âncora longa, usar microbeats sincronizados com a fala (ex. D10: mostra secante → "inclinação média" → começa dx→0 → pontos se aproximam → secante vira tangente → só quando a voz disser "vira uma derivada" aparece ∂E_x/∂x). Vale especialmente para D09–D15, P06–P10, R02–R07, C02–C09, S03–S10, F01–F05. Não resolver a nova duração só com `wait()`.
""", 1)
(aqui / "narracao_v3_1.md").write_text(md, encoding="utf-8")
print("ok", len(NOVO))
