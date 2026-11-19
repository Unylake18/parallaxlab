# Exceções de composição declaradas

- **Corpo voxel (B2, B4-3 e S2):** o enquadramento é um detalhe do corpo, mantendo elevação de 22° e azimute de 30°. O eixo e a bancada são contexto e continuam abaixo da borda inferior. A máscara `mascaras_palco` mede somente o corpo; `mascaras` conserva todo o contexto para testar texto sobre objeto e oclusão. A prancha de objetos inclui também um plano geral da montagem. Essa separação não permite texto sobre o corpo, nem ignora colisões com o eixo visível.
- **Inset do pêndulo (B1-5):** fica à direita do aparato, acima do piso, para não cobrir o sólido. No haltere, permanece na parte inferior direita. Mantém a indicação `VISTA DE CIMA`, que representa o espaço dos momentos angulares.
- **Sinal de mais em B3-3:** a permanência de 0,3 s faz parte da fusão dos dois sinais de menos expressamente prescrita no handoff §6; não é uma linha de conta que aparece antes de ser escrita.
- **Partes individuais de L e onda de setinhas do voxel:** a escala geométrica permanece física. Algumas componentes individuais são menores que 0,6 u, especialmente antes da soma. Não são ampliadas independentemente, pois isso alteraria a comparação vetorial protegida no handoff.

Estas exceções não convertem outras falhas do portão em aprovação.

- **Setas nos insets:** o raio do círculo é 0,5 u; os segmentos de L e dL medem 0,5 u e 0,35 u, com stroke 5. São menores que o mínimo geral de 0,6 para conservar dL menor que L dentro do inset limitado a 28% da largura da coluna. Os rótulos permanecem em 36 pt, separados das pontas.

## Adaptação do auditor herdado

O teste da CONTA usava x máximo 6,8, herdado do yt_0019. A Pilha desta unidade ocupa x=0,75…7,25 (largura 6,5), conforme a divisão aproximadamente 50/50 do handoff §2.3. O auditor local usa limite 7,4, mantendo a margem externa mínima de 0,45; nenhuma fórmula foi reduzida para caber. G25 no handoff exige Pilha, sem impor o limite antigo de 6,8.

Nos cubinhos (B2-2/B2-3), a origem e parte dos vetores ficam dentro do sólido. Os rótulos ficam fora da silhueta com chamada fina até o vetor. A distância de 0,4 do G27 pode ser ultrapassada nesses rótulos para preservar a leitura; a chamada explicita a associação.

Em B1-6, os dados do fio, do ângulo e do campo gravitacional usam chamadas quando o aparato impede a distância de 0,4. Em particular, `g` é uma propriedade do campo, e sua chamada não cria uma força adicional. A busca fica limitada ao ESQUEMA, sem ocupar a calha nem a CONTA.

## Onda 1 (v2, 2026-11-08)
- PALCO 3D fora da zona (PB1 917 q., PB3 702 q.): placas de base do pórtico (PB1) e coluna da bancada abaixo do haltere (PB3) passam da borda inferior da zona porque o objeto foi aproximado para 55–75% da coluna (G3). Decisão de enquadramento, a confirmar.
- PB1 `OBJETO FORA DA MARGEM` (151 q.) e PB3 `acima do ESQUEMA` (291 q., pontas de seta): vetores L/τ passam do topo da zona em alguns ângulos; ainda não zerado.
- Caneta: cadência adaptativa (0,30 s/glifo; até 0,16 s) quando a janela da fala não comporta a linha; desvio do padrão, registrado em `[ordem] ... cadencia=`.

## Ondas 2 e 3 (PB2, PB4, PB5, PB6, PS) — preview completo v2

Portões G28 (log_aud_*.txt) ainda NÃO zerados; o que sobra, por lote:
- PB2: 1 `TRÂNSITO` (glifo da linha dL/dt = Σ r×F cruza outro durante o passo).
- PB4, PS, PH: sem ocorrência (PS só tinha `TORTO` sobre linha de sombra, removido ao mover os rótulos para baixo das bases).
- PB5: inset `VISTA DE CIMA` (`— — PLANO` 22 pt abaixo do mínimo e encostado em `dL`; linha tracejada do plano cruzando o título quando gira), 46 `RÓTULO SOLTO` e 30 `FORA DA ZONA` (rótulos com chamada longa no B5-4 "CONFERE").
- PB6: 106 `CALHA desenho Triangle` (pontas de seta das forças dos apoios) e 2 `PALCO` (2 px).
Medidos e aprovados: `MANCAIS ANGULO` = 180,0° em todos os quadros (PH e PB5, câmeras ortográficas); `RODA` L⊥ e forças dos apoios a 90,0° do eixo (PB6, 0 falhas).

## v3 (handoff v3) — G28 e portões
- PH: G28 0 ocorrências-quadro
- PB1: G28 476 ocorrências-quadro: PALCO ND N pixels fora da zona (284); TEXTO SOBRE OBJETO '..' (94); ENCOSTADO no tracejado '..' (folga N < N,N) (90)
- PB2: G28 0 ocorrências-quadro
- PB3: G28 427 ocorrências-quadro: TEXTO SOBRE OBJETO '..' x Line em (N; N)  (137); TEXTO PEQUENO '..' (N < N) (137); TEXTO SOBRE OBJETO '..' (126)
- PB4: G28 127 ocorrências-quadro: FORA DA ZONA desenho acima do ESQUEMA Triangle (y N) (102); FORA DA ZONA desenho acima do ESQUEMA Line (y N) (24); FORA DA ZONA desenho acima do ESQUEMA VMobject (y N) (1)
- PB5: G28 117 ocorrências-quadro: RÓTULO SOLTO '..' a N do dono (88); PALCO ND N pixels fora da zona (16); FORA DA ZONA desenho acima do ESQUEMA Triangle (y N) (9)
- PB6: G28 409 ocorrências-quadro: FORA DA ZONA desenho acima do ESQUEMA Line (y N) (175); CALHA desenho Triangle em (N; N) (88); FORA DA ZONA desenho acima do ESQUEMA Triangle (y N) (62)
- PS: G28 0 ocorrências-quadro

TAMANHO: haltere é magro (L×A ≈ 0,3×0,67 m); com altura 55–75% a largura fica em 26–31% (< 40%): os dois critérios do handoff são incompatíveis para ele. Mantida a altura.

## v4 (handoff v4) — portões finais (08/11/2026, preview `renders/preview_yt0025_v4_completo_960x540.mp4`, 14:14,1)
Lotes re-renderizados: PH (nenhuma mudança de código além do material do haltere, mantido do passe anterior), PB1, PB2, PB3, PB4, PB5, PB6, PS. Detalhe por quadro em `qa/g28_resumo.txt`.

G28 (ocorrências por lote, após as correções):
- PH 0 · PB2 0 · PB3 0 · PS 0.
- PB1 475 (igual ao v3, 476): PALCO 284 (plano CLOSE: o suporte sai do quadro; autorizado), TEXTO SOBRE OBJETO 99 (título «VISTA DE CIMA» do inset sobre a coluna do pórtico, no CLOSE do B1-5), ENCOSTADO no tracejado de θ 90, TRÂNSITO 2. NÃO zerado: PB1 manteve a busca de vaga do v3 (a regra de chamada curta não foi aplicada ao pêndulo); ficam TEXTO SOBRE OBJETO e ENCOSTADO.
- PB4 16: RÓTULO SEM VAGA de `L_z` no B4-3 (corpo em pé ocupa a vizinhança da ponta; sobreposição parcial com os cubos). Antes: 127 (FORA DA ZONA de pontas de seta, zerado).
- PB5 337: RÓTULO SEM VAGA 280 e TEXTO SOBRE OBJETO 46 (rótulo `L_z` na abertura do B5-1, sobre o cartão do plano), ENCOSTADO 8 e SOBREPOSIÇÃO 1 (`L_⊥` × `dL⃗` na vista de topo), PALCO 2. Antes: 117 (RÓTULO SOLTO e PALCO; RÓTULO SOLTO zerado).
- PB6 460: TEXTO SOBRE OBJETO 409 (rótulo de `L⃗_⊥` colado à ponta, em cima do pneu translúcido, em CLOSE/AXIAL: a ponta está dentro do pneu), PALCO 36 (suporte, plano CLOSE: autorizado), FORA DA ZONA 1, ANGULO TELA 14 linhas brutas (quadros de transição). Antes: 409 (FORA DA ZONA/CALHA, zerados).

TAMANHO v4 (grupo objeto+vetores, altura 55–75 %, área ≥ 18 % da coluna, sem corte): 0 falhas em PH, PB1, PB2, PB4, PB5, PB6, PS. PB3 tem 1 falha: B3-1 com área 17 % (haltere esbelto já com altura 75 %; aumentar a câmera estoura a altura).
CONTRASTE: ≥ 3,0 em todas as amostras de todos os lotes (PB3: 2,1 → ≥ 3; PB2 e PS corrigidos com material mais claro).
RESÍDUO v4: 0 em PH; PB1 5, PB2 8, PB3 4, PB4 9, PB5 6, PB6 1, PS 2 apontamentos; as linhas que rolam na Pilha são ignoradas (11 em PB1, 8 em PB2, 9 em PB3, 8 em PB5, 8 em PB6, 1 em PS); os apontamentos conferidos eram selo, sublinhado ou o começo da linha seguinte. O `2` do B3-5 é uma cópia deliberada (voo) que se sobrepõe ao original por 1–2 quadros, sem sobra.
FLASH POR QUADRO: 0 com tinta antes da vez em PH, PB1, PB2, PB5, PB6, PS; PB3 (108,20 s) e PB4 (51,13 s) têm 1 evento cada, com tira em `qa/flash/`: rolagem da Pilha e linha anterior sumindo, sem destino antecipado.
MANCAIS ANGULO: 180,0° em 54 amostras (PH 25, PB5 29). RODA 90,0° em 249 amostras. ANGULO NA TELA: 8/9 pares OK; B6-4 tem 1 amostra (a âncora dura 1,3 s).
CADÊNCIA: mínimo 0,200 s/glifo (PB1); lista «enxugar a pauta» (para a Produção): PB2 B2-3, `\vec L_i = (\vec\rho_i+z_i\hat z)\times m_i\vec v_i` (0,180 s/glifo) e `\vec L_i = \vec\rho_i\times m_i\vec v_i + z_i\hat z\times m_i\vec v_i` (0,164 s/glifo).
ORDEM POR X: medidor ainda marca linhas por termo mapeado; tiras conferidas em `qa/ordem/` (B4-3 e B2-1 vistas no v4: ordem correta, sem fade cruzado).
