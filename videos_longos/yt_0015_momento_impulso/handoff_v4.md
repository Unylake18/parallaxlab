# HANDOFF v4 — yt_0015 "Momento linear e impulso" (preview silencioso v4)

Documento autocontido para o Claude Code. A **narração v4** (anexa: `yt_0015_roteiro_narracao_v4.md`, salvar na unidade como `narracao_sugestao.md` e manter a v3 como `narracao_sugestao_v3.md`) é a especificação de conteúdo: física, texto de fala e linhas `tela:`. Se achar inconsistência objetiva, reporte antes de ampliar o escopo.

## 0. Contexto
- Unidade: `.claude/worktrees/lucid-ritchie-cd87ad/videos_longos/yt_0015_momento_impulso/` (preview v3). Rode `git status --short` e preserve tudo.
- O Kaio aprovou a evolução visual do v3: representação, animações, cavalo, gráfico em escala real. **O que ele pediu agora:**
  1. **O começo ainda é fraco:** não mostra de onde vem o m v⃗. A teoria deve ser construída como no Sears: partir da segunda lei, chegar em p⃗ = m v⃗, decompor em x, y, z no espaço, e desenvolver a álgebra até o impulso.
  2. **Nenhuma cena só de álgebra.** Sempre há algo acontecendo: animação, esquema 2D ou 3D, junto com a álgebra. As variáveis saem da animação direto para a conta (MF-Tools).
  3. **Exercícios:** o esquema visual fica na tela o tempo todo, com a álgebra se desenvolvendo à direita.
  4. **Nada de tempo morto:** muitas cenas demoram sem informação nova.
  5. **Tirar todas as referências de livros** da tela (e da fala). As fontes vão só na descrição do YouTube. Cada exercício entra como situação didática ligada à teoria que acabou de ser mostrada.
- Sem voz, SRT, master, entrega, commit ou push. Não alterar `template/`, `docs/`, `assets/`, `experimentos/threejs/`.
- Rodada: preview silencioso **v4** 960×540 / 15 fps, completo, mais os stills da §7. Duração esperada: ~19–20 min (fala ~18 min).

## 1. Estrutura nova da teoria (o que muda em relação ao v3)

| Bloco | Linha 2 do header (= capítulo do YouTube) | Origem |
|---|---|---|
| Hook / abertura | — | igual (A3 sem citar livro) |
| **T1** | `DE ONDE VEM O MOMENTO` | **novo** (absorve o antigo "A SEGUNDA LEI COM MOMENTO", que deixa de existir) |
| T2 | `O FATO EXPERIMENTAL` | antigo T1 (discos), com ponte nova e T2-5 animado |
| T3 | `POR QUE MASSA VEZES VELOCIDADE?` | antigo T2 (trilho), com T3-5 novo |
| T4 | `DA CONSERVAÇÃO À TERCEIRA LEI` | antigo T3 |
| **T5** | `IMPULSO` | **refeito**: caso constante → integral → força média → componentes |
| E1–E5, T6, síntese, CTA | iguais ao v3 | só tiram o selo de livro e ganham o selo de ligação (§3) |

Atualizar `ancoras.json` a partir da narração v4 (a numeração das âncoras T1–T5 mudou) e o `ficha.md` (status v4; o campo `referencia:` da ficha fica, porque é interno).

## 2. Física e construção dos blocos novos
Todas as equações em `MathTex` de string única, estabilizadas antes do glyph map. Cores: velocidade violeta, momento magenta, força azul-claro, impulso/área `#9CC7FF`.

### T1 — DE ONDE VEM O MOMENTO (Three.js + Manim, modo PALCO + CONTA)
- **Cena 3D (PALCO, Three.js):** eixos x, y, z finos (`GEO`), com chão em grade leve; uma partícula (esfera de aço) percorre uma **curva suave no espaço**, por exemplo r⃗(t) = (a cos ωt, b t, c sin ωt) ou outra curva lisa e reversa, com rastro fino. Em cada quadro: v⃗ = dr⃗/dt (violeta, tangente) e F⃗_res = m d²r⃗/dt² (azul-claro, apontando para a concavidade). **Os vetores saem da própria curva**, nada desenhado à mão, para a física ficar coerente.
- **Exportar** por quadro as coordenadas de tela da partícula e das pontas dos vetores e das projeções (`timeline.json`), para o Manim prender rótulos e fazer os rótulos "descerem" para a conta. Conferir com `qa/alinhamento.js` (≤ 2 px).
- T1-1: na CONTA, `ΣF⃗ = m a⃗`, com F⃗ e a⃗ nascendo dos rótulos da cena (`TransformFromCopy` do rótulo para o glifo).
- T1-2: v⃗ em dois instantes próximos, copiados para a mesma origem; a diferença Δv⃗ encolhe para dv⃗ (Δt → 0); vira `a⃗ = dv⃗/dt` e substitui na conta: `ΣF⃗ = m dv⃗/dt`. Depois o `m` **desliza para dentro da derivada** com `TransformByGlyphMap`: `ΣF⃗ = d(m v⃗)/dt`, com o selo `MASSA CONSTANTE`.
- T1-3: `m v⃗` acende; na partícula, a seta magenta p⃗ nasce da violeta v⃗, esticada pelo fator m; `p⃗ = m v⃗` + `MOMENTO LINEAR · QUANTIDADE DE MOVIMENTO` + `kg·m/s`.
- T1-4 (2D, vista de cima): dois carros iguais (silhuetas preenchidas em aço), 20 m/s, um para o norte e outro para o leste, com setas magenta do mesmo tamanho; `|p⃗₁| = |p⃗₂|` e `p⃗₁ ≠ p⃗₂`.
- T1-5 (volta ao 3D): v⃗ copiado para a origem; caixa tracejada até os três eixos; as projeções `vx`, `vy`, `vz` acendem nos eixos, **e os rótulos descem para a conta**: `px = m vx`, `py = m vy`, `pz = m vz`.
- T1-6: na conta, `ΣF⃗ = d(m v⃗)/dt` vira `ΣF⃗ = dp⃗/dt` (caixa) por substituição; depois as três componentes `ΣFx = dpx/dt`, `ΣFy = dpy/dt`, `ΣFz = dpz/dt`. No PALCO, F⃗_res também se projeta, e **três barras magenta** (px, py, pz) ao lado da cena variam no tempo, cada uma na taxa da componente de força correspondente. Como p⃗ = m v⃗(t) da mesma curva, isso fecha sozinho.
- T1-7: `ΣF⃗ = dp⃗/dt` com os selos `A FORMA ORIGINAL DE NEWTON` e `REFERENCIAL INERCIAL`; no PALCO, o foguete do v3 soltando gás com `MASSA VARIÁVEL`.

### T2 — O FATO EXPERIMENTAL
- Igual ao v3 em T2-1 a T2-3.
- T2-4: a tabela é **montada a partir dos discos**: cada linha nasce de uma colisão, com os valores de v saindo das setas; os discos ficam pequenos à esquerda, repetindo a colisão da linha atual.
- T2-5: no lugar da tela só com `P⃗ = constante`, a experiência 3 roda em loop lento com as setas p⃗₁, p⃗₂ e a soma P⃗ (magenta, sempre do mesmo tamanho) acompanhando; a equação e o `PRINCÍPIO DE CONSERVAÇÃO DO MOMENTO (SISTEMA ISOLADO)` ficam na CONTA.

### T3 — POR QUE MASSA VEZES VELOCIDADE?
- T3-1 a T3-3 iguais ao v3 (trilho 3D, visão do carro).
- T3-4: o trilho continua visível em cima, rodando cada colisão (m×m, m×2m, 2m×3m) **enquanto a conta correspondente fecha** embaixo. Hoje as três equações ficam sozinhas na tela (200 s).
- T3-5: o bloco com v⃗ e p⃗ do T1 volta ao lado da soma; dois selos (`DA SEGUNDA LEI` e `DA SIMETRIA`) convergem para o mesmo `p⃗ = m v⃗`.

### T4 — DA CONSERVAÇÃO À TERCEIRA LEI
Igual ao v3, mais um relógio de colisão no PALCO encolhendo Δt durante o T4-2. As setas Δp⃗ saem do ponto de contato.

### T5 — IMPULSO (construção do caso constante até as componentes)
- **T5-1 (caso constante):** PALCO com um bloco num piso sem atrito, uma força constante F⃗ de t₁ a t₂ (relógio) e a seta magenta crescendo. Na CONTA, **dois gráficos empilhados**: F × t (o retângulo cresce com o tempo) e p × t (reta, inclinação = F). Os três andam sincronizados.
- **T5-2:** o triângulo de inclinação aparece no gráfico p × t; o cateto vertical vira `p⃗₂ − p⃗₁` e o horizontal vira `t₂ − t₁` dentro da conta (`TransformFromCopy` dos rótulos do gráfico). Cadeia: `ΣF⃗ = dp⃗/dt` → `ΣF⃗ = (p⃗₂ − p⃗₁)/(t₂ − t₁)` → `ΣF⃗ (t₂ − t₁) = p⃗₂ − p⃗₁`, com o `(t₂ − t₁)` **atravessando a igualdade** por `TransformByGlyphMap`.
- **T5-3:** `J⃗ = ΣF⃗ Δt = p⃗₂ − p⃗₁` (caixa); a área do retângulo no F × t acende em `#9CC7FF` junto com o J⃗. Linha de unidades animada: `N·s = (kg·m/s²)·s = kg·m/s`, com o `s` cancelando um dos `s` do `s²`.
- **T5-4 e T5-5:** a parede e o Riemann do v3 (4 → 8 → 32). Novidade: a cada retângulo, um pedacinho Δp⃗ se soma na seta da bola (ligação visual entre área e momento).
- **T5-6:** `Σ F⃗ₖ Δtₖ → ∫ₜ₁ᵗ² ΣF⃗ dt`, depois `∫ₜ₁ᵗ² (dp⃗/dt) dt = ∫ dp⃗` (limites p⃗₁ a p⃗₂) `= p⃗₂ − p⃗₁`. O `dt` se cancela e **os limites trocam de t₁, t₂ para p⃗₁, p⃗₂** (glyph map). Enquanto isso, a área do gráfico é preenchida da esquerda para a direita e a seta p⃗ da bola acompanha. Hoje a integral fica sozinha numa caixa (400 s).
- **T5-7:** `J⃗ = ∫ΣF⃗ dt = F⃗_méd (t₂ − t₁)`; retângulo de mesma base e mesma área; depois duas curvas de formas diferentes e mesma área. **Reportar as áreas medidas.**
- **T5-8 (componentes):** PALCO com p⃗₁, p⃗₂ e Δp⃗ num plano xy, com as componentes projetadas nos eixos (tracejado); na CONTA, `Jx = ∫ΣFx dt = (F_méd)x Δt = m v₂x − m v₁x` e a linha de y, com cada termo acendendo junto com a projeção correspondente; `E O MESMO EM z`. O vetor J⃗ solitário do v3 (420 s) sai.
- T5-9: DICA (igual).

## 3. Regras de tela para o vídeo todo
1. **Proibida a tela só de álgebra.** Teoria = PALCO vivo (3D, esquema 2D ou gráfico animado) + CONTA. Telas do v3 a corrigir: 125 s (P⃗ = constante), 200 s (três equações), 400 s (integral na caixa), 420 s (J⃗ sozinho), 615 s (K = ½mv² e v = p/m), 735 s (E4: só os dois painéis de conta), 820 s (E5: só o painel). A síntese (895 s) ganha o muro ou as duas curvas pequenas no PALCO.
2. **As variáveis saem da animação.** Todo símbolo que representa algo desenhado (v⃗, F⃗, p⃗, Δt, vx, h, d, as massas) aparece primeiro como rótulo no desenho e vai para a conta com `TransformFromCopy`, na mesma cor. Rearranjos algébricos com `TransformMatchingTex`; termo atravessando a igualdade, cancelamento e troca de limites com `TransformByGlyphMap`. Sem índices de debug no render.
3. **Sempre algo acontecendo.** No máximo ~4 s sem informação nova. Enquanto a fala explica, o PALCO trabalha: o fenômeno em loop lento, o termo que está sendo dito realçado no desenho e na conta ao mesmo tempo, vetores pulsando quando citados. Pausas paradas medidas no v3: 4–13, 30–37, 195–202, 210–217, 245–252, 491–501, 516–530, 545–557, 582–595, 622–632, 684–692, 725–732, 765–772, 805–813, 815–822 s. Rodar a mesma medição no v4 e reportar o que passar de 6 s.
4. **Exercícios com layout fixo:** o esquema do problema fica no PALCO **do começo ao fim do exercício** (nunca sai); dados, álgebra e resultado descem linha a linha na CONTA. Os dados nascem dos rótulos do esquema.
   - E4: PALCO com o manequim e o muro (3D recuado) e, depois, o gráfico em escala real; os dois caminhos na CONTA, um embaixo do outro (o caminho 1 fica apagado a 40% quando o 2 começa); o número final pisca nos dois ao mesmo tempo.
   - E5: a pulga (e o zoom) fica no PALCO durante os dois caminhos.
   - T6: as mãos e as bolas, e depois os barcos, ficam no PALCO enquanto K = p²/(2m) se constrói na CONTA. A substituição v = p/m entra no lugar de v por `TransformByGlyphMap`.
5. **Sem referências de livro.** Remover o selo de fonte de todas as cenas (`MOYSÉS §…`, `SEARS · EX. …`, `FEYNMAN §…`). O header fica com as duas linhas. No lugar, cada exercício abre com um **selo de ligação** pequeno, no mesmo lugar do antigo selo de fonte (`DIM`, opacidade 0,85), dizendo o que da teoria ele usa:
   - E1 `TEOREMA DO IMPULSO · COM SINAL`
   - E2 `IMPULSO POR COMPONENTES`
   - E3 `IMPULSO COMO INTEGRAL`
   - T6 `IMPULSO × TRABALHO`
   - E4 `DOIS CAMINHOS: TEMPO E DISTÂNCIA`
   - E5 `FORÇA DE CONTATO × RESULTANTE`
6. Continuam valendo do v3: a grade PALCO/CONTA/CENTRO/DOIS PAINÉIS, folga ≥ 0,25, centralização pela tela inteira, a DICA no canto e a paleta.

## 4. Correções pontuais do v3
- Hook: a cota ainda está `2.5 m`; usar `2,5 m`.
- T5 (350 s): o rótulo `FORÇA DA PAREDE` aparece quase transparente e o gráfico fica só com o eixo t. Entrar com os eixos completos e o rótulo opaco.
- T6, barcos (660 s): o rótulo `2m` está em cima da faixa da raia. Pôr os rótulos acima de cada barco.
- CTA (cavalo): está muito melhor, manter. Só a seta −F⃗ no cavalo fica pequena e por cima do corpo. Ela deve ficar fora do corpo, na altura da corda, perto do peitoral, com o mesmo comprimento da F⃗ da pedra e o rótulo `−F⃗`. A interrogação está apagada demais: usar opacidade ~0,7.

## 5. Narração
Usar a v4 anexa. Mudanças em relação à v3: T1 novo; T2–T4 renumerados (antigos T1–T3) com pontes; T5 refeito; nenhuma menção a livro (A3, T3-1, T4-1, T4-5, T6-1, T6-3 e as aberturas dos exercícios foram reescritas como situação didática). As fontes estão no fim do arquivo, só para a descrição.

## 6. Render mínimo
- O 3D do T1 primeiro em quadros soltos (T1-1, T1-5 com a caixa de projeção, T1-6 com as barras), conferindo o alinhamento dos rótulos; depois o trecho inteiro.
- Iterar por lote; o completo só no fim.

## 7. Stills e QA
- Stills 1920×1080: T1-2 (m entrando na derivada), T1-5 (projeções e px, py, pz), T1-6 (barras), T5-2 (triângulo de inclinação → conta), T5-6 (troca de limites com a área preenchida), T5-8 (componentes), E4 (manequim + caminhos), E5 (pulga + caminhos).
- QA:
  - nenhuma tela só de álgebra (listar qualquer intervalo > 2 s sem objeto não textual animado ou visível no PALCO);
  - pausas paradas > 6 s;
  - sobreposição e folga;
  - alinhamento 3D × Manim ≤ 2 px (hook, T1, T3, E4, F2);
  - áreas do T5-7 e do E4;
  - nenhum texto com `MOYSÉS`, `SEARS` ou `FEYNMAN` no código das cenas (grep) nem no vídeo.

## 8. Parada e relatório
Pare com o preview v4 completo. Relatório (AGENTS.md):
- arquivos alterados e criados;
- renders e caminhos;
- resultados do QA;
- curva usada no T1 e como os vetores foram calculados;
- duração final;
- Teste do arsenal;
- pendências.

Sem commit nem push.

## Adendo do Kaio (2026-10-28, no chat)
- T3 (trilho, "POR QUE MASSA VEZES VELOCIDADE?"): sai o 3D do trilho. Fazer em 2D/2,5D, bem bonito, com as cores aprovadas; referência de
  paleta = o conteúdo de colisões (yt_0014), que usa mais cores. O 3D ali é pesado e não soma na didática. Com isso, o alinhamento
  3D × Manim do QA deixa de valer para o T3.
