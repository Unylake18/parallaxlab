# yt_0037 · CÁLCULO III · EP. 12 · Coordenadas polares na integral dupla
# AVALIAÇÃO DO PREVIEW v1 + HANDOFF v2 · preview silencioso (540p, 15 fps)

2026-11-14. Produção → Claude Code. Este documento é **autocontido**. Ele vale junto com:
- o handoff v1, que continua na unidade como `handoff_v1.md`;
- a pasta `calculo3_34t2_quadros_alvo_v2/` (os 9 alvos do v1, que continuam valendo onde este documento não os troca);
- a pasta nova `yt_0037_alvos_handoff_v2/`, que traz:
  - 6 alvos novos `v2_01` … `v2_06` e a folha `00_folha_contato_alvos_handoff_v2.jpg`;
  - `erros_v1/`: os **42 quadros do v1** com os defeitos desta avaliação, nomeados `E<nn>_<tempo>s_<bloco>_<defeito>.jpg`;
  - `c3d34t2.html` com a **cena 3D nova `casca`** e `sb34t2.html` com as chaves novas (`v2casca`, `v2erro`, `v2gauss`, `v2quad`, `v2sint`, `v2gancho`). Para rodar, copie os arquivos desta pasta por cima de `calculo3_34t2_quadros_alvo_v2/` (os dois usam o katex, as fontes e o logo de lá).

Onde este documento e o v1 divergirem, **vale este**.

Fase aberta: **preview visual silencioso v2**. Sem voz, SRT, 1080p, master, entrega, commit ou push.

O pedido do Kaio, nas palavras dele: *"tem que melhorar mtmt o visual, tem horas que aparece errado o 2pir*e, ele circula metade da circunferencia so na animação, tem mt melhorias de didatica, legibilidade, mftools, visual, animações, sobreposições tem umas 32"*.

---

## 0. O que entregar

1. A mesma unidade `videos_longos/yt_0037_coordenadas_polares/`, com as mudanças deste documento.
   - Antes de mexer, copie o v1 para `renders/v1/`. Não apague nada do v1.
2. `renders/v2/yt_0037_preview_v2_540p15.mp4`: 960×540, 15 fps, sem áudio, no tempo da **narração v2.1** (§5, total ≈ 16:01).
   - Todas as seções mudam. Rerrenderize seção por seção e remonte.
3. `renders/v2/qa/`: tudo o que o §7 pede, **inclusive a prancha antes × depois dos 42 erros**.
4. A prancha render × alvo: os 9 alvos do v1 que continuam (01, 02, 03, 05, 07; o 04 só na metade de cima; o 06 só no B4-1; o 08 só no B6-1; o 09 é trocado pelo `v2_06`) e os 6 alvos `v2_*`.
5. O relatório de entrega do AGENTS.md.

---

## 1. Avaliação do v1

**O que o v1 acertou e não muda:**
- o sistema visual: fundo violeta, grade `papel(ax)`, canto em duas linhas, cores por grandeza, `r` do jacobiano em lima;
- a ordem e o conteúdo dos blocos, e a conta inteira (`conta_inteira_v1.txt` está certo);
- o teorema em duas metades (B3-1), com o corte e a origem em ALERTA;
- a tabela do confronto (B6-2), com os valores certos;
- o pouso 3D → 2D do `gauss` e o cartão `√π ?` no canto;
- o tempo total, colado na narração (917 s).

**O que falhou.** O v1 cumpre o roteiro, mas a tela não está no nível da série:
1. **Legibilidade.** As fórmulas da coluna têm algarismo com ~22 px de altura a 1080p (medido em `r = 0 → u = 0`, B4-1), e as legendas também ~22 px. Os rótulos do palco (`a`, `a√2`, `D_a`, `θ = π/3 ⇒ r = 1`) ficam em 16–24 px. Num celular, nada disso se lê.
2. **Palcos pequenos.** Os discos do H1 têm raio de ~250 px; o disco do B5 tem ~190 px (o alvo pede 285); o palco do B6-3 e do B7 ocupa metade do que pode; o S1 deixa o centro vazio.
3. **O B4-2 está errado** (as duas queixas do Kaio):
   - em 532 s um **anel laranja flutua no topo da tela**, sobre o canto (E18);
   - em 533 s a parede aparece cinza e uma **placa escura vazia** fica sobre ela (E19);
   - em 540 s o contorno lima no chão faz **só meia circunferência, com um raio saindo do centro**, e um **blob lima** (o `2πr` em voo) cobre o rótulo (E20);
   - em 546 s `2π r · e^{−r²}` fica **sobre a base da parede** e `PAREDE DA CASCA` sobre a parede (E21);
   - e a conta da casca está **incompleta**: `2πr · e^{−r²}` é a área da parede, não o volume. Falta o `dr`, e a casca, sem espessura, parece um bolo inteiro.
4. **Esqueleto e caixas vazias** (pré-visualização do destino): operadores na tela antes dos termos (284, 724, 808 s), molduras e placas vazias antes do texto (64, 533, 836, 848 s).
5. **Glifos duplicados ou soltos depois dos voos e dos glyph maps** (MF-Tools): 208, 236, 404, 500, 540, 624, 664, 788, 800, 804, 808, 852 s. A conta fica embaralhada justamente quando a voz lê.
6. **Sobreposições.** Rótulo sobre eixo, curva ou superfície; rótulo cortado pela borda; legenda colada em fórmula. Somando os quadros de `erros_v1/`, são 42 defeitos: cerca de 26 de sobreposição, corte ou glifo duplicado, e 16 de palco vazio, palco parado, esqueleto ou caixa vazia.
7. **Palco parado e vazio**: H1 parado de 36 a 56 s; B3-1 quase parado de 340 a 400 s; palco vazio em 336, 448 e 648 s; metade da tela vazia no B7 (816–832 s).
8. **3D vazando**: o sino do `gauss` sai pela borda esquerda (708–720 s); a câmera mostra o `gauss` de cima, achatado, **antes** de subir (704 s).

**Por que o QA do v1 não pegou** (e o §7 corrige):
- `sobreposicoes_v1.txt` deu 0 porque **excluía** o 3D, o glifo em voo e os rótulos dos eixos contra os próprios eixos;
- `palco_parado_v1.txt` media "menos de 40 px mudando"; um cursor de sublinhado já passa disso;
- `palco_vazio` usava 300 px de diferença do fundo; o canto e o cartão `√π ?` já contam;
- `flash_por_quadro_v1.txt` só olhava "fórmula de caneta antes da vez", e não esqueleto, glifo duplicado nem caixa vazia.

---

## 2. Regras novas para o vídeo inteiro (G1–G8)

Medidas em px a **1080p** (no preview 540p, metade).

- **G1 · Tipografia mínima.** Meça a altura de um algarismo (`0` ou `1`) ou de uma maiúscula:
  - fórmula principal da coluna: **≥ 30 px** (v1: 22). No `sb34t2.html`, é o `tex(…, 44–52)`;
  - linha secundária (substituição, limites novos, tabela): **≥ 27 px** (`tex(…, 38–42)`);
  - rótulo matemático no palco (`a`, `a√2`, `D_a`, `r = sec θ`): **≥ 27 px**;
  - legenda Space Grotesk: **≥ 22 px de maiúscula** (fonte ≥ 30 px), e no máximo 6 palavras;
  - título de painel e cartão: fonte ≥ 32 px.
  - O alvo novo vence o v1: os alvos `v2_*` já estão nessa escala.
- **G2 · Coluna paginada.** No máximo **6 linhas de conta visíveis** e mais 1–2 chips no topo.
  - Quando a 7ª linha precisa entrar, as linhas de cima saem (`FadeOut` para cima, 0,4 s) e o resultado delas fica como chip.
  - A linha nova nasce no lugar livre, nunca sobre a velha (R3).
- **G3 · Palco grande.** O desenho (sem a coluna) ocupa **≥ 65 % da altura útil** (y de 180 a 1040) no layout A.
  - O 3D cabe inteiro na tela: a caixa dos pixels com alfa > 0 do PNG fica em x ∈ [40, 1010] e y ∈ [170, 1050].
  - Enquadre por `setViewOffset`/zoom, nunca cortando o PNG.
- **G4 · Nada antes da vez** (vale para fórmula, caixa, placa e chip):
  - em todo quadro, os glifos visíveis de uma fórmula em escrita formam um **prefixo na ordem de leitura**. O pouso de um voo conta como a escrita daquele glifo: a caneta **para antes** do lugar de um glifo que vai chegar voando e só continua depois do pouso;
  - moldura de chip, placa (`placa_min`) e painel **nascem junto com o texto ou depois dele**, nunca vazios;
  - nenhum glifo fica solto fora da caixa final da sua fórmula (o `∫.` de 788 s).
- **G5 · Voo e glyph map limpos (MF-Tools):**
  - o voo é um `TransformFromCopy` da fonte; ao pousar, **a cópia é o glifo** (`scene.remove` do alvo invisível + `add` da cópia, ou `ReplacementTransform` para o alvo oculto). Nunca dois objetos do mesmo glifo no destino;
  - depois de cada `TransformByGlyphMap`, a cena guarda **só** o MathTex de destino: confira `scene.mobjects` e remova a fonte e o que o `auto_fade` deixou;
  - um degrau por vez: o glyph map seguinte só começa quando o anterior terminou (sem `AnimationGroup` de dois glyph maps).
- **G6 · Rótulos (R1–R6 do v1, mais estas):**
  - folga **≥ 10 px** entre a caixa do rótulo e qualquer eixo, curva, aresta, borda de região ou ponto (o rótulo do eixo fica **na ponta**, fora da linha);
  - rótulo sobre o 3D só com `placa_min` e só se nomeia aquele objeto; senão, vai para fora com uma linha-guia fina (2–3 px) até o ponto;
  - nada a menos de **40 px da borda da tela**; nada cortado;
  - miniatura (o retângulo rθ, o triângulo) tem ≥ 200 px de altura e não carrega rótulo menor que G1.
- **G7 · Movimento:**
  - **palco vazio**: nunca, por mais de 0,5 s. Na troca de bloco, o palco novo começa a se desenhar no mesmo quadro em que o velho sai;
  - **palco parado**: nada parado por mais de **5 s**. De 3 a 5 s, só com a voz lendo a conta que se escreve na coluna;
  - a câmera 3D só se move nos gatilhos do texto.
- **G8 · Palavras (Space Grotesk):**
  - entram com `AddTextLetterByLetter` (ou `Write` com `stroke_width ≤ 0,7`) e, quando terminam, **não sobra traço**. O borrado de 864–880 s (E41) é o traço grosso da caneta sobre letra pequena;
  - nunca a mesma informação em dois lugares da tela (S1 tinha a lista duas vezes).

---

## 3. Correções por defeito (E01–E42)

Os tempos são do preview v1. O quadro de cada um está em `erros_v1/`. O aceite vale no quadro do mesmo gatilho do v2, e a prancha do §7 mostra os pares antes × depois.

| # | t (v1) | bloco | o que está errado | troca | aceite |
|---|---|---|---|---|---|
| E01 | 36–56 s | H1/H2 | palco parado 20 s; `TRAVA` em cima das linhas; discos com raio ~250 px; `e^{−y²}?` minúsculo | discos com raio ≥ 300 px (palco de 0 a 1880 px de largura, sem coluna no hook); `TRAVA` na ponta de cada linha, fora do disco, com folga ≥ 10 px; `e^{−y²} ? SEM PRIMITIVA ELEMENTAR` com fonte ≥ 40/30 px. **No H2** ("quanto vale a área de cada pedaço"): a célula quadrada da esquerda escorrega da origem para a borda **sem mudar de tamanho**; ao mesmo tempo, a célula polar da direita escorrega e **cresce** (4 s, ida e volta uma vez) | nenhuma janela de 5 s parada; rótulo × linha = 0 |
| E02 | 64 s | A1 | moldura do chip antes do texto | o chip nasce com o texto (G4) | caixa vazia = 0 |
| E03 | 112 s | B1-1 | tick `1` duplicado no eixo x (`11`) | um rótulo só | — |
| E04 | 128 s | B1-2 | palco só com os eixos rθ por ~4 s; miniatura do triângulo cortada no canto, com rótulos de 16 px | o retângulo rθ se desenha logo no gatilho; a miniatura sai (o triângulo já foi visto no B1-1) | palco vazio = 0 |
| E05 | 156–168 s | B1-2 | `r = 0` em cima do eixo θ; `r = 0 → ORIGEM` sobre a grade do disco | `r = 0` à esquerda do eixo θ, entre os ticks `π` e `2π`, com folga ≥ 10 px; `r = 0 → ORIGEM` fora do disco, com linha-guia até a origem | rótulo × eixo = 0 |
| E06 | 208 s | B2-1 | glifos em voo embaralhados na linha `= ½(r₂² − r₁²)Δθ` | G5 | duplicados = 0 |
| E07 | 236 s | B2-1 | `π/16` sobreposto a `π/6` | G5; a célula ganha o valor numa placa só | — |
| E08 | 240 s | B2-1 | a célula de fora fica gigante e passa da grade | a de fora ocupa exatamente r ∈ [1,5; 2] e um Δθ = π/6 (bordas sobre os arcos 1,5 e 2); a grade do palco vai até r = 2,2 | as bordas da célula coincidem com os arcos (≤ 2 px) |
| E09 | 256–300 s | B2-2 | a célula ampliada aparece sozinha, verde, sem eixos nem origem | **lupa**: a grade polar pequena com a célula fica à esquerda; a ampliação, num painel ao lado, ligada à célula pequena por duas linhas-guia finas. `r Δθ` (arco) e `Δr` (lado) por fora dos lados | o aluno vê de onde veio a célula |
| E10 | 284 s | B2-2 | esqueleto: `∂(x` e `∂(.` com operadores antes dos termos | G4 | prefixo = 100 % |
| E11 | 324–332 s | B2-3 | o erro clássico é escrito em 2 linhas minúsculas, na borda de baixo | **alvo `v2_02`**: coluna limpa, `SEM O r` (✗) em cima e `COM O r` (✓) embaixo, com as linhas da conta; o disco grande com o perímetro em ALERTA e a área em menta | igual ao alvo ±20 px; G1 |
| E12 | 336 s | B3-1 | palco vazio | G7 | — |
| E13 | 340–400 s | B3-1 | palco quase parado por 60 s | no gatilho "interior", o interior acende (preenchimento 0 → 30 %, 1 s); em "falha", a origem e a costura engrossam em ALERTA (traço 2 → 5 px); em "duas metades", **cada metade do retângulo se deforma por φ** até a metade do disco (homotopia de 2 s, a grade junto); em "a soma", as duas metades piscam uma vez cada, na ordem da fala | nenhuma janela de 5 s parada |
| E14 | 404 s | B3 | `NO INTERIOR: …` colado no tick `π`; limites `π` e `0` soltos à esquerda da linha das duas integrais | a legenda vai abaixo do palco, com folga ≥ 20 px; os limites pertencem ao MathTex (G5) | glifo solto = 0 |
| E15 | 448 s | B4-1 | palco vazio | o sino entra por corte no 1º quadro do B4-1 | — |
| E16 | 500 s | B4-1 | glifos duplicados em `= −e^{−u}/2 …` | G5; coluna paginada (G2): página 1 = C4-1…C4-3; página 2 = C4-4…C4-7 com o chip `x² + y² = r², dA = r dr dθ` no topo; página 3 = C4-8 com o chip `∫₀¹ e^{−r²} r dr = (1 − 1/e)/2 ≈ 0,316` | duplicados = 0; ≤ 6 linhas |
| E17 | 470–548 s | B4 | rótulo `y` numa caixinha sobre a superfície; miniatura rθ cortada na borda esquerda | `y` na ponta visível do eixo, fora da superfície; a miniatura vai para x ≥ 60, com ≥ 200 px de altura | G6 |
| E18 | 532 s | B4-2 | anel laranja flutuando no topo da tela, sobre o canto | **refeito pela cena `casca`** (§4.1) | nada do 3D acima de y = 170 |
| E19 | 533 s | B4-2 | parede cinza translúcida e placa escura vazia | §4.1; G4 | placa vazia = 0 |
| E20 | 540 s | B4-2 | anel lima só com **meia circunferência**, mais um raio do centro; blob lima do `2πr` em voo | §4.1: o anel lima se desenha **inteiro, 0 → 2π**, sem raio; o `2πr` é escrito a caneta no rótulo e depois **voa** do rótulo para a coluna | o arco do anel cobre 360° no fim do traço; blob = 0 |
| E21 | 546 s | B4-2 | `2π r · e^{−r²}` sobre a base da parede; `PAREDE DA CASCA` sobre a parede; falta o `dr` | §4.1, alvo `v2_01`: três rótulos fora da casca (`COMPRIMENTO 2πr`, `ALTURA e^{−r²}`, `ESPESSURA dr`) e, na coluna, `≈ 2πr · e^{−r²} · dr` | igual ao alvo ±20 px |
| E22 | 552–570 s | B5 | palco só com os eixos por 18 s | o disco de centro (1, 0) se desenha no 1º gatilho ("não está centrada na origem"), antes da coluna | — |
| E23 | 580–650 s | B5 | disco com raio ~190 px; `θ = π/2` e `θ = −π/2` sobre o eixo y; `θ = π/3 ⇒ r = 1` encostado no eixo e no raio | disco com raio ≥ 285 px (alvo 07); os rótulos de ±π/2 à direita do eixo y, na altura das pontas, com folga ≥ 10 px; a placa de π/3 ao lado do ponto coral, por fora da circunferência | G6; ±20 px do alvo 07 |
| E24 | 624 s | B5 | glifos embaralhados na linha `ÁREA = ∫∫ r dr dθ` | G5 | — |
| E25 | 648 s | B5→B6 | palco vazio | G7: a curva `e^{−x²}` do B6-1 começa a se desenhar no quadro em que o disco sai | — |
| E26 | 664 s | B6-1 | `−a` e `I(a)` duplicados | G5 | — |
| E27 | 704 s | B6-1 | o `gauss` aparece **de cima e achatado** antes de subir | no gatilho "o sino girado", corte para o `gauss` **na câmera oblíqua do alvo 08**, com o sino crescendo (`cresce` 0 → 1). A vista de cima só existe no B6-2, depois de "região maior" | nenhum quadro do `gauss` com câmera de cima antes do B6-2 |
| E28 | 708–720 s | B6-1 | o sino sai pela borda esquerda; `D_a` encostado | G3: caixa do alfa em x ≥ 40 | — |
| E29 | 720 s | B6-2 | `MEIA DIAGONAL` numa placa sobre o sino, com `a√2` em cima | a chave da meia diagonal e `a√2` ficam fora do sino, no chão, com linha-guia | G6 |
| E30 | 724 s | B6-2 | esqueleto `⊂ Q_a ⊂ , e^{−(` com buracos para os voos | G4 (a caneta espera o pouso) | prefixo = 100 % |
| E31 | 728–740 s | B6-2 | linhas brancas (as faixas do Fubini do B6-1) cruzando para fora do quadrado | nada do 2D do B6-1 fica na vista de cima; só o quadrado, os dois discos, os raios e os rótulos do alvo `v2_03` | — |
| E32 | 744–784 s | B6-2 | expoentes faltando; `a` e `a√2` em caixinhas de ~16 px; coluna e tabela pequenas | **alvo `v2_03`**: palco de cima com o disco circunscrito de raio ≥ 360 px, rótulos ≥ 40 px, coluna e tabela na escala G1 | ±20 px do alvo |
| E33 | 788 s | B6-3 | `∫.` solto no meio da tela | G4/G5 | glifo solto = 0 |
| E34 | 800 s | B6-3 | `e^{−x²/2} dx` com glifos sobrepostos | G5 | — |
| E35 | 804 s | B6-3 | `√2 · √π` embaralhado | G5 | — |
| E36 | 808 s | B6-3 | a fração `1/√(2π)` com o `1` e a barra antes do denominador; blob no rótulo da curva | G4: `1/√(2π)` é escrita por inteiro, e o `√(2π)` do denominador **voa** do resultado da coluna; o rótulo da curva fica fora dela | — |
| E37 | 816–832 s | B7 | metade direita da tela vazia | **alvo `v2_04`** + narração v2.1 (§5): a coluna escreve `x = 1 ⇒ r cos θ = 1 ⇒ r = sec θ`, a linha do `cossec` e as duas integrais | — |
| E38 | 836–844 s | B7 | caixa `POLARES:` vazia antes do texto; `DUAS INTEGRAIS` na borda de baixo | sem caixa: `POLARES VALEM A PENA QUANDO` com dois ✓ (alvo `v2_04`); `DUAS INTEGRAIS` na coluna | G4; G6 |
| E39 | 848 s | S1 | caixas vazias, `dA ¬` e `↑` soltos | **alvo `v2_05`**: três painéis, cada um nascendo com o seu título | — |
| E40 | 852 s | S1 | ✓ solto; `dA = r dr dθ` duplicado | idem | — |
| E41 | 864–884 s | S1 | `SETORES · ARCO × LADO · DETERMINANTE` borrado; a mesma lista à esquerda e embaixo à direita | G8; uma lista só (os três painéis) | — |
| E42 | 888–910 s | S2 | o meio disco é feito de anéis de traço iguais: não mostra "mais pesado na borda"; o palco ocupa só a metade de cima | **alvo `v2_06`**: o tom **cresce com r** (40 setores de anel, do escuro no centro ao claro na borda), meio disco de raio 400 px, cartão `NO PRÓXIMO VÍDEO` ≥ 8 s | ±20 px do alvo |

---

## 4. Mudanças de conteúdo e alvos novos

### 4.1 B4-2 · a casca com o anel inteiro (alvo `v2_01`, cena 3D `casca`)
A cena nova está em `c3d34t2.html?k=casca` (porte para a unidade como os outros estados).

- **Geometria** (mesmos `SC = 2`, `ZS = 0,95` do `sino`): o sino **inteiro vira traço** `#6C7698` (anéis em r = 0,25, 0,42, 0,84 e 1, e 8 meridianos), e só a **casca fina** fica opaca:
  - parede de fora em r₁ = r₀ + 0,10, laranja escurecido com o tom por ângulo;
  - parede de dentro em r₀, laranja mais escuro;
  - o teto da casca é a faixa do próprio sino entre r₀ e r₁, com a cor por altura (ciano);
  - bordas de cima em `#FF9440` vivo;
  - no chão, o **anel lima** `#C6F26B` em r₁, um tubo fechado.
- **Câmera:** `ver([7.0, −6.3, 6.4], [0, .05, .45], 540, 560)`; no alvo, o PNG entra com `esc = 0,92`, `(dx, dy) = (10, 40)`. Enquadre por `setViewOffset` (G3).
- **Estados:**
  - `r0` (de 0,10 a 0,85; no fim, 0,45);
  - `anel` 0 → 1: o tubo lima cresce em θ de 0 a **2π** (anel inteiro, sem raio ligando ao centro);
  - `traco` 0 → 1: a passagem do sino opaco do B4-1 para o traço, junto com a casca acendendo (1 s). A peça não se separa.
- **Pontos para o Manim** (exportados por quadro, como no `sino`): `baseFrente`, `paredeTopo`, `paredeBaixo`, `tetoDentro`, `tetoFora`, `raioPe`, `pico`, `ex`, `ey`. Os rótulos andam com a casca quando `r0` muda.
- **Gatilhos** (narração v2.1, §5):
  - "volume" → `VOLUME ≈ 1,99` perto do `pico` (como no v1);
  - "cada anel fino" → `traco` 0 → 1 e a casca entra em r₀ = 0,45;
  - "uma altura só" → a casca **anda**: r₀ de 0,45 a 0,10, depois a 0,85 e de volta a 0,45 (5 s, suave). A altura da parede muda junto;
  - "o comprimento é dois pi erre" → `anel` 0 → 1 (2 s) e `COMPRIMENTO 2πr` (lima) com linha-guia até `baseFrente`;
  - "a altura" → a chave vertical ciano ao lado da parede e `ALTURA e^{−r²}`;
  - "a espessura" → `ESPESSURA dr` com seta até a faixa do teto;
  - "O volume da casca" → a coluna limpa (G2) e escreve `VOLUME DE UMA CASCA` / `≈ 2πr · e^{−r²} · dr`. O `2πr`, o `e^{−r²}` e o `dr` **voam dos três rótulos**; os `·` são de caneta;
  - "Somando as cascas" → a casca anda de r₀ = 0,10 a 0,85 mais uma vez, e a coluna escreve `∫₀¹ 2π r e^{−r²} dr = 2π ∫₀¹ e^{−r²} r dr` (glyph map: o `2π` sai da integral);
  - "acabou de fazer" → o `(1 − 1/e)/2` **voa do chip** `∫₀¹ e^{−r²} r dr = (1 − 1/e)/2` (página 3 do B4-1, E16) para a linha `= 2π · (1 − 1/e)/2`;
  - "De novo" → `= π(1 − 1/e)` em menta e a legenda `O MESMO VOLUME: ANÉIS × CASCAS`.
- **Conta (conferida no sympy):** ∫₀¹ 2πr e^{−r²} dr = 2π · (1 − e^{−1})/2 = π(1 − 1/e) ≈ 1,986.

### 4.2 B2-3 · o teste da unidade (alvo `v2_02`)
Ver E11. A conta do `COM O r` tem o degrau `[r²/2]₀ᵃ → (a²/2 − 0)` escrito, como na narração ("de zero a á, que dá á ao quadrado sobre dois"). O palco tem:
- o perímetro desenhado em ALERTA no gatilho "dois pi á";
- a área pintada em menta no gatilho "pi á ao quadrado".

### 4.3 B6-2 · entre dois discos (alvo `v2_03`)
Ver E27–E32. Depois que a câmera sobe e o 2D entra (≤ 2 px), o palco de cima fica como no alvo:
- o quadrado com o sino visto de cima (o próprio último PNG, ou o 2D com o degradê radial);
- os dois discos e os dois raios (`a` em azul-claro na vertical, `a√2` em coral na diagonal);
- os rótulos `Q_a`, `D_a` e `D_{a√2}` nas placas.

A coluna fica em 6 linhas + o chip `I(a)² = ∬_{Q_a} …`. Na tabela, as linhas entram nos gatilhos "á igual a um / dois / três". O resultado `√π` vai em duas linhas (o alvo mostra a quebra).

### 4.4 B7 · o quadrado em polares (alvo `v2_04`)
- **Palco:** o quadrado [0, 1]² grande, a metade de baixo azul-claro a 22 % e a de cima coral a 20 %, e a diagonal tracejada `θ = π/4`. Um raio laranja **varre** de θ = 0 a π/2 (`ValueTracker`, 4 s). O ponto de saída anda na borda e muda de cor ao passar de lado (azul-claro → coral). Depois, dois raios fixos ficam de exemplo, com `r = sec θ` e `r = cossec θ` nas placas.
- **Coluna:** as duas linhas de dedução, as duas integrais e `DUAS INTEGRAIS` / `EM x E y: UMA SÓ`. Depois, `POLARES VALEM A PENA QUANDO` com dois ✓ (sem caixa).

### 4.5 S1 · síntese em três painéis (alvo `v2_05`)
Os três painéis entram um por vez, cada um no seu gatilho:
- **"o pedacinho de área"** → painel 1, `O FATOR`. A célula lima escorrega para fora e cresce, uma vez. Em "três caminhos", entra a legenda `SETORES · ARCO × LADO · DET`;
- **"o disco deu"** → painel 2;
- **"o sino inteiro deu raiz de pi"** → painel 3; o `√π` voa do cartão do canto, que sai.

### 4.6 S2 · o gancho (alvo `v2_06`)
Ver E42. O meio disco se pinta **do centro para a borda** (os 40 setores de anel acendendo em ordem de r, 2 s) no gatilho "a densidade cresce junto com a distância". Em "um lápis", o lápis sobe de baixo. O `?` entra em "Onde ele equilibra?". O cartão fica ≥ 8 s antes do CTA.

---

## 5. Narração v2.1 (três trechos mudam)

O arquivo completo está no zip como `yt_0037_narracao_v2_1.md`. As mudanças:

1. **B4-1** (não citar vídeo que pode não estar publicado; sai também a legenda `O MESMO NÚMERO DO SINO`):
   - antes: *"Repara: é o mesmo número do sino do vídeo da troca de ordem, zero vírgula três um seis."*
   - agora: *"Guarda esse número: zero vírgula três um seis."*
2. **B4-2** (a casca com espessura e a soma das cascas), inteiro:
   > [thoughtful] E esse número tem cara: é o volume debaixo do sino, em cima do disco. Dá até para ver o erre no desenho. Como a função só depende da distância, cada anel fino tem uma altura só, é elevado a menos erre ao quadrado. Em cima do anel de raio erre e espessura dê erre fica uma casca: o comprimento é dois pi erre, a altura é é elevado a menos erre ao quadrado e a espessura é dê erre. O volume da casca é o produto: dois pi erre, vezes é elevado a menos erre ao quadrado, vezes dê erre. Somando as cascas de zero a um, sai a integral de zero a um de dois pi erre, é elevado a menos erre ao quadrado, dê erre: dois pi vezes a integral que a gente acabou de fazer, que deu um menos um sobre é, sobre dois. De novo, pi vezes um menos um sobre é. A fatia das polares é o anel, ou, em três dimensões, uma casca, e o comprimento do anel é que traz o erre.
3. **B7** (os degraus do sec e do cossec, que agora aparecem na coluna), inteiro:
   > [serious] Mas polar não é botão mágico. Num quadrado, o raio sai ora pelo lado xis igual a um, ora pelo lado ípsilon igual a um. No lado xis igual a um, erre cosseno de teta é um, então erre é secante de teta. No lado ípsilon igual a um, erre seno de teta é um, então erre é cossecante de teta. A integral racha em duas, em teta igual a pi sobre quatro: de zero a pi sobre quatro, erre vai até secante de teta; de pi sobre quatro a pi sobre dois, até cossecante de teta. Em xis e ípsilon, o quadrado é a região mais simples que existe. Polar vale a pena quando a região tem simetria em torno da origem, um disco, um anel, um setor, ou quando o integrando tem xis ao quadrado mais ípsilon ao quadrado. Melhor ainda quando tem os dois.

**Tempos** (0,15 + palavras/3 + 0,35 s por âncora; só estas mudam):

| Âncora | v2 | v2.1 |
|---|---:|---:|
| B4-1 | 220 p · 1:13.8 | 210 p · 1:10.5 |
| B4-2 | 87 p · 0:29.5 | 180 p · 1:00.5 |
| B7 | 99 p · 0:33.5 | 147 p · 0:49.5 |
| **Total** | 2724 p · 15:17.5 | **2855 p · 16:01** |

---

## 6. O que NÃO fazer

- Não mudar a matemática, a ordem dos blocos, as cores nem o fundo.
- Não acrescentar efeito (brilho, partícula, sombra, pulsação em loop). As animações novas do §3/§4 são todas de conteúdo: escorregar, varrer, deformar por φ, pintar em ordem de r.
- Não usar `FadeIn` de fórmula pronta nem `Succession(Wait…)`/`AnimationGroup` que ponham o destino na tela antes da hora.
- Não deixar índices de glyph map, `bounding_box` nem debug no render.
- Não fazer o 3D dentro do Manim.
- Não começar voz, SRT, 1080p ou entrega.

---

## 7. QA do preview v2 (obrigatório)

Tudo em `renders/v2/qa/`. Cada relatório lista os eventos com o tempo e o bloco. **O critério é zero**, salvo onde está escrito outro número.

1. **`erros_v1_antes_depois.jpg`:** os 42 pares (quadro de `erros_v1/` × quadro do v2 no mesmo gatilho), 2 por linha, com o código E<nn>. Para cada um, uma linha em `erros_v1_status.txt` dizendo **corrigido** ou o motivo.
2. **`sobreposicoes_v2.txt`**, amostrado a cada 0,5 s, também durante as animações. Agora entram:
   - texto × texto (> 2 px);
   - texto × traço: eixo, curva, aresta, borda de região, seta, raio, linha-guia alheia. Folga mínima de **10 px** (G6);
   - texto × **3D**: a caixa do texto contra o alfa > 0 do PNG do mesmo quadro. Só passa com `placa_min` e se o rótulo nomeia aquele objeto (lista branca no relatório);
   - texto × **borda**: caixa a menos de 40 px da borda da tela, ou cortada;
   - **o glifo em voo também entra**, contra tudo o que não é o seu destino.

   Fica de fora só o papel (z ≤ −9).
3. **`esqueleto_v2.txt`:** para cada MathTex em escrita, em cada quadro, os glifos visíveis formam um prefixo na ordem de leitura, contando o pouso dos voos (G4). E também: chip, placa ou painel visível com o texto ainda vazio.
4. **`duplicados_v2.txt`:** ao fim de cada `play`, nenhum par de glifos visíveis com IoU > 0,3 e mesma forma, e nenhum glifo fora da caixa final da sua fórmula (G5).
5. **`tipografia_v2.txt`:** a altura medida do algarismo/maiúscula de cada classe do G1, com o mínimo de cada bloco.
6. **`palco_v2.txt`:**
   - **palco parado:** janela de 3 s em que menos de **1 % da área do palco** (sem coluna e sem canto) muda mais de 8 níveis. Liste as de 3 a 5 s com o motivo; acima de 5 s, zero;
   - **palco vazio:** mais de 0,5 s com menos de 2 % da área do palco diferente do fundo violeta (o canto e o cartão `√π ?` não contam);
   - **coluna:** linhas visíveis por quadro (≤ 6, G2);
   - **3D dentro da tela:** caixa do alfa em x ∈ [40, 1010] e y ∈ [170, 1050] (G3).
7. **`casca_v2.txt`:** no fim do estado `anel = 1`, o arco lima projetado cobre 360° (amostre 72 ângulos sobre o círculo r₁ no chão: todos com pixel lima visível ou atrás da casca), e não existe segmento lima do centro até o anel. A coluna do B4-2 tem `· dr`.
8. **Render × alvo:** os 6 alvos `v2_*` e os 9 do v1 que continuam, ±20 px.
9. **Conta inteira:** `conta_inteira_v2.txt` com os degraus novos (B4-2, B7, B2-3) e o tempo de cada um.
10. `alinhamento3d_v2.txt` (≤ 2 px, agora também para a cena `casca`) e `tempos_render_v2.txt`.

---

## 8. Parada

Entregue o preview v2, a pasta `qa/` e o relatório do AGENTS.md:
1. os arquivos alterados;
2. as verificações com os resultados;
3. o caminho do preview;
4. o que ficou pendente.

E pare. Voz, 1080p e entrega só depois que o Kaio aprovar o v2.
