# Arsenal 3D — índice enxuto para briefings

> Arquivo **gerado** por `gerar_indice.py` (não editar à mão). **90 sólidos**, todos `aprovado`
> (0 em outro status); versão completa em `catalogo.md`, cobertura em `cobertura.md`.

## Como usar num briefing

- Preencha `solido_3d:` com um `id` desta lista ou `nenhum` + motivo, e diga **o que o 3D deve mostrar e em que ponto do storyboard entra**.
- O 3D só dá a **geometria**: valores, fórmulas, rótulos, sinais e setas de sentido são do Manim. Gramática de cor fixa: campo elétrico = ciano,
  campo magnético = magenta, vetores físicos = branco, construções matemáticas = violeta tracejado, superfícies/corpos = vidro azul.
- Movimento: **loop** = fase 0–1 se repete sem emenda; **único** = ciclo que termina num estado diferente (congela no fim); **—** = estático.
- Cada sólido tem parâmetros (tamanho, quantidade, estado) na ficha `solidos/<id>.json`; quem implementa vê o sólido com `abrir/<id>.bat`.
- Um sólido só entra num vídeo com `solido_3d:` no briefing; quem implementa avalia o encaixe e devolve o relatório "Teste do arsenal" (`docs/formatos.md`).

## Sólidos por capítulo do mapa curricular

### 4.4–4.5 — Plano inclinado (o diagrama de forças é do Manim)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `plano_inclinado` | Um bloco numa rampa com três setas brancas e duas linhas tracejadas | único | polias e sistemas conectados (só um bloco) |

### 4.6 — Movimento circular e curva inclinada

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `movimento_circular` | Uma bola girando com uma seta tangente e uma seta para o centro | loop | movimento circular não uniforme (a velocidade aqui é constante) |
| `curva_inclinada` | Um carro numa pista inclinada com três setas brancas | loop | curvas com atrito estático (este modelo é sem atrito) |

### 4.7–4.8 — Energia potencial e conservação

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `paisagem_potencial` | Bola descendo e subindo numa pista em forma de poço duplo, com a reta da energia total | loop | potenciais dependentes do tempo |

### 4.9–4.10 — Momento linear e colisões (1D, 2D e explosão)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `colisao_1d` | Dois blocos se aproximam, colidem e se afastam (ou seguem juntos) | único | colisões em duas dimensões |
| `colisao_2d` | Dois discos que se afastam em ângulo depois do choque, com o centro de massa seguindo em linha reta | único | colisões 1D (use colisao_1d) |
| `explosao` | Uma esfera que vira três esferas se afastando em direções opostas, com o centro de massa seguindo reto | único | fragmentos com direções arbitrárias (aqui são três, a 120°) |

### 4.11 — Rotação de corpos rígidos (anel, disco e haste com `com_cargas=0` e `eixo=1` servem ao momento de inércia)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `giroscopio_precessao` | Pião inclinado com um rastro circular tracejado e três setas brancas | loop | nutação e movimento geral do pião (só precessão estacionária) |
| `anel_carregado` | Aro de vidro fino com pontos azuis alinhados e, opcionalmente, o eixo tracejado atravessando o centro | loop | a carga está numa superfície (use disco_carregado) ou numa linha reta (use… |
| `disco_carregado` | Disco translúcido de borda luminosa, cheio de pontos uniformes e, opcionalmente, o eixo tracejado atravessando o centro | loop | o ponto do vídeo é um plano ilimitado sem borda (use placa_infinita_carregada) |
| `haste_carregada` | Bastão de vidro fino com uma fileira de pontos azuis e, opcionalmente, o eixo tracejado cruzando-o ao meio | loop | a haste deve ser infinita |

### 4.12 — Rolamento (chão plano, rampa e looping)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `esfera_rolando` | Esfera de vidro girando parada no centro, com riscos que mostram a rotação e um ponto de superfície que descreve uma ciclóide | loop | o corpo desliza (rolamento com escorregamento) |
| `cilindro_rolando` | Tambor de vidro girando parado no centro, com geratrizes e uma marca na borda que mostram a rotação | loop | o corpo desliza (rolamento com escorregamento) |
| `aro_rolando` | Aro girando parado no centro, com 3 marcas que mostram a rotação sem rótulo | loop | o corpo desliza (rolamento com escorregamento) |
| `rampa_rolamento` | Três corpos descendo lado a lado, a esfera na frente e o aro atrás | único | rolamento em chão plano (use esfera_rolando e companhia) |
| `trilho_looping` | Uma bola descendo uma rampa, subindo o laço e saindo | único | rolamento com rotação (a bola aqui desliza sem atrito) |

### 4.13 — Gravitação

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `orbita_kepleriana` | Elipse tracejada com o corpo central num foco e fatias violeta | loop | problemas de dois corpos com massas comparáveis (o centro é fixo) |
| `poco_gravitacional` | Funil de vidro com grade e uma bola circulando | loop | curvatura do espaço-tempo da relatividade geral (é só uma analogia de potencial) |

### 5.1 — Movimento harmônico simples

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `massa_mola` | Bloco entre duas marcas pontilhadas, com a mola mudando de comprimento | loop | movimento vertical com gravidade (a mola é horizontal, sem atrito) |
| `pendulo_simples` | Massa balançando num fio, com o arco pontilhado do percurso e a vertical | loop | grandes amplitudes (o movimento real não é senoidal) |

### 5.3–5.4 — Ondas mecânicas, superposição e estacionárias

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `onda_corda` | Onda com contas brancas que oscilam na vertical enquanto a forma anda (progressiva) ou fica parada com nós (estacionária) | loop | ondas longitudinais (som) |
| `ondas_duas_fontes` | Superfície ondulada com dois pontos brancos e um padrão de cristas e vales cruzados | loop | uma única fonte ou ondas estacionárias (use onda_corda) |

### 5.6 — Fluidos em repouso (pressão, empuxo e Pascal)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `tanque_hidrostatico` | Um bloco boiando num tanque, com setas de pressão que crescem para baixo e duas setas verticais iguais | loop | fluidos em movimento (use tubo_escoamento ou tanque_torricelli) |
| `prensa_hidraulica` | Um êmbolo pequeno descendo muito e um grande subindo pouco, com uma seta pequena e uma grande | loop | fluidos em movimento |

### 5.7 — Fluidos em movimento (continuidade e Torricelli)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `tubo_escoamento` | Tubo com um gargalo e pontos que aceleram ao passar por ele e ficam mais espaçados | loop | escoamento turbulento ou viscoso (o campo de velocidades é uniforme na seção) |
| `tanque_torricelli` | Um tanque com um jato curvo saindo de um furo, marcado por pontos | loop | tanques que esvaziam (o nível é constante aqui) |

### 5.8–5.10 — Teoria cinética e gases ideais (êmbolo oscilante)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `caixa_gas_cinetica` | Caixa de vidro com um êmbolo e pontos brancos em movimento | loop | o ponto é o gráfico P×V (é do Manim |

### 6.1 — Lei de Coulomb

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `cargas_pontuais` | Esferas com + e −, com setas entre as cargas de sinais opostos (atração) ou afastando as de sinais iguais (repulsão) | loop | campos e potenciais de distribuições contínuas |
| `dipolo_eletrico` | Um par + e − com setas ciano saindo de uma e chegando na outra, desenhando o padrão do dipolo | loop | distribuições contínuas (use anel, disco e haste) |

### 6.2 — Campo elétrico (distribuições contínuas)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `anel_carregado` | (ver acima) | loop | |
| `disco_carregado` | (ver acima) | loop | |
| `haste_carregada` | (ver acima) | loop | |
| `campo_vetorial` | Grade de setas ciano | — | campos que variam no tempo ou com singularidades (o preview não evita o centro) |
| `dipolo_eletrico` | (ver acima) | loop | |
| `linhas_de_campo_3d` | Um feixe de curvas ciano que sai de uma esfera + e se fecha na esfera −, com setinhas | loop | campos de distribuições contínuas |

### 6.3 — Lei de Gauss

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `casca_cilindrica_oca` | Aro claro (#7FB2FF) marca a parede fina | — | precisa mostrar cargas individuais no volume (use cilindro_macico_isolante) |
| `cilindro_macico_isolante` | Vidro translúcido de borda luminosa cheio de pontos | — | o material só existe na superfície (use casca_cilindrica_oca) |
| `casca_esferica_oca` | Exterior azul (#267BFF) opaco | — | precisa mostrar cargas individuais no volume (use esfera_macica_isolante) |
| `esfera_macica_isolante` | Vidro translúcido de borda luminosa cheio de pontos | — | o material só existe na superfície (use casca_esferica_oca) |
| `placa_infinita_carregada` | Plano azul translúcido de grade discreta, cheio de pontos e sumindo nas bordas | loop | o vídeo precisa mostrar as bordas ou efeitos de borda |
| `cilindro_coaxial` | Casca azul opaca aberta, com aro claro (#7FB2FF) marcando a parede e o corte | — | o interno é isolante com carga em volume (use cilindro_macico_isolante) |
| `gaussiana_esferica` | Três círculos violeta tracejados sobre uma esfera quase transparente, envolvendo a fonte azul | — | simetria cilíndrica ou planar (use gaussiana_cilindrica ou gaussiana_caixa) |
| `gaussiana_cilindrica` | Cilindro de traços violeta sobre a fonte azul | — | simetria esférica ou planar (use gaussiana_esferica ou gaussiana_caixa) |
| `gaussiana_caixa` | Caixa de arestas violeta tracejadas atravessando o plano azul | — | simetria esférica ou cilíndrica (use gaussiana_esferica ou gaussiana_cilindrica) |

### 6.4 — Potencial elétrico (o gradiente é o de uma colina genérica)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `equipotenciais` | Cascas violeta aninhadas em torno de uma esfera com + ou − | — | potenciais de distribuições contínuas (use as fontes do arsenal e o Manim) |
| `gradiente_colina` | Colina de vidro com anéis e um ponto com uma seta ciano perpendicular ao anel, apontando para o topo | loop | funções com pontos de sela (use superficie_parametrizada, tipo sela) |

### 6.5 — Condutores e capacitores

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `capacitor_placas_paralelas` | Duas folhas de vidro paralelas com pontos azuis voltados um para o outro | — | o ponto é o plano infinito sem borda (use placa_infinita_carregada) |
| `capacitor_esferico` | Esfera de vidro com pontos azuis dentro de uma casca azul aberta em corte, também com pontos na face interna | — | isolante com carga em volume (use esfera_macica_isolante) |
| `cilindro_coaxial` | (ver acima) | — | |
| `condutor_com_cavidade` | Uma esfera aberta com um + no centro, vários − dentro da parede da cavidade e vários + por fora | — | cavidades não concêntricas (o arranjo uniforme da carga induzida seria distorcido) |

### 6.7 — Força magnética

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `particula_em_campo_magnetico` | Uma esfera com + ou − girando numa hélice no meio de setas magenta | único | campo elétrico junto (E × B) |
| `espira_em_campo_magnetico` | Uma espira circular inclinada em relação às setas magenta, com uma seta normal e uma seta de torque | loop | campos não uniformes (há força líquida) |

### 6.8 — Biot–Savart

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `biot_savart_espira` | Anel com uma seta branca no fio e uma seta magenta em P | loop | campos de fios retos ou arcos (a geometria é outra) |

### 6.9 — Lei de Ampère

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `fio_infinito` | Linha azul luminosa com halo suave que some nas pontas | loop | o fio é finito e o efeito de pontas importa |
| `solenoide_corrente` | Hélice azul luminosa de espiras abertas em volta de um núcleo de vidro translúcido | loop | o enrolamento é fechado em anel (use toroide_corrente) |
| `toroide_corrente` | Anel formado por espiras azuis apertadas, com o buraco central visível | loop | enrolamento reto (use solenoide_corrente) |
| `amperiano_circular` | Círculo tracejado violeta em torno do fio azul | — | o contorno atravessa a parede de um solenoide (use amperiano_retangular) |
| `amperiano_retangular` | Retângulo tracejado violeta atravessando a parede do solenoide | — | fio ou toroide (use amperiano_circular) |

### 6.10 — Indução eletromagnética

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `ima_espira_inducao` | Uma barra bicolor passando por um anel | único | ímã que gira ou espiras que se movem (use barra_trilhos_fem_movimento) |
| `barra_trilhos_fem_movimento` | Um retângulo violeta que cresce e encolhe com uma barra, e setinhas que giram e invertem | loop | campos não uniformes ou barras que giram |

### 6.12 e 7.1 — Maxwell e ondas eletromagnéticas

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `onda_eletromagnetica` | Dois campos perpendiculares oscilando juntos ao longo de um eixo | loop | ondas circularmente polarizadas ou com atrasos de fase |

### 7.2 — Óptica geométrica (os raios são do Manim)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `lente_delgada` | Lente de vidro com o eixo tracejado e duas marcas nos focos | — | lentes espessas ou aberração (esta é delgada, de faces esféricas ideais) |
| `prisma_triangular` | Prisma de vidro com arestas claras | — | lentes (use lente_delgada) |
| `espelho_esferico` | Uma calota curva com um eixo tracejado e três pontos sobre ele | — | lentes (o vidro daqui não é lente) |
| `dioptro_plano` | Um raio chegando numa fronteira, um refletido e outro que muda de direção ao entrar no vidro (ou some, na reflexão total) | loop | lentes e prismas (a geometria é uma fronteira plana) |

### 7.3–7.4 — Interferência e difração (fenda dupla, N fendas, filme fino e Michelson)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `anteparo_fenda_dupla` | Placa azul com duas frestas escuras e bordas claras | — | redes de difração com muitas fendas |
| `ondas_duas_fontes` | (ver acima) | loop | |
| `rede_de_difracao` | Uma placa com várias frestas verticais regularmente espaçadas | — | fenda simples (use n_fendas = 1) |
| `filme_fino` | Um raio se dividindo em dois ao bater numa película, e uma esfera que acende e apaga | loop | interferência de fendas (use anteparo_fenda_dupla ou rede_de_difracao) |
| `interferometro_michelson` | Uma cruz de feixes com um espelho em cada ponta e um disco no fim que acende e apaga | loop | difração e fendas |

### 7.5 — Polarização e lei de Malus

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `polarizador_malus` | Setas ciano em várias direções entrando num disco, uma seta vertical saindo, e depois uma segunda que diminui conforme o segundo disco gira | loop | polarização circular ou elíptica |

### 7.6 — Relatividade especial

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `cone_de_luz` | Dois cones, uma curva dentro deles e um disco violeta que corta o cone num círculo | único | transformações de Lorentz e diagramas 1+1 (são melhores em 2D) |
| `relogio_de_luz` | Um fóton subindo na diagonal entre dois espelhos que andam para a direita, com um triângulo tracejado | único | contração do comprimento |

### 7.11 — Estrutura atômica (orbitais 1s, 2s, 2p, 3d e o modelo de Bohr)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `orbital_atomico` | Uma nuvem de pontos com forma característica | loop | energia dos níveis e espectros (são do Manim) |
| `atomo_bohr` | Órbitas concêntricas tracejadas, um ponto que muda de órbita e um pequeno pulso ondulado que sai | único | orbitais e a nuvem de probabilidade (use orbital_atomico) |

### 8.12 e 9.5 — Volumes de revolução

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `solido_revolucao_disco` | Corpo de vidro azul atravessado por um disco violeta de arestas tracejadas | loop | a região é limitada por duas curvas (use solido_revolucao_arruela) |
| `solido_revolucao_arruela` | Corpo de vidro azul em forma de taça aberta, com uma arruela violeta de arestas tracejadas | loop | a região vai até o eixo (use solido_revolucao_disco) |
| `solido_revolucao_cascas` | Tigela de vidro azul com uma casca cilíndrica violeta de arestas tracejadas, concêntrica ao eixo vertical | loop | rotação em torno do eixo x com a região sob a curva (use solido_revolucao_disco) |

### 10.1 — Geometria e vetores em R³

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `produto_vetorial` | Dois vetores brancos, um paralelogramo violeta e uma seta azul perpendicular | loop | produto escalar e projeções |
| `superficie_quadrica` | Superfície de vidro com a malha | — | superfícies que não são quádricas |
| `plano_e_reta_r3` | Uma folha inclinada com uma seta azul perpendicular, uma reta que a fura e um ponto com um fio tracejado até ela | loop | planos tangentes a superfícies (use plano_tangente) |

### 10.3 — Derivadas parciais e plano tangente

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `plano_tangente` | Superfície com um quadrilátero violeta encostado e uma seta azul perpendicular | loop | tangente a curvas (use as curvas do Manim) |

### 10.5 — Gradiente

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `gradiente_colina` | (ver acima) | loop | |

### 10.6 — Extremos em várias variáveis

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `pontos_criticos` | Superfície ondulada com três planos horizontais violeta encostados | — | máximos com restrição (use lagrange quando existir) |
| `lagrange_restricao` | Uma superfície ondulada, um círculo tracejado no piso e a curva na superfície, com um ponto que gira e duas setas que ora divergem ora se alinham | loop | restrições múltiplas |

### 10.7 — Integrais duplas

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `integral_dupla_colunas` | Um bloco de colunas que fica cada vez mais fino e se ajusta à superfície | único | regiões não retangulares |

### 10.8–10.9 — Integrais triplas e Jacobiano

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `elemento_volume` | Uma pequena cunha violeta flutuando perto da origem, com as guias tracejadas até ela | loop | integrais de superfície (use superficie_parametrizada) |

### 10.10 — Centro de massa e momentos em 3D (hemisfério, cone, parabolóide e halteres)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `centro_de_massa_3d` | Um corpo transparente com um ponto branco no eixo e um disco violeta que o percorre de baixo para cima | loop | corpos sem simetria de revolução (o centroide fora do eixo) |

### 11.1 e 11.8 — Campos vetoriais, divergência e rotacional

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `campo_vetorial` | (ver acima) | — | |
| `divergencia_local` | Uma caixinha violeta num campo de setas ciano, com uma seta saindo de cada face | loop | a definição formal de limite (o cubo é de tamanho fixo) |
| `rotacional_roda_de_pas` | Uma cruz azul no centro de um redemoinho de setas ciano, girando com ele (ou parada, se não há rotação) | loop | rotacional em 3D com os três componentes (o campo é plano) |

### 11.2–11.3 — Integrais de linha

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `integral_de_linha` | Um redemoinho de setas ciano com uma espiral que sobe, um ponto que a percorre e duas setas (dr e F) sobre ele | único | integrais de linha de funções escalares |

### 11.4 — Campos conservativos e potencial (φ fixa (colina gaussiana))

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `campo_conservativo` | Uma colina com duas trilhas diferentes ligando os mesmos pontos, e pontos que chegam juntos | único | testar conservatividade com ∂F/∂y = ∂F/∂x (é do Manim) |
| `gradiente_colina` | (ver acima) | loop | |

### 11.6–11.7 — Superfícies parametrizadas e integrais de superfície

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `superficie_parametrizada` | Superfície de vidro com malha, um quadrilátero violeta e três setas (duas brancas no plano tangente, uma azul normal) | loop | superfícies de revolução com fatias (use solido_revolucao_*) |
| `gaussiana_esferica` | (ver acima) | — | |
| `gaussiana_cilindrica` | (ver acima) | — | |
| `gaussiana_caixa` | (ver acima) | — | |

### 13 — Álgebra linear

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `transformacao_linear_3d` | Uma caixa que se deforma a partir de uma caixa tracejada, com três setas brancas nas arestas | loop | transformações afins (a origem é fixa) |
| `autovetores_elipsoide` | Uma esfera tracejada que se estica num elipsoide inclinado, com três setas brancas ao longo dos eixos | loop | matrizes não simétricas (eixos oblíquos ou complexos) |

### 15 — Equações diferenciais parciais (um modo por vez)

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `membrana_modos` | Uma folha azul presa numa moldura, ondulando em cristas e vales separados por linhas tracejadas | loop | membranas circulares (modos de Bessel) |

### 11.9 — Teorema de Stokes

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `teorema_stokes` | Cúpula de vidro com anel violeta na base, normais azuis para fora e setas ciano girando | loop | superfícies fechadas (use o teorema da divergência com as gaussianas) |

### 11.10 — Teorema da divergência de Gauss

| id | mostra | mov. | não usar quando |
|---|---|---|---|
| `gaussiana_esferica` | (ver acima) | — | |
| `gaussiana_cilindrica` | (ver acima) | — | |
| `gaussiana_caixa` | (ver acima) | — | |

## Sem sólido 3D (melhor no Manim)

- **4.4–4.5** Polias, atrito e máquina de Atwood: o essencial são os diagramas de corpo livre e as equações: o 3D acrescenta pouco
- **5.2** Oscilações amortecidas e forçadas: o essencial é o gráfico x(t) e o plano de fase
- **5.5** Som (pressão, Doppler, batimentos): ondas longitudinais e figuras de pressão pedem 2D (cortes) e animação de frentes
- **5.11–5.12** Entropia, máquinas térmicas, condução e radiação: dependem de uma escala de cor de temperatura (não definida no padrão) e de diagramas planos
- **6.6** Circuitos DC, RC e Kirchhoff: esquemas elétricos são diagramas planos
- **6.11** Indutância, RL, LC e RLC: circuitos e gráficos de oscilação
- **7.7–7.10** Corpo negro, fótons, ondas de matéria e Schrödinger: gráficos e funções de onda 1D
- **7.12** Física nuclear e partículas: decaimento exponencial e panorama de partículas
- **8.1–8.11, 9.1–9.4, 9.8–9.11** Funções, limites, derivadas, integrais, séries e Taylor: são curvas e equações em 2D
- **9.6–9.7** Curvas paramétricas e polares: planas: o sólido de revolução cobre a parte 3D (9.5)
- **10.4** Regra da cadeia multivariável: é uma fórmula com diagrama de dependências
- **11.5** Teorema de Green: região plana e contorno (o `teorema_stokes` é o análogo 3D)
- **14** Equações diferenciais ordinárias e planos de fase: campos de direção e retratos de fase em 2D
