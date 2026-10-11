# ABSURDO CALCULÁVEL · EP. 02 — versão final narrada

Narração fornecida pelo usuário após refinamento com a Produção: **129,600 s**, estéreo, 44,1 kHz. O WAV está preservado em `audio/narracao_final.wav`; o texto completo está em `texto_narracao.txt`. A voz não foi acelerada, esticada nem regravada. Final vertical nativo 1080×1920 / 30 fps, com cópia narrada limpa e cópia com legendas incorporadas. Preview narrado 540×960 / 15 fps aprovado pelo usuário e preservado.

O roteiro falado fornecido substitui as falas de referência do preview V5 abaixo. O conceito V1.1 permanece congelado. Nuvens removidas, origem reta da chuva, logo oficial e @labparallax em degradê preservados.

Entregas finais verificadas: `renders/vid_0019_chuva_sem_arrasto_final_master_limpo.mp4` e `renders/vid_0019_chuva_sem_arrasto_final_legendado.mp4`. Ambas com áudio e vídeo de 129,600 s, 3.888 quadros; 53 legendas, até duas linhas. Render e montagem H.264 em CRF 16. A montagem retira apenas um quadro excedente do final do render bruto, sem mexer na narração. Reproduzir por `montar.py`; `--preview` monta a versão anterior preservada em `renders/vid_0019_narrado/`.

Finalização solicitada pelo usuário: treze frases redundantes do topo retiradas a partir da engenharia (53,17 s), mantendo fontes, valores, identificações dos diagramas e a síntese complementar “Energia cinética ≠ dano”. Álgebra com transições de até 0,38 s; queda e contadores continuam durante a leitura. Fluxo de gotas, rotores, aeronave e comparação dos cenários mantêm movimento durante a fala. QA completo registrado em `renders/vid_0019_final/qa/verificacao.json`, com 42 quadros críticos inspecionados em sete pranchas e conferência de movimento, áudio e legendas. Final entregue para postagem pelo usuário; sem publicação externa.

## Sincronização desta rodada

| Tempo aproximado | Conteúdo visual sincronizado |
|---|---|
| 0:00–0:07 | Pergunta, antecipação de mais de 700 km/h e parâmetro de 2 km |
| 0:07–0:17 | Peso, arrasto crescente e velocidade terminal |
| 0:17–0:21 | Retirada apenas do arrasto; gota intacta por hipótese |
| 0:21–0:38 | Energia gravitacional, cancelamento da massa, velocidade e resultado; posição, distância e velocidade seguem o mesmo progresso |
| 0:38–0:45 | Comparação das gotas de 2 e 5 mm, mesma velocidade |
| 0:45–0:53 | Massa e energia cúbicas; barras 0,082 J e 1,28 J, razão 15,625 |
| 0:53–1:04 | 198 m/s como ponte; velocidade da água em relação à superfície |
| 1:04–1:10 | Pás de turbinas e motores; faixas e fonte da revisão |
| 1:10–1:19 | Experimento em Ti–6Al–4V e limiar específico; destaque do resultado do modelo |
| 1:19–1:24 | Registro documental da NASA e velocidades citadas |
| 1:24–1:34 | Aeronave atravessando chuva real; água vista da aeronave, sem atribuir 198 m/s à queda real |
| 1:34–1:39 | No modelo sem arrasto, a própria queda fornece a velocidade |
| 1:39–1:43 | Dois cenários diferentes; comparação da ordem de velocidade, não de dano |
| 1:43–2:00 | Impactos repetidos, materiais específicos, condições controladas; energia cinética ≠ dano |
| 2:00–2:08 | Retorno à chuva real e conclusão sobre o freio atmosférico |
| 2:08–2:09,6 | CTA com logo oficial e @labparallax |

`gerar_sync.py` mede pausas do WAV e estima tempos das palavras por sílabas entre elas, seguindo o método local já usado no projeto. Não é ASR nem alinhamento fonético. `sync.json` registra o método, as âncoras e as estimativas. As legendas mantêm o conteúdo falado, com alguns números em algarismos para leitura, até duas linhas e largura conferida na fonte usada. Áudio, SRT e âncoras da versão narrada aprovada pelo usuário permanecem idênticos; a inspeção final confere estados, movimento e montagem.

## Referência histórica — preview silencioso V5

# ABSURDO CALCULÁVEL · EP. 02 — Preview silencioso V5

**Pergunta:** E se o ar parasse de frear a chuva?

Conceito V1.1 congelado. Direção Manim-only. Planejamento: **104 s**, 540×960 / 15 fps. As falas abaixo são referência editorial condensada, ainda sem gravação, aprovação final de voz ou sincronização de fala. Os tempos descrevem a cena silenciosa implementada.

## 0–7 s — Hook

**Fala de referência:** “E se o ar parasse de frear a chuva? Dois quilômetros de queda, mais de setecentos quilômetros por hora. Por que não acontece?”

**Tela/movimento:** chuva desde o primeiro frame; gota, velocidade crescente, intervenção no arrasto. “2 km de queda · prévia sem arrasto” distingue a antecipação do mundo real. Cabeçalho e logo existentes preservados.

## 7–19 s — Chuva real

**Fala:** “A gravidade puxa, mas o arrasto aumenta com a velocidade. Quando equilibra o peso, a gota continua caindo quase sem acelerar: velocidade terminal.”

**Tela/movimento:** mesma gota, peso constante, arrasto crescente e ponteiro estabilizando. F_arrasto ≈ mg; a ≈ 0. Contexto: gotas de 0,5–5 mm → aproximadamente 2–9 m/s; não representa uma velocidade terminal única. Callout UCAR / MetEd.

## 19–25 s — Intervenção

**Fala:** “Agora desligamos só esse freio. A gota já formada parte praticamente do repouso e fica intacta por hipótese.”

**Tela/movimento:** retira apenas o arrasto. Hipótese explícita na tela. Reposicionamento junto à régua para iniciar a queda de Δh = 2 km; essa distância é parâmetro do modelo.

## 25–42 s — Queda e cálculo juntos

**Fala:** “Em dois quilômetros, a energia gravitacional vira energia de movimento. A massa cancela. Com g igual a 9,81, chegamos a 198 metros por segundo: cerca de 713 quilômetros por hora.”

**Tela/movimento:** mgΔh = ½mv² → cancelamento destacado → gΔh = ½v² → v = √(2gΔh) → substituição → 198 m/s → conversão. Um único progresso controla posição quadrática, distância quadrática e velocidade linear. HUD inteiro truncado; 713, equação final e chegada ao fim da régua liberados juntos. Breve ênfase final, sem prolongar a queda.

## 42–55 s — Tamanho entra pela massa

**Fala:** “Vamos usar dois milímetros como referência típica. A gota grande, de cinco milímetros, chega à mesma velocidade. Então tamanho não importa? Importa pela massa, que cresce com o cubo do diâmetro.”

**Tela/movimento:** segunda gota nasce da primeira; diâmetros na razão 2,5. Microqueda conjunta de 2,4 s. Identificações “referência típica”, “gota grande” e UCAR. Diâmetros destacados, hipótese de esferas e mesma densidade, massas ≈4,19 mg e ≈65,4 mg, m ∝ d³.

## 55–68 s — Energia por gota

**Fala:** “Na mesma queda, E é mgΔh. A energia também cresce com o cubo: 0,082 joule contra 1,28. Quinze vírgula seiscentos e vinte e cinco vezes. Mesma velocidade não significa a mesma energia carregada pela gota.”

**Tela/movimento:** E = mgΔh → E ∝ d³, com g e Δh fixos. Barras vinculadas às gotas, mesmo zero e mesma escala; alturas na razão exata 15,625. Valores arredondados em joules. Nenhuma inferência de dano a partir dessas energias.

## 68–72 s — Terceira virada

**Fala:** “198 metros por segundo parece só um número. Até você comparar com o mundo real.”

**Tela/movimento:** o resultado da comparação de gotas dá origem ao marcador persistente ≈198 m/s / 713 km/h, identificado como “nosso modelo”. Escala linear comum de 0 a 400 m/s. A comparação é de ordem de grandeza de velocidade, sem equivalência direta de cenários.

## 72–79 s — Aplicações de engenharia

**Fala:** “Pás eólicas: 70 a 150 metros por segundo. Motores aeronáuticos: 200 a 400.”

**Tela/movimento:** faixas proporcionais entram em sequência ao redor de 198; turbina eólica e rotor desenhados no Manim. Gotas de 0,5–5 mm nas pás eólicas e 1–5 mm nos motores. Callout curto: Ibrahim & Medraj · Materials, 2020 · tab. 1. Nosso 198 está acima da primeira faixa e próximo da borda inferior da segunda; não afirmar que está dentro de ambas.

## 79–85 s — Experimento específico

**Fala:** “Titânio: testes de 150 a 350. Naquelas condições, o limiar observado ficou entre 150 e 200.”

**Tela/movimento:** faixa de testes 150–350 m/s e intervalo 150 ≤ V_limiar < 200 m/s na mesma escala do marcador. Ti–6Al–4V, exposição repetida. Callout Gujba et al. · Wear, 2016. Superfície abstrata e pequenas gotas sucessivas, sem dramatizar destruição. O intervalo é experimental, não um limiar universal nem previsão de dano de uma gota de 2 mm.

## 85–93 s — Documento NASA e rigor

**Fala:** “A NASA também documentava erosão nessa ordem de velocidade. Mas impactos repetidos não são uma gota: o dano depende do material e das condições.”

**Tela/movimento:** perfil simples de aeronave; capacidade superior a ~178 m/s e ponto de testes citados ~220 m/s. NASA TM-82473 · 1982 · §4.7 Rain Erosion. A seta aberta a partir de 178 indica capacidade superior a esse valor, não um intervalo experimental fechado. Não atribuir os testes à NASA nem ao nosso modelo. De 90 a 93 s, ainda com engenharia e 198 visíveis: **“impactos repetidos ≠ uma única gota”**, abaixo **“o dano depende do material e das condições”**.

## 93–100 s — Atmosfera e conclusão

**Fala:** “O ar não está só no caminho. A atmosfera impede quilômetros de queda de virarem centenas de quilômetros por hora. Sem esse freio, a chuva entraria numa faixa que a engenharia leva a sério.”

**Tela/movimento:** retorna à chuva real, referência típica de 2 mm, forças e ponteiro estabilizando. Contraste mundo real: 0,5–5 mm, ~2–9 m/s; modelo sem arrasto: Δh = 2 km, ~198 m/s, 713 km/h. Não atribuir toda a faixa de velocidades reais a uma gota de 2 mm.

## 100–104 s — CTA

**Fala de referência preservada:** “Se você curte enxergar a física por outro ângulo, segue o Parallax Lab, arroba labparallax.”

**Tela/movimento:** chuva discreta saindo da linha reta, logo oficial que já contém Parallax Lab e @labparallax abaixo em degradê ciano–violeta–rosa; sem nome duplicado. Sem áudio nesta rodada.

## Referências e limites de interpretação

1. **UCAR Center for Science Education.** *Sizes of Aerosols, Raindrop and Cloud Droplets*. Ilustração de Randy Russell (2007). [Página original](https://scied.ucar.edu/image/aerosols-raindrop-cloud-droplets-sizes). Referência típica de aproximadamente 2 mm; não média universal.
2. **UCAR / COMET MetEd.** *Instrumentation and Measurement of Surface Precipitation*. [Módulo original](https://www.meted.ucar.edu/instrumentation/precipitation/print.php). Faixa de contexto fornecida pela Produção: gotas líquidas ~0,5–5 mm, velocidades terminais ~2–9 m/s. A leitura integral dessa página não ficou disponível na verificação desta rodada; preservado o dado aprovado do handoff, sem ampliá-lo.
3. **Turner, R. E.; Hill, C. K. (1982).** *Terrestrial environment (climatic) criteria guidelines for use in aerospace vehicle development*. NASA-TM-82473, seção 4.7, “Rain Erosion”. [Registro NTRS](https://ntrs.nasa.gov/citations/19820020441) · [PDF original](https://ntrs.nasa.gov/api/citations/19820020441/downloads/19820020441.pdf). Relata o problema em aeronaves capazes de mais de ~178 m/s e cita testes de materiais a ~220 m/s. Contexto de erosão por exposição; não prova de efeito de uma gota isolada.
4. **Ibrahim, M. E.; Medraj, M. (2020).** *Water Droplet Erosion of Wind Turbine Blades: Mechanics, Testing, Modeling and Future Perspectives*. Materials, 13(1), 157, tabela 1. [Artigo e DOI 10.3390/ma13010157](https://www.mdpi.com/1996-1944/13/1/157). Pás eólicas: 70–150 m/s e 0,5–5 mm; pás de motores aeronáuticos: 200–400 m/s e 1–5 mm. Velocidades de impacto em aplicações distintas, sem equivalência direta com a queda sem arrasto.
5. **Gujba, A. K.; Hackel, L.; Kevorkov, D.; Medraj, M. (2016).** *Water droplet erosion behaviour of Ti–6Al–4V and mechanisms of material damage at the early and advanced stages*. Wear, 358–359, 109–122. [DOI 10.1016/j.wear.2016.04.008](https://doi.org/10.1016/j.wear.2016.04.008) · [PDF hospedado pelo autor](https://users.encs.concordia.ca/~mmedraj/papers/abdullah2.pdf). Testes 150–350 m/s; intervalo observado 150 ≤ V_threshold < 200 m/s para aquele material, aparato e exposição repetida. As condições e dimensões das gotas do estudo diferem do nosso modelo; o marcador 198 compara velocidades, sem transportar o limiar para outras condições.

Energia cinética ≠ dano. A pesquisa contextualiza erosão acumulada; nenhuma imagem ou fala prevê quebra, lesão ou dano por gota única. Fontes curtas aparecem nos próprios estados relevantes, com referências completas aqui e na ficha. Voz, SRT, capa, master e publicação permanecem fora desta etapa.
