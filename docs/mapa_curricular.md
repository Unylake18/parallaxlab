# Mapa curricular editorial — Parallax Lab

**Versão:** v2, aprovada em 2026-10-27. A v1 está preservada, sem mudanças, em `docs/mapa_curricular_old.md`.\
**O que é:** a grade curricular da biblioteca do Parallax Lab. As disciplinas aparecem na ordem de uma graduação em Física, subindo de nível assunto por assunto, e cada uma é dividida em módulos.\
**O que não é:** calendário de publicação. Os vídeos são produzidos e publicados em qualquer ordem, variando de disciplina e de nível à vontade. O mapa só diz onde cada vídeo mora.\
**Referência do Eletromagnetismo:** Griffiths, *Introduction to Electrodynamics*, 4ª edição. É a numeração que as fichas já usam (o `yt_0011` cobre 7.2.1–7.2.2).\
**Marcação:** *(novo)* indica módulo ou tópico que não existia na v1. Serve para comparar com `docs/mapa_curricular_old.md`; pode sair numa revisão futura.

## O que mudou da v1 para a v2

1. **Eletromagnetismo (Griffiths)** virou disciplina própria, seção por seção (EM 1 a EM 12, mais os apêndices). É onde moram os longos de eletromagnetismo feitos até agora.
2. **Física III** continua na grade, como a primeira passagem por eletricidade e magnetismo, no nível Moysés/Sears. Ganhou circuitos de corrente alternada e magnetismo na matéria.
3. **A grade (§0.2)** mostra a ordem por nível e inclui Álgebra Linear, EDO e EDP, que na v1 estavam como "futuras".
4. **Módulos novos** em todas as disciplinas. Todo módulo ganhou pré-requisitos e uma pergunta-âncora sugerida.
5. **Instruções com o fluxo atual:** curtos e séries, ficha, tag do canto, pasta de entrega, playlists, arsenal 3D e a duração real dos longos.
6. **IDs estáveis:** nenhum número da v1 mudou (4.10 continua sendo Colisões; 6.11 continua sendo Indutância). Módulo novo recebe o próximo número livre da disciplina.
7. **Anexos:** retrato da cobertura (A), o mesmo assunto em dois níveis (B), o que mudou da v1 (C) e decisões de adoção (D).

---

# PARTE 0 — COMO USAR O MAPA

## 0.1 Para que serve

A biblioteca é organizada por:

**disciplina → bloco → módulo → vídeo autossuficiente**

- **Disciplina:** uma linha da grade (Física I, Cálculo II, Eletromagnetismo...).
- **Bloco:** um grupo de módulos vizinhos. Dá nome às playlists e às pastas de entrega (Eletrostática, Colisões, Fluidos...).
- **Módulo:** a unidade didática, um assunto que o aluno estuda de uma vez.
- **Vídeo:** funciona sozinho; o módulo diz onde ele entra.

O mapa existe para evitar dois extremos:

1. transformar o canal cedo demais num curso linear rígido;
2. acumular dezenas de vídeos excelentes, porém sem arquitetura curricular.

A ordem do mapa é a da grade. A ordem de produção é livre: um longo de Eletromagnetismo, depois um curto de Cálculo I, depois um exercício de Física II. O vídeo que sai antes dos vizinhos já nasce com endereço e entra na posição certa da playlist depois.

A ordem de publicação pode ser diferente da ordem de estudo: o Parallax Lab pode publicar vídeos em ordem editorial, aproveitando os melhores temas para descoberta e retenção, sem perder coerência acadêmica.

Quem usa o mapa:

- o chat de planejamento, para escolher e endereçar pautas;
- o agente de código, para preencher a ficha, a tag do canto e o nome da pasta de entrega;
- o arsenal 3D: `experimentos/blender/arsenal/cobertura.md` organiza os sólidos pelos IDs deste mapa.

## 0.2 A grade

Ordem de referência de uma graduação em Física. É editorial: não reproduz a ementa de uma universidade específica.

**Livros de referência.** Física I–IV: Moysés Nussenzveig (*Curso de Física Básica*) e Sears & Zemansky (Young & Freedman), pelas aplicações e problemas. Eletromagnetismo: Griffiths (4ª ed.), que também dá os IDs. Em todas as Físicas, o Feynman (*Lições de Física*, vols. I–III) é a base de consulta teórica e discursiva: de onde vêm as ideias, por que a lei tem essa forma, as discussões conceituais. Ele não define nível nem endereço.

| Etapa | Física | Matemática |
|---|---|---|
| 1 | Física I — Mecânica (4.x) | Cálculo I (8.x) |
| 2 | Física II — Oscilações, ondas, fluidos e termodinâmica (5.x) | Cálculo II (9.x) · Álgebra Linear (13.x) |
| 3 | Física III — Eletricidade e magnetismo (6.x) | Cálculo III (10.x) · EDO (14.x) |
| 4 | Física IV — Óptica, relatividade e física moderna (7.x) | Cálculo IV — Cálculo vetorial (11.x) |
| 5–6 | Eletromagnetismo — Griffiths (EM 1 a EM 12) | EDP e métodos de Fourier (15.x) |
| depois | disciplinas avançadas possíveis (§16) | |

Como as disciplinas se apoiam:

- Física I usa derivada e integral desde o começo; pode andar junto com Cálculo I.
- Física II usa EDO de segunda ordem no oscilador (5.1–5.2) e derivadas parciais na equação de onda (5.3).
- Física III usa integrais múltiplas (10.7–10.8) nas distribuições de carga, e integrais de linha e de superfície (11.2–11.7) em Gauss, Ampère e Faraday.
- Eletromagnetismo supõe Física III e Cálculo IV. O capítulo 1 do Griffiths (EM 1) revisa a análise vetorial que o livro usa.
- Muitas grades dividem o Eletromagnetismo em duas disciplinas, com o corte variando. Para playlists, o corte natural deste mapa fica entre EM 6 (campos na matéria) e EM 7 (eletrodinâmica).

## 0.3 Endereço de um vídeo

Antes de entrar em produção, todo vídeo longo deve conseguir responder aos campos abaixo. De agora em diante, todo curto também recebe pelo menos disciplina e módulo.

| Campo | O que é | Exemplo (`yt_0011`) |
|---|---|---|
| disciplina | linha da grade | Eletromagnetismo |
| bloco | grupo de módulos (playlist, pasta) | Eletrodinâmica |
| módulo | ID e nome deste mapa | EM 7.2 Indução eletromagnética |
| referência | livro e seções, quando houver | Griffiths 7.2.1–7.2.2 |
| natureza (só longo) | `teoria_visual`, `derivacao_aplicada` ou `exercicio_resolvido` | `teoria_visual` |
| pergunta central | a pergunta que o vídeo responde | Como um campo magnético cria um campo elétrico? |
| pré-requisitos | IDs de módulos, só os necessários | EM 7.1, EM 5.1, 11.9 |
| payoff | o que o aluno passa a enxergar | (na ficha) |

**Endereço pelo nível do tratamento.** Vários assuntos aparecem em mais de uma disciplina: a lei de Gauss está em 6.3 e em EM 2.2; a relatividade, em 7.6 e em EM 12. O vídeo vai para o módulo do nível em que foi feito:

- nível Moysés/Sears (forma integral em geometrias simétricas, circuitos e fenômenos, sem divergente nem rotacional) → Física III (6.x) ou Física IV (7.x);
- nível Griffiths (forma local com divergente e rotacional, potenciais, condições de contorno, delta de Dirac) → EM.

A ficha cita o outro módulo como ponte quando ajudar. O Anexo B liga os dois lados.

**Um endereço principal, várias playlists.** A divisa entre os níveis não é rígida: o Griffiths também apresenta a forma integral e as aplicações por simetria. Por isso a regra prática é:

- o vídeo tem **um** módulo principal, que decide o ID, a tag do canto e a pasta de entrega. Normalmente é o da sequência em que ele foi produzido (os longos de Gauss `yt_0001`–`yt_0004` são uma sequência do EM 2.2);
- se o conteúdo também cobre o outro nível sem exigir pré-requisito a mais, ele entra **também** na playlist do outro bloco (ex.: `yt_0001`, `yt_0002` e `yt_0004` servem à playlist de Física III · Lei de Gauss; o `yt_0003`, com divergente e rotacional, não);
- um vídeo novo só é feito para o outro nível quando a abordagem muda de verdade (outra pergunta central, outros pré-requisitos). Repetir o mesmo conteúdo com outro rótulo não vale um vídeo novo.

**Onde o endereço aparece:**

- **Ficha:** `disciplina:`, `bloco:`, `modulo:` com o ID e o nome (`EM 7.2 Indução eletromagnética`) e `referencia:` (campos em `docs/formatos.md`). O antigo `macroassunto:` saiu; fichas antigas não são reescritas.
- **Pasta de entrega dos longos:** `entregas/Vídeos Longos/<Área> - <Bloco> - <Assunto>`, como já é feito (`Eletromagnetismo - Eletrodinâmica - Lei de Faraday e campo elétrico induzido`, `Mecânica - Colisões - Colisões em 1D`). Área e bloco saem da tabela no começo de cada disciplina.
- **Tag do canto dos longos:** leva a área deste mapa, como `ELETROMAGNETISMO · INDUÇÃO`. A forma da tag está em `docs/padrao_video_longo.md` §2.
- **Playlists:** uma por bloco, na ordem da grade, sem "Aula 1, Aula 2". Este mapa não afirma regras de plataforma.

## 0.4 Como um módulo amadurece

Não é obrigatório completar um módulo antes de publicar outro.

Como alvo de biblioteca, um módulo importante pode amadurecer com algo próximo de:

1. **vídeo-âncora (`teoria_visual`)** — estabelece o conceito e a representação visual principal;
2. **derivação ou aplicação (`derivacao_aplicada`)** — mostra de onde vem uma relação importante ou como ela se conecta a um fenômeno;
3. **problema forte (`exercicio_resolvido`)** — usa o conceito em uma questão universitária não trivial e extrai algo além da resposta imediata.

Nem todo módulo exige exatamente três vídeos. É uma estrutura de referência, não uma cota. Um módulo também pode receber vários longos: o EM 2.2 tem quatro (`yt_0001` a `yt_0004`), um de cada natureza e mais um de forma local.

**Os curtos também moram nos módulos.** As séries são famílias de forma, não de disciplina:

- **Por Trás da Fórmula:** de onde vem uma fórmula.
- **Da Equação ao Fenômeno:** uma equação explicando um fenômeno real.
- **Exercício Resolvido:** um problema com resultado e algo a mais.
- **Absurdo Calculável:** uma pergunta curiosa ou absurda, respondida com conta de verdade.

Um curto pode ser porta de entrada para o longo do mesmo módulo, mas não precisa ser teaser dele (`docs/formatos.md`).

## 0.5 Como ler um módulo

```
## 4.10 Colisões                     ← ID estável e nome
- tópico                              ← conteúdo do módulo
- tópico (extensão)                   ← além do curso básico; entra se o vídeo pedir
**Pré-requisitos:** 4.9, 4.8.         ← só os necessários
**Âncora sugerida:** “...?”           ← sugestão editorial, não decisão
**Pontes:** EM 12.2.                  ← ligações com outras disciplinas, quando úteis
```

No Eletromagnetismo, o título do módulo traz a seção do Griffiths e cada tópico traz a subseção.

As âncoras sugeridas priorizam o que funciona no canal: um fenômeno curioso e visual em que o próprio objeto físico gera a equação. A pergunta oficial de cada vídeo continua sendo a da ficha.

## 0.6 IDs estáveis

- Um ID nunca muda: 4.10 é Colisões na v1, na v2 e depois. Fichas antigas que citam "mapa 6.11" continuam válidas.
- Módulo novo recebe o próximo número livre da disciplina (ex.: 4.14). A linha **Ordem de estudo** no começo da disciplina diz onde ele entra.
- No Eletromagnetismo, o ID é a seção do Griffiths (4ª ed.): EM 7.2 = Griffiths 7.2. Os apêndices viram EM A, EM B e EM C.
- Para tirar um módulo, marque "(retirado, ver X)" em vez de apagar.
- O `cobertura.md` do arsenal usa estes IDs. Renumerar obrigaria a regerá-lo (`gerar_cobertura.py`); com IDs estáveis, isso não acontece.

---

# PARTE A — FÍSICA

# 4. Física I — Mecânica

Referência: Moysés Nussenzveig, *Curso de Física Básica* vol. 1, e Sears & Zemansky (Young & Freedman), *Física I*. Escolhidos pelas aplicações e pelos problemas, que vão além do Halliday. Consulta teórica e discussão conceitual: Feynman, *Lições de Física*, vol. I. Os longos de colisões já passam desse nível em alguns pontos (referencial do centro de massa, círculo de estados permitidos).

| Área | Bloco | Módulos |
|---|---|---|
| Mecânica | Cinemática | 4.1, 4.2, 4.3 |
| Mecânica | Dinâmica | 4.4, 4.5, 4.6, 4.14 |
| Mecânica | Energia | 4.7, 4.8 |
| Mecânica | Momento e colisões | 4.9, 4.10 |
| Mecânica | Rotação | 4.11, 4.12, 4.15 |
| Mecânica | Gravitação | 4.13 |

**Ordem de estudo:** 4.1 → 4.2 → 4.3 → 4.4 → 4.5 → 4.6 → 4.14 → 4.7 → 4.8 → 4.9 → 4.10 → 4.11 → 4.15 → 4.12 → 4.13.

## 4.1 Cinemática em uma dimensão

- posição, deslocamento e distância;
- velocidade média e instantânea;
- aceleração média e instantânea;
- gráficos `x(t)`, `v(t)` e `a(t)`;
- integração e diferenciação entre as grandezas;
- movimento com aceleração constante;
- queda livre *(novo)*;
- área e inclinação em gráficos;
- problemas por trechos;
- aceleração que depende do tempo, da velocidade ou da posição (extensão) *(novo)*.

**Pré-requisitos:** 8.4 (pode andar junto).\
**Âncoras possíveis:** “O que a derivada realmente mede no movimento?” e “Como posição, velocidade e aceleração aparecem no mesmo gráfico?”.\
**Pontes:** 8.4, 8.9–8.10, 14.1.

## 4.2 Vetores e movimento em duas dimensões

- vetores posição, velocidade e aceleração;
- decomposição em componentes;
- independência dos movimentos em eixos ortogonais;
- trajetória paramétrica;
- eliminação do tempo;
- aceleração tangencial e normal *(novo)*;
- movimento relativo;
- referenciais em movimento simples;
- transformação de Galileu *(novo)*;
- componentes radial e transversal em coordenadas polares (extensão) *(novo)*.

**Pré-requisitos:** 4.1; vetores (10.1) ajudam.\
**Âncora sugerida:** “Por que dá para tratar o movimento em x e em y separadamente?”\
**Pontes:** 9.6, 10.11.

## 4.3 Lançamentos

- lançamento horizontal;
- lançamento oblíquo;
- tempo de voo;
- altura máxima;
- alcance;
- lançamento a partir de alturas diferentes;
- otimização do alcance;
- família de trajetórias para velocidade inicial fixa;
- região alcançável;
- envoltória / parábola de segurança;
- limites e casos particulares;
- lançamento com resistência do ar, qualitativo ou numérico (extensão) *(novo)*.

**Pré-requisitos:** 4.2; 8.8 para a otimização.\
**Âncora sugerida:** “Por que o lançamento ótimo de uma altura não é a 45°?”\
**Possíveis vídeos:** teoria sobre a trajetória parabólica; derivação de alcance/altura; exercício de ângulo ótimo com altura inicial; derivação avançada da fronteira alcançável.

## 4.4 Leis de Newton e diagramas de corpo livre

- massa, força e aceleração;
- primeira, segunda e terceira leis;
- diagrama de corpo livre;
- normal, tração e peso;
- força elástica e lei de Hooke *(novo)*;
- sistemas conectados;
- polias ideais;
- máquina de Atwood *(novo)*;
- referenciais inerciais;
- problemas com vínculos.

**Pré-requisitos:** 4.2.\
**Âncora sugerida:** “Se ação e reação são iguais e opostas, por que alguma coisa se move?”

## 4.5 Atrito e arrasto

- atrito estático;
- atrito cinético;
- limite de escorregamento;
- plano inclinado;
- curvas e contato;
- dissipação;
- diferença entre o regime estático real e usar automaticamente `f=μN`;
- força aplicada em ângulo e o ângulo que minimiza o esforço (`tg θ = μ`) *(novo)*;
- arrasto linear e quadrático; velocidade terminal *(novo)*.

**Pré-requisitos:** 4.4.\
**Âncora sugerida:** “Por que a força de atrito estático quase nunca vale μN?”\
**Pontes:** 14.1 (velocidade terminal como EDO de primeira ordem).

## 4.6 Movimento circular

- velocidade angular;
- aceleração centrípeta;
- origem geométrica de `a_c=v²/R`;
- dinâmica radial;
- curvas horizontais e inclinadas;
- loopings;
- condições de contato;
- movimento circular não uniforme;
- componentes tangencial e centrípeta da aceleração *(novo)*.

**Pré-requisitos:** 4.2, 4.4.\
**Âncora sugerida:** “Por que uma curva inclinada dispensa o atrito numa única velocidade?”

## 4.7 Trabalho e teorema trabalho–energia

- trabalho de força constante;
- trabalho como integral;
- área no gráfico `F×x`;
- trabalho do peso e da força elástica *(novo)*;
- potência;
- potência média e instantânea *(novo)*;
- energia cinética;
- teorema trabalho–energia;
- forças variáveis.

**Pré-requisitos:** 4.4; 8.9.\
**Âncora sugerida:** “De onde vem o ½mv² da energia cinética?”

## 4.8 Energia potencial e conservação de energia

- forças conservativas;
- `F=-dU/dx`;
- obtenção de `U(x)` a partir de `F(x)`;
- escolha do zero de energia;
- energia mecânica;
- `K=E-U`;
- regiões permitidas;
- pontos de retorno;
- equilíbrio;
- estabilidade;
- leitura qualitativa do movimento por `U(x)`;
- barreiras de potencial;
- poços simples e duplos;
- forças não conservativas e energia dissipada *(novo)*.

**Pré-requisitos:** 4.7; 8.4.\
**Âncora recomendada (`teoria_visual`):** **Como a energia potencial permite prever o movimento?**\
**Pontes:** 11.4, 5.1, 7.10.

Plano da âncora (vem da v1, onde era o primeiro piloto do long-form; o `yt_0001` acabou sendo Lei de Gauss e este vídeo continua por fazer):

- ideias centrais: `F=-dU/dx`, `E=K+U`, `K=E-U≥0`, `U(x)≤E`;
- construir visualmente: força e inclinação do potencial; mínimos, máximos e estabilidade; linha de energia; regiões permitidas e proibidas; pontos de retorno; previsão qualitativa do movimento sem resolver `x(t)`;
- diferentes potenciais como exemplos, sem transformar o vídeo no `vid_0013` esticado.

O `vid_0013` pode futuramente funcionar como aplicação/exercício dentro do mesmo módulo.

## 4.9 Momento linear e impulso

- momento linear;
- impulso;
- força média;
- impulso como integral;
- conservação do momento;
- sistemas isolados;
- centro de massa;
- movimento do centro de massa;
- sistemas de massa variável: o foguete e a equação de Tsiolkovsky (extensão) *(novo)*.

**Pré-requisitos:** 4.4; 8.9.\
**Âncora sugerida:** “Por que o centro de massa de uma granada que explode continua na mesma parábola?”\
**Pontes:** EM 1.5 (a força impulsiva idealizada como delta).

## 4.10 Colisões

- colisões elásticas e inelásticas;
- coeficiente de restituição, quando útil;
- colisões em uma dimensão;
- colisões em duas dimensões;
- explosões;
- centro de massa;
- energia cinética antes/depois;
- referencial do centro de massa: numa colisão elástica, as velocidades só mudam de direção *(novo)*;
- colisão elástica com alvo parado e massas iguais: fora o choque frontal, os corpos saem a 90° *(novo)*;
- círculo de estados permitidos e ângulo máximo de deflexão, `sen θmax = m₂/m₁` para `m₁ > m₂` com alvo parado *(novo)*;
- pêndulo balístico *(novo)*.

**Observação editorial:** colisões pertencem melhor a este módulo do que a “movimento em duas dimensões”. O fato de uma colisão ocorrer em 2D não define o conceito central do problema.\
**Pré-requisitos:** 4.9, 4.8.\
**Âncora sugerida:** “Como saber o que acontece depois de uma colisão?” (a pergunta do `yt_0013`).\
**Pontes:** EM 12.2 (colisões relativísticas).

## 4.11 Rotação de corpos rígidos

- cinemática angular;
- torque;
- torque como produto vetorial *(novo)*;
- momento de inércia;
- cálculo de momentos de inércia;
- teorema dos eixos paralelos;
- teorema dos eixos perpendiculares, para lâminas *(novo)*;
- energia cinética de rotação;
- dinâmica rotacional;
- equilíbrio estático (desenvolvido em 4.15);
- momento angular;
- momento angular de uma partícula e de um corpo rígido *(novo)*;
- conservação do momento angular;
- precessão do giroscópio (extensão) *(novo)*.

**Pré-requisitos:** 4.4, 4.7; 8.12 ou 10.7–10.8 para momentos de inércia por integral.\
**Âncora sugerida:** “Por que um giroscópio girando não cai?”\
**Pontes:** 10.10, 13.8 (eixos principais).

## 4.12 Rolamento

- condição de rolamento sem deslizamento;
- translação + rotação;
- energia no rolamento;
- esfera, cilindro e aro;
- rampas;
- loopings com rotação;
- atrito estático no rolamento;
- rolamento com deslizamento: a bola que derrapa até começar a rolar *(novo)*;
- ioiô *(novo)*.

**Pré-requisitos:** 4.11, 4.5.\
**Âncora sugerida:** “Uma bola de boliche sai derrapando: com que velocidade ela termina rolando?” (esfera maciça lançada sem girar: `v = 5v₀/7`).

## 4.13 Gravitação

- lei da gravitação;
- campo gravitacional;
- potencial gravitacional;
- teorema das cascas *(novo)*;
- gravidade dentro de uma esfera maciça *(novo)*;
- energia orbital;
- velocidade de escape;
- órbitas circulares;
- leis de Kepler;
- satélites;
- interpretação energética das órbitas;
- problema de dois corpos e massa reduzida (extensão) *(novo)*;
- marés *(novo)*;
- manobras orbitais, como a transferência de Hohmann (extensão) *(novo)*.

**Pré-requisitos:** 4.6, 4.8, 4.11.\
**Âncora sugerida:** “Por que ligar o motor para a frente deixa o satélite mais lento no fim?” (a órbita sobe e, na órbita mais alta, a velocidade é menor).\
**Pontes:** 11.10 e EM 2.2 (Gauss para a gravidade), 10.8.

## 4.14 Referenciais não inerciais *(novo)*

- referencial acelerado em linha reta e a força fictícia `−m·a_ref`;
- peso aparente no elevador e o pêndulo no carro que acelera;
- referencial em rotação: forças centrífuga e de Coriolis;
- superfície de um líquido em rotação;
- `g` efetivo e a rotação da Terra;
- pêndulo de Foucault e desvio para leste na queda (extensão).

**Pré-requisitos:** 4.4, 4.6.\
**Âncora sugerida:** “Quando uma força é só efeito de quem está olhando?”\
**Nota:** Coriolis já foi pauta de curto e foi cancelada em 2026-10-14 (`docs/decisoes.md`). O tópico fica no mapa; voltar a ele é decisão nova.

## 4.15 Equilíbrio estático e elasticidade *(novo)*

- condições de equilíbrio: força resultante e torque resultante nulos;
- centro de gravidade;
- estabilidade e tombamento;
- estruturas estaticamente indeterminadas (menção);
- tensão e deformação; módulo de Young;
- cisalhamento e compressão volumétrica.

**Pré-requisitos:** 4.4, 4.11.\
**Âncora sugerida:** “Até onde dá para empilhar blocos para fora da mesa?” (o balanço máximo cresce como a série harmônica e não tem limite).\
**Pontes:** 9.9.

# 5. Física II — Oscilações, ondas, fluidos e termodinâmica

Referência: Moysés vol. 2 e Sears (Young & Freedman), *Física II*. Consulta teórica e discussão conceitual: Feynman, *Lições de Física*, vol. I (oscilações, ondas, som, calor e teoria cinética) e vol. II (fluidos, cap. 40–41).

| Área | Bloco | Módulos |
|---|---|---|
| Oscilações e ondas | Oscilações | 5.1, 5.2, 5.13 |
| Oscilações e ondas | Ondas mecânicas | 5.3, 5.4 |
| Oscilações e ondas | Som | 5.5 |
| Fluidos | Hidrostática | 5.6 |
| Fluidos | Hidrodinâmica | 5.7 |
| Termodinâmica | Calor e primeira lei | 5.8, 5.9, 5.10 |
| Termodinâmica | Segunda lei e entropia | 5.11 |
| Termodinâmica | Transporte de calor | 5.12 |

**Ordem de estudo:** 5.1 → 5.2 → 5.13 → 5.3 → 5.4 → 5.5 → 5.6 → 5.7 → 5.8 → 5.9 → 5.10 → 5.11 → 5.12.

## 5.1 Movimento harmônico simples

- sistema massa–mola;
- equação do MHS;
- relação entre `x`, `v` e `a`;
- energia;
- fase;
- interpretação geométrica;
- MHS como projeção do movimento circular uniforme *(novo)*;
- pequenas oscilações;
- pêndulo no regime de pequenos ângulos;
- pêndulo físico e pêndulo de torção *(novo)*;
- pequenas oscilações em torno de um mínimo de `U(x)` *(novo)*.

**Pré-requisitos:** 4.4, 4.8; 14.3 pode andar junto.\
**Âncora sugerida:** “Por que quase tudo que oscila pouco é um oscilador harmônico?”\
**Pontes:** 9.11, 14.4.

## 5.2 Oscilações amortecidas e forçadas

- amortecimento;
- regimes subcrítico, crítico e supercrítico;
- oscilador forçado;
- ressonância;
- amplitude e fase;
- fator de qualidade, quando apropriado;
- largura da ressonância *(novo)*;
- energia e dissipação.

**Pré-requisitos:** 5.1; 14.4–14.5 podem andar junto.\
**Âncora sugerida:** “Por que um oscilador forçado responde muito mais perto de uma frequência só?”\
**Pontes:** 6.11, 6.13 (o RLC obedece à mesma equação).

## 5.3 Ondas mecânicas

- pulsos;
- ondas progressivas;
- velocidade de propagação;
- comprimento de onda, frequência e fase;
- equação de onda;
- ondas em cordas;
- energia transportada;
- reflexão e transmissão numa junção de cordas *(novo)*;
- frentes de onda em 2D e 3D; intensidade caindo com `1/r²` *(novo)*;
- dispersão e velocidade de grupo (extensão) *(novo)*.

**Pré-requisitos:** 5.1; 10.3.\
**Âncora sugerida:** “De onde sai a equação de onda numa corda?”\
**Pontes:** 15.1, EM 9.1.

## 5.4 Superposição, interferência e ondas estacionárias

- princípio de superposição;
- interferência;
- diferença de fase;
- batimentos;
- ondas estacionárias;
- nós e ventres;
- modos normais;
- cordas e tubos.

**Pré-requisitos:** 5.3.\
**Âncora sugerida:** “Por que uma corda de violão só toca certas notas?”\
**Pontes:** 15.5, 7.3.

## 5.5 Som

- pressão e deslocamento;
- intensidade;
- nível sonoro;
- velocidade do som em gases *(novo)*;
- interferência acústica;
- ressonância;
- efeito Doppler;
- onda de choque e cone de Mach *(novo)*;
- cancelamento ativo de ruído como aplicação, com limites do modelo ideal.

**Pré-requisitos:** 5.3, 5.4.\
**Âncora sugerida:** “Por que a sirene muda de tom quando passa por você?”

## 5.6 Fluidos em repouso

- densidade;
- pressão;
- pressão hidrostática;
- pressão atmosférica, barômetro e manômetro *(novo)*;
- princípio de Pascal;
- empuxo;
- princípio de Arquimedes;
- estabilidade de corpos flutuantes, quando útil;
- fluido em recipiente acelerado ou em rotação: superfície livre inclinada ou parabólica *(novo)*;
- tensão superficial e capilaridade (extensão) *(novo)*.

**Pré-requisitos:** 4.4.\
**Âncora sugerida:** “Por que vasos de formatos diferentes têm a mesma pressão no fundo?” (o paradoxo hidrostático).\
**Pontes:** 4.14.

## 5.7 Fluidos em movimento

- vazão;
- continuidade;
- Bernoulli;
- Torricelli;
- escoamentos ideais;
- tubo de Venturi e tubo de Pitot *(novo)*;
- viscosidade como extensão;
- Poiseuille como aplicação/derivação futura;
- escoamento laminar e turbulento; número de Reynolds (extensão) *(novo)*;
- sustentação: o que Bernoulli explica e o que não explica (extensão, com cuidado) *(novo)*.

**Pré-requisitos:** 5.6, 4.7.\
**Âncora sugerida:** “Por que a pressão cai justamente onde o fluido acelera?”\
**Pontes:** 11.10 (continuidade como divergente nulo).

## 5.8 Temperatura, calor e teoria cinética

- temperatura;
- equilíbrio térmico;
- calor;
- capacidade térmica e calor específico;
- mudanças de fase;
- expansão térmica;
- gás ideal;
- interpretação microscópica da pressão e temperatura;
- distribuição de velocidades de Maxwell *(novo)*;
- livre caminho médio *(novo)*;
- graus de liberdade e equipartição da energia *(novo)*.

**Pré-requisitos:** 4.9 (pressão como troca de momento).\
**Âncora sugerida:** “O que a temperatura de um gás mede, molécula por molécula?”

## 5.9 Primeira lei da Termodinâmica

- energia interna;
- calor e trabalho;
- convenções de sinal;
- processos quase-estáticos;
- diagramas `P×V`;
- isocórico;
- isobárico;
- isotérmico;
- adiabático;
- capacidades térmicas;
- expansão livre *(novo)*.

**Pré-requisitos:** 5.8; 8.9.\
**Âncora sugerida:** “Por que o calor depende do caminho e a energia interna não?”

## 5.10 Processos em gases ideais

- equação de estado;
- trabalho em processos;
- `C_P-C_V=R`;
- `γ=C_P/C_V`;
- derivação de `PV^γ=constante`;
- comparação visual isotérmica × adiabática.

**Pré-requisitos:** 5.9.\
**Âncora sugerida:** “Por que a adiabática cai mais rápido que a isotérmica?”

## 5.11 Segunda lei e entropia

- processos reversíveis e irreversíveis;
- máquinas térmicas;
- refrigeradores;
- ciclo de Carnot;
- eficiência;
- ciclos Otto e Diesel *(novo)*;
- entropia;
- entropia como contagem de microestados, `S = k ln W` *(novo)*;
- desigualdade de Clausius em nível adequado;
- direção temporal dos processos macroscópicos;
- terceira lei (menção) *(novo)*.

**Pré-requisitos:** 5.9, 5.10.\
**Âncora sugerida:** “Por que nenhuma máquina térmica passa do rendimento de Carnot?”

## 5.12 Transporte térmico

- condução;
- convecção;
- radiação;
- lei de Fourier para condução;
- Stefan–Boltzmann, quando útil;
- escalas de tempo térmico;
- lei do resfriamento de Newton *(novo)*.

**Pré-requisitos:** 5.8; 14.1.\
**Âncora sugerida:** “Por que o café esfria rápido no começo e devagar no fim?”\
**Pontes:** 15.2.

## 5.13 Oscilações acopladas e modos normais *(novo)*

- dois osciladores acoplados;
- modos normais e frequências normais;
- batimento como troca de energia entre os osciladores;
- cadeia de N massas e o limite contínuo (a corda);
- modos normais como autovetores.

**Pré-requisitos:** 5.1; 13.5 ajuda.\
**Âncora sugerida:** “Como dois pêndulos ligados por uma mola trocam a energia sozinhos?”\
**Pontes:** 13.5, 13.8, 5.4.

# 6. Física III — Eletricidade e Magnetismo

Primeira passagem pelo eletromagnetismo, no nível Moysés/Sears (Moysés vol. 3; Sears, *Física III*; consulta teórica no Feynman, *Lições de Física*, vol. II): leis em forma integral, geometrias simétricas, circuitos e fenômenos. A forma local (divergente, rotacional, potenciais, condições de contorno) fica no Eletromagnetismo (EM). A correspondência módulo a módulo está no Anexo B.

| Área | Bloco | Módulos |
|---|---|---|
| Eletromagnetismo | Eletrostática | 6.1, 6.2, 6.3, 6.4, 6.5 |
| Eletromagnetismo | Circuitos | 6.6, 6.13 |
| Eletromagnetismo | Magnetostática | 6.7, 6.8, 6.9, 6.14 |
| Eletromagnetismo | Eletrodinâmica | 6.10, 6.11, 6.12 |

**Ordem de estudo:** 6.1 → 6.2 → 6.3 → 6.4 → 6.5 → 6.6 → 6.7 → 6.8 → 6.9 → 6.14 → 6.10 → 6.11 → 6.13 → 6.12.

## 6.1 Carga elétrica e lei de Coulomb

- carga;
- conservação e quantização da carga *(novo)*;
- condutores, isolantes e eletrização por indução *(novo)*;
- superposição;
- força elétrica;
- distribuições discretas;
- simetria básica.

**Pré-requisitos:** 4.4; vetores (10.1).\
**Âncora sugerida:** “Por que um pente atritado atrai pedacinhos de papel neutros?”

## 6.2 Campo elétrico

- definição operacional;
- linhas de campo;
- superposição;
- distribuições contínuas;
- integração de elementos de carga;
- anel;
- disco;
- haste;
- eixo de simetria;
- análise de máximos e limites;
- dipolo elétrico e torque num campo uniforme *(novo)*;
- carga em movimento num campo uniforme *(novo)*.

**Pré-requisitos:** 6.1; 8.9.\
**Âncora sugerida:** “Onde o campo de um anel carregado é máximo, e por que no centro ele é zero?”

## 6.3 Lei de Gauss

- fluxo elétrico;
- superfícies gaussianas;
- simetria;
- esfera;
- cilindro;
- plano;
- densidades não uniformes;
- quando Gauss ajuda e quando não ajuda.

**Pré-requisitos:** 6.2; 11.7 ajuda.\
**Âncora sugerida:** “Por que o campo dentro de uma casca carregada é zero?”

## 6.4 Potencial elétrico

- energia potencial elétrica;
- potencial;
- `E=-∇V`;
- diferença de potencial;
- potencial de distribuições;
- superfícies equipotenciais;
- relação campo–potencial;
- o elétron-volt *(novo)*.

**Pré-requisitos:** 6.2, 4.8.\
**Âncora sugerida:** “Por que um passarinho pousa num fio de alta tensão sem levar choque?”

## 6.5 Condutores e capacitores

- equilíbrio eletrostático;
- condutores;
- cavidades;
- blindagem eletrostática e gaiola de Faraday *(novo)*;
- poder das pontas *(novo)*;
- capacitância;
- capacitores em série/paralelo;
- energia armazenada;
- dielétricos;
- densidade de energia.

**Pré-requisitos:** 6.3, 6.4.\
**Âncora sugerida:** “Por que um carro protege quem está dentro de um raio?” (é a lataria, não os pneus).

## 6.6 Corrente, resistência e circuitos DC

- corrente;
- densidade de corrente;
- resistência;
- resistividade;
- lei de Ohm;
- potência;
- fem e resistência interna *(novo)*;
- associações;
- leis de Kirchhoff;
- amperímetro e voltímetro *(novo)*;
- circuitos RC;
- carga e descarga exponencial.

**Pré-requisitos:** 6.4; 14.1 para o RC.\
**Âncora sugerida:** “Se as cargas andam menos de um milímetro por segundo no fio, por que a lâmpada acende na hora?”

## 6.7 Força magnética

- força de Lorentz;
- movimento de partículas em campo magnético;
- raio ciclotrônico;
- hélices;
- seletor de velocidades e espectrômetro de massa *(novo)*;
- efeito Hall *(novo)*;
- força em fios;
- torque em espiras;
- momento de dipolo magnético.

**Pré-requisitos:** 6.2; produto vetorial (10.1).\
**Âncora sugerida:** “Como o efeito Hall descobre o sinal das cargas que formam a corrente?”

## 6.8 Campo magnético e Biot–Savart

- contribuição de elementos de corrente;
- fio retilíneo;
- arco;
- espira;
- eixo de uma espira;
- superposição;
- limites distante/próximo;
- força entre fios paralelos (a antiga definição do ampère) *(novo)*.

**Pré-requisitos:** 6.7; 8.9.\
**Âncora sugerida:** “Por que dois fios com correntes no mesmo sentido se atraem?”

## 6.9 Lei de Ampère

- circulação;
- simetria;
- fio infinito;
- solenoide;
- toroide;
- aproximações de sistemas finitos;
- relação com Biot–Savart.

**Pré-requisitos:** 6.8; 11.3 ajuda.\
**Âncora sugerida:** “Por que o campo dentro de um solenoide longo é uniforme?”

## 6.10 Indução eletromagnética

- fluxo magnético;
- lei de Faraday;
- lei de Lenz;
- fem de movimento;
- espiras móveis;
- geradores;
- correntes induzidas;
- correntes de Foucault e freio magnético *(novo)*;
- transformador, em princípio *(novo)*.

**Pré-requisitos:** 6.7, 6.9.\
**Âncora sugerida:** “Por que um ímã cai devagar dentro de um tubo de cobre?”

## 6.11 Indutância e circuitos com indutores

- autoindutância;
- indutância mútua *(novo)*;
- energia magnética;
- RL;
- LC;
- RLC;
- oscilações eletromagnéticas;
- ressonância elétrica.

**Pré-requisitos:** 6.10, 6.6; 14.4.\
**Âncora sugerida:** “Por que a corrente demora a subir num circuito com bobina?”\
**Pontes:** 5.1–5.2 (o LC e o RLC são osciladores).

## 6.12 Maxwell e ondas eletromagnéticas

- corrente de deslocamento;
- estrutura das equações de Maxwell;
- campos elétrico e magnético acoplados;
- propagação;
- velocidade da luz;
- energia;
- vetor de Poynting em nível adequado.

**Pré-requisitos:** 6.10, 6.11.\
**Âncora sugerida:** “Por que um capacitor carregando cria campo magnético entre as placas, onde não passa corrente?”

## 6.13 Circuitos de corrente alternada *(novo)*

- tensão e corrente senoidais; fasores;
- reatâncias capacitiva e indutiva; impedância;
- circuito RLC série com fonte senoidal; ressonância e largura de banda;
- potência em CA, valor eficaz e fator de potência;
- transformadores;
- filtros simples (extensão).

**Pré-requisitos:** 6.11; 9.11 (fórmula de Euler) ajuda.\
**Âncora sugerida:** “Se a tomada é de 127 V, por que a tensão chega a quase 180 V em cada ciclo?” (o valor eficaz é o pico dividido por √2).\
**Pontes:** 5.2, 14.5.

## 6.14 Magnetismo na matéria (introdutório) *(novo)*

- ímãs e dipolos magnéticos;
- momento magnético de uma espira e do átomo;
- diamagnetismo, paramagnetismo e ferromagnetismo;
- domínios, histerese e temperatura de Curie;
- lei de Gauss do magnetismo: não existe polo isolado.

**Pré-requisitos:** 6.7, 6.9.\
**Âncora sugerida:** “Por que cortar um ímã ao meio dá dois ímãs, e não um polo norte solto?”

# 7. Física IV — Óptica, relatividade e física moderna

Referência: Moysés vol. 4 e Sears (Young & Freedman), *Física IV*. Consulta teórica e discussão conceitual: Feynman, *Lições de Física*, vol. I (óptica, relatividade) e vol. III (mecânica quântica).

**Nota:** a divisão exata de Física IV varia entre cursos. Para o Parallax Lab, este bloco funciona como arquitetura editorial de tópicos posteriores a Física III, não como reprodução de uma ementa institucional específica.

| Área | Bloco | Módulos |
|---|---|---|
| Óptica | Luz e óptica geométrica | 7.1, 7.2 |
| Óptica | Óptica ondulatória | 7.3, 7.4, 7.5 |
| Relatividade | Relatividade especial | 7.6 |
| Física moderna | Origens da física quântica | 7.7, 7.8, 7.9 |
| Física moderna | Quântica introdutória | 7.10, 7.11 |
| Física moderna | Núcleo, partículas e sólidos | 7.12, 7.13 |

**Ordem de estudo:** a dos números, de 7.1 a 7.13.

## 7.1 Ondas eletromagnéticas e luz

- luz como onda eletromagnética;
- intensidade;
- pressão de radiação *(novo)*;
- polarização;
- espectro eletromagnético;
- energia transportada.

**Pré-requisitos:** 6.12, 5.3.\
**Âncora sugerida:** “A luz empurra?” (pressão de radiação e velas solares).\
**Pontes:** EM 9.2.

## 7.2 Óptica geométrica

- reflexão;
- refração;
- lei de Snell;
- reflexão total interna e fibra óptica *(novo)*;
- dispersão e prismas *(novo)*;
- arco-íris: o desvio mínimo *(novo)*;
- princípio de Fermat;
- espelhos;
- lentes;
- formação de imagens;
- instrumentos ópticos;
- aproximação paraxial;
- miragens e índice de refração variável (extensão) *(novo)*.

**Pré-requisitos:** 7.1; 8.8 (Fermat como otimização).\
**Âncora sugerida:** “Por que a luz parece escolher o caminho mais rápido?” (com rigor: o tempo é estacionário, nem sempre mínimo).\
**Pontes:** EM 9.3.

## 7.3 Interferência óptica

- diferença de caminho;
- coerência;
- dupla fenda;
- filmes finos;
- anéis de Newton *(novo)*;
- interferômetros;
- intensidade de interferência.

**Pré-requisitos:** 5.4, 7.1.\
**Âncora sugerida:** “Por que uma bolha de sabão fica colorida?”

## 7.4 Difração

- fenda simples;
- redes de difração;
- limite de resolução;
- critério de Rayleigh *(novo)*;
- abertura circular, quando apropriado;
- difração de Fraunhofer × Fresnel, qualitativo *(novo)*;
- conexão Fourier–difração como extensão futura.

**Pré-requisitos:** 7.3.\
**Âncora sugerida:** “Por que um telescópio maior enxerga detalhes menores?”\
**Pontes:** 15.6.

## 7.5 Polarização

- polarização linear;
- polarizadores;
- lei de Malus;
- polarização por reflexão;
- polarização por espalhamento: a luz do céu *(novo)*;
- estados de polarização em nível introdutório;
- birrefringência e atividade óptica (extensão) *(novo)*.

**Pré-requisitos:** 7.1.\
**Âncora sugerida:** “Por que óculos polarizados apagam o reflexo da água?”\
**Pontes:** EM 9.3 (ângulo de Brewster).

## 7.6 Relatividade especial

- postulados;
- simultaneidade;
- dilatação do tempo;
- contração do comprimento;
- transformações de Lorentz;
- composição relativística de velocidades;
- energia e momento relativísticos;
- `E = mc²` e energia de ligação *(novo)*;
- efeito Doppler relativístico *(novo)*;
- paradoxo dos gêmeos *(novo)*;
- diagramas espaço-tempo.

**Pré-requisitos:** 4.2 (Galileu), 4.9.\
**Âncora sugerida:** “Por que dois observadores discordam sobre o que aconteceu ao mesmo tempo?”\
**Pontes:** EM 12.

## 7.7 Radiação térmica e nascimento da física quântica

- corpo negro;
- lei de Planck;
- Wien;
- Stefan–Boltzmann;
- catástrofe ultravioleta;
- quantização.

**Pré-requisitos:** 5.12, 7.1.\
**Âncora sugerida:** “Por que um metal aquecido fica vermelho antes de ficar branco?”

## 7.8 Fótons

- efeito fotoelétrico;
- energia e momento do fóton;
- espalhamento Compton;
- dualidade onda-partícula.

**Pré-requisitos:** 7.7, 7.6.\
**Âncora sugerida:** “Por que uma luz azul fraca arranca elétrons de certos metais e uma luz vermelha forte não?”

## 7.9 Ondas de matéria

- de Broglie;
- interferência de matéria;
- princípio de incerteza;
- pacotes de onda em nível introdutório.

**Pré-requisitos:** 7.8, 7.3.\
**Âncora sugerida:** “Como elétrons enviados um de cada vez formam uma figura de interferência?”

## 7.10 Introdução à equação de Schrödinger

- função de onda;
- interpretação probabilística;
- estados estacionários;
- poço infinito;
- barreiras;
- tunelamento;
- oscilador harmônico como extensão.

**Pré-requisitos:** 7.9; 14.3; 4.8 (leitura por `U(x)`).\
**Âncora sugerida:** “Como uma partícula atravessa uma barreira para a qual não tem energia?”\
**Pontes:** 4.8, 15.4.

## 7.11 Estrutura atômica

- espectros;
- modelo de Bohr como ponte histórica;
- átomo de hidrogênio;
- níveis de energia;
- números quânticos em nível introdutório;
- spin, princípio de exclusão e a tabela periódica *(novo)*.

**Pré-requisitos:** 7.10.\
**Âncora sugerida:** “Por que cada elemento tem um código de barras de cores?”

## 7.12 Física nuclear e partículas — introdução

- radioatividade;
- decaimento exponencial;
- datação por carbono-14 *(novo)*;
- energia de ligação;
- fissão;
- fusão;
- reações nucleares;
- panorama introdutório de partículas, sem transformar o módulo em catálogo.

**Pré-requisitos:** 7.6; 14.1.\
**Âncora sugerida:** “Como o carbono-14 diz a idade de um fóssil?”

## 7.13 Sólidos e semicondutores — introdução *(novo)*

- bandas de energia;
- condutores, isolantes e semicondutores;
- dopagem e junção p-n;
- diodo, LED e célula solar (qualitativo);
- laser e emissão estimulada.

**Pré-requisitos:** 7.10, 7.11.\
**Âncora sugerida:** “Por que um semicondutor conduz melhor quando esquenta, ao contrário de um metal?”

# Eletromagnetismo — Griffiths (EM) *(novo)*

**Referência:** David J. Griffiths, *Introduction to Electrodynamics*, 4ª edição. Cada módulo é uma seção do livro e o ID repete o número dela (EM 7.2 = Griffiths 7.2); os tópicos seguem as subseções. Se uma ficha usar outra edição, conferir a numeração.\
**Nível:** depois de Física III e Cálculo IV. É o nível em que os longos de eletromagnetismo vêm sendo feitos (`yt_0001` a `yt_0012`).\
**Ordem de estudo:** a do livro.\
**Consulta teórica:** Feynman, *Lições de Física*, vol. II (e vol. I, cap. 28–34, para radiação). Sobretudo nas discussões conceituais: o sentido físico do divergente e do rotacional, de onde vem a corrente de deslocamento, o magnetismo como efeito relativístico.\
**Toda a disciplina é nova na v2**, por isso os módulos abaixo não levam a marca *(novo)*.

| Área | Bloco | Módulos | Griffiths |
|---|---|---|---|
| Eletromagnetismo | Análise vetorial | EM 1.1–EM 1.6, EM A, EM B, EM C | cap. 1 e apêndices |
| Eletromagnetismo | Eletrostática | EM 2.1–EM 2.5, EM 3.1–EM 3.4, EM 4.1–EM 4.4 | caps. 2, 3 e 4 |
| Eletromagnetismo | Magnetostática | EM 5.1–EM 5.4, EM 6.1–EM 6.4 | caps. 5 e 6 |
| Eletromagnetismo | Eletrodinâmica | EM 7.1–EM 7.3, EM 8.1–EM 8.3 | caps. 7 e 8 |
| Eletromagnetismo | Ondas eletromagnéticas | EM 9.1–EM 9.5 | cap. 9 |
| Eletromagnetismo | Potenciais e radiação | EM 10.1–EM 10.3, EM 11.1–EM 11.2 | caps. 10 e 11 |
| Eletromagnetismo | Relatividade | EM 12.1–EM 12.3 | cap. 12 |

Eletrostática, Magnetostática e Eletrodinâmica são os blocos que as pastas de entrega já usam.

## EM 1 — Análise vetorial (Griffiths cap. 1)

Boa parte deste capítulo é Cálculo III e IV (10.x e 11.x). Um vídeo vem para EM 1 quando a ferramenta aparece a serviço do eletromagnetismo; se for matemática pura, o endereço é o módulo de Cálculo.

### EM 1.1 Álgebra vetorial (1.1)

- operações com vetores e forma em componentes (1.1.1–1.1.2);
- produtos triplos (1.1.3);
- vetores posição, deslocamento e separação, `𝓻 = r − r′` (1.1.4);
- como os vetores se transformam numa rotação (1.1.5).

**Pré-requisitos:** 10.1.\
**Âncora sugerida:** “Por que o eletromagnetismo sempre fala de dois pontos: onde está a fonte e onde se mede o campo?”

### EM 1.2 Cálculo diferencial (1.2)

- derivadas ordinárias, gradiente e o operador ∇ (1.2.1–1.2.3);
- divergente (1.2.4);
- rotacional (1.2.5);
- regras de produto (1.2.6);
- derivadas segundas e o laplaciano (1.2.7).

**Pré-requisitos:** 10.3, 10.5.\
**Âncora sugerida:** “O que o divergente e o rotacional medem num campo?”\
**Pontes:** 11.8, 11.12.

### EM 1.3 Cálculo integral (1.3)

- integrais de linha, de superfície e de volume (1.3.1);
- teorema fundamental do cálculo (1.3.2);
- teorema fundamental para gradientes (1.3.3);
- teorema fundamental para divergentes, o de Gauss (1.3.4);
- teorema fundamental para rotacionais, o de Stokes (1.3.5);
- integração por partes em três dimensões (1.3.6).

**Pré-requisitos:** EM 1.2; 11.2–11.10.\
**Âncora sugerida:** “Por que gradiente, Gauss e Stokes são versões do mesmo teorema?”\
**Pontes:** 11.11.

### EM 1.4 Coordenadas curvilíneas (1.4)

- coordenadas esféricas (1.4.1);
- coordenadas cilíndricas (1.4.2);
- vetores unitários que mudam de direção de ponto a ponto;
- elementos de linha, área e volume;
- gradiente, divergente, rotacional e laplaciano nessas coordenadas (o caso geral fica em EM A).

**Pré-requisitos:** 10.8, 10.9.\
**Âncora sugerida:** “De onde vem o r² na fórmula do divergente em coordenadas esféricas?”\
**Pontes:** 11.12.

### EM 1.5 A função delta de Dirac (1.5)

- o divergente de `r̂/r²`: zero em todo ponto fora da origem, mas com fluxo `4π` (1.5.1);
- delta de Dirac em uma dimensão (1.5.2);
- delta de Dirac em três dimensões; a carga pontual como densidade, `ρ = q δ³(r)` (1.5.3).

**Pré-requisitos:** EM 1.3, EM 1.4.\
**Âncora sugerida:** “Como um campo com divergente zero em todo lugar tem fluxo diferente de zero?”\
**Pontes:** 4.9 (força impulsiva).

### EM 1.6 Teoria dos campos vetoriais (1.6)

- teorema de Helmholtz: o divergente e o rotacional determinam o campo, se ele vai a zero no infinito (1.6.1);
- potenciais: rotacional nulo ⇔ o campo é um gradiente; divergente nulo ⇔ o campo é um rotacional (1.6.2).

**Pré-requisitos:** EM 1.2, EM 1.3.\
**Âncora sugerida:** “Por que bastam o divergente e o rotacional para conhecer um campo inteiro?”

### EM A, EM B e EM C — Apêndices

- **EM A:** cálculo vetorial em coordenadas curvilíneas gerais, com fatores de escala.
- **EM B:** a demonstração do teorema de Helmholtz.
- **EM C:** unidades: SI e gaussiano, e por que existem `ε₀` e `μ₀`.

**Âncora sugerida (EM C):** “Por que a lei de Coulomb tem `1/4πε₀` em alguns livros e não tem em outros?”

## EM 2 — Eletrostática (Griffiths cap. 2)

### EM 2.1 O campo elétrico (2.1)

- o problema fundamental da eletrodinâmica: a força de cargas-fonte sobre uma carga de prova (2.1.1);
- lei de Coulomb (2.1.2);
- campo elétrico e superposição (2.1.3);
- distribuições contínuas: densidades λ, σ e ρ e a integral com o vetor separação (2.1.4).

**Pré-requisitos:** EM 1.1; 10.7–10.8. Física III (6.1–6.2) ajuda.\
**Âncora sugerida:** “Como uma integral transforma infinitas cargas num campo só?”

### EM 2.2 Divergente e rotacional do campo eletrostático (2.2)

- linhas de campo, fluxo e lei de Gauss (2.2.1);
- divergente de E: `∇·E = ρ/ε₀` (2.2.2);
- aplicações da lei de Gauss: simetrias esférica, cilíndrica e plana (2.2.3);
- rotacional de E: `∇×E = 0` (2.2.4).

**Pré-requisitos:** EM 1.3, EM 1.5, EM 2.1.\
**Âncora sugerida:** “Quando a lei de Gauss realmente permite calcular o campo, e por que escolher qualquer superfície fechada não basta?” (a pergunta do `yt_0001`).\
**Pontes:** 11.8, 11.10.

### EM 2.3 Potencial elétrico (2.3)

- introdução ao potencial: rotacional nulo, então `E = −∇V` (2.3.1);
- comentários: ponto de referência, superposição, unidades (2.3.2);
- equações de Poisson e de Laplace (2.3.3);
- potencial de uma distribuição localizada (2.3.4);
- condições de contorno: o salto de E numa superfície carregada e a continuidade de V (2.3.5).

**Pré-requisitos:** EM 2.2, EM 1.6.\
**Âncora sugerida:** “Por que um número em cada ponto basta para guardar um campo vetorial inteiro?”

### EM 2.4 Trabalho e energia na eletrostática (2.4)

- o trabalho para mover uma carga (2.4.1);
- energia de uma distribuição de cargas pontuais (2.4.2);
- energia de uma distribuição contínua, `W = (ε₀/2)∫E² dτ` (2.4.3);
- comentários: a energia não obedece à superposição; a autoenergia da carga pontual é infinita (2.4.4).

**Pré-requisitos:** EM 2.3.\
**Âncora sugerida:** “Onde fica guardada a energia de um conjunto de cargas: nas cargas ou no campo?”

### EM 2.5 Condutores (2.5)

- propriedades básicas: campo nulo dentro, carga na superfície, condutor equipotencial (2.5.1);
- cargas induzidas e cavidades (2.5.2);
- carga superficial e força num condutor: a pressão eletrostática `σ²/2ε₀` (2.5.3);
- capacitores (2.5.4).

**Pré-requisitos:** EM 2.3, EM 2.4.\
**Âncora sugerida:** “Por que o campo dentro de um condutor é zero, e o que isso obriga as cargas a fazer?”

## EM 3 — Potenciais: técnicas especiais (Griffiths cap. 3)

### EM 3.1 Equação de Laplace (3.1)

- introdução (3.1.1);
- a equação de Laplace em uma, duas e três dimensões: o valor num ponto é a média em volta, sem máximos nem mínimos locais (3.1.2–3.1.4);
- condições de contorno e teoremas de unicidade (3.1.5);
- condutores e o segundo teorema de unicidade (3.1.6).

**Pré-requisitos:** EM 2.3, EM 2.5; 15.3 ajuda.\
**Âncora sugerida:** “Por que é impossível prender uma carga parada só com campos eletrostáticos?” (teorema de Earnshaw).\
**Pontes:** 11.12, 15.3.

### EM 3.2 Método das imagens (3.2)

- o problema clássico: carga diante de um plano condutor aterrado (3.2.1);
- a carga induzida na superfície (3.2.2);
- força e energia: por que a energia não é a do par carga + imagem (3.2.3);
- outros problemas de imagens, como a esfera aterrada (3.2.4).

**Pré-requisitos:** EM 3.1.\
**Âncora sugerida:** “Como uma carga que não existe resolve um problema real?”

### EM 3.3 Separação de variáveis (3.3)

- coordenadas cartesianas: a fenda infinita e as séries de Fourier (3.3.1);
- coordenadas esféricas: polinômios de Legendre; esfera condutora num campo uniforme (3.3.2).

**Pré-requisitos:** EM 3.1; 15.4–15.5.\
**Âncora sugerida:** “Como uma esfera condutora deforma um campo elétrico uniforme?”\
**Pontes:** 14.8, 15.4, 15.5.

### EM 3.4 Expansão multipolar (3.4)

- potenciais aproximados a grandes distâncias (3.4.1);
- os termos de monopolo e de dipolo (3.4.2);
- a origem das coordenadas na expansão (3.4.3);
- o campo elétrico de um dipolo (3.4.4).

**Pré-requisitos:** EM 2.3; 9.11.\
**Âncora sugerida:** “Por que, de longe, toda distribuição de carga parece uma carga pontual, ou então um dipolo?”\
**Pontes:** 9.11.

## EM 4 — Campos elétricos na matéria (Griffiths cap. 4)

### EM 4.1 Polarização (4.1)

- dielétricos (4.1.1);
- dipolos induzidos e polarizabilidade (4.1.2);
- alinhamento de moléculas polares: o torque `p × E` (4.1.3);
- a polarização P (4.1.4).

**Pré-requisitos:** EM 3.4.\
**Âncora sugerida:** “Por que um isolante neutro é atraído por um objeto carregado?”

### EM 4.2 O campo de um objeto polarizado (4.2)

- cargas ligadas: `σ_b = P·n̂` e `ρ_b = −∇·P` (4.2.1);
- interpretação física das cargas ligadas (4.2.2);
- o campo dentro de um dielétrico: a média macroscópica (4.2.3).

**Pré-requisitos:** EM 4.1.\
**Âncora sugerida:** “De onde vêm as cargas que aparecem na superfície de um isolante polarizado?”

### EM 4.3 O deslocamento elétrico (4.3)

- a lei de Gauss com dielétricos: `∇·D = ρ_livre` (4.3.1);
- um paralelo enganoso: D não se calcula como E, porque `∇×D` em geral não é zero (4.3.2);
- condições de contorno (4.3.3).

**Pré-requisitos:** EM 4.2.\
**Âncora sugerida:** “D parece um E melhorado: onde essa ideia engana?”

### EM 4.4 Dielétricos lineares (4.4)

- suscetibilidade, permissividade e constante dielétrica (4.4.1);
- problemas de contorno com dielétricos lineares, como a esfera dielétrica num campo uniforme (4.4.2);
- energia em sistemas com dielétricos (4.4.3);
- forças em dielétricos (4.4.4).

**Pré-requisitos:** EM 4.3, EM 3.3.\
**Âncora sugerida:** “Por que um bloco dielétrico é puxado para dentro de um capacitor?” (a força vem do campo de borda).

## EM 5 — Magnetostática (Griffiths cap. 5)

### EM 5.1 A força de Lorentz (5.1)

- campos magnéticos (5.1.1);
- forças magnéticas: movimento ciclotrônico e cicloidal; a força magnética não realiza trabalho (5.1.2);
- correntes linear, superficial e volumétrica; equação da continuidade (5.1.3).

**Pré-requisitos:** EM 2.1; 6.7 ajuda.\
**Âncora sugerida:** “Por que uma carga solta em campos elétrico e magnético cruzados anda numa cicloide?”

### EM 5.2 A lei de Biot–Savart (5.2)

- correntes estacionárias (5.2.1);
- o campo magnético de uma corrente estacionária: fio, espira e outras geometrias (5.2.2).

**Pré-requisitos:** EM 5.1.\
**Âncora sugerida:** “Como cada pedacinho de corrente contribui para o campo magnético?”

### EM 5.3 Divergente e rotacional de B (5.3)

- correntes retilíneas (5.3.1);
- `∇·B = 0` e `∇×B = μ₀J` (5.3.2);
- lei de Ampère e suas aplicações: fio, lâmina de corrente, solenoide e toroide (5.3.3);
- comparação entre magnetostática e eletrostática (5.3.4).

**Pré-requisitos:** EM 5.2, EM 1.2.\
**Âncora sugerida:** “Por que as linhas de campo magnético nunca começam nem terminam?”

### EM 5.4 O potencial vetor magnético (5.4)

- o potencial vetor A, com `B = ∇×A` e a escolha `∇·A = 0` (5.4.1);
- condições de contorno: o salto de B numa lâmina de corrente (5.4.2);
- expansão multipolar do potencial vetor; o dipolo magnético `m = I a` (5.4.3).

**Pré-requisitos:** EM 5.3, EM 1.6.\
**Âncora sugerida:** “O que é o potencial vetor, e por que a circulação dele dá o fluxo magnético?”

## EM 6 — Campos magnéticos na matéria (Griffiths cap. 6)

### EM 6.1 Magnetização (6.1)

- diamagnéticos, paramagnéticos e ferromagnéticos (6.1.1);
- torques e forças em dipolos magnéticos: `N = m × B` e `F = ∇(m·B)` (6.1.2);
- efeito de um campo magnético nas órbitas atômicas: a origem do diamagnetismo (6.1.3);
- a magnetização M (6.1.4).

**Pré-requisitos:** EM 5.4.\
**Âncora sugerida:** “Como um campo magnético muito forte faz um sapo levitar?” (diamagnetismo).

### EM 6.2 O campo de um objeto magnetizado (6.2)

- correntes ligadas: `J_b = ∇×M` e `K_b = M × n̂` (6.2.1);
- interpretação física das correntes ligadas (6.2.2);
- o campo magnético dentro da matéria (6.2.3).

**Pré-requisitos:** EM 6.1.\
**Âncora sugerida:** “Por que um ímã de barra tem o mesmo campo de um solenoide?”

### EM 6.3 O campo auxiliar H (6.3)

- a lei de Ampère em materiais magnetizados: `∇×H = J_livre` (6.3.1);
- um paralelo enganoso: `∇·H` em geral não é zero (6.3.2);
- condições de contorno (6.3.3).

**Pré-requisitos:** EM 6.2.\
**Âncora sugerida:** “Para que serve o H, se o campo de verdade é o B?”

### EM 6.4 Meios lineares e não lineares (6.4)

- suscetibilidade e permeabilidade magnéticas (6.4.1);
- ferromagnetismo: domínios, histerese e temperatura de Curie (6.4.2).

**Pré-requisitos:** EM 6.3.\
**Âncora sugerida:** “Por que um ímã lembra que foi magnetizado?”

## EM 7 — Eletrodinâmica (Griffiths cap. 7)

### EM 7.1 Força eletromotriz (7.1)

- lei de Ohm: `J = σ(E + v×B)` (7.1.1);
- força eletromotriz (7.1.2);
- fem de movimento e a regra do fluxo (7.1.3).

**Pré-requisitos:** EM 5.1, EM 2.3.\
**Âncora sugerida:** “Quem empurra as cargas num circuito?” (a pergunta do `yt_0009`).

### EM 7.2 Indução eletromagnética (7.2)

- lei de Faraday (7.2.1);
- o campo elétrico induzido (7.2.2);
- indutância: mútua, com a fórmula de Neumann, e própria (7.2.3);
- energia em campos magnéticos, `W = (1/2μ₀)∫B² dτ` (7.2.4).

**Pré-requisitos:** EM 7.1, EM 5.4.\
**Âncora sugerida:** “Como um campo magnético que muda cria um campo elétrico?” (a pergunta do `yt_0011`).

### EM 7.3 Equações de Maxwell (7.3)

- a eletrodinâmica antes de Maxwell: a lei de Ampère falha fora da magnetostática (7.3.1);
- como Maxwell consertou a lei de Ampère: a corrente de deslocamento (7.3.2);
- as equações de Maxwell (7.3.3);
- carga magnética: a simetria que faltaria (7.3.4);
- as equações de Maxwell na matéria (7.3.5);
- condições de contorno (7.3.6).

**Pré-requisitos:** EM 7.2.\
**Âncora sugerida:** “O que estava errado na lei de Ampère?” (o capacitor carregando e duas superfícies com a mesma borda).

## EM 8 — Leis de conservação (Griffiths cap. 8)

### EM 8.1 Carga e energia (8.1)

- a equação da continuidade (8.1.1);
- teorema de Poynting e o vetor `S = (1/μ₀) E×B` (8.1.2).

**Pré-requisitos:** EM 7.3.\
**Âncora sugerida:** “Por onde a energia entra num resistor?” (pelo campo em volta do fio, não por dentro dele).

### EM 8.2 Momento (8.2)

- a terceira lei de Newton na eletrodinâmica: duas cargas em movimento (8.2.1);
- o tensor das tensões de Maxwell (8.2.2);
- conservação do momento: o campo carrega momento (8.2.3);
- momento angular no campo (8.2.4).

**Pré-requisitos:** EM 8.1; álgebra linear (13.3) ajuda.\
**Âncora sugerida:** “Quando ação e reação não se anulam, para onde vai o momento?”

### EM 8.3 Forças magnéticas não realizam trabalho (8.3)

- quem realiza o trabalho quando um eletroímã levanta um objeto ou quando um campo magnético empurra um fio com corrente.

**Pré-requisitos:** EM 8.1, EM 7.1.\
**Âncora sugerida:** “Se a força magnética não realiza trabalho, quem levanta o clipe?”

## EM 9 — Ondas eletromagnéticas (Griffiths cap. 9)

### EM 9.1 Ondas em uma dimensão (9.1)

- a equação de onda (9.1.1);
- ondas senoidais e notação complexa (9.1.2);
- condições de contorno: reflexão e transmissão (9.1.3);
- polarização (9.1.4).

**Pré-requisitos:** 5.3; 9.11 (fórmula de Euler).\
**Âncora sugerida:** “Por que parte de uma onda volta quando a corda muda de espessura?”

### EM 9.2 Ondas eletromagnéticas no vácuo (9.2)

- a equação de onda para E e B, com velocidade `1/√(ε₀μ₀)` (9.2.1);
- ondas planas monocromáticas (9.2.2);
- energia e momento: intensidade e pressão de radiação (9.2.3).

**Pré-requisitos:** EM 7.3, EM 9.1.\
**Âncora sugerida:** “Como as equações de Maxwell preveem a velocidade da luz?”

### EM 9.3 Ondas eletromagnéticas na matéria (9.3)

- propagação em meios lineares e índice de refração (9.3.1);
- reflexão e transmissão em incidência normal (9.3.2);
- incidência oblíqua: leis da reflexão e de Snell, equações de Fresnel, ângulo de Brewster (9.3.3).

**Pré-requisitos:** EM 9.2, EM 7.3.\
**Âncora sugerida:** “Por que a luz refletida na água sai polarizada num ângulo especial?”

### EM 9.4 Absorção e dispersão (9.4)

- ondas em condutores: a profundidade de penetração (9.4.1);
- reflexão numa superfície condutora (9.4.2);
- a permissividade depende da frequência: o modelo do oscilador e a dispersão anômala (9.4.3).

**Pré-requisitos:** EM 9.3; 5.2.\
**Âncora sugerida:** “Por que os metais brilham?”\
**Pontes:** 7.2 (dispersão e arco-íris).

### EM 9.5 Ondas guiadas (9.5)

- guias de onda (9.5.1);
- ondas TE num guia retangular e a frequência de corte (9.5.2);
- a linha de transmissão coaxial (9.5.3).

**Pré-requisitos:** EM 9.2, EM 3.3.\
**Âncora sugerida:** “Por que uma onda dentro de um tubo de metal tem uma frequência mínima?”

## EM 10 — Potenciais e campos (Griffiths cap. 10)

### EM 10.1 A formulação por potenciais (10.1)

- potenciais escalar e vetor na eletrodinâmica (10.1.1);
- transformações de calibre (10.1.2);
- calibres de Coulomb e de Lorenz (10.1.3);
- a força de Lorentz em termos dos potenciais (10.1.4).

**Pré-requisitos:** EM 7.3, EM 5.4.\
**Âncora sugerida:** “Se dois potenciais diferentes dão o mesmo campo, qual deles é o verdadeiro?”

### EM 10.2 Distribuições contínuas (10.2)

- potenciais retardados (10.2.1);
- equações de Jefimenko (10.2.2).

**Pré-requisitos:** EM 10.1.\
**Âncora sugerida:** “Se uma carga se mexe aqui, quando o campo muda lá longe?”

### EM 10.3 Cargas pontuais (10.3)

- potenciais de Liénard–Wiechert (10.3.1);
- os campos de uma carga pontual em movimento: o termo de velocidade e o termo de aceleração (10.3.2).

**Pré-requisitos:** EM 10.2; EM 12.1 ajuda.\
**Âncora sugerida:** “Como fica o campo de uma carga que acelera de repente?” (as linhas de campo dobram).

## EM 11 — Radiação (Griffiths cap. 11)

### EM 11.1 Radiação de dipolo (11.1)

- o que é radiação: energia que chega ao infinito, com campos que caem como `1/r` (11.1.1);
- radiação de dipolo elétrico: padrão `sen²θ` e potência proporcional a `ω⁴` (11.1.2);
- radiação de dipolo magnético (11.1.3);
- radiação de uma fonte qualquer (11.1.4).

**Pré-requisitos:** EM 10.2, EM 3.4.\
**Âncora sugerida:** “Por que o céu é azul, e não violeta?” (espalhamento com potência ∝ `ω⁴`, mais o espectro do Sol e a sensibilidade do olho).

### EM 11.2 Cargas pontuais (11.2)

- potência irradiada por uma carga pontual: a fórmula de Larmor (11.2.1);
- reação de radiação (11.2.2);
- o mecanismo da reação de radiação (11.2.3).

**Pré-requisitos:** EM 10.3.\
**Âncora sugerida:** “Pela física clássica, por que o átomo de hidrogênio deveria colapsar em menos de um nanossegundo?”

## EM 12 — Eletrodinâmica e relatividade (Griffiths cap. 12)

### EM 12.1 A teoria da relatividade especial (12.1)

- os postulados de Einstein (12.1.1);
- a geometria da relatividade: simultaneidade, dilatação do tempo e contração do comprimento (12.1.2);
- as transformações de Lorentz (12.1.3);
- a estrutura do espaço-tempo: quadrivetores, intervalo invariante e diagramas (12.1.4).

**Pré-requisitos:** 7.6 ajuda; 13.3.\
**Âncora sugerida:** “O que todos os observadores concordam em medir, se o tempo e o espaço mudam de um para outro?” (o intervalo).

### EM 12.2 Mecânica relativística (12.2)

- tempo próprio e velocidade própria (12.2.1);
- energia e momento relativísticos (12.2.2);
- cinemática relativística: colisões e decaimentos (12.2.3);
- dinâmica relativística (12.2.4).

**Pré-requisitos:** EM 12.1.\
**Âncora sugerida:** “De onde sai o `E = mc²`?”

### EM 12.3 Eletrodinâmica relativística (12.3)

- o magnetismo como fenômeno relativístico (12.3.1);
- como os campos se transformam (12.3.2);
- o tensor do campo (12.3.3);
- a eletrodinâmica em notação tensorial (12.3.4);
- potenciais relativísticos (12.3.5).

**Pré-requisitos:** EM 12.2, EM 7.3.\
**Âncora sugerida:** “O magnetismo é a eletricidade vista de outro referencial?”

---

# PARTE B — CÁLCULO

# 8. Cálculo I — Funções, limites, derivadas e integral básica

| Área | Bloco | Módulos |
|---|---|---|
| Cálculo | Funções, limites e continuidade | 8.1, 8.2, 8.3 |
| Cálculo | Derivadas | 8.4, 8.5, 8.6, 8.7, 8.8, 8.13 |
| Cálculo | Integrais | 8.9, 8.10, 8.11, 8.12 |

**Ordem de estudo:** 8.1 → 8.2 → 8.3 → 8.4 → 8.5 → 8.13 → 8.6 → 8.7 → 8.8 → 8.9 → 8.10 → 8.11 → 8.12.

## 8.1 Funções e gráficos

- domínio e imagem;
- composição;
- inversa;
- transformações de gráfico;
- polinomiais;
- racionais;
- exponenciais;
- logarítmicas;
- trigonométricas;
- funções definidas por partes *(novo)*;
- funções hiperbólicas (extensão) *(novo)*;
- leitura qualitativa.

**Pré-requisitos:** nenhum.\
**Âncora sugerida:** “O que acontece com o gráfico quando f(x) vira f(x − a), a·f(x) ou f(bx)?”

## 8.2 Limites

- ideia de aproximação;
- limites laterais;
- limites infinitos;
- limites no infinito;
- indeterminações;
- técnicas algébricas;
- teorema do confronto e o limite fundamental `sen x / x` *(novo)*;
- o número e como limite *(novo)*;
- definição formal como aprofundamento visual.

**Pré-requisitos:** 8.1.\
**Âncora sugerida:** “Por que `sen x / x` tende a 1 quando x vai a zero?”

## 8.3 Continuidade

- definição;
- tipos de descontinuidade;
- teorema do valor intermediário;
- existência de raízes;
- conexão com limites.

**Pré-requisitos:** 8.2.\
**Âncora sugerida:** “Por que, a qualquer momento, existem dois pontos opostos do equador com a mesma temperatura?” (valor intermediário).

## 8.4 Derivada

- taxa média → taxa instantânea;
- secante → tangente;
- definição por limite;
- interpretação geométrica;
- interpretação física;
- diferenciabilidade.

**Pré-requisitos:** 8.2.\
**Âncora sugerida:** “Como a reta secante vira a reta tangente?”\
**Pontes:** 4.1.

## 8.5 Regras de derivação

- potência;
- soma;
- produto;
- quociente;
- cadeia;
- derivação implícita;
- derivação logarítmica *(novo)*;
- exponenciais e logaritmos;
- trigonométricas;
- funções inversas.

**Pré-requisitos:** 8.4.\
**Âncora sugerida:** “Por que a derivada de eˣ é ela mesma?”

## 8.6 Teoremas e estrutura local de funções

- Rolle;
- valor médio;
- regra de L'Hôpital *(novo)*;
- monotonicidade;
- extremos;
- testes com derivadas;
- concavidade;
- pontos de inflexão.

**Pré-requisitos:** 8.5, 8.3.\
**Âncora sugerida:** “Por que, em algum instante da viagem, o velocímetro marcou exatamente a velocidade média?”

## 8.7 Estudo completo de funções

- domínio;
- zeros;
- sinais;
- limites;
- assíntotas;
- derivada primeira;
- extremos;
- derivada segunda;
- concavidade;
- inflexões;
- esboço consistente.

Este é um dos módulos com maior potencial para vídeos visuais do Parallax Lab.

**Pré-requisitos:** 8.6.\
**Âncora sugerida:** “Como desenhar uma função só com o sinal das derivadas?”

## 8.8 Otimização e taxas relacionadas

- modelagem;
- restrições;
- construção da função objetivo;
- pontos críticos;
- extremos globais;
- interpretação;
- problemas geométricos e físicos;
- taxas relacionadas.

**Pré-requisitos:** 8.6.\
**Âncora sugerida:** “Qual lata gasta menos material para guardar o mesmo volume?” (altura igual ao diâmetro).

## 8.9 Integral e acumulação

- soma de Riemann;
- integral definida;
- área com sinal;
- acumulação;
- função acumulação;
- antiderivada.

**Pré-requisitos:** 8.4.\
**Âncora sugerida:** “Como infinitos retângulos finos dão uma área exata?”

## 8.10 Teorema Fundamental do Cálculo

- derivar uma acumulação;
- integrar uma taxa;
- conexão derivada–integral;
- interpretação geométrica e física.

**Pré-requisitos:** 8.9, 8.5.\
**Âncora sugerida:** “Por que derivar e integrar desfazem uma à outra?”

## 8.11 Substituição

- regra da cadeia ao contrário;
- escolha de substituição;
- mudança de variável;
- integrais definidas e limites transformados.

**Pré-requisitos:** 8.10.\
**Âncora sugerida:** “Por que a substituição é a regra da cadeia lida de trás para a frente?”

## 8.12 Aplicações da integral

- área;
- deslocamento;
- distância;
- valor médio;
- volumes por discos/anéis;
- volumes por cascas, se adequado à sequência adotada;
- princípio de Cavalieri *(novo)*.

**Pré-requisitos:** 8.10, 8.11.\
**Âncora sugerida:** “Como fatiar um sólido para descobrir o volume dele?”

## 8.13 Aproximação linear, diferenciais e método de Newton *(novo)*

- a reta tangente como aproximação;
- diferenciais e propagação de erro;
- método de Newton para raízes.

**Pré-requisitos:** 8.5.\
**Âncora sugerida:** “Como uma sequência de retas tangentes encontra a raiz de uma equação?”

# 9. Cálculo II — Técnicas de integração, curvas, sequências e séries

| Área | Bloco | Módulos |
|---|---|---|
| Cálculo | Técnicas de integração | 9.1, 9.2, 9.3, 9.4, 9.12 |
| Cálculo | Aplicações e curvas | 9.5, 9.6, 9.7 |
| Cálculo | Sequências e séries | 9.8, 9.9, 9.10, 9.11 |

**Ordem de estudo:** 9.1 → 9.2 → 9.3 → 9.4 → 9.12 → 9.5 → 9.6 → 9.7 → 9.8 → 9.9 → 9.10 → 9.11.

## 9.1 Integração por partes

- origem pela regra do produto;
- escolha de `u`;
- aplicações repetidas;
- integrais cíclicas;
- interpretação estrutural.

**Pré-requisitos:** 8.10, 8.5.\
**Âncora sugerida:** “Como a regra do produto vira uma ferramenta de integração?”

## 9.2 Integrais trigonométricas e substituições trigonométricas

- potências de seno/cosseno;
- identidades;
- substituições para radicais;
- interpretação geométrica quando útil.

**Pré-requisitos:** 8.11.\
**Âncora sugerida:** “Por que trocar x por sen θ desfaz a raiz de 1 − x²?”

## 9.3 Frações parciais

- decomposição;
- fatores lineares e quadráticos;
- integração de funções racionais.

**Pré-requisitos:** 8.11.\
**Âncora sugerida:** “Como quebrar uma fração em pedaços que se integram sozinhos?”

## 9.4 Integrais impróprias

- limites infinitos;
- intervalos infinitos;
- singularidades;
- convergência e divergência;
- comparação;
- a trombeta de Gabriel: volume finito, área infinita *(novo)*.

**Pré-requisitos:** 8.10, 8.2.\
**Âncora sugerida:** “Como uma trombeta pode ter volume finito e área infinita?”

## 9.5 Aplicações geométricas avançadas

- comprimento de arco;
- área de superfície de revolução;
- centroide;
- trabalho por força variável;
- outras aplicações conforme interesse editorial.

**Pré-requisitos:** 8.12.\
**Âncora sugerida:** “Por que a área de uma fatia de esfera depende só da espessura da fatia, e não de onde ela é cortada?” (resultado de Arquimedes).

## 9.6 Curvas paramétricas

- parametrização;
- velocidade;
- derivada `dy/dx`;
- segunda derivada;
- comprimento;
- cicloides e outras curvas clássicas.

**Pré-requisitos:** 8.5; 9.5 para o comprimento.\
**Âncora sugerida:** “Que curva um ponto da roda desenha enquanto ela rola?”\
**Pontes:** 4.2, 4.12.

## 9.7 Coordenadas polares

- representação;
- curvas polares;
- inclinação;
- área polar;
- comprimento;
- simetrias.

**Pré-requisitos:** 9.6.\
**Âncora sugerida:** “Como calcular a área de uma rosácea?”

## 9.8 Sequências

- limite;
- monotonicidade;
- limitação;
- recorrências simples;
- convergência.

**Pré-requisitos:** 8.2.\
**Âncora sugerida:** “Uma sequência pode subir para sempre e mesmo assim parar num valor?”

## 9.9 Séries numéricas

- séries geométricas;
- telescópicas;
- testes de convergência;
- comparação;
- razão;
- raiz;
- integral;
- convergência absoluta/condicional.

**Pré-requisitos:** 9.8, 9.4.\
**Âncora sugerida:** “Por que 1 + 1/2 + 1/3 + ... cresce sem limite, se os termos vão a zero?”\
**Pontes:** 4.15.

## 9.10 Séries de potências

- raio e intervalo de convergência;
- operações;
- diferenciação e integração termo a termo.

**Pré-requisitos:** 9.9.\
**Âncora sugerida:** “Por que uma série de potências só funciona dentro de um raio?”

## 9.11 Taylor e Maclaurin

- polinômio local;
- aproximação;
- resto/erro;
- expansões clássicas;
- aplicações em física;
- por que aproximações de pequenas oscilações funcionam;
- fórmula de Euler, `e^{iθ} = cos θ + i sen θ`, pelas séries *(novo)*.

**Pré-requisitos:** 9.10.\
**Âncora sugerida:** “Como um polinômio consegue imitar qualquer função perto de um ponto?”\
**Pontes:** 5.1, 6.13, EM 3.4.

## 9.12 Integração numérica *(novo)*

- regras do trapézio e de Simpson;
- erro e refinamento;
- integrais sem primitiva elementar, como a de `e^{−x²}`.

**Pré-requisitos:** 8.9.\
**Âncora sugerida:** “Como calcular uma integral que não tem primitiva?”

# 10. Cálculo III — Cálculo multivariável

| Área | Bloco | Módulos |
|---|---|---|
| Cálculo | Geometria e curvas no espaço | 10.1, 10.11 |
| Cálculo | Funções de várias variáveis | 10.2, 10.3, 10.4, 10.5, 10.6 |
| Cálculo | Integrais múltiplas | 10.7, 10.8, 10.9, 10.10 |

**Ordem de estudo:** 10.1 → 10.11 → 10.2 → 10.3 → 10.4 → 10.5 → 10.6 → 10.7 → 10.8 → 10.9 → 10.10.

## 10.1 Geometria e vetores em R³

- vetores;
- produto escalar;
- produto vetorial;
- retas;
- planos;
- distâncias;
- superfícies quádricas.

**Pré-requisitos:** geometria analítica básica.\
**Âncora sugerida:** “O que o produto vetorial mede de verdade?” (área orientada).

## 10.2 Funções de várias variáveis

- domínio;
- gráficos;
- curvas e superfícies de nível;
- limites;
- continuidade.

**Pré-requisitos:** 10.1, 8.2.\
**Âncora sugerida:** “Como ler um mapa de curvas de nível como se fosse a montanha?”

## 10.3 Derivadas parciais

- interpretação;
- plano tangente;
- linearização;
- diferenciais;
- aproximações locais.

**Pré-requisitos:** 10.2, 8.13.\
**Âncora sugerida:** “O que é o plano tangente a uma superfície?”

## 10.4 Regra da cadeia multivariável

- dependências compostas;
- Jacobiano;
- derivação implícita;
- mudanças de coordenadas.

**Pré-requisitos:** 10.3.\
**Âncora sugerida:** “Como uma pequena mudança se espalha por uma cadeia de dependências?”

## 10.5 Gradiente e derivada direcional

- direção de maior crescimento;
- ortogonalidade às curvas/superfícies de nível;
- interpretação geométrica;
- aplicações físicas.

**Pré-requisitos:** 10.3.\
**Âncora sugerida:** “Por que o gradiente aponta para a subida mais íngreme?”\
**Pontes:** 4.8, 6.4.

## 10.6 Extremos em várias variáveis

- pontos críticos;
- Hessiana;
- classificação;
- otimização com restrições;
- multiplicadores de Lagrange.

**Pré-requisitos:** 10.5, 8.6.\
**Âncora sugerida:** “Por que, no ótimo com restrição, os dois gradientes ficam paralelos?”

## 10.7 Integrais duplas

- soma e volume;
- regiões gerais;
- troca da ordem de integração;
- coordenadas polares.

**Pré-requisitos:** 8.10, 10.2.\
**Âncora sugerida:** “Como trocar a ordem de integração transforma uma integral impossível numa fácil?”

## 10.8 Integrais triplas

- volumes;
- massa;
- densidades;
- coordenadas cilíndricas;
- coordenadas esféricas.

**Pré-requisitos:** 10.7.\
**Âncora sugerida:** “Qual a massa de uma esfera cuja densidade cresce para fora?”

## 10.9 Mudança de variáveis e Jacobiano

- origem geométrica do fator de área/volume;
- transformações;
- polar, cilíndrica e esférica;
- mudanças gerais simples.

**Pré-requisitos:** 10.7, 10.4.\
**Âncora sugerida:** “Por que a integral de `e^{−x²}` na reta inteira dá √π?” (o truque das coordenadas polares).\
**Pontes:** 13.4.

## 10.10 Aplicações físicas

- centro de massa;
- momentos;
- densidades não uniformes;
- distribuições espaciais;
- integrais que reaparecem em eletromagnetismo e mecânica.

**Pré-requisitos:** 10.8, 10.9.\
**Âncora sugerida:** “Onde fica o centro de massa de um hemisfério?” (a 3R/8 da base).\
**Pontes:** 4.9, 4.11, EM 2.1.

## 10.11 Funções vetoriais e curvas no espaço *(novo)*

- curvas parametrizadas em R³;
- vetores velocidade e aceleração;
- comprimento de arco no espaço;
- curvatura e torção;
- triedro de Frenet (extensão).

**Pré-requisitos:** 10.1, 9.6.\
**Âncora sugerida:** “Como medir quanto uma curva se dobra e se torce?”\
**Pontes:** 4.2, 6.7 (a hélice da carga).

# 11. Cálculo IV — Cálculo vetorial

| Área | Bloco | Módulos |
|---|---|---|
| Cálculo | Campos e integrais de linha | 11.1, 11.2, 11.3, 11.4 |
| Cálculo | Superfícies e fluxo | 11.6, 11.7 |
| Cálculo | Divergente, rotacional e os grandes teoremas | 11.5, 11.8, 11.9, 11.10, 11.11, 11.12 |

**Ordem de estudo:** 11.1 → 11.2 → 11.3 → 11.4 → 11.5 → 11.6 → 11.7 → 11.8 → 11.12 → 11.9 → 11.10 → 11.11.

## 11.1 Campos escalares e vetoriais

- visualização;
- linhas de campo;
- campos em 2D e 3D;
- interpretação física.

**Pré-requisitos:** 10.2.\
**Âncora sugerida:** “O que as linhas de campo mostram, e o que elas escondem?”

## 11.2 Integrais de linha escalares

- parametrização;
- comprimento de arco;
- densidade ao longo de curvas.

**Pré-requisitos:** 10.11, 9.5.\
**Âncora sugerida:** “Qual a massa de um arame cuja densidade muda ao longo dele?”

## 11.3 Trabalho e integrais de linha vetoriais

- trabalho;
- circulação;
- orientação;
- dependência do caminho.

**Pré-requisitos:** 11.2.\
**Âncora sugerida:** “Por que o trabalho de uma força pode depender do caminho?”\
**Pontes:** 4.7.

## 11.4 Campos conservativos e potenciais

- gradiente;
- independência de caminho;
- função potencial;
- condições de conservatividade;
- conexão direta com Mecânica e Eletrostática.

**Pré-requisitos:** 11.3, 10.5.\
**Âncora sugerida:** “Como saber se um campo tem potencial sem testar todos os caminhos?”\
**Pontes:** 4.8, EM 2.3.

## 11.5 Teorema de Green

- circulação;
- fluxo em 2D;
- orientação;
- área como aplicação;
- interpretação geométrica.

**Pré-requisitos:** 11.3, 10.7.\
**Âncora sugerida:** “Como um planímetro mede uma área só percorrendo a borda?”

## 11.6 Superfícies parametrizadas

- parametrização;
- vetores tangentes;
- elemento de área;
- orientação.

**Pré-requisitos:** 10.1, 10.9.\
**Âncora sugerida:** “Como medir a área de uma superfície curva?”

## 11.7 Integrais de superfície

- campos escalares;
- fluxo;
- superfícies abertas/fechadas.

**Pré-requisitos:** 11.6.\
**Âncora sugerida:** “Quanto de um campo atravessa uma superfície?”

## 11.8 Divergência e rotacional

- significado local;
- fontes/sumidouros;
- circulação local;
- visualização;
- aplicações físicas.

**Pré-requisitos:** 10.3, 11.1.\
**Âncora sugerida:** “O que o divergente e o rotacional medem num ponto?”\
**Pontes:** EM 1.2, EM 2.2, EM 5.3.

## 11.9 Teorema de Stokes

- circulação × rotacional;
- orientação;
- conexão entre comportamento local e contorno.

**Pré-requisitos:** 11.7, 11.8.\
**Âncora sugerida:** “Por que a circulação na borda só depende do rotacional dentro dela?”\
**Pontes:** EM 7.2.

## 11.10 Teorema da divergência de Gauss

- fluxo por superfície fechada;
- divergência no volume;
- fontes;
- conexão com leis de campo.

**Pré-requisitos:** 11.7, 11.8.\
**Âncora sugerida:** “Por que o fluxo pela casca conta exatamente o que nasce lá dentro?”\
**Pontes:** EM 2.2, 4.13.

## 11.11 Síntese dos grandes teoremas

Objetivo editorial: mostrar Green, Stokes e Gauss como manifestações de uma mesma ideia — uma grandeza acumulada no interior se conecta a uma grandeza medida na fronteira.

Esse é um módulo especialmente adequado ao princípio visual do Parallax Lab.

**Pré-requisitos:** 11.5, 11.9, 11.10.\
**Pontes:** EM 1.3; 8.10 (o teorema fundamental em uma dimensão).

## 11.12 Operadores em coordenadas curvilíneas e laplaciano *(novo)*

- gradiente, divergente, rotacional e laplaciano em coordenadas cilíndricas e esféricas;
- fatores de escala;
- o laplaciano como a diferença entre o valor num ponto e a média em volta;
- funções harmônicas;
- identidades: `∇×(∇f) = 0` e `∇·(∇×F) = 0`.

**Pré-requisitos:** 11.8, 10.9.\
**Âncora sugerida:** “O que o laplaciano mede de verdade?”\
**Pontes:** EM 1.2, EM 1.4, EM 3.1, 15.3.

---

# PARTE C — CONEXÕES ENTRE OS CURSOS

# 12. Pontes prioritárias Física ↔ Matemática

## Derivada ↔ cinemática

- `v=dx/dt`;
- `a=dv/dt`;
- inclinação de gráficos;
- taxas relacionadas.

## Integral ↔ movimento

- deslocamento como integral da velocidade;
- impulso como integral da força;
- trabalho como integral de `F dx`.

## Derivada ↔ potencial

- `F=-dU/dx`;
- estabilidade e derivadas;
- aproximações locais.

## Séries de Taylor ↔ pequenas oscilações

- aproximação quadrática de potenciais;
- seno para pequenos ângulos;
- origem local do oscilador harmônico;
- a mesma ideia na expansão multipolar (EM 3.4) *(novo)*.

## Cálculo multivariável ↔ campos

- gradiente ↔ potencial;
- integrais múltiplas ↔ distribuições contínuas;
- coordenadas adaptadas à simetria.

## Cálculo vetorial ↔ Eletromagnetismo

- fluxo;
- circulação;
- Gauss;
- Ampère;
- Faraday;
- Maxwell;
- divergência e rotacional;
- por módulo: 11.8 ↔ EM 1.2, EM 2.2 e EM 5.3; 11.9 ↔ EM 7.2; 11.10 ↔ EM 2.2; 11.12 ↔ EM 1.4 e EM 3.1 *(novo)*;
- delta de Dirac ↔ cargas pontuais (EM 1.5) *(novo)*.

## EDO ↔ oscilações e circuitos *(novo)*

- 14.3–14.5 ↔ 5.1–5.2 ↔ 6.11 e 6.13: massa–mola e RLC obedecem à mesma equação;
- 14.1 ↔ 4.5 (velocidade terminal), 5.12 (resfriamento), 6.6 (circuito RC) e 7.12 (decaimento).

## Álgebra linear ↔ física *(novo)*

- autovetores ↔ modos normais (13.5 ↔ 5.13) e eixos principais de inércia (4.11);
- transformações lineares ↔ rotações e transformações de Lorentz (13.3 ↔ 7.6, EM 12.1);
- tensores ↔ tensor das tensões de Maxwell e tensor do campo (EM 8.2, EM 12.3).

## EDP e Fourier ↔ física *(novo)*

- equação da onda ↔ cordas, som e ondas eletromagnéticas (15.1 ↔ 5.3, EM 9.2);
- equação do calor ↔ condução (15.2 ↔ 5.12);
- equação de Laplace ↔ potenciais (15.3 ↔ EM 3.1, EM 3.3);
- transformada de Fourier ↔ difração (15.6 ↔ 7.4).

## Física III e IV ↔ Eletromagnetismo *(novo)*

O mesmo assunto em dois níveis. Tabela no Anexo B.

---

# PARTE D — MATEMÁTICA ALÉM DO CÁLCULO E DISCIPLINAS AVANÇADAS

# 13. Álgebra Linear

Entra na grade junto com Cálculo II (§0.2); na v1 era "futura". Os módulos 13.1–13.9 são novos e reúnem os tópicos da lista da v1; os acréscimos estão marcados.

| Área | Bloco | Módulos |
|---|---|---|
| Álgebra Linear | Sistemas e espaços vetoriais | 13.1, 13.2 |
| Álgebra Linear | Transformações e determinantes | 13.3, 13.4 |
| Álgebra Linear | Autovalores e ortogonalidade | 13.5, 13.6, 13.7 |
| Álgebra Linear | Aplicações e decomposições | 13.8, 13.9 |

## 13.1 Sistemas lineares

- sistemas lineares e eliminação de Gauss;
- interpretação geométrica: interseção de retas e de planos *(novo)*;
- sistemas sem solução e com infinitas soluções *(novo)*.

**Pré-requisitos:** nenhum.\
**Âncora sugerida:** “Por que três planos podem se cruzar num ponto, numa reta ou em lugar nenhum?”

## 13.2 Espaços vetoriais

- vetores e subespaços;
- independência linear;
- base e dimensão.

**Pré-requisitos:** 13.1, 10.1.\
**Âncora sugerida:** “O que quer dizer um conjunto de vetores ser independente?”

## 13.3 Transformações lineares

- transformações lineares;
- matriz de uma transformação;
- composição como produto de matrizes *(novo)*.

**Pré-requisitos:** 13.2.\
**Âncora sugerida:** “Por que toda transformação linear cabe numa matriz?”

## 13.4 Determinantes

- determinantes;
- determinante como fator de área e de volume *(novo)*.

**Pré-requisitos:** 13.3.\
**Âncora sugerida:** “Por que o determinante mede quanto uma transformação estica a área?”\
**Pontes:** 10.9 (Jacobiano).

## 13.5 Autovalores e autovetores

- autovalores e autovetores;
- diagonalização.

**Pré-requisitos:** 13.4.\
**Âncora sugerida:** “Quais direções uma transformação não gira?”\
**Pontes:** 5.13, 14.6.

## 13.6 Produto interno e ortogonalidade

- produto interno;
- ortogonalidade;
- Gram–Schmidt;
- projeções;
- mínimos quadrados *(novo)*.

**Pré-requisitos:** 13.2.\
**Âncora sugerida:** “Como achar a reta que melhor passa por pontos que não se alinham?”

## 13.7 Formas quadráticas

- formas quadráticas;
- eixos principais de uma cônica *(novo)*.

**Pré-requisitos:** 13.5, 13.6.\
**Âncora sugerida:** “Por que toda elipse inclinada vira uma elipse reta num eixo girado?”

## 13.8 Aplicações

- aplicações a rotações, modos normais e mecânica/quântica.

**Pré-requisitos:** 13.5.\
**Âncora sugerida:** “Como os modos normais saem dos autovetores?”

## 13.9 Decomposições matriciais

- decomposições matriciais como expansão posterior;
- decomposição em valores singulares (SVD) *(novo)*.

**Pré-requisitos:** 13.5, 13.6.\
**Âncora sugerida:** “Por que toda matriz é uma rotação, um esticamento e outra rotação?” (com rigor: rotações ou reflexões).

# 14. Equações Diferenciais Ordinárias

Entra na grade junto com Cálculo III (§0.2); na v1 era "futura". Os módulos 14.1–14.9 são novos e reúnem os tópicos da lista da v1; os acréscimos estão marcados.

| Área | Bloco | Módulos |
|---|---|---|
| Equações diferenciais | EDO de primeira ordem | 14.1, 14.2 |
| Equações diferenciais | EDO de segunda ordem | 14.3, 14.4, 14.5 |
| Equações diferenciais | Sistemas e métodos | 14.6, 14.7, 14.8, 14.9 |

## 14.1 Equações de primeira ordem

- equações de primeira ordem;
- separáveis;
- lineares;
- problemas de valor inicial;
- existência e unicidade, em nível adequado *(novo)*.

**Pré-requisitos:** 8.10, 8.11.\
**Âncora sugerida:** “Como achar uma função conhecendo só a taxa com que ela muda?”

## 14.2 Campos de direção e modelos

- campos de direção;
- crescimento e decaimento;
- crescimento logístico *(novo)*;
- resfriamento de Newton e velocidade terminal como modelos *(novo)*.

**Pré-requisitos:** 14.1.\
**Âncora sugerida:** “Por que uma população não cresce exponencialmente para sempre?”

## 14.3 Equações lineares de segunda ordem

- equações de segunda ordem;
- coeficientes constantes e equação característica *(novo)*;
- superposição de soluções *(novo)*.

**Pré-requisitos:** 14.1, 8.5.\
**Âncora sugerida:** “Por que as soluções de uma EDO linear com coeficientes constantes são exponenciais?”

## 14.4 Oscilador harmônico e amortecimento

- oscilador harmônico;
- amortecimento.

**Pré-requisitos:** 14.3.\
**Âncora sugerida:** “Por que um oscilador amortecido tem exatamente três jeitos de voltar ao repouso?”\
**Pontes:** 5.1, 5.2.

## 14.5 Forçamento e ressonância

- forçamento e ressonância.

**Pré-requisitos:** 14.4.\
**Âncora sugerida:** “Por que, sem atrito, a resposta cresce sem limite quando a força acompanha o ritmo natural?”\
**Pontes:** 5.2, 6.13.

## 14.6 Sistemas lineares e plano de fase

- sistemas lineares;
- plano de fase;
- autovalores e estabilidade.

**Pré-requisitos:** 14.3, 13.5.\
**Âncora sugerida:** “Como prever o futuro de um sistema sem resolver a equação?”

## 14.7 Transformada de Laplace

- transformada de Laplace;
- a derivada vira multiplicação por s *(novo)*.

**Pré-requisitos:** 14.3, 9.4.\
**Âncora sugerida:** “Como a transformada de Laplace troca derivadas por álgebra?”

## 14.8 Soluções por séries de potências

- séries de potências;
- polinômios de Legendre e funções de Bessel (extensão) *(novo)*.

**Pré-requisitos:** 14.3, 9.10.\
**Âncora sugerida:** “Como resolver uma equação cuja solução não é nenhuma função conhecida?”\
**Pontes:** EM 3.3.

## 14.9 Métodos numéricos *(novo)*

- métodos de Euler e de Runge–Kutta;
- passo, erro e estabilidade.

**Pré-requisitos:** 14.1.\
**Âncora sugerida:** “Como o computador resolve uma EDO, um passo de cada vez?”

# 15. Equações Diferenciais Parciais e métodos de Fourier

Entra na grade junto com o Eletromagnetismo (§0.2); na v1 era "futura". Os módulos 15.1–15.6 são novos e reúnem os tópicos da lista da v1; os acréscimos estão marcados. Conexões com ondas, termodinâmica, eletromagnetismo e quântica: §12.

| Área | Bloco | Módulos |
|---|---|---|
| Equações diferenciais | EDP e Fourier | 15.1, 15.2, 15.3, 15.4, 15.5, 15.6 |

## 15.1 Equação da onda

- equação da onda;
- modos normais;
- a solução de d'Alembert *(novo)*.

**Pré-requisitos:** 10.3, 14.3.\
**Âncora sugerida:** “Por que qualquer onda numa corda é a soma de duas ondas viajando em sentidos opostos?”

## 15.2 Equação do calor e difusão

- equação do calor;
- difusão.

**Pré-requisitos:** 10.3, 14.1.\
**Âncora sugerida:** “Por que o calor se espalha e apaga os detalhes?”

## 15.3 Equação de Laplace

- equação de Laplace;
- funções harmônicas e a propriedade da média *(novo)*.

**Pré-requisitos:** 11.12.\
**Âncora sugerida:** “Como achar a temperatura de equilíbrio dentro de uma placa?”

## 15.4 Condições de contorno e separação de variáveis

- condições de contorno;
- separação de variáveis.

**Pré-requisitos:** 15.1, 15.2 ou 15.3.\
**Âncora sugerida:** “Como uma EDP se quebra em várias EDOs?”

## 15.5 Séries de Fourier

- séries de Fourier;
- modos normais como base;
- fenômeno de Gibbs *(novo)*.

**Pré-requisitos:** 15.4, 9.9.\
**Âncora sugerida:** “Como somar senos para fazer uma onda quadrada?”

## 15.6 Transformada de Fourier *(novo)*

- a transformada de Fourier;
- largura de um sinal × largura do espectro;
- a figura de difração como transformada da abertura.

**Pré-requisitos:** 15.5, 9.4.\
**Âncora sugerida:** “Por que a figura de difração é a transformada de Fourier da fenda?”\
**Pontes:** 7.4, 7.9.

# 16. Disciplinas avançadas possíveis

Sem compromisso de implementação. Quando uma delas entrar em produção, ganha módulos com IDs pela referência escolhida, como o Eletromagnetismo.

- Análise Complexa;
- Probabilidade e Estatística;
- Métodos Matemáticos da Física;
- Mecânica Analítica;
- Mecânica Clássica intermediária: forças centrais, corpo rígido, Lagrange e Hamilton, caos *(novo)*;
- Mecânica Quântica mais formal (referência natural: Griffiths, *Introduction to Quantum Mechanics*, do mesmo autor do Eletromagnetismo);
- Física Estatística *(novo)*;
- Relatividade em maior profundidade;
- Física Matemática.

---

# PARTE E — REGRAS EDITORIAIS

# 17. Ordem de publicação não é ordem curricular

Não numerar vídeos públicos como se a publicação precisasse seguir o currículo. O mapa ordena a biblioteca; o calendário é livre e pode variar de disciplina e de nível de um vídeo para o outro.

O vídeo publicado hoje pode ocupar futuramente a posição 7 de uma playlist.

Seguir a sequência de um livro por um tempo, como os longos de eletromagnetismo vêm seguindo o Griffiths, é uma escolha válida, não uma obrigação.

A prioridade para escolher a próxima pauta é a combinação de:

1. qualidade didática;
2. potencial visual;
3. rigor;
4. capacidade de funcionar sozinho;
5. valor para a biblioteca futura;
6. interesse observado do público;
7. custo de produção.

# 18. Como escolher a próxima pauta longa

Antes de aprovar um tema, perguntar:

- Em qual disciplina, bloco e módulo (ID) ele entra? Em qual nível (Física III ou EM; Física IV ou EM 12)?
- É âncora conceitual, derivação/aplicação ou exercício?
- Funciona sozinho?
- O que ele acrescenta à biblioteca? (O Anexo A mostra o que o módulo já tem.)
- Existe um payoff visual forte?
- Ele cria uma ponte útil para outro vídeo futuro?
- O assunto sustenta um longo sem enchimento? A duração sai da explicação: os longos entregues têm de 12 a 27 min (`docs/padrao_video_longo.md` §6).
- É possível representar a ideia com Manim de maneira melhor que uma aula tradicional?
- Algum sólido do arsenal 3D ajuda? Consultar `experimentos/blender/arsenal/indice_producao.md` e `cobertura.md` e preencher `solido_3d:` com um id aprovado ou "nenhum, porque ...". O 3D dá só a geometria; não forçar 3D onde o 2D explica melhor.
- Qual é a referência, com seções? (No EM, as subseções do Griffiths.)

Se as respostas forem fracas, a pauta pode ser boa para curto e ruim para longo.

# 19. Regra para exercícios específicos

Exercícios resolvidos longos são desejáveis.

Eles não precisam introduzir um bloco, mas devem ter endereço curricular claro.

Exemplo:

**Física I → Cinemática → 4.3 Lançamentos → exercício de alcance ótimo a partir de uma altura.**

O exercício pode ser publicado antes das aulas teóricas relacionadas. Depois ele entra na posição didática correta da playlist.

Para inaugurar um módulo importante, dar preferência a um vídeo-âncora conceitual quando isso produzir uma biblioteca mais coerente.

# 20. Curtos no mapa *(novo)*

Substitui o §20 da v1 ("Primeiro piloto long-form recomendado"), que ficou desatualizado: o plano daquele piloto mora agora em 4.8.

- Todo curto novo recebe um módulo (ID) no planejamento. A série define a forma, não o endereço.
- O nível do tratamento decide o módulo, como nos longos (§0.3): o campo no eixo do anel é 6.2; a energia do solenoide no nível de Física III é 6.11.
- Um curto não precisa de longo no mesmo módulo, nem o contrário. Quando os dois existem, o curto pode apontar para o longo, sem virar teaser.
- Na ficha do curto, o endereço vai em `disciplina:` e `modulo:` (`docs/formatos.md`).

# 21. Fonte de verdade e manutenção

Este documento registra a **arquitetura editorial de conteúdo**: disciplinas, blocos, módulos, IDs e regras de endereço.

Ele não substitui:

- `docs/estado_atual.md` para estado operacional;
- `docs/decisoes.md` para decisões estáveis;
- `docs/formatos.md` para regras dos formatos e campos da ficha;
- `docs/padrao_video_longo.md` para a forma dos longos (tag do canto, cores, narração);
- `docs/identidade_visual.md` para identidade;
- `experimentos/blender/arsenal/cobertura.md` para os sólidos 3D por módulo;
- `AGENTS.md` para comportamento de agentes.

Atualize este mapa quando:

- um módulo for reorganizado;
- um curso/eixo novo for oficialmente incorporado;
- uma fronteira curricular mudar de forma duradoura;
- uma nova disciplina futura sair de “planejada” e entrar em produção;
- a referência de uma disciplina mudar, por exemplo outra edição do Griffiths *(novo)*.

Não atualizar os módulos após cada vídeo apenas para marcar progresso. O progresso de unidades pertence ao estado operacional e às fichas dos vídeos. O Anexo A é a exceção: é um retrato datado e, quando for atualizado, a data muda junto *(novo)*.

`docs/` é global (`AGENTS.md`): mudanças neste arquivo acontecem em rodada própria, nunca escondidas na produção de um vídeo.

---

# ANEXOS

## Anexo A — Retrato da cobertura em 2026-10-27

Fontes: fichas do repositório, `docs/estado_atual.md` (25/10), as pautas do projeto e os nomes das pastas em `entregas/` no PC pessoal. Publicação não é registrada no repositório. Este retrato não substitui o estado operacional.

### Longos

| Vídeo | Módulo | Referência | Assunto | Situação |
|---|---|---|---|---|
| `yt_0001` | EM 2.2 | Griffiths 2.2 | Lei de Gauss | entregue |
| `yt_0002` | EM 2.2 | Griffiths 2.2.3 | Lei de Gauss: três simetrias, um método | entregue |
| `yt_0003` | EM 2.2 | Griffiths 2.2.2 e 2.2.4 | Divergente e rotacional do campo eletrostático | entregue |
| `yt_0004` | EM 2.2 | Griffiths 2.2.3 e 2.1.3 (superposição) | Exercícios resolvidos: configurações estranhas e não simétricas, por superposição | entregue (`exercicio_resolvido`) |
| `yt_0005` | EM 5.1 | Griffiths 5.1 | Força de Lorentz | entregue |
| `yt_0006` | EM 5.2 | Griffiths 5.2 | Lei de Biot–Savart | entregue |
| `yt_0007` | 4.13 | Moysés vol. 1, Sears *Física I* (gravitação) | Por que uma órbita é uma queda que nunca termina? | em preview, a terminar |
| `yt_0008` | EM 5.3 | Griffiths 5.3 | Divergente, rotacional e Lei de Ampère | entregue |
| `yt_0009` | EM 7.1 | Griffiths 7.1.1–7.1.2 | Quem empurra as cargas? (Lei de Ohm e força eletromotriz) | entregue |
| `yt_0010` | EM 7.1 | Griffiths 7.1.3 | FEM de movimento e regra do fluxo magnético | entregue |
| `yt_0011` | EM 7.2 | Griffiths 7.2.1–7.2.2 | Lei de Faraday e campo elétrico induzido | entregue |
| `yt_0012` | EM 7.2 | Griffiths 7.2.3–7.2.4 | Indutância e energia magnética | entregue |
| `yt_0013` | 4.10 | — | Colisões em 1D | entregue |
| `yt_0014` | 4.10 | — | Colisões em 2D | pasta em `entregas/` (conferir) |

As fichas antigas citam a posição da v1 (`yt_0002`: §6.3; `yt_0006`: 6.8; `yt_0012`: 6.11). Pelo Anexo B, elas correspondem aos módulos EM acima; não é preciso editar as fichas.

### Curtos, na ordem dos módulos

| Módulo | Curto | Série |
|---|---|---|
| 4.1 | `vid_0004` Velocidade instantânea | Da Equação ao Fenômeno |
| 4.5 | `vid_0019` E se o ar parasse de frear a chuva? | Absurdo Calculável |
| 4.5 | `vid_0023` Qual o melhor ângulo para puxar uma caixa? | Exercício Resolvido |
| 4.6 | `vid_0005` De onde vem a aceleração centrípeta | Por Trás da Fórmula |
| 4.8 | `vid_0013` Potencial de poço duplo | Da Equação ao Fenômeno |
| 4.10 | `vid_0026` Colisão no cruzamento (em produção) | Exercício Resolvido |
| 4.11 | `vid_0014` Por que o eixo muda o momento de inércia? | Por Trás da Fórmula |
| 4.12 | `vid_0010` Esfera maciça rolando num looping | Exercício Resolvido |
| 5.5 | `vid_0006` Interferência e cancelamento ativo de ruído | Da Equação ao Fenômeno |
| 5.6 | `vid_0022` Superfície de um líquido em rotação (ponte com 4.14) | Por Trás da Fórmula |
| 5.7 | `vid_0016` Torricelli: onde furar para o jato ir mais longe | Da Equação ao Fenômeno |
| 5.7 | `vid_0018` Bernoulli | Por Trás da Fórmula |
| 5.9 | `vid_0021` Ciclo termodinâmico | Exercício Resolvido |
| 5.10 | `vid_0011` De onde vem PV^γ = constante | Por Trás da Fórmula |
| 6.2 | `vid_0007` Campo elétrico no eixo de um anel carregado | Exercício Resolvido |
| 6.3 | `vid_0012` O campo máximo está na superfície? | Exercício Resolvido |
| 6.7 | `vid_0024` Por que uma carga faz uma hélice? | Da Equação ao Fenômeno |
| 6.8 | `vid_0008` Campo magnético no eixo de uma espira | Por Trás da Fórmula |
| 6.8 | `vid_0015` Duas linhas carregadas em movimento (ponte com EM 12.3) | Exercício Resolvido |
| 6.9 | `vid_0009` Campo magnético de um solenoide | Da Equação ao Fenômeno |
| 6.9 | `vid_0029` Campo do toroide (em produção) | Por Trás da Fórmula |
| 6.11 | `vid_0027` Energia de um solenoide (em produção) | Exercício Resolvido |
| 7.2 | `vid_0025` Por que o arco-íris tem 42°? (em produção) | Da Equação ao Fenômeno |
| 7.6 | `vid_0017` Uma bateria carregada pesa mais? | Absurdo Calculável |
| 7.6 | `vid_0028` Soma relativística de velocidades (em produção) | Da Equação ao Fenômeno |
| 8.11 | `vid_0002` Integral por substituição | Exercício Resolvido |
| 8.12 | `vid_0030` O anel de guardanapo (em produção) | Absurdo Calculável |
| 9.1 | `vid_0001` Integração por partes | Exercício Resolvido |
| 9.1 | `vid_0003` De onde vem a fórmula da integração por partes? | Por Trás da Fórmula |
| 10.7 | `vid_0020` Por que uma integral dupla calcula volume? | Por Trás da Fórmula |

"Em produção" vem das pautas do projeto em 2026-10-27; conferir com as fichas antes de usar.

### Leitura rápida

- **Eletromagnetismo:** os longos seguiram o Griffiths em EM 2.2, EM 5.1–5.3 e EM 7.1–7.2. Na ordem do livro, o próximo é EM 7.3 (equações de Maxwell). Sem longo: EM 1, EM 2.1, EM 2.3–2.5, EM 3, EM 4, EM 5.4, EM 6 e EM 8 a EM 12.
- **Física I:** só 4.10 tem longo (dois). A âncora recomendada de 4.8 (energia potencial) continua sem longo.
- **Física II, Física III, Física IV e Cálculo I a IV:** só curtos.
- **Álgebra Linear, EDO e EDP:** nenhum vídeo ainda.

## Anexo B — O mesmo assunto em dois níveis

Física III (nível Moysés/Sears) ↔ Eletromagnetismo (Griffiths):

| Física III | Eletromagnetismo | Observação |
|---|---|---|
| 6.1 Carga e lei de Coulomb | EM 2.1 | |
| 6.2 Campo elétrico | EM 2.1 | o dipolo também em EM 3.4.4 |
| 6.3 Lei de Gauss | EM 2.2 | |
| 6.4 Potencial elétrico | EM 2.3, EM 2.4 | |
| 6.5 Condutores e capacitores | EM 2.5, EM 4 | dielétricos em EM 4 |
| 6.6 Corrente e circuitos DC | EM 7.1 | circuitos (Kirchhoff, RC) aparecem pouco no Griffiths |
| 6.7 Força magnética | EM 5.1, EM 6.1 | torque em espira em EM 6.1.2 |
| 6.8 Biot–Savart | EM 5.2 | |
| 6.9 Lei de Ampère | EM 5.3 | |
| 6.10 Indução | EM 7.1.3, EM 7.2.1–7.2.2 | |
| 6.11 Indutância | EM 7.2.3–7.2.4 | RL, LC e RLC são de circuitos |
| 6.12 Maxwell e ondas | EM 7.3, EM 8.1, EM 9.2 | |
| 6.13 Circuitos CA | — | sem equivalente no Griffiths |
| 6.14 Magnetismo na matéria | EM 6 | |

Física IV ↔ Eletromagnetismo:

| Física IV | Eletromagnetismo |
|---|---|
| 7.1 Ondas eletromagnéticas e luz | EM 9.2 |
| 7.2 Óptica geométrica | EM 9.3.3 (reflexão e Snell a partir das condições de contorno) |
| 7.5 Polarização | EM 9.1.4, EM 9.3.3 (Brewster) |
| 7.6 Relatividade especial | EM 12.1, EM 12.2 |

## Anexo C — O que mudou da v1 para a v2

**Verificação.** Um script comparou os 754 itens de texto da v1 (cada item de lista e cada parágrafo) com o corpo da v2 (sem este anexo, que cita alguns deles). 721 aparecem literalmente. Os 33 restantes foram reescritos de propósito, todos nas partes de instrução, e estão listados abaixo. Nenhum tópico de conteúdo dos módulos se perdeu. Dos 93 títulos de módulo da v1, só um mudou de nome (4.5).

**Estrutura**

- Níveis da biblioteca: "curso/eixo → macroassunto → módulo" virou "disciplina → bloco → módulo" (§0.1). O bloco é o nível que as pastas de entrega já usam (Eletrostática, Eletrodinâmica, Colisões).
- §1 a §3 da v1 viraram a Parte 0 (0.1 a 0.6). As coordenadas obrigatórias do §2 viraram a tabela de endereço (§0.3), com referência e IDs.
- O Eletromagnetismo (Griffiths) entrou como disciplina nova, depois de Física IV.
- O §12 ganhou pontes com EDO, Álgebra Linear, EDP e EM, e passou a se chamar "Física ↔ Matemática".
- §13 a §15 deixaram de ser "futuras": viraram disciplinas da grade, com módulos 13.1–13.9, 14.1–14.9 e 15.1–15.6 montados a partir das listas da v1.
- O §16 "Outras expansões possíveis" virou "Disciplinas avançadas possíveis" e ganhou Mecânica Clássica intermediária e Física Estatística.
- O §20 da v1 (primeiro piloto do long-form, com o `yt_0001` como energia potencial) estava desatualizado. O plano foi para 4.8, e o §20 agora trata dos curtos no mapa.

**Textos da v1 reescritos de propósito (os 33 itens)**

- Cabeçalho: "Status", "Escopo atual: Física I–IV e Cálculo I–IV", "Futuro planejado" e "Importante" viraram a versão, o "O que é / O que não é" e a grade com EM, Álgebra Linear, EDO e EDP.
- §1 e §2: a frase dos níveis da biblioteca e os sete campos obrigatórios viraram a tabela do §0.3. "A taxonomia é editorial" virou a frase de abertura do §0.2.
- 4.8: "Vídeo-âncora recomendado para inaugurar o long-form" virou "Âncora recomendada", porque o long-form já começou.
- 7 (nota): "tópicos posteriores a Eletromagnetismo" virou "posteriores a Física III", porque o Eletromagnetismo agora é a disciplina do Griffiths.
- 13: "Status: planejada, não é backlog obrigatório atual" saiu; nenhum módulo é backlog obrigatório (§17).
- §18: as três perguntas (curso/eixo, macroassunto, módulo) viraram uma só, com nível; "justifica 8–10 minutos" virou a duração observada de 12 a 27 min; entraram o arsenal 3D e a referência.
- §19: o exemplo ganhou bloco e ID (Física I → Cinemática → 4.3).
- §20: os itens do "estado editorial recomendado" do piloto (`yt_0001`, curso, macroassunto, módulo, natureza, título, ideias centrais, construção visual) foram para 4.8.
- §21: "não atualizar o arquivo após cada vídeo" passou a valer para os módulos, com o Anexo A como retrato datado.

**Módulos novos:** 4.14 Referenciais não inerciais · 4.15 Equilíbrio estático e elasticidade · 5.13 Oscilações acopladas e modos normais · 6.13 Circuitos de corrente alternada · 6.14 Magnetismo na matéria (introdutório) · 7.13 Sólidos e semicondutores · 8.13 Aproximação linear, diferenciais e método de Newton · 9.12 Integração numérica · 10.11 Funções vetoriais e curvas no espaço · 11.12 Operadores em coordenadas curvilíneas e laplaciano · EM 1.1 a EM 12.3 e EM A–C · 13.1–13.9 · 14.1–14.9 · 15.1–15.6.

**Nome alterado:** 4.5 "Atrito" virou "Atrito e arrasto" (entraram o arrasto e a velocidade terminal).

**Tópicos novos dentro de módulos antigos:** marcados *(novo)* ao longo do texto.

## Anexo D — Decisões de adoção (2026-10-27)

O Kaio aprovou a v2 em 2026-10-27. Ficou decidido:

1. **Campos da ficha.** `disciplina:`, `bloco:`, `modulo:` (ID e nome deste mapa) e `referencia:` substituem o `macroassunto:` de valores fixos. Os longos usam os quatro; os curtos, pelo menos `disciplina:` e `modulo:`. Atualizados `docs/formatos.md` e o §6 do `padrao_video_longo.md`. Fichas antigas não são reescritas.
2. **Bloco de 4.9–4.10:** "Momento e colisões". A pasta já entregue do `yt_0013` (`Mecânica - Colisões - Colisões em 1D`) não é renomeada.
3. **Playlists:** uma por bloco, juntando Física III e EM na ordem da grade, com um endereço principal por vídeo e entrada em mais de uma playlist quando servir (§0.3).
4. **Anexo A:** fica dentro do mapa, como retrato datado. Atualizar quando for útil, não a cada vídeo.
5. **Referências:** Física I–IV usam Moysés Nussenzveig e Sears (Young & Freedman), pelas aplicações e problemas; o Halliday sai como referência. Feynman (*Lições de Física*) é consulta teórica e discursiva em todas as Físicas e no EM. EM = Griffiths, 4ª ed.
6. **`yt_0007`:** é de 4.13 Gravitação ("Por que uma órbita é uma queda que nunca termina?"), em preview.
7. **Duração dos longos:** `formatos.md` passa a registrar a duração observada (12–27 min); a duração sai da explicação.
8. **Adoção:** a v2 substitui `docs/mapa_curricular.md`; a v1 fica em `docs/mapa_curricular_old.md`; a decisão entra em `docs/decisoes.md`; o `cobertura.md` do arsenal ganhou a coluna com o módulo equivalente do EM.

Em aberto:

- terminar o `yt_0007` (4.13 Gravitação, em preview);
- se a Mecânica Clássica intermediária (§16) ganha livro fixo.
