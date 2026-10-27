# vid_0029 — Avaliação do preview v1 e HANDOFF v2 (correções)

Documento autocontido para o Claude Code. Responda em pt-BR. Base: preview v1 entregue em 2026-10-26
(`renders/preview_540x960.mp4`, 172 s) e o briefing `vid_0029_toroide_briefing.md`, que **continua valendo** em tudo que não for
alterado aqui (física, sentidos, cores, decisões do Kaio, pipeline).

---

## 1. Avaliação do v1

**Funcionou (manter):**
- Pipeline `timeline.json` + `setFrame(f)` + Manim transparente + composição: provado. Alinhamento na vista de cima com erro 0 px,
  ⊙/⊗ exatamente sobre os cruzamentos do fio. Isso é o coração do teste e está certo.
- Física e sentidos corretos: ⊙ dentro, ⊗ fora, amperiano e B anti-horários vistos de cima; I_enc = 0, NI, NI − NI; curva 1/r
  com razão 1,91 medida na própria curva; caso-limite μ₀nI.
- Estrutura dos 10 beats, títulos de região (`NO BURACO`, `DENTRO DO ENROLAMENTO`, `FORA DO ANEL`), painel final e end card.

**Corrigir (pedido do Kaio + avaliação):**
1. **3D poluído.** Os tracinhos verdes (≈150 ao longo do fio, `NTRACOS = L/0.5`) somados aos anéis magenta, ao brilho branco do aço
   e, na vista de cima, aos marcadores do Manim viram ruído. O Kaio quer **um rastro de luz verde passando**, não infinitos pontos.
2. **Álgebra pouco animada.** As equações aparecem e trocam quase por substituição. O raciocínio precisa *se mover*: termos
   saindo da integral, o comprimento do círculo virando 2πr, as espiras contadas virando N I, o cancelamento NI − NI, o 2πr
   atravessando a igualdade. Usar mais MF-Tools (`TransformByGlyphMap` com mapa explícito).
3. **Poucos vetores.** O vídeo afirma "B tangente, mesmo módulo, mais forte perto do buraco" mas quase não mostra setas de B e dℓ.
   Vetores precisam carregar essas ideias (B ∥ dℓ; |B| igual no círculo; |B| ∝ 1/r).
4. **Disputa pela tela na vista de cima.** Nas contagens (B05–B07), o 3D continua no brilho máximo e compete com os ⊙/⊗ e o círculo.
5. **Detalhes:** definições em MathTex corpo 34 pequenas no celular; esboço de R e a do B02 minúsculo; B09 aproxima demais (tubos e
   tracinhos gigantes); aço levemente lilás.

---

## 2. Unidade e rodada

- **Unidade:** `videos/vid_0029_campo_toroide/` (existente). Classe `CampoToroide029`.
- **Fase:** novo **preview visual silencioso**, 540×960 / 15 fps. Sem voz, SRT, master, legendado, entrega, publicação, commit ou push.
- **Preservar o v1:** renderize em `renders/preview_v2_540x960.mp4` (e `parte3d_v2`), sem apagar o v1.
- **Duração:** pode crescer até **~185 s** por causa das animações novas; ajuste só pelo `timeline.json`.
- Não alterar `template/`, `docs/`, `AGENTS.md`, `pyproject.toml`, `uv.lock`, o arsenal ou o `kit.py` de outras unidades
  (o `kit.py` local desta unidade pode mudar).

---

## 3. Correções do 3D (`cena3d/cena3d.js`)

### 3.1 Corrente = rastro de luz (substitui os tracinhos)

- **Remover os ~150 tracinhos.** O fio fica em aço liso.
- **Rastro (cometa) verde** no mesmo shader ao longo do fio (parâmetro s ∈ [0, L) do comprimento do fio): cabeça brilhante e cauda
  que decai para trás, `intensidade(s) = Σ_k exp(−Δ_k/τ)` para `Δ_k = mod(cabeça_k − s, L) ≥ 0`, com cauda τ ≈ 1,2 espira de
  comprimento, cabeça curta e mais clara. Cor `#3FE08B` pura na cauda, cabeça clareada ~30% (nunca branca).
- **3 rastros** igualmente espaçados no fio, velocidade constante (cada rastro dá a volta no toroide inteiro em ~8 s). O sentido do
  movimento segue a corrente da seção 5 do briefing (sobe no lado de dentro).
- Ligar a corrente (B01): **um único rastro** nasce numa ponta e percorre o enrolamento todo em ~2 s, deixando o fio aceso por um
  instante (o "flash" atual vira isso); depois entram os 3 rastros permanentes.
- **Flashes de contagem (B06/B07) ficam**, mas como **brilho só nos trechos que furam o disco** (já existe `uIn`/`uOut`): no B06 os
  24 trechos de dentro acendem um a um, em sincronia com o contador do Manim (seção 4.4); no B07 acendem os 24 de dentro e, logo
  depois, os 24 de fora, com intensidades iguais.

### 3.2 Campo = luz correndo nos anéis

- Menos anéis: **3 raios** (R − 0,6a, R, R + 0,6a) **× 3 alturas** (−0,5a, 0, +0,5a), tubos finos.
- Trocar as pontas de seta estáticas por **pulsos magenta** correndo ao longo de cada anel no sentido de B (anti-horário visto de
  cima), velocidade ∝ 1/r (mais rápidos perto do buraco): o sentido e a intensidade aparecem no movimento, sem setas.
  Brilho base ∝ 1/r mantido.
- Nada de campo no buraco nem fora, como antes.

### 3.3 Modo "contagem" (B03–B08 na vista de cima)

- Novo canal no `timeline.json`: `realce_3d` ∈ [0, 1]. Em 1 (vista de cima, B04–B08) o 3D **recua**: fio com 55% do brilho, anéis
  de campo a 35%, rastros verdes a 40%. Os flashes de contagem continuam a 100% (são eles que precisam ser vistos).
- Transições de 0,6 s. Fora da vista de cima, `realce_3d = 0`.

### 3.4 Outros

- **Aço sem lilás:** baixar a contraluz magenta para ~0,5 e o `envMapIntensity` do aço; conferir que o fio lê cinza-aço `#7A8696`.
- **B09:** aproximar menos (o trecho mostrado deve conter ~5–6 espiras, não 3), com a câmera de lado: o trecho parece um solenoide
  reto, anéis de campo quase retos atravessando. Duração da ida e volta inalterada.

---

## 4. Correções do Manim (`cena.py`)

**Regras gerais:**
- Toda passagem algébrica com correspondência clara usa **`TransformByGlyphMap` com mapa explícito** (MF-Tools 1.4.9). Construa os
  mapas com `show_indices` só no desenvolvimento; nada de índices no vídeo. `MathTex` de string única nos dois lados.
- `TransformMatchingTex` só onde casa sem enganar. `FadeOut/FadeIn` se qualquer matching enganar.
- Definições "símbolo: significado": corpo **≥ 40** (era 34). No máximo 2 definições em tela ao mesmo tempo.
- No máximo ~3 elementos novos por vez. Vetores finos quando pequenos; cores das grandezas sempre.

### 4.1 B02 — objeto
- Tirar o esboço pequeno de R e a. Os chips `MODELO IDEAL`, `N`, `I` ficam.
- R e a passam para o **início do B03, sobre a vista de cima** (seção 4.2), onde dá para ver.

### 4.2 B03 — simetria, com vetores
1. Pousou a câmera em cima: seta GEO do centro até o círculo de raio R (rótulo `R`), e um segmento GEO curto atravessando a largura
   do anel com o rótulo `a` (largura 2a, raio a da seção). 1,5 s e saem.
2. Círculo amperiano (raio dentro do enrolamento) com **8 setas magenta B tangentes, todas do mesmo comprimento**, girando
   devagar junto com o círculo (rotação rígida: mostra que girar não muda nada).
3. Junto de cada seta B, uma **seta GEO curta dℓ** sobre o círculo, no mesmo sentido. Chip `B ∥ dℓ` e o já existente
   `MESMO B NO CÍRCULO TODO`.

### 4.3 B04 — Ampère, com o comprimento do círculo
- `∮ B⃗·dℓ⃗ = μ₀ I_enc` → `∮ B dℓ = μ₀ I_enc`: **glyph map** em que o ponto do produto escalar e as setas de vetor somem
  (a justificativa visual são as setas paralelas do B03, ainda em tela, que piscam 1 vez).
- `∮ B dℓ` → `B ∮ dℓ`: **glyph map** com o B atravessando para fora da integral (arco de movimento curto, não teletransporte).
- `∮ dℓ` → `2πr`: **visual, não glyph map**: o círculo amperiano GEO se **desenrola** num segmento reto horizontal na área da
  álgebra (`Circle` → `Line` de comprimento 2πr na mesma escala, ou um retângulo fino), o segmento ganha o rótulo `2πr` e esse
  rótulo voa para o lugar de `∮ dℓ` na equação. Ponto alto do B04.
- Resultado: `B (2πr) = μ₀ I_enc`, que fica como linha de referência no topo da área da álgebra até o B07.

### 4.4 B05–B07 — contagem
- **B05:** disco translúcido GEO no buraco; o contador `I_enc` mostra 0; `B = 0` entra e as 8 setas B do B03 (agora no círculo do
  buraco) **encolhem até sumir**.
- **B06:** os 24 ⊙ aparecem **um a um em sincronia com o flash 3D** de cada trecho (seção 3.1); cada ⊙ manda uma cópia verde
  pequena para o contador, que sobe 1, 2, 3… 24 (rápido, ~2,5 s, com aceleração). Depois **glyph map** `24 I` → `N I` (o 24 vira N,
  marcando que o número da tela é só ilustração).
  Em seguida: `B (2πr) = μ₀ N I` → `B = μ₀ N I / (2πr)` por **glyph map** com o `(2πr)` atravessando a igualdade e descendo para
  o denominador (arco), e o r do denominador recebe `Indicate` GEO. As 8 setas B voltam no círculo, com o comprimento de μ₀NI/(2πr)
  na escala do gráfico do B08.
- **B07:** os ⊗ entram em sincronia com o flash de fora; o contador mostra `N I − N I`; **cancelamento**: os dois termos ganham
  um risco diagonal branco ao mesmo tempo e colapsam para `0` (glyph map dos dois N I para o 0). `B = 0`, e as setas B no círculo
  de fora encolhem até sumir.

### 4.5 B08 — gráfico ligado ao toroide (mudança de layout)
- **Eixo r do gráfico alinhado com a vista de cima:** origem do eixo r em **x = 0** (o centro do toroide) e **mesma escala** do topo
  (R − a em x = 1,886; R + a em x = 3,600). Assim as bordas do anel **descem em linhas tracejadas GEO direto do toroide para o
  gráfico**. O gráfico ocupa a metade direita (x de 0 a ~4,2); o eixo B fica em x = 0. A metade esquerda fica para a fórmula
  `B = μ₀NI/(2πr)` e o chip.
- O cursor do gráfico continua preso ao raio do amperiano (já está), e **sobre o círculo amperiano** as 8 setas B mudam de
  comprimento ao vivo: zero no buraco, salto em R − a, encolhem com 1/r, zero depois de R + a. O cursor e as setas são a mesma
  função do tempo.
- `QUASE O DOBRO` vira uma comparação visual: no fim da varredura, duas setas B paradas no gráfico (em R − a e em R + a, verticais,
  magenta) e o chip `≈ 1,9×` entre elas. Desenhar também o salto vertical tracejado em R − a e em R + a.

### 4.6 B09 — caso-limite
- `μ₀ N I / (2πR)` → `μ₀ (N / 2πR) I`: glyph map (já existe). `N / 2πR` → `n`: **glyph map** com o bloco colapsando no n, com a
  definição `n: espiras por unidade de comprimento` (corpo ≥ 40) aparecendo no mesmo tempo.
- Chip `SOLENOIDE` mantido. Sem teaser de outro vídeo.

### 4.7 B10
- Sem mudanças além de seguir as cores e corpos novos.

---

## 5. `timeline.json`

- Acrescentar: `rastros` (quantidade, período), `realce_3d` (chaves), `contagem_dentro` (início e duração do sobe-um-a-um,
  compartilhado entre o flash 3D e o contador do Manim), `contagem_fora`, `desenrola_circulo` (B04).
- Todos os tempos novos vivem só aqui; o 3D e o Manim leem a mesma chave. Se a duração passar de ~185 s, cortar pela seção 8.

---

## 6. QA do preview v2 (só o necessário)

1. `py_compile`; render do 3D e do Manim 540×960 / 15 fps; composição. Sem renders extras.
2. Quadros de conferência: B01 (rastro ligando o fio), um quadro em órbita (no máximo 3 rastros, sem pontinhos), B03 (R, a; setas B e
   dℓ paralelas e iguais), B04 (círculo desenrolado em 2πr), B06 (contador sincronizado com o flash: ⊙ número k aceso no mesmo quadro
   do contador = k), B07 (risco e colapso NI − NI → 0), B08 (bordas do anel descendo para o gráfico; setas no círculo e cursor
   coerentes; `≈ 1,9×`), B09 (5–6 espiras), B10.
3. Alinhamento 3D ↔ Manim continua ≤ 2 px (rodar `qa/alinhamento.js`) e vale também para o eixo r do gráfico (R − a e R + a do
   gráfico na mesma vertical das bordas do anel).
4. Sem índices de glyph map, sem debug, sem azul/ciano/violeta (fora o degradê da marca no end card), texto de tela em MAIÚSCULAS.
5. Duração total e por beat; custo do 3D por quadro (comparar com 0,127 s/quadro do v1).

---

## 7. O que NÃO fazer

- Voltar a usar bolinhas ou tracinhos densos; mais de 3 rastros simultâneos; setas de B fora do enrolamento ou no buraco (exceto as
  que encolhem até zero nas animações de B05/B07).
- Calcular o campo da hélice (Biot–Savart): o desenho é o modelo ideal.
- Remotion; voz; SRT; master; entrega; commit; push.
- Mudar a física, os sentidos, as cores ou o roteiro aprovados no briefing.

---

## 8. Se passar de ~185 s

Cortar nesta ordem: (1) a rotação rígida das setas no B03 (setas paradas); (2) as cópias verdes voando para o contador no B06
(o contador sobe sozinho); (3) as duas setas de comparação do B08 (fica o chip `≈ 1,9×`). **Nunca** cortar o círculo desenrolando
em 2πr (B04), o 2πr atravessando a igualdade (B06) nem o cancelamento NI − NI (B07).

---

## 9. Relatório de entrega (obrigatório)

Arquivos alterados; verificações e renders com resultados; caminho do preview v2; duração total e por beat; custo do 3D e do Manim;
limitações/pendências; atualização curta do "Teste do arsenal" e do "Teste do pipeline Three.js + Manim" (o que melhorou com o modo
"contagem" e o gráfico alinhado). Pare após o preview, sem iniciar voz.
