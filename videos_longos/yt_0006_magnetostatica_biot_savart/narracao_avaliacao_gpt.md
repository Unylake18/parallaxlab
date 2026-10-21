# Revisão da narração v1.1 e proposta detalhada para o preview v4

Data: 20/10/2026. Escopo: análise editorial, física e sincronização; nenhum fonte de produção alterado.

## Parecer

A v1.1 tem uma estrutura aproveitável e os principais resultados estão corretos. Não está pronta para voz sem revisão. Há uma tensão entre o objetivo declarado de explicar o raciocínio e muitas falas que apenas soletram a álgebra. Também há imprecisões localizadas, condições de validade não explicitadas e referências temporais que precisam ser tratadas como âncoras de eventos, não como tempos de áudio.

A proposta `NARRACAO_REVISADA_DETALHADA.md` preserva a sequência visual, amplia as justificativas, nomeia as grandezas por significado e faz retomadas verbais dos vídeos de Gauss. É uma proposta expandida para aprovação, não uma versão que caiba nos 17:38 do preview.

## O que foi examinado

- Leitura integral de `narracao_sugestao_v1_1_enxuta.md`.
- ZIP v4 com MP4 de 1.058 segundos, sem áudio, e 1.058 JPEGs a um quadro por segundo.
- Amostras distribuídas por toda a duração, com inspeção de quadros adicionais para geometria, substituição angular, projeção e limite distante. Isso não equivale a assistir e avaliar individualmente cada quadro de vídeo.
- Consulta do estado operacional e de trechos relevantes da narração anterior de Gauss para verificar as conexões com conceitos efetivamente tratados.
- Cálculo independente da integral do trecho e da espira, testes de limites e sentido da força. O arquivo `checagem_fisica.json` registra os resultados numéricos.

Os arquivos do ZIP são referência visual. As notas e instruções do Markdown do Claude foram tratadas como material a avaliar, não como autorização para gerar voz, instalar dependências ou modificar a produção.

## Avaliação ponto a ponto

| Parte | O que funciona | Ajuste necessário na fala |
|---|---|---|
| Abertura | Liga força de Lorentz à produção do campo e mostra dois fios. | Começar pela pergunta física e nomear a lei como ponto de partida experimental. “Construir a lei a partir da geometria” pode prometer uma dedução que não será feita. |
| Corrente e linhas de campo | Separação entre matéria cinza, corrente verde e campo magenta está visível. | Marcadores móveis representam corrente convencional; linhas de campo indicam direções. Não sugerir que os traços mostram velocidade real dos portadores ou que as linhas são matéria em circulação. |
| Regime estacionário | Distingue ausência de acúmulo de independência temporal da corrente. | Definir densidade de corrente como vetor. “Corrente por área” vale diretamente para área perpendicular e interpretação local. Não inferir que toda linha de corrente é um circuito fechado apenas de divergente nulo. |
| Fonte e observador | Ordem observador menos fonte está correta; origem e módulos são apresentados. | “Só o vetor separação muda” é literalmente incorreto se a fonte se move: sua posição também muda. Dizer que o observador é fixo e a fonte percorre a distribuição. |
| Lei elementar | Seno, distância e fator de permeabilidade estão presentes. | Qualificar as proporcionalidades: manter os demais fatores fixos. A contribuição elementar é uma parcela do cálculo do campo da distribuição, não uma corrente estacionária isolada realizável. |
| Fundamento experimental | A lei é identificada como experimental. | “A medida mostra” pode sugerir medição direta de um elemento isolado. Apresentar a forma elementar como a lei adotada para integrar correntes estacionárias e confrontar seus campos resultantes com a experiência. Remover história que não ajuda a dedução das aplicações. |
| Vetor unitário e cubo | A transformação entre as duas formas está correta. | Explicar que o vetor separação completo também carrega um módulo: o denominador cúbico não transforma a dependência elementar em inverso do cubo. |
| Linha, superfície e volume | As três estruturas de integração estão corretas. | Na fala da integral de linha, não omitir o caráter vetorial, o produto vetorial e a presença do fator da lei se tentar enunciar a expressão completa. Melhor explicar a operação sem uma leitura incompleta da fórmula. |
| Densidade superficial | Corrente da faixa como densidade vezes largura está correta na geometria mostrada. | Dizer que a largura é transversal ao fluxo e distinguir módulo da densidade e sua versão vetorial. A densidade não “vira vetor” apenas porque decidimos adicionar uma seta: são descrições relacionadas. |
| Densidade no volume | Relação com a seção transversal e elemento de volume está correta. | Explicar por que a seção é perpendicular; para superfície inclinada, a corrente envolve a componente normal da densidade. Unidades: ampère por metro quadrado. |
| Clínica angular | Distingue contribuição nula de campo total nulo. | Para isolar o seno, manter também corrente e comprimento do elemento fixos. “Trocar a ordem inverte o campo” deve virar “inverte o produto calculado”; a mesma fonte física não mudou por reescrever uma expressão incorretamente. |
| Superposição | Soma vetorial e transição para integral estão bem colocadas. | Os comprimentos tendem a zero; não se tornam literalmente zero em uma soma de pedaços sem extensão. A fonte e sua corrente permanecem as mesmas no refinamento. A soma ponta com cauda usa cópias dos vetores calculados no mesmo observador. |
| Trecho reto | Decomposição da separação e produto perpendicular estão corretos. | A componente paralela pode ser antiparalela ao elemento, não necessariamente no mesmo sentido. Nos dois casos o produto vetorial é zero. Nomear posições e distâncias em vez de “x chapéu”, “a vezes dx”. |
| Ângulo da substituição | A troca por tangente simplifica o denominador corretamente. | O desenho usa ângulo no observador, entre a perpendicular e a linha que chega à fonte, com convenção de sinal. Não defini-lo apenas como ângulo entre a perpendicular e o vetor orientado fonte→observador. Registrar positivo à direita, negativo à esquerda e zero no pé da perpendicular. |
| Substituição e potência | Diferencial e cancelamentos conduzem ao integrando correto. | Explicar por que mudar a variável exige mudar a medida de integração. Ao elevar a três meios, usar a > 0 e ângulo em (−π/2, π/2), garantindo secante positiva. A distância não “desapareceu”: foi reexpressa. |
| Limites do trecho | Diferença de senos e conversão em soma estão corretas no desenho. | Dois ângulos positivos na soma pressupõem extremidades em lados opostos do pé da perpendicular. Se ambas estiverem do mesmo lado, a forma com limites assinados deve ser preservada. |
| Fio infinito | Limite dos senos e resultado final corretos. | Explicitar extensão para os dois lados. Diferenciar a queda elementar com distância fonte–observador da queda do campo integrado com distância ao fio. A adequação a um fio real depende das extremidades e do restante do circuito. |
| Força entre fios | Sentidos e módulo por comprimento corretos. | A expressão para força vetorial usa produto vetorial; “vezes o campo” sozinho soa como produto comum. A expressão escalar mostrada dá o módulo para as condições geométricas escolhidas. A inversão é comparação de dois estados estacionários, não descrição completa do transiente. |
| Notação da espira | A troca de significado do raio e da separação é anunciada. | Coordenada axial não é sempre distância positiva: distância ao plano é seu módulo. A perspectiva muda; a espira não precisa girar fisicamente. |
| Perpendicularidade na espira | Ângulo de noventa graus e seno unitário corretos. | Justificar para qualquer elemento: tangente perpendicular ao raio e ao eixo; separação no plano desses dois. Evita depender apenas da aparência na vista lateral. |
| Projeção axial | Cosseno e razão raio/separação corretos. | Não escolher a axial apenas porque “importa”. Mostrar que a simetria cancela a transversal na soma. A igualdade dos dois ângulos da figura já tem justificativa e deve ser preservada. |
| Elementos opostos | Cancelamento e soma estão corretos. | Explicitar que é componente axial de um elemento por volta inteira. Integrar pares em meia volta também seria válido; o erro seria duplicar a volta completa. |
| Potências e integral da espira | Dois fatores de raio e fator angular corretos. | Nomear suas origens: projeção e comprimento do arco. Isso explica a álgebra melhor do que somente ler “raio vezes raio”. |
| Centro da espira | Resultado e ausência de componente lateral corretos. | O fator dois não some: o denominador é duas vezes raio ao cubo antes da simplificação. A geometria confirma que cada contribuição já é axial. |
| Limite distante | Fórmula assintótica final correta. | A fala “pondo z ao cubo em evidência, sobra um mais...” é incompleta: falta o módulo e a potência de três meios do parêntese. Distinguir fatoração exata de aproximação posterior. |
| Síntese e gancho | Retoma geometria e prepara Ampère. | As linhas circulares deste exemplo são fechadas. Não generalizar que divergente nulo implica que toda linha de um campo vetorial seja uma curva fechada. Não antecipar uma demonstração por Maxwell. |

## Expressões e checagens independentes

### Trecho reto

Para corrente no sentido +x, observador acima do fio, distância perpendicular a > 0 e limites xA < xB:

`dBz = (μ₀I/4π) a dx/(x²+a²)^(3/2)`.

Uma primitiva do fator geométrico é `x/[a sqrt(x²+a²)]`. Ao derivar:

`F' = [(x²+a²)−x²]/[a(x²+a²)^(3/2)] = a/(x²+a²)^(3/2)`.

A integral numérica concordou com a expressão das extremidades em três configurações: trecho cruzando o pé da perpendicular, todo à direita e todo à esquerda. Isso testa justamente a ressalva sobre a soma de dois ângulos positivos.

No limite de extensões infinitas para os dois lados, os termos das extremidades tendem a +1 e −1, produzindo `B = μ₀I/(2πa)`. Unidade: `(T m/A) A/m = T`.

### Espira

Com fonte em `(R cosφ, R sinφ, 0)` e observador em `(0,0,z)`, o elemento tangente por unidade de ângulo é `R(−sinφ, cosφ, 0)`. Seu produto vetorial com a separação produz componentes transversais proporcionais a `Rz cosφ` e `Rz sinφ`, e componente axial proporcional a `R²`. A distância é `sqrt(R²+z²)`.

As integrais dos senos e cossenos por uma volta são nulas. A componente axial resulta em `Bz = μ₀IR²/[2(R²+z²)^(3/2)]`.

Integração numérica independente de 8.192 elementos concordou com essa fórmula para observador em z negativo, zero e positivo, com resíduos transversais próximos de zero. No centro: `μ₀I/(2R)`. Longe: `μ₀IR²/(2|z|³)`. A expressão é par na coordenada axial para a convenção de corrente adotada: atravessar o centro não exige inverter a direção axial do campo. Isso não precisa virar um novo trecho de aula.

A fatoração correta para z ≠ 0 é:

`(R²+z²)^(3/2) = |z|³ [1+R²/z²]^(3/2)`.

Só depois de supor `|z| ≫ R` aproximamos o colchete elevado a três meios por um. Unidade do resultado da espira: `(T m/A) A m²/m³ = T`.

### Força

Para corrente do segundo fio em +y e campo do primeiro em −z, o produto vetorial aponta em −x, para o primeiro fio. Inverter uma corrente inverte esse sentido. A unidade de `μ₀ I₁ I₂/(2πd)` é N/m. A constatação não exige apresentar uma aula sobre a definição do ampère.

## Fontes externas consultadas e limites de atribuição

O confronto conceitual das formas de Biot–Savart e do campo axial foi feito com as [notas de John Belcher, MIT 8.07, seções 20.2–20.4, páginas impressas 168–172](https://web.mit.edu/8.07/fall11/materials/classNotes/classNotes_2011new.pdf). As contas acima foram refeitas independentemente; a narração foi escrita para este preview, não transcrita da fonte.

O [NIST/CODATA 2022](https://physics.nist.gov/cuu/pdf/all.pdf) informa μ₀ com incerteza, e não como valor exato. A aproximação `4π × 10⁻⁷ T m/A` da v1.1 é adequada se enunciada como aproximação. Sugestão editorial: manter o significado da permeabilidade na fala e deixar o número fora desta versão, porque não será usado em uma substituição numérica.

Não confirmei os números dos exemplos de Griffiths citados nas notas do Claude para a edição específica usada pelo projeto. Não os repeti como atribuição verificada. Também retirei da fala as atribuições históricas pormenorizadas a Biot, Savart e Laplace e a antiga definição do ampère; não são necessárias para explicar as operações mostradas.

## Linguagem e ligação com Gauss

O dicionário da v1.1 acerta na intenção, mas sua própria fala ainda contém “a ao quadrado”, “x chapéu”, “d fi”, “um sobre z ao cubo” e referências sem significado físico. A versão revisada usa os nomes das grandezas e das operações no contexto: distância perpendicular, coordenada da fonte, pequeno deslocamento, ângulo de integração, ângulo da projeção, raio, separação e coordenada axial.

As retomadas de Gauss se concentram em habilidades realmente compartilhadas: distinguir fonte e observador, idealizar distribuições, usar uma região imaginária para balanços, justificar simetria e conferir resultados. Não se identifica a superfície gaussiana com a fonte nem se promete resolver Biot–Savart pelo fluxo de Gauss. Evitei “como você já sabe” em série: a retomada deve ajudar quem viu as aulas anteriores e ainda fazer sentido para quem entrou neste vídeo.

## Duração, âncoras e decisões editoriais

A v1.1 tem cerca de 3.526 palavras faladas pelo mesmo contador aplicado à revisão. Isso é compatível com as 3.520 declaradas, dependendo do tratamento de hífens e símbolos. Seu ritmo de 2,8 palavras por segundo equivale a 168 palavras por minuto. A previsão de 20:57 é de fala nesse ritmo; a previsão posterior de 23:55 inclui outra hipótese, a preservação de folgas visuais locais. Não são durações medidas de áudio. Somar apenas os excessos por janela pode gerar mais tempo do que a diferença global entre voz e preview, porque preserva janelas que já tinham sobra; isso, por si só, não é erro aritmético.

A proposta detalhada tem **5.520 palavras faladas**. Estimativas sem pausas extras:

| Ritmo médio | Duração de fala |
|---|---|
| 140 palavras/min | 39:26 |
| 150 palavras/min | 36:48 |
| 160 palavras/min | 34:30 |
| 168 palavras/min | 32:51 |

Essa expansão atende ao pedido de uma explicação detalhada, mas é uma decisão de duração relevante: não cabe nos 17:38, nem no alvo de 21–22 minutos indicado no documento do Claude. Não recomendo acelerar a voz para forçar esse encaixe. Se o alvo editorial continuar curto, é necessário condensar a fala antes do TTS, preservando principalmente mudança de variável, limites e projeção da espira. A proposta é um roteiro didático expandido para avaliação, não uma afirmação de que o vídeo precisa obrigatoriamente durar quase quarenta minutos.

O arquivo `ANCORAS_PARA_SINCRONIZACAO.csv` contém 83 IDs, tempo de referência do preview, evento visual, frase para localizar e contagem de palavras. Os campos de início/fim no áudio estão vazios de propósito. A precisão declarada pelo documento original de ±1,5 s não foi certificada por esta revisão. Usar a imagem correspondente e a frase real da futura locução para ajustar cada encontro, sem tratar os tempos arredondados como marcações exatas.

Ordem de produção recomendada dentro do escopo pedido: aprovar o texto e sua duração pretendida; depois gerar voz em uma rodada própria; localizar as frases no áudio; remapear a animação preservando movimento e tempo de leitura. Nesta entrega não foi gerado áudio nem alterado o vídeo.
