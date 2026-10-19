# yt_0005 — Rodada de redesign visual/didático (previews R1–R4)

Escopo: previews silenciosos 960×540 / 30 fps, um por trecho. Sem voz, SRT, master, 1080p, contínuo B01–B09, commit ou push. Nenhum arquivo global (`template/`, `docs/`, `AGENTS.md`) alterado. Blender não usado (o 2.5D do B06 é Manim). `yt_0003`/`yt_0004` não tocados.

## Arquivos alterados
- `videos_longos/yt_0005_magnetostatica_forca_lorentz/cena.py` (único arquivo de código alterado).
- `videos_longos/yt_0005_magnetostatica_forca_lorentz/RELATORIO_REDESIGN.md` (este relatório, novo).
- Artefatos novos em `renders/redesign/` (previews, quadros, zips, logs; mídia pesada não é versionada).

## Mudanças globais
- **Corrente em verde** `#3FE08B` (o mesmo do `vid_0009_campo_solenoide`): I, K, J, setas e pulsos de corrente, fluxo de J, leituras I_ent/I_sai, ∇·J. Carga (q, dq, λ, σ, ρ, Q) segue azul; B magenta; E ciano; v violeta; forças azul-claro.
- **Painéis azul-escuros** (`PANEL`) no lugar de caixas brancas: destaques, cards, leituras e callouts (função `box()`/`panel()`).
- **Fonte das equações mais contida** (`fs()`: redução progressiva acima de 32 pt) e largura máxima por equação (`MAXW` = 5,7 unidades), para evitar sobreposição.
- Seletores `SEG=R1|R2|R3|R4` (`rsec()`/`seg()`): só o trecho escolhido gera quadros.

## R1 — B01 + aprofundamento K + B02/B03 (`preview_R1`, 6:55)
- B01: corrente verde e em movimento nos fios; geometria de Lorentz preservada.
- Determinante construído por componentes (i → F_x=0, j → +Bv_z ŷ, k → −Bv_y ẑ), com a célula/menor destacados, a componente da força acendendo no desenho e os termos coletados por `TransformFromCopy`.
- Newton com o vetor calculado; uma equação por componente, com a componente correspondente destacada.
- EDO → "qual função volta com sinal trocado" (verificação por derivação de sen e cos) → solução geral C1 cos + C2 sen → condições iniciais (C1 = 0; C2 = v⊥ pela equação acoplada em t = 0) → v_z = (1/ω_c) dv_y/dt (cosseno nasce da equação acoplada).
- Espaço das velocidades com `vec()` próprio: a ponta do v⊥ termina exatamente no ponto da circunferência; painéis separados "trajetória real" × "espaço das velocidades".
- Integração com limites (dy = …, ∫_{y0}^{y(t)} dy = ∫_0^t …, primitiva, colchetes), depois R ≡ v⊥/ω_c, y−y0−R = −R cos, quadrados, soma → circunferência (centro C e R no desenho). Texto fala "circunferência", não cicloide.
- Hélice: glifo de v∥ corrigido (MathTex no lugar de `∥` em `Text`).
- Centrípeta com a órbita viva (v⊥, F_B radial e R acompanham a partícula); período com barra de tempo e "2πR uma volta"; cancelamento de v⊥ por `strike`.

## R2 — B04 + B05 (`preview_R2`, 3:23)
- B04: `dW = F·dr` (com dr desenhado na órbita viva, F_B ⊥ dr) → `P = dW/dt` → `P = F·(dr/dt)` → `dr/dt = v` → `P = F·v` → `P_B = q(v×B)·v = 0`; trabalho e energia cinética a partir daí.
- Quatro cards (fonte elétrica ciano → corrente verde → interação magenta → movimento violeta) com pulso colorido de alto contraste.
- B05: I/K/J verdes; carga azul; definições viraram chamadas curtas ("carga / comprimento", "corrente / largura", "corrente / área"); textos longos encurtados.

## R3 — B06 (`preview_R3`, 1:48)
- Volume de controle 2.5D em Manim (faces translúcidas, arestas ocultas tracejadas); J como linhas verdes contínuas, regulares e animadas (largura ∝ corrente); carga interna como grade de partículas cuja ocupação segue Q_int.
- Desbalanço causal (I_sai > I_ent → Q_int ↓; I_ent > I_sai → Q_int ↑) com leituras vivas; a nota "câmera lenta" saiu da tela (a lei física permanece internamente).
- Álgebra da continuidade à direita com o volume vivo à esquerda; faces de entrada/saída acendem; células com setas de divergência no passo do teorema; regime estacionário com fluxo contínuo e `J≠0`, `∇·J=0`.

## R4 — B07 + B08 + B09 + CTA (`preview_R4`, 2:48)
- Thomson: aparato à esquerda (~58%), gráfico à direita; F_E → F_B → resultante em sequência com líderes; cartão limpo do produto vetorial (v→+x̂, B→+ẑ, v×B→−ŷ); callout externo do `v_sel` ligado ao ponto; margem própria para o gráfico.
- B08: mesma composição do B07; E desligado visível; região de B delimitada; R legível; equações à direita.
- B09: J verde regular e animado (J≠0, ∇·J=0); retorno aos fios da abertura com corrente verde em movimento e anéis de B orientados (portadores magenta girando, regra da mão direita); a pergunta "Como uma corrente cria B?" aparece com a cena viva.
- CTA no padrão do `yt_0001` (anéis tracejados, logo horizontal, chamada de inscrição) + tease "Próximo: como uma corrente gera campo magnético".

## Verificações executadas
- `py_compile` e checagem de nomes indefinidos (AST) em cada versão.
- Teste K isolado a 960×540/15 fps, depois os quatro previews finais a 960×540/30 fps, todos concluídos sem erro na última tentativa (R1, R2, R3, R4).
- Inspeção visual de folhas de contato (1 quadro a cada 6–10 s) de cada preview, em várias rodadas; correções de sobreposição aplicadas e re-renderizadas: legendas fora da tela, painéis "trajetória real × espaço das velocidades", rótulo F_B × R, texto das duas partículas × órbita, painel de leituras × setas de saída (B06), rótulos F_E/F_B × placas, caixa vazia do `v_sel`, "v = E/B" × "vem do seletor".
- QA por trecho (R1): determinante passo a passo ✔; tokens que sobrevivem (`TransformFromCopy`) ✔; cada componente ligada ao desenho ✔; EDO→sen/cos deduzido ✔; condições iniciais fixam C1/C2 ✔; v_z da equação acoplada ✔; v⊥ chega ao ponto ✔ (conferido no quadro); integração com limites ✔; circunferência demonstrada com centro e R ✔; glifo de v∥ ✔; centrípeta com órbita viva ✔; período visual ✔.
- QA R2 ✔ (dW antes de P; P = F·v derivado; P_B = 0 pela perpendicularidade; cards com contraste; pulso colorido; corrente verde; definições discretas). QA R3 ✔ (profundidade, J verde móvel e regular, carga interna convincente, desbalanço causal, "câmera lenta" fora da tela, divisão da tela, J estacionário contínuo). QA R4 ✔ (sem sobreposições relevantes no Thomson, produto vetorial em área limpa, gráfico × v_sel, B08 contínuo, fios espelham a abertura, corrente verde em movimento, B orientado, pergunta com cena viva, CTA presente).

## Pontos ainda imperfeitos
- R4: sem pendências visuais conhecidas (o rótulo F_y foi movido para fora das placas e re-renderizado).
- Verificação por amostragem de quadros (1 a cada 6–10 s), não quadro a quadro; transições rápidas (ReplacementTransform) mostram estados intermediários sobrepostos por frações de segundo.
- O desenho do B01–B03 ainda usa v⊥ branco em B01 (gramática antiga aprovada) e violeta nos trechos novos.
- Escala fixa 2,5D do B06 não tem rotação de câmera; o balanço usa a lei física com escala de tempo interna (não exibida).
- Memória: um render paralelo do `yt_0006` (outra tarefa) causou `MemoryError` em várias tentativas; os previews finais foram refeitos um por vez.
- Dependências de áudio/voz continuam fechadas; nada foi sincronizado.

## Teste do arsenal
Nenhum sólido Blender integrado nesta rodada (o briefing pede 2.5D em Manim para o B06). O volume 2.5D foi feito com polígonos em projeção oblíqua; se o catálogo tiver "caixa com profundidade" aprovada, vale testá-la como alternativa mais barata em uma rodada futura.

## Artefatos
- `renders/redesign/media_R{1..4}/videos/cena/540p30/preview_R{1..4}.mp4`.
- `renders/redesign/entrega_gpt/yt0005_redesign_R{1..4}_para_gpt.zip` (vídeo + `cena.py` + relatório + quadros 1 fps).
- Logs: `renders/redesign/R{1..4}.log` e `renders/redesign/old/`.

## Contínuo B01–B09 (`yt0005_continuo_B01_B09_540p30.mp4`, 14:53)
- Montado pela **concatenação sem recodificação** (remux de pacotes H.264) dos quatro previews finais R1 → R2 → R3 → R4, que cobrem exatamente as seções consecutivas da mesma `cena.py` (abertura–B03 | B04–B05 | B06 | B07–B09+CTA). Cada preview executa as seções anteriores sem render, então o estado de cena na emenda é idêntico ao de um render único; não foi feito um render único de ponta a ponta.
- Verificação: 960×540 / 30 fps, 26.802 quadros decodificados sem erro (soma das durações: 415,3 + 203,1 + 107,6 + 167,4 = 893,4 s). Emendas conferidas por quadros em 6:55, 10:18 e 12:05 (cross-fade natural, sem salto de estado).
- Zip: `renders/redesign/entrega_gpt/yt0005_continuo_B01_B09_para_gpt.zip` — vídeo contínuo, `cena.py`, este relatório, 894 quadros (1 por segundo, nomeados por tempo), folha das emendas.
- Não é render de 1080p, não tem áudio/SRT/master; sem commit.

## Render único do contínuo (`yt0005_continuo_unico_B01_B09_540p30.mp4`, 14:53)
- Render de ponta a ponta de `YT0005MagnetostaticaM1` sem `SEG`, 960×540 / 30 fps, na tentativa 1 da fila (sem falha por memória). 26.802 quadros decodificados sem erro, 893,4 s.
- Comparado quadro a quadro (amostra de 1 por segundo, 894 quadros) com o contínuo montado por concatenação: nenhuma diferença média acima de 1 nível de cinza; os dois são equivalentes. **Este é o arquivo de referência**; a versão concatenada fica como redundância.
- Zip: `renders/redesign/entrega_gpt/yt0005_continuo_unico_para_gpt.zip` (vídeo, `cena.py`, relatório, 894 quadros nomeados por tempo).
