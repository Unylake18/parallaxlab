# E se o ar parasse de frear a chuva?

- id: vid_0019
- série: ABSURDO CALCULÁVEL
- episódio: EP. 02 — confirmado pelo usuário
- formato: curto_vertical
- assunto: arrasto na queda de gotas, velocidade terminal e energia cinética
- pergunta central: “E se o ar parasse de frear a chuva?”
- status: V1.1 conceitualmente aprovada e congelada
- etapa atual: final renderizado e verificado; pronto para postagem pelo usuário
- duração atual: 129,600 s, determinada pelo WAV fornecido; V5 silenciosa de 104 s preservada
- direção visual: Manim-only; sem Blender
- implementação: cena.py — ChuvaSemArrasto019
- roteiro: roteiro.md — fala, tela, animação e objetivo didático
- solido_3d: nenhum
- justificativa de solido_3d: vetores, velocímetro, gotas e barras de energia são melhor explicados em 2D/Manim.

## Premissa hipotética

Uma gota líquida já formada começa praticamente do repouso e cai uma distância vertical Δh. Suprimimos a interação aerodinâmica responsável pelo arrasto e mantemos a gota intacta por hipótese. O restante do cenário permanece igual.

O caso principal fixa Δh = 2 km. Essa distância vertical de queda é um parâmetro do modelo, não uma afirmação sobre a altura típica da chuva.

## Solução/modelo verificado

Chuva real não é queda livre prolongada. A gravidade acelera a gota, mas o arrasto cresce com a velocidade. Quando o arrasto equilibra o peso, a aceleração praticamente zera e surge a velocidade terminal.

No modelo sem arrasto, para uma gota que parte praticamente do repouso:

\[
v = \sqrt{2g\Delta h}.
\]

Para Δh = 2 km:

Adota-se g = 9,81 m/s².

\[
v \approx 198\ \text{m/s} \approx 713\ \text{km/h}.
\]

Gotas que caem a mesma Δh chegam com a mesma velocidade nesse modelo sem arrasto, independentemente da massa.

Para gotas aproximadamente esféricas, de mesma densidade, com diâmetro d:

\[
m = \frac{\rho\pi d^3}{6},\qquad
m \propto d^3.
\]

A energia cinética ao final da queda, no mesmo modelo, é:

\[
E = \frac{1}{2}mv^2 = mg\Delta h.
\]

Portanto, para a mesma Δh:

\[
E \propto d^3.
\]

## Valores numéricos aprovados

Todos os valores abaixo correspondem ao modelo sem arrasto, com a gota mantida intacta por hipótese e Δh = 2 km.

| Grandeza | Valor aprovado |
| --- | --- |
| Distância vertical Δh | 2 km |
| Velocidade final | ≈ 198 m/s ≈ 713 km/h |
| Massa — gota de 2 mm de diâmetro | ≈ 4,19 mg |
| Massa — gota grande de 5 mm de diâmetro | ≈ 65,4 mg |
| Energia cinética — gota de 2 mm de diâmetro | ≈ 0,082 J |
| Energia cinética — gota grande de 5 mm de diâmetro | ≈ 1,28 J |
| Razão de massa e de energia, gota de 5 mm / gota de 2 mm | (5/2)³ = 15,625 |

## Duas viradas narrativas obrigatórias

1. “Por que a chuva real para de acelerar?” → o arrasto cresce com a velocidade → velocidade terminal → remover o arrasto → 713 km/h no modelo para Δh = 2 km.
2. V5, na tela: “Então tamanho não importa?” → gotas diferentes chegam com a mesma velocidade no modelo → tamanho entra pela massa → massa cresce como d³ → energia também cresce como d³. A provocação original “Então virou uma bala?” permanece apenas uma possibilidade narrativa, sem conclusão de dano; não conduz a tela da V5.

Essas viradas orientam a direção audiovisual V5, conforme o handoff de Produção. O conceito e o modelo V1.1 permanecem congelados.

## Restrição editorial: energia cinética ≠ dano

Energia cinética não deve ser tratada como sinônimo de dano. Formulação preferida: “mesma velocidade não significa a mesma energia carregada pela gota”. Qualquer afirmação sobre dano exigiria outro modelo.

“Chuva de balas” pode aparecer futuramente apenas como provocação narrativa, nunca como conclusão física. A pergunta da segunda virada não autoriza concluir que a gota se transforma em uma bala.

## Payoff principal

A atmosfera impede que quilômetros de queda continuem sendo convertidos em velocidade.

## Limite desta etapa

Conceito e modelo fechados. A rodada atual abre direção audiovisual V5, roteiro de referência condensado e preview vertical silencioso de 540×960 / 15 fps, com duração planejada de 104 s. A narração final ainda não está aprovada. Voz, SRT, capa, montagem final, publicação e QA final da unidade não estão abertos.

O velocímetro da chuva real é qualitativo. A V5 acrescenta a faixa contextual aprovada de ~2–9 m/s para gotas de ~0,5–5 mm (UCAR / MetEd), sem afirmar uma velocidade terminal única. A queda real e a comparação final são esquemas; o resultado de 713 km/h pertence exclusivamente ao modelo sem arrasto, para Δh = 2 km e partida praticamente do repouso.

## Histórico — entrega visual V1 e verificações

- Preview: `renders/vid_0019_preview/videos/cena/960p15/chuva_sem_arrasto_v1.mp4`.
- Formato conferido no arquivo: 540×960, 15 fps nominais, H.264, 1.875 quadros, duração aproximada de 125 s (124,998 s), sem faixa de áudio.
- `py_compile` da cena concluído e um preview completo renderizado. O ambiente validado foi preservado; usou-se `uv run --no-sync python -m manim` após restrição de acesso ao cache do uv no sandbox.
- Conferência numérica: v = 198,090888 m/s = 713,127198 km/h; massas = 4,188790 mg e 65,449847 mg; energias = 0,082184064 J e 1,284125997 J; razão = 15,625.
- Frames extraídos para QA em `renders/vid_0019_preview/qa/`: 19, 25, 32, 48, 53, 62, 73, 88, 94, 96, 100, 109, 116 e 124 s. Inspeção visual cobriu vetores, equilíbrio, retirada do arrasto, cancelamento da massa, resultado, comparação de gotas, relações cúbicas, barras e fechamento.
- Nos estados inspecionados, sem inconsistência física identificada ou sobreposição que prejudique a leitura; faixa inferior preservada. Barras partem do mesmo zero e usam a razão 15,625, com valores em joules arredondados.
- No fechamento da V1, ficou pendente a revisão da Produção sobre composição, roteiro e ritmo. O feedback sobre aparência de slides, separação entre fenômeno e matemática e falta de continuidade motivou o redesenho V2 abaixo. A fala não foi gravada nem sincronizada.
- Nenhuma decisão adicional sobre o modelo físico foi necessária. Voz, SRT, capa, montagem final, publicação, commit e push não foram executados.

## Histórico — arquitetura visual V2

- Episódio em tela: `ABSURDO CALCULÁVEL · EP. 02`, conforme correção explícita do usuário.
- Referência única de cabeçalho: `videos/vid_0012_campo_esfera_nao_uniforme/cena.py`, unidade com vídeo final aprovado. Mesmo sistema de tag/série, fonte Space Grotesk, tamanho 20, opacidade 0,65, canto superior esquerdo com margem 0,4; watermark oficial com largura 1,8, opacidade 0,35, canto superior direito com margem 0,28. Template e assets preservados.
- Abertura refeita: gota e velocímetro já presentes no primeiro frame; a pergunta entra depois do movimento inicial.
- Arrasto, velocidade e marcas de queda ligados a um único estado qualitativo, com o peso constante no enquadramento inicial. A intervenção retira só o arrasto, sem trocar a gota ou o dial.
- Queda de 2 km refeita: a mesma gota se reposiciona junto à régua, parte do repouso e permanece visível durante toda a conta. Um parâmetro comum controla distância percorrida, distância restante e velocidade; posição varia com o quadrado desse parâmetro e velocidade varia linearmente. O tempo da animação é esquemático.
- Cancelamento da massa exposto com destaque e riscos, seguido por TransformMatchingTex. Chegada da gota sincronizada com o resultado de 198 m/s; conversão para 713 km/h no mesmo sistema visual.
- Comparação refeita: a segunda gota nasce da primeira. Ambas usam o mesmo estado de queda e chegam juntas; a pergunta visual passa a ser “Então tamanho não importa?”.
- Massa/energia refeitas: gotas e dials permanecem junto às fórmulas, massas e barras. Barras com zero comum e razão 15,625; ressalva energia ≠ dano inserida como nota secundária, sem tela própria.
- Conclusão refeita: a gota original retorna ao enquadramento inicial, o arrasto reaparece pequeno e cresce, e o ponteiro estabiliza. Duas frases curtas substituem o parágrafo final.
- Roteiro de referência V2: dez blocos, 257 palavras, 115 s planejados. Texto ainda não aprovado como narração final.
- A inspeção da primeira passagem V2 identificou tamanhos diferentes nos textos dos dials e nota qualitativa grande no retorno; a escala proporcional dos componentes foi corrigida antes da entrega.

## Histórico — entrega V2 e verificações

- Preview: `renders/vid_0019_preview_v2/videos/cena/960p15/chuva_sem_arrasto_v2.mp4`.
- Arquivo conferido: 540×960, 15 fps nominais, 1.725 quadros, 114,996 s, sem faixa de áudio. Apenas a variante V2 foi renderizada nesta rodada; V1 preservada.
- Sintaxe verificada com `py_compile`. Valores numéricos reconferidos: 198,090888 m/s = 713,127198 km/h; 2 mm → 0,082184064 J; 5 mm → 1,284125997 J; razão 15,625.
- Vinte frames extraídos do MP4 corrigido em `renders/vid_0019_preview_v2/qa/`. Inspeção dos momentos críticos cobriu abertura, equilíbrio das forças, hipótese da gota intacta, cancelamento de massa durante a queda de 2 km, resultado, chegada conjunta, relações cúbicas, barras, ressalva e retorno do arrasto.
- Nos estados inspecionados, nenhuma inconsistência física ou sobreposição prejudicial à leitura identificada. Escalas tipográficas dos velocímetros e nota qualitativa do retorno conferidas após a correção. Cabeçalho confirmado como EP. 02.
- Pendente para a Produção: avaliar continuidade visual, leitura simultânea da conta e da queda, ritmo de 115 s e falas de referência. A narração final e as próximas etapas não foram aprovadas por esta entrega.
- Alterações restritas a `ficha.md`, `roteiro.md` e `cena.py` desta unidade, além dos arquivos gerados de preview/inspeção. Unidade vid_0020 e arquivos compartilhados preservados. Sem voz, SRT, capa, master final, commit ou push.

## Histórico — Direção audiovisual V3

- Feedback da Produção: V2 organizada, mas linguagem visual ainda não aprovada; faltava chuva reconhecível e sensação de aceleração. V3 redesenha direção e composição, preservando integralmente o modelo aprovado.
- EP. 02 confirmado pelo usuário e pela própria unidade. Cabeçalho conferido novamente contra `videos/vid_0012_campo_esfera_nao_uniforme/cena.py`; posições, tipografia e watermark preservados.
- Chuva contextual persistente: faixa de nuvem estilizada, gotas secundárias, profundidade, rastros e protagonista ciano aproximadamente esférica com brilho discreto. Sem geração de imagens ou assets externos.
- Cold open de 0–6 s: pergunta central, ARRASTO ON → OFF, desaparecimento da força e teaser “mais de 700 km/h?”, explicitamente associado à prévia de 2 km sem arrasto.
- Chuva real: estado qualitativo com velocidade proporcional a tanh(τ), arrasto proporcional ao quadrado desse estado e deslocamento visual proporcional a log(cosh(τ)); ponteiro perde ganho e se estabiliza. Sem velocidade terminal numérica real.
- Queda de 2 km reconstruída: α controla deslocamento 2000α², número de velocidade sqrt(2g·2000)α e contador de metros. Número quantitativo grande substitui dial. Massas somem juntas durante a queda. Chegada com 198 m/s, conversão ×3,6 e payoff 713 km/h.
- Duplicação da protagonista em gotas de diâmetros na razão 2,5. Queda curta representa a mesma Δh, com chegada conjunta. Linhas de diâmetro atravessam as gotas durante m ∝ d³ e E ∝ d³; fórmula completa da massa permanece como origem documentada, sem sobrecarregar a tela.
- Barras verticais nascem diretamente sob as respectivas gotas, alinhadas no mesmo zero e com altura na razão 15,625. Pequena primeiro, grande depois; razão só após a descoberta visual. Ressalva sobre dano dura aproximadamente 3 s junto às barras.
- Fechamento retorna literalmente à chuva, com força nomeada “arrasto” e payoff “Ele impede quilômetros de queda de continuarem virando velocidade.” CTA PARALLAX LAB / @labparallax sobre chuva em movimento, usando apenas o asset oficial existente.
- Roteiro de referência V3 atualizado. CTA falado é referência futura e não foi sincronizado; sua tomada deve ser avaliada em etapa própria. Nenhuma narração final aprovada nesta rodada.

## Histórico — Entrega V3 e verificações

- Preview: `renders/vid_0019_preview_v3/videos/cena/960p15/chuva_sem_arrasto_v3.mp4`.
- Metadados conferidos: H.264, 540×960, 15 fps nominais, 1.696 quadros, 113,065 s, zero faixas de áudio.
- `py_compile` e import localizado passaram. Timeline verificada até 113 s, com 74 animações, antes da geração do vídeo. A primeira checagem sem saída de vídeo foi interrompida por calcular quadros intermediários; a chamada foi corrigida para pular explicitamente essas animações.
- Um preview V3 completo foi renderizado. O QA encontrou pequeno desalinhamento das unidades km/h entre as duas colunas; a geometria proporcional foi corrigida, renderizando apenas as animações 37–67 afetadas e recompondo o mesmo preview pelo mecanismo de concatenação do Manim. V1 e V2 preservadas.
- Vinte e quatro frames críticos extraídos do MP4 final em `renders/vid_0019_preview_v3/qa/`, com pranchas `01_chuva.png`, `02_queda.png`, `03_gotas.png` e `04_energia_cta.png`. Metadados registrados em `verificacao_preview.json`.
- Inspecionados: chuva desde o primeiro quadro, teaser após ON → OFF, crescimento suave do arrasto, estabilização qualitativa, retirada seletiva, hipótese da gota intacta, queda acelerada com contador, cancelamento simultâneo da massa, chegada em 2000 m com 198 m/s, conversão para 713 km/h, duas gotas chegando juntas, linhas de diâmetro, m ∝ d³, E ∝ d³, barras associadas às próprias gotas, razão após crescimento, ressalva junto às barras, conclusão com arrasto nomeado e CTA sobre chuva em movimento.
- Conferência física: Δh = 2000 m, g = 9,81 m/s², v = 198,090888 m/s = 713,127198 km/h. 2 mm → 4,188790 mg e 0,082184064 J; 5 mm → 65,449847 mg e 1,284125997 J; razão 15,625. Nenhuma mudança no conceito/modelo V1.1.
- Nos frames inspecionados, nenhuma inconsistência física ou sobreposição crítica restante identificada. Confirmado o alinhamento das unidades após a correção localizada.
- Decisões pendentes da Produção: aprovação da linguagem de chuva/queda, da leitura simultânea da conta e do ritmo de 113 s. CTA visual tem aproximadamente 3 s de sustentação; a frase falada é referência futura e ainda exige adequação temporal na etapa de voz. Esta entrega não aprova a narração final.
- Arquivos-fonte alterados nesta rodada: apenas `ficha.md`, `roteiro.md` e `cena.py` da unidade vid_0019. Unidade vid_0020 e arquivos compartilhados preservados. Sem voz, SRT, capa, master final, publicação, commit ou push.

## Histórico — Direção e ritmo V4

- V3 ainda não aprovada visualmente pela Produção. V4 trabalha hook, ritmo e sincronismo, preservando o conceito/modelo V1.1 e EP. 02. Cabeçalho V3 e asset oficial preservados.
- Chuva desde o primeiro quadro, contador 100→700+ km/h e ON→OFF com nota explícita de prévia sem arrasto em 2 km. Chuva real permanece qualitativa, sem velocidade terminal numérica.
- Queda de 15,6 s: α único controla deslocamento quadrático, 2000α² m, velocidade proporcional a α e âncoras da conta. Cancelamento em 20–30%; ≈198 m/s em 84,6%; ≈713 km/h liberado somente na chegada. HUD em km/h do início ao fim; hold final de aproximadamente 1,4 s.
- Microqueda conjunta de 2,4 s; diâmetros em razão 2,5, massas e energia ∝ d³. Barras associadas às gotas na mesma escala, razão 15,625. Pausas encurtadas; duração visual planejada 94 s.
- Nova comparação de escala energética expressamente aprovada pela Produção na V4: 1,28 J ≈ energia convertida na queda de 100 g por ≈1,3 m; h = 1,28/(0,100×9,81) = 1,304791… m. Bloco geométrico neutro, sem chão/choque. Comparação apenas de energia, sem equivalência de impacto, dano ou força.
- Ressalva junto à comparação por cerca de 2,4 s: “mesma energia ≠ mesmo efeito no impacto”; nota “colisão exigiria outro modelo”. Substitui a seção isolada sobre dano.
- Conclusão retorna à chuva real com força nomeada arrasto. CTA PARALLAX LAB / @labparallax sobre chuva contínua, branding maior usando o asset existente.
- Roteiro V4 atualizado com a fala de referência fornecida pela Produção. Não é locução final e ainda não foi gravada/sincronizada.

## Histórico — Entrega V4 e verificações

- Preview entregue: `renders/vid_0019_preview_v4/videos/cena/960p15/chuva_sem_arrasto_v4.mp4`. H.264, 540×960, 15 fps nominais, 1.411 quadros, 94,065690 s, zero faixas de áudio. Aproximadamente 19 s a menos que a V3.
- Sintaxe e import localizado passaram. Checagem da timeline: 94 s, 94 animações; queda principal de 15,6 s, microqueda de 2,4 s. Assertivas confirmaram α = 1, 2000 m, velocidade final 713,127198 km/h e posição final da gota.
- No MP4, quadro 624: 1983 m e 710 km/h, conversão ainda sem resultado. Quadro 625, aproximadamente 41,667 s: gota no fim, 2000 m, HUD ≈713 km/h e equação ≈713 km/h simultaneamente. Quadro seguinte e hold conferidos; gota permanece no fim até 43 s, cerca de 1,33 s de sustentação.
- Conferência matemática: sqrt(2×9,81×2000) = 198,090888 m/s = 713,127198 km/h. 2 mm → 4,188790 mg e 0,082184064 J. 5 mm → 65,449847 mg e 1,284125997 J. Razão = 15,625. Comparação usando 1,28 J arredondado: h = 1,304791 m para 100 g.
- 36 estados críticos extraídos do arquivo entregue e seis pranchas em `renders/vid_0019_preview_v4/qa/`. Registro com metadados, contas, sincronismo e hash da fonte em `verificacao_preview.json`.
- Inspeção cobriu abertura/contador, crescimento do arrasto e terminal, OFF/hipótese da integridade, início/cancelamento/metade/chegada da queda, duas gotas, diâmetros e massas, relações cúbicas, barras na mesma escala, bloco de 100 g, ressalva, conclusão e CTA.
- O QA encontrou deformação transitória das letras nas trocas de título. Corrigida com saída e entrada sequenciais localizadas, preservando duração e continuidade do restante da composição. Apenas a V4 foi regenerada; quadros e pranchas atualizados. Troca de título, chegada e fechamento reconferidos após a correção. V1, V2 e V3 preservadas.
- Nenhuma inconsistência física ou sobreposição crítica restante identificada nos estados inspecionados. Permanecem decisões da Produção: aprovação visual da V4, força do hook, leitura simultânea e ritmo de 94 s. A futura locução, especialmente o CTA de 4 s, ainda exige avaliação de encaixe em etapa própria; a fala permanece referência.
- Arquivos-fonte alterados: apenas `ficha.md`, `roteiro.md` e `cena.py` da unidade vid_0019. Unidade vid_0020 e arquivos compartilhados preservados. Sem voz, SRT, capa, master, publicação, commit ou push. Parada no preview visual.

## Ajustes factuais e fontes — V5

- 2 mm passa a ser a referência típica principal (UCAR), sem alegação de média universal. A gota de 5 mm é explicitamente grande e participa somente da comparação de tamanho, massa e energia. Conceito físico V1.1 preservado.
- A comparação energética arbitrária da V4 foi retirada da implementação e do roteiro V5; registros acima descrevem exclusivamente versões anteriores.
- Terceira virada: “198 m/s parece só um número. Até você comparar com o mundo real.” Um marcador persistente de 198 m/s (713 km/h, nosso modelo) ancora faixas proporcionais numa escala linear 0–400 m/s. Compara ordem de grandeza das velocidades, sem equivalência direta entre cenários, gotas, materiais ou condições.
- Pás eólicas: 70–150 m/s, gotas 0,5–5 mm. Pás de motores aeronáuticos: 200–400 m/s, gotas 1–5 mm. Fonte: revisão Materials, 2020, tabela 1.
- Ti–6Al–4V: testes 150–350 m/s; intervalo observado 150 ≤ V_threshold < 200 m/s. Resultado restrito ao material e condições daquele estudo, com exposição repetida e gotas diferentes da nossa referência; sem limiar universal ou previsão de dano por gota única.
- NASA: documento de 1982 relata erosão por chuva em aeronaves capazes de >~178 m/s e cita testes de materiais a ~220 m/s. Não atribuímos à NASA um teste da nossa gota ou prova de dano isolado.
- Ressalva ainda sobre a engenharia: “impactos repetidos ≠ uma única gota”; “o dano depende do material e das condições”. Energia cinética continua não sendo sinônimo de dano.
- Referências completas e limites de leitura registrados também em roteiro.md. Callouts curtos na tela, sem bibliografia longa ou URLs sobre o vídeo.

### Referências V5

1. UCAR Center for Science Education. *Sizes of Aerosols, Raindrop and Cloud Droplets*. Randy Russell, 2007. https://scied.ucar.edu/image/aerosols-raindrop-cloud-droplets-sizes — referência típica ~2 mm.
2. UCAR / COMET MetEd. *Instrumentation and Measurement of Surface Precipitation*. https://www.meted.ucar.edu/instrumentation/precipitation/print.php — faixa ~0,5–5 mm e ~2–9 m/s fornecida no handoff aprovado. Página localizada, mas leitura integral indisponível na verificação desta rodada; não alegamos reconferência independente dessa faixa.
3. Turner, R. E.; Hill, C. K. (1982). *Terrestrial environment (climatic) criteria guidelines for use in aerospace vehicle development*. NASA-TM-82473, §4.7 Rain Erosion. https://ntrs.nasa.gov/citations/19820020441 — PDF: https://ntrs.nasa.gov/api/citations/19820020441/downloads/19820020441.pdf
4. Ibrahim, M. E.; Medraj, M. (2020). *Water Droplet Erosion of Wind Turbine Blades: Mechanics, Testing, Modeling and Future Perspectives*. Materials 13(1), 157, tabela 1. DOI: 10.3390/ma13010157. https://www.mdpi.com/1996-1944/13/1/157
5. Gujba, A. K.; Hackel, L.; Kevorkov, D.; Medraj, M. (2016). *Water droplet erosion behaviour of Ti–6Al–4V and mechanisms of material damage at the early and advanced stages*. Wear 358–359, 109–122. DOI: 10.1016/j.wear.2016.04.008. https://users.encs.concordia.ca/~mmedraj/papers/abdullah2.pdf

### Registro factual — entrega e verificação V5

- Preview: `renders/vid_0019_preview_v5/videos/cena/960p15/chuva_sem_arrasto_v5.mp4`. Arquivo H.264, 540×960, 15 fps nominais, 1.561 quadros, 104,066 s, sem faixa de áudio. Apenas V5 renderizada nesta rodada; versões anteriores preservadas.
- Sintaxe/import localizado e execução sem vídeo passaram. O primeiro preflight encontrou uma incompatibilidade na transformação do contador com updater para o grupo de pesquisa; corrigida com entrada simples, antes do render. Preflight corrigido: 104 s, chegada em α = 1, distância 2.000 m, posição final −3,35 e velocidade 713,127198 km/h.
- No MP4: quadro 609 mostra 1.983 m e 710 km/h, conversão sem resultado; quadro 610 (~40,667 s) mostra gota no fim, 2.000 m e ≈713 km/h no HUD e na equação. Quadro 611 e hold conferidos. Microqueda conjunta: 2,4 s.
- Valores reconferidos: v = 198,090888 m/s = 713,127198 km/h; massas 4,188790 mg e 65,449847 mg; energias 0,082184064 J e 1,284125997 J; razão 15,625. Barras usam a razão exata, valores escritos arredondados.
- QA local: 38 quadros e sete pranchas em `renders/vid_0019_preview_v5/qa/`; quatro estados do terceiro ato/fechamento também inspecionados em resolução integral. Cobertura: hook; chuva real e terminal; OFF e integridade; queda/cancelamento/chegada; comparação 2 mm × 5 mm; massas e energia; transição; marcador 198 m/s; faixas eólica/motores/titânio; NASA; ressalva; conclusão; fontes; CTA.
- Nos estados inspecionados, sem sobreposição crítica ou inconsistência física identificada. Fontes legíveis, escalas proporcionais, 198 persistente e ressalva de impactos repetidos visível por aproximadamente 2,7 s junto à engenharia. Nenhuma conclusão sobre dano por gota única ou limiar universal.
- Limitação factual registrada: a faixa UCAR/MetEd foi implementada conforme o briefing aprovado; o conteúdo integral dessa página não ficou acessível para reconferência independente. As demais referências específicas foram consultadas.
- Pendente: revisão editorial/visual da Produção. A fala continua referência sem gravação ou sincronização final; não houve voz, SRT, capa, master, publicação, commit ou push. Arquivos compartilhados e unidade vid_0020 preservados.

### Ajuste visual solicitado após V5

- Nuvens retiradas; linha horizontal preservada e rastros da chuva limitados abaixo dela.
- CTA: removido o texto adicional PARALLAX LAB. Mantido o logo oficial que já contém o nome; @labparallax abaixo, em degradê ciano–violeta–rosa.
- Preview atualizado: `renders/vid_0019_preview_v5_ajuste/videos/cena/960p15/chuva_sem_arrasto_v5_ajuste.mp4`; 104,066 s, 540×960, 15 fps nominais, 1.561 quadros, sem áudio. Preview V5 anterior preservado.
- Sintaxe e render concluídos; inspeção localizada de abertura, pesquisa e CTA em `renders/vid_0019_preview_v5_ajuste/qa/`. Sem sobreposição prejudicial identificada nesses estados. Roteiro ajustado apenas na descrição visual do CTA.


## Narração fornecida e sincronização — 2026-10-10

- Usuário autorizou sincronizar o áudio recebido após refinamento com a Produção e incorporar legendas. Texto integral registrado em `texto_narracao.txt`.
- Origem: `C:/Users/KaioOrtiz/Downloads/ElevenLabs_Untitled_project (20).wav`; cópia integral em `audio/narracao_final.wav`. Duração de 129,600 s, PCM16 estéreo, 44.100 Hz. Sem aceleração, alongamento ou nova geração de voz.
- `gerar_sync.py`, `sync.json` e `legenda.srt`: pausas medidas e interpolação silábica, sem ASR/alinhamento fonético. Âncoras de frases estimadas; tempos de palavras são estimativas, não reconhecimento acústico.
- A extensão concentra-se na engenharia: velocidade relativa água/superfície, aeronave cruzando chuva real, modelo com gota caindo sem arrasto, comparação da ordem de velocidade e ressalva de exposição repetida/material/condições. Não estabelece equivalência de dano entre os cenários.
- O movimento da queda, a distância e o velocímetro continuam ligados ao mesmo progresso; 713 km/h e chegada aos 2.000 m são liberados juntos. Valores 0,082 J, 1,28 J e razão 15,625 preservados.
- Nuvens ausentes; chuva nasce da linha reta. CTA preserva apenas o logo oficial com nome incorporado e @labparallax abaixo em degradê.
- Entregas: `renders/vid_0019_narrado/chuva_sem_arrasto_narrado.mp4` e `renders/vid_0019_narrado/chuva_sem_arrasto_legendado.mp4`. Ambas H.264/AAC, 540×960, 15 fps, 1.944 quadros, vídeo e áudio com 129,600 s. Sem publicação, commit ou push.

- Montagem reproduzível por `montar.py`, reutilizando os montadores do projeto. O render bruto fechou em 129,667 s por arredondamento de quadros; apenas o último quadro excedente do CTA foi retirado na montagem. Voz integral, sem cortes ou mudança de velocidade.
- Verificações: sintaxe dos três scripts; um render da nova variante; montagem das duas entregas; legendas sem sobreposição temporal, até duas linhas e largura máxima real de 435,19 px (limite 440 px); cópia WAV idêntica por SHA-256.
- Áudio AAC comparado ao WAV em cinco intervalos (1, 35, 80, 110 e 127 s): correlação de 0,9990 a 0,9999, sem deslocamento temporal nesses pontos. Isso verifica preservação/montagem, não é escuta humana nem validação fonética das estimativas de palavras.
- QA visual: 42 quadros críticos do arquivo legendado, inspecionados em sete pranchas; cobrindo chuva/terminal/hipótese, cancelamento, chegada conjunta em 37,467 s, gotas, energia, comparação relativa, aplicações, titânio, NASA, ressalvas, retorno e CTA. Fontes, valores e condições permanecem legíveis acima das legendas. Registros em `renders/vid_0019_narrado/qa/verificacao.json`.
- Sem inconsistência objetiva encontrada no modelo/conceito aprovado. Alinhamento por pausas e estimativa silábica, conforme registrado; versão entregue para revisão da Produção, sem aprovação de publicação inferida.


## Finalização autorizada pelo usuário — 2026-10-10

- Usuário aprovou a versão narrada e pediu final em qualidade máxima do projeto, retirada dos textos redundantes no topo a partir da engenharia e revisão de pausas/travadas nas animações. Não solicitou publicação externa, commit ou push.
- Final nativo: 1080×1920 / 30 fps, conforme `docs/formatos.md`. Render e montagem H.264 em CRF 16; sem ampliar o preview de 540×960. Áudio aprovado e SRT preservados.
- Treze frases de topo removidas de 53,17 s em diante por repetirem a fala/legenda, incluindo o fechamento. Mantida a síntese complementar “Energia cinética ≠ dano” na ressalva. Cabeçalho da série, fontes, valores e identificações dos diagramas preservados.
- Álgebra: trocas limitadas a 0,38 s, terminando nas mesmas âncoras; o progresso da queda/velocidade/distância continua durante os intervalos de leitura.
- Engenharia: fluxo de três gotas em vez de duas travessias seguidas de espera; rotores giram durante a exposição; aeronave cruza continuamente e só reentra fora do quadro; comparação dos dois cenários com movimento contínuo. O rastro da gota principal é retirado durante a engenharia para não permanecer junto ao HUD.
- Pré-validação sem vídeo em 1080×1920 / 30 fps passou: 129,600 s, α = 1 na chegada, 2.000 m, 713,127198 km/h e posição final −3,35. Render Full HD concluído; montagem retira apenas o quadro excedente final do render bruto, preservando a voz integral.
- Entregas finais: `renders/vid_0019_chuva_sem_arrasto_final_legendado.mp4` e `renders/vid_0019_chuva_sem_arrasto_final_master_limpo.mp4`. Ambas nativas 1080×1920 / 30 fps, H.264/AAC, 3.888 quadros e 129,600 s de áudio e vídeo. Preview aprovado preservado.
- QA final: sintaxe dos scripts, pré-validação, render da variante final e montagem das duas entregas; decodificação dos 3.888 quadros com tempos crescentes; inspeção visual de 42 quadros críticos em sete pranchas. Sem quadro consecutivo integralmente idêntico. Aeronave: 267 pares visíveis conferidos, maior intervalo sem deslocamento perceptível de um quadro (0,033 s), sem pausa sustentada. Fluxo relativo: 124/124 quadros distintos; rotores: 58/58 e 37/37 quadros distintos nas janelas verificadas.
- Topo conferido em 16 pontos entre 54,8 e 128,9 s: apenas “Energia cinética ≠ dano” permanece como síntese complementar, em 104,8 e 109,8 s. Fontes, valores e identificações dos diagramas permanecem legíveis acima das legendas.
- WAV e SRT com os mesmos SHA-256 da versão aprovada; 53 legendas sem sobreposição, até duas linhas e dentro de 880 px em Arial Bold 58 px. Áudio final comparado ao WAV em cinco intervalos: correlação entre 0,9990 e 0,9999, sem deslocamento nesses pontos. Método de sincronização anterior preservado, sem nova inferência de alinhamento fonético.
- Registros: `renders/vid_0019_final/qa/verificacao.json`, pranchas e quadros na mesma pasta. Sem inconsistência objetiva encontrada. Sem publicação externa, commit, push ou alteração de arquivos globais.

## Dez propostas de capa — 2026-10-10

- Solicitadas pelo usuário após a aprovação do vídeo final. Dez PNGs individuais em `capas_v1/capa_01.png` até `capa_10.png`, todos 1080×1920. Nenhuma opção foi eleita como capa definitiva.
- Padrão das capas anteriores: fundo cósmico, símbolo oficial no topo, título em Space Grotesk Bold com segunda linha em degradê, divisor, “ABSURDO CALCULÁVEL · EP. 02”, painel neon e marca no rodapé. Tipografia Space Grotesk Medium/Bold dos arquivos oficiais.
- Composição reaproveitada do gerador do vid_0009 e primitivas de arte do vid_0010, somente por importação; arquivos de referência e assets preservados. O símbolo do topo é aplicado diretamente do PNG oficial transparente para evitar o recorte frágil da base antiga.
- Propostas variam pergunta, antecipação de 713 km/h, comparação com chuva real, distância de 2 km, gotas de 2 e 5 mm, energia, velocidade terminal, retirada do arrasto, aeronave e payoff atmosférico. Valores continuam vinculados ao modelo sem arrasto; nenhuma conclusão de dano ou metáfora de bala.
- Entregas adicionais: `capas_v1/comparativo_10_capas.jpg`, `capas_v1/10_capas_ep02.zip`, `indice.json` e `qa.json`. Gerador local: `gerar_capas.py`.
- Conferências: dez PNGs distintos e íntegros, resolução e modo RGB, fonte oficial, logo comum às dez opções, inspeção visual do comparativo completo, elementos do painel dentro dos limites e ZIP íntegro com os dez PNGs. Vídeo, áudio, legendas e arquivos globais não alterados nesta rodada.
