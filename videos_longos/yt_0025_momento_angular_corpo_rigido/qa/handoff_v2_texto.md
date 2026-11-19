

<pasted_content id="6091">
# yt_0025 "Momento angular do corpo rígido" · avaliação do preview v1 e HANDOFF v2

2026-11-08 · preview avaliado: `preview_yt0025_v1_960x540.mp4` (14:07, 960×540, 15 fps; 22 pranchas a 0,5 fps e 20 quadros cheios conferidos).
Complementa o `yt_0025_handoff_v1.md`. **Onde divergem, vale este.** Continuam valendo: física e números do Anexo B, cores das grandezas, operadores neutros, fundo de estrelas contínuas, Three.js com acabamento HDR/PBR, sem caixas, sem livros na tela, sem citar vídeo futuro. A narração v1 continua valendo, **exceto** os trechos trocados no §4 (narração v1.1).

---

## 0. Veredito do v1

### Funcionou (manter)
- A estrutura pêndulo → corpo → haltere → eixo principal → mancais → roda está inteira, na ordem, e a física dos blocos B1, B2, B3-5 e B5 está certa nos números (ω = 3,36 rad/s, período de 1,87 s, L_z = 0,113, L_⊥ = 0,196, τ = 1,23 N·m, F = 3,1 N, F_c = 2,37 N, binário de 6,9 N·m).
- Cadeias certas e bem escolhidas: o cancelamento do pêndulo até ω² = g/(ℓ cos θ) (2:56–3:18); r⃗ᵢ = ρ⃗ᵢ + zᵢ ẑ com a distributiva (4:24–4:54); a dos dois sinais de menos (6:42–7:04); a conferência pelas forças (10:34–11:02).
- A vista lateral do haltere (7:24–7:42): L⃗ inclinado para o lado da massa de baixo, a 60° do eixo e com o ângulo marcado. O sinal está certo.
- A paleta, o canto, o selo único, o sublinhado no resultado e a câmera lenta com selo na roda e nas 3 voltas/s.

### Ainda ruim (P0 = bloqueia o v2)
1. **P0 · Caneta e ordem.** A álgebra não usa a caneta (regra já registrada no `docs/padrao_video_longo.md` e no `AGENTS.md`) e **não é escrita da esquerda para a direita**: termos que voam do desenho **pousam no meio da linha antes** dos termos à esquerda deles, e os operadores aparecem depois, preenchendo os buracos. Ver §1.
2. **P0 · Erros de conceito no desenho** (§2): na roda, L⃗_⊥ e as forças dos apoios estão **ao longo do eixo** (deveriam ser perpendiculares e girar); no haltere, as forças dos dois mancais **não são opostas**; a cena "DE OUTRO PONTO" mostra o pêndulo pendurado reto; o rótulo `L_⊥` continua na tela depois de L⃗_⊥ = 0; `sin` em vez de `sen`.
3. **P0 · Hook, encerramento e gancho** fracos (§3 e §4). O Kaio pediu explicitamente para melhorar os três.
4. **~24 sobreposições** (contagem do Kaio). O §5 lista as que eu achei nos quadros, com o tempo de cada uma.
5. **Visual** (§6): objetos pequenos (pêndulo e haltere com ~30–35% da altura da coluna, meta de 55–75%); a batata **cortada na borda de baixo** e **quase preta** sobre o fundo; a coluna da direita com metade vazia; o passo-chave do B3-4 (os dois L⃗ᵢ somando na origem) **virou texto** (`VERTICAL COM VERTICAL`, `AS DUAS PARTES SE SOMAM`) em vez de animação.

---

## 1. P0 · Caneta e ordem da escrita

### 1.1 Regra (já nos docs; aqui só o que reprovou)
A regra **"Escrita da álgebra: caneta"** do `docs/padrao_video_longo.md` (e as linhas correspondentes do `AGENTS.md`) vale **inteira** para esta unidade. Ler a seção antes de mexer. A implementação de referência é a do `yt_0023` (`Vez()` em `prob2.py`, primitiva `escreve`, auditorias `FLASH POR QUADRO` e `CANETA`): copiar para esta unidade, sem alterar o `yt_0023`. Em resumo: termo novo = caneta, glifo a glifo, da esquerda para a direita (traço finíssimo, ponta branca, 0,6 s por glifo, um glifo a cada 0,30 s; **no preview 960×540, traço 1,5 px e ponta 4 px** para a caneta ser visível); termo com origem no desenho = voo (`TransformFromCopy`); manipulação = `TransformByGlyphMap`; nada de `FadeIn` de linha pronta; nada de destino visível antes da vez.

### 1.2 O defeito que o Kaio viu ("vai coisa do nada no meio da equação")
O voo hoje sai do desenho **no começo do passo** e pousa na posição final **antes** de a caneta escrever o que fica à esquerda dele. Resultado: buracos na linha que depois se preenchem. Exemplos do v1:

| Tempo | O que aparece primeiro | Depois |
|---|---|---|
| 0:58 | `L⃗   r⃗   p⃗` soltos | `=` e `×` preenchem |
| 1:42 | `R` duplicado sobre `R = ℓ sin θ` | — |
| 1:48 | `θ` voando alto no meio da linha | `= ‖L⃗‖ sin` |
| 2:22–2:30 | `L_h` pousado à direita | `‖dL⃗‖ =` e `· ω dt` |
| 2:42 | `τ = m` com `g` no expoente (pousando) | — |
| 3:00 | `g   ℓ   θ` espalhados | `= ω² … cos` |
| 3:08 | `ω` sozinho | `² = g/(ℓ cos θ)` |
| 4:24–4:36 | `r⃗ᵢ   ρ⃗ᵢ   zᵢ ẑ` | `=` e `+`; `zᵢ` voa de baixo |
| 5:20–5:26 | `L_z =        ω` (buraco) | `I_z` voa para o buraco |
| 7:28 | `L_z = ²` (expoente antes da base) | — |
| 7:36 | `L_⊥ = 2` sozinho | — |
| 9:34 | `‖dL⃗/dt‖ =   L_⊥` (buraco) | `ω` |
| 10:08 | `d` sozinho no lugar final | `τ = F` |
| 10:54 | `τ = 2,37 · ⁰` | — |

### 1.3 Correção
1. **Fila única por x, inclusive para os voos.** Em cada linha, os tokens entram estritamente em ordem crescente de x. Um voo **só sai do desenho quando chega a vez dele**, isto é, quando o glifo imediatamente à esquerda terminou. Ele pode voar 0,4–0,6 s, mas pousa antes de o próximo glifo à direita começar. Operadores (`=`, `+`, `×`, `·`) são escritos pela caneta **na vez deles**, nunca depois.
2. **Expoente, índice, fração e raiz** entram junto com a base (bloco), nunca antes dela.
3. **Linha de números**: a linha literal termina inteira antes; depois, os números substituem um por vez, da esquerda para a direita.
4. **Auditoria `ORDEM POR X` (nova, FALHA):** para cada linha, o instante de pouso de cada token (voo ou caneta) deve ser crescente em x (tolerância de 0,05 s). Relatório `ordem.txt` com zero eventos. Os 14 casos da tabela acima entram como teste de regressão.
5. **`FLASH POR QUADRO` = 0** e **`CANETA`** (nenhum termo novo por `FadeIn`) = 0, como no yt_0023.
6. **Prova antes do resto:** `renders/prova_caneta_yt0025.mp4` (≈ 20 s, 960×540, dentro do zip de QA): B1-6 inteiro (o cancelamento) e B2-4 (`L_z = (Σ mᵢ ρᵢ²) ω → L_z = I_z ω`), sem corte.

### 1.4 Notação
- `\sin` → **`\operatorname{sen}`** em todo o vídeo (pt-BR; θ e α continuam). `\cos` fica.
- Módulo com **uma barra**: `|L⃗|`, `|dL⃗/dt|` (não `‖ ‖`).
- O período do pêndulo (`T`) em **branco** (é tempo), não azul.
- Unidades com ponto: `kg·m²/s`, `N·m`.

---

## 2. P0 · Conceitos (o desenho contradiz a física)

| # | Onde | Erro | Correção |
|---|---|---|---|
| C1 | Roda, 11:42–12:58 | `L_par` e as setas azuis dos apoios estão **ao longo do eixo da roda**. A parte transversal de L⃗ e as forças dos apoios são **perpendiculares ao eixo** e **giram com a roda** | L⃗_⊥ (rótulo `L⊥`, não `L_par`) radial, no plano (eixo, excessos), girando com a roda. Forças dos apoios radiais, opostas entre os dois apoios, girando em fase. Auditoria `RODA`: ângulo entre L⃗_⊥ e o eixo = 90° ± 1°; idem para as forças |
| C2 | Roda, todo o B6 | Só **um** pedestal; a roda fica em balanço. A fala diz "os apoios" | **Dois** pedestais com mancal, um de cada lado da roda (como no §4.1 do v1). As forças aparecem nos dois |
| C3 | Haltere, 10:08–10:30 e 11:04–11:16 | As setas dos dois mancais **não são opostas** (uma para baixo à esquerda, outra para baixo à direita na tela). A cota `d = 0,40 m` está fora do lugar, longe dos mancais | Forças horizontais e **antiparalelas** (mesma reta de ação vista de cima, sentidos opostos), presas aos centros dos mancais. A cota GEO vai de um mancal ao outro, encostada no eixo. Auditoria: ângulo entre as projeções na tela = 180° ± 2° |
| C4 | Pêndulo, 3:38–3:52 (`DE OUTRO PONTO`) | O pêndulo aparece **pendurado reto** (fio vertical, sem bolinha), e as setas ficam no piso | **Cortar o B1-8** (já era cortável e confunde). Se ficar, o pêndulo continua girando a 30° e só a origem desce |
| C5 | B4-1 (8:22–8:44) e B4-3 (9:12–9:26) | O rótulo `L⊥` continua na tela, com linha-guia apontando para o nada, depois de L⃗_⊥ = 0 | Quando a parte transversal zera, o rótulo `L⊥` some junto com a seta. Só `L⃗` (vertical) fica |
| C6 | Hook e B5 | Setas horizontais que apontam para a câmera parecem verticais (33 s: τ⃗ parece descer) | Toda seta horizontal importante ganha uma **sombra fina** projetada num plano horizontal de referência (o piso ou um anel GEO a 15%), e a câmera respeita a regra do §4.5 do v1 (seta ≥ 60% do comprimento verdadeiro na tela) |
| C7 | B5, 9:28–10:06 | Não dá para ler que τ⃗ é **perpendicular ao plano (eixo, haste)**: o plano é visto quase de frente e τ⃗ parece estar nele | Inset `VISTA DE CIMA` mostrando o plano como uma **linha** (de cima, o plano eixo–haste é uma reta) e τ⃗ perpendicular a ela. Auditoria `HALTERE` do v1, medida |
| C8 | B3-6, 7:44–8:02 | Os "retângulos massa × altura × raio" são grandes blocos rosa **cobrindo as massas** | Retângulos de **contorno** rosa (preenchimento 15%), lados z e ρ sobre as cotas, sem cobrir as esferas; os dois acendem iguais lado a lado |
| C9 | B2-4 | Falta a imagem da soma: os cubinhos não empilham fatias em L_z | Implementar a onda do §5 do v1 (cada cubo empilha uma fatia na seta vertical). É a imagem que justifica L_z = I_z ω |

---

## 3. Hook novo (v1.1)

O pêndulo segue no vídeo como **primeiro passo** (B1), mas sai do hook. O hook do v1 era abstrato: uma seta de torque saindo de um prego, um pêndulo pequeno e uma frase. O hook novo mostra um **efeito** que o público vê e não sabe explicar, com o objeto que é o núcleo do vídeo.

### 3.1 Cena `bancada_dupla` (Three.js)
- Duas bancadas **idênticas** às do `haltere_torto`, lado a lado (centros a ±0,75 m), mesma câmera 3/4 (`D_34`, 18° de elevação, as duas inteiras ocupando ~70% da largura).
- **Esquerda:** haltere **reto**, perpendicular ao eixo (α = 90°). **Direita:** haltere **torto** (α = 30°). Mesmas esferas e haste, CM no eixo nos dois.
- Os dois giram a **1 volta/s**; um mostrador violeta pequeno sobre cada um: `ω = 1 VOLTA/S` (iguais).
- **Base em pés de borracha:** a base do torto **balança** (inclinação em torno do eixo horizontal que tem a direção de τ⃗ naquele instante, amplitude 1,5° desenhada, selo `FORA DE ESCALA`, uma oscilação por volta, em fase com o binário dos mancais). A base do reto fica parada. Nenhuma outra diferença.
- **Física (conferida):** no reto, os produtos de inércia são nulos, L⃗ ∥ ω⃗, o binário é zero e a base não recebe esforço girante. No torto, o binário horizontal de 1,23 N·m gira com o haltere e balança uma base apoiada em pés flexíveis. O centro de massa não se move em nenhum dos dois, então não há força resultante, só o binário.

### 3.2 Narração v1.1 do hook (substitui H1–H3 e A2)

### H1 · tela: `D_34`; as duas bancadas girando; mostradores `ω = 1 VOLTA/S` iguais; rótulos pequenos `RETO` e `TORTO`
[curious] Dois halteres iguais, com a mesma massa, girando no mesmo tipo de motor, com a mesma velocidade angular. Nos dois, o centro de massa está bem em cima do eixo. A única diferença: um está reto, e o outro está torto.

### H2 · tela: a base do torto começa a balançar (`FORA DE ESCALA`); setas azuis finas nos dois mancais do torto, opostas, girando; a base do reto parada
[curious] Agora repara nas bancadas. A da direita balança, uma vez a cada volta. A da esquerda fica quietinha. Os mancais do haltere torto estão sendo empurrados, e esse empurrão gira junto com ele.

### H3 · tela: congela; topo `ω CONSTANTE… E MESMO ASSIM HÁ TORQUE`; hold de 2 s
[thoughtful] Só que a velocidade angular não muda, e o centro de massa nem sai do lugar. Então para que serve esse torque que os mancais fazem? Como pode existir torque sem a velocidade angular aumentar?

### A2 · tela: `MOMENTO ANGULAR DO CORPO RÍGIDO`; `NESTE VÍDEO:` e três ícones (cone · haltere torto · roda)
[thoughtful] Hoje o assunto é o momento angular de um corpo rígido, e a gente vai responder essa pergunta em três passos: primeiro uma bolinha num pêndulo, depois esse haltere torto, e no fim a roda de um carro. Os três contam a mesma história.

### B1-0 (nova) · tela: `P_34` **mais perto** (pêndulo com ~65% da altura da coluna), pêndulo cônico girando, mostrador `ω` constante; seta azul do torque do peso saindo do prego, com sombra no piso, girando junto com a bolinha
[thoughtful] Para entender o haltere, a gente começa com uma coisa mais simples: uma bolinha só. Nesse pêndulo, ela anda num círculo deitado, sempre com a mesma rapidez. E, em relação ao prego, o peso dela faz torque. De novo: torque, e a velocidade angular não muda.

**B1-1:** trocar a primeira frase ("Antes de somar muitas partículas, vamos entender uma só.") por **"Então vamos olhar para o momento angular dela."** O resto do B1-1 fica.

**Corte:** B1-8 sai (C4).

---

## 4. Encerramento e gancho novos (v1.1)

### 4.1 Síntese responde o hook

### S1 · tela: `D_34` de novo, as duas bancadas girando; no torto, L⃗ inclinado girando e a base balançando; no reto, L⃗ vertical parado; à direita, escritas uma a uma: L_z = I_z ω · τ⃗ = dL⃗/dt · Eixo principal: L⃗ = I ω⃗; depois os três cartões `PANEL` do v1
[calm, satisfied] Então, por que só a bancada do haltere torto balança? Porque, no haltere torto, o momento angular não aponta ao longo do eixo. Ele fica inclinado e gira junto com o haltere. Um vetor que gira está mudando, e mudar o momento angular exige torque. Quem faz esse torque são os mancais, e o empurrão deles, girando, balança a bancada. Esse torque é perpendicular ao eixo, por isso não muda a rapidez do giro: ele só muda a direção do momento angular. No haltere reto, o eixo é principal, o momento angular fica alinhado e ninguém precisa empurrar nada. Resumindo: a componente ao longo do eixo é sempre o momento de inércia vezes a velocidade angular. Mas o vetor inteiro só fica paralelo ao eixo quando o eixo é principal.

### 4.2 Gancho de conteúdo (substitui o S2 da batata)

**Cena `plataforma_livre` (Three.js):** plataforma circular de aço sobre um rolamento **livre** (sem motor, selo `SEM TORQUE EXTERNO`), com dois trilhos radiais e uma massa rosa em cada um; fios das massas até um carretel no centro. Mostrador violeta de ω. O carretel (mecanismo interno, a reação dele fica na própria plataforma) recolhe os fios: as massas vão de 0,40 m para 0,20 m do eixo e o mostrador sobe de **1 para 3 voltas/s**.
**Física (conferida):** I_plataforma = 0,020 kg·m², massas de 0,50 kg; I = 0,180 → 0,060 kg·m²; sem torque externo, L constante ⇒ ω × 3. **Nenhum número na tela além do mostrador**; nenhuma equação.

### S2 · tela: `plataforma_livre` girando; as massas deslizam para dentro; o mostrador vai de 1 para 3 voltas/s
[curious] E agora uma última cena. Uma plataforma girando livre, sem motor nenhum empurrando. Lá no meio, um carretel puxa as duas massas para perto do eixo. Nada de fora faz torque nela… e ela passa a girar três vezes mais rápido. Quem acelerou essa plataforma? E por que exatamente três vezes? É isso que a gente vai explorar quando o assunto for a conservação do momento angular.

### EN · tela: encerramento padrão; ao lado da pergunta, a roda pequena com **um** excesso só (o CM sai do eixo: um ponto rosa fora do eixo)
[happy] Se essas conexões ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos. E deixa nos comentários: se a roda tivesse um excesso de massa só, numa face só, os apoios sentiriam só um binário, ou alguma coisa a mais? Até a próxima!

- Sem quadro vazio entre o S2 e o EN (no v1 houve ~1 s vazio em 13:50).
- O gancho fala de um **assunto**, não de um vídeo; a frase "quando o assunto for" segue a regra de não prometer um vídeo específico.

---

## 5. Sobreposições (as que achei; o portão G28 deve listar todas e zerar)

| # | Tempo | Caso |
|---|---|---|
| S1 | 1:38–2:18 | `L_h` e `L_z` colados um no outro sobre o prego; rótulos menores que o mínimo |
| S2 | 1:42 | `R` duplicado sobre `R = ℓ sen θ` (cópia sobre o original, G14) |
| S3 | 2:04–2:18 | cone branco forte cobrindo o fio e a bolinha (preenchimento deve ser 0,08, não ~0,35) |
| S4 | 2:20–2:46 | inset `VISTA DE CIMA` encostado na seta L_h e no pórtico |
| S5 | 2:50–3:20 | `θ = 30°` e `g = 9,8 m/s²` empilhados em cima do pórtico e do fio |
| S6 | 4:04 e 4:16 | linha nova nasce **em cima** da linha-mãe durante o passo (dois Σ sobrepostos) |
| S7 | 4:24–5:58 | `r⃗ᵢ`, `ρ⃗ᵢ`, `zᵢ ẑ` amontoados na lateral da batata |
| S8 | 6:06–6:24 | `m = 0,40 kg` e `ℓ = 0,30 m` em cima da esfera e da haste |
| S9 | 7:24–7:42 | `L⊥`, `L_z` encostados no canto do plano; `m` duplicado solto (7:26, 7:36) |
| S10 | 7:44–8:02 | retângulos rosa sobre as massas (C8) |
| S11 | 8:04 | `PRODUTOS DE INÉRCIA` solto, longe das somas |
| S12 | 8:22–8:44 | `L_z`, `L⊥` e `L⃗` amontoados no topo do X |
| S13 | 8:34–8:38 | `= 0` órfão numa segunda linha |
| S14 | 9:28–9:44 | inset `VISTA DE CIMA` encostado na base do haltere |
| S15 | 9:36 | `L⃗` fantasma parado entre o desenho e a conta (voo que não terminou) |
| S16 | 10:34–11:02 | `ℓ`, `m`, `0,52 m` e `α` sobre o plano translúcido e a haste |
| S17 | 10:40 | `F_c` duplicado (dois `F_c` sobrepostos) |
| S18 | 11:04–11:16 | setas das 3 voltas/s saindo da tela pela borda de baixo |
| S19 | 11:18 | dois títulos de canto sobrepostos (`A RODA` sobre `O QUE OS MANCAIS FAZEM`) e as contas do B5 ainda apagando sobre a roda |
| S20 | 11:42–12:58 | `L_par` sobre o pneu e a seta azul atravessando o cubo |
| S21 | 12:22–12:36 | gráfico da senoide pequeno demais e encostado na base |
| S22 | 13:00 | crossfade roda → haltere com os dois objetos sobrepostos e o `EIXO PRINCIPAL` por cima |
| S23 | 13:40–13:48 | batata do S2 cortada na borda de baixo (sai com a cena nova) |
| S24 | 0:14–0:34 | frase do topo do hook longe do desenho e a seta τ⃗ cruzando o rótulo `r⃗` |

---

## 6. Visual

1. **Tamanho (G3):** pêndulo, haltere e roda com **55–75% da altura** da coluna esquerda. No v1: pêndulo ~30%, haltere ~35%, roda ~30%. Aproximar as câmeras; o L⃗ desenhado cresce junto (a escala de L⃗ do v1 continua, só a câmera chega mais perto).
2. **Batata:** não pode encostar na borda (nem a bancada); luminância do aço dos cubinhos **≥ 35%** (está ~10–15%, quase preta); AO só até 25%; contorno frio da contraluz visível. Forma de batata (três elipsoides **arredondados**), não de placa inclinada.
3. **Coluna da direita:** a `Pilha` mostra até **4 linhas** (a do v1 mostrava 2–3 e apagava o resto). O resultado sublinhado de cada bloco fica no alto da coluna até o fim do bloco.
4. **Sem texto no lugar da animação:** sai `VERTICAL COM VERTICAL`, `TRANSVERSAL COM TRANSVERSAL` e `AS DUAS PARTES SE SOMAM` (7:06–7:22). No lugar, o **B3-4 como especificado**: L⃗₁ e L⃗₂ grandes, cada um nascendo na sua massa, deslizam até a origem e se encaixam ponta com cauda. Câmera parada e mais perto (o haltere com ~70% da coluna). É o momento mais importante do vídeo.
5. **Cone do pêndulo:** preenchimento 0,08 e borda fresnel, como especificado; no v1 está branco leitoso.
6. **Roda:** os dois excessos têm que ser **vistos** (no v1 são pontinhos): rosa forte, 2× (`FORA DE ESCALA`), e o raio X ligado sempre que a fala falar deles.
7. **Sombra das setas horizontais** (C6) no hook novo, no B1 e no B5.

---

## 7. Ordem de trabalho e render

0. **Ler** `docs/padrao_video_longo.md` (seção da caneta) e `AGENTS.md`; copiar a implementação da caneta do `yt_0023` (`Vez()`, `escreve`, `flash23.py` e a auditoria `CANETA`) para a unidade.
1. **Caneta e ORDEM POR X** (§1) + prova `renders/prova_caneta_yt0025.mp4` + `ordem.txt` e `flash.txt` com zero.
2. **Conceitos** C1–C9 (§2).
3. **Hook novo** (`bancada_dupla`, §3) e **gancho novo** (`plataforma_livre`, §4); `ancoras.json` com a narração v1.1 (H1–H3, A2, B1-0, B1-1, S1, S2, EN trocados; B1-8 removida).
4. **Visual** (§6) e **sobreposições** (§5, G28 zerado).
5. **Render da onda 1:** PH (hook + abertura), PB1 e PB3 inteiros, 960×540 / 15 fps, sem voz. Quadros de conferência: H2, H3, B1-0, B1-5, B1-6, B3-3, B3-4 (**seis quadros consecutivos** do encaixe dos vetores), B3-5; **seis quadros consecutivos** de um passo com voo (mostrando o voo pousando na sua vez) e **seis** de um passo de caneta.
6. **Pare** e espere o Kaio aprovar a onda 1. Depois: PB2, PB4, PB5, PB6 e PS no mesmo padrão.
7. Sem voz, SRT, master, entrega, commit ou push. Relatório: arquivos alterados, verificações com resultado, caminhos e pendências reais. Falha de portão não é aviso menor.

## 8. Não reabrir
Física e números do Anexo B; pergunta guia; pêndulo → haltere → roda como fio da explicação (o pêndulo agora abre o B1, não o hook); eixo principal como condição (não simetria); matriz 3×3 fora; conferência pelas forças dentro; cores; caneta; fundo de estrelas contínuas; operadores neutros; sem livros na tela; sem citar vídeo futuro.
</pasted_content id="6091">
