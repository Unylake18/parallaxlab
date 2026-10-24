# vid_0024 — correções de layout, legibilidade e ritmo

Refine o preview atual de `vid_0024_carga_helice`. O usuário aprovou o conteúdo e solicita uma rodada de acabamento visual: remover sobreposições, ampliar e valorizar o gráfico, distinguir a velocidade paralela e desacelerar momentos importantes.

Preservar a física, as derivações, os gráficos sincronizados, a comparação entre sinais e a representação integralmente em Manim 2.5D.

## Arquivos e escopo

Unidade:
`C:\Users\KaioOrtiz\PycharmProjects\manim-fisica\videos\vid_0024_carga_helice`

Ler:
- `docs/estado_atual.md`: somente contexto operacional necessário.
- `docs/identidade_visual.md`: paleta e tipografia.
- `videos/vid_0024_carga_helice/cena.py`.
- `media_polimento/estados.json`.
- Preview e quadros de `analise_temporaria_preview_polimento_0024`.

Alterar somente o `cena.py` da unidade. Gerar o novo preview em uma pasta distinta, preservando os anteriores.

Não reler o repositório inteiro nem investigar vídeos anteriores sem necessidade concreta.

## 1. Reorganizar o espaço antes de ajustar fontes

Separar claramente:
- Cabeçalho: título e subtítulo.
- Geometria: campo, plano, trajetória e vetores.
- Apoio didático: gráfico ou álgebra.
- Área inferior reservada para futuras legendas.

Criar posições consistentes para essas áreas, evitando coordenadas independentes que provoquem novas colisões.

Textos e fórmulas devem ficar inteiramente dentro ou inteiramente fora do plano desenhado, com folga visível. Nenhum contorno deve atravessar caracteres, índices, frações ou caixas de resultado.

Priorizar reposicionamento e composição. Reduzir fonte apenas quando necessário, preservando leitura no celular.

Verificar as posições durante todo o movimento, não apenas no quadro inicial.

## 2. Dar mais espaço e tempo ao gráfico

Trecho atual: aproximadamente 00:26–00:34.

O gráfico está muito próximo do plano: em 00:28, a borda inferior do plano praticamente encosta na borda superior do painel. Os dois gráficos também estão baixos em altura.

Modificar `graphs()` e o enquadramento desse bloco:
- Mover o painel um pouco para baixo e ajustar a geometria acima para manter uma separação clara.
- Aumentar a altura útil das curvas, rótulos e eixos.
- Reposicionar ou remover textos inferiores que disputem espaço com o painel.
- Manter `t/T`, os pontos e o cursor legíveis e sincronizados.
- Preservar a relação entre componentes variáveis e módulos constantes.

Planejar aproximadamente 10–12s de exposição útil, além das entradas e saídas. Distribuir esse tempo entre apresentação do painel, movimento sincronizado e uma breve pausa de leitura.

Usar uma explicação visual curta, por exemplo:
**“As componentes oscilam; os módulos permanecem constantes.”**

Evitar repetir essa mesma informação em vários lugares. Não acrescentar novos gráficos ou conteúdo físico.

## 3. Distinguir a velocidade paralela

A componente paralela atual, em ciano, perde contraste perceptivo entre trajetória e linhas azuis do campo.

Adotar para `v_parallel` um verde claro suficientemente distinto do azul, conforme sugestão do usuário. Valor inicial possível: `#63E6BE`.

Essa é uma escolha desta rodada; não registrar que esse hexadecimal já constava da paleta aprovada.

Aplicar a cor consistentemente:
- Seta e rótulo de `v_parallel`.
- Termos correspondentes nas equações.
- Guias da decomposição.
- Indicações do avanço longitudinal associadas à componente.
- Comparação de velocidade paralela.

Manter:
- Campo magnético: azul.
- Velocidade total: branco.
- Componente transversal: violeta.
- Força: magenta.

Não substituir globalmente o ciano: trajetória, marca e outros usos podem permanecer como estão.

Preservar escala comum e fechamento geométrico da soma vetorial.

## 4. Corrigir o layout da álgebra

Trecho atual: aproximadamente 01:05–01:34.

Problemas confirmados:
- Em torno de 01:19–01:22, a referência `r = m v_perp / (|q| B)` encosta na borda inferior do plano.
- Depois, a referência de `omega_c` ocupa a mesma região.
- A fórmula ativa fica próxima demais dessas referências.

Reorganizar `radius_algebra()` e `period_algebra()`:
- Reservar uma área própria para a equação ativa.
- Quando a fórmula anterior precisar continuar visível, colocá-la em uma posição de referência claramente separada.
- Preferir referências lado a lado em uma faixa abaixo da geometria, se houver espaço; manter a derivação ativa em outra linha.
- Ajustar tamanho e posição do plano/círculo para acomodar a álgebra com folga.
- Retirar cada referência assim que deixar de contribuir para a passagem seguinte.

Preservar as operações e os mapeamentos MF-Tools existentes. Ao reposicionar fórmulas, fazer caixas, riscos de cancelamento e objetos auxiliares acompanharem a nova posição.

Aumentar o tempo de percepção dos passos importantes. Evitar sequência contínua de cancelamento, compactação, substituição e resultado sem pausas curtas.

Não alterar o conteúdo matemático nem refazer glyph maps que continuem funcionando.

## 5. Reposicionar “saindo da tela”

Na vista transversal, o texto “saindo da tela” atravessa a borda superior do plano.

Manter a indicação, pois ajuda a interpretar a orientação do campo.

Agrupar `⊙ B` e “saindo da tela” em uma pequena legenda:
- Fora do plano, com margem clara.
- Afastada do título e dos rótulos dos vetores.
- Sem tocar na borda superior durante a cena.

## 6. Remover repetição e reduzir poluição textual

No trecho próximo de 01:38–01:44:
- Manter **“Círculo + translação = hélice”** no título.
- Remover a repetição inferior em `MathTex`.
- Não preencher automaticamente o espaço liberado com outra frase.
- Usar a área para valorizar as projeções e, quando chegar o momento, a relação do passo.

Revisar os demais blocos:
- O texto inferior só deve permanecer quando acrescentar informação ao título e subtítulo.
- Remover frases genéricas ou repetidas.
- Preservar condições e explicações indispensáveis.
- Considerar que haverá narração e legendas posteriormente.

Textos em linguagem natural devem usar o helper tipográfico oficial `screen_text`/`words`, com Space Grotesk. Reservar `MathTex` para matemática e pequenos elementos matemáticos.

## 7. Reposicionar rótulos e medidas

O rótulo “círculo” fica junto à borda do plano. Colocá-lo um pouco dentro, em uma região livre, sem tocar na curva ou nas projeções.

Nas comparações:
- Separar `r_0` e `r_1`.
- Afastar as medidas da borda inferior do plano.
- Manter associação inequívoca entre rótulo, seta e condição.
- Organizar também `p_0` e `p_1`, preservando leitura dos índices.
- Usar duas linhas de medida com espaço suficiente, em vez de setas quase encostadas.

Conferir essas posições para B, velocidade transversal e velocidade paralela.

## 8. Redistribuir o ritmo

Não desacelerar uniformemente o vídeo inteiro.

Dar mais tempo para:
- Leitura e observação do gráfico.
- Operações algébricas relevantes.
- Reconhecimento das medidas nas comparações.
- Síntese final.

Recuperar tempo em transições repetidas, reapresentações e textos que forem removidos.

Na síntese atual, círculo e reta são percorridos em apenas 1,6s cada, e a hélice em 2,2s. Ampliar o tempo desses movimentos para que os três casos sejam reconhecíveis, sem atropelar as mudanças de condição.

A frase final termina de entrar por volta de 02:47,77 e começa a desaparecer imediatamente. Manter:
**“Giro transversal + avanço paralelo = hélice.”**
totalmente visível por aproximadamente 2,5–3s antes da saída.

Preservar o end card somente com `@labparallax`.

Recalcular os marcos `until()` e atualizar a verificação rígida de duração atual. Buscar redistribuição próxima da duração existente; não sacrificar legibilidade para manter exatamente 170,85s.

## Validação mínima e parada

Gerar um preview completo em 540×960/15 fps, em novo caminho.

Inspecionar especialmente:
- Gráfico: tamanho, bordas e tempo de exposição.
- Contraste de `v_parallel`.
- Fórmulas de referência de r e omega.
- Legenda “saindo da tela”.
- Rótulos “círculo”, `r_0`, `r_1`, `p_0` e `p_1`.
- Ausência da frase inferior duplicada.
- Pausa de leitura da síntese final.
- Espaço para futuras legendas.

Conferir quadros intermediários das animações de fórmulas, pois as colisões podem surgir durante o movimento. Preservar o sincronismo físico dos gráficos e o fechamento da decomposição.

Não alterar física, narrativa central, dependências, template global ou infraestrutura. Não produzir voz, legendas, render final, commit ou push. Não investigar Blender.

Parar após entregar o novo preview completo, com QA visual focal concluído, caminho do MP4 e resumo curto das mudanças. Rerenderizar somente se houver um defeito concreto.