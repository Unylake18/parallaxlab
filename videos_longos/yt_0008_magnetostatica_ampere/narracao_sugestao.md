# yt_0008 (5.3) — Divergente, rotacional e lei de Ampère: sugestão de narração (v1, para fechar com o GPT antes do TTS)

Status: **sugestão para revisão. Voz não gerada, sem audio tags.** Depois de aprovada, vira `texto_narracao.txt` e a cópia com tags (`narracao_tags.md`) pela skill `gerar-narracao`.
Base de tempo: o preview silencioso `renders/preview/YT0008Ampere_preview_v6.mp4` (19:12,9, 960×540, 15 fps, cor padronizada). Cada tempo é o **início** de um evento (legenda, título, equação ou checkpoint), registrado por um levantamento externo do relógio da própria cena (`renders/tempos/log_tempos.json`; versão legível em `log_legivel.txt`) e convertido para o relógio do mp4 (±2 s; as juntas dos cinco trechos do preview somam 15 s a mais que o relógio de código).
Princípio (igual ao 5.1, ao 5.2 e aos vídeos de Gauss): **a voz explica o porquê; o Manim mostra o como.** A fala não lê a álgebra: diz o que cada passo quer, de onde vem cada termo e o que o resultado significa. **O vídeo se molda à voz** (remapeamento por âncoras): este roteiro é mais longo que a animação, e isso é esperado. No fim há a estimativa por bloco e a lista dos pontos em que a animação precisa segurar.

Arquitetura: gancho (do 5.2 para o 5.3) → o paradoxo do fio (campo curvo, rotacional nulo) → o rotacional como medida local (a sonda) → laço local e laço global → o divergente como fluxo → divergente de B a partir de Biot–Savart → os dois nablas e a continuidade → rotacional de B a partir de Biot–Savart → o delta de Dirac e o primeiro termo → por que o segundo termo some → fio de raio finito → região externa → limite filamentar → da lei local à lei sobre superfícies → Stokes e a lei de Ampère → verdadeira não é o mesmo que útil → as quatro aplicações (fio, lâmina, solenoide, toroide) → eletrostática × magnetostática → síntese → gancho (o potencial vetor) → CTA.

Retomadas dos vídeos anteriores (a fala usa exatamente estas): **5.1** (força de Lorentz: o que o campo faz com uma carga), **5.2** (Biot–Savart: como calcular o campo de uma corrente), **lei de Gauss** (fluxo por uma superfície fechada e carga dentro), **divergente e rotacional do campo eletrostático** (o divergente como fluxo por volume, o rotacional como circulação por área, a roda de pás, os teoremas de Stokes e da divergência).

## Como falar as grandezas (regra: pelo nome, nunca só pela letra)

| Na tela | Na fala |
|---|---|
| **B** | **o campo magnético** (1ª vez: "que na tela aparece como B em negrito") |
| **J** | **a densidade de corrente, que é corrente por área** (ampère por metro quadrado) |
| I, I_enc | **a corrente**; **a corrente encerrada**, a que atravessa a superfície |
| K | **a densidade superficial de corrente: corrente por largura**, em ampère por metro |
| ∇×**B**, ∇·**B** | **o rotacional de B** (1ª vez: "nabla cruz B"); **o divergente de B** ("nabla ponto B") |
| ∇, ∇′ | **nabla**, que deriva em relação ao observador; **nabla linha**, que deriva em relação à fonte |
| μ₀ | **mi zero, a permeabilidade magnética do vácuo** |
| s | **a distância até o eixo do fio** |
| φ̂, B_φ, ẑ | **o vetor unitário que dá a volta no fio**; **a componente do campo que dá a volta**; **o vetor unitário ao longo do fio** |
| A, ∂A, **n̂** | **a área da sonda**; **a borda da sonda**; **a normal da sonda**, dada pela regra da mão direita |
| dℓ, d**a**, S, V, C | **um pedacinho do caminho, orientado**; **o elemento de área orientado**; **a superfície**; **o volume**; **o caminho fechado** |
| Φ_B | **o fluxo magnético** |
| **r**, **r′**, **R**, R | **a posição do observador**; **a posição da fonte** (a linha marca a fonte); **o vetor separação, da fonte ao observador**; **a distância entre os dois** |
| **F** | **o vetor F, o vetor separação dividido pela distância ao cubo** (não é força nem campo magnético: é uma abreviatura geométrica) |
| dτ′, δ³ | **o elemento de volume da fonte**; **o delta de Dirac em três dimensões** |
| ρ | **rô, a densidade de carga** |
| a, b | fio: **o raio**; solenoide: **as distâncias dos dois lados do retângulo ao eixo**; toroide: **o raio interno e o raio externo** |
| C (constante) | **a constante de integração** (não confundir com o caminho C: avisar) |
| L, n, N | **o comprimento do lado do retângulo** (na lâmina: **a largura que o caminho cobre**); **espiras por comprimento**; **número total de espiras** |
| **A** (final) | **o potencial vetor magnético** (não confundir com a área A da sonda) |

Operações por extenso ("vezes", "dividido por", "ao quadrado", "igual a", "mais", "menos"). Funções: "integral de … sobre …", "derivada de … em relação a …", "limite quando … tende a zero". Letra só quando a tela aponta e o símbolo é novo.

Evitar: dizer "o campo é zero" quando o que é zero é o rotacional (este vídeo existe por causa dessa diferença); chamar o vetor F de força ou de campo magnético; chamar o delta de "função" sem dizer que é um pico infinitamente fino; dizer "uniforme" para a célula pequena (é **aproximadamente** uniforme); dizer que os traços verdes são a velocidade das cargas (são marcas convencionais); atribuir à lei de Ampère o campo nulo fora do solenoide (vem da lei **e** da condição no infinito); chamar de "lei de Ampère" o resultado do B03 (ali o valor vem de Biot–Savart).

---

## B00 — Do 5.2 para o 5.3: o campo tem estrutura (0:00–0:20)

| Tempo | Na tela | Fala |
|---|---|---|
| 0:00.0 | tema "Eletromagnetismo · Magnetostática" | Fala, pessoal! Bem-vindos de volta ao Parallax Lab. No primeiro vídeo desta série, vimos o que o campo magnético faz com uma carga em movimento. No segundo, aprendemos a calcular o campo de uma corrente com a lei de Biot–Savart. Hoje a pergunta é outra: que estrutura esse campo tem? |
| 0:02.0 | fio de aço, traços verdes subindo, seta de I | Aqui está um fio longo, retilíneo, com uma corrente elétrica, que na tela aparece como I. Os traços verdes se movem, mas o fio fica parado: eles só indicam o sentido convencional da corrente. |
| 0:05.6 | anel magenta em volta do fio | Essa corrente cria em volta do fio um campo magnético, que na tela aparece como B em negrito. As linhas são círculos que envolvem o fio, e o sentido vem da regra da mão direita. |
| 0:07.2 | caixa "J → Biot–Savart → B" | Resumindo: a densidade de corrente, J, entra na lei de Biot–Savart, e sai o campo magnético. |
| 0:11.4 | o anel se repete em três alturas | Esse padrão se repete em qualquer altura: como o fio é infinito, nada distingue um ponto do eixo de outro. |
| 0:14.1 | caixa "B → ?" | Agora a pergunta se inverte. Dado o campo, o que a geometria dele revela? |
| 0:17.6 | título "O que a geometria de B revela?" | Linhas que dão a volta no fio... será que isso quer dizer que o campo gira? Vamos descobrir. |

*Por quê:* liga 5.1 (efeito), 5.2 (causa) e 5.3 (estrutura). "Estrutura" prepara os dois operadores do vídeo: divergente (o que sai de um volume) e rotacional (o quanto circula em torno de um ponto). A pergunta final planta a ideia do B01: linha curva não implica rotacional diferente de zero.

## B01 — O paradoxo do fio (0:20–1:17)

| Tempo | Na tela | Fala |
|---|---|---|
| 0:20.7 | vista de cima: o fio vira um ponto (⊙); círculo magenta | Para ver como o campo muda com a distância, vamos olhar o fio de cima. Visto assim, o fio é um ponto, e o símbolo indica que a corrente sai da tela, na nossa direção. O campo é um círculo em volta dele. |
| 0:27.5 | ponto P, raio s, B tangente | Escolhe um ponto, P, a uma distância do eixo que na tela aparece como s. Ali, o campo é tangente ao círculo de raio s: na direção que dá a volta no fio, que a gente escreve como phi chapéu. |
| 0:28.2 | B = μ₀I/(2πs) φ̂ | O valor vem de Biot–Savart: mi zero vezes a corrente, dividido por dois pi vezes s. Mi zero é a permeabilidade magnética do vácuo. |
| 0:32.2 | vetores em raios diferentes, mais curtos longe | Quanto mais longe do fio, mais curto o vetor: o módulo cai com um sobre s. |
| 0:35.9 | título do rotacional; (∇×B)_z = (1/s) d/ds (s B_φ) | Agora a pergunta central: esse campo tem rotacional? O rotacional, nabla cruz B, mede a tendência de o campo girar em torno de um ponto, como a roda de pás do vídeo sobre divergente e rotacional do campo elétrico. Em coordenadas cilíndricas, a parte ao longo do fio é: um sobre s, vezes a derivada, em relação a s, de s vezes a componente do campo que dá a volta. |
| 0:40.9 | entra o valor de Biot–Savart | Vamos pôr o valor de Biot–Savart no lugar dessa componente: mi zero vezes a corrente, dividido por dois pi s. |
| 0:45.4 | o s que multiplica corta o s do denominador | Dentro do parêntese, o s que multiplica cancela o s que divide. |
| 0:47.3 | (μ₀I/2π) dentro da derivada | Sobra mi zero vezes a corrente, sobre dois pi: uma constante, sem s nenhum. |
| 0:50.1 | P se afasta; leituras s/s₀, B/B₀ e o produto | Dá para ver no desenho. Chama de s zero a distância inicial, e de B zero o campo nela. Afasta o ponto P: a distância sobe, o campo cai na mesma proporção, e o produto das duas coisas fica sempre igual a um. |
| 1:01.1 | (∇×B)_z = (1/s)·0 | E a derivada de uma constante é zero. |
| 1:04.6 | (∇×B)_z = 0 | Então o rotacional, ao longo do fio, é zero. |
| 1:06.8 | legenda "só componente φ…" | As outras componentes também são zero, porque o campo só dá a volta e só depende de s. |
| 1:09.4 | ∇×B = 0 (s > 0) | Em todo ponto fora do fio, o rotacional do campo magnético é zero. |
| 1:12.2 | legenda "Linhas de campo curvas e, mesmo assim, rotacional zero" | Parece estranho: as linhas dão a volta no fio, mas o rotacional é zero. A lição é que linha curva não significa rotacional diferente de zero. Rotacional é uma conta feita ponto a ponto. Vamos medi-lo de forma mais concreta. |

*Por quê:* o "paradoxo" organiza o vídeo: B_φ ∝ 1/s tem rotacional nulo fora do eixo (s·B_φ constante), mas a circulação ao redor do fio vale μ₀I (B03). A resolução (rotacional concentrado no eixo) vem no B12. As leituras adimensionais s/s₀ e B_φ/B₀ eliminam o problema de unidades. A fala diz "rotacional zero", nunca "campo zero".

## B02 — O rotacional como medida local: a sonda (1:17–2:08)

| Tempo | Na tela | Fala |
|---|---|---|
| 1:17.6 | título "Rotacional: uma medida local" | Para entender esse zero, vamos transformar o rotacional numa medida que uma sonda faz. |
| 1:22.6 | laço pequeno em P, normal n̂, rótulo ∂A | Imagina um laço minúsculo em torno de P. Ele encerra uma área, A; a borda dele é a curva que a gente chama de borda de A; e a normal dele, n chapéu, é o vetor unitário perpendicular, dado pela regra da mão direita. |
| 1:25.2 | (∇×B)·n̂ = lim (1/A) ∮ B·dℓ | A definição é esta: a componente do rotacional na direção da normal é o limite, quando a área tende a zero, da circulação do campo ao longo da borda, dividida pela área. Circulação é somar o campo vezes um pedacinho do caminho, ao longo de um caminho fechado. É a mesma ideia da roda de pás. |
| 1:31.7 | legenda "Por que zero aqui?" | Por que dá zero, se o campo dá a volta no fio? Vamos deformar a sonda em dois arcos e dois raios, e olhar de cima. |
| 1:38.3 | setor; arco curto B forte, arco longo B fraco, raios B ⊥ dℓ | Nos dois trechos radiais, o campo é perpendicular ao caminho: não contribuem. Sobram os arcos. Perto do fio, o campo é mais forte, mas o arco é mais curto. Longe, mais fraco, mas mais longo. |
| 1:38.9 | ∮B·dℓ = (sB_φ)_fora Δφ − (sB_φ)_dentro Δφ | O comprimento do arco é a distância ao eixo vezes o ângulo. Então cada arco contribui com distância vezes campo, vezes o ângulo, e eles entram com sinais opostos. |
| 1:42.6 | ∮B·dℓ = 0 | Como distância vezes campo é igual nos dois arcos, as duas parcelas se cancelam: circulação zero. |
| 1:51.1 | a sonda gira; n̂ gira junto | Mas o rotacional é um vetor, com três componentes, e cada orientação da normal mede uma delas. Então a gente gira a sonda. |
| 1:51.7 | três componentes de (∇×B) | Normal ao longo do fio: zero. Normal para fora: zero. Normal na direção que dá a volta: zero. |
| 2:01.8 | legenda "Três orientações, três componentes, todas nulas" | O vetor rotacional, nesse ponto, é o vetor nulo. As linhas curvas não têm giro local nenhum. |

*Por quê:* a sonda usa a definição do vídeo do campo elétrico (limite da circulação por área). A deformação em setor mostra que o zero vem de um cancelamento exato (s·B_φ constante), não de o campo ser fraco. A sonda só prova no ponto onde está; a conclusão geral é a álgebra do B01.

## B03 — Do laço local ao laço global (2:08–2:46)

| Tempo | Na tela | Fala |
|---|---|---|
| 2:08.2 | título "Do laço local ao laço global" | Agora a pergunta inversa: se cada laço minúsculo dá zero, o que acontece com um laço grande? |
| 2:11.7 | ∮B·dℓ = 0; laço pequeno | Começa com o laço fora do fio: circulação zero. Vamos aumentá-lo e levar o centro até o eixo. |
| 2:13.4 | o laço cresce; I_enc = 0 | Enquanto o fio fica de fora, nenhuma corrente atravessa a superfície do laço: a corrente encerrada é zero, e a circulação também. |
| 2:19.3 | o laço passa pelo eixo; "indefinida" | No instante em que o laço passa exatamente sobre o fio, o campo diverge no eixo, e a circulação não está definida. Valem o que acontece antes e o que acontece depois. |
| 2:22.3 | I_enc = I; ∮ = μ₀I | Depois que o fio fica dentro, a corrente atravessa a superfície, e a circulação passa a valer mi zero vezes a corrente. |
| 2:28.3 | legenda "qualquer que seja o laço" | E esse valor não depende da forma do laço. |
| 2:31.5 | círculo centrado; B_φ(s) · 2πs | Confere com o círculo centrado: o campo tem o mesmo valor em todo ponto, na direção do caminho. A circulação é esse valor vezes dois pi s. |
| 2:32.2 | B_φ(s) · 2πs = μ₀I; nota "calculado com Biot–Savart" | Com o campo de Biot–Savart, dá exatamente mi zero vezes a corrente. Repara: isso foi calculado com Biot–Savart. Ainda não estou chamando de lei de Ampère. |
| 2:37.8 | legenda "Rotacional zero fora do fio, circulação ≠ 0: como?" | E aqui está o problema. Todo laço pequeno fora do fio dá zero, mas o laço grande dá mi zero vezes a corrente. Como somar zeros dá um número diferente de zero? |
| 2:42.3 | zoom no eixo; "?" | A diferença só pode estar escondida num lugar onde ainda não olhamos: o eixo. Guarda essa ideia. |

*Por quê:* geometria, equação e nota dizem a mesma coisa (V4 do QA), e o laço sobre o fio é tratado como singular. "Lei de Ampère" só aparece no B14. A pergunta final é respondida no B12.

## B04 — O divergente como fluxo por um volume (2:46–3:39)

| Tempo | Na tela | Fala |
|---|---|---|
| 2:46.4 | título "Outra sonda: um volume fechado" | Agora outra pergunta: o campo nasce ou termina em algum lugar? Para isso, outra sonda: um volume fechado. |
| 2:49.8 | caixa transparente em meio a linhas retas de B | De perto, numa região pequena, o campo do fio é aproximadamente uniforme: linhas quase retas e paralelas. Envolve essa região com uma caixa fechada. |
| 2:53.3 | normais para fora | Cada face tem uma normal, um vetor unitário que aponta para fora do volume. |
| 2:56.2 | face de entrada; −Φ_B | Na face por onde o campo entra, ele aponta contra a normal, e o fluxo magnético sai negativo. |
| 2:59.7 | face de saída; +Φ_B | Na face por onde sai, o campo acompanha a normal, e o mesmo fluxo aparece positivo. |
| 3:02.4 | as outras quatro faces | Nas outras quatro faces, o campo corre paralelo: fluxo zero. |
| 3:05.1 | −Φ_B + Φ_B = 0 | O total é menos o fluxo, mais o fluxo: zero. |
| 3:08.1 | ∮_S B·da = 0 | Em símbolos: a integral do campo vezes o elemento de área, sobre a superfície fechada, é zero. |
| 3:10.5 | legenda "Lei de Gauss para o magnetismo" | Esse resultado é a lei de Gauss para o magnetismo. Lembra da lei de Gauss do campo elétrico? Lá, o fluxo dá a carga dentro dividida por epsilon zero. Aqui, o fluxo é sempre zero. |
| 3:11.1 | ∇·B = lim (1/V) ∮ B·da | Encolhe o volume até um ponto: o fluxo por volume, no limite, é o divergente, nabla ponto B, como no vídeo do campo elétrico. |
| 3:15.0 | ∇·B = 0 | Como o fluxo é sempre zero, o divergente do campo magnético é zero em todo ponto. |
| 3:25.2 | carga com E saindo; ∮E·da = Q/ε₀ | Compara com uma carga: as linhas do campo elétrico saem pela superfície, e o fluxo é positivo. A carga é fonte do campo elétrico. |
| 3:29.5 | legenda "para B não existe fonte nem sumidouro" | Para o campo magnético, não há fonte nem sumidouro, no eletromagnetismo clássico. Por isso as linhas se fecham, ou vão ao infinito. |

*Por quê:* mesmo caminho do vídeo anterior (fluxo por volume → limite). O contraste com a carga marca a diferença entre E e B sem entrar em monopolos. A caixa só vale numa região pequena: a fala diz "aproximadamente uniforme".

## B05 — Divergente de B a partir de Biot–Savart (3:39–4:57)

| Tempo | Na tela | Fala |
|---|---|---|
| 3:43.3 | região verde; r′ (fonte) e r (observador); vetor R | Até aqui, o divergente nulo veio de um desenho. Agora vamos mostrar que sai da própria lei de Biot–Savart, para qualquer distribuição de corrente. Imagina uma região onde a corrente está espalhada, com densidade de corrente J. Um ponto dentro dela é a fonte, na posição r linha. O observador está fora, na posição r. |
| 3:47.1 | B(r) = (μ₀/4π) ∫ J(r′) × R/R³ dτ′ | Biot–Savart, para volumes: o campo é mi zero sobre quatro pi, vezes a integral, sobre toda a corrente, da densidade de corrente na fonte vezes o vetor separação dividido pela distância ao cubo, vezes o elemento de volume da fonte. |
| 3:51.0 | legenda do elemento de volume | Esse d tau linha é o elemento de volume da região-fonte: cada pedacinho de volume traz uma densidade de corrente, e a integral soma todos. |
| 3:51.7 | R = r − r′; F ≡ R/R³ | Para simplificar: o vetor separação é a posição do observador menos a da fonte. E o vetor F, que não é força nenhuma, é só o vetor separação dividido pela distância ao cubo. |
| 3:54.7 | cores: r ciano, r′ verde | As cores ajudam: o que é do observador, a posição r e o nabla, em ciano; o que é da fonte, em verde. |
| 3:58.8 | B(r) = (μ₀/4π) ∫ J(r′) × F dτ′ | Com F, o campo é mi zero sobre quatro pi, vezes a integral de J vezes F. |
| 4:01.8 | legenda "Tome o divergente dos dois lados" | Tira o divergente dos dois lados. |
| 4:05.1 | ∇ entra na integral | O nabla deriva em relação ao observador, e a integral percorre a fonte: variáveis diferentes. Por isso o nabla entra na integral. |
| 4:10.2 | ∇·(A×C) = C·(∇×A) − A·(∇×C) | Dentro aparece o divergente de um produto vetorial. Existe uma identidade para isso: o divergente de A vetorial C é C escalar o rotacional de A, menos A escalar o rotacional de C. |
| 4:12.6 | legenda "se abre em dois termos" | Aplicando com J no lugar de A e F no lugar de C, o divergente se abre em dois termos. |
| 4:14.8 | F·(∇×J) − J·(∇×F) | F escalar o rotacional de J; menos J escalar o rotacional de F. |
| 4:23.6 | ∇×J(r′) = 0 | No primeiro, o nabla deriva em relação ao observador, e J só depende da fonte. Quando o observador se mexe, J não muda: derivada zero. É por serem variáveis independentes, não por uma propriedade física. |
| 4:28.9 | ∇·B = −(μ₀/4π) ∫ J·(∇×F) dτ′ | Sobra o segundo termo, com o sinal de menos. |
| 4:36.6 | legenda "1/R diminui…" | Agora uma propriedade de F: um sobre R diminui quando a gente se afasta da fonte, e F aponta exatamente para onde isso diminui... |
| 4:37.3 | F = R/R³ = −∇(1/R) | ... com um sinal de menos. F é menos o gradiente de um sobre R. F é um gradiente. |
| 4:40.4 | legenda "rotacional de um gradiente é zero" | E o rotacional de um gradiente é sempre zero, para qualquer função. |
| 4:41.1 | ∇×F = −∇×∇(1/R) = 0 | Logo, o rotacional de F é zero. |
| 4:45.9 | ∇·B = −(μ₀/4π) ∫ J·0 dτ′ | O segundo termo vira J escalar zero: zero. |
| 4:49.7 | ∇·B = 0 | E o divergente de B é zero. |
| 4:52.3 | legenda "Da própria lei de Biot–Savart" | Então ∇·B = 0 não é suposição: sai da lei de Biot–Savart. |

*Por quê:* prova formal do B04. Cuidado: duas razões diferentes para dois zeros: (1) ∇×J(r′) = 0 porque as variáveis são independentes (não é continuidade); (2) ∇×F = 0 porque F é gradiente. F (violeta na tela) é geometria, não campo nem força.

## B06 — Dois pontos, dois operadores (4:57–5:49)

| Tempo | Na tela | Fala |
|---|---|---|
| 5:00.3 | diagrama; observador ciano se move | Antes do rotacional, uma ideia decisiva: a diferença entre nabla e nabla linha. O nabla deriva movendo o observador, com a fonte parada. |
| 5:00.7 | ∇ ↔ r | Nabla é a derivada em relação à posição do observador. |
| 5:08.1 | o observador anda; R e F mudam; J(r′) não | Anda com o observador: o vetor separação e o vetor F mudam. Mas a densidade de corrente na fonte não muda. |
| 5:08.8 | ∇ J(r′) = 0 · "variáveis independentes" | Então nabla aplicado em J, na fonte, dá zero. A razão é só essa: variáveis independentes. |
| 5:13.2 | ∇′ ↔ r′; a fonte anda | Agora o contrário: nabla linha deriva em relação à fonte. Anda com a fonte pela região: aí a densidade de corrente muda de um ponto para outro. |
| 5:22.3 | linhas de corrente verdes com traços | Em magnetostática, a densidade de corrente não muda no tempo. Os traços mostram cargas percorrendo as linhas de corrente, mas o campo de densidade de corrente é fixo. Cada linha verde mostra a direção de J em cada ponto. |
| 5:26.1 | quadradinho sobre uma linha | Escolhe uma célula tão pequena que, dentro dela, J seja praticamente o mesmo. E amplia. |
| 5:32.5 | célula ampliada; J grande | Dentro da célula ampliada, J é aproximadamente uniforme. Os traços andam sobre as linhas; as setas grandes não giram. |
| 5:35.3 | normais para fora | Cada face tem uma normal para fora. A corrente entra por uma face e sai pela oposta. |
| 5:38.3 | "entra: −Φ_J", "sai: +Φ_J"; ∇′·J = 0 | O que entra é igual ao que sai: nenhuma carga se acumula. Então o divergente de J, em relação à fonte, é zero. |
| 5:41.3 | legenda "São afirmações diferentes" | São duas afirmações diferentes. A de cima, nabla aplicado em J igual a zero, é sobre variáveis. A de baixo, nabla linha ponto J igual a zero, é física: a carga não se acumula. |

*Por quê:* mensagem protegida pelo QA. A célula é ampliada por zoom de câmera; os traços andam sobre as linhas de corrente; J (campo) é estacionário.

## B07 — O rotacional de B a partir de Biot–Savart (5:49–6:33)

| Tempo | Na tela | Fala |
|---|---|---|
| 5:51.7 | B(r) = (μ₀/4π) ∫ J(r′) × F dτ′ | Agora o rotacional. Começa do mesmo lugar: o campo como a integral de J vezes F. |
| 5:53.9 | legenda "rotacional dos dois lados" | Tira o rotacional dos dois lados. Como antes, o operador entra na integral. |
| 6:00.2 | ∇×(A×C) = A(∇·C) − C(∇·A) + (C·∇)A − (A·∇)C | Dentro, o rotacional de um produto vetorial, que tem quatro termos: A vezes o divergente de C; menos C vezes o divergente de A; mais "C escalar nabla" aplicado a A; menos "A escalar nabla" aplicado a C. Os dois últimos derivam um campo na direção do outro. |
| 6:05.5 | quatro termos com J e F | Com J no lugar de A e F no lugar de C: J vezes o divergente de F; menos F vezes o divergente de J; mais "F escalar nabla" aplicado a J; menos "J escalar nabla" aplicado a F. |
| 6:13.7 | legenda "Dois termos derivam J em relação a r" | Dois desses termos derivam J em relação ao observador: o segundo e o terceiro. |
| 6:16.1 | ∇·J(r′)=0; (F·∇)J(r′)=0 | Mas J, na fonte, não muda quando o observador se mexe. Os dois são zero. |
| 6:18.2 | os termos são riscados | De novo: por variáveis independentes, não por continuidade. |
| 6:22.5 | dois termos restantes | Sobram dois: J vezes o divergente de F, e menos "J escalar nabla" aplicado a F. |
| 6:28.1 | duas integrais, (1) e (2) | Em duas linhas: mi zero sobre quatro pi, vezes a integral de J vezes o divergente de F; menos mi zero sobre quatro pi, vezes a integral do operador "J escalar nabla" aplicado a F. Vamos tratar cada uma. |

*Por quê:* a fala diz de onde cada termo nasce e por que dois somem (mesma razão do B05/B06). O diagrama recua e a matemática cresce; "(1)" e "(2)" ficam dentro do painel.

## B08 — O primeiro termo: o delta de Dirac (6:33–7:46)

| Tempo | Na tela | Fala |
|---|---|---|
| 6:38.4 | setas radiais; ∇·F = 0 (r ≠ r′) | Primeiro termo: o divergente de F. F aponta radialmente para fora da fonte, em todas as direções (a tela mostra oito). Atenção: não é campo magnético, é geometria da lei. O módulo de F cai com um sobre a distância ao quadrado. |
| 6:41.3 | pequena caixa longe da fonte | Longe da fonte, o que entra numa célula sai: divergente zero. |
| 6:44.9 | esfera em volta da fonte; ∮F·da = 4π | Mas numa esfera em volta da fonte: o módulo de F é um sobre R ao quadrado, a área é quatro pi R ao quadrado, o R ao quadrado cancela, e o fluxo dá quatro pi. |
| 6:47.1 | a esfera encolhe | E não depende do raio: encolha a esfera quanto quiser, dá sempre quatro pi. |
| 6:51.9 | legenda "Divergente zero fora da singularidade" | Então o divergente de F é zero em todo lugar, menos na fonte, onde está concentrado o fluxo quatro pi inteiro. |
| 6:52.6 | ∇·F = 4π δ³(r − r′) | Escreve-se com o delta de Dirac em três dimensões: um pico infinitamente fino, que vale zero em todo lugar menos num ponto, e cuja integral no espaço todo é um. |
| 6:56.7 | 4π δ³ dentro da integral | De volta ao primeiro termo: o quatro pi do delta multiplica J, dentro da integral. |
| 7:02.2 | os dois 4π se cancelam | E cancela com o quatro pi do denominador. |
| 7:02.9 | μ₀ ∫ J(r′) δ³ dτ′ | Sobra mi zero vezes a integral de J na fonte, vezes o delta, vezes o elemento de volume. |
| 7:05.9 | legenda "leve o observador para dentro" | Para olhar dentro da corrente, leva o observador para dentro da região. |
| 7:12.1 | pontos-fonte; cada um com J(r′) | Cada ponto da região é uma fonte possível, e cada um contribui com sua densidade de corrente. |
| 7:16.5 | pico sobre o observador; "esquema da delta 3D" | O delta é um pico centrado no observador. A figura é só um esquema: um pico de verdade, em três dimensões, não cabe numa tela. |
| 7:18.6 | pesos esmaecendo | Na integral, cada contribuição é multiplicada pelo delta: longe do pico, o peso é quase zero. |
| 7:22.8 | o pico se estreita | Estreitando o pico, as contribuições somem uma a uma, de fora para dentro. |
| 7:32.0 | uma única seta verde grande | Sobrevive uma só: a da fonte que coincide com o observador. |
| 7:35.5 | rótulo J(r) | E ela traz a densidade de corrente naquele ponto. |
| 7:36.1 | ∇×B = μ₀ J(r) − (μ₀/4π) ∫ (J·∇)F dτ′ | O primeiro termo virou mi zero vezes a densidade de corrente no próprio ponto. |
| 7:39.5 | legenda "Primeiro termo: μ₀ J(r)" | Em palavras: uma parte do rotacional de B, num ponto, é mi zero vezes a densidade de corrente que passa ali. |

*Por quê:* o payoff do delta (QA V5): observador fixo, fundo atenuado, e **uma** contribuição final legível. O pico é um esquema: a fala diz "esquema" e "pico infinitamente fino". Os dois quatro pi são cancelados no tempo certo. A analogia com Gauss: o fluxo de F é 4π, como o fluxo do campo de uma carga pontual.

## B09 — O segundo termo some (7:46–9:14)

| Tempo | Na tela | Fala |
|---|---|---|
| 7:48.9 | F = F(r − r′) | Falta o segundo termo. Para tratá-lo, uma propriedade de F: ele depende só da diferença entre a posição do observador e a da fonte. |
| 7:53.3 | observador e fonte juntos | Se mexermos observador e fonte juntos, no mesmo deslocamento, o vetor separação não muda. |
| 7:58.2 | observador se afasta de +dx; a fonte se aproxima | Afastar o observador de um pedacinho dx muda o vetor separação do mesmo jeito que aproximar a fonte desse pedacinho, no sentido oposto. |
| 8:02.4 | ∂F/∂x = −∂F/∂x′ | A derivada de F em relação a x, do observador, é menos a derivada em relação a x linha, da fonte. |
| 8:05.0 | legenda "Vale para cada coordenada" | E vale para x, y e z. |
| 8:05.7 | ∇F = −∇′F | Então nabla aplicado em F é menos nabla linha aplicado em F. |
| 8:08.5 | os dois nablas destacados | Troca: no segundo termo, o nabla que age em F vira menos nabla linha. |
| 8:11.0 | (J·(−∇′))F | O segundo termo já tinha um sinal de menos na frente. Agora ganha outro, dentro do parêntese. |
| 8:14.2 | legenda "Os dois sinais negativos se cancelam" | Menos com menos dá mais. |
| 8:14.9 | +(μ₀/4π)∫(J·∇′)F dτ′ | O segundo termo agora tem nabla linha, com sinal positivo. |
| 8:18.4 | legenda "Regra do produto" | Para cada componente de F, vale a regra do produto. |
| 8:19.1 | (J·∇′)F_i = ∇′·(F_iJ) − F_i(∇′·J) | O operador "J escalar nabla linha" aplicado a uma componente é o divergente de F_i vezes J, menos F_i vezes o divergente de J. |
| 8:22.2 | legenda "teorema da divergência" | Integrando no volume: o primeiro termo é a integral de um divergente. Pelo teorema da divergência, o mesmo do vídeo do campo elétrico, vira um fluxo por uma superfície que envolve a corrente. |
| 8:22.8 | duas parcelas: ∮_∞ F_i J·da′ e −∫ F_i(∇′·J) dτ′ | Duas parcelas: a de cima, um termo de superfície, numa superfície muito distante; a de baixo, menos a integral de F_i vezes o divergente de J. |
| 8:30.1 | superfície tracejada; "superfície distante: J = 0" | Primeira razão: a corrente é localizada. Na superfície distante, J é zero, e o termo de superfície some. A outra parcela fica na tela, esperando. |
| 8:30.8 | 0 no lugar do termo de superfície | A integral vale zero, menos a integral de F_i vezes o divergente de J. |
| 8:36.9 | célula ampliada de novo | Segunda razão: a mesma célula de antes. |
| 8:43.4 | J aproximadamente uniforme; traços | J é aproximadamente uniforme, e as cargas andam sobre as linhas. |
| 8:46.2 | normais para fora | A corrente entra por uma face e sai pela oposta. |
| 8:49.2 | entra/sai | O que entra é igual ao que sai. |
| 8:50.6 | legenda "Continuidade com ρ constante" | A equação da continuidade diz que o divergente de J é menos a derivada da densidade de carga no tempo. Em magnetostática, rô não muda. Então o divergente de J é zero. |
| 8:52.8 | ∫(J·∇′)F_i dτ′ = 0 − 0 = 0 | A integral dá zero menos zero: zero. Por duas razões diferentes: a corrente é localizada, e a carga não se acumula. |
| 8:58.1 | legenda "só agora, o segundo termo some" | Só agora o segundo termo some: com as duas razões, e nenhuma antes. |
| 8:58.7 | ∇×B = μ₀ J(r) + 0 | O rotacional de B é mi zero vezes J, mais zero. |
| 9:02.3 | ∇×B = μ₀ J | Ou seja: o rotacional do campo magnético é mi zero vezes a densidade de corrente. |
| 9:04.9 | legenda "A lei local da magnetostática" | Essa é a lei de Ampère na forma local: em cada ponto, o rotacional do campo é mi zero vezes a densidade de corrente que passa ali. |

*Por quê:* as duas razões do QA, em separado: (1) o termo de superfície no infinito é zero porque J é localizado; (2) ∇′·J = 0 por continuidade com densidade de carga constante. "Continuidade" só entra na segunda. A forma local ganha nome aqui; a integral, no B14.

## B10 — Um fio de verdade tem espessura (9:14–10:15)

| Tempo | Na tela | Fala |
|---|---|---|
| 9:18.2 | cilindro de aço; traços verdes; a e J | Até agora o fio era uma linha, mas um fio de verdade tem espessura. Imagina um cilindro de raio a, com densidade de corrente uniforme, em ampère por metro quadrado, ao longo do eixo. Fora dele, não há corrente. |
| 9:18.6 | J = J ẑ (s < a) | A densidade de corrente tem valor J, na direção do eixo, z chapéu, para pontos mais perto do eixo que o raio a. |
| 9:21.2 | anéis magenta | A simetria é a do fio fino: o campo dá a volta e só depende da distância ao eixo. |
| 9:21.9 | B = B_φ(s) φ̂ | O campo é a componente B fi, função de s, vezes o vetor unitário que dá a volta. |
| 9:25.0 | o cilindro gira para vista de cima | Para raciocinar com clareza, cortamos o fio e olhamos a seção de cima. |
| 9:32.4 | seção com ⊙; sonda dentro; leitura 1,00 μ₀J | Uma sonda pequena, inteira dentro do condutor, mede o rotacional por área, e a leitura é exatamente mi zero vezes J. Onde há corrente, o rotacional não é zero. |
| 9:36.6 | a sonda chega à borda; a leitura cai | Move a sonda até a borda: quando começa a sair, só parte dela está dentro, e a leitura cai continuamente. |
| 9:40.7 | sonda fora; leitura 0,00 | Fora do fio, a sonda mede zero. |
| 9:46.5 | gráfico B_φ(s); (1/s) d/ds (s B_φ) = μ₀J | Agora a conta. Dentro do fio: um sobre s, vezes a derivada de s vezes B fi, igual a mi zero J. O gráfico vai mostrar o campo em função da distância ao eixo, junto com a sonda. |
| 9:50.3 | d/ds (s B_φ) = μ₀ J s | Multiplica por s: a derivada de s B fi é mi zero J vezes s. |
| 9:53.9 | s B_φ = (μ₀J/2) s² + C | Integra em s: mi zero J sobre dois, vezes s ao quadrado, mais uma constante de integração, C, que ainda não sabemos. |
| 9:57.6 | B_φ = (μ₀J/2) s + C/s | Dividindo por s: mi zero J sobre dois vezes s, mais C sobre s. |
| 10:01.7 | "C/s → ∞" | Se C não for zero, quando s tende a zero esse termo explode: campo infinito no meio do fio. |
| 10:04.7 | legenda "Regularidade no eixo" | Para uma corrente espalhada, o campo no eixo é finito. Isso elimina o termo C sobre s: C vale zero. |
| 10:05.8 | B_φ = (μ₀J/2) s | Dentro do fio, o campo é mi zero J sobre dois, vezes s: cresce linearmente com a distância. |
| 10:08.1 | a reta nasce da origem | No gráfico, a reta nasce na origem e cresce até a fronteira do fio. |
| 10:10.8 | sonda e ponto andam juntos | A sonda e o ponto andam juntos: quanto mais longe do centro, maior o campo. |

*Por quê:* QA V5: a sonda inicial fica **inteira** dentro e dá 1,00·μ₀J pela geometria; na fronteira, valores intermediários. A constante C (integração) não é o caminho C: a fala avisa na primeira vez. O termo C/s explode no eixo sem curva parcial.

## B11 — Fora do fio (10:15–10:52)

| Tempo | Na tela | Fala |
|---|---|---|
| 10:16.8 | legenda "Fora, J = 0"; (1/s) d/ds (s B_φ) = 0 | Fora, a densidade de corrente é zero: um sobre s, vezes a derivada de s B fi, igual a zero. |
| 10:20.1 | s B_φ = C_ext | Derivada nula quer dizer constante: s B fi é uma constante fora do fio. Chamamos de constante externa, para não confundir com a de dentro. |
| 10:23.4 | B_φ = C_ext / s | O campo de fora é a constante externa dividida por s. |
| 10:25.5 | duas curvas tracejadas e uma cheia | A constante ainda é livre: cada valor dá uma curva do tipo constante sobre s. Qual é a certa? |
| 10:28.6 | legenda "A continuidade em s = a seleciona uma" | A resposta vem da fronteira: a continuidade em s igual a a seleciona uma. |
| 10:32.8 | a curva escolhida passa pelo ponto de dentro | Não há corrente superficial especial na fronteira: a corrente está toda espalhada no volume. Então o campo é contínuo ali, e a curva de fora precisa passar pelo ponto onde a reta termina. Só uma passa. |
| 10:35.0 | C_ext/a = (μ₀J/2) a | A constante externa dividida por a é mi zero J sobre dois vezes a. |
| 10:38.0 | C_ext = (μ₀J/2) a² | Então a constante externa é mi zero J sobre dois, vezes a ao quadrado. |
| 10:40.6 | legenda "I = J π a²" | A corrente total é J vezes a área da seção, pi a ao quadrado. |
| 10:41.2 | C_ext = μ₀ I / 2π | Substituindo, a constante é mi zero vezes a corrente, sobre dois pi, e não depende mais do raio. |
| 10:44.0 | B_φ = μ₀ I / (2π s) (s > a) | Fora do fio, o campo é o do fio fino: mi zero vezes a corrente, sobre dois pi s. |
| 10:46.7 | B ∝ s dentro, B ∝ 1/s fora | A sonda atravessa a fronteira: dentro, o campo cresce; depois, cai com um sobre s. O máximo está na superfície do fio. |

*Por quê:* a hipótese "sem corrente superficial singular em s = a" garante a continuidade de B_φ; vem numa frase. As curvas C/s surgem já nas posições finais; a escolhida ganha destaque e as outras somem. O campo de fora coincide com o do fio fino: bom teste de consistência.

## B12 — O rotacional concentrado no eixo (10:52–11:28)

| Tempo | Na tela | Fala |
|---|---|---|
| 10:56.5 | pilar verde; painel com a, J/J₀, I = 1,00 I₀ | Agora um experimento mental: comprimir o fio, mantendo a corrente fixa. O pilar verde mostra a densidade de corrente: altura é J, base é a área da seção, volume é a corrente. J zero e I zero são os valores iniciais. |
| 11:03.0 | o pilar fica alto e fino; pico "fora de escala" | Quando o raio diminui, a área encolhe, e a densidade sobe para manter a corrente. O campo de fora nem percebe. O pico do campo, na fronteira, sobe e se aproxima do eixo; quando passa do alto do gráfico, a tela avisa: pico fora de escala. A curva não é achatada. |
| 11:09.1 | legenda "cada vez mais estreita e mais intensa" | A região onde o rotacional não é zero fica cada vez mais estreita e mais intensa. |
| 11:12.4 | J → I δ(x) δ(y) ẑ | No limite, a corrente fica só sobre o eixo: densidade de corrente igual à corrente vezes um delta em x, vezes um delta em y, na direção do eixo. É um delta bidimensional. |
| 11:15.2 | legenda "um delta bidimensional com integral I" | A integral desse delta no plano é um, e a corrente total continua I. |
| 11:15.9 | ∇×B = μ₀ I δ(x) δ(y) ẑ | Na lei local: o rotacional é mi zero vezes a corrente, vezes os deltas, na direção do eixo. |
| 11:23.5 | laço grande envolvendo o eixo; laço pequeno fora | Agora o paradoxo se desfaz. Fora do eixo, laço pequeno dá zero. O laço grande envolve o eixo e dá mi zero vezes a corrente, porque todo o rotacional está concentrado ali. Zeros fora do eixo, mais uma contribuição infinita num ponto, podem dar um valor finito. |

*Por quê:* resposta do B03. Distingue o delta bidimensional da corrente (x e y) do delta tridimensional do B08. O pico cortado tem aviso, para não sugerir que a curva exibida valha a integral do delta.

## B13 — Da lei local a uma lei sobre superfícies (11:28–12:07)

| Tempo | Na tela | Fala |
|---|---|---|
| 11:32.3 | quatro fios (I₁ a I₄); ∇×B = μ₀J | Temos uma lei local, ponto a ponto. Mas, na prática, sabemos a corrente que passa por um circuito, não a densidade em cada ponto. Vamos transformar a lei local numa lei sobre uma superfície. |
| 11:34.5 | legenda "Some ela sobre uma superfície" | Como no vídeo do campo elétrico: uma lei local vira integral somando sobre uma região. |
| 11:37.0 | contorno C | Primeiro, um caminho fechado, C, com um sentido de percurso. |
| 11:42.3 | S nasce da borda | Depois, uma superfície S cuja borda é exatamente C. |
| 11:45.2 | mão direita; normais; da | As orientações se ligam pela regra da mão direita: dedos no sentido de C, polegar na normal de S. O elemento de área orientado, d a em negrito, segue essa normal. |
| 11:48.4 | legenda "Integre os dois lados sobre S" | Integra a lei local dos dois lados, sobre a superfície. |
| 11:49.1 | ∫_S (∇×B)·da = μ₀ ∫_S J·da | À esquerda, a integral do rotacional vezes o elemento de área. À direita, mi zero vezes a integral de J vezes o elemento de área. |
| 11:53.4 | legenda "J·da só não é zero onde a corrente fura S" | À direita, só conta onde a corrente fura a superfície, e o sinal vem do sentido: com a normal, positivo; contra, negativo. |
| 11:55.5 | ∫ J·da = I₁ + I₂ − I₃; I₄ não fura | Na figura, o primeiro e o segundo fio atravessam no sentido da normal; o terceiro, no contrário; o quarto passa fora e não conta. A integral é o primeiro mais o segundo menos o terceiro. |
| 12:01.0 | ∫ J·da = I_enc | É a corrente que atravessa a superfície, com sinal: a corrente encerrada. |
| 12:03.9 | ∫ (∇×B)·da = μ₀ I_enc | A integral do rotacional de B sobre a superfície é mi zero vezes a corrente encerrada. |

*Por quê:* troca "J local" por "corrente encerrada" com sinal; o fio que não fura S não entra. "Lei de Ampère" ainda não aparece.

## B14 — Stokes e a lei de Ampère (12:07–13:14)

| Tempo | Na tela | Fala |
|---|---|---|
| 12:09.0 | disco visto de cima; duas células vizinhas | Agora o teorema de Stokes, que já usamos no vídeo do campo elétrico: o rotacional somado numa superfície é a circulação na borda. Vamos ver por quê. Começa com duas sondas vizinhas, circulando no mesmo sentido do contorno. |
| 12:15.2 | aresta comum; setas opostas | A aresta que elas têm em comum é percorrida pela primeira para dentro e pela segunda para fora: mesmo caminho, sentidos opostos. As contribuições se cancelam. |
| 12:18.2 | legenda "equivalem a uma só" | Somadas, as duas equivalem a uma só, que percorre só a borda de fora. |
| 12:25.8 | malha inteira | Cobre a superfície inteira com células. Cada sonda mede o rotacional vezes a sua área. |
| 12:26.5 | ∫_S (∇×B)·da = Σ ∮ B·dℓ | A integral do rotacional na superfície é a soma das circulações de todas as sondas. |
| 12:29.1 | legenda "lados internos se cancelam aos pares" | Cada lado interno é percorrido duas vezes, em sentidos opostos. Todos se cancelam. |
| 12:32.6 | só a borda | Só sobra a borda. |
| 12:35.4 | ∫_S (∇×B)·da = ∮_C B·dℓ; "teorema de Stokes" | Esse é o teorema de Stokes: a integral do rotacional sobre a superfície é a circulação ao longo da borda. |
| 12:41.3 | ∮_C B·dℓ = μ₀ I_enc | Juntando com o que tínhamos: a circulação do campo magnético ao longo do contorno é mi zero vezes a corrente encerrada. |
| 12:45.3 | caixa emoldurada; "Lei de Ampère · magnetostática" | Essa é a lei de Ampère, na forma integral, para a magnetostática. Ela nasceu da lei local com o teorema de Stokes. |
| 12:49.8 | disco vira cúpula; S₁ e S₂ | Se trocarmos a superfície por outra com a mesma borda, a corrente encerrada muda? Deforma o disco numa cúpula. |
| 12:54.0 | I_S₁ = I₁ + I₂ − I₃ = I_S₂ | As mesmas correntes atravessam a cúpula. A corrente encerrada é a mesma. |
| 12:57.7 | S₁ e S₂ formam V | Juntas, as duas superfícies formam um volume fechado, V: o que entra por uma sai pela outra. |
| 13:00.7 | ∮_{S₁−S₂} J·da = ∫_V ∇·J dτ = 0 | Pelo teorema da divergência, o fluxo de J por esse volume é a integral do divergente de J. |
| 13:03.8 | legenda "∇·J = 0" | E o divergente de J é zero: nada se acumula. |
| 13:04.5 | I_S₁ = I_S₂ | A corrente encerrada não depende da superfície, só da borda. |

*Por quê:* a aresta comum é **a mesma** nas duas células, com sentidos opostos, e a malha cobre o disco sem furo no centro (QA V5). S₁ e S₂ juntas formam V de propósito. O nome "teorema de Stokes" aparece uma vez; "lei de Ampère", só depois dele.

## B15 — Verdadeira não é o mesmo que útil (13:14–13:51)

| Tempo | Na tela | Fala |
|---|---|---|
| 13:18.7 | contorno irregular; B magenta, dℓ branco | Uma pergunta honesta: a lei de Ampère vale para qualquer caminho fechado, então é verdadeira. Mas serve para calcular o campo? |
| 13:19.1 | ∮_C B·dℓ = μ₀I | Escolhe um contorno qualquer em volta do fio. A circulação vale mi zero vezes a corrente. |
| 13:22.7 | legenda "B·dℓ varia ao longo de C" | Mas ao longo dele o campo e o pedacinho do caminho mudam de direção e módulo. Não dá para tirar o campo da integral. |
| 13:26.8 | legenda "verdadeira ≠ útil" | Ampère ser verdadeira é uma coisa; Ampère ser útil para calcular o campo é outra. |
| 13:29.9 | círculo centrado; barra da estratégia | A utilidade vem da simetria: com ela, escolhemos o caminho, um círculo centrado no fio. |
| 13:34.1 | B e dℓ paralelos; B constante | Agora o campo é paralelo ao caminho e tem o mesmo módulo em todo ele. |
| 13:34.8 | ∮ B·dℓ = B ∮ dℓ | O produto vira B vezes o pedacinho do caminho, e B sai da integral. |
| 13:37.4 | legenda "virou ferramenta" | A lei verdadeira virou ferramenta. |
| 13:47.4 | barra "simetria → direção de B → caminho → B·dℓ → I_enc" | Esse é o método: simetria, direção do campo, caminho, produto do campo pelo caminho, corrente encerrada. Vamos usar esses cinco passos nas quatro aplicações. |

*Por quê:* separa validade de utilidade. A barra de estratégia vira o fio condutor das aplicações: a fala a enuncia uma vez e depois só aponta para ela.

## B16 — Aplicação 1: o fio infinito (13:51–14:42)

| Tempo | Na tela | Fala |
|---|---|---|
| 13:53.9 | título "Fio infinito, agora por Ampère"; barra no passo 0 | Primeira aplicação: o fio reto e infinito. Já calculamos o campo dele por Biot–Savart, com uma integral. Agora, com Ampère, vamos ver quanto fica mais curto. |
| 14:00.3 | o campo gira e desliza | Simetria: girar em torno do fio não muda nada, e deslizar ao longo dele também não. O campo só depende da distância ao eixo. |
| 14:06.9 | B = B(s) φ̂ | Pela simetria e pela regra da mão direita, o campo é tangente aos círculos em torno do fio. |
| 14:11.7 | círculo de raio s | O caminho: um círculo de raio s, centrado no fio, onde o módulo é o mesmo em todo ponto. |
| 14:12.3 | ∮ B·dℓ = μ₀ I_enc | Ampère: a circulação é mi zero vezes a corrente encerrada. |
| 14:16.1 | dℓ branco e B magenta, paralelos | Em cada ponto, o campo e o pedacinho do caminho são paralelos: o produto é B vezes dℓ. |
| 14:20.7 | repete em todo o círculo | Em todo o círculo, com o mesmo B: ele sai da integral. |
| 14:21.4 | B ∮ dℓ = μ₀ I_enc | Sobra a integral de dℓ: o comprimento do caminho. |
| 14:24.6 | o círculo vira segmento de comprimento 2πs | Desenrolando o círculo, ele vira um segmento de comprimento dois pi s. |
| 14:28.0 | B (2πs) = μ₀ I_enc | B vezes dois pi s é mi zero vezes a corrente encerrada. |
| 14:32.3 | disco violeta; o fio atravessa | Só o fio atravessa o disco: a corrente encerrada é I. |
| 14:35.6 | B = μ₀ I / (2π s) | O campo é mi zero vezes a corrente, sobre dois pi s. |
| 14:38.2 | legenda "o campo do fio retilíneo infinito" | É o campo que calculamos com Biot–Savart, agora em poucas linhas. |

*Por quê:* primeira aplicação, segue a barra. O comprimento 2πs nasce do círculo desenrolado. A comparação com a integral do 5.2 é verbal.

## B17 — Aplicação 2: a lâmina infinita (14:42–15:28)

| Tempo | Na tela | Fala |
|---|---|---|
| 14:46.1 | lâmina cinza; K verde; x̂ branco | Segunda aplicação: uma lâmina plana infinita, com corrente espalhada na superfície. A corrente por unidade de largura é a densidade superficial de corrente, K, em ampère por metro. |
| 14:48.6 | deslizar a lâmina | Simetria: deslizar ao longo da lâmina, em qualquer direção, não muda nada. |
| 14:52.5 | a lâmina gira até virar uma linha; ⊙ | Gira para ver de perfil: a lâmina vira uma linha, e a corrente sai da tela. |
| 14:58.3 | setas magenta acima e abaixo | O campo é paralelo à lâmina e perpendicular à corrente. Pela mão direita, acima aponta para a esquerda, abaixo, para a direita. |
| 14:59.0 | B = ∓B x̂ | Em símbolos, menos B acima e mais B abaixo, na direção x. |
| 15:03.3 | retângulo atravessando a lâmina; L | O caminho é um retângulo que atravessa a lâmina: dois lados longos paralelos a ela, de comprimento L, a largura da lâmina que o caminho cobre. |
| 15:04.0 | ∮ = μ₀ I_enc | Ampère: circulação igual a mi zero vezes a corrente encerrada. |
| 15:07.3 | lados curtos | Nos lados curtos, o campo é perpendicular: zero. |
| 15:10.0 | lados longos; BL e BL | Nos lados longos, o campo acompanha o caminho: cada um dá B vezes L. |
| 15:10.7 | ∮ = BL + BL = 2BL | A circulação é duas vezes B vezes L. |
| 15:14.8 | faixa verde de largura L | A corrente encerrada é a que passa pela faixa de largura L que o retângulo cobre. |
| 15:15.5 | I_enc = K L | Corrente por largura vezes largura: K vezes L. |
| 15:17.9 | 2B L = μ₀ K L | Duas vezes B L é mi zero vezes K vezes L. |
| 15:21.3 | legenda "L cancela" | L cancela dos dois lados. |
| 15:21.9 | B = μ₀K/2 | O campo é mi zero K sobre dois, e não depende da distância à lâmina. |

*Por quê:* 2.5D só para estabelecer; toda a aplicação acontece no corte 2D. K é verde (corrente) e L é branco (geometria). A fala limita o resultado ao modelo infinito.

## B18 — Aplicação 3: o solenoide (15:28–16:57)

| Tempo | Na tela | Fala |
|---|---|---|
| 15:32.4 | hélice cinza com traços verdes | Terceira aplicação: o solenoide, um enrolamento longo, com n espiras por unidade de comprimento e corrente I. Vamos tratar o solenoide infinito ideal. |
| 15:35.3 | eixo axial, ẑ | Pela simetria, o campo é só axial, ao longo do eixo, e só depende da distância ao eixo. |
| 15:36.0 | B = B(s) ẑ | Em símbolos: B de s, na direção do eixo. |
| 15:39.3 | "ainda nada sobre dentro ou fora" | Mas ainda não sabemos o valor, nem dentro nem fora. |
| 15:45.9 | corte lateral: ⊙ em cima, ⊗ embaixo | Cortando pelo meio: em cima, a corrente sai da tela; embaixo, entra. O campo, dentro e fora, é desconhecido. |
| 15:51.0 | primeiro retângulo, todo fora; a e b | Primeiro caminho: um retângulo inteiro do lado de fora, com um lado a uma distância a do eixo e o outro a uma distância b. Aqui, a e b são só essas distâncias, não os raios do toroide. |
| 15:56.4 | lados verticais | Nos lados verticais, o campo axial é perpendicular ao caminho: zero. |
| 15:57.1 | B(a)L − B(b)L | Sobram os dois lados horizontais, de comprimento L, em sentidos opostos: campo em a vezes L, menos campo em b vezes L. |
| 16:00.6 | legenda "Sem corrente encerrada…" | Esse retângulo não envolve corrente. Ampère só compara os campos dos dois lados. |
| 16:01.3 | B(a)L − B(b)L = 0; B(a) = B(b) | Então o campo em a é igual ao campo em b. |
| 16:06.2 | o retângulo desliza | Desliza o retângulo, sempre fora: fora do solenoide, o campo não depende da distância. |
| 16:11.1 | B(s) → 0 (s → ∞) | Ampère deixou uma constante, igual em todo o lado de fora. Agora entra uma segunda informação, que não é de Ampère: longe do solenoide, o campo vai a zero. |
| 16:14.4 | B_fora = 0 | Se é o mesmo em todo o lado de fora e vai a zero longe, é zero em todo o lado de fora. |
| 16:16.9 | legenda "B_fora = 0 é resultado" | Esse resultado veio de duas coisas: da lei de Ampère e da condição no infinito. |
| 16:24.1 | segundo retângulo, um lado dentro e outro fora | Segundo caminho: um lado dentro, outro fora. |
| 16:26.4 | só o lado de dentro contribui | Fora, o campo é zero; nos lados verticais, perpendicular. Só o lado de dentro contribui. |
| 16:27.1 | ∮ = B L | A circulação é o campo dentro vezes L. |
| 16:32.2 | espiras 1, 2, 3, 4 | Quantas espiras o retângulo atravessa? Em L são n vezes L; na figura, quatro. |
| 16:32.9 | I_enc = (nL) I | A corrente encerrada é n L vezes I. |
| 16:35.3 | B L = μ₀ (nL) I | Ampère: B L é mi zero vezes n L vezes I. |
| 16:39.0 | legenda "L cancela" | L cancela. |
| 16:39.7 | B_dentro = μ₀ n I | Dentro do solenoide, o campo é mi zero vezes n vezes a corrente. |
| 16:42.2 | o lado de dentro desliza | Se o lado de dentro deslizar, o resultado não muda: dentro, o campo é uniforme. |
| 16:52.1 | solenoide finito (esquema) | Atenção: isso vale para o solenoide infinito ideal. Um real é finito: perto das pontas, o campo se espalha, as linhas internas se ligam às de retorno por fora, e fora o campo é pequeno, mas não exatamente zero. |

*Por quê:* ordem física do QA: (1) retângulo todo fora → B(a) = B(b); (2) condição no infinito → B_fora = 0; (3) segundo retângulo → B_dentro = μ₀nI. B_fora = 0 vem da lei **e** do infinito. O esquema finito deixa clara a diferença entre ideal e real.

## B19 — Aplicação 4: o toroide (16:57–17:59)

| Tempo | Na tela | Fala |
|---|---|---|
| 17:01.5 | toroide; traços sobre as espiras | Quarta aplicação: o toroide, um solenoide dobrado em forma de anel, com N espiras no total. A corrente sobe pela face interna e desce pela externa. |
| 17:08.8 | vista de cima; B = B(s) φ̂ | Pela simetria, o campo dá a volta no eixo do anel e só depende da distância ao eixo. |
| 17:16.6 | seção de cima; a e b; ⊙ na interna, ⊗ na externa | De cima, o enrolamento tem o raio interno, a, e o raio externo, b. Na face interna, N correntes saem da tela; na externa, N entram. |
| 17:21.6 | amperiano em s < a | Testamos três círculos centrados no eixo, um por vez. O primeiro, de raio menor que a, não envolve corrente nenhuma. |
| 17:22.3 | B(2πs) = 0 ⇒ B = 0 (s < a) | Então o campo é zero na região interna. |
| 17:25.2 | amperiano entre a e b | O segundo, entre a e b, envolve as N correntes da face interna, todas no mesmo sentido. |
| 17:28.8 | B(2πs) = μ₀ N I | B vezes dois pi s é mi zero vezes N vezes a corrente. |
| 17:31.4 | B = μ₀NI/(2πs) (a < s < b) | O campo é mi zero N I sobre dois pi s: cai com um sobre s dentro do enrolamento. |
| 17:35.3 | amperiano em s > b | O terceiro, de raio maior que b, envolve N correntes saindo e N entrando. |
| 17:38.3 | B(2πs) = μ₀(NI − NI) = 0 | A corrente líquida é zero, e o campo também. |
| 17:42.0 | B(s) por partes | Juntando: zero para s menor que a; mi zero N I sobre dois pi s entre a e b; zero para s maior que b. |
| 17:44.8 | gráfico; ponto branco | O mesmo caminho percorre as três regiões, e o ponto no gráfico acompanha: zero, cai com um sobre s, zero de novo. |
| 17:51.5 | legenda "confinado" | No toroide ideal, o campo fica confinado dentro do enrolamento. |

*Por quê:* os zeros pertencem ao modelo ideal. Um amperiano por vez. O ponto do gráfico deve cair exatamente em B = 0 nas duas regiões externas (correção V5). A fala distingue a e b do toroide dos do solenoide.

## B20 — Eletrostática × magnetostática (17:59–18:22)

| Tempo | Na tela | Fala |
|---|---|---|
| 18:09.4 | painéis ELETROSTÁTICA e MAGNETOSTÁTICA | Compare com a eletricidade. Na eletrostática, o divergente do campo elétrico é a densidade de carga sobre epsilon zero: cargas são fontes. Na magnetostática, o divergente do campo magnético é zero: não há fonte. |
| 18:13.0 | ∇×E = 0; ∇×B = μ₀J | O rotacional: na eletrostática, o campo elétrico não circula; na magnetostática, o campo magnético circula em torno da corrente, com rotacional igual a mi zero J. |
| 18:16.9 | legenda "valem para campos que não variam no tempo" | Atenção: essas formas valem para campos que não variam no tempo. Quando variam, ganham termos novos. |

*Por quê:* retoma os vídeos de Gauss e do divergente/rotacional do campo elétrico, com os qualificadores "NA ELETROSTÁTICA" e "NA MAGNETOSTÁTICA" na tela. O aviso final evita generalizar.

## B21 — Síntese (18:22–18:40)

| Tempo | Na tela | Fala |
|---|---|---|
| 18:26.5 | quatro ícones | O fio, a lâmina, o solenoide e o toroide: em todos, a simetria escolheu o caminho. |
| 18:34.1 | "simetria → caminho → circulação"; ∇×B = μ₀J | Não é decorar quatro campos: é ver por que existe, em cada caso, um caminho que simplifica a integral. A lei é a mesma; a simetria é que muda. |

*Por quê:* fecha a barra de estratégia. Os domínios de validade ficam na tela, sob cada fórmula.

## B22 — Gancho: um campo com divergente sempre zero (18:40–19:01)

| Tempo | Na tela | Fala |
|---|---|---|
| 18:42.9 | título; ∇·B = 0 | O divergente do campo magnético é sempre zero. Existe uma maneira de construir automaticamente um campo com essa propriedade? |
| 18:46.8 | legenda "Qualquer rotacional tem divergente zero" | Existe: o divergente de um rotacional é sempre zero, seja qual for o campo dentro dele. |
| 18:55.8 | B = ∇×A; "A: potencial vetor magnético" | Se escrevermos o campo magnético como o rotacional de outro campo, A, o divergente zero vem de graça. Esse campo é o potencial vetor magnético. |

*Por quê:* gancho para o próximo vídeo. O A aqui é o potencial vetor, não a área da sonda: a fala avisa pelo nome.

## B23 — Despedida (19:01–19:13)

| Tempo | Na tela | Fala |
|---|---|---|
| 19:01.8 | marca do Parallax Lab | No próximo vídeo, o potencial vetor magnético. Se você gostou, se inscreve no canal para acompanhar os próximos. Valeu, pessoal, e até a próxima! |

*Por quê:* despedida curta, padrão do canal; o teaser vem antes do pedido.

---

## Decisões abertas para fechar com o GPT

0. **Duração (decisão principal):** ver a tabela. Se o vídeo final tiver de ficar perto de 24 a 28 minutos, o caminho é enxugar a fala (não a animação) nos blocos de álgebra (B05, B07, B09).
1. **Abertura:** "Fala, pessoal!" como nos outros longos, ou entrada mais seca por já estarmos no terceiro vídeo da série.
2. **Valor de mi zero:** a fala diz só "permeabilidade magnética do vácuo". Dizer o valor numérico ou omitir.
3. **Lei de Ampère "na forma local" no B09:** o nome já aparece no fim do B09, ou só no B14 junto com a forma integral.
4. **Nablas:** a fala diz "nabla cruz B" e "nabla ponto B" só na primeira vez; depois, "o rotacional de B", "o divergente de B". Confirmar a convenção da série.
5. **Delta de Dirac (B08):** a fala usa "pico infinitamente fino" e avisa que a figura é um esquema. Se o GPT preferir uma definição por distribuição, ela cabe sem mudar a tela.
6. **Resposta do paradoxo (B12):** "zeros fora do eixo, mais uma contribuição infinita num ponto, podem dar um valor finito". Confirmar se é rigorosa o bastante.
7. **Retomadas dos vídeos anteriores:** a v1 cita "o vídeo do campo elétrico" (divergente e rotacional) e "a lei de Gauss". Confirmar os nomes exatos dos vídeos.
8. **Pontos que a animação precisa segurar:** os blocos de maior folga (coluna da direita, abaixo).

## Estimativa de duração e folga da animação

Contagem automática: palavras da coluna Fala de cada linha, a 2,8 palavras por segundo; a janela de cada linha vai do seu início até o início da linha seguinte (a última, até o fim do bloco).

| Bloco | Janela no vídeo | Palavras | Voz (2,8 p/s) | Folga extra necessária |
|---|---|---|---|---|
| B00 | 0:00–0:20 | 189 | 1:07.5 | +0:47.5 |
| B01 | 0:20–1:17 | 372 | 2:12.9 | +1:17.2 |
| B02 | 1:17–2:08 | 278 | 1:39.3 | +0:55.5 |
| B03 | 2:08–2:46 | 224 | 1:20.0 | +0:42.2 |
| B04 | 2:46–3:39 | 248 | 1:28.6 | +0:42.1 |
| B05 | 3:39–4:57 | 421 | 2:30.4 | +1:30.2 |
| B06 | 4:57–5:49 | 244 | 1:27.1 | +0:43.3 |
| B07 | 5:49–6:33 | 208 | 1:14.3 | +0:36.1 |
| B08 | 6:33–7:46 | 333 | 1:58.9 | +0:57.9 |
| B09 | 7:46–9:14 | 434 | 2:35.0 | +1:15.0 |
| B10 | 9:14–10:15 | 343 | 2:02.5 | +1:11.8 |
| B11 | 10:15–10:52 | 226 | 1:20.7 | +0:45.5 |
| B12 | 10:52–11:28 | 220 | 1:18.6 | +0:48.2 |
| B13 | 11:28–12:07 | 219 | 1:18.2 | +0:45.2 |
| B14 | 12:07–13:14 | 274 | 1:37.9 | +0:42.8 |
| B15 | 13:14–13:51 | 149 | 0:53.2 | +0:29.1 |
| B16 | 13:51–14:42 | 196 | 1:10.0 | +0:22.1 |
| B17 | 14:42–15:28 | 211 | 1:15.4 | +0:35.5 |
| B18 | 15:28–16:57 | 387 | 2:18.2 | +1:06.3 |
| B19 | 16:57–17:59 | 227 | 1:21.1 | +0:29.4 |
| B20 | 17:59–18:22 | 76 | 0:27.1 | +0:14.5 |
| B21 | 18:22–18:40 | 45 | 0:16.1 | +0:04.5 |
| B22 | 18:40–19:01 | 60 | 0:21.4 | +0:06.6 |
| B23 | 19:01–19:13 | 24 | 0:08.6 | +0:00.0 |
| **Total** | 0:00–19:13 | **5608** | **33:22.9** | **+17:08.7** |

Leitura: a voz soma cerca de 33:22.9, contra 19:12,9 de animação. A folga extra (soma dos trechos em que a fala de uma linha passa da janela até o próximo evento) é de cerca de 17:08.7: é isso que a animação precisa segurar (pausas de leitura, paradas em quadro) para a voz caber, e é o que o remapeamento por âncoras resolve. Por isso o vídeo final deve ficar em torno de 36:21.6, e não nos 19:12,9 do preview mudo. Os blocos com maior folga pedem as pausas mais longas: veja a coluna da direita.

