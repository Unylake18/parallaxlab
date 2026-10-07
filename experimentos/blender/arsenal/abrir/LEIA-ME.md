# Abrir os sólidos no Blender

> Arquivo **gerado** por `gerar_atalhos.py` (rode de novo ao criar sólidos). Dê dois cliques no `.bat` do sólido: o Blender abre com ele
> montado, enquadrado e em modo Renderizado; se tem movimento, o loop já toca (espaço pausa, setas andam um quadro).
> `_escolher.bat` pergunta o id. Para mudar parâmetros: `blender.exe -P experimentos/blender/arsenal/abrir_no_blender.py -- <id> --set nome=valor`.
> Os parâmetros e seus valores estão em `solidos/<id>.json`. Blender 5.2; se estiver em outro lugar, defina `BLENDER_EXE`.

## algebra_linear

| Atalho | Sólido | Status | Movimento |
|---|---|---|---|
| [`autovetores_elipsoide.bat`](autovetores_elipsoide.bat) | Autovetores e elipsoide de uma matriz simétrica | aprovado | loop |
| [`transformacao_linear_3d.bat`](transformacao_linear_3d.bat) | Transformação linear em R³ | aprovado | loop |

## calculo

| Atalho | Sólido | Status | Movimento |
|---|---|---|---|
| [`campo_conservativo.bat`](campo_conservativo.bat) | Campo conservativo e potencial | aprovado | ciclo único |
| [`campo_vetorial.bat`](campo_vetorial.bat) | Campo vetorial (setas) | aprovado | — |
| [`centro_de_massa_3d.bat`](centro_de_massa_3d.bat) | Centro de massa em 3D | aprovado | loop |
| [`divergencia_local.bat`](divergencia_local.bat) | Divergência local (cubo elementar) | aprovado | loop |
| [`elemento_volume.bat`](elemento_volume.bat) | Elemento de volume dV (cartesiano, cilíndrico, esférico) | aprovado | loop |
| [`gradiente_colina.bat`](gradiente_colina.bat) | Gradiente numa colina (curvas de nível) | aprovado | loop |
| [`integral_de_linha.bat`](integral_de_linha.bat) | Integral de linha (trabalho) | aprovado | ciclo único |
| [`integral_dupla_colunas.bat`](integral_dupla_colunas.bat) | Soma de Riemann dupla (colunas) | aprovado | ciclo único |
| [`lagrange_restricao.bat`](lagrange_restricao.bat) | Multiplicadores de Lagrange | aprovado | loop |
| [`plano_e_reta_r3.bat`](plano_e_reta_r3.bat) | Plano e reta em R³ | aprovado | loop |
| [`plano_tangente.bat`](plano_tangente.bat) | Plano tangente a uma superfície | aprovado | loop |
| [`pontos_criticos.bat`](pontos_criticos.bat) | Pontos críticos (máximo, mínimo e sela) | aprovado | — |
| [`produto_vetorial.bat`](produto_vetorial.bat) | Produto vetorial a × b | aprovado | loop |
| [`rotacional_roda_de_pas.bat`](rotacional_roda_de_pas.bat) | Rotacional local (roda de pás) | aprovado | loop |
| [`solido_revolucao_arruela.bat`](solido_revolucao_arruela.bat) | Sólido de revolução: método das arruelas | aprovado | loop |
| [`solido_revolucao_cascas.bat`](solido_revolucao_cascas.bat) | Sólido de revolução: método das cascas | aprovado | loop |
| [`solido_revolucao_disco.bat`](solido_revolucao_disco.bat) | Sólido de revolução: método dos discos | aprovado | loop |
| [`superficie_parametrizada.bat`](superficie_parametrizada.bat) | Superfície parametrizada com remendo dS | aprovado | loop |
| [`superficie_quadrica.bat`](superficie_quadrica.bat) | Superfícies quádricas | aprovado | — |
| [`teorema_stokes.bat`](teorema_stokes.bat) | Teorema de Stokes (hemisfério e contorno) | aprovado | loop |

## edp

| Atalho | Sólido | Status | Movimento |
|---|---|---|---|
| [`membrana_modos.bat`](membrana_modos.bat) | Modos de vibração de uma membrana | aprovado | loop |

## eletromagnetismo

| Atalho | Sólido | Status | Movimento |
|---|---|---|---|
| [`amperiano_circular.bat`](amperiano_circular.bat) | Contorno amperiano circular | aprovado | — |
| [`amperiano_retangular.bat`](amperiano_retangular.bat) | Contorno amperiano retangular | aprovado | — |
| [`anel_carregado.bat`](anel_carregado.bat) | Anel carregado (aro) | aprovado | loop |
| [`barra_trilhos_fem_movimento.bat`](barra_trilhos_fem_movimento.bat) | Barra em trilhos num campo B (fem de movimento) | aprovado | loop |
| [`biot_savart_espira.bat`](biot_savart_espira.bat) | Biot–Savart numa espira | aprovado | loop |
| [`capacitor_esferico.bat`](capacitor_esferico.bat) | Capacitor esférico (esferas concêntricas, em corte) | aprovado | — |
| [`capacitor_placas_paralelas.bat`](capacitor_placas_paralelas.bat) | Capacitor de placas paralelas | aprovado | — |
| [`cargas_pontuais.bat`](cargas_pontuais.bat) | Cargas pontuais e forças de Coulomb | aprovado | loop |
| [`casca_cilindrica_oca.bat`](casca_cilindrica_oca.bat) | Casca cilíndrica oca | aprovado | — |
| [`casca_esferica_oca.bat`](casca_esferica_oca.bat) | Casca esférica oca (com corte em octante) | aprovado | — |
| [`cilindro_coaxial.bat`](cilindro_coaxial.bat) | Cilindro coaxial (condutor maciço + casca externa, em corte) | aprovado | — |
| [`cilindro_macico_isolante.bat`](cilindro_macico_isolante.bat) | Cilindro maciço isolante com cargas no volume | aprovado | — |
| [`condutor_com_cavidade.bat`](condutor_com_cavidade.bat) | Condutor com cavidade e cargas induzidas | aprovado | — |
| [`dipolo_eletrico.bat`](dipolo_eletrico.bat) | Dipolo elétrico e seu campo | aprovado | loop |
| [`disco_carregado.bat`](disco_carregado.bat) | Disco carregado | aprovado | loop |
| [`equipotenciais.bat`](equipotenciais.bat) | Superfícies equipotenciais (carga pontual e dipolo) | aprovado | — |
| [`esfera_macica_isolante.bat`](esfera_macica_isolante.bat) | Esfera maciça isolante com cargas no volume | aprovado | — |
| [`espira_em_campo_magnetico.bat`](espira_em_campo_magnetico.bat) | Espira de corrente num campo magnético (torque) | aprovado | loop |
| [`fio_infinito.bat`](fio_infinito.bat) | Fio infinito (retilíneo) | aprovado | loop |
| [`gaussiana_caixa.bat`](gaussiana_caixa.bat) | Superfície gaussiana em caixa (pillbox) | aprovado | — |
| [`gaussiana_cilindrica.bat`](gaussiana_cilindrica.bat) | Superfície gaussiana cilíndrica (fechada) | aprovado | — |
| [`gaussiana_esferica.bat`](gaussiana_esferica.bat) | Superfície gaussiana esférica | aprovado | — |
| [`haste_carregada.bat`](haste_carregada.bat) | Haste carregada | aprovado | loop |
| [`ima_espira_inducao.bat`](ima_espira_inducao.bat) | Ímã atravessando uma espira (Faraday e Lenz) | aprovado | ciclo único |
| [`linhas_de_campo_3d.bat`](linhas_de_campo_3d.bat) | Linhas de campo em 3D | aprovado | loop |
| [`onda_eletromagnetica.bat`](onda_eletromagnetica.bat) | Onda eletromagnética plana | aprovado | loop |
| [`particula_em_campo_magnetico.bat`](particula_em_campo_magnetico.bat) | Partícula carregada em campo magnético uniforme | aprovado | ciclo único |
| [`placa_infinita_carregada.bat`](placa_infinita_carregada.bat) | Placa infinita carregada (plano com cargas na superfície) | aprovado | loop |
| [`solenoide_corrente.bat`](solenoide_corrente.bat) | Solenoide (hélice de fio) | aprovado | loop |
| [`toroide_corrente.bat`](toroide_corrente.bat) | Toroide (fio enrolado em anel) | aprovado | loop |

## fisica2

| Atalho | Sólido | Status | Movimento |
|---|---|---|---|
| [`massa_mola.bat`](massa_mola.bat) | Sistema massa-mola horizontal (MHS) | aprovado | loop |
| [`onda_corda.bat`](onda_corda.bat) | Onda numa corda (progressiva e estacionária) | aprovado | loop |
| [`ondas_duas_fontes.bat`](ondas_duas_fontes.bat) | Ondas na superfície com duas fontes (interferência) | aprovado | loop |
| [`pendulo_simples.bat`](pendulo_simples.bat) | Pêndulo simples (pequenas oscilações) | aprovado | loop |

## fisica4

| Atalho | Sólido | Status | Movimento |
|---|---|---|---|
| [`atomo_bohr.bat`](atomo_bohr.bat) | Átomo de Bohr: salto e fóton | aprovado | ciclo único |
| [`cone_de_luz.bat`](cone_de_luz.bat) | Cone de luz no espaço-tempo | aprovado | ciclo único |
| [`orbital_atomico.bat`](orbital_atomico.bat) | Orbitais atômicos (nuvens de probabilidade) | aprovado | loop |
| [`relogio_de_luz.bat`](relogio_de_luz.bat) | Relógio de luz e dilatação do tempo | aprovado | ciclo único |

## fluidos

| Atalho | Sólido | Status | Movimento |
|---|---|---|---|
| [`prensa_hidraulica.bat`](prensa_hidraulica.bat) | Prensa hidráulica (Pascal) | aprovado | loop |
| [`tanque_hidrostatico.bat`](tanque_hidrostatico.bat) | Tanque com pressão e empuxo | aprovado | loop |
| [`tanque_torricelli.bat`](tanque_torricelli.bat) | Jato de Torricelli | aprovado | loop |
| [`tubo_escoamento.bat`](tubo_escoamento.bat) | Tubo com estrangulamento (continuidade) | aprovado | loop |

## mecanica

| Atalho | Sólido | Status | Movimento |
|---|---|---|---|
| [`aro_rolando.bat`](aro_rolando.bat) | Aro rolando sem deslizar | aprovado | loop |
| [`cilindro_rolando.bat`](cilindro_rolando.bat) | Cilindro rolando sem deslizar | aprovado | loop |
| [`colisao_1d.bat`](colisao_1d.bat) | Colisão unidimensional entre dois blocos | aprovado | ciclo único |
| [`colisao_2d.bat`](colisao_2d.bat) | Colisão elástica em 2D | aprovado | ciclo único |
| [`curva_inclinada.bat`](curva_inclinada.bat) | Curva inclinada (pista com inclinação) | aprovado | loop |
| [`esfera_rolando.bat`](esfera_rolando.bat) | Esfera rolando sem deslizar | aprovado | loop |
| [`explosao.bat`](explosao.bat) | Explosão em três fragmentos | aprovado | ciclo único |
| [`giroscopio_precessao.bat`](giroscopio_precessao.bat) | Giroscópio e precessão | aprovado | loop |
| [`movimento_circular.bat`](movimento_circular.bat) | Movimento circular uniforme | aprovado | loop |
| [`orbita_kepleriana.bat`](orbita_kepleriana.bat) | Órbita kepleriana com setores de áreas iguais | aprovado | loop |
| [`paisagem_potencial.bat`](paisagem_potencial.bat) | Bola numa paisagem de energia potencial | aprovado | loop |
| [`plano_inclinado.bat`](plano_inclinado.bat) | Plano inclinado com forças | aprovado | ciclo único |
| [`poco_gravitacional.bat`](poco_gravitacional.bat) | Poço gravitacional (potencial) | aprovado | loop |
| [`rampa_rolamento.bat`](rampa_rolamento.bat) | Corrida de esfera, cilindro e aro numa rampa | aprovado | ciclo único |
| [`trilho_looping.bat`](trilho_looping.bat) | Looping (pista com laço vertical) | aprovado | ciclo único |

## otica

| Atalho | Sólido | Status | Movimento |
|---|---|---|---|
| [`anteparo_fenda_dupla.bat`](anteparo_fenda_dupla.bat) | Anteparo de fenda dupla | aprovado | — |
| [`dioptro_plano.bat`](dioptro_plano.bat) | Dioptro plano: refração e reflexão interna total | aprovado | loop |
| [`espelho_esferico.bat`](espelho_esferico.bat) | Espelho esférico (côncavo e convexo) | aprovado | — |
| [`filme_fino.bat`](filme_fino.bat) | Filme fino e interferência | aprovado | loop |
| [`interferometro_michelson.bat`](interferometro_michelson.bat) | Interferômetro de Michelson | aprovado | loop |
| [`lente_delgada.bat`](lente_delgada.bat) | Lente delgada (biconvexa ou biconcava) | aprovado | — |
| [`polarizador_malus.bat`](polarizador_malus.bat) | Polarizadores e lei de Malus | aprovado | loop |
| [`prisma_triangular.bat`](prisma_triangular.bat) | Prisma triangular | aprovado | — |
| [`rede_de_difracao.bat`](rede_de_difracao.bat) | Rede de difração | aprovado | — |

## termodinamica

| Atalho | Sólido | Status | Movimento |
|---|---|---|---|
| [`caixa_gas_cinetica.bat`](caixa_gas_cinetica.bat) | Gás ideal em recipiente com êmbolo (teoria cinética) | aprovado | loop |
