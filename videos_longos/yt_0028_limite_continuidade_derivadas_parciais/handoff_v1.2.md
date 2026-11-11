# yt_0028 · CÁLCULO III · EP. 03 · Limite, continuidade e derivadas parciais
## HANDOFF v1.2 (para o Claude Code): preview visual do vídeo inteiro

**v1.2 (2026-11-11, revisão de rigor):**
- B6: do B6-3 em diante, o palco mostra o **modelo linear local** J·H, e não o campo original, porque o fluxo e^{tJ} é exato só para esse modelo. Entra o rótulo `MODELO LINEAR LOCAL`.
- A curva das pontas do B1 nunca é chamada de elipse, e o B7-5 sai.
- A narração deixa claro que o limite não olha o próprio ponto e que a tabela descreve como o campo muda **bem de perto**, não o campo inteiro.
- O QA de sobreposição passa a medir a seta inteira (haste e ponta).
- Quadros-alvo 10–13 e 18 refeitos.

**v1.1 (2026-11-11, Kaio):** o pedacinho de fluido deixa de ser um bloco coral liso. Agora ele é uma chapa coral escura, com uma malha 4×4 por dentro que se deforma junto (§3.2). Os quadros-alvo 01, 12–18 foram refeitos.

Data: 2026-11-11. Formato: `longo_horizontal`. Unidade nova: `videos_longos/yt_0028_limite_continuidade_derivadas_parciais/`.

**Fase:** só o **preview visual silencioso** do vídeo inteiro, em 960×540 a 15 fps. Não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

Este handoff é autocontido. Tudo o que você precisa está nele e na pasta que vem junto no zip (`yt0028_handoff_v1.2_completo.zip`):
- `yt_0028_quadros_alvo_v1/`: os 18 quadros-alvo (1920×1080) e a folha de contato. O gerador `sb28.html` (Canvas + KaTeX, `?k=<chave>`) também está lá e guarda as coordenadas exatas. Rode com o `fundo.png`, as fontes e a pasta `katex/` do lado.
- `verificacao/verifica_calc3_t3_sympy.py` e a saída dele: 40 checagens, todas `True`. Todos os números da tela saem dali.

A matemática, o roteiro e os textos já estão aprovados pelo Kaio. Não rediscuta. Se encontrar uma inconsistência objetiva, reporte antes de mudar.

---

## 0. O que entregar

1. A unidade nova, com `ficha.md` (§1), `cena.py` e as seções `sec_*.py` (uma por bloco).
2. O preview do vídeo inteiro, `renders/v1/yt_0028_preview_v1_540p15.mp4`, com a duração guiada pela narração estimada (§8).
3. Para cada um dos 18 quadros-alvo, um still do render no gatilho correspondente e uma **prancha lado a lado, render × alvo**: `renders/v1/qa/comparacao_v1.jpg`, com uma linha por quadro.
4. O relatório de sobreposição (R5): `renders/v1/qa/sobreposicoes_v1.txt`, com zero ocorrências esperadas.
5. O relatório de entrega (AGENTS.md): arquivos, renders, QA, pendências.

## 1. Ficha

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 03
titulo: Limite, continuidade e derivadas parciais
disciplina: Cálculo III
modulo: 3.1 Funções de várias variáveis reais a valores vetoriais (no repositório: 11.1)
bloco: 3.1-T3
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §1.5 e §1.6 (só na descrição do YouTube; nada de livro na tela nem na fala)
solido_3d: nenhum do arsenal Blender, porque o vídeo é inteiro no plano
3d_threejs: nenhuma cena
duracao_alvo: 12–13 min
```

## 2. Base de código

- **Antes de começar:** leia `docs/estado_atual.md` e rode `verificacao/verifica_calc3_t3_sympy.py` com o Python da `.venv` (as 40 linhas devem dar `True`). Se faltar sympy ou numpy, não instale nada: diga no relatório e siga.
- **Copie, não importe.** Copie o kit da unidade do EP. 02 (`videos_longos/yt_0027_*`: `kit.py`, `v7.py`, o fundo e o filtro de clareira). Se ele não estiver no seu checkout, copie do EP. 01 (`videos_longos/yt_0026_funcoes_vetoriais_campos/`: `kit.py`, `v7.py`, `render.sh`). Não altere as outras unidades.
- Use o que já existe: `campo7` (setas comprimidas), `seta7`, `placa_min`, `TC`/`TX` com caneta, `painel`, o canto de duas linhas e o fundo milimetrado parado (`assets/calculo/`).
- Render por bloco (`render.sh <Classe>`, 540p/15) e depois concatene. Nada de `always_redraw` com `MathTex`. Quadradinhos andam com o **fluxo exato** (`ApplyPointwiseFunction`/`Homotopy`), uma vez só.

## 3. Sistema visual (o aprovado do EP. 01 e do EP. 02, sem novidade)

### 3.1 Layouts e escala

| layout | geometria a 1080p | blocos |
|---|---|---|
| **A · palco + fórmulas** | origem do palco em (600, 540) px, **1 u = 120 px**; coluna de fórmulas alinhada à esquerda em **x = 1120** (no B4-3, x = 1090) | H, B2, B4-3, B5, B6, B7-3/4, S |
| **B · dois painéis** | painéis 700×560 em x 130–830 e 1090–1790, y 260–820, só a moldura (`#B8C4DA` a 35 %, raio 14). **Neste vídeo, 1 u = 140 px nos dois painéis** (escala comum entre eles). Origem do painel esquerdo em (480, 540); a origem comum da direita está no alvo de cada cena. Nomes **embaixo** dos painéis, em y = 868: `ONDE VOCÊ ANDA` e `ONDE A SETA CHEGA` (SGM 28, GEO). Fórmula ou números em y ≈ 955 | B1, B4-1, B4-2 |
| **C · três cartões** | 480×460 em x = 140, 720 e 1300, y 250–710, 1 u = 56 px; título em y = 760–775, legenda e fórmula embaixo | B3, B7-1/2 |

Conversão para o Manim: x_m = (x_px − 960)/135; y_m = (540 − y_px)/135.

### 3.2 Setas, objetos e textos

- **Seta de campo:** só a flecha, com haste de 5 px e ponta de 19 px, opaca. Comprimento comprimido L = Lmax·(0,4 + 0,6·t), com t = min(1, |F|/mmax) e Lmax = 0,84 × passo. Cor de `#2EE6A0` a `#8CFFD2` pela intensidade. Em contexto: `#1A5F55`, opaco.
- **Exceção (só o campo das diagonais G):** o comprimento é **proporcional**, L = Lmax·|G| (|G| ≤ 1). Sobre os eixos **não há seta nenhuma**, e isso é o conteúdo. Setas com menos de 6 px não são desenhadas.
- **R1 · Clareira:** toda seta de campo cujo centro caia a menos de 0,25 u de um rótulo, ponto, disco, quadradinho (pelo **polígono**, não pela caixa) ou caminho tracejado **não é desenhada** enquanto o objeto está ali.
- **R2 · Placa:** todo rótulo solto usa `placa_min` (`#091226` a 85 %, 4–6 px).
- **R3:** fórmula nova nunca nasce sobre fórmula velha.
- **R4:** rótulo de contador fica junto do objeto.
- **R5:** QA automático de sobreposição em cada gatilho (§9).
- **Pedacinho de fluido (v1.1):** chapa opaca `#663A4C`, contorno coral 4 px e uma **malha 4×4** (3 linhas em cada direção, `#FFB3BC`, 2 px) que é transformada pelo **mesmo fluxo** do quadradinho. Na prática, é um `VGroup` (chapa + linhas + contorno) passado inteiro ao `ApplyPointwiseFunction`/`Homotopy`, e as linhas devem ter pontos suficientes para curvar se o fluxo não for linear. As células mostram a deformação (retângulos, losangos) e a orientação mostra o giro. O fantasma do estado inicial continua só o contorno tracejado, sem malha. Vale para todo quadradinho: H, B6-4/5, B7-1/3/4 e S.
- Proibido: partículas ou pontinhos, laços (cada movimento roda **uma vez**, com o estado inicial em fantasma tracejado), lupa com linhas de chamada, brilho, contorno ou transparência em seta, sombra, barra, e qualquer efeito que não esteja no alvo.
- Parado no máximo 3 s. Se a fala continuar e a cena tiver acabado, o próximo passo entra mais cedo; nunca preencha com efeito.

### 3.3 Cores

| Papel | Cor |
|---|---|
| Campo, setas, P, Q, F⃗, G⃗, L⃗ | verde-menta `#2EE6A0 → #8CFFD2`; contexto `#1A5F55` |
| x, ∂x, h, **seta ∂F/∂x**, curva da ponta andando em x, reta horizontal do caminho | âmbar `#FFC24D` |
| y, ∂y, k, **seta ∂F/∂y**, curva da ponta andando em y, reta vertical | magenta `#EA63FF` |
| Ponto P, ponto X, **disco δ** (contorno 3 px) e a letra δ | laranja `#E08A3C` |
| **Disco ε** (contorno 3 px), a letra ε e a curva das pontas | `#8CFFD2` |
| Quadradinho (pedacinho de fluido) | chapa `#663A4C` (coral misturado 62 % com o fundo, opaca) + malha interna `#FFB3BC` 2 px + contorno coral `#FF7A8A` 4 px; fantasma tracejado coral 3 px |
| rot e GIRA | violeta `#9C8CFF` |
| div e MUDA DE ÁREA | azul-claro `#7FB2FF` |
| **Deformação** (DEFORMA, DEFORMAÇÃO, os dois números) | **lima `#C6F26B`** (cor nova, em teste; o Kaio aprovou testar) |
| Caminhos tracejados, origem comum, fantasma da seta F(P) no B4-2 | GEO `#B8C4DA` |
| Carga do cartão do meio | azul `#267BFF` com `+` |

Operadores (lim, ∂, ‖ ‖, rot, div) ficam brancos. A cor vai na grandeza.

### 3.4 Álgebra

- **Caneta** em toda fórmula nova: traço finíssimo, glifo a glifo, da esquerda para a direita, preenchendo na cor da grandeza, sem flash nem preview.
- Termo que nasce no desenho **voa** para a fórmula (`TransformFromCopy`, arco).
- Conta que continua a anterior usa `TransformByGlyphMap` (lista no §5).
- Alturas: fórmula principal de 48–52 px no alvo; secundária de 36–44 px. Nada menor que 30 px (só a linha do campo no B4-3, que é referência).
- Fórmulas **ficam** na tela enquanto a cena dura.

## 4. Os campos (números conferidos no sympy)

| Nome | Campo | Usado em |
|---|---|---|
| gancho | `F = (x, −y)` | H, B7-3 |
| campo da aula | `F = (1 + sen x − sen y, 2 sen x + 2 − cos x − cos y)`, ponto P = (0, 0) | B1, B3 (cartão 1), B4, B6, S |
| campo das diagonais | `G = (2xy/(x² + y²), 0)`, com `G(0,0) = (0,0)` | B2, B3 (cartão 3), B5 |
| campo da carga | `E = (x, y)/(x² + y²)^{3/2}` | B3 (cartão 2) |
| tijolos | `(−y, x)`, `(x, y)`, `(x, −y)`, `(y, x)` | B7 |

Números:
- **Campo da aula em P:** F(P) = (1, 0); ∂F/∂x = (cos x, 2cos x + sen x) = **(1, 2)**; ∂F/∂y = (−cos y, sen y) = **(−1, 0)**; J = [[1, −1], [2, 0]]; rot 3, div 1, deformações 1 e 1.
- **ε-δ:** ε = 1 → δ = 0,41; ε = 0,5 → δ = 0,21 (o maior δ é 0,416 e 0,212; use os valores arredondados para baixo).
- **Quociente em x:** h = 1: (0,84; 2,14) · 0,5: (0,96; 2,16) · 0,2: (0,99; 2,09) · 0,1: (1,00; 2,05) → (1, 2).
- **Quociente em y:** k = 1: (−0,84; 0,46) · 0,5: (−0,96; 0,25) · 0,2: (−0,99; 0,10) · 0,1: (−1,00; 0,05) → (−1, 0).
- **Curvas da ponta:** andando em x, (1 + sen s, 2 sen s + 1 − cos s), com s ∈ [−0,75; 1]. Andando em y, (1 − sen s, 1 − cos s), um **círculo** de centro (1, 1) e raio 1, com s ∈ [−1,25; 1,6].
- **Curva das pontas no B1:** F(P + δ(cos θ, sen θ)), com θ de 0 a 2π (exata, pela função original). **Não rotular como elipse:** ela só se parece com uma, e a fala não usa a palavra.
- **G:** na reta y = mx, G = (2m/(1 + m²), 0). ∂G/∂x(0,0) = ∂G/∂y(0,0) = 0⃗.
- **Zoom do B6:** no B6-1/B6-2, o campo residual `R(X, Y) = 10·[F(P + (X, Y)/10) − F(P)]`, que é quase igual ao linear (erro ≤ 8 %). **Do B6-3 em diante**, o palco mostra o **modelo linear local** `J·(X, Y) = (X − Y, 2X)`, exato, com `Transform` único das setas, e o rótulo `MODELO LINEAR LOCAL` (SGM 26, GEO, com placa) ao lado de `ZOOM × 10`, na faixa de cima (as setas do palco vão só até y = 2,5 nessas cenas). O quadradinho anda por e^{tJ}, que é o fluxo exato **desse modelo**, e não do campo original (a diferença no palco é de ~3 %, mas o rigor pede o rótulo).
- **Fluxos exatos:**
  - gancho: (x eᵗ, y e⁻ᵗ), quadradinho de lado 1,2 de t = 0 a 0,55 → 2,08 × 0,69, área 1,44 → 1,44;
  - tabela da aula: exp(tJ) = e^{t/2}[cos(ωt)·I + (sen(ωt)/ω)·(J − I/2)], com ω = √7/2; quadradinho [0; 1,2]² com a quina em P, de t = 0 a **0,35**, área × **1,42**;
  - (y, x): [[cosh t, senh t], [senh t, cosh t]], quadradinho de lado 1,2 de t = 0 a 0,55 (vira losango);
  - cartões do B7: giro de 0,6 rad, explosão × 1,42, (x, −y) × 1,5 e ÷ 1,5.

## 5. Cena a cena

Gatilho = a palavra da narração (Anexo A) em que a ação começa. **Alvo** = o quadro em `yt_0028_quadros_alvo_v1/`, reproduzido com tolerância de ±20 px na posição e ±5 % no tamanho.

### H · o quadradinho que deforma (layout A, canto sem linha 2) · alvo 01
- O palco tem o campo (x, −y) (mmax 3) e o quadradinho coral de lado 1,2 no centro.
- Coluna, na caneta: `\vec F = (x,\ -y)` em "Lembra do campo"; `rot F⃗ = 0` em "O rotacional dá zero"; `div F⃗ = 0` em "O divergente também".
- Em "deixa o fluido andar", o fluxo exato roda de 0 a 0,55 em ~2,5 s, com o fantasma tracejado. O rótulo `ÁREA 1,44 → 1,44` fica embaixo do retângulo, com placa (clareira).
- `MAS DEFORMA` (lima, Bold 48) entra em "Mas virou outra coisa", e `QUE NÚMERO MEDE ISSO?` (GEO) em "Que número".

### A · bem-vindos
Padrão do canal, com o título `LIMITE, CONTINUIDADE E DERIVADAS PARCIAIS` e `NESTE VÍDEO: CHEGAR PERTO · NÃO PULAR · MEDIR A MUDANÇA`.

### B1 · chegar perto (layout B) · alvos 02 e 03
- **B1-1** ("duas telas"): à esquerda, o campo da aula em contexto (passo 0,5) e o ponto P laranja; à direita, a origem comum (ponto GEO de 6 px) e a seta F(P) = (1, 0) em `#8CFFD2`, 7 px. Os nomes dos painéis entram embaixo.
- **B1-2** ("conforme você chega perto"): o ponto X sai de (1,4; 0,9) e anda **uma vez** até P, por um arco. A seta de X fica acesa no painel esquerdo (verde claro, 7 px), e no direito a seta F(X), levada para a origem comum, se mexe até coincidir com F(P).
- **B1-3** ("disquinho de raio épsilon"): entra o disco ε = 1 em volta da ponta de F(P). Em "disquinho de raio delta", entra o disco δ = 0,41 em volta de P. Em "dá a volta na borda", X dá **uma** volta no disco δ (~3 s), e a ponta desenha a curva das pontas (traço fino `#8CFFD2`), que fica dentro do disco ε. Embaixo, na caneta: `ε = 1 ⇒ δ = 0,41`. **Alvo 02.**
- **B1-4** ("aperta para meio"): ε encolhe para 0,5 e δ para 0,21, juntos (~1,5 s). A curva das pontas é redesenhada e a linha de baixo vira `ε = 0,5 ⇒ δ = 0,21` (`TransformByGlyphMap`).
- **B1-5** ("Escrito, é exatamente essa frase"): a linha de baixo sai e a definição entra na caneta, em uma linha de 40 px. **Alvo 03.**
- **B1-6** ("um atalho"): a definição se transforma em `\lim \vec F = \vec L \iff \lim P = L_1 \text{ e } \lim Q = L_2`. Em "repara na curva", a curva das pontas continua na tela (sem pulso e sem rótulo de elipse).

### B2 · quando o limite não existe (layout A) · alvo 04
- O palco tem o campo G (proporcional), com a origem limpa.
- Coluna: `\vec G = (2xy/(x^2+y^2),\ 0)` em "campo encrenqueiro".
- Três caminhos, um de cada vez, em GEO tracejado, cada um com a sua clareira (0,2 u): semieixo x positivo, diagonal y = x (do 1º quadrante) e diagonal y = −x (do 2º).
- Em cada um, o ponto laranja anda **uma vez** até perto da origem, carregando a sua seta (verde claro, 8 px): nenhuma seta (rótulo `0⃗`), `(1, 0)` e `(−1, 0)`. Os rótulos ficam com placa.
- Coluna: `NA RETA y = m x:` e `\vec G = (2m/(1+m^2),\ 0)` em "Fazendo a conta"; depois `m = 0 → 0 · m = 1 → 1 · m = −1 → −1` e `NÃO EXISTE O LIMITE EM (0, 0)` em "Então não existe".

### B3 · continuidade (layout C) · alvo 05
- Os três cartões entram um por vez, nos gatilhos "No primeiro", "No segundo" e "No terceiro":
  - **CONTÍNUO**: campo da aula, disco laranja e ponto P;
  - **FORA DO DOMÍNIO**: campo da carga, carga azul `+` e anel tracejado vazio;
  - **DESCONTÍNUO**: G, ponto P na origem e `G(0,0) = 0⃗` com placa.
- Legendas embaixo, iguais ao alvo.
- A definição da continuidade entra embaixo em "quando o limite ali existe e é igual", e `CONTÍNUA ⇔ CADA COMPONENTE É CONTÍNUA` em "de novo, dá para trabalhar por componentes".

### B4 · derivada parcial · alvos 06, 07 e 08
- **B4-1 (layout B, em x) · alvo 06:**
  - À esquerda: a reta horizontal âmbar tracejada pelo P e o ponto P + h.
  - À direita: F(P) (7 px), F(P + h) (5 px), a corda entre as pontas (âmbar, 4 px) e o quociente ΔF/h saindo da ponta de F(P) (âmbar, 8 px).
  - h vai de 1 → 0,5 → 0,2 → 0,1, em degraus de ~1 s. Os números entram embaixo, um por degrau (no alvo estão três e o limite).
  - Em "a ponta da seta desenha uma curva", a curva âmbar é traçada (s ∈ [−0,75; 1]) e a tangente GEO tracejada aparece. O quociente termina **sobre** a tangente: é ∂F/∂x = (1, 2), que ganha rótulo.
- **B4-2 (layout B, em y) · alvo 07:** o mesmo em magenta. Aqui F(P) vira fantasma GEO de 3 px, porque o quociente aponta de volta sobre ela. A curva é o círculo. O alvo mostra k = 1 (corda = quociente); depois k desce até 0,1 e o quociente fica tangente ao círculo, apontando para a esquerda: ∂F/∂y = (−1, 0).
- **B4-3 (layout A) · alvo 08:**
  - O palco tem o campo da aula em contexto. As setas ∂F/∂x = (1, 2) (âmbar, 8 px) e ∂F/∂y = (−1, 0) (magenta, 8 px) **voam** das tangentes do B4-1/B4-2 para o P do palco.
  - Coluna (x = 1090), em cinco linhas na caneta:
    1. a definição;
    2. `∂F/∂x = (∂P/∂x, ∂Q/∂x)`;
    3. `= (cos x, 2cos x + sen x) = (1, 2)`, em que o último termo entra por `TransformByGlyphMap` no gatilho "no ponto, um e dois";
    4. `∂F/∂y = (…)`;
    5. `= (−cos y, sen y) = (−1, 0)`.
  - A linha do campo fica embaixo, em 30 px.

### B5 · o engano (layout A) · alvo 09
- O palco tem o G. Em "Andando pelo eixo horizontal", a reta horizontal âmbar (4 px) acende sobre o eixo; em "Pelo eixo vertical", a magenta. Elas ficam onde não há setas.
- Coluna: `∂G/∂x(0,0) = 0⃗` e `∂G/∂y(0,0) = 0⃗` na caneta.
- Em "esse campo esconde tudo nas diagonais", as setas das duas diagonais ficam verde claro, 7 px. Entram `AS PARCIAIS SÓ OLHAM DUAS RETAS` e `E G NEM É CONTÍNUO EM (0, 0)`.
- Em "classe cê um", entram `CLASSE C¹ (PARCIAIS CONTÍNUAS) ⇒` e a fórmula da aproximação.

### B6 · a tabela (layout A) · alvos 10, 11, 12 e 13
- **B6-1** ("dez vezes mais perto"): o campo da aula no palco faz zoom × 10 em volta de P. A transição troca a grade de setas por uma nova, avaliada em P + (X, Y)/10, com `Transform` único. Todas as setas ficam quase iguais a (1, 0) (comprimidas, mmax 6 nesta etapa). Entra o rótulo `ZOOM × 10` com placa.
- **B6-2** ("tira a seta do centro") · **alvo 10:** cada seta vira o campo residual R, com `Transform` único. O centro fica sem seta. Coluna: `F(P+H) − F(P) ≈ h ∂F/∂x + k ∂F/∂y` e as duas legendas.
- **B6-3** ("coloca as duas lado a lado") · **alvo 11:** o campo vira contexto. As setas ∂F/∂x e ∂F/∂y do B4-3 voltam pequenas e **voam** para as colunas da matriz `J_F(P)`, que é escrita com ∂x âmbar e ∂y magenta. Depois, `TransformByGlyphMap` para `= (1 −1; 2 0)`, com a 1ª coluna âmbar e a 2ª magenta. Entram `MATRIZ JACOBIANA` (Bold 40) e a legenda das colunas.
- **B6-4** ("Coloca um quadradinho") · **alvo 12:** a matriz sobe e encolhe para a forma `J = (…)` do alvo. O quadradinho coral [0; 1,2]² entra com a quina inferior esquerda em P. Na quina da direita, a seta âmbar (0,4; 0,8); na quina de cima, a seta magenta (−0,4; 0). São as colunas × 0,4: **direção certa, tamanho de exibição**. Entram `AS COLUNAS EMPURRAM AS ARESTAS` e as duas legendas coloridas.
- **B6-5** ("Solta o fluido") · **alvo 13:** as duas setas saem, e o quadradinho anda pelo fluxo do modelo linear (e^{tJ}) de t = 0 a 0,35 (~2,5 s), com o fantasma tracejado. A clareira acompanha o polígono. Entram `ÁREA × 1,42` (placa, junto do quadradinho) e `GIRA · CRESCE · ENTORTA`.

### B7 · quatro números, quatro medidas · alvos 14 a 17
- **B7-1 (layout C) · alvo 14:**
  - Os cartões entram um por vez, cada um com o seu quadradinho fazendo o movimento **uma vez**:
    - `GIRA` em "O giro vem";
    - `MUDA DE ÁREA` em "A mudança de área";
    - `DEFORMA` em "As outras duas são a deformação".
  - As fórmulas entram embaixo, na caneta, no gatilho de cada uma.
  - No cartão DEFORMA, o campo troca de (x, −y) para (y, x) (setas com `Transform`, o quadradinho vira losango) em "entre as duas diagonais".
- **B7-2 · alvo 15:** em "No nosso ponto", os valores entram embaixo de cada fórmula, na ordem rot, div, deformações. `4 NÚMEROS ENTRAM, 4 MEDIDAS SAEM` entra no alto (y = 205) em "Quatro números entram".
- **B7-3 (layout A) · alvo 16:** o palco do gancho volta com o retângulo final. Coluna: `J = (1 0; 0 −1)`, `rot = 0 · div = 0` e `DEFORMAÇÃO: 2 e 0` (lima), em "a primeira deformação vale dois". As legendas `É TUDO DEFORMAÇÃO` e `ESTICA NO x · ACHATA NO y` entram embaixo.
- **B7-4 (layout A) · alvo 17:** em "um deles é este", o palco troca para (y, x), e o quadradinho de lado 1,2 vira losango pelo fluxo exato (0 → 0,55). Coluna: `F = (y, x)`, `J = (0 1; 1 0)`, `rot = 0 · div = 0`, `DEFORMAÇÃO: 0 e 2` e `O MESMO, GIRADO DE 45°`. Em "quem achou um de segundo grau", entra `TAMBÉM VALE: (x² − y², −2xy)` com placa, por ~3 s.
- **B7-5:** cortado na v1.2. A ligação entre a curva do B1 e a deformação mistura duas leituras do campo (como transformação e como velocidade), e a frase "círculo vira círculo só sem deformação" é falsa (uma reflexão leva círculo em círculo). Do B7-4, vá direto ao S.

### S · resumo e CTA (layout A) · alvo 18
- O palco mostra o campo residual em contexto e o quadradinho final do B6.
- Coluna: a matriz e, uma por gatilho do resumo, `rot = 3` (violeta), `div = 1` (azul-claro) e `deformação = 1 e 1` (lima).
- **Não repetir os cartões.**
- CTA padrão do canal (logo, anéis, INSCREVA-SE) em "No próximo vídeo".

## 6. Narração (para o tempo do preview)

O preview é silencioso, mas cada bloco dura o tempo estimado da fala do Anexo A, a ~2,8 palavras/s. Gere um `duracoes_estimadas.json` por bloco e trecho, como no yt_0026. A fala tem ≈ 2.000 palavras (≈ 12 min); com as cenas se esticando, o preview deve ficar em 12–13 min. **Não gerar voz.**

## 7. O que NÃO fazer

- Nenhum 3D, nenhuma partícula, nenhuma lupa, nenhum laço, nenhum brilho, contorno ou transparência em seta, nenhuma sombra ou barra.
- Não usar `ThreeDScene`.
- Não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md` nem nas unidades yt_0026 e yt_0027.
- Não citar livro nem o Atlas na tela.
- Não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

## 8. QA do preview (obrigatório antes de entregar)

1. **Render × alvo:** um still em cada um dos 18 gatilhos, tirado quando o estado do alvo está completo (fora de escrita ou transição) e comparado na mesma resolução (alvo reduzido a 960×540, tolerância de 10 px nessa escala) e a prancha `comparacao_v1.jpg` (render à esquerda, alvo à direita). Diferença de posição ≤ 20 px, de tamanho ≤ 5 %, mesmo texto e mesmas cores. Toda diferença acima disso precisa de justificativa no relatório.
2. **R5 · sobreposição:** em cada gatilho, as caixas de todo texto e `MathTex` não se cruzam entre si, e nenhum texto cruza uma seta de campo visível, medindo a **seta inteira** (haste e ponta, + 4 px), não só o centro. Se sobrar alguma ocorrência, liste-a com o motivo; não force o zero. Relatório em `sobreposicoes_v1.txt`, com zero ocorrências esperadas.
3. **Flash por quadro = 0:** nenhuma fórmula aparece inteira antes da caneta.
4. **Parado ≤ 3 s** (`qa_parado.py` do yt_0026).
5. **Números:** confira na tela os valores do §4 (δ, quocientes, matrizes, áreas).

## 9. Parada

Entregue o preview, a prancha, os dois relatórios e o relatório de entrega. Pare e não inicie voz nem 1080p.

---

## Anexo A · Narração canônica (com tags do ElevenLabs v4)

Uma tag por trecho, em inglês, valendo até a próxima. Sem `[slowly]` e sem `[pause]`. Nenhuma letra solta. Épsilon e delta são ditos pelo nome.

### H · O quadradinho que deforma

[curious] Lembra do campo que fechou o episódio passado? A componente horizontal é a própria coordenada horizontal, e a vertical é menos a coordenada vertical. Coloca um quadradinho de fluido no meio e faz as contas que a gente já conhece. O rotacional dá zero, em todo ponto: nenhuma rodinha gira. O divergente também dá zero: nenhum pedacinho muda de área.

[thoughtful] Então, pelas duas medidas, não acontece nada. Só que agora deixa o fluido andar… e o quadradinho estica para os lados e achata na vertical. A área continua a mesma, e ele não girou nem um grau. Mas virou outra coisa.

[curious] Então tem alguma coisa nesse campo que o rotacional e o divergente não enxergam. Que número mede isso? E de onde ele sai? A resposta está nas derivadas parciais do campo. Só que, para usar essas derivadas com segurança, a gente precisa começar pelo chão: o que quer dizer chegar perto de um ponto.

### A · Bem-vindos

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab. Hoje são três ideias que se apoiam uma na outra: limite, continuidade e derivadas parciais de um campo vetorial. E, no fim, a gente vai juntar tudo numa tabela de quatro números que mostra, bem de perto, como o campo muda em volta de um ponto.

### B1 · Chegar perto

[thoughtful] Vamos usar duas telas. Na da esquerda está o campo, e é ali que você anda: você escolhe um ponto e vai se aproximando dele. Na da direita, eu pego cada seta e trago para a mesma origem, para comparar só onde a ponta dela chega.

[curious] Repara: conforme você chega perto do ponto, a ponta da seta chega perto da ponta da seta do ponto. É isso que o limite quer dizer. Mas "perto" precisa de um número. Então funciona como um desafio. Alguém escolhe uma tolerância lá na chegada: um disquinho de raio épsilon em volta da ponta. E você precisa responder com um disquinho de raio delta em volta do ponto, de um jeito que todo mundo que estiver dentro do seu disco mande a ponta da seta para dentro do disco dele.

[thoughtful] Com épsilon igual a um, um delta de zero vírgula quatro um já resolve: dá a volta na borda do disco e a ponta não sai do disco da chegada. Se o desafio aperta para meio, você aperta também, para zero vírgula dois um. O limite existe quando você sempre consegue responder, por menor que seja o épsilon. Escrito, é exatamente essa frase: para todo épsilon positivo existe um delta positivo tal que, se a distância até o ponto é maior que zero e menor que delta, a distância da seta até o limite é menor que épsilon. E repara nesse maior que zero: o próprio ponto fica de fora. O limite só olha para quem está chegando, e isso vai fazer diferença daqui a pouco.

[curious] E tem um atalho muito bom. Uma seta está perto de outra exatamente quando cada componente está perto da componente correspondente. Então o limite de um campo existe quando o limite de cada componente existe, e aí é só fazer o limite de funções de várias variáveis que você já conhece. E repara na curva que a ponta desenhou quando você deu a volta no disco: ela não é um círculo. A seta muda mais depressa numa direção do que em outra. E medir essa mudança, direção por direção, é exatamente o trabalho das derivadas parciais.

### B2 · Quando o limite não existe

[curious] Agora um campo encrenqueiro. Todas as setas são horizontais. Nos eixos, não tem seta nenhuma; nas diagonais, as setas têm tamanho um: numa delas apontam para a direita, na outra, para a esquerda.

[thoughtful] Vem andando até a origem pelo eixo horizontal: a seta é zero o caminho todo. Agora vem pela diagonal de subida: a seta é um, para a direita, o caminho todo. E pela outra diagonal: um, para a esquerda. Em cada reta que passa pela origem, o campo é constante, e cada reta tem a sua constante. Fazendo a conta numa reta qualquer pela origem, o campo vale o dobro da inclinação, dividido por um mais a inclinação ao quadrado. Muda a reta, muda o valor.

[thoughtful, emphatic] Então não existe limite na origem. Não tem disquinho em volta da origem que mande todas as pontas para perto de uma seta só. E fica um cuidado importante: dois caminhos dando valores diferentes provam que o limite não existe. Mas todas as retas darem o mesmo valor ainda não provam que ele existe, porque dá para chegar por uma curva.

### B3 · Continuidade

[thoughtful] Agora a continuidade. Um campo é contínuo num ponto do domínio quando o limite ali existe e é igual à própria seta do ponto. Na prática: chegando perto, a seta não dá salto.

[curious] Olha três casos. No primeiro, o nosso campo de antes: em volta do ponto, as setas vizinhas são parecidas com a do ponto. Contínuo. No segundo, o campo elétrico de uma carga. Em cima da carga, o campo nem existe: a pergunta "é contínuo ali?" nem se faz, porque continuidade só se pergunta em ponto do domínio. Em todo o resto, ele é contínuo. No terceiro, o campo encrenqueiro, agora definido na origem como zero. Ali ele existe, mas não tem limite. Isso, sim, é descontínuo.

[thoughtful] E, de novo, dá para trabalhar por componentes: o campo é contínuo exatamente quando cada componente é contínua. Por isso quase todo campo que vem de fórmula é contínuo onde está definido, porque somas, produtos, quocientes com denominador diferente de zero e composições de funções contínuas continuam contínuas.

### B4 · Derivada parcial de um campo

[thoughtful] Agora sim: medir como a seta muda. Fica no ponto e anda só na horizontal, um passo pequeno. A seta muda de uma para outra, e a diferença entre as duas é um vetor. Divide esse vetor pelo tamanho do passo e encolhe o passo. Esse limite é a derivada parcial do campo na direção horizontal.

[curious] Olha os números. Com passo um, o quociente vale zero vírgula oito quatro e dois vírgula um quatro. Com meio, zero vírgula nove seis e dois vírgula um seis. Com passo cada vez menor, ele vai chegando em um e dois. E repara no que acontece lá na tela da chegada: andando na horizontal, a ponta da seta desenha uma curva. A derivada parcial na direção horizontal é exatamente a seta tangente a essa curva, a velocidade da ponta quando você anda na horizontal com velocidade um.

[thoughtful] Agora na vertical. Andando para cima, a ponta da seta anda num círculo. E o quociente vai chegando em menos um e zero: a derivada parcial na direção vertical aponta para a esquerda, tangente ao círculo.

[thoughtful, emphatic] Então a derivada parcial de um campo não é um número: é um vetor, e ele diz como a seta muda quando você anda numa direção. E a conta é por componentes: derivada da componente horizontal e derivada da componente vertical. Aqui, a derivada na direção horizontal dá cosseno e dois cossenos mais seno, todos da coordenada horizontal; no ponto, um e dois. A derivada na direção vertical dá menos cosseno e seno da coordenada vertical; no ponto, menos um e zero. A conta bate com o desenho.

### B5 · O engano

[curious] Só que tem uma armadilha. Volta no campo encrenqueiro. Calcula as derivadas parciais na origem. Andando pelo eixo horizontal, a seta é zero o tempo todo, então a derivada na direção horizontal é zero. Pelo eixo vertical, mesma coisa: a derivada na direção vertical é zero. As duas existem, e as duas são zero.

[thoughtful] Quem olhasse só para essas duas derivadas ia achar que, perto da origem, o campo quase não muda. E ele nem é contínuo ali! As derivadas parciais só olham duas retas, a horizontal e a vertical, e esse campo esconde tudo nas diagonais.

[thoughtful, emphatic] Por isso aparece a condição de classe cê um: as derivadas parciais existem e são contínuas. Com ela, aí sim, as parciais contam a história inteira perto do ponto: a seta num ponto vizinho é a seta do ponto, mais o passo horizontal vezes a derivada na horizontal, mais o passo vertical vezes a derivada na vertical, com um erro que some mais rápido que o passo. O nosso campo, feito de senos e cossenos, é cê um. O encrenqueiro, não.

### B6 · A tabela

[curious] Então vamos usar isso. Pega o campo da aula e chega bem perto do ponto, dez vezes mais perto. De perto, todas as setas ficam quase iguais à seta do centro. Agora tira a seta do centro de todas elas. O que sobra é só a mudança… e olha que campo arrumadinho apareceu.

[thoughtful] Bem de perto, essa mudança é escrita com as duas derivadas parciais. Então coloca as duas lado a lado, como colunas: a derivada na horizontal na primeira e a derivada na vertical na segunda. Fica uma tabela de quatro números, com as derivadas das duas componentes nas duas direções. Ela tem nome: matriz jacobiana. No nosso ponto, ela vale um e menos um em cima, dois e zero embaixo.

[curious] E agora a parte bonita. Usa essa tabela como modelo do campo bem pertinho do ponto e coloca um quadradinho com a quina no ponto. A quina da direita está um passo para o lado, então ela é empurrada pela primeira coluna. A quina de cima está um passo para cima, então é empurrada pela segunda coluna. Cada coluna da tabela empurra uma aresta. Solta o fluido no modelo… e o quadradinho gira, cresce e entorta, tudo ao mesmo tempo. Tudo isso estava guardado nos quatro números.

### B7 · Quatro números, quatro medidas

[thoughtful] E dá para separar essa bagunça. O giro vem de uma combinação da tabela: a derivada da componente vertical na horizontal, menos a da componente horizontal na vertical. É o rotacional. A mudança de área vem de outra: a soma das duas derivadas da diagonal da tabela. É o divergente.

[curious] Só que a tabela tem quatro números, e até agora a gente usou duas combinações. As outras duas são a deformação. A primeira é a derivada da componente horizontal na horizontal, menos a da vertical na vertical: ela diz quanto o pedacinho estica no horizontal mais do que no vertical. A segunda é a derivada da componente vertical na horizontal, mais a da horizontal na vertical: ela faz a mesma comparação, só que entre as duas diagonais.

[thoughtful, emphatic] No nosso ponto: rotacional três, divergente um, e deformação um e um. Quatro números entram, quatro medidas saem, e nada se perde no caminho. Bem de perto e sem a seta do centro, todo campo cê um se comporta como uma mistura de quatro campos simples: um redemoinho, uma explosão e duas deformações. E isso não é só matemática: num fluido, o atrito viscoso vem da deformação. Um bloco de fluido girando inteiro, rígido, não tem atrito viscoso nenhum por dentro.

[curious] Agora volta lá no começo. No campo que esticava o quadradinho, a tabela é um e zero em cima, zero e menos um embaixo. Rotacional zero, divergente zero, e a primeira deformação vale dois. É tudo deformação: estica na horizontal e achata na vertical, na mesma medida.

[happy] E lá no episódio passado ficou um desafio: achar outro campo, que não fosse constante, com rotacional e divergente zero. Um deles é este, que troca as coordenadas de lugar. A tabela dá zero e um em cima, um e zero embaixo. Agora quem vale dois é a segunda deformação: o quadradinho estica numa diagonal e achata na outra. É o mesmo campo de antes, girado quarenta e cinco graus. E quem achou um de segundo grau, como o da tela, também acertou.

### S · Síntese e encerramento

[thoughtful] Então, resumindo a aula: limite é chegar perto e a seta chegar perto também. Continuidade é a seta não dar salto. A derivada parcial diz como a seta muda numa direção. E, quando essas derivadas são contínuas, as quatro juntas descrevem como o campo muda bem perto do ponto: giro, área e deformação.

[excited] No próximo vídeo, a gente coloca o módulo inteiro para trabalhar em exercícios: campo vetorial, rotacional, divergente, limite e derivadas parciais, tudo junto. Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual dessas quatro medidas você acha que aparece mais na física? Até a próxima!
