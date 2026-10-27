# Órbita como queda contínua — proposta de repaginação visual

**Parallax Lab · yt_0007 · 18/10/2026**  
**Status: proposta para revisão editorial. Sem implementação.**

A proposta é reconstruir a encenação do vídeo: começar junto da montanha, acompanhar os lançamentos, revelar a curvatura do planeta, entrar na geometria local e voltar ao espaço. O modelo físico e a progressão N01–N18 permanecem. A mudança principal está na relação entre movimento, câmera, escala e explicação.

## 1. Base examinada e limites da avaliação

Foi inspecionado o ZIP `avaliacao_visual_completa_0007.zip` fornecido no caminho local da unidade. Ele contém 42 PNGs, sete pranchas, o preview completo e os arquivos de timing, validação física e QA. A decodificação do MP4 confirmou **960×540, 15 fps, 5.800 quadros, 386,67 s e nenhuma faixa de áudio**. Foram examinados os 42 quadros nas sete pranchas, além de amostras temporais adicionais da abertura e das transições extraídas do próprio MP4. Não se trata de uma revisão contínua, quadro a quadro, de toda a animação.

Também foram lidos o estado operacional atual do repositório, as decisões pertinentes, a identidade visual, a ficha e os trechos relevantes da cena de órbita. A comparação com Gauss usa as pranchas da revisão 2.1 de `yt_0001` e o código das duas unidades. **Não foi localizado nesta cópia um MP4 ou conjunto de frames de `yt_0002`; sua comparação é documental e pelo código, sem alegar inspeção do master.**

O relatório de QA que acompanha o ZIP registra verificações técnicas e físicas. Isso não equivale à aprovação artística da direção visual. A avaliação abaixo é independente desse parecer.

### Evidências visuais da versão atual

- [Abertura em oito instantes](./evidencia_N01_movimento.jpg).
- [Amostras das transições](./evidencia_transicoes.jpg).
- [N01–N02](./referencias_zip/pranchas/prancha_01.jpg), [N03–N04](./referencias_zip/pranchas/prancha_02.jpg), [N05–N08](./referencias_zip/pranchas/prancha_03.jpg).
- [N09–N11](./referencias_zip/pranchas/prancha_04.jpg), [N12–N13](./referencias_zip/pranchas/prancha_05.jpg), [N13–N14](./referencias_zip/pranchas/prancha_06.jpg), [N15–N18](./referencias_zip/pranchas/prancha_07.jpg).

## 2. Diagnóstico: o que está enfraquecendo o vídeo

| Evidência | Efeito na experiência | Direção proposta |
| --- | --- | --- |
| N01, 00:01–00:39: a Terra abre o enquadramento, mas a montanha permanece um triângulo pequeno; não há canhão construído como objeto. | O espectador vê um esquema antes de conseguir imaginar o lançamento. | Começar em plano próximo, com relevo, plataforma, canhão e pedra claramente distinguíveis; revelar o planeta durante a experiência. |
| N02–N06: repetição de planeta à esquerda, título acima e frases/fórmulas à direita. | A animação fica confinada a uma região pequena e o texto assume a explicação. | Alternar plano amplo, detalhe local e pausa geométrica; abrir espaço para uma equação apenas quando necessária. |
| A função de abertura de cada bloco apaga a composição e cria outro título. | Os 18 marcos internos tornam-se 18 reinícios visuais. | Preservar objetos e enquadramento nas passagens conceitualmente contínuas. |
| N07: a geometria local é válida, mas aparece depois de uma troca de tela. | O público precisa reconstruir sozinho a ligação entre o pequeno arco e a órbita global. | Extrair visivelmente o detalhe da própria órbita e devolver esse detalhe ao planeta em N08. |
| N09: estação e astronauta são pequenos ao lado de explicações escritas. | A queda conjunta é enunciada com mais força do que é vivenciada. | Aproximar a estação, revelar seu interior e mostrar objetos livres acompanhando a cabine. |
| N13, aproximadamente 04:14–04:46: a curva e a seta inicial variam; o marcador permanece no lançamento. | A família de órbitas aparece como catálogo de desenhos. | Distinguir ajuste da condição inicial e execução do lançamento, com movimento efetivo em estados selecionados. |
| N16–N18 retomam corpos pequenos e composições conhecidas. | A expansão de escala e o fechamento têm pouco impacto visual. | Fazer a escala conduzir a síntese e reencontrar a imagem de abertura. |

Há animação na versão atual, inclusive abertura de enquadramento, vetores e trajetórias calculadas. O problema é a pouca variedade de encenação e a fraca ligação espacial entre as representações. Aumentar apenas resolução, brilho ou quantidade de efeitos preservaria essa estrutura.

## 3. Continuidade com os longos de Gauss

| Elemento | Padrão verificado em Gauss | Órbita atual | Proposta para órbita |
| --- | --- | --- | --- |
| Cabeçalho editorial | `ELETROMAGNETISMO · LEI DE GAUSS`, no alto à esquerda. | `FÍSICA I / GRAVITAÇÃO`. | **`GRAVITAÇÃO · ÓRBITAS`**, com a mesma hierarquia e o mesmo separador. |
| Marca durante o conteúdo | Asset oficial no alto à direita; largura lógica 1,92, opacidade 0,45, margem 0,30. | Mesmo tamanho/opacidade, mas deslocado para baixo à direita. | Recuperar a aplicação de Gauss; manter fixa em relação à tela durante os movimentos de câmera. |
| Contador | Os blocos são internos; as cenas consultadas não exibem contador de seções nesse canto. | `01 / 18` até `18 / 18`. | **Retirar do produto.** N01–N18 continuam no planejamento, timing e QA. |
| Cor | Funções diferentes recebem cores estáveis, ligando geometria e símbolos. | Há semântica nos desenhos, mas várias fórmulas estão brancas ou inteiramente ciano. | Colorir grandezas e correspondências, preservando operadores e sinais neutros. |
| Construção | Objetos, regiões e expressões se transformam em etapas. | Há reconstrução frequente da tela. | Herdar a continuidade de construção e a hierarquia visual de Gauss. |
| Composição | FOCUS, SPLIT, COMPARE e BUILD conforme a função. | Predomínio do mesmo arranjo esquerda/direita. | Usar a composição para conduzir a descoberta; análise em coluna somente nos trechos que a pedem. |

**Recomendação de nome:** `GRAVITAÇÃO · ÓRBITAS`. “Mecânica” continua na classificação curricular da ficha. O cabeçalho apresenta assunto e recorte, como em Gauss; não precisa expor toda a árvore curricular.

Há uma exceção histórica em Gauss: a abertura anterior à apresentação da marca ocorre sem header/watermark. Para esta repaginação, a preferência expressa pelo usuário é manter a marca no canto superior direito; proponho aplicá-la desde o início, discretamente, sem acrescentar uma vinheta ou nova cena ao storyboard.

## 4. Direção visual: três escalas conectadas

### Perto da montanha

Mostrar um lugar de lançamento reconhecível: faces iluminadas e sombreadas do relevo, plataforma horizontal, canhão simplificado e pedra com volume. O horizonte deve continuar além do quadro. A Terra inteira só precisa aparecer quando o alcance do lançamento exigir.

A montanha permanece uma idealização. O ponto inicial aprovado, `r₀ = 1,06 R_T`, fica aproximadamente **382 km acima da superfície**. A arte pode ser elaborada, mas deve manter a identificação “montanha idealizada · sem atmosfera”; não sugerir uma montanha terrestre real com essa altura. Não introduzir fumaça, resistência do ar ou um mecanismo de propulsão durante o voo.

### Perto do movimento

A câmera acompanha a pedra com espaço à frente, mantendo uma referência do solo ou do centro. O movimento da superfície no quadro revela a geometria. Quando uma relação precisar ser examinada, a câmera desacelera e estabiliza antes de entrarem vetores, cotas ou equações.

Essa câmera é uma ferramenta de apresentação. Não acrescentar forças aparentes, nem confundir a orientação da tela com a direção física de “cair”. A seta gravitacional continua apontando para o centro terrestre projetado.

### Na escala orbital

A Terra ganha leitura volumétrica por iluminação estável, contorno e oclusão coerente dos corpos. Uma vista oblíqua breve pode revelar o plano orbital; em seguida, a câmera se alinha perpendicularmente a esse plano para explicar tangência, raio, círculo e elipse.

Se um círculo for visto obliquamente, identificar **“mesma órbita circular · vista oblíqua”**. A forma projetada não representa uma mudança de excentricidade. A superfície terrestre não gira fisicamente para criar espetáculo: rotação continua fora do modelo aprovado.

## 5. Assinatura Parallax em movimento

**Transformação recorrente proposta:** cena física → estrutura geométrica → relação matemática → retorno à cena física. O espectador reconhece os mesmos objetos através dessas mudanças de representação.

- A superfície pode perder detalhe e preenchimento, deixando centro, posição do satélite e órbita. Depois, ela retorna. Isso permite “tirar a Terra” visualmente sem desligar sua gravidade.
- A trajetória é um traço fino do movimento, sem aparência de tubo, trilho ou suporte material.
- Planos, guias e construções translúcidas entram apenas quando explicam algo. A identidade de planos e profundidade da marca aparece na organização espacial.
- Relevo próximo, planeta e fundo recebem profundidades distintas. A paralaxe serve às mudanças de escala; o fundo permanece discreto.
- Oclusão por uma Terra opaca e continuação matemática através do planeta têm tratamentos diferentes. A exceção de N14 deve ser explicitamente identificada.

**Gramática de câmera proposta:** aproximar para inspecionar; acompanhar para perceber movimento; abrir para revelar escala; mudar o ângulo para esclarecer a geometria. Cada movimento deve responder a uma pergunta visual. Durante leitura de fórmula ou comparação de vetores, estabilizar o quadro.

**Gramática de transição proposta:** conservar o objeto de referência e transformar a composição ao redor dele. Troca explícita de caso físico é necessária em N10, N11→N12, nas reinicializações de N13 e na montagem de escalas de N16. Continuidade de imagem não deve sugerir uma evolução física que não foi modelada.

## 6. Cores semânticas e equações

As cores abaixo são uma **adaptação proposta para esta unidade**, mantendo as famílias visuais de Gauss. Não constituem alteração da identidade global.

| Papel | Cor proposta | Aplicação |
| --- | --- | --- |
| Fundo | `#050816` | Fundo existente. |
| Terra e trajetória física | `#267BFF`, contorno `#7FB2FF` | Corpo atrator e caminho físico, distinguidos também por preenchimento/traço. |
| Gravidade | `#35D9FF` | Campo gravitacional, `g`, vetor aceleração gravitacional e força gravitacional quando explicitada. |
| Velocidade e matéria móvel | `#F5F7FF` | Pedra/satélite, vetor `v`, `v₀`; seta e rótulo sempre ligados. |
| Geometria auxiliar | `#9C8CFF` | Raio orbital `r`, semieixo `a`, cotas e construções. Traçado diferenciado para contrafactuais e continuação matemática. |
| Corpo central | `#7FB2FF` | `M`, `R_T` e elementos associados à Terra. |
| Tempo | `#FFC24D` | `t`, `T` e referência temporal, aproveitando o acento âmbar presente em Gauss 1. |
| Operadores, unidades e constantes | `#F5F7FF` | Igualdades, sinais, barras de fração, unidades e `G`. |

O ciano, usado como campo elétrico em Gauss, passa a identificar o campo gravitacional neste vídeo. Essa adaptação precisa aparecer de forma consistente nos objetos e nas expressões. Em N12, distinguir por contexto o semieixo escalar `a` da aceleração vetorial `a⃗` mostrada antes.

Exemplos de aplicação:

- Em `GM/r² = v²/r`, os dois `r` mantêm o violeta da cota radial; `M` mantém o azul da Terra; `v` continua branco. Ao apresentar o lado gravitacional como um todo, destacar brevemente sua ligação com a seta ciano, sem pintar permanentemente a expressão inteira dessa cor.
- Em `v_orb = √(GM/r)`, manter esse mesmo mapa. A cota radial e o `r` da fórmula reagem juntos quando o raio muda na comparação de casos.
- Em `T² = (4π²/GM)a³`, `T` acompanha o marcador temporal âmbar e `a` acompanha a cota violeta da elipse.
- Em N07, as duas medidas de 4,35 m recebem a mesma ênfase no instante da comparação; suas origens permanecem identificadas como queda e curvatura.

**Construção das equações:** primeiro apontar a grandeza no desenho; depois fazer aparecer seu símbolo na relação; por fim transformar uma operação de cada vez. Manter uma equação ativa e, quando necessário, uma referência secundária. Não diminuir a matemática para acomodar várias linhas simultâneas.

MF-Tools é pertinente aos cancelamentos e à reorganização de termos de N06 e N11. O repositório já o utiliza em Gauss 2. `TransformMatchingTex` continua adequado quando a correspondência é clara; `TransformByGlyphMap` entra onde esclarece a operação. Montanha, Terra, órbita e câmera pedem transformações geométricas e estados sincronizados: a biblioteca de glifos não substitui essa direção de animação.

## 7. Repaginação de N01 a N18

Os códigos abaixo são internos; não entram no canto do vídeo. Os intervalos citados pertencem ao preview atual e servem para localizar a evidência, sem fixar a duração futura.

| Cena | Encenação e movimento propostos | Câmera e ligação com a seguinte |
| --- | --- | --- |
| **N01 — Lançamentos** | Abrir perto do canhão e da pedra sobre a montanha. Primeiro lançamento mostra avanço e impacto próximo. Segundo revela um trecho maior da superfície. Terceiro força a abertura até quase o lado oposto. Quarto mantém a pedra em voo e fecha a volta. As tentativas anteriores ficam secundárias. | Voltar ao mesmo ponto de lançamento em cada tentativa, com velocidade inicial crescente. Acompanhamento lateral → horizonte curvo → planeta inteiro. Terminar com o corpo ainda em órbita. |
| **N02 — Queda contínua** | Conservar o quarto lançamento. Entrar uma única seta gravitacional, acompanhando o corpo e apontando para o centro. Mostrar sua direção em posições diferentes; então estabilizar. | Aproximar o satélite e um trecho da Terra, sem apagar a cena. A mesma posição prepara o contrafactual. |
| **N03 — Sem gravidade** | Congelar um instante. No ramo identificado como “sem gravidade”, o corpo segue pela tangente violeta tracejada. Retornar ao mesmo estado e mostrar o ramo com gravidade. | Manter o mesmo enquadramento nos dois ramos para permitir comparação. Voltar ao instante de partida para construir os vetores. |
| **N04 — A velocidade gira** | Ampliar o vetor tangente. Copiar `v(t)` e `v(t+Δt)` para uma origem comum e construir sua diferença. Repetir o pequeno desvio em três posições. | Sair da geometria local para o arco com uma ligação visível. Usar `Δv ≈ aΔt` para setas finitas; apresentar `dv = a dt` como relação diferencial. |
| **N05 — Uma aceleração, duas descrições** | Da seta para o centro, construir o raio e o arco circular. Relacionar a descrição gravitacional `GM/r²` à descrição cinemática `v²/r`. | Quadro estável enquanto a relação é lida. Preservar o mesmo corpo e a mesma seta para N06. |
| **N06 — Velocidade circular** | Transformar a igualdade até a raiz, deixando explícito o cancelamento do fator de raio. O vetor tangente e a cota radial continuam ligados aos símbolos correspondentes. | Após a conta, reduzir a presença da fórmula e voltar a acompanhar o corpo. Declarar a mudança para o exemplo a 400 km. |
| **N07 — Um segundo** | Partir da órbita de 400 km, marcar um pequeno trecho e ampliá-lo. Um marcador de `0 → 1 s` sincroniza movimento e medidas. Construir primeiro 7,67 km na direção tangente; depois a queda de 4,35 m; então a curvatura correspondente. | Mostrar a transição da escala global para a ampliação local. Avisos permanecem durante a distorção. Só depois da comparação visual entra a cadeia curta de relações. |
| **N08 — De volta à órbita** | Recolocar o detalhe local na órbita global. Os dois resultados coincidentes se integram à ideia de trajetória circular. Remover cotas e retomar o movimento. | Abrir a câmera a partir do mesmo ponto. Evitar repetir a construção inteira de N07 ou criar outra tela de título. |
| **N09 — Microgravidade** | Aproximar a estação e revelar um corte do interior: astronauta e objeto solto acompanham a cabine. Mostrar gravidade ainda presente e ausência de apoio sustentado no caso ideal. Comparar brevemente com astronauta apoiado no chão terrestre. | Exterior orbital → interior em corte, identificado como vista local que acompanha a estação. Voltar à visão global. Preservar `g_órbita/g_superfície ≈ 0,89` como informação curta. |
| **N10 — Alta e baixa** | Mostrar duas órbitas circulares como casos independentes, com corpos distinguíveis, raios e vetores tangentes. Um relógio físico comum permite perceber a diferença de avanço, velocidade e período. | Vista perpendicular ao plano, sem deslocar um satélite de uma órbita para outra. Destacar um dos casos para construir o período em N11. |
| **N11 — Período** | Um marcador acompanha uma volta e um acento percorre seu comprimento. Relacionar `2πr`, `v` e `T`; transformar a expressão até a terceira lei circular com cores estáveis. | Estabilizar a câmera durante as operações. Encerrar explicitamente o caso circular antes da generalização. |
| **N12 — Generalização elíptica** | Identificar “novo caso: órbita elíptica”. Revelar a Terra em um foco e medir o semieixo a partir do centro geométrico da elipse. Transformar a relação circular na relação com `a`. | Se houver vista oblíqua, voltar à vista perpendicular antes de discutir a forma da elipse. A troca `r → a` é conceitual; não representa deformação espontânea da órbita anterior. |
| **N13 — Um parâmetro** | Fixar `r₀ = 1,5R_T` e a direção tangencial. Um único controle visual de `v₀` atualiza seta, previsão e classificação. Em estados selecionados, soltar o corpo e mostrar seu destino. Retornar ao mesmo início antes de ajustar outra vez. | Manter uma referência espacial comum. Se abrir para a trajetória extensa, conservar o ponto de lançamento identificável. A velocidade inicial só é ajustada com o lançamento reinicializado. |
| **N14 — Impacto** | Continuar a experiência do caso que colide: aproximar o encontro com a superfície e parar o corpo no primeiro impacto. Só então revelar a continuação matemática violeta tracejada através da Terra. | Preservar o ponto de colisão como âncora. Ao tornar a Terra translúcida, manter contorno e identificação para que a continuação não pareça um voo físico. |
| **N15 — Newton** | Retomar o conjunto de trajetórias em linguagem de diagrama: reduzir detalhe superficial e conservar montanha e curvas. Entrar apenas “Experimento mental de Newton”. | Reenquadrar a mesma construção; a transformação de estilo faz a ponte histórica. Depois recuperar volume e iluminação para a síntese. |
| **N16 — Pedra, satélite, Lua** | Usar correspondência de enquadramento entre a queda perto do solo, o satélite e o sistema Terra–Lua. O aumento de escala conduz a montagem. | Identificar a troca de sistema e escala: a pedra não se transforma fisicamente em satélite ou Lua. A mesma lei conecta os casos. |
| **N17 — Baricentro** | Mostrar o movimento conjunto e conectar a visão geral a uma ampliação da região terrestre. Marcar centro da Terra e baricentro como pontos diferentes. A Terra executa a pequena órbita; o baricentro permanece fixo no referencial do centro de massa. | Na ampliação local, preservar `r_b/R_T ≈ 0,733`, mantendo o ponto dentro da Terra. A ligação com a visão geral impede que pareçam duas simulações independentes. |
| **N18 — Síntese** | Reencontrar a montanha da abertura e a trajetória que não toca o chão. Retomar as duas frases aprovadas com o corpo em movimento. Retirar os overlays de conteúdo até restarem Terra, satélite e trajetória, com a marca discreta. | Abrir e estabilizar no plano orbital final. A conclusão visual responde à imagem inicial, sem acrescentar uma nova demonstração. |

### Abertura: o padrão de elaboração que deve orientar o restante

1. **Reconhecer a situação.** A montanha ocupa parte relevante do quadro; o canhão aponta ao longo da tangente local, e a pedra é visível antes do disparo.
2. **Sentir a tentativa.** A câmera acompanha o avanço e conserva o solo como referência. O impacto interrompe o voo com uma marca discreta, sem explosão decorativa.
3. **Perceber a escala.** Cada tentativa mais rápida exige ver mais superfície. A abertura da câmera nasce dessa necessidade e revela a curvatura.
4. **Descobrir a órbita.** Na última tentativa, a câmera abre o suficiente para mostrar a volta completa, preservando o movimento do mesmo corpo. A montanha perde detalhe naturalmente com a distância.
5. **Investigar o mecanismo.** A cena continua em N02; a seta de gravidade cria a pergunta que o bloco seguinte resolve.

## 8. Física preservada e verificações objetivas

Foram recalculados diretamente a partir das constantes aprovadas:

| Grandeza a 400 km | Valor |
| --- | --- |
| Raio orbital | 6.771 km |
| Velocidade circular | 7,67260 km/s |
| Gravidade | 8,69425 m/s² |
| Período | 92,4143 min |
| Gravidade relativa à superfície | 0,88534 |
| Queda local `gt²/2`, em 1 s | 4,34712524 m |
| Desvio exato do círculo em relação à tangente, em 1 s | 4,34712478 m |

A diferença entre os dois últimos valores é aproximadamente `4,65 × 10⁻⁷ m`. Isso confirma os arredondamentos do pacote e a adequação da aproximação local. Não transforma a representação ampliada em desenho de escala uniforme.

**Restrições que continuam valendo:**

- Modelo newtoniano, SI, Terra esférica, sem atmosfera e sem rotação; massa do satélite desprezível.
- Terra fixa no núcleo da explicação; o modelo de dois corpos é explicitado no fechamento Terra–Lua.
- A gravidade fornece a aceleração centrípeta; não adicionar uma segunda força centrípeta.
- `Δv ≈ aΔt` no passo finito; `dv = a dt` na relação diferencial.
- N07 mantém “aproximação local · t = 1 s” e “curvatura ampliada para visualização”. Identificar também que as escalas horizontal e vertical diferem.
- Em N07, a curvatura medida é a da circunferência orbital de raio `r`, em relação à tangente naquele ponto. Não afirmar que a superfície terrestre, de raio `R_T`, apresenta a mesma medida de 4,35 m.
- N09 preserva a diferença entre gravidade e peso aparente; a vista interna não deve simular forças de apoio que não existem no caso ideal.
- N10 compara casos; N11→N12 generaliza o modelo; N13 reinicializa lançamentos. Nenhuma dessas mudanças representa uma manobra orbital espontânea.
- Em N13, `.70`, `.92`, `1.00`, `1.20` e `1.44` vezes a velocidade circular são referências internas aprovadas. Trajetória ligada e colisão são classificações independentes.
- O corpo para no primeiro impacto. A continuação através do planeta é exclusivamente matemática e identificada em N14.
- Não introduzir derivação de energia orbital, velocidade de escape, segunda lei de Kepler ou uma explicação nova de transferência orbital.

## 9. Caminho técnico proposto, sem executar

**Base recomendada:** manter o modelo orbital existente como fonte comum e reconstruir sua apresentação no Manim com câmera, geometria de aparência volumétrica e projeção coerente. Trajetória, corpo, vetores, cotas e superfícies precisam obedecer à mesma transformação de câmera. Objetos de interface — header e marca — permanecem fixos à tela.

O briefing anterior fixou `solido_3d: nenhum` e Manim 2D. A solicitação atual reabre a direção visual. A proposta é ultrapassar a aparência de disco plano, usando volume e vistas espaciais onde esclarecem a situação; os trechos de medição conservam a vista perpendicular. **Isso é uma mudança visual proposta, ainda não registrada como decisão aprovada.**

Foi consultado o arsenal existente. `orbita_kepleriana` tem aparência aprovada e pode servir de referência visual, mas seu recurso atual representa elipses com centro fixo; não cobre órbitas abertas, impactos ou dois corpos. Sua câmera e fase próprias também precisariam corresponder à apresentação do Manim. Portanto, não é um substituto único para N01–N18. `poco_gravitacional` introduziria a imagem de potencial, fora do foco desta unidade; não o recomendo aqui.

Se, na implementação futura, uma tomada volumétrica exigir Blender ou ajuste de asset, esse encaixe deve ser especificado para a tomada concreta, sem fazer o vídeo depender de um segundo movimento orbital desconectado do modelo. O ambiente validado e as dependências existentes são preservados. A presente revisão não instala ferramentas, integra sólidos ou altera templates.

## 10. Critérios visuais para uma futura revisão

Estes critérios descrevem o resultado esperado; não autorizam renders nesta rodada.

| Ponto | Condição de aceitação |
| --- | --- |
| Identidade | Header `GRAVITAÇÃO · ÓRBITAS` à esquerda; marca oficial no alto à direita; nenhum `NN/18` público. |
| Abertura | É possível identificar montanha, canhão, direção do disparo e pedra sem depender de um parágrafo ao lado. |
| Câmera | O início contém plano próximo, acompanhamento e revelação global motivados pelo alcance das tentativas. |
| Continuidade | N01→N02, N05→N06 e N07→N08 preservam uma âncora visual reconhecível. |
| Volume | A Terra tem iluminação e oclusão coerentes; o satélite não aparece atravessando uma esfera opaca por erro de camadas. |
| Projeção | A perspectiva não transforma visualmente uma órbita circular em uma elipse física sem explicação. |
| N04 | A origem comum e a diferença vetorial são construídas em tamanho suficiente para leitura. |
| N06 | A passagem central da relação circular à velocidade orbital continua visível, em vez de saltar ao resultado. |
| N07 | O detalhe nasce da órbita; tempo, distâncias e avisos permanecem legíveis durante a ampliação. |
| N09 | A animação mostra o significado de cair junto antes de exigir leitura da explicação. |
| N10–N13 | Novos casos físicos são identificados; a câmera e os morphs não sugerem impulsos ou transferências inexistentes. |
| N14 | Impacto e continuação matemática são distinguíveis mesmo sem cor, pelo movimento, traço e rótulo. |
| N17 | Baricentro visivelmente dentro da Terra na ampliação; proporção local preservada. |
| Equações | Mesma grandeza conserva a cor entre desenho e fórmula; sinais, expoentes e unidades têm contraste. |
| Legibilidade | Câmera estável nas leituras importantes; conteúdo crítico respeita a área segura e a faixa inferior reservada. |
| Encerramento | A imagem final retoma a pergunta inicial e sustenta as frases aprovadas com movimento compreensível. |

Quando houver autorização para implementar, a validação deve mirar primeiro os pontos que podem reprovar a nova linguagem — abertura, transição global/local de N07 e leitura espacial — sem reabrir o storyboard nem impor uma nova produção isolada N01–N06. O fechamento visual completo continua sendo da unidade N01–N18. Os 6min26,7s do preview atual não são uma duração final congelada.

## 11. Fontes e proveniência

- Pacote fornecido: [ZIP original](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0007_orbita_queda_continua/avaliacao_visual_completa_0007.zip).
- Referência temporal: [timing do pacote](./referencias_zip/timing_preview_revisado.json); [QA recebido](./referencias_zip/qa_visual.md); [validação recebida](./referencias_zip/validacao_fisica.json).
- Situação operacional: [estado atual do repositório](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/docs/estado_atual.md).
- Identidade: [documento vigente](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/docs/identidade_visual.md); [decisões](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/docs/decisoes.md).
- Gauss 1: [header, logo e continuidade](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0001_lei_gauss/cena.py:620); [prancha 1 da revisão 2.1](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0001_lei_gauss/frames_avaliacao_v2_1/folha_01.png); [prancha 7](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0001_lei_gauss/frames_avaliacao_v2_1/folha_07.png).
- Gauss 2: [paleta e hierarquia](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0002_lei_gauss_casos_classicos/cena.py:87); [header e logo](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0002_lei_gauss_casos_classicos/cena.py:1084); [uso de MF-Tools](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0002_lei_gauss_casos_classicos/cena.py:1607).
- Órbita: [identidade e reconstrução de telas](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0007_orbita_queda_continua/cena.py:130); [N01](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0007_orbita_queda_continua/cena.py:184); [N13](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0007_orbita_queda_continua/cena.py:524); [ficha](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0007_orbita_queda_continua/ficha.md); [modelo físico](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0007_orbita_queda_continua/modelo_orbital.py).
- Composição: [área segura horizontal](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/template/layout_horizontal.py:19).
- Arsenal: [ficha de órbita kepleriana](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/experimentos/blender/arsenal/solidos/orbita_kepleriana.json).

**Entrega desta rodada:** proposta editorial, evidências extraídas e conferência numérica dos valores de referência. Nenhum arquivo de produção foi alterado; nenhum novo render Manim, voz, legenda, master, commit ou publicação foi realizado.
