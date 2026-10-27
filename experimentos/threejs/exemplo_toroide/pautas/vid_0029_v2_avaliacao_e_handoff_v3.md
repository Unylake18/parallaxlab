# vid_0029 — Avaliação do preview v2 e HANDOFF v3

Documento autocontido para o Claude Code. Responda em pt-BR. Base: preview v2 (`renders/preview_v2_540x960.mp4`, 185 s).
Continuam valendo o briefing `vid_0029_toroide_briefing.md` e o handoff v2 em tudo que não for alterado aqui (física, sentidos, cores,
rastros, modo contagem, gráfico alinhado, decisões do Kaio).

---

## 1. Avaliação do v2

**O Kaio aprovou a direção visual** ("tá ficando sensacional toda a representação gráfica"). Funcionou e fica:
- 3 rastros verdes no lugar dos tracinhos; pulsos magenta nos anéis; modo contagem recuando o 3D; ⊙/⊗ em sincronia com os flashes.
- Setas B e dℓ paralelas e iguais no círculo; setas encolhendo a zero no buraco e fora; eixo r do gráfico na escala da vista de
  cima, com as bordas do anel descendo tracejadas; `≈ 1,9×`; colapso N/2πR → n; painel final.
- Alinhamento 3D ↔ Manim 0 px e contador sincronizado com o flash (t = 89,4 s: 5 e 5).

**O que falta (pedido do Kaio + avaliação):**
1. **Equações soltas do desenho.** As contas aparecem embaixo, mas quase nada liga um símbolo ao que ele representa no desenho.
   O Kaio quer "linkar o máximo possível do desenho com as equações, o gráfico, a representação".
2. **Faixa de legenda.** Reservar um espaço pequeno, mais baixo, para a legenda queimada, com fonte menor que a atual. Hoje a álgebra
   e o gráfico descem até perto da base (eixo r do gráfico em ~88 % da altura).
3. **B04:** o círculo que rola e se desenrola passa **por cima da equação** (quadro em ~66 s): fica embolado.
4. **Trocas embaralhadas:** NI − NI → 0 e 2πr descendo têm quadros intermediários ilegíveis (o relatório já apontou).
5. **Rótulo a** pequeno e coberto pelo fio no B03.

---

## 2. Unidade e rodada

- **Unidade:** `videos/vid_0029_campo_toroide/`. Classe `CampoToroide029`.
- **Fase:** preview visual silencioso, 540×960 / 15 fps. Sem voz, SRT, master, legendado, entrega, publicação, commit ou push.
- **Preservar v1 e v2:** saídas `renders/preview_v3_540x960.mp4` e `parte3d_v3`.
- **Duração:** até ~195 s, ajustando só o `timeline.json`.
- Não alterar `template/`, `docs/`, `AGENTS.md`, `pyproject.toml`, `uv.lock`, o arsenal nem `videos/montar_legendado.py`
  (a legenda compacta da seção 4 é só reserva de espaço agora; o estilo do script entra numa rodada própria).

---

## 3. Elos entre equação e desenho (o centro desta rodada)

**Regra do elo.** Todo símbolo com significado geométrico ou físico tem um **gêmeo no desenho**. Quando o símbolo entra, muda ou é
destacado, o gêmeo **pulsa junto** (mesma cor, mesmo instante, 0,4–0,6 s). Na primeira vez de cada par, uma **linha-guia** fina e
tracejada, na cor da grandeza, liga o glifo ao gêmeo por ~1 s e some. No máximo **um elo aberto por vez**. Implementar como helper
(`elo(glifo, alvo, cor)`) no `kit.py` local, usado igual em todos os beats.

| Símbolo na equação | Gêmeo no desenho | Quando |
|---|---|---|
| **B** (magenta) | as 8 setas B no círculo | B03, B04, e sempre que B aparece pela 1ª vez numa linha |
| **dℓ** (GEO) | as setas dℓ no círculo | B03 e B04 (ponto do produto escalar some) |
| **r** (GEO) | **seta de raio GEO** do centro até o círculo amperiano, rótulo `r` na ponta | entra no B03 e fica até o B08, acompanhando o raio do círculo |
| **2πr** (GEO) | o contorno do círculo (já desenrola no B04) | B04; depois, sempre que `2πr` for destacado, o contorno acende |
| **I_enc** (verde) | o disco translúcido GEO do amperiano + as marcas ⊙/⊗ dentro dele | B04 (definição), B05–B07 |
| **N** (branco) | o anel de 24 ⊙ (acende todo de uma vez) | no `24 I → N I` do B06 |
| primeiro **N I** do B07 | o anel de ⊙ | B07 |
| segundo **N I** do B07 | o anel de ⊗ | B07 |
| **r** do denominador (B06) | a seta de raio | `Indicate` simultâneo |
| **B = μ₀NI/(2πr)** (B08) | a curva do gráfico **e** as setas no círculo | B08 (seção 3.2) |
| **n** (B09) | um trecho de "1 unidade" no close do solenoide, com as espiras contadas (opcional, ver 3.3) | B09 |
| `DENTRO` / `FORA` (painel B10) | ícone 2D do anel no painel (seção 3.4) | B10 |

### 3.1 B04 sem embolar
- O círculo que rola e se desenrola ganha **faixa própria**, acima da equação (entre o toroide e a álgebra), sem cruzar nenhum glifo.
  O segmento 2πr fica nessa faixa; só o rótulo `2πr` voa para a equação.
- A seta de raio `r` entra **antes** do desenrolar: o segmento resultante é visualmente "2π vezes aquela seta".

### 3.2 B08 — gráfico como leitura da equação
- Enquanto o cursor varre: **barra vertical magenta** do eixo r até a curva, no ponto do cursor, com o **mesmo comprimento** das
  setas B no círculo naquele instante (mesma escala). A barra e as setas são o mesmo valor desenhado em dois lugares.
- O `r` do denominador da fórmula ao lado **acende** enquanto o cursor anda dentro do enrolamento; chip pequeno `∝ 1/r` com linha-guia
  do denominador até a curva, uma vez.
- Nos trechos de B = 0 (buraco e fora), o `B = 0` correspondente (já mostrado em B05/B07) reaparece pequeno junto do eixo, ligado ao
  trecho reto da curva por linha-guia.

### 3.3 B09 (opcional, cortar primeiro se faltar tempo)
- No close lateral, um colchete GEO marcando um trecho do anel com o rótulo `1 unidade`, e as espiras desse trecho acendendo em
  verde (flash do 3D): é o n. Ligado ao `n` da equação por elo.

### 3.4 B10 — painel com ícone
- No painel final, à esquerda das duas linhas, um **ícone 2D pequeno do anel** (dois círculos GEO). `DENTRO` acende a coroa do anel
  em magenta; `FORA` acende o buraco e a região externa em magenta-escuro tracejado com o `B = 0`.

### 3.5 Trocas sem quadros embolados
- **NI − NI → 0:** risco nos dois termos (como hoje) → os dois termos fazem `FadeOut` (sem morphing) → `0` faz `FadeIn` no lugar.
  Glyph map só onde há correspondência real; aqui não há.
- **2πr descendo:** o glyph map continua, mas com **arco maior e `run_time` ≥ 1,2 s**, e os glifos de `2πr` passam por **cima** do
  traço de fração (z-index) para não cruzar com μ₀NI. Conferir quadro a quadro o meio do movimento.

### 3.6 Rótulo a (B03)
- `a` sai do anel com **linha-guia** curta para fora, à direita do toroide, corpo ≥ 40; o segmento da largura fica acima do fio
  (z-index) por esses 1,5 s.

---

## 4. Faixa de legenda (reserva de espaço)

**Pedido do Kaio:** um espaço pequeno, mais baixo, com fonte menor, visível no Reels.

**Especificação para este layout (540×960):**
- **Faixa reservada para a legenda:** de **y_px = 760 a 840** (79 % a 87,5 % da altura). Em unidades do Manim: **y de −4,67 a −6,0**.
  Nada da cena (Manim nem 3D importante) entra nessa faixa, exceto o fundo e as estrelas.
- **Abaixo de 840 px** (y < −6,0): sem conteúdo (área mais coberta pela interface do celular).
- **Conteúdo útil:** da manchete até **y = −4,5** no máximo.
- **Legenda futura (alvo):** fonte ~**23 px em 540** (hoje 29), uma linha preferencialmente, no máximo duas, centrada, base em
  ~835 px. Isso vira um estilo novo (`compacto`) no `montar_legendado.py` **numa rodada própria**, quando a fase de legenda abrir.
  Agora só a reserva.
- **QA:** gerar um quadro de cada beat com um **retângulo de teste** desenhado nessa faixa (só no quadro de QA, nunca no vídeo) e um
  texto de exemplo em 23 px, para o Kaio conferir num rascunho do Reels no celular.

**Consequência no layout (reescala a vista de cima):**
- Fator 3D → Manim novo: **3,0/2,1 ≈ 1,4286** (era 1,714). Centro do toroide na vista de cima em **(0; 3,3)**. Então
  R − a → 1,571; R → 2,286; R + a → 3,000; o anel ocupa y de 0,3 a 6,3. Manchete e tag continuam acima.
- **Área da álgebra:** y de **0 a −4,5**. Uma equação principal por vez (corpo 56; resultado 64), mais uma linha de apoio.
- **Gráfico do B08:** eixo r alinhado à nova escala (origem x = 0; R − a em x = 1,571; R + a em x = 3,000), eixo B de altura ~2,6,
  base em y ≈ −4,2. Fórmula à esquerda, menor (corpo 48).
- Marcadores ⊙/⊗: raio ~0,11 (o círculo de dentro encolheu). Conferir legibilidade.
- Atualizar `timeline.json` (`fator_3d_manim`, `centro_topo_manim`) e o `qa/alinhamento.js`: continua ≤ 2 px.
- O close do B09 e as órbitas também respeitam y > −4,5.

---

## 5. QA do preview v3 (só o necessário)

1. `py_compile`; render 3D e Manim 540×960 / 15 fps; composição. Sem renders extras.
2. Quadros: B03 (rótulo a legível; seta r), B04 (desenrolar na faixa própria, sem cruzar a equação), B06 (`24 I → N I` com o anel de ⊙
   acendendo; 2πr descendo sem embolar: 3 quadros do meio do movimento), B07 (os dois N I ligados aos dois anéis; FadeOut/FadeIn no 0),
   B08 (barra do cursor = setas do círculo; `∝ 1/r`), B10 (ícone do painel).
3. **Faixa da legenda:** prancha com o retângulo de teste em todos os beats; nada de conteúdo dentro dela.
4. Alinhamento 3D ↔ Manim ≤ 2 px na nova escala (vista de cima e eixo r do gráfico).
5. No máximo um elo aberto por vez; linhas-guia somem; sem índices/debug; texto de tela em MAIÚSCULAS.
6. Duração total e por beat; custos.

---

## 6. O que NÃO fazer

- Conteúdo na faixa da legenda ou abaixo dela; alterar `montar_legendado.py` agora.
- Mais de um elo aberto ao mesmo tempo; linhas-guia permanentes.
- Morphing de glifos sem correspondência real (NI − NI → 0).
- Mudar física, sentidos, cores, roteiro, rastros ou o modo contagem aprovados.
- Voz, SRT, master, entrega, commit, push, Remotion.

---

## 7. Se passar de ~195 s

Cortar nesta ordem: (1) o colchete `1 unidade` do B09 (3.3); (2) o ícone do painel (3.4) vira só os chips; (3) as linhas-guia da
segunda ocorrência em diante (fica só o pulso simultâneo). **Nunca** cortar a seta de raio r, a barra do cursor igual às setas, nem o
elo dos dois N I com os dois anéis.

---

## 8. Relatório de entrega (obrigatório)

Arquivos alterados; verificações e renders; caminho do preview v3; prancha com a faixa de legenda; duração total e por beat; custos;
limitações e pendências; nota curta para o "Teste do pipeline Three.js + Manim" sobre o helper de elos (se ficou genérico o bastante
para outros vídeos). Pare após o preview.
