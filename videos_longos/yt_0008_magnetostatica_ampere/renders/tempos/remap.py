import re, io, sys, json, collections
D = r"C:\Users\KaioOrtiz\PycharmProjects\parallax-long-0008\videos_longos\yt_0008_magnetostatica_ampere"
raw = io.open(D + r"\narracao_revisada_gpt.md", encoding="utf-8").read()
body = raw.split("\n---\n")[1].strip()          # só a fala
TOTAL = 19 * 60 + 12.9


def T(s):
    m, r = s.split(":")
    return int(m) * 60 + float(r)


def F(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


# (bloco, âncora, tela, frase inicial da unidade)
U = [
    ("B00", "0:00.0", "tema + fio (segura o quadro do fio com os traços verdes)", "Existe uma coisa estranha"),
    ("B00", "0:00.0", "(continua o quadro do fio) introdução do canal e da pergunta", "Fala, pessoal!"),
    ("B00", "0:14.1", "caixa «B → ?»", "Em vez de começar pela corrente"),
    ("B00", "0:02.0", "fio de aço, traços verdes (REPLAY do início, após a abertura)", "Comecemos pelo exemplo mais simples."),
    ("B00", "0:05.6", "anel magenta em volta do fio", "Ao redor do fio, o campo magnético forma"),
    ("B00", "0:07.2", "caixa «J → Biot–Savart → B»", "Até aqui, seguimos o caminho"),
    ("B00", "0:14.1", "caixa «B → ?»", "Mas agora vamos inverter"),
    ("B00", "0:17.6", "título «O que a geometria de B revela?»", "As linhas são curvas."),
    ("B01", "0:20.7", "vista de cima: ⊙ e círculo magenta", "Visto de cima, o fio aparece"),
    ("B01", "0:27.5", "ponto P, raio s, B tangente", "Escolhemos um ponto onde queremos observar"),
    ("B01", "0:28.2", "B = μ₀I/(2πs) φ̂", "Para um fio retilíneo infinito, Biot–Savart"),
    ("B01", "0:35.9", "título do rotacional; (∇×B)_z", "Agora calculamos o rotacional."),
    ("B01", "0:40.9", "entra o valor de Biot–Savart", "Substituímos o campo do fio."),
    ("B01", "0:45.4", "o s corta o s", "A distância \\(s\\) cancela"),
    ("B01", "0:47.3", "(μ₀I/2π) constante", "Sobra apenas uma constante."),
    ("B01", "0:50.1", "P se afasta; leituras s/s₀, B/B₀", "Isso também aparece no desenho."),
    ("B01", "1:01.1", "(∇×B)_z = (1/s)·0", "Como a derivada de uma constante é zero"),
    ("B01", "1:06.8", "legenda «só componente φ…»", "E as demais componentes também são nulas."),
    ("B01", "1:09.4", "∇×B = 0 (s > 0)", "Portanto, em qualquer ponto fora do eixo,"),
    ("B01", "1:12.2", "legenda «linhas curvas e rotacional zero»", "Essa é a primeira ideia importante do vídeo:"),
    ("B02", "1:17.6", "título «Rotacional: uma medida local»", "Para entender o que o rotacional realmente mede"),
    ("B02", "1:22.6", "laço pequeno em P, normal n̂, ∂A", "Imagine uma pequena sonda"),
    ("B02", "1:25.2", "(∇×B)·n̂ = lim (1/A)∮B·dℓ", "Agora percorremos a borda da sonda"),
    ("B02", "1:31.7", "legenda «Por que zero aqui?»", "Isso explica por que simplesmente olhar"),
    ("B02", "1:38.3", "setor: arcos e raios", "Neste campo do fio, podemos enxergar"),
    ("B02", "1:38.9", "∮B·dℓ = (sB_φ)ₒᵤₜ Δφ − (sB_φ)ᵢₙ Δφ", "No arco mais próximo do fio"),
    ("B02", "1:42.6", "∮B·dℓ = 0", "Como a intensidade varia inversamente"),
    ("B02", "1:51.1", "a sonda gira; n̂ gira junto", "Se girarmos a sonda"),
    ("B02", "2:01.8", "três orientações, três componentes nulas", "Portanto, o vetor rotacional é realmente nulo"),
    ("B03", "2:08.2", "título «Do laço local ao laço global»", "Mas agora vem a parte interessante."),
    ("B03", "2:13.4", "o laço cresce; I_enc = 0", "Enquanto o caminho não envolve o fio"),
    ("B03", "2:19.3", "o laço passa pelo eixo; «indefinida»", "Mas, no instante em que tentamos passar"),
    ("B03", "2:22.3", "I_enc = I; ∮ = μ₀I", "Depois que o laço passa a envolver"),
    ("B03", "2:31.5", "círculo centrado; B_φ·2πs", "Para um círculo centrado no fio"),
    ("B03", "2:32.2", "B_φ·2πs = μ₀I («calculado com Biot–Savart»)", "É importante notar que ainda"),
    ("B03", "2:37.8", "legenda «rotacional zero, circulação ≠ 0: como?»", "E surge a pergunta:"),
    ("B03", "2:42.3", "zoom no eixo; «?»", "A resposta está exatamente"),
    ("B04", "2:46.4", "título «Outra sonda: um volume fechado»", "Antes de resolver essa singularidade"),
    ("B04", "2:49.8", "caixa em meio a linhas retas", "Nessa região pequena, podemos tratar"),
    ("B04", "2:53.3", "normais para fora", "Como nos vídeos sobre a lei de Gauss"),
    ("B04", "2:56.2", "face de entrada; −Φ_B", "Onde o campo entra na caixa"),
    ("B04", "3:02.4", "as outras quatro faces", "Nas faces em que o campo é tangente"),
    ("B04", "3:05.1", "−Φ_B + Φ_B = 0", "Somando todas as faces"),
    ("B04", "3:11.1", "∇·B = lim (1/V)∮B·da", "Se dividimos esse fluxo pelo volume"),
    ("B04", "3:15.0", "∇·B = 0", "Essa é a forma diferencial da lei de Gauss"),
    ("B04", "3:25.2", "carga com E saindo; ∮E·da = Q/ε₀", "O contraste com o campo elétrico"),
    ("B04", "3:29.5", "legenda «não existe fonte nem sumidouro»", "Para o campo magnético, não aparece"),
    ("B05", "3:43.3", "região verde; r′, r, R", "Agora vamos mostrar que esse resultado"),
    ("B05", "3:47.1", "B(r) = (μ₀/4π)∫J×R/R³ dτ′", "Biot–Savart soma as contribuições"),
    ("B05", "3:51.7", "R = r − r′; F ≡ R/R³", "Para simplificar a notação"),
    ("B05", "4:01.8", "legenda «Tome o divergente»", "Agora calculamos o divergente do campo magnético"),
    ("B05", "4:10.2", "∇·(A×C) = C·(∇×A) − A·(∇×C)", "Usamos então uma identidade vetorial"),
    ("B05", "4:12.6", "legenda «se abre em dois termos»", "Ela produz dois termos."),
    ("B05", "4:14.8", "F·(∇×J) − J·(∇×F)", "No primeiro, aparece"),
    ("B05", "4:23.6", "∇×J(r′) = 0", "Mas a densidade \\(\\mathbf J(\\mathbf r')\\) depende"),
    ("B05", "4:28.9", "∇·B = −(μ₀/4π)∫J·(∇×F)", "O segundo termo contém"),
    ("B05", "4:37.3", "F = −∇(1/R)", "Mas esse fator pode ser escrito"),
    ("B05", "4:45.9", "∇·B = −(μ₀/4π)∫J·0", "Assim, os dois termos desaparecem"),
    ("B05", "4:52.3", "legenda «da própria lei de Biot–Savart»", "Existe uma sutileza"),
    ("B06", "5:00.3", "diagrama; observador se move; ∇ ↔ r", "Antes, vale separar muito bem"),
    ("B06", "5:08.1", "R e F mudam; J(r′) não", "Se movemos o observador"),
    ("B06", "5:13.2", "∇′ ↔ r′; a fonte anda", "Agora considere o operador nabla linha."),
    ("B06", "5:22.3", "linhas de corrente com traços", "As linhas verdes mostram"),
    ("B06", "5:26.1", "quadradinho sobre uma linha", "Agora escolhemos uma célula"),
    ("B06", "5:35.3", "normais para fora", "Nesse pequeno volume, entra tanta"),
    ("B06", "5:38.3", "∇′·J = 0", "Perceba que agora a justificativa"),
    ("B07", "5:51.7", "B(r) = (μ₀/4π)∫J×F dτ′", "Com essa diferença clara"),
    ("B07", "6:00.2", "∇×(A×C) = quatro termos", "A identidade vetorial correspondente"),
    ("B07", "6:13.7", "legenda «dois termos derivam J»", "Dois deles envolvem derivadas"),
    ("B07", "6:22.5", "dois termos restantes", "Sobram duas parcelas."),
    ("B08", "6:38.4", "setas radiais; ∇·F = 0", "O fator geométrico \\(\\mathbf F\\) aponta"),
    ("B08", "6:44.9", "esfera em volta da fonte; ∮F·da = 4π", "Mas algo especial acontece"),
    ("B08", "6:47.1", "a esfera encolhe", "Mesmo se fizermos a esfera encolher"),
    ("B08", "6:52.6", "∇·F = 4π δ³(r − r′)", "E é exatamente esse tipo de objeto"),
    ("B08", "6:56.7", "4π δ³ dentro da integral", "A delta de Dirac não deve ser pensada"),
    ("B08", "7:02.2", "os dois 4π se cancelam", "Depois que o fator quatro pi cancela"),
    ("B08", "7:12.1", "pontos-fonte com J(r′)", "Fixamos o observador."),
    ("B08", "7:16.5", "pico sobre o observador", "Agora imagine pesos"),
    ("B08", "7:22.8", "o pico se estreita", "No limite, apenas a contribuição"),
    ("B08", "7:32.0", "uma única seta verde grande", "A integral se reduz"),
    ("B08", "7:36.1", "∇×B = μ₀J(r) − …", "Portanto, a primeira parcela"),
    ("B09", "7:48.9", "F = F(r − r′)", "Ainda precisamos verificar a segunda."),
    ("B09", "7:53.3", "observador e fonte juntos", "Se deslocamos os dois pontos juntos"),
    ("B09", "8:02.4", "∂F/∂x = −∂F/∂x′", "Por isso, derivar o fator"),
    ("B09", "8:11.0", "(J·(−∇′))F", "Fazemos essa troca"),
    ("B09", "8:18.4", "regra do produto", "Agora usamos a regra do produto"),
    ("B09", "8:22.8", "duas parcelas (superfície e continuidade)", "O resultado se separa em duas contribuições."),
    ("B09", "8:30.1", "superfície distante: J = 0", "Como estamos considerando uma distribuição de corrente localizada"),
    ("B09", "8:36.9", "célula ampliada de novo", "A segunda contribuição contém"),
    ("B09", "8:50.6", "legenda «continuidade»", "Aqui, finalmente, entra a equação da continuidade."),
    ("B09", "8:52.8", "∫(J·∇′)F_i dτ′ = 0 − 0", "No regime estacionário, a densidade de carga"),
    ("B09", "8:58.1", "legenda «só agora o segundo termo some»", "As duas contribuições desaparecem."),
    ("B09", "9:02.3", "∇×B = μ₀J", "E sobra a relação local fundamental:"),
    ("B09", "9:04.9", "legenda «a lei local da magnetostática»", "Essa é a forma local da lei de Ampère"),
    ("B10", "9:18.2", "cilindro de aço; a e J", "Em vez de um fio matematicamente sem espessura"),
    ("B10", "9:21.9", "B = B_φ(s) φ̂", "Por simetria, o campo magnético continua"),
    ("B10", "9:32.4", "seção com ⊙; sonda dentro; 1,00 μ₀J", "Agora podemos usar diretamente a lei local"),
    ("B10", "9:36.6", "a sonda chega à borda", "Quando essa sonda atravessa parcialmente"),
    ("B10", "9:40.7", "sonda fora; leitura 0,00", "Quando fica completamente fora"),
    ("B10", "9:46.5", "gráfico B_φ(s); equação", "Agora escrevemos a equação diferencial"),
    ("B10", "9:53.9", "s B_φ = (μ₀J/2)s² + C", "Multiplicando pela distância radial"),
    ("B10", "9:57.6", "B_φ = (μ₀J/2)s + C/s", "Ao dividir novamente"),
    ("B10", "10:01.7", "«C/s → ∞»", "Mas esse termo explodiria no eixo."),
    ("B10", "10:04.7", "legenda «regularidade no eixo»", "Portanto, a regularidade exige"),
    ("B10", "10:05.8", "B_φ = (μ₀J/2)s", "Dentro do condutor, o campo cresce linearmente"),
    ("B10", "10:10.8", "sonda e ponto andam juntos", "E o gráfico acompanha"),
    ("B11", "10:16.8", "legenda «Fora, J = 0»", "Agora vamos para fora do cilindro."),
    ("B11", "10:23.4", "B_φ = C_ext/s", "A solução assume a forma"),
    ("B11", "10:25.5", "duas curvas tracejadas e uma cheia", "Mas ainda não sabemos"),
    ("B11", "10:28.6", "legenda «a continuidade em s = a»", "Nosso modelo possui corrente volumétrica"),
    ("B11", "10:32.8", "a curva passa pelo ponto de dentro", "O ramo externo precisa passar"),
    ("B11", "10:40.6", "legenda «I = Jπa²»", "A corrente total é igual"),
    ("B11", "10:41.2", "C_ext = μ₀I/2π", "Substituindo esse resultado"),
    ("B11", "10:46.7", "B ∝ s dentro, B ∝ 1/s fora", "Agora temos o perfil completo."),
    ("B12", "10:56.5", "pilar verde; painel a, J/J₀, I", "Agora vamos comprimir esse fio."),
    ("B12", "11:03.0", "pilar alto e fino; pico fora de escala", "Para conservar a mesma corrente"),
    ("B12", "11:09.1", "legenda «mais estreita e mais intensa»", "No limite em que o raio tende a zero"),
    ("B12", "11:12.4", "J → I δ(x)δ(y) ẑ", "Agora usamos uma delta de Dirac em duas dimensões"),
    ("B12", "11:15.2", "legenda «delta 2D com integral I»", "Quando integramos essa densidade singular"),
    ("B12", "11:15.9", "∇×B = μ₀I δ(x)δ(y) ẑ", "E finalmente resolvemos o paradoxo da abertura."),
    ("B12", "11:23.5", "laço grande envolvendo o eixo", "Portanto, um laço que envolve o fio"),
    ("B13", "11:32.3", "quatro fios; ∇×B = μ₀J", "Agora temos uma lei local:"),
    ("B13", "11:37.0", "contorno C", "Escolhemos um caminho fechado."),
    ("B13", "11:42.3", "S nasce da borda", "E escolhemos uma superfície"),
    ("B13", "11:45.2", "mão direita; normais; da", "A orientação do percurso"),
    ("B13", "11:48.4", "legenda «integre os dois lados sobre S»", "Integramos a componente normal"),
    ("B13", "11:53.4", "legenda «J·da só onde fura S»", "Cada pequeno elemento de área"),
    ("B13", "12:01.0", "∫J·da = I_enc", "A soma algébrica dessas contribuições"),
    ("B13", "12:03.9", "∫(∇×B)·da = μ₀I_enc", "Assim, a integral do rotacional sobre a superfície"),
    ("B14", "12:09.0", "disco de cima; duas células", "Agora falta transformar"),
    ("B14", "12:15.2", "aresta comum; setas opostas", "Na aresta compartilhada"),
    ("B14", "12:25.8", "malha inteira", "Quando repetimos isso por toda a superfície"),
    ("B14", "12:26.5", "∫(∇×B)·da = Σ∮B·dℓ", "No limite de uma divisão cada vez mais fina"),
    ("B14", "12:32.6", "só a borda", "E depois de todos os cancelamentos internos"),
    ("B14", "12:35.4", "∫(∇×B)·da = ∮B·dℓ; «Stokes»", "Esse é o teorema de Stokes."),
    ("B14", "12:41.3", "∮B·dℓ = μ₀I_enc", "Aplicando-o à lei local"),
    ("B14", "12:45.3", "caixa «Lei de Ampère · magnetostática»", "Continuamos falando de magnetostática."),
    ("B14", "12:49.8", "disco vira cúpula; S₁ e S₂", "Se mantemos a mesma borda"),
    ("B14", "12:54.0", "I_S₁ = I_S₂", "Considere duas superfícies diferentes"),
    ("B14", "12:57.7", "S₁ e S₂ formam V", "Juntas, elas formam"),
    ("B14", "13:00.7", "∮J·da = ∫∇·J dτ = 0", "No regime estacionário, o divergente da densidade de corrente é zero.\n\nPortanto"),
    ("B14", "13:04.5", "legenda «∇·J = 0»; I_S₁ = I_S₂", "Isso significa que a corrente líquida"),
    ("B15", "13:18.7", "contorno irregular", "Agora temos uma lei poderosa."),
    ("B15", "13:22.7", "legenda «B·dℓ varia ao longo de C»", "Se direção e intensidade variam"),
    ("B15", "13:26.8", "legenda «verdadeira ≠ útil»", "Como já vimos com a lei de Gauss"),
    ("B15", "13:47.4", "barra «simetria → B → caminho → I_enc»", "A estratégia é:"),
    ("B16", "13:53.9", "título «Fio infinito, agora por Ampère»", "Vamos aplicar esse método"),
    ("B16", "14:00.3", "o campo gira e desliza", "A fonte não muda se girarmos"),
    ("B16", "14:06.9", "B = B(s) φ̂", "Por isso, o campo depende apenas"),
    ("B16", "14:11.7", "círculo de raio s", "Escolhemos então uma circunferência"),
    ("B16", "14:16.1", "dℓ branco ∥ B magenta", "Em todos os seus pontos"),
    ("B16", "14:21.4", "B∮dℓ = μ₀I_enc", "A circulação se torna"),
    ("B16", "14:24.6", "o círculo vira segmento 2πs", "Esse comprimento é dois pi"),
    ("B16", "14:32.3", "disco violeta; o fio atravessa", "A corrente envolvida é simplesmente"),
    ("B16", "14:35.6", "B = μ₀I/(2πs)", "Então obtemos novamente"),
    ("B16", "14:38.2", "legenda «campo do fio infinito»", "É exatamente o resultado de Biot–Savart."),
    ("B17", "14:46.1", "lâmina cinza; K verde", "Segundo exemplo: uma lâmina"),
    ("B17", "14:52.5", "a lâmina vira linha; ⊙", "Vista de perfil, a corrente sai"),
    ("B17", "14:58.3", "setas magenta acima e abaixo", "Pela regra da mão direita, o campo aponta"),
    ("B17", "15:03.3", "retângulo atravessando a lâmina; L", "Escolhemos um caminho retangular"),
    ("B17", "15:07.3", "lados curtos", "Nos lados perpendiculares ao campo"),
    ("B17", "15:10.0", "lados longos; 2BL", "Nos dois lados paralelos, campo e caminho"),
    ("B17", "15:14.8", "faixa verde de largura L", "Agora calculamos a corrente envolvida."),
    ("B17", "15:17.9", "2BL = μ₀KL", "Esse mesmo comprimento aparece"),
    ("B17", "15:21.9", "B = μ₀K/2", "O resultado é:"),
    ("B18", "15:32.4", "hélice com traços verdes", "Terceiro caso: o solenoide ideal infinito."),
    ("B18", "15:35.3", "eixo axial, ẑ", "Pela simetria do modelo infinito ideal"),
    ("B18", "15:39.3", "«ainda nada sobre dentro ou fora»", "Mas ainda não vamos assumir"),
    ("B18", "15:51.0", "primeiro retângulo, todo fora", "Primeiro escolhemos um retângulo completamente externo."),
    ("B18", "15:56.4", "lados verticais", "Os lados transversais não contribuem."),
    ("B18", "16:01.3", "B(a)L − B(b)L = 0", "A lei de Ampère mostra então"),
    ("B18", "16:11.1", "B(s) → 0 quando s → ∞", "Agora usamos a condição física no infinito."),
    ("B18", "16:14.4", "B_fora = 0", "Portanto, para o solenoide infinito ideal, o campo externo é nulo."),
    ("B18", "16:24.1", "segundo retângulo, um lado dentro", "Só agora usamos um segundo caminho."),
    ("B18", "16:26.4", "só o lado de dentro contribui", "O trecho externo não contribui"),
    ("B18", "16:32.2", "espiras 1, 2, 3, 4; I_enc = (nL)I", "Se existem \\(n\\) espiras por unidade de comprimento"),
    ("B18", "16:35.3", "BL = μ₀(nL)I", "Substituindo na lei de Ampère"),
    ("B18", "16:39.7", "B_dentro = μ₀nI", "O campo interno é igual"),
    ("B18", "16:52.1", "solenoide finito (esquema)", "Num solenoide real e finito"),
    ("B19", "17:01.5", "toroide; traços nas espiras", "Nosso último exemplo é o toroide."),
    ("B19", "17:08.8", "vista de cima; B = B(s) φ̂", "Pela simetria do toroide ideal"),
    ("B19", "17:16.6", "seção; a e b; ⊙ interna, ⊗ externa", "Na seção mostrada"),
    ("B19", "17:19.0", "seção; a e b; ⊙ interna, ⊗ externa", "Existem três regiões."),
    ("B19", "17:21.6", "amperiano em s < a", "Primeiro, o vazio central."),
    ("B19", "17:25.2", "amperiano entre a e b", "Agora escolhemos um caminho dentro da região"),
    ("B19", "17:28.8", "B(2πs) = μ₀NI", "Portanto, a corrente envolvida vale"),
    ("B19", "17:35.3", "amperiano em s > b", "Finalmente, considere um caminho além"),
    ("B19", "17:38.3", "B(2πs) = μ₀(NI − NI) = 0", "A superfície é atravessada"),
    ("B19", "17:44.8", "gráfico; ponto branco", "O gráfico reúne as três regiões:"),
    ("B20", "18:09.4", "painéis ELETRO × MAGNETOSTÁTICA", "Agora podemos enxergar a estrutura completa."),
    ("B20", "18:13.0", "∇×E = 0; ∇×B = μ₀J", "Na magnetostática, o divergente do campo magnético é zero."),
    ("B20", "18:16.9", "legenda «campos que não variam no tempo»", "Esses qualificadores são importantes."),
    ("B21", "18:26.5", "quatro ícones", "Então, se você quiser guardar"),
    ("B21", "18:34.1", "«simetria → caminho → circulação»", "Reconheça a fonte."),
    ("B22", "18:42.9", "título; ∇·B = 0", "Mas ainda ficou uma última pergunta."),
    ("B22", "18:46.8", "legenda «qualquer rotacional tem divergente zero»", "Existe.\n"),
    ("B22", "18:55.8", "B = ∇×A; potencial vetor", "Isso sugere representar"),
    ("B23", "19:01.8", "marca do Parallax Lab", "Se esse vídeo te ajudou"),
]

pos = []
cur = 0
for u in U:
    i = body.find(u[3], cur)
    assert i >= 0, u
    pos.append(i)
    cur = i
assert body[:pos[0]].strip() == ""
chunks = [body[pos[k]:(pos[k + 1] if k + 1 < len(pos) else len(body))].strip() for k in range(len(U))]


def words(t):
    t = re.sub(r"\\\(.*?\\\)", "x", t).replace("**", "")
    return len(re.findall(r"[\wÀ-ÿ'’]+", t))


anch = [T(u[1]) for u in U]
rows = []
final = 0.0
for k, u in enumerate(U):
    nxt = anch[k + 1] if k + 1 < len(U) else TOTAL
    win = max(nxt - anch[k], 0.0)
    w = words(chunks[k])
    v = w / 2.8
    rows.append((u, w, v, win, final, chunks[k]))
    final += max(v, win)

out = []
out.append("# yt_0008 — Remapeamento da narração revisada (GPT) nas âncoras do preview V6\n")
out.append("Fonte da fala: `narracao_revisada_gpt.md` (inalterada). Âncoras: início de cada evento da cena, relógio do mp4 `YT0008Ampere_preview_v6.mp4` (19:12,9; ±2 s), levantado em `renders/tempos/log_tempos.json`.")
out.append("Voz estimada a 2,8 palavras/s. **Janela** = tempo de animação até a próxima âncora. **Segurar** = quanto a animação precisa esperar para a voz terminar (voz − janela). **Início final** = onde a unidade começa no vídeo remapeado (cumulativo: cada unidade dura o maior entre a voz e a janela). Unidades com janela 0 não têm animação própria: seguem a anterior.\n")
out.append("| Bloco | Âncora (V6) | Na tela | Início da unidade (fala) | Palavras | Voz (s) | Janela (s) | Segurar (s) | Início final |")
out.append("|---|---|---|---|---:|---:|---:|---:|---|")
tot_hold = 0.0
for (u, w, v, win, fin, ch) in rows:
    hold = max(0.0, v - win)
    tot_hold += hold
    first = ch.replace("\n", " ")[:55]
    out.append(f"| {u[0]} | {u[1]} | {u[2]} | {first}… | {w} | {v:.1f} | {win:.1f} | {hold:.1f} | {F(fin)} |")
tw = sum(r[1] for r in rows)
out.append("")
out.append(f"**Totais:** {tw} palavras de fala · voz ≈ {F(tw / 2.8)} · animação {F(TOTAL)} · soma das esperas ≈ {F(tot_hold)} · vídeo remapeado ≈ **{F(final)}**.\n")

byb = collections.OrderedDict()
for (u, w, v, win, fin, ch) in rows:
    d = byb.setdefault(u[0], [0, 0.0, 0.0])
    d[0] += w
    d[1] += v
    d[2] += max(0.0, v - win)
out.append("## Resumo por bloco\n")
out.append("| Bloco | Palavras | Voz | Segurar (soma) |")
out.append("|---|---:|---|---:|")
for b, d in byb.items():
    out.append(f"| {b} | {d[0]} | {F(d[1])} | {d[2]:.0f} s |")
io.open(D + r"\narracao_ancoras.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("unidades", len(U), "palavras", tw, "voz", F(tw / 2.8), "final", F(final), "esperas", F(tot_hold))
for b, d in byb.items():
    print(b, d[0], F(d[1]), "espera", round(d[2]))
