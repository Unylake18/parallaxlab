# Cobertura do arsenal 3D por capítulo do mapa curricular

> Arquivo **gerado** por `gerar_cobertura.py`. O status vem das fichas (`solidos/*.json`); as lacunas são mantidas no script.
> Total: **58 sólidos** (57 aprovado, 1 estudo); **39** têm animação (loop ou ciclo único). Fonte dos capítulos: `docs/mapa_curricular.md`.

## 1. O que temos, por assunto do curso

| Capítulo | Assunto | Sólidos (status, animação) | Observação |
|---|---|---|---|
| 4.7–4.8 | Energia potencial e conservação | `paisagem_potencial` (aprovado, anima) |  |
| 4.9–4.10 | Momento linear e colisões | `colisao_1d` (aprovado, anima) | só 1D |
| 4.11 | Rotação de corpos rígidos | `giroscopio_precessao` (aprovado, anima), `anel_carregado` (aprovado, anima), `disco_carregado` (aprovado, anima), `haste_carregada` (aprovado, anima) | anel, disco e haste com `com_cargas=0` e `eixo=1` servem ao momento de inércia |
| 4.12 | Rolamento | `esfera_rolando` (aprovado, anima), `cilindro_rolando` (aprovado, anima), `aro_rolando` (aprovado, anima) | só em chão plano |
| 4.13 | Gravitação | `orbita_kepleriana` (aprovado, anima), `poco_gravitacional` (aprovado, anima) |  |
| 5.1 | Movimento harmônico simples | `massa_mola` (aprovado, anima), `pendulo_simples` (aprovado, anima) |  |
| 5.3–5.4 | Ondas mecânicas, superposição e estacionárias | `onda_corda` (aprovado, anima), `ondas_duas_fontes` (aprovado, anima) |  |
| 5.7 | Fluidos em movimento | `tubo_escoamento` (aprovado, anima) | continuidade |
| 5.8–5.10 | Teoria cinética e gases ideais | `caixa_gas_cinetica` (aprovado, anima) | êmbolo oscilante |
| 6.2 | Campo elétrico (distribuições contínuas) | `anel_carregado` (aprovado, anima), `disco_carregado` (aprovado, anima), `haste_carregada` (aprovado, anima), `campo_vetorial` (aprovado) |  |
| 6.3 | Lei de Gauss | `casca_cilindrica_oca` (aprovado), `cilindro_macico_isolante` (aprovado), `casca_esferica_oca` (aprovado), `esfera_macica_isolante` (aprovado), `placa_infinita_carregada` (aprovado, anima), `cilindro_coaxial` (aprovado), `gaussiana_esferica` (aprovado), `gaussiana_cilindrica` (aprovado), `gaussiana_caixa` (aprovado) |  |
| 6.4 | Potencial elétrico | `equipotenciais` (aprovado), `gradiente_colina` (aprovado, anima) | o gradiente é o de uma colina genérica |
| 6.5 | Condutores e capacitores | `capacitor_placas_paralelas` (aprovado), `capacitor_esferico` (aprovado), `cilindro_coaxial` (aprovado) |  |
| 6.7 | Força magnética | `particula_em_campo_magnetico` (aprovado, anima), `espira_em_campo_magnetico` (aprovado, anima) |  |
| 6.8 | Biot–Savart | `biot_savart_espira` (aprovado, anima) |  |
| 6.9 | Lei de Ampère | `fio_infinito` (aprovado, anima), `solenoide_corrente` (aprovado, anima), `toroide_corrente` (aprovado, anima), `amperiano_circular` (aprovado), `amperiano_retangular` (aprovado) |  |
| 6.10 | Indução eletromagnética | `ima_espira_inducao` (estudo, anima), `barra_trilhos_fem_movimento` (aprovado, anima) |  |
| 6.12 e 7.1 | Maxwell e ondas eletromagnéticas | `onda_eletromagnetica` (aprovado, anima) |  |
| 7.2 | Óptica geométrica | `lente_delgada` (aprovado), `prisma_triangular` (aprovado) |  |
| 7.3–7.4 | Interferência e difração | `anteparo_fenda_dupla` (aprovado), `ondas_duas_fontes` (aprovado, anima) | só fenda dupla |
| 7.6 | Relatividade especial | `cone_de_luz` (aprovado, anima) |  |
| 7.11 | Estrutura atômica | `orbital_atomico` (aprovado, anima) | só 1s, 2s, 2p, 3d |
| 8.12 e 9.5 | Volumes de revolução | `solido_revolucao_disco` (aprovado, anima), `solido_revolucao_arruela` (aprovado, anima), `solido_revolucao_cascas` (aprovado, anima) |  |
| 10.1 | Geometria e vetores em R³ | `produto_vetorial` (aprovado, anima), `superficie_quadrica` (aprovado) |  |
| 10.3 | Derivadas parciais e plano tangente | `plano_tangente` (aprovado, anima) |  |
| 10.5 | Gradiente | `gradiente_colina` (aprovado, anima) |  |
| 10.6 | Extremos em várias variáveis | `pontos_criticos` (aprovado) |  |
| 10.7 | Integrais duplas | `integral_dupla_colunas` (aprovado, anima) |  |
| 10.8–10.9 | Integrais triplas e Jacobiano | `elemento_volume` (aprovado, anima) |  |
| 11.1 e 11.8 | Campos vetoriais, divergência e rotacional | `campo_vetorial` (aprovado) | a divergência e o rotacional locais ainda se leem só pela forma |
| 11.6–11.7 | Superfícies parametrizadas e integrais de superfície | `superficie_parametrizada` (aprovado, anima), `gaussiana_esferica` (aprovado), `gaussiana_cilindrica` (aprovado), `gaussiana_caixa` (aprovado) |  |
| 11.9 | Teorema de Stokes | `teorema_stokes` (aprovado, anima) |  |
| 11.10 | Teorema da divergência de Gauss | `gaussiana_esferica` (aprovado), `gaussiana_cilindrica` (aprovado), `gaussiana_caixa` (aprovado) |  |

Todos os sólidos aparecem em pelo menos um capítulo.

## 2. O que não temos, com o assunto e a limitação

### 2a. Poderiam ser sólidos 3D (22 lacunas)

| Capítulo | Assunto | Sólido sugerido | Limitação / por que ainda não |
|---|---|---|---|
| 4.4–4.5 | Plano inclinado, atrito, polias e diagramas de corpo livre | `plano_inclinado` | o plano inclinado e o bloco cabem em 3D, mas o diagrama de forças é plano: o ganho do 3D é pequeno |
| 4.6 | Movimento circular e curva inclinada | `movimento_circular, curva_inclinada` | a curva inclinada precisa de um carro e de uma pista; os vetores a_c e v são do Manim |
| 4.10 | Colisões em 2D e explosões | `colisao_2d, explosao` | o movimento é no plano: a vista de cima já resolve em 2D |
| 4.12 | Rolamento em rampas e looping | `rampa_rolamento, trilho_looping` | câmera acompanhando o corpo não serve para rampa; exige compor no Manim |
| 5.6 | Fluidos em repouso: pressão, Pascal e empuxo | `tanque_hidrostatico, prensa_hidraulica` | o líquido translúcido sobrepõe vidros e fica difícil de ler; o empuxo é mais claro em corte 2D |
| 5.7 | Torricelli e Bernoulli com manômetros | `tanque_torricelli` | o jato é uma parábola plana |
| 6.1 | Lei de Coulomb (cargas pontuais e forças) | `cargas_pontuais, dipolo_eletrico` | o sinal esculpido já existe (`carga_sinal`), falta só montar o sólido e as setas de força |
| 6.2 | Linhas de campo em 3D | `linhas_de_campo_3d` | linhas de campo contínuas com setas exigem integração numérica e muitas curvas: o `campo_vetorial` cobre a leitura básica |
| 6.5 | Condutor com cavidade e cargas induzidas | `condutor_com_cavidade` | a carga induzida precisa de sinais nas duas faces; usa `carga_sinal` em escala pequena |
| 7.2 | Espelhos e refração (Snell, reflexão interna) | `espelho_esferico, dioptro_plano` | os raios são do Manim: o sólido só dá o espelho ou o bloco de vidro |
| 7.3–7.4 | Filme fino, Michelson e redes de difração | `filme_fino, interferometro_michelson, rede_de_difracao` | a rede é uma generalização do `anteparo_fenda_dupla` para N fendas |
| 7.5 | Polarização e lei de Malus | `polarizador_malus` | precisa de uma convenção de cor para a polarização |
| 7.6 | Relógio de luz e dilatação do tempo | `relogio_de_luz` | o diagrama espaço-tempo e as transformações de Lorentz são 2D |
| 7.11 | Modelo de Bohr e níveis de energia | `atomo_bohr` | os níveis e os saltos são melhor num diagrama de energia |
| 10.1 | Retas e planos em R³ (distâncias) | `plano_e_reta_r3` | o produto vetorial e o plano tangente cobrem boa parte |
| 10.6 | Multiplicadores de Lagrange | `lagrange_restricao` | a leitura é melhor com curvas de nível em 2D |
| 10.10 | Centro de massa e momentos em 3D | `—` | reutiliza os sólidos de revolução e `elemento_volume`; não há um sólido dedicado |
| 11.2–11.3 | Integrais de linha (trabalho e circulação) | `integral_de_linha` | o trabalho é uma soma ao longo da curva: a curva em 3D com o campo ajuda, mas é mais simples em 2D |
| 11.4 | Campos conservativos e potencial | `—` | `gradiente_colina` mostra o potencial; o teste de conservatividade é do Manim |
| 11.8 | Divergência e rotacional locais (cubo elementar, roda de pás) | `divergencia_local, rotacional_roda_de_pas` | a roda de pás precisa de uma animação de rotação no campo |
| 13 | Álgebra linear (transformações, autovetores) | `transformacao_linear_3d, autovetores_elipsoide` | futuro: a maior parte é em 2D e em matrizes |
| 15 | Equações diferenciais parciais (modos de uma membrana) | `membrana_modos` | futuro |

### 2b. Melhor no Manim, sem sólido 3D (12 blocos)

| Capítulo | Assunto | Motivo |
|---|---|---|
| 5.2 | Oscilações amortecidas e forçadas | o essencial é o gráfico x(t) e o plano de fase |
| 5.5 | Som (pressão, Doppler, batimentos) | ondas longitudinais e figuras de pressão pedem 2D (cortes) e animação de frentes |
| 5.11–5.12 | Entropia, máquinas térmicas, condução e radiação | dependem de uma escala de cor de temperatura (não definida no padrão) e de diagramas planos |
| 6.6 | Circuitos DC, RC e Kirchhoff | esquemas elétricos são diagramas planos |
| 6.11 | Indutância, RL, LC e RLC | circuitos e gráficos de oscilação |
| 7.7–7.10 | Corpo negro, fótons, ondas de matéria e Schrödinger | gráficos e funções de onda 1D |
| 7.12 | Física nuclear e partículas | decaimento exponencial e panorama de partículas |
| 8.1–8.11, 9.1–9.4, 9.8–9.11 | Funções, limites, derivadas, integrais, séries e Taylor | são curvas e equações em 2D |
| 9.6–9.7 | Curvas paramétricas e polares | planas: o sólido de revolução cobre a parte 3D (9.5) |
| 10.4 | Regra da cadeia multivariável | é uma fórmula com diagrama de dependências |
| 11.5 | Teorema de Green | região plana e contorno (o `teorema_stokes` é o análogo 3D) |
| 14 | Equações diferenciais ordinárias e planos de fase | campos de direção e retratos de fase em 2D |

## 3. Limitações que valem para todo o arsenal

- **Só o objeto**: fórmulas, valores, gráficos, rótulos (N/S, +/−, nomes de vetores) e raios são do Manim.
- **Cor**: segue `estilo.json` (E = ciano, B = magenta, vetores físicos = branco, normal = azul, construções = violeta).
- **Uso em vídeo**: nenhum sólido foi usado em vídeo real ainda; usar um exige handoff (ver `AGENTS.md`).
- **Movimento**: calculado por fórmula (didático), não uma simulação física; os loops fecham sem emenda, os de ciclo único (colisão, partícula em B, ímã, cone de luz, soma de Riemann) não.
- **Custo**: de 0,4 a 1,7 s por quadro em 1080p com alpha; frames ficam fora do Git (`renders/arsenal3d/`).
