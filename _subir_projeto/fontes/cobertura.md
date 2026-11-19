# Cobertura do arsenal 3D por capítulo do mapa curricular

> Arquivo **gerado** por `gerar_cobertura.py`. O status vem das fichas (`solidos/*.json`); as lacunas são mantidas no script.
> Total: **90 sólidos** (90 aprovado); **68** têm animação (loop ou ciclo único). Fonte dos capítulos: `docs/mapa_curricular.md`.

## 1. O que temos, por assunto do curso

| Capítulo | Assunto | Sólidos (status, animação) | Observação |
|---|---|---|---|
| 4.4–4.5 | Plano inclinado | `plano_inclinado` (aprovado, anima) | o diagrama de forças é do Manim |
| 4.6 | Movimento circular e curva inclinada | `movimento_circular` (aprovado, anima), `curva_inclinada` (aprovado, anima) |  |
| 4.7–4.8 | Energia potencial e conservação | `paisagem_potencial` (aprovado, anima) |  |
| 4.9–4.10 | Momento linear e colisões | `colisao_1d` (aprovado, anima), `colisao_2d` (aprovado, anima), `explosao` (aprovado, anima) | 1D, 2D e explosão |
| 4.11 | Rotação de corpos rígidos | `giroscopio_precessao` (aprovado, anima), `anel_carregado` (aprovado, anima), `disco_carregado` (aprovado, anima), `haste_carregada` (aprovado, anima) | anel, disco e haste com `com_cargas=0` e `eixo=1` servem ao momento de inércia |
| 4.12 | Rolamento | `esfera_rolando` (aprovado, anima), `cilindro_rolando` (aprovado, anima), `aro_rolando` (aprovado, anima), `rampa_rolamento` (aprovado, anima), `trilho_looping` (aprovado, anima) | chão plano, rampa e looping |
| 4.13 | Gravitação | `orbita_kepleriana` (aprovado, anima), `poco_gravitacional` (aprovado, anima) |  |
| 5.1 | Movimento harmônico simples | `massa_mola` (aprovado, anima), `pendulo_simples` (aprovado, anima) |  |
| 5.3–5.4 | Ondas mecânicas, superposição e estacionárias | `onda_corda` (aprovado, anima), `ondas_duas_fontes` (aprovado, anima) |  |
| 5.6 | Fluidos em repouso | `tanque_hidrostatico` (aprovado, anima), `prensa_hidraulica` (aprovado, anima) | pressão, empuxo e Pascal |
| 5.7 | Fluidos em movimento | `tubo_escoamento` (aprovado, anima), `tanque_torricelli` (aprovado, anima) | continuidade e Torricelli |
| 5.8–5.10 | Teoria cinética e gases ideais | `caixa_gas_cinetica` (aprovado, anima) | êmbolo oscilante |
| 6.1 | Lei de Coulomb | `cargas_pontuais` (aprovado, anima), `dipolo_eletrico` (aprovado, anima) |  |
| 6.2 | Campo elétrico (distribuições contínuas) | `anel_carregado` (aprovado, anima), `disco_carregado` (aprovado, anima), `haste_carregada` (aprovado, anima), `campo_vetorial` (aprovado), `dipolo_eletrico` (aprovado, anima), `linhas_de_campo_3d` (aprovado, anima) |  |
| 6.3 | Lei de Gauss | `casca_cilindrica_oca` (aprovado), `cilindro_macico_isolante` (aprovado), `casca_esferica_oca` (aprovado), `esfera_macica_isolante` (aprovado), `placa_infinita_carregada` (aprovado, anima), `cilindro_coaxial` (aprovado), `gaussiana_esferica` (aprovado), `gaussiana_cilindrica` (aprovado), `gaussiana_caixa` (aprovado) |  |
| 6.4 | Potencial elétrico | `equipotenciais` (aprovado), `gradiente_colina` (aprovado, anima) | o gradiente é o de uma colina genérica |
| 6.5 | Condutores e capacitores | `capacitor_placas_paralelas` (aprovado), `capacitor_esferico` (aprovado), `cilindro_coaxial` (aprovado), `condutor_com_cavidade` (aprovado) |  |
| 6.7 | Força magnética | `particula_em_campo_magnetico` (aprovado, anima), `espira_em_campo_magnetico` (aprovado, anima) |  |
| 6.8 | Biot–Savart | `biot_savart_espira` (aprovado, anima) |  |
| 6.9 | Lei de Ampère | `fio_infinito` (aprovado, anima), `solenoide_corrente` (aprovado, anima), `toroide_corrente` (aprovado, anima), `amperiano_circular` (aprovado), `amperiano_retangular` (aprovado) |  |
| 6.10 | Indução eletromagnética | `ima_espira_inducao` (aprovado, anima), `barra_trilhos_fem_movimento` (aprovado, anima) |  |
| 6.12 e 7.1 | Maxwell e ondas eletromagnéticas | `onda_eletromagnetica` (aprovado, anima) |  |
| 7.2 | Óptica geométrica | `lente_delgada` (aprovado), `prisma_triangular` (aprovado), `espelho_esferico` (aprovado), `dioptro_plano` (aprovado, anima) | os raios são do Manim |
| 7.3–7.4 | Interferência e difração | `anteparo_fenda_dupla` (aprovado), `ondas_duas_fontes` (aprovado, anima), `rede_de_difracao` (aprovado), `filme_fino` (aprovado, anima), `interferometro_michelson` (aprovado, anima) | fenda dupla, N fendas, filme fino e Michelson |
| 7.5 | Polarização e lei de Malus | `polarizador_malus` (aprovado, anima) |  |
| 7.6 | Relatividade especial | `cone_de_luz` (aprovado, anima), `relogio_de_luz` (aprovado, anima) |  |
| 7.11 | Estrutura atômica | `orbital_atomico` (aprovado, anima), `atomo_bohr` (aprovado, anima) | orbitais 1s, 2s, 2p, 3d e o modelo de Bohr |
| 8.12 e 9.5 | Volumes de revolução | `solido_revolucao_disco` (aprovado, anima), `solido_revolucao_arruela` (aprovado, anima), `solido_revolucao_cascas` (aprovado, anima) |  |
| 10.1 | Geometria e vetores em R³ | `produto_vetorial` (aprovado, anima), `superficie_quadrica` (aprovado), `plano_e_reta_r3` (aprovado, anima) |  |
| 10.3 | Derivadas parciais e plano tangente | `plano_tangente` (aprovado, anima) |  |
| 10.5 | Gradiente | `gradiente_colina` (aprovado, anima) |  |
| 10.6 | Extremos em várias variáveis | `pontos_criticos` (aprovado), `lagrange_restricao` (aprovado, anima) |  |
| 10.7 | Integrais duplas | `integral_dupla_colunas` (aprovado, anima) |  |
| 10.8–10.9 | Integrais triplas e Jacobiano | `elemento_volume` (aprovado, anima) |  |
| 10.10 | Centro de massa e momentos em 3D | `centro_de_massa_3d` (aprovado, anima) | hemisfério, cone, parabolóide e halteres |
| 11.1 e 11.8 | Campos vetoriais, divergência e rotacional | `campo_vetorial` (aprovado), `divergencia_local` (aprovado, anima), `rotacional_roda_de_pas` (aprovado, anima) |  |
| 11.2–11.3 | Integrais de linha | `integral_de_linha` (aprovado, anima) |  |
| 11.4 | Campos conservativos e potencial | `campo_conservativo` (aprovado, anima), `gradiente_colina` (aprovado, anima) | φ fixa (colina gaussiana) |
| 11.6–11.7 | Superfícies parametrizadas e integrais de superfície | `superficie_parametrizada` (aprovado, anima), `gaussiana_esferica` (aprovado), `gaussiana_cilindrica` (aprovado), `gaussiana_caixa` (aprovado) |  |
| 13 | Álgebra linear | `transformacao_linear_3d` (aprovado, anima), `autovetores_elipsoide` (aprovado, anima) |  |
| 15 | Equações diferenciais parciais | `membrana_modos` (aprovado, anima) | um modo por vez |
| 11.9 | Teorema de Stokes | `teorema_stokes` (aprovado, anima) |  |
| 11.10 | Teorema da divergência de Gauss | `gaussiana_esferica` (aprovado), `gaussiana_cilindrica` (aprovado), `gaussiana_caixa` (aprovado) |  |

Todos os sólidos aparecem em pelo menos um capítulo.

## 2. O que não temos, com o assunto e a limitação

### 2a. Poderiam ser sólidos 3D (0 lacunas)

| Capítulo | Assunto | Sólido sugerido | Limitação / por que ainda não |
|---|---|---|---|


### 2b. Melhor no Manim, sem sólido 3D (13 blocos)

| Capítulo | Assunto | Motivo |
|---|---|---|
| 4.4–4.5 | Polias, atrito e máquina de Atwood | o essencial são os diagramas de corpo livre e as equações: o 3D acrescenta pouco |
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
