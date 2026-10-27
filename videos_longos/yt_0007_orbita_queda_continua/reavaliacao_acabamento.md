# Órbita — reavaliação da repaginação e ajustes de acabamento

**Parallax Lab · yt_0007 · 18/10/2026**  
**Etapa: revisão do preview. Sem alteração da implementação.**

A nova versão já encontrou uma direção de arte melhor. A abertura próxima da montanha, o acompanhamento dos lançamentos, a iluminação do globo e as mudanças de escala devem ser preservados. A próxima rodada deve corrigir definição, identificação dos objetos, continuidade das equações e apresentação da Lua sobre essa base.

**Restrições reafirmadas pelo usuário:** somente Manim; preservar física e storyboard conceitual; usar a paleta aprovada; retirar o amarelo. As especificações abaixo são recomendações de revisão, não alterações já realizadas.

## 1. O que foi examinado

Pacote `avaliacao_repagina_visual_0007.zip`: 58 quadros de avaliação, dez pranchas de marcos, pranchas temporais com 12 instantes por bloco, documentação e MP4. Foram examinadas as dez pranchas de marcos, as pranchas temporais de N01, N05, N06, N11, N16 e N17, seis quadros nativos e 18 amostras adicionais extraídas diretamente do MP4. Não se alega inspeção visual individual de todos os frames.

A leitura do vídeo confirmou **960×540, 15 fps, 6.506 quadros, 433,73 s e ausência de áudio**. O relatório recebido registra CRF 23, próprio deste preview. Foram consultados `encenacao.py`, `geometria_visual.py`, os trechos pertinentes da ficha, a identidade vigente e o estado operacional.

Evidências extraídas do MP4:

- [Zoom e troca de representação em N01](C:/Users/KaioOrtiz/.codex/.chatgpt-projects/g-p-6ab183a145388191aed91cc173805989/outputs/reavaliacao_repagina_0007/zoom_N01.jpg).
- [Entrada das expressões em N05–N06](C:/Users/KaioOrtiz/.codex/.chatgpt-projects/g-p-6ab183a145388191aed91cc173805989/outputs/reavaliacao_repagina_0007/algebra_N05_N06.jpg).
- [Apresentação da Lua e do baricentro](C:/Users/KaioOrtiz/.codex/.chatgpt-projects/g-p-6ab183a145388191aed91cc173805989/outputs/reavaliacao_repagina_0007/lua_N16_N17.jpg).

## 2. Definição da Terra durante os zooms

**Constatação:** a perda de definição é visível no próprio quadro nativo, por exemplo em N01 a 10 s. O globo usa uma imagem procedural RGBA de **512×512**. A câmera amplia essa imagem; somente nos aumentos extremos troca para um horizonte vetorial. O código permite um diâmetro projetado próximo de 3.120 pixels no preview antes dessa troca, mais de seis vezes a largura da imagem de origem. O recorte visível continua sofrendo essa ampliação, mesmo quando grande parte do globo está fora da tela.

Portanto, aumentar apenas a resolução do vídeo final não resolve a causa. A diferença de aparência entre o horizonte vetorial e a textura também torna a troca perceptível.

**Ajuste proposto, dentro do Manim:**

1. Manter a silhueta e as referências geométricas da Terra nítidas por construção vetorial.
2. Gerar o acabamento procedural com densidade suficiente para o enquadramento efetivamente exibido. Em grandes aproximações, calcular o recorte visível na resolução de saída, em vez de ampliar a imagem inteira de 512 pixels.
3. Compartilhar contorno, iluminação e material entre a visão de globo e a visão local. A troca de representação precisa ocorrer enquanto ambas têm definição suficiente e posições coincidentes.
4. Retirar detalhe geográfico que deixe de ser legível na escala local, de forma progressiva. O relevo e a curvatura continuam como referências; a textura não precisa carregar todos os planos.
5. Dimensionar o cache pela memória e pelo trecho necessário. Não multiplicar indiscriminadamente a resolução das 24 imagens atualmente possíveis no cache.

Uma imagem de maior resolução para planos médios pode ajudar, mas não é solução única para todos os zooms. A escolha deve considerar o maior tamanho projetado, incluindo o destino em 1080p. Não há necessidade demonstrada de trocar o ambiente, renderer ou ferramenta.

**Aceite:** nos movimentos de ida e volta de N01, N07/N08, N16 e N18, não deve aparecer uma faixa de pixels ampliados, um salto de contorno ou uma troca abrupta de material. O custo da solução ainda precisa ser medido na implementação; não foi estimado nesta revisão.

## 3. Canhão: reconhecer antes de nomear

**Constatação:** no plano próximo de 3,4 s, o objeto é formado principalmente por um tubo retangular, uma roda e uma base. Sua silhueta não separa claramente boca, corpo e suporte. A pedra e a seta tangente também disputam esse pequeno espaço.

**Ajuste proposto:** construir no próprio Manim um canhão esquemático com tubo de contorno arredondado, espessura na boca, culatra identificável, suporte e rodas coerentes com a vista lateral. Usar luz e sombra derivadas da paleta; conservar a elegância simples da montanha, sem acrescentar detalhes menores do que a imagem permite ler.

Na primeira aproximação, incluir uma chamada **“canhão idealizado”**, com linha curta apontando para o objeto. Identificar também **“pedra”** e, no momento apropriado, **“velocidade inicial”**. Essas chamadas entram em sequência e saem antes do acompanhamento do voo. A seta de velocidade deve nascer na pedra, diferenciada do tubo.

O disparo pode usar um pulso breve de luz para marcar a saída. Manter o modelo sem atmosfera e sem propulsão durante o voo; fumaça e efeitos de explosão não são necessários. O aviso “montanha idealizada · sem atmosfera” permanece.

**Aceite:** mesmo sem o rótulo, a forma deve ser reconhecível; o rótulo confirma a identificação. Não usar a chamada como substituto permanente da melhoria da arte.

## 4. Equações: construir a origem e a operação

**Constatação:** existe cor em alguns símbolos e há uma passagem com MF-Tools em N06. Entretanto, N05 introduz as duas expressões por aparição; N06 limpa essas expressões e faz surgir uma igualdade nova. Em N11, a substituição da velocidade e a simplificação do radical continuam rápidas. No quadro de 236,9 s, a parte superior da fórmula também encosta na órbita. Esses pontos mantêm a sensação de tela expositiva.

### N05–N06: da atração gravitacional à condição circular

Apresentar o contexto físico dentro dos blocos existentes, com uma relação ativa por vez:

| Passo | Ligação verbal sugerida | Construção visual |
| --- | --- | --- |
| Identificar | “A Terra atrai a pedra. A massa da Terra é M; a da pedra é m.” | Rótulos `M` e `m` ligados aos corpos; cota `r` medida a partir do centro terrestre. |
| Lei gravitacional | “Pela gravitação de Newton, o módulo dessa força é…” | A seta para o centro recebe `F_g`; construir `F_g = GMm/r²`, trazendo os símbolos das referências visuais. |
| Movimento circular | “Para seguir uma circunferência, a aceleração precisa apontar para o centro e ter módulo v²/r.” | Destacar tangente, raio e curvatura; apresentar `a_c = v²/r`. Não desenhar outra força. |
| Conectar | “Neste modelo, é a gravidade que fornece essa aceleração.” | Relacionar a resultante radial `m v²/r` à força gravitacional já identificada. |
| Igualar | “Por isso, na órbita circular…” | Construir `GMm/r² = m v²/r` a partir das relações anteriores, sem apagar tudo e começar outra tela. |
| Cancelar | “A massa da pedra aparece nos dois lados e se cancela.” | Destacar os dois fatores `m` e realizar o cancelamento explícito com MF-Tools. Resulta `GM/r² = v²/r`. |
| Isolar | “Multiplicando os dois lados por r…” | Construir `v² = GM/r`, mostrando a operação e o cancelamento correspondente. |
| Interpretar | “Essa é a velocidade necessária para a órbita circular desse raio.” | Extrair a raiz positiva e chegar a `v_orb = √(GM/r)`; voltar a destacar velocidade e raio no desenho. |

Essas frases são pontes curtas para a futura narração ou para indicações temporárias de preview. Não constituem produção de voz nem uma nova aula sobre forças. “Centrípeta” descreve o papel da resultante; não há gravidade mais uma segunda força centrípeta. A aceleração gravitacional obtida da lei é `g = F_g/m = GM/r²`.

### N07: preservar o momento de compreensão

Apresentar as medidas antes das contas: 1 s físico → 7,67 km na tangente → cerca de 4,35 m de queda → cerca de 4,35 m de desvio da circunferência orbital. Usar chamadas **“queda”** e **“curvatura da órbita”**. Só depois construir a relação matemática curta.

Manter os avisos de aproximação e escalas distintas. A curvatura comparada é a da circunferência orbital de raio `r`; não confundir com a superfície de raio `R_T`. A fórmula de queda e a de curvatura não devem competir com uma terceira linha pequena: transformar as relações em sequência, com espaço de leitura.

### N10–N12: da volta completa à terceira lei

- Identificar os dois casos como **“órbita baixa”** e **“órbita alta”**, conservando o relógio físico comum e a distinção entre casos independentes.
- Em N11, marcar partida, percurso e retorno. A chamada **“uma volta”** dá origem ao símbolo `T`; o comprimento destacado dá origem a `2πr`.
- Fazer a ponte: “O período é o comprimento da volta dividido pela velocidade”. Construir `T = 2πr/v`.
- Retomar brevemente `v = √(GM/r)` e copiar seu lado direito para o denominador. A substituição deve ser acompanhável, sem surgir pronta.
- Mostrar a simplificação `T = 2πr √(r/GM) = 2π √(r³/GM)` e só depois elevar os dois lados ao quadrado.
- Em N12, identificar **“generalização: órbita elíptica”** e o semieixo `a`. A fórmula anterior persiste enquanto `r³` é substituído por `a³` no novo caso. Não sugerir deformação espontânea da órbita.
- Reposicionar a equação em uma região própria, separada do contorno da Terra e da trajetória. Não reduzir o corpo da matemática para fazê-la caber.

### Uso de MF-Tools nesta rodada

Aplicar mapas de glifos nos cancelamentos de `m` e `r`, na substituição da velocidade em N11 e na simplificação que combina os fatores de raio. A animação deve explicar cada operação. A continuidade de N05→N06 também depende de conservar objetos e símbolos, não apenas de acrescentar um efeito à fórmula final.

Estabilizar as expressões e as cores antes dos mapas. Definir as grandezas por elementos LaTeX explícitos, evitando depender apenas da semelhança geométrica entre glifos para atribuir semântica. Manter a correspondência ao longo de toda a cadeia; não deixar cópias residuais, sinais atravessados ou resultados antecipados. Usar uma transição simples quando uma correspondência seria enganosa.

## 5. Paleta: retirar amarelo e tornar a cor perceptível

O amarelo `#FFC24D` foi sugerido na revisão anterior por existir como acento em Gauss 1. **Essa recomendação fica retirada para esta unidade**, conforme a instrução atual do usuário. A semântica abaixo usa somente as seis cores centrais documentadas na identidade:

| Uso nesta unidade | Cor |
| --- | --- |
| Fundo | Azul muito escuro `#050816` |
| Terra, fonte gravitacional e `M` | Azul `#267BFF` |
| Gravidade, `F_g`, `g` e aceleração gravitacional | Ciano `#35D9FF` |
| Raios, distâncias e semieixo `r`, `R_T`, `s`, `a` | Violeta `#745CFF` |
| Tempo e período `t`, `T`; relógio e percurso temporal destacado | Magenta `#EA63FF` |
| Pedra, velocidade, `m`, constantes, operadores e unidades | Branco `#F5F7FF` |

Essa é uma aplicação semântica local proposta, não uma alteração global do projeto. Sombras, transparências e gradações de iluminação devem derivar dessas famílias; não acrescentar outro matiz para substituir o amarelo. O logo oficial permanece intacto.

O vídeo já contém azul, ciano e violeta, mas os acentos são pequenos e várias informações ficam pouco salientes. Para a cor participar da explicação:

- Destacar juntos o elemento do desenho e o símbolo correspondente.
- Em N05–N06, usar ciano na seta e em `F_g`/`g`, violeta na cota e em `r`, azul em `M`; manter sinais e unidades brancos.
- Em N11–N12, usar magenta no relógio, em `T` e no destaque de uma volta; violeta no raio/semieixo e no símbolo correspondente.
- Colorir uma palavra-chave dos títulos quando útil, por exemplo “gravidade”, “velocidade” ou “volta”, sem aplicar um degradê indiscriminado à frase inteira.
- Na identificação do baricentro, combinar marcador distinto e rótulo; não depender apenas da diferença de cor para distingui-lo do centro terrestre.

A retirada do amarelo abrange avisos, relógios, arcos e fórmulas em N04, N07, N09, N10, N11 e N12, além de qualquer quadro ou trecho intermediário reutilizado no preview. Conferir o arquivo montado, não apenas a definição de uma constante.

## 6. Lua: identificação, mecanismo e baricentro em sequência

**Constatação:** o trecho final de N16 mostra Terra e Lua muito pequenas, com a Lua como um ponto branco sem rótulo. A abertura de escala dura aproximadamente 3 s, seguida de cerca de 4 s de movimento/pausa. Em N17, a visão geral e o detalhe terrestre já entram com pouca apresentação dos pontos. A Lua pode ser visível sem ser identificável.

**Tratamento proposto, dentro de N16–N17:**

1. **Reconhecer a Lua.** Apresentá-la em ampliação com um disco sombreado e poucas crateras vetoriais legíveis, feito no Manim. Rotular **“Lua”** e **“Terra”**. Identificar os tamanhos ampliados quando aplicável.
2. **Reconhecer o mecanismo.** Mostrar a velocidade tangente e a atração para a Terra: “A Lua também avança enquanto a gravidade curva seu movimento”. A animação precisa ter tempo para mostrar mudança de direção; não basta abrir a câmera e manter dois pontos.
3. **Revelar a escala.** Abrir para a distância do sistema e conservar os rótulos ligados aos corpos. Se os marcadores forem ampliados, avisar isso e preservar as distâncias dos centros.
4. **Mostrar que a Terra também se move.** Em N17, deslocar a atenção para a Terra antes de abrir o detalhe. O pequeno movimento terrestre motiva a procura do ponto comum.
5. **Nomear o baricentro.** Conectar a visão geral à ampliação. Apresentar **“centro da Terra”** e **“baricentro”** em momentos separados, com marcadores distintos. Só então mostrar os dois movimentos em torno do ponto comum.
6. **Sustentar a conclusão.** Manter o baricentro fixo no referencial do centro de massa e visivelmente dentro da Terra na ampliação, preservando `r_b/R_T ≈ 0,733`. O número pode ser secundário; reconhecer o que se move e em torno de quê é o objetivo principal.

O ganho vem de ordenar identificação e demonstração. Acrescentar cerca de **10–15 s úteis ao conjunto N16–N17** é uma referência editorial inicial, sujeita ao movimento e à leitura; não é duração final obrigatória. Se for preciso redistribuir ritmo, revisar esperas repetidas em N13, hoje com aproximadamente 77 s, preservando seus cinco estados. Não acrescentar uma nova derivação lunar ou novas leis de Kepler.

## 7. Escritas superiores propostas

Manter o header **“GRAVITAÇÃO — ÓRBITAS”**, a marca no alto à direita e a ausência do contador. A revisão é dos títulos de conteúdo. Frases sobre o fenômeno substituem descrições de operação interna, como “ajustar, depois lançar”.

| Cena | Título proposto |
| --- | --- |
| N01 | E se lançássemos a pedra cada vez mais rápido? |
| N02 | Ele continua caindo. |
| N03 | Sem gravidade, seguiria em linha reta. |
| N04 | A gravidade muda a direção da velocidade. |
| N05 | A gravidade fornece a aceleração. |
| N06 | Qual velocidade mantém a órbita circular? |
| N07 | Quanto ele cai em um segundo? |
| N08 | A queda acompanha a curva da órbita. |
| N09 | Por que os astronautas flutuam? |
| N10 | Mais alto, mais devagar. |
| N11 | Quanto tempo dura uma volta? |
| N12 | E quando a órbita é uma elipse? |
| N13 | Só a velocidade inicial muda. |
| N14 | A Terra está no caminho. |
| N15 | O canhão de Newton. |
| N16 | A Lua também está caindo. |
| N17 | A Terra também se move. |
| N18 | Preservar as duas frases aprovadas: “Orbitar não é vencer a gravidade.” → “É cair… e continuar errando o chão.” |

Os títulos não devem se acumular com longas notas logo abaixo. Identificações como “novo caso” e avisos de escala permanecem como apoio temporário quando necessários. Manter Space Grotesk nos textos e MathTex na matemática.

## 8. Prioridades e revisão mínima da próxima implementação

| Prioridade | Resultado esperado |
| --- | --- |
| 1 — Definição | Corrigir o globo e a passagem para horizonte, preservando os movimentos de câmera já bem recebidos. |
| 2 — Identificação | Canhão reconhecível com chamada inicial; Terra, Lua, centro terrestre e baricentro identificados no momento certo. |
| 3 — Explicação | Equações construídas a partir do fenômeno e das relações anteriores, com operações explícitas e uso dirigido de MF-Tools. |
| 4 — Identidade | Eliminar amarelo; aplicar cores aprovadas com mais presença e consistência; revisar títulos e separação entre fórmulas e desenho. |
| 5 — Lua | Dar tempo e sequência à apresentação do mecanismo e do baricentro. |

Os arquivos centrais de uma futura rodada são `geometria_visual.py` e `encenacao.py`, dentro da unidade. Preservar o modelo orbital, os valores de referência, os casos de lançamento, as condições de impacto e o storyboard. Não usar Blender, instalar dependências, alterar templates globais, produzir voz, gerar master ou publicar nesta fase.

A validação futura pode começar nos trechos afetados: zoom de N01 e passagem local/global; cadeia de equações N05–N06/N11; Lua e baricentro. Como o defeito de definição depende da densidade da imagem, um trecho curto com o pior zoom precisa ser conferido também na resolução prevista para o final, sem produzir um master completo. Os demais pontos podem ser avaliados nos previews e quadros correspondentes. QA completo pertence ao fechamento da unidade.

**Condição para encerrar a revisão visual:** movimento nítido, objetos identificáveis, símbolos ligados ao desenho, operações acompanháveis, ausência de amarelo, nenhuma fórmula sobreposta à órbita e Lua apresentada como parte da explicação. A nova base visual deve ser preservada durante esses ajustes.

## Referências locais

- [ZIP avaliado](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0007_orbita_queda_continua/avaliacao_repagina_visual_0007.zip).
- [Relatório recebido](C:/Users/KaioOrtiz/.codex/.chatgpt-projects/g-p-6ab183a145388191aed91cc173805989/outputs/reavaliacao_repagina_0007/referencias/documentacao/qa_repagina.md) e [timing](C:/Users/KaioOrtiz/.codex/.chatgpt-projects/g-p-6ab183a145388191aed91cc173805989/outputs/reavaliacao_repagina_0007/referencias/documentacao/timing_repagina.json).
- [Globo procedural e transição de escala](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0007_orbita_queda_continua/geometria_visual.py:18).
- [Construção atual das expressões](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0007_orbita_queda_continua/encenacao.py:299).
- [Período e generalização](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0007_orbita_queda_continua/encenacao.py:450).
- [Terra–Lua e baricentro](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/videos_longos/yt_0007_orbita_queda_continua/encenacao.py:564).
- [Paleta central documentada](C:/Users/KaioOrtiz/PycharmProjects/manim-fisica/docs/identidade_visual.md:27).

**Entrega desta rodada:** reavaliação fundamentada e especificação dos ajustes. Foram criados apenas este documento e referências de inspeção no espaço de trabalho desta conversa. Nenhum arquivo de produção foi alterado e nenhum novo render Manim foi executado.
