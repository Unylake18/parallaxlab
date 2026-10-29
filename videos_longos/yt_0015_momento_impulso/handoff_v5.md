# HANDOFF v5 — yt_0015 "Momento linear e impulso" (polimento do preview v4)

Documento autocontido para o Claude Code. **Substitui a versão de 28/10 de manhã deste mesmo arquivo.** A narração v4 (`narracao_sugestao.md`) não muda, e a física não muda.
Esta rodada é **só tela**: legibilidade, sobreposição, vetores e rótulos. O v4 cumpriu a estrutura pedida, então não reestruture blocos.
Mantém-se a decisão do v4: **T1 e T3 em Manim** (2,5D com a curva calculada em 3D, alinhamento de 0 px). O Three.js fica só no hook, no E4-1 e no CTA.

## 0. Contexto
- Unidade: `.claude/worktrees/lucid-ritchie-cd87ad/videos_longos/yt_0015_momento_impulso/` (preview v4, 18:16). Rode `git status --short` e preserve tudo.
- Sem voz, SRT, master, entrega, commit ou push. Não alterar `template/`, `docs/`, `assets/`, `experimentos/threejs/`.
- Rodada: preview silencioso **v5** 960×540 / 15 fps. Rerenderizar só os lotes afetados (T1, T3, T4, T5-8, E1, E2, E3, T6, E5, hook, CTA) e remontar o completo.

**Pedido do Kaio:** "no início tem coisas sobrepostas nas barras de momento em x, y, z; com a massa se mexendo, tem momentos em que o vetor fica borrado, ou o nome dele fica atrás do vetor; era bom sempre ficar à mostra e nítido".

## 1. T1 — DE ONDE VEM O MOMENTO (prioridade)
O que se vê no v4, quadro a quadro (tempos do preview):
- 74–96 s: a partícula anda o tempo todo enquanto a álgebra acontece. Os rótulos `m`, `v⃗`, `ΣF⃗`, `a⃗`, `Δv⃗`, `dv⃗` se empilham em cima da esfera (80 s: `m` e `v⃗` fundidos em "mv"; 87–96 s: `Δv⃗`/`dv⃗` escondidos atrás da esfera e da seta de ΣF⃗).
- a⃗ e ΣF⃗ são paralelos (F = m a), então as duas setas ficam uma sobre a outra.
- Quando a seta aponta quase na direção da câmera, a projeção encurta, a ponta fica maior que a haste e o vetor "borra" (83 s, 87 s, 99 s, 171 s, 177 s).
- 107 s: o `m` vira "ɱn" no meio do glyph map; 110–112 s: `d(mv⃗)` dobrado e um `=` órfão embaixo; 158–159 s: `d(mv⃗)` reaparece com o m deformado.
- 123,5 s: tela vazia (só `p⃗ = m v⃗`) entre a cena 3D e os carros.
- 126–134 s: um carro passa por cima do outro no cruzamento, e os rótulos `p⃗₁` e `p⃗₂` aparecem em dobro (`p⃗₂p⃗₂`). Há também um `≠` órfão em 134 s.
- 140–156 s: o v⃗ copiado na origem é curto; a caixa de projeção e os rótulos `vx`, `vy`, `vz` ficam miúdos.
- 164–177 s: a coluna das barras px, py, pz fica colada no eixo y e na caixa da equação. As setas azuis passam por cima das barras, e os rótulos `pxpypz` viram uma palavra só.
- Em todo o T1, a cena 3D ocupa só ~1/3 da largura, com um halo radial escuro recortado atrás.

**Correções:**
1. **A partícula para quando a álgebra fala.** Ela anda livre só no T1-1 (uma volta) e nas transições. Em cada passo de derivação (T1-2, T1-3, T1-5) ela desacelera até parar (`rate_func=smooth`, ~0,8 s) num **ponto de pose** e só volta a andar quando o passo terminar. Critérios do ponto de pose, que devem ser calculados e reportados:
   - ângulo entre v⃗ e ΣF⃗ projetados entre 70° e 110°;
   - comprimento projetado de cada vetor ≥ 1,0 unidade e ≥ 60% do comprimento real (nada apontando para a câmera);
   - nenhum vetor cruzando um eixo;
   - rótulos livres de sobreposição.

   No T1-6 (barras), a partícula anda **devagar** (metade de ω) para as barras variarem.
2. **Ordem de desenho fixa** (`z_index`): rastro/curva 0, eixos e chão 1, esfera 2, vetores 3, **rótulos 4**. Nenhum rótulo fica atrás de nada.
3. **Rótulos nítidos:**
   - cada rótulo tem contorno de fundo na cor do fundo (`set_stroke(BG, width=6, background=True)`), tamanho fixo e nunca gira;
   - ele fica além da ponta do vetor, no prolongamento, com folga de 0,2 em espaço de tela;
   - se colidir com outro rótulo ou com a esfera, gira o deslocamento em ±60° até ficar livre;
   - o `m` aparece só no começo do T1-1, abaixo e à esquerda da esfera, e some quando entra na conta.
4. **Vetores sem borrar:** haste com `stroke_width` 4 e opacidade 1. A ponta tem tamanho fixo (`tip_length` 0,18), mas se reduz junto se o vetor projetado ficar curto (nunca maior que 35% do comprimento). Comprimento mínimo projetado de 0,9: abaixo disso, o vetor não é desenhado e a pose é evitada pelo item 1. Nada de opacidade parcial em vetor em movimento.
5. **a⃗ fora da partícula.** Na partícula fica só ΣF⃗. A construção de Δv⃗ → dv⃗ (T1-2) vai para um **inset ampliado** (lupa circular de ~2,2 de diâmetro, ao lado da esfera, ligada a ela por um traço fino):
   - v⃗(t) e v⃗(t + Δt) saem da mesma origem, em escala 2×, e Δv⃗ vai entre as pontas;
   - Δt encolhe e Δv⃗ vira dv⃗, que gira até ficar paralelo a ΣF⃗;
   - o rótulo `a⃗ = dv⃗/dt` sai do inset para a conta.
6. **Escala:** a cena ocupa ~55% da largura (x ∈ [−6,6; 1,0]), e a conta encosta nela. Tirar o halo radial (ou deixá-lo com opacidade ≤ 0,15, sem borda visível).
7. **Glyph maps sem deformação:** no `ΣF⃗ = m dv⃗/dt → ΣF⃗ = d(m v⃗)/dt`, o `m` **viaja inteiro** (translação pura) para dentro dos parênteses; os parênteses entram com `FadeIn` e o `v⃗` desliza. Nada de morph de glifo diferente em glifo diferente. Depois de cada transformação, nenhum mobject órfão pode sobrar na cena (ver QA).
8. **Sem tela vazia em 123 s:** crossfade direto da cena 3D para o painel dos carros (sobreposição de 0,5 s).
9. **Carros:**
   - cada carro anda na sua estrada sem cruzar a do outro (o carro 1 numa estrada vertical à esquerda e o carro 2 numa horizontal embaixo, com as estradas sem se encontrar dentro do painel);
   - os rótulos `p⃗₁` e `p⃗₂` aparecem **uma vez** em cada seta: as setas nos carros têm rótulo, e a comparação com origem comum usa as mesmas setas copiadas, sem novos rótulos;
   - o `≠` só entra dentro da equação `p⃗₁ ≠ p⃗₂`.
10. **Caixa de projeção (T1-5):**
    - v⃗ copiado para a origem com comprimento ≥ 1,8 (escala uniforme, legenda pequena `CÓPIA DE v⃗ NA ORIGEM`);
    - arestas tracejadas com opacidade 0,6;
    - componentes `vx`, `vy`, `vz` grossas (stroke 5) sobre os eixos, com rótulos de contorno de fundo;
    - a partícula parada no ponto de pose enquanto isso.
11. **Barras px, py, pz (T1-6):**
    - painel próprio dentro do PALCO, à direita da cena e **separado do eixo y e da caixa da equação por ≥ 0,3**, com linha de zero marcada;
    - três barras de largura ≥ 0,35 e vão de 0,25;
    - rótulos `px`, `py`, `pz` em cima de cada barra, em magenta, separados;
    - a seta azul de ΣFx, ΣFy, ΣFz **ao lado** de cada barra (à direita), nunca por cima;
    - a linha da conta de cada componente acende junto com a barra correspondente.
12. Foguete (T1-7): ele anda devagar para a direita enquanto solta gás (hoje fica parado, só com as partículas).

## 2. Resto do vídeo (achados da varredura quadro a quadro)
- **Hook (5–13 s, parado):** desta vez está autorizado mexer na animação 3D do hook. Faça um travelling lento da câmera (dolly-in de ~8%) e um balanço leve de peso do manequim antes do pulo. O pulo em si fica como está.
- **T3 (312 s):** o trilho fica sozinho e vazio por ~3 s entre as colisões. Emendar a próxima colisão já entrando.
- **T4 (344–372 s):** as setas Δp⃗₁ e Δp⃗₂ ficam soltas abaixo do painel. Elas devem sair dos próprios discos, dentro do painel, a partir do ponto de contato. O rótulo `CONTATO` encosta nos rótulos Δp⃗: tirar ou subir.
- **T4 (396–400 s):** `REAÇÃO DO PESO` e `−P⃗` cruzam a borda do círculo da Terra. Rótulos fora do círculo, com um fio fino até a seta.
- **T5-8 (572–600 s):** o halo recortado de novo; os traços soltos `Jx`/`Jy` devem virar projeções tracejadas de Δp⃗ = J⃗ nos eixos (como no handoff anterior).
- **E1:**
  - 648 s: a seta F⃗_méd sai de dentro da parede e passa por cima de `mg = 3,9 N` e dos textos apagados. A seta deve sair da bola, na altura do centro dela, com `mg` abaixo da bola.
  - 656 s: a linha `|Δp⃗|: 12 → 20` termina com a unidade cortada. Escrever `12 → 20 kg·m/s` inteiro.
- **E2 (692–715 s):** o esquema vira miniatura ilegível. O esquema fica em tamanho legível à esquerda (textos ≥ 20 px a 960×540) e o triângulo entra ao lado, ou o triângulo é desenhado sobre o próprio esquema, com origem na bola.
- **E3 (720–760 s):** há dois pontos brancos na curva (o que anda e o do dado 1,25 s). Deixar só o ponto do dado, com rótulo `(1,25 s; 781,25 N)` acima e à esquerda da curva, sem encostar no eixo.
- **T6:**
  - 800–825 s: as mãos ainda parecem garras. Trocar por luva de beisebol de perfil (forma única preenchida, concha aberta, sem antebraço), com a bola entrando na concha e as cotas `d` e `5d`.
  - 848 s: um `F⃗ᵣ` órfão no alto antes da equação.
  - 796 s: o meio da substituição mostra `K ≡ (p/2m)`. Usar a sequência `K = ½ m v²` → `K = ½ m (p/m)²` → `K = p²/(2m)`, cada passo por `TransformMatchingTex`, sem estados intermediários estranhos.
- **E5 (1004–1012 s):** o `2d` do denominador de `F_res = m a = m v²/(2d)` bate em `CAMINHO 2 TEMPO`. Abrir 0,25 de folga entre os blocos dos dois caminhos.
- **CTA (1080–1095 s):** a corda ainda sai da pedra e atravessa o flanco do cavalo até a faixa do ombro. Prender a corda num ponto que não cruze o corpo: um gancho na traseira, na altura do quadril, ou um tirante pelo lado de lá, escondido pelo corpo. As setas F⃗ e −F⃗ continuam nas pontas da corda, na direção dela.

## 3. QA (obrigatório antes de entregar)
1. **Órfãos:** depois de cada `TransformByGlyphMap`/`TransformMatchingTex`/`ReplacementTransform`, listar os mobjects na cena e comparar com o esperado. Zero órfãos.
2. **Rótulos visíveis:** no T1, para cada quadro, verificar se a caixa de cada rótulo não intersecta a esfera, outro rótulo ou outro vetor (folga ≥ 0,1). Reportar o pior caso.
3. **Vetores legíveis:** no T1, para cada quadro, comprimento projetado ≥ 0,9 e razão ponta/comprimento ≤ 0,35. Reportar o pior caso.
4. Sobreposição geral com folga ≥ 0,25, pausas paradas > 6 s (`medir_parado.py`) e "só álgebra" (deve continuar zero).
5. Stills 1920×1080: T1-2 (inset Δv⃗ → dv⃗), T1-3, T1-5 (caixa de projeção), T1-6 (barras), carros, T4 (Δp⃗ nos discos), E2, T6 (luvas), E5 (dois caminhos), F2 (corda).

## 4. Parada e relatório
Pare com o preview v5 completo. Relatório (AGENTS.md):
- arquivos alterados;
- lotes rerenderizados;
- pontos de pose escolhidos no T1 (s, ângulo, comprimentos);
- resultados do QA 1–4;
- caminhos dos stills, do preview e do zip para revisão;
- pendências.

Sem commit nem push.
